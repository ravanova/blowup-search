"""Leg 312 -- ROUTE-APIA: does arbitrary precision change leg 178's or leg 176's
banked headline?

Gate, verbatim from the DM's pre-committed brief:

    "Do the two pre-registered re-measurements (leg 178, leg 176), run at
    arbitrary precision, change the banked headline of leg 178 (the 3.1e+03
    contamination) or leg 176 (the lost N=1024 row) -- magnitudes, not
    booleans?"

This driver performs BOTH re-measurements and reports the before/after
magnitudes.  It does not build a general arbitrary-precision library -- it
patches ONLY the specific step in each banked runner that float64 cannot
represent, using `solver/interval_mp.py`'s rigorous `MPInterval` machinery
(leg 178) and its banded high-precision linear algebra (leg 176), and leaves
everything else (quadrature nodes, weights, the final eigenvalue solves)
exactly as the banked runners computed them, since those steps are not where
either banked artifact's precision loss lives.

Run: `.venv/bin/python experiments/p2_route_apia_v1.py`
Writes: `writeup/data/p2_route_apia_v1.json`
"""
from __future__ import annotations

import json
import math
import sys
import time
from decimal import Context, Decimal, localcontext
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.energy_coercivity import (  # noqa: E402
    clm_linearization_values,
    graded_quadrature,
    wes_coercivity_gap_exact,
    wes_constrained_basis,
    wes_damping_factor,
    wes_weight_values,
)
from solver.interval_mp import (  # noqa: E402
    MPInterval,
    assert_exact_as_decimal,
    banded_cholesky,
    banded_matmul,
    banded_triangular_inverse,
    dcos,
    dsin,
    mp_add,
    mp_mul,
)
from solver.origin_h2_certificate import (  # noqa: E402
    border_row,
    bordered_gram,
    l0_plus,
    symmetry_modes,
    x_gram,
)

OUT = ROOT / "writeup" / "data" / "p2_route_apia_v1.json"

# ---------------------------------------------------------------------------
# Leg 178's own pre-registered configuration, read off
# experiments/p2_route_wes_v1_space.py verbatim (N_QUAD_CHECK, GRADE_DEPTHS,
# the T2_egm|E_egm combination that produced the banked 3.1e+03 / -230.71
# reading) -- not chosen here, reproduced.
# ---------------------------------------------------------------------------
L178_N = 128            # N_QUAD_CHECK
L178_CLASS = "T2_egm"
L178_FAMILY = "E"
L178_GAMMA = 4.0
L178_N_GRADE_BANKED = 96
L178_N_GRADE_CLEAN = 48   # the clean neighbouring depth, for a sanity cross-check
L178_N_UNIF = max(64, 4 * L178_N)   # 512, matches wes_form_matrices_constrained's default
L178_ORDER = 12
L178_UNSAFE_THETA = 1e-3   # min(theta, pi-theta) below this triggers the MP patch
L178_MP_PREC = 120         # working decimal digits for the patched nodes


def _mp_sin_cos(theta_dec, prec):
    """Adaptive-term Taylor series for sin/cos of a small |theta| <= ~6e-3,
    inside an EXPLICIT `localcontext` (so bare operators round correctly to
    `prec` digits -- the ambient-context pitfall `test_interval_mp.py`
    documents does not apply here, since the context is set for the whole
    block). Adaptive term count is the point: at leg 178's own regime
    (theta ~ 3e-31) the second term is already ~theta^3 ~1e-92, far below
    any digit count this leg uses, so the series terminates after ONE term;
    at the outer end of the graded region (theta ~ a few e-3) it needs
    ~15-20 terms. A fixed term count (as `solver/interval_mp.py`'s own
    `dsin`/`dcos` deliberately use, for simplicity and a uniform proof) would
    cost 200+ terms per node regardless -- this local adaptive version is
    the leg's own performance optimisation on top of that machinery, not a
    change to it, and is spot-checked against the rigorous `dsin`/`dcos`
    below."""
    work = prec + 15   # guard digits, matching interval_mp.py's own `work = prec + 20`
    with localcontext(Context(prec=work)):
        x = +theta_dec
        x2 = x * x
        sin_acc = x
        term = x
        cos_acc = Decimal(1)
        cterm = Decimal(1)
        k = 1
        while k < 400:
            term = -term * x2 / Decimal((2 * k) * (2 * k + 1))
            cterm = -cterm * x2 / Decimal((2 * k - 1) * (2 * k))
            sin_acc += term
            cos_acc += cterm
            sin_done = term == 0 or (sin_acc.adjusted() - term.adjusted()) > work
            cos_done = cterm == 0 or (cos_acc.adjusted() - cterm.adjusted()) > work
            if sin_done and cos_done:
                break
            k += 1
    with localcontext(Context(prec=prec)):
        return +sin_acc, +cos_acc


