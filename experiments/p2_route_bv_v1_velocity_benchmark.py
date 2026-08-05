"""Route-BV v1 (leg 73): the FIRST EXTERNAL known-answer check for solver/boussinesq_velocity.py.

    .venv/bin/python -u experiments/p2_route_bv_v1_velocity_benchmark.py

Writes writeup/data/p2_route_bv_v1_velocity_benchmark.json.  Runtime ~2 min.

WHY THIS EXISTS
---------------
capabilities.py records this module's validated line as "manufactured stream-function
solutions; the Route-L line sweep is gated to 9.5e-16 against the operator it inverts".
Both are INTERNAL: a manufactured solution picks phi and differentiates to get omega, and
the line sweep is checked against the operator it inverts.  Neither has ever been scored
against a number somebody else published.  This runner does that.

THE BENCHMARK (see writeup/novelty/leg_73.md for the literature pass and the pre-commitment)
-------------------------------------------------------------------------------------------
Two published closed forms, assembled:

  (1) The LAMB-OSEEN vortex.  Prescribed Gaussian vorticity
          omega_O(R) = (Gamma / (pi d^2)) exp(-R^2/d^2),
      whose published velocity is  v_theta(R) = (Gamma / (2 pi R)) (1 - exp(-R^2/d^2)),
      and whose stream function (-Lap psi = omega_O) is, in closed form,
          psi_O(R) = -(Gamma/4pi) [ ln(R^2/d^2) + E_1(R^2/d^2) + gamma_E ].
      This is the exact inverse of a manufactured solution: omega is given, phi is the
      consequence.  It is the standard first verification case for Biot-Savart/Poisson
      solvers.

  (2) The CLASSICAL CORNER IMAGE SYSTEM (Lamb, Hydrodynamics Art. 155; Greenhill 1878;
      restated in Crosby-Johnson-Morrison, Phys. Fluids 25 (2013), sec. IV eq. (14)).  A
      vortex at (a,b) in the quarter plane with phi = 0 on BOTH rays has three images,
          (-a, b) : -Gamma,   (a, -b) : -Gamma,   (-a, -b) : +Gamma,
      and the induced velocity AT THE VORTEX is the published closed form (point-vortex
      limit, with u = -phi_y, v = phi_x and -Lap phi = omega):
          u_img = (Gamma/4pi) [ -1/b + b/(a^2+b^2) ],
          v_img = (Gamma/4pi) [  1/a - a/(a^2+b^2) ],
      whose orbit invariant is Lamb's  a^{-2} + b^{-2} = const  (verified analytically in
      check_invariant() below).  For a FINITE Oseen core each image term carries the exact
      factor (1 - exp(-R_i^2/d^2)); we use the finite-core form as ground truth and REPORT
      the size of the point-vortex correction rather than hiding it.

Why this is external and not another manufactured solution:
  * omega is prescribed; phi is never reverse-engineered from a chosen phi.
  * The target number is a DIFFERENCE of image contributions.  It exists only because of the
    two Dirichlet rays, so a manufactured solution with hand-imposed Dirichlet data cannot
    test it.
  * The four-vortex system has ZERO net circulation, so its far field is a quadrupole and
    each angular mode n decays as r^{-2n} -- exactly what radial_bc="robin" imposes.  The
    headline number therefore puts the far-field closure under test.  radial_bc="dirichlet",
    which is HANDED the answer at both radial ends, is used only as a labelled control.

PRE-COMMITTED TOLERANCES (fixed in writeup/novelty/leg_73.md, committed BEFORE this file)
  P1  ||u_num - u_exact|| / ||u_exact|| at the blob centre  <= 1e-2  at the finest level.
  P2  that error decreases monotonically, observed order    >= 1.5.
  P3  relative L2 error of phi over r in [0.1, 10]          <= 1e-3  at the finest level.
Reading rule: P1/P3 are ACCURACY, P2 is CORRECTNESS.  A P1/P3 miss with P2 holding is a
resolution finding.  A P2 failure is the gate's "disagrees" branch -> escalate, do not patch.

This runner READS solver/boussinesq_velocity.py and edits nothing under any outcome.
"""

