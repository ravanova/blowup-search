"""Phase-2 Route-MM v1 (fig49): the last free choice was the SHAPE of the approximate
inverse, and spending it is worth 1.4x where 45x was needed.

Leg 53 assembled the bordered certificate with the block-diagonal approximate inverse the
method requires and the polynomial did not close: the coupling sub-block `Z1[Gamma<-tail]`
came out 43.15 at the best split against the 1 it must be under.  Four of the five degrees
of freedom were already measured and banned.  This leg spends the fifth -- the shape of `A`
-- across seven shapes, and finds a real but far-too-small improvement with a
SHAPE-INDEPENDENT floor underneath it: the tail operator is singular on exactly the
far-field direction the certificate borders, so along that direction the coupling collapses
to `Gamma^-1` applied to the far-field column, and the off-diagonal block of `A` drops out
of the algebra entirely.

Rebuild fig49 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_mm_v1_shape_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_mm_v1_shape.py

Six panels: A the shape battery at the best split, against the line Z_1 = 1; B Z_1 against
the split K for every shape and both admissible classes; C MM-1, which is measured to be an
EQUALITY, with the small-K region where its RHS drops below 1 marked and the odd splits
marked singular; D MM-4, the shape-independent floor; E MM-3, the admissibility audit that
disqualifies the exact inverse; F MM-5, the positive control that CAN report the other
answer.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "writeup" / "data"
FIGS = ROOT / "writeup" / "figures"
JSON = DATA / "p2_route_mm_v1_shape.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79", "warn": "#e08a1e",
     "grey": "#888888", "ours": "#7b1fa2", "floor": "#00695c"}
SHAPE_C = {"block_diag": "#c1440e", "gs_lower": "#e08a1e", "gs_upper": "#1f4e79",
           "schur": "#2e7d32", "ff_lift": "#7b1fa2", "oracle_pinv": "#888888",
           "exact_inv": "#444444"}
SHAPE_LBL = {"block_diag": "block diagonal\n(leg 53)", "gs_lower": "block GS\n($\\Gamma$ first)",
             "gs_upper": "block GS\n(tail first)", "schur": "Schur\ncomplement",
             "ff_lift": "far-field\nlift (rank 1)", "oracle_pinv": "oracle $A_{12}$\n(NOT admissible)",
             "exact_inv": "exact inverse\n(NOT admissible)"}


def clabel(r):
    return "flat" if r["class"] == "flat" else f"s={r['param']:g}"


def build_figure():
    d = json.loads(JSON.read_text())
    battery = d["MM2_shape_battery"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the shape battery at the best admissible split ----------------
    a = ax[0, 0]
    ba = d["MM2_best_admissible"]
    row = next(r for r in battery if r["class"] == ba["class"] and r["K"] == ba["K"]
               and r["gauge"] == ba["gauge"] and r["param"] == ba["param"])
    shapes = [s for s in d["shapes"] if s in row["by_shape"]]
    vals = [max(row["by_shape"][s]["Z1"], 1e-10) for s in shapes]
    cols = [SHAPE_C[s] for s in shapes]
    hatch = ["" if row["by_shape"][s]["admissible"] else "///" for s in shapes]
    bars = a.bar(range(len(shapes)), vals, color=cols, alpha=0.88)
    for b, h in zip(bars, hatch):
        b.set_hatch(h)
        if h:
            b.set_edgecolor("white")
    a.axhline(1.0, color=C["good"], lw=2.0, ls="--")
    a.text(len(shapes) - 0.4, 1.35, r"$Z_1=1$: what a certificate needs",
           color=C["good"], fontsize=9, ha="right", fontweight="bold")
    a.axhline(d["MM4_min_floor"], color=C["floor"], lw=1.6, ls=":")
    a.text(-0.4, d["MM4_min_floor"] * 1.25,
           f"shape-independent floor {d['MM4_min_floor']:.2f}",
           color=C["floor"], fontsize=8.5)
    a.set_yscale("log")
    a.set_xticks(range(len(shapes)))
    a.set_xticklabels([SHAPE_LBL[s] for s in shapes], fontsize=7.5)
    for i, (v, s) in enumerate(zip(vals, shapes)):
        a.text(i, v * 1.5, f"{row['by_shape'][s]['Z1']:.3g}", ha="center", fontsize=8)
    a.set_ylabel(r"assembled $Z_1$   (log)")
    a.set_title(f"A  the shape battery at the best split\n"
                f"({clabel(ba)}, K={ba['K']}, gauge={ba['gauge']}) — hatched = NOT admissible",
                fontsize=10, fontweight="bold")

    # ---- B: Z_1 against the split, every shape ---------------------------
    b = ax[0, 1]
    for kind, ls in (("flat", "--"), ("algebraic", "-")):
        for sh in ("block_diag", "gs_upper", "schur", "oracle_pinv"):
            rows = sorted([r for r in battery if r["class"] == kind
                           and r["gauge"] == "null"], key=lambda r: r["K"])
            if not rows:
                continue
            b.plot([r["K"] for r in rows], [r["by_shape"][sh]["Z1"] for r in rows],
                   ls, marker="o", ms=3.5, color=SHAPE_C[sh], alpha=0.9,
                   label=f"{sh} ({clabel(rows[0])})" if kind == "algebraic" else None)
    b.axhline(1.0, color=C["good"], lw=2.0, ls="--")
    b.set_xscale("log", base=2)
    b.set_yscale("log")
    b.set_xlabel("split K")
    b.set_ylabel(r"assembled $Z_1$")
    b.legend(fontsize=7.5, loc="upper left")
    b.set_title("B  every shape grows with the split\n"
                "solid = algebraic s=0.3, dashed = flat; null gauge",
                fontsize=10, fontweight="bold")

    # ---- C: MM-1, an equality, and where its RHS stops binding ------------
    c = ax[1, 0]
    for kind, mk in (("flat", "s"), ("algebraic", "o")):
        rows = sorted([r for r in d["MM1_inequality"] if r["class"] == kind],
                      key=lambda r: r["K"])
        c.plot([r["K"] for r in rows], [max(r["rhs"], 1e-4) for r in rows],
               "-", marker=mk, ms=5, color=C["anchor"] if kind == "flat" else C["ours"],
               label=f"RHS of MM-1 ({clabel(rows[0])})")
        c.plot([r["K"] for r in rows],
               [max(r["measured_Z1_tail_Gamma"], 1e-4) for r in rows],
               "none", marker="x", ms=8, ls="none",
               color=C["bad"], label="measured (coincides: it is an EQUALITY)"
               if kind == "flat" else None)
    c.axhline(1.0, color=C["good"], lw=2.0, ls="--")
    c.axvspan(1.7, 4.3, color=C["warn"], alpha=0.16)
    c.text(2.0, 3e-3, "MM-1 does NOT bind here\n(prefactor |1-K/2| -> 0)",
           fontsize=8, color=C["warn"], fontweight="bold")
    for K in (3, 5, 7, 9, 11):
        c.axvline(K, color=C["grey"], lw=0.8, ls=":", alpha=0.7)
    c.text(6.5, 1e-3, "dotted: ODD K, finite block is SINGULAR", fontsize=7.5,
           color=C["grey"])
    c.set_xscale("log", base=2)
    c.set_yscale("log")
    c.set_xlabel("split K")
    c.set_ylabel(r"$Z_1[\mathrm{tail}\leftarrow\Gamma]$")
    c.legend(fontsize=7.5, loc="lower right")
    c.set_title("C  MM-1 is an EQUALITY, but it only bites for K>=4\n"
                "(the small-K corner is closed by MM-4, panel D)",
                fontsize=10, fontweight="bold")

    # ---- D: MM-4, the shape-independent floor ----------------------------
    e = ax[1, 1]
    for kind, mk in (("flat", "s"), ("algebraic", "o")):
        rows = sorted([r for r in d["MM4_floor"] if r["class"] == kind],
                      key=lambda r: r["K"])
        e.plot([r["K"] for r in rows], [r["floor_with_Gamma_inv_A11"] for r in rows],
               "-", marker=mk, ms=5, color=C["floor"] if kind == "flat" else C["ours"],
               label=f"floor, {clabel(rows[0])}")
        e.plot([r["K"] for r in rows], [r["floor_with_schur_A11"] for r in rows],
               ls="none", marker="+", ms=8, color=C["bad"],
               label="with the Schur A11 (ablation)" if kind == "flat" else None)
    e.axhline(1.0, color=C["good"], lw=2.0, ls="--")
    e.set_xscale("log", base=2)
    e.set_yscale("log")
    e.set_xlabel("split K")
    e.set_ylabel(r"$\|\Gamma^{-1} L\hat h\|_w/\|\hat h\|_w$")
    e.legend(fontsize=7.5, loc="upper left")
    e.set_title("D  MM-4: the floor no shape of A can cross\n"
                r"($\hat h$ spans $\ker T$, so $A_{12}$ drops out algebraically)",
                fontsize=10, fontweight="bold")

    # ---- E: MM-3, the admissibility audit --------------------------------
    f = ax[0, 2]
    for kind, mk in (("flat", "s"), ("algebraic", "o")):
        rows = sorted([r for r in d["MM3_admissibility_audit"]
                       if r["class"] == kind and r["M_L_extra"] == 1024],
                      key=lambda r: r["M_A_extra"])
        f.plot([r["M_A_extra"] for r in rows], [r["Z1"] for r in rows], "-",
               marker=mk, ms=5, color=C["bad"] if kind == "flat" else C["warn"],
               label=f"exact inverse made admissible ({clabel(rows[0])})")
    f.axhline(1.0, color=C["good"], lw=2.0, ls="--")
    f.axhline(d["MM2_block_diagonal_baseline"]["Z1"], color=C["anchor"], lw=1.5, ls="-.")
    f.text(140, d["MM2_block_diagonal_baseline"]["Z1"] * 1.4,
           f"block-diagonal baseline {d['MM2_block_diagonal_baseline']['Z1']:.1f}",
           fontsize=8, color=C["anchor"])
    f.set_xscale("log", base=2)
    f.set_yscale("log")
    f.set_xlabel(r"$M_A$: modes carried by the finite-rank part of $A$")
    f.set_ylabel(r"assembled $Z_1$")
    f.legend(fontsize=7.5, loc="lower right")
    f.set_title("E  MM-3: the exact inverse is the TRUNCATION, not a shape\n"
                r"(it reads $\sim\!10^{-9}$ in-sample; made admissible it is $10^4$ and rising)",
                fontsize=10, fontweight="bold")

    # ---- F: MM-5, the positive control ------------------------------------
    g = ax[1, 2]
    ctrl = d["MM5_positive_control"]
    for sh in ("block_diag", "gs_upper", "schur"):
        rows = sorted([r for r in ctrl if r["class"] == "algebraic" and r["mu"] > 0],
                      key=lambda r: r["mu"])
        g.plot([r["mu"] for r in rows], [max(r["by_shape"][sh], 1e-16) for r in rows],
               "-", marker="o", ms=4, color=SHAPE_C[sh], label=sh)
    g.axhline(1.0, color=C["good"], lw=2.0, ls="--")
    g.set_xscale("log")
    g.set_yscale("log")
    g.set_xlabel(r"dissipation $\mu$  ($\Lambda^1$, unbordered tail)")
    g.set_ylabel(r"assembled $Z_1$")
    g.legend(fontsize=8, loc="lower left")
    g.set_title("F  MM-5: the instrument CAN say yes\n"
                r"the same code path reaches $Z_1<1$ once the tail is a multiplier",
                fontsize=10, fontweight="bold")

    for row_ in ax:
        for a_ in row_:
            a_.grid(alpha=0.25, lw=0.6)

    fig.suptitle(
        "Route-MM v1 — spending the last free choice, the SHAPE of the approximate inverse: "
        f"{d['MM2_improvement_over_block_diagonal']:.2f}x where {d['MM2_block_diagonal_baseline']['Z1']:.0f}x was needed. "
        f"GATE: {d['gate_answer'].upper()}",
        fontweight="bold", fontsize=12.5, y=1.005)
    fig.tight_layout()
    out = FIGS / "fig49_route_mm_v1_shape.png"
    fig.savefig(out, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print(f"wrote {out}")

    # ---- the claims, rebuilt from the curated JSON alone ------------------
    print("\nCLAIMS REBUILT FROM writeup/data/p2_route_mm_v1_shape.json (no re-run):")
    print(f"  gate answer                                    : {d['gate_answer'].upper()}")
    print(f"  best admissible shape                          : {ba['shape']} "
          f"({clabel(ba)}, K={ba['K']}, gauge={ba['gauge']})")
    print(f"  smallest assembled Z_1, admissible shapes      : {ba['Z1']:.4f}")
    print(f"  block-diagonal baseline (leg 53's shape)       : "
          f"{d['MM2_block_diagonal_baseline']['Z1']:.4f}")
    print(f"  improvement from spending the shape            : "
          f"{d['MM2_improvement_over_block_diagonal']:.3f}x")
    print(f"  shape-independent floor (MM-4), smallest       : {d['MM4_min_floor']:.4f}")
    print(f"  MM-1 is an equality to                         : "
          f"{d['MM1_max_ratio_deviation_from_one']:.2e}")
    print(f"  MM-1's RHS first exceeds 1 at K                : "
          f"{d['MM1_smallest_K_with_rhs_above_one']}")
    print(f"  every odd split is singular                    : "
          f"{d['MM1b_every_odd_split_is_singular']} "
          f"(max smallest sv {d['MM1b_max_smallest_sv_at_odd_K']:.1e})")
    print(f"  admissibility audit, minimum Z_1               : "
          f"{d['MM3_min_Z1_over_audit']:.5g}")
    print(f"  positive control reaches Z_1 < 1               : "
          f"{d['MM5_control_can_report_below_one']} "
          f"(smallest mu {d['MM5_min_mu_with_Z1_below_one']})")
    print(f"  negative control fails for every shape         : "
          f"{d['MM5b_wrong_directions_are_worse_for_every_shape']} "
          f"(exceptions: {d['MM5b_shapes_where_a_wrong_border_is_BETTER']})")
    print(f"  any positive interval anywhere                 : "
          f"{any(p['has_positive_interval'] for p in d['MM6_polynomial'])}")


if __name__ == "__main__":
    build_figure()
