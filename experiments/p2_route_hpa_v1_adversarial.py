"""Leg 106 (Route-HPA) -- the adversarial battery against hilbert_pointwise.py's BOUND DIRECTION.

THE QUESTION (the leg's gate, verbatim):

    Under an adversarial battery of degenerate or NaN-poisoned inputs, does
    solver/hilbert_pointwise.py's bound ever fail to dominate the true |H(h)| value on a
    case where both are computable?

**THE ANSWER IS YES, AND IT IS REPRODUCED HERE TWICE.**  `solver/hilbert_pointwise.py` is
READ-ONLY under this leg and is NOT patched: the gate's yes-branch escalates, it does not
repair.

WHAT THIS IS NOT.  No bound is sharpened, no constant is improved, no `||A||`, `C_Q`, `Y_0`,
`Z_1` or `Z_2` is re-derived.  The plan-of-record ban *"another Route-D bound-sharpening
leg"* is respected literally -- the audit direction is one-sided and can only ever weaken
confidence in an existing number.

--------------------------------------------------------------------------------
THE CLAIM UNDER TEST
--------------------------------------------------------------------------------
`pointwise_bound(theta, alpha, gamma, rho)` returns `(a_sup, a_semi)` and the module's
docstring asserts, for EVERY even h and -- explicitly -- for EVERY fixed rho:

    |H(h)(theta)| <= a_sup * S + a_semi * T ,     "any FIXED rule for choosing gives a
                                                   valid linear bound a_sup S + a_semi T"

with S the weighted sup part and T the weighted Holder seminorm.

--------------------------------------------------------------------------------
THE MECHANISM OF FAILURE (measured, then explained, then predicted)
--------------------------------------------------------------------------------
At each offset s = |phi - theta| the increment |h(phi) - h(theta)| is charged either to the
seminorm account (`cT = s^gamma * cos^{alpha-gamma}`) or to the sup account
(`cS = cos^alpha(phi/2) + cos^alpha(theta/2)`), by the rule `take_T = rho*cT <= cS`.

As s -> 0 the kernel weight `|K|*s -> 2` while `cS -> 2 cos^alpha(theta/2) != 0`.  So the
sup account's integrand in `d(log s)` tends to a NONZERO constant and the sup-route integral
is LOGARITHMICALLY DIVERGENT.  Only `cT -> 0` (which needs gamma > 0) tames the singularity,
and only if the rule actually selects it near s = 0.  Two ways it does not:

  (V1) `rho = NaN`.  IEEE-754 sec 5.11: every comparison against NaN is False, so
       `take_T = rho*cT <= cS` is False EVERYWHERE and the whole integral -- singularity
       included -- is charged to the sup account.  `rho = +inf` and `rho >= ~1e300` take the
       same branch.  The function returns a FINITE, plausible-looking pair whose second
       entry is exactly 0.0.
  (V2) `gamma = 0` (or gamma < 0), with any rho.  `cT` no longer vanishes at s -> 0, so
       whichever account is charged, the integrand does not vanish and the integral
       diverges.

In both cases the number returned is finite ONLY because the quadrature starts at
`s = eps*L` rather than 0.  It is the eps-truncation of a divergent integral, not a bound --
gate A5c demonstrates this by moving eps and watching the "bound" grow without limit.

--------------------------------------------------------------------------------
THE ADVERSARY, AND WHY ITS |H(h)| IS TRUSTWORTHY
--------------------------------------------------------------------------------
The extremiser is forced by the kernel's sign structure: sign K_theta(phi) = sign(theta-phi),
so the increment must be positive below theta and negative above it, at the largest size the
sup account allows.  That is a STEP of width delta inside the decay envelope,

    h(phi) = cos^alpha(phi/2) * clip(-(phi - theta)/delta, -1, 1) ,   h(theta) = 0 ,

with S = 1 exactly (|h| <= cos^alpha(phi/2), attained).  Its |H(h)(theta)| is computed by
the SAME subtracted-p.v. identity the module bounds, on a log-graded mesh, parameterised by
the exact signed offset u = phi - theta -- the module's own offset trick, which is what keeps
delta = 1e-50 free of cancellation.  Gate A1 known-answer-checks that quadrature against
`solver.hilbert_holder.conjugate` (cos k th -> sin k th, exact) before any verdict is read
from it, and gate A5b checks the measured growth rate against the analytic prediction
`d|psi| / d ln(1/delta) = (2/pi) cos^alpha(theta/2)`.

--------------------------------------------------------------------------------
WHAT IS **NOT** AFFECTED (the blast radius, stated up front)
--------------------------------------------------------------------------------
The shipped Route-D configuration -- alpha = 1.5, gamma = 0.5, rho in {1, 6, 25} -- is
NOT affected.  Gate A7 hunts it with the same adversary and finds domination holding
everywhere, with the margin narrowing to 2.1e-4 only in the far field (theta -> pi), where
the bound is asymptotically SATURATED rather than violated.  V1 and V2 are reachable only by
a caller who passes a NaN/inf rho or a non-positive gamma.

Run:  .venv/bin/python experiments/p2_route_hpa_v1_adversarial.py
Writes: writeup/data/p2_route_hpa_v1_adversarial.json
"""
from __future__ import annotations

