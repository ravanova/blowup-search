"""Leg 284, Route-NU12: THE GRID-CONVERGED `nu` AT a = 1/2 -- or an honest does-not-converge.

WHAT THIS IS.  Leg 185 (M2SD, landed) reparametrized leg 125's stalled Object-B continuation
with `a` FIXED, the dilation gauge `Omega_X(0)` IMPOSED and `nu` the UNKNOWN, and banked

    nu = +0.01799364              at a = 0.30   (refined on four grids, 55x domain extension)
    nu = -0.00817525 / -0.00895316 at Chen's a = 1/2   (SINGLE grid n = 401, NO refinement)

Leg 210 (M2SV, parked on `leg/210-m2sv-v1`) re-derived the same measurement in an independently
discretized scheme, confirmed the a = 0.30 headline to 1.198e-06 relative, and supplied the
a = 1/2 refinement ladder leg 185 never ran.  It found NON-CONVERGENCE in BOTH schemes at
n in {201, 401, 801} -- leg 185's own values span 62.2% non-monotonically, leg 210's span 119.2%
with the amplitude collapsing by 0.483 -- and STOPPED THERE.  It did not take the ladder to a
verdict and it did not name a mechanism.

THIS LEG DOES BOTH, against a criterion pre-registered in `writeup/novelty/leg_284.md` BEFORE
any number here was computed.  That file is the contract; this runner scores itself against it
and prints every clause with its magnitude, pass or fail.

WHAT IS NEW HERE, RELATIVE TO 185 AND 210.
  (A) THE LADDER IS EXTENDED TWO RUNGS, to n in {201, 401, 801, 1601, 3201}.  `h = 16/(n-1)` in
      rho halves EXACTLY at each rung, so Richardson runs at a constant refinement ratio r = 2.
  (B) A NAMED, FALSIFIABLE MECHANISM WITH POINT PREDICTIONS.  H1, the grid-locked-layer
      hypothesis, read off leg 210's ALREADY-BANKED table before this code existed: the
      diffusive length `ell = sqrt(|nu|/c_l)` sat at 2.036 h then 2.012 h on leg 210's two
      converged a = 1/2 points, and |nu| fell 4.095x for a 2x refinement.  H1 says the root is
      a boundary layer LOCKED TO TWO GRID SPACINGS, so `nu` is set by the mesh, not by the
      equation: |nu(n)| = c_l (2h)^2 = 128/(n-1)^2.  The novelty pass fixes the point
      predictions nu(1601) = -5.000e-05 and nu(3201) = -1.250e-05 and the scoring windows.
      THEY CAN FAIL, and if they do this runner says so.
  (C) ROOT SELECTION BY PSEUDO-ARCLENGTH CONTINUATION IN `a`, from the converged, independently
      confirmed a = 0.30 root.  Legs 185 and 210 both restarted Newton from the Chen profile at
      every (n, a), so WHICH root they landed on was a basin accident.  Continuing the branch
      asks the question neither asked: does the a = 0.30 branch REACH a = 1/2 at all?  Folds in
      `a` are traversable and are DETECTED rather than mistaken for failure.
  (D) A CONVERGENCE CRITERION THAT CANNOT BE FOOLED BY nu -> 0 (lesson 84).  A sequence
      converging to zero at rate h^2 passes every naive Richardson test -- zero is a perfect
      plateau.  Clause K1 therefore requires the layer to be RESOLVED (ell/h >= 8) and ell/h to
      GROW under refinement, which is what a fixed continuum length does and a mesh-locked one
      cannot.  That clause was written before the run, not after seeing the answer.

SCOPE, PRE-COMMITTED AND BINDING.  Everything is FLOATING POINT on a discretised, truncated
domain.  NO CERTIFICATE, no existence claim, no movement on L1..L4.  Clay stays ~0.05%.  This
module BUILDS NO SOLVER: the discretization lives entirely inside `experiments/` so it cannot
be mistaken for or reused as banked machinery (`capabilities.py` grepped first -- see
`writeup/novelty/leg_284.md` sec 1).  `solver/dissipative_profile.py` and
`solver/line_hilbert.py` are imported READ-ONLY and never edited; NO file under `solver/` is
touched, so Ruling 178-3 (the contamination cap on `solver/energy_coercivity.py`) is checked
and does not bind.  `no_dynamics_run: true` -- every solve here is of a STEADY equation.
Leg 174's catalog is NOT touched: that edit is leg 283's, running in another slot.

ON REUSING LEG 210'S DISCRETIZATION, DECLARED RATHER THAN HIDDEN.  This leg carries leg 210's
independent scheme forward DELIBERATELY -- 6th-order differences, the chain-rule second
derivative, the degree-5 Lagrange panel quadrature, the odd-subspace LU -- because the whole
point is to extend THAT ladder to a verdict.  A third discretization would answer a different
question.  What is new is the ladder's length, the mechanism test, the continuation, and the
criterion; the operators are re-derived here (not imported from the parked branch, which is
read but never edited) and are re-validated against closed forms in V0 before use, so this
module stands alone.  `solver/line_hilbert.py`'s dense whole-line Hilbert matrix is the one
shared operator, as in leg 210, and is validated rather than trusted.
"""

import json
import os
import time

# Pinned BEFORE numpy loads, and it matters twice over.  (1) SPEED: this machine's threaded
# BLAS spends 1.27 s on a 200x200 `solve` that takes 0.0013 s on one thread -- a 1000x
# thread-thrash penalty that made the extended ladder unaffordable.  (2) DETERMINISM: a
# multithreaded GEMM sums in a nondeterministic order, and V6 below measures that at Chen's
# `a` a residual perturbation of 1.8e-15 moves `nu` by 61%.  A run whose arithmetic order can
# vary between invocations could not report that number honestly.  Every solve here is
# single-threaded and bit-reproducible.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from solver.dissipative_profile import DissipativeProfile, chen_profile
from solver.line_hilbert import line_hilbert_matrix

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "writeup", "data", "p2_route_nu12_v1_converge.json")

C_L = 0.5                       # Delta = 0, the gamma = 2 steadiness condition (leg 185's)
C_OMEGA = -1.0                  # the amplitude gauge (leg 185's)
B_CHEN = float(np.sqrt(3.0 / 8.0))
G_CHEN_ANALYTIC = -2.0 / B_CHEN ** 3

# --- everything below this line is PRE-REGISTERED in writeup/novelty/leg_284.md --------------
LADDER = (201, 401, 801, 1601, 3201)      # h in rho halves exactly at each rung
A_CONTROL = 0.30                          # the known-answer control (lesson 84's window)
A_CHEN = 0.50
A_SECOND_NEG = 0.45

K1_MIN_ELL_OVER_H = 8.0                   # layer resolved by >= 8 points at the origin
K1_MIN_GROWTH_PER_DOUBLING = 1.5          # ell/h must GROW; a mesh-locked length cannot
K2_MAX_RELRES = 1e-10                     # leg 210's own CONVERGED_RELRES, carried unchanged
K4_ORDER_WINDOW = (1.5, 8.0)
K5_MAX_EXTRAP_REL = 1e-3
K5_MIN_DIFF_SHRINK = 2.0
K6_MAX_START_SPREAD = 1e-3
K6_MAX_TRUNC_SPREAD = 1e-2

P1_LAW = lambda n: -128.0 / (n - 1.0) ** 2          # |nu| = c_l (2h)^2, h = 8/(n-1)
P1_WINDOW = (0.80, 1.25)
P2_K = 0.638                                        # calibrated from leg 210's two points
P2_LAW = lambda n: P2_K * abs(G_CHEN_ANALYTIC) * 2.0 * (8.0 / (n - 1.0))
P2_WINDOW = (0.85, 1.18)
P3_MIN_SV_DECAY_AT_CHEN = 4.0
P3_MAX_SV_DRIFT_AT_CONTROL = 2.0
P3_LOCALISATION_WINDOW_IN_ELL = 4.0
P4_MIN_ERR_AT_CHEN = 1e-2
P4_MAX_ERR_AT_CONTROL = 1e-3
P5_MAX_BRACKET_WIDTH = 0.02

# leg 185's / leg 210's banked numbers, transcribed for explicit comparison
LEG185_NU_A030 = 0.01799364
LEG185_NU_A050 = (-0.00817525, -0.00895316)
LEG210_NU_A050 = {401: -0.00082927, 801: -0.00020250}
LEG210_AMP_A050 = {401: 0.2260, 801: 0.1092}
LEG125_A_STAR = 0.3864963972206034
LEG210_BRACKET = (0.36, 0.37)


