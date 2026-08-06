"""gCLM self-similar profiles at FULL-LAPLACIAN dissipation (gamma = 2), Route-M2P.

WHY THIS MODULE EXISTS
----------------------
Leg 63 (Route-M2, branch `leg/m2-v1`, parked) screened every certification target this
repository has ever ranked and found exactly one that passes its multiplier/shift screen:
gCLM with full Laplacian dissipation, `gamma = 2`, whose blow-up is PROVED analytically by
J. Chen, arXiv:1908.09385 (Nonlinearity 33 (2020) 2502-2532).  Leg 63 read only the
abstract.  Leg 125 read the full text.  **What the full text says changes the object**, and
that reading is transcribed here in `CHEN_1908_09385` with page/equation provenance so no
later leg has to re-derive it from an abstract again (this repository has been burned twice
by abstract-depth reading: leg 53/BDL, leg 64 Trap 1).

THE HEADLINE, BEFORE ANY CODE
-----------------------------
Chen's Theorem 1.1 does prove finite-time self-similar blow-up at `gamma = 2`.  But the
profile he supplies at `gamma = 2` is the **INVISCID** profile.  Verbatim, p.4 sec 2:

    "Firstly, we study the inviscid problem, i.e. nu = 0. ... For a = 1/2, Plugging this
     ansatz in (2.1) with nu = 0 yields (c_l x + 1/2 U) Omega_x = (c_omega + U_x) Omega,
     where U_x = H Omega.  Surprisingly, it has the following analytic self-similar
     solution
        Omega = -2 b x / (x^2 + b^2)^2,  U_x = (b^2 - x^2)/(b^2 + x^2)^2,
        U = x/(b^2 + x^2),  c_l = 1/3,  c_omega = -1,
     where b = sqrt(3/8)."                                             -- (2.2), p.4

and immediately after, verbatim, the sentence that decides this module's whole question:

    "In this self-similar blowup, the spatial blowup scaling is c_l = 1/3, if we add the
     diffusion term, such term is asymptotically small compared to the nonlinear term in
     the equation of the self-similar variables.  In our later analysis, we will treat the
     diffusion term as a small perturbation to the nonlinear part, especially the vortex
     stretch term u_x omega."                                          -- p.4, sec 2

Everywhere `nu` appears in Chen's argument it appears as the TIME-DEPENDENT `nu(t)`, and
`nu(t) -> 0`.  The two places that fix the steady object are (p.5, eqs (2.7) and (2.8)):

    nu(t) = exp( int_0^t (c_omega(s) + 2 c_l(s)) ds ) C_l(0)^{-2} C_omega(0) nu     (2.7)
    bar c_omega(t) = -1 - nu(t) bar omega_xxx(0) / bar omega_x(0)                   (2.8)

and `c_omega + 2 c_l = -1 + 2/3 = -1/3 < 0`, so `nu(t) -> 0` exponentially in the rescaled
time.  **There is therefore no `nu`-dependent steady profile in Chen's paper to certify.**
The approximate steady state (2.8) IS the inviscid profile (2.2).

The consequence for this repository is recorded, not argued: the thing leg 63 ranked first
-- "a dissipative self-similar profile with a proved blow-up behind it" -- does not exist
as a distinct object at `gamma = 2`.  What exists is an exact, closed-form, INVISCID
profile.  This module builds both, measures both, and reports the magnitudes.

WHAT THIS MODULE DOES NOT DO (bans, read from `plan_of_record.py`)
-----------------------------------------------------------------
* **No gCLM time evolution.** Newton on a steady residual only; the shipped JSON records
  `no_dynamics_run: true`.  The "another gCLM measurement leg" ban is about running the
  model's blow-up dynamics (Stage 3.5's exhaustion), not about steady profile algebra.
* **No dissipation parameter is floated against any certificate's margin.**  That is stage
  V *as posed* and it is banned; the DM's leg-125 ruling makes it an explicit tripwire.
  `nu` appears here as a FIXED constant, never as a continuation parameter, and there is no
  existing certificate here whose margin could be floated.  Lushnikov-Silantyev-Siegel
  (arXiv:2207.07548) sec 2 note independently that `nu` is a pure gauge for this equation
  -- "By rescaling each of t and omega, we can eliminate nu from the problem.  We therefore
  set nu = 1 without loss of generality" -- so a `nu` sweep is not merely banned, it is
  vacuous.
* `capabilities.py` was grepped before this file existed (standing ban).  Nearest entries
  are `solver/fractional_gclm.py` (Lambda^s relevance thresholds, no profile solve),
  `solver/critical_dissipation.py` (criticality, not gamma = 2) and `solver/gclm_family.py`
  (the INVISCID rescaled residual).  None holds a dissipative steady profile.

THE TWO OBJECTS
---------------
Write `U_X = H Omega`, `U(0) = 0`.  Both objects live on the whole line, odd `Omega`.

  **Object A -- CHEN's object, as his text poses it** (`nu = 0`):

      F_A(Omega) = (c_omega + U_X) Omega - (c_l X + a U) Omega_X                   = 0

  At `a = 1/2` this has the exact closed form (2.2) with `c_l = 1/3, c_omega = -1,
  b = sqrt(3/8)`.  That closed form is this module's KNOWN-ANSWER GATE.

  **Object B -- the profile that WOULD have to exist for leg 63's reading to hold**:

      F_B(Omega) = (c_omega + U_X) Omega - (c_l X + a U) Omega_X + nu Omega_XX      = 0

  A steady state of Chen's dynamic-rescaling equation (2.6) with `nu != 0` requires `nu(t)`
  to be constant, i.e. `c_omega + 2 c_l = 0` by (2.7) -- the diffusive scaling.  Object B
  imposes exactly that.  Chen's own exponents violate it (`-1 + 2/3 = -1/3`), which is the
  same fact as "the diffusion term is asymptotically small", seen from the steady side.

GAUGE DISCIPLINE (banked lesson, `solver/gclm_family.py`)
--------------------------------------------------------
`c_l` and `c_omega` are a NORMALIZATION gauge, not results.  The gauge-invariant content is
the ratio `c_l / c_omega` and the profile SHAPE.  Both objects here fix the gauge by the
ORIGIN RELATION, which is not a choice but an identity: differentiating `F` at `X = 0` for
odd `Omega` gives

    c_omega = c_l + (a - 1) U_X(0),

and Chen's constants satisfy it exactly -- `a = 1/2`, `U_X(0) = 1/b^2 = 8/3`,
`c_l = 1/3` => `c_omega = 1/3 - (1/2)(8/3) = -1`.  The AMPLITUDE gauge is fixed by
`c_omega = -1` (Object A) or by the diffusive constraint `c_omega + 2 c_l = 0` (Object B);
the DILATION gauge is fixed by the bordered row `Omega_X(0) = -2/b^3`.  See
`SteadyProfile.OMX0_TARGET` for why the obvious-looking alternative `U_X(0) = 8/3` is a
tautology that pins nothing.

THE CEILING, PART OF THE ENTRY
------------------------------
Every constant below is computed on the **TRUNCATED DISCRETE** system on the sinh grid, in
FLOAT, with `A = inv(J)` an exact float inverse.  The far-field tail beyond the grid is NOT
bounded, and `Z_1` is therefore float conditioning rather than a rigorous bound -- exactly
the ceiling `solver/interval_certificate.py` carries for L1 step one.  A `Y_0` under budget
here is a NECESSARY condition for a certificate, never a sufficient one.
"""

