"""Breden-Chu's weighted-Sobolev setting H^2(mu), mu = e^{|x|^2/4}/Z -- reproduction machinery.

WHAT THIS IS, AND WHAT IT IS NOT
-----------------------------------------------------------------------------
This module implements, from their published formulas, the machinery of

    Maxime Breden, Hugo Chu, "Constructive proofs for some semilinear PDEs on
    H^2(e^{|x|^2/4}, R^d)", arXiv:2404.04054v2 (18 Jan 2026),

specifically everything needed to recompute the constants of their **Theorem 42**
(section 6, the generalised viscous Burgers self-similar profile -- the one result in
the paper carrying a genuine first-order term f(x, u, grad u), and the one Remark 40
is attached to).

It is a NEW module and touches no existing solver file (leg 256's territory grant).
`capabilities.py` was grepped first: nothing in the tree holds the operator
L = -Delta - (x/2).grad, its eigenbasis, H^2(mu), or a Gauss-Laguerre quadrature for
products of half-Hermite functions.  The single Laguerre hit,
`solver/origin_h2_certificate.py::project_to_laguerre`, belongs to the origin-H^2
realization `plan_of_record.py` names DEAD and is not reusable here.

THE BAN, AND WHY THIS FILE IS NOT INSIDE IT
-----------------------------------------------------------------------------
`plan_of_record.py`'s standing ban forbids re-attempting the ell^1-Fourier /
radii-polynomial machinery measured dead in three realizations (ell^1_w coefficient
basis, collocation basis, origin-H^2-capped-at-a=0).  NONE of the three appears here:

  * the norm is ||u||_{H^2(mu)} = ||L u||_{L^2(mu)} -- a HILBERT (ell^2-type,
    eigenvalue-weighted) norm, not the ell^1_w Banach-algebra norm;
  * the basis is the even half-Hermite family psi_m = e^{-x^2/4} Hhat_{2m}(x/2),
    i.e. Laguerre L_m^{(-1/2)}(x^2/4) -- not Fourier, not collocation, not the
    compactified X = tan(theta/2) modes;
  * the nonlinearity is tamed by the Sobolev embedding H^2(mu) -> C^0_0 plus a
    quadrature rule, not by an ell^1 Banach-algebra property;
  * the tail is tamed by the genuine Poincare inequality that L's spectral gap d/2
    supplies on the UNBOUNDED domain -- there is no domain truncation and no
    compactification.

This module makes NO claim that the ban is lifted.  Leg 257 is the leg that argues
distinctness; this file supplies reproduction evidence only.

ARITHMETIC MODEL -- STATED BEFORE ANY NUMBER LEAVES THIS FILE
-----------------------------------------------------------------------------
Breden-Chu's proof runs in INTERVAL ARITHMETIC over 16384-bit BigFloat (their
`quadrature.jl` sets prec = 16384 in order to enclose, by the intermediate value
theorem, the roots of a degree-4503 Laguerre polynomial).  This environment has numpy
only -- no scipy, no mpmath.  **Everything here is float64.**  This module reproduces
their certificate's CONSTANTS, not their proof.  Nothing it returns is a rigorous
enclosure and nothing it returns may be cited as one.

What makes the float number trustworthy at the resolution the reproduction needs is
MEASURED here rather than asserted, by three gates any caller can run:

  `check_quadrature_identities`  their own two exact rational integrals, the same two
                                 `quadrature.jl` checks:
                                    sqrt(5) pi Int psi_1^4 psi_1'^2 e^{-r^2/4} = 669/31250
                                    pi      Int psi_1^3 psi_1'   e^{-r^2/4} = -29/324
  `check_orthonormality`         <psi_a, psi_b> = delta_ab for ALL a,b <= n, which is
                                 the all-mode version of the same test and is the one
                                 that would catch a high-mode cancellation loss
  `check_weight_normalisation`   sum_i w_i = Gamma(alpha+1) for each Gauss-Laguerre rule

NUMERICAL DESIGN NOTES (the two things that are actually hard in float64)
-----------------------------------------------------------------------------
1.  RANGE.  The quadrature nodes for n = 1500 run out to s ~ 4N ~ 1.8e4, where the
    Gauss-Laguerre weight is ~e^{-1.8e4} and the Laguerre polynomial value is ~1e1220.
    Neither factor is representable; their PRODUCT is.  Every Vandermonde entry is
    therefore assembled as `value * exp(running_log_scale + log_weight - log_norm)`,
    with the three-term recurrence carrying a per-node running log scale that is
    renormalised at every step.  Breden-Chu do not need this: BigFloat's exponent
    range makes the factors representable directly.

2.  NODES.  Without scipy there is no Gauss-Laguerre rule to call.  Nodes are obtained
    as the eigenvalues of the symmetric tridiagonal Jacobi matrix by STURM BISECTION
    (which cannot converge to the wrong root -- the Sturm count fixes each root's index
    exactly), then polished by Newton on the same scaled recurrence.  Log-weights come
    from the closed form w_i = Gamma(N+a+1) s_i / (N! (N+1)^2 L_{N+1}^{(a)}(s_i)^2),
    evaluated entirely in logs.

REFERENCES INTO THE PAPER (v2, pdf md5 ff7a34b776bfe5edf97397e5eabdbb7a)
-----------------------------------------------------------------------------
  Corollary 9      radial eigenbasis, L psi_n = (d/2 + n) psi_n
  eq. (12), (15)   Poincare inequality and the compactness estimate
  Lemma 16         ||.||_{H^2(mu)} := ||L .||_{L^2(mu)} induces the H^2(mu) topology
  Corollary 21     the radii polynomials P and Q, for T polynomial of degree p
  section 6        eq. (53)-(56), the bounds Y, Z11, Z21, Z12, Z22, Z2, Z3
  Remark 40        "terms like (u.grad)u could in principle also be handled in d in {2,3}"
  Remark 41        the L^infty bounds on psi_m and d_x psi_m
  Theorem 42       the result reproduced: ||u* - ubar||_{H^2(mu)} <= 1e-3 at n = 1500
"""

