#!/usr/bin/env python3
"""Route-H2C — the origin-`H^2` certificate at `a = 0`, CONSTRUCTED.

THE CEILING, BEFORE ANY CODE (DIRECTION.md sec 176, leg 163 census item O3)
--------------------------------------------------------------------------
Everything in this module is a consequence of `a = 0` EXACTNESS.  The
single-simple-pole identity, the Hardy block-diagonalization, the closed-form
resolvent and the exact Mellin norm all hold because `Omega(y) = -y/(y^2+1/4)`
is the exact CLM profile.  For `a > 0` Xu (arXiv:2607.19762) proves only a
conditional two-line inclusion under his hypothesis `Adm(a)`: no resolvent, no
invertibility, no gap.  `HL_S2_nonsymmetric` is not a CLM profile and inherits
NONE of it.

So a certificate built here certifies an object Xu ALREADY INVERTS IN CLOSED
FORM.  Nothing transfers to the real target.  No link of the `L1 -> L4` chain
moves.  No Clay movement.  This module is INFRASTRUCTURE and a worked example of
the non-`ell^1_w` lane -- it is not a theorem, and it is not progress on the
chain.  Float64 throughout; nothing interval-enclosed, nothing rigorous.

Xu records three gaps toward a computer-assisted proof (his sec 3.2, the
Evans-determinant strand): a uniform large-imaginary-part bound, trace-ideal
membership of the kernel, and quadrature-error bounds in the trace norm.  THIS
MODULE CLOSES NONE OF THE THREE.  It builds a static invertibility certificate
at `z = 0`, a different object in a different strand of the same paper.

THE OBJECT
----------
At `a = 0`, on the upper-half-plane Hardy space `H_+^2`, the Hilbert transform
acts as `-i` and Xu's single-simple-pole identity collapses the nonlocal
linearization to a scalar first-order operator (Xu eq. 4.21):

    L_0^+ = -1 - y d/dy + i/b ,        b(y) = y + i/2 .

`X = {phi odd : phi, phi'' in L^2(0,inf), phi(y) = a_1 y + o(y)}`, with
`||phi||_X^2 = ||phi||_{L^2}^2 + ||phi''||_{L^2}^2`.

THE REALIZATION THIS MODULE ADDS, AND WHY IT IS EXACT
-----------------------------------------------------
Write `phi(y) = int_0^inf phihat(xi) e^{i y xi} dxi` (`H_+^2 == L^2(0,inf)`).
Then `d/dy -> i xi` and `y -> i d/dxi`, so `y d/dy -> -1 - xi d/dxi` and

    -1 - y d/dy  ->  xi d/dxi                    (the MELLIN generator)

while `i/b(y)` has transform `e^{-xi/2}`, so multiplication by it becomes the
Volterra convolution `(V g)(xi) = int_0^xi e^{-(xi-eta)/2} g(eta) d eta`.  Hence
on the Fourier side

    L_0^+ = xi d/dxi + V ,       ||phi||_X^2 = 2 pi int_0^inf (1+xi^4)|phihat|^2 dxi.

In the LAGUERRE basis `l_n(xi) = L_n(xi) e^{-xi/2}` (orthonormal on `(0,inf)`)
BOTH pieces are exact and banded, by two classical identities (this module
claims neither -- see `writeup/novelty/leg_176.md`):

    int_0^x L_n = L_n - L_{n+1}          =>   V l_n = l_n - l_{n+1}
    xi L_n' = n(L_n - L_{n-1}),  xi L_n = (2n+1)L_n - (n+1)L_{n+1} - n L_{n-1}

Combining them, `L_0^+` is EXACTLY TRIDIAGONAL WITH RATIONAL ENTRIES:

    L_0^+ l_n = -(n/2) l_{n-1} + (1/2) l_n + ((n-1)/2) l_{n+1}

and Xu's two symmetry modes occupy EXACTLY `span{l_0, l_1}`:

    b^{-2}   <->  -(l_0 - l_1)          (eigenvalue 1, time-shift)
    m = y b^{-2} <-> -(i/2)(l_0 + l_1)  (eigenvalue 0, scaling; the border column)

The border row `ell(f) = i f(0) - f'(0)/4` (Xu's `G'(0)`, the only `z = 0` pole)
becomes, using `int_0^inf l_n = 2(-1)^n` and `int_0^inf xi l_n = 4(-1)^n(2n+1)`,

    ell_n = i (-1)^n (1 - 2n)

which satisfies `ell . L_0^+ = 0` EXACTLY (`ell` is the left null vector) and
`ell(m) = 1` EXACTLY.  Because `ell_n` grows linearly while `l_n`'s `X`-norm
grows like `n^2`, `ell` is a bounded functional on `X` but NOT on `l^2`; that
distinction is measured, not assumed, in `border_row_dual_norm`.

WHAT IS AND IS NOT CLAIMED
--------------------------
The two Laguerre identities above are classical.  What is this module's own is
their assembly into THIS operator's exact tridiagonal matrix, the observation
that modulating out the symmetry modes is literally truncating two coefficients,
and the measurement of a certificate diagnostic on the result.
"""

