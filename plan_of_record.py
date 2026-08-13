"""THE PLAN OF RECORD — the committed sequence, machine-readable, with its own gates.

--------------------------------------------------------------------------
WHY THIS FILE EXISTS
--------------------------------------------------------------------------
This project's characteristic failure is not error.  It is **drift**.  Ranked item (3) sat at
the top of the list marked "most important" and lost to a cheaper leg **six consecutive
times**; five literature passes were written while zero papers were read; a resolution ladder
showing the method diverging sat in `writeup/data/` for two legs with nobody reading the
column's direction.  Every one of those was prevented by a document that said the right thing
and was not consulted.

Banked lesson (68) is the general form: **a check that is not executable decays at the rate
of memory.**  Route-J applied it to the literature.  This file applies it to the plan.

`test_plan_of_record.py` asserts that the committed sequence, `CONTINUATION_PROMPT.md`,
`CLAY_ROADMAP.md` §7 and the working notes **agree with each other**, and that every stage
carries a pre-committed gate naming BOTH outcomes.  A plan that has drifted fails the suite.

    .venv/bin/python plan_of_record.py          # print status
    .venv/bin/python test_plan_of_record.py     # fail if the plan has drifted

--------------------------------------------------------------------------
WHAT WAS ADOPTED, AND WHAT WAS NOT
--------------------------------------------------------------------------
Adopted by the user on 2026-08-04, after leg 44: **re-aim the search machinery from finding
the OBJECT to closing the CERTIFICATE**, sequenced behind a target-selection leg. Stage B,
that certificate-search stage, closed its own gate NO at leg 126 (audited its full declared
search space: 1,686/1,686 configurations covered, zero uncovered; a perfect search would
still land at Z1 >= 6.0424, 6.04x short) -- the committed sequence was EXHAUSTED for many
cycles, parked as escalation #1.

**SUPERSEDING RULING, 2026-08-06 (user decision, resolving escalation #1):** the exit
criterion is answered -- **pursue a full Clay solve.** This supersedes the "novel Tier-3
result, NOT Clay" prize below. The user explicitly accepts that this means building
seriously heavy code, and explicitly does NOT lower the evidentiary bar for the change:
**Clay stays a ~0.05% horizon, recorded in the same breath as the goal change, not quietly
dropped now that the prize is bigger.** Walls 1 and 2 (`CLAY_ROADMAP.md` §2, and Wall 2 as
corrected below per leg 172) still cap everything. No output is ever described as movement
toward Clay unless a link of the L1->L4 chain actually moves -- that rule is EASIER to erode
under a Clay-directed programme, not harder, and it does not relax.

The programme is sequenced deliberately, per this repository's own Route-A discipline (two
unknowns are never debugged simultaneously): Phase 0 (target selection under the Clay goal,
constrained by Necas-Ruzicka-Sverak and Tsai's exclusion of nontrivial exactly-backward-
self-similar 3D NS blow-up) before Phase 1 (the viscous rung -- can ANY model's viscous
blow-up be certified? The Grade-A/fluid cell is empty -- no published work applies interval
arithmetic to a dissipative FLUID equation's own self-similar object -- but Grade-A
dissipative certification DOES exist off the fluid axis: Dahne-Figueras CGL
(arXiv:2410.05480), reproduced row-for-row by leg 316, and Breden-Chu's viscous Burgers.
Corrected from "no certified viscous blow-up exists in any model, in any dimension" per the
user's external-review packet of 2026-08-11: the cell is empty, the generalisation from that
cell to every model in every dimension was an over-read (over-read closure #5, after 165,
180, 185, 178). The Phase-1 rationale is unchanged and does not depend on the wider claim; if
it cannot be done for a dissipative FLUID equation in 1D, 3D NS is not a question of compute)
before Phase 2 (the
3D near-singular viscous solver, `PLAN.md` Stage 4, user-authorized but unscheduled until
Phase 1 reports -- a 3D candidate with no certification story reproduces Hou-Luo 2013 and
answers nothing).
"""

ADOPTED = "2026-08-04"
ADOPTED_BY = "user decision, in session; supersedes the ranked-item habit"

GOAL_CHANGE_DATE = "2026-08-06"
GOAL_CHANGE_BY = ("user ruling, resolving escalation #1 (stage B exhausted with no "
                   "successor); supersedes the prior Tier-3-not-Clay prize")

PRIZE = ("Pursue a full Clay solve (rigorous resolution of the 3D Navier-Stokes "
         "regularity/blow-up problem), adopted 2026-08-06, superseding the prior "
         "'novel Tier-3 result, NOT Clay' prize. Clay odds stay ~0.05% -- an accepted "
         "risk under the new goal, not a claim of movement -- behind Walls 1 and 2.")

WALLS = [
    ("Wall 1", "A search can only argue FOR blow-up, never for regularity. If 3D NS is "
               "globally smooth, this programme is empty by construction. Caps everything. "
               "Direction (a) (global regularity) is additionally closed to anything "
               "search-/certificate-shaped by Tao's averaged-NS supercriticality barrier: "
               "energy methods plus the preserved algebraic structure are provably "
               "insufficient. Only direction (b) (blow-up) is in scope."),
    ("Wall 2", "CORRECTED 2026-08-06 per leg 172: the NAIVE form (spatial dimension is the "
               "barrier) is FALSE -- van den Berg-Williams certified genuinely 3D "
               "Ohta-Kawasaki stationary states in 2019. The real barrier is TIME-DEPENDENT "
               "singularity formation, not dimension. Every work stating a 3D singularity "
               "theorem WITH a certificate supplies the 3D-ness via a 2D reduction "
               "(Chen-Hou) or a spherically-symmetric ODE profile (BCG -> CGSS) -- never "
               "via the certificate itself. Any Clay plan must say explicitly which side of "
               "that line it lives on. The missing rung is viscous certification: no "
               "certified viscous blow-up exists in any model, any dimension (leg 174's "
               "occupancy matrix, leg 242 confirms still empty). A cheaper certificate does "
               "not by itself cross this -- it is what Phase 1 exists to test."),
]

CLAY_ODDS = 0.0005

# --------------------------------------------------------------------------
# the posture, adopted 2026-08-13 -- THE WALLS ARE THE WORK
# --------------------------------------------------------------------------
# User ruling 2026-08-13, recorded in CLAY_ROADMAP.md sec 7.6 and ORCHESTRATION.md sec 3g/3h.
# NOTHING BELOW LIFTS, NARROWS OR REWORDS A BAN.  This block is additive: it records the mode,
# points at the blocker enumeration, and names the lanes, so that a task consulting this file
# executably learns where the work is ranked -- lesson 68 again, a check that is not executable
# decays at the rate of memory.
#
# The two-item WALLS list above is CLAY_ROADMAP.md sec 2's pair of STRUCTURAL walls and is
# unchanged.  WALLS.md is a different and larger object: SEVEN blockers between here and a Clay
# answer, each with its evidence separated from its assumption and each with a PRE-COMMITTED
# statement of what breaking it consists of.  Read that file whole before working in a lane.

POSTURE = "the walls are the work (user ruling 2026-08-13)"
POSTURE_ADOPTED = "2026-08-13"
BLOCKERS_FILE = "WALLS.md"          # 7 walls (W1-W7), 4 lanes -- read whole, never paraphrased
MODE = "CONDUCTOR"                  # ORCHESTRATION.md sec 3g; direction and integration are one entity

# lane id -> (walls attacked, one line).  Ranking is the Conductor's and is stated in STATE.md;
# this table exists so a worker can see which wall its unit is against without reading DIRECTION.md.
LANES = [
    ("T", "W2, W4, W6", "TORUS -- priority 1. POCP's only named obstruction (leg 348) is DOMAIN "
                        "SHAPE; T^3 is that domain; arXiv:1902.00384 already certifies a viscous "
                        "3D-NS periodic orbit there; leg 390 sec 5 item 4 records the credit "
                        "UNCLAIMED. Price: 0 of 4 rigidity clearances carry to T^3, the periodic "
                        "rigidity literature has never been searched here, and the DSS ansatz does "
                        "NOT survive periodization (342 modes survive one step at lambda=1.7, 0 "
                        "survive two) -- so the lane needs a NON-DSS ansatz that does not exist yet. "
                        "Lane T does NOT retire CLAY_OBLIGATIONS.md sec 6's two obligations."),
    ("V", "W3",         "VISCOUS RUNG -- fill the Grade-A x fluid cell in the lowest dimension "
                        "admitting fluid structure. Leg 174: empty FOR WANT OF A TARGET, not a "
                        "method. Both branches valuable, which is what makes it cheap."),
    ("L", "W4, W5",     "LOCALISATION, PRICED -- sec 4's 'no known method' is the one load-bearing "
                        "roadmap claim never checked to this repository's own standard, and "
                        "CLAY_OBLIGATIONS.md sec 6's TWO no-method obligations (certified far-field "
                        "decay with an admissible cutoff; persistence under that localisation) live "
                        "here. NO UNIT IN 390 LEGS HAS ATTACKED EITHER."),
    ("R", "W7",         "REFORMULATION FOR SCALE + SOLVER COMPETITIVENESS -- attack the compute wall "
                        "by mathematics, not procurement; every factor removed is permanent and "
                        "transfers to Lane T unchanged. REPORTED METRIC IS DISTINCT ORBITS PER "
                        "CORE-HOUR, not per-attempt convergence rate (R0). A best-in-field orbit "
                        "finder makes questions affordable; it does NOT move a Clay link."),
]

