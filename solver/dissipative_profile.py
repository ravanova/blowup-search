"""Chen's gamma=2 dissipative gCLM candidate: profile, constants, and the Y_0 budget.

WHAT THIS MODULE IS FOR (Route-M2P, leg 125).  Leg 63's screen put ONE candidate at the top
of the target ledger in 63+ legs: gCLM with FULL LAPLACIAN dissipation (gamma = 2), advection
`a` close to 1/2, blow-up proved analytically by J. Chen, arXiv:1908.09385 (*Nonlinearity* 33
(2020) 2502).  It did not read Chen's full text, transcribe the profile's constants, or
measure `Y_0`.  This module discharges the numerical part of those three debts.

WHAT THE FULL TEXT SAYS, BECAUSE IT CHANGES WHAT THIS MODULE MUST COMPUTE.  Chen's Theorem
1.1 asserts finite-time self-similar blow-up for `a` in `(1/2 - delta, 1/2 + delta)` and
`0 <= nu <= 1` with `L = -d_xx` (gamma = 2).  But the profile it converges to is NOT a
gamma = 2 dissipative profile.  Section 2.6 closes with, verbatim:

    "Since nu(t) converges to 0, such profile is the same as the inviscid profile
     associated with a."                                     -- Chen, sec 2.6, p.12

and Remark 2.1 (p.11): "(2.43) implies that the diffusion term in (2.6) vanishes as
t -> +infty."  The self-similar object in that theorem is the EXPLICIT INVISCID a = 1/2
pole-dynamics solution, eq (2.2) p.4, reproduced verbatim in `chen_constants()` below.
So the module's job is NOT to construct a dissipative profile and assume it exists: it is to
CONSTRUCT the profile Chen actually names and to MEASURE the obstruction to a gamma = 2 one.

THE OBSTRUCTION, AND WHY IT IS AN EXACT ALGEBRAIC CONDITION.  Chen's eq (2.7) gives the
effective viscosity in dynamic-rescaling variables

    nu(t) = exp( int_0^t [ 2 c_l(s) + c_omega(s) ] ds ) C_l(0)^{-2} C_omega(0) nu.

A STEADY self-similar state requires `d nu / dt = 0`, i.e. `(2 c_l + c_omega) nu = 0`: either
`nu = 0`, or the profile's own exponents satisfy `2 c_l + c_omega = 0`.  Because
`(Omega, c_l, c_omega) -> (kappa Omega, kappa c_l, kappa c_omega)` is an exact symmetry of the
steady equation (the time-normalisation gauge; see `gclm_family`'s banked gauge discipline),
the SIGN and the RATIO are gauge-invariant while `2 c_l + c_omega` alone is not.  The
gauge-invariant form is therefore

    Delta(a) := 2 c_l / |c_omega| - 1                         (`diffusion_consistency`)

    Delta = 0  <=> a gamma = 2 self-similar profile with NON-VANISHING dissipation is
                   admissible on this branch (equivalently c_l/|c_omega| = 1/2, the heat
                   scaling: the structure collapses exactly as fast as the diffusive length).
    Delta < 0  <=> dissipation vanishes in self-similar variables, at exponential rate
                   |Delta| |c_omega| per unit rescaled time.  Chen's case.
    Delta > 0  <=> dissipation would dominate; no such branch here.

At Chen's profile `c_l = 1/3`, `c_omega = -1`, so `Delta = -1/3` EXACTLY, and Chen's own
rigorous bootstrap (2.40) bounds the integrand "above by -1/3 and a small term", tightened to
`<= -1/4` in (2.43).  `Delta` is measured here, not assumed: `newton_profile` solves for
`c_l` and it is free to land anywhere.

WHAT IS REUSED, NOT REBUILT (standing ban -- `capabilities.py` grepped first, see
writeup/novelty/leg_125.md).  `solver.gclm_family.GCLMResidual` supplies the sinh grid, the
whole-line Hilbert matrix (`solver.line_hilbert`) and the a-family steady residual convention;
`solver.gclm_rescaled.sinh_grid` the grid; `solver.nk_bounds.budget` the radii-polynomial
budget.  This module adds only the four things that do not exist anywhere in the repository:
(1) a 4th-order cumulative velocity operator (the banked trapezoid one floors the residual at
~8e-05, which would DOMINATE any Y_0 measured against it -- lesson 86), (2) the DISSIPATIVE
steady residual and its analytic Jacobian, (3) `diffusion_consistency`, and (4) the Y_0
measurement.

SCOPE, PRE-COMMITTED.  Everything here is FLOATING POINT.  No number this module produces is
a certificate, and `nk_bounds.budget`'s own header says the same of the budget.  This is the
dress rehearsal that tells you whether a certificate attempt is worth its cost.  No gCLM
DYNAMICS are run anywhere in this module (`no_dynamics_run: true`): every solve is of a
STEADY equation.  And nothing here floats a dissipation parameter against an existing
certificate's margin -- `nu` is floated only against the PROFILE EQUATION's own residual,
which is the object Chen's theorem is about, not against any Z-constant or margin.
"""

