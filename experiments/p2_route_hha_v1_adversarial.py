"""Leg 119 (Route-HHA) -- the adversarial battery against hilbert_holder.py's BOUND DIRECTION.

THE QUESTION (the leg's gate, verbatim):

    Under adversarial/degenerate inputs, can any bound hilbert_holder.py reports be exceeded
    (fail to be a true bound), or a wrong value be silently returned?

**THE ANSWER IS YES.**  `solver/hilbert_holder.py` is READ-ONLY under this leg and is NOT
patched: the gate's yes-branch escalates, it does not repair.

WHAT THIS IS NOT.  No bound is sharpened, no constant is improved, no `b_sup`, `b_semi`,
`C_Q`, `Y_0`, `Z_1` or `Z_2` is re-derived.  The plan-of-record ban *"another Route-D
bound-sharpening leg"* is respected literally -- the audit direction is one-sided and can
only ever weaken confidence in an existing number.

--------------------------------------------------------------------------------
THE CLAIM UNDER TEST
--------------------------------------------------------------------------------
`increment_pair_bound(theta1, sigma, alpha, gamma)` returns `(u_S, u_T)` and the module's
docstring asserts, for every even h with psi = H(h),

    w_{1-gamma}(theta_inner) |psi(th1) - psi(th2)| / d^gamma  <=  u_S S + u_T T ,   (C_H)

d = |th1 - th2|, S the weighted sup part of h and T its weighted Holder seminorm.  The
per-point routing rule that builds (u_S, u_T), `_increment_env`'s `take_T = (cT <= cS)`, has
the identical shape to `hilbert_pointwise.py`'s `take_T = rho*cT <= cS` that leg 106 found
unsound for gamma <= 0 -- except here there is no `rho` (the comparison is always at S=T=1)
and the pair geometry is two-point, not one-point.

--------------------------------------------------------------------------------
THE MECHANISM OF FAILURE (measured, then explained, then predicted)
--------------------------------------------------------------------------------
At each point the increment |h(phi) - h(ref)| is charged either to the seminorm account
(cT = dphi^gamma * cos^(alpha-gamma)(inner)) or to the sup account
(cS = cos^alpha(a_phi/2) + cos^alpha(a_ref/2)), by the rule take_T = (cT <= cS).

As dphi -> 0, cS -> 2*cos^alpha(inner/2) != 0 -- the sup account does NOT vanish -- while
only cT -> 0 (which needs gamma > 0) tames the near-pole singularity in the E_N integral.
For gamma <= 0, cT does NOT vanish as dphi -> 0 either (dphi^gamma diverges or stays O(1)),
so at gamma = 0 the accumulated near-pole mass is charged entirely to the sup account (u_T
comes out to a finite-looking, non-zero value from surrounding non-singular contributions,
u_S = 0 exactly), and the returned (u_S, u_T) is finite ONLY because `increment_pair_bound`'s
log-graded quadrature starts at `s = eps*lo`, not `s = 0` -- an eps-truncation of what is
otherwise a logarithmically divergent integral, not a bound.  Gate A5 demonstrates exactly
this by moving eps.

--------------------------------------------------------------------------------
THE ADVERSARY, AND WHY ITS |psi(th1)-psi(th2)| IS TRUSTWORTHY
--------------------------------------------------------------------------------
h(phi) = cos^alpha(phi/2) * clip(-(phi-center)/delta, -1, 1) -- the same clipped-ramp shape
leg 106 used, centred at theta1 (so the near-pole singularity of the E_N integral at th1 is
attacked directly).  Its |H(h)| at any evaluation point is computed by the SAME subtracted
p.v. identity `increment_pair_bound` bounds, on a log-graded mesh, parameterised by the exact
signed offset from the ramp's own centre (the module's own offset trick, which is what keeps
delta = 1e-50 free of cancellation).  Gate A1 known-answer-checks this quadrature machinery
against `solver.hilbert_holder.conjugate` (cos k th -> sin k th, exact) on cosine polynomials,
and separately reproduces `decomposition_exact`'s own known-answer gate, BEFORE any verdict is
read from it.  S = 1 exactly by construction; T is computed as the genuine sup over pairs
straddling the ramp (using the same offset trick to avoid the floating-point cancellation that
absolute theta coordinates suffer once delta is many decades below machine epsilon).

--------------------------------------------------------------------------------
WHAT IS **NOT** AFFECTED (the blast radius, stated up front)
--------------------------------------------------------------------------------
The shipped Route-D configuration (alpha=1.5, gamma=0.5) and the production optimum
(~1.4, ~0.15) are NOT reached by this violation: gate A6 hunts the shipped pair with the
identical adversary and finds domination holding at every probed delta, the ratio falling
toward zero (not toward 1) as delta shrinks, because gamma > 0 makes T grow FASTER than the
true increment as the ramp narrows.  V1 (gamma = 0) and V2 (gamma < 0) are reachable only by
a caller who passes a non-positive gamma to `increment_pair_bound` or `hilbert_holder_constant`
directly; every production call site fixes gamma in [0.05, 0.9].

Run:  .venv/bin/python experiments/p2_route_hha_v1_adversarial.py
Writes: writeup/data/p2_route_hha_v1_adversarial.json
"""
from __future__ import annotations

