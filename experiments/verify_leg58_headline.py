"""VER-A for leg 58: independent re-derivation of leg 54's headline numbers.

Trigger (a), lesson 85: re-measure a headline BEFORE the leg that consumes it builds
further on it.  Leg 58's proposition leans on three numbers from leg 54:

    best admissible Z1 over every shape/class/gauge/split  =  8.9591  (ff_lift, s=0.3, K=2)
    block-diagonal baseline                                = 10.4584
    MM-1's inequality is an EXACT equality                 =  1.89e-15 deviation

This script does NOT import leg 54's runner (`p2_route_mm_v1_shape.py`) or leg 53's
assembler (`p2_route_tc_v1_assemble.py`).  It rebuilds the assembled operator from the
primitives in `solver/spectral_certificate.py` alone -- so an error in either leg's
assembly code shows up here as a disagreement rather than being inherited.

Four checks:

  VER1  STRUCTURE.  The assembled `L` must be a partition of the honest linearization
        `bordered_linearization(M)` (modes 1..M + gauge + delta c_omega), augmented by
        the far-field column `L hhat` and its matching row.  Every entry of the four
        blocks G/B/C/T is checked against that global matrix.  This is the check that
        leg 54's hand-written coupling blocks `Ltg`/`Lgt` are the operator's and not a
        transcription.
  VER2  BATTERY.  block_diag and ff_lift re-measured as the true column-max of I - A L
        over every class / gauge / even split, from my own assembly.  Reports the best
        admissible Z1 and the block-diagonal baseline.
  VER3  MM-1.  The inequality's RHS recomputed from its three stated factors, against
        the measured (tail,Gamma) sub-block norm, over every split in the sweep -- and
        the K-restriction under which the RHS actually clears 1.
  VER4  TRUNCATION.  Is the headline an artifact of M_extra = 1024?  Re-run at 512 and
        2048.

Writes nothing to the ledger; prints, and dumps JSON next to itself for the record.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.spectral_certificate import (                              # noqa: E402
    bordered_linearization, tail_block, tail_left_null, tail_right_null,
)

CLASSES = (("flat", 0.0), ("algebraic", 0.3))
K_EVEN = (2, 4, 6, 8, 16, 32, 64)
M_EXTRA = 1024


def w(k, kind, param):
    k = np.asarray(k, dtype=float)
    return np.ones_like(k) if kind == "flat" else (1.0 + k) ** float(param)


def colmax(Mx):
    """Induced norm of the weighted-l1 space in the scaled coordinates = max abs colsum."""
    Mx = np.abs(np.asarray(Mx, dtype=float))
    return float(np.max(Mx.sum(0))) if Mx.size else 0.0


# --------------------------------------------------------------------------
# my own assembly, from solver/ primitives only
# --------------------------------------------------------------------------
def assemble(K, M, kind, param, gauge="null", mu=0.0):
    """`L` in scaled coordinates as blocks [[G,B],[C,T]].

    Unknowns / columns : b_1..b_K | delta c_omega | a (far-field amplitude) || modes K+1..M
    Equations  / rows  : modes 1..K | gauge | matching                      || modes K+1..M
    """
    K, M = int(K), int(M)
    n = M - K
    hh_raw = tail_right_null(K, M)                    # kernel of the tail block
    m = np.arange(K + 1, M + 1, dtype=float)

    # --- the finite block, built from the K-mode bordered linearization -------------
    F = bordered_linearization(K, mu=mu)              # (K+1)x(K+1): modes 1..K + gauge row
    N = K + 2
    G = np.zeros((N, N))
    G[:K + 1, :K + 1] = F
    # the far-field column: (L hhat) restricted to the finite rows.
    G[K - 1, K + 1] += (K + 1) / 2.0 * hh_raw[0]      # col K+1's k/2 entry lands in row K
    G[0, K + 1] += float(np.sum(-((-1.0) ** m) * hh_raw))   # the rank-one H*Omega term
    if gauge == "dilation":
        G[K, K + 1] = float(np.sum(m * hh_raw))
    elif gauge == "null":
        G[K, :] = 0.0
        G[K, 1] = 1.0                                  # pin b_2, the exact null direction
    else:
        raise ValueError(gauge)
    G[K + 1, K + 1] = 1.0                              # matching row

    wk = w(np.arange(1, K + 1), kind, param)
    wt = w(m, kind, param)
    Wa = float(np.sum(wt * np.abs(hh_raw)))            # "shipped" normalisation
    rho = float(w([K + 1], kind, param)[0])
    w_col = np.concatenate([wk, [1.0], [Wa]])
    w_row = np.concatenate([wk, [1.0], [rho]])
    Gs = G * (w_row[:, None] / w_col[None, :])

    # --- the coupling blocks ---------------------------------------------------------
    T_raw = tail_block(K, M, mu=mu)
    Ltg = np.zeros((n, N))
    Ltg[0, K - 1] = 1.0 - K / 2.0                      # mode K feeds tail row K+1
    Ltg[:, K + 1] = T_raw @ hh_raw                     # the amplitude column's tail rows
    C = (Ltg * wt[:, None]) / w_col[None, :]

    Lgt = np.zeros((N, n))
    Lgt[K - 1, 0] += (K + 1) / 2.0                     # mode K+1 feeds residual row K
    Lgt[0, :] += -((-1.0) ** m)                        # every tail mode feeds row 1
    if gauge == "dilation":
        Lgt[K, :] += m
    Lgt[K + 1, 0] += -1.0                              # matching row reads b_{K+1}
    B = (Lgt * w_row[:, None]) / wt[None, :]

    T = T_raw * (wt[:, None] / wt[None, :])

    # --- A_tail: the BORDERED inverse of the scaled tail -----------------------------
    v = tail_right_null(K, M) * wt
    u = tail_left_null(K, M) * wt
    v, u = v / np.linalg.norm(v), u / np.linalg.norm(u)
    Bd = np.zeros((n + 1, n + 1))
    Bd[:n, :n] = T
    Bd[:n, n] = u
    Bd[n, :n] = v
    A_t = np.linalg.inv(Bd)[:n, :n]

    hh = hh_raw * wt
    hh = hh / float(np.sum(np.abs(hh)))
    # Gamma^-1 is NOT formed here: leg 54 reports every ODD split has an exactly singular
    # augmented finite block, so `assemble` must survive one.  MM-1 (VER3) needs only A_t
    # and C, so the inversion is deferred to whoever actually asks for it.
    sv = float(np.linalg.svd(Gs, compute_uv=False)[-1])
    ob = {"G": Gs, "B": B, "C": C, "T": T, "A_t": A_t, "hhat": hh, "nG": N, "n": n,
          "K": K, "M": M, "wt": wt, "w_row": w_row, "w_col": w_col,
          "smallest_sv_of_Gamma": sv, "L": np.block([[Gs, B], [C, T]])}
    if sv > 1e-13:
        ob["Gi"] = np.linalg.inv(Gs)
    return ob


def build_A(ob, shape):
    G, B, C, T, A_t, Gi = ob["G"], ob["B"], ob["C"], ob["T"], ob["A_t"], ob["Gi"]
    nG, n = ob["nG"], ob["n"]
    Z, Zt = np.zeros((nG, n)), np.zeros((n, nG))
    if shape == "block_diag":
        return np.block([[Gi, Z], [Zt, A_t]])
    if shape == "gs_lower":
        return np.block([[Gi, Z], [-A_t @ C @ Gi, A_t]])
    if shape == "gs_upper":
        return np.block([[Gi, -Gi @ B @ A_t], [Zt, A_t]])
    if shape == "schur":
        Si = np.linalg.inv(G - B @ A_t @ C)
        return np.block([[Si, -Si @ B @ A_t],
                         [-A_t @ C @ Si, A_t + A_t @ C @ Si @ B @ A_t]])
    if shape == "ff_lift":
        # rank-one lift of the far field back into the tail rows.  Unlike leg 54 I score
        # every candidate on the TRUE full residual, not on a shortcut that assumes the
        # top block is untouched -- if that assumption were wrong this would catch it.
        v = B @ ob["hhat"]
        best, bestz = None, np.inf
        cands = {"e_rowK": np.eye(nG)[max(0, nG - 3)], "e_row1": np.eye(nG)[0],
                 "lstsq": v / max(float(np.dot(v, v)), 1e-300),
                 "GiT": (Gi.T @ Gi) @ v}
        for _, uu in cands.items():
            d = float(np.dot(uu, v))
            if abs(d) < 1e-13:
                continue
            A = np.block([[Gi, Z], [np.outer(ob["hhat"], uu / d), A_t]])
            z = colmax(np.eye(nG + n) - A @ ob["L"])
            if z < bestz:
                best, bestz = A, z
        return best
    raise ValueError(shape)


ADMISSIBLE = ("block_diag", "gs_lower", "gs_upper", "schur", "ff_lift")


def measure(ob, shape):
    A = build_A(ob, shape)
    if A is None:
        return None
    nG = ob["nG"]
    R = np.eye(ob["nG"] + ob["n"]) - A @ ob["L"]
    return {"Z1": colmax(R), "Z1_GG": colmax(R[:nG, :nG]), "Z1_Gt": colmax(R[:nG, nG:]),
            "Z1_tG": colmax(R[nG:, :nG]), "Z1_tt": colmax(R[nG:, nG:])}


# --------------------------------------------------------------------------
def ver1_structure(res):
    """Every block of the assembled L must come from bordered_linearization(M)."""
    print("\n[VER1] STRUCTURE: assembled L vs bordered_linearization(M), unscaled")
    worst = 0.0
    for K in (2, 4, 6, 8):
        M = K + 64
        FM = bordered_linearization(M)                 # rows modes 1..M + gauge; cols b + dc
        ob = assemble(K, M, "flat", 0.0, gauge="dilation")
        # undo the scaling to compare against the raw operator
        Graw = ob["G"] * (ob["w_col"][None, :] / ob["w_row"][:, None])
        Braw = ob["B"] * (ob["wt"][None, :] / ob["w_row"][:, None])
        Craw = ob["C"] * (ob["w_col"][None, :] / ob["wt"][:, None])
        Traw = ob["T"]
        d = []
        # (modes 1..K) x (b_1..b_K, delta c_omega)
        d.append(np.max(np.abs(Graw[:K, :K] - FM[:K, :K])))
        d.append(np.max(np.abs(Graw[:K, K] - FM[:K, M])))
        # (modes 1..K) x (tail modes K+1..M)
        d.append(np.max(np.abs(Braw[:K, :] - FM[:K, K:M])))
        # (tail modes) x (b_1..b_K, delta c_omega)
        d.append(np.max(np.abs(Craw[:, :K] - FM[K:M, :K])))
        d.append(np.max(np.abs(Craw[:, K] - FM[K:M, M])))
        # (tail modes) x (tail modes)
        d.append(np.max(np.abs(Traw - FM[K:M, K:M])))
        # the gauge row over b_1..b_K and over the tail
        d.append(np.max(np.abs(Graw[K, :K] - FM[M, :K])))
        d.append(np.max(np.abs(Braw[K, :] - FM[M, K:M])))
        # the far-field column IS L applied to hhat (finite rows and tail rows)
        hh = tail_right_null(K, M)
        full_h = np.concatenate([np.zeros(K), hh, [0.0]])
        Lh = FM @ full_h
        d.append(abs(Graw[K - 1, K + 1] + Graw[0, K + 1]
                     - (Lh[K - 1] + Lh[0])))
        d.append(np.max(np.abs(Craw[:, K + 1] - Lh[K:M])))
        dm = float(max(d))
        worst = max(worst, dm)
        print(f"      K={K:3d} M={M:4d}: max |assembled - bordered_linearization| = {dm:.2e}")
    res["VER1_max_structural_deviation"] = worst
    res["VER1_pass"] = bool(worst < 1e-12)
    print(f"      worst over all splits: {worst:.2e}  ->  "
          f"{'STRUCTURE CONFIRMED' if worst < 1e-12 else 'STRUCTURE MISMATCH'}")


def ver2_battery(res, m_extra=M_EXTRA, key="VER2"):
    print(f"\n[{key}] BATTERY: true column-max of I - A L, M_extra = {m_extra}")
    rows = []
    for kind, p in CLASSES:
        for gauge in ("dilation", "null"):
            for K in K_EVEN:
                ob = assemble(K, K + m_extra, kind, p, gauge=gauge)
                by = {sh: measure(ob, sh) for sh in ADMISSIBLE}
                rows.append({"class": kind, "param": p, "gauge": gauge, "K": K,
                             "by_shape": by})
                print(f"      {kind:9s} s={p:.1f} {gauge:8s} K={K:3d}: " +
                      "  ".join(f"{sh[:9]}={by[sh]['Z1']:9.4g}" for sh in ADMISSIBLE))
    flat = [(r, sh, m) for r in rows for sh, m in r["by_shape"].items()]
    best = min(flat, key=lambda t: t[2]["Z1"])
    bd = min((r for r in rows), key=lambda r: r["by_shape"]["block_diag"]["Z1"])
    res[f"{key}_best_admissible"] = {
        "Z1": best[2]["Z1"], "shape": best[1], "class": best[0]["class"],
        "param": best[0]["param"], "gauge": best[0]["gauge"], "K": best[0]["K"],
        "subblocks": {k: v for k, v in best[2].items() if k != "Z1"}}
    res[f"{key}_block_diagonal_baseline"] = {
        "Z1": bd["by_shape"]["block_diag"]["Z1"], "class": bd["class"],
        "param": bd["param"], "gauge": bd["gauge"], "K": bd["K"]}
    res[f"{key}_improvement_factor"] = (bd["by_shape"]["block_diag"]["Z1"]
                                        / best[2]["Z1"])
    print(f"      BEST ADMISSIBLE Z1 = {best[2]['Z1']:.6f}  "
          f"({best[1]}, {best[0]['class']} s={best[0]['param']}, "
          f"{best[0]['gauge']}, K={best[0]['K']})")
    print(f"      BLOCK-DIAG BASELINE = {bd['by_shape']['block_diag']['Z1']:.6f}  "
          f"({bd['class']} s={bd['param']}, {bd['gauge']}, K={bd['K']})")
    print(f"      improvement factor  = {res[f'{key}_improvement_factor']:.6f}")
    return rows


def ver3_mm1(res):
    print("\n[VER3] MM-1:  Z1 >= |1 - K/2| (w_{K+1}/w_K) ||A_tail e_{K+1}||_w / w_{K+1}")
    out = []
    for kind, p in CLASSES:
        for K in K_EVEN + (3, 5):
            M = K + M_EXTRA
            ob = assemble(K, M, kind, p)
            wK = float(w([K], kind, p)[0])
            wK1 = float(w([K + 1], kind, p)[0])
            e = np.zeros(ob["n"])
            e[0] = 1.0
            second = float(np.sum(np.abs(ob["A_t"] @ e)))   # = ||A_tail e_{K+1}||_w/w_{K+1}
            rhs = abs(1.0 - K / 2.0) * (wK1 / wK) * second
            meas = colmax(ob["A_t"] @ ob["C"])              # the (tail,Gamma) block for A21=0
            ratio = (meas / rhs) if rhs > 0 else None
            out.append({"class": kind, "K": K, "rhs": rhs, "measured": meas,
                        "ratio": ratio, "second_factor": second,
                        "smallest_sv_of_Gamma": ob["smallest_sv_of_Gamma"]})
            print(f"      {kind:9s} s={p:.1f} K={K:3d}: RHS={rhs:10.5f}  "
                  f"measured={meas:10.5f}  ratio="
                  f"{ratio if ratio is not None else float('nan'):9.6f}"
                  f"{'   <-- VACUOUS (prefactor 0)' if rhs == 0 else ''}")
    tight = [r for r in out if r["ratio"] is not None]
    dev = float(max(abs(r["ratio"] - 1.0) for r in tight))
    res["VER3_max_ratio_deviation_from_one"] = dev
    res["VER3_is_an_equality"] = bool(dev < 1e-6)
    res["VER3_second_factor_range"] = [float(min(r["second_factor"] for r in out)),
                                       float(max(r["second_factor"] for r in out))]
    binding = {}
    for kind, p in CLASSES:
        cand = sorted(r["K"] for r in out if r["class"] == kind and r["rhs"] > 1.0)
        binding[kind] = cand[0] if cand else None
    res["VER3_smallest_K_with_rhs_above_one"] = binding
    res["VER3_rows"] = out
    odd = [r["smallest_sv_of_Gamma"] for r in out if r["K"] % 2 == 1]
    even = [r["smallest_sv_of_Gamma"] for r in out if r["K"] % 2 == 0]
    res["VER3_max_smallest_sv_at_odd_K"] = float(max(odd))
    res["VER3_min_smallest_sv_at_even_K"] = float(min(even))
    print(f"      leg 54's odd-split claim: max smallest-sv(Gamma) over ODD K = "
          f"{max(odd):.2e}; min over EVEN K = {min(even):.2e}")
    print(f"      max |ratio - 1| = {dev:.3e}   -> equality: {res['VER3_is_an_equality']}")
    print(f"      smallest K with RHS > 1: {binding}")
    print(f"      second factor range: {res['VER3_second_factor_range'][0]:.6f} .. "
          f"{res['VER3_second_factor_range'][1]:.6f}")


def ver4_truncation(res):
    print("\n[VER4] TRUNCATION: is the headline an artifact of M_extra = 1024?")
    tr = {}
    for me in (512, 2048):
        sub = {}
        ver2_battery(sub, m_extra=me, key=f"M{me}")
        tr[me] = {"best": sub[f"M{me}_best_admissible"]["Z1"],
                  "baseline": sub[f"M{me}_block_diagonal_baseline"]["Z1"],
                  "shape": sub[f"M{me}_best_admissible"]["shape"],
                  "K": sub[f"M{me}_best_admissible"]["K"]}
    res["VER4_truncation_ladder"] = tr
    for me, v in tr.items():
        print(f"      M_extra={me:5d}: best={v['best']:.6f} ({v['shape']}, K={v['K']})  "
              f"baseline={v['baseline']:.6f}")


def main():
    res = {"verifier": "VER-A", "leg": 58, "verifies": 54,
           "claimed": {"best_admissible_Z1": 8.9591, "block_diag_baseline": 10.4584,
                       "MM1_equality_deviation": 1.89e-15,
                       "MM1_scope": "K >= 6 flat / K >= 4 algebraic"}}
    ver1_structure(res)
    ver2_battery(res)
    ver3_mm1(res)
    ver4_truncation(res)

    print("\n================ VERDICT ================")
    b = res["VER2_best_admissible"]["Z1"]
    d = res["VER2_block_diagonal_baseline"]["Z1"]
    print(f"  best admissible Z1 : claimed 8.9591   measured {b:.6f}   "
          f"rel diff {abs(b - 8.9591) / 8.9591:.2e}")
    print(f"  block-diag baseline: claimed 10.4584  measured {d:.6f}   "
          f"rel diff {abs(d - 10.4584) / 10.4584:.2e}")
    print(f"  MM-1 equality dev  : claimed 1.89e-15 measured "
          f"{res['VER3_max_ratio_deviation_from_one']:.2e}")
    out = Path(__file__).with_name("verify_leg58_headline.json")
    out.write_text(json.dumps(res, indent=1, default=float))
    print(f"  written: {out}")


if __name__ == "__main__":
    main()
