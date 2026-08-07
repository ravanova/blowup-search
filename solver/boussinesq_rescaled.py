"""Step B of Spike 1 (PHASE2_SPIKE1_NOTES.md sec.3): the rescaled 2D Boussinesq RHS.

Built incrementally, de-risked crux-piece-first like Step A. This file starts with the
TRANSPORT operator (c_l x + u).grad f on the log-radial x angular grid -- the highest-risk
new numerical kernel of Step B (2D upwind advection on the curved, stretched grid). It is
validated standalone against a manufactured known answer (test_boussinesq_transport.py)
BEFORE it is wired into the coupled (omega, theta[, ...]) system.

FORMULATION (Chen-Hou Part I arXiv:2210.07191, transcribed):
Rescaled system, one-scale (2.10):
    omega_tau + (c_l x + u).grad omega = theta_x + c_omega omega
    theta_tau + (c_l x + u).grad theta = c_theta theta,     c_theta = c_l + 2 c_omega
    u = grad^perp (-Lap)^{-1} omega        (the Step-A velocity operator)
Normalization (2.11), enforcing frozen origin slopes (2.12) theta_xx(0), omega_x(0):
    c_l = 2 theta_xx(0)/omega_x(0),   c_omega = (1/2) c_l + u_x(0),   c_theta = c_l + 2 c_omega
Exact profile constants (2.23), the Step-C gate target:
    c_l ~ 3.006499,  c_omega ~ -1.029425,  u_x(0) ~ -2.532674,  v_x(0) = 0,
    c_l/c_omega ~ -2.920560,  alpha = c_omega/c_l ~ -0.3424.

TRANSPORT ON THE LOG-POLAR GRID (the piece built here).
The advecting field is A = (c_l x + u, c_l y + v). In polar (r, beta) with the log-radial
coordinate rho = log r (so d_r = r^{-1} d_rho), a general advection decomposes as
    A.grad f = (A_r / r) f_rho + (A_beta / r) f_beta,
with the radial/angular components of A (A_r = A.rhat, A_beta = A.betahat)
    A_r     = c_l r + u cos b + v sin b,       s_rho  := A_r/r    = c_l + (u cos b + v sin b)/r
    A_beta  =        -u sin b + v cos b,        s_beta := A_beta/r =      (v cos b - u sin b)/r.
So the transport is  s_rho f_rho + s_beta f_beta, upwinded independently in rho and beta by
the signs of s_rho, s_beta (the same 3rd-order Shu upwind stencil as Spike 0's CLM solver,
generalized to 2D). At large r, s_rho -> c_l (bounded outward dilation) -> CFL ~ drho, the
Spike-0 CFL cure; s_beta decays. At the wall beta=0, v=0 so s_beta -> 0 (no angular
advection into the wall); at the axis beta=pi/2, omega=0 by odd-x symmetry.
"""

import numpy as np

from solver.boussinesq_velocity import PolarGrid  # noqa: F401  (re-exported for Step B users)

# Exact Chen-Hou profile constants (Part I (2.23)) -- the Step-C gate target.
CL_STAR = 3.00649898
COMEGA_STAR = -1.02942516
UX0_STAR = -2.532674
CL_OVER_COMEGA_STAR = CL_STAR / COMEGA_STAR   # ~ -2.920560
ALPHA_STAR = COMEGA_STAR / CL_STAR            # ~ -0.342407


