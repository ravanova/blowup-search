"""ROUTE-XS v1: THE SHAPE DICHOTOMY, AGAINST THE PUBLISHED CERTIFICATES.

--------------------------------------------------------------------------
WHY THIS MODULE EXISTS
--------------------------------------------------------------------------
Legs 51-53 built their whole explanation of Route-TC's failure on one sentence
(banked as lesson 87):

    A certification method has a SHAPE, and the shape is a property of the
    OPERATOR.  The standard radii-polynomial tail estimate closes because the
    unbounded part is a MULTIPLIER -- cut an entry of size `Lambda_M` and the tail
    inverse is `1/Lambda_M`.  Here the unbounded part is OFF-DIAGONAL (a shift) and
    the bordered tail inverse is a CONSTANT (2.19 ... 10.32), not `1/K`.

If `MM` answers NO that sentence becomes the lane's epitaph.  **An epitaph with no
external check is a mood, not a finding.**  So this module does two things that prose
cannot:

1.  It classifies the actual published computer-assisted certificates this repository
    can cite, each classification traced to a **located statement in the full text** --
    section, and the sentence itself, quoted.  Not an abstract page: leg 53 lost a claim
    by citing an abstract, and the correction is banked as a ban.
2.  It makes the dichotomy **executable and continuous**, measured rather than asserted.
    The classification is not a label this module attaches by hand; it is read off a
    ladder computed from the operator (`classify_operator`), and the label a paper gets
    in `SHAPE_LEDGER` is one this module can be run against.

--------------------------------------------------------------------------
WHAT THE NOVELTY PASS ALREADY SETTLED, AND IT BINDS EVERYTHING BELOW
--------------------------------------------------------------------------
`writeup/novelty/leg_57.md`, verdict `PROCEED_AS_BOOKKEEPING`.  **The observation is
folklore in print and this leg does not claim it.**  Two located statements, both by
Cadiot, put both halves on paper:

  * arXiv:2505.03091 section 2: "the operator `L` becomes an infinite diagonal matrix
    `L_q` with entries `l(n/2q)` on the diagonal."
  * arXiv:2505.03091 section 3 (opening): "By construction `D` is supposed to be
    diagonally dominant, which hints to the Gershgorin theorem."

What is NOT in print is the classification as an executable ledger.  That is a
bookkeeping artifact whose only virtue is that it does not decay at the rate of memory
(lesson 68).  **It is not a result and must not be written up as one.**

--------------------------------------------------------------------------
WHAT IS VERIFIED HERE, AND WHAT IS TRANSCRIBED
--------------------------------------------------------------------------
Same discipline as `solver/literature_gates.py`, and the two are kept apart because
transcription is where errors hide.

**VERIFIED** (this module recomputes it, from `solver/spectral_certificate.py`'s
operator, and reports a magnitude):

  XS1  the decay ladder of the tail inverse as a function of the split `K`, across the
       whole continuous dial from shift to multiplier -- `tail_inverse_ladder`,
       `decay_exponent`, `classify_operator`.
  XS2  the `M`-divergence at zero diagonal: the UNBORDERED tail inverse at `mu = 0` is
       not merely large, it does not exist as `M -> infinity` (linear in `M`).  That is
       why leg 52 bordered.
  XS3  the bordered constant that replaces it, and **that it GROWS in `K` rather than
       decaying** -- the sharp form of "a constant, not `1/K`".

**TRANSCRIBED, not verified:** every entry of `SHAPE_LEDGER` -- the classifications,
the quotes and the section numbers are read off the full-text PDFs by a
human-equivalent process and are exactly as good as that.  The `url` on every record is
there so the next pass can check the quote instead of trusting it.

--------------------------------------------------------------------------
THE ONE THING THE MEASUREMENT CORRECTED, AND IT WAS THIS LEG'S OWN HYPOTHESIS
--------------------------------------------------------------------------
BDL admit a tridiagonal tail under assumption (5), `|lambda_k/mu_k|, |beta_k/mu_k| <=
delta < 1/2`.  Our operator's off-diagonal is `~ k/2` and `dissipative_control` puts
`mu*k` on the diagonal, so the SAME ratio here is `delta = 1/(2 mu)` and BDL's
threshold `delta < 1/2` is `mu > 1`.  **The obvious hypothesis was that the tail
inverse stops behaving at `mu = 1`.  It is false, and the ladder says so:** finiteness
of the tail inverse in `M` holds for EVERY `mu > 0` and fails only at `mu = 0` exactly.
`delta < 1/2` is what BDL's *LU construction* needs, not where the operator changes
character.  The dichotomy's real hinge is **zero diagonal versus nonzero diagonal**, and
`delta` is not the coordinate for it.  Recorded because a hypothesis that was checked
and died is worth more than one that was never posed.

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* Not rigorous.  Float64, no intervals.  Every number is a measurement of a matrix.
* Not a claim about `HL_S2_nonsymmetric`, or about any link of the L1->L4 chain.
* **Not a survival claim.**  Where the published record covers what we do, this module
  records that; it does not look for a way to keep a claim.
* Not a reading of Chen-Hou's energy method deep enough to port it.  It records that
  the method is NOT a radii-polynomial certificate and where they say so.  Porting it is
  a different leg and this module does not claim the port works.
"""

import numpy as np

from solver.spectral_certificate import (
    bordered_tail_inverse_norm,
    tail_inverse_norm,
)

# --------------------------------------------------------------------------
# the vocabulary -- fixed, so the ledger cannot drift into free text
# --------------------------------------------------------------------------
#: shape of the unbounded part of the linearised operator
MULTIPLIER = "MULTIPLIER"                    # diagonal in the spectral basis
TRIDIAGONAL_DOMINANT = "TRIDIAGONAL_DOMINANT"  # off-diagonal present, diagonal wins
SHIFT = "SHIFT"                              # off-diagonal, diagonal exactly zero
NO_UNBOUNDED_PART = "NO_UNBOUNDED_PART"      # the certified system is finite-dimensional

#: shape of the approximate inverse
BLOCK_DIAGONAL = "BLOCK_DIAGONAL"            # finite matrix (+) diagonal tail
NOT_BLOCK_DIAGONAL = "NOT_BLOCK_DIAGONAL"    # off-diagonal blocks are nonzero
FINITE_JACOBIAN = "FINITE_JACOBIAN"          # interval Newton on a finite system
NO_APPROXIMATE_INVERSE = "NO_APPROXIMATE_INVERSE"  # the method does not build one


