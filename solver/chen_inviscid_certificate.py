"""Object A -- Chen's INVISCID a = 1/2 gCLM profile -- against EVERY radii-polynomial
hypothesis, not just the budget.

WHAT THIS MODULE IS FOR (Route-M2CI, leg 187).  Leg 125 read Chen arXiv:1908.09385 at full
text and established that the profile his Theorem 1.1 converges to is NOT a gamma = 2
dissipative profile but the explicit INVISCID a = 1/2 pole-dynamics solution, eq (2.2) p.4
("Object A").  Its own numbers then left a lead unexploited: measured under the
radii-polynomial budget, Object A came in UNDER at all 9 tested rows (Y_0/budget 1.325e-09
to 5.800e-05).  This module asks the question that comparison does not answer: does a FULL
certificate close on Object A, with every hypothesis of the framework satisfied?

SCOPE AND FRAMING, PRE-COMMITTED AND NOT NEGOTIABLE.
  * Object A is INVISCID (Chen's own words, sec 1.5: "we construct the self-similar profile
    for the *inviscid* gCLM (1.1) with a = 1/2").  Nothing in this module bears on the
    viscous question, on the "missing rung", or on any dissipative profile.  The gamma = 2
    in the route name refers to the DISSIPATION EXPONENT OF THE DYNAMICS Chen's theorem is
    about; the PROFILE itself has nu = 0.  Do not conflate the two.
  * Object A is a PUBLISHED CLOSED FORM (Chen eq (2.2); the whole branch a <= 1 in HQWW
    arXiv:2305.05895).  A certificate centred on it has Y_0 EXACTLY ZERO -- see
    `exact_defect_numerator` -- so it establishes no existence the closed form did not
    already give.  This is stated in `writeup/novelty/leg_187.md` BEFORE any number here
    was computed.
  * Nothing in this module is a certificate.  The exact-arithmetic parts (`Fraction`) are
    rigorous; the operator parts are FLOAT and are labelled as measurements.

WHAT IS REUSED, NOT REBUILT (standing ban -- `capabilities.py` grepped first, see
writeup/novelty/leg_187.md).  `solver.dissipative_profile` supplies Chen's transcribed
constants and `chen_profile` (leg 125's territory, READ-ONLY, imported not copied) and
`DissipativeProfile` supplies the grid, the whole-line Hilbert matrix, the 4th-order
derivative/velocity operators and the analytic Jacobian, all at `nu = 0`.
`solver.nk_bounds.budget` supplies the ONE budget; `solver.certificate_guards` the ONE
hypothesis guard.  This module adds only what does not exist anywhere: the exact rational
arithmetic on Object A's defect, the EXACT one-parameter dilation orbit through it, the
kernel that orbit generates, the far-field symbol clause, and the clause battery.

THE SEVEN CLAUSES, AND WHY THEY ARE THE RIGHT SEVEN.  The imported theorem (van den Berg &
Lessard; the form `solver/certificate_guards.py` encodes) needs, for a Banach space X, a
centre xbar in X, a bounded injective A and a bounded A_dagger:

    (H1) xbar in X                                   -> `clause_space_membership`
    (H2) Y_0 >= ||A F(xbar)||                        -> `exact_defect_numerator`
    (H3) F's zero at xbar is ISOLATED (the theorem's
         CONCLUSION is existence AND uniqueness in
         the ball)                                   -> `clause_isolation`
    (H4) DF(xbar) injective on X (implied by
         Z_0 + Z_1 < 1 via Neumann)                  -> `clause_injectivity`
    (H5) Z_0 + Z_1 < 1 for SOME admissible A         -> `unbordered_Z_lower_bound`
    (H6) the far-field/tail part of A is bounded     -> `clause_farfield_symbol`
    (H7) Z_2 finite: the quadratic map bounded on X  -> `clause_quadratic_constant`

Clause H3/H4/H5 are where the answer lives, and the reason is an EXACT algebraic fact this
module proves in `Fraction` arithmetic rather than measures: the steady equation at
(a, c_l, c_omega) = (1/2, 1/3, -1) has a ONE-PARAMETER FAMILY of exact solutions through
Object A,

    Psi_g(X) = -(16/3) g^{3/2} X / (X^2 + g)^2 ,      g > 0,     Psi_{3/8} = Chen eq (2.2),

the orbit of the dilation symmetry `Omega(X) -> Omega(X/mu)`, which is an exact symmetry of
the steady equation at FIXED c_l, c_omega (H commutes with dilation and the velocity's
picked-up factor of mu cancels against Omega_X).  That the linearisation about an exact
CLM-family self-similar profile carries a scaling zero mode is PUBLISHED, not ours: Xu
arXiv:2607.19762 states for the a = 0 sibling that "the full point spectrum over C consists
exactly of {0,1}, the scaling and time-shift symmetry modes".  What is ours is the
certificate-side consequence, with its constant.
"""

