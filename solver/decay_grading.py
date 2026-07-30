"""Decay-graded function spaces for the Route-D v3 space-pair analysis.

Route-D v2 (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_DRESS.md) ended with a
constructive suggestion: the gauged finite-section inverse A of the linearized
two-scale operator LOSES exactly one power of decay, so grade the CODOMAIN by one
mode power and ||A|| goes flat at 3.000.  This module is the machinery needed to
check whether that suggestion can actually carry a Newton-Kantorovich certificate,
i.e. whether the SAME pair of spaces also controls the quadratic term.

It provides three independent things.

(1) THE EXACT QUADRATIC.  `quadratic_coeffs` writes the sine coefficients of
    Q(h) = h H(h) in closed form.  The identity worth banking is that Q is a PURE
    CONVOLUTION -- no difference frequencies at all:

        Q(h) = (1/2) sum_{m>=0} ( sum_{j+k=m} h_j h_k ) sin(m theta).       (Q)

    Proof: with H(cos k th) = sin k th (solver/nk_fourier, unconditional),
    h H(h) = sum_{j>=0,k>=1} h_j h_k cos(j th) sin(k th)
           = (1/2) sum_{j>=0,k>=1} h_j h_k [ sin((j+k) th) + sin((k-j) th) ].
    The difference part is antisymmetric in (j,k) once the missing k=0 row is
    added back, and the same k=0 row is what the sum part is missing, so the two
    corrections cancel EXACTLY and only sum frequencies survive.  (Structurally:
    h + i H(h) is a boundary value of a Hardy-space function and 2 h H(h) is the
    imaginary part of its square; squaring a holomorphic function cannot produce
    difference frequencies.)

    Consequence -- the sharp weighted bound.  For X = ell^1_u (cosine side) and
    Y = ell^1_v (sine side),

        ||Q(h)||_Y <= M ||h||_X^2   for all h    <==>   sup_{j,k} v_{j+k}/(u_j u_k) < oo

    with the two-sided constant  (1/4) sup <= M <= (1/2) sup  (`algebra_constant`).
    Sufficiency is termwise from (Q); necessity comes from h = xi e_j + eta e_k,
    optimized over xi, eta > 0, which gives v_{j+k} <= 4 M u_j u_k.

(2) THE DECAY DICTIONARY.  `cos_power_coeffs` gives the EXACT cosine coefficients
    of the model profile

        f_alpha(X) = (1 + X^2)^{-alpha/2} = |cos(theta/2)|^alpha,

    the canonical element of the "decays like X^{-alpha}" class, via the
    generalized binomial series (a stable two-term recursion, no Gamma of a
    negative argument).  Together with H(cos k th) = sin k th this makes H f_alpha
    computable to machine precision with no quadrature, which is what lets the
    far-field asymptotics be MEASURED rather than assumed.

(3) THE FAR-FIELD BLOCK.  `farfield_inverse_norm` discretizes the far-field model
    operator of Route-D v2 D6,

        (L h)(X) = -c h_X - h/X,                                            (L)

    on a geometric grid and returns its induced norm between the decay-graded sup
    norms ||h|| = sup X^alpha |h|, ||g|| = sup X^{alpha+1} |g|.  L is bidiagonal
    with an M-matrix sign pattern in this discretization, so the induced norm is
    ONE linear solve (no dense inverse): ||L^{-1}|| = max_i w_h(i) (L^{-1} 1/w_g)_i.

    The exact solution operator is (X^2 h)' = -(2/c) X^2 g at c = 1/2, giving
    ||L^{-1}|| = 2/|alpha - 2|: a pole at alpha = 2 because X^{-2} is exactly the
    homogeneous solution at c = 1/2 (and exactly the decay of the anchor
    Omega_2 = -1/(1+X^2)).  The far field is RESONANT at the anchor's own decay
    rate; detuning to alpha = 2 -/+ eps costs a factor 2/eps and nothing else.
"""

import math

import numpy as np

# ---------------------------------------------------------------------------
# (1) the exact quadratic and the sharp weighted-algebra constant
# ---------------------------------------------------------------------------