import numpy as np

from solver.gclm_rescaled import sinh_grid
from solver.line_hilbert import line_hilbert_matrix
from solver.target_selection import radii_polynomial, y0_budget

# --------------------------------------------------------------------------
# (A) the transcription -- every constant, with provenance
# --------------------------------------------------------------------------
# Source: J. Chen, "Singularity formation and global well-posedness for the generalized
# Constantin-Lax-Majda equation with dissipation", arXiv:1908.09385v1 (25 Aug 2019);
# Nonlinearity 33 (2020) 2502-2532.  Page numbers are the arXiv v1 PDF's own.
CHEN_1908_09385 = {
    "arxiv": "1908.09385v1",
    "journal": "Nonlinearity 33 (2020) 2502-2532",
    "equation_studied": {
        "where": "p.1 abstract and eq (1.1)",
        "verbatim": ("omega_t + a u omega_x = u_x omega - nu Lambda^gamma omega, "
                     "u_x = H omega"),
    },
    "theorem_1_1": {
        "where": "p.3, Theorem 1.1 (Finite time blow-up for a close to 1/2)",
        "verbatim": ("Consider (1.1) with L omega = -partial_xx omega. There exists "
                     "delta > 0 such that for a in (1/2 - delta, 1/2 + delta), "
                     "0 <= nu <= 1, (2.1) develops a self-similar singularity in finite "
                     "time for some C_c^infty initial data."),
        # THE a-NEIGHBOURHOOD IS UNQUANTIFIED IN THE PAPER.  delta is asserted to exist and
        # is never given a numerical value anywhere in the text.  Leg 63 flagged this as
        # unknown; the full-text read confirms it is unknown IN THE SOURCE, not merely
        # unread.  Any certificate attempt would have to supply its own delta.
        "delta_quantified": False,
        "nu_range": (0.0, 1.0),
        "gamma": 2.0,
        "L": "-partial_xx  (FULL Laplacian, gamma = 2)",
    },
    "remark_1_2": {
        "where": "p.3, Remark 1.2",
        "verbatim": ("nu = 0 corresponds to the inviscid case. If the dissipative operator "
                     "is replaced by fractional Laplacian Lambda^gamma with gamma in "
                     "[0,2], one can apply similar analysis to obtain finite time blowup. "
                     "We focus on the full Laplacian for simplicity."),
    },
    # (2.2) -- THE PROFILE.  Note the header: Chen derives it for the INVISCID problem.
    "profile_2_2": {
        "where": "p.4, eq (2.2), inside sec 2 after 'Firstly, we study the inviscid "
                 "problem, i.e. nu = 0.'",
        "verbatim": ("Omega = -2bx/(x^2+b^2)^2, U_x = (b^2-x^2)/(b^2+x^2)^2, "
                     "U = x/(b^2+x^2), c_l = 1/3, c_omega = -1, where b = sqrt(3/8)"),
        "b_squared": 3.0 / 8.0,          # b^2 = 3/8, used to null the residual (p.4)
        "c_l": 1.0 / 3.0,
        "c_omega": -1.0,
        "inviscid": True,                # <-- the load-bearing field
    },
    "diffusion_is_subdominant": {
        "where": "p.4, immediately after the verification of (2.2)",
        "verbatim": ("In this self-similar blowup, the spatial blowup scaling is "
                     "c_l = 1/3, if we add the diffusion term, such term is asymptotically "
                     "small compared to the nonlinear term in the equation of the "
                     "self-similar variables. In our later analysis, we will treat the "
                     "diffusion term as a small perturbation to the nonlinear part, "
                     "especially the vortex stretch term u_x omega."),
    },
    # (2.7)-(2.8) -- where nu actually enters, and why it leaves.
    "nu_of_t_2_7": {
        "where": "p.5, eq (2.7)",
        "verbatim": ("nu(t) = C_l(t)^{-2} C_omega(t) nu = exp(int_0^t (c_omega(s) + "
                     "2 c_l(s)) ds) C_l(0)^{-2} C_omega(0) nu"),
        "exponent_at_chen_constants": -1.0 + 2.0 / 3.0,   # = -1/3 < 0  => nu(t) -> 0
    },
    "approximate_steady_state_2_8": {
        "where": "p.5, eq (2.8)",
        "verbatim": ("bar omega = -2bx/(x^2+b^2)^2, bar u_x = H bar omega = "
                     "(b^2-x^2)/(b^2+x^2)^2, bar u = x/(x^2+b^2), "
                     "bar c_l = 1/3 - (a - 1/2) bar u_x(0), "
                     "bar c_omega(t) = -1 - nu(t) bar omega_xxx(0)/bar omega_x(0), "
                     "b = sqrt(3/8)"),
        # the two derived constants, closed form, verified in test_dissipative_profile.py
        "ux0": 8.0 / 3.0,                     # bar u_x(0) = 1/b^2 = 8/3
        "omega_xxx0_over_omega_x0": -32.0,    # = -12/b^2 = -32 exactly
    },
    # criticality, and the resolution of the gamma tension a prior verifier flagged
    "criticality_a_gt_minus1": {
        "where": "p.2, sec 1.2",
        "verbatim": ("We will show that for several classes of initial data, ||omega||_L1 "
                     "is conserved. In these cases, a simple scaling analysis shows that "
                     "L = Lambda corresponds to the critical dissipation."),
        "gamma_critical": 1.0,
    },
    "criticality_a_le_minus1": {
        "where": "p.2, sec 1.2",
        "verbatim": ("For (1.1) with a <= -1, we will show that the equation possesses "
                     "a-priori L^{|a|} estimate, i.e. ||omega(t,.)||_{L^{|a|}} <= "
                     "||omega_0||_{L^{|a|}}, which makes Lambda^gamma with gamma = |a| - 1 "
                     "the critical dissipation with respect to the natural scaling of the "
                     "equation."),
        # NOTE, and this correction matters: the formula is gamma = |a| - 1, NOT
        # gamma = |a|^{-1}.  The |a|^{-1} form carried into this repository by a prior
        # verifier's leg-64 review is a TRANSCRIPTION SLIP, corrected here against p.2.
        "gamma_critical_formula": "gamma = |a| - 1",
        "prior_repo_transcription": "gamma = |a|^{-1}  (WRONG, corrected leg 125)",
    },
}

