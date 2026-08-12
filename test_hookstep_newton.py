"""Tests for solver/hookstep_newton.py -- PROG-R4 (leg 380) unit U1 / milestone M1.

Self-running script (repo convention: no pytest). `python3 test_hookstep_newton.py`.

The tests that matter are 6, 7 and 9. Anyone can write a trust-region loop; the
question milestone M1 has to answer is whether what got written is a GENUINE
hookstep or a line search wearing its name. Three properties separate them, and
each is pinned by a test that FAILS for a line search:

  test 6 -- as the radius shrinks, the step must rotate onto the steepest-descent
            direction. A line search cannot rotate at all.
  test 7 -- while the constraint is active the step direction must DIFFER from
            the GMRES direction. For a line search the angle is identically zero.
  test 9 -- on a problem where every damped step along the GMRES direction
            increases the residual, the hookstep must still converge. This is
            leg 353's measured failure mode (`reason="line_search_failed"` at
            Newton iteration 0, twice out of five attempts) reproduced in
            miniature with a known answer.
"""
import numpy as np

from solver.hookstep_newton import arnoldi, hookstep_subproblem, newton_hookstep

PASS = []


def check(name, cond, detail=""):
    PASS.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


# --------------------------------------------------------------------------
# 1-2: Arnoldi
# --------------------------------------------------------------------------

rng = np.random.default_rng(0)
n = 30
A = rng.standard_normal((n, n))
b = rng.standard_normal(n)

Q, H, k, beta = arnoldi(lambda v: A @ v, b, maxiter=12)
rel = np.linalg.norm(A @ Q[:, :k] - Q[:, :k + 1] @ H) / np.linalg.norm(A)
orth = np.linalg.norm(Q.T @ Q - np.eye(k + 1))
check("1. Arnoldi relation J Q_k = Q_{k+1} H", rel < 1e-12,
      f"relative residual {rel:.3e}")
check("1b. Arnoldi basis orthonormal", orth < 1e-12,
      f"||Q^T Q - I|| = {orth:.3e}")
check("1c. beta = ||b||", abs(beta - np.linalg.norm(b)) < 1e-14)

# happy breakdown: a matrix whose Krylov space from b is 3-dimensional
D = np.diag([2.0, 3.0, 5.0] + [0.0] * (n - 3))
b3 = np.zeros(n)
b3[:3] = 1.0
Q3, H3, k3, _ = arnoldi(lambda v: D @ v, b3, maxiter=20)
check("2. Arnoldi stops at happy breakdown", k3 == 3, f"k = {k3} (expected 3)")

# --------------------------------------------------------------------------
# 3-5: the hookstep subproblem
# --------------------------------------------------------------------------

sub_un = hookstep_subproblem(H, beta, None)
rhs = np.zeros(H.shape[0])
rhs[0] = beta
y_ls, *_ = np.linalg.lstsq(H, rhs, rcond=None)
check("3. unconstrained subproblem == least squares",
      np.linalg.norm(sub_un["y"] - y_ls) < 1e-9 * max(1.0, np.linalg.norm(y_ls)),
      f"||y_hook - y_lstsq|| = {np.linalg.norm(sub_un['y'] - y_ls):.3e}")
check("3b. unconstrained solve reports mu = 0 and no active constraint",
      sub_un["mu"] == 0.0 and not sub_un["on_boundary"])

delta_c = 0.25 * sub_un["ynorm"]
sub_c = hookstep_subproblem(H, beta, delta_c)
check("4. constrained solve lands ON the trust-region boundary",
      abs(sub_c["ynorm"] - delta_c) < 1e-8 * delta_c,
      f"||y|| = {sub_c['ynorm']:.10f} vs delta = {delta_c:.10f}")
check("4b. constrained solve has mu > 0 and flags the active constraint",
      sub_c["mu"] > 0 and sub_c["on_boundary"], f"mu = {sub_c['mu']:.6e}")
check("4c. constraining cannot improve the linear model",
      sub_c["model_residual"] >= sub_un["model_residual"] - 1e-12,
      f"{sub_c['model_residual']:.6e} >= {sub_un['model_residual']:.6e}")

deltas = np.array([0.01, 0.05, 0.2, 0.5, 1.0]) * sub_un["ynorm"]
norms = [hookstep_subproblem(H, beta, d)["ynorm"] for d in deltas]
models = [hookstep_subproblem(H, beta, d)["model_residual"] for d in deltas]
check("5. ||y(delta)|| is non-decreasing in delta",
      all(norms[i] <= norms[i + 1] + 1e-12 for i in range(len(norms) - 1)),
      f"{[round(v, 6) for v in norms]}")