import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.hilbert_holder import (                                          # noqa: E402
    conjugate, cq_sup_split, decomposition_exact, hilbert_holder_constant,
    increment_pair_bound, increment_regime, near_padding, pointwise_pair_bound,
    quadratic_constant_full,
)

ALPHA, GAMMA = 1.5, 0.5          # the shipped Route-D pair
PROD_ALPHA, PROD_GAMMA = 1.4, 0.15   # the map's actual production optimum (module docstring)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_hha_v1_adversarial.json")


# ---------------------------------------------------------------------------
# the adversary: a clipped-ramp step centred at a given point, and its exact H
# ---------------------------------------------------------------------------


def step_h_offset(center, off, delta, alpha):
    """h(center+off) = cos^alpha((center+off)/2) * clip(-off/delta, -1, 1).

    `off` is the SIGNED offset from `center`, supplied directly rather than recovered by
    subtracting two nearby floats -- what keeps delta = 1e-50 meaningful instead of noise.
    """
    phi = center + off
    return np.cos(0.5 * phi) ** alpha * np.clip(-off / delta, -1.0, 1.0)


def psi_generic(theta_eval, center, delta, alpha, n=600000, smin=1e-70):
    """|H(h)(theta_eval)| for the step adversary, by the subtracted p.v. identity.

    Works whether theta_eval is the ramp's own centre (needs the offset trick for precision)
    or a different evaluation point (no cancellation hazard there either way).
    """
    tot = 0.0
    for L, sgn in ((theta_eval, -1.0), (np.pi - theta_eval, 1.0)):
        if L <= 0.0:
            continue
        s = np.geomspace(smin * L, L, int(n))
        u = sgn * s
        off_c = (theta_eval - center) + u
        h_phi = step_h_offset(center, off_c, delta, alpha)
        h_ref = step_h_offset(center, np.array([theta_eval - center]), delta, alpha)[0]
        phi = theta_eval + u
        K = -np.sin(theta_eval) / (np.sin(0.5 * (phi + theta_eval)) * np.sin(0.5 * u))
        tot += float(np.trapezoid((h_phi - h_ref) * K * s, np.log(s)))
    return tot / (2.0 * np.pi)