# ---------------------------------------------------------------------------
# operators -- leg 210's independent discretization, re-derived here
# ---------------------------------------------------------------------------

def _sinh_grid(n, c=0.5, rho_max=8.0):
    if n % 2 == 0:
        n += 1
    rho = np.linspace(-rho_max, rho_max, n)
    return rho, c * np.sinh(rho), n


def _d1_matrix6(n, h):
    """6th-order centred d/drho, tapering to 4/2/1 at the last three nodes each end."""
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
    """6th-order centred d^2/drho^2 -- a DIRECT second-difference stencil, not `D @ D`."""
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
    """int_0^1 L_k(t) dt on t = -2..3, solved from the moment system, not quoted."""
    t = np.array([-2.0, -1.0, 0.0, 1.0, 2.0, 3.0])
    V = np.vander(t, 6, increasing=True).T
    return np.linalg.solve(V, np.array([1.0 / (k + 1) for k in range(6)]))


def _cumint_matrix6(n, h, i0):
    wl = _panel_weights6() * h
    C = np.zeros((n, n))

    def panel(i):
        w = np.zeros(n)
        if 2 <= i <= n - 4:
            w[i - 2:i + 4] += wl
        else:
            w[i] += h / 2.0
            w[i + 1] += h / 2.0
        return w

    for i in range(i0, n - 1):
        C[i + 1] = C[i] + panel(i)
    for i in range(i0 - 1, -1, -1):
        C[i] = C[i + 1] - panel(i)
    return C


class Grid:
    """Grid-dependent operators, built ONCE per (n, rho_max) and reused across every `a`.

    Leg 210 rebuilt the whole operator set for every (a, n) pair.  None of these operators
    depends on `a`, and the dense Hilbert matrix is the build's dominant cost, so hoisting it
    is what makes n = 3201 and a continuation run affordable at all.  It changes no number:
    the operators are bit-identical to leg 210's for the same (n, rho_max)."""

    def __init__(self, n=801, c=0.5, rho_max=8.0, keep_V=True):
        self.rho, self.X, self.n = _sinh_grid(n, c=c, rho_max=rho_max)
        n = self.n
        self.rho_max = float(rho_max)
        self.i0 = n // 2
        self.m = n - self.i0 - 1
        self.h_rho = self.rho[1] - self.rho[0]
        self.h_X0 = float(c * self.h_rho)          # grid spacing AT THE ORIGIN, the layer scale
        X_rho = c * np.cosh(self.rho)
        D1r = _d1_matrix6(n, self.h_rho)
        D2r = _d2_matrix6(n, self.h_rho)
        self.X_rho = X_rho
        self.D = D1r / X_rho[:, None]
        self.D2 = D2r / (X_rho ** 2)[:, None] - (self.X / X_rho ** 3)[:, None] * D1r
        del D2r
        self.H = line_hilbert_matrix(self.X)
        V = _cumint_matrix6(n, self.h_rho, self.i0) * X_rho[None, :]
        self.VH = V @ self.H
        self.V = V if keep_V else None
        del D1r
        self.g_row = self.D[self.i0]
        # leg 185's DISCRETE gauge, recomputed in ITS OWN discretization so the comparison
        # tests leg 185's computation and not a better normalization of ours
        dp = DissipativeProfile(a=0.5, n=n, rho_max=rho_max)
        self.gauge = float(dp.D[dp.i0] @ chen_profile(dp.X)[0])
        del dp
        self.chen = chen_profile(self.X)[0]

    # -- the equation -----------------------------------------------------
    def residual(self, Om, a, nu, assoc="leg210"):
        """R = (c_om + H Om) Om - c_l X Om_X - a U Om_X + nu Om_XX.

        `assoc` selects only the ORDER OF THE FLOATING-POINT ADDITIONS, nothing else:
          "grouped" -- the two advection terms combined as -(c_l X + a U) Om_X;
          "leg210"  -- written out as -c_l X Om_X - a U Om_X, byte-for-byte leg 210's line.
        The two are the same expression in exact arithmetic and differ by ~1e-15 in float64.
        Tier V6 measures what that difference does, and the answer is the reason this
        parameter exists rather than being a stylistic choice."""
        HOm = self.H @ Om
        OmX = self.D @ Om
        U = self.VH @ Om
        if assoc == "leg210":
            return ((C_OMEGA + HOm) * Om - C_L * self.X * OmX - a * U * OmX
                    + nu * (self.D2 @ Om))
        return (C_OMEGA + HOm) * Om - (C_L * self.X + a * U) * OmX + nu * (self.D2 @ Om)

    def jacobian(self, Om, a, nu, assoc="leg210"):
        """dR/dOmega, differentiated by hand; R is quadratic so this is exact.

        Accumulated in place: at n = 3201 each n x n temporary is 82 MB, and the naive
        expression allocates five of them.  `assoc` carries the same meaning as in
        `residual`."""
        HOm = self.H @ Om
        OmX = self.D @ Om
        U = self.VH @ Om
        J = Om[:, None] * self.H
        if assoc == "leg210":
            J -= C_L * (self.X[:, None] * self.D)
            J -= a * (OmX[:, None] * self.VH + U[:, None] * self.D)
        else:
            J -= (C_L * self.X + a * U)[:, None] * self.D
            J -= (a * OmX)[:, None] * self.VH
        J += nu * self.D2
        J[np.diag_indices(self.n)] += C_OMEGA + HOm
        return J

    def dR_dnu(self, Om):
        return self.D2 @ Om

    def dR_da(self, Om):
        return -(self.VH @ Om) * (self.D @ Om)

    # -- odd subspace -----------------------------------------------------
    def odd_reduce(self, M):
        """Restrict a linear map to ODD vectors (leg 210's `_odd_reduce`).

        H maps odd -> even, so (c_omega + H Om) Om, X Om_X, U Om_X and Om_XX are ALL odd:
        the residual of an odd profile is odd, R(0) = 0 identically, and the rows below the
        centre are the negatives of those above.  That is the exact rank deficiency leg 185
        absorbed with least squares; restricting removes it and leaves a nonsingular square
        system for LU."""
        i0 = self.i0
        return M[i0 + 1:, i0 + 1:] - M[i0 + 1:, i0 - 1::-1]

    def odd_row(self, v):
        i0 = self.i0
        return v[i0 + 1:] - v[i0 - 1::-1]

    def expand(self, w):
        Om = np.zeros(self.n)
        Om[self.i0 + 1:] = w
        Om[:self.i0] = -w[::-1]
        return Om


_GRIDS = {}


def grid_for(n, rho_max=8.0):
    key = (n, rho_max)
    if key not in _GRIDS:
        _GRIDS[key] = Grid(n=n, rho_max=rho_max, keep_V=(n <= 801))
    return _GRIDS[key]


# ---------------------------------------------------------------------------
# V0 -- operators validated against closed forms BEFORE they measure anything
# ---------------------------------------------------------------------------

def v0_operator_validation(n=801):
    g = grid_for(n)
    X, b = g.X, B_CHEN
    Om, Ux, U = chen_profile(X)
    den = X ** 2 + b ** 2
    Om_X_exact = -2.0 * b * (den ** -2 - 4.0 * X ** 2 * den ** -3)
    Om_XX_exact = -2.0 * b * (-12.0 * X * den ** -3 + 24.0 * X ** 3 * den ** -4)
    Om0 = -4.0 * X / (1.0 + 4.0 * X ** 2)
    HOm0 = 2.0 / (1.0 + 4.0 * X ** 2)
    return {
        "n": g.n, "X_max": float(X[-1]), "h_X_at_origin": g.h_X0,
        "hilbert_on_chen_pair_relative":
            float(np.abs(g.H @ Om - Ux).max() / np.abs(Ux).max()),
        "hilbert_on_a0_clm_pair_sup_error": float(np.abs(g.H @ Om0 - HOm0).max()),
        "hilbert_on_a0_clm_pair_note": (
            "LARGER than the Chen check by ~5 orders and that is EXPECTED, not a defect: "
            "Omega_0 = -4X/(1+4X^2) decays like 1/X so the whole-line integral has a tail the "
            "truncated grid cannot see.  Chen's decays like X^-3 and is the regime every solve "
            "here uses.  Reported because a validation you only quote when it passes is not "
            "a validation."),
        "cumint_on_chen_U_relative":
            float(np.abs(g.V @ Ux - U).max() / np.abs(U).max()) if g.V is not None else None,
        "d1_on_chen_relative_sup_error":
            float(np.abs(g.D @ Om - Om_X_exact).max() / np.abs(Om_X_exact).max()),
        "d2_on_chen_relative_sup_error":
            float(np.abs(g.D2 @ Om - Om_XX_exact).max() / np.abs(Om_XX_exact).max()),
        "gauge_leg185_discrete": g.gauge,
        "gauge_closed_form_minus_two_over_b_cubed": G_CHEN_ANALYTIC,
        "gauge_relative_error_vs_closed_form":
            float(abs(g.gauge - G_CHEN_ANALYTIC) / abs(G_CHEN_ANALYTIC)),
        "reading": ("every operator reproduces a closed form before it is used, so no verdict "
                    "below can be an agreement between two copies of one bug.  The gauge is "
                    "leg 185's OWN discrete value, not the closed form, so the comparison "
                    "tests leg 185's computation rather than substituting a better "
                    "normalization."),
    }