# What the posture does NOT license -- ORCHESTRATION.md sec 3h, restated executably.
POSTURE_LIMITS = [
    "A ban is superseded by a MEASUREMENT, never by a decision. The permitted move is the "
    "2026-08-11 SCOPING of the DSS expensive-entrance ban: read the ban's own text, find an "
    "object it does not name, open that lane while the measurement stays true.",
    "A ban whose WORDING has become defective is a USER ESCALATION (sec 8), not an agent's "
    "reading. The three that were pending were RULED BY THE USER 2026-08-13 (writeup/"
    "escalations/RULING_BAN_WORDING_2026-08-13.md): Cadiot = A2, the ban STANDS and its "
    "clause is CLOSED; stage V's 'needs L1 first' = B1, STRUCK as editorial; the apparatus "
    "question = C1, the ell^1-Fourier/radii-polynomial ban NAMES AN APPARATUS and a "
    "Galerkin-plus-tail DYNAMICAL closure is outside it. C1 binds every unit claiming it to "
    "NAME ITS APPARATUS and SHOW IT BUILDS NO SINGLE BOUNDED APPROXIMATE INVERSE UNIFORM IN "
    "M; absent both, the ban applies in full. One defect is knowingly left open: the lift "
    "clause still names a FOURTH SPACE/BASIS, which is the wrong kind of object for a "
    "candidate that is an APPARATUS.",
    "Scale is not evidence. A large build is not a result; the gate is the deliverable.",
    "The ceiling clause survives the ambition. Tier 2 is never called a proof, and no output is "
    "described as movement toward Clay unless a link of the L1->L4 chain actually moved. Clay "
    "stays ~0.05%.",
    "A wall may be reported as UNBROKEN. sec 3d still governs: an under-resourced attempt returns "
    "UNDER-RESOURCED and a cost estimate, never NO.",
]