def _upwind_deriv(f, d, speed, axis):
    """3rd-order upwind-biased derivative of f along `axis` (uniform spacing d), the sign
    selected pointwise by `speed`. Generalizes Spike 0's _drho_upwind (solver/gclm_rescaled)
    to a 2D array via axis moves. `speed` broadcasts against f.

    a>0 :  f'_i = ( f_{i-2} - 6 f_{i-1} + 3 f_i + 2 f_{i+1}) / (6 d)
    a<0 :  f'_i = (-2 f_{i-1} - 3 f_i + 6 f_{i+1} -   f_{i+2}) / (6 d)
    with 2nd-order one-sided fallbacks on the two rows each stencil cannot reach (used only
    where they are the upwind side; the outermost row per side is 1st-order one-sided)."""
    g = np.moveaxis(f, axis, 0)
    sp = np.moveaxis(np.broadcast_to(speed, f.shape), axis, 0)
    n = g.shape[0]
    dfp = np.zeros_like(g)  # a>0 stencil
    dfm = np.zeros_like(g)  # a<0 stencil
    if n >= 4:
        dfp[2:n - 1] = (g[0:n - 3] - 6 * g[1:n - 2] + 3 * g[2:n - 1] + 2 * g[3:n]) / (6 * d)
        dfm[1:n - 2] = (-2 * g[0:n - 3] - 3 * g[1:n - 2] + 6 * g[2:n - 1] - g[3:n]) / (6 * d)
    # boundary fallbacks (mirror Spike 0)
    dfp[1] = (g[2] - g[0]) / (2 * d)
    dfp[n - 1] = (3 * g[n - 1] - 4 * g[n - 2] + g[n - 3]) / (2 * d)
    dfp[0] = (g[1] - g[0]) / d
    dfm[n - 2] = (g[n - 1] - g[n - 3]) / (2 * d)
    dfm[0] = (-3 * g[0] + 4 * g[1] - g[2]) / (2 * d)
    dfm[n - 1] = (g[n - 1] - g[n - 2]) / d
    out = np.where(sp >= 0.0, dfp, dfm)
    return np.moveaxis(out, 0, axis)


def advection_speeds(u, v, grid, c_l):
    """Return (s_rho, s_beta): the log-radial and angular advection speeds of the rescaled
    transport field A = (c_l x + u, c_l y + v). See module docstring for the derivation."""
    cb = np.cos(grid.B)
    sb = np.sin(grid.B)
    s_rho = c_l + (u * cb + v * sb) / grid.R
    s_beta = (v * cb - u * sb) / grid.R
    return s_rho, s_beta


def transport(f, u, v, grid, c_l):
    """(c_l x + u).grad f on the log-polar grid, upwinded in rho and beta. Returns an array
    the shape of f. This is the transport term of (2.10); the RHS negates it."""
    s_rho, s_beta = advection_speeds(u, v, grid, c_l)
    dbeta = grid.beta[1] - grid.beta[0]
    f_rho = _upwind_deriv(f, grid.drho, s_rho, axis=0)
    f_beta = _upwind_deriv(f, dbeta, s_beta, axis=1)
    return s_rho * f_rho + s_beta * f_beta


# ---------------------------------------------------------------------------------------
# Piece 2: gradient of a general grid field  (used for the velocity-gradient FIELDS u_x,
# v_x, u_y in the eta/xi reaction terms).  Central FD -- basis-agnostic, since u, v are not
# in a pure sine/cosine angular series.  2nd order; the reaction terms multiply eta, xi
# which vanish near the origin, so this precision is ample at POC level.
# ---------------------------------------------------------------------------------------

def _dbeta_central(f, dbeta):
    """d f / d beta by central differences (axis 1), 2nd-order one-sided at the beta ends."""
    g = np.empty_like(f)
    g[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2 * dbeta)
    g[:, 0] = (-3 * f[:, 0] + 4 * f[:, 1] - f[:, 2]) / (2 * dbeta)
    g[:, -1] = (3 * f[:, -1] - 4 * f[:, -2] + f[:, -3]) / (2 * dbeta)
    return g


def _drho_central(f, drho):
    """d f / d rho by central differences (axis 0), 2nd-order one-sided at the rho ends."""
    g = np.empty_like(f)
    g[1:-1, :] = (f[2:, :] - f[:-2, :]) / (2 * drho)
    g[0, :] = (-3 * f[0, :] + 4 * f[1, :] - f[2, :]) / (2 * drho)
    g[-1, :] = (3 * f[-1, :] - 4 * f[-2, :] + f[-3, :]) / (2 * drho)
    return g


def grad_xy(f, grid):
    """Cartesian gradient (f_x, f_y) of a grid field via the polar chain rule
    f_x = cos b f_r - (sin b/r) f_b,  f_y = sin b f_r + (cos b/r) f_b,  f_r = f_rho/r."""
    f_r = _drho_central(f, grid.drho) / grid.R
    f_b = _dbeta_central(f, grid.beta[1] - grid.beta[0])
    cb = np.cos(grid.B)
    sb = np.sin(grid.B)
    f_x = cb * f_r - (sb / grid.R) * f_b
    f_y = sb * f_r + (cb / grid.R) * f_b
    return f_x, f_y


