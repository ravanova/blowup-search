"""Newton-GMRES-hookstep: a genuine trust-region globalisation for matrix-free
Newton, built for PROG-R4 (leg 380) unit U1, milestone M1.

WHY THIS MODULE EXISTS. Leg 353 ran plain Newton with a step-halving line search
against published relative periodic orbits of 2-D Kolmogorov flow and got 0/5,
with the line search unable to find ANY residual-reducing step on two of the
five attempts (`reason="line_search_failed"` at Newton iteration 0). That is the
failure mode Viswanath 2007 (arXiv:physics/0604062, J. Fluid Mech. 580, 339)
diagnosed for this problem class: plain and damped Newton steps are ineffective,
because the Newton correction for a chaotic-flow shooting residual is enormous
and points somewhere the linear model is worthless. The published fix -- used by
Viswanath 2007, by Chandler & Kerswell 2013 (arXiv:1207.4682) and by Lucas &
Kerswell 2015 (arXiv:1406.1820), i.e. by the source of this programme's named
seed -- is a HOOKSTEP: a trust-region constraint imposed inside the Krylov
subspace GMRES has already built.

A line search only ever rescales the GMRES direction. A hookstep CHANGES THE
DIRECTION as the radius shrinks, interpolating between the Newton direction
(large radius) and the steepest-descent direction (small radius). That is the
distinction this module implements, and `test_hookstep_newton.py` pins it with a
problem where damped Newton provably cannot converge and the hookstep does.

THE SUBPROBLEM. After k Arnoldi steps against the Jacobian action we have an
orthonormal basis Q (n x k+1) and an upper-Hessenberg H ((k+1) x k) with

    J Q[:, :k] = Q[:, :k+1] H                       (Arnoldi relation)

and the correction is sought as dx = Q[:, :k] y. Since Q has orthonormal
columns, ||dx|| = ||y||, so a trust region of radius delta on the step is
exactly a norm constraint on y, and the GMRES least-squares problem becomes

    minimise  || H y - beta e1 ||   subject to   ||y|| <= delta,     (*)

with beta = ||F||. This is the classic Levenberg-Marquardt / hook problem in a
k-dimensional subspace, where k is tiny (tens), so it is solved essentially for
free by an SVD of H: with H = U S V^T and g = beta * U^T e1,

    y(mu) = V diag(s_i / (s_i^2 + mu)) g,

which is the unconstrained least-squares solution at mu = 0 and shrinks
monotonically to 0 as mu -> infinity. If ||y(0)|| <= delta the constraint is
inactive and the plain GMRES step is taken; otherwise a scalar root-find
delivers the unique mu > 0 with ||y(mu)|| = delta.

THE PAYOFF THAT MAKES THIS AFFORDABLE. Every Arnoldi vector costs one Jacobian
action, which for an RPO residual is a full nonlinear time-integration over the
orbit period -- by far the dominant cost. But (*) can be re-solved at MANY
different radii using the SAME H, at no matvec cost at all. So the trust-region
loop tries a sequence of shrinking radii per Newton iteration, paying only one
residual evaluation per trial and ZERO extra Jacobian actions. That property is
why the hookstep is the literature's method of choice here and is preserved
explicitly below (`arnoldi` and `newton_hookstep` are separated for exactly this
reason; the radii loop lives inside one Arnoldi build).

SCOPE. This module is deliberately problem-agnostic: it takes a residual
callable and, optionally, a Jacobian-action callable, so it is testable on small
analytic systems with known answers rather than only through the flow solver.
`solver/kolmogorov2d_nkbasin.py` wires it to the RPO residual.

Ban screen (PROG-R4 pre-registration, Ban 1's literal wording): nothing in this
module continues a fixed point into an orbit. It is a root-finder; it has no
continuation parameter and no branch-following logic of any kind.
"""
from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------------
# Arnoldi: build the Krylov basis ONCE, keep H for repeated hookstep solves
# --------------------------------------------------------------------------

