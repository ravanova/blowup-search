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