import numpy as np
from math import comb

# ---------------------------------------------------------------------------
# the exact discrete realization
# ---------------------------------------------------------------------------

def l0_plus(N):
    """`L_0^+` in the Laguerre basis: EXACTLY tridiagonal, rational entries.

    Column `n` is `-(n/2) l_{n-1} + (1/2) l_n + ((n-1)/2) l_{n+1}`.  Every entry
    is a half-integer, exactly representable in float64 for any `N` this project
    will use, so the matrix is exact data and not a discretization.
    """
    N = int(N)
    A = np.zeros((N, N))
    for n in range(N):
        if n - 1 >= 0:
            A[n - 1, n] = -n / 2.0
        A[n, n] = 0.5
        if n + 1 < N:
            A[n + 1, n] = (n - 1) / 2.0
    return A


def jacobi_xi(N):
    """Matrix of multiplication by `xi` in the Laguerre basis (symmetric, exact)."""
    N = int(N)
    J = np.zeros((N, N))
    for n in range(N):
        J[n, n] = 2 * n + 1
        if n + 1 < N:
            J[n + 1, n] = -(n + 1)
            J[n, n + 1] = -(n + 1)
    return J


def x_gram(N, pad=12):
    """Gram matrix of the `X` inner product: `G = I + J^4`, banded, exact.

    `<l_m, (1+xi^4) l_n>` is the `(m,n)` entry of `I + J^4` computed in the
    INFINITE basis; `J^4` has bandwidth 4, so forming it at size `N+pad` and
    truncating gives the exact `N x N` block (no truncation error at all for
    `pad >= 4`).  Padding is checked, not assumed, by `test_origin_h2_certificate`.
    """
    N, pad = int(N), max(int(pad), 4)
    J = jacobi_xi(N + pad)
    G = np.eye(N + pad) + np.linalg.matrix_power(J, 4)
    return G[:N, :N]


def _sym_sqrt(G):
    w, U = np.linalg.eigh(G)
    if w.min() <= 0.0:
        raise ValueError("X Gram matrix lost positive-definiteness")
    return (U * np.sqrt(w)) @ U.T, (U * (1.0 / np.sqrt(w))) @ U.T


def x_norm(c, G=None):
    """`||phi||_X` for Laguerre coefficients `c` (up to the common factor sqrt(2 pi)).

    NOTE, and it matters: this is `sqrt(c* G c)` with the FULL banded `G`, NOT
    `sqrt(sum w_n^2 |c_n|^2)`.  The diagonal `w_n = ||l_n||_X` grows like `8.4 n^2`
    while the exact solution's coefficients decay only like `C/n`, so the
    diagonal-only surrogate diverges where the true norm is finite.  The
    off-diagonal cancellation in `G` is the whole difference.
    """
    c = np.asarray(c)
    if G is None:
        G = x_gram(len(c))
    return float(np.sqrt(np.real(np.vdot(c, G @ c))))