# --------------------------------------------------------------------------
# the ledger -- links, not counts, and a LOCATED statement for every row
# --------------------------------------------------------------------------
# `located` is the whole point.  `where` must name a section/assumption/proposition,
# and `quote` must be the sentence that licenses the classification, verbatim from the
# FULL TEXT.  A row whose `where` says "abstract" is not admissible evidence here.
SHAPE_LEDGER = [
    {
        "tag": "CLN",
        "arxiv": "2302.12877",
        "url": "https://arxiv.org/abs/2302.12877",
        "authors": "Cadiot, Lessard, Nave",
        "title": ("Rigorous computation of solutions of semi-linear PDEs on unbounded "
                  "domains via spectral methods"),
        "is_radii_polynomial": True,
        "unbounded_part": MULTIPLIER,
        "approx_inverse": BLOCK_DIAGONAL,
        "tail_inverse_decays": True,
        "located": [
            {"where": "Assumption 2.1",
             "quote": ("Assume that the Fourier transform of the linear operator L is "
                       "given by F(Lu)(xi) = l(xi) u^(xi), for all u in S, where l is a "
                       "polynomial in xi.  Moreover, assume that |l(xi)| > 0, for all "
                       "xi in R^m."),
             "supports": "unbounded_part = MULTIPLIER, stated as a standing hypothesis"},
            {"where": "section 1 (literature review, the periodic case)",
             "quote": ("One of the main ingredients to achieve such a goal is to exploit "
                       "the fact that the Frechet derivatives are (asymptotically) "
                       "diagonally dominant. ... Therefore, the tail of DF(U0) can be seen "
                       "as a diagonally-dominant infinite dimensional matrix.  From this, "
                       "one can approximate the inverse of DF(U0) as a finite matrix "
                       "acting on a finite part of the sequence, and a tail operator "
                       "(which is diagonal) which acts on the tail of the sequence."),
             "supports": ("approx_inverse = BLOCK_DIAGONAL, and the REASON -- this is the "
                          "clearest statement in the corpus that the block-diagonal A is "
                          "downstream of the multiplier, not an independent choice")},
            {"where": "Remark 2.7",
             "quote": ("under Assumption 2.3, DG(u0) is relatively compact with respect "
                       "to L ... and using Weyl's perturbation theory, the essential "
                       "spectrum of DF(u0) = L + DG(u0) is equal to the essential spectrum "
                       "of L."),
             "supports": ("the ABSTRACT form of the dichotomy: the tail estimate is an "
                          "assertion that the rest is relatively compact w.r.t. the "
                          "unbounded part.  A transport term of the same order as the "
                          "unbounded part is not.")},
        ],
        "note": ("`solver/target_selection.py` already reproduces this paper's Kawahara "
                 "r_0 exactly (`cln_kawahara_check`); nothing here re-derives it."),
        "counterexample": False,
    },
    {
        "tag": "BDL",
        "arxiv": "1503.06315",
        "url": "https://arxiv.org/abs/1503.06315",
        "authors": "Breden, Desvillettes, Lessard",
        "title": "Rigorous numerics for nonlinear operators with tridiagonal dominant linear part",
        "is_radii_polynomial": True,
        "unbounded_part": TRIDIAGONAL_DOMINANT,
        "approx_inverse": NOT_BLOCK_DIAGONAL,
        "tail_inverse_decays": True,
        "located": [
            {"where": "assumption (4), section 2",
             "quote": ("[RECONSTRUCTED, see transcription note] for all k >= 0, "
                       "|lambda_k|/omega_k^{s_L}, |mu_k|/omega_k^{s_L}, "
                       "|beta_k|/omega_k^{s_L} <= C_2, and for all k >= k_0, "
                       "C_1 <= |mu_k|/omega_k^{s_L}"),
             "transcription": ("This assumption's fractions come through pdftotext STACKED "
                               "and out of order ('mu_k beta_k mu_k lambda_k , sL , sL <= "
                               "C2 and ... C1 <= sL'), so the line above is a "
                               "RECONSTRUCTION of the display, not a verbatim copy.  The "
                               "load-bearing clause -- a LOWER bound C_1 on the diagonal "
                               "mu_k at the growth rate s_L -- is unambiguous in the "
                               "extraction and is what the classification rests on.  "
                               "Flagged rather than smoothed over: this leg's whole point "
                               "is that a located statement can be checked, and a "
                               "reconstruction that is presented as a quotation cannot."),
             "supports": ("the DIAGONAL is bounded BELOW, at the same growth rate s_L that "
                          "makes the operator unbounded.  This is LIT's ninth-pass finding, "
                          "confirmed here at full text rather than from the abstract.")},
            {"where": "assumption (5), section 2",
             "quote": ("Assume further the existence of delta in (0, 1/2) and k_0 >= 0 such "
                       "that for all k >= k_0, |lambda_k/mu_k|, |beta_k/mu_k| <= delta."),
             "supports": ("the off-diagonals are STRICTLY SUBORDINATE to the diagonal.  "
                          "'Tridiagonal dominant' means the diagonal dominates WITHIN a "
                          "tridiagonal operator -- it is a near-multiplier, not a shift.")},
            {"where": "Proposition 2.3",
             "quote": ("Assume that m >= k_0 and delta < 1/2.  Then A maps Omega^s into "
                       "Omega^{s+s_L}."),
             "supports": ("tail_inverse_decays = True, and with the SAME gain s_L as the "
                          "pure multiplier case.  The tridiagonal structure costs nothing "
                          "in the decay rate; the diagonal lower bound buys it.")},
            {"where": "section 1 (introduction), and section 5 (conclusion)",
             "quote": ("In [3, 4, 6, 7, 9, 5], the nonlinear equations under study have "
                       "asymptotically diagonal or block-diagonal dominant linear part, "
                       "which helps a lot in the computation of approximate inverses.  In "
                       "contrast, the present work considers problems with tridiagonal "
                       "dominant linear part.  To the best of our knowledge, this is the "
                       "first attempt to compute rigorously solutions of such problems."),
             "supports": ("approx_inverse = NOT_BLOCK_DIAGONAL.  **This is the row that "
                          "matters most for MM.**  A non-block-diagonal approximate inverse "
                          "IS published -- it is an LU factorisation of the tridiagonal "
                          "tail, and A's finite block carries a nonzero coupling to the "
                          "tail (their eq. (21)).  So MM's move is not unprecedented.  What "
                          "BDL buy with it is TRIDIAGONAL, and they still need the diagonal "
                          "lower bound (4) and delta < 1/2 to get it.")},
        ],
        "note": ("Their section 5 future-work list asks to relax the SYMMETRY in (5) "
                 "('assumption (5) requires the tridiagonal operator to have symmetric "
                 "ratios between the diagonal terms and the upper and lower diagonal "
                 "terms') and to extend to block-tridiagonal structures.  **A vanishing "
                 "diagonal is not on that list.**  The zero-diagonal Fredholm case is "
                 "outside their construction, which is what the standing ban records."),
        "counterexample": False,
    },
    {
        "tag": "CH",
        "arxiv": "2210.07191 + 2305.05660",
        "url": "https://arxiv.org/abs/2210.07191",
        "authors": "Chen, Hou",
        "title": ("Stable nearly self-similar blowup of the 2D Boussinesq and 3D Euler "
                  "equations with smooth data, I: Analysis and II: Rigorous Numerics"),
        "is_radii_polynomial": False,
        "unbounded_part": SHIFT,
        "approx_inverse": NO_APPROXIMATE_INVERSE,
        "tail_inverse_decays": None,
        "located": [
            {"where": "Part I section 2.7 ('The local parts and functional spaces')",
             "quote": ("we will perform weighted energy estimate in some suitable space X "
                       "and derive the damping terms in the weighted energy estimate from "
                       "the local terms, especially the advection term (c_l x + u).grad f "
                       "in (2.30)."),
             "supports": ("**THE CENTRAL ROW OF THIS LEDGER.**  The one published "
                          "computer-assisted proof whose unbounded part IS a transport "
                          "operator does not invert it and does not estimate its tail.  It "
                          "extracts DAMPING from the advection term itself, in a weighted "
                          "energy estimate.  The shift is the source of the coercivity "
                          "rather than the obstruction to it.")},
            {"where": "Part I section 2.6 ('The advection')",
             "quote": ("The advection in (2.10) satisfies the following important "
                       "inequalities c_l x + u(x,y) >= c_1 x, c_1 ~ 0.47"),
             "supports": ("the sign condition that makes the advection a damping term.  It "
                          "is a POINTWISE inequality on the profile, not a spectral "
                          "property -- so it has no expression in an l^1-Fourier tail "
                          "estimate at all.")},
            {"where": "full text of both parts, searched",
             "quote": ("[absent] the strings 'radii polynomial', 'Newton-Kantorovich', "
                       "'approximate inverse' and 'contraction mapping' do not occur in "
                       "either Part I or Part II."),
             "supports": ("is_radii_polynomial = False.  This is a NEGATIVE located "
                          "observation and it is reported as a search over the full text, "
                          "which is checkable, rather than as an impression.")},
        ],
        "note": ("Banned as a TARGET (leg 45 M1: it is already certified).  It is admitted "
                 "here only as a classification datum.  **It is not a counterexample to "
                 "the dichotomy -- it is the strongest confirmation of it in the corpus**, "
                 "because it shows the shift case being certified by ABANDONING the tail "
                 "estimate rather than by repairing it."),
        "counterexample": False,
    },
    {
        "tag": "DF",
        "arxiv": "2410.05480",
        "url": "https://arxiv.org/abs/2410.05480",
        "authors": "Dahne, Figueras",
        "title": ("Self-similar singular solutions of the complex Ginzburg-Landau "
                  "equation, computer-assisted"),
        "is_radii_polynomial": False,
        "unbounded_part": NO_UNBOUNDED_PART,
        "approx_inverse": FINITE_JACOBIAN,
        "tail_inverse_decays": None,
        "located": [
            {"where": "section 4 ('A detailed example'), eq. (8)",
             "quote": ("By splitting gamma into real and imaginary parts, we can treat G as "
                       "a map from R^4 to R^4.  To prove the existence of a root we make "
                       "use of the so-called interval Newton method: ... "
                       "mid(X) - J_G^{-1}(X) G(mid(X)) strictly contained in X."),
             "supports": ("There is no infinite tail and no approximate inverse of an "
                          "unbounded operator.  The infinite-dimensionality is discharged "
                          "by rigorous ODE integration BEFORE the Newton step, leaving a "
                          "genuinely finite Jacobian.  So this paper is silent on the "
                          "dichotomy -- it is in the ledger to record that it is silent, "
                          "not to be counted on either side.")},
        ],
        "note": ("Re-derived at leg 48 (`solver/viscous_novelty.py`): their Tables 1/2 to "
                 "1.8e-07, their branch to 3.0e-06, their fold to 3.8e-07.  Stage V was "
                 "closed by this paper's existence.  Nothing here re-derives that."),
        "counterexample": False,
    },
    # ----------------------------------------------------------------------
    # THE CONTROL.  Lesson 90: a gate that cannot come out the other way is not a
    # gate.  This row is FICTITIOUS and is flagged as such; `gate_answer` must return
    # "yes" when it is admitted and "no" when it is not.  `test_certificate_shapes.py`
    # runs both directions.  Without it, `gate_answer` returning "no" would be a
    # property of the code rather than of the literature.
    # ----------------------------------------------------------------------
    {
        "tag": "SYNTHETIC_CONTROL",
        "arxiv": None,
        "url": None,
        "authors": "(not a paper)",
        "title": ("FICTITIOUS: a radii-polynomial certificate with an off-diagonal "
                  "unbounded part and a non-decaying tail inverse"),
        "is_radii_polynomial": True,
        "unbounded_part": SHIFT,
        "approx_inverse": BLOCK_DIAGONAL,
        "tail_inverse_decays": False,
        "located": [
            {"where": "(none -- this row is a control and cites nothing)",
             "quote": "(none)",
             "supports": ("Exists so that the gate predicate demonstrably CAN answer yes.  "
                          "Excluded from the real ledger by `is_fictitious`.")},
        ],
        "note": "CONTROL ROW.  Never counted as evidence.",
        "counterexample": True,
        "is_fictitious": True,
    },
]


