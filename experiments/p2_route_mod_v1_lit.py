"""P2 Route-MOD v1 -- leg 181: what does Xu arXiv:2607.19762's "gap 1/2 AFTER MODULATION"
actually require, and does the modulation move transfer to anything this repository built?

A LITERATURE leg. It builds no solver module, MUTATES none, edits none, touches no shared
ledger, lifts no ban, promotes no route and moves no link of the `L1 -> L4` chain.
`solver/spectral_certificate.py` is imported READ-ONLY (leg 127's territory, closed on
landing) and must be byte-identical to `origin/main`; nothing here writes to it.

THE GATE, verbatim from `DIRECTION.md` leg 181:

    "Does Xu's modulation technique, read at full-text depth, apply (as stated, or via a
     straightforward adaptation) to any operator/space combination this repository has
     already built, beyond origin-H^2?"

    ANSWER: YES -- and in a stronger and more useful sense than the gate anticipated. It
    does not merely "apply": it is ALREADY APPLIED, in two places, and one of them is the
    `ell^1_w` line the leg was sent to ask about.

      (T1) `solver/energy_coercivity.py`'s weighted-`L^2_phi` sine realization already runs
           it -- `coercivity_gap(..., modulate=True)` quotients `span{sin theta,
           sin 2theta}`, which is exactly Xu's two symmetry modes, over a seven-weight
           family. Already banked; recorded here, not re-claimed.

      (T2) `solver/spectral_certificate.py`'s `ell^1_w` line already carries HALF of it, and
           has since leg 51, WITHOUT ANYONE NOTICING. `bordered_linearization`'s GAUGE ROW
           is `sum_k k b_k`, which in the odd sine basis IS the first origin derivative
           `v'(0)` -- Xu's second Taylor functional, eq (A.13) sec A.4 p.37 -- and the
           module's own docstring says it "removes the exact zero eigenvalue the dilation
           symmetry puts there", i.e. Xu's lambda = 0 scaling mode. So leg 127's
           `Z_1 >= 1` is a theorem about an ALREADY-PARTIALLY-MODULATED object. And that
           half of the projection is UNBOUNDED on the space for every `s < 1` -- exactly
           and only the range leg 127's theorem lives in (check C1).

      (T2b) WHETHER THE REMAINING HALF HELPS IS OPEN, and this leg opened it rather than
           closing it: the check pre-registered to decide it failed, for instrument reasons
           recorded in full below. Escalated.

      (T3) Route-D's two-grading weighted-Holder space is the one UNDECIDED candidate, and
           the only one not already capped by Xu's own sec 8 no-go. Escalated.

    Per the gate's yes-branch this leg RECORDS AND ESCALATES. It builds and tests nothing
    of its own.

WHAT MODULATION COSTS, read at full-text depth (the leg's first job):

    NOTHING, and it buys nothing beyond deleting two already-known eigenvalues. It is not
    Xu's technique -- he calls it "the standard modulation" every time and credits the
    method to Elgindi-Ghoul-Masmoudi [15] (sec 1, p. 2). It is a rank-2 projection onto the
    two origin Taylor functionals, eq (A.13). Its ONE structural prerequisite is that those
    two functionals be BOUNDED on the realization, and Xu supplies his own worked failure of
    that (`Y_theta`, Definition A.2 -- banked by leg 171, cited not claimed here). And the
    clause that WOULD carry weight, the dynamic modulation closure, is EXPLICITLY OPEN
    (sec 8, p. 33; sec 6.1, p. 31) -- which no file in this repository had recorded.

THE CRITERION (this leg's own one-line abstraction of (A.13) + Def A.2 + sec A.4; Xu
nowhere states it as a criterion, and it is claimed as new to THIS REPOSITORY only):

    Modulation is available on a realization `Z` of this operator IFF
      (a) the two exact symmetry modes `y Omega'` and `Omega + c_l y Omega'` lie in `Z`, and
      (b) the two origin Taylor functionals `v -> v(0)` and `v -> v'(0)` are BOUNDED on `Z`.

WHY IT IS A SCRIPT AND NOT ONLY PROSE (lesson 68; the leg-57/65/112/141/171 pattern):

  (1) VERBATIM PRESENCE. Every quote the verdict rests on is re-located in the actual PDF
      text at run time by whitespace- and non-ASCII-insensitive substring match, so a
      misquote fails loudly instead of decaying at the rate of memory. `Papers/` is
      gitignored, so when the PDF is absent the flags are read back from the committed JSON
      and clearly LABELLED as such -- never silently defaulted to True.

  (2) NEGATIVE LOCATORS (lesson 90 -- a control that cannot come out differently is not a
      control). Five fragments that must NOT be in the paper. Declared in
      `writeup/novelty/leg_181.md` sec 4 BEFORE they were coded.

  (3) THE CRITERION, EVALUATED, IN A FORM THAT CAN REPORT THE OTHER ANSWER. Three
      arithmetic checks, all pre-registered in the novelty pass with their predictions:
        C1  criterion (b) for `ell^1_w`, `w_k = (1+k)^s`: the dual norm of `v'(0)` is
            `sup_k k/(1+k)^s`. PREDICTED finite iff `s >= 1`. If it came out finite at
            `s = 0.3` this leg's reading would be wrong.
        C2  the `s = 1` crossing is the SAME crossing `fredholm_sides` already measures --
            the cokernel functional grows like `m`, i.e. at the same rate as `v'(0)`.
            PREDICTED kernel exponent ~ -2, cokernel exponent ~ +1.
        C3  the no-op test -- FAILED ITS OWN PRE-REGISTRATION, IN BOTH NUMBERS, and is kept
            and marked INCONCLUSIVE rather than deleted or laundered (lesson 76). Predicted
            that the worst column of `M_K^{-1}` carries negligible `ell^1_w` mass on the
            modulation span and that removing the span leaves the constant unchanged;
            measured 66% and a 92x collapse. Interrogation (lesson 90) showed the
            instrument is not measuring the certificate's constant -- the domain-only
            quotient is OVERDETERMINED, so `pinv` returns a least-squares number, and the
            dimensionally comparable two-sided compression `Q L Q` is EXACTLY SINGULAR. So
            C3 decides nothing in either direction, THIS LEG'S VERDICT DOES NOT REST ON IT,
            and its real output is the new escalation T2b.

    bash Papers/fetch.sh 2607.19762
    .venv/bin/python experiments/p2_route_mod_v1_lit.py
        -> writeup/data/p2_route_mod_v1_lit.json

NO FIGURE: no measurement of a curve of this repository's own; every number here is Xu's,
arithmetic on Xu's, or a read-only evaluation of an existing module ("no measurement, no
figure", the convention legs 141 and 171 used).

CEILING (pre-committed). Literature-only. No link of `L1 -> L4` moves from anything here.
The `ell^1_w` finding NARROWS leg 127 -- it says what leg 127's theorem is a theorem ABOUT --
and reverses nothing banked.

VERSION ACTUALLY READ (recorded because a version mismatch silently invalidates a locator):
arXiv:2607.19762v1, 22 Jul 2026, physics.flu-dyn, 41 pp -- the version this repository
already cites in `capabilities.py`, in leg 127's journal and in legs 171/173.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

OUT = ROOT / "writeup" / "data" / "p2_route_mod_v1_lit.json"
PAPERS = ROOT / "Papers"
ARXIV = "2607.19762"
VERSION_READ = "arXiv:2607.19762v1, 22 Jul 2026, physics.flu-dyn, 41 pp"

GATE = ("Does Xu's modulation technique, read at full-text depth, apply (as stated, or via "
        "a straightforward adaptation) to any operator/space combination this repository "
        "has already built, beyond origin-H^2?")

GATE_ANSWER = "YES"

GATE_YES_BRANCH_VERBATIM = (
    "Name the target and what modulation would require precisely, escalate as a candidate "
    "scoping question for a later leg.")


# ---------------------------------------------------------------------------
# 1. THE QUOTES.  `fragment` is re-located in the PDF at run time.
# ---------------------------------------------------------------------------
QUOTES = [
    {
        "id": "Q1-ABSTRACT-HEADLINE",
        "where": "Abstract, p. 1",
        "quote": ("removing these by the standard modulation leaves a spectral gap of 1/2 "
                  "on X"),
        "fragment": "removing these by the standard modulation leaves a spectral gap of",
        "reading": ("THE sentence legs 127/163 have been citing. Note what it does NOT say: "
                    "it does not say a hypothesis is added, and it does not say anything "
                    "dynamical. 'these' are the two point-spectrum modes just named."),
        "new_to_this_repo": False,
        "already_banked_by": "leg 127 journal l. 32-38; solver/energy_coercivity.py (K1)/(K2)",
    },
    {
        "id": "Q2-STANDARD-NOT-XUS",
        "where": "Section 1, p. 2",
        "quote": ("Inviscid stable self-similar blow-up for this family of nonlocal "
                  "transport models was proved by Elgindi, Ghoul, and Masmoudi [15] using "
                  "modulation, near a known family of self-similar solutions"),
        "fragment": ("proved by Elgindi, Ghoul, and Masmoudi [15] using modulation, near a "
                     "known family of self-similar solutions"),
        "reading": ("There is NO 'Xu modulation technique'. Xu attributes the method, and "
                    "calls it 'the standard modulation' at every one of its three "
                    "appearances. This leg therefore cannot make a novel-technique claim, "
                    "and its question reduces to 'does the move help anywhere here'."),
        "new_to_this_repo": True,
        "already_banked_by": None,
    },
    {
        "id": "Q3-WHAT-IS-MODULATED",
        "where": "Section 3.2 ('The two symmetry modes and the numerical spectrum'), p. 10",
        "quote": ("They are modded out by the standard modulation (choosing the collapse "
                  "time and spatial scale) and do not represent instability."),
        "fragment": ("They are modded out by the standard modulation (choosing the collapse "
                     "time and spatial scale) and do not represent instability."),
        "reading": ("WHAT IS BEING MODULATED, in one sentence: the two free parameters of "
                    "the self-similar ansatz -- the collapse time T and the spatial scale. "
                    "Not the operator, not the space, not the norm. The two parameters "
                    "generate the two eigenmodes at lambda = +1 (time shift) and "
                    "lambda = 0 (scaling)."),
        "new_to_this_repo": True,
        "already_banked_by": None,
    },
    {
        "id": "Q4-THE-MODES-ARE-EXACT",
        "where": "Section 3.2, p. 10",
        "quote": ("every term cancels and La (y Omega') = 0; ... hence La (Omega + cl y "
                  "Omega') = Omega + cl y Omega'"),
        "fragment": "every term cancels and",
        "reading": ("COST #1: the two modes must be EXACT and EXPLICIT. Xu proves both by "
                    "direct substitution, using admissibility (H1)/(H3) (which give "
                    "Omega' in L^1 with integral zero) and the profile equation itself. "
                    "This is cheap for THIS operator and is not a restriction in practice, "
                    "because the same two modes exist for every admissible profile."),
        "new_to_this_repo": True,
        "already_banked_by": ("the modes themselves are banked -- solver/energy_coercivity.py "
                              "(K1): L sin 2theta = 0 and L(sin theta + sin 2theta/2) = "
                              "itself. What is new is that they are exact for ALL admissible "
                              "a, not only a = 0."),
    },
    {
        "id": "Q5-THE-PROJECTION-ITSELF",
        "where": "eq (A.13), Section A.4, p. 37",
        "quote": ("Thus Q is the regular part at the collapse point: it removes the zeroth "
                  "and first Taylor coefficients of v at y = 0, matching the "
                  "origin-regularity mechanism of the realization X of Theorem 1."),
        "fragment": ("Thus Q is the regular part at the collapse point: it removes the "
                     "zeroth and first Taylor coefficients of v at y = 0"),
        "reading": ("WHAT MODULATION IS, AS AN OPERATOR -- and no file in this repository "
                    "had written it down. P v = v(0) + v'(0) y, Q v = v - v(0) - v'(0) y. "
                    "A RANK-2 PROJECTION ONTO THE TWO ORIGIN TAYLOR FUNCTIONALS. That is "
                    "the whole technique."),
        "new_to_this_repo": True,
        "already_banked_by": None,
    },
    {
        "id": "Q6-THE-ONE-PREREQUISITE",
        "where": "Definition A.2, Section A.4, p. 37",
        "quote": ("Because the weight y^{-2theta-1} blows up at the origin, elements of "
                  "Y_theta carry no pointwise origin traces; the modulation projection is "
                  "therefore defined on the physical X (which has traces) and mapped into "
                  "Y_theta, not applied within Y_theta"),
        "fragment": ("carry no pointwise origin traces; the modulation projection is "
                     "therefore defined on the physical X (which has traces)"),
        "reading": ("COST #2, AND THE ONLY STRUCTURAL ONE: the realization must carry the "
                    "two origin TRACES, or the projection is not even defined on it. Xu "
                    "supplies his own worked failure case. This is the sentence the "
                    "criterion in this leg's docstring abstracts."),
        "new_to_this_repo": False,
        "already_banked_by": ("leg 171, experiments/p2_route_xul_v1_lit.py entry S5-Y-THETA "
                              "hypothesis (c). CITED, NOT CLAIMED."),
    },
    {
        "id": "Q7-THE-TRANSFER-COST",
        "where": "Section A.4, p. 39",
        "quote": ("Since elements of Y_theta carry no origin traces, the "
                  "modulation-complement Q of Section A.1 cannot act inside Y_theta; it "
                  "acts on the physical X, which has traces, and lands in Y_theta."),
        "fragment": "the modulation-complement Q of Section A.1 cannot act inside",
        "reading": ("COST #3: when (b) fails you need a bounded transfer map J_X : X -> "
                    "script-Y_{3/2}, which costs a constant C_Q (not 1), forces theta in "
                    "(1, 2) because of 'the two integrable subtracted terms', and needs a "
                    "double Hardy inequality on the core. That is the 'extra computational "
                    "machinery' the leg spec asked about, and it is the ONLY machinery."),
        "new_to_this_repo": False,
        "already_banked_by": "leg 171, S5-Y-THETA hypothesis (c). CITED, NOT CLAIMED.",
    },
    {
        "id": "Q8-SUBTRACTS-TWO-COEFFICIENTS",
        "where": "Section A.4, p. 39",
        "quote": ("subtracting the two symmetry Taylor coefficients that phi in X possesses "
                  "(phi is C^1 with phi(0) = 0, and v_pm = M_pm phi_pm has a value and a "
                  "first derivative at 0)"),
        "fragment": "subtracting the two symmetry Taylor coefficients",
        "reading": ("The parenthesis matters for the transfer to THIS repository's odd "
                    "realizations: on the physical odd space phi(0) = 0 holds "
                    "AUTOMATICALLY, so the non-trivial functional is the FIRST ORIGIN "
                    "DERIVATIVE. Xu's rank-2 count is per Hardy block on the CONJUGATED "
                    "variable v = b^2 u; it is not two independent conditions on the "
                    "physical odd function."),
        "new_to_this_repo": True,
        "already_banked_by": None,
    },
    {
        "id": "Q9-CLOSURE-IS-OPEN",
        "where": "Section 8 (closing discussion), p. 33",
        "quote": ("Three inputs are still missing, and none is supplied here: a lower bound "
                  "for the dissipation form in the Y_theta norm, a quadratic estimate for "
                  "N(phi) = phi H phi in the same norm, and the modulation closure that "
                  "removes the two symmetry directions along the flow"),
        "fragment": ("and the modulation closure that removes the two symmetry directions "
                     "along the flow"),
        "reading": ("THE FINDING THAT CORRECTS THIS REPOSITORY'S OWN CITATION HABIT. 'gap "
                    "1/2 after modulation' is a STATIC statement -- the spectrum minus two "
                    "known points. The DYNAMIC modulation closure, the thing that would "
                    "make 'after modulation' mean anything, is one of three inputs Xu "
                    "explicitly does not supply. No file in this repository records this."),
        "new_to_this_repo": True,
        "already_banked_by": None,
    },
    {
        "id": "Q10-CLOSURE-IS-OPEN-AGAIN",
        "where": "Section 6.1, p. 31",
        "quote": ("the required weighted dissipation-form bound, nonlinear estimate, and "
                  "modulation closure are open, Appendix A"),
        "fragment": ("modulation closure are open"),
        "reading": ("Q9 restated in a second, independent place in the paper, so the "
                    "reading does not rest on one sentence."),
        "new_to_this_repo": True,
        "already_banked_by": None,
    },
    {
        "id": "Q11-COERCIVITY-NOGO-CAPS-T1",
        "where": "Section 8, p. 34",
        "quote": ("no coercivity certificate in an L^2-equivalent norm reaches the spectral "
                  "gap"),
        "fragment": "coercivity certificate in an L",
        "reading": ("Why target T1 (energy_coercivity's weighted-L^2_phi) is APPLICABLE but "
                    "CAPPED: modulation runs there, and Xu's own no-go says the lane it "
                    "runs in cannot reach the gap regardless. So T1 is not a scoping "
                    "question for a later leg -- it is closed from both ends."),
        "new_to_this_repo": False,
        "already_banked_by": "leg 141 (Route-WEL). CITED, NOT CLAIMED.",
    },
]

# Fragments that must NOT be in the paper (lesson 90).  Declared in
# writeup/novelty/leg_181.md sec 4 BEFORE they were coded.
NEGATIVE = [
    {
        "id": "N1-NO-WEIGHTED-SEQUENCE-SPACE",
        "fragment": "weighted sequence space",
        "why": ("`ell^1_w` is THIS repository's space, not Xu's. If this ever relocates, the "
                "whole framing of legs 127/163/171/181 is wrong."),
    },
    {
        "id": "N2-CLOSURE-NOT-CLAIMED-PROVED",
        "fragment": "we prove the modulation closure",
        "why": "Q9/Q10 say the closure is OPEN. A claim that it is proved would contradict.",
    },
    {
        "id": "N3-MODULATION-NOT-XUS-CONTRIBUTION",
        "fragment": "our modulation technique",
        "why": ("Q2 says the technique is standard and attributed. If Xu claimed it, the "
                "leg's central 'nothing to transfer' reading would be wrong."),
    },
    {
        "id": "N4-NOT-IN-THE-RADII-POLYNOMIAL-LANE",
        "fragment": "radii polynomial",
        "why": ("Xu is not in this repository's certification lane at all; the transfer "
                "question is ours to ask, and nobody has answered it for us."),
    },
    {
        "id": "N5-NO-GENERAL-BOUNDEDNESS-CLAIM",
        "fragment": "the modulation projection is bounded on",
        "why": ("Xu states boundedness only for the specific transfer J_X : X -> "
                "script-Y_{3/2}, never in general. The criterion in this leg is OURS, "
                "abstracted from his worked cases, and must not be attributed to him."),
    },
]


# ---------------------------------------------------------------------------
# 2. LOCATOR MACHINERY
# ---------------------------------------------------------------------------
def _normalize(text):
    """ASCII-only, whitespace-free.  Robust to pdftotext's line breaks, ligatures and the
    unicode primes/thetas that would otherwise make every fragment a coin flip."""
    ascii_only = "".join(ch for ch in text if ord(ch) < 128)
    return re.sub(r"\s+", "", ascii_only)


def _pdf_text():
    """Extract the PDF once.  Returns None when Papers/ is empty (it is gitignored)."""
    pdf = PAPERS / f"{ARXIV}.pdf"
    if not pdf.exists():
        return None
    try:
        r = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                           capture_output=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", errors="replace")


def locate(entries, text, prior):
    """Re-locate every fragment.  When the PDF is absent, read the flag back from the
    committed JSON and LABEL it -- never silently default to True."""
    out = []
    norm = _normalize(text) if text is not None else None
    for e in entries:
        rec = dict(e)
        if norm is None:
            was = prior.get(e["id"])
            rec["located"] = was
            rec["located_source"] = ("READ BACK FROM COMMITTED JSON -- Papers/ is gitignored "
                                     "and the PDF is absent; NOT verified this run")
        else:
            rec["located"] = _normalize(e["fragment"]) in norm
            rec["located_source"] = "VERIFIED THIS RUN against Papers/%s.pdf" % ARXIV
        out.append(rec)
    return out


# ---------------------------------------------------------------------------
# 3. THE CRITERION, EVALUATED
# ---------------------------------------------------------------------------
def c1_trace_functional_dual_norm(s_values=(0.0, 0.3, 0.7, 0.9, 1.0, 1.5),
                                  ladders=(64, 256, 1024, 4096)):
    """C1 -- criterion (b) for `ell^1_w`, `w_k = (1+k)^s`.

    In the odd sine basis `v = sum_k b_k sin k theta` on the compactified variable, the two
    origin Taylor functionals of eq (A.13) are

        v(0)  = 0                (identically, by oddness -- FREE, costs nothing)
        v'(0) = sum_k k b_k      (Xu's second functional)

    and the dual norm of the second on `ell^1_w` is `sup_k k / (1+k)^s`.

    PRE-REGISTERED PREDICTION (writeup/novelty/leg_181.md sec 4.3): finite iff `s >= 1`.
    The ladder is what makes it falsifiable -- a finite sup would stop growing with K.
    """
    rows = []
    for s in s_values:
        vals = []
        for K in ladders:
            k = np.arange(1, K + 1, dtype=float)
            vals.append(float(np.max(k / (1.0 + k) ** s)))
        growth = vals[-1] / vals[-2] if vals[-2] > 0 else float("nan")
        rows.append({
            "s": float(s),
            "dual_norm_by_K": {str(K): v for K, v in zip(ladders, vals)},
            "ratio_last_two_K": float(growth),
            "saturates": bool(growth < 1.05),
            "predicted_finite": bool(s >= 1.0),
        })
    agrees = all(r["saturates"] == r["predicted_finite"] for r in rows)
    return {
        "rows": rows,
        "prediction": "finite iff s >= 1",
        "prediction_holds": bool(agrees),
        "reading": ("Xu's modulation projection is UNBOUNDED on `ell^1_w` for every s < 1 -- "
                    "which is exactly and only the range in which leg 127's `Z_1 >= 1` "
                    "lives -- and bounded for s >= 1, which is exactly the range in which "
                    "leg 127's obstruction (the tail kernel) has already LEFT the space. "
                    "Modulation and the obstruction sit on opposite sides of s = 1."),
    }


def c2_same_crossing(K=64, M=3136):
    """C2 -- the `s = 1` crossing of C1 is the SAME crossing `fredholm_sides` already
    measures. READ-ONLY use of solver/spectral_certificate.py.

    PRE-REGISTERED PREDICTION: kernel exponent ~ -2, cokernel exponent ~ +1, crossing 1.0.
    The cokernel functional growing like `m` is the same growth rate as `v'(0)`'s weights.
    """
    from solver.spectral_certificate import fredholm_sides
    fs = fredholm_sides(K=K, M=M)
    return {
        "fredholm_sides": {k: (float(v) if isinstance(v, (int, float)) else v)
                           for k, v in fs.items()},
        "predicted_kernel_exponent": -2.0,
        "predicted_cokernel_exponent": 1.0,
        "kernel_matches": bool(abs(fs["kernel_exponent"] - (-2.0)) < 0.25),
        "cokernel_matches": bool(abs(fs["cokernel_exponent"] - 1.0) < 0.25),
        "reading": ("The cokernel functional grows like `m`, i.e. at the SAME rate as the "
                    "weights of `v'(0) = sum_k k b_k`. Xu's modulation functional and this "
                    "repository's cokernel functional are the same growth class, so they "
                    "enter the dual at the same exponent. `s = 1` is not a coincidence of "
                    "two separate facts; it is one fact seen twice."),
    }


def c3_no_op_test(K=96, s=0.3):
    """C3 -- the no-op test. IT FAILED ITS OWN PRE-REGISTRATION, IN BOTH NUMBERS, AND IT IS
    KEPT (lesson 76) AND MARKED INCONCLUSIVE RATHER THAN LAUNDERED OR DELETED.

    WHAT IT WAS SUPPOSED TO DO. `||M_K^{-1}||_w` is a max over COLUMNS of the weighted
    inverse, so the column realizing it is the direction the certificate constant is worst
    in. Two numbers:

      (i)  the fraction of that direction's `ell^1_w` mass carried by `span{e_1, e_2}` --
           the modulation span, since the two symmetry modes are `e_2` (lambda = 0) and
           `e_1 + e_2/2` (lambda = 1) in this basis (solver/energy_coercivity.py (K1));
      (ii) `||.||_w` of `L` RESTRICTED TO THE MODULATED DOMAIN `L|_{QX}` -- columns 1 and 2
           deleted, every equation kept -- which is the SECOND half of modulation, the half
           the gauge row does NOT already do. Modulation quotients the DOMAIN; it does not
           discard equations, so the restriction is rectangular and the constant is read off
           the pseudo-inverse.

    PRE-REGISTERED PREDICTION (writeup/novelty/leg_181.md sec 4.3): (i) negligible,
    (ii) essentially unchanged.

    WHAT ACTUALLY HAPPENED: (i) came out at ~66%, not <5%. (ii) collapsed by ~92x, not ~1x.
    Both predictions are WRONG as stated.

    WHY THE CHECK IS NEVERTHELESS INCONCLUSIVE, AND NOT A VERDICT FLIP. Interrogating the
    two numbers rather than banking them (lesson 90, and leg 127's own `mu = 0` coincidence
    is the precedent):

      * (ii) IS NOT THE CERTIFICATE'S CONSTANT. Modulation quotients the DOMAIN, so
        dropping two columns while keeping every equation leaves an OVERDETERMINED system:
        `pinv` then returns a LEAST-SQUARES constant, which does not solve anything and is
        not comparable to `||M_K^{-1}||_w`. Its smallness says the tall system is
        well-conditioned in the least-squares sense; it says nothing about invertibility.
      * THE TWO-SIDED COMPRESSION IS WORSE, NOT BETTER. `Q L Q` -- dropping rows 1 and 2 as
        well, so the system stays square -- is EXACTLY SINGULAR (rank deficient, flagged
        below). So the one form of the question that IS dimensionally comparable answers
        "modulation destroys invertibility here", which is also not a repair.
      * (i) IS NOT NECESSARILY LEG 127's WITNESS. `||M_K^{-1}||_w`'s argmax column is the
        direction of the `||A||` constant at one `(K, s)`; identifying it with leg 127's
        `sigma_min` near-null direction would need leg 127's own instrument, which is
        outside this leg's territory. The 66% is reported as a measurement and is NOT read
        as a statement about leg 127's obstruction.

    CONSEQUENCE: C3 decides nothing, in either direction, and this leg's verdict does NOT
    rest on it. The verdict rests on C1, C2 and the gauge-row identity, all three of which
    are closed-form or exact. C3's real output is a NEW, PROPERLY-POSED QUESTION, escalated
    as T2b: what IS the right finite-dimensional realization of "quotient the lambda = 1
    mode" inside a weighted-`ell^1` radii-polynomial certificate, given that the naive
    domain-only form is overdetermined and the naive two-sided form is singular?

    READ-ONLY: imports `bordered_linearization` and `log_weight_vector` and mutates neither.
    """
    from solver.spectral_certificate import bordered_linearization, log_weight_vector

    def wnorm_and_witness(mat, lw):
        scaled = mat * np.exp(lw[:, None] - lw[None, :])
        inv = np.linalg.inv(scaled)
        colsums = np.abs(inv).sum(0)
        j = int(np.argmax(colsums))
        return float(colsums[j]), inv[:, j], j

    Mfull = bordered_linearization(K)
    lw = np.concatenate([log_weight_vector(K, "algebraic", s), [0.0]])
    norm_full, witness, jstar = wnorm_and_witness(Mfull, lw)

    mass = np.abs(witness)
    total = float(mass.sum())
    mass_on_span = float(mass[0] + mass[1])          # modes 1 and 2 == the modulation span

    # modulation quotients the DOMAIN: drop columns 1 and 2, keep every equation.
    keep = np.array([j for j in range(K + 1) if j not in (0, 1)])
    scaled_full = Mfull * np.exp(lw[:, None] - lw[None, :])
    S = scaled_full[:, keep]
    norm_mod = float(np.max(np.abs(np.linalg.pinv(S)).sum(0)))

    # the aside: the two-sided compression, recorded because it is a trap
    two_sided = Mfull[np.ix_(keep, keep)] * np.exp(lw[keep][:, None] - lw[keep][None, :])
    two_sided_singular = bool(
        np.linalg.matrix_rank(two_sided) < min(two_sided.shape))

    return {
        "K": int(K), "s": float(s),
        "argmax_column": jstar,
        "norm_unmodulated": norm_full,
        "norm_modulated_domain_restricted": norm_mod,
        "ratio_modulated_over_unmodulated": float(norm_mod / norm_full),
        "two_sided_compression_QLQ_is_singular": two_sided_singular,
        "witness_l1w_mass_on_modulation_span": mass_on_span,
        "witness_l1w_mass_total": total,
        "witness_mass_fraction_on_span": float(mass_on_span / total),
        "prediction_span_fraction_negligible": bool(mass_on_span / total < 0.05),
        "prediction_norm_essentially_unchanged": bool(0.5 < norm_mod / norm_full < 2.0),
        "both_predictions_held": bool(
            (mass_on_span / total < 0.05) and (0.5 < norm_mod / norm_full < 2.0)),
        "verdict": "INCONCLUSIVE -- BOTH PRE-REGISTERED PREDICTIONS FAILED, AND THE "
                   "INSTRUMENT IS NOT MEASURING THE CERTIFICATE'S CONSTANT",
        "reading": ("Kept, not deleted (lesson 76). The domain-only restriction is "
                    "OVERDETERMINED, so its `pinv` constant is a least-squares number and "
                    "is not comparable to `||M_K^{-1}||_w`; the dimensionally comparable "
                    "form, the two-sided compression `Q L Q`, is EXACTLY SINGULAR. So "
                    "neither number is evidence that modulation repairs the `ell^1_w` "
                    "object, and neither is evidence that it does not. This leg's verdict "
                    "rests on C1, C2 and the gauge-row identity instead. The real output "
                    "is escalation T2b: what the right finite-dimensional realization of "
                    "'quotient the lambda = 1 mode' inside a weighted-`ell^1` "
                    "radii-polynomial certificate even is."),
    }


def gauge_row_is_xus_functional(K=8):
    """THE CENTRAL STRUCTURAL FINDING, made checkable rather than asserted.

    `bordered_linearization`'s gauge row is `M[K][k-1] = k`, i.e. the functional
    `b -> sum_k k b_k`. In the odd sine basis that IS `v'(0)`, Xu's second Taylor
    functional of eq (A.13). The module's own docstring says the row "removes the exact
    zero eigenvalue the dilation symmetry puts there" -- Xu's lambda = 0 scaling mode.

    So the `ell^1_w` line has been carrying HALF of Xu's modulation projection since
    leg 51, and leg 127's `Z_1 >= 1` is a theorem about an already-partially-modulated
    object. READ-ONLY.
    """
    from solver.spectral_certificate import bordered_linearization
    M = bordered_linearization(K)
    row = np.asarray(M)[K, :K]
    expected = np.arange(1, K + 1, dtype=float)
    return {
        "gauge_row": [float(x) for x in row],
        "expected_v_prime_at_origin_coefficients": [float(x) for x in expected],
        "max_abs_deviation": float(np.max(np.abs(row - expected))),
        "is_exactly_v_prime_at_origin": bool(np.array_equal(row, expected)),
        "reading": ("Character for character, the gauge row is `v'(0)`. This is not an "
                    "analogy: it is the same linear functional, and the module's own "
                    "docstring already says which symmetry mode it removes."),
    }


# ---------------------------------------------------------------------------
# 4. THE TARGETS, AND THE ESCALATION
# ---------------------------------------------------------------------------
TARGETS = [
    {
        "id": "T1-WEIGHTED-L2-COERCIVITY",
        "target": "solver/energy_coercivity.py -- the weighted-`L^2_phi` odd sine realization",
        "criterion_a_modes_in_space": ("YES. Both modes are `span{sin theta, sin 2theta}` and "
                                       "the admissibility check (gamma < 3) keeps them in "
                                       "every weight of the named seven-weight family."),
        "criterion_b_traces_bounded": ("YES, trivially: the trial space is the "
                                       "finite-dimensional `span{sin 1..sin N}`, on which "
                                       "every linear functional is bounded."),
        "verdict": "APPLIES -- AND IS ALREADY IMPLEMENTED",
        "status": "NOT A SCOPING QUESTION. Closed from both ends.",
        "detail": ("`coercivity_gap(..., modulate=True)` already quotients the two modes by "
                   "the `G`-orthogonal complement, and its own docstring calls this 'the "
                   "modulation Xu's 1/2 refers to'. And Xu sec 8 p. 34 (Q11) independently "
                   "caps the lane: no coercivity certificate in an `L^2`-equivalent norm "
                   "reaches the gap. So there is nothing for a later leg to do here."),
        "escalate": False,
    },
    {
        "id": "T2-ELL1W",
        "target": ("solver/spectral_certificate.py -- the `ell^1_w` line, "
                   "`w_k = (1+k)^s`, where leg 127 proved `Z_1 >= 1` unconditionally"),
        "criterion_a_modes_in_space": ("YES. `e_2` and `e_1 + e_2/2` are finitely supported, "
                                       "hence in `ell^1_w` for every `s`."),
        "criterion_b_traces_bounded": ("SPLIT, AND THIS IS THE ANSWER. `v(0) = 0` identically "
                                       "by oddness, so that half is free. `v'(0) = sum_k k "
                                       "b_k` has dual norm `sup_k k/(1+k)^s`, FINITE IFF "
                                       "`s >= 1` (check C1) -- and leg 127's theorem lives "
                                       "at `s < 1`."),
        "verdict": ("APPLIES, AND HALF OF IT HAS BEEN APPLIED SINCE LEG 51 WITHOUT ANYONE "
                    "NOTICING. `bordered_linearization`'s GAUGE ROW IS `v'(0)`, character "
                    "for character (exact check, deviation 0.0), and its own docstring says "
                    "it removes the eigenvalue the dilation symmetry puts there -- Xu's "
                    "lambda = 0 scaling mode. Leg 127's `Z_1 >= 1` is therefore a theorem "
                    "about an ALREADY-PARTIALLY-MODULATED object."),
        "status": ("BANKED AS A NARROWING OF LEG 127 -- nothing banked is reversed; what "
                   "changes is what leg 127's theorem is a theorem ABOUT. The SECOND half "
                   "(the lambda = 1 mode) is UNDECIDED and is escalated as T2b."),
        "detail": ("Two solid findings and one honest non-finding. SOLID (1): the gauge-row "
                   "identity above -- exact, not an analogy. SOLID (2): `v'(0)` is UNBOUNDED "
                   "on `ell^1_w` for every `s < 1` (check C1, closed form, ladder-verified "
                   "to K = 4096), which is exactly and only the range leg 127's theorem "
                   "lives in; and at `s >= 1`, where it becomes bounded, the obstruction "
                   "(the tail kernel, measured exponent -2.0024) has already LEFT the space "
                   "-- `fredholm_sides`' crossing at s = 1.0, check C2, cokernel exponent "
                   "+1.0012 confirming that Xu's modulation functional and this "
                   "repository's cokernel functional are the same growth class. So "
                   "modulation is unbounded where the obstruction is, and defined only "
                   "where the obstruction is gone. NON-FINDING (3): whether removing the "
                   "REMAINING half repairs anything is NOT decided here. Check C3 was "
                   "pre-registered to decide it, both of its predictions failed, and "
                   "interrogation showed the instrument is not measuring the certificate's "
                   "constant (overdetermined one way, exactly singular the other). Recorded "
                   "as such, and escalated as T2b rather than resolved by assertion."),
        "escalate": False,
    },
    {
        "id": "T2b-WHAT-IS-MODULATION-IN-AN-ELL1-CERTIFICATE",
        "target": ("the same `ell^1_w` object, but a question this leg opened rather than "
                   "closed: what IS the right finite-dimensional realization of 'quotient "
                   "the lambda = 1 symmetry mode' inside a weighted-`ell^1` "
                   "radii-polynomial certificate?"),
        "criterion_a_modes_in_space": "YES (as T2).",
        "criterion_b_traces_bounded": ("The lambda = 1 mode `e_1 + e_2/2` is finitely "
                                       "supported, so quotienting IT needs no unbounded "
                                       "functional -- unlike the lambda = 0 half. That is "
                                       "why the question is live rather than closed by C1."),
        "verdict": "OPEN -- OPENED BY THIS LEG'S OWN FAILED CHECK",
        "status": "ESCALATED as a candidate scoping question for a later leg.",
        "detail": ("The naive domain-only quotient is OVERDETERMINED (two fewer unknowns, "
                   "same number of equations) so its constant is a least-squares number "
                   "that does not solve the system; the naive two-sided compression `Q L Q` "
                   "is EXACTLY SINGULAR. Both were measured here, at K = 96, s = 0.3. The "
                   "literature already knows the answer's SHAPE and this repository already "
                   "uses it: the `ell^1` way to remove a symmetry direction is a PHASE "
                   "CONDITION -- give the direction its own unfolding parameter and its own "
                   "column, keeping the system square -- which is precisely what leg 52's "
                   "bordering does, and what the gauge row already does for lambda = 0. "
                   "WHAT A LATER LEG WOULD HAVE TO DO, PRECISELY: add a SECOND border "
                   "column/row pair for `e_1 + e_2/2`, keep the system square, and "
                   "re-measure `||M_K^{-1}||_w` and `Z_1` on leg 127's own ladder. CHEAP, "
                   "and decidable either way in one leg. STRONG PRIOR AGAINST, recorded now "
                   "so nobody is sold a hope: leg 127 measured that the existing border's "
                   "coupling column is supported on a SINGLE row, the truncation edge, so "
                   "'the bordering repair has nowhere else to reach'; a second border of "
                   "the same kind has no obvious reason to reach further."),
        "escalate": True,
    },
    {
        "id": "T3-ROUTE-D-WEIGHTED-HOLDER",
        "target": ("solver/holder_norms.py + solver/hilbert_holder.py -- Route-D's "
                   "TWO-GRADING weighted-Holder space (a decay weight AND a smoothness "
                   "grading), the space Route-D v5+ actually works in"),
        "criterion_a_modes_in_space": ("NOT CHECKED HERE -- out of this leg's territory. The "
                                       "two modes exist for every admissible profile "
                                       "(Q4), so the question is only whether the decay "
                                       "grading admits them."),
        "criterion_b_traces_bounded": ("NOT CHECKED HERE. This is the whole scoping "
                                       "question: does the SMOOTHNESS grading exceed one "
                                       "derivative, so that `v -> v'(0)` is bounded? "
                                       "v7's provisional optimum sat at (alpha, gamma) = "
                                       "(1.4, 0.15), and `alpha > 1` is exactly the "
                                       "condition -- but what `alpha` indexes in that map "
                                       "is not verified by this leg."),
        "verdict": "CANDIDATE -- UNDECIDED, AND THE ONLY ONE",
        "status": "ESCALATED as a candidate scoping question for a later leg.",
        "detail": ("Why this is the only live candidate. It is the one space this "
                   "repository has built that (i) is NOT `L^2`-equivalent, so Xu sec 8's "
                   "coercivity no-go (Q11) does not cap it the way it caps T1; (ii) is not "
                   "at `s < 1` in the `ell^1_w` sense, so T2's unboundedness argument does "
                   "not transfer verbatim; and (iii) grades SMOOTHNESS explicitly, which is "
                   "the only property criterion (b) actually asks about. WHAT A LATER LEG "
                   "WOULD HAVE TO DO, PRECISELY: (1) evaluate the dual norm of "
                   "`v -> v'(0)` in the two-grading norm and report whether it is finite; "
                   "(2) if finite, check the two modes lie in the space under the decay "
                   "grading; (3) ONLY THEN ask whether the Route-D obstruction is a "
                   "symmetry-mode object at all -- because T2's check C3 is the cautionary "
                   "case, where modulation was both available and completely useless. "
                   "STRONG PRIOR AGAINST, recorded now so the later leg is not sold a "
                   "hope: in every case this repository has measured, the obstruction has "
                   "been a FAR-FIELD object, and modulation touches only the origin."),
        "escalate": True,
    },
]


def main():
    text = _pdf_text()
    prior = {}
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text())
            for sect in ("quotes", "negative_locators"):
                for e in old.get(sect, []):
                    prior[e["id"]] = e.get("located")
        except (ValueError, OSError):
            prior = {}

    quotes = locate(QUOTES, text, prior)
    negatives = locate(NEGATIVE, text, prior)

    c1 = c1_trace_functional_dual_norm()
    c2 = c2_same_crossing()
    c3 = c3_no_op_test()
    gauge = gauge_row_is_xus_functional()

    n_loc = sum(1 for q in quotes if q["located"] is True)
    n_bad = sum(1 for n in negatives if n["located"] is True)

    payload = {
        "leg": 181,
        "route": "ROUTE-MOD",
        "kind": "literature scoping (light); no solver module built, imported read-only only",
        "paper": {"arxiv": ARXIV, "version_read": VERSION_READ,
                  "url": "https://arxiv.org/abs/%s" % ARXIV,
                  "pdf_present_this_run": text is not None},
        "gate": GATE,
        "gate_answer": GATE_ANSWER,
        "gate_yes_branch_verbatim": GATE_YES_BRANCH_VERBATIM,
        "headline": (
            "Xu's 'modulation' is not Xu's and is not a technique: it is the STANDARD "
            "blow-up modulation, credited by Xu to Elgindi-Ghoul-Masmoudi, and as an "
            "operator it is the rank-2 projection onto the two origin Taylor functionals "
            "`v(0)` and `v'(0)` (eq A.13). It costs nothing, it buys nothing beyond deleting "
            "two already-known eigenvalues, and the dynamic modulation CLOSURE is explicitly "
            "OPEN (sec 8 p. 33). Its ONE structural prerequisite is that those two "
            "functionals be bounded on the realization. Applied to this repository: it is "
            "ALREADY RUNNING in two places -- energy_coercivity's `modulate=True`, and, "
            "unnoticed since leg 51, `bordered_linearization`'s GAUGE ROW, which is `v'(0)` "
            "character for character. So leg 127's `Z_1 >= 1` is a theorem about an "
            "already-partially-modulated object -- and that half of the projection is "
            "UNBOUNDED on `ell^1_w` for every s < 1, exactly the range leg 127 lives in. "
            "Whether COMPLETING the modulation would help is NOT settled here: the check "
            "pre-registered to settle it failed both its predictions and was found to be "
            "measuring the wrong quantity, so it is escalated (T2b) rather than asserted."),
        "quotes": quotes,
        "negative_locators": negatives,
        "locator_summary": {
            "quotes_total": len(quotes), "quotes_located": n_loc,
            "negatives_total": len(negatives), "negatives_wrongly_located": n_bad,
            "verified_this_run": text is not None,
        },
        "checks": {"C1_trace_dual_norm": c1, "C2_same_crossing": c2, "C3_no_op": c3,
                   "gauge_row_identity": gauge},
        "targets": TARGETS,
        "escalations": [t for t in TARGETS if t["escalate"]],
        "what_is_new_to_this_repository": [
            q["id"] for q in QUOTES if q["new_to_this_repo"]
        ] + ["CRITERION (b)-as-a-test", "GAUGE-ROW-IS-XUS-FUNCTIONAL"],
        "what_is_new_to_the_world": "nothing -- a reading of one published paper",
        "no_figure_because": ("no measurement of a curve of this repository's own; every "
                              "number is Xu's, arithmetic on Xu's, or a read-only "
                              "evaluation of an existing module"),
        "ceiling": ("literature-only; no link of L1 -> L4 moves; no ban lifted; no route "
                    "promoted; solver/spectral_certificate.py byte-identical to origin/main"),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")

    print("LEG 181 / ROUTE-MOD -- what does Xu's 'gap 1/2 after modulation' require?")
    print("=" * 78)
    print("GATE: %s" % GATE_ANSWER)
    print()
    print("locators: %d/%d quotes located, %d/%d negatives WRONGLY located (want 0)%s"
          % (n_loc, len(quotes), n_bad, len(negatives),
             "" if text is not None else "   [PDF ABSENT -- flags read back from JSON]"))
    print()
    print("C1 v'(0) dual norm on ell^1_w, w_k=(1+k)^s   prediction 'finite iff s>=1': %s"
          % ("HOLDS" if c1["prediction_holds"] else "FAILS -- READING IS WRONG"))
    for r in c1["rows"]:
        print("     s=%-4.1f  sup_k k/(1+k)^s at K=4096: %-12.4g  saturates=%s"
              % (r["s"], r["dual_norm_by_K"]["4096"], r["saturates"]))
    print()
    print("C2 fredholm_sides: kernel exponent %.4f (want ~-2, %s), cokernel %.4f "
          "(want ~+1, %s), crossing s=%.1f"
          % (c2["fredholm_sides"]["kernel_exponent"],
             "ok" if c2["kernel_matches"] else "MISMATCH",
             c2["fredholm_sides"]["cokernel_exponent"],
             "ok" if c2["cokernel_matches"] else "MISMATCH",
             c2["fredholm_sides"]["crossing"]))
    print()
    print("GAUGE ROW IDENTITY: bordered_linearization's gauge row == v'(0) exactly: %s"
          % gauge["is_exactly_v_prime_at_origin"])
    print()
    print("C3 no-op test at K=%d, s=%.1f:" % (c3["K"], c3["s"]))
    print("     ||M^-1||_w unmodulated       %.6g" % c3["norm_unmodulated"])
    print("     ||.||_w on the modulated domain  %.6g  (ratio %.4f)"
          % (c3["norm_modulated_domain_restricted"],
             c3["ratio_modulated_over_unmodulated"]))
    print("     witness mass on modulation span: %.4g%% of ||witness||_w"
          % (100.0 * c3["witness_mass_fraction_on_span"]))
    print("     two-sided compression Q L Q exactly singular: %s"
          % c3["two_sided_compression_QLQ_is_singular"])
    print("     PRE-REGISTERED PREDICTIONS HELD: %s  ->  %s"
          % (c3["both_predictions_held"], c3["verdict"]))
    print("     (verdict rests on C1 + C2 + gauge-row identity, NOT on C3)")
    print()
    for t in TARGETS:
        print("%-28s %s" % (t["id"], t["verdict"]))
    print()
    print("ESCALATED: %s" % ", ".join(t["id"] for t in TARGETS if t["escalate"]))
    print("wrote %s" % OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
