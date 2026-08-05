"""Phase-2 P2 Route-V v0 (fig43): stage V's novelty gate — the question was already
answered, and this is the re-derivation that proves it was.

Stage V wanted to switch dissipation on and watch a blow-up certificate's margin. The
plan put a ban in front of it: check first whether anyone has already done
certification-under-dissipation for a self-similar profile. They have —
Dahne–Figueras (arXiv:2410.05480) verify whole branches of self-similar singular
solutions of the complex Ginzburg–Landau equation, continued in the dissipation
parameter, in interval arithmetic. This figure is the check, run as a re-derivation
rather than as a citation.

Rebuild fig43 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_v_v0_evidence.py
Regenerate the data (deterministic, ~90 s):
    .venv/bin/python -u experiments/p2_route_v_v0_novelty.py

Six panels: A the ledger and what each entry settles; B the re-derivation of their
published NLS zeros; C THE PICTURE — their published branch in the dissipation dial and
ours on top of it; D the difference between the two curves; E the margin proxy along the
dial, and its divergence exponent at the fold; F the two guards, resolution and far-field
truncation.
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
JSON = DATA / "p2_route_v_v0_novelty.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    g, rep, guards = d["V0_1_gate"], d["V0_2_reproduction"], d["V0_3_guards"]
    br, mar = d["V0_4_branch"], d["V0_5_margin"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the ledger ---------------------------------------------------
    a0 = ax[0, 0]
    order = {"PRE_EMPTS": 0, "ADJACENT": 1, "EXCLUSION": 2}
    cols = {"PRE_EMPTS": C["bad"], "ADJACENT": C["warn"], "EXCLUSION": C["grey"]}
    rows = sorted(g["ledger"], key=lambda p: order[p["verdict"]])
    y = np.arange(len(rows))[::-1]
    a0.barh(y, [3 - order[p["verdict"]] for p in rows],
            color=[cols[p["verdict"]] for p in rows], alpha=0.85)
    a0.set_yticks(y)
    a0.set_yticklabels([p["id"].replace("arXiv:", "").split(" +")[0] for p in rows],
                       fontsize=7.5)
    for yy, p in zip(y, rows):
        a0.text(0.06, yy, f"{p['verdict']} — {p['dial'][:34]}", fontsize=6.6,
                va="center", color="white" if order[p["verdict"]] < 2 else "black")
    a0.set_xticks([])
    a0.set_xlim(0, 3.2)
    a0.set_title("A  the gate, computed off the ledger:\n"
                 f"answer {g['answer']} — {g['pre_empting'][0]} pre-empts stage V",
                 fontsize=9)
    a0.text(0.02, -0.14,
            f"{len(g['search_log'])} arXiv queries; the four asking for the FLUID version "
            f"(viscous Boussinesq / Euler + CAP) return nothing —\nthat hole is real and it "
            f"is not what stage V asked for.",
            fontsize=7, transform=a0.transAxes, va="top")

    # ---- B: the re-derivation --------------------------------------------
    a1 = ax[0, 1]
    lbl = [f"{r['case']} j={r['j']}" for r in rep["rows"]]
    x = np.arange(len(lbl))
    a1.bar(x - 0.18, [abs(r["d_mu"]) for r in rep["rows"]], 0.36, color=C["anchor"],
           label=r"$|\Delta\mu|$")
    a1.bar(x + 0.18, [abs(r["d_kappa"]) for r in rep["rows"]], 0.36, color=C["ours"],
           label=r"$|\Delta\kappa|$")
    a1.axhline(rep["gate"], color=C["bad"], ls="--", lw=1.3)
    a1.text(len(lbl) - 0.5, rep["gate"] * 1.3, "gate 1e−06", fontsize=7,
            color=C["bad"], ha="right")
    a1.set_yscale("log")
    a1.set_xticks(x)
    a1.set_xticklabels(lbl, fontsize=8)
    a1.set_ylabel("deviation from the published enclosure")
    a1.set_title("B  their Tables 1 and 2, re-derived: independent RK4 +\n"
                 "an independently derived far field, no shared code", fontsize=9)
    a1.legend(fontsize=8, loc="upper left")
    a1.text(0.02, 0.72,
            f"j=1 rows land within {rep['headline_deviation']:.1e}\n"
            f"worst row (j=4, our $\\xi_1$=20 vs their 25): {rep['worst_deviation']:.1e}",
            fontsize=7.2, transform=a1.transAxes, va="top")

    # ---- C: THE PICTURE --------------------------------------------------
    a2 = ax[0, 2]
    rec = [r for r in br["records"] if r["converged"]]
    if br.get("published_figure"):
        pf = br["published_figure"]
        a2.plot(pf["eps"], pf["kappa"], color=C["grey"], lw=3.2, alpha=0.55,
                label="Dahne–Figueras Fig. 1a (their curve)")
    else:
        s = br["published_samples"]
        a2.plot([r["eps"] for r in s], [r["kappa"] for r in s], "o", color=C["grey"],
                ms=4, label="Dahne–Figueras Fig. 1a (samples)")
    a2.plot([r["eps"] for r in rec], [r["kappa"] for r in rec], color=C["ours"], lw=1.3,
            label="ours (this leg)")
    f = br["fold"]
    a2.plot([f["eps_star"]], [f["kappa_star"]], "*", color=C["bad"], ms=14, zorder=5)
    a2.annotate(f"fold: $\\epsilon^*$ = {f['eps_star']:.6f}\n"
                f"theirs {br['published_fold']['eps_star']:.6f}"
                f"  ($\\Delta$ = {br['d_eps_star']:+.1e})",
                xy=(f["eps_star"], f["kappa_star"]), xytext=(0.30, 0.62),
                textcoords="axes fraction", fontsize=7.6, color=C["bad"],
                arrowprops=dict(arrowstyle="->", color=C["bad"], lw=1.0))
    a2.set_xlabel(r"$\epsilon$ — the DISSIPATION dial (0 = NLS)")
    a2.set_ylabel(r"$\kappa$")
    a2.legend(fontsize=7.5, loc="upper right")
    a2.set_title("C  the certificate does not die when dissipation is\n"
                 "switched on — it dies at a FOLD, and here it is", fontsize=9)

    # ---- D: the difference -----------------------------------------------
    a3 = ax[1, 0]
    cmp = br["comparison_to_published_curve"]
    if cmp:
        kk = [r["kappa"] for r in cmp["rows"]]
        dd = [abs(r["diff"]) for r in cmp["rows"]]
        a3.semilogy(kk, dd, "o-", color=C["ours"], ms=4)
        a3.axvline(f["kappa_star"], color=C["bad"], ls=":", lw=1.2)
        a3.text(f["kappa_star"], max(dd), " the fold", fontsize=7, color=C["bad"])
        a3.set_xlabel(r"$\kappa$ (the branch's own parameter)")
        a3.set_ylabel(r"$|\epsilon_{\rm ours} - \epsilon_{\rm published}|$")
        a3.set_title(f"D  ours against theirs along the whole branch:\n"
                     f"max {cmp['max_abs_diff']:.1e}, rms {cmp['rms_diff']:.1e} "
                     f"on {cmp['n']} samples", fontsize=9)
        a3.invert_xaxis()

    # ---- E: the margin proxy ---------------------------------------------
    a4 = ax[1, 1]
    cur = mar["curve"]
    a4.semilogy([r["eps"] for r in cur], [r["Jinv_norm"] for r in cur], "o-",
                color=C["anchor"], ms=3.5, lw=1.1)
    a4.plot([mar["at_eps_zero"]["eps"]], [mar["at_eps_zero"]["Jinv_norm"]], "s",
            color=C["good"], ms=8, label=r"$\epsilon = 0$ (the NLS end)")
    a4.plot([mar["at_fold"]["eps"]], [mar["at_fold"]["Jinv_norm"]], "*", color=C["bad"],
            ms=14, label="nearest sample to the fold")
    a4.set_xlabel(r"$\epsilon$")
    a4.set_ylabel(r"$\|J^{-1}\|_\infty$   (the float analogue of $\|A\|$)")
    a4.legend(fontsize=7.5, loc="lower right")
    law = mar.get("law") or {}
    a4.set_title("E  the margin proxy IMPROVES "
                 f"{mar['at_eps_zero']['Jinv_norm']/mar['mid_branch']['Jinv_norm']:.0f}"
                 r"$\times$ as $\epsilon$ rises," "\n"
                 f"then diverges at the fold with exponent {law.get('slope', float('nan')):+.3f} "
                 "(quadratic fold: −1)", fontsize=9)
    if law.get("rows"):
        ins = a4.inset_axes([0.30, 0.60, 0.34, 0.36])
        dist = np.array([r["distance"] for r in law["rows"]])
        val = np.array([r["Jinv_norm"] for r in law["rows"]])
        ins.loglog(dist, val, "o", color=C["ours"], ms=3)
        xs = np.array([dist.min(), dist.max()])
        ins.loglog(xs, 10 ** law["intercept"] * xs ** law["slope"], "-",
                   color=C["bad"], lw=1.0)
        ins.set_xlabel(r"$|\kappa-\kappa^*|$", fontsize=6)
        ins.set_xticks([], minor=True)
        ins.set_xticks([0.01, 0.08])
        ins.set_xticklabels(["0.01", "0.08"])
        ins.set_yticks([0.1, 1.0])
        ins.set_yticklabels(["0.1", "1"])
        ins.tick_params(labelsize=5.5)

    # ---- F: the guards ---------------------------------------------------
    a5 = ax[1, 2]
    xil = guards["xi1_ladder"]
    a5.plot([r["xi1"] for r in xil], [r["kappa"] for r in xil], "o-", color=C["anchor"],
            ms=5)
    a5.axhline(rep["rows"][0]["kappa_published"], color=C["bad"], ls="--", lw=1.2)
    a5.text(xil[-1]["xi1"], rep["rows"][0]["kappa_published"],
            "  published $\\kappa$", fontsize=7, color=C["bad"], va="bottom", ha="right")
    a5.set_xlabel(r"matching point $\xi_1$")
    a5.set_ylabel(r"$\kappa$ returned")
    a5.ticklabel_format(axis="y", useOffset=False, style="plain")
    a5.set_title("F  the two guards: far-field truncation (shown) and\n"
                 "step halving (below) — measured, not assumed", fontsize=9)
    res = guards["resolution_ladder"]
    a5.text(0.03, 0.26,
            "step halving, Case II:\n" + "\n".join(
                f"   {r['steps_per_osc']:>4d} steps/osc: defect {r['defect']:.3e}"
                for r in res)
            + f"\n   moves it by {guards['defect_moved_by_halving']:.1e}\n"
              f"$\\xi_1$ = 10→30 moves $\\kappa$ by "
              f"{guards['kappa_spread_over_xi1']:.1e}",
            fontsize=6.8, transform=a5.transAxes, va="top", family="monospace")

    fig.suptitle("Route-V v0 — the novelty gate: certification under dissipation is a "
                 "2024 result, re-derived here to be sure of it", fontsize=12, y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig43_route_v_v0_novelty.png"
    fig.savefig(out, dpi=150)
    print(f"-> {out}")


if __name__ == "__main__":
    build_figure()
