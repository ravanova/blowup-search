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
# ROUTE-CP v1 (leg 62): CADIOT arXiv:2505.03091, SETTLED FROM THE FULL TEXT
# ==========================================================================
# Leg 57 flagged this paper from two sentences and correctly declined to settle the
# question.  Its recommendation -- do not re-claim leg 51's methodological finding at
# full strength -- was right and incomplete: the same paper is the largest novelty risk
# to leg 58's (NG's) proposition, whose hypothesis is NARROWER than leg 51's.  NG is
# specifically about an unbounded part that is OFF-DIAGONAL with a NON-DECAYING tail
# inverse.  Leg 57 never established whether Cadiot's construction reaches that case.
# This block settles it from the PDF, and records the hypotheses verbatim.
#
# THE VOCABULARY CHANGES HERE, ON PURPOSE.  `SHAPE_LEDGER` above classifies by LABEL
# (MULTIPLIER / SHIFT / ...).  A label cannot express what the located sources actually
# require, which turned out to be an ORDERING OF GROWTH RATES.  So `CP_LEDGER` carries
# two magnitudes per row instead of a label:
#
#   `diag_growth`     gamma_D : |diagonal entry at index k|          ~ k^gamma_D
#   `offdiag_growth`  gamma_R : (weighted) off-diagonal ROW SUM at k ~ k^gamma_R
#
# and the predicate every located construction actually needs is the asymptotic
# Gershgorin dominance ratio
#
#   rho = limsup_k (off-diagonal row sum at k) / |diagonal entry at k|   <   1.
#
# `rho` is the right coordinate and `gamma_D - gamma_R` is not, because BDL is the row
# that separates them: BDL has gamma_D - gamma_R = 0 (EQUAL exponents) and is still
# admissible, because its assumption (5) buys rho <= 2*delta < 1 by a constant factor.
# Both magnitudes are carried; `rho` is the one the gate reads.


#: how deeply the source was read.  A row that is not FULL_TEXT may not carry the gate.
FULL_TEXT = "FULL_TEXT"          # PDF fetched and the located statement read in place
SECOND_HAND = "SECOND_HAND"      # hypotheses recorded from another paper that quotes them

#: `rho`, the asymptotic Gershgorin dominance ratio, when the diagonal vanishes
RHO_INFINITE = float("inf")