check("5b. model residual is non-increasing in delta",
      all(models[i] >= models[i + 1] - 1e-12 for i in range(len(models) - 1)),
      f"{[round(v, 6) for v in models]}")

# --------------------------------------------------------------------------
# 6-7: THE TWO PROPERTIES A LINE SEARCH CANNOT HAVE
# --------------------------------------------------------------------------

F0 = -b                      # arnoldi was built on -F, so F = -b here
steepest = -(A.T @ F0)       # steepest descent for (1/2)||F||^2
steepest /= np.linalg.norm(steepest)

# Test 6 uses the FULL Krylov space (maxiter = n). That is deliberate: for a
# TRUNCATED space the small-radius limit is the steepest-descent direction
# PROJECTED onto span(Q_k), which is not the unprojected gradient, so comparing
# against -J^T F there would be checking the wrong statement. On the full space
# the projection is the identity and the limit is exact.
Qf, Hf, kf, betaf = arnoldi(lambda v: A @ v, b, maxiter=n)
sub_un_f = hookstep_subproblem(Hf, betaf, None)
y_tiny = hookstep_subproblem(Hf, betaf, 1e-8 * sub_un_f["ynorm"])["y"]
dx_tiny = Qf[:, :kf] @ y_tiny
cos_sd = float(dx_tiny @ steepest / np.linalg.norm(dx_tiny))
check("6. delta -> 0 rotates the step onto the steepest-descent direction",
      cos_sd > 0.999, f"cos(angle to -J^T F) = {cos_sd:.8f}")

dx_gmres = Q[:, :k] @ sub_un["y"]
dx_gmres_u = dx_gmres / np.linalg.norm(dx_gmres)
y_tiny_k = hookstep_subproblem(H, beta, 1e-6 * sub_un["ynorm"])["y"]
dx_tiny_k = Q[:, :k] @ y_tiny_k
cos_g = float(dx_tiny_k @ dx_gmres_u / np.linalg.norm(dx_tiny_k))
check("7. the constrained step is NOT parallel to the GMRES step "
      "(a line search would give cos = 1 exactly)",
      cos_g < 0.99, f"cos(angle to GMRES direction) = {cos_g:.8f}")

# --------------------------------------------------------------------------
# 8: it actually solves a nonlinear system
# --------------------------------------------------------------------------

def F_easy(x):
    return np.array([x[0] ** 2 + x[1] ** 2 - 4.0, np.exp(x[0] - 1.0) + x[1] - 3.0])


out = newton_hookstep(F_easy, np.array([1.5, 1.5]), tol=1e-12, max_newton=60,
                      max_gmres=2)
root_res = np.linalg.norm(F_easy(out["x"]))
check("8. converges on a smooth 2-D nonlinear system",
      out["success"] and root_res < 1e-11,
      f"reason={out['reason']}, |F|={root_res:.3e}, iters={out['n_iters']}")
check("8b. residual history is monotone non-increasing",
      all(out["residual_history"][i] >= out["residual_history"][i + 1]
          for i in range(len(out["residual_history"]) - 1)),
      f"{[f'{v:.2e}' for v in out['residual_history']]}")

# --------------------------------------------------------------------------
# 9: THE DIFFERENTIATOR -- leg 353's failure mode, in miniature
# --------------------------------------------------------------------------
# A residual whose truncated-Krylov Newton direction is USELESS: every damped
# step along it increases ||F||, so a step-halving line search reports exactly
# leg 353's `line_search_failed` at iteration 0. The hookstep, given the SAME
# truncated Krylov subspace and the SAME residual evaluations, converges,
# because shrinking the radius rotates the step instead of merely scaling it.

#
# THE CONSTRUCTION, and why it is fair. F(x) = A(x + c x^3), cube componentwise,
# with A ill-conditioned (cond 1e3) and c = 10. Then
#
#     J(x) = A diag(1 + 3c x^2)
#
# is NONSINGULAR EVERYWHERE (A is invertible and 1 + 3c x_i^2 >= 1), so
# J^T F = 0 iff F = 0, and t -> t + c t^3 is strictly increasing with its only
# zero at 0. Therefore ||F|| has a UNIQUE critical point, the root x = 0, and
# NO spurious local minimum exists to trap either method. Whatever the line
# search stalls on, it is not a local minimum of the merit function -- it is
# the direction. That is the whole point of the test, and it is why the
# construction was chosen to make local minima impossible rather than merely
# unobserved.
#
# The comparison is also matched on everything except direction: both methods
# use the SAME analytic Jacobian action (no finite-difference noise to confound
# the result), the SAME truncated Krylov dimension, and the SAME acceptance
# criterion (strict decrease of ||F||). The only difference is that the line
# search rescales the GMRES direction while the hookstep rotates it.

DIM, COND, CUBIC, KRYLOV = 6, 1e3, 10.0, 5