# --------------------------------------------------------------------------
# the committed sequence
# --------------------------------------------------------------------------
# status: DONE | NEXT | QUEUED
# Every stage MUST carry a gate with both branches spelled out.  This project has shipped
# gates that only specified the pass branch (Route-H's refusal predicate is the counterexample
# that fixed it); the test suite enforces both.
STAGES = [
    {
        "id": "M",
        "name": "Target selection -- certify WHAT, that isn't already done?",
        "status": "DONE",
        "done": (
            "leg 45, 2026-08-04. GATE: YES. solver/target_selection.py + "
            "test_target_selection.py 9/9; experiments/p2_route_m_v1_targets.py -> fig42; "
            "PHASE2_P2_NOTES section 34. **Named target: HL_S2_nonsymmetric** -- the "
            "non-symmetric positive regular self-similar profile of the 1D Hou-Luo model "
            "(Chen-Huang-Li arXiv:2604.01868 sections 2.5/4), uncertified, at 1.11e-3 of "
            "the certified object's unknown count, needing THREE modulation constants "
            "because it has no symmetry point to pin the translation. Four uncertified "
            "candidates found in total; seven objects moved onto the exclusion list, four "
            "of them proved ANALYTICALLY. The 3D-NS preprint arXiv:2604.09949 is recorded "
            "as CLAIMED_UNUSABLE with its scalar closure audited in both forms (both "
            "close -- the arithmetic is not where it fails)."),
        "why_first": (
            "The port's entire value is contingent on there being an uncertified target at "
            "the end of it, and nobody has checked. The 2D Boussinesq profile the port aims "
            "at is the one Chen-Hou certified in 145 pages: closing a radii polynomial there "
            "proves we CAN certify, it is not a new result. Leg 42 deleted seven of twelve "
            "standing novelty claims, so the 'novel' bar is measurably higher than assumed."),
        "deliverable": (
            "A ranked, sourced ledger entry per candidate object answering three questions: "
            "(1) is there a computer-assisted proof of THIS profile (not merely 'is blow-up "
            "known'); (2) is it within interval-arithmetic reach -- record state dimension, "
            "the nonlocal operator's form, and whether comparable validated numerics exist; "
            "(3) what would certifying it contribute, in a sentence a specialist would "
            "accept. Extend solver/literature_gates.py's ledger, do not write prose."),
        "inputs": ["Papers/MANIFEST.md Tier 2 and Tier 3 -- fetched, extracted, NEVER READ",
                   "2302.12877 answers (2) for a whole class at once",
                   "2308.01528 and 2604.01868 bear directly on (1)"],
        "gate": {
            "question": "Does an uncertified, interval-arithmetic-reachable target exist?",
            "if_yes": ("Name it. Re-aim stage PORT at that object. This is the good outcome "
                       "and it is a re-plan, not a continuation."),
            "if_no": ("SAY SO AND STOP. That is a decisive negative about the whole "
                      "programme, worth more than any further leg, and it must be reported "
                      "to the user. Do NOT soften it into 'more search needed'."),
        },
        "time_box": "one leg",
    },
    {
        "id": "PORT",
        "name": ("Finish the certification port -- RE-AIMED BY M at the 1D non-symmetric "
                 "Hou-Luo profile, as a BORDERED system"),
        "status": "DONE",
        "done": (
            "leg 46, 2026-08-04. GATE: YES, WITH A CEILING. solver/bordered_hl.py + "
            "test_bordered_hl.py 10/10; experiments/p2_route_port_v1_bordered.py -> "
            "writeup/data/p2_route_port_v1_bordered.json; PHASE2_P2_NOTES section 35; 7/7 "
            "pre-committed clauses. Newton converges to 5.7e-15 in 16 steps (4 on "
            "continuation) where the relaxation floors at ~1e-2; the contraction ratio "
            "extrapolates to -2.511926 against CHL's -2.5114 (2.09e-04), the 1.17% gap "
            "attributed to REACH not resolution. **The radii polynomial CLOSES IN FLOAT at "
            "every rung** (Y0/budget 1.95e-04 / 6.36e-04 / 2.40e-04 at n=201/401/801). "
            "**AND CLAUSE P6b -- pre-committed before the certificate was computed -- SAYS "
            "THE BALL IS 1.55e+08x TOO SMALL TO CONTAIN THE OBJECT**: the truncation "
            "distance is 1.831e-01 against r_max 1.18e-09. It closes around the TRUNCATED "
            "object. It is a float rehearsal (A = DF^-1 in float64), not a proof. Carried to "
            "stage B: one weight constant is worth ~5200x, and p* = 0.39 is a wall the "
            "EQUATION built (the tail is |X|^-0.394). **LEG 47 (Route-PORT v2) then priced "
            "the ceiling: extending the domain makes the gap WORSE, +0.47 decades per unit "
            "rho -- the distance is flat (-0.02) while the ball shrinks (-0.49) -- so reach "
            "cannot close it AT ANY SIZE and an analytic far-field enclosure (a tail lemma) "
            "is FORCED. The L1 road is now priced: interval arithmetic (engineering) plus a "
            "tail lemma (mathematics, and nobody here has written one).**"),
        "why_here": (
            "M re-aimed this stage, which is what M's YES branch said it would do. The "
            "target is HL_S2_nonsymmetric, not Chen-Hou's 2D profile: same certification "
            "chain, an object nobody has proved, and 1.11e-3 of the unknowns. Chen-Hou's "
            "object remains available as the KNOWN-ANSWER substrate for validating stage "
            "C-PILOT's fitness -- that role never needed the certificate to close, only the "
            "answer to be known, and it is the reason the 2D work is not wasted."),
        "deliverable": (
            "(1) The bordered residual for CHL (4.1) with all THREE modulation constants "
            "(c_l, c_omega, c_r) as unknowns -- built as a bordered system from the start, "
            "NOT projected after the fact, which is what failed in 2D. (2) A converged "
            "profile with the contraction ratio against CHL's -2.5114. (3) Then the "
            "function space, Y_0 and Z_1 -- now measurable, against the budget "
            "(1-Z_1)^2/(2 Z_2) that solver/target_selection.py computes."),
        "known": ["The solver EXISTS: solver/hl_rescaled.py::RescaledHLScenario2, gauge "
                  "gated to 4.4e-16, ratio reproduced to ~1% (PHASE2_P2_NOTES section 8). "
                  "It was built 2026-07-26 and then left unused for nine legs.",
                  "Route-M made the Scenario-2 step 10x faster (line_hilbert.slope_matrix, "
                  "gated at 2.7e-13) -- the refinement ladder is affordable now.",
                  "CHL's own normalization (4.2) pins d_tau{Omega(0),Omega_X(0),V(0)}=0; "
                  "the absolute triple is normalization-dependent, the RATIO c_l/c_omega "
                  "is not. Compare against the ratio (leg 45 M3, and section 8 before it).",
                  "The 2D near-null direction from leg 44 is STILL UNIDENTIFIED, and leg "
                  "45 raises the odds it was the translation mode: CHL needed a third "
                  "constant for exactly this family. That is now a question about the 2D "
                  "object, which is no longer the target -- do not spend the leg on it.",
                  "The scaling gauge is REFUTED as the 2D near-null direction (leg 44 L-7)."],
        "gate": {
            "question": "Does the radii polynomial close in float, with margin?",
            "if_yes": ("Report it. The certification capability exists and stage C-PILOT can "
                       "use it as a validated fitness."),
            "if_no": ("STOP AND REPORT -- do not harden. A negative here is worth more than "
                      "a positive anywhere else, because it is about the object certification "
                      "results actually count on."),
        },
        "time_box": "two legs (identify, then border+solve)",
    },
    {
        "id": "V",
        "name": ("Viscous survival, IN FLOAT: does the certificate's margin survive "
                 "dissipation as mu -> criticality?  -- CLOSED BY ITS OWN GATE, leg 48"),
        "status": "DONE",
        "why_here": (
            "USER DIRECTION, 2026-08-04, after being shown that the L1->L4 chain cannot be "
            "climbed: L2 and L3 are occupied by Chen-Hou and L4 is out of reach of interval "
            "arithmetic, so 'move a link' has no Clay-relevant reading. This is the ONE route "
            "identified that is both Clay-ADJACENT and matched to what this project already "
            "owns. The Euler->NS gap IS viscosity: 3D Euler blow-up with boundary is proved, "
            "NS is not, and the entire difference is the dissipative term. Routes F/H/I "
            "measured in 1D that NS sits EXACTLY at the critical exponent where every scaling "
            "argument returns zero information, and that criticality is a tar pit (mu decays "
            "algebraically, nine times per decade). Leg 46 built certification machinery. "
            "Nobody appears to have combined them."),
        "deliverable": (
            "The question is NOT 'does the scaling say the blow-up survives' -- Xu did that "
            "and pre-empted Route-F. It is: **switch dissipation on and ask whether the RADII "
            "POLYNOMIAL STILL CLOSES**, and walk mu up toward criticality watching the margin. "
            "**RUN IT IN FLOAT. That needs NO prerequisite** -- leg 46's machinery already "
            "produces Y_0, Z_1, Z_2 in float64 -- and it is decisive either way: (1) the "
            "certificate constants as a function of mu; (2) the margin's trajectory as "
            "mu -> mu_crit; (3) whether it degrades smoothly or falls off a cliff, and at "
            "which mu. **If the margin collapses the moment mu > 0, the Euler->NS question is "
            "answered in this toy for ONE leg of work, and it saves building interval "
            "arithmetic and a tail lemma for a target that was never going to survive them.**"),
        "premise_correction": (
            "An earlier version of this stage said 'on an object where the inviscid "
            "certificate is in hand'. **WE DO NOT HAVE ONE** -- leg 47 established that the "
            "inviscid certificate needs a tail lemma nobody here has written. That premise "
            "was wrong when written and is removed. The RIGOROUS form of V (does the "
            "CERTIFICATE survive) has L1 as an unstated prerequisite; the FLOAT form does "
            "not, which is why the float form is what this stage delivers."),
        "gate": {
            "question": ("FIRST: has anyone already done certification-under-dissipation for "
                         "a self-similar blow-up profile?"),
            "if_yes": ("Report it, fall back to stage C-PILOT, and do NOT spend the leg. "
                       "Leg 42 deleted seven of twelve novelty claims; this one is a "
                       "SPECULATION about novelty of exactly that kind and it gets checked "
                       "before it gets built, using Route-M's ledger machinery."),
            "if_no": ("Proceed to the deliverable. Report the margin trajectory whichever way "
                      "it goes -- a certificate that DIES at small mu is as informative as one "
                      "that survives, and is the more likely outcome."),
            "answer": (
                "**YES, leg 48 (Route-V v0).** Dahne-Figueras arXiv:2410.05480 verify whole "
                "BRANCHES of self-similar singular solutions of the complex Ginzburg-Landau "
                "equation, continued in the dissipation parameter eps from the conservative "
                "NLS limit, in interval arithmetic (their Thm 4.1 whole-branch in Case I, "
                "Thm 4.4 partial in Case II). arXiv:2404.04054 is a second, weaker precedent "
                "(certified self-similar profiles of parabolic PDEs incl. viscous Burgers, no "
                "dial). The gate's YES branch was taken: stage V is CLOSED and C-PILOT is "
                "next. solver/viscous_novelty.py re-derives their published zeros to 1.8e-07, "
                "their branch to 3.0e-06, and their fold to 3.8e-07 -- the pre-emption is "
                "verified, not cited. The margin does NOT die when dissipation is switched on "
                "(it improves 26x); it dies at a FOLD, with divergence exponent -1.061."),
        },
        "time_box": ("one leg for the novelty check, then one for the FLOAT measurement -- "
                     "and the novelty check comes first, always"),
        "sequel": (
            "V-RIGOROUS -- 'does the CERTIFICATE survive' rather than 'do the float constants "
            "survive' -- is downstream of L1 (interval arithmetic + a tail lemma), NOT a "
            "competitor to it. L1 is the first step of V-rigorous and a novel result in its "
            "own right, so the two are not in tension. Do not read the prerequisite as "
            "optional: without an inviscid certificate there is nothing for dissipation to "
            "perturb, and a float study cannot be upgraded into one after the fact."),
        "honesty": (
            "Even a complete success here is NOT Clay and is NOT a chain link. It is a "
            "statement about a toy model's certificate under dissipation. What makes it "
            "Clay-ADJACENT is that it probes the one structural difference between the "
            "proved case (Euler) and the open one (NS). Say that in every writeup."),
    },
    {
        "id": "C-PILOT",
        "name": ("Pilot: evolve the Lyapunov weight, on an object with a KNOWN answer "
                 "-- GATE ANSWERED NO, leg 49; the GA was NOT run"),
        "status": "DONE",
        "why_here": (
            "The narrowest member of the re-framing, and the right first bite: the fitness is "
            "ONE NUMBER (the worst-case coercivity constant of the linearized operator under "
            "a searched weight) and the constraint is checkable pointwise. Run where the "
            "answer is known so the fitness itself can be validated before it is trusted."),
        "deliverable": (
            "A searched weight beating the hand-picked one on a known-answer object, with the "
            "six-property viability gate re-run ON THE NEW FITNESS before any GA compute."),
        "gate": {
            "question": "Does the new fitness pass the six-property viability gate?",
            "if_yes": "Proceed to stage B with the validated fitness.",
            "if_no": ("STOP. Do not run the GA. Stage 3.5 is the precedent and it is "
                      "non-negotiable -- a fitness that fails the gate produces confident "
                      "garbage at scale."),
            "answer": (
                "**NO, leg 49 (Route-C-PILOT v0). 4 of 6 on the FROZEN predicate, and the "
                "NO branch was taken: no GA compute has touched this fitness.** P2 finite "
                "0.775 < 0.90 (nine of forty roster weights have Z_1 >= 1, so A is not an "
                "approximate inverse in that norm at any residual); P3 max|slope-1| = 0.092 "
                "> 0.05 against the known answer that Y_0 is linear in an injected defect "
                "-- and the probe's own window had to be diagnosed first (the linear regime "
                "starts at eps ~ 1/||A|| = 5.9e-07; median |slope-1| is 0.0018 inside it). "
                "The deterministic grid that property 6 needed anyway found a weight beating "
                "the naive one by 48,270x and leg 46's hand-tuned constant by 8.61x. TWO "
                "further findings re-price stage B: (i) leg 46's 5186x reproduces at 5604x "
                "but COLLAPSES TO 0.56x when c_l is pinned by a border row instead of coming "
                "out implicitly, so the weight is preconditioning the border rows and not "
                "choosing a function space; (ii) the analytic wall p* = 1 NEVER BINDS "
                "(removing it costs 1.5e-04 decades), while a MEASURED lower wall Z_1 = 1 "
                "climbs with refinement -- p_- = -3.68, -2.85, -1.64, -1.00 at n = 201, 401, "
                "801, 1601 -- until the admissible band is EMPTY at n = 3201. The "
                "certificate on this object closes only at the coarsest grid, and the reason "
                "is float conditioning, not the equation."),
        },
        "time_box": "one leg",
        "sequel": (
            "Stage B does NOT start on this fitness. Both repairs are engineering, not "
            "research, and neither is worth a leg on its own: carry the MEASURED lower wall "
            "in the box as the analytic one already is (P2), and state the fitness's "
            "defect-tracking accuracy as a resolution rather than assuming it exact (P3). "
            "The leg's third finding is the one that should set the order of work: the float "
            "rehearsal's Z_1 kills every weight at n ~ 3.2e3, which is the strongest "
            "quantitative case this project has produced for L1's interval arithmetic. Do L1 "
            "first."),
    },
    {
        "id": "L1",
        "name": ("Certify HL_S2_nonsymmetric FOR REAL: interval arithmetic + an analytic "
                 "far-field enclosure "
                 "[NOTE 2026-08-13, user ruling B1: this stage is marked DONE because the "
                 "STAGE RAN TO ITS GATE and the gate answered NO -- a completed stage, not a "
                 "successful one. That is NOT in conflict with the ban review's description "
                 "of L1 as dead in THREE REALIZATIONS; the two statements are about "
                 "different things, the stage's completion marker versus its realizations. "
                 "The [x] is deliberately UNCHANGED.]"),
        "status": "DONE",
        "outcome": (
            "GATE ANSWERED **NO** AT LEG 51, AND THE TERM THAT RAN OUT IS THE WEIGHT CLASS "
            "OF THE TAIL -- which is the branch the gate itself said to write up as the "
            "finding. The representation change worked: rebuilt in the compactified basis "
            "(solver/spectral_certificate.py) the operator gap VANISHES (H, dilation and "
            "velocity exact, checked in exact rational arithmetic) and Y_0 is EXACTLY ZERO "
            "in Fraction arithmetic, so the two open-ended gaps did collapse into one. That "
            "one has no bound: the tail operator's DIAGONAL IS EXACTLY ZERO (the unbounded "
            "part of the linearisation is the dilation SHIFT, not a multiplier), its kernel "
            "is the |X|^-1 far field (measured m^-2.007 vs predicted m^-2), and the tail "
            "inverse diverges in every class tried -- flat M^1.28, algebraic best M^0.64 at "
            "s=1, geometric x nu PER MODE. The window is EMPTY by 0.606 in exponent units: "
            "the object needs s < alpha = 0.394, the operator wants s ~ 1. Positive control: "
            "the same code with Lambda^1 dissipation saturates in every class, so the "
            "instrument can report 'bounded'. Next stage T carries the repair."),
        "progress": (
            "STEP ONE DONE (leg 50): solver/interval_certificate.py wires solver/interval.py "
            "through the bordered residual. The radii polynomial CLOSES IN INTERVAL "
            "ARITHMETIC at all three rungs -- rigorous Z_1 = 8.59e-09 / 5.71e-08 / 1.54e-07 "
            "at n = 201/401/801, all below 1; Y_0/budget = 2.282e-03 at n=201 where the naive "
            "evaluation path gives 1.479 and fails. **But the claim is only about the "
            "FINITE-DIMENSIONAL polynomial system with H, D, Uop taken as EXACT STORED DATA.** "
            "Two gaps remain between that and a theorem about the continuum profile, and "
            "BOTH are artifacts of the representation -- see deliverable."),
        "why_here": (
            "The ONLY movable link of the chain (L2 and L3 are occupied by Chen-Hou, L4 is "
            "out of reach by Wall 2), a novel result in its own right, and the object is "
            "uncertified (CHL April 2026, numerical only, no proof of any kind)."),
        "deliverable": (
            "**CHANGE THE REPRESENTATION; DO NOT PUSH THE CURRENT ONE.** The two remaining "
            "gaps -- (a) the truncation tail |X| > X_max, and (b) H/D/Uop being finite-"
            "difference approximations treated as exact data -- are BOTH consequences of "
            "certifying on a truncated finite-difference grid. Route-E's compactified basis "
            "(X = tan(theta/2), odd sines, solver/rescaled_spectrum.py) removes both by "
            "construction: its own docstring says three operators are exact on the WHOLE LINE "
            "with NO TRUNCATION AND NO QUADRATURE, and the velocity is exact too. Rebuild the "
            "bordered certificate there. (a) becomes a SPECTRAL TAIL BOUND on neglected "
            "Fourier coefficients -- the standard radii-polynomial move -- and (b) vanishes. "
            "**Expect the algebraic tail to bite:** Omega ~ |X|^-0.394 is non-smooth at "
            "theta = pi, so coefficients decay ALGEBRAICALLY (~k^-1.4) and geometric ell^1 "
            "weights fail. Two responses, in order: factor the tail out (Omega = "
            "(1+X^2)^(-p/2) Psi, so Psi is smooth and its coefficients decay geometrically), "
            "and if that is not enough, ALGEBRAIC weights -- which is exactly the one "
            "methodological claim Route-J's literature pass found NO hit for."),
        "gate": {
            "question": "Does the polynomial close in INTERVAL arithmetic, tail included?",
            "if_yes": ("That is a novel Tier-3 result on an object with no proof of any kind. "
                       "Report it as such, and only as such -- it is not Clay and not a step "
                       "toward it."),
            "if_no": ("STOP AND REPORT which term ran out of margin -- the interval widening, "
                      "the spectral tail, or the weight class. Do not harden. If it is the "
                      "WEIGHT CLASS, that is the methodological finding and it should be "
                      "written up as one rather than treated as a failure."),
        },
        "time_box": ("two legs: the basis rebuild, then the tail bound. The tail is "
                     "mathematics, not compute."),
    },
    {
        "id": "T",
        "name": ("The TAIL LEMMA: border the certificate with the far field the transport "
                 "operator cannot invert"),
        "status": "DONE",
        "outcome": (
            "GATE ANSWERED **YES** AT LEG 52. One border row and one border column bound the "
            "tail uniformly in M, in the classes where the target profile ALSO has finite "
            "norm: flat 7.46 -> 9.44 (M^0.100 against M^1.085 unbordered) and s = 0.3, "
            "8.09 -> 11.37 (M^0.147 against M^0.837). **The window leg 51 measured EMPTY by "
            "0.606 in exponent units is no longer empty**, so L1's NO was a statement about "
            "the STANDARD CONSTRUCTION and not about the object. "
            "WHAT MAKES IT A MEASUREMENT AND NOT A FIT: (i) the failing side was PREDICTED "
            "before the ladders ran, from the Fredholm structure alone -- kernel h_m ~ "
            "m^-2.0024 is in the space iff s < 1, cokernel u_m ~ m^+1.0012 is a bounded "
            "functional iff s >= 1, so bordering must help below s = 1 and not at or above "
            "it; measured, it saturates at s = 0 and 0.3 and keeps growing at s = 1 and 1.5. "
            "(ii) The ANALYTIC far-field mode -- the one a proof can write down -- achieves "
            "the SVD optimum to three digits in the admissible classes (1.000 / 1.007), and "
            "the alignment |cos| -> 1.00000; where the repair fails the alignment flatlines "
            "at 0.902 and the ratio degrades to 1.383, i.e. the two fail TOGETHER. (iii) Two "
            "negative controls diverge -- the second singular pair lands on 48.76, EXACTLY "
            "the unbordered value, so a wrong direction is asymptotically worth nothing. "
            "T-0 NOVELTY: PROCEED_NARROW. Breden-Desvillettes-Lessard arXiv:1503.06315 state "
            "the 'not asymptotically diagonally dominant' problem in nearly leg 51's words "
            "and give a construction for TRIDIAGONAL DOMINANT operators, so the general "
            "observation is NOT new and leg 51's methodological claim drops to a "
            "re-derivation. Whether their construction reaches a tridiagonal operator with "
            "ZERO diagonal and a kernel was NOT resolved (the PDF did not extract) and is "
            "recorded as an open question, not as a gap. "
            "CEILING (pre-committed as clause T6 before any number existed): a bounded "
            "bordered tail IS NOT A CERTIFICATE, and the object is still the a = 0 CLM "
            "linearisation -- one mode, analytic -- so this bounds the difficulty for "
            "HL_S2_nonsymmetric FROM BELOW, exactly as leg 51's failure did. Nothing is "
            "claimed about the target. No link of the chain moved."),
        "why_here": (
            "L1 answered its gate with a NO whose term is named, and the gate's own no-branch "
            "says the weight class IS the finding. But leg 51 also identified the obstruction "
            "precisely enough to attack it, which a 'the space is wrong' verdict on its own "
            "would not: the tail operator is not merely awkward, it is NOT INJECTIVE, and its "
            "kernel is one explicit mode per parity -- the |X|^-1 far field, h_m ~ m^-2. An "
            "operator that fails to be invertible by a finite-dimensional kernel is the "
            "classic case for BORDERING, which is the same move that made the finite block "
            "work in Route-PORT (three gauge freedoms -> three border rows). The repair is "
            "therefore named and cheap to test before anything is built on it."),
        "deliverable": (
            "T-0 FIRST, BEFORE ANY CONSTRUCTION: the novelty pass on the methodological claim "
            "leg 51 produced -- 'radii-polynomial / ell^1-Fourier certification needs the "
            "unbounded part of the operator to be a MULTIPLIER; inviscid self-similar "
            "transport makes it a SHIFT with zero diagonal'. Leg 51 states a checkable "
            "prediction about the shape of the field (the certified self-similar blow-ups "
            "using this machinery are DISSIPATIVE -- Dahne-Figueras CGL; the certified "
            "INVISCID ones -- Chen-Hou -- use weighted energy estimates instead). Check it. "
            "If it is known, say so and drop the claim to a re-derivation. "
            "T-1 THEN THE REPAIR, MEASURED BEFORE IT IS BUILT: add the far-field mode(s) as "
            "explicit unknowns and the transport's solvability functionals as border rows -- "
            "one per parity chain -- and measure ||T_tail^-1||_w on the BORDERED tail as a "
            "ladder in M, in the same three weight classes and through the same code path. "
            "solver/spectral_certificate.py already carries the tail block, the homogeneous "
            "mode and the dissipative positive control, so this is a one-function change and "
            "its answer is a magnitude."),
        "gate": {
            "question": ("Does bordering the tail with its own kernel give a tail inverse "
                         "that is BOUNDED uniformly in M, in a class where the target profile "
                         "also has finite norm (s < 0.394)?"),
            "if_yes": ("Then L1's no was a statement about the standard construction and not "
                       "about the object, and the certificate is worth rebuilding end to end "
                       "on HL_S2_nonsymmetric. Report the constant, and re-run the ceiling: "
                       "the borders are new unknowns and they need their own Y_0."),
            "if_no": ("Report which of the two sides failed -- the bordered inverse still "
                      "diverging (the kernel was not the whole obstruction) or the window "
                      "still empty (it was, but the class is). Then STOP building certificates "
                      "in ell^1-Fourier for this operator and say so in the plan: the finding "
                      "is then that the method and the object are mismatched, which is worth "
                      "more written down than worked around."),
        },
        "time_box": ("one leg. T-0 is a literature pass, T-1 is a measurement on machinery "
                     "that already exists. If T-1 needs a new solver, the plan was wrong."),
    },
    {
        "id": "TC",
        "name": ("ASSEMBLE the bordered certificate: give the far-field amplitude its own "
                 "column, its own Y_0, and a matching condition"),
        "status": "DONE",
        "outcome": (
            "GATE ANSWERED **NO** AT LEG 53. With the far-field amplitude carried as a real "
            "unknown through all four terms, the radii polynomial does NOT close on the a = 0 "
            "CLM object in any admissible class. "
            "THE TERM THAT RAN OUT IS Z_1, AND SPECIFICALLY ITS TWO BLOCK-COUPLING "
            "SUB-BLOCKS -- quantities that did not exist before this leg, because the finite "
            "block and the bordered tail had never been in the same object. With the "
            "block-diagonal approximate inverse the method requires, A = Gamma^-1 (+) A_tail: "
            "Z_1[tail<-Gamma] = 0.996 (flat) / 1.387 (s = 0.3) and Z_1[Gamma<-tail] = 59.0 / "
            "43.15 at K = 4, the BEST split in the whole sweep, growing like K/2 and K^2/2 "
            "respectively across K = 4..64, both admissible classes, both gauges. Smallest "
            "Z_1 lower bound anywhere: 43.15. The assembled Z_1 is 44.54 at its minimum. "
            "NOT THE TAIL TERM: leg 52's bordered tail constant appears as ||A_tail|| = "
            "2.19..10.32 and behaves. NOT Y_0: it is EXACTLY zero including the new matching "
            "row, and for the banned degenerate reason -- the anchor IS one basis mode, so it "
            "has no far field and the matching condition has nothing to fail. The polynomial "
            "therefore has the root r = 0 and NO POSITIVE INTERVAL (r_max = 0 in all ten "
            "rows); the counterfactual with leg 51's finite-block Z_1 alone does have one "
            "(r_max 2.14e-02 down to 4.64e-04), and the difference between those two columns "
            "IS the content of the leg. "
            "SCOPE, STATED EXACTLY: what is established is that the BLOCK-DIAGONAL "
            "approximate inverse the standard method requires cannot close this certificate "
            "-- Z_1[Gamma<-tail] equals 2||Gamma^-1|| to four digits in every row, so it is a "
            "statement about the finite block THIS leg built. What is NOT established is that "
            "no finite block can: the genuinely finite-block-independent sub-block is "
            "Z_1[tail<-Gamma], whose minimum over the whole sweep is 0.9961, BELOW 1. That is "
            "why stage MM is a real question and not a formality. "
            "THE MECHANISM, CORRECTED AFTER VERIFIER's REVIEW: ||Gamma^-1|| for the augmented "
            "block is EXACTLY 2(K^2 - 1) -- K^2, not K -- and dropping the amplitude column "
            "restores EXACTLY 4(K - 1). The K^2 is CREATED by the augmentation's weight "
            "pairing (amplitude column ~ ||hhat||_w ~ K/2 against a matching row of weight "
            "w_{K+1}, so the matching equation carries coefficient ~2/K). The coupling then "
            "contributes a factor 2, NOT K/2, and its dominant column is the RANK-ONE row-1 "
            "term rather than the (K+1)/2 sub-diagonal. TC-8 ablates five normalisations of "
            "the augmented block plus the un-augmented one; the smallest Z_1 lower bound over "
            "ALL of them is still one to two orders above 1, so the NO survives the "
            "renormalisation that the corrected mechanism invites. The underlying structural "
            "fact stands and is unchanged: the standard tail estimate needs the unbounded "
            "part to be a MULTIPLIER (cut of size Lambda_M against a tail inverse "
            "1/Lambda_M), and here it is OFF-DIAGONAL while the bordered tail inverse is a "
            "CONSTANT rather than a decaying multiplier -- which is why Z_1[tail<-Gamma] "
            "grows exactly x2 per doubling of K and reaches 38.2 by K = 64. Tuning s cannot "
            "touch it. "
            "TC-3, THE BORDER'S OWN DEFECT: the matching row's residual at the anchor is "
            "EXACTLY 0.0 (same degeneracy); the asymptotic expansion's truncation defect is "
            "6.15e-02 (flat) / 1.10e-01 (s = 0.3) falling like M^-1.00 / M^-0.78; and the "
            "GAUGE ROW's entry on the far-field column, sum_m m h_m, is LOG-DIVERGENT "
            "(3347 -> 7222 over M-K = 256..2048, +1865 per e-fold) because the dilation gauge "
            "sum_k k b_k has dual norm max_k k/w_k, infinite for every s < 1. The far-field "
            "column has an entry that does not exist. Repair (not a tuning of s): pin the "
            "exact dilation zero mode instead, which is EXACTLY e_2 (||L e_2||_inf = 0.0, "
            "checked) -- worth 1.5x to 8.7x, and the gate still answers NO. "
            "CONTROLS: the positive control (Lambda^1 dissipation, unbordered tail, no "
            "far-field unknown -- a dissipative tail has no kernel) drives the coupling like "
            "1/mu and brings the ASSEMBLED Z_1 to 0.9156 at mu = 2, so the instrument can "
            "report the other answer. Four border directions were tried; the analytic "
            "far-field mode is the best (9.441 against 13.37 second-pair and 19.65 random) "
            "and Z_1[Gamma<-tail] is 546.57 for ALL FOUR -- that block never sees the border, "
            "which is the sharpest form of the result: the coupling is not a property of the "
            "border. "
            "TC-0 NOVELTY: PROCEED_NARROW, six queries. THIS LEG FIRST REPORTED LEG 52's "
            "SEARCH-INDEX FLAG AS CLEARED; THAT CLEARANCE IS WITHDRAWN AND THE FLAG STANDS -- "
            "the query used prepended the literal arXiv ID, which tests retrieval by ID and "
            "not the topical recall the flag was raised against, and LIT's ninth pass re-ran "
            "leg 52's query VERBATIM and reproduced the null result. This leg's search log "
            "recorded counts, not links, so its claim could not be audited against its own "
            "record; a later pass should enumerate links. BDL arXiv:1503.06315: this leg read "
            "the abstract page only and left the question open; LIT's ninth pass settled it "
            "from the full PDF -- their assumptions (4)-(5) require a diagonal bounded away "
            "from zero, so the zero-diagonal Fredholm case is outside their construction. "
            "CEILING (pre-committed as clause TC7): nothing is claimed about "
            "HL_S2_nonsymmetric -- on the gate's own terms that run happens only if the "
            "polynomial closes here, and it did not. No link of the chain moved."),
        "why_here": (
            "This stage is written by T's own yes-branch, and it is the ONLY thing that "
            "converts leg 52 from a bounded term into a theorem. Leg 52 measured ONE term of "
            "four in isolation: the weighted l^1 norm of the inverse of the tail block PLUS "
            "one border row and one border column. In a certificate that border is not "
            "bookkeeping -- it is a NEW UNKNOWN, the far-field amplitude -- and an unknown "
            "that appears in the tail must also appear in the finite block, in the defect, "
            "and in a condition matching the spectral series to the asymptotic expansion. "
            "Until those three exist there is no radii polynomial, only three of its terms "
            "and a fourth measured under an assumption about the fourth. The stage is named "
            "now, before the assembly, so that 'the tail is bounded' cannot be quietly read "
            "as 'the certificate closes' in the interval between."),
        "deliverable": (
            "TC-1 THE AUGMENTED SYSTEM. Extend the bordered linearisation so the far-field "
            "amplitude is a genuine unknown: one extra column in the finite block (how the "
            "amplitude feeds back into modes 1..K), one extra row (the matching condition), "
            "and the tail block bordered as leg 52 measured it. solver/spectral_certificate.py "
            "carries the tail side (bordered_tail_inverse_norm, tail_right_null, "
            "tail_left_null); what is missing is the COUPLING, and that is where the work is. "
            "TC-2 THE FOUR TERMS AGAINST EACH OTHER, WHICH IS THE POINT. Leg 51 gave Y_0 = 0 "
            "exactly, Z_1 = 1.44e-10, Z_2 = 79.5 on the FINITE block alone; leg 52 gives a "
            "tail constant of 9.44 (flat) / 11.37 (s = 0.3). Those numbers have never been "
            "put in the same polynomial, and the tail constant is NOT small next to Z_2. "
            "Assemble them and report whether Z_2 r^2 - (1 - Z_1) r + Y_0 <= 0 has a root. "
            "TC-3 THE BORDER'S OWN DEFECT. The matching condition has a residual of its own; "
            "it enters Y_0 and it has never been computed. Report it as a magnitude, and if "
            "it dominates, say which term it dominates."),
        "gate": {
            "question": ("With the far-field amplitude carried as a real unknown through all "
                         "four terms, does the radii polynomial close -- on the a = 0 CLM "
                         "object, in a class with s < 0.394?"),
            "if_yes": ("Then the tail lemma exists as an assembled object rather than as a "
                       "measured term, and the next question is the ONLY one that matters: "
                       "re-run it on HL_S2_nonsymmetric, whose profile is not one basis mode "
                       "and whose coefficients decay ALGEBRAICALLY. Do not claim anything "
                       "about the target before that run. Report the margin, and report which "
                       "of the four terms is closest to spending it."),
            "if_no": ("Report WHICH TERM ran out, and do not repair it by tuning s -- lesson "
                      "88 is precisely that the parameter's optimum is not where the mechanism "
                      "lives. If it is the TAIL CONSTANT being too large next to Z_2, that is "
                      "a statement that bordering fixed the boundedness and not the size, and "
                      "it should be written up as one. If it is the MATCHING CONDITION's own "
                      "defect, the coupling is wrong and the stage was mis-specified."),
        },
        "time_box": ("one leg for the assembly, one for the four terms. If TC-1 needs a new "
                     "basis, stop -- leg 51 already chose the basis and leg 52 already "
                     "measured the tail in it."),
    },
    {
        "id": "MM",
        "name": ("THE MISMATCH: is a NON-block-diagonal approximate inverse a real lane, or "
                 "is this the lane's end? -- GATE ANSWERED NO, leg 54"),
        "status": "DONE",
        "why_here": (
            "This stage is written by T's OWN no-branch, promoted one level deeper by TC's "
            "measurement. T said: if the certificate does not close, 'STOP building "
            "certificates in ell^1-Fourier for this operator and say so in the plan -- the "
            "finding is then that the method and the object are mismatched, which is worth "
            "more written down than worked around.' TC then located the mismatch precisely, "
            "and it is NOT where L1 or T thought. It is not the weight class (leg 51), it is "
            "not the tail's invertibility (leg 52 fixed that), and it is not Y_0 or Z_2. It "
            "is the COUPLING between the two blocks of the approximate inverse -- and the "
            "method's block-diagonal A is exactly what makes that coupling a term at all. "
            "So there is exactly ONE remaining degree of freedom that is not a tuning, and "
            "the plan should either spend it or close the lane. Everything else -- s, the "
            "weight family, the split K -- is measured and banned: the coupling entry is K/2 "
            "for every s and every split."),
        "deliverable": (
            "MM-1 THE MISMATCH AS AN INEQUALITY, NOT A MOOD. State and check the lower bound "
            "Z_1 >= |1 - K/2| (w_{K+1}/w_K) ||A_tail e_{K+1}||_w / w_{K+1}, which holds for "
            "EVERY choice of finite block because that sub-block does not contain Gamma^-1; "
            "with leg 53's measured second factor (0.94..1.33 across the sweep) this is a "
            "statement that no block-diagonal A can work for this operator, and it should be "
            "written as one. "
            "MM-2 THE ONE MOVE THAT IS NOT A TUNING: an approximate inverse whose off-diagonal "
            "blocks are NOT zero -- one step of block Gauss-Seidel across the split, or the "
            "Schur complement of the coupling -- measured on the SAME assembled object of "
            "leg 53 (experiments/p2_route_tc_v1_assemble.py), with the same controls. Either "
            "it brings the assembled Z_1 below 1 or it does not, and both are reportable. "
            "MM-3 THE NOVELTY PASS FIRST. Leg 53 recorded as UNCHECKED whether the literature "
            "treats a radii-polynomial tail whose unbounded part is off-diagonal; six queries "
            "returned nothing addressing it. That is not evidence of a gap. Search it before "
            "constructing, and record the log. "
            "GATE ANSWERED NO, leg 54, VERIFIED TWICE. Best admissible Z_1 over EVERY shape "
            "(block Gauss-Seidel, Schur complement) x class x gauge x split, including K=2 and "
            "K=6 which the first draft's battery omitted (a verifier caught this): 8.9591 "
            "(ff_lift shape, algebraic s=0.3, K=2), against a block-diagonal baseline of "
            "10.4584 -- a 1.167x improvement where more than 8x was needed. MM-1's inequality "
            "verifies as an EXACT equality (max |ratio-1| = 1.89e-15), restricted to K>=6 flat "
            "/ K>=4 algebraic (its |1-K/2| prefactor vanishes at K=2, a gap a verifier caught "
            "before construction); every ODD split gives an exactly singular finite block in "
            "both classes and both gauges, closing the remaining small-K corner. A candidate "
            "shape-independent floor (MM-4, the tail operator's singularity on the bordered "
            "direction making A_12 drop out algebraically) was PROPOSED, then REFUTED by an "
            "explicit counter-construction (a rank-one A_11 choice drives the floor to ~1e-16, "
            "surviving only because the resulting total Z_1 is 5.7e+05) -- it is a floor for "
            "the shapes actually tested, not a universal one. Two self-flagged weaknesses "
            "(the border-direction control does not discriminate for the Schur shape; MM-4's "
            "identity holds only to an O(1/M)=1.46e-2 truncation defect) were independently "
            "confirmed to NOT change the gate's robustness. THIS FIRES THE GATE'S OWN NO-"
            "BRANCH below."),
        "gate": {
            "question": ("Does an approximate inverse that is NOT block diagonal bring the "
                         "ASSEMBLED Z_1 below 1, on the a = 0 CLM object, in a class with "
                         "s < 0.394?"),
            "if_yes": ("Then the method and the object are not mismatched after all, only the "
                       "standard SHAPE of A was -- report the assembled Y_0, Z_1, Z_2 and the "
                       "positive interval, then re-run on HL_S2_nonsymmetric, whose profile "
                       "is not one basis mode and decays algebraically. Claim nothing about "
                       "the target before that run, and re-state the ceiling: on the a = 0 "
                       "object Y_0 is exactly zero for a degenerate reason."),
            "if_no": ("STOP building ell^1-Fourier radii-polynomial certificates for inviscid "
                      "self-similar transport, and say so in the plan rather than working "
                      "around it. REPORT the mismatch as the result: the unbounded part of "
                      "this operator is a shift, the method's tail estimate needs a "
                      "multiplier, and the gap survives bordering, every admissible weight "
                      "class, every split and both gauges. DO NOT re-enter the lane by tuning "
                      "s, the weight family, the split, or the border direction -- all four "
                      "are measured and banned."),
        },
        "time_box": ("one leg. MM-3 is a literature pass; MM-1 is arithmetic on numbers that "
                     "already exist; MM-2 reuses leg 53's assembled object. If MM-2 needs a "
                     "new basis, a new object or a new solver, the plan was wrong -- the "
                     "whole point is that only the SHAPE of A is still free."),
    },
    {
        "id": "NG",
        "name": "THE NO-GO, STATED AS A THEOREM AND CHECKED AGAINST THE LITERATURE",
        "status": "DONE",
        "why_here": (
            "Seven legs (51-57) produced a coherent negative with every part a real result "
            "needs, and all of it is currently scattered across four PR bodies and a notes "
            "file: a named mechanism (the unbounded part is off-diagonal and the bordered "
            "tail inverse is a constant, not a decaying multiplier); an inequality that "
            "proves the block-diagonal case (MM-1); a battery over shapes, classes, gauges "
            "and splits bottoming at 8.9591; a POSITIVE CONTROL that reports the other answer "
            "(Z_1 = 0.9156 at mu = 2), which makes the hypothesis NECESSARY rather than "
            "merely sufficient; and a literature classification saying the case is "
            "unpublished. Escalation #1 (a route entering the committed sequence), entered "
            "under the user's pre-delegation ('whichever pursues our goals best') on "
            "2026-08-05 after MM's gate answered NO and stage B was found pre-refuted (leg "
            "52 measured the space, leg 53 measured the split at K/2 for every choice, leg 54 "
            "measured the shape of A -- all three of B's degrees of freedom are dead for this "
            "operator before its still-banned GA would ever run). A fresh target round was "
            "considered and rejected as premature: leg 55 already showed the object was never "
            "the problem, so what needs writing down first is the SCREEN (multiplier vs "
            "off-diagonal shift) that a target round should run through, not a new target "
            "picked blind."),
        "deliverable": (
            "NG-0 THE NOVELTY PASS FIRST, and it must resolve Cadiot arXiv:2505.03091's scope "
            "against THIS no-go specifically, not just against leg 51's earlier claim -- "
            "links, not counts. "
            "NG-1 THE PROPOSITION: hypotheses (operator class, weight classes, admissible A), "
            "conclusion, and a scope line separating measured from proved. "
            "NG-2 THE GAP: extend MM-1 beyond block-diagonal A, or state the restriction "
            "honestly -- leg 54 measured a battery, MM-1 proves only the block-diagonal case, "
            "and 'no A we tried' is not 'no A'. "
            "NG-3 SHARPNESS: the mu = 2 control as the statement that the hypothesis cannot "
            "be dropped."),
        "gate": {
            "question": ("Does the no-go admit a PROOF for a named class of approximate "
                         "inverses strictly larger than block-diagonal, with hypotheses that "
                         "provably contain the a = 0 CLM linearization?"),
            "if_yes": ("The repository has a Tier-3-shaped negative theorem; write it as a "
                       "standalone claim with its sharpness control, and escalate publication "
                       "scoping to the user."),
            "if_no": ("REPORT the result as a MEASUREMENT OVER A BATTERY, not a theorem. Cap "
                      "the claim at 'measured, not proved' everywhere it appears, and DO NOT "
                      "claim more; the next stage is the target round (leg 63, Route-M2) with "
                      "the multiplier/shift screen as its selection predicate."),
        },
        "time_box": ("one leg. NG-0 is a literature pass on one paper; NG-1 is writing down "
                     "what seven legs already measured; NG-3 reuses leg 54's control. NG-2 is "
                     "the only open mathematics, and if it needs a new object, a new solver, "
                     "or new machinery, the honest answer is the no-branch, not a new stage."),
    },
    {
        "id": "B",
        "name": "Evolve the CERTIFICATE -- the function space, the operator split, the constants",
        "status": "DONE",
        "done": (
            "leg 126, 2026-08-05. GATE: NO. Route-BX audited stage B's full declared search "
            "space (space x split x constants/shape, plus the fitness route) against the "
            "banked refutations: 1,686 of 1,686 enumerated configurations covered (144 by "
            "theorem, 1,032 structurally, 510 by measurement), zero uncovered. Even a "
            "perfect search over the residual headroom lands at Z1 >= 6.0424, 6.04x short. "
            "The committed sequence was EXHAUSTED with no successor for many cycles -- "
            "parked as escalation #1, RESOLVED 2026-08-06 by the user's ruling that "
            "supersedes the goal itself (see the module docstring's SUPERSEDING RULING). "
            "Stage P0 below is the resolution, not a continuation of B's own search."),
        "why_here": (
            "The bottleneck since Route-D has not been finding the object; it has been closing "
            "a certificate around an object we already have. Route-D hand-tuned a function "
            "space for ELEVEN legs and it turned out a=0-only. Routes K and L hand-picked "
            "preconditioners. Those are search problems with a fitness that CANNOT LIE -- "
            "'does the radii polynomial close, and by how much' is a theorem, not a plot, and "
            "an under-resolved run cannot fake it."),
        "deliverable": (
            "A searched certificate closing on the object stage M named, or an honest report "
            "that it does not and where the margin runs out."),
        "gate": {
            "question": "Does the searched certificate beat the hand-tuned one?",
            "if_yes": "Report the margin, and say plainly that the search found it, not us.",
            "if_no": ("Report that too. A negative bounds how much of the difficulty was "
                      "tuning versus structure, which is worth knowing either way."),
        },
        "time_box": "unscoped until C-PILOT reports",
    },
    {
        "id": "P0",
        "name": "Target selection under the CLAY goal -- object, ansatz, what a certificate "
                "would even mean",
        "status": "NEXT",
        "why_here": (
            "The user's 2026-08-06 ruling resolves escalation #1 by changing the goal itself: "
            "pursue a full Clay solve, not a novel Tier-3 result. Stage B's own exhaustion "
            "does not carry over as a dead end for THIS goal -- B searched certificates for "
            "an object already named under the OLD goal (HL_S2_nonsymmetric); P0 re-does "
            "target selection (Route-M's own discipline) against a DIFFERENT screen. "
            "Necas-Ruzicka-Sverak and Tsai exclude nontrivial exactly-backward-self-similar "
            "3D NS blow-up under the relevant decay, so any candidate must be discretely "
            "self-similar, unstable-self-similar with a finite unstable spectrum, or "
            "non-self-similar. arXiv:2604.09949 is the recorded negative-control citation: "
            "what happens when this constraint is missed."),
        "deliverable": (
            "A named target object + ansatz class, with an explicit statement of what a "
            "certificate for it would need to show, checked against the NRS/Tsai exclusion "
            "and against every already-banked dead end this repository's own record "
            "contains (L1's death in three realizations: legs 54/56/163/176/182; stage B's "
            "own exhaustion, leg 126; the space-axis synthesis, legs 179/186)."),
        "gate": {
            "question": ("Does a target+ansatz combination survive the NRS/Tsai screen AND "
                         "avoid every already-measured dead end this repository's own record "
                         "contains?"),
            "if_yes": ("Proceed to Phase 1 (the viscous rung) using this leg's named object. "
                       "State explicitly whether it is fluid/vortex-dynamics-adjacent, "
                       "bearing directly on Phase 1's own scope."),
            "if_no": ("Report precisely which screen killed every candidate tried (NRS/Tsai, "
                      "or the already-banked-dead-end check). This means target selection "
                      "itself needs more candidates or a different screen before Phase 1 can "
                      "even be posed -- report honestly, do not force a candidate through."),
        },
        "time_box": ("one leg (Phase 0). Phase 1 (the viscous rung) and Phase 2 (the 3D "
                     "solver, PLAN.md Stage 4) are sequenced strictly after -- per this "
                     "repository's own Route-A discipline, two unknowns are never debugged "
                     "simultaneously. Phase 2 is user-authorized but unscheduled until "
                     "Phase 1 reports."),
    },
]

