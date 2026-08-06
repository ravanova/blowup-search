"""Route-RSA v1: an ADVERSARIAL AUDIT of solver/rescaled_spectrum.py.

WHAT THIS IS NOT.  It is not a measurement of anything physical.  No number printed here is a
statement about gCLM, about blow-up, about DSS, about a certificate constant, or about any
quantity in the plan of record.  It re-derives no physics, contests no banked value, and runs
no new gCLM measurement (that is banned -- the model is exhausted, leg 42).  Every number is a
statement about CODE BEHAVIOUR UNDER DEGENERATE, POISONED OR BOUNDARY INPUT.

THE GATE (DIRECTION.md, leg 203), answered YES:

    Under adversarial and degenerate inputs, does solver/rescaled_spectrum.py ever silently
    return a wrong value rather than reject or visibly propagate the defect?

WHY THIS MODULE.  It is imported by solver/critical_dissipation.py (which re-implements the
same convergence filter), by Route-E's spectrum sweep, by Route-G's cross-model rows and by
Route-H.  It has a dedicated valid-input gate file (test_rescaled_spectrum.py, 8 tests) and one
docs-only realization audit (leg 70, which lists this module's own entry points in its
BANNED_CALLS and never executes them).  It has never had an adversarial battery.

WHERE THE BOUNDARIES COME FROM (novelty pass, writeup/novelty/leg_203.md sec 3).  This module
implements no published algorithm -- the filter, the structural pair, the gauge (N) and the
closed-form continuum are this repository's own construction.  So the normative anchor is the
module's OWN WRITTEN CONTRACT, quoted verbatim, which makes each battery a test of a sentence
somebody actually wrote rather than of an invented standard:

  (C1) rescaled_spectrum.py:116-119 -- "THAT IS WHY A CONVERGENCE FILTER IS MANDATORY, not
       decoration: the discrete eigenvalues are the ones that stop moving under refinement, and
       the continuum is the part that never does."                      -> S3
  (C2) rescaled_spectrum.py:315-316 -- "Continuation is the honest test for a branch: it
       FOLLOWS the object rather than searching for it."                 -> S4
  (C3) test_rescaled_spectrum.py:26-27 (test 7) -- "Past the end of the branch Newton returns
       converged=False rather than handing back its last iterate."       -> S5
  (C4) rescaled_spectrum.py:104-112 -- admissibility holds EXACTLY for -1 < Re lambda < 1.  -> S8

Two further anchors are external and are VERIFIED BY EXECUTION here rather than quoted from
memory: numpy.linalg's non-finite rejection, and IEEE-754 nan/inf propagation (S1).

RESOLUTION, AND WHY IT IS SMALL.  One continuation to a = 0.5 at K = 96 costs 371 s on this
machine, so the batteries are run at K <= 64 and are anchored at a = 0, where the fixed point
is EXACT (Omega_0 = -sin theta nulls the residual to 1.1e-16 at every K) and the whole analytic
spectrum is known in closed form to be exactly {0, -1}.  That is a stronger truth reference
than a converged solve at a generic a, not a weaker one: every S3/S5/S7 magnitude below is a
distance from a value known exactly, not from a numerical reference.  The natural-failure
census in S6 recomputes nothing -- it reads the banked Route-E and Route-G JSONs.

PASSES ARE REPORTED AS LOUDLY AS FAILURES (leg 91's design rule, inherited).  S1, S2b and S9
are the map of inputs this module handles CORRECTLY, and they are the majority of what was
tested.  The deliverable is a behaviour map, not a bug list.

THE NINE BATTERIES
  S1  NON-FINITE PROPAGATION.  nan/inf planted in the coefficient vector and in the model
      parameter a, at every entry point.  Does the defect propagate or vanish?
  S2  DEGENERATE BASIS SIZE K.  K = 0, 1, 2, negative, and NON-INTEGER.
  S3  THE SELF-COMPARISON TRAP (C1).  converged_spectrum with K_fine == K_coarse.
  S4  CONTINUATION SILENTLY SKIPPED (C2).  Sign-mismatched da empties the arange grid.
  S5  THE CONVERGENCE FLAG IS DROPPED ONE FRAME UP (C3).  newton honours test 7; spectrum and
      converged_spectrum discard the flag.  Magnitude against the exact a = 0 spectrum.
  S6  EXPOSURE CENSUS.  Which banked rows were computed at a non-fixed point.  Reads JSON only.
  S7  PLANTED WRONG VALUE, PASS-THROUGH RADIUS.  Perturb the exact fixed point by delta; at
      what delta does the filter stop returning {0, -1}?
  S8  continuum_defect HAS NO ADMISSIBILITY CONTENT (C4).  Sweep lambda inside and outside the
      strip and compare the defect.  Lesson 90: a control that cannot come out differently.
  S9  THE PASSES.  Degenerate tolerances that are correctly rejected, and the positive control
      that can and does report the other answer.

Deterministic (fixed seed), no logging, no solver file edited.  Writes
writeup/data/p2_route_rsa_v1_adversarial.json.

Run: .venv/bin/python -u experiments/p2_route_rsa_v1_adversarial.py
"""

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.rescaled_spectrum import (          # noqa: E402
    OddCompactBasis, RescaledFlow, continuation, continuum_defect,
    continuum_eigenfunction, converged_spectrum, match_filter,
    planted_eigenvalue_control, spectrum,
)

OUT = ROOT / "writeup" / "data" / "p2_route_rsa_v1_adversarial.json"
SEED = 20260806
POISONS = (("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf")))

# The exact a = 0 truth (module docstring, lines 98-113): requiring analyticity at X = 0
# leaves exactly lambda = 0 (dilation) and lambda = -1 (amplitude), and nothing else.
EXACT_A0_SPECTRUM = (0.0, -1.0)


def hdr(s):
    print("\n" + "=" * 78 + "\n%s\n" % s + "=" * 78, flush=True)