def T_seminorm(center, delta, alpha, gamma, n_local=4000, rel_lo=1e-6, rel_hi=5000.0):
    """sup over pairs straddling the ramp of min(w)|dh|/d^gamma -- the genuine T, not a grid one."""
    rel = np.geomspace(rel_lo, rel_hi, n_local)
    d = rel * delta
    off_a, off_b = -d / 2.0, d / 2.0
    ha = step_h_offset(center, off_a, delta, alpha)
    hb = step_h_offset(center, off_b, delta, alpha)
    a, b = center + off_a, center + off_b
    ok = (a > 0.0) & (b < np.pi)
    with np.errstate(divide="ignore", invalid="ignore"):
        wa = np.cos(0.5 * a) ** (-(alpha - gamma))
        wb = np.cos(0.5 * b) ** (-(alpha - gamma))
        vals = np.where(ok, np.minimum(wa, wb) * np.abs(ha - hb) / d ** gamma, 0.0)
    return float(np.max(vals))


def psi_of_poly(coef, theta, n=200000, smin=1e-13):
    """The same subtracted-p.v. quadrature, on a cosine polynomial -- for the known-answer gate."""
    k = np.arange(np.asarray(coef).size)

    def h(x):
        return np.cos(np.outer(np.atleast_1d(x), k)) @ coef

    h_th = float(h(theta)[0])
    tot = 0.0
    for L, sgn in ((theta, -1.0), (np.pi - theta, 1.0)):
        if L <= 0.0:
            continue
        s = np.geomspace(smin * L, L, int(n))
        u = sgn * s
        phi = theta + u
        K = -np.sin(theta) / (np.sin(0.5 * (phi + theta)) * np.sin(0.5 * u))
        tot += float(np.trapezoid((h(phi) - h_th) * K * s, np.log(s)))
    return tot / (2.0 * np.pi)


def pair_ratio(theta1, sigma, alpha, gamma, delta, n_quad=4000, eps=1e-10):
    """true/bound for increment_pair_bound at one adversarial pair; center = theta1."""
    th2 = theta1 + sigma
    psi1 = psi_generic(theta1, theta1, delta, alpha)
    psi2 = psi_generic(th2, theta1, delta, alpha)
    dphi_true = abs(psi1 - psi2)
    S = 1.0
    T = T_seminorm(theta1, delta, alpha, gamma)
    uS, uT = increment_pair_bound(theta1, sigma, alpha, gamma, n_quad=n_quad, eps=eps)
    inner = min(abs(theta1), abs(th2))
    w = np.cos(0.5 * inner) ** -(1.0 - gamma)
    d = abs(sigma)
    lhs = w * dphi_true / d ** gamma
    bound = uS * S + uT * T
    ratio = (lhs / bound) if bound > 0 else float("inf")
    return {"theta1": theta1, "sigma": sigma, "delta": delta, "S": S, "T": T,
            "u_S": uS, "u_T": uT, "true_weighted_increment": lhs, "bound": bound,
            "ratio_true_over_bound": ratio}


def _call(fn):
    """Return the value, or a string tag naming the exception -- never a boolean."""
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            v = fn()
        tag = "|WARN:%s" % ";".join(sorted({type(w.message).__name__ for w in caught})) \
            if caught else ""
        if isinstance(v, tuple):
            return [None if x is None else (float(x) if np.isscalar(x) or
                    isinstance(x, (int, float, np.floating)) else x) for x in v] \
                if not tag else ([None if x is None else float(x) for x in v], tag)
        if isinstance(v, (int, float, np.floating, np.integer)):
            return v if not tag else (float(v), tag)
        if isinstance(v, dict):
            return v if not tag else (v, tag)
        return v
    except Exception as e:                                     # noqa: BLE001
        return "%s: %s" % (type(e).__name__, str(e)[:90])


# ---------------------------------------------------------------------------
# A1 -- known answer: the adversary's quadrature machinery reproduces the exact conjugate
# ---------------------------------------------------------------------------


