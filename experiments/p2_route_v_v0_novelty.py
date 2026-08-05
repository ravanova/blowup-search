"""Route-V v0: stage V's NOVELTY GATE, and the re-derivation of the paper that answers it.

Stage V asks: switch dissipation on, and does the blow-up certificate's margin still
close?  `plan_of_record.py` puts a BAN in front of that question --

    FIRST: has anyone already done certification-under-dissipation for a self-similar
    blow-up profile?  yes -> report it, fall back to C-PILOT, do NOT spend the leg.

-- because leg 42 deleted seven of twelve novelty claims and stage V was flagged as a
speculation of the same kind when it was proposed.  This run is that gate, asked before
any stage-V measurement exists.

THE ANSWER IS YES.  Dahne-Figueras, arXiv:2410.05480, prove branches of self-similar
singular solutions of the complex Ginzburg-Landau equation, continued in the DISSIPATION
parameter eps from the conservative NLS limit, and verify them in interval arithmetic --
whole-branch in their Case I, partially in Case II.  That is stage V's question, answered
in 2024, with rigour this project does not have.

PRE-COMMITTED CLAUSES, written before the run (both branches of each are reportable):

  V0-1  THE GATE.  The ledger's verdict is computed, not remembered.  YES -> the leg
        reports the pre-emption and stops; NO -> stage V proceeds and this file becomes
        the first half of it.
  V0-2  THE PRE-EMPTION IS RE-DERIVED, NOT ASSERTED.  An independent integrator and an
        independently derived far-field expansion must land on their published (mu,
        kappa) for Case I j=1 and Case II j=1.  Threshold 1e-06.  If it does NOT, the
        gate is reported as UNVERIFIED and the leg says so instead of claiming the
        pre-emption.
  V0-3  THE GUARDS COME BEFORE THE CLAIM.  Step halving must move the defect by less than
        the defect, and the answer must not move as the matching point xi_1 goes out.
  V0-4  THE DISSIPATION DIAL.  Continue branch j = 1 in eps.  Report the fold as a
        magnitude and compare it against their own Fig. 1a, read as vector data.
  V0-5  THE SHAPE OF THEIR ANSWER, which is the part stage V would have wanted:
        ||J^-1|| along the branch -- the float analogue of the certificate's ||A||.
        Does the margin die when dissipation switches on, or at the fold?
  V0-6  THE CEILING.  Whatever this leg finds, it moves no link of the L1->L4 chain, and
        a reproduction of somebody else's certified branch is not a result of ours.

Deterministic, ~4 min.  Writes writeup/data/p2_route_v_v0_novelty.json.

Run: .venv/bin/python -u experiments/p2_route_v_v0_novelty.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.viscous_novelty import (                                  # noqa: E402
    DF_FIG1A_BRANCH1_FOLD, DF_FIG1A_BRANCH1_SAMPLES, DF_TABLE1, DF_TABLE2,
    DF_EPS_RANGE, PRECEDENTS, SEARCH_LOG, branch_in_kappa, compare_to_published_branch,
    fold_of, margin_law, margin_proxy, match_defect, novelty_verdict, read_df_figure,
    resolution_ladder, shoot_newton, xi1_ladder,
)

OUT = ROOT / "writeup" / "data" / "p2_route_v_v0_novelty.json"
PDF = ROOT / "Papers" / "2410.05480.pdf"

REPRODUCTION_GATE = 1e-6          # V0-2
DKAPPA = 0.005                    # V0-4: fine enough that the fold's parabola is resolved
KAPPA_STOP = 0.21


def main():
    t0 = time.time()
    out = {}

    # ---- V0-1 the gate ---------------------------------------------------
    answer, pre = novelty_verdict()
    out["V0_1_gate"] = {
        "question": "has anyone already done certification-under-dissipation for a "
                    "self-similar blow-up profile?",
        "answer": answer,
        "pre_empting": [p["id"] for p in pre],
        "ledger": PRECEDENTS,
        "search_log": [{"query": q, "hits": n} for q, n in SEARCH_LOG],
        "action": ("stage V is pre-empted; fall back to C-PILOT" if answer == "YES"
                   else "stage V proceeds"),
    }
    print(f"[V0-1] gate: {answer}  pre-empting: {[p['id'] for p in pre]}", flush=True)

    # ---- V0-2 the re-derivation ------------------------------------------
    rows = []
    for j, mu_p, kap_p, xi1_pub in DF_TABLE1:
        # their xi_1 grows with j; ours is clipped into [15, 20] because the three-term
        # far-field expansion errs at O(xi^-6) below 15 and the oscillatory integration
        # gets expensive above 20.  The gap for j = 4 (they use 25) is reported, not hidden.
        xi1 = float(np.clip(xi1_pub, 15.0, 20.0))
        (mu, kap), hist = shoot_newton(round(mu_p, 3), round(kap_p, 3), 0.0, 1, 2.3, xi1)
        rows.append({"case": "I", "j": j, "d": 1, "sigma": 2.3, "xi1": xi1,
                     "mu_published": mu_p, "kappa_published": kap_p,
                     "mu_ours": mu, "kappa_ours": kap,
                     "d_mu": mu - mu_p, "d_kappa": kap - kap_p,
                     "xi1_published": xi1_pub,
                     "newton_steps": len(hist), "defect": hist[-1]})
        print(f"[V0-2] case I  j={j}: dmu={mu - mu_p:+.2e} dkappa={kap - kap_p:+.2e} "
              f"({len(hist)} Newton steps, defect {hist[-1]:.1e})", flush=True)
    for j, mu_p, kap_p, _ in DF_TABLE2:
        (mu, kap), hist = shoot_newton(round(mu_p, 3), round(kap_p, 3), 0.0, 3, 1.0, 40.0)
        rows.append({"case": "II", "j": j, "d": 3, "sigma": 1.0, "xi1": 40.0,
                     "mu_published": mu_p, "kappa_published": kap_p,
                     "mu_ours": mu, "kappa_ours": kap,
                     "d_mu": mu - mu_p, "d_kappa": kap - kap_p,
                     "newton_steps": len(hist), "defect": hist[-1]})
        print(f"[V0-2] case II j={j}: dmu={mu - mu_p:+.2e} dkappa={kap - kap_p:+.2e} "
              f"({len(hist)} Newton steps, defect {hist[-1]:.1e})", flush=True)
    worst = max(max(abs(r["d_mu"]), abs(r["d_kappa"])) for r in rows)
    headline = max(max(abs(r["d_mu"]), abs(r["d_kappa"]))
                   for r in rows if r["j"] == 1)
    out["V0_2_reproduction"] = {
        "rows": rows, "worst_deviation": worst, "headline_deviation": headline,
        "gate": REPRODUCTION_GATE,
        "verdict": "VERIFIED" if headline < REPRODUCTION_GATE else "UNVERIFIED",
        "note": "gamma is NOT gated: DF parameterise the manifold at infinity in their "
                "sec 7 and our gamma is the coefficient in OUR expansion.",
    }

    # ---- V0-3 the guards --------------------------------------------------
    _, mu_p2, kap_p2, _ = DF_TABLE2[0]
    res = resolution_ladder(mu_p2, kap_p2, 0.0, 3, 1.0, 40.0)
    _, mu_p1, kap_p1, _ = DF_TABLE1[0]
    xil = xi1_ladder(round(mu_p1, 3), round(kap_p1, 3), 0.0, 1, 2.3, [10.0, 15.0, 20.0, 30.0])
    kap_spread = float(max(r["kappa"] for r in xil) - min(r["kappa"] for r in xil))
    out["V0_3_guards"] = {
        "resolution_ladder": res, "xi1_ladder": xil,
        "defect_moved_by_halving": abs(res[-1]["defect"] - res[0]["defect"]),
        "defect_level": res[-1]["defect"], "kappa_spread_over_xi1": kap_spread,
    }
    print(f"[V0-3] step halving moves the defect {abs(res[-1]['defect'] - res[0]['defect']):.1e} "
          f"(level {res[-1]['defect']:.1e}); xi_1 10..30 moves kappa {kap_spread:.1e}",
          flush=True)

    # ---- V0-4 the dissipation dial ---------------------------------------
    branch = branch_in_kappa(mu_p1, kap_p1, KAPPA_STOP, 1, 2.3, 15.0, dkappa=DKAPPA)
    fold = fold_of(branch)
    cmp_pub = compare_to_published_branch(branch)
    figure = read_df_figure(str(PDF), 8, "/Im1")
    fig_curve = None
    if figure is not None:
        curves, cal = figure
        e, k = curves[0]
        fig_curve = {"eps": [float(v) for v in e[::4]], "kappa": [float(v) for v in k[::4]],
                     "calibration": cal, "n_curves": len(curves),
                     "curve_starts": [float(kk[0]) for _, kk in curves[:8]]}
    out["V0_4_branch"] = {
        "records": branch, "fold": fold, "published_fold": DF_FIG1A_BRANCH1_FOLD,
        "d_eps_star": (None if fold is None else
                       fold["eps_star"] - DF_FIG1A_BRANCH1_FOLD["eps_star"]),
        "d_kappa_star": (None if fold is None else
                         fold["kappa_star"] - DF_FIG1A_BRANCH1_FOLD["kappa_star"]),
        "comparison_to_published_curve": cmp_pub,
        "published_samples": [{"kappa": k, "eps": e} for k, e in DF_FIG1A_BRANCH1_SAMPLES],
        "published_figure": fig_curve,
        "eps_axis_range": DF_EPS_RANGE["case_I"],
        "dkappa": DKAPPA,
    }
    print(f"[V0-4] fold at eps*={fold['eps_star']:.7f}, kappa*={fold['kappa_star']:.6f}  "
          f"(published {DF_FIG1A_BRANCH1_FOLD['eps_star']:.7f}, "
          f"{DF_FIG1A_BRANCH1_FOLD['kappa_star']:.6f})", flush=True)
    if cmp_pub:
        print(f"[V0-4] against their Fig. 1a on {cmp_pub['n']} samples: "
              f"max |d eps| = {cmp_pub['max_abs_diff']:.2e}, rms {cmp_pub['rms_diff']:.2e}",
              flush=True)

    # ---- V0-5 the margin proxy along the dial ----------------------------
    conv = [r for r in branch if r["converged"]]
    picks = conv[::4]
    if fold is not None:
        picks = sorted({id(r): r for r in
                        picks + [min(conv, key=lambda r: abs(r["kappa"] - fold["kappa_star"]))]}
                       .values(), key=lambda r: -r["kappa"])
    margin = []
    for r in picks:
        n_inv, cond = margin_proxy(r["mu"], r["kappa"], r["eps"], 1, 2.3, 15.0)
        margin.append({"kappa": r["kappa"], "eps": r["eps"], "Jinv_norm": n_inv,
                       "cond": cond})
    at_zero = margin[0]
    at_fold = min(margin, key=lambda m: abs(m["kappa"] - fold["kappa_star"]))
    mid = min(margin, key=lambda m: abs(m["kappa"] - 0.70))
    law = margin_law(branch, fold, 1, 2.3, 15.0)
    print(f"[V0-5] divergence exponent at the fold: {law['slope']:+.3f} "
          f"(a quadratic fold predicts -1)", flush=True)
    out["V0_5_margin"] = {
        "law": law,
        "curve": margin, "at_eps_zero": at_zero, "mid_branch": mid, "at_fold": at_fold,
        "fold_over_mid": at_fold["Jinv_norm"] / mid["Jinv_norm"],
        "mid_over_zero": mid["Jinv_norm"] / at_zero["Jinv_norm"],
        "reading": ("the margin proxy IMPROVES as dissipation is switched on and diverges "
                    "at the fold" if mid["Jinv_norm"] < at_zero["Jinv_norm"] else
                    "the margin proxy degrades from eps = 0 onward"),
    }
    print(f"[V0-5] ||J^-1||: eps=0 {at_zero['Jinv_norm']:.2e}, mid {mid['Jinv_norm']:.2e}, "
          f"fold {at_fold['Jinv_norm']:.2e}", flush=True)

    # ---- V0-6 the ceiling -------------------------------------------------
    out["V0_6_ceiling"] = {
        "moved_a_chain_link": False,
        "novel": False,
        "what_this_is": "a reproduction of a published, already-certified branch, run to "
                        "settle whether stage V had anything left to find. It did not.",
        "what_it_is_not": [
            "not a certificate: nothing here is interval-enclosed, and DF's result is "
            "the rigorous one",
            "not about a fluid model: CGL is semilinear and radial; the Hou-Luo target is "
            "a transport model on the line",
            "not Clay, not a chain link, and not evidence about Navier-Stokes",
        ],
        "clay_odds_percent": 0.05,
    }

    out["meta"] = {"seconds": time.time() - t0,
                   "deterministic": True,
                   "papers_pdf_present": PDF.exists()}
    OUT.write_text(json.dumps(out, indent=1))
    print(f"\nwrote {OUT}  ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
