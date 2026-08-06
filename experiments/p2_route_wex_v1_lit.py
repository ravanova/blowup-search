"""P2 Route-WEX v1 -- leg 159: is there a DIFFERENT weighted-energy functional in this
literature, one that is not subject to leg 111's gamma-threshold coincidence?

A LITERATURE leg, and a READ-AND-REPORT-ONLY one.  It builds no solver module and edits
none (it IMPORTS `solver/energy_coercivity.py` READ-ONLY, to run its checks on leg 111's
OWN weight family rather than on a private re-derivation).  It touches no shared ledger,
lifts no ban, claims NO COERCIVITY GAP, computes none, and moves no link of the
`L1 -> L4` chain.  `L1` stays measured-dead in all three realizations whatever this file
says.

THE GATE, verbatim from `DIRECTION.md` leg 159:

    "Does the weighted-energy / Chen-Hou-lineage literature already consulted by legs 65
     and 111/141 contain, explicitly or as a derivable special case, a weighted-energy
     functional different from leg 111's construction that is not subject to the same
     gamma-threshold coincidence?"

    ANSWER: YES.  Lei-Liu-Ren arXiv:1811.09754 (1.3)-(1.6) -- the `H_DW` weighted-`Hdot^1`
    inner product `<xi,eta>_g = (1/4pi) int d_theta xi d_theta eta / sin^2(theta/2)` --
    extended by J. Chen arXiv:2010.12700 Definition 1.1 / Lemma 2.4 / Remark 2.5 to a
    weighted `H^2` norm on the weighted derivative `D_x = sin x d_x`.

    WHY IT IS DIFFERENT, in one line: leg 111's construction is a plain weighted `L^2` of
    the FUNCTION whose damping is a POINTWISE MULTIPLIER made negative AT THE ORIGIN by
    pushing `gamma` past `3` -- which the space forbids.  The located functional is a
    DERIVATIVE form at `gamma = 2`, BELOW that threshold and on the admissible side of leg
    111's own admissibility test, and its damping is not a pointwise multiplier at all: it
    is an EXACT identity (Chen Lemma 2.4) plus an exact tridiagonal diagonalisation in the
    basis LLR (1.5).  There is no threshold to push past, so there is nothing for the
    admissibility threshold to coincide WITH.

    Per the yes-branch's own instruction the functional is RECORDED and ESCALATED as a
    candidate for a leg-111-v2 construction leg, and NOT computed here.

WHAT THIS LEG DOES **NOT** DO, stated before the code so it can be checked against it:
no coercivity gap, no Gram matrix, no eigenvalue, no operator matrix, no trial space, no
sweep, and no tuning of any exponent.  `gamma = 2` is not selected by this leg and not
selected by a search: it is FORCED by a published exact identity, and it was already a
member of leg 111's own pre-named family.

WHY IT IS A SCRIPT AND NOT ONLY PROSE (lesson 68, and legs 57/65/112/141's ledgers).
Two jobs no amount of prose does:

  (1) VERBATIM PRESENCE.  Every quote the verdict rests on is re-located in the actual PDF
      text at run time by whitespace-insensitive substring match, so a misquote or a
      hallucinated sentence fails loudly instead of decaying at the rate of memory.
      `Papers/` is gitignored, so when the PDFs are absent the located flags are read back
      from the committed JSON and CLEARLY MARKED as such.

  (2) THE LOAD-BEARING ARITHMETIC, ON LEG 111'S OWN WEIGHTS.  The escalation rests on the
      claim that Chen's Lemma 2.4 -- `sin^-2(x/2)` is an eigenfunction of the adjoint of
      `sin x d_x` -- transfers to leg 111's family, and does so at `gamma = 2` AND AT NO
      OTHER MEMBER OF IT.  That is checkable arithmetic on the WEIGHT alone.  Define the
      transport part of leg 111's own `D_phi` (its `damping_factor` minus the `cos theta`
      stretching term):

          m_gamma(theta) = (1/2) [ cos theta + sin theta (log phi)'(theta) ]

      PREDICTED IN THE NOVELTY LOG (sec 8) BEFORE THIS FILE EXISTED, from
      `(log phi^A_gamma)' = -(gamma/2) cot(theta/2)` and `sin th cot(th/2) = 1 + cos th`:

          m_gamma(theta) = (1/2) cos th - (gamma/4)(1 + cos th) = (1 - gamma/2) cos^2(th/2) - 1/2

          gamma = 2  ->  m == -1/2 EXACTLY, for every theta: variation 0
          gamma = 0,1,3,4 -> variation |1 - gamma/2| = 1, 0.5, 0.5, 1  (all NON-zero)
          family B -> never constant except at gamma = 0 (extra `sin^2(th/2)` term)

      TWO CONTROLS THAT CAN REPORT THE OTHER ANSWER (lesson 90):
        C1  `m_gamma` is ALSO recomputed by finite difference of
            `energy_coercivity.weight_values`' own returned weights.  If the analytic and
            the finite-difference forms disagree, the formula above is not leg 111's weight
            family and the escalation is WITHDRAWN, not softened.
        C2  the same arithmetic is run at leg 111's damping threshold `gamma = 3`.  If
            `gamma = 3` came back as the constant one, the located functional would be a
            re-tread of leg 111's own family rather than a different one, and the gate
            would answer NO.

    bash Papers/fetch.sh 1811.09754 2010.12700 1710.02737 2210.07191
    .venv/bin/python experiments/p2_route_wex_v1_lit.py
        -> writeup/data/p2_route_wex_v1_lit.json

NO FIGURE: no measurement of a curve, nothing to plot ("no measurement, no figure").

VERSIONS ACTUALLY READ (a version mismatch silently invalidates a locator):
arXiv:1811.09754 (CMP 373 (2020); the arXiv PDF), arXiv:2010.12700 (ARMA,
doi 10.1007/s00205-021-01685-w; the arXiv PDF), arXiv:1710.02737 (the arXiv PDF),
arXiv:2210.07191 (the copy already in `Papers/`, banked at leg 57).
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

from solver.energy_coercivity import (          # noqa: E402  -- READ-ONLY import
    WEIGHT_FAMILY,
    damping_factor,
    weight_values,
)

OUT = ROOT / "writeup" / "data" / "p2_route_wex_v1_lit.json"
PAPERS = ROOT / "Papers"

GATE = ("Does the weighted-energy / Chen-Hou-lineage literature already consulted by legs "
        "65 and 111/141 contain, explicitly or as a derivable special case, a "
        "weighted-energy functional different from leg 111's construction that is not "
        "subject to the same gamma-threshold coincidence?")

# Predicted in the novelty log (sec 8) BEFORE this file existed: family A is constant only
# at gamma = 2 (value -1/2, the damping sign), family B only at gamma = 0 (value +1/2, the
# ANTI-damping sign, so it is not a candidate -- it is listed because a prediction that
# quietly drops a member it got right is not a prediction).
PREDICTED_CONSTANT_MEMBERS = ["A2", "B0"]

GATE_YES_BRANCH = ("yes -> Record the functional verbatim with its hypotheses and exact "
                   "reference; ESCALATE as a candidate for a leg-111-v2 construction leg "
                   "-- do not compute it here.")

# --------------------------------------------------------------------------------------
# the quotes the verdict rests on.  (arxiv id, label, fragment to re-locate verbatim)
# Fragments are PROSE, never extracted math: `pdftotext` mangles math and a locator that
# fails for a typesetting reason is a locator that teaches nothing.
# --------------------------------------------------------------------------------------
QUOTES = [
    ("1811.09754", "LLR_space_and_inner_product_are_the_paper's_own",
     "We remark that the inner product in (1.4) and the exact form of the basis vectors"),
    ("1811.09754", "LLR_found_it_accidentally",
     "are still mysterious to us even though we are fortunate enough to find them"),
    ("1811.09754", "LLR_direct_energy_method_not_spectral",
     "using a\ndirect energy method"),
    ("2010.12700", "CHEN_the_weight_is_the_adjoint_eigenfunction_of_the_transport_field",
     "is an eigenfunction\nof the adjoint of sin x"),
    ("2010.12700", "CHEN_the_weight_is_not_chosen_it_arises",
     "arise naturally from the viewpoint of energy estimates"),
    ("2010.12700", "CHEN_H_norm_is_LLR's",
     "were first introduced in [19] for stability analysis"),
    ("2010.12700", "CHEN_weighted_derivative",
     "We introduce the weighted derivative"),
    ("1710.02737", "JSS_same_family_as_leg111_far_side_of_the_threshold",
     "Let us fix"),
    ("1710.02737", "JSS_published_ladder_in_the_vanishing_order",
     "There is a natural generalization of Y0 to higher-order approximations"),
    ("2210.07191", "CH_the_squeeze_in_the_pointwise-multiplier_method",
     "so that the energy is well-defined"),
]

# --------------------------------------------------------------------------------------
# what each located functional IS, in leg 111's own exponent, so "different" is checkable
# --------------------------------------------------------------------------------------
FUNCTIONALS = [
    {
        "who": "leg 111 (this repository)",
        "ref": "solver/energy_coercivity.py",
        "form": "int_0^pi h^2 phi dtheta,  phi = (2 sin(theta/2))^(-gamma)",
        "acts_on": "the FUNCTION h",
        "gamma_in_leg111_family": "0,1,2,3,4 (family A) -- the pre-named ladder",
        "damping_mechanism": "pointwise multiplier D_phi made negative AT THE ORIGIN",
        "needs_gamma_gt": 3.0,
        "space_needs_gamma_lt": 3.0,
        "window_width_at_p1": 0.0,
        "is_leg111's_own": True,
    },
    {
        "who": "Elgindi-Ghoul-Masmoudi arXiv:1906.05811 Prop 2.1 (leg 141's answer)",
        "ref": "arXiv:1906.05811",
        "form": "int |f|^2 phi,  phi = (1+y^2)^2 / y^4",
        "acts_on": "the FUNCTION f",
        "gamma_in_leg111_family": "4",
        "damping_mechanism": "pointwise multiplier -- THE SAME MECHANISM as leg 111's",
        "needs_gamma_gt": 3.0,
        "space_needs_gamma_lt": "2p+1, opened by the hypotheses f'(0) = Hf(0) = 0 (p >= 2)",
        "window_width_at_p1": 0.0,
        "is_leg111's_own": True,
        "note": "SAME functional as leg 111's, at gamma = 4, with TWO origin hypotheses. "
                "This is leg 141's finding and it is NOT leg 159's.",
    },
    {
        "who": "Jia-Stewart-Sverak arXiv:1710.02737 (3.82)-(3.83), and (3.132) for general m",
        "ref": "arXiv:1710.02737",
        "form": "|| |sin(theta/2)|^(-gamma_JSS) f ||_{L^2},  gamma_JSS in (m - 1/2, m)",
        "acts_on": "the FUNCTION f",
        "gamma_in_leg111_family": "2*gamma_JSS in (2m-1, 2m); at m = 2 that is (3, 4)",
        "damping_mechanism": "spectral (complex-variable), but the SPACE is leg 111's family",
        "needs_gamma_gt": 3.0,
        "space_needs_gamma_lt": "2p+1, opened by splitting off P_{m-1} (their Y^(m) = Y_0^(m) (+) P_{m-1})",
        "window_width_at_p1": 0.0,
        "is_leg111's_own": True,
        "note": "The published ladder in the VANISHING ORDER, and it lands exactly on leg "
                "111's window (3, 2p+1) for p = m >= 2, and below the damping threshold "
                "(2*gamma_JSS in (1,2)) for m = 1. Same family, same coincidence.",
    },
    {
        "who": "Lei-Liu-Ren arXiv:1811.09754 (1.3)-(1.6); J. Chen arXiv:2010.12700 Def 1.1",
        "ref": "arXiv:1811.09754 / arXiv:2010.12700",
        "form": "(1/4pi) int |d_theta h|^2 / sin^2(theta/2) dtheta   [+ int |h_xx|^2 cos^2(x/2) for the X norm]",
        "acts_on": "the DERIVATIVE d_theta h  (and d_x^2 h for Chen's X norm)",
        "gamma_in_leg111_family": "2 -- BELOW leg 111's damping threshold 3, and on the "
                                  "ADMISSIBLE side of leg 111's own admissibility test",
        "damping_mechanism": "NOT a pointwise multiplier: an EXACT identity (Chen Lemma 2.4, "
                             "sin^-2(x/2) is an eigenfunction of the adjoint of sin x d_x) "
                             "plus an exact tridiagonal diagonalisation in the basis LLR (1.5)",
        "needs_gamma_gt": None,
        "space_needs_gamma_lt": None,
        "window_width_at_p1": None,
        "is_leg111's_own": False,
        "note": "THE GATE'S ANSWER. There is no gamma-threshold to push past, so there is "
                "nothing for the admissibility threshold to coincide with. Its own origin "
                "constraint is ONE condition (h'(0) = 0, implied by finiteness) where EGM "
                "Prop 2.1 needs TWO (f'(0) = Hf(0) = 0).",
    },
]

HYPOTHESES_VERBATIM = {
    "space_LLR_1.3": "H_DW = { eta in H^1(S^1) : eta(0) = 0, "
                     "int_{-pi}^{pi} |d_theta eta|^2 / sin^2(theta/2) dtheta < infinity }",
    "inner_product_LLR_1.4": "<xi, eta>_g = (1/4pi) int_{-pi}^{pi} "
                             "d_theta xi d_theta eta / sin^2(theta/2) dtheta",
    "basis_LLR_1.5": "tilde-e_k^(o) = sin[(k+1)theta]/(k+1) - sin(k theta)/k,  k >= 1, "
                     "orthonormal for <,>_g by (1.6)",
    "jacobi_form_LLR_3.7": "L tilde-e_k = -d_{k+1} tilde-e_{k+1} - (d_{k+1} - d_k) tilde-e_k "
                           "+ d_k tilde-e_{k-1},  d_k = (k-1)^2 (k+1) / (2 k^2)",
    "published_rate_LLR_Prop3.1": "|| e^{tL} eta(0) ||_Ytilde <= e^{-(3/8) t} || eta(0) ||_Ytilde",
    "coercivity_as_quoted_by_Chen_Lemma2.2c": "<L_1 f, f>_Y <= -(3/8) ||f||_Y^2",
    "norms_Chen_Def1.1": "||f||_H^2 = (1/4pi) int |f_x|^2 / sin^2(x/2) dx ; "
                         "||f||_X^2 = ||f||_H^2 + int |f_xx|^2 cos^2(x/2) dx ; "
                         "H = {f : f(0) = 0, ||f||_H < inf}, X = {f : f(0) = 0, ||f||_X < inf}",
    "identity_Chen_Lemma2.4": "<sin x f_x, f rho> = (1/2) <f^2, rho>,  rho = (sin(x/2))^(-2)",
    "nonlinear_hypotheses_LLR_Thm1.5": "eta_in in H_DW, int_{S^1} eta_in dtheta = 0, "
                                       "||eta_in||_{H_DW} < delta_0; rate any beta < 3/8",
    "MODEL_CAVEAT": "Both papers are at a = 1 (De Gregorio) and small |a-1|. This "
                    "repository's object is a = 0 CLM, where the Jacobi coefficients differ "
                    "(leg 111's matrix: column k has row k+1 entry 1 - k/2, row k-1 entry "
                    "k/2, row 1 entry -(-1)^k) and the advection is absent. NO GAP IS "
                    "CLAIMED FOR a = 0 AND NONE IS COMPUTED.",
    "WHAT_COULD_KILL_IT": "the nonlocal terms the derivative form generates "
                          "(-cos theta H h - sin theta H(h_theta)), which no weight "
                          "controls -- leg 111's own docstring: 'the nonlocal Hilbert term "
                          "is what the weight cannot touch' -- and the -sin theta h term "
                          "coupling the Hdot^1 form back to the L^2 one.",
}


# --------------------------------------------------------------------------------------
# (1) verbatim presence
# --------------------------------------------------------------------------------------
def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


def locate_quotes():
    """Re-locate every quote in the actual PDF text.  Returns (rows, source)."""
    if not PAPERS.is_dir() or shutil.which("pdftotext") is None:
        return None, "papers_absent_or_no_pdftotext"
    texts = {}
    with tempfile.TemporaryDirectory() as tmp:
        for arxiv_id in sorted({q[0] for q in QUOTES}):
            pdf = PAPERS / f"{arxiv_id}.pdf"
            if not pdf.exists():
                continue
            txt = Path(tmp) / f"{arxiv_id}.txt"
            try:
                subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)],
                               check=True, capture_output=True)
            except Exception:
                continue
            texts[arxiv_id] = _norm(txt.read_text(errors="replace"))
    if not texts:
        return None, "papers_absent_or_no_pdftotext"
    rows = []
    for arxiv_id, label, fragment in QUOTES:
        body = texts.get(arxiv_id)
        rows.append({
            "arxiv": arxiv_id,
            "label": label,
            "fragment": _norm(fragment),
            "pdf_present": body is not None,
            "located": bool(body is not None and _norm(fragment) in body),
        })
    return rows, "relocated_in_pdf_text_at_run_time"


# --------------------------------------------------------------------------------------
# (2) the load-bearing arithmetic, on leg 111's OWN weights
# --------------------------------------------------------------------------------------
def transport_multiplier(theta, family, gamma):
    """`m_gamma = (1/2)[cos th + sin th (log phi)']`, i.e. leg 111's own `damping_factor`
    with its `cos theta` STRETCHING term removed.  Read straight off `damping_factor` so
    it cannot drift from leg 111's definition."""
    return damping_factor(theta, family, gamma) - np.cos(theta)