import json
import sys
from os.path import abspath, dirname

import numpy as np

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from solver.boussinesq_velocity import (PolarGrid, poisson_solve,  # noqa: E402
                                        velocity_from_vorticity)

OUT = (dirname(dirname(abspath(__file__)))
       + "/writeup/data/p2_route_bv_v1_velocity_benchmark.json")

EULER_GAMMA = 0.57721566490153286060651209008240243104215933593992

# ---- the benchmark configuration, pre-committed in writeup/novelty/leg_73.md -------------
GAMMA = 1.0                 # circulation of the physical blob
D_CORE = 0.25               # Oseen core radius
R0 = 1.0                    # blob sits at radius 1 -> exactly on the rho = 0 node
BETA_FRAC = 0.7             # blob angle = BETA_FRAC * (pi/2); 0.7 = 7/10 lands on a node
R_MIN, R_MAX = 1e-3, 1e3
LADDER = ((601, 49), (1201, 99), (2401, 199))
FIELD_WINDOW = (0.1, 10.0)  # radial window for the P3 field norm

# P1 / P2 / P3, restated in code so the JSON carries them next to the results.
P1_TOL = 1e-2
P2_MIN_ORDER = 1.5
P3_TOL = 1e-3


# ---------------------------------------------------------------------------------------
# E_1, hand-rolled: this repository ships no scipy (see solver/interval.py's same policy).
# Numerical-Recipes expint(1, x): power series for x <= 1, modified Lentz continued
# fraction for x > 1.  Validated against published reference values in check_exp1().
# ---------------------------------------------------------------------------------------
def exp1(x):
    """E_1(x) = int_x^inf e^{-t}/t dt, for x > 0.  Vectorised, ~1e-15 relative."""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)

    small = x <= 1.0
    if np.any(small):
        xs = x[small]
        ans = -np.log(xs) - EULER_GAMMA
        fact = np.ones_like(xs)
        for i in range(1, 200):
            fact = fact * (-xs) / i
            delta = -fact / i
            ans = ans + delta
            if np.all(np.abs(delta) <= 1e-18 * np.abs(ans)):
                break
        out[small] = ans

    big = ~small
    if np.any(big):
        xb = x[big]
        tiny = 1e-300
        b = xb + 1.0
        c = np.full_like(xb, 1.0 / tiny)
        d = 1.0 / b
        h = d.copy()
        for i in range(1, 400):
            a = -float(i * i)
            b = b + 2.0
            d = 1.0 / (a * d + b)
            c = b + a / c
            delta = c * d
            h = h * delta
            if np.all(np.abs(delta - 1.0) <= 1e-17):
                break
        # exp(-x) underflows to 0 for x beyond ~745, which is the correct limit for E_1.
        out[big] = h * np.exp(-xb)

    return out


def _exp1_reference(xs):
    """E_1 by an INDEPENDENT route: Gauss-Laguerre on E_1(x) = e^{-x} int_0^inf e^{-s}/(x+s) ds
    for x >= 1, and Gauss-Legendre on int_x^1 e^{-t}/t dt + E_1(1) for x < 1.  Shares no code
    path with exp1(), so agreement is evidence and not a tautology."""
    xl, wl = np.polynomial.laguerre.laggauss(80)
    xg, wg = np.polynomial.legendre.leggauss(200)
    e1_at_1 = float(np.exp(-1.0) * np.sum(wl / (1.0 + xl)))
    out = []
    for X in xs:
        if X >= 1.0:
            out.append(float(np.exp(-X) * np.sum(wl / (X + xl))))
        else:
            t = 0.5 * (1.0 - X) * xg + 0.5 * (1.0 + X)
            w = 0.5 * (1.0 - X) * wg
            out.append(float(np.sum(w * np.exp(-t) / t) + e1_at_1))
    return np.array(out)