import numpy as np

from solver.gclm_family import GCLMResidual
from solver.nk_bounds import budget


# ---------------------------------------------------------------------------
# (1) Chen's transcribed constants, with per-constant provenance
# ---------------------------------------------------------------------------

def chen_constants():
    """Every constant of Chen arXiv:1908.09385 sec 2 that this leg uses, with provenance.

    Transcribed from the FULL TEXT (pdftotext -layout of arXiv:1908.09385v1), not the
    abstract.  `value` is exact where the paper gives it exactly; `None` means the paper
    leaves it unquantified and that is itself a reportable fact."""
    b = np.sqrt(3.0 / 8.0)
    return {
        "equation": {
            "value": "omega_t + a u omega_x = u_x omega - nu Lambda^gamma omega, u_x = H omega",
            "provenance": "Chen arXiv:1908.09385, abstract and eq (1.1) p.1",
        },
        "theorem_1_1": {
            "value": ("Consider (1.1) with L omega = -d_xx omega.  There exists delta > 0 such "
                      "that for a in (1/2 - delta, 1/2 + delta), 0 <= nu <= 1, (2.1) develops a "
                      "self-similar singularity in finite time for some C_c^infty initial data."),
            "provenance": "Chen, Theorem 1.1, p.3 (quoted verbatim)",
        },
        "a": {"value": 0.5, "provenance": "Chen sec 2, the a = 1/2 exact solution, eq (2.2) p.4"},
        "gamma": {"value": 2.0, "provenance": "Chen Theorem 1.1, L = -d_xx (full Laplacian)"},
        "b": {"value": float(b),
              "provenance": "Chen eq (2.2) p.4: b = sqrt(3/8); b^2 = 3/8 is used to close the "
                            "verification identity on p.4"},
        "b_squared": {"value": 0.375, "provenance": "Chen p.4, 'we have used b^2 = 3/8'"},
        "c_l": {"value": 1.0 / 3.0, "provenance": "Chen eq (2.2) p.4: c_l = 1/3"},
        "c_omega": {"value": -1.0, "provenance": "Chen eq (2.2) p.4: c_omega = -1"},
        "Omega": {"value": "Omega(x) = -2 b x / (x^2 + b^2)^2",
                  "provenance": "Chen eq (2.2) p.4"},
        "U_x": {"value": "U_x(x) = (b^2 - x^2) / (b^2 + x^2)^2",
                "provenance": "Chen eq (2.2) p.4 (= H Omega)"},
        "U": {"value": "U(x) = x / (b^2 + x^2)", "provenance": "Chen eq (2.2) p.4"},
        "ubar_x_at_0": {"value": 8.0 / 3.0,
                        "provenance": "Chen p.5, 'where we have used ubar_x(0) = 8/3' (= 1/b^2)"},
        "steady_equation": {
            "value": "(c_l x + a U) Omega_x = (c_omega + U_x) Omega,  a = 1/2",
            "provenance": "Chen sec 2 p.4, the display above eq (2.2); the layout prints the "
                          "advection coefficient a = 1/2 as a stacked fraction",
        },
        "nu_of_t": {
            "value": "nu(t) = exp(int_0^t [c_omega(s) + 2 c_l(s)] ds) C_l(0)^-2 C_omega(0) nu",
            "provenance": "Chen eq (2.7) p.5",
        },
        "nu_decay_rate_exact": {
            "value": -1.0 / 3.0,
            "provenance": "Chen (2.40) p.11, 'the integrand in the exponent is bounded above by "
                          "-1/3 and a small term'; equals 2 c_l + c_omega = 2/3 - 1 at eq (2.2)",
        },
        "nu_decay_rate_rigorous": {
            "value": -0.25,
            "provenance": "Chen eq (2.43) p.11: nu(t) <= exp(-t/4) nu(0)",
        },
        "profile_identity": {
            "value": "Since nu(t) converges to 0, such profile is the same as the inviscid "
                     "profile associated with a.",
            "provenance": "Chen sec 2.6, final sentence of the proof of Theorem 1.1, p.12 "
                          "(quoted verbatim) -- and Remark 2.1 p.11",
        },
        "delta": {
            "value": None,
            "provenance": "Chen (2.41) p.11: delta, nu_0 chosen so that "
                          "(1 + C_2 + C_3 + C_2 C_3 + C_2^2)(delta + nu_0) < 1/1000, where "
                          "C_2, C_3 are UNNAMED universal constants -- so the a-neighbourhood "
                          "is UNQUANTIFIED in the paper.  Leg 63 flagged this; it is confirmed.",
        },
        "nu_0": {
            "value": None,
            "provenance": "Chen (2.41)/(2.42) p.11.  Also note nu(0) <= C_l(0)^{-2} <= nu_0: "
                          "Theorem 1.1's '0 <= nu <= 1' is reached by taking the initial length "
                          "scale C_l(0) LARGE, i.e. the RESCALED viscosity is driven small.",
        },
        "critical_dissipation_a_le_minus1": {
            "value": "gamma = |a|^{-1}",
            "provenance": "Chen sec 1.2 p.2, and Theorem 1.5 -- stated ONLY for a <= -1, where "
                          "the a-priori L^{|a|} estimate holds",
        },
        "critical_dissipation_a_gt_minus1": {
            "value": 1.0,
            "provenance": "Chen sec 1.2 p.2: for a > -1 with ||omega||_{L^1} conserved, "
                          "'a simple scaling analysis shows that L = Lambda corresponds to the "
                          "critical dissipation'",
        },
        "blowup_data_class": {
            "value": "class 3 (omega_0 odd, omega_0 <= 0 for x > 0)",
            "provenance": "Chen Remark 1.4 p.3 -- the class in which L^1 is NOT conserved "
                          "(Lemma 3.1(b), eq (3.5)), so the L^1-based criticality of sec 1.2 "
                          "does not classify the blow-up data",
        },
        "computer_assisted": {
            "value": False,
            "provenance": "Chen sec 2.3-2.5: weighted L^2 (weight phi) and weighted H^4 "
                          "(weight psi) energy estimates, eq (2.12) p.6; no interval "
                          "arithmetic, no computer assistance anywhere in the paper",
        },
        "weights": {
            "value": "phi = (x^2+b^2)^3/(2b x^4) = -(1/omegabar)(x^2+b^2)/x^3, "
                     "psi = (x^2+b^2)^3/(2b) = -x(x^2+b^2)/omegabar",
            "provenance": "Chen eq (2.12) p.6",
        },
    }


