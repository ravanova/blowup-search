"""Phase-2 P2 Route-M v1 (fig42): target selection — "certify WHAT, that isn't already done?"

The certification port has been aimed at Chen–Hou's 2D Boussinesq profile for twenty legs.
That object was certified by its authors. This leg asks which objects with numerically
convincing blow-up are still UNCERTIFIED, ranks them, and measures whether the top one is
reachable on our own code.

Rebuild fig42 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_m_v1_evidence.py
Regenerate the data (deterministic; ~45 min, the M3 ladder is the cost):
    .venv/bin/python -u experiments/p2_route_m_v1_targets.py

Six panels: A the ledger, cost against certification status — the whole finding in one
picture; B the Y_0 budget, i.e. what "reachable" means as a number, gated on Cadiot–
Lessard–Nave's completed Kawahara certificate; C the 3D Navier–Stokes preprint's scalar
closure in both forms, kept because the arithmetic is NOT where it fails; D THE
MEASUREMENT — the top candidate's residual under refinement with the dissipation going to
zero; E the same measurement on the object the port is aimed at, going the other way; F the
profile itself, non-symmetric and positive, with the contraction ratio against CHL's.
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
JSON = DATA / "p2_route_m_v1_targets.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ns": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    m1, m2, m3, m4 = (d["M1_ledger"], d["M2_feasibility"], d["M3_reachability"],
                      d["M4_contrast_2d"])
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the ledger ---------------------------------------------------
    a0 = ax[0, 0]
    rows = m1["rank_table"]
    cols = {"NO": C["good"], "YES_CAP": C["bad"], "YES_ANALYTIC": C["bad"],
            "CLAIMED_UNUSABLE": C["ns"]}
    y = np.arange(len(rows))[::-1]
    a0.barh(y, [r["ratio"] for r in rows],
            color=[cols[r["certified"]] for r in rows], alpha=0.85)
    a0.set_yticks(y)
    a0.set_yticklabels([f"{r['rank']}. {r['id']}" for r in rows], fontsize=7)
    a0.set_xscale("log")
    a0.axvline(1.0, color=C["anchor"], ls="--", lw=1.4)
    a0.text(1.15, len(rows) - 1.4, "the object that WAS\ncertified (Chen–Hou)",
            fontsize=6.8, color=C["anchor"])
    a0.set_xlabel("unknown count / unknowns of the certified object (same $n$)")
    named = m1["gate"]["named_target"]
    a0.set_title("A  the ledger: green = UNCERTIFIED, red = already proved\n"
                 f"gate {m1['gate']['gate']} → {named}", fontsize=9)

    # ---- B: the Y_0 budget ----------------------------------------------
    a1 = ax[0, 1]
    Z1s = np.linspace(0.0, 0.95, 200)
    for Z2, ls in ((1e0, "-"), (1e2, "--"), (1e4, ":")):
        a1.plot(Z1s, (1 - Z1s) ** 2 / (2 * Z2), ls, color=C["anchor"], lw=1.8,
                label=f"$Z_2 = 10^{{{int(np.log10(Z2))}}}$")
    k = m2["cln_kawahara"]
    a1.axhline(k["Y0_published"], color=C["good"], lw=1.6)
    a1.plot([k["Z1_implied"]], [k["Y0_published"]], "o", color=C["good"], ms=8)
    a1.annotate(f"CLN Kawahara, a COMPLETED certificate\n"
                f"$Y_0$ = {k['Y0_published']:.2e}, our algebra returns their\n"
                f"$r_0$ = {k['r_from_our_algebra']:.3e} "
                f"(rel err {k['rel_err_vs_published_r0']:.0e})",
                xy=(k["Z1_implied"], k["Y0_published"]),
                xytext=(0.28, 3e-11), fontsize=6.8, color=C["good"],
                arrowprops=dict(arrowstyle="->", color=C["good"], lw=1.0))
    a1.set_yscale("log")
    a1.set_ylim(1e-16, 1e0)
    a1.set_xlabel("$Z_1$")
    a1.set_ylabel("$Y_0$ budget $=(1-Z_1)^2/(2Z_2)$")
    a1.legend(fontsize=7, loc="upper right")
    a1.set_title("B  what “within reach” means as a NUMBER:\n"
                 "the residual a certificate is allowed to have", fontsize=9)

    # ---- C: the NS preprint closure --------------------------------------
    a2 = ax[0, 2]
    a = m2["ns_preprint_audit"]
    vals = [a["closure_as_printed_2dMK"], a["closure_corrected_2M2Kdelta"]]
    a2.bar([0, 1], vals, color=[C["grey"], C["ns"]], alpha=0.9, width=0.55)
    a2.axhline(1.0, color=C["bad"], ls="--", lw=1.6)
    a2.text(1.52, 1.15, "closure fails above here", fontsize=7, color=C["bad"], ha="right")
    a2.set_yscale("log")
    a2.set_xticks([0, 1])
    a2.set_xticklabels(["as printed\n$2\\delta MK$",
                        "as Kantorovich\nrequires\n$2M^2K\\delta$"], fontsize=7.5)
    a2.set_ylim(1e-6, 1e2)
    for i, v in enumerate(vals):
        a2.text(i, v * 1.6, f"{v:.2e}", ha="center", fontsize=7.5)
    a2.text(0.02, 0.03,
            "BOTH CLOSE. The arithmetic is not where that manuscript\n"
            "fails — which is why the reasons it cannot be used (no released\n"
            "verification package; a backward self-similar ansatz excluded by\n"
            "Nečas–Růžička–Šverák / Tsai) have to stand on their own.",
            fontsize=6.9, transform=a2.transAxes, va="bottom")
    a2.set_title("C  the 3D Navier–Stokes claim, audited\n"
                 "(the top target's Q1, answered rather than assumed)", fontsize=9)

    # ---- D: THE MEASUREMENT ---------------------------------------------
    a3 = ax[1, 0]
    for r in m3["rungs"]:
        a3.plot(r["hist"]["tau"], r["hist"]["res"], "-", lw=1.6,
                label=f"$n$={r['n']}, $\\nu$={r['nu']:.3f}")
    a3.set_yscale("log")
    a3.set_xlabel(r"rescaled time $\tau$")
    a3.set_ylabel(r"$\max(\|\Omega_\tau\|_\infty, \|V_\tau\|_\infty)$")
    a3.legend(fontsize=7)
    lad = m3["residual_ladder"]
    tds = [r["tau_direction"] for r in m3["rungs"]]
    a3.set_title("D  the top candidate under refinement, $\\nu\\to0$ with the grid\n"
                 f"ladder {lad['classification']} (net {lad['net_ratio']:.3f}); "
                 f"final/min "
                 f"{', '.join(f'{t['final_over_min']:.2f}' for t in tds)}", fontsize=9)

    # ---- E: the contrast --------------------------------------------------
    a4 = ax[1, 1]
    if m4.get("available"):
        lg = sorted(m4["ladder"], key=lambda r: r["n_r"])
        seen, uniq = set(), []
        for r in lg:
            if r["n_r"] not in seen:
                uniq.append(r); seen.add(r["n_r"])
        a4.plot([r["n_r"] for r in uniq], [r["residual"] for r in uniq], "s-",
                color=C["bad"], lw=2.0, ms=7, label="2D object (the port's target)")
    ns = [r["n"] for r in m3["rungs"]]
    a4.plot(ns, [r["residual"] for r in m3["rungs"]], "o-", color=C["good"], lw=2.0,
            ms=7, label="1D candidate (Route-M's target)")
    a4.set_xscale("log"); a4.set_yscale("log")
    a4.set_xlabel("grid resolution")
    a4.set_ylabel("steady residual at the end of the run")
    a4.legend(fontsize=7.5)
    net2d = m4.get("net_ratio", float("nan"))
    a4.set_title("E  the same measurement on both objects\n"
                 f"2D: {net2d:.1f}× WORSE under refinement; "
                 f"1D: {lad['net_ratio']:.2f}×", fontsize=9)

    # ---- F: the profile ---------------------------------------------------
    a5 = ax[1, 2]
    fine = m3["rungs"][-1]
    X = np.array(fine["X_sample"]); Om = np.array(fine["Omega_sample"])
    V = np.array(fine["V_sample"])
    sel = np.abs(X) < 12.0
    a5.plot(X[sel], Om[sel], "-", color=C["anchor"], lw=2.0, label=r"$\Omega$")
    a5.plot(X[sel], V[sel], "-", color=C["warn"], lw=1.6, label=r"$V=\Theta_X$")
    a5.axvline(0.0, color=C["grey"], lw=0.8, ls=":")
    a5.axvline(fine["X_peak"], color=C["good"], lw=1.2, ls="--")
    a5.set_xlabel("$X$")
    a5.legend(fontsize=8)
    a5.text(0.02, 0.97,
            f"peak at $X^*$ = {fine['X_peak']:.3f}, NOT at the origin\n"
            f"$\\min\\Omega$ = {fine['min_Omega']:.2e} > 0 — regular and positive\n"
            f"$c_l/c_\\omega$ = {fine['ratio']:+.4f} vs CHL {m3['chl_ratio']}"
            f"  ({100*fine['ratio_err_vs_CHL']:.2f}%)\n"
            f"Chen–Hou–Huang's SYMMETRIC branch sits at −2.9987",
            fontsize=7.2, transform=a5.transAxes, va="top")
    a5.set_title("F  the object itself: no symmetry point to pin the\n"
                 "translation — which is why it needs a THIRD constant", fontsize=9)

    fig.suptitle("Route-M v1 — target selection: the port was aimed at a certified object, "
                 "and the uncertified one was already in the repository", fontsize=12,
                 y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig42_route_m_v1_targets.png"
    fig.savefig(out, dpi=150)
    print(f"-> {out}")


if __name__ == "__main__":
    build_figure()
