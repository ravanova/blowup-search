"""Phase-2 P2 Route-H v1 (fig37): the MARGINAL case -- what happens AT s = s_c.

Route-F (fig35) and Route-G (fig36) located the critical dissipation exponent and both
stopped at the same wall: AT s = s_c the two terms balance identically, so the scaling
argument returns zero information.  That point is exactly where Navier-Stokes sits.

This leg makes the marginal case answerable by promoting the dissipation coefficient to
a dynamical variable of the rescaled flow,

    mu := nu / (A L^{2s}) ,      mu_tau = (2s - alpha[Omega, mu]) mu ,

so Route-F's s_c becomes the EIGENVALUE 2s - alpha_0, and at criticality that eigenvalue
is exactly zero -- leaving the quadratic term, mu_tau = -alpha_1 mu^2, and one number:
alpha_1 = d alpha / d mu.

Rebuilds fig37 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_h_v1_evidence.py
Regenerate the data (deterministic; ~20 min):
    .venv/bin/python -u experiments/p2_route_h_v1_critical.py

Six panels: A the eigenvalue reading of s_c, with the marginal point marked; B the a = 0
neutral line (alpha == 1 at every mu, against the closed-form solution); C the a = 1/2
secant extrapolation that gives alpha_1, with its K-ladder; D the DSS re-ask -- the
converged spectrum with dissipation on, and the one mode that moves; E the
time-dependent cross-check at s = 1/2 exactly; F what (M) does, in tau.
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
JSON = DATA / "p2_route_h_v1_critical.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ns": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: s_c is an eigenvalue, and at criticality it is zero -----------
    a0 = ax[0, 0]
    s = np.linspace(0.0, 3.0, 400)
    # the third point is REFUSED (H4): drawn greyed, so the figure cannot be read as
    # three measured points when only two are.
    reached3 = bool(d["h4_third_point"].get("reached"))
    pts = [(1.0, 0.5, r"$a=0$  ($\alpha=1$): $\alpha_1=0$", C["anchor"], True),
           (3.0, 1.5, r"$a=1/2$  ($\alpha=3$): $\alpha_1>0$", C["bad"], True),
           (5.0, 2.5, r"$a=0.58218$  ($\alpha=5$): %s"
            % ("measured" if reached3 else "NOT REACHED"), C["grey"], reached3)]
    for alpha0, sc, label, col, ok in pts:
        a0.plot(s, 2.0 * s - alpha0, color=col, lw=2.0 if ok else 1.4,
                ls="-" if ok else ":", label=label)
        a0.plot([sc], [0.0], "o" if ok else "x", ms=9, color=col, zorder=5,
                mew=2.0)
    a0.axhline(0.0, color="k", lw=1.0)
    a0.axvline(1.0, color=C["ns"], ls="--", lw=1.6)
    a0.text(1.03, -4.5, "NS sits here\n($s=1$, ordinary Laplacian)", fontsize=8.5,
            color=C["ns"])
    a0.fill_between(s, -6, 0, color=C["good"], alpha=0.07)
    a0.text(0.08, -5.6, "dissipation IRRELEVANT\n($\\lambda_\\mu<0$: $\\mu\\to0$)",
            fontsize=8.5, color=C["good"])
    a0.set_xlabel("dissipation exponent $s$")
    a0.set_ylabel(r"$\lambda_\mu = 2s - \alpha_0$")
    a0.set_title("A. Route-F's $s_c$ is a STABILITY EIGENVALUE\n"
                 "and at $s=s_c$ it is exactly zero", fontsize=10.5)
    a0.set_ylim(-6, 2)
    a0.legend(fontsize=8, loc="upper left")
    a0.grid(alpha=0.25)

    # ---- B: the a = 0 neutral line ----------------------------------------
    b0 = ax[0, 1]
    h2 = d["h2_a0"]
    mu = np.array([r["mu"] for r in h2["rows"]])
    al = np.array([r["alpha"] for r in h2["rows"]])
    err = np.array([r["closed_form_error"] for r in h2["rows"]])
    # ABSOLUTE values on a log axis, not signed on a symlog: the signed version reads
    # as wild oscillation when the whole excursion is 1e-16, i.e. the sign is noise.
    FLOOR = 1e-18
    b0.plot(mu, np.maximum(np.abs(al - 1.0), FLOOR), "o-", color=C["anchor"], lw=1.8,
            ms=7, label=r"$|\alpha(\mu)-1|$ (Newton, cold start)")
    b0.plot(mu, np.maximum(err, FLOOR), "s--", color=C["good"], lw=1.4, ms=6,
            label=r"$\|\Omega_{\rm num}-\Omega_{\rm exact}\|_\infty$")
    b0.axhspan(FLOOR, 2.3e-16, color=C["grey"], alpha=0.18)
    b0.text(2.05, 3e-17, "machine precision", fontsize=8, color=C["grey"])
    b0.set_yscale("log")
    b0.set_ylim(FLOOR, 1e-11)
    b0.set_xlabel(r"$\mu = \nu/(AL^{2s})$")
    b0.set_title("B. $a=0$: $\\alpha\\equiv1$ at EVERY $\\mu$\n"
                 r"$\alpha_1=%.1e$ $\Rightarrow$ a LINE of viscous self-similar blow-ups"
                 % h2["slope"]["alpha_1"], fontsize=10.5)
    b0.legend(fontsize=8, loc="upper left")
    b0.grid(alpha=0.25)

    # ---- C: the a = 1/2 secant extrapolation ------------------------------
    c0 = ax[0, 2]
    lad = d["h3_a_half"]["ladder"]
    for row, col in zip(lad, (C["grey"], C["warn"], C["bad"], C["anchor"])):
        m = np.array(row["mu"], float)
        m = m[m > 0]
        sec = np.array(row["secants"], float)
        c0.plot(m, sec, "o-", ms=5, lw=1.5, color=col, label="K=%d" % row["K"])
        c0.plot([0.0], [row["alpha_1"]], "*", ms=13, color=col, zorder=5)
    # the CHORD is what a straight fit of alpha vs mu returns, and it is 5.5% low --
    # draw it, because the whole reason the secants exist is to correct it.
    c0.axhline(lad[-1]["alpha_1_chord"], color=C["good"], ls="--", lw=1.6,
               label="chord (a straight fit of\n$\\alpha$ vs $\\mu$): %.5f"
                     % lad[-1]["alpha_1_chord"])
    c0.set_xlabel(r"$\mu$")
    c0.set_ylabel(r"secant $(\alpha(\mu)-\alpha_0)/\mu$")
    c0.set_xlim(left=-0.012)
    allv = [v for row in lad for v in row["secants"]] + \
           [row["alpha_1"] for row in lad] + [lad[-1]["alpha_1_chord"]]
    lo, hi = min(allv), max(allv)
    pad = 0.12 * (hi - lo)
    c0.set_ylim(lo - pad, hi + pad)
    c0.set_title("C. $a=1/2$, $s=3/2$: the secants extrapolate to\n"
                 r"$\alpha_1=%.5f>0$ (K-spread %.1e) $\Rightarrow$ $\mu$ DECAYS"
                 % (d["h3_a_half"]["alpha_1"], d["h3_a_half"]["K_spread"]),
                 fontsize=10.5)
    c0.legend(fontsize=8, loc="lower right")
    c0.grid(alpha=0.25)

    # ---- D: the DSS re-ask ------------------------------------------------
    d0 = ax[1, 0]
    rows = d["h5_dss"]["rows"]
    cmap = plt.get_cmap("viridis")
    mus = [r["mu"] for r in rows]
    for r in rows:
        col = cmap(mus.index(r["mu"]) / max(1, len(mus) - 1))
        d0.plot(r["kept_real"], r["kept_imag"], "o", ms=6, color=col, alpha=0.85,
                label=r"$\mu=%.2f$" % r["mu"])
    mm = np.linspace(0.0, max(mus), 200)
    d0.plot(-np.sqrt(1.0 + 4.0 * mm), np.zeros_like(mm), "-", color=C["bad"], lw=1.6,
            label=r"amplitude mode $-\sqrt{1+4\mu}$")
    d0.axvline(0.0, color="k", lw=1.0)
    # name the one thing that is off the real axis, rather than leaving two dots to be
    # read as structure: it is a DEGENERATE REAL PAIR split at the 1e-5 level.
    worst_im = max((r.get("max_abs_imag") or 0.0) for r in rows)
    if worst_im > 0:
        d0.annotate("degenerate real pair split by\n$|\\mathrm{Im}|=%.1e$ — noise, "
                    "not a Hopf" % worst_im, xy=(-3.0, -worst_im),
                    xytext=(-6.9, -0.62 * worst_im), fontsize=8, color=C["bad"],
                    arrowprops=dict(arrowstyle="->", color=C["bad"], lw=1.0))
    d0.set_xlabel(r"$\mathrm{Re}\,\lambda$")
    d0.set_ylabel(r"$\mathrm{Im}\,\lambda$")
    d0.set_title("D. DSS re-ask: dissipation does NOT open a Hopf\n"
                 "no converged eigenvalue is complex or in $\\mathrm{Re}>0$ "
                 "(control: %d$\\to$%d)"
                 % (d["h5_dss"]["control"]["n_plain"],
                    d["h5_dss"]["control"]["n_planted"]), fontsize=10.5)
    d0.legend(fontsize=7, loc="upper left", ncol=2)
    d0.grid(alpha=0.25)

    # ---- E: the time-dependent cross-check --------------------------------
    e0 = ax[1, 1]
    h7 = d["h7_time_dependent"]
    for i, r in enumerate(h7["rows"]):
        vals = list(r["p_windows"].values())
        e0.plot([i] * len(vals), vals, "o", ms=8, color=C["anchor"], alpha=0.8)
        e0.plot([i], [r["p"]], "_", ms=26, color=C["bad"], lw=2.5)
    e0.axhline(0.0, color=C["good"], lw=2.0, ls="--", label="predicted $p=0$ at $s=s_c$")
    e0.set_xticks(range(len(h7["rows"])))
    e0.set_xticklabels([r"$\nu=$%.0e" % r["nu"] for r in h7["rows"]], fontsize=8)
    e0.set_ylabel(r"fitted $p$ in $D/N\sim(T-t)^p$")
    e0.set_title("E. INDEPENDENT machinery at $s=1/2$ exactly:\n"
                 "time-dependent periodic solver, mean $p=%+.3f$ (spread %.3f)"
                 % (h7["p_mean"], h7["p_spread"]), fontsize=10.5)
    e0.legend(fontsize=8)
    e0.grid(alpha=0.25)

    # ---- F: what (M) does -------------------------------------------------
    f0 = ax[1, 2]
    tau = np.linspace(0.0, 400.0, 600)
    mu0 = 0.2
    for a1, label, col in ((d["h3_a_half"]["alpha_1"],
                            r"$a=1/2$: $\alpha_1=%.4f$" % d["h3_a_half"]["alpha_1"],
                            C["bad"]),
                           (0.0, r"$a=0$: $\alpha_1=0$ (neutral line)", C["anchor"])):
        f0.plot(tau, mu0 / (1.0 + a1 * mu0 * tau), lw=2.2, color=col, label=label)
    f0.plot(tau, mu0 * np.exp(-0.1 * tau), ls=":", lw=1.8, color=C["grey"],
            label=r"what an OFF-critical $s$ would do ($e^{-|\lambda_\mu|\tau}$)")
    f0.set_yscale("log")
    f0.set_ylim(1e-4, 0.4)
    f0.set_xlabel(r"rescaled time $\tau$")
    f0.set_ylabel(r"$\mu(\tau)$")
    v = d["h6_verdict"]
    f0.set_title("F. The marginal verdict: $\\mu$ decays ALGEBRAICALLY.\n"
                 r"$\mu:0.2\to0.02$ costs $\tau=%.0f$; $\to0.002$ costs $\tau=%.0f$"
                 % (v[1]["tau_mu_0.2_to_0.02"], v[1]["tau_mu_0.2_to_0.002"]),
                 fontsize=10.5)
    f0.legend(fontsize=8, loc="lower left")
    f0.grid(alpha=0.25)

    fig.suptitle("Route-H v1 — the MARGINAL case ($s=s_c$ exactly), where every scaling "
                 "argument returns zero information.  Plain float64, NOT rigorous; a toy "
                 "model, not Navier–Stokes.", fontsize=11.5)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig37_route_h_v1_critical.png"
    fig.savefig(out, dpi=135)
    print("wrote", out)


if __name__ == "__main__":
    build_figure()