B_CHEN = np.sqrt(3.0 / 8.0)


def chen_profile(X, b=B_CHEN):
    """Chen (2.2), p.4: the exact INVISCID a = 1/2 self-similar profile and its velocity.

    Returns (Omega, U_x, U).  This is a closed form, not a solve -- it is the
    known-answer gate every Newton run in this module is measured against.
    """
    X = np.asarray(X, dtype=float)
    b2 = b * b
    d = X * X + b2
    return -2.0 * b * X / d ** 2, (b2 - X * X) / d ** 2, X / d


def chen_gamma_tension():
    """Resolve the gamma tension flagged before this leg, from the located text.

    The tension as posed: Chen's criticality formula is said to give one exponent while
    the abstract's headline is `a` close to 1/2 with `gamma = 2`.  What the full text
    actually says (all page refs in `CHEN_1908_09385`):

    1. The formula is `gamma = |a| - 1`, and it applies ONLY for `a <= -1` (p.2, sec 1.2),
       where the `L^{|a|}` a-priori estimate exists.  At `a = 1/2` it does not apply at all.
       (The `gamma = |a|^{-1}` form previously carried in this repository is a slip.)
    2. For `a > -1` -- which contains `a = 1/2` -- criticality comes from `L^1`
       conservation and is `gamma = 1` (p.2, sec 1.2).  So `gamma = 2` at `a = 1/2` is
       STRONGER than critical, i.e. the regime where one naively expects global existence.
    3. There is NO CONTRADICTION, and the reason is the scaling, not the criticality:
       Chen's self-similar exponents are `c_l = 1/3`, `c_omega = -1`.  Diffusion-balanced
       scaling at `gamma = 2` would need `c_l = 1/2`.  Since `c_l = 1/3 < 1/2`, the
       diffusion term is asymptotically SMALLER than the nonlinearity near the singularity
       (p.4, quoted in `diffusion_is_subdominant`).  The blow-up is inviscid-dominated and
       survives arbitrarily strong dissipation of this form for `0 <= nu <= 1`.
    4. Theorem 1.3's global well-posedness (which would be the apparent conflict) is stated
       for initial data in Class 1 and Class 2 (p.3).  Chen's blow-up data is Class 3, for
       which Theorem 1.3 gives only a one-point blow-up criterion, and Remark 1.4 says so
       explicitly: "(1.4) is sharp due to the blowup result in Theorem 1.1."

    Returns the numbers a later leg can check without re-reading the paper.
    """
    c_l, c_omega = CHEN_1908_09385["profile_2_2"]["c_l"], CHEN_1908_09385["profile_2_2"]["c_omega"]
    gamma = CHEN_1908_09385["theorem_1_1"]["gamma"]
    return {
        "gamma": gamma,
        "c_l": c_l,
        "c_omega": c_omega,
        "c_l_diffusive_balance": 1.0 / gamma,          # 1/2 at gamma = 2
        "c_l_minus_balance": c_l - 1.0 / gamma,        # -1/6 < 0 => diffusion subdominant
        "diffusion_subdominant": bool(c_l < 1.0 / gamma),
        "nu_of_t_exponent": c_omega + 2.0 * c_l,       # -1/3 < 0 => nu(t) -> 0
        "nu_decays_in_rescaled_time": bool(c_omega + 2.0 * c_l < 0.0),
        "gamma_critical_a_gt_minus1": 1.0,
        "gamma_critical_formula_a_le_minus1": "gamma = |a| - 1",
        "formula_applies_at_a_half": False,
        "profile_at_gamma_2_is_inviscid": True,
    }


