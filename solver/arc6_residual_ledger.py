"""Exact-rational scaling ledger for a concentrating axisymmetric blowup residual.

Arc 6, unit `U3` (leg 419). Novelty pass: `writeup/novelty/leg_419.md`, committed
first.

WHAT THIS IS
------------
Every length, speed, rate and residual term of a concentrating axisymmetric
ansatz scales as a power of the concentration variable, and every one of those
powers is `a + b*h` for rationals `a, b` and the single free profile exponent
`h`. This module carries those powers as `Fraction` pairs and does the algebra
EXACTLY. A balance either holds or it does not; there is no tolerance, and
therefore none to widen after seeing a number — the failure mode this repository
recorded against itself at leg 408 and refused.

It re-derives, rather than transcribes, the ledger of OpenAI's *Finite Time
Blowup for Navier-Stokes* (`Papers/openai-navier-stokes.pdf`, sha256
0e779481c4da40bd..., 166 pp, pinned at leg 417). Each balance is recomputed from
the geometry and the profile exponents and then CHECKED against the value the
manuscript prints, so a transcription error surfaces as a failing check rather
than as agreement.

It also carries a CONTRAST COLUMN: the same ledger for this repository's own
route-4 DSS object, whose far-field exponent is pinned at `alpha = 1` (`L2'`,
leg 397; `WALLS.md` W4). That column is where W4 lives, and it is the thing U5
must port onto.

WHAT THIS IS NOT
----------------
* Not a proof of anything, and not Tier 2. It is exponent bookkeeping. A
  consistent ledger is a NECESSARY condition on a construction and nowhere near
  a sufficient one: every term could scale correctly and the construction still
  fail, because the ledger cannot see whether the objects it counts exist.
* Not a numerical solution of anything. Nothing here is integrated, and that is
  deliberate: `CORRECTIONS.md` §52-§54 record two integrals in this repository
  that looked convergent on a truncation and were not. Convergence questions
  here are answered as INEQUALITIES ON RATIONAL EXPONENTS.
* Not a claim about the manuscript's correctness. The ledger checks internal
  consistency of the SCALINGS. That is the cheapest thing that could have been
  wrong, so it is worth checking, and it is not the thing that matters most.

CONVENTIONS
-----------
`tau = 1 - t` is time remaining. `q` is the manuscript's concentration variable,
with `q ~ tau + |z|^(1/D)`; on the core `q ~ tau`, so a `q`-exponent and a
`tau`-exponent agree there and this module works in one variable throughout.
Exponents are stored so that `Scale(a, b)` means `q**(a + b*h)`.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

__all__ = [
    "Scale",
    "GeometryLedger",
    "PulseLedger",
    "EnergyLedger",
    "CorrectionCycle",
    "manuscript_ledger",
    "route4_contrast",
    "MANUSCRIPT_PRINTED",
]


@dataclass(frozen=True)
class Scale:
    """The exponent of `q` in `q**(a + b*h)`, exactly.

    Multiplying two scales adds exponents; that is all the algebra needed, so
    `+` on `Scale` means multiplication of the quantities it labels. The name
    kept is `Scale` and not `Exponent` because every use site reads as a
    physical quantity.
    """

    a: F
    b: F

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    def __add__(self, other: "Scale") -> "Scale":
        return Scale(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "Scale") -> "Scale":
        return Scale(self.a - other.a, self.b - other.b)

    def __mul__(self, k) -> "Scale":
        k = F(k)
        return Scale(self.a * k, self.b * k)

    __rmul__ = __mul__

    def __neg__(self) -> "Scale":
        return Scale(-self.a, -self.b)

    def at(self, h) -> F:
        """The exponent as a number, at a given `h`. Exact for rational `h`."""
        return self.a + self.b * F(h)

    def blows_up_at(self, h) -> bool:
        """Does `q**exponent` diverge as `q -> 0`? Exactly `exponent < 0`."""
        return self.at(h) < 0

    def integrable_in_tau_at(self, h) -> bool:
        """Is `int_0^{tau0} tau**exponent dtau` finite? Exactly `exponent > -1`.

        Answered as an inequality on a rational, never by quadrature -- see the
        module docstring on `CORRECTIONS.md` §52-§54.
        """
        return self.at(h) > F(-1)

    def __str__(self) -> str:
        if self.b == 0:
            return f"q^({self.a})"
        sign = "+" if self.b > 0 else "-"
        mag = abs(self.b)
        coef = "h" if mag == 1 else f"{mag}h"
        return f"q^({self.a} {sign} {coef})"


# --------------------------------------------------------------------------
# The manuscript's printed values, transcribed ONCE, in one place, so that
# every check below compares a RE-DERIVED value against a transcription that a
# reader can audit against the PDF in a single glance. Nothing downstream reads
# the PDF; everything downstream re-derives and compares to this table.
# Locations are the manuscript's own, at the pinned sha256.
# --------------------------------------------------------------------------
MANUSCRIPT_PRINTED = {
    "A": (F(1, 2), F(1)),              # A = 1/2 + h                    §3.1
    "D": (F(1, 2), F(-1)),             # D = 1/2 - h                    §3.1
    "ell_r": (F(1, 2), F(0)),          # ell_r ~ tau^(1/2)              §2.1, §3.1
    "ell_z": (F(1, 2), F(-1)),         # ell_z ~ tau^(1/2 - h)          §2.1
    "aspect_r_over_z": (F(0), F(1)),   # ell_r/ell_z ~ tau^h            §2.1
    "core_volume": (F(3, 2), F(-1)),   # volume ~ tau^(3/2 - h)         §2.1, §3.5
    "u_theta": (F(-1, 2), F(-1)),      # |u_theta| ~ tau^(-1/2 - h)     §2.1, §3.1
    "u_z": (F(-1, 2), F(-1)),          # |u_z|     ~ tau^(-1/2 - h)     §2.1, §3.1
    "u_r": (F(-1, 2), F(0)),           # |u_r|   = O(tau^(-1/2))        §2.1, §3.1
    "u_r_over_u_theta": (F(0), F(1)),  # ratio = O(tau^h)               §3.1
    "Re_theta": (F(0), F(-1)),         # Re_theta ~ tau^(-h) -> oo      §2.1, §3.1
    "Re_r": (F(0), F(0)),              # Re_r = O(1)                    §2.1, §3.1
    "radial_transport_rate": (F(-1), F(0)),   # |u_r|/ell_r = O(q^-1)   §3.1
    "axial_transport_rate": (F(-1), F(0)),    # q^-A/ell_z  = q^-1      §3.1
    "radial_diffusion_rate": (F(-1), F(0)),   # 1/ell_r^2   = q^-1      §3.1
    "axial_over_radial_diffusion": (F(0), F(2)),  # ell_r^2/ell_z^2 = q^(2h)  §3.1
    "A_wave": (F(-1, 2), F(-1, 2)),    # A_wave ~ q^(-1/2 - h/2)        §3.3
    "ell_wave": (F(1, 2), F(1, 2)),    # ell_wave ~ q^(1/2 + h/2)       §3.3
    "wave_ratio": (F(0), F(1, 2)),     # A_wave/q^-A = ell_wave/ell_r = q^(h/2)  §3.3
    "A_wave_squared": (F(-1), F(-1)),  # A_wave^2 ~ q^(-1 - h)          §3.3
    "stress_divergence": (F(-3, 2), F(-1)),   # A_wave^2/q^(1/2) = q^(-3/2 - h)  §3.3
    "E_core": (F(1, 2), F(-3)),        # E_core ~ tau^(1/2 - 3h)        §3.5
    "D_core": (F(-1, 2), F(-3)),       # D_core ~ tau^(-1/2 - 3h)       §3.5
}


def _printed(name: str) -> Scale:
    a, b = MANUSCRIPT_PRINTED[name]
    return Scale(a, b)


@dataclass(frozen=True)
class GeometryLedger:
    """Lengths, speeds and rates, all re-derived from `A`, `D` and the profile.

    The two inputs are the manuscript's own definitions `A = 1/2 + h`,
    `D = 1/2 - h` (§3.1). Everything else here is computed.
    """

    A: Scale = Scale(F(1, 2), F(1))
    D: Scale = Scale(F(1, 2), F(-1))

    # -- lengths -----------------------------------------------------------
    @property
    def ell_r(self) -> Scale:
        """Radial core scale. `ell_r = q^(1/2)` -- the parabolic scale, from
        `X = r^2/(2q)` bounded (§3.1, eq. (3.2))."""
        return Scale(F(1, 2), F(0))

    @property
    def ell_z(self) -> Scale:
        """Axial core scale, `q^D`, from `z = q^D * eta` with `|eta| <= eta_c`."""
        return self.D

    @property
    def aspect_r_over_z(self) -> Scale:
        return self.ell_r - self.ell_z

    @property
    def core_volume(self) -> Scale:
        """`ell_r^2 * ell_z` -- a cylinder of radius `ell_r`, height `ell_z`."""
        return 2 * self.ell_r + self.ell_z

    # -- speeds ------------------------------------------------------------
    @property
    def u_theta(self) -> Scale:
        """`u_theta = q^-A * E`, so the scale is `q^-A` (§3.1)."""
        return -self.A

    @property
    def u_z(self) -> Scale:
        """`u_z = q^-A * U`, same scale."""
        return -self.A

    @property
    def u_r(self) -> Scale:
        """`r*u_r = V_0`, `V_0/X` smooth, so `u_r ~ r/q ~ q^(1/2)/q = q^(-1/2)`.

        RE-DERIVED, not read off: it follows from `V_0 = O(X)` near the axis and
        `r = sqrt(2 q X)`. The manuscript prints `O(tau^(-1/2))`.
        """
        return self.ell_r - Scale(F(1), F(0))

    @property
    def u_r_over_u_theta(self) -> Scale:
        return self.u_r - self.u_theta

    # -- Reynolds numbers, at viscosity one --------------------------------
    @property
    def Re_theta(self) -> Scale:
        return self.u_theta + self.ell_r

    @property
    def Re_r(self) -> Scale:
        return self.u_r + self.ell_r

    # -- the three rates that must coincide --------------------------------
    @property
    def radial_transport_rate(self) -> Scale:
        return self.u_r - self.ell_r

    @property
    def axial_transport_rate(self) -> Scale:
        return self.u_theta - self.ell_z

    @property
    def radial_diffusion_rate(self) -> Scale:
        return -2 * self.ell_r

    @property
    def axial_diffusion_rate(self) -> Scale:
        return -2 * self.ell_z

    @property
    def axial_over_radial_diffusion(self) -> Scale:
        """The background expansion parameter. `q^(2h)` (§3.1)."""
        return self.axial_diffusion_rate - self.radial_diffusion_rate

    @property
    def leading_tangential_residual(self) -> Scale:
        """The scale the tangential momentum residual actually carries.

        `speed x rate`, where the rate is the common value of the three above.
        This is THE NUMBER the pulses have to cancel, and it is derived here,
        not asserted.
        """
        return self.u_theta + self.radial_diffusion_rate

    def leading_balance_holds(self) -> bool:
        """The three leading rates coincide exactly. Independent of `h`."""
        return (self.radial_transport_rate == self.axial_transport_rate
                == self.radial_diffusion_rate)


@dataclass(frozen=True)
class PulseLedger:
    """The oscillatory pulses and the stress they are required to supply."""

    geom: GeometryLedger = GeometryLedger()

    @property
    def A_wave(self) -> Scale:
        """Pulse amplitude, from the requirement that its Reynolds stress
        divergence match `leading_tangential_residual`.

        SOLVED, not transcribed. Requiring
            2*A_wave - ell_r == geom.leading_tangential_residual
        gives `A_wave = (u_theta - ell_r)/2`, which is `q^(-1/2 - h/2)`.
        """
        return (self.geom.u_theta + self.geom.radial_diffusion_rate
                + self.geom.ell_r) * F(1, 2)

    @property
    def ell_wave(self) -> Scale:
        """Pulse wavelength. The manuscript's own relation is that the pulse is
        smaller than the core by the SAME factor that its amplitude exceeds the
        background speed: `A_wave/q^-A = ell_wave/ell_r`."""
        return self.geom.ell_r + (self.A_wave - self.geom.u_theta)

    @property
    def wave_ratio(self) -> Scale:
        return self.A_wave - self.geom.u_theta

    @property
    def A_wave_squared(self) -> Scale:
        return 2 * self.A_wave

    @property
    def stress_divergence(self) -> Scale:
        """`div(w (x) w)` in the radial direction: `A_wave^2 / ell_r`."""
        return self.A_wave_squared - self.geom.ell_r

    def stress_cancels_residual(self) -> bool:
        """The whole point of the pulses, as an exact identity in `h`."""
        return self.stress_divergence == self.geom.leading_tangential_residual

    def ratios_agree(self) -> bool:
        """`A_wave/q^-A == ell_wave/ell_r`, the manuscript's own consistency."""
        return (self.A_wave - self.geom.u_theta) == (self.ell_wave - self.geom.ell_r)