import math

import numpy as np

# ---------------------------------------------------------------------------
# Breden-Chu's published constants for Theorem 42, at their n = 1500.
# Transcribed from the proof of Theorem 42, arXiv:2404.04054v2 p. 31.
# ---------------------------------------------------------------------------
BC_THEOREM_42 = {
    "arxiv": "2404.04054v2",
    "pdf_md5": "ff7a34b776bfe5edf97397e5eabdbb7a",
    "code_repo": "github.com/Huggzz/Hermite-Laguerre_proofs",
    "code_commit": "7acaac71c84147d745cc959fbd97b548dc12372c",
    "n": 1500,
    "Y_published": 0.00075636391,
    "Z1_published": 0.065135932,
    "Z2_published": 343.3917,
    "Z3_published": 556.478,
    "deltabar_published": 0.00271646316,
    "enclosure_published": 1e-3,
    # Back-solved from the two published constants -- see writeup/novelty/leg_256.md
    # section 8.  These are NOT printed by the paper; they are what the printed Z2, Z3
    # imply, and they give two further independently-comparable quantities.
    "op_norm_LAL_implied": 556.478 / 96.0,
    "sup_combination_implied": 343.3917 / (2.0 ** 3.75 * (556.478 / 96.0)),
}


# ===========================================================================
# 1.  THE SPACE:  L = -Delta - (x/2).grad  on H^2(mu),  d = 1, even (Neumann)
# ===========================================================================
#
# Basis (Corollary 9 at d = 1, alpha = -1/2, restated in section 6 as the "even
# half-Hermite series"):
#
#     psi_m(x) = L_m^{(-1/2)}(y) e^{-y} / Zeta_m,        y = x^2 / 4,
#
# orthonormal for <u,v> = Int_R u v mu dx = Int_0^inf u v e^{x^2/4} dx (d = 1 gives
# Z = 2^{d-1} omega_{d-1} = 2, and every element is evenly extended), with
#
#     Zeta_m^2 = Gamma(m + 1/2) / m!,
#
# and  L psi_m = lambda_m psi_m  with  lambda_m = d/2 + m = 1/2 + m.
#
# Their `proof.ipynb` cell 4 uses exactly this: 'Lfrak = Diagonal(0:n .+ 1/2)' and
# 'lambda_m = 1/2 + n + 1' for the first DISCARDED eigenvalue.


def log_zeta(n):
    """log Zeta_m for m = 0..n, where Zeta_m^2 = Gamma(m+1/2)/m! normalises psi_m."""
    return 0.5 * np.array([math.lgamma(m + 0.5) - math.lgamma(m + 1.0)
                           for m in range(n + 1)])


def eigenvalues(n):
    """lambda_m = 1/2 + m, m = 0..n -- the diagonal of L in this basis."""
    return 0.5 + np.arange(n + 1, dtype=float)


def lambda_next(n):
    """lambda_{n+1} = n + 3/2: the first eigenvalue P_n discards.

    This is the constant their code calls `lambda_m` and the paper writes
    lambda_{n+1}; it is what the compactness estimate (15) is applied with.
    """
    return n + 1.5


def psi_at_zero(n):
    """psi_m(0) = sqrt( (2m-1)!! / (2^m m!) / sqrt(pi) ), m = 0..n.

    Since L_m^{(-1/2)}(0) = Gamma(m+1/2)/(Gamma(1/2) m!), this is
    L_m^{(-1/2)}(0)/Zeta_m; computed in logs.  Their cell 15.
    """
    lg = np.array([math.lgamma(m + 0.5) - math.lgamma(0.5) - math.lgamma(m + 1.0)
                   for m in range(n + 1)])
    return np.exp(lg - log_zeta(n))


def sup_psi_bounds(n):
    """Breden-Chu's own L^infty bounds on psi_m and d_x psi_m (their cells 16, 17).

    Implemented exactly as their code has them, NOT as the sharper Remark 41 bound
    ||psi_m||_inf <= pi^{-1/4}:

        sup psi_m  <=  (2^{2m+1} - C(2m,m)) m! / 2^m / sqrt((2m)!) / pi^{1/4}
        sup psi_m' <=  sqrt((2m+1)(2m+1)! / 4^m) / m! * e^{-1/2} / pi^{1/4}

    These are the numbers their Z2 is built from, so a reproduction must use them.
    `sharp_sup_psi` below computes the true sup numerically, so the looseness can be
    measured rather than argued.
    """
    m = np.arange(n + 1)
    lg = np.vectorize(math.lgamma, otypes=[float])
    # log C(2m,m) = lgamma(2m+1) - 2 lgamma(m+1)
    log_c = lg(2 * m + 1.0) - 2.0 * lg(m + 1.0)
    a = (2.0 * m + 1.0) * math.log(2.0)
    # log(2^{2m+1} - C(2m,m)) = a + log1p(-exp(log_c - a));  C/2^{2m+1} ~ 1/(2 sqrt(pi m)) < 1
    log_head = a + np.log1p(-np.exp(log_c - a))
    log_sup = (log_head + lg(m + 1.0) - m * math.log(2.0)
               - 0.5 * lg(2.0 * m + 1.0) - 0.25 * math.log(math.pi))
    log_dsup = (0.5 * (np.log(2.0 * m + 1.0) + lg(2.0 * m + 2.0) - 2.0 * m * math.log(2.0))
                - lg(m + 1.0) - 0.5 - 0.25 * math.log(math.pi))
    return np.exp(log_sup), np.exp(log_dsup)


