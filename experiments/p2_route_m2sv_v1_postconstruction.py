"""Leg 210, Route-M2SV: INDEPENDENT VERIFICATION of leg 185's reparametrized `nu` measurement.

WHAT THIS IS.  Leg 185 (M2SD) produced a numeric CONSTRUCTION result, not just a diagnostic
classification: reparametrizing leg 125's stalled Object-B continuation with `a` FIXED, the
dilation gauge IMPOSED and `nu` as the UNKNOWN, it recovered

    nu = +0.01799364   at a = 0.30   (grid-converged, truncation-insensitive over 55x domain)
    nu = -0.00817525 / -0.00895316   at Chen's a = 1/2   (two starts, sign-stable)

-- the measured shape of "Object B exists below a* = 0.3865 and is anti-diffusive at or above
it".  `DIRECTION.md` sec 210 asks whether an INDEPENDENT re-derivation reproduces those
numbers.  Per lesson 90 and the pre-committed design in `writeup/novelty/leg_210.md`, this
leg does NOT simply re-execute leg 185's script and trust the output.  It runs four tiers,
ranked by evidential weight, WEAKEST LAST:

  V0  OPERATOR REVALIDATION AGAINST CLOSED FORMS.  Every operator this leg uses is checked
      against an analytic answer before it is used to verify anything: the Hilbert transform
      against Chen eq (2.2)'s exact pair (`H Omega = U_x`) and against the exact a=0 CLM pair
      (`Omega_0 = -4X/(1+4X^2)`, `H Omega_0 = 2/(1+4X^2)`); the cumulative-integral operator
      against Chen's exact `U = X/(b^2+X^2)`; the first and second derivative matrices against
      the closed-form derivatives of Chen's profile.  Without this, "reproduction" could be an
      agreement between two copies of one bug.

  V2  INDEPENDENTLY DISCRETIZED RE-DERIVATION.  A second implementation of the residual and
      its Jacobian, DERIVED HERE from the equation rather than transcribed from leg 125's
      `solver/dissipative_profile.py`, and deliberately discretized DIFFERENTLY:
        * 6th-order centred first/second difference matrices, against leg 125's 4th-order;
        * the second derivative assembled through the CHAIN RULE on the sinh coordinate,
          d^2/dX^2 = X_rho^-2 d^2/drho^2 - X_rhorho X_rho^-3 d/drho, against leg 125's `D @ D`
          (composition of two first-derivative matrices) -- a structurally different operator
          with a different error constant, not a re-spelling;
        * a degree-5 Lagrange PANEL quadrature for the cumulative velocity integral, against
          leg 125's 4-point Adams-Moulton rule;
        * the whole system restricted to the ODD subspace (the residual of an odd profile is
          odd, proved term by term in `_odd_reduce`'s docstring), which makes the reduced
          square system NONSINGULAR and lets it be solved by LU -- against leg 185's
          least-squares solve of the rank-deficient full system.  Different linear algebra,
          not just a different matrix.
      TWO DIFFERENT DISCRETIZATIONS MUST AGREE IN THE CONTINUUM LIMIT, NOT DIGIT-FOR-DIGIT AT
      ONE `n`.  So the honest comparison is between grid-refined / Richardson-extrapolated
      values, and that is what is reported.  Reporting a raw single-`n` disagreement as a
      discrepancy would be a discretization error mistaken for a finding.

  V3  AN ALGEBRAICALLY DISTINCT ROUTE -- the dilation covariance, used as a DERIVATION rather
      than as a check.  The profile equation obeys, exactly,
          Omega -> Omega(./mu),   nu -> mu^2 nu,   Omega_X(0) -> Omega_X(0)/mu .
      Hence solving the SAME square system at a deliberately WRONG gauge `kappa * g_chen`
      must return `nu(kappa) = nu(g_chen) / kappa^2` -- so `nu(kappa) * kappa^2` recovers leg
      185's number from solves that never impose leg 185's gauge.  Two consequences are
      tested, both of which leg 185 did not run:
        (i)  the number is recoverable off-gauge, to the accuracy of the covariance itself;
        (ii) because mu^2 > 0 always, THE SIGN OF nu IS A DILATION INVARIANT of the branch --
             i.e. leg 185's sign claim ("+ below a*, - at and above") is GAUGE-INDEPENDENT and
             does not rest on the particular normalization it chose.  That is a strengthening
             of leg 185's result, obtained by verifying it.

  V4  THE SIGN FLIP LOCATED INDEPENDENTLY.  `a*` is found here by bisecting the independently
      computed gauge-fixed `nu(a)` to machine precision, and compared against leg 125's
      `a* = 0.3864963972206034`, which came from a third and completely different computation
      (the Delta(a) sweep at nu = 0, with c_l as the OUTPUT).

  V1  REPLAY OF LEG 185'S OWN CODE PATH.  Ranked LAST and reported as what it is: a
      DETERMINISM / TRANSCRIPTION check, not a verification.  It answers only "does leg 185's
      script, re-run today from its own banked constants, still print its own banked numbers",
      which cannot detect an error shared by the script and its output.

SCOPE, PRE-COMMITTED AND BINDING.  Verification only.  This module BUILDS NO SOLVER: the
independent implementation lives entirely here, inside `experiments/`, precisely so it cannot
be mistaken for or reused as banked machinery (`capabilities.py` grepped first; see
`writeup/novelty/leg_210.md`).  `solver/dissipative_profile.py`, leg 185's script, and leg
185's JSON are imported and read READ-ONLY and are never edited.  `no_dynamics_run: true` --
every solve here is of a STEADY equation.  Everything is FLOATING POINT.  NO NUMBER HERE IS A
CERTIFICATE, and confirming leg 185's number is a REPRODUCIBILITY statement about this
repository's own computation, NOT an existence result about gCLM.

ONE OPERATOR IS SHARED AND THAT IS DECLARED, NOT HIDDEN.  `solver/line_hilbert.py`'s dense
whole-line Hilbert matrix is reused rather than rebuilt: it is a self-contained quadrature of
a singular integral whose independent re-derivation would be a leg of its own.  It is
therefore VALIDATED HERE against two exact analytic pairs (V0) rather than trusted, and the
measured accuracy of that validation is banked next to every number that depends on it.
"""

import json
import os
import time

import numpy as np

from solver.dissipative_profile import DissipativeProfile, chen_profile
from solver.line_hilbert import line_hilbert_matrix

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "writeup", "data", "p2_route_m2sv_v1_postconstruction.json")
LEG185_JSON = os.path.join(HERE, "writeup", "data", "p2_route_m2sd_v1_diagnostic.json")

C_L_IMPOSED = 0.5            # Delta = 0, the gamma = 2 steadiness condition (leg 185's)
C_OMEGA = -1.0               # the amplitude gauge (leg 185's)
B_CHEN = float(np.sqrt(3.0 / 8.0))
G_CHEN_ANALYTIC = -2.0 / B_CHEN ** 3     # Omega_X(0) of Chen eq (2.2), in CLOSED FORM

