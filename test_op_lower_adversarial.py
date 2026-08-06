"""Leg 101 (Route-OLA) -- permanent adversarial gates for solver/op_lower.py.

WHAT THIS FILE PINS, AND WHY IT ASSERTS A DEFECT RATHER THAN ITS ABSENCE.

Leg 101's gate asked whether `solver/op_lower.py` can be made to return a value
ABOVE the true operator norm -- i.e. whether the one property a lower bound must
have can be broken.  It answered **YES**, on **47 of 209** gate-deciding cases, by
two distinct mechanisms:

  (1) OVERFLOW, 46 cases.  The numerator `A @ g` overflows to `inf` while the
      true norm is finite and often perfectly ordinary.  The sharpest case
      returns `inf` as a "lower bound" on an operator whose norm is exactly
      **1.0e13**.  Two separate routes reach it: a degenerate codomain weight
      (`1/w` makes the candidate huge -- check 1), and `ascend`'s own step, which
      is sized proportional to the bound found so far, so the search overflows
      itself on any large-norm operator even with unit weights and a finite
      family value (check 2).

  (2) FINITE EXCEEDANCE, 1 case.  In the denormal range the float quotient is
      inflated ~1e-6 relative per operation, and because the maximiser sits ON
      the extremal direction there is no slack to absorb it: the reported value
      lands **425 ULP (6.04e-04 relative) above** the exact true norm, as an
      ordinary-looking finite number (check 4).  This is the more insidious of
      the two -- `inf` at least announces itself.

Per the leg contract the defect was **escalated, not patched** -- `op_lower.py` is
byte-identical to what leg 101 found.  So checks (1), (2) and (4) are
**characterization** gates: they assert the violation is STILL THERE.  That is
deliberate.  If one fails because the module now returns a finite/sound value,
the defect has been FIXED, which is good news and means this file must be updated
(and `capabilities.py`'s "brackets the dense operator norm from below" claim
revisited) -- the failure message says so.

Checks (3), (5), (6), (7) are ordinary regression gates on the properties that DID
hold, and must not rot: NaN poisoning under-reports (exactly 0.0) rather than
inventing a plausible number, everything in the normal float range is sound to
within one ULP, the headline is always reproduced by an admissible vector, and the
production path keeps a vast margin to the overflow ceiling.

SCOPE, measured (7): no banked Route-D number is affected.  On the real
J-collocation operator the largest image the candidate family produces is 2.38,
which is **307.9 decades** below the float64 overflow ceiling, and its entries are
~1e2, some 300 decades above the denormal range.  The defect is real and it is
reachable only by inputs hundreds of orders of magnitude away from anything this
project feeds the module.

Run: .venv/bin/python test_op_lower_adversarial.py
"""

from fractions import Fraction

import numpy as np

from solver.decay_collocation import Collocation, C_ANCHOR
from solver.holder_norms import HolderNorm
from solver.op_lower import (
    best_lower, family_lower, sign_pattern_lower, smooth_family,
)

N = 32
KW = dict(n_centre=8, n_step=8)
FIXME = ("  If this fails because op_lower now returns a FINITE value, the "
         "leg-101 overflow defect has been FIXED: update this file and revisit "
         "capabilities.py's validated-clause for solver/op_lower.py.")


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


# ---------------------------------------------------------------------------
def test_1_the_violation_near_singular_tiny_weights():
    """THE SHARPEST CASE: inf returned as a lower bound on a norm of 1.0e13."""
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
    assert np.isinf(r["lower"]), (r["lower"], FIXME)
    assert np.isinf(s), (s, FIXME)
    print("[ok] (1) VIOLATION pinned: true norm = %.3e, op_lower reports "
          "lower = %r (sign patterns %r, family %r) -- an INFINITE lower bound "
          "on a finite operator. 1/w = 1e300 makes |A g| = 1e313, past the "
          "1.798e308 ceiling; the codomain norm stays a benign %.1f."
          % (float(true), r["lower"], s, r["smooth_family"], cod(np.full(N, 1e300))))


