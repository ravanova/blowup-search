"""Phase-2 P2 Route-F v1 (fig35): the critical dissipation exponent for gCLM.

The Clay question in miniature -- can a blow-up beat viscosity?  A self-similar
blow-up has L ~ (T-t)^{1/alpha} with alpha the far-field decay exponent Route-E v1
measured, so comparing nu omega/L^{2s} against omega^2 gives

    D/N ~ nu (T-t)^{1 - 2 s / alpha}      =>      s_c(a) = alpha(a)/2 .

The leg tests the whole LINE p(s) = 1 - 2s/alpha rather than locating a threshold,
and its headline is a cross-check between two computations that share nothing: alpha
from a steady compactified solve on the LINE, dp/ds from time-dependent PERIODIC
simulation.  Navier-Stokes sits exactly at alpha = 2, where the ordinary Laplacian
is marginal -- which is what the map makes visible.

Rebuilds fig35 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_f_v1_evidence.py
Regenerate the data (deterministic; ~6 min):
    .venv/bin/python -u experiments/p2_route_f_v1_viscosity.py

Six panels: A the relevance line at a=0 with nothing fitted; B THE CROSS-CHECK;
C the fit-window systematic (swept, not chosen); D the nu-independence control;
E the resolution ladder; F the s_c(a) map and where it crosses the Laplacian.
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
JSON = DATA / "p2_route_f_v1_viscosity.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the relevance line at a = 0 -----------------------------------
    F2 = d["F2_relevance_line"]
    a0 = ax[0, 0]
    ss = np.array([r["s"] for r in F2["rows"]])
    pp = np.array([r["p"] for r in F2["rows"]])
    a0.plot(ss, 1.0 - 2.0 * ss, "-", color=C["anchor"], lw=2,
            label="prediction $p = 1 - 2s$  (nothing fitted)")
    a0.plot(ss, pp, "o", color=C["bad"], ms=8, label="measured")
    a0.axhline(0, color="k", lw=0.8)
    a0.axvline(0.5, color=C["good"], ls="--", lw=1.3)
    a0.text(0.505, 0.55, "$s_c = \\alpha/2 = 1/2$", fontsize=8.5, color=C["good"])
    a0.set_xlabel("dissipation exponent $s$")
    a0.set_ylabel("relevance exponent $p$   ($D/N \\sim (T-t)^p$)")
    a0.set_title("A  $a=0$: $\\alpha=1$ EXACTLY, so the line has no free parameter\n"
                 "slope %+.4f vs $-2$;  $p=0$ at $s=%.4f$ vs $1/2$"
                 % (F2["slope"], F2["s_zero"]), fontsize=10)
    a0.legend(fontsize=7.5)
    a0.grid(alpha=0.3)

    # ---- B: THE CROSS-CHECK ------------------------------------------------
    F3 = d["F3_cross_check"]
    a1 = ax[0, 1]
    al = np.array([r["alpha"] for r in F3])
    sl = np.array([r["slope"] for r in F3])
    pr = np.array([r["slope_pred"] for r in F3])
    a1.plot(al, -pr, "-", color=C["anchor"], lw=2,
            label="$-2/\\alpha$, with $\\alpha$ from Route-E (steady, on the LINE)")
    a1.plot(al, -sl, "o", color=C["bad"], ms=9,
            label="measured $-dp/ds$ (time-dependent, PERIODIC)")
    for r in F3:
        a1.annotate("$a$=%.1f" % r["a"], (r["alpha"], -r["slope"]),
                    textcoords="offset points", xytext=(8, 6), fontsize=7.5)
    a1.set_xlabel("$\\alpha$  (far-field decay exponent, from Route-E v1)")
    a1.set_ylabel("$-dp/ds$")
    a1.set_title("B  THE CROSS-CHECK — two computations sharing no grid,\n"
                 "basis, formulation or fitted constant", fontsize=10)
    a1.set_ylim(min(-sl) - 0.08, max(-sl) + 0.16)
    a1.legend(fontsize=7.0, loc="upper right")
    a1.grid(alpha=0.3)
    rat = np.array([r["ratio"] for r in F3])
    a1.text(0.03, 0.06, "ratio measured/predicted: %s\n= %.3f $\\pm$ %.3f while "
                        "$\\alpha$ itself DOUBLES\n(a uniform bias, not an "
                        "$a$-dependent failure)"
            % (", ".join("%.4f" % v for v in rat), rat.mean(),
               (rat.max() - rat.min()) / 2),
            transform=a1.transAxes, fontsize=7,
            bbox=dict(fc="white", ec=C["good"], alpha=0.95))

    # ---- C: the window systematic -----------------------------------------
    a2 = ax[0, 2]
    if "F7_window_systematic" in d:
        F7 = d["F7_window_systematic"]
        lab = ["%.2f-%.2f" % tuple(r["window"]) for r in F7["rows"]]
        xs = np.arange(len(lab))
        a2.plot(xs, [r["slope"] for r in F7["rows"]], "o-", color=C["bad"],
                label="slope (predicted $-2$)")
        a2.axhline(-2.0, color=C["bad"], ls="--", lw=1.2, alpha=0.6)
        a2b = a2.twinx()
        a2b.plot(xs, [r["zero"] for r in F7["rows"]], "s-", color=C["good"],
                 label="zero crossing (predicted $1/2$)")
        a2b.axhline(0.5, color=C["good"], ls="--", lw=1.2, alpha=0.6)
        a2b.set_ylabel("$s$ at $p=0$", color=C["good"])
        a2.set_xticks(xs)
        a2.set_xticklabels(lab, fontsize=7.5, rotation=20)
        a2.set_ylabel("$dp/ds$", color=C["bad"])
        a2.set_title("C  the fit window is the dominant systematic\n"
                     "slope %.3f$\\pm$%.3f,  zero %.3f$\\pm$%.3f"
                     % (F7["slope_mean"], F7["slope_halfspread"],
                        F7["zero_mean"], F7["zero_halfspread"]), fontsize=10)
        a2.grid(alpha=0.3)
        a2.text(0.03, 0.06, "swept, not chosen: $p$ is ASYMPTOTIC,\nso early windows "
                            "have not got there\nand late ones are noise",
                transform=a2.transAxes, fontsize=7,
                bbox=dict(fc="white", ec=C["grey"], alpha=0.95))
    a2.set_xlabel("fit window (fraction of the amplitude range)")

    # ---- D: the nu control -------------------------------------------------
    F4 = d["F4_nu_control"]
    a3 = ax[1, 0]
    for r in F4["rows"]:
        a3.plot(r["s"], r["p"], "o-", label="$\\nu=%.0e$: slope %+.3f"
                % (r["nu"], r["slope"]))
    sgrid = np.linspace(min(F4["rows"][0]["s"]), max(F4["rows"][0]["s"]), 20)
    a3.plot(sgrid, 1.0 - 2.0 * sgrid, "k--", lw=1.5, label="prediction $1-2s$")
    a3.set_xlabel("$s$")
    a3.set_ylabel("$p$")
    a3.set_title("D  control: the prediction contains $s$ and $\\alpha$,\n"
                 "NOT $\\nu$  (slope spread %.3f over 3 decades)"
                 % F4["slope_spread"], fontsize=10)
    a3.legend(fontsize=7.0)
    a3.grid(alpha=0.3)

    # ---- E: resolution -----------------------------------------------------
    F5 = d["F5_resolution"]
    a4 = ax[1, 1]
    ns = [r["n"] for r in F5["rows"]]
    pv = [r["p"] for r in F5["rows"]]
    a4.semilogx(ns, pv, "o-", color=C["anchor"], lw=1.8, base=2)
    a4.axhline(1.0 - 2.0 * F5["rows"][0]["s"], color=C["good"], ls="--", lw=1.3,
               label="prediction at $s=%.2f$" % F5["rows"][0]["s"])
    a4.set_xlabel("$n$ (Fourier modes)")
    a4.set_ylabel("$p$")
    a4.set_title("E  resolution: the two finest differ by %.1e\n"
                 "(the whole 8x ladder spans %.1e)"
                 % (F5.get("finest_pair_diff", float("nan")), F5["spread"]), fontsize=10)
    a4.legend(fontsize=7.5)
    a4.grid(alpha=0.3, which="both")

    # ---- F: the s_c(a) map -------------------------------------------------
    F6 = d["F6_sc_map"]
    a5 = ax[1, 2]
    aa = [r["a"] for r in F6["rows"]]
    sc = [r["s_c"] for r in F6["rows"]]
    a5.plot(aa, sc, "o-", color=C["anchor"], lw=2, label="$s_c(a) = \\alpha(a)/2$")
    a5.axhline(1.0, color=C["bad"], ls="--", lw=1.6)
    a5.text(0.02, 1.03, "the ordinary Laplacian, $s=1$", fontsize=8.5, color=C["bad"])
    a5.axhline(0.5, color=C["grey"], ls=":", lw=1.2)
    a5.text(0.20, 0.545, "$s_c(0)=1/2$ — classical, dissipative CLM", fontsize=7.5,
            color=C["grey"])
    astar = F6.get("a_at_sc_equals_1", float("nan"))
    if np.isfinite(astar):
        a5.plot([astar], [1.0], "*", color=C["bad"], ms=18, zorder=5)
        a5.annotate("$\\alpha=2$ at $a\\approx%.3f$\n— the NS-critical scaling" % astar,
                    (astar, 1.0), textcoords="offset points", xytext=(-140, 24),
                    fontsize=8, color=C["bad"])
    a5.fill_between([min(aa), max(aa)], 1.0, max(sc) * 1.05, color=C["good"], alpha=0.08)
    a5.text(0.30, 1.28, "here the scaling says the blow-up\nBEATS ordinary viscosity",
            fontsize=8, color=C["good"])
    a5.set_xlabel("$a$")
    a5.set_ylabel("$s_c$")
    a5.set_title("F  the map, and where Navier–Stokes sits\n"
                 "NS is pinned at $\\alpha=2$; here $\\alpha$ is free to move",
                 fontsize=10)
    a5.legend(fontsize=7.5, loc="upper left")
    a5.grid(alpha=0.3)

    fig.suptitle("Route-F v1 — the critical dissipation exponent is HALF the far-field decay "
                 "exponent, $s_c = \\alpha/2$:\nmeasured with nothing fitted at $a=0$, and "
                 "cross-checked against a completely independent computation of $\\alpha$",
                 fontsize=11.5)
    fig.tight_layout(rect=(0, 0, 1, 0.935))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig35_p2_route_f_v1_viscosity.png"
    fig.savefig(out, dpi=145)
    print("wrote", out)


if __name__ == "__main__":
    build_figure()
