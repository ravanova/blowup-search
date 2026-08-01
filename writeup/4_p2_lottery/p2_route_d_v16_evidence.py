"""Phase-2 P2 Route-D v16 (fig33): the float rehearsal, and the two things it still needs.

v14 removed the far field from the problem and the discrete inverse converged.  This leg
assembles the certificate constants in that space and the answer is a NEGATIVE with a named
repair: Y_0 reaches machine precision, Z_0 is roundoff, and Z_2 does not exist in the
sup-to-sup setting -- because the finite Hilbert transform is unbounded on the sup norm on a
BOUNDED interval too (the obstruction v4 found on the whole line, which the far-field removal
never touched), and separately because sup|N''| is finite only for a <= 1/2.  Z_1 is not
computed at all.  Level-1 tooling + a negative, NOT a certificate.

Rebuilds fig33 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v16_evidence.py
Regenerate the data (deterministic; ~5 min):
    .venv/bin/python -u experiments/p2_route_d_v16_rehearsal.py

Six panels: A Y_0 falling to machine level against its nodal control; B the adversary vs the
naive probe under quadrature refinement; C the sup divergence in log K; D the Holder repair
and its gamma threshold; E the nonlinearity's a <= 1/2 threshold; F the ledger.
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
JSON = DATA / "p2_route_d_v16_rehearsal.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.6))

    # ---- A: Y_0 ------------------------------------------------------------
    A = d["A_Y0"]
    a0 = ax[0, 0]
    for a, col in (("0.3", C["good"]), ("0.4", C["anchor"])):
        r = A[a]
        a0.loglog(r["K"], np.maximum(r["defect"], 1e-16), "o-", color=col,
                  label=f"a={a}: interpolant defect ($K^{{{r['slope_above_floor']:+.1f}}}$)")
        a0.loglog(r["K"], np.maximum(r["nodal"], 1e-16), "s--", color=col, alpha=0.4,
                  label=f"a={a}: nodal residual (Newton, by construction)")
    a0.axhline(1e-11, color=C["grey"], ls=":", lw=1)
    a0.text(17, 1.4e-11, "float floor", fontsize=7, color=C["grey"])
    a0.set_xlabel("K (reduced modes)")
    a0.set_ylabel("$\\sup|F|$")
    a0.set_title("A  $Y_0$ reaches machine precision\n"
                 "sixteen legs carried a defect floor of $10^{-2}$", fontsize=10)
    a0.legend(fontsize=6.6, loc="lower left")
    a0.grid(alpha=0.3, which="both")

    # ---- B: adversary vs naive probe ---------------------------------------
    B = d["B_sup_obstruction"]
    a1 = ax[0, 1]
    n_rule = np.arange(len(B["rules"]))
    for K, mk in (("64", "o"), ("128", "s"), ("256", "^")):
        a1.plot(n_rule, B["adversary"][K], mk + "-", color=C["good"],
                label=f"adversary, K={K}")
        a1.plot(n_rule, B["naive"][K], mk + "--", color=C["bad"], alpha=0.75,
                label=f"naive probe, K={K}")
    a1.set_xticks(n_rule)
    a1.set_xticklabels([f"{lv}/{od}" for lv, od in B["rules"]], fontsize=8)
    a1.set_xlabel("quadrature rule (levels / order)  →  finer")
    a1.set_ylabel("$\\sup|H\\delta e| / \\sup|\\delta e|$")
    a1.set_title("B  which divergence is real?\n"
                 "refine the INSTRUMENT and see which row moves", fontsize=10)
    a1.legend(fontsize=6.4, ncol=2)
    a1.grid(alpha=0.3)
    a1.text(0.03, 0.55, "naive probe collapses to 1.00 → it was\nthe quadrature.\n"
                        "adversary is flat under a 4× refinement\n→ it is the operator.",
            transform=a1.transAxes, fontsize=7,
            bbox=dict(fc="white", ec=C["grey"], alpha=0.95))

    # ---- C: the sup divergence ---------------------------------------------
    a2 = ax[0, 2]
    a2.semilogx(B["K"], B["sup_ratio"], "o-", color=C["bad"], lw=1.8,
                label=f"sup norm: ${B['sup_slope']:+.3f}$ per e-fold")
    fit = np.polyval(np.polyfit(np.log(B["K"]), B["sup_ratio"], 1), np.log(B["K"]))
    a2.semilogx(B["K"], fit, ":", color=C["grey"], label="linear in $\\log K$")
    a2.set_xlabel("K")
    a2.set_ylabel("$\\sup|H\\delta e| / \\sup|\\delta e|$")
    a2.set_title("C  $H$ is unbounded on sup — on a BOUNDED interval\n"
                 "removing the far field killed decay, not smoothness", fontsize=10)
    a2.legend(fontsize=7.5)
    a2.grid(alpha=0.3, which="both")

    # ---- D: the Holder repair ----------------------------------------------
    Cd = d["C_holder_repair"]
    a3 = ax[1, 0]
    gs = sorted(Cd["gamma"], key=float)
    for g in gs:
        r = Cd["gamma"][g]
        a3.semilogx(Cd["K"], r["ratio"], "o-", lw=1.4,
                    label=f"$\\gamma$={g}: {r['slope']:+.4f}")
    a3.set_xlabel("K")
    a3.set_ylabel("$\\sup|H\\delta e| / \\|\\delta e\\|_\\gamma$")
    a3.set_title("D  the repair, measured\n"
                 "the divergence stops at $\\gamma \\gtrsim 0.35$", fontsize=10)
    a3.legend(fontsize=6.8)
    a3.grid(alpha=0.3, which="both")
    a3.text(0.30, 0.80, "v5 U1 found the SAME threshold\non the whole line, where the norm\n"
                        "also carried a decay grading.\nThis one has none — so the\n"
                        "threshold belongs to smoothness.",
            transform=a3.transAxes, fontsize=7,
            bbox=dict(fc="white", ec=C["good"], alpha=0.95))

    # ---- E: the a <= 1/2 threshold -----------------------------------------
    D = d["D_nonlinearity"]
    a4 = ax[1, 1]
    aa = np.asarray(D["a"])
    ratio = np.array([D["rows"][str(x)][-1] / D["rows"][str(x)][0] for x in D["a"]])
    val = np.array([D["rows"][str(x)][0] for x in D["a"]])
    col = [C["good"] if D["finite"][str(x)] else C["bad"] for x in D["a"]]
    a4.semilogy(aa, ratio, "o-", color=C["grey"], lw=1.2, zorder=1,
                label="growth over a $10^{8}$ tightening of the edge cutoff")
    a4.scatter(aa, ratio, c=col, s=55, zorder=3)
    a4.axvline(0.5, color=C["anchor"], ls="--", lw=1.4)
    a4.axhline(1.0, color=C["grey"], ls=":", lw=1)
    a4.text(0.505, 3e3, "$a = 1/2$\n$\\Omega$ loses $C^2$", fontsize=8, color=C["anchor"])
    a4.set_xlabel("a")
    a4.set_ylabel("$\\sup|N''|$ growth factor")
    a4.set_title("E  $\\sup|N''|$ is finite exactly for $a \\leq 1/2$\n"
                 "flat = finite; growing = the cutoff is all that bounds it", fontsize=10)
    a4.legend(fontsize=7, loc="upper left")
    a4.grid(alpha=0.3, which="both")
    a4.text(0.03, 0.55, "\n".join(f"a={x}: {D['rows'][str(x)][0]:.3f}"
                                  for x in (0.2, 0.3, 0.4, 0.5)),
            transform=a4.transAxes, fontsize=7, family="monospace",
            bbox=dict(fc="white", ec=C["good"], alpha=0.95))

    # ---- F: the ledger -----------------------------------------------------
    a5 = ax[1, 2]
    a5.axis("off")
    y03 = d["A_Y0"]["0.3"]
    lines = [
        ("THE REHEARSAL, AND WHY IT DOES NOT CLOSE", "head"),
        ("", "n"),
        (f"$Y_0$   {y03['defect'][0]:.1e} → {min(y03['defect']):.1e}   MACHINE LEVEL", "good"),
        ("$Z_0$   roundoff                       DONE", "good"),
        ("$Z_1$   the infinite-dimensional tail   NOT COMPUTED", "bad"),
        ("$Z_2$   INFINITE in the sup setting     TWO REASONS", "bad"),
        ("", "n"),
        ("  (a) $H$ unbounded on sup, on a bounded interval", "bad"),
        ("      → needs a Hölder domain norm, $\\gamma \\gtrsim 0.35$", "warn"),
        ("  (b) $\\sup|N''|$ finite only for $a \\leq 1/2$", "bad"),
        ("      → norm-dependent; a weight $(1-v)^{(2-1/a)/2}$ fixes it", "warn"),
        ("", "n"),
        ("NOT the far field. (a) is v4's W3 surviving the move to", "eq"),
        ("a bounded interval; the far-field removal killed the DECAY", "eq"),
        ("grading and left the SMOOTHNESS one untouched. So v5/v8's", "eq"),
        ("Hölder machinery is the next brick, not wasted work.", "eq"),
        ("", "n"),
        ("(b) coincides with $a^* \\approx 0.5$–$0.55$. RECORDED, NOT", "warn"),
        ("EXPLAINED — v14 solves the profile cleanly to $a=1.2$.", "warn"),
    ]
    y = 0.97
    for txt, kind in lines:
        if kind == "n":
            y -= 0.026
            continue
        colr = {"head": "black", "eq": C["anchor"], "good": C["good"],
                "warn": C["warn"], "bad": C["bad"]}[kind]
        a5.text(0.0, y, txt, transform=a5.transAxes, fontsize=8.2, color=colr,
                weight="bold" if kind == "head" else None)
        y -= 0.049

    fig.suptitle("Route-D v16 — the float rehearsal: $Y_0$ is finally machine-level, "
                 "and $Z_2$ still needs a smoothness norm", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig33_route_d_v16_rehearsal.png"
    fig.savefig(out, dpi=145)
    print("wrote " + str(out))


if __name__ == "__main__":
    build_figure()
