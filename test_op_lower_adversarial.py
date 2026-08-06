"""Leg 101 (Route-OLA) -- permanent adversarial gates for solver/op_lower.py.

WHAT THIS FILE PINS.

Leg 101's gate asked whether `solver/op_lower.py` can be made to return a value
ABOVE the true operator norm -- i.e. whether the one property a lower bound must
have can be broken.  It answered **YES**, on **47 of 209** gate-deciding cases, by
two distinct mechanisms:

  (1) OVERFLOW, 46 cases.  `A @ g` overflowed to `inf` while the true norm was
      finite and often perfectly ordinary -- the sharpest case reported `inf` as a
      "lower bound" on an operator whose norm is exactly **1.0e13**.  Two separate
      routes reached it: a small codomain weight (every candidate carries `1/w`,
      so `w = 1e-300` makes the candidate `1e300` and its image `1e313`), and
      `ascend`'s own trial step, sized proportional to the bound found so far, so
      the search overflowed itself on any operator of norm above ~1e154 even with
      unit weights and a finite family value one line earlier.
  (2) FINITE EXCEEDANCE, 1 case.  In the denormal range each product carries
      ~1e-6 relative rounding and the maximiser sits ON the extremal direction, so
      nothing absorbs it: the reported value landed **425.2 ULP (6.04e-04
      relative) above** the exact true norm, as an ordinary-looking finite number.

Leg 101 escalated rather than patched.  The bench repair on
`bench/fix-op-lower-bound-violation` then fixed both at their root -- exact
power-of-two rescaling of `A` and (when its scale needs it) of each candidate,
a rigorous downward deflation, rejection of non-evaluable candidates, and
saturation to `finfo.max` instead of `inf`.  **So checks (1), (2) and (4) are no
longer characterization gates: they assert the violation is GONE, and they carry
the pre-repair number so a reader can see the size of the move.**

  (1) `inf` on a true norm of 1.0e13   ->  1.000000e+13, ratio 0.999999999999
  (2) `inf` on a true norm of 5.0e199  ->  5.000000e+199, ratio 0.999999999999
  (4) +425.2 ULP in the denormal range ->  -0.836 ULP (below, as it must be)

Checks (3), (5), (6), (7) are the regression gates on the properties that DID hold
before the repair and must not rot: NaN poisoning under-reports (exactly 0.0)
rather than inventing a plausible number, everything in the normal float range is
sound, the headline is always attained by an admissible vector, and the production
path keeps a vast margin to the overflow ceiling.  Checks (8), (9), (10) are new
with the repair and pin the three things it added: the rescaling is EXACT, an
out-of-range norm SATURATES rather than returning `inf`, and the production path
moves downward-only by a bounded amount with nothing rejected.

SCOPE, measured (7): no banked Route-D number was ever affected.  On the real
J-collocation operator the largest image the candidate family produces is 2.380,
which is **307.878 decades** below the float64 overflow ceiling, and its entries
are ~1e2, some 300 decades above the denormal range.  The defect was real and it
was reachable only by inputs hundreds of orders of magnitude away from anything
this project feeds the module.

Run: .venv/bin/python test_op_lower_adversarial.py
"""

from fractions import Fraction

import numpy as np

from solver.decay_collocation import Collocation, C_ANCHOR
from solver.holder_norms import HolderNorm
from solver.op_lower import (
    NORM_SLACK, _pow2_normalise, best_lower, family_lower, sign_pattern_lower,
    smooth_family,
)

N = 32
KW = dict(n_centre=8, n_step=8)
REGRESSED = ("  If this fails because op_lower again returns a value ABOVE the "
             "true norm (or `inf`), the leg-101 soundness defect has REGRESSED: "
             "solver/op_lower.py's _Quotient rescale/deflate path is the thing "
             "to look at, and capabilities.py's validated-clause is false again.")


# -- duck-typed norms whose induced operator norm is EXACTLY computable -------
class WeightedL1:
    def __init__(self, u):
        self.u = np.asarray(u, dtype=float)
        self.w = self.u

    def __call__(self, g):
        return float(np.sum(self.u * np.abs(np.asarray(g, dtype=float))))


class WeightedLinf:
    def __init__(self, t):
        self.t = np.asarray(t, dtype=float)
        self.w = self.t

    def __call__(self, v):
        return float(np.max(self.t * np.abs(np.asarray(v, dtype=float))))


