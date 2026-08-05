"""Route-A12 v1 (leg 64): is alpha_1 at a = 1/2 -- or the sigma = 3 criticality it
comes from -- published anywhere for gCLM?

PURE LITERATURE LEG.  Nothing here computes a gCLM quantity; the standing ban on
further gCLM measurement legs is respected.  This script is the executable record of
a search: it carries the query strings, the corpus enumeration, the primary-source
locations (paper section + extracted-text line), and the verbatim sentences, and it
re-emits them as writeup/data/p2_route_a12_v1_alpha_lit.json.

WHAT WAS ASKED (the leg's gate, verbatim)
    "Does any primary source publish alpha_1 at a=1/2 (or the sigma=3 criticality
     statement it comes from) for this model?"

WHAT CAME BACK -- the disjunction splits:

  * sigma = 3 at a = 1/2:  YES, and in TIER 1.  Xu arXiv:2607.19762 sec 6.1 (after
    eq (6.3)), Table 1 row a = 0.5, and Figure 3's in-plot annotation all state
    s*(1/2) = 3 EXACTLY.  Under the repository's own exponent dictionary (their
    Lambda^sigma is our (-Delta)^s with sigma = 2s; our alpha = 1/c_l) their
    s*(1/2) = 3 IS our "criticality at a = 1/2 is sigma = 3", digit for digit --
    and theirs is exact where ours is a numerical branch value.

  * alpha_1 = dalpha/dmu at that point:  NO.  Not in Xu, not in ALS, not in J. Chen,
    not in LSS, not in the periodic exact-solution paper, not in Sakajo, and not
    anywhere in a complete 25-result arXiv enumeration (max_results=100 requested,
    totalResults=25 returned) of the Constantin-Lax-Majda corpus.
    Xu, in the same subsection that publishes the threshold, says the marginal case
    s = s* is open and that his machinery lives at a = 0.

THE REASON THE GAP IS STRUCTURAL, not an accident of searching:
    the dissipative-gCLM exact-solution corpus is
        real line: (a,sigma) in {(0,0), (0,1), (0,2), (1/2,1)}
        periodic : (a,sigma) in {(0,0), (0,1), (1/2,0), (1/2,1)}
    sigma = 3 appears in NONE of them.  alpha_1 at a = 1/2 is a coefficient of the
    marginal flow AT sigma = 3, so there is no exact solution in the literature from
    which anyone could have read it off.

TWO TRAPS, either of which produces a wrong verdict (both recorded in the JSON):
  T1  "critical dissipation" means two different things at a = 1/2.  J. Chen's own
      NORM criticality, from L^1 conservation in his a > -1 regime, is gamma = 1
      (his formula gamma = |a|^{-1}, in the L^{|a|} norm, is stated only for
      a <= -1 and does not apply here).  The scaling-relevance criticality of the
      self-similar profile is sigma = 3, two units above.  Chen's Theorem 1.1
      blow-up result separately uses the full Laplacian, gamma = 2 (his chosen
      instrument, "for simplicity" -- one unit below sigma = 3, matching Xu's
      "s = 2 < 3, subcritical").  Either reading, Chen's theorem does not touch the
      point in question.
  T2  ALS call sigma = 0 "'marginal' dissipation".  That is the BOTTOM of the sigma
      range, not the point sigma = sigma_c.  It is the only "marginal" hit in the
      dissipative corpus and it is a false friend.

METHOD, so the pass is reproducible:
    bash Papers/fetch.sh 2607.19762 2207.07548 2010.01201 1908.09385   (4/4 first try)
    pdftotext -layout <each>.pdf <each>.txt
    grep the extracted text for the strings recorded in GREPS below.
    Papers/ is gitignored on purpose; the PDFs are not committed, the locations are.

Full prose, with the verbatim quotations and the reported corrections to
capabilities.py / LITERATURE_CHECK.md / PHASE2_P2_NOTES.md, is in
writeup/novelty/leg_64.md (this leg's technical note as well as its novelty log).
"""