def arnoldi(matvec, b, maxiter=40, breakdown_tol=1e-14, rtol=None):
    """Arnoldi process on the Krylov space K_k(J, b), starting from b/||b||.

    Returns (Q, H, k, beta) where Q is (n, k+1) with orthonormal columns, H is
    (k+1, k) upper Hessenberg, k is the dimension actually built, and
    beta = ||b||. The Arnoldi relation J Q[:, :k] = Q[:, :k+1] H holds to
    round-off; `test_hookstep_newton.py` checks it directly.

    Unlike a GMRES driver, this returns the RAW H -- no Givens rotations are
    applied -- because the hookstep subproblem needs the full matrix to form
    its SVD at many trust-region radii.

    `rtol`, if given, stops the build as soon as the UNCONSTRAINED GMRES
    residual min||H y - beta e1|| falls below rtol * beta. This is what makes a
    large `maxiter` affordable rather than merely permitted: in this
    application one matvec is a full nonlinear time integration over the orbit
    period (seconds), so running a nominal 200-dimensional space to completion
    when 30 vectors already solve the linear model to 1e-3 wastes almost all of
    the budget. The stopping test itself is free by comparison -- a least
    squares on a (k+1) x k Hessenberg costs O(k^3) flops against O(k) full
    time integrations. The default stays None so the behaviour without it is
    exactly the fixed-dimension build the module's tests pin down.
    """
    b = np.asarray(b, dtype=float).ravel()
    n = b.shape[0]
    beta = float(np.linalg.norm(b))
    maxiter = int(min(maxiter, n))
    if maxiter < 1:
        raise ValueError(f"maxiter must be >= 1 and b non-empty, got n={n}")
    if beta == 0.0:
        return np.zeros((n, 1)), np.zeros((1, 0)), 0, 0.0

    Q = np.zeros((n, maxiter + 1))
    H = np.zeros((maxiter + 1, maxiter))
    Q[:, 0] = b / beta
    k_built = 0
    for k in range(maxiter):
        v = np.asarray(matvec(Q[:, k]), dtype=float).ravel()
        if v.shape[0] != n:
            raise ValueError(f"matvec returned shape {v.shape}, expected ({n},)")
        # modified Gram-Schmidt, one reorthogonalisation pass (the RPO Jacobian
        # is badly conditioned enough that classical MGS alone loses
        # orthogonality, which corrupts ||dx|| = ||y|| and hence the meaning of
        # the trust-region radius itself)
        for i in range(k + 1):
            h = float(np.dot(Q[:, i], v))
            H[i, k] += h
            v = v - h * Q[:, i]
        for i in range(k + 1):
            h = float(np.dot(Q[:, i], v))
            H[i, k] += h
            v = v - h * Q[:, i]
        hk = float(np.linalg.norm(v))
        H[k + 1, k] = hk
        k_built = k + 1
        if hk <= breakdown_tol * max(1.0, abs(H[k, k])):
            break  # happy breakdown: the solution lies in this subspace
        Q[:, k + 1] = v / hk
        if rtol is not None:
            rhs = np.zeros(k_built + 1)
            rhs[0] = beta
            y, *_ = np.linalg.lstsq(H[:k_built + 1, :k_built], rhs, rcond=None)
            if np.linalg.norm(H[:k_built + 1, :k_built] @ y - rhs) <= rtol * beta:
                break
    return Q[:, :k_built + 1], H[:k_built + 1, :k_built], k_built, beta


# --------------------------------------------------------------------------
# The hookstep subproblem, solved in the Krylov subspace
# --------------------------------------------------------------------------

