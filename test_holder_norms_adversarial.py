"""ADVERSARIAL gates for solver/holder_norms.py -- Route-HNA, leg 100.

`test_holder_norms.py` (the module's own file) tests that the module MEASURES correctly on
well-formed input: the norm axioms, the conformal identity, the embedding constants.  This
file tests what the module SAYS when the caller hands it input that is not well-formed --
a NaN or Inf in a weight-class parameter or a grid node, or a degenerate grading exponent.
`capabilities.py`'s validated line for the module covers "norm axioms and the embedding
constants", and that line is about correctness ON well-formed inputs; it makes no claim
about behaviour off them.  This file measures the off-window behaviour.

**Leg 100's gate answered YES: the module has a silent-corruption gap, in six distinct
places.**  `solver/holder_norms.py` was NOT patched under leg 100 (territory rule -- the
leg was authorised to audit, not to repair), so every gate below **pins the current
silence deliberately and will FAIL the day a guard lands.  Invert them then, do not weaken
them** -- exactly what leg 84's file did for `solver/target_norm.py` when its guard landed.

The mechanism is a single documented IEEE-754 hazard, instantiated five times: **every NaN
compares unordered, so an ordered comparison used as a filter silently DROPS the poisoned
item instead of propagating it.**  The four filters are

  * `jacobian_identity_error`  : `ok = |mid| * dth <= resolved`   (line ~126)
  * `family_op_norm`           : `if ng <= 0: continue`           (line ~183)
  * `family_op_norm`           : `if r > best:`                   (line ~186)
  * `holder_H_constant`        : `if den > 0:` and `max(best, .)` (line ~246)

plus one initialiser that survives an empty filter as a plausible answer:
`jacobian_identity_error`'s `worst, xmax = 0.0, 0.0`, where 0.0 means EXACT agreement.

WHAT IS NOT BROKEN, and is pinned as such: the norm objects themselves.  `HolderNorm`'s
sup part, seminorm and total all reduce through `np.max`, which DOES propagate NaN, so a
poisoned exponent or a poisoned grid node reaches the caller as NaN (gates 9-11).

Magnitudes, not booleans: every gate asserts the number the module returned against the
number the same call returns on clean input.  Full battery and JSON:
`experiments/p2_route_hna_v1_adversarial.py`, `writeup/data/p2_route_hna_v1_adversarial.json`.
Novelty pass (all of this is a KNOWN hazard, none of it is claimed as a discovery):
`writeup/novelty/leg_100.md`.
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


def substrate(J=48, scale=0.05, seed=1):
    th, X = grid(J)
    A = np.random.default_rng(seed).standard_normal((J, J)) * scale
    return th, X, A, HolderNorm(th, X, 1.0, 0.3), HolderNorm(th, X, 1.0, 0.3)


# ---------------------------------------------------------------------------
# 1 -- the structural reason: the module has no validation surface at all
# ---------------------------------------------------------------------------

_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "solver", "holder_norms.py")).read()
_tree = ast.parse(_src)
_n_raise = sum(1 for n in ast.walk(_tree) if isinstance(n, ast.Raise))
_n_assert = sum(1 for n in ast.walk(_tree) if isinstance(n, ast.Assert))
_names = ({n.attr for n in ast.walk(_tree) if isinstance(n, ast.Attribute)}
          | {n.id for n in ast.walk(_tree) if isinstance(n, ast.Name)})
_guards = sorted(_names & {"isfinite", "isnan", "isinf", "warn", "ValueError"})
_publics = [n.name for n in _tree.body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith("_")]

gate("GAP PIN: the module has zero argument-validation sites",
     _n_raise == 0 and _n_assert == 0 and _guards == [],
     f"{_n_raise} raise, {_n_assert} assert, finiteness guards {_guards} across "
     f"{len(_publics)} public entry points {sorted(_publics)}.  This is the structural "
     "reason gates 2-8 can find silence: nothing in the module ever asks whether its "
     "arguments are finite.  When a guard lands, this gate flips first")


# ---------------------------------------------------------------------------
# 2-4 -- the module's OWN self-validation routine, on a poisoned grid
# ---------------------------------------------------------------------------

_th128, _ = grid(128)
_CLEAN_CONF = conformal_check(_th128, 0.3)
_CLEAN_JAC = jacobian_identity_error(_th128)

gate("clean baseline: conformal_check reproduces the module's own headline",
     abs(_CLEAN_CONF[0] - 1.517287054473293e-04) < 1e-15
     and abs(_CLEAN_CONF[1] - 1.9094999985985477) < 1e-12,
     f"on a clean 128-node grid conformal_check = ({_CLEAN_CONF[0]:.9e}, "
     f"{_CLEAN_CONF[1]:.9f}); every poisoned value below is measured against THIS")

_bad = []
for _i in (7, 64, 120):
    _t = _th128.copy(); _t[_i] = NAN
    _bad.append((_i, quiet(conformal_check, _t, 0.3)))

gate("GAP PIN (silent): a NaN grid node leaves conformal_check BIT-IDENTICAL to clean",
     all(v[0] == _CLEAN_CONF[0] and v[1] == _CLEAN_CONF[1] for _, v in _bad),
     "conformal_check on grids with theta[7], theta[64], theta[120] set to NaN returns "
     f"{[float(v[0]) for _, v in _bad]} -- every one bit-identical to the clean "
     f"{_CLEAN_CONF[0]:.9e}, deviation exactly 0.0, no NaN, no warning, no exception.  "
     "The mask `|mid| * dth <= resolved` is an ORDERED comparison, so the poisoned pairs "
     "evaluate False and are dropped from the average instead of poisoning it.  This is "
     "the module's OWN self-validation routine -- its docstring credits conformal_check "
     "with catching a wrong seminorm exponent in the first draft -- so the routine that "
     "is supposed to detect a broken discretization certifies a broken grid as clean")

_tj = _th128.copy(); _tj[64] = NAN
_jac_bad = quiet(jacobian_identity_error, _tj)
gate("GAP PIN (silent): the same for the underlying jacobian_identity_error",
     _jac_bad[0] == _CLEAN_JAC[0] and _jac_bad[1] == _CLEAN_JAC[1],
     f"jacobian_identity_error returns {_jac_bad[0]:.9e} on the NaN-poisoned grid vs "
     f"{_CLEAN_JAC[0]:.9e} clean -- identical to the last bit")

_allnan = quiet(conformal_check, np.full(16, NAN), 0.3)
gate("GAP PIN (silent): an ALL-NaN grid is certified as a PERFECT conformal match",
     _allnan == (0.0, 0.0),
     f"conformal_check(np.full(16, nan), 0.3) returns {_allnan} -- worst deviation from "
     "the exact conformal identity = 0.0, which is the value that means EXACT agreement. "
     "`jacobian_identity_error` initialises `worst, xmax = 0.0, 0.0` and `continue`s past "
     "every offset whose resolved-pair mask is empty, so a grid on which NOTHING was "
     "checked is indistinguishable from a grid that passed.  This is the single worst "
     "case in the battery: maximally invalid input, maximally reassuring output")


# ---------------------------------------------------------------------------
# 5-7 -- family_op_norm: the operator-norm surface
# ---------------------------------------------------------------------------

_th48, _X48, _A, _dn, _cn = substrate()
_CLEAN_OP = family_op_norm(_A, _dn, _cn)

gate("clean baseline: family_op_norm on the unpoisoned substrate",
     abs(_CLEAN_OP[0] - 661.2075718521894) < 1e-9 and _CLEAN_OP[1] == 47,
     f"family_op_norm = ({_CLEAN_OP[0]:.9f}, arg={_CLEAN_OP[1]}) on a seeded 48x48 "
     "operator with matched alpha=1.0, gamma=0.3 norms")

_op_nan = [quiet(lambda P=p: family_op_norm(P, _dn, _cn))
           for p in [np.where(np.arange(_A.size).reshape(_A.shape) == k, NAN, _A)
                     for k in (3 * 48 + 7, 0, 47 * 48 + 47)]]
gate("GAP PIN (silent): ONE NaN entry collapses family_op_norm to exactly 0.0",
     all(v == (0.0, -1) for v in _op_nan),
     f"a single NaN anywhere in a 48x48 operator turns {_CLEAN_OP[0]:.6f} into "
     f"{[v[0] for v in _op_nan]} with arg=-1 -- a %.0f%% collapse, returned as a "
     "legitimate finite lower bound and numerically indistinguishable from the answer "
     "for the ZERO operator.  Both guards (`if ng <= 0: continue` and `if r > best`) are "
     "ordered comparisons that reject every NaN candidate, so control falls through to "
     "the initialiser `best, arg = 0.0, -1`.  arg=-1 is the only trace, and it is a "
     "sentinel no caller in the repo inspects" % (100.0,))

_g_a = np.exp(-_X48 ** 2)
_g_b = np.exp(-0.25 * _X48 ** 2) * np.cos(_th48)
_r_a = _dn(_A @ _g_a) / _cn(_g_a)
_r_b = _dn(_A @ _g_b) / _cn(_g_b)
_hi, _lo = (_g_a, _g_b) if _r_a > _r_b else (_g_b, _g_a)
_r_hi, _r_lo = max(_r_a, _r_b), min(_r_a, _r_b)
_two_clean = family_op_norm(_A, _dn, _cn, extra=[_lo, _hi], include_sup_extremizers=False)
_poisoned = _hi.copy(); _poisoned[len(_hi) // 2] = NAN
_two_bad = quiet(family_op_norm, _A, _dn, _cn, extra=[_lo, _poisoned],
                 include_sup_extremizers=False)

gate("GAP PIN (silent): a poisoned TRUE MAXIMIZER is dropped and the runner-up is "
     "reported as the answer",
     abs(_two_clean[0] - _r_hi) < 1e-9 and abs(_two_bad[0] - _r_lo) < 1e-9
     and _two_bad[1] == 0 and np.isfinite(_two_bad[0]),
     f"with two clean test vectors family_op_norm returns {_two_clean[0]:.6f} (arg="
     f"{_two_clean[1]}, the maximizer).  Put ONE NaN into that same maximizer and it "
     f"returns {_two_bad[0]:.6f} (arg={_two_bad[1]}, the runner-up) -- a factor "
     f"{_r_hi / _r_lo:.4f} understatement of the module's own lower bound, finite, "
     "plausible, and pointing at a perfectly legitimate clean test vector.  Nothing in "
     "the return value records that a test function was discarded.  This is the sharpest "
     "case in the battery: unlike the 0.0 collapse above, the returned number carries no "
     "tell at all")

_full_clean = family_op_norm(_A, _dn, _cn, extra=[_lo, _hi])
_full_bad = quiet(family_op_norm, _A, _dn, _cn, extra=[_lo, _poisoned])
gate("GAP PIN (silent): inside the full family the poisoned vector is invisible",
     _full_bad == _full_clean,
     f"with the sup extremizers on, the poisoned extra changes nothing: {_full_bad[0]!r} "
     f"vs {_full_clean[0]!r} clean, bit-identical.  A caller who supplies a corrupt test "
     "family gets the same number as one who supplies a clean one")


# ---------------------------------------------------------------------------
# 8 -- the EMBEDDING CONSTANT surface
# ---------------------------------------------------------------------------

_CLEAN_PD, _CLEAN_RB = holder_H_constant(_th128, 0.3, degrees=(4, 16, 64), n_random=60)
gate("clean baseline: the Holder-Hilbert embedding constant",
     abs(_CLEAN_RB - 0.8914207747116539) < 1e-9 and len(_CLEAN_PD) == 3
     and all(np.isfinite(x) for x in _CLEAN_PD),
     f"holder_H_constant(gamma=0.3) = per_degree {[round(x, 6) for x in _CLEAN_PD]}, "
     f"random_best {_CLEAN_RB:.9f}")

_hc = {}
for _lab, _tt, _gg in (("gamma=NaN", _th128, NAN),
                       ("gamma=-0.3", _th128, -0.3),
                       ("theta[7]=NaN", (lambda t: (t.__setitem__(7, NAN), t)[1])(_th128.copy()), 0.3),
                       ("theta[7]=+Inf", (lambda t: (t.__setitem__(7, INF), t)[1])(_th128.copy()), 0.3)):
    _hc[_lab] = quiet(holder_H_constant, _tt, _gg, degrees=(4, 16, 64), n_random=60)

gate("GAP PIN (silent): holder_H_constant's random arm returns an embedding constant of "
     "exactly 0.0 on every poisoned input",
     all(v[1] == 0.0 for v in _hc.values()) and len(_hc) == 4,
     "on {NaN grading exponent, negative grading exponent, NaN grid node, Inf grid node} "
     f"the second return value is {[v[1] for v in _hc.values()]}, against a clean "
     f"{_CLEAN_RB:.6f}.  `if den > 0` rejects the NaN denominators and python's builtin "
     "`max(best, x)` returns `best` when `x` is NaN (`NaN > best` is False), so `best` "
     "never leaves its 0.0 initialiser.  A caller reading only the random arm is told "
     "the Hilbert transform has Holder operator constant ZERO -- i.e. that it annihilates "
     "the space -- which is the most consequential wrong answer this module can give")

gate("NOT BROKEN: holder_H_constant's per-degree arm DOES propagate",
     all(all(np.isnan(x) for x in v[0]) for v in _hc.values()),
     "the adversarial per-degree arm is a plain list comprehension with no filter, so it "
     f"returns {[float(v[0][0]) for v in _hc.values()]} -- all NaN -- on the same four "
     "inputs.  The two arms of ONE function disagree about whether the input was valid, "
     "which is what makes the random arm's silence a latent trap rather than an obvious "
     "one: a caller who checks the first return value is protected and a caller who "
     "checks the second is not")


# ---------------------------------------------------------------------------
# 9-11 -- what is NOT broken: the norms themselves
# ---------------------------------------------------------------------------

_th64, _X64 = grid(64)
_h = 1.0 / (1.0 + _X64 ** 2)
_clean_n = HolderNorm(_th64, _X64, 1.0, 0.3)
_CLEAN_TRIPLE = (_clean_n.sup_part(_h), _clean_n.seminorm(_h), _clean_n(_h))


def _triple(alpha, gamma, **kw):
    n = quiet(HolderNorm, _th64, _X64, alpha, gamma, **kw)
    return quiet(lambda: (n.sup_part(_h), n.seminorm(_h), n(_h)))


_prop = {
    "alpha=NaN": _triple(NAN, 0.3),
    "gamma=NaN": _triple(1.0, NAN),
    "gamma=-0.5": _triple(1.0, -0.5),
    "semi_alpha=NaN": _triple(1.0, 0.3, semi_alpha=NAN),
}
gate("NOT BROKEN: HolderNorm propagates NaN out of every poisoned weight-class exponent",
     all(np.isnan(v[2]) for v in _prop.values()),
     "alpha=NaN, gamma=NaN, gamma=-0.5 and semi_alpha=NaN all reach the caller as a NaN "
     f"total norm (clean total {_CLEAN_TRIPLE[2]:.6f}); the reductions are `np.max`, "
     "which propagates, unlike the python builtin `max` in holder_H_constant.  The "
     "difference between gate 8 and this one is one function call name")


def _poisoned_grid_triple():
    tX = _X64.copy(); tX[30] = NAN
    n = HolderNorm(_th64, tX, 1.0, 0.3)
    return (n.sup_part(_h), n.seminorm(_h), n(_h))


_pg = quiet(_poisoned_grid_triple)
gate("NOT BROKEN: a NaN grid node reaches the caller through the norm",
     all(np.isnan(x) for x in _pg),
     f"HolderNorm with X[30] = NaN returns {_pg} -- the sup part alone is enough to "
     "propagate.  Note the contrast with gate 2: the SAME poisoned grid is invisible to "
     "conformal_check and fatal to the norm, because one filters and the other maximises")

_w = decay_weight(np.array([0.0, 1.0, 10.0]), NAN)
gate("LATENT (not live): pow(1.0, NaN) = 1.0 keeps an exactly-unit weight at X = 0",
     _w[0] == 1.0 and np.isnan(_w[1]) and np.isnan(_w[2]),
     f"decay_weight([0, 1, 10], alpha=NaN) = {list(_w)}: the node X = 0 keeps weight "
     "exactly 1.0 by the IEEE-754 pow special case, while every other node goes NaN.  "
     "Harmless TODAY only because the sup over the grid still sees the NaNs -- it would "
     "become live the moment anything evaluates the weight at a single origin node.  "
     "Pinned so it cannot decay at the rate of memory")


# ---------------------------------------------------------------------------
# 12 -- the Inf twins, and how wide the one signal actually is
# ---------------------------------------------------------------------------

_t_inf = _th128.copy(); _t_inf[64] = INF
_seen, _vals = [], []
with warnings.catch_warnings(record=True) as _caught:
    warnings.simplefilter("default")             # the interpreter's OWN default policy
    for _k in range(3):
        _before = len(_caught)
        _vals.append(conformal_check(_t_inf, 0.3))
        _seen.append(len(_caught) - _before)

gate("GAP PIN: the Inf cases are 'flagged' only by an incidental RuntimeWarning that "
     "stops firing on the second call",
     _seen[0] > 0 and _seen[1] == 0 and _seen[2] == 0
     and all(v == _CLEAN_CONF for v in _vals),
     f"conformal_check on an Inf-poisoned grid emits {_seen} warnings over three "
     f"identical calls and returns {[float(v[0]) for v in _vals]} every time -- the "
     f"clean value {_CLEAN_CONF[0]:.9e}, unchanged.  The warning is numpy's, not the "
     "module's, and python's default filter shows it once per source location, so in any "
     "caller that has already touched this line the Inf case is exactly as silent as the "
     "NaN case.  The NaN/Inf distinction the other gates record is one warning wide")


# ---------------------------------------------------------------------------
# 13 -- POSITIVE CONTROL: the harness can see a signal
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
    except Exception as e:                        # noqa: BLE001 -- classifying
        _ctl.append((_lab, type(e).__name__))

gate("POSITIVE CONTROL: structurally malformed calls DO raise",
     all(t is not None for _, t in _ctl),
     f"{len([1 for _, t in _ctl if t])}/{len(_ctl)} malformed calls raise "
     f"{sorted({t for _, t in _ctl if t})} -- shape and dtype errors surface from numpy "
     "on their own.  Every silence pinned above is the module's, not this harness's.  "
     "Note what the last one means in practice: holder_H_constant's random family draws "
     "degrees up to 63 and matmuls against a (J x J) basis, so it is only callable at "
     "all on grids with J >= 64 -- an undocumented precondition enforced by a ValueError "
     "from numpy rather than by the module")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("NOTE: leg 100's gate answered YES.  Gates 2-8 and 12 pin a CURRENT silent-"
      "corruption gap in solver/holder_norms.py that leg 100 was not authorised to "
      "repair; they assert the module's present (wrong) behaviour on purpose and will "
      "FAIL the day a finiteness guard lands.  Invert them then -- keep every magnitude "
      "and flip only the sign of the SIGNAL claim -- exactly as leg 84 did for "
      "solver/target_norm.py.  Gates 9-11 pin what already works and must never flip.")
sys.exit(1 if n_fail else 0)