from __future__ import annotations

import json
import os

PASS_DATE = "2026-08-05"

GATE = (
    "Does any primary source publish alpha_1 at a=1/2 (or the sigma=3 criticality "
    "statement it comes from) for this model?"
)

# ---------------------------------------------------------------------------
# The number this leg is about.  NOT recomputed here -- quoted from Route-H v1
# (PHASE2_P2_NOTES.md H3, writeup/data/p2_route_h_v1_critical.json) so that the
# comparison against the literature has something to compare.
# ---------------------------------------------------------------------------
ALPHA_1_LADDER = {96: 0.132770, 144: 0.133470, 192: 0.133628, 240: 0.133683}

# ---------------------------------------------------------------------------
# Query log.  Links, not counts (writeup/novelty/README.md's rule, after leg 53).
# ---------------------------------------------------------------------------
QUERIES = [
    {
        "id": "Q1",
        "kind": "web_search",
        "query": (
            "generalized Constantin-Lax-Majda equation critical fractional "
            "dissipation exponent a=1/2 sigma=3"
        ),
        "relevant_links": [
            "https://arxiv.org/abs/1908.09385",
            "https://arxiv.org/abs/2207.07548",
            "https://arxiv.org/pdf/2411.01891",
            "https://iopscience.iop.org/article/10.1088/1361-6544/ad140c",
        ],
        "verdict": "surfaced the four-paper dissipative corpus; no sigma=3 result",
    },
    {
        "id": "Q2",
        "kind": "web_search",
        "query": (
            "gCLM marginal critical dissipation self-similar exponent derivative "
            "with respect to viscosity mu_tau = -alpha_1 mu^2 algebraic decay"
        ),
        "relevant_links": [
            "https://arxiv.org/html/2607.19762v1",
            "https://arxiv.org/pdf/1908.09385",
        ],
        "verdict": "no hit on the marginal expansion; other returns off-topic",
    },
    {
        "id": "Q3",
        "kind": "web_search",
        "query": (
            "Constantin-Lax-Majda a=1/2 dissipation Lambda^3 critical self-similar "
            "blowup persistence"
        ),
        "relevant_links": [
            "https://arxiv.org/abs/1908.09385",
            "https://arxiv.org/pdf/2411.01891",
            "https://arxiv.org/abs/2607.19762",
            "https://arxiv.org/pdf/2401.14615",
        ],
        "verdict": "Lambda^3 returns nothing; the a=1/2 dissipative results are at gamma=2",
    },
    {
        "id": "Q4",
        "kind": "web_search",
        "query": (
            '"generalized Constantin-Lax-Majda" dissipation marginal case rescaled '
            "viscosity parameter dynamical system fixed point second order coefficient"
        ),
        "relevant_links": [
            "https://arxiv.org/pdf/2506.02800",
            "https://arxiv.org/pdf/2207.07548",
            "https://www.researchgate.net/publication/326959516_Unimodal_solutions_of_the_generalized_Constantin-Lax-Majda_equation_with_viscosity",
        ],
        "verdict": "only 'marginal' hit is ALS's sigma=0 -- trap T2, a false friend",
    },
    {
        "id": "Q5",
        "kind": "web_search",
        "query": (
            "arXiv generalized Constantin-Lax-Majda equation fractional dissipation "
            "2025 2026 self-similar profile viscosity dependence exponent"
        ),
        "relevant_links": [
            "https://arxiv.org/html/2607.19762v1",
            "https://arxiv.org/html/2603.25104",
            "https://arxiv.org/pdf/2401.14615",
            "https://arxiv.org/abs/1908.09385",
        ],
        "verdict": "recent work is inviscid (2603.25104, 2401.14615) or Xu's threshold",
    },
    {
        "id": "Q6",
        "kind": "web_search",
        "query": (
            '"0.133683" OR "critical dissipation" gCLM "a = 1/2" sigma = 3 marginal '
            "exponent alpha_1"
        ),
        "relevant_links": ["https://arxiv.org/pdf/2312.01702"],
        "verdict": (
            "the number itself returns nothing in this model's literature; all other "
            "returns were condensed-matter critical-exponent papers"
        ),
    },
    {
        "id": "Q7",
        "kind": "web_search",
        "query": (
            "Sakajo generalized viscosity Constantin-Lax-Majda arbitrary derivative "
            "order blow-up small viscosity global solutions"
        ),
        "relevant_links": [
            "https://www.ms.u-tokyo.ac.jp/journal/abstract/jms100107.html",
            "https://ui.adsabs.harvard.edu/abs/2003Nonli..16.1319S/abstract",
            "https://www.math.kyoto-u.ac.jp/~sakajo/research/CLM/CLM.html",
        ],
        "verdict": (
            "Sakajo is a=0 and gives thresholds IN nu for arbitrary derivative order, "
            "not a derivative of the exponent with respect to nu"
        ),
    },
    {
        "id": "Q8",
        "kind": "corpus_enumeration",
        "query": (
            'https://export.arxiv.org/api/query?search_query=all:"Constantin-Lax-Majda"'
            "&start=0&max_results=100"
        ),
        "relevant_links": [
            "http://arxiv.org/abs/1908.09385v1",
            "http://arxiv.org/abs/2207.07548v1",
            "http://arxiv.org/abs/2411.01891v2",
            "http://arxiv.org/abs/2607.19762v1",
        ],
        "verdict": (
            "full corpus enumerated by title; the DISSIPATIVE gCLM subset is exactly "
            "these four papers, everything else is inviscid gCLM/De Gregorio, "
            "right-invariant-metric geometry, or 3D-Euler papers that merely cite CLM"
        ),
    },
    {
        "id": "Q9",
        "kind": "web_fetch",
        "query": "https://arxiv.org/abs/2411.01891",
        "relevant_links": ["https://arxiv.org/abs/2411.01891"],
        "verdict": (
            "abstract read verbatim: periodic exact solutions for a=0 and 1/2 and "
            "sigma=0 and 1 -- sigma=3 absent"
        ),
    },
]

