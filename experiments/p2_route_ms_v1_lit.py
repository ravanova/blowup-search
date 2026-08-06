"""P2 Route-MS v1 (leg 113) -- does any published CERTIFIED INVISCID self-similar
blow-up use a DIAGONAL-TAIL (ell^1-multiplier / radii-polynomial) framework?

A LITERATURE leg.  No solve runs under either branch of the gate; the only computation
here is string search over full texts and boolean algebra over a curated ledger.

THE GATE, verbatim from DIRECTION.md section 113:

    "Does any published certified INVISCID self-similar blow-up use a diagonal-tail
     (ell-1-multiplier / radii-polynomial) framework for its linearized tail estimate?"

    ANSWER: NO.  0 of 7 in-population rows, and 0 of 5 after every judgement call in the
    population rule is resolved the OTHER way (see gate_answers()).  The two rows that DO
    run a diagonal tail fail the population rule on two DIFFERENT clauses, and a fictitious
    SYNTHETIC_CONTROL row satisfying both conjuncts flips the same predicate to YES.

WHAT IT TESTS.  Lesson 87's explicitly-unchecked prediction, quoted from this repository
(writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md lines 188-192):

    "It also predicts the literature's shape: the certified self-similar blow-ups that used
     this machinery (Dahne-Figueras, CGL) are DISSIPATIVE, and the certified inviscid ones
     (Chen-Hou) use weighted energy estimates instead.  That prediction is checkable and it
     has not been checked here."

If the prediction were WRONG -- if some published certified inviscid self-similar blow-up
ran an ell^1-multiplier tail estimate -- then the realization legs 52-54 measured dead
(bordered radii-polynomial certificate on the a=0 CLM linearisation; Z_1 block coupling
43.15 where <1 was needed; best achievable 1.167x where >8x was needed) would have a
PUBLISHED REPAIR this project missed.  That is why the gate's yes-branch escalates.

SCOPE GUARD, pre-committed in DIRECTION.md section 113 and honoured here.  Cadiot
arXiv:2505.03091 appears in this ledger with METHOD SHAPE and POPULATION MEMBERSHIP only.
Whether its construction covers NG's zero-diagonal / off-diagonal hypothesis is LEG 62's
question (branch leg/cp-v1) and is neither answered nor narrowed here.

REPRODUCTION.

    bash Papers/fetch.sh                       # Papers/ is gitignored
    curl -sSL -o Papers/<id>.pdf https://arxiv.org/pdf/<id>
    .venv/bin/python experiments/p2_route_ms_v1_lit.py
        -> writeup/data/p2_route_ms_v1_lit.json

The script runs WITHOUT the PDFs -- the ledger is the curated artifact.  But if
Papers/<id>.txt is present (pypdf text extraction) it RE-RUNS every recorded string search
and compares against the recorded count, reporting VERIFIED / MISMATCH / TEXT_ABSENT per
probe.  A recorded negative that cannot be re-executed decays at the rate of memory
(lesson 68); a recorded negative that CAN come out differently on re-run is the only kind
worth quoting (lesson 90).

QUOTE PROVENANCE.  Every verbatim quote below was read out of a pypdf text extraction of
the published PDF and is whitespace- and ligature-normalized: pypdf inserts spurious spaces
inside words ("coe fficients", "st ability") and renders ligatures inconsistently.  NO WORD
IS ADDED, REMOVED OR REORDERED.  Displayed mathematics is NOT quoted anywhere in this file,
because that is exactly where pdf extraction reorders symbols -- leg 57 hit this and had to
label a reconstruction as a reconstruction.  Here the rule is simpler: prose only.

NO FIGURE: one table of booleans over eleven papers has nothing to plot.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

OUT = ROOT / "writeup" / "data" / "p2_route_ms_v1_lit.json"
PAPERS = ROOT / "Papers"

GATE = ("Does any published certified INVISCID self-similar blow-up use a diagonal-tail "
        "(ell-1-multiplier / radii-polynomial) framework for its linearized tail estimate?")

# ---------------------------------------------------------------------------
# 1. the query log -- verbatim strings, links not counts
# ---------------------------------------------------------------------------

SEARCH_LOG = [
    {"engine": "web", "query": "computer-assisted proof self-similar blowup inviscid radii "
                               "polynomial Fourier ell^1",
     "kept": ["2308.01528", "2605.19716", "2605.15149", "2406.16597", "2401.14615",
              "2106.05422"]},
    {"engine": "web", "query": "radii polynomial approach computer-assisted proof blowup Euler "
                               "Boussinesq Constantin-Lax-Majda De Gregorio self-similar profile",
     "kept": ["2305.05660", "2106.05422", "2401.14615", "2308.01528"]},
    {"engine": "web", "query": "\"computer-assisted\" proof \"self-similar\" blowup "
                               "\"compressible Euler\" implosion interval arithmetic "
                               "Gomez-Serrano",
     "kept": ["2208.09445", "2310.05325", "2606.12758", "2509.14185"]},
    {"engine": "web", "query": "Lessard van den Berg radii polynomial computer-assisted proof "
                               "blow-up self-similar \"ell^1\" Fourier tail operator diagonal "
                               "fluid transport",
     "kept": ["2605.19716"]},
    {"engine": "web", "query": "\"Newton-Kantorovich\" OR \"radii polynomial\" computer-assisted "
                               "proof \"self-similar\" blowup Euler incompressible transport "
                               "advection 2025 2026",
     "kept": ["2605.19716", "2604.09949"]},
    {"engine": "web", "query": "Takayasu Lessard Jaquette Okamoto \"rigorous numerics\" nonlinear "
                               "heat equation blow-up radii polynomial Fourier arxiv",
     "kept": ["1910.12472"]},
    {"engine": "web", "query": "\"unstable singularities\" 2509.14185 computer-assisted proof "
                               "certified follow-up rigorous 2026 Euler Boussinesq IPM",
     "kept": ["2509.14185"]},
    {"engine": "arxiv-api", "query": "https://export.arxiv.org/api/query?id_list=1905.06387,"
                                     "2106.05422,2210.07191,2305.05660,2208.09445,2310.05325,"
                                     "1910.12472,2410.05480,2505.03091,2406.16597",
     "kept": ["journal_ref and doi fields for every row that has one"]},
    {"engine": "repo", "query": "grep -rn \"inviscid\" --include=*.md writeup/ LITERATURE_CHECK.md "
                                "| grep -i \"certif|radii|CAP|diagonal\"",
     "kept": ["TECHNICAL_P2_ROUTEL1_V2.md:190 (the claim under test)",
              "TECHNICAL_P2_ROUTET_V1.md:52", "LITERATURE_CHECK.md:18-19,34"]},
]

# ---------------------------------------------------------------------------
# 2. the pre-committed population rule and predicate
#    (fixed in writeup/novelty/leg_113.md, committed BEFORE any row was scored)
# ---------------------------------------------------------------------------

POPULATION_RULE = {
    "clause_1_blowup": "claims a PROOF (not a numerical discovery) of finite-time blow-up "
                       "that is self-similar, asymptotically self-similar, or nearly "
                       "self-similar",
    "clause_2_inviscid": "the certified equation carries NO dissipative term -- no -nu*Laplacian, "
                         "no fractional Lambda^alpha damping",
    "clause_3_certified": "the proof is computer-assisted: some step is discharged by rigorous "
                          "numerics (interval arithmetic or equivalent), not pen and paper alone",
    "peer_review": "RECORDED PER ROW, NOT USED AS A FILTER -- a publication-status filter is "
                   "exactly the knob that could exclude a falsifier, so the gate is answered "
                   "both over all rows and over the journal_ref-confirmed subset",
}

# tail_treatment vocabulary -- closed set, asserted by check_vocabulary()
ELL1_MULTIPLIER_TAIL = "ELL1_MULTIPLIER_TAIL"          # the shape lesson 87 predicts absent
WEIGHTED_ENERGY_NO_TAIL_OP = "WEIGHTED_ENERGY_NO_TAIL_OP"
RIGOROUS_ODE_NO_TAIL_OP = "RIGOROUS_ODE_NO_TAIL_OP"
NO_TAIL_ESTIMATE_ANALYTIC = "NO_TAIL_ESTIMATE_ANALYTIC"
NOT_A_BLOWUP_PAPER = "NOT_A_BLOWUP_PAPER"
TAIL_VOCAB = {ELL1_MULTIPLIER_TAIL, WEIGHTED_ENERGY_NO_TAIL_OP, RIGOROUS_ODE_NO_TAIL_OP,
              NO_TAIL_ESTIMATE_ANALYTIC, NOT_A_BLOWUP_PAPER}

# ---------------------------------------------------------------------------
# 3. the ledger
# ---------------------------------------------------------------------------
#
# Field contract, enforced by unlocated_rows():
#   locator   -- section / subsection / assumption number inside the source
#   quote     -- verbatim prose from that locator (normalized, see module docstring)
#   probes    -- {probe name: recorded count over the full text}; re-executed when the
#                extraction is present on disk
#
# A row with tail_treatment set and no locator+quote is a classification with nothing behind
# it, and is a failure of this script rather than a finding.

LEDGER = [
    # ---------------- IN POPULATION: certified, inviscid, self-similar blow-up -----------
    {
        "key": "CHH-DG",
        "cite": "Chen, Hou, Huang -- On the Finite Time Blowup of the De Gregorio Model for "
                "the 3D Euler Equations",
        "url": "https://arxiv.org/abs/1905.06387",
        "journal_ref": "Comm. Pure Appl. Math., 74: 1282-1350, (2021)",
        "doi": "10.1002/cpa.21991",
        "journal_ref_source": "arXiv API metadata, fetched 2026-08-06",
        "equation": "De Gregorio / gCLM on the real line and the circle -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": WEIGHTED_ENERGY_NO_TAIL_OP,
        "locator": "section 2.3, 'Energy estimates with computer assistance'",
        "quote": "The key part of the stability analysis is to use energy estimates to establish "
                 "the linear stability. In the energy estimates, instead of bounding several "
                 "coefficients by some absolute constants, which leads to overestimates, we keep "
                 "track of these coefficients. Since these coefficients depend on the approximate "
                 "self-similar profile constructed numerically, we use numerical computation with "
                 "rigorous error control to verify several inequalities that involve these "
                 "coefficients.",
        "second_locator": "section 2.3, the paragraph immediately following -- THE HEADLINE OF "
                          "THIS LEG: the obstruction lesson 87 names, stated in print by the "
                          "authors of a peer-reviewed certified inviscid blow-up",
        "second_quote": "There is another computer-assisted approach to establish the stability "
                        "by tracking the spectrum of a given operator and quantifying the spectral "
                        "gap; see, e.g. [2]. The key difference between this approach and our "
                        "approach is that we do not use computation to quantify the spectral gap "
                        "of the linearized operator L in (2.2). In fact, the linearized operator L "
                        "is not a compact operator due to the Hilbert transform u_x = H omega and "
                        "the non-compact part of L cannot be treated as a small perturbation. Thus "
                        "we cannot approximate the linearized operator by a finite rank operator "
                        "which can be estimated using numerical computation.",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 0,
                   "interval arithmetic": 20, "computer-assisted": 9},
        "note": "The authors' stated reason for the obstruction is the NON-COMPACTNESS of the "
                "Hilbert transform, not the shift structure of a far-field block. Those are "
                "related but not identical mechanisms and this ledger does NOT assert the "
                "identification; what it records is that the finite-block-plus-tail "
                "decomposition is explicitly declared unavailable, in print, for an inviscid "
                "nonlocal transport model.",
    },
    {
        "key": "CHH-HL",
        "cite": "Chen, Hou, Huang -- Asymptotically self-similar blowup of the Hou-Luo model "
                "for the 3D Euler equations",
        "url": "https://arxiv.org/abs/2106.05422",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv API metadata reports NONE as of 2026-08-06; peer-review "
                              "status NOT established in this pass",
        "equation": "Hou-Luo model (1D model of the 3D axisymmetric Euler equations with "
                    "boundary) -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": WEIGHTED_ENERGY_NO_TAIL_OP,
        "locator": "section 3.13, 'From linear stability to nonlinear stability with rigorous "
                   "verification'",
        "quote": "As we discuss at the beginning of Section 2, the most challenging and essential "
                 "part in the proof is the weighted L2 linear stability analysis established in "
                 "Section 3",
        "second_locator": "section 1, the overview of the computer-assisted part",
        "second_quote": "Yet we need to verify various inequalities involving the approximate "
                        "steady state using the interval arithmetic and numerical analysis with "
                        "computer assistance. The most essential part of the linear stability "
                        "analysis can be established based on the grid point values of the "
                        "approximate steady state",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 1,
                   "interval arithmetic": 16, "computer-assisted": 22},
        "note": "The single 'Fourier' occurrence is bibliographic, not a spectral tail estimate.",
    },
    {
        "key": "CH-I",
        "cite": "Chen, Hou -- Stable nearly self-similar blowup of the 2D Boussinesq and 3D "
                "Euler equations with smooth data I: Analysis",
        "url": "https://arxiv.org/abs/2210.07191",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv API metadata reports NONE as of 2026-08-06. A peer-reviewed "
                              "venue for the Chen-Hou 3D Euler result was located by web search "
                              "(PNAS, doi 10.1073/pnas.2500940122, 'Singularity formation in 3D "
                              "Euler equations with smooth initial data and boundary'); the PNAS "
                              "full text was NOT read in this pass (HTTP 403) and this row does "
                              "NOT claim its content.",
        "equation": "2D Boussinesq and 3D axisymmetric Euler with boundary -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": WEIGHTED_ENERGY_NO_TAIL_OP,
        "locator": "abstract, and section 2.7 (the located statement leg 57 also used)",
        "quote": "we establish an analytic framework to prove nonlinear stability of an "
                 "approximate self-similar blowup profile using a combination of weighted "
                 "L-infinity and weighted C-1/2 energy estimates",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 0,
                   "interval arithmetic": 5, "computer-assisted": 14},
        "note": "The quote as recorded here is from Part II's abstract describing Part I's "
                "framework (Part II is the row below); the negative probe counts are measured "
                "over Part I's own 145-page full text, 455588 normalized characters, and "
                "independently reproduce leg 57's negative located observation.",
    },
    {
        "key": "CH-II",
        "cite": "Chen, Hou -- Stable nearly self-similar blowup of the 2D Boussinesq and 3D "
                "Euler equations with smooth data II: Rigorous Numerics",
        "url": "https://arxiv.org/abs/2305.05660",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv API metadata reports NONE as of 2026-08-06",
        "equation": "2D Boussinesq and 3D axisymmetric Euler with boundary -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": WEIGHTED_ENERGY_NO_TAIL_OP,
        "locator": "abstract",
        "quote": "In Part I of our paper, we establish an analytic framework to prove nonlinear "
                 "stability of an approximate self-similar blowup profile using a combination of "
                 "weighted L-infinity and weighted C-1/2 energy estimates. We reduce proving "
                 "nonlinear stability to verifying several inequalities for the constants in the "
                 "energy estimate which depend on the approximate steady state and the weights in "
                 "the energy functional only. In Part II of our paper, we construct approximate "
                 "space-time solutions with rigorous error control",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 0,
                   "interval arithmetic": 1, "computer-assisted": 10},
        "note": "This is the volume whose TITLE is 'Rigorous Numerics'. It is the strongest "
                "single place in the corpus for a diagonal tail to appear if one were used, and "
                "over 146 pages / 431417 normalized characters the count is zero on all five "
                "diagnostic strings.",
    },
    {
        "key": "BCG-IMP",
        "cite": "Buckmaster, Cao-Labora, Gomez-Serrano -- Smooth imploding solutions for 3D "
                "compressible fluids",
        "url": "https://arxiv.org/abs/2208.09445",
        "journal_ref": "Forum of Mathematics, Pi 13 (2025) e6",
        "doi": "10.1017/fmp.2024.12",
        "journal_ref_source": "arXiv API metadata, fetched 2026-08-06",
        "equation": "3D isentropic compressible Euler (and Navier-Stokes) -- the self-similar "
                    "imploding PROFILE is constructed for the inviscid compressible Euler system",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": RIGOROUS_ODE_NO_TAIL_OP,
        "locator": "section 1.4, 'we will use the computer in two different parts of our strategy'",
        "quote": "In our concrete case, we will use the computer in two different parts of our "
                 "strategy: 1. Computing (with rigorous bounds) a high amount of Taylor "
                 "coefficients of a solution of an ODE at a",
        "second_locator": "section 1.3",
        "second_quote": "Furthermore, we employ a computer-assisted proof to compute the first "
                        "10000 coefficient pairs at r = r*, with rigorous error bounds. In order "
                        "to perform rigorous, error-free calculations, interval arithmetic will be "
                        "used as part of the proof whenever needed.",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 1,
                   "interval arithmetic": 2, "computer-assisted": 35},
        "note": "The infinite-dimensionality is discharged BEFORE any operator inversion: the "
                "self-similar profile is an ODE solution and the computer certifies its Taylor "
                "coefficients. There is no unbounded linear operator whose tail needs an "
                "approximate inverse, so the diagonal-vs-shift question does not arise -- the "
                "same structural position Dahne-Figueras occupies in leg 57's ledger, reached "
                "here on an INVISCID equation and in a peer-reviewed venue.",
    },
    {
        "key": "CGSS-NR",
        "cite": "Cao-Labora, Gomez-Serrano, Shi, Staffilani -- Non-radial implosion for "
                "compressible Euler and Navier-Stokes in T^3 and R^3",
        "url": "https://arxiv.org/abs/2310.05325",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv API metadata reports NONE as of 2026-08-06",
        "equation": "compressible Euler and Navier-Stokes -- the Euler statement is inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": False,
        "tail_treatment": WEIGHTED_ENERGY_NO_TAIL_OP,
        "locator": "section 1 (the profile's provenance) and section 3.4 ('Energy estimate for "
                   "higher order bounds')",
        "quote": "We know the existence of profiles for gamma = 7/5 due to [8]. If we drop "
                 "condition (1.8) (which is only needed for the stability of Navier-Stokes, not "
                 "the Euler one), [8] gives the existence of profiles solving (1.9) in the regime "
                 "(1.6) for all gamma > 1",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 4,
                   "interval arithmetic": 0, "computer-assisted": 0},
        "note": "own_cap_step is FALSE and it is measured, not assumed: 0 occurrences of "
                "'interval arithmetic' and 0 of 'computer-assist*' over 80 pages. This paper "
                "INHERITS its certified profile from [8] = arXiv:2208.09445 and contributes the "
                "non-radial stability, which it does by Sobolev energy estimates plus a "
                "topological argument for the unstable modes. It is therefore the row most "
                "sensitive to a judgement call, and gate_answers() reports the gate with this "
                "row both in and out.",
    },
    {
        "key": "CHEN-C13",
        "cite": "Chen -- Asymptotically Self-Similar Blowup for 3D Incompressible Euler with "
                "C^{1,1/3-} Velocity I: C-infinity 1D Limiting Profiles",
        "url": "https://arxiv.org/abs/2605.15149",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv preprint submitted 2026-05-14; no journal_ref; peer-review "
                              "status NOT established in this pass",
        "equation": "one-parameter family of 1D models for the 3D axisymmetric incompressible "
                    "Euler equation -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": RIGOROUS_ODE_NO_TAIL_OP,
        "locator": "section 1, 'Computer-assisted proofs in PDEs' and the reading guide",
        "quote": "The computer-assisted estimates are confined to Section 3, Section 4.3-4.4, and "
                 "Appendices B-C, while Sections 4.1, 4.2, Sections 5-7, and Appendix A are purely "
                 "analytic. For rigorous proof, we control all truncation and round-off errors "
                 "using numerical analysis and Interval Arithmetic.",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 0,
                   "interval arithmetic": 19, "computer-assisted": 18},
        "note": "The newest in-population row (May 2026) and the one that keeps the survey "
                "current: a fresh inviscid CAP, 92 pages, and still zero on all five diagnostic "
                "strings. The computer bounds integrals for a fixed-point argument; there is no "
                "sequence-space tail operator.",
    },
    {
        "key": "DS-NLS",
        "cite": "Donninger, Schorkhuber -- Self-similar blowup for the cubic Schrodinger equation",
        "url": "https://arxiv.org/abs/2406.16597",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv API metadata reports NONE as of 2026-08-06 (v3, Dec 2025)",
        "equation": "focusing cubic NLS in 3D -- DISPERSIVE, and carries NO dissipative term, so "
                    "it satisfies clause 2 as written",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": RIGOROUS_ODE_NO_TAIL_OP,
        "locator": "abstract",
        "quote": "We give a rigorous proof for the existence of a finite-energy, self-similar "
                 "solution to the focusing cubic Schrodinger equation in three spatial dimensions. "
                 "The proof is computer-assisted and relies on a fixed point argument that shows "
                 "the existence of a solution in the vicinity of a numerically constructed "
                 "approximation. The latter is obtained by a standard pseudo-spectral method. The "
                 "computer-assisted part of the rigorous proof uses nothing but fraction "
                 "arithmetic in order to obtain quantitative bounds for the fixed point argument.",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 2, "Fourier": 1,
                   "interval arithmetic": 3, "computer-assisted": 19},
        "note": "ADMITTED BY THE LETTER OF THE PRE-COMMITTED RULE, and flagged. Clause 2 was "
                "written as 'no dissipative term'; cubic NLS has none, so it is in, even though "
                "it is not a fluid transport equation. It is the row that could most easily have "
                "falsified the prediction -- its unbounded part -i*Laplacian IS a multiplier, so "
                "an ell^1 diagonal tail was available to these authors and they did not use one "
                "(1 occurrence of 'Fourier' in 83 pages; the profile equation is an ODE). "
                "gate_answers() reports the gate with this row both in and out.",
    },

    # ---------------- OUT OF POPULATION, RECORDED WITH THE CLAUSE THEY FAIL -------------
    {
        "key": "TLJO-HEAT",
        "cite": "Takayasu, Lessard, Jaquette, Okamoto -- Rigorous numerics for nonlinear heat "
                "equations in the complex plane of time",
        "url": "https://arxiv.org/abs/1910.12472",
        "journal_ref": "Numer. Math. 151, 693-750 (2022)",
        "doi": "10.1007/s00211-022-01291-2",
        "journal_ref_source": "publisher landing page located by web search 2026-08-06; the "
                              "arXiv API reports no journal_ref for this id",
        "equation": "u_t = u_xx + u^2 on (0,1), periodic -- DISSIPATIVE",
        "clause_1_blowup": True, "clause_2_inviscid": False, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": ELL1_MULTIPLIER_TAIL,
        "locator": "section 2 (the space) and section 3 (the linearized problem defining the "
                   "solution map operator A)",
        "quote": "X = C(J; ell^1) ... An important and useful feature of ell^1 is that it is a "
                 "Banach algebra under discrete convolution. Our task of rigorous numerics is to "
                 "determine the Fourier coefficients of the solution of the Cauchy problem.",
        "second_locator": "section 3, the homogeneous IVP (3.1) that defines the evolution "
                          "operator",
        "second_quote": "The simplified Newton operator (2.9) is characterized by the solution map "
                        "operator A. We define A using an evolution operator U(t,s) of the "
                        "following homogeneous initial value problem",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 1, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 7, "Fourier": 14,
                   "interval arithmetic": 11, "computer-assisted": 4},
        "note": "POSITIVE CONTROL 1, and it fails clause 2 ONLY. The linearized sequence problem "
                "(3.1) is d/dt b_k + e^{i theta}[k^2 omega^2 b_k - 2(abar * b)_k] = 0: the "
                "unbounded part is the EXACT DIAGONAL MULTIPLIER k^2 omega^2 and the rest is a "
                "convolution. This is a diagonal-tail framework, in ell^1 Fourier, applied to a "
                "BLOW-UP problem (its own keyword list opens with 'blow-up solutions for "
                "nonlinear heat equations') -- on a dissipative equation. Delete clause 2 and "
                "this row alone flips the gate to YES.",
    },
    {
        "key": "CLN",
        "cite": "Cadiot, Lessard, Nakao -- (unbounded-domain computer-assisted framework)",
        "url": "https://arxiv.org/abs/2302.12877",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv API not queried for this id in this pass; the row is a "
                              "method-shape control, not a population member",
        "equation": "semilinear PDEs on R^m -- no blow-up claimed",
        "clause_1_blowup": False, "clause_2_inviscid": False, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": ELL1_MULTIPLIER_TAIL,
        "locator": "section 1, literature review, the periodic case",
        "quote": "One of the main ingredients to achieve such a goal is to exploit the fact that "
                 "the Frechet derivatives are (asymptotically) diagonally dominant. Indeed, in "
                 "autonomous semi-linear PDEs, the linear part DF(0) dominates for high-order "
                 "modes. Therefore, the tail of DF(U0) can be seen as a diagonally-dominant "
                 "infinite dimensional matrix. From this, one can approximate the inverse of "
                 "DF(U0) as a finite matrix acting on a finite part of the sequence, and a tail "
                 "operator (which is diagonal) which acts on the tail of the sequence.",
        "probes": {"radii polynomial": 2, "Newton-Kantorovich": 5, "approximate inverse": 27,
                   "diagonally dominant": 7, "contraction mapping": 1, "Fourier": 67,
                   "interval arithmetic": 5, "computer-assisted": 30},
        "note": "POSITIVE CONTROL 2, and it fails clause 1 ONLY -- a DIFFERENT clause from "
                "TLJO-HEAT. This is the canonical statement of the diagonal-tail framework and "
                "of WHY it is available (relative compactness of DF(U0)-DF(0) with respect to "
                "DF(0)). Quote independently re-extracted here, not copied from leg 57's "
                "solver/certificate_shapes.py, which this leg does not edit or import.",
    },
    {
        "key": "CADIOT-STAB",
        "cite": "Cadiot -- Stability analysis for localized solutions in PDEs and nonlocal "
                "equations on R^m",
        "url": "https://arxiv.org/abs/2505.03091",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "arXiv API metadata reports NONE as of 2026-08-06",
        "equation": "planar Swift-Hohenberg, planar Gray-Scott, capillary-gravity Whitham",
        "clause_1_blowup": False, "clause_2_inviscid": False, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": NOT_A_BLOWUP_PAPER,
        "locator": "abstract",
        "quote": "In this paper, we present a general methodology for investigating the linear "
                 "stability of localized solutions in PDEs and nonlocal equations on R^m. More "
                 "specifically, we control the spectrum of the Jacobian DF(u-tilde) at a localized "
                 "solution u-tilde, enclosing both the eigenvalues and the essential spectrum. Our "
                 "approach is computer-assisted and is based on a controlled approximation of "
                 "DF(u-tilde) by its Fourier coefficients counterpart on a bounded domain. We "
                 "first control the spectrum of the Fourier coefficients operator combining a "
                 "pseudo-diagonalization and a generalized Gershgorin disk theorem.",
        "probes": {},
        "note": "SCOPE GUARD ROW. Recorded for METHOD SHAPE (pseudo-diagonalization plus a "
                "generalized Gershgorin disk theorem on the Fourier-coefficient operator) and "
                "for POPULATION MEMBERSHIP ONLY: it fails clause 1 because it is a paper about "
                "the linear stability of LOCALIZED SOLUTIONS -- solitary waves -- and makes no "
                "blow-up claim at all. Whether its construction covers NG's zero-diagonal / "
                "off-diagonal hypothesis is LEG 62's question and is neither answered nor "
                "narrowed here. Read at abstract level only in this pass, which is sufficient "
                "for a subject-matter exclusion and is NOT sufficient for anything else.",
    },
    {
        "key": "HQWW-HL",
        "cite": "Huang, Qin, Wang, Wei -- Exact self-similar finite-time blowup of the Hou-Luo "
                "model with smooth profiles",
        "url": "https://arxiv.org/abs/2308.01528",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "not queried; excluded on clause 3",
        "equation": "1D Hou-Luo model on the real line -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": False,
        "own_cap_step": False,
        "tail_treatment": NO_TAIL_ESTIMATE_ANALYTIC,
        "locator": "abstract",
        "quote": "The existence of these profiles is established via a fixed-point method that is "
                 "purely analytic.",
        "probes": {},
        "note": "Fails clause 3 by its own abstract's words. Recorded because it is the exact "
                "object class of this project's dead realization and would have been the most "
                "natural home for a diagonal-tail treatment.",
    },
    {
        "key": "HQW-CLM",
        "cite": "Huang, Qin, Wang -- Multi-scale self-similar finite-time blowups of the "
                "Constantin-Lax-Majda model for the 3D Euler equations",
        "url": "https://arxiv.org/abs/2401.14615",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "not queried; excluded on clause 3",
        "equation": "Constantin-Lax-Majda model -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": False,
        "own_cap_step": False,
        "tail_treatment": NO_TAIL_ESTIMATE_ANALYTIC,
        "locator": "section 1, introduction",
        "quote": "Our construction is based on an asymptotic analysis applied to the explicit "
                 "solution formula of the model, and a complex analysis is performed to provide an "
                 "understanding of multi-scale blowups from a pole dynamics perspective.",
        "probes": {"radii polynomial": 0, "Newton-Kantorovich": 0, "approximate inverse": 0,
                   "diagonally dominant": 0, "contraction mapping": 0, "Fourier": 0,
                   "interval arithmetic": 0, "computer-assisted": 1},
        "note": "Fails clause 3, measured: 0 occurrences of 'interval arithmetic' over the full "
                "26-page text and the single 'computer-assist*' hit is a citation of other work. "
                "This is the model whose a=0 linearisation IS this project's dead object, and the "
                "published route to blow-up on it is the explicit CLM solution formula -- no "
                "linearized tail estimate of any kind.",
    },
    {
        "key": "SWZZ-EULER",
        "cite": "Shao, Wei, Zhang, Zhang -- Self-similar blow-up solutions of d-dimensional "
                "incompressible Euler equations with C^{1,(1-2/d)-} velocity",
        "url": "https://arxiv.org/abs/2605.19716",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "not queried; excluded on clause 3",
        "equation": "axisymmetric incompressible Euler in R^d, d >= 3 -- inviscid",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": False,
        "own_cap_step": False,
        "tail_treatment": NO_TAIL_ESTIMATE_ANALYTIC,
        "locator": "abstract",
        "quote": "a fixed-point argument formulated for the self-similar profile equations, which "
                 "form a coupled elliptic-transport system",
        "probes": {},
        "note": "Read at abstract level only; excluded on clause 3 (no computer-assisted step "
                "indicated). Recorded so that its absence from the population is a decision with "
                "a reason attached rather than an omission.",
    },
    {
        "key": "UNSTABLE-DISC",
        "cite": "Wang et al. -- Discovery of Unstable Singularities",
        "url": "https://arxiv.org/abs/2509.14185",
        "journal_ref": None,
        "doi": None,
        "journal_ref_source": "not queried; excluded on clause 1",
        "equation": "IPM, 2D Boussinesq, 3D Euler with boundary, CCF -- inviscid",
        "clause_1_blowup": False, "clause_2_inviscid": True, "clause_3_certified": False,
        "own_cap_step": False,
        "tail_treatment": NO_TAIL_ESTIMATE_ANALYTIC,
        "locator": "abstract / LITERATURE_CHECK.md sixth pass, which already classified it",
        "quote": "unstable singularities at CAP-ready precision, inviscid, no certificate claimed "
                 "[this repository's own sixth-pass classification, LITERATURE_CHECK.md line 19]",
        "probes": {},
        "note": "Fails clause 1: numerical DISCOVERY at near-machine precision, no proof claimed. "
                "Re-checked 2026-08-06 for a certified follow-up and none was located. This is "
                "the row most likely to move: if a CAP lands on one of these profiles, the "
                "population gains a member and this gate is worth re-running.",
    },

    # ---------------- LESSON 90: the row that makes the predicate able to say YES --------
    {
        "key": "SYNTHETIC_CONTROL",
        "cite": "FICTITIOUS -- not a paper. Exists so that a 'no' is a property of the "
                "literature and not of this script.",
        "url": None,
        "journal_ref": "FICTITIOUS",
        "doi": None,
        "journal_ref_source": "FICTITIOUS",
        "equation": "an inviscid transport model, certified, whose linearized tail is inverted "
                    "by dividing through by a diagonal symbol",
        "clause_1_blowup": True, "clause_2_inviscid": True, "clause_3_certified": True,
        "own_cap_step": True,
        "tail_treatment": ELL1_MULTIPLIER_TAIL,
        "locator": "n/a -- fictitious",
        "quote": "n/a -- fictitious",
        "probes": {},
        "note": "Admitting this row flips falsifies_lesson_87 to YES (asserted by "
                "check_synthetic_control()). It is excluded from every reported count.",
    },
]

# ---------------------------------------------------------------------------
# 4. the predicate, and the guards
# ---------------------------------------------------------------------------


def in_population(row):
    return (row["clause_1_blowup"] and row["clause_2_inviscid"] and row["clause_3_certified"])


def uses_diagonal_tail(row):
    return row["tail_treatment"] == ELL1_MULTIPLIER_TAIL


def falsifies_lesson_87(row):
    return in_population(row) and uses_diagonal_tail(row)


def real_rows():
    return [r for r in LEDGER if r["key"] != "SYNTHETIC_CONTROL"]


def unlocated_rows():
    """A classification with no locator+quote behind it is a bug in this file."""
    bad = []
    for r in real_rows():
        if not r.get("locator") or not r.get("quote"):
            bad.append(r["key"])
    return bad


def check_vocabulary():
    bad = [r["key"] for r in LEDGER if r["tail_treatment"] not in TAIL_VOCAB]
    assert not bad, f"tail_treatment outside the closed vocabulary: {bad}"


def check_resolvable_links():
    bad = [r["key"] for r in real_rows()
           if not (r.get("url") or "").startswith("https://arxiv.org/abs/")]
    assert not bad, f"rows without a resolvable arXiv link: {bad}"


def check_synthetic_control():
    """Lesson 90: the predicate must be able to come out the other way."""
    syn = [r for r in LEDGER if r["key"] == "SYNTHETIC_CONTROL"][0]
    assert falsifies_lesson_87(syn), "the synthetic control does not flip the predicate"
    assert not any(falsifies_lesson_87(r) for r in real_rows()), \
        "a REAL row falsifies lesson 87 -- ESCALATE, do not merge silently"


def check_clauses_each_do_work():
    """Each clause must be load-bearing: dropping it must admit a real diagonal-tail row,
    and the two near misses must fail DIFFERENT clauses."""
    diag = [r for r in real_rows() if uses_diagonal_tail(r)]
    assert diag, "no real diagonal-tail row at all -- the ledger has no positive side"
    failed_clauses = {}
    for r in diag:
        fails = tuple(c for c in ("clause_1_blowup", "clause_2_inviscid", "clause_3_certified")
                      if not r[c])
        failed_clauses[r["key"]] = fails
        assert fails, f"{r['key']} uses a diagonal tail and is in population -- ESCALATE"
    distinct = {v for v in failed_clauses.values()}
    assert len(distinct) >= 2, \
        f"all diagonal-tail near-misses fail the same clause(s): {failed_clauses}"
    return failed_clauses


# ---------------------------------------------------------------------------
# 5. re-execute the recorded string searches when the extractions are on disk
# ---------------------------------------------------------------------------

PROBE_PATTERNS = {
    "radii polynomial": r"radii\s*-?\s*polynomial",
    "Newton-Kantorovich": r"Newton\s*[-–]\s*Kantorovich",
    "approximate inverse": r"approximate\s+inverse",
    "diagonally dominant": r"diagonal(?:ly)?\s*-?\s*dominan",
    "contraction mapping": r"contraction\s+mapping",
    "Fourier": r"Fourier",
    "interval arithmetic": r"interval\s+arithmetic",
    "computer-assisted": r"computer\s*-?\s*assist",
}


def arxiv_id(row):
    return (row.get("url") or "").rsplit("/", 1)[-1] or None


def reverify_probes():
    """Re-run every recorded count against Papers/<id>.txt when present.

    Returns {key: {"status": VERIFIED|MISMATCH|TEXT_ABSENT|NO_PROBES, ...}}.
    THIS is what makes the negative result executable rather than remembered: with the
    extractions in place a drift in any recorded count fails loudly here.
    """
    out = {}
    for r in real_rows():
        if not r.get("probes"):
            out[r["key"]] = {"status": "NO_PROBES"}
            continue
        aid = arxiv_id(r)
        txt = PAPERS / f"{aid}.txt"
        if not txt.exists():
            out[r["key"]] = {"status": "TEXT_ABSENT", "expected_at": f"Papers/{aid}.txt"}
            continue
        body = re.sub(r"\s+", " ", txt.read_text())
        got, mism = {}, []
        for name, count in r["probes"].items():
            n = len(re.findall(PROBE_PATTERNS[name], body, re.I))
            got[name] = n
            if n != count:
                mism.append({"probe": name, "recorded": count, "measured": n})
        out[r["key"]] = {"status": "MISMATCH" if mism else "VERIFIED",
                         "chars": len(body), "measured": got, "mismatches": mism}
    return out


# ---------------------------------------------------------------------------
# 6. the gate, answered several ways so the reader can see what it depends on
# ---------------------------------------------------------------------------


def gate_answers():
    rows = real_rows()
    pop = [r for r in rows if in_population(r)]

    def n_falsify(subset):
        return sum(1 for r in subset if uses_diagonal_tail(r))

    peer = [r for r in pop if r.get("journal_ref")]
    fluid = [r for r in pop if r["key"] != "DS-NLS"]
    own_cap = [r for r in pop if r["own_cap_step"]]
    strict = [r for r in pop if r["own_cap_step"] and r["key"] != "DS-NLS"]

    return {
        "as_stated": {"population": len(pop), "falsifying": n_falsify(pop),
                      "answer": "NO" if n_falsify(pop) == 0 else "YES",
                      "keys": [r["key"] for r in pop]},
        "peer_review_confirmed_only": {
            "population": len(peer), "falsifying": n_falsify(peer),
            "answer": "NO" if n_falsify(peer) == 0 else "YES",
            "keys": [r["key"] for r in peer],
            "meaning": "rows carrying a journal_ref located in this pass"},
        "fluid_transport_only": {
            "population": len(fluid), "falsifying": n_falsify(fluid),
            "answer": "NO" if n_falsify(fluid) == 0 else "YES",
            "keys": [r["key"] for r in fluid],
            "meaning": "drops DS-NLS, admitted by the letter of clause 2 but dispersive"},
        "own_cap_step_only": {
            "population": len(own_cap), "falsifying": n_falsify(own_cap),
            "answer": "NO" if n_falsify(own_cap) == 0 else "YES",
            "keys": [r["key"] for r in own_cap],
            "meaning": "drops CGSS-NR, which inherits its certified profile from BCG-IMP"},
        "strictest": {
            "population": len(strict), "falsifying": n_falsify(strict),
            "answer": "NO" if n_falsify(strict) == 0 else "YES",
            "keys": [r["key"] for r in strict],
            "meaning": "every judgement call resolved the OTHER way at once"},
    }


def clause_ablation():
    """Drop one clause of the population rule at a time and recount.

    Lesson 90's question -- 'what would have had to change for this to report the other
    answer?' -- answered as a number rather than as a reassurance. Each ablation names the
    real rows that would then falsify lesson 87.
    """
    clauses = ("clause_1_blowup", "clause_2_inviscid", "clause_3_certified")
    out = {}
    for drop in clauses:
        kept = [c for c in clauses if c != drop]
        adm = [r for r in real_rows() if all(r[c] for c in kept)]
        fal = [r["key"] for r in adm if uses_diagonal_tail(r)]
        out[f"drop_{drop}"] = {"population": len(adm), "falsifying": len(fal),
                               "answer": "YES" if fal else "NO", "keys": fal}
    adm = real_rows()
    fal = [r["key"] for r in adm if uses_diagonal_tail(r)]
    out["drop_all_three"] = {"population": len(adm), "falsifying": len(fal),
                             "answer": "YES" if fal else "NO", "keys": fal}
    return out


def tail_treatment_census():
    census = {}
    for r in real_rows():
        census.setdefault(r["tail_treatment"], []).append(r["key"])
    return census


# ---------------------------------------------------------------------------
# 7. run
# ---------------------------------------------------------------------------


def main():
    check_vocabulary()
    check_resolvable_links()
    bad = unlocated_rows()
    assert not bad, f"rows classified without a locator+quote: {bad}"
    check_synthetic_control()
    failed_clauses = check_clauses_each_do_work()

    answers = gate_answers()
    verify = reverify_probes()

    payload = {
        "leg": 113,
        "route": "MS",
        "branch": "leg/ms-v1",
        "date": "2026-08-06",
        "gate": GATE,
        "gate_answer": answers["as_stated"]["answer"],
        "claim_under_test": {
            "source": "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md lines 188-192",
            "text": "the certified self-similar blow-ups that used this machinery "
                    "(Dahne-Figueras, CGL) are DISSIPATIVE, and the certified inviscid ones "
                    "(Chen-Hou) use weighted energy estimates instead. That prediction is "
                    "checkable and it has not been checked here.",
            "lesson": "87 -- a certification method has a SHAPE, and the shape is a property "
                      "of the OPERATOR: multiplier or shift?",
        },
        "population_rule": POPULATION_RULE,
        "predicate": "falsifies_lesson_87(row) == in_population(row) and "
                     "row.tail_treatment == ELL1_MULTIPLIER_TAIL",
        "search_log": SEARCH_LOG,
        "gate_answers": answers,
        "clause_ablation": clause_ablation(),
        "tail_treatment_census": tail_treatment_census(),
        "diagonal_tail_near_misses": {k: list(v) for k, v in failed_clauses.items()},
        "probe_reverification": verify,
        "ledger": LEDGER,
        "scope_guard": "Cadiot arXiv:2505.03091 is recorded for METHOD SHAPE and POPULATION "
                       "MEMBERSHIP only. Whether its construction covers the zero-diagonal / "
                       "off-diagonal case NG needs is LEG 62's question (leg/cp-v1) and is "
                       "neither answered nor narrowed here.",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))

    print(f"GATE: {GATE}")
    print(f"ANSWER: {answers['as_stated']['answer']}")
    for name, a in answers.items():
        print(f"  {name:28s} {a['falsifying']:d} falsifying of {a['population']:d} "
              f"-> {a['answer']}")
    print("\ntail-treatment census over real rows:")
    for k, v in sorted(tail_treatment_census().items()):
        print(f"  {k:30s} {len(v)}  {', '.join(v)}")
    print("\nclause ablation -- what would have to change for the gate to say YES:")
    for k, v in clause_ablation().items():
        print(f"  {k:24s} {v['falsifying']:d} falsifying of {v['population']:d} "
              f"-> {v['answer']:3s} {', '.join(v['keys'])}")
    print("\ndiagonal-tail near misses (each must fail a DIFFERENT clause):")
    for k, v in failed_clauses.items():
        print(f"  {k:12s} fails {', '.join(v)}")
    print("\nprobe re-verification against Papers/<id>.txt:")
    for k, v in verify.items():
        extra = ""
        if v["status"] == "MISMATCH":
            extra = f"  {v['mismatches']}"
        print(f"  {k:14s} {v['status']}{extra}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
