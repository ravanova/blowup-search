"""The dynamically-rescaled gCLM flow, its self-similar fixed point, and its spectrum.

ROUTE E v1 -- the first leg of the DSS lane that v15/v16 named as the swing.

--------------------------------------------------------------------------
WHY THIS OBJECT, AND WHY NOW
--------------------------------------------------------------------------
Necas-Ruzicka-Sverak (extended by Tsai) rules out EXACTLY self-similar blow-up for
3D Navier-Stokes in the natural scaling class, so the "find a self-similar profile
and certify it" template that Route D spent sixteen legs on cannot be pointed at NS
as posed.  The candidate class that survives is DISCRETELY self-similar (DSS): the
solution repeats itself under a fixed dilation at a discrete sequence of times
instead of at every time.  In dynamic-rescaling variables that is exactly the
statement

    a self-similar blow-up  =  a FIXED POINT of the rescaled flow,
    a DSS blow-up           =  a PERIODIC ORBIT of the rescaled flow.

The cheapest question that can kill or open that lane is therefore not "search for a
periodic orbit" (expensive, and a global search needs somewhere to start).  It is:

    does the self-similar fixed point have a complex-conjugate pair of eigenvalues
    that crosses the imaginary axis as the model parameter `a` moves?

A Hopf bifurcation off the self-similar branch would BIRTH a periodic orbit -- a DSS
blow-up -- with the crossing point telling you where to look.  No eigenvalue
available to cross means no Hopf, and that particular route into the DSS lane is
closed for this family.  This module answers that question for gCLM.

--------------------------------------------------------------------------
THE FLOW
--------------------------------------------------------------------------
gCLM on the line:  omega_t + a u omega_x = omega u_x,  u_x = H(omega).  Dynamic
rescaling omega(x,t) = A(t) Omega(X, tau), X = x/L(t), dtau/dt = A gives

    Omega_tau = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X ,        (F)
    U(X) = int_0^X H(Omega) dX' ,   U(0) = 0 .

Two gauge functions (c_omega, c_l) carry the two scaling freedoms.  This module fixes
c_l = 1 (a choice, not a result) and determines c_omega by the NORMALIZATION that
freezes the origin slope:  requiring (Omega_tau)_X(0) = 0 for odd Omega gives

    c_omega[Omega] = 1 + (a - 1) H(Omega)(0) ,                                   (N)

which at a = 0 is exactly the value-based normalization the project has used since
Spike 0 (solver/gclm_rescaled.py), so this is the same flow continued in `a` rather
than a new convention.  With c_l fixed, DILATION survives as a symmetry of (F) --
Omega(X) -> Omega(X/mu) is again a fixed point, and H(Omega)(0) is dilation-invariant
so (N) is untouched -- which is where the exact zero eigenvalue below comes from.

--------------------------------------------------------------------------
THE DISCRETIZATION (why the far field costs nothing here)
--------------------------------------------------------------------------
Compactify with X = tan(theta/2), theta in (-pi, pi), and expand the ODD profile in
SINES.  Three operators are then exact on the whole line with no truncation and no
quadrature:

    H(sin k theta) = -cos k theta + (-1)^k        (H(cos k theta) = sin k theta, and
                                                   H^2 = -1 modulo constants: the
                                                   (-1)^k is what makes H(Omega)
                                                   vanish at X = infinity)
    X d/dX          = sin(theta) d/d theta       (the DILATION term is a bounded,
                                                   exact operator on the circle)
    d/dX            = (1 + cos theta) d/d theta

and the velocity is exact too.  Writing N_k(t) := ((-1)^k - cos k t)/(1 + cos t),
the three-term identity 2 cos t cos kt = cos(k+1)t + cos(k-1)t gives

    N_{k+1} = -2 N_k - N_{k-1} - 2 cos k t ,      N_0 = 0, N_1 = -1,

so every N_k is a TRIG POLYNOMIAL (the 1 + cos t in the denominator always cancels)
and U = int_0^X H(Omega) dX' = sum_k b_k int_0^theta N_k is elementary.  There is no
quadrature anywhere in the build.

The a = 0 fixed point is a single mode:  Omega_0 = -sin theta = -2X/(1 + X^2), with
H(Omega_0) = 1 + cos theta = 2/(1 + X^2) and c_omega = -1.  It nulls the residual to
1.1e-16 on the grid, which is the module's first gate.

--------------------------------------------------------------------------
WHAT THE SPECTRUM CONTAINS BEFORE YOU COMPUTE IT (state it first)
--------------------------------------------------------------------------
TWO EIGENVALUES ARE EXACT AND STRUCTURAL, at EVERY a.  Let L be the linearization of
(F) at a fixed point.  Then

    L (X Omega_X) = 0            (dilation is a symmetry: the orbit is a curve of
                                  fixed points, so its generator is in the kernel)
    L (Omega)     = -Omega + X Omega_X

-- the second by substituting the profile equation into L(Omega) and using (N).  So
span{Omega, X Omega_X} is invariant with matrix [[-1, 0], [1, 0]]:

    lambda = 0   (dilation)      and      lambda = -1  (amplitude),

a Jordan-like pair present for every a and carrying no dynamical information.  Any
DSS-relevant eigenvalue has to be something ELSE, and `structural_pair_defect`
gates the identities rather than trusting the derivation.

THE REST OF THE SPECTRUM IS ESSENTIAL, AND AT a = 0 IT IS KNOWN IN CLOSED FORM.
With w = e^{-i theta} and Z = H Omega + i Omega (so Z_0 = 1 + w), the a = 0
linearization in the variable s = delta Z is

    L s = w s - ((w^2 - 1)/2) s_w - s(w=1) (1 + w) ,

whose homogeneous eigenfunctions are  s = (w-1)^{1-lambda} (w+1)^{1+lambda}.
Admissibility (vanishing at w = -1, i.e. decay at X = infinity; bounded at w = 1,
i.e. at X = 0) gives a CONTINUUM filling the strip -1 < Re lambda < 1, whose
eigenfunctions carry a FRACTIONAL power at X = 0 and are therefore not in the
analytic class the discretization uses.  Requiring analyticity at X = 0 forces
1 - lambda to be a non-negative integer, leaving exactly lambda = 0 and lambda = -1
-- the two structural modes and nothing else.  The numerical spectrum reproduces
this: one eigenvalue at -1 isolated to 1e-14, everything else pinned to the
imaginary axis (the discretized continuum) and moving with K.

THAT IS WHY A CONVERGENCE FILTER IS MANDATORY, not decoration: the discrete
eigenvalues are the ones that stop moving under refinement, and the continuum is the
part that never does.  `converged_spectrum` implements it and
`planted_eigenvalue_control` is the POSITIVE control -- add a localized potential to
the same operator and check the filter finds the bound state it creates, so that
"nothing converged" is a measurement and not a broken instrument.

--------------------------------------------------------------------------
LIMITS OF THIS BUILD (say them out loud)
--------------------------------------------------------------------------
* Plain float64.  Nothing is interval-enclosed and nothing here is rigorous.
* The essential spectrum's LOCATION is norm-dependent; what this module measures is
  the spectrum of the DISCRETIZATION, filtered for grid-independence.  A discrete
  eigenvalue embedded in the continuum can be missed by any such method, and the
  a = 0 closed form is the only place where the answer is known independently.
* For generic a the profile has a branch point at X = infinity of order
  alpha(a) = -c_omega(a) (the far-field decay rate), so the sine coefficients decay
  ALGEBRAICALLY and everything converges algebraically with it.  The exceptions are
  the values of a at which alpha is an odd integer -- a = 0 (alpha = 1) and
  a = 1/2 (alpha = 3) -- where the profile is analytic and the method is spectral.
  Quantitative statements are quoted at those two points for that reason.

--------------------------------------------------------------------------
THE REFINEMENT GUARD (leg 225, repairing leg 203's finding R1)
--------------------------------------------------------------------------
Line 114 above states the specification: "the discrete eigenvalues are the ones
that stop moving under refinement".  `converged_spectrum` used to accept any
(K_coarse, K_fine) pair without ever checking that refinement HAPPENED.  Leg 203
(Route-RSA, `experiments/journal/leg_203.md`, finding R1) measured what that
costs at K_fine == K_coarse: the filter compares a spectrum with ITSELF, every
match distance is identically 0.0, and the entire discretized continuum is
returned as "the grid-independent part of the spectrum" -- n_kept goes 2 -> K
(24/24, 32/32, 48/48, a 24x inflation at K = 48), including a purely imaginary
conjugate pair at +-40.4623i, which is exactly the Hopf-crossing signature this
module exists to RULE OUT.

`converged_spectrum` now requires K_fine > K_coarse and raises ValueError
otherwise.  Equality is called out by name in the message because it is the
degenerate case that certifies everything; K_fine < K_coarse is rejected under
the same guard because a COARSER second grid is not a refinement either, even
though leg 203 measured that it happens to return the right answer (2) at a = 0.
The guard rejects on the specification, not on the outcome.

  * `on_no_refinement="raise"` (default) -- ValueError, as above.
  * `on_no_refinement="allow"` -- the pre-repair behaviour verbatim, with a
    warning, so leg 203's R1 measurement stays EXECUTABLE rather than becoming
    a story about a number nobody can reproduce (lesson 68).

WHAT THIS GUARD DOES NOT COVER, said out loud so nobody reads it as wider than
it is.  Leg 225 measured both and repaired neither, because both sit outside the
mechanism leg 203 named and (for the second) outside leg 225's declared file
territory:
  * `planted_eigenvalue_control` in this file takes the same (K_coarse, K_fine)
    pair through the same `match_filter` and is UNGUARDED.
  * `converged_dissipative_spectrum` in `solver/critical_dissipation.py` is a
    re-implementation of this filter and is UNGUARDED.
Leg 203's other seven mechanisms (R2-R8) are also untouched here; in particular
R2 -- that `spectrum` and `converged_spectrum` discard `newton`'s `converged`
flag -- is a separate design decision and is NOT what this repair addresses.
"""

