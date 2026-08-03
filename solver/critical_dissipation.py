"""The MARGINAL case: gCLM at exactly the critical dissipation exponent.

ROUTE H v1.  Route-F v1 (§27) and Route-G v1 (§28) measured WHERE the critical
dissipation exponent sits: s_c = 1/(2 beta) = alpha/2 in gCLM's gauge, with alpha
the self-similar profile's far-field decay exponent.  Both legs then said the same
thing about the point s = s_c itself:

    at criticality the two terms balance identically, so the scaling argument
    returns ZERO INFORMATION.

That is not a footnote.  **It is exactly where Navier-Stokes lives** (beta = 1/2 by
dimensional analysis => s_c = 1, the ordinary Laplacian), and it is the reason every
scaling argument about NS comes back empty.  This module asks what actually happens
at the marginal point, in a model where the marginal point is REACHABLE because
alpha is a dial.

--------------------------------------------------------------------------
THE AUGMENTED FLOW: mu BECOMES A DYNAMICAL VARIABLE
--------------------------------------------------------------------------
Take gCLM with fractional dissipation on the line,

    omega_t + a u omega_x = omega u_x - nu Lambda^{2s} omega ,   u_x = H(omega),

and the same dynamic rescaling Route-E used: omega = A(t) Omega(X, tau), X = x/L,
dtau = A dt, with c_l = 1.  The dissipative term does not vanish and does not
survive with a fixed coefficient -- it comes back multiplied by

    mu(tau) := nu / (A L^{2s}) ,

and the rescaling ODEs A'/A^2 = -c_omega, L'/(LA) = -1 turn that into an ORDINARY
DIFFERENTIAL EQUATION for mu.  With alpha := -c_omega (Route-E's output, and the
profile's far-field exponent),

    Omega_tau = (c_omega + H Omega) Omega - X Omega_X - a U Omega_X
                                                     - mu Lambda^{2s} Omega ,   (F_mu)
    mu_tau    = (2 s - alpha[Omega, mu]) mu .                                   (M)

The pair (Omega, mu) is AUTONOMOUS, and reading it is the whole leg:

* **Route-F's s_c is an EIGENVALUE.**  Linearize (M) at the inviscid fixed point
  (mu = 0, alpha = alpha_0): the mu-direction has growth rate

        lambda_mu = 2 s - alpha_0 ,

  negative exactly when s < alpha_0 / 2 = s_c.  Route-F measured s_c by fitting a
  power law to D/N along a trajectory; it is the same number, and this says what it
  IS -- the stability exponent of the inviscid self-similar profile against the one
  direction that dissipation opens.  A scaling statement has become a spectral one.

* **At s = s_c that eigenvalue is EXACTLY ZERO.**  The marginal direction is neutral
  to linear order, so the outcome is decided by the next term.  Expanding
  alpha(mu) = alpha_0 + alpha_1 mu + O(mu^2) with 2s = alpha_0,

        mu_tau = -alpha_1 mu^2 + O(mu^3) ,

  so **the entire marginal case reduces to the SIGN OF alpha_1 = d alpha / d mu**:

        alpha_1 > 0  =>  mu decays like 1/(alpha_1 tau) -- ALGEBRAICALLY, not
                         exponentially, because the linear term is gone.  The
                         critical viscous solution relaxes onto the INVISCID
                         self-similar profile and blows up anyway.
        alpha_1 < 0  =>  mu runs away; dissipation wins and the self-similar form is
                         not reached.
        alpha_1 = 0  =>  a genuine LINE of viscous self-similar blow-ups.

  One number, and it is cheap.  That is the payoff for writing (M) down.

--------------------------------------------------------------------------
WHY THE MARGINAL PROBLEM IS EXACTLY REPRESENTABLE HERE (a lucky alignment)
--------------------------------------------------------------------------
Route-E's compactified basis (X = tan(theta/2), odd sines) makes H exact:
H(sin k th) = -cos k th + (-1)^k and H(cos k th) = sin k th.  Therefore

    Lambda = H d/dX  maps sines to sines EXACTLY,

and so does every INTEGER power of it.  So Lambda^{2s} is an exact, quadrature-free
matrix precisely when 2s is a positive integer -- i.e. when s is a half-integer.

And criticality asks for 2s = alpha.  Route-E found that alpha(a) passes through the
ODD INTEGERS at isolated a -- alpha = 1 at a = 0, alpha = 3 at a = 1/2, alpha = 5 at
a = 0.5821792673 -- and those are exactly the points where the profile is ANALYTIC
and the basis is spectral rather than algebraic.  So:

    the critical dissipative problem is exactly representable, with a spectrally
    accurate profile, at precisely the points where criticality can be posed at all.

That is a coincidence of the two conditions, not a design choice, and it is what
makes this leg cheap.  Away from those a the same equations are still correct; the
basis just converges algebraically and Lambda^{2s} is no longer a finite matrix.

**CORRECTED IN PLACE BY H4 -- THE ALIGNMENT BUYS p = 1 AND p = 3 AND NOT p = 5.**
The paragraph above is right that Lambda^p is a FINITE matrix at the resonances and
wrong to conclude that the composite is therefore ACCURATE.  Each application widens
the sine range by one mode and weights mode k by k, so Lambda^p amplifies exactly the
coefficients the single final truncation discards.  Measured at the third resonance:
`lambda_truncation` is 0.84 for the inviscid profile but **7.5e3 at K = 192 and 1.5e3
at K = 288 once mu is on** -- the dropped coefficients are three to four orders LARGER
than the kept ones.  It does fall under refinement (~K^-4), and that is the honest
statement: it starts so far above 1 that the observed rate puts the K needed to make
Lambda^5 trustworthy at ~3000, which dense linear algebra cannot reach.  The third
point is NOT REACHED, and the exact-representability claim should be read as covering
s = 1/2 and s = 3/2 only.

--------------------------------------------------------------------------
THE GAUGE HAD TO BE RE-DERIVED (banked lesson 48)
--------------------------------------------------------------------------
Route-E's c_omega = 1 + (a-1) H(Omega)(0) comes from freezing the origin slope,
(Omega_tau)_X(0) = 0.  The dissipative term contributes to that derivative -- for odd
Omega, Lambda^{2s} Omega is odd and its X-derivative at 0 is NOT zero -- so

    c_omega = 1 + (a - 1) H(Omega)(0) + mu (Lambda^{2s} Omega)_X(0) / Omega_X(0) .  (N')

Lesson 48 says re-derive a gauge when you generalize it rather than extending it;
this is that lesson applied to the previous leg's own gauge.

--------------------------------------------------------------------------
THE KNOWN ANSWER AT a = 0 (the gate everything hangs from)
--------------------------------------------------------------------------
At a = 0, s = 1/2 the marginal problem is solvable in closed form, and it is worth
saying how cheaply.  With z = H(omega) + i omega -- analytic in the LOWER half plane
for these profiles -- one has Lambda z = i z_x, so the dissipative CLM equation is

    z_t + i nu z_x = z^2 / 2 ,

a complex Burgers equation whose characteristics are the CONSTANT complex shift
x -> x - i nu t.  Substituting the CLM profile gives, for every mu_0 > 0 and every
nu > 0 with kappa := nu / mu_0,

    omega(x, t) = -2 (1 + mu_0) kappa x / ( kappa^2 (T-t)^2 + x^2 )               (E)

as an EXACT self-similar finite-time blow-up of the dissipative equation, with
||omega||_inf = (1 + mu_0)/(T - t) and length scale L = kappa (T-t), i.e. beta = 1,
alpha = 1, s_c = 1/2 -- critical, for every mu_0.  In the rescaled variables that is
the one-parameter family Omega_mu = -(1 + mu_0) sin theta with alpha == 1 IDENTICALLY,
i.e. **alpha_1 = 0 at a = 0**: the marginal direction is neutral to ALL orders and the
viscous self-similar blow-ups form a line.

`exact_a0_family` and `exact_a0_residual` are that solution and its PDE residual, and
`CriticalDissipativeFlow` rediscovers it numerically from a cold start, which is the
"build the same object twice" gate (banked lesson 3).

NOVELTY: **not claimed, and (E) is at high risk of being known.**  Explicit solutions
of the VISCOUS CLM equation by complexification go back to Schochet (CPAM 1986), and
the s*(a) = 1/c_l(a) relevance exponent for dissipative gCLM is reported in
arXiv:1908.09385 / arXiv:2207.07548.  See LITERATURE_CHECK.md.  What this module is
for is (M) and alpha_1, not (E).

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* Plain float64.  Nothing is interval-enclosed and nothing here is rigorous.
* (E) decays like 1/x, so it is NOT finite energy.  That is the honest analogy to
  Necas-Ruzicka-Sverak: their theorem excludes exactly self-similar NS blow-up in the
  FINITE-ENERGY class, and self-similar solutions with slowly-decaying (-1-homogeneous,
  non-L^2) profiles are exactly what escapes it -- Jia-Sverak constructed those.  (E)
  is the toy analogue of the escaping class, NOT a counterexample to NRS.
* s = 3/2 and s = 5/2 are HYPERviscosity.  They are used here because they are where
  criticality can be posed exactly, not because they resemble NS.  What carries over
  is the MARGINAL STRUCTURE, not the exponent.
"""

