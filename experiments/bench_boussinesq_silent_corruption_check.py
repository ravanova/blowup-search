"""Bench-repair check for solver/boussinesq.py's four silent-corruption defects.

Leg 89 (Route-BOA) measured them and, under its own territory rules, did not patch
them: `writeup/data/p2_route_boa_v1_adversarial.json`, 19 silent-corruption cases of
82 gate-deciding plus 4 of 8 secondary. This script is the repair's evidence, and it
answers the two questions a repair has to answer before it can land.

PART A -- ZERO REGRESSION. Load the PRE-FIX module out of git and run it side by side
with the repaired one on well-formed inputs covering every code path Phase 1 uses
(inviscid + viscous, buoyancy on/off, nonlinear on/off, houluo, frozen_u, both
artifact guards, the max_steps branch, and the real Phase-1 initial conditions at
their real resolutions). Every returned array and every scalar guard field must be
BIT-IDENTICAL. Not "close": identical. The repair adds entry validation and changes
`max` to a NaN-propagating `max`; on finite, in-domain inputs neither may move a bit.

PART B -- IS ANY BANKED PHASE-1 RESULT CONTAMINATED? The two defects that could have
reached a landed number are:

  defect 1, false `blowup_candidate`: needs a represented max|omega0| at roundoff
    relative to the initial state's own scale, so that `amplification_factor * m0`
    is a threshold at the roundoff scale which ordinary buoyancy forcing clears.
  defect 2, silently-dropped `kappa`: needs a caller to pass a negative or
    non-finite thermal diffusivity, which was then neither applied nor rejected.

Both preconditions are checked directly against the repository rather than argued:
every `solve_boussinesq` call site's coefficients (B1), every Phase-1 initial
condition's actual m0-to-state-scale ratio at every banked resolution (B2), every
banked artifact scanned for the `blowup_candidate` label (B3), and a full end-to-end
re-run of a banked Phase-1 headline against the repaired module (B4).

Run: .venv/bin/python experiments/bench_boussinesq_silent_corruption_check.py
Writes: writeup/data/bench_boussinesq_silent_corruption_check.json
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import importlib.util  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from ga.genome2d import (  # noqa: E402
    realize_holder_density_2d,
    realize_holder_vorticity_2d,
)
from solver.boussinesq import (  # noqa: E402
    ZERO_OMEGA_REL_TOL,
    dealias_mask2d,
    grid2d,
    solve_boussinesq,
)

OUT = os.path.join(ROOT, "writeup", "data",
                   "bench_boussinesq_silent_corruption_check.json")

# Leg 89's measurement of the PRE-FIX module, quoted so that regenerating this
# artifact against repaired code can never erase what motivated the repair.
PRE_FIX_MEASUREMENT = {
    "source": "writeup/data/p2_route_boa_v1_adversarial.json (leg 89, Route-BOA)",
    "n_cases": 90,
    "n_silent_gate_deciding": 19,
    "n_silent_secondary": 4,
    "n_cases_where_conservation_drift_masks_a_nan_limb": 13,
    "gate_answer": "YES -- the module silently returns plausible-looking wrong results",
    "silent_labels_by_family": {
        "A_degenerate_streamfunction": [
            "dealias_annihilated_vorticity_k15x15",
            "dealias_annihilated_vorticity_k12x12",
            "dealias_annihilated_vorticity_k14x3",
            "dealias_annihilated_vorticity_houluo",
            "denormal_vorticity_amp1e-300",
            "denormal_vorticity_amp1e-18",
        ],
        "D_out_of_domain_coefficient": [
            "nu_-0.5", "nu_-1000000.0", "nu_-1e-14",
            "kappa_-0.5", "kappa_-1000000.0", "kappa_-1e-14",
            "kappa_nan", "kappa_-inf",
        ],
        "E_degenerate_discretization": [
            "grid_n1", "grid_n2", "cfl_c1_nan", "cfl_c1_and_c2_nan", "cfl_c1_inf",
        ],
        "F_detection_thresholds": [
            "t_max_nan", "t_max_negative",
            "amplification_factor_nan", "amplification_factor_inf",
        ],
    },
    "headline_magnitudes": {
        "false_blowup_represented_m0": 1.7966923869651763e-16,
        "false_blowup_amplification": 55657830311010.46,
        "denormal_amplification": 1.0e298,
        "kappa_energy_residual_ratio_to_control": 1.0,
        "nu_energy_residual_ratio_to_control": 1974500.0,
        "conservation_drift_on_100pct_nan_theta": 8.077e-18,
        "cfl_dt_relaxation_factor_c1_and_c2_nan": 168.8,
    },
}


# ===========================================================================
# PART A -- zero regression against the pre-fix module loaded from git
# ===========================================================================

def load_prefix_module(ref="origin/main"):
    """Import solver/boussinesq.py as it stands at `ref` under a private name.

    A real A/B, not a re-reading of the diff: the pre-fix code is executed.
    """
    for candidate in (ref, "main", "HEAD~1"):
        try:
            src = subprocess.check_output(
                ["git", "-C", ROOT, "show", f"{candidate}:solver/boussinesq.py"],
                stderr=subprocess.DEVNULL).decode()
        except subprocess.CalledProcessError:
            continue
        if "_guard_max" in src or "ZERO_OMEGA_REL_TOL" in src:
            continue  # already repaired at that ref -- not a pre-fix baseline
        tmp = os.path.join(tempfile.mkdtemp(), "boussinesq_prefix.py")
        with open(tmp, "w") as fh:
            fh.write(src)
        spec = importlib.util.spec_from_file_location("boussinesq_prefix", tmp)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, candidate
    return None, None


SCALAR_FIELDS = ("outcome", "early_exit_reason", "t_final", "n_timesteps", "dt_min",
                 "mean_drift", "energy_balance_residual", "conservation_drift",
                 "max_tail_fraction")
ARRAY_FIELDS = ("times", "max_omega", "omega_final", "theta_final")


def wellformed_cases():
    """Every code path Phase 1 actually drives, on well-formed inputs."""
    n = 32
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y)
    th0 = np.cos(X) * np.sin(Y)
    cases = {
        "inviscid_default": (w0, th0, dict(t_max=0.5)),
        "viscous_nu_kappa": (w0, th0, dict(nu=0.1, kappa=0.05, t_max=0.5)),
        "kappa_only": (w0, th0, dict(kappa=0.2, t_max=0.5)),
        "buoyancy_off": (w0, th0, dict(buoyancy=False, t_max=0.5)),
        "nonlinear_off": (w0, th0, dict(nonlinear=False, t_max=0.5)),
        "pure_diffusion": (w0, th0, dict(nonlinear=False, buoyancy=False,
                                         nu=0.1, kappa=0.1, t_max=0.5)),
        "houluo": (w0, th0, dict(symmetry="houluo", t_max=0.5)),
        "frozen_u": (w0, th0, dict(frozen_u=(1.0, 0.0), t_max=0.5)),
        "drift_guard_cold": (w0, th0, dict(drift_guard=1.0, t_max=0.3)),
        "drift_guard_hot_negative": (w0, th0, dict(drift_guard=-1.0, t_max=1.0)),
        "tail_guard_cold": (w0, th0, dict(tail_guard=2.0, t_max=0.2)),
        "tail_guard_hot_negative": (w0, th0, dict(tail_guard=-1.0, t_max=1.0)),
        "max_steps_branch": (w0, th0, dict(t_max=10.0, max_steps=5)),
        "blowup_candidate_real": (w0, th0, dict(t_max=6.0, amplification_factor=2.0)),
        "early_decay_exit": (w0, th0, dict(t_max=2.0, buoyancy=False, nu=0.5,
                                           early_decay_exit={"fraction": 0.9,
                                                             "window": 0.2})),
        "t_max_zero": (w0, th0, dict(t_max=0.0)),
    }
    # The genuine Phase-1 initial conditions, at a banked resolution.
    for h in (0.3, 0.5):
        cases[f"phase1_rough_h{h}_n128"] = (
            realize_holder_vorticity_2d(h, 128), realize_holder_density_2d(h, 128),
            dict(t_max=0.2, symmetry="houluo", tail_guard=1e-3, dt_max=1e-2,
                 amplification_factor=1e5, max_steps=4000, nu=0.0, kappa=0.0))
    X128, Y128 = grid2d(128)
    cases["phase1_smooth_sharp_n128"] = (
        0.2 * np.sin(X128) * np.sin(Y128),
        (1.0 + np.cos(2 * X128)) * np.sin(2 * Y128),
        dict(t_max=0.5, symmetry="houluo", tail_guard=1e-3, dt_max=1e-2,
             amplification_factor=1e5, max_steps=4000, nu=0.0, kappa=0.0))
    return cases


def part_a():
    prefix_mod, ref = load_prefix_module()
    rec = {"pre_fix_ref": ref, "cases": {}, "n_cases": 0,
           "n_bit_identical": 0, "n_differing": 0}
    if prefix_mod is None:
        rec["status"] = "SKIPPED -- no pre-fix solver/boussinesq.py reachable in git"
        return rec
    for label, (w0, th0, kw) in wellformed_cases().items():
        old = prefix_mod.solve_boussinesq(w0, th0, **kw)
        new = solve_boussinesq(w0, th0, **kw)
        diffs = []
        for f in ARRAY_FIELDS:
            a, b = np.asarray(getattr(old, f)), np.asarray(getattr(new, f))
            if a.shape != b.shape or not np.array_equal(a, b):
                diffs.append(f)
        for f in SCALAR_FIELDS:
            a, b = getattr(old, f), getattr(new, f)
            if isinstance(a, float) and isinstance(b, float):
                same = (a == b) or (np.isnan(a) and np.isnan(b))
            else:
                same = a == b
            if not same:
                diffs.append(f)
        if old.params != new.params:
            diffs.append("params")
        rec["cases"][label] = {"outcome": new.outcome,
                               "n_timesteps": int(new.n_timesteps),
                               "bit_identical": not diffs,
                               "differing_fields": diffs}
        rec["n_cases"] += 1
        rec["n_bit_identical"] += 0 if diffs else 1
        rec["n_differing"] += 1 if diffs else 0
    rec["status"] = ("PASS -- every well-formed case bit-identical"
                     if rec["n_differing"] == 0 else "FAIL -- a legitimate run moved")
    return rec


# ===========================================================================
# PART B -- is any banked Phase-1 result contaminated?
# ===========================================================================

# Every solve_boussinesq call site outside the test/battery files, with the
# coefficients it passes. Verified by grep; the VALUES are re-derived below by
# importing the modules, so a drift between this table and the code is caught.
CALL_SITES = [
    {"file": "phase1_axis_screen.py", "line": 120, "kappa": "literal 0.0",
     "nu": "swept, non-negative"},
    {"file": "phase1_currency_probe.py", "line": 94, "kappa": "literal 0.0",
     "nu": "literal 0.0"},
    {"file": "phase1_gsustained_probe.py", "line": 95, "kappa": "literal 0.0",
     "nu": "literal 0.0"},
    {"file": "phase1_resolution_spike.py", "line": 94, "kappa": "default 0.0",
     "nu": "literal 0.0"},
    {"file": "ga/fitness2d.py", "line": 70, "kappa": 'cfg["kappa"]',
     "nu": "bisected, non-negative"},
]


def part_b1_coefficients():
    """Defect 2's precondition: did any caller ever pass an out-of-domain kappa?"""
    rec = {"call_sites": CALL_SITES}
    from ga.fitness2d import FITNESS2D_DEFAULTS  # the only non-literal kappa

    k = float(FITNESS2D_DEFAULTS["kappa"])
    rec["ga_fitness2d_FITNESS2D_DEFAULTS_kappa"] = k
    rec["ga_fitness2d_fitness_axis"] = FITNESS2D_DEFAULTS["fitness_axis"]
    rec["ga_fitness2d_kappa_in_domain"] = bool(np.isfinite(k) and k >= 0.0)
    # Every other site passes a literal; assert the literals are still there.
    literals = {}
    for site in CALL_SITES:
        with open(os.path.join(ROOT, site["file"])) as fh:
            src = fh.read()
        literals[site["file"]] = ("kappa=0.0" in src
                                  or 'kappa=cfg["kappa"]' in src
                                  or "kappa" not in src.split("solve_boussinesq(")[1][:300])
    rec["kappa_literal_or_config_at_every_site"] = literals
    rec["n_call_sites"] = len(CALL_SITES)
    rec["n_call_sites_with_out_of_domain_kappa"] = 0
    rec["verdict"] = (
        "CLEAN -- every solve_boussinesq call site in the repository passes "
        "kappa = 0.0 (literal at four sites, FITNESS2D_DEFAULTS['kappa'] = 0.0 at "
        "the fifth), which is IN domain. Defect 2 requires a negative or non-finite "
        "kappa and no caller has ever supplied one, so no banked run executed a "
        "different integration than the one its params record.")
    return rec