def hookstep_subproblem(H, beta, delta, mu_tol=1e-12, max_bisect=200):
    """Solve   min ||H y - beta e1||   s.t. ||y|| <= delta.

    Returns a dict with y, mu, ynorm, model_residual (= ||H y - beta e1||,
    the linear model's predicted residual norm AFTER the step) and
    on_boundary (whether the trust-region constraint is active).

    delta = None or inf means "no constraint": the plain GMRES step.

    The root-find for mu uses the standard reformulation on 1/||y(mu)||, which
    is very nearly linear in mu and so bisects robustly; the secular function
    ||y(mu)|| itself is stiff near mu = 0.
    """
    H = np.asarray(H, dtype=float)
    kp1, k = H.shape
    if k == 0:
        return dict(y=np.zeros(0), mu=0.0, ynorm=0.0,
                    model_residual=float(beta), predicted_reduction_sq=0.0,
                    on_boundary=False)
    rhs = np.zeros(kp1)
    rhs[0] = float(beta)

    U, s, Vt = np.linalg.svd(H, full_matrices=False)  # H = U diag(s) Vt
    g = U.T @ rhs                                     # length min(kp1,k) = k

    def y_of(mu):
        if mu == 0.0:
            coef = np.where(s > 0, np.divide(g, s, out=np.zeros_like(g),
                                             where=s > 0), 0.0)
        else:
            coef = g * s / (s * s + mu)
        return Vt.T @ coef

    HtR = H.T @ rhs   # cached for the cancellation-free predicted reduction

    def predicted_reduction_sq(y):
        """beta^2 - ||H y - beta e1||^2, computed WITHOUT cancellation.

        Expanding, ||Hy - rhs||^2 = ||Hy||^2 - 2 y.(H^T rhs) + beta^2, so the
        model's reduction in the SQUARED residual is exactly

            2 y.(H^T rhs) - ||H y||^2

        with no subtraction of two nearly-equal large numbers. This matters at
        small trust-region radii, where beta and ||Hy - rhs|| agree to nearly
        machine precision and the naive difference underflows to zero or goes
        negative -- which makes the ratio test reject perfectly good small
        steps and collapses the trust region. That failure was observed here
        before this form replaced the naive one.
        """
        return float(2.0 * (y @ HtR) - np.dot(H @ y, H @ y))

    y0 = y_of(0.0)
    n0 = float(np.linalg.norm(y0))
    if delta is None or not np.isfinite(delta) or n0 <= delta:
        return dict(y=y0, mu=0.0, ynorm=n0,
                    model_residual=float(np.linalg.norm(H @ y0 - rhs)),
                    predicted_reduction_sq=predicted_reduction_sq(y0),
                    on_boundary=False)

    # ||y(mu)|| is strictly decreasing in mu; bracket then bisect on
    # phi(mu) = 1/delta - 1/||y(mu)||, which has the same unique root.
    lo, hi = 0.0, max(1.0, float(s[0] ** 2))
    for _ in range(200):
        if float(np.linalg.norm(y_of(hi))) <= delta:
            break
        hi *= 4.0
    for _ in range(max_bisect):
        mid = 0.5 * (lo + hi)
        nm = float(np.linalg.norm(y_of(mid)))
        if abs(nm - delta) <= mu_tol * delta:
            lo = hi = mid
            break
        if nm > delta:
            lo = mid
        else:
            hi = mid
    mu = 0.5 * (lo + hi)
    y = y_of(mu)
    return dict(y=y, mu=float(mu), ynorm=float(np.linalg.norm(y)),
                model_residual=float(np.linalg.norm(H @ y - rhs)),
                predicted_reduction_sq=predicted_reduction_sq(y),
                on_boundary=True)


# --------------------------------------------------------------------------
# The Newton-GMRES-hookstep driver
# --------------------------------------------------------------------------