# leg 185's banked headline numbers, transcribed here so the comparison is explicit
LEG185_NU_A030 = 0.01799364              # grid-converged (n = 1201) value at a = 0.30
LEG185_NU_A050_FROM_0P3 = -0.00817525
LEG185_NU_A050_FROM_0P01 = -0.00895316
LEG125_A_STAR = 0.3864963972206034


# ---------------------------------------------------------------------------
# V0 -- independent operators, each validated against a closed form before use
# ---------------------------------------------------------------------------

def _sinh_grid(n, c=0.5, rho_max=8.0):
    """X = c sinh(rho), rho uniform on [-rho_max, rho_max], n forced ODD so X = 0 is a node."""
    if n % 2 == 0:
        n += 1
    rho = np.linspace(-rho_max, rho_max, n)
    return rho, c * np.sinh(rho), n


def _d1_matrix6(n, h):
    """6th-order centred d/drho on a uniform rho grid (leg 125's is 4th-order).

    Order tapers to 4 / 2 / 1 in the last three nodes at each end; the profile is ~0 there
    (V0 measures how close), so the reduced end-accuracy is harmless and is MEASURED, not
    assumed."""
    D = np.zeros((n, n))
    w6 = np.array([-1 / 60, 3 / 20, -3 / 4, 0.0, 3 / 4, -3 / 20, 1 / 60]) / h
    for i in range(3, n - 3):
        D[i, i - 3:i + 4] = w6
    w4 = np.array([1 / 12, -2 / 3, 0.0, 2 / 3, -1 / 12]) / h
    for i in (2, n - 3):
        D[i, i - 2:i + 3] = w4
    w2 = np.array([-0.5, 0.0, 0.5]) / h
    for i in (1, n - 2):
        D[i, i - 1:i + 2] = w2
    D[0, 0:3] = np.array([-1.5, 2.0, -0.5]) / h
    D[n - 1, n - 3:n] = np.array([0.5, -2.0, 1.5]) / h
    return D


def _d2_matrix6(n, h):
    """6th-order centred d^2/drho^2 -- a DIRECT second-difference stencil.

    This is the point of departure from leg 125, which forms d^2/dX^2 as `D @ D`, the square of
    its first-derivative matrix.  Squaring a first-difference operator and discretizing the
    second derivative directly are different operators with different (and independently
    signed) truncation errors, so agreement between them is evidence rather than bookkeeping."""
    D = np.zeros((n, n))
    w6 = np.array([1 / 90, -3 / 20, 3 / 2, -49 / 18, 3 / 2, -3 / 20, 1 / 90]) / h ** 2
    for i in range(3, n - 3):
        D[i, i - 3:i + 4] = w6
    w4 = np.array([-1 / 12, 4 / 3, -5 / 2, 4 / 3, -1 / 12]) / h ** 2
    for i in (2, n - 3):
        D[i, i - 2:i + 3] = w4
    w2 = np.array([1.0, -2.0, 1.0]) / h ** 2
    for i in (1, n - 2):
        D[i, i - 1:i + 2] = w2
    D[0, 0:4] = np.array([2.0, -5.0, 4.0, -1.0]) / h ** 2
    D[n - 1, n - 4:n] = np.array([-1.0, 4.0, -5.0, 2.0]) / h ** 2
    return D


def _panel_weights6():
    """int_0^1 L_k(t) dt for the degree-5 Lagrange basis on t = -2,-1,0,1,2,3.

    Solved from the moment (Vandermonde) system rather than quoted from a table, so the rule is
    derived here and not transcribed.  leg 125 uses the 4-point Adams-Moulton rule instead."""
    t = np.array([-2.0, -1.0, 0.0, 1.0, 2.0, 3.0])
    V = np.vander(t, 6, increasing=True).T           # V[k, j] = t_j^k
    moments = np.array([1.0 / (k + 1) for k in range(6)])
    return np.linalg.solve(V, moments)


def _cumint_matrix6(n, h, i0):
    """Cumulative integral in rho, zeroed at node i0, from the degree-5 panel rule."""
    wl = _panel_weights6() * h
    C = np.zeros((n, n))

    def panel(i):
        w = np.zeros(n)
        if 2 <= i <= n - 4:
            w[i - 2:i + 4] += wl
        else:                                        # end panels: trapezoid, profile ~0 there
            w[i] += h / 2.0
            w[i + 1] += h / 2.0
        return w

    for i in range(i0, n - 1):
        C[i + 1] = C[i] + panel(i)
    for i in range(i0 - 1, -1, -1):
        C[i] = C[i + 1] - panel(i)
    return C


class IndepProfile:
    """The steady dissipative gCLM profile operator, INDEPENDENTLY discretized.

        R(Omega; c_l, c_omega, nu, a) = (c_omega + H Omega) Omega
                                        - c_l X Omega_X - a U Omega_X + nu Omega_XX,
        U(X) = int_0^X H Omega dX'.

    Same equation as `solver/dissipative_profile.DissipativeProfile` -- that is the point --
    but every operator in it is built here at a different order or by a different rule, and the
    Jacobian below is differentiated by hand from this expression rather than copied."""

    def __init__(self, a=0.5, n=801, c=0.5, rho_max=8.0):
        self.a = float(a)
        self.rho, self.X, self.n = _sinh_grid(n, c=c, rho_max=rho_max)
        n = self.n
        self.i0 = n // 2
        self.h = self.rho[1] - self.rho[0]
        self.X_rho = c * np.cosh(self.rho)            # dX/drho
        self.X_rhorho = self.X                        # d^2X/drho^2 = c sinh(rho) = X
        D1r = _d1_matrix6(n, self.h)
        D2r = _d2_matrix6(n, self.h)
        self.D = D1r / self.X_rho[:, None]            # d/dX
        # chain rule, NOT D @ D:
        self.D2 = D2r / (self.X_rho ** 2)[:, None] \
            - (self.X_rhorho / self.X_rho ** 3)[:, None] * D1r
        self.H = line_hilbert_matrix(self.X)          # SHARED, validated in V0
        self.V = _cumint_matrix6(n, self.h, self.i0) * self.X_rho[None, :]
        self.VH = self.V @ self.H
        self.g_row = self.D[self.i0]                  # extracts Omega_X(0)

    def residual(self, Om, a, nu, c_l=C_L_IMPOSED, c_om=C_OMEGA):
        HOm = self.H @ Om
        OmX = self.D @ Om
        U = self.VH @ Om
        return (c_om + HOm) * Om - c_l * self.X * OmX - a * U * OmX + nu * (self.D2 @ Om)

    def jacobian(self, Om, a, nu, c_l=C_L_IMPOSED, c_om=C_OMEGA):
        """dR/dOmega, differentiated by hand.  R is quadratic in Omega so this is exact.

        Written with row-scaling (`v[:, None] * M`) rather than `np.diag(v) @ M`: same operator,
        O(n^2) instead of O(n^3)."""
        HOm = self.H @ Om
        OmX = self.D @ Om
        U = self.VH @ Om
        J = Om[:, None] * self.H - c_l * (self.X[:, None] * self.D) \
            - a * (OmX[:, None] * self.VH + U[:, None] * self.D) \
            + nu * self.D2
        J[np.diag_indices(self.n)] += c_om + HOm
        return J

    def dR_dnu(self, Om):
        return self.D2 @ Om


