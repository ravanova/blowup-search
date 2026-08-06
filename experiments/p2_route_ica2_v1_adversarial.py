"""Route-ICA2 (leg 201): the DEGENERATE-BAND battery for `interval_certificate.py`.

WHAT THIS ASKS, AND WHY IT IS NOT LEG 98's QUESTION
-----------------------------------------------------------------------------
Leg 98 (Route-ICA) already pointed a 39-case fabrication battery at this module and found
12 false accepts out of 36 hypothesis-violating inputs; the repairs are in the shipped
file (`_hypothesis_violations`, `_containment_screen`, the weight-sign check, the
`Z_2 == 0` structured verdict) and its battery lives in
`test_interval_certificate_adversarial.py`.  **Every one of leg 98's 39 cases is a
normal-range float.**  It asked whether the module enforces the HYPOTHESES it is imported
under.  It did not ask whether the module's own ARITHMETIC is a bound.

Leg 69 (Route-IA) found two real soundness gaps in the primitive underneath,
`solver/interval.py`, and repaired them THERE:

  (D1) the purely RELATIVE error bound `gamma_m * sum|x_j y_j|` underflows to zero once
       the individual products go subnormal, while the true accumulation error is
       ABSOLUTE -- a few eta.  Repaired by Rump's explicit eta term (BIT 52:201-220,
       2012); `_ETA_TERMS_PLAIN = 2`, `_ETA_TERMS_DOT2 = 8`, applied in `isum`, `matvec`
       and `dot2_matvec`.
  (D2) Dekker's splitting constant `2^27 + 1` overflows for `|operand| >= 2^997`, silently
       returning a NaN error term.  Repaired by raising `OverflowError` in `_two_product`.

THE QUESTION NOBODY HAS ASKED is what happens when `interval_certificate.py`'s OWN
routines -- not `interval.py`'s -- are driven into those two bands.  That is this battery.

WHAT COUNTS AS A FAILURE, PRE-COMMITTED
-----------------------------------------------------------------------------
A case FAILS -- is a `silent_wrong` -- when a routine RETURNS NORMALLY a value that is
not what it claims:

  * for an enclosure routine, an interval `[lo, hi]` that does NOT contain the exact real
    value of the quantity it encloses.  The exact value is computed in `fractions.
    Fraction` from the same float inputs, so the reference is exact, not a tighter float;
  * for a bound routine, a returned bound STRICTLY BELOW the exact quantity it bounds;
  * for `interval_constants`, a returned `Y_0` strictly below the exact
    `max_i w_i |(A F(z))_i|`.

Three outcomes are recorded per case, and only the first is a failure:

  `silent_wrong`   returned normally, and the returned value is not a bound  -- UNSOUND
  `sound`          returned normally, and the returned value IS a bound      -- sound
  `raised`         an exception propagated                                   -- sound but
                   loud; recorded separately because a broad `except` in a caller could
                   still turn it into a silent skip (leg 98's convention, kept).

MAGNITUDES, NOT BOOLEANS (discipline 73)
-----------------------------------------------------------------------------
Every case records the exact-rational reference, the returned endpoints, the signed
containment escape in units of eta = 2^-1074, AND the escape as a fraction of the returned
magnitude -- because an escape of 200 eta is meaningless until you know whether that is
1e-14 of the value or 33% of it.  A case that holds reports `0.0` eta, never "pass".

THE CONTROL, AND WHY IT CAN COME OUT THE OTHER WAY (discipline 90)
-----------------------------------------------------------------------------
Leg 53's failure was a control computed from objects that could not vary.  The control
here is `solver.interval.matvec` -- the REPAIRED sibling of the routine under test -- run
on BYTE-IDENTICAL input.  If the input were simply "too hard for interval arithmetic",
both would escape and the control would report a failure too.  It is a real control: it
varies, and what it isolates is the clone, not the data.

Run: .venv/bin/python experiments/p2_route_ica2_v1_adversarial.py
"""

import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.interval import Interval, dot2_matvec, matvec
from solver.interval_certificate import (BorderedCLMIntervals, CertificateInputError,
                                         _scale_rows, interval_constants,
                                         matmul_point_interval, radii_verdict,
                                         weighted_rowsum_bound)