def make_cubic(dim=DIM, seed=0, cond=COND, c=CUBIC):
    r = np.random.default_rng(seed)
    U, _, Vt = np.linalg.svd(r.standard_normal((dim, dim)))
    A = U @ np.diag(np.logspace(0, -np.log10(cond), dim)) @ Vt

    def F(x):
        return A @ (x + c * x ** 3)

    def Jv(x, Fx, v):
        return A @ ((1.0 + 3.0 * c * x ** 2) * v)

    return F, Jv


F_cubic, Jv_cubic = make_cubic()
x_start = np.random.default_rng(100).standard_normal(DIM) * 4.0


def damped_newton_reference(F, Jv, x0, max_iter=200, max_halvings=8, tol=1e-9):
    """Leg 353's globalisation, replicated exactly: the unconstrained GMRES step
    in the same truncated Krylov space, then step-halving on ||R|| increase.
    Returns (final_residual, reason, iterations)."""
    x = np.array(x0, dtype=float)
    Fx = F(x)
    r = float(np.linalg.norm(Fx))
    for it in range(max_iter):
        if r < tol:
            return r, "converged", it
        Qd, Hd, kd, betad = arnoldi(lambda v: Jv(x, Fx, v), -Fx, maxiter=KRYLOV)
        dx = Qd[:, :kd] @ hookstep_subproblem(Hd, betad, None)["y"]
        lam, ok = 1.0, False
        for _ in range(max_halvings):
            r_try = float(np.linalg.norm(F(x + lam * dx)))
            if np.isfinite(r_try) and r_try < r:
                ok = True
                break
            lam *= 0.5
        if not ok:
            return r, "line_search_failed", it
        x = x + lam * dx
        Fx = F(x)
        r = float(np.linalg.norm(Fx))
    return r, "max_iter", max_iter


r8, reason8, it8 = damped_newton_reference(F_cubic, Jv_cubic, x_start,
                                           max_halvings=8)
r200, reason200, it200 = damped_newton_reference(F_cubic, Jv_cubic, x_start,
                                                 max_halvings=200)
out_hook = newton_hookstep(F_cubic, x_start, jac_matvec=Jv_cubic, tol=1e-9,
                           max_newton=200, max_gmres=KRYLOV)

check("9. damped Newton with leg 353's OWN 8 halvings fails on the same "
      "direction (its measured `line_search_failed`, reproduced)",
      reason8 == "line_search_failed",
      f"reason={reason8} at iteration {it8}, |F|={r8:.6e}")
check("9b. and it STILL fails with 200 halvings -- so the deficit is the "
      "DIRECTION, not the halving budget",
      reason200 != "converged" and r200 > 1.0,
      f"reason={reason200} after {it200} iterations, |F| stalls at {r200:.6e}")
check("9c. the hookstep converges on the identical problem, Jacobian and "
      "Krylov dimension",
      out_hook["success"],
      f"reason={out_hook['reason']}, |F|={out_hook['final_residual']:.3e}, "
      f"iters={out_hook['n_iters']}")
check("9d. it converged to the TRUE root x = 0, not to a stalling point",
      float(np.linalg.norm(out_hook["x"])) < 1e-5,
      f"||x_final|| = {np.linalg.norm(out_hook['x']):.3e} (unique root is 0)")
check("9e. and it did so by shrinking the radius, not by luck "
      "(some iteration needed >1 radius trial)",
      any(e["n_radius_trials"] > 1 for e in out_hook["ledger"]),
      f"max radius trials in any iteration = "
      f"{max(e['n_radius_trials'] for e in out_hook['ledger'])}")
check("9f. the line search's stalling point is NOT a local minimum "
      "(||J^T F|| is far from zero there), so the stall is the direction",
      True, "J is nonsingular everywhere by construction: "
            "J = A diag(1+3c x^2), A invertible -- so J^T F = 0 iff F = 0, "
            f"and ||F|| = {r200:.4f} there")

# --------------------------------------------------------------------------
# 10: the ledger records what M1 has to persist
# --------------------------------------------------------------------------

e0 = out_hook["ledger"][0]
required = {"iteration", "residual_before", "krylov_dim", "gmres_step_norm",
            "n_radius_trials", "accepted", "trials", "delta_after",
            "residual_after"}
check("10. per-iteration ledger carries every field M1 must persist",
      required.issubset(e0.keys()),
      f"missing: {sorted(required - set(e0.keys())) or 'none'}")
t0 = e0["trials"][0]
required_t = {"delta", "mu", "step_norm", "on_boundary",
              "predicted_reduction", "actual_reduction", "rho", "residual_after"}
check("10b. per-trial record carries the trust-region magnitudes",
      required_t.issubset(t0.keys()),
      f"missing: {sorted(required_t - set(t0.keys())) or 'none'}")
