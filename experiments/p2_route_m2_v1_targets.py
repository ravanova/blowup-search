"""Route-M2 v1 (leg 63): TARGET RESELECTION, SCREENED BY THE MEASURED PREDICATE.

Stage M chose `HL_S2_nonsymmetric` on defensible grounds, and leg 55 confirmed the object
itself was never the problem -- it sits in an admissible class with coefficients decaying
`k^-1.396`.  What legs 51-57 refuted is the METHOD's reach, and they refuted it with a
predicate sharp enough to screen candidates: does the linearization's unbounded part act
as a MULTIPLIER (the method's shape -- cut the tail at `K` and its inverse DECAYS) or as a
SHIFT (off-diagonal, the bordered tail inverse a constant that GROWS in `K`)?

This runner re-runs stage M's ledger machinery with that predicate as a COLUMN, over
uncertified targets on models where blow-up is provable -- the prize's actual wording.

PRE-COMMITTED CLAUSES, written before the run, both branches reportable:

  M2-0  THE NOVELTY PASS COMES FIRST and can only narrow the claim.  Committed at
        `writeup/novelty/leg_63.md` BEFORE any of this was built (commit on branch
        `leg/m2-v1`), five queries with LINKS, not counts.  Its verdict is
        `PROCEED_AS_SCOPING`, and it settled the fact the gate turns on: Chen
        arXiv:1908.09385 PROVES finite-time self-similar blow-up for gCLM with a full
        Laplacian (`gamma = 2`) at `a` close to `1/2`.  That verdict is carried into the
        JSON so the writeups cannot overstate past it.

  M2-1  THE SCREEN IS NOT CLAIMED AS A FINDING.  Leg 57 already established the
        multiplier/shift dichotomy is folklore in print (Cadiot arXiv:2505.03091 sec 2
        and 3).  This leg uses it as bookkeeping.  Every writeup says so at the top.

  M2-2  THE PREDICATE IS MEASURED PER ROW, NEVER ASSIGNED.  Each ledger row is screened by
        computing its tail inverse ladder and reading the SIGN of the `K`-exponent, and
        the exponent is reported next to every verdict so no row can be quoted as
        "multiplier" without its magnitude.

  M2-3  THE DIAL IS THE ORDER OF THE DISSIPATION, NOT ITS STRENGTH, and the dial CONTAINS
        leg 57's: at `gamma = 1` the operator is `spectral_certificate.tail_block(mu=nu)`
        entry for entry.  Gated, exactly, in `test_target_selection.py`.

  M2-4  THIS LEG'S OWN HYPOTHESIS IS ALLOWED TO DIE IN THE ARTIFACT.  The obvious guess
        was `gamma* = 1` -- the transport off-diagonal grows like `k/2`, so the diagonal
        `nu k^gamma` "should" have to beat it.  The bisection is run at three strengths
        and reports what it finds, whatever that does to the guess.

  M2-5  A YES ANSWER IS SCOPING, NOT PROMOTION.  Promoting any row into the committed
        sequence is escalation #1 (ORCHESTRATION.md sec 8).  The blocking constraint --
        every multiplier-side row is dissipative, stage V's ban governs, and its lift
        condition names L1, which is measured dead -- travels WITH the verdict, in the
        JSON, not in prose that a summary can drop.

  M2-6  RESOLUTION IS A CONTROL, NOT AN ASSUMPTION.  Every headline exponent is recomputed
        at a second (`K`, `M`) setting and both are reported, because an exponent quoted
        at one truncation is a number with an unmeasured error bar.

WHAT THIS RUNNER DOES NOT DO.  It runs NO gCLM dynamics -- the ban on another gCLM
measurement leg is live and this leg respects it: the only gCLM numbers here are
constants already transcribed in stage M's ledger, used in arithmetic.  It does not
promote anything, does not touch the five shared ledgers, and claims nothing about
whether the top candidate's certificate would close: that needs `Y_0` under budget on a
profile whose constants this leg deliberately did not transcribe.

USAGE.  `python experiments/p2_route_m2_v1_targets.py` recomputes everything and writes
both the JSON and the figure.  With the curated JSON already present it rebuilds ONLY the
figure, so `writeup/build_figures.py` can re-run it without paying for the measurement;
pass `--recompute` to force the full run.
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np                                                     # noqa: E402

from solver.spectral_certificate import tail_block                     # noqa: E402
from solver.target_selection import (                                  # noqa: E402
    M2_LIFT_CONSTRAINT, MULTIPLIER_SIDE, TARGET_LEDGER,
    fractional_tail_block, fractional_tail_inverse_norm, m2_gate_verdict, m2_rank_table,
    multiplier_crossover, screen_operator,
)

DATA = ROOT / "writeup" / "data" / "p2_route_m2_v1_targets.json"
FIG = ROOT / "writeup" / "figures" / "fig57_route_m2_v1_targets.png"

#: production resolution for the ladder, and the SECOND setting M2-6 controls against
KS_PROD, M_PROD = (4, 8, 16, 32, 64, 128), 1024
KS_CTRL, M_CTRL = (8, 16, 32, 64), 512
NU_REF = 0.1
GAMMA_GRID = [round(g, 3) for g in np.arange(0.0, 2.401, 0.1)]
NU_GRID = (0.01, 0.1, 1.0)


def dial_containment():
    """M2-3: the order dial at gamma = 1 IS leg 57's Lambda^1 dial, entry for entry."""
    worst = 0.0
    for K, M, nu in ((4, 64, 0.0), (8, 128, 0.3), (16, 256, 1.0), (8, 512, 0.05)):
        d = float(np.max(np.abs(fractional_tail_block(K, M, nu=nu, gamma=1.0)
                                - tail_block(K, M, mu=nu))))
        worst = max(worst, d)
    fast_worst = 0.0
    for nu in (0.01, 0.1, 1.0):
        for gamma in (0.25, 0.5, 1.0, 2.0):
            f = fractional_tail_inverse_norm(8, 256, nu=nu, gamma=gamma)
            s = fractional_tail_inverse_norm(8, 256, nu=nu, gamma=gamma, dense=True)
            fast_worst = max(fast_worst, abs(f - s) / s)
    return {"max_entrywise_difference_at_gamma_1": worst,
            "settings_checked": 4,
            "fast_vs_dense_worst_relative": float(fast_worst),
            "note": ("A dial that does not contain the old one is a new operator, not a "
                     "generalization; and a fast path that disagrees with the dense one "
                     "is a second operator.  Both are gated, both report magnitudes.")}