from solver.weight_search import BorderedCLM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_ica2_v1_adversarial.json")

ETA = 2.0 ** -1074
POW997 = 2.0 ** 997
N_GRID = 101
THETA = (0.0, 0.0, 0.0, 0.0, -2.0)      # leg 98's gauge, reused so the substrates match

# The two accumulation lengths the shipped certificate actually runs at, so the battery is
# not measuring a length nothing uses: BorderedCLM n=101 -> N=103; BorderedHL n=201 -> N=405.
LIVE_M = (103, 405)


# --------------------------------------------------------------------------
# exact references (fractions.Fraction -- every double is a dyadic rational, exactly)
# --------------------------------------------------------------------------
def exact_matvec_row(M_row, lo, hi):
    """Exact (min, max) of sum_j M_j b_j over b in [lo, hi], as Fractions.

    M is a POINT row, so the extremum is attained at an endpoint componentwise and the
    monotone split is exact -- no optimisation, just a sum of per-term extrema."""
    slo = Fr(0)
    shi = Fr(0)
    for j in range(len(M_row)):
        a = Fr(float(M_row[j]))
        t1, t2 = a * Fr(float(lo[j])), a * Fr(float(hi[j]))
        slo += min(t1, t2)
        shi += max(t1, t2)
    return slo, shi


def escape_eta(lo, hi, exact_lo, exact_hi):
    """Signed containment escape in units of eta. POSITIVE means the enclosure MISSES.

    Returns (escape, which_side): the larger of (lo - exact_lo) and (exact_hi - hi)."""
    e_lo = float(Fr(float(lo)) - exact_lo) / ETA
    e_hi = float(exact_hi - Fr(float(hi))) / ETA
    return (e_lo, "lower") if e_lo >= e_hi else (e_hi, "upper")


def rel_escape(escape, lo, hi):
    """The escape as a fraction of the returned magnitude -- the number that says whether
    an eta-scale escape is a rounding curiosity or a third of the answer."""
    m = max(abs(float(lo)), abs(float(hi)))
    return float(escape * ETA / m) if m > 0 else float("inf")


# --------------------------------------------------------------------------
# the deterministic subnormal construction, derived from the mechanism, not searched
# --------------------------------------------------------------------------
# WHY THESE TWO CONSTANTS.  With every M entry = 2^-537 and every v entry = k * 2^-537, the
# products are all exactly k * eta -- subnormal, and each one lands on a HALF-INTEGER
# multiple of eta when k is a half-integer, so its rounding is a forced tie:
#
#   k = 1.5 -> 1.5 eta ties to 2 eta (even)  -> each product rounds UP   by 0.5 eta
#   k = 2.5 -> 2.5 eta ties to 2 eta (even)  -> each product rounds DOWN by 0.5 eta
#
# Subnormal ADDITION is exact, so the m per-product errors accumulate without further
# rounding: the float sum is off by exactly m/2 eta, in a direction I choose with k.  The
# relative guard term gamma_m * (mass ~ 1e-321) underflows to 0, so the only protection
# left is the single outward nextafter push, worth 1 eta.  The escape is therefore
# (m/2 - 1) eta by construction -- predicted before it was measured, and the measurement
# below matches it exactly at every m.
#
# k = 1.5 walks the LOWER endpoint above the truth (the enclosure sits entirely too high);
# k = 2.5 walks the UPPER endpoint below the truth, which is the one that understates a
# MAGNITUDE and therefore the one that reaches Y_0.
#
# THE ANALYTIC VALUE IS A BOUND, AND THE MEASUREMENT IS 1 eta INSIDE IT, AT EVERY m.
# The hand analysis above gives (m/2 - 1) eta.  What is MEASURED is (m/2 - 2) eta -- the
# same slope, one eta tighter, at m = 4, 8, 16, 64, 103, 200 and 405 alike.  The missing
# eta is one rounding in the BLAS accumulation `Mp @ Blo`, which this module does not own
# and which is not entitled to be predicted from the operation count.  Both numbers are
# recorded per case (`analytic_escape_bound_eta`, `measured_minus_analytic`) rather than
# the analysis being quietly retuned to match: what is claimed is the SHAPE -- the escape
# grows LINEARLY in the accumulation length with slope 1/2 eta per term (discipline 72,
# report the shape of a ladder, not its endpoint) -- and the shape is what both agree on.
_SUB_BASE = 2.0 ** -537
_K_UP, _K_DOWN = 1.5, 2.5