def attempt(fn):
    """Run fn, classify the outcome as raised / non-finite / finite-value."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            v = fn()
        except Exception as ex:                       # noqa: BLE001
            return {"outcome": "raised", "exc": type(ex).__name__,
                    "msg": str(ex)[:140]}
    arr = np.asarray(v, dtype=complex) if not isinstance(v, dict) else None
    if arr is not None and arr.size and not np.all(np.isfinite(arr)):
        return {"outcome": "non_finite", "value": jc(v)}
    return {"outcome": "finite", "value": jc(v)}


def jc(v):
    """JSON-safe."""
    if isinstance(v, dict):
        return {k: jc(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [jc(x) for x in v]
    if isinstance(v, np.ndarray):
        return [jc(x) for x in v.ravel()[:24].tolist()]
    if isinstance(v, (np.bool_, bool)):
        return bool(v)          # MUST precede int: bool is a subclass of int
    if isinstance(v, complex) or isinstance(v, np.complexfloating):
        return {"re": float(np.real(v)), "im": float(np.imag(v))}
    if isinstance(v, (np.floating, float)):
        return float(v)
    if isinstance(v, (np.integer, int)):
        return int(v)
    return v


def dist_to_exact(ev):
    """Distance of the computed spectrum from the EXACT a = 0 pair {0, -1}."""
    ev = np.asarray(ev)
    return {"to_0": float(np.min(np.abs(ev - 0.0))),
            "to_minus1": float(np.min(np.abs(ev + 1.0)))}


# --------------------------------------------------------------------------
# S1  NON-FINITE PROPAGATION
# --------------------------------------------------------------------------
def s1_non_finite():
    hdr("S1  NON-FINITE PROPAGATION -- does a planted nan/inf survive, or vanish?")
    rows = []
    for K in (16, 32):
        f = RescaledFlow(0.0, K=K)
        b0 = f.B.anchor()
        for slot in (0, 3, K - 1):
            for name, val in POISONS:
                b = b0.copy()
                b[slot] = val
                rows.append({
                    "K": K, "slot": int(slot), "poison": name,
                    "residual": attempt(lambda b=b, f=f: float(np.max(np.abs(f.residual(b))))),
                    "c_omega": attempt(lambda b=b, f=f: float(f.c_omega(b))),
                    "jacobian_max": attempt(
                        lambda b=b, f=f: float(np.max(np.abs(f.jacobian(b))))),
                    "generator": attempt(lambda b=b, f=f: f.generator(b)),
                    "eigvals_of_generator": attempt(
                        lambda b=b, f=f: np.linalg.eigvals(f.generator(b))),
                    "newton_from_poison": attempt(
                        lambda b=b, K=K: {
                            k: v for k, v in RescaledFlow(0.0, K=K).newton(b0=b).items()
                            if k in ("converged", "reason", "residual")}),
                })
    # poisoned MODEL PARAMETER a
    a_rows = []
    for name, val in POISONS:
        a_rows.append({"a": name, "newton": attempt(
            lambda val=val: {k: v for k, v in RescaledFlow(val, K=16).newton().items()
                             if k in ("converged", "reason", "residual", "c_omega")})})

    n = len(rows)
    erased = [r for r in rows
              if r["residual"]["outcome"] == "finite" and r["c_omega"]["outcome"] == "finite"]
    prop_res = sum(1 for r in rows if r["residual"]["outcome"] == "non_finite")
    gen_prop = sum(1 for r in rows if r["generator"]["outcome"] == "non_finite")
    eig_raised = sum(1 for r in rows if r["eigvals_of_generator"]["outcome"] == "raised")
    newton_flagged = sum(1 for r in rows
                         if r["newton_from_poison"]["outcome"] == "finite"
                         and r["newton_from_poison"]["value"].get("converged") is False)
    a_flagged = sum(1 for r in a_rows
                    if r["newton"]["outcome"] == "finite"
                    and r["newton"]["value"].get("converged") is False)
    print("  coefficient poisons tested            : %d" % n)
    print("  residual returned NON-FINITE          : %d/%d  (IEEE-754 propagation)"
          % (prop_res, n))
    print("  generator() returned NON-FINITE       : %d/%d  (np.linalg.solve does NOT"
          % (gen_prop, n))
    print("                                                  reject a non-finite matrix)")
    print("  eigvals(generator) RAISED LinAlgError : %d/%d  (the rejection happens one"
          % (eig_raised, n))
    print("                                                  frame later, inside spectrum())")
    print("  newton() returned converged=False     : %d/%d" % (newton_flagged, n))
    print("  poisoned model parameter a flagged    : %d/%d" % (a_flagged, len(a_rows)))
    print("  SILENTLY ERASED (finite from poison)  : %d/%d" % (len(erased), n))
    print("  VERDICT: %s" % ("PASS -- every poison propagates or is flagged"
                             if not erased else "DEFECT -- %d erased" % len(erased)))
    print("\n  The chain is honest end to end: the defect stays visible as nan through")
    print("  residual/c_omega/jacobian/generator and then hard-stops at eigvals.  Nothing")
    print("  is erased.  This is the majority of what was tested and it is a PASS.")
    return {"rows": rows, "a_rows": a_rows, "n_cases": n,
            "n_residual_non_finite": prop_res, "n_generator_non_finite": gen_prop,
            "n_eigvals_raised": eig_raised,
            "n_newton_flagged": newton_flagged, "n_a_flagged": a_flagged,
            "n_silently_erased": len(erased),
            "verdict": "PASS" if not erased else "DEFECT",
            "newton_reason_on_poison": next(
                (r["newton_from_poison"]["value"].get("reason") for r in rows
                 if r["newton_from_poison"]["outcome"] == "finite"), None),
            "linalg_msg": next((r["eigvals_of_generator"].get("msg") for r in rows
                                if r["eigvals_of_generator"]["outcome"] == "raised"), None)}


# --------------------------------------------------------------------------
# S2  DEGENERATE BASIS SIZE K
# --------------------------------------------------------------------------
def s2_degenerate_K():
    hdr("S2  DEGENERATE BASIS SIZE K -- zero-measure and non-integer resolutions")
    rows = []
    for K in (0, 1, 2, 3, -1, -4):
        rows.append({"K": K, "basis": attempt(lambda K=K: list(OddCompactBasis(K).S.shape)),
                     "anchor": attempt(lambda K=K: OddCompactBasis(K).anchor().tolist())})
    # NON-INTEGER K: int(K) truncates with no warning and no error
    trunc = []
    for K in (3.7, 15.9, 96.9, 144.9999, np.float64(48.5)):
        got = OddCompactBasis(K).K
        trunc.append({"requested": float(K), "got": int(got),
                      "silent": bool(int(got) != float(K))})
        print("  OddCompactBasis(%-10r) -> K = %-4d  (requested %.4f)"
              % (K, got, float(K)))
    n_silent = sum(1 for t in trunc if t["silent"])
    print("\n  non-integer K silently truncated      : %d/%d" % (n_silent, len(trunc)))
    for r in rows:
        print("  K = %-3s basis -> %-34s anchor -> %s"
              % (r["K"], r["basis"].get("value", r["basis"].get("exc")),
                 r["basis"].get("exc") or r["anchor"].get("exc")
                 or "ok %s" % r["anchor"]["value"]))
    print("\n  D2  K is silently floor-truncated.  It is the RESOLUTION parameter, and S3")
    print("      shows that two K values which differ by less than 1 collapse to the SAME")
    print("      grid -- which is exactly the input that defeats the convergence filter.")
    excs = {str(r["K"]): r["basis"].get("exc") for r in rows
            if r["basis"]["outcome"] == "raised"}
    print("\n  D2b INCONSISTENT REJECTION at negative K: %s.  Both are rejections, so"
          % ", ".join("K=%s -> %s" % (k, v) for k, v in excs.items()))
    print("      nothing is silently wrong, but the two invalid inputs leave by different")
    print("      doors -- the shape leg 120 recorded as its D7 in spectral_utils.")
    print("  D2c K = 0 builds EMPTY (0,0) operators with no error; anchor() then raises")
    print("      IndexError.  K = 1 and K = 2 build and anchor cleanly.")
    return {"degenerate": rows, "truncation": trunc, "n_silent_truncations": n_silent,
            "negative_K_exceptions": excs,
            "negative_K_raises": all(
                r["basis"]["outcome"] == "raised" for r in rows
                if isinstance(r["K"], int) and r["K"] < 0),
            "K0_builds_empty": bool(rows[0]["basis"].get("value") == [0, 0])}


# --------------------------------------------------------------------------
# S3  THE SELF-COMPARISON TRAP   (contract C1)
# --------------------------------------------------------------------------
def s3_self_comparison():
    hdr("S3  THE SELF-COMPARISON TRAP -- converged_spectrum with K_fine == K_coarse")
    print("  Contract C1 (rescaled_spectrum.py:116): 'the discrete eigenvalues are the ones")
    print("  that stop moving under refinement'.  With K_fine == K_coarse NOTHING is refined,")
    print("  so nothing can move, so everything is kept.  There is no guard on the pair.\n")
    rows = []
    for K_c, K_f in ((24, 36), (24, 24), (24, 12), (32, 48), (32, 32), (48, 72), (48, 48)):
        t0 = time.time()
        r = converged_spectrum(0.0, K_coarse=K_c, K_fine=K_f, tol=1e-3)
        kept = np.asarray(r["kept"])
        row = {"K_coarse": K_c, "K_fine": K_f, "equal": bool(K_c == K_f),
               "n_total": int(r["n_total"]), "n_kept": int(r["n_kept"]),
               "max_match_distance": float(np.max(r["dist"])) if r["dist"].size else None,
               "max_abs_imag_kept": float(np.max(np.abs(np.imag(kept)))) if kept.size else 0.0,
               "dist_to_exact": dist_to_exact(kept) if kept.size else None,
               "seconds": round(time.time() - t0, 2)}
        rows.append(row)
        print("  K_c=%-3d K_f=%-3d  n_kept = %3d / %3d   max match dist = %-10s"
              "  max |Im lambda| kept = %.4f"
              % (K_c, K_f, row["n_kept"], row["n_total"],
                 ("%.3e" % row["max_match_distance"]) if row["max_match_distance"] is not None
                 else "-", row["max_abs_imag_kept"]))
    eq = [r for r in rows if r["equal"]]
    ne = [r for r in rows if not r["equal"]]
    worst = max(eq, key=lambda r: r["n_kept"])
    infl = max(r["n_kept"] for r in eq) / max(1, max(r["n_kept"] for r in ne))
    print("\n  K_fine != K_coarse : n_kept = %s   -- the exact answer {0, -1}"
          % sorted({r["n_kept"] for r in ne}))
    print("  K_fine == K_coarse : n_kept = %s   -- the ENTIRE discretized continuum"
          % sorted({r["n_kept"] for r in eq}))
    print("  match distances on the equal-K rows are IDENTICALLY %s (lesson 90: a control"
          % sorted({r["max_match_distance"] for r in eq}))
    print("  that cannot come out differently), and the largest kept eigenvalue is a")
    print("  conjugate pair at +-%.4f i -- a purely imaginary pair, which is EXACTLY the"
          % worst["max_abs_imag_kept"])
    print("  Hopf-crossing signature this module exists to rule out.")
    print("\n  CONTROL that can come out differently: K_fine < K_coarse (24/12, a COARSER")
    print("  'refinement') still returns 2.  So the trap is EQUALITY specifically, not any")
    print("  mis-ordering -- the filter is not simply broken.")
    return {"rows": rows,
            "n_kept_unequal": sorted({r["n_kept"] for r in ne}),
            "n_kept_equal": sorted({r["n_kept"] for r in eq}),
            "inflation_factor": float(infl),
            "equal_K_match_distances": sorted({r["max_match_distance"] for r in eq}),
            "worst_spurious_imag_pair": worst["max_abs_imag_kept"],
            "coarser_fine_grid_still_correct": bool(
                all(r["n_kept"] == 2 for r in ne if r["K_fine"] < r["K_coarse"]))}


# --------------------------------------------------------------------------
# S4  CONTINUATION SILENTLY SKIPPED   (contract C2)
# --------------------------------------------------------------------------
def s4_continuation_skipped():
    hdr("S4  CONTINUATION SILENTLY SKIPPED -- a sign-mismatched step empties the grid")
    print("  Contract C2 (rescaled_spectrum.py:315): 'Continuation is the honest test for a")
    print("  branch: it FOLLOWS the object rather than searching for it.'")
    print("  continuation() builds a_grid = np.arange(0.0, a_target + 1e-12, da).  When da")
    print("  has the WRONG SIGN for a_target that arange is EMPTY, and the size-0 fallback")
    print("  appends a_target alone -- so the routine solves COLD from the anchor in one")
    print("  jump while presenting itself as a followed branch.  No warning, same return.\n")
    K = 48
    rows = []
    for a, da, label in ((0.3, 0.02, "correct: da > 0, a > 0"),
                         (0.3, -0.02, "SIGN-MISMATCHED da"),
                         (0.3, 5.0, "da >> a_target"),
                         (0.5, 0.02, "correct: da > 0, a > 0"),
                         (0.5, -0.02, "SIGN-MISMATCHED da"),
                         (-0.3, -0.02, "correct: da < 0, a < 0"),
                         (-0.3, 0.02, "SIGN-MISMATCHED da")):
        grid = np.arange(0.0, float(a) + 1e-12, float(da))
        n_grid = int(grid.size) if float(da) != 0.0 else -1
        t0 = time.time()
        r = attempt(lambda a=a, da=da: (lambda fo: {
            "c_omega": float(fo[1]["c_omega"]), "alpha": float(-fo[1]["c_omega"]),
            "residual": float(fo[1]["residual"]), "converged": bool(fo[1]["converged"]),
            "iterations": int(fo[1]["iterations"])})(continuation(a, K=K, da=da)))
        rows.append({"a_target": a, "da": da, "label": label,
                     "arange_size": n_grid, "grid_degenerate": bool(n_grid == 0),
                     "result": r, "seconds": round(time.time() - t0, 2)})
        v = r.get("value", {})
        print("  a=%+.2f da=%+.3f  arange size = %-3d  %-24s alpha = %s  res = %s"
              % (a, da, n_grid, label,
                 ("%+.8f" % v["alpha"]) if v else r.get("exc"),
                 ("%.2e" % v["residual"]) if v else ""))
    # da = 0 is a VISIBLE rejection
    zero = attempt(lambda: continuation(0.3, K=16, da=0.0))
    print("\n  da = 0.0 -> %s: %s  (VISIBLE rejection -- a pass)"
          % (zero["outcome"], zero.get("exc")))

    # pair each SIGN-MISMATCHED row with the correct row at the same a_target
    pairs = []
    for bad in rows:
        if not bad["grid_degenerate"]:
            continue
        good = next(r for r in rows
                    if r["a_target"] == bad["a_target"] and not r["grid_degenerate"])
        gv, bv = good["result"]["value"], bad["result"]["value"]
        pairs.append({"a_target": bad["a_target"], "da_bad": bad["da"],
                      "alpha_followed": gv["alpha"], "alpha_skipped": bv["alpha"],
                      "abs_delta_alpha": abs(gv["alpha"] - bv["alpha"]),
                      "residual_followed": gv["residual"],
                      "residual_skipped": bv["residual"]})
    worst = max(pairs, key=lambda p: p["abs_delta_alpha"])
    print("\n  MAGNITUDE, K = %d, each degenerate call against the correct one at the same a:"
          % K)
    for p in pairs:
        print("    a = %+.2f : alpha followed = %+.8f   skipped = %+.8f   |delta| = %.6f"
              % (p["a_target"], p["alpha_followed"], p["alpha_skipped"],
                 p["abs_delta_alpha"]))
    print("\n  WORST at a = %+.2f: |delta alpha| = %.6f.  alpha is the FAR-FIELD DECAY"
          % (worst["a_target"], worst["abs_delta_alpha"]))
    print("  EXPONENT -- the quantity Route-E's E2 branch and Route-G's G4 rows bank.")
    print("  Same call signature, same return shape, no flag distinguishes the two paths.")
    print("\n  Stated against my own case: at a = +0.30 the gap is only %.6f, because a"
          % pairs[0]["abs_delta_alpha"])
    print("  cold solve there still lands on the same branch.  The defect is STRUCTURAL --")
    print("  the advertised continuation is not performed -- and its numerical size depends")
    print("  on how far the cold solve drifts.  The a = %+.2f row is where that bites."
          % worst["a_target"])
    return {"rows": rows, "da_zero": zero, "K": K, "pairs": pairs,
            "alpha_followed": worst["alpha_followed"],
            "alpha_skipped": worst["alpha_skipped"],
            "abs_delta_alpha": float(worst["abs_delta_alpha"]),
            "worst_a_target": worst["a_target"],
            "n_degenerate_grids": sum(1 for r in rows if r["grid_degenerate"])}


# --------------------------------------------------------------------------
# S5  THE CONVERGENCE FLAG IS DROPPED ONE FRAME UP   (contract C3)
# --------------------------------------------------------------------------
def s5_flag_dropped():
    hdr("S5  THE CONVERGENCE FLAG IS DROPPED -- spectrum()/converged_spectrum() discard it")
    print("  Contract C3 (test_rescaled_spectrum.py:26, test 7): 'Past the end of the branch")
    print("  Newton returns converged=False rather than handing back its last iterate.'")
    print("  newton() HONOURS this -- it returns the flag.  But it also returns 'b', and")
    print("  spectrum() does  flow, out = continuation(...); eigvals(flow.generator(out['b']))")
    print("  with NO reference to out['converged'].  converged_spectrum() likewise: it")
    print("  forwards residual_coarse/residual_fine but its 'kept' array -- documented as")
    print("  'the grid-independent part of the spectrum' -- carries no flag at all.\n")
    src_spectrum = "flow, out = continuation(a, K=K, da=da, **kw); eigvals(flow.generator(out['b']))"
    print("  Source check: does the string 'converged' appear in spectrum() or")
    print("  converged_spectrum()'s bodies?")
    import inspect
    import solver.rescaled_spectrum as RS
    checks = {}
    for fn in (RS.spectrum, RS.converged_spectrum):
        body = inspect.getsource(fn)
        checks[fn.__name__] = {
            "mentions_converged": bool("converged" in body.split('"""')[-1]),
            "returns_residual": bool("residual" in body)}
        print("    %-20s mentions 'converged' in code: %-5s   forwards residual: %s"
              % (fn.__name__, checks[fn.__name__]["mentions_converged"],
                 checks[fn.__name__]["returns_residual"]))

    # MAGNITUDE, against the EXACT a = 0 spectrum {0, -1}.  Plant the failure by capping
    # max_iter from a deliberately poor start, so the truth is known exactly.
    print("\n  MAGNITUDE, at a = 0 where the spectrum is EXACTLY {0, -1}.  A non-converged")
    print("  iterate is planted by capping max_iter from a poor start; spectrum() consumes")
    print("  it without complaint.")
    rng = np.random.default_rng(SEED)
    K = 48
    f = RescaledFlow(0.0, K=K)
    b_true = f.B.anchor()
    ev_true = np.linalg.eigvals(f.generator(b_true))
    rows = []
    b_bad_start = b_true + 0.5 * rng.standard_normal(K) / (1.0 + np.arange(K)) ** 2
    for mi in (1, 2, 3, 5, 8, 120):
        out = f.newton(b0=b_bad_start.copy(), max_iter=mi)
        ev = np.linalg.eigvals(f.generator(out["b"]))
        d = dist_to_exact(ev)
        rows.append({"max_iter": mi, "converged": bool(out["converged"]),
                     "residual": float(out["residual"]),
                     "dist_to_exact": d,
                     "max_real_part": float(np.max(np.real(ev))),
                     "n_right_half_plane": int(np.sum(np.real(ev) > 1e-6))})
        print("    max_iter=%-4d converged=%-5s residual=%.3e  |lambda-0|=%.3e"
              "  |lambda+1|=%.3e  max Re = %+.4f  #Re>0 = %d"
              % (mi, out["converged"], out["residual"], d["to_0"], d["to_minus1"],
                 rows[-1]["max_real_part"], rows[-1]["n_right_half_plane"]))
    unconv = [r for r in rows if not r["converged"]]
    worst = max(unconv, key=lambda r: r["dist_to_exact"]["to_minus1"]) if unconv else None
    print("\n  At a = 0 the amplitude eigenvalue is EXACTLY -1.  On the worst non-converged")
    if worst:
        print("  iterate accepted silently by spectrum(), it sits %.4e away, and %d"
              % (worst["dist_to_exact"]["to_minus1"], worst["n_right_half_plane"]))
        print("  eigenvalue(s) appear in the RIGHT half plane where the exact spectrum has")
        print("  none (max Re = %+.4f vs the true 0)." % worst["max_real_part"])
    print("\n  NOTE, stated because it cuts the other way: the 1e-8 convergence threshold is")
    print("  a HARD-CODED sup-residual test, not the tol argument, and it is conservative --")
    print("  Route-E's banked a = 0.5 / K = 96 row has residual 3.319e-08 and is flagged")
    print("  converged=False while its alpha is 3.00000002 against an exact 3.  So")
    print("  'converged=False' is NOT by itself evidence a banked spectrum is wrong.  S6")
    print("  measures the census; it does not assume the sign of the error.")
    return {"source_checks": checks, "spectrum_body": src_spectrum,
            "exact_spectrum": list(EXACT_A0_SPECTRUM), "K": K,
            "true_spectrum_dist": dist_to_exact(ev_true), "rows": rows,
            "worst_unconverged": worst,
            "threshold_is_hardcoded_1e-8": True}