import numpy as np

from solver.rescaled_spectrum import OddCompactBasis, RescaledFlow, match_filter


# --------------------------------------------------------------------------
# Lambda = H d/dX, exact on odd sine coefficients
# --------------------------------------------------------------------------
def lambda_block(n_in):
    """sine coefficients (k = 1..n_in) -> sine coefficients (m = 1..n_in+1).

    Omega = sum_k b_k sin k th.  Then Omega_th = sum k b_k cos k th and
    d/dX = (1 + cos th) d/d th gives

        Omega_X = sum_k k b_k [ cos k th + (cos(k+1)th + cos(k-1)th)/2 ] ,

    a COSINE series; and H(cos m th) = sin m th for m >= 1 with H(1) = 0.  So the
    m = 0 row is DROPPED, not zeroed by hand -- H kills constants on the line, which
    is the same fact that puts the (-1)^k in H(sin k th).
    """
    n = int(n_in)
    C = np.zeros((n + 2, n))
    for k in range(1, n + 1):
        C[k, k - 1] += float(k)
        C[k + 1, k - 1] += 0.5 * k
        C[k - 1, k - 1] += 0.5 * k
    return C[1:n + 2, :]                      # rows m = 1..n+1


def lambda_power(K, p):
    """Lambda^p as a K x K matrix on odd sine coefficients, p a positive integer.

    Each application widens the sine range by one mode, so the composite is built at
    full width and truncated ONCE at the end.  The truncation error is the size of
    the coefficients being dropped, which the K-ladder measures; `lambda_truncation`
    reports it directly rather than leaving it implicit.
    """
    K, p = int(K), int(p)
    if p < 1:
        raise ValueError("p must be a positive integer (2s = p)")
    M = np.eye(K)
    n = K
    for _ in range(p):
        M = lambda_block(n) @ M
        n += 1
    return M[:K, :], M[K:, :]                 # (kept, dropped)


