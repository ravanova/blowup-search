"""Term A4 of leg 285's fifteen-term apparatus spec: the adiabatic / gamma-law pressure.

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

from __future__ import annotations

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