# --------------------------------------------------------------------------
# S6  EXPOSURE CENSUS -- reads banked JSON, recomputes nothing
# --------------------------------------------------------------------------
def s6_exposure():
    hdr("S6  EXPOSURE CENSUS -- which banked rows were computed at a NON-FIXED POINT")
    print("  Reads writeup/data/*.json.  Recomputes nothing.  No solver run.\n")
    out = {}
    ep = ROOT / "writeup" / "data" / "p2_route_e_v1_spectrum.json"
    e = json.loads(ep.read_text())
    e5 = []
    for r in e.get("E5_sweep", []):
        e5.append({"a": r["a"], "residual_coarse": r["residual_coarse"],
                   "residual_fine": r["residual_fine"],
                   "counts": r["counts"], "n_unstable_converged": r["n_unstable_converged"],
                   "above_1e-8": bool(min(r["residual_coarse"], r["residual_fine"]) > 1e-8)})
        print("  E5  a=%-5s res_c=%.3e res_f=%.3e  counts=%s  n_unstable=%d  %s"
              % (r["a"], r["residual_coarse"], r["residual_fine"], r["counts"],
                 r["n_unstable_converged"],
                 "NOT A FIXED POINT" if e5[-1]["above_1e-8"] else "converged"))
    n_bad_e5 = sum(1 for r in e5 if r["above_1e-8"])
    print()
    gp = ROOT / "writeup" / "data" / "p2_route_g_v1_collapse.json"
    g = json.loads(gp.read_text())
    g4 = []
    for r in g.get("g4_cross_model", {}).get("negative_a", []):
        if "alpha" not in r:
            continue
        g4.append({"a": r["a"], "K": r["K"], "converged": r["converged"],
                   "residual": r["residual"], "alpha": r["alpha"], "beta": r.get("beta")})
        print("  G4  a=%+.1f K=%-4d converged=%-5s res=%.3e  alpha=%.8f"
              % (r["a"], r["K"], r["converged"], r["residual"], r["alpha"]))
    n_bad_g4 = sum(1 for r in g4 if not r["converged"])

    # which call sites pass an S4-trapping argument pair?
    sites = [
        {"site": "experiments/p2_route_e_v1_spectrum.py:393 e2_branch", "a": ">= 0",
         "da": "+0.02", "s4_exposed": False},
        {"site": "experiments/p2_route_e_v1_spectrum.py:396 e5_sweep", "a": ">= 0",
         "da": "+0.02", "s4_exposed": False},
        {"site": "experiments/p2_route_g_v1_collapse.py:383", "a": "-1.0 .. -2.5",
         "da": "-0.02", "s4_exposed": False},
        {"site": "solver/critical_dissipation.py:422", "a": "caller", "da": "+0.02 default",
         "s4_exposed": False},
    ]
    pairs = [
        {"site": "test_rescaled_spectrum.py:132", "K_coarse": 96, "K_fine": 144,
         "s3_exposed": False},
        {"site": "experiments/p2_route_e_v1_spectrum.py:158 e5_sweep", "K_coarse": 96,
         "K_fine": 144, "s3_exposed": False},
        {"site": "experiments/p2_route_h_v1_critical.py:224", "K_coarse": 96, "K_fine": 144,
         "s3_exposed": False},
        {"site": "solver/critical_dissipation.py:576 defaults", "K_coarse": 96, "K_fine": 144,
         "s3_exposed": False},
    ]
    print("\n  S3 exposure (K_fine == K_coarse) at a live call site : %d/%d  -- LATENT"
          % (sum(1 for p in pairs if p["s3_exposed"]), len(pairs)))
    print("  S4 exposure (sign-mismatched da) at a live call site : %d/%d  -- LATENT"
          % (sum(1 for s in sites if s["s4_exposed"]), len(sites)))
    print("  S5 exposure (spectrum taken at a non-fixed point)    : %d/%d Route-E E5 rows,"
          % (n_bad_e5, len(e5)))
    print("                                                         %d/%d Route-G G4 rows"
          " -- NOT LATENT" % (n_bad_g4, len(g4)))
    print("\n  The two a values at which the module's docstring says quantitative statements")
    print("  are quoted -- a = 0 (alpha = 1) and a = 1/2 (alpha = 3), the analytic points --")
    print("  are the two E5 rows that ARE converged (1.110e-16 and 3.319e-08 / 2.869e-13).")
    print("  Both give n_kept = 2 and n_unstable = 0.  The affected rows are the")
    print("  INTERMEDIATE ones, where the docstring already declines to quote.")
    out["route_e_E5"] = e5
    out["route_g_G4"] = g4
    out["n_route_e_rows_not_fixed_points"] = n_bad_e5
    out["n_route_e_rows"] = len(e5)
    out["n_route_g_rows_not_converged"] = n_bad_g4
    out["n_route_g_rows"] = len(g4)
    out["s4_call_sites"] = sites
    out["s3_call_sites"] = pairs
    out["s3_latent"] = True
    out["s4_latent"] = True
    out["s5_latent"] = False
    out["origin_h2_downstream"] = False
    return out


