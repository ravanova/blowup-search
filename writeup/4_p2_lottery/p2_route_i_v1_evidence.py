"""Phase-2 P2 Route-I v1 (fig38): the marginal flow DRIVEN, not read off a branch.

Route-H (fig37) wrote the augmented flow -- dissipation's coefficient mu promoted to a
dynamical variable of the rescaled system -- and read it STATICALLY: Newton at frozen mu,
alpha off the branch, the dynamics inferred.  This leg integrates the coupled system as
an initial-value problem, which makes two inferred numbers into measured ones and answers
the piece of ranked item (2) that the scaling legs left open: does a viscous solution
actually REACH the self-similar form?

Rebuilds fig38 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_i_v1_evidence.py
Regenerate the data (deterministic; ~15 min):
    .venv/bin/python -u experiments/p2_route_i_v1_driven.py

Six panels: A lambda_mu = 2s - alpha_0 as a measured GROWTH RATE (Route-F's s_c, from a
trajectory); B the tar pit driven -- mu(tau) against the closed law, with the dynamic and
static alpha_1 K-ladders side by side; C adiabaticity, and off-branch starts joining;
D THE STABILITY INVERSION -- unstable directions against mu, with the crossover that
shows the limits do not commute; E where the instability lives (Re against |Im|: the
log-periodic band); F the nonlinear control, twin trajectories against the spectral gap.
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
JSON = DATA / "p2_route_i_v1_driven.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ns": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: s_c as a measured growth rate ---------------------------------
    a0 = ax[0, 0]
    i2 = d["i2_lambda_mu"]
    kept = [r for r in i2["rows"] if not r.get("refused")]
    main = [r for r in kept if r["a"] == d["a_crit"]]
    other = [r for r in kept if r["a"] != d["a_crit"]]
    refused = [r for r in i2["rows"] if r.get("refused")]
    s = np.linspace(0.3, 2.7, 100)
    a0.plot(s, 2 * s - d["alpha_0"], lw=2.0, color=C["good"],
            label=r"predicted $\lambda_\mu = 2s-\alpha_0$")
    a0.plot([r["s"] for r in main], [r["measured"] for r in main], "o", ms=9,
            color=C["bad"], label=r"measured $d(\log\mu)/d\tau$, $a=1/2$")
    if other:
        a0.plot([r["s"] for r in other], [r["measured"] for r in other], "s", ms=7,
                mfc="none", color=C["anchor"],
                label=r"$a=0.3$ ($\alpha_0=%.3f$, non-integer)" % other[0]["alpha_0"])
        a0.plot(s, 2 * s - other[0]["alpha_0"], lw=1.2, ls="--", color=C["anchor"])
    for r in refused:
        a0.plot([r["s"]], [r["predicted"]], "x", ms=10, mew=2.0, color=C["grey"])
    if refused:
        a0.plot([], [], "x", ms=9, mew=2.0, color=C["grey"],
                label="REFUSED (%d: left the linear regime,\nor the rung gate failed)"
                % len(refused))
    a0.axhline(0.0, color=C["grey"], lw=1.0)
    a0.axvline(d["alpha_0"] / 2, color=C["ns"], lw=1.6, ls=":",
               label=r"$s_c=\alpha_0/2$: the MARGINAL point")
    a0.set_xlabel("dissipation exponent $s$")
    a0.set_ylabel(r"$\lambda_\mu$")
    a0.set_title("A. Route-F's $s_c$, measured as a GROWTH RATE.\n"
                 "slope %+.4f (pred. +2), zero at $s=%.4f$ (pred. %.3f); "
                 "worst |err| %.1e"
                 % (i2["slope"], i2["zero"], i2["zero_predicted"],
                    i2["worst_abs_error"]), fontsize=10.5)
    a0.legend(fontsize=7.5, loc="upper left")
    a0.grid(alpha=0.25)

    # ---- B: the tar pit, driven -------------------------------------------
    b0 = ax[0, 1]
    lr = d["i3_tar_pit"]["long_run"]
    tau = np.array(lr["tau"])
    mu = np.array(lr["mu"])
    b0.plot(tau, mu, lw=2.4, color=C["bad"], label=r"integrated $\mu(\tau)$")
    law = 1.0 / (1.0 / mu[0] + lr["alpha_1_used"] * tau)
    b0.plot(tau, law, lw=1.4, ls="--", color=C["good"],
            label=r"$1/(1/\mu_0+\alpha_1\tau)$  (worst dev %.2f%%)"
            % (lr["law_max_rel_dev"] * 100))
    b0.plot(tau, mu[0] * np.exp(-0.5 * tau), ls=":", lw=1.6, color=C["grey"],
            label=r"what an OFF-critical $s$ would do")
    b0.set_yscale("log")
    b0.set_ylim(max(1e-3, 0.5 * mu.min()), 0.5)
    b0.set_xlabel(r"rescaled time $\tau$")
    b0.set_ylabel(r"$\mu(\tau)$")
    kl = d["i3_tar_pit"]["k_ladder"]
    b0.plot([], [], " ", label=r"$\alpha_1$ dynamic/static, converging:")
    for r in kl:
        b0.plot([], [], " ", label="   K=%d:  %.5f / %.5f  (%.2f%%)"
                % (r["K"], r["dynamic"], r["static"],
                   100 * abs(r["dynamic"] - r["static"]) / r["static"]))
    b0.set_title("B. The tar pit, DRIVEN: $\\mu(\\tau)$ against its closed law,\n"
                 r"with $\alpha_1$ read off the TRAJECTORY", fontsize=10.5)
    b0.legend(fontsize=7.5, loc="lower left")
    b0.grid(alpha=0.25)

    # ---- C: adiabaticity ---------------------------------------------------
    c0 = ax[0, 2]
    i4 = d["i4_adiabaticity"]
    c0.semilogy(i4["branch_tau"], i4["branch_dist"], "o-", ms=3.5, lw=1.4,
                color=C["anchor"], label=r"$\|\Omega(\tau)-\Omega^*(\mu(\tau))\|_\infty$")
    c0.set_xlabel(r"rescaled time $\tau$")
    c0.set_ylabel("relative distance to the frozen-$\\mu$ branch")
    # A REFUSED ROW MUST READ "REFUSED", NOT "nan".  The first version of this legend
    # printed `alpha_1 = nan` three times, because every off-branch run had overflowed
    # and nothing checked (banked lesson 65).
    lines = []
    for r in i4["off_branch"]:
        if r.get("converged") and r.get("alpha_1") is not None:
            lines.append(r"off-branch $\epsilon=%g$: $\mu$ within %.3f%%, $\alpha_1=%.5f$"
                         % (r["eps"], r["rel_to_on_branch"] * 100, r["alpha_1"]))
        else:
            lines.append(r"off-branch $\epsilon=%g$: REFUSED (diverged at $\tau=%s$)"
                         % (r["eps"], r.get("diverged_at_tau")))
    prof = i4.get("off_branch_profile_relative_at_eps_0.05")
    if prof is not None:
        lines.append(r"…but $\epsilon=0.05$ is only $%.0e$ of $\Omega$: this tests the"
                     % prof)
        lines.append(r"GAUGE direction (cond $\sim K^4$), NOT the basin — see F")
    c0.text(0.03, 0.06, "\n".join(lines), transform=c0.transAxes, fontsize=7.0,
            va="bottom", bbox=dict(fc="white", alpha=0.85, ec=C["grey"]))
    c0.set_title("C. The trajectory HUGS the branch, and tightens:\n"
                 "%.1e $\\to$ %.1e — the static reading's assumption, measured"
                 % (i4["dist_first"], i4["dist_last"]), fontsize=10.5)
    c0.legend(fontsize=8, loc="upper right")
    c0.grid(alpha=0.25)

    # ---- D: THE STABILITY INVERSION ---------------------------------------
    d0 = ax[1, 0]
    lad = d["i5_stability"]["ladders"]
    floor = 3e-9
    for K, col in zip(sorted(lad, key=int), (C["grey"], C["anchor"], C["bad"])):
        rows = lad[K]["rows"]
        x = [max(r["mu"], floor) for r in rows]
        d0.plot(x, [max(r["n_unstable"], 0.3) for r in rows], "o-", ms=5, lw=1.5,
                color=col, label="K=%s (inviscid: %d unstable, max Re %+.2f)"
                % (K, lad[K]["n_unstable_inviscid"], lad[K]["max_re_inviscid"]))
        cr = lad[K]["crossover"]["bracket"]
        d0.axvspan(cr[0], cr[1], color=col, alpha=0.10)
        d0.plot([lad[K]["crossover_predicted"]], [0.45], "v", ms=8, color=col)
    d0.set_xscale("log")
    d0.set_yscale("log")
    d0.set_xlabel(r"$\mu$   (leftmost point is $\mu=0$ exactly)")
    d0.set_ylabel("unstable directions (Re $>10^{-6}$)")
    rr = d["i5_stability"]["crossover_ratios"]
    d0.set_title("D. THE INVERSION: $\\mu=0$ is violently unstable, any\n"
                 "$\\mu>0$ is not.  Crossover $\\times$%.1f/$\\times$%.1f per K-doubling"
                 " ($\\mu_*\\!\\sim\\!\\mathrm{Re}_{\\max}/K^p$ predicts "
                 "$\\times$%.0f/$\\times$%.0f)"
                 % (rr["48->96"]["measured"], rr["96->144"]["measured"],
                    rr["48->96"]["predicted"], rr["96->144"]["predicted"]),
                 fontsize=9.5)
    d0.legend(fontsize=7.5, loc="lower left")
    d0.grid(alpha=0.25)

    # ---- E: where the instability lives -----------------------------------
    e0 = ax[1, 1]
    for fp, col in zip(d["i6_frequency"]["inviscid"],
                       (C["grey"], C["anchor"], C["bad"])):
        caps = sorted(((float(k), v) for k, v in fp["caps"].items()), key=lambda t: t[0])
        e0.plot([c for c, _ in caps], [v["max_re"] for _, v in caps], "o-", ms=5,
                lw=1.5, color=col,
                label="K=%d (max$|$Im$|$=%.0f)" % (fp["K"], fp["max_abs_im"]))
        e0.plot([abs(fp["im_of_max_re"])], [fp["max_re"]], "*", ms=13, color=col)
    visc = d["i6_frequency"]["viscous"]
    e0.axhline(0.0, color=C["good"], lw=2.0, ls="--",
               label=r"$\mu=0.05$: max Re $=%+.1e$ (the whole band is gone)"
               % visc["max_re"])
    e0.set_xscale("log")
    e0.set_xlabel(r"log-frequency cutoff: max Re over $|\mathrm{Im}\,\lambda|\leq$ cap")
    e0.set_ylabel(r"max $\mathrm{Re}\,\lambda$")
    e0.set_title("E. The unstable directions are the LOG-PERIODIC ones\n"
                 "(Route-E's continuum, i.e. the DSS-shaped modes): Re rises\n"
                 "with $|$Im$|$, and max$|$Im$|$ grows with $K$", fontsize=9.5)
    e0.legend(fontsize=7.5, loc="upper left")
    e0.grid(alpha=0.25)

    # ---- F: the nonlinear control -----------------------------------------
    f0 = ax[1, 2]
    for r, col in zip(d["i7_nonlinear"]["rows"],
                      (C["bad"], C["warn"], C["anchor"], C["good"])):
        t, amp = np.array(r["tau"]), np.array(r["amp"])
        f0.semilogy(t, amp / amp[0], lw=1.8, color=col,
                    label=r"$\mu=%g$: rate %+.3f (gap %+.3f)"
                    % (r["mu"], r["rate"], r["gap"]))
    f0.axhline(1.0, color=C["grey"], lw=1.0)
    f0.set_xlabel(r"rescaled time $\tau$")
    f0.set_ylabel("kick amplitude / initial")
    f0.set_title("F. The NONLINEAR control (twin trajectories).\n"
                 "$\\mu>0$: decay rate matches the spectral gap to <1%%.\n"
                 "$\\mu=0$ is a LOWER bound — $dt$ resolves $|$Im$|\\lesssim%.0f$"
                 % d["i7_nonlinear"]["rows"][0]["im_resolved"], fontsize=9.5)
    f0.legend(fontsize=7.5, loc="upper left")
    f0.grid(alpha=0.25)

    fig.suptitle("Route-I v1 — the marginal flow DRIVEN.  The inviscid self-similar profile has "
                 "~K unstable directions; any $\\mu>0$ has none, and $\\mu$ then decays too\n"
                 "slowly to escape.  Plain float64, NOT rigorous; a toy model, not "
                 "Navier–Stokes.", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig38_route_i_v1_driven.png"
    fig.savefig(out, dpi=135)
    print("wrote", out)


if __name__ == "__main__":
    build_figure()