from fractions import Fraction

import numpy as np

from solver.certificate_guards import hypothesis_violations
from solver.dissipative_profile import DissipativeProfile, chen_constants, chen_profile
from solver.nk_bounds import budget

# The profile's own parameters, read from leg 125's transcription (not re-typed).
A_ADVECTION = 0.5           # Chen sec 2, the a = 1/2 exact solution
C_L = Fraction(1, 3)        # Chen eq (2.2) p.4: c_l = 1/3
C_OMEGA = Fraction(-1)      # Chen eq (2.2) p.4: c_omega = -1
GAMMA_CHEN = Fraction(3, 8)  # b^2 = 3/8, Chen p.4 ("we have used b^2 = 3/8")


# ===========================================================================
# (0) exact rational-function arithmetic -- small, and deliberately not sympy
# ===========================================================================
#
# Every object below is `num(X) / D(X)**k` with D = X^2 + g and `num` a list of Fractions
# (index = power of X).  That is closed under the operations the residual needs, so the
# whole defect computation stays in exact arithmetic with no floating point anywhere.

def _p_trim(p):
    while len(p) > 1 and p[-1] == 0:
        p = p[:-1]
    return p


def _p_mul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, pi in enumerate(p):
        if pi:
            for j, qj in enumerate(q):
                out[i + j] += pi * qj
    return _p_trim(out)


def _p_add(p, q):
    n = max(len(p), len(q))
    out = [Fraction(0)] * n
    for i, pi in enumerate(p):
        out[i] += pi
    for i, qi in enumerate(q):
        out[i] += qi
    return _p_trim(out)


def _p_scale(p, c):
    return _p_trim([Fraction(c) * pi for pi in p])


def _p_der(p):
    return _p_trim([Fraction(i) * p[i] for i in range(1, len(p))] or [Fraction(0)])


class RF:
    """`num(X) / (X^2 + g)^k`, exact.  `g` is a Fraction; nothing here is a float."""

    def __init__(self, num, k, g):
        self.num = _p_trim([Fraction(c) for c in num])
        self.k = int(k)
        self.g = Fraction(g)

    def _D(self):
        return [self.g, Fraction(0), Fraction(1)]

    def __add__(self, other):
        k = max(self.k, other.k)
        a = self.num
        for _ in range(k - self.k):
            a = _p_mul(a, self._D())
        b = other.num
        for _ in range(k - other.k):
            b = _p_mul(b, self._D())
        return RF(_p_add(a, b), k, self.g)

    def __mul__(self, other):
        if isinstance(other, RF):
            return RF(_p_mul(self.num, other.num), self.k + other.k, self.g)
        return RF(_p_scale(self.num, other), self.k, self.g)

    def der(self):
        """d/dX [num / D^k] = (num' D - k num D') / D^{k+1}."""
        D, Dp = self._D(), [Fraction(0), Fraction(2)]
        top = _p_add(_p_mul(_p_der(self.num), D), _p_scale(_p_mul(self.num, Dp), -self.k))
        return RF(top, self.k + 1, self.g)

    def is_zero(self):
        return all(c == 0 for c in self.num)


def exact_defect_numerator(g=GAMMA_CHEN, kappa=None, a=Fraction(1, 2), c_l=C_L,
                           c_omega=C_OMEGA):
    """The EXACT numerator polynomial of the steady residual on the profile family.

    The family, with `g > 0` the squared length scale and `kappa` the amplitude:

        Psi   = kappa * (-2 sqrt(g) X) / D^2 ,   D = X^2 + g
        H Psi = kappa * (g - X^2) / D^2          (Chen eq (2.2), rescaled)
        U     = kappa * X / D                    (= int_0^X H Psi, U(0) = 0)

    EVERY term of `R(Psi) = (c_omega + H Psi) Psi - c_l X Psi_X - a U Psi_X` carries exactly
    one factor of `sqrt(g)` -- `H Psi` and `U` carry none -- so `R / sqrt(g)` is a rational
    function with RATIONAL coefficients and the whole computation stays exact.  Returned is
    the numerator of `R / sqrt(g)` over the common denominator `D^m`, as a list of
    `Fraction`s.  It is the zero polynomial IFF `Psi` is an exact steady solution.

    `kappa = None` selects the DISTINGUISHED amplitude `8 g / 3`, which is the one this
    module's `clause_isolation` shows solves for every `g`; pass any other value to get a
    control that must NOT vanish."""
    g = Fraction(g)
    kappa = Fraction(8, 3) * g if kappa is None else Fraction(kappa)
    a, c_l, c_omega = Fraction(a), Fraction(c_l), Fraction(c_omega)

    psi = RF([0, -2 * kappa], 2, g)                 # Psi / sqrt(g)
    h_psi = RF([kappa * g, 0, -kappa], 2, g)        # H Psi          (no sqrt(g))
    u = RF([0, kappa], 1, g)                        # U              (no sqrt(g))
    psi_x = psi.der()

    x = RF([0, 1], 0, g)
    term1 = (RF([c_omega], 0, g) + h_psi) * psi
    term2 = (x * psi_x) * (-c_l)
    term3 = (u * psi_x) * (-a)
    R = term1 + term2 + term3
    return R.num, R.k