import warnings

import numpy as np


# --------------------------------------------------------------------------
# the basis
# --------------------------------------------------------------------------
class OddCompactBasis:
    """Sine collocation for odd functions of X = tan(theta/2) on the whole line.

    theta_j = (j + 1/2) pi / K, j = 0..K-1 -- the MIDPOINT grid, which avoids
    theta = 0 and theta = pi where every sin k theta (and hence every residual row)
    vanishes identically.  Coefficients b_k multiply sin(k theta), k = 1..K.
    """

    def __init__(self, K):
        K = int(K)
        self.K = K
        self.theta = (np.arange(K) + 0.5) * np.pi / K
        self.k = np.arange(1, K + 1)
        th, k = self.theta, self.k
        self.S = np.sin(np.outer(th, k))                      # b -> Omega
        self.H = -np.cos(np.outer(th, k)) + (-1.0) ** k       # b -> H(Omega)
        self.Dt = k * np.cos(np.outer(th, k))                 # b -> Omega_theta
        self.XD = np.sin(th)[:, None] * self.Dt               # b -> X Omega_X
        self.DX = (1.0 + np.cos(th))[:, None] * self.Dt       # b -> Omega_X
        self.U = self._velocity_matrix()                      # b -> U
        self.h0 = (-1.0) ** k - 1.0                           # b -> H(Omega)(0)
        self.X = np.tan(th / 2.0)

    def _velocity_matrix(self):
        """U(theta) = sum_k b_k P_k(theta), P_k = int_0^theta N_k, N_k a polynomial.

        N_{k+1} = -2 N_k - N_{k-1} - 2 cos k t with N_0 = 0, N_1 = -1.  Exact: no
        quadrature, and the 1 + cos t singularity at theta = pi cancels identically.
        """
        K, th = self.K, self.theta
        n = np.zeros((K + 2, K + 2))
        n[1, 0] = -1.0
        for kk in range(1, K + 1):
            n[kk + 1, :] = -2.0 * n[kk, :] - n[kk - 1, :]
            n[kk + 1, kk] -= 2.0
        m = np.arange(1, K + 2)
        sin_m = np.sin(np.outer(th, m))
        U = np.empty((K, K))
        for kk in range(1, K + 1):
            U[:, kk - 1] = n[kk, 0] * th + sin_m @ (n[kk, 1:K + 2] / m)
        return U

    # -- the exact a = 0 fixed point ---------------------------------------
    def anchor(self):
        """Omega_0 = -sin theta = -2X/(1 + X^2): the CLM self-similar profile."""
        b = np.zeros(self.K)
        b[0] = -1.0
        return b

    def eval_on(self, b, theta):
        """Evaluate the interpolant off the collocation grid."""
        return np.sin(np.outer(np.asarray(theta, float), self.k)) @ b