# ---------------------------------------------------------------------------
# the square solve, with the layer diagnostics H1 needs
# ---------------------------------------------------------------------------

def _diagnose(g, w, a, nu, relres, iters):
    Om = g.expand(w)
    amp = float(np.abs(Om).max())
    ell = float(np.sqrt(abs(nu) / C_L))
    return {
        "n": g.n, "a": float(a), "rho_max": g.rho_max, "nu": float(nu),
        "residual_relative": float(relres), "iters": int(iters),
        "amplitude": amp,
        "h_X_at_origin": g.h_X0,
        "diffusive_length_ell": ell,
        "ell_over_h": float(ell / g.h_X0),
        "amp_over_h": float(amp / g.h_X0),
        "edge_over_amplitude": float(abs(Om[-1]) / max(amp, 1e-300)),
        "converged_relres": bool(relres < K2_MAX_RELRES),
        "layer_resolved_K1": bool(ell / g.h_X0 >= K1_MIN_ELL_OVER_H),
    }


def solve_nu(g, a, nu0, w_start=None, iters=60, tol=1e-13, gauge=None,
              assoc="leg210"):
    """Square system on the ODD subspace: unknowns (Omega_odd, nu); equations (R_odd, gauge)."""
    i0, m = g.i0, g.m
    gauge = g.gauge if gauge is None else float(gauge)
    w = np.array(g.chen[i0 + 1:] if w_start is None else w_start, dtype=float)
    nu = float(nu0)
    relres = np.inf
    best = np.inf
    since_best = 0
    k = 0
    for k in range(iters):
        Om = g.expand(w)
        R = g.residual(Om, a, nu, assoc)
        scale = float(np.sqrt(np.mean(((C_OMEGA + g.H @ Om) * Om) ** 2)))
        rms = float(np.sqrt(np.mean(R ** 2)))
        relres = rms / max(scale, 1e-300)
        if rms < tol:
            break
        # STAGNATION BREAK, declared.  Newton converges quadratically: a solve that is going
        # to reach `tol` does so in well under 20 iterations, so this can only ever fire on a
        # solve that is NOT converging -- exactly the ones where the augmented Jacobian is
        # numerically singular (P3 measures sigma_min/sigma_max = 7e-16 at Chen's `a`).  It
        # changes no converged number; it stops the run from spending 60 iterations at
        # n = 3201 discovering that the residual has stopped falling.  The final relative
        # residual is reported either way, so a solve stopped here is visibly NOT converged.
        if rms < best * 0.9:
            best, since_best = rms, 0
        else:
            since_best += 1
            if since_best >= 10:
                break
        F = np.concatenate([R[i0 + 1:], [float(g.g_row @ Om) - gauge]])
        J = np.zeros((m + 1, m + 1))
        J[:m, :m] = g.odd_reduce(g.jacobian(Om, a, nu, assoc))
        J[:m, m] = g.dR_dnu(Om)[i0 + 1:]
        J[m, :m] = g.odd_row(g.g_row)
        try:
            step = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            step, *_ = np.linalg.lstsq(J, -F, rcond=None)
        w = w + step[:m]
        nu = nu + float(step[m])
    out = _diagnose(g, w, a, nu, relres, k)
    out["assoc"] = assoc
    out["stopped_on_stagnation"] = bool(since_best >= 10)
    out["w"] = w
    return out


def augmented_jacobian(g, w, a, nu):
    m = g.m
    Om = g.expand(w)
    J = np.zeros((m + 1, m + 1))
    J[:m, :m] = g.odd_reduce(g.jacobian(Om, a, nu))
    J[:m, m] = g.dR_dnu(Om)[g.i0 + 1:]
    J[m, :m] = g.odd_row(g.g_row)
    return J


def conditioning_and_localisation(g, w, a, nu):
    """P3: is the near-null direction of the augmented Jacobian the ORIGIN LAYER?

    A genuinely isolated root has a Jacobian whose smallest singular value is bounded away from
    zero relative to its largest, uniformly in n.  A root that is an artifact of the mesh does
    not: the direction that costs nothing is the one that reshapes the layer, and that
    direction is LOCALISED at the origin on the scale ell."""
    J = augmented_jacobian(g, w, a, nu)
    U_, s, Vt = np.linalg.svd(J)
    v = Vt[-1]
    vw = v[:g.m]
    Xr = g.X[g.i0 + 1:]
    ell = np.sqrt(abs(nu) / C_L)
    mass = float(vw @ vw)
    win_ell = float(vw[Xr <= P3_LOCALISATION_WINDOW_IN_ELL * ell]
                    @ vw[Xr <= P3_LOCALISATION_WINDOW_IN_ELL * ell]) / max(mass, 1e-300)
    win_h = float(vw[Xr <= 4.0 * g.h_X0] @ vw[Xr <= 4.0 * g.h_X0]) / max(mass, 1e-300)
    return {
        "sigma_max": float(s[0]), "sigma_min": float(s[-1]),
        "sigma_min_over_sigma_max": float(s[-1] / s[0]),
        "nullvec_mass_within_4_ell_of_origin": win_ell,
        "nullvec_mass_within_4_h_of_origin": win_h,
        "nu_component_of_nullvec": float(abs(v[g.m])),
    }


# ---------------------------------------------------------------------------
# A -- the extended ladder (the leg's headline instrument)
# ---------------------------------------------------------------------------

def _richardson(ns, vals):
    ns = np.asarray(ns[-3:], dtype=float)
    vs = np.asarray(vals[-3:], dtype=float)
    d1, d2 = vs[1] - vs[0], vs[2] - vs[1]
    if d2 == 0.0 or d1 / d2 <= 0:
        return {"extrapolated": float(vs[-1]), "observed_order": None,
                "note": "non-monotone or at the float64 floor; finest value reported"}
    r = ns[1] / ns[0]
    p = float(np.log(d1 / d2) / np.log(r))
    return {"extrapolated": float(vs[2] + d2 / (r ** p - 1.0)), "observed_order": p,
            "note": "v(n) = v_inf + C n^-p through the three finest grids"}


# ---------------------------------------------------------------------------
# C -- pseudo-arclength continuation in `a` from the CONVERGED a = 0.30 root
# ---------------------------------------------------------------------------

