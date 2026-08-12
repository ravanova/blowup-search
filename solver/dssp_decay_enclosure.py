"""A CERTIFIED far-field decay exponent enclosure — the instrument
`CLAY_OBLIGATIONS.md` §4 asks for and §6 item 1 records as missing.

WHY THIS MODULE EXISTS.  `solver/dssp_screen.py` records a *fitted* far-field decay
exponent per candidate (`fitted_far_field_decay_exponent`, a bare `np.polyfit` of
`log|V|` against `log r` over `np.logspace(1,3,12)`).  `CLAY_OBLIGATIONS.md` §4 is
explicit that this is not sufficient: "the admissible cutoff radius and the size of
the perturbation the cutoff introduces are both functions of it", so the exponent has
to come with a rigorous error bar, not a residual.  This module supplies the bound.
It does NOT replace the fitted routine and does not import it; `dssp_screen.py` is
untouched, and the intended use is that both columns are recorded side by side.

WHAT IS CERTIFIED, STATED BEFORE ANY CODE (leg 382 pre-registration §1).  For a
supplied positive profile magnitude ``f`` on a radial window ``[R0, R1]``:

    P_cert(f, R0, R1) := { p >= 0 : there is C > 0 with C * r**(-p) == f(r)
                                    for ALL r in [R0, R1] }

The routines below return an **outer enclosure** ``[p_lo, p_hi] ⊇ P_cert``, or the
verdict ``EMPTY`` (a PROOF that no power law of any exponent in the search bracket
fits the profile on the window), or ``INCAPACITY``.

Read the asymmetry, because it is the whole honesty of the instrument:

  * ``EMPTY`` is a proof of a negative.  It says: no exponent works.
  * a nonempty ``[p_lo, p_hi]`` is NOT a proof that the profile is a power law.
    It says only: no exponent outside this interval can be one.  A profile with
    an exactly-power-law envelope and a wiggle inside the tube is not excluded.

That asymmetry is why this is a usable instrument for §4 rather than a dressed-up
fit: the number a cutoff analysis needs is a *bound* on the exponent, and a bound is
exactly what an outer enclosure of `P_cert` is.

THE METHOD (elementary, and claimed as such -- see writeup/novelty/leg_382.md, which
states plainly that no novel mathematics is claimed here).  Put ``t = log r`` and
``g = log f``.  A power law is the affine relation ``g(t) = c - p t`` in the two
unknowns ``(c, p)``, with ``c = log C``.  Enclose ``g`` over the window; each
enclosure gives linear inequalities in ``(c, p)``; eliminate the nuisance amplitude
``c`` by Fourier--Motzkin, which is EXACT in two variables, and what survives is
exactly the projection of the feasible set onto the ``p`` axis.  Concretely, for
constraint points ``k`` and ``m``,

    g_lo_k + p * t_lo_k  <=  c  <=  g_hi_m + p * t_hi_m
        <==>   p * (t_lo_k - t_hi_m)  <=  g_hi_m - g_lo_k
        <==>   p * A_km <= B_km ,

an explicit half-line in ``p`` for every ordered pair.  Their intersection with the
search bracket is the answer.  Directed rounding is applied OUTWARD (lower bounds
pushed down, upper bounds pushed up), so the computed set contains the true one;
emptiness is therefore proved on a RELAXED system and holds a fortiori on the exact
one.  Pairs whose ``A`` enclosure straddles zero are DROPPED, which can only enlarge
the returned set -- conservative in the same direction.

TWO MODES, AND THEY ANSWER DIFFERENT QUESTIONS.

  * ``mode="cells"`` -- the window is cut into ``n_cells`` geometric cells and the
    profile is evaluated over each WHOLE CELL in interval arithmetic.  The resulting
    statement covers every ``r`` in ``[R0, R1]``; there is no gap between samples for
    the profile to wiggle through.  **This is the mode whose statement matches
    "on a stated radial window", and it is the one leg 382's gate was decided on.**
  * ``mode="nodes"`` -- the profile is evaluated at exact nodes.  Much tighter (the
    width falls to the rounding floor) but the statement is strictly WEAKER: only
    "consistent with r**(-p) at these nodes".  Provided as a tightness reference so a
    caller can see how much of a certified width is cell coverage and how much is
    floating point.  Never quote a `nodes` width as a certified decay bound.

DOMAIN RESTRICTION, DECLARED NOT HIDDEN.  The search runs over ``p in [0, 12]`` by
default.  Fixing ``p >= 0`` is what makes ``max_{t in T} (p t)`` attain at a fixed
endpoint, hence every constraint linear in ``p``; it also requires ``R0 > 1`` so that
every ``t = log r`` is positive.  Both are checked.  A feasible set that touches
either bracket end is reported as ``INCAPACITY``, never as a bound -- a bracket end
is an artefact of the search, not a property of the profile.

WHAT THIS MODULE DOES NOT DO, so nothing downstream over-reads it:

  * It does not produce a profile.  It CONSUMES one.  No profile of route 4's object
    exists in this repository, so the only inputs validated here are planted analytic
    knowns (below).
  * It does not perform the admissible-cutoff analysis.  `CLAY_OBLIGATIONS.md` §4
    requires the certified exponent AND the cutoff radius AND the size of the
    perturbation the cutoff introduces.  This module is the first of those three.
    §6 item 1 does not close.
  * It proves no existence.  There is no function space here, no truncation, no
    approximate inverse, no Newton step and no radii polynomial -- it is not, and
    cannot be turned into, the machinery `plan_of_record.py` bans.

SUBSTRATE.  `solver/interval.py` (`Interval`, `ilog`, outward-rounded arithmetic) --
the existing capability, reused rather than re-written.  The single new primitive is
`isqrt`, one outward-rounded `np.sqrt`, and it is needed only by the planted-profile
GENERATOR (for half-integer exponents), never by the enclosure itself.
"""

