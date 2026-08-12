"""2-D Kolmogorov flow: pseudospectral DNS, recurrence-flow guess generation,
and a matrix-free Newton-Krylov + phase-condition solver for relative periodic
orbits (RPOs) -- Route-DSSP brick B5 (DSSP-NKBASIN, plan sec 5.1).

TARGET OBJECT (pinned in writeup/novelty/leg_353.md, novelty pass completed
first): Lucas & Kerswell 2015 (arXiv:1406.1820v2, Phys. Fluids 27, 045106),
their Table IV row "UPO 37": a relative periodic orbit of 2-D Kolmogorov flow
at Re=60, forcing wavenumber n=4, square torus alpha=1 (domain [0,2*pi)^2),
with published period T=19.334 and x-translation shift s=0.375 (m=0, i.e. no
extra discrete y-shift/reflect component). This module sets up the IDENTICAL
dynamical system (same equations, Re, n, domain, symmetry group) the paper
uses, so that the recovery it performs can be checked against the paper's own
published (T, s) and Fig. 4-style dissipation/energy-input invariants -- see
the novelty pass for exactly what is and is not available from the paper text
(no bit-for-bit initial-condition data; T, s and qualitative diagnostics are
the only published numbers that a Newton search can be checked against).

GOVERNING EQUATIONS (Lucas & Kerswell eq. 3-6, alpha=1, n=n_forcing):

    domega/dt + u.grad(omega) = (1/Re) Lap(omega) - n*cos(n*y)
    u = (-psi_y, psi_x),  Lap(psi) = omega           (Biot-Savart)

on the doubly 2*pi-periodic square. Vorticity-streamfunction pseudospectral
method: full fft2 (complex spectra, real fields), 2/3-rule dealiasing on the
quadratic advection product, RK4 on the nonlinear+forcing terms with an EXACT
integrating factor exp(-Ksq*dt/Re) for the linear viscous term applied after
each RK4 step -- the same splitting solver/boussinesq.py uses for the analogous
2D vorticity system (independently written here, not imported: this module is
its own territory, disjoint from B2-B4's modules per the plan's B5 entry).

NEWTON-KRYLOV + PHASE-CONDITION LAYER. An RPO with pure x-translation symmetry
(m=0) satisfies

    shift_x(Phi_T(omega0), s) = omega0

where Phi_T is the T-time flow map. This is `state_dim` equations in
`state_dim + 2` unknowns (omega0, T, s) -- the +2 continuous degeneracy is the
1-parameter time-translation invariance along the orbit (which point on the
orbit is "t=0") and the 1-parameter x-translation invariance of omega0 itself
(which representative of the translation-orbit is being called "omega0"). Both
are removed by a moving Poincare-section PHASE CONDITION, evaluated at the
current Newton iterate x_k = (omega0_k, T_k, s_k):

    phase A (kills time-translation slip):  <RHS(omega0_k), omega0-omega0_k> = 0
    phase B (kills x-translation slip):      <d(omega0_k)/dx, omega0-omega0_k> = 0

Together with the state residual this is a SQUARE (state_dim+2)-dimensional
system, solved by Newton's method with the correction step found via
matrix-free GMRES (Jacobian-vector products by one-sided finite differences of
the whole extended residual) -- i.e. genuine Newton-Krylov, not a dense
Jacobian (the plan's B5 gate names the method; this is what it means run
literally). No hookstep/trust-region globalisation is implemented (a
simplification from Viswanath's/the paper's own "Newton-GMRES-hookstep":
plain Newton with step-halving line search is used instead); this is recorded
here and in the leg's journal rather than silently presented as identical to
the paper's algorithm.

Runtime note (ORCHESTRATION.md "assess before you run anything long"): every
integration in this module runs at FIXED dt (no adaptive CFL controller) so
the flow map is a smooth, reproducible function of (omega0, T) for finite
differencing. Resolution is deliberately modest (default N=24, i.e. state_dim
= 576) -- the paper's own reduced recurrence criterion (their eq. 15) already
established that this orbit's near-recurrence signature lives in the 8
largest Fourier modes each direction, and this leg's runtime budget (heavy,
2-leg ceiling) does not afford the paper's own 128x128 resolution or its
T=5e6 recurrence-mining DNS.
"""
from __future__ import annotations

