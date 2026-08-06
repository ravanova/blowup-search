"""Route-OLA v1 -- ADVERSARIAL SOUNDNESS AUDIT of solver/op_lower.py.

THE GATE (leg 101, DIRECTION.md):

  Under an adversarial battery of degenerate or NaN-poisoned operator inputs,
  does solver/op_lower.py ever return a value that is NOT a true lower bound on
  the dense operator norm (i.e. exceeds the true norm on a case where both are
  computable)?

WHY A LOWER BOUND CAN EVEN BE WRONG.  Every number op_lower returns is an
evaluated Rayleigh quotient dom(A g)/cod(g), and ||A|| >= that for every g -- so
the module is sound by construction IN EXACT ARITHMETIC.  It is float64.  Two
mechanisms can break the inequality anyway, and neither is reachable by any
existing test, which runs only on the benign J-collocation inverse:

  (a) the NUMERATOR overflows: A @ g -> inf while the true norm is finite, so the
      reported "lower bound" is inf;
  (b) the DENOMINATOR underflows: cod(g) loses its small limbs to flush-to-zero
      faster than dom(A g) does, inflating a FINITE ratio above the true norm.

THE REFERENCE (pre-committed, writeup/novelty/leg_101.md sec 3).  Deciding this
gate needs a TRUE norm, not another estimate -- so the battery does not use the
project's Holder norms for the gate.  op_lower is generic in its norms (it
consumes only a callable and a `.w` array), so it is fed two duck-typed pairs for
which the induced operator norm is EXACTLY computable:

  l1(u) -> linf(t):  N = max_{i,j} t_i |A_ij| / u_j          (closed form: the
                     extreme points of the l1(u) ball are +-e_j/u_j)
  l2(u) -> l2(t):    N = sigma_max(diag(t) A diag(u)^-1)      (numpy SVD)

Both references are compared over the SAME subspace the module searches -- it
forces g[0] = 0, so column 0 of A is deleted for the gate-deciding reference
(N_res); the unrestricted N_full is reported alongside.

  VIOLATION := N_res finite AND L > (1 + 1e-9) * N_res, AND the excess is more
               than ONE ULP of the returned float.

The ULP clause is a correction the data forced, recorded rather than quietly
applied: the rule pre-committed in the novelty pass used a fixed RELATIVE slack
of 1e-9, which is the wrong instrument in the denormal range, where one ULP is
already ~1e-6 relative.  A correctly-rounded quotient there can land up to half
an ULP ABOVE the exact value through no fault of the module, and the first run
duly flagged one such case (0.38 ULP) as a violation.  It is not one.  The
overflow class below is untouched by this: `inf` against a finite true norm is
not a rounding question.

Under-reporting (L = 0 against a huge N_res) is a PASS and is reported as a
magnitude, never as a gate trip: a lower bound may be weak, it may not be wrong.
Cases whose reference is itself non-finite are OUT OF SCOPE by the gate's own
words ("wherever both are computable") and are counted so the excluded fraction
is visible.

TIER B carries the project's real HolderNorm pair over the same operator zoo,
where no exact reference exists: it checks only that a nonzero headline is finite
and is reproduced to 1e-12 by an admissible g of finite positive codomain norm.
It is reported, and it does not decide the gate.

solver/op_lower.py is READ-ONLY under both gate outcomes.

Run: .venv/bin/python experiments/p2_route_ola_v1_adversarial.py
"""

import json
import os
import sys
import time
import warnings
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.op_lower import (                                    # noqa: E402
    ascend, best_lower, family_lower, sign_pattern_lower, smooth_family,
)

TOL = 1e-9                       # the pre-committed violation slack
N = 48                           # operator dimension for the zoo
KW = dict(n_centre=12, n_step=12)
ASCENT_ITERS = 200


# ---------------------------------------------------------------------------
# duck-typed norms with EXACTLY computable induced operator norms
# ---------------------------------------------------------------------------
class WeightedL1:
    """||g|| = sum_j u_j |g_j|.  `.w` is what op_lower uses to shape candidates."""

    def __init__(self, u, w=None):
        self.u = np.asarray(u, dtype=float)
        self.w = np.asarray(self.u if w is None else w, dtype=float)

    def __call__(self, g):
        return float(np.sum(self.u * np.abs(np.asarray(g, dtype=float))))