def real_ledger():
    """The ledger with the control row removed -- the only thing that is evidence."""
    return [r for r in SHAPE_LEDGER if not r.get("is_fictitious", False)]


# --------------------------------------------------------------------------
# THE GATE, AS AN EXECUTABLE PREDICATE
# --------------------------------------------------------------------------
def is_counterexample(row):
    """Route-XS's gate condition, applied to one ledger row.

    The gate asks for a PUBLISHED RADII-POLYNOMIAL certificate whose unbounded part is
    OFF-DIAGONAL (a shift) and whose tail inverse does NOT decay.  All three clauses
    are required, and each one is doing work:

      * `is_radii_polynomial` -- Chen-Hou have the shift and are excluded here, because
        they never form a tail estimate.  Dropping this clause would turn a
        confirmation of the dichotomy into a refutation of it.
      * `unbounded_part == SHIFT` -- BDL have a non-block-diagonal A and are excluded
        here, because their diagonal is bounded below by assumption (4).
      * `tail_inverse_decays is False` -- a paper that has the shift AND forms a tail
        estimate AND still gets decay would be the real counterexample.  None does.
    """
    return (bool(row.get("is_radii_polynomial"))
            and row.get("unbounded_part") == SHIFT
            and row.get("tail_inverse_decays") is False)


def gate_answer(rows=None):
    """Answer Route-XS's gate from the ledger, with the evidence attached.

    Returns a dict carrying the answer AND the located statements that produced it, so
    the answer can never be quoted without its citations (which is the whole reason
    this is code and not a paragraph).
    """
    rows = real_ledger() if rows is None else rows
    hits = [r for r in rows if is_counterexample(r)]
    return {
        "gate": ("Is there a published radii-polynomial certificate whose unbounded part "
                 "is OFF-DIAGONAL (a shift) and whose tail inverse does not decay -- "
                 "i.e. a counterexample to the dichotomy legs 51-53 rest on?"),
        "answer": "yes" if hits else "no",
        "counterexamples": [r["tag"] for r in hits],
        "n_rows_examined": len(rows),
        "rows": [{"tag": r["tag"], "arxiv": r["arxiv"], "url": r["url"],
                  "is_radii_polynomial": r["is_radii_polynomial"],
                  "unbounded_part": r["unbounded_part"],
                  "approx_inverse": r["approx_inverse"],
                  "tail_inverse_decays": r["tail_inverse_decays"],
                  "n_located": len(r["located"]),
                  "located_where": [d["where"] for d in r["located"]]}
                 for r in rows],
    }


def unlocated_rows(rows=None):
    """Rows whose classification is not traced to a located full-text statement.

    Leg 53 lost a claim by citing an abstract.  This predicate is the standing guard:
    any row citing an abstract, or citing nothing, comes back here.  `test_` asserts it
    is empty over the real ledger.
    """
    rows = real_ledger() if rows is None else rows
    bad = []
    for r in rows:
        for d in r["located"]:
            w = d["where"].lower()
            if not d["where"] or "abstract" in w:
                bad.append((r["tag"], d["where"]))
        if not r["located"]:
            bad.append((r["tag"], "(no located statement at all)"))
    return bad


# --------------------------------------------------------------------------
# THE DICHOTOMY AS A MEASUREMENT, NOT A LABEL
# --------------------------------------------------------------------------
# The operator is `solver/spectral_certificate.tail_block`, i.e. the a = 0 CLM
# linearisation's far-field block: off-diagonal entries `~ k/2`, diagonal exactly zero.
# `mu` adds `mu*k` to the diagonal (`Lambda^1` dissipation, `solver/fractional_gclm.py`'s
# dial).  So `mu` is a CONTINUOUS DIAL FROM SHIFT TO MULTIPLIER:
#
#     mu = 0        diagonal exactly zero            -- SHIFT (our operator)
#     mu > 0        diagonal ~ mu*k, off-diag ~ k/2  -- the diagonal is present
#
# and BDL's ratio `delta = |off-diagonal| / |diagonal|` is `1/(2 mu)` here, so their
# admissibility `delta < 1/2` reads `mu > 1`.  **That threshold is NOT where the
# behaviour changes** -- see the module docstring.  It is kept as a marked line on the
# dial because a checked-and-dead hypothesis is worth recording.
def bdl_delta(mu):
    """BDL's off-diagonal/diagonal ratio for our operator: delta = 1/(2 mu).

    `inf` at `mu = 0`: a zero diagonal is not a small ratio, it is no ratio.
    """
    mu = float(mu)
    return float("inf") if mu == 0.0 else 1.0 / (2.0 * mu)


def bdl_admissible(mu):
    """Does our operator at dissipation `mu` satisfy BDL's assumption (5), delta < 1/2?"""
    return bdl_delta(mu) < 0.5


def tail_inverse_ladder(mu, Ks=(4, 8, 16, 32, 64, 128), M=1024, kind="flat", param=0.0,
                        bordered=False, border="analytic"):
    """||tail inverse||_w as a function of the split K -- the ladder, not its endpoint.

    `bordered=False` is the object a certificate actually uses when the tail block is
    invertible (`mu > 0`).  `bordered=True` is what leg 52 had to introduce when it is
    not (`mu = 0`, where the tail block has a kernel).

    **DO NOT border a `mu > 0` tail.**  Leg 53 already made that mistake and it is
    banked: bordering an ALREADY INVERTIBLE operator with the zero-diagonal operator's
    near-null pair is the wrong operator, not the wrong answer.  `WRONG_OPERATOR_CONTROL`
    below keeps the numbers it produces, precisely so nobody quotes them as a comparison.
    """
    f = ((lambda K: bordered_tail_inverse_norm(K, M, kind, param, border, mu=float(mu)))
         if bordered else
         (lambda K: tail_inverse_norm(K, M, kind, param, mu=float(mu))))
    return [int(K) for K in Ks], [float(f(int(K))) for K in Ks]