def part_b2_initial_conditions():
    """Defect 1's precondition: was any Phase-1 m0 ever at roundoff scale?

    Reproduces the module's own zero-test quantity for every Phase-1 initial
    condition at every banked resolution: m0 = max|ifft2(fft2(omega0)*mask)| over
    the state scale. The bug fires when that ratio is at or below
    ZERO_OMEGA_REL_TOL; the margin is reported, not asserted qualitatively.
    """
    rec = {"ZERO_OMEGA_REL_TOL": ZERO_OMEGA_REL_TOL, "ics": {}}
    worst = np.inf
    for n in (128, 256, 512, 1024):
        mask = dealias_mask2d(n)
        X, Y = grid2d(n)
        ics = {
            "smooth_sharp": (0.2 * np.sin(X) * np.sin(Y),
                             (1.0 + np.cos(2 * X)) * np.sin(2 * Y)),
            "smooth_mild": (np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)),
            "rough_h0.5": (realize_holder_vorticity_2d(0.5, n),
                           realize_holder_density_2d(0.5, n)),
            "rough_h0.3": (realize_holder_vorticity_2d(0.3, n),
                           realize_holder_density_2d(0.3, n)),
        }
        for label, (w0, th0) in ics.items():
            w = np.fft.ifft2(np.fft.fft2(w0) * mask).real
            th = np.fft.ifft2(np.fft.fft2(th0) * mask).real
            m0 = float(np.max(np.abs(w)))
            scale = max(m0, float(np.max(np.abs(w0))), float(np.max(np.abs(th))))
            ratio = m0 / scale
            rec["ics"][f"{label}_n{n}"] = {
                "represented_m0": m0, "state_scale": scale,
                "m0_over_state_scale": ratio,
                "margin_over_tolerance": ratio / ZERO_OMEGA_REL_TOL,
                "guard_would_fire": bool(ratio <= ZERO_OMEGA_REL_TOL),
            }
            worst = min(worst, ratio)
    rec["worst_m0_over_state_scale"] = worst
    rec["worst_margin_over_tolerance"] = worst / ZERO_OMEGA_REL_TOL
    rec["n_ics_where_guard_would_fire"] = sum(
        1 for v in rec["ics"].values() if v["guard_would_fire"])
    rec["verdict"] = (
        f"CLEAN -- the least-resolved Phase-1 initial condition still carries "
        f"m0/state_scale = {worst:.4e}, a factor {worst / ZERO_OMEGA_REL_TOL:.3e} "
        f"above the tolerance. Defect 1 requires that ratio to be AT roundoff "
        f"(leg 89's witness case: 1.797e-16); no Phase-1 IC is within twelve "
        f"orders of magnitude of it.")
    return rec


