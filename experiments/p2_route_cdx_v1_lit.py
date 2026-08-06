"""Route-CDX v1 (leg 157): CADIOT arXiv:2505.03091 READ FOR ITS CONSTRUCTION, NOT ITS SCOPE.

Leg 62 (Route-CP) read this paper at full text and settled a COVERAGE question: does
Cadiot's framework reach our operator?  It answered NO on 6 of 6 located clauses.  That
leg never asked what his construction is MADE of, and it followed only FORWARD citations
(`CP_FORWARD`).  This leg asks the deeper question DIRECTION.md ### 157 poses:

    does Cadiot's own construction -- whatever approximate-inverse or preconditioning
    technique it uses for its covered case -- suggest an adaptation, generalization, or
    explicit alternative construction that could be tried on the A21 != 0 class leg 127
    (NGX) is searching?

This is read-deeper-not-reconfirm.  Leg 62's NO is not re-litigated and is not reopened.

PRE-COMMITTED CLAUSES, written before the run, both branches reportable:

  CDX0 THE NOVELTY PASS CAME FIRST, and it CHANGED THIS LEG'S ANSWER.
       `writeup/novelty/leg_157.md`, committed BEFORE this file existed (commit
       "Leg 157: LEG -- Route-CDX novelty pass, run and logged BEFORE construction").
       The pass's headline candidate -- Cadiot's BACKWARD citation [15],
       Breden-Payan-Reisch-Tang arXiv:2504.05066 -- was drafted as "never consulted by
       this repository" and the in-repo sweep FALSIFIED that: leg 62 already identified
       it mid-cycle and relayed its operative reading to leg 58
       (`reports/REPORT_2026-08-05.md` ll. 219-223).  That verdict is carried into the
       JSON so the prose cannot overstate past it.  This leg claims NO mathematical
       novelty of its own.

  CDX1 EVERY CLAUSE IS TRACED TO A LOCATED FULL-TEXT STATEMENT -- section / definition /
       theorem number plus the sentence verbatim.  Never an abstract.  Both PDFs fetched,
       not searched (`bash Papers/fetch.sh 2505.03091 2504.05066`, `pdftotext -layout`).

  CDX2 THE CONSTRUCTION IS INVENTORIED, AND TRANSLATED INTO THIS REPOSITORY'S OWN
       A-SHAPE LANGUAGE.  A technique described in someone else's notation is a sentence;
       a technique translated into `Z_1 = ||I - AL||`'s block structure is something
       leg 127 can accept or reject.  Each row carries `a21_is_zero`, which is the field
       the gate reads.

  CDX3 THE DECIDING STRUCTURAL FACT IS MEASURED, NOT ASSERTED.  Both papers build their
       change of basis as `P = P_N + (I - Pi^N)` -- an invertible finite block, and the
       IDENTITY on the tail.  The claim "so the induced approximate inverse has A21 = 0"
       is checked as a matrix identity, with a control that reports the other answer.

  CDX4 THE ONE HYPOTHESIS THAT COULD HAVE OPENED A ROUTE IS MEASURED ON OUR OPERATOR.
       BPRT's Theorem 2.6 removes Farid-Lancaster's nonzero-diagonal requirement outright
       and asks in exchange only that L have COMPACT RESOLVENT.  For an operator with
       discrete spectrum that means the eigenvalues leave every bounded set: only finitely
       many |lambda| <= 1.  Measured as a LADDER in the truncation (discipline 72), with
       a positive control that saturates.

  CDX5 A DIAGONAL CHANGE OF BASIS CANNOT MANUFACTURE A NONZERO DIAGONAL.  BPRT's first
       change of basis (Definition 2.8) is diagonal, and so is this repository's entire
       weight family (leg 52).  Checked as a BITWISE identity, with a non-diagonal control
       that moves it.

  CDX6 THE GATE IS ANSWERED IN DIRECTION.md's PRE-COMMITTED WORDING, off an executable
       predicate that can answer both ways.

WHAT THIS RUNNER DOES NOT DO.  Per the gate's own yes-branch ("do not build or test it
under this leg's own authority") it builds and tests NO construction.  Every measurement
below checks whether a PUBLISHED HYPOTHESIS holds for our operator -- leg 62's precedent
exactly -- and none of them evaluates a candidate certificate.  It edits no solver module;
it only READS `solver.spectral_certificate.tail_block`.  It says nothing about
`HL_S2_nonsymmetric` and nothing about any link of the L1->L4 chain.  It does not reopen
leg 62's NO, does not touch `CADIOT_SCOPE`, and is not evidence FOR leg 58's proposition.

Run: `.venv/bin/python experiments/p2_route_cdx_v1_lit.py`
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.spectral_certificate import tail_block                     # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_cdx_v1_lit.json"

K_SPLIT = 8
MS = (128, 256, 512, 1024)
RNG = np.random.default_rng(1957)


# --------------------------------------------------------------------------
# CDX1 / CDX2 -- THE CONSTRUCTION INVENTORY, LOCATED AND TRANSLATED
# --------------------------------------------------------------------------
# TRANSCRIBED: every `quote` is read off the full text of the PDF named in `paper`.
# The `url` is on every row so the next pass can CHECK the quote rather than trust it.

CDX_CONSTRUCTIONS = [
    {
        "tag": "PSEUDO_DIAG",
        "paper": "arXiv:2505.03091",
        "url": "https://arxiv.org/abs/2505.03091",
        "where": "section 3, the paragraph defining P, and eq. (15)",
        "quote": ("Our approach is based on a pseudo-diagonalization of DF(U0), that is we "
                  "construct a linear operator P and its inverse, and study the spectrum "
                  "of D = P^{-1} DF(U0) P instead.  ...  We choose the linear operator P "
                  "as P = P^N + pi_N : l^2 -> l^2 where P^N = pi^N P^N pi^N and "
                  "P^N : pi^N l^2 -> pi^N l^2 is invertible.  ...  In practice we choose "
                  "P^N such that the columns of P^N approximate the eigenvectors of "
                  "pi^N DF(U0) pi^N."),
        "what_it_is": ("A SIMILARITY transform, not an approximate inverse: an invertible "
                       "finite block P^N on the first N modes, and the IDENTITY on the "
                       "tail.  This is the technique leg 62 never examined AS a technique, "
                       "and it is the natural candidate for manufacturing a nonzero "
                       "diagonal out of a zero-diagonal operator -- conjugation moves the "
                       "diagonal, which is exactly what a weighted space cannot do."),
        "why_it_does_not_reach_us": ("P is the IDENTITY on the tail BY CONSTRUCTION, and "
                                     "the tail is where our zero diagonal lives.  The "
                                     "paper says so itself for the tail rows: 'For the "
                                     "case n in Z^m \\ I^N, notice that lambda_n = "
                                     "(pi_N (L + DG(U0)) pi_N)_{n,n} = l(n~) + "
                                     "(DG(U0))_{n,n}' -- the RAW diagonal, unconjugated.  "
                                     "The pseudo-diagonalization cannot move it."),
        "a21_is_zero": True,
    },
    {
        "tag": "L_CANCELS",
        "paper": "arXiv:2505.03091",
        "url": "https://arxiv.org/abs/2505.03091",
        "where": "Lemma 3.3, proof (page 11)",
        "quote": ("Now, since L is diagonal, we have that L pi_N = pi_N L pi_N and "
                  "therefore (P^N)^{-1} DF(U0) pi_N = (P^N)^{-1} DG(U0) pi_N and "
                  "pi_N DF(U0) P^N = pi_N DG(U0) P^N."),
        "what_it_is": ("THE ALGEBRAIC HINGE OF THE WHOLE CONSTRUCTION, and it is one "
                       "line.  The UNBOUNDED part L drops out of BOTH finite-tail "
                       "coupling blocks, leaving only the bounded part DG(U0).  That is "
                       "why Cadiot's coupling blocks are bounded and ours (leg 53's K/2) "
                       "are not."),
        "why_it_does_not_reach_us": ("the cancellation is licensed by 'since L is "
                                     "diagonal' and by nothing else.  Our unbounded part "
                                     "is bidiagonal with an exactly zero diagonal, so "
                                     "L pi_N != pi_N L pi_N and the unbounded part "
                                     "SURVIVES in the coupling blocks.  This is leg 53's "
                                     "K/2 coupling, reached from the literature's side."),
        "a21_is_zero": True,
    },
    {
        "tag": "SHIFT_S",
        "paper": "arXiv:2505.03091",
        "url": "https://arxiv.org/abs/2505.03091",
        "where": "Lemma 3.2, proof (page 10)",
        "quote": ("Consequently, we can find some s in C big enough in amplitude such "
                  "that |lambda_n + s| > (1/2) sum_{k in Z^m} |R_{n,k}| for all n in Z^m.  "
                  "Consequently, the matrix D + sI satisfies the hypotheses (1) and (2) "
                  "of Theorem 2.1 in [24]."),
        "what_it_is": ("A SHIFT inside the approximate inverse: the tail is inverted as "
                       "(S + tI)^{-1}, not S^{-1} (see Lemma 4.1's Z_{1,3}, Z_{1,4}).  "
                       "This repository's A has never carried a shift."),
        "why_it_does_not_reach_us": ("MEASURED BY LEG 62 AND NOT RE-DERIVED HERE: the "
                                     "minimum-modulus s satisfying this inequality grows "
                                     "LINEARLY in the truncation for our operator "
                                     "(exponent ~ +1.005), so no finite s survives the "
                                     "limit; Cadiot's own Whitham operator SATURATES at "
                                     "0.28723.  Note the shift exists only to satisfy "
                                     "[24]'s hypotheses -- see FL91_REPLACED."),
        "a21_is_zero": True,
    },
    {
        "tag": "SYSTEMS_ELIMINATION",
        "paper": "arXiv:2505.03091",
        "url": "https://arxiv.org/abs/2505.03091",
        "where": "section 5.3, proof of Theorem 5.5, eq. (46)",
        "quote": ("Then, taking the second equation of DF(u~)u - lambda u = 0, we have "
                  "that (lambda_1 lambda_2 - 1) u_1 + (Delta - lambda_2 - lambda) u_2 = 0. "
                  " This implies that |lambda_2 + lambda| ||u_2||_2 <= "
                  "||(Delta - lambda_2 - lambda) u_2||_2 = ||(lambda_1 lambda_2 - 1) "
                  "u_1||_2 <= |lambda_1 lambda_2 - 1| ||u_1||_2.  In particular, using the "
                  "above, we have that ||u_1||_2 > 0."),
        "what_it_is": ("THE CLOSEST SHAPE-MATCH IN EITHER PAPER TO LEG 127's CANDIDATE "
                       "PROOF.  It is a worked TWO-DIRECTION argument in the presence of "
                       "a nonzero off-diagonal: use the row the off-diagonal populates to "
                       "bound one component by the other, then substitute back.  "
                       "DIRECTION.md ### 127 describes exactly this shape ('pair "
                       "x = (0; h) with the columns A21 populates')."),
        "why_it_does_not_reach_us": ("it is CONFIRMATION that leg 127's chosen proof shape "
                                     "is the one the literature uses, NOT a new technique: "
                                     "leg 58's SS5 already measured this trade-off "
                                     "(A21 != 0 buys back exactly one unit on the kernel "
                                     "direction).  It is also the COMPONENT index, not the "
                                     "Fourier index, and Cadiot's off-diagonal entry is "
                                     "the bounded constant lambda_1 lambda_2 - 1 = 1/9 "
                                     "against diagonals growing like |2 pi xi|^2."),
        "a21_is_zero": False,
    },
    {
        "tag": "FL91_REPLACED",
        "paper": "arXiv:2504.05066",
        "url": "https://arxiv.org/abs/2504.05066",
        "where": "section 2.1, the paragraph introducing Theorem 2.6 (page 9)",
        "quote": ("has also been generalized to some infinite matrices in [FL91, Theorem "
                  "2.1].  However, some of the assumptions of [FL91, Theorem 2.1] are "
                  "needlessly restrictive (for instance, all the diagonal elements of L "
                  "have to be nonzero), and others may not be straightforward to check in "
                  "practice (like the invertibility of a one-parameter family of operators "
                  "constructed from L).  We propose below a simpler and slightly more "
                  "general statement, which is still strongly inspired from [FL91, Theorem "
                  "2.1] and from its proof, but is easier to use in practice.  Indeed, in "
                  "addition to (2.2), we simply require that L has compact resolvent."),
        "what_it_is": ("THE SINGLE MOST RELEVANT SENTENCE THIS DEEP-MINE FOUND.  Cadiot's "
                       "Lemma 3.2 imports Farid-Lancaster [24] = [FL91], which "
                       "`CP_NOT_OBTAINED` records as 'NOT OBTAINED -- paywalled "
                       "(Elsevier)'.  BPRT state FL91's hypotheses explicitly -- "
                       "DISCHARGING leg 62's un-read-source gap secondhand -- and then "
                       "REPLACE the theorem with one that drops the nonzero-diagonal "
                       "requirement and the shift entirely.  Theorem 2.6's hypotheses in "
                       "full: E Banach with a Schauder basis, property (2.2), and L has "
                       "COMPACT RESOLVENT.  No l_min, no dominance, no multiplier."),
        "why_it_does_not_reach_us": ("two independent reasons, both recorded rather than "
                                     "one.  (i) It is an EIGENVALUE ENCLOSURE theorem, "
                                     "not an approximate-inverse construction -- it "
                                     "produces no Z_1 bound, so it is not applicable to "
                                     "the A21 != 0 class; it replaces the question rather "
                                     "than answering it.  (ii) Its one non-automatic "
                                     "hypothesis, COMPACT RESOLVENT, is measured on our "
                                     "operator below (CDX4) and is the hypothesis that "
                                     "fails.  Leg 62 already relayed the operative "
                                     "reading of this paper to leg 58 -- see CDX0."),
        "a21_is_zero": True,
    },
    {
        "tag": "TWO_BASIS_CHANGES",
        "paper": "arXiv:2504.05066",
        "url": "https://arxiv.org/abs/2504.05066",
        "where": "section 2.2, Definition 2.8 and Definition 2.14 / eq. (2.12)",
        "quote": ("The purpose of this section is to introduce two successive changes of "
                  "basis, where the first one ensures that all the radii become finite, "
                  "and the second one brings enough control on the first disks.  ...  Let "
                  "f : x -> max(1, x^p), p >= 0, and Q be the infinite diagonal matrix "
                  "...  We then define M~ = Q^{-1} M Q.  ...  Let P_N be an invertible "
                  "matrix of size 2N x 2N, obtained numerically such that "
                  "P_N^{-1} Pi^N M~ Pi^N P_N is approximately diagonal ...  We then define "
                  "P, an infinite matrix, by P = P_N + I - Pi^N."),
        "what_it_is": ("The most general preconditioning in this lineage: a DIAGONAL "
                       "weight Q, then a finite-rank near-diagonalization P.  Notably "
                       "BPRT allow Q^{-1} to be UNBOUNDED ('Q is invertible but its "
                       "inverse is unbounded when p > 0'), which this repository's weight "
                       "family does not exploit."),
        "why_it_does_not_reach_us": ("BOTH changes of basis are powerless on the tail, for "
                                     "two DIFFERENT measured reasons.  Q is diagonal, and "
                                     "a diagonal conjugation preserves the diagonal "
                                     "BITWISE (CDX5) -- it can never manufacture a nonzero "
                                     "diagonal, which is also why leg 52's weight family "
                                     "never could.  P is the identity on the tail, exactly "
                                     "as Cadiot's is (CDX3).  Their own operator does not "
                                     "need either to: its diagonal grows by Weyl's law, "
                                     "'lambda_i >= kappa i^{2/n}' (eq. (2.5))."),
        "a21_is_zero": True,
    },
]


def cdx_unlocated_rows():
    """Every clause traced to a section, never an abstract, and never without a quote."""
    bad = []
    for r in CDX_CONSTRUCTIONS:
        w = (r.get("where") or "").lower()
        if not w or "abstract" in w:
            bad.append((r["tag"], r.get("where")))
        if not r.get("quote"):
            bad.append((r["tag"], "(no quote)"))
    return bad


# --------------------------------------------------------------------------
# CDX3 -- "IDENTITY ON THE TAIL" => A21 = 0, AS A MATRIX IDENTITY
# --------------------------------------------------------------------------
def induced_a21_norm(n, n_finite, tail_is_identity=True):
    """Translate `P = P_N + (I - Pi^N)` into this repository's A-shape language.

    Both papers precondition by conjugation: the induced operator acting on the problem
    is `A = P D P^{-1}` for a block-diagonal `D`.  This measures the resulting
    tail-by-finite block `A21` -- the block leg 58's theorem requires to be zero and
    leg 127 is searching for a nonzero admissible choice of.

    `tail_is_identity=False` is the CONTROL (lesson 90): it perturbs P's tail-by-finite
    block away from zero, and the SAME code path must then report a nonzero A21.  If it
    could not, this measurement would be a tautology of the code rather than a finding.
    """
    n, n_finite = int(n), int(n_finite)
    P = np.eye(n)
    P[:n_finite, :n_finite] = RNG.normal(size=(n_finite, n_finite)) + 3.0 * np.eye(n_finite)
    if not tail_is_identity:
        P[n_finite:, :n_finite] = RNG.normal(size=(n - n_finite, n_finite))
    D = np.zeros((n, n))
    D[:n_finite, :n_finite] = RNG.normal(size=(n_finite, n_finite))
    D[n_finite:, n_finite:] = np.diag(RNG.normal(size=n - n_finite))
    A = P @ D @ np.linalg.inv(P)
    return float(np.max(np.abs(A[n_finite:, :n_finite])))


# --------------------------------------------------------------------------
# CDX4 -- BPRT THEOREM 2.6's ONE NON-AUTOMATIC HYPOTHESIS, ON OUR OPERATOR
# --------------------------------------------------------------------------
RADII = (1.0, 10.0, 100.0)


def compact_resolvent_ladder(matrix_fn, sizes, radii=RADII):
    """Do the eigenvalues LEAVE every bounded set as the truncation grows?

    Theorem 2.6 asks only that `L` have COMPACT RESOLVENT.  For an operator whose
    spectrum is a sequence of eigenvalues that is equivalent to: every disc of fixed
    radius contains only finitely many eigenvalues, so the count inside a FIXED disc
    SATURATES as the truncation grows.  A count that keeps growing means the eigenvalues
    accumulate, the resolvent is not compact, and Theorem 2.6 -- which needs no nonzero
    diagonal at all -- is nevertheless unavailable.

    Reported as a LADDER at several radii, not an endpoint (discipline 72).  The growth
    here is LOGARITHMIC in the truncation, so the honest summary statistic is the slope
    against log2(size) -- "new eigenvalues admitted per doubling of the truncation" --
    and NOT a log-log exponent, which would flatter a logarithm into a small power.
    """
    sizes = [int(s) for s in sizes]
    spectra = [np.abs(np.linalg.eigvals(np.asarray(matrix_fn(s), float))) for s in sizes]
    out = {"sizes": sizes,
           "min_abs_eigenvalue": [float(np.min(a)) for a in spectra],
           "per_radius": {}}
    saturates_all = True
    for r in radii:
        vals = [int(np.sum(a <= float(r))) for a in spectra]
        slope = float(np.polyfit(np.log2(sizes), vals, 1)[0])
        sat = bool(slope < 0.5)
        saturates_all = saturates_all and sat
        out["per_radius"][f"r={r:g}"] = {
            "count_in_disc": vals,
            "new_eigenvalues_per_doubling": slope,
            "saturates": sat,
        }
    out["saturates"] = saturates_all
    out["compact_resolvent_hypothesis_holds"] = saturates_all
    return out


def _growing_diagonal(m):
    """POSITIVE CONTROL for CDX4: a diagonal operator whose symbol grows, i.e. exactly
    the class Cadiot's Assumption 1 and BPRT's Weyl-law bound (2.5) both describe.  Its
    resolvent IS compact, so the same code path must report SATURATION here."""
    return np.diag(np.arange(1, int(m) + 1, dtype=float))


# --------------------------------------------------------------------------
# CDX5 -- A DIAGONAL CHANGE OF BASIS CANNOT MOVE THE DIAGONAL
# --------------------------------------------------------------------------
def diagonal_conjugation_moves_diagonal(T, log_weights):
    """max |diag(Q^{-1} T Q) - diag(T)| for the diagonal Q = diag(exp(log_weights)).

    BPRT's first change of basis (Definition 2.8) is diagonal, and so is this
    repository's entire weight family (leg 52's `kind='algebraic'/'geometric'`).  This
    is EXACTLY ZERO for every weight, which is the mechanism-level reason no weighted
    space can ever repair a zero diagonal.

    The weight is taken in LOG space and the ratio formed as `exp(lw_i - lw_j)`, the same
    convention as `solver.spectral_certificate.tail_inverse_norm`.  A first draft of this
    function took the weights directly, and a super-polynomial family overflowed to `inf`,
    producing `inf/inf = nan` -- which `max()` then silently skipped, reporting a clean
    `0.0` that was really a missing measurement.  The result is checked finite here rather
    than trusted (a NaN that reads as agreement is the worst kind of agreement).
    """
    T = np.asarray(T, float)
    lw = np.asarray(log_weights, float)
    with np.errstate(over="ignore", invalid="ignore"):
        Tc = T * np.exp(lw[:, None] - lw[None, :])
    return {
        "diagonal_move": float(np.max(np.abs(np.diag(Tc) - np.diag(T)))),
        "offdiagonal_finite_in_float64": bool(np.all(np.isfinite(Tc))),
    }


def dense_conjugation_moves_diagonal(T):
    """CONTROL for CDX5 (lesson 90): a NON-diagonal conjugation on the same matrix, via
    the same 'conjugate then read the diagonal' path.  It must report a nonzero move --
    otherwise CDX5's zero is a property of the code, not of diagonal similarity."""
    T = np.asarray(T, float)
    n = T.shape[0]
    P = RNG.normal(size=(n, n)) + 3.0 * np.eye(n)
    Tc = np.linalg.solve(P, T @ P)
    return float(np.max(np.abs(np.diag(Tc) - np.diag(T))))