def tail_constant_S(n):
    """S_n = ( pi log 4 - sum_{m=0}^n (2m-1)!!/((m+1/2)^2 m! 2^m) ) / sqrt(pi).

    The constant controlling h_inf(0)^2 <= ||h_inf||^2_{H^2(mu)} S_n in their
    derivation of Zbar12 (paper p. 30, their cell 20).  Computed in logs, summed in
    ascending order.
    """
    m = np.arange(n + 1)
    lg = np.vectorize(math.lgamma, otypes=[float])
    # (2m-1)!! / (2^m m!) = Gamma(m+1/2)/(Gamma(1/2) m!)
    log_t = (lg(m + 0.5) - math.lgamma(0.5) - lg(m + 1.0)
             - 2.0 * np.log(m + 0.5))
    return float((math.pi * math.log(4.0) - np.sum(np.exp(log_t)[::-1]))
                 / math.sqrt(math.pi))


# ===========================================================================
# 2.  GAUSS-LAGUERRE, WITHOUT SCIPY:  nodes by Sturm bisection, weights in logs
# ===========================================================================


def _laguerre_pair_scaled(N, alpha, x):
    """(L_{N-1}^{(a)}, L_N^{(a)}) at x, each divided by a common per-point scale.

    Returns (p_prev, p_cur, log_scale) with max(|p_prev|,|p_cur|) == 1 pointwise, so
    the true values are p * exp(log_scale).  Ratios (which is all Newton needs) are
    scale-free.
    """
    x = np.asarray(x, dtype=float)
    p_prev = np.ones_like(x)
    p_cur = 1.0 + alpha - x
    sc = np.zeros_like(x)
    for k in range(1, N):
        p_next = (((2 * k + 1 + alpha) - x) * p_cur - (k + alpha) * p_prev) / (k + 1.0)
        p_prev, p_cur = p_cur, p_next
        r = np.maximum(np.abs(p_prev), np.abs(p_cur))
        r = np.where(r > 0.0, r, 1.0)
        p_prev = p_prev / r
        p_cur = p_cur / r
        sc = sc + np.log(r)
    return p_prev, p_cur, sc


def _sturm_count(diag, offd2, x):
    """#{eigenvalues of the Jacobi matrix < x}, vectorised over x.

    LDL^T recurrence d_1 = a_1 - x, d_k = (a_k - x) - b_k^2/d_{k-1}; the number of
    negative pivots is the number of eigenvalues below x (Sylvester's law of inertia).
    """
    x = np.asarray(x, dtype=float)
    tiny = np.finfo(float).tiny
    d = diag[0] - x
    cnt = (d < 0.0).astype(np.int64)
    for k in range(1, len(diag)):
        d = np.where(np.abs(d) < tiny, np.sign(d) * tiny + tiny, d)
        d = (diag[k] - x) - offd2[k - 1] / d
        cnt += (d < 0.0)
    return cnt


def gauss_laguerre(N, alpha, newton_steps=3):
    """Gauss-Laguerre nodes and LOG-weights for Int_0^inf f(s) e^{-s} s^alpha ds.

    Nodes: eigenvalues of the Jacobi matrix (diag 2k+alpha+1, offdiag sqrt(k(k+alpha)))
    located by Sturm bisection -- each root's index is fixed by the Sturm count, so no
    root can be missed or doubled -- then polished by Newton on the scaled recurrence.

    Weights, in logs (they underflow catastrophically as doubles for large N):
        log w_i = lgamma(N+alpha+1) - lgamma(N+1) + log s_i
                  - 2 log(N+1) - 2 log|L_{N+1}^{(alpha)}(s_i)|.

    Returns (nodes, log_weights), both length N, nodes strictly increasing.
    """
    k = np.arange(N, dtype=float)
    diag = 2.0 * k + alpha + 1.0
    offd2 = (k[1:] * (k[1:] + alpha))          # b_k^2, length N-1
    lo = np.zeros(N)
    hi = np.full(N, 4.0 * N + 2.0 * alpha + 2.0)
    target = np.arange(1, N + 1)               # want #(< x) == i for the i-th root
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        c = _sturm_count(diag, offd2, mid)
        below = c < target
        lo = np.where(below, mid, lo)
        hi = np.where(below, hi, mid)
    x = 0.5 * (lo + hi)

    for _ in range(newton_steps):
        p_prev, p_cur, _ = _laguerre_pair_scaled(N, alpha, x)
        # d/dx L_N^{(a)} = (N L_N^{(a)} - (N+a) L_{N-1}^{(a)}) / x
        denom = N * p_cur - (N + alpha) * p_prev
        step = np.where(np.abs(denom) > 0.0, x * p_cur / denom, 0.0)
        x = x - step

    # log|L_{N+1}^{(alpha)}(x_i)| via one more recurrence step
    p_prev, p_cur, sc = _laguerre_pair_scaled(N + 1, alpha, x)
    log_abs_L = np.log(np.abs(p_cur)) + sc
    log_w = (math.lgamma(N + alpha + 1.0) - math.lgamma(N + 1.0) + np.log(x)
             - 2.0 * math.log(N + 1.0) - 2.0 * log_abs_L)
    return x, log_w