# --------------------------------------------------------------------------
# (B) the discrete operators
# --------------------------------------------------------------------------
class Grid:
    """Whole-line sinh grid X = c sinh(rho) plus the operators the residual needs.

    Built once per resolution: the dense Hilbert matrix is O(n^2) to build and is reused
    by every Newton step and every constant.
    """

    def __init__(self, n=401, c=0.5, rho_max=8.0):
        self.rho, self.X = sinh_grid(n, c=c, rho_max=rho_max)
        self.n = self.X.size
        self.drho = float(self.rho[1] - self.rho[0])
        self.c, self.rho_max = float(c), float(rho_max)
        self.Xmax = float(self.X.max())
        self.i0 = self.n // 2                       # index of X = 0 (n is odd)
        self.H = line_hilbert_matrix(self.X)
        self.Drho = _d_drho_matrix(self.n, self.drho)
        # dX/drho = c cosh(rho); d/dX = (1/X_rho) d/drho
        self.Xrho = self.c * np.cosh(self.rho)
        self.D = (1.0 / self.Xrho)[:, None] * self.Drho             # d/dX
        self.D2 = self.D @ self.D                                   # d^2/dX^2
        self.XD = self.X[:, None] * self.D                          # X d/dX
        # U(X) = int_0^X H Omega dX' = int_0^rho (H Omega) X_rho drho', integrated on the
        # UNIFORM rho grid with a 4th-order cumulative rule so that the velocity is not the
        # accuracy bottleneck.  (Cumulative trapezoid in X is 2nd order and WAS the
        # bottleneck: it held the known-answer residual to order 2.00 while the Hilbert
        # transform and the derivative stencil both deliver 4.)
        self.C = _cumulative_matrix(self.n, self.drho, self.i0)
        self.V = self.C @ (self.Xrho[:, None] * self.H)             # U = int_0^X H Omega

    def odd_mask(self):
        """Boolean mask of the strictly-positive nodes: the independent unknowns."""
        return self.X > 0.0

    def embed_odd(self, v_pos):
        """Lift values on X > 0 to a full odd grid function (Omega(0) = 0)."""
        full = np.zeros(self.n)
        idx = np.where(self.odd_mask())[0]
        full[idx] = v_pos
        full[self.n - 1 - idx] = -v_pos
        return full


def _d_drho_matrix(n, drho):
    """4th-order centred d/drho on the uniform rho grid; one-sided at the four ends.

    Same stencil family as `solver/gclm_family._drho_centered4`, built as a MATRIX because
    this module needs an exact Jacobian, not just an action.
    """
    D = np.zeros((n, n))
    for i in range(2, n - 2):
        D[i, i - 2:i + 3] = np.array([1.0, -8.0, 0.0, 8.0, -1.0]) / (12.0 * drho)
    # second-order one-sided at the ends; profiles are ~0 there (Omega ~ X^{-3})
    D[0, 0:3] = np.array([-3.0, 4.0, -1.0]) / (2.0 * drho)
    D[1, 0:3] = np.array([-1.0, 0.0, 1.0]) / (2.0 * drho)
    D[n - 2, n - 3:n] = np.array([-1.0, 0.0, 1.0]) / (2.0 * drho)
    D[n - 1, n - 3:n] = np.array([1.0, -4.0, 3.0]) / (2.0 * drho)
    return D


def _cumulative_matrix(n, h, i0):
    """Matrix C with (C g)_j = int_{rho_{i0}}^{rho_j} g drho', 4th order, uniform step h.

    Composite Simpson to the nearest even offset, then the 4th-order half-step correction
    `(h/12)(5 g_k + 8 g_{k+1} - g_{k+2})` for an odd offset.  `U(0) = 0` is the gauge, so
    row `i0` is zero and the integral runs outward from the origin in both directions.
    """
    C = np.zeros((n, n))
    # outward, X > 0
    for j in range(i0 + 1, n):
        if (j - i0) % 2 == 0:                       # even offset: extend by one Simpson panel
            C[j] = C[j - 2]
            C[j, j - 2] += h / 3.0
            C[j, j - 1] += 4.0 * h / 3.0
            C[j, j] += h / 3.0
        else:                                       # odd offset: one 4th-order half step
            k = j - 1
            C[j] = C[k]
            if k + 2 <= n - 1:
                C[j, k] += 5.0 * h / 12.0
                C[j, k + 1] += 8.0 * h / 12.0
                C[j, k + 2] += -h / 12.0
            else:                                   # last node: reach inward instead
                C[j, k - 1] += -h / 12.0
                C[j, k] += 8.0 * h / 12.0
                C[j, k + 1] += 5.0 * h / 12.0
    # outward, X < 0 (mirror of the same rules, with the sign of the interval)
    for j in range(i0 - 1, -1, -1):
        if (i0 - j) % 2 == 0:
            C[j] = C[j + 2]
            C[j, j + 2] -= h / 3.0
            C[j, j + 1] -= 4.0 * h / 3.0
            C[j, j] -= h / 3.0
        else:
            k = j + 1
            C[j] = C[k]
            if k - 2 >= 0:
                C[j, k] -= 5.0 * h / 12.0
                C[j, k - 1] -= 8.0 * h / 12.0
                C[j, k - 2] -= -h / 12.0
            else:
                C[j, k + 1] -= -h / 12.0
                C[j, k] -= 8.0 * h / 12.0
                C[j, k - 1] -= 5.0 * h / 12.0
    return C