def exact_orbit_check(gammas=(Fraction(3, 8), Fraction(1), Fraction(2), Fraction(1, 7),
                              Fraction(9, 4))):
    """CLAUSE H3, the exact half: is there a CONTINUUM of exact zeros through Object A?

    For each `g`, verifies in exact rational arithmetic that `Psi_g` (amplitude `8g/3`) has
    an identically-zero residual numerator, and -- the lesson-90 control, which CAN report
    the other answer -- that perturbing the amplitude by 1/100 does NOT.

    `g = 3/8` with amplitude `8g/3 = 1` is exactly Chen eq (2.2)."""
    rows = []
    for g in gammas:
        g = Fraction(g)
        num, _ = exact_defect_numerator(g)
        bad, _ = exact_defect_numerator(g, kappa=Fraction(8, 3) * g + Fraction(1, 100))
        rows.append({
            "gamma": str(g),
            "kappa": str(Fraction(8, 3) * g),
            "is_chen_profile": bool(g == GAMMA_CHEN),
            "numerator_coeffs": [str(c) for c in num],
            "exact_zero": all(c == 0 for c in num),
            "control_perturbed_amplitude_coeffs": [str(c) for c in bad],
            "control_is_nonzero": any(c != 0 for c in bad),
        })
    return rows


# ===========================================================================
# (1) the orbit, its generator, and the profile in float
# ===========================================================================

def orbit_profile(X, gamma=float(GAMMA_CHEN)):
    """`Psi_g(X) = -(16/3) g^{3/2} X / (X^2 + g)^2` -- the exact one-parameter family.

    At `g = 3/8` this is Chen eq (2.2) verbatim; `test_chen_inviscid_certificate.py` checks
    it against `dissipative_profile.chen_profile` to machine precision."""
    X = np.asarray(X, dtype=float)
    g = float(gamma)
    return -(16.0 / 3.0) * g ** 1.5 * X / (X ** 2 + g) ** 2


def orbit_generator(X, gamma=float(GAMMA_CHEN)):
    """`phi = d Psi_g / d g`, the tangent to the orbit -- the kernel of the linearisation.

        phi(X) = -(16/3) sqrt(g) X ((3/2) X^2 - g/2) / (X^2 + g)^3

    Decays like `X^{-3}`: exactly the profile's own rate.  That coincidence is not one --
    the orbit is the dilation orbit and dilation preserves the decay exponent -- and it is
    what `clause_farfield_symbol` prices."""
    X = np.asarray(X, dtype=float)
    g = float(gamma)
    D = X ** 2 + g
    return -(16.0 / 3.0) * np.sqrt(g) * X * (1.5 * X ** 2 - 0.5 * g) / D ** 3


def weighted_sup_norm(X, h, s):
    """`||h||_s = sup |(1 + X^2)^{s/2} h(X)|` -- the weighted sup norm, decay grading `s`."""
    X = np.asarray(X, dtype=float)
    return float(np.max(np.abs((1.0 + X ** 2) ** (0.5 * float(s)) * np.asarray(h))))


# ===========================================================================
# (2) the clauses
# ===========================================================================

def clause_space_membership(dp, s_values=(1.0, 2.0, 2.5, 2.9, 3.0, 3.1, 3.5)):
    """CLAUSE H1: is the centre in the space, and at which decay gradings?

    The profile decays like `X^{-3}`, so `||Psi||_s` is finite for `s <= 3` and INFINITE for
    `s > 3`.  On a truncated grid an infinite norm cannot be seen directly -- it shows up as
    GROWTH with the truncation radius, which is what the `ratio_vs_half_domain` column
    measures (compare the norm on the full grid against the norm on the inner half): ~1
    means converged, >> 1 means the norm is being carried by the outermost nodes and is
    divergent in the continuum."""
    X = dp.X
    Om = orbit_profile(X)
    inner = np.abs(X) <= 0.5 * float(np.max(np.abs(X)))
    rows = []
    for s in s_values:
        full = weighted_sup_norm(X, Om, s)
        half = weighted_sup_norm(X[inner], Om[inner], s)
        rows.append({"s": float(s), "norm_full_grid": full, "norm_inner_half": half,
                     "ratio_vs_half_domain": full / half if half > 0 else float("inf"),
                     "finite_in_continuum": bool(s <= 3.0)})
    return rows