def chen_profile(X, b=None):
    """Chen eq (2.2): the exact inviscid a = 1/2 self-similar profile and its velocity.

    Returns (Omega, U_x, U).  `U_x = H Omega` and `U(0) = 0` hold exactly."""
    b = float(np.sqrt(3.0 / 8.0)) if b is None else float(b)
    X = np.asarray(X, dtype=float)
    den = X ** 2 + b ** 2
    Omega = -2.0 * b * X / den ** 2
    U_x = (b ** 2 - X ** 2) / den ** 2
    U = X / den
    return Omega, U_x, U


# ---------------------------------------------------------------------------
# (2) high-order operators the banked machinery does not have
# ---------------------------------------------------------------------------

def _drho_matrix4(n, drho):
    """4th-order centred d/d rho matrix on a uniform rho grid; one-sided at the ends."""
    D = np.zeros((n, n))
    for i in range(2, n - 2):
        D[i, i - 2] = 1.0 / (12 * drho)
        D[i, i - 1] = -8.0 / (12 * drho)
        D[i, i + 1] = 8.0 / (12 * drho)
        D[i, i + 2] = -1.0 / (12 * drho)
    D[1, 0], D[1, 2] = -1.0 / (2 * drho), 1.0 / (2 * drho)
    D[n - 2, n - 3], D[n - 2, n - 1] = -1.0 / (2 * drho), 1.0 / (2 * drho)
    D[0, 0], D[0, 1], D[0, 2] = -3.0 / (2 * drho), 4.0 / (2 * drho), -1.0 / (2 * drho)
    D[n - 1, n - 3], D[n - 1, n - 2], D[n - 1, n - 1] = \
        1.0 / (2 * drho), -4.0 / (2 * drho), 3.0 / (2 * drho)
    return D


