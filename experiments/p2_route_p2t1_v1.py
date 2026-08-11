"""Route-P2T1 v1 (leg 302) — the validation battery for apparatus term A4 (gamma-law pressure).

Self-contained: term A4 is inlined below (see the banner) and this runner is the *measurement*
— eleven known-answer probes with tolerances fixed in advance (`experiments/journal/leg_302.md`
Part 1, committed before this file existed), five negative controls that can fail, and two
deliberate plants swept for their per-probe DETECTION THRESHOLD.

The gate's second half is the reason the plants exist: a battery that reproduces every known
answer but cannot notice a corrupted constant is measuring the code, not the constant.  So the
deliverable is a probe x plant matrix with a magnitude in every cell, blind cells included.

    .venv/bin/python experiments/p2_route_p2t1_v1.py
    .venv/bin/python experiments/p2_route_p2t1_v1.py --figure writeup/figures/figNN_route_p2t1_v1_sensitivity.png

Writes `writeup/data/p2_route_p2t1_v1.json`.  Deterministic; no randomness anywhere.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# ===========================================================================
# TERM A4 -- INLINED, DELIBERATELY NOT BANKED AS solver/p2_apparatus_term1.py
# ---------------------------------------------------------------------------
# The pre-committed gate's *yes* branch is what banks a module ('yes -> Bank
# module + battery').  This leg's gate came out NO (journal leg_302.md Part 4:
# KA8 at 129.048x its 1e-9 tolerance), so the term is NOT promoted into
# solver/ and NOT registered as a capability.  It lives here, inside its own
# measurement, where it is reproducible but not advertised as trusted.
# The capabilities.py entry a future leg should use IF it re-banks this term
# -- caveat and all -- is written out in journal leg_302.md Sec.5.1.
#
# The provenance docstring below is the term's own, carried over verbatim.
# ===========================================================================

TERM_A4_PROVENANCE = """Term A4 of leg 285's fifteen-term apparatus spec: the adiabatic / gamma-law pressure.

WHAT THIS IS
------------
Leg 285 (ROUTE-P2S) turned leg 265's *count* of the apparatus a BCG-style imploding-profile
certificate would need into a per-term *bill of materials*: 16 records, 7 dependency layers,
critical path ``A4 -> A1 -> A2 -> A9 -> A8 -> A13 -> A14`` of depth 7.  This module implements
**exactly one** of those records -- **A4**, the head of that critical path, whose own spec row
reads "the barotropic pressure law and the two constants every other term is a function of".

It is a **float dress rehearsal**, not a certificate: everything here is IEEE double arithmetic.
``solver/interval.py`` is the repository's interval substrate and is deliberately *not* used --
term A15a (ball arithmetic) is a different record of the same spec and is not built here.

WHAT THIS IS NOT
----------------
None of A1, A2, A3, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15a, A15b is built, and no
claim is made on any of them.  Nothing in this file integrates an ODE, assembles a Jacobian,
constructs a phase portrait, locates ``P_s``, evaluates the dissipative forcing ``F_dis``, or
builds a profile.

The ``consumer layer`` below (``delta_dis``, ``r_min_*``, ``r_star``, ``k``) is **scalar algebra
on (gamma, r)**, transcribed from closed forms *printed in* BCG, and exists for one purpose: to
validate A4's two constants by pushing them through published formulas whose answers are known
in advance.  Evaluating BCG's closed form for ``k(r)`` is not a construction of A2 any more than
quoting it would be; A2's content is the ODE system, which does not appear.

SOURCE, PINNED
--------------
Buckmaster-Cao-Labarbe-Gomez, "Smooth imploding solutions for 3D compressible fluids",
``arXiv:2208.09445``; e-print md5 ``45ea63c45a1a199ecfb4dc4a15431600``, 6898 TeX lines (a sixth
bit-identical independent download; see ``writeup/novelty/leg_302.md`` Sec.5).  Line numbers below
are into that file.

    eq:Euler / ideal gas law   l.134, l.140-141   p(rho) = rho^gamma / gamma,  gamma > 1
    sigma, alpha              l.180              sigma = alpha^-1 rho^alpha,  alpha = (gamma-1)/2
    eq:rstar                  l.353-357          r*(gamma), two branches split at gamma = 5/3
    eq:delta:dis              l.489-491          -delta_dis = 2 - r + (1-r)/alpha < 0
    eq:r:restriction          l.493-495          equivalently r > 2 gamma / (gamma + 1)
    gamma ceiling             l.497-499          r_min < r*  <=>  gamma < 1 + 2/sqrt(3)
    eq:R1                     l.526-528          R_1(gamma, r)
    eq:W1Z1 / eq:def_R2       l.543-550          R_2(gamma, r)
    lemma:k / eq:k_asquotientDZ1  l.579, l.600   k(r) = checkD_{Z,1} / D_{Z,1}

THE TWO PLANTS
--------------
``alpha_scale`` and ``sqrt3_scale`` are **deliberate defect injectors**, both 1.0 by default.
They exist so the leg's controls can come out differently (lesson 90): with ``alpha_scale =
1+eps`` every quantity that genuinely depends on A4's constant moves, and every quantity that
does not stays put -- which is exactly the distinction the validation battery is there to expose.
They are not tuning knobs and no result is ever reported at a non-unit plant except as a
detection threshold.