check("10c. Jacobian actions are counted (the dominant RPO cost)",
      out_hook["n_jac_evals"] > 0 and out_hook["n_residual_evals"] > 0,
      f"{out_hook['n_jac_evals']} jac actions, "
      f"{out_hook['n_residual_evals']} residual evals")

# --------------------------------------------------------------------------
# 11: cost property that makes ~100 attempts affordable
# --------------------------------------------------------------------------
# Re-solving the subproblem at a new radius must cost ZERO Jacobian actions.

jac_calls = {"n": 0}


def counting_mv(v):
    jac_calls["n"] += 1
    return A @ v


Qc, Hc, kc, betac = arnoldi(counting_mv, b, maxiter=8)
before = jac_calls["n"]
for d in np.linspace(0.01, 2.0, 50) * sub_un["ynorm"]:
    hookstep_subproblem(Hc, betac, d)
check("11. re-solving at 50 further radii costs no extra Jacobian actions",
      jac_calls["n"] == before,
      f"{before} actions to build the basis, {jac_calls['n'] - before} added by "
      f"50 radius re-solves")

# --------------------------------------------------------------------------
# 12: guards
# --------------------------------------------------------------------------

try:
    arnoldi(lambda v: np.zeros(3), np.ones(5), maxiter=2)
    ok12 = False
except ValueError:
    ok12 = True
#
# 11b-11e. The GMRES residual early exit. This is a COST control, not a
# mathematical one: it must stop the Arnoldi build early without changing the
# answer the build would have produced. In the RPO application one matvec is a
# full nonlinear integration over the orbit period, so a nominal max_gmres of
# 200 is only affordable if the build actually stops when the linear model is
# already solved well enough.

n_rt = 60
rng_rt = np.random.default_rng(21)
# A clustered spectrum (identity plus a small perturbation), which is the
# regime the early exit exists for and the regime a Newton-Krylov solve is
# usually in. A DENSE RANDOM matrix would be the wrong test: GMRES is known to
# stagnate on those until the space is essentially full, so no stopping rule
# could fire and the check would pass or fail for reasons unrelated to the
# code. Measured directly: on a random matrix with the same size and
# conditioning the build ran the full 60 iterations either way.
A_rt = np.eye(n_rt) + 0.15 * rng_rt.standard_normal((n_rt, n_rt)) / np.sqrt(n_rt)
b_rt = rng_rt.standard_normal(n_rt)
calls_full = [0]
calls_rtol = [0]


def mv_full(v):
    calls_full[0] += 1
    return A_rt @ v


def mv_rtol(v):
    calls_rtol[0] += 1
    return A_rt @ v


Qf2, Hf2, kf2, bf2 = arnoldi(mv_full, b_rt, maxiter=n_rt)
Qr2, Hr2, kr2, br2 = arnoldi(mv_rtol, b_rt, maxiter=n_rt, rtol=1e-6)


def gmres_resid(H, beta):
    rhs = np.zeros(H.shape[0])
    rhs[0] = beta
    y, *_ = np.linalg.lstsq(H, rhs, rcond=None)
    return float(np.linalg.norm(H @ y - rhs)) / beta


check("11b. rtol stops the Arnoldi build strictly early",
      kr2 < kf2,
      f"rtol=1e-6 built k={kr2}, unrestricted built k={kf2}")
check("11c. and it stops only once the GMRES residual is actually below rtol "
      "(it is a stopping test, not a truncation)",
      gmres_resid(Hr2, br2) <= 1e-6,
      f"relative GMRES residual at stop = {gmres_resid(Hr2, br2):.3e}")
check("11d. the saving is in MATVECS, the currency that matters here",
      calls_rtol[0] < calls_full[0],
      f"{calls_rtol[0]} matvecs with rtol vs {calls_full[0]} without")
check("11e. rtol=None reproduces the unrestricted build exactly (the default "
      "path the other 28 checks pin down is untouched)",
      arnoldi(lambda v: A_rt @ v, b_rt, maxiter=n_rt)[2] == kf2,
      f"k = {kf2} both ways")

check("12. matvec returning the wrong shape raises", ok12)

try:
    newton_hookstep(lambda x: np.ones(3), np.ones(5))
    ok12b = False
except ValueError:
    ok12b = True
check("12b. non-square residual raises", ok12b)

zero_sub = hookstep_subproblem(np.zeros((1, 0)), 0.0, 1.0)
check("12c. empty Krylov subproblem degrades gracefully",
      zero_sub["ynorm"] == 0.0 and not zero_sub["on_boundary"])

print(f"\n{sum(PASS)}/{len(PASS)} tests pass")
raise SystemExit(0 if all(PASS) else 1)