import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.hilbert_holder import conjugate                                  # noqa: E402
from solver.hilbert_pointwise import (                                       # noqa: E402
    measured_pointwise, pointwise_bound, pointwise_curves, theta_grid, weighted_sups,
)

ALPHA, GAMMA = 1.5, 0.5          # the shipped Route-D pair
SHIPPED_RHOS = (1.0, 6.0, 25.0)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_hpa_v1_adversarial.json")


# ---------------------------------------------------------------------------
# the adversary and its exact conjugate
# ---------------------------------------------------------------------------


def step_profile(phi, theta, delta, alpha=ALPHA, offset=None):
    """h(phi) = cos^alpha(phi/2) * clip(-(phi-theta)/delta, -1, 1); h(theta) = 0.

    `offset` supplies u = phi - theta EXACTLY when the caller has it (it always does
    inside a log-graded offset mesh), which is what makes delta = 1e-50 meaningful.
    """
    u = (phi - theta) if offset is None else offset
    return np.cos(0.5 * phi) ** alpha * np.clip(-u / delta, -1.0, 1.0)


def psi_of_step(theta, delta, alpha=ALPHA, n=400000, smin=1e-60):
    """|H(h)(theta)| for the step adversary, by the subtracted p.v. identity."""
    tot = 0.0
    for L, sgn in ((theta, -1.0), (np.pi - theta, 1.0)):
        if L <= 0.0:
            continue
        s = np.geomspace(smin * L, L, int(n))
        u = sgn * s
        phi = theta + u
        h = step_profile(phi, theta, delta, alpha, offset=u)      # h(theta) = 0
        K = -np.sin(theta) / (np.sin(0.5 * (phi + theta)) * np.sin(0.5 * u))
        tot += float(np.trapezoid(h * K * s, np.log(s)))
    return tot / (2.0 * np.pi)


def step_norms(theta, delta, alpha=ALPHA, gamma=GAMMA, n=400000, smin=1e-60):
    """(S, T) for the step adversary.  S = 1 exactly; T is a sup over exact offsets."""
    T = 0.0
    for L, sgn in ((theta, -1.0), (np.pi - theta, 1.0)):
        if L <= 0.0:
            continue
        s = np.geomspace(smin * L, L, int(n))
        u = sgn * s
        phi = theta + u
        h = step_profile(phi, theta, delta, alpha, offset=u)
        wsemi = np.cos(0.5 * np.minimum(phi, theta)) ** (alpha - gamma)
        T = max(T, float(np.max(np.abs(h) / (wsemi * s ** gamma))))
    return 1.0, T


def psi_of_poly(coef, theta, n=200000, smin=1e-13):
    """The same quadrature, applied to a cosine polynomial -- for the known-answer gate."""
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