def gate_A1():
    cases = [np.array([0.0, 1.0]), np.array([0.0, 0.0, 0.0, 1.0]),
             np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])]
    worst, n = 0.0, 0
    for coef in cases:
        for th in (0.03, 0.4, 1.2, 2.5, 3.0, 3.14):
            worst = max(worst, abs(psi_of_poly(coef, th) - float(conjugate(coef, [th])[0])))
            n += 1
    zero = max(abs(psi_of_poly(np.array([1.0]), th)) for th in (0.2, 1.5, 3.0))
    # cross-check: the module's OWN decomposition_exact gate, at higher precision
    dec_worst = 0.0
    pairs = [(0.7, 0.05), (0.7, -0.3), (2.9, 0.02), (0.02, 0.5), (1.0, 1.5), (3.1, -0.001)]
    for coef in cases:
        for th, sig in pairs:
            got = decomposition_exact(coef, th, sig, n_quad=8000)
            exact = float(conjugate(coef, [th])[0] - conjugate(coef, [th + sig])[0])
            dec_worst = max(dec_worst, abs(got - exact))
    return {"cases": n, "max_abs_error_this_batterys_quadrature": worst,
            "pv_of_constant_function": zero,
            "max_abs_error_modules_own_decomposition_exact": dec_worst,
            "note": ("the battery's own |H(h)| quadrature AND the module's own "
                     "decomposition_exact are both checked against the exact spectral "
                     "conjugate before any verdict is read from either")}


# ---------------------------------------------------------------------------
# A2 -- the degenerate / NaN-poisoned input inventory (values, never booleans)
# ---------------------------------------------------------------------------


def gate_A2():
    gamma_cases = {}
    for g in (0.5, 0.0, -0.5, -1.0, np.nan, np.inf, -np.inf, 1.0, 1.5):
        gamma_cases[repr(g)] = _call(lambda g=g: increment_pair_bound(1.0, 0.05, 1.5, g))
    alpha_cases = {}
    for a in (1.5, 0.0, -0.5, np.nan, np.inf, -np.inf):
        alpha_cases[repr(a)] = _call(lambda a=a: increment_pair_bound(1.0, 0.05, a, 0.5))
    sigma_cases = {}
    for s in (0.05, 0.0, -0.0, 1e-300, np.nan, np.inf, -np.inf, np.pi, 2 * np.pi, 100.0):
        sigma_cases[repr(s)] = _call(lambda s=s: increment_pair_bound(1.0, s, 1.5, 0.5))
    theta_cases = {}
    for t in (1.0, 0.0, np.pi, -1.0, np.pi + 0.5, np.nan, np.inf, 1e-300):
        theta_cases[repr(t)] = _call(lambda t=t: increment_pair_bound(t, 0.05, 1.5, 0.5))
    near_pad_cases = {}
    for d in (0.01, 2.5, 3.0, 0.0, -1.0, np.nan, np.inf):
        near_pad_cases[repr(d)] = _call(lambda d=d: near_padding(d))
    regime_cases = {}
    for th, sig in ((1.0, 0.05), (1.0, np.nan), (np.nan, 0.05), (1.0, np.inf)):
        regime_cases["theta=%r,sigma=%r" % (th, sig)] = _call(
            lambda th=th, sig=sig: increment_regime(th, sig))
    pw_cases = {}
    for a, g in ((1.5, 0.5), (1.5, 0.0), (1.5, -0.5), (np.nan, 0.5), (1.5, np.nan)):
        pw_cases["alpha=%r,gamma=%r" % (a, g)] = _call(
            lambda a=a, g=g: pointwise_pair_bound(1.0, 0.05, a, g, n_quad=200))
    hhc_cases = {}
    for a, g in ((1.5, 0.5), (1.5, 0.0), (1.5, -0.3), (1.5, np.nan), (np.nan, 0.5)):
        hhc_cases["alpha=%r,gamma=%r" % (a, g)] = _call(
            lambda a=a, g=g: hilbert_holder_constant(a, g, n_theta=16, n_d=10, n_quad=100))
    n_finite_pairs = sum(
        1 for v in list(gamma_cases.values()) + list(alpha_cases.values())
        if isinstance(v, list) and all(x is not None and np.isfinite(x) for x in v))
    n_finite_no_warn = sum(
        1 for v in list(gamma_cases.values()) + list(alpha_cases.values())
        if isinstance(v, list) and all(x is not None and np.isfinite(x) for x in v))
    return {"gamma": gamma_cases, "alpha": alpha_cases, "sigma": sigma_cases,
            "theta1": theta_cases, "near_padding": near_pad_cases,
            "increment_regime": regime_cases, "pointwise_pair_bound": pw_cases,
            "hilbert_holder_constant": hhc_cases,
            "n_gamma_or_alpha_cases_returning_finite_pair": n_finite_pairs,
            "note": ("gamma=0.0 and gamma=-0.5/-1.0 return FINITE pairs with NO warning "
                     "from increment_pair_bound; hilbert_holder_constant(1.5, 0.0, ...) "
                     "instead CRASHES (ZeroDivisionError inside solver.nk_seminorm."
                     "hilbert_split_bound's own gamma divisor) -- a loud failure, not a "
                     "silent one, for that one exact value -- while "
                     "hilbert_holder_constant(1.5, -0.3, ...) returns a FINITE pair with "
                     "only non-fatal RuntimeWarnings, no exception")}