def exact_norm(A, t, u, restricted=True):
    """max_{i,j} t_i |A_ij| / u_j in EXACT rationals -- the induced l1(u)->linf(t)
    norm.  In float64 this same expression underflows to 0.0 on denormal input,
    which is why the reference is rational and not a float."""
    B = A[:, 1:] if restricted else A
    uu = u[1:] if restricted else u
    ta = [Fraction(float(x)) for x in t]
    ua = [Fraction(float(x)) for x in uu]
    best = Fraction(0)
    for i in range(B.shape[0]):
        if ta[i] == 0:
            continue
        for j in np.nonzero(B[i])[0]:
            v = ta[i] * Fraction(abs(float(B[i, j]))) / ua[j]
            if v > best:
                best = v
    return best


def theta_grid(n=N):
    return (np.arange(n) + 0.5) * np.pi / n


def decay_weights(n=N):
    X = np.tan(0.5 * theta_grid(n))
    return (1.0 + X ** 2) ** (-0.75)


def _excess_ulps(L, true):
    """How far `L` sits above `true`, in ULPs of `L`.  Negative means below."""
    if L == 0.0:
        return 0.0
    ulp = float(np.nextafter(abs(L), np.inf) - abs(L))
    return float((Fraction(L) - true) / Fraction(ulp))


# ---------------------------------------------------------------------------
def test_1_repaired_near_singular_tiny_weights():
    """THE SHARPEST CASE, REPAIRED: `inf` on a norm of 1.0e13 is now 1.0e13."""
    th = theta_grid()
    M = np.eye(N)
    M[3, 3] = 1e-13
    A = np.linalg.inv(M)                       # one entry of 1e13, else identity
    w = np.full(N, 1e-300)
    dom, cod = WeightedLinf(w), WeightedL1(w)
    with np.errstate(all="ignore"):
        r = best_lower(A, dom, cod, th, ascent_iters=50, **KW)
        s = sign_pattern_lower(A, dom, cod)["lower"]
    true = exact_norm(A, w, w)
    assert float(true) == 1e13, float(true)
    assert np.isfinite(r["lower"]), (r["lower"], REGRESSED)
    assert np.isfinite(s), (s, REGRESSED)
    assert Fraction(r["lower"]) <= true, (r["lower"], float(true), REGRESSED)
    assert Fraction(s) <= true, (s, float(true), REGRESSED)
    # and it is not merely sound -- the sign patterns now ATTAIN the true norm
    assert r["lower"] / float(true) > 1.0 - 1e-9, (r["lower"], float(true))
    print("[ok] (1) REPAIRED: true norm = %.6e, op_lower reports %.6e (sign "
          "patterns %.6e), ratio %.12f -- was `inf` before the repair. The "
          "candidate still carries 1/w = 1e300, but A and g are now normalised "
          "by an exact power of two, so |A g| = 1e313 never forms."
          % (float(true), r["lower"], s, r["lower"] / float(true)))


def test_2_ascent_no_longer_overflows_on_its_own_step():
    """THE SECOND ROUTE, REPAIRED, and it needed no degenerate weight at all.

    `ascend` still sizes its trial step proportional to the bound found so far --
    the step law is deliberately UNCHANGED, because changing which directions the
    search visits would sharpen or blunt the bound, which the repair may not do.
    What changed is that a step that runs out of exponent range now yields a
    REJECTED candidate instead of an `inf` headline.
    """
    th = theta_grid()
    i, j = np.arange(N), np.arange(N)
    A = (1.0 / (i[:, None] + j[None, :] + 1.0)) * 1e200
    w = np.ones(N)
    dom, cod = WeightedLinf(w), WeightedL1(w)
    with np.errstate(all="ignore"):
        f = family_lower(A, dom, cod, th, **KW)
        r = best_lower(A, dom, cod, th, ascent_iters=50, **KW)
    true = exact_norm(A, w, w)
    assert np.isfinite(float(true)), float(true)
    assert np.isfinite(f["lower"]), f["lower"]
    assert np.isfinite(r["after_ascent"]), (r["after_ascent"], REGRESSED)
    assert np.isfinite(r["lower"]), (r["lower"], REGRESSED)
    assert Fraction(r["lower"]) <= true, (r["lower"], float(true), REGRESSED)
    assert Fraction(r["after_ascent"]) <= true, (r["after_ascent"], REGRESSED)
    print("[ok] (2) REPAIRED at the ASCENT, with UNIT weights and all-finite "
          "entries: true norm = %.4e, family = %.4e, after_ascent = %.4e, "
          "headline = %.4e (ratio %.12f) -- headline and after_ascent were both "
          "`inf` before the repair."
          % (float(true), f["lower"], r["after_ascent"], r["lower"],
             r["lower"] / float(true)))