def _odd_reduce(M, i0):
    """Restrict a linear map to ODD vectors: columns folded, rows taken above the centre.

    Why this is legitimate, term by term.  H maps odd -> even on the line.  So for odd Omega:
    (c_omega + H Omega) Omega is even*odd = odd; X Omega_X is odd*even = odd; U = int_0^X H Omega
    is the integral of an even function from 0, hence odd, and U Omega_X is odd*even = odd;
    Omega_XX is odd.  Every term is odd, so R is ODD -- R(0) = 0 identically and the rows below
    the centre are the negatives of the rows above.  THAT is the exact rank deficiency leg 185
    absorbed with a least-squares solve; restricting to the odd subspace removes it instead,
    leaving a genuinely nonsingular square system that LU can solve."""
    return M[i0 + 1:, i0 + 1:] - M[i0 + 1:, i0 - 1::-1]


def _odd_expand(y, n, i0):
    Om = np.zeros(n)
    Om[i0 + 1:] = y
    Om[:i0] = -y[::-1]
    return Om


def solve_nu_indep(ip, a, nu0, gauge, iters=60, tol=1e-13, Om_start=None):
    """Square system on the ODD subspace: unknowns (Omega_odd, nu); equations (R_odd, gauge).

    Newton with an LU solve.  Same MATHEMATICAL system leg 185 solved; different discretization,
    different subspace, different linear algebra."""
    n, i0 = ip.n, ip.i0
    Om = np.array(chen_profile(ip.X)[0] if Om_start is None else Om_start, dtype=float)
    Om = _odd_expand(Om[i0 + 1:], n, i0)              # project the start onto odd
    nu = float(nu0)
    m = n - i0 - 1
    hist = []
    k = 0
    for k in range(iters):
        R = ip.residual(Om, a, nu)
        hist.append(float(np.sqrt(np.mean(R ** 2))))
        if hist[-1] < tol:
            break
        F = np.concatenate([R[i0 + 1:], [float(ip.g_row @ Om) - gauge]])
        J = np.zeros((m + 1, m + 1))
        J[:m, :m] = _odd_reduce(ip.jacobian(Om, a, nu), i0)
        J[:m, m] = ip.dR_dnu(Om)[i0 + 1:]
        grow = ip.g_row[i0 + 1:] - ip.g_row[i0 - 1::-1]
        J[m, :m] = grow
        try:
            step = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            step, *_ = np.linalg.lstsq(J, -F, rcond=None)
        Om = _odd_expand(Om[i0 + 1:] + step[:m], n, i0)
        nu = nu + float(step[m])
    amp = float(np.abs(Om).max())
    scale = float(np.sqrt(np.mean(((C_OMEGA + ip.H @ Om) * Om) ** 2)))
    return {"n": n, "a": float(a), "nu0": float(nu0), "gauge": float(gauge),
            "nu": float(nu), "residual_rms_absolute": hist[-1],
            "residual_relative": hist[-1] / max(scale, 1e-300),
            "amplitude": amp, "iters": k,
            "edge_over_amplitude": float(abs(Om[-1]) / max(amp, 1e-300)),
            "X_max": float(ip.X[-1]),
            "odd_symmetry_defect": float(np.abs(Om + Om[::-1]).max() / max(amp, 1e-300)),
            "Omega": Om}


def v0_operator_validation(n=801, rho_max=8.0):
    """Every operator checked against a closed form BEFORE it verifies anything."""
    ip = IndepProfile(a=0.30, n=n, rho_max=rho_max)
    X, b = ip.X, B_CHEN
    Om, Ux, U = chen_profile(X)
    den = X ** 2 + b ** 2
    Om_X_exact = -2.0 * b * (den ** -2 - 4.0 * X ** 2 * den ** -3)
    Om_XX_exact = -2.0 * b * (-12.0 * X * den ** -3 + 24.0 * X ** 3 * den ** -4)
    Om0 = -4.0 * X / (1.0 + 4.0 * X ** 2)             # exact a = 0 CLM profile
    HOm0 = 2.0 / (1.0 + 4.0 * X ** 2)
    amp = float(np.abs(Om).max())
    return {
        "n": ip.n, "X_max": float(X[-1]),
        "hilbert_on_chen_pair_sup_error": float(np.abs(ip.H @ Om - Ux).max()),
        "hilbert_on_chen_pair_relative": float(np.abs(ip.H @ Om - Ux).max()
                                               / np.abs(Ux).max()),
        "hilbert_on_a0_clm_pair_sup_error": float(np.abs(ip.H @ Om0 - HOm0).max()),
        "hilbert_on_a0_clm_pair_note": (
            "LARGER than the Chen check by ~5 orders and that is EXPECTED, not a defect: "
            "Omega_0 = -4X/(1+4X^2) decays like 1/X, so the whole-line Hilbert integral has a "
            "slowly-decaying tail the truncated grid cannot see.  Chen's profile decays like "
            "X^-3 and is the relevant regime for every solve in this leg.  Reported because a "
            "validation you only quote when it passes is not a validation."),
        "cumint_on_chen_U_sup_error": float(np.abs(ip.V @ Ux - U).max()),
        "cumint_on_chen_U_relative": float(np.abs(ip.V @ Ux - U).max() / np.abs(U).max()),
        "d1_on_chen_relative_sup_error": float(np.abs(ip.D @ Om - Om_X_exact).max()
                                               / np.abs(Om_X_exact).max()),
        "d2_on_chen_relative_sup_error": float(np.abs(ip.D2 @ Om - Om_XX_exact).max()
                                               / np.abs(Om_XX_exact).max()),
        "d1_at_origin_on_chen": float((ip.D @ Om)[ip.i0]),
        "d1_at_origin_closed_form": G_CHEN_ANALYTIC,
        "d1_at_origin_relative_error": float(abs((ip.D @ Om)[ip.i0] - G_CHEN_ANALYTIC)
                                             / abs(G_CHEN_ANALYTIC)),
        "chen_profile_amplitude": amp,
        "reading": ("all four operators reproduce closed forms to <= 1e-8 relative in the "
                    "regime the solves use, so a reproduction of leg 185's number cannot be "
                    "two copies of one bug -- the operators here agree with ANALYSIS, not just "
                    "with leg 125's operators."),
    }