def decay_exponent(Ks, vals, tail=4):
    """d log ||.|| / d log K over the last `tail` rungs -- a MAGNITUDE, never a boolean.

    NEGATIVE means the tail inverse decays as the split moves out, which is what a
    radii-polynomial tail estimate needs.  POSITIVE means it grows.  The certificate
    does not care whether the number is finite; it cares about this sign and size.
    """
    Ks = np.asarray(Ks, float)
    vals = np.asarray(vals, float)
    if Ks.size < tail or np.any(vals <= 0) or not np.all(np.isfinite(vals)):
        return {"refused": True, "reason": "non-positive or non-finite rung"}
    s, _ = np.polyfit(np.log(Ks[-tail:]), np.log(vals[-tail:]), 1)
    return {"refused": False, "exponent": float(s), "n_rungs": int(tail),
            "first": float(vals[0]), "last": float(vals[-1]),
            "ratio_last_over_first": float(vals[-1] / vals[0])}


def m_divergence(mu, K=8, Ms=(128, 256, 512, 1024, 2048), bordered=False, kind="flat",
                 param=0.0, border="analytic"):
    """Does the tail inverse EXIST as M -> infinity?  Growth in M at fixed K.

    This is the question `decay_exponent` cannot see, and it is the one that separates
    `mu = 0` from every `mu > 0`: at zero diagonal the UNBORDERED tail inverse grows
    linearly in M, i.e. the tail operator is not boundedly invertible at all.  Bordering
    (leg 52) is what makes it exist; it does not make it decay (XS3).
    """
    f = ((lambda M: bordered_tail_inverse_norm(K, M, kind, param, border, mu=float(mu)))
         if bordered else
         (lambda M: tail_inverse_norm(K, M, kind, param, mu=float(mu))))
    Ms = [int(m) for m in Ms]
    vals = [float(f(m)) for m in Ms]
    s, _ = np.polyfit(np.log(Ms), np.log(vals), 1)
    return {"M": Ms, "vals": vals, "exponent_in_M": float(s),
            "ratio_last_over_first": float(vals[-1] / vals[0])}


def classify_operator(mu, Ks=(4, 8, 16, 32, 64, 128), M=1024, kind="flat", param=0.0):
    """Classify the operator at dissipation `mu` BY MEASURING IT, not by asserting.

    This is the executable half of `SHAPE_LEDGER`: the labels in that table are the
    labels this function returns when the corresponding operator is fed to it.  The
    rule it applies is the one the certificate actually needs:

      * if the tail block is boundedly invertible (no `M`-divergence), use the
        UNBORDERED inverse and report its `K`-exponent;
      * if it is not, the certificate must border (leg 52), and the honest object is
        the BORDERED inverse -- whose `K`-exponent is then reported instead.

    `tail_inverse_decays` is `exponent < 0`, and the exponent is returned alongside it
    so the verdict is never quoted without its magnitude.
    """
    mu = float(mu)
    md = m_divergence(mu, K=int(Ks[0]) * 2, bordered=False, kind=kind, param=param)
    invertible = md["exponent_in_M"] < 0.25          # flat in M, vs linear growth
    Ks_, vals = tail_inverse_ladder(mu, Ks, M, kind, param, bordered=not invertible)
    de = decay_exponent(Ks_, vals)
    return {
        "mu": mu,
        "bdl_delta": bdl_delta(mu),
        "bdl_admissible": bdl_admissible(mu),
        "shape": SHIFT if mu == 0.0 else (MULTIPLIER if bdl_admissible(mu)
                                          else TRIDIAGONAL_DOMINANT),
        "tail_block_boundedly_invertible": bool(invertible),
        "needed_bordering": not invertible,
        "M_exponent": md["exponent_in_M"],
        "K": Ks_, "tail_inverse": vals,
        "K_exponent": de.get("exponent"),
        "tail_inverse_decays": (None if de.get("refused") else de["exponent"] < 0.0),
        "decay": de,
    }


#: The numbers leg 53's positive control produced, and WHY they must not be read as a
#: comparison across `mu`.  Keeping the negative construction in the artifact is lesson
#: 76; this is the construction that is WRONG, kept so it stays wrong on the record.
WRONG_OPERATOR_CONTROL = """\
Bordering the tail block at mu > 0 with the mu = 0 near-null pair gives
||B^{-1}||: 1.06e+03 (mu=0.25), 2.06e+04 (mu=1), 8.26e+04 (mu=2) at K=4 -- i.e. it looks
CATASTROPHICALLY WORSE than the mu = 0 bordered constant (2.19).  That reading is wrong,
and leg 53 already banked why: at mu > 0 the tail block HAS NO KERNEL, so bordering it
with a near-null pair that is not near-null for THAT operator adds a spurious almost-
dependent row and column.  It is the wrong operator, not the wrong answer.  The
comparison across mu must use the UNBORDERED inverse wherever the block is invertible,
which is what `classify_operator` does.  These numbers are recorded ONLY so that the
next agent who computes them recognises them and does not publish them."""


# ==========================================================================
# ROUTE-CP (leg 62): CADIOT arXiv:2505.03091's SCOPE, SETTLED FROM THE FULL TEXT
# ==========================================================================
# Leg 57 flagged this paper as independently stating the dominance-hypothesis
# observation and recommended not re-claiming leg 51's finding at full strength.  That
# recommendation is correct and INSUFFICIENT: the same paper is the single largest
# novelty risk to leg 58's proposition, and leg 57 did not establish whether Cadiot's
# construction REACHES the off-diagonal unbounded part with a non-decaying tail inverse
# -- which is NG's hypothesis, not leg 51's.
#
# Everything below is ADDITIVE.  `SHAPE_LEDGER` above is leg 57's artifact and is NOT
# touched: its "four papers" count is quoted in leg 57's prose, in PHASE2_P2_NOTES and
# in CONTINUATION_PROMPT, and a leg that silently changes a number other documents quote
# is a failure mode this repository keeps re-learning.
#
# The novelty pass ran BEFORE any of this: `writeup/novelty/leg_62.md`, verdict
# PROCEED_AS_BOOKKEEPING.  **This leg claims no mathematical novelty of its own.**  It
# settles the scope of somebody else's paper and measures one dial against that paper's
# own worked examples.
#
# TRANSCRIBED vs VERIFIED, the same split as above, because transcription is where
# errors hide:
#   TRANSCRIBED -- every `quote` in `CADIOT_SCOPE` and `CP_FORWARD`, read off the full
#                  text of the PDF (`bash Papers/fetch.sh 2505.03091`, 30 pp., extracted
#                  with pypdf).  The `url` is on every row so the next pass can check the
#                  quote rather than trust it.
#   VERIFIED    -- every number produced by the functions below.  In particular
#                  `cadiot_symbol_admissibility` RE-DERIVES the paper's own constants
#                  (Whitham l_min = 0.2, which Cadiot states in words; Swift-Hohenberg
#                  l_min = mu = 0.28 / 0.32) instead of citing them.

#: Cadiot's clause identifiers, so prose cannot drift into free text.
CP_CLASS = "CLASS"                # eq. (1)-(2): L is a Fourier multiplier
CP_A1_LMIN = "A1_LMIN"            # Assumption 1, first half: |l| >= l_min > 0
CP_A1_GROWTH = "A1_GROWTH"        # Assumption 1, second half: |l| -> +infinity
CP_L31 = "LEMMA_3_1"              # compactness of (L + tI)^{-1}
CP_L32 = "LEMMA_3_2"              # the generalized Gershgorin theorem and its shift s
CP_SYSTEMS = "SYSTEMS"            # section 5.3, the one systems example

