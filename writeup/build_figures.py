"""Build the writeup figures from the curated evidence in writeup/data/.

Depends ONLY on the committed writeup/data/*.json (never on the raw run logs),
so the figures rebuild in future with no sweep or GA re-run:

    .venv/bin/python writeup/build_figures.py

Writes PNGs into writeup/figures/.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = Path(__file__).resolve().parent / "data"
FIGS = Path(__file__).resolve().parent / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
    "legend.frameon": False,
})
C_GA, C_RAND, C_LIT = "#2563eb", "#dc2626", "#6b7280"
C_A = {0.7: "#059669", 0.9: "#d97706", 1.0: "#6b7280"}


def load(name):
    return json.loads((DATA / name).read_text())


def fig_ga_vs_random():
    ga = load("ga_vs_random.json")
    seeds = sorted(ga, key=int)
    fig, axes = plt.subplots(1, len(seeds), figsize=(12, 3.6), sharey=True)
    for ax, s in zip(axes, seeds):
        d = ga[s]
        gx = [n for n, v in d["ga_curve"] if v is not None]
        gy = [v for _, v in d["ga_curve"] if v is not None]
        rx = [n for n, v in d["rand_curve"] if v is not None]
        ry = [v for _, v in d["rand_curve"] if v is not None]
        ax.plot(gx, gy, color=C_GA, lw=2, label="GA (evolved)")
        ax.plot(rx, ry, color=C_RAND, lw=2, ls="--", label="random (budget-matched)")
        ax.axhline(d["lit_best"], color=C_LIT, lw=1.2, ls=":", label="best literature")
        ax.set_title(f"seed {s}  (margin {d['margin_over_tol']:.1f}× tol)")
        ax.set_xlabel("cumulative fitness evaluations")
    axes[0].set_ylabel(r"best-so-far  $\nu_{crit}$  (a=0.7)")
    axes[0].legend(loc="lower right", fontsize=8.5)
    fig.suptitle("Stage 2 acceptance: evolutionary search beats budget-matched "
                 "random on 3/3 seeds", fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGS / "fig1_ga_vs_random.png", bbox_inches="tight")
    plt.close(fig)


def fig_resolution_convergence():
    studies = load("stage3_resolution.json")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, role, title in [
        (axes[0], "inviscid_anchor", "Inviscid anchor (ν=0)"),
        (axes[1], "viscous_resistance", "Viscosity-resistance (ν≈0.081)")]:
        rows = [s for s in studies if s["role"] == role]
        for s in rows:
            ax.plot(s["resolutions_tested"], s["t_star_by_resolution"],
                    "o-", lw=1.3, ms=4, color=C_A[0.7], alpha=0.55)
        ax.set_xscale("log", base=2)
        ax.set_xticks(rows[0]["resolutions_tested"])
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.set_xlabel("spectral resolution N")
        ax.set_title(title, fontsize=10)
    axes[0].set_ylabel(r"estimated blow-up time  $T^*$")
    fig.suptitle("Stage 3: T* is resolution-converged for all 9 elites "
                 "(18/18 → NUMERICALLY_CONFIRMED)", fontweight="bold", y=1.0)
    fig.text(0.5, -0.03,
             "Finest-two agreement: inviscid ≤3.5e-6, viscous ≤4.1e-4 "
             "(gate = 2e-2). Flat lines = genuine singularity, not a grid artifact.",
             ha="center", fontsize=8.5, color="#444")
    fig.tight_layout()
    fig.savefig(FIGS / "fig2_resolution_convergence.png", bbox_inches="tight")
    plt.close(fig)


def fig_nongenericity():
    ng = load("nongenericity.json")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3),
                                   gridspec_kw={"width_ratios": [1.1, 1]})
    # left: alpha(256) vs alpha(512), colored by a
    for a in (0.7, 0.9):
        rows = [e for e in ng["per_a"][str(a)]
                if e["a256"] is not None and e["a512"] is not None]
        ax1.scatter([e["a256"] for e in rows], [e["a512"] for e in rows],
                    s=42, color=C_A[a], alpha=0.75, edgecolor="white", lw=0.6,
                    label=f"a={a}")
    ax1.plot([0.2, 3.1], [0.2, 3.1], color="#999", lw=1, ls="--", zorder=0)
    ax1.axhline(1.0, color="#ccc", lw=0.8, zorder=0)
    ax1.axvline(1.0, color="#ccc", lw=0.8, zorder=0)
    ax1.set_xlabel(r"fitted exponent $\alpha$ at N=256")
    ax1.set_ylabel(r"fitted exponent $\alpha$ at N=512")
    ax1.set_title("Exponent stability across resolution", fontsize=10)
    ax1.legend(loc="upper left")
    ax1.annotate("a=0.7: pinned at\n(1,1) — generic CLM", (1.0, 1.0),
                 xytext=(1.35, 0.55), fontsize=8.5, color=C_A[0.7],
                 arrowprops=dict(arrowstyle="->", color=C_A[0.7], lw=1))
    ax1.annotate("a=0.9: rails to 3.0,\ncollapses — grid artifact", (3.0, 0.3),
                 xytext=(1.7, 2.5), fontsize=8.5, color=C_A[0.9],
                 arrowprops=dict(arrowstyle="->", color=C_A[0.9], lw=1))

    # right: per-a health bars
    va = ng["verdicts"]
    a_list = [0.7, 0.9, 1.0]
    blow = [va[str(a)]["n_blowup_either_res"] for a in a_list]
    flips = [va[str(a)]["n_welldef_flips"] for a in a_list]
    nong = [va[str(a)]["n_nongeneric"] for a in a_list]
    x = range(len(a_list))
    ax2.bar([i - 0.25 for i in x], blow, 0.25, color="#94a3b8", label="blow-up (of 40)")
    ax2.bar([i for i in x], flips, 0.25, color=C_A[0.9], label="resolution flips")
    ax2.bar([i + 0.25 for i in x], nong, 0.25, color=C_A[0.7], label="non-generic |α-1|>noise")
    ax2.set_xticks(list(x))
    ax2.set_xticklabels([f"a={a}" for a in a_list])
    ax2.set_title("Where non-genericity lives (and why it fails)", fontsize=10)
    ax2.legend(fontsize=8.5)
    fig.suptitle("Stage 3.5: the GA edge (a=0.7, generic, stable) and the novel "
                 "α≠1 target are disjoint", fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGS / "fig3_nongenericity.png", bbox_inches="tight")
    plt.close(fig)


def fig_blowup_curve():
    d = load("blowup_curve.json")
    t = d["times"]
    m = d["max_omega"]
    inv = [1.0 / v for v in m]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.semilogy(t, m, color="#7c3aed", lw=1.8)
    ax1.set_xlabel("time t")
    ax1.set_ylabel(r"$\max_x|\omega(x,t)|$  (log)")
    ax1.set_title("Vorticity maximum blows up", fontsize=10)
    ax2.plot(t, inv, color="#7c3aed", lw=1.8, label=r"$1/\max|\omega|$")
    ax2.axvline(d["t_star"], color=C_RAND, lw=1.2, ls="--",
                label=fr"$T^*={d['t_star']:.3f}$")
    ax2.axhline(0, color="#ccc", lw=0.8)
    ax2.set_xlabel("time t")
    ax2.set_ylabel(r"$1/\max|\omega|$")
    ax2.set_title(fr"BKM diagnostic: $1/M\!\to\!0$ linearly ($\alpha$={d['exponent']:.2f})",
                  fontsize=10)
    ax2.legend(loc="upper right")
    fig.suptitle(f"Confirmed blow-up: elite {d['genome_id']} (a=0.7, ν=0, N=1024)",
                 fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGS / "fig4_blowup_curve.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import matplotlib.ticker  # noqa: needed for ScalarFormatter above
    fig_ga_vs_random(); print("fig1_ga_vs_random.png")
    fig_resolution_convergence(); print("fig2_resolution_convergence.png")
    fig_nongenericity(); print("fig3_nongenericity.png")
    fig_blowup_curve(); print("fig4_blowup_curve.png")