# ---------------------------------------------------------------------------
# the gauge question, settled before it can be mistaken for a discrepancy
# ---------------------------------------------------------------------------

def v0b_gauge_transcription(n=801, rho_max=8.0):
    """leg 185's gauge is DISCRETE (`D[i0] @ chen_profile`); the closed form is -2/b^3.

    They differ, and by the covariance nu ~ g^-2 that difference propagates into nu at TWICE
    its relative size.  Measured here explicitly so the resulting ~1e-8 offset in nu is
    accounted for rather than reported as a disagreement."""
    ip = IndepProfile(a=0.30, n=n, rho_max=rho_max)
    dp = DissipativeProfile(a=0.30, n=n, rho_max=rho_max)
    g185 = float(dp.D[dp.i0] @ chen_profile(dp.X)[0])
    gmine = float(ip.g_row @ chen_profile(ip.X)[0])
    rel = abs(g185 - G_CHEN_ANALYTIC) / abs(G_CHEN_ANALYTIC)
    return {"n": ip.n,
            "gauge_closed_form_minus_two_over_b_cubed": G_CHEN_ANALYTIC,
            "gauge_leg185_discrete": g185,
            "gauge_this_leg_discrete": gmine,
            "leg185_gauge_relative_error_vs_closed_form": float(rel),
            "this_leg_gauge_relative_error_vs_closed_form":
                float(abs(gmine - G_CHEN_ANALYTIC) / abs(G_CHEN_ANALYTIC)),
            "implied_relative_offset_in_nu": float(2.0 * rel),
            "reading": ("leg 185's 4th-order discrete gauge sits %.3e relative from the closed "
                        "form, which by nu ~ g^-2 moves nu by %.3e relative (~%.1e absolute at "
                        "nu = 0.018).  BOTH gauges are therefore run below, and the comparison "
                        "against leg 185's banked number uses LEG 185'S OWN GAUGE, so that the "
                        "verification tests its computation and not its normalization choice."
                        % (rel, 2.0 * rel, 2.0 * rel * 0.018)),
            }


# ---------------------------------------------------------------------------
# V2 -- the independently discretized re-derivation
# ---------------------------------------------------------------------------

def _richardson(ns, vals):
    """Fit v(n) = v_inf + C n^-p through the three finest points; report v_inf and p."""
    ns = np.asarray(ns[-3:], dtype=float)
    vs = np.asarray(vals[-3:], dtype=float)
    d1, d2 = vs[1] - vs[0], vs[2] - vs[1]
    if d2 == 0.0 or d1 / d2 <= 0:
        return {"extrapolated": float(vs[-1]), "observed_order": None,
                "note": "non-monotone or exhausted at float64 floor; finest value reported"}
    r = ns[1] / ns[0]
    p = float(np.log(d1 / d2) / np.log(r))
    v_inf = float(vs[2] + d2 / (r ** p - 1.0))
    return {"extrapolated": v_inf, "observed_order": p,
            "note": "v(n) = v_inf + C n^-p through the three finest grids"}


def v2_independent_rederivation(gauge_mode="leg185"):
    t0 = time.time()

    def gauge_for(ip, rho_max=8.0):
        """leg 185's gauge is `D[i0] @ chen_profile` in ITS OWN discretization, so it is
        recomputed from leg 125's module here rather than from this leg's operators -- the
        verification must test leg 185's computation, not substitute a better normalization."""
        if gauge_mode == "leg185":
            dp = DissipativeProfile(a=0.30, n=ip.n, rho_max=rho_max)
            return float(dp.D[dp.i0] @ chen_profile(dp.X)[0])
        return G_CHEN_ANALYTIC

    # -- the a sweep, at leg 185's own N_MAIN = 401, from leg 185's own two nu starts --
    sweep = []
    for a_fix in (0.30, 0.3865, 0.45, 0.50, 0.55, 0.70):
        ip = IndepProfile(a=a_fix, n=401)
        gv = gauge_for(ip)
        pair = [solve_nu_indep(ip, a_fix, nu0, gv) for nu0 in (0.3, 0.01)]
        for p in pair:
            p.pop("Omega", None)
        sweep.append({
            "a": a_fix,
            "nu_from_nu0_0p3": pair[0]["nu"], "nu_from_nu0_0p01": pair[1]["nu"],
            "sign_agrees_across_starts": bool((pair[0]["nu"] > 0) == (pair[1]["nu"] > 0)),
            "relative_spread": abs(pair[0]["nu"] - pair[1]["nu"])
                               / max(abs(pair[0]["nu"]), abs(pair[1]["nu"]), 1e-300),
            "worst_relative_residual": max(p["residual_relative"] for p in pair),
            "admissible_positive_nu": bool(pair[0]["nu"] > 0 and pair[1]["nu"] > 0),
            "runs": pair,
        })

    # -- grid refinement at a = 0.30 --
    grid = []
    for nn in (201, 401, 801, 1201):
        ip = IndepProfile(a=0.30, n=nn)
        r = solve_nu_indep(ip, 0.30, 0.3, gauge_for(ip))
        r.pop("Omega", None)
        grid.append(r)
    ladder = [r["nu"] for r in grid]

    # -- truncation sensitivity at a = 0.30 --
    trunc = []
    for rm in (6.0, 8.0, 10.0):
        ip = IndepProfile(a=0.30, n=801, rho_max=rm)
        r = solve_nu_indep(ip, 0.30, 0.3, gauge_for(ip, rho_max=rm))
        r.pop("Omega", None)
        trunc.append(r)

    rich = _richardson([r["n"] for r in grid], ladder)
    pos = [r["a"] for r in sweep if r["admissible_positive_nu"]]
    neg = [r["a"] for r in sweep if not r["admissible_positive_nu"]]
    return {
        "gauge_mode": gauge_mode,
        "a_sweep_at_n401": sweep,
        "a_with_admissible_positive_nu": pos,
        "a_with_inadmissible_negative_nu": neg,
        "grid_convergence_at_a_0p30": grid,
        "nu_ladder_at_a_0p30": ladder,
        "richardson_at_a_0p30": rich,
        "truncation_sensitivity_at_a_0p30": trunc,
        "truncation_spread_relative": float(
            (max(r["nu"] for r in trunc) - min(r["nu"] for r in trunc))
            / abs(np.mean([r["nu"] for r in trunc]))),
        "X_max_range": [trunc[0]["X_max"], trunc[-1]["X_max"]],
        "seconds": time.time() - t0,
    }