def main():
    t0 = time.time()
    res = {
        "leg": 157,
        "route": "CDX",
        "primary_paper": "arXiv:2505.03091",
        "primary_url": "https://arxiv.org/abs/2505.03091",
        "primary_title": ("Cadiot, Stability analysis for localized solutions in PDEs and "
                          "nonlocal equations on R^m (6 May 2025, 30 pp.)"),
        "secondary_paper": "arXiv:2504.05066",
        "secondary_url": "https://arxiv.org/abs/2504.05066",
        "secondary_title": ("Breden, Payan, Reisch, Tang, Turing instability for nonlocal "
                            "heterogeneous reaction-diffusion systems: a computer-assisted "
                            "proof approach (7 Apr 2025, 25 pp., to appear Ann. Inst. "
                            "Fourier).  Cadiot's [15] -- a BACKWARD citation, which leg 62 "
                            "did not follow in its ledger."),
        "how_obtained": ("bash Papers/fetch.sh 2505.03091 2504.05066 -- egress probe HTTP "
                         "200; 1004 KB / 22 MB; text via `pdftotext -layout`.  Papers/ is "
                         "gitignored on purpose."),
    }

    # ---------------- CDX0: the novelty pass, carried forward ----------------
    res["CDX0_novelty"] = {
        "log": "writeup/novelty/leg_157.md",
        "committed_before_construction": True,
        "verdict": "PROCEED_AS_LITERATURE",
        "claims_mathematical_novelty": False,
        "the_pass_changed_this_legs_answer": True,
        "what_it_caught": ("This leg's headline candidate -- arXiv:2504.05066, reached as "
                           "Cadiot's backward citation [15] -- was drafted as 'never "
                           "consulted by this repository'.  The in-repo sweep falsified "
                           "that: reports/REPORT_2026-08-05.md ll. 219-223 records leg 62 "
                           "identifying it mid-cycle and relaying its operative reading to "
                           "leg 58 -- 'a \"zero diagonal\" framing would be falsifiable "
                           "against Breden-Payan-Reisch-Tang arXiv:2504.05066; the correct "
                           "framing is quantitative (off-diagonal row-sum growth vs. "
                           "diagonal growth)'.  What remains is bookkeeping: the paper was "
                           "never read at full text and is in no executable ledger."),
        "what_is_genuinely_added": [
            "arXiv:2504.05066 read at full text; Theorem 2.6 and both changes of basis "
            "located with verbatim hypotheses.",
            "Farid-Lancaster [FL91]'s hypotheses, which CP_NOT_OBTAINED records as never "
            "obtained (paywalled), are now known SECONDHAND from BPRT section 2.1.",
            "Cadiot's construction translated into this repository's A-shape language, "
            "with the A21 = 0 property measured rather than asserted.",
        ],
    }

    # ---------------- CDX1: located, never an abstract ----------------
    res["CDX1_located"] = {
        "constructions": CDX_CONSTRUCTIONS,
        "unlocated_rows": cdx_unlocated_rows(),
        "all_located": len(cdx_unlocated_rows()) == 0,
    }

    # ---------------- CDX2: the A-shape translation ----------------
    a21_zero = [r["tag"] for r in CDX_CONSTRUCTIONS if r["a21_is_zero"]]
    a21_nonzero = [r["tag"] for r in CDX_CONSTRUCTIONS if not r["a21_is_zero"]]
    res["CDX2_a_shape"] = {
        "constructions_whose_induced_A21_is_zero": a21_zero,
        "constructions_with_a_nonzero_off_diagonal": a21_nonzero,
        "reading": ("Every PRECONDITIONING construction in either paper induces an "
                    "approximate inverse with A21 = 0 -- the class leg 58's theorem "
                    "already proves Z_1 >= 1 on.  The single row with a nonzero "
                    "off-diagonal (SYSTEMS_ELIMINATION) is off-diagonal in the COMPONENT "
                    "index, is the bounded constant 1/9, and is an eigenvalue argument "
                    "rather than a certificate construction."),
    }

    # ---------------- CDX3: identity on the tail => A21 = 0 ----------------
    n, n_fin = 240, 24
    a21_measured = induced_a21_norm(n, n_fin, tail_is_identity=True)
    a21_control = induced_a21_norm(n, n_fin, tail_is_identity=False)
    res["CDX3_identity_tail"] = {
        "n": n, "n_finite": n_fin,
        "max_abs_A21_when_P_is_identity_on_the_tail": a21_measured,
        "max_abs_A21_control_when_P_is_not": a21_control,
        "control_reports_the_other_answer": bool(a21_control > 1e-6),
        "reading": ("`P = P_N + (I - Pi^N)` -- the shape BOTH papers use (Cadiot section "
                    "3; BPRT eq. (2.12)) -- induces an approximate inverse whose "
                    "tail-by-finite block is EXACTLY zero.  The control perturbs only P's "
                    "tail-by-finite block and the same code path reports a nonzero A21, "
                    "so the zero is a property of the construction and not of the code "
                    "(lesson 90)."),
    }

    # ---------------- CDX4: compact resolvent, the hypothesis that fails ----------------
    ours = compact_resolvent_ladder(lambda m: tail_block(K_SPLIT, m), MS)
    ctrl = compact_resolvent_ladder(_growing_diagonal, MS)
    res["CDX4_compact_resolvent"] = {
        "hypothesis": ("BPRT Theorem 2.6 (section 2.1): 'Let E a Banach space having a "
                       "Schauder basis and satisfying assumption (2.2), and L ... a "
                       "(possibly unbounded) linear operator.  Assume that L has a compact "
                       "resolvent.'  This is the ONLY non-automatic hypothesis, and it is "
                       "what replaces FL91's nonzero diagonal AND Cadiot's shift s."),
        "ours_a0_CLM_tail_block": ours,
        "positive_control_growing_diagonal": ctrl,
        "control_can_report_the_other_answer": bool(ctrl.get("saturates")),
        "reading": ("For a compact resolvent the eigenvalues must leave every bounded set, "
                    "so the count inside a fixed disc SATURATES.  The control (a diagonal "
                    "operator with a growing symbol -- Cadiot's Assumption 1 class, BPRT's "
                    "Weyl-law class) saturates at EVERY radius: the disc of radius r holds "
                    "exactly floor(r) eigenvalues no matter how far the truncation runs.  "
                    "Our tail block admits new eigenvalues into every fixed disc at a "
                    "steady rate per doubling of the truncation, while its smallest "
                    "eigenvalue modulus DECREASES monotonically -- the spectrum "
                    "accumulates rather than escaping.  So the resolvent is not compact, "
                    "and the one theorem in this lineage that needs no nonzero diagonal at "
                    "all is nevertheless unavailable to us.  Two hypotheses, two "
                    "independent failures: this is not the l_min obstruction again."),
    }

    # ---------------- CDX5: diagonal conjugation preserves the diagonal ----------------
    T = tail_block(K_SPLIT, 256)
    kk = np.arange(K_SPLIT + 1, 257, dtype=float)
    log_weight_families = {
        "algebraic_s_0.3": 0.3 * np.log1p(kk),
        "algebraic_s_1.0": 1.0 * np.log1p(kk),
        "geometric_1.05": kk * np.log(1.05),
        "BPRT_Definition_2.8_p_2": 2.0 * np.log(np.maximum(1.0, kk)),
        "factorial_super_polynomial": np.cumsum(np.log(kk)),
    }
    moves = {name: diagonal_conjugation_moves_diagonal(T, lw)
             for name, lw in log_weight_families.items()}
    dense_move = dense_conjugation_moves_diagonal(T)
    res["CDX5_diagonal_conjugation"] = {
        "per_weight_family": moves,
        "all_exactly_zero": bool(all(v["diagonal_move"] == 0.0 for v in moves.values())),
        "families_whose_offdiagonal_overflows_float64": [
            k for k, v in moves.items() if not v["offdiagonal_finite_in_float64"]],
        "note_on_the_overflow": (
            "The super-polynomial family's DIAGONAL move is exactly 0.0 like every other "
            "family -- exp(lw_i - lw_i) = 1 is exact -- but its OFF-diagonal entries "
            "overflow float64.  Recorded rather than hidden: it says a factorial-type "
            "weight, which is the only kind that could shrink this operator's Gershgorin "
            "radii, is not representable in this arithmetic anyway.  A first draft "
            "returned a bare NaN here, which `max()` silently skipped and reported as a "
            "clean 0.0 -- a missing measurement wearing the costume of agreement."),
        "control_dense_conjugation_move": dense_move,
        "control_reports_the_other_answer": bool(dense_move > 1e-6),
        "reading": ("A diagonal change of basis moves the diagonal by EXACTLY 0.0 in every "
                    "weight family tried, including BPRT's own Definition 2.8 and a "
                    "super-polynomial one this repository has never used.  A non-diagonal "
                    "conjugation on the same matrix through the same path moves it.  This "
                    "is the mechanism-level reason leg 52's weight search could not have "
                    "repaired a zero diagonal, and it is why BPRT's first change of basis "
                    "is not a candidate."),
    }

    # ---------------- CDX6: the gate ----------------
    suggests_untried_construction = bool(
        a21_nonzero and not all(r["a21_is_zero"] for r in CDX_CONSTRUCTIONS)
        and ours.get("saturates")
    )
    res["CDX6_gate"] = {
        "question": ("Does Cadiot arXiv:2505.03091, at full-text depth (including any "
                     "construction, remark, or forward citation it contains), suggest a "
                     "concrete alternative construction or adaptation applicable to the "
                     "A21 != 0 class that has not already been tried in this repository "
                     "(by leg 54's battery, leg 58's theorem, or leg 127's in-progress "
                     "work)?"),
        "answer": "yes" if suggests_untried_construction else "no",
        "pre_committed_no_branch": ("Cadiot's construction is confirmed to offer nothing "
                                    "beyond its own settled scope.  Bank the ledger entry; "
                                    "this closes the 'unmined literature' question for "
                                    "this specific source."),
        "why": ("Every preconditioning construction in the paper and in its most relevant "
                "citation induces A21 = 0 (CDX2, CDX3); the one theorem that drops the "
                "nonzero-diagonal hypothesis outright (BPRT Theorem 2.6) is an eigenvalue "
                "enclosure rather than an approximate inverse AND fails its own compact- "
                "resolvent hypothesis on our operator (CDX4); the diagonal change of basis "
                "provably cannot move a zero diagonal (CDX5); and the one genuinely "
                "shape-matching argument (SYSTEMS_ELIMINATION) confirms leg 127's chosen "
                "proof shape rather than supplying a new one."),
        "for_leg_127": ("RELAY, NOT ESCALATION.  Two things are worth leg 127's attention "
                        "and neither reverses a banked conclusion.  (1) Cadiot section 5.3 "
                        "/ Theorem 5.5 eq. (46) is a PUBLISHED WORKED INSTANCE of exactly "
                        "the two-direction elimination DIRECTION.md ### 127 proposes -- "
                        "the literature uses that shape, which is mild evidence the "
                        "approach is the right one.  (2) The mechanism-level statement "
                        "'no published construction in this lineage conjugates the TAIL' "
                        "(CDX3) is sharper than 'no published construction covers us', and "
                        "it localizes precisely where an A21 != 0 construction would have "
                        "to be original."),
    }

    res["ceiling"] = (
        "Two papers is not a corpus and a corpus is not a theorem.  Every quote is "
        "transcribed from a full text by a human-equivalent process and is exactly as good "
        "as that; every row carries its URL so the next pass can check rather than trust.  "
        "All numbers are float64 measurements of finite truncations, no intervals.  "
        "Farid-Lancaster [FL91] is STILL NOT OBTAINED -- its hypotheses are now known only "
        "secondhand, from BPRT section 2.1, and that is recorded rather than glossed.  This "
        "leg builds and tests NO construction (its gate forbids it), is not evidence FOR "
        "leg 58's proposition, does not reopen leg 62's NO, and does not lift any standing "
        "ban.  No link of the L1->L4 chain moved."
    )

    res["elapsed_s"] = round(time.time() - t0, 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(f"wrote {OUT}  ({res['elapsed_s']} s)")
    print(f"  CDX3 A21 (P identity on tail) : {a21_measured:.3e}   "
          f"control {a21_control:.3e}")
    for r, blk in ours["per_radius"].items():
        print(f"  CDX4 ours    {r:<8} {blk['count_in_disc']}  "
              f"+{blk['new_eigenvalues_per_doubling']:.2f}/doubling  "
              f"saturates={blk['saturates']}")
    for r, blk in ctrl["per_radius"].items():
        print(f"  CDX4 control {r:<8} {blk['count_in_disc']}  "
              f"saturates={blk['saturates']}")
    print(f"  CDX4 ours min|eig| : {[round(v, 4) for v in ours['min_abs_eigenvalue']]}")
    print(f"  CDX5 diagonal move : "
          f"{ {k: v['diagonal_move'] for k, v in moves.items()} }  "
          f"control {dense_move:.3e}")
    print(f"  GATE: {res['CDX6_gate']['answer']}")
    return res


if __name__ == "__main__":
    main()
