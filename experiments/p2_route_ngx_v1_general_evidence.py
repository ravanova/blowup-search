"""Phase-2 Route-NGX v1 (fig63): the general class `A21 != 0` is decided, and the wall is a
property of the SPACE and not of the operator.

Leg 58 proved `Z1 >= 1` on `A21 = 0` by testing one direction and watching `T h = 0` kill the
`A12` and `A22` terms; the argument stopped at `A21 != 0`, where the surviving term
`h - A21 B h` can be cancelled.  Leg 127 closes the general class with an argument that never
splits `A` into blocks at all: in weighted `l^1` at `s < 1` the assembled bordered operator is
NOT BOUNDED BELOW, `sigma_min = 1/||L^-1||_w` falls like `M^-(1-s)`, and the folklore bound
`Z1 >= 1 - ||A||_w sigma_min` -- which is ATTAINED, not merely valid -- then gives `Z1 >= 1`
for every bounded `A` with `A21` completely free.

THE SCOPE LINE IS DRAWN IN THE FIGURE ITSELF, because it is the whole point:
arXiv:2607.19762 (Xu, 2026) proves this same `a = 0` CLM linearization is INVERTIBLE on
origin-`H^2` after the standard modulation, with a spectral gap of `1/2`.  So this is not a
statement about the operator.  It is a statement about the certificate's space.

Rebuild fig63 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_ngx_v1_general_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_ngx_v1_general.py

Six panels: A the ladders -- sigma_min against M for every s, log-log; B the fitted exponent
against the predicted 1-s, with the s = 1 crossing and the DIFFERENT mechanism at s = 1.5;
C the explicit sequence, its agreement with the numerical optimum and the single row its
residual lives in; D the truncation-artifact audit; E the mu dial, where the same code path
saturates; F the trade-off against leg 54's battery, with the exact inverse sitting exactly
on the line, and the counterexample floor that diverges.
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
JSON = DATA / "p2_route_ngx_v1_general.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79", "warn": "#e08a1e",
     "grey": "#888888", "ours": "#7b1fa2", "floor": "#00695c"}
S_COL = {0.0: "#1f4e79", 0.3: "#7b1fa2", 0.7: "#2e7d32", 1.0: "#e08a1e", 1.5: "#c1440e"}


def main():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(17.5, 10.2))
    fig.suptitle(
        "Route-NGX (leg 127): the general class $A_{21}\\neq 0$ is decided — in $\\ell^1_w$ "
        "at $s<1$ the bordered $a=0$ CLM linearisation is NOT bounded below,\n"
        "so $Z_1\\geq 1$ for EVERY bounded $A$.  It is a statement about the SPACE: "
        "arXiv:2607.19762 proves the same operator is invertible on origin-$H^2$.",
        fontsize=12.5, y=0.985)

    # ---------------------------------------------------------------- A
    a = ax[0, 0]
    for row in d["NGX2_sigma_min_ladder"]:
        if row["K"] != 4:
            continue
        s = row["s"]
        a.loglog(row["M_extra"], row["sigma_min"], "o-", color=S_COL[s], lw=1.8, ms=5,
                 label=f"$s={s}$  ($p={row['fitted_exponent_p_in_sigma_M_to_the_minus_p']:.3f}$)")
    a.set_xlabel("$M-K$  (tail modes)")
    a.set_ylabel("$\\sigma_{\\min}(L)=1/\\|L^{-1}\\|_w$")
    a.set_title("A  the ladder that decides it ($K=4$)\n"
                "$\\sigma_{\\min}\\to 0$ for every $s<1$", fontsize=10.5)
    a.legend(fontsize=7.6, loc="lower left")
    a.grid(alpha=0.3, which="both")

    # ---------------------------------------------------------------- B
    b = ax[0, 1]
    ss = sorted({r["s"] for r in d["NGX2_sigma_min_ladder"]})
    for K, mk in ((2, "o"), (4, "s"), (8, "^")):
        ps = [next(r["fitted_exponent_p_in_sigma_M_to_the_minus_p"]
                   for r in d["NGX2_sigma_min_ladder"] if r["s"] == s and r["K"] == K)
              for s in ss]
        b.plot(ss, ps, mk + "-", ms=6, lw=1.3, label=f"$K={K}$",
               color={2: C["anchor"], 4: C["ours"], 8: C["good"]}[K])
    xs = np.linspace(0, 1, 50)
    b.plot(xs, 1 - xs, "--", color=C["grey"], lw=2, label="predicted $1-s$")
    b.axvline(1.0, color=C["bad"], lw=1.2, ls=":")
    b.annotate("kernel leaves $\\ell^1_w$ at $s=1$:\nthe exponent vanishes", xy=(0.99, 0.09),
               xytext=(0.04, 0.40), fontsize=8, color=C["bad"],
               arrowprops=dict(arrowstyle="->", color=C["bad"], lw=1.1))
    b.annotate("rises again — but this is the\nCOKERNEL, a DIFFERENT mechanism",
               xy=(1.46, 0.46), xytext=(0.04, 0.13), fontsize=7.8, color=C["bad"],
               arrowprops=dict(arrowstyle="->", color=C["bad"], lw=1.1))
    b.set_xlabel("weight exponent $s$")
    b.set_ylabel("fitted $p$ in $\\sigma_{\\min}\\sim M^{-p}$")
    b.set_title("B  the exponent is $1-s$, and it vanishes exactly at $s=1$\n"
                f"max |deviation| for $s<1$: "
                f"{d['NGX2_max_deviation_from_1_minus_s_for_s_below_1']:.4f}", fontsize=10.5)
    b.legend(fontsize=8, loc="upper right")
    b.grid(alpha=0.3)

    # ---------------------------------------------------------------- C
    c = ax[0, 2]
    ex = [r for r in d["NGX3_explicit_sequence"] if r["class"] == "algebraic"]
    c.loglog([r["M_extra"] for r in ex], [r["explicit_ratio"] for r in ex], "o-",
             color=C["ours"], lw=2, ms=7, label="explicit  $v=(z;h)$, written down")
    c.loglog([r["M_extra"] for r in ex], [r["numerical_sigma_min"] for r in ex], "x--",
             color=C["anchor"], lw=1.4, ms=9, label="numerical optimum $1/\\|L^{-1}\\|_w$")
    c.set_xlabel("$M-K$")
    c.set_ylabel("$\\|Lv\\|_w/\\|v\\|_w$")
    c.set_title("C  the sequence is CONSTRUCTED, not found\n"
                f"agreement {d['NGX3_max_ratio_over_optimum']:.10f}×,  "
                f"residual in {d['NGX3_max_rows_carrying_residual']} row,  "
                f"$z_K={d['NGX3_max_abs_z_K']:.0f}$ exactly", fontsize=10.5)
    c.legend(fontsize=8, loc="upper right")
    c.grid(alpha=0.3, which="both")
    c.text(0.03, 0.06,
           "finite-block residual at float zero;\nthe whole defect is the truncation\n"
           "edge row $|1-M/2|\\,|h_M|\\,w_M\\sim M^{s-1}$",
           transform=c.transAxes, fontsize=7.6, color=C["floor"], va="bottom")

    # ---------------------------------------------------------------- D
    dd = ax[1, 0]
    aud = [r for r in d["NGX4_truncation_artifact_audit"] if r["class"] == "algebraic"]
    for i, r in enumerate(aud):
        xs = [r["M_extra_built_at"]] + [e["M_extra"] for e in r["embedded"]]
        ys = [r["ratio_at_own_M"]] + [e["ratio"] for e in r["embedded"]]
        dd.loglog(xs, ys, "o-", lw=1.7, ms=6,
                  color=[C["anchor"], C["ours"], C["good"]][i],
                  label=f"built at $M-K={r['M_extra_built_at']}$, zero-padded")
    dd.set_xlabel("$M-K$ it is EVALUATED at")
    dd.set_ylabel("$\\|Ly\\|_w/\\|y\\|_w$")
    dd.set_title("D  not a truncation artifact (leg 58's NG2c, re-aimed)\n"
                 f"zero-padding into a 4× larger tail costs ≤ "
                 f"{d['NGX4_max_degradation_factor']:.3f}×, not O(1)", fontsize=10.5)
    dd.legend(fontsize=7.6, loc="upper right")
    dd.grid(alpha=0.3, which="both")

    # ---------------------------------------------------------------- E
    e = ax[1, 1]
    for r in d["NGX5_positive_control_mu"]:
        if r["arm"] != "bordered_like_mu_0":
            continue
        lab = f"$\\mu={r['mu']}$" + ("  (the object)" if r["mu"] == 0 else "")
        e.loglog(r["M_extra"], r["sigma_min"], "o-", lw=2 if r["mu"] == 0 else 1.4,
                 ms=6 if r["mu"] == 0 else 4,
                 color=C["bad"] if r["mu"] == 0 else C["good"], label=lab,
                 alpha=1.0 if r["mu"] == 0 else 0.55)
    e.set_xlabel("$M-K$")
    e.set_ylabel("$\\sigma_{\\min}(L)$")
    e.set_title("E  the control CAN report the other answer\n"
                f"$\\mu>0$: |exponent| ≤ "
                f"{d['NGX5_max_abs_exponent_for_mu_positive']:.1e} (saturates); "
                f"$\\mu=0$: {d['NGX5_exponent_at_mu_0'][0]:.4f}", fontsize=10.5)
    e.legend(fontsize=7.6, loc="lower left")
    e.grid(alpha=0.3, which="both")

    # ---------------------------------------------------------------- F
    f = ax[1, 2]
    fls = d["NGX6_counterexample_norm_floor"]
    for kind, col in (("flat", C["anchor"]), ("algebraic", C["ours"])):
        fl = [x for x in fls if x["class"] == kind]
        s_lab = "0" if kind == "flat" else "0.3"
        for key, ls, mk, lab in (("floor_for_Z1_0", "-", "o", "$Z_1=0$"),
                                 ("floor_for_Z1_0p5", "--", "s", "$Z_1=0.5$"),
                                 ("floor_for_Z1_0p99", ":", "^", "$Z_1=0.99$")):
            f.loglog([x["M_extra"] for x in fl], [x[key] for x in fl], ls, marker=mk,
                     color=col, lw=1.6, ms=5, alpha=0.9,
                     label=f"$s={s_lab}$, {lab}")
    f.set_xlabel("$M-K$")
    f.set_ylabel("required $\\|A\\|_w$")
    f.set_title("F  what a counterexample would COST\n"
                "$\\|A\\|_w\\geq(1-Z_1)/\\sigma_{\\min}\\sim M^{1-s}$ — "
                f"×{d['NGX6_floor_growth_per_doubling_of_M']['flat']:.2f} / "
                f"×{d['NGX6_floor_growth_per_doubling_of_M']['algebraic']:.2f} per doubling",
                fontsize=10.5)
    f.set_ylim(top=2.0e7)
    f.legend(fontsize=6.8, loc="upper left", ncol=2)
    f.grid(alpha=0.3, which="both")
    f.text(0.035, 0.55,
           f"the bound holds on all {d['NGX6_rows_checked']} rows of leg 54's battery,\n"
           f"and is ATTAINED: min slack {d['NGX6_min_slack']:.1e}, at the exact inverse.\n"
           "At any FIXED $M$ the floor is modest — a finite-$M$ counterexample\n"
           "is not excluded.  What is excluded is ONE bounded $A$ for all $M$.",
           transform=f.transAxes, fontsize=7.2, color=C["floor"], va="bottom")

    fig.tight_layout(rect=(0, 0.012, 1, 0.955))
    fig.text(0.5, 0.004,
             "Object: the $a=0$ CLM linearisation, $Y_0$ exactly zero for the degenerate "
             "reason.  No dynamics run.  Nothing claimed about HL_S2_nonsymmetric or any "
             "link of the L1→L4 chain.",
             ha="center", fontsize=8, color=C["grey"])
    out = FIGS / "fig63_route_ngx_v1_general.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
