"""Stage 3 — automated resolution study: Tier 1 -> Tier 2 promotion.

PLAN.md Stage 3 and WIN_CONDITION.md Tier 2. A GA elite is only a *candidate*
(Tier 1): a single-run blow-up signal is cheap to produce by under-resolving
the grid. To rule that out we rerun each elite at increasing spectral
resolution (N = 256, 512, 1024) and feed the resulting T* estimates through
`win_condition.resolution_converged`. A genome whose extrapolated blow-up time
stabilizes as the grid refines is promoted to NUMERICALLY_CONFIRMED (Tier 2);
one whose T* keeps drifting was a resolution artifact and stays a candidate.

Design decisions (documented so a reviewer can check them):

* **Operating point.** Each elite is rerun at the *exact frozen fitness
  config it was evolved under* — a, t_max, dt policy, tail_fraction, and
  energy budget are read back from that run's `config.json`, never
  re-guessed. Fitness itself is a nu_crit *bisection*; a resolution study is
  a single trajectory, so we must pick a viscosity. We study two, per elite:
    - an **inviscid anchor** (nu = 0): the cleanest, best-conditioned member
      of the blow-up regime, with no viscous dt stiffness. This is the
      sharpest test of the deepest open risk (PLAN.md: a smooth bandlimited
      genome is C-infinity and may not blow up at all, with growing N merely
      chasing an ever-smaller-scale near-singularity — a resolution artifact).
      Promotion is gated on convergence here.
    - a **viscosity-resistance** point (nu = viscous_frac * nu_crit, inside
      the blow-up band by monotonicity): confirms that the *viscosity-
      resistant* blow-up — the project's actually-novel property — also
      refines cleanly, not just the inviscid one. Reported alongside, and it
      can independently reach Tier 2, but the headline promotion uses the
      anchor.

* **Amplification threshold.** The cheap fitness oracle stops at 100x growth;
  at a fixed 100x stop, every resolution halts at the same physical growth, so
  T* agreement is almost tautological. The study raises the stop to
  `study_amplification_factor` (default 1e4 = four decades of 1/M -> 0) so
  refinement is actually stressed across many decades of growth. This is the
  one parameter deliberately *stricter* than the fitness config; everything
  else (a, nu policy region, t_max, dt) is frozen.

* **Artifact guard.** `conservation_drift` is recorded per resolution. A
  "blow-up" whose invariants drifted is distrusted regardless of a clean 1/M
  fit (LOGGING.md): if any blow-up run in the sequence exceeds
  `drift_threshold` (default 1e-3), the genome is NOT promoted even if T*
  looks converged, and the event records `drift_exceeded: true`.

Output (LOGGING.md schema #6): one `resolution_study` event per (genome, nu)
into a dedicated Stage-3 experiment directory, and any
`numerically_confirmed` hit mirrored into the cross-experiment
`experiments/promoted_candidates.jsonl`.
"""

import argparse
import json
import multiprocessing
import os
from pathlib import Path

import numpy as np

from ga.genome import Genome, realize
from ga.logbook import (
    DEFAULT_EXPERIMENTS_ROOT,
    PROJECT_ROOT,
    Logbook,
    _utc_now,
    genome_hash,
)
from solver.gclm import solve_gclm
from win_condition import (
    BlowupEstimate,
    InsufficientDataError,
    WinTier,
    classify,
    estimate_blowup_time,
    resolution_converged,
)

DEFAULT_RESOLUTIONS = (256, 512, 1024)
DEFAULT_STUDY_AMPLIFICATION = 1e4  # 4 decades of growth; > the 100x fitness stop
DEFAULT_VISCOUS_FRAC = 0.5         # viscous study point = frac * nu_crit
DEFAULT_DRIFT_THRESHOLD = 1e-3     # conservation-drift artifact guard
DEFAULT_TOP_K = 3
DEFAULT_REL_TOL = 0.02             # win_condition.resolution_converged default


# --- reading elites out of the acceptance archives -------------------------

def latest_checkpoint(experiment_dir):
    """Path to the highest-generation checkpoint in an experiment dir."""
    ckpts = sorted((Path(experiment_dir) / "checkpoints").glob("gen_*.json"))
    if not ckpts:
        raise FileNotFoundError(f"no checkpoints under {experiment_dir}")
    return ckpts[-1]


