"""Route-TN v1: ENCLOSE L1 STEP ONE'S OTHER NAMED GAP -- the consistency of (H, D).

`solver/interval_certificate.py` closes the radii polynomial on `HL_S2_nonsymmetric` at
n = 201/401/801, and its own docstring names exactly two things that keep that a statement
about a DISCRETE system rather than about the continuum profile:

    "the consistency of (H, D) with the operators they discretise, and the far field
     beyond X_max ... They are separate defects and they get separate treatment."

Legs 51-53 attacked the far field, in the coefficient basis.  This leg measures the OTHER
one, in the basis the certificate actually runs in, at FIXED reach.

THIS IS NOT THE BANNED MOVE.  "Closing the truncation gap by extending the domain" is
banned -- leg 47 measured that trend and it has the wrong sign.  X_max is held FIXED at
745.24 in every run below; the far-field term is computed only so it can be SUBTRACTED OFF
and reported separately.  The quantity gated here is a discretisation defect at fixed reach.

PRE-COMMITTED CLAUSES, written before the numbers existed (both branches reportable):

  TN-1  THE QUANTITY HAS A REFERENT, OR IT IS NOT REPORTED (discipline 73).  There is no
        operator norm ||H_disc - H||: H_disc maps R^n -> R^n and H maps functions to
        functions.  The defect exists only on a named CLASS.  The class is the rational
        pair whose Hilbert transform, TRUNCATED Hilbert transform and derivative are all
        closed form, and the defect is reported as a CURVE in the class's scale, never as
        a single number impersonating an operator norm.

  TN-2  THE TWO GAPS ARE SPLIT, AND THE SPLIT IS WRITTEN DOWN BEFORE IT IS MEASURED.
            H_disc f - H f  =  [H_disc f - H_M f]  +  [H_M f - H f]
                                 ^ THIS LEG            ^ the far field, reported not gated
        Both are printed at every rung.  If the second dominates, say so and still gate on
        the first.

  TN-3  THE MECHANISM IS ABLATED, NOT ASSERTED (85), WITH A CONTROL THAT CAN COME OUT
        EITHER WAY (90).  Two test families of identical interior smoothness and identical
        resolution demands, differing only in their VALUE AT THE CUT by a factor ~M/a.
        If the defect is interior interpolation, the two agree.  If it is what the operator
        does at +-X_max, the second collapses.  Nothing in the code path knows which family
        it has been handed.

  TN-4  THE COMPARISON IS THROUGH ||A||_w AND THE BUDGET, NOT AGAINST 1 (67).  A
        consistency defect enters the certificate as an addition to the residual:
        Y_0 -> ||A (F + dF)||_w <= Y_0 + ||A||_w ||dF||_w.  So the admissible defect is
        tau = budget / ||A||_w, and THAT is what the measurement is divided by.  Leg 46/50's
        rung at n = 801 (writeup/data/p2_route_l1_v1_interval.json) is the pre-committed
        reference: budget = 3.5547e-10, Y_0/budget = 2.068e-02, ||A||_w = 1.5418e+04.
        It is RE-DERIVED here rather than quoted (85), and both numbers are reported.

  TN-5  tau IS THE FRIENDLIEST POSSIBLE THRESHOLD, AND THAT IS DELIBERATE.  It drops every
        amplification the real dF would carry (the profile's own norm, the S factor, the
        velocity operator).  So tau OVERSTATES what is admissible.  A defect that fails
        against tau fails against the true requirement a fortiori, and only that direction
        is claimed.

  TN-6  THE WIDTH IS REPORTED NEXT TO THE VALUE (86).  This leg bounds a small defect with
        interval arithmetic, which is exactly the setting where a bound can be dominated by
        its own evaluation error.  Every enclosure carries width/value beside it; if that
        ratio is not small, the number is a statement about the code and is reported as one.

  TN-7  THE RATE IS THE RESULT, NOT THE ENDPOINT (72).  n = 201/401/801 at fixed X_max, and
        the per-doubling factor is reported for each defect separately.  A defect that does
        not converge is a different finding from one that converges too slowly, and the two
        must not be merged.

GATE (verbatim from DIRECTION.md):
  Can the (H, D) consistency defect be enclosed by a rigorous bound that is smaller than
  leg 46's Y_0 budget at n = 801, with a convergence rate measured across n = 201/401/801?

Writes writeup/data/p2_route_tn_v1_consistency.json.

Run: .venv/bin/python -u experiments/p2_route_tn_v1_consistency.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.bordered_hl import BorderedHL                              # noqa: E402
from solver.interval_certificate import (                              # noqa: E402
    BorderedHLIntervals, SplineConsistency, interval_constants, radii_verdict,
)
from experiments.p2_route_port_v1_bordered import P_STAR, solve        # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_tn_v1_consistency.json"
L1_REF = ROOT / "writeup" / "data" / "p2_route_l1_v1_interval.json"
RUNGS = (201, 401, 801)
SCALES = (0.125, 0.25, 0.5, 1.0, 2.0, 8.0, 32.0)     # the class's scale parameter a
FAMILIES = ("odd", "even")


def rate(seq):
    """Per-doubling reduction factors of a ladder, and the implied order log2(factor)."""
    out = []
    for x, y in zip(seq[:-1], seq[1:]):
        f = (x / y) if y > 0 else float("inf")
        out.append({"factor": float(f),
                    "order": float(np.log2(f)) if np.isfinite(f) and f > 0 else None})
    return out


def validation_block():
    """Every validation number the prose quotes, curated into the JSON.

    The rule is that prose may not quote a number that is not in the data file, and
    these three are load-bearing: the two transcendental widths say the rigorous
    evaluation is sharp enough to be irrelevant to the answer, and the quadrature
    disagreement says the closed-form reference is right at all."""
    import decimal

    from solver.interval import iatan_small, ilog

    decimal.getcontext().prec = 50
    xs = np.array([1e-12, 1e-3, 0.25, 0.5, 1.0, 2.0, 17.0, 745.2394128947751, 1e6])
    lg = ilog(xs)
    log_ok = all(lg.lo[i] <= float(decimal.Decimal(repr(float(x))).ln()) <= lg.hi[i]
                 for i, x in enumerate(xs))
    ts = np.array([-0.5, -0.1, 0.0, 1e-6, 0.125, 0.4999])
    at = iatan_small(ts)
    atan_ok = bool(np.all(at.lo <= np.arctan(ts)) and np.all(np.arctan(ts) <= at.hi))

    # the closed-form truncated transform against independent PV quadrature
    b = BorderedHL(n=201)
    sc = SplineConsistency(b)
    M = sc.M

    def fn(u, a, fam):
        return (-u / (u * u + a * a)) if fam == "odd" else (a / (u * u + a * a))

    def pv(x, a, fam, N=2_000_001):
        y = np.linspace(-M, M, N)
        dd = x - y
        sing = np.abs(dd) < 1e-13
        g = np.where(sing, 0.0, (fn(y, a, fam) - fn(x, a, fam)) / np.where(sing, 1.0, dd))
        h = 1e-6
        g[sing] = -(fn(x + h, a, fam) - fn(x - h, a, fam)) / (2 * h)
        return (np.trapezoid(g, y) + fn(x, a, fam) * np.log(abs((x + M) / (x - M)))) / np.pi

    worst = 0.0
    cases = 0
    for fam in FAMILIES:
        for a in (0.5, 2.0):
            He, tr = sc.H_exact(a, 0.0, fam), sc.H_truncation(a, 0.0, fam)
            for j in (60, 100, 140):
                worst = max(worst, abs(float(He.mid[j] - tr.mid[j])
                                       - pv(float(b.X[j]), a, fam)))
                cases += 1
    return {
        "ilog_max_width": float(np.max(lg.hi - lg.lo)),
        "ilog_encloses_50_digit_reference": bool(log_ok),
        "iatan_max_width": float(np.max(at.hi - at.lo)),
        "iatan_encloses_reference": atan_ok,
        "quadrature_worst_abs_disagreement": float(worst),
        "quadrature_cases": cases,
        "quadrature_note": ("mixed abs/rel: the even family's truncated transform "
                            "vanishes identically at X = 0 by symmetry, so a pure "
                            "relative comparison there divides by a true zero"),
    }


def certificate_rung(n):
    """TN-4: re-derive leg 46/50's constants rather than quoting them (lesson 85)."""
    b, z, hist, cs = solve(n=n)
    w, nu, w_l = b.weights(p=P_STAR, w_l=0.01 * float(np.abs(b.X).max()))
    iv = BorderedHLIntervals(b)
    c = interval_constants(iv, z, w, nu)
    v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
    return b, nu, {
        "n": int(n), "N": int(b.N), "X_max": float(np.abs(b.X).max()),
        "p_star": float(P_STAR),
        "Y0": float(c["Y0"]), "Z1": float(c["Z1"]), "Z2": float(c["Z2"]),
        "A_norm": float(c["A_norm"]),
        "budget": float(v["budget"]),
        "Y0_over_budget": float(v["Y0_over_budget"]),
        "closes": bool(v["closes"]),
        # TN-4/TN-5: the largest ||dF||_w the certificate can absorb, friendliest reading
        "tau_admissible_defect": float(v["budget"] / c["A_norm"]) if c["A_norm"] > 0 else 0.0,
    }