def check_exp1():
    """Score exp1 two ways: against published tabulated values of E_1 (Abramowitz & Stegun
    5.1.53 / DLMF sec. 6), and against the independent quadrature above.  Returns the worst
    relative error of each."""
    ref = {
        0.01: 4.037929576537837,
        0.1: 1.8229239584193906,
        0.5: 0.5597735947761608,
        1.0: 0.21938393439552029,
        2.0: 0.04890051070806112,
        5.0: 1.1482955912753e-3,
        10.0: 4.156968929685324e-6,
        20.0: 9.83552529065e-11,
    }
    xs = np.array(sorted(ref))
    got = exp1(xs)
    want = np.array([ref[float(v)] for v in xs])
    rel = np.abs(got - want) / np.abs(want)
    quad = _exp1_reference(xs)
    rel_q = np.abs(got - quad) / np.abs(quad)
    return {"max_rel_err": float(rel.max()),
            "max_rel_err_vs_independent_quadrature": float(rel_q.max()),
            "per_point": {str(float(v)): float(e) for v, e in zip(xs, rel)}}


# ---------------------------------------------------------------------------------------
# The exact four-blob solution
# ---------------------------------------------------------------------------------------
def images(a, b):
    """The physical blob plus Lamb's three corner images: (position, sign)."""
    return (((a, b), +1.0), ((-a, b), -1.0), ((a, -b), -1.0), ((-a, -b), +1.0))


def exact_vorticity(X, Y, a, b, gamma=GAMMA, d=D_CORE):
    """omega = sum of the four Oseen blobs, restricted to the quarter plane.

    Including the three (exponentially small) image tails makes the benchmark EXACT rather
    than approximate: the four-blob phi below is then the exact solution of the BVP the
    solver is actually handed."""
    w = np.zeros_like(X)
    for (px, py), s in images(a, b):
        r2 = (X - px) ** 2 + (Y - py) ** 2
        w = w + s * (gamma / (np.pi * d * d)) * np.exp(-r2 / (d * d))
    return w


def _psi_oseen(r2, gamma=GAMMA, d=D_CORE):
    """psi_O with -Lap psi_O = omega_O: -(Gamma/4pi)[ln t + E_1(t) + gamma_E], t = R^2/d^2.

    The additive constant and the d^2 inside the log both cancel in the four-blob sum
    (the signs total zero), so no gauge choice enters the comparison."""
    t = np.maximum(r2 / (d * d), 1e-300)
    return -(gamma / (4.0 * np.pi)) * (np.log(t) + exp1(t) + EULER_GAMMA)


def exact_phi(X, Y, a, b, gamma=GAMMA, d=D_CORE):
    """The exact stream function: phi = 0 on both rays by the odd-odd image symmetry."""
    phi = np.zeros_like(X)
    for (px, py), s in images(a, b):
        phi = phi + s * _psi_oseen((X - px) ** 2 + (Y - py) ** 2, gamma, d)
    return phi


def exact_velocity(X, Y, a, b, gamma=GAMMA, d=D_CORE):
    """u = -phi_y, v = phi_x for the four-blob field, in closed form.

    Per blob, |grad psi_O| = (Gamma/2 pi R)(1 - e^{-R^2/d^2}) -- the published Lamb-Oseen
    azimuthal velocity -- so
        u_i = +s_i K_i (y - y_i),  v_i = -s_i K_i (x - x_i),
        K_i = (Gamma/2pi) (1 - e^{-R_i^2/d^2}) / R_i^2,
    which is regular as R_i -> 0 (K_i -> Gamma/(2 pi d^2))."""
    u = np.zeros_like(X)
    v = np.zeros_like(X)
    for (px, py), s in images(a, b):
        dx, dy = X - px, Y - py
        r2 = dx * dx + dy * dy
        t = r2 / (d * d)
        # (1 - e^{-t})/r2 = (1 - e^{-t})/(t d^2); use expm1 for the small-t cancellation.
        k = (gamma / (2.0 * np.pi)) * np.where(
            t > 1e-8, -np.expm1(-t) / np.maximum(r2, 1e-300), 1.0 / (d * d))
        u = u + s * k * dy
        v = v - s * k * dx
    return u, v