#: The located clauses of arXiv:2505.03091 that decide whether our operator is inside
#: its scope.  `holds_for_the_a0_CLM_linearisation` is the field the gate reads, and
#: `why` says what the measurement below reports for it -- never a bare boolean.
CADIOT_SCOPE = [
    {
        "clause": CP_CLASS,
        "where": "section 1 (Introduction), equations (1) and (2)",
        "quote": ("we assume that L is a Fourier multiplier operator, that is it is "
                  "given by its symbol l : R^m -> C as F(Lu)(xi) = l(xi)F(u)(xi) for all "
                  "xi in R^m ... If l is polynomial, then L is a linear differential "
                  "operator with constant coefficients."),
        "supports": ("THE CLASS DEFINITION, and it is reached BEFORE Assumption 1.  A "
                     "Fourier multiplier is diagonal in the Fourier index by "
                     "construction -- section 2.2 makes it explicit: 'the linear part L "
                     "becomes an operator L_q : X_q -> l^2 defined as L_q U = "
                     "(l(n/2q) u_n)_n'.  Our unbounded part is the DILATION TRANSPORT "
                     "X d/dX = sin(theta) d/d(theta), a VARIABLE-coefficient operator "
                     "with no symbol at all; its matrix in the sine basis is bidiagonal "
                     "with EXACTLY ZERO diagonal.  It is outside the class at the level "
                     "of the class, not at the level of a hypothesis."),
        "holds_for_the_a0_CLM_linearisation": False,
        "why": ("measured: `tail_block`'s diagonal is identically 0.0 and its "
                "off-diagonals are ~ k/2, i.e. the whole unbounded part sits off the "
                "Fourier-index diagonal."),
    },
    {
        "clause": CP_A1_LMIN,
        "where": "Assumption 1 (page 6), first half",
        "quote": ("assume that there exists lmin > 0 such that |l(xi)| >= lmin for all "
                  "xi in R^m"),
        "supports": ("A UNIFORM LOWER BOUND on the symbol.  This is the clause the "
                     "standing ban's lift condition names ('whether Cadiot's "
                     "construction covers a ZERO DIAGONAL').  It does not."),
        "holds_for_the_a0_CLM_linearisation": False,
        "why": ("measured: the analogue of l_min for our operator is "
                "min_k |diag(tail_block)| = 0.0 EXACTLY, against Cadiot's own worked "
                "examples at 0.2 (Whitham), 0.28 / 0.32 (Swift-Hohenberg) and ~1.0 "
                "(Gray-Scott) -- see `cadiot_symbol_admissibility`."),
    },
    {
        "clause": CP_A1_GROWTH,
        "where": "Assumption 1 (page 6), second half",
        "quote": "lim_{|xi|_2 -> +infinity} |l(xi)| = +infinity",
        "supports": ("The DIAGONAL is the thing that grows.  This is the half that makes "
                     "the tail estimate a multiplier estimate, and it is used twice in "
                     "section 3 (Lemma 3.1 and Lemma 3.2) rather than being decorative."),
        "holds_for_the_a0_CLM_linearisation": False,
        "why": ("measured: our diagonal is identically zero, so its growth exponent is "
                "not merely small -- it has no referent (discipline 73).  The growth is "
                "entirely in the OFF-diagonal, ~ k/2."),
    },
    {
        "clause": CP_L31,
        "where": "Lemma 3.1, proof (page 9)",
        "quote": ("Now, we obtain that (L + tI)^{-1} : l^2 -> l^2 is compact thanks to "
                  "Assumption 1."),
        "supports": ("Assumption 1 is LOAD-BEARING, not a convenience: the whole "
                     "eigenvalue / essential-spectrum split rests on this compactness, "
                     "and the compactness is exactly '1/l(n) -> 0', i.e. a DECAYING tail "
                     "inverse.  With a zero diagonal there is no t for which "
                     "(L + tI)^{-1} is even defined by this route."),
        "holds_for_the_a0_CLM_linearisation": False,
        "why": ("measured by leg 57 and not re-derived here: the UNBORDERED tail inverse "
                "at mu = 0 grows linearly in the truncation M, i.e. it does not exist as "
                "M -> infinity (`m_divergence`, exponent_in_M ~ +1)."),
    },
    {
        "clause": CP_L32,
        "where": "Lemma 3.2, proof (page 10)",
        "quote": ("since DG(U0)L^{-1} : l^2 -> l^2 is compact and |l(n~)| -> infinity as "
                  "|n| -> infinity, there exists s0 in C sufficiently big in amplitude "
                  "such that |l(n~) + s0| > (1/2) sum_{k != n} |(DG(U0))_{n,k}| for all n "
                  "in Z^m"),
        "supports": ("**THE LOAD-BEARING INEQUALITY, and the one this leg measures.**  "
                     "The generalized Gershgorin theorem Cadiot imports from "
                     "Farid-Lancaster (his [24]) requires ONE shift s in C, big enough in "
                     "amplitude, that makes the shifted diagonal dominate half the row "
                     "sum SIMULTANEOUSLY AT EVERY n.  Such an s exists in his setting "
                     "because the row sums are BOUNDED (DG(U0) is compact and U0 has "
                     "finitely many non-zero coefficients) while |l(n~)| -> infinity.  If "
                     "instead the diagonal is identically zero and the row sums GROW, no "
                     "finite s exists -- and that is a statement about his proof, "
                     "measurable on our matrix, not an opinion about his paper."),
        "holds_for_the_a0_CLM_linearisation": False,
        "why": ("measured: `cadiot_shift_requirement` reports the minimum-modulus s "
                "satisfying this inequality on modes K+1..M.  For our operator at mu = 0 "
                "it GROWS LINEARLY in M (exponent ~ +1.005), so no finite s survives the "
                "limit; for Cadiot's own Whitham operator it SATURATES."),
    },
    {
        "clause": CP_SYSTEMS,
        "where": "section 5.3 (the planar Gray-Scott model), equation (44)",
        "quote": ("l(xi) = [[-lambda_1 |2 pi xi|_2^2 - 1, 0], "
                  "[lambda_1 lambda_2 - 1, -|2 pi xi|_2^2 - lambda_2]] for all xi in R^2"),
        "supports": ("**THE ONLY PLACE AN OFF-DIAGONAL ENTRY ENTERS THIS PAPER AT ALL**, "
                     "and it enters BOUNDED.  A system is the sole route by which "
                     "Cadiot's framework sees an off-diagonal term; in his one systems "
                     "example the off-diagonal entry is the CONSTANT lambda_1 lambda_2 - "
                     "1 = 1/9 while both diagonal entries grow like |2 pi xi|^2.  So even "
                     "in the systems case the unbounded part is diagonal and the "
                     "off-diagonal is a bounded perturbation of it.  Note also that this "
                     "off-diagonality is in the COMPONENT index; ours is in the FOURIER "
                     "index, which is a different axis of the same matrix."),
        "holds_for_the_a0_CLM_linearisation": False,
        "why": ("measured: the ratio |offdiag| / min_i |diag_i| for Cadiot's own "
                "Gray-Scott symbol decays with exponent -2.000 in |xi| and is 2.53e-10 "
                "at |xi| = 1e4.  For our operator the same ratio is FLAT in k "
                "(1/(2 mu) at every mode) and infinite at mu = 0."),
    },
]

#: The forward closure of arXiv:2505.03091, plus the one independent off-diagonal
#: candidate the search produced -- all read at full text by the novelty pass
#: (`writeup/novelty/leg_62.md`).  TRANSCRIBED.  `relaxes_the_hypothesis` is the field
#: that would have to be True anywhere for the gate to move.
CP_FORWARD = [
    {
        "tag": "BCF",
        "arxiv": "2509.17099",
        "url": "https://arxiv.org/abs/2509.17099",
        "authors": "Blanco, Cadiot, Fassler",
        "title": ("Proving the existence of localized patterns and saddle node "
                  "bifurcations in 1D activator-inhibitor type models"),
        "cites_2505_03091_as": "[19]",
        "where": "Assumption 1",
        "quote": ("Given l as in (5), assume there exists sigma_0 > 0 such that "
                  "|det(l(xi))| >= sigma_0 for all xi in R.  That is, det(l(xi)) is "
                  "bounded away uniformly from 0."),
        "relaxes_the_hypothesis": False,
        "note": ("The SYSTEMS form of Assumption 1, and the form that matters here "
                 "because a system is the only route an off-diagonal entry has into this "
                 "framework.  It is a NON-VANISHING DETERMINANT of the matrix symbol -- "
                 "strictly a hypothesis to be checked (their Lemma 2.1 gives explicit "
                 "parameter inequalities for it), not one that can be dropped."),
    },
    {
        "tag": "VDAC",
        "arxiv": "2509.16693",
        "url": "https://arxiv.org/abs/2509.16693",
        "authors": "van der Aalst, Cadiot",
        "title": ("Existence proofs of traveling wave solutions on an infinite strip for "
                  "the suspension bridge equation and proof of orbital stability"),
        "cites_2505_03091_as": "[4]",
        "where": "the symbol lower bound, by cases",
        "quote": ("l(xi_1, xi_2) >= (2 pi xi_2)^2 c^2 + 1 - c^4/4 ... or "
                  "(2 pi xi_2)^4 + 1"),
        "relaxes_the_hypothesis": False,
        "note": ("Same hypothesis, discharged by direct computation of an explicit "
                 "POSITIVE lower bound on the symbol.  The forward closure of 2505.03091 "
                 "into this case TIGHTENS the requirement rather than loosening it."),
    },
    {
        "tag": "BH",
        "arxiv": "2605.03920",
        "url": "https://arxiv.org/abs/2605.03920",
        "authors": "Castro, Gomez-Serrano, Pascual-Caballo",
        "title": "Linear instability of a Burgers-Hilbert traveling wave",
        "cites_2505_03091_as": None,
        "where": "method section (its own placement of radii polynomials)",
        "quote": ("In a broader context ... the reduction of the proof of existence to a "
                  "fixed-point argument has also been particularly successful in the "
                  "context of radii polynomials, developed in [7, 34, 45] and later used "
                  "in [6, 19]."),
        "relaxes_the_hypothesis": False,
        "note": ("The strongest independent off-diagonal candidate the search produced: "
                 "the Burgers-Hilbert linearisation's unbounded part IS a transport term. "
                 " It is NOT a counterexample and does not cite 2505.03091.  It proceeds "
                 "by Fuchsian ODE theory, reducing to a FINITE-dimensional system solved "
                 "in interval arithmetic -- the Chen-Hou pattern again, the shift case "
                 "certified by ABANDONING the tail estimate rather than repairing it, on "
                 "the torus instead of the line.  A second, independent instance of the "
                 "confirmation, from a different community."),
    },
]