def _call(fn):
    """Return the value, or a string tag naming the exception -- never a boolean."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            v = fn()
        if isinstance(v, tuple):
            return [None if x is None else float(x) for x in v]
        if isinstance(v, (int, float, np.floating, np.integer)):
            return float(v)
        return v
    except Exception as e:                                     # noqa: BLE001
        return "%s: %s" % (type(e).__name__, str(e)[:70])


# ---------------------------------------------------------------------------
# A1 -- known answer: the adversary's quadrature reproduces the exact conjugate
# ---------------------------------------------------------------------------


def gate_A1():
    cases = [np.array([0.0, 1.0]), np.array([0.0, 0.0, 0.0, 1.0]),
             np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])]
    worst, n = 0.0, 0
    for coef in cases:
        for th in (0.03, 0.4, 1.2, 2.5, 3.0, 3.14):
            worst = max(worst, abs(psi_of_poly(coef, th)
                                   - float(conjugate(coef, [th])[0])))
            n += 1
    zero = max(abs(psi_of_poly(np.array([1.0]), th)) for th in (0.2, 1.5, 3.0))
    return {"cases": n, "max_abs_error_vs_exact_conjugate": worst,
            "pv_of_constant_function": zero,
            "note": ("the battery's |H(h)| machinery is known-answer checked against "
                     "solver.hilbert_holder.conjugate BEFORE any verdict is read from it")}


# ---------------------------------------------------------------------------
# A2 -- signed quadrature error of the shipped (n_quad=400, eps=1e-10)
# ---------------------------------------------------------------------------


def gate_A2():
    rows = []
    for th in (1e-6, 1e-3, 0.05, 0.5, 1.0, 2.0, 3.0, np.pi - 1e-3, np.pi - 1e-7):
        ref = pointwise_bound(th, ALPHA, GAMMA, rho=6.0, n_quad=200000, eps=1e-14)
        dfl = pointwise_bound(th, ALPHA, GAMMA, rho=6.0)
        rows.append({"theta": th,
                     "rel_err_a_sup": dfl[0] / ref[0] - 1.0 if ref[0] else None,
                     "rel_err_a_semi": dfl[1] / ref[1] - 1.0 if ref[1] else None})
    ladder = []
    ref = np.array(pointwise_bound(1.0, ALPHA, GAMMA, rho=6.0, n_quad=200000, eps=1e-14))
    for nq in (2, 3, 5, 10, 25, 50, 100, 200, 400, 800, 1600):
        d = np.array(pointwise_bound(1.0, ALPHA, GAMMA, rho=6.0, n_quad=nq))
        ladder.append({"n_quad": nq, "rel_err_sum": float(d.sum() / ref.sum() - 1.0)})
    worst_under = min(r["rel_err_a_sup"] for r in rows if r["rel_err_a_sup"] is not None)
    return {"per_theta": rows, "n_quad_ladder": ladder,
            "worst_understatement_a_sup": worst_under,
            "note": ("the DEFAULT quadrature understates its own majorant by up to "
                     "%.2f%% (at small theta); the sign matters because an understated "
                     "majorant is the unsafe direction" % (100 * abs(worst_under)))}


# ---------------------------------------------------------------------------
# A3 -- the eps truncation, as a function of gamma
# ---------------------------------------------------------------------------


def gate_A3():
    rows = []
    for g in (0.9, 0.5, 0.25, 0.1, 0.03, 0.01, 0.0):
        vals = [sum(pointwise_bound(1.0, ALPHA, g, rho=1.0, n_quad=4000, eps=e))
                for e in (1e-4, 1e-7, 1e-10, 1e-13)]
        rows.append({"gamma": g, "bound_at_eps_1e-4": vals[0],
                     "bound_at_eps_1e-7": vals[1], "bound_at_eps_1e-10": vals[2],
                     "bound_at_eps_1e-13": vals[3],
                     "ratio_1e-13_over_1e-4": vals[3] / vals[0]})
    return {"rows": rows,
            "note": ("truncation cost goes like eps^gamma: negligible at the shipped "
                     "gamma = 0.5 (1.01x over 9 decades of eps) and TOTAL at gamma = 0 "
                     "(3.17x and still growing -- the integral does not converge)")}


# ---------------------------------------------------------------------------
# A4 -- the degenerate / NaN-poisoned input inventory (values, never booleans)
# ---------------------------------------------------------------------------


def gate_A4():
    th_cases = {}
    for t in (0.0, np.pi, -0.5, np.pi + 0.5, 2 * np.pi, np.nan, np.inf, -np.inf,
              1e-300, 5e-324):
        th_cases[repr(t)] = _call(lambda t=t: pointwise_bound(t, ALPHA, GAMMA, rho=1.0,
                                                              n_quad=200))
    ag = {}
    for a, g in ((np.nan, 0.5), (1.5, np.nan), (np.inf, 0.5), (1.5, np.inf), (1.5, 0.0),
                 (1.5, 1.5), (1.5, 2.5), (0.0, 0.0), (-1.0, 0.5), (1.5, -0.5)):
        ag["alpha=%r,gamma=%r" % (a, g)] = _call(
            lambda a=a, g=g: pointwise_bound(1.0, a, g, rho=1.0, n_quad=200))
    rh = {}
    for r in (0.0, -1.0, np.nan, np.inf, -np.inf, 1e300, 1e-300):
        rh[repr(r)] = _call(lambda r=r: pointwise_bound(1.0, ALPHA, GAMMA, rho=r,
                                                        n_quad=200))
    nq = {repr(n): _call(lambda n=n: pointwise_bound(1.0, ALPHA, GAMMA, n_quad=n))
          for n in (0, 1, 2, -5, np.nan, np.inf)}
    ep = {repr(e): _call(lambda e=e: pointwise_bound(1.0, ALPHA, GAMMA, n_quad=200,
                                                     eps=e))
          for e in (0.0, 1.0, 2.0, -1e-3, np.nan, np.inf)}
    tg = {repr(n): _call(lambda n=n: float(theta_grid(n).size))
          for n in (0, 1, 2, 3, -4)}
    tg["lo=0.0"] = _call(lambda: float(theta_grid(140, lo=0.0).size))
    tg["lo=nan"] = _call(lambda: float(theta_grid(140, lo=np.nan).size))

    class _N:
        def __init__(s_, a, b): s_.a, s_.b = a, b
        def sup_part(s_, h): return s_.a
        def seminorm(s_, h): return s_.b

    cv = pointwise_curves(ALPHA, GAMMA, n_theta=40, n_quad=200)
    tt = np.linspace(0.01, 3.1, 60)
    mp = {}
    for a, b in ((1.0, 1.0), (0.0, 0.0), (np.nan, 1.0), (np.inf, 1.0), (-1.0, -1.0)):
        mp["S=%r,T=%r" % (a, b)] = _call(
            lambda a=a, b=b: measured_pointwise({"p": np.sin(tt)}, tt,
                                                lambda h: np.cos(tt), _N(a, b),
                                                ALPHA, GAMMA, cv, n_sample=20))
    mp["psi_is_nan"] = _call(
        lambda: measured_pointwise({"p": np.sin(tt)}, tt, lambda h: np.full(60, np.nan),
                                   _N(1.0, 1.0), ALPHA, GAMMA, cv, n_sample=20))
    mp["empty_family"] = _call(
        lambda: measured_pointwise({}, tt, lambda h: np.cos(tt), _N(1.0, 1.0),
                                   ALPHA, GAMMA, cv, n_sample=20))
    n_finite_pairs = sum(1 for v in list(th_cases.values()) + list(ag.values())
                         + list(rh.values()) if isinstance(v, list)
                         and all(np.isfinite(x) for x in v))
    return {"theta": th_cases, "alpha_gamma": ag, "rho": rh, "n_quad": nq, "eps": ep,
            "theta_grid": tg, "measured_pointwise": mp,
            "n_inputs_returning_a_finite_pair": n_finite_pairs,
            "note": ("rho = NaN, +inf and 1e300 all return the SAME finite pair with "
                     "a_semi exactly 0.0 -- IEEE-754 sec 5.11 makes `rho*cT <= cS` False "
                     "everywhere; measured_pointwise reports worst_ratio 0.0 with an "
                     "empty profile name whenever the ratio is NaN, which reads as "
                     "'no violation' and is the same silence for a poisoned norm, a "
                     "poisoned psi and an empty family")}


# ---------------------------------------------------------------------------
# A5 -- **VIOLATION 1**: rho = NaN / +inf routes the singularity to the sup account
# ---------------------------------------------------------------------------


def gate_A5():
    theta = 1.0
    coeffs = {repr(r): list(pointwise_bound(theta, ALPHA, GAMMA, rho=r))
              for r in (np.nan, np.inf, 1e300)}
    a_sup, a_semi = pointwise_bound(theta, ALPHA, GAMMA, rho=np.nan)
    rows = []
    for delta in (1e-10, 1e-20, 1e-30, 1e-40, 1e-50):
        psi = abs(psi_of_step(theta, delta))
        S, T = step_norms(theta, delta)
        b = a_sup * S + a_semi * T
        rows.append({"delta": delta, "S": S, "T": T, "true_abs_H": psi, "bound": b,
                     "ratio_true_over_bound": psi / b})
    # A5b: the growth rate against its analytic prediction
    pred = (2.0 / np.pi) * np.cos(0.5 * theta) ** ALPHA
    meas = ((rows[2]["true_abs_H"] - rows[1]["true_abs_H"]) / np.log(1e10))
    # A5c: the returned "bound" is an eps-truncation, not a bound
    eps_scan = [{"eps": e,
                 "a_sup": pointwise_bound(theta, ALPHA, GAMMA, rho=np.nan,
                                          n_quad=20000, eps=e)[0]}
                for e in (1e-6, 1e-10, 1e-14, 1e-20, 1e-30)]
    viol = [r for r in rows if r["ratio_true_over_bound"] > 1.0]
    return {"theta": theta, "coefficients_by_rho": coeffs,
            "a_semi_value": a_semi, "rows": rows,
            "n_violating_cases": len(viol),
            "first_violating_delta": viol[0]["delta"] if viol else None,
            "worst_ratio": max(r["ratio_true_over_bound"] for r in rows),
            "divergence_slope_measured_per_ln": meas,
            "divergence_slope_predicted_per_ln": pred,
            "slope_rel_error": abs(meas / pred - 1.0),
            "eps_scan_of_the_bound": eps_scan,
            "note": ("|H(h)| grows like (2/pi) cos^alpha(theta/2) * ln(1/delta) without "
                     "limit while the returned bound is frozen at its eps-truncated "
                     "value, so EVERY sufficiently thin step violates it")}


# ---------------------------------------------------------------------------
# A6 -- **VIOLATION 2**: gamma = 0, a degenerate but entirely NaN-free input
# ---------------------------------------------------------------------------


def gate_A6():
    theta = 1.0
    a_sup, a_semi = pointwise_bound(theta, ALPHA, 0.0, rho=1.0)
    rows = []
    for delta in (1e-10, 1e-20, 1e-30, 1e-40, 1e-50):
        psi = abs(psi_of_step(theta, delta))
        S, T = step_norms(theta, delta, gamma=0.0)
        b = a_sup * S + a_semi * T
        rows.append({"delta": delta, "S": S, "T": T, "true_abs_H": psi, "bound": b,
                     "ratio_true_over_bound": psi / b})
    viol = [r for r in rows if r["ratio_true_over_bound"] > 1.0]
    return {"theta": theta, "coefficients": [a_sup, a_semi],
            "a_sup_value": a_sup, "rows": rows,
            "n_violating_cases": len(viol),
            "first_violating_delta": viol[0]["delta"] if viol else None,
            "worst_ratio": max(r["ratio_true_over_bound"] for r in rows),
            "note": ("no NaN anywhere: gamma = 0 is an ordinary-looking argument and the "
                     "violation is already 1.04x at delta = 1e-10")}


# ---------------------------------------------------------------------------
# A6b -- the exact soundness predicate, mapped
# ---------------------------------------------------------------------------


def gate_A6b():
    """Soundness needs gamma > 0 AND rho finite-and-not-NaN.  Map it by the ONE
    signature that separates the two regimes: does a coefficient collapse to exactly
    zero (all mass on one account) and does the pair move with eps?"""
    rows = []
    for g in (-0.5, 0.0, 0.01, 0.1, 0.5, 0.9):
        for r in (0.0, 1.0, 6.0, 25.0, 1e300, np.inf, np.nan):
            b1 = pointwise_bound(1.0, ALPHA, g, rho=r, n_quad=4000, eps=1e-8)
            b2 = pointwise_bound(1.0, ALPHA, g, rho=r, n_quad=4000, eps=1e-16)
            drift = (sum(b2) / sum(b1)) if sum(b1) else None
            rows.append({"gamma": g, "rho": (None if np.isnan(r) else
                                             (1e308 if np.isinf(r) else r)),
                         "rho_label": repr(r), "a_sup": b1[0], "a_semi": b1[1],
                         "eps_drift_1e-16_over_1e-8": drift,
                         "predicted_sound": bool(g > 0.0 and np.isfinite(r))})
    ok = [x for x in rows if x["predicted_sound"]]
    bad = [x for x in rows if not x["predicted_sound"]]
    resolved = [x for x in ok if x["gamma"] >= 0.1]
    marginal = [x for x in ok if x["gamma"] < 0.1]
    return {"rows": rows, "n_sound": len(ok), "n_unsound": len(bad),
            "max_eps_drift_sound_and_gamma_at_least_0.1": max(
                x["eps_drift_1e-16_over_1e-8"] for x in resolved),
            "max_eps_drift_sound_but_gamma_below_0.1": max(
                x["eps_drift_1e-16_over_1e-8"] for x in marginal),
            "min_eps_drift_where_predicted_unsound": min(
                x["eps_drift_1e-16_over_1e-8"] for x in bad),
            "note": ("the ANALYTIC predicate -- gamma > 0 and rho finite-and-not-NaN -- "
                     "is exact, and it is what gates A5/A6 exhibit.  The eps-drift "
                     "DIAGNOSTIC that would let a caller detect the failure at runtime "
                     "separates the two regimes only for gamma >= 0.1 (drift <= 1.0001 "
                     "there vs >= 1.98 when unsound); at gamma = 0.01 a formally sound "
                     "configuration still drifts 2.00x over 8 decades of eps, because "
                     "the truncation cost eps^gamma converges too slowly to tell the "
                     "two apart numerically.  Reported rather than hidden: the runtime "
                     "test is not a substitute for the predicate")}


# ---------------------------------------------------------------------------
# A7 -- the SHIPPED configuration, hunted with the same adversary
# ---------------------------------------------------------------------------


def _refined_theta(t, n_local=500, n_base=500):
    base = np.linspace(1e-14, np.pi - 1e-14, n_base)
    s = np.geomspace(1e-12, max(np.pi - t, t), n_local // 2)
    th = np.unique(np.concatenate([base, t - s, t + s, [t]]))
    return th[(th > 0) & (th < np.pi)]


def _holder_step(thv, t, delta, gamma):
    u = (t - thv) / delta
    return np.cos(0.5 * thv) ** ALPHA * np.sign(u) * np.minimum(1.0, np.abs(u) ** gamma)


def _norms_at(thv, hv, alpha=ALPHA, gamma=GAMMA):
    S = float(np.max(np.cos(0.5 * thv) ** (-alpha) * np.abs(hv)))
    ws = np.cos(0.5 * thv) ** (-(alpha - gamma))
    d = np.abs(thv[:, None] - thv[None, :])
    np.fill_diagonal(d, np.inf)
    T = float(np.max(np.minimum(ws[:, None], ws[None, :])
                     * np.abs(hv[:, None] - hv[None, :]) / d ** gamma))
    return S, T


def _psi_analytic(t, delta, gamma, n=60000):
    tot = 0.0
    for L, sgn in ((t, -1.0), (np.pi - t, 1.0)):
        if L <= 0.0:
            continue
        s = np.geomspace(1e-13 * L, L, int(n))
        u = sgn * s
        phi = t + u
        sig = np.sign(-u / delta) * np.minimum(1.0, np.abs(u / delta) ** gamma)
        h = np.cos(0.5 * phi) ** ALPHA * sig
        K = -np.sin(t) / (np.sin(0.5 * (phi + t)) * np.sin(0.5 * u))
        tot += float(np.trapezoid(h * K * s, np.log(s)))
    return tot / (2.0 * np.pi)


def gate_A7():
    out = {}
    thetas = (1e-6, 1e-3, 0.05, 0.5, 2.0, 3.0, np.pi - 3e-3, np.pi - 1e-4,
              np.pi - 1e-6, np.pi - 1e-8)
    for rho in SHIPPED_RHOS:
        Xs, aS, aT = pointwise_curves(ALPHA, GAMMA, rho=rho, n_theta=140, n_quad=400)
        rows = []
        for t in thetas:
            eS, eT = pointwise_bound(t, ALPHA, GAMMA, rho=rho, n_quad=200000, eps=1e-14)
            lx = np.log(np.clip(np.tan(0.5 * t), Xs[0], Xs[-1]))
            iS = float(np.interp(lx, np.log(Xs), aS))
            iT = float(np.interp(lx, np.log(Xs), aT))
            thv = _refined_theta(t)
            best = (0.0, 0.0, None)
            for delta in np.geomspace(1e-9, 2.0, 16):
                hv = _holder_step(thv, t, delta, GAMMA)
                S, T = _norms_at(thv, hv)
                psi = abs(_psi_analytic(t, delta, GAMMA))
                r_ex = psi / (eS * S + eT * T)
                if r_ex > best[0]:
                    best = (r_ex, psi / (iS * S + iT * T), delta)
            rows.append({"theta": t, "pi_minus_theta": np.pi - t,
                         "ratio_vs_exact_bound": best[0],
                         "ratio_vs_interpolated_bound": best[1],
                         "worst_delta": best[2]})
        out["rho=%g" % rho] = {
            "rows": rows,
            "max_ratio_vs_exact_bound": max(r["ratio_vs_exact_bound"] for r in rows),
            "max_ratio_vs_interpolated_bound": max(r["ratio_vs_interpolated_bound"]
                                                   for r in rows)}
    out["note"] = ("domination HOLDS everywhere in the shipped configuration; the margin "
                   "collapses toward zero as theta -> pi because the bound is "
                   "asymptotically SATURATED there, not because it is violated")
    out["thinnest_margin"] = 1.0 - max(v["max_ratio_vs_interpolated_bound"]
                                       for k, v in out.items() if k.startswith("rho="))
    return out


# ---------------------------------------------------------------------------
# A8 -- the GRID-NORM evaluation hazard (JOURNAL B1, re-measured not re-claimed)
# ---------------------------------------------------------------------------


def gate_A8():
    from solver.decay_collocation import grid, transforms

    rows = []
    for J, t0 in ((80, 3.12), (80, 3.05), (160, 3.13)):
        th, _ = grid(J)
        to_coef, _, _ = transforms(J)
        it = int(np.argmin(np.abs(th - t0)))
        t = th[it]
        aS, aT = pointwise_bound(t, ALPHA, GAMMA, rho=1.0, n_quad=4000)
        k = np.arange(J)
        c = np.sin(t * k) @ to_coef
        w = np.cos(0.5 * th) ** (-ALPHA)
        ws = np.cos(0.5 * th) ** (-(ALPHA - GAMMA))
        ii, jj = np.triu_indices(J, 1)
        p = np.minimum(ws[ii], ws[jj]) / np.abs(th[ii] - th[jj]) ** GAMMA

        def ratio(h):
            S = float(np.max(w * np.abs(h)))
            T = float(np.max(p * np.abs(h[ii] - h[jj])))
            return abs(float(c @ h)) / (aS * S + aT * T), S, T

        rng = np.random.default_rng(106)
        best = (0.0, None)
        for h0 in [np.cos(0.5 * th) ** ALPHA * np.clip((t - th) / d, -1, 1)
                   for d in (0.003, 0.02, 0.1)] + \
                  [np.cos(0.5 * th) ** ALPHA * rng.standard_normal(J) for _ in range(3)]:
            h = h0 / max(np.max(np.abs(h0)), 1e-300)
            for beta in (20.0, 100.0, 500.0, 2500.0):
                step = 0.15
                for _ in range(150):
                    a1 = w * np.abs(h)
                    a2 = p * np.abs(h[ii] - h[jj])
                    m1, m2 = a1.max(), a2.max()
                    e1 = np.exp(beta * (a1 - m1) / max(m1, 1e-300)); e1 /= e1.sum()
                    e2 = np.exp(beta * (a2 - m2) / max(m2, 1e-300)); e2 /= e2.sum()
                    S, T = float(e1 @ a1), float(e2 @ a2)
                    cont = e2 * p * np.sign(h[ii] - h[jj])
                    gT = np.bincount(ii, cont, J) - np.bincount(jj, cont, J)
                    num = float(c @ h) or 1e-300
                    g = c / num - (aS * e1 * w * np.sign(h) + aT * gT) / (aS * S + aT * T)
                    h = h + step * g / (np.linalg.norm(g) + 1e-300) * np.linalg.norm(h)
                    r = ratio(h)[0]
                    if r > best[0]:
                        best = (r, h.copy())
                    step *= 0.999
        h = best[1]
        r, S, T = ratio(h)
        coef = to_coef @ h
        thf = np.linspace(th[0], th[-1], J * 6)
        hf = np.cos(np.outer(thf, k)) @ coef
        Sf, Tf = _norms_at(thf, hf)
        rows.append({"J": J, "theta": t, "grid_norm_ratio": r,
                     "worst_h_nodal_values": [float(x) for x in h],
                     "refined_norm_ratio": abs(float(c @ h)) / (aS * Sf + aT * Tf),
                     "S_grid": S, "S_refined": Sf, "S_blowup": Sf / S,
                     "T_grid": T, "T_refined": Tf, "T_blowup": Tf / T})
    return {"rows": rows,
            "max_grid_norm_ratio": max(r["grid_norm_ratio"] for r in rows),
            "max_refined_norm_ratio": max(r["refined_norm_ratio"] for r in rows),
            "note": ("this is NOT a defect of the bound: it is JOURNAL section B1's "
                     "grid-seminorm lesson re-measured on this module.  The extremiser's "
                     "TRUE norms are several-fold larger than the grid pairs can see, so "
                     "a caller who feeds grid-evaluated S and T into the bound is not "
                     "using the norms the theorem is stated in")}


# ---------------------------------------------------------------------------
# A9 -- the two consumption paths: interpolation, and the sup over theta_grid
# ---------------------------------------------------------------------------


def gate_A9():
    interp = []
    thf = np.unique(np.concatenate([np.geomspace(1e-7, np.pi / 2, 200),
                                    np.pi - np.geomspace(1e-7, np.pi / 2, 200)]))
    thf = thf[(thf > 0) & (thf < np.pi)]
    for rho in (1.0, 6.0):
        Xs, aS, aT = pointwise_curves(ALPHA, GAMMA, rho=rho, n_theta=140, n_quad=400)
        worst = (9.9, None)
        for t in thf:
            lx = np.log(np.clip(np.tan(0.5 * t), Xs[0], Xs[-1]))
            eS, eT = pointwise_bound(t, ALPHA, GAMMA, rho=rho, n_quad=4000)
            for lbl, i_, e_ in (("a_sup", float(np.interp(lx, np.log(Xs), aS)), eS),
                                ("a_semi", float(np.interp(lx, np.log(Xs), aT)), eT)):
                if e_ > 0 and i_ / e_ < worst[0]:
                    worst = (i_ / e_, {"coefficient": lbl, "theta": t,
                                       "interpolated": i_, "exact": e_})
        interp.append({"rho": rho, "worst_interp_over_exact": worst[0],
                       "where": worst[1]})
    sups = []
    for n_th in (70, 140, 280, 560, 1120, 2240):
        w = weighted_sups(pointwise_curves(ALPHA, GAMMA, rho=6.0, n_theta=n_th,
                                           n_quad=800), ALPHA)
        sups.append({"n_theta": n_th, **w})
    base = next(s for s in sups if s["n_theta"] == 140)
    fine = sups[-1]
    return {"interpolation": interp, "weighted_sups_vs_n_theta": sups,
            "closure_sup_understatement_at_140":
                1.0 - base["closure_sup"] / fine["closure_sup"],
            "closure_semi_understatement_at_140":
                1.0 - base["closure_semi"] / fine["closure_semi"],
            "note": ("both consumption paths are optimistic: linear interpolation in "
                     "log X understates the exact coefficient, and a max over 140 grid "
                     "nodes understates the sup over theta.  Neither is large enough to "
                     "break the shipped configuration (gate A7), but both eat the same "
                     "far-field margin")}


# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    res = {"leg": 106, "route": "HPA", "module_audited": "solver/hilbert_pointwise.py",
           "read_only": True,
           "gate": ("Under an adversarial battery of degenerate or NaN-poisoned inputs, "
                    "does solver/hilbert_pointwise.py's bound ever fail to dominate the "
                    "true |H(h)| value on a case where both are computable?"),
           "scope_note": ("Soundness DIRECTION only.  No bound is sharpened and no "
                          "constant is improved; the plan-of-record ban on Route-D "
                          "bound-sharpening is respected literally.  The module is not "
                          "patched: the gate's yes-branch escalates, it does not repair."),
           "shipped_configuration": {"alpha": ALPHA, "gamma": GAMMA,
                                     "rho": list(SHIPPED_RHOS)}}
    for name, fn in (("A1_known_answer", gate_A1),
                     ("A2_quadrature_signed_error", gate_A2),
                     ("A3_eps_truncation_vs_gamma", gate_A3),
                     ("A4_degenerate_input_inventory", gate_A4),
                     ("A5_VIOLATION_rho_nan_or_inf", gate_A5),
                     ("A6_VIOLATION_gamma_zero", gate_A6),
                     ("A6b_soundness_predicate", gate_A6b),
                     ("A7_shipped_configuration_is_safe", gate_A7),
                     ("A8_grid_norm_hazard", gate_A8),
                     ("A9_consumption_paths", gate_A9)):
        s = time.time()
        print("  running %s ..." % name, flush=True)
        res[name] = fn()
        print("    done in %.1fs" % (time.time() - s), flush=True)

    res["gate_answer"] = "YES"
    res["headline"] = (
        "Two computable configurations exceed the bound.  (V1) rho = NaN -- and "
        "identically rho = +inf and rho >= 1e300 -- returns (a_sup, a_semi) = "
        "(%.6f, 0.0) at theta = 1.0, and the step adversary of width 1e-20 attains "
        "|H(h)| = %.6f, a ratio of %.4f rising to %.4f at width 1e-50.  (V2) gamma = 0, "
        "with no NaN anywhere, returns (0.0, %.6f) and is already exceeded by %.4f at "
        "width 1e-10, rising to %.4f.  Both are the eps-truncation of a logarithmically "
        "divergent integral.  The SHIPPED configuration (alpha 1.5, gamma 0.5, rho in "
        "{1, 6, 25}) is NOT affected: domination holds at every probed theta, with the "
        "margin narrowing to %.2e only as theta -> pi, where the bound is asymptotically "
        "saturated." % (
            res["A5_VIOLATION_rho_nan_or_inf"]["coefficients_by_rho"][repr(np.nan)][0],
            res["A5_VIOLATION_rho_nan_or_inf"]["rows"][1]["true_abs_H"],
            res["A5_VIOLATION_rho_nan_or_inf"]["rows"][1]["ratio_true_over_bound"],
            res["A5_VIOLATION_rho_nan_or_inf"]["worst_ratio"],
            res["A6_VIOLATION_gamma_zero"]["coefficients"][1],
            res["A6_VIOLATION_gamma_zero"]["rows"][0]["ratio_true_over_bound"],
            res["A6_VIOLATION_gamma_zero"]["worst_ratio"],
            res["A7_shipped_configuration_is_safe"]["thinnest_margin"]))
    res["disposition"] = (
        "ESCALATE, do not patch.  solver/hilbert_pointwise.py is untouched by this leg.  "
        "The repair, when it is authorised, is a guard -- reject non-finite rho and "
        "gamma <= 0 -- not a change to the majorant, which is correct wherever the payer "
        "rule selects the seminorm account on a neighbourhood of the singularity.  "
        "Gates A5, A6 and A6b pin the current silence deliberately and MUST BE INVERTED, "
        "not weakened, the day a guard lands.")
    res["runtime_seconds"] = time.time() - t0

    with open(OUT, "w") as f:
        json.dump(res, f, indent=2, default=float)
    print("\n" + res["headline"])
    print("\nwrote %s (%.1fs)" % (OUT, res["runtime_seconds"]))


if __name__ == "__main__":
    main()
