#!/usr/bin/env python3
"""Dedicated tests for solver/dissipative_profile.py (Route-M2P, leg 125).

Self-running script, no pytest -- the repository's convention.

The tests are ordered by what they protect:
  1-4   the TRANSCRIPTION of Chen arXiv:1908.09385 (a wrong constant here poisons
        everything downstream, and the whole point of this leg was to stop reading
        the paper at abstract depth)
  5-8   the DISCRETE OPERATORS against closed forms (Hilbert, velocity, derivative)
  9-12  the KNOWN-ANSWER GATE and its convergence order
  13-16 the BORDERED system: gauge pinning, Jacobian exactness, Newton recovery
  17-19 the certificate constants and their guards
"""
import sys

import numpy as np

from solver.dissipative_profile import (
    B_CHEN, CHEN_1908_09385, Grid, SteadyProfile, chen_gamma_tension,
    chen_known_answer, chen_profile, measure_chen_object, measure_viscous_object,
)

FAILS = []


def check(name, ok, detail=""):
    status = "ok  " if ok else "FAIL"
    print(f"  [{status}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


print("== (1-4) the transcription of arXiv:1908.09385 ==")

# 1. b^2 = 3/8 is the constant that nulls Chen's residual (p.4).
check("b^2 = 3/8 exactly", abs(B_CHEN ** 2 - 3.0 / 8.0) < 1e-15,
      f"b = {B_CHEN!r}")

# 2. Chen (2.2): the closed forms for U_x and U must be consistent with Omega under the
#    Hilbert transform and integration -- checked here analytically at a point, and
#    numerically in test 5.
X = np.linspace(-6, 6, 4001)
Om, Ux, U = chen_profile(X)
dU = np.gradient(U, X)
check("Chen (2.2): U' = U_x to 1e-4 (np.gradient is 2nd order)",
      float(np.abs(dU - Ux)[10:-10].max()) < 1e-4,
      f"max |U' - U_x| = {float(np.abs(dU - Ux)[10:-10].max()):.3e}")

# 3. bar u_x(0) = 1/b^2 = 8/3 (eq (2.8), p.5).
check("u_x(0) = 8/3 = 1/b^2", abs(chen_profile(np.array([0.0]))[1][0] - 8.0 / 3.0) < 1e-14,
      f"{chen_profile(np.array([0.0]))[1][0]!r}")

# 4. omega_xxx(0)/omega_x(0) = -12/b^2 = -32 exactly (the constant in bar c_omega(t),
#    eq (2.8)).  Series: Omega = -2 b^{-3} X + 4 b^{-5} X^3 + O(X^5).
b = B_CHEN
ratio = (6.0 * 4.0 * b ** -5) / (-2.0 * b ** -3)
check("omega_xxx(0)/omega_x(0) = -32", abs(ratio + 32.0) < 1e-12, f"{ratio!r}")
check("transcribed constant agrees",
      CHEN_1908_09385["approximate_steady_state_2_8"]["omega_xxx0_over_omega_x0"] == -32.0)

# 4b. The gamma tension, resolved from the located text: diffusion is subdominant because
#     c_l = 1/3 < 1/gamma = 1/2, and nu(t) decays because c_omega + 2 c_l = -1/3 < 0.
gt = chen_gamma_tension()
check("c_l = 1/3 < 1/2 = diffusive balance", gt["diffusion_subdominant"],
      f"c_l - 1/gamma = {gt['c_l_minus_balance']:.6f}")
check("nu(t) decays in rescaled time", gt["nu_decays_in_rescaled_time"],
      f"c_omega + 2 c_l = {gt['nu_of_t_exponent']:.6f}")
check("criticality formula is |a|-1 and does NOT apply at a=1/2",
      (CHEN_1908_09385["criticality_a_le_minus1"]["gamma_critical_formula"]
       == "gamma = |a| - 1") and not gt["formula_applies_at_a_half"])
check("the profile Chen supplies at gamma=2 is recorded as INVISCID",
      CHEN_1908_09385["profile_2_2"]["inviscid"] is True
      and gt["profile_at_gamma_2_is_inviscid"] is True)
check("Theorem 1.1's a-neighbourhood is recorded as UNQUANTIFIED in the source",
      CHEN_1908_09385["theorem_1_1"]["delta_quantified"] is False)

print("== (5-8) the discrete operators against closed forms ==")
g = Grid(n=401)
Om_g, Ux_g, U_g = chen_profile(g.X)

# 5. Hilbert transform: H Omega = U_x, in closed form.
herr = float(np.abs(g.H @ Om_g - Ux_g).max())
check("H Omega = U_x to 1e-5 at n=401", herr < 1e-5, f"max err {herr:.3e}")

# 6. Velocity: U = int_0^X H Omega, in closed form, and U(0) = 0 exactly.
verr = float(np.abs(g.V @ Om_g - U_g).max())
check("V Omega = U to 1e-5 at n=401", verr < 1e-5, f"max err {verr:.3e}")
check("U(0) = 0 exactly (the gauge)", abs(float((g.V @ Om_g)[g.i0])) < 1e-14)

# 7. Derivative matrix against the analytic Omega_X.
dOm = -2.0 * b * (b * b - 3.0 * g.X ** 2) / (g.X ** 2 + b * b) ** 3
derr = float(np.abs((g.D @ Om_g - dOm))[5:-5].max())
check("D Omega = Omega_X to 1e-4 at n=401", derr < 1e-4, f"max err {derr:.3e}")

# 8. Parity: H of an odd function is even; U of an odd function is odd.
HOm = g.H @ Om_g
check("H(odd) is even", float(np.abs(HOm - HOm[::-1]).max()) < 1e-9,
      f"{float(np.abs(HOm - HOm[::-1]).max()):.3e}")
UOm = g.V @ Om_g
check("U(odd) is odd", float(np.abs(UOm + UOm[::-1]).max()) < 1e-9,
      f"{float(np.abs(UOm + UOm[::-1]).max()):.3e}")

print("== (9-12) the known-answer gate and its convergence order ==")
ka = [chen_known_answer(n=n) for n in (201, 401, 801, 1601)]
res = [r["residual_sup"] for r in ka]
print("      residual sup:", "  ".join(f"{r:.3e}" for r in res))
check("Chen's closed form nulls the residual to <1e-3 at n=201", res[0] < 1e-3,
      f"{res[0]:.3e}")
check("and to <1e-6 at n=1601", res[-1] < 1e-6, f"{res[-1]:.3e}")
orders = [np.log2(res[i] / res[i + 1]) for i in range(len(res) - 1)]
print("      observed order:", "  ".join(f"{o:.2f}" for o in orders))
check("observed order >= 3.5 (4th-order discretisation)", min(orders) >= 3.5,
      f"min order {min(orders):.2f}")
check("u_x(0) -> 8/3 as the grid refines",
      ka[-1]["ux0_rel_error"] < ka[0]["ux0_rel_error"] / 100,
      f"{ka[0]['ux0_rel_error']:.2e} -> {ka[-1]['ux0_rel_error']:.2e}")

print("== (13-16) the bordered system ==")
prob = SteadyProfile(g, a=0.5, nu=0.0, mode="chen")
z_exact = prob.pack(Om_g[prob.idx], 1.0 / 3.0)

# 13. THE GAUGE IS REALLY THERE: the unbordered block has a near-null vector X Omega_X
#     (the dilation generator).  This is the defect that made the first version of this
#     module report resolution-independent Y_0 ~ 0.18, so it is pinned as a test.
Jb = prob.jacobian(z_exact)
Jsq = Jb[:prob.N, :prob.N]
sv = np.linalg.svd(Jsq, compute_uv=False)
check("unbordered block IS near-singular (the dilation gauge is real)",
      sv[-1] / sv[0] < 1e-6, f"sigma_min/sigma_max = {sv[-1] / sv[0]:.3e}")
check("bordering fixes it: bordered cond << unbordered cond",
      np.linalg.cond(Jb) < 0.05 * (sv[0] / sv[-1]),
      f"cond(bordered) = {np.linalg.cond(Jb):.3e} vs {sv[0] / sv[-1]:.3e}")

# 13b. THE BORDER MUST NOT BE A TAUTOLOGY.  U_X(0) is INVARIANT along the dilation family
#      (Omega_b -> mu^{-2} Omega_{b/mu} leaves 1/b^2 fixed), so bordering with it pins
#      nothing -- that was this module's first version and it is pinned here as a
#      regression so it cannot come back.  Omega_X(0) does vary along the family.
mu = 1.37
Xs = np.linspace(-40, 40, 20001)
Om_1, Ux_1, _ = chen_profile(Xs)
Om_mu = chen_profile(mu * Xs)[0]
Ux_mu = chen_profile(mu * Xs)[1]
check("U_X(0) is INVARIANT along the dilation family (so it is NOT a valid border)",
      abs(Ux_mu[len(Xs) // 2] - Ux_1[len(Xs) // 2]) < 1e-12,
      f"U_X(0): {Ux_1[len(Xs) // 2]:.10f} -> {Ux_mu[len(Xs) // 2]:.10f}")
dOm_1 = np.gradient(Om_1, Xs)[len(Xs) // 2]
dOm_mu = np.gradient(Om_mu, Xs)[len(Xs) // 2]
check("Omega_X(0) DOES vary along it (so it is a valid border)",
      abs(dOm_mu / dOm_1 - mu) < 1e-3,
      f"ratio {dOm_mu / dOm_1:.6f} vs mu = {mu}")
check("SteadyProfile borders on Omega_X(0), not U_X(0)",
      abs(SteadyProfile.OMX0_TARGET + 2.0 / (3.0 / 8.0) ** 1.5) < 1e-12,
      f"OMX0_TARGET = {SteadyProfile.OMX0_TARGET:.12f}")

# 14. The Jacobian is EXACT (F is degree 2): F(z+d) - F(z) - DF d must be the exact
#     quadratic remainder, so a directional finite difference matches to machine precision
#     after the quadratic term is removed.
rng = np.random.default_rng(7)
d = 1e-6 * rng.standard_normal(prob.N + 1)
lhs = prob.F(z_exact + d) - prob.F(z_exact) - Jb @ d
check("F is exactly degree 2 (remainder is O(|d|^2), not O(|d|))",
      float(np.abs(lhs).max()) < 1e-8 and float(np.abs(lhs).max()) > 0,
      f"|remainder| = {float(np.abs(lhs).max()):.3e} at |d| ~ 1e-6")
d2 = 2.0 * d
lhs2 = prob.F(z_exact + d2) - prob.F(z_exact) - Jb @ d2
scale = float(np.abs(lhs2).max() / max(np.abs(lhs).max(), 1e-300))
check("remainder scales exactly x4 when the step doubles", abs(scale - 4.0) < 1e-3,
      f"ratio {scale:.6f}")

# 15. Newton recovers Chen's closed form AND his c_l = 1/3 from a perturbed start.
m = measure_chen_object(n=401, s=0.0)
check("Newton converges from a 1e-3 perturbation", m["newton_converged"],
      f"{m['newton_steps']} steps, residual {m['final_residual_sup']:.2e}")
check("recovers c_l = 1/3 to <1e-3", m["c_l_abs_error"] < 1e-3,
      f"c_l = {m['c_l']:.9f}, |err| = {m['c_l_abs_error']:.2e}")
check("recovers the closed-form profile to <1e-2 relative",
      m["dist_to_closed_form_rel"] < 1e-2, f"{m['dist_to_closed_form_rel']:.3e}")

# 16. The mode guards: the two objects cannot be silently confused.
for bad in (dict(nu=1.0, mode="chen"), dict(nu=0.0, mode="viscous"),
            dict(nu=0.0, mode="nonsense")):
    try:
        SteadyProfile(g, a=0.5, **bad)
        check(f"guard rejects {bad}", False, "no exception raised")
    except ValueError:
        check(f"guard rejects {bad}", True)

print("== (17-19) the certificate constants ==")
cst = prob.certificate_constants(z_exact, s=0.0)
check("Z1 < 1 at the exact profile (A is an approximate inverse)", cst["Z1"] < 1.0,
      f"Z1 = {cst['Z1']:.3e}")
check("Y0 >= 0 and finite", cst["Y0"] >= 0 and np.isfinite(cst["Y0"]),
      f"Y0 = {cst['Y0']:.4e}")
check("budget = (1-Z1)^2/(2 Z2), matching solver/target_selection.y0_budget",
      abs(cst["budget"] - (1 - cst["Z1"]) ** 2 / (2 * cst["Z2"])) < 1e-12 * cst["budget"],
      f"budget = {cst['budget']:.4e}")
check("Y0_over_budget is reported as a MAGNITUDE, not just a boolean",
      np.isfinite(cst["Y0_over_budget"]) and "Y0_over_budget" in cst,
      f"Y0/budget = {cst['Y0_over_budget']:.4e}")

# 18. Object B runs and reports a ladder whatever it does (it must never raise).
mb = measure_viscous_object(n=201, nu=1.0, s=0.0)
check("Object B reports a residual ladder whatever it does",
      len(mb["residual_ladder"]) >= 1 and np.isfinite(mb["final_residual_sup"]),
      f"converged={mb['newton_converged']} reason={mb['newton_reason']} "
      f"final residual {mb['final_residual_sup']:.3e}")
check("Object B enforces the diffusive balance c_omega + 2 c_l = 0 exactly",
      abs(mb["diffusive_balance_residual"]) < 1e-14,
      f"{mb['diffusive_balance_residual']:.2e}")

# 19. The tripwire, as an executable assertion: nothing in this module sweeps nu.
import inspect

import solver.dissipative_profile as dp
src = inspect.getsource(dp)
check("no nu sweep anywhere in the module (stage-V tripwire)",
      "for nu in" not in src and "nu_sweep" not in src and "nu_range=" not in src)

print()
if FAILS:
    print(f"FAILED {len(FAILS)}: " + ", ".join(FAILS))
    sys.exit(1)
print("test_dissipative_profile.py: all checks passed")
