"""Phase-2 P2 Route-J v1 (fig39): the primary-source pass, as measurements.

Six legs of literature checking were blocked on egress and written anyway -- five
passes, all search-level, zero papers read.  Egress opened; the papers are read; this
figure is what the reading leaves behind that a paragraph would not.

Rebuild fig39 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_j_v1_evidence.py
Regenerate the data (deterministic; ~5 s):
    .venv/bin/python -u experiments/p2_route_j_v1_literature.py

Six panels: A the constant ALS corrected in Schochet 1986, settled from our side by the
PDE residual; B Route-H's closed form (E) against ALS (57)-(58), pointwise -- the
retraction, drawn; C alpha(1/2) = 3 by integrating the published a = 1/2 pole system,
with the rungs the d-tau gate refuses shaded rather than dropped; D what lies ABOVE
criticality -- the Schochet family collapsing at beta = 2 and failing to at beta = 1;
E our alpha(a) branch against XU's s*(a) = 1/c_l(a), the formula that pre-empts Route-F;
F the claim ledger, twelve claims by verdict.
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
JSON = DATA / "p2_route_j_v1_literature.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ns": "#7b1fa2"}

from solver.critical_dissipation import exact_a0_spacetime          # noqa: E402
from solver.literature_gates import (                               # noqa: E402
    a_half_branch, als_a0_sigma1, collapse_spread, rescaled_collapse,
    route_h_E_as_als, schochet_K,
)


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: Schochet's constant ------------------------------------------
    a0 = ax[0, 0]
    j1 = d["J1_schochet_constant"]
    labels, vals, cols = [], [], []
    for r in j1["rows"]:
        labels.append(("ALS " if "corrected" in r["family"] else "1986 ") + r["which"])
        vals.append(max(r["worst_residual"], 1e-17))
        cols.append(C["good"] if "corrected" in r["family"] else C["bad"])
    a0.bar(range(len(vals)), vals, color=cols)
    a0.set_yscale("log")
    a0.set_xticks(range(len(vals)))
    a0.set_xticklabels(labels, rotation=20, fontsize=8)
    a0.axhline(1e-15, color=C["grey"], ls=":", lw=1)
    a0.text(0.02, 0.93, "rounding", transform=a0.transAxes, fontsize=7, color=C["grey"])
    a0.set_ylabel("relative PDE residual of ALS (36)")
    a0.set_title("A  the constant ALS corrected in Schochet (1986)\n"
                 "$K_\\pm = 24(3\\pm\\sqrt{6})$ solves it; $12(6\\pm\\sqrt{6})$ does not "
                 f"({j1['separation_decades']:.1f} decades)", fontsize=9)

    # ---- B: (E) is ALS (57)-(58) -----------------------------------------
    a1 = ax[0, 1]
    mu0, nu, T = 0.7, 1.3, 2.0
    m = route_h_E_as_als(mu0, nu, T)
    x = np.linspace(-6, 6, 1200)
    for t, ls in ((0.0, "-"), (1.7, "--"), (1.98, ":")):
        b = exact_a0_spacetime(x, t, nu, mu0, T=T)["omega"]
        a1.plot(x, b / np.max(np.abs(b)), ls, color=C["anchor"], lw=1.6,
                label=f"Route-H (E), $t/T$={t / T:.2f}")
        a2v = als_a0_sigma1(x, t, m["w_m1_0"], m["vc0"], nu)
        a1.plot(x[::40], (a2v / np.max(np.abs(b)))[::40], "o", ms=3.5,
                color=C["bad"], mfc="none")
    a1.plot([], [], "o", ms=4, color=C["bad"], mfc="none", label="ALS (57)-(58)")
    a1.set_xlabel("$x$")
    a1.set_ylabel("$\\omega$, normalised")
    a1.legend(fontsize=7, loc="upper right")
    a1.set_title("B  Route-H's closed form (E) IS ALS eq. (57)-(58)\n"
                 f"worst relative difference {d['J2_route_h_E_is_als']['worst_rel_diff']:.1e}; "
                 "their $t_c$ formula returns our $T$ exactly", fontsize=9)

    # ---- C: alpha(1/2) = 3 from the published a=1/2 system ---------------
    a2 = ax[0, 2]
    br = a_half_branch(Om0=10.0, n=120_000)
    ok = br["tau"] > 0
    tau, cl, res = br["tau"][ok], br["c_l_local"][ok], br["resolved"][ok]
    a2.semilogx(tau[res], cl[res], "-", color=C["anchor"], lw=1.6, label="resolved")
    a2.semilogx(tau[~res], cl[~res], "-", color=C["bad"], lw=1.2, alpha=0.75,
                label="REFUSED ($d\\tau$ below the floor)")
    a2.axhline(1.0 / 3.0, color=C["good"], ls="--", lw=1.2, label="exact $c_l = 1/3$")
    a2.invert_xaxis()
    a2.set_ylim(0.24, 0.40)
    a2.set_xlabel("$\\tau = t_c - t$   (collapse to the left)")
    a2.set_ylabel("$d\\log v_c / d\\log\\tau$")
    a2.legend(fontsize=7, loc="lower left")
    v = d["J3_alpha_half_from_als"]["verdict_row"]
    a2.set_title("C  $\\alpha(1/2)=3$ from ALS (49)-(50), integrated cold\n"
                 f"$c_l$ = {v['c_l']:.7f} (rel {v['c_l_rel_err']:.0e}); "
                 "the gate is on $d\\tau$, not $\\tau$", fontsize=9)

    # ---- D: ABOVE criticality -- the supercritical exponent --------------
    a3 = ax[1, 0]
    K, nuS = schochet_K(+1, corrected=True), 1.0
    taus = [1e-3, 3e-4, 1e-4, 3e-5, 1e-5]
    xi, curves, _ = rescaled_collapse(-1j, -2j, nuS, K, taus)
    # each family is normalised by its OWN peak over the ladder -- otherwise the two
    # sit on scales 30x apart and the panel shows the normalisation, not the collapse
    n2 = max(float(np.max(np.abs(curves[t] * t ** 2))) for t in taus)
    n1 = max(float(np.max(np.abs(curves[t] * t ** 1))) for t in taus)
    for t in taus:
        a3.plot(xi, curves[t] * t ** 2 / n2, "-", color=C["good"], lw=1.4, alpha=0.9)
        a3.plot(xi, curves[t] * t ** 1 / n1, "-", color=C["bad"], lw=1.1, alpha=0.7)
    a3.plot([], [], color=C["good"], lw=1.6,
            label="$\\tau^{2}\\omega$ — 5 rungs, superposed")
    a3.plot([], [], color=C["bad"], lw=1.6, label="$\\tau^{1}\\omega$ — 5 rungs, fanned")
    a3.set_xlabel("$\\xi = x/\\tau$")
    a3.set_ylabel("rescaled $\\omega$, each family to its own peak")
    a3.legend(fontsize=7, loc="upper right")
    j4 = d["J4_supercritical"]
    a3.set_title("D  ABOVE $s_c$: $\\beta = \\sigma\\,\\alpha$, and $\\omega_t$ is subdominant\n"
                 f"Schochet $\\sigma=2,\\alpha=1\\Rightarrow\\beta=2$; spreads differ "
                 f"{j4['beta_1_over_beta_2']:.0f}$\\times$", fontsize=9)

    # ---- E: our branch against XU's s*(a) --------------------------------
    a4 = ax[1, 1]
    rows = d["J5_branch_vs_xu"]["rows"]
    aa = [r["a"] for r in rows]
    a4.plot([r["a"] for r in d["J5_branch_vs_xu"]["xu_table1"]],
            [r["s_star"] for r in d["J5_branch_vs_xu"]["xu_table1"]],
            "-", color=C["bad"], lw=1.8, label="XU Table 1: $s^*(a) = 1/c_l(a)$")
    a4.plot(aa, [r["alpha_ours"] for r in rows], "o", ms=7, mfc="none",
            color=C["anchor"], mew=1.6, label="ours: $\\alpha(a)$ (Route-E/F)")
    a4.set_yscale("log")
    a4.axhline(2.0, color=C["grey"], ls=":", lw=1)
    a4.text(0.02, 0.63, "ordinary Laplacian $s=2$", transform=a4.transAxes,
            fontsize=7, color=C["grey"])
    a4.set_xlabel("$a$")
    a4.set_ylabel("$s^*(a) = \\alpha(a)$")
    a4.legend(fontsize=7, loc="upper left")
    a4.set_title("E  Route-F's $s_c=\\alpha/2$ is XU eq. (6.3), posted 11 days earlier\n"
                 f"worst row {d['J5_branch_vs_xu']['worst_rel_diff']:.1e}, "
                 "exact at $a=0$ and $a=1/2$", fontsize=9)

    # ---- F: the ledger ---------------------------------------------------
    a5 = ax[1, 2]
    counts = d["J6_ledger"]["counts"]
    order = ["PRE-EMPTED", "CONFIRMED_AND_PRE-EMPTED", "PRE-EMPTED_AND_RE-CLASSIFIED",
             "PARTIAL", "UNSEARCHED_AT_PRIMARY_SOURCE",
             "CONFIRMED (never claimed as ours)",
             "OPEN_QUESTION_ANSWERED_BY_THE_LITERATURE"]
    short = {"PRE-EMPTED": "pre-empted",
             "CONFIRMED_AND_PRE-EMPTED": "right, and known",
             "PRE-EMPTED_AND_RE-CLASSIFIED": "known + re-classified",
             "PARTIAL": "partial (scope differs)",
             "UNSEARCHED_AT_PRIMARY_SOURCE": "unsearched (Tier 2/3)",
             "CONFIRMED (never claimed as ours)": "cited all along",
             "OPEN_QUESTION_ANSWERED_BY_THE_LITERATURE": "inbound: they answer US"}
    col = {"PRE-EMPTED": C["bad"], "CONFIRMED_AND_PRE-EMPTED": C["bad"],
           "PRE-EMPTED_AND_RE-CLASSIFIED": C["ns"], "PARTIAL": C["warn"],
           "UNSEARCHED_AT_PRIMARY_SOURCE": C["grey"],
           "CONFIRMED (never claimed as ours)": C["anchor"],
           "OPEN_QUESTION_ANSWERED_BY_THE_LITERATURE": C["good"]}
    keys = [k for k in order if k in counts]
    a5.barh(range(len(keys)), [counts[k] for k in keys],
            color=[col[k] for k in keys])
    a5.set_yticks(range(len(keys)))
    a5.set_yticklabels([short[k] for k in keys], fontsize=8)
    a5.invert_yaxis()
    a5.set_xlabel("claims")
    lost = sum(v for k, v in counts.items() if "PRE-EMPTED" in k)
    a5.set_title(f"F  the ledger: {d['J6_ledger']['n_claims']} standing claims\n"
                 f"{lost} pre-empted, 1 partial, 2 unsearched,\n"
                 "1 result arriving FROM the literature", fontsize=9)

    fig.suptitle("Route-J v1 -- the primary-source pass: five search-level literature "
                 "passes, checked against the papers at last",
                 fontsize=12, y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig39_route_j_v1_literature.png"
    fig.savefig(out, dpi=150)
    print(f"-> {out}")


if __name__ == "__main__":
    build_figure()