import numpy as np

from solver.hookstep_newton import newton_hookstep

TWO_PI = 2.0 * np.pi


# --------------------------------------------------------------------------
# Grid, spectral operators, forcing (mirrors the vorticity-streamfunction
# machinery in solver/boussinesq.py structurally; written independently here,
# no import, so this module owns its own territory outright).
# --------------------------------------------------------------------------

def grid2d(N):
    x = TWO_PI * np.arange(N) / N
    return np.meshgrid(x, x, indexing="ij")  # X, Y ; axis0=x, axis1=y


def wavenumbers2d(N):
    k = np.fft.fftfreq(N, d=1.0 / N)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    Ksq = KX * KX + KY * KY
    inv_Ksq = np.zeros_like(Ksq)
    nz = Ksq > 0
    inv_Ksq[nz] = 1.0 / Ksq[nz]
    return KX, KY, Ksq, inv_Ksq


def dealias_mask2d(N):
    k = np.fft.fftfreq(N, d=1.0 / N)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    cut = N / 3.0
    return (np.abs(KX) <= cut) & (np.abs(KY) <= cut)


def velocity_from_vorticity(w_hat, KX, KY, inv_Ksq):
    u_hat = 1j * KY * w_hat * inv_Ksq
    v_hat = -1j * KX * w_hat * inv_Ksq
    return np.fft.ifft2(u_hat).real, np.fft.ifft2(v_hat).real


class Kolmogorov2D:
    """Fixed-parameter (Re, n_forcing, N) container for the spectral operators
    and a fixed-dt RK4 + integrating-factor time-stepper."""

    def __init__(self, N=24, Re=60.0, n_forcing=4, dt=0.01):
        if int(N) != N or N < 6:
            raise ValueError(f"N must be an integer >= 6, got {N!r}")
        N = int(N)
        self.N = N
        self.Re = float(Re)
        self.n_forcing = int(n_forcing)
        self.dt = float(dt)
        self.KX, self.KY, self.Ksq, self.inv_Ksq = wavenumbers2d(N)
        self.mask = dealias_mask2d(N)
        if not np.any(self.mask & (self.Ksq > 0.0)):
            raise ValueError(f"N={N} leaves the 2/3 mask with only the mean mode")
        X, Y = grid2d(N)
        self.X, self.Y = X, Y
        forcing_phys = -self.n_forcing * np.cos(self.n_forcing * Y)
        self.forcing_hat = np.fft.fft2(forcing_phys)
        self.decay = np.exp(-self.Ksq / self.Re * self.dt)  # exact viscous factor
        self.state_dim = N * N

    # -- RHS of the non-stiff part: -(u.grad w) + forcing, dealiased -------
    def _rhs_hat(self, w_hat):
        u, v = velocity_from_vorticity(w_hat, self.KX, self.KY, self.inv_Ksq)
        wx = np.fft.ifft2(1j * self.KX * w_hat).real
        wy = np.fft.ifft2(1j * self.KY * w_hat).real
        adv_hat = np.fft.fft2(u * wx + v * wy) * self.mask
        return -adv_hat + self.forcing_hat

    def _rk4_step(self, w_hat, dt):
        decay = np.exp(-self.Ksq / self.Re * dt) if dt != self.dt else self.decay
        k1 = self._rhs_hat(w_hat)
        k2 = self._rhs_hat(w_hat + 0.5 * dt * k1)
        k3 = self._rhs_hat(w_hat + 0.5 * dt * k2)
        k4 = self._rhs_hat(w_hat + dt * k3)
        w_hat = w_hat + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        return w_hat * decay

    def rhs_physical(self, w):
        """d(omega)/dt in physical space, at fixed omega (for the phase A
        condition, which needs RHS(omega0_k) -- the FULL rhs including
        viscosity, not just the nonstiff part)."""
        w_hat = np.fft.fft2(w) * self.mask
        nonstiff = self._rhs_hat(w_hat)
        visc = -(self.Ksq / self.Re) * w_hat
        return np.fft.ifft2(nonstiff + visc).real

    def integrate(self, w0, T, save_times=None):
        """Integrate the real field w0 forward by T at fixed self.dt (last
        step shortened to land exactly on T). save_times: optional sorted
        array of times in [0,T] to also record (nearest-step snapshots);
        returns (w_final, saved) where saved is a list of (t, w) pairs."""
        w0 = np.asarray(w0, dtype=float)
        if w0.shape != (self.N, self.N):
            raise ValueError(f"w0 must be ({self.N},{self.N}), got {w0.shape}")
        w_hat = np.fft.fft2(w0) * self.mask
        t = 0.0
        saved = []
        save_times = [] if save_times is None else sorted(save_times)
        si = 0
        while t < T - 1e-12:
            dt = min(self.dt, T - t)
            w_hat = self._rk4_step(w_hat, dt)
            t += dt
            while si < len(save_times) and save_times[si] <= t + 1e-9:
                saved.append((t, np.fft.ifft2(w_hat).real))
                si += 1
        return np.fft.ifft2(w_hat).real, saved

    # -- diagnostics, eq. (10)/(13) ----------------------------------------
    def diagnostics(self, w):
        w_hat = np.fft.fft2(w) * self.mask
        u, v = velocity_from_vorticity(w_hat, self.KX, self.KY, self.inv_Ksq)
        E = 0.5 * float(np.mean(u * u + v * v))
        D = (1.0 / self.Re) * float(np.mean(w * w))  # int|grad u|^2 == int w^2 (2D)
        I = float(np.mean(u * np.sin(self.n_forcing * self.Y)))
        return E, D, I

    @property
    def D_lam(self):
        return self.Re / (2.0 * self.n_forcing ** 2)

    @property
    def E_lam(self):
        return self.Re ** 2 / (4.0 * self.n_forcing ** 2)


