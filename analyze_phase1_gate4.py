"""Gate 4 analysis — the FROZEN six-property pass/fail predicate (PHASE1_PLAN.md).

Committed BEFORE the run so a rail is a finding, not a nudge. Reads
experiments/phase1_gate4.jsonl and reports each property PASS/FAIL plus the
overall verdict. Thresholds inherited from Stage 1.5 (five properties) and
Stage 2.5 (the non-trivial-optimum property), in the frozen constants below.

The six properties (on the nu_crit-analog fitness):
  1. Nonzero          -- uncensored growers have nu_crit > 2*tol (not dead-flat).
  2. Finite           -- nothing censored high (blow-up doesn't survive nu=hi).
  3. Monotone         -- 0 monotonicity-probe violations (measured at N-coarse).
  4. Resolution-stable-- |nu_crit(coarse) - nu_crit(fine)| <= 2*tol per shape,
                         and no shape that grew at coarse rails/expands at fine.
  5. Wide band        -- (max-min) nu_crit spread >= WIDEBAND_MIN * tol.
  6. Non-trivial optimum -- the landscape winner is a STRUCTURED shape (not a
                         trivial low-(1,1) concentration), AND nu_crit is not
                         strongly organized by the centroid dissipation scaling
                         (rho(nu_crit, centroid) > -RHO_MAX). This is the property
                         that killed 1D gCLM (STAGE_2_5_RESULTS.md, rho=0.79).

Usage: .venv/bin/python analyze_phase1_gate4.py [--in experiments/phase1_gate4.jsonl]
"""

import argparse
import json
from collections import defaultdict

import numpy as np

# --- FROZEN thresholds (pre-committed) ---
TOL = 5e-3                    # the bisection tolerance (phase1_gate4.NU_TOL)
NONZERO_MIN = 2 * TOL        # 0.010: a shape is "nonzero" above this
NONZERO_FRAC = 0.80          # >= 80% of uncensored growers must clear it
RESSTAB_MAX = 2 * TOL        # 0.010: max |Delta nu_crit| across resolutions
WIDEBAND_MIN = 10            # (max-min)/tol must exceed this (Stage 1.5: 12x)
RHO_MAX = 0.70              # |rho(nu_crit, centroid)| below this passes (2.5: 0.79 FAIL)
WINNER_CENTROID_MIN = 1.3 * np.sqrt(2.0)  # winner must sit clearly above the (1,1) floor
GAP_MIN = 10 * TOL          # 0.050: reported gap top vs runner-up (Stage 2.5 diag)


def load(path):
    """Group rows by label into {label: {class, buoyancy, descriptors, byN}}."""
    shapes = defaultdict(lambda: {"byN": {}})
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            s = shapes[r["label"]]
            s["cls"] = r["shape_class"]
            s["buoyancy"] = r["buoyancy"]
            s["descriptors"] = r["descriptors"]
            s["byN"][r["resolution_N"]] = r
    return shapes