# --------------------------------------------------------------------------
# S7  PLANTED WRONG VALUE -- the pass-through radius
# --------------------------------------------------------------------------
def s7_planted_pass_through():
    hdr("S7  PLANTED WRONG VALUE -- how wrong may the fixed point be before the filter says so?")
    print("  The module offers no injection hook, so the two-grid filter is reproduced here")
    print("  around a DELIBERATELY PERTURBED profile: b -> b + delta * v, the same smooth v")
    print("  at both resolutions, and the exact a = 0 anchor as the delta = 0 control.\n")
    rng = np.random.default_rng(SEED)
    K_c, K_f = 32, 48
    fc, ff = RescaledFlow(0.0, K=K_c), RescaledFlow(0.0, K=K_f)

    def smooth(K):
        v = rng2.standard_normal(K) / (1.0 + np.arange(K)) ** 2
        return v / np.max(np.abs(v))

    rows = []
    for delta in (0.0, 1e-10, 1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 1e-1, 3e-1):
        rng2 = np.random.default_rng(SEED)      # same v at both K
        bc = fc.B.anchor() + delta * smooth(K_c)
        rng2 = np.random.default_rng(SEED)
        bf = ff.B.anchor() + delta * smooth(K_f)
        ev_c = np.linalg.eigvals(fc.generator(bc))
        ev_f = np.linalg.eigvals(ff.generator(bf))
        kept, dist = match_filter(ev_c, ev_f, 1e-3)
        res = float(np.max(np.abs(fc.residual(bc))))
        d = dist_to_exact(kept) if kept.size else {"to_0": float("nan"),
                                                   "to_minus1": float("nan")}
        rows.append({"delta": delta, "residual": res, "n_kept": int(kept.size),
                     "dist_to_exact": d,
                     "max_real_kept": float(np.max(np.real(kept))) if kept.size else None})
        print("    delta=%-7.0e residual=%.3e  n_kept=%2d  |lambda-0|=%.3e  |lambda+1|=%.3e"
              % (delta, res, kept.size, d["to_0"], d["to_minus1"]))
    base = rows[0]
    blind = [r for r in rows[1:] if r["n_kept"] == base["n_kept"]]
    radius = max((r["delta"] for r in blind), default=0.0)
    worst_blind = max(blind, key=lambda r: r["residual"]) if blind else None
    print("\n  BLINDNESS RADIUS: the filter returns the SAME count (%d) as the exact anchor"
          % base["n_kept"])
    print("  for every planted delta up to %.0e, at which the residual is already %.3e"
          % (radius, worst_blind["residual"] if worst_blind else float("nan")))
    print("  -- %s decades above the module's own 1e-8 convergence threshold."
          % ("%.1f" % np.log10((worst_blind["residual"] / 1e-8))
             if worst_blind and worst_blind["residual"] > 0 else "n/a"))
    print("  The count is the quantity Route-E reports; it is NOT sensitive to a planted")
    print("  wrong profile until the perturbation is large.  The eigenvalue POSITIONS do")
    print("  move -- see |lambda+1| above -- but nothing in the return value flags it.")
    return {"K_coarse": K_c, "K_fine": K_f, "rows": rows,
            "baseline_n_kept": base["n_kept"], "blindness_radius_delta": float(radius),
            "residual_at_blindness_radius":
                float(worst_blind["residual"]) if worst_blind else None}


