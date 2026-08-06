"""Route-EXT4 v1 (leg 90): has the RANK-4 target object's CONJECTURE been resolved since April 2026?

PURE LITERATURE LEG.  Nothing here computes a gCLM quantity -- nothing here computes anything at
all; the standing ban on further gCLM measurement legs is respected trivially.  This script is
the executable record of a search: it carries the query strings, the corpus enumerations (arXiv
API and TWO independent citation graphs, not keyword luck), the primary-source locations, and
the verbatim sentences, and re-emits them as
writeup/data/p2_route_ext4_v1_target_watch4.json.

WHAT WAS ASKED (the leg's gate, verbatim)
    "Has Chen-Huang-Li's Conjecture 2.4 (stability of the HL singular steady state) been proved
     or disproved, by anyone, since arXiv:2604.01868?"

WHAT CAME BACK: NO.  Ten channels, 0 of 10, at pass date 2026-08-06 -- 126 days after v1.

  The object is solver/target_selection.py's RANK-4 candidate HL_singular_steady_stability: the
  asymptotic stability of the 1D Hou-Luo SINGULAR steady state 1_{X>1}(X-1)^{-1/2}, whose
  EXISTENCE (in the weak sense) is Chen-Huang-Li's Theorem 2.3 and whose STABILITY is their
  Conjecture 2.4.

  This watch differs in KIND from legs 74/77/82.  Those three asked whether a CERTIFICATE had
  appeared for an uncertified-but-not-conjectural profile, and an absence answer there is only
  ever "still nobody has done it".  Here the watched item is a NAMED CONJECTURE with a stated
  claim, resolvable in EITHER direction: a disproof counts as loudly as a proof, and the search
  was run symmetrically for both (channel 4 and channel 7 would return an instability result as
  readily as a stability one).  Both directions came back empty.

  The source paper is still at v1.  It has never been revised.  Same shape of evidence as leg
  82's rank-3 watch and the same known weakness: this is an ABSENCE argument, with no positive
  act to point at.  What it has that legs 74/77/82 did not is a SECOND, independently built
  citation index (OpenAlex) agreeing with the first (Semantic Scholar) at zero.

THE FOUR FALSE FRIENDS, any of which produces a wrong YES from an abstract-only pass:

  FF1  Xu arXiv:2607.19762v1 (2026-07-22) -- the newest 1D-family entry, and the one that most
       looks like a stability resolution: it PROVES a spectral gap of 1/2 and an exact linear
       decay rate e^{-tau/2} for a self-similar profile of the CLM family.  Not this conjecture
       on four counts:
       FF1a  wrong PROFILE -- it linearizes about Omega(y) = -y/(y^2 + 1/4), the SMOOTH exact
             a = 0 CLM collapse profile.  Conjecture 2.4's object is UNBOUNDED at X = 1.
       FF1b  wrong MODEL -- CLM/gCLM (w_t + a u w_x = u_x w), not the Hou-Luo model, which
             carries a second field Theta and a second modulation constant c_omega.
       FF1c  the words are ABSENT -- "Hou-Luo"/"Hou--Luo" and "singular steady" each return 0
             hits in the full text.
       FF1d  no CONTACT -- 2604.01868 is not cited anywhere in it.  (It DOES cite the sibling
             paper 2603.25104 at reference [7], which is how it enters this leg's corpus at
             all.)  ALREADY KNOWN TO THIS REPOSITORY: Papers/fetch.sh lists 2607.19762 in
             TIER1 and Papers/MANIFEST.md gates Route-E v1's spectral picture on it.  It is
             not news; it is simply not this object.

  FF2  Bradshaw-Palmer arXiv:2606.22291v1 (2026-06-21) -- the ONLY 2026 entry on the
       "singular steady state" + "stability" channel, and it announces exactly the two words
       the gate is about: "The second objective of this paper is to establish asymptotic
       stability for many of these solutions".  Not this conjecture on three counts:
       FF2a  wrong EQUATION -- 3D STATIONARY Navier-Stokes (Landau solutions, Squire's
             solution, Serrin's swirling vortex), a viscous stationary problem.  The HL model
             is a 1D inviscid transport model, and the conjecture lives in dynamic rescaling
             coordinates around a BLOWUP profile.
       FF2b  wrong SINGULARITY -- an isolated point singularity of a stationary flow, "Type
             III" in that literature.  Conjecture 2.4's profile is singular at the free
             boundary X = 1 of a self-similar profile, and is only in L^p for p < 2.
       FF2c  no CONTACT -- 2604.01868 is not cited; the Hou-Luo model does not appear.

  FF3  Huang-Tong-Wang arXiv:2603.25104, revised to v2 on 2026-06-16 -- the SHARPEST false
       friend, because it is by the source paper's lead author, it is dated AFTER the source
       paper, and its abstract says "we rigorously prove the convergence of the outer profile
       to an explicit singular function in self-similar coordinates".  A convergence-to-a-
       singular-profile theorem, by De Huang, filed after 2604.01868, is precisely what a YES
       would look like.  It is not one, on four counts:
       FF3a  wrong MODEL -- the generalized Constantin-Lax-Majda model with parameter a, not
             the Hou-Luo model.  The paper's own title says so.
       FF3b  wrong STATEMENT -- what is proved at a = 0 is convergence of the OUTER profile
             for the specific constructed solution, plus existence of the inner traveling wave
             by a fixed-point method.  It is not an asymptotic-stability statement about a
             steady state under perturbation of initial data, which is what Conjecture 2.4
             asserts.
       FF3c  its own stability language is NUMERICAL, and says so: "This indicates that the
             self-similar blowup with a singular profile is robust with respect to the choice
             of degenerate initial data, hence suggesting stability of the observed blowup."
             SUGGESTING, from two cases agreeing to numerical error.  That is the same
             evidentiary status Conjecture 2.4 already has.
       FF3d  no CONTACT -- 2604.01868 is not cited (v1 of 2603.25104 predates it by 7 days,
             and the v2 revision did not add the citation).  "Hou-Luo" appears once, at line
             549 of the extracted text, listing prior work; "Conjecture 2.4" appears nowhere.

  FF4  Shi arXiv:2605.16322v1 (2026-05-05) -- the ONLY entry on the whole "Hou-Luo" corpus
       channel filed after the source paper.  Already excluded by leg 82 for the rank-3 object,
       and excluded again here for reasons that are DIFFERENT, because the object is different:
       FF4a  wrong OBJECT -- a closed (1+1)D BOUNDARY-JET reduction (system Q0, the
             first-order truncation phi_qq(x,1,t) = 0), not the HL singular steady state.
       FF4b  wrong QUESTION -- it proves finite-time BLOW-UP by a Riccati argument.  It makes
             no stability claim about any steady state, and exhibits no profile at all.
       FF4c  its own abstract disclaims its scope: "The theorem is therefore a blow-up result
             for the closed boundary-jet model, not for the unrestricted Boussinesq or Euler
             systems."
       FF4d  no CONTACT -- 2604.01868 is not cited.

  (Rampf-Kolluru arXiv:2601.02464 is excluded before content matters: it PREDATES the source
  paper by three months, so it cannot answer a gate scoped to "since arXiv:2604.01868".)

THE LEDGER ENTRY WAS VERIFIED FIELD BY FIELD against the repository's local copy
Papers/2604.01868.pdf -- the ledger's word was not taken for what the conjecture says.  In
particular the rank-4 entry's q2 note ("the obstruction is not the unknown count, it is the
SPACE") is confirmed by the conjecture's OWN wording, which leaves the norm unnamed: "under
suitable normalization conditions, for any degenerate smooth initial data (omega_0, theta_0)
which is sufficiently close to (omega_bar, theta_bar) in some norm ||.||, the solution of the
Cauchy problem (2.4) converges to (Omega_bar, Theta_bar) in ||.||".  SOME NORM.  The conjecture
does not name its own function space.  See PRIMARY_SOURCE below.

CONSEQUENCE FOR THE LEDGER (reported, never applied -- solver/target_selection.py is PARKED
pending the user's ruling on leg 63's escalation and is NOT touched by this leg):
    its HL_singular_steady_stability entry, field "certified": "NO", and its q1 text "Stability
    is an explicitly stated conjecture with numerical support only", are CURRENT as of
    2026-08-06, not stale.  Two precision suggestions only, both bookkeeping, in
    GATE_ANSWER below.

USAGE
    python experiments/p2_route_ext4_v1_target_watch4.py
"""