def test_3_nan_and_inf_poisoning_underreports():
    """NaN/Inf poisoning must go the SAFE way: never above the true norm."""
    th = theta_grid()
    rng = np.random.default_rng(7)
    G = rng.normal(size=(N, N))
    w = decay_weights()
    dom, cod = WeightedLinf(w), WeightedL1(w)
    nan_cases, inf_cases = [], []
    for name, A, kind in (
        ("nan_entry", _poke(G, (5, 7), np.nan), "nan"),
        ("nan_gauge_column", _poke(G, (slice(None), 0), np.nan), "nan"),
        ("nan_row", _poke(G, (3, slice(None)), np.nan), "nan"),
        ("inf_entry", _poke(G, (9, 11), np.inf), "inf"),
        ("neg_inf_row", _poke(G, (4, slice(None)), -np.inf), "inf"),
    ):
        with np.errstate(all="ignore"):
            L = best_lower(A, dom, cod, th, ascent_iters=50, **KW)["lower"]
        assert not np.isnan(L), (name, L)
        assert L >= 0.0, (name, L)
        assert np.isfinite(L), (name, L, REGRESSED)      # never `inf` any more
        if kind == "nan":
            # a NaN-poisoned operator has no norm at all: the only safe answer
            # is to under-report, and it does -- exactly 0.0, never a plausible
            # finite number that a caller would believe.
            assert L == 0.0, (name, L)
            nan_cases.append((name, L))
        else:
            # An Inf-poisoned operator has unbounded norm on the FULL space, so
            # `inf` used to be graded correct here.  The repair gives that report
            # up deliberately: the module searches only {g : g_0 = 0}, and when
            # the infinity sits in the gauge column the true norm OVER THAT
            # SUBSPACE is finite, so `inf` would be unsound.  Weak-and-true beats
            # strong-and-sometimes-wrong.
            assert L == 0.0, (name, L)
            inf_cases.append((name, L))
    print("[ok] (3) 3 NaN-poisoned operators report exactly 0.0 (safe "
          "under-report, never NaN, never a plausible finite number); 2 "
          "Inf-poisoned operators now report %s rather than `inf` -- the "
          "repair gives up an `inf` that is unsound whenever the infinity sits "
          "in the gauge column the search excludes. Clean-operator norm for "
          "scale: %.2f"
          % (", ".join("%s=%r" % c for c in inf_cases),
             float(exact_norm(G, w, w))))


def _poke(G, idx, val):
    A = G.copy()
    A[idx] = val
    return A


def test_4_denormal_range_no_longer_exceeds_the_true_norm():
    """THE SECOND VIOLATION CLASS, REPAIRED -- and it was the insidious one:
    not `inf` but a perfectly ordinary-looking FINITE number above the true norm.

    Before the repair this case reported +425.2 ULP (6.04e-04 relative) above the
    exact true norm.  The cause was that at denormal scale each product carries
    ~1e-6 relative rounding and the maximiser sits ON the extremal direction, so
    the whole error landed above the true norm.  Normalising `A` by an exact power
    of two lifts the arithmetic back into the normal range and restores the full
    53-bit mantissa; the residue is removed by the downward deflation and, because
    the recombined result lands back in the SUBNORMAL range where `ldexp` itself
    rounds, by one final step down.

    Still verified three ways, so the verdict cannot be blamed on the reference:
    the exact rational true norm, the exact rational ratio OF THE SAME WITNESS
    (which must be <= the true norm), and the reported float (which must now be
    <= both).
    """
    n = 32
    th = (np.arange(n) + 0.5) * np.pi / n
    X = np.tan(0.5 * th)
    w = (1.0 + X ** 2) ** (-0.75)
    A = np.random.default_rng(7).normal(size=(n, n)) * 1e-320
    dom, cod = WeightedLinf(w), WeightedL1(w)
    with np.errstate(all="ignore"):
        f = family_lower(A, dom, cod, th, **KW)
    true = exact_norm(A, w, w)
    L = f["lower"]
    assert np.isfinite(L) and L > 0.0, L
    excess = _excess_ulps(L, true)
    assert excess <= 0.0, (L, float(true), excess, REGRESSED)

    hit = None
    for nm, g in smooth_family(th, cod.w, **KW):
        if nm == f["argmax"]:
            hit = g.copy()
            break
    hit[0] = 0.0
    gF = [Fraction(float(x)) for x in hit]
    numF = max(Fraction(float(w[i]))
               * abs(sum(Fraction(float(A[i, j])) * gF[j] for j in range(n)))
               for i in range(n))
    denF = sum(Fraction(float(w[j])) * abs(gF[j]) for j in range(n))
    exact_ratio = numF / denF
    assert exact_ratio <= true, (float(exact_ratio), float(true))
    assert Fraction(L) <= exact_ratio, (L, float(exact_ratio), REGRESSED)
    print("[ok] (4) REPAIRED, FINITE class: true norm = %.6e, reported lower = "
          "%.6e -- now %+.3f ULP (%.2e relative), was +425.2 ULP (+6.04e-04) "
          "before the repair. The SAME witness's EXACT ratio is %.6e and the "
          "reported value is at or below it, so the float evaluation no longer "
          "manufactures an excess."
          % (float(true), L, excess, float(Fraction(L) / true) - 1.0,
             float(exact_ratio)))


