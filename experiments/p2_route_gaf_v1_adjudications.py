"""Leg 303 / Route-GAF — MANUAL adjudications, applied on top of the mechanical screen.

The mechanical screen in `p2_route_gaf_v1_sweep.py` is keyword regex over title+abstract.
It is deliberately kept, unedited, in the curated JSON as `verdict_mechanical`, so that
every override below is visible as an override rather than as a silently-tuned regex.

Each entry names the clause that actually decides it, judged from **title and abstract
only** — the depth this leg is scoped to.  The adversarial full-text read of any HIT is
**reserve leg 309**, not this leg (dispatch, verbatim).

Clause vocabulary (pre-committed, writeup/novelty/leg_303.md §4):
    a_certificate  — computer-assisted / rigorous-numerics certificate
    b_blowup       — of a blow-up or singular self-similar profile
    c_dissipative  — dissipative term INSIDE the certified object
    d_fluid_model  — for a fluid transport model

Metadata below (authors, primary category, comment, journal-ref, version) came from one
further arXiv call, recorded as provenance and not as a reading of any paper:
    https://export.arxiv.org/api/query?id_list=2604.09949,2607.15256,2511.22819,
    2509.12435,1704.00560,2506.19243,2501.15701&max_results=20
"""

ADJUDICATIONS = {

    # ---------------------------------------------------------------- THE ONE HIT
    "2604.09949": {
        "verdict": "HIT",
        "failing_clause": None,
        "overrides_mechanical": "NEAR -> HIT",
        "why": (
            "All four clauses hold AT ABSTRACT LEVEL, which is the level this leg's rule is "
            "written for. (a) 'a computer-assisted Newton--Kantorovich validation based on "
            "interval arithmetic'; (b) 'finite-time singularity formation', via 'a stationary "
            "rescaled profile Ombar satisfying a nonlinear elliptic fixed-point equation'; "
            "(c) the enclosed object is the rescaled profile equation OF NAVIER-STOKES "
            "itself, not of an inviscid reduction later dominated -- this is precisely the "
            "Grade-A distinction, and it is the clause no other entrant in this sweep meets; "
            "(d) '3D incompressible Navier--Stokes equations on the periodic torus T^3'. "
            "The mechanical screen scored c_dissipative FALSE for a purely lexical reason: "
            "the regex 'navier[- ]stokes' does not match the LaTeX double hyphen in "
            "'Navier--Stokes', and the abstract uses no other dissipation word. That miss is "
            "kept visible rather than patched -- see the METHOD_FINDINGS note below."),
        "metadata": {
            "authors": "Rishad Shahmurov (single author)",
            "primary_category": "math.AP",
            "version": "v1 only", "comment": "none", "journal_ref": "none",
            "published": "2026-04-10T23:03:18Z",
        },
        "credibility_flags_visible_at_abstract_level": [
            "the abstract says the manuscript is 'organized IN THE STYLE OF a computer-assisted "
            "proof paper, with theorem statements, proof packages, and explicit validation "
            "constants' -- a description of presentation, not of a completed verification",
            "single author, v1 only, no page-count comment, no journal reference, no visible "
            "uptake in the ~4 months since posting",
            "the claim as stated (stable finite-time singularity for 3D incompressible "
            "Navier-Stokes on T^3) would resolve the Clay problem in the negative, which sets "
            "the prior accordingly",
            "the '5D-lifted axisymmetric reduction' device is not one this repository's ledger "
            "has seen used in a certified construction",
        ],
        "what_this_leg_does_with_it": (
            "RECORDS THE POINTER AND STOPS. Whether the claim stands cannot be settled from "
            "an abstract, and the adversarial full-text read is reserve leg 309's job by "
            "explicit dispatch. The cell is therefore NOT recorded as filled: it is recorded "
            "as CLAIMED, with the claim routed."),
    },

    # ---------------------------------------- mechanical HITs demoted on the (a) clause
    "1704.00560": {
        "verdict": "NEAR", "failing_clause": "a_certificate",
        "overrides_mechanical": "HIT -> NEAR",
        "why": (
            "Guillod & Sverak, J. Math. Fluid Mech. 25 (2023). The mechanical screen fired on "
            "the abstract's mention of what would follow from a proof. The paper itself is "
            "explicitly NOT a certificate: 'we calculate numerically scale-invariant solutions', "
            "and 'if the behavior seen here numerically can be proved' ... 'assuming our "
            "(finite-dimensional) numerics'. No enclosure, no interval arithmetic. It is "
            "nonetheless a genuine NRS/Tsai SCREEN-BOUNDARY document -- see screen_boundary "
            "below -- because it is the Jia-Sverak non-uniqueness program on exactly the "
            "(-1)-homogeneous scale-invariant data the screen governs."),
        "metadata": {"authors": "Julien Guillod, Vladimir Sverak",
                     "journal_ref": "J. Math. Fluid Mech. 25 (2023)"},
    },
    "2506.19243": {
        "verdict": "NEAR", "failing_clause": "a_certificate",
        "overrides_mechanical": "HIT -> NEAR",
        "why": (
            "Wang, Liu, Li, Anandkumar, Hou (cs.LG). High-precision PINN training; the "
            "mechanical screen fired on the conditional sentence 'when combined with rigorous "
            "computer-assisted proofs ... can serve as a powerful tool'. The paper supplies "
            "the high-precision approximate solution, not the enclosure. Its targets (1D "
            "Burgers, 2D Boussinesq) are also inviscid/non-dissipative-at-the-object, so (c) "
            "fails as well. Same family as arXiv:2509.14185, already an EXCLUSION row."),
        "metadata": {"authors": "Yixuan Wang, Ziming Liu, Zongyi Li, Anima Anandkumar, "
                                "Thomas Y. Hou", "primary_category": "cs.LG"},
    },

    # ---------------------------------------- the strongest NEARs, clause named
    "2607.15256": {
        "verdict": "NEAR", "failing_clause": "c_dissipative",
        "why": (
            "The most recent CAP-machinery paper the sweep returned (2026-07-16, ~26 days "
            "before this sweep). Analytic finite-rank corrections for singularly weighted "
            "estimates in the Chen-Hou 2D Boussinesq / 3D EULER computer-assisted proof. "
            "Method-side progress on exactly the machinery the empty cell would need, but the "
            "certified object is inviscid, so the cell is untouched. This is the clearest "
            "evidence for leg 174's own phrasing: the cell is empty 'for want of a target, "
            "not a method' -- the method is still being sharpened, on inviscid targets."),
    },
    "2511.22819": {
        "verdict": "NEAR", "failing_clause": "c_dissipative",
        "why": (
            "Wang, Leger, Lai, Buckmaster: neural-network resolution of unstable self-similar "
            "solutions to machine precision (IPM, 2D Boussinesq, 1D CCF). The direct successor "
            "to arXiv:2509.14185, which the ledger already holds as EXCLUSION ('CAP-ready "
            "precision; no certificate claimed'). Inviscid objects; (a) also unmet at "
            "certificate strength."),
    },
    "2509.12435": {
        "verdict": "NEAR", "failing_clause": "c_dissipative",
        "overrides_mechanical": "NEAR (d) -> NEAR (c)",
        "why": (
            "Guo, Hadzic, Jang, Schrecker, 149pp: nonlinear stability of Larson-Penston "
            "collapse for the isothermal EULER-POISSON system, using 'rigorous "
            "computer-assisted techniques in the intermediate regime' of a mode-stability "
            "problem. Clause (d) holds on adjudication (a compressible self-gravitating fluid "
            "IS a fluid transport model; the mechanical screen scored it FALSE only because no "
            "listed model name appears). Clause (c) is what fails: Euler-Poisson carries no "
            "dissipation, so the computer-assisted part encloses a non-dissipative spectral "
            "problem. Strongest new fluid-side computer-assisted entrant of the sweep, and "
            "still Grade-B-adjacent, not Grade A."),
    },
    "2501.15701": {
        "verdict": "NEAR", "failing_clause": "a_certificate",
        "why": (
            "Blow-up of 3D isentropic compressible NAVIER-STOKES at gamma=5/3 (the degenerate "
            "Merle-Raphael-Rodnianski-Szeftel case), by constructing self-similar imploding "
            "profiles of compressible EULER and transferring them to Navier-Stokes. This is "
            "structurally a NEW Grade-B/fluid row -- the same shape as arXiv:2208.09445 "
            "already in PRECEDENTS -- but the abstract claims no computer assistance at all, "
            "so it does not even reach Grade B's 'certified inviscid object' bar. It confirms "
            "the Grade-B/fluid cell is where the field's viscous blow-up results keep landing."),
    },
    "2307.03434": {
        "verdict": "NEAR", "failing_clause": "a_certificate",
        "why": (
            "Finite-time blowup for Fourier-restricted Euler and HYPODISSIPATIVE Navier-Stokes "
            "model equations, alpha < log(3)/(6 log 2) ~ 0.264. A genuine blow-up theorem for a "
            "dissipative model -- clause (c) holds in the strong sense (the dissipation is in "
            "the equation proved to blow up) -- but the proof is analytic, with no "
            "computer-assisted enclosure, so (a) fails. This is the closest the literature "
            "comes to the cell from the ANALYTIC side, and it is a model equation with a "
            "restricted Helmholtz projection, not the fluid transport model itself."),
    },
    "2308.01528": {
        "verdict": "NEAR", "failing_clause": "c_dissipative",
        "why": (
            "Exact self-similar finite-time blowup of the 1D Hou-Luo model with smooth "
            "profiles, by a purely analytic fixed-point method, explicitly supplementing the "
            "earlier computer-assisted proof. Inviscid; this is the object legs 54/55/57/291 "
            "already track."),
    },
    "2509.10806": {
        "verdict": "NEAR", "failing_clause": "a_certificate",
        "why": (
            "Navier-Stokes with fractional dissipation (-Delta)^gamma via doubly stochastic "
            "Yule cascades: finite-time blowup and non-uniqueness are established for a SCALAR "
            "PDE associated with the fractional NSE, probabilistically, not by enclosure, and "
            "not for the fluid system itself."),
    },
}