import json
import os

GATE = (
    "Has Chen-Huang-Li's Conjecture 2.4 (stability of the HL singular steady state) been "
    "proved or disproved, by anyone, since arXiv:2604.01868?"
)

PASS_DATE = "2026-08-06"
SOURCE_V1_DATE = "2026-04-02"
DAYS_OPEN = 126  # 2026-04-02 -> 2026-08-06

# ---------------------------------------------------------------------------
# The channels, verbatim, in the order issued.  Every arXiv-API URL re-runs.
# ---------------------------------------------------------------------------

CHANNELS = [
    {
        "id": "C1",
        "name": "the source paper's own version history",
        "kind": "arXiv API id_list, the Atom <updated> field",
        "url": "https://export.arxiv.org/api/query?id_list=2604.01868&max_results=1",
        "enumerated": "the full submission history of 2604.01868",
        "result": (
            "v1 ONLY -- <id>http://arxiv.org/abs/2604.01868v1</id>, "
            "<published>2026-04-02T10:25:28Z</published>, "
            "<updated>2026-04-02T10:25:28Z</updated>.  No v2 at 126 days."
        ),
        "candidates": 0,
        "note": (
            "the single strongest channel: when these authors change their mind about a "
            "conjecture's status, the revision is where it shows.  For the rank-2 object "
            "(leg 77) a v2 at 82 days settled the question.  Here there is no v2 at 126 days"
        ),
        "sufficient_alone": True,
    },
    {
        "id": "C2",
        "name": "all three authors, enumerated separately",
        "kind": "arXiv API author enumeration",
        "url": [
            "https://export.arxiv.org/api/query?search_query=au:%22De_Huang%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=60",
            "https://export.arxiv.org/api/query?search_query=au:%22Bojin_Chen%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=60",
            "https://export.arxiv.org/api/query?search_query=au:%22Xiangyuan_Li%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=60",
        ],
        "enumerated": "24 + 2 + 4 = 30 entries across the three queries, date-descending",
        "result": (
            "De Huang's newest entry IS 2604.01868v1 itself; the next-newest is 2603.25104 "
            "(v1 2026-03-26, v2 2026-06-16 -- FF3).  Bojin Chen and Xiangyuan Li have nothing "
            "after it either.  NOT ONE of the three has filed anything, in any field, since "
            "2026-04-02.  (Two of De Huang's 24 are name collisions -- an ALMA receiver paper "
            "and a bilayer-manganites paper -- and are excluded on sight.)"
        ),
        "candidates": 0,
        "note": (
            "the ONE post-source act by any author is a REVISION of a sibling paper, not a new "
            "filing, and that revision is FF3: it neither cites 2604.01868 nor mentions "
            "Conjecture 2.4"
        ),
        "sufficient_alone": True,
    },
    {
        "id": "C3",
        "name": 'the whole "Hou-Luo" corpus',
        "kind": "arXiv API full-text-field enumeration",
        "url": [
            "https://export.arxiv.org/api/query?search_query=all:%22Hou-Luo%22"
            "&sortBy=submittedDate&sortOrder=descending&max_results=60",
            "https://export.arxiv.org/api/query?search_query=ti:%22Hou-Luo%22+OR+"
            "ti:%22Hou--Luo%22&sortBy=submittedDate&sortOrder=descending&max_results=60",
        ],
        "enumerated": "7 entries on all:, 6 on ti:, 3 of them from 2026 in both cases",
        "result": (
            "2605.16322v1 Shi (= FF4, the ONLY entry filed after the source paper); "
            "2604.01868v1 (the source paper); 2601.02464v1 Rampf-Kolluru (predates by three "
            "months, out of scope).  The other four are 2308.01528, 2106.05422, 2010.00648, "
            "1604.07118 -- all pre-2026 and all about the SMOOTH profile or the boundary layer"
        ),
        "candidates": 0,
        "sufficient_alone": True,
    },
    {
        "id": "C4",
        "name": "the conjecture's own subject matter",
        "kind": "arXiv API abstract-field enumeration",
        "url": "https://export.arxiv.org/api/query?search_query=abs:%22singular+steady+state%22"
               "+AND+abs:%22stability%22&sortBy=submittedDate&sortOrder=descending"
               "&max_results=60",
        "enumerated": "4 entries total, 1 of them from 2026",
        "result": (
            "the only 2026 entry is 2606.22291v1 Bradshaw-Palmer (= FF2, excluded on 3 "
            "counts).  The rest are 2309.15633 (Keller-Segel), 2110.12934 (viscous "
            "Hamilton-Jacobi) and 0904.3759 (nonlinear heat) -- none a fluid transport model"
        ),
        "candidates": 0,
        "note": (
            "this channel is DIRECTION-SYMMETRIC: 'stability vs. instability' papers index "
            "here too (2309.15633's own title is exactly that), so a DISPROOF of Conjecture "
            "2.4 would have surfaced on this channel as readily as a proof"
        ),
        "sufficient_alone": True,
    },
    {
        "id": "C5",
        "name": "the profile's own adjective",
        "kind": "arXiv API abstract-field enumeration",
        "url": "https://export.arxiv.org/api/query?search_query=abs:%22self-similar%22+AND+"
               "abs:%22singular+profile%22&sortBy=submittedDate&sortOrder=descending"
               "&max_results=60",
        "enumerated": "4 entries total, 1 of them from 2026",
        "result": (
            "the only 2026 entry IS the source paper.  The others are 2410.21765 "
            "(Abe-Ginsberg-Jeong, stationary 2D Boussinesq self-similar profiles, 2024), "
            "1306.0859 (Yamabe flow) and physics/0410119 (liquid-metal cusps)"
        ),
        "candidates": 0,
        "sufficient_alone": True,
    },
    {
        "id": "C6",
        "name": "the adjacent 1D family",
        "kind": "arXiv API abstract-field enumeration",
        "url": "https://export.arxiv.org/api/query?search_query=abs:%22Constantin-Lax-Majda%22"
               "&sortBy=submittedDate&sortOrder=descending&max_results=60",
        "enumerated": "25 entries total, 5 of them from 2026",
        "result": (
            "2607.19762v1 Xu (= FF1); 2604.01244v4 Shi; 2603.25104v2 Huang-Tong-Wang (= FF3); "
            "2603.26715v5 Shi; 2603.06182v1 Fujita-Fukuizumi-Sakajo (ergodicity, predates).  "
            "The two Shi entries are the same boundary-jet programme as FF4 and fail on the "
            "same counts"
        ),
        "candidates": 0,
        "note": (
            "run because the HL and gCLM literatures share authors and machinery: if anyone "
            "resolved Conjecture 2.4 by transporting a gCLM argument, this is where it lands"
        ),
        "sufficient_alone": True,
    },
    {
        "id": "C7",
        "name": "stability-of-blowup generally",
        "kind": "arXiv API abstract-field enumeration",
        "url": [
            "https://export.arxiv.org/api/query?search_query=abs:%22asymptotic+stability%22"
            "+AND+abs:%22blowup%22&sortBy=submittedDate&sortOrder=descending&max_results=60",
            "https://export.arxiv.org/api/query?search_query=abs:%22degenerate%22+AND+"
            "abs:%22self-similar+blowup%22&sortBy=submittedDate&sortOrder=descending"
            "&max_results=60",
        ],
        "enumerated": "20 entries on the first, 1 on the second",
        "result": (
            "the newest on the first is 2603.01924 (wave maps, 2026-03-02) -- it PREDATES the "
            "source paper, so the whole channel is empty of post-source candidates.  The "
            "corpus is wave maps / Yang-Mills / NLS / harmonic-map heat flow blowup stability: "
            "no 1D transport model, no Hou-Luo, no singular steady state.  The second returns "
            "only 2510.25326 (supercritical wave maps with additive noise, 2025)"
        ),
        "candidates": 0,
        "sufficient_alone": True,
    },
    {
        "id": "C8",
        "name": "the citation graph (index 1 of 2)",
        "kind": "Semantic Scholar graph API",
        "url": [
            "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868/citations"
            "?fields=title,year,externalIds,abstract&limit=100",
            "https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868"
            "?fields=title,citationCount,year",
        ],
        "enumerated": "every indexed citation of the source paper",
        "result": (
            '{"offset": 0, "data": []} -- an EMPTY array; the paper record itself reports '
            '"citationCount": 0, paperId 7d3062ed647f390d9a2f28231a3383871534bf33'
        ),
        "candidates": 0,
        "note": (
            "CORROBORATING ONLY, and explicitly NOT treated as decisive: this index lags arXiv "
            "by weeks, so an empty array is as consistent with indexing lag as with genuine "
            "absence.  Reported because it AGREES, not because it PROVES"
        ),
        "sufficient_alone": False,
    },
    {
        "id": "C9",
        "name": "the citation graph (index 2 of 2, INDEPENDENTLY BUILT)",
        "kind": "OpenAlex works API",
        "url": [
            "https://api.openalex.org/works/doi:10.48550/arXiv.2604.01868"
            "?select=id,title,cited_by_count,publication_date",
            "https://api.openalex.org/works?filter=cites:W7148668037&per-page=25",
        ],
        "enumerated": "every work OpenAlex records as citing W7148668037",
        "result": (
            'the work resolves to W7148668037 with "cited_by_count": 0 and '
            '"publication_date": "2026-04-02"; the cites: filter returns '
            '{"count": 0}, results []'
        ),
        "candidates": 0,
        "note": (
            "THIS IS THE CHANNEL LEGS 74/77/82 DID NOT RUN.  Two citation indexes with "
            "different ingest pipelines, both empty, is materially stronger than either alone "
            "-- it makes 'indexing lag' have to be a coincidence across two independent "
            "pipelines.  Still corroborating rather than sufficient: both index arXiv, and a "
            "common upstream delay is not fully excluded"
        ),
        "sufficient_alone": False,
    },
    {
        "id": "C10",
        "name": "the authors' own homepage, and the open web",
        "kind": "direct fetch + open-web search",
        "url": [
            "https://sites.google.com/view/de-huang/research",
            "search: Chen Huang Li Conjecture 2.4 stability singular steady state Hou-Luo "
            "model 2026 proof",
            'search: arXiv 2026 "asymptotic stability" singular steady state 1D Hou-Luo model '
            "weak solution proof",
        ],
        "enumerated": "the corresponding author's own preprint list, plus two open-web passes",
        "result": (
            "the homepage's 'Recent Preprints' section lists exactly two items -- 2603.25104 "
            "and 2604.01868 -- and nothing newer; its 2026 publication is the Bernoulli Markov-"
            "chain paper, unrelated.  The open-web passes returned the source paper, "
            "2601.02464, 2106.05422, 2308.01528 and unrelated chemotaxis/Keller-Segel spiky-"
            "steady-state stability work.  No resolution, in either direction"
        ),
        "candidates": 0,
        "note": (
            "the homepage matters because it is the one channel that can show a manuscript "
            "BEFORE arXiv -- authors list submitted-but-unposted work there.  It shows none"
        ),
        "sufficient_alone": False,
    },
]