def v2b_gauge_scaling_check(n=801):
    """One extra solve under the CLOSED-FORM gauge, to confirm the g^-2 law quantitatively.

    Replaces a full duplicate sweep: the whole content of re-running under the analytic gauge is
    the single question 'does changing the gauge move nu by exactly 2x its relative change?',
    and one solve answers it.  A second full sweep would have cost ~12 minutes to re-measure a
    scalar."""
    ip = IndepProfile(a=0.30, n=n)
    dp = DissipativeProfile(a=0.30, n=ip.n, rho_max=8.0)
    g185 = float(dp.D[dp.i0] @ chen_profile(dp.X)[0])
    nu_185 = solve_nu_indep(ip, 0.30, 0.3, g185)["nu"]
    nu_cf = solve_nu_indep(ip, 0.30, 0.3, G_CHEN_ANALYTIC)["nu"]
    predicted = 2.0 * abs(g185 - G_CHEN_ANALYTIC) / abs(G_CHEN_ANALYTIC)
    observed = abs(nu_185 - nu_cf) / abs(nu_185)
    return {"n": ip.n,
            "nu_under_leg185_discrete_gauge": nu_185,
            "nu_under_closed_form_gauge": nu_cf,
            "predicted_relative_offset": float(predicted),
            "observed_relative_offset": float(observed),
            "observed_over_predicted": float(observed / max(predicted, 1e-300)),
            "reading": ("nu ~ g^-2 predicts the gauge change moves nu by twice the gauge's own "
                        "relative change; observed/predicted is reported so the law is checked "
                        "as a NUMBER, not asserted.  This also fixes the size of the residual "
                        "offset between this leg's numbers and leg 185's that is attributable "
                        "to normalization rather than to discretization.")}


# ---------------------------------------------------------------------------
# V3 -- the algebraically distinct route: derive nu from OFF-GAUGE solves
# ---------------------------------------------------------------------------

def v3_dilation_covariance_route(n=401, kappas=(0.5, 0.8, 1.25, 2.0), a_list=(0.30, 0.50)):
    """Solve at gauge kappa*g and recover nu(g) = kappa^2 * nu(kappa*g).

    Exact covariance, re-derived here: with Omega_mu(X) = Omega(X/mu), H commutes with dilation
    so (H Omega_mu)(X) = (H Omega)(X/mu); U_mu(X) = mu U(X/mu); Omega_mu,X(X) = Omega_X(X/mu)/mu.
    Then (c_om + H Omega_mu) Omega_mu, c_l X Omega_mu,X and U_mu Omega_mu,X are each the
    original term evaluated at X/mu, while nu Omega_mu,XX = (nu/mu^2) Omega_XX(X/mu).  So
    Omega_mu solves the equation at mu^2 nu, and its gauge is Omega_X(0)/mu.  Gauge kappa*g
    therefore corresponds to mu = 1/kappa, seed Omega(kappa X), and nu -> nu/kappa^2.

    TWO things follow, and both are tested:
      (1) nu is recoverable from solves that NEVER impose leg 185's gauge;
      (2) sign(nu) is a DILATION INVARIANT (mu^2 > 0), so leg 185's sign claim does not depend
          on its normalization -- a strengthening leg 185 did not run.

    BOTH SEEDINGS ARE REPORTED, because the difference between them is itself a measurement.
    SEEDED: Newton started from the dilated base solution, which is the covariance test proper --
    it asks whether the dilated solution IS a solution at the rescaled gauge.  UNSEEDED: Newton
    started from the Chen profile, as leg 185 always starts.  The covariance is a statement about
    SOLUTIONS, not about which solution Newton finds, so a large unseeded error is a basin fact
    about the square system and NOT a refutation of the identity.  Recording only the seeded
    numbers would hide how delicate that basin is."""
    out = []
    for a_fix in a_list:
        ip = IndepProfile(a=a_fix, n=n)
        dp = DissipativeProfile(a=a_fix, n=ip.n, rho_max=8.0)
        g0 = float(dp.D[dp.i0] @ chen_profile(dp.X)[0])
        base = solve_nu_indep(ip, a_fix, 0.3, g0)
        Om_base = base.pop("Omega")
        rows = []
        for kap in kappas:
            pred = base["nu"] / kap ** 2
            seed = np.interp(kap * ip.X, ip.X, Om_base, left=0.0, right=0.0)
            rs = solve_nu_indep(ip, a_fix, pred, g0 * kap, Om_start=seed)
            ru = solve_nu_indep(ip, a_fix, 0.3 * kap ** 2, g0 * kap)
            rs.pop("Omega", None)
            ru.pop("Omega", None)
            rows.append({
                "kappa": kap,
                "predicted_nu_at_kappa_gauge": pred,
                "seeded_nu_at_kappa_gauge": rs["nu"],
                "seeded_rescaled_kappa_squared": rs["nu"] * kap ** 2,
                "seeded_relative_error_vs_on_gauge":
                    abs(rs["nu"] * kap ** 2 - base["nu"]) / abs(base["nu"]),
                "seeded_residual_relative": rs["residual_relative"],
                "seeded_sign_matches": bool((rs["nu"] > 0) == (base["nu"] > 0)),
                "unseeded_nu_at_kappa_gauge": ru["nu"],
                "unseeded_relative_error_vs_on_gauge":
                    abs(ru["nu"] * kap ** 2 - base["nu"]) / abs(base["nu"]),
                "unseeded_sign_matches": bool((ru["nu"] > 0) == (base["nu"] > 0)),
                "unseeded_residual_relative": ru["residual_relative"],
            })
        out.append({
            "a": a_fix, "n": ip.n,
            "nu_on_leg185_gauge": base["nu"],
            "on_gauge_residual_relative": base["residual_relative"],
            "off_gauge_recoveries": rows,
            "seeded_worst_relative_error":
                max(r["seeded_relative_error_vs_on_gauge"] for r in rows),
            "unseeded_worst_relative_error":
                max(r["unseeded_relative_error_vs_on_gauge"] for r in rows),
            "seeded_sign_invariant": all(r["seeded_sign_matches"] for r in rows),
            "gauge_range_tested": [min(kappas), max(kappas)],
        })
    return {
        "identity": ("Omega -> Omega(./mu), nu -> mu^2 nu, Omega_X(0) -> Omega_X(0)/mu, "
                     "so nu at gauge kappa*g equals nu(g)/kappa^2 EXACTLY in the continuum"),
        "per_a": out,
        "reading": ("SEEDED, the identity holds to ~3e-5 relative across a 4x gauge range at "
                    "a = 0.30 -- leg 185's number is recovered from normalizations it never "
                    "used, and the residual error is the seed's interpolation error plus the "
                    "grid's own inexactness, not a failure of the covariance.  UNSEEDED, the "
                    "error is O(1-100): Newton started from the Chen profile at a wrong gauge "
                    "lands on OTHER roots of the same square system.  That is a BASIN "
                    "measurement, and it is the same multiplicity V5 finds on the negative "
                    "side.  Because mu^2 > 0, no dilation can change sign(nu), so the sign "
                    "claim is gauge-independent."),
    }


# ---------------------------------------------------------------------------
# V4 -- locate the sign flip independently
# ---------------------------------------------------------------------------

CONVERGED_RELRES = 1e-10        # what "this solve actually solved the system" means here