# ---------------------------------------------------------------------------------------
# Piece 3: origin slope of an odd-in-x field  g ~ g_x(0) * x  near 0, and the modulation.
# g_x(0) is the LINEAR r-slope of g's leading odd angular mode cos(beta):
#     d1(r) = (4/pi) int_0^{pi/2} g cos(beta) dbeta  ~  g_x(0) * r + O(r^3).
# The decision experiment (scratchpad/decide_formulation.py) validated this as ~2x more
# accurate + noise-robust than a primitive-theta curvature read.  For c_l = 2 eta_x(0)/
# omega_x(0) the projection's quadrature bias CANCELS in the ratio (same basis both reads).
# ---------------------------------------------------------------------------------------

def odd_field_x_slope(g, grid, r_win=0.4, i_lo=3, min_points=3, max_rel_residual=0.5):
    """g_x(0) for an odd-in-x field g. Projects onto cos(beta) (axis endpoint g=0 enforced,
    wall endpoint linearly extrapolated), then fits d1 = a r + b r^3 + c r^5 over a small-r
    window and returns a. Extrapolatory (skips the innermost i_lo nodes).

    TWO GUARDS, both landed by leg 221 for mechanisms leg 205 measured and escalated without
    patching.  Neither moves a value on in-contract input; both refuse rather than fabricate.

    DEFECT A -- the fit window is REFUSED when it cannot determine the three parameters.
    The unguarded form handed a masked window straight to np.linalg.lstsq, which absorbs an
    empty (0,3) design matrix into a zero coefficient without raising or warning: leg 205
    measured exactly 0.0 against a truth of 2.0 (100% relative error, 2000x this module's own
    5e-4 acceptance tolerance), and one node against three parameters returning lstsq's
    minimum-norm solution 1.9061 (4.694e-2, 93.9x) presented as the fit.  A fabricated 0.0 is
    indistinguishable at the call site from the true statement "the origin strain vanishes".
    This is the second occurrence of the mechanism leg 99 measured in the sibling
    u_x_at_origin and leg 104 repaired THERE ONLY, at the line leg 99 named by number.
    min_points is the well-posedness floor for this three-parameter fit, not an accuracy
    guarantee; the rank returned by lstsq is checked as well, so a degenerate three-node
    configuration is still refused.

    DEFECT B -- the fit window is MEASURED IN THE FIELD'S OWN RADIAL SCALE, not in absolute
    length.  r_win = 0.4 was a hard-coded absolute length that never referenced the field it
    was fitting, and the lstsq residual that would have exposed the resulting misfit was
    discarded by the `*_`.  On a FULLY RESOLVED grid (177 window nodes, rank 3, condition
    number constant at 5.537e2 -- so the occupancy/rank guard above is provably blind to it)
    leg 205 measured a smooth in-contract field of scale 0.05 read as 0.269302 against a truth
    of 2.0 (86.5%, 1731x tolerance), and modulation()'s c_l as +0.188423 against 1.4 (same
    86.5%) when omega and eta carry different radial scales -- refuting the claim two comment
    blocks above that the projection's quadrature bias "CANCELS in the ratio", which holds
    only when the two fields share a radial scale.  The cure is leg 205's own recovery
    control read as a rule: d1 itself reports the field's scale through the radius at which
    it peaks (for the d1 = a r exp(-lam r^2) class the module is validated on, r_peak =
    1/sqrt(2 lam), so sqrt(2) r_peak is the envelope scale 1/sqrt(lam)), and the fit is
    restricted to the inner HALF of that scale, where the (r, r^3, r^5) truncation is
    controlled.  This heuristic is EXACT for the single-scale class just named and is NOT
    claimed beyond it: leg 221 measured a two-scale field, r cos(b) [exp(-r^2) +
    exp(-400 r^2)], read as 1.135121 against a truth of 2.0 (43.2%, 86x tolerance) -- the peak
    resolves to the OUTER scale, the cap goes non-binding, and the inner scale is never
    resolved.  That case is outside leg 205's battery and outside this leg's gate; it is
    banked with its magnitude in writeup/data/p2_route_bvrr_v1_repair.json's
    `residual_margin_probe` and handed to the postrepair-verification leg.  The cap is
    one-sided: it can only SHRINK the caller's window, never widen it,
    and it is non-binding at and above the scale the module's own gate validates -- so on
    in-contract input `min` returns the caller's r_win as the identical float and the fit is
    bit-identical.  The discarded residual is then kept as a fit-quality backstop -- a PARTIAL
    one, not a catch-all for every shape the peak heuristic does not describe: the two-scale
    field above sits at a relative residual of 8.1e-2, well under the threshold below, so the
    backstop does not fire on it.  max_rel_residual = 0.5 is set from the measured
    evidence set, not tuned: the worst legitimate in-repository fit is 4.4e-3 (Step-C's
    `profile_ansatz` omega read, the field every banked relaxation runs on), the worst
    precondition-violating field any harness in this repository feeds it is 0.147 (leg 81's
    constant marker field, whose returned value is never recorded), and leg 205's headline
    fabrication sat at 8.6e-1.  The backstop is deliberately the looser of the two guards --
    the window cap is what closes the measured mechanism.

    Raises ValueError if the window holds fewer than min_points nodes, if the fit is
    rank-deficient, or if the relative least-squares residual exceeds max_rel_residual."""
    beta = grid.beta
    dbeta = beta[1] - beta[0]
    cb = np.cos(beta)
    # trapezoid over [0, pi/2] with synthesized endpoints: axis (beta=pi/2) g=0 for odd g;
    # wall (beta=0) linear extrapolation from the two nearest interior nodes.
    g_wall = 2 * g[:, 0] - g[:, 1]           # (n_r,)
    integrand = g * cb[None, :]              # interior
    wall_term = g_wall * np.cos(0.0)
    axis_term = 0.0                          # g(pi/2)=0, cos(pi/2)=0 anyway
    # trapezoid: interior sum + endpoint half-panels
    interior = np.trapezoid(integrand, beta, axis=1)
    d1 = (4.0 / np.pi) * (interior
                          + 0.5 * dbeta * (wall_term + integrand[:, 0])
                          + 0.5 * dbeta * (integrand[:, -1] + axis_term))
    r = grid.r
    live = np.arange(len(r)) >= i_lo

    # DEFECT B: size the window from the field's own radial scale, one-sided (shrink only).
    a1 = np.where(live, np.abs(d1), 0.0)
    peak = float(np.max(a1)) if a1.size else 0.0
    if np.isfinite(peak) and peak > 0.0:
        # The peak is taken at the OUTERMOST radius attaining it, not the innermost. The
        # cap must bind only when d1 genuinely concentrates inside the window, so a tie or
        # a flat run -- a d1 that does not decay at all, e.g. the constant marker fields
        # leg 81's status audit drives run() with -- has to resolve OUTWARD, the direction
        # in which the cap is non-binding and nothing moves. Resolving inward would shrink
        # the window on a field that has no small scale, which is a fabrication of the
        # opposite sign to the one being repaired.
        i_peak = int(len(a1) - 1 - np.argmax(a1[::-1]))
        r_scale = np.sqrt(2.0) * float(r[i_peak])
        r_win_eff = min(float(r_win), 0.5 * r_scale)
    else:
        r_scale = np.inf          # d1 vanishes (or is non-finite): no scale to read
        r_win_eff = float(r_win)

    m = live & (r < r_win_eff)

    # DEFECT A: refuse an under-determined window instead of letting lstsq fabricate a value.
    n_in = int(m.sum())
    min_points = max(int(min_points), 3)
    if n_in < min_points:
        raise ValueError(
            f"odd_field_x_slope: the origin fit window (r in "
            f"({r[min(i_lo, len(r) - 1)]:.6g}, "
            f"{r_win_eff:.6g})) holds {n_in} of {len(r)} radial nodes, fewer than the "
            f"{min_points} required for the three-parameter (r, r^3, r^5) fit. "
            f"r_win={r_win:.6g} was capped to {r_win_eff:.6g} by the field's own radial "
            f"scale {r_scale:.6g}; refine the radial grid, lower r_min, or pass a field "
            f"whose scale this grid resolves. Fitting anyway would return a fabricated "
            f"finite value (leg 205 measured exactly 0.0 against a truth of 2.0).")

    A = np.vstack([r[m], r[m] ** 3, r[m] ** 5]).T
    coef, res, rank, _sv = np.linalg.lstsq(A, d1[m], rcond=None)
    if rank < A.shape[1]:
        raise ValueError(
            f"odd_field_x_slope: the origin fit is rank-deficient (rank {rank} < "
            f"{A.shape[1]} parameters) over {n_in} in-window node(s). lstsq would return "
            f"the minimum-norm solution, which is not the extrapolated d1'(0).")

    # DEFECT B, backstop: the residual lstsq already computed, no longer discarded.
    nrm = float(np.linalg.norm(d1[m]))
    rel_res = float(np.sqrt(res[0]) / nrm) if (np.size(res) and nrm > 0.0) else 0.0
    if rel_res > max_rel_residual:
        raise ValueError(
            f"odd_field_x_slope: the (r, r^3, r^5) basis does not represent d1 over the fit "
            f"window (r < {r_win_eff:.6g}): relative least-squares residual {rel_res:.4g} "
            f"exceeds max_rel_residual={max_rel_residual:.4g} over {n_in} nodes. The "
            f"returned slope would be a finite plausible wrong number (leg 205 measured "
            f"0.269302 against a truth of 2.0 at a discarded residual of 8.6e-1).")

    return float(coef[0])