# --------------------------------------------------------------------------
# x-translation shift and optimal-shift near-recurrence residual
# --------------------------------------------------------------------------

def shift_x(w, s, KX=None, N=None):
    """Translate a real field w(x,y) -> w(x-s, y) [so that shift_x(w,s)
    evaluated at x equals w at x-s -- consistent with eq. (14)'s T_s acting
    by argument shift] via a Fourier phase multiply."""
    N = w.shape[0] if N is None else N
    if KX is None:
        KX, _, _, _ = wavenumbers2d(N)
    w_hat = np.fft.fft2(w)
    w_hat = w_hat * np.exp(-1j * KX * s)
    return np.fft.ifft2(w_hat).real


def optimal_shift_residual(w1, w2, n_grid=None):
    """min_s ||shift_x(w2,s) - w1||^2 / ||w1||^2, found by an FFT
    cross-correlation over discrete shifts (exact for the grid's own shift
    resolution) then a parabolic refinement near the discrete optimum.
    Returns (best_s, relative_residual)."""
    N = w1.shape[0]
    if n_grid is None:
        n_grid = N
    w1_hat_x = np.fft.fft(w1, axis=0)
    w2_hat_x = np.fft.fft(w2, axis=0)
    # C[j] = sum_{x,y} w1(x,y) w2(x+j,y) = R(-j) where R(s) = sum w1(x+s)w2(x)
    # is the quantity maximised by the TRUE shift solving shift_x(w2,s)=w1
    # (shift_x(w,s)(x)=w(x-s)); so the correlation peak sits at j = -s_best,
    # i.e. s_best = -j_peak (NOT +j_peak -- verified against a synthetic
    # shift_x-constructed pair in test_kolmogorov2d_nkbasin.py, which is what
    # caught this sign bug).
    cross = np.fft.ifft(np.conj(w1_hat_x) * w2_hat_x, axis=0).real
    C = cross.sum(axis=1)  # length N, C[j]
    j_best = int(np.argmax(C))
    # parabolic refine around j_best using neighbours (periodic wrap)
    jm, jp = (j_best - 1) % N, (j_best + 1) % N
    c0, cm, cp = C[j_best], C[jm], C[jp]
    denom = (cm - 2 * c0 + cp)
    frac = 0.5 * (cm - cp) / denom if abs(denom) > 1e-14 else 0.0
    frac = max(-1.0, min(1.0, frac))
    s_best = -(j_best + frac) * (TWO_PI / N)
    w2_shift = shift_x(w2, s_best, N=N)
    num = float(np.sum((w2_shift - w1) ** 2))
    den = float(np.sum(w1 ** 2))
    rel = num / den if den > 0 else np.inf
    return s_best, rel