CP_LEDGER = [
    {
        "tag": "CADIOT-STAB",
        "arxiv": "2505.03091",
        "url": "https://arxiv.org/abs/2505.03091",
        "authors": "Cadiot",
        "title": ("Stability analysis for localized solutions in PDEs and nonlocal "
                  "equations on R^m"),
        "read_at": FULL_TEXT,
        "fetch": "Papers/fetch.sh 2505.03091",
        # the three applications the paper actually carries, each with its own symbol
        "diag_growth": {"swift_hohenberg": 4.0, "whitham": 0.5, "gray_scott": 2.0},
        "offdiag_growth": 0.0,      # DG(U_0) is a multiplication operator: bounded
        "rho": 0.0,
        "covers_zero_diagonal": False,
        "covers_offdiag_unbounded": False,
        "contains_positive_result_contradicting_NG": False,
        "located": [
            {"where": "Assumption 1 (section 2.1)",
             "quote": ("Let l be defined in (2).  Assume that there exists rho > 0 such "
                       "that l is analytic on the strip I_rho = {z in C^m, |Im(z)|_inf "
                       "<= rho}, where Im(z) is the imaginary part of z.  Moreover, "
                       "assume that there exists l_min > 0 such that |l(xi)| >= l_min "
                       "for all xi in R^m and lim_{|xi|_2 -> +infinity} |l(xi)| = "
                       "+infinity."),
             "supports": ("**THE DECIDING HYPOTHESIS.**  Read with eq. (2), "
                          "F(Lu)(xi) = l(xi) F(u)(xi), it says the unbounded part is a "
                          "FOURIER MULTIPLIER -- exactly diagonal in the Fourier basis, "
                          "constant-coefficient -- AND bounded below.  Our unbounded part "
                          "is a variable-coefficient transport term.  It is outside this "
                          "class by definition, and it is precisely the variable "
                          "coefficient that makes it off-diagonal.")},
            {"where": "section 1.2 (construction of the periodic counterpart)",
             "quote": ("In fact, the operator L becomes an infinite diagonal matrix L_q "
                       "with entries l(n/(2q)) on the diagonal."),
             "supports": ("the multiplier half of the dichotomy, written down as the "
                          "reason the construction works.  Leg 57 located this sentence; "
                          "it is kept because it is the paper's own statement of shape.")},
            {"where": ("section 3 (opening paragraph, 'Spectrum of DF(U_0) using "
                       "Gershgorin disks')"),
             "quote": ("By construction D is supposed to be diagonally dominant, which "
                       "hints to the Gershgorin theorem.  In particular, we derive a "
                       "generalization of the Gershgorin theorem in the specific context "
                       "of Assumptions 1 and 2."),
             "supports": ("the dominance hypothesis, named as a hypothesis, by the author "
                          "of CLN -- and scoped explicitly to Assumptions 1 and 2.")},
            {"where": "proof of Lemma 3.3 (section 3)",
             "quote": ("Now, since L is diagonal, we have that L pi_N = pi_N L pi_N and "
                       "therefore (P^N)^{-1} DF(U_0) pi_N = (P^N)^{-1} DG(U_0) pi_N and "
                       "pi_N DF(U_0) P^N = pi_N DG(U_0) P^N."),
             "supports": ("**THE LOAD-BEARING STEP, AND THE REASON THE ANSWER IS NO.**  "
                          "Diagonality of L is not ambient convenience -- it is the step "
                          "that REMOVES the unbounded part from the off-diagonal blocks, "
                          "so the Gershgorin radii r_n involve only the bounded DG(U_0).  "
                          "When the unbounded part is off-diagonal this identity fails "
                          "and r_n inherits the unbounded entries.  That is exactly NG's "
                          "mechanism, and the paper never meets it.")},
            {"where": "Lemma 2.2 (section 2.3), proof",
             "quote": ("Indeed, using Lemma 3.1 in [21], we known that DG(u~) is "
                       "relatively compact with respect to L.  This implies that "
                       "sigma_ess(DF(u~)) = sigma_ess(L)."),
             "supports": ("the third independent exclusion.  Everything off the diagonal "
                          "is assumed relatively compact w.r.t. the unbounded part.  A "
                          "transport term of the SAME ORDER as the unbounded part is not "
                          "relatively compact with respect to anything in this setup.")},
            {"where": "Remark 4.1 (section 4)",
             "quote": ("Under Assumptions 1 and 2, Theorem 3.9 in [21] provides that "
                       "there exists C > 0 such that Z_{u,1}, Z_{u,2} <= C e^{-2 pi rho "
                       "d}, where rho is given in Assumption 1."),
             "supports": ("the tail bounds DECAY, exponentially in the domain size, and "
                          "the decay is attributed by name to Assumption 1.  This is the "
                          "'decaying tail inverse' half of NG's hypothesis, and the paper "
                          "gets it from precisely the assumption our object violates.")},
            {"where": "section 5.2 (the capillary-gravity Whitham equation)",
             "quote": ("u_t + (1/2) d_x M_T u + u d_x u = 0 ... Using the ansatz X = x - "
                       "c t, we look for u : R -> R satisfying F(u) = M_T u - c u + u^2 = "
                       "0 ... L = M_T - c I, l(xi) = m_T(2 pi xi) - c and G(u) = u^2."),
             "supports": ("**THE NEAR MISS, AND WHY IT IS A MISS.**  This is the one "
                          "equation in the paper carrying a transport term u d_x u.  It "
                          "never becomes an unbounded off-diagonal operator, because the "
                          "traveling-wave reduction divides out d_x: the transport "
                          "collapses to G(u) = u^2, whose derivative 2 u~ is a BOUNDED "
                          "multiplication operator.  The gCLM/CLM linearisation has no "
                          "such reduction -- its a u~ d_x term keeps its derivative and "
                          "its variable coefficient.")},
        ],
        "note": ("Fetched and read at full text on 2026-08-05 (leg 62).  Leg 57 read two "
                 "sentences of this paper from a search index and correctly declined to "
                 "settle the question; this row is the settlement.  **The answer is NO on "
                 "the paper's own defining hypothesis, not on a gap in its coverage** -- "
                 "which is a stronger and more durable NO than an absence of a statement."),
    },
    {
        "tag": "BRT",
        "arxiv": "2504.05066",
        "url": "https://arxiv.org/abs/2504.05066",
        "authors": "Breden, Payan, Reisch, Tang",
        "title": ("Turing instability for nonlocal heterogeneous reaction-diffusion "
                  "systems: a computer-assisted proof approach"),
        "read_at": FULL_TEXT,
        "fetch": "Papers/fetch.sh 2504.05066",
        "diag_growth": {"weyl_law_in_index": "2/n"},
        "offdiag_growth": "p - q_1",         # after their weight; see Lemma 2.10 below
        "rho": 0.0,                          # ONLY when their inequality p - q_1 < 2/n holds
        "covers_zero_diagonal": True,        # the abstract theorem does; see below
        "covers_offdiag_unbounded": False,   # but it returns infinite radii and says nothing
        "contains_positive_result_contradicting_NG": False,
        "located": [
            {"where": "section 2.1, the paragraph introducing Theorem 2.6",
             "quote": ("This stronger version has also been generalized to some infinite "
                       "matrices in [FL91, Theorem 2.1].  However, some of the "
                       "assumptions of [FL91, Theorem 2.1] are needlessly restrictive "
                       "(for instance, all the diagonal elements of L have to be "
                       "nonzero), and others may not be straightforward to check in "
                       "practice (like the invertibility of a one-parameter family of "
                       "operators constructed from L).  We propose below a simpler and "
                       "slightly more general statement."),
             "supports": ("**THE ROW THAT CAPS NG'S WORDING.**  The nonzero-diagonal "
                          "hypothesis of the classical infinite-matrix Gershgorin theorem "
                          "is REMOVED by a 2025 paper.  So NG may NOT phrase its no-go as "
                          "'the published machinery requires a nonzero diagonal' -- that "
                          "sentence is false against this statement.")},
            {"where": "Definition 2.5 (section 2.1)",
             "quote": ("We refer to D_i(L) as the ith Gershgorin disk of L.  We note that "
                       "its radius r_i(L) can be infinite."),
             "supports": ("and here is WHY the removal costs NG nothing in substance: the "
                          "generalised theorem applies to a zero diagonal and returns "
                          "D(0, infinity) = C.  It is VACUOUS, not violated.  The content "
                          "is entirely in whether the radii can be made finite AND smaller "
                          "than the diagonal.")},
            {"where": "Theorem 2.6 (section 2.1)",
             "quote": ("Let E a Banach space having a Schauder basis and satisfying "
                       "assumption (2.2), and L = (l_ij) : E -> E a (possibly unbounded) "
                       "linear operator.  Assume that L has a compact resolvent.  Then, "
                       "the spectrum of L, denoted sigma(L), is included in the union "
                       "over i in N of D_i(L)."),
             "supports": ("the most general Gershgorin statement located anywhere in this "
                          "project.  Its hypotheses are a Schauder basis, a sup-attaining "
                          "property (2.2), and a COMPACT RESOLVENT -- nothing about the "
                          "diagonal at all.")},
            {"where": "section 2.2, immediately after Theorem 2.6",
             "quote": ("Naively, if we apply Theorem 2.6 to M from (1.7), we get no "
                       "information on the localization of the eigenvalues, as some of "
                       "the disks have infinite radius.  Indeed, for i in N, the radii "
                       "(r_{2i+1}(M))_{i in N} are not finite since (B_{i,j})_{j in N} "
                       "are not summable."),
             "supports": ("**the closest any located source comes to our situation** -- "
                          "they face infinite Gershgorin radii and repair them.  The "
                          "repair is Definition 2.8 and it does not transfer; see "
                          "`shift_damping_ladder` below.")},
            {"where": "Definition 2.8 (section 2.2)",
             "quote": ("Let f : x -> max(1, x^p), p >= 0, and Q be the infinite diagonal "
                       "matrix such that Q_{2i+eps, 2j+eta} = (1/f(i)) delta_{2i+eps, "
                       "2j+eta} ... We then define Mtilde = Q^{-1} M Q."),
             "supports": ("**their repair is a DIAGONAL WEIGHT -- the same family "
                          "legs 51-53 swept as the exponent s.**  Conjugation by a "
                          "diagonal Q multiplies entry (i,j) by f(i)/f(j).")},
            {"where": "Lemma 2.10 (section 2.2), with hypothesis (H:B) from section 1.1",
             "quote": ("Let p in (1 - q_2, q_1 + 2/n) ... r_{2i+1}(Mtilde) <= C' |delta| "
                       "i^{p - q_1} + |c| ... Mtilde_{2i+1,2i+1} + r_{2i+1}(Mtilde) <= "
                       "-kappa i^{2/n} + C' |delta| i^{p - q_1} + d + |b|.  Since theta, "
                       "kappa, C' > 0 and p - q_1 < 2/n, the right hand side of (2.9) and "
                       "of (2.10) is negative for all i large enough.  [(H:B), section "
                       "1.1: there exist q_1 > 1/2, q_2 > -3/2, C >= 0 with |B_{i,j}| <= "
                       "C / (max(1, i^{q_1}) max(1, j^{q_2})) for all i, j >= 0.]"),
             "supports": ("**THE PREDICATE, MADE QUANTITATIVE AND PUBLISHED.**  The "
                          "off-diagonal row sum after weighting grows like i^{p - q_1}; "
                          "the diagonal grows like i^{2/n} by Weyl's law (their (2.5)); "
                          "and the method requires p - q_1 < 2/n, i.e. OFF-DIAGONAL "
                          "GROWTH STRICTLY BELOW DIAGONAL GROWTH.  This is the exact "
                          "inequality our object violates, and it is the form NG's "
                          "proposition should take.  Note their off-diagonal is BOUNDED "
                          "and merely non-summable; ours is unbounded.")},
        ],
        "note": ("Cadiot's reference [15], described by him as deriving a generalized "
                 "Gershgorin theorem 'under very broad assumptions ... whenever a linear "
                 "operator is expressed on an adequate Schauder basis'.  It is the "
                 "forward citation with the best chance of covering our case, it removes "
                 "the one hypothesis NG might have leaned on, and it still does not cover "
                 "our case -- for the quantitative reason in Lemma 2.10."),
    },
    {
        "tag": "CB",
        "arxiv": "2404.08529",
        "url": "https://arxiv.org/abs/2404.08529",
        "authors": "Cadiot, Blanco",
        "title": ("The 2D Gray-Scott system of equations: constructive proofs of "
                  "existence of localized stationary patterns"),
        "read_at": FULL_TEXT,
        "fetch": "Papers/fetch.sh 2404.08529",
        "diag_growth": {"gray_scott": 2.0},
        "offdiag_growth": 0.0,
        "rho": 0.0,
        "covers_zero_diagonal": False,
        "covers_offdiag_unbounded": False,
        "contains_positive_result_contradicting_NG": False,
        "located": [
            {"where": "Assumption 1 (section 2.1)",
             "quote": ("Assume that the Fourier transform of the linear operator L is "
                       "given by F(Lu)(xi) = l(xi) u^(xi), for all u in S^k, where l is a "
                       "k by k matrix of polynomials in xi.  Moreover, assume that there "
                       "exists sigma_0 > 0 such that |det(l(xi))| >= sigma_0, for all xi "
                       "in R^m.  That is, the determinant of l(xi) is uniformly bounded "
                       "away from 0."),
             "supports": ("**THE SYSTEMS CASE, THE ONLY ROUTE TO A GENUINELY "
                          "MATRIX-VALUED SYMBOL -- and it is still constant-coefficient.**  "
                          "l is a matrix of POLYNOMIALS in xi, so the unbounded part is "
                          "still a Fourier multiplier: block-diagonal by frequency, with "
                          "finite blocks.  That is exactly the case MM-1 already proves.  "
                          "The determinant condition is the systems form of |l| >= l_min.")},
            {"where": "Remark 2.1 (section 2.1)",
             "quote": ("Observe that Assumption 1 is the equivalent of Assumption 2.1 "
                       "from [15] for systems of PDEs.  In fact, as illustrated in Remark "
                       "2.7 in [15], such an assumption is essential for controlling the "
                       "essential spectrum of L away from zero.  As such, it is necessary "
                       "for constructing a contracting Newton-like fixed point operator, "
                       "which is our main objective in Section 3."),
             "supports": ("the authors call the hypothesis NECESSARY for the fixed-point "
                          "construction, in their own words.  Not a convenience.")},
            {"where": ("Cadiot arXiv:2505.03091 section 5.3, eq. (44) -- the instance, "
                       "read at full text"),
             "quote": ("l(xi) = [[-lambda_1 |2 pi xi|_2^2 - 1, 0], [lambda_1 lambda_2 - "
                       "1, -|2 pi xi|_2^2 - lambda_2]] for all xi in R^2 ... we fix "
                       "lambda_1 = 19 and lambda_2 = 10."),
             "supports": ("**the sharpest single datum in this ledger.**  Here is the one "
                          "place in the whole Cadiot corpus where the LINEAR part has a "
                          "nonzero off-diagonal entry.  It is lambda_1 lambda_2 - 1 = 189, "
                          "a CONSTANT, while the diagonal grows like |2 pi xi|^2.  The "
                          "off-diagonal is present and bounded; the unbounded part is "
                          "diagonal.  rho -> 0.  `solver/literature_gates.py` recomputes "
                          "the crossover frequency from this symbol.")},
        ],
        "note": ("Cadiot's reference [20], the systems extension.  Admitted to this "
                 "ledger because 'systems' is the only mechanism by which the framework "
                 "could acquire an off-diagonal unbounded part, and this row records that "
                 "it does not: the off-diagonal entry it acquires is a constant."),
    },
    {
        "tag": "FL91",
        "arxiv": None,
        "url": "https://www.sciencedirect.com/science/article/pii/002437959190004H",
        "authors": "Farid, Lancaster",
        "title": "Spectral properties of diagonally dominant infinite matrices, II",
        "venue": "Linear Algebra and its Applications 143:7-17 (1991)",
        "read_at": SECOND_HAND,
        "fetch": "(paywalled; no arXiv copy located -- see writeup/novelty/leg_62.md Q3)",
        "diag_growth": None,
        "offdiag_growth": None,
        "rho": None,
        "covers_zero_diagonal": False,
        "covers_offdiag_unbounded": False,
        "contains_positive_result_contradicting_NG": False,
        "located": [
            {"where": ("Theorem 2.1, as quoted and criticised in "
                       "Breden-Payan-Reisch-Tang arXiv:2504.05066 section 2.1 -- read "
                       "there, not here"),
             "quote": ("some of the assumptions of [FL91, Theorem 2.1] are needlessly "
                       "restrictive (for instance, all the diagonal elements of L have to "
                       "be nonzero), and others may not be straightforward to check in "
                       "practice (like the invertibility of a one-parameter family of "
                       "operators constructed from L)"),
             "supports": ("the theorem Cadiot's Lemma 3.2 actually invokes.  It requires a "
                          "NONZERO DIAGONAL, which excludes our case outright.  **This "
                          "row is SECOND_HAND and is marked so.**  Leg 53 was withdrawn "
                          "for reading a hypothesis at the wrong depth; the correction is "
                          "not to hide the depth but to label it.")},
            {"where": ("Cadiot arXiv:2505.03091, proof of Lemma 3.2 -- the hypotheses AS "
                       "APPLIED, read at full text"),
             "quote": ("Consequently, we can find some s in C big enough in amplitude "
                       "such that |lambda_n + s| > (1/2) sum_{k in Z^m} |R_{n,k}| for all "
                       "n in Z^m.  Consequently, the matrix D + sI satisfies the "
                       "hypotheses (1) and (2) of Theorem 2.1 in [24]."),
             "supports": ("this IS first-hand, and it is enough for the gate on its own: "
                          "whatever FL91's exact hypotheses, Cadiot discharges them by "
                          "establishing SHIFTED STRICT DIAGONAL DOMINANCE with FINITE row "
                          "sums.  Our operator has neither -- the row sums diverge and "
                          "there is no diagonal to shift into dominance.")},
        ],
        "note": ("Not reachable at primary source.  Its hypotheses enter this ledger only "
                 "through two sources that were read in full, and the row is flagged "
                 "SECOND_HAND so no later pass mistakes it for a reading.  It does not "
                 "carry the gate: `cp_gate_answer` refuses rows that are not FULL_TEXT."),
    },
    # ----------------------------------------------------------------------
    # OUR OWN OBJECT, on the same axis, so the comparison is arithmetic and not rhetoric.
    # This row is NOT literature and is excluded from the gate by `is_ours`.
    # ----------------------------------------------------------------------
    {
        "tag": "OURS-a0-CLM-BORDERED",
        "arxiv": None,
        "url": None,
        "authors": "(this repository, legs 51-54)",
        "title": ("the a = 0 CLM linearisation's bordered far-field block "
                  "(solver/spectral_certificate.py)"),
        "read_at": FULL_TEXT,
        "fetch": "(local)",
        "diag_growth": {"a0_clm": 0.0},     # the diagonal is EXACTLY zero
        "offdiag_growth": 1.0,              # the coupling entry is K/2 -- linear in K
        "rho": RHO_INFINITE,
        "covers_zero_diagonal": None,
        "covers_offdiag_unbounded": None,
        "contains_positive_result_contradicting_NG": False,
        "is_ours": True,
        "located": [
            {"where": ("legs 53 and 54 (MM), recorded in plan_of_record.py's ban list -- "
                       "this repository's own full text"),
             "quote": ("the coupling entry is K/2 for EVERY s, the sweep K = 4..64 has "
                       "its minimum at the smallest K and still gives 43.15, and "
                       "Z_1[Gamma<-tail] is 546.57 for all four border directions because "
                       "that sub-block never sees the border"),
             "supports": ("gamma_R = 1 (the off-diagonal grows linearly in the split) and "
                          "gamma_D = 0 (the diagonal is exactly zero), hence rho = "
                          "infinity.  Every located source needs rho < 1.")},
        ],
        "note": ("Placed on the same axis as the literature so the gate's answer is an "
                 "inequality rather than an impression.  **The margin is not small and "
                 "not marginal: every located construction sits at rho = 0 (or rho <= "
                 "2*delta < 1 for BDL), and this object sits at rho = infinity.**"),
    },
]