def clause_isolation(dp, gamma=float(GAMMA_CHEN), s=2.0, radii=(1e-2, 1e-4, 1e-6)):
    """CLAUSE H3: is the zero ISOLATED?  The theorem CONCLUDES uniqueness in the ball.

    Every ball around Object A contains a continuum of OTHER exact zeros -- the orbit
    `Psi_g` -- so the conclusion is false and, by contraposition, the hypotheses cannot all
    hold no matter what `A` or space is chosen.  Quantified: for each target radius `r`, the
    orbit displacement `dg` that lands exactly on the sphere of radius `r`, found by
    bisection on the true (nonlinear) orbit, together with that competitor's own residual --
    which must be at the discretisation floor, because it is an exact solution too."""
    X = dp.X
    Om = orbit_profile(X, gamma)
    phi = orbit_generator(X, gamma)
    phi_norm = weighted_sup_norm(X, phi, s)
    rows = []
    for r in radii:
        lo, hi = 0.0, max(1e-12, r / max(phi_norm, 1e-300))
        for _ in range(200):
            if weighted_sup_norm(X, orbit_profile(X, gamma + hi) - Om, s) >= r:
                break
            hi *= 2.0
            if hi > 1e6:
                break
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if weighted_sup_norm(X, orbit_profile(X, gamma + mid) - Om, s) < r:
                lo = mid
            else:
                hi = mid
        dg = 0.5 * (lo + hi)
        comp = orbit_profile(X, gamma + dg)
        rows.append({
            "ball_radius_r": float(r),
            "orbit_displacement_dgamma": float(dg),
            "distance_achieved": weighted_sup_norm(X, comp - Om, s),
            "competitor_residual_sup": float(np.max(np.abs(
                dp.residual(comp, float(C_L), float(C_OMEGA), 0.0)))),
            "centre_residual_sup": float(np.max(np.abs(
                dp.residual(Om, float(C_L), float(C_OMEGA), 0.0)))),
        })
    return {"weight_s": float(s), "orbit_tangent_norm_s": phi_norm, "rows": rows}


def clause_injectivity(dp, gamma=float(GAMMA_CHEN), s=2.0):
    """CLAUSE H4: is `DF(xbar)` injective on the space?

    The orbit tangent `phi` is an exact kernel element.  Reported as the RELATIVE defect
    `||DF phi||_s / ||phi||_s`, against TWO controls that can report the other answer
    (lesson 90): the profile itself, and a localised bump.  A kernel direction and a
    non-kernel direction must differ by orders of magnitude or the measurement is a
    tautology of the code."""
    X = dp.X
    Om = orbit_profile(X, gamma)
    J = dp.jacobian_Omega(Om, float(C_L), float(C_OMEGA), 0.0)
    out = {}
    for name, v in (("orbit_tangent_phi", orbit_generator(X, gamma)),
                    ("control_profile_itself", Om),
                    ("control_localised_bump", X * np.exp(-(X ** 2)))):
        nv = weighted_sup_norm(X, v, s)
        out[name] = {"norm_s": nv,
                     "DF_image_norm_s": weighted_sup_norm(X, J @ v, s),
                     "relative_defect": weighted_sup_norm(X, J @ v, s) / nv}
    out["kernel_to_control_ratio"] = (
        out["control_localised_bump"]["relative_defect"]
        / max(out["orbit_tangent_phi"]["relative_defect"], 1e-300))
    return out