@dataclass(frozen=True)
class EnergyLedger:
    """Kinetic energy and dissipation of the core, and the `h` conditions.

    These are the two conditions that make the object admissible for Clay
    condition (7). They are the ONLY place in this ledger where `h` is
    constrained by anything other than the profile construction.
    """

    geom: GeometryLedger = GeometryLedger()

    @property
    def E_core(self) -> Scale:
        """`volume x speed^2`."""
        return self.geom.core_volume + 2 * self.geom.u_theta

    @property
    def D_core(self) -> Scale:
        """`volume x (speed/ell_r)^2` -- squared radial derivative."""
        return self.geom.core_volume + 2 * (self.geom.u_theta - self.geom.ell_r)

    def energy_vanishes_at(self, h) -> bool:
        """`E_core -> 0` as `tau -> 0` iff its exponent is positive."""
        return self.E_core.at(h) > 0

    def dissipation_integrable_at(self, h) -> bool:
        """`int_0^{tau0} D_core dtau < oo`. An inequality, not a quadrature."""
        return self.D_core.integrable_in_tau_at(h)

    def admissible_at(self, h) -> bool:
        return self.energy_vanishes_at(h) and self.dissipation_integrable_at(h)

    def critical_h(self) -> F:
        """The exact `h` at which the energy condition fails.

        Solves `E_core.a + E_core.b * h = 0`. Both conditions turn out to have
        the SAME threshold; `test_arc6_residual_ledger.py` checks that rather
        than this docstring asserting it.
        """
        return -self.E_core.a / self.E_core.b