def image_velocity_at_vortex(a, b, gamma=GAMMA, d=D_CORE):
    """The published corner-image velocity AT the vortex: the three image terms only (the
    blob's self-field vanishes at its own centre by radial symmetry).

    Returns (u, v) for the finite Oseen core, and (u, v) for the point-vortex limit -- the
    textbook closed form  u = (G/4pi)[-1/b + b/(a^2+b^2)],  v = (G/4pi)[1/a - a/(a^2+b^2)]."""
    u = v = 0.0
    for (px, py), s in images(a, b)[1:]:
        dx, dy = a - px, b - py
        r2 = dx * dx + dy * dy
        k = (gamma / (2.0 * np.pi)) * (-np.expm1(-r2 / (d * d))) / r2
        u += s * k * dy
        v -= s * k * dx
    g4 = gamma / (4.0 * np.pi)
    u_pt = g4 * (-1.0 / b + b / (a * a + b * b))
    v_pt = g4 * (1.0 / a - a / (a * a + b * b))
    return (float(u), float(v)), (float(u_pt), float(v_pt))


def check_invariant(a, b, gamma=GAMMA):
    """Lamb's corner orbit invariant: d/dt (a^-2 + b^-2) = 0 under the point-vortex image
    velocity.  Confirms the closed form we score against is the published one, not a
    lookalike.  Returns the residual, which should be at round-off."""
    g4 = gamma / (4.0 * np.pi)
    adot = g4 * (-1.0 / b + b / (a * a + b * b))
    bdot = g4 * (1.0 / a - a / (a * a + b * b))
    return float(-2.0 * adot / a ** 3 - 2.0 * bdot / b ** 3)