def _cumint_matrix4(n, drho, i0):
    """4th-order cumulative-integration matrix on the uniform rho grid, zeroed at node i0.

    Per panel [rho_i, rho_{i+1}] the Adams-Moulton 4-point rule
        int ~ h/24 * (-f_{i-1} + 13 f_i + 13 f_{i+1} - f_{i+2})
    is O(h^4), against the banked trapezoid's O(h^2).  This matters: at n = 601 the trapezoid
    velocity leaves the exact Chen profile with a 2.4124e-04 residual sup, which would DOMINATE
    any Y_0 measured against it (lesson 86 -- a bound dominated by its own evaluation error is
    a statement about the code).  This rule brings that to 3.7426e-06 (64.5x), off a velocity
    error cut from 1.4375e-04 to 7.467e-07 (192.5x)."""
    C = np.zeros((n, n))
    h = drho

    def panel(i):
        """weights for int_{rho_i}^{rho_{i+1}} f d rho."""
        w = np.zeros(n)
        if 1 <= i <= n - 3:
            w[i - 1] += -h / 24.0
            w[i] += 13.0 * h / 24.0
            w[i + 1] += 13.0 * h / 24.0
            w[i + 2] += -h / 24.0
        else:                                    # end panels: trapezoid (measure-zero effect,
            w[i] += h / 2.0                      # the profile is ~0 there)
            w[i + 1] += h / 2.0
        return w

    for i in range(i0, n - 1):                   # march up from i0
        C[i + 1] = C[i] + panel(i)
    for i in range(i0 - 1, -1, -1):              # march down from i0
        C[i] = C[i + 1] - panel(i)
    return C


# ---------------------------------------------------------------------------
# (3) the dissipative steady residual, its Jacobian, and Newton
# ---------------------------------------------------------------------------

