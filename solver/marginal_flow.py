"""The marginal flow, DRIVEN: time integration of the augmented system (Omega, mu).

ROUTE I v1.  Route-H v1 (§29) wrote down the augmented flow

    Omega_tau = (c_omega + H Omega) Omega - X Omega_X - a U Omega_X
                                                     - mu Lambda^{2s} Omega ,   (F_mu)
    mu_tau    = (2 s - alpha[Omega, mu]) mu ,        alpha = -c_omega ,          (M)

and then read it *statically*: it solved (F_mu) for a family of FROZEN mu with Newton,
read alpha(mu) off the branch, and inferred what (M) would do.  Two numbers came out
of that reading and neither was ever integrated:

    lambda_mu = 2 s - alpha_0     the growth rate of mu at the inviscid fixed point,
                                  i.e. Route-F's critical exponent s_c in spectral
                                  clothing (lambda_mu = 0 <=> s = s_c);
    alpha_1   = d alpha / d mu    the coefficient of the quadratic that decides the
                                  MARGINAL case, where lambda_mu vanishes identically.

This module integrates (F_mu)+(M) as a coupled initial-value problem and measures both
as properties of a TRAJECTORY.  That is a different computation, not a re-run: Newton
on a frozen-mu branch and BDF2 on the coupled flow share the residual and nothing else
-- no fitted constant, no shared linear solve, and the trajectory is free to leave the
branch, which is exactly the thing the static reading had to assume it would not do.

--------------------------------------------------------------------------
THE QUESTION THE LEG IS ACTUALLY FOR
--------------------------------------------------------------------------
Ranked item (2) has one piece left after §27 and §28 closed its scaling half:

    the scaling says which term dominates GIVEN the self-similar form.  Does a
    VISCOUS solution actually reach that form?

That is a dynamical question about an attractor, and §26 appeared to have answered it
NO in the worst possible way.  At a = 1/2 the linearization of the INVISCID rescaled
flow has essential spectrum filling [-2, +5]: in any truncation essentially every
direction is unstable (measured here: 142 of 144 eigenvalues with Re > 0, max Re =
+4.56).  A fixed point with a 142-dimensional unstable manifold is not an attractor
and nothing generic reaches it.

**The measurement in this module is that mu > 0 removes ALL of it.**  Every eigenvalue
of the dissipative generator lands on the negative real axis, the leading one at 0
(the exact dilation mode) and the next at approximately -1, and that gap is INSENSITIVE
to mu over four decades.  The marginal viscous profile is linearly attracting; the
inviscid one is violently unstable; and they are connected by a limit that does not
commute.

--------------------------------------------------------------------------
WHY THAT IS NOT A TRUNCATION ARTIFACT -- AND THE GUARD IT BUYS
--------------------------------------------------------------------------
Adding a large negative-definite operator to a matrix pushes its eigenvalues left, so
"mu > 0 stabilizes the truncated generator" is exactly the kind of statement that can
be an artifact.  The crossover is measurable and it has the shape that settles the
question.  Dissipation damps mode k at rate mu k^p, so it beats a growth rate g once

    mu K^p  >~  g ,   i.e.   mu*(K) ~ g / K^p     with g = max Re of the INVISCID
                                                  generator (4.55 at a = 1/2).      (C)

Measured at a = 1/2, p = 3, g = 4.55: the count collapses between mu = 1e-5 and 1e-4 at
K = 48 (C: 4.1e-5), between 1e-6 and 1e-5 at K = 96 (C: 5.1e-6) and at K = 144
(C: 1.5e-6).  **mu*(K) falls like K^-p, so at any FIXED mu > 0 a fine enough grid sees
zero unstable directions, and at any FIXED K a small enough mu sees ~K of them.**  The
two limits do not commute, and the artifact reading is the one that is excluded: an
artifact would need mu* to be independent of K or to grow with it.

(C) is also the resolution guard every trajectory in this module is run against:
`resolution_guard` REFUSES a run whose smallest mu leaves modes undamped, rather than
returning a number (banked lesson 45).

--------------------------------------------------------------------------
THE GAUGE IS AN EXACT INVARIANT, AND IT IS ENFORCED AS ONE
--------------------------------------------------------------------------
c_omega is DEFINED by freezing the origin slope, R_X(0) = 0, so the dilation gauge
sum_k k b_k = -1 is a conserved quantity of (F_mu): analytically kk . S^{-1} R == 0 for
every b.  Numerically it is zero to a relative 1e-10, which over thousands of steps
accumulates -- measured drift 4.0e-4 in a 60-time-unit run, which is 3% of the
alpha - alpha_0 signal the leg is quoting.  So the flow subtracts the dilation
component that the roundoff put there:

    db  ->  db - [ (kk . db) / (kk . d_dil) ] d_dil ,     d_dil = S^{-1}(X Omega_X) ,

which is analytically the zero vector and numerically is "re-pin L(tau) to keep the
gauge".  It is not free: `AugmentedFlow.gauge_correction` records the size of what was
subtracted at every step so the correction is auditable, and gate 5 asserts both that
it is at roundoff and that turning it OFF moves the leg's headline by less than a
percent.  A projection that had to do real work would be a bug, not a fix.

--------------------------------------------------------------------------
INTEGRATOR
--------------------------------------------------------------------------
BDF2 with a backward-Euler start, Newton with a stagnation-aware stop.  The system is
stiff by construction -- Lambda^p has eigenvalues ~ mu k^p, which is 1.2e6 at K = 96,
mu = 0.3, p = 3 -- so an explicit method would need dt ~ 1e-6 and a non-L-stable
implicit one (trapezoid) would ring on exactly those modes.  BDF2's amplification
factor tends to zero on them.

The Newton stop is worth stating because it is not a tolerance.  The step residual
cannot go below the roundoff that mu Lambda^p b generates from the 1e-16 noise in the
high coefficients -- mu K^p * 1e-16 ~ 1e-10 at K = 96 -- so a fixed 1e-13 tolerance is
BELOW the achievable floor and Newton grinds against it for 40 iterations, silently
degrading the gauge.  The stop is therefore "converged OR no longer improving by 4x",
and the achieved residual is recorded per step rather than assumed.  With it, every
step in this module converges in <= 6 iterations.

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* Plain float64; nothing interval-enclosed, nothing rigorous, no link of the L1->L4
  chain moved.  s = 3/2 is HYPERviscosity.
* "Linearly attracting in this norm at this truncation" is not "an attractor".  The
  unstable-count statement is about the SPECTRUM of a truncated generator, supported by
  the K-ladder (C) and by a nonlinear trajectory that stays put; it is not a theorem
  about the continuum operator, whose essential spectrum for mu > 0 is not computed
  here.
* NOVELTY UNCHECKED.  (M) itself is at risk through Route-F/H's inheritance (see
  LITERATURE_CHECK.md); "dissipation regularizes the linearization of a self-similar
  rescaling" is the kind of statement that is standard in the parabolic-blowup
  literature.  Presume known until a specialist says otherwise.
"""