Leg 302.  Territory: this file is NEW; no existing solver file is edited, and ``capabilities.py``
is not edited (leg 292 owns it this roster; registration is an integration note in
``experiments/journal/leg_302.md`` Sec.5).
"""

import math
from dataclasses import dataclass, field

__all__ = [
    "GammaLawError",
    "GammaLaw",
    "GAMMA_AIR",
    "GAMMA_MONATOMIC",
    "GAMMA_CEILING",
]

# The target's own gamma (BCG work the case gamma = 7/5 throughout) and the monatomic case
# used by the independent-group control paper (SWWZ arXiv:2501.15701, gamma = 5/3).
GAMMA_AIR = 7.0 / 5.0
GAMMA_MONATOMIC = 5.0 / 3.0

# BCG l.497-499: r_min < r* requires gamma < 1 + 2/sqrt(3).  Published closed form.
GAMMA_CEILING = 1.0 + 2.0 / math.sqrt(3.0)


class GammaLawError(ValueError):
    """Raised when an input leaves the domain on which term A4 is defined."""


def _finite(name: str, x: float) -> float:
    x = float(x)
    if not math.isfinite(x):
        raise GammaLawError("%s must be finite, got %r" % (name, x))
    return x


@dataclass(frozen=True)
class GammaLaw:
    """Term A4: the barotropic gamma-law pressure and the constants alpha, 1/alpha.

    Parameters
    ----------
    gamma : float
        Adiabatic exponent, ``gamma > 1`` (BCG l.141: "the ideal gas law p(rho) =
        rho^gamma/gamma for gamma > 1").  ``gamma <= 1`` is rejected, not clamped: at
        ``gamma = 1`` the constant ``alpha`` vanishes and the dissipative multiplier
        ``S^{-1/alpha}`` has a pole of infinite order, so there is no term to build.
    alpha_scale, sqrt3_scale : float
        Defect injectors, both 1.0 in every reported configuration.  See the module docstring.
    """

    gamma: float
    alpha_scale: float = 1.0
    sqrt3_scale: float = 1.0
    # populated in __post_init__ so the frozen dataclass stays cheap to evaluate
    alpha: float = field(init=False)
    one_over_alpha: float = field(init=False)

    def __post_init__(self) -> None:
        gamma = _finite("gamma", self.gamma)
        if gamma <= 1.0:
            raise GammaLawError(
                "gamma must be > 1 (BCG l.141); got %r.  At gamma <= 1 the constant "
                "alpha = (gamma-1)/2 is non-positive and the multiplier S^{-1/alpha} is "
                "not a finite-order pole." % gamma
            )
        a_scale = _finite("alpha_scale", self.alpha_scale)
        s_scale = _finite("sqrt3_scale", self.sqrt3_scale)
        if a_scale <= 0.0:
            raise GammaLawError("alpha_scale must be > 0, got %r" % a_scale)
        alpha = 0.5 * (gamma - 1.0) * a_scale
        object.__setattr__(self, "gamma", gamma)
        object.__setattr__(self, "alpha_scale", a_scale)
        object.__setattr__(self, "sqrt3_scale", s_scale)
        object.__setattr__(self, "alpha", alpha)
        object.__setattr__(self, "one_over_alpha", 1.0 / alpha)

    # ---------------------------------------------------------------- A4 proper

    def pressure(self, rho: float) -> float:
        """p(rho) = rho^gamma / gamma.  BCG l.140-141."""
        rho = _finite("rho", rho)
        if rho <= 0.0:
            raise GammaLawError(
                "rho must be > 0, got %r -- the vacuum is exactly the state term A5's "
                "lower bound S_min > 0 exists to exclude." % rho
            )
        return rho ** self.gamma / self.gamma

    def dpressure(self, rho: float) -> float:
        """p'(rho) = rho^(gamma-1).  Monotone increasing pressure law."""
        rho = _finite("rho", rho)
        if rho <= 0.0:
            raise GammaLawError("rho must be > 0, got %r" % rho)
        return rho ** (self.gamma - 1.0)

    def sound_speed(self, rho: float) -> float:
        """c(rho) = sqrt(p'(rho)) = rho^alpha_true, with alpha_true = (gamma-1)/2.

        Note this uses the *thermodynamic* exponent rather than ``self.alpha``: the sound speed
        is defined by the pressure law, so PLANT-alpha must not silently rewrite it.  The
        constant that PLANT-alpha moves is the one BCG's self-similar bookkeeping uses.
        """
        return math.sqrt(self.dpressure(rho))

    def sigma(self, rho: float) -> float:
        """Rescaled sound speed sigma = alpha^-1 rho^alpha.  BCG l.180.

        A5 owns the *change of unknowns*; this is A4's constant applied to a density, exposed so
        A5 has something to consume, and is not a construction of A5.
        """
        rho = _finite("rho", rho)
        if rho <= 0.0:
            raise GammaLawError("rho must be > 0, got %r" % rho)
        return rho ** self.alpha / self.alpha

    def dissipative_multiplier(self, S: float) -> float:
        """S^{-1/alpha}: the multiplier whose pole order at the vacuum is 1/alpha.

        At gamma = 7/5 the order is 5; it diverges as gamma -> 1+.
        """
        S = _finite("S", S)
        if S <= 0.0:
            raise GammaLawError(
                "S must be > 0, got %r -- S^{-1/alpha} is a pole of order %.6g there."
                % (S, self.one_over_alpha)
            )
        return S ** (-self.one_over_alpha)

    @property
    def vacuum_pole_order(self) -> float:
        """Order of the pole of S^{-1/alpha} at the vacuum: 1/alpha."""
        return self.one_over_alpha

    # ------------------------------------------------- consumer layer (validation only)

    def delta_dis(self, r: float) -> float:
        """delta_dis(r) = r - 2 + (r-1)/alpha.

        BCG eq:delta:dis l.489-491 print ``-delta_dis = 2 - r + (1-r)/alpha``; this is that,
        with the sign resolved.  The dissipative term is treatable as an error iff
        ``delta_dis > 0``.  Runs through ``self.alpha``, so PLANT-alpha moves it.
        """
        r = _finite("r", r)
        return r - 2.0 + (r - 1.0) * self.one_over_alpha

    def r_min_published(self) -> float:
        """r_min = 2 gamma / (gamma + 1).  BCG eq:r:restriction l.493-495.

        Computed from gamma directly and NOT through alpha -- this is the published reference
        that the alpha-routed bisection is tested against, so it must not move with PLANT-alpha.
        """
        return 2.0 * self.gamma / (self.gamma + 1.0)

    def r_min_via_alpha(self) -> float:
        """The same threshold derived through A4's constant: (2 alpha + 1) / (1 + alpha).

        Multiplying ``2 - r + (1-r)/alpha < 0`` by ``alpha > 0`` gives ``r > (2 alpha + 1)/(1 +
        alpha)``, which equals ``2 gamma/(gamma+1)`` exactly when ``alpha = (gamma-1)/2``.  That
        identity is the point: it is the algebraic link BCG assert with the word "equivalently",
        and it is false the moment alpha is wrong.
        """
        a = self.alpha
        return (2.0 * a + 1.0) / (1.0 + a)

    def r_min_bisected(self, lo: float = 1.0, hi: float = 64.0, iters: int = 200) -> float:
        """Zero-crossing of ``delta_dis`` in r, found by bisection rather than by formula."""
        f_lo, f_hi = self.delta_dis(lo), self.delta_dis(hi)
        if not (f_lo <= 0.0 <= f_hi):
            raise GammaLawError(
                "delta_dis does not bracket a root on [%g, %g]: f=%g,%g" % (lo, hi, f_lo, f_hi)
            )
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            if self.delta_dis(mid) <= 0.0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def r_star_branch_low(self) -> float:
        """r*(gamma) on the ``1 < gamma < 5/3`` branch: 2/(sqrt(2) sqrt(1/(gamma-1)) + 1)^2 + 1."""
        g = self.gamma
        if g <= 1.0:  # pragma: no cover - guarded in __post_init__
            raise GammaLawError("gamma must be > 1")
        return 2.0 / (math.sqrt(2.0) * math.sqrt(1.0 / (g - 1.0)) + 1.0) ** 2 + 1.0

    def r_star_branch_high(self) -> float:
        """r*(gamma) on the ``gamma >= 5/3`` branch: (3 gamma - 1)/(2 + sqrt(3)(gamma - 1)).

        PLANT-FORMULA perturbs the sqrt(3) here, and only here.
        """
        g = self.gamma
        root3 = math.sqrt(3.0) * self.sqrt3_scale
        return (3.0 * g - 1.0) / (2.0 + root3 * (g - 1.0))

    def r_star(self) -> float:
        """r*(gamma), BCG eq:rstar l.353-357, the two branches with their published split."""
        return (
            self.r_star_branch_low()
            if self.gamma < GAMMA_MONATOMIC
            else self.r_star_branch_high()
        )

    def R1(self, r: float) -> float:
        """BCG eq:R1 l.526-528."""
        g, r = self.gamma, _finite("r", r)
        inner = g * g * (r - 3.0) ** 2 - 2.0 * g * (3.0 * r * r - 6.0 * r + 7.0) + (
            9.0 * r * r - 14.0 * r + 9.0
        )
        if inner < 0.0:
            raise GammaLawError("R1 radicand negative (%g) at gamma=%g, r=%g" % (inner, g, r))
        return math.sqrt(inner)

    def R2(self, r: float) -> float:
        """BCG eq:def_R2 l.547-550.

        The leading ``1/(gamma-1)`` is written as ``1/(2 alpha)`` -- A4's own identity -- so that
        PLANT-alpha propagates into k(r) exactly as it propagates into every other consumer.
        """
        g, r = self.gamma, _finite("r", r)
        R1 = self.R1(r)
        inner = (
            g * ((76.0 - 27.0 * g) * g - 71.0)
            - (3.0 * g - 5.0) * ((g - 5.0) * g + 2.0) * r * r
            + (g * (g * (18.0 * g - 52.0) + 50.0) - 8.0) * r
            + R1 * (9.0 * (g - 2.0) * g + ((2.0 - 3.0 * g) * g + 5.0) * r + 5.0)
            + 18.0
        )
        if inner < 0.0:
            raise GammaLawError("R2 radicand negative (%g) at gamma=%g, r=%g" % (inner, g, r))
        return math.sqrt(inner) / (2.0 * self.alpha)

    def k(self, r: float) -> float:
        """BCG eq:k_asquotientDZ1 l.600.

            k(r) = (-4 + (1+gamma)(r-1)/(gamma-1) - R2) / (-4 + (1+gamma)(r-1)/(gamma-1) + R2)

        ``(gamma-1)`` is again written as ``2 alpha``.  BCG lemma:k (l.579) assert k(1) = 1,
        k'(r) > 0 on (1, r*), and k -> +infinity as r -> r*; those three are the transcription
        test of this function and are checked by the battery before k is believed anywhere else.
        """
        g, r = self.gamma, _finite("r", r)
        base = -4.0 + (1.0 + g) * (r - 1.0) / (2.0 * self.alpha)
        R2 = self.R2(r)
        den = base + R2
        if den == 0.0:
            raise GammaLawError("k(r) singular at gamma=%g, r=%g" % (g, r))
        return (base - R2) / den

    def k_high_precision(self, r: float, digits: int = 60) -> float:
        """``k(r)`` evaluated in ``digits``-digit decimal arithmetic instead of double.

        This exists because leg 302 MEASURED the double-precision evaluation of ``R2`` to be
        ill-conditioned near ``r = 1``: BCG's printed radicand is a sum of terms of magnitude up
        to 24.528 that cancels to **exactly zero** at ``r = 1``, so in IEEE double the residue is
        rounding noise of order ``24.5 * 2^-52 ~ 5e-15``, and the square root turns that into an
        absolute error of order ``7e-8`` -- i.e. ``|k(1) - 1| = 1.29e-07`` where the paper's own
        lemma says the value is 1.  Half the digits are gone, and they are gone to conditioning,
        not to a transcription error: at 60 digits the radicand is 0 and ``k(1) = 1`` exactly.

        The plants are honoured here too (``alpha_scale`` enters via ``2*alpha``), so this path is
        a *precision* variant of the same function, not a different function.
        """
        from decimal import Decimal, getcontext, localcontext

        with localcontext() as ctx:
            ctx.prec = int(digits)
            g = Decimal(repr(self.gamma))
            rr = Decimal(repr(float(r)))
            two_alpha = Decimal(2) * Decimal(repr(self.alpha))
            r1_sq = (g * g * (rr - 3) ** 2 - 2 * g * (3 * rr * rr - 6 * rr + 7)
                     + (9 * rr * rr - 14 * rr + 9))
            if r1_sq < 0:
                raise GammaLawError("R1 radicand negative at gamma=%g, r=%g" % (self.gamma, r))
            R1 = r1_sq.sqrt()
            inner = (g * ((76 - 27 * g) * g - 71)
                     - (3 * g - 5) * ((g - 5) * g + 2) * rr * rr
                     + (g * (g * (18 * g - 52) + 50) - 8) * rr
                     + R1 * (9 * (g - 2) * g + ((2 - 3 * g) * g + 5) * rr + 5)
                     + 18)
            if inner < 0:
                raise GammaLawError("R2 radicand negative at gamma=%g, r=%g" % (self.gamma, r))
            R2 = inner.sqrt() / two_alpha
            base = Decimal(-4) + (1 + g) * (rr - 1) / two_alpha
            den = base + R2
            if den == 0:
                raise GammaLawError("k(r) singular at gamma=%g, r=%g" % (self.gamma, r))
            return float((base - R2) / den)

    # ------------------------------------------------------------------ reporting

    def summary(self) -> dict:
        """Everything A4 owes its twelve downstream consumers, as plain floats."""
        return {
            "gamma": self.gamma,
            "alpha": self.alpha,
            "one_over_alpha": self.one_over_alpha,
            "vacuum_pole_order": self.vacuum_pole_order,
            "p_at_1": self.pressure(1.0),
            "sound_speed_at_1": self.sound_speed(1.0),
            "r_min_published": self.r_min_published(),
            "r_min_via_alpha": self.r_min_via_alpha(),
            "r_star": self.r_star(),
            "alpha_scale": self.alpha_scale,
            "sqrt3_scale": self.sqrt3_scale,
        }


DATA = os.path.join(ROOT, "writeup", "data", "p2_route_p2t1_v1.json")

# ---------------------------------------------------------------------------
# The references, quoted with their provenance.  Class E = BCG's printed closed
# forms (md5 45ea63c..., see writeup/novelty/leg_302.md Sec.5).  Class I = constants
# banked independently by earlier legs through a different code path.
# ---------------------------------------------------------------------------
REF = {
    "alpha_air": (0.2, "E", "BCG l.180, alpha=(gamma-1)/2 at gamma=7/5"),
    "one_over_alpha_air": (5.0, "E", "BCG l.180"),
    "window_lo": (1.1666667, "I", "leg 240 (Route-CNS2) banked dominance window, low end"),
    "window_hi": (1.1909830, "I", "leg 240, high end"),
    "window_width": (2.43e-02, "I", "leg 240, quoted to 3 significant figures"),
    "delta_dis_margin": (0.1458980, "I", "leg 240, max delta_dis on the window"),
    "r_star_at_5_3": (1.2679491924, "I", "leg 240, the value both r* branches take at gamma=5/3"),
    "gamma_ceiling": (GAMMA_CEILING, "E", "BCG l.497-499, 1 + 2/sqrt(3)"),
    "k_at_7_6": (16.3479210516613, "I", "legs 265/266, k(7/6) at gamma=7/5 in closed form"),
    "odd_branches_in_target_window": (7, "I", "leg 265 via DIRECTION.md l.11548: 3,5,...,15"),
}

# Pre-stated tolerances (journal Part 1, Sec.1.2).  Nothing here is adjusted after measurement.
TOL = {
    "KA1": 1e-14,
    "KA2": 1e-13,
    "KA3": 1e-12,
    "KA4_endpoint": 5e-8,
    "KA4_width": 5e-5,
    "KA4_margin": 5e-8,
    "KA5_branch_gap": 1e-14,
    "KA5_value": 5e-11,
    "KA6": 1e-6,
    "KA7": 1e-11,
    "KA8_k1": 1e-9,
    "KA8_blowup": 1e3,
    "KA9": 1e-9,
    "KA11": 1e-14,
    "NEG4": 1e-6,
    "NEG5": 1e-6,
}

# Pre-stated plant requirements (journal Part 1, Sec.1.3).
PLANT_ALPHA_MUST_FAIL_AT = 1e-2
PLANT_ALPHA_REQUIRED = ["KA2", "KA3", "KA4", "KA7", "KA9"]
PLANT_FORMULA_MUST_FAIL_AT = 1e-6
PLANT_FORMULA_REQUIRED = ["KA5", "KA7"]
PLANT_FORMULA_EXPECTED_BLIND = ["KA2", "KA3"]


def _law(gamma, a_scale=1.0, s_scale=1.0):
    return GammaLaw(gamma, alpha_scale=a_scale, sqrt3_scale=s_scale)


def _linspace(a, b, n):
    if n == 1:
        return [a]
    step = (b - a) / (n - 1)
    return [a + step * i for i in range(n)]


def _bisect(f, lo, hi, iters=200):
    """Sign-change bisection; f(lo) and f(hi) must straddle zero."""
    f_lo, f_hi = f(lo), f(hi)
    if f_lo == 0.0:
        return lo
    if f_hi == 0.0:
        return hi
    if (f_lo > 0.0) == (f_hi > 0.0):
        raise GammaLawError("no sign change on [%g, %g]: %g, %g" % (lo, hi, f_lo, f_hi))
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0.0) == (f_lo > 0.0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ===========================================================================
# The eleven known-answer probes.  Each returns (residual, tolerance, detail-dict).
# A probe PASSES iff residual <= tolerance.  Residuals are magnitudes, not booleans.
# ===========================================================================

def ka1(a=1.0, s=1.0):
    """alpha(7/5) = 1/5 and 1/alpha = 5, exactly."""
    gl = _law(GAMMA_AIR, a, s)
    r_alpha = abs(gl.alpha - REF["alpha_air"][0]) / REF["alpha_air"][0]
    r_inv = abs(gl.one_over_alpha - REF["one_over_alpha_air"][0]) / REF["one_over_alpha_air"][0]
    res = max(r_alpha, r_inv)
    return res, TOL["KA1"], {"alpha": gl.alpha, "one_over_alpha": gl.one_over_alpha,
                             "rel_alpha": r_alpha, "rel_one_over_alpha": r_inv}


def ka2(a=1.0, s=1.0):
    """At gamma=7/5, delta_dis(r) collapses to the line 6r-7 (1/alpha = 5)."""
    gl = _law(GAMMA_AIR, a, s)
    grid = _linspace(1.0, 1.25, 201)
    dev = [abs(gl.delta_dis(r) - (6.0 * r - 7.0)) for r in grid]
    return max(dev), TOL["KA2"], {"n_points": len(grid), "max_abs_dev": max(dev),
                                  "at_r_1p1": gl.delta_dis(1.1)}


def ka3(a=1.0, s=1.0):
    """The zero-crossing of delta_dis, BISECTED through A4's alpha, equals 2 gamma/(gamma+1)."""
    gammas = _linspace(1.05, 3.0, 39)
    dev, worst = [], None
    for g in gammas:
        gl = _law(g, a, s)
        root = gl.r_min_bisected()
        d = abs(root - gl.r_min_published())
        dev.append(d)
        if worst is None or d > worst[1]:
            worst = (g, d, root, gl.r_min_published())
    return max(dev), TOL["KA3"], {"n_gamma": len(gammas), "worst_gamma": worst[0],
                                  "worst_dev": worst[1], "bisected": worst[2],
                                  "published": worst[3]}


def ka4(a=1.0, s=1.0, gamma=GAMMA_AIR):
    """Leg 240's gamma=7/5 dominance window, reproduced through the module."""
    gl = _law(gamma, a, s)
    lo = gl.r_min_bisected()
    hi = gl.r_star()
    width = hi - lo
    margin = gl.delta_dis(hi)          # delta_dis is increasing in r, so the max is at r*
    d_lo = abs(lo - REF["window_lo"][0])
    d_hi = abs(hi - REF["window_hi"][0])
    d_w = abs(width - REF["window_width"][0])
    d_m = abs(margin - REF["delta_dis_margin"][0])
    # A single residual for the probe: each deviation measured in units of its own tolerance.
    res = max(d_lo / TOL["KA4_endpoint"], d_hi / TOL["KA4_endpoint"],
              d_w / TOL["KA4_width"], d_m / TOL["KA4_margin"])
    return res, 1.0, {"lo": lo, "hi": hi, "width": width, "delta_dis_at_r_star": margin,
                      "dev_lo": d_lo, "dev_hi": d_hi, "dev_width": d_w, "dev_margin": d_m,
                      "units": "residual is max deviation / its own pre-stated tolerance"}


def ka5(a=1.0, s=1.0):
    """r*'s two branches agree at gamma = 5/3, at leg 240's value."""
    gl = _law(GAMMA_MONATOMIC, a, s)
    lo_b, hi_b = gl.r_star_branch_low(), gl.r_star_branch_high()
    gap = abs(lo_b - hi_b)
    val = abs(hi_b - REF["r_star_at_5_3"][0])
    res = max(gap / TOL["KA5_branch_gap"], val / TOL["KA5_value"])
    return res, 1.0, {"branch_low": lo_b, "branch_high": hi_b, "branch_gap": gap,
                      "dev_from_banked_value": val,
                      "units": "residual is max deviation / its own pre-stated tolerance"}


def ka6(a=1.0, s=1.0):
    """r*(gamma) -> sqrt(3) as gamma -> infinity (BCG (1.7))."""
    gl = _law(1e8, a, s)
    val = gl.r_star()
    dev = abs(val - math.sqrt(3.0))
    return dev, TOL["KA6"], {"r_star_at_1e8": val, "sqrt3": math.sqrt(3.0)}


def ka7(a=1.0, s=1.0):
    """The ceiling: r*(gamma) = r_min(gamma) at gamma = 1 + 2/sqrt(3).

    r_min is taken in its alpha-routed form (2 alpha + 1)/(1 + alpha), which is identically
    2 gamma/(gamma+1) at the true alpha -- that identity is BCG's word "equivalently", and it is
    what makes this probe a test of A4's constant rather than of arithmetic on gamma.
    """
    def f(g):
        gl = _law(g, a, s)
        return gl.r_star() - gl.r_min_via_alpha()
    root = _bisect(f, GAMMA_MONATOMIC + 1e-9, 4.0)
    dev = abs(root - REF["gamma_ceiling"][0])
    return dev, TOL["KA7"], {"bisected_gamma_ceiling": root,
                             "published": REF["gamma_ceiling"][0]}


def ka8(a=1.0, s=1.0):
    """BCG lemma:k's own three properties -- THE TRANSCRIPTION GATE for R1, R2, k."""
    gl = _law(GAMMA_AIR, a, s)
    k1 = gl.k(1.0)
    d_k1 = abs(k1 - 1.0)
    r_star = gl.r_star()
    grid = _linspace(1.0, r_star - 1e-9, 200)
    ks = [gl.k(r) for r in grid]
    violations = sum(1 for i in range(1, len(ks)) if not (ks[i] > ks[i - 1]))
    blow = gl.k(r_star - 1e-6)
    ok_blow = blow >= TOL["KA8_blowup"]
    res = max(d_k1 / TOL["KA8_k1"], float(violations), 0.0 if ok_blow else 2.0)
    return res, 1.0, {"k_at_1": k1, "dev_k_at_1": d_k1, "monotonicity_violations": violations,
                      "n_points": len(grid), "k_near_r_star": blow,
                      "blowup_threshold": TOL["KA8_blowup"],
                      "k_min": min(ks), "k_max": max(ks),
                      "units": "residual is max(dev/tol, violations, 2 if no blow-up)"}


def ka9(a=1.0, s=1.0):
    """k(7/6) at gamma=7/5 against legs 265/266's independently derived 16.3479210516613."""
    gl = _law(GAMMA_AIR, a, s)
    val = gl.k(7.0 / 6.0)
    rel = abs(val - REF["k_at_7_6"][0]) / REF["k_at_7_6"][0]
    return rel, TOL["KA9"], {"k_at_7_6": val, "banked": REF["k_at_7_6"][0], "rel_dev": rel}


def ka10(a=1.0, s=1.0):
    """Odd branch indices strictly inside the target window (1, 7/6]: exactly 7, i.e. 3,5,...,15."""
    gl = _law(GAMMA_AIR, a, s)
    k76 = gl.k(7.0 / 6.0)
    odds = [j for j in range(3, int(math.floor(k76)) + 1) if j % 2 == 1]
    res = float(abs(len(odds) - REF["odd_branches_in_target_window"][0]))
    return res, 0.0, {"k_at_7_6": k76, "floor_k": int(math.floor(k76)), "odd_indices": odds,
                      "count": len(odds), "expected": REF["odd_branches_in_target_window"][0]}


def ka11(a=1.0, s=1.0):
    """The independent-group cross-form delta_dis = l(r-1) + r - 2, l = 2/(gamma-1)."""
    gammas = _linspace(1.05, 3.0, 39)
    rs = _linspace(1.0, 1.5, 19)
    dev = 0.0
    for g in gammas:
        gl = _law(g, a, s)
        ell = 2.0 / (g - 1.0)          # the other paper's notation, computed from gamma
        for r in rs:
            dev = max(dev, abs(gl.delta_dis(r) - (ell * (r - 1.0) + r - 2.0)))
    return dev, TOL["KA11"], {"grid": "%dx%d" % (len(gammas), len(rs)), "max_abs_dev": dev}


PROBES = [
    ("KA1", ka1, "alpha(7/5)=1/5, 1/alpha=5", "E"),
    ("KA2", ka2, "delta_dis collapses to 6r-7 at gamma=7/5", "E"),
    ("KA3", ka3, "bisected zero-crossing = 2 gamma/(gamma+1)", "E"),
    ("KA4", ka4, "leg 240's dominance window, width and margin", "I"),
    ("KA5", ka5, "r* branch agreement at gamma=5/3", "E+I"),
    ("KA6", ka6, "r* -> sqrt(3) as gamma -> infinity", "E"),
    ("KA7", ka7, "gamma ceiling = 1 + 2/sqrt(3)", "E+I"),
    ("KA8", ka8, "BCG lemma:k's three properties (transcription gate)", "E"),
    ("KA9", ka9, "k(7/6) = legs 265/266's 16.3479210516613", "I"),
    ("KA10", ka10, "exactly 7 odd branches in the target window", "I"),
    ("KA11", ka11, "independent-group cross-form of delta_dis", "I"),
]


def run_probes(a=1.0, s=1.0):
    out = {}
    for name, fn, desc, cls in PROBES:
        try:
            res, tol, detail = fn(a, s)
            out[name] = {"residual": res, "tolerance": tol, "passed": bool(res <= tol),
                         "description": desc, "reference_class": cls, "detail": detail}
        except Exception as exc:                                   # noqa: BLE001
            out[name] = {"residual": float("inf"), "tolerance": None, "passed": False,
                         "description": desc, "reference_class": cls,
                         "detail": {"raised": "%s: %s" % (type(exc).__name__, exc)}}
    return out


# ===========================================================================
# POST-HOC DIAGNOSTIC -- NOT pre-registered, and labelled as such wherever it is reported.
# Added after KA8 failed, to decide between the only two candidate mechanisms:
# a wrong transcription of R1/R2/k, or ill-conditioning of BCG's printed expression.
# It does not enter the gate.
# ===========================================================================

def conditioning_diagnostic():
    gl = _law(GAMMA_AIR)
    r_star = gl.r_star()

    # (i) the same three properties, in 60-digit arithmetic
    k1_hp = gl.k_high_precision(1.0)
    k76_hp = gl.k_high_precision(7.0 / 6.0)

    # (ii) how large are the terms that must cancel to zero at r = 1?
    #      (the radicand of R2 at r=1 is exactly 0 in exact arithmetic; BCG l.603 say so)
    g, r = GAMMA_AIR, 1.0
    R1 = gl.R1(r)
    terms = [g * ((76.0 - 27.0 * g) * g - 71.0),
             -(3.0 * g - 5.0) * ((g - 5.0) * g + 2.0) * r * r,
             (g * (g * (18.0 * g - 52.0) + 50.0) - 8.0) * r,
             R1 * (9.0 * (g - 2.0) * g + ((2.0 - 3.0 * g) * g + 5.0) * r + 5.0),
             18.0]
    largest = max(abs(t) for t in terms)
    radicand_double = sum(terms)

    # (iii) the loss curve: double vs 60-digit, as r moves away from the cancellation point
    curve = []
    for h in [0.0, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 1.0 / 6.0 - 1e-9]:
        rr = 1.0 + h
        if rr >= r_star:
            continue
        d, hp = gl.k(rr), gl.k_high_precision(rr)
        curve.append({"h": h, "r": rr, "k_double": d, "k_hp": hp,
                      "abs_err": abs(d - hp),
                      "rel_err": abs(d - hp) / abs(hp) if hp != 0 else float("inf")})

    return {
        "NOT_PRE_REGISTERED": ("added after KA8 failed; diagnostic only, does not enter the "
                               "gate, and KA8's pre-stated tolerance was NOT changed"),
        "k_at_1_double": gl.k(1.0),
        "k_at_1_high_precision": k1_hp,
        "dev_k_at_1_double": abs(gl.k(1.0) - 1.0),
        "dev_k_at_1_high_precision": abs(k1_hp - 1.0),
        "k_at_7_6_double": gl.k(7.0 / 6.0),
        "k_at_7_6_high_precision": k76_hp,
        "R2_radicand_at_1": {
            "terms": terms,
            "largest_abs_term": largest,
            "sum_in_double": radicand_double,
            "exact_value": 0.0,
            "predicted_double_residue": largest * 2.0 ** -52,
            "note": ("BCG l.603 state the radicand vanishes at r=1; in 60-digit arithmetic it "
                     "is exactly 0.  In IEEE double it is rounding noise, and sqrt() turns a "
                     "residue eps into an absolute error sqrt(eps) -- half the digits."),
        },
        "loss_curve": curve,
        "verdict": ("TRANSCRIPTION CORRECT, EVALUATION ILL-CONDITIONED: at 60 digits k(1)=1 and "
                    "k(7/6) reproduces legs 265/266's banked value; the double-precision defect "
                    "is localised at the cancellation point r=1 and decays as r moves away."),
    }


# ===========================================================================
# Negative controls that can fail
# ===========================================================================

def negative_controls():
    res = {}

    # NEG-1: gamma <= 1 must be rejected, not clamped.
    rejected = []
    for g in (1.0, 0.5, -2.0, 0.0):
        try:
            _law(g)
            rejected.append((g, False))
        except GammaLawError:
            rejected.append((g, True))
    res["NEG1_gamma_domain"] = {"passed": all(ok for _, ok in rejected),
                                "detail": {"rejected": rejected}}

    # NEG-2: rho <= 0 must be rejected.
    gl = _law(GAMMA_AIR)
    rho_rej = []
    for rho in (0.0, -1.0):
        for meth in ("pressure", "dpressure", "sigma"):
            try:
                getattr(gl, meth)(rho)
                rho_rej.append((meth, rho, False))
            except GammaLawError:
                rho_rej.append((meth, rho, True))
    try:
        gl.dissipative_multiplier(0.0)
        s_ok = False
    except GammaLawError:
        s_ok = True
    res["NEG2_rho_domain"] = {"passed": all(ok for _, _, ok in rho_rej) and s_ok,
                              "detail": {"rejections": rho_rej, "S_zero_rejected": s_ok}}

    # NEG-3: wrong-gamma discrimination.  The gamma=7/5 window probe run at gamma=5/3 must NOT
    # reproduce leg 240's gamma=7/5 numbers; if it did, the probe would measure the code.
    r_air, _, d_air = ka4(gamma=GAMMA_AIR)
    r_mon, _, d_mon = ka4(gamma=GAMMA_MONATOMIC)
    res["NEG3_wrong_gamma"] = {
        "passed": bool(r_air <= 1.0 and r_mon > 1.0),
        "detail": {"residual_at_7_5": r_air, "residual_at_5_3": r_mon,
                   "window_at_5_3": [d_mon["lo"], d_mon["hi"]],
                   "window_at_7_5": [d_air["lo"], d_air["hi"]],
                   "discrimination_ratio": (r_mon / r_air) if r_air > 0 else float("inf")}}

    # NEG-4: finite-difference p'(rho) against the analytic derivative.
    worst = 0.0
    for rho in _linspace(1e-2, 10.0, 400):
        h = 1e-6 * max(rho, 1e-3)
        fd = (gl.pressure(rho + h) - gl.pressure(rho - h)) / (2.0 * h)
        an = gl.dpressure(rho)
        worst = max(worst, abs(fd - an) / abs(an))
    res["NEG4_derivative"] = {"passed": bool(worst <= TOL["NEG4"]),
                              "detail": {"max_rel_err": worst, "tolerance": TOL["NEG4"]}}

    # NEG-5: the vacuum pole order diverges as gamma -> 1+, one decade per decade.
    ks = list(range(2, 9))
    xs = [float(kk) for kk in ks]
    ys = [math.log10(_law(1.0 + 10.0 ** (-kk)).vacuum_pole_order) for kk in ks]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    res["NEG5_vacuum_pole"] = {"passed": bool(abs(slope - 1.0) <= TOL["NEG5"]),
                               "detail": {"loglog_slope": slope, "expected": 1.0,
                                          "one_over_alpha_at_gamma_1p01": _law(1.01).one_over_alpha}}
    return res


# ===========================================================================
# The plants: per-probe detection thresholds
# ===========================================================================

def _probe_passes(name, a, s):
    fn = dict((p[0], p[1]) for p in PROBES)[name]
    try:
        res, tol, _ = fn(a, s)
    except Exception:                                              # noqa: BLE001
        return False                                               # a raise is a detection
    return bool(res <= tol)


def detection_threshold(name, plant, lo_exp=-16.0, hi_exp=0.0, iters=60):
    """Smallest plant magnitude at which the probe crosses its own tolerance.

    Returns None if the probe still passes at the largest magnitude swept (a BLIND cell), and
    0.0 if it already fails at the smallest.
    """
    def passes(eps):
        a, s = (1.0 + eps, 1.0) if plant == "alpha" else (1.0, 1.0 + eps)
        return _probe_passes(name, a, s)

    if passes(10.0 ** hi_exp):
        return None                                                # blind across the whole sweep
    if not passes(10.0 ** lo_exp):
        return 0.0                                                 # detects at machine level
    lo, hi = lo_exp, hi_exp
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if passes(10.0 ** mid):
            lo = mid
        else:
            hi = mid
    return 10.0 ** hi


def plant_sweep():
    out = {}
    for plant in ("alpha", "sqrt3"):
        cells = {}
        for name, _fn, _d, _c in PROBES:
            thr = detection_threshold(name, plant)
            cells[name] = {"detection_threshold": thr,
                           "blind": thr is None,
                           "fails_at_required_magnitude": None}
        out[plant] = cells

    # The pre-stated requirements, evaluated explicitly rather than inferred from the threshold.
    for name in [p[0] for p in PROBES]:
        a_res = run_probes(1.0 + PLANT_ALPHA_MUST_FAIL_AT, 1.0)[name]["passed"]
        out["alpha"][name]["fails_at_required_magnitude"] = (not a_res)
        s_res = run_probes(1.0, 1.0 + PLANT_FORMULA_MUST_FAIL_AT)[name]["passed"]
        out["sqrt3"][name]["fails_at_required_magnitude"] = (not s_res)
    return out


# ===========================================================================
# Self-tests: does the battery itself work?
# ===========================================================================

def self_tests():
    t = []

    def chk(name, ok, detail=""):
        t.append({"name": name, "passed": bool(ok), "detail": str(detail)})

    gl = _law(GAMMA_AIR)
    chk("module is frozen (constants cannot be mutated after construction)",
        _frozen_check(gl))
    chk("pressure is strictly increasing on (0, 10]",
        all(gl.pressure(x) < gl.pressure(x + 1e-3) for x in _linspace(1e-3, 9.9, 200)))
    chk("p(1) = 1/gamma", abs(gl.pressure(1.0) - 1.0 / GAMMA_AIR) < 1e-15)
    chk("c(rho)^2 = gamma p(rho)/rho (thermodynamic consistency)",
        max(abs(gl.sound_speed(x) ** 2 - GAMMA_AIR * gl.pressure(x) / x)
            for x in _linspace(0.1, 5.0, 100)) < 1e-13)
    chk("sigma(1) = 1/alpha", abs(gl.sigma(1.0) - gl.one_over_alpha) < 1e-15)
    chk("r_min_via_alpha == r_min_published at the true alpha",
        max(abs(_law(g).r_min_via_alpha() - _law(g).r_min_published())
            for g in _linspace(1.05, 3.0, 40)) < 1e-15)
    chk("the plants are inert at scale 1.0 (default configuration is unplanted)",
        _law(GAMMA_AIR, 1.0, 1.0).summary() == _law(GAMMA_AIR).summary())
    chk("PLANT-alpha actually moves alpha",
        abs(_law(GAMMA_AIR, 1.1).alpha - _law(GAMMA_AIR).alpha) > 1e-3)
    chk("PLANT-sqrt3 actually moves r* on the high branch, and NOT on the low branch",
        abs(_law(2.0, 1.0, 1.1).r_star() - _law(2.0).r_star()) > 1e-3
        and abs(_law(1.4, 1.0, 1.1).r_star() - _law(1.4).r_star()) == 0.0)
    chk("a probe with a deliberately corrupted reference FAILS (the battery can say no)",
        _corrupted_reference_fails())
    chk("re-running the battery is bit-identical (determinism)",
        json.dumps(run_probes(), sort_keys=True) == json.dumps(run_probes(), sort_keys=True))
    chk("the 60-digit path agrees with double AWAY from the cancellation point",
        abs(gl.k(7.0 / 6.0) - gl.k_high_precision(7.0 / 6.0)) < 1e-11)
    chk("the 60-digit path and double DISAGREE at the cancellation point r=1 "
        "(so the diagnostic is measuring something real)",
        abs(gl.k(1.0) - gl.k_high_precision(1.0)) > 1e-9)
    chk("delta_dis is strictly increasing in r (so its max on the window is at r*)",
        all(gl.delta_dis(r) < gl.delta_dis(r + 1e-4) for r in _linspace(1.0, 1.3, 100)))
    return t


def _frozen_check(gl):
    try:
        gl.gamma = 2.0                                             # type: ignore[misc]
        return False
    except Exception:                                              # noqa: BLE001
        return True


def _corrupted_reference_fails():
    """Temporarily corrupt a reference and confirm the probe reports the failure."""
    saved = REF["k_at_7_6"]
    REF["k_at_7_6"] = (saved[0] * 1.001, saved[1], saved[2] + " [CORRUPTED FOR SELF-TEST]")
    try:
        res, tol, _ = ka9()
        return res > tol
    finally:
        REF["k_at_7_6"] = saved


# ===========================================================================
# Figure
# ===========================================================================

def build_figure(path, results):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    gl = _law(GAMMA_AIR)
    fig, axes = plt.subplots(1, 3, figsize=(16.6, 4.8))

    # (a) delta_dis(r) at gamma = 7/5, with the two windows.
    ax = axes[0]
    rs = _linspace(1.0, 1.22, 400)
    ax.plot(rs, [gl.delta_dis(r) for r in rs], lw=2.0, color="#1f4e79",
            label=r"$\delta_{\rm dis}(r)=6r-7$  ($\gamma=7/5$)")
    ax.axhline(0.0, color="0.4", lw=0.8)
    lo, hi = gl.r_min_bisected(), gl.r_star()
    ax.axvspan(lo, hi, color="#2e7d32", alpha=0.16,
               label="dominance window (%.7f, %.7f)" % (lo, hi))
    ax.axvspan(1.070374, 1.094975, color="#c62828", alpha=0.20,
               label=r"leg 275 target $r^{(3)}$ (viscous-inadmissible)")
    ax.axvline(lo, color="#2e7d32", lw=1.2)
    ax.axvline(hi, color="#2e7d32", lw=1.2)
    ax.set_xlabel(r"self-similar scaling exponent $r$")
    ax.set_ylabel(r"$\delta_{\rm dis}$")
    ax.set_title(r"(a) A4's $\alpha$ decides where the viscous term is an error")
    ax.legend(fontsize=7.5, loc="upper left")
    ax.grid(alpha=0.25)

    # (b) the probe x plant detection-threshold matrix.
    ax = axes[1]
    names = [p[0] for p in PROBES]
    floor_exp = -17.0
    for j, (plant, colour, marker, label) in enumerate([
            ("alpha", "#1f4e79", "o", r"PLANT-$\alpha$:  $\alpha\to\alpha(1+\epsilon)$"),
            ("sqrt3", "#b8860b", "s",
             r"PLANT-FORMULA:  $\sqrt{3}\to\sqrt{3}(1+\delta)$")]):
        xs, ys, blind_x = [], [], []
        for i, nm in enumerate(names):
            thr = results["plants"][plant][nm]["detection_threshold"]
            if thr is None:
                blind_x.append(i)
            else:
                xs.append(i)
                ys.append(math.log10(thr) if thr > 0 else floor_exp)
        ax.plot(xs, ys, marker, color=colour, ms=7, label=label, ls="none")
        ax.plot(blind_x, [0.6] * len(blind_x), "x", color=colour, ms=9, mew=2,
                label=None if j else None)
    ax.axhline(0.0, color="0.4", lw=0.8, ls=":")
    ax.text(0.02, 0.62, "x  = BLIND across the whole sweep", transform=ax.transAxes,
            fontsize=7.5, color="0.25")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, fontsize=8)
    ax.set_ylabel(r"$\log_{10}$ detection threshold $\epsilon^\ast$")
    ax.set_title("(b) what each probe can notice: smaller = sharper")
    ax.legend(fontsize=7.5, loc="lower right")
    ax.grid(alpha=0.25)

    # (c) the conditioning curve: what the float dress rehearsal actually found.
    ax = axes[2]
    curve = [c for c in results["post_hoc_conditioning_diagnostic"]["loss_curve"]]
    hs = [max(c["h"], 1e-16) for c in curve]
    errs = [max(c["abs_err"], 1e-18) for c in curve]
    ax.loglog(hs, errs, "o-", color="#8e24aa", lw=1.8, ms=6,
              label=r"$|k_{\rm double}(1+h)-k_{60\,\rm digit}(1+h)|$")
    ax.axhline(1e-9, color="#c62828", ls="--", lw=1.2,
               label=r"KA8's pre-stated tolerance $10^{-9}$")
    ax.set_xlabel(r"distance $h$ from the cancellation point $r=1$")
    ax.set_ylabel("absolute error of the double evaluation")
    ax.set_title("(c) BCG's $R_2$ radicand cancels to 0 at $r=1$:\n"
                 "the square root costs half the digits")
    ax.legend(fontsize=7.5, loc="upper right")
    ax.grid(alpha=0.25, which="both")

    fig.suptitle("Leg 302 / Route-P2T1: apparatus term A4 (gamma-law pressure), "
                 "float dress rehearsal", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ===========================================================================
# Main
# ===========================================================================

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--figure", default=None, help="write the registered figure to this path")
    ap.add_argument("--no-write", action="store_true", help="do not write the curated JSON")
    args = ap.parse_args(argv)

    print("Route-P2T1 v1 (leg 302) -- apparatus term A4, gamma-law pressure")
    print("=" * 78)

    unplanted = run_probes()
    print("\nKNOWN-ANSWER PROBES (unplanted).  tolerances fixed in the journal beforehand.")
    for name, _fn, desc, cls in PROBES:
        p = unplanted[name]
        print("  %-5s %-4s %-48s residual %-12.4g tol %-9.4g %s"
              % (name, cls, desc[:48], p["residual"], p["tolerance"] if p["tolerance"]
                 is not None else float("nan"), "ok" if p["passed"] else "FAIL"))

    negs = negative_controls()
    print("\nNEGATIVE CONTROLS (each can fail):")
    for name, v in negs.items():
        print("  %-22s %s" % (name, "ok" if v["passed"] else "FAIL"))

    print("\nPLANT SWEEP (detection thresholds; this is the gate's second half) ...")
    plants = plant_sweep()
    print("  %-6s %-24s %-24s" % ("probe", "PLANT-alpha eps*", "PLANT-FORMULA delta*"))
    for name, _fn, _d, _c in PROBES:
        a = plants["alpha"][name]["detection_threshold"]
        s = plants["sqrt3"][name]["detection_threshold"]
        print("  %-6s %-24s %-24s"
              % (name,
                 "BLIND" if a is None else "%.3g" % a,
                 "BLIND" if s is None else "%.3g" % s))

    diag = conditioning_diagnostic()
    print("\nPOST-HOC DIAGNOSTIC (not pre-registered, does not enter the gate):")
    print("  |k(1)-1|  double %.4g   vs   60-digit %.4g"
          % (diag["dev_k_at_1_double"], diag["dev_k_at_1_high_precision"]))
    print("  R2 radicand at r=1: largest term %.4f, exact sum 0, double sum %.4g"
          % (diag["R2_radicand_at_1"]["largest_abs_term"],
             diag["R2_radicand_at_1"]["sum_in_double"]))
    print("  k(7/6) double %.13f   60-digit %.13f"
          % (diag["k_at_7_6_double"], diag["k_at_7_6_high_precision"]))

    tests = self_tests()
    print("\nSELF-TESTS: %d/%d passed" % (sum(1 for t in tests if t["passed"]), len(tests)))
    for t in tests:
        if not t["passed"]:
            print("  FAIL: %s %s" % (t["name"], t["detail"]))

    # ---- the gate, DERIVED (never hardcoded) -------------------------------
    all_probes_pass = all(unplanted[n]["passed"] for n in unplanted)
    all_negs_pass = all(v["passed"] for v in negs.values())
    all_tests_pass = all(t["passed"] for t in tests)
    alpha_required_fail = {n: plants["alpha"][n]["fails_at_required_magnitude"]
                           for n in PLANT_ALPHA_REQUIRED}
    formula_required_fail = {n: plants["sqrt3"][n]["fails_at_required_magnitude"]
                             for n in PLANT_FORMULA_REQUIRED}
    half_one = all_probes_pass and all_negs_pass and all_tests_pass
    half_two = all(alpha_required_fail.values()) and all(formula_required_fail.values())
    gate = "YES" if (half_one and half_two) else "NO"

    results = {
        "leg": 302,
        "route": "P2T1",
        "what_this_is": ("a float dress rehearsal of ONE term (A4, adiabatic/gamma-law pressure) "
                         "from leg 285's fifteen-term apparatus spec, with eleven known-answer "
                         "probes at pre-stated tolerances, five negative controls, and two "
                         "plants swept for per-probe detection thresholds"),
        "term": {"id": "A4", "name": "adiabatic / gamma-law pressure",
                 "module": ("inlined in experiments/p2_route_p2t1_v1.py; deliberately NOT banked "
                            "as solver/p2_apparatus_term1.py, because banking a module is the "
                            "gate's YES-branch action and this gate came out NO (journal "
                            "leg_302.md Part 4 and Part 8)"),
                 "spec_source": "leg 285, writeup/data/p2_route_p2s_v1_spec.json",
                 "why_this_term": ("cheapest LOAD-BEARING term: A15a is 285's cheapest overall "
                                   "but its substrate solver/interval.py already exists and it "
                                   "sits off the critical path; A4 is the head of 285's "
                                   "critical path A4->A1->A2->A9->A8->A13->A14 (depth 7) and "
                                   "the only in-degree-0 term on it"),
                 "not_built": ["A1", "A2", "A3", "A5", "A6", "A7", "A8", "A9", "A10", "A11",
                               "A12", "A13", "A14", "A15a", "A15b"]},
        "clay_odds": "~0.05%, unchanged; building an apparatus term moves no L1->L4 link",
        "arithmetic": "IEEE double (float dress rehearsal); solver/interval.py deliberately unused",
        "references": {k: {"value": v[0], "class": v[1], "provenance": v[2]}
                       for k, v in REF.items()},
        "pre_stated_tolerances": TOL,
        "pre_stated_plant_requirements": {
            "plant_alpha": {"magnitude": PLANT_ALPHA_MUST_FAIL_AT,
                            "must_fail": PLANT_ALPHA_REQUIRED},
            "plant_formula": {"magnitude": PLANT_FORMULA_MUST_FAIL_AT,
                              "must_fail": PLANT_FORMULA_REQUIRED,
                              "expected_blind": PLANT_FORMULA_EXPECTED_BLIND}},
        "probes": unplanted,
        "post_hoc_conditioning_diagnostic": diag,
        "negative_controls": negs,
        "plants": plants,
        "self_tests": {"total": len(tests), "passed": sum(1 for t in tests if t["passed"]),
                       "tests": tests},
        "gate": {
            "question": ("Does the implemented term reproduce its pre-stated known-answer / "
                         "planted control within a pre-stated tolerance AND report the failure "
                         "when the plant is perturbed?"),
            "half_one_known_answers": half_one,
            "half_two_plants_detected": half_two,
            "alpha_required_failures": alpha_required_fail,
            "formula_required_failures": formula_required_fail,
            "answer": gate,
            "derivation": ("gate = YES iff (all 11 probes pass at their pre-stated tolerances "
                           "AND all 5 negative controls pass AND all self-tests pass) AND (every "
                           "probe named in the pre-stated must-fail lists actually fails at the "
                           "pre-stated plant magnitude).  Computed, not asserted."),
        },
    }

    # The figure's registered home (writeup/figures/ + writeup/build_figures.py) is outside this
    # leg's declared file territory, so the runner records the intended path and the one command
    # that emits it; placement is an orchestrator integration note (journal leg_302 §5).
    results["figure"] = {
        "registered_path": "writeup/figures/fig69_route_p2t1_v1_sensitivity.png",
        "index_caveat": ("fig69 was the next free index at this leg's rebase (fig68 was taken by "
                         "leg 303 mid-run); the orchestrator should use whatever index is free at "
                         "integration time -- the number is not load-bearing."),
        "command": (".venv/bin/python experiments/p2_route_p2t1_v1.py "
                    "--figure writeup/figures/fig69_route_p2t1_v1_sensitivity.png"),
        "panels": ["(a) delta_dis(r) with the gamma=7/5 dominance window",
                   "(b) probe x plant detection-threshold matrix, BLIND cells marked",
                   "(c) double vs 60-digit k(1+h): the KA8 conditioning defect"],
        "emitted_this_run_to": None,
    }
    if args.figure:
        p = build_figure(args.figure, results)
        results["figure"]["emitted_this_run_to"] = os.path.relpath(p, ROOT) \
            if p.startswith(ROOT) else p
        print("\nfigure: %s" % p)

    if not args.no_write:
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        with open(DATA, "w") as fh:
            json.dump(results, fh, indent=1, sort_keys=False)
            fh.write("\n")
        print("wrote %s" % os.path.relpath(DATA, ROOT))

    print("\nGATE: %s   (known answers %s, plants detected %s)"
          % (gate, "PASS" if half_one else "FAIL", "PASS" if half_two else "FAIL"))
    return 0 if gate == "YES" else 1


if __name__ == "__main__":
    sys.exit(main())