# --------------------------------------------------------------------------
# NRS/Tsai SCREEN BOUNDARY -- the gate's second half, recorded separately because a
# screen-boundary mover need not be a certificate at all.
# --------------------------------------------------------------------------
SCREEN_BOUNDARY = {
    "what_the_screen_is": (
        "Necas-Ruzicka-Sverak (1996) plus Tsai (1998): no nontrivial BACKWARD self-similar "
        "Leray solution of 3D Navier-Stokes in the relevant energy class. It is the reason "
        "this repository does not aim a self-similar viscous ansatz at 3D NS directly."),
    "verdict": "UNMOVED at the exclusion boundary; the activity is on the non-uniqueness and "
               "Type-I sides, both of which the screen already allows",
    "movers_found": [
        {"link": "https://arxiv.org/abs/1704.00560",
         "what": "Guillod-Sverak: numerical non-uniqueness for scale-invariant (-1)-homogeneous "
                 "data, the Jia-Sverak program; FORWARD self-similar, which NRS/Tsai never "
                 "excluded. Journal-published (JMFM 25, 2023), still numerical.",
         "moves_boundary": False},
        {"link": "https://arxiv.org/abs/1610.09464",
         "what": "Removing discretely self-similar singularities for 3D Navier-Stokes -- pushes "
                 "the EXCLUSION side outward (more excluded), the direction that makes the "
                 "screen stronger, not weaker.",
         "moves_boundary": "outward (strengthens the screen)"},
        {"link": "https://arxiv.org/abs/2511.09556",
         "what": "Instantaneous Type I blow-up and non-uniqueness of smooth solutions -- "
                 "Type-I/non-uniqueness side, not backward self-similar Leray.",
         "moves_boundary": False},
        {"link": "https://arxiv.org/abs/2604.07785",
         "what": "Partial Type-I solutions to axisymmetric Navier-Stokes (2026-04) -- the most "
                 "recent boundary-adjacent entrant; refines Type-I exclusion, does not touch "
                 "backward self-similar.",
         "moves_boundary": False},
        {"link": "https://arxiv.org/abs/2509.25116",
         "what": "Non-uniqueness of Leray-Hopf solutions to the unforced incompressible 3D "
                 "Navier-Stokes -- non-uniqueness, not self-similar blow-up; the screen is "
                 "silent on it.",
         "moves_boundary": False},
    ],
}