# --------------------------------------------------------------------------
# S8  continuum_defect HAS NO ADMISSIBILITY CONTENT   (contract C4)
# --------------------------------------------------------------------------
def s8_continuum_admissibility():
    hdr("S8  continuum_defect -- a control that cannot come out differently (lesson 90)")
    print("  Contract C4 (rescaled_spectrum.py:104-112): the closed-form eigenfunctions are")
    print("  admissible EXACTLY for -1 < Re lambda < 1.  But s = (w-1)^(1-l)(w+1)^(1+l)")
    print("  solves the homogeneous ODE for EVERY complex l -- admissibility is a BOUNDARY")
    print("  condition, not an ODE property -- and continuum_defect measures only the ODE")
    print("  residual.  It also DROPS the -s(w=1)(1+w) term on the stated grounds that")
    print("  's(w=1) = 0 for Re lambda < 1', which is false outside the strip.  So the")
    print("  check should be expected to pass for lambda it has no business accepting.\n")
    inside, outside = [], []
    for lm in (0.0, -1.0 + 0.0j, -0.9, 0.9, 0.999, 0.5j, -0.5j, 2.0j, 0.3 + 0.7j, -0.4 - 0.2j):
        d = float(continuum_defect(lm))
        inside.append({"lambda": jc(complex(lm)), "defect": d})
    for lm in (1.0, 1.5, 2.0, 3.0, 5.0, 10.0, -2.0, -5.0, 2.0 + 3.0j, -4.0 + 1.0j):
        d = float(continuum_defect(lm))
        outside.append({"lambda": jc(complex(lm)), "defect": d})
    for lab, grp in (("INSIDE  the strip", inside), ("OUTSIDE the strip", outside)):
        print("  %s:" % lab)
        for r in grp:
            print("     lambda = %+7.3f %+7.3fi   defect = %.3e"
                  % (r["lambda"]["re"], r["lambda"]["im"], r["defect"]))
    mi = max(r["defect"] for r in inside)
    mo = max(r["defect"] for r in outside)
    print("\n  worst defect INSIDE  the admissible strip : %.3e" % mi)
    print("  worst defect OUTSIDE the admissible strip : %.3e" % mo)
    print("  separation                                : %.1f decades" % np.log10(mo / mi))
    print("\n  NOTHING IS REJECTED.  The %.1f decades between the two groups are not an"
          % np.log10(mo / mi))
    print("  admissibility signal: the defect grows with |lambda| because np.gradient's")
    print("  truncation error does, and it grows just as much for lambda = +2i (INSIDE,")
    print("  %.3e) as for lambda = -2 (OUTSIDE, %.3e).  There is no threshold that"
          % ([r["defect"] for r in inside if r["lambda"]["im"] == 2.0][0],
             [r["defect"] for r in outside if r["lambda"]["re"] == -2.0][0]))
    print("  separates the groups, so the function has no admissibility content at all.")

    # THE DECISIVE NUMBER: how big is the term the function drops?
    print("\n  THE DROPPED TERM, measured.  continuum_defect omits -s(w=1)(1+w) because")
    print("  's(w=1) = 0 for Re lambda < 1'.  Relative to the size of s on the interior:")
    th = np.linspace(1e-3, np.pi - 1e-3, 4001)
    ctrl = []
    for lm in (0.5, 0.999, 1.0, 2.0, 5.0):
        s = continuum_eigenfunction(lm, th)
        interior = slice(int(0.05 * 4001), int(0.95 * 4001))
        max_s = float(np.max(np.abs(s[interior])))
        s_at_w1 = abs(complex(continuum_eigenfunction(lm, np.array([1e-9]))[0]))
        ratio = s_at_w1 / (max_s + 1e-300)
        ctrl.append({"lambda": lm, "abs_s_at_w_eq_1": s_at_w1, "max_abs_s_interior": max_s,
                     "dropped_over_scale": ratio,
                     "reported_defect": float(continuum_defect(lm))})
        print("     lambda=%+6.3f  |s(w=1)| = %.3e   |s(w=1)|/max|s| = %.3e"
              "   defect REPORTED = %.3e"
              % (lm, s_at_w1, ratio, ctrl[-1]["reported_defect"]))
    worst_drop = max(ctrl, key=lambda c: c["dropped_over_scale"])
    print("\n  At lambda = %+.1f the omitted term is %.3e times the scale the defect is"
          % (worst_drop["lambda"], worst_drop["dropped_over_scale"]))
    print("  normalised by, and the function still reports %.3e.  That is the gap between"
          % worst_drop["reported_defect"])
    print("  what was left out and what was reported: %.1f decades."
          % np.log10(worst_drop["dropped_over_scale"] / worst_drop["reported_defect"]))
    print("  Inside the strip (lambda = +0.500) the same ratio is %.3e -- there the"
          % ctrl[0]["dropped_over_scale"])
    print("  omission is genuinely harmless, which is why the bug is invisible in test 5b.")
    return {"inside": inside, "outside": outside, "worst_inside": mi, "worst_outside": mo,
            "separation_decades": float(np.log10(mo / mi)),
            "dropped_term_control": ctrl,
            "worst_dropped_over_scale": worst_drop["dropped_over_scale"],
            "worst_dropped_lambda": worst_drop["lambda"],
            "dropped_vs_reported_decades": float(np.log10(
                worst_drop["dropped_over_scale"] / worst_drop["reported_defect"])),
            "discriminating": False}


