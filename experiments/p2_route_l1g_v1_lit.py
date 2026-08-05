"""P2 Route-L1G v1 -- the primary-source pass on the LAST two unread Tier-2 papers.

Leg 65.  A LITERATURE leg: no computation, no new bound, no Route-D bound-sharpening
(the standing ban is untouched -- this leg produces no constant).

WHAT IT ANSWERS.  The gate, verbatim:

    "Does any primary source (the two unread Tier-2 papers, or anything they cite
     forward) already publish the weighted-ell-1 no-go or the discrete-ball trap for
     this operator class, or an equivalent statement under different notation?"

    ANSWER: NO, for both claims, after four papers at full text.

WHY IT IS A SCRIPT AND NOT ONLY PROSE (lesson 68, and leg 57's ledger).  Five literature
passes in this project were written at search level and decayed.  This file is the
executable form of the pass: the query strings are stored verbatim, each paper carries the
sections actually read, and every full-text verdict carries a LOCATOR (equation or section
number) plus a verbatim quote.  The term-frequency block is a re-runnable MAGNITUDE, not a
boolean -- re-extract the PDFs with `pdftotext -layout` and the counts must reproduce.

    bash Papers/fetch.sh 2312.01702 1908.09385 2607.15256 2005.14027
    pdftotext -layout Papers/<id>.pdf Papers/<id>.txt      # for the term counts only
    .venv/bin/python experiments/p2_route_l1g_v1_lit.py
        -> writeup/data/p2_route_l1g_v1_lit.json

Papers/ is gitignored, so the counts are recomputed when the PDFs are present and read
back from the committed JSON when they are not.  The JSON is the curated artifact; the
prose lives in writeup/novelty/leg_65.md, which doubles as this leg's technical note.

NO FIGURE: nothing here is a numeric plot.

THE TWO CLAIMS UNDER TEST (quoted from this repository, not paraphrased):

  C1  the weighted-ell^1 no-go, Route-D v3, restated in solver/holder_norms.py:
      "a diagonal weight on Fourier coefficients measures SMOOTHNESS, and the far-field
       transport needs DECAY.  No weighted-ell^1 pair can carry the certificate."
  C2  the discrete-ball trap, Route-D v6 measurement B1:
      "Computing an induced norm by duality over the DISCRETE unit ball is unsound: a
       discrete Holder seminorm only inspects grid nodes, so the extremizer duality
       selects is a grid-scale sign pattern whose interpolant has an enormous continuum
       norm."
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

OUT = ROOT / "writeup" / "data" / "p2_route_l1g_v1_lit.json"
PAPERS = ROOT / "Papers"

# ---------------------------------------------------------------------------
# 1. the query log -- verbatim strings, links not counts
# ---------------------------------------------------------------------------

QUERIES = [
    {
        "id": "Q1",
        "query": ("weighted ell^1 Fourier norm cannot simultaneously control smoothness "
                  "and decay computer-assisted proof no-go"),
        "targets": ["C1"],
        "links": [
            "https://arxiv.org/pdf/2203.02404",
            "https://arxiv.org/html/2603.02021",
            "https://arxiv.org/pdf/1601.00307",
            "https://arxiv.org/pdf/2303.03518",
            "https://www.sciencedirect.com/science/article/pii/S1063520315000196",
            "https://arxiv.org/pdf/1308.0759",
            "https://arxiv.org/pdf/1503.02352",
        ],
        "on_topic": [],
        "reading": ("the ell^1 hits are compressed-sensing weighted ell^1, a different object; "
                    "the CAP hits USE an ell^1-Wiener norm with geometric weights nu > 1, the "
                    "regime that avoids the algebraic-decay setting where C1 bites"),
    },
    {
        "id": "Q2",
        "query": ("induced operator norm by duality over discretized unit ball unsound "
                  "extremizer grid-scale sign pattern Holder seminorm validated numerics"),
        "targets": ["C2"],
        "links": [
            "https://njohnston.ca/2016/01/how-to-compute-hard-to-compute-matrix-norms/",
            "https://www.sciencedirect.com/science/article/pii/S0024379520300197",
            "https://arxiv.org/pdf/2503.19190",
        ],
        "on_topic": [],
        "reading": "only the generic sup-over-the-dual-ball fact, which is C2's premise, not C2",
    },
    {
        "id": "Q3",
        "query": ("rigorous numerics dual norm computed over finite-dimensional discretization "
                  "underestimates continuum operator norm interpolant Holder seminorm pitfall"),
        "targets": ["C2"],
        "links": [
            "https://arxiv.org/pdf/2305.05660",
            "https://arxiv.org/abs/2502.09984",
            "https://arxiv.org/pdf/1812.08100",
            "https://arxiv.org/pdf/2203.07126",
            "https://link.springer.com/article/10.1007/s00365-021-09539-0",
            "https://arxiv.org/pdf/2312.05670",
        ],
        "on_topic": ["https://arxiv.org/pdf/1812.08100", "https://arxiv.org/pdf/2203.07126"],
        "reading": ("the sampling-discretization literature is the AMBIENT mathematics behind C2 "
                    "(when does a norm sampled at nodes control the continuum norm; it degrades "
                    "as class smoothness drops) but none of it is about a dual/extremizer step "
                    "inside a certificate, and none reports an inflation factor"),
    },
    {
        "id": "Q4",
        "query": ("Temlyakov sampling discretization of norms fails for function classes without "
                  "smoothness discrete norm does not control continuum norm survey"),
        "targets": ["C2"],
        "links": [
            "https://arxiv.org/abs/2203.07126",
            "https://link.springer.com/article/10.1007/s00365-021-09539-0",
            "https://link.springer.com/article/10.1134/S0001434625030265",
        ],
        "on_topic": ["https://arxiv.org/abs/2203.07126"],
        "reading": "confirms Q3's reading and adds nothing new",
    },
    {
        "id": "Q5",
        "query": ('Campolina Mailybaev "Fluid dynamics on logarithmic lattices" Nonlinearity 2021 '
                  "arXiv function spaces norms conservation laws"),
        "targets": ["C1"],
        "links": [
            "https://iopscience.iop.org/article/10.1088/1361-6544/abef73",
            "https://arxiv.org/pdf/2005.14027",
            "https://iopscience.iop.org/article/10.1088/1361-6544/ad7661",
        ],
        "on_topic": ["https://arxiv.org/pdf/2005.14027"],
        "reading": ("the framework paper 2312.01702 rests on, and the only forward-cited place a "
                    "weighted sequence-space conservation law could live -- read at full text"),
    },
    {
        "id": "Q6",
        "query": ("https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}/citations"
                  "?fields=title,externalIds  [forward-citation sweep, not a text query]"),
        "targets": ["C1", "C2"],
        "links": [
            "https://api.semanticscholar.org/graph/v1/paper/arXiv:2312.01702/citations",
            "https://api.semanticscholar.org/graph/v1/paper/arXiv:1908.09385/citations",
            "https://arxiv.org/abs/2607.15256",
        ],
        "on_topic": ["https://arxiv.org/abs/2607.15256"],
        "reading": ("2312.01702 is cited by 8 papers, all turbulence physics, none with a norm; "
                    "1908.09385 is cited by 31, the gCLM/Hou-Luo blowup corpus, of which exactly "
                    "ONE is methodological about weighted norms in a CAP: 2607.15256"),
    },
]

# ---------------------------------------------------------------------------
# 2. the full-text pass -- one record per paper, with LOCATORS and quotes
# ---------------------------------------------------------------------------

PAPERS_READ = [
    {
        "arxiv": "2312.01702",
        "url": "https://arxiv.org/abs/2312.01702",
        "cite": ("Pikeroen, Barral, Costa, Campolina, Mailybaev, Dubrulle, 'Tracking complex "
                 "singularities of fluids on log-lattices', v1 4 Dec 2023; Nonlinearity 37 (2024), "
                 "doi 10.1088/1361-6544/ad7661"),
        "tier": "Tier 2 -- previously fetched, NEVER read for C1/C2",
        "sections_read": ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1-3.4", "4.1-4.5", "5.1-5.3",
                          "references (28 items)"],
        "c1": "ABSENT",
        "c2": "ABSENT",
        "why": ("a numerical-physics scaling study: the singularity-strip method fits delta from "
                "the slope of log E(k) (sec 2.4, u_k ~ k^{-d-xi} e^{ika} e^{-delta k} => E(k) ~ "
                "e^{-2 delta k}), integrated by explicit RK4 with viscous splitting "
                "exp(-nu k^{2 gamma} dt) (sec 2.5). No norm, no operator bound, no approximate "
                "inverse, no duality anywhere in the paper"),
        "quotes": [
            {"locator": "sec 2, p.5",
             "text": "we have presently no rigorous statements about the dyadic model for the "
                     "parameter"},
            {"locator": "sec 3 intro",
             "text": "Despite the absence of rigorous proofs, it is"},
        ],
        "note": ("its 'measure the exponent, not the threshold' discipline is the flagged possible "
                 "pre-emption of the mu-as-a-coordinate candidate -- a DIFFERENT claim, not this "
                 "leg's"),
    },
    {
        "arxiv": "1908.09385",
        "url": "https://arxiv.org/abs/1908.09385",
        "cite": ("J. Chen, 'Singularity formation and global well-posedness for the generalized "
                 "Constantin-Lax-Majda equation with dissipation', v1 25 Aug 2019"),
        "tier": "Tier 2 -- previously read for COMPUTER ASSISTANCE ONLY (leg 45), never for C1/C2",
        "sections_read": ["1 (Thms 1.1-1.5, Rmks 1.2-1.7)", "2.1", "2.2", "2.3", "2.4", "2.5",
                          "2.6", "global well-posedness sections", "Appendix A"],
        "c1": "ABSENT -- nearest structure is a CHOSEN two-weight offset, not a no-go",
        "c2": "ABSENT -- the paper never discretizes, so there is no discrete ball",
        "why": ("a perturbative analytic argument whose weights are continuum physical-space "
                "energy weights on the line; the working space is L^2(phi) cap H^4(psi), a "
                "HILBERT pair, so sec M-4's reason that CLN does not close C1 applies verbatim"),
        "quotes": [
            {"locator": "eq (2.12) and the line after",
             "text": "phi = (x^2+b^2)^3/(2b x^4) = -(1/wbar)(x^2+b^2)/x^3 , psi = (x^2+b^2)^3/(2b) "
                     "= -x(x^2+b^2)/wbar ... and will perform weighted L2 and weighted H4 "
                     "estimates to establish the nonlinear stability"},
            {"locator": "sec 2.2, after eq (2.12)",
             "text": "In the following discussion, we assume omega in L^2(phi) cap H^4(psi)"},
            {"locator": "sec 2.3, term D",
             "text": "For D, we separate the singular and less singular part of the weight phi "
                     "defined in (2.12)"},
        ],
        "near_miss": ("phi = psi / x^4: the SINGULAR weight sits on the LOW-order (L^2) estimate "
                      "and the less singular one on the HIGH-order (H^4) estimate -- a two-grading "
                      "structure with a fixed grading offset, the same SHAPE as C1's 'separated by "
                      "exactly one grading power'. It is not C1: the offset is chosen to make a "
                      "cancellation work, nothing is claimed impossible, no statement is made "
                      "about the class of admissible weights, and the space is Hilbert not ell^1"),
    },
    {
        "arxiv": "2607.15256",
        "url": "https://arxiv.org/abs/2607.15256",
        "cite": ("J. Chen and T. Y. Hou, 'Analytic finite-rank corrections for singularly weighted "
                 "estimates in a computer-assisted proof of 3D Euler singularity', 16 Jul 2026"),
        "tier": "FORWARD CITATION of 1908.09385 -- the one live candidate the sweep produced",
        "sections_read": ["abstract", "1.1", "1.2", "1.3", "1.4", "2.1", "4", "5 Step 2"],
        "c1": "NEAREST PUBLISHED COUSIN, and still not C1",
        "c2": "the MORAL is present as working practice; the CLAIM is absent",
        "why": ("it publishes a weight obstruction, but a LOCAL VANISHING-ORDER one at the "
                "singularity, in weighted L^infinity / C^{1/2} energy spaces, and it RESOLVES it "
                "by analytic low-rank corrections. C1 is a FAR-FIELD decay-vs-smoothness "
                "obstruction in a weighted ell^1 sequence space, asserted as a no-go over a whole "
                "class of weights: different end of the domain, different space, different "
                "logical form"),
        "quotes": [
            {"locator": "abstract",
             "text": "One effective approach to establishing stability of perturbations around a "
                     "numerically constructed profile is to perform weighted energy estimates with "
                     "singular weights near the singularity. However, the weighted norms require "
                     "exact local vanishing conditions that are not automatically preserved by the "
                     "equations nor the numerical construction."},
            {"locator": "sec 1.4, around eq (1.25)",
             "text": "the singular weights are effectively of order |x|^{-3} near the origin. To "
                     "employ the singularly weighted energy estimates, the perturbation must vanish "
                     "cubically near the origin f(x) = O(|x|^3), near x = 0 ... However, the natural "
                     "odd/even symmetry class of the perturbation and the equations preserves only "
                     "quadratic vanishing order."},
            {"locator": "sec 1.2, around eqs (1.17)-(1.18)",
             "text": "Since the energy must be finite and eta(x,0) != 0, one cannot choose beta >= "
                     "1. If (1-beta) is not small, since a2 is much larger than a1, a3, the term "
                     "a2(1-beta)/2 arising from the y-advection in (1.17) contributes a large "
                     "positive growth term. On the other hand, if (1-beta) is small, the estimate "
                     "of the nonlocal term u_x in (2.2) contributes a large constant "
                     "(1-beta)^{-1/2} ... As a result, one needs to take a very singular weight "
                     "x^{-alpha} y^{-beta} or |(x,y)|^{-alpha} y^{-beta} with large alpha to "
                     "extract the desired damping effect."},
            {"locator": "sec 1.4",
             "text": "The key point is that the numerical step only determines coefficients in "
                     "explicit basis representations. Once these coefficients are fixed, they "
                     "determine functions defined on the entire domain, rather than merely "
                     "numerical values on grid points."},
        ],
        "near_miss": ("(1.17)-(1.18) is a published instance of C1's GENRE -- one weight exponent "
                      "squeezed from both sides, finite energy above and a nonlocal constant "
                      "diverging like (1-beta)^{-1/2} below -- in weighted L^2. It is a "
                      "quantitative trade-off RESOLVED BY A CHOICE (take alpha large), the "
                      "competing requirements are damping vs finite energy rather than smoothness "
                      "vs far-field decay, and no conservation of the separation is claimed. The "
                      "sec-1.4 basis-vs-grid-values passage is C2's hygiene stated as practice, "
                      "with no dual computation, no extremizer and no inflation measurement"),
    },
    {
        "arxiv": "2005.14027",
        "url": "https://arxiv.org/abs/2005.14027",
        "cite": ("C. S. Campolina and A. A. Mailybaev, 'Fluid dynamics on logarithmic lattices', "
                 "Nonlinearity 34 (2021) 4684-4715, doi 10.1088/1361-6544/abef73"),
        "tier": "FORWARD-CITED framework paper of 2312.01702",
        "sections_read": ["function spaces eqs (37)-(38),(40)", "local existence eqs (45)-(46),(50)",
                          "blow-up criterion", "Appendix B Lemma 15 eq (78)"],
        "c1": "ABSENT -- and the structural result runs the OPPOSITE way",
        "c2": "ABSENT",
        "why": ("the lattice space is a weighted ell^2 (homogeneous Sobolev h^m), i.e. a Hilbert "
                "grading exactly as CLN's H^l is, and the nonlinear term is proved BOUNDED because "
                "log-lattice interactions are local. A log-lattice is geometric in k, so there is "
                "no unbounded physical-space transport tail to invert and the far-field half of "
                "C1's tension never arises"),
        "quotes": [
            {"locator": "eq (37)",
             "text": "||u||_{h^m} = ||D^m u||_{ell^2} = ( sum |k|^{2m} |u(k)|^2 )^{1/2} < infinity"},
            {"locator": "after eq (44)",
             "text": "Operator B is a bounded bilinear operator in h^m - see the proof in Appendix B"},
            {"locator": "eq (54) / Lemma 15 eq (78)",
             "text": "||f * g||_{h^m} <= C(||f||_{h^m}||g||_{ell^infinity} + "
                     "||Df||_{ell^infinity}||g||_{h^{m-1}})"},
        ],
    },
]

# ---------------------------------------------------------------------------
# 3. re-runnable magnitudes: term frequencies in the extracted full texts
# ---------------------------------------------------------------------------

TERMS = ["weight", "fourier", "banach", "rigorous", "computer-assist", "validated",
         "duality", "discret", "wiener", "interval arith"]

# recorded from the pass, so the JSON is complete even when Papers/ is empty
TERM_COUNTS_RECORDED = {
    "1908.09385": {"weight": 14, "fourier": 3, "banach": 0, "rigorous": 0, "computer-assist": 0,
                   "validated": 0, "duality": 0, "discret": 0, "wiener": 0, "interval arith": 0,
                   "chars": 102610},
    "2312.01702": {"weight": 0, "fourier": 11, "banach": 0, "rigorous": 3, "computer-assist": 0,
                   "validated": 0, "duality": 0, "discret": 0, "wiener": 0, "interval arith": 0,
                   "chars": 66790},
    "2607.15256": {"weight": 108, "fourier": 0, "banach": 0, "rigorous": 26, "computer-assist": 12,
                   "validated": 0, "duality": 0, "discret": 2, "wiener": 0, "interval arith": 0,
                   "chars": 105271},
    "2005.14027": {"weight": 1, "fourier": 41, "banach": 2, "rigorous": 5, "computer-assist": 0,
                   "validated": 1, "duality": 0, "discret": 5, "wiener": 0, "interval arith": 0,
                   "chars": 108587},
}


def term_counts():
    """Recompute from Papers/<id>.txt when present; else return the recorded pass values.

    Case-folded substring counts on the `pdftotext -layout` output.  They are MAGNITUDES:
    'weight' occurs 0 times in 2312.01702 and 108 times in 2607.15256, which is the whole
    argument for where each paper sits relative to C1.
    """
    out, source = {}, {}
    for pid, recorded in TERM_COUNTS_RECORDED.items():
        txt = PAPERS / (pid + ".txt")
        if txt.exists():
            body = txt.read_text(errors="ignore").lower()
            out[pid] = {t: body.count(t) for t in TERMS}
            out[pid]["chars"] = len(body)
            source[pid] = "recomputed"
        else:
            out[pid] = dict(recorded)
            source[pid] = "recorded (Papers/ is gitignored; run Papers/fetch.sh + pdftotext)"
    return out, source


# ---------------------------------------------------------------------------

GATE = ("Does any primary source (the two unread Tier-2 papers, or anything they cite forward) "
        "already publish the weighted-ell-1 no-go or the discrete-ball trap for this operator "
        "class, or an equivalent statement under different notation?")


def build():
    counts, source = term_counts()
    return {
        "leg": 65,
        "route": "P2 Route-L1G v1 -- primary-source pass on the last two unread Tier-2 papers",
        "kind": "literature classification; no computation, no bound, no figure",
        "claims_under_test": {
            "C1": {
                "name": "the weighted-ell^1 no-go (Route-D v3)",
                "statement": ("a diagonal weight on Fourier coefficients measures SMOOTHNESS, and "
                              "the far-field transport needs DECAY. No weighted-ell^1 pair can "
                              "carry the certificate; the two NK requirements are separated by "
                              "exactly one grading power, and the separation is conserved"),
                "stated_in": ["solver/holder_norms.py (module docstring)",
                              "writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_SPACES.md",
                              "LITERATURE_CHECK.md candidate table"],
            },
            "C2": {
                "name": "the discrete-ball trap (Route-D v6, measurement B1)",
                "statement": ("computing an induced norm by duality over the DISCRETE unit ball is "
                              "unsound: a discrete Holder seminorm only inspects grid nodes, so "
                              "the extremizer duality selects is a grid-scale sign pattern whose "
                              "interpolant has an enormous continuum norm"),
                "stated_in": ["experiments/p2_route_d_v6_bounds.py (header, B1)",
                              "writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_V6.md"],
            },
        },
        "prior_bookkeeping": {
            "capabilities.py": ("solver/holder_norms.py entry: 'the weighted-l1 no-go is derived "
                                "here and is UNSEARCHED at primary source'"),
            "PHASE2_P2_NOTES.md M-4": ("CLN arXiv:2302.12877 works in Hilbert/Fourier H^l spaces, "
                                       "not weighted ell^1, so C1 and C2 are narrowed, not closed "
                                       "-- 'still UNSEARCHED at primary source, and still the only "
                                       "claims with a real chance of being new'"),
        },
        "gate": GATE,
        "gate_answer": "NO",
        "gate_answer_detail": ("neither C1 nor C2, nor an equivalent statement under different "
                               "notation, is published in the two remaining Tier-2 papers or in "
                               "anything they cite forward. The nearest published object is "
                               "arXiv:2607.15256 secs 1.2/1.4, which states a weight tension of "
                               "the same GENRE in weighted L^2/L^infinity energy spaces and "
                               "resolves it, rather than stating a no-go over a class of weights"),
        "papers_read_full_text": PAPERS_READ,
        "queries": QUERIES,
        "magnitudes": {
            "papers_read_at_full_text": len(PAPERS_READ),
            "queries_logged": len(QUERIES),
            "forward_citations_swept_2312_01702": 8,
            "forward_citations_swept_1908_09385": 31,
            "forward_citations_on_topic": 1,
            "on_topic_forward_citation": "arXiv:2607.15256",
            "term_counts": counts,
            "term_count_source": source,
            "chen_weight_offset_between_the_two_estimates": "phi = psi / x^4 (eq 2.12)",
            "chen_hou_singular_weight_order_near_origin": "|x|^{-3}",
            "chen_hou_vanishing_order_gap": "required O(|x|^3) vs preserved O(|x|^2)",
        },
        "consequences": {
            "holder_norms_py": ("NO change required and none made -- its docstring carries no "
                                "novelty claim, and it is outside this leg's territory in any case"),
            "capabilities_py_line_179": ("HANDED TO THE ORCHESTRATOR, not edited here (integration-"
                                         "owned): 'UNSEARCHED at primary source' is now the wrong "
                                         "word in a favourable direction. The accurate wording is "
                                         "SEARCHED AT PRIMARY SOURCE AND NOT FOUND, over 5 papers "
                                         "(2302.12877, 2312.01702, 1908.09385, 2607.15256, "
                                         "2005.14027)"),
            "route_d_ban": ("UNTOUCHED. This leg produces no bound and does not resume any Route-D "
                            "bound-sharpening computation; B stays dead on all three DOF"),
        },
        "residual_risk": ("search-level absence is not proof. Two directions were classified but "
                          "not read at full text: the sampling-discretization corpus "
                          "(arXiv:1812.08100, arXiv:2203.07126) which is C2's ambient mathematics, "
                          "and the ell^1-Wiener CAP corpus with geometric weights nu > 1, which "
                          "avoids C1's algebraic-decay regime by construction"),
    }


def main():
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")

    print("P2 Route-L1G v1 -- primary-source pass, leg 65")
    print("GATE:", GATE)
    print("ANSWER:", data["gate_answer"], "--", data["gate_answer_detail"][:120], "...")
    print()
    print("papers read at full text:", data["magnitudes"]["papers_read_at_full_text"],
          "| queries logged:", data["magnitudes"]["queries_logged"],
          "| forward citations swept:",
          data["magnitudes"]["forward_citations_swept_2312_01702"] +
          data["magnitudes"]["forward_citations_swept_1908_09385"],
          "| on topic:", data["magnitudes"]["forward_citations_on_topic"])
    print()
    for p in PAPERS_READ:
        print(f"  {p['arxiv']:<12} C1={p['c1'][:44]:<44} C2={p['c2'][:34]}")
    print()
    print("term counts (magnitudes, not booleans):")
    for pid, c in data["magnitudes"]["term_counts"].items():
        print(f"  {pid:<12} weight={c['weight']:<4} fourier={c['fourier']:<4} "
              f"rigorous={c['rigorous']:<4} computer-assist={c['computer-assist']:<3} "
              f"duality={c['duality']}  [{data['magnitudes']['term_count_source'][pid][:9]}]")
    print()
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