class DissipativeProfile:
    """Steady self-similar gCLM residual WITH full-Laplacian dissipation, on the sinh grid.

        R(Omega; c_l, c_omega, nu) = (c_omega + H Omega) Omega
                                     - c_l X Omega_X - a U Omega_X + nu Omega_XX

    At nu = 0 this is exactly `gclm_family.GCLMResidual.residual`'s convention (verified in
    `test_dissipative_profile.py`), which is in turn Chen's steady equation on p.4 with the
    advection coefficient `a`.  The nu term is the new part: it is the steady form of Chen's
    dynamic-rescaling equation (2.6)."""

    def __init__(self, a=0.5, n=801, c=0.5, rho_max=8.0):
        self.a = float(a)
        self.base = GCLMResidual(a=a, n=n, c=c, rho_max=rho_max)
        self.X = self.base.X
        self.rho = self.base.rho
        self.n = self.base.n
        self.i0 = self.base.i0
        self.drho = self.base.drho
        self.X_rho = self.base.X_rho
        self.H = self.base.Hmat
        Drho = _drho_matrix4(self.n, self.drho)
        self.D = Drho / self.X_rho[:, None]                    # d/dX
        self.D2 = self.D @ self.D                              # d^2/dX^2
        # U(X) = int_0^X H Omega dX' = int_0^rho (H Omega) X_rho d rho'
        self.V = _cumint_matrix4(self.n, self.drho, self.i0) * self.X_rho[None, :]
        self.VH = self.V @ self.H

    # -- evaluation ---------------------------------------------------------
    def residual(self, Omega, c_l, c_omega, nu=0.0, a=None):
        a = self.a if a is None else float(a)
        HOm = self.H @ Omega
        Om_X = self.D @ Omega
        U = self.VH @ Omega
        R = (c_omega + HOm) * Omega - c_l * self.X * Om_X - a * U * Om_X
        if nu != 0.0:
            R = R + nu * (self.D2 @ Omega)
        return R

    def jacobian_Omega(self, Omega, c_l, c_omega, nu=0.0, a=None):
        """dR/dOmega, exact (R is quadratic in Omega, so this is not an approximation)."""
        a = self.a if a is None else float(a)
        HOm = self.H @ Omega
        Om_X = self.D @ Omega
        U = self.VH @ Omega
        J = (np.diag(Omega) @ self.H + np.diag(c_omega + HOm)
             - c_l * (self.X[:, None] * self.D)
             - a * (np.diag(Om_X) @ self.VH + np.diag(U) @ self.D))
        if nu != 0.0:
            J = J + nu * self.D2
        return J

    def dR_dcl(self, Omega):
        return -self.X * (self.D @ Omega)

    def dR_dnu(self, Omega):
        return self.D2 @ Omega

    def dR_da(self, Omega):
        return -(self.VH @ Omega) * (self.D @ Omega)

    # -- the gamma = 2 branch search ----------------------------------------
    def newton_gamma2(self, Omega0, a0, nu, c_l=0.5, c_omega=-1.0, iters=60, tol=1e-13):
        """Solve the DISSIPATIVE steady equation with the STEADINESS condition IMPOSED.

        A genuine gamma = 2 self-similar profile must satisfy BOTH
            (i)  R(Omega; c_l, c_omega, nu) = 0                (steady profile), and
            (ii) 2 c_l + c_omega = 0, i.e. Delta = 0           (steady effective viscosity,
                                                                Chen eq (2.7)).
        `newton` solves (i) and MEASURES Delta.  This routine does the converse and harder
        thing: it IMPOSES (ii) by fixing `(c_l, c_omega) = (1/2, -1)` and asks whether (i) can
        then be solved at a given `nu > 0`, with the advection `a` as the free unknown.  If it
        can, a full-Laplacian dissipative self-similar profile EXISTS and `a(nu)` locates it.
        If the residual floor stays bounded away from zero, it does not.

        Least-squares (`lstsq`): the residual of an odd profile is odd, so the system is
        rank-deficient in the even subspace by construction."""
        Om = np.array(Omega0, dtype=float)
        a = float(a0)
        hist = []
        for _ in range(iters):
            R = self.residual(Om, c_l, c_omega, nu, a=a)
            nrm = float(np.sqrt(np.mean(R ** 2)))
            hist.append(nrm)
            if nrm < tol:
                break
            J = np.zeros((self.n, self.n + 1))
            J[:, :self.n] = self.jacobian_Omega(Om, c_l, c_omega, nu, a=a)
            J[:, self.n] = self.dR_da(Om)
            step, *_ = np.linalg.lstsq(J, -R, rcond=None)
            Om = Om + step[:self.n]
            a = a + float(step[self.n])
        return {"Omega": Om, "a": a, "nu": float(nu), "c_l": float(c_l),
                "c_omega": float(c_omega),
                "residual_rms": float(np.sqrt(np.mean(
                    self.residual(Om, c_l, c_omega, nu, a=a) ** 2))),
                "history": hist}

    # -- Newton -------------------------------------------------------------
    def newton(self, Omega0, c_l0, c_omega=-1.0, nu=0.0, iters=40, tol=1e-14,
               scale_gauge=None):
        """Gauss-Newton on (Omega, c_l) with c_omega held as the time-normalisation gauge.

        Two gauges must be fixed, because the steady equation has two exact symmetries:
        amplitude `(Omega, c_l, c_omega) -> (kappa Omega, kappa c_l, kappa c_omega)` and
        spatial dilation `Omega(X) -> Omega(X/mu)` (same c's).  Fixing `c_omega` kills the
        first; `scale_gauge` (the value of `Omega_X(0)`) kills the second.  `c_l` is then a
        genuine OUTPUT -- the whole point, since `Delta` is built from it.

        Solved in least-squares form (`lstsq`): the residual row at X = 0 is identically zero
        for odd Omega, so the square system is rank-deficient by construction and a plain
        solve would be reporting the conditioning of a gauge, not a solution."""
        Om = np.array(Omega0, dtype=float)
        c_l = float(c_l0)
        g = self.D[self.i0]                       # row extracting Omega_X(0)
        target = float(g @ Om) if scale_gauge is None else float(scale_gauge)
        hist = []
        for _ in range(iters):
            R = self.residual(Om, c_l, c_omega, nu)
            gap = float(g @ Om) - target
            F = np.concatenate([R, [gap]])
            nrm = float(np.sqrt(np.mean(R ** 2)))
            hist.append(nrm)
            if nrm < tol:
                break
            JO = self.jacobian_Omega(Om, c_l, c_omega, nu)
            Jc = self.dR_dcl(Om)
            J = np.zeros((self.n + 1, self.n + 1))
            J[:self.n, :self.n] = JO
            J[:self.n, self.n] = Jc
            J[self.n, :self.n] = g
            step, *_ = np.linalg.lstsq(J, -F, rcond=None)
            Om = Om + step[:self.n]
            c_l = c_l + float(step[self.n])
        return {"Omega": Om, "c_l": c_l, "c_omega": float(c_omega), "nu": float(nu),
                "residual_rms": float(np.sqrt(np.mean(
                    self.residual(Om, c_l, c_omega, nu) ** 2))),
                "history": hist, "scale_gauge": target}