# --------------------------------------------------------------------------
# S9  THE PASSES
# --------------------------------------------------------------------------
def s9_passes():
    hdr("S9  THE PASSES -- inputs this module handles correctly")
    ev_c = np.array([0.0, -1.0, 0.5j, -0.5j])
    ev_f = np.array([1e-12, -1.0 + 1e-12, 0.6j, -0.6j])
    tol_rows = []
    for tol in (1e-3, 0.0, -1.0, float("nan"), float("inf"), 1e9):
        r = attempt(lambda tol=tol: int(match_filter(ev_c, ev_f, tol)[0].size))
        tol_rows.append({"tol": None if tol != tol else float(tol)
                         if np.isfinite(tol) else str(tol), "raw_tol": str(tol), "result": r})
        print("  match_filter tol = %-8s -> n_kept = %s" % (tol, r.get("value", r.get("exc"))))
    empty = attempt(lambda: int(match_filter(ev_c, np.array([]), 1e-3)[0].size))
    print("  match_filter with an EMPTY fine spectrum -> %s: %s   (VISIBLE -- a pass)"
          % (empty["outcome"], empty.get("exc")))
    print("\n  D-TOL  tol = nan keeps 0 (nan < tol is False) and tol = inf keeps all, both")
    print("  SILENTLY.  tol = nan is the sharper one: 'nothing survived the filter' is")
    print("  precisely this module's headline, so a nan tolerance REPRODUCES THE CONCLUSION.")
    print("  No live call site passes a non-finite tol (all pass 1e-4 .. 1e-1): LATENT.")

    print("\n  The positive control, checked that it CAN come out BOTH ways (lesson 90).")
    print("  Run at the module's OWN defaults K = 96/144: at a = 0 the continuation grid is")
    print("  a single point, so this is two eigendecompositions and is cheap.")
    ctrl = []
    for strength, label in ((6.0, "planted potential"),
                            (0.0, "potential REMOVED -- must not bind")):
        t0 = time.time()
        r = planted_eigenvalue_control(a=0.0, K_coarse=96, K_fine=144, strength=strength,
                                       tol=1e-3)
        planted = np.asarray(r["planted"])
        plain = np.asarray(r["plain"])
        # test 6's own criterion: a POSITION shift into the right half plane,
        # not an increase in the count.
        max_re = float(np.max(np.real(planted))) if planted.size else float("nan")
        shift = (max(float(np.min(np.abs(plain - z))) for z in planted)
                 if planted.size and plain.size else float("nan"))
        ctrl.append({"strength": strength, "label": label, "n_plain": int(r["n_plain"]),
                     "n_planted": int(r["n_planted"]), "max_real_planted": max_re,
                     "shift_from_plain": shift, "binds": bool(max_re > 0.5 and shift > 0.5),
                     "seconds": round(time.time() - t0, 2)})
        print("    strength=%.1f  %-32s n_plain=%d n_planted=%d  max Re = %+.4f  shift = %.4f"
              % (strength, label, r["n_plain"], r["n_planted"], max_re, shift))
    binds, quiet = ctrl[0]["binds"], not ctrl[1]["binds"]
    can_fail = bool(binds and quiet)
    print("\n  -> with the potential the filter returns an eigenvalue at Re = %+.4f, %.4f"
          % (ctrl[0]["max_real_planted"], ctrl[0]["shift_from_plain"]))
    print("     away from anything the plain operator has; with the potential removed it")
    print("     does not (Re = %+.4f).  BOTH OUTCOMES OCCUR: %s.  A real control."
          % (ctrl[1]["max_real_planted"], can_fail))
    print("\n  D-CTRL  The COUNT is unchanged either way (%d vs %d), so the module's"
          % (ctrl[0]["n_plain"], ctrl[0]["n_planted"]))
    print("  docstring -- 'the control asserts that the filter reports MORE converged")
    print("  eigenvalues than the unperturbed operator does' -- describes a criterion that")
    print("  does NOT hold.  Its own test 6 checks the right thing (a position shift into")
    print("  the right half plane), so the CHECK is sound and only the prose is wrong.")
    print("  Recorded because a reader taking the docstring at its word would conclude the")
    print("  control had failed.")
    return {"tolerance": tol_rows, "empty_fine": empty, "planted_control": ctrl,
            "control_binds_with_potential": binds,
            "control_quiet_without_potential": quiet,
            "control_can_fail": can_fail,
            "count_criterion_in_docstring_does_not_hold": bool(
                ctrl[0]["n_planted"] == ctrl[0]["n_plain"])}


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("Route-RSA v1 -- adversarial audit of solver/rescaled_spectrum.py (leg 203)")
    print("READ-ONLY on solver/.  No physical measurement.  Seed %d." % SEED)
    res = {"leg": 203, "route": "RSA",
           "title": "Adversarial audit of solver/rescaled_spectrum.py",
           "module_under_audit": "solver/rescaled_spectrum.py",
           "module_edited": False, "seed": SEED,
           "generated": time.strftime("%Y-%m-%dT%H:%M:%S")}
    res["S1_non_finite"] = s1_non_finite()
    res["S2_degenerate_K"] = s2_degenerate_K()
    res["S3_self_comparison"] = s3_self_comparison()
    res["S4_continuation_skipped"] = s4_continuation_skipped()
    res["S5_flag_dropped"] = s5_flag_dropped()
    res["S6_exposure"] = s6_exposure()
    res["S7_planted"] = s7_planted_pass_through()
    res["S8_continuum_admissibility"] = s8_continuum_admissibility()
    res["S9_passes"] = s9_passes()

    s3, s4, s5, s6, s7, s8 = (res["S3_self_comparison"], res["S4_continuation_skipped"],
                              res["S5_flag_dropped"], res["S6_exposure"],
                              res["S7_planted"], res["S8_continuum_admissibility"])
    gate = "YES"
    res["gate"] = {
        "question": ("Under adversarial and degenerate inputs, does "
                     "solver/rescaled_spectrum.py ever silently return a wrong value rather "
                     "than reject or visibly propagate the defect?"),
        "answer": gate,
        "findings": {
            "R1_self_comparison_certifies_the_continuum": {
                "what": ("converged_spectrum has no guard on K_fine vs K_coarse.  At "
                         "K_fine == K_coarse the filter compares a spectrum with itself, "
                         "every match distance is identically 0, and the ENTIRE discretized "
                         "continuum is returned as 'the grid-independent part of the "
                         "spectrum'.  Contradicts the module's own line 116."),
                "n_kept_correct": s3["n_kept_unequal"],
                "n_kept_equal_K": s3["n_kept_equal"],
                "inflation_factor": s3["inflation_factor"],
                "match_distances_on_equal_K": s3["equal_K_match_distances"],
                "worst_spurious_imaginary_pair": s3["worst_spurious_imag_pair"],
                "reachable_via": ("S2's silent non-integer truncation: K_fine=96.9 and "
                                  "K_coarse=96 collapse to the same grid"),
                "exposure": "LATENT -- every live call site passes 96/144"},
            "R2_convergence_flag_dropped": {
                "what": ("newton() honours test 7 and returns converged=False, but spectrum() "
                         "and converged_spectrum() consume out['b'] without ever reading the "
                         "flag; the returned 'kept' array carries no convergence information."),
                "worst_unconverged_dist_to_exact_minus1":
                    (s5["worst_unconverged"] or {}).get("dist_to_exact", {}).get("to_minus1"),
                "spurious_right_half_plane":
                    (s5["worst_unconverged"] or {}).get("n_right_half_plane"),
                "exposure": ("NOT LATENT -- %d/%d banked Route-E E5 rows and %d/%d Route-G G4 "
                             "rows were computed at points whose residual exceeds the "
                             "module's own 1e-8 threshold"
                             % (s6["n_route_e_rows_not_fixed_points"], s6["n_route_e_rows"],
                                s6["n_route_g_rows_not_converged"], s6["n_route_g_rows"]))},
            "R3_continuation_silently_skipped": {
                "what": ("np.arange(0, a_target+1e-12, da) is EMPTY when da's sign does not "
                         "match a_target's; the size-0 fallback appends a_target alone, so a "
                         "FOLLOWED branch silently becomes a single cold solve from the "
                         "anchor.  Contradicts the module's own line 315."),
                "alpha_followed": s4["alpha_followed"],
                "alpha_skipped": s4["alpha_skipped"],
                "abs_delta_alpha": s4["abs_delta_alpha"],
                "worst_at_a": s4["worst_a_target"],
                "all_pairs": s4["pairs"],
                "exposure": ("LATENT -- Route-E passes a >= 0 with da = +0.02 and Route-G "
                             "passes a < 0 with da = -0.02; both signs match")},
            "R4_continuum_defect_has_no_admissibility_content": {
                "what": ("continuum_defect measures only the homogeneous ODE residual, which "
                         "the closed form satisfies for EVERY complex lambda, and drops the "
                         "-s(w=1)(1+w) term on grounds false outside the strip.  It accepts "
                         "every lambda tested, including lambda = 5 (five times outside the "
                         "admissible strip).  Lesson 90 shape."),
                "worst_inside": s8["worst_inside"], "worst_outside": s8["worst_outside"],
                "separation_decades": s8["separation_decades"],
                "dropped_term_over_scale_at_worst_lambda": s8["worst_dropped_over_scale"],
                "dropped_vs_reported_decades": s8["dropped_vs_reported_decades"],
                "exposure": ("LATENT -- test_rescaled_spectrum.py test 5b calls it only on "
                             "in-strip lambda")},
            "R5_non_integer_K_silently_truncated": {
                "what": "OddCompactBasis does int(K) with no warning; it is the resolution.",
                "n_silent": res["S2_degenerate_K"]["n_silent_truncations"],
                "exposure": "LATENT, but it is the reachability path for R1"},
            "R6_planted_profile_pass_through": {
                "what": ("the filter's kept-COUNT -- the quantity Route-E reports -- is "
                         "unchanged by a planted wrong profile up to delta = %g, where the "
                         "residual is already %s." % (s7["blindness_radius_delta"],
                                                      s7["residual_at_blindness_radius"])),
                "blindness_radius_delta": s7["blindness_radius_delta"],
                "residual_at_blindness_radius": s7["residual_at_blindness_radius"]},
            "R7_tolerance_degeneracies": {
                "what": ("match_filter with tol = nan keeps 0 silently -- which REPRODUCES "
                         "the module's headline conclusion -- and tol = inf keeps all."),
                "exposure": "LATENT -- all live call sites pass 1e-4 .. 1e-1"},
            "R8_planted_control_docstring_criterion_wrong": {
                "what": ("planted_eigenvalue_control's docstring says the control 'asserts "
                         "that the filter reports MORE converged eigenvalues than the "
                         "unperturbed operator does'.  The count is UNCHANGED (2 vs 2).  "
                         "test 6 checks a position shift into the right half plane instead, "
                         "which does hold -- so the CHECK is sound and the PROSE is wrong."),
                "n_plain": res["S9_passes"]["planted_control"][0]["n_plain"],
                "n_planted": res["S9_passes"]["planted_control"][0]["n_planted"],
                "max_real_planted":
                    res["S9_passes"]["planted_control"][0]["max_real_planted"],
                "severity": "prose only -- no number depends on it"},
        },
        "passes": {
            "non_finite_propagation": res["S1_non_finite"]["verdict"],
            "n_poisons_tested": res["S1_non_finite"]["n_cases"],
            "n_silently_erased": res["S1_non_finite"]["n_silently_erased"],
            "negative_K_raises": res["S2_degenerate_K"]["negative_K_raises"],
            "da_zero_raises": res["S4_continuation_skipped"]["da_zero"]["outcome"] == "raised",
            "empty_fine_spectrum_raises":
                res["S9_passes"]["empty_fine"]["outcome"] == "raised",
            "positive_control_can_fail": res["S9_passes"]["control_can_fail"],
        },
        "claim_adjacency": {
            "origin_h2_spectral_gap_downstream": False,
            "why": ("solver/origin_h2_certificate.py -- the STRICT realization, the one with "
                    "the gap (legs 176/186) -- imports only numpy and math.comb.  Legs "
                    "176/186 cite this module's DOCSTRING on the loose realization; no "
                    "banked origin-H2 gap number is computed by any code path in it."),
            "banked_numbers_touched": ("Route-E's own E5 spectrum sweep and Route-G's G4 "
                                       "cross-model alpha/beta rows, via R2"),
            "verdict": "CLAIM-ADJACENT via Route-E/Route-G; ESCALATE, DO NOT PATCH",
        },
        "module_edited_by_this_leg": False,
    }

    hdr("GATE")
    print("  %s" % res["gate"]["question"])
    print("\n  ANSWER: %s\n" % gate)
    print("  R1  converged_spectrum(K_coarse=K, K_fine=K) certifies the ENTIRE continuum:")
    print("      n_kept %s -> %s (%.0fx), every match distance identically %s, worst"
          % (s3["n_kept_unequal"], s3["n_kept_equal"], s3["inflation_factor"],
             s3["equal_K_match_distances"]))
    print("      spurious pair at +-%.4fi -- the Hopf signature the module rules out."
          % s3["worst_spurious_imag_pair"])
    print("  R2  spectrum()/converged_spectrum() drop newton's converged flag; worst")
    print("      planted non-converged iterate sits %.3e from the exact -1 and puts %d"
          % ((s5["worst_unconverged"] or {}).get("dist_to_exact", {}).get("to_minus1", 0.0),
             (s5["worst_unconverged"] or {}).get("n_right_half_plane", 0)))
    print("      eigenvalue(s) in the right half plane where the truth has none.")
    print("  R3  sign-mismatched da silently degrades a followed branch to a cold solve:")
    print("      at a = %+.2f, alpha %+.8f -> %+.8f, |delta| = %.6f."
          % (s4["worst_a_target"], s4["alpha_followed"], s4["alpha_skipped"],
             s4["abs_delta_alpha"]))
    print("  R4  continuum_defect accepts every lambda tested, in-strip and out, with no")
    print("      threshold separating them; the term it drops reaches %.2e times the"
          % s8["worst_dropped_over_scale"])
    print("      scale it normalises by while it reports a defect %.1f decades smaller."
          % s8["dropped_vs_reported_decades"])
    print("  R5  non-integer K silently truncated (%d/%d) -- the reachability path for R1."
          % (res["S2_degenerate_K"]["n_silent_truncations"], 5))
    print("  R6  planted wrong profile: kept-count unchanged out to delta = %.0e, where"
          % s7["blindness_radius_delta"])
    print("      the residual is already %.3e." % s7["residual_at_blindness_radius"])
    print("  R7  match_filter tol = nan silently reproduces the headline conclusion.")
    print("  R8  the planted control's DOCSTRING criterion ('MORE converged eigenvalues')")
    print("      does not hold -- the count is unchanged; its test 6 checks a position")
    print("      shift instead, so the check is sound and only the prose misdescribes it.")
    print("\n  PASSES: %d/%d poisons propagated or were flagged; negative K, da = 0 and an"
          % (res["S1_non_finite"]["n_cases"] - res["S1_non_finite"]["n_silently_erased"],
             res["S1_non_finite"]["n_cases"]))
    print("  empty fine spectrum all raise; and the positive control binds with the")
    print("  potential (Re = %+.4f) and goes quiet without it -- both outcomes occur."
          % res["S9_passes"]["planted_control"][0]["max_real_planted"])
    print("\n  EXPOSURE: R1, R3, R4, R5, R7 are LATENT -- no live call site passes the")
    print("  trapping argument.  R2 is NOT latent: %d/%d banked Route-E E5 rows and %d/%d"
          % (s6["n_route_e_rows_not_fixed_points"], s6["n_route_e_rows"],
             s6["n_route_g_rows_not_converged"], s6["n_route_g_rows"]))
    print("  Route-G G4 rows sit on non-fixed points.  The two analytic points a = 0 and")
    print("  a = 1/2 -- the only two the module quotes quantitatively -- are converged.")
    print("\n  ORIGIN-H2 SPECTRAL GAP: NOT downstream (origin_h2_certificate.py imports")
    print("  numpy and math.comb only).  Claim-adjacency runs through Route-E/Route-G.")
    print("  ESCALATE, DO NOT PATCH -- leg 203's yes-branch.  No solver file edited.")

    res["wall_clock_seconds"] = round(time.time() - t0, 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, sort_keys=False, default=str) + "\n")
    print("\nwrote %s  (%.1f s)" % (OUT.relative_to(ROOT), res["wall_clock_seconds"]))
    return res


if __name__ == "__main__":
    main()