# ---------------------------------------------------------------------------
# The false friends, opened and excluded on named grounds.
# ---------------------------------------------------------------------------

FALSE_FRIENDS = [
    {
        "id": "FF1",
        "arxiv": "2607.19762v1",
        "date": "2026-07-22",
        "authors": ["Jie Xu"],
        "title": ("The spectral picture of self-similar collapse in the "
                  "Constantin-Lax-Majda equation"),
        "why_it_looks_like_a_yes": (
            "it is the newest 1D-family entry and it PROVES stability-flavoured statements: a "
            "spectral gap of 1/2 after modulation, full point spectrum exactly {0,1} with no "
            "embedded eigenvalues, and an exact linear decay rate e^{-tau/2} in closed form"
        ),
        "excluded_on": [
            ("FF1a wrong PROFILE -- it linearizes about Omega(y) = -y/(y^2 + 1/4), the SMOOTH "
             "exact a = 0 CLM collapse profile.  Conjecture 2.4's steady state is UNBOUNDED "
             "at X = 1 and lies in L^p only for p < 2; no origin-H^2 realization holds it"),
            ("FF1b wrong MODEL -- CLM/gCLM, w_t + a u w_x = u_x w with u_x = Hw, a single "
             "field.  The HL model carries a second field Theta and a second modulation "
             "constant c_omega"),
            ("FF1c the words are ABSENT -- 'Hou-Luo'/'Hou--Luo' and 'singular steady' each "
             "return 0 hits in the extracted full text"),
            ("FF1d no CONTACT -- 2604.01868 is not cited.  It cites the sibling 2603.25104 at "
             "reference [7], which is the only reason it enters this leg's corpus"),
        ],
        "already_known_here": (
            "Papers/fetch.sh lists 2607.19762 in TIER1 and Papers/MANIFEST.md gates Route-E "
            "v1's spectral picture on it ('already assessed as likely pre-empted').  This leg "
            "does not discover it and does not re-open that assessment -- it only records that "
            "the paper is NOT a resolution of Conjecture 2.4"
        ),
        "flag_for_the_orchestrator": (
            "orthogonal to this gate, but worth one line: 2607.19762 gives a full spectral "
            "picture of the a = 0 CLM linearization L_0, including a realization dichotomy and "
            "a non-normality caveat ('a spectral gap does not by itself give a decay rate in "
            "the X norm').  That is the SAME operator the NG stage's no-go is stated about.  "
            "Reported, not acted on: NG is not this leg's territory"
        ),
    },
    {
        "id": "FF2",
        "arxiv": "2606.22291v1",
        "date": "2026-06-21",
        "authors": ["Zachary Bradshaw", "Dakota Palmer"],
        "title": "Singular stationary Navier-Stokes flows: examples and stability",
        "why_it_looks_like_a_yes": (
            "the only 2026 entry on the 'singular steady state' + 'stability' channel, and its "
            "abstract announces the gate's own words: 'The second objective of this paper is "
            "to establish asymptotic stability for many of these solutions'"
        ),
        "excluded_on": [
            ("FF2a wrong EQUATION -- 3D STATIONARY Navier-Stokes: Landau solutions, Squire's "
             "solution, Serrin's swirling vortex.  A viscous stationary problem.  The HL model "
             "is a 1D inviscid transport model and Conjecture 2.4 lives in dynamic-rescaling "
             "coordinates around a BLOWUP profile"),
            ("FF2b wrong SINGULARITY -- an isolated point singularity at the origin of a "
             "stationary flow ('Type III' in that literature).  Conjecture 2.4's profile is "
             "singular at X = 1, the edge of a one-sided support, and is L^p only for p < 2"),
            ("FF2c no CONTACT -- 2604.01868 is not cited; the Hou-Luo model does not appear"),
        ],
    },
    {
        "id": "FF3",
        "arxiv": "2603.25104",
        "date": "v1 2026-03-26, v2 2026-06-16",
        "authors": ["De Huang", "Jiajun Tong", "Xiuyuan Wang"],
        "title": ("Self-similar finite-time blowups with singular profiles of the generalized "
                  "Constantin-Lax-Majda model: theoretical and numerical investigations"),
        "why_it_looks_like_a_yes": (
            "THE SHARPEST ONE.  By the source paper's own lead author; REVISED after the "
            "source paper (v2 at 2026-06-16, 75 days after 2604.01868v1); and its abstract "
            "says 'we rigorously prove the convergence of the outer profile to an explicit "
            "singular function in self-similar coordinates'.  A rigorous "
            "convergence-to-a-singular-profile theorem by De Huang, filed after the "
            "conjecture, is exactly the shape a YES would have"
        ),
        "excluded_on": [
            ("FF3a wrong MODEL -- the generalized Constantin-Lax-Majda model with parameter a. "
             "Its own title says so.  Not the Hou-Luo model"),
            ("FF3b wrong STATEMENT -- at a = 0 it proves convergence of the OUTER profile for "
             "the constructed solution, plus existence of the inner traveling wave by a "
             "fixed-point method.  Neither is an asymptotic-stability statement about a steady "
             "state under perturbation of initial data, which is what Conjecture 2.4 asserts"),
            ("FF3c its own stability language is NUMERICAL and says so, verbatim: 'This "
             "indicates that the self-similar blowup with a singular profile is robust with "
             "respect to the choice of degenerate initial data, hence suggesting stability of "
             "the observed blowup.'  SUGGESTING, from two initial-data cases agreeing to "
             "numerical error -- the same evidentiary status Conjecture 2.4 already has"),
            ("FF3d no CONTACT -- 2604.01868 is not cited (v1 predates it by 7 days, and the v2 "
             "revision did not add the citation).  'Hou-Luo' appears once, listing prior work; "
             "'Conjecture 2.4' appears nowhere in the extracted full text"),
        ],
        "what_the_v2_revision_is_evidence_OF": (
            "read the other way, this is the leg's strongest POSITIVE datum, and the thing "
            "leg 82's rank-3 watch lacked: the lead author DID touch the sibling paper 75 days "
            "after announcing Conjecture 2.4, and did not use the occasion to announce a "
            "resolution, add a citation, or upgrade the conjecture's status.  That is an act, "
            "not a silence"
        ),
    },
    {
        "id": "FF4",
        "arxiv": "2605.16322v1",
        "date": "2026-05-05",
        "authors": ["Yaoming Shi"],
        "title": ("A unified Boussinesq--Euler formulation and finite-time blow-up for a "
                  "Hou--Luo type boundary-jet system"),
        "why_it_looks_like_a_yes": (
            "the ONLY entry in the entire 'Hou-Luo' corpus filed after the source paper, and "
            "it carries a genuine PROVED theorem"
        ),
        "excluded_on": [
            ("FF4a wrong OBJECT -- a closed (1+1)D BOUNDARY-JET reduction (system Q0, the "
             "first-order Taylor truncation phi_qq(x,1,t) = 0), not the HL singular steady "
             "state"),
            ("FF4b wrong QUESTION -- finite-time BLOW-UP by a Riccati argument.  No stability "
             "claim about any steady state, and no profile exhibited at all"),
            ("FF4c its own abstract disclaims its scope: 'The theorem is therefore a blow-up "
             "result for the closed boundary-jet model, not for the unrestricted Boussinesq "
             "or Euler systems.'"),
            ("FF4d no CONTACT -- 2604.01868 is not cited"),
        ],
        "note": (
            "leg 82 excluded this same paper for the RANK-3 object on different grounds "
            "(wrong object / wrong kind / no computer assistance / no contact).  The grounds "
            "differ here because the watched object differs; the paper is a false friend for "
            "both, for non-identical reasons"
        ),
    },
]

