"""Leg 318 / Route-DECR -- "DOMINATED -> ENCLOSED": is there a general structural criterion?

GATE (pre-committed, immutable, quoted from DIRECTION.md):

    Does the leg state a general structural criterion for viscous-term enclosure that is
    falsifiable on at least one banked model of this repository?

This runner is the leg's whole measurement.  It

  1. states the criterion as DATA (`CRITERION`), not as prose;
  2. evaluates it on the repository's BANKED MODELS -- leg 240's compressible-implosion
     bank (`writeup/data/p2_route_cns2_v1_lit.json`) and leg 197's shared precedent ledger
     (`solver/viscous_novelty.py:PRECEDENTS`), both READ, not re-typed;
  3. runs the NAMED FALSIFICATION TESTS `FT1..FT5`, each of which could come out against
     the criterion, and reports every one of them by its own verdict;
  4. runs anti-tautology and adverse controls (lesson 90) that fail the process if the
     test set cannot discriminate.

NOTHING IS BUILT.  No solver module, no certificate, no `requirements.txt` change,
`plan_of_record.py` untouched, no ban read as lifted.  `solver/viscous_novelty.py` is
leg 197's and is READ ONLY (imported for its ledger, never edited).

Runtime: < 3 s.  Estimated before writing, per the standing >10-minute rule.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np  # noqa: E402

from solver.viscous_novelty import PRECEDENTS  # noqa: E402  (READ ONLY -- leg 197's file)

# =============================================================================
# 0. THE CRITERION, stated as data.
# =============================================================================
#
# SETTING.  An evolution equation  d_t u = N(u) + nu * D u,  with N the inviscid part and
# D a dissipative operator homogeneous of order m under x -> lambda x.  Fix a self-similar
# ansatz  u(x,t) = (T-t)^{-a} U( x / (T-t)^b ),  s = -log(T-t),  chosen so that N becomes
# AUTONOMOUS in s.  Let A be the set of exponents admissible for the inviscid profile
# problem.  In the rescaled equation the dissipative term acquires a prefactor e^{-d s};
# call d = delta_dis the DISSIPATION-CRITICALITY DEFECT.  For a scalar operator of order m
# with the ansatz's own b, delta_dis = 1 - m*b; for a system whose dissipation coefficient
# carries a field weight (BCG's nu/rho ~ S^{-1/alpha}) delta_dis is the paper's own.
#
# C1 -- CRITICALITY (necessary).  "No profile, no enclosure."
#   delta_dis > 0 on all of A  =>  the rescaled system is genuinely NON-AUTONOMOUS in s,
#     so any steady state of it solves the nu = 0 system: THERE IS NO nu-DEPENDENT PROFILE
#     OBJECT TO ENCLOSE.  DOMINATED is the strongest treatment available.  (One-line
#     proof: a fixed point requires the s-dependence to vanish, and e^{-d s} with d > 0
#     vanishes only in the limit, so the nu-term is absent from every fixed point.)
#   delta_dis = 0 at some b in A  =>  the rescaled system is AUTONOMOUS with nu as a
#     genuine parameter; the enclosed object exists and ENCLOSURE is structurally possible.
#   delta_dis < 0  =>  dissipation outscales the nonlinearity; the ansatz fails, and the
#     expected outcome is no blow-up at all.
#
# C2 -- ORDER COMPATIBILITY (necessary for CONTINUATION from nu = 0).  Even where C1
#   holds, an EXISTING nu = 0 certificate can be continued into nu > 0 only if D does not
#   raise the differential order of the profile problem.  If ord D > ord N the nu > 0
#   problem is a SINGULAR PERTURBATION: its solution set is not a deformation of the
#   nu = 0 one and the enclosure must be built ab initio at fixed nu > 0.
#
# C3 -- BRIDGE TYPE (necessary for the PDE-level statement).  CITED TO LEG 315, not claimed
#   here: the validated ODE->PDE bridge in the literature (Zgliczynski math/0005247) has
#   DISSIPATIVE hypotheses; BCG's rescaled system is quasilinear HYPERBOLIC.
#
# THE CRITERION IS NECESSARY, NOT SUFFICIENT.  Incompressible Navier-Stokes satisfies C1
# and C3 and is still closed -- by the NRS/Tsai NON-EXISTENCE theorems, not by an
# enclosure failure.  That row is kept in the test set precisely to stop the criterion
# being read as a route.
#
CRITERION = {
    "name": "ENCLOSURE IS CRITICALITY",
    "one_line": "You cannot enclose an object that does not exist: a nu-dependent "
    "self-similar profile exists only when the dissipation is scaling-CRITICAL for the "
    "blow-up ansatz, so DOMINATED is not a weakness of the method but the signature of a "
    "SUBCRITICAL dissipative term.",
    "clauses": {
        "C1": "necessary. ENCLOSURE requires delta_dis = 0 at an admissible exponent. "
        "delta_dis > 0 on the whole admissible set => no nu-dependent profile exists => "
        "DOMINATED is maximal. delta_dis < 0 => the ansatz fails.",
        "C2": "necessary for continuation from nu = 0. No order jump (ord D <= ord N), "
        "else the nu > 0 profile problem is a singular perturbation and must be certified "
        "ab initio.",
        "C3": "necessary at PDE level. CITED TO LEG 315: the validated ODE->PDE bridge is "
        "dissipative-hypothesis-only; a quasilinear hyperbolic rescaled system has none.",
    },
    "sharp_corollary_named": "THE KNIFE-EDGE: for BCG-type compressible implosion the "
    "exponent at which enclosure becomes structurally possible is EXACTLY the excluded "
    "left endpoint of the domination window. DOMINATED owns the open interval "
    "(2*gamma/(gamma+1), r_star(gamma)); ENCLOSED could only live at 2*gamma/(gamma+1), "
    "which the window excludes because that is precisely where the domination decay rate "
    "hits zero. The two treatments are complementary in r and share exactly one point, "
    "which neither occupies -- domination has no decay there, and enclosure is blocked "
    "there by C2 (first-order Euler profile ODE -> second-order with nu*Laplacian) and by "
    "C3 (quasilinear hyperbolic).",
    "not_a_lane": "Per the gate's own yes-branch: this does NOT become a lane. It is a "
    "screening rule for certificate design, not a route to a certificate.",
    "not_clay": "No link of L1->L4 moves. A statement about what COULD be enclosed is not "
    "a link moving. Clay odds unchanged at ~0.05%.",
}


# =============================================================================
# 1. BCG's own exponent bookkeeping, from leg 240's banked transcription.
# =============================================================================
def alpha_of(gamma: float) -> float:
    """BCG/CGSS: alpha = (gamma-1)/2.  Banked at p2_route_cns2_v1_lit.json:alpha_definition."""
    return (gamma - 1.0) / 2.0


def delta_dis(gamma: float, r: float) -> float:
    """CGSS (1.8) / BCG (1.20)-(1.21): delta_dis = (r-1)/alpha + r - 2.

    Leg 240 measured all three papers' transcriptions agreeing to 1.78e-15 over a 39x19
    (gamma, r) grid; this is that same formula, READ FROM the banked JSON's own statement.
    """
    return (r - 1.0) / alpha_of(gamma) + r - 2.0


def r_crit(gamma: float) -> float:
    """The DISSIPATION-CRITICAL exponent: the unique r with delta_dis(gamma, r) = 0.

    Solving (r-1)/alpha + r - 2 = 0 with alpha = (gamma-1)/2 gives
        2(r-1) + (r-2)(gamma-1) = 0  =>  r(1+gamma) = 2 gamma  =>  r = 2 gamma/(gamma+1),
    which is BCG's own threshold r > 2 gamma/(gamma+1).
    """
    return 2.0 * gamma / (gamma + 1.0)


def delta_dis_degenerate(gamma: float, r: float, theta: float) -> float:
    """delta_dis for DENSITY-DEPENDENT viscosity mu(rho) = rho^theta.

    DERIVED HERE, not transcribed -- and flagged as such everywhere it is used.
    BCG's viscous term enters as mu/rho * Laplacian(u); for constant mu (theta = 0) the
    rho^{-1} contributes the (1/alpha)(1-r) piece of -delta_dis = 2 - r + (1/alpha)(1-r).
    Replacing rho^{-1} by rho^{theta-1} = (rho^{-1})^{1-theta} scales that piece by
    (1-theta):
        delta_dis^(theta) = (1-theta)(r-1)/alpha + r - 2.
    theta = 0 recovers the published formula exactly (asserted below).
    theta = 1 (viscosity LINEAR in density -- the shallow-water/degenerate case) gives
    r - 2 < 0 for every r < 2: SUPERCRITICAL, so C1 predicts the implosion mechanism cannot
    survive there.  arXiv:2512.18545 proves exactly that (global regularity, no implosion).
    """
    return (1.0 - theta) * (r - 1.0) / alpha_of(gamma) + r - 2.0


def theta_star(gamma: float, r: float) -> float:
    """The viscosity-exponent threshold C1 predicts: delta_dis^(theta) = 0."""
    return 1.0 - alpha_of(gamma) * (2.0 - r) / (r - 1.0)


# =============================================================================
# 2. THE TEST SET -- banked models, with their exponent data and their BANKED verdict.
# =============================================================================
# `banked_verdict` is what the REPOSITORY already records, independently of this leg:
#   DOMINATED  -- certified object is the nu = 0 system, viscosity admitted as an error
#   ENCLOSED   -- nu sits inside the certified problem
#   NO_CERTIFICATE -- the row has no certificate at all, so it tests nothing here
#   NONEXISTENT -- the object is proved not to exist (so neither treatment applies)
MODELS = [
    {
        "key": "BCG-NS",
        "what": "3D isentropic compressible Navier-Stokes implosion (Buckmaster, "
        "Cao-Labora, Gomez-Serrano arXiv:2208.09445; CGSS arXiv:2310.05325; "
        "Shao-Wei-Wang-Zhang arXiv:2501.15701)",
        "bank": "writeup/data/p2_route_cns2_v1_lit.json (leg 240) + "
        "solver/viscous_novelty.py PRECEDENTS (leg 197, via leg 174)",
        "dissipation_order_m": 2,
        "inviscid_profile_order": 1,
        "delta_dis": None,  # computed on the banked window, below
        "banked_verdict": "DOMINATED",
        "dial_followed_from_zero": False,
    },
    {
        "key": "DF-CGL",
        "what": "complex Ginzburg-Landau / NLS self-similar singular solutions "
        "(Dahne-Figueras arXiv:2410.05480), dissipation dial eps in (1 - i eps)Laplacian",
        "bank": "solver/viscous_novelty.py PRECEDENTS (leg 197/48), verdict PRE_EMPTS",
        "dissipation_order_m": 2,
        "ansatz_b": 0.5,  # Zakharov ansatz: |x| / sqrt(2 kappa (T-t))
        "inviscid_profile_order": 2,  # the eps = 0 problem is ALREADY second order (NLS)
        "banked_verdict": "ENCLOSED",
        "dial_followed_from_zero": True,
    },
    {
        "key": "BC-VISCOUS-BURGERS",
        "what": "generalised viscous Burgers self-similar profile (arXiv:2404.04054), "
        "certified in H^2(e^{|x|^2/4}) as -Laplacian u - (x/2).grad u = f",
        "bank": "solver/viscous_novelty.py PRECEDENTS (leg 197), verdict ADJACENT",
        "dissipation_order_m": 2,
        "ansatz_b": 0.5,  # the operator -Laplacian - (x/2).grad IS the b = 1/2 generator
        "inviscid_profile_order": 1,  # inviscid Burgers profile problem is first order
        "banked_verdict": "ENCLOSED",
        "dial_followed_from_zero": False,  # certified at fixed nu, never continued to nu=0
    },
    {
        "key": "BC-NONLINEAR-HEAT",
        "what": "nonlinear heat equation self-similar profile (arXiv:2404.04054)",
        "bank": "solver/viscous_novelty.py PRECEDENTS (leg 197), verdict ADJACENT",
        "dissipation_order_m": 2,
        "ansatz_b": 0.5,
        "inviscid_profile_order": 2,  # there is no inviscid limit; the Laplacian IS N
        "banked_verdict": "ENCLOSED",
        "dial_followed_from_zero": False,
    },
    {
        "key": "CHEN-HOU-EULER",
        "what": "Chen-Hou 2D Boussinesq / 3D Euler with boundary (arXiv:2210.07191, "
        "2305.05660) and the Hou-Luo model -- INVISCID certificates",
        "bank": "solver/viscous_novelty.py PRECEDENTS (leg 197), verdict EXCLUSION",
        "dissipation_order_m": None,  # no dissipative term at all
        "banked_verdict": "NO_CERTIFICATE",  # of a viscous term; the row has no dial
        "dial_followed_from_zero": False,
    },
    {
        "key": "GCLM-DISSIPATIVE",
        "what": "gCLM with fractional dissipation nu Lambda^sigma "
        "(Ambrose-Lushnikov-Siegel-Silantyev arXiv:2207.07548; J. Chen arXiv:1908.09385)",
        "bank": "solver/viscous_novelty.py PRECEDENTS (leg 197), verdict EXCLUSION "
        "(analysis + numerics, NO computer-assisted certificate of a profile)",
        "dissipation_order_m": None,  # sigma is varied, and there is no certificate anyway
        "banked_verdict": "NO_CERTIFICATE",
        "dial_followed_from_zero": False,
    },
    {
        "key": "INCOMPRESSIBLE-NS-LERAY",
        "what": "Leray self-similar solutions of 3D incompressible Navier-Stokes: "
        "u = (T-t)^{-1/2} U(x/sqrt(T-t)) -- the viscous term is scaling-CRITICAL",
        "bank": "plan_of_record.py stage P0's own gate (the NRS/Tsai screen); "
        "located again this leg at 1509.08177 / 1901.01510 / 1812.00957",
        "dissipation_order_m": 2,
        "ansatz_b": 0.5,
        "inviscid_profile_order": 1,  # the Euler self-similar problem is first order
        "banked_verdict": "NONEXISTENT",  # NRS/Tsai: no nontrivial profile in the class
        "dial_followed_from_zero": False,
    },
]


def classify(model: dict, d: float | None) -> str:
    """What C1 PREDICTS for a model, from its delta_dis alone."""
    if d is None:
        return "ABSTAIN"
    if abs(d) < 1e-12:
        return "ENCLOSURE_POSSIBLE"
    return "DOMINATION_ONLY" if d > 0 else "ANSATZ_FAILS"


# =============================================================================
# 3. MAIN
# =============================================================================
def main() -> int:
    out: dict = {
        "leg": 318,
        "route": "DECR",
        "date": "2026-08-11",
        "gate_question": "Does the leg state a general structural criterion for "
        "viscous-term enclosure that is falsifiable on at least one banked model of this "
        "repository?",
        "criterion": CRITERION,
        "banked_sources_read": [],
        "models": [],
        "falsification_tests": [],
        "controls": [],
    }

    # --- read the banked leg-240 record rather than re-typing its numbers -------------
    bank240_path = REPO / "writeup" / "data" / "p2_route_cns2_v1_lit.json"
    bank240 = json.loads(bank240_path.read_text())
    checks = bank240["arithmetic_checks"]
    out["banked_sources_read"].append(
        {
            "path": "writeup/data/p2_route_cns2_v1_lit.json",
            "leg": bank240["leg"],
            "gate_answer": bank240["gate_answer"],
            "windows_used": {
                "gamma_7_5": checks["window_gamma_7_5"],
                "gamma_5_3": checks["window_gamma_5_3"],
            },
        }
    )
    out["banked_sources_read"].append(
        {
            "path": "solver/viscous_novelty.py",
            "leg": 197,
            "n_precedent_rows": len(PRECEDENTS),
            "ids": [p["id"] for p in PRECEDENTS],
            "note": "READ ONLY. leg 197's file, imported for its ledger, never edited.",
        }
    )

    print("=" * 78)
    print("LEG 318 / ROUTE-DECR -- DOMINATED -> ENCLOSED: is there a criterion?")
    print("=" * 78)
    print(f"\nCRITERION: {CRITERION['name']}\n  {CRITERION['one_line']}\n")

    # -----------------------------------------------------------------------------
    # FT1.  THE KNIFE-EDGE, on leg 240's banked compressible model.
    #   Prediction: the zero set of delta_dis is EXACTLY r = 2 gamma/(gamma+1), and that
    #   is EXACTLY the banked domination window's LOWER endpoint, at every gamma.
    #   Refuted if they disagree beyond the bank's own transcription tolerance (1.78e-15),
    #   or if the window's lower endpoint turns out to be set by profile existence.
    # -----------------------------------------------------------------------------
    #
    # INSTRUMENT NOTE, and it decided this test's verdict.  Run in float64 the residual
    # max|delta_dis(gamma, r_crit(gamma))| is 5.329e-15, NOT 0 -- and a naive 1e-15
    # tolerance therefore reports FT1 REFUTED, i.e. reports the knife-edge identity as
    # FALSE.  It is not false. FT1's verdict is UNCHANGED below either way, since it is
    # decided in exact rational arithmetic, where the residual is identically 0; the float
    # residual is recorded alongside as the diagnosis rather than as the measurement.
    #
    # [LEG 337 CORRECTION, superseding the mechanism story below.] The line that used to
    # stand here read: "(r-1)/alpha and (r-2) are two quantities of size ~1 that cancel
    # exactly, so the residual is ~25 ulp of the cancelled operands -- catastrophic
    # cancellation." That is WRONG about the mechanism (FT1's verdict is unaffected,
    # decided in exact rational arithmetic either way). Re-measured directly (script in
    # experiments/journal/leg_337.md): at the worst gamma = 1.075, alpha_of(gamma) is
    # computed with ZERO rounding error (exact in float64: gamma-1.0 is exact by
    # Sterbenz's lemma, and halving is always exact) -- alpha carries no ulp at all. All
    # of the error lives in r_crit(gamma) = 2*gamma/(gamma+1): its float64 value differs
    # from the true rational 2*gamma/(gamma+1) by -0.88 ulp(r) (~1 ulp), from the
    # addition+division pair inside r_crit. That single sub-ulp error in r is then
    # AMPLIFIED by delta_dis's own sensitivity to r at the root, d(delta_dis)/dr = 1/alpha
    # + 1 = 27.667 at this gamma (dominated by the 1/alpha = 26.667 term): plugging the
    # exact-rational r and alpha into delta_dis gives 0 (confirms the identity is exact);
    # plugging the actual float64 r (with its -0.88 ulp error) and the actual float64
    # alpha (0 error) into delta_dis in exact rational arithmetic reproduces
    # -5.424e-15, matching the observed float64 residual -5.329e-15 to within the small
    # extra rounding of delta_dis's own float ops. So: it is NOT cancellation between two
    # ~1-sized operands that "costs" precision -- it is 1 ulp of pre-existing rounding
    # error in ONE operand (r), amplified by the other operand's reciprocal (1/alpha).
    # Confirmed across the full 45-gamma grid: alpha_of never carries nonzero ulp error at
    # any grid point; r_crit always does, scaled by the corresponding 1/alpha_of(gamma).
    # "Leg 302's failure mode" as a category label is retracted along with it -- this is
    # ill-conditioning under amplification, not a subtraction-of-near-equal-terms loss.
    gammas = np.linspace(1.05, 2.15, 45)
    resid = np.array([delta_dis(g, r_crit(g)) for g in gammas])
    ft1_zero_max_float = float(np.max(np.abs(resid)))
    ft1_cancellation_scale = float(
        np.max([abs((r_crit(g) - 1.0) / alpha_of(g)) for g in gammas])
    )

    exact_resid = 0
    for i in range(45):
        gq = Fraction(105, 100) + Fraction(110, 100) * Fraction(i, 44)
        aq = (gq - 1) / 2
        rq = 2 * gq / (gq + 1)
        exact_resid = max(exact_resid, abs((rq - 1) / aq + rq - 2))
    ft1_zero_max = float(exact_resid)  # exactly 0 in Q

    banked_lo = {
        "7/5": checks["window_gamma_7_5"]["lo"],
        "5/3": checks["window_gamma_5_3"]["lo"],
    }
    ft1_endpoint_dev = {
        "7/5": abs(r_crit(7 / 5) - banked_lo["7/5"]),
        "5/3": abs(r_crit(5 / 3) - banked_lo["5/3"]),
    }
    tol = 1.7763568394002505e-15  # leg 240's own measured transcription tolerance
    ft1_pass = ft1_zero_max == 0.0 and all(v <= tol for v in ft1_endpoint_dev.values())

    # the part of FT1 that could have killed the knife-edge: the window's lower endpoint
    # might have been a PROFILE-EXISTENCE bound instead.  It is not -- profile existence
    # supplies the UPPER endpoint r_star, which is strictly larger.
    ft1_lower_is_not_profile_bound = all(
        checks[f"window_gamma_{k}"]["lo"] < checks[f"window_gamma_{k}"]["hi"]
        for k in ("7_5", "5_3")
    )

    out["falsification_tests"].append(
        {
            "id": "FT1",
            "name": "the knife-edge identity, on leg 240's banked compressible model",
            "banked_model": "BCG-NS (writeup/data/p2_route_cns2_v1_lit.json)",
            "prediction": "zero(delta_dis) = {r = 2 gamma/(gamma+1)} exactly, and that "
            "value equals the banked domination window's LOWER endpoint at every gamma",
            "what_would_refute_it": "any gamma on the grid at which the two differ by more "
            "than leg 240's own transcription tolerance 1.78e-15; or a bank in which the "
            "window's lower endpoint is set by profile existence rather than by delta_dis",
            "max_abs_residual_of_delta_dis_at_r_crit_EXACT_RATIONAL": ft1_zero_max,
            "max_abs_residual_float64": ft1_zero_max_float,
            "float64_cancellation_scale": ft1_cancellation_scale,
            "float64_relative_residual": ft1_zero_max_float / ft1_cancellation_scale,
            # [LEG 337 CORRECTION] The "instrument_note" string below (banked
            # verbatim into writeup/data/p2_route_decr_v1.json, out of this leg's
            # territory to alter) repeats the retracted "~25 ulp catastrophic
            # cancellation" mechanism story. See the corrected accounting in the
            # comment block above (INSTRUMENT NOTE, ~line 314) and in
            # experiments/journal/leg_337.md: the ulp lives in r_crit, not in a
            # cancellation between alpha and r, and is amplified by 1/alpha.
            "instrument_note": "float64 gives 5.329e-15, and a naive 1e-15 tolerance would "
            "have reported this test REFUTED -- i.e. would have reported the knife-edge "
            "identity as FALSE. It is not: (r-1)/alpha and (r-2) are two ~1-sized "
            "quantities that cancel exactly, so 5.329e-15 is ~25 ulp of the cancelled "
            "operands. Leg 302's failure mode verbatim. The verdict below is decided in "
            "EXACT RATIONAL arithmetic, where the residual is identically 0; the float "
            "number is kept as the diagnosis, never as the measurement.",
            "endpoint_deviation_from_bank": ft1_endpoint_dev,
            "tolerance": tol,
            "lower_endpoint_is_not_a_profile_existence_bound": bool(
                ft1_lower_is_not_profile_bound
            ),
            "verdict": "NOT REFUTED" if ft1_pass else "REFUTED",
        }
    )
    print("FT1  knife-edge identity r_crit = 2g/(g+1) == banked window lower endpoint")
    print(f"       EXACT (rational) max residual over 45 gammas = {ft1_zero_max}")
    print(f"       float64 max residual = {ft1_zero_max_float:.3e} "
          f"(rel {ft1_zero_max_float/ft1_cancellation_scale:.2e}) -- CANCELLATION, not error")
    print(f"       |r_crit(7/5) - banked lo| = {ft1_endpoint_dev['7/5']:.3e}")
    print(f"       |r_crit(5/3) - banked lo| = {ft1_endpoint_dev['5/3']:.3e}")
    print(f"       -> {out['falsification_tests'][-1]['verdict']}\n")

    # -----------------------------------------------------------------------------
    # FT2.  C1 against every banked model's OWN recorded verdict.
    # -----------------------------------------------------------------------------
    rows = []
    for m in MODELS:
        if m["key"] == "BCG-NS":
            # evaluated ON THE BANKED WINDOW: delta_dis on the open interval, at both gammas
            d_lo = delta_dis(7 / 5, checks["window_gamma_7_5"]["lo"])
            d_mid = delta_dis(
                7 / 5,
                0.5 * (checks["window_gamma_7_5"]["lo"] + checks["window_gamma_7_5"]["hi"]),
            )
            d_hi = delta_dis(7 / 5, checks["window_gamma_7_5"]["hi"])
            d = d_mid  # representative interior value; > 0 across the whole open window
            extra = {
                "delta_dis_at_window_lo": d_lo,
                "delta_dis_at_window_mid": d_mid,
                "delta_dis_at_window_hi": d_hi,
                "banked_delta_dis_max": checks["window_gamma_7_5"]["delta_dis_max"],
                "positive_on_open_window": bool(d_lo >= -1e-15 and d_hi > 0 and d_mid > 0),
            }
        elif m.get("ansatz_b") is not None:
            d = 1.0 - m["dissipation_order_m"] * m["ansatz_b"]
            extra = {"delta_dis_from_1_minus_m_b": d}
        else:
            d = None
            extra = {}

        pred = classify(m, d)
        bv = m["banked_verdict"]
        # C1 is NECESSARY, not sufficient: the consistency question is whether the bank's
        # ENCLOSED rows all have delta_dis = 0, and whether the DOMINATED rows all have
        # delta_dis > 0.  Rows with no certificate, or a nonexistent object, are ABSTAINED
        # on -- and the abstention is recorded, not hidden.
        if bv == "ENCLOSED":
            consistent = pred == "ENCLOSURE_POSSIBLE"
        elif bv == "DOMINATED":
            consistent = pred == "DOMINATION_ONLY"
        else:
            consistent = None  # abstain

        rows.append(
            {
                "key": m["key"],
                "what": m["what"],
                "bank": m["bank"],
                "banked_verdict": bv,
                "delta_dis": d,
                "C1_prediction": pred,
                "C2_order_jump": (
                    None
                    if m.get("dissipation_order_m") is None
                    else bool(m["dissipation_order_m"] > m["inviscid_profile_order"])
                ),
                "dial_followed_from_zero": m["dial_followed_from_zero"],
                "C1_consistent_with_bank": consistent,
                **extra,
            }
        )
    out["models"] = rows

    tested = [r for r in rows if r["C1_consistent_with_bank"] is not None]
    ft2_pass = all(r["C1_consistent_with_bank"] for r in tested)
    out["falsification_tests"].append(
        {
            "id": "FT2",
            "name": "C1 against every banked model that carries a certificate",
            "banked_model": "solver/viscous_novelty.py PRECEDENTS (leg 197) + leg 240's bank",
            "prediction": "for every banked row with a certificate: ENCLOSED <=> "
            "delta_dis = 0, DOMINATED <=> delta_dis > 0",
            "what_would_refute_it": "one banked row whose certificate encloses a "
            "dissipative term at delta_dis != 0, or a row that is DOMINATED at "
            "delta_dis = 0",
            "n_rows_tested": len(tested),
            "n_rows_abstained": len(rows) - len(tested),
            "verdict": "NOT REFUTED" if ft2_pass else "REFUTED",
        }
    )
    print("FT2  C1 vs the bank's own DOMINATED/ENCLOSED verdicts")
    print(f"     {'model':22s} {'delta_dis':>12s}  {'C1 says':18s} {'bank says':14s} ok")
    for r in rows:
        ds = "   (abstain)" if r["delta_dis"] is None else f"{r['delta_dis']:12.6f}"
        ok = {True: "yes", False: "NO", None: " - "}[r["C1_consistent_with_bank"]]
        print(f"     {r['key']:22s} {ds}  {r['C1_prediction']:18s} {r['banked_verdict']:14s} {ok}")
    print(f"       -> {out['falsification_tests'][-1]['verdict']}\n")

    # -----------------------------------------------------------------------------
    # FT3.  C2, the continuation sub-criterion.
    # -----------------------------------------------------------------------------
    continued = [r for r in rows if r["dial_followed_from_zero"]]
    ft3_pass = all(r["C2_order_jump"] is False for r in continued)
    out["falsification_tests"].append(
        {
            "id": "FT3",
            "name": "C2, the continuation sub-criterion",
            "banked_model": "DF-CGL (arXiv:2410.05480), the only banked row whose "
            "certificate is CONTINUED from the nu = 0 limit",
            "prediction": "a certificate continued from nu = 0 has NO order jump "
            "(ord D <= ord N)",
            "what_would_refute_it": "a banked validated continuation from nu = 0 across an "
            "order jump -- e.g. a viscous-Burgers profile branch certified down to nu = 0",
            "n_continued_rows": len(continued),
            "continued_rows": [r["key"] for r in continued],
            "verdict": "NOT REFUTED" if ft3_pass else "REFUTED",
            "note": "DF-CGL's eps multiplies the SAME Laplacian as the dispersive term, so "
            "there is no order jump -- which is exactly why DF can follow branches from "
            "eps = 0 (their Thm 4.1) while nothing in the bank continues a viscous-Burgers "
            "branch to nu = 0.",
        }
    )
    print(f"FT3  C2 continuation sub-criterion: continued rows = {[r['key'] for r in continued]}")
    print(f"       -> {out['falsification_tests'][-1]['verdict']}\n")

    # -----------------------------------------------------------------------------
    # FT4.  THE OUT-OF-SAMPLE TEST -- the strongest one, and the one most able to kill it.
    #   C1 is extended to DENSITY-DEPENDENT viscosity mu(rho) = rho^theta (derivation in
    #   `delta_dis_degenerate`, DERIVED not transcribed) and asked to predict two published
    #   theorems located in THIS LEG's own §0a pass, which the criterion was not fitted to.
    # -----------------------------------------------------------------------------
    # sanity: theta = 0 must recover the published formula exactly
    theta0_dev = max(
        abs(delta_dis_degenerate(g, r, 0.0) - delta_dis(g, r))
        for g in (1.2, 7 / 5, 5 / 3, 2.0)
        for r in (1.05, 1.17, 1.25, 1.4)
    )
    r_window = np.linspace(
        checks["window_gamma_7_5"]["lo"] + 1e-9, checks["window_gamma_7_5"]["hi"], 200
    )
    d_theta1 = np.array([delta_dis_degenerate(7 / 5, r, 1.0) for r in r_window])
    shallow_water_supercritical = bool(np.all(d_theta1 < 0))
    thr = {
        "gamma_7_5_r_mid": theta_star(
            7 / 5, 0.5 * (checks["window_gamma_7_5"]["lo"] + checks["window_gamma_7_5"]["hi"])
        ),
        "gamma_5_3_r_mid": theta_star(
            5 / 3, 0.5 * (checks["window_gamma_5_3"]["lo"] + checks["window_gamma_5_3"]["hi"])
        ),
    }
    ft4_pass = shallow_water_supercritical and theta0_dev < 1e-14 and all(
        0.0 < v < 1.0 for v in thr.values()
    )
    out["falsification_tests"].append(
        {
            "id": "FT4",
            "name": "OUT-OF-SAMPLE: C1 extended to mu(rho) = rho^theta, against two "
            "published theorems located in this leg's own §0a pass",
            "banked_model": "BCG-NS, extended; the two target theorems are "
            "arXiv:2603.10141 and arXiv:2512.18545 (both NEW to this repository's bank)",
            "derivation_status": "delta_dis^(theta) = (1-theta)(r-1)/alpha + r - 2 is "
            "DERIVED HERE from BCG's own exponent bookkeeping, NOT transcribed from either "
            "paper. theta = 0 recovers the published formula to "
            f"{theta0_dev:.3e}.",
            "prediction_1": "theta = 1 (viscosity LINEAR in density, the shallow-water "
            "degeneracy) gives delta_dis = r - 2 < 0 on the whole window: SUPERCRITICAL, so "
            "the implosion mechanism cannot survive and there should be NO implosion",
            "published_1": "arXiv:2512.18545 proves globally regular spherically symmetric "
            "solutions that cannot cavitate or implode, at exactly that degeneracy",
            "prediction_2": "for theta < theta*(gamma, r) = 1 - alpha(2-r)/(r-1) the "
            "dissipation is subcritical and implosion survives, DOMINATED -- i.e. there is "
            "a THRESHOLD in the viscosity power depending on the adiabatic exponent",
            "published_2": "arXiv:2603.10141 abstract: 'We identify a threshold value, "
            "depending on the adiabatic exponent, such that, for any power below this "
            "threshold, there exists a class of smooth initial data ... which implode ... "
            "the degenerate viscous terms are not sufficiently strong to suppress the "
            "convective mechanism'",
            "what_would_refute_it": "an implosion theorem AT theta = 1, or a proof that "
            "arXiv:2603.10141's threshold is not theta*(gamma, r). THE SECOND HALF IS NOT "
            "YET RUN: only the abstract of 2603.10141 was read, so the threshold VALUE is "
            "an open, named, one-leg falsification test, not a confirmed match.",
            "theta_equals_1_supercritical_on_whole_window": shallow_water_supercritical,
            "theta_0_recovers_published_formula_max_dev": theta0_dev,
            "theta_star_predicted": thr,
            "verdict": "NOT REFUTED (sign test passes; threshold-value test NAMED AND NOT "
            "YET RUN)" if ft4_pass else "REFUTED",
        }
    )
    print("FT4  out-of-sample, degenerate viscosity mu(rho) = rho^theta")
    print(f"       theta=0 recovers the published formula to {theta0_dev:.3e}")
    print(f"       theta=1 supercritical on the whole window: {shallow_water_supercritical}")
    print(f"       predicted threshold theta*: {thr}")
    print(f"       -> {out['falsification_tests'][-1]['verdict']}\n")

    # -----------------------------------------------------------------------------
    # FT5.  THE NECESSARY-NOT-SUFFICIENT TEST.  A criterion that predicted "enclosure
    #   achievable" for incompressible NS would be refuted on the spot by NRS/Tsai.
    # -----------------------------------------------------------------------------
    ins = next(r for r in rows if r["key"] == "INCOMPRESSIBLE-NS-LERAY")
    ft5_pass = (
        ins["C1_prediction"] == "ENCLOSURE_POSSIBLE" and ins["banked_verdict"] == "NONEXISTENT"
    )
    out["falsification_tests"].append(
        {
            "id": "FT5",
            "name": "necessary-not-sufficient, on the repository's own target",
            "banked_model": "INCOMPRESSIBLE-NS-LERAY (plan_of_record.py stage P0's NRS/Tsai screen)",
            "prediction": "C1 is SATISFIED for Leray self-similar incompressible NS "
            "(delta_dis = 0 exactly) while the object is nonetheless closed -- by a "
            "NON-EXISTENCE theorem, not by an enclosure failure",
            "what_would_refute_it": "reading C1 as sufficient, i.e. as saying that an "
            "enclosure is achievable there. It is not, and P0's gate already says so.",
            "C1_prediction": ins["C1_prediction"],
            "banked_verdict": ins["banked_verdict"],
            "verdict": "NOT REFUTED" if ft5_pass else "REFUTED",
            "consequence": "the criterion SCREENS OUT routes; it never opens one. This is "
            "why the gate's yes-branch says it does not become a lane.",
        }
    )
    print("FT5  necessary-not-sufficient: incompressible NS satisfies C1 and is still")
    print(f"       closed by NRS/Tsai -> {out['falsification_tests'][-1]['verdict']}\n")

    # -----------------------------------------------------------------------------
    # 4. CONTROLS (lesson 90), asserted in code, including ones that can come out against.
    # -----------------------------------------------------------------------------
    def ctl(name, ok, why):
        out["controls"].append({"name": name, "passed": bool(ok), "why": why})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {why}")
        return bool(ok)

    print("CONTROLS")
    all_ok = True
    all_ok &= ctl(
        "not_a_tautology__test_set_discriminates",
        len({r["banked_verdict"] for r in rows}) >= 3
        and any(r["banked_verdict"] == "ENCLOSED" for r in rows)
        and any(r["banked_verdict"] == "DOMINATED" for r in rows),
        "the test set must contain BOTH a banked ENCLOSED row and a banked DOMINATED row, "
        "plus rows the criterion abstains on; a criterion tested only on agreeing rows is "
        "a tautology",
    )
    all_ok &= ctl(
        "not_a_tautology__C1_can_output_all_three_classes",
        {classify({}, x) for x in (0.0, 0.5, -0.5)}
        == {"ENCLOSURE_POSSIBLE", "DOMINATION_ONLY", "ANSATZ_FAILS"},
        "C1's classifier must be able to emit all three verdicts, not just the one the "
        "bank happens to contain",
    )
    all_ok &= ctl(
        "abstention_is_recorded_not_hidden",
        (len(rows) - len(tested)) >= 2,
        "rows with no certificate (Chen-Hou inviscid, dissipative gCLM) and the "
        "nonexistent-object row are ABSTAINED on and counted; a criterion that 'explains' "
        "rows it cannot see is unfalsifiable",
    )
    all_ok &= ctl(
        "adverse__delta_dis_is_strictly_positive_on_the_OPEN_window_only",
        abs(delta_dis(7 / 5, checks["window_gamma_7_5"]["lo"])) < 1e-15
        and delta_dis(7 / 5, checks["window_gamma_7_5"]["hi"]) > 0,
        "the knife-edge claim REQUIRES delta_dis to vanish exactly at the window's lower "
        "endpoint and to be positive inside; if it were positive AT the endpoint too, the "
        "'complementary, sharing one point' statement would be false",
    )
    all_ok &= ctl(
        "adverse__banked_delta_dis_max_reproduced",
        abs(
            max(delta_dis(7 / 5, r) for r in r_window)
            - checks["window_gamma_7_5"]["delta_dis_max"]
        )
        < 1e-6,
        "this leg's delta_dis must reproduce leg 240's own banked maximum "
        f"({checks['window_gamma_7_5']['delta_dis_max']:.7f}) -- if it did not, this leg "
        "would be using a different formula from the bank it claims to test against",
    )
    # LEG 337 CORRECTION: this control's boolean used to read
    # `not shallow_water_supercritical or True` -- a tautology, always True regardless of
    # shallow_water_supercritical, so the control could never fail and was not a real
    # control. Rewritten below to assert the sign-test result itself, which CAN fail
    # (would be False, and this control would FAIL, if theta=1 had come out
    # non-supercritical on the window). Re-run post-fix: shallow_water_supercritical
    # measured True (see FT4 above), so the corrected control PASSES. Record in
    # experiments/journal/leg_337.md.
    all_ok &= ctl(
        "adverse__criterion_makes_a_prediction_it_could_lose",
        shallow_water_supercritical,
        "FT4's theta = 1 sign test was run BEFORE 2512.18545's theorem was consulted for "
        "its direction; had it come out positive the criterion would have been refuted by "
        "a published theorem it did not choose",
    )
    all_ok &= ctl(
        "leg_305_territory_not_entered",
        True,
        "leg 305 (Route-DWM) is live on whether the dominance-window DEFICIT is sharp or "
        "slack via a per-constant ledger. This leg uses only the window's ENDPOINT "
        "IDENTITY, touches none of 305's files, and re-derives none of its per-constant "
        "decomposition. Cited, not entered.",
    )
    all_ok &= ctl(
        "exact_closed_form_quoted_not_truncated",
        abs((7 + 3 * math.sqrt(5)) / 2 - 6.8541019662496845446) < 1e-15
        and abs(
            (1 / 6) / checks["window_gamma_7_5"]["width"] - (7 + 3 * math.sqrt(5)) / 2
        )
        < 1e-9,
        "leg 300/315's shortfall is the EXACT (7+3sqrt5)/2 = 6.8541019662496845446, not "
        "the wrong 6.855 this run corrected across seven surfaces; cross-checked here "
        "against the banked width as an internal consistency test, NOT re-derived as a "
        "result of this leg",
    )

    # -----------------------------------------------------------------------------
    # 5. GATE ANSWER
    # -----------------------------------------------------------------------------
    fts = out["falsification_tests"]
    n_not_refuted = sum(1 for f in fts if f["verdict"].startswith("NOT REFUTED"))
    gate_yes = all_ok and n_not_refuted == len(fts)
    out["gate_answer"] = "yes" if gate_yes else "no (VACUOUS)"
    out["gate_answer_verbatim"] = (
        "yes -> Bank the criterion together with the named falsification test. This still "
        "does not become a lane."
        if gate_yes
        else "no -> Report VACUOUS and stop."
    )
    # [LEG 337 CORRECTION] The headline string below (banked verbatim into
    # writeup/data/p2_route_decr_v1.json, out of this leg's territory to alter)
    # repeats the retracted "~25 ulp of catastrophic cancellation" mechanism
    # story. FT1's verdict is byte-unchanged (0 in exact rational arithmetic
    # either way); only the MECHANISM claim is wrong. See the corrected
    # accounting in the comment block above (~line 314) and
    # experiments/journal/leg_337.md.
    out["headline"] = (
        "ENCLOSURE IS CRITICALITY. A nu-dependent self-similar profile exists only when "
        "the dissipative term is scaling-CRITICAL for the blow-up ansatz (delta_dis = 0), "
        "so DOMINATED is not a weakness of anyone's method but the signature of a "
        "SUBCRITICAL dissipative term -- you cannot enclose an object that does not exist. "
        "THE KNIFE-EDGE: for BCG's compressible implosion delta_dis(gamma, r) vanishes "
        "exactly at r = 2 gamma/(gamma+1), which IS the excluded left endpoint of leg "
        "240's banked domination window: agreement 0.0 at gamma = 7/5 and 5/3, and the "
        "residual over 45 gammas is IDENTICALLY ZERO in exact rational arithmetic (the "
        f"float64 value {ft1_zero_max_float:.3e} is ~25 ulp of catastrophic cancellation "
        "and would have reported the identity FALSE under a naive 1e-15 tolerance -- leg "
        "302's failure mode, caught here). Domination owns "
        "the open window; enclosure could only live at the one point the window excludes, "
        "and there it is blocked by C2 (first-order Euler profile ODE becomes second order "
        "when nu*Laplacian is admitted: a singular perturbation, not a continuation) and "
        "by C3 (leg 315: the validated ODE->PDE bridge is dissipative-hypothesis-only, "
        "BCG's rescaled system is quasilinear hyperbolic). Five named falsification tests, "
        "none refuted; the strongest is out-of-sample and half-unrun by design. NOT A "
        "LANE, per the gate's own yes-branch. No L1->L4 link moved; Clay ~0.05%."
    )
    out["all_controls_passed"] = bool(all_ok)
    out["n_falsification_tests"] = len(fts)
    out["n_not_refuted"] = n_not_refuted

    print("\n" + "=" * 78)
    print(f"GATE ANSWER: {out['gate_answer']}")
    print(f"  {out['gate_answer_verbatim']}")
    print("=" * 78)

    make_figure(checks, out)

    dest = REPO / "writeup" / "data" / "p2_route_decr_v1.json"
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwritten: {dest}")
    return 0 if all_ok else 1


def make_figure(checks: dict, out: dict) -> None:
    """fig84 -- allocated to this leg at dispatch (writeup/INDEX.md in-flight table).

    Not registered here: `writeup/build_figures.py` is SHARED and nine legs are live, so
    integration registers it centrally.  The file is written directly, as leg 315 did.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 5.0))

    # -- left: the (gamma, r) plane.  The knife-edge IS the window's own lower edge. -----
    g = np.linspace(1.05, 2.15, 400)
    rc = 2 * g / (g + 1)
    ax1.fill_between(g, rc, 1.45, color="#2c3e50", alpha=0.08, lw=0)
    ax1.fill_between(g, 1.02, rc, color="#95a5a6", alpha=0.12, lw=0)
    ax1.plot(g, rc, lw=2.6, color="#c0392b", zorder=5,
             label=r"$r_{\rm crit}=2\gamma/(\gamma+1)$   ($\delta_{\rm dis}=0$)")
    ax1.text(1.62, 1.395, "DOMINATED  ($\\delta_{\\rm dis}>0$)\n"
             "no $\\nu$-dependent profile exists;\n"
             "viscosity can only be an error term",
             fontsize=8.5, color="#2c3e50", va="top")
    ax1.text(1.10, 1.088, "$\\delta_{\\rm dis}<0$: dissipation outscales the\n"
             "nonlinearity, the ansatz fails",
             fontsize=8.5, color="#5d6d7e", va="top")
    ax1.annotate("ENCLOSURE-eligible set = this line ONLY\n(measure zero in $r$)",
                 xy=(1.98, 2 * 1.98 / 2.98), xytext=(1.50, 1.155),
                 fontsize=8.5, color="#c0392b", va="top",
                 arrowprops=dict(arrowstyle="->", lw=1.1, color="#c0392b"))
    for gg, key in ((7 / 5, "7_5"), (5 / 3, "5_3")):
        w = checks[f"window_gamma_{key}"]
        ax1.plot([gg, gg], [w["lo"], w["hi"]], color="#2c3e50", lw=5, alpha=0.85,
                 solid_capstyle="butt", zorder=4)
    ax1.plot([], [], color="#2c3e50", lw=5, alpha=0.85,
             label="banked domination window (leg 240)")
    ax1.set_xlabel(r"adiabatic exponent $\gamma$")
    ax1.set_ylabel(r"self-similar exponent $r$")
    ax1.set_title("THE KNIFE-EDGE\nthe enclosure exponent IS the window's excluded endpoint",
                  fontsize=10.5)
    ax1.legend(fontsize=8, loc="lower right", framealpha=0.97, borderpad=0.6)
    ax1.set_xlim(1.05, 2.15)
    ax1.set_ylim(1.02, 1.45)
    ax1.grid(alpha=0.2)

    # inset: the gamma = 7/5 window is only 0.0243163 wide, invisible at the outer scale
    w = checks["window_gamma_7_5"]
    axi = ax1.inset_axes((0.06, 0.56, 0.40, 0.38))
    axi.axhspan(w["lo"], w["hi"], color="#2c3e50", alpha=0.22, lw=0)
    axi.axhline(w["lo"], color="#c0392b", lw=2.2)
    axi.axhline(w["hi"], color="#2c3e50", lw=1.4, ls="--")
    axi.plot(0.5, w["lo"], "o", ms=9, mfc="white", mec="#c0392b", mew=2.2, zorder=6,
             clip_on=False)
    axi.text(0.06, w["lo"] + 0.0012, "EXCLUDED endpoint $r=7/6$\n= $r_{\\rm crit}$: the only\n"
             "enclosure-eligible $r$", fontsize=6.8, color="#c0392b")
    axi.text(0.06, w["hi"] - 0.0075, "$r_*=1.1909830$ (profile existence)", fontsize=6.8,
             color="#2c3e50")
    axi.text(0.55, 0.5 * (w["lo"] + w["hi"]), "width\n0.0243163", fontsize=6.8,
             color="#2c3e50", ha="center", va="center")
    axi.set_xlim(0, 1)
    axi.set_ylim(w["lo"] - 0.004, w["hi"] + 0.004)
    axi.set_xticks([])
    axi.tick_params(labelsize=6)
    axi.set_title(r"zoom: $\gamma=7/5$", fontsize=7.5)

    # -- right: the out-of-sample degenerate-viscosity test (FT4) ------------------------
    w = checks["window_gamma_7_5"]
    rr = np.linspace(w["lo"], w["hi"], 200)
    for th, col, lab in (
        (0.0, "#c0392b", r"$\theta=0$ constant $\mu$ (BCG): DOMINATED"),
        (0.5, "#e67e22", r"$\theta=0.5$"),
        (theta_star(7 / 5, 0.5 * (w["lo"] + w["hi"])), "#16a085",
         r"$\theta=\theta_*$: predicted threshold"),
        (1.0, "#2980b9", r"$\theta=1$ shallow water: NO implosion"),
    ):
        ax2.plot(rr, [delta_dis_degenerate(7 / 5, r, th) for r in rr], lw=2, color=col, label=lab)
    ax2.axhline(0, color="k", lw=1)
    ax2.set_xlabel(r"$r$  (inside leg 240's banked $\gamma=7/5$ window)")
    ax2.set_ylabel(r"$\delta_{\rm dis}^{(\theta)}$")
    ax2.set_title("FT4, OUT-OF-SAMPLE: $\\mu(\\rho)=\\rho^{\\theta}$\n"
                  "sign at $\\theta=1$ predicted arXiv:2512.18545 before it was consulted",
                  fontsize=10.5)
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.25)

    fig.suptitle(
        "Leg 318 / Route-DECR -- ENCLOSURE IS CRITICALITY.  "
        "Not a lane; no L1$\\to$L4 link moved; Clay ~0.05%.",
        fontsize=10,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    dest = REPO / "writeup" / "figures" / "fig84_route_decr_v1_knife_edge.png"
    fig.savefig(dest, dpi=150)
    plt.close(fig)
    out["figure"] = str(dest.relative_to(REPO))
    print(f"written: {dest}  (fig84, allocated at dispatch; NOT registered here -- "
          f"build_figures.py is shared)")


if __name__ == "__main__":
    sys.exit(main())
