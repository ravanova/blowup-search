"""Phase-2 P2 Route-E v1 (fig34): the spectrum of the rescaled gCLM flow at its
self-similar fixed point -- the cheapest test of the Hopf route into the DSS lane.

A DSS blow-up is a PERIODIC ORBIT of the dynamically-rescaled flow, and the cheapest way
one could exist near what this project already has is a HOPF BIFURCATION off the
self-similar FIXED POINT.  This leg computes that fixed point's spectrum and finds that
the only grid-converged ISOLATED eigenvalues are the two SYMMETRY modes -- 0 (dilation)
and -1 (amplitude) -- which are exact at every a, carry no dynamical information, and
cannot cross anything.  The apparent THIRD mode at a = 1/2 is the essential spectrum's
left edge, c_omega + 1, and the a = 0 control (where the same edge carries 99% of the
spectrum) is what exposes it.  Negative with a mechanism, plus the far-field exponent map
alpha(a) and an analytic resonance at a = 1/2 with alpha = 3.

Rebuilds fig34 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_e_v1_evidence.py
Regenerate the data (deterministic; ~35 min):
    .venv/bin/python -u experiments/p2_route_e_v1_spectrum.py

Six panels: A the branch alpha(a) and its resonances; B convergence set by the profile's
own regularity; C the residual scan that finds a = 1/2; D the a = 0 spectrum against the
analytically known strip; E THE EIGENVALUE THAT WASN'T (the K-ladder to -2 and the a = 0
control); F the planted-eigenvalue positive control.
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
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

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
            ms=6, label="Richardson (K=64/128/256)")
    marks = [(0.0, 1.0, "$\\alpha=1$ (CLM, exact)"), (0.5, 3.0, "$\\alpha=3$ at $a=1/2$")]
    if "E8c_alpha5_resonance" in d:
        marks.append((d["E8c_alpha5_resonance"]["a_star"], 5.0, "$\\alpha=5$"))
    for a_r, al_r, lab in marks:
        a0.plot([a_r], [al_r], "*", color=C["bad"], ms=14, zorder=5)
        a0.annotate(lab, (a_r, al_r), textcoords="offset points", xytext=(10, -3),
                    fontsize=8, color=C["bad"])
    ac = E7.get("a_c_linear_extrapolation", float("nan"))
    if np.isfinite(ac):
        a0.axvline(ac, color=C["grey"], ls=":", lw=1.3)
        a0.text(ac, 0.45 * a0.get_ylim()[1],
                "  $1/\\alpha \\to 0$\n  at $a\\approx%.3f$" % ac, fontsize=7.5,
                color=C["grey"])
    a0.set_xlabel("$a$")
    a0.set_ylabel("far-field exponent $\\alpha$   ($\\Omega \\sim X^{-\\alpha}$)")
    a0.set_title("A  the self-similar branch\n"
                 "the decay exponent is an OUTPUT, and it runs away", fontsize=10)
    a0.legend(fontsize=7.2, loc="upper left")
    a0.grid(alpha=0.3)

    # ---- B: convergence set by the profile's regularity --------------------
    E3 = d["E3_resonance"]
    a1 = ax[0, 1]
    for key, col, lab in (("a=0.30", C["bad"], "$a=0.3$: $\\alpha$ non-integer"),
                          ("a=0.50", C["good"], "$a=0.5$: $\\alpha=3$, analytic")):
        r = E3[key]
        a1.loglog(r["K"], np.maximum(r["residual"], 1e-17), "o-", color=col, label=lab)
    if "E8c_alpha5_resonance" in d:
        L = d["E8c_alpha5_resonance"]["K_ladder"]
        a1.loglog([r["K"] for r in L], np.maximum([r["residual"] for r in L], 1e-17),
                  "^-", color=C["warn"],
                  label="$\\alpha=5$ ($a=%.5f$)" % d["E8c_alpha5_resonance"]["a_star"])
    Kk = np.array(E3["a=0.30"]["K"], float)
    a1.loglog(Kk, E3["a=0.30"]["residual"][0] * (Kk / Kk[0]) ** -2.0, ":",
              color=C["grey"], label="$K^{-2}$ reference")
    a1.set_xlabel("K (sine modes)")
    a1.set_ylabel("fixed-point residual $\\sup|R|$")
    a1.set_title("B  the profile's own regularity sets the rate\n"
                 "branch point of order $\\alpha$ at $X=\\infty$", fontsize=10)
    a1.legend(fontsize=7.0)
    a1.grid(alpha=0.3, which="both")

    # ---- C: the residual scan ---------------------------------------------
    S = E3["scan"]
    a2 = ax[0, 2]
    a2.semilogy(S["a"], np.maximum(S["residual"], 1e-16), "-", color=C["anchor"], lw=1.6,
                label="K=%d scan" % S["K"])
    i = int(np.argmin(np.array(S["residual"][1:]))) + 1
    a2.plot([S["a"][i]], [max(S["residual"][i], 1e-16)], "*", color=C["bad"], ms=16)
    a2.annotate("$a=%.2f$: $\\alpha=%.10f$\n$|R|=%.1e$ — ten orders deep"
                % (S["a"][i], -S["c_omega"][i], S["residual"][i]),
                (S["a"][i], max(S["residual"][i], 1e-16)), textcoords="offset points",
                xytext=(-30, 30), fontsize=8, color=C["bad"])
    if "E8b_second_resonance" in d:
        B = d["E8b_second_resonance"]["rows"]
        a2.semilogy([r["a"] for r in B], [r["residual"] for r in B], "-",
                    color=C["warn"], lw=1.6, label="fine scan near $\\alpha=5$")
    a2.set_xlabel("$a$")
    a2.set_ylabel("fixed-point residual")
    a2.set_title("C  the resonance was FOUND, not assumed\n"
                 "$\\alpha$ odd integer $\\Rightarrow$ analytic $\\Rightarrow$ spectral",
                 fontsize=10)
    a2.legend(fontsize=7.2, loc="lower left")
    a2.grid(alpha=0.3, which="both")

    # ---- D: the a = 0 spectrum vs the exact strip --------------------------
    a3 = ax[1, 0]
    E9 = d.get("E9_essential_edges", [])
    e9_0 = [r for r in E9 if r["a"] == 0.0]
    a3.axvspan(-1, 1, color=C["warn"], alpha=0.12)
    if e9_0:
        a3.axvspan(e9_0[-1]["left_pred"], e9_0[-1]["right_pred"], color=C["bad"],
                   alpha=0.10)
    E1 = d["E1_anchor"]
    for r in E1:
        a3.plot([0.0, 0.0], [r["max_abs_im"], -r["max_abs_im"]], "|", color=C["grey"],
                ms=9, alpha=0.7)
    a3.plot([0.0], [0.0], "o", color=C["grey"], ms=4,
            label="discretized continuum: 99%% on $c_\\omega+1=0$")
    E5 = d["E5_sweep"]
    kept0 = cx([r for r in E5 if abs(r["a"]) < 1e-9][0]["kept_ref"])
    a3.plot(kept0.real, kept0.imag, "*", color=C["good"], ms=17, zorder=6,
            label="grid-converged: $0$ and $-1$")
    a3.axvline(0, color="k", lw=0.8)
    a3.set_xlim(-1.7, 1.7)
    a3.set_xlabel("$\\mathrm{Re}\\,\\lambda$")
    a3.set_ylabel("$\\mathrm{Im}\\,\\lambda$")
    a3.set_title("D  $a=0$: the answer is known in closed form\n"
                 "continuum $(w-1)^{1-\\lambda}(w+1)^{1+\\lambda}$ on $-1<\\mathrm{Re}\\lambda<1$",
                 fontsize=10)
    a3.legend(fontsize=6.8, loc="lower right")
    a3.grid(alpha=0.3)
    a3.text(0.02, 0.97, "analytic class $\\Rightarrow$ $1-\\lambda \\in \\mathbb{Z}_{\\geq0}$\n"
                        "$\\Rightarrow$ exactly $\\{0,-1\\}$: the two symmetry modes.\n"
                        "$\\lambda=iy$: $X^{1-iy}e^{iy\\tau}$ = a LOG-PERIODIC wave —\n"
                        "the DSS structure, but continuous spectrum.",
            transform=a3.transAxes, fontsize=6.9, va="top",
            bbox=dict(fc="white", ec=C["warn"], alpha=0.95))

    # ---- E: THE EIGENVALUE THAT WASN'T ------------------------------------
    a4 = ax[1, 1]
    if "E8_third_mode" in d:
        L = d["E8_third_mode"]["rows"]
        Ks = [r["K"] for r in L]
        v = [r["near"]["-2"][0] for r in L]
        a4.semilogx(Ks, v, "o-", color=C["bad"], lw=1.8,
                    label="'third eigenvalue' at $a=1/2$")
    a4.axhline(-2.0, color=C["anchor"], ls="--", lw=1.4)
    a4.text(100, -1.9985, "$c_\\omega + 1 = -2$  —  the LEFT EDGE of the\n"
                          "essential spectrum, not a mode", fontsize=8, color=C["anchor"])
    a4.set_xlabel("K")
    a4.set_ylabel("converged value")
    a4.set_title("E  the eigenvalue that wasn't\n"
                 "six digits of grid-convergence, and still an artefact", fontsize=10)
    a4.legend(fontsize=7.5, loc="lower right")
    a4.grid(alpha=0.3, which="both")
    txt = ("THE CONTROL, at $a=0$ where the answer is known:\n"
           "the identical edge sits at $c_\\omega+1 = 0$ and carries\n"
           "99% of the discretized spectrum. Nobody would call\n"
           "that an isolated eigenvalue.\n\n"
           "Strip $[c_\\omega+1,\\; c_\\omega+H\\Omega(0)]$ predicted / measured:")
    if e9_0:
        r0 = e9_0[-1]
        txt += "\n  $a=0$:    $[%+.2f, %+.2f]$ / $[%+.4f, %+.4f]$" % (
            r0["left_pred"], r0["right_pred"], r0["re_min"], r0["re_max"])
    e9_5 = [r for r in E9 if r["a"] == 0.5]
    if e9_5:
        r5 = e9_5[-1]
        txt += "\n  $a=1/2$: $[%+.2f, %+.2f]$ / $[%+.4f, %+.4f]$" % (
            r5["left_pred"], r5["right_pred"], r5["re_min"], r5["re_max"])
    a4.text(0.02, 0.02, txt, transform=a4.transAxes, fontsize=6.6, va="bottom",
            bbox=dict(fc="white", ec=C["good"], alpha=0.96))

    # ---- F: the positive control ------------------------------------------
    E6 = d["E6_control"]
    a5 = ax[1, 2]
    for j, r in enumerate(E6):
        plain, planted = cx(r["plain"]), cx(r["planted"])
        a5.plot(plain.real, [j + 0.13] * plain.size, "o", color=C["grey"], ms=9,
                label="plain operator" if j == 0 else None)
        a5.plot(planted.real, [j - 0.13] * planted.size, "*", color=C["bad"], ms=15,
                label="with a planted potential" if j == 0 else None)
        a5.text(-2.55, j, "$V=%.0f$" % r["strength"], fontsize=8, va="center")
    a5.axvline(0.0, color="k", lw=0.8)
    a5.axvspan(0.0, 5.2, color=C["bad"], alpha=0.08)
    a5.set_xlim(-2.8, 5.2)
    a5.set_yticks([])
    a5.set_xlabel("$\\mathrm{Re}\\,\\lambda$ of the CONVERGED eigenvalues")
    a5.set_title("F  positive control: the filter DOES see\n"
                 "an isolated unstable eigenvalue when one exists", fontsize=10)
    a5.legend(fontsize=7.5, loc="upper right")
    a5.grid(alpha=0.3, axis="x")
    a5.text(0.03, 0.05, "so 'only the two symmetry modes survive'\nis a measurement, not a blind spot",
            transform=a5.transAxes, fontsize=7.2,
            bbox=dict(fc="white", ec=C["good"], alpha=0.95))

    fig.suptitle("Route-E v1 — no eigenvalue is available for a Hopf bifurcation: the only isolated "
                 "grid-converged spectrum is the two exact symmetry modes, and the log-periodic (DSS) "
                 "directions are CONTINUOUS spectrum", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig34_p2_route_e_v1_spectrum.png"
    fig.savefig(out, dpi=145)
    print("wrote", out)


if __name__ == "__main__":
    build_figure()