def _spot_check_against_rigorous_mp(thetas, prec, n_report=6):
    """Certify `_mp_sin_cos`'s plain high-precision recurrence against the
    RIGOROUS `MPInterval`-based `dsin`/`dcos` (which passed the adversarial
    battery in `test_interval_mp.py`, including the exact leg-178-regime
    test) on a handful of representative nodes. Returns the worst observed
    relative discrepancy plus the rigorous interval's own width, so the
    plain series' fidelity is a measured number, not an assumption."""
    rows = []
    for th in thetas[:n_report]:
        th = +th
        s_iv = dsin(th, prec)
        c_iv = dcos(th, prec)
        s_plain, c_plain = _mp_sin_cos(th, prec)
        # NB: this midpoint is only for a human-readable "how far off" number
        # -- do it inside an explicit context (the exact ambient-context
        # pitfall test_interval_mp.py documents: a bare `/2` outside any
        # localcontext silently rounds to the 28-digit default) so this
        # diagnostic itself isn't the thing lying.
        with localcontext(Context(prec=prec + 10)):
            s_mid = (s_iv.lo + s_iv.hi) / 2
            c_mid = (c_iv.lo + c_iv.hi) / 2
        s_in = s_iv.contains(s_plain)
        c_in = c_iv.contains(c_plain)
        rows.append({
            "theta": str(th),
            "sin_width": str(s_iv.width), "cos_width": str(c_iv.width),
            "sin_contained": bool(s_in), "cos_contained": bool(c_in),
            "sin_plain_minus_mid": str(s_plain - s_mid),
            "cos_plain_minus_mid": str(c_plain - c_mid),
        })
    all_ok = all(r["sin_contained"] and r["cos_contained"] for r in rows)
    return {"rows": rows, "all_contained": bool(all_ok)}


def _mp_recurrence_all_k(theta_dec, n_k, prec):
    """sin(k*theta), cos(k*theta) for k = 1..n_k via the angle-addition
    recurrence built on `_mp_sin_cos`'s (theta, theta) base pair -- O(n_k)
    Decimal multiplications per node instead of re-deriving each k from a
    fresh series (the performance-rule optimisation for this leg)."""
    with localcontext(Context(prec=prec)):
        s1, c1 = _mp_sin_cos(theta_dec, prec)
        sk, ck = s1, c1
        sins = [s1]
        for _ in range(2, n_k + 1):
            sk, ck = sk * c1 + ck * s1, ck * c1 - sk * s1
            sins.append(sk)
        return sins