def test_5_sound_on_the_non_overflowing_battery():
    """No FINITE value above the true norm, by any margin, anywhere in range."""
    th = theta_grid()
    rng = np.random.default_rng(7)
    G = rng.normal(size=(N, N))
    i, j = np.arange(N), np.arange(N)
    ops = {
        "random": G,
        "hilbert": 1.0 / (i[:, None] + j[None, :] + 1.0),
        "rank1": np.outer(G[:, 0], G[0, :]),
        "zero": np.zeros((N, N)),
        "zero_gauge_column": _poke(G, (slice(None), 0), 0.0),
        "near_defective": np.eye(N) * 1e-12 + np.diag(np.ones(N - 1), 1),
        "tiny": G * 1e-300,
        "huge": G * 1e300,
        "denormal": G * 1e-320,
    }
    wts = {"unit": np.ones(N), "decay": decay_weights()}
    worst, worst_name, n = -np.inf, "", 0
    for oname, A in ops.items():
        for wname, w in wts.items():
            dom, cod = WeightedLinf(w), WeightedL1(w)
            with np.errstate(all="ignore"):
                r = best_lower(A, dom, cod, th, ascent_iters=50, **KW)
            L = r["lower"]
            assert np.isfinite(L), (oname, wname, L, REGRESSED)
            true = exact_norm(A, w, w)
            n += 1
            if L == 0.0:
                continue
            excess = _excess_ulps(L, true)
            assert excess <= 0.0, (oname, wname, L, float(true), excess, REGRESSED)
            if excess > worst:
                worst, worst_name = excess, "%s/%s" % (oname, wname)
    print("[ok] (5) %d in-range cases (now including the huge and denormal "
          "scalings that used to overflow): NO finite value exceeds the exact "
          "true norm at all -- worst margin is %+.3f ULP, at %s, i.e. below it"
          % (n, worst, worst_name or "none"))