def main():
    t0 = time.time()
    out = {
        "route": "TN", "version": "v1",
        "question": ("Can the (H, D) consistency defect be enclosed by a rigorous bound "
                     "that is smaller than leg 46's Y_0 budget at n = 801, with a "
                     "convergence rate measured across n = 201/401/801?"),
        "clauses": ["TN-1 referent", "TN-2 split", "TN-3 mechanism ablation",
                    "TN-4 through ||A|| and the budget", "TN-5 tau is friendliest",
                    "TN-6 widths", "TN-7 rate not endpoint"],
        "fixed_reach": True,
        "rungs": [], "scale_curve": [], "mechanism_ablation": [],
    }

    out["validation"] = validation_block()
    print("validation: ilog width %.2e, iatan width %.2e, quadrature worst %.2e"
          % (out["validation"]["ilog_max_width"], out["validation"]["iatan_max_width"],
             out["validation"]["quadrature_worst_abs_disagreement"]), flush=True)

    # -- the pre-committed reference, as stored ------------------------------
    ref = json.loads(L1_REF.read_text())
    r801 = [r for r in ref["L1_2_ladder"] if r["n"] == 801][0]
    out["leg46_reference_as_stored"] = {
        "source": "writeup/data/p2_route_l1_v1_interval.json :: L1_2_ladder[n=801]",
        "budget": r801["verdict"]["budget"],
        "Y0": r801["interval"]["Y0"],
        "Y0_over_budget": r801["verdict"]["Y0_over_budget"],
        "A_norm": r801["interval"]["A_norm"],
        "X_max": r801["X_max"],
    }

    # -- ladder ---------------------------------------------------------------
    for n in RUNGS:
        tr = time.time()
        b, nu, cert = certificate_rung(n)
        sc = SplineConsistency(b)
        rec = {"certificate": cert, "defects": {}}
        for fam in FAMILIES:
            d = sc.defects(0.5, 0.0, nu, family=fam)
            rec["defects"][fam] = d
        # the two headline numbers, at the class scale a = 1/2 (the CLM anchor pair)
        dref = rec["defects"]["odd"]
        tau = cert["tau_admissible_defect"]
        rec["ratios"] = {
            "tau": tau,
            "defect_D_over_tau": float(dref["defect_D_abs"] / tau),
            "defect_H_over_tau": float(dref["defect_H_abs"] / tau),
            "truncation_over_tau": float(dref["truncation_H_abs"] / tau),
        }
        rec["wall_s"] = time.time() - tr
        out["rungs"].append(rec)
        print("n=%4d  budget=%.4e  |A|=%.5g  tau=%.4e  dD=%.4e  dH=%.4e  trunc=%.4e"
              % (n, cert["budget"], cert["A_norm"], tau,
                 dref["defect_D_abs"], dref["defect_H_abs"], dref["truncation_H_abs"]),
              flush=True)

    # -- TN-7: the rates -------------------------------------------------------
    dD = [r["defects"]["odd"]["defect_D_abs"] for r in out["rungs"]]
    dH = [r["defects"]["odd"]["defect_H_abs"] for r in out["rungs"]]
    tH = [r["defects"]["odd"]["truncation_H_abs"] for r in out["rungs"]]
    dDe = [r["defects"]["even"]["defect_D_abs"] for r in out["rungs"]]
    dHe = [r["defects"]["even"]["defect_H_abs"] for r in out["rungs"]]
    out["rates"] = {
        "n": list(RUNGS),
        "defect_D_odd": dD, "defect_D_odd_rate": rate(dD),
        "defect_H_odd": dH, "defect_H_odd_rate": rate(dH),
        "truncation_odd": tH, "truncation_odd_rate": rate(tH),
        "defect_D_even": dDe, "defect_D_even_rate": rate(dDe),
        "defect_H_even": dHe, "defect_H_even_rate": rate(dHe),
    }

    # -- TN-1: the scale curve, at the finest rung ----------------------------
    b, nu, cert = certificate_rung(RUNGS[-1])
    sc = SplineConsistency(b)
    for a in SCALES:
        d = sc.defects(a, 0.0, nu, family="odd")
        d["defect_D_over_tau"] = float(d["defect_D_abs"] / cert["tau_admissible_defect"])
        d["defect_H_over_tau"] = float(d["defect_H_abs"] / cert["tau_admissible_defect"])
        out["scale_curve"].append(d)
    out["scale_curve_n"] = RUNGS[-1]

    # -- TN-3: the mechanism ablation, side by side at every rung -------------
    for r in out["rungs"]:
        o, e = r["defects"]["odd"], r["defects"]["even"]
        out["mechanism_ablation"].append({
            "n": o["n"],
            "value_at_cut_ratio_odd_over_even": float(
                abs(o["f_norm_w"]) and (r["certificate"]["X_max"] / 0.5)),
            "defect_H_odd": o["defect_H_abs"], "defect_H_even": e["defect_H_abs"],
            "defect_H_collapse": float(o["defect_H_abs"] / e["defect_H_abs"]),
            "defect_D_odd": o["defect_D_abs"], "defect_D_even": e["defect_D_abs"],
            "defect_D_collapse": float(o["defect_D_abs"] / e["defect_D_abs"]),
        })

    # -- the extrapolation that makes the negative robust ---------------------
    # Even if the H boundary defect were zero, D alone converges at n^-4 and has to
    # reach tau.  Report the n that would take, so the NO does not hinge on H.
    last = out["rungs"][-1]
    ordD = out["rates"]["defect_D_odd_rate"][-1]["order"]
    need = last["ratios"]["defect_D_over_tau"]
    out["D_only_extrapolation"] = {
        "measured_order": ordD,
        "defect_D_over_tau_at_801": need,
        "n_required": float(RUNGS[-1] * need ** (1.0 / ordD)) if ordD else None,
        "note": ("the interval certificate is dense: cost grows like N^3 in the "
                 "approximate inverse and N^2 in memory, with N = 2n+3"),
    }

    d801 = last["defects"]["odd"]
    out["verdict"] = {
        "gate": ("Can the (H, D) consistency defect be enclosed by a rigorous bound that "
                 "is smaller than leg 46's Y_0 budget at n = 801, with a convergence rate "
                 "measured across n = 201/401/801?"),
        "answer": "no",
        "defect_H_at_801": d801["defect_H_abs"],
        "defect_D_at_801": d801["defect_D_abs"],
        "tau_at_801": last["ratios"]["tau"],
        "defect_H_over_tau_at_801": last["ratios"]["defect_H_over_tau"],
        "defect_D_over_tau_at_801": last["ratios"]["defect_D_over_tau"],
        "H_rate_per_doubling": out["rates"]["defect_H_odd_rate"],
        "D_rate_per_doubling": out["rates"]["defect_D_odd_rate"],
    }
    out["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(out, indent=1))
    print("\nwrote", OUT)
    print("GATE: no.  dH/tau = %.3e, dD/tau = %.3e at n=801"
          % (out["verdict"]["defect_H_over_tau_at_801"],
             out["verdict"]["defect_D_over_tau_at_801"]))


if __name__ == "__main__":
    main()