def quadratic_coeffs(h, M=None):
    """Sine coefficients of Q(h) = h H(h), by the pure-convolution identity (Q).

    `h` is the cosine-coefficient vector (h[0] = h_0).  Returns q_1..q_M with
    q_m = (1/2) sum_{j+k=m} h_j h_k; M defaults to the full 2K modes generated.

    This is deliberately an INDEPENDENT second implementation of the quadratic
    part of solver.nk_fourier.residual (which builds it as a double loop over
    sum AND difference frequencies).  test_decay_grading gate 4 requires the two
    to agree exactly -- the "build the same object twice" rule that caught the
    k=0 fold bug in Route-D v1.
    """
    h = np.asarray(h, dtype=float)
    K = h.size - 1
    M = max(2 * K, 1) if M is None else int(M)
    full = np.convolve(h, h)                     # (full)_m = sum_{j+k=m} h_j h_k
    q = np.zeros(M)
    n = min(M, full.size - 1)                    # mode 0 is dropped (sin 0 = 0)
    q[:n] = 0.5 * full[1:n + 1]
    return q


def algebra_constant(u, v):
    """Sharp constant of the quadratic bound ||Q(h)||_{ell^1_v} <= M ||h||^2_{ell^1_u}.

    Returns (S, M_lo, M_hi, argmax) where

        S = max_{j+k <= len(v)} v_{j+k} / (u_j u_k),    M_hi = S/2,  M_lo = S/4,

    so the bound holds with M = S/2 and cannot hold with any M < S/4.  `u` is
    indexed from mode 0, `v` from mode 1 (v[0] is the weight of sin(theta)).

    The whole no-go theorem is read off this one expression: taking k = 0 gives
    S >= v_m / (u_0 u_m), i.e.  v_m / u_m <= S u_0  UNIFORMLY IN m, whereas a
    bounded far-field inverse needs v_m / u_m to grow like m.
    """
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    j = np.arange(u.size)[:, None]
    k = np.arange(u.size)[None, :]
    m = j + k
    ok = (m >= 1) & (m <= v.size)
    ratio = np.where(ok, v[np.clip(m - 1, 0, v.size - 1)] / np.outer(u, u), -np.inf)
    flat = int(np.argmax(ratio))
    best = float(ratio.flat[flat])
    arg = (flat // u.size, flat % u.size)
    return best, float(best / 4.0), float(best / 2.0), arg


# ---------------------------------------------------------------------------
# (2) the decay dictionary: f_alpha = (1+X^2)^{-alpha/2} = |cos(theta/2)|^alpha
# ---------------------------------------------------------------------------


def X_of_theta(theta):
    """X = tan(theta/2); theta in (-pi, pi) maps onto the whole line."""
    return np.tan(np.asarray(theta, dtype=float) / 2.0)


def theta_of_X(X):
    """Inverse of `X_of_theta`."""
    return 2.0 * np.arctan(np.asarray(X, dtype=float))


def cos_power_coeffs(alpha, K):
    """Cosine coefficients a_0..a_K of |cos(theta/2)|^alpha = (1+X^2)^{-alpha/2}.

    From the generalized binomial expansion of cos^alpha,

        a_0 = 2^{-alpha} Gamma(alpha+1) / Gamma(alpha/2+1)^2,
        a_1 = 2 a_0 (alpha/2) / (alpha/2 + 1),
        a_{k+1} = a_k (alpha/2 - k) / (alpha/2 + k + 1),        k >= 1,

    evaluated by the recursion so that no Gamma of a negative argument is ever
    formed.  Sanity anchors: alpha = 0 -> (1, 0, 0, ...);  alpha = 2 ->
    (1/2, 1/2, 0, ...) because (1+X^2)^{-1} = (1 + cos theta)/2 exactly.

    For non-even alpha the ratio tends to -1, so the coefficients ALTERNATE and
    decay like k^{-alpha-1}: alternation in k is concentration at theta = pi,
    i.e. mass at X = infinity.  That is the precise sense in which "decay in X"
    is a statement about the k-oscillatory part of the coefficient sequence and
    NOT about any diagonal weight -- a single mode cos(k theta) does not decay at
    all (it equals (-1)^k at theta = pi).
    """
    K = int(K)
    a = np.zeros(K + 1)
    half = 0.5 * alpha
    a[0] = math.exp(math.lgamma(alpha + 1.0) - 2.0 * math.lgamma(half + 1.0)
                    - alpha * math.log(2.0))
    if K >= 1:
        a[1] = 2.0 * a[0] * half / (half + 1.0)
    for k in range(1, K):
        a[k + 1] = a[k] * (half - k) / (half + k + 1.0)
    return a


def _folded_angles(theta):
    """(delta, parity) with cos(k th) = parity^k cos(k delta), |delta| <= pi/2.

    The far field is theta -> +-pi, where k theta reaches ~ 3e5 radians for the
    truncation lengths this module needs; np.sin/np.cos would then be evaluating a
    hugely range-reduced argument.  Folding through
    cos(k(pi - d)) = (-1)^k cos(k d),  sin(k(pi - d)) = -(-1)^k sin(k d)
    keeps the argument O(k |pi - theta|) = O(1) exactly where the accuracy matters.
    """
    th = np.atleast_1d(np.asarray(theta, dtype=float))
    delta = np.where(np.abs(th) <= 0.5 * np.pi, th, np.sign(th) * np.pi - th)
    parity = np.where(np.abs(th) <= 0.5 * np.pi, 1.0, -1.0)
    return delta, parity


def eval_cos_series(a, theta):
    """sum_k a_k cos(k theta) at the given theta (dense, exact to truncation)."""
    a = np.asarray(a, dtype=float)
    d, p = _folded_angles(theta)
    k = np.arange(a.size)
    sgn = p[:, None] ** k[None, :]
    return (np.cos(np.outer(d, k)) * sgn) @ a


def eval_sin_series(a, theta):
    """sum_k a_k sin(k theta) -- i.e. H of `eval_cos_series`, by H(cos k) = sin k."""
    a = np.asarray(a, dtype=float)
    d, p = _folded_angles(theta)
    k = np.arange(a.size)
    sgn = p[:, None] ** (k[None, :] + 1)      # sin(k th) = parity^{k+1} sin(k delta)
    return (np.sin(np.outer(d, k)) * sgn) @ a


def hilbert_of_cos_power(alpha, X, K=100000):
    """H(f_alpha) evaluated on the line, via the exact coefficients + H(cos)=sin.

    No quadrature: the only error is the coefficient truncation, whose tail is
    O(K^{-alpha}).  Resolving the far field at abscissa X needs K >> X/2 (mode k
    resolves |pi - theta| ~ 1/k and |pi - theta| ~ 2/X), which is why K defaults
    to 1e5 and callers should stay below X ~ 1e4.
    """
    return eval_sin_series(cos_power_coeffs(alpha, K), theta_of_X(X))


def cos_power_mass(alpha):
    """int f_alpha dX = sqrt(pi) Gamma((alpha-1)/2) / Gamma(alpha/2)  (alpha > 1).

    This is the constant in the far-field law H(f)(X) ~ (1/(pi X)) int f, hence
    the predicted limit of X^{alpha+1} f_alpha H(f_alpha) -- the oracle that gates
    "the quadratic term gains exactly one power of decay".
    """
    if alpha <= 1.0:
        raise ValueError("f_alpha is not integrable for alpha <= 1")
    return math.exp(0.5 * math.log(math.pi)
                    + math.lgamma(0.5 * (alpha - 1.0)) - math.lgamma(0.5 * alpha))


# ---------------------------------------------------------------------------
# (3) the far-field block: L h = -c h_X - h/X between decay-graded sup norms
# ---------------------------------------------------------------------------


def farfield_grid(X0=1.0, Xmax=1e8, n=20001):
    """Geometric grid on [X0, Xmax] -- uniform in log X, as the far field wants."""
    return np.geomspace(float(X0), float(Xmax), int(n))


def farfield_inverse_norm(alpha, c=0.5, X0=1.0, Xmax=1e12, n=8001):
    """Induced norm of L^{-1} between ||h|| = sup X^a |h| and ||g|| = sup X^{a+1} |g|.

    L h = -c h_X - h/X.  In tau = log X (the variable the far field is uniform in)
    the equation is  dh/dtau = -beta h - beta X g,  beta = 1/c, and it is
    discretized by the trapezoidal rule -- second order, so the exponent drift
    that a one-sided difference accumulates over a dozen decades (4% at
    Xmax = 1e12, n = 8001) does not appear.

    The direction of integration is set by which solution the space admits:

      alpha < 2 : the homogeneous solution X^{-1/c} = X^{-2} decays FASTER than
                  the space requires, so it is admissible and the operator has a
                  kernel (it is the same kernel direction the two Route-D gauge
                  conditions already remove); the matching condition from the
                  compact core, h(X0) = 0, selects a solution and the recursion
                  runs outward.
      alpha > 2 : the homogeneous solution is NOT in the space, decay at infinity
                  selects the solution, and the recursion runs inward from
                  h(Xmax) = 0.

    Every coefficient in either recursion is non-negative, so feeding the extremal
    magnitude |g| = 1/w_g gives the induced norm in ONE pass -- no dense inverse.

    Returns (norm, predicted) with predicted = 2/|alpha - 2|, the exact continuum
    value from (X^{1/c} h)' = -(1/c) X^{1/c} g.  The finite domain costs a
    relative (X0/Xmax)^{2-alpha} on the alpha < 2 branch, so Xmax must be large.
    """
    if abs(alpha - 2.0) < 1e-12:
        return float("inf"), float("inf")
    x = farfield_grid(X0, Xmax, n)
    dtau = np.diff(np.log(x))
    beta = 1.0 / c
    src = x ** (-alpha)                       # beta * X * |g|, |g| = X^{-alpha-1}
    h = np.zeros(x.size)

    if alpha < 2.0:
        for i in range(1, x.size):
            p, q = 1.0 / dtau[i - 1] + 0.5 * beta, 1.0 / dtau[i - 1] - 0.5 * beta
            h[i] = (q * h[i - 1] + 0.5 * beta * (src[i] + src[i - 1])) / p
    else:
        for i in range(x.size - 1, 0, -1):
            p, q = 1.0 / dtau[i - 1] + 0.5 * beta, 1.0 / dtau[i - 1] - 0.5 * beta
            if q <= 0.0:
                raise ValueError("grid too coarse: need dtau < 2c")
            h[i - 1] = (p * h[i] + 0.5 * beta * (src[i] + src[i - 1])) / q
    return float(np.max(x ** alpha * h)), float(2.0 / abs(alpha - 2.0))


def farfield_inverse_norm_finite(alpha, X0=1.0, Xmax=1e12):
    """The EXACT continuum norm on the truncated domain [X0, Xmax].

        2 (1 - (X0/Xmax)^{|2-alpha|}) / |2 - alpha|

    -- both branches at once.  It is what a finite computation can actually
    match: the infinite-domain law 2/|alpha-2| is approached only as
    (X0/Xmax)^{|2-alpha|} -> 0, which is 6% at alpha = 1.9, Xmax = 1e12, so
    comparing a truncated measurement against 2/|alpha-2| understates agreement
    near the resonance.
    """
    e = abs(2.0 - alpha)
    return float(2.0 * (1.0 - (X0 / Xmax) ** e) / e)


def farfield_symbol_coefficient(alpha, c=0.5):
    """Leading far-field coefficient of DF applied to a X^{-alpha} profile.

    With h ~ X^{-alpha}, Omega_2 = -1/(1+X^2) ~ -X^{-2} and
    H(Omega_2) = -X/(1+X^2) ~ -1/X,

        DF h = h H(Omega_2) + Omega_2 H(h) - c h_X
             ~ [ -1 + c alpha ] X^{-alpha-1} + O(X^{-3}),

    so  lim X^{alpha+1} (DF h) = c alpha - 1 = (alpha - 2)/2 at c = 1/2.  It
    VANISHES at alpha = 2 -- the same resonance that puts the pole in
    `farfield_inverse_norm`, seen from the operator side instead of the inverse.
    """
    return float(c * alpha - 1.0)