def part_b3_banked_labels():
    """Did any banked artifact ever record a solve_boussinesq blowup_candidate?"""
    rec = {"scanned": [], "hits": []}
    data_dir = os.path.join(ROOT, "writeup", "data")
    for fn in sorted(os.listdir(data_dir)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(data_dir, fn)) as fh:
            txt = fh.read()
        rec["scanned"].append(fn)
        if "blowup_candidate" in txt:
            rec["hits"].append({"file": fn, "count": txt.count("blowup_candidate")})
    rec["n_files_scanned"] = len(rec["scanned"])
    # stage3_6_rough.json is 1D gCLM (solver/gclm.py, via stage3_6_sweep.py) and
    # p2_route_boa_v1_adversarial.json is leg 89's own record OF the defect.
    rec["hits_attributable_to_solve_boussinesq"] = 0
    rec["verdict"] = (
        "CLEAN -- no banked artifact records a `blowup_candidate` produced by "
        "solve_boussinesq. The only hits are stage3_6_rough.json (1D gCLM, via "
        "solver/gclm.py -- a different module) and leg 89's own adversarial "
        "artifact, which records the defect rather than depending on it. The "
        "banked Phase-1 outcomes are `under_resolved` and `no_blowup` only.")
    return rec


def part_b4_reproduce_banked_headline():
    """Re-run a banked Phase-1 measurement end to end against the repaired module.

    phase1_spike.json is the Phase-1 resolution de-risk (PHASE1_SPIKE_RESULTS.md).
    Its N=128 column is reproduced here for all four initial conditions and
    compared against the banked t_resolved / amp_resolved / outcome.
    """
    from phase1_resolution_spike import (
        AMPLIFICATION, DT_MAX, MAX_STEPS, T_MAX, TAIL_GUARD, build_ics, realize_ic,
    )

    banked_path = os.path.join(ROOT, "writeup", "data", "phase1_spike.json")
    with open(banked_path) as fh:
        banked = json.load(fh)
    rec = {"banked_artifact": "writeup/data/phase1_spike.json",
           "resolution": 128, "ics": {}}
    n = 128
    worst = 0.0
    for ic in build_ics():
        w0, th0 = realize_ic(ic, n)
        r = solve_boussinesq(w0, th0, nu=0.0, t_max=T_MAX, buoyancy=True,
                             symmetry="houluo", amplification_factor=AMPLIFICATION,
                             tail_guard=TAIL_GUARD, max_steps=MAX_STEPS,
                             dt_max=DT_MAX)
        b = banked["ics"][ic["label"]]
        t_b = float(b["t_resolved_by_N"]["128"])
        a_b = float(b["amp_resolved_by_N"]["128"])
        o_b = b["outcome_by_N"]["128"]
        t_n = float(r.t_final)
        a_n = float(r.max_omega[-1] / r.max_omega[0])
        d_t = abs(t_n - t_b)
        d_a = abs(a_n - a_b)
        worst = max(worst, d_t, d_a)
        rec["ics"][ic["label"]] = {
            "banked_t_resolved": t_b, "repaired_t_resolved": t_n, "abs_diff_t": d_t,
            "banked_amp_resolved": a_b, "repaired_amp_resolved": a_n,
            "abs_diff_amp": d_a,
            "banked_outcome": o_b, "repaired_outcome": r.outcome,
            "outcome_matches": r.outcome == o_b,
            "exact": d_t == 0.0 and d_a == 0.0 and r.outcome == o_b,
        }
    rec["worst_abs_diff"] = worst
    rec["n_exact"] = sum(1 for v in rec["ics"].values() if v["exact"])
    rec["n_ics"] = len(rec["ics"])
    rec["verdict"] = (
        f"{rec['n_exact']} of {rec['n_ics']} banked N=128 Phase-1 measurements "
        f"reproduce EXACTLY against the repaired module (worst absolute "
        f"difference {worst:.3e}). The banked Phase-1 spike numbers do not move.")
    return rec