# --------------------------------------------------------------------------
# what is banned, and what lifts each ban
# --------------------------------------------------------------------------
# Every ban names the stage that lifts it.  A ban with no lifting condition is how a plan
# becomes a superstition.
BANNED = [
    ("another gCLM measurement leg", "never -- the model is exhausted (Stage 3.5, leg 42)"),
    ("another Route-D bound-sharpening leg", "B"),
    ("another DSS CHEAP-ENTRANCE re-ask -- any attempt to obtain a DSS orbit by BIFURCATION "
     "OFF A FIXED POINT of a rescaled flow (Hopf or otherwise), inviscid or viscous",
     "never -- three independent reasons, each a measured spectral statement at the fixed point "
     "of the gCLM rescaled flow in the compactified odd-sine basis (gauge c_omega = 1 + (a-1) "
     "H(Omega)(0)), carried at a=0 (closed form) and a=1/2 (alpha=3 exactly) because the free "
     "error bar is 0.35 at a=0.2 vs 8.9e-5 at a=1/2: (1) Route-E cd43893 / PHASE2_P2_NOTES §26 "
     "-- the log-periodic directions are CONTINUOUS spectrum, the only grid-converged isolated "
     "eigenvalues are the two exact symmetry modes 0 and -1, planted positive control +1.083 "
     "(V=6) / +4.578 (V=12); a continuum has no eigenvalue to move. (2) Route-H 9dba93f / §29 "
     "-- dissipation DOES discretize that continuum (converged eigenvalues 2 -> 8, condensing "
     "on the negative integers) and every member still lands on the negative real axis, max Re "
     "= 3e-13, nothing goes complex; positive control 6 -> 9 with one at Re = +1.58. (3) "
     "Route-I 35929a4 / §30 -- inviscidly the log-periodic band IS the unstable set (141/144 "
     "unstable directions at K=144, leading +4.5455+430.35i, Re rising with |Im|) and any mu>0 "
     "DELETES it rather than damping it: max Re = -1e-13 at mu=0.05"),
    ("the DSS lane's EXPENSIVE entrance -- a GLOBAL periodic-orbit search of a rescaled flow "
     "with no fixed point nearby to seed it (TECHNICAL_P2_ROUTEG_V1.md:59, "
     "TECHNICAL_P2_ROUTEE_V1.md:416). SPLIT OUT AND RE-POSED 2026-08-07 (leg 254, user-"
     "approved): it was excluded by PRICE, not by measurement. All three reasons above are "
     "local-linear statements at a fixed point; 0 of 3 concern a global search. Route-E's own "
     "sec 6.4 states the opposite of an exclusion -- 'periodic orbits can exist without a "
     "fixed point nearby that spawned them' -- and Route-G's gate-check (b) rejected this "
     "entrance in a literal cost comparison ('this is much cheaper'). It has never been "
     "built, run, or costed with a number (repo-wide grep: 0 periodic-orbit searches of a "
     "rescaled flow), and 12 of 12 post-ban legs mentioning DSS are ban-walk non-contact "
     "lines that never inspect it. SCOPED BY USER RULING 2026-08-11 (scope, NOT a lift; the "
     "ban stands in full and its lift condition below is unchanged): the ban's object, in its "
     "own text above, is a search with NO FIXED POINT NEARBY TO SEED IT. A SEEDED search -- "
     "one initialised from a named, published orbit or an equivalently specified starting "
     "point -- is outside the ban, and route 4 is such a search. Any leg claiming this scope "
     "MUST NAME ITS SEED in its own pre-registration: source, identifier, and why it is not a "
     "cheap-entrance construction (the cheap-entrance ban above is untouched and still binds "
     "seed selection, as leg 342 applied it to triple-disqualify Kwon-Tsai arXiv:2011.02800 "
     "for bifurcating off Landau solutions). ABSENT A NAMED SEED, THIS BAN APPLIES IN FULL. "
     "The UNSEEDED global trawl remains banned on MEASUREMENT, not price: leg 260's kill is "
     "of the unseeded variant by its own defining adjective ('Entry B's defining adjective "
     "UNSEEDED is incompatible with its object's only function space') and is untouched. Two "
     "reasons this is a scope ruling and not a lift: lifting would also release the unseeded "
     "trawl leg 260 genuinely killed; and clause (a) below can no longer be met on leg 260's "
     "own answer, because the algebraically weighted space it gave is the space leg 341 later "
     "measured dead in three lanes",
     "never -- unless a scoping leg answers all three of: (a) the FUNCTION SPACE the search "
     "runs in, carrying sec 26 sec 4.1's recorded difficulty -- the orbit's building blocks "
     "are of LIMITED REGULARITY at the origin (X^{1-iy}, fractional power at X=0) and in the "
     "VISCOUS gCLM problem that band is absent entirely (max Re = -1e-13 at mu=0.05); (b) the "
     "OBJECT, since all three reasons hold only in gCLM -- Route-E: 'Nothing about NS. "
     "gCLM's scaling structure is not NS's' -- while Phase 0's target is NS; and (c) a PRICE "
     "in leg-hours against Phase 1's viscous rung. Under the Clay goal, expense alone neither "
     "holds nor lifts a ban"),
    ("re-measuring beta on the 2D object", "never -- leg 43 showed the object does not converge"),
    ("re-testing the scaling gauge as the near-null direction",
     "never -- leg 44 L-7 refuted it"),
    ("the PORT itself", "M"),
    ("any GA compute on an unvalidated fitness -- C-PILOT's gate ANSWERED NO at leg 49 "
     "(4/6), so this ban did NOT lift when the stage closed",
     "never -- only a re-run of the six-property gate that PASSES on a repaired fitness AT "
     "THE PINNED FROZEN RESOLUTION n = 201 coarse / 401 fine (wall_model '2d', seed 0, "
     "per_gene 9, refine 4 -- leg 59's configuration, the one legs 49 and 59 were scored at), "
     "or at a strictly FINER grid; a pass at any COARSER grid does NOT lift this ban. Leg 160 "
     "measured why: the unmodified, unrepaired leg-49 fitness passes 6/6 at n = 101/151 "
     "(P3 = 0.02007528568401651, P2 = 1.0000) while failing 5/6 at 201/401, because "
     "coarsening drops the residual floor ||rho||_inf from 4.79e-11 to 4.64e-13, below the "
     "frozen eps grid's 1e-11 bottom -- P3 stops failing because the probe stops measuring, "
     "with nothing repaired. Leg 160 reported that and refused to use it; its gate stays NO"),
    ("reading the float rehearsal's closure as resolution-independent -- leg 49 measured "
     "the certificate on the CLM object closing ONLY at n=201 and the admissible weight "
     "band going EMPTY at n=3201, because Z_1 is float conditioning", "L1"),
    ("repeating 'closure is a property of the SPACE' as an explanation -- leg 49's gauge "
     "ablation put the 5604x in the BORDER ROWS: pin c_l and it collapses to 0.56x",
     "never -- the observation stands, the explanation does not"),
    ("another literature leg beyond M's three questions", "M"),
    ("re-opening stage V as posed -- the novelty gate answered YES on 2026-08-04 "
     "(arXiv:2410.05480 verifies CGL branches in the dissipation parameter, in interval "
     "arithmetic), and leg 48 re-derived their zeros, branch and fold to confirm it",
     "never -- unless the question is re-posed for a FLUID transport model. "
     "('which needs L1 first' STRUCK 2026-08-13, user ruling B1: the 2026-08-06 ban review "
     "retired that wording in the re-posed entry's own prose and never applied it to this "
     "field. The retirement is an editorial correction, not a new decision, and the ban's "
     "own justification -- the novelty gate of 2026-08-04 on arXiv:2410.05480, re-derived "
     "by leg 48 -- is untouched.)"),
    ("RE-POSED 2026-08-06 (ban review, user ruling 2): re-attempting the ell^1-Fourier/"
     "radii-polynomial machinery this repository has measured DEAD in three realizations "
     "(ell^1_w coefficient basis leg 54, collocation basis leg 56, origin-H^2 capped at "
     "a=0 with no transfer to the real target legs 163/176), on ANY model, fluid or "
     "otherwise -- this retires the prior 'needs L1 first' wording, which the ban review "
     "found had become an impossible precondition (L1 has three independent dead "
     "attempts and no fourth candidate) rather than a live lift path. "
     "SCOPED 2026-08-13 by user ruling C1 (writeup/escalations/"
     "RULING_BAN_WORDING_2026-08-13.md), on the leg 391 escalation packet. THIS BAN NAMES "
     "AN APPARATUS. A Zgliczynski-style Galerkin-plus-tail DYNAMICAL closure -- "
     "self-consistent a-priori bounds, in which a finite Galerkin block and a controlled "
     "tail close a DYNAMICAL invariance argument rather than a Newton-Kantorovich "
     "contraction in a function space -- IS A DIFFERENT APPARATUS AND IS OUTSIDE THE BAN'S "
     "OBJECT. THIS IS A SCOPE RULING, NOT A LIFT, AND NO MEASUREMENT IS SUPERSEDED BY IT "
     "(the sec 3h rule 1 test): the ban STANDS IN FULL for the machinery it names, the "
     "three dead realizations stay dead (ell^1_w leg 54, collocation leg 56, origin-H^2/"
     "Mellin legs 163/176), Theorem NGX stays true (Z_1 >= 1 for every bounded A, "
     "sigma_min(L_M) = c_s M^-(1-s) -> 0), and leg 341's three-lane death of the "
     "algebraically weighted space stays true. "
     "THE NAMING REQUIREMENT -- ANY UNIT CLAIMING THIS SCOPE MUST, IN ITS OWN "
     "PRE-REGISTRATION, BOTH (1) NAME ITS APPARATUS, the closure it uses, with a citation, "
     "AND (2) SHOW IT DOES NOT CONSTRUCT A SINGLE BOUNDED APPROXIMATE INVERSE UNIFORM IN M, "
     "which is the precise quantity NGX excludes and therefore the precise thing that puts "
     "a unit inside or outside this ban. ABSENT BOTH, THIS BAN APPLIES IN FULL. A unit that "
     "reaches for a Y_0/Z_0/Z_1/Z_2 contraction, IN ANY SPACE, is inside the ban whatever "
     "it calls itself. "
     "THE OBLIGATION THE RULING CREATES: C1 makes this ban NARROWER than the repository has "
     "been treating it, so work may have been declined, deferred or never proposed on a "
     "reading now ruled too wide. A sweep of the landed record is OWED (unit T5) -- this is "
     "an obligation of the ruling, not an optional follow-up, and it is the honest price of "
     "narrowing a ban",
     "never -- unless a namable FOURTH space/basis this repository has not yet tried is "
     "proposed, with its own scoping leg establishing it is not subject to the same "
     "three-realization death. "
     "NOTE 2026-08-13 (ruling C1): this clause names a FOURTH SPACE/BASIS. Lane T holds a "
     "fourth APPARATUS, which is not literally that -- under C1 the mismatch is MOOT for "
     "Lane T, which needs no lift because the ban does not reach its apparatus. THE CLAUSE "
     "IS NOT REPAIRED. It still names the wrong kind of object for any future candidate "
     "that IS a space. Recorded as a KNOWN LIVE DEFECT; not ruled, because nothing "
     "currently depends on it"),
    ("SUPERSEDED 2026-08-06 (ban review): reading V-rigorous's L1 prerequisite as optional "
     "-- a float study cannot be upgraded into a certificate after the fact. Retained for "
     "the record; the re-posed ban above is now the operative wording on this question.",
     "never -- superseded by the re-posed ban above, retained for history only"),
    ("closing the truncation gap by extending the domain", "never -- leg 47 measured the trend and it has the WRONG SIGN, +0.47 decades per unit rho"),
    ("sweeping another weight FAMILY without first bordering the tail -- leg 51 measured "
     "flat, algebraic (nine exponents) and geometric, and the divergence curve has no zero; "
     "the obstruction is the tail operator's kernel, not the shape of the weight", "T"),
    ("reading leg 52's BOUNDED bordered tail as a certificate, or as a statement about "
     "HL_S2_nonsymmetric -- it is ONE of four terms, measured in isolation on the a=0 CLM "
     "object, and the border it adds is an unknown with no column, no Y_0 and no matching "
     "condition yet", "TC"),
    ("reading leg 53's assembled result as a statement about HL_S2_nonsymmetric, or as a "
     "statement that the TAIL term failed -- the object is still the a=0 CLM linearisation, "
     "Y_0 is exactly zero there for the banned degenerate reason, and the tail constant "
     "(2.19..10.32) is one of the terms that BEHAVED. What ran out is Z_1's block coupling",
     "never -- the ceiling was pre-committed as clause TC7, and the gate's yes-branch is the "
     "only route to the target"),
    ("repairing Z_1's block coupling by tuning s, the weight family, the split K, or the "
     "border direction -- all four are measured: the coupling entry is K/2 for EVERY s, the "
     "sweep K = 4..64 has its minimum at the smallest K and still gives 43.15, and "
     "Z_1[Gamma<-tail] is 546.57 for all four border directions because that sub-block never "
     "sees the border",
     "never -- lesson 88 again, and the mechanism is measured, not argued"),
    ("building any further ell^1-Fourier radii-polynomial machinery for this operator before "
     "MM's gate answers -- the one remaining free choice is the SHAPE of A, and MM spends it",
     "MM"),
    ("tuning the weight exponent s toward the minimum of leg 51's divergence curve -- that "
     "minimum (s = 1) is where the kernel leaves the space at the same moment the cokernel "
     "functional enters the dual, i.e. the ONE exponent at which bordering cannot help; "
     "leg 52 measured the repair working at s = 0 and 0.3 and failing at s = 1 and 1.5",
     "never -- lesson 88, and the mechanism is measured, not argued"),
    ("re-claiming leg 51's methodological finding at full strength -- RESOLVED at leg 57: "
     "Breden-Desvillettes-Lessard arXiv:1503.06315's assumptions (4)-(5) require a diagonal "
     "bounded away from zero (read from the full PDF, not the abstract), so BDL does NOT "
     "cover the zero-diagonal Fredholm case -- that BDL-shaped reason to keep this ban is "
     "discharged. A DIFFERENT, STRONGER reason replaces it: Cadiot arXiv:2505.03091 sec 2/3 "
     "independently states the same dominance-hypothesis observation, in full text, located "
     "and verified by a second independent pass (VER-D)",
     "never -- unless a pass resolves whether Cadiot's construction covers a zero diagonal, "
     "which is now the live open question, not BDL's. "
     "STATUS 2026-08-11, leg 304 (Route-CADX), gate YES(i), landed at b319449: the named "
     "pass HAS RUN and the open question IS RESOLVED -- Cadiot does NOT cover a zero "
     "diagonal, and the exclusion is BY HYPOTHESIS, not by accident: Assumption 1, p.6, "
     "'there exists l_min > 0 such that |l(xi)| >= l_min for all xi in R^m'; L is a Fourier "
     "multiplier by the class definition, so l IS the diagonal and a vanishing diagonal is "
     "exactly the excluded case l_min = 0. Load-bearing at 8 of 12 located clauses. A zero "
     "EIGENVALUE is covered; a zero DIAGONAL is not. "
     "THE BAN IS NOT LIFTED AND THIS ANNOTATION DOES NOT LIFT IT. The resolution CONFIRMS "
     "the stronger reason the ban rests on rather than discharging it, so lifting on it "
     "would be lifting a ban because its own justification was validated. But the lift "
     "clause is worded as 'unless a pass resolves whether', and a pass has now resolved it, "
     "so the clause's literal reading and its evident purpose now disagree. That is a "
     "wording question, not a judgement call an agent may make: ESCALATED TO THE USER "
     "2026-08-11. "
     "RULED A2 BY THE USER 2026-08-13 (writeup/escalations/"
     "RULING_BAN_WORDING_2026-08-13.md): THE BAN STANDS. The lift condition's pass HAS RUN "
     "(leg 304, Route-CADX, gate YES(i), landed b319449) and RESOLVED THE QUESTION AGAINST "
     "LIFTING -- Cadiot does not cover a zero diagonal, and the exclusion is BY HYPOTHESIS "
     "(Assumption 1, p.6). Lifting a ban because its own justification was validated "
     "inverts sec 3h rule 1. THE CLAUSE IS CLOSED, NOT OPEN. THE 2026-08-11 ESCALATION IS "
     "DISCHARGED. The ban stands in force, unchanged, and binds every leg"),
    ("reading leg 51's exactly-zero Y_0 as progress toward the target -- it is exactly zero "
     "because the a=0 CLM profile IS one basis mode; the non-symmetric Hou-Luo profile is "
     "not. NARROWED at leg 55 (measured, not asserted): the target DOES have finite ell^1_w "
     "norm at s=0 (margin +0.394) and s=0.3 (margin +0.094) -- the classes legs 51-53 "
     "actually used -- and diverges only at s=1, which is exactly the class the operator is "
     "least bad in (leg 51's own TECHNICAL sec 9: 'the class where the operator is least bad "
     "is the class where the target has infinite norm'). So the clause was never false, but "
     "its practical reading -- 'the target was never in the space' -- is NOT available as an "
     "explanation for legs 52-53's failures; leg 53's block-coupling finding (leg 54/MM: no "
     "shape of A closes it, best 1.167x where >8x was needed) stands as the operative reason",
     "never -- the ceiling was pre-committed as clause S7"),
    ("aiming the port at Chen-Hou's 2D profile as a TARGET -- it is certified "
     "(arXiv:2210.07191 + Part II); it stays only as C-PILOT's known-answer substrate",
     "never -- leg 45 M1"),
    ("chasing the 2D near-null direction of leg 44", "never -- the 2D object is no longer "
     "the target; if it is ever wanted again, the live hypothesis is the translation mode"),
    ("building a solver without grepping capabilities.py for the object first",
     "never -- leg 45 nearly rebuilt RescaledHLScenario2 from scratch"),
]