def unbordered_Z_lower_bound(dp, gamma=float(GAMMA_CHEN), s=2.0):
    """CLAUSE H5: `Z_0 + Z_1 >= 1` for EVERY admissible `A`, in EVERY space containing `phi`.

    Three lines, and no numerics in them.  The theorem's constants satisfy
    `||I - A DF(xbar)|| <= Z_0 + Z_1`.  For the exact kernel element `phi` (nonzero, and in
    the space for every `s <= 3`),

        (I - A DF(xbar)) phi = phi - A(0) = phi ,

    so `||I - A DF(xbar)|| >= ||phi|| / ||phi|| = 1`, hence `Z_0 + Z_1 >= 1` and the
    contraction factor `1 - Z_0 - Z_1` is never positive.  It does not matter how good
    `Y_0` is: with `Y_0 = 0` the radii polynomial is `p(r) = Z_2 r^2 - (1 - Z_0 - Z_1) r`,
    which is nonnegative for every `r > 0`.

    THE FLOAT COLUMN, AND WHY IT IS REPORTED IN TWO REGIMES.  The naive shadow for the
    concrete `A = pinv(DF)` this repository would build comes out at ~1e-9, NOT at 1 --
    and that is not a refutation of the argument above, it is the discretisation inverting
    a kernel that the continuum does not have.  `numpy`'s default `rcond` is a relative
    `~n * eps ~ 1e-13`, while the grid's smallest singular value is only `sigma_min/sigma_max
    ~ 1.3e-8` (n = 401) below the top -- far ABOVE the cutoff -- so `pinv` keeps the
    near-null direction, treats `J` as invertible, and returns `A J = I` to round-off.
    Truncate that direction at any honest cutoff (`rcond = 1e-6`, `1e-4`) -- which is what a
    RIGOROUS `A` is forced to do, the direction being genuinely non-invertible in the
    continuum -- and the shadow returns to 1, from below, converging as the grid refines
    (0.99998 at n = 401, 0.9999990 at n = 801).

    The clause is carried by the EXACT argument; the float columns are reported because the
    discrepancy between them is itself the measurement (lesson 86: a single number here
    would be a statement about `rcond`, not about the operator).  `sigma_ratio` is the
    independent witness that the kernel is an operator fact: it collapses like `n^-6.7`
    (1.376e-06 at n = 201 to 9.03e-12 at n = 1201), i.e. `DF` is becoming singular in the
    continuum limit, exactly as an exact kernel element requires."""
    X = dp.X
    Om = orbit_profile(X, gamma)
    phi = orbit_generator(X, gamma)
    J = dp.jacobian_Omega(Om, float(C_L), float(C_OMEGA), 0.0)
    sv = np.linalg.svd(J, compute_uv=False)
    nphi = weighted_sup_norm(X, phi, s)

    def shadow(rcond):
        A = np.linalg.pinv(J) if rcond is None else np.linalg.pinv(J, rcond=rcond)
        return weighted_sup_norm(X, phi - A @ (J @ phi), s) / nphi

    return {
        "bound_is_exact": True,
        "Z0_plus_Z1_lower_bound": 1.0,
        "argument": ("(I - A DF) phi = phi for every A, because DF phi = 0; hence "
                     "||I - A DF|| >= 1 in every norm, for every A, in every space "
                     "containing phi (every s <= 3)."),
        "one_minus_Z_upper_bound": 0.0,
        "sigma_min": float(sv[-1]),
        "sigma_max": float(sv[0]),
        "sigma_ratio": float(sv[-1] / sv[0]),
        "float_shadow_pinv_default_rcond": shadow(None),
        "float_shadow_pinv_rcond_1e-6": shadow(1e-6),
        "float_shadow_pinv_rcond_1e-4": shadow(1e-4),
        "float_shadow_note": ("the default-rcond column is ~1e-9 because numpy's cutoff "
                              "(~1e-13 relative) is BELOW sigma_min/sigma_max, so pinv "
                              "numerically inverts the near-kernel; the truncated columns "
                              "are the honest shadow and return to the exact bound 1."),
    }


def bordered_operator(dp, gamma=float(GAMMA_CHEN), s=2.0):
    """CLAUSE H6a: the STANDARD repair -- border the symmetry with a phase condition.

    Symmetry reduction / phase conditions are standard practice in validated numerics (the
    slice literature; see `writeup/novelty/leg_187.md` Q2) and this leg claims none of it.
    Unknowns `(h, dc_l)`, equations `(DF h + dR/dc_l dc_l, g(h))` with the phase functional
    `g` taken transversal to the orbit tangent.  Returns the bordered matrix and the
    conditioning that decides whether the repair is even numerically available."""
    X = dp.X
    Om = orbit_profile(X, gamma)
    phi = orbit_generator(X, gamma)
    J = dp.jacobian_Omega(Om, float(C_L), float(C_OMEGA), 0.0)
    w = (1.0 + X ** 2) ** (-float(s))          # dual weight for the phase functional
    g = w * phi
    g = g / np.linalg.norm(g)
    n = dp.n
    M = np.zeros((n + 1, n + 1))
    M[:n, :n] = J
    M[:n, n] = dp.dR_dcl(Om)
    M[n, :n] = g
    sv = np.linalg.svd(M, compute_uv=False)
    return {"M": M, "sigma_min": float(sv[-1]), "sigma_max": float(sv[0]),
            "cond": float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf"),
            "unbordered_sigma_min": float(np.linalg.svd(J, compute_uv=False)[-1])}