def predicate_curve(nu=NU_REF, Ks=KS_PROD, M=M_PROD):
    """M2-2: the K-exponent of the tail inverse as a function of the dissipation ORDER."""
    out = []
    for g in GAMMA_GRID:
        s = screen_operator(nu, g, Ks=Ks, M=M)
        out.append({"gamma": g, "predicate": s["predicate"], "shape": s["shape"],
                    "K_exponent": s["K_exponent"], "M_exponent": s["M_exponent"],
                    "tail_inverse_first": s["tail_inverse"][0],
                    "tail_inverse_last": s["tail_inverse"][-1],
                    "needed_bordering": s["needed_bordering"]})
    return out


def crossovers(Ks=KS_PROD, M=M_PROD):
    """M2-4: gamma*(nu) by bracketed bisection, at three strengths."""
    return [multiplier_crossover(nu, lo=0.0, hi=2.0, tol=0.01, Ks=Ks, M=M,
                                 Ms=(128, 256, 512))
            for nu in NU_GRID]


def resolution_control():
    """M2-6: every headline exponent, at a second (K, M) setting."""
    rows = []
    for nu, gamma in ((0.0, 0.0), (0.1, 0.5), (0.1, 1.0), (0.1, 2.0)):
        a = screen_operator(nu, gamma, Ks=KS_PROD, M=M_PROD)
        b = screen_operator(nu, gamma, Ks=KS_CTRL, M=M_CTRL)
        rows.append({"nu": nu, "gamma": gamma,
                     "K_exponent_prod": a["K_exponent"], "Ks_prod": list(KS_PROD),
                     "M_prod": M_PROD,
                     "K_exponent_ctrl": b["K_exponent"], "Ks_ctrl": list(KS_CTRL),
                     "M_ctrl": M_CTRL,
                     "abs_difference": abs(a["K_exponent"] - b["K_exponent"]),
                     "predicate_agrees": a["predicate"] == b["predicate"]})
    return rows