# ===========================================================================
# 3.  THE PRODUCT QUADRATURE RULES  (their quadrature.jl, in log space)
# ===========================================================================
#
# psi_m(x) = L_m(y) e^{-y} / Zeta_m and d_x psi_m(x) = (x/2) D_m(y) e^{-y} / Zeta_m
# with D_m(y) = -( L_{m-1}^{(1/2)}(y) + L_m^{(-1/2)}(y) ), y = x^2/4.
#
# A product of  (K - j) factors psi  and  j factors d_x psi , integrated against the
# weight e^{x^2/4}, is EXACTLY a Gauss-Laguerre integral: the Gaussians collapse to
# e^{-(K-1)y}, the j copies of (x/2) supply y^{j/2}, and dx = dy/sqrt(y) supplies
# y^{-1/2}, leaving
#
#     Int_0^inf (...) e^{x^2/4} dx = c^{-1} Int_0^inf P(s/c) e^{-s} s^{(j-1)/2} ds,
#     c = K - 1,    alpha = (j - 1)/2,
#
# with P polynomial of degree <= K n.  Their three instantiations:
#
#   K=6, j=2 -> c=5, alpha= 1/2, N=3n+3   (psi^4 psi'^2 : the Y and Zbar21/Zbar12 tails)
#   K=4, j=1 -> c=3, alpha= 0,   N=2n+3   (psi^3 psi'   : F, DF, the Gram matrices)
#   K=2, j=0 -> c=1, alpha=-1/2, N=n+1    (psi  psi     : the orthonormality gate)
#
# and the matrices are built so that a plain elementwise product of K columns, summed
# down the rows, IS the integral -- exactly as their `V6`/`DV6`/`V4`/`DV4` do.


class ProductRule:
    """One (V, DV) pair: the K-factor Gauss-Laguerre rule for the half-Hermite basis.

    `V[i, m]` and `DV[i, m]` are psi_m and d_xpsi_m at node i, each pre-multiplied by
    the K-th root of the node's quadrature weight, so that

        sum_i V[i,a] V[i,b] ... DV[i,e] ...   ==   Int (psi_a psi_b ... d_xpsi_e ...)
                                                     e^{x^2/4} dx

    for any K factors of which exactly `n_deriv` are derivatives.
    """

    def __init__(self, n, K, n_deriv, N=None):
        self.n, self.K, self.n_deriv = n, K, n_deriv
        c = float(K - 1)
        alpha = 0.5 * (n_deriv - 1.0)
        if N is None:
            # 2N - 1 >= K n  (exactness for the degree-(K n) polynomial)
            N = int(math.ceil((K * n + 1) / 2.0)) + 2
        self.N, self.c, self.alpha = N, c, alpha
        s, log_w = gauss_laguerre(N, alpha)
        self.nodes_s = s
        self.log_w = log_w
        y = s / c
        self.y = y
        self.x = 2.0 * np.sqrt(y)
        # per-node share of the weight: (w_i c^{-(alpha+1)})^{1/K}, in logs.
        # The exponent is (alpha+1), not 1: substituting s = c y in
        #   Int P(y) e^{-cy} y^alpha dy  =  c^{-(alpha+1)} Int P(s/c) e^{-s} s^alpha ds
        # carries y^alpha through as well as dy.  Getting this wrong costs exactly a
        # factor c^alpha, which for the six-product rule is sqrt(5) -- and is precisely
        # what `check_quadrature_identities` catches (their 669/31250 test).
        log_share = (log_w - (alpha + 1.0) * math.log(c)) / K
        self.V, self.DV = self._build(y, log_share)

    def _build(self, y, log_share):
        n = self.n
        lz = log_zeta(n)
        M = len(y)
        V = np.empty((M, n + 1))
        DV = np.empty((M, n + 1))
        # A = L^{(-1/2)} family, B = L^{(1/2)} family, each with a running log scale
        A_prev = np.ones(M)
        A_cur = 0.5 - y                       # L_1^{(-1/2)} = 1 + alpha - y
        sA = np.zeros(M)
        B_prev = np.ones(M)
        B_cur = 1.5 - y                       # L_1^{(1/2)}
        sB = np.zeros(M)
        # m = 0:  V = L_0/Zeta_0,  DV = -(L_0^{(-1/2)})/Zeta_0  (no L_{-1}^{(1/2)} term)
        V[:, 0] = np.exp(log_share - lz[0])
        DV[:, 0] = -V[:, 0]
        for m in range(1, n + 1):
            # A_cur is L_m^{(-1/2)} * e^{-sA};  B_prev is L_{m-1}^{(1/2)} * e^{-sB}
            base = log_share - lz[m]
            V[:, m] = A_cur * np.exp(sA + base)
            s = np.maximum(sA, sB)
            t = -(B_prev * np.exp(sB - s) + A_cur * np.exp(sA - s))
            DV[:, m] = t * np.exp(s + base)
            if m == n:
                break
            A_prev, A_cur = A_cur, (((2 * m + 0.5) - y) * A_cur
                                    - (m - 0.5) * A_prev) / (m + 1.0)
            r = np.maximum(np.abs(A_prev), np.abs(A_cur))
            r = np.where(r > 0.0, r, 1.0)
            A_prev, A_cur, sA = A_prev / r, A_cur / r, sA + np.log(r)
            B_prev, B_cur = B_cur, (((2 * m + 1.5) - y) * B_cur
                                    - (m + 0.5) * B_prev) / (m + 1.0)
            r = np.maximum(np.abs(B_prev), np.abs(B_cur))
            r = np.where(r > 0.0, r, 1.0)
            B_prev, B_cur, sB = B_prev / r, B_cur / r, sB + np.log(r)
        return V, DV


def make_rules(n):
    """The three rules Theorem 42's bounds need, at truncation n.

    N is set to Breden-Chu's own choices (their quadrature.jl: N = 3n+3 for the
    six-product, N = 2n+3 for the four-product) so the comparison is at their
    discretisation, not merely at their n.
    """
    return {
        "six": ProductRule(n, K=6, n_deriv=2, N=3 * n + 3),
        "four": ProductRule(n, K=4, n_deriv=1, N=2 * n + 3),
        "two": ProductRule(n, K=2, n_deriv=0, N=n + 1),
    }


# ---------------------------------------------------------------------------
# The three accuracy gates.  These are what license quoting a float64 number.
# ---------------------------------------------------------------------------


def check_weight_normalisation(rule):
    """sum_i w_i should equal Gamma(alpha+1).  Returns the relative error."""
    got = float(np.sum(np.exp(rule.log_w)))
    want = math.gamma(rule.alpha + 1.0)
    return {"sum_w": got, "gamma_alpha_plus_1": want,
            "rel_err": abs(got / want - 1.0)}


