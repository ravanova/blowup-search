"""Route-W2L v1: is Wall 2 this repository's wall, or the field's wall?

The user asked, in substance, whether the claim in `CLAY_ROADMAP.md` and
`plan_of_record.py` -- that validated/interval numerics today reaches only 1D/2D models
and that 3D Navier-Stokes is out of reach -- is a property of THIS repository's chosen
approach or a property of the technology as a whole.

This repository's own EXT-family freshness legs (74, 77, 82, 90, 93, 123) never answered
that.  They asked the narrower question "has anyone certified THIS repository's target
object", which cannot see a computer-assisted 3D result in celestial mechanics,
combustion, chemotaxis, pattern formation, or compressible fluids.  Leg 172 asked the
broad question instead, and this driver is the auditable form of the answer.

IT IS NOT A SEARCH.  The search is leg 172's novelty pass, whose query strings, returned
links and verbatim primary-source quotations are committed at `writeup/novelty/leg_172.md`
BEFORE this file was written.  What this driver does is turn that pass into a structured
record that can be re-audited, and then MEASURE the gate against it rather than asserting
the gate's answer in prose:

  W1  THE SURVEY, AS A TABLE WITH A DECIDABLE FIELD.  Every surveyed work carries
      `certified_dims` -- the number of SPATIAL variables of the object the machine
      actually bounds -- alongside `statement_dims`, the number of spatial variables in
      the theorem's own statement.  The gate is then arithmetic, not rhetoric.

  W2  THE GATE, EVALUATED.  A record reaches the gate iff it is (a) a singularity/blow-up
      result, (b) time-dependent, (c) machine-certified, and (d) `certified_dims == 3`.
      Reported as the list of records passing each clause, so a future reader can see
      exactly which clause each near-miss fails.

  W3  THE LIFT GAP, MADE EXPLICIT.  For every record whose STATEMENT is 3D, report how the
      distance from `certified_dims` to 3 is bridged.  This is the leg's real finding: in
      every case it is bridged by ANALYSIS (a symmetry reduction, or an ODE profile plus a
      stability theorem), never by the certificate.

  W4  THE CONTROL THAT REPORTS A DIFFERENT ANSWER (lesson 90).  Re-run the same predicate
      with the singularity requirement dropped, i.e. "has validated numerics ever certified
      a genuinely 3D PDE object of ANY kind".  That returns YES (van den Berg-Williams,
      Ohta-Kawasaki in three dimensions, 2019).  Two different answers out of one code
      path -- which is what stops the NO from being an artifact of a predicate that could
      never have said YES.

  W5  THE FALSE-POSITIVE AUDIT.  Every record that ASSERTS a 3D machine-certified
      singularity must carry an explicit, quotable disqualifier.  Exactly one such record
      exists (arXiv:2604.09949) and it is disqualified twice over, independently.

  W6  THE SCOPE GUARD, ENFORCED IN CODE.  The leg's declared territory and the assertion
      that the Clay odds are unmoved under BOTH branches are written into the JSON, and
      the driver refuses to emit if the recorded odds differ from `plan_of_record.py`'s.

Deterministic, no network, no solver module, sub-second.  Writes
`writeup/data/p2_route_w2l_v1_lit.json`.

Run: .venv/bin/python -u experiments/p2_route_w2l_v1_lit.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "writeup" / "data" / "p2_route_w2l_v1_lit.json"

GATE = (
    "Does any published work -- in fluid dynamics, PDE theory, or any other "
    "computer-assisted-proof tradition -- establish a rigorous (interval-arithmetic, "
    "validated numerics, or otherwise machine-certified) singularity/blow-up result for a "
    "genuinely 3D PDE model (not an ODE, not a 1D/2D reduction)?"
)

# The odds this leg is forbidden to move, under either branch.  Cross-checked against
# plan_of_record.py at the end of the run rather than trusted.
CLAY_ODDS_PCT = 0.05


# ---------------------------------------------------------------------------
# W1 -- the survey
#
# `certified_dims`  number of SPATIAL variables of the object the machine bounds.
#                   0 = a finite-dimensional/parameter object (polynomial sign conditions,
#                   eigenvalue enclosures); an ODE profile in a single self-similar
#                   variable counts as 1.
# `statement_dims`  number of spatial variables in the theorem's own statement.
# `machine`         'interval'  = interval arithmetic / validated numerics in THIS paper
#                   'inherited' = no CAP of its own; imports a certified ingredient
#                   'none'      = analytic proof
#                   'claimed'   = asserts a CAP that this repository does not accept
# ---------------------------------------------------------------------------
SURVEY = [
    dict(
        key="chen_hou_boussinesq_euler",
        cite="J. Chen, T. Y. Hou, arXiv:2210.07191 (I: Analysis) + arXiv:2305.05660 "
             "(II: Rigorous Numerics), Multiscale Model. Simul., doi:10.1137/23M1580395; "
             "smooth-data 3D Euler statement also PNAS 2025, doi:10.1073/pnas.2500940122",
        tradition="fluid mechanics (incompressible)",
        object="2D Boussinesq approximate self-similar profile and the linearized "
               "operator around it, in the meridional half-plane",
        statement="finite time blowup of the 2D Boussinesq and 3D axisymmetric Euler "
                  "equations with smooth initial data of finite energy AND BOUNDARY",
        technique="weighted L-inf plus weighted C^{1/2} energy framework; rigorous "
                  "space-time solutions of the linearized problem with error control; "
                  "computer-assisted sharp velocity estimates in the regular case",
        singularity=True,
        time_dependent=True,
        machine="interval",
        certified_dims=2,
        statement_dims=3,
        lift="axisymmetric reduction: the 3D Euler unknowns depend on (r, z) only, and "
             "the 2D Boussinesq system is the exact correspondence away from the axis",
        hypotheses="smooth initial data of finite energy; a SOLID BOUNDARY; axisymmetry; "
                   "the Part I stability constants satisfying the stability lemma's "
                   "inequalities, verified numerically in Part II",
    ),
    dict(
        key="bcg_imploding",
        cite="T. Buckmaster, G. Cao-Labora, J. Gomez-Serrano, 'Smooth imploding solutions "
             "for 3D compressible fluids', arXiv:2208.09445, Forum of Mathematics Pi "
             "(January 2025); profiles also arXiv:2301.10101",
        tradition="fluid mechanics (compressible)",
        object="(i) Taylor coefficients of a solution of an ODE at a singular point, to "
               "order 10000, with rigorous error bounds; (ii) sign of degree-7-11 "
               "polynomials in 2 parameters, by branch and bound",
        statement="exact smooth self-similar imploding solutions to the 3D isentropic "
                  "compressible Euler equations for all gamma > 1, and asymptotically "
                  "self-similar imploding solutions to compressible Navier-Stokes at "
                  "gamma = 7/5",
        technique="interval arithmetic; Taylor expansion at a singular point of the "
                  "self-similar ODE; branch-and-bound polynomial sign validation",
        singularity=True,
        time_dependent=True,
        machine="interval",
        certified_dims=1,
        statement_dims=3,
        lift="SPHERICAL SYMMETRY, stated verbatim at the head of sec 1.5 ('Let us begin "
             "by rewriting (1.2) under spherical symmetry'), after which the system is a "
             "pair of equations in (R, t) alone; the self-similar profile is an ODE",
        hypotheses="isentropic ideal gas; spherical symmetry for the profile; gamma > 1 "
                   "for Euler, gamma = 7/5 with density-independent viscosity for "
                   "Navier-Stokes; smoothness of the constructed solution",
    ),
    dict(
        key="cgss_nonradial_implosion",
        cite="G. Cao-Labora, J. Gomez-Serrano, J. Shi, G. Staffilani, 'Non-radial "
             "implosion for compressible Euler and Navier-Stokes in T^3 and R^3', "
             "arXiv:2310.05325, accepted Cambridge J. Math.",
        tradition="fluid mechanics (compressible)",
        object="none of its own -- imports the certified self-similar profile of "
               "arXiv:2208.09445",
        statement="smooth, NON-RADIAL solutions of compressible Euler and Navier-Stokes "
                  "in T^3 and R^3 developing an imploding finite time singularity",
        technique="analytic stability/perturbation theory around the imported "
                  "spherically-symmetric self-similar profile; no interval arithmetic of "
                  "its own",
        singularity=True,
        time_dependent=True,
        machine="inherited",
        certified_dims=1,
        statement_dims=3,
        lift="PURE ANALYSIS on top of a 1D certified object -- this is the closest the "
             "literature comes to a genuinely 3D, genuinely non-symmetric certified "
             "singularity, and the certificate still sits at the bottom, on an ODE",
        hypotheses="periodic or non-radial smooth initial data; the imported profile's "
                   "hypotheses (hence gamma = 7/5 where the Navier-Stokes case is used)",
    ),
    dict(
        key="tucker_lorenz",
        cite="W. Tucker, 'A rigorous ODE solver and Smale's 14th problem', Found. Comput. "
             "Math. 2 (2002) 53-117; W. Tucker, 'Validated Numerics', Princeton (2011)",
        tradition="dynamical systems / celestial-mechanics lineage",
        object="the Lorenz vector field on R^3 -- three DEPENDENT variables, ZERO spatial "
               "variables",
        statement="the Lorenz attractor is a genuine strange attractor (Smale's 14th "
                  "problem)",
        technique="interval arithmetic; normal form near the origin; rigorous ODE "
                  "integration with a Poincare-section return map",
        singularity=False,
        time_dependent=True,
        machine="interval",
        certified_dims=0,
        statement_dims=0,
        lift="n/a -- the ancestor of the pattern, and the reason the gate says 'not an "
             "ODE': '3D' here names the phase space, not a spatial domain",
        hypotheses="the classical Lorenz parameter values",
    ),
    dict(
        key="vdb_williams_ohta_kawasaki_3d",
        cite="J. B. van den Berg, J. F. Williams, 'Rigorously computing symmetric "
             "stationary states of the Ohta-Kawasaki problem in three dimensions', "
             "SIAM J. Math. Anal. 51(1) (2019) 131-158",
        tradition="pattern formation / elliptic CAP",
        object="stationary states of the Ohta-Kawasaki PDE on a three-dimensional "
               "periodic cell -- THREE genuine spatial variables",
        statement="first existence proofs of the double gyroid and the body-centered "
                  "cubic packed sphere stationary states in three space dimensions",
        technique="Fourier-spectral Newton-Kantorovich with interval arithmetic, with "
                  "space-group symmetry imposed for 'an enormous reduction in "
                  "computational cost'",
        singularity=False,
        time_dependent=False,
        machine="interval",
        certified_dims=3,
        statement_dims=3,
        lift="n/a -- no lift needed; the certified object IS 3D",
        hypotheses="periodic cell; the imposed space-group symmetry class",
    ),
    dict(
        key="takayasu_lessard_jaquette_okamoto_heat",
        cite="A. Takayasu, J.-P. Lessard, J. Jaquette, H. Okamoto, 'Rigorous numerics for "
             "nonlinear heat equations in the complex plane of time', Numer. Math. 151 "
             "(2022) 693-750",
        tradition="parabolic PDE / blow-up",
        object="the 1D complex-time nonlinear heat equation",
        statement="rigorous local inclusions of solutions of the Cauchy problem for "
                  "complex time values, and blow-up structure in the complex time plane",
        technique="Chebyshev series in time, Fourier in space, Newton-Kantorovich with "
                  "interval arithmetic",
        singularity=True,
        time_dependent=True,
        machine="interval",
        certified_dims=1,
        statement_dims=1,
        lift="n/a -- 1D throughout; the closest the parabolic blow-up CAP tradition gets",
        hypotheses="periodic boundary conditions; analyticity in the complex time domain",
    ),
    dict(
        key="matsue_takayasu_compactification",
        cite="K. Matsue, A. Takayasu, 'Numerical validation of blow-up solutions with "
             "quasi-homogeneous compactifications', Numer. Math. 145 (2020) 605-654; and "
             "'Numerical validation of blow-up solutions of ordinary differential "
             "equations', J. Comput. Appl. Math.",
        tradition="blow-up validation (ODE)",
        object="finite-dimensional vector fields, compactified at infinity",
        statement="validated blow-up solutions and validated blow-up times for ODEs",
        technique="quasi-homogeneous compactification plus rigorous integration in "
                  "interval arithmetic",
        singularity=True,
        time_dependent=True,
        machine="interval",
        certified_dims=0,
        statement_dims=0,
        lift="n/a -- ODE by construction; the general-purpose blow-up CAP machinery, and "
             "it is finite-dimensional",
        hypotheses="quasi-homogeneity of the vector field's principal part",
    ),
    dict(
        key="vdb_breden_rigorous_integrator",
        cite="J. B. van den Berg, M. Breden, 'A simple rigorous integrator for semilinear "
             "parabolic PDEs', arXiv:2601.05146 (January 2026); cf. arXiv:2305.08221, "
             "arXiv:2402.00406",
        tradition="rigorous time integration of PDEs (the state of the art, 2026)",
        object="Swift-Hohenberg, Ohta-Kawasaki, Kuramoto-Sivashinsky -- demonstrated in "
               "one spatial dimension",
        statement="a posteriori rigorous and explicit error bounds between the numerical "
                  "and exact solutions, with adaptive time-stepping",
        technique="fixed-point reformulation around a piecewise-in-time constant "
                  "linearization; interval arithmetic",
        singularity=False,
        time_dependent=True,
        machine="interval",
        certified_dims=1,
        statement_dims=1,
        lift="n/a -- this is the frontier of rigorous FORWARD-IN-TIME integration, and it "
             "is demonstrated in 1D as of January 2026",
        hypotheses="semilinear parabolic; periodic boundary conditions",
    ),
    dict(
        key="keller_segel_3d_blowup",
        cite="e.g. arXiv:2501.07073 (nonradial stability of self-similar blowup, 3D "
             "Keller-Segel), arXiv:2502.19775, arXiv:2406.11358, "
             "doi:10.1007/s00220-025-05371-w (Keller-Segel-Navier-Stokes, 3D)",
        tradition="chemotaxis",
        object="n/a -- no machine certificate",
        statement="finite-time blowup and its stability for the 3D Keller-Segel system, "
                  "including non-radial finite-codimensional stability",
        technique="explicit self-similar solutions plus spectral and abstract semigroup "
                  "stability arguments -- ANALYTIC",
        singularity=True,
        time_dependent=True,
        machine="none",
        certified_dims=0,
        statement_dims=3,
        lift="n/a -- genuinely 3D blow-up IS proved here, but with no computer assistance "
             "at all, so it says nothing about the reach of validated numerics",
        hypotheses="the specific chemotaxis nonlinearity; the constructed profile",
    ),
    dict(
        key="shahmurov_5d_lift",
        cite="R. Shahmurov, 'Stable Finite-Time Singularity Formation for 3D "
             "Navier-Stokes via 5D-Lifted Axisymmetric Reductions', arXiv:2604.09949 v1 "
             "(2026-04-10)",
        tradition="fluid mechanics (claimed)",
        object="a self-similar profile in a 5D-lifted AXISYMMETRIC reduction",
        statement="stable finite-time singularity formation for 3D Navier-Stokes",
        technique="claimed computer-assisted Newton-Kantorovich validation in interval "
                  "arithmetic",
        singularity=True,
        time_dependent=True,
        machine="claimed",
        certified_dims=2,
        statement_dims=3,
        lift="an AXISYMMETRIC REDUCTION, by the paper's own title",
        hypotheses="axisymmetry in the 5D lift with measure dmu_5 = r^3 dr dz; the "
                   "reconstructed profile is exactly backward self-similar",
        disqualifiers=[
            "FAILS THE GATE ON ITS OWN TITLE: 'via 5D-Lifted Axisymmetric Reductions' is "
            "a symmetry reduction, so the certified object is not genuinely 3D even if "
            "every claim in the paper were correct.",
            "INDEPENDENTLY CLAIMED_UNUSABLE in this repository (legs 90, 93): no "
            "verification package released; the reconstructed exactly-backward "
            "self-similar solution is excluded by Necas-Ruzicka-Sverak; and the author "
            "has since posted six papers claiming the LOGICALLY OPPOSITE result in the "
            "same 5D lift, none of which cite it. Still v1, 0 revisions, 0 independent "
            "citations at 118 days (leg 93's four-channel measurement).",
        ],
    ),
    dict(
        key="deepmind_unstable_singularities",
        cite="'Discovery of Unstable Singularities', arXiv:2509.14185 (September 2025)",
        tradition="fluid mechanics (numerical discovery, not proof)",
        object="IPM (2D), Boussinesq (2D), Cordoba-Cordoba-Fontelos (1D)",
        statement="systematic discovery of families of UNSTABLE self-similar blowup "
                  "profiles to near machine precision, explicitly aimed at enabling "
                  "future computer-assisted proofs",
        technique="high-precision physics-informed neural networks with full-matrix "
                  "Gauss-Newton optimization -- NOT a proof, and no interval arithmetic",
        singularity=True,
        time_dependent=True,
        machine="none",
        certified_dims=0,
        statement_dims=2,
        lift="n/a -- the most prominent recent 'AI for singularities' result, and its "
             "objects are still 1D and 2D",
        hypotheses="self-similar ansatz with scaling exponent lambda; no rigorous bound",
    ),
]


def clause_report(rec):
    """Which of the gate's four clauses each record satisfies."""
    return dict(
        is_singularity=bool(rec["singularity"]),
        is_time_dependent=bool(rec["time_dependent"]),
        is_machine_certified=rec["machine"] in ("interval", "inherited"),
        certified_object_is_3d=rec["certified_dims"] >= 3,
    )


