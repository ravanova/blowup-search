"""Phase-2 P2 (fig18) evidence: is the gCLM two-scale survival boundary GENUINE or
just genome-limited? An a_p(K) convergence map that sharpens the banked a-sweep's
T4 fail (where a fixed even K=2 genome gave a_p~0.40 that a richer genome beat).

Result (LOGGED run experiments/p2_two_scale_kladder.py --logged; predicate T1-T7
locked in git first). Rebuilds fig18 from committed data WITHOUT re-running the GA:
    .venv/bin/python writeup/p2_two_scale_kladder_evidence.py
Regenerate the underlying data:
    .venv/bin/python experiments/p2_two_scale_kladder.py --logged

Four panels (fig18):
  A. THE a_p(K) MAP: scale-invariant residual floor vs a for the even genome at
     K=2,3,4 (converged budget), 1e-2 persistence threshold, a_p(K) window, and the
     boundary a* where the CONVERGED floor crosses 1e-2. K=2's a_p is understated.
  B. CONVERGENCE AT THE BOUNDARY (the "genuine, not artifact" panel): at the
     boundary a's, floor vs GA budget (plateau) and K=4 vs K=6 (genome plateau) --
     the floor stops dropping, so the 1e-2 crossing is a real property.
  C. a_p(K) SATURATION: a_p vs K -- rises from K=2 (understated) then flattens at
     the genuine boundary; contrast with a hypothetical "keeps marching out".
  D. RESOLUTION + BASIS INDEPENDENCE: selected half-max width W(a;K) (all >> 8-pt
     guard) and the different-basis (Lorentzian+squared) crosscheck vs even K=3.
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
JSON = DATA / "p2_two_scale_kladder.json"


def build_figure():
    d = json.loads(JSON.read_text())
    recs = d["records"]
    cfg = d["config"]
    checks = d["predicate_checks"]
    summ = d["summary"]
    a = np.array([r["a"] for r in recs])
    fl = {K: np.array([r["floor"].get(str(K), np.nan) for r in recs]) for K in (2, 3, 4)}
    a_star = summ["a_star_boundary"]
    a_p = {K: summ[f"a_p_K{K}"] for K in (2, 3, 4)}

    fig, ax = plt.subplots(2, 2, figsize=(12.8, 9.4))
    cols = {2: "#c1440e", 3: "#e08a1e", 4: "#1f4e79"}

    # -- Panel A: the a_p(K) map ---------------------------------------------
    axA = ax[0, 0]
    for K in (2, 3, 4):
        axA.semilogy(a, fl[K], "o-", color=cols[K], lw=1.8, ms=5, label=f"even K={K}")
    # K=6 genome spot-check points (where present)
    a6 = np.array([r["a"] for r in recs if "6" in r["floor"]])
    f6 = np.array([r["floor"]["6"] for r in recs if "6" in r["floor"]])
    if a6.size:
        axA.semilogy(a6, f6, "*", color="#2e8b57", ms=13, mfc="none", mew=1.8,
                     label="even K=6 (genome check)")
    axA.axhline(1e-2, color="gray", ls=":", lw=1.2)
    axA.text(0.02, 1.15e-2, "persistence threshold $10^{-2}$", fontsize=8, color="gray")
    axA.axvline(a_star, color="#1f4e79", ls="--", lw=1.4)
    axA.text(a_star + 0.01, 3e-6, f"boundary\n$a^*\\approx{a_star:.2f}$", fontsize=9,
             color="#1f4e79")
    axA.set_title("A. a_p(K) MAP: two-scale residual floor "
                  r"$\|R_2\|/\|\Omega H\Omega\|$ vs advection $a$", fontsize=10.5)
    axA.set_xlabel("advection parameter  a   (0 = CLM,  1 = De Gregorio)")
    axA.set_ylabel("residual floor (log)")
    axA.legend(fontsize=8.5, loc="lower right"); axA.grid(alpha=0.25, which="both")

    # -- Panel B: convergence at the boundary --------------------------------
    axB = ax[0, 1]
    bk = [r for r in recs if "floor_K4_bigbudget" in r]
    labels, base, big = [], [], []
    for r in bk:
        labels.append(f"a={r['a']:.2f}")
        base.append(r["floor"]["4"]); big.append(r["floor_K4_bigbudget"])
    x = np.arange(len(labels)); w = 0.35
    axB.bar(x - w/2, base, w, color="#1f4e79", label=f"K=4, budget {cfg['pop']}x{cfg['gen']}")
    axB.bar(x + w/2, big, w, color="#8fb3d9", label="K=4, ~1.7x budget")
    # overlay K=6 at the same a's if present
    for i, r in enumerate(bk):
        if "6" in r["floor"]:
            axB.plot(x[i], r["floor"]["6"], "*", color="#2e8b57", ms=13,
                     label="K=6" if i == 0 else None)
    axB.axhline(1e-2, color="gray", ls=":", lw=1.2)
    axB.set_xticks(x); axB.set_xticklabels(labels)
    axB.set_ylabel("residual floor")
    axB.set_title("B. CONVERGENCE at the boundary: floor plateaus under\n"
                  "~1.7x budget AND K=4->6 -> the crossing is genuine", fontsize=10.5)
    axB.legend(fontsize=8.5); axB.grid(alpha=0.25, axis="y")

    # -- Panel C: a_p(K) saturation ------------------------------------------
    axC = ax[1, 0]
    Kv = np.array([2, 3, 4])
    apv = np.array([a_p[K] for K in Kv])
    axC.plot(Kv, apv, "o-", color="#1f4e79", lw=2.2, ms=9, label="measured $a_p(K)$")
    axC.axhline(a_star, color="#1f4e79", ls="--", lw=1.0, alpha=0.6)
    axC.text(2.05, a_star + 0.005, f"genuine boundary $a^*\\approx{a_star:.2f}$",
             fontsize=8.5, color="#1f4e79")
    # a guide: if it "kept marching out" it would not flatten
    axC.plot(Kv, apv[0] + 0.1 * (Kv - 2), ":", color="#c1440e", lw=1.4,
             label="(if genome-limited: keeps rising)")
    axC.set_xticks(Kv)
    axC.set_ylim(min(apv.min(), a_star) - 0.08, apv.max() + 0.12)
    axC.set_xlabel("even genome richness  K  (number of Lorentzian poles)")
    axC.set_ylabel("persistence window  $a_p$")
    axC.set_title("C. $a_p(K)$ SATURATES: K=2 understates, richer genome\n"
                  "converges to the genuine boundary (not marching out)", fontsize=10.5)
    axC.legend(fontsize=8.5, loc="lower right"); axC.grid(alpha=0.25)

    # -- Panel D: resolution + basis independence ----------------------------
    axD = ax[1, 1]
    for K in (2, 3, 4):
        wpt = np.array([r["width_pts"].get(str(K), np.nan) for r in recs])
        axD.plot(a, wpt, "o-", color=cols[K], lw=1.5, ms=4, label=f"width K={K}")
    axD.axhline(8, color="k", ls=":", lw=1.2)
    axD.text(0.02, 9, "resolution guard 8 pts", fontsize=8)
    axD.set_xlabel("advection parameter  a"); axD.set_ylabel("half-max width (grid pts)")
    # basis-independence inset text
    xtxt = []
    for r in recs:
        if "floor_crosscheck6" in r:
            xtxt.append(f"a={r['a']:.2f}: mixed {r['floor_crosscheck6']:.1e} vs "
                        f"K3 {r['floor']['3']:.1e}")
    axD.set_title("D. Resolution guard (W >> 8 pts everywhere) +\n"
                  "basis independence (mixed vs Lorentzian, boundary)", fontsize=10.5)
    axD.legend(fontsize=8, loc="upper left"); axD.grid(alpha=0.25)
    if xtxt:
        axD.text(0.98, 0.02, "\n".join(xtxt), transform=axD.transAxes, fontsize=7.5,
                 ha="right", va="bottom",
                 bbox=dict(boxstyle="round", fc="#f4f4f4", ec="#bbb", alpha=0.9))

    npass = sum(checks.values())
    fig.suptitle(
        f"gCLM two-scale survival boundary: a_p(K) convergence  (n={cfg['n']}, "
        f"{cfg['pop']}x{cfg['gen']}x{cfg['seeds']} GA)   —   predicate {npass}/7   —   "
        f"genuine boundary $a^*\\approx{a_star:.2f}$, NOT a Clay solve",
        fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = FIGS / "fig18_two_scale_kladder.png"
    fig.savefig(out, dpi=130)
    print(f"wrote {out}")
    print(f"  verdict {npass}/7  a_p(K)={a_p[2]:.2f}/{a_p[3]:.2f}/{a_p[4]:.2f}  "
          f"a*={a_star:.2f}  genome_conv={summ['genome_converged']}  "
          f"budget_conv={summ['budget_converged']}  basis_indep={summ['basis_independent']}")


if __name__ == "__main__":
    build_figure()