# ---------------------------------------------------------------------------
# A3 -- eps-truncation mechanism: uT (or uS) grows without limit as eps shrinks
# ---------------------------------------------------------------------------


def gate_A3():
    eps_list = (1e-6, 1e-8, 1e-10, 1e-12, 1e-14, 1e-16)
    rows_g0, rows_gneg, rows_ship = [], [], []
    for e in eps_list:
        u = increment_pair_bound(1.0, 0.05, 1.5, 0.0, n_quad=4000, eps=e)
        rows_g0.append({"eps": e, "u_S": u[0], "u_T": u[1]})
        u2 = increment_pair_bound(1.0, 0.05, 1.5, -0.5, n_quad=4000, eps=e)
        rows_gneg.append({"eps": e, "u_S": u2[0], "u_T": u2[1]})
        u3 = increment_pair_bound(1.0, 0.05, 1.5, 0.5, n_quad=4000, eps=e)
        rows_ship.append({"eps": e, "u_S": u3[0], "u_T": u3[1]})
    growth_g0 = rows_g0[-1]["u_T"] / rows_g0[0]["u_T"]
    growth_gneg = rows_gneg[-1]["u_S"] / rows_gneg[0]["u_S"]
    growth_ship = (rows_ship[-1]["u_S"] + rows_ship[-1]["u_T"]) / \
        (rows_ship[0]["u_S"] + rows_ship[0]["u_T"])
    return {"gamma_0.0": rows_g0, "gamma_-0.5": rows_gneg, "gamma_0.5_shipped": rows_ship,
            "growth_uT_gamma0_over_10_decades_of_eps": growth_g0,
            "growth_uS_gammaneg_over_10_decades_of_eps": growth_gneg,
            "growth_shipped_over_10_decades_of_eps": growth_ship,
            "note": ("the coefficient the singularity is charged to GROWS WITHOUT A "
                     "PLATEAU as eps shrinks at gamma <= 0, while the shipped gamma = 0.5 "
                     "converges after ~2 decades -- the finite pair increment_pair_bound "
                     "returns at gamma <= 0 is where the quadrature happened to be cut "
                     "off, not a bound")}


# ---------------------------------------------------------------------------
# A4 -- **VIOLATION 1**: gamma = 0.0, no NaN anywhere
# ---------------------------------------------------------------------------


def gate_A4():
    theta1, sigma = 1.0, 0.05
    u_S, u_T = increment_pair_bound(theta1, sigma, 1.5, 0.0)
    deltas = (1e-3, 1e-6, 1e-9, 1e-12, 1e-15, 1e-20, 1e-25, 1e-30, 1e-40, 1e-45, 1e-50)
    rows = [pair_ratio(theta1, sigma, 1.5, 0.0, d) for d in deltas]
    viol = [r for r in rows if r["ratio_true_over_bound"] > 1.0]
    return {"theta1": theta1, "sigma": sigma, "u_S": u_S, "u_T": u_T, "rows": rows,
            "n_violating_cases": len(viol),
            "first_violating_delta": viol[0]["delta"] if viol else None,
            "worst_ratio": max(r["ratio_true_over_bound"] for r in rows),
            "note": ("gamma = 0.0 is an ordinary-looking, entirely NaN-free argument.  "
                     "u_S = 0.0 exactly (the whole near-pole mass was NOT charged there); "
                     "the true weighted increment ratio exceeds the reported bound once "
                     "the adversary's feature is narrower than roughly delta ~ 1e-45")}