def leg178_remeasure():
    t_start = time.time()

    # ---- the banked "before" readings, exactly as leg 178's own runner
    # computed them (float64 throughout) -- read off wes_coercivity_gap_exact
    # directly so the "before" numbers here are the ACTUAL banked function's
    # output, not a re-typed copy of the journal.
    before_96 = wes_coercivity_gap_exact(L178_N, L178_CLASS, L178_FAMILY, L178_GAMMA,
                                          n_grade=L178_N_GRADE_BANKED,
                                          n_unif=L178_N_UNIF, order=L178_ORDER)
    before_48 = wes_coercivity_gap_exact(L178_N, L178_CLASS, L178_FAMILY, L178_GAMMA,
                                          n_grade=L178_N_GRADE_CLEAN,
                                          n_unif=L178_N_UNIF, order=L178_ORDER)

    # ---- rebuild the pointwise pieces (float64) exactly as
    # wes_form_matrices_constrained does, so F can be patched before G/B
    # assembly -- energy_coercivity.py itself is read-only, not edited; this
    # mirrors its published formula (read above) rather than importing a
    # private intermediate it does not expose.
    th, qw = graded_quadrature(n_unif=L178_N_UNIF, n_grade=L178_N_GRADE_BANKED,
                                order=L178_ORDER)
    for x in th[:5]:
        assert_exact_as_decimal(x)   # spot check: float->Decimal is exact
    V = wes_constrained_basis(L178_N, L178_CLASS)     # (128, 126), exact ints
    phi = wes_weight_values(th, L178_FAMILY, L178_GAMMA)
    ks = np.arange(1, L178_N + 1)
    E = np.stack([np.sin(k * th) for k in ks])
    LE = np.stack([clm_linearization_values(th, int(k)) for k in ks])
    HE = np.stack([-np.cos(k * th) + (-1.0) ** int(k) for k in ks])
    F_float = V.T @ E
    LF_float = V.T @ LE
    HF_float = V.T @ HE

    unsafe = np.minimum(th, np.pi - th) < L178_UNSAFE_THETA
    n_unsafe = int(unsafe.sum())

    # certify the plain high-precision recurrence against the rigorous
    # MPInterval dsin/dcos on a handful of nodes spanning the unsafe range
    unsafe_idx = np.nonzero(unsafe)[0]
    order_by_theta = unsafe_idx[np.argsort(np.minimum(th[unsafe_idx],
                                                        np.pi - th[unsafe_idx]))]
    sample_idx = np.unique(np.concatenate([
        order_by_theta[:3], order_by_theta[-3:] if len(order_by_theta) >= 3 else order_by_theta,
    ]))
    sample_thetas = [Decimal(float(min(th[i], np.pi - th[i]))) for i in sample_idx]
    spot_check = _spot_check_against_rigorous_mp(sample_thetas, prec=L178_MP_PREC)

    # patch F (and LF, HF -- same pointwise-cancellation mechanism, same fix)
    # at the unsafe nodes with the MP-recomputed dot products.
    V_int = V.astype(np.int64)
    nz_cols = [np.nonzero(V_int[:, m])[0] for m in range(V.shape[1])]
    t_mp = time.time()
    F_patch = F_float.copy()
    LF_patch = LF_float.copy()
    HF_patch = HF_float.copy()
    for i in unsafe_idx:
        theta_i = th[i]
        # sin/cos series is symmetric enough that using theta itself (not
        # pi-theta) is correct for both ends: sin(k*theta) at theta near pi
        # is NOT small (sin(pi-eps)=sin(eps) but k*theta near k*pi is not),
        # so the near-pi endpoint needs its own recurrence around theta_i
        # directly -- no reflection trick applied, this is a literal
        # recomputation at the literal node.
        theta_dec = Decimal(float(theta_i))
        with localcontext(Context(prec=L178_MP_PREC)):
            sins = _mp_recurrence_all_k(theta_dec, L178_N, L178_MP_PREC)
            # cos(k theta), and the two other pointwise integrands, from the
            # same recurrence pair for consistency
            s1, c1 = _mp_sin_cos(theta_dec, L178_MP_PREC)
            sk, ck = s1, c1
            coss = [c1]
            for _ in range(2, L178_N + 1):
                sk, ck = sk * c1 + ck * s1, ck * c1 - sk * s1
                coss.append(ck)
            for m in range(V.shape[1]):
                idx = nz_cols[m]
                if idx.size == 0:
                    continue
                fs = Decimal(0)
                for k in idx:
                    fs += Decimal(int(V_int[k, m])) * sins[k]
                F_patch[m, i] = float(fs)
            # LF, HF: linearisation is c*sk - s*(-ck+(-1)^k) - k*s*ck with
            # s=sin(theta_i), c=cos(theta_i) -- same catastrophic-cancellation
            # exposure at tiny theta (the whole vector is O(theta) times an
            # O(1) combination), so patched from the same MP sin/cos values.
            s_th, c_th = s1, c1
            le_k = []
            he_k = []
            for k in range(1, L178_N + 1):
                sk_, ck_ = sins[k - 1], coss[k - 1]
                le = c_th * sk_ - s_th * (-ck_ + Decimal((-1) ** k)) - Decimal(k) * s_th * ck_
                he = -ck_ + Decimal((-1) ** k)
                le_k.append(le)
                he_k.append(he)
            for m in range(V.shape[1]):
                idx = nz_cols[m]
                if idx.size == 0:
                    continue
                fl = Decimal(0)
                fh = Decimal(0)
                for k in idx:
                    fl += Decimal(int(V_int[k, m])) * le_k[k]
                    fh += Decimal(int(V_int[k, m])) * he_k[k]
                LF_patch[m, i] = float(fl)
                HF_patch[m, i] = float(fh)
    t_mp_elapsed = time.time() - t_mp

    def _assemble_and_gap(F, LF, HF, n_grade):
        pw = phi * qw
        G = (F * pw) @ F.T
        B = (F * pw) @ LF.T
        eps = float(np.finfo(float).eps)
        Fabs = np.abs(V).T @ np.abs(E)
        num = ((eps * Fabs) ** 2 * pw).sum(axis=1)
        den = (F ** 2 * pw).sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            contamination = float(np.nanmax(np.where(den > 0, num / den, 0.0)))
        D = wes_damping_factor(th, L178_FAMILY, L178_GAMMA)
        B_loc = (F * (pw * D)) @ F.T
        sw = pw * np.sin(th)
        M = (F * sw) @ HF.T
        B_nl = -0.5 * (M + M.T)
        ev, U = np.linalg.eigh(0.5 * (G + G.T))
        top = float(ev.max()) if ev.size else 0.0
        rcond = 1e-12
        keep = ev > rcond * top
        dropped = int(np.sum(~keep))
        W = U[:, keep] / np.sqrt(ev[keep])

        def rayleigh(Mat):
            Mh = W.T @ (0.5 * (Mat + Mat.T)) @ W
            return -float(np.linalg.eigvalsh(0.5 * (Mh + Mh.T)).max())

        return {"gap": rayleigh(0.5 * (B + B.T)), "contamination": contamination,
                "dim_kept": int(np.sum(keep)), "dropped": dropped, "n_grade": n_grade}

    after_float_reproduced = _assemble_and_gap(F_float, LF_float, HF_float,
                                                L178_N_GRADE_BANKED)
    after_mp_patched = _assemble_and_gap(F_patch, LF_patch, HF_patch,
                                          L178_N_GRADE_BANKED)

    elapsed = time.time() - t_start
    return {
        "config": {"n": L178_N, "class": L178_CLASS, "family": L178_FAMILY,
                   "gamma": L178_GAMMA, "n_unif": L178_N_UNIF, "order": L178_ORDER,
                   "n_grade_banked": L178_N_GRADE_BANKED,
                   "n_grade_clean_crosscheck": L178_N_GRADE_CLEAN,
                   "unsafe_theta_threshold": L178_UNSAFE_THETA,
                   "mp_working_precision_digits": L178_MP_PREC,
                   "n_quadrature_nodes": int(len(th)), "n_unsafe_nodes_patched": n_unsafe},
        "before_banked_n_grade_96": {"gap": before_96["gap"],
                                     "contamination": before_96["contamination"]},
        "before_banked_n_grade_48_crosscheck": {"gap": before_48["gap"],
                                                "contamination": before_48["contamination"]},
        "float64_reproduction_check_n_grade_96": after_float_reproduced,
        "after_mp_patched_n_grade_96": after_mp_patched,
        "spot_check_vs_rigorous_mpinterval": spot_check,
        "performance": {"total_seconds": elapsed, "mp_patch_seconds": t_mp_elapsed,
                        "nodes_patched": n_unsafe,
                        "seconds_per_patched_node": (t_mp_elapsed / n_unsafe
                                                     if n_unsafe else 0.0)},
    }


