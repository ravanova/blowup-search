"""Phase-2 P2 (fig17) evidence: does HQW25's exact a=0 two-scale TRAVELING WAVE
survive gCLM advection? A global GA fixed-point map of the two-scale residual
across the advection parameter a (a=0 CLM -> a=1 De Gregorio).

Result (LOGGED run experiments/p2_two_scale_sweep.py --logged; predicate T1-T6
locked in git first; verdict 5/6, PARTIAL by construction): the exact a=0
traveling wave Omega_2 = -1/(1+X^2) DEFORMS SMOOTHLY under advection -- it
persists (scale-invariant residual < 1e-2) for a <~ 0.4, the residual floor then
rises monotonically to ~0.18 at a=1, and the profile STAYS EVEN throughout (no
symmetry-breaking). The one clause that FAILED is the honest one: at intermediate
a the floor is partly GENOME-LIMITED (a richer even K=3 ansatz cuts the a=0.5
floor 4x), so the precise survival boundary is genome-relative -- an upper bound,
not a proof of collapse; a rigorous (Route-D) or adaptive-mesh step would sharpen
it. At a=1 (De Gregorio) K=3 does NOT rescue the floor -> that degradation is
robust. NOVEL TOY-MODEL RESEARCH (Tier-1/2), NOT a Clay solve.

Data committed as writeup/data/p2_two_scale_sweep.json (produced by the logged
harness). The figure rebuilds from it without re-running the GA sweep:
    .venv/bin/python writeup/p2_two_scale_sweep_evidence.py         # rebuild fig17
Regenerate the underlying data:
    .venv/bin/python experiments/p2_two_scale_sweep.py --logged

Four panels (fig17):
  A. a=0 KNOWN-ANSWER GATE: the exact anchor Omega_2 = -1/(1+X^2) and its Hilbert
     transform -X/(1+X^2); the two-scale residual R2 nulls to ~1e-9 (c_tw=1/2).
  B. THE MAP: scale-invariant residual floor ||R2||/||Omega H Omega|| vs a, for the
     even (two-scale-symmetric) and mixed (free-to-skew) genomes, plus the even K=3
     ladder. Persistence window a<=a_p (<1e-2) shaded; monotone rise to a=1 marked.
  C. DEFORMATION: best even profiles at a=0,0.3,0.5,1.0 (peak-normalized) -- the
     traveling bump broadens/deforms but stays even as advection grows.
  D. SYMMETRY + SCALE SELECTION: odd-fraction vs a (stays < 0.05 -> no skew) and the
     selected half-max width vs a (advection lifts the a=0 scaling degeneracy).
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DATA = Path(__file__).resolve().parent / "data"
FIGS = Path(__file__).resolve().parent / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_two_scale_sweep.json"


def build_figure():
    from solver.gclm_family import GCLMResidual, even_lorentz, clm_two_scale

    d = json.loads(JSON.read_text())
    recs = d["records"]
    cfg = d["config"]
    checks = d["predicate_checks"]
    summ = d["summary"]
    a = np.array([r["a"] for r in recs])
    re_even = np.array([r["relres_even"] for r in recs])
    re_mixed = np.array([r["relres_mixed"] for r in recs])
    odd = np.array([r["diag_mixed"]["odd_frac"] for r in recs])
    wpts = np.array([r["diag_even"]["width_pts"] for r in recs])
    lad_a = np.array([r["a"] for r in recs if "relres_even_K3" in r])
    lad_f = np.array([r["relres_even_K3"] for r in recs if "relres_even_K3" in r])

    R0 = GCLMResidual(a=0.0, n=cfg["n"])
    X = R0.X

    fig, ax = plt.subplots(2, 2, figsize=(12.5, 9.2))

    # -- Panel A: a=0 known-answer gate --------------------------------------
    Om2 = clm_two_scale(X)
    H2 = R0.Hmat @ Om2
    resA, c_tw = R0.residual_two_scale(Om2)
    rmsA = float(np.sqrt(np.mean(resA ** 2)))
    m = np.abs(X) < 8
    axA = ax[0, 0]
    axA.plot(X[m], Om2[m], lw=2.2, color="#1f4e79", label=r"$\Omega_2=-1/(1+X^2)$")
    axA.plot(X[m], H2[m], lw=1.8, color="#c1440e", label=r"$H(\Omega_2)=-X/(1+X^2)$")
    axA.plot(X[m], resA[m] * 1e6, lw=1.2, color="#2e8b57", ls="--",
             label=r"$R_2 \times 10^{6}$")
    axA.axhline(0, color="k", lw=0.6, alpha=0.4)
    axA.set_title(f"A. a=0 known-answer gate: exact traveling wave\n"
                  f"$R_2$ RMS = {rmsA:.1e},  gauge speed $c_{{tw}}$ = {c_tw:.4f} "
                  f"(exact 1/2)", fontsize=10.5)
    axA.set_xlabel("X"); axA.set_ylabel("profile / transform")
    axA.legend(fontsize=8.5, loc="lower right"); axA.grid(alpha=0.25)

    # -- Panel B: the map -----------------------------------------------------
    axB = ax[0, 1]
    axB.semilogy(a, re_even, "o-", color="#1f4e79", lw=1.8, ms=5,
                 label="even genome (K=2)")
    axB.semilogy(a, re_mixed, "s--", color="#8064a2", lw=1.4, ms=4,
                 label="mixed genome (even+odd, K=2)")
    axB.semilogy(lad_a, lad_f, "D", color="#c1440e", ms=8, mfc="none", mew=2,
                 label="even K=3 (genome-limit check)")
    axB.axhline(1e-2, color="gray", ls=":", lw=1.2)
    axB.text(0.02, 1.2e-2, "persistence threshold $10^{-2}$", fontsize=8, color="gray")
    a_p = summ["a_p"]
    axB.axvspan(0, a_p, color="#1f4e79", alpha=0.08)
    axB.text(a_p / 2, 3e-7, f"persists\n$a\\leq a_p={a_p:.2f}$", fontsize=8.5,
             ha="center", color="#1f4e79")
    axB.annotate(f"K=3 rescues here\n(genome-limited)", xy=(0.5, lad_f[2]),
                 xytext=(0.35, 3e-4), fontsize=8, color="#c1440e",
                 arrowprops=dict(arrowstyle="->", color="#c1440e", lw=1.2))
    axB.set_title("B. THE MAP: scale-invariant residual floor "
                  r"$\|R_2\|/\|\Omega H\Omega\|$ vs advection $a$", fontsize=10.5)
    axB.set_xlabel("advection parameter  a   (0 = CLM,  1 = De Gregorio)")
    axB.set_ylabel("residual floor (log)")
    axB.legend(fontsize=8.5, loc="lower right"); axB.grid(alpha=0.25, which="both")

    # -- Panel C: deformation -------------------------------------------------
    axC = ax[1, 0]
    show = [0.0, 0.3, 0.5, 1.0]
    colors = ["#1f4e79", "#2e8b57", "#e08a1e", "#c1440e"]
    mc = np.abs(X) < 10
    for av, col in zip(show, colors):
        rec = min(recs, key=lambda r: abs(r["a"] - av))
        prof = even_lorentz(X, rec["genome_even"])
        prof = prof / np.abs(prof).max()  # peak-normalize
        axC.plot(X[mc], prof[mc], lw=2.0, color=col,
                 label=f"a={rec['a']:.1f}  (floor {rec['relres_even']:.1e})")
    axC.set_title("C. Best even profile vs a (peak-normalized):\n"
                  "the traveling bump deforms but stays even", fontsize=10.5)
    axC.set_xlabel("X"); axC.set_ylabel(r"$\Omega/\max|\Omega|$")
    axC.legend(fontsize=8.5, loc="lower center"); axC.grid(alpha=0.25)

    # -- Panel D: symmetry + scale selection ----------------------------------
    axD = ax[1, 1]
    axD.plot(a, odd, "o-", color="#7030a0", lw=1.8, ms=5, label="odd-fraction (mixed)")
    axD.axhline(0.05, color="#7030a0", ls=":", lw=1.0, alpha=0.7)
    axD.text(0.02, 0.052, "skew threshold 0.05", fontsize=8, color="#7030a0")
    axD.set_ylim(-0.005, 0.08)
    axD.set_xlabel("advection parameter  a"); axD.set_ylabel("odd-fraction", color="#7030a0")
    axD.tick_params(axis="y", labelcolor="#7030a0")
    axD2 = axD.twinx()
    axD2.plot(a, wpts, "s--", color="#1f7a1f", lw=1.4, ms=4, label="selected width")
    axD2.set_ylabel("half-max width (grid pts)", color="#1f7a1f")
    axD2.tick_params(axis="y", labelcolor="#1f7a1f")
    axD2.axhline(8, color="#1f7a1f", ls=":", lw=1.0, alpha=0.6)
    axD.set_title("D. Symmetry preserved (odd-frac < 0.05) +\n"
                  "advection selects a finite scale (lifts a=0 valley)", fontsize=10.5)
    axD.grid(alpha=0.2)

    npass = sum(checks.values())
    fig.suptitle(
        f"gCLM two-scale traveling wave under advection  (n={cfg['n']}, "
        f"{cfg['seeds']} seeds/a)   —   predicate {npass}/6, PARTIAL by "
        f"construction   —   Tier-1/2, NOT a Clay solve",
        fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = FIGS / "fig17_two_scale_sweep.png"
    fig.savefig(out, dpi=130)
    print(f"wrote {out}")
    print(f"  verdict {npass}/6  a_p={summ['a_p']}  floor@a=1={summ['floor_at_a1']:.2e}  "
          f"odd_max={summ['odd_frac_max']:.3f}  genome_limited={summ['genome_limited']}")


if __name__ == "__main__":
    build_figure()