OUT_OF_SCOPE = [
    {
        "arxiv": "2601.02464v1",
        "date": "2026-01-05",
        "authors": ["Cornelius Rampf", "Sai Swetha Venkata Kolluru"],
        "title": "Complex-time singular structure of the 1D Hou-Luo model",
        "excluded_before_content_matters": (
            "PREDATES the source paper by three months.  A gate scoped to 'since "
            "arXiv:2604.01868' cannot be answered by it, whatever it contains"
        ),
    },
    {
        "arxiv": "2604.16842v1",
        "date": "2026-04-18",
        "title": ("Singularity Formation: Synergy in Theoretical, Numerical and Machine "
                  "Learning Approaches"),
        "excluded_before_content_matters": (
            "surfaced by the open-web channel and postdates the source paper, but it is a PhD "
            "THESIS on NLH / CGL / 3D Keller-Segel with logistic damping, PINNs and "
            "Kolmogorov-Arnold networks.  No Hou-Luo model, no singular steady state, no "
            "conjecture resolution"
        ),
    },
]

# ---------------------------------------------------------------------------
# Primary-source verification -- the ledger's word was not taken.
# ---------------------------------------------------------------------------

PRIMARY_SOURCE = {
    "local_copy": "Papers/2604.01868.pdf (gitignored; re-pull with bash Papers/fetch.sh 2604.01868)",
    "extraction": "pdftotext -f 1 -l 30",
    "conjecture_2_4_verbatim": (
        "Conjecture 2.4. The singular steady state (Omega_bar, Theta_bar, c_bar_l, c_bar_omega) "
        "is asymptotically stable. More specifically, under suitable normalization conditions, "
        "for any degenerate smooth initial data (omega_0, theta_0) which is sufficiently close "
        "to (omega_bar, theta_bar) in some norm ||.||, the solution of the Cauchy problem (2.4) "
        "converges to (Omega_bar, Theta_bar) in ||.||."
    ),
    "theorem_2_3_verbatim_core": (
        "Theorem 2.3. In the weak sense, (omega_bar, theta_bar) = (1_{x>0}/(2 sqrt(x)), "
        "pi 1_{x>0}) solves the steady state equation of (1.1).  Moreover, (Omega_bar, "
        "Theta_bar, c_bar_l, c_bar_omega) [solves the corresponding rescaled steady state]"
    ),
    "what_this_confirms_in_the_ledger": [
        ("the rank-4 entry's q1 -- 'Existence in the weak sense is PROVED (their Theorem 5.3). "
         "Stability is an explicitly stated conjecture with numerical support only' -- is "
         "EXACT.  Theorem 2.3 says 'In the weak sense'; Conjecture 2.4 is labelled Conjecture"),
        ("the rank-4 entry's q2 note -- 'the obstruction is not the unknown count, it is the "
         "SPACE' -- is confirmed by the conjecture's OWN wording, which leaves the norm "
         "unnamed: 'in some norm ||.||'.  The conjecture does not name its own function "
         "space.  That is not this repository's reading of the paper; it is the paper"),
        ("the paper's section 1 states the mechanism the entry's 'p < 2' note refers to: the "
         "solution 'is locally unbounded at some point' and develops 'a local L^p blowup at a "
         "later time T > T_tilde for some p > 0'"),
        ("the paper's own comparison to the smooth-profile line -- section 2 records that "
         "earlier work used 'a weighted H^1 norm ||.||' and showed the solution stays within a "
         "neighbourhood -- makes the gap explicit: the weighted-H^1 route that worked for the "
         "SMOOTH profile is exactly what the singular profile denies"),
    ],
    "what_this_does_NOT_confirm": (
        "the entry's published constants c_l = 2.0, c_omega = -1.0 were NOT re-derived here.  "
        "capabilities.py already records them as validated in solver/hl_rescaled.py ('the "
        "exact Thm-2.3 singular anchor is a steady state on its support'), and re-deriving "
        "them would be a computation this leg is not chartered for"
    ),
}