# ---------------------------------------------------------------------------
# Leg 176's own pre-registered configuration -- N=1024, the row leg 176's
# own ladder lost to the Gram float floor ~1e12 (experiments/journal/leg_176.md).
# ---------------------------------------------------------------------------
L176_N = 1024
L176_N_CROSS = 512   # the float-reliable window's own top row, for a sanity check
L176_BW = 4          # x_gram's exact bandwidth
L176_PREC = 60       # working decimal digits for the banded Cholesky chain


def _rect_sigma_mp(N, prec, bw=L176_BW):
    """`sigma_min`, `sigma_max` of the bordered/whitened operator at
    truncation N, using solver/interval_mp.py's banded Cholesky +
    banded-triangular-inverse + banded matmul in place of
    `origin_h2_certificate._sym_sqrt`'s dense `np.linalg.eigh`-based
    symmetric square root -- the step leg 176's own journal names as the
    precision-losing one at N=1024 (Gram condition number ~1e13).

    Mathematical substitution, not an approximation: for SPD `G = R^T R`
    (any valid Cholesky-type factorisation, not necessarily the SYMMETRIC
    square root `_sym_sqrt` uses), `||Ax||_G = ||Rx||_2`, so the singular
    values of `R_c @ A @ R_d^{-1}` equal those of `sqrt(G_c) @ A @
    sqrt(G_d)^{-1}` (two factorisations of the same inner product differ by
    a unitary on each side, which does not change singular values). This
    lets the whitening be built entirely from banded Cholesky + banded
    triangular solves (both O(n^2 * bw), not the O(n^3) dense eigh `_sym_sqrt`
    needs), exploiting `x_gram`'s exact bandwidth-4 structure that leg 176's
    own ladder does not.

    `Gd = bordered_gram(nd, Gx_d)` and `Gc = bordered_gram(Nr, Gx_c)` are
    each EXACTLY block-diagonal (the border amplitude carries weight 1 with
    no cross term), so their Cholesky factors and inverses are block-diagonal
    too -- the border row/column of A is handled by a single dense
    matrix-vector product (O(nd^2), the border row itself is dense), not by
    a dense (nd+1)x(nd+1) solve.

    A = A_re + i*A_im splits into a REAL tridiagonal-shaped block (`L`,
    bandwidth 1) and a REAL structure carrying the (purely imaginary)
    border terms (`m`, `e`), so every Decimal matrix operation below is on
    REAL matrices -- no complex Decimal arithmetic needed anywhere; only the
    final (already well-conditioned) SVD, done in float64, recombines them
    as `W = W_re + i*W_im`.
    """
    Nr = N + 2
    nd = N

    Gx_d = x_gram(nd)
    Gx_c = x_gram(Nr)
    for M, tag in ((Gx_d, "Gx_d"), (Gx_c, "Gx_c")):
        # spot-check exactness of the banded entries actually read
        for i in range(min(5, M.shape[0])):
            for j in range(max(0, i - L176_BW), min(M.shape[1], i + L176_BW + 1)):
                assert_exact_as_decimal(M[i, j])

    Rd = banded_cholesky([[Decimal(Gx_d[i, j]) for j in range(nd)] for i in range(nd)],
                          nd, bw, prec)
    Rc = banded_cholesky([[Decimal(Gx_c[i, j]) for j in range(Nr)] for i in range(Nr)],
                          Nr, bw, prec)
    Zd = banded_triangular_inverse(Rd, nd, bw, prec)   # Rd^{-1}, dense nd x nd

    # A_re = L (Nr x nd, tridiagonal-shaped: nonzero only |i-n|<=1)
    L_full = l0_plus(Nr)
    L_block = [[Decimal(L_full[i, n]) for n in range(nd)] for i in range(Nr)]
    # A_im: m column (top-right, 2 nonzeros) and e row (bottom-left, dense)
    _, m_vec = symmetry_modes(Nr)     # complex, purely imaginary; m/i is real
    m_im = (m_vec / 1j).real
    e_vec = border_row(nd)            # complex, purely imaginary; e/i is real
    e_im = (e_vec / 1j).real
    for x in list(m_im[:2]) + list(e_im[:5]):
        assert_exact_as_decimal(x)

    # Y_re[:Nr, :nd] = L @ Zd  (banded-times-dense, bw_lo=bw_hi=1)
    Y_L = banded_matmul(L_block, 1, 1, Zd, prec)
    # Y_im[Nr, :nd] = e @ Zd   (dense row vector times dense Zd)
    with localcontext(Context(prec=prec)):
        e_dec = [Decimal(float(v)) for v in e_im]
        Y_e = [Decimal(0)] * nd
        for j in range(nd):
            s = Decimal(0)
            for k in range(nd):
                if e_dec[k] != 0:
                    s += e_dec[k] * Zd[k][j]
            Y_e[j] = s

    # W_re[:Nr, :nd] = Rc[:Nr,:Nr] @ Y_L   (banded bw=bw)
    W_re_top = banded_matmul(Rc, bw, bw, Y_L, prec)
    # W_re[:Nr, nd] = Rc @ 0 = 0 (m has no real part)
    # W_re[Nr, :nd] = Y_e  (the border row is untouched by Rc's [1] block)
    # W_re[Nr, nd] = 0
    # W_im[:Nr, :nd] = Rc @ 0 = 0 (L has no imaginary part)
    # W_im[:Nr, nd] = Rc[:Nr,:Nr] @ m_im   (banded times a 2-sparse vector)
    with localcontext(Context(prec=prec)):
        m_col = [[Decimal(float(v))] for v in m_im]
    W_im_col = banded_matmul(Rc, bw, bw, m_col, prec)
    # W_im[Nr, :nd] = 0, W_im[Nr, nd] = 0

    with localcontext(Context(prec=prec)):
        W = np.zeros((Nr + 1, nd + 1), dtype=complex)
        for i in range(Nr):
            for j in range(nd):
                W[i, j] = float(W_re_top[i][j])
            W[i, nd] = 1j * float(W_im_col[i][0])
        for j in range(nd):
            W[Nr, j] = float(Y_e[j])
        W[Nr, nd] = 0.0

    s = np.linalg.svd(W, compute_uv=False)
    return float(s.min()), float(s.max())


