"""Leg 209 / Route-SCA2 -- permanent adversarial regression battery for
`solver/spectral_certificate.py`.

`test_spectral_certificate.py` (466 lines, 37 gates) is the completeness-direction suite:
every input it passes is well-formed, and 0 of its 466 lines inject a non-finite,
degenerate, out-of-domain or wrong-but-type-compatible value.  This file is the other
direction, and it is a NEW file -- unlike legs 198 and 201, no adversarial battery for
this module existed (`git log --all -- test_spectral_certificate_adversarial.py` was
empty at dispatch), so nothing here is appended to a prior leg's gates.

--------------------------------------------------------------------------
TWO KINDS OF GATE, AND THE DIFFERENCE MATTERS (leg 80/198's convention)
--------------------------------------------------------------------------
CHARACTERIZATION pins (prefix `C`) describe what the module does TODAY, on the four
silent-wrong mechanisms leg 209 found.  **They pass because the defect is present.**
When a repair lands they MUST start failing -- that is the point of pinning them, and a
repair leg should expect to invert them in the same commit that fixes the module.

SOUNDNESS gates (prefix `S`) assert behaviour that must NEVER regress: the paths that
already reject or visibly propagate, the containment of `weighted_l1_upper` on positive
weights, and -- most important -- that the CLEAN-input numbers still agree with exact
rational arithmetic.  If an `S` gate fails, something real broke.

The module is READ-ONLY to leg 209 and is not patched by it.
"""

import os
import sys
from fractions import Fraction

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np                                                     # noqa: E402

sys.path.insert(0, ".")

import solver.spectral_certificate as sc                               # noqa: E402

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


def raises(fn):
    try:
        fn()
        return False
    except Exception:                                                  # noqa: BLE001
        return True


# ==========================================================================
# S -- CLEAN INPUT MUST STAY SOUND.  Everything else in this file is about inputs
# the shipped path never produces; this gate is about the ones it does.
# ==========================================================================
_worst = 0.0
for _K in (8, 16, 32, 64):
    _f = sc.finite_section_inverse_norm(_K, "geometric", 1.1)
    _e = float(sc.exact_inverse_norm(_K, Fraction(11, 10)))
    _worst = max(_worst, abs(_f - _e) / _e)
gate("S1 clean input: float64 agrees with exact rational", _worst < 1e-14,
     f"max relative difference between finite_section_inverse_norm and "
     f"exact_inverse_norm over K = 8,16,32,64 at nu = 11/10 is {_worst:.4e} "
     f"(banked lesson 86: this is what bounds leg 209's blast radius to LATENT)")

_L = sc._scaled_tail(8, 8 + 512, "algebraic", 0.3)[0]
_sig_clean, _j, _ = sc.l1_bounded_below_constant(_L)
gate("S2 clean sigma_min at leg 127's shipped corner is finite and positive",
     np.isfinite(_sig_clean) and _sig_clean > 0,
     f"K=8, M_extra=512, algebraic s=0.3 -> sigma_min = {_sig_clean!r}; "
     f"counterexample_norm_floor(Z1=0.5) = "
     f"{sc.counterexample_norm_floor(0.5, _sig_clean)!r}")

gate("S3 sigma_min is correct on a hand-computable input",
     sc.l1_bounded_below_constant(np.diag([2.0, 4.0]))[0] == 2.0,
     "inf ||Lx||_1/||x||_1 for diag(2,4) is 2 by hand; the instrument is right where "
     "the answer is known independently of the code")