# --------------------------------------------------------------------------
# Extended residual for the Newton-Krylov + phase-condition layer
# --------------------------------------------------------------------------

def pack(w0, T, s):
    return np.concatenate([w0.ravel(), [T, s]])


def unpack(x, N):
    w0 = x[:-2].reshape(N, N)
    return w0, float(x[-2]), float(x[-1])


def extended_residual(x, solver, ref_w0, ref_rhs, ref_dwdx):
    """R(x) in R^{state_dim+2}: state_dim rows of shift_x(Phi_T(w0),s)-w0,
    plus the two phase conditions evaluated against the FIXED reference
    (ref_w0, ref_rhs=RHS(ref_w0), ref_dwdx=d(ref_w0)/dx) -- the reference is
    the outer Newton iterate x_k, held fixed across one GMRES solve/finite
    difference so the phase rows are exactly linear in the correction."""
    N = solver.N
    w0, T, s = unpack(x, N)
    if T <= 0:
        # keep the map well-defined (finite-diff probes can wander here);
        # penalise instead of raising, so GMRES sees a smooth-enough residual
        T_eff = 1e-3
    else:
        T_eff = T
    wT, _ = solver.integrate(w0, T_eff)
    state_res = (shift_x(wT, s, KX=solver.KX, N=N) - w0).ravel()
    delta = w0 - ref_w0
    phase_a = float(np.sum(ref_rhs * delta))
    phase_b = float(np.sum(ref_dwdx * delta))
    return np.concatenate([state_res, [phase_a, phase_b]])


# --------------------------------------------------------------------------
# Homemade matrix-free GMRES (no scipy in this environment)
# --------------------------------------------------------------------------

def gmres_matrix_free(matvec, b, maxiter=40, tol=1e-6):
    """Full (non-restarted) GMRES via Arnoldi, matrix-free. Returns
    (x, residual_history). x0 = 0."""
    n = b.shape[0]
    beta = np.linalg.norm(b)
    if beta == 0.0:
        return np.zeros(n), [0.0]
    maxiter = min(maxiter, n)
    Q = np.zeros((n, maxiter + 1))
    H = np.zeros((maxiter + 1, maxiter))
    Q[:, 0] = b / beta
    g = np.zeros(maxiter + 1)
    g[0] = beta
    cs = np.zeros(maxiter)
    sn = np.zeros(maxiter)
    resid_hist = [beta]
    k_used = 0
    for k in range(maxiter):
        v = matvec(Q[:, k])
        for i in range(k + 1):
            H[i, k] = np.dot(Q[:, i], v)
            v = v - H[i, k] * Q[:, i]
        H[k + 1, k] = np.linalg.norm(v)
        k_used = k + 1
        if H[k + 1, k] > 1e-14:
            Q[:, k + 1] = v / H[k + 1, k]
        # apply previous Givens rotations
        for i in range(k):
            temp = cs[i] * H[i, k] + sn[i] * H[i + 1, k]
            H[i + 1, k] = -sn[i] * H[i, k] + cs[i] * H[i + 1, k]
            H[i, k] = temp
        denom = np.hypot(H[k, k], H[k + 1, k])
        if denom < 1e-300:
            cs[k], sn[k] = 1.0, 0.0
        else:
            cs[k] = H[k, k] / denom
            sn[k] = H[k + 1, k] / denom
        H[k, k] = cs[k] * H[k, k] + sn[k] * H[k + 1, k]
        H[k + 1, k] = 0.0
        g[k + 1] = -sn[k] * g[k]
        g[k] = cs[k] * g[k]
        resid_hist.append(abs(g[k + 1]))
        if abs(g[k + 1]) < tol * beta:
            break
    y = np.zeros(k_used)
    Hs = H[:k_used, :k_used]
    gs = g[:k_used]
    y = np.linalg.solve(Hs, gs) if k_used > 0 else y
    x = Q[:, :k_used] @ y
    return x, resid_hist