# ---------------------------------------------------------------------------
# The answer.
# ---------------------------------------------------------------------------

GATE_ANSWER = {
    "verdict": "NO",
    "meaning": (
        "Chen-Huang-Li's Conjecture 2.4 has been NEITHER PROVED NOR DISPROVED, by anyone, in "
        "the enumerated corpora, as of 2026-08-06.  It is still open, 126 days after v1"
    ),
    "pass_date": PASS_DATE,
    "days_open": DAYS_OPEN,
    "source_versions_existing": 1,
    "source_revisions_since_v1": 0,
    "channels_run": 10,
    "channels_returning_a_candidate": 0,
    "channels_sufficient_alone": 6,
    "author_entries_enumerated": 30,
    "author_entries_after_source": 0,
    "author_revisions_after_source": 1,   # 2603.25104 v1 -> v2, and it is FF3
    "indexed_citations_semantic_scholar": 0,
    "indexed_citations_openalex": 0,
    "independent_citation_indexes_agreeing_at_zero": 2,
    "false_friends_opened_and_excluded": 4,
    "out_of_scope_items_recorded": 2,
    "direction_symmetry": (
        "the search was run for BOTH directions.  A disproof (instability, an unstable "
        "eigenvalue, a non-uniqueness obstruction) would surface on C4 -- whose corpus "
        "contains 'Stability vs. instability of singular steady states...' as a member -- and "
        "on C7, and would cite the source paper, hence C8/C9.  All empty.  This is not a "
        "one-sided watch"
    ),
    "known_weakness": (
        "every channel is an ABSENCE argument.  What this leg has that leg 82's rank-3 watch "
        "did not: (i) a SECOND independently built citation index (OpenAlex) agreeing at zero, "
        "and (ii) one genuine POSITIVE act -- the lead author revised the sibling paper "
        "2603.25104 to v2 on 2026-06-16, 75 days after announcing Conjecture 2.4, and did not "
        "use the occasion to announce a resolution or even add a citation.  What it still "
        "lacks is any statement BY the authors that the conjecture remains open; the evidence "
        "is that nobody has said otherwise"
    ),
    "why_a_resolution_would_matter_more_here_than_at_ranks_1_3": (
        "ranks 1-3 are UNCERTIFIED objects: an absence answer there means only that nobody has "
        "done the work yet, and the ledger entry is unchanged either way.  Rank 4 is a NAMED "
        "CONJECTURE: a proof would move HL_singular_steady_stability from 'open problem before "
        "the certificate is even posed' to 'certifiable target with a known function space', "
        "and a DISPROOF would delete it from the ledger outright, because an unstable steady "
        "state is not a blow-up mechanism.  Either direction is consequential; neither has "
        "happened"
    ),
    "ledger_consequence": (
        "target_selection.py's rank-4 HL_singular_steady_stability entry -- 'certified': 'NO', "
        "and q1's 'Stability is an explicitly stated conjecture with numerical support only' "
        "-- is CURRENT as of 2026-08-06, not stale.  Bank the dated watch entry.  NO EDIT "
        "REQUIRED and none made: the file is PARKED pending the user's ruling on leg 63's "
        "escalation and was READ only"
    ),
    "ledger_precision_suggestions": [
        ("the entry's 'source' field cites the paper WITHOUT a version.  Only v1 exists as of "
         "this pass, so pinning it to '2604.01868v1' costs nothing and makes a future revision "
         "detectable by diff rather than by re-reading.  Same suggestion leg 82 made for the "
         "rank-3 entry; it applies verbatim here"),
        ("the entry's q2 note says the profile 'is only in L^p for p < 2'.  The paper's own "
         "phrasing in section 1 is looser -- 'a local L^p blowup ... for some p > 0' -- and "
         "the p < 2 threshold is a consequence of the explicit profile, not a sentence in the "
         "paper.  Recording it as DERIVED rather than QUOTED would keep the ledger's "
         "provenance clean.  A bookkeeping nicety, not a correction"),
    ],
}