def load_elites(experiment_dir, top_k=DEFAULT_TOP_K):
    """Top-`top_k` MAP-Elites archive entries (by fitness = nu_crit) from an
    acceptance run, each carried with the frozen config it was evolved under.

    Only genuinely-bracketed elites live in the archive (censored/non-monotone
    evaluations are excluded by rule at insertion time), so every entry here
    is a real critical-value measurement, not a range edge.
    """
    exp_dir = Path(experiment_dir)
    config = json.loads((exp_dir / "config.json").read_text())
    ckpt = json.loads(latest_checkpoint(exp_dir).read_text())
    archive = ckpt["archive"] or {}
    ranked = sorted(archive.items(), key=lambda kv: kv[1]["fitness"], reverse=True)
    elites = []
    for map_cell, entry in ranked[:top_k]:
        elites.append({
            "genome_id": entry["genome_id"],
            "coeffs": list(entry["coeffs"]),
            "envelope_p": float(entry["envelope_p"]),
            "nu_crit": float(entry["fitness"]),
            "descriptors": entry.get("descriptors"),
            "map_cell": map_cell,
            "source_experiment_id": ckpt["experiment_id"],
            "source_generation": ckpt["generation_index"],
            "config": config,
        })
    return elites


def study_points(nu_crit, viscous_frac=DEFAULT_VISCOUS_FRAC):
    """The (role, nu) operating points a single elite is studied at: an
    inviscid anchor and a viscosity-resistance point inside the blow-up band."""
    points = [("inviscid_anchor", 0.0)]
    nu_visc = round(viscous_frac * nu_crit, 6)
    if nu_visc > 0.0:
        points.append(("viscous_resistance", nu_visc))
    return points


# --- one solver run at one resolution --------------------------------------

def run_at_resolution(coeffs, envelope_p, N, config, nu,
                      study_amplification_factor=DEFAULT_STUDY_AMPLIFICATION):
    """Rerun a genome at resolution N and viscosity nu under the frozen fitness
    config (a, t_max, dt policy, tail_fraction, energy budget), with the study
    amplification threshold. Returns a summary dict; `t_star` is None when the
    run produced no forward-pointing blow-up fit (including the amplification-
    stopped-but-too-short-to-fit case, which is a blow-up without a usable T*).
    """
    genome = Genome(coeffs=np.asarray(coeffs, dtype=float),
                    envelope_p=float(envelope_p))
    stop = config["stop_criteria"]
    dt_policy = config["solver_params"]["dt_policy"]
    tail_fraction = config["bisection"]["tail_fraction"]
    omega0 = realize(genome, N, config["energy_budget"], config.get("bandwidth_cap"))
    # Headroom for the extra decades of growth: near the singularity dt ~ 1/max|w|,
    # so more amplification means more steps than the fitness run needed.
    max_steps = max(int(stop["max_steps"]),
                    int(stop["max_steps"] * (study_amplification_factor
                                             / stop["omega_amplification_factor"])))
    result = solve_gclm(
        omega0, a=float(config["gclm_a"]), nu=float(nu),
        t_max=stop["t_max"], max_steps=max_steps,
        amplification_factor=float(study_amplification_factor),
        early_decay_exit=stop["early_decay_exit"],
        dt_max=dt_policy["dt_max"], c1=dt_policy["c1"], c2=dt_policy["c2"],
    )
    blew_up = result.outcome in ("blowup_candidate", "diverged")
    summary = {
        "resolution_N": int(N),
        "nu": float(nu),
        "outcome": result.outcome,
        "blew_up": bool(blew_up),
        "t_final": float(result.t_final),
        "max_omega_final": float(result.max_omega[-1]),
        "n_timesteps": int(result.n_timesteps),
        "dt_min": float(result.dt_min),
        "conservation_drift": float(result.conservation_drift),
        "wall_clock_seconds": float(result.wall_clock_seconds),
        "t_star": None,
        "r_squared": None,
        "exponent": None,
    }
    try:
        est = estimate_blowup_time(
            result.times.tolist(), result.max_omega.tolist(),
            tail_fraction=tail_fraction, fit_exponent=True,
        )
    except InsufficientDataError:
        est = None  # blow-up too fast to fit; no usable T* for convergence
    if est is not None:
        summary.update(t_star=float(est.t_star),
                       r_squared=float(est.r_squared),
                       exponent=float(est.exponent))
    return summary


# --- assembling a per-(genome, nu) resolution study ------------------------