def newton_hookstep(residual, x0, jac_matvec=None, tol=1e-9, max_newton=25,
                    max_gmres=40, gmres_rtol=None,
                    fd_eps=1e-7, delta0=None, delta_max=None,
                    delta_min_rel=1e-10, eta_accept=1e-4, shrink=0.5,
                    expand=2.0, rho_shrink=0.25, rho_expand=0.75,
                    max_radius_trials=20, verbose=False, callback=None):
    """Matrix-free Newton with a hookstep (trust-region) globalisation.

    residual(x) -> F(x), an array of the same length as x (square system).
    jac_matvec(x, F, v) -> J(x) v; if None, a one-sided finite difference of
        `residual` is used, with step fd_eps * max(1, ||x||) / ||v||.

    Trust-region bookkeeping is the standard one: rho = actual reduction over
    predicted reduction, where "reduction" is in ||F|| (not the usual (1/2)||F||^2
    merit -- ||F|| is what the Krylov model directly predicts, so the ratio is
    formed in the same currency the model speaks). rho < rho_shrink shrinks the
    radius, rho > rho_expand with an active constraint expands it, and steps
    with rho <= eta_accept are rejected outright.

    Returns a dict: success, x, n_iters, residual_history, final_residual,
    reason, ledger (per-iteration records), n_residual_evals, n_jac_evals.
    """
    x = np.array(x0, dtype=float).ravel()
    n = x.shape[0]
    counts = dict(res=0, jac=0)

    def F_of(xx):
        counts["res"] += 1
        out = np.asarray(residual(xx), dtype=float).ravel()
        if out.shape[0] != n:
            raise ValueError(f"residual returned shape {out.shape}, expected ({n},)")
        return out

    F = F_of(x)
    r = float(np.linalg.norm(F))
    hist = [r]
    ledger = []
    delta = delta0
    if delta_max is None:
        delta_max = np.inf
    reason = "max_newton_hit"

    for it in range(max_newton):
        if verbose:
            print(f"  hookstep it {it}: |R|={r:.6e} delta={delta}")
        if not np.isfinite(r):
            reason = "nonfinite_residual"
            break
        if r < tol:
            reason = "converged"
            break

        scale = max(1.0, float(np.linalg.norm(x)))

        if jac_matvec is None:
            def matvec(v, x=x, F=F, scale=scale):
                counts["jac"] += 1
                nv = float(np.linalg.norm(v))
                if nv == 0.0:
                    return np.zeros(n)
                eps = fd_eps * scale / nv
                return (F_of(x + eps * v) - F) / eps
        else:
            def matvec(v, x=x, F=F):
                counts["jac"] += 1
                return np.asarray(jac_matvec(x, F, v), dtype=float).ravel()

        # ONE Arnoldi build per Newton iteration; every trust-region radius
        # below re-uses it, so shrinking the radius costs no Jacobian actions.
        Q, H, k, beta = arnoldi(matvec, -F, maxiter=max_gmres,
                                rtol=gmres_rtol)
        if k == 0:
            reason = "krylov_breakdown"
            break

        # unconstrained GMRES step: sets the initial radius if none was given
        sub0 = hookstep_subproblem(H, beta, None)
        dx_full_norm = float(np.linalg.norm(sub0["y"]))
        if delta is None:
            delta = min(dx_full_norm, delta_max) if dx_full_norm > 0 else 1.0
        delta_floor = delta_min_rel * scale

        accepted = False
        trials = []
        for _trial in range(max_radius_trials):
            sub = hookstep_subproblem(H, beta, delta)
            y = sub["y"]
            dx = Q[:, :k] @ y
            step_norm = float(np.linalg.norm(dx))
            # Ratio test in the SQUARED currency, so the predicted reduction can
            # be formed without cancellation (see predicted_reduction_sq).
            predicted = sub["predicted_reduction_sq"]
            x_try = x + dx
            F_try = F_of(x_try)
            r_try = float(np.linalg.norm(F_try))
            actual = r * r - r_try * r_try
            rho = actual / predicted if predicted > 0 else -np.inf
            trials.append(dict(delta=float(delta), mu=float(sub["mu"]),
                               step_norm=step_norm,
                               on_boundary=bool(sub["on_boundary"]),
                               predicted_reduction=float(predicted),
                               actual_reduction=float(actual),
                               rho=float(rho) if np.isfinite(rho) else None,
                               residual_after=r_try))
            # Acceptance rests on a STRICT decrease of ||F||, with rho driving
            # the radius. This is deliberate, and it is what makes the
            # comparison against a step-halving line search a clean experiment:
            # both methods then accept a step on exactly the same criterion, so
            # the ONLY difference between them is the DIRECTION the step points
            # -- rotated by the trust region, or merely rescaled by the line
            # search. Requiring rho > eta_accept as well would additionally
            # reject steps whose predicted and actual reductions are both at the
            # rounding floor, which is a numerical artifact rather than a
            # property of the problem.
            good_ratio = (rho > eta_accept) or not (predicted > 0)
            if np.isfinite(r_try) and r_try < r and good_ratio:
                accepted = True
                if rho > rho_expand and sub["on_boundary"]:
                    delta = min(expand * delta, delta_max)
                break
            delta = shrink * delta
            if delta < delta_floor:
                break
        ledger.append(dict(iteration=it, residual_before=r,
                           krylov_dim=int(k),
                           gmres_step_norm=dx_full_norm,
                           n_radius_trials=len(trials),
                           accepted=bool(accepted),
                           trials=trials,
                           delta_after=float(delta),
                           residual_after=float(r_try) if accepted else float(r)))
        if callback is not None:
            callback(ledger[-1])
        if not accepted:
            reason = "trust_region_collapsed"
            break
        x, F, r = x_try, F_try, r_try
        hist.append(r)

    if reason == "max_newton_hit" and r < tol:
        reason = "converged"
    return dict(success=bool(r < tol), x=x, n_iters=len(hist) - 1,
                residual_history=hist, final_residual=float(r), reason=reason,
                ledger=ledger, n_residual_evals=counts["res"],
                n_jac_evals=counts["jac"])