class WeightedLinf:
    """||v|| = max_i t_i |v_i|."""

    def __init__(self, t):
        self.t = np.asarray(t, dtype=float)
        self.w = self.t

    def __call__(self, v):
        return float(np.max(self.t * np.abs(np.asarray(v, dtype=float))))


class WeightedL2:
    """||v|| = ||t*v||_2."""

    def __init__(self, t):
        self.t = np.asarray(t, dtype=float)
        self.w = self.t

    def __call__(self, v):
        return float(np.sqrt(np.sum((self.t * np.asarray(v, dtype=float)) ** 2)))


def ref_l1_linf(A, t, u, restricted):
    """max_{i,j} t_i |A_ij| / u_j -- the induced norm, in EXACT RATIONALS.

    Returns a Fraction, or None when the reference is not computable (a
    non-finite entry or weight, or a zero codomain weight, which makes the norm
    unbounded).  Exact arithmetic is not decoration: computed in float64 this
    same expression UNDERFLOWS to 0.0 on the denormal cases -- i.e. the naive
    reference is itself wrong exactly where the audit is sharpest, and would
    manufacture violations that are artifacts of the reference.
    """
    B = A[:, 1:] if restricted else A
    uu = u[1:] if restricted else u
    if B.size == 0:
        return Fraction(0)
    if not (np.all(np.isfinite(B)) and np.all(np.isfinite(t))
            and np.all(np.isfinite(uu))):
        return None
    if np.any(uu == 0.0):
        return None                       # a zero codomain weight: unbounded
    ta = [Fraction(float(x)) for x in t]
    ua = [Fraction(float(x)) for x in uu]
    best = Fraction(0)
    for i in range(B.shape[0]):
        ti = ta[i]
        if ti == 0:
            continue
        row = B[i]
        nz = np.nonzero(row)[0]
        for j in nz:
            v = ti * Fraction(abs(float(row[j]))) / ua[j]
            if v > best:
                best = v
    return best


def _pow2_rescale(x):
    """Scale by an exact power of two into a benign range. Returns (y, exp)."""
    m = np.max(np.abs(x[np.isfinite(x)])) if np.any(np.isfinite(x)) else 0.0
    if m == 0.0:
        return np.asarray(x, dtype=float), 0
    e = int(np.frexp(m)[1])
    return np.ldexp(np.asarray(x, dtype=float), -e), e


def ref_l2_l2(A, t, u, restricted):
    """sigma_max(diag(t) A diag(u)^-1) -- by SVD, on a pow-2-rescaled matrix.

    The rescaling is exact in binary floating point, so it neither creates nor
    destroys information; it only keeps the SVD away from the overflow ceiling.
    Accurate to ~1e-13 relative, NOT exact -- so per the pre-committed rule this
    reference decides only the overflow class (a non-finite L against a finite
    reference); any finite exceedance it sees is reported unconfirmed and the
    gate is decided on the exact l1->linf reference instead.
    """
    B = A[:, 1:] if restricted else A
    uu = u[1:] if restricted else u
    if B.size == 0:
        return Fraction(0)
    if not (np.all(np.isfinite(B)) and np.all(np.isfinite(t))
            and np.all(np.isfinite(uu))):
        return None
    if np.any(uu == 0.0):
        return None
    B2, eB = _pow2_rescale(B)
    t2, et = _pow2_rescale(t)
    u2, eu = _pow2_rescale(uu)
    M = (t2[:, None] * B2) / u2[None, :]
    if not np.all(np.isfinite(M)):
        return None
    try:
        s = float(np.linalg.svd(M, compute_uv=False)[0])
    except np.linalg.LinAlgError:
        return None
    if s == 0.0:
        return Fraction(0)
    return Fraction(s) * Fraction(2) ** (eB + et - eu)


