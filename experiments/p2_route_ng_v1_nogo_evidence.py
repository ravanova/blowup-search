"""Phase-2 Route-NG v1 (fig55): the no-go is a THEOREM on every block-upper-triangular
approximate inverse, and a MEASUREMENT everywhere else.

Legs 51-57 held every part of a negative result and assembled none of them.  Leg 54 spent
the last free choice -- the shape of `A` -- over seven shapes and bottomed at `Z1 = 8.9591`
against a block-diagonal baseline of `10.4584`.  That is a battery, not a theorem, and "no
`A` we tried" is not "no `A`".

This leg names the class where it IS a theorem.  The tail block's far-field kernel `h`
satisfies `T h = 0` and, decaying like `m^-2`, lies IN `l^1_w` for every `s < 1` -- which
includes both classes legs 51-54 used.  Testing `I - A L` on `(0; h)` kills the `A12` term
and the `A22` term outright, so for every `A` with `A21 = 0`

    Z1 >= 1 + ||A11 B h||_w / ||h||_w >= 1,

at every split `K` and with `A11`, `A12`, `A22` otherwise arbitrary.  That class strictly
contains the block-diagonal `A` the method conventionally uses, and it contains leg 54's
`gs_upper` shape.  It does NOT contain `gs_lower`, `schur` or `ff_lift`: those have
`A21 != 0`, the rank-one far-field lift buys back exactly the kernel's own unit
contribution, and beyond that the repository has the battery and nothing else.

Rebuild fig55 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_ng_v1_nogo_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_ng_v1_nogo.py

Six panels: A the hypothesis (H2) -- the kernel's `l^1_w` partial norms settle for s < 1
and grow for s >= 1; B the bound against leg 54's battery, in-class shapes never below the
line `Z1 = 1`; C what `A21 != 0` buys, which is exactly 1.0000; D the split-placement
audit -- moving the far-field amplitude into the tail trades a kernel for an inverse norm
diverging at the SAME exponent; E the sharpness dial in `mu`, where the same class reaches
`Z1 < 1` once the hypothesis is removed; F proved vs measured, drawn to scale.
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
JSON = DATA / "p2_route_ng_v1_nogo.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79", "warn": "#e08a1e",
     "grey": "#888888", "ours": "#7b1fa2", "floor": "#00695c"}
IN_CLASS = ("block_diag", "gs_upper")
SHAPE_C = {"block_diag": "#c1440e", "gs_upper": "#1f4e79", "gs_lower": "#e08a1e",
           "schur": "#2e7d32", "ff_lift": "#7b1fa2", "oracle_pinv": "#888888",
           "exact_inv": "#444444"}
SHAPE_LBL = {"block_diag": "block diagonal", "gs_upper": "block GS (tail first)",
             "gs_lower": "block GS ($\\Gamma$ first)", "schur": "Schur complement",
             "ff_lift": "far-field lift (rank 1)", "oracle_pinv": "oracle $A_{12}$",
             "exact_inv": "exact inverse"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, axes = plt.subplots(2, 3, figsize=(16.5, 9.6))
    fig.suptitle(
        "Route-NG (leg 58): the no-go is a THEOREM for every block-upper-triangular "
        "approximate inverse ($A_{21}=0$),\nand a MEASUREMENT for every other shape "
        "-- on the $a=0$ CLM linearisation",
        fontsize=13.5, y=0.985)

    # ---- A  the hypothesis (H2) -----------------------------------------
    ax = axes[0, 0]
    for row in d["NG2a_kernel_membership"]:
        s, ok = row["s"], row["in_l1_w"]
        ax.plot(row["M"], row["partial_norm"], "o-",
                color=(C["good"] if ok else C["bad"]),
                alpha=0.95 if ok else 0.65, lw=2.0 if ok else 1.4,
                label=f"$s={s:g}$  $r={row['last_increment_ratio']:.2f}$ "
                      + ("in $\\ell^1_w$" if ok else row["verdict"].replace("_", " ")))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("truncation $M$")
    ax.set_ylabel(r"partial $\|h\|_{\ell^1_w}$")
    ax.set_title("A. hypothesis (H2): is the tail kernel IN the space?\n"
                 "the discriminator is the increment ratio $r$, not a flat-looking curve",
                 fontsize=10.5)
    ax.legend(fontsize=7.5, loc="upper left")
    ax.grid(alpha=0.3)

    # ---- B  the bound against the battery -------------------------------
    ax = axes[0, 1]
    checks = d["NG2b_bound_vs_battery"]
    alg = [c for c in checks if c["class"] == "algebraic"]
    Ks = sorted({c["K"] for c in alg})
    for sh in ("block_diag", "gs_upper", "gs_lower", "schur", "ff_lift"):
        ys = [next((c["hhat_column"] for c in alg if c["K"] == K and c["shape"] == sh), np.nan)
              for K in Ks]
        ax.plot(Ks, ys, "o-" if sh in IN_CLASS else "s--", color=SHAPE_C[sh],
                lw=2.2 if sh in IN_CLASS else 1.3,
                ms=7 if sh in IN_CLASS else 5,
                mfc=SHAPE_C[sh] if sh in IN_CLASS else "none",
                label=SHAPE_LBL[sh] + (r"  ($A_{21}=0$)" if sh in IN_CLASS else ""))
    ax.axhline(1.0, color="k", lw=1.6)
    ax.text(Ks[0], 1.06, "$Z_1 = 1$: the proposition's floor", fontsize=8.5, va="bottom")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("split $K$")
    ax.set_ylabel(r"$\|(I-AL)(0;h)\|_w / \|h\|_w$")
    ax.set_title("B. the bound vs leg 54's battery (algebraic $s=0.3$)\n"
                 "filled = inside the proved class, where the bound is ATTAINED",
                 fontsize=10.5)
    ax.legend(fontsize=7.5, loc="upper left")
    ax.grid(alpha=0.3)

    # ---- C  what A21 != 0 buys ------------------------------------------
    ax = axes[0, 2]
    cr = d["NG2d_lift_credit"]
    for kind, col in (("flat", C["anchor"]), ("algebraic", C["ours"])):
        rows = [c for c in cr if c["class"] == kind]
        ax.plot([c["K"] for c in rows], [c["credit"] for c in rows], "o-", color=col,
                label=("flat $s=0$" if kind == "flat" else "algebraic $s=0.3$"))
    ax.axhline(1.0, color="k", ls=":", lw=1.6)
    lo, hi = d["NG2d_credit_range"]
    ax.text(0.03, 0.08,
            f"credit over the whole sweep: {lo:.4f} .. {hi:.4f}\n"
            f"1 on the infinite tail; short at finite $M$ by\n"
            f"at most {d['NG2d_max_deficit_from_one']:.4f} = "
            f"{d['NG2d_max_deficit_over_rho']:.3f}$\\times\\rho_M$",
            transform=ax.transAxes, fontsize=8.5,
            bbox=dict(fc="white", ec=C["grey"], alpha=0.9))
    ax.set_xscale("log", base=2)
    ax.set_ylim(0.0, 1.35)
    ax.set_xlabel("split $K$")
    ax.set_ylabel("column removed by the rank-one lift")
    ax.set_title("C. where the proof stops: $A_{21}\\neq 0$ buys back\n"
                 "ONE unit -- the kernel's own contribution -- and no more", fontsize=10.5)
    ax.legend(fontsize=8.5)
    ax.grid(alpha=0.3)

    # ---- D  the split-placement audit -----------------------------------
    ax = axes[1, 0]
    for a in d["NG2c_alternative_split"]:
        lbl = "flat $s=0$" if a["class"] == "flat" else f"algebraic $s={a['param']:g}$"
        col = C["anchor"] if a["class"] == "flat" else C["ours"]
        xs = [r["M_minus_K"] for r in a["ladder"]]
        ax.plot(xs, [r["alt_tail_inverse_norm"] for r in a["ladder"]], "o-", color=col,
                label=lbl + f"  $\\|T'^{{-1}}\\|\\sim M^{{{a['fitted_exponent']:+.2f}}}$")
    for dd in d["NG2a_finite_M_defect"]:
        col = C["anchor"] if dd["class"] == "flat" else C["ours"]
        xs = [r["M_minus_K"] for r in dd["ladder"]]
        ax.plot(xs, [r["rho"] for r in dd["ladder"]], "s--", color=col, alpha=0.6,
                label=f"$\\rho_M\\sim M^{{{dd['fitted_exponent']:+.2f}}}$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("tail size $M-K$")
    ax.set_ylabel("norm")
    ax.set_title("D. the split-placement audit: moving the amplitude into\n"
                 "the tail trades a kernel for a DIVERGING inverse, same exponent",
                 fontsize=10.5)
    ax.legend(fontsize=7.5, loc="center left")
    ax.grid(alpha=0.3)

    # ---- E  the sharpness dial ------------------------------------------
    ax = axes[1, 1]
    dial = [r for r in d["NG3_sharpness_dial"] if r["class"] == "algebraic"]
    mus = [r["mu"] for r in dial]
    x = np.arange(len(mus))
    for sh, col in (("block_diag", C["bad"]), ("gs_upper", C["anchor"])):
        ax.plot(x, [r["by_shape"][sh] for r in dial], "o-", color=col,
                label=SHAPE_LBL[sh] + r" ($A_{21}=0$)")
    ax.axhline(1.0, color="k", lw=1.6)
    ax.axvspan(-0.35, 0.35, color=C["bad"], alpha=0.10)
    ax.text(0.0, ax.get_ylim()[1], " $\\mu=0$: (H2) holds,\n the theorem FORBIDS $Z_1<1$",
            fontsize=8.5, va="top", ha="left")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{m:g}" for m in mus])
    ax.set_xlabel(r"dissipation $\mu$  ($\Lambda^1$)")
    ax.set_ylabel("$Z_1$ (true column-max)")
    ax.set_title("E. sharpness: remove the hypothesis and the SAME class\n"
                 "reaches $Z_1<1$ -- so the control can report the other answer",
                 fontsize=10.5)
    ax.legend(fontsize=8.5, loc="lower left")
    ax.grid(alpha=0.3)

    # ---- F  proved vs measured ------------------------------------------
    ax = axes[1, 2]
    ax.axis("off")
    best_ctrl = d["NG3_best_in_class_control_Z1"]
    txt = (
        "PROVED (this leg)\n"
        r"   class $A_{21}=0$: block-diagonal, $gs\_upper$," "\n"
        "   and every $A_{12}$, $A_{22}$ whatsoever\n"
        f"   $Z_1 \\geq 1 + \\|A_{{11}}Bh\\|_w/\\|h\\|_w$   at every $K$, every $s<1$\n"
        f"   in-class minimum over the sweep: "
        f"{d['NG2b_in_class_min_hhat_column']:.4f}   (forbidden below 1)\n"
        f"   deviation from the infinite-tail equality:\n"
        f"   {d['NG2b_max_deviation_over_truncation_budget']:.4f}x the truncation budget\n\n"
        "MEASURED, NOT PROVED (leg 54's battery)\n"
        r"   every $A$ with $A_{21}\neq 0$: $gs\_lower$, Schur, lift" "\n"
        "   best admissible $Z_1 = 8.9591$ vs baseline $10.4584$\n"
        "   (1.167x, where more than 8x was needed)\n\n"
        "SHARP\n"
        f"   $\\mu>0$ removes the kernel; the same class reaches\n"
        f"   $Z_1 = {best_ctrl:.4f}$\n\n"
        "NOT CLAIMED\n"
        "   the dominance observation (folklore in print),\n"
        "   the $m^{-2}$ decay and $s<1$ threshold (leg 51),\n"
        "   the shapes (textbook preconditioning),\n"
        "   anything about HL_S2_nonsymmetric or L1$\\to$L4")
    ax.text(0.0, 1.0, txt, transform=ax.transAxes, fontsize=9.6, va="top", family="monospace")
    ax.set_title("F. the scope line, which is load-bearing", fontsize=10.5)

    fig.tight_layout(rect=(0, 0, 1, 0.955))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig55_route_ng_v1_nogo.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out.relative_to(ROOT)}")
    return d


def restate(d):
    """Every number the prose quotes, re-read from the committed JSON."""
    print("\nRoute-NG v1 -- the claims, restated from the JSON")
    print(f"  gate                        : {d['gate_answer']}")
    print(f"  named class                 : {d['gate_named_class']}")
    print(f"  in-class min hhat-column    : {d['NG2b_in_class_min_hhat_column']:.4f} "
          f"(the proposition says >= 1)")
    print(f"  finite-M bound min slack    : {d['NG2b_finite_M_bound_min_slack']:.3e} "
          f"(never violated: {d['NG2b_finite_M_bound_never_violated']})")
    print(f"  deviation / truncation budget: "
          f"{d['NG2b_max_deviation_over_truncation_budget']:.4f}")
    print(f"  instrument vs leg 54        : "
          f"block_diag {d['NG2b_instrument_check_vs_leg54']['block_diag_baseline_here']:.4f} "
          f"(banked 10.4584), ff_lift "
          f"{d['NG2b_instrument_check_vs_leg54']['ff_lift_best_here']:.4f} (banked 8.9591)")
    print(f"  lift credit                 : {d['NG2d_credit_range'][0]:.4f} .. "
          f"{d['NG2d_credit_range'][1]:.4f}")
    print(f"  alt-split max ||T'^-1||_w   : {d['NG2c_max_alt_tail_inverse_norm']:.4g}")
    print(f"  sharpness: best in-class Z1 : {d['NG3_best_in_class_control_Z1']:.4f} "
          f"at mu >= {d['NG3_smallest_mu_with_in_class_Z1_below_one']:g}")
    print(f"  mu=2 algebraic, column-max  : {d['NG3_mu2_algebraic_column_max']:.4f} "
          f"(leg 54's convention)")
    print(f"  mu=2 algebraic, subblock sum: {d['NG3_mu2_algebraic_subblock_sum']:.4f} "
          f"(leg 53's convention)")
    print(f"  H2 holds for s              : {d['NG2a_H2_holds_for_s']}")
    print(f"  H2 fails for s              : {d['NG2a_H2_fails_for_s']}")


if __name__ == "__main__":
    restate(build_figure())
