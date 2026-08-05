"""Route-IA (leg 69): a size- and conditioning-matched adversarial stress test of
`solver/interval.py`, the interval core BOTH live realizations of L1 stand on.

WHY THIS RUNS.  `solver/interval.py` is shared infrastructure: leg 58's compactified-basis
certificate (`spectral_certificate.py`) and leg 61's known-answer pipeline
(`interval_certificate.py`) both evaluate every rigorous number through its outward-rounded
`Interval` type and, above all, through `dot2_matvec` -- the compensated (Ogita-Rump-Oishi)
matvec whose error bound is RELATIVE TO THE ANSWER rather than to the terms.  `capabilities.py`
records the module as validated because "containment holds on adversarial cases", but the corpus
behind that line is `test_interval.py`'s: its largest matrix is 6x4 and its longest accumulation
is 4 terms.  The certificate stack now runs K up to 128 (leg 57), i.e. accumulations of 129 to
258 terms, against an operator whose tail-block diagonal is exactly zero (legs 51-53) so that the
rows cancel catastrophically.  Neither the SIZE nor the CONDITIONING was ever tested.

WHAT IS MEASURED.  Every case is checked against EXACT RATIONAL ground truth: the inputs are
exact float64 data, so `fractions.Fraction` reproduces the real answer with no error at all, and
the question "does the enclosure contain the real value" is decided exactly, not numerically.
No booleans are reported on their own -- every family reports the worst RELATIVE SLACK

    slack_rel = min(x - lo, hi - x) / (hi - lo)

(the true value's distance to the nearest endpoint, as a fraction of the enclosure width: 0.5 is
dead centre, 0 is touching an endpoint, NEGATIVE IS A FALSE NEGATIVE) and, where a case fails,
the ABSOLUTE ESCAPE |x - nearest endpoint| in units of eta = 2^-1074, the smallest positive
subnormal.  The absolute escape is the number that decides severity, because it says whether the
defect is a relative one (which would scale into the certificate's own regime) or an absolute
one (which cannot).

This file makes NO certification claim and does not modify `solver/interval.py`.
"""

import json
import os
import sys
import warnings
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.interval import (                                          # noqa: E402
    Interval, dot2_matvec, isum, matvec, _two_product,
)

ETA = 2.0 ** -1074          # smallest positive subnormal (Rump's underflow unit)
U = 2.0 ** -53              # unit roundoff

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_ia_v1_interval_stress.json")


# --------------------------------------------------------------------------
# the exact-rational verdict on one scalar enclosure
# --------------------------------------------------------------------------

def _safe_float_repr(x):
    """float() of an exact rational, without letting an out-of-range value abort the run."""
    try:
        return repr(float(x))
    except (OverflowError, ValueError):
        return f"<out of float range: {'+' if x > 0 else '-'}~1e{len(str(abs(x.numerator))) - len(str(x.denominator))}>"


def verdict(lo, hi, exact):
    """Exact-rational verdict for one enclosure [lo, hi] against the real value `exact`.

    Returns (contained, slack_rel, escape_eta).  `escape_eta` is 0.0 when contained and the
    absolute distance outside, in units of eta, when not.

    Non-finite endpoints are decided WITHOUT the rational path and are not silently skipped:
    a NaN endpoint is scored as a false negative with an infinite escape (it is a soundness
    hole, not a wide answer), while an infinite endpoint on the correct side is a VACUOUSLY
    TRUE, infinitely wide enclosure -- contained, but reported with slack_rel = None so that it
    is COUNTED SEPARATELY and can neither flatter nor damage the worst-case slack statistic."""
    if not isinstance(exact, Fr):
        exact = Fr(exact)
    lo_f, hi_f = float(lo), float(hi)
    if np.isnan(lo_f) or np.isnan(hi_f):
        return False, -1.0, float("inf")
    if np.isinf(lo_f) or np.isinf(hi_f):
        ok = ((Fr(lo_f) <= exact) if np.isfinite(lo_f) else lo_f < 0) and \
             ((exact <= Fr(hi_f)) if np.isfinite(hi_f) else hi_f > 0)
        return ok, (None if ok else -1.0), (0.0 if ok else float("inf"))
    L, H = Fr(lo_f), Fr(hi_f)
    w = H - L
    slack = min(exact - L, H - exact)
    contained = slack >= 0
    if w > 0:
        slack_rel = float(slack / w)
    else:
        slack_rel = 0.0 if slack == 0 else float(slack) and -1.0
    escape = 0.0 if contained else float(-slack / Fr(ETA))
    return contained, slack_rel, escape