import numpy as np

from solver.interval import Interval, ilog, _down, _up

__all__ = [
    "isqrt", "ipow_half_integer",
    "planted_power_law", "planted_two_power", "planted_rational_cutoff",
    "planted_log_corrected", "planted_perturbed", "planted_curvature",
    "radial_field_fn",
    "certified_decay_interval", "certified_decay_from_cell_enclosures",
    "critical_tolerance",
    "VERDICT_INTERVAL", "VERDICT_EMPTY", "VERDICT_INCAPACITY",
]

VERDICT_INTERVAL = "INTERVAL"
VERDICT_EMPTY = "EMPTY"
VERDICT_INCAPACITY = "INCAPACITY"

DEFAULT_P_BRACKET = (0.0, 12.0)


# ---------------------------------------------------------------------------
# 0.  the one added interval primitive, and integer/half-integer powers
# ---------------------------------------------------------------------------

def isqrt(x):
    """Enclosure of sqrt for a positive Interval.

    `np.sqrt` is correctly rounded by IEEE-754, so the true square root of each
    endpoint lies within one ulp of the computed value; pushing the endpoints
    outward by one ulp is therefore rigorous.  sqrt is increasing, so the
    enclosure is endpointwise."""
    if not isinstance(x, Interval):
        x = Interval.point(np.asarray(x, dtype=float))
    if np.any(np.asarray(x.lo) < 0.0):
        raise ValueError("isqrt: interval reaches below zero")
    return Interval(_down(np.sqrt(x.lo)), _up(np.sqrt(x.hi)))


def _ipow_int(x, n):
    """x**n for integer n >= 0, by binary exponentiation in interval arithmetic."""
    if n < 0:
        raise ValueError("_ipow_int: n must be >= 0")
    result = Interval.point(np.ones_like(np.asarray(x.lo, dtype=float)))
    base = x
    while n:
        if n & 1:
            result = result * base
        n >>= 1
        if n:
            base = base * base
    return result