# ---------------------------------------------------------------------------
# Primary-source locations.  "line" is into the pdftotext -layout extraction, so
# the read is reproducible from the fetch command in this docstring.
# ---------------------------------------------------------------------------
SOURCES = [
    {
        "key": "XU",
        "arxiv": "2607.19762",
        "cite": "Xu, 'The spectral picture of self-similar collapse in the CLM equation', 22 Jul 2026",
        "tier": 1,
        "role": "PUBLISHES the sigma=3 criticality at a=1/2; leaves the marginal case open",
        "locations": {
            "sec_6": "line 1751",
            "sec_6.1": "line 1760",
            "eq_6.3": "line 1769",
            "s_star_half_sentence": "lines 1794-1797",
            "table_1": "paper page 4, lines 230-247 (row a = 0.5)",
            "fig_3_caption": "lines 1818-1829",
            "marginal_open_sentence": "lines 1777-1781",
            "appendix_A": "line 1984 ('The exact linear semigroup at a = 0')",
        },
    },
    {
        "key": "ALS",
        "arxiv": "2207.07548",
        "cite": "Ambrose, Lushnikov, Siegel, Silantyev, Nonlinearity 33 (2020) / arXiv 2022",
        "tier": 1,
        "role": "exact dissipative solutions; sigma=3 absent; eq (61) is the a=0 alpha_1=0 object",
        "locations": {
            "sec_5.1_a0_sigma2": "line 1044",
            "sec_5.2_ahalf_sigma1": "line 1178",
            "sec_5.3_a0_sigma1": "line 1298",
            "eq_61": "line 1385",
            "sec_5.4_a0_sigma0": "line 1561",
            "marginal_sigma0_language": "line ~213 (intro) -- trap T2",
        },
    },
    {
        "key": "CHEN",
        "arxiv": "1908.09385",
        "cite": "J. Chen 2020, Nonlinearity 33 2502-2532",
        "tier": 2,
        "role": "blow-up via full Laplacian (gamma=2) for a near 1/2; his NORM criticality (L^1 conservation) is gamma=1 -- trap T1",
        "locations": {
            "sec_1.2_scaling_and_critical_dissipation": "lines 84-96",
            "a_half_self_similar_ansatz_inviscid": "lines 195-222",
        },
    },
    {
        "key": "LSS",
        "arxiv": "2010.01201",
        "cite": "Lushnikov, Silantyev, Siegel 2021, J. Nonlinear Sci. 31 art. 82",
        "tier": 2,
        "role": "INVISCID branch + a_c = 0.6890665; cannot contain alpha_1",
        "locations": {
            "only_dissipation_string_in_paper": "line 2236 -- a bibliography entry",
        },
    },
    {
        "key": "SLSA",
        "arxiv": "2411.01891",
        "cite": "Silantyev, Lushnikov, Siegel, Ambrose, submitted 4 Nov 2024, rev 3 Nov 2025",
        "tier": 2,
        "role": "periodic exact pole dynamics, a = 0 and 1/2, sigma = 0 and 1 only",
        "locations": {"abstract": "read verbatim via arxiv.org/abs/2411.01891"},
    },
    {
        "key": "SAKAJO",
        "arxiv": None,
        "cite": (
            "Sakajo, Nonlinearity 16 (2003) 1319-1328; J. Math. Sci. Univ. Tokyo 10 "
            "(2003) 187-207 (= Xu refs [18], [19])"
        ),
        "tier": 3,
        "role": "a=0, arbitrary derivative order; thresholds IN nu, not d(exponent)/d(nu)",
        "locations": {},
    },
]

