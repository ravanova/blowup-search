"""Phase-2 P2 Route-G v1 (fig36): the critical dissipation exponent on the 2D object.

Route-F v1 measured s_c = alpha/2 for 1D gCLM.  This leg ports the question to the 2D
Boussinesq system in the Hou-Luo geometry -- the system the 1D model is a model OF -- and
the port forces the law into its invariant form:

    s_c = 1/(2 beta),   L ~ (T-t)^beta,   beta = 1/2 IS Navier-Stokes.

s_c DECREASES with beta, so a FASTER collapse loses to viscosity more easily.  The proven
2D Boussinesq boundary blow-up collapses at beta = 2.92 -- nearly six times the NS rate --
which puts it at s_c = 0.17, nowhere near beating the ordinary Laplacian.

Rebuilds fig36 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_g_v1_evidence.py
Regenerate the data (deterministic; ~90 min):
    .venv/bin/python -u experiments/p2_route_g_v1_collapse.py

Six panels: A the law s_c(beta) with every object this project has on it; B beta from
our OWN dynamically-rescaled 2D machine (steps + resolution ladders); C the direct
time-dependent route, refused, with the reason; D the underpowered p(s) line kept for
its sign structure; E the cross-model calibration on gCLM's dial; F who beats the
ordinary Laplacian, as a signed bar.
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
JSON = DATA / "p2_route_g_v1_collapse.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ns": "#7b1fa2"}
CL_GAUGE = 3.00649898   # the c_l the normalization is SET to (Chen-Hou Part I (2.23))


def g2_beta_preview(d):
    """Our own beta, if the run produced it (panel A shows it next to the published one)."""
    g2 = d.get("g2_our_beta")
    return g2["beta_mean"] if g2 else None


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the law -------------------------------------------------------
    a0 = ax[0, 0]
    b = np.logspace(np.log10(0.15), np.log10(6.0), 400)
    a0.loglog(b, 0.5 / b, color=C["anchor"], lw=2.2, label=r"$s_c = 1/(2\beta)$")
    a0.axhline(1.0, color=C["grey"], ls=":", lw=1.2)
    a0.axvline(0.5, color=C["ns"], ls="--", lw=1.6)
    a0.fill_between(b, 1.0, 40, where=(0.5 / b > 1.0), color=C["good"], alpha=0.10)
    a0.text(0.17, 2.4, "beats the ordinary\nLaplacian  ($s_c>1$)", fontsize=9,
            color=C["good"])
    for r in d["g0_law"]["rows"]:
        # the NS-critical gCLM member IS the NS point; one marker, one label
        if "NAVIER" in r["object"] or "NS-critical" in r["object"]:
            continue
        a0.plot(r["beta"], r["s_c"], "o", ms=8, color=C["bad"], zorder=5)
        a0.annotate(r["object"].split(" (")[0], (r["beta"], r["s_c"]),
                    textcoords="offset points", xytext=(7, 6), fontsize=8)
    if g2_beta_preview(d) is not None:
        bm = g2_beta_preview(d)
        a0.plot(bm, 0.5 / bm, "D", ms=8, color=C["warn"], zorder=6)
        a0.annotate("2D Boussinesq\n(our machine)", (bm, 0.5 / bm),
                    textcoords="offset points", xytext=(-6, -30), fontsize=8,
                    ha="right", color=C["warn"])
    a0.plot(0.5, 1.0, "*", ms=20, color=C["ns"], zorder=6)
    a0.annotate("NAVIER-STOKES = gCLM $a\\approx0.383$\n$\\beta=1/2$, $s_c=1$ exactly",
                (0.5, 1.0), textcoords="offset points", xytext=(-4, 16), fontsize=8.5,
                ha="center", color=C["ns"], fontweight="bold")
    a0.set_xlabel(r"collapse exponent $\beta$   ($L \sim (T-t)^\beta$)")
    a0.set_ylabel(r"critical dissipation exponent $s_c$")
    a0.set_title("A. The law, and every object on it\n"
                 "faster collapse (right) = LOSES to viscosity", fontsize=10)
    a0.set_ylim(0.05, 6)
    a0.set_xticks([0.2, 0.33, 0.5, 1.0, 2.0, 3.0, 5.0])
    a0.set_xticklabels(["0.2", "1/3", "1/2", "1", "2", "3", "5"])
    a0.set_yticks([0.1, 0.171, 0.5, 1.0, 1.5, 3.0])
    a0.set_yticklabels(["0.1", "0.17", "0.5", "1", "1.5", "3"])
    a0.minorticks_off()
    a0.legend(fontsize=8, loc="upper right")
    a0.grid(alpha=0.25, which="both")

    # ---- B: our own beta --------------------------------------------------
    a1 = ax[0, 1]
    g2 = d.get("g2_our_beta")
    if g2:
        st = g2["steps_ladder"]
        a1.plot([r["steps"] for r in st], [r["beta"] for r in st], "o-",
                color=C["warn"], label="relaxation (steps), $n_r=300$")
        rl = g2["resolution_ladder"]
        labs = [f"$n_r$={r['n_r']}\n$r_{{max}}$={r['r_max']:.0e}" for r in rl]
        xs = np.linspace(st[-1]["steps"] * 1.15, st[-1]["steps"] * 1.9, len(rl))
        a1.plot(xs, [r["beta"] for r in rl], "s", ms=8, color=C["anchor"],
                label="resolution / domain ladder")
        for x, r, lab in zip(xs, rl, labs):
            a1.annotate(lab, (x, r["beta"]), textcoords="offset points",
                        xytext=(0, -26), fontsize=6.5, ha="center")
        # THE GAUGE-CORRECTED READING.  c_l is PINNED by the normalization, so its
        # discrete readout (3.0637) should equal the gauge it was set to (3.00650); it
        # does not, by 1.9%, and beta = -c_l/c_omega inherits that as a systematic.
        # c_omega -- the actual output -- is far more accurate than beta looks.
        bc = [-CL_GAUGE / r["c_omega"] for r in rl]
        a1.plot(xs, bc, "^", ms=8, color=C["good"],
                label=r"same runs, $c_l$ at its INTENDED gauge")
        a1.axhline(g2["published_beta"], color=C["good"], ls="--", lw=1.8,
                   label=f"Chen-Hou published  {g2['published_beta']:.4f}")
        a1.set_title(f"B. $\\beta$ from OUR machine: {g2['beta_mean']:.4f} "
                     f"({100 * g2['relative_error_vs_published']:.1f}% off) -- but "
                     f"{np.mean(bc):.4f} ({100 * abs(np.mean(bc) - g2['published_beta']) / g2['published_beta']:.2f}%)\n"
                     "once the PINNED $c_l$ is held to the gauge it was set to",
                     fontsize=9.5)
        a1.set_xlabel("relaxation steps  /  ladder member")
        a1.set_ylabel(r"$\beta = -c_l/c_\omega$")
        a1.set_xscale("log")
        a1.legend(fontsize=7.5, loc="lower right")
    a1.grid(alpha=0.25)

    # ---- C: the direct route, refused -------------------------------------
    a2 = ax[0, 2]
    g3 = d.get("g3_direct")
    if g3:
        rep = g3["inviscid"]["window_report"]
        bw = rep.get("betas_by_window", [])
        a2.bar(range(len(bw)), bw, color=C["bad"], alpha=0.75)
        a2.axhline(float(np.mean(bw)) if bw else 0, color=C["grey"], ls=":")
        a2.set_xticks(range(len(bw)))
        a2.set_xticklabels(["early", "middle", "late"][:len(bw)], fontsize=9)
        a2.set_ylabel(r"$\beta$ fitted on that sub-window")
        a2.set_title("C. The 1D method does NOT port\n"
                     f"{rep['decades']:.2f} decades of $(T-t)$ (1D had ~4); "
                     f"$\\beta$ moves {100 * rep['beta_spread']:.0f}%", fontsize=10)
        a2.text(0.02, 0.02,
                f"growth {rep['growth']:.0f}x then the spectral guard fires\n"
                f"REFUSED: {rep['reason'][:70]}",
                transform=a2.transAxes, fontsize=7.5, va="bottom", color=C["bad"])
    a2.grid(alpha=0.25, axis="y")

    # ---- D: the underpowered p(s) line ------------------------------------
    a3 = ax[1, 0]
    if g3 and g3.get("relevance"):
        ss = np.array([r["s"] for r in g3["relevance"]])
        ps = np.array([r["p"] for r in g3["relevance"]])
        a3.plot(ss, ps, "o", color=C["bad"], ms=7, label="measured (underpowered)")
        if g3.get("p_line"):
            L = g3["p_line"]
            a3.plot(ss, L["slope"] * ss + L["intercept"], "-", color=C["bad"],
                    lw=1.4, label=f"fit: slope {L['slope']:+.2f} "
                                  f"$\\Rightarrow \\beta$={L['beta_implied']:.2f}")
        if g2:
            bm = g2["beta_mean"]
            a3.plot(ss, 1 - 2 * bm * ss, "--", color=C["good"], lw=2.0,
                    label=f"prediction from panel B ($\\beta$={bm:.2f})")
        a3.axhline(0, color=C["grey"], lw=1.0)
        a3.set_xlabel("dissipation exponent $s$")
        a3.set_ylabel("relevance exponent $p$ in $D/N \\sim (T-t)^p$")
        a3.set_title("D. What the direct route DOES still show:\n"
                     "the sign structure, not the location of the zero", fontsize=10)
        a3.legend(fontsize=7.5)
    a3.grid(alpha=0.25)

    # ---- E: the cross-model calibration -----------------------------------
    a4 = ax[1, 1]
    g4 = d.get("g4_cross_model")
    if g4:
        pa = g4["positive_a"]
        a4.plot([r["a"] for r in pa], [r["beta"] for r in pa], "o-",
                color=C["anchor"], label=r"gCLM $\beta(a)=1/\alpha(a)$ (Route-E)")
        na = [r for r in g4["negative_a"] if "beta" in r and r["K"] == 96]
        if na:
            na = sorted(na, key=lambda r: r["a"])
            a4.plot([r["a"] for r in na], [r["beta"] for r in na], "s--",
                    color=C["warn"], label="continuation to $a<0$ (not converged)")
        a4.axhline(0.5, color=C["ns"], ls="--", lw=1.6, label=r"NS line $\beta=1/2$")
        a4.axhline(g4["target_beta"], color=C["good"], ls="-.", lw=1.8,
                   label=f"Chen-Hou 2D  $\\beta$={g4['target_beta']:.3f}")
        a4.axvline(g4["a_at_NS_line"], color=C["ns"], ls=":", lw=1.0)
        a4.annotate(f"gCLM crosses NS at\n$a\\approx{g4['a_at_NS_line']:.3f}$",
                    (g4["a_at_NS_line"], 0.5), textcoords="offset points",
                    xytext=(6, 22), fontsize=8, color=C["ns"])
        a4.set_xlabel("gCLM advection parameter $a$")
        a4.set_ylabel(r"collapse exponent $\beta$")
        a4.set_title("E. The toy and its target are on OPPOSITE sides\n"
                     "of the NS line, and far apart", fontsize=10)
        a4.legend(fontsize=7)
    a4.grid(alpha=0.25)

    # ---- F: who beats the ordinary Laplacian ------------------------------
    a5 = ax[1, 2]
    rows = [r for r in d["g0_law"]["rows"] if "NAVIER" not in r["object"]]
    if g2:
        rows = rows + [{"object": f"2D Boussinesq (OUR machine)",
                        "beta": g2["beta_mean"],
                        "p_at_s1": float(1 - 2 * g2["beta_mean"])}]
    rows = sorted(rows, key=lambda r: r["p_at_s1"])
    names = [r["object"].split(" (")[0][:30] for r in rows]
    vals = [r["p_at_s1"] for r in rows]
    cols = [C["good"] if v > 0 else C["bad"] for v in vals]
    a5.barh(range(len(vals)), vals, color=cols, alpha=0.8)
    a5.axvline(0, color="k", lw=1.2)
    a5.plot([0], [len(vals)], "*", ms=1)
    a5.set_yticks(range(len(names)))
    a5.set_yticklabels(names, fontsize=8)
    a5.set_xlabel(r"$p(s{=}1) = 1 - 2\beta$   (>0: beats ordinary viscosity)")
    a5.set_title("F. At the ORDINARY Laplacian.\n"
                 "NS sits exactly at 0 -- which is the whole problem", fontsize=10)
    a5.axvline(0.0, color=C["ns"], lw=2.0, alpha=0.5)
    a5.grid(alpha=0.25, axis="x")

    fig.suptitle("Route-G v1 -- the critical dissipation exponent on the 2D object: "
                 r"$s_c = 1/(2\beta)$, and where each blow-up sits relative to "
                 "Navier-Stokes", fontsize=12.5)
    fig.tight_layout(rect=[0, 0, 1, 0.965])
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig36_route_g_v1_collapse.png"
    fig.savefig(out, dpi=135)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