# ---------------------------------------------------------------------------------------
# One rung of the ladder
# ---------------------------------------------------------------------------------------
def run_level(n_r, n_beta, radial_bc="robin", r_min=R_MIN, r_max=R_MAX, window=None):
    grid = PolarGrid(n_r=n_r, n_beta=n_beta, r_min=r_min, r_max=r_max)
    if window is None:
        window = FIELD_WINDOW

    # The blob centre must land EXACTLY on a node, so no interpolation enters the headline.
    i0 = int(np.argmin(np.abs(grid.rho - np.log(R0))))
    M = grid.M
    j_target = BETA_FRAC * M                      # beta_j = (pi/2) j / M
    j0 = int(round(j_target)) - 1                 # grid.beta is indexed from j = 1
    r_node = float(grid.r[i0])
    beta_node = float(grid.beta[j0])
    a = r_node * np.cos(beta_node)
    b = r_node * np.sin(beta_node)
    node_offset = {"rho": float(abs(grid.rho[i0] - np.log(R0))),
                   "beta": float(abs(beta_node - BETA_FRAC * np.pi / 2.0))}

    omega = exact_vorticity(grid.X, grid.Y, a, b)
    phi_ex = exact_phi(grid.X, grid.Y, a, b)
    u_ex_f, v_ex_f = exact_velocity(grid.X, grid.Y, a, b)

    u, v, phi = velocity_from_vorticity(
        omega, grid, radial_bc=radial_bc,
        phi_exact=(phi_ex if radial_bc == "dirichlet" else None))

    # -- P1: the velocity at the blob centre vs the published corner-image closed form ----
    (ux, vx), (ux_pt, vx_pt) = image_velocity_at_vortex(a, b)
    un, vn = float(u[i0, j0]), float(v[i0, j0])
    norm_ex = float(np.hypot(ux, vx))
    err_vec = float(np.hypot(un - ux, vn - vx))
    p1_rel = err_vec / norm_ex

    # -- P3: the field norm over the window --------------------------------------------
    win = (grid.r >= window[0]) & (grid.r <= window[1])
    dphi = (phi - phi_ex)[win, :]
    p3_rel = float(np.linalg.norm(dphi) / np.linalg.norm(phi_ex[win, :]))
    du, dv = (u - u_ex_f)[win, :], (v - v_ex_f)[win, :]
    vel_rel = float(np.sqrt(np.sum(du ** 2 + dv ** 2)
                            / np.sum(u_ex_f[win, :] ** 2 + v_ex_f[win, :] ** 2)))

    return {
        "n_r": n_r, "n_beta": n_beta, "radial_bc": radial_bc,
        "r_min": float(r_min), "r_max": float(r_max), "window": list(window),
        "drho": float(grid.drho), "dbeta": float(np.pi / (2.0 * M)),
        "pts_across_core_rho": float(D_CORE / grid.drho),
        "pts_across_core_beta": float((D_CORE / r_node) / (np.pi / (2.0 * M))),
        "blob": {"r": r_node, "beta": beta_node, "a": float(a), "b": float(b),
                 "node_offset": node_offset},
        "u_numeric": un, "v_numeric": vn,
        "u_exact_finite_core": ux, "v_exact_finite_core": vx,
        "u_exact_point_vortex": ux_pt, "v_exact_point_vortex": vx_pt,
        "finite_core_correction_rel": float(np.hypot(ux - ux_pt, vx - vx_pt) / norm_ex),
        "abs_err_vec": err_vec,
        "p1_rel_err_centre_velocity": p1_rel,
        "p3_rel_l2_phi_window": p3_rel,
        "rel_l2_velocity_window": vel_rel,
    }


def observed_order(errs):
    """Refinement factor is 2 per rung, so order = log2(e_coarse / e_fine)."""
    return [float(np.log2(errs[i] / errs[i + 1])) for i in range(len(errs) - 1)]