def modulation(omega, eta, phi, grid):
    """Compute (c_l, c_omega, c_theta) from the normalization (2.11)/(2.12):
        c_l = 2 eta_x(0)/omega_x(0),  c_omega = c_l/2 + u_x(0),  c_theta = c_l + 2 c_omega.
    u_x(0) comes from the Step-A mode-localized phi read (u_x_at_origin)."""
    from solver.boussinesq_velocity import u_x_at_origin
    wx0 = odd_field_x_slope(omega, grid)
    ex0 = odd_field_x_slope(eta, grid)
    ux0 = u_x_at_origin(phi, grid)
    c_l = 2.0 * ex0 / wx0
    c_omega = 0.5 * c_l + ux0
    c_theta = c_l + 2.0 * c_omega
    return c_l, c_omega, c_theta, dict(omega_x0=wx0, eta_x0=ex0, u_x0=ux0)


# ---------------------------------------------------------------------------------------
# Piece 4: the coupled rescaled integrator.  Fields (omega, eta=theta_x, xi=theta_y) on the
# log-polar grid; RHS (2.10)/(2.28), modulation (2.11), SSPRK3 in tau.  A steady state is a
# self-similar profile -- Step C relaxes to the Chen-Hou one (the gate).
#
#   omega_tau = -(c_l x+u).grad omega + eta + c_omega omega
#   eta_tau   = -(c_l x+u).grad eta   + (2 c_omega - u_x) eta - v_x xi
#   xi_tau    = -(c_l x+u).grad xi    + (2 c_omega + u_x) xi  - u_y eta   (v_y = -u_x used)
# ---------------------------------------------------------------------------------------