def subnormal_case(m, k):
    """(M, v) whose products are all exactly k * eta."""
    return np.full((1, m), _SUB_BASE), np.full(m, k * _SUB_BASE)


class SubnormalToy:
    """A minimal enclosure class whose A @ F products all land in the subnormal range.

    It exists to carry the defect END TO END, into `interval_constants`' returned `Y_0`,
    rather than stopping at the helper routine.  It is a LINEAR system (identity
    Jacobian), which is the most favourable possible case: nothing about the escape
    depends on the problem being hard."""

    def __init__(self, m, k):
        self.n = self.N = m
        self.f = np.full(m, k * _SUB_BASE)

    def F_float(self, z):
        return self.f.copy()

    def F(self, z):
        return Interval.point(self.f)

    def jacobian(self, z):
        return np.eye(self.N), np.eye(self.N)

    def bilinear_bound(self, w, nu):
        return 1.0


# --------------------------------------------------------------------------
# the battery
# --------------------------------------------------------------------------
def run(write=True, verbose=True):
    cases = []

    def rec(cid, family, target, band, outcome, **kw):
        row = {"case": cid, "family": family, "target": target, "band": band,
               "outcome": outcome}
        row.update(kw)
        cases.append(row)
        if verbose:
            tag = {"silent_wrong": "!! SILENT_WRONG", "sound": "   sound",
                   "raised": "   raised"}[outcome]
            print(f"{tag}  {cid}")
        return row

    # ======================================================================
    # SUB -- the subnormal band (leg 69's defect 1, asked of THIS module)
    # ======================================================================
    for m in (4, 16, 64) + LIVE_M:
        for k, tag in ((_K_UP, "up"), (_K_DOWN, "down")):
            M, v = subnormal_case(m, k)
            lo, hi = matmul_point_interval(M, v[:, None], v[:, None])
            elo, ehi = exact_matvec_row(M[0], v, v)
            esc, side = escape_eta(lo[0, 0], hi[0, 0], elo, ehi)
            rec(f"SUB01_matmul_point_interval_m{m}_{tag}", "SUB",
                "interval_certificate.matmul_point_interval", "subnormal",
                "silent_wrong" if esc > 0 else "sound",
                m=m, k=k, returned_lo=float(lo[0, 0]), returned_hi=float(hi[0, 0]),
                exact=float(elo), escape_eta=esc, escape_side=side,
                escape_relative=rel_escape(esc, lo[0, 0], hi[0, 0]),
                analytic_escape_bound_eta=(m / 2.0 - 1.0),
                measured_minus_analytic=esc - (m / 2.0 - 1.0),
                note=("the enclosure lies entirely above the true value" if side == "lower"
                      else "the upper endpoint is below the true value, so the MAGNITUDE "
                           "is understated -- this is the one that reaches Y_0"))

    # -- THE CONTROL: the REPAIRED sibling on byte-identical input (discipline 90) ------
    for m in LIVE_M:
        for k, tag in ((_K_UP, "up"), (_K_DOWN, "down")):
            M, v = subnormal_case(m, k)
            r = matvec(M, Interval(v, v))
            elo, ehi = exact_matvec_row(M[0], v, v)
            esc, side = escape_eta(r.lo[0], r.hi[0], elo, ehi)
            rec(f"SUB02_CONTROL_interval_matvec_m{m}_{tag}", "SUB",
                "interval.matvec (leg 69 REPAIRED -- the control)", "subnormal",
                "silent_wrong" if esc > 0 else "sound",
                m=m, k=k, returned_lo=float(r.lo[0]), returned_hi=float(r.hi[0]),
                exact=float(elo), escape_eta=esc, escape_side=side,
                note=("byte-identical input to SUB01. This control CAN fail -- if the data "
                      "were simply too hard, it would. It does not, which is what "
                      "attributes the escape to the clone rather than the input."))

    # -- the second control: the SAME routine in the NORMAL range ----------------------
    rng = np.random.default_rng(20201)
    for m in LIVE_M:
        M = rng.standard_normal((1, m))
        v = rng.standard_normal(m)
        lo, hi = matmul_point_interval(M, v[:, None], v[:, None])
        elo, ehi = exact_matvec_row(M[0], v, v)
        esc, side = escape_eta(lo[0, 0], hi[0, 0], elo, ehi)
        rec(f"SUB03_CONTROL_matmul_normal_range_m{m}", "SUB",
            "interval_certificate.matmul_point_interval", "normal",
            "silent_wrong" if esc > 0 else "sound",
            m=m, returned_lo=float(lo[0, 0]), returned_hi=float(hi[0, 0]),
            exact=float(elo), escape_eta=esc, escape_side=side,
            note="the SAME routine, O(1) data: sound. The defect is band-specific.")

    # -- randomised sweep, to show the deterministic case is not a special point -------
    worst = {"escape_eta": 0.0}
    n_esc = 0
    trials = 240
    for t in range(trials):
        m = 200
        scale = 10.0 ** rng.uniform(-165, -150)
        M = rng.standard_normal((1, m)) * scale
        v = rng.standard_normal(m) * scale
        lo, hi = matmul_point_interval(M, v[:, None], v[:, None])
        elo, ehi = exact_matvec_row(M[0], v, v)
        esc, side = escape_eta(lo[0, 0], hi[0, 0], elo, ehi)
        if esc > 0:
            n_esc += 1
            if esc > worst["escape_eta"]:
                worst = {"escape_eta": esc, "side": side, "trial": t,
                         "returned_lo": float(lo[0, 0]), "returned_hi": float(hi[0, 0]),
                         "exact": float(elo)}
    rec("SUB04_random_subnormal_sweep", "SUB",
        "interval_certificate.matmul_point_interval", "subnormal",
        "silent_wrong" if n_esc else "sound",
        m=200, trials=trials, escaping_trials=n_esc,
        escape_rate=n_esc / trials, worst=worst,
        note="random data at input scales 1e-165..1e-150; the deterministic SUB01 "
             "construction is the worst case of the same mechanism, not a separate one.")

    # -- END TO END: does it reach `interval_constants`' returned Y_0? -----------------
    for m in LIVE_M:
        iv = SubnormalToy(m, _K_DOWN)
        A = np.full((m, m), _SUB_BASE)
        w = np.ones(m)
        try:
            c = interval_constants(iv, np.zeros(m), w, w, A=A)
            y_true = float(m * Fr(_SUB_BASE) * Fr(_K_DOWN * _SUB_BASE))
            deficit = y_true - c["Y0"]
            rec(f"SUB05_interval_constants_Y0_m{m}", "SUB",
                "interval_certificate.interval_constants", "subnormal",
                "silent_wrong" if deficit > 0 else "sound",
                m=m, Y0_returned=c["Y0"], Y0_exact=y_true,
                ratio_returned_over_exact=c["Y0"] / y_true,
                understated_percent=100.0 * (1.0 - c["Y0"] / y_true),
                deficit_abs=deficit, deficit_eta=deficit / ETA,
                Z1=c["Z1"], Z2=c["Z2"],
                note="Y_0 is a claimed UPPER bound on max_i w_i |(A F)_i| and comes back "
                     "strictly below it. No exception, no warning, `rigorous: True`.")
        except Exception as e:                                  # pragma: no cover
            rec(f"SUB05_interval_constants_Y0_m{m}", "SUB",
                "interval_certificate.interval_constants", "subnormal", "raised",
                m=m, exception=type(e).__name__, message=str(e)[:300])

    # -- why leg 98's containment screen does not see it -------------------------------
    m = 405
    iv = SubnormalToy(m, _K_DOWN)
    A = np.full((m, m), _SUB_BASE)
    w = np.ones(m)
    c = interval_constants(iv, np.zeros(m), w, w, A=A)
    y_float = float(np.max(np.abs(w * (A @ iv.F_float(None)))))
    rec("SUB06_containment_screen_blind_to_it", "SUB",
        "interval_certificate._containment_screen", "subnormal", "sound",
        m=m, Y0=c["Y0"], Y0_float=y_float, screen_ratio=y_float / c["Y0"],
        screen_threshold=1.0e4,
        note="the screen compares the enclosure against a FLOAT re-evaluation, and the "
             "float re-evaluation makes the SAME underflow error. Ratio ~1, four decades "
             "inside the threshold. The screen is not broken -- it was built for leg 98's "
             "order-of-magnitude fabrication and correctly reports nothing here. Recorded "
             "so the two defects are not merged (discipline 75).")

    # -- the module's OTHER helpers, same band -----------------------------------------
    for m in LIVE_M:
        _, v = subnormal_case(m, _K_DOWN)
        A_ = np.full((1, m), _SUB_BASE)
        b = weighted_rowsum_bound(A_, A_, np.ones(1), np.full(m, 1.0))
        exact = float(sum(abs(Fr(float(x))) for x in A_[0]))
        rec(f"SUB07_weighted_rowsum_bound_m{m}", "SUB",
            "interval_certificate.weighted_rowsum_bound", "subnormal",
            "silent_wrong" if b < exact else "sound",
            m=m, returned=b, exact=exact, deficit_eta=(exact - b) / ETA,
            note="all terms same sign, so no cancellation and the single outward push "
                 "covers it. Sound in this band.")

    for m in LIVE_M:
        M, v = subnormal_case(m, _K_DOWN)
        s = Interval.point(np.full(1, _SUB_BASE))
        lo, hi = _scale_rows(s, np.full((1, m), _K_DOWN * _SUB_BASE))
        ok = all(Fr(float(lo[0, j])) <= Fr(_SUB_BASE) * Fr(_K_DOWN * _SUB_BASE)
                 <= Fr(float(hi[0, j])) for j in range(m))
        rec(f"SUB08_scale_rows_m{m}", "SUB", "interval_certificate._scale_rows",
            "subnormal", "sound" if ok else "silent_wrong",
            m=m, contains_all=bool(ok),
            note="a single product per entry: <=0.5 ulp, covered by the 1-ulp push even "
                 "subnormal. No accumulation, no gap.")

    r = dot2_matvec(np.full((1, 405), _SUB_BASE), np.full(405, _K_DOWN * _SUB_BASE))
    ex = 405 * Fr(_SUB_BASE) * Fr(_K_DOWN * _SUB_BASE)
    ok = Fr(float(r.lo[0])) <= ex <= Fr(float(r.hi[0]))
    rec("SUB09_CONTROL_dot2_matvec_subnormal", "SUB",
        "interval.dot2_matvec (leg 69 REPAIRED -- the control)", "subnormal",
        "sound" if ok else "silent_wrong",
        m=405, returned_lo=float(r.lo[0]), returned_hi=float(r.hi[0]), exact=float(ex),
        note="the residual path `F` uses this, and it carries the eta term. That is why "
             "the escape enters through A @ F and not through F itself.")

    # ======================================================================
    # OVF -- the 2^997 band (leg 69's defect 2, asked of THIS module)
    # ======================================================================
    try:
        dot2_matvec(np.array([[POW997, 1.0], [1.0, 1.0]]), np.array([1.0, 1.0]))
        rec("OVF01_dot2_matvec_at_2_997", "OVF", "interval.dot2_matvec", "overflow",
            "silent_wrong", note="returned instead of raising")
    except OverflowError as e:
        rec("OVF01_dot2_matvec_at_2_997", "OVF", "interval.dot2_matvec", "overflow",
            "raised", exception="OverflowError", message=str(e)[:200],
            note="leg 69's defect-2 repair, confirmed to still hold one level up: the "
                 "compensated path REFUSES rather than emitting [nan, nan].")

    class BigToy(SubnormalToy):
        """An enclosure class whose `F` reaches 2^997 THROUGH the compensated path.

        The point is to exercise the guard where the shipped classes exercise it: every
        real `F` in this module (`BorderedHLIntervals`, `BorderedCLMIntervals`,
        `KawaharaIntervals`) builds its residual with `dot2_matvec`, so that is the route
        by which an oversized operand actually reaches the certificate entry point."""

        def __init__(self, m):
            self.n = self.N = m
            self.M = np.full((m, m), POW997)
            self.v = np.ones(m)
            self.f = np.full(m, POW997)

        def F(self, z):
            return dot2_matvec(self.M, self.v)

    try:
        ivb = BigToy(8)
        interval_constants(ivb, np.zeros(8), np.ones(8), np.ones(8), A=np.eye(8))
        rec("OVF02_interval_constants_at_2_997", "OVF",
            "interval_certificate.interval_constants", "overflow", "sound",
            note="returned without raising; checked for containment below")
    except OverflowError as e:
        rec("OVF02_interval_constants_at_2_997", "OVF",
            "interval_certificate.interval_constants", "overflow", "raised",
            exception="OverflowError", message=str(e)[:200],
            note="the OverflowError from `_two_product` propagates out of the certificate "
                 "entry point loudly. This is the sound outcome.")
    except Exception as e:                                      # pragma: no cover
        rec("OVF02_interval_constants_at_2_997", "OVF",
            "interval_certificate.interval_constants", "overflow", "raised",
            exception=type(e).__name__, message=str(e)[:200])

    with np.errstate(all="ignore"):
        n_finite_wrong = 0
        worst_ovf = None
        for t in range(200):
            m = 8
            M = rng.standard_normal((1, m)) * (2.0 ** rng.integers(990, 1024))
            v = rng.standard_normal(m) * (2.0 ** rng.integers(990, 1024))
            lo, hi = matmul_point_interval(M, v[:, None], v[:, None])
            if not (np.isfinite(lo).all() and np.isfinite(hi).all()):
                continue                       # nan/inf: caught downstream, not silent
            elo, ehi = exact_matvec_row(M[0], v, v)
            esc, side = escape_eta(lo[0, 0], hi[0, 0], elo, ehi)
            if esc > 0:
                n_finite_wrong += 1
                if worst_ovf is None or esc > worst_ovf["escape_eta"]:
                    worst_ovf = {"escape_eta": esc, "side": side}
        rec("OVF03_matmul_point_interval_overflow_sweep", "OVF",
            "interval_certificate.matmul_point_interval", "overflow",
            "silent_wrong" if n_finite_wrong else "sound",
            trials=200, finite_but_non_containing=n_finite_wrong, worst=worst_ovf,
            note="overflow in this routine always produces inf or nan (inf - inf), never "
                 "a FINITE wrong endpoint; nan/inf then reach `radii_verdict`, which "
                 "rejects them by hypothesis (leg 98's repair). Latent, not silent.")

    for lbl, y0 in (("nan", float("nan")), ("posinf", float("inf"))):
        v = radii_verdict(y0, 0.3, 1.0)
        rec(f"OVF04_radii_verdict_Y0_{lbl}", "OVF", "interval_certificate.radii_verdict",
            "overflow", "silent_wrong" if v["closes"] else "sound",
            closes=bool(v["closes"]), reason=v["reason"][:160],
            note="the downstream backstop for the nan/inf that OVF03 produces.")

    # ======================================================================
    # DEG -- degenerate shapes leg 98 did not reach
    # ======================================================================
    z1_just_below = float(np.nextafter(1.0, -np.inf))
    for cid, (y0, z1, z2, why) in {
        "DEG01_Z1_one_ulp_below_one": (1e-30, z1_just_below, 1.0,
                                       "the tightest admissible contraction"),
        "DEG02_Z2_subnormal": (1e-30, 0.5, 5e-324, "budget overflows to +inf"),
        "DEG03_Y0_subnormal": (5e-324, 0.5, 1.0, "Y_0 at the smallest positive double"),
        "DEG04_Y0_and_Z2_subnormal": (5e-324, 0.5, 5e-324, "both ends degenerate"),
        "DEG05_negative_zeros": (-0.0, -0.0, 1.0,
                                 "-0.0 is a legitimate bound, NOT a violation"),
        "DEG06_Z2_huge": (1e-300, 0.5, 1e300, "budget underflows toward zero"),
    }.items():
        try:
            v = radii_verdict(y0, z1, z2)
            bad = bool(v["closes"]) and (v["r_min"] is not None and
                                         not (v["r_min"] > 0 and v["r_min"] < v["r_max"]))
            rec(cid, "DEG", "interval_certificate.radii_verdict", "degenerate",
                "silent_wrong" if bad else "sound",
                Y0=y0, Z1=z1, Z2=z2, closes=bool(v["closes"]),
                reason=v["reason"][:120], budget=v["budget"],
                r_min=v["r_min"], r_max=v["r_max"], why=why)
        except Exception as e:
            rec(cid, "DEG", "interval_certificate.radii_verdict", "degenerate", "raised",
                Y0=y0, Z1=z1, Z2=z2, exception=type(e).__name__,
                message=str(e)[:200], why=why)

    try:
        iv1 = SubnormalToy(1, 1.0)
        iv1.f = np.array([1e-8])
        c = interval_constants(iv1, np.zeros(1), np.ones(1), np.ones(1), A=np.eye(1))
        exact1 = 1e-8
        rec("DEG07_N_equals_one", "DEG", "interval_certificate.interval_constants",
            "degenerate", "silent_wrong" if c["Y0"] < exact1 else "sound",
            N=1, Y0=c["Y0"], exact=exact1, Z1=c["Z1"], Z2=c["Z2"],
            why="the smallest possible system; m = 1 in every gamma_m")
    except Exception as e:
        rec("DEG07_N_equals_one", "DEG", "interval_certificate.interval_constants",
            "degenerate", "raised", exception=type(e).__name__, message=str(e)[:200])

    # ======================================================================
    # SCOPE -- is either band REACHABLE from a live operator? (measured, not asserted)
    # ======================================================================
    b = BorderedCLM(n=N_GRID)
    z, info = b.newton()
    w, nu = b.weight_vector(THETA)
    ivc = BorderedCLMIntervals(b)
    Jlo, Jhi = ivc.jacobian(z)
    A = np.linalg.inv(0.5 * (Jlo + Jhi))
    Fz = ivc.F(z)
    absmass = np.abs(A) @ np.abs(0.5 * (Fz.lo + Fz.hi))
    min_mass = float(np.min(absmass[absmass > 0]))
    maxent = float(np.max(np.abs(A)))
    # the band is entered only when a whole row's absolute mass is ~ m * eta
    band_top = 405 * ETA
    rec("SCOPE01_BorderedCLM_row_mass", "SCOPE", "solver.weight_search.BorderedCLM",
        "live", "sound",
        n=N_GRID, N=b.N, converged=bool(info["converged"]),
        min_row_abs_mass=min_mass, max_abs_A=maxent,
        subnormal_band_top=band_top,
        decades_of_headroom=float(np.log10(min_mass / band_top)),
        note="the subnormal band is entered only when an ENTIRE row's |A| @ |F| mass is "
             "of order m*eta. The live minimum is this far above it.")

    max_op = max(float(np.max(np.abs(A))), float(np.max(np.abs(b.H))),
                 float(np.max(np.abs(Fz.mid)))) if hasattr(Fz, "mid") else maxent
    rec("SCOPE02_BorderedCLM_vs_2_997", "SCOPE", "solver.weight_search.BorderedCLM",
        "live", "sound",
        max_abs_operand=max_op, threshold=POW997,
        decades_below=float(np.log10(POW997 / max_op)),
        note="the overflow band sits this many decades above the largest live operand.")

    # ======================================================================
    # CTRL -- the honest certificate, both directions (leg 98's controls, re-run)
    # ======================================================================
    c_ok = interval_constants(ivc, z, w, nu)
    v_ok = radii_verdict(c_ok["Y0"], c_ok["Z1"], c_ok["Z2"])
    rec("CTRL01_honest_closes", "CTRL", "interval_certificate (end to end)", "live",
        "sound" if v_ok["closes"] else "silent_wrong",
        Y0=c_ok["Y0"], Z1=c_ok["Z1"], Z2=c_ok["Z2"], closes=bool(v_ok["closes"]),
        r_min=v_ok["r_min"], r_max=v_ok["r_max"],
        note="POSITIVE control: the module still works. Every number in this battery is "
             "produced by a module that certifies this correctly.")

    c_bad = interval_constants(ivc, z + 1e-3, w, nu)
    v_bad = radii_verdict(c_bad["Y0"], c_bad["Z1"], c_bad["Z2"])
    rec("CTRL02_displaced_does_not_close", "CTRL", "interval_certificate (end to end)",
        "live", "sound" if not v_bad["closes"] else "silent_wrong",
        Y0=c_bad["Y0"], Z1=c_bad["Z1"], Z2=c_bad["Z2"], closes=bool(v_bad["closes"]),
        separation=c_bad["Y0"] / c_ok["Y0"],
        note="NEGATIVE control: displaced by 1e-3, it does not close. Separation quoted.")

    # ======================================================================
    totals = {
        "cases": len(cases),
        "silent_wrong": sum(1 for c in cases if c["outcome"] == "silent_wrong"),
        "sound": sum(1 for c in cases if c["outcome"] == "sound"),
        "raised": sum(1 for c in cases if c["outcome"] == "raised"),
    }
    sw = [c["case"] for c in cases if c["outcome"] == "silent_wrong"]
    worst_rel = max((c.get("escape_relative", 0.0) for c in cases
                     if c["outcome"] == "silent_wrong"), default=0.0)
    worst_abs = max((c.get("escape_eta", 0.0) for c in cases
                     if c["outcome"] == "silent_wrong"), default=0.0)
    y0_rows = [c for c in cases if c["case"].startswith("SUB05")]

    out = {
        "leg": 201, "route": "ICA2",
        "question": ("Under adversarial and degenerate inputs -- including inputs near "
                     "interval.py's own known failure bands (subnormal range, above "
                     "2^997), even though no live operator's range reaches them -- does "
                     "interval_certificate.py ever silently return a wrong value?"),
        "answer": "YES" if totals["silent_wrong"] else "NO",
        "substrate": {"live": f"BorderedCLM n={N_GRID}, N={b.N}, theta={list(THETA)}",
                      "synthetic": "SubnormalToy, identity Jacobian, m in "
                                   f"{list(LIVE_M)} (the shipped N values)"},
        "totals": totals,
        "silent_wrong_cases": sw,
        "headline": {
            "routine": "solver.interval_certificate.matmul_point_interval",
            "mechanism": ("the m-term accumulation error bound is purely RELATIVE "
                          "(gamma_m * sum|M_ij v_j|); it underflows to exactly 0 once the "
                          "products are subnormal, leaving only the 1-ulp outward push "
                          "against an accumulation error of up to m/2 eta"),
            "traces_to": ("the SAME mechanism as leg 69's defect 1 in solver/interval.py, "
                          "but an INDEPENDENT UNREPAIRED INSTANCE: leg 69 added the eta "
                          "term to interval.isum / matvec / dot2_matvec and this module's "
                          "own clone of matvec never received it"),
            "worst_escape_eta": worst_abs,
            "worst_escape_relative": worst_rel,
            "Y0_understated_percent": max((r.get("understated_percent", 0.0)
                                           for r in y0_rows), default=0.0),
            "reachable_from_live_operator": False,
        },
        "cases": cases,
    }
    if write:
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=2, sort_keys=False, default=float)
    if verbose:
        print("\n" + "=" * 74)
        print(f"cases {totals['cases']}   silent_wrong {totals['silent_wrong']}   "
              f"sound {totals['sound']}   raised {totals['raised']}")
        print(f"worst containment escape : {worst_abs:.1f} eta "
              f"= {worst_rel * 100:.2f}% of the returned magnitude")
        for r in y0_rows:
            print(f"Y_0 at m={r['m']}: returned {r['Y0_returned']:.6e} vs exact "
                  f"{r['Y0_exact']:.6e}  ({r['understated_percent']:.2f}% too small)")
        print(f"GATE: {out['answer']}")
        print("=" * 74)
    return out


if __name__ == "__main__":
    run()