def main():
    res = {"leg": 73, "route": "BV",
           "module_under_test": "solver/boussinesq_velocity.py",
           "gate": ("Does a published, independent benchmark exist for the 2D polar-grid "
                    "Biot-Savart / stream-function solve, and does "
                    "solver/boussinesq_velocity.py reproduce it to a pre-committed "
                    "tolerance?"),
           "benchmark": {
               "name": "Lamb-Oseen vortex in a right-angled corner (three images)",
               "sources": [
                   "Lamb, Hydrodynamics (1932), Art. 155 -- vortex in a corner",
                   "Greenhill, Messenger of Mathematics VIII (1878)",
                   "Crosby, Johnson & Morrison, Phys. Fluids 25 (2013), sec. IV eq. (14) "
                   "-- arXiv:1301.6245, the quarter-plane three-image construction",
                   "Lamb-Oseen closed form: v_theta = (Gamma/2 pi R)(1 - exp(-R^2/d^2))",
               ],
               "gamma": GAMMA, "d_core": D_CORE, "r0": R0,
               "beta_frac_of_half_pi": BETA_FRAC,
               "r_min": R_MIN, "r_max": R_MAX,
               "field_window": list(FIELD_WINDOW)},
           "precommitted": {"P1_rel_tol_finest": P1_TOL,
                            "P2_min_observed_order": P2_MIN_ORDER,
                            "P3_rel_tol_finest": P3_TOL,
                            "recorded_in": "writeup/novelty/leg_73.md",
                            "reading_rule": ("P1/P3 are accuracy, P2 is correctness; a "
                                             "P1/P3 miss with P2 holding is a resolution "
                                             "finding, a P2 failure is the disagrees "
                                             "branch")}}

    print("[0] instrument checks")
    res["exp1_check"] = check_exp1()
    print("    exp1 vs published E_1 values: max rel err "
          f"{res['exp1_check']['max_rel_err']:.3e}")

    # Score the invariant at the actual benchmark point (filled in after level 0 gives a,b).
    print("\n[A] the ladder, radial_bc='robin' (the far-field closure IS under test)")
    levels = []
    for n_r, n_beta in LADDER:
        lv = run_level(n_r, n_beta, "robin")
        levels.append(lv)
        print(f"    n_r={n_r:5d} n_beta={n_beta:4d}  "
              f"core pts (rho,beta)=({lv['pts_across_core_rho']:.1f},"
              f"{lv['pts_across_core_beta']:.1f})  "
              f"P1={lv['p1_rel_err_centre_velocity']:.4e}  "
              f"P3={lv['p3_rel_l2_phi_window']:.4e}")
    res["ladder_robin"] = levels

    a, b = levels[0]["blob"]["a"], levels[0]["blob"]["b"]
    res["invariant_residual"] = check_invariant(a, b)
    print(f"    Lamb corner-orbit invariant d/dt(a^-2+b^-2) residual: "
          f"{res['invariant_residual']:.3e}")
    print(f"    finite-core correction to the point-vortex formula: "
          f"{levels[0]['finite_core_correction_rel']:.3e} (relative)")

    print("\n[B] the same ladder with radial_bc='dirichlet' (CONTROL: handed the answer "
          "at both radial ends, so it isolates the interior stencil)")
    ctrl = [run_level(n_r, n_beta, "dirichlet") for n_r, n_beta in LADDER]
    for lv in ctrl:
        print(f"    n_r={lv['n_r']:5d}  P1={lv['p1_rel_err_centre_velocity']:.4e}  "
              f"P3={lv['p3_rel_l2_phi_window']:.4e}")
    res["ladder_dirichlet_control"] = ctrl

    # The control reproduces block A to every printed digit.  That is itself a measurement,
    # not a coincidence: with r_max = 1e3 the exact phi is already at its asymptotic form, so
    # the Robin closure and the exact Dirichlet data differ far below the discretisation
    # error.  Quantify that gap rather than reporting "identical".
    print("\n[B'] how far apart are the two closures, in magnitude")
    sep = []
    for lv_r, lv_d in zip(levels, ctrl):
        sep.append({"n_r": lv_r["n_r"],
                    "d_p1_abs": abs(lv_r["p1_rel_err_centre_velocity"]
                                    - lv_d["p1_rel_err_centre_velocity"]),
                    "d_p3_abs": abs(lv_r["p3_rel_l2_phi_window"]
                                    - lv_d["p3_rel_l2_phi_window"]),
                    "d_centre_u": abs(lv_r["u_numeric"] - lv_d["u_numeric"]),
                    "d_centre_v": abs(lv_r["v_numeric"] - lv_d["v_numeric"])})
        print(f"    n_r={sep[-1]['n_r']:5d}  |P1_robin - P1_dirichlet|="
              f"{sep[-1]['d_p1_abs']:.3e}   centre |du|={sep[-1]['d_centre_u']:.3e} "
              f"|dv|={sep[-1]['d_centre_v']:.3e}")
    res["closure_separation"] = sep

    # Block A therefore does NOT stress the radial closure -- the domain is too big for it to
    # bind.  To put the r^{-2n} Robin modelling under real load, shrink the domain until the
    # blob's own field is still live at r_max, and score the closure alone.
    print("\n[D] the far-field closure under load: shrink the domain until it binds")
    trunc = []
    for r_max in (5.0, 20.0, 100.0, 1000.0):
        r_min = 1.0 / r_max
        w = (max(0.15, 1.5 * r_min), min(FIELD_WINDOW[1], r_max / 1.5))
        rb = run_level(1201, 99, "robin", r_min, r_max, w)
        db = run_level(1201, 99, "dirichlet", r_min, r_max, w)
        trunc.append({"r_max": r_max, "r_min": r_min, "window": list(w),
                      "r_max_over_blob_radius": float(r_max / R0),
                      "robin_p1": rb["p1_rel_err_centre_velocity"],
                      "dirichlet_p1": db["p1_rel_err_centre_velocity"],
                      "robin_p3": rb["p3_rel_l2_phi_window"],
                      "dirichlet_p3": db["p3_rel_l2_phi_window"],
                      "closure_penalty_p3_ratio": float(rb["p3_rel_l2_phi_window"]
                                                        / db["p3_rel_l2_phi_window"]),
                      "closure_own_error_p3": float(rb["p3_rel_l2_phi_window"]
                                                    - db["p3_rel_l2_phi_window"])})
        print(f"    r in [{r_min:g}, {r_max:g}]  robin P1={rb['p1_rel_err_centre_velocity']:.3e}"
              f"  exact-Dirichlet P1={db['p1_rel_err_centre_velocity']:.3e}"
              f"   robin P3={rb['p3_rel_l2_phi_window']:.3e}"
              f"  exact-Dirichlet P3={db['p3_rel_l2_phi_window']:.3e}")
    res["truncation_stress"] = trunc

    print("\n[C] verdict against the pre-commitment")
    p1 = [lv["p1_rel_err_centre_velocity"] for lv in levels]
    p3 = [lv["p3_rel_l2_phi_window"] for lv in levels]
    ord1, ord3 = observed_order(p1), observed_order(p3)
    mono1 = all(p1[i] > p1[i + 1] for i in range(len(p1) - 1))
    mono3 = all(p3[i] > p3[i + 1] for i in range(len(p3) - 1))

    # Richardson extrapolate the headline error from the last pair, at its observed order.
    rich = float(p1[-1] ** 2 / p1[-2]) if p1[-2] > 0 else float("nan")

    res["verdict"] = {
        "p1_errors": p1, "p1_observed_orders": ord1, "p1_monotone": bool(mono1),
        "p1_finest": p1[-1], "p1_pass": bool(p1[-1] <= P1_TOL),
        "p1_richardson_estimate": rich,
        "p3_errors": p3, "p3_observed_orders": ord3, "p3_monotone": bool(mono3),
        "p3_finest": p3[-1], "p3_pass": bool(p3[-1] <= P3_TOL),
        "p2_pass": bool(mono1 and mono3
                        and min(ord1) >= P2_MIN_ORDER and min(ord3) >= P2_MIN_ORDER),
        "p2_min_order_seen": float(min(min(ord1), min(ord3))),
        "p1_margin_factor": float(P1_TOL / p1[-1]),
        "p3_margin_factor": float(P3_TOL / p3[-1]),
    }
    vd = res["verdict"]
    print(f"    P1 finest {vd['p1_finest']:.4e} (tol {P1_TOL:.0e})  -> "
          f"{'PASS' if vd['p1_pass'] else 'MISS'}")
    print(f"    P2 orders P1 {['%.2f' % o for o in ord1]}  P3 "
          f"{['%.2f' % o for o in ord3]}  -> "
          f"{'PASS' if vd['p2_pass'] else 'MISS'}")
    print(f"    P3 finest {vd['p3_finest']:.4e} (tol {P3_TOL:.0e})  -> "
          f"{'PASS' if vd['p3_pass'] else 'MISS'}")

    if vd["p2_pass"] and vd["p1_pass"] and vd["p3_pass"]:
        gate = "YES_AND_IT_REPRODUCES"
    elif vd["p2_pass"]:
        gate = "YES_REPRODUCES_AT_ORDER_ACCURACY_TOLERANCE_MISSED"
    else:
        gate = "YES_BUT_IT_DISAGREES__ESCALATE"
    res["gate_answer"] = gate
    print(f"\n    GATE: {gate}")

    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
    print(f"\nwrote {OUT}")
    return res


if __name__ == "__main__":
    main()