# --------------------------------------------------------------------------
# the standing refusal discipline, carried across every stage
# --------------------------------------------------------------------------
DISCIPLINE = [
    (58, "Report a MAGNITUDE, never a boolean, for anything you claim the absence of."),
    (66, "'Small' is meaningless until you say IN WHICH NORM, and the binding norm is set "
         "by the operator, not the coefficient vector."),
    (67, "Gate the quantity the measurement DIVIDES BY, not the quantity it is about."),
    (68, "A check that is not EXECUTABLE decays at the rate of memory."),
    (70, "A spectrum is not a property of an operator until you NAME THE REALIZATION."),
    (72, "Report the SHAPE of a convergence ladder, not its endpoint; pair it with a planted "
         "control so 'flat' has a yardstick."),
    (73, "When a quantity has no referent, SAY SO instead of bounding it."),
    (74, "Test all the suspects at once -- a battery costs about what the guesses cost."),
    (75, "Two defects in the same problem are not the same defect."),
    (76, "Keep the NEGATIVE construction in the artifact, or the next session re-tries it."),
    (84, "A known-answer probe has a WINDOW, and the window is part of the probe -- leg 49's "
         "slope-1 test was valid only for eps <~ 1/||A||, and outside it reported a property "
         "of the probe as a property of the fitness."),
    (85, "Re-measure your own headline before building a stage on it, and ablate the "
         "MECHANISM and not just the effect -- leg 46's 5186x replicated at 5604x and still "
         "had the wrong explanation attached to it for three legs."),
    (86, "A rigorous bound that is dominated by its own EVALUATION error is a statement "
         "about the code, not about the mathematics -- leg 50's near-miss at 1.48x was an "
         "enclosure 400x wider than the residual it enclosed."),
    (87, "A certification METHOD has a shape, and the shape is a property of the OPERATOR "
         "rather than of the object: before choosing one, ask whether the unbounded part of "
         "the linearisation is a MULTIPLIER or a SHIFT. Every ell^1-Fourier tail estimate "
         "assumes a diagonal; leg 51 measured that inviscid self-similar transport has none, "
         "on the friendliest object available, and that dissipation restores it instantly."),
]