def test_6_headline_is_always_an_admissible_deflated_witness():
    """On the project's REAL Holder norms: whatever is reported is attained.

    Post-repair the headline is a certified DEFLATION of the witness's own float
    quotient, not that quotient itself, so the criterion is directional: the
    headline must sit at or below its witness.  That is strictly stronger than
    the pre-repair two-sided 1e-12 reproduction it replaces.

    The SIZE of the gap splits into two regimes, and conflating them would hide
    the finding rather than pin it:

      * in the NORMAL range the gap is the deflation itself, ~1e-12 relative;
      * in the SUBNORMAL range the naive witness quotient is the very thing leg
        101 caught being wrong -- it is evaluated on denormal products carrying
        ~1e-6 relative rounding each.  The module's value is computed after the
        exact power-of-two lift into the normal range, so it is MORE accurate
        than the witness, and the gap measures the denormal inflation the repair
        REMOVES (47.7 ULP here), not a deflation it applies.  Bounding it in ULP
        is the only meaningful statement; one ULP is already 1.4e-6 relative
        there, so a 1e-9 relative budget is not a coherent test.
    """
    col = Collocation(N)
    dom = HolderNorm(col.theta, col.X, 1.5, 0.5)
    cod = HolderNorm(col.theta, col.X, 2.5, 0.5)
    cod.w[0] = 1.0
    rng = np.random.default_rng(7)
    G = rng.normal(size=(N, N))
    checked, zeros, worst, sub_ulp, sub_n = 0, 0, 0.0, 0.0, 0
    for name, A in (("random", G), ("rank1", np.outer(G[:, 0], G[0, :])),
                    ("hilbert_1e200", (1.0 / (np.arange(N)[:, None]
                                              + np.arange(N)[None, :] + 1.0)) * 1e200),
                    ("denormal", G * 1e-320),
                    ("nan_entry", _poke(G, (5, 7), np.nan)),
                    ("inf_entry", _poke(G, (9, 11), np.inf))):
        with np.errstate(all="ignore"):
            f = family_lower(A, dom, cod, col.theta, **KW)
        if f["lower"] == 0.0:
            zeros += 1
            continue
        hit = None
        for nm, g in smooth_family(col.theta, cod.w, **KW):
            if nm == f["argmax"]:
                hit = g.copy()
                break
        assert hit is not None, (name, f["argmax"])
        hit[0] = 0.0
        with np.errstate(all="ignore"):
            nrm = cod(hit)
            ratio = dom(A @ hit) / nrm
        assert np.isfinite(nrm) and nrm > 0, (name, nrm)
        assert np.isfinite(ratio), (name, ratio)
        assert f["lower"] <= ratio, (name, f["lower"], ratio, REGRESSED)
        rel = (ratio - f["lower"]) / ratio
        if abs(f["lower"]) < np.finfo(float).tiny:
            ulp = float(np.nextafter(ratio, np.inf) - ratio)
            gap = (ratio - f["lower"]) / ulp
            # No ULP threshold is invented here: the naive quotient is the very
            # quantity leg 101 caught being wrong in this range, so it is not an
            # authority to grade against.  What IS asserted is that the gap stays
            # inside the denormal ROUNDING REGIME (~1e-6 to 1e-3 relative); a gap
            # beyond 1e-2 would mean something other than rounding.  Soundness
            # here is decided by the exact rational reference in check (4).
            assert rel <= 1e-2, (name, ratio, f["lower"], rel, gap)
            sub_ulp, sub_n = max(sub_ulp, gap), sub_n + 1
        else:
            assert rel <= 1e-9, (name, ratio, f["lower"], rel)
            worst = max(worst, rel)
        checked += 1
    print("[ok] (6) on the real Holder pair, %d nonzero headlines each sit at or "
          "below their named family member's own quotient. In the NORMAL range "
          "the gap is the certified deflation, at most %.2e relative (slack "
          "budget %.0e); in the SUBNORMAL range (%d case) the gap is %.1f ULP "
          "and runs the other way -- it is the denormal inflation the repair "
          "REMOVES from the naive quotient. The other %d report exactly 0.0"
          % (checked, worst, NORM_SLACK, sub_n, sub_ulp, zeros))


def test_7_production_path_has_vast_overflow_headroom():
    """The scope bound: no banked Route-D number can be touched by this."""
    J = 200
    col = Collocation(J)
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    A = np.linalg.inv(M)
    cod = HolderNorm(col.theta, col.X, 2.5, 0.5)
    cod.w[0] = 1.0
    worst = 0.0
    for name, g in smooth_family(col.theta, cod.w, **KW):
        g = g.copy()
        g[0] = 0.0
        worst = max(worst, float(np.max(np.abs(A @ g))))
    decades = np.log10(np.finfo(float).max / worst)
    assert decades > 250.0, (worst, decades)
    print("[ok] (7) production path (J = %d, the banked Route-D operator): the "
          "largest image the family produces is %.3f, i.e. %.3f DECADES below "
          "the overflow ceiling -- the defect in (1) and (2) never could reach "
          "any banked number" % (J, worst, decades))


def test_8_the_rescaling_is_exact():
    """The repair's load-bearing assumption, VERIFIED rather than assumed.

    Everything rests on `x -> x * 2**-e` being exact in binary floating point.
    If it were not, the rescale would itself be a source of error and the whole
    deflation argument would be circular.  Checked by round-trip over the full
    exponent range, including denormal input, on the exact arrays the module
    builds.
    """
    rng = np.random.default_rng(3)
    checked = 0
    for scale in (1e-320, 1e-300, 1e-8, 1.0, 1e8, 1e300):
        x = rng.normal(size=(N, N)) * scale
        y, e = _pow2_normalise(x)
        fin = np.abs(y[np.isfinite(y) & (y != 0)])
        if fin.size:
            assert float(np.max(np.abs(y))) < 1.0, scale
            assert float(np.max(np.abs(y))) >= 0.5, scale
        back = np.ldexp(y, e)
        # exact means EXACT: bit-for-bit, not "to within a tolerance"
        assert np.array_equal(back, x), (scale, float(np.max(np.abs(back - x))))
        # and the rational values agree, which is the statement that matters
        assert (Fraction(float(y[0, 0])) * Fraction(2) ** e
                == Fraction(float(x[0, 0]))), scale
        checked += 1
    print("[ok] (8) the power-of-two rescaling round-trips BIT-FOR-BIT on %d "
          "scalings from 1e-320 (denormal) to 1e300, and the rational identity "
          "y * 2^e == x holds exactly -- the rescale contributes zero error"
          % checked)