class Family:
    """Accumulates the verdicts of one adversarial family and reports MAGNITUDES."""

    def __init__(self, name, note):
        self.name = name
        self.note = note
        self.n = 0
        self.n_fail = 0
        self.n_unbounded = 0
        self.n_touching = 0
        self.worst_slack = float("inf")
        self.worst_escape = 0.0
        self.reproducer = None

    def add(self, lo, hi, exact, tag=None):
        c, s, e = verdict(lo, hi, exact)
        self.n += 1
        if s is None:
            self.n_unbounded += 1
        else:
            self.worst_slack = min(self.worst_slack, s)
            if s == 0.0:
                self.n_touching += 1
        if not c:
            self.n_fail += 1
            if e > self.worst_escape:
                self.worst_escape = e
                self.reproducer = {"tag": tag, "lo": repr(float(lo)), "hi": repr(float(hi)),
                                   "exact_float": _safe_float_repr(exact),
                                   "escape_eta": e}
        return c

    def report(self):
        return {"family": self.name, "note": self.note, "cases": self.n,
                "false_negatives": self.n_fail,
                "worst_relative_slack": self.worst_slack,
                "cases_touching_an_endpoint": self.n_touching,
                "cases_with_unbounded_endpoint": self.n_unbounded,
                "worst_absolute_escape_eta": self.worst_escape,
                "reproducer": self.reproducer}


# --------------------------------------------------------------------------
# corpus builders
# --------------------------------------------------------------------------

def cancel_row(M_row, v):
    """Append two exact-float columns that cancel the row's exact dot product.

    Given an exact-float row and vector, the exact dot product S is a rational.  Its
    double-double head/tail (h, l) are exact floats, so appending columns (-h, -l) against
    v-entries 1.0 leaves an exact dot product of S - h - l, which is ~1e-32 RELATIVE to the
    absolute mass.  This manufactures catastrophic cancellation without leaving exact float data,
    which is what makes the Fraction ground truth available at all."""
    S = sum(Fr(M_row[j]) * Fr(v[j]) for j in range(len(v)))
    h = float(S)
    l = float(S - Fr(h))
    return np.array([-h, -l], dtype=float)


def build_cancelled(rng, n_rows, m, scale_M, scale_v):
    M = rng.standard_normal((n_rows, m)) * scale_M
    v = rng.standard_normal(m) * scale_v
    ext = np.array([cancel_row(M[i], v) for i in range(n_rows)])
    M2 = np.concatenate([M, ext], axis=1)
    v2 = np.concatenate([v, [1.0, 1.0]])
    return M2, v2


def exact_matvec(M, v):
    return [sum(Fr(M[i, j]) * Fr(v[j]) for j in range(M.shape[1]))
            for i in range(M.shape[0])]


# --------------------------------------------------------------------------
# FAMILY 1 -- elementary operations on adversarial endpoint pairs
# --------------------------------------------------------------------------

def fam_elementary(rng):
    f = Family("elementary_ops",
               "+, -, *, / and reciprocal on adversarial endpoint pairs spanning 1e-320 to "
               "1e300, including the subnormal boundary; exact-rational check on both endpoints")
    scales = [1e-320, 1e-310, 1e-300, 1e-200, 1e-8, 1.0, 1e8, 1e200, 1e300]
    for sa in scales:
        for sb in scales:
            for _ in range(6):
                a = rng.standard_normal(2) * sa
                b = rng.standard_normal(2) * sb
                A = Interval(min(a), max(a))
                B = Interval(min(b), max(b))
                for op, fn in (("add", lambda x, y: x + y),
                               ("sub", lambda x, y: x - y),
                               ("mul", lambda x, y: x * y)):
                    R = fn(A, B)
                    # the exact range of the op over the two boxes, at the corners
                    fa = [Fr(float(A.lo)), Fr(float(A.hi))]
                    fb = [Fr(float(B.lo)), Fr(float(B.hi))]
                    if op == "add":
                        vals = [x + y for x in fa for y in fb]
                    elif op == "sub":
                        vals = [x - y for x in fa for y in fb]
                    else:
                        vals = [x * y for x in fa for y in fb]
                    for val in vals:
                        f.add(R.lo, R.hi, val, tag=f"{op}|{sa:.0e}|{sb:.0e}")
                if float(B.lo) > 0 or float(B.hi) < 0:
                    R = A / B
                    vals = [x / y for x in fa for y in fb]
                    for val in vals:
                        f.add(R.lo, R.hi, val, tag=f"div|{sa:.0e}|{sb:.0e}")
    return f