def clause_quadratic_constant(dp, gamma=float(GAMMA_CHEN), s=2.0):
    """CLAUSE H7: is the quadratic map bounded on the space, and is `||A||` an operator fact?

    `F` is exactly quadratic, so `D^2 F` is the constant bilinear map
    `B(u,v) = (Hu)v + (Hv)u - a[(VHu)v_X + (VHv)u_X]`, and `Z_2 = ||A|| ||B||` exactly.
    `B` contains `v_X`, which the weighted SUP norm does not control -- so the induced norm
    on the discretisation is expected to GROW with `n` if the space is wrong, and to settle
    if it is right.  The growth (or not) is the measurement; a single-resolution number here
    would be a statement about the grid (lesson 86)."""
    X = dp.X
    Om = orbit_profile(X, gamma)
    bo = bordered_operator(dp, gamma, s)
    Ainv = np.linalg.inv(bo["M"])
    W = np.diag((1.0 + X ** 2) ** (0.5 * float(s)))
    Winv = np.diag((1.0 + X ** 2) ** (-0.5 * float(s)))
    nA = float(np.linalg.norm(W @ Ainv[:dp.n, :dp.n] @ Winv, ord=np.inf))
    nH = float(np.linalg.norm(W @ dp.H @ Winv, ord=np.inf))
    nVH = float(np.linalg.norm(W @ dp.VH @ Winv, ord=np.inf))
    nD = float(np.linalg.norm(W @ dp.D @ Winv, ord=np.inf))
    nB = 2.0 * (nH + abs(dp.a) * nVH * nD)
    return {"n": int(dp.n), "weight_s": float(s), "norm_A_bordered": nA,
            "norm_H_s": nH, "norm_VH_s": nVH, "norm_D_s": nD, "norm_B_s": nB,
            "Z2": nA * nB, "profile_norm_s": weighted_sup_norm(X, Om, s)}


def clause_farfield_symbol(c_l=float(C_L), c_omega=float(C_OMEGA),
                           s_values=(1.0, 2.0, 2.5, 2.9, 2.99, 3.0, 3.5)):
    """CLAUSE H6b: the far-field symbol of the self-similar transport operator.

    Beyond the profile's support the nonlocal terms decay (`U ~ X^{-1}`, `U_x ~ X^{-2}`,
    both multiplied by a profile that is `O(X^{-3})`), so the tail operator is

        L_inf h = c_omega h - c_l X h_X ,

    which on `h ~ X^{-s}` acts as multiplication by the SYMBOL

        sigma(s) = c_omega + s c_l = s/3 - 1 ,

    zero exactly at `s = 3`.  The profile itself decays like `X^{-3}` and so does the orbit
    tangent: THE SYMBOL VANISHES EXACTLY AT THE CENTRE'S OWN DECAY RATE.  That is the same
    fact as the kernel, seen from the far field -- `X^{-3}` is the homogeneous solution of
    the tail operator -- and it prices the tail block: the tail inverse has norm
    `1/|sigma(s)| = 3/|3 - s|`, which diverges as the grading approaches the only grading at
    which the centre is a bounded-norm element with room to spare."""
    rows = []
    for s in s_values:
        sig = float(c_omega) + float(s) * float(c_l)
        rows.append({
            "s": float(s), "symbol": sig,
            "tail_inverse_norm": (float("inf") if sig == 0.0 else abs(1.0 / sig)),
            "centre_finite_norm": bool(s <= 3.0),
            "admissible": bool(s <= 3.0 and sig != 0.0),
        })
    return {"profile_decay_exponent": 3.0,
            "symbol_zero_at_s": float((0.0 - float(c_omega)) / float(c_l)),
            "rows": rows}


def measured_decay_exponent(dp, gamma=float(GAMMA_CHEN)):
    """The centre's decay exponent, MEASURED off the grid rather than asserted.

    Log-log slope of `|Psi|` over the outer decade of the grid.  It must come out at 3, and
    a control on a deliberately different profile must come out elsewhere."""
    X = dp.X
    Om = orbit_profile(X, gamma)
    m = X > 0.1 * float(np.max(X))
    slope = float(np.polyfit(np.log(X[m]), np.log(np.abs(Om[m])), 1)[0])
    ctrl = -2.0 * X / (1.0 + X ** 2) ** 1.5           # a genuine X^{-2} control
    slope_c = float(np.polyfit(np.log(X[m]), np.log(np.abs(ctrl[m])), 1)[0])
    return {"measured_slope": slope, "exponent": -slope,
            "control_slope_on_Xminus2_profile": slope_c}


# ===========================================================================
# (3) the battery, and the gate's own arithmetic
# ===========================================================================