def x_operator_norm(A, G=None):
    """`||A||_{X->X}` = largest singular value of `G^{1/2} A G^{-1/2}`."""
    A = np.asarray(A)
    if G is None:
        G = x_gram(A.shape[0])
    Gh, Ghi = _sym_sqrt(G)
    return float(np.linalg.svd(Gh @ A @ Ghi, compute_uv=False)[0])


def x_singular_values(A, G=None):
    A = np.asarray(A)
    if G is None:
        G = x_gram(A.shape[0])
    Gh, Ghi = _sym_sqrt(G)
    return np.linalg.svd(Gh @ A @ Ghi, compute_uv=False)


def symmetry_modes(N):
    """Xu's two symmetry modes, EXACTLY in `span{l_0, l_1}`.

    Returns `(b_inv2, m)`: `b^{-2}` (eigenvalue 1) and `m = y b^{-2}` (eigenvalue
    0, the border column).
    """
    N = int(N)
    b2 = np.zeros(N, dtype=complex); b2[0] = -1.0; b2[1] = 1.0
    m = np.zeros(N, dtype=complex);  m[0] = -0.5j; m[1] = -0.5j
    return b2, m


def border_row(N):
    """`ell(f) = i f(0) - f'(0)/4` in Laguerre coordinates: `ell_n = i(-1)^n(1-2n)`."""
    n = np.arange(int(N))
    return 1j * ((-1.0) ** n) * (1.0 - 2.0 * n)


def border_row_dual_norm(N, G=None):
    """`||ell||_{X*}` at truncation `N`.  Bounded in `X*`, unbounded in `l^2`.

    Returned as `(x_dual, l2)` so the contrast is a measurement, not a remark:
    `x_dual` converges, `l2` diverges like `N^{3/2}`.
    """
    e = border_row(N)
    if G is None:
        G = x_gram(N)
    Gi = np.linalg.inv(G)
    return float(np.sqrt(np.real(np.vdot(e, Gi @ e)))), float(np.linalg.norm(e))


def bordered_operator(N):
    """Leg 163's bordered formulation, `[[L_0^+, m], [ell, 0]]` on `X (+) C`."""
    N = int(N)
    B = np.zeros((N + 1, N + 1), dtype=complex)
    B[:N, :N] = l0_plus(N)
    B[:N, N] = symmetry_modes(N)[1]
    B[N, :N] = border_row(N)
    return B


def bordered_gram(N, G=None):
    """`X (+) C` Gram: the `X` block plus a unit weight on the border amplitude."""
    if G is None:
        G = x_gram(N)
    Gb = np.zeros((N + 1, N + 1))
    Gb[:N, :N] = G
    Gb[N, N] = 1.0
    return Gb


# ---------------------------------------------------------------------------
# y-space evaluation, and the map back and forth
# ---------------------------------------------------------------------------

def to_y(c, y, deriv=0):
    """`phi(y) = i sum_n c_n a^n / b^{n+1}`, `a = y - i/2`, `b = y + i/2`.

    Evaluated through the Blaschke factor `r = a/b` (`|r| = 1` on the real axis),
    so nothing overflows at large `|y|` however many modes are carried -- the
    naive `a**n / b**(n+1)` form overflows above `n ~ 200`.
    """
    c = np.asarray(c)
    y = np.atleast_1d(np.asarray(y, dtype=float)).astype(complex)
    a = y - 0.5j; b = y + 0.5j; r = a / b
    n = len(c)
    R = np.empty((n + 1, len(y)), dtype=complex)
    R[0] = 1.0
    for k in range(1, n + 1):
        R[k] = R[k - 1] * r
    out = np.zeros(len(y), dtype=complex)
    for k in range(n):
        ck = c[k]
        if ck == 0:
            continue
        if deriv == 0:
            T = R[k] / b
        elif deriv == 1:
            T = -R[k] / b ** 2
            if k:
                T = T + 1j * k * R[k - 1] / b ** 3
        elif deriv == 2:
            T = 2 * R[k] / b ** 3
            if k:
                T = T - 4j * k * R[k - 1] / b ** 4
            if k > 1:
                T = T - k * (k - 1) * R[k - 2] / b ** 5
        else:
            raise ValueError("deriv must be 0, 1 or 2")
        out = out + ck * T
    return 1j * out


