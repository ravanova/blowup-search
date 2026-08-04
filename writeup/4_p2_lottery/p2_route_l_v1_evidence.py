"""Phase-2 P2 Route-L v1 (fig41): the 2D preconditioner — the stall attributed, and removed.

Route-K left the certification port blocked at step (iii) with the obstruction half
identified and two candidates named. This leg eliminates both of them by measurement, finds
the real one, and builds the operator that removes it.

Rebuild fig41 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_l_v1_evidence.py
Regenerate the data (deterministic; ~25 min):
    .venv/bin/python -u experiments/p2_route_l_v1_precond.py

Six panels: A the attribution battery, six ablations ranked by how much each un-flattens the
Krylov ladder; B Route-K's two candidates, both eliminated — freezing the velocity makes it
worse, and the stalled residual is not concentrated at the wall; C THE PRECONDITIONER, the
ladder going from flat to bending; D the ADI composition that does not work, kept because
the negative is load-bearing; E Newton with the working linear solve; F what the chain looks
like now.
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
JSON = DATA / "p2_route_l_v1_precond.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ns": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    lad = d["L1_attribution"]["ladders"]
    ranked = d["L1_attribution"]["ranked"]
    pre = d["L3_preconditioners"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the attribution battery --------------------------------------
    a0 = ax[0, 0]
    for label, rows in lad.items():
        col = {"full": C["bad"], "angular transport OFF": C["good"],
               "pure dilation, no angular": C["ns"]}.get(label, C["grey"])
        lw = 2.2 if label in ("full", "angular transport OFF",
                              "pure dilation, no angular") else 1.2
        a0.plot([q["m"] for q in rows], [q["rel_residual"] for q in rows], "o-",
                color=col, lw=lw, ms=5, label=label, alpha=0.95 if lw > 2 else 0.7)
    a0.set_xscale("log")
    a0.set_xlabel("Krylov dimension $m$")
    a0.set_ylabel("relative residual of $DF\\,x = -F$")
    a0.legend(fontsize=6.2, loc="lower left")
    a0.set_title("A  the attribution battery: which term makes the ladder FLAT?\n"
                 f"ranked by gain: {ranked[0]['ablation']} ({ranked[0]['gain']:.2f}), "
                 f"{ranked[1]['ablation']} ({ranked[1]['gain']:.2f}), "
                 f"full ({ranked[-1]['gain']:.2f})",
                 fontsize=9)

    # ---- B: Route-K's two candidates, both eliminated --------------------
    a1 = ax[0, 1]
    full_end = lad["full"][-1]["rel_residual"]
    vel_end = lad["velocity feedback OFF"][-1]["rel_residual"]
    a1.bar([0, 1], [full_end, vel_end], color=[C["grey"], C["bad"]], width=0.55)
    a1.set_xticks([0, 1])
    a1.set_xticklabels(["full", "velocity\nfeedback OFF"], fontsize=8)
    a1.set_ylabel("stalled residual at $m=160$")
    a1.set_ylim(0, max(full_end, vel_end) * 1.35)
    a1.text(1, vel_end * 1.04, "WORSE — not the culprit", ha="center",
            fontsize=8, color=C["bad"], weight="bold")
    b = d["L2_stalled_residual_bands"]
    share = b["proportional_share_3_of_48"]
    a2b = a1.twinx()
    xs = [2.2, 2.8, 3.4]
    a2b.bar(xs, [b[f]["wall_first3_frac"] for f in ("omega", "eta", "xi")],
            color=C["anchor"], width=0.45, alpha=0.85)
    a2b.axhline(share, color=C["good"], ls="--", lw=1.4)
    a2b.text(3.6, share * 1.08, "proportional share\n(3 of 48 nodes)", fontsize=6.5,
             color=C["good"], va="bottom")
    a1.axvspan(1.85, 4.6, color=C["anchor"], alpha=0.06)
    a2b.set_ylabel("wall share of the stalled residual (RIGHT axis)", color=C["anchor"])
    a2b.tick_params(axis="y", labelcolor=C["anchor"])
    a1.set_xlim(-0.6, 4.6)
    for x, f in zip(xs, ("$\\omega$", "$\\eta$", "$\\xi$")):
        a1.text(x, 0.02 * a1.get_ylim()[1], f, ha="center", fontsize=8)
    a1.set_title("B  both of Route-K's candidates, eliminated\n"
                 "the nonlocal velocity HELPS; the wall carries only its "
                 "proportional share for $\\omega,\\eta$", fontsize=9)

    # ---- C: the preconditioner -------------------------------------------
    a2 = ax[0, 2]
    order = [("none", C["bad"], "-"), ("radial only (Route-K)", C["warn"], "-"),
             ("full transport line sweep", C["good"], "-")]
    for label, col, ls in order:
        rows = pre["ladders"][label]
        a2.semilogy([q["m"] for q in rows], [max(q["rel_residual"], 1e-12) for q in rows],
                    "o" + ls, color=col, lw=2.0, ms=6, label=label)
    dp = pre["line_sweep_deeper"]
    a2.semilogy([q["m"] for q in dp], [max(q["rel_residual"], 1e-12) for q in dp],
                "o--", color=C["good"], lw=2.0, ms=6)
    a2.set_xscale("log")
    a2.set_xlabel("Krylov dimension $m$")
    a2.set_ylabel("relative residual")
    a2.legend(fontsize=6.8, loc="lower left")
    a2.set_title("C  THE PRECONDITIONER: the ladder stops being flat\n"
                 f"{pre['ladders']['none'][-1]['rel_residual']:.4f} (flat) → "
                 f"{pre['ladders']['full transport line sweep'][-1]['rel_residual']:.4f} at "
                 f"$m$=160 → {dp[-1]['rel_residual']:.1e} at $m$={dp[-1]['m']}", fontsize=9)

    # ---- D: the ADI negative ---------------------------------------------
    a3 = ax[1, 0]
    for label, col in (("none", C["grey"]), ("ADI composition", C["bad"]),
                       ("full transport line sweep", C["good"])):
        rows = pre["ladders"][label]
        a3.plot([q["m"] for q in rows], [q["rel_residual"] for q in rows], "o-",
                color=col, lw=2.0, ms=6, label=label)
    a3.set_xscale("log")
    a3.set_ylim(0, 1.05)
    a3.set_xlabel("Krylov dimension $m$")
    a3.set_ylabel("relative residual")
    a3.legend(fontsize=7, loc="center left")
    a3.set_title("D  the operator does NOT split — the negative is load-bearing\n"
                 "composing two exact 1D solves is WORSE than doing nothing "
                 f"({pre['ladders']['ADI composition'][-1]['rel_residual']:.3f})", fontsize=9)

    # ---- E: Newton -------------------------------------------------------
    a4 = ax[1, 1]
    n4 = d["L4_newton"]["iterations"]
    a4.semilogy([q["iter"] for q in n4], [q["F_l2"] for q in n4], "o-",
                color=C["warn"], lw=1.8, ms=6, label="Newton (no gauge)")
    if "L5_gauge_projected_newton" in d:
        n5 = d["L5_gauge_projected_newton"]["iterations"]
        a4.semilogy([q["iter"] for q in n5], [q["F_l2"] for q in n5], "s-",
                    color=C["good"], lw=1.8, ms=6, label="Newton + gauge projection")
    a4.set_xlabel("Newton iteration")
    a4.set_ylabel("$\\|F\\|_2$")
    a4.legend(fontsize=7)
    lam = [q.get("step_lambda") for q in n4 if q.get("step_lambda")]
    a4.set_title("E  the LINEAR solve now works — the Newton iteration still does not\n"
                 f"GMRES relative residual {n4[0].get('gmres_rel', float('nan')):.1e} "
                 f"(was 1.00); line search caps at $\\lambda$="
                 f"{min(lam) if lam else float('nan'):.4g}", fontsize=9)

    # ---- F: the chain now ------------------------------------------------
    a5 = ax[1, 2]
    a5.axis("off")
    conv = d.get("L5_gauge_projected_newton", {}).get("converged", False)
    steps = [("(i)   a fixed profile $x^*$", "STILL BLOCKED", C["bad"]),
             ("(ii)  $Y_0$, the defect", "STILL UNDEFINED", C["bad"]),
             ("(iii) $A \\approx DF^{-1}$, $Z_1 < 1$", "UNBLOCKED", C["good"]),
             ("(iv)  the radii polynomial", "NOT REACHED", C["grey"])]
    a5.text(0.0, 0.96, "the certification chain, after this leg:", fontsize=9.5,
            weight="bold", transform=a5.transAxes)
    for i, (txt, tag, col) in enumerate(steps):
        y = 0.82 - 0.11 * i
        a5.text(0.0, y, txt, fontsize=9.5, transform=a5.transAxes)
        a5.text(0.66, y, tag, fontsize=9.5, weight="bold", color=col,
                transform=a5.transAxes)
    a5.text(0.0, 0.34,
            "Step (iii) was the one Route-K called impossible on this grid.\n"
            "It is now an $O(N)$ sweep, and the obstruction it removes is\n"
            "entirely the TRANSPORT operator — radial and angular — with\n"
            "nothing else in the equation contributing.\n\n"
            "What blocks (i) is now a DIFFERENT kind of problem: the linear\n"
            "solves succeed and Newton still creeps, with the line search\n"
            "capped. That is a near-null direction, not a spectrum — the\n"
            "scaling gauge that the relaxation pins and $F$ does not carry.\n"
            + ("\nThe obvious candidate was the scaling gauge that the relaxation\n"
               "pins and $F$ does not carry. It was tested and REFUTED: projecting\n"
               "onto the gauge makes it worse, and the line search accepts no step\n"
               "at all. The near-null direction is something else."
               if not conv else
               "\nThe scaling gauge was the cause: projecting onto it CONVERGES."),
            fontsize=8.4, transform=a5.transAxes, va="top")
    a5.set_title("F  one link unblocked, and the next obstruction is a different kind",
                 fontsize=9)

    fig.suptitle("Route-L v1 — the 2D preconditioner: both named suspects cleared, the real "
                 "one found, and the stall removed", fontsize=12, y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig41_route_l_v1_precond.png"
    fig.savefig(out, dpi=150)
    print(f"-> {out}")


if __name__ == "__main__":
    build_figure()
