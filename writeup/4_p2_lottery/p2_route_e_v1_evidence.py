"""Phase-2 P2 Route-E v1 (fig34): the spectrum of the rescaled gCLM flow at its
self-similar fixed point -- the cheapest test of the Hopf route into the DSS lane.

A DSS blow-up is a PERIODIC ORBIT of the dynamically-rescaled flow, and the cheapest
way for one to exist near what this project already has is a Hopf bifurcation off the
self-similar FIXED POINT.  This leg computes that fixed point's spectrum along the
whole gCLM branch and finds that the only grid-converged eigenvalues are the two
SYMMETRY modes -- 0 (dilation) and -1 (amplitude) -- which are exact at every a for
algebraic reasons, carry no dynamical information, and cannot cross anything.  There
is no eigenvalue available to undergo a Hopf bifurcation.  Negative with a mechanism,
plus two by-products: the far-field exponent map alpha(a) and an analytic resonance
at a = 1/2 where alpha = 3 exactly.

Rebuilds fig34 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_e_v1_evidence.py
Regenerate the data (deterministic; ~20 min):
    .venv/bin/python -u experiments/p2_route_e_v1_spectrum.py

Six panels: A the branch alpha(a); B spectral vs algebraic convergence; C the
residual dip that locates the analytic resonance; D the a=0 spectrum against the
analytically known continuum strip; E the converged spectrum vs a (the DSS verdict);
F the positive control.
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
JSON = DATA / "p2_route_e_v1_spectrum.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def cx(pairs):
    arr = np.asarray(pairs, float)
    if arr.size == 0:
        return np.array([], complex)
    return arr[:, 0] + 1j * arr[:, 1]


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.6))

    # ---- A: the branch alpha(a) -------------------------------------------
    E7 = d["E7_end"]
    a0 = ax[0, 0]
    rows = [r for r in E7["rows"] if r["ok"]]
    aa = np.array([r["a"] for r in rows])
    al = np.array([-r["c_omega"] for r in rows])
    a0.plot(aa, al, "-", color=C["anchor"], lw=2,
            label="$\\alpha(a) = -c_\\omega(a)$  (K=%d)" % E7["K"])
    E2 = d["E2_branch"]
    a0.plot([r["a"] for r in E2], [r["alpha"] for r in E2], "o", color=C["good"],
            ms=6, label="Richardson-extrapolated (K=64/128/256)")
    for a_res, al_res, lab in ((0.0, 1.0, "$\\alpha=1$ (CLM, exact)"),
                               (0.5, 3.0, "$\\alpha=3$ (analytic resonance)")):
        a0.plot([a_res], [al_res], "*", color=C["bad"], ms=15, zorder=5)
        a0.annotate(lab, (a_res, al_res), textcoords="offset points",
                    xytext=(12, -4), fontsize=8, color=C["bad"])
    ac = E7.get("a_c_linear_extrapolation", float("nan"))
    if np.isfinite(ac):
        a0.axvline(ac, color=C["grey"], ls=":", lw=1.3)
        a0.text(ac, 0.55 * a0.get_ylim()[1], "  $1/\\alpha \\to 0$\n  at $a\\approx%.3f$" % ac,
                fontsize=7.5, color=C["grey"])
    a0.set_xlabel("$a$")
    a0.set_ylabel("far-field exponent $\\alpha$  ($\\Omega \\sim X^{-\\alpha}$)")
    a0.set_title("A  the self-similar branch\n"
                 "the decay exponent is an OUTPUT and it runs away", fontsize=10)
    a0.legend(fontsize=7.2, loc="upper left")
    a0.grid(alpha=0.3)

    # ---- B: spectral vs algebraic convergence ------------------------------
    E3 = d["E3_resonance"]
    a1 = ax[0, 1]
    for key, col, lab in (("a=0.30", C["bad"], "$a=0.3$: $\\alpha$ non-integer"),
                          ("a=0.50", C["good"], "$a=0.5$: $\\alpha=3$, analytic")):
        r = E3[key]
        a1.loglog(r["K"], np.maximum(r["residual"], 1e-17), "o-", color=col, label=lab)
    Kk = np.array(E3["a=0.30"]["K"], float)
    ref = E3["a=0.30"]["residual"][0] * (Kk / Kk[0]) ** -2.0
    a1.loglog(Kk, ref, ":", color=C["grey"], label="$K^{-2}$ reference")
    a1.set_xlabel("K (sine modes)")
    a1.set_ylabel("fixed-point residual $\\sup|R|$")
    a1.set_title("B  the profile's own regularity sets the rate\n"
                 "branch point of order $\\alpha$ at $X=\\infty$", fontsize=10)
    a1.legend(fontsize=7.2)
    a1.grid(alpha=0.3, which="both")

    # ---- C: the resonance scan --------------------------------------------
    S = E3["scan"]
    a2 = ax[0, 2]
    a2.semilogy(S["a"], np.maximum(S["residual"], 1e-16), "-", color=C["anchor"], lw=1.6)
    i = int(np.argmin(np.array(S["residual"][1:]))) + 1
    a2.plot([S["a"][i]], [max(S["residual"][i], 1e-16)], "*", color=C["bad"], ms=16)
    a2.annotate("$a=%.2f$, $\\alpha=%.6f$\n$|R| = %.1e$"
                % (S["a"][i], -S["c_omega"][i], S["residual"][i]),
                (S["a"][i], max(S["residual"][i], 1e-16)),
                textcoords="offset points", xytext=(14, 18), fontsize=8, color=C["bad"])
    a2.set_xlabel("$a$")
    a2.set_ylabel("fixed-point residual at K=%d" % S["K"])
    a2.set_title("C  one value of $a$ is special\n"
                 "$\\alpha$ odd integer $\\Rightarrow$ analytic $\\Rightarrow$ spectral", fontsize=10)
    a2.grid(alpha=0.3, which="both")

    # ---- D: the a = 0 spectrum vs the analytic strip -----------------------
    E5 = d["E5_sweep"]
    a3 = ax[1, 0]
    row0 = [r for r in E5 if abs(r["a"]) < 1e-9][0]
    ev = cx(row0.get("ev_coarse_sample", [])) if "ev_coarse_sample" in row0 else None
    a3.axvspan(-1, 1, color=C["warn"], alpha=0.13)
    a3.text(-0.95, 0.90, "analytic continuum strip\n$-1 < \\mathrm{Re}\\,\\lambda < 1$\n"
                         "eigenfunctions $(w-1)^{1-\\lambda}(w+1)^{1+\\lambda}$\n"
                         "— fractional power at $X=0$",
            transform=a3.get_yaxis_transform(), fontsize=7, va="top",
            bbox=dict(fc="white", ec=C["warn"], alpha=0.95))
    E1 = d["E1_anchor"]
    for r, mk in zip(E1, ["o", "s", "^", "v"]):
        a3.plot([0.0] * 2, [r["max_abs_im"], -r["max_abs_im"]], mk, color=C["grey"],
                ms=4, alpha=0.6)
    kept0 = cx(row0["kept_ref"])
    a3.plot(kept0.real, kept0.imag, "*", color=C["good"], ms=17, zorder=6,
            label="grid-converged (2 of %d)" % row0.get("n_total", 96))
    a3.axvline(0, color="k", lw=0.8)
    a3.set_xlim(-1.6, 1.6)
    a3.set_xlabel("$\\mathrm{Re}\\,\\lambda$")
    a3.set_ylabel("$\\mathrm{Im}\\,\\lambda$")
    a3.set_title("D  $a=0$: the whole discretized spectrum\n"
                 "everything but two points sits on the axis and MOVES", fontsize=10)
    a3.legend(fontsize=7.5, loc="lower right")
    a3.grid(alpha=0.3)

    # ---- E: the converged spectrum vs a  (the verdict) ---------------------
    a4 = ax[1, 1]
    for r in E5:
        k = cx(r["kept_ref"])
        if k.size:
            a4.plot([r["a"]] * k.size, k.real, "o", color=C["good"], ms=7)
    a4.axhline(0.0, color=C["anchor"], ls="--", lw=1.2)
    a4.axhline(-1.0, color=C["anchor"], ls="--", lw=1.2)
    a4.text(0.02, 0.06, "$\\lambda = 0$: dilation  ($L(X\\Omega_X)=0$)", fontsize=8,
            color=C["anchor"])
    a4.text(0.02, -0.94, "$\\lambda = -1$: amplitude  ($L\\Omega = -\\Omega + X\\Omega_X$)",
            fontsize=8, color=C["anchor"])
    a4.axhspan(0.02, 1.4, color=C["bad"], alpha=0.09)
    a4.text(0.30, 0.75, "nothing here at any $a$\n$\\Rightarrow$ no Hopf, no periodic orbit",
            fontsize=8.5, color=C["bad"], ha="center")
    a4.set_ylim(-1.5, 1.4)
    a4.set_xlabel("$a$")
    a4.set_ylabel("$\\mathrm{Re}\\,\\lambda$ (grid-converged only)")
    a4.set_title("E  THE VERDICT: only the two symmetry modes survive\n"
                 "they are exact at every $a$ and cannot cross", fontsize=10)
    a4.grid(alpha=0.3)
    counts = " ".join("%.2f:%s" % (r["a"], r["counts"]["0.01"]) for r in E5)
    a4.text(0.02, 0.02, "kept at tol=$10^{-2}$ — " + counts, transform=a4.transAxes,
            fontsize=6.6, bbox=dict(fc="white", ec=C["grey"], alpha=0.95))

    # ---- F: the positive control ------------------------------------------
    E6 = d["E6_control"]
    a5 = ax[1, 2]
    for j, r in enumerate(E6):
        plain = cx(r["plain"])
        planted = cx(r["planted"])
        a5.plot(plain.real, [j + 0.12] * plain.size, "o", color=C["grey"], ms=9,
                label="plain operator" if j == 0 else None)
        a5.plot(planted.real, [j - 0.12] * planted.size, "*", color=C["bad"], ms=15,
                label="with planted potential" if j == 0 else None)
        a5.text(-2.4, j, "$V=%.0f$" % r["strength"], fontsize=8, va="center")
    a5.axvline(0.0, color="k", lw=0.8)
    a5.axvspan(0.0, 2.0, color=C["bad"], alpha=0.09)
    a5.set_xlim(-2.6, 2.0)
    a5.set_yticks([])
    a5.set_xlabel("$\\mathrm{Re}\\,\\lambda$ of the CONVERGED eigenvalues")
    a5.set_title("F  positive control: the filter can see\n"
                 "an unstable eigenvalue when one is planted", fontsize=10)
    a5.legend(fontsize=7.5, loc="upper right")
    a5.grid(alpha=0.3, axis="x")

    fig.suptitle("Route-E v1 — the rescaled gCLM flow has no eigenvalue available for a Hopf "
                 "bifurcation: the only grid-converged spectrum is the two exact symmetry modes",
                 fontsize=12.5)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig34_p2_route_e_v1_spectrum.png"
    fig.savefig(out, dpi=145)
    print("wrote", out)


if __name__ == "__main__":
    build_figure()