# --------------------------------------------------------------------------
# Newton-Krylov RPO solver
# --------------------------------------------------------------------------

def newton_krylov_rpo(w0_guess, T_guess, s_guess, solver,
                       tol=1e-9, max_newton=25, max_gmres=40,
                       fd_eps=1e-6, verbose=False):
    """Converge (w0, T, s) to an RPO by Newton's method with the correction
    found via matrix-free GMRES, phase conditions re-linearised at every
    outer iterate (moving Poincare section). Plain-Newton line search
    (step-halving on ||R|| increase) substitutes for the hookstep.

    Returns a dict: success, w0, T, s, n_iters, residual_history,
    final_residual, reason.
    """
    N = solver.N
    w0 = np.array(w0_guess, dtype=float)
    T, s = float(T_guess), float(s_guess)
    hist = []
    for it in range(max_newton):
        ref_rhs = solver.rhs_physical(w0)
        w0_hat = np.fft.fft2(w0) * solver.mask
        ref_dwdx = np.fft.ifft2(1j * solver.KX * w0_hat).real
        x0 = pack(w0, T, s)
        F0 = extended_residual(x0, solver, w0, ref_rhs, ref_dwdx)
        r0 = float(np.linalg.norm(F0))
        hist.append(r0)
        if verbose:
            print(f"  newton it {it}: |R|={r0:.6e}  T={T:.6f} s={s:.6f}")
        if r0 < tol:
            return dict(success=True, w0=w0, T=T, s=s, n_iters=it,
                        residual_history=hist, final_residual=r0,
                        reason="converged")
        if not np.isfinite(r0):
            return dict(success=False, w0=w0, T=T, s=s, n_iters=it,
                        residual_history=hist, final_residual=r0,
                        reason="nonfinite_residual")

        scale = max(1.0, float(np.linalg.norm(x0)))

        def matvec(v, x0=x0, F0=F0, scale=scale):
            eps = fd_eps * scale / max(np.linalg.norm(v), 1e-14)
            Fp = extended_residual(x0 + eps * v, solver, w0, ref_rhs, ref_dwdx)
            return (Fp - F0) / eps

        dx, _ = gmres_matrix_free(matvec, -F0, maxiter=max_gmres, tol=1e-3)

        # step-halving line search
        lam = 1.0
        accepted = False
        for _ in range(8):
            x_try = x0 + lam * dx
            w0_try, T_try, s_try = unpack(x_try, N)
            if T_try <= 0:
                lam *= 0.5
                continue
            F_try = extended_residual(x_try, solver, w0, ref_rhs, ref_dwdx)
            r_try = float(np.linalg.norm(F_try))
            if np.isfinite(r_try) and r_try < r0:
                accepted = True
                break
            lam *= 0.5
        if not accepted:
            return dict(success=False, w0=w0, T=T, s=s, n_iters=it,
                        residual_history=hist, final_residual=r0,
                        reason="line_search_failed")
        w0, T, s = w0_try, T_try, s_try

    ref_rhs = solver.rhs_physical(w0)
    w0_hat = np.fft.fft2(w0) * solver.mask
    ref_dwdx = np.fft.ifft2(1j * solver.KX * w0_hat).real
    F_final = extended_residual(pack(w0, T, s), solver, w0, ref_rhs, ref_dwdx)
    r_final = float(np.linalg.norm(F_final))
    hist.append(r_final)
    return dict(success=r_final < tol, w0=w0, T=T, s=s, n_iters=max_newton,
                residual_history=hist, final_residual=r_final,
                reason="converged" if r_final < tol else "max_newton_hit")


# --------------------------------------------------------------------------
# Newton-GMRES-hookstep RPO solver (PROG-R4 U1 / milestone M1)
# --------------------------------------------------------------------------