@dataclass(frozen=True)
class CorrectionCycle:
    """The residual-decay exponent recursion, `sigma_{j+1} = sigma_j + step`.

    `sigma_j` is the manuscript's measure of how fast the remaining residual
    vanishes as `q -> 0` (§3.4). Flatness -- every Cartesian space-time
    derivative `O(q^N)` for every `N` -- is the statement that `sigma_j -> oo`.
    That, and nothing about the pulses, is what makes the residual extendable to
    a SMOOTH force through the singular time.
    """

    sigma_0: F = F(1, 5)
    step: F = F(1, 10)

    def sigma(self, j: int) -> F:
        if j < 0:
            raise ValueError("stage index must be >= 0")
        return self.sigma_0 + self.step * j

    def stages_to_reach(self, target) -> int:
        """Smallest `j` with `sigma(j) >= target`. Exact ceiling division."""
        target = F(target)
        if target <= self.sigma_0:
            return 0
        need = target - self.sigma_0
        j = need / self.step
        return int(j) if j.denominator == 1 else int(j) + 1

    def diverges(self) -> bool:
        return self.step > 0


def manuscript_ledger(h=F(1, 100)):
    """The full re-derived ledger, with every value checked against
    `MANUSCRIPT_PRINTED`.

    Returns a dict of `{name: (derived_scale, printed_scale, agree)}`. The
    caller decides what to do about disagreement; this function never raises,
    so a disagreement is DATA rather than a crash.
    """
    g = GeometryLedger()
    p = PulseLedger(g)
    e = EnergyLedger(g)
    derived = {
        "A": g.A, "D": g.D,
        "ell_r": g.ell_r, "ell_z": g.ell_z,
        "aspect_r_over_z": g.aspect_r_over_z,
        "core_volume": g.core_volume,
        "u_theta": g.u_theta, "u_z": g.u_z, "u_r": g.u_r,
        "u_r_over_u_theta": g.u_r_over_u_theta,
        "Re_theta": g.Re_theta, "Re_r": g.Re_r,
        "radial_transport_rate": g.radial_transport_rate,
        "axial_transport_rate": g.axial_transport_rate,
        "radial_diffusion_rate": g.radial_diffusion_rate,
        "axial_over_radial_diffusion": g.axial_over_radial_diffusion,
        "A_wave": p.A_wave, "ell_wave": p.ell_wave,
        "wave_ratio": p.wave_ratio,
        "A_wave_squared": p.A_wave_squared,
        "stress_divergence": p.stress_divergence,
        "E_core": e.E_core, "D_core": e.D_core,
    }
    return {k: (v, _printed(k), v == _printed(k)) for k, v in derived.items()}