def project_to_laguerre(u_of_y, M=8192):
    """Laguerre/Hardy coefficients of a function given by its values on `R`.

    Uses the Blaschke map `y = -cot(theta/2)/2`, under which
    `a^n/b^{n+1} = -2 sin(theta/2) e^{i(n+1/2)theta}`, so the coefficients are a
    plain Fourier transform of `u(y(theta)) csc(theta/2) e^{-i theta/2}`.  Exact
    to 1.8e-16 on a round trip (see the test module).
    """
    M = int(M)
    th = 2 * np.pi * (np.arange(M) + 0.5) / M
    y = -0.5 / np.tan(th / 2.0)
    v = u_of_y(y) / np.sin(th / 2.0) * np.exp(-0.5j * th)
    vhat = np.fft.fft(v) / M * np.exp(-1j * np.pi * np.arange(M) / M)
    return 0.5j * vhat


# ---------------------------------------------------------------------------
# Xu's closed form, eq. (4.23) at z = 0 -- the cross-check target
# ---------------------------------------------------------------------------

def _G_derivs(c, t):
    """`G = b^2 f` and its first two derivatives at complex `t`, in closed form."""
    t = np.asarray(t, dtype=complex)
    a = t - 0.5j; b = t + 0.5j
    G = np.zeros_like(t); G1 = np.zeros_like(t); G2 = np.zeros_like(t)
    for k in range(len(c)):
        ck = c[k]
        if ck == 0:
            continue
        G = G + ck * a ** k * b ** (1 - k)
        G1 = G1 + ck * (k * a ** (k - 1) * b ** (1 - k) + (1 - k) * a ** k * b ** (-k))
        G2 = G2 + ck * (k * (k - 1) * a ** (k - 2) * b ** (1 - k)
                        + 2 * k * (1 - k) * a ** (k - 1) * b ** (-k)
                        + (1 - k) * (-k) * a ** k * b ** (-k - 1))
    return 1j * G, 1j * G1, 1j * G2


def taylor_G(c, M=90):
    """EXACT Taylor coefficients of `G = b^2 f` about `t = 0` -- by algebra.

    `a = -(i/2)(1+2it)`, `b = (i/2)(1-2it)`, so
    `G(t) = -(1/2) sum_k c_k (-1)^k (1+2it)^k (1-2it)^{1-k}`; both factors have
    exact integer coefficient sequences, convolved here and rescaled by `(2i)^m`.

    THIS IS NOT A CONVENIENCE.  `G_2(t) = G(t) - G(0) - G'(0)t` is `O(t^2)` while
    `G(0)` is `O(1)`, and Xu's integrand multiplies the difference by `s^{-2}`.
    Forming `G_2` by literal subtraction is the floating-point defect leg 163
    caught and repaired (its worst case improved by 7.05e+22x); building `G_2`
    from its own Taylor coefficients means nothing is ever subtracted.  An FFT
    recovery of these coefficients is NOT good enough either -- `G`'s radius of
    convergence is 1/2, so the FFT's `rho^{-m}` amplification destroys them
    beyond `m ~ 26`.  Hence exact algebra.
    """
    M = int(M)
    g = np.zeros(M, dtype=complex)
    for k in range(len(c)):
        ck = c[k]
        if ck == 0:
            continue
        P = np.array([comb(k, j) for j in range(min(k, M - 1) + 1)], dtype=complex)
        if k == 0:
            Q = np.array([1.0, -1.0], dtype=complex)
        elif k == 1:
            Q = np.array([1.0], dtype=complex)
        else:
            Q = np.array([float(comb(j + k - 2, j)) for j in range(M)], dtype=complex)
        pr = np.convolve(P, Q)[:M]
        g[:len(pr)] += ck * ((-1) ** k) * pr
    return (-0.5 * g) * (2j) ** np.arange(M)


_TAY_R = 0.25      # |t| below which the exact Taylor series is used
_MSER = 80         # series truncation; (2*0.25)^80 = 8e-25, fully converged
_PAN_RATIO = 1.6   # max |t| ratio spanned by one Gauss panel (grid-independence)