NEXT_REASK = {
    "object": "HL_singular_steady_stability",
    "source": "arXiv:2604.01868v1 Theorem 2.3 (existence) + Conjecture 2.4 (open)",
    "last_pass": PASS_DATE,
    "last_verdict": "NO -- still open",
    "cheapest_sufficient_channels_in_order_of_value": [
        "https://export.arxiv.org/api/query?id_list=2604.01868 -- a v2 is the single strongest "
        "signal, exactly as it was for the rank-2 object at leg 77",
        "https://export.arxiv.org/api/query?search_query=au:%22De_Huang%22"
        "&sortBy=submittedDate&sortOrder=descending",
        "https://api.openalex.org/works?filter=cites:W7148668037 -- the cheapest single call "
        "that would surface ANY citing work, in either direction",
        "https://export.arxiv.org/api/query?search_query=abs:%22singular+steady+state%22+AND+"
        "abs:%22stability%22&sortBy=submittedDate&sortOrder=descending",
    ],
    "interval_advice": (
        "SHORTER than the rank-3 watch's.  A named conjecture is a target people aim at, and "
        "the first citation of the source paper -- whichever index catches it -- is the event "
        "to watch for.  Both indexes are at zero now, so the next pass has a cheap, sharp "
        "trigger: any nonzero cited_by_count at all"
    ),
    "what_would_make_this_watch_UNNECESSARY": (
        "the user's ruling on leg 63's escalation.  If target_selection.py is unparked and the "
        "rank-4 entry is retired or promoted on other grounds, the watch's consumer disappears"
    ),
}