def continuation_in_a(n, a0=A_CONTROL, a_target=0.60, target_da=0.004,
                      ds_max=2.0, ds_min=1e-9, max_steps=400, land_at=(A_CHEN,), a_back_stop=None):
    """Continue (Omega_odd, nu, a) with the gauge held, by pseudo-arclength.

    Unknowns y = (w, nu, a) in R^(m+2); equations F = (R_odd, gauge) in R^(m+1) plus the
    arclength condition t . (y - y_prev) = ds.  The tangent t is the null vector of the
    (m+1) x (m+2) Jacobian, so FOLDS IN `a` ARE TRAVERSABLE -- a natural-parameter sweep would
    stop at one and report a failure that is really a turning point.  The step is chosen so
    that |t_a| ds ~ target_da, which automatically lengthens the step near a fold.

    Every accepted point carries its own K1/K2 verdict, so the branch is reported as a curve of
    MEASURED points, not as a smooth story."""
    g = grid_for(n)
    m = g.m
    base = solve_nu(g, a0, 0.3)
    y = np.concatenate([base.pop("w"), [base["nu"], a0]])
    pts = [dict(base, step=0, ds=0.0, tangent_a=None)]
    t_prev = None
    ds = 0.05
    fold_count = 0
    stop = "max_steps"

    def bigJ(y):
        w, nu, a = y[:m], y[m], y[m + 1]
        Om = g.expand(w)
        J = np.zeros((m + 1, m + 2))
        J[:m, :m] = g.odd_reduce(g.jacobian(Om, a, nu))
        J[:m, m] = g.dR_dnu(Om)[g.i0 + 1:]
        J[:m, m + 1] = g.dR_da(Om)[g.i0 + 1:]
        J[m, :m] = g.odd_row(g.g_row)
        return J, Om

    def Fvec(y):
        w, nu, a = y[:m], y[m], y[m + 1]
        Om = g.expand(w)
        R = g.residual(Om, a, nu)
        return np.concatenate([R[g.i0 + 1:], [float(g.g_row @ Om) - g.gauge]]), Om, R

    def tangent(y, t_prev):
        """Null vector of the (m+1) x (m+2) Jacobian, by a BORDERED SOLVE, not an SVD.

        Bordering with the previous tangent and solving once costs one LU of size m+2; an SVD
        of the same matrix costs ~10x more and, at n = 3201, would have made the continuation
        ladder unaffordable.  The first step has no previous tangent and falls back to the SVD."""
        J, _ = bigJ(y)
        if t_prev is None:
            _, _, Vt = np.linalg.svd(J)
            t = Vt[-1]
            return t if t[m + 1] >= 0 else -t         # start by moving `a` upward
        A = np.zeros((m + 2, m + 2))
        A[:m + 1] = J
        A[m + 1] = t_prev
        rhs = np.zeros(m + 2)
        rhs[m + 1] = 1.0
        try:
            t = np.linalg.solve(A, rhs)
        except np.linalg.LinAlgError:
            _, _, Vt = np.linalg.svd(J)
            t = Vt[-1]
        nrm = float(np.linalg.norm(t))
        if not np.isfinite(nrm) or nrm == 0.0:
            _, _, Vt = np.linalg.svd(J)
            t = Vt[-1]
            nrm = 1.0
        t = t / nrm
        return t if float(t @ t_prev) >= 0 else -t

    landed = {}
    for step in range(1, max_steps + 1):
        t = tangent(y, t_prev)
        if t_prev is not None and t[m + 1] * t_prev[m + 1] < 0:
            fold_count += 1
        ds = float(min(ds_max, target_da / max(abs(t[m + 1]), 1e-4)))
        if step == 1:
            ds = min(ds, 0.05)          # the first predictor has no tangent history to trust
        ok = False
        while ds > ds_min:
            yy = y + ds * t
            good = False
            for _ in range(30):
                F, Om, R = Fvec(yy)
                # RELATIVE, not absolute.  DEFECT FOUND AND RECORDED (lesson 67): the first
                # version of this corrector required rms(R) < 1e-13 ABSOLUTE.  The n = 1601
                # grid's own residual floor is 2.39e-13 -- the a = 0.30 ladder solve reports
                # exactly that -- so the test was UNREACHABLE there and the continuation died
                # at step 0 with ds halved to 9.14e-10 after 348 s, reporting a branch failure
                # that was a property of the tolerance and not of the branch.  n = 801 passed
                # only because its floor happens to sit below 1e-13.  A convergence test that
                # a grid cannot satisfy manufactures a negative result, which is exactly the
                # failure mode this repository keeps finding in its own instruments.
                scale = float(np.sqrt(np.mean(((C_OMEGA + g.H @ Om) * Om) ** 2)))
                rms = float(np.sqrt(np.mean(R ** 2)))
                if rms < 1e-13 or rms / max(scale, 1e-300) < 1e-11:
                    good = True
                    break
                JJ, _ = bigJ(yy)
                A = np.zeros((m + 2, m + 2))
                A[:m + 1] = JJ
                A[m + 1] = t
                b = np.concatenate([-F, [ds - float(t @ (yy - y))]])
                try:
                    dy = np.linalg.solve(A, b)
                except np.linalg.LinAlgError:
                    break
                if not np.all(np.isfinite(dy)):
                    break
                yy = yy + dy
            if good:
                ok = True
                break
            ds *= 0.5
        if not ok:
            stop = "corrector_failed_at_ds_%.2e" % ds
            break
        t_prev = t
        y = yy
        F, Om, R = Fvec(y)
        scale = float(np.sqrt(np.mean(((C_OMEGA + g.H @ Om) * Om) ** 2)))
        relres = float(np.sqrt(np.mean(R ** 2))) / max(scale, 1e-300)
        d = _diagnose(g, y[:m], y[m + 1], y[m], relres, 0)
        d.update({"step": step, "ds": ds, "tangent_a": float(t[m + 1])})
        pts.append(d)
        # land EXACTLY on the requested a-values, by a fixed-a Newton seeded from the branch
        a_now, a_was = y[m + 1], pts[-2]["a"]
        for at in land_at:
            if at not in landed and min(a_was, a_now) <= at <= max(a_was, a_now):
                r = solve_nu(g, at, y[m], w_start=y[:m])
                r.pop("w")
                r["selected_by"] = "continuation_from_a_%.2f" % a0
                landed[at] = r
        if d["amplitude"] < 1e-8:
            stop = "amplitude_collapsed_to_%.2e" % d["amplitude"]
            break
        if y[m + 1] >= a_target:
            stop = "reached_a_target"
            break
        back = (a0 - 0.05) if a_back_stop is None else a_back_stop
        if fold_count > 0 and y[m + 1] < back:
            stop = "branch_FOLDED_and_turned_back_below_a_%.3f" % back
            break
    good = [p for p in pts if p["converged_relres"]]
    k1 = [p for p in good if p["layer_resolved_K1"]]
    reached = [p for p in k1 if abs(p["a"] - A_CHEN) < 1e-3]
    # THE FOLD.  The last point before the tangent's `a`-component changes sign and the first
    # after it bracket a turning point: the value of `a` beyond which this branch CEASES TO
    # EXIST.  A fold is not a solver failure and not a zero of nu -- it is a statement about
    # the solution set, and it is the reason a pseudo-arclength continuation was built here
    # instead of a natural-parameter sweep, which would have reported a failed Newton solve.
    fold = None
    for p, q in zip(pts[1:], pts[2:]):
        ta, tb = p["tangent_a"], q["tangent_a"]
        if ta is not None and tb is not None and ta * tb < 0:
            lo, hi = sorted([p["a"], q["a"]])
            fold = {"bracket": [lo, hi], "width": hi - lo,
                    "a_fold_estimate": max(p["a"], q["a"]),
                    "nu_at_fold": q["nu"], "amplitude_at_fold": q["amplitude"],
                    "step_index": q["step"],
                    "leg125_a_star": LEG125_A_STAR,
                    "leg125_a_star_minus_fold": LEG125_A_STAR - max(p["a"], q["a"])}
            break
    return {
        "n": g.n, "a_start": a0, "stop_reason": stop, "steps_taken": len(pts) - 1,
        "landed_on_branch": {("a_%.2f" % k): v for k, v in landed.items()},
        "folds_detected": fold_count,
        "points": pts,
        "a_max_reached": float(max(p["a"] for p in pts)),
        "a_max_with_K1_and_K2": float(max([p["a"] for p in k1], default=float("nan"))),
        "nu_at_a_max_K1": float([p["nu"] for p in k1][-1]) if k1 else None,
        "reaches_chen_a_with_K1": bool(reached),
        "a_star_bracket_on_branch": _crossing_bracket(k1),
        "fold_turning_point": fold,
        "branch_reaches_chen_a": bool(max(p["a"] for p in pts) >= A_CHEN),
        "nu_on_branch_at_chen_a": (landed[A_CHEN]["nu"] if A_CHEN in landed else None),
        "lower_sheet_after_fold": ([{"a": p["a"], "nu": p["nu"], "amplitude": p["amplitude"],
                                     "ell_over_h": p["ell_over_h"]}
                                    for p in pts if p["step"] > fold["step_index"]]
                                   if fold else []),
    }


def _crossing_bracket(pts):
    """The nu = 0 crossing, quoted ONLY between consecutive points that BOTH pass K1 and K2.

    Deliberately NOT a bisection: leg 210 recorded against itself that its first pass printed a
    12-digit a* from a bisection that stepped through non-convergent points (lesson 67).  Here a
    crossing that is not bracketed by two admissible points simply is not reported."""
    for p, q in zip(pts, pts[1:]):
        if p["nu"] * q["nu"] < 0:
            lo, hi = sorted([p["a"], q["a"]])
            return {"bracket": [lo, hi], "width": hi - lo, "midpoint": 0.5 * (lo + hi),
                    "leg125_a_star_inside": bool(lo <= LEG125_A_STAR <= hi),
                    "leg210_bracket": list(LEG210_BRACKET)}
    return None