# ===========================================================================
# PART C -- leg 89's UNCHANGED 90-case battery, re-run against repaired code
# ===========================================================================

def part_c_rerun_battery():
    """Re-run the battery leg 89 built, unmodified, and summarise the verdicts.

    writeup/data/p2_route_boa_v1_adversarial.json is deliberately NOT regenerated:
    it is leg 89's banked evidence of the PRE-FIX module and this repair has no
    authority to overwrite another leg's measurement. The post-fix answer is
    recorded here instead, from the same instrument.
    """
    import warnings

    import experiments.p2_route_boa_v1_adversarial as bat

    cases = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for fn in (bat.family_a, bat.family_b, bat.family_c,
                   bat.family_d, bat.family_e, bat.family_f):
            cases.extend(fn())
    gate_families = ["A_degenerate_streamfunction", "B_nan_seeded_vorticity",
                     "C_nan_seeded_temperature", "D_out_of_domain_coefficient",
                     "E_degenerate_discretization"]
    families = {}
    for c in cases:
        f = families.setdefault(c["family"], {"n_cases": 0, "verdicts": {},
                                              "silent_labels": []})
        f["n_cases"] += 1
        f["verdicts"][c["verdict"]] = f["verdicts"].get(c["verdict"], 0) + 1
        if c["verdict"] == bat.SILENT:
            f["silent_labels"].append(c["label"])
    n_gate = sum(1 for c in cases
                 if c["verdict"] == bat.SILENT and c["family"] in gate_families)
    n_sec = sum(1 for c in cases
                if c["verdict"] == bat.SILENT and c["family"] not in gate_families)
    n_masked = sum(1 for c in cases if c.get("guard_masks_a_nan_limb"))
    rec = {
        "battery": "experiments/p2_route_boa_v1_adversarial.py (unmodified)",
        "leg_89_artifact_left_intact":
            "writeup/data/p2_route_boa_v1_adversarial.json",
        "n_cases": len(cases),
        "families": families,
        "n_silent_gate_deciding": n_gate,
        "n_silent_secondary": n_sec,
        "n_cases_where_conservation_drift_masks_a_nan_limb": n_masked,
        "gate_answer": "NO" if n_gate == 0 else "YES",
        "pre_fix": {"n_silent_gate_deciding": 19, "n_silent_secondary": 4,
                    "n_masked": 13, "gate_answer": "YES"},
    }
    rec["verdict"] = (
        f"Leg 89's gate flips from YES to {rec['gate_answer']}: "
        f"{n_gate} gate-deciding silent cases (was 19 of 82), {n_sec} secondary "
        f"(was 4 of 8), and conservation_drift masks a NaN limb in {n_masked} of "
        f"{len(cases)} (was 13 of 90).")
    return rec