import numpy as np

from solver.critical_dissipation import (
    CriticalDissipativeFlow, inviscid_seed, lambda_truncation, mu_branch,
)


# --------------------------------------------------------------------------
# the augmented flow y = (b, mu)
# --------------------------------------------------------------------------
class AugmentedFlow:
    """(F_mu) + (M) as one autonomous system on R^{K+1}.

    `freeze_mu` runs (F_mu) alone at a fixed mu -- used for the linear-stability
    trajectories, where the point is to watch a perturbation of Omega decay with mu
    held where it was put.
    """

    def __init__(self, a, p, K=96, gauge_project=True, freeze_mu=False):
        self.a, self.p, self.K = float(a), int(p), int(K)
        self.s = 0.5 * self.p
        self.flow = CriticalDissipativeFlow(self.a, mu=0.0, p=self.p, K=self.K)
        self.B = self.flow.B
        self.Sinv = np.linalg.inv(self.B.S)
        self.kk = self.B.k.astype(float)
        self.gauge_project = bool(gauge_project)
        self.freeze_mu = bool(freeze_mu)
        self.gauge_correction = 0.0        # worst |kk.db| removed, in absolute terms
        self.gauge_abs = 0.0               # worst |kk . db| BEFORE removal (== 0 exactly)
        self.rhs_scale = 0.0               # worst ||db||_2, the scale it is judged on

    # -- pieces ------------------------------------------------------------
    def _at(self, mu):
        self.flow.mu = float(mu)
        return self.flow

    def _db(self, b, f):
        db = self.Sinv @ f.residual(b)
        # The two maxima are tracked separately and divided at the END (see
        # `gauge_violation`).  A per-step ratio is 0/0 AT the fixed point, where db is
        # pure roundoff and therefore has an O(1) gauge component by direction alone --
        # measured 5.7 and then 0.996 in two tries, both of them the diagnostic
        # misbehaving rather than the flow leaving its invariant.
        self.gauge_abs = max(self.gauge_abs, abs(float(self.kk @ db)))
        self.rhs_scale = max(self.rhs_scale, float(np.linalg.norm(db)))
        if self.gauge_project:
            d = self.Sinv @ (self.B.XD @ b)
            g = (self.kk @ db) / (self.kk @ d)
            self.gauge_correction = max(self.gauge_correction,
                                        abs(g) * float(np.max(np.abs(d))))
            db = db - g * d
        return db

    def rhs(self, y):
        b, mu = y[:-1], y[-1]
        f = self._at(mu)
        dmu = 0.0 if self.freeze_mu else (2.0 * self.s - f.alpha(b)) * mu
        return np.concatenate([self._db(b, f), [dmu]])

    def jacobian(self, y):
        """Exact (K+1) x (K+1) Jacobian of `rhs`, including the mu column and row.

        THE GAUGE PROJECTION IS DIFFERENTIATED, AND THE VERSION THAT DID NOT WAS A BUG.
        The old note here read: "it is analytically the zero map, so its derivative is
        analytically zero too."  That is true ON the branch, where kk . db is roundoff
        and the projection is a no-op -- and false anywhere else.  Start off the branch
        and kk . db is O(1), so `_db` subtracts a genuine O(1) vector while the Newton
        matrix described a flow without it.  BDF2's Newton then solves against the wrong
        operator, stagnates, and `_implicit_step`'s stagnation stop ACCEPTS the bad step;
        the error compounds and the trajectory overflows.  Measured: every off-branch
        start NaN'd, at eps down to 1e-6 and at dt = 0.25, 0.05 AND 0.01 -- dt-independent,
        which is what says "inconsistent Newton" rather than "stiff".

        d(db - g d)/db with g = (kk.db)/(kk.d) is P J_raw - (dg/db) d, and the second
        term is dropped: it carries the b-dependence of d = S^-1 XD b, is O(kk.db), and
        therefore vanishes exactly where the flow is heading.  P J_raw is what restores
        Newton, and gate 11 measures the resulting convergence rather than assuming it.
        """
        b, mu = y[:-1], y[-1]
        f = self._at(mu)
        Om = self.B.S @ b
        omx0 = 2.0 * (self.kk @ b)
        dc_dmu = (f.lam_dx0 @ b) / omx0
        J = np.zeros((self.K + 1, self.K + 1))
        Jbb = self.Sinv @ f.jacobian(b)
        Jbmu = self.Sinv @ (dc_dmu * Om - f.Lam @ b)
        if self.gauge_project:
            d = self.Sinv @ (self.B.XD @ b)
            denom = float(self.kk @ d)
            if abs(denom) > 1e-300:
                # P = I - d kk^T / (kk.d), applied on the left of both b-blocks
                Jbb = Jbb - np.outer(d, self.kk @ Jbb) / denom
                Jbmu = Jbmu - d * (float(self.kk @ Jbmu) / denom)
        J[:self.K, :self.K] = Jbb
        J[:self.K, self.K] = Jbmu
        if not self.freeze_mu:
            J[self.K, :self.K] = mu * f._dc_omega(b)
            J[self.K, self.K] = (2.0 * self.s - f.alpha(b)) + mu * dc_dmu
        return J

    # -- diagnostics -------------------------------------------------------
    @property
    def gauge_violation(self):
        """worst |kk . db| over the run, divided by the scale it could have had.

        Analytically zero: c_omega is defined by R_X(0) = 0, which IS kk . S^{-1}R = 0.
        What is left is roundoff, and the number says how much.
        """
        return self.gauge_abs / (np.linalg.norm(self.kk) * self.rhs_scale + 1e-300)

    def gauge(self, y):
        return float(self.kk @ y[:-1] + 1.0)

    def alpha(self, y):
        return self._at(y[-1]).alpha(y[:-1])

    def generator(self, b, mu):
        """S^{-1} dR/db at (b, mu): the linearization of (F_mu) in Omega alone."""
        return self.Sinv @ self._at(mu).jacobian(b)