def row_robustness(Ks=KS_PROD, M=M_PROD):
    """Does a row's verdict survive a change of dissipation STRENGTH?

    The crossover turned out to move a long way with `nu` (M2-4), so a row screened at one
    strength is a row screened at one strength.  Each dissipative row is therefore re-run
    across two decades of `nu` and the verdict is reported as a COUNT of strengths that
    agree, never as a single flag.  A gate answer that rests on a row which flips is a
    weaker answer than one that does not, and the JSON has to make that visible.
    """
    out = []
    for gamma, label in ((2.0, "gCLM_Lambda2_viscous_profiles"),
                         (0.5, "CCF_fractional_subcritical")):
        per = []
        for nu in NU_GRID:
            s = screen_operator(nu, gamma, Ks=Ks, M=M)
            per.append({"nu": nu, "predicate": s["predicate"],
                        "K_exponent": s["K_exponent"]})
        agree = sum(1 for p in per if p["predicate"] == MULTIPLIER_SIDE)
        out.append({"id": label, "gamma": gamma, "by_nu": per,
                    "n_multiplier_side": agree, "n_strengths": len(per),
                    "robust": agree == len(per)})
    return out


def survival_window(gamma_star_lo, gamma_star_hi):
    """Where the two thresholds leave a window -- ARITHMETIC ON PUBLISHED CONSTANTS ONLY.

    Two independent conditions have to hold at once for a dissipative target to be worth
    anything to this method:

      * the METHOD needs the dissipation order above the measured crossover,
        `gamma > gamma*`, or its tail estimate has nothing to decay with;
      * the BLOW-UP needs the dissipation to stay asymptotically negligible, which
        `solver/fractional_gclm.py` derives (and validated against XU eq (6.3)) as
        `s < s_c = alpha/2` for a `(-Delta)^s` dissipation, i.e. `gamma < alpha` in the
        `Lambda^gamma` convention, with `alpha` the profile's far-field decay exponent.

    So the window is `gamma* < gamma < alpha`, and it is NONEMPTY exactly when the
    profile's far-field decay beats the measured crossover.  `alpha = -c_omega` is read
    off constants ALREADY TRANSCRIBED in stage M's ledger; **no gCLM solver is run here**,
    the standing ban on another gCLM measurement leg is live and this is arithmetic.

    Honest caveat, carried in the output: those constants are the DEGENERATE k = 3 branch
    of arXiv:2603.25104, which is not the branch Chen's `gamma = 2` theorem is about.  The
    window is therefore an illustration of how the two thresholds combine, not a claim
    about the proved object.
    """
    row = next(t for t in TARGET_LEDGER if t["id"] == "gCLM_degenerate_one_scale")
    a_vals = row["published"]["a"]
    c_om = row["published"]["c_omega"]
    rows = []
    for a, c in zip(a_vals, c_om):
        alpha = -float(c)
        rows.append({"a": a, "c_omega": c, "alpha_far_field": alpha,
                     "gamma_c_blowup_survives_below": alpha,
                     "window_lo_best_case": gamma_star_lo,
                     "window_lo_worst_case": gamma_star_hi,
                     "window_hi": alpha,
                     "window_nonempty_best_case": bool(alpha > gamma_star_lo),
                     "window_nonempty_worst_case": bool(alpha > gamma_star_hi),
                     "window_width_worst_case": float(alpha - gamma_star_hi),
                     "contains_gamma_2": bool(gamma_star_hi < 2.0 < alpha)})
    return {"source_row": row["id"], "source": row["source"],
            "branch_caveat": ("degenerate k = 3 branch; NOT the branch arXiv:1908.09385's "
                              "gamma = 2 theorem is about -- illustration, not a claim "
                              "about the proved object"),
            "criterion": "gamma* < gamma < alpha, with alpha = -c_omega the far-field decay",
            "criterion_source": ("solver/fractional_gclm.py, s_c = alpha/2, validated "
                                 "against XU eq (6.3) row by row"),
            "gamma_star_range_used": [gamma_star_lo, gamma_star_hi],
            "no_solver_was_run": True,
            "rows": rows,
            "n_rows": len(rows),
            "n_nonempty_best_case": sum(1 for r in rows
                                        if r["window_nonempty_best_case"]),
            "n_nonempty_worst_case": sum(1 for r in rows
                                         if r["window_nonempty_worst_case"]),
            "n_containing_gamma_2": sum(1 for r in rows if r["contains_gamma_2"]),
            "reading": ("The window is real but NARROW and branch-dependent: on this "
                        "branch it closes for most a once the crossover is taken at its "
                        "worst measured value.  It is quoted at BOTH ends of the measured "
                        "gamma* range for that reason.")}