def cp_literature_rows(rows=None):
    """The literature rows of `CP_LEDGER` -- our own object is not evidence about it."""
    rows = CP_LEDGER if rows is None else rows
    return [r for r in rows if not r.get("is_ours", False)]


def our_cp_row(rows=None):
    """The repository's own object, as one row on the same axis."""
    rows = CP_LEDGER if rows is None else rows
    ours = [r for r in rows if r.get("is_ours", False)]
    assert len(ours) == 1, "CP_LEDGER must carry exactly one row for our own object"
    return ours[0]


def dominance_ratio_admits(rho):
    """Does a source's asymptotic Gershgorin dominance ratio admit the tail estimate?

    The predicate is `rho < 1`, and it is the ONLY predicate this leg's gate reads.  It
    is chosen over the exponent difference `gamma_D - gamma_R` because BDL separates
    them: BDL has EQUAL exponents and is still admissible, on a constant factor.

    `None` (unknown) is neither admissible nor inadmissible -- it is refused, so an
    unread source can never silently answer a gate.
    """
    if rho is None:
        return None
    return bool(rho < 1.0)


def cp_gate_answer(rows=None):
    """Answer Route-CP's gate from the ledger, with the located evidence attached.

    THE GATE (verbatim, DIRECTION.md leg 62):
      "Does Cadiot arXiv:2505.03091's construction cover an operator whose unbounded
       part is off-diagonal with a non-decaying tail inverse -- i.e. does it already
       contain leg 58's no-go, or a positive result that contradicts it?"

    A row answers YES only if it covers an off-diagonal unbounded part, or carries a
    positive result contradicting NG.  Rows not read at full text are REFUSED rather
    than counted either way -- leg 53's correction, applied as code.
    """
    rows = cp_literature_rows(rows)
    full = [r for r in rows if r["read_at"] == FULL_TEXT]
    refused = [r["tag"] for r in rows if r["read_at"] != FULL_TEXT]
    covering = [r for r in full if r.get("covers_offdiag_unbounded")]
    contradicting = [r for r in full
                     if r.get("contains_positive_result_contradicting_NG")]
    return {
        "gate": ("Does Cadiot arXiv:2505.03091's construction cover an operator whose "
                 "unbounded part is off-diagonal with a non-decaying tail inverse -- "
                 "i.e. does it already contain leg 58's no-go, or a positive result that "
                 "contradicts it?"),
        "answer": "yes" if (covering or contradicting) else "no",
        "covering_rows": [r["tag"] for r in covering],
        "contradicting_rows": [r["tag"] for r in contradicting],
        "n_full_text": len(full),
        "refused_not_full_text": refused,
        "rows": [{"tag": r["tag"], "arxiv": r["arxiv"], "url": r["url"],
                  "read_at": r["read_at"],
                  "rho": r["rho"],
                  "rho_admits_tail_estimate": dominance_ratio_admits(r["rho"]),
                  "offdiag_growth": r["offdiag_growth"],
                  "diag_growth": r["diag_growth"],
                  "n_located": len(r["located"]),
                  "located_where": [d["where"] for d in r["located"]]}
                 for r in rows],
        "ours": {"tag": our_cp_row()["tag"],
                 "rho": our_cp_row()["rho"],
                 "rho_admits_tail_estimate": dominance_ratio_admits(our_cp_row()["rho"]),
                 "diag_growth": our_cp_row()["diag_growth"],
                 "offdiag_growth": our_cp_row()["offdiag_growth"]},
    }