RELATED_WATCHES = [
    {"leg": 74, "route": "EXT", "rank": 1, "object": "HL_S2_nonsymmetric",
     "kind": "certificate watch", "source": "arXiv:2604.01868 sections 2.5/4", "verdict": "NO"},
    {"leg": 77, "route": "EXT2", "rank": 2, "object": "gCLM_degenerate_one_scale",
     "kind": "certificate watch", "source": "arXiv:2603.25104 section 4", "verdict": "NO"},
    {"leg": 82, "route": "EXT3", "rank": 3, "object": "Boussinesq_S2_nonsymmetric",
     "kind": "certificate watch", "source": "arXiv:2604.01868 section 6.2", "verdict": "NO"},
    {"leg": 90, "route": "EXT4", "rank": 4, "object": "HL_singular_steady_stability",
     "kind": "CONJECTURE-RESOLUTION watch (either direction)",
     "source": "arXiv:2604.01868 Conjecture 2.4", "verdict": "NO -- still open"},
]

INDEPENDENCE = (
    "shares a PAPER with legs 74 and 82 but not a section, not an object, and not a question.  "
    "Leg 74 watched the 1D non-symmetric REGULAR profile (sections 2.5/4); leg 82 the 2D "
    "Boussinesq analogue (section 6.2); this leg the SINGULAR steady state of Theorem 2.3 and "
    "the conjecture attached to it.  The question differs in kind as well as object: those "
    "three asked 'has a certificate appeared?', a one-sided existence question; this asks 'has "
    "a conjecture been resolved?', which is two-sided and which a DISPROOF answers as loudly "
    "as a proof.  Leg 77 shares neither paper nor object.  solver/target_selection.py was READ "
    "and never written -- it is parked pending the user's ruling on leg 63's escalation."
)