def assess_convergence(runs, rel_tol=DEFAULT_REL_TOL,
                       tier1_r2_threshold=0.98,
                       drift_threshold=DEFAULT_DRIFT_THRESHOLD):
    """Turn a list of per-resolution run summaries (coarse -> fine) into the
    resolution_study verdict fields.

    `converged` requires every resolution to have blown up AND produced a
    forward T*, and those T* to pass `win_condition.resolution_converged`.
    The win tier comes from `win_condition.classify` on the finest run's fit
    plus the T* sequence, so it is exactly the WIN_CONDITION.md contract — but
    a drift-flagged sequence is refused promotion regardless of a clean fit.
    """
    t_stars = [r["t_star"] for r in runs]
    all_blew_up = all(r["blew_up"] for r in runs)
    all_have_t_star = all(t is not None for t in t_stars)
    reproduced = all_blew_up  # blow-up reproduced at every resolution

    blowup_drifts = [r["conservation_drift"] for r in runs if r["blew_up"]]
    max_drift = max(blowup_drifts) if blowup_drifts else None
    drift_exceeded = max_drift is not None and max_drift > drift_threshold

    converged = False
    if all_blew_up and all_have_t_star and len(t_stars) >= 3:
        converged = resolution_converged(t_stars, rel_tol=rel_tol)

    finest = runs[-1]
    finest_est = None
    if finest["t_star"] is not None:
        finest_est = BlowupEstimate(
            t_star=finest["t_star"], r_squared=finest["r_squared"],
            slope=float("nan"), last_time=finest["t_final"],
            n_points=finest["n_timesteps"], exponent=finest["exponent"],
        )
    # classify() promotes to NUMERICALLY_CONFIRMED only when the T* sequence
    # converges; pass it only when we trust the sequence (blew up everywhere,
    # drift within bounds), so a drifted run can never be promoted.
    trust_sequence = all_blew_up and all_have_t_star and not drift_exceeded
    tier = classify(
        finest_est,
        t_star_by_resolution=(t_stars if trust_sequence else None),
        r_squared_threshold=tier1_r2_threshold,
        rel_tol=rel_tol,
    )
    return {
        "t_star_by_resolution": t_stars,
        "converged": bool(converged),
        "reproduced": bool(reproduced),
        "drift_exceeded": bool(drift_exceeded),
        "max_blowup_drift": max_drift,
        "win_tier": tier.value,
    }


# --- the driver ------------------------------------------------------------

def _run_task(task):
    """Pool worker: one (elite, N, nu) solver run. Returns the run summary
    tagged with the keys needed to regroup it in the parent."""
    summary = run_at_resolution(
        task["coeffs"], task["envelope_p"], task["N"], task["config"],
        task["nu"], task["study_amplification_factor"],
    )
    summary["_group"] = task["_group"]
    return summary


def resolution_study(
    source_experiment_dirs,
    experiments_root=DEFAULT_EXPERIMENTS_ROOT,
    repo_root=PROJECT_ROOT,
    resolutions=DEFAULT_RESOLUTIONS,
    top_k=DEFAULT_TOP_K,
    study_amplification_factor=DEFAULT_STUDY_AMPLIFICATION,
    viscous_frac=DEFAULT_VISCOUS_FRAC,
    drift_threshold=DEFAULT_DRIFT_THRESHOLD,
    rel_tol=DEFAULT_REL_TOL,
    n_workers=10,
    experiment_id=None,
    allow_dirty=False,
    run_fn=_run_task,
):
    """Run the Stage 3 resolution study over the elites of one or more
    acceptance runs. Logs a `resolution_study` event per (genome, nu) and
    mirrors numerically_confirmed hits into promoted_candidates.jsonl.

    Returns the list of logged event payloads.
    """
    experiments_root = Path(experiments_root)
    elites = []
    for d in source_experiment_dirs:
        elites.extend(load_elites(d, top_k=top_k))

    # Flatten to (elite, nu, N) solver tasks; group id ties runs back together.
    tasks = []
    groups = {}  # group_key -> {elite, role, nu, runs: {N: summary}}
    for idx, elite in enumerate(elites):
        for role, nu in study_points(elite["nu_crit"], viscous_frac):
            gkey = f"{idx}:{role}"
            groups[gkey] = {"elite": elite, "role": role, "nu": nu, "runs": {}}
            for N in resolutions:
                tasks.append({
                    "_group": gkey, "N": N, "nu": nu,
                    "coeffs": elite["coeffs"], "envelope_p": elite["envelope_p"],
                    "config": elite["config"],
                    "study_amplification_factor": study_amplification_factor,
                })

    if n_workers > 1 and len(tasks) > 1:
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(n_workers) as pool:
            results = pool.map(run_fn, tasks)
    else:
        results = [run_fn(t) for t in tasks]
    for summary in results:
        gkey = summary.pop("_group")
        groups[gkey]["runs"][summary["resolution_N"]] = summary

    # One Stage-3 experiment directory holds all the resolution_study events.
    config = {
        "stage": 3,
        "study_type": "resolution_study",
        "source_experiments": [str(d) for d in source_experiment_dirs],
        "resolutions": list(resolutions),
        "top_k_per_source": top_k,
        "study_amplification_factor": study_amplification_factor,
        "viscous_frac": viscous_frac,
        "drift_threshold": drift_threshold,
        "rel_tol": rel_tol,
        "gclm_a": elites[0]["config"]["gclm_a"] if elites else None,
        "fitness_axis": "nu_crit",
        "n_workers": n_workers,
    }
    logbook = Logbook(experiments_root, repo_root)
    eid = logbook.start_experiment(
        config, allow_dirty=allow_dirty,
        experiment_id=experiment_id
        or ("stage3-resolution-" + _utc_now()[:19].replace(":", "").replace("-", "")),
    )

    events = []
    n_promotions = 0
    try:
        for gkey, group in groups.items():
            elite = group["elite"]
            runs = [group["runs"][N] for N in resolutions]
            tier1_r2 = elite["config"].get("tier1_r2_threshold", 0.98)
            verdict = assess_convergence(
                runs, rel_tol=rel_tol, tier1_r2_threshold=tier1_r2,
                drift_threshold=drift_threshold,
            )
            payload = {
                "generation_index": elite["source_generation"],
                "genome_id": elite["genome_id"],
                "source_experiment_id": elite["source_experiment_id"],
                "map_cell": elite["map_cell"],
                "genome_hash": genome_hash(np.asarray(elite["coeffs"]),
                                           elite["envelope_p"]),
                "role": group["role"],
                "a": float(elite["config"]["gclm_a"]),
                "nu": float(group["nu"]),
                "nu_crit": elite["nu_crit"],
                "study_amplification_factor": study_amplification_factor,
                "resolutions_tested": list(resolutions),
                "t_star_by_resolution": verdict["t_star_by_resolution"],
                "converged": verdict["converged"],
                "reproduced": verdict["reproduced"],
                "drift_exceeded": verdict["drift_exceeded"],
                "max_blowup_drift": verdict["max_blowup_drift"],
                "win_tier": verdict["win_tier"],
                "genome_coeffs": list(elite["coeffs"]),
                "genome_envelope_p": elite["envelope_p"],
                "shape_descriptors": elite["descriptors"],
                "runs": runs,
            }
            logbook.append_event("resolution_study", payload)
            events.append(payload)
            if payload["win_tier"] == WinTier.NUMERICALLY_CONFIRMED.value:
                n_promotions += 1
                _mirror_promotion(experiments_root, eid, payload)
    finally:
        logbook.finish_experiment(
            status="completed", n_tier2_promotions=n_promotions,
        )
    return events