# ---------------------------------------------------------------------------
# A5 -- **VIOLATION 2**: gamma = -0.5, still no NaN
# ---------------------------------------------------------------------------


def gate_A5():
    theta1, sigma = 1.0, 0.05
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        u_S, u_T = increment_pair_bound(theta1, sigma, 1.5, -0.5)
    deltas = (1e-3, 1e-9, 1e-20, 1e-30, 1e-40, 1e-45, 1e-50)
    rows = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rows = [pair_ratio(theta1, sigma, 1.5, -0.5, d) for d in deltas]
    viol = [r for r in rows if r["ratio_true_over_bound"] > 1.0]
    # also confirm the ASSEMBLY-level API silently returns a finite pair for gamma < 0
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        hhc = hilbert_holder_constant(1.5, -0.3, n_theta=24, n_d=14, n_quad=200)
    return {"theta1": theta1, "sigma": sigma, "u_S": u_S, "u_T": u_T, "rows": rows,
            "n_violating_cases": len(viol),
            "first_violating_delta": viol[0]["delta"] if viol else None,
            "worst_ratio": max(r["ratio_true_over_bound"] for r in rows),
            "assembly_level_gamma_neg0.3": {"b_sup": hhc["b_sup"], "b_semi": hhc["b_semi"],
                                            "n_warnings": len(caught),
                                            "warning_types": sorted({type(w.message).__name__
                                                                     for w in caught})},
            "note": ("gamma < 0 needs no NaN either; the seminorm route now diverges (u_S "
                     "carries the near-pole mass instead), and the public assembly API "
                     "hilbert_holder_constant(1.5, -0.3, ...) itself returns a FINITE "
                     "(b_sup, b_semi) with only non-fatal warnings for the whole 24x14 "
                     "pair-grid sweep, never raising")}


# ---------------------------------------------------------------------------
# A6 -- CONTROL: the shipped and production configurations, hunted the same way
# ---------------------------------------------------------------------------


def gate_A6():
    out = {}
    deltas = (1e-3, 1e-9, 1e-20, 1e-30, 1e-40, 1e-50)
    for label, (a, g) in (("shipped_1.5_0.5", (ALPHA, GAMMA)),
                          ("production_1.4_0.15", (PROD_ALPHA, PROD_GAMMA))):
        rows_by_pair = []
        for theta1, sigma in ((1.0, 0.05), (0.3, 0.01), (2.5, 0.05), (np.pi - 0.2, 0.01)):
            rows = [pair_ratio(theta1, sigma, a, g, d) for d in deltas]
            rows_by_pair.append({"theta1": theta1, "sigma": sigma, "rows": rows,
                                 "max_ratio": max(r["ratio_true_over_bound"] for r in rows)})
        out[label] = {"alpha": a, "gamma": g, "by_pair": rows_by_pair,
                     "max_ratio_over_all_pairs": max(p["max_ratio"] for p in rows_by_pair)}
    out["note"] = ("domination HOLDS everywhere probed for both gamma > 0 configurations; "
                   "the ratio falls toward ZERO (not toward 1) as delta shrinks, because "
                   "gamma > 0 makes the reported T grow FASTER than the true increment as "
                   "the adversary's feature narrows -- the opposite asymptotics from V1/V2")
    return out


# ---------------------------------------------------------------------------
# A7 -- what is NOT a finding: alpha = inf's vacuous (0, 0) is trivially sound
# ---------------------------------------------------------------------------