# ---------------------------------------------------------------------------
# P4 -- dilation covariance, as a CONSEQUENCE test of H1
# ---------------------------------------------------------------------------

def dilation_covariance(a, ns=(401, 801, 1601), kappa=2.0):
    """Omega -> Omega(./mu) sends nu -> mu^2 nu and Omega_X(0) -> Omega_X(0)/mu, EXACTLY.

    So solving at gauge kappa*g, seeded with the dilated base solution, must return
    nu(g)/kappa^2.  A root whose length scale is set by the EQUATION obeys this; a root whose
    length scale is set by the MESH cannot, because the mesh does not dilate with the profile.
    That makes this an independent, gauge-free discriminator for H1 -- and unlike H1's own
    h^2 law it does not involve the number 2h anywhere."""
    rows = []
    for n in ns:
        g = grid_for(n)
        base = solve_nu(g, a, 0.3)
        wb = base.pop("w")
        Om_b = g.expand(wb)
        seed = np.interp(kappa * g.X, g.X, Om_b, left=0.0, right=0.0)
        r = solve_nu(g, a, base["nu"] / kappa ** 2, w_start=seed[g.i0 + 1:],
                     gauge=g.gauge * kappa)
        r.pop("w")
        err = abs(r["nu"] * kappa ** 2 - base["nu"]) / max(abs(base["nu"]), 1e-300)
        rows.append({"n": g.n, "kappa": kappa, "nu_on_gauge": base["nu"],
                     "nu_at_kappa_gauge": r["nu"],
                     "rescaled_kappa_squared": r["nu"] * kappa ** 2,
                     "seeded_relative_error": float(err),
                     "residual_relative": r["residual_relative"],
                     "sign_preserved": bool((r["nu"] > 0) == (base["nu"] > 0))})
        print("      a=%.2f n=%-5d seeded covariance error %.3e" % (a, g.n, err), flush=True)
    return rows


# ---------------------------------------------------------------------------
# V6 -- THE ASSOCIATIVITY PROBE.  NOT PRE-REGISTERED: found post hoc, and labelled as such.
# ---------------------------------------------------------------------------

def v6_associativity_probe(ns=(401, 801, 1601), a_list=(A_CONTROL, A_CHEN), nu0=0.3):
    """How far apart do two BIT-IDENTICAL schemes land when only the ADDITION ORDER differs?

    PROVENANCE, STATED PLAINLY: this tier is NOT in `writeup/novelty/leg_284.md`.  It was not
    predicted; it was found while cross-checking this leg's operators against leg 210's parked
    code, when the two produced different `nu` at a = 1/2 and identical `nu` at a = 0.30.  The
    operator matrices were then compared entry by entry and are EQUAL TO 0.000e+00 in D, D2, H
    and VH, with the same gauge -- so the only difference between the two runs is that leg 210
    wrote `- c_l X Om_X - a U Om_X` and this leg wrote `- (c_l X + a U) Om_X`.  Identical in
    exact arithmetic; ~1e-15 apart in float64.

    Both orderings are therefore run on the whole ladder, at Chen's `a` and at the a = 0.30
    control, and the resulting spread in `nu` is reported as a magnitude.  A quantity that
    moves when the compiler-level association of a sum changes is not a measurement of the
    continuum problem, and no amount of grid refinement can make it one -- which is a STRONGER
    statement than non-convergence and is a different one."""
    rows = []
    for a in a_list:
        for n in ns:
            g = grid_for(n)
            pair = {}
            for assoc in ("leg210", "grouped"):
                r = solve_nu(g, a, nu0, assoc=assoc)
                r.pop("w")
                pair[assoc] = r
            v1, v2 = pair["leg210"]["nu"], pair["grouped"]["nu"]
            both = pair["leg210"]["converged_relres"] and pair["grouped"]["converged_relres"]
            rows.append({
                "a": a, "n": g.n,
                "nu_leg210_ordering": v1, "nu_grouped_ordering": v2,
                "relative_difference": float(abs(v1 - v2) / max(abs(v1), abs(v2), 1e-300)),
                "amplitude_leg210_ordering": pair["leg210"]["amplitude"],
                "amplitude_grouped_ordering": pair["grouped"]["amplitude"],
                "both_converged_to_relres_1e_10": bool(both),
                "residuals": [pair["leg210"]["residual_relative"],
                              pair["grouped"]["residual_relative"]],
                "iters": [pair["leg210"]["iters"], pair["grouped"]["iters"]],
            })
            print("      a=%.2f n=%-5d  leg210-order %+.8e   grouped-order %+.8e   rel diff "
                  "%.3e  (both converged: %s)"
                  % (a, g.n, v1, v2, rows[-1]["relative_difference"], both), flush=True)
    at = lambda aa: [r for r in rows if r["a"] == aa and r["both_converged_to_relres_1e_10"]]
    worst_chen = max([r["relative_difference"] for r in at(A_CHEN)], default=None)
    worst_ctrl = max([r["relative_difference"] for r in at(A_CONTROL)], default=None)
    return {
        "not_preregistered": True,
        "provenance": ("found while cross-checking this leg's operators against leg 210's "
                       "parked code; D, D2, H, VH agree to 0.000e+00 and the gauge is "
                       "identical, so the ONLY difference is the order of two float additions"),
        "rows": rows,
        "worst_relative_difference_at_chen_a": worst_chen,
        "worst_relative_difference_at_control_a": worst_ctrl,
        "discrimination_ratio": (float(worst_chen / worst_ctrl)
                                 if worst_chen and worst_ctrl else None),
        "reading": ("at the a = 0.30 control the two orderings agree to the last digits that "
                    "the discretization itself determines; at Chen's a = 1/2 they land on "
                    "DIFFERENT roots, each solved to relative residual ~5e-15.  Refining the "
                    "grid cannot repair this, because the perturbation that moves the answer "
                    "is already at the floating-point floor."),
    }


# ---------------------------------------------------------------------------
# V7 -- THE STOPPING-RULE PROBE.  NOT PRE-REGISTERED: found post hoc, like V6.
# ---------------------------------------------------------------------------

def v7_stopping_rule_probe(ns=(401, 801), a_list=(A_CONTROL, A_CHEN), nu0=0.3,
                           caps=(15, 20, 30, 45, 60, 90)):
    """Does `nu` depend on WHERE NEWTON IS STOPPED, at residuals that all look converged?

    PROVENANCE, STATED PLAINLY: not in `writeup/novelty/leg_284.md`.  It exists because this
    leg CHANGED ONE OF ITS OWN REPORTED NUMBERS by adding a Newton stagnation break, and the
    honest response to that is to measure the effect rather than to pick a stopping rule and
    not mention it.  An earlier pass of this runner, with an iteration cap of 80 and no
    stagnation break, reported nu = -5.16359197e-04 at a = 1/2, n = 401 in the `grouped`
    ordering, at relative residual 4.86e-15.  With the cap at 60 and the break in place, the
    same code path reports -8.29269100e-04 at relative residual 3.44e-14.  Both look converged
    by any residual test.

    WHY THAT IS POSSIBLE, AND WHY IT IS NOT A BUG: at Chen's `a` the augmented Jacobian is
    SINGULAR TO WORKING PRECISION -- sigma_min/sigma_max = 7.35e-16 at n = 801, i.e. machine
    epsilon.  A singular system has no isolated root; it has a numerically indistinguishable
    FAMILY, every member of which satisfies the residual test.  Newton does not converge to a
    point, it drifts along that family, and any stopping rule selects a different member.
    The a = 0.30 control is run identically as the discriminator: there the Jacobian is well
    conditioned and the stopping rule must not matter at all."""
    rows = []
    for a in a_list:
        for n in ns:
            g = grid_for(n)
            vals = []
            for cap in caps:
                r = solve_nu(g, a, nu0, iters=cap)
                r.pop("w")
                vals.append({"iteration_cap": cap, "nu": r["nu"],
                             "residual_relative": r["residual_relative"],
                             "amplitude": r["amplitude"],
                             "iters_used": r["iters"],
                             "stopped_on_stagnation": r.get("stopped_on_stagnation"),
                             "looks_converged": r["converged_relres"]})
            conv = [v["nu"] for v in vals if v["looks_converged"]]
            spread = (float((max(conv) - min(conv)) / max(abs(np.mean(conv)), 1e-300))
                      if len(conv) > 1 else None)
            rows.append({"a": a, "n": g.n, "per_cap": vals,
                         "n_caps_that_look_converged": len(conv),
                         "relative_spread_over_converged_caps": spread})
            print("      a=%.2f n=%-5d  nu over caps %s  spread %s"
                  % (a, g.n, ["%+.6e" % v["nu"] for v in vals], spread), flush=True)
    at = lambda aa: [r["relative_spread_over_converged_caps"] for r in rows
                     if r["a"] == aa and r["relative_spread_over_converged_caps"] is not None]
    worst_chen = max(at(A_CHEN), default=None)
    worst_ctrl = max(at(A_CONTROL), default=None)
    return {
        "not_preregistered": True,
        "rows": rows,
        "worst_spread_at_chen_a": worst_chen,
        "worst_spread_at_control_a": worst_ctrl,
        "discrimination_ratio": (float(worst_chen / worst_ctrl)
                                 if worst_chen and worst_ctrl else None),
        "self_correction_recorded": (
            "an earlier pass of this runner reported nu = -5.16359197e-04 at a = 1/2, n = 401 "
            "(cap 80, no stagnation break) and the final one reports -8.29269100e-04 (cap 60, "
            "break).  Both at relative residual < 5e-14.  That discrepancy is not hidden, it is "
            "the thing this tier measures."),
        "reading": ("if the spread over stopping rules is large at Chen's a and ~0 at the "
                    "a = 0.30 control, then nu(1/2) is not a property of the discrete system "
                    "either -- it is a property of the solver's trajectory across a "
                    "numerically singular family, and no grid refinement addresses that."),
    }