def _taylor_cums(g, T):
    """The three cumulative integrals below `|T| <= _TAY_R`, term by term, exactly.

        A(T) = int_0^T G_2(t)/t^2 dt = sum_{m>=2} g_m T^{m-1}/(m-1)
        B(T) = int_0^T G'(t)/t   dt = sum_{m>=2} m g_m T^{m-1}/(m-1)
        C(T) = int_0^T G''(t)    dt = sum_{m>=2} m g_m T^{m-1}
    """
    m = np.arange(2, _MSER)
    gm = g[m]
    Tp = T ** (m - 1)
    return (np.sum(gm * Tp / (m - 1)),
            np.sum(m * gm * Tp / (m - 1)),
            np.sum(m * gm * Tp))


def _cum_branch(c, g, ys, kpan=24):
    """Cumulative `A, B, C` at each node of a monotone branch `ys` away from 0.

    Xu's three integrals are ALL cumulative in `t = ys`:

        I(y) = y A(y),      I'(y) = B(y),      I''(y) = C(y)/y

    so one sweep along the sorted nodes serves every `y` at once, instead of a
    fresh panel quadrature per point.  Below `|t| = 0.25` the exact Taylor sums
    are used (nothing subtracted); above it, Gauss panels.
    All three integrands are regular at `t = 0` because `G'(0) = ell(f) = 0`.

    EACH INTER-NODE INTERVAL IS SUBDIVIDED GEOMETRICALLY (`_PAN_RATIO` per
    sub-panel).  Without that the accuracy of the result would depend on how
    finely the CALLER happened to sample -- a sparse grid puts a single Gauss
    panel across `t = 0.25 .. 20`, where the integrand varies over two decades,
    and the residual degrades from 3e-15 to 2.5e-06.  The integrand has two
    regimes (`|t| < 1` and the `log`-spaced decades beyond), which is exactly the
    two-panel/log-grading defect leg 163 caught in the same family of integrals;
    grading here makes the answer a property of the operator and not of the
    caller's grid.
    """
    x, w = np.polynomial.legendre.leggauss(int(kpan))
    G0 = g[0]
    A = np.empty(len(ys), dtype=complex)
    B = np.empty(len(ys), dtype=complex)
    C = np.empty(len(ys), dtype=complex)
    sgn = 1.0 if ys[0] > 0 else -1.0
    T0 = sgn * _TAY_R
    acc = None
    for j, y in enumerate(ys):
        if abs(y) <= _TAY_R:
            A[j], B[j], C[j] = _taylor_cums(g, y)
            continue
        if acc is None:
            acc = list(_taylor_cums(g, T0))
            prev = T0
        nsub = max(1, int(np.ceil(np.log(abs(y) / abs(prev)) / np.log(_PAN_RATIO))))
        edges = sgn * np.exp(np.linspace(np.log(abs(prev)), np.log(abs(y)), nsub + 1))
        for lo, hi in zip(edges[:-1], edges[1:]):
            tt = 0.5 * (hi - lo) * x + 0.5 * (hi + lo)
            ww = 0.5 * (hi - lo) * w
            Gv, G1v, G2v = _G_derivs(c, tt)
            acc[0] += np.sum(ww * (Gv - G0) / tt ** 2)
            acc[1] += np.sum(ww * G1v / tt)
            acc[2] += np.sum(ww * G2v)
        prev = y
        A[j], B[j], C[j] = acc
    return A, B, C