def newton_hookstep_rpo(w0_guess, T_guess, s_guess, solver,
                        tol=1e-9, max_newton=25, max_gmres=40,
                        gmres_rtol=None, fd_eps=1e-6, delta0=None,
                        delta_max=None, verbose=False):
    """As newton_krylov_rpo, but the step is globalised by a genuine
    trust-region hookstep (Viswanath 2007) instead of step-halving: the
    correction is constrained INSIDE the Krylov subspace, so shrinking the
    radius ROTATES the step rather than merely rescaling it.

    Structure. The residual's two phase rows are evaluated against a FIXED
    reference (the current outer iterate), so the residual MAP changes
    whenever the iterate is accepted. One "epoch" below is therefore one
    outer Newton step at one fixed reference -- exactly the moving Poincare
    section newton_krylov_rpo already uses. The trust-region radius is
    THREADED across epochs (a trust region that reset every step would not be
    a trust region), and the per-epoch ledger is concatenated so the caller
    sees one continuous per-iteration record.

    Returns a dict: success, w0, T, s, n_iters, residual_history,
    final_residual, reason, ledger, n_residual_evals, n_jac_evals.
    """
    N = solver.N
    w0 = np.array(w0_guess, dtype=float)
    T, s = float(T_guess), float(s_guess)
    hist = []
    ledger = []
    delta = delta0
    n_jac = 0
    r = float("nan")
    reason = "max_newton_hit"
    # Every finite-difference probe is a full nonlinear integration over the
    # orbit period, so it is counted as a residual evaluation wherever it is
    # issued from -- including the domain-safe action below, which calls the
    # residual directly and so bypasses the generic counter.
    probe_count = [0]

    for epoch in range(max_newton):
        ref_rhs = solver.rhs_physical(w0)
        w0_hat = np.fft.fft2(w0) * solver.mask
        ref_dwdx = np.fft.ifft2(1j * solver.KX * w0_hat).real
        ref_w0 = w0

        def resid(xx, ref_w0=ref_w0, ref_rhs=ref_rhs, ref_dwdx=ref_dwdx):
            # T > 0 is a DOMAIN constraint, and the trust region is the right
            # place to enforce it: returning a non-finite residual makes the
            # radius loop reject the trial and shrink, which is exactly the
            # behaviour wanted, and it costs no time integration. The
            # alternative (extended_residual's T_eff floor) silently evaluates
            # a DIFFERENT problem at negative T and would corrupt the ratio
            # test. Note this leaves extended_residual itself untouched, so
            # leg 353's line-search path is bit-for-bit unchanged.
            if xx[-2] <= 0.0:
                return np.full(xx.shape[0], np.inf)
            probe_count[0] += 1
            return extended_residual(xx, solver, ref_w0, ref_rhs, ref_dwdx)

        def jac_mv(xx, Fx, v, scale_ref=None):
            # The generic finite-difference action in hookstep_newton probes
            # xx + eps*v with eps set only by ||v||, which can step THROUGH
            # T = 0 and hand the Arnoldi a non-finite column. The domain
            # constraint therefore has to be honoured by the probe as well as
            # by the trial step, so this RPO-specific action shrinks eps until
            # the probe stays inside T > 0 (at worst halving the current T).
            # A directional difference over a shorter baseline is still a
            # consistent one-sided approximation of the same derivative.
            nv = float(np.linalg.norm(v))
            if nv == 0.0:
                return np.zeros(xx.shape[0])
            sc = max(1.0, float(np.linalg.norm(xx)))
            eps = fd_eps * sc / nv
            if v[-2] < 0.0:
                eps = min(eps, 0.5 * xx[-2] / (-v[-2]))
            return (resid(xx + eps * v) - Fx) / eps

        out = newton_hookstep(resid, pack(w0, T, s), jac_matvec=jac_mv,
                              tol=tol, max_newton=1,
                              max_gmres=max_gmres, gmres_rtol=gmres_rtol,
                              fd_eps=fd_eps,
                              delta0=delta, delta_max=delta_max)
        n_jac += out["n_jac_evals"]
        r = float(out["residual_history"][0])
        hist.append(r)
        if verbose:
            print(f"  hookstep epoch {epoch}: |R|={r:.6e} "
                  f"T={T:.6f} s={s:.6f} delta={delta}")

        if out["reason"] == "nonfinite_residual":
            reason = "nonfinite_residual"
            break
        if not out["ledger"]:
            # No inner iteration ran. That includes convergence AT ENTRY, in
            # which case r above is already the converged residual and the
            # iterate is unmoved, so out["reason"] carries straight through.
            reason = out["reason"]
            break

        entry = dict(out["ledger"][-1])
        entry["iteration"] = epoch
        entry["T_before"] = T
        entry["s_before"] = s
        ledger.append(entry)
        delta = entry["delta_after"]

        if not entry["accepted"]:
            reason = "trust_region_collapsed"
            break

        w0_try, T_try, s_try = unpack(out["x"], N)
        if T_try <= 0:
            reason = "nonpositive_period"
            break
        w0, T, s = w0_try, T_try, s_try

        if out["reason"] == "converged":
            # The inner call ran with max_newton=1, so reaching here means it
            # converged ON THE STEP JUST ACCEPTED: hookstep_newton upgrades
            # "max_newton_hit" to "converged" AFTER the step, and the converged
            # pair is (out["x"], out["final_residual"]) while
            # residual_history[0] -- what r was read from above -- is the
            # PRE-step value. Breaking on r would discard the solution and
            # return success=False on a solve that reached tol. Control P
            # caught exactly this: an exact planted fixed point reported
            # "converged" with final_residual 1.6e-8 > tol=1e-8.
            r = float(out["final_residual"])
            hist.append(r)
            reason = "converged"
            break

    return dict(success=bool(r < tol), w0=w0, T=T, s=s,
                n_iters=len(hist) - 1, residual_history=hist,
                final_residual=r, reason=reason, ledger=ledger,
                n_residual_evals=probe_count[0], n_jac_evals=n_jac)