def ipow_half_integer(x, p):
    """Enclosure of ``x**p`` for a POSITIVE interval x and p a non-negative
    multiple of 1/2.

    Restricted to half-integers on purpose: `solver/interval.py` has `ilog` but no
    `iexp`, and rather than write a new transcendental (and have to prove its
    remainder) this module stays inside operations the substrate already proves --
    multiplication and a correctly-rounded sqrt.  THE RESTRICTION IS ON THE PLANTED
    PROFILE GENERATOR ONLY.  The enclosure routines below accept any interval-valued
    callable whatsoever, and place no restriction on the exponent they can certify:
    `certified_decay_interval` searches the continuum ``p in [0, 12]``."""
    twice = round(2.0 * p)
    if abs(2.0 * p - twice) > 1e-12 or twice < 0:
        raise ValueError(f"ipow_half_integer: p={p} is not a non-negative half-integer")
    out = _ipow_int(x, twice // 2)
    if twice % 2:
        out = out * isqrt(x)
    return out


# ---------------------------------------------------------------------------
# 1.  planted analytic knowns and planted mismatched controls
# ---------------------------------------------------------------------------
#
# Each generator returns a pair of callables ``(iv_fn, float_fn)`` evaluating the
# SAME profile magnitude: `iv_fn` on an `Interval` (what the enclosure consumes),
# `float_fn` on a float array (what `dssp_screen.fitted_far_field_decay_exponent`
# consumes, via `radial_field_fn`).  Keeping them paired is deliberate: it is what
# makes the fitted and certified columns provably measurements of one object rather
# than of two profiles that merely share a name.

def planted_power_law(C, p):
    """f(r) = C * r**(-p).  EXACT power law; its exponent is exactly ``p``."""
    def iv_fn(R):
        return Interval.point(np.asarray(float(C))) / ipow_half_integer(R, p)

    def float_fn(r):
        return float(C) * np.asarray(r, dtype=float) ** (-float(p))

    return iv_fn, float_fn


def planted_two_power(C1, p1, C2, p2):
    """f(r) = C1 r**(-p1) + C2 r**(-p2).  NOT a power law when C1,C2 != 0 and
    p1 != p2: the local log-log slope runs from p_max to p_min across any window
    containing the crossover ``r* = (C2/C1)**(1/(p1-p2))``."""
    a, b = planted_power_law(C1, p1)
    c, d = planted_power_law(C2, p2)

    def iv_fn(R):
        return a(R) + c(R)

    def float_fn(r):
        return b(r) + d(r)

    return iv_fn, float_fn


def planted_rational_cutoff(C, p, r_c, m=4):
    """f(r) = C r**(-p) / (1 + (r/r_c)**m).  Models a far-field cutoff -- exactly
    the structural mismatch §4's localisation step would introduce -- and is
    deliberately RATIONAL so its interval extension needs no transcendental beyond
    what `solver/interval.py` already proves.  Log-log slope runs p -> p+m."""
    base_iv, base_fl = planted_power_law(C, p)

    def iv_fn(R):
        denom = Interval.point(np.asarray(1.0)) + _ipow_int(R / Interval.point(np.asarray(float(r_c))), int(m))
        return base_iv(R) / denom

    def float_fn(r):
        r = np.asarray(r, dtype=float)
        return base_fl(r) / (1.0 + (r / float(r_c)) ** int(m))

    return iv_fn, float_fn


def planted_log_corrected(C, p):
    """f(r) = C r**(-p) log r.  A subtle mismatch: the effective slope is
    p - 1/log r, which over [10,1000] moves only from about p-0.43 to p-0.14."""
    base_iv, base_fl = planted_power_law(C, p)

    def iv_fn(R):
        return base_iv(R) * ilog(R)

    def float_fn(r):
        r = np.asarray(r, dtype=float)
        return base_fl(r) * np.log(r)

    return iv_fn, float_fn


def planted_perturbed(C, p, eps, R1):
    """f(r) = C r**(-p) * (1 + eps * (r/R1 - 1/2)).

    An EXACT power law multiplied by a bounded, non-oscillatory relative
    perturbation of size at most |eps|/2.  Its purpose is to answer the question a
    future consumer will actually have: how clean does a numerical profile have to
    be before the certified interval is narrow enough to use?  The truth ``p``
    remains inside the enclosure for every eps -- a violation of that would be a
    SOUNDNESS DEFECT in the instrument, not a property of the profile."""
    base_iv, base_fl = planted_power_law(C, p)
    half = Interval.point(np.asarray(0.5))

    def iv_fn(R):
        shape = R / Interval.point(np.asarray(float(R1))) - half
        return base_iv(R) * (Interval.point(np.asarray(1.0)) + Interval.point(np.asarray(float(eps))) * shape)

    def float_fn(r):
        r = np.asarray(r, dtype=float)
        return base_fl(r) * (1.0 + float(eps) * (r / float(R1) - 0.5))

    return iv_fn, float_fn


def planted_curvature(C, p, kappa, t_mid):
    """f(r) = C r**(-p) * (1 + kappa * (log r - t_mid)**2).

    Curvature in the log-log plane is the single thing a power law cannot have, so
    sweeping ``kappa`` measures the instrument's DETECTION THRESHOLD directly: the
    smallest departure from a straight log-log line it can certify as impossible."""
    base_iv, base_fl = planted_power_law(C, p)

    def iv_fn(R):
        d = ilog(R) - Interval.point(np.asarray(float(t_mid)))
        return base_iv(R) * (Interval.point(np.asarray(1.0))
                             + Interval.point(np.asarray(float(kappa))) * (d * d))

    def float_fn(r):
        r = np.asarray(r, dtype=float)
        return base_fl(r) * (1.0 + float(kappa) * (np.log(r) - float(t_mid)) ** 2)

    return iv_fn, float_fn


_DEFAULT_DIRECTION = (0.4, 0.5, float(np.sqrt(1.0 - 0.4 ** 2 - 0.5 ** 2)))


def radial_field_fn(float_fn, direction=_DEFAULT_DIRECTION):
    """Lift a scalar radial magnitude to a 3D vector field V(x) = f(|x|) * e_hat.

    |V| = f(r) exactly, so `dssp_screen.fitted_far_field_decay_exponent` run on this
    field measures the SAME profile the enclosure measures.  The default direction is
    `dssp_screen`'s own generic off-axis ray, unchanged, so the fitted column is
    produced by that module's default configuration and not by a tuned one."""
    e = np.asarray(direction, dtype=float)
    e = e / np.linalg.norm(e)

    def field_fn(pts):
        pts = np.asarray(pts, dtype=float)
        r = np.linalg.norm(pts, axis=-1)
        return float_fn(r)[..., None] * e[None, :]

    return field_fn


# ---------------------------------------------------------------------------
# 2.  the enclosure
# ---------------------------------------------------------------------------

def _fourier_motzkin_p_range(t_lo, t_hi, g_lo, g_hi, p_bracket, block=256):
    """Exact elimination of the amplitude, with outward rounding.

    Constraint k:  c - p*t_k in [g_lo_k, g_hi_k]  with t_k in [t_lo_k, t_hi_k].
    Since p >= 0 on the search bracket, relax to the fixed endpoints

        c <= g_hi_k + p*t_hi_k        and        c >= g_lo_k + p*t_lo_k,

    which is a valid weakening (it can only enlarge the feasible set).  Feasibility
    in c for a given p is then ``max_k(lower) <= min_m(upper)``, i.e. for every
    ordered pair (k, m):  p*(t_lo_k - t_hi_m) <= g_hi_m - g_lo_k.  Each pair is one
    half-line in p; their intersection is the exact projection.

    Pairs whose A-enclosure straddles zero carry no usable half-line and are
    DROPPED.  Dropping constraints enlarges the set, so the result stays an OUTER
    enclosure; the count is returned so the caller can see it was not silent."""
    K = int(len(t_lo))
    p_lo, p_hi = float(p_bracket[0]), float(p_bracket[1])
    n_dropped = 0
    n_pairs = 0
    for s in range(0, K, block):
        e = min(s + block, K)
        a = t_lo[:, None] - t_hi[None, s:e]
        b = g_hi[None, s:e] - g_lo[:, None]
        a_lo, a_hi = _down(a), _up(a)
        b_lo, b_hi = _down(b), _up(b)
        n_pairs += a.size
        pos = a_lo > 0.0
        neg = a_hi < 0.0
        n_dropped += int(np.count_nonzero(~(pos | neg)))
        if np.any(pos):
            q = Interval(b_lo[pos], b_hi[pos]) / Interval(a_lo[pos], a_hi[pos])
            p_hi = min(p_hi, float(np.min(q.hi)))
        if np.any(neg):
            q = Interval(b_lo[neg], b_hi[neg]) / Interval(a_lo[neg], a_hi[neg])
            p_lo = max(p_lo, float(np.max(q.lo)))
    return p_lo, p_hi, n_dropped, n_pairs


def certified_decay_from_cell_enclosures(r_lo, r_hi, f_lo, f_hi,
                                         p_bracket=DEFAULT_P_BRACKET,
                                         rel_tolerance=0.0):
    """The entry point a future profile-producing unit should call.

    Inputs are CERTIFIED CELL ENCLOSURES: cell ``i`` spans radii ``[r_lo[i], r_hi[i]]``
    and the profile magnitude satisfies ``f_lo[i] <= f(r) <= f_hi[i]`` for EVERY r in
    that cell.  Supplying those is the caller's obligation and this routine cannot
    check it -- if the caller has only pointwise samples, it must first convert them
    using a certified modulus of continuity, or a monotonicity hypothesis, and must
    state which.  That obligation is named here rather than buried, because it is
    exactly where a "certified" pipeline would otherwise leak.

    ``rel_tolerance`` (delta >= 0) relaxes the certified set from EXACT power-law
    consistency to consistency within a stated relative tolerance:

        P_cert^delta := { p >= 0 : there is C > 0 with
                          f(r)/(1+delta) <= C r**(-p) <= f(r)*(1+delta)
                          for ALL r in [R0, R1] }

    ``delta = 0`` recovers the exact set and is the default.  **Delta is not a
    fitting knob and must never be tuned until something passes.**  It is an INPUT
    the caller owes: the relative accuracy to which the caller's own profile is
    itself certified.  Leg 382 measured why it exists at all -- at ``delta = 0`` the
    set is empty for ANY profile that is not an exact power law, including one
    perturbed at the 1e-12 level, so the exact instrument cannot be applied to
    numerical data.  The honest way to use this argument is to report, alongside any
    enclosure, the CRITICAL TOLERANCE at which a known mismatch would stop being
    excluded; leg 382 measures those for its controls.

    Returns a dict; see `certified_decay_interval` for the fields."""
    r_lo = np.asarray(r_lo, dtype=float)
    r_hi = np.asarray(r_hi, dtype=float)
    f_lo = np.asarray(f_lo, dtype=float)
    f_hi = np.asarray(f_hi, dtype=float)
    if np.any(r_lo <= 1.0):
        raise ValueError("certified_decay: the window must satisfy r > 1 (log r > 0), "
                         "which is what fixes the sign in the p >= 0 relaxation")
    if np.any(f_lo <= 0.0):
        return {"verdict": VERDICT_INCAPACITY,
                "reason": "profile enclosure touches or crosses zero; log is undefined",
                "p_lo": None, "p_hi": None, "width": None,
                "n_cells": int(len(r_lo)), "n_constraints": 0,
                "n_pairs": 0, "n_dropped": 0,
                "max_log_tube_width": None,
                "p_bracket": [float(p_bracket[0]), float(p_bracket[1])]}

    delta = float(rel_tolerance)
    if delta < 0.0:
        raise ValueError("rel_tolerance must be >= 0")
    if delta > 0.0:
        one_plus = Interval.point(np.asarray(1.0 + delta))
        f_lo_new = (Interval(f_lo, f_lo) / one_plus).lo
        f_hi_new = (Interval(f_hi, f_hi) * one_plus).hi
        f_lo, f_hi = f_lo_new, f_hi_new

    G = ilog(Interval(f_lo, f_hi))
    T_lo = ilog(Interval.point(r_lo))
    T_hi = ilog(Interval.point(r_hi))
    t_lo = np.concatenate([T_lo.lo, T_hi.lo])
    t_hi = np.concatenate([T_lo.hi, T_hi.hi])
    g_lo = np.concatenate([G.lo, G.lo])
    g_hi = np.concatenate([G.hi, G.hi])

    p_lo, p_hi, n_dropped, n_pairs = _fourier_motzkin_p_range(
        t_lo, t_hi, g_lo, g_hi, p_bracket)

    out = {"n_cells": int(len(r_lo)),
           "n_constraints": int(len(t_lo)),
           "n_pairs": int(n_pairs),
           "n_dropped": int(n_dropped),
           "max_log_tube_width": float(np.max(G.hi - G.lo)),
           "p_bracket": [float(p_bracket[0]), float(p_bracket[1])],
           "rel_tolerance": delta,
           "window": [float(np.min(r_lo)), float(np.max(r_hi))],
           "leverage_log_ratio": float(np.log(np.max(r_hi) / np.min(r_lo)))}

    # A profile whose exponent lies OUTSIDE the search bracket also drives p_lo past
    # p_hi, and calling that EMPTY would be a lie of exactly the kind this module
    # exists to prevent: it would report "no power law" for a perfectly good power
    # law that merely sits outside the bracket.  Diagnose it separately and report
    # INCAPACITY, which is the weaker and therefore honest verdict.
    if p_lo > p_bracket[1] or p_hi < p_bracket[0]:
        out.update({"verdict": VERDICT_INCAPACITY,
                    "reason": ("the constraints force the exponent OUTSIDE the search "
                               "bracket [%g, %g] (projection gave p_lo %.17g, p_hi %.17g); "
                               "widen the bracket and re-run — this is NOT a statement that "
                               "the profile has no power-law exponent"
                               % (p_bracket[0], p_bracket[1], p_lo, p_hi)),
                    "p_lo": float(p_lo), "p_hi": float(p_hi),
                    "width": float(p_hi - p_lo)})
        return out

    if p_lo > p_hi:
        out.update({"verdict": VERDICT_EMPTY,
                    "reason": ("no exponent in the search bracket is consistent with the "
                               "profile on this window: the Fourier-Motzkin projection is "
                               "empty (p_lo %.17g > p_hi %.17g)" % (p_lo, p_hi)),
                    "p_lo": float(p_lo), "p_hi": float(p_hi),
                    "width": float(p_hi - p_lo)})
        return out

    touches_lo = p_lo <= p_bracket[0]
    touches_hi = p_hi >= p_bracket[1]
    if touches_lo or touches_hi:
        out.update({"verdict": VERDICT_INCAPACITY,
                    "reason": ("the projection reaches the search bracket "
                               f"({'lower' if touches_lo else ''}"
                               f"{'/' if touches_lo and touches_hi else ''}"
                               f"{'upper' if touches_hi else ''} end); a bracket end is an "
                               "artefact of the search, not a bound on the profile"),
                    "p_lo": float(p_lo), "p_hi": float(p_hi),
                    "width": float(p_hi - p_lo)})
        return out

    out.update({"verdict": VERDICT_INTERVAL, "reason": "",
                "p_lo": float(p_lo), "p_hi": float(p_hi),
                "width": float(p_hi - p_lo)})
    return out


def certified_decay_interval(profile_iv_fn, r0, r1, n_cells=1000, mode="cells",
                             p_bracket=DEFAULT_P_BRACKET, rel_tolerance=0.0):
    """Certified enclosure of the decay exponent of ``profile_iv_fn`` on [r0, r1].

    ``profile_iv_fn`` takes an `Interval` of radii and returns an `Interval`
    enclosing the profile magnitude over it.

    ``mode="cells"`` (default, and the only mode whose statement covers the whole
    window) evaluates over whole cells; ``mode="nodes"`` evaluates at exact nodes and
    its far narrower answer is a strictly WEAKER statement -- see the module
    docstring.  Returns a dict with keys ``verdict`` (INTERVAL / EMPTY / INCAPACITY),
    ``p_lo``, ``p_hi``, ``width``, ``max_log_tube_width``, ``n_cells``,
    ``n_constraints``, ``n_pairs``, ``n_dropped``, ``leverage_log_ratio``, ``mode``."""
    if mode not in ("cells", "nodes"):
        raise ValueError("mode must be 'cells' or 'nodes'")
    edges = np.geomspace(float(r0), float(r1), int(n_cells) + 1)
    if mode == "cells":
        lo, hi = edges[:-1], edges[1:]
        F = profile_iv_fn(Interval(lo, hi))
        res = certified_decay_from_cell_enclosures(lo, hi, F.lo, F.hi, p_bracket,
                                                   rel_tolerance)
    else:
        F = profile_iv_fn(Interval.point(edges))
        res = certified_decay_from_cell_enclosures(edges, edges, F.lo, F.hi, p_bracket,
                                                   rel_tolerance)
    res["mode"] = mode
    return res


def critical_tolerance(profile_iv_fn, r0, r1, n_cells=1000, mode="cells",
                       p_bracket=DEFAULT_P_BRACKET, hi=10.0, iters=60):
    """The smallest relative tolerance ``delta*`` at which the profile stops being
    certified EMPTY -- i.e. how accurately a numerical profile must be known before
    THIS mismatch can still be excluded.

    Monotone by construction: increasing ``delta`` only widens the tube, hence only
    enlarges the feasible set, so "EMPTY" is a downward-closed property of delta and
    plain bisection locates the transition.  Returns ``(delta_lo, delta_hi)``
    bracketing it, with EMPTY certified at ``delta_lo`` and not at ``delta_hi``; a
    returned ``delta_hi`` equal to the search ceiling means the mismatch is excluded
    at every tolerance tried, which is the strongest outcome available.

    This is the number that makes the instrument reportable rather than brittle:
    quoting a certified exponent without it would hide that at ``delta = 0`` the
    enclosure rejects essentially every profile, exact-power-law or not."""
    def is_empty(d):
        return certified_decay_interval(profile_iv_fn, r0, r1, n_cells, mode,
                                        p_bracket, d)["verdict"] == VERDICT_EMPTY

    if not is_empty(0.0):
        return (0.0, 0.0)
    if is_empty(hi):
        return (float(hi), float("inf"))
    a, b = 0.0, float(hi)
    for _ in range(int(iters)):
        m = 0.5 * (a + b)
        if is_empty(m):
            a = m
        else:
            b = m
    return (a, b)