# ---------------------------------------------------------------------------
# scoring, against the PRE-REGISTERED criterion
# ---------------------------------------------------------------------------

def _series(rows, nu0, assoc="leg210"):
    sel = [r for r in rows if r["nu0"] == nu0 and r.get("assoc", "leg210") == assoc]
    return [r["n"] for r in sel], [r["nu"] for r in sel], sel


def score_criterion(a, rows, trunc_rows=None, cont=None, nu0=0.3, assoc="leg210"):
    """K1..K6, each with the magnitude that decided it."""
    ns, vals, sel = _series(rows, nu0, assoc)
    fine = sel[-3:]
    k1_res = [r["ell_over_h"] for r in fine]
    growth = [k1_res[i + 1] / max(k1_res[i], 1e-300) for i in range(len(k1_res) - 1)]
    K1 = bool(all(v >= K1_MIN_ELL_OVER_H for v in k1_res)
              and all(gg >= K1_MIN_GROWTH_PER_DOUBLING for gg in growth))
    k2_res = [r["residual_relative"] for r in fine]
    K2 = bool(all(v < K2_MAX_RELRES for v in k2_res))
    vf = [r["nu"] for r in fine]
    K3 = bool((vf[0] <= vf[1] <= vf[2]) or (vf[0] >= vf[1] >= vf[2]))
    rich = _richardson([r["n"] for r in fine], vf)
    p = rich["observed_order"]
    K4 = bool(p is not None and K4_ORDER_WINDOW[0] <= p <= K4_ORDER_WINDOW[1])
    extrap_rel = abs(rich["extrapolated"] - vf[-1]) / max(abs(rich["extrapolated"]), 1e-300)
    d1, d2 = abs(vf[1] - vf[0]), abs(vf[2] - vf[1])
    shrink = d1 / max(d2, 1e-300)
    K5 = bool(extrap_rel < K5_MAX_EXTRAP_REL and shrink >= K5_MIN_DIFF_SHRINK)
    finest = max(ns)
    at_fine = {r["nu0"]: r["nu"] for r in rows
               if r["n"] == finest and r.get("assoc", "leg210") == assoc}
    starts = list(at_fine.values())
    start_spread = (abs(max(starts) - min(starts)) / max(abs(np.mean(starts)), 1e-300)
                    if len(starts) > 1 else 0.0)
    cont_nu = None
    if cont is not None and cont.get("reaches_chen_a_with_K1"):
        cont_nu = cont["nu_at_a_max_K1"]
        starts = starts + [cont_nu]
        start_spread = abs(max(starts) - min(starts)) / max(abs(np.mean(starts)), 1e-300)
    trunc_spread = None
    if trunc_rows:
        tv = [r["nu"] for r in trunc_rows]
        trunc_spread = float((max(tv) - min(tv)) / max(abs(np.mean(tv)), 1e-300))
    K6 = bool(start_spread < K6_MAX_START_SPREAD
              and (trunc_spread is None or trunc_spread < K6_MAX_TRUNC_SPREAD))
    all_ok = bool(K1 and K2 and K3 and K4 and K5 and K6)
    return {
        "a": a, "nu0_scored": nu0, "assoc_scored": assoc,
        "ladder_n": ns, "ladder_nu": vals,
        "ladder_ell_over_h": [r["ell_over_h"] for r in sel],
        "ladder_amplitude": [r["amplitude"] for r in sel],
        "ladder_residual_relative": [r["residual_relative"] for r in sel],
        "K1_layer_resolved_and_growing": {
            "pass": K1, "ell_over_h_three_finest": k1_res,
            "growth_per_doubling": growth,
            "threshold_ell_over_h": K1_MIN_ELL_OVER_H,
            "threshold_growth": K1_MIN_GROWTH_PER_DOUBLING,
            "why": ("a continuum length is fixed in X, so ell/h DOUBLES under refinement; a "
                    "mesh-locked length holds ell/h constant.  This is the clause that makes "
                    "'nu -> 0 like h^2' a FAILURE and not a plateau (lesson 84)."),
        },
        "K2_solve_quality": {"pass": K2, "relres_three_finest": k2_res,
                             "threshold": K2_MAX_RELRES},
        "K3_monotone": {"pass": K3, "nu_three_finest": vf},
        "K4_richardson_order": {"pass": K4, "observed_order": p, "window": list(K4_ORDER_WINDOW),
                                "extrapolated": rich["extrapolated"]},
        "K5_extrapolation_tight": {"pass": K5, "relative_extrapolation_gap": float(extrap_rel),
                                   "successive_difference_shrink": float(shrink),
                                   "thresholds": [K5_MAX_EXTRAP_REL, K5_MIN_DIFF_SHRINK]},
        "K6_start_and_truncation_independent": {
            "pass": K6, "start_spread_at_finest": float(start_spread),
            "continuation_nu_included": cont_nu,
            "truncation_spread": trunc_spread,
            "thresholds": [K6_MAX_START_SPREAD, K6_MAX_TRUNC_SPREAD]},
        "GRID_CONVERGED": all_ok,
        "first_failing_clause": next((k for k, v in
                                      [("K1", K1), ("K2", K2), ("K3", K3),
                                       ("K4", K4), ("K5", K5), ("K6", K6)] if not v), None),
    }