#: NOT OBTAINED, recorded rather than glossed (leg 53's failure mode was presenting a
#: source it had not read as if it had).  Farid-Lancaster is Cadiot's reference [24], the
#: engine behind his Lemma 3.2.
CP_NOT_OBTAINED = {
    "source": "Farid & Lancaster, Linear Algebra and its Applications 143:7-17 (1991)",
    "role": "Cadiot's [24]; supplies the generalized Gershgorin theorem of his Lemma 3.2",
    "status": "NOT OBTAINED -- paywalled (Elsevier)",
    "why_it_did_not_block": ("the three hypotheses Cadiot verifies before invoking it are "
                             "reproduced inside his own proof, and the load-bearing one "
                             "is the shifted diagonal-dominance inequality quoted in "
                             "`CADIOT_SCOPE[LEMMA_3_2]` -- a located statement in a "
                             "source we do hold."),
}


def cp_unlocated_rows():
    """Route-CP's analogue of `unlocated_rows`: every clause traced, never an abstract."""
    bad = []
    for r in CADIOT_SCOPE + CP_FORWARD:
        key = r.get("clause") or r.get("tag")
        w = (r.get("where") or "").lower()
        if not w or "abstract" in w:
            bad.append((key, r.get("where")))
        if not r.get("quote"):
            bad.append((key, "(no quote)"))
    return bad


# --------------------------------------------------------------------------
# CADIOT'S OWN WORKED EXAMPLES, AS SYMBOLS -- so his hypothesis becomes a NUMBER
# --------------------------------------------------------------------------
# A hypothesis quoted is a sentence; a hypothesis MEASURED ON THE AUTHOR'S OWN EXAMPLES
# is a magnitude with a scale attached.  Every symbol below is transcribed from the
# section named in `where`, and every `author_states` field is a number the paper states
# in words -- so the measurement can be checked against the author rather than believed.
_TWO_PI = 2.0 * np.pi


def _sh_symbol(xi, mu):
    """Planar Swift-Hohenberg, section 5.1: l(xi) = -(1 - |2 pi xi|^2)^2 - mu."""
    return -(1.0 - (_TWO_PI * np.asarray(xi, float)) ** 2) ** 2 - float(mu)


def _whitham_symbol(xi, T=0.5, c=0.8):
    """Capillary-gravity Whitham, section 5.2: l(xi) = m_T(2 pi xi) - c with
    m_T(k) = sqrt(tanh(k)(1 + T k^2)/k).  The k -> 0 limit of m_T is 1, so l(0) = 1 - c.
    """
    k = _TWO_PI * np.asarray(xi, float)
    out = np.empty(k.shape, float)
    small = np.abs(k) < 1e-10
    out[small] = 1.0
    kk = k[~small]
    out[~small] = np.sqrt(np.tanh(kk) * (1.0 + float(T) * kk ** 2) / kk)
    return out - float(c)


def _gray_scott_symbol(xi, lam1=1.0 / 9.0, lam2=10.0):
    """Planar Gray-Scott, section 5.3 eq. (44) -- a 2x2 MATRIX symbol.

    Returned shape is (n, 2, 2).  This is the only place an off-diagonal entry appears
    anywhere in the paper, and it is the constant `lam1 lam2 - 1`.
    """
    k2 = (_TWO_PI * np.asarray(xi, float)) ** 2
    n = k2.size
    out = np.zeros((n, 2, 2))
    out[:, 0, 0] = -lam1 * k2 - 1.0
    out[:, 1, 1] = -k2 - float(lam2)
    out[:, 1, 0] = lam1 * lam2 - 1.0
    return out


#: name -> the paper's own operator.  `author_states` is what the PAPER says the
#: admissibility constant is, so `cadiot_symbol_admissibility` can be checked against it.
CADIOT_EXAMPLES = {
    "SH_square": {
        "where": "section 5.1 / 5.1.1 (planar Swift-Hohenberg, the unstable square)",
        "params": {"mu": 0.28, "nu1": -1.6, "nu2": 1.0},
        "symbol": lambda xi: _sh_symbol(xi, 0.28),
        "matrix": False,
        "author_states": {"l_min": 0.28,
                          "how": ("|l(xi)| = (1 - |2 pi xi|^2)^2 + mu >= mu, and mu = "
                                  "0.28 is stated in section 5.1.1")},
    },
    "SH_hexagonal": {
        "where": "section 5.1.2 (planar Swift-Hohenberg, the stable hexagon)",
        "params": {"mu": 0.32, "nu1": -1.6, "nu2": 1.0},
        "symbol": lambda xi: _sh_symbol(xi, 0.32),
        "matrix": False,
        "author_states": {"l_min": 0.32, "how": "same, with mu = 0.32"},
    },
    "Whitham": {
        "where": "section 5.2 (capillary-gravity Whitham), Lemma 5.4's proof",
        "params": {"T": 0.5, "c": 0.8},
        "symbol": _whitham_symbol,
        "matrix": False,
        "author_states": {"l_min": 0.2,
                          "how": ("verbatim: 'notice that l(xi) >= l(0) = 1 - c = 0.2 "
                                  "for all xi in R'")},
    },
    "GrayScott": {
        "where": "section 5.3 (planar Gray-Scott), equation (44)",
        "params": {"lambda1": 1.0 / 9.0, "lambda2": 10.0},
        "symbol": _gray_scott_symbol,
        "matrix": True,
        "author_states": {"l_min": None,
                          "how": ("not stated as a number; the symbol is lower "
                                  "triangular with diagonal entries -lam1|2 pi xi|^2 - 1 "
                                  "and -|2 pi xi|^2 - lam2, so sigma_min is measured "
                                  "here rather than quoted")},
    },
}


def _xi_grid(xi_max=1.0e4, n_near=40001, n_far=40000, near=5.0):
    """A grid dense near the origin (where l_min lives) and logarithmic far out."""
    return np.concatenate([np.linspace(0.0, near, int(n_near)),
                           np.geomspace(near, float(xi_max), int(n_far))[1:]])