def cp_unlocated_rows(rows=None):
    """Same guard as `unlocated_rows`, over `CP_LEDGER`, plus a depth check.

    Adds one clause leg 57's guard did not have: a row read only SECOND_HAND must SAY so
    in its `where`, so the depth of the reading travels with the quotation.
    """
    rows = CP_LEDGER if rows is None else rows
    bad = []
    for r in rows:
        if not r["located"]:
            bad.append((r["tag"], "(no located statement at all)"))
        for d in r["located"]:
            w = d["where"].lower()
            if not d["where"] or "abstract" in w:
                bad.append((r["tag"], d["where"]))
            if not (d["quote"] and d["supports"]):
                bad.append((r["tag"], f"{d['where']} (empty quote or supports)"))
        if r["read_at"] == SECOND_HAND:
            if not any("read \nthere" in d["where"].lower()
                       or "read there" in d["where"].lower()
                       or "as quoted" in d["where"].lower()
                       for d in r["located"]):
                bad.append((r["tag"], "SECOND_HAND row does not disclose its depth"))
    return bad


# --------------------------------------------------------------------------
# WHY THE ONE PUBLISHED REPAIR FOR INFINITE GERSHGORIN RADII CANNOT REACH US
# --------------------------------------------------------------------------
# BRT Definition 2.8 repairs infinite radii by conjugating with a DIAGONAL weight
# `Q = diag(1/f(i))`, `f(i) = max(1, i^p)`.  That maps entry `(i, j)` to
# `(f(i)/f(j)) M_{i,j}`.  It is the same one-parameter family legs 51-53 swept as the
# weight exponent `s`, and legs 51-53 measured it failing ("the coupling entry is K/2 for
# EVERY s").  These two functions are WHY, and they turn that measurement into an
# identity:
#
#   for a NEAREST-NEIGHBOUR coupling, `j = i + offset` with `offset` FIXED,
#       f(i)/f(i+offset) = (i/(i+offset))^p  ->  1   as i -> infinity, FOR EVERY p.
#
# A diagonal weight cannot damp a shift, because a shift's entries live a BOUNDED
# DISTANCE from the diagonal and any diagonal weight is asymptotically flat there.  BRT
# are not damping a shift: their `B_{i,j}` is spread across the whole row and bounded, so
# the same weight converts a divergent row sum into `C' i^{p-q_1}`.  Different operator,
# different repair, and the repair does not transfer.  Both halves are MEASURED here, so
# the contrast is arithmetic rather than asserted.
def diagonal_weight_ratio(i, offset, p):
    """BRT's conjugation factor `f(i)/f(i+offset)` for `f(x) = max(1, x^p)`."""
    fi = max(1.0, float(i) ** float(p))
    fj = max(1.0, float(i + offset) ** float(p))
    return fi / fj


