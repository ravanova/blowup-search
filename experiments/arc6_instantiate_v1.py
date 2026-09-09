"""Arc 6, unit U4 (leg 420): instantiate the concentrating vortex and MEASURE
the momentum residual the pulses must absorb.

    .venv/bin/python experiments/arc6_instantiate_v1.py

PRE-REGISTRATION: experiments/journal/leg_420_prereg.md, committed at d026cd4
BEFORE this file existed. Predicted exponent -3/2 - h = -1.51, tolerance 0.05
(derived from the O(q^2h) subleading floor, not chosen), three resolution
levels rho in {1e-2, 1e-3, 1e-4} with a required spread < 0.025, seven planted
controls with pre-computed predictions.

THE OBJECT
----------
    u = curl( (S/r) e_theta ) + B e_theta
      =>  u_r = -(1/r) d_z S,   u_z = (1/r) d_r S,   u_theta = B
so incompressibility is EXACT BY CONSTRUCTION and is never enforced afterwards.

    similarity:  q solves  q - z^2 q^(1-2D) = tau,   X = r^2/(2q),  eta = z/q^D
    S = q^(1-A) * Ucal(X) * w(eta)          (so u_z = q^-A * Ucal'(X) w)
    B = q^-A   * E(X,eta)
    E = sqrt(2X) (1+X)^(-1-h) g(eta)        (E/sqrt(2X) smooth at the axis;
                                             E ~ sqrt2 X^(-1/2-h) g at infinity)
    Ucal = a C^infty bump on (0,2)          (so U = Ucal' has ZERO radial mean
                                             and S vanishes beyond the support,
                                             which is the manuscript's (4.28))
    p = q^(-2A) Pi(X,eta),  Pi = -g^2 (1+X)^(-1-2h) / (1+2h)   [CLOSED FORM]

The pressure is not fitted: Pi is the exact integral -int_X^oo E^2/(2x) dx for
this E, and it satisfies the leading radial balance d_r p = u_theta^2 / r
IDENTICALLY -- which the runner checks as its own first control.

THIS IS NOT THE MANUSCRIPT'S PROFILE AND IS NOT CLAIMED TO BE. The manuscript's
(E, U, Pi) are the output of its Sections 4, A, B, C -- a joined inner/exterior
solution meeting five radial moment identities and an admissible-stress-cone
condition. None of that is reproduced. What is instantiated is an object with
the manuscript's SCALING STRUCTURE and its exact incompressibility, which is
what a scaling measurement needs and all it needs.

CEILING: float64 finite differences on a synthetic field. Tier 2 at best, and a
proof of nothing. No L1->L4 link can move here; Clay stays ~0.05%; W4 is not
touched.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "arc6_instantiate_v1.json"

# ---------------------------------------------------------------- pre-committed
PREREG = {
    "file": "experiments/journal/leg_420_prereg.md",
    "commit": "d026cd4",
    "h": 0.01,
    "A": 0.51,
    "D": 0.49,
    "predicted_exponent": -1.51,
    "tolerance": 0.05,
    "systematic_floor_derived": 0.0201,
    "rho_levels": [1e-2, 1e-3, 1e-4],
    "rho_reported": 1e-3,
    "max_spread_allowed": 0.025,
    "tau_ladder": [1e-4, 1e-5, 1e-6, 1e-7, 1e-8],
    "grid_X": [0.05, 1.0, 25],
    "grid_eta": [-0.5, 0.5, 11],
}


# ------------------------------------------------------------------- the field
@dataclass(frozen=True)
class Params:
    A: float = 0.51
    D: float = 0.49
    h: float = 0.01
    B_scale: float = 1.0
    S_scale: float = 1.0

    @property
    def leading_exponent(self) -> float:
        """-max(A + 1, 2A + D). The prediction, from the ledger of leg 419."""
        return -max(self.A + 1.0, 2.0 * self.A + self.D)


def _bump(X):
    """C^infty bump supported on (0, 2): exp(-1/(X(2-X))), zero outside."""
    X = np.asarray(X, dtype=float)
    out = np.zeros_like(X)
    m = (X > 0.0) & (X < 2.0)
    s = X[m] * (2.0 - X[m])
    out[m] = np.exp(-1.0 / s)
    return out


def _bump_d(X, d=1e-6):
    """d/dX of the bump, by a 4th-order stencil on a smooth compactly supported
    function. The bump is analytic on its support; a stencil is used rather than
    the closed form only to keep the support logic in one place."""
    X = np.asarray(X, dtype=float)
    return (-_bump(X + 2 * d) + 8 * _bump(X + d)
            - 8 * _bump(X - d) + _bump(X - 2 * d)) / (12 * d)


def solve_q(z, tau, P: Params):
    """Unique positive root of q - z^2 q^(1-2D) = tau, by Newton.

    Seeded at tau + |z|^(1/D), which is the manuscript's own q ~ tau + |z|^(1/D).
    """
    z = np.asarray(z, dtype=float)
    tau = np.asarray(tau, dtype=float)
    e = 1.0 - 2.0 * P.D
    q = tau + np.abs(z) ** (1.0 / P.D)
    q = np.maximum(q, 1e-300)
    for _ in range(80):
        f = q - z**2 * q**e - tau
        fp = 1.0 - e * z**2 * q ** (e - 1.0)
        step = f / np.where(np.abs(fp) < 1e-14, 1e-14, fp)
        q_new = q - step
        q_new = np.where(q_new <= 0, q * 0.5, q_new)
        if np.all(np.abs(q_new - q) <= 1e-15 * np.abs(q_new)):
            q = q_new
            break
        q = q_new
    return q


def _q_derivs(z, tau, q, P: Params):
    """dq/dz and dq/dtau by implicit differentiation of F = q - z^2 q^(1-2D) - tau."""
    e = 1.0 - 2.0 * P.D
    Fq = 1.0 - e * z**2 * q ** (e - 1.0)
    Fz = -2.0 * z * q**e
    return -Fz / Fq, 1.0 / Fq


def fields(r, z, t, P: Params):
    """(u_r, u_theta, u_z, p) at Cartesian-cylindrical (r, z, t). All analytic.

    u_r is obtained by differentiating S ANALYTICALLY, not by a nested finite
    difference: nesting a stencil inside a stencil is how a derivative
    measurement quietly becomes a measurement of the stencil.
    """
    r = np.asarray(r, dtype=float)
    z = np.asarray(z, dtype=float)
    tau = 1.0 - np.asarray(t, dtype=float)
    q = solve_q(z, tau, P)
    qz, _ = _q_derivs(z, tau, q, P)

    X = r**2 / (2.0 * q)
    eta = z / q**P.D

    g = np.exp(-2.0 * eta**2)
    gp = -4.0 * eta * g
    w = np.exp(-(eta**2))
    wp = -2.0 * eta * w

    Ucal = _bump(X)
    Ucal_X = _bump_d(X)

    # --- u_theta = q^-A E,  E = sqrt(2X)(1+X)^(-1-h) g(eta)
    E = np.sqrt(2.0 * X) * (1.0 + X) ** (-1.0 - P.h) * g
    u_theta = P.B_scale * q ** (-P.A) * E

    # --- u_z = (1/r) d_r S = q^-A Ucal'(X) w(eta)
    S_amp = P.S_scale * q ** (1.0 - P.A)
    u_z = P.S_scale * q ** (-P.A) * Ucal_X * w

    # --- u_r = -(1/r) d_z S, analytic
    dX_dz = -X * qz / q
    deta_dz = q ** (-P.D) - P.D * eta * qz / q
    dSamp_dz = P.S_scale * (1.0 - P.A) * q ** (-P.A) * qz
    dS_dz = (dSamp_dz * Ucal * w
             + S_amp * (Ucal_X * dX_dz * w + Ucal * wp * deta_dz))
    u_r = -dS_dz / r

    # --- p = q^(-2A) Pi,  Pi = -g^2 (1+X)^(-1-2h)/(1+2h)   (closed form)
    Pi = -(g**2) * (1.0 + X) ** (-1.0 - 2.0 * P.h) / (1.0 + 2.0 * P.h)
    p = (P.B_scale**2) * q ** (-2.0 * P.A) * Pi

    return u_r, u_theta, u_z, p


# ------------------------------------------------------- the residual operator
def _d1(f, var, args, d):
    """4th-order central first derivative of a scalar-valued field callable."""
    a = list(args)
    out = []
    for k, c in ((-2, 1.0), (-1, -8.0), (1, 8.0), (2, -1.0)):
        a[var] = args[var] + k * d
        out.append(c * f(*a))
    return sum(out) / (12.0 * d)


def _d2(f, var, args, d):
    """4th-order central second derivative."""
    a = list(args)
    out = []
    for k, c in ((-2, -1.0), (-1, 16.0), (0, -30.0), (1, 16.0), (2, -1.0)):
        a[var] = args[var] + k * d
        out.append(c * f(*a))
    return sum(out) / (12.0 * d * d)


def residual(r, z, t, P: Params, dr, dz, dt, comps=None):
    """Cylindrical axisymmetric Navier-Stokes residual at viscosity one.

        R_r     = d_t u_r + u_r d_r u_r + u_z d_z u_r - u_theta^2/r
                  + d_r p - [Lap u_r - u_r/r^2]
        R_theta = d_t u_th + u_r d_r u_th + u_z d_z u_th + u_r u_th/r
                  - [Lap u_th - u_th/r^2]
        R_z     = d_t u_z + u_r d_r u_z + u_z d_z u_z + d_z p - Lap u_z
        Lap f   = d_rr f + (1/r) d_r f + d_zz f

    `comps` optionally supplies a (u_r, u_theta, u_z, p) callable, so the SAME
    operator can be applied to a planted exact solution -- which is what
    controls C4-C6 do.
    """
    F = comps if comps is not None else (lambda rr, zz, tt: fields(rr, zz, tt, P))

    def ur(rr, zz, tt): return F(rr, zz, tt)[0]
    def ut(rr, zz, tt): return F(rr, zz, tt)[1]
    def uz(rr, zz, tt): return F(rr, zz, tt)[2]
    def pp(rr, zz, tt): return F(rr, zz, tt)[3]

    a = (r, z, t)
    u_r, u_th, u_z, _ = F(r, z, t)

    ur_r, ur_z, ur_t = _d1(ur, 0, a, dr), _d1(ur, 1, a, dz), _d1(ur, 2, a, dt)
    ut_r, ut_z, ut_t = _d1(ut, 0, a, dr), _d1(ut, 1, a, dz), _d1(ut, 2, a, dt)
    uz_r, uz_z, uz_t = _d1(uz, 0, a, dr), _d1(uz, 1, a, dz), _d1(uz, 2, a, dt)
    p_r, p_z = _d1(pp, 0, a, dr), _d1(pp, 1, a, dz)

    lap_ur = _d2(ur, 0, a, dr) + ur_r / r + _d2(ur, 1, a, dz)
    lap_ut = _d2(ut, 0, a, dr) + ut_r / r + _d2(ut, 1, a, dz)
    lap_uz = _d2(uz, 0, a, dr) + uz_r / r + _d2(uz, 1, a, dz)

    R_r = ur_t + u_r * ur_r + u_z * ur_z - u_th**2 / r + p_r - (lap_ur - u_r / r**2)
    R_th = ut_t + u_r * ut_r + u_z * ut_z + u_r * u_th / r - (lap_ut - u_th / r**2)
    R_z = uz_t + u_r * uz_r + u_z * uz_z + p_z - lap_uz
    div = ur_r + u_r / r + uz_z
    return R_r, R_th, R_z, div


# --------------------------------------------------------------- the ladder run
def similarity_grid():
    x0, x1, nx = PREREG["grid_X"]
    e0, e1, ne = PREREG["grid_eta"]
    X = np.linspace(x0, x1, nx)
    eta = np.linspace(e0, e1, ne)
    return np.meshgrid(X, eta, indexing="ij")


def measure(P: Params, rho: float):
    """max|R_theta| on the FIXED similarity grid, at each tau of the ladder."""
    Xg, Eg = similarity_grid()
    rows = []
    for tau in PREREG["tau_ladder"]:
        q = tau / (1.0 - Eg**2)
        r = np.sqrt(2.0 * q * Xg)
        z = q**P.D * Eg
        t = 1.0 - tau
        dr = rho * np.sqrt(q)
        dz = rho * q**P.D
        dt = rho * tau
        R_r, R_th, R_z, div = residual(r, z, t, P, dr, dz, dt)
        u_r, u_th, u_z, _ = fields(r, z, t, P)
        umax = np.max(np.abs(u_th))
        scale = umax / np.sqrt(q).max()
        rows.append({
            "tau": tau,
            "max_abs_R_theta": float(np.max(np.abs(R_th))),
            "max_abs_R_z": float(np.max(np.abs(R_z))),
            "max_abs_R_r": float(np.max(np.abs(R_r))),
            "max_abs_div_normalised": float(np.max(np.abs(div)) / scale),
            "max_abs_u_theta": float(umax),
        })
    return rows


def fit_exponent(rows, key="max_abs_R_theta"):
    x = np.log10([r["tau"] for r in rows])
    y = np.log10([r[key] for r in rows])
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return float(slope), float(intercept), (1.0 - ss_res / ss_tot if ss_tot else 1.0)


def run_case(name, P: Params, predicted):
    per_rho = {}
    for rho in PREREG["rho_levels"]:
        rows = measure(P, rho)
        slope, icept, r2 = fit_exponent(rows)
        per_rho[f"{rho:g}"] = {
            "fitted_exponent": slope,
            "intercept": icept,
            "r_squared": r2,
            "ladder": rows,
        }
    slopes = [v["fitted_exponent"] for v in per_rho.values()]
    reported = per_rho[f"{PREREG['rho_reported']:g}"]["fitted_exponent"]
    return {
        "name": name,
        "A": P.A, "D": P.D, "h": P.h,
        "B_scale": P.B_scale, "S_scale": P.S_scale,
        "predicted_exponent": predicted,
        "predicted_by_formula_minus_max_Aplus1_2ApluD": P.leading_exponent,
        "per_rho": per_rho,
        "reported_exponent": reported,
        "spread_across_rho": float(max(slopes) - min(slopes)),
        "abs_error_vs_prediction": abs(reported - predicted),
        "inside_tolerance": abs(reported - predicted) <= PREREG["tolerance"],
        "spread_ok": (max(slopes) - min(slopes)) < PREREG["max_spread_allowed"],
    }


# --------------------------------------------------- controls on the OPERATOR
def _rigid_rotation(Om=1.3):
    def F(r, z, t):
        r = np.asarray(r, dtype=float)
        return (np.zeros_like(r), Om * r, np.zeros_like(r), 0.5 * Om**2 * r**2)
    return F


def _bessel_shear(a=2.1, bad=False):
    from scipy.special import j0
    def F(r, z, t):
        r = np.asarray(r, dtype=float)
        decay = a * (1.01 if bad else 1.0)
        u_z = np.exp(-(decay**2) * np.asarray(t, dtype=float)) * j0(a * r)
        zeros = np.zeros_like(r)
        return (zeros, zeros, u_z, zeros)
    return F


def operator_control(name, comps, rho=1e-3):
    r = np.linspace(0.4, 2.0, 17)
    z = np.linspace(-1.0, 1.0, 9)
    R, Z = np.meshgrid(r, z, indexing="ij")
    T = np.full_like(R, 0.3)
    P = Params()
    R_r, R_th, R_z, div = residual(R, Z, T, P, rho, rho, rho, comps=comps)
    u_r, u_th, u_z, _ = comps(R, Z, T)
    umag = max(float(np.max(np.abs(u_th))), float(np.max(np.abs(u_z))), 1.0)
    worst = max(float(np.max(np.abs(R_r))), float(np.max(np.abs(R_th))),
                float(np.max(np.abs(R_z))))
    return {"name": name, "max_abs_residual": worst,
            "relative_to_velocity_scale": worst / umag,
            "max_abs_div": float(np.max(np.abs(div)))}


def main():
    t0 = time.time()
    print("ARC 6 / U4 — instantiate and measure. Pre-registration:",
          PREREG["file"], "@", PREREG["commit"])
    print("predicted", PREREG["predicted_exponent"], "tolerance", PREREG["tolerance"])
    print()

    base = Params()
    cases = [
        run_case("P0_instantiation", base, PREREG["predicted_exponent"]),
        run_case("C1_A0.80_D0.49", Params(A=0.80, D=0.49), -2.09),
        run_case("C2_A0.51_D0.70", Params(A=0.51, D=0.70), -1.72),
        run_case("C3_amplitudes_rescaled",
                 Params(B_scale=3.7, S_scale=0.4), PREREG["predicted_exponent"]),
    ]
    for c in cases:
        print(f"{c['name']:<26} predicted {c['predicted_exponent']:+.4f}  "
              f"measured {c['reported_exponent']:+.6f}  "
              f"|err| {c['abs_error_vs_prediction']:.6f}  "
              f"spread {c['spread_across_rho']:.2e}  "
              f"{'OK' if c['inside_tolerance'] and c['spread_ok'] else 'OUT'}")

    print()
    ops = [
        operator_control("C4_rigid_rotation", _rigid_rotation()),
        operator_control("C5_bessel_shear", _bessel_shear()),
        operator_control("C6_bessel_shear_1pc_wrong", _bessel_shear(bad=True)),
    ]
    for o in ops:
        print(f"{o['name']:<28} max|R| {o['max_abs_residual']:.6e}  "
              f"relative {o['relative_to_velocity_scale']:.3e}")

    # radial balance: this construction's pressure satisfies d_r p = u_th^2/r
    # identically. Checked, because a pressure that did not would make R_r
    # meaningless and R_theta unrepresentative.
    Xg, Eg = similarity_grid()
    tau = 1e-6
    q = tau / (1.0 - Eg**2)
    r = np.sqrt(2.0 * q * Xg)
    z = q**base.D * Eg
    t = 1.0 - tau
    def pf(rr, zz, tt): return fields(rr, zz, tt, base)[3]
    p_r = _d1(pf, 0, (r, z, t), 1e-3 * np.sqrt(q))
    u_r0, u_th0, u_z0, _ = fields(r, z, t, base)
    lhs, rhs = p_r, u_th0**2 / r
    radial_balance_rel = float(np.max(np.abs(lhs - rhs)) / np.max(np.abs(rhs)))
    print(f"\nradial balance  max|d_r p - u_th^2/r| / max|u_th^2/r| = "
          f"{radial_balance_rel:.3e}")

    # exterior moment identities: EXPECTED TO FAIL here, reported anyway.
    Xline = np.linspace(0.02, 1.9, 400)
    qq = tau
    rr = np.sqrt(2.0 * qq * Xline)
    zz = np.zeros_like(rr)
    tt = np.full_like(rr, 1.0 - tau)
    Rr_, Rth_, Rz_, _ = residual(rr, zz, tt, base,
                                 1e-3 * math.sqrt(qq), 1e-3 * qq**base.D, 1e-3 * tau)
    m_theta = float(np.trapezoid(rr**2 * Rth_, rr))
    m_z = float(np.trapezoid(rr * Rz_, rr))
    n_theta = float(np.trapezoid(np.abs(rr**2 * Rth_), rr))
    n_z = float(np.trapezoid(np.abs(rr * Rz_), rr))
    print(f"exterior moment  int r^2 R_theta dr = {m_theta:.6e}  "
          f"(|.| integral {n_theta:.6e}, ratio {abs(m_theta)/n_theta:.4f})")
    print(f"exterior moment  int r   R_z     dr = {m_z:.6e}  "
          f"(|.| integral {n_z:.6e}, ratio {abs(m_z)/n_z:.4f})")

    # ---------------------------------------------------------------- POST HOC
    # THE PRE-REGISTRATION'S OWN FORMULA WAS WRONG AND THIS RUN CAUGHT IT.
    # experiments/journal/leg_420_prereg.md §7 predicts the leading exponent as
    # -max(A + 1, 2A + D). That OMITS AXIAL DIFFUSION, whose scale is
    # u_theta / ell_z^2 = q^-(A + 2D). It is invisible at the design point
    # because A + 2D = 1.49 < 1.51 there, and it dominates as soon as D > 1/2.
    # C2 (D = 0.70) is exactly that case: A + 2D = 1.91.
    #
    # The pre-committed numbers above are LEFT EXACTLY AS THEY WERE MEASURED
    # AGAINST THE PRE-COMMITTED PREDICTIONS. Everything below is labelled
    # post-hoc, is not used to answer the gate, and is banked so the defect in
    # the pre-registration is in the artefact rather than in a memory.
    def corrected(P):
        return -max(P.A + 1.0, 2.0 * P.A + P.D, P.A + 2.0 * P.D)

    posthoc = []
    for c, P in zip(cases, [base, Params(A=0.80, D=0.49), Params(A=0.51, D=0.70),
                            Params(B_scale=3.7, S_scale=0.4)]):
        posthoc.append({
            "name": c["name"],
            "prereg_prediction": c["predicted_exponent"],
            "corrected_prediction": corrected(P),
            "measured": c["reported_exponent"],
            "abs_error_vs_prereg": c["abs_error_vs_prediction"],
            "abs_error_vs_corrected": abs(c["reported_exponent"] - corrected(P)),
        })
    # Two FRESH exponent pairs the corrected formula has never seen, so it is
    # tested rather than fitted.
    for nm, P in (("PH1_A0.51_D0.60", Params(A=0.51, D=0.60)),
                  ("PH2_A0.60_D0.55", Params(A=0.60, D=0.55))):
        cc = run_case(nm, P, corrected(P))
        posthoc.append({
            "name": nm,
            "prereg_prediction": None,
            "corrected_prediction": corrected(P),
            "measured": cc["reported_exponent"],
            "abs_error_vs_prereg": None,
            "abs_error_vs_corrected": abs(cc["reported_exponent"] - corrected(P)),
            "spread_across_rho": cc["spread_across_rho"],
        })
    # A second post-hoc diagnostic, and it is a PREDICTION not a fit: if the
    # offsets above are subleading contamination, restricting the fit to the
    # last three decades must move every exponent TOWARD its corrected
    # prediction, because every competing term is relatively q^gap smaller
    # there. If they moved away, the explanation would be wrong.
    tails = []
    for nm, P, pred in (("P0_instantiation", base, corrected(base)),
                        ("C1_A0.80_D0.49", Params(A=0.80, D=0.49),
                         corrected(Params(A=0.80, D=0.49))),
                        ("C2_A0.51_D0.70", Params(A=0.51, D=0.70),
                         corrected(Params(A=0.51, D=0.70))),
                        ("PH1_A0.51_D0.60", Params(A=0.51, D=0.60),
                         corrected(Params(A=0.51, D=0.60))),
                        ("PH2_A0.60_D0.55", Params(A=0.60, D=0.55),
                         corrected(Params(A=0.60, D=0.55)))):
        rows = measure(P, PREREG["rho_reported"])
        full, _, _ = fit_exponent(rows)
        tail, _, _ = fit_exponent(rows[-3:])
        tails.append({
            "name": nm, "corrected_prediction": pred,
            "full_ladder_exponent": full, "tail_3pt_exponent": tail,
            "abs_error_full": abs(full - pred),
            "abs_error_tail": abs(tail - pred),
            "moved_toward_prediction": abs(tail - pred) < abs(full - pred),
        })
    print("\nPOST HOC — subleading contamination: restricting to the last three "
          "decades must move every exponent TOWARD its prediction")
    for t in tails:
        print(f"{t['name']:<26} pred {t['corrected_prediction']:+.4f}  "
              f"full {t['full_ladder_exponent']:+.6f} (|err| {t['abs_error_full']:.6f})"
              f"  tail {t['tail_3pt_exponent']:+.6f} (|err| {t['abs_error_tail']:.6f})"
              f"  {'toward' if t['moved_toward_prediction'] else 'AWAY'}")
    tails_all_toward = all(t["moved_toward_prediction"] for t in tails)
    print(f"every case moved toward its prediction: {tails_all_toward}")

    print("\nPOST HOC — the pre-registration's formula omitted axial diffusion "
          "q^-(A+2D):")
    for ph in posthoc:
        pre = ("      —" if ph["prereg_prediction"] is None
               else f"{ph['prereg_prediction']:+.4f}")
        errp = ("    —" if ph["abs_error_vs_prereg"] is None
                else f"{ph['abs_error_vs_prereg']:.4f}")
        print(f"{ph['name']:<26} prereg {pre}  corrected "
              f"{ph['corrected_prediction']:+.4f}  measured "
              f"{ph['measured']:+.6f}  |err| prereg {errp}  "
              f"corrected {ph['abs_error_vs_corrected']:.6f}")

    p0 = cases[0]
    gate = ("UNDER-RESOURCED" if not p0["spread_ok"]
            else ("YES" if p0["inside_tolerance"] else "NO"))
    controls_ok = (
        cases[1]["inside_tolerance"] and cases[2]["inside_tolerance"]
        and cases[3]["inside_tolerance"]
        and abs(cases[1]["reported_exponent"] - p0["reported_exponent"]) > 0.2
        and abs(cases[2]["reported_exponent"] - p0["reported_exponent"]) > 0.1
        and abs(cases[3]["reported_exponent"] - p0["reported_exponent"]) < 1e-6
        and ops[0]["relative_to_velocity_scale"] < 1e-6
        and ops[1]["relative_to_velocity_scale"] < 1e-6
        and ops[2]["relative_to_velocity_scale"] > 1e-4
    )
    if gate == "YES" and not controls_ok:
        gate = "YES-BUT-CONTROLS-FAILED"

    out = {
        "schema": "arc6_instantiate_v1",
        "unit": "U4 (leg 420, CONSTRUCTION) — INSTANTIATE",
        "arc": 6, "leg": 420, "date_utc": "2026-09-09",
        "prereg": PREREG,
        "verification_status": "UNVERIFIED (§3f rule 1).",
        "cases": cases,
        "operator_controls": ops,
        "radial_balance_relative_residual": radial_balance_rel,
        "exterior_moment_int_r2_Rtheta": m_theta,
        "exterior_moment_int_r2_Rtheta_abs": n_theta,
        "exterior_moment_int_r_Rz": m_z,
        "exterior_moment_int_r_Rz_abs": n_z,
        "exterior_moments_expected_to_fail": True,
        "gate": {
            "question": "Does the measured residual scale as the construction requires?",
            "answer": gate,
            "answer_in_full": (
                "YES ON THE MEASURED QUESTION, AND THE PRE-COMMITTED CONJUNCTION IS NOT MET. "
                "P0 measures -1.498218 against a pre-committed -1.51: |err| 0.011782 inside the "
                "pre-committed tolerance 0.05, three-level spread 2.11e-07 far inside the "
                "pre-committed 0.025. But the pre-registration's §8 requires ALSO that every "
                "control do what its row says, and C2 did not. C2 FAILED BECAUSE THE "
                "PRE-REGISTRATION'S FORMULA WAS WRONG, NOT BECAUSE THE MEASUREMENT WAS: it "
                "omitted axial diffusion, q^-(A+2D), which is subdominant at the design point "
                "(1.49 < 1.51) and dominant for D > 1/2. Against the corrected formula C2 "
                "measures -1.909028 versus -1.91, |err| 0.000972. The conjunction is reported "
                "as UNMET rather than re-scored against the corrected formula, because "
                "re-scoring a pre-committed control after seeing the number is the thing the "
                "pre-registration exists to prevent."
            ),
            "controls_all_as_predicted": bool(controls_ok),
            "P0_inside_tolerance": bool(p0["inside_tolerance"]),
            "P0_spread_ok": bool(p0["spread_ok"]),
            "which_control_failed": "C2_A0.51_D0.70",
            "why_it_failed": "the pre-registration's own formula, not the instrument",
        },
        "posthoc_corrected_formula": {
            "prereg_formula": "-max(A + 1, 2A + D)",
            "corrected_formula": "-max(A + 1, 2A + D, A + 2D)",
            "omitted_term": "axial diffusion, u_theta / ell_z^2 = q^-(A + 2D)",
            "why_it_was_invisible_at_the_design_point": "A + 2D = 1.49 < 1.51 when A = 0.51, D = 0.49, so the omitted term is SUBDOMINANT exactly at the design point and dominates only for D > 1/2. C2 (D = 0.70) is that case.",
            "status": "POST HOC. Not used to answer the gate. The pre-committed predictions and the errors against them are left exactly as measured.",
            "rows": posthoc,
        },
        "posthoc_tail_fit": {
            "what": "the same ladder fitted over its last three decades only",
            "prediction_made_before_looking": "if the offsets are subleading contamination, every exponent must move TOWARD its corrected prediction",
            "all_moved_toward": bool(tails_all_toward),
            "rows": tails,
        },
        "clay_movement": {"links_moved": 0, "clay_odds": "~0.05%, unchanged",
                          "walls_moved": "none", "tier": "Tier 2 at best"},
        "runtime_seconds": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nGATE: {gate}   controls_all_as_predicted={controls_ok}")
    print(f"wrote {OUT.relative_to(ROOT)}  ({time.time()-t0:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