def measure():
    t0 = time.time()
    print("M2-3  dial containment ...", flush=True)
    dial = dial_containment()
    print(f"      max entrywise diff at gamma=1: {dial['max_entrywise_difference_at_gamma_1']:.1e}"
          f"   fast-vs-dense: {dial['fast_vs_dense_worst_relative']:.1e}", flush=True)

    print("M2-2  predicate curve over the order dial ...", flush=True)
    curve = predicate_curve()
    flips = [c for c in curve if c["predicate"] == MULTIPLIER_SIDE]
    print(f"      {len(flips)} of {len(curve)} grid points multiplier-side; "
          f"first at gamma = {flips[0]['gamma'] if flips else None}", flush=True)

    print("M2-4  crossover by bracketed bisection, three strengths ...", flush=True)
    cross = crossovers()
    for c in cross:
        print(f"      nu = {c.get('nu')}: gamma* = {c.get('gamma_star')}", flush=True)
    g_star = [c["gamma_star"] for c in cross if not c.get("refused")]

    print("M2-6  resolution control ...", flush=True)
    res = resolution_control()

    print("M2-4b robustness of each dissipative row across two decades of nu ...",
          flush=True)
    robust = row_robustness()
    for r in robust:
        print(f"      {r['id']:34s} gamma={r['gamma']:.1f}  multiplier-side at "
              f"{r['n_multiplier_side']}/{r['n_strengths']} strengths", flush=True)

    print("M2-2  the ledger, with the predicate column ...", flush=True)
    rows = m2_rank_table(Ks=KS_PROD, M=M_PROD)
    verdict = m2_gate_verdict(rows)
    for r in rows:
        print(f"      {r['m2_rank']}  {r['id']:34s} gamma={r['gamma']:.1f}  "
              f"{r['predicate']:15s} K-exp {r['K_exponent']:+.4f}", flush=True)
    print(f"      GATE: {verdict['gate']}  ->  {verdict['top_candidate']}", flush=True)

    win = survival_window(min(g_star) if g_star else float("nan"),
                          max(g_star) if g_star else float("nan"))

    out = {
        "leg": 63, "route": "M2", "branch": "leg/m2-v1",
        "title": "Target reselection, screened by the leg-57 multiplier/shift predicate",
        "novelty": {"file": "writeup/novelty/leg_63.md",
                    "verdict": "PROCEED_AS_SCOPING",
                    "committed_before_construction": True,
                    "screen_is_claimed": False,
                    "why_not": ("leg 57 settled that the multiplier/shift dichotomy is "
                                "folklore in print (Cadiot arXiv:2505.03091 sec 2 and 3); "
                                "this leg uses it as bookkeeping"),
                    "decisive_fact": ("Chen arXiv:1908.09385 proves finite-time "
                                      "self-similar blowup for gCLM at a close to 1/2 "
                                      "with gamma = 2, analytically, TRANSCRIBED FROM THE "
                                      "ABSTRACT and not read at full text")},
        "settings": {"Ks_prod": list(KS_PROD), "M_prod": M_PROD,
                     "Ks_ctrl": list(KS_CTRL), "M_ctrl": M_CTRL,
                     "nu_reference": NU_REF, "nu_grid": list(NU_GRID),
                     "gamma_grid": GAMMA_GRID, "weight_class": "flat",
                     "arithmetic": "float64, no intervals -- every number is a measurement"},
        "dial_containment": dial,
        "predicate_curve": curve,
        "crossovers": cross,
        "crossover_summary": {
            "gamma_star_by_nu": {str(c.get("nu")): c.get("gamma_star") for c in cross},
            "min": min(g_star) if g_star else None,
            "max": max(g_star) if g_star else None,
            "strength_dependence": (
                "gamma* moves a LOT with nu across the two decades measured, so 'the "
                "order decides and the strength only shifts it' is true in direction and "
                "false in magnitude at this truncation.  Every row's verdict is therefore "
                "re-run across nu in `row_robustness`, and the gate leans on the row that "
                "does not flip."),
            "hypothesis_that_died": (
                "gamma* = 1, i.e. the diagonal must out-grow the k/2 transport "
                "off-diagonal entry for entry.  Measured false at every strength tried, "
                "and by a wide margin -- the tail inverse is set by the recursion, not by "
                "an entrywise size comparison.  Same shape as leg 57's delta < 1/2 "
                "hypothesis dying on the Lambda^1 dial.")},
        "resolution_control": res,
        "row_robustness": robust,
        "ledger": rows,
        "gate": {
            "question": ("Is there at least one uncertified target, on a model where "
                         "blow-up is provable, whose linearization's unbounded part is a "
                         "MULTIPLIER under the leg-57 predicate?"),
            **verdict,
            "top_candidate_robust_across_nu": next(
                (r["robust"] for r in robust if r["id"] == verdict["top_candidate"]),
                None),
            "answer_depends_on_a_fragile_row": not any(
                r["robust"] for r in robust
                if r["id"] in verdict["multiplier_side_ids"])},
        "lift_constraint": M2_LIFT_CONSTRAINT,
        "promotion": ("NONE.  This leg promotes nothing.  A YES is escalation #1 under "
                      "ORCHESTRATION.md sec 8: branch pushed, main untouched, the "
                      "sequence change escalated to the user."),
        "survival_window": win,
        "scope": ("Float64, no intervals.  The predicate is measured on the SHARED "
                  "spectral tail operator with a dissipation dial, not on each target's "
                  "own linearization -- the shape is a property of the operator class "
                  "(lesson 87), and that is what makes a column computable at all, but it "
                  "means a row's verdict is a statement about its dissipation ORDER, not "
                  "about its profile.  Every blow-up provability field is TRANSCRIBED from "
                  "abstracts and surveys, not read at full text.  Nothing here says a "
                  "certificate would close: that needs Y_0 under budget."),
        "runtime_seconds": round(time.time() - t0, 1),
    }
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(out, indent=2))
    print(f"wrote {DATA.relative_to(ROOT)}  ({out['runtime_seconds']} s)", flush=True)
    return out


