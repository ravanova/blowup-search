"""Phase-2 P2 Route-D v5 (fig23) evidence: the TWO-GRADING space (decay x
smoothness) -- v4's obstruction defused, and the one marginal direction left.

Route-D v3 (fig21) proved no diagonal-weight pair can carry the certificate; v4
(fig22) showed the decay-graded sup pair fixes the inverse but not the quadratic,
because H is unbounded on L^infinity.  Each leg found half the requirement.  This
leg builds the space that carries both -- a decay weight AND a Holder smoothness
scale -- and asks whether the two halves are compatible.

They are, with one caveat that is itself the same phenomenon v3 already named:

  * the exact construction that broke v4 is DEFUSED for gamma >~ 0.35;
  * the Holder constant of H bowls in gamma, so smoothness has its own interior
    optimum, structurally identical to the one alpha has;
  * the quadratic constant drops below 1 and stops growing;
  * BUT at the codomain's CRITICAL decay rate the inverse creeps logarithmically.
    Keeping the residual class open (decay strictly faster than critical) fixes it
    -- the same detuning v3 used for alpha, one level down.

Level-1 tooling + scoping.  NOT a certificate: the operator norms here are
family-restricted lower bounds, Z1 is still unbounded, and nothing closes.  Clay
odds unchanged (~0.05%).

Rebuilds fig23 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v5_evidence.py
Regenerate the underlying data (deterministic; ~10 min):
    .venv/bin/python experiments/p2_route_d_v5_holder.py

Four panels (fig23):
  A. THE DEFUSAL (U1).  The square-wave adversary in both norms.  The sup ratio
     grows at every gamma -- that is v4's obstruction, and it does not care about
     the decay weight.  The Holder ratio is flat or falling once gamma >~ 0.35.
  B. TWO OPTIMA, ONE PER GRADING (U2/U5).  The Holder constant of H against gamma
     bowls; the inverse norm against alpha bowls (v4).  Each grading has an
     interior optimum for its own reason, and the joint optimum is where they meet.
  C. THE MARGINAL DIRECTION (U3c).  Feeding the inverse residuals that decay like
     X^{-(alpha+1+delta)}: delta = 0 (the critical rate) creeps up with the
     resolved far field; every delta > 0 saturates.  The same marginality v3 found
     at alpha = 2, now at the edge of the codomain class -- and the same fix.
  D. THE QUADRATIC, BEFORE AND AFTER (U4).  v4's constant grew like log m on the
     adversary; here it falls.  Shown against gamma, with the v4 sup-pair value
     for scale.
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
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_route_d_v5_holder.json"
JSON_V4 = DATA / "p2_route_d_v4_graded.json"

C = {"sup": "#1f4e79", "hol": "#c1440e", "crit": "#c00000", "ok": "#2e7d32",
     "warn": "#e08a1e", "v4": "#6a1b9a", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.9))

    # -- Panel A: the defusal ------------------------------------------------
    axA = ax[0, 0]
    u1 = d["u1_defusal"]
    deg = np.array(u1[0]["degrees"], float)
    axA.semilogx(deg, u1[0]["sup_ratio"], "o-", color=C["sup"], lw=2.2, ms=7,
                 label=r"sup norm (v4): $\|Hp_m\|/\|p_m\|$ GROWS")
    cmap = plt.cm.autumn(np.linspace(0.0, 0.75, len(u1)))
    for r, cc in zip(u1, cmap):
        axA.semilogx(deg, r["holder_ratio"], "-", color=cc, lw=1.7,
                     label=r"Holder $\gamma=%.2f$" % r["gamma"])
    axA.axhline(1.0, color=C["grey"], ls=":", lw=1.2)
    axA.set_xlabel("degree m of the square-wave partial sum")
    axA.set_ylabel(r"$\|H p_m\| / \|p_m\|$")
    axA.set_title("A. The construction that broke v4, defused\n"
                  r"sup ratio $\times%.2f$ over $m=8..512$; Holder ratio "
                  r"$\times%.2f$ at $\gamma=0.5$"
                  % (u1[0]["sup_growth"], u1[3]["holder_growth"]), fontsize=9.8)
    axA.legend(fontsize=7.2, loc="upper left", ncol=2)
    axA.grid(alpha=0.3, which="both")

    # -- Panel B: two optima -------------------------------------------------
    axB = ax[0, 1]
    u2 = d["u2_holder_H_constant"]
    g = np.array([r["gamma"] for r in u2])
    ch = np.array([r["C_H"] for r in u2])
    axB.plot(g, ch, "o-", color=C["hol"], lw=2.2, ms=7,
             label=r"$C_H(\gamma)$: Holder constant of $H$")
    kb = int(np.argmin(ch))
    axB.plot([g[kb]], [ch[kb]], "*", color=C["crit"], ms=16, zorder=5)
    axB.annotate(r"$\gamma^\ast\approx%.2f$" % g[kb], xy=(g[kb], ch[kb]),
                 xytext=(g[kb] + 0.05, ch[kb] + 0.08), fontsize=9.5, color=C["crit"])
    axB.set_xlabel(r"smoothness exponent $\gamma$")
    axB.set_ylabel(r"$C_H$")
    axB.grid(alpha=0.3)
    axB.legend(fontsize=8.5, loc="upper center")
    axB2 = axB.inset_axes([0.52, 0.52, 0.45, 0.42])
    try:
        v4 = json.loads(JSON_V4.read_text())["w2_resonance"]["rows"]
        a4 = np.array([r["alpha"] for r in v4])
        A4 = np.array([r["A_norm"] for r in v4])
        keep = a4 <= 1.8
        axB2.plot(a4[keep], A4[keep], "s-", color=C["v4"], lw=1.6, ms=4)
        k4 = int(np.argmin(A4[keep]))
        axB2.plot([a4[keep][k4]], [A4[keep][k4]], "*", color=C["crit"], ms=11)
        axB2.set_title(r"v4: $\|A\|$ vs decay $\alpha$", fontsize=7.5,
                       color=C["v4"])
        axB2.set_xlabel(r"$\alpha$", fontsize=7, labelpad=0)
        axB2.tick_params(labelsize=6.5)
        axB2.grid(alpha=0.3)
        axB2.annotate(r"$\alpha^\ast\approx%.1f$" % a4[keep][k4],
                      xy=(a4[keep][k4], A4[keep][k4]),
                      xytext=(a4[keep][k4] - 0.32, A4[keep][k4] + 1.3),
                      fontsize=7, color=C["crit"])
    except Exception:
        pass
    axB.set_title("B. Each grading has its own interior optimum\n"
                  r"smoothness: $C_H$ bowls in $\gamma$;  decay: $\|A\|$ bowls in "
                  r"$\alpha$ (v4)", fontsize=9.8)

    # -- Panel C: the marginal direction -------------------------------------
    axC = ax[1, 0]
    u3c = d["u3c_critical_direction"]
    Js = np.array(u3c["rows"][0]["J"], float)
    for r in u3c["rows"]:
        lab = (r"$\delta=0$ (CRITICAL)" if r["delta"] == 0.0
               else r"$\delta=%.2f$" % r["delta"])
        style = "o-" if r["delta"] == 0.0 else "s--"
        col_ = C["crit"] if r["delta"] == 0.0 else C["ok"]
        lw = 2.4 if r["delta"] == 0.0 else 1.3
        axC.semilogx(Js, r["ratio"], style, color=col_, lw=lw, ms=6, label=lab,
                     alpha=1.0 if r["delta"] == 0.0 else 0.75)
    axC.set_xlabel("collocation points J   (resolved far field $X\\sim 4J/\\pi$)")
    axC.set_ylabel(r"$\|A g\|_X / \|g\|_Y$")
    crit = [r for r in u3c["rows"] if r["delta"] == 0.0][0]
    axC.set_title("C. One marginal direction survives\n"
                  r"residual $\sim X^{-(\alpha+1+\delta)}$: $\delta=0$ creeps "
                  r"($\sim J^{%.2f}$, a log), every $\delta>0$ saturates"
                  % crit["growth_exponent_in_J"], fontsize=9.8)
    axC.legend(fontsize=8, loc="upper left"); axC.grid(alpha=0.3, which="both")
    axC.text(0.97, 0.05, "the same marginality v3 found at $\\alpha=2$,\n"
                         "now at the edge of the codomain class --\n"
                         "and the same fix: keep the class OPEN",
             transform=axC.transAxes, fontsize=7.6, ha="right", va="bottom",
             color=C["crit"], bbox=dict(boxstyle="round", fc="#f6f0f0", ec="#d0b0b0"))

    # -- Panel D: the quadratic before and after -----------------------------
    axD = ax[1, 1]
    u4 = [r for r in d["u4_quadratic"] if abs(r["alpha"] - 1.5) < 1e-9]
    gg = np.array([r["gamma"] for r in u4])
    grow = np.array([r["C_Q_adversary_growth"] for r in u4])
    cq = np.array([r["C_Q"] for r in u4])
    axD.plot(gg, grow, "o-", color=C["hol"], lw=2.2, ms=7,
             label=r"adversary growth $C_Q(512)/C_Q(8)$")
    axD.axhline(1.0, color=C["crit"], ls="--", lw=1.6)
    axD.text(0.17, 1.04, "above 1 = still growing = not defused", color=C["crit"],
             fontsize=8)
    axD.fill_between(gg, 0, 1.0, where=gg >= 0.35, color=C["ok"], alpha=0.10)
    axD.plot(gg, cq, "s-", color=C["sup"], lw=1.8, ms=6,
             label=r"$C_Q$ (smooth family dominates)")
    try:
        v4q = json.loads(JSON_V4.read_text())["w3_quadratic"]
        r15 = [r for r in v4q if abs(r["alpha"] - 1.5) < 1e-9][0]
        axD.axhline(r15["C_Q_per_degree"][-1], color=C["v4"], ls=":", lw=1.8)
        axD.text(0.6, r15["C_Q_per_degree"][-1] + 0.06,
                 r"v4 sup pair at $m=512$: %.2f (and still climbing)"
                 % r15["C_Q_per_degree"][-1], color=C["v4"], fontsize=8)
    except Exception:
        pass
    axD.set_xlabel(r"smoothness exponent $\gamma$")
    axD.set_ylabel("constant / growth factor")
    axD.set_title("D. The quadratic term, before and after\n"
                  r"$\alpha=1.5$: growth falls below 1 for $\gamma\gtrsim0.35$, "
                  r"and $C_Q$ drops below 1", fontsize=9.8)
    axD.legend(fontsize=8.5, loc="center right"); axD.grid(alpha=0.3)

    fig.suptitle("P2 Route-D v5 -- the two-grading space (decay $\\times$ smoothness):\n"
                 "v4's obstruction is defused and both gradings have interior optima; "
                 "one marginal direction remains  (NOT a certificate)",
                 fontsize=11.5, y=0.997)
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    out = FIGS / "fig23_p2_route_d_v5_holder.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"[fig] wrote {out.relative_to(ROOT)}")


def print_summary():
    d = json.loads(JSON.read_text())
    u1, u2 = d["u1_defusal"], d["u2_holder_H_constant"]
    print("\nP2 Route-D v5 -- the two-grading (decay x smoothness) space "
          "(a=0 anchor, plain float64)")
    ok = [r for r in u1 if r["holder_growth"] <= 1.0]
    print(f"  U1 v4's adversary: sup ratio x{u1[0]['sup_growth']:.2f} at every gamma; "
          f"Holder ratio <= 1 (DEFUSED) for gamma >= {min(r['gamma'] for r in ok):.2f}")
    kb = min(u2, key=lambda r: r["C_H"])
    print(f"  U2 the Holder constant of H bowls: minimum {kb['C_H']:.3f} at gamma = "
          f"{kb['gamma']:.2f} -- smoothness has its own interior optimum, as decay does")
    c = d["u3c_critical_direction"]
    crit = [r for r in c["rows"] if r["delta"] == 0.0][0]
    det = [r for r in c["rows"] if r["delta"] > 0.0]
    print(f"  U3c the critical codomain direction (delta=0) creeps: "
          f"{crit['ratio'][0]:.2f} -> {crit['ratio'][-1]:.2f} over J="
          f"{crit['J'][0]}..{crit['J'][-1]} (~J^{crit['growth_exponent_in_J']:+.2f}); "
          f"every delta > 0 saturates (e.g. delta={det[-1]['delta']}: "
          f"{det[-1]['ratio'][0]:.2f} -> {det[-1]['ratio'][-1]:.2f})")
    b = d["u5_budget"]["best_defused"]
    print(f"  U5 best in the DEFUSED region: alpha={b['alpha']:.2f}, "
          f"gamma={b['gamma']:.2f}, ||A||={b['A_norm']:.2f}, C_Q={b['C_Q']:.3f}, "
          f"Z2={b['Z2']:.2f}, budget ceiling {b['budget_ceiling']:.2e}")
    print("  CAVEATS: operator norms are FAMILY-RESTRICTED lower bounds (the exact "
          "induced norm between polyhedral norms is an LP); Z1 is still not bounded; "
          "nothing closes. Level-1 tooling + scoping. Clay odds ~0.05%.")


if __name__ == "__main__":
    build_figure()
    print_summary()