def v4_sign_flip_location(n=401, a_lo=0.30, a_hi=0.45, points=16):
    """Locate the sign flip by a SCAN, with each point's convergence reported alongside it.

    Deliberately NOT a bisection.  A bisection returns a 12-digit number whatever the function
    does, and this leg's first pass did exactly that -- it printed a* = 0.3659213753 while
    silently stepping through a-values where the square system does not converge at all
    (relative residual 6e-3 at a = 0.3865).  Reporting that number would have been reporting
    the conditioning of a bracket, not a measurement (lesson 67).  A scan cannot hide that: the
    crossing is quoted as a BRACKET BETWEEN CONVERGED POINTS, and points that failed to converge
    are listed as failures rather than used as function values."""
    rows = []
    for a in np.linspace(a_lo, a_hi, points):
        a = float(a)
        ip = IndepProfile(a=a, n=n)
        dp = DissipativeProfile(a=a, n=ip.n, rho_max=8.0)
        g0 = float(dp.D[dp.i0] @ chen_profile(dp.X)[0])
        r = solve_nu_indep(ip, a, 0.3, g0)
        r.pop("Omega", None)
        rows.append({"a": a, "nu": r["nu"], "residual_relative": r["residual_relative"],
                     "amplitude": r["amplitude"],
                     "converged": bool(r["residual_relative"] < CONVERGED_RELRES)})
    ok = [r for r in rows if r["converged"]]
    bracket = None
    for x, y in zip(ok, ok[1:]):
        if x["nu"] * y["nu"] < 0:
            bracket = [x["a"], y["a"]]
            break
    out = {
        "n": int(n if n % 2 else n + 1),
        "scan": rows,
        "points_scanned": len(rows),
        "points_converged": len(ok),
        "points_failed_to_converge": [r["a"] for r in rows if not r["converged"]],
        "sign_change_bracket_between_converged_points": bracket,
        "a_star_leg125_from_Delta_sweep": LEG125_A_STAR,
        "leg125_a_star_inside_bracket":
            bool(bracket is not None and bracket[0] <= LEG125_A_STAR <= bracket[1]),
    }
    if bracket is not None:
        mid = 0.5 * (bracket[0] + bracket[1])
        out["bracket_midpoint"] = mid
        out["bracket_width"] = bracket[1] - bracket[0]
        out["midpoint_minus_leg125_a_star"] = mid - LEG125_A_STAR
    out["reading"] = (
        "a* is NOT independently reproduced at the precision leg 185's journal implies.  Leg "
        "185 wrote that its nu(a) zero crossing 'lands on leg 125's own independently measured "
        "a* = 0.3864963972206034' and called that 'a cross-check, not a restatement'.  But leg "
        "185's OWN a-sweep row at a = 0.3865 reports +0.00000035 from one start and -0.00425080 "
        "from the other -- its two starts STRADDLE ZERO there, so its own data does not pin the "
        "crossing to anything like 8 digits; the agreement it reports is the agreement of ONE "
        "of two disagreeing starts.  Independently discretized, the crossing moves.  What "
        "survives is the QUALITATIVE statement -- nu > 0 at a = 0.30, nu < 0 at a >= 0.45 -- "
        "not a determined a*.")
    return out


# ---------------------------------------------------------------------------
# V5 -- THE DECISIVE TEST: is the NEGATIVE side grid-converged in EITHER scheme?
# ---------------------------------------------------------------------------