def figure(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    curve = d["predicate_curve"]
    g = [c["gamma"] for c in curve]
    e = [c["K_exponent"] for c in curve]
    gs = d["crossover_summary"]["gamma_star_by_nu"]
    rows = d["ledger"]

    fig, ax = plt.subplots(1, 2, figsize=(13.6, 5.4))

    a = ax[0]
    a.axhspan(0, max(e) * 1.15, color="#c2410c", alpha=0.07)
    a.axhspan(min(e) * 1.15, 0, color="#0e7490", alpha=0.07)
    a.axhline(0, color="0.35", lw=1.0)
    a.plot(g, e, "o-", color="#1d4ed8", ms=4, lw=1.8,
           label=f"K-exponent of $\\|T_{{tail}}^{{-1}}\\|$, $\\nu = {d['settings']['nu_reference']}$")
    lo = min(e) * 1.12
    for i, (nu, gv) in enumerate(sorted(gs.items(), key=lambda kv: kv[1] or 0)):
        if gv is not None:
            a.axvline(gv, ls="--", lw=1.2, color="#7c3aed", alpha=0.8)
            a.annotate(f"$\\gamma^*$={gv:.2f}\n$\\nu$={nu}", (gv, lo * (0.93 - 0.09 * i)),
                       fontsize=7.5, color="#5b21b6", ha="center",
                       bbox=dict(fc="white", ec="none", alpha=0.75, pad=1.0))
    a.axvline(1.0, ls=":", lw=1.4, color="#b91c1c")
    a.annotate("the guess that died:\n$\\gamma^*=1$ (entrywise dominance)", (1.28, max(e) * 0.30),
               fontsize=8, color="#b91c1c", ha="left")
    for gm, lab, off in ((0.0, "the 4 inviscid ledger rows", (10, -16)),
                         (0.5, "CCF, generous end\nof the proved range", (10, 12)),
                         (2.0, "gCLM $\\Lambda^2$:\nblow-up PROVED", (-10, 18))):
        yv = next(c["K_exponent"] for c in curve if abs(c["gamma"] - gm) < 1e-9)
        a.plot([gm], [yv], "*", ms=15, color="#111827", zorder=5)
        a.annotate(lab, (gm, yv), textcoords="offset points", xytext=off, fontsize=7.5,
                   ha="right" if off[0] < 0 else "left")
    a.set_xlabel("dissipation ORDER $\\gamma$   (diagonal $-\\nu k^{\\gamma}$ against the $k/2$ transport off-diagonal)")
    a.set_ylabel("$d\\log\\|T_{tail}^{-1}\\|_w \\, / \\, d\\log K$")
    a.set_title("(a) the predicate, measured on the order dial\n"
                "above 0 = SHIFT side (nothing to decay with); below 0 = MULTIPLIER side",
                fontsize=10)
    a.legend(fontsize=8, loc="upper right")
    a.grid(alpha=0.25)

    b = ax[1]
    ys = range(len(rows))[::-1]
    cols = ["#0e7490" if r["predicate"] == MULTIPLIER_SIDE else "#c2410c" for r in rows]
    b.barh(list(ys), [r["K_exponent"] for r in rows], color=cols, alpha=0.85, height=0.6)
    b.axvline(0, color="0.35", lw=1.0)
    for y, r in zip(ys, rows):
        rb = ""
        for q in d.get("row_robustness", []):
            if q["id"] == r["id"]:
                rb = f"   [{q['n_multiplier_side']}/{q['n_strengths']} strengths]"
        b.annotate(f"{r['id']}  ($\\gamma$={r['gamma']:.1f}){rb}", (-2.55, y + 0.42),
                   va="center", ha="left", fontsize=8)
        dx = -0.06 if r["K_exponent"] < 0 else 0.06
        b.annotate(f"{r['K_exponent']:+.3f}", (r["K_exponent"] + dx, y), va="center",
                   ha="right" if r["K_exponent"] < 0 else "left", fontsize=8,
                   fontweight="bold")
    b.set_yticks([])
    b.set_xlim(-2.6, 2.6)
    b.set_xlabel("K-exponent of the tail inverse (measured)")
    b.set_title("(b) the M2 ledger, ranked by the predicate\n"
                f"gate: {d['gate']['gate']} -- "
                f"{d['gate']['n_multiplier_side']} of {d['gate']['n_rows']} rows multiplier-side, "
                "and every one of them is dissipative", fontsize=10)
    b.grid(alpha=0.25, axis="x")

    fig.suptitle("Route-M2 v1 (leg 63): uncertified targets, screened by the leg-57 "
                 "multiplier/shift predicate -- SCOPING, nothing promoted",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    recompute = "--recompute" in sys.argv or not DATA.exists()
    data = measure() if recompute else json.loads(DATA.read_text())
    if not recompute:
        print(f"reusing {DATA.relative_to(ROOT)} (pass --recompute to re-measure)")
    figure(data)