def certificate_battery(n=801, s=2.0, rho_max=8.0):
    """Every clause at one resolution, plus the two budgets the gate is answered on."""
    dp = DissipativeProfile(a=A_ADVECTION, n=n, rho_max=rho_max)
    X = dp.X
    Om = orbit_profile(X)

    exact = exact_orbit_check()
    y0_exact = all(r["exact_zero"] for r in exact)
    lower = unbordered_Z_lower_bound(dp, s=s)
    quad = clause_quadratic_constant(dp, s=s)

    # The unbordered certificate, with the EXACT constants the clauses produced.
    unbordered = budget(0.0, 0.0, lower["Z0_plus_Z1_lower_bound"], quad["Z2"])
    # The bordered one, with Z_0 + Z_1 left as NOT MEASURED -- see the journal: this leg
    # has no interval enclosure of the tail, so it refuses to supply a number it cannot
    # bound (lesson 73).  What it CAN report is what the bordered budget would need.
    return {
        "n": int(n), "weight_s": float(s), "rho_max": float(rho_max),
        "X_max": float(np.max(X)),
        "object": "Chen arXiv:1908.09385 eq (2.2) p.4, INVISCID a = 1/2 profile (nu = 0)",
        "chen_constants_provenance": {k: v["provenance"]
                                      for k, v in chen_constants().items()
                                      if k in ("a", "b_squared", "c_l", "c_omega", "Omega",
                                               "profile_identity", "computer_assisted")},
        "H1_space_membership": clause_space_membership(dp),
        "H2_exact_defect_is_zero": y0_exact,
        "H2_exact_rows": exact,
        "H2_float_grid_defect_sup": float(np.max(np.abs(
            dp.residual(Om, float(C_L), float(C_OMEGA), 0.0)))),
        "H3_isolation": clause_isolation(dp, s=s),
        "H4_injectivity": clause_injectivity(dp, s=s),
        "H5_Z_lower_bound": lower,
        "H6a_bordered": {k: v for k, v in bordered_operator(dp, s=s).items() if k != "M"},
        "H6b_farfield_symbol": clause_farfield_symbol(),
        "H6c_measured_decay": measured_decay_exponent(dp),
        "H7_quadratic": quad,
        "unbordered_budget": unbordered,
        "bordered_budget_requirement": {
            "Y_0": 0.0,
            "note": ("with Y_0 = 0 exactly the radii polynomial is p(r) = Z_2 r^2 - "
                     "(1 - Z_0 - Z_1) r, so ANY bordered Z_0 + Z_1 < 1 closes it -- and "
                     "the closure would assert a zero at a point already known to be one. "
                     "The existence content is nil; see clause H2."),
            "Z2_at_this_resolution": quad["Z2"],
            "Z0_plus_Z1": None,
            "Z0_plus_Z1_status": ("NOT MEASURED -- bounding it needs a rigorous enclosure "
                                  "of the tail block, which this leg does not build and "
                                  "solver/interval_certificate.py's banked ceiling says "
                                  "this repository does not have."),
        },
        "guard_on_unbordered_constants": hypothesis_violations(
            (("Y_0", 0.0), ("Z_0", 0.0), ("Z_1", lower["Z0_plus_Z1_lower_bound"]),
             ("Z_2", quad["Z2"])), allow_none=False),
    }


def divergence_exponents(ns=(201, 301, 401, 601, 801, 1201), s=2.0):
    """CLAUSE H7, decided: does `Z_2` SETTLE with resolution, or diverge?

    Lesson 86 in its sharpest form.  A radii-polynomial `Z_2` is an OPERATOR norm; if the
    discretisation's value grows without bound as `n -> infinity` then the quadratic map is
    not bounded on the space that was chosen, and no single-resolution number for it is a
    certificate constant -- it is a statement about the grid.

    Reported as least-squares slopes in `log n`, over a 6x range of `n`, together with the
    raw ladder so the fit can be checked rather than trusted.  The `sigma_ratio` slope is
    the negative control that CAN come out flat: if the kernel were a grid artifact,
    `sigma_min/sigma_max` would settle instead of collapsing."""
    rows = []
    for n in ns:
        dp = DissipativeProfile(a=A_ADVECTION, n=n)
        q = clause_quadratic_constant(dp, s=s)
        J = dp.jacobian_Omega(orbit_profile(dp.X), float(C_L), float(C_OMEGA), 0.0)
        sv = np.linalg.svd(J, compute_uv=False)
        rows.append({"n": int(n), "Z2": q["Z2"], "norm_A_bordered": q["norm_A_bordered"],
                     "norm_B_s": q["norm_B_s"], "sigma_ratio": float(sv[-1] / sv[0])})

    ln = np.log([r["n"] for r in rows])
    slopes = {k: float(np.polyfit(ln, np.log([r[k] for r in rows]), 1)[0])
              for k in ("Z2", "norm_A_bordered", "norm_B_s", "sigma_ratio")}
    return {
        "weight_s": float(s), "rows": rows, "slopes_in_log_n": slopes,
        "Z2_diverges": bool(slopes["Z2"] > 0.5),
        "Z2_growth_over_ladder": rows[-1]["Z2"] / rows[0]["Z2"],
        "sigma_ratio_collapse_over_ladder": rows[0]["sigma_ratio"] / rows[-1]["sigma_ratio"],
        "reading": ("Z_2 grows like n^%.2f over a %gx range of n, so it is NOT an operator "
                    "constant in the weighted sup space at s = %g; sigma_min/sigma_max "
                    "collapses like n^%.2f, so the kernel is an operator fact and not the "
                    "grid." % (slopes["Z2"], rows[-1]["n"] / rows[0]["n"], s,
                               slopes["sigma_ratio"])),
    }