# ---------------------------------------------------------------------------
# (4) the diffusion-consistency functional -- the leg's central measurement
# ---------------------------------------------------------------------------

def diffusion_consistency(c_l, c_omega):
    """Delta = 2 c_l / |c_omega| - 1: the gauge-invariant obstruction to a gamma = 2 profile.

    Derived from Chen eq (2.7): a steady effective viscosity needs `(2 c_l + c_omega) nu = 0`.
    Dividing by `|c_omega|` removes the time-normalisation gauge, so `Delta` is invariant
    under `(Omega, c_l, c_omega) -> (kappa Omega, kappa c_l, kappa c_omega)` for every
    `kappa > 0`.

    `Delta == 0` is exactly the heat scaling `c_l/|c_omega| = 1/2`.  The functional CAN
    report zero -- `diffusion_consistency(0.5, -1.0) == 0.0` exactly -- which is the lesson-90
    check that this is a measurement and not a tautology of the code."""
    c_omega = float(c_omega)
    if c_omega == 0.0 or not np.isfinite(c_omega):
        raise ValueError(f"c_omega must be finite and non-zero, got {c_omega!r}: Delta has no "
                         "referent when the amplitude exponent vanishes (lesson 73).")
    return 2.0 * float(c_l) / abs(c_omega) - 1.0


