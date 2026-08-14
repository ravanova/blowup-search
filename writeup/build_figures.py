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


def fig_rough_rails():
    """Stage 3.6: genuine rough (C^{0,h}) data still rails the blow-up exponent
    near a=1, while the a=0.7 control stays flat at the generic alpha=1 — the
    reason the fine-N negative is trustworthy."""
    import matplotlib.ticker
    d = load("stage3_6_rough.json")
    ns = d["resolutions"]
    cells = d["cells"]
    col = {0.7: "#059669", 0.9: "#d97706", 0.95: "#dc2626"}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3),
                                   gridspec_kw={"width_ratios": [1.15, 1]})

    # left: fitted blow-up exponent alpha vs resolution N, one line per (h,a)
    seen = set()
    for a in (0.7, 0.9, 0.95):
        for h in d["h_values"]:
            pts = [(c["N"], c["alpha"]) for c in cells
                   if c["a"] == a and c["h"] == h and c["usable"]]
            pts.sort()
            if len(pts) >= 2:
                lbl = {0.7: "a=0.7 (control)", 0.9: "a=0.9",
                       0.95: "a=0.95"}[a] if a not in seen else None
                seen.add(a)
                ax1.plot([p[0] for p in pts], [p[1] for p in pts], "o-",
                         color=col[a], lw=1.3, ms=4, alpha=0.7, label=lbl)
    for edge in (0.30, 3.00):
        ax1.axhline(edge, color="#bbb", lw=0.9, ls=":", zorder=0)
    ax1.axhline(1.0, color="#888", lw=1.0, ls="--", zorder=0)
    ax1.text(ns[0], 1.04, "generic α=1", fontsize=8, color="#666")
    ax1.text(ns[-1], 3.03, "fit-grid edge (rail)", fontsize=8, color="#999",
             ha="right", va="bottom")
    ax1.set_xscale("log", base=2)
    ax1.set_xticks(ns)
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.set_xlabel("spectral resolution N")
    ax1.set_ylabel(r"fitted blow-up exponent $\alpha$")
    ax1.set_title("Rough data: α vs resolution", fontsize=10)
    ax1.legend(loc="upper left", fontsize=8.5)
    ax1.annotate("control stays flat\nat α≈1 (generic)", (ns[-1], 1.0),
                 xytext=(ns[0] * 1.15, 1.9), fontsize=8.5, color=col[0.7],
                 arrowprops=dict(arrowstyle="->", color=col[0.7], lw=1))

    # right: cross-resolution exponent span per a (instability) + dead a=1.0
    a_list = [0.7, 0.9, 0.95, 1.0]
    med = [d["per_a"][str(a)]["median_cross_N_span"] or 0 for a in a_list]
    mx = [d["per_a"][str(a)]["max_cross_N_span"] or 0 for a in a_list]
    x = range(len(a_list))
    ax2.bar([i - 0.19 for i in x], med, 0.38, color="#94a3b8",
            label="median cross-N |Δα|")
    ax2.bar([i + 0.19 for i in x], mx, 0.38, color=col[0.95],
            label="max cross-N |Δα|")
    ax2.axhline(0.05, color="#888", lw=0.9, ls=":")
    ax2.text(2.6, 0.09, "grid step 0.05", fontsize=8, color="#666")
    ax2.text(3, 0.15, "a=1.0:\ndead axis\n(0/18)", ha="center", fontsize=8.5,
             color="#444")
    ax2.set_xticks(list(x))
    ax2.set_xticklabels([f"a={a:g}" for a in a_list])
    ax2.set_ylabel(r"cross-resolution exponent span $|\Delta\alpha|$")
    ax2.set_title("Exponent instability near a=1", fontsize=10)
    ax2.legend(fontsize=8.5, loc="upper left")

    fig.suptitle("Stage 3.6: genuine C^{0,h} rough data still rails the exponent "
                 "near a=1 (control validates the measurement)",
                 fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGS / "fig5_rough_rails.png", bbox_inches="tight")
    plt.close(fig)