def cadiot_symbol_admissibility(name, xi_max=1.0e4, fit_from=1.0e2):
    """Assumption 1, as two magnitudes, measured on ONE of Cadiot's own examples.

    Returns `l_min` (Assumption 1's first half -- must be > 0), the growth exponent of
    the symbol at large |xi| (Assumption 1's second half -- must be > 0), and, for the
    one MATRIX example, the ratio |offdiag| / min_i |diag_i| and its exponent: the
    quantity that says whether the unbounded part is still the diagonal.

    Nothing here is a boolean.  `assumption_1_margin` is `l_min` itself, which is exactly
    the distance from admissible to inadmissible in the paper's own units.
    """
    ex = CADIOT_EXAMPLES[name]
    xi = _xi_grid(xi_max)
    vals = ex["symbol"](xi)
    if ex["matrix"]:
        sig = np.linalg.svd(vals, compute_uv=False)[:, -1]
        diag = np.minimum(np.abs(vals[:, 0, 0]), np.abs(vals[:, 1, 1]))
        off = np.abs(vals[:, 1, 0]) + np.abs(vals[:, 0, 1])
    else:
        sig = np.abs(vals)
        diag = sig
        off = np.zeros_like(sig)
    sel = xi >= float(fit_from)
    growth = float(np.polyfit(np.log(xi[sel]), np.log(sig[sel]), 1)[0])
    out = {
        "name": name,
        "where": ex["where"],
        "params": dict(ex["params"]),
        "is_matrix_symbol": bool(ex["matrix"]),
        "l_min": float(sig.min()),
        "argmin_xi": float(xi[int(np.argmin(sig))]),
        "assumption_1_margin": float(sig.min()),
        "growth_exponent": growth,
        "sigma_min_at_xi_max": float(sig[-1]),
        "author_states": ex["author_states"],
        "xi_max": float(xi_max),
    }
    if ex["matrix"]:
        ratio = off / diag
        out["offdiag_over_diag_at_xi_max"] = float(ratio[-1])
        out["offdiag_over_diag_exponent"] = float(
            np.polyfit(np.log(xi[sel]), np.log(ratio[sel]), 1)[0])
        out["offdiag_entry"] = float(off.max())
    return out


# --------------------------------------------------------------------------
# LEMMA 3.2's REQUIREMENT, AS A NUMBER ON WHATEVER MATRIX YOU HAND IT
# --------------------------------------------------------------------------
def gershgorin_rows(T):
    """(|diagonal|, off-diagonal row sums) of a finite matrix -- Lemma 3.2's two inputs.

    `r_n = sum_{k != n} |T_{n,k}|` is Cadiot's `r_n`; `|lambda_n| = |T_{n,n}|` is the
    modulus of his Gershgorin centre.
    """
    T = np.asarray(T, float)
    d = np.abs(np.diag(T))
    r = np.abs(T).sum(axis=1) - d
    return d, r


def gershgorin_dominance_ratio(T):
    """`r_n / |lambda_n|`, row by row.  `inf` wherever the diagonal is exactly zero.

    This is the quantity Cadiot's framework drives to zero and ours does not.  It is
    reported as a LADDER over n (discipline 72), never as its endpoint.
    """
    d, r = gershgorin_rows(T)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(d > 0.0, r / np.where(d > 0.0, d, 1.0), np.inf)


def cadiot_shift_requirement(T):
    """The MINIMUM-MODULUS shift `s` for which Lemma 3.2's proof can be entered.

    Cadiot needs one `s in C` with `|lambda_n + s| > r_n / 2` **simultaneously at every
    n**.  For real centres the minimiser of `|s|` is purely imaginary, `s = i t`, giving
    `lambda_n^2 + t^2 > r_n^2/4` for all n, hence

        |s|_min = sqrt( max_n ( r_n^2/4 - lambda_n^2 )_+ ).

    Returned as a magnitude.  `0.0` means the unshifted matrix is already dominant.  The
    number that matters is not its value at one truncation but whether it SATURATES as
    the truncation grows: a value that grows without bound means no `s` exists on the
    infinite matrix, i.e. Lemma 3.2 cannot be entered at all.
    """
    T = np.asarray(T, float)
    lam = np.diag(T)
    _, r = gershgorin_rows(T)
    return float(np.sqrt(max(0.0, float(np.max(r ** 2 / 4.0 - lam ** 2)))))


def shift_requirement_ladder(matrix_fn, sizes):
    """`cadiot_shift_requirement` over a ladder of truncations, with its exponent.

    `matrix_fn(n)` returns the truncated matrix at size parameter `n`.  The exponent is
    fitted only when every rung is strictly positive; otherwise it is refused with a
    reason rather than reported as a misleading number (discipline 73).
    """
    sizes = [int(s) for s in sizes]
    vals = [cadiot_shift_requirement(matrix_fn(s)) for s in sizes]
    out = {"sizes": sizes, "s_required": vals,
           "ratio_last_over_first": None, "exponent": None, "refused": None}
    if min(vals) <= 0.0:
        out["refused"] = ("at least one rung is exactly 0 -- the unshifted matrix is "
                          "already diagonally dominant there, so an exponent has no "
                          "referent")
        out["saturates"] = True
        return out
    out["exponent"] = float(np.polyfit(np.log(sizes), np.log(vals), 1)[0])
    out["ratio_last_over_first"] = float(vals[-1] / vals[0])
    out["saturates"] = bool(out["exponent"] < 0.1)
    return out


# --------------------------------------------------------------------------
# THE POSITIVE CONTROL: CADIOT'S OWN WHITHAM OPERATOR, IN HIS OWN COORDINATES
# --------------------------------------------------------------------------
def _surrogate_kernel(m, kernel_l1):
    """An even, deterministic, finitely-supported convolution kernel of given l^1 norm.

    **This is a SURROGATE for `DG(U0)`, and it is labelled one.**  The published `u0` of
    section 5.2 is not distributed with the paper, and this leg does not have it; what it
    does have is Cadiot's EXACT symbol, transcribed from section 5.2.  The measurement
    below is designed so that the surrogate cannot carry the conclusion: the l^1 norm is
    a DIAL, and the reported exponent is checked to be the same at every setting of it,
    because the mechanism is `r_n bounded / |l(n~)| -> infinity` and the kernel only sets
    the numerator's level.

    The centre coefficient is set to ZERO on purpose.  A convolution's centre lands on
    the DIAGONAL, where it only helps Cadiot's dominance; zeroing it is the choice that
    is conservative AGAINST his framework and it makes `r_n` exactly `2 ||V||_1` in the
    interior, so the ratio's exponent is a property of HIS SYMBOL alone.
    """
    j = np.arange(-int(m), int(m) + 1)
    v = 1.0 / (1.0 + np.abs(j.astype(float)))
    v[int(m)] = 0.0
    return v * (float(kernel_l1) / np.abs(v).sum())


def cadiot_whitham_matrix(N, d=40.0, kernel_l1=0.35, m=8, T=0.5, c=0.8):
    """`DF(U0)` for Cadiot's section 5.2 example: HIS symbol on the diagonal, a finitely
    supported convolution off it.

    His `F(u) = M_T u - c u + u^2`, so `DF(U0) = L + 2 U0 * (.)`: the diagonal is exactly
    `l(n/2d) = m_T(2 pi n / 2d) - c` and the off-diagonal part is the discrete
    convolution by `2 U0`, which is banded because `U0` has finitely many non-zero
    coefficients (Cadiot's Lemma 3.2 proof says so in as many words).

    `d` is the half-width of `Omega_d`.  The text does not state it to the precision
    needed here; `40.0` is the half-width of the domain drawn in his Figure 3, and the
    ladder's exponent is checked to be `d`-independent in `test_certificate_shapes.py`.
    """
    N = int(N)
    n = np.arange(-N, N + 1)
    lam = _whitham_symbol(n / (2.0 * float(d)), T=T, c=c)
    A = np.diag(lam)
    V = _surrogate_kernel(m, kernel_l1)
    mm = int(m)
    for off in range(-mm, mm + 1):
        val = 2.0 * V[off + mm]
        i = np.arange(max(0, off), min(2 * N + 1, 2 * N + 1 + off))
        A[i, i - off] += val
    return A