from solver.boussinesq_velocity import velocity_from_vorticity


class RescaledBoussinesq:
    """Dynamic-rescaling integrator for 2D Boussinesq in the Hou-Luo geometry, on a fixed
    log-polar grid.  Wires the Step-A velocity operator into the rescaled (omega, eta, xi)
    system with the (2.11) modulation."""

    def __init__(self, grid):
        self.grid = grid
        self.dbeta = grid.beta[1] - grid.beta[0]

    def velocity_and_grads(self, omega):
        u, v, phi = velocity_from_vorticity(omega, self.grid, radial_bc="robin")
        u_x, u_y = grad_xy(u, self.grid)
        v_x, _ = grad_xy(v, self.grid)
        return u, v, phi, u_x, u_y, v_x

    def rhs(self, omega, eta, xi):
        """Return (R_omega, R_eta, R_xi, info). info carries c_l, c_omega, c_theta, the
        origin reads, and the max advection speeds (for CFL)."""
        g = self.grid
        u, v, phi, u_x, u_y, v_x = self.velocity_and_grads(omega)
        c_l, c_omega, c_theta, reads = modulation(omega, eta, phi, g)
        s_rho, s_beta = advection_speeds(u, v, g, c_l)
        T_om = transport(omega, u, v, g, c_l)
        T_et = transport(eta, u, v, g, c_l)
        T_xi = transport(xi, u, v, g, c_l)
        R_om = -T_om + eta + c_omega * omega
        R_et = -T_et + (2.0 * c_omega - u_x) * eta - v_x * xi
        R_xi = -T_xi + (2.0 * c_omega + u_x) * xi - u_y * eta
        cfl_speed = np.max(np.abs(s_rho)) / g.drho + np.max(np.abs(s_beta)) / self.dbeta
        info = dict(c_l=c_l, c_omega=c_omega, c_theta=c_theta, cfl_speed=cfl_speed, **reads)
        return R_om, R_et, R_xi, info

    def step(self, omega, eta, xi, dt):
        """One SSPRK3 (Shu-Osher) step on the triple. Returns (om, et, xi, info, res)."""
        R0o, R0e, R0x, info = self.rhs(omega, eta, xi)
        o1, e1, x1 = omega + dt * R0o, eta + dt * R0e, xi + dt * R0x
        R1o, R1e, R1x, _ = self.rhs(o1, e1, x1)
        o2 = 0.75 * omega + 0.25 * (o1 + dt * R1o)
        e2 = 0.75 * eta + 0.25 * (e1 + dt * R1e)
        x2 = 0.75 * xi + 0.25 * (x1 + dt * R1x)
        R2o, R2e, R2x, _ = self.rhs(o2, e2, x2)
        on = (1 / 3) * omega + (2 / 3) * (o2 + dt * R2o)
        en = (1 / 3) * eta + (2 / 3) * (e2 + dt * R2e)
        xn = (1 / 3) * xi + (2 / 3) * (x2 + dt * R2x)
        res = max(np.abs(R0o).max(), np.abs(R0e).max(), np.abs(R0x).max())
        return on, en, xn, info, res

    def run(self, omega0, eta0, xi0, dt_frac=0.3, tol=1e-6, max_steps=50000, verbose=False,
            renorm=False):
        """Evolve (omega, eta, xi) toward a steady state (||RHS||_inf < tol) with a per-step
        advective-CFL dt. Returns a result dict with histories of c_l, c_omega, residual.

        renorm=True discretely ENFORCES the normalization (2.12): after each step it rescales
        omega, eta (and xi with eta's factor) to re-pin omega_x(0), eta_x(0) at their INITIAL
        values -- so c_l = 2 eta_x(0)/omega_x(0) is held fixed regardless of the near-origin
        truncation slip that otherwise makes it drift (diagnosed in experiments/). A weak
        restoring correction (factors ~1); the paper's continuous (2.12) is the exact analogue.
        """
        om, et, xi = (np.array(a, float) for a in (omega0, eta0, xi0))
        wx0_target = odd_field_x_slope(om, self.grid)
        ex0_target = odd_field_x_slope(et, self.grid)
        cl_h, cw_h, res_h, tau_h = [], [], [], []
        tau, res = 0.0, np.inf
        info = {}
        for step in range(max_steps):
            _, _, _, info0 = self.rhs(om, et, xi)
            dt = dt_frac / info0["cfl_speed"]
            om, et, xi, info, res = self.step(om, et, xi, dt)
            if renorm:
                fw = wx0_target / odd_field_x_slope(om, self.grid)
                fe = ex0_target / odd_field_x_slope(et, self.grid)
                om *= fw
                et *= fe
                xi *= fe
            tau += dt
            cl_h.append(info["c_l"]); cw_h.append(info["c_omega"])
            res_h.append(res); tau_h.append(tau)
            if verbose and step % 500 == 0:
                print(f"    step {step:6d} tau={tau:8.3f} c_l={info['c_l']:+.5f} "
                      f"c_om={info['c_omega']:+.5f} res={res:.2e}")
            if res < tol:
                break
            if not np.isfinite(res) or res > 1e8:
                break
        return dict(omega=om, eta=et, xi=xi, c_l=info.get("c_l", np.nan),
                    c_omega=info.get("c_omega", np.nan), residual=res, tau=tau,
                    steps=step + 1, converged=res < tol,
                    cl_hist=np.array(cl_h), cw_hist=np.array(cw_h),
                    res_hist=np.array(res_h), tau_hist=np.array(tau_h))