# --------------------------------------------------------------------------
# METHOD FINDINGS -- kept because they are re-usable by the next sweep leg.
# --------------------------------------------------------------------------
METHOD_FINDINGS = [
    {"id": "MF1", "title": "the LaTeX double hyphen makes a paper lexically invisible",
     "what": "The single HIT of this sweep writes its model as 'Navier--Stokes' throughout "
             "title and abstract. A regex or a search string spelling it 'Navier-Stokes' does "
             "not match it. This is a silent, systematic false-negative channel for exactly "
             "the model this project cares about most.",
     "consequence": "any future sweep must spell fluid model names with a hyphen class, e.g. "
                    "Navier[-]{1,2}Stokes, and must not treat a zero from a single spelling "
                    "as a zero."},
    {"id": "MF2", "title": "leg 174 banked counts, not links -- 10 papers are unattributable",
     "what": "solver/viscous_novelty.py::SEARCH_LOG records only (query, count). Seven of its "
             "12 queries returned a non-zero count, 10 links in total, and none of those links "
             "was written down. This sweep re-ran all 12 verbatim and every count is IDENTICAL "
             "(0/12 grew), so it is provable that leg 174's net saw the same result sets -- but "
             "NOT provable which papers it read and rejected. arXiv:2604.09949 is returned by "
             "leg 174's own query #12; whether leg 174 saw and dismissed it, or never opened "
             "it, cannot be recovered from the ledger.",
     "consequence": "this is the leg-53 'links, not counts' lesson paying its bill four months "
                    "later. This leg records all 35 queries WITH their full link sets."},
    {"id": "MF3", "title": "arXiv rate-limits a 3s-spaced sweep; an UNAVAILABLE is not a zero",
     "what": "The first pass got 6 of 35 queries back as HTTP 429/503/timeout. Had those been "
             "recorded as zeros, the sweep would have reported the single HIT's second "
             "discovery channel and the whole C4 model-name axis as empty.",
     "consequence": "the runner separates status OK from UNAVAILABLE and has a "
                    "--retry-unavailable mode at 25s spacing; the curated JSON asserts a count "
                    "only for OK rows."},
]