# The exact-solution corpus, which is why the gap is structural.
EXACT_SOLUTION_CORPUS = {
    "real_line": [[0, 0], [0, 1], [0, 2], [0.5, 1]],
    "periodic": [[0, 0], [0, 1], [0.5, 0], [0.5, 1]],
    "sigma_3_present": False,
}

GREPS = [
    {"file": "2607.19762.txt", "pattern": r"s\*|Table 1|critical|marginal|Appendix A"},
    {"file": "2207.07548.txt", "pattern": r"a = 1/2|sigma = 3|\(61\)|section headings"},
    {"file": "2010.01201.txt", "pattern": r"viscos|dissipat|Lambda\^|nu "},
    {"file": "1908.09385.txt", "pattern": r"a = 1/2|critical|self-similar exponent|s = 3"},
]

VERBATIM = {
    "xu_s_star_half": (
        "The branch value is tested at a = 1/2, where s* = 3 exactly (cl(1/2) = 1/3 by "
        "the exact solution of [20]; also [4, Thm. 2]) and J. Chen [20] proved blow-up "
        "at s = 2 < 3 (subcritical), consistent with persistence."
    ),
    "xu_table_1_row_a_half": "0.5   0.3333   0.833   3.000   J. Chen [20]: blow-up at s = 2 < 3 (subcritical)",
    "xu_fig_3_annotation": "s * (1/2) = 3 (exact)",
    "xu_marginal_open": (
        "That the inviscid profile then persists as the attractor is the program of "
        "Section 8, not established here (the required weighted dissipation-form bound, "
        "nonlinear estimate, and modulation closure are open, Appendix A); and s* is not "
        "the sharp critical dissipation curve separating blow-up from global regularity, "
        "which for this family remains unknown."
    ),
    "xu_marginal_label": (
        "The case s = s* is marginal (gamma = 0) and s > s* is relevant (the open "
        "supercritical regime)."
    ),
    "slsa_abstract_sigma_values": (
        "We derive new periodic solutions for a=0 and 1/2 and sigma=0 and 1, for which a "
        "closed collection of (periodically repeated) poles evolve in the complex plane."
    ),
}