def lambda_truncation(b, K, p):
    """|dropped coefficients| / |kept coefficients| for Lambda^p b -- the honest
    size of the one approximation in this module's operator."""
    keep, drop = lambda_power(K, p)
    num = float(np.max(np.abs(drop @ b))) if drop.size else 0.0
    return num / (float(np.max(np.abs(keep @ b))) + 1e-300)


# the analytic gate: Lambda[sin th] = sin th + (1/2) sin 2th.
#   sin th = 2X/(1+X^2) = 2 pi Q_1(X) with Q_a the conjugate Poisson kernel, whose
#   Fourier transform is -i sgn(xi) e^{-a|xi|}; so Lambda Q_a = -d Q_a/da, giving
#   Lambda[X/(1+X^2)] = 2X/(1+X^2)^2 = (sin th + (1/2) sin 2th)/2.
LAMBDA_SIN1 = np.array([1.0, 0.5])


# --------------------------------------------------------------------------
# the dissipative rescaled flow
# --------------------------------------------------------------------------
class CriticalDissipativeFlow(RescaledFlow):
    """(F_mu) in Route-E's compactified odd sine basis.  2s = p, a positive integer.

    Everything Route-E built is reused unchanged -- the exact H, the exact dilation
    operator, the quadrature-free velocity, the Newton with the appended dilation
    gauge.  The only additions are the -mu Lambda^p term and the re-derived gauge
    (N').  Setting mu = 0 reproduces `RescaledFlow` bit-for-bit, which is the first
    gate in the test suite.
    """

    def __init__(self, a, mu=0.0, p=1, K=96):
        super().__init__(a, K=K)
        self.mu = float(mu)
        self.p = int(p)
        self.s = 0.5 * self.p
        Lp, _drop = lambda_power(self.K, self.p)
        self.Lp = Lp
        self.Lam = self.B.S @ Lp                                  # b -> Lambda^p Om
        self.lam_dx0 = 2.0 * (self.B.k.astype(float) @ Lp)        # b -> (Lambda^p Om)_X(0)

    # -- the re-derived gauge (N') -----------------------------------------
    def c_omega(self, b):
        B = self.B
        omx0 = 2.0 * (B.k @ b)
        return (1.0 + (self.a - 1.0) * (B.h0 @ b)
                + self.mu * (self.lam_dx0 @ b) / omx0)

    def _dc_omega(self, b):
        """d c_omega / d b -- needed for an EXACT Jacobian, not a finite-difference one."""
        B = self.B
        kk = 2.0 * B.k.astype(float)
        omx0 = kk @ b
        d = (self.a - 1.0) * B.h0.astype(float)
        if self.mu != 0.0:
            num = self.lam_dx0 @ b
            d = d + self.mu * (self.lam_dx0 * omx0 - num * kk) / (omx0 ** 2)
        return d

    def residual(self, b):
        B = self.B
        Om = B.S @ b
        R = (self.c_omega(b) + B.H @ b) * Om - B.XD @ b
        if self.a != 0.0:
            R = R - self.a * (B.U @ b) * (B.DX @ b)
        if self.mu != 0.0:
            R = R - self.mu * (self.Lam @ b)
        return R

    def jacobian(self, b):
        B = self.B
        Om = B.S @ b
        HOm = B.H @ b
        cw = self.c_omega(b)
        J = ((cw + HOm)[:, None] * B.S + Om[:, None] * B.H
             + np.outer(Om, self._dc_omega(b)) - B.XD)
        if self.a != 0.0:
            J = J - self.a * ((B.DX @ b)[:, None] * B.U + (B.U @ b)[:, None] * B.DX)
        if self.mu != 0.0:
            J = J - self.mu * self.Lam
        return J

    # -- the two numbers the leg is about ----------------------------------
    def alpha(self, b):
        """alpha = -c_omega: the profile's far-field decay exponent, and the thing
        criticality compares against 2s."""
        return -float(self.c_omega(b))

    def mu_growth(self, b):
        """The right-hand side of (M) divided by mu: 2s - alpha.  Zero AT criticality."""
        return 2.0 * self.s - self.alpha(b)