def xu_resolvent(c, yv, c1=0.0, kpan=24, derivs=False):
    """Xu eq. (4.23) at `z = 0`, bordered: `u = -b^{-2}(I - G(0) + c_1 y)`.

    At `z = 0` Xu's `c_1 = G'(0)/z` is the ONLY singular object, and
    `G'(0) = ell(f)`; on `{ell(f) = 0}` the singularity is removable and `c_1`
    becomes the free amplitude along the kernel direction `m = y b^{-2}` -- which
    is exactly leg 163's border column.  `c_0 = G(0)/(z-1) = -G(0)` at `z = 0`.
    """
    g = taylor_G(c)
    G0 = g[0]
    yv = np.atleast_1d(np.asarray(yv, dtype=float))
    I = np.zeros(len(yv), dtype=complex)
    I1 = np.zeros(len(yv), dtype=complex)
    I2 = np.zeros(len(yv), dtype=complex)
    for mask, order in ((yv > 0, 1), (yv < 0, -1)):
        idx = np.where(mask)[0]
        if not len(idx):
            continue
        idx = idx[np.argsort(order * yv[idx])]      # outward from 0
        ys = yv[idx]
        A, B, C = _cum_branch(c, g, ys, kpan=kpan)
        I[idx] = ys * A
        I1[idx] = B
        I2[idx] = C / ys
    b = yv + 0.5j
    Phi = I - G0 + c1 * yv
    u = -Phi / b ** 2
    if not derivs:
        return u
    Phi1 = I1 + c1
    Phi2 = I2
    u1 = -Phi1 / b ** 2 + 2 * Phi / b ** 3
    u2 = -Phi2 / b ** 2 + 4 * Phi1 / b ** 3 - 6 * Phi / b ** 4
    return u, u1, u2


def xu_ode_residual(c, yv, **kw):
    """`(L_0^+ u - f)(y)` pointwise for Xu's closed form -- the realization-free check.

    `L_0^+ u = -u - y u' + i u / b`.  Every derivative analytic; no finite
    differences anywhere.  This is the quantity the gate's second conjunct asks
    about, and it does not reference the Laguerre realization at all.
    """
    yv = np.atleast_1d(np.asarray(yv, dtype=float))
    u, u1, _ = xu_resolvent(c, yv, derivs=True, **kw)
    b = yv + 0.5j
    return (-u - yv * u1 + 1j * u / b) - to_y(c, yv)


# ---------------------------------------------------------------------------
# X norms in y-space, by quadrature on the Blaschke circle
# ---------------------------------------------------------------------------

def _blaschke_nodes(M):
    th = 2 * np.pi * (np.arange(int(M)) + 0.5) / int(M)
    y = -0.5 / np.tan(th / 2.0)
    dy = 0.25 / np.sin(th / 2.0) ** 2 * (2 * np.pi / int(M))
    return y, dy


def x_norm_y(u_of_y, M=4096):
    """`||phi||_X = (int |phi|^2 + int |phi''|^2)^{1/2}` over the whole line.

    `u_of_y(y)` must return `(phi, phi'')`.  The substitution `y = -cot(th/2)/2`
    turns both integrals into smooth periodic ones -- the same trick the
    projection uses -- so a plain uniform rule is spectrally accurate.
    """
    y, dy = _blaschke_nodes(M)
    phi, phi2 = u_of_y(y)
    return float(np.sqrt(np.sum(dy * (np.abs(phi) ** 2 + np.abs(phi2) ** 2))))


def resolvent_ratio(c, M=4096, **kw):
    """`||u||_X / ||f||_X` for Xu's exact solution, normalized by `ell(u) = 0`.

    This is leg 163's G4 quantity -- the `X`-realization analogue of the ratio
    leg 127 drove to zero in `ell^1_w` -- but computed from the CLOSED FORM on
    the whole line rather than from a truncated matrix, so no finite section
    enters it.  The free amplitude `c_1` is fixed by `ell(u) = 0`, evaluated in
    y-space as `i u(0) - u'(0)/4`.
    """
    c = np.asarray(c)
    # fix c_1 by ell(u) = 0; ell is linear in c_1 and ell(-c_1 m) = -c_1
    u0, u10, _ = xu_resolvent(c, np.array([0.0]), c1=0.0, derivs=True, **kw)
    ell_u0 = 1j * u0[0] - u10[0] / 4.0
    c1 = ell_u0
    fn = x_norm_y(lambda yy: (to_y(c, yy), to_y(c, yy, 2)), M=M)
    def uu(yy):
        a, _, a2 = xu_resolvent(c, yy, c1=c1, derivs=True, **kw)
        return a, a2
    un = x_norm_y(uu, M=M)
    return un / fn, un, fn, c1