# ---------------------------------------------------------------------------
# The corrections this leg REPORTS rather than applies (all three files are
# outside its territory; capabilities.py explicitly must not be edited here).
# ---------------------------------------------------------------------------
REPORTED_CORRECTIONS = [
    {
        "file": "capabilities.py",
        "where": "line 80, the solver/critical_dissipation.py entry's 'validated' field",
        "current": (
            "alpha_1 = 0 at a=0 == ALS eq (61); a=1/2 is UNSEARCHED at primary source"
        ),
        "proposed": (
            "alpha_1 = 0 at a=0 == ALS eq (61); criticality sigma=3 at a=1/2 IS "
            "published (XU arXiv:2607.19762 sec 6.1 + Table 1 row a=0.5 + Fig 3, "
            "'s*(1/2)=3 exactly'); alpha_1 = +0.133683 there is SEARCHED-NOT-FOUND "
            "(leg 64), i.e. measured, not independently validated"
        ),
        "why": (
            "the first clause is confirmed and stays; the second is stale in BOTH "
            "directions -- the criticality half is published, and the alpha_1 half is "
            "no longer unsearched"
        ),
    },
    {
        "file": "LITERATURE_CHECK.md",
        "where": "the row 'alpha_1 = +0.133683 at a = 1/2 | Route-H v1 | not in Tier 1 | unsearched'",
        "current": "source 'not in Tier 1'; verdict 'unsearched'",
        "proposed": (
            "source: XU sec 6.1 / Table 1 for the sigma=3 half (Tier 1 after all); "
            "verdict: 'searched -- not found' for alpha_1 itself"
        ),
        "why": "'not in Tier 1' is wrong for the criticality statement; Xu is Tier 1",
    },
    {
        "file": "PHASE2_P2_NOTES.md",
        "where": "J-2's parenthetical",
        "current": "(criticality there is sigma=3, in neither ALS nor XU)",
        "proposed": (
            "criticality there is sigma=3, which IS in XU (sec 6.1, Table 1, Fig 3) "
            "and is not in ALS; what is in neither is alpha_1 itself, and XU says in "
            "the same subsection that the marginal case s = s* is open"
        ),
        "why": (
            "the clause is false about XU.  The conclusion it supports survives; the "
            "corrected reason is stronger than the wrong one"
        ),
    },
]