def fig_phase1_spike():
    """Route A Phase 1 resolution wall: the fixed-window growth rate g CONVERGES
    across N (a resolution-stable search signal exists) while the fitted blow-up
    exponent RAILS (the true singularity is out of uniform-grid reach)."""
    d = load("phase1_spike.json")
    growers = ["smooth_sharp", "smooth_mild"]
    col = {"smooth_sharp": "#2563eb", "smooth_mild": "#059669"}
    fig, (axg, axe) = plt.subplots(1, 2, figsize=(11, 3.8))
    for ic in growers:
        g = d["ics"][ic]["g_by_N"]
        Ns = sorted((int(n) for n in g), key=int)
        axg.plot(Ns, [g[str(n)] for n in Ns], "o-", color=col[ic], lw=2, label=ic)
        e = d["ics"][ic]["exponent_by_N"]
        ev = [(n, e[str(n)]) for n in Ns if e[str(n)] is not None]
        axe.plot([n for n, _ in ev], [v for _, v in ev], "o-", color=col[ic],
                 lw=2, label=ic)
    axg.set_xscale("log", base=2); axe.set_xscale("log", base=2)
    axg.set_xticks(Ns); axg.set_xticklabels(Ns)
    axe.set_xticks(Ns); axe.set_xticklabels(Ns)
    axg.set_xlabel("grid resolution N"); axe.set_xlabel("grid resolution N")
    axg.set_ylabel("fixed-window growth rate  g"); axg.set_ylim(0, 1.6)
    axg.set_title("g CONVERGES  →  resolution-stable search signal", fontsize=10)
    axe.set_ylabel(r"fitted blow-up exponent  $\alpha$")
    axe.set_title(r"$\alpha$ RAILS  →  true singularity out of uniform-grid reach",
                  fontsize=10)
    axg.legend(loc="center right", fontsize=9); axe.legend(loc="best", fontsize=9)
    fig.suptitle("Phase 1 resolution de-risk spike (2D Boussinesq, Hou–Luo): "
                 "search-viable, Tier-2-of-the-true-singularity out of reach",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGS / "fig6_phase1_spike.png", bbox_inches="tight")
    plt.close(fig)


def fig_phase1_axis_screen():
    """Route A Phase 1 fitness-axis screen: on the labeled ground-truth pair
    (sharp blows up, mild saturates, control flat), only nu_crit orders
    sharp>mild>control (propensity) AND is resolution-stable. Raw g gets it
    backwards; persistence puts the saturating grower below the non-grower."""
    d = load("phase1_axis_screen.json")
    ics = d["ics"]; Nhi = str(max(d["resolutions"]))
    labels = {"smooth_sharp": "sharp\n(blows up)", "smooth_mild": "mild\n(saturates)",
              "euler_control": "control\n(flat)"}
    axmeta = [("nu_crit", r"$\nu_{crit}$  (amp$\geq2\times$)", "#2563eb", "PASS"),
              ("persistence", "persistence", "#d97706", "FAIL"),
              ("g_baseline", "raw growth rate  g", "#dc2626", "FAIL")]
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.8))
    x = range(len(ics))
    for ax, (axis, title, c, tag) in zip(axes, axmeta):
        vals = [d["values"][axis][ic][Nhi] or 0.0 for ic in ics]
        bars = ax.bar(x, vals, color=c, alpha=0.85)
        ok = d["verdict"][axis]["direction_ok"]
        ax.set_xticks(list(x)); ax.set_xticklabels([labels[ic] for ic in ics], fontsize=8.5)
        ax.axhline(0, color="#333", lw=0.8)
        ax.set_title(f"{title}\n[{tag}: direction {'OK' if ok else 'WRONG'}]",
                     fontsize=9.5)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.2f}",
                    ha="center", va="bottom" if v >= 0 else "top", fontsize=8)
    axes[0].set_ylabel(f"axis value at N={Nhi}")
    fig.suptitle("Phase 1 fitness-axis screen: only ν_crit tracks blow-up "
                 "PROPENSITY (sharp>mild>control) — and it is N-identical to 4 dp",
                 fontweight="bold", y=1.03)
    fig.tight_layout()
    fig.savefig(FIGS / "fig7_phase1_axis_screen.png", bbox_inches="tight")
    plt.close(fig)