# --------------------------------------------------------------------------
# FAMILY 2 -- isum at certificate lengths, with engineered cancellation
# --------------------------------------------------------------------------

def fam_isum(rng):
    f = Family("isum_cancellation",
               "rigorous sum at accumulation lengths 32..258 (the certificate's own K range, "
               "bordered), with the terms driven to ~1e-32 relative cancellation")
    for m in (32, 64, 128, 258):
        for scale in (1e-8, 1.0, 1e8):
            for _ in range(20):
                x = rng.standard_normal(m) * scale
                S = sum(Fr(t) for t in x)
                h = float(S)
                l = float(S - Fr(h))
                xx = np.concatenate([x, [-h, -l]])
                ex = sum(Fr(t) for t in xx)
                r = isum(Interval.point(xx))
                f.add(r.lo, r.hi, ex, tag=f"m={m}|scale={scale:.0e}")
    return f


# --------------------------------------------------------------------------
# FAMILY 3 -- point matvec and box matvec at certificate sizes
# --------------------------------------------------------------------------

def fam_matvec(rng):
    f = Family("matvec_point_and_box",
               "uncompensated matvec at n x m up to 8 x 260, catastrophically cancelled rows; "
               "plus the interval-vector (box) path checked at every box CORNER pair")
    for m in (32, 64, 128, 258):
        for scale in (1e-8, 1.0, 1e8):
            for _ in range(6):
                M, v = build_cancelled(rng, 8, m, 1.0, scale)
                r = matvec(M, Interval.point(v))
                for i, ex in enumerate(exact_matvec(M, v)):
                    f.add(r.lo[i], r.hi[i], ex, tag=f"point|m={m}|scale={scale:.0e}")
    # box path: the enclosure must dominate the exact value at the worst corner of the box
    for m in (32, 128):
        for _ in range(6):
            M = rng.standard_normal((6, m))
            v = rng.standard_normal(m)
            rad = 1e-3 * np.abs(v)
            box = Interval.from_mid_rad(v, rad)
            r = matvec(M, box)
            lo_c = np.where(M >= 0, box.lo[None, :], box.hi[None, :])
            hi_c = np.where(M >= 0, box.hi[None, :], box.lo[None, :])
            for i in range(M.shape[0]):
                exl = sum(Fr(M[i, j]) * Fr(lo_c[i, j]) for j in range(m))
                exh = sum(Fr(M[i, j]) * Fr(hi_c[i, j]) for j in range(m))
                f.add(r.lo[i], r.hi[i], exl, tag=f"box_lo|m={m}")
                f.add(r.lo[i], r.hi[i], exh, tag=f"box_hi|m={m}")
    return f


# --------------------------------------------------------------------------
# FAMILY 4 -- dot2_matvec in the NORMAL range, size- and cancellation-matched
# --------------------------------------------------------------------------

def fam_dot2_normal(rng):
    f = Family("dot2_normal_range",
               "the COMPENSATED matvec both live legs use, at m = 32..260 and input scales "
               "1e-100..1e100, every row driven to ~1e-32 relative cancellation -- this is the "
               "regime the certificate stack actually occupies")
    for m in (32, 64, 128, 258):
        for scale in (1e-100, 1e-8, 1.0, 1e8, 1e100):
            for _ in range(6):
                M, v = build_cancelled(rng, 6, m, 1.0, scale)
                r = dot2_matvec(M, v)
                for i, ex in enumerate(exact_matvec(M, v)):
                    f.add(r.lo[i], r.hi[i], ex, tag=f"m={m}|scale={scale:.0e}")
    return f


# --------------------------------------------------------------------------
# FAMILY 5 -- the TAIL BLOCK's own conditioning: exactly-zero diagonal, O(1) entries
# --------------------------------------------------------------------------

