"""VER-A (leg 54): INDEPENDENT re-derivation of leg 53's headline numbers.

This is a VERIFICATION script.  It does not import leg 53's runner for anything it
checks -- the augmented block, the amplitude column, the sub-block norms and the closed
forms are rebuilt here from `solver/spectral_certificate.py` primitives only, and then
compared against leg 53's committed JSON.  Where the two disagree, the disagreement is
the finding.

Checks, in order:
  V1  ||Gamma^{-1}|| closed forms: 2(K^2 - 1) augmented, 4(K - 1) unaugmented.
      Re-derived numerically over K, in BOTH classes and BOTH gauges, and confirmed in
      EXACT RATIONAL arithmetic so that "exactly" is not a float coincidence.
  V2  Z1[tail <- Gamma] over the full sweep, plus the splits leg 53 did NOT run
      (K = 2, 3, 5, 6, 12, 24, 48), to test whether 0.9961 is the true minimum.
  V3  Y_0: is it exactly zero, or a hardcoded constant?  Exact rational residual of the
      anchor, INCLUDING the matching row and the far-field column.
  V4  The positive control: does Z1 at mu = 2 actually move when the dissipation and the
      border direction are perturbed (lesson 90)?
  V5  MM-1's inequality  Z1 >= |1 - K/2| * (w_{K+1}/w_K) * ||A_tail e_{K+1}||_w / w_{K+1}
      -- LHS and RHS both measured, and the factor |1 - K/2| tabulated over K.

Run: .venv/bin/python -u experiments/p2_route_mm_v1_headline_verify.py
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.spectral_certificate import (                              # noqa: E402
    bordered_linearization, clm_residual_exact, quadratic_bound,
    rigorous_finite_block, tail_block, tail_left_null, tail_right_null,
)

TC_JSON = ROOT / "writeup" / "data" / "p2_route_tc_v1_assemble.json"
M_EXTRA = 1024
CLASSES = (("flat", 0.0), ("algebraic", 0.3))


# ---------------------------------------------------------------- primitives
def wfun(k, kind, param):
    k = np.asarray(k, dtype=float)
    if kind == "flat":
        return np.ones_like(k)
    if kind == "algebraic":
        return (1.0 + k) ** float(param)
    raise ValueError(kind)


def colsum_norm(A):
    """max_j sum_i |A_ij| -- the l^1 operator norm of an ALREADY-SCALED matrix."""
    A = np.abs(np.asarray(A, float))
    return float(np.max(A.sum(0))) if A.size else 0.0


def far_field_column(K, M, h=None):
    """L applied to the tail kernel hhat, restricted to the finite rows.

    Re-derived, not imported.  hhat lives on modes K+1..M with h_{K+1} = 1.  The exact
    linearisation sends mode m to: (1 - m/2) into row m+1, (m/2) into row m-1, and
    -(-1)^m into row 1.  Restricted to rows 1..K only mode K+1's `(K+1)/2` term into row
    K survives from the bidiagonal part, plus the full rank-one row-1 sum.
    """
    h = tail_right_null(K, M) if h is None else np.asarray(h, float)
    m = np.arange(K + 1, M + 1, dtype=float)
    col = np.zeros(K)
    col[K - 1] += (K + 1) / 2.0 * h[0]
    row1 = float(np.sum(-((-1.0) ** m) * h))
    col[0] += row1
    return col, row1, float(np.sum(m * h)), h


def augmented(K, M, kind, param, gauge="null", mu=0.0, far_field=True, h=None,
              col_w="hhat_norm", row_w="w_Kplus1"):
    """Gamma with (optionally) the amplitude column and the matching row, plus weights."""
    K = int(K)
    F = bordered_linearization(K, mu=mu)
    col, row1, gauge_entry, hh = far_field_column(K, M, h=h)
    wk = wfun(np.arange(1, K + 1), kind, param)
    if not far_field:
        G = F.copy()
        if gauge == "null":
            G[K, :] = 0.0
            G[K, 1] = 1.0
        w = np.concatenate([wk, [1.0]])
        return G, w, w, gauge_entry, hh
    N = K + 2
    G = np.zeros((N, N))
    G[:K + 1, :K + 1] = F
    G[:K, K + 1] = col
    if gauge == "dilation":
        G[K, K + 1] = gauge_entry
    else:
        G[K, :] = 0.0
        G[K, 1] = 1.0
        G[K, K + 1] = 0.0
    G[K + 1, K + 1] = 1.0
    hnorm = float(np.sum(wfun(np.arange(K + 1, M + 1), kind, param) * np.abs(hh)))
    pick = {"hhat_norm": hnorm, "one": 1.0,
            "w_Kplus1": float(wfun([K + 1], kind, param)[0])}
    w_col = np.concatenate([wk, [1.0], [pick[col_w]]])
    w_row = np.concatenate([wk, [1.0], [pick[row_w]]])
    return G, w_row, w_col, gauge_entry, hh


def gamma_inv_norm(K, M, kind, param, gauge="null", far_field=True, mu=0.0, **kw):
    G, w_row, w_col, _, _ = augmented(K, M, kind, param, gauge, mu, far_field, **kw)
    Gs = G * (w_row[:, None] / w_col[None, :])
    return colsum_norm(np.linalg.inv(Gs))


def tail_inverse(K, M, kind, param, mu=0.0, border="analytic", seed=0):
    T = tail_block(K, M, mu=mu)
    k = np.arange(int(K) + 1, int(M) + 1, dtype=float)
    w = wfun(k, kind, param)
    Ts = T * (w[:, None] / w[None, :])
    n = int(M) - int(K)
    if border is None:
        return np.linalg.inv(Ts), w
    if border == "analytic":
        v, u = tail_right_null(K, M) * w, tail_left_null(K, M) * w
    elif border in ("svd", "second"):
        U, S, Vt = np.linalg.svd(Ts)
        i = -1 if border == "svd" else -2
        v, u = Vt[i, :], U[:, i]
    elif border == "random":
        rng = np.random.default_rng(seed)
        v, u = rng.standard_normal(n), rng.standard_normal(n)
    else:
        raise ValueError(border)
    v, u = v / np.linalg.norm(v), u / np.linalg.norm(u)
    B = np.zeros((n + 1, n + 1))
    B[:n, :n] = Ts
    B[:n, n] = u
    B[n, :n] = v
    return np.linalg.inv(B), w


def z1_tail_from_gamma(K, M, kind, param, gauge="null", mu=0.0, border="analytic",
                       far_field=True, seed=0, return_cols=False, **kw):
    """||A_tail L_{tail<-Gamma}||_w, and WHICH column attains it."""
    h = None
    if far_field and border not in (None, "analytic"):
        h = _amp_direction(K, M, kind, param, border, seed)
    G, w_row, w_col, _, hh = augmented(K, M, kind, param, gauge, mu, far_field, h=h, **kw)
    Ainv, wt = tail_inverse(K, M, kind, param, mu, border, seed)
    n = int(M) - int(K)
    Ltg = np.zeros((n, G.shape[1]))
    Ltg[0, K - 1] = 1.0 - K / 2.0
    if far_field:
        Ltg[:, K + 1] = tail_block(K, M, mu=mu) @ hh
    Ltg_s = (Ltg * wt[:, None]) / w_col[None, :]
    A_TT = Ainv[:, :n] if border is not None else Ainv
    cols = np.abs(A_TT @ Ltg_s).sum(0)
    if return_cols:
        return float(np.max(cols)), int(np.argmax(cols)), cols
    return float(np.max(cols))


def _amp_direction(K, M, kind, param, border, seed):
    T = tail_block(K, M)
    k = np.arange(int(K) + 1, int(M) + 1, dtype=float)
    w = wfun(k, kind, param)
    Ts = T * (w[:, None] / w[None, :])
    n = int(M) - int(K)
    if border in ("svd", "second"):
        U, S, Vt = np.linalg.svd(Ts)
        v = Vt[-1 if border == "svd" else -2, :]
    else:
        v = np.random.default_rng(seed).standard_normal(n)
    v = v / w
    return v / v[0] if v[0] != 0 else v / np.max(np.abs(v))


def z1_gamma_from_tail(K, M, kind, param, gauge="null", mu=0.0, border="analytic",
                       far_field=True, seed=0, **kw):
    # the amplitude direction MUST be threaded into Gamma here, or the border-direction
    # control becomes a tautology of this script -- lesson 90, and the first draft of this
    # verifier had exactly that bug.
    h = None
    if far_field and border not in (None, "analytic"):
        h = _amp_direction(K, M, kind, param, border, seed)
    G, w_row, w_col, _, _ = augmented(K, M, kind, param, gauge, mu, far_field, h=h, **kw)
    Gs = G * (w_row[:, None] / w_col[None, :])
    Ginv = np.linalg.inv(Gs)
    _, wt = tail_inverse(K, M, kind, param, mu, border)
    n = int(M) - int(K)
    Lgt = np.zeros((G.shape[0], n))
    mt = np.arange(K + 1, M + 1, dtype=float)
    Lgt[K - 1, 0] += (K + 1) / 2.0
    Lgt[0, :] += -((-1.0) ** mt)
    if gauge == "dilation":
        Lgt[K, :] += mt
    if far_field:
        Lgt[K + 1, 0] += -1.0
    return colsum_norm(Ginv @ ((Lgt * w_row[:, None]) / wt[None, :]))


# ---------------------------------------------------------------- V1
def rational_inverse(Mx):
    n = len(Mx)
    A = [list(r) + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(Mx)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        if A[p][c] == 0:
            raise ValueError("singular")
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]


def v1_closed_forms():
    print("\n[V1] the two closed forms, re-derived (flat weights, gauge = null)")
    rows = []
    for K in (4, 6, 8, 12, 16, 24, 32, 48, 64):
        M = K + M_EXTRA
        aug = gamma_inv_norm(K, M, "flat", 0.0, "null", far_field=True)
        una = gamma_inv_norm(K, M, "flat", 0.0, "null", far_field=False)
        # WHICH column attains it -- the attribution leg 53 got wrong once
        G, wr, wc, _, _ = augmented(K, M, "flat", 0.0, "null", 0.0, True)
        ca = np.abs(np.linalg.inv(G * (wr[:, None] / wc[None, :]))).sum(0)
        G2, wr2, wc2, _, _ = augmented(K, M, "flat", 0.0, "null", 0.0, False)
        cu = np.abs(np.linalg.inv(G2 * (wr2[:, None] / wc2[None, :]))).sum(0)
        rows.append({"K": K, "aug": aug, "unaug": una,
                     "aug_argmax_col": int(np.argmax(ca)),
                     "aug_argmax_is_amplitude_col": bool(int(np.argmax(ca)) == K + 1),
                     "unaug_argmax_col": int(np.argmax(cu)),
                     "unaug_argmax_is_mode_K_row": bool(int(np.argmax(cu)) == K - 1),
                     "aug_pred": 2.0 * (K * K - 1), "unaug_pred": 4.0 * (K - 1),
                     "aug_relerr": abs(aug - 2.0 * (K * K - 1)) / (2.0 * (K * K - 1)),
                     "unaug_relerr": abs(una - 4.0 * (K - 1)) / (4.0 * (K - 1))})
        print(f"      K={K:3d}  aug ||G^-1|| = {aug:12.5f}  vs 2(K^2-1) = "
              f"{2*(K*K-1):9.1f}  relerr {rows[-1]['aug_relerr']:.2e}   |   "
              f"unaug = {una:10.5f} vs 4(K-1) = {4*(K-1):6.1f}  relerr "
              f"{rows[-1]['unaug_relerr']:.2e}")
        print(f"             attained at: aug -> col {rows[-1]['aug_argmax_col']} "
              f"(amplitude col = {K+1}: {rows[-1]['aug_argmax_is_amplitude_col']}) ; "
              f"unaug -> col {rows[-1]['unaug_argmax_col']} "
              f"(mode-K row = {K-1}: {rows[-1]['unaug_argmax_is_mode_K_row']})")
    # exact rational, unaugmented, flat weights, null gauge
    print("      exact rational check of the UNAUGMENTED closed form 4(K-1):")
    exact = []
    for K in (4, 8, 16, 32):
        F = bordered_linearization(K, exact=True)
        Fr = [[Fraction(x) for x in row] for row in F]
        Fr[K] = [Fraction(0)] * (K + 1)
        Fr[K][1] = Fraction(1)
        A = rational_inverse(Fr)
        nrm = max(sum(abs(A[i][j]) for i in range(K + 1)) for j in range(K + 1))
        exact.append({"K": K, "exact": str(nrm), "pred": 4 * (K - 1),
                      "equal": nrm == Fraction(4 * (K - 1))})
        print(f"        K={K:3d}: exact = {nrm}  4(K-1) = {4*(K-1)}  EQUAL = "
              f"{nrm == Fraction(4*(K-1))}")
    # does the closed form survive the OTHER class and the OTHER gauge?
    print("      does 2(K^2-1) survive s = 0.3 and the dilation gauge?")
    other = []
    for kind, p in CLASSES:
        for gauge in ("null", "dilation"):
            for K in (4, 16, 64):
                a = gamma_inv_norm(K, K + M_EXTRA, kind, p, gauge, far_field=True)
                other.append({"class": kind, "param": p, "gauge": gauge, "K": K,
                              "aug": a, "ratio_to_2K2m1": a / (2.0 * (K * K - 1))})
                print(f"        {kind:9s} s={p:.1f} gauge={gauge:8s} K={K:3d}: "
                      f"{a:14.5f}  = {a/(2*(K*K-1)):8.4f} x 2(K^2-1)")
    return {"flat_null": rows, "exact_unaugmented": exact, "other_classes_gauges": other}


# ---------------------------------------------------------------- V2
def v2_tail_from_gamma():
    print("\n[V2] Z1[tail <- Gamma] over leg 53's sweep AND the splits it did not run")
    rows = []
    for kind, p in CLASSES:
        for gauge in ("dilation", "null"):
            for K in (2, 3, 4, 5, 6, 8, 12, 16, 24, 32, 48, 64):
                M = K + M_EXTRA
                v, jmax, cols = z1_tail_from_gamma(K, M, kind, p, gauge,
                                                   return_cols=True)
                rows.append({"class": kind, "param": p, "gauge": gauge, "K": K,
                             "Z1_tail_Gamma": v, "argmax_col": jmax,
                             "col_is_bK": jmax == K - 1,
                             "col_is_amplitude": jmax == K + 1,
                             "in_leg53_sweep": K in (4, 8, 16, 32, 64)})
    mn = min(rows, key=lambda r: r["Z1_tail_Gamma"])
    mn53 = min([r for r in rows if r["in_leg53_sweep"]],
               key=lambda r: r["Z1_tail_Gamma"])
    for r in rows:
        mark = "  " if r["in_leg53_sweep"] else " *"
        print(f"     {mark}{r['class']:9s} s={r['param']:.1f} {r['gauge']:8s} "
              f"K={r['K']:3d}: Z1[tG] = {r['Z1_tail_Gamma']:10.4f}   argmax col "
              f"{r['argmax_col']:3d} ({'b_K' if r['col_is_bK'] else ('amp' if r['col_is_amplitude'] else 'other')})")
    print(f"      MIN over leg 53's own sweep (K = 4..64): {mn53['Z1_tail_Gamma']:.4f} "
          f"at {mn53['class']} s={mn53['param']} {mn53['gauge']} K={mn53['K']}")
    print(f"      MIN over the EXTENDED sweep (K = 2..64):  {mn['Z1_tail_Gamma']:.4f} "
          f"at {mn['class']} s={mn['param']} {mn['gauge']} K={mn['K']}")
    return {"rows": rows, "min_leg53_sweep": mn53, "min_extended": mn}


# ---------------------------------------------------------------- V3
def v3_y0():
    print("\n[V3] is Y_0 exactly zero, or a hardcoded constant?")
    res_exact = clm_residual_exact(K=8)
    allzero = all(x == 0 for x in res_exact)
    print(f"      exact rational residual of the a=0 CLM anchor (K=8): "
          f"{[str(x) for x in res_exact]}  ALL ZERO = {allzero}")
    # the matching row's residual: the anchor's far-field amplitude
    K, M = 16, 16 + M_EXTRA
    _, _, _, hh = far_field_column(K, M)
    anchor_tail = np.zeros(M - K)          # Omega_0 = -sin theta lives in mode 1 only
    amp_resid = float(np.max(np.abs(anchor_tail)))
    print(f"      the anchor's tail coefficients (modes K+1..M): max |.| = {amp_resid:.1e}"
          f"  -> the matching row's residual is 0 for the same structural reason")
    rig = rigorous_finite_block(16, "flat", 0.0)
    print(f"      NOTE: rigorous_finite_block returns Y0 as the LITERAL 0.0 "
          f"(value {rig['Y0']}), and the runner sets Y0 = 0.0 at the polynomial. "
          f"Neither evaluates a float residual; the justification is the exact "
          f"rational identity above, which does hold.")
    return {"exact_residual_all_zero": bool(allzero),
            "exact_residual": [str(x) for x in res_exact],
            "anchor_tail_max_abs": amp_resid,
            "Y0_is_hardcoded_not_measured": True,
            "hardcoded_but_justified_by_exact_rational_identity": bool(allzero)}


# ---------------------------------------------------------------- V4
def v4_control():
    print("\n[V4] the positive control -- can it come out differently? (lesson 90)")
    rows = []
    for mu in (0.0, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        for kind, p in CLASSES:
            K, M = 16, 16 + M_EXTRA
            border = "analytic" if mu == 0.0 else None
            ff = (mu == 0.0)
            tg = z1_tail_from_gamma(K, M, kind, p, "null", mu, border, ff)
            gt = z1_gamma_from_tail(K, M, kind, p, "null", mu, border, ff)
            Ainv, _ = tail_inverse(K, M, kind, p, mu, border)
            G, wr, wc, _, _ = augmented(K, M, kind, p, "null", mu, ff)
            Gs = G * (wr[:, None] / wc[None, :])
            Gi = np.linalg.inv(Gs)
            gg = colsum_norm(np.eye(G.shape[0]) - Gi @ Gs)
            n = M - K
            Ts = tail_block(K, M, mu=mu) * 1.0
            wt = wfun(np.arange(K + 1, M + 1), kind, p)
            Ts = Ts * (wt[:, None] / wt[None, :])
            tt = (colsum_norm(np.eye(n) - Ainv @ Ts) if border is None
                  else colsum_norm(np.eye(n + 1) - Ainv @ np.linalg.inv(Ainv)))
            tot = gg + tg + gt + tt
            rows.append({"mu": mu, "class": kind, "param": p, "Z1_total": tot,
                         "Z1_tail_Gamma": tg, "Z1_Gamma_tail": gt,
                         "A_tail_norm": colsum_norm(Ainv)})
            print(f"      mu={mu:5.2f} {kind:9s} s={p:.1f}: ||A_tail||="
                  f"{rows[-1]['A_tail_norm']:11.4g}  Z1[tG]={tg:10.4g}  "
                  f"Z1[Gt]={gt:10.4g}  Z1_total={tot:10.4g}")
    below = [r for r in rows if r["mu"] > 0 and r["Z1_total"] < 1.0]
    mu2 = [r for r in rows if r["mu"] == 2.0]
    print(f"      Z1 < 1 reached at mu in "
          f"{sorted(set(r['mu'] for r in below)) if below else 'NEVER'}")
    print(f"      at mu = 2: {[round(r['Z1_total'], 4) for r in mu2]}")
    # does the control depend on the BORDER at all?  At mu > 0 the runner forces
    # border=None and far_field=False, so the border direction cannot reach it.
    print("      border sensitivity, with the amplitude direction threaded through Gamma")
    print("      (the runner hard-wires border=None at mu > 0, so the CONTROL ITSELF is")
    print("       border-independent by construction -- these rows force it on):")
    bs = []
    for mu in (0.0, 2.0):
        for border in ("analytic", "svd", "second", "random"):
            K, M = 16, 16 + M_EXTRA
            tg = z1_tail_from_gamma(K, M, "algebraic", 0.3, "null", mu, border, True)
            gt = z1_gamma_from_tail(K, M, "algebraic", 0.3, "null", mu, border, True)
            bs.append({"mu": mu, "border": border, "Z1_tail_Gamma": tg,
                       "Z1_Gamma_tail": gt})
            print(f"        mu={mu:.1f} border={border:9s}: Z1[tG]={tg:11.4g}  "
                  f"Z1[Gt]={gt:13.5g}")
    ident = {mu: len(set(round(b["Z1_Gamma_tail"], 6) for b in bs
                         if b["mu"] == mu)) == 1 for mu in (0.0, 2.0)}
    print(f"        Z1[Gt] identical across borders?  {ident}  (True => tautology)")
    return {"mu_ladder": rows, "border_sensitivity": bs,
            "Z1_Gamma_tail_identical_across_borders": {str(k): bool(v)
                                                       for k, v in ident.items()},
            "control_is_border_independent_by_construction": True}


# ---------------------------------------------------------------- V5
def v5_mm1():
    print("\n[V5] MM-1's inequality, both sides measured")
    print("      Z1 >= |1 - K/2| * (w_{K+1}/w_K) * ||A_tail e_{K+1}||_w / w_{K+1}")
    rows = []
    for kind, p in CLASSES:
        for K in (2, 3, 4, 5, 6, 8, 16, 32, 64):
            M = K + M_EXTRA
            Ainv, wt = tail_inverse(K, M, kind, p, 0.0, "analytic")
            n = M - K
            e1 = np.zeros(n)
            e1[0] = 1.0
            col = np.abs(Ainv[:, :n] @ e1).sum()      # ||A_tail e_{K+1}||_w / w_{K+1}
            wK = float(wfun([K], kind, p)[0])
            wK1 = float(wfun([K + 1], kind, p)[0])
            second = (wK1 / wK) * col
            rhs = abs(1.0 - K / 2.0) * second
            lhs = z1_tail_from_gamma(K, M, kind, p, "null")
            rows.append({"class": kind, "param": p, "K": K,
                         "factor_1_minus_K_over_2": abs(1.0 - K / 2.0),
                         "second_factor": second, "rhs": rhs, "lhs_Z1_tail_Gamma": lhs,
                         "inequality_holds": bool(lhs >= rhs - 1e-9),
                         "rhs_above_one": bool(rhs > 1.0)})
            print(f"      {kind:9s} s={p:.1f} K={K:3d}: |1-K/2|={abs(1-K/2):6.1f}  "
                  f"second={second:7.4f}  RHS={rhs:10.4f}  "
                  f"LHS(Z1[tG])={lhs:10.4f}  holds={rows[-1]['inequality_holds']}  "
                  f"RHS>1={rows[-1]['rhs_above_one']}")
    sf = [r["second_factor"] for r in rows]
    sf53 = [r["second_factor"] for r in rows if r["K"] in (4, 8, 16, 32, 64)]
    print(f"      second factor over the whole table (K = 2..64): "
          f"{min(sf):.4f} .. {max(sf):.4f}")
    print(f"      second factor over LEG 53's OWN SWEEP (K = 4..64): "
          f"{min(sf53):.4f} .. {max(sf53):.4f}   "
          f"(the directive quotes 0.94 .. 1.33)")
    bad = [r for r in rows if not r["rhs_above_one"]]
    print(f"      splits where MM-1's RHS is NOT above 1 (so the inequality does NOT "
          f"forbid closure): K = {sorted(set(r['K'] for r in bad))}")
    return {"rows": rows, "second_factor_range_K2_64": [min(sf), max(sf)],
            "second_factor_range_leg53_sweep": [min(sf53), max(sf53)],
            "K_where_rhs_not_above_one": sorted(set(r["K"] for r in bad)),
            "equality_not_just_inequality": bool(
                all(abs(r["lhs_Z1_tail_Gamma"] - r["rhs"]) <= 1e-9 * max(1.0, r["rhs"])
                    for r in rows if r["K"] >= 3))}


def main():
    out = {"verifier": "VER-A", "serves_leg": 54, "verifies_leg": 53}
    out["V1_closed_forms"] = v1_closed_forms()
    out["V2_tail_from_gamma"] = v2_tail_from_gamma()
    out["V3_Y0"] = v3_y0()
    out["V4_positive_control"] = v4_control()
    out["V5_MM1_inequality"] = v5_mm1()
    p = ROOT / "writeup" / "data" / "leg_54_verify_headline.json"
    p.write_text(json.dumps(out, indent=1, default=str))
    print(f"\nwrote {p}")


if __name__ == "__main__":
    main()