def build() -> dict:
    last_two_spread = abs(ALPHA_1_LADDER[240] - ALPHA_1_LADDER[192])
    full_spread = abs(ALPHA_1_LADDER[240] - ALPHA_1_LADDER[96])
    return {
        "leg": 64,
        "route": "A12 v1",
        "pass_date": PASS_DATE,
        "kind": "literature classification -- no computation, no gCLM measurement",
        "gate": GATE,
        "gate_answer": {
            "sigma_3_criticality_at_a_half": "YES -- published, Tier 1, XU arXiv:2607.19762",
            "alpha_1_at_a_half": "NO -- searched and not found in any located source",
            "summary": (
                "the disjunction splits: the threshold is published and the "
                "coefficient at the threshold is not"
            ),
        },
        "quantity_definition": {
            "alpha_1": "d(alpha)/d(mu) at the marginal fixed point of the (Omega, mu) flow",
            "flow": "mu_tau = (2s - alpha[Omega, mu]) mu; at 2s = alpha_0, mu_tau = -alpha_1 mu^2 + O(mu^3)",
            "mu": "mu(tau) := nu / (A L^{2s}), the rescaled dissipation coefficient",
            "why_it_matters": (
                "alpha_1 > 0 => mu decays like 1/(alpha_1 tau), algebraically, so the "
                "critical viscous solution relaxes onto the inviscid profile"
            ),
            "source_module": "solver/critical_dissipation.py (Route-H v1)",
        },
        "our_number": {
            "value": ALPHA_1_LADDER[240],
            "a": 0.5,
            "sigma_critical": 3,
            "s_critical_our_gauge": 1.5,
            "ladder_K_to_alpha_1": {str(k): v for k, v in ALPHA_1_LADDER.items()},
            "spread_full_ladder": full_spread,
            "spread_last_two_rungs": last_two_spread,
            "distance_from_zero_in_last_rung_spreads": ALPHA_1_LADDER[240] / last_two_spread,
            "rigor": "float64, no interval enclosure, one basis, one instrument",
            "label": "measured, not independently validated",
        },
        "literature_number_for_the_published_half": {
            "xu_s_star_at_a_half": 3.0,
            "exact": True,
            "our_sigma_c_at_a_half": 3.0,
            "agreement": "identical, exactly 3 on both sides, under the exponent dictionary",
            "underlying_c_l_half": {
                "exact": 1.0 / 3.0,
                "xu_table_1_recompute": 0.3333,
                "this_repo_cold_integration_of_ALS_49_50": 0.3333076,
                "rel_error_this_repo_vs_exact": abs(0.3333076 - 1.0 / 3.0) / (1.0 / 3.0),
            },
        },
        "exponent_dictionary": {
            "als_xu_form": "omega ~ tau^{-beta} f(x/tau^{c_l})",
            "their_c_l": "our beta",
            "our_alpha": "1 / c_l",
            "their_Lambda_sigma": "our (-Delta)^s with sigma = 2s",
            "consequence": "s_c(ours) = alpha/2 = s*(XU)/2; at a=1/2, s* = 3 <=> sigma_c = 3",
            "warning": "get this wrong and every verdict inverts while still looking consistent",
        },
        "queries": QUERIES,
        "sources": SOURCES,
        "greps": GREPS,
        "verbatim": VERBATIM,
        "exact_solution_corpus": EXACT_SOLUTION_CORPUS,
        "traps": [
            {
                "id": "T1",
                "statement": (
                    "'critical dissipation' means two different things at a = 1/2 and "
                    "they differ by two units of sigma"
                ),
                "chen_norm_criticality_gamma": 1.0,
                "chen_norm_criticality_note": (
                    "from L^1 conservation, Chen's a > -1 regime; his gamma = |a|^-1 "
                    "formula (norm L^|a|) is stated only for a <= -1 and does not apply "
                    "at a = 1/2"
                ),
                "chen_theorem_1.1_dissipation_gamma": 2.0,
                "chen_theorem_1.1_note": (
                    "full Laplacian, his chosen instrument 'for simplicity' -- not a "
                    "criticality claim"
                ),
                "scaling_relevance_criticality_sigma": 3.0,
                "consequence": (
                    "Chen's theorem is SUBcritical in Xu's classification (gamma=2 or "
                    "gamma=1, either way below sigma=3) and does not touch the point in "
                    "question"
                ),
            },
            {
                "id": "T2",
                "statement": "ALS call sigma = 0 \"'marginal' dissipation\"",
                "consequence": "the bottom of the sigma range, not sigma = sigma_c; a false friend",
            },
        ],
        "reported_corrections": REPORTED_CORRECTIONS,
        "bans_respected": [
            "no gCLM measurement leg -- nothing here computes; alpha_1 is quoted from Route-H v1",
            "capabilities.py grepped before building; not edited (outside territory)",
        ],
    }


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "writeup", "data", "p2_route_a12_v1_alpha_lit.json")
    payload = build()
    with open(os.path.normpath(out), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")
    ans = payload["gate_answer"]
    print("Route-A12 v1 (leg 64) -- literature classification, no computation")
    print("  gate:", GATE)
    print("  sigma=3 at a=1/2 :", ans["sigma_3_criticality_at_a_half"])
    print("  alpha_1 at a=1/2 :", ans["alpha_1_at_a_half"])
    n = payload["our_number"]
    print(
        "  our number: alpha_1 = %.6f, ladder spread %.2e (full) / %.2e (last two), "
        "%.0fx the last-rung spread from zero"
        % (
            n["value"],
            n["spread_full_ladder"],
            n["spread_last_two_rungs"],
            n["distance_from_zero_in_last_rung_spreads"],
        )
    )
    print("  queries logged:", len(QUERIES), "| sources located:", len(SOURCES))
    print("  corrections REPORTED (not applied):", len(REPORTED_CORRECTIONS))
    print("  wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