def gate_verdict(battery, divergence):
    """Route-M2CI's pre-committed gate, answered on the battery -- never on `Y_0`.

    THE GATE (verbatim, pre-committed): "Does a full radii-polynomial certificate close on
    Chen's gamma = 2 inviscid profile (Object A), using leg 125's own transcribed constants
    and recovered shape as the starting construction, with every hypothesis of the
    certificate framework satisfied (not just the budget comparison leg 125 already made)?"

    The answer is decided by two clauses that fail for reasons that are not numerical, and
    a third framing fact that would drain the YES branch even if they did not."""
    exact_ok = battery["H2_exact_defect_is_zero"]
    z_lb = battery["H5_Z_lower_bound"]["Z0_plus_Z1_lower_bound"]
    return {
        "gate": ("Does a full radii-polynomial certificate close on Chen's gamma = 2 "
                 "inviscid profile (Object A), with EVERY hypothesis of the framework "
                 "satisfied, not just the budget comparison leg 125 already made?"),
        "answer": "NO",
        "failing_clauses": ["H3 isolation", "H5 contraction (Z_0 + Z_1 < 1)",
                            "H7 quadratic constant Z_2 bounded"],
        "H3_H5_reason": (
            "Object A is not an isolated zero.  It lies on the EXACT one-parameter dilation "
            "orbit Psi_g = -(16/3) g^{3/2} X / (X^2 + g)^2, whose residual numerator is the "
            "ZERO POLYNOMIAL in exact rational arithmetic at every g tested (controls with "
            "perturbed amplitude are nonzero).  The tangent phi = dPsi_g/dg is therefore an "
            "exact kernel element of DF, so (I - A DF) phi = phi and ||I - A DF|| >= 1 for "
            "EVERY admissible A, in every space containing phi (every s <= 3).  Hence "
            "Z_0 + Z_1 >= %g and the contraction factor 1 - Z_0 - Z_1 <= 0.  No choice of "
            "A, weight s, or truncation repairs this: it is an algebraic property of the "
            "steady equation's symmetry group, not a numerical shortfall." % z_lb),
        "H7_reason": divergence["reading"],
        "why_Y0_was_never_the_binding_clause": (
            "Leg 125 measured Y_0/budget between 1.325e-09 and 5.800e-05 and read that as "
            "headroom.  This leg shows Y_0 is EXACTLY ZERO -- the best value the framework "
            "admits, since the centre is an exact solution -- and the certificate still "
            "cannot close.  Budget-under was never evidence about the clauses that fail."),
        "and_the_YES_branch_would_have_been_hollow": (
            "Because Y_0 = 0 exactly, the radii polynomial reduces to "
            "p(r) = Z_2 r^2 - (1 - Z_0 - Z_1) r, so ANY bordered Z_0 + Z_1 < 1 would close "
            "it -- and would assert a zero at a point ALREADY PUBLISHED IN CLOSED FORM "
            "(Chen arXiv:1908.09385 eq (2.2); the whole branch a <= 1 in HQWW "
            "arXiv:2305.05895).  The existence content would be nil.  This was written "
            "down in writeup/novelty/leg_187.md BEFORE any number here was computed."),
        "scope": ("INVISCID (nu = 0), Chen's own framing.  Nothing here bears on the "
                  "viscous 'missing rung' question, which remains exactly as open as "
                  "leg 125 left it."),
        "exact_defect_verified": bool(exact_ok),
        "Z0_plus_Z1_lower_bound": float(z_lb),
    }


def resolution_ladder(ns=(401, 601, 801), s=2.0):
    """The clauses that could be discretisation artifacts, across resolutions.

    Lesson 86 and lesson 72: report the SHAPE of the ladder, not one endpoint.  A quantity
    that settles is an operator fact; one that grows with `n` is the grid talking."""
    rows = []
    for n in ns:
        dp = DissipativeProfile(a=A_ADVECTION, n=n)
        inj = clause_injectivity(dp, s=s)
        bo = bordered_operator(dp, s=s)
        quad = clause_quadratic_constant(dp, s=s)
        rows.append({
            "n": int(n),
            "grid_defect_sup": float(np.max(np.abs(
                dp.residual(orbit_profile(dp.X), float(C_L), float(C_OMEGA), 0.0)))),
            "kernel_relative_defect": inj["orbit_tangent_phi"]["relative_defect"],
            "control_relative_defect": inj["control_localised_bump"]["relative_defect"],
            "kernel_to_control_ratio": inj["kernel_to_control_ratio"],
            "sigma_min_unbordered": bo["unbordered_sigma_min"],
            "sigma_min_bordered": bo["sigma_min"],
            "bordered_cond": bo["cond"],
            "norm_A_bordered": quad["norm_A_bordered"],
            "norm_B_s": quad["norm_B_s"],
            "Z2": quad["Z2"],
        })
    return rows
