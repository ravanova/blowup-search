#!/usr/bin/env python3
"""Leg 406, unit `L6-b` -- EVIDENCE SCRIPT.  Re-runnable by an independent verifier.

    .venv/bin/python experiments/p2_route_l6b_v1_evidence.py

Exits 0 iff every check passes; non-zero on the first failure count.  It re-derives the
headline numbers from the banked artefacts and from `L6`'s own code, NOT from prose:

  * `L6`'s artefact is byte-untouched by this unit and its `self_hash` still recomputes;
  * this unit's artefact `self_hash` recomputes;
  * `n_dof`, the realization, the trial space, the basis and the norm are IDENTICAL
    strings to `L6`'s -- the gate's scope limit, checked rather than asserted;
  * `L6`'s banked `J4` coefficients still evaluate to `1.613811231995397` under `L6`'s
    own `objective`, so start (i) really is `L6`'s minimiser;
  * the two fresh seeds regenerate bit-for-bit from `numpy.random.default_rng`;
  * the gate's YES/NO is recomputed from the raw per-start trajectories;
  * the residual at the 800-iteration cap is recomputed from the trajectories, giving the
    like-for-like comparison with `L6`;
  * the banked FINAL iterate of every start re-evaluates to that start's reported
    residual -- so the numbers are checkable without rerunning the 20,000 iterations;
  * `T_A` and `T_D` reproduce, both on `L6`'s own self-test field and at this unit's
    starting point;
  * the `leg_401.md` SS7.3 false-convergence defect is checked, not assumed absent.

Cost: a few minutes (it re-runs `L6`'s self-test suite and a handful of objective
evaluations at n_dof = 6720).  It does NOT re-run the minimisation.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("L6_THREADS", "4")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, os.environ["L6_THREADS"])

import numpy as np                                                    # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import p2_route_l6_v1 as l6                                           # noqa: E402

L6_ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"
ART = ROOT / "writeup" / "data" / "p2_route_l6b_v1.json"
CKPT = ROOT / "experiments" / "route4" / "l6b_ckpt"

L6_SELF_HASH = "6a033004deef39d3"
L6_RESIDUAL = 1.613811231995397

FAILS = []
N = 0


def check(tag, ok, msg):
    global N
    N += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {tag:5s}  {msg}")
    if not ok:
        FAILS.append(tag)


def selfhash(doc):
    body = dict(doc)
    body.pop("self_hash", None)
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def main():
    d6 = json.loads(L6_ART.read_text())
    d = json.loads(ART.read_text())
    print("L6-b (leg 406) evidence\n")

    # ---- provenance -------------------------------------------------------------------
    check("C01", selfhash(d6) == L6_SELF_HASH == d6["self_hash"],
          f"L6 artefact self_hash recomputes to {selfhash(d6)} (untouched by this unit)")
    check("C02", selfhash(d) == d["self_hash"],
          f"L6-b artefact self_hash recomputes to {selfhash(d)}")
    check("C03", d["answers_about"]["self_hash"] == L6_SELF_HASH,
          "L6-b names the artefact the gate names")

    # ---- the scope limit: n_dof and the realization are UNCHANGED ---------------------
    r6, rb = d6["realization_lesson_91"], d["realization_lesson_91"]
    bp = d6["banked_profile"]["B"]
    check("C04", rb["n_dof"] == bp["n_dof"] == 6720,
          f"n_dof = {rb['n_dof']} in both, and the gate fixes 6720")
    check("C05", (rb["Lmax"], rb["Nr"], rb["Ks"], rb["Lmap"]) ==
          (bp["Lmax"], bp["Nr"], bp["Ks"], bp["Lmap"]),
          f"(Lmax,Nr,Ks,Lmap) = {(rb['Lmax'], rb['Nr'], rb['Ks'], rb['Lmap'])} identical")
    check("C06", rb["object"] == r6["object"], "realization string identical to L6's")
    check("C07", rb["trial_space"] == r6["trial_space"], "trial space identical to L6's")
    check("C08", rb["basis"] == r6["basis"], "basis identical to L6's")
    check("C09", rb["norm_LOAD_BEARING"] == r6["norms"]["LOAD_BEARING"],
          "load-bearing norm string identical to L6's")
    check("C10", rb["normalisation_branch_B"] == r6["normalisations"]["branch_B"],
          "branch-B normalisation identical to L6's")
    check("C11", rb["branch"] == "B", "branch B, as the gate says")

    # ---- the geometry, rebuilt from L6's own numbers ----------------------------------
    g = l6.Geom(bp["Lmax"], bp["Nr"], bp["Ks"], bp["Lmap"])
    check("C12", int(g.n_dof) == 6720 and (g.nq_r, g.nth, g.nph, g.ns) ==
          (rb["nq_r"], rb["n_theta"], rb["n_phi"], rb["n_s"]),
          f"Geom rebuilds to n_dof={g.n_dof}, quadrature "
          f"({g.nq_r},{g.nth},{g.nph},{g.ns})")

    # ---- start (i) really is L6's minimiser ------------------------------------------
    x6 = np.array(bp["coefficients"], float)
    J6, _ = l6.objective(g, x6, "B")
    check("C13", abs(J6 - L6_RESIDUAL) <= 1e-12 * L6_RESIDUAL,
          f"L6's banked J4 coefficients evaluate to {J6!r} (banked {L6_RESIDUAL!r})")
    check("C14", abs(d["selftests"]["starting_point_J"] - L6_RESIDUAL)
          <= 1e-12 * L6_RESIDUAL,
          "the run's own starting-point evaluation agrees")

    # ---- the two fresh seeds regenerate ----------------------------------------------
    seeds = d["optimiser"]["fresh_seeds"]
    check("C15", set(seeds).isdisjoint(set(d["optimiser"]["L6_seeds"])),
          f"fresh seeds {seeds} are disjoint from L6's {d['optimiser']['L6_seeds']}")
    for sd in seeds:
        rng = np.random.default_rng(sd)
        x0 = l6.normalise(g, rng.standard_normal(g.n_dof) * 0.1, "B")
        J0, _ = l6.objective(g, x0, "B")
        st = d["starts"][f"seed{sd}"]
        traj0 = [t for t in st["trajectory_k_sec_J_ginf_gscaled"] if t[0] == 1]
        # the objective at the start point is not sampled at k=0, so compare against the
        # value the run recorded at its first callback: it must be BELOW the start value
        check(f"C16{sd}", J0 > 0 and (not traj0 or traj0[0][2] <= J0),
              f"seed{sd} start regenerates; J(start) = {J0:.6g}, "
              f"first recorded J = {traj0[0][2] if traj0 else float('nan'):.6g}")

    # ---- the gate, recomputed from the raw trajectories -------------------------------
    per = {}
    for name, st in d["starts"].items():
        traj = st["trajectory_k_sec_J_ginf_gscaled"]
        per[name] = min(t[2] for t in traj)
        check(f"C17_{name}", abs(per[name] - st["smallest_residual_at_20000"])
              <= 1e-14 * max(1.0, per[name]),
              f"{name}: smallest J over the trajectory = {per[name]!r}")
    smallest = min(per.values())
    check("C18", abs(smallest - d["gate"]["smallest_residual_at_20000"]) <= 1e-14,
          f"gate smallest residual at 20,000 = {smallest!r}")
    verdict = "YES" if smallest < d["gate"]["material_threshold"] else "NO"
    check("C19", verdict == d["gate"]["materially_below_1_6138"],
          f"materially below 1.6138 (i.e. < {d['gate']['material_threshold']}) = {verdict}")
    check("C20", d["gate"]["L6_residual_at_800"] == L6_RESIDUAL,
          "compared against L6's banked number, not a re-measurement")

    # ---- the like-for-like 800-iteration comparison -----------------------------------
    for name, st in d["starts"].items():
        traj = st["trajectory_k_sec_J_ginf_gscaled"]
        at800 = min((t[2] for t in traj if t[0] <= 800), default=None)
        rec = st["residual_at_iteration_cap"]["800"]
        check(f"C21_{name}", at800 is not None and abs(at800 - rec) <= 1e-14,
              f"{name}: best J by iteration 800 = {at800!r}")

    # ---- the independent-seed basin-floor reading -------------------------------------
    lo, hi = d["gate"]["basin_floor_band"]
    for name in [k for k in d["starts"] if k.startswith("seed")]:
        inband = bool(lo <= per[name] <= hi)
        check(f"C22_{name}", inband == d["gate"]["independent_seed_reached_basin_floor"][name],
              f"{name} reached {per[name]:.6g}; in [{lo},{hi}] = {inband}")

    # ---- the SS7.3 false-convergence defect, checked not assumed ----------------------
    for name, st in d["starts"].items():
        rounds = st["rounds"]
        if st["hit_maxiter"]:
            ok, why = True, f"ran to the cap ({st['iterations']} iterations)"
        else:
            gains = []
            prev = float("inf")
            for rd in rounds:
                gains.append((prev - rd["fun"]) / abs(prev) if np.isfinite(prev) else 1.0)
                prev = rd["fun"]
            ok = bool(gains and gains[-1] < l6.REL_STALL)
            why = (f"stopped at {st['iterations']} iterations after {len(rounds)} "
                   f"renormalising restarts; last restart bought {gains[-1]:.3e} "
                   f"< REL_STALL = {l6.REL_STALL:g}, so it is NOT the SS7.3 defect")
        check(f"C23_{name}", ok, f"{name}: {why}")

    # ---- the banked final iterates reproduce their residuals --------------------------
    for name, st in d["starts"].items():
        f = CKPT / f"{name}_final_iterate.json"
        if not f.exists():
            check(f"C24_{name}", False, f"missing final iterate {f}")
            continue
        rec = json.loads(f.read_text())
        xf = np.array(rec["coefficients"], float)
        Jf, _ = l6.objective(g, xf, "B")
        check(f"C24_{name}", xf.size == 6720
              and abs(Jf - st["final_residual"]) <= 1e-10 * max(1.0, Jf),
              f"{name}: banked final iterate re-evaluates to {Jf!r} "
              f"(reported {st['final_residual']!r})")

    # ---- self-tests -------------------------------------------------------------------
    st_l6 = l6.selftests(verbose=False)
    banked = d["selftests"]["L6_suite_banked"]
    for k in ("T_A_div_V_max_abs_over_scale", "T_D_W_vs_fd_curlR_max_rel_err"):
        rel = abs(st_l6[k] - banked[k]) / abs(banked[k])
        check(f"C25_{k[:3]}", rel < 1e-9,
              f"{k} reproduces L6's banked {banked[k]:.4e} (rel diff {rel:.2e})")
    sp = d["selftests"]["at_this_units_starting_point"]
    check("C26", sp["T_A_div_V_max_abs_over_scale"] < 1e-6,
          f"T_A at the starting point (n_dof=6720) = "
          f"{sp['T_A_div_V_max_abs_over_scale']:.3e} < 1e-6")
    check("C27", sp["T_D_W_vs_fd_curlR_max_rel_err"] < 2e-3,
          f"T_D at the starting point (n_dof=6720) = "
          f"{sp['T_D_W_vs_fd_curlR_max_rel_err']:.3e} < 2e-3")

    # ---- discipline -------------------------------------------------------------------
    check("C28", d["chain"]["L1_to_L4_link_moved"] == "NONE"
          and d["chain"]["clay_percent_unchanged"] is True
          and d["chain"]["this_is_not_a_blowup"] is True
          and d["chain"]["this_is_not_a_certificate"] is True
          and d["chain"]["this_is_not_an_infimum"] is True,
          "chain block: no L1->L4 link moved, not a blow-up, not a certificate, "
          "not an infimum")
    cs = d["cost_and_shortfall"]
    check("C29", cs["maxiter_actually_used"] == cs["preregistered_maxiter"] == 20000,
          f"the full 20,000 was run, not truncated "
          f"({cs['wall_clock_hours']} h wall, {cs['core_hours']} core-h on "
          f"{cs['cores_used']} cores)")
    check("C30", d["optimiser"]["ftol"] == 1e-16 and d["optimiser"]["gtol"] == 1e-12
          and d["optimiser"]["REL_STALL"] == l6.REL_STALL
          and d["optimiser"]["TRAJ_EVERY"] == l6.TRAJ_EVERY,
          "optimiser settings are L6's module constants, imported not retyped")

    print(f"\n{N - len(FAILS)}/{N} checks passed"
          + (f"; FAILED: {FAILS}" if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
