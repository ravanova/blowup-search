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
the OBJECT to closing the CERTIFICATE**, sequenced behind a target-selection leg.

**NOT adopted, and not claimed:** any route to Clay.  Walls 1 and 2 (`CLAY_ROADMAP.md` §2)
are untouched by all of this — a cheaper certificate does not make 3D Navier-Stokes reachable
by interval arithmetic, and if NS is globally smooth the whole programme is empty by
construction.  **Clay stays a ~0.05% horizon.**  The prize this plan is aimed at is a *novel
Tier-3 result on a model where blow-up is provable*, which is what §2 has said since
2026-07-23.
"""

ADOPTED = "2026-08-04"
ADOPTED_BY = "user decision, in session; supersedes the ranked-item habit"

PRIZE = ("A novel Tier-3 result on a model where blow-up is provable. "
         "NOT Clay -- see WALLS.")

WALLS = [
    ("Wall 1", "A search can only argue FOR blow-up, never for regularity. If 3D NS is "
               "globally smooth, this programme is empty by construction. Caps everything."),
    ("Wall 2", "Provable != where Clay lives. Validated/interval numerics reach 1D and 2D "
               "models; 3D NS is far out of reach. A cheaper certificate does not move this "
               "-- it is a dimensional wall, not a tuning wall."),
]

CLAY_ODDS = 0.0005

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
        "status": "NEXT",
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
        "id": "C-PILOT",
        "name": "Pilot: evolve the Lyapunov weight, on an object with a KNOWN answer",
        "status": "QUEUED",
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
        },
        "time_box": "one leg",
    },
    {
        "id": "B",
        "name": "Evolve the CERTIFICATE -- the function space, the operator split, the constants",
        "status": "QUEUED",
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
]

# --------------------------------------------------------------------------
# what is banned, and what lifts each ban
# --------------------------------------------------------------------------
# Every ban names the stage that lifts it.  A ban with no lifting condition is how a plan
# becomes a superstition.
BANNED = [
    ("another gCLM measurement leg", "never -- the model is exhausted (Stage 3.5, leg 42)"),
    ("another Route-D bound-sharpening leg", "B"),
    ("another DSS re-ask, or the DSS lane's expensive entrance",
     "never -- three independent reasons the cheap entrances fail"),
    ("re-measuring beta on the 2D object", "never -- leg 43 showed the object does not converge"),
    ("re-testing the scaling gauge as the near-null direction",
     "never -- leg 44 L-7 refuted it"),
    ("the PORT itself", "M"),
    ("any GA compute on an unvalidated fitness", "C-PILOT"),
    ("another literature leg beyond M's three questions", "M"),
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