# --------------------------------------------------------------------------
# the branch in mu, and alpha_1 = d alpha / d mu
# --------------------------------------------------------------------------
def inviscid_seed(a, K=96, da=0.02, **kw):
    """Route-E's own continuation from the exact a = 0 anchor -- unchanged."""
    from solver.rescaled_spectrum import continuation
    flow, out = continuation(a, K=K, da=da, **kw)
    return out["b"], out


def mu_branch(a, p, mus, K=96, da=0.02, b0=None, **kw):
    """Continue the fixed point in mu from the inviscid profile at the same a.

    Continuation, not search: each mu is seeded by the previous one, so the branch is
    FOLLOWED.  Returns one record per mu with the residual, alpha, the gauge defect
    and the Lambda^p truncation, so a caller can reject a rung instead of averaging
    over it.
    """
    b = inviscid_seed(a, K=K, da=da)[0] if b0 is None else np.asarray(b0, float)
    kk = np.arange(1, K + 1, dtype=float)
    rows = []
    for mu in np.asarray(mus, float):
        flow = CriticalDissipativeFlow(a, mu=float(mu), p=p, K=K)
        out = flow.newton(b0=b, **kw)
        b = out["b"]
        rows.append({
            "mu": float(mu), "K": int(K), "a": float(a), "p": int(p),
            "residual": float(out["residual"]),
            "alpha": flow.alpha(b),
            "mu_growth": flow.mu_growth(b),
            "gauge": float(kk @ b + 1.0),
            "omega_x0": float(2.0 * (kk @ b)),
            "tail": float(out["tail"]),
            "lambda_truncation": lambda_truncation(b, K, p),
            "b": b.copy(),
        })
    return rows