# --------------------------------------------------------------------------
# (C) the two residuals
# --------------------------------------------------------------------------
class SteadyProfile:
    """Steady self-similar residual for gCLM, BORDERED, with optional gamma = 2 dissipation.

        F_1(Omega, c_l) = (c_omega + H Omega) Omega - (c_l X + a U) Omega_X + nu Omega_XX
        F_2(Omega)      = U_X(0) - ux0_target

    WHY IT IS BORDERED, AND WHY THE FIRST ATTEMPT AT THIS MODULE WAS WRONG
    ---------------------------------------------------------------------
    The unbordered residual has a SINGULAR Jacobian, exactly, for a structural reason, and
    reporting `Y_0 = ||A F||` through a numerically-inverted singular `A` produces numbers
    that are pure conditioning noise.  (Measured, on the way here: `A_norm` ~ 1e8..1e11 and
    `Y_0` = 0.179/0.190/0.148 at n = 201/401/801, i.e. INDEPENDENT of resolution -- a `Y_0` that does not fall when the residual
    falls 4 orders is the signature of an inverse that is not one.)  The equation carries
    TWO exact one-parameter gauge symmetries:

      * **dilation**   Omega(X) -> Omega(mu X), with (c_l, c_omega) unchanged.  For Chen's
        family this is exactly `b -> b/mu` with an amplitude factor: `Omega_b(mu X) =
        mu^{-2} Omega_{b/mu}(X)`.  Its infinitesimal generator `X Omega_X` is a null vector.
      * **amplitude**  (Omega, c_l, c_omega) -> lambda (Omega, c_l, c_omega).  This is the
        gauge `solver/gclm_family.py`'s docstring warns about: "c_omega, c_l are a
        NORMALIZATION gauge, not results.  The physical, gauge-invariant self-similar
        exponent is the RATIO c_l / c_omega and the profile SHAPE."

    So the profile is a 2-parameter family and two conditions must be imposed.  Both are
    imposed HERE, and both are Chen's own conventions rather than free choices:

      (i)  the AMPLITUDE gauge, mode-dependent (see `mode` below);
      (ii) the DILATION gauge, `U_X(0) = 8/3`, which is Chen's `bar u_x(0) = 1/b^2` at
           `b = sqrt(3/8)` -- eq (2.8), p.5.  This is the bordered row `F_2`.

    Modes
    -----
    `mode="chen"`    -- Object A: `nu = 0`, amplitude gauge `c_omega = -1` (Chen (2.2)).
                        `c_l` is a genuine UNKNOWN, and the solver recovering `c_l = 1/3` at
                        `a = 1/2` is a second known-answer check on top of the residual.
    `mode="viscous"` -- Object B: `nu` fixed and nonzero.  `nu` BREAKS the amplitude gauge
                        (the dissipation term is linear where the rest is quadratic) and
                        breaks dilation too, but the COMBINATION `Omega -> mu^2 Omega(mu X)`,
                        `(c_l, c_omega) -> mu^2 (c_l, c_omega)` survives at fixed `nu`, so
                        exactly one gauge remains and `F_2` still pins it.  The amplitude
                        gauge slot is taken instead by the PHYSICAL requirement that makes
                        this a dissipative steady state at all: `c_omega + 2 c_l = 0`, forced
                        by Chen (2.7) -- `nu(t) = exp(int (c_omega + 2 c_l))`, so `nu(t)` is
                        constant iff that exponent vanishes.  Chen's own constants give
                        `-1 + 2/3 = -1/3`, which is the steady-side statement of "the
                        diffusion term is asymptotically small" (p.4).

    Unknowns are `z = (w, c_l)` with `w` the profile on `X > 0`; oddness is structural, so
    the residual at `X = 0` (identically zero for odd `Omega`) is never a spurious equation.
    """

    # THE BORDER CONSTANT, and the one that does NOT work.
    # `bar omega_x(0) = -2/b^3` at `b = sqrt(3/8)` -- Chen (2.2)/(2.8).  This is the
    # DILATION gauge and it is sensitive to it: under `Omega(X) -> Omega(mu X)` (with
    # `c_l, c_omega` held) the family is `Omega_b -> mu^{-2} Omega_{b/mu}`, so
    # `Omega_X(0) -> mu Omega_X(0)`.
    # `bar u_x(0) = 1/b^2 = 8/3` was tried first and is a TAUTOLOGY: along that same
    # family `U_X(0) = mu^{-2} * (b/mu)^{-2} = 1/b^2` identically, so bordering with it
    # pins nothing and the Jacobian stays singular.  Measured, n = 401: bordered
    # cond = 1.233e+07 against an unbordered sigma_max/sigma_min = 1.225e+07 -- i.e. the
    # border bought a factor 0.99.  Banked lesson 53/TC-5b in the flesh: a control that
    # returns the same number whatever you do to it is a tautology of the code, not a
    # measurement.  It is kept below as a REPORTED DIAGNOSTIC, never as the border.
    OMX0_TARGET = -2.0 / (3.0 / 8.0) ** 1.5      # = -8.709296863229080
    UX0_INVARIANT = 8.0 / 3.0                    # the tautology, reported not imposed

    def __init__(self, grid, a=0.5, nu=0.0, mode="chen", w_c=1.0,
                 omx0_target=OMX0_TARGET):
        if mode not in ("chen", "viscous"):
            raise ValueError("mode must be 'chen' or 'viscous'")
        if mode == "chen" and nu != 0.0:
            raise ValueError("mode='chen' IS Chen's inviscid steady equation (p.4); "
                             "nu != 0 there would misattribute the object")
        if mode == "viscous" and nu == 0.0:
            raise ValueError("mode='viscous' with nu = 0 is Object A under another name")
        self.g, self.a, self.nu, self.mode = grid, float(a), float(nu), mode
        self.w_c = float(w_c)               # border weight (a stated gauge, reported)
        self.omx0_target = float(omx0_target)
        m = grid.odd_mask()
        idx = np.where(m)[0]
        mir = grid.n - 1 - idx
        self.idx, self.mir, self.N = idx, mir, int(m.sum())
        # restriction of each operator to (odd input on X>0) -> (values on X>0)
        self._Hp = grid.H[np.ix_(idx, idx)] - grid.H[np.ix_(idx, mir)]
        self._Dp = grid.D[np.ix_(idx, idx)] - grid.D[np.ix_(idx, mir)]
        self._D2p = grid.D2[np.ix_(idx, idx)] - grid.D2[np.ix_(idx, mir)]
        self._Vp = grid.V[np.ix_(idx, idx)] - grid.V[np.ix_(idx, mir)]
        self._XDp = grid.XD[np.ix_(idx, idx)] - grid.XD[np.ix_(idx, mir)]
        self._h0 = grid.H[grid.i0, idx] - grid.H[grid.i0, mir]     # U_X(0) = h0 . w
        self._d0 = grid.D[grid.i0, idx] - grid.D[grid.i0, mir]     # Omega_X(0) = d0 . w
        self.Xp = grid.X[idx]

    # -- unknown packing ---------------------------------------------------
    def pack(self, w, c_l):
        return np.concatenate([np.asarray(w, dtype=float), [float(c_l)]])

    def unpack(self, z):
        return np.asarray(z[:self.N], dtype=float), float(z[self.N])

    def c_omega(self, c_l):
        """The amplitude-gauge slot: Chen's -1, or the diffusive-invariance constraint."""
        return -1.0 if self.mode == "chen" else -2.0 * float(c_l)

    def ux0(self, w):
        """U_X(0) -- the DIAGNOSTIC (invariant along the dilation family, so not a border)."""
        return float(self._h0 @ w)

    def omx0(self, w):
        """Omega_X(0) -- the quantity the border row actually pins."""
        return float(self._d0 @ w)

    # -- residual ----------------------------------------------------------
    def F(self, z):
        w, c_l = self.unpack(z)
        c_om = self.c_omega(c_l)
        Hw, Dw, U = self._Hp @ w, self._Dp @ w, self._Vp @ w
        r = (c_om + Hw) * w - (c_l * self.Xp + self.a * U) * Dw
        if self.nu != 0.0:
            r = r + self.nu * (self._D2p @ w)
        return np.concatenate([r, [self._d0 @ w - self.omx0_target]])

    def jacobian(self, z):
        """Exact analytic Jacobian.  F is degree 2 in z, so this is not an approximation."""
        w, c_l = self.unpack(z)
        c_om = self.c_omega(c_l)
        Hw, Dw, U = self._Hp @ w, self._Dp @ w, self._Vp @ w
        J = np.zeros((self.N + 1, self.N + 1))
        J[:self.N, :self.N] = (np.diag(c_om + Hw) + w[:, None] * self._Hp
                               - (c_l * self.Xp + self.a * U)[:, None] * self._Dp
                               - self.a * Dw[:, None] * self._Vp)
        if self.nu != 0.0:
            J[:self.N, :self.N] += self.nu * self._D2p
        # d/dc_l : the -c_l X Omega_X term always; plus d c_omega/d c_l = -2 in viscous mode
        J[:self.N, self.N] = -self.Xp * Dw
        if self.mode == "viscous":
            J[:self.N, self.N] += -2.0 * w
        J[self.N, :self.N] = self._d0
        return J

    # -- Newton ------------------------------------------------------------
    def newton(self, z0, tol=1e-12, max_iter=80, damping=True):
        """Damped Newton.  Returns (z, info) carrying the residual ladder, always.

        The line search is on the 2-NORM of F, not the sup norm.  That is not cosmetic:
        with a sup-norm criterion the full Newton step is rejected here on every iteration
        (a step that cuts the residual almost everywhere can still raise the single largest
        entry), the search collapses to lambda = 2^-12, and Newton crawls -- measured, at
        n = 201: the ladder went 2.948e-04 -> 2.912e-04 over five steps and was reported
        "stalled", while the SAME steps undamped reach 1.4e-12 in five and the float floor
        in six.  A solver that is 8 orders from its floor and says "stalled" is an
        instrument fault, not a finding about the equation.
        """
        z = np.array(z0, dtype=float)
        sup = lambda v: float(np.abs(v).max())
        two = lambda v: float(np.sqrt(np.sum(v * v)))
        ladder = [sup(self.F(z))]
        reason = "max_iter"
        for _ in range(max_iter):
            Fz = self.F(z)
            try:
                dz = np.linalg.solve(self.jacobian(z), -Fz)
            except np.linalg.LinAlgError:
                reason = "singular Jacobian"
                break
            lam, r0 = 1.0, two(Fz)
            if damping:
                while lam > 1.0 / 4096 and two(self.F(z + lam * dz)) >= r0:
                    lam *= 0.5
            z = z + lam * dz
            ladder.append(sup(self.F(z)))
            if ladder[-1] < tol:
                reason = "ok"
                break
            if len(ladder) >= 8 and ladder[-1] > 0.9 * ladder[-4]:
                reason = "stalled"
                break
        return z, {"residual_ladder": np.array(ladder),
                   "converged": bool(ladder[-1] < tol), "reason": reason}

    # -- the certificate constants ----------------------------------------
    def certificate_constants(self, z, s=0.0):
        """(Y_0, Z_1, Z_2) in the weighted sup norm, on the BORDERED system.

        Norm: `||(v, e)|| = max( max_j w_j |v_j| , w_c |e| )` with `w_j = (1+X_j^2)^{s/2}`
        and `w_c` the border weight -- the same shape of norm `solver/weight_search.py`
        uses for its bordered CLM system, re-read from that file rather than transferred.

        Convention, also re-read: `A = inv(J)`, `Y0 = max(w |A F|)`,
        `Z1 = max(w (|I - A J| 1/w))`, `Z2 = 2 ||A||_w B`.

        `F` is EXACTLY degree 2, so the Newton-Kantorovich remainder is exact:
            F_1(z+d) - F_1(z) - DF_1 d = (Hv) v - (e X + a (Vv)) (Dv)  [+ (-2 e v) in mode B]
            F_2(z+d) - F_2(z) - DF_2 d = 0                             (F_2 is linear)
        bounded term by term in the weighted sup norm:
            ||(Hv) v||_w        <= max(|H| 1/w) ||d||^2
            ||e X (Dv)||_w      <= (1/w_c) max(w (|XD| 1/w)) ||d||^2
            ||a (Vv)(Dv)||_w    <= |a| max(|V| 1/w) max(w (|D| 1/w)) ||d||^2
            ||2 e v||_w         <= (2/w_c) ||d||^2                      (mode B only)
        """
        wt = np.concatenate([(1.0 + self.Xp ** 2) ** (0.5 * s), [self.w_c]])
        J = self.jacobian(z)
        A = np.linalg.inv(J)
        Y0 = float(np.max(wt * np.abs(A @ self.F(z))))
        M = np.eye(self.N + 1) - A @ J
        Z1 = float(np.max(wt * (np.abs(M) @ (1.0 / wt))))
        A_norm = float(np.max(wt * (np.abs(A) @ (1.0 / wt))))
        wp = wt[:self.N]
        H_ni = float(np.max(np.abs(self._Hp) @ (1.0 / wp)))
        V_ni = float(np.max(np.abs(self._Vp) @ (1.0 / wp)))
        D_nn = float(np.max(wp * (np.abs(self._Dp) @ (1.0 / wp))))
        XD_nn = float(np.max(wp * (np.abs(self._XDp) @ (1.0 / wp))))
        B = H_ni + XD_nn / self.w_c + abs(self.a) * V_ni * D_nn
        if self.mode == "viscous":
            B += 2.0 / self.w_c
        Z2 = 2.0 * A_norm * B
        out = {"Y0": Y0, "Z1": Z1, "Z2": Z2, "A_norm": A_norm, "B": B,
               "H_norm": H_ni, "V_norm": V_ni, "D_norm": D_nn, "XD_norm": XD_nn,
               "s": float(s), "w_c": self.w_c, "budget": y0_budget(Z1, Z2)}
        out["Y0_over_budget"] = Y0 / out["budget"] if out["budget"] > 0 else np.inf
        out["under_budget"] = bool(Y0 < out["budget"])
        out["radii"] = radii_polynomial(Y0, Z1, Z2)
        return out

    def cond(self, z):
        """Condition number of the bordered Jacobian -- the number that catches a gauge
        that was NOT pinned (the unbordered version of this class had ~1e10 here)."""
        return float(np.linalg.cond(self.jacobian(z)))