def current():
    """The one stage that is NEXT."""
    nxt = [s for s in STAGES if s["status"] == "NEXT"]
    if len(nxt) != 1:
        raise RuntimeError(f"plan is ambiguous: {len(nxt)} stages marked NEXT")
    return nxt[0]


def banned_now():
    """Bans in force, given the current stage -- i.e. those whose lifting stage is not DONE."""
    done = {s["id"] for s in STAGES if s["status"] == "DONE"}
    return [(what, lifts) for what, lifts in BANNED if lifts not in done]


def status_report():
    s = current()
    lines = [
        "PLAN OF RECORD",
        f"  adopted   {ADOPTED} ({ADOPTED_BY})",
        f"  prize     {PRIZE}",
        f"  Clay      {CLAY_ODDS:.2%} -- behind Walls 1 and 2, unmoved by this plan",
        f"  posture   {POSTURE}",
        f"  mode      {MODE} (ORCHESTRATION.md 3g) -- blockers enumerated in {BLOCKERS_FILE}, READ IT WHOLE",
        "",
        "LANES (WALLS.md) -- every wave carries at least one unit attacking a wall on the Clay chain",
    ]
    for lane, walls, one_line in LANES:
        lines.append(f"  {lane}  [{walls}]  {one_line[:96]}...")
    lines += [
        "",
        "WHAT THE POSTURE DOES NOT LICENSE (ORCHESTRATION.md 3h)",
    ]
    for lim in POSTURE_LIMITS:
        lines.append(f"  - {lim[:120]}...")
    lines += [
        "",
        "SEQUENCE",
    ]
    for st in STAGES:
        mark = {"DONE": "[x]", "NEXT": "==>", "QUEUED": "[ ]"}[st["status"]]
        lines.append(f"  {mark} {st['id']:<8} {st['name']}")
    lines += ["", f"NEXT: {s['id']} -- {s['name']}",
              f"  deliverable: {s['deliverable'][:100]}...",
              f"  GATE: {s['gate']['question']}",
              f"    yes -> {s['gate']['if_yes'][:80]}...",
              f"    no  -> {s['gate']['if_no'][:80]}...",
              "", "BANNED RIGHT NOW"]
    for what, lifts in banned_now():
        lines.append(f"  - {what}   (lifted by: {lifts})")
    return "\n".join(lines)


if __name__ == "__main__":
    print(status_report())
