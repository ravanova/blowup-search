"""ADVERSARIAL gates for solver/holder_norms.py -- Route-HNA, leg 100, INVERTED after the
bench repair landed the finiteness/degeneracy guard.

`test_holder_norms.py` (the module's own file) tests that the module MEASURES correctly on
well-formed input: the norm axioms, the conformal identity, the embedding constants.  This
file tests what the module SAYS when the caller hands it input that is not well-formed --
a NaN or Inf in a weight-class parameter or a grid node, or a degenerate grading exponent.
`capabilities.py`'s validated line for the module covers "norm axioms and the embedding
constants", and that line is about correctness ON well-formed inputs; it makes no claim
about behaviour off them.  This file measures the off-window behaviour.

**HISTORY, AND WHY THIS FILE READS THE WAY IT DOES.**  Leg 100's gate answered YES: the
module had a silent-corruption gap in six distinct places.  Leg 100 was authorised to
audit and not to repair, so the gates below originally PINNED that silence on purpose --
they asserted the module's then-current WRONG behaviour, and carried the instruction to
"invert them the day a guard lands: keep every magnitude and flip only the sign of the
SIGNAL claim", exactly as leg 84's file did for `solver/target_norm.py`.  The bench repair
landed that guard.  This file is the inversion: **every magnitude leg 100 measured is
retained verbatim below, as the value the module USED to return, and each gate now asserts
that the same call is REFUSED.**  Nothing was weakened and nothing was deleted.

The mechanism was a single documented IEEE-754 hazard, instantiated at five sites: **every
NaN compares unordered, so an ordered comparison used as a filter silently DROPS the
poisoned item instead of propagating it.**  The four filters were

  * `jacobian_identity_error`  : `ok = |mid| * dth <= resolved`
  * `family_op_norm`           : `if ng <= 0: continue`
  * `family_op_norm`           : `if r > best:`
  * `holder_H_constant`        : `if den > 0:` and `max(best, .)`

plus one initialiser that survived an empty filter as a plausible answer:
`jacobian_identity_error`'s `worst, xmax = 0.0, 0.0`, where 0.0 means EXACT agreement.

**A SEVENTH CASE, found by the repair and not separated out by leg 100** (gates 14-16):
the builtin-`max` hazard also sits at `jacobian_identity_error`, where it is reachable
with **no NaN anywhere in the input** -- a single REPEATED grid node gives `dth = 0`, a
0/0 quotient at offset 1, and a NaN contribution that `max(0.0, nan)` discards, deleting
the finest and most informative offset from the maximum in total silence.

WHAT WAS NEVER BROKEN, and is still pinned as such (gate 17): the norm objects reduce the
CALLER'S DATA VECTOR through `np.max`, which propagates NaN honestly.  The repair
deliberately left that path alone -- validating `h` on every call would put an O(J^2) scan
inside `family_op_norm`'s inner loop to replace an already-correct answer.

Magnitudes, not booleans: every gate carries the number the module returned BEFORE the
repair alongside the number the same call returns on clean input.  Full battery and JSON:
`experiments/p2_route_hna_v1_adversarial.py` (leg 100's audit, which still measures the
pre-repair behaviour of a module loaded out of git),
`writeup/data/p2_route_hna_v1_adversarial.json`, and the repair's own A/B:
`experiments/bench_holder_norms_nan_guard_check.py`,
`writeup/data/bench_holder_norms_nan_guard_check.json`.
Novelty pass (all of this is a KNOWN hazard, none of it claimed as a discovery):
`writeup/novelty/leg_100.md`.

Run: `.venv/bin/python test_holder_norms_adversarial.py`
"""

import ast
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, ".")

from solver.holder_norms import (
    HolderNorm, conformal_check, decay_weight, family_op_norm, holder_H_constant,
    jacobian_identity_error, square_wave_partial_sum,
)

NAN, INF = float("nan"), float("inf")
PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    status = PASS if ok else FAIL
    results.append((status, name, detail))
    print(f"[{status}] {name}\n       {detail}")