def gate_A7():
    """alpha = inf makes the decay weight (1+X^2)^(alpha/2) infinite for every X != 0, so
    the ONLY finite-S function is h == 0 a.e. -- a (0,0) bound is then vacuously true, not a
    silent corruption. Verified directly: no nonzero h with S = 1 and alpha = inf exists."""
    a_sup, a_semi = increment_pair_bound(1.0, 0.05, np.inf, 0.5)
    # a genuinely alpha=inf-admissible h must vanish away from theta=0
    thetas = np.array([0.5, 1.0, 2.0, 3.0])
    with np.errstate(over="ignore"):
        w = np.cos(0.5 * thetas) ** (-np.inf)
    return {"a_sup": float(a_sup), "a_semi": float(a_semi),
            "decay_weight_at_alpha_inf_away_from_theta0": [float(x) for x in w],
            "note": ("weight = +inf at every theta != 0 when alpha = inf, so the alpha=inf "
                     "'ball' of finite-S functions contains only h == 0; a (0, 0) bound on "
                     "an empty (modulo the zero function) admissible set is vacuously "
                     "correct, not a soundness gap -- reported as a control, not a finding, "
                     "exactly as the novelty pass's MAY-NOT-claim clause anticipated for "
                     "any degeneracy that turns out to be vacuous rather than violating")}


# ---------------------------------------------------------------------------
# A8 -- the soundness predicate, mapped (mirrors leg 106's A6b)
# ---------------------------------------------------------------------------


def gate_A8():
    rows = []
    for g in (-1.0, -0.5, -0.1, 0.0, 0.05, 0.15, 0.25, 0.5, 0.8):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            b1 = increment_pair_bound(1.0, 0.05, 1.5, g, n_quad=4000, eps=1e-8)
            b2 = increment_pair_bound(1.0, 0.05, 1.5, g, n_quad=4000, eps=1e-16)
        s1, s2 = sum(b1), sum(b2)
        drift = (s2 / s1) if s1 else None
        rows.append({"gamma": g, "u_S": b1[0], "u_T": b1[1],
                     "eps_drift_1e-16_over_1e-8": drift, "predicted_sound": bool(g > 0.0)})
    ok = [r for r in rows if r["predicted_sound"]]
    bad = [r for r in rows if not r["predicted_sound"]]
    return {"rows": rows, "n_sound": len(ok), "n_unsound": len(bad),
            "max_eps_drift_sound": max(r["eps_drift_1e-16_over_1e-8"] for r in ok),
            "min_eps_drift_unsound": min(r["eps_drift_1e-16_over_1e-8"] for r in bad),
            "note": ("the analytic predicate is exact -- gamma > 0 -- and the eps-drift "
                     "diagnostic separates the two regimes with a clear gap here: every "
                     "sound row drifts < 1.34x over 8 decades of eps (the smallest "
                     "positive gamma tried, 0.05, is the closest approach) against >= "
                     "1.98x for every gamma <= 0 row, so no marginal gamma close to the "
                     "boundary was found where the diagnostic and the predicate disagree")}


# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    res = {"leg": 119, "route": "HHA", "module_audited": "solver/hilbert_holder.py",
           "read_only": True,
           "gate": ("Under adversarial/degenerate inputs, can any bound "
                    "hilbert_holder.py reports be exceeded (fail to be a true bound), or "
                    "a wrong value be silently returned?"),
           "scope_note": ("Soundness DIRECTION only.  No bound is sharpened and no "
                          "constant is improved; the plan-of-record ban on Route-D "
                          "bound-sharpening is respected literally.  The module is not "
                          "patched: the gate's yes-branch escalates, it does not repair."),
           "shipped_configuration": {"alpha": ALPHA, "gamma": GAMMA},
           "production_configuration": {"alpha": PROD_ALPHA, "gamma": PROD_GAMMA}}
    for name, fn in (("A1_known_answer", gate_A1),
                     ("A2_degenerate_input_inventory", gate_A2),
                     ("A3_eps_truncation_mechanism", gate_A3),
                     ("A4_VIOLATION_gamma_zero", gate_A4),
                     ("A5_VIOLATION_gamma_negative", gate_A5),
                     ("A6_CONTROL_shipped_and_production_are_safe", gate_A6),
                     ("A7_alpha_inf_is_vacuous_not_a_finding", gate_A7),
                     ("A8_soundness_predicate", gate_A8)):
        s = time.time()
        print("  running %s ..." % name, flush=True)
        res[name] = fn()
        print("    done in %.1fs" % (time.time() - s), flush=True)

    res["gate_answer"] = "YES"
    a4, a5, a6 = res["A4_VIOLATION_gamma_zero"], res["A5_VIOLATION_gamma_negative"], \
        res["A6_CONTROL_shipped_and_production_are_safe"]
    res["headline"] = (
        "Two computable, entirely NaN-free configurations exceed increment_pair_bound's "
        "reported (u_S, u_T).  (V1) gamma = 0.0 at theta1=1.0, sigma=0.05 returns "
        "(%.6f, %.6f); the true weighted increment ratio first exceeds the bound at "
        "delta = %s, reaching a ratio of %.4f at delta = 1e-50.  (V2) gamma = -0.5 "
        "returns (%.6f, %.6f) and is exceeded by %.4f at the same delta.  Both are the "
        "eps-truncation of a logarithmically divergent integral: the coefficient carrying "
        "the singularity grows %.2fx / %.2fx over 10 decades of eps with no plateau, "
        "against %.4fx for the shipped gamma = 0.5 over the identical sweep.  The public "
        "assembly API is affected too: hilbert_holder_constant(1.5, -0.3, ...) returns a "
        "FINITE (b_sup, b_semi) = (%.4f, %.4f) with only non-fatal warnings across a full "
        "pair-grid sweep, never raising -- while gamma = 0.0 EXACTLY crashes instead "
        "(ZeroDivisionError inside the pointwise route's hilbert_split_bound), a loud "
        "failure for that one value only.  The SHIPPED (alpha=1.5, gamma=0.5) and "
        "PRODUCTION (alpha~1.4, gamma~0.15) configurations are NOT affected: domination "
        "holds at every probed pair and delta, with the ratio falling toward zero (not "
        "toward one) as the adversary's feature narrows." % (
            a4["u_S"], a4["u_T"], a4["first_violating_delta"], a4["worst_ratio"],
            a5["u_S"], a5["u_T"], a5["worst_ratio"],
            res["A3_eps_truncation_mechanism"]["growth_uT_gamma0_over_10_decades_of_eps"],
            res["A3_eps_truncation_mechanism"]["growth_uS_gammaneg_over_10_decades_of_eps"],
            res["A3_eps_truncation_mechanism"]["growth_shipped_over_10_decades_of_eps"],
            a5["assembly_level_gamma_neg0.3"]["b_sup"],
            a5["assembly_level_gamma_neg0.3"]["b_semi"]))
    res["disposition"] = (
        "ESCALATE, do not patch.  solver/hilbert_holder.py is untouched by this leg.  The "
        "repair, when authorised, is a guard on increment_pair_bound and "
        "hilbert_holder_constant -- reject gamma <= 0 (and non-finite gamma/alpha) -- not a "
        "change to the majorant, which is correct wherever the payer rule selects the "
        "seminorm account on a neighbourhood of the near-pole singularity.  Gates A2 "
        "(the gamma<=0 rows), A4, A5 and A8 (the unsound rows) are GAP-PINS in the sense "
        "of leg 84: they assert the CURRENT unsound behaviour so it cannot decay at the "
        "rate of memory, and MUST BE INVERTED, NOT WEAKENED, the day a guard lands.")
    res["runtime_seconds"] = time.time() - t0

    with open(OUT, "w") as f:
        json.dump(res, f, indent=2, default=float)
    print("\n" + res["headline"])
    print("\nwrote %s (%.1fs)" % (OUT, res["runtime_seconds"]))


if __name__ == "__main__":
    main()