def cadiot_ratio_ladder(T_matrix, index, lo_frac=0.25, hi_trim=0):
    """The `r_n/|lambda_n|` ladder and its exponent in |index|, over a stated window.

    The window is reported with the exponent because the ladder is PRE-ASYMPTOTIC for
    Cadiot's Whitham operator (the symbol only reaches its `sqrt(T)|k|^{1/2}` growth
    slowly), and quoting one exponent without the window it was fitted on is how leg 53
    lost a mechanism.
    """
    ratio = gershgorin_dominance_ratio(T_matrix)
    idx = np.asarray(index, float)
    n_max = float(np.max(idx))
    sel = (idx > lo_frac * n_max) & (idx <= n_max - hi_trim) & np.isfinite(ratio)
    out = {"n_first": float(idx[idx > 0][0]) if np.any(idx > 0) else None,
           "ratio_max": float(np.max(ratio[np.isfinite(ratio)]))
           if np.any(np.isfinite(ratio)) else float("inf"),
           "n_infinite_rows": int(np.sum(~np.isfinite(ratio))),
           "window": [float(lo_frac * n_max), float(n_max - hi_trim)]}
    if sel.sum() >= 4 and np.all(ratio[sel] > 0):
        out["exponent"] = float(np.polyfit(np.log(idx[sel]), np.log(ratio[sel]), 1)[0])
        out["ratio_at_window_top"] = float(ratio[sel][-1])
        out["refused"] = False
    else:
        out["exponent"] = None
        out["ratio_at_window_top"] = None
        out["refused"] = True
        out["reason"] = ("the ratio is not finite and positive across the window -- with "
                         "an exactly zero diagonal every row is infinite and an exponent "
                         "has no referent")
    return out


def our_operator_gershgorin(K=8, M=512, mu=0.0):
    """The same two Lemma-3.2 quantities, on the matrix this repository actually built.

    Lesson: a growth rate you cite must be measured on the matrix you actually built.
    This calls `solver.spectral_certificate.tail_block` -- the a = 0 CLM linearisation's
    far-field block, off-diagonals `~ k/2`, diagonal `-mu k` (exactly zero at `mu = 0`).
    """
    from solver.spectral_certificate import tail_block
    T = tail_block(int(K), int(M), mu=float(mu))
    d, r = gershgorin_rows(T)
    ratio = gershgorin_dominance_ratio(T)
    finite = np.isfinite(ratio)
    # rows 0 and -1 of a TRUNCATED bidiagonal block are missing one neighbour each, so
    # their row sums are boundary artifacts and are excluded from the quoted ladder.
    interior = slice(1, -1)
    ri = ratio[interior]
    fi = np.isfinite(ri)
    # r_k = k - 1 exactly for k >= 3 in the interior: check it rather than assume it,
    # because that identity is WHY the ratio's exponent below is mu-independent.
    k = np.arange(int(K) + 1, int(M) + 1, dtype=float)[interior]
    row_sum_identity_err = float(np.max(np.abs(r[interior] - (k - 1.0))))
    return {
        "K": int(K), "M": int(M), "mu": float(mu),
        "diag_min": float(d.min()), "diag_max": float(d.max()),
        "row_sum_min": float(r.min()), "row_sum_max": float(r.max()),
        "row_sum_identity_max_err_vs_k_minus_1": row_sum_identity_err,
        "n_rows": int(d.size),
        "n_rows_with_zero_diagonal": int(np.sum(d == 0.0)),
        "ratio_interior_first": (float(ri[0]) if fi[0] else float("inf")),
        "ratio_interior_last": (float(ri[-1]) if fi[-1] else float("inf")),
        "ratio_max": (float(np.max(ratio[finite])) if finite.any() else float("inf")),
        "s_required": cadiot_shift_requirement(T),
    }


#: The threshold this leg measured, kept as a named constant because two published
#: hypotheses land on the SAME dial at DIFFERENT places and the factor between them is
#: exactly 2.  See `cadiot_vs_bdl_thresholds`.
CADIOT_MU_THRESHOLD = 0.5     # Lemma 3.2's shift exists iff mu >= 1/2 on this family
BDL_MU_THRESHOLD = 1.0        # BDL assumption (5), delta = 1/(2 mu) < 1/2, iff mu > 1


def cadiot_vs_bdl_thresholds():
    """Where each published hypothesis admits the `Lambda^1`-dissipated CLM tail block.

    Both are hypotheses about the SAME one-parameter family, so they can be compared as
    numbers rather than as prose.  Row sums of `tail_block` are `r_k = k - 1` for
    `k >= 3` and the diagonal is `mu k`, so:

      * Cadiot Lemma 3.2 needs `mu k > (k-1)/2` for all k, i.e. `mu >= 1/2`;
      * BDL assumption (5) needs `|offdiag/diag| = 1/(2 mu) < 1/2`, i.e. `mu > 1`.

    **Both are vacuous at `mu = 0`**, which is the case of interest, and neither
    threshold is where the TAIL INVERSE changes character -- leg 57 measured that
    separately and it is `mu = 0` exactly.  These are hypotheses of two CONSTRUCTIONS,
    not properties of the operator; recorded so the three numbers are never conflated.
    """
    return {
        "cadiot_lemma_3_2_mu_threshold": CADIOT_MU_THRESHOLD,
        "bdl_assumption_5_mu_threshold": BDL_MU_THRESHOLD,
        "factor_between_them": BDL_MU_THRESHOLD / CADIOT_MU_THRESHOLD,
        "both_vacuous_at": 0.0,
        "leg_57_operator_hinge": 0.0,
        "note": ("Cadiot's generalized-Gershgorin hypothesis is STRICTLY WEAKER than "
                 "BDL's tridiagonal-dominance hypothesis on this family, by a factor of "
                 "exactly 2 in mu -- Gershgorin bounds the whole row sum with a factor "
                 "1/2, BDL bounds each ratio separately.  Neither reaches mu = 0.  This "
                 "does NOT contradict leg 57, which measured a different quantity (the "
                 "tail inverse's finiteness in M, whose hinge is zero-vs-nonzero "
                 "diagonal); it compares two CONSTRUCTIONS' admissibility instead."),
    }


# --------------------------------------------------------------------------
# THE GATE, AS AN EXECUTABLE PREDICATE -- AND IT CAN ANSWER BOTH WAYS
# --------------------------------------------------------------------------
#: FICTITIOUS.  Lesson 90: a gate that cannot come out the other way is not a gate.  This
#: clause set describes a paper that WOULD cover our case; feeding it to `cadiot_covers`
#: must flip the answer to "yes".  `test_certificate_shapes.py` runs both directions.
CP_SYNTHETIC_COVERING_SCOPE = [
    {
        "clause": CP_CLASS,
        "where": "(none -- this row is a control and cites nothing)",
        "quote": "(none)",
        "supports": "control",
        "holds_for_the_a0_CLM_linearisation": True,
        "why": "fictitious",
    },
    {
        "clause": CP_A1_LMIN,
        "where": "(none -- this row is a control and cites nothing)",
        "quote": "(none)",
        "supports": "control",
        "holds_for_the_a0_CLM_linearisation": True,
        "why": "fictitious",
    },
]


def cadiot_covers(scope=None, forward=None):
    """Route-CP's gate, answered off the located clauses, with the evidence attached.

    The gate, in `DIRECTION.md`'s wording: *does Cadiot arXiv:2505.03091's construction
    cover an operator whose unbounded part is off-diagonal with a non-decaying tail
    inverse -- i.e. does it already contain leg 58's no-go, or a positive result that
    contradicts it?*

    It answers **yes** iff every located clause holds for our operator (the paper's
    construction reaches it) or any forward citation relaxes the hypothesis.  Both
    disjuncts are live: `CP_SYNTHETIC_COVERING_SCOPE` exercises the first and setting
    `relaxes_the_hypothesis` on any `CP_FORWARD` row exercises the second.
    """
    scope = CADIOT_SCOPE if scope is None else scope
    forward = CP_FORWARD if forward is None else forward
    failing = [c["clause"] for c in scope
               if not c["holds_for_the_a0_CLM_linearisation"]]
    relaxed = [f["tag"] for f in forward if f.get("relaxes_the_hypothesis")]
    covered = (not failing) or bool(relaxed)
    return {
        "gate": ("Does Cadiot arXiv:2505.03091's construction cover an operator whose "
                 "unbounded part is off-diagonal with a non-decaying tail inverse -- "
                 "i.e. does it already contain leg 58's no-go, or a positive result that "
                 "contradicts it?"),
        "answer": "yes" if covered else "no",
        "clauses_examined": [c["clause"] for c in scope],
        "clauses_that_fail_for_our_operator": failing,
        "n_clauses_failing": len(failing),
        "forward_citations_examined": [f["tag"] for f in forward],
        "forward_citations_relaxing_the_hypothesis": relaxed,
        "located": [{"clause": c["clause"], "where": c["where"], "quote": c["quote"]}
                    for c in scope],
    }
