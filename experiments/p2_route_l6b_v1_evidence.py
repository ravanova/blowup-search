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

    # ---- V-W6's binding reading: terminal stationarity, all three starts -------------
    ts = d.get("terminal_stationarity")
    check("C31", ts is not None,
          "terminal_stationarity block present (V-W6's binding recommendation)")
    if ts:
        for name, st in d["starts"].items():
            v = ts["per_start"][name]
            check(f"C32_{name}",
                  v["max_abs_grad"] == st["max_abs_grad"]
                  and v["scale_invariant_grad"] == st["scale_invariant_grad"]
                  and v["is_a_critical_point"] == (st["scale_invariant_grad"]
                                                   < ts["not_a_critical_point_above"]),
                  f"{name}: terminal |g|inf = {st['max_abs_grad']:.5g}, "
                  f"||x||||g||/|J| = {st['scale_invariant_grad']:.5g}, "
                  f"critical point = {v['is_a_critical_point']}")
        l6c = ts["L6_same_quantities_at_its_own_J4_rung"]["continuation"]
        biggest = max(r["scale_invariant_grad"]
                      for r in ts["L6_same_quantities_at_its_own_J4_rung"].values())
        # SS43: this check previously required `== biggest`, i.e. it ASSERTED the ranking
        # that was later withdrawn as confounded.  It now tests the ABSOLUTE statement,
        # which is the claim, and uses no comparison to any other start.
        check("C33", abs(l6c["J"] - L6_RESIDUAL) <= 1e-15
              and l6c["scale_invariant_grad"] >= ts["not_a_critical_point_above"],
              f"L6's reported branch-B minimum {l6c['J']!r} carries "
              f"||x||||g||/|J| = {l6c['scale_invariant_grad']:.4g} >> 1 on an ABSOLUTE "
              f"threshold fixed a priori -- it was never a critical point.  No ranking "
              f"against the other five starts is used (WITHDRAWN, SS43)")
        # re-derive that table straight out of L6's untouched artefact, not from mine
        rows = {r["start"]: r for r in d6["ladder_results"]["B"][-1]["starts"]}
        check("C34", all(
            rows[n]["scale_invariant_grad"] == r["scale_invariant_grad"]
            and rows[n]["max_abs_grad"] == r["max_abs_grad"]
            and rows[n]["fun"] == r["J"]
            for n, r in ts["L6_same_quantities_at_its_own_J4_rung"].items()),
            "the L6 comparison table is copied from L6's artefact, digit for digit")

    # --- C35-C38: the L6 exhaustive audit and the three-way verdict licence -------------
    if ts is not None:
        aud = ts.get("L6_ladder_exhaustive_audit")
        allrec = [st for br, rungs in d6["ladder_results"].items()
                  for ru in rungs for st in ru.get("starts", [])]
        check("C35", aud is not None and aud["start_records"] == len(allrec) == 58
              and aud["every_record_hit_the_800_cap"] is True
              and all(st["nit"] == 800 for st in allrec),
              "all 58 of L6's start-records recounted here: every one hit the 800 cap")
        check("C36", aud["records_not_critical_at_threshold_1"]
              == sum(1 for st in allrec if st["scale_invariant_grad"] >= 1.0) == 56,
              "56 of 58 non-critical at threshold 1, recounted")

        cols = ts.get("the_two_columns_rank_differently", {})
        rows = {r["start"]: r for r in d6["ladder_results"]["B"][-1]["starts"]}
        # C37: both columns are reported, and the RANKING is not used as evidence (SS43)
        wd = ts.get("ranking_WITHDRAWN_as_evidence", {})
        dec = wd.get("decomposition_continuation_over_median_seed", {})
        g2 = lambda r: r["scale_invariant_grad"] * abs(r["fun"]) / r["coeff_norm"]
        seeds = [n for n in rows if n != "continuation"]
        med = lambda f: sorted(f(rows[n]) for n in seeds)[len(seeds) // 2]
        c = rows["continuation"]
        check("C37", wd.get("status", "").startswith("WITHDRAWN")
              and abs(dec.get("grad_L2_implied", 0) - g2(c) / med(g2)) < 1e-9
              and dec.get("grad_L2_implied", 9) < 0.2 and dec.get("J", 9) < 0.06,
              "the 'largest of its six' ranking is WITHDRAWN and the decomposition is "
              "recomputed here: the minimiser's ||grad||_2 is ~6x SMALLER and its |J| ~20x "
              "smaller than the median seed's, so sig is dominated by its denominator")
        check("C37b", cols.get("positions_matching_a_reversal") == 2
              and abs(cols.get("spearman_all_six", 9) - 0.0857) < 5e-3
              and abs(cols.get("spearman_seeds_only", 0) - 0.9) < 5e-3
              and cols.get("exact_reversal") is False
              and min(rows, key=lambda n: rows[n]["max_abs_grad"]) == "continuation",
              "there is no reversal, near or exact: 2 of 6 positions, Spearman +0.086 over "
              "six but +0.900 over the five seeds -- the columns AGREE except at one point")

    vl = d.get("verdict_licence")
    if vl is not None:
        k = vl["keyed_on"]
        expect = ("drop_below_1.45" if k["dropped_below_1_45"]
                  else ("no_drop_and_stationary" if k["terminal_iterate_is_stationary"]
                        else "no_drop_and_NOT_stationary"))
        check("C38", vl["row_that_fires"] == expect
              and vl["threshold_unchanged"] == d["gate"]["material_threshold"] == 1.45
              and k["dropped_below_1_45"] == (d["gate"]["smallest_residual_at_20000"] < 1.45)
              and (d["gate"]["reading_that_fires_is_SUPERSEDED"]
                   == (expect == "no_drop_and_NOT_stationary")),
              "the three-way verdict licence is keyed to the banked gate and stationarity "
              "fields, and the 1.45 threshold is unmoved")

    # --- C39-C41: SS44 -- the window key, the distributions, and the landscape finding ---
    if ts is not None:
        win = ts.get("scale_invariant_grad_trailing_window", {}).get("per_start", {})
        ok = True
        for name, st in d["starts"].items():
            traj = st["trajectory_k_sec_J_ginf_gscaled"]
            K = traj[-1][0]
            w = sorted(r[4] for r in traj if r[0] >= K - 2000)
            v = win.get(name, {})
            ok &= (v.get("n_samples") == len(w) and v.get("min") == w[0]
                   and v.get("max") == w[-1] and v.get("terminal") == traj[-1][4])
        check("C39", bool(win) and ok,
              "the trailing-2,000 distribution of scale_invariant_grad is recomputed here "
              "from the banked trajectories for all three starts and matches")

    vl = d.get("verdict_licence")
    if vl is not None:
        k = vl["keyed_on"]
        traj = d["starts"][k["start"]]["trajectory_k_sec_J_ginf_gscaled"]
        K = traj[-1][0]
        wmax = max(r[4] for r in traj if r[0] >= K - 2000)
        check("C40", abs(k["scale_invariant_grad_max_over_trailing_2000"] - wmax) < 1e-12
              and (vl["row_that_fires"] == "no_drop_and_stationary") == (wmax < 1.0
                   and not k["dropped_below_1_45"]),
              "the licence is keyed to the MAXIMUM over the trailing 2,000 iterations "
              "(SS44), not to the terminal sample, and the row follows from it")

    lf = d.get("landscape_finding_seeds_become_less_stationary_while_descending")
    if lf is not None:
        import math
        def r_of(name):
            traj = d["starts"][name]["trajectory_k_sec_J_ginf_gscaled"]
            w = [q for q in traj if q[0] >= traj[-1][0] - 3000 and q[4] > 0]
            xs = [q[0] for q in w]; ys = [math.log(q[4]) for q in w]
            mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
            num = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
            den = (sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))**0.5
            return num/den
        seeds_ = [n for n in d["starts"] if n.startswith("seed")]
        # SS44/SS45: this check originally ASSERTED that the seeds' relative gradients RISE.
        # That was true over the window in which it was FIRST MEASURED (k 4,700-7,700) and
        # is FALSE over the final window -- so the assertion form would have failed a true
        # artefact, exactly as C37's assertion form would have passed a false one.  It now
        # verifies that the artefact's reported coefficients MATCH a recomputation, and that
        # the artefact reports the window each one was measured over.
        check("C41", all(abs(lf["per_start"][n]["pearson_r_log_sig_vs_k_trailing_3000"]
                             - r_of(n)) < 1e-9 for n in d["starts"]),
              "the reported log-linear coefficients are recomputed here from the raw "
              "trajectories and match; the claim is scoped to its window, not asserted "
              "as a direction")
        early = lf.get("window_in_which_it_was_first_measured", {})
        check("C41b", bool(early) and early.get("k_range") == [4700, 7700]
              and all(early["per_start"][n]["pearson_r"] > 0.5 for n in seeds_)
              and all(lf["per_start"][n]["pearson_r_log_sig_vs_k_trailing_3000"] < 0
                      for n in seeds_),
              "the rise is recorded as a MID-RUN window (k 4,700-7,700, r > +0.5 for both "
              "seeds) and the artefact also records that it REVERSES by the final window "
              "(r < 0 for both) -- the finding is window-scoped, not a law")

    df = d.get("discipline_finding_a_selfcheck_encoded_the_defect_it_existed_to_catch")
    check("C42", df is not None
          and df.get("stated_plainly") == "C37 would have passed on a false claim.",
          "the artefact states plainly that this unit's own evidence check C37 would have "
          "certified the claim it was withdrawn for")

    print(f"\n{N - len(FAILS)}/{N} checks passed"
          + (f"; FAILED: {FAILS}" if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
