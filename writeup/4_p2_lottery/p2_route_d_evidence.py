"""Phase-2 P2 Route-D v1 (fig19) evidence: the interval-arithmetic core + the a=0
operator-framing scoping probe. Level-1 tooling toward a Level-2 (computer-assisted
certification) attempt -- NOT a certificate.

Rebuilds fig19 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/p2_route_d_evidence.py
Regenerate the underlying data (deterministic; ~10 s):
    .venv/bin/python experiments/p2_route_d_probe.py

Four panels (fig19):
  A. ARITHMETIC PRECISION (Q1): the rigorous interval enclosure of the two-scale
     residual at the exact a=0 anchor -- enclosure width 8.5e-11 vs the 8.9e-10
     defect (a small overhead) -- and the sup|R2| growth over a genome box (slope
     1). The interval core is precise enough to carry a Newton-Kantorovich defect.
  B. DEGENERACY COUNT (Q2): singular values of the finite genome-map Jacobian.
     Gauge-slaved c_tw -> BOTH tiny (2-dim kernel = the amplitude+dilation scaling
     valley); fixing c_tw removes ONE -> 1-dim kernel. So exactly TWO gauge
     conditions isolate a nondegenerate zero.
  C. DIAGONALIZATION (Q3): under X = tan(theta/2) the LINE Hilbert transform equals
     the CIRCULAR conjugate (cos k.theta -> sin k.theta), verified to ~1e-7 for
     k=1..6 on the decaying subspace. The anchor is then a 2-term Fourier object.
  D. BANDED OPERATOR (Q4): the linearized operator DF at the anchor in the
     cos->sin Fourier basis is TRIDIAGONAL + a rank-1 c_tw column -- the structural
     reason the finite-section NK bounds Z0+Z1<1 are plausible.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_route_d_probe.json"


def build_figure():
    d = json.loads(JSON.read_text())
    q1, q2, q3, q4 = (d["q1_arithmetic_precision"], d["q2_degeneracy"],
                      d["q3_diagonalization"], d["q4_operator_structure"])

    fig, ax = plt.subplots(2, 2, figsize=(12.8, 9.6))
    C = {"anchor": "#1f4e79", "box": "#c1440e", "ok": "#2e7d32", "warn": "#e08a1e"}

    # -- Panel A: arithmetic precision + genome-box growth -------------------
    axA = ax[0, 0]
    radii = np.array([b["radius"] for b in q1["genome_box"]])
    sups = np.array([b["sup_R2_over_box"] for b in q1["genome_box"]])
    axA.loglog(radii, sups, "o-", color=C["box"], lw=2, ms=8, label="sup|R2| over genome box")
    axA.loglog(radii, sups[0] * (radii / radii[0]), "--", color="#999", lw=1,
               label="slope 1 (Lipschitz)")
    axA.axhline(q1["defect_inf"], color=C["anchor"], lw=1.6, ls=":",
                label=f"point defect = {q1['defect_inf']:.1e}")
    axA.axhline(q1["enclosure_width"], color=C["ok"], lw=1.6, ls="-.",
                label=f"interval width = {q1['enclosure_width']:.1e}")
    axA.set_xlabel("genome box radius r"); axA.set_ylabel("sup |R2|")
    axA.set_title(f"A. Rigorous R2 enclosure at the a=0 anchor\n"
                  f"arithmetic overhead = width/defect = {q1['overhead_ratio']:.2f}"
                  f"  (<< 1  -> carries NK defect Y0)", fontsize=10)
    axA.legend(fontsize=8, loc="upper left"); axA.grid(alpha=0.3, which="both")

    # -- Panel B: degeneracy count ------------------------------------------
    axB = ax[0, 1]
    gs = q2["gauge_slaved"]["sigma"]; fc = q2["fixed_ctw_half"]["sigma"]
    xpos = np.array([0, 1, 3, 4])
    vals = [gs[0], gs[1], fc[0], fc[1]]
    colors = [C["warn"], C["warn"], C["anchor"], C["ok"]]
    axB.bar(xpos, vals, color=colors, width=0.8)
    axB.set_yscale("log")
    axB.set_xticks([0.5, 3.5])
    axB.set_xticklabels(["gauge-slaved c_tw\n(kernel dim 2)", "fixed c_tw = 1/2\n(kernel dim 1)"])
    axB.axhline(1e-4 * q2["reference_scale"], color="#c00", ls="--", lw=1,
                label="kernel threshold (1e-4 x O(1) scale)")
    for x, v in zip(xpos, vals):
        axB.text(x, v * 1.4, f"{v:.1e}", ha="center", fontsize=7.5, rotation=0)
    axB.set_ylabel("singular value")
    axB.set_title("B. Linearization degeneracy: the scaling valley\n"
                  "both tiny (2-dim kernel) -> fix speed -> one O(1) + one tiny (1-dim)",
                  fontsize=10)
    axB.legend(fontsize=8, loc="center right"); axB.grid(alpha=0.3, axis="y")

    # -- Panel C: circular-Hilbert diagonalization --------------------------
    axC = ax[1, 0]
    labels = ["anchor\n(k=1)"] + ["".join(f"{k}" for k in pm["modes"]) for pm in q3["per_mode"]]
    errs = [q3["anchor_rel_err"]] + [pm["rel_err"] for pm in q3["per_mode"]]
    xc = np.arange(len(errs))
    axC.bar(xc, errs, color=C["anchor"], width=0.65)
    axC.axhline(1e-6, color="#999", ls="--", lw=1, label="discretization floor ~1e-6")
    axC.set_yscale("log"); axC.set_xticks(xc)
    axC.set_xticklabels(labels, fontsize=8)
    axC.set_ylabel("rel. sup-error  H_line vs circular conjugate")
    axC.set_title("C. Line Hilbert = circular conjugate under X=tan(theta/2)\n"
                  "cos k.theta -> sin k.theta on the decaying subspace (k=1..6)",
                  fontsize=10)
    axC.legend(fontsize=8); axC.grid(alpha=0.3, axis="y")

    # -- Panel D: banded + rank-1 linearized operator -----------------------
    axD = ax[1, 1]
    B = np.array(q4["B_cos_to_sin"])                 # rows sin m=1..N, cols cos k=0..N
    dcol = np.array(q4["dc_column"]).reshape(-1, 1)  # rank-1 c_tw column (sin modes)
    M = np.abs(np.hstack([B, dcol]))
    im = axD.imshow(M, cmap="magma", aspect="auto")
    axD.axvline(B.shape[1] - 0.5, color="w", lw=2)
    axD.set_xlabel("domain: cos(k.theta) coeffs  |  d/dc_tw")
    axD.set_ylabel("range: sin(m.theta) coeffs")
    axD.set_title(f"D. DF at the anchor: tridiagonal (bandwidth {q4['bandwidth']}) "
                  f"+ rank-1 c_tw col\ngrid cross-check {q4['grid_crosscheck_max_mismatch']:.1e} "
                  f"(the flagged theta=+-pi endpoint correction)", fontsize=10)
    fig.colorbar(im, ax=axD, fraction=0.046, pad=0.04, label="|matrix entry|")

    fig.suptitle("P2 Route-D v1 -- interval core + a=0 Newton-Kantorovich framing "
                 "(Level-1 tooling + scoping, NOT a certificate)", fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    out = FIGS / "fig19_p2_route_d.png"
    fig.savefig(out, dpi=130)
    print(f"[fig] wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    build_figure()