def leg176_remeasure():
    t_start = time.time()

    # "before": the banked float64 reading, via the actual banked function
    sys.path.insert(0, str(ROOT / "experiments"))
    import p2_route_h2c_v1_construction as h2c   # noqa: E402
    smin_before, smax_before = h2c.rect_sigma(L176_N, bordered=True, gram=True, lo_mode=0)
    smin_cross_before, smax_cross_before = h2c.rect_sigma(L176_N_CROSS, bordered=True,
                                                            gram=True, lo_mode=0)

    t_mp = time.time()
    smin_after, smax_after = _rect_sigma_mp(L176_N, L176_PREC)
    mp_seconds_1024 = time.time() - t_mp
    t_mp2 = time.time()
    smin_cross_after, smax_cross_after = _rect_sigma_mp(L176_N_CROSS, L176_PREC)
    mp_seconds_512 = time.time() - t_mp2

    elapsed = time.time() - t_start
    return {
        "config": {"N": L176_N, "N_crosscheck": L176_N_CROSS, "bandwidth": L176_BW,
                   "mp_working_precision_digits": L176_PREC},
        "before_banked_N1024": {"sigma_min": smin_before, "sigma_max": smax_before},
        "before_banked_N512_crosscheck": {"sigma_min": smin_cross_before,
                                          "sigma_max": smax_cross_before},
        "after_mp_N1024": {"sigma_min": smin_after, "sigma_max": smax_after},
        "after_mp_N512_crosscheck": {"sigma_min": smin_cross_after,
                                     "sigma_max": smax_cross_after},
        "performance": {"total_seconds": elapsed, "N1024_seconds": mp_seconds_1024,
                        "N512_seconds": mp_seconds_512},
    }