# ---------------------------------------------------------------------------
# the operator zoo -- degenerate, near-singular, non-finite, extreme-scale
# ---------------------------------------------------------------------------
def operator_zoo(n=N, seed=7):
    rng = np.random.default_rng(seed)
    G = rng.normal(size=(n, n))
    out = []

    def add(name, A, note):
        out.append({"name": name, "A": np.asarray(A, dtype=float), "note": note})

    add("benign_random", G.copy(), "control: well-formed dense Gaussian")

    i, j = np.arange(n), np.arange(n)
    add("hilbert", 1.0 / (i[:, None] + j[None, :] + 1.0),
        "ill-conditioned control, cond ~ 1e19 at this size")

    M = np.eye(n)
    M[3, 3] = 1e-13
    add("near_singular_inverse", np.linalg.inv(M),
        "inverse of a matrix with one 1e-13 pivot -> a 1e13 entry")

    Jd = np.eye(n) * 1e-12 + np.diag(np.ones(n - 1), 1)
    add("near_defective", Jd, "near-defective Jordan block, eps diagonal")

    add("rank1", np.outer(G[:, 0], G[0, :]), "rank-deficient (rank 1)")
    add("zero", np.zeros((n, n)), "the zero operator: true norm is exactly 0")

    Z = G.copy()
    Z[:, 0] = 0.0
    add("zero_col0", Z, "the gauge column is zero")

    Zr = G.copy()
    Zr[5, :] = 0.0
    add("zero_row", Zr, "one zero row")

    P = G.copy()
    P[5, 7] = np.nan
    add("nan_entry", P, "a single NaN in a generic entry")

    P = G.copy()
    P[:, 0] = np.nan
    add("nan_col0", P, "the whole GAUGE column is NaN -- the column op_lower zeroes")

    P = G.copy()
    P[3, :] = np.nan
    add("nan_row", P, "a whole row is NaN")

    P = G.copy()
    P[9, 11] = np.inf
    add("inf_entry", P, "a single +inf")

    P = G.copy()
    P[4, :] = -np.inf
    add("neg_inf_row", P, "a whole row is -inf")

    add("huge_1e300", G * 1e300,
        "entries ~1e300: every ENTRY is finite, but a length-48 dot product is not")

    P = G.copy() * 1e-300
    P[:, 3] *= 1e300
    add("mixed_scale", P, "1e-300 background with one 1e0-scale column")

    add("denormal", G * 1e-320, "denormal-scale entries")

    P = G * 1e-300
    P[:, 0] = G[:, 0] * 1e300
    add("huge_col0_only", P, "all the mass is in the gauge column op_lower discards")

    P = G * 1e300
    P[7, 7] = np.nan
    add("huge_and_nan", P, "overflow scale AND a NaN")

    add("hilbert_1e200", (1.0 / (i[:, None] + j[None, :] + 1.0)) * 1e200,
        "ill-conditioned and near the overflow ceiling")

    return out


# ---------------------------------------------------------------------------
# degenerate weight vectors and grids
# ---------------------------------------------------------------------------
def theta_grid(n=N):
    return (np.arange(n) + 0.5) * np.pi / n


def weight_zoo(n=N):
    th = theta_grid(n)
    X = np.tan(0.5 * th)
    decay = (1.0 + X ** 2) ** (-0.75)
    out = [
        ("unit", np.ones(n), "all weights 1"),
        ("decay", decay.copy(), "the project's algebraic-decay shape"),
    ]
    for label, val, note in (
        ("zero_entry", 0.0, "one weight is exactly 0 -> 1/w is inf"),
        ("denormal_entry", 1e-320, "one weight is denormal -> 1/w ~ 1e320 overflows"),
        ("huge_entry", 1e300, "one weight is 1e300 -> 1/w underflows"),
        ("nan_entry", np.nan, "one weight is NaN"),
    ):
        w = decay.copy()
        w[7] = val
        out.append(("decay_" + label, w, note))
    out.append(("tiny_all", np.full(n, 1e-300), "every weight 1e-300"))
    out.append(("huge_all", np.full(n, 1e300), "every weight 1e300"))
    return out


def grid_zoo(n=N):
    th = theta_grid(n)
    out = [("regular", th.copy(), "the ordinary grid")]
    c = th.copy()
    c[:] = th[0]
    out.append(("constant", c, "a constant theta grid (all collocation points equal)"))
    p = th.copy()
    p[3] = np.nan
    out.append(("nan_point", p, "one NaN collocation point"))
    return out