def _mirror_promotion(experiments_root, experiment_id, payload):
    """Append a Tier 2 hit to the cross-experiment promoted_candidates.jsonl
    (LOGGING.md schema #6) so it is never buried in one run's log."""
    path = Path(experiments_root) / "promoted_candidates.jsonl"
    row = {
        "experiment_id": experiment_id,
        "source_experiment_id": payload["source_experiment_id"],
        "genome_id": payload["genome_id"],
        "genome_hash": payload["genome_hash"],
        "role": payload["role"],
        "a": payload["a"],
        "nu": payload["nu"],
        "nu_crit": payload["nu_crit"],
        "resolutions_tested": payload["resolutions_tested"],
        "t_star_by_resolution": payload["t_star_by_resolution"],
        "max_blowup_drift": payload["max_blowup_drift"],
        "win_tier": payload["win_tier"],
        "timestamp": _utc_now(),
        "genome_coeffs": payload["genome_coeffs"],
        "genome_envelope_p": payload["genome_envelope_p"],
    }
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Stage 3 resolution study")
    parser.add_argument(
        "source_dirs", nargs="+",
        help="acceptance-run experiment directories (with checkpoints/)")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--resolutions", type=int, nargs="+",
                        default=list(DEFAULT_RESOLUTIONS))
    parser.add_argument("--amplification", type=float,
                        default=DEFAULT_STUDY_AMPLIFICATION)
    parser.add_argument("--viscous-frac", type=float, default=DEFAULT_VISCOUS_FRAC)
    parser.add_argument("--drift-threshold", type=float,
                        default=DEFAULT_DRIFT_THRESHOLD)
    parser.add_argument("--n-workers", type=int, default=10)
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args(argv)

    events = resolution_study(
        args.source_dirs, resolutions=tuple(args.resolutions), top_k=args.top_k,
        study_amplification_factor=args.amplification,
        viscous_frac=args.viscous_frac, drift_threshold=args.drift_threshold,
        n_workers=args.n_workers, allow_dirty=args.allow_dirty,
    )
    n_conf = sum(1 for e in events
                 if e["win_tier"] == WinTier.NUMERICALLY_CONFIRMED.value)
    print(f"\n{len(events)} resolution_study events, {n_conf} NUMERICALLY_CONFIRMED")
    for e in events:
        ts = ", ".join(f"{t:.5f}" if t is not None else "None"
                       for t in e["t_star_by_resolution"])
        print(f"  {e['genome_id']} [{e['role']:19s} nu={e['nu']:.4f}] "
              f"T*=({ts}) conv={e['converged']!s:5s} "
              f"drift={e['max_blowup_drift']:.1e} -> {e['win_tier']}")


if __name__ == "__main__":
    main()