# --------------------------------------------------------------------------
# the stepper
# --------------------------------------------------------------------------
def _implicit_step(A, y_n, y_prev, dt, first, max_iter=25):
    """One BDF2 step (backward Euler when `first`), Newton with a stagnation stop."""
    I = np.eye(A.K + 1)
    if first:
        c0, coef, y = y_n, dt, y_n + dt * A.rhs(y_n)
    else:
        c0, coef, y = (4.0 * y_n - y_prev) / 3.0, (2.0 / 3.0) * dt, 2.0 * y_n - y_prev
    prev, nrm, floor = np.inf, np.inf, 0.0
    for it in range(1, max_iter + 1):
        g = A.rhs(y)
        F = y - c0 - coef * g
        nrm = float(np.max(np.abs(F)))
        floor = 1e-13 * max(1.0, coef * float(np.max(np.abs(g))))
        if nrm < floor or nrm > 0.25 * prev:
            return y, it, nrm, floor
        prev = nrm
        y = y + np.linalg.solve(I - coef * A.jacobian(y), -F)
    return y, max_iter, nrm, floor


def integrate(A, b0, mu0, tau_end, dt, n_sample=200, branch_every=0):
    """Integrate (F_mu)+(M) from (b0, mu0) and record the trajectory.

    `branch_every` > 0 also solves the FROZEN-mu fixed point at the sampled mu and
    records the distance to it -- the adiabaticity measurement, i.e. how far the
    driven trajectory sits from the static branch the previous leg read alpha off.
    """
    y = np.concatenate([np.asarray(b0, float), [float(mu0)]])
    y_prev = None
    n = max(1, int(round(float(tau_end) / float(dt))))
    stride = max(1, n // int(n_sample))
    tau = 0.0
    worst_it, worst_res = 0, 0.0
    rec = {"tau": [0.0], "mu": [float(mu0)], "alpha": [A.alpha(y)],
           "gauge": [A.gauge(y)], "branch_dist": [], "branch_tau": []}
    b_seed = np.asarray(b0, float)
    for i in range(n):
        y_new, it, nrm, floor = _implicit_step(A, y, y_prev, dt, first=(i == 0))
        # REFUSE rather than carry a broken state to the end.  `_implicit_step` has a
        # stagnation stop, so it RETURNS a step whose Newton never converged; without
        # this check that step compounds and the run ends as a NaN which then reaches a
        # figure legend reading "alpha_1 = nan".  It did, once (banked lesson 65).
        if not np.all(np.isfinite(y_new)):
            rec["diverged_at_tau"] = float(tau)
            rec["diverged_at_step"] = int(i)
            break
        y_prev, y = y, y_new
        tau += dt
        worst_it = max(worst_it, it)
        worst_res = max(worst_res, nrm / max(floor, 1e-300))
        if (i + 1) % stride == 0 or i == n - 1:
            rec["tau"].append(tau)
            rec["mu"].append(float(y[-1]))
            rec["alpha"].append(A.alpha(y))
            rec["gauge"].append(A.gauge(y))
            if branch_every and (len(rec["tau"]) % int(branch_every) == 0):
                row = mu_branch(A.a, A.p, [float(y[-1])], K=A.K, b0=b_seed)[0]
                b_seed = row["b"]
                rec["branch_tau"].append(tau)
                rec["branch_dist"].append(
                    float(np.max(np.abs(y[:-1] - row["b"]))) / (float(np.max(np.abs(row["b"]))) + 1e-300))
    # WHAT COUNTS AS CONVERGED, and finiteness alone is NOT it.  `_implicit_step` stops
    # on stagnation and returns the iterate anyway, so a run can stay finite and still
    # be garbage -- the off-branch trap ended at mu = -1.6e24 with every value finite.
    # The discriminator that separates them cleanly is the implicit solve's own residual
    # over its floor: ~6e2 on a healthy run, 1e13 when Newton never converged.
    NEWTON_STAGNATION = 1e8
    finite = bool(np.all(np.isfinite(y)))
    rec.update({"finite": finite,
                "newton_stagnation_threshold": float(NEWTON_STAGNATION),
                "converged": bool(finite and "diverged_at_tau" not in rec
                                  and worst_res < NEWTON_STAGNATION),
                "dt": float(dt), "tau_end": float(tau), "steps": n,
                "worst_newton_iters": int(worst_it),
                "worst_newton_residual_over_floor": float(worst_res),
                "gauge_drift": float(A.gauge(y)),
                "gauge_violation": float(A.gauge_violation),
                "gauge_correction": float(A.gauge_correction),
                "rhs_scale": float(A.rhs_scale),
                "b_end": y[:-1].copy(), "mu_end": float(y[-1]),
                "a": A.a, "p": A.p, "K": A.K, "s": A.s})
    return rec


# --------------------------------------------------------------------------
# what the trajectories are read for
# --------------------------------------------------------------------------
def rung_gate(seed_row, res_max=1e-5, trunc_max=1.0):
    """Is this (a, p, K) rung worth measuring on?  TWO conditions, and both are needed.

    (i) THE PROFILE IS RESOLVED -- the seed's Newton residual.  At the resonances
        (alpha an odd integer) the profile is analytic and the residual is 1e-8 or
        better; off them the basis converges only algebraically and it is 3e-3, five
        orders worse, at the same K.
    (ii) THE OPERATOR IS ACCURATE -- `lambda_truncation`, the size of the coefficients
        Lambda^p pushes past the truncation relative to the ones it keeps.  This is
        §29's lesson 59: a structural coincidence that makes Lambda^p a FINITE matrix
        does not make the composite accurate.

    Measured at K = 96, mu = 2e-3:  a = 1/2 gives residual <= 1e-6 with truncation
    2.8e-7/3.4e-3/1.1e-2/0.13/1.77 for p = 1..5;  a = 0.3 gives residual 6e-4..4e-3 with
    truncation 3.9e-2..161, and at p = 3 Newton lands on a state whose alpha has the
    WRONG SIGN (-1.618 where the inviscid profile has +1.617).  Condition (i) alone
    catches that one; neither condition alone catches everything.
    """
    res = float(seed_row["residual"])
    tr = float(seed_row["lambda_truncation"])
    reasons = []
    if not (res < float(res_max)):
        reasons.append("seed residual %.1e >= %.0e (profile not resolved)"
                       % (res, res_max))
    if not (tr < float(trunc_max)):
        reasons.append("Lambda^p truncation %.2f >= %.1f (operator not accurate)"
                       % (tr, trunc_max))
    return {"passed": not reasons, "residual": res, "lambda_truncation": tr,
            "reason": "; ".join(reasons) or None}


def dynamic_lambda_mu(rec, frac=0.4, linear_factor=3.0):
    """d(log mu)/d tau in the LINEAR REGIME: the off-critical rate.

    (M) is mu_tau = (2s - alpha[Omega, mu]) mu, and only the mu -> 0 limit of the
    bracket is 2s - alpha_0.  So the fit window is bounded twice: by the first `frac`
    of the run, AND by mu <= linear_factor * mu(0).  The second bound is not
    housekeeping -- at a = 0.3, p = 3 the rate is +4.6, mu crosses 1 before tau = 1.2,
    and a fit over "the first 40% of the run" returned +11.8 against a prediction of
    +4.6 while the integrator overflowed underneath it.  With the bound the same run
    either measures the rate or REFUSES, and refusing is the correct answer for a
    trajectory that left the regime the number is defined in.
    """
    tau = np.asarray(rec["tau"], float)
    mu = np.asarray(rec["mu"], float)
    ok = (mu > 0) & np.isfinite(mu)
    if not ok.any():
        return {"lambda_mu": float("nan"), "refused": True,
                "reason": "no finite positive mu on the trajectory", "n_points": 0}
    mu0 = float(mu[ok][0])
    lin = ok & (mu <= float(linear_factor) * mu0)
    n = max(3, int(frac * lin.sum()))
    t, u = tau[lin][:n], np.log(mu[lin][:n])
    if t.size < 3:
        return {"lambda_mu": float("nan"), "refused": True,
                "reason": "fewer than 3 samples inside mu <= %g mu0" % linear_factor,
                "n_points": int(t.size)}
    c = np.polyfit(t, u, 1)
    resid = float(np.max(np.abs(np.polyval(c, t) - u)))
    return {"lambda_mu": float(c[0]), "fit_residual": resid, "refused": False,
            "n_points": int(t.size), "tau_window": [float(t[0]), float(t[-1])],
            "mu_window": [float(mu[lin][:n].min()), float(mu[lin][:n].max())]}


def dynamic_alpha_1(rec, mu_max=None):
    """alpha_1 from the trajectory: mu_tau = -alpha_1 mu^2 at criticality.

    1/mu is LINEAR in tau under the quadratic law, so alpha_1 is the slope of 1/mu --
    which is why the fit is done there and not on mu.  The higher-order term shows up
    as curvature, so the fit is restricted to the small-mu tail and the window is swept
    by the caller rather than chosen here.
    """
    tau = np.asarray(rec["tau"], float)
    mu = np.asarray(rec["mu"], float)
    m = (mu > 0) & np.isfinite(mu)
    if mu_max is not None:
        m &= mu <= float(mu_max)
    if m.sum() < 3:
        return {"alpha_1": float("nan"), "n_points": int(m.sum()),
                "refused": True, "reason": "fewer than 3 samples in the mu-window"}
    t, inv = tau[m], 1.0 / mu[m]
    c = np.polyfit(t, inv, 1)
    resid = float(np.max(np.abs(np.polyval(c, t) - inv))) / (float(np.max(inv)) + 1e-300)
    return {"alpha_1": float(c[0]), "fit_residual_rel": resid, "n_points": int(m.sum()),
            "mu_window": [float(mu[m].min()), float(mu[m].max())], "refused": False}


def dt_ladder(a, p, K, mu0, tau_end, dts, b0=None, quantity="alpha_1", mu_max=None,
              **kw):
    """The same trajectory at several dt, and the SPREAD in the number extracted from it.

    This is banked lesson 57 ported from a Newton residual to a time step.  "Did the
    integrator run?" is not the refusal predicate for a derivative read off a
    trajectory; "is the number bigger than the spread the discretization puts on it?"
    is.  `signal_over_discretization` is that ratio, and a caller is expected to refuse
    below 10 rather than to quote a number with a caveat attached.
    """
    if b0 is None:
        b0 = mu_branch(a, p, [float(mu0)], K=K)[0]["b"]
    vals, recs = [], []
    for dt in np.asarray(dts, float):
        A = AugmentedFlow(a, p, K=K)
        rec = integrate(A, b0, mu0, tau_end, float(dt), **kw)
        v = (dynamic_alpha_1(rec, mu_max=mu_max)["alpha_1"] if quantity == "alpha_1"
             else dynamic_lambda_mu(rec)["lambda_mu"])
        vals.append(float(v))
        recs.append({"dt": float(dt), "value": float(v), "mu_end": rec["mu_end"],
                     "gauge_drift": rec["gauge_drift"],
                     "worst_newton_iters": rec["worst_newton_iters"]})
    vals = np.array(vals)
    spread = float(vals.max() - vals.min())
    # BDF2 order, from the finest three rungs when the ladder is a halving sequence
    order = float("nan")
    if len(vals) >= 3:
        d1, d2 = abs(vals[-3] - vals[-2]), abs(vals[-2] - vals[-1])
        if d2 > 0:
            order = float(np.log2(d1 / d2))
    return {"quantity": quantity, "dts": [float(d) for d in dts],
            "values": vals.tolist(), "value": float(vals[-1]), "spread": spread,
            "observed_order": order,
            "signal_over_discretization": float(abs(vals[-1]) / (spread + 1e-300)),
            "rows": recs}


def tar_pit_law(alpha_1, mu0, tau):
    """The closed solution of mu_tau = -alpha_1 mu^2: 1/mu = 1/mu0 + alpha_1 tau."""
    tau = np.asarray(tau, float)
    return 1.0 / (1.0 / float(mu0) + float(alpha_1) * tau)


# --------------------------------------------------------------------------
# the stability side
# --------------------------------------------------------------------------
def unstable_count(a, p, K, mu, b0=None, tol=1e-6):
    """Eigenvalues of S^{-1} dR/db at the frozen-mu fixed point, and how many grow.

    THE DILATION MODE IS REMOVED BY IDENTITY, NOT BY THRESHOLD.  L(X Omega_X) = 0 is
    exact, so one eigenvalue is analytically zero; numerically it lands anywhere from
    1e-13 to 2.6e-6 depending on mu and K.  A threshold tuned to swallow it either
    misses it (the count then reads "one unstable direction" at every mu) or swallows a
    real small eigenvalue with it.  So the eigenvalue NEAREST zero is excised as the
    dilation mode and REPORTED (`dilation_eigenvalue`), and everything else is judged
    on its own -- banked lesson 58 applied to a mode rather than to an absence.
    """
    a, p, K, mu = float(a), int(p), int(K), float(mu)
    if b0 is None:
        b0 = inviscid_seed(a, K=K)[0]
    flow = CriticalDissipativeFlow(a, mu=mu, p=p, K=K)
    if mu > 0.0:
        out = flow.newton(b0=np.asarray(b0, float))
        b, res = out["b"], out["residual"]
    else:
        b = np.asarray(b0, float)
        res = float(np.max(np.abs(flow.residual(b))))
    ev = np.linalg.eigvals(np.linalg.solve(flow.B.S, flow.jacobian(b)))
    i_dil = int(np.argmin(np.abs(ev)))
    dil = ev[i_dil]
    rest = np.delete(ev, i_dil)
    re = np.sort(rest.real)[::-1]
    return {"a": a, "p": p, "K": K, "mu": mu, "residual": float(res),
            "n_unstable": int(np.sum(re > tol)), "max_re": float(re[0]),
            "gap": float(re[0]),
            "dilation_eigenvalue": [float(dil.real), float(dil.imag)],
            "min_re": float(re[-1]), "max_abs_im": float(np.max(np.abs(ev.imag))),
            "lambda_truncation": lambda_truncation(b, K, p), "b": b}


def stability_ladder(a, p, K, mus, tol=1e-6):
    """`unstable_count` along a mu-ladder, CONTINUED (each mu seeded by the last)."""
    rows, b = [], None
    for mu in np.asarray(mus, float):
        r = unstable_count(a, p, K, float(mu), b0=b, tol=tol)
        b = r["b"]
        rows.append(r)
    return rows


def crossover_mu(rows):
    """The mu at which the unstable count collapses, bracketed by the ladder."""
    rows = sorted(rows, key=lambda r: r["mu"])
    lo = hi = float("nan")
    for r0, r1 in zip(rows, rows[1:]):
        if r0["n_unstable"] > 1 and r1["n_unstable"] <= 1:
            lo, hi = r0["mu"], r1["mu"]
    return {"bracket": [lo, hi], "geometric_mid": float(np.sqrt(lo * hi))}


def frequency_profile(a, p, K, mu, caps=(2.0, 5.0, 10.0, 30.0, 100.0), b0=None):
    """max Re of the generator RESTRICTED to |Im| <= cap, plus the largest |Im| present.

    This exists because the leading eigenvalue of the INVISCID flow at a = 1/2 is
    4.5455 + 430.35i.  The unstable spectrum is not a set of slow growing modes -- it is
    a curve on which Re INCREASES with |Im|, and max|Im| grows with K (430 at K = 96,
    661 at K = 144).  Two consequences the leg has to state rather than discover twice:

      * these are Route-E's log-periodic continuum modes exp(i y (tau - log X)), so the
        directions that grow FASTEST in the inviscid rescaled flow are exactly the ones
        a DISCRETELY SELF-SIMILAR solution is built out of;
      * any time integrator caps the |Im| it can resolve at ~1/dt, so a nonlinear
        growth rate measured from a generic kick is a LOWER BOUND on max Re, not a
        measurement of it.  `perturbation_decay` inherits that caveat and says so.
    """
    r = unstable_count(a, p, K, mu, b0=b0)
    flow = CriticalDissipativeFlow(float(a), mu=float(mu), p=int(p), K=int(K))
    ev = np.linalg.eigvals(np.linalg.solve(flow.B.S, flow.jacobian(r["b"])))
    out = {"a": float(a), "p": int(p), "K": int(K), "mu": float(mu),
           "max_re": float(ev.real.max()), "max_abs_im": float(np.abs(ev.imag).max()),
           "im_of_max_re": float(ev[int(np.argmax(ev.real))].imag), "caps": {}}
    for cap in caps:
        sel = ev[np.abs(ev.imag) <= float(cap)]
        out["caps"][str(cap)] = {
            "n": int(sel.size),
            "max_re": float(sel.real.max()) if sel.size else float("nan")}
    return out


def resolution_guard(a, p, K, mu_min, g=None):
    """(C): REFUSE a run whose smallest mu leaves the top mode undamped.

    Returns the required K rather than a boolean, so a caller that fails it knows what
    to do about it.  `g` defaults to the measured max Re of the INVISCID generator,
    which is the growth rate the dissipation has to beat.
    """
    if g is None:
        g = unstable_count(a, p, K, 0.0)["max_re"]
    K_req = (float(g) / float(mu_min)) ** (1.0 / int(p))
    return {"g": float(g), "K_required": float(K_req), "K": int(K),
            "mu_min": float(mu_min), "margin": float(K) / K_req,
            "resolved": bool(K > K_req)}


def admissible_direction(A, b, seed=0, decay=0.25):
    """A perturbation direction that is small in THE NORM THAT ACTUALLY BINDS.

    "eps = 1e-3" means nothing until you say in which norm, and the first version of
    the off-branch measurement got this wrong in a way worth keeping (banked lesson 66).
    It drew v with a decaying spectrum, projected off the gauge direction, and scaled it
    to `max|v_k| = 1` -- small in the COEFFICIENT sup-norm.  But the gauge (N') carries
    the functional b -> (Lambda^p Omega)_X(0) = lam_dx0 . b, and Lambda^p weights mode k
    by ~k^p while the derivative at the origin adds one more power.  Measured at
    a = 1/2, p = 3, K = 96:

        |lam_dx0 . v| / |lam_dx0 . b|  =  3.6e8 ,

    so eps = 1e-3 in coefficients was a 3.6e5 RELATIVE perturbation of the quantity the
    flow divides by.  alpha came back as 11713 instead of 3.04 AT tau = 0, before a
    single step, and every off-branch trajectory overflowed -- at eps down to 1e-6 and
    at dt = 0.25, 0.05 and 0.01 alike.  dt-independence is what says the integrator was
    innocent.

    So normalize in that functional instead: `eps` is then a genuine relative
    perturbation of the thing the gauge reads, and the gauge component is still
    projected out so Omega_X(0) = -2 survives exactly.
    """
    rng = np.random.default_rng(int(seed))
    v = rng.standard_normal(A.K) * np.exp(-float(decay) * np.arange(A.K))
    v = v - (A.kk @ v) / (A.kk @ A.kk) * A.kk
    lam = A.flow.lam_dx0
    scale = abs(float(lam @ v))
    base = abs(float(lam @ np.asarray(b, float)))
    if scale > 0:
        v = v * (base / scale)              # |lam . v| == |lam . b|: eps is RELATIVE
    return v


def perturbation_decay(a, p, K, mu, eps=1e-6, tau_end=4.0, dt=0.02, seed=0, b0=None,
                       fit_window=(0.3, 0.6)):
    """Kick Omega off the frozen-mu fixed point and fit the growth rate of the kick.

    TWIN TRAJECTORIES, and the reason is a measurement that went wrong without them.
    The obvious version -- integrate the kicked state and watch |b(tau) - b0| -- reads
    the base state's OWN motion, because b0 is a Newton fixed point with residual
    ~1e-8 and not an exact one, so it drifts at a rate comparable to a small kick.  Run
    that way, mu = 0.05 and mu = 0.2 both returned a GROWTH rate of +1.5, the opposite
    of what every eigenvalue says.  Integrating the unkicked state alongside and
    differencing removes the base motion exactly, at the cost of one more trajectory.

    The kick is drawn in coefficient space and PROJECTED off the gauge direction
    (kk . v = 0), so the perturbed state still satisfies Omega_X(0) = -2 exactly and
    the measurement is not the gauge relaxing.  mu is frozen: this is the linear
    stability of (F_mu) at fixed mu, which is what the eigenvalues claim to describe,
    measured through the nonlinear flow as a control on them.
    """
    A = AugmentedFlow(a, p, K=K, freeze_mu=True)
    if b0 is None:
        b0 = (mu_branch(a, p, [mu], K=K)[0]["b"] if mu > 0
              else inviscid_seed(a, K=K)[0])
    b0 = np.asarray(b0, float)
    rng = np.random.default_rng(int(seed))
    v = rng.standard_normal(K)
    v = v - (A.kk @ v) / (A.kk @ A.kk) * A.kk
    v /= np.max(np.abs(v))
    yk = np.concatenate([b0 + float(eps) * v, [float(mu)]])
    yb = np.concatenate([b0, [float(mu)]])
    yk_p = yb_p = None
    n = max(2, int(round(tau_end / dt)))
    tau, taus, amp = 0.0, [0.0], [float(np.max(np.abs(yk[:-1] - yb[:-1])))]
    for i in range(n):
        yk_n, _a, _b, _c = _implicit_step(A, yk, yk_p, dt, first=(i == 0))
        yb_n, _d, _e, _f = _implicit_step(A, yb, yb_p, dt, first=(i == 0))
        yk_p, yk = yk, yk_n
        yb_p, yb = yb, yb_n
        tau += dt
        taus.append(tau)
        amp.append(float(np.max(np.abs(yk[:-1] - yb[:-1]))))
    taus, amp = np.array(taus), np.array(amp)
    lo, hi = float(fit_window[0]) * tau_end, float(fit_window[1]) * tau_end
    m = (amp > 0) & np.isfinite(amp) & (taus >= lo) & (taus <= hi)
    if m.sum() < 3:
        m = (amp > 0) & np.isfinite(amp)
    c = np.polyfit(taus[m], np.log(amp[m]), 1)
    pred = np.polyval(c, taus[m])
    return {"a": a, "p": p, "K": K, "mu": float(mu), "eps": float(eps),
            "rate": float(c[0]), "amp0": float(amp[0]), "amp_end": float(amp[-1]),
            "growth_factor": float(amp[-1] / (amp[0] + 1e-300)),
            "fit_residual": float(np.max(np.abs(pred - np.log(amp[m])))),
            "fit_window": [lo, hi], "n_fit": int(m.sum()),
            "im_resolved": float(np.pi / float(dt)),
            "base_drift": float(np.max(np.abs(yb[:-1] - b0))),
            "tau": taus.tolist(), "amp": amp.tolist()}


def stability_verdict(rows, tol=1e-6):
    """A SENTENCE, so a dropped sign fails a test (banked lesson 60).

    The reflex reading of "dissipation stabilizes" is that it damps the small scales;
    what the ladder actually says is that it converts a CONTINUUM reaching Re = +4.5
    into a discrete negative ladder, which is a statement about the far field, not the
    small scales.  The two are easy to conflate in prose, so the verdict is a value.
    """
    inv = [r for r in rows if r["mu"] == 0.0]
    vis = [r for r in rows if r["mu"] > 0.0]
    if not inv or not vis:
        return "incomplete_ladder"
    if inv[0]["n_unstable"] <= 1:
        return "inviscid_already_stable"
    if all(r["n_unstable"] <= 1 for r in vis):
        return "dissipation_removes_all_unstable_directions"
    if all(r["n_unstable"] >= inv[0]["n_unstable"] for r in vis):
        return "dissipation_does_not_help"
    return "partial"