def test_9_out_of_range_norm_saturates_instead_of_returning_inf():
    """When the true norm really IS past the ceiling, saturate -- never `inf`.

    `finfo.max` is a true lower bound on a norm of ~1e400 and a caller can act on
    it; `inf` is also true here but indistinguishable from the overflow bug the
    repair removed, so the module reports the former and counts it.
    """
    th = theta_grid()
    A = np.random.default_rng(1).normal(size=(N, N)) * 1e100
    t, u = np.full(N, 1e150), np.full(N, 1e-150)
    dom, cod = WeightedLinf(t), WeightedL1(u)
    with np.errstate(all="ignore"):
        f = family_lower(A, dom, cod, th, **KW)
    assert np.isfinite(f["lower"]), (f["lower"], REGRESSED)
    assert f["lower"] == np.finfo(float).max, f["lower"]
    assert f["saturated"] >= 1, f
    true_decades = np.log10(np.max(np.abs(A))) + 150.0 + 150.0
    assert true_decades > 308.0, true_decades
    print("[ok] (9) a genuinely out-of-range operator (true norm ~1e%.0f, past "
          "the 1.798e308 ceiling) SATURATES to finfo.max with saturated = %d, "
          "instead of returning `inf`" % (true_decades, f["saturated"]))


def test_10_production_path_moves_down_only_and_rejects_nothing():
    """The other half of the repair's pre-committed rule.

    A repair that fixed soundness by returning 0 everywhere would pass every
    check above.  This one pins the opposite side: on the operator Route-D
    actually banked, the reported bound must move DOWN by at most 1e-9 relative
    and NOTHING may be rejected or saturated.
    """
    for J, banked in ((200, 2.682095980021302), (300, 2.805616494722006),
                      (400, 2.8844503038532703)):
        col = Collocation(J)
        M = np.empty((J, J))
        M[0, :] = col.to_coef.sum(axis=0)
        M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
        A = np.linalg.inv(M)
        dom = HolderNorm(col.theta, col.X, 1.5, 0.5)
        cod = HolderNorm(col.theta, col.X, 2.5, 0.5)
        cod.w[0] = 1.0
        f = family_lower(A, dom, cod, col.theta, n_centre=12, n_step=12)
        assert f["rejected"] == 0, (J, f["rejected"])
        assert f["saturated"] == 0, (J, f["saturated"])
        assert f["lower"] <= banked, (J, f["lower"], banked)          # down only
        rel = (banked - f["lower"]) / banked
        assert rel <= 1e-9, (J, f["lower"], banked, rel)
        assert f["argmax"] == "bump3.12/0.50", (J, f["argmax"])
        print("[ok] (10) J = %d: pre-repair %.15f -> %.15f, moved DOWN by "
              "%.3e relative (budget 1e-9), 0 rejected, 0 saturated, argmax "
              "unchanged (%s)" % (J, banked, f["lower"], rel, f["argmax"]))


if __name__ == "__main__":
    test_1_repaired_near_singular_tiny_weights()
    test_2_ascent_no_longer_overflows_on_its_own_step()
    test_3_nan_and_inf_poisoning_underreports()
    test_4_denormal_range_no_longer_exceeds_the_true_norm()
    test_5_sound_on_the_non_overflowing_battery()
    test_6_headline_is_always_an_admissible_deflated_witness()
    test_7_production_path_has_vast_overflow_headroom()
    test_8_the_rescaling_is_exact()
    test_9_out_of_range_norm_saturates_instead_of_returning_inf()
    test_10_production_path_moves_down_only_and_rejects_nothing()
    print("\nALL OP-LOWER ADVERSARIAL TESTS PASSED "
          "(checks 1, 2, 4 pin leg 101's REPAIRED violations -- see the module "
          "docstring)")