# --------------------------------------------------------------------------
# Basin-radius measurement: perturb a converged RPO and re-run Newton
# --------------------------------------------------------------------------

def measure_basin_radius(w0_star, T_star, s_star, solver, eps_values,
                          n_trials=3, rng=None, tol=1e-9, max_newton=20,
                          max_gmres=40, fd_eps=1e-6,
                          match_T_tol=0.05, match_s_tol=0.05):
    """For each perturbation magnitude eps in eps_values (relative L2 norm of
    w0_star), run n_trials random-direction perturbations, Newton from
    (w0_star+perturbation, T_star, s_star), and record whether Newton (a)
    converges AND (b) lands back on the SAME orbit (|T-T_star|<match_T_tol
    and the shift matches mod 2pi within match_s_tol). Returns a list of
    per-eps dicts with success counts, plus the measured basin radius (the
    largest tested eps with 100% success immediately followed by the first
    eps with <100% success, i.e. the bracket the measurement resolves)."""
    if rng is None:
        rng = np.random.default_rng(0)
    scale = float(np.linalg.norm(w0_star))
    results = []
    for eps in eps_values:
        successes = 0
        trial_records = []
        for trial in range(n_trials):
            direction = rng.standard_normal(w0_star.shape)
            direction /= np.linalg.norm(direction)
            w0_pert = w0_star + eps * scale * direction
            out = newton_krylov_rpo(w0_pert, T_star, s_star, solver,
                                     tol=tol, max_newton=max_newton,
                                     max_gmres=max_gmres, fd_eps=fd_eps)
            ds = abs(((out["s"] - s_star + np.pi) % TWO_PI) - np.pi)
            same_orbit = (out["success"]
                          and abs(out["T"] - T_star) < match_T_tol
                          and ds < match_s_tol)
            if same_orbit:
                successes += 1
            trial_records.append(dict(success=out["success"],
                                       same_orbit=bool(same_orbit),
                                       T=out["T"], s=out["s"],
                                       n_iters=out["n_iters"],
                                       final_residual=out["final_residual"]))
        results.append(dict(eps=float(eps), successes=successes,
                             n_trials=n_trials, trials=trial_records))
    # basin radius bracket: largest eps with successes==n_trials, and the
    # first eps (in the given, assumed-increasing order) with successes<n_trials
    radius_ok = None
    radius_fail = None
    for r in results:
        if r["successes"] == r["n_trials"]:
            radius_ok = r["eps"]
        elif radius_fail is None:
            radius_fail = r["eps"]
    return dict(results=results, radius_lower_bound=radius_ok,
                radius_upper_bound=radius_fail)