def shift_damping_ladder(ps=(0.0, 0.5, 1.0, 2.0, 4.0), offset=1,
                         indices=(8, 32, 128, 512, 2048, 8192)):
    """How much a diagonal weight damps a NEAREST-NEIGHBOUR coupling, as `i` grows.

    Returns, for every exponent `p`, the ladder of `f(i)/f(i+offset)` and how far the
    last rung sits from 1.  A repair would need this to go to ZERO.  It goes to ONE, and
    the magnitude of its approach is the report -- never a boolean.
    """
    out = []
    for p in ps:
        vals = [diagonal_weight_ratio(i, offset, p) for i in indices]
        out.append({"p": float(p), "offset": int(offset),
                    "indices": [int(i) for i in indices],
                    "ratio": [float(v) for v in vals],
                    "ratio_at_largest_index": float(vals[-1]),
                    "distance_from_one_at_largest_index": float(abs(1.0 - vals[-1]))})
    return out


def spread_damping_ladder(p, q1, q2=1.0, indices=(8, 32, 128, 512), n_terms=20000):
    """The SAME weight against BRT's OWN operator -- the contrast that makes the point.

    BRT's off-diagonal is bounded and spread: `|B_{i,j}| <= C i^{-q1} j^{-q2}` (H:B).  The
    weighted row sum `sum_j (f(i)/f(j)) |B_{i,j}|` then grows like `i^{p-q1}` (their eq.
    (2.8)).  This function measures that exponent numerically with `C = 1`, so the claim
    "the weight works there and not here" is a computed pair of exponents rather than a
    pair of adjectives.
    """
    rows = []
    for i in indices:
        fi = max(1.0, float(i) ** float(p))
        s = 0.0
        for j in range(n_terms):
            fj = max(1.0, float(j) ** float(p))
            b = 1.0 / (max(1.0, float(i) ** float(q1)) * max(1.0, float(j) ** float(q2)))
            s += (fi / fj) * b
        rows.append({"i": int(i), "weighted_row_sum": float(s)})
    slope, _ = np.polyfit(np.log([r["i"] for r in rows]),
                          np.log([r["weighted_row_sum"] for r in rows]), 1)
    return {"p": float(p), "q1": float(q1), "q2": float(q2), "rows": rows,
            "measured_growth_exponent_in_i": float(slope),
            "brt_predicted_exponent_p_minus_q1": float(p) - float(q1)}