def check_quadrature_identities(rules):
    """Breden-Chu's own two exact rational integrals (their quadrature.jl tests).

        sqrt(5) pi Int_0^inf psi_1^4 psi_1'^2 e^{-r^2/4} dr = 669/31250
        pi        Int_0^inf psi_1^3 psi_1'   e^{-r^2/4} dr = -29/324

    Note their integrals carry e^{-r^2/4}, i.e. they are stated for the RAW Laguerre
    factors L/Zeta rather than for psi; that is exactly what the V columns hold, so
    the sums below are their sums.
    """
    V6, DV6 = rules["six"].V, rules["six"].DV
    V4, DV4 = rules["four"].V, rules["four"].DV
    six = float(np.sum(V6[:, 1] ** 4 * DV6[:, 1] ** 2) * math.pi * math.sqrt(5.0))
    four = float(np.sum(V4[:, 1] ** 3 * DV4[:, 1]) * math.pi)
    return {
        "six_product": six, "six_product_exact": 669.0 / 31250.0,
        "six_product_rel_err": abs(six / (669.0 / 31250.0) - 1.0),
        "four_product": four, "four_product_exact": -29.0 / 324.0,
        "four_product_rel_err": abs(four / (-29.0 / 324.0) - 1.0),
    }


def check_orthonormality(rules):
    """<psi_a, psi_b> = delta_ab for ALL a, b <= n, via the two-product rule.

    The all-mode version of the identity test: it is the gate that would catch a
    cancellation loss at high m, which the m = 1 identities cannot see.
    """
    V2 = rules["two"].V
    G = V2.T @ V2
    off = G - np.eye(G.shape[0])
    return {
        "n": G.shape[0] - 1,
        "max_abs_offdiag_and_diag_defect": float(np.max(np.abs(off))),
        "max_abs_diag_defect": float(np.max(np.abs(np.diag(off)))),
        "frobenius_defect": float(np.linalg.norm(off)),
    }


def psi_values(n, x):
    """psi_m(x) and d_x psi_m(x) for m = 0..n, as arrays of shape (len(x), n+1).

    Allocates (len(x), n+1) doubles, so this is for SMALL n (tests, plotting).  The
    heavy paths stream the same recurrence a column at a time instead.
    """
    x = np.asarray(x, dtype=float)
    y = x * x / 4.0
    lz = log_zeta(n)
    P = np.empty((len(x), n + 1))
    D = np.empty((len(x), n + 1))
    A_prev = np.ones_like(x)
    A_cur = 0.5 - y
    sA = np.zeros_like(x)
    B_prev = np.ones_like(x)
    B_cur = 1.5 - y
    sB = np.zeros_like(x)
    P[:, 0] = np.exp(-y - lz[0])
    D[:, 0] = -(x / 2.0) * P[:, 0]
    for m in range(1, n + 1):
        base = -y - lz[m]
        P[:, m] = A_cur * np.exp(sA + base)
        s = np.maximum(sA, sB)
        t = -(B_prev * np.exp(sB - s) + A_cur * np.exp(sA - s))
        D[:, m] = (x / 2.0) * t * np.exp(s + base)
        if m == n:
            break
        A_prev, A_cur = A_cur, (((2 * m + 0.5) - y) * A_cur
                                - (m - 0.5) * A_prev) / (m + 1.0)
        r = np.maximum(np.abs(A_prev), np.abs(A_cur))
        r = np.where(r > 0.0, r, 1.0)
        A_prev, A_cur, sA = A_prev / r, A_cur / r, sA + np.log(r)
        B_prev, B_cur = B_cur, (((2 * m + 1.5) - y) * B_cur
                                - (m + 0.5) * B_prev) / (m + 1.0)
        r = np.maximum(np.abs(B_prev), np.abs(B_cur))
        r = np.where(r > 0.0, r, 1.0)
        B_prev, B_cur, sB = B_prev / r, B_cur / r, sB + np.log(r)
    return P, D


def sharp_sup_psi(n, n_x=20001, x_max=200.0):
    """||psi_m||_inf and ||d_x psi_m||_inf, evaluated on a grid.

    Not a bound -- a measurement, so that the looseness of Breden-Chu's own
    analytic sup bounds (which is what their Z2 and Z3 are built from) can be
    reported as a magnitude instead of asserted.
    """
    x = np.linspace(0.0, x_max, n_x)
    y = x * x / 4.0
    lz = log_zeta(n)
    sup = np.empty(n + 1)
    dsup = np.empty(n + 1)
    A_prev = np.ones_like(x)
    A_cur = 0.5 - y
    sA = np.zeros_like(x)
    B_prev = np.ones_like(x)
    B_cur = 1.5 - y
    sB = np.zeros_like(x)
    base0 = -y - lz[0]
    sup[0] = float(np.max(np.abs(np.exp(base0))))
    dsup[0] = float(np.max(np.abs((x / 2.0) * np.exp(base0))))
    for m in range(1, n + 1):
        base = -y - lz[m]
        psi = A_cur * np.exp(sA + base)
        s = np.maximum(sA, sB)
        t = -(B_prev * np.exp(sB - s) + A_cur * np.exp(sA - s))
        dpsi = (x / 2.0) * t * np.exp(s + base)
        sup[m] = float(np.max(np.abs(psi)))
        dsup[m] = float(np.max(np.abs(dpsi)))
        if m == n:
            break
        A_prev, A_cur = A_cur, (((2 * m + 0.5) - y) * A_cur
                                - (m - 0.5) * A_prev) / (m + 1.0)
        r = np.maximum(np.abs(A_prev), np.abs(A_cur))
        r = np.where(r > 0.0, r, 1.0)
        A_prev, A_cur, sA = A_prev / r, A_cur / r, sA + np.log(r)
        B_prev, B_cur = B_cur, (((2 * m + 1.5) - y) * B_cur
                                - (m + 0.5) * B_prev) / (m + 1.0)
        r = np.maximum(np.abs(B_prev), np.abs(B_cur))
        r = np.where(r > 0.0, r, 1.0)
        B_prev, B_cur, sB = B_prev / r, B_cur / r, sB + np.log(r)
    return sup, dsup