def route4_contrast():
    """The same question, asked of THIS repository's own route-4 object.

    Route 4's banked object is a backward-DSS profile on `R^3` whose far-field
    exponent is PINNED at `alpha = 1` -- `|U(y)| ~ C/|y|` (`solver/
    dssp_biot_savart.py`'s closed-form witness; `L2'`, leg 397, measured the pin
    from BOTH sides: `>= 1` by Chae-Wolf Thm 1.1, `<= 1` by Rmk 1.2 + ESS).
    `WALLS.md` W4 is the statement that such a profile has infinite global
    energy while Clay condition (7) demands bounded energy.

    This function makes the contrast a computation instead of a sentence. It
    returns, exactly:

      * the exponent of the energy density integrand in `|y|`, at `alpha`;
      * whether `int |U|^2 dy` over `R^3` converges (an inequality on a
        rational, never a quadrature -- `CORRECTIONS.md` §52-§54);
      * the same for `int |U|^3`, which `PB2` (leg 410) measured to be
        log-divergent at `alpha = 1`, so agreement here is a check on the
        ledger and not a new result;
      * the exponent `alpha` would have to reach for each integral to converge.

    NOTHING here is new mathematics. It is the repository's own pinned number,
    put in the same units as the manuscript's ledger so U5 can compare them.
    """
    alpha = F(1)  # PINNED. L2' (leg 397), verified V-W4. Not a fitted value.
    out = {"alpha_pinned": alpha}
    for power, key in ((2, "L2"), (3, "L3")):
        # int_{|y|>1} |U|^p dy ~ int r^{-p*alpha} r^2 dr : converges iff
        # -p*alpha + 2 < -1, i.e. p*alpha > 3.
        out[f"{key}_integrand_exponent"] = -power * alpha + 2
        out[f"{key}_converges"] = (power * alpha > 3)
        out[f"{key}_alpha_needed"] = F(3, power)
        out[f"{key}_deficit"] = F(3, power) - alpha
    # leg 381's cutoff bill, in the same units.
    out["cutoff_bill_alpha_needed"] = F(3, 2)
    out["cutoff_bill_deficit"] = F(3, 2) - alpha
    return out


