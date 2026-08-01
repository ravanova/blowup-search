"""The float rehearsal of the certificate in the reduced space -- and what it still needs.

v14 reduced the two-scale profile problem to a scalar system on the profile's own
support [0, X_c] and showed the discrete approximate inverse CONVERGES there, against
a whole-line ladder that diverges as J^+2.80.  The obvious next move -- and standing
brick (4), "finish one certificate end-to-end" -- is to assemble the four
Newton-Kantorovich constants in that space and see whether the radii polynomial

    p(r) = Z_2 r^2 - (1 - Z_0 - Z_1) r + Y_0 <= 0   for some r > 0

closes in plain float BEFORE anything is hardened (banked lesson 1).  This module is
that rehearsal.  Its result is a NEGATIVE with a named repair, so read the verdict
before reusing any number in it.

--------------------------------------------------------------------------
WHAT THE REHEARSAL FINDS
--------------------------------------------------------------------------
(1) **Y_0 reaches machine precision.**  The defect that matters is the residual of the
    INTERPOLANT as a function, not the nodal vector Newton zeroed (the v12 distinction,
    which survives the change of formulation).  `interpolant_defect` evaluates F off the
    collocation nodes; it falls to ~1e-12 by K ~ 96 at a = 0.3.  Sixteen legs carried a
    defect floor of ~1e-2 (GA) and then ~1e-4 (whole-line Newton, anchor-priced budget);
    this is the first time the number a certificate needs is at machine level.

(2) **Z_0 is roundoff**, as it must be when A is built from the same DF.  Reported so
    the ledger is complete, not because it is informative.

(3) **Z_2 DOES NOT EXIST IN THE SUP SETTING, and the far field is not why.**  Two
    separate obstructions, both measured here:

    (3a) **The finite Hilbert transform is unbounded on the sup norm** -- on a BOUNDED
         interval.  Removing the far field killed the DECAY grading v3-v11 needed; it did
         nothing to the SMOOTHNESS one.  `step_adversary` builds the classical extremal
         family (Chebyshev partial sums of a step) inside the actual perturbation space
         de = (1-v^2) ds: the ratio runs 1.35 -> 3.04 over K = 8..256, linear in log K at
         +0.499 per e-fold, and is STABLE under a 4x refinement of the quadrature.
         The naive probe -- a single high Chebyshev mode -- reports a divergence too
         (0.99 -> 6.44) and it is entirely the quadrature: refined, it is flat at 0.999 at
         every K.  Banked lessons 9 and 14 in one table, which is why both rows are kept.

    (3b) **The nonlinearity's second derivative is bounded exactly for a <= 1/2.**
         N(e) = e^{1/a} has N''(e) = p(p-1) e^{p-2}, p = 1/a, and e vanishes LINEARLY at
         the support edge, so sup|N''| is finite iff p >= 2 iff **a <= 1/2** -- which is
         exactly where Omega = -e^{1/a} loses C^2.  Measured: flat at 20 / 7.78 / 3.75 /
         2.716 / 2.000 for a = 0.2 ... 0.5 under any edge cutoff, and divergent as the
         cutoff tightens for a > 1/2 (a=0.55: 5.6 -> 19.8 -> 105.8; a=0.8: 60 -> 1.1e4 ->
         1.1e7).  **This is a property of the NORM, not of the equation** -- v14 solved the
         profile cleanly to a = 1.2 -- and a weight vanishing like (1-v)^{(2-1/a)/2}
         restores finiteness at the price of restricting the perturbation class.
         **Do NOT read it as an explanation of the survival boundary a* ~ 0.5-0.55.**  The
         coincidence is recorded because it is striking and because recording it is how the
         next person gets to disprove it.

(4) **Z_1 IS NOT COMPUTED.**  It is the infinite-dimensional tail -- the part of the
    operator outside the K-mode subspace -- and it is the whole content of a real
    computer-assisted proof.  Nothing here bounds it and nothing here should be read as
    if it did.

--------------------------------------------------------------------------
THE VERDICT (state it before running)
--------------------------------------------------------------------------
The sup-to-sup rehearsal **does not close**, because Z_2 is infinite in it by (3a).
That is a real negative and it is NOT the obstruction v12/v13 found: it is the one v4
found on the whole line (W3, "H is unbounded on L^infty") surviving the move to a
bounded interval.  The repair is the one v5 built and is MEASURED here:
`holder_ratio` re-runs the adversary against a Holder domain norm and the divergence
stops at **gamma >~ 0.35** (slopes +0.499 sup, +0.066 at gamma=0.15, -0.021 at 0.35,
-0.049 at 0.5) -- the same threshold v5 U1 found in a completely different geometry.
So v5/v8's Holder machinery is not wasted; its compact-interval version is the next
brick, and it is a smaller job than the whole-line one because there is no decay
grading and no matching radius left to price.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np

from solver.first_integral import (ReducedProfile, even_cheb, graded_grid,
                                   hilbert_pv)


# ---------------------------------------------------------------------------
# Y_0 and Z_0
# ---------------------------------------------------------------------------


def interpolant_defect(rp, b, Xc, n=997):
    """sup |F| of the INTERPOLANT, evaluated OFF the collocation nodes.

    Newton drives F to ~1e-14 at the K nodes by construction; the certificate asks
    about F as a function on [0, 1].  The evaluation grid is Chebyshev-like and
    deliberately of a size coprime to the node count, so it does not accidentally
    sample where the residual is already zero.
    """
    n = int(n)
    v = 0.5 * (1.0 - np.cos(np.pi * (np.arange(n) + 0.5) / n))
    T, dT = even_cheb(rp.K, v)
    e = (1.0 - v ** 2) * (T @ b)
    de = -2.0 * v * (T @ b) + (1.0 - v ** 2) * (dT @ b)
    e_u = rp.PHI_u @ b
    H = hilbert_pv(rp.u, rp.w, np.abs(e_u) ** rp.p, np.abs(e) ** rp.p, v)
    return float(np.max(np.abs(rp.c * de + rp.a * Xc * H)))


def z0_defect(rp, b, Xc):
    """||I - A DF|| for A = the numerically inverted Jacobian: roundoff, by design."""
    M = rp.jacobian(b, Xc)
    A = np.linalg.inv(M)
    return float(np.max(np.abs(A @ M - np.eye(rp.K + 1)).sum(axis=1)))


# ---------------------------------------------------------------------------
# the Z_2 ingredients
# ---------------------------------------------------------------------------


def second_derivative_sup(rp, b, edge_cutoffs=(1e-3, 1e-6, 1e-10), n=20001):
    """sup |N''(e)| = |p(p-1)| sup e^{p-2}, by how close to the support edge we look.

    FLAT across cutoffs  => finite (p >= 2, i.e. a <= 1/2).
    GROWING with cutoff  => the sup is infinite and the cutoff is the only thing
                            keeping it finite, which is the honest way to display a
                            divergence rather than quoting whatever the grid happened
                            to reach.
    """
    p = rp.p
    out = []
    for eps in edge_cutoffs:
        v = np.linspace(0.0, 1.0 - float(eps), int(n))
        e = np.abs(rp.e_of(b, v))
        out.append(float(np.max(abs(p * (p - 1.0)) * e ** (p - 2.0))))
    return out


def _step_coefficients(K, m=8000):
    """Even Chebyshev coefficients of sign(|v| - 1/2): the classical extremal family.

    The adversary for the sup-norm boundedness of H is a JUMP, and its band-limited
    approximations are the partial sums.  Sampling smooth perturbations cannot find
    this direction (banked lesson 9) -- it has to be constructed.
    """
    th = np.pi * (np.arange(int(m)) + 0.5) / int(m)
    f = np.sign(np.abs(np.cos(th)) - 0.5)
    return np.array([(2.0 / int(m)) * np.sum(f * np.cos(2 * k * th))
                     * (0.5 if k == 0 else 1.0) for k in range(int(K))])


def step_adversary(K, levels=24, order=60, n_eval=2001, kind="step"):
    """sup|Hpv[de]| / sup|de| over the perturbation space de = (1-v^2) ds.

    `kind="step"` is the adversary; `kind="single"` is the naive probe (one high
    Chebyshev mode) kept as the CONTROL, because it reports a divergence that is
    purely the quadrature and vanishes under refinement.
    """
    u, w = graded_grid(levels, order)
    v = np.linspace(-0.999, 0.999, int(n_eval))
    c = np.zeros(int(K))
    if kind == "single":
        c[int(K) - 1] = 1.0
    else:
        c = _step_coefficients(K)
    T_u, _ = even_cheb(K, u)
    T_v, _ = even_cheb(K, v)
    de_u = (1.0 - u ** 2) * (T_u @ c)
    de_v = (1.0 - v ** 2) * (T_v @ c)
    H = hilbert_pv(u, w, de_u, de_v, v)
    return float(np.max(np.abs(H)) / np.max(np.abs(de_v)))


def holder_seminorm(f, x, gamma):
    """[f]_gamma = sup_{i != j} |f_i - f_j| / |x_i - x_j|^gamma."""
    d = np.abs(np.asarray(x)[:, None] - np.asarray(x)[None, :])
    num = np.abs(np.asarray(f)[:, None] - np.asarray(f)[None, :])
    np.fill_diagonal(d, np.inf)
    return float(np.max(num / d ** float(gamma)))


def holder_ratio(K, gamma, levels=24, order=60, n_eval=2001, n_semi=401):
    """The same adversary, against ||de||_gamma = sup|de| + [de]_gamma.

    v5 U1 did this on the whole line and found the divergence stops at gamma >~ 0.35.
    Repeating it on the bounded interval is a genuine independent check: the decay
    grading that v5's norm also carried is absent here, so if the threshold survives
    it belongs to the smoothness half.
    """
    u, w = graded_grid(levels, order)
    v = np.linspace(-0.999, 0.999, int(n_eval))
    xs = np.linspace(-0.999, 0.999, int(n_semi))
    c = _step_coefficients(K)
    T_u, _ = even_cheb(K, u)
    T_v, _ = even_cheb(K, v)
    T_x, _ = even_cheb(K, xs)
    de_u = (1.0 - u ** 2) * (T_u @ c)
    de_v = (1.0 - v ** 2) * (T_v @ c)
    de_x = (1.0 - xs ** 2) * (T_x @ c)
    H = hilbert_pv(u, w, de_u, de_v, v)
    nrm = np.max(np.abs(de_v)) + holder_seminorm(de_x, xs, gamma)
    return float(np.max(np.abs(H)) / nrm)


# ---------------------------------------------------------------------------
# the assembled rehearsal
# ---------------------------------------------------------------------------


def rehearsal(a, K=96, Xc0=10.0):
    """Y_0, Z_0, the Z_2 ingredients, and an explicit verdict with Z_1 named as open.

    Returns a dict whose `verdict` field says, in words, that the sup-to-sup budget
    does not close and why.  It deliberately does NOT return an assembled radii
    polynomial: assembling one from constants that include an infinity, or from a
    ledger with an uncomputed entry, is the exact failure mode banked as lesson 15.
    """
    rp = ReducedProfile(a, K=K)
    r = rp.solve(Xc0=Xc0)
    if not r["converged"]:
        return {"a": a, "K": K, "converged": False, "detail": r}
    b, Xc = r["b"], r["Xc"]
    npp = second_derivative_sup(rp, b)
    finite = bool(rp.p >= 2.0 and max(npp) / min(npp) < 1.01)
    return {
        "a": float(a), "K": int(K), "converged": True,
        "Xc_over_c": r["Xc"], "newton_residual": r["residual"],
        "Y0_interpolant_defect": interpolant_defect(rp, b, Xc),
        "Z0": z0_defect(rp, b, Xc),
        "opnorm": rp.operator_norm(b, Xc),
        "N2_sup_by_cutoff": npp,
        "N2_finite": finite,
        "Z1": None,
        "verdict": ("Y_0 is at machine level and Z_0 is roundoff. Z_2 is INFINITE in "
                    "the sup-to-sup setting because the finite Hilbert transform is "
                    "unbounded on the sup norm even on a bounded interval (see "
                    "step_adversary); and separately sup|N''| is finite only for "
                    "a <= 1/2 (see N2_finite). Z_1, the infinite-dimensional tail, is "
                    "NOT computed. The budget therefore DOES NOT CLOSE and no radii "
                    "polynomial is returned. The named repair is a Holder domain norm "
                    "with gamma >~ 0.35 (see holder_ratio).")}