def main():
    print("== Leg 312 / Route-APIA: arbitrary-precision re-measurement of leg 178 and leg 176")
    print("-- leg 178 (T2_egm | E_egm, gamma=4, n_grade=96, N_QUAD_CHECK=128) --")
    t0 = time.time()
    l178 = leg178_remeasure()
    print(f"   banked (float64):  gap {l178['before_banked_n_grade_96']['gap']:+.6f}  "
          f"contamination {l178['before_banked_n_grade_96']['contamination']:.4e}")
    print(f"   MP-patched:        gap "
          f"{l178['after_mp_patched_n_grade_96']['gap']:+.6f}  contamination "
          f"{l178['after_mp_patched_n_grade_96']['contamination']:.4e}")
    print(f"   {l178['config']['n_unsafe_nodes_patched']} / "
          f"{l178['config']['n_quadrature_nodes']} nodes patched, "
          f"{l178['performance']['mp_patch_seconds']:.2f}s "
          f"({l178['performance']['seconds_per_patched_node']*1000:.3f} ms/node), "
          f"total leg178 wall time {time.time()-t0:.2f}s")

    print("-- leg 176 (rect_sigma, bordered, N=1024) --")
    t1 = time.time()
    l176 = leg176_remeasure()
    print(f"   banked (float64):  sigma_min {l176['before_banked_N1024']['sigma_min']:.10f}")
    print(f"   MP-patched:        sigma_min {l176['after_mp_N1024']['sigma_min']:.10f}")
    print(f"   total leg176 wall time {time.time()-t1:.2f}s")

    out = {"leg_312_route_apia": {"leg178": l178, "leg176": l176}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, default=str))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