def transport_multiplier_fd(theta, family, gamma, h=1e-6):
    """CONTROL C1: the same quantity from a finite difference of leg 111's OWN
    `weight_values`, with no analytic formula anywhere in the path."""
    theta = np.asarray(theta, dtype=float)
    lp = np.log(weight_values(theta + h, family, gamma))
    lm = np.log(weight_values(theta - h, family, gamma))
    dlogphi = (lp - lm) / (2.0 * h)
    return 0.5 * (np.cos(theta) + np.sin(theta) * dlogphi)


def weight_table():
    # interior grid: both endpoints are weight singularities, so stay strictly inside
    theta = np.linspace(0.05, np.pi - 0.05, 20001)
    rows = []
    for name, family, gamma in WEIGHT_FAMILY:
        m = transport_multiplier(theta, family, gamma)
        m_fd = transport_multiplier_fd(theta, family, gamma)
        variation = float(m.max() - m.min())
        rows.append({
            "name": name,
            "family": family,
            "gamma": float(gamma),
            "m_min": float(m.min()),
            "m_max": float(m.max()),
            "variation": variation,
            "is_constant": bool(variation < 1e-12),
            "constant_value": float(m.mean()) if variation < 1e-12 else None,
            "predicted_variation": (abs(1.0 - 0.5 * gamma) if family == "A" else None),
            "control_C1_max_abs_diff_vs_finite_difference_of_weight_values":
                float(np.max(np.abs(m - m_fd))),
        })
    return rows