# ===========================================================================
# 4.  THE PROBLEM:  L u - u/4 + u^2 d_x u = 0  on R+, Neumann at 0   [their (54)]
# ===========================================================================


class BurgersSelfSimilar:
    """Breden-Chu eq. (54): the self-similar profile of d_t v + v^2 d_x v = d_xx v.

    F(u) = u + L^{-1}( -u/4 + u^2 d_x u )   [their (55)], on H = span{psi_m}.

    Everything is in the coefficient vector a with u = sum_m a_m psi_m.
    """

    def __init__(self, n, rules=None):
        self.n = n
        self.rules = rules if rules is not None else make_rules(n)
        self.lam = eigenvalues(n)

    # -- the nonlinearity, projected: P_n( u^2 d_x u ) ----------------------
    def nonlinear_coeffs(self, a):
        V4, DV4 = self.rules["four"].V, self.rules["four"].DV
        u = V4 @ a
        du = DV4 @ a
        return V4.T @ (u * u * du)

    def F(self, a):
        return a + (-a / 4.0 + self.nonlinear_coeffs(a)) / self.lam

    def DF(self, a):
        """P_n DF(ubar) P_n = I - L^{-1}/4 + L^{-1}(2G + DG)   [their cell 9]."""
        V4, DV4 = self.rules["four"].V, self.rules["four"].DV
        u = V4 @ a
        du = DV4 @ a
        G = V4.T @ ((u * du)[:, None] * V4)        # d/du of u^2 d_xu : the 2 u d_xu part
        DG = V4.T @ ((u * u)[:, None] * DV4)       # the u^2 d_x part
        M = np.eye(self.n + 1) - np.diag(1.0 / (4.0 * self.lam))
        M += (2.0 * G + DG) / self.lam[:, None]
        return M, G, DG

    def newton(self, a0, tol=1e-14, max_iter=40):
        a = np.array(a0, dtype=float)
        hist = []
        for _ in range(max_iter):
            r = self.F(a)
            rn = float(np.linalg.norm(self.lam * r))     # the H^2(mu) norm of F(a)
            hist.append(rn)
            if rn < tol:
                break
            M, _, _ = self.DF(a)
            a = a - np.linalg.solve(M, r)
        return a, hist


# ---------------------------------------------------------------------------
# An INDEPENDENT approximate solution: shoot the ODE, project onto the basis.
# This is what makes the reproduction independent rather than a re-run of their
# stored `ubar` -- the seed never touches their data.
# ---------------------------------------------------------------------------


def _ode_rhs(x, u, v):
    return v, -(x / 2.0) * v - u / 4.0 + u * u * v


def shoot_profile(a0, x_max=12.0, h=1e-4):
    """RK4 for u'' + (x/2)u' + u/4 - u^2 u' = 0, u(0) = a0, u'(0) = 0.

    Returns (x grid, u).  Eq. (54) written as an ODE: L u = -u'' - (x/2)u'.
    Scalar inner loop on purpose -- numpy on 2-vectors is pure call overhead here.
    """
    N = int(round(x_max / h))
    xs = np.empty(N + 1)
    us = np.empty(N + 1)
    u, v, x = a0, 0.0, 0.0
    xs[0], us[0] = 0.0, a0
    h2, h6 = h / 2.0, h / 6.0
    for i in range(1, N + 1):
        k1u, k1v = _ode_rhs(x, u, v)
        k2u, k2v = _ode_rhs(x + h2, u + h2 * k1u, v + h2 * k1v)
        k3u, k3v = _ode_rhs(x + h2, u + h2 * k2u, v + h2 * k2v)
        k4u, k4v = _ode_rhs(x + h, u + h * k3u, v + h * k3v)
        u = u + h6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        v = v + h6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        x += h
        xs[i], us[i] = x, u
        if not (abs(u) < 1e8):
            return xs[:i + 1], us[:i + 1]
    return xs, us


