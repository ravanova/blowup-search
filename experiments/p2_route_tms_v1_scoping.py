#!/usr/bin/env python3
"""Leg 315 -- ROUTE-TMS: validated integration and Taylor models, SCOPING ONLY.

WHAT THIS IS
------------
A scoping runner. It BUILDS NOTHING and RUNS NO SOLVER. It encodes, as a checkable
table, the answer to one question:

    Does at least one CONCRETE object exist that the radii-polynomial / Newton-Kantorovich
    apparatus (as this repository realizes it) does not reach, and that Taylor-model
    arithmetic does, with a NAMED reaching mechanism and an EVIDENCE-BACKED build cost class?

WHAT THIS IS NOT
----------------
* Not a build. The build is a separate leg, drafted by the DM on a YES.
* Not a policy change. `requirements.txt` is NOT touched. Every dependency observation
  below is routed as an integration note in experiments/journal/leg_315.md.
* Not a ban lift. No ban lifts here, by anything, ever. See writeup/novelty/leg_315.md sec 0.
* Not movement on the L1->L4 chain. Naming a reachable object is not reaching it.
  Walls 1 and 2 stand. Clay odds ~0.05%, unchanged.

DESIGN NOTE -- LESSON 90 (a control that cannot come out differently is not a control)
--------------------------------------------------------------------------------------
A reach matrix whose every row says "Taylor models win" would be a tautology of the
author's intent, not evidence. So the matrix carries TWO CONTROLS THAT COME OUT THE
OTHER WAY -- objects NK reaches and Taylor models do NOT (C1, C2) -- and one object
NEITHER reaches (O3). For the matrix to have reported "TM wins everywhere", C1 and C2
would have had to be scored differently, and C2 is scored off an EXTERNAL paper
(arXiv:2305.08221) that directly contradicts the naive form of this leg's own thesis.

RUNTIME
-------
Estimated < 2 s, achieved < 2 s (a table, a JSON dump and one 2-panel figure). No long
run arises; the assess-before-running-long rule is satisfied trivially and recorded.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "writeup" / "data" / "p2_route_tms_v1.json"
FIGS = ROOT / "writeup" / "figures"

# ---------------------------------------------------------------------------
# 1. The target's measured numbers. REPO-INTERNAL, carried forward, NOT re-derived.
#    Source: leg 266 -> corrected by leg 300 (experiments/journal/leg_300.md:40-51)
#    -> propagated repo-wide by leg 319 (P0TCR). gamma = 7/5 (diatomic / air).
# ---------------------------------------------------------------------------
GAMMA = "7/5"
R_DOMINANCE_LO = 1.1666667       # = 7/6, the lower endpoint
R_DOMINANCE_HI = 1.1909830       # the upper endpoint: where BCG's domination argument stops
W_CERTIFIED = 0.0243163          # width of the window BCG's dominance argument certifies
W_AVAILABLE = 0.1666667          # = 1/6, width of the window the target makes available
WIDTH_RATIO = 6.8541019662496845446   # = (7 + 3*sqrt(5))/2, leg 300's exact closed form
WIDTH_RATIO_CLOSED_FORM = "(7 + 3*sqrt(5))/2"

# ---------------------------------------------------------------------------
# 2. The reach matrix.
#
#    Columns are the two apparatus:
#      NK  = radii-polynomial / Newton-Kantorovich, AS THIS REPOSITORY REALIZES IT.
#            Lesson 91 forces the realization to be named, so every "no" below names
#            the exact realization(s) the negative holds in. It is NOT a claim about
#            NK in the abstract -- see C2, which is an NK *win* on an external result.
#      TM  = Taylor-model arithmetic / validated ODE integration (Lohner, Berz-Makino,
#            Zgliczynski; CAPD/COSY/VNODE-LP/Flow*/TaylorModels.jl).
# ---------------------------------------------------------------------------
MATRIX = [
    {
        "id": "O1",
        "kind": "target object",
        "name": (
            "The sonic-crossing r-tube: a rigorous enclosure of BCG's autonomous (W,Z) "
            "self-similar Euler ODE flow THROUGH THE SONIC POINT, carried as a Taylor "
            "model polynomial in the similarity exponent r over an r-INTERVAL at "
            "gamma = 7/5, whose output is the profile-vs-F_dis domination margin as a "
            "certified function of r extending ACROSS and BEYOND the dominance-window "
            "upper endpoint r = 1.1909830."
        ),
        "why_this_object": (
            "The verifier of leg 251 established that certificate obligation #1 named an "
            "object that DOES NOT EXIST for this target: at BCG's scaling there is no "
            "self-similar profile system of the dissipative equation. The (W,Z) reduction "
            "Thms 1.1/1.2 solve is the EULER system; dissipation enters the dynamically "
            "rescaled system as a non-autonomous, exponentially decaying forcing F_dis. "
            "The real gap is the STABILITY step -- the r-restriction that lets the profile "
            "dominate F_dis -- and the verifier re-posed the obligation at 'a similarity "
            "exponent outside BCG's dominance regime'. O1 is the first rigorous rung of "
            "exactly that re-posed obligation, and NOT a profile enclosure."
        ),
        "nk_reaches": False,
        "nk_realizations_the_negative_holds_in": [
            "ell^1_w coefficient basis (leg 54: best Z_1 improvement 1.167x where >8x needed)",
            "sup-norm collocation basis (leg 56: (H,D) defect 1.85e7x / 2.04e11x over budget)",
            "origin-H^2 capped at a=0, no transfer to the real target (legs 163/176)",
        ],
        "nk_reason": (
            "A radii-polynomial certificate is a ZERO-FINDER: it needs a fixed function "
            "space, a numerical candidate, and an approximate inverse of the linearization "
            "in that space. The (W,Z) trajectory must pass through the SONIC POINT, a "
            "degeneracy of the vector field, where a GLOBAL-basis linearization is not "
            "boundedly invertible. This repository's NK apparatus is measured dead in the "
            "three named realizations above, and its standing ban forecloses proposing a "
            "FOURTH space/basis without its own scoping leg. So the NK route is closed "
            "here by this repository's own law, not merely by difficulty."
        ),
        "tm_reaches": True,
        "reaching_mechanism": (
            "SONIC-POINT-DESINGULARIZED TAYLOR-MODEL STEPPING IN THE SIMILARITY PARAMETER. "
            "Three named parts. (i) The object is a FINITE-DIMENSIONAL AUTONOMOUS ODE -- "
            "the verifier's own words, 'the autonomous (W,Z) ODE system that Thms 1.1/1.2 "
            "solve' -- which is precisely what a validated IVP integrator is built for, and "
            "the enclosure is of the FLOW MAP, so NO function space is required. "
            "(ii) The sonic degeneracy is crossed by quasi-homogeneous desingularization "
            "plus local analytic continuation -- the technique this repository has ALREADY "
            "recorded, at writeup/data/p2_route_w2l_v1_lit.json:180, verbatim "
            "'quasi-homogeneous compactification plus rigorous integration in interval "
            "arithmetic'. (iii) Wrapping control by Lohner-QR / mean-value form / "
            "shrink-wrapping (Berz-Makino), without which naive interval stepping cannot "
            "cross an interval of useful length -- this is the part that is Taylor-model "
            "arithmetic PROPER and not merely interval arithmetic, and it is exactly what "
            "solver/interval.py cannot supply. Carrying r as a symbolic Taylor variable "
            "then certifies an r-INTERVAL in one integration rather than one r per run."
        ),
        "mechanism_honesty_caveat": (
            "The parameter-interval property (iii, last clause) is a CONVENIENCE, not the "
            "load-bearing half: radii-polynomial certificates are routinely run with "
            "interval parameters for branch continuation, so 'TM sweeps r and NK does not' "
            "would be a FALSE distinction and is not claimed. The load-bearing halves are "
            "the FLOW-MAP-vs-ZERO shape (lesson 87: the shape is a property of the "
            "operator) and the SONIC DEGENERACY defeating a global basis."
        ),
        "cost_class": "C",
        "cost_class_label": "genuine research problem, with a Class-B implementable core",
        "cost_evidence": [
            "NOT class A: no maintained, pip-installable, PYTHON Taylor-model ODE "
            "integrator was located. python-flint 0.9.0 (PyPI, released 2026-07-03, SPDX "
            "'MIT AND LGPL-3.0-or-later', requires only Python>=3.10, does NOT require "
            "scipy) supplies arb/acb rigorous balls and arb_series -- but NO Taylor-model "
            "IVP integrator. The field's implementations are out-of-language: CAPD (C++, "
            "arXiv:2010.07097), VNODE-LP (C++, unmaintained), Flow* (C++), COSY Infinity "
            "(restricted licence), TaylorModels.jl (Julia). TERA (arXiv:2607.01189, 2026) "
            "IS Python but is control-systems reachability, brand-new and unvalidated for "
            "a fluid profile.",
            "Class-B core: a Taylor-model type over solver/interval.py's existing "
            "outward-rounded Interval plus a Lohner-QR wrapping layer is a hand-roll of "
            "exactly the kind leg 256 was FORCED into (Gauss-Laguerre nodes by Sturm "
            "bisection + Newton, with per-node log renormalization, because 'with no scipy "
            "there is no Gauss-Laguerre rule to call'). Leg 256's hand-roll was one leg for "
            "a STATIC quadrature rule; a validated IVP integrator with wrapping control is "
            "strictly larger, so >= 1 leg and plausibly several.",
            "WHY C AND NOT B -- the research obstacle is not the integrator. O1 is only the "
            "first rung. The verifier's re-posed obligation is the STABILITY step with "
            "F_dis RETAINED over self-similar time s in [s_0, infinity) -- a non-autonomous "
            "PDE trapping argument, not an ODE. The standard bridge from a validated ODE "
            "integrator to a validated PDE enclosure is Zgliczynski's SELF-CONSISTENT "
            "A-PRIORI BOUNDS (math/0005247), whose hypotheses are DISSIPATIVE/parabolic. "
            "BCG's rescaled system is quasilinear HYPERBOLIC, with dissipation entering as "
            "an exponentially decaying FORCING (e^{-delta_dis s_0} prefactors) rather than "
            "as a smoothing principal part. THAT MISMATCH IS THE RESEARCH PROBLEM, and "
            "naming it is this leg's most useful output.",
        ],
    },
    {
        "id": "O2",
        "kind": "target object",
        "name": (
            "Rigorous enclosure of the degree-4503 Gauss-Laguerre nodes and weights, and of "
            "the resulting quadrature, that leg 256 had to hand-roll in float64 -- i.e. "
            "closing leg 256's OWN recorded ceiling."
        ),
        "why_this_object": (
            "capabilities.py:496-498 records the ceiling verbatim: 'CEILING: float64, NOT "
            "interval arithmetic -- this reproduces their CONSTANTS, not their proof'. "
            "Breden-Chu prove their Theorem 42 in interval arithmetic over 16384-bit "
            "BigFloat; leg 256 could not, and said so."
        ),
        "nk_reaches": False,
        "nk_realizations_the_negative_holds_in": [
            "not an NK question at all: NK certifies zeros of an operator equation, and a "
            "quadrature node enclosure is an arithmetic-substrate capability, upstream of "
            "any certificate. The negative is one of CATEGORY, not of realization.",
        ],
        "nk_reason": (
            "Out of NK's category. Recorded for completeness and because it is the leg's "
            "cheapest, most immediately actionable item -- but see the territory note: it "
            "belongs to leg 312 (Route-APIA), not to a new build leg."
        ),
        "tm_reaches": True,
        "reaching_mechanism": (
            "ARBITRARY-PRECISION BALL ARITHMETIC WITH RIGOROUS SPECIAL-FUNCTION AND ROOT "
            "ENCLOSURES. This is the VALIDATED-INTEGRATION half of the route name, not the "
            "Taylor-model half, and is labelled as such rather than smuggled in: FLINT/Arb "
            "supplies rigorous balls, arb_poly root isolation, and the exponent range that "
            "makes leg 256's e^{-1.8e4} x 1e1220 product representable DIRECTLY, removing "
            "the per-node log-renormalization scaffolding leg 256 was forced to build."
        ),
        "cost_class": "A/B split",
        "cost_class_label": (
            "Class A for the arithmetic substrate; Class B for the quadrature layer on top"
        ),
        "cost_evidence": [
            "CLASS A, with licence and version pinned: python-flint 0.9.0, PyPI, released "
            "2026-07-03, SPDX 'MIT AND LGPL-3.0-or-later' (FLINT/Arb themselves LGPL "
            "v2.1+), requires only Python>=3.10, does NOT require scipy -- so it does not "
            "even engage the 'no adaptive ODE integrators' policy line, which is about "
            "scipy and about ODE integration, neither of which this is.",
            "CLASS B for the layer: it is NOT confirmed that rigorous quadrature "
            "(acb_calc_integrate) is EXPOSED through the Python bindings -- the "
            "python-flint API page reached documents v0.3.0 and lists no .integral() "
            "method. UNDER-EVIDENCED and recorded as such rather than assumed either way. "
            "If exposed: Class A. If not: bind or hand-roll, Class B.",
            "TERRITORY: leg 312 (Route-APIA) already owns the arbitrary-precision interval "
            "build (solver/interval_mp.py). O2 is a CONSUMER of APIA, not a new build leg.",
        ],
    },
    {
        "id": "O3",
        "kind": "target object -- REACHED BY NEITHER",
        "name": (
            "Forward invariance (a trapping region) for the dynamically rescaled "
            "compressible-NS perturbation system with F_dis RETAINED, over the SEMI-INFINITE "
            "self-similar time interval s in [s_0, infinity), at r outside the dominance window."
        ),
        "why_this_object": (
            "This is the verifier's re-posed obligation in full. It is recorded here "
            "explicitly so the leg's YES is not read as bigger than it is."
        ),
        "nk_reaches": False,
        "nk_realizations_the_negative_holds_in": [
            "all three dead realizations above, plus: the semi-infinite time horizon has no "
            "compact-interval Chebyshev representation (see C2, which is compact-interval)",
        ],
        "nk_reason": "no stationary object to Newton around; semi-infinite horizon.",
        "tm_reaches": False,
        "reaching_mechanism": (
            "NONE STATED, AND NONE CLAIMED. A Taylor-model IVP integrator encloses a "
            "FINITE-dimensional flow over a FINITE time. Reaching O3 needs (a) a "
            "Galerkin-plus-tail bridge whose known form (Zgliczynski self-consistent "
            "a-priori bounds) assumes dissipativity BCG's hyperbolic system lacks, and "
            "(b) an asymptotic argument closing s* -> infinity off the e^{-delta_dis s} "
            "decay. Whether any computer-assisted work has ever enclosed a non-autonomous "
            "forcing-domination / trap-region argument of this SHAPE, in any field, is the "
            "explicit territory of leg 267 (Route-FDL). THIS LEG DOES NOT PRE-EMPT OR "
            "PREDICT FDL'S ANSWER and does not claim the precedent is absent."
        ),
        "cost_class": "C",
        "cost_class_label": "genuine research problem; not costed further here",
        "cost_evidence": [
            "Deliberately not costed: costing an object neither apparatus reaches would be "
            "vibes, which the spec forbids.",
        ],
    },
    {
        "id": "C1",
        "kind": "CONTROL -- must come out the OTHER way (lesson 90)",
        "name": (
            "A stationary zero of a nonlinear operator F(u)=0 in a weighted Banach space "
            "with an explicit approximate inverse -- e.g. this repository's own bordered "
            "certificate assembly (solver/interval_certificate.py, solver/nk_bounds.py)."
        ),
        "why_this_object": (
            "If the matrix could not report 'NK yes / TM no' anywhere, it would be a "
            "tautology of the author's intent rather than a finding."
        ),
        "nk_reaches": True,
        "nk_realizations_the_negative_holds_in": [],
        "nk_reason": (
            "This is exactly what radii-polynomial certificates are FOR, and this repo has "
            "the machinery registered in capabilities.py:238-243 and :359-360."
        ),
        "tm_reaches": False,
        "reaching_mechanism": (
            "NONE. A Taylor-model IVP integrator has no notion of an infinite-dimensional "
            "zero-finding problem with an approximate inverse. Taylor models LOSE this row."
        ),
        "cost_class": "n/a",
        "cost_class_label": "already built in this repository",
        "cost_evidence": ["capabilities.py:238-243, :333-337, :359-360 register it."],
    },
    {
        "id": "C2",
        "kind": "CONTROL -- must come out the OTHER way, scored off an EXTERNAL paper",
        "name": (
            "Validated TIME integration of a semilinear PARABOLIC PDE on a compact time "
            "interval (Fisher, Swift-Hohenberg, Ohta-Kawasaki, Kuramoto-Sivashinsky)."
        ),
        "why_this_object": (
            "This control directly CONTRADICTS the naive form of this leg's own thesis. If "
            "the thesis were 'NK cannot reach time-dependent objects', this row refutes it. "
            "It is scored off an external result, so it could not have come out the "
            "author's way by construction."
        ),
        "nk_reaches": True,
        "nk_realizations_the_negative_holds_in": [],
        "nk_reason": (
            "van den Berg, Breden & Sheombarsing, arXiv:2305.08221, 'Validated integration "
            "of semilinear parabolic PDEs' (2023): Fourier-space variation-of-constants, "
            "Chebyshev in time, domain decomposition, NEWTON-KANTOROVICH. NK does time."
        ),
        "tm_reaches": False,
        "reaching_mechanism": (
            "Not the natural tool: the object is infinite-dimensional and parabolic, and "
            "the NK space-time formulation is the state of the art for it. Taylor models "
            "lose this row too."
        ),
        "cost_class": "n/a",
        "cost_class_label": "external, already done by others",
        "cost_evidence": ["arXiv:2305.08221, published method."],
    },
]


def _check_matrix_is_not_a_tautology(rows):
    """Lesson 90: assert the controls actually come out the other way.

    If this assertion ever fails, the matrix has become a restatement of the author's
    intent and the leg's YES is void. It is wired to the SAME field the headline reads,
    so it cannot pass vacuously.
    """
    tm_wins = [r["id"] for r in rows if r["tm_reaches"] and not r["nk_reaches"]]
    nk_wins = [r["id"] for r in rows if r["nk_reaches"] and not r["tm_reaches"]]
    neither = [r["id"] for r in rows if not r["nk_reaches"] and not r["tm_reaches"]]
    assert tm_wins, "no TM-only row: the gate cannot answer yes"
    assert nk_wins, "TAUTOLOGY: no row comes out the other way; the matrix is not evidence"
    assert neither, "no honest 'neither' row: the YES is being over-read"
    return {"tm_only": tm_wins, "nk_only": nk_wins, "neither": neither}


def make_figure(summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 130, "font.size": 9})
    fig, (axr, axm) = plt.subplots(1, 2, figsize=(12.2, 4.3),
                                   gridspec_kw={"width_ratios": [1.0, 1.25]})

    # ---- Panel A: the r-axis at gamma = 7/5 -----------------------------------
    lo, hi = R_DOMINANCE_LO, R_DOMINANCE_LO + W_AVAILABLE
    axr.add_patch(plt.Rectangle((R_DOMINANCE_LO, 0.55), W_AVAILABLE, 0.40,
                                color="#d9d9d9", zorder=1))
    axr.add_patch(plt.Rectangle((R_DOMINANCE_LO, 0.55),
                                W_CERTIFIED, 0.40, color="#2b6cb0", zorder=3))
    axr.set_xlim(lo - 0.012, hi + 0.012)
    axr.set_ylim(0.0, 1.45)
    axr.annotate(f"certified by BCG's\ndominance argument\n{W_CERTIFIED:.7f}",
                 xy=(R_DOMINANCE_LO + W_CERTIFIED / 2, 0.95),
                 xytext=(R_DOMINANCE_LO + 0.030, 1.30),
                 arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.2),
                 ha="left", va="top", fontsize=8.5, color="#2b6cb0",
                 fontweight="bold")
    axr.text(R_DOMINANCE_LO + W_AVAILABLE * 0.66, 0.75,
             f"available to the target: {W_AVAILABLE:.7f}",
             ha="center", va="center", fontsize=8.5, color="#444444")
    axr.annotate("", xy=(hi, 0.35), xytext=(R_DOMINANCE_HI, 0.35),
                 arrowprops=dict(arrowstyle="->", color="#c05621", lw=1.8))
    axr.text((R_DOMINANCE_HI + hi) / 2, 0.24,
             "O1 certifies INTO here\n(r beyond 1.1909830)",
             ha="center", va="top", fontsize=8.5, color="#c05621")
    for xv in (R_DOMINANCE_LO, R_DOMINANCE_HI):
        axr.axvline(xv, color="#333333", lw=0.9, ls="--", zorder=4)
    axr.text(R_DOMINANCE_LO, 0.50, "7/6\n1.1666667", ha="center", va="top",
             fontsize=7.5, color="#333333")
    axr.text(R_DOMINANCE_HI, 0.06, "1.1909830", ha="center", va="bottom",
             fontsize=7.5, color="#333333")
    axr.set_yticks([])
    axr.set_xlabel("similarity exponent  r     (gamma = 7/5)")
    axr.set_title(f"A. BCG dominance window: shortfall {WIDTH_RATIO:.4f}x\n"
                  f"= {WIDTH_RATIO_CLOSED_FORM}   (leg 300's exact closed form)",
                  fontsize=9.5)

    # ---- Panel B: the reach matrix -------------------------------------------
    rows = MATRIX[::-1]
    ylab, nk, tm, cols = [], [], [], []
    for r in rows:
        ylab.append(f"{r['id']}  {'[CONTROL]' if r['kind'].startswith('CONTROL') else ''}")
        nk.append(r["nk_reaches"])
        tm.append(r["tm_reaches"])
        cols.append("#c05621" if r["kind"].startswith("CONTROL") else "#2b6cb0")
    y = range(len(rows))
    for i, (a, b) in enumerate(zip(nk, tm)):
        for j, v in enumerate((a, b)):
            axm.add_patch(plt.Rectangle((j - 0.42, i - 0.42), 0.84, 0.84,
                                        color="#2f855a" if v else "#e2e8f0", zorder=2))
            axm.text(j, i, "REACHES" if v else "does not", ha="center", va="center",
                     fontsize=8, color="white" if v else "#4a5568",
                     fontweight="bold" if v else "normal", zorder=3)
    axm.set_xlim(-0.6, 1.6)
    axm.set_ylim(-0.6, len(rows) - 0.4)
    axm.set_xticks([0, 1])
    axm.set_xticklabels(["radii-polynomial / NK\n(as this repo realizes it)",
                         "Taylor-model arithmetic\n/ validated integration"], fontsize=8.5)
    axm.set_yticks(list(y))
    axm.set_yticklabels(ylab, fontsize=8.5)
    for tick, c in zip(axm.get_yticklabels(), cols):
        tick.set_color(c)
    axm.set_title("B. Reach matrix. The two CONTROLS come out the OTHER way\n"
                  "(C2 is scored off arXiv:2305.08221, which refutes the naive thesis)",
                  fontsize=9.5)
    axm.invert_yaxis()

    fig.suptitle("fig79 — Leg 315 / Route-TMS: what Taylor-model arithmetic reaches "
                 "that this repo's NK apparatus does not.  SCOPING ONLY: nothing built, "
                 "no link of L1→L4 moved, Clay odds ~0.05% unchanged.", fontsize=9.0)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out = FIGS / "fig79_route_tms_v1_reach.png"
    fig.savefig(out, bbox_inches="tight")
    return out.name


def main():
    summary = _check_matrix_is_not_a_tautology(MATRIX)

    # The gate, in its PRE-COMMITTED, IMMUTABLE wording (DIRECTION.md:13848-13851).
    gate_question = (
        "Does the scoping name at least one concrete object currently unreachable by the "
        "radii-polynomial/NK apparatus that Taylor-model arithmetic reaches, with the "
        "reaching mechanism stated and its build cost classed?"
    )
    named = [r for r in MATRIX if r["tm_reaches"] and not r["nk_reaches"]]
    gate_answer = "yes" if named else "no"

    data = {
        "leg": 315,
        "route": "TMS",
        "role": "scoping only -- NOTHING IS BUILT",
        "branch": "leg/315-tms-v1",
        "gate_question": gate_question,
        "gate_answer": gate_answer,
        "gate_answer_wording": (
            "YES. The scoping names two concrete objects currently unreachable by the "
            "radii-polynomial/NK apparatus as this repository realizes it (O1, O2), each "
            "with its reaching mechanism named and its build cost classed against evidence. "
            "The headline object is O1, the sonic-crossing r-tube for BCG's autonomous "
            "(W,Z) system at gamma = 7/5; its reaching mechanism is sonic-point-"
            "desingularized Taylor-model stepping in the similarity parameter; its build "
            "cost class is C -- a genuine research problem with a Class-B implementable "
            "core -- because the integrator is a hand-roll of leg 256's kind but the "
            "Galerkin-plus-tail bridge to the non-autonomous PDE stability step has no "
            "known form for a quasilinear HYPERBOLIC system, Zgliczynski's self-consistent "
            "a-priori bounds being dissipative."
        ),
        "target": {
            "gamma": GAMMA,
            "source": "BCG, arXiv:2208.09445, Forum of Math Pi 13 (2025) e6",
            "dominance_window_lo": R_DOMINANCE_LO,
            "dominance_window_hi": R_DOMINANCE_HI,
            "width_certified": W_CERTIFIED,
            "width_available": W_AVAILABLE,
            "width_ratio_shortfall": WIDTH_RATIO,
            "width_ratio_closed_form": WIDTH_RATIO_CLOSED_FORM,
            "numbers_provenance": (
                "REPO-INTERNAL, carried forward and NOT re-derived by this leg: leg 266, "
                "corrected by leg 300 (experiments/journal/leg_300.md:40-51), propagated "
                "repo-wide by leg 319 (P0TCR). Leg 266's '6.855' was a slipped digit."
            ),
            "verifier_finding": (
                "The gap is NOT a profile enclosure. writeup/novelty/verify_251.md sec C: "
                "at BCG's scaling there is no self-similar profile system of the "
                "dissipative equation; the (W,Z) reduction is the EULER system; dissipation "
                "enters the dynamically rescaled system as the non-autonomous, "
                "exponentially decaying forcing F_dis (e^{-delta_dis s_0} prefactors). The "
                "gap is in the STABILITY step -- the r-restriction that lets the profile "
                "dominate F_dis -- re-posed as a rigorous enclosure of that step with the "
                "dissipative forcing RETAINED, at a similarity exponent outside BCG's "
                "dominance regime."
            ),
        },
        "reach_matrix": MATRIX,
        "matrix_control_summary": summary,
        "figure": "fig79_route_tms_v1_reach.png",
        "figure_number": 79,
        "capabilities_grep": {
            "ban": "building a solver without grepping capabilities.py for the object first",
            "terms": ["Taylor model", "validated integration", "rigorous integration",
                      "interval ODE", "CAPD", "Lohner", "COSY", "VNODE", "flow map",
                      "wrapping"],
            "hits": 1,
            "hit_detail": ("capabilities.py:98 'exact-Taylor inner integrals' -- an exact "
                           "Taylor expansion inside Xu's resolvent, UNRELATED to "
                           "Taylor-MODEL arithmetic. Every other term: zero."),
            "registered_neighbour": ("capabilities.py:206-207 solver/interval.py, 'rigorous "
                                     "interval arithmetic ... hand-rolled outward-rounded "
                                     "intervals; no scipy, no mpmath' -- SCALAR arithmetic, "
                                     "no integrator."),
            "in_repo_corroboration": ("experiments/p2_route_p2s_v1_spec.py:493 verbatim: "
                                      "existing=\"solver/interval.py supplies the arithmetic "
                                      "but no validated integrator\""),
        },
        "instrument_controls": {
            "positive": "arXiv:2505.03091 (Cadiot) fetched, matches in-repo record -- PASS",
            "negative": "arxiv.org/a/does_not_exist -> HTTP 404 -- PASS",
            "variant": ("'Navier--Stokes' (LaTeX double hyphen) + computer-assisted interval "
                        "arithmetic returned exactly this repo's own recorded negative "
                        "control, arXiv:2604.09949 -- PASS"),
            "broken_and_discarded": (
                "arXiv search UI returns ZERO for ANY two quoted phrases ANDed "
                "(\"Taylor models\" alone = 84 results; \"validated integration\" alone = 20; "
                "any two-phrase conjunction = 0). Six all-zero queries treated as a broken "
                "instrument and DISCARDED, not banked. pypi.org/search likewise blocked by a "
                "Client Challenge page and discarded; project pages used instead."
            ),
        },
        "bans": {
            "lifted": [],
            "walked": "writeup/novelty/leg_315.md sec 0 -- term by term, 13 rows",
            "adjacent_ban_note": (
                "The re-posed radii-polynomial ban does NOT bite: its subject is "
                "radii-polynomial machinery in a FUNCTION SPACE, and a Taylor-model flow "
                "enclosure proposes NO function space, so it is not the 'fourth space/basis' "
                "the lift clause contemplates. Recorded as disjoint subject matter and "
                "ROUTED TO THE USER, not decided here. No ban is lifted by this leg."
            ),
        },
        "policy_note_NOT_actioned_in_leg": (
            "requirements.txt is NOT edited by this leg, by explicit instruction. Its line "
            "'scipy is intentionally NOT required (no adaptive ODE integrators are used)' is "
            "confirmed a POLICY, not a finding. On this leg's evidence the policy is ALSO "
            "not the binding constraint: the tooling that would matter (python-flint/Arb) is "
            "not scipy, and the Taylor-model IVP integrators are not Python at all. Routed "
            "as an integration note in experiments/journal/leg_315.md."
        ),
        "clay": {
            "odds": "~0.05%",
            "chain_links_moved": 0,
            "statement": ("Naming a reachable object is NOT reaching it. No link of the "
                          "L1->L4 chain moved. Walls 1 and 2 stand."),
        },
    }

    fig_name = make_figure(summary)
    data["figure"] = fig_name

    DEST.parent.mkdir(parents=True, exist_ok=True)
    with open(DEST, "w") as fh:
        json.dump(data, fh, indent=1, sort_keys=False)
        fh.write("\n")

    print("LEG 315 -- ROUTE-TMS (SCOPING ONLY; NOTHING BUILT)")
    print(f"  gamma = {GAMMA}; dominance window "
          f"({R_DOMINANCE_LO}, {R_DOMINANCE_HI}), width {W_CERTIFIED}")
    print(f"  available {W_AVAILABLE}; shortfall {WIDTH_RATIO:.10f}x "
          f"= {WIDTH_RATIO_CLOSED_FORM}")
    print(f"  matrix: TM-only {summary['tm_only']}, NK-only {summary['nk_only']} "
          f"(controls, come out the OTHER way), neither {summary['neither']}")
    for r in MATRIX:
        if r["tm_reaches"] and not r["nk_reaches"]:
            print(f"  {r['id']}: cost class {r['cost_class']} -- {r['cost_class_label']}")
    print(f"  figure: {fig_name}")
    print(f"  wrote:  {DEST.relative_to(ROOT)}")
    print(f"  GATE:   {data['gate_answer'].upper()}")
    print("  CLAY:   ~0.05%, unchanged. No link of L1->L4 moved.")


if __name__ == "__main__":
    main()