# --------------------------------------------------------------------------
# (D) the measurements this leg's gate reads
# --------------------------------------------------------------------------
def chen_known_answer(n=401, a=0.5, c=0.5, rho_max=8.0):
    """KNOWN-ANSWER GATE: Chen's closed form (2.2) nulls Object A's residual.

    This is the only place in the whole leg where the answer is known independently of the
    solver, so it is what decides whether any other number here means anything.  Reports
    the residual sup norm at the EXACT profile, with Chen's own `c_l = 1/3` substituted --
    no solve involved.
    """
    g = Grid(n=n, c=c, rho_max=rho_max)
    prob = SteadyProfile(g, a=a, nu=0.0, mode="chen")
    Om, _, _ = chen_profile(g.X)
    w_exact = Om[prob.idx]
    z = prob.pack(w_exact, CHEN_1908_09385["profile_2_2"]["c_l"])
    R = prob.F(z)
    return {"n": g.n, "a": float(a), "Xmax": g.Xmax,
            "residual_sup": float(np.abs(R[:prob.N]).max()),
            "residual_rms": float(np.sqrt(np.mean(R[:prob.N] ** 2))),
            "border_residual": float(R[prob.N]),
            "profile_sup": float(np.abs(w_exact).max()),
            "ux0_numeric": prob.ux0(w_exact),
            "ux0_exact": CHEN_1908_09385["approximate_steady_state_2_8"]["ux0"],
            "ux0_rel_error": abs(prob.ux0(w_exact) - 8.0 / 3.0) / (8.0 / 3.0),
            "omx0_numeric": prob.omx0(w_exact), "omx0_target": prob.omx0_target,
            "cond_bordered_jacobian": prob.cond(z)}