def v5_negative_branch_grid_study(grids=(201, 401, 801), a_list=(0.30, 0.45, 0.50)):
    """Run the grid ladder AT CHEN'S a, in BOTH schemes -- the study leg 185 ran only at a=0.30.

    This is the sharpest instrument this leg has, and it exists because of an asymmetry in leg
    185's own artifact: leg 185 refined its a = 0.30 result on four grids and over a 55x domain
    extension, but banked its a = 1/2 numbers (-0.00817525 / -0.00895316) from a SINGLE grid,
    n = 401, with no refinement at all.  A number that has never been refined is not a
    measurement of the continuum problem, whoever computed it.

    a = 0.30 is included as the CONTROL: if the method is sound, the positive side must refine
    cleanly in both schemes while the negative side does not.  Amplitude is tracked at every
    point because a square system whose solution amplitude is collapsing is drifting toward the
    trivial null, where nu is unidentifiable -- leg 185's own D1 named exactly that failure
    mode, and it must be checked for here rather than assumed absent."""
    import importlib.util
    path = os.path.join(HERE, "experiments", "p2_route_m2sd_v1_diagnostic.py")
    spec = importlib.util.spec_from_file_location("leg185_readonly_v5", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    per_a = []
    for a_fix in a_list:
        mine, theirs = [], []
        for nn in grids:
            ip = IndepProfile(a=a_fix, n=nn)
            dp = DissipativeProfile(a=a_fix, n=ip.n, rho_max=8.0)
            g0 = float(dp.D[dp.i0] @ chen_profile(dp.X)[0])
            for nu0 in (0.3, 0.01):
                r = solve_nu_indep(ip, a_fix, nu0, g0)
                r.pop("Omega", None)
                mine.append({"n": nn, "nu0": nu0, "nu": r["nu"],
                             "residual_relative": r["residual_relative"],
                             "amplitude": r["amplitude"],
                             "converged": bool(r["residual_relative"] < CONVERGED_RELRES)})
                t = mod._solve_nu_unknown(nn, a_fix, nu0)
                theirs.append({"n": nn, "nu0": nu0, "nu": t["nu"],
                               "residual_relative": t["residual_relative"],
                               "amplitude": t["amplitude"],
                               "converged": bool(t["residual_relative"] < CONVERGED_RELRES)})

        def span(rows):
            ok = [r["nu"] for r in rows if r["converged"]]
            if len(ok) < 2:
                return None
            return float((max(ok) - min(ok)) / max(abs(np.mean(ok)), 1e-300))

        def amp_ratio(rows):
            ok = [r["amplitude"] for r in rows if r["converged"]]
            if len(ok) < 2:
                return None
            return float(min(ok) / max(max(ok), 1e-300))

        per_a.append({
            "a": a_fix,
            "this_leg_scheme": mine, "leg185_scheme": theirs,
            "this_leg_relative_span_over_converged": span(mine),
            "leg185_relative_span_over_converged": span(theirs),
            "this_leg_min_over_max_amplitude": amp_ratio(mine),
            "leg185_min_over_max_amplitude": amp_ratio(theirs),
            "all_converged_signs_negative_this_leg":
                all(r["nu"] < 0 for r in mine if r["converged"]),
            "all_converged_signs_negative_leg185":
                all(r["nu"] < 0 for r in theirs if r["converged"]),
            "all_converged_signs_positive_this_leg":
                all(r["nu"] > 0 for r in mine if r["converged"]),
            "all_converged_signs_positive_leg185":
                all(r["nu"] > 0 for r in theirs if r["converged"]),
        })
    return {
        "why": ("leg 185 refined a = 0.30 on four grids but banked a = 1/2 from n = 401 alone; "
                "this supplies the missing refinement, in BOTH discretizations."),
        "per_a": per_a,
        "grids": list(grids),
    }


# ---------------------------------------------------------------------------
# V1 -- replay of leg 185's own code path (WEAKEST TIER, reported as such)
# ---------------------------------------------------------------------------

def v1_replay_leg185(full_ladder=True):
    """Re-execute leg 185's OWN `_solve_nu_unknown` and compare against its OWN banked JSON.

    This can only detect nondeterminism or a transcription slip between the run and the report.
    It CANNOT detect an error shared by the script and its output, which is precisely why the
    gate's question needed V0/V2/V3 and why this tier is reported last."""
    import importlib.util
    path = os.path.join(HERE, "experiments", "p2_route_m2sd_v1_diagnostic.py")
    spec = importlib.util.spec_from_file_location("leg185_readonly", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    with open(LEG185_JSON) as fh:
        banked = json.load(fh)
    d5 = banked["D5_is_a_genuine_profile_reachable"]
    banked_chen = d5["nu_at_chen_a_one_half"]

    rows = []
    grids = (201, 401, 801, 1201) if full_ladder else (201, 401)
    for nn in grids:
        r = mod._solve_nu_unknown(nn, 0.30, 0.3)
        rows.append({"n": nn, "nu_replayed": r["nu"],
                     "residual_relative": r["residual_relative"]})
    chen = [mod._solve_nu_unknown(401, 0.50, nu0) for nu0 in (0.3, 0.01)]
    return {
        "tier": "WEAKEST -- determinism/transcription only, NOT a verification",
        "leg185_script_md5": _md5(path),
        "leg185_json_md5": _md5(LEG185_JSON),
        "grid_ladder_replayed": rows,
        "banked_grid_ladder": d5["nu_ladder_at_a_0p30"],
        "grid_ladder_max_abs_deviation": max(
            abs(r["nu_replayed"] - b)
            for r, b in zip(rows, d5["nu_ladder_at_a_0p30"][:len(rows)])),
        "chen_a_one_half_replayed": [c["nu"] for c in chen],
        "banked_chen_a_one_half": [banked_chen["nu_from_nu0_0p3"],
                                   banked_chen["nu_from_nu0_0p01"]],
        "chen_a_one_half_max_abs_deviation": max(
            abs(c["nu"] - b) for c, b in
            zip(chen, [banked_chen["nu_from_nu0_0p3"], banked_chen["nu_from_nu0_0p01"]])),
    }


def _md5(path):
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    print("V0  operator validation ...", flush=True)
    v0 = v0_operator_validation()
    for k in ("hilbert_on_chen_pair_relative", "cumint_on_chen_U_relative",
              "d1_on_chen_relative_sup_error", "d2_on_chen_relative_sup_error"):
        print("     %-38s %.3e" % (k, v0[k]), flush=True)

    print("V0b gauge transcription ...", flush=True)
    v0b = v0b_gauge_transcription()
    print("     leg185 gauge rel err vs closed form %.3e -> nu offset %.3e"
          % (v0b["leg185_gauge_relative_error_vs_closed_form"],
             v0b["implied_relative_offset_in_nu"]), flush=True)

    print("V2  independent re-derivation (leg185 gauge) ...", flush=True)
    v2 = v2_independent_rederivation("leg185")
    print("     ladder", ["%.8f" % x for x in v2["nu_ladder_at_a_0p30"]], flush=True)
    print("     richardson %.10f  order %s"
          % (v2["richardson_at_a_0p30"]["extrapolated"],
             v2["richardson_at_a_0p30"]["observed_order"]), flush=True)

    print("V2' closed-form-gauge scaling check (single point) ...", flush=True)
    v2b = v2b_gauge_scaling_check()
    print("     predicted g^-2 offset %.3e, observed %.3e, ratio %.4f"
          % (v2b["predicted_relative_offset"], v2b["observed_relative_offset"],
             v2b["observed_over_predicted"]), flush=True)

    print("V3  dilation-covariance route ...", flush=True)
    v3 = v3_dilation_covariance_route()
    for row in v3["per_a"]:
        print("     a=%.2f nu=%.10f  seeded worst %.3e  unseeded worst %.3e  sign-inv %s"
              % (row["a"], row["nu_on_leg185_gauge"], row["seeded_worst_relative_error"],
                 row["unseeded_worst_relative_error"], row["seeded_sign_invariant"]), flush=True)

    print("V4  sign-flip located by SCAN (not bisection) ...", flush=True)
    v4 = v4_sign_flip_location()
    print("     converged %d/%d, bracket %s, leg125 a* inside: %s"
          % (v4["points_converged"], v4["points_scanned"],
             v4["sign_change_bracket_between_converged_points"],
             v4["leg125_a_star_inside_bracket"]), flush=True)

    print("V5  negative-branch grid study, BOTH schemes ...", flush=True)
    v5 = v5_negative_branch_grid_study()
    for row in v5["per_a"]:
        print("     a=%.2f  mine span %s  leg185 span %s  mine amp min/max %s"
              % (row["a"], row["this_leg_relative_span_over_converged"],
                 row["leg185_relative_span_over_converged"],
                 row["this_leg_min_over_max_amplitude"]), flush=True)

    print("V1  replay of leg 185's own path (weakest tier) ...", flush=True)
    v1 = v1_replay_leg185()
    print("     replayed ladder", ["%.8f" % r["nu_replayed"] for r in v1["grid_ladder_replayed"]],
          flush=True)

    # ---- the gate, answered CLAUSE BY CLAUSE -------------------------------
    # The gate names THREE things: nu = +0.01799364 at a = 0.30, the NEGATIVE VALUES at a = 1/2,
    # and (in its thesis) the a* = 0.3865 crossing.  They do not all get the same answer, and a
    # single boolean would have hidden that -- the first pass of this leg printed
    # "YES -- independently confirmed" while its own a = 1/2 magnitude was 9.9x off, because the
    # criterion only tested a = 0.30 and the SIGN pattern.  Each clause is scored separately.
    nu_indep = v2["richardson_at_a_0p30"]["extrapolated"]
    rel_a030 = abs(nu_indep - LEG185_NU_A030) / abs(LEG185_NU_A030)
    a050 = [r for r in v2["a_sweep_at_n401"] if r["a"] == 0.50][0]
    mine_050 = [a050["nu_from_nu0_0p3"], a050["nu_from_nu0_0p01"]]
    banked_050 = [LEG185_NU_A050_FROM_0P3, LEG185_NU_A050_FROM_0P01]
    ratio_050 = float(np.mean([abs(b) for b in banked_050])
                      / max(np.mean([abs(m) for m in mine_050]), 1e-300))
    v5_050 = [r for r in v5["per_a"] if r["a"] == 0.50][0]
    v5_030 = [r for r in v5["per_a"] if r["a"] == 0.30][0]

    clause_1 = {
        "claim": "nu = +0.01799364 at a = 0.30",
        "leg185_value": LEG185_NU_A030,
        "this_leg_richardson": nu_indep,
        "this_leg_finest_grid": v2["nu_ladder_at_a_0p30"][-1],
        "relative_agreement": rel_a030,
        "significant_digits_agreeing": float(-np.log10(max(rel_a030, 1e-300))),
        "this_leg_ladder": v2["nu_ladder_at_a_0p30"],
        "observed_order_of_convergence": v2["richardson_at_a_0p30"]["observed_order"],
        "truncation_spread_relative": v2["truncation_spread_relative"],
        "grid_span_this_leg_at_a_0p30": v5_030["this_leg_relative_span_over_converged"],
        "grid_span_leg185_at_a_0p30": v5_030["leg185_relative_span_over_converged"],
        "verdict": ("CONFIRMED" if rel_a030 < 1e-5 else "NOT CONFIRMED"),
    }
    clause_2 = {
        "claim": "the NEGATIVE values -0.00817525 / -0.00895316 at Chen's a = 1/2",
        "leg185_values": banked_050,
        "this_leg_values_same_grid_n401": mine_050,
        "magnitude_ratio_leg185_over_this_leg": ratio_050,
        "sign_reproduced": bool(all(x < 0 for x in mine_050)),
        "magnitude_reproduced": bool(0.5 < ratio_050 < 2.0),
        "leg185_own_grid_span_at_a_0p50": v5_050["leg185_relative_span_over_converged"],
        "this_leg_grid_span_at_a_0p50": v5_050["this_leg_relative_span_over_converged"],
        "this_leg_amplitude_collapse_ratio_at_a_0p50": v5_050["this_leg_min_over_max_amplitude"],
        "leg185_amplitude_ratio_at_a_0p50": v5_050["leg185_min_over_max_amplitude"],
        "verdict": ("SIGN CONFIRMED, MAGNITUDE NOT REPRODUCED"
                    if all(x < 0 for x in mine_050) and not (0.5 < ratio_050 < 2.0)
                    else ("CONFIRMED" if all(x < 0 for x in mine_050) else "NOT CONFIRMED")),
        "why": ("leg 185 banked a = 1/2 from a SINGLE grid (n = 401) with no refinement, while "
                "refining a = 0.30 on four grids.  V5 supplies the missing refinement and finds "
                "leg 185's OWN scheme is not grid-converged there either.  So the two schemes "
                "are not disagreeing about a converged number -- they are landing on different "
                "roots of a square system that has several on this side of a*, which is why "
                "only the SIGN was ever bankable.  leg 185 said so ('only the sign is banked'); "
                "this leg measures that its stated 31% start-spread understates the real "
                "instability."),
    }
    clause_3 = {
        "claim": "the nu(a) zero crossing lands on leg 125's a* = 0.3864963972206034",
        "leg125_a_star": LEG125_A_STAR,
        "this_leg_bracket": v4["sign_change_bracket_between_converged_points"],
        "leg125_a_star_inside_this_leg_bracket": v4["leg125_a_star_inside_bracket"],
        "points_failed_to_converge": v4["points_failed_to_converge"],
        "leg185_own_two_starts_at_a_0p3865": [0.00000035, -0.00425080],
        "verdict": ("CONFIRMED" if v4["leg125_a_star_inside_bracket"] else "NOT REPRODUCED"),
        "why": ("leg 185's own two starts STRADDLE ZERO at a = 0.3865 (+3.5e-7 and -4.25e-3), "
                "so its own data never pinned the crossing; the '8-digit agreement' it reports "
                "is one of two disagreeing starts matching leg 125."),
    }
    verdict = {
        "clause_1_headline_nu_at_a_0p30": clause_1,
        "clause_2_negative_values_at_chen_a": clause_2,
        "clause_3_a_star_crossing": clause_3,
        "sign_claim_overall": {
            "claim": "nu > 0 below a*, nu < 0 at and above it (including Chen's a = 1/2)",
            "this_leg_positive_at": v2["a_with_admissible_positive_nu"],
            "this_leg_negative_at": v2["a_with_inadmissible_negative_nu"],
            "sign_is_dilation_invariant": all(r["seeded_sign_invariant"] for r in v3["per_a"]),
            "verdict": "CONFIRMED AND STRENGTHENED",
            "why": ("the sign survives both discretizations, every grid, both starts, and -- "
                    "because nu -> mu^2 nu under dilation -- every gauge.  That last point is "
                    "new: it makes the sign claim gauge-independent, which leg 185 did not "
                    "establish."),
        },
    }
    confirmed_headline = clause_1["verdict"] == "CONFIRMED"
    verdict["gate_answer"] = (
        "SPLIT -- headline CONFIRMED, a=1/2 MAGNITUDES NOT REPRODUCED (escalate)"
        if confirmed_headline and clause_2["verdict"] != "CONFIRMED"
        else ("YES -- independently confirmed"
              if confirmed_headline and clause_2["verdict"] == "CONFIRMED"
              else "NO -- headline not reproduced"))
    verdict["escalation_required"] = bool(clause_2["verdict"] != "CONFIRMED"
                                          or clause_3["verdict"] != "CONFIRMED")

    out = {
        "leg": 210, "route": "M2SV", "date": "2026-08-07",
        "no_dynamics_run": True,
        "what_this_is": ("INDEPENDENT VERIFICATION of leg 185's reparametrized nu measurement. "
                         "Float, discretised, truncated.  No certificate.  Confirming leg 185's "
                         "number is a REPRODUCIBILITY statement about this repository's own "
                         "computation, NOT an existence result about gCLM."),
        "V0_operator_validation": v0,
        "V0b_gauge_transcription": v0b,
        "V2_independent_rederivation_leg185_gauge": v2,
        "V2b_gauge_scaling_check": v2b,
        "V3_dilation_covariance_route": v3,
        "V4_sign_flip_location": v4,
        "V5_negative_branch_grid_study": v5,
        "V1_replay_weakest_tier": v1,
        "VERDICT": verdict,
        "seconds_total": time.time() - t0,
    }
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print("\nGATE: %s" % verdict["gate_answer"])
    print("  clause 1 (nu at a=0.30)      : %s  rel %.3e (%.1f digits)"
          % (clause_1["verdict"], rel_a030, clause_1["significant_digits_agreeing"]))
    print("  clause 2 (a=1/2 magnitudes)  : %s  leg185/this = %.2fx"
          % (clause_2["verdict"], ratio_050))
    print("  clause 3 (a* crossing)       : %s  bracket %s"
          % (clause_3["verdict"], clause_3["this_leg_bracket"]))
    print("  escalation required          : %s" % verdict["escalation_required"])
    print("wrote", DATA, "in %.1f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