def _fmt(x) -> str:
    return str(x) if isinstance(x, str) else f"{x}"


def main() -> int:
    print("ARC 6 / U3 — exact scaling ledger")
    print("=" * 78)
    led = manuscript_ledger()
    bad = [k for k, (_, _, ok) in led.items() if not ok]
    print(f"{'quantity':<30} {'re-derived':<22} {'manuscript prints':<22} ok")
    for k, (d, pr, ok) in led.items():
        print(f"{k:<30} {str(d):<22} {str(pr):<22} {'yes' if ok else 'NO'}")
    print()
    g, p, e, c = GeometryLedger(), PulseLedger(), EnergyLedger(), CorrectionCycle()
    print(f"three leading rates coincide      : {g.leading_balance_holds()}")
    print(f"leading tangential residual scale : {g.leading_tangential_residual}")
    print(f"pulse stress divergence           : {p.stress_divergence}")
    print(f"stress cancels residual (exact)   : {p.stress_cancels_residual()}")
    print(f"A_wave/u_theta == ell_wave/ell_r  : {p.ratios_agree()}")
    print(f"critical h (energy condition)     : {e.critical_h()}")
    print(f"admissible at h = 1/100           : {e.admissible_at(F(1, 100))}")
    print(f"admissible at h = 1/6             : {e.admissible_at(F(1, 6))}")
    print(f"sigma_j -> oo                     : {c.diverges()}  "
          f"(sigma_0={c.sigma_0}, step={c.step})")
    print()
    print("route-4 contrast (THIS repository's object, alpha pinned at 1):")
    for k, v in route4_contrast().items():
        print(f"  {k:<28} {_fmt(v)}")
    print()
    print("mismatches against the manuscript's printed values:",
          bad if bad else "none")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