def _pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def analyze(path):
    shapes = load(path)
    resolutions = sorted({n for s in shapes.values() for n in s["byN"]})
    n_coarse = resolutions[0]
    n_fine = resolutions[-1] if len(resolutions) > 1 else None

    # coarse-resolution rows, split by censoring
    coarse = {lbl: s["byN"][n_coarse] for lbl, s in shapes.items() if n_coarse in s["byN"]}
    uncensored = {lbl: r for lbl, r in coarse.items() if r["bracket_censored"] is None}
    growers = uncensored  # uncensored == crossed A_CRIT somewhere in (0, hi)

    print(f"Gate 4 analysis: {len(shapes)} shapes, resolutions {resolutions}")
    print(f"  uncensored growers @N={n_coarse}: {len(growers)} / {len(coarse)} "
          f"(censored low: "
          f"{sum(r['bracket_censored']=='low' for r in coarse.values())}, "
          f"high: {sum(r['bracket_censored']=='high' for r in coarse.values())})\n")

    results = {}

    # --- 1. Nonzero ---
    nz = [r["nu_crit"] for r in growers.values() if r["nu_crit"] > NONZERO_MIN]
    frac_nz = len(nz) / max(len(growers), 1)
    p1 = len(growers) >= 3 and frac_nz >= NONZERO_FRAC
    results["1. nonzero"] = (p1, f"{len(nz)}/{len(growers)} growers > 2*tol "
                                 f"({frac_nz:.0%}, need {NONZERO_FRAC:.0%})")

    # --- 2. Finite ---
    n_high = sum(r["bracket_censored"] == "high" for r in coarse.values())
    p2 = n_high == 0
    results["2. finite"] = (p2, f"{n_high} shapes censored high (need 0)")

    # --- 3. Monotone ---
    viol = sum(r["n_monotone_violations"] for r in coarse.values())
    n_probed = sum(r["n_monotone_probes"] > 0 for r in coarse.values())
    p3 = viol == 0
    results["3. monotone"] = (p3, f"{viol} probe violations across {n_probed} "
                                  f"probed bisections (need 0)")

    # --- 4. Resolution-stable ---
    deltas, rail = [], []
    if n_fine is not None:
        for lbl, s in shapes.items():
            rc, rf = s["byN"].get(n_coarse), s["byN"].get(n_fine)
            if not rc or not rf or rc["bracket_censored"] is not None:
                continue
            if rf["bracket_censored"] is not None or rf["n_bracket_expansions"] > 0:
                rail.append(lbl)          # grew at coarse, rails/expands at fine
            else:
                deltas.append((lbl, abs(rc["nu_crit"] - rf["nu_crit"])))
        max_d = max((d for _, d in deltas), default=0.0)
        worst = max(deltas, key=lambda t: t[1], default=("-", 0.0))
        p4 = (not rail) and max_d <= RESSTAB_MAX
        results["4. resolution-stable"] = (
            p4, f"max |dnu|={max_d:.4f} ({worst[0]}) <= {RESSTAB_MAX:.4f}; "
                f"rails/expands: {rail or 'none'}")
    else:
        results["4. resolution-stable"] = (None, "single resolution -- not evaluated")

    # --- 5. Wide band ---
    vals = [r["nu_crit"] for r in growers.values()]
    band = (max(vals) - min(vals)) if len(vals) >= 2 else 0.0
    p5 = band >= WIDEBAND_MIN * TOL
    results["5. wide band"] = (p5, f"spread {band:.4f} = {band/TOL:.1f}*tol "
                                   f"(need >= {WIDEBAND_MIN}*tol)")

    # --- 6. Non-trivial optimum ---
    ranked = sorted(growers.items(), key=lambda kv: -kv[1]["nu_crit"])
    if len(ranked) >= 3:
        win_lbl, win = ranked[0]
        win_cls = shapes[win_lbl]["cls"]
        win_centroid = shapes[win_lbl]["descriptors"]["centroid"]
        gap = win["nu_crit"] - ranked[1][1]["nu_crit"]
        cen = [shapes[l]["descriptors"]["centroid"] for l, _ in ranked]
        spl = [shapes[l]["descriptors"]["split"] for l, _ in ranked]
        aln = [shapes[l]["descriptors"]["alignment"] for l, _ in ranked]
        nus = [r["nu_crit"] for _, r in ranked]
        rho_c = _pearson(nus, cen)
        rho_s = _pearson(nus, spl)
        rho_a = _pearson(nus, aln)
        winner_structured = (win_cls != "trivial") and (win_centroid >= WINNER_CENTROID_MIN)
        not_centroid_ruled = not (rho_c < -RHO_MAX)  # strongly negative == trivial cheat
        p6 = winner_structured and not_centroid_ruled
        results["6. non-trivial optimum"] = (
            p6, f"winner={win_lbl}[{win_cls}] nu={win['nu_crit']:.4f} "
                f"centroid={win_centroid:.2f} gap={gap:.4f} ({gap/TOL:.1f}*tol); "
                f"rho(nu,centroid)={rho_c:+.2f} (need > {-RHO_MAX:+.2f}); "
                f"rho(nu,split)={rho_s:+.2f} rho(nu,align)={rho_a:+.2f}")
        top5 = ", ".join(f"{l}[{shapes[l]['cls'][:4]}]={r['nu_crit']:.3f}"
                         for l, r in ranked[:5])
    else:
        results["6. non-trivial optimum"] = (None, "too few growers to rank")
        top5 = ""

    # --- report ---
    print("PROPERTY VERDICTS (frozen predicate):")
    passed = failed = 0
    for name, (ok, detail) in results.items():
        # ok may be a numpy bool or None; dispatch on None-ness then truthiness
        # (identity checks against True/False fail for numpy bools).
        if ok is None:
            tag = "N/A "
        elif ok:
            tag = "PASS"; passed += 1
        else:
            tag = "FAIL"; failed += 1
        print(f"  [{tag}] {name:24s} -- {detail}")
    if top5:
        print(f"\n  top-5 by nu_crit: {top5}")

    # All six properties must PASS (none failing, none N/A) to clear the gate.
    overall = "PASS -- proceed to the GA campaign (Gate 5)" \
        if failed == 0 and passed == len(results) \
        else "FAIL -- STOP. A finding, not a push-harder signal (per Stages 2.5/3.5/3.6)."
    print(f"\nOVERALL: {passed} pass / {failed} fail  =>  {overall}")
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="experiments/phase1_gate4.jsonl")
    args = ap.parse_args()
    analyze(args.inp)