def test_2_the_ascent_overflows_on_its_own_step():
    """A SECOND, distinct mechanism, and it needs no degenerate weight at all.

    `ascend` sizes its trial step as `scale * best * (...)`, i.e. proportional to
    the bound found so far.  So on any operator whose norm is large enough, the
    ascent's OWN candidate vectors overflow even though the family that seeded it
    was perfectly finite -- and `best_lower` then takes the max, promoting `inf`
    to the headline.  Here the family returns a finite 5.0e199 and the ascent
    turns it into `inf`.  Weights are all 1; every entry of A is finite.
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
    assert np.isfinite(f["lower"]), f["lower"]          # the family is fine
    assert np.isinf(r["after_ascent"]), (r["after_ascent"], FIXME)
    assert np.isinf(r["lower"]), (r["lower"], FIXME)
    print("[ok] (2) VIOLATION via the ASCENT, with UNIT weights and all-finite "
          "entries: true norm = %.4e, family = %.4e (sound), after_ascent = %r, "
          "headline = %r. The step is proportional to `best`, so the search "
          "overflows itself."
          % (float(true), f["lower"], r["after_ascent"], r["lower"]))


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
        if kind == "nan":
            # a NaN-poisoned operator has no norm at all: the only safe answer
            # is to under-report, and it does -- exactly 0.0, never a plausible
            # finite number that a caller would believe.
            assert L == 0.0, (name, L)
            nan_cases.append((name, L))
        else:
            # an Inf-poisoned operator genuinely HAS unbounded norm, so `inf` is
            # the CORRECT answer here, not a violation.  What must never happen
            # is a finite, plausible-looking value.
            assert L == 0.0 or np.isinf(L), (name, L)
            inf_cases.append((name, L))
    print("[ok] (3) 3 NaN-poisoned operators report exactly 0.0 (safe "
          "under-report, never NaN, never a plausible finite number); 2 "
          "Inf-poisoned operators report %s -- correct, their true norm IS "
          "unbounded. Clean-operator norm for scale: %.2f"
          % (", ".join("%s=%r" % c for c in inf_cases),
             float(exact_norm(G, w, w))))


def _poke(G, idx, val):
    A = G.copy()
    A[idx] = val
    return A


def test_4_finite_value_above_the_true_norm_in_the_denormal_range():
    """THE SECOND VIOLATION CLASS, and the more insidious one: not `inf` but a
    perfectly ordinary-looking FINITE number that is above the true norm.

    At denormal scale each product carries ~1e-6 relative rounding, and the
    maximiser sits ON the extremal direction, so there is no slack to absorb it:
    the whole error lands above the true norm.  Verified three ways here -- the
    exact rational true norm, the exact rational ratio OF THE SAME VECTOR (which
    is correctly <= the true norm), and the float ratio (which is not).  That
    triple is what shows the fault is in the float evaluation and not in the
    reference.
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
    ulp = float(np.nextafter(L, np.inf) - L)
    excess = float((Fraction(L) - true) / Fraction(ulp))
    assert excess > 100.0, (L, float(true), excess, FIXME)

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
    assert Fraction(L) > exact_ratio, (L, float(exact_ratio))
    print("[ok] (4) VIOLATION, FINITE: true norm = %.6e, reported lower = %.6e "
          "-- above it by %.1f ULP (%.2e relative). The SAME vector's EXACT "
          "ratio is %.6e, correctly <= the true norm, so the excess is created "
          "by the float evaluation of the quotient, not by the reference."
          % (float(true), L, excess, float(Fraction(L) / true) - 1.0,
             float(exact_ratio)))


def test_5_sound_on_the_non_overflowing_battery():
    """No FINITE value above the true norm, beyond one ULP, anywhere in range."""
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
    }
    wts = {"unit": np.ones(N), "decay": decay_weights()}
    worst, worst_name, n = 0.0, "", 0
    for oname, A in ops.items():
        for wname, w in wts.items():
            dom, cod = WeightedLinf(w), WeightedL1(w)
            with np.errstate(all="ignore"):
                r = best_lower(A, dom, cod, th, ascent_iters=50, **KW)
            L = r["lower"]
            assert np.isfinite(L), (oname, wname, L)
            true = exact_norm(A, w, w)
            n += 1
            if L == 0.0:
                continue
            ulp = float(np.nextafter(L, np.inf) - L)
            excess = float((Fraction(L) - true) / Fraction(ulp))
            assert excess <= 1.0, (oname, wname, L, float(true), excess)
            if excess > worst:
                worst, worst_name = excess, "%s/%s" % (oname, wname)
    print("[ok] (5) %d in-range cases: no finite value exceeds the exact true "
          "norm by more than one ULP (worst excess %.3f ULP, at %s -- that is "
          "correct rounding in the denormal range, not a defect)"
          % (n, worst, worst_name or "none"))


def test_6_headline_is_always_an_admissible_witness():
    """On the project's REAL Holder norms: whatever is reported is attained."""
    col = Collocation(N)
    dom = HolderNorm(col.theta, col.X, 1.5, 0.5)
    cod = HolderNorm(col.theta, col.X, 2.5, 0.5)
    cod.w[0] = 1.0
    rng = np.random.default_rng(7)
    G = rng.normal(size=(N, N))
    checked, zeros = 0, 0
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
        assert abs(ratio - f["lower"]) <= 1e-12 * max(1.0, abs(f["lower"])), \
            (name, ratio, f["lower"])
        checked += 1
    print("[ok] (6) on the real Holder pair, %d nonzero headlines are each "
          "reproduced to 1e-12 by the named family member (codomain norm finite "
          "and positive); the other %d report exactly 0.0" % (checked, zeros))


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
          "largest image the family produces is %.3f, i.e. %.1f DECADES below "
          "the overflow ceiling -- the defect in (1) and (2) cannot reach any "
          "banked number" % (J, worst, decades))


if __name__ == "__main__":
    test_1_the_violation_near_singular_tiny_weights()
    test_2_the_ascent_overflows_on_its_own_step()
    test_3_nan_and_inf_poisoning_underreports()
    test_4_finite_value_above_the_true_norm_in_the_denormal_range()
    test_5_sound_on_the_non_overflowing_battery()
    test_6_headline_is_always_an_admissible_witness()
    test_7_production_path_has_vast_overflow_headroom()
    print("\nALL OP-LOWER ADVERSARIAL TESTS PASSED "
          "(checks 1-2 PIN A LIVE DEFECT -- see the module docstring)")