def grid(J, eps=1e-3):
    th = np.linspace(-np.pi + eps, np.pi - eps, J)
    return th, np.tan(0.5 * th)


def quiet(fn, *a, **kw):
    """Run with warnings suppressed -- the point of most gates is the RETURNED VALUE."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            return fn(*a, **kw)


def refuses(fn, *a, **kw):
    """(was_refused, ValueError message or the value that came back instead)."""
    try:
        return False, quiet(fn, *a, **kw)
    except ValueError as e:
        return True, str(e)
    except Exception as e:                            # noqa: BLE001 -- classifying
        return False, f"{type(e).__name__}: {e}"


def substrate(J=48, scale=0.05, seed=1):
    th, X = grid(J)
    A = np.random.default_rng(seed).standard_normal((J, J)) * scale
    return th, X, A, HolderNorm(th, X, 1.0, 0.3), HolderNorm(th, X, 1.0, 0.3)


# ---------------------------------------------------------------------------
# 1 -- the structural reason the gap existed, now inverted
# ---------------------------------------------------------------------------

_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "solver", "holder_norms.py")).read()
_tree = ast.parse(_src)
_n_raise = sum(1 for n in ast.walk(_tree) if isinstance(n, ast.Raise))
_names = ({n.attr for n in ast.walk(_tree) if isinstance(n, ast.Attribute)}
          | {n.id for n in ast.walk(_tree) if isinstance(n, ast.Name)})
_guards = sorted(_names & {"isfinite", "isnan", "isinf", "warn", "ValueError"})
_publics = [n.name for n in _tree.body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith("_")]

gate("GUARD: the module now HAS an argument-validation surface",
     _n_raise > 0 and "isfinite" in _guards and "ValueError" in _guards,
     f"{_n_raise} raise sites and finiteness guards {_guards} across {len(_publics)} "
     f"public entry points {sorted(_publics)}.  Leg 100 measured this same count as "
     "**0 raise, 0 assert, no isfinite/isnan/isinf/warn anywhere**, and named it the "
     "structural reason every gate below could find silence: nothing in the module ever "
     "asked whether its arguments were finite.  This gate flipped first, as leg 100 said "
     "it would")


# ---------------------------------------------------------------------------
# 2-5 -- the module's OWN self-validation routine, on a poisoned grid
# ---------------------------------------------------------------------------

_th128, _ = grid(128)
_CLEAN_CONF = conformal_check(_th128, 0.3)
_CLEAN_JAC = jacobian_identity_error(_th128)

gate("ZERO REGRESSION: conformal_check still reproduces the module's own headline, "
     "bit-for-bit",
     _CLEAN_CONF[0] == 1.517287054473293e-04
     and _CLEAN_CONF[1] == 1.9094999985985477
     and _CLEAN_JAC[0] == 5.058518859734074e-04,
     f"on a clean 128-node grid conformal_check = ({_CLEAN_CONF[0]:.15e}, "
     f"{_CLEAN_CONF[1]:.13f}) and jacobian_identity_error = {_CLEAN_JAC[0]:.15e} -- "
     "identical to the last bit to the values leg 100 banked BEFORE the guard existed. "
     "The guard refuses input; it computes nothing and changes no number")

_bad = []
for _i in (7, 64, 120):
    _t = _th128.copy(); _t[_i] = NAN
    _bad.append((_i, refuses(conformal_check, _t, 0.3)))

gate("GUARD: a NaN grid node is now REFUSED by conformal_check "
     "(was bit-identical to clean)",
     all(r[0] for _, r in _bad) and len(_bad) == 3,
     "conformal_check on grids with theta[7], theta[64], theta[120] set to NaN now "
     f"raises ValueError on {sum(1 for _, r in _bad if r[0])}/3.  BEFORE the repair all "
     f"three returned {_CLEAN_CONF[0]:.15e} -- every one bit-identical to the clean "
     "value, deviation exactly 0.0, no NaN, no warning, no exception -- because the mask "
     "`|mid| * dth <= resolved` is an ORDERED comparison and the poisoned pairs "
     "evaluated False and were dropped rather than poisoning the result.  This is the "
     "module's OWN self-validation routine, whose docstring credits it with catching a "
     "wrong seminorm exponent in the first draft, so the routine meant to detect a "
     f"broken discretization certified a broken grid as clean.  Message: "
     f"{_bad[0][1][1][:110]!r}")

_tj = _th128.copy(); _tj[64] = NAN
_jac_ref = refuses(jacobian_identity_error, _tj)
gate("GUARD: the same for the underlying jacobian_identity_error",
     _jac_ref[0],
     "jacobian_identity_error now raises ValueError on the NaN-poisoned grid; before "
     f"the repair it returned {_CLEAN_JAC[0]:.15e}, identical to the clean value to the "
     "last bit")

_allnan = refuses(conformal_check, np.full(16, NAN), 0.3)
gate("GUARD: an ALL-NaN grid is REFUSED (was certified as a PERFECT conformal match)",
     _allnan[0],
     "conformal_check(np.full(16, nan), 0.3) now raises ValueError.  BEFORE the repair "
     "it returned **(0.0, 0.0)** -- worst deviation from the exact conformal identity "
     "0.0, which is the value that means EXACT agreement -- because "
     "`jacobian_identity_error` initialised `worst, xmax = 0.0, 0.0` and `continue`d "
     "past every offset whose resolved-pair mask was empty, so a grid on which NOTHING "
     "was checked was indistinguishable from a grid that passed.  Leg 100 called this "
     "the single worst case in the battery: maximally invalid input, maximally "
     "reassuring output")


# ---------------------------------------------------------------------------
# 6-9 -- family_op_norm: the operator-norm surface
# ---------------------------------------------------------------------------

_th48, _X48, _A, _dn, _cn = substrate()
_CLEAN_OP = family_op_norm(_A, _dn, _cn)

gate("ZERO REGRESSION: family_op_norm on the unpoisoned substrate is unchanged",
     _CLEAN_OP[0] == 661.2075718521894 and _CLEAN_OP[1] == 47,
     f"family_op_norm = ({_CLEAN_OP[0]:.13f}, arg={_CLEAN_OP[1]}) on a seeded 48x48 "
     "operator with matched alpha=1.0, gamma=0.3 norms -- bit-identical to leg 100's "
     "pre-guard baseline")

_op_ref = [refuses(family_op_norm, np.where(
    np.arange(_A.size).reshape(_A.shape) == k, NAN, _A), _dn, _cn)
    for k in (3 * 48 + 7, 0, 47 * 48 + 47)]
gate("GUARD: ONE NaN operator entry is now REFUSED (was a collapse to exactly 0.0)",
     all(r[0] for r in _op_ref),
     f"{sum(1 for r in _op_ref if r[0])}/3 NaN placements in a 48x48 operator now raise "
     f"ValueError.  BEFORE the repair each turned {_CLEAN_OP[0]:.6f} into **0.0** with "
     "arg=-1 -- a 100% collapse, returned as a legitimate finite LOWER bound and "
     "numerically indistinguishable from the answer for the ZERO operator.  Both guards "
     "(`if ng <= 0: continue` and `if r > best`) were ordered comparisons that rejected "
     "every NaN candidate, so control fell through to the initialiser `best, arg = 0.0, "
     "-1`; arg=-1 was the only trace, and it is a sentinel no caller in the repo inspects")

_g_a = np.exp(-_X48 ** 2)
_g_b = np.exp(-0.25 * _X48 ** 2) * np.cos(_th48)
_r_a = _dn(_A @ _g_a) / _cn(_g_a)
_r_b = _dn(_A @ _g_b) / _cn(_g_b)
_hi, _lo = (_g_a, _g_b) if _r_a > _r_b else (_g_b, _g_a)
_r_hi, _r_lo = max(_r_a, _r_b), min(_r_a, _r_b)
_two_clean = family_op_norm(_A, _dn, _cn, extra=[_lo, _hi], include_sup_extremizers=False)
_poisoned = _hi.copy(); _poisoned[len(_hi) // 2] = NAN
_two_ref = refuses(family_op_norm, _A, _dn, _cn, extra=[_lo, _poisoned],
                   include_sup_extremizers=False)

gate("GUARD: a poisoned TRUE MAXIMIZER is now REFUSED (was silently replaced by the "
     "runner-up)",
     _two_ref[0] and abs(_two_clean[0] - _r_hi) < 1e-9,
     f"with two clean test vectors family_op_norm returns {_two_clean[0]:.6f} (arg="
     f"{_two_clean[1]}, the maximizer), unchanged by the repair.  Put ONE NaN into that "
     "same maximizer and the call now raises ValueError.  BEFORE the repair it returned "
     f"{_r_lo:.6f} -- the RUNNER-UP -- a factor {_r_hi / _r_lo:.4f} understatement of "
     "the module's own lower bound, finite, plausible, and with arg pointing at a "
     "perfectly legitimate clean test vector.  Nothing in the return value recorded that "
     "a test function had been discarded.  Leg 100 called this the sharpest case in the "
     "battery: unlike the 0.0 collapse above, the returned number carried no tell at all")

_full_clean = family_op_norm(_A, _dn, _cn, extra=[_lo, _hi])
_full_ref = refuses(family_op_norm, _A, _dn, _cn, extra=[_lo, _poisoned])
gate("GUARD: a poisoned vector inside the FULL family is refused too (was invisible)",
     _full_ref[0] and _full_clean == _CLEAN_OP,
     "with the sup extremizers on, the poisoned extra now raises ValueError.  BEFORE "
     f"the repair it changed nothing at all: {_full_clean[0]!r} both ways, "
     "bit-identical, so a caller who supplied a corrupt test family got exactly the same "
     "number as one who supplied a clean one")


# ---------------------------------------------------------------------------
# 10-11 -- the EMBEDDING CONSTANT surface
# ---------------------------------------------------------------------------

_CLEAN_PD, _CLEAN_RB = holder_H_constant(_th128, 0.3, degrees=(4, 16, 64), n_random=60)
gate("ZERO REGRESSION: the Holder-Hilbert embedding constant is unchanged",
     _CLEAN_RB == 0.8914207747116539 and len(_CLEAN_PD) == 3
     and all(np.isfinite(x) for x in _CLEAN_PD),
     f"holder_H_constant(gamma=0.3) = per_degree {[round(x, 6) for x in _CLEAN_PD]}, "
     f"random_best {_CLEAN_RB:.16f} -- bit-identical to leg 100's pre-guard baseline")

_hc = {}
for _lab, _tt, _gg in (("gamma=NaN", _th128, NAN),
                       ("gamma=-0.3", _th128, -0.3),
                       ("theta[7]=NaN", (lambda t: (t.__setitem__(7, NAN), t)[1])(_th128.copy()), 0.3),
                       ("theta[7]=+Inf", (lambda t: (t.__setitem__(7, INF), t)[1])(_th128.copy()), 0.3)):
    _hc[_lab] = refuses(holder_H_constant, _tt, _gg, degrees=(4, 16, 64), n_random=60)

gate("GUARD: holder_H_constant REFUSES all four poisoned inputs (its random arm used to "
     "report an embedding constant of exactly 0.0)",
     all(r[0] for r in _hc.values()) and len(_hc) == 4,
     f"{sum(1 for r in _hc.values() if r[0])}/4 of {sorted(_hc)} now raise ValueError.  "
     "BEFORE the repair the random arm returned **0.0** on every one of them, against a "
     f"clean {_CLEAN_RB:.6f}: `if den > 0` rejected the NaN denominators and python's "
     "BUILTIN `max(best, x)` returns `best` when `x` is NaN (`nan > best` is False), so "
     "`best` never left its 0.0 initialiser.  A caller reading only the random arm was "
     "told the Hilbert transform has Holder operator constant ZERO -- that it "
     "annihilates the space -- the most consequential wrong answer this module can give. "
     "The per-degree arm of the SAME function returned all-NaN on the same inputs, so "
     "the two arms disagreed about whether the input was valid; now neither answers")


# ---------------------------------------------------------------------------
# 12-13 -- the weight-class exponents and the grid, at the constructor
# ---------------------------------------------------------------------------

_th64, _X64 = grid(64)
_h = 1.0 / (1.0 + _X64 ** 2)
_clean_n = HolderNorm(_th64, _X64, 1.0, 0.3)
_CLEAN_TRIPLE = (_clean_n.sup_part(_h), _clean_n.seminorm(_h), _clean_n(_h))

_prop = {
    "alpha=NaN": refuses(HolderNorm, _th64, _X64, NAN, 0.3),
    "gamma=NaN": refuses(HolderNorm, _th64, _X64, 1.0, NAN),
    "gamma=-0.5": refuses(HolderNorm, _th64, _X64, 1.0, -0.5),
    "semi_alpha=NaN": refuses(HolderNorm, _th64, _X64, 1.0, 0.3, semi_alpha=NAN),
}
gate("GUARD: every poisoned weight-class exponent is REFUSED at the constructor",
     all(r[0] for r in _prop.values()),
     f"{sum(1 for r in _prop.values() if r[0])}/4 of {sorted(_prop)} now raise "
     f"ValueError (clean total norm {_CLEAN_TRIPLE[2]:.6f}, unchanged).  BEFORE the "
     "repair all four reached the caller as a NaN total norm -- honest, but only because "
     "the reductions here happen to be `np.max`; the SAME poisoned grid was invisible to "
     "conformal_check, which filters instead of maximising.  Rejecting at the door "
     "removes the dependence on which reduction a given consumer happens to use")

_pg_ref = refuses(lambda: HolderNorm(
    _th64, (lambda x: (x.__setitem__(30, NAN), x)[1])(_X64.copy()), 1.0, 0.3))
gate("GUARD: a NaN grid node is REFUSED at the constructor",
     _pg_ref[0],
     "HolderNorm with X[30] = NaN now raises ValueError; before the repair it returned "
     "a NaN triple.  Note the contrast leg 100 drew with gate 3: the SAME poisoned grid "
     "was fatal to the norm and invisible to conformal_check.  After the repair both "
     "refuse it, for the same stated reason")

_w_ref = refuses(decay_weight, np.array([0.0, 1.0, 10.0]), NAN)
gate("GUARD: the latent pow(1.0, NaN) = 1.0 trap is REFUSED before it can go live",
     _w_ref[0],
     "decay_weight([0, 1, 10], alpha=NaN) now raises ValueError.  BEFORE the repair it "
     "returned **[1.0, nan, nan]**: the node X = 0 kept a weight of exactly 1.0 by the "
     "IEEE-754 `pow(1.0, NaN) = 1.0` special case while every other node went NaN.  Leg "
     "100 recorded this as LATENT, harmless only because the sup over the grid still saw "
     "the other NaNs, and flagged that it would go live the moment anything evaluated "
     "the weight at a single origin node.  It is now refused rather than left to decay "
     "at the rate of memory")


# ---------------------------------------------------------------------------
# 14-16 -- the SEVENTH mechanism: the builtin-max hazard with NO NaN in the input
# ---------------------------------------------------------------------------

_dup = _th128.copy(); _dup[64] = _dup[63]
_dup_ref = refuses(jacobian_identity_error, _dup)
gate("GUARD (7th mechanism, found by the repair): a REPEATED grid node is REFUSED",
     _dup_ref[0],
     "jacobian_identity_error on a 128-node grid with theta[64] = theta[63] now raises "
     "ValueError.  BEFORE the repair it returned **8.127828757138467e-04** against a "
     f"clean {_CLEAN_JAC[0]:.15e} -- a factor "
     f"{8.127828757138467e-04 / _CLEAN_JAC[0]:.4f} change, finite and plausible and "
     "carrying no tell.  Mechanism: dth = 0 at that pair gives a 0/0 finite difference "
     "whose offset-1 contribution is NaN, and `worst = max(worst, ...)` is python's "
     "BUILTIN max, so `max(0.0, nan)` returned 0.0 and DELETED the entire finest offset "
     "from the maximum.  This is leg 100's mechanism 5 hazard at a site leg 100 "
     "attributed only to holder_H_constant, and it is reachable with **no NaN anywhere "
     "in the input**")

_dupc_ref = refuses(conformal_check, _dup, 0.3)
gate("GUARD (7th mechanism): conformal_check on the same repeated-node grid is REFUSED",
     _dupc_ref[0],
     "conformal_check now raises ValueError; before the repair it returned "
     f"2.4376552996407952e-04 against a clean {_CLEAN_CONF[0]:.15e}, a factor "
     f"{2.4376552996407952e-04 / _CLEAN_CONF[0]:.4f} change")

_desc_ref = refuses(jacobian_identity_error, _th128[::-1].copy())
gate("GUARD (7th mechanism): a DESCENDING grid is REFUSED",
     _desc_ref[0],
     "jacobian_identity_error on the reversed 128-node grid now raises ValueError.  "
     "BEFORE the repair it returned (9.735756699671507e-01, **1019.8141148113144**) "
     f"against a clean ({_CLEAN_JAC[0]:.9e}, {_CLEAN_JAC[1]:.9f}).  Mechanism: a "
     "descending grid makes dth < 0, which satisfies the ordered comparison `|mid| * "
     "dth <= resolved` for EVERY pair and so switches the resolution restriction off "
     f"entirely -- the reported far-field coverage was overstated by a factor "
     f"{1019.8141148113144 / _CLEAN_JAC[1]:.1f}x, and test_holder_norms.py prints that "
     "coverage as 'verified out to X=...'")


# ---------------------------------------------------------------------------
# 17 -- what was NEVER broken, and must not have been broken BY the repair
# ---------------------------------------------------------------------------

_hbad = _h.copy(); _hbad[30] = NAN
_dtriple = quiet(lambda: (_clean_n.sup_part(_hbad), _clean_n.seminorm(_hbad),
                          _clean_n(_hbad)))
gate("NOT BROKEN (and must never flip): the norms still PROPAGATE NaN out of the "
     "caller's DATA vector",
     all(np.isnan(x) for x in _dtriple),
     f"a clean HolderNorm applied to a data vector h with h[30] = NaN returns "
     f"{_dtriple} -- all NaN, propagated honestly through `np.max`, against a clean "
     f"total {_CLEAN_TRIPLE[2]:.6f}.  The repair validates the GRID and the EXPONENTS "
     "at construction and deliberately does NOT validate `h` on every call: that path "
     "was already correct, and scanning h would put an O(J^2) check inside "
     "family_op_norm's inner loop to replace a right answer.  This gate exists so the "
     "repair cannot quietly convert propagation into silence")

_zero_op = family_op_norm(np.zeros((48, 48)), _dn, _cn)
gate("NOT BROKEN: the legitimate zero-norm paths still work",
     _zero_op == (0.0, -1),
     f"family_op_norm on the ZERO operator still returns {_zero_op} -- 0.0 with the "
     "arg=-1 sentinel, which is the CORRECT answer there (every sup-part extremizer is "
     "the zero vector, so no candidate carries information).  The `if ng <= 0: continue` "
     "filter survived the repair on purpose: it now has a reason it can STATE, rather "
     "than dropping candidates merely because a comparison against NaN was False")


# ---------------------------------------------------------------------------
# 18 -- NO FALSE REJECTION: the guard must not reject legitimate input
# ---------------------------------------------------------------------------

_valid, _rejected = 0, []
for _a, _g in [(0.0, 0.5), (1.5, 0.4), (1.5, 0.5), (2.5, 0.5), (1.0, 0.3), (0.0, 0.15),
               (0.0, 0.85), (1.5, 0.05), (1.5, 0.9), (-1.0, 0.5), (3.0, 0.5)]:
    _valid += 1
    try:
        HolderNorm(_th64, _X64, _a, _g)(_h)
    except Exception as e:                            # noqa: BLE001 -- classifying
        _rejected.append((f"alpha={_a}, gamma={_g}", str(e)[:60]))
for _J in (8, 16, 64, 128, 300):
    _valid += 1
    try:
        jacobian_identity_error(grid(_J)[0])
    except Exception as e:                            # noqa: BLE001 -- classifying
        _rejected.append((f"J={_J}", str(e)[:60]))
_valid += 1
try:
    _nu = np.sort(np.unique(np.concatenate([np.linspace(-3.0, 3.0, 120),
                                            np.linspace(-0.5, 0.5, 120)])))
    HolderNorm(_nu, np.tan(0.5 * _nu), 1.0, 0.5)(1.0 / (1.0 + np.tan(0.5 * _nu) ** 2))
except Exception as e:                                # noqa: BLE001 -- classifying
    _rejected.append(("non-uniform strictly increasing grid", str(e)[:60]))

gate("NO FALSE REJECTION: every legitimate configuration is still accepted",
     not _rejected,
     f"{_valid - len(_rejected)}/{_valid} valid configurations pass the guard silently: "
     "every (alpha, gamma) pair used anywhere in this repository (gamma spans "
     "0.05..0.9, alpha spans -1.0..3.0), grids from J=8 to J=300, and a non-uniform but "
     "strictly increasing grid (the guard demands ordering, NOT uniformity).  "
     f"Rejections: {_rejected}.  A guard that is too aggressive is a new correctness bug "
     "sitting on top of a fix; the repair's own A/B checks 46 such configurations and "
     "53 clean calls for bit-identity (bench_holder_norms_nan_guard_check.py)")


# ---------------------------------------------------------------------------
# 19 -- POSITIVE CONTROL: the harness can see a signal
# ---------------------------------------------------------------------------

_ctl = []
_n32 = HolderNorm(*grid(32), 1.0, 0.3)
for _lab, _fn, _args in (
    ("norm on a wrong-length vector", _n32, (np.ones(33),)),
    ("family_op_norm on a non-conforming operator", family_op_norm,
     (np.ones((32, 35)), _n32, _n32)),
    ("square_wave_partial_sum with m = NaN", square_wave_partial_sum, (grid(32)[0], NAN)),
    ("holder_H_constant with a grid smaller than its random degrees",
     holder_H_constant, (grid(32)[0], 0.3)),
):
    try:
        quiet(_fn, *_args)
        _ctl.append((_lab, None))
    except Exception as e:                            # noqa: BLE001 -- classifying
        _ctl.append((_lab, type(e).__name__))

gate("POSITIVE CONTROL: structurally malformed calls DO raise",
     all(t is not None for _, t in _ctl),
     f"{len([1 for _, t in _ctl if t])}/{len(_ctl)} malformed calls raise "
     f"{sorted({t for _, t in _ctl if t})}.  Every refusal pinned above is the module's "
     "own, not this harness's.  The last case is now the module's OWN error rather than "
     "an incidental numpy shape error: holder_H_constant's random family draws degrees "
     "up to 63 and contracts against a (J x J) basis, so it is only callable on grids "
     "with J >= 64 -- a precondition leg 100 found enforced by numpy and documented "
     "nowhere, and which the repair states and checks explicitly")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("NOTE: leg 100's gate answered YES, and the bench repair CLOSED it.  This file was "
      "inverted, not weakened: every magnitude leg 100 measured is retained above as the "
      "value the module USED to return, and each gate now asserts that the same call is "
      "refused.  Gates 17-18 are the ones that must never flip -- they pin that the "
      "repair did not convert honest NaN propagation into silence, and that it does not "
      "reject legitimate input.")
sys.exit(1 if n_fail else 0)