def fig_route_ivax_v1():
    """fig70 -- Route-IVAX v1 (leg 311): does screen (iv_a) bite off the fluid axis?
    Plots directly from the banked census in p2_route_ivax_v1.json -- no re-measurement.
    Left: kill-rate comparison, the fluid pool (leg 261, 18/18) vs the non-fluid pool this
    leg measured (3/3). Right: per-model count of operator classes Remark 40 leaves
    unnamed, the mechanism (nonlocality) the gate actually tracks."""
    d = load("p2_route_ivax_v1.json")
    census = d["census"]
    rows = census["rows"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    # left: fluid pool (leg 261) vs non-fluid pool (this leg), killed vs total
    pools = ["fluid pool\n(leg 261)", "non-fluid pool\n(leg 311)"]
    killed = [18, census["n_killed_by_iv_a"]]
    total = [18, census["n_total"]]
    x = range(len(pools))
    ax1.bar(x, total, 0.5, color="#e5e7eb", label="total models")
    ax1.bar(x, killed, 0.5, color="#dc2626", label="killed by (iv_a)")
    for i, (k, n) in enumerate(zip(killed, total)):
        ax1.text(i, n + 0.4, f"{k}/{n}", ha="center", fontsize=10, fontweight="bold")
    ax1.set_xticks(list(x)); ax1.set_xticklabels(pools)
    ax1.set_ylabel("models")
    ax1.set_ylim(0, 21)
    ax1.set_title("(iv_a) kill rate: same clause, both pools", fontsize=10)
    ax1.legend(fontsize=8.5, loc="upper right")

    # right: per-model count of operator classes unnamed by Remark 40
    keys = [r["key"] for r in rows]
    n_unnamed = [r["n_unnamed_by_remark_40"] for r in rows]
    fluid_adj = [r["fluid_adjacent"] for r in rows]
    colors = ["#d97706" if fa else "#2563eb" for fa in fluid_adj]
    y = range(len(keys))
    ax2.barh(y, n_unnamed, color=colors)
    ax2.set_yticks(list(y)); ax2.set_yticklabels(keys, fontsize=8.5)
    ax2.set_xlabel("operator classes unnamed by Remark 40")
    ax2.set_xlim(0, max(n_unnamed) + 1)
    ax2.set_title("Mechanism: nonlocality, not incompressibility", fontsize=10)
    ax2.invert_yaxis()
    from matplotlib.patches import Patch
    ax2.legend(handles=[Patch(color="#2563eb", label="non-fluid"),
                        Patch(color="#d97706", label="fluid-adjacent")],
               fontsize=8.5, loc="lower right")

    fig.suptitle("Route-IVAX v1 (leg 311): screen (iv_a) bites off the fluid axis too "
                 f"-- verdict: {d['verdict_code']}", fontweight="bold", y=1.04, fontsize=10.5)
    fig.tight_layout()
    fig.savefig(FIGS / "fig70_route_ivax_v1.png", bbox_inches="tight")
    plt.close(fig)


# Phase-2 per-leg figures live in their own *_evidence.py next to their writeups, so that
# each one rebuilds from its own curated JSON with no re-run. Registered here so that
# `build_figures.py` rebuilds the whole figure set rather than only the Phase-1 half.
P2_EVIDENCE = [
    "4_p2_lottery/p2_route_tc_v1_evidence.py",      # fig48 -- Route-TC v1 (leg 53)
    # Legs 54-57 keep their evidence scripts in experiments/ (their declared territory in
    # DIRECTION.md) rather than beside their writeups like leg 53's -- these paths are
    # relative to writeup/, so they step up one level.
    "../experiments/p2_route_mm_v1_shape_evidence.py",          # fig49 -- Route-MM v1 (leg 54)
    "../experiments/p2_route_nb_v1_targetnorm_evidence.py",     # fig50 -- Route-NB v1 (leg 55)
    "../experiments/p2_route_tn_v1_consistency_evidence.py",    # fig51 -- Route-TN v1 (leg 56)
    "../experiments/p2_route_xs_v1_shapes_evidence.py",         # fig52 -- Route-XS v1 (leg 57)
    "../experiments/p2_weight_repairs_v2_evidence.py",          # fig58 -- Route-WV v2 (leg 59)
    "../experiments/p2_route_port_v1_bordered_evidence.py",     # fig59 -- Route-PORT v1 (leg 46)
    "../experiments/p2_route_port_v2_reach_evidence.py",        # fig60 -- Route-PORT v2 (leg 47)
    "../experiments/p2_route_cp_v1_cadiot_evidence.py",         # fig56 -- Route-CP v1 (leg 62)
    "../experiments/p2_route_ng_v1_nogo_evidence.py",           # fig55 -- Route-NG v1 (leg 58)
    "../experiments/p2_route_wvr_v1_fitness_evidence.py",       # fig64 -- Route-WVR v1 (leg 160)
    "../experiments/p2_route_m2ci_v1_construction_evidence.py", # fig65 -- Route-M2CI v1 (leg 187)
    "../experiments/p2_route_wes_v1_space_evidence.py",         # fig66 -- Route-WES v1 (leg 178)
    "../experiments/p2_route_p0tcv_v1_verify_evidence.py",      # fig68 -- Route-P0TCV v1 (leg 300), renumbered from fig67
    "../experiments/p2_route_cadx_v1_scope.py",                 # fig67 -- Route-CADX v1 (leg 304)
    "../experiments/p2_route_gaf_v1_sweep_evidence.py",         # fig71 -- Route-GAF v1 (leg 303), renumbered from fig68
    "../experiments/p2_route_dfre_v1_evidence.py",              # fig74 -- Route-DFRE v1 (leg 316), renumbered from fig71
    "../experiments/p2_route_tms_v1_scoping.py",                # fig79 -- Route-TMS v1 (leg 315)
    # fig69 (Route-P2T1 v1, leg 302) used to be deliberately absent from this list: its own
    # runner only emits the figure under --figure and exits nonzero because its gate answers
    # NO, which would fail an unconditional rebuild. Leg 327 wrote a standalone
    # p2_route_p2t1_v1_evidence.py that redraws fig69 from the curated JSON alone (no
    # re-run); it is registered below. Items 9, 10 and 13 of writeup/INDEX.md used to be the
    # same class of debt, reserved for a batched follow-up leg -- leg 372 closed that batch:
    # item 9 (Weight-repairs v1) turned out already closed by leg 138 (evidence.py landed in
    # 9d9b7ea, predating leg 108's own pass; not re-touched here, a duplicate would have been
    # a fail per leg 372's own gate). Item 10 (Route-KA v1) and the NKR half of item 13 are
    # known-answer/repair audits whose own TECHNICAL headers declare "no figure, established
    # convention" (the same class as Route-D's advection/literature-scope legs) -- their
    # p2_route_ka_v1_kawahara_evidence.py and p2_route_nkr_v1_repair_evidence.py exist,
    # verify their banked numbers from JSON alone, and are intentionally NOT registered here
    # because this list is specifically for rebuilding figures. Only the M2P half of item 13
    # produces a figure and is registered below.
    "../experiments/p2_route_p2t1_v1_evidence.py",              # fig69 -- Route-P2T1 v1 (leg 302), evidence script by leg 327
    "../experiments/p2_route_capa_v2_audit_evidence.py",        # fig80 -- Route-CAPA v2 (leg 292)
    "../experiments/p2_route_fus_v1_scoping_evidence.py",       # fig77 -- Route-FUS v1 (leg 314); brief recorded fig69-fig76 as taken/reserved, so this leg took fig77
    "../experiments/p2_route_apia_v1_evidence.py",              # fig73 -- Route-APIA v1 (leg 312)
    "../experiments/p2_route_dwm_v1_evidence.py",               # fig82 -- Route-DWM v1 (leg 305)
    "../experiments/p2_route_m2p_v1_promotion_evidence.py",     # fig61 -- Route-M2P v1 (leg 125), evidence script by leg 372, item 13
    "../experiments/p2_route_sdss_v1_evidence.py",              # fig76 -- Route-SDSS v1 (leg 313), landed late under the cycle-11a caveat
    "../experiments/p2_route_dexc_v1_evidence.py",              # fig100 -- Route-DEXC v1 (leg 382); fig100 assigned at dispatch, fig96 being the highest then in use
    "../experiments/p2_route_st2g_v1_evidence.py",              # fig102 -- Route-ST2G v1 (leg 383); fig102 assigned at dispatch (fig100 and fig101 already allocated this cycle to legs 382 and 233)
    "../experiments/p2_route_cloc_v1_evidence.py",              # fig104 -- Route-CLOC v1 (leg 381), evidence script by the DOCS-lane closure of leg 381's missing-figure audit finding; fig104 (NOT fig99, which leg 381's omission freed and which is now leg 386's)
    ("../experiments/p2_route_scel_v1.py", ["--figure"]),       # fig103 -- Route-SCEL v1 (leg 385); fig103 assigned at dispatch. The runner IS the evidence script under --figure: it redraws fig103 from writeup/data/p2_route_scel_v1.json alone and re-runs no interval arithmetic (leg 385's territory listed one experiments/ file, so the rebuild path lives in it rather than in a separate *_evidence.py)
    "../experiments/p2_route_bvrrv_v1_postrepair_evidence.py",  # fig101 -- Route-BVRRV v1 (leg 233); fig101 allocated at dispatch, quartet closed later by a DOCS rework unit
    "../experiments/p2_route_cobv_v1_evidence.py",              # fig105 -- Route-COBV v1 (leg 384); fig105 assigned at dispatch (fig103 to leg 385, fig104 to a DOCS unit)
    "../experiments/p2_route_dtol_v1_evidence.py",              # fig99 -- Route-DTOL v1 (leg 386); fig99 was reserved for leg 381, which drew no figure and left it unused, and was re-allocated to this leg at dispatch
    "../experiments/p2_route_dtor_v1_evidence.py",              # fig106 -- Route-DTOR v1 (leg 390); fig106 assigned at dispatch (fig105 to leg 384, fig103 to leg 385, fig99 to leg 386, fig97/98 to PROG-R4, fig101/104 to the DOCS units)
    "figures/fig108_prog_r4_r0r1.py",                           # fig108 -- PROG-R4 R0+R1, Lane R metric reconciliation and flatness abort; fig108 assigned at dispatch (fig107 to U5, fig109 to another worker in the same wave). The drawing script IS the rebuild path: it redraws from writeup/data/p2_prog_r4_r0r1_v1.json alone and re-runs no solver
    "figures/fig109_prog_r4_hhard.py",                          # fig109 -- PROG-R4 unit E, the H-hard diagnostic (leg 380, wave 1); fig109 assigned at dispatch (fig107 is U5's, fig108 another worker's in the same wave). The drawing script IS the rebuild path: it redraws from writeup/data/p2_prog_r4_e_v1.json and the two banked PROG-R4 records alone and re-runs no solve. Its 17 self-checks exit non-zero if the JSON stops supporting a panel
    "../experiments/p2_route_t4_v1_evidence.py",                # fig110 -- Route-T4 v1 (leg 393); fig110 assigned at dispatch. Redraws from writeup/data/p2_route_t4_v1.json alone: no network, no PDF, no .mat at rebuild time
]


def build_p2_evidence_figures():
    import subprocess
    import sys
    here = Path(__file__).resolve().parent
    for entry in P2_EVIDENCE:
        # An entry is either a path, or a (path, extra_args) pair for the few runners that
        # emit their figure only when asked -- leg 302's --figure is the first such case.
        rel, extra = (entry, []) if isinstance(entry, str) else entry
        extra = [a.format(figures=here / "figures") for a in extra]
        script = here / rel
        if not script.exists():
            print(f"  SKIP {rel} (not present)")
            continue
        subprocess.run([sys.executable, str(script), *extra], check=True)


if __name__ == "__main__":
    import matplotlib.ticker  # noqa: needed for ScalarFormatter above
    fig_ga_vs_random(); print("fig1_ga_vs_random.png")
    fig_resolution_convergence(); print("fig2_resolution_convergence.png")
    fig_nongenericity(); print("fig3_nongenericity.png")
    fig_blowup_curve(); print("fig4_blowup_curve.png")
    fig_rough_rails(); print("fig5_rough_rails.png")
    fig_phase1_spike(); print("fig6_phase1_spike.png")
    fig_phase1_axis_screen(); print("fig7_phase1_axis_screen.png")
    fig_route_ivax_v1(); print("fig70_route_ivax_v1.png")
    build_p2_evidence_figures()