def alpha_slope(rows, alpha_0=None):
    """alpha_1 = d alpha / d mu AT mu = 0, by extrapolating the SECANTS.

    A straight fit of alpha against mu over a finite mu-window returns the CHORD, not
    the derivative, and alpha(mu) is visibly curved: at a = 1/2 the chord over
    mu <= 0.2 is 0.1256 while the true slope at the origin is 0.1337, a 6% error in
    the one number the marginal verdict is quoted from.  So the secants
    (alpha(mu) - alpha_0)/mu are fitted linearly in mu and extrapolated to mu = 0 --
    the same "add rungs until the exponent stops moving" discipline as banked lesson
    52, applied to a derivative instead of a rate.

    Only the SIGN of alpha_1 decides the marginal verdict, and the chord and the
    extrapolant agree on that; the magnitude is what needs the care.
    """
    mu = np.array([r["mu"] for r in rows], float)
    al = np.array([r["alpha"] for r in rows], float)
    if alpha_0 is None:
        if not np.any(mu == 0.0):
            raise ValueError("need a mu = 0 rung, or an explicit alpha_0")
        alpha_0 = float(al[mu == 0.0][0])
    m = mu > 0
    sec = (al[m] - alpha_0) / mu[m]
    chord = float(np.polyfit(mu[m], al[m], 1)[0])
    if m.sum() >= 2:
        c = np.polyfit(mu[m], sec, 1)
        a1 = float(c[1])                       # the intercept: the secant at mu -> 0
        a2 = float(c[0])                       # curvature: alpha ~ a0 + a1 mu + a2 mu^2
    else:
        a1, a2 = float(sec[0]), float("nan")
    return {"alpha_0": float(alpha_0), "alpha_1": a1, "alpha_2": a2,
            "alpha_1_chord": chord,
            "mu": mu[m].tolist(), "secants": sec.tolist(),
            "secant_spread": float(sec.max() - sec.min())}


def marginal_verdict(alpha_1, tol=1e-9):
    """What (M) does at criticality, given alpha_1.  A sentence, not a number --
    and it is a unit test, because the sign is easy to write down backwards
    (banked lesson 60)."""
    if abs(alpha_1) <= tol:
        return "neutral_line"       # mu_tau = 0: a line of viscous self-similar blow-ups
    if alpha_1 > 0:
        return "relaxes_to_inviscid"   # mu_tau = -alpha_1 mu^2 < 0: mu ~ 1/(alpha_1 tau)
    return "dissipation_runs_away"