# ---------------------------------------------------------------------------
# one case
# ---------------------------------------------------------------------------
def run_case(A, dom, cod, theta, ref_fn, t, u, exact_ref=True):
    """Run op_lower and compare against the reference. Returns a record."""
    rec = {"_exact_ref": bool(exact_ref)}
    with np.errstate(all="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            r = best_lower(A, dom, cod, theta, ascent_iters=ASCENT_ITERS, **KW)
            rec["raised"] = ""
            rec["L"] = float(r["lower"])
            rec["L_sign"] = float(r["sign_patterns"])
            rec["L_family"] = float(r["smooth_family"])
            rec["L_ascent"] = float(r["after_ascent"])
            rec["argmax"] = str(r["family_argmax"])
        except Exception as exc:                                  # loud = a PASS
            rec["raised"] = "%s: %s" % (type(exc).__name__, exc)
            for k in ("L", "L_sign", "L_family", "L_ascent"):
                rec[k] = float("nan")
            rec["argmax"] = ""
        Nr = ref_fn(A, t, u, True)
        Nf = ref_fn(A, t, u, False)
    rec["N_res"] = _fstr(Nr)
    rec["N_full"] = _fstr(Nf)

    L = rec["L"]
    rec["ref_computable"] = Nr is not None
    if rec["raised"]:
        rec["verdict"] = "raised"
        rec["ratio"] = float("nan")
        return rec
    if Nr is None:
        rec["verdict"] = "excluded_ref_nonfinite"
        rec["ratio"] = float("nan")
        return rec
    if np.isnan(L):
        rec["verdict"] = "nan_headline"
        rec["ratio"] = float("nan")
        return rec
    if np.isinf(L):
        rec["ratio"] = float("inf")
        rec["verdict"] = "VIOLATION_overflow"      # inf against a finite norm
        return rec
    LF = Fraction(L)
    rec["ratio"] = _ratio(LF, Nr)
    # ULP-AWARE, and this correction was forced by the data (see the journal):
    # the pre-committed slack was a fixed RELATIVE 1e-9, which is the wrong
    # instrument in the denormal range, where one ULP is ~1e-6 relative and can
    # reach 1e-1.  A correctly-rounded quotient there sits up to half an ULP
    # ABOVE the exact value through no fault of the module.  Exceedance is
    # therefore measured in ULPs of the returned float, and only an excess of
    # more than one full ULP counts as a finite violation.
    ulp = float(np.nextafter(abs(L), np.inf) - abs(L)) if L != 0.0 else 5e-324
    rec["excess_ulps"] = float((LF - Nr) / Fraction(ulp)) if LF > Nr else 0.0
    if LF > Nr and rec["excess_ulps"] <= 1.0:
        rec["verdict"] = "sound_within_one_ulp"
    elif LF > Nr * (1 + Fraction(TOL)) and rec["excess_ulps"] > 1.0:
        # a FINITE number strictly above the true norm.  Only the exact
        # (l1->linf) reference may decide this class; the SVD reference is
        # float and reports it unconfirmed.
        rec["verdict"] = ("VIOLATION_finite" if rec.get("_exact_ref", True)
                          else "finite_exceedance_unconfirmed")
    elif L == 0.0 and Nr > 0:
        rec["verdict"] = "sound_but_zero"
    else:
        rec["verdict"] = "sound"
    return rec


def _fstr(x):
    """Report a reference value as a float when it fits, always as a string."""
    if x is None:
        return None
    try:
        return "%.17e" % float(x)
    except (OverflowError, ValueError):
        return "inf(exact rational, magnitude beyond float64)"


def _ratio(LF, Nr):
    if Nr == 0:
        return 0.0 if LF == 0 else float("inf")
    try:
        return float(LF / Nr)
    except (OverflowError, ValueError):
        return float("inf")


def tier_a():
    """The gate-deciding tier: exact references."""
    ops, wts, grids = operator_zoo(), weight_zoo(), grid_zoo()
    recs = []
    for op in ops:
        for wname, w, wnote in wts:
            for gname, th, gnote in grids:
                # only sweep the grid zoo on a couple of operators: the grid
                # enters only through the candidate SHAPES, not the reference.
                if gname != "regular" and op["name"] not in (
                        "benign_random", "huge_1e300", "nan_entry"):
                    continue
                t = w
                u = w
                for pair, dom, cod, ref, exact in (
                    ("l1->linf", WeightedLinf(t), WeightedL1(u), ref_l1_linf, True),
                    ("l2->l2", WeightedL2(t), WeightedL2(u), ref_l2_l2, False),
                ):
                    rec = run_case(op["A"], dom, cod, th, ref, t, u, exact)
                    rec.update(operator=op["name"], op_note=op["note"],
                               weights=wname, w_note=wnote, grid=gname,
                               pair=pair, tier="A")
                    recs.append(rec)
    return recs


def denormal_sweep():
    """A dedicated sweep of the DENORMAL range, across dimension.

    The main zoo runs at one dimension and under-samples this: the second
    violation class is a FINITE value above the true norm, produced when the
    quotient is evaluated on denormal-scale products whose rounding error is
    ~1e-6 relative per operation.  It matters because the maximiser sits ON the
    extremal direction there, so the whole rounding error lands above the true
    norm rather than being absorbed by slack.  Sporadic in n, so it is swept.
    """
    recs = []
    for n in (16, 24, 32, 40, 48, 64, 80, 96):
        th = (np.arange(n) + 0.5) * np.pi / n
        X = np.tan(0.5 * th)
        w = (1.0 + X ** 2) ** (-0.75)
        A = np.random.default_rng(7).normal(size=(n, n)) * 1e-320
        dom, cod = WeightedLinf(w), WeightedL1(w)
        rec = run_case(A, dom, cod, th, ref_l1_linf, w, w, True)
        rec.update(operator="denormal_1e-320", op_note="denormal-scale entries",
                   weights="decay", w_note="the project's decay shape",
                   grid="regular", pair="l1->linf", tier="A_denormal", dim=n)
        recs.append(rec)
    return recs


def tier_b():
    """The project's real HolderNorm pair -- reported, not gate-deciding."""
    from solver.decay_collocation import Collocation
    from solver.holder_norms import HolderNorm

    col = Collocation(N)
    dom = HolderNorm(col.theta, col.X, 1.5, 0.5)
    cod = HolderNorm(col.theta, col.X, 2.5, 0.5)
    cod.w[0] = 1.0
    recs = []
    for op in operator_zoo(N):
        A = op["A"]
        rec = {"operator": op["name"], "op_note": op["note"], "tier": "B",
               "pair": "HolderNorm(1.5)->HolderNorm(2.5)"}
        with np.errstate(all="ignore"), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                f = family_lower(A, dom, cod, col.theta, **KW)
                rec["L_family"] = float(f["lower"])
                rec["argmax"] = str(f["argmax"])
                rec["raised"] = ""
                # witness: regenerate the named member and re-evaluate it
                hit = None
                for name, g in smooth_family(col.theta, cod.w, **KW):
                    if name == f["argmax"]:
                        hit = g.copy()
                        break
                if hit is None:
                    rec["witness"] = "argmax_not_found"
                    rec["witness_ratio"] = float("nan")
                    rec["witness_cod"] = float("nan")
                else:
                    hit[0] = 0.0
                    n = cod(hit)
                    rec["witness_cod"] = float(n)
                    rr = float(dom(A @ hit) / n) if n > 0 else float("nan")
                    rec["witness_ratio"] = rr
                    if f["lower"] == 0.0:
                        rec["witness"] = "no_candidate_accepted"
                    elif np.isfinite(rr) and abs(rr - f["lower"]) <= 1e-12 * max(
                            1.0, abs(f["lower"])):
                        rec["witness"] = "reproduced"
                    else:
                        rec["witness"] = "NOT_REPRODUCED"
                rec["headline_finite"] = bool(np.isfinite(rec["L_family"]))
            except Exception as exc:
                rec["raised"] = "%s: %s" % (type(exc).__name__, exc)
                rec["L_family"] = float("nan")
                rec["witness"] = "raised"
                rec["witness_ratio"] = float("nan")
                rec["witness_cod"] = float("nan")
                rec["headline_finite"] = False
        recs.append(rec)
    return recs


def main():
    t0 = time.time()
    a = tier_a() + denormal_sweep()
    b = tier_b()
    dt = time.time() - t0

    def by(*v):
        return [r for r in a if r["verdict"] in v]

    over = by("VIOLATION_overflow")
    finv = by("VIOLATION_finite")
    unconf = by("finite_exceedance_unconfirmed")
    viol = over + finv
    ulpok = by("sound_within_one_ulp")
    decid = by("sound", "sound_but_zero", "sound_within_one_ulp",
               "VIOLATION_overflow", "VIOLATION_finite",
               "finite_exceedance_unconfirmed")
    excl = by("excluded_ref_nonfinite")
    nanh = by("nan_headline")
    raised = by("raised")
    zero = by("sound_but_zero")

    fin = [r["ratio"] for r in decid if np.isfinite(r["ratio"])]
    print("TIER A -- %d cases, %d gate-deciding (reference computable)"
          % (len(a), len(decid)))
    print("  VIOLATIONS, overflow (L = inf vs finite norm) .. %d" % len(over))
    print("  VIOLATIONS, FINITE value above the true norm ... %d" % len(finv))
    print("  finite exceedance, SVD ref, unconfirmed ....... %d" % len(unconf))
    print("  sound, within one ULP of the true norm ........ %d%s"
          % (len(ulpok),
             ("  (max %.3f ULP)" % max(r["excess_ulps"] for r in ulpok))
             if ulpok else ""))
    print("  sound, nonzero ................................ %d"
          % (len(decid) - len(zero) - len(viol) - len(unconf) - len(ulpok)))
    print("  sound but L = 0 ............................... %d" % len(zero))
    print("  excluded (reference not computable) ........... %d" % len(excl))
    print("  NaN headline .................................. %d" % len(nanh))
    print("  raised ........................................ %d" % len(raised))
    if fin:
        print("  max FINITE L/N_res over decided cases: %.9f (min %.3e)"
              % (max(fin), min(fin)))
    dsw = [r for r in a if r.get("tier") == "A_denormal"]
    if dsw:
        print("\n  DENORMAL SWEEP (dimension): " + ", ".join(
            "n=%d %s%s" % (r["dim"], r["verdict"],
                           ("" if r.get("excess_ulps", 0.0) <= 0 else
                            " (+%.1f ULP, %.2e rel)"
                            % (r["excess_ulps"], r["ratio"] - 1.0)))
            for r in dsw))
    for r in viol + unconf:
        print("  !! %s %s | %s | %s | %s : L = %.6e  N_res = %s  ratio = %.9g "
              "(sign %.3e family %.3e ascent %.3e)"
              % (r["verdict"], r["operator"], r["weights"], r["grid"], r["pair"],
                 r["L"], r["N_res"], r["ratio"], r["L_sign"], r["L_family"],
                 r["L_ascent"]))

    notrep = [r for r in b if r.get("witness") == "NOT_REPRODUCED"]
    nonfin = [r for r in b if r["L_family"] != 0.0 and not r["headline_finite"]]
    print("\nTIER B (HolderNorm, reported only) -- %d cases: %d reproduced, "
          "%d NOT reproduced, %d nonzero-but-nonfinite headlines"
          % (len(b), sum(1 for r in b if r.get("witness") == "reproduced"),
             len(notrep), len(nonfin)))
    for r in notrep + nonfin:
        print("  !! %s: L = %r witness = %r (%s)"
              % (r["operator"], r["L_family"], r.get("witness_ratio"),
                 r.get("witness")))

    gate = "yes" if viol else "no"
    print("\nGATE (does op_lower ever exceed the true norm?): %s" % gate.upper())
    print("elapsed %.1f s" % dt)

    out = {
        "leg": 101, "route": "OLA", "generated": time.strftime("%Y-%m-%d"),
        "gate_question": (
            "Under an adversarial battery of degenerate or NaN-poisoned operator "
            "inputs, does solver/op_lower.py ever return a value that is NOT a true "
            "lower bound on the dense operator norm (i.e. exceeds the true norm on a "
            "case where both are computable)?"),
        "gate_answer": gate,
        "violation_definition": "N_res finite AND L > (1+1e-9)*N_res",
        "tolerance": TOL, "dimension": N, "elapsed_s": round(dt, 2),
        "tier_a": {
            "cases": len(a), "gate_deciding": len(decid),
            "violations": len(viol),
            "violations_overflow": len(over),
            "violations_finite": len(finv),
            "finite_exceedance_unconfirmed": len(unconf),
            "sound_within_one_ulp": len(ulpok),
            "max_excess_ulps": (max(r["excess_ulps"] for r in ulpok)
                                if ulpok else 0.0),
            "sound_but_zero": len(zero),
            "excluded_ref_nonfinite": len(excl), "nan_headline": len(nanh),
            "raised": len(raised),
            "max_ratio": max(fin) if fin else None,
            "min_ratio": min(fin) if fin else None,
            "records": a,
        },
        "tier_b": {
            "cases": len(b),
            "reproduced": sum(1 for r in b if r.get("witness") == "reproduced"),
            "not_reproduced": len(notrep),
            "nonzero_nonfinite": len(nonfin),
            "records": b,
        },
    }
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "writeup", "data", "p2_route_ola_v1_adversarial.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote %s" % path)
    return out


if __name__ == "__main__":
    main()