def _measure(prob, g, z0, s, extra):
    """Shared tail of both measurements: Newton, then the constants, then the magnitudes."""
    z, info = prob.newton(z0)
    w, c_l = prob.unpack(z)
    cst = prob.certificate_constants(z, s=s)
    c_om = prob.c_omega(c_l)
    cst.update({
        "n": g.n, "a": prob.a, "nu": prob.nu, "mode": prob.mode, "Xmax": g.Xmax,
        "newton_converged": info["converged"], "newton_reason": info["reason"],
        "newton_steps": int(info["residual_ladder"].size - 1),
        "residual_ladder": [float(x) for x in info["residual_ladder"]],
        "final_residual_sup": float(info["residual_ladder"][-1]),
        "c_l": float(c_l), "c_omega": float(c_om),
        "c_l_over_c_omega": float(c_l / c_om) if c_om != 0 else float("nan"),
        "ux0": prob.ux0(w), "profile_sup": float(np.abs(w).max()),
        # U_X(0) is the DIAGNOSTIC that is invariant along the dilation family (so it can
        # never be the border); Omega_X(0) is what the border row actually pins.
        "ux0_invariant_reference": prob.UX0_INVARIANT,
        "omx0": prob.omx0(w), "omx0_target": prob.omx0_target,
        "cond_bordered_jacobian": prob.cond(z),
    })
    cst.update(extra(w, c_l))
    return cst