def mu_decay_time(alpha_1, mu0, target):
    """tau at which mu falls from mu0 to `target` under mu_tau = -alpha_1 mu^2.

    The point of having this is that the answer is ALGEBRAIC, 1/(alpha_1 tau), not
    exponential -- a decade of mu costs nine times the tau the previous decade did,
    and tau is itself logarithmic in (T-t).  The critical case relaxes onto the
    inviscid profile impossibly slowly in physical time, which is worth a number.
    """
    if alpha_1 <= 0:
        return float("inf")
    return float((1.0 / target - 1.0 / mu0) / alpha_1)


# --------------------------------------------------------------------------
# the exact a = 0 marginal family
# --------------------------------------------------------------------------
def exact_a0_family(mu, X):
    """The gauge-fixed member of (E) in rescaled variables, on the grid X.

    With the dilation gauge Omega_X(0) = -2 the equation's parameter mu and the
    family parameter mu_0 are related by mu = mu_0 (1 + mu_0): the gauge fixes the
    width to lam = 1 + mu_0, and Lambda's coefficient scales with the width.
    """
    mu = float(mu)
    mu0 = 0.5 * (-1.0 + np.sqrt(1.0 + 4.0 * mu))
    lam = 1.0 + mu0
    X = np.asarray(X, float)
    return -2.0 * (1.0 + mu0) * lam * X / (lam ** 2 + X ** 2), mu0, lam


def exact_a0_spacetime(x, t, nu, mu0, T=1.0):
    """(E) itself: omega, H(omega), Lambda(omega), omega_t -- all in closed form.

    Everything comes from z = 2(1+mu_0) kappa / (kappa (T-t) + i x), for which
    omega = Im z, H(omega) = Re z, Lambda(omega) = Re(z_x) (because Lambda z = i z_x
    on the lower-half-plane-analytic side) and omega_t = Im(z_t).  No quadrature and
    no differencing, so `exact_a0_residual` tests the SOLUTION rather than a
    discretization of it.
    """
    x = np.asarray(x, float)
    kappa = float(nu) / float(mu0)
    D = kappa * (T - float(t)) + 1j * x
    c = 2.0 * (1.0 + float(mu0)) * kappa
    z = c / D
    z_t = c * kappa / D ** 2                     # d/dt of c/D with dD/dt = -kappa
    z_x = -1j * c / D ** 2
    return {"omega": np.imag(z), "H_omega": np.real(z),
            "lambda_omega": np.real(z_x), "omega_t": np.imag(z_t), "z": z}


def exact_a0_residual(x, t, nu, mu0, T=1.0):
    """Pointwise |omega_t - omega H(omega) + nu Lambda omega| for (E), relative."""
    q = exact_a0_spacetime(x, t, nu, mu0, T=T)
    r = q["omega_t"] - q["omega"] * q["H_omega"] + float(nu) * q["lambda_omega"]
    scale = float(np.max(np.abs(q["omega"] * q["H_omega"]))) + 1e-300
    return float(np.max(np.abs(r))) / scale


# --------------------------------------------------------------------------
# the spectrum of the dissipative fixed point, and its control
# --------------------------------------------------------------------------
def dissipative_spectrum(a, p, mu, K, da=0.02, b0=None, **kw):
    rows = mu_branch(a, p, _ladder_to(mu), K=K, da=da, b0=b0, **kw)
    flow = CriticalDissipativeFlow(a, mu=mu, p=p, K=K)
    b = rows[-1]["b"]
    return np.linalg.eigvals(flow.generator(b)), flow, rows[-1]


def _ladder_to(mu, step=0.05):
    if mu == 0.0:
        return [0.0]
    n = max(1, int(round(abs(mu) / step)))
    return list(np.linspace(0.0, mu, n + 1))[1:]