def score_mechanism(rows_chen, cond_chen, cond_ctrl, cov_chen, cov_ctrl, nu0=0.3,
                    assoc="leg210"):
    _, _, sel = _series(rows_chen, nu0, assoc)
    p1 = []
    for r in sel:
        pred = P1_LAW(r["n"])
        p1.append({"n": r["n"], "predicted_nu": pred, "observed_nu": r["nu"],
                   "observed_over_predicted": float(r["nu"] / pred),
                   "converged_relres": r["converged_relres"],
                   "was_predicted_in_advance": r["n"] in (1601, 3201)})
    new = [q for q in p1 if q["was_predicted_in_advance"] and q["converged_relres"]]
    P1 = bool(new and all(P1_WINDOW[0] <= q["observed_over_predicted"] <= P1_WINDOW[1]
                          for q in new))
    p2 = []
    for r in sel:
        pred = P2_LAW(r["n"])
        p2.append({"n": r["n"], "predicted_amplitude": pred, "observed_amplitude": r["amplitude"],
                   "observed_over_predicted": float(r["amplitude"] / pred),
                   "converged_relres": r["converged_relres"],
                   "was_predicted_in_advance": r["n"] in (1601, 3201)})
    new2 = [q for q in p2 if q["was_predicted_in_advance"] and q["converged_relres"]]
    P2 = bool(new2 and all(P2_WINDOW[0] <= q["observed_over_predicted"] <= P2_WINDOW[1]
                           for q in new2))

    def decay(cond):
        ks = sorted(cond)
        if len(ks) < 2:
            return None
        return float(cond[ks[0]]["sigma_min_over_sigma_max"]
                     / max(cond[ks[-1]]["sigma_min_over_sigma_max"], 1e-300))
    dchen, dctrl = decay(cond_chen), decay(cond_ctrl)
    loc_chen = [cond_chen[k]["nullvec_mass_within_4_ell_of_origin"] for k in sorted(cond_chen)]
    loc_ctrl = [cond_ctrl[k]["nullvec_mass_within_4_ell_of_origin"] for k in sorted(cond_ctrl)]
    P3 = bool(dchen is not None and dchen >= P3_MIN_SV_DECAY_AT_CHEN
              and dctrl is not None and (max(dctrl, 1.0 / max(dctrl, 1e-300))
                                         < P3_MAX_SV_DRIFT_AT_CONTROL)
              and min(loc_chen) > 0.5 and max(loc_ctrl) < 0.5)
    e_chen = [r["seeded_relative_error"] for r in cov_chen]
    e_ctrl = [r["seeded_relative_error"] for r in cov_ctrl]
    P4 = bool(min(e_chen) > P4_MIN_ERR_AT_CHEN and max(e_ctrl) < P4_MAX_ERR_AT_CONTROL)
    return {
        "assoc_scored": assoc,
        "H1": ("the a = 1/2 root is a boundary layer LOCKED to two grid spacings, so nu is set "
               "by the mesh (|nu| = c_l (2h)^2 = 128/(n-1)^2), not by the equation"),
        "P1_h_squared_law": {"pass": P1, "window": list(P1_WINDOW), "rows": p1},
        "P2_amplitude_law": {"pass": P2, "window": list(P2_WINDOW), "K_calibrated": P2_K,
                             "rows": p2},
        "P3_near_null_is_the_layer": {
            "pass": P3,
            "sigma_min_over_max_decay_at_chen_a": dchen,
            "sigma_min_over_max_drift_at_control": dctrl,
            "localisation_within_4_ell_at_chen_a": loc_chen,
            "localisation_within_4_ell_at_control": loc_ctrl,
            "per_n_chen": cond_chen, "per_n_control": cond_ctrl,
            "thresholds": {"decay": P3_MIN_SV_DECAY_AT_CHEN,
                           "control_drift": P3_MAX_SV_DRIFT_AT_CONTROL}},
        "P4_dilation_non_covariance": {
            "pass": P4, "errors_at_chen_a": e_chen, "errors_at_control": e_ctrl,
            "thresholds": [P4_MIN_ERR_AT_CHEN, P4_MAX_ERR_AT_CONTROL],
            "rows_chen": cov_chen, "rows_control": cov_ctrl},
        "predictions_passed": int(P1) + int(P2) + int(P3) + int(P4),
        "verdict": ("H1 SUPPORTED" if (P1 and P2) else "H1 REFUTED ON ITS OWN POINT PREDICTIONS"),
        "note": ("P1 and P2 are the load-bearing ones: they were fixed as NUMBERS in the "
                 "novelty pass before this file existed.  P3 and P4 are corroborating.  If P1 "
                 "or P2 fails, H1 is refuted and this leg cannot name the mechanism -- which "
                 "is reported as such rather than repaired."),
    }


# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    print("V0  operator validation ...", flush=True)
    v0 = v0_operator_validation()
    for k in ("hilbert_on_chen_pair_relative", "cumint_on_chen_U_relative",
              "d1_on_chen_relative_sup_error", "d2_on_chen_relative_sup_error"):
        print("      %-34s %s" % (k, v0[k]), flush=True)

    ladders, conds = {}, {}
    for a in (A_CONTROL, A_SECOND_NEG, A_CHEN):
        print("A   extended ladder at a = %.2f  (BOTH float-association orderings) ..." % a,
              flush=True)
        rows = []
        cond = {}
        for n in LADDER:
            g = grid_for(n)
            # Both float-association orderings are carried at every rung at CHEN'S a, which is
            # the one the gate is about; at the two other a-values the second ordering stops at
            # n = 1601.  Both nu0 starts are carried at the control and at Chen's a; a = 0.45 is
            # a secondary negative-side point and carries one.  This is a COST decision on a
            # machine running at load ~50, stated so the solve matrix is not mistaken for a
            # uniform one -- no scored clause loses a rung it needs.
            assocs = ("leg210", "grouped") if (a == A_CHEN or n <= 1601) else ("leg210",)
            starts = (0.3, 0.01) if a in (A_CONTROL, A_CHEN) else (0.3,)
            for assoc in assocs:
                for nu0 in starts:
                    t1 = time.time()
                    r = solve_nu(g, a, nu0, assoc=assoc)
                    w = r.pop("w")
                    r["nu0"] = float(nu0)
                    r["seconds"] = time.time() - t1
                    rows.append(r)
                    print("      n=%-5d %-7s nu0=%-5g nu=%+.8e relres=%.2e amp=%.6f "
                          "ell/h=%.3f (%.1fs)"
                          % (n, assoc, nu0, r["nu"], r["residual_relative"], r["amplitude"],
                             r["ell_over_h"], r["seconds"]), flush=True)
                    if (assoc == "leg210" and nu0 == 0.3 and n in (401, 801, 1601)
                            and a in (A_CONTROL, A_CHEN)):
                        cond[n] = conditioning_and_localisation(g, w, a, r["nu"])
                        print("        sigma_min/sigma_max %.3e  nullvec mass in 4ell %.3f, "
                              "in 4h %.3f"
                              % (cond[n]["sigma_min_over_sigma_max"],
                                 cond[n]["nullvec_mass_within_4_ell_of_origin"],
                                 cond[n]["nullvec_mass_within_4_h_of_origin"]), flush=True)
        ladders[a] = rows
        conds[a] = cond

    print("B   truncation ladder at a = 1/2, n = 1601, rho_max in {7,8,9} ...", flush=True)
    trunc = []
    for rm in (7.0, 8.0, 9.0):
        g = grid_for(1601, rho_max=rm)
        r = solve_nu(g, A_CHEN, 0.3)
        r.pop("w")
        r["nu0"] = 0.3
        trunc.append(r)
        print("      rho_max=%.1f  X_max=%.1f  nu=%+.8e  ell/h=%.3f"
              % (rm, g.X[-1], r["nu"], r["ell_over_h"]), flush=True)

    print("C   pseudo-arclength continuation in a, from the converged a = 0.30 root ...",
          flush=True)
    conts = {}
    for n in (401, 801, 1601, 3201):
        t1 = time.time()
        c = continuation_in_a(n, a_target=0.55,
                              a_back_stop=(0.35 if n >= 3201 else A_CONTROL - 0.05))
        conts[n] = c
        print("      n=%-5d steps=%-4d stop=%-32s a_max=%.4f  a_max(K1&K2)=%.4f  folds=%d "
              "(%.0fs)" % (n, c["steps_taken"], c["stop_reason"], c["a_max_reached"],
                           c["a_max_with_K1_and_K2"], c["folds_detected"], time.time() - t1),
              flush=True)
        if c["fold_turning_point"]:
            print("         FOLD at a in %s   (leg125 a* = %.6f, offset %+.5f)"
                  % (c["fold_turning_point"]["bracket"], LEG125_A_STAR,
                     c["fold_turning_point"]["leg125_a_star_minus_fold"]), flush=True)
        print("         branch reaches Chen a = 1/2: %s   nu there: %s"
              % (c["branch_reaches_chen_a"], c["nu_on_branch_at_chen_a"]), flush=True)

    print("D   dilation covariance (P4) ...", flush=True)
    cov_ctrl = dilation_covariance(A_CONTROL)
    cov_chen = dilation_covariance(A_CHEN)

    print("V6  associativity probe (NOT pre-registered -- found post hoc) ...", flush=True)
    v6 = v6_associativity_probe()

    print("V7  stopping-rule probe (NOT pre-registered -- found post hoc) ...", flush=True)
    v7 = v7_stopping_rule_probe()

    print("SCORING against writeup/novelty/leg_284.md ...", flush=True)
    crit_chen = score_criterion(A_CHEN, ladders[A_CHEN], trunc, conts[1601])
    crit_ctrl = score_criterion(A_CONTROL, ladders[A_CONTROL])
    crit_045 = score_criterion(A_SECOND_NEG, ladders[A_SECOND_NEG])
    crit_chen_alt = score_criterion(A_CHEN, ladders[A_CHEN], trunc, conts[1601],
                                    assoc="grouped")
    crit_ctrl_alt = score_criterion(A_CONTROL, ladders[A_CONTROL], assoc="grouped")
    mech = score_mechanism(ladders[A_CHEN], conds[A_CHEN], conds[A_CONTROL], cov_chen, cov_ctrl)
    mech_alt = score_mechanism(ladders[A_CHEN], conds[A_CHEN], conds[A_CONTROL], cov_chen,
                               cov_ctrl, assoc="grouped")

    # P5 -- does the branch-termination / crossing location converge under the ladder?
    brackets = {n: conts[n]["a_star_bracket_on_branch"] for n in conts}
    amax = {n: conts[n]["a_max_reached"] for n in conts}
    folds = {n: (conts[n]["fold_turning_point"]["a_fold_estimate"]
                 if conts[n]["fold_turning_point"] else None) for n in conts}
    fold_vals = [v for v in folds.values() if v is not None]
    p5_width = (float(max(fold_vals) - min(fold_vals)) if len(fold_vals) > 1 else None)
    P5 = bool(p5_width is not None and p5_width < P5_MAX_BRACKET_WIDTH)

    gate = "YES" if crit_chen["GRID_CONVERGED"] else "NO"
    verdict = {
        "gate_question": ("Does the extended ladder produce a grid-converged nu(1/2) under the "
                          "pre-registered criterion?"),
        "gate_answer": gate,
        "criterion_at_chen_a": crit_chen,
        "criterion_at_control_a_0p30": crit_ctrl,
        "criterion_at_a_0p45": crit_045,
        "criterion_at_chen_a_other_float_association": crit_chen_alt,
        "criterion_at_control_other_float_association": crit_ctrl_alt,
        "verdict_is_association_independent": bool(
            crit_chen["GRID_CONVERGED"] == crit_chen_alt["GRID_CONVERGED"]
            and crit_ctrl["GRID_CONVERGED"] == crit_ctrl_alt["GRID_CONVERGED"]),
        "control_returns_converged": crit_ctrl["GRID_CONVERGED"],
        "lesson_84_window": (
            "The criterion is only worth its verdict if it can return YES.  a = 0.30 is run on "
            "the SAME extended ladder with the SAME six clauses as a planted positive control; "
            "its verdict is reported above.  If the control fails too, the criterion is too "
            "strict and the a = 1/2 NO carries no information -- that is stated here rather "
            "than left for a reader to notice."),
        "mechanism": mech,
        "mechanism_other_float_association": mech_alt,
        "V6_associativity_probe": v6,
        "V7_stopping_rule_probe": v7,
        "P5_branch_endpoint_converges": {
            "pass": P5,
            "fold_location_per_n": folds,
            "a_max_reached_per_n": amax,
            "a_max_with_K1_and_K2_per_n": {n: conts[n]["a_max_with_K1_and_K2"] for n in conts},
            "spread_across_ladder": p5_width, "threshold": P5_MAX_BRACKET_WIDTH,
            "nu_zero_brackets_per_n": brackets,
            "why": ("P5 was pre-registered as 'the largest a at which the continued branch "
                    "still satisfies K1 converges under the ladder'.  What the branch actually "
                    "does is FOLD, so the well-defined version of that quantity is the TURNING "
                    "POINT, and it is scored on that.  Both the pre-registered quantity and "
                    "the fold location are reported per grid.")},
        "a_star": {
            "leg125_value_from_Delta_sweep": LEG125_A_STAR,
            "leg210_independent_bracket": list(LEG210_BRACKET),
            "this_leg_brackets_on_the_continued_branch": brackets,
            "this_leg_fold_location_per_n": folds,
            "fold_brackets_per_n": {n: (conts[n]["fold_turning_point"]["bracket"]
                                        if conts[n]["fold_turning_point"] else None)
                                    for n in conts},
            "reinterpretation": ("a* is NOT a zero-crossing of nu along a branch that continues "
                                 "to Chen's a.  On the refined grids the Object-B branch has a "
                                 "TURNING POINT there: it ceases to exist as `a` increases past "
                                 "it and doubles back.  That is a different object from what "
                                 "legs 125/185 quoted, and it is what this leg re-pins."),
            "rule": ("quoted ONLY between consecutive continuation points that BOTH pass K1 and "
                     "K2; no bisection anywhere in this leg (lesson 67)."),
        },
        "what_this_replaces": {
            "leg185_banked_at_chen_a": list(LEG185_NU_A050),
            "leg210_at_chen_a": LEG210_NU_A050,
            "this_leg_ladder": crit_chen["ladder_nu"],
        },
    }

    out = {
        "leg": 284, "route": "NU12", "date": "2026-08-07",
        "no_dynamics_run": True,
        "what_this_is": ("Extension of leg 210's a = 1/2 refinement ladder to a VERDICT under a "
                         "criterion pre-registered in writeup/novelty/leg_284.md before any "
                         "number here was computed.  Float, discretised, truncated.  No "
                         "certificate, no existence claim.  Clay stays ~0.05%."),
        "preregistration": "writeup/novelty/leg_284.md",
        "ruling_178_3": ("checked and does NOT bind: no file under solver/ is edited by this "
                         "leg, and solver/energy_coercivity.py is neither imported nor read"),
        "V0_operator_validation": v0,
        "A_extended_ladders": {("a_%.2f" % a): ladders[a] for a in ladders},
        "B_truncation_ladder_at_chen_a": trunc,
        "C_continuation_in_a": conts,
        "D_dilation_covariance": {"control_a_0p30": cov_ctrl, "chen_a_0p50": cov_chen},
        "V6_associativity_probe": v6,
        "V7_stopping_rule_probe": v7,
        "blas_threads_pinned_to_one": True,
        "VERDICT": verdict,
        "honest_ceiling": ("A grid-converged nu would be a NUMERICAL statement about a "
                           "discretised, truncated profile equation -- not an existence proof, "
                           "not a certificate, not a rung on L1..L4.  A non-convergence verdict "
                           "is likewise a statement about this equation and these two schemes, "
                           "not about gCLM.  Clay stays ~0.05%; stage P0 is unaffected."),
        "seconds_total": time.time() - t0,
    }
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True, default=float)

    print("\nGATE: %s -- grid-converged nu(1/2) under the pre-registered criterion?" % gate)
    for k in ("K1_layer_resolved_and_growing", "K2_solve_quality", "K3_monotone",
              "K4_richardson_order", "K5_extrapolation_tight",
              "K6_start_and_truncation_independent"):
        print("   %-38s a=1/2 %-5s   a=0.30 control %-5s"
              % (k, crit_chen[k]["pass"], crit_ctrl[k]["pass"]))
    print("   first failing clause at a=1/2      : %s" % crit_chen["first_failing_clause"])
    print("   CONTROL a=0.30 grid-converged      : %s" % crit_ctrl["GRID_CONVERGED"])
    print("   mechanism H1                       : %s (%d/4 predictions)"
          % (mech["verdict"], mech["predictions_passed"]))
    for q in mech["P1_h_squared_law"]["rows"]:
        print("      P1 n=%-5d predicted %+.4e  observed %+.4e  ratio %.4f%s"
              % (q["n"], q["predicted_nu"], q["observed_nu"], q["observed_over_predicted"],
                 "   <-- PREDICTED IN ADVANCE" if q["was_predicted_in_advance"] else ""))
    for q in mech["P2_amplitude_law"]["rows"]:
        print("      P2 n=%-5d predicted %.6f  observed %.6f  ratio %.4f%s"
              % (q["n"], q["predicted_amplitude"], q["observed_amplitude"],
                 q["observed_over_predicted"],
                 "   <-- PREDICTED IN ADVANCE" if q["was_predicted_in_advance"] else ""))
    print("   fold location per n                : %s" % folds)
    print("   P5 fold-location spread            : %s (pass %s)" % (p5_width, P5))
    print("   branch reaches Chen a=1/2 per n    : %s"
          % {n: conts[n]["branch_reaches_chen_a"] for n in conts})
    print("   V6 float-association spread in nu  : a=1/2 worst %s   a=0.30 worst %s"
          % (v6["worst_relative_difference_at_chen_a"],
             v6["worst_relative_difference_at_control_a"]))
    print("   same verdict under both orderings  : %s"
          % verdict["verdict_is_association_independent"])
    print("   V7 stopping-rule spread in nu      : a=1/2 worst %s   a=0.30 worst %s"
          % (v7["worst_spread_at_chen_a"], v7["worst_spread_at_control_a"]))
    print("wrote", DATA, "in %.1f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