def main():
    print("=" * 78)
    print("ROUTE-W2L v1 -- has validated numerics ever certified a genuinely 3D PDE")
    print("                singularity, in ANY field?")
    print("=" * 78)
    print()
    print("GATE:", GATE)
    print()

    for rec in SURVEY:
        rec["clauses"] = clause_report(rec)
        rec["reaches_gate"] = all(rec["clauses"].values())

    # ---------------- W1 -------------------------------------------------
    print("-- W1  THE SURVEY " + "-" * 59)
    print(f"{'key':<34} {'trad':<10} {'cert':>4} {'stmt':>4}  {'machine':<10} gate")
    for rec in SURVEY:
        print(f"{rec['key']:<34} {rec['tradition'][:10]:<10} "
              f"{rec['certified_dims']:>4} {rec['statement_dims']:>4}  "
              f"{rec['machine']:<10} {'YES' if rec['reaches_gate'] else 'no'}")
    print()

    # ---------------- W2 -------------------------------------------------
    print("-- W2  THE GATE, EVALUATED " + "-" * 50)
    passing = [r for r in SURVEY if r["reaches_gate"]]
    gate_answer = "YES" if passing else "NO"
    for clause in ("is_singularity", "is_time_dependent",
                   "is_machine_certified", "certified_object_is_3d"):
        keys = [r["key"] for r in SURVEY if r["clauses"][clause]]
        print(f"  {clause:<24} satisfied by {len(keys)}: {', '.join(keys) or '(none)'}")
    print()
    print(f"  ALL FOUR CLAUSES: {len(passing)} record(s) -> GATE ANSWER: {gate_answer}")
    print()

    # The decisive intersection, stated as its own measurement.
    sing = [r for r in SURVEY
            if r["clauses"]["is_singularity"] and r["clauses"]["is_machine_certified"]]
    max_sing = max(r["certified_dims"] for r in sing)
    argmax_sing = [r["key"] for r in sing if r["certified_dims"] == max_sing]
    print(f"  Max certified_dims over MACHINE-CERTIFIED SINGULARITY results: {max_sing}"
          f"  ({', '.join(argmax_sing)})")

    # ---------------- W3 -------------------------------------------------
    print()
    print("-- W3  THE LIFT GAP " + "-" * 57)
    lifts = []
    for rec in SURVEY:
        if rec["statement_dims"] == 3 and rec["machine"] in ("interval", "inherited"):
            gap = 3 - rec["certified_dims"]
            lifts.append(dict(key=rec["key"], gap=gap, lift=rec["lift"]))
            print(f"  {rec['key']:<34} certified {rec['certified_dims']}D, "
                  f"stated 3D, GAP {gap}")
            print(f"       bridged by: {rec['lift']}")
    print()
    print("  Every gap above is bridged by ANALYSIS -- a symmetry reduction or an ODE")
    print("  profile plus a stability theorem -- and never by the certificate itself.")

    # ---------------- W4  the control ------------------------------------
    print()
    print("-- W4  CONTROL: drop the singularity requirement " + "-" * 28)
    ctrl = [r for r in SURVEY
            if r["clauses"]["is_machine_certified"] and r["clauses"]["certified_object_is_3d"]]
    ctrl_answer = "YES" if ctrl else "NO"
    print(f"  'has validated numerics ever certified a genuinely 3D PDE object at all?'")
    print(f"  -> {ctrl_answer}: {', '.join(r['key'] for r in ctrl) or '(none)'}")
    print()
    print("  TWO DIFFERENT ANSWERS OUT OF ONE CODE PATH (lesson 90).  The NO of W2 is not")
    print("  an artifact of a predicate that could never have said YES: relax exactly one")
    print("  clause -- 'singularity' -- and the same machinery returns YES.  So Wall 2 is")
    print("  about TIME-DEPENDENT SINGULARITY FORMATION, not about three spatial")
    print("  variables, and its naive wording ('validated numerics cannot do 3D') is")
    print("  WRONG and is corrected here.")

    # ---------------- W5  false-positive audit ---------------------------
    print()
    print("-- W5  FALSE-POSITIVE AUDIT " + "-" * 49)
    claimants = [r for r in SURVEY if r["machine"] == "claimed"]
    audit_ok = True
    for rec in claimants:
        ds = rec.get("disqualifiers", [])
        print(f"  {rec['key']}: {len(ds)} independent disqualifier(s)")
        for d in ds:
            print(f"     - {d}")
        if len(ds) < 2:
            audit_ok = False
    if not claimants:
        print("  (no record asserts a 3D machine-certified singularity)")
    print(f"  audit_ok (every claimant doubly disqualified): {audit_ok}")

    # ---------------- W6  scope guard ------------------------------------
    print()
    print("-- W6  SCOPE GUARD " + "-" * 58)
    import plan_of_record as por  # noqa: E402  -- read-only, never written by this leg
    por_src = Path(por.__file__).read_text()
    odds_consistent = f"{CLAY_ODDS_PCT}%" in por_src
    print(f"  plan_of_record.py still carries '{CLAY_ODDS_PCT}%': {odds_consistent}")
    print("  odds under YES branch: unchanged (scope guard, DIRECTION.md sec 172)")
    print("  odds under NO  branch: unchanged (scope guard, DIRECTION.md sec 172)")
    print("  chain links claimed by this leg: 0")
    if not odds_consistent:
        print("  REFUSING TO EMIT: recorded odds disagree with plan_of_record.py")
        return 1
    if not audit_ok:
        print("  REFUSING TO EMIT: a 3D-singularity claimant lacks two disqualifiers")
        return 1

    # ---------------- emit -----------------------------------------------
    payload = dict(
        route="W2L",
        leg=172,
        version=1,
        date="2026-08-06",
        kind="literature scoping, no computation on any model",
        gate=GATE,
        gate_answer=gate_answer,
        gate_answer_records=[r["key"] for r in passing],
        control_question="has validated numerics ever certified a genuinely 3D PDE "
                         "object of ANY kind (singularity requirement dropped)?",
        control_answer=ctrl_answer,
        control_records=[r["key"] for r in ctrl],
        max_certified_dims_among_machine_certified_singularities=max_sing,
        max_certified_dims_argmax=argmax_sing,
        lift_gaps=lifts,
        survey=SURVEY,
        wall2_sourced_form=(
            "No published work machine-certifies a singularity for an object with three "
            "spatial variables. Every 3D singularity theorem carrying a computer-assisted "
            "ingredient obtains its 3D-ness from a symmetry reduction or from an ODE "
            "profile plus analysis. This repository's 1D/2D scope IS the field's scope, "
            "not a self-imposed limit."
        ),
        wall2_naive_form_corrected=(
            "'Validated numerics cannot reach three spatial dimensions' is FALSE as "
            "stated -- van den Berg & Williams certified genuinely 3D Ohta-Kawasaki "
            "stationary states in 2019. The barrier is time-dependent singularity "
            "formation, not dimension."
        ),
        scope_guard=dict(
            clay_odds_pct=CLAY_ODDS_PCT,
            odds_moved_by_this_leg=False,
            odds_moved_under_yes_branch=False,
            odds_moved_under_no_branch=False,
            chain_links_claimed=0,
            plan_of_record_consistent=odds_consistent,
            files_this_leg_must_not_touch=[
                "solver/literature_gates.py", "plan_of_record.py", "CLAY_ROADMAP.md",
                "CONTINUATION_PROMPT.md", "PHASE2_P2_NOTES.md", "LITERATURE_CHECK.md",
                "experiments/JOURNAL.md",
            ],
            territory=[
                "experiments/p2_route_w2l_v1_lit.py",
                "writeup/data/p2_route_w2l_v1_lit.json",
                "writeup/novelty/leg_172.md",
                "experiments/journal/leg_172.md",
            ],
        ),
        provenance="Query strings, returned links and verbatim primary-source quotations "
                   "are in writeup/novelty/leg_172.md, committed BEFORE this driver was "
                   "written. This file records no search it did not first log there.",
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")
    print()
    print(f"wrote {OUT.relative_to(ROOT)}")
    print()
    print("=" * 78)
    print(f"GATE ANSWER: {gate_answer} -- Wall 2 is confirmed FIELD-WIDE, not an artifact")
    print("of this repository's narrower literature scope. Odds unchanged.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