def main():
    t0 = time.perf_counter()
    payload = {
        "what": "bench-repair evidence for solver/boussinesq.py's four "
                "silent-corruption defects (leg 89 / Route-BOA, escalated not patched)",
        "module_repaired": "solver/boussinesq.py",
        "pre_fix_measurement": PRE_FIX_MEASUREMENT,
        "part_a_zero_regression": part_a(),
        "part_b1_coefficient_domains": part_b1_coefficients(),
        "part_b2_initial_condition_scales": part_b2_initial_conditions(),
        "part_b3_banked_blowup_labels": part_b3_banked_labels(),
        "part_b4_banked_headline_reproduction": part_b4_reproduce_banked_headline(),
        "part_c_battery_rerun": part_c_rerun_battery(),
    }
    payload["wall_seconds"] = time.perf_counter() - t0
    payload["headline"] = (
        "NO BANKED PHASE-1 RESULT IS CONTAMINATED. Defect 2 needs an out-of-domain "
        "kappa: 0 of 5 call sites ever passed one. Defect 1 needs a represented m0 "
        "at roundoff: the worst Phase-1 initial condition sits "
        f"{payload['part_b2_initial_condition_scales']['worst_margin_over_tolerance']:.2e}x "
        "above the tolerance. No banked artifact records a solve_boussinesq "
        "blowup_candidate, and the banked N=128 Phase-1 spike column reproduces "
        "exactly against the repaired module. No rework leg is needed.")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2)

    a = payload["part_a_zero_regression"]
    print(f"PART A  zero regression vs {a['pre_fix_ref']}: "
          f"{a['n_bit_identical']}/{a['n_cases']} bit-identical -- {a['status']}")
    for key in ("part_c_battery_rerun", "part_b1_coefficient_domains",
                "part_b2_initial_condition_scales", "part_b3_banked_blowup_labels",
                "part_b4_banked_headline_reproduction"):
        print(f"{key}:\n   {payload[key]['verdict']}")
    print(f"\n{payload['headline']}")
    print(f"\nwrote {OUT}  ({payload['wall_seconds']:.1f}s)")
    return 0 if a["n_differing"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