# --------------------------------------------------------------------------
# the flow, its fixed point and its linearization
# --------------------------------------------------------------------------
class RescaledFlow:
    """Right-hand side of (F) in the compactified odd sine basis."""

    def __init__(self, a, K=96):
        self.a = float(a)
        self.B = OddCompactBasis(K)
        self.K = self.B.K

    # -- pieces ------------------------------------------------------------
    def parts(self, b):
        B = self.B
        Om = B.S @ b
        HOm = B.H @ b
        OmX = B.DX @ b
        Uv = B.U @ b
        c_omega = 1.0 + (self.a - 1.0) * (B.h0 @ b)
        return Om, HOm, OmX, Uv, c_omega

    def c_omega(self, b):
        return 1.0 + (self.a - 1.0) * (self.B.h0 @ b)

    def residual(self, b):
        """R = (c_omega + H Omega) Omega - X Omega_X - a U Omega_X, on the grid."""
        B = self.B
        Om, HOm, OmX, Uv, cw = self.parts(b)
        R = (cw + HOm) * Om - B.XD @ b
        if self.a != 0.0:
            R = R - self.a * Uv * OmX
        return R

    def jacobian(self, b):
        """dR/db (K x K), exact -- including the variation of the gauge (N)."""
        B = self.B
        Om, HOm, OmX, Uv, cw = self.parts(b)
        J = ((cw + HOm)[:, None] * B.S + Om[:, None] * B.H
             + (self.a - 1.0) * np.outer(Om, B.h0) - B.XD)
        if self.a != 0.0:
            J = J - self.a * (OmX[:, None] * B.U + Uv[:, None] * B.DX)
        return J

    def generator(self, b):
        """The linearized FLOW generator in coefficient space.

        The flow is Omega_tau = R, i.e. S b_tau = R(b), so the generator whose
        eigenvalues are the growth rates is S^{-1} dR/db -- NOT dR/db itself.
        """
        return np.linalg.solve(self.B.S, self.jacobian(b))

    # -- the fixed point ---------------------------------------------------
    def newton(self, b0=None, tol=1e-14, max_iter=120, damping=True):
        """Newton on R = 0 with the DILATION gauge Omega_X(0) = -2.

        Omega_X(0) = 2 sum_k k b_k, so the gauge row is sum_k k b_k = -1.  It is
        APPENDED (K + 1 rows, K unknowns) and the step is taken in least squares:
        the dilation symmetry makes dR/db exactly singular, and appending rather
        than replacing keeps every collocation condition in play.
        """
        B = self.B
        b = B.anchor() if b0 is None else np.asarray(b0, float).copy()
        kk = B.k.astype(float)
        hist = []
        for _ in range(int(max_iter)):
            R = self.residual(b)
            g = kk @ b + 1.0
            F = np.concatenate([R, [g]])
            hist.append(float(np.max(np.abs(F))))
            if hist[-1] < tol:
                break
            J = np.vstack([self.jacobian(b), kk])
            try:
                step = np.linalg.lstsq(J, -F, rcond=None)[0]
            except np.linalg.LinAlgError:
                return {"converged": False, "reason": "singular Jacobian",
                        "b": b, "history": hist}
            t = 1.0
            while damping and t > 1e-6:
                bt = b + t * step
                Ft = max(float(np.max(np.abs(self.residual(bt)))), abs(kk @ bt + 1.0))
                if Ft < hist[-1]:
                    break
                t *= 0.5
            b = b + t * step
        R = self.residual(b)
        res = float(np.max(np.abs(R)))
        return {"converged": bool(res < 1e-8), "b": b, "residual": res,
                "c_omega": float(self.c_omega(b)), "history": hist,
                "iterations": len(hist), "gauge": float(kk @ b + 1.0),
                "tail": float(np.max(np.abs(b[-max(4, self.K // 16):])))}

    # -- the two structural modes -----------------------------------------
    def structural_pair_defect(self, b):
        """|L(X Omega_X)| and |L(Omega) + Omega - X Omega_X|, both relative.

        These are the two identities the module CLAIMS hold at every a.  Measuring
        them is cheaper than trusting the derivation, and a nonzero answer would
        mean the gauge (N) is not the one the algebra assumed.
        """
        B = self.B
        A = self.generator(b)
        scale = float(np.max(np.abs(b))) + 1e-300
        # dilation generator, in coefficients: X Omega_X = sin th Omega_th
        d_dil = np.linalg.solve(B.S, B.XD @ b)
        r_dil = A @ d_dil
        # amplitude: L(Omega) should equal -Omega + X Omega_X
        r_amp = A @ b + b - d_dil
        return (float(np.max(np.abs(r_dil))) / (np.max(np.abs(d_dil)) + 1e-300),
                float(np.max(np.abs(r_amp))) / scale)


# --------------------------------------------------------------------------
# spectrum, with the convergence filter and its control
# --------------------------------------------------------------------------
def continuation(a_target, K=96, da=0.02, b0=None, **kw):
    """Follow the fixed point from the exact a = 0 anchor up to a_target.

    Returns the final RescaledFlow and its Newton result.  Continuation is the
    honest test for a branch: it FOLLOWS the object rather than searching for it.
    """
    a_grid = np.arange(0.0, float(a_target) + 1e-12, float(da))
    if a_grid.size == 0 or abs(a_grid[-1] - a_target) > 1e-12:
        a_grid = np.append(a_grid, float(a_target))
    b = b0
    flow = out = None
    for a in a_grid:
        flow = RescaledFlow(a, K=K)
        out = flow.newton(b0=b, **kw)
        b = out["b"]
    return flow, out


def spectrum(a, K, da=0.02, **kw):
    """Eigenvalues of the linearized rescaled flow at the fixed point reached at `a`."""
    flow, out = continuation(a, K=K, da=da, **kw)
    ev = np.linalg.eigvals(flow.generator(out["b"]))
    return ev, flow, out


def match_filter(ev_coarse, ev_fine, tol):
    """Keep the coarse eigenvalues that a finer grid reproduces to within `tol`.

    Absolute tolerance on |lambda_coarse - lambda_fine| for the NEAREST fine
    eigenvalue.  Returns (kept, distances) sorted by decreasing real part.
    """
    kept, dist = [], []
    for z in ev_coarse:
        d = float(np.min(np.abs(ev_fine - z)))
        if d < tol:
            kept.append(z)
            dist.append(d)
    order = np.argsort(-np.real(kept)) if kept else np.array([], int)
    return np.array(kept)[order], np.array(dist)[order]


def converged_spectrum(a, K_coarse=96, K_fine=144, tol=1e-3, da=0.02,
                       on_no_refinement="raise", **kw):
    """The grid-independent part of the spectrum at parameter `a`.

    Guarded since leg 225 -- see the module docstring.  `K_fine` must be strictly
    greater than `K_coarse`, because the filter's whole content is that a
    discrete eigenvalue is one that survives REFINEMENT; without refinement the
    filter compares a spectrum with itself and keeps all K of them.
    `on_no_refinement` is one of `"raise"` (the default) or `"allow"` (the
    pre-repair behaviour, with a warning, so leg 203's R1 measurement -- the
    evidence that authorised this repair -- stays executable).
    """
    K_coarse, K_fine = int(K_coarse), int(K_fine)
    if K_fine <= K_coarse:
        why = ("K_fine == K_coarse == %d: the filter would compare the spectrum "
               "with ITSELF, every match distance would be 0.0, and all %d "
               "eigenvalues -- the whole discretized continuum -- would be "
               "certified as converged (leg 203 R1)" % (K_coarse, K_coarse)
               ) if K_fine == K_coarse else (
              "K_fine=%d < K_coarse=%d: a coarser second grid is not a "
              "refinement, so 'stopped moving under refinement' is not what "
              "the filter would be measuring" % (K_fine, K_coarse))
        if on_no_refinement == "raise":
            raise ValueError(
                "converged_spectrum requires K_fine > K_coarse -- " + why +
                ". Pass on_no_refinement='allow' to reproduce the pre-repair "
                "behaviour anyway.")
        if on_no_refinement != "allow":
            raise ValueError("on_no_refinement must be 'raise' or 'allow', "
                             "got %r" % (on_no_refinement,))
        warnings.warn("converged_spectrum: " + why + " -- running the "
                      "pre-repair path anyway because on_no_refinement='allow'",
                      RuntimeWarning, stacklevel=2)
    ev_c, flow_c, out_c = spectrum(a, K_coarse, da=da, **kw)
    ev_f, flow_f, out_f = spectrum(a, K_fine, da=da, **kw)
    kept, dist = match_filter(ev_c, ev_f, tol)
    return {"a": float(a), "kept": kept, "dist": dist,
            "n_total": int(ev_c.size), "n_kept": int(kept.size),
            "c_omega_coarse": out_c["c_omega"], "c_omega_fine": out_f["c_omega"],
            "residual_coarse": out_c["residual"], "residual_fine": out_f["residual"],
            "ev_coarse": ev_c, "ev_fine": ev_f}


def continuum_eigenfunction(lmbda, theta):
    """The exact a = 0 continuum eigenfunction s_lambda = (w-1)^{1-l} (w+1)^{1+l}.

    Evaluated on the circle w = e^{-i theta}.  These are the eigenfunctions of the
    a = 0 linearization written in s = delta Z (see the module docstring); they are
    admissible -- vanishing at w = -1 (X = infinity), bounded and vanishing at w = 1
    (X = 0) -- exactly for -1 < Re lambda < 1.

    THE ONE WORTH LOOKING AT IS lambda = i y.  Near the origin w - 1 ~ -2iX, so

        s ~ X^{1 - i y} = X * exp(-i y log X),      time factor  e^{i y tau},

    i.e. exp(i y (tau - log X)): a wave travelling OUTWARD IN log X at unit speed,
    exactly time-periodic with period 2 pi / y.  That is the log-periodic structure a
    DSS solution is made of -- so the oscillation the DSS lane wants IS present in
    this operator.  It is CONTINUOUS spectrum, not a discrete eigenvalue: it is the
    dilation transport carrying a scale-invariant wave out to infinity, not a bound
    state.  Nothing there can cross an axis, which is the mechanism behind this
    module's negative result rather than a restatement of it.
    """
    theta = np.asarray(theta, dtype=float)
    w = np.exp(-1j * theta)
    lm = complex(lmbda)
    return (w - 1.0 + 0j) ** (1.0 - lm) * (w + 1.0 + 0j) ** (1.0 + lm)


def continuum_defect(lmbda, n=4001, pad=1e-3):
    """Relative defect of  L s = lambda s  for the closed-form eigenfunction.

    The derivative is taken NUMERICALLY in theta and converted with
    d/dw = -(1/(i w)) d/d theta, so this checks the identity rather than re-deriving
    it: a wrong s_w would not cancel.  The endpoints theta = 0, pi are excluded --
    the eigenfunction has a branch point at each -- which is the statement being
    tested, not a fudge.
    """
    th = np.linspace(pad, np.pi - pad, int(n))
    w = np.exp(-1j * th)
    s = continuum_eigenfunction(lmbda, th)
    ds_dth = np.gradient(s, th, edge_order=2)
    s_w = ds_dth / (-1j * w)
    Ls = w * s - ((w ** 2 - 1.0) / 2.0) * s_w        # s(w=1) = 0 for Re lambda < 1
    interior = slice(int(0.05 * n), int(0.95 * n))
    num = np.max(np.abs((Ls - complex(lmbda) * s)[interior]))
    # normalise by the SIZE OF THE TERMS, not by |lambda s| -- at lambda = 0 the
    # latter is zero and the ratio would report a spurious blow-up
    den = (1.0 + abs(complex(lmbda))) * np.max(np.abs(s[interior])) + 1e-300
    return float(num / den)


def planted_eigenvalue_control(a=0.0, K_coarse=96, K_fine=144, strength=6.0,
                               width=0.25, center=1.2, tol=1e-3, da=0.02):
    """POSITIVE CONTROL: plant a bound state and check the filter finds it.

    "Nothing survived the filter" is only a measurement if the filter can find
    something that is there.  Adding a smooth localized potential V(theta) h to the
    same generator creates genuine discrete eigenvalues (a localized potential in a
    transport operator binds states); the control asserts that the filter reports
    MORE converged eigenvalues than the unperturbed operator does.
    """
    def run(K):
        flow, out = continuation(a, K=K, da=da)
        A = flow.generator(out["b"])
        th = flow.B.theta
        V = strength * np.exp(-((th - center) / width) ** 2)
        # act as multiplication by V on the VALUES, pushed back to coefficients
        Av = A + np.linalg.solve(flow.B.S, V[:, None] * flow.B.S)
        return np.linalg.eigvals(A), np.linalg.eigvals(Av)
    ev_c, evV_c = run(K_coarse)
    ev_f, evV_f = run(K_fine)
    plain, _ = match_filter(ev_c, ev_f, tol)
    planted, dist = match_filter(evV_c, evV_f, tol)
    return {"n_plain": int(plain.size), "n_planted": int(planted.size),
            "plain": plain, "planted": planted, "planted_dist": dist}