def fam_tail_block(rng):
    """The conditioning legs 51-53 actually hit, taken from the LIVE operator rather than
    imitated: `bordered_linearization(K)` is the matrix leg 58's certificate linearizes, and
    `tail_diagonal` is exactly zero on it -- the rows have no diagonal to dominate them."""
    f = Family("tail_block_conditioning",
               "the LIVE bordered linearization (spectral_certificate.bordered_linearization) "
               "at K = 16, 32, 64, 128, whose tail diagonal is EXACTLY zero, against vectors "
               "chosen to cancel its rows")
    try:
        from solver.spectral_certificate import bordered_linearization
    except Exception as exc:                                    # pragma: no cover
        f.note += f"  [SKIPPED: {exc}]"
        return f
    for K in (16, 32, 64, 128):
        M = np.asarray(bordered_linearization(K), dtype=float)
        n = M.shape[1]
        for _ in range(8):
            v = rng.standard_normal(n)
            ext = np.array([cancel_row(M[i], v) for i in range(M.shape[0])])
            M2 = np.concatenate([M, ext], axis=1)
            v2 = np.concatenate([v, [1.0, 1.0]])
            ex = exact_matvec(M2, v2)
            r2 = dot2_matvec(M2, v2)
            rm = matvec(M2, Interval.point(v2))
            for i in range(M2.shape[0]):
                f.add(r2.lo[i], r2.hi[i], ex[i], tag=f"dot2|K={K}")
                f.add(rm.lo[i], rm.hi[i], ex[i], tag=f"matvec|K={K}")
    return f


# --------------------------------------------------------------------------
# FAMILY 6 -- the SUBNORMAL range: where the ORO bound has no eta term
# --------------------------------------------------------------------------

def fam_subnormal(rng):
    f = Family("dot2_subnormal_range",
               "the compensated matvec at input scales 1e-120..1e-185, i.e. products straddling "
               "the normal/subnormal boundary (min normal 2.2e-308, eta = 4.9e-324); the ORO "
               "bound u|x.y| + gamma^2 |x||y| is purely RELATIVE and carries no absolute eta term")
    onset = {}
    for e in range(-120, -190, -5):
        scale = 10.0 ** e
        fails = 0
        total = 0
        for _ in range(30):
            M, v = build_cancelled(rng, 2, 64, scale, scale)
            r = dot2_matvec(M, v)
            for i, ex in enumerate(exact_matvec(M, v)):
                ok = f.add(r.lo[i], r.hi[i], ex, tag=f"scale=1e{e}")
                total += 1
                fails += (not ok)
        onset[f"1e{e}"] = {"cases": total, "false_negatives": fails}
    rep = f.report()
    rep["scale_scan"] = onset
    f.report = lambda rep=rep: rep
    return f


def fam_subnormal_matvec(rng):
    f = Family("matvec_subnormal_range",
               "the UNCOMPENSATED matvec over the same subnormal band, to separate which of the "
               "two reductions carries the defect")
    for e in range(-120, -190, -5):
        scale = 10.0 ** e
        for _ in range(30):
            M, v = build_cancelled(rng, 2, 64, scale, scale)
            r = matvec(M, Interval.point(v))
            for i, ex in enumerate(exact_matvec(M, v)):
                f.add(r.lo[i], r.hi[i], ex, tag=f"scale=1e{e}")
    return f


# --------------------------------------------------------------------------
# FAMILY 7 -- Dekker's splitting under overflow (a SEPARATE, non-containment defect)
# --------------------------------------------------------------------------

def probe_dekker_overflow():
    """Dekker's splitting constant 2^27+1 overflows for large operands; find the exact exponent
    at which `_two_product` stops returning a finite error term, and record what dot2_matvec
    then returns.  This is not a containment miss -- it is a SILENT NaN."""
    thresh = None
    for e in range(0, 1024):
        p, err = _two_product(np.array([2.0 ** e]), np.array([1.0]))
        if not np.isfinite(err[0]):
            thresh = e
            break
    M = np.array([[2.0 ** thresh]])
    v = np.array([1.0])
    r = dot2_matvec(M, v)
    return {"probe": "dekker_split_overflow",
            "note": ("_two_product's Dekker splitting multiplies by 2^27+1 before splitting, so "
                     "it overflows for |a| >= 2^e_crit and returns a NaN error term; "
                     "dot2_matvec then returns a NaN enclosure and RAISES NOTHING, because the "
                     "Interval constructor's lo <= hi guard is vacuous on NaN"),
            "e_crit": thresh,
            "magnitude_crit": 2.0 ** thresh,
            "enclosure_at_crit_lo": repr(float(r.lo[0])),
            "enclosure_at_crit_hi": repr(float(r.hi[0])),
            "silent": bool(np.isnan(r.lo[0]) and np.isnan(r.hi[0]))}