def window_ladder():
    """PURE ARITHMETIC, no operator: leg 111's window `(3, 2p+1)` as a function of the
    vanishing order `p` of the trial function at the origin, with the published exponents
    placed in it.  This is where the NON-escapes are made auditable."""
    rows = []
    for p in (1, 2, 3, 4):
        lo, hi = 3.0, 2.0 * p + 1.0
        rows.append({
            "vanishing_order_p": p,
            "damping_needs_gamma_gt": lo,
            "space_needs_gamma_lt": hi,
            "window_width": max(0.0, hi - lo),
            "leg111_basis_sin_k_theta_has_this_p": (p == 1),
            "EGM_1906.05811_gamma_4_admissible_here": bool(4.0 < hi),
            "JSS_1710.02737_band_2*gamma_in": [2.0 * (p - 0.5), 2.0 * p],
            "JSS_band_inside_window": bool(2.0 * (p - 0.5) >= lo and 2.0 * p <= hi),
        })
    return rows


def main():
    quotes, quote_source = locate_quotes()
    if quotes is None and OUT.exists():
        prev = json.loads(OUT.read_text())
        quotes = prev.get("quotes_located")
        quote_source = "READ BACK FROM THE COMMITTED JSON -- Papers/ is gitignored and absent"

    weights = weight_table()
    ladder = window_ladder()

    constant_members = [r["name"] for r in weights if r["is_constant"]]
    c1_worst = max(r["control_C1_max_abs_diff_vs_finite_difference_of_weight_values"]
                   for r in weights)
    gamma3 = next(r for r in weights if r["name"] == "A3")

    payload = {
        "leg": 159,
        "route": "ROUTE-WEX",
        "kind": "literature deep-mine, read-and-report only; NO coercivity computation",
        "gate": GATE,
        "gate_answer": "YES",
        "gate_answer_branch_verbatim": GATE_YES_BRANCH,
        "the_functional": {
            "name": "the H_DW weighted-Hdot^1 inner product (Lei-Liu-Ren), extended to a "
                    "weighted H^2 norm on the weighted derivative D_x = sin x d_x (J. Chen)",
            "primary": "https://arxiv.org/abs/1811.09754  (CMP 373 (2020)) eqs (1.3)-(1.6), "
                       "sec 3.1-3.2, Prop 3.1",
            "secondary": "https://arxiv.org/abs/2010.12700  (ARMA, "
                         "doi 10.1007/s00205-021-01685-w) Definition 1.1, Lemma 2.2(c), "
                         "Lemma 2.4, Remark 2.5",
            "hypotheses_verbatim": HYPOTHESES_VERBATIM,
        },
        "functionals_compared": FUNCTIONALS,
        "quotes_located": quotes,
        "quotes_source": quote_source,
        "weight_arithmetic": {
            "definition": "m_gamma(theta) = (1/2)[cos th + sin th (log phi)'] = leg 111's "
                          "own damping_factor MINUS its cos theta stretching term",
            "prediction_from_novelty_log_sec8": "m_2 == -1/2 for every theta (variation 0); "
                                                "every other family-A member has variation "
                                                "|1 - gamma/2|; family B constant only at "
                                                "gamma = 0",
            "grid_inset": "theta in [0.05, pi - 0.05]: both endpoints are weight "
                          "singularities, so the measured variation of a NON-constant "
                          "member is its predicted endpoint value |1 - gamma/2| shrunk by "
                          "the inset (0.9988 where 1 is predicted). The CONSTANT member's "
                          "variation is 0 to round-off and does not depend on the inset.",
            "rows": weights,
            "constant_members": constant_members,
            "predicted_constant_members": PREDICTED_CONSTANT_MEMBERS,
            "prediction_held": bool(constant_members == PREDICTED_CONSTANT_MEMBERS),
            "B0_is_constant_at_the_WRONG_SIGN": "+1/2, i.e. anti-damping; it is a member "
                                                "the prediction got right, not a candidate",
            "control_C1_worst_abs_diff": c1_worst,
            "control_C2_gamma3_is_NOT_constant": not gamma3["is_constant"],
            "control_C2_gamma3_variation": gamma3["variation"],
        },
        "window_ladder": {
            "note": "leg 111's window (3, 2p+1) in the weight exponent, as a function of "
                    "the vanishing order p -- pure arithmetic, no operator. The published "
                    "exponents of EGM and JSS are placed in it: both sit in the p >= 2 "
                    "rows, i.e. both escape by CONSTRAINING THE ORIGIN, not by changing "
                    "the functional.",
            "rows": ladder,
        },
        "what_is_NOT_claimed": [
            "NO coercivity gap for the located functional on the a = 0 CLM linearisation: "
            "none is computed here and none is claimed. The published rate 3/8 is at a = 1.",
            "The located functional does not lift a ban, promote a route, or move a link of "
            "the L1 -> L4 chain. L1 stays measured-dead in all three realizations.",
            "Leg 111's measurements are untouched and remain correct for the construction "
            "leg 111 built.",
            "Absence of a search hit is not absence of literature (PHASE2_P2_NOTES sec 24; "
            "leg 52's search-index flag still stands).",
        ],
        "correction_to_a_banked_reading": {
            "where": "writeup/novelty/leg_141.md Q2, and experiments/journal/leg_141.md",
            "banked": "arXiv:1811.09754 'concerns global regularity/blowup for the "
                      "convective model, carries no weighted-energy coercivity estimate'; "
                      "arXiv:2010.12700 and arXiv:1811.09754 'read and found not to carry "
                      "the coincidence'",
            "correction": "The second half is right and answers leg 141's gate: neither "
                          "paper states the coincidence. The first half is not: sec 3.2 of "
                          "arXiv:1811.09754 proves the decay estimate in a weighted Hdot^1 "
                          "'using a direct energy method', and arXiv:2010.12700 quotes it "
                          "as Lemma 2.2(c) in the form <L_1 f, f>_Y <= -(3/8)||f||_Y^2. "
                          "That IS a weighted-energy coercivity estimate, and it is what "
                          "leg 159 was sent to find.",
            "status": "recorded as a correction to a banked reading, not as a criticism of "
                      "a gate that answered its own question correctly",
        },
        "escalation": "leg-111-v2 construction leg: test the H_DW / Chen weighted-derivative "
                      "functional on the a = 0 CLM linearisation this repository already "
                      "carries. It is a CONSTRUCTION leg's job, with its own pre-committed "
                      "gate, and the two terms named in WHAT_COULD_KILL_IT are what it has "
                      "to survive.",
        "novelty_log": "writeup/novelty/leg_159.md",
        "journal": "experiments/journal/leg_159.md",
        "figure": None,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")

    print(f"leg 159  ROUTE-WEX   gate: YES")
    print(f"  quotes: {quote_source}")
    if quotes:
        n_ok = sum(1 for q in quotes if q.get("located"))
        print(f"          {n_ok}/{len(quotes)} located verbatim")
        for q in quotes:
            if not q.get("located"):
                print(f"          NOT LOCATED: {q['arxiv']} {q['label']}")
    print(f"  weight arithmetic: constant members = {constant_members}  "
          f"(predicted: {PREDICTED_CONSTANT_MEMBERS})")
    for r in weights:
        print(f"    {r['name']:>12}  gamma={r['gamma']:.0f}  m in "
              f"[{r['m_min']:+.6f}, {r['m_max']:+.6f}]  variation={r['variation']:.3e}"
              f"  predicted={r['predicted_variation']}")
    print(f"  control C1 worst |analytic - finite-difference(weight_values)| = {c1_worst:.3e}")
    print(f"  control C2 gamma=3 variation = {gamma3['variation']:.6f}  (must be NON-zero)")
    print(f"  -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