def nu_decay_rate(c_l, c_omega):
    """The rescaled-viscosity exponent `2 c_l + c_omega` of Chen eq (2.7), as measured.

    Gauge-COVARIANT (scales with kappa), so report it alongside `diffusion_consistency`, never
    instead of it.  Chen's exact value at eq (2.2) is -1/3; his rigorous bound is <= -1/4."""
    return 2.0 * float(c_l) + float(c_omega)


# ---------------------------------------------------------------------------
# (5) Y_0 and the radii-polynomial budget -- FLOATING POINT, not a certificate
# ---------------------------------------------------------------------------

def y0_measure(dp, Omega, c_l, c_omega, nu=0.0, norm="sup"):
    """Y_0 = || A F(Omega) || with A the numerically inverted Jacobian at Omega.

    This is the radii-polynomial `Y_0`: the defect of the approximate zero, mapped through
    the approximate inverse.  `A` is built by pseudo-inverting the (rank-deficient, by gauge)
    Jacobian, so `Y_0` here is the gauge-orthogonal part of the defect -- the honest quantity,
    since the gauge directions are not errors.

    FLOAT, not interval.  Nothing here is a certificate."""
    R = dp.residual(Omega, c_l, c_omega, nu)
    J = dp.jacobian_Omega(Omega, c_l, c_omega, nu)
    corr, *_ = np.linalg.lstsq(J, R, rcond=None)
    if norm == "sup":
        return float(np.max(np.abs(corr))), float(np.max(np.abs(R)))
    if norm == "l1":
        return float(np.sum(np.abs(corr))), float(np.sum(np.abs(R)))
    raise ValueError(f"unknown norm {norm!r}: use 'sup' or 'l1'")


def z2_quadratic_constant(dp, Omega, c_l, c_omega, nu=0.0, norm="sup"):
    """Z_2: the (exact) quadratic constant of the radii polynomial for this operator.

    `F` is exactly quadratic in `Omega`, so `D^2 F` is the constant bilinear map
        B(u, v) = (H u) v + (H v) u - a [ (V H u) v_X + (V H v) u_X ]
    and `Z_2 = ||A|| * ||B||` with no higher-order remainder.  `||B||` is bounded by its
    induced operator norm on the discretisation, which is what is returned."""
    J = dp.jacobian_Omega(Omega, c_l, c_omega, nu)
    A = np.linalg.pinv(J)
    ordr = np.inf if norm == "sup" else 1
    normA = float(np.linalg.norm(A, ord=ordr))
    # ||B|| <= 2 (||H|| + |a| (||V H|| ||D|| + ||D|| ||V H||)) / 2 ; assembled directly:
    nH = float(np.linalg.norm(dp.H, ord=ordr))
    nVH = float(np.linalg.norm(dp.VH, ord=ordr))
    nD = float(np.linalg.norm(dp.D, ord=ordr))
    normB = 2.0 * (nH + abs(dp.a) * nVH * nD)
    return {"norm_A": normA, "norm_B": normB, "Z2": normA * normB,
            "norm_H": nH, "norm_VH": nVH, "norm_D": nD}


def radii_budget(Y0, Z0, Z1, Z2):
    """Thin pass-through to `solver.nk_bounds.budget` so every leg quotes ONE budget.

    Kept as a named function purely so the runner cannot silently re-implement the quadratic
    (this repository has done that before).  Returns nk_bounds' dict verbatim."""
    return budget(Y0, Z0, Z1, Z2)