def find_amplitude(lo=1.0, hi=1.3, x_test=9.0, iters=52):
    """Bisect on u(0) for the H^2(mu) branch of eq. (54).

    The generic solution of the ODE decays only like x^{-1/2} (not in H^2(mu)); the
    admissible one decays like e^{-x^2/4}.  u(x_test) changes sign across the
    admissible amplitude, so plain bisection isolates it.  Fully independent of
    Breden-Chu's stored coefficients.
    """
    def endpoint(a):
        xs, us = shoot_profile(a, x_max=x_test, h=2e-4)
        return us[-1] if len(us) and np.isfinite(us[-1]) else np.inf
    f_lo = endpoint(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        f_mid = endpoint(mid)
        if not np.isfinite(f_mid):
            hi = mid
            continue
        if np.sign(f_mid) == np.sign(f_lo):
            lo, f_lo = mid, f_mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return 0.5 * (lo + hi)


def project_profile(xs, us, n):
    """Coefficients a_m = <u, psi_m> of a profile given on a grid.

    <u, psi_m> = Int_0^inf u psi_m e^{x^2/4} dx = Int_0^inf u(x) L_m(x^2/4)/Zeta_m dx
    -- the exponentials cancel exactly, so this is a plain (Simpson) integral in x of
    a decaying integrand, with no weight to underflow.
    """
    y = xs * xs / 4.0
    lz = log_zeta(n)
    out = np.empty(n + 1)
    A_prev = np.ones_like(xs)
    A_cur = 0.5 - y
    sA = np.zeros_like(xs)

    def simpson(f):
        h = xs[1] - xs[0]
        k = len(f) - ((len(f) - 1) % 2) - 1        # largest even count of intervals
        w = np.ones(k + 1)
        w[1:k:2] = 4.0
        w[2:k:2] = 2.0
        return float(h / 3.0 * np.dot(w, f[:k + 1]))

    out[0] = simpson(us * np.exp(-lz[0]))
    for m in range(1, n + 1):
        out[m] = simpson(us * A_cur * np.exp(sA - lz[m]))
        if m == n:
            break
        A_prev, A_cur = A_cur, (((2 * m + 0.5) - y) * A_cur
                                - (m - 0.5) * A_prev) / (m + 1.0)
        r = np.maximum(np.abs(A_prev), np.abs(A_cur))
        r = np.where(r > 0.0, r, 1.0)
        A_prev, A_cur, sA = A_prev / r, A_cur / r, sA + np.log(r)
    return out


# ===========================================================================
# 5.  THE BOUNDS OF SECTION 6, and the radii polynomial of Corollary 21
# ===========================================================================


def op_norm(A):
    """sqrt(||A||_1 ||A||_inf) >= ||A||_2 -- Breden-Chu's own operator-norm bound.

    Their `op_norm` (cell 5).  It is what their Zbar11, Z2 and Z3 are built from, so a
    reproduction must use the same (loose) bound and not the true spectral norm.
    """
    return math.sqrt(float(np.max(np.sum(np.abs(A), axis=0)))
                     * float(np.max(np.sum(np.abs(A), axis=1))))


def bounds(problem, a, sup_psi=None, sup_dpsi=None):
    """Y, Zbar11, Zbar21, Zbar12, Zbar22, Z1, Z2, Z3 for eq. (54) at ubar = a.

    Every formula is Breden-Chu's, section 6 pp. 29-31, cross-read against their
    `Burger/proof.ipynb` cells 7-32.  Returns a dict of magnitudes.
    """
    n = problem.n
    lam = problem.lam
    lam_next = lambda_next(n)
    V4, DV4 = problem.rules["four"].V, problem.rules["four"].DV
    V6, DV6 = problem.rules["six"].V, problem.rules["six"].DV
    if sup_psi is None or sup_dpsi is None:
        sup_psi, sup_dpsi = sup_psi_bounds(n)

    u4, du4 = V4 @ a, DV4 @ a
    u6, du6 = V6 @ a, DV6 @ a

    # -- the finite-dimensional pieces --------------------------------------
    PF = problem.F(a)                                  # P_n F(ubar)
    M, G, DG = problem.DF(a)                           # P_n DF(ubar) P_n, and its parts
    An = np.linalg.inv(M)

    # -- Y  (their cell 12) --------------------------------------------------
    #    Y^2 = ||L An P_n F(ubar)||^2_{L^2}  +  ( ||ubar^2 d_xubar||^2 - ||P_n(.)||^2 )
    proj_nl = V4.T @ (u4 * u4 * du4)
    full_nl_sq = float(np.sum(u6 ** 4 * du6 ** 2))     # ||ubar^2 d_xubar||^2_{L^2(mu)}
    proj_nl_sq = float(np.dot(proj_nl, proj_nl))
    tail_sq = full_nl_sq - proj_nl_sq
    finite_sq = float(np.sum((lam * (An @ PF)) ** 2))
    Y = math.sqrt(max(finite_sq + tail_sq, 0.0))

    # -- Zbar11  (their cell 13) ---------------------------------------------
    Z11 = op_norm(lam[:, None] * (np.eye(n + 1) - An @ M) / lam[None, :])

    # -- Zbar21  (their cells 10, 11, 14) ------------------------------------
    #    w_m = 2||P_inf(ubar psi_m d_xubar)|| + ||P_inf(ubar^2 d_xpsi_m)||
    col = (u6 * du6)[:, None] * V6
    int_full = np.sum(col * col, axis=0)
    dcol = (u6 * u6)[:, None] * DV6
    dint_full = np.sum(dcol * dcol, axis=0)
    w = (2.0 * np.sqrt(np.maximum(int_full - np.sum(G * G, axis=0), 0.0))
         + np.sqrt(np.maximum(dint_full - np.sum(DG * DG, axis=0), 0.0)))
    Z21 = float(np.linalg.norm(w / lam))

    # -- Zbar12  (their cells 20-25) -----------------------------------------
    #    wtilde_m = ubar(0)^2 psi_m(0) sqrt(S_n)
    #               + ||P_inf( ubar^2 (d_xpsi_m + (x/2)psi_m) )|| / lambda_{n+1}
    S_n = tail_constant_S(n)
    psi0 = psi_at_zero(n)
    u0 = float(np.dot(a, psi0))
    dcol2 = (u6 * u6)[:, None] * (DV6 + V6)
    dint2 = np.sum(dcol2 * dcol2, axis=0)
    DG2 = V4.T @ ((u4 * u4)[:, None] * (V4 + DV4))
    wt = (u0 * u0 * math.sqrt(S_n) * psi0
          + np.sqrt(np.maximum(dint2 - np.sum(DG2 * DG2, axis=0), 0.0)) / lam_next)
    Z12 = float(np.linalg.norm(np.abs(lam[:, None] * An / lam[None, :]) @ wt))

    # -- Zbar22  (their cell 26) ---------------------------------------------
    sup_u = float(np.dot(np.abs(a), sup_psi))
    sup_du = float(np.dot(np.abs(a), sup_dpsi))
    Z22 = (0.25 + 2.0 * sup_u * sup_du) / lam_next + sup_u ** 2 / math.sqrt(lam_next)

    # -- Z1: the 2x2 spectral norm  (their cells 5, 27) ----------------------
    B = np.array([[Z11, Z12], [Z21, Z22]])
    Z1 = float(np.linalg.norm(B, 2))

    # -- Z2, Z3  (their cells 30-32) -----------------------------------------
    op_n = max(op_norm(lam[:, None] * An / lam[None, :]), 1.0)
    Z2 = 2.0 ** 3.75 * op_n * (math.sqrt(2.0) * sup_u + sup_du)
    Z3 = 96.0 * op_n

    return {
        "n": n, "Y": Y, "Z1": Z1, "Z2": Z2, "Z3": Z3,
        "Zbar11": Z11, "Zbar12": Z12, "Zbar21": Z21, "Zbar22": Z22,
        "op_norm_LAL": op_n,
        "sup_ubar": sup_u, "sup_dubar": sup_du,
        "sup_combination": math.sqrt(2.0) * sup_u + sup_du,
        "ubar_at_zero": u0, "S_n": S_n,
        "Y_finite_part": math.sqrt(max(finite_sq, 0.0)),
        "Y_tail_part": math.sqrt(max(tail_sq, 0.0)),
        "nonlinearity_norm": math.sqrt(max(full_nl_sq, 0.0)),
        "PF_H2_norm": float(np.linalg.norm(lam * PF)),
    }


def sup_bound_families(n):
    """The candidate L^infty bound families for psi_m and d_x psi_m, by name.

    Z1 and Z2 are the only Theorem-42 constants that depend on how ||psi_m||_inf and
    ||d_x psi_m||_inf are bounded, and arXiv:2404.04054v2 contains more than one answer:

      `code_cells_16_17`  what `Burger/proof.ipynb` cells 16 and 17 actually compute --
                          the released artifact, and what this leg's headline uses.
      `code_cell_15_commented`  cells 16 + the ALTERNATIVE d_xpsi bound that sits
                          commented out in cell 15 of the same released notebook.
      `remark_41`         the paper's own Remark 41: ||psi_m||_inf <= pi^{-1/4} and
                          ||d_xpsi_m||_inf <= pi^{-1/4}(sqrt(m) + e^{-1/2}).  This is
                          SHARPER than the code for psi and the code does not use it.
      `remark_41_psi_only` Remark 41's psi bound with the code's d_xpsi bound.
      `measured`          the true suprema, evaluated on a grid.  Not a bound -- the
                          yardstick the others are loose against.

    Returned as {name: (sup_psi, sup_dpsi)}.  Used to attribute any Z1/Z2 gap to a
    specific choice rather than to argue about it.
    """
    m = np.arange(n + 1, dtype=float)
    code_sup, code_dsup = sup_psi_bounds(n)
    q = math.pi ** -0.25
    meas_sup, meas_dsup = sharp_sup_psi(n)
    return {
        "code_cells_16_17": (code_sup, code_dsup),
        "code_cell_15_commented": (
            code_sup,
            code_sup * (1.0 + 2.0 * np.sqrt(1.0 - 0.5 / (m + 1.0)))
            / math.sqrt(2.0 * math.e)),
        "remark_41": (np.full(n + 1, q), q * (np.sqrt(m) + math.exp(-0.5))),
        "remark_41_psi_only": (np.full(n + 1, q), code_dsup),
        "measured": (meas_sup, meas_dsup),
    }


def recombine_with_sups(base, a, sup_psi, sup_dpsi, n):
    """Z22, Z1, Z2 under a different L^infty bound family, reusing `base`.

    Zbar11, Zbar12, Zbar21, Y and ||L A L^{-1}|| do not depend on the sup bounds, so
    swapping the family only needs the Zbar22/Z2 algebra redone -- no quadrature.
    """
    lam_next = lambda_next(n)
    sup_u = float(np.dot(np.abs(a), sup_psi))
    sup_du = float(np.dot(np.abs(a), sup_dpsi))
    Z22 = (0.25 + 2.0 * sup_u * sup_du) / lam_next + sup_u ** 2 / math.sqrt(lam_next)
    B = np.array([[base["Zbar11"], base["Zbar12"]], [base["Zbar21"], Z22]])
    Z1 = float(np.linalg.norm(B, 2))
    comb = math.sqrt(2.0) * sup_u + sup_du
    Z2 = 2.0 ** 3.75 * base["op_norm_LAL"] * comb
    return {"sup_ubar": sup_u, "sup_dubar": sup_du, "sup_combination": comb,
            "Zbar22": Z22, "Z1": Z1, "Z2": Z2, "Z3": base["Z3"], "Y": base["Y"]}


def radii_verdict(Y, Z1, Z2, Z3):
    """Corollary 21 with p = 3: P(d) = Y - d + Z1 d + Z2 d^2/2 + Z3 d^3/6.

    Returns delta_min (smallest positive root of P), delta_bar (positive root of Q),
    and whether the certificate closes.  Magnitudes, never a bare boolean.
    """
    out = {"Y": Y, "Z1": Z1, "Z2": Z2, "Z3": Z3, "Z1_lt_1": bool(Z1 < 1.0)}
    if Z3 > 0:
        disc = Z2 ** 2 + 2.0 * Z3 * (1.0 - Z1)
        out["delta_bar"] = (-Z2 + math.sqrt(disc)) / Z3 if disc >= 0 else float("nan")
    else:
        out["delta_bar"] = float("nan")
    roots = np.roots([Z3 / 6.0, Z2 / 2.0, -(1.0 - Z1), Y])
    real = np.sort([r.real for r in roots if abs(r.imag) < 1e-12 * max(1.0, abs(r))
                    and r.real > 0])
    out["positive_real_roots"] = [float(r) for r in real]
    out["closes"] = bool(Z1 < 1.0 and len(real) >= 1)
    out["delta_min"] = float(real[0]) if len(real) else float("nan")
    return out


def radii_polynomial(Y, Z1, Z2, Z3, d):
    """P(delta), for reporting the sign at a named radius."""
    return Z3 / 6.0 * d ** 3 + Z2 / 2.0 * d ** 2 - (1.0 - Z1) * d + Y
