"""DECISION EXPERIMENT for Spike-1 Step B: which evolved-variable formulation?

The modulation (2.11) origin reads are the crux. Compare, against a MANUFACTURED profile
with KNOWN origin derivatives, how cleanly theta_xx(0) is recovered:

  Option 2/3 (track eta = theta_x):  theta_xx(0) = eta_x(0), a LINEAR r-slope of eta's
     single odd angular mode cos(beta).  [same read class as omega_x(0) and Step-A u_x(0)]
  Option 1 (track primitive theta):  theta_xx(0) from the r^2-CURVATURE of theta's even
     modes -- the cos(2beta) mode gives only (theta_xx - theta_yy); recovering theta_xx
     needs a second (constant-mode) r^2 read plus a theta(0,0) subtraction.

Manufactured (parities respected, smooth, decaying):
  theta = (t0 + p x^2 + q y^2) e^{-r^2}   (even in x)
     => near 0: theta ~ t0 + (p-t0) x^2 + (q-t0) y^2, so
        theta_xx(0) = 2(p-t0),  theta_yy(0) = 2(q-t0)
  eta = theta_x = 2x e^{-r^2} [p - (t0 + p x^2 + q y^2)]   (odd in x), eta_x(0)=2(p-t0)
  omega = wx0 * x e^{-r^2}   (odd in x),  omega_x(0)=wx0

Reads use trapezoid angular projections on the interior beta-grid and a small-r fit window.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.boussinesq_velocity import PolarGrid  # noqa: E402

# --- manufactured constants ---
T0, P, Q, WX0 = 0.3, 1.7, -0.9, -2.1
THXX_TRUE = 2 * (P - T0)   # theta_xx(0)
THYY_TRUE = 2 * (Q - T0)   # theta_yy(0)


def fields(grid):
    x, y, r = grid.X, grid.Y, grid.R
    e = np.exp(-(r**2))
    theta = (T0 + P * x**2 + Q * y**2) * e
    eta = 2 * x * e * (P - (T0 + P * x**2 + Q * y**2))   # = theta_x
    omega = WX0 * x * e
    return omega, theta, eta


def _proj(f, ang, grid, norm):
    """(norm/pi)*int_0^{pi/2} f(r,.) ang(beta) dbeta  per radius, trapezoid on interior grid.
    We append the analytic boundary behavior via simple edge handling: interior-only trapezoid
    is enough since the integrand is smooth and we only need small-r scaling."""
    w = np.trapezoid(f * ang[None, :], grid.beta, axis=1)
    return (norm / np.pi) * w


def read_eta_slope(eta, grid, rlo_idx=3, r_win=0.4):
    """theta_xx(0) = eta_x(0): d1(r) = (4/pi) int eta cos(beta) dbeta ~ eta_x(0) r + O(r^3).
    Fit odd polynomial d1 = a r + b r^3 (+ c r^5), take a = eta_x(0)."""
    cb = np.cos(grid.beta)
    d1 = _proj(eta, cb, grid, 4.0)
    r = grid.r
    m = (np.arange(len(r)) >= rlo_idx) & (r < r_win)
    A = np.vstack([r[m], r[m] ** 3, r[m] ** 5]).T
    coef, *_ = np.linalg.lstsq(A, d1[m], rcond=None)
    return float(coef[0])


def read_theta_curv(theta, grid, rlo_idx=3, r_win=0.4):
    """theta_xx(0) from primitive theta via two r^2 curvature reads:
       c0(r) = (2/pi) int theta dbeta        ~ t0 + (r^2/4)(theta_xx+theta_yy)
       c1(r) = (4/pi) int theta cos2beta db  ~      (r^2/4)(theta_xx-theta_yy)
       => theta_xx = 2*(A + B) with c0 = t0 + A r^2, c1 = B r^2."""
    r = grid.r
    c0 = _proj(theta, np.ones_like(grid.beta), grid, 2.0)
    c1 = _proj(theta, np.cos(2 * grid.beta), grid, 4.0)
    m = (np.arange(len(r)) >= rlo_idx) & (r < r_win)
    # c0 = t0 + A r^2 + A2 r^4  (even; fit intercept + r^2 + r^4)
    M0 = np.vstack([np.ones(m.sum()), r[m] ** 2, r[m] ** 4]).T
    coef0, *_ = np.linalg.lstsq(M0, c0[m], rcond=None)
    A = coef0[1]
    # c1 = B r^2 + B2 r^4  (no constant: c1(0)=0 by parity)
    M1 = np.vstack([r[m] ** 2, r[m] ** 4]).T
    coef1, *_ = np.linalg.lstsq(M1, c1[m], rcond=None)
    B = coef1[0]
    return 2.0 * (A + B)


print(f"TRUE theta_xx(0) = {THXX_TRUE:.6f}   (theta_yy(0) = {THYY_TRUE:.6f})\n")
print(f"{'n_r':>6} {'n_b':>4} | {'eta-slope (opt2/3)':>20} {'err':>10} | {'theta-curv (opt1)':>18} {'err':>10}")
for n_r, n_b in [(300, 48), (600, 64), (1200, 96)]:
    grid = PolarGrid(n_r=n_r, n_beta=n_b, r_min=1e-3, r_max=20.0)
    omega, theta, eta = fields(grid)
    e_read = read_eta_slope(eta, grid)
    t_read = read_theta_curv(theta, grid)
    e_err = abs(e_read - THXX_TRUE) / abs(THXX_TRUE)
    t_err = abs(t_read - THXX_TRUE) / abs(THXX_TRUE)
    print(f"{n_r:>6} {n_b:>4} | {e_read:>20.6f} {e_err:>10.2e} | {t_read:>18.6f} {t_err:>10.2e}")

# sensitivity: add small grid-scale noise, see which read degrades (Spike-0 noise-amp lesson)
print("\n--- sensitivity to 1e-3 relative grid-scale noise (10 trials) ---")
rng = np.random.RandomState(0)
grid = PolarGrid(n_r=600, n_beta=64, r_min=1e-3, r_max=20.0)
omega, theta, eta = fields(grid)
amp_t = np.max(np.abs(theta))
amp_e = np.max(np.abs(eta))
e_errs, t_errs = [], []
for _ in range(10):
    tn = theta + 1e-3 * amp_t * rng.standard_normal(theta.shape)
    en = eta + 1e-3 * amp_e * rng.standard_normal(eta.shape)
    e_errs.append(abs(read_eta_slope(en, grid) - THXX_TRUE) / abs(THXX_TRUE))
    t_errs.append(abs(read_theta_curv(tn, grid) - THXX_TRUE) / abs(THXX_TRUE))
print(f"eta-slope  (opt2/3): mean err {np.mean(e_errs):.2e}  worst {np.max(e_errs):.2e}")
print(f"theta-curv (opt1)  : mean err {np.mean(t_errs):.2e}  worst {np.max(t_errs):.2e}")
