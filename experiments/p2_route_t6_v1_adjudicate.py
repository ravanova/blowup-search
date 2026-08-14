"""Leg 394 / Route-T6 -- the ADJUDICATION, applied to the fetched full texts.

Reads writeup/data/p2_route_t6_v1.json (the instrument's output, produced by
experiments/p2_route_t6_v1.py) and adds the per-paper verdict table required by
the gate.  The verdicts themselves were reached by a human reading the extracted
full texts against the verdict rules PRE-REGISTERED at
experiments/journal/leg_394.md sec 0.3, which were committed at 0ee0b4c BEFORE the
first fetch and are not adjusted here.

VERDICT RULES (sec 0.3, restated so this file is self-contained):

    confirm     -- full text obtained, nothing contradicts or materially narrows
                   leg 348's recorded classification.  CONSISTENCY IS NOT
                   STRENGTHENING; this is the default landing place.  Requires a
                   deciding sentence quoted verbatim and located.
    strengthen  -- confirm, PLUS at least one S-code the ABSTRACT did not carry:
                   S1 viscous term explicitly inside the certified equation;
                   S2 explicit dimensionality of the certified object;
                   S3 explicit statement of what the computer-assisted part covers;
                   S4 explicit domain / boundary conditions the abstract lacked.
                   Each S-code carries `abstract_absent_tokens`, checked MECHANICALLY
                   against the same run's fetched abstract by the evidence script.
    UNDERCUT    -- full text contradicts, materially weakens or narrows leg 348's
                   recorded classification (trigger codes U1-U6, sec 0.3).
    UNREACHABLE -- full text not obtained or not readable.  NOT a zero, NOT a
                   confirmation.

Every quote below is EXACT and is re-found by the evidence script (a) in the
extracted full text and (b) on its own claimed page, by independent re-extraction.
A paraphrase exits non-zero.  Gate by EXIT CODE, never by a printed line.

    .venv/bin/python experiments/p2_route_t6_v1_adjudicate.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data" / "p2_route_t6_v1.json"


VERDICTS = [
    {
        "id": "math/0005247",
        "paper": "P1",
        "authors_as_served": "P. Zgliczynski, K. Mischaikow",
        "leg348_recorded_authors": "Zgliczynski",
        "verdict": "strengthen",
        "s_codes": ["S4"],
        "u_codes": [],
        "deciding_sentence": "subject to periodic and odd boundary conditions",
        "locator": "sec 1, between eq. (1) and eq. (2), p.2",
        "supporting": [
            {
                "quote": "we do not pursue these more complicated structures in this paper",
                "locator": "sec 1, p.3",
                "what_it_settles": (
                    "leg 348's careful reading is CORRECT and is confirmed at full text: this "
                    "paper's certified objects are FIXED POINTS, not periodic orbits. The "
                    "periodic-orbit extension is named as possible 'in principle' and explicitly "
                    "NOT carried out here."
                ),
            },
        ],
        "s_code_detail": {
            "S4": {
                "claim": (
                    "The full text states the domain and the boundary conditions EXPLICITLY -- "
                    "KS on (-pi, pi) with periodic and odd boundary conditions, eq. (1)-(2) -- "
                    "where leg 348 could only INFER them ('abstract does not state BC explicitly "
                    "but ... is the standard periodic-domain Fourier-truncation construction in "
                    "this line of work'). The inference is now a stated fact."
                ),
                "abstract_absent_tokens": ["boundary condition", "periodic", "odd"],
            }
        },
        "leg348_classification_status": (
            "ACCURATE and now better evidenced. The domain-compactness inference leg 348 flagged "
            "as an inference is confirmed by the paper's own problem statement."
        ),
    },
    {
        "id": "2305.08221",
        "paper": "P2",
        "verdict": "strengthen",
        "s_codes": ["S2"],
        "u_codes": [],
        "deciding_sentence": (
            "we develop a rigorous computational method for validating solutions of initial "
            "value problems for scalar semilinear parabolic equations, with periodic boundary "
            "conditions, of the form"
        ),
        "locator": "sec 1, immediately above eq. (1), p.2",
        "supporting": [],
        "s_code_detail": {
            "S2": {
                "claim": (
                    "eq. (1) fixes the spatial domain and the dimensionality explicitly -- "
                    "x in [0, 2 pi], ONE space dimension -- neither of which the abstract "
                    "carries ('scalar' qualifies the unknown, not the space). Leg 348 recorded "
                    "the periodic BC from the abstract; the full text adds the domain itself."
                ),
                "abstract_absent_tokens": ["2π", "2 pi", "one-dimensional"],
            }
        },
        "k4_probe_adjudications": [
            {
                "probe": "whole space",
                "hit_context": "Over the whole space, the norm",
                "locator": "sec 3, above Lemma 3.6, p.13",
                "adjudication": (
                    "NOT an undercut. 'whole space' here is the whole BANACH space X_nu, not a "
                    "spatial domain. The probe fired and was adjudicated, which is what K4 is for."
                ),
            }
        ],
        "leg348_classification_status": "ACCURATE.",
    },
    {
        "id": "1902.00384",
        "paper": "P3",
        "verdict": "UNDERCUT",
        "s_codes": [],
        "u_codes": ["U3"],
        "deciding_sentence": (
            "While all of the analysis is performed in full generality on the 3-torus, the "
            "solutions we present in Theorem 1.1 below are two-dimensional (in space) "
            "time-periodic solutions."
        ),
        "locator": "sec 1, p.3",
        "supporting": [
            {
                "quote": (
                    "Indeed, they are homogeneous in one spatial variable and can thus be "
                    "interpreted as solutions on the 2-torus."
                ),
                "locator": "sec 1, p.3",
                "what_it_settles": (
                    "The certified object IS a lift of a lower-dimensional one -- which is "
                    "exactly the disqualifier WALLS.md's W2 pre-committed test names."
                ),
            },
            {
                "quote": (
                    "they are independent of x3 and the third component of the velocity "
                    "vanishes. We call such a solution an (essentially) 2D solution."
                ),
                "locator": "sec 1, p.3",
                "what_it_settles": "u_3 = 0 and d/dx_3 = 0 on the certified solution. Stated by the authors.",
            },
            {
                "quote": (
                    "The only reason for this reduction is that the physical memory requirements"
                ),
                "locator": "sec 1, p.3 (continues '...for a three-dimensional solution are, for now, prohibitive in our current implementation.')",
                "what_it_settles": (
                    "THE REASON IS COST, NOT MATHEMATICS. The analytic estimates are built in "
                    "full generality on T^3; what is missing is memory. That is a price, and a "
                    "price is a number -- it does NOT make the 3D case impossible, and this "
                    "leg does not claim it does."
                ),
            },
            {
                "quote": "Theorem 2.15. Let",
                "locator": "sec 2.4, p.13 (statement continues: 'eta > 1 ... assume there exist W in X and non-negative constants Y_0, Z_0, Z_1 and Z_2')",
                "what_it_settles": (
                    "THE APPARATUS, READ AT FULL TEXT AND RELEVANT TO RULING C1: the paper's "
                    "validation theorem is literally a Y_0 / Z_0 / Z_1 / Z_2 radii-polynomial "
                    "contraction, and Z_0 = ||I - A A_dagger|| requires a BOUNDED APPROXIMATE "
                    "INVERSE A. C1's own words: 'A unit that reaches for a Y_0/Z_0/Z_1/Z_2 "
                    "contraction, IN ANY SPACE, is inside the ban whatever it calls itself.' "
                    "This is NOT the Galerkin-plus-tail dynamical closure C1 put outside the ban. "
                    "It CONFIRMS leg 348's own apparatus sorting (leg 348 called it 'the same "
                    "NK-in-exponentially-decaying-coefficient-basis family already measured DEAD "
                    "in this repository') -- and it is a fact unit T4 needs, because T4 is "
                    "chartered to reproduce THIS paper with a C1-COMPLIANT apparatus."
                ),
            },
        ],
        "what_is_NOT_undercut": (
            "The viscous term IS inside the certified equation. Eq. (1.1) carries -nu Delta u; "
            "the zero-finding problem is derived from the vorticity form of (1.1); and the tail "
            "of the approximate inverse acts diagonally as lambda_n = 1 / (nu n^2 + i Omega n), "
            "i.e. the VISCOSITY is what makes the tail of A bounded. Leg 348's parenthetical "
            "'(viscous term inside the certified equation)' STANDS. The domain is genuinely the "
            "three-torus. What does not stand is 'genuine 3D' / 'natively 3D'."
        ),
        "leg348_classification_status": (
            "SPLIT. Leg 348's QUOTE is accurate -- the abstract does say 'on the three-torus'. "
            "Leg 348's INFERENCE is not: its `relevance` field calls this 'a periodic orbit of "
            "genuine 3D NS', and WALLS.md's W2 crack calls the object 'natively 3D'. The "
            "certified solutions of Theorem 1.1 are, in the authors' own words, '(essentially) "
            "2D'. This is precisely the failure mode W2 exists to name -- 'Every published work "
            "stating a 3D singularity theorem with a certificate obtains the 3D-ness from "
            "somewhere other than the certificate' -- and it is invisible from the abstract, "
            "which is why leg 348 could not have caught it at abstract level."
        ),
        "consequence_for_T4": (
            "T4 / leg 393 is running against THIS paper in THIS wave. Two findings bear on it, "
            "and neither is this unit's to rule on. (1) The rows T4 reproduces are rows for an "
            "(essentially) 2D certified solution, so a successful reproduction does NOT "
            "demonstrate a certificate supplying its own three-dimensionality, and T4's write-up "
            "must not be read as clearing W2's pre-committed test. (2) The paper's apparatus is a "
            "Y_0/Z_0/Z_1/Z_2 contraction with a bounded approximate inverse -- which is T4's own "
            "pre-committed reading (c) firing on the paper rather than on the implementation. "
            "REPORTED, NOT RULED: the Conductor decides what happens to T4."
        ),
    },
    {
        "id": "2409.09234",
        "paper": "P4",
        "verdict": "UNDERCUT",
        "s_codes": [],
        "u_codes": ["U4", "U1"],
        "deciding_sentence": (
            "our results, depending on numerical approximations, do not guarantee that the "
            "Navier-Stokes solutions exhibit chaotic behaviour in the sense of Devaney"
        ),
        "locator": "sec 5 Conclusion, p.9",
        "supporting": [
            {
                "quote": (
                    "the theorems hinge upon an imperative condition: the map must be "
                    "one-dimensional and continuous"
                ),
                "locator": "sec 3, p.5",
                "what_it_settles": (
                    "The rigorous content (Li-Yorke / Sharkovskii) is a theorem about a ONE-"
                    "DIMENSIONAL MAP fitted to DNS data, not about the Navier-Stokes system. "
                    "There is no interval arithmetic, no Galerkin projection, no tail-domination "
                    "estimate and no Newton-Kantorovich argument anywhere in the paper. The "
                    "UPOs themselves are obtained by a (non-rigorous) Poincare-Newton-Krylov "
                    "solve on DNS data."
                ),
            },
            {
                "quote": "Periodicity is enforced to the rest of boundaries of the parallelogram domain",
                "locator": "sec 2, p.4",
                "what_it_settles": (
                    "U1, secondary: the domain is NOT a periodic cell. It carries NO-SLIP "
                    "rotating-wall Dirichlet conditions at r = r_i and r = r_o and is periodic "
                    "only in the remaining directions. Leg 348 filed it under 'minimal periodic "
                    "domain' on the abstract's phrase alone."
                ),
            },
        ],
        "leg348_classification_status": (
            "SPLIT, and the aggregate is the part that breaks. Leg 348's per-paper `method` field "
            "-- 'rigorous chaos statement via a discrete map approximation' -- is ACCURATE. But "
            "leg 348 then used this paper as one of its seven instances of the certification "
            "technology, writing in its journal sec 3 that 'every located instance of the "
            "self-consistent-a-priori-bounds / Galerkin-plus-tail / NK-in-Fourier-space "
            "technology -- ... a Taylor-Couette UPO paper (arXiv:2409.09234 ...) -- closes its "
            "tail-domination (neglected-mode) estimate against a COMPACT domain'. THIS PAPER "
            "CLOSES NO TAIL-DOMINATION ESTIMATE AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT "
            "ALL. The census over-counts by one."
        ),
        "consequence": (
            "`p2_route_pocp_v1.json.domain_census.compact_or_periodic_domain` lists six entries; "
            "one of them (this paper) is not an instance of the technology being censused, and a "
            "second (P3) is an instance whose certified object is essentially 2D. The obstruction "
            "leg 348 named is NOT thereby refuted -- no counter-instance on an unbounded, "
            "algebraically weighted domain was found at full text either -- but the evidence base "
            "for it is thinner than the record says. REPORTED, NOT RULED."
        ),
    },
    {
        "id": "2105.04148",
        "paper": "P5",
        "verdict": "strengthen",
        "s_codes": ["S2"],
        "u_codes": [],
        "deciding_sentence": (
            "This is essentially the Brussellator system with diffusion and Dirichlet boundary "
            "conditions"
        ),
        "locator": "sec 1, immediately below eq. (1), p.2",
        "supporting": [],
        "s_code_detail": {
            "S2": {
                "claim": (
                    "eq. (1) fixes the domain and the dimensionality explicitly -- ONE space "
                    "dimension, x in (0, pi), with U(0,t) = U(pi,t) = V(0,t) = V(pi,t) = 0 -- "
                    "neither of which the abstract carries. The abstract names the BC type only."
                ),
                "abstract_absent_tokens": ["π", "one-dimensional", "1D"],
            }
        },
        "k4_probe_adjudications": [
            {
                "probe": "real line",
                "hit_context": "a property that simplifies the computer assisted estimates",
                "locator": "sec 1, p.2 (full sentence: 'This choice allows solutions admitting analytic extensions to the whole real line, a property that simplifies the computer assisted estimates')",
                "adjudication": (
                    "NOT an undercut, and it is the closest call in the set. The 'whole real line' "
                    "is the domain of ANALYTIC EXTENSION of the solutions, invoked to make the "
                    "computer-assisted estimates easier; the PDE is still posed on (0, pi) with "
                    "Dirichlet conditions. This is a genuine near-miss on trigger U1 and it is "
                    "recorded as adjudicated, not silently dropped."
                ),
            }
        ],
        "leg348_classification_status": "ACCURATE.",
    },
    {
        "id": "2009.12762",
        "paper": "P6",
        "verdict": "strengthen",
        "s_codes": ["S1"],
        "u_codes": [],
        "deciding_sentence": "Following [21], we impose Navier boundary conditions",
        "locator": "sec 1, immediately above eq. (1.2), p.1",
        "supporting": [
            {
                "quote": "In order to reduce the complexity of the problem, the domain",
                "locator": "sec 1, p.1 (continues '... Omega is chosen to be as simple as possible, namely the square Omega = (0, pi)^2.')",
                "what_it_settles": "Explicit bounded 2D domain, confirming leg 348's abstract-level read.",
            },
        ],
        "s_code_detail": {
            "S1": {
                "claim": (
                    "The abstract never exhibits the equation, so it cannot state that the viscous "
                    "term is inside the certified one. The full text does: eq. (1.1) is "
                    "d_t u - nu Laplacian u + (u.grad)u + grad p = f, and after the rescaling "
                    "u -> nu^{-1} u it is eq. (1.4), alpha d_t u - Laplacian u + gamma (u.grad)u "
                    "+ grad p = f, which is the equation Theorem 1.1's certified solutions solve. "
                    "The dissipative term is INSIDE the certified equation."
                ),
                "abstract_absent_tokens": ["∆", "Δ", "Laplac", "grad p"],
            }
        },
        "leg348_classification_status": "ACCURATE.",
    },
    {
        "id": "2308.01528",
        "paper": "P7",
        "verdict": "confirm",
        "s_codes": [],
        "u_codes": [],
        "deciding_sentence": "denotes the Hilbert transform on the real line",
        "locator": "sec 1, immediately below eq. (1.1), p.1",
        "supporting": [
            {
                "quote": (
                    "Therefore, it would be helpful to develop pure analytic strategies to prove "
                    "the existence of exact self-similar finite-time blowups"
                ),
                "locator": "sec 1, p.2",
                "what_it_settles": (
                    "Confirms leg 348's apparatus sorting: this paper's method is PURELY "
                    "ANALYTIC and is offered as an alternative to the computer-assisted route, "
                    "not as an instance of the Galerkin-plus-tail technology."
                ),
            },
        ],
        "k4_probe_adjudications": [
            {
                "probe": "algebraic decay / axisymmetric / Euler equation / real line",
                "hit_context": "sec 1's discussion of [CHH22] and [CH22]",
                "locator": "sec 1, p.1-2",
                "adjudication": (
                    "NOT an undercut of THIS paper's classification, but it is the one thing at "
                    "full text that narrows leg 348's AGGREGATE claim and it is recorded rather "
                    "than dropped. The full text characterises Chen-Hou [CH22] as a "
                    "computer-assisted proof of asymptotically self-similar blow-up for the 2D "
                    "Boussinesq / 3D Euler equations -- i.e. computer-assisted certification "
                    "reaching MORE THAN 1D on an UNBOUNDED domain (the half-space R x R+) with "
                    "algebraic far-field decay. It does NOT fire trigger U6, because U6 requires "
                    "a TIME-PERIODIC target and CH22's target is a stationary self-similar "
                    "profile, and because CH22's apparatus is energy estimates with "
                    "computer-assisted constants, not a Galerkin-plus-tail dynamical closure. "
                    "Recorded as a NARROWING OBSERVATION, deliberately NOT banked as a verdict."
                ),
            }
        ],
        "leg348_classification_status": "ACCURATE.",
    },
]


def main() -> int:
    data = json.loads(DATA.read_text())
    data["verdict_rules"] = {
        "pre_registered_at": "experiments/journal/leg_394.md sec 0.3, committed 0ee0b4c BEFORE the first fetch",
        "confirm": "reachable and not contradicted; CONSISTENCY IS NOT STRENGTHENING",
        "strengthen": "confirm PLUS an S-code (S1-S4) the abstract did not carry, checked mechanically",
        "UNDERCUT": "contradicts, materially weakens or narrows leg 348's recorded classification (U1-U6)",
        "UNREACHABLE": "full text not obtained or not readable -- NOT a zero, NOT a confirmation",
    }
    data["verdicts"] = VERDICTS
    counts = {"confirm": 0, "strengthen": 0, "UNDERCUT": 0, "UNREACHABLE": 0}
    for v in VERDICTS:
        counts[v["verdict"]] += 1
    data["verdict_counts"] = counts
    data["gate_answer"] = {
        "answered": True,
        "headline": (
            "TWO UNDERCUTS. arXiv:1902.00384's certified solutions are, in the authors' own "
            "words, '(essentially) 2D' -- homogeneous in x3 with u3 = 0 -- so the certificate "
            "does NOT supply its own three-dimensionality, which is the exact thing WALLS.md's "
            "W2 crack claimed it did. arXiv:2409.09234 proves nothing rigorous about "
            "Navier-Stokes at all, by its own conclusion, so leg 348's technology census "
            "over-counts it."
        ),
        "table": "see `verdicts` above; one row per paper, deciding sentence verbatim, located",
        "unreachable": 0,
        "note_on_unreachable": "no paper was UNREACHABLE; 7/7 full texts retrieved and extracted",
    }
    data["clay_status"] = {
        "l1_l4_chain_moved": False,
        "clay_odds": "~0.05%, unchanged",
        "note": (
            "A literature re-read at full text is not movement toward Clay in either direction. "
            "TIER 2 ceiling; nothing here is a proof. Both walls stand -- and W2's recorded "
            "CRACK is what this unit narrows, not W2 itself."
        ),
    }
    DATA.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {DATA.relative_to(ROOT)}")
    print(json.dumps(counts, indent=2))
    for v in VERDICTS:
        print(f"  {v['paper']} {v['id']:14s} {v['verdict']:11s} "
              f"{','.join(v['s_codes'] + v['u_codes']) or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