CAPABILITIES_GREP = (
    "capabilities.py was grepped before anything else, per the plan of record's permanent ban "
    "on building without it.  solver/hl_rescaled.py is registered at line 45 and its validated "
    "field already carries this leg's object: 'the exact Thm-2.3 singular anchor is a steady "
    "state on its support'.  solver/target_selection.py is registered at line 387.  So the "
    "anchor for the rank-4 object EXISTS and is validated, and nothing needed building -- "
    "which is just as well, since this leg is chartered to build nothing.  Nothing was built, "
    "so nothing was rebuilt."
)


def build_record() -> dict:
    """Assemble the curated record.  No computation -- this is a search log."""
    return {
        "leg": 90,
        "route": "EXT4 v1",
        "pass_date": PASS_DATE,
        "kind": ("literature watch -- no computation, no gCLM measurement, no solver touched, "
                 "no figure"),
        "gate": GATE,
        "gate_answer": GATE_ANSWER,
        "object": {
            "ledger_id": "HL_singular_steady_stability",
            "ledger_module": "solver/target_selection.py",
            "ledger_rank": 4,
            "ledger_status": "PARKED pending the user's ruling on leg 63's escalation; READ ONLY here",
            "arxiv": "2604.01868",
            "version_at_pass": "v1 (only)",
            "v1_date": SOURCE_V1_DATE,
            "locations": "Theorem 2.3 (existence, weak sense) + Conjecture 2.4 (stability, open)",
            "title": ("Novel Self-similar Finite-time Blowups with Singular Profiles of the "
                      "1D Hou-Luo Model and the 2D Boussinesq Equations: A Numerical "
                      "Investigation"),
            "authors": ["Bojin Chen", "De Huang", "Xiangyuan Li"],
            "object_in_question": (
                "the asymptotic stability of the 1D Hou-Luo SINGULAR steady state "
                "1_{X>1}(X-1)^{-1/2} -- a profile UNBOUNDED at X = 1, in L^p only for p < 2, "
                "with two modulation constants (c_l = 2, c_omega = -1, exact, c_l + 2 c_omega "
                "= 0) and one Hilbert transform on R"
            ),
        },
        "channels": CHANNELS,
        "false_friends": FALSE_FRIENDS,
        "out_of_scope": OUT_OF_SCOPE,
        "primary_source_verification": PRIMARY_SOURCE,
        "related_watches": RELATED_WATCHES,
        "independence": INDEPENDENCE,
        "capabilities_grep": CAPABILITIES_GREP,
        "next_reask": NEXT_REASK,
        "writeup": "writeup/novelty/leg_90.md",
    }


def main() -> None:
    record = build_record()
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_ext4_v1_target_watch4.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(record, fh, indent=1)
        fh.write("\n")

    ga = GATE_ANSWER
    print(f"Route-EXT4 v1 (leg 90) -- literature watch, pass date {PASS_DATE}")
    print(f"  gate: {GATE}")
    print(f"  VERDICT: {ga['verdict']} -- {ga['meaning']}")
    print(f"  channels run: {ga['channels_run']}, "
          f"returning a candidate: {ga['channels_returning_a_candidate']}, "
          f"sufficient alone: {ga['channels_sufficient_alone']}")
    print(f"  days open: {ga['days_open']}   "
          f"source versions existing: {ga['source_versions_existing']}   "
          f"revisions since v1: {ga['source_revisions_since_v1']}")
    print(f"  author entries enumerated: {ga['author_entries_enumerated']}, "
          f"filed after source: {ga['author_entries_after_source']}, "
          f"revisions after source: {ga['author_revisions_after_source']}")
    print(f"  indexed citations: Semantic Scholar "
          f"{ga['indexed_citations_semantic_scholar']}, OpenAlex "
          f"{ga['indexed_citations_openalex']} "
          f"({ga['independent_citation_indexes_agreeing_at_zero']} independent indexes, "
          f"corroborating only)")
    print(f"  false friends opened and excluded: "
          f"{ga['false_friends_opened_and_excluded']}; "
          f"out-of-scope items recorded: {ga['out_of_scope_items_recorded']}")
    print(f"  ledger: {ga['ledger_consequence']}")
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