def measure_chen_object(n=401, a=0.5, s=0.0, c=0.5, rho_max=8.0, perturb=1e-3, seed=0):
    """Object A at resolution `n`: Newton from a PERTURBED exact profile, then Y_0.

    `perturb` seeds Newton away from the closed form so the solve is a real solve and not
    a fixed point of doing nothing (banked lesson: a control that cannot fail is not a
    control).  Two independent known answers are checked on the way out: the recovered
    profile against Chen's closed form, and the recovered `c_l` against his `1/3`.
    """
    g = Grid(n=n, c=c, rho_max=rho_max)
    prob = SteadyProfile(g, a=a, nu=0.0, mode="chen")
    Om, _, _ = chen_profile(g.X)
    exact = Om[prob.idx]
    w0 = exact.copy()
    if perturb:
        rng = np.random.default_rng(seed)
        w0 = w0 * (1.0 + perturb * rng.standard_normal(w0.size))
    z0 = prob.pack(w0, CHEN_1908_09385["profile_2_2"]["c_l"] * (1.0 + perturb))

    def extra(w, c_l):
        return {"perturb": float(perturb),
                "dist_to_closed_form_sup": float(np.abs(w - exact).max()),
                "dist_to_closed_form_rel": float(np.abs(w - exact).max()
                                                 / max(np.abs(exact).max(), 1e-300)),
                "c_l_exact": CHEN_1908_09385["profile_2_2"]["c_l"],
                "c_l_abs_error": abs(c_l - CHEN_1908_09385["profile_2_2"]["c_l"])}
    return _measure(prob, g, z0, s, extra)


def measure_viscous_object(n=401, a=0.5, nu=1.0, s=0.0, c=0.5, rho_max=8.0):
    """Object B at resolution `n`: does a gamma = 2 DISSIPATIVE steady profile exist?

    Seeded from Chen's inviscid closed form, which is the most favourable start available.
    Reports the residual ladder whatever it does -- a non-convergent ladder is a MEASUREMENT
    of how far a dissipative steady state is from existing near this seed, not a failure to
    report.  `nu` is FIXED, never swept: sweeping it against a margin is stage V as posed
    and is banned (and is vacuous anyway, LSS arXiv:2207.07548 sec 2).
    """
    g = Grid(n=n, c=c, rho_max=rho_max)
    prob = SteadyProfile(g, a=a, nu=nu, mode="viscous")
    Om, _, _ = chen_profile(g.X)
    exact = Om[prob.idx]
    z0 = prob.pack(exact.copy(), CHEN_1908_09385["profile_2_2"]["c_l"])

    def extra(w, c_l):
        return {"dist_to_chen_profile_sup": float(np.abs(w - exact).max()),
                "dist_to_chen_profile_rel": float(np.abs(w - exact).max()
                                                  / max(np.abs(exact).max(), 1e-300)),
                "diffusive_balance_residual": float(prob.c_omega(c_l) + 2.0 * c_l)}
    return _measure(prob, g, z0, s, extra)


def resolution_study(ns=(201, 401, 801), a=0.5, s=0.0, nu=1.0):
    """Both objects at every resolution in `ns`.  Magnitudes, never booleans."""
    return {
        "known_answer": [chen_known_answer(n=n, a=a) for n in ns],
        "chen": [measure_chen_object(n=n, a=a, s=s) for n in ns],
        "viscous": [measure_viscous_object(n=n, a=a, nu=nu, s=s) for n in ns],
    }