# ==========================================================================
# C1 -- THE HEADLINE.  `nrm > 0` is IEEE-754-unordered under NaN, so
# `l1_bounded_below_constant` returns +inf: the MOST FAVOURABLE sigma_min.
# ==========================================================================
_n = _L.shape[0]
_infs = []
for _w in [(0, 0), (_n // 2, _n // 2), (_n - 1, _n - 1), (0, _n - 1)]:
    _Lp = _L.copy()
    _Lp[_w] = np.nan
    _infs.append(sc.l1_bounded_below_constant(_Lp)[0])
gate("C1a PIN: one NaN sends sigma_min to +inf, not to a defect signal",
     all(np.isinf(v) and v > 0 for v in _infs),
     f"a single NaN anywhere in {_n * _n} entries ({1.0 / (_n * _n):.3e} of the matrix) "
     f"returns sigma_min = +inf against the clean {_sig_clean!r}. "
     f"MECHANISM: IEEE 754 gives comparisons four outcomes, the fourth being UNORDERED "
     f"when an operand is NaN, so `nrm > 0` is False and the function takes the "
     f"`float('inf')` branch written for nrm == 0. MUST FAIL after a repair.")

_floor_clean = sc.counterexample_norm_floor(0.5, _sig_clean)
gate("C1b PIN: the defect signal is fully laundered two calls downstream",
     sc.counterexample_norm_floor(0.5, float("inf")) == 0.0,
     f"counterexample_norm_floor(0.5, inf) = 0.0 -- finite, plausible, and Theorem NGX's "
     f"general-class conclusion INVERTED: it reports that a counterexample reaching "
     f"Z1 = 0.5 needs ||A||_w >= 0 (any bounded A will do) where the clean answer is "
     f"||A||_w >= {_floor_clean!r}. MUST FAIL after a repair.")

_td = sc.general_class_tradeoff(0.5, 100.0, float("inf"))
gate("C1c PIN: general_class_tradeoff reports the no-go as holding, vacuously",
     _td["holds"] is True and _td["rhs"] == float("-inf"),
     f"general_class_tradeoff(Z1=0.5, ||A||=100, sigma_min=inf) -> holds=True with "
     f"rhs=-inf: the inequality is reported satisfied while carrying zero information. "
     f"MUST FAIL after a repair.")

gate("C1d PIN: the NaN is MANUFACTURED by the module's own documented weight API",
     all(int(np.isnan(sc._scaled_tail(8, 8 + 64, k, p)[0]).sum()) > 0
         for k, p in (("geometric", -1.1), ("geometric", 0.0), ("geometric", -0.5))),
     "_scaled_tail returns an all-NaN matrix for a geometric `param` <= 0, which "
     "weight_vector/log_weight_vector accept with no check although the docstring "
     "documents nu > 1. So C1a is reachable without injecting anything. MUST FAIL "
     "after a repair.")

# S -- and the Inf / exactly-singular arms DO hold.  Saying so is the point: the
# finding is about NaN specifically, not about non-finite input in general.
gate("S4 exactly-singular and all-zero inputs are REJECTED, visibly",
     raises(lambda: sc.l1_bounded_below_constant(np.zeros((4, 4)))[0]) and
     raises(lambda: sc.l1_bounded_below_constant(
         np.where(np.arange(4)[None, :] == 3, 0.0, np.eye(4)))[0]),
     "np.linalg.inv raises LinAlgError -- these paths hold and must keep holding")

# ==========================================================================
# C2 -- NEGATIVE WEIGHTS: an unguarded `nu` produces signed 'weights', and the routine
# that stamps `rigorous: True` then returns a bound BELOW what it claims to bound.
# Independent, unrepaired instance of leg 198's bordered_hl.py mechanism.
# ==========================================================================
_w_neg = sc.weight_vector(4, "geometric", -1.1)
gate("C2a PIN: weight_vector accepts a negative geometric nu and returns signed weights",
     bool(np.any(_w_neg < 0)),
     f"weight_vector(4,'geometric',-1.1) = {np.round(_w_neg, 4).tolist()} -- no check, "
     f"no warning, no exception, against a docstring that says nu > 1. MUST FAIL after "
     f"a repair.")

_M = sc.bordered_linearization(4)
_wp = np.concatenate([sc.weight_vector(4, "geometric", 1.1), [1.0]])
_wn = np.concatenate([_w_neg, [1.0]])
_np_, _nn = sc.weighted_l1_opnorm(_M, _wp, _wp), sc.weighted_l1_opnorm(_M, _wn, _wn)
_na = sc.weighted_l1_opnorm(_M, np.abs(_wn), np.abs(_wn))
gate("C2b PIN: weighted_l1_opnorm understates via sign cancellation",
     _nn < _na and _nn > 0,
     f"same magnitudes, one sign pattern: returns {_nn!r} against the true {_na!r} -- "
     f"understated {_na / _nn:.4f}x, and POSITIVE and plausible so nothing downstream "
     f"can tell. MUST FAIL after a repair.")

_rp = sc.rigorous_finite_block(8, "geometric", 1.1)
_rn = sc.rigorous_finite_block(8, "geometric", -1.1)
gate("C2c PIN: rigorous_finite_block returns a NON-CONTAINING ||A||_w with rigorous=True",
     _rn["A_norm"] < _rp["A_norm"] and _rn["rigorous"] is True,
     f"A_norm = {_rn['A_norm']!r} at nu=-1.1 against {_rp['A_norm']!r} at nu=+1.1 -- "
     f"UNDERSTATED {_rp['A_norm'] / _rn['A_norm']:.6f}x and BELOW 1, flagged "
     f"rigorous=True, while finite_section_inverse_norm on identical arguments returns "
     f"NaN. weighted_l1_upper is documented as a RIGOROUS UPPER BOUND. Same shape as "
     f"leg 201's non-containing enclosure. MUST FAIL after a repair.")

gate("C2d PIN: algebra_constant is bit-identically blind to the sign of nu",
     sc.algebra_constant("geometric", 1.1, K=16) ==
     sc.algebra_constant("geometric", -1.1, K=16),
     f"both return {sc.algebra_constant('geometric', 1.1, K=16)!r}. Lesson 90's tell: "
     f"identical numbers from two inputs that should differ. It reports 'Banach algebra "
     f"holds' (<= 1) for a weight class that is not a norm. MUST FAIL after a repair.")

gate("C2e PIN: the two weight representations disagree outside the documented domain",
     bool(np.all(np.isnan(sc.log_weight_vector(4, "geometric", -1.1)))) and
     bool(np.all(np.isfinite(sc.weight_vector(4, "geometric", -1.1)))),
     "weight_vector returns finite signed numbers where log_weight_vector returns NaN. "
     "rigorous_finite_block uses the first and finite_section_inverse_norm the second, "
     "so the same arguments give a finite 'rigorous' constant on one path and NaN on "
     "the other. MUST FAIL after a repair.")

# S -- the containment control, which must come out BOTH ways
_rng = np.random.default_rng(0)
_bad_pos = 0
for _ in range(200):
    _K = int(_rng.integers(3, 12))
    _A = _rng.standard_normal((_K + 1, _K + 1))
    _w = np.exp(_rng.uniform(-3, 3, _K + 1))
    if sc.weighted_l1_upper(_A, _A, _w) < float(np.max((np.abs(_A) * _w[:, None]).sum(0) / _w)):
        _bad_pos += 1
gate("S5 weighted_l1_upper CONTAINS on positive weights, 200/200",
     _bad_pos == 0,
     f"{_bad_pos}/200 non-containing draws. The routine is not broken in general -- this "
     f"is what makes C2b/C2c findings rather than noise, and it must never regress.")

_bad_neg = 0
_worst_ratio = 1.0
for _ in range(200):
    _K = int(_rng.integers(3, 12))
    _A = _rng.standard_normal((_K + 1, _K + 1))
    _w = np.exp(_rng.uniform(-3, 3, _K + 1))
    _w[int(_rng.integers(0, _K + 1))] *= -1.0
    _ub = sc.weighted_l1_upper(_A, _A, _w)
    _ex = float(np.max((np.abs(_A) * np.abs(_w)[:, None]).sum(0) / np.abs(_w)))
    if _ub < _ex:
        _bad_neg += 1
        _worst_ratio = min(_worst_ratio, _ub / _ex)
gate("C2f PIN: exactly one sign flip breaks containment 200/200",
     _bad_neg == 200,
     f"worst ub/exact = {_worst_ratio!r} -- the 'rigorous upper bound' comes back "
     f"NEGATIVE. The control differs from S5 by one sign and nothing else, so the "
     f"mechanism is the sign. MUST FAIL after a repair.")

# ==========================================================================
# C3 -- `kernel_membership_ladder` misclassifies CONVERGENT cases as not-in-space.
# Direction is CONSERVATIVE for the no-go (it refuses (H2) rather than misapplying it);
# pinned because it is a wrong classification of a documented hypothesis, not because
# it weakens the theorem.
# ==========================================================================
_r099 = sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", 0.99)
gate("C3a PIN: a convergent algebraic exponent is reported not-in-l^1_w",
     _r099["in_l1_w"] is False,
     f"s = 0.99: verdict='{_r099['verdict']}' from increment ratio "
     f"{_r099['last_increment_ratio']!r} against the hard-coded 0.95 threshold, but "
     f"sum m^-1.01 CONVERGES so h IS in l^1_w. MUST FAIL after a repair.")

_geo = [sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "geometric", nu)
        for nu in (0.5, 0.9, 1.05, 1.1)]
gate("C3b PIN: all four geometric cases return 'indeterminate'",
     all(r["verdict"] == "indeterminate" for r in _geo),
     "increments underflow to exactly 0.0 (nu<1) or overflow so inf-inf=NaN (nu>1), and "
     "`incr[i] if incr[i] else nan` turns both into a NaN ratio. The geometric class is "
     "the one this module's own docstring calls 'the literature's default'. MUST FAIL "
     "after a repair.")

_lo, _hi = 0.7, 1.0
for _ in range(40):
    _mid = 0.5 * (_lo + _hi)
    if sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", _mid)["in_l1_w"]:
        _lo = _mid
    else:
        _hi = _mid
gate("C3c PIN: the wrongly-excluded band is [0.9639, 1) and the shipped path misses it",
     0.96 < _hi < 0.97,
     f"bisected band edge {_hi!r}, width {1.0 - _hi!r} in the weight exponent; nearest "
     f"shipped s is 0.7 (ratio 0.6590), margin {_hi - 0.7:.6f} in s. This margin is why "
     f"leg 209 reported the finding LATENT rather than contaminating. MUST FAIL after "
     f"a repair.")

gate("S6 kernel_membership_ladder is CORRECT across the shipped exponents",
     all(sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", s)["in_l1_w"]
         is (s < 1.0) for s in (0.0, 0.3, 0.7)) and
     sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", 1.5)["verdict"]
     == "power_divergent",
     "s = 0, 0.3, 0.7 all in_l1_w=True and s = 1.5 power_divergent: every exponent leg "
     "51/58/127 actually shipped is classified correctly, which is the executable form "
     "of leg 209's LATENT determination")

# ==========================================================================
# C4 -- the same unordered-comparison mechanism as C1, at a second site.
# ==========================================================================
gate("C4 PIN: weight_window reports empty=False for an undefined alpha",
     sc.weight_window(float("nan"), 0.3)["empty"] is False,
     "bool(nan >= nan) is False, so the FAVOURABLE answer ('the window is not empty, a "
     "certificate can still close') is returned on undefined input. `gap` is a visible "
     "NaN but `empty` is the boolean a caller branches on. MUST FAIL after a repair.")

gate("S7 weight_window's `empty` flag is not a constant",
     sc.weight_window(0.394, 0.3)["empty"] is False and
     sc.weight_window(0.394, 1.0)["empty"] is True,
     "comes out both ways on clean input (alpha=0.394 against s_operator 0.3 and 1.0) -- "
     "lesson 90: a control that cannot come out differently is not a control")

# ==========================================================================
# S -- the degenerate index domain is SOUND, and that is a result too.
# ==========================================================================
gate("S8 degenerate index domains all reject visibly, 6/6",
     all(raises(f) for f in (
         lambda: sc.tail_inverse_norm(4, 4),
         lambda: sc.tail_block(4, 3),
         lambda: sc.tail_inverse_norm(4, 5),
         lambda: sc.tail_left_null(4, 5),
         lambda: sc.bordered_tail_inverse_norm(4, 5),
         lambda: sc.singular_sequence_rate([1, 1], [1.0, 2.0]))),
     "M == K, M < K, a one-row tail, and degenerate polyfit abscissae all raise "
     "(ValueError / LinAlgError / IndexError) rather than returning a number")

_res = sc.clm_residual([float("nan"), 0.0], -1.0, 1.0)
gate("S9 a NaN in the profile propagates through clm_residual, 0 absorbed",
     any(isinstance(x, float) and np.isnan(x) for x in _res),
     "the exact coefficient-space residual does not launder a poisoned profile")

gate("C5 PIN: a non-integer K is silently truncated",
     sc.bordered_linearization(4.9).shape == (5, 5),
     "bordered_linearization(4.9) becomes K=4 via int() with no warning. Same shape as "
     "leg 198's 'pin of arity 5 truncated to 3'. Low magnitude, pinned for completeness "
     "of the mechanism count. MUST FAIL after a repair.")

# ==========================================================================
print()
_fails = [r for r in results if r[0] == FAIL]
print(f"{len(results) - len(_fails)}/{len(results)} gates pass "
      f"({sum(1 for r in results if r[1].startswith('C'))} characterization pins, "
      f"{sum(1 for r in results if r[1].startswith('S'))} soundness gates)")
if _fails:
    for _, n, d in _fails:
        print(f"  FAIL {n}: {d}")
    sys.exit(1)