def probe_live_dynamic_range():
    """How far is the live certificate stack from the failure band?  Measure the actual entry
    magnitudes of the operators legs 58 and 61 feed to dot2_matvec."""
    out = {}
    try:
        from solver.spectral_certificate import bordered_linearization
        for K in (16, 32, 64, 128):
            A = np.abs(np.asarray(bordered_linearization(K), dtype=float))
            nz = A[A > 0]
            out[f"bordered_linearization_K{K}"] = {
                "shape": list(np.shape(A)),
                "min_nonzero_abs": float(nz.min()),
                "max_abs": float(nz.max()),
                "exact_zero_entries": int((A == 0).sum())}
    except Exception as exc:                                    # pragma: no cover
        out["error"] = str(exc)
    return out


# --------------------------------------------------------------------------

def main():
    warnings.simplefilter("ignore")
    rng = np.random.default_rng(20260805)
    fams = [
        fam_elementary(rng),
        fam_isum(rng),
        fam_matvec(rng),
        fam_dot2_normal(rng),
        fam_tail_block(rng),
        fam_subnormal(rng),
        fam_subnormal_matvec(rng),
    ]
    reports = [f.report() for f in fams]

    normal = [r for r in reports if "subnormal" not in r["family"]]
    subn = [r for r in reports if "subnormal" in r["family"]]

    total = sum(r["cases"] for r in reports)
    fails = sum(r["false_negatives"] for r in reports)
    n_total = sum(r["cases"] for r in normal)
    n_fails = sum(r["false_negatives"] for r in normal)
    n_worst = min(r["worst_relative_slack"] for r in normal)
    n_touch = sum(r["cases_touching_an_endpoint"] for r in normal)
    n_unb = sum(r["cases_with_unbounded_endpoint"] for r in normal)

    result = {
        "leg": 69,
        "route": "IA",
        "module_under_test": "solver/interval.py",
        "ground_truth": "exact rational (fractions.Fraction) on exact float64 inputs",
        "eta": ETA,
        "unit_roundoff": U,
        "families": reports,
        "dekker_overflow_probe": probe_dekker_overflow(),
        "live_operator_dynamic_range": probe_live_dynamic_range(),
        "totals": {
            "cases": total,
            "false_negatives": fails,
            "normal_range_cases": n_total,
            "normal_range_false_negatives": n_fails,
            "normal_range_worst_relative_slack": n_worst,
            "normal_range_cases_touching_an_endpoint": n_touch,
            "normal_range_cases_with_unbounded_endpoint": n_unb,
            "subnormal_range_cases": sum(r["cases"] for r in subn),
            "subnormal_range_false_negatives": sum(r["false_negatives"] for r in subn),
            "subnormal_range_worst_escape_eta": max(
                r["worst_absolute_escape_eta"] for r in subn),
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)

    print(f"wrote {OUT}")
    for r in reports:
        print(f"  {r['family']:26s} cases={r['cases']:6d} "
              f"false_neg={r['false_negatives']:5d} "
              f"worst_rel_slack={r['worst_relative_slack']:+.4e} "
              f"touching={r['cases_touching_an_endpoint']:5d} "
              f"unbounded={r['cases_with_unbounded_endpoint']:4d} "
              f"worst_escape={r['worst_absolute_escape_eta']:.3g} eta")
    t = result["totals"]
    print(f"\n  NORMAL RANGE : {t['normal_range_cases']} cases, "
          f"{t['normal_range_false_negatives']} false negatives, "
          f"worst relative slack {t['normal_range_worst_relative_slack']:+.4e}, "
          f"{t['normal_range_cases_touching_an_endpoint']} touching, "
          f"{t['normal_range_cases_with_unbounded_endpoint']} unbounded-endpoint")
    print(f"  SUBNORMAL    : {t['subnormal_range_cases']} cases, "
          f"{t['subnormal_range_false_negatives']} false negatives, "
          f"worst absolute escape {t['subnormal_range_worst_escape_eta']:.3g} eta "
          f"({t['subnormal_range_worst_escape_eta'] * ETA:.3g} absolute)")
    d = result["dekker_overflow_probe"]
    print(f"  DEKKER SPLIT : finite error term lost at |a| >= 2^{d['e_crit']} "
          f"= {d['magnitude_crit']:.3g}; silent NaN enclosure = {d['silent']}")
    return result


if __name__ == "__main__":
    main()