def converged_dissipative_spectrum(a, p, mu, K_coarse=96, K_fine=144, tol=1e-3,
                                   da=0.02, **kw):
    """Route-E's convergence filter, applied to the DISSIPATIVE generator.

    The filter is not decoration here either: the inviscid operator's non-symmetry
    spectrum is CONTINUOUS and never stops moving under refinement, and the whole
    question this module asks is whether dissipation converts any of it into
    something that does.
    """
    ev_c, flow_c, row_c = dissipative_spectrum(a, p, mu, K_coarse, da=da, **kw)
    ev_f, flow_f, row_f = dissipative_spectrum(a, p, mu, K_fine, da=da, **kw)
    kept, dist = match_filter(ev_c, ev_f, tol)
    return {"a": float(a), "p": int(p), "mu": float(mu),
            "kept": kept, "dist": dist,
            "n_total": int(ev_c.size), "n_kept": int(kept.size),
            "alpha_coarse": row_c["alpha"], "alpha_fine": row_f["alpha"],
            "residual_coarse": row_c["residual"], "residual_fine": row_f["residual"],
            "ev_coarse": ev_c, "ev_fine": ev_f}


def amplitude_eigenvalue(mu):
    """MEASURED, not derived: the a = 0 amplitude mode sits at -sqrt(1 + 4 mu).

    At mu = 0 this is Route-E's exact symmetry eigenvalue -1.  Dissipation breaks the
    amplitude symmetry (rescaling omega changes the effective size of nu), so that
    eigenvalue is free to move, and it moves LEFT along the real axis -- the amplitude
    mode becomes more stable, not less.  In dilation-invariant terms the value is
    -(1 + 2 mu_0) with mu_0 = mu/lam the width-normalised dissipation strength.

    THIS IS AN EMPIRICAL FIT TO SIX DIGITS OVER A mu-LADDER AND IS NOT DERIVED.
    It is in the module because it is gated, not because it is understood.
    """
    return -np.sqrt(1.0 + 4.0 * np.asarray(mu, float))


def planted_dissipative_control(a=0.0, p=1, mu=0.5, K_coarse=96, K_fine=144,
                                strength=6.0, width=0.25, center=1.2, tol=1e-3,
                                da=0.02):
    """POSITIVE CONTROL for the dissipative filter (banked lesson 47).

    "The ladder does not move with mu, and nothing goes complex" is a claim about
    ABSENCE.  Plant a localized potential in the same dissipative generator and check
    the filter reports strictly more converged eigenvalues, so that the absence is a
    measurement rather than a filter that cannot see.
    """
    def run(K):
        ev, flow, row = dissipative_spectrum(a, p, mu, K, da=da)
        A = flow.generator(row["b"])
        th = flow.B.theta
        V = strength * np.exp(-((th - center) / width) ** 2)
        Av = A + np.linalg.solve(flow.B.S, V[:, None] * flow.B.S)
        return ev, np.linalg.eigvals(Av)
    ev_c, evV_c = run(K_coarse)
    ev_f, evV_f = run(K_fine)
    plain, _ = match_filter(ev_c, ev_f, tol)
    planted, dist = match_filter(evV_c, evV_f, tol)
    return {"n_plain": int(plain.size), "n_planted": int(planted.size),
            "plain": plain, "planted": planted, "planted_dist": dist}


# --------------------------------------------------------------------------
# where criticality can be posed exactly
# --------------------------------------------------------------------------
#   a at which Route-E's alpha(a) is an odd integer.  alpha = 2s => s = alpha/2, and
#   Lambda^{2s} is an exact matrix exactly when 2s is an integer.  a = 0.5821792673
#   is Route-E v1's third point -- the one that cost banked lesson 52.
CRITICAL_POINTS = (
    {"a": 0.0,          "alpha": 1, "p": 1, "s": 0.5, "label": "a=0 (CLM)"},
    {"a": 0.5,          "alpha": 3, "p": 3, "s": 1.5, "label": "a=1/2"},
    {"a": 0.5821792673, "alpha": 5, "p": 5, "s": 2.5, "label": "a=0.58218"},
)
