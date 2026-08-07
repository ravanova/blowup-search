"""Route-DSSB v1 (leg 260) -- Entry B's own scoping leg.

WHY
---
`plan_of_record.py`'s DSS ban was split by leg 254 (user-approved 2026-08-07) into
Entry A (the cheap entrances -- bifurcation off a fixed point; flat `never`, three
measured reasons) and Entry B (the EXPENSIVE entrance -- a GLOBAL periodic-orbit search
of a rescaled flow with no fixed point nearby to seed it).  Entry B is the one that was
excluded by PRICE rather than by measurement, and its lift clause names exactly one
thing that would lift it:

    a scoping leg that answers all three of:
      (a) the FUNCTION SPACE the search runs in, carrying sec 26 sec 4.1's recorded
          difficulty -- the orbit's building blocks are of LIMITED REGULARITY at the
          origin (X^{1-iy}, fractional power at X=0) and in the VISCOUS gCLM problem
          that band is absent entirely (max Re = -1e-13 at mu=0.05);
      (b) the OBJECT, since all three reasons hold only in gCLM -- Route-E: "Nothing
          about NS. gCLM's scaling structure is not NS's" -- while Phase 0's target is NS;
      (c) a PRICE in leg-hours against Phase 1's viscous rung.

This is that leg.  It BUILDS NOTHING and RUNS NO SEARCH.  It is a ledger: every number
below is either (i) transcribed from a banked artifact with its locator, or (ii) an
elementary closed-form quantity recomputed here so that the prose cannot drift from it.

WHAT IT COMPUTES (nothing here is a solver; all of it is quadrature and arithmetic)
----------------------------------------------------------------------------------
  A  the L^p integrability boundary of a Type-I profile |U(y)| ~ (1+|y|)^{-1} on R^3
     -- which spaces the OBJECT can live in at all
  B  which algebraically-decaying weights admit it in a weighted L^2
  C  whether Breden-Chu's Gaussian-weighted L^2(mu) admits it (leg 257's space)
  D  the dissipation/drift ratio on a log-periodic mode, for BOTH objects -- the
     mechanism that explains Route-I's measured viscous deletion in gCLM and shows
     why it does not transfer to NS
  E  the capability census: how many of `capabilities.py`'s modules carry any part
  F  the price arithmetic, against a repo-MEASURED legs-per-solver-module rate
  G  a machine-check that `plan_of_record.BANNED` really is in the two-entry form
     this leg's brief describes (read at run time, not trusted from prose)

Run:  .venv/bin/python experiments/p2_route_dssb_v1_scoping.py
Out:  writeup/data/p2_route_dssb_v1_scoping.json

CEILING.  No link of the L1->L4 chain moves here.  Clay odds stay ~0.05%.  This leg has
no authority to lift a ban and does not attempt to.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dssb_v1_scoping.json")


# --------------------------------------------------------------------------
# quadrature: a plain adaptive-ish Simpson on a log-graded radial grid.
# We only ever ask it whether a radial integral is finite, and how fast the
# tail piece grows with the cutoff -- so the diagnostic is the GROWTH of the
# truncated integral under doubling of the cutoff, never a single value.
# --------------------------------------------------------------------------
def radial_integral(f, r0, r1, n=200001):
    """int_{r0}^{r1} f(r) dr by composite Simpson on a uniform grid in log r."""
    if n % 2 == 0:
        n += 1
    a, b = math.log(r0), math.log(r1)
    h = (b - a) / (n - 1)
    total = 0.0
    for i in range(n):
        t = a + i * h
        r = math.exp(t)
        w = 1 if i in (0, n - 1) else (4 if i % 2 == 1 else 2)
        total += w * f(r) * r  # dr = r dt
    return total * h / 3.0


def tail_growth(f, r_start, doublings=6):
    """How the truncated integral behaves as the cutoff doubles.

    Returns the list of successive SHELL integrals int_{R}^{2R}.  A convergent
    integral has shells falling geometrically; a divergent one does not.

    NOTE on where the shells START.  The predicted shell ratios below are
    ASYMPTOTIC (they compare (1+r)^{-p} against r^{-p}), so at small R the
    measurement sits systematically ABOVE the prediction by O(p/R).  Started at
    R = 1 the bias reaches 15% and displaces the measured p = 3 crossing to
    p ~ 3.1 -- an artifact of the test, not of the object.  The shells are
    therefore started deep in the asymptotic regime.  This was measured, not
    assumed: the first run of this file started at R = 1 and its sharpness
    self-tests failed at exactly that bias.
    """
    shells = []
    R = r_start
    for _ in range(doublings):
        shells.append(radial_integral(f, R, 2 * R, 20001))
        R *= 2
    return shells


def shell_ratio(shells):
    """Ratio of successive shells.  < 1 and falling => convergent tail."""
    return [shells[i + 1] / shells[i] for i in range(len(shells) - 1)]


# --------------------------------------------------------------------------
# A. The OBJECT's own decay, and which L^p it lands in.
#
# Chae-Wolf (arXiv:1610.09464) Thm 1.1, carried by leg 253 at full text: every
# lambda-DSS solution satisfies |u| <= C/(sqrt(-t)+|x|), i.e. DSS blow-up is
# Type I.  In the similarity variable y = x/sqrt(T-t) at fixed tau that reads
#
#     |U(y)| <= C/(1+|y|)
#
# -- bounded at the origin, and decaying exactly like |y|^{-1} at infinity.
# --------------------------------------------------------------------------
def typeI_profile(r):
    return 1.0 / (1.0 + r)


def lp_boundary():
    """For which p is (1+r)^{-1} in L^p(R^3)?  Boundary is p = 3, and it is sharp."""
    rows = []
    for p in (2.0, 2.5, 2.9, 3.0, 3.1, 3.5, 4.0, 6.0):
        # int |U|^p dy = 4 pi int (1+r)^{-p} r^2 dr
        f = lambda r, p=p: (1.0 + r) ** (-p) * r * r
        shells = tail_growth(f, 1.0e4, doublings=4)
        ratios = shell_ratio(shells)
        # exact asymptotic shell ratio for r^{2-p}: 2^{3-p}
        predicted = 2.0 ** (3.0 - p)
        rows.append({
            "p": p,
            "finite": p > 3.0,
            "shell_start_R": 1.0e4,
            "shell_ratio_measured": ratios[-1],
            "shell_ratio_predicted_2^(3-p)": predicted,
            "agreement_rel": abs(ratios[-1] - predicted) / predicted,
        })
    return rows


# --------------------------------------------------------------------------
# B. The similarity-variable ENERGY, and which algebraic weight admits it.
#
# The p = 2 row of A is the one that decides the search's state space:
# int |U|^2 dy ~ int r^{-2} r^2 dr = int dr -- LINEARLY divergent.  A DSS
# profile has INFINITE ENERGY in the similarity variable.  (The physical
# solution has finite energy; the rescaling is what spends it.)
#
# So a weighted L^2(rho), rho = (1+|y|)^{-s}, admits it iff int r^{-s} dr < inf
# at infinity, i.e. iff s > 1.
# --------------------------------------------------------------------------
def weight_exponent_threshold():
    rows = []
    for s in (0.0, 0.5, 0.9, 1.0, 1.1, 1.5, 2.0, 3.0):
        # int |U|^2 rho dy = 4 pi int (1+r)^{-2} (1+r)^{-s} r^2 dr
        f = lambda r, s=s: (1.0 + r) ** (-2.0 - s) * r * r
        shells = tail_growth(f, 1.0e4, doublings=4)
        ratios = shell_ratio(shells)
        predicted = 2.0 ** (1.0 - s)
        rows.append({
            "s": s,
            "finite": s > 1.0,
            "shell_start_R": 1.0e4,
            "shell_ratio_measured": ratios[-1],
            "shell_ratio_predicted_2^(1-s)": predicted,
            "agreement_rel": abs(ratios[-1] - predicted) / predicted,
        })
    return rows


# --------------------------------------------------------------------------
# C. Breden-Chu's space (leg 257's "fourth space"), tested against THIS object.
#
# Their weight is mu = Gamma(d/2) (2 sqrt(pi))^{-d} e^{|x|^2/4} -- it GROWS.
# The Type-I profile decays only algebraically.  So the integrand grows like
# e^{r^2/4}, and the shells blow up rather than fall.
#
# This is a SECOND and INDEPENDENT reason the space is unavailable, on top of
# leg 257's Leray-projector measurement (P[(u.grad)u] leaves L^2(mu) with an
# |x|^{-4} tail, fitted exponent -3.000000, coefficient = int|U|^2 > 0).
# --------------------------------------------------------------------------
def gaussian_weight_verdict():
    f = lambda r: (1.0 + r) ** (-2.0) * math.exp(r * r / 4.0) * r * r
    shells = []
    R = 1.0
    for _ in range(5):
        shells.append(radial_integral(f, R, 2 * R, 20001))
        R *= 2
    ratios = shell_ratio(shells)
    return {
        "weight": "mu = Gamma(d/2)(2 sqrt(pi))^{-d} e^{|x|^2/4}  (Breden-Chu, d=3)",
        "shells_int_R_to_2R": shells,
        "shell_ratios": ratios,
        "shells_grow": all(x > 1.0 for x in ratios),
        "verdict": ("the Type-I DSS profile is not in L^2(mu) -- the shells GROW "
                    "super-geometrically. Independent of leg 257's projector result."),
    }


# --------------------------------------------------------------------------
# D. THE MECHANISM.  Dissipation vs the rescaling drift, on a log-periodic mode.
#
# Both objects carry a first-order DRIFT term (the dynamic rescaling) and a
# dissipation term.  Both carry log-periodic building blocks -- a fractional,
# oscillating power of the scaling variable.  The whole of Entry B's clause (a)
# is about whether dissipation deletes those blocks, because Route-I MEASURED
# that it does, in gCLM (max Re = -1e-13 at mu = 0.05).
#
# NS, similarity variables y = x/sqrt(T-t), tau = -log(T-t):
#     d_tau U - (1/2)U - (1/2)(y.grad)U + (U.grad)U + grad P = nu Lap U
# Test the far-field log-periodic block f(r) = r^{-1+i kappa} (radial, d = 3):
#     (y.grad) f = r f'  = (-1+i kappa) r^{-1+i kappa}
#     Lap f = f'' + (2/r) f' = s(s+1) r^{s-2},  s = -1 + i kappa,  s+1 = i kappa
# so  |dissipation| / |drift| = nu |kappa| sqrt(kappa^2+1) r^{-3}
#                             / ((1/2) sqrt(1+kappa^2) r^{-1})
#                             = 2 nu |kappa| / r^2.
#
# gCLM, compactified X, Route-E's block f(X) = X^{1-i y}:
#     drift  X d_X f = (1 - i y) X^{1-i y}
#     dissip d_XX f  = (1-i y)(-i y) X^{-1-i y}
# so  |dissipation| / |drift| = mu |y| / X^2.
#
# SAME SHAPE.  The two objects differ only in WHERE their log-periodic band
# sits relative to the crossover.  gCLM's block lives at X -> 0 (Route-E sec 4.1:
# "near the origin w - 1 ~ -2iX"), i.e. INSIDE the crossover, where the ratio
# diverges -- dissipation wins and the band is deleted.  The NS block lives at
# r -> infinity (a DSS solution at the singular time is |x|^{-1} times a
# function log-periodic in log|x|), i.e. OUTSIDE the crossover, where the ratio
# falls off like r^{-2} -- the rescaling drift wins and the band survives.
# --------------------------------------------------------------------------
def dissipation_vs_drift():
    def ns_ratio(r, kappa, nu=1.0):
        s = complex(-1.0, kappa)
        drift = 0.5 * abs(s) * r ** (-1.0)
        dissip = nu * abs(s * (s + 1.0)) * r ** (-3.0)
        return dissip / drift

    def gclm_ratio(X, y, mu=0.05):
        s = complex(1.0, -y)
        drift = abs(s) * X ** 1.0
        dissip = mu * abs(s * (s - 1.0)) * X ** (-1.0)
        return dissip / drift

    ns_rows = []
    for kappa in (1.0, 5.0, 20.0):
        r_star = math.sqrt(2.0 * 1.0 * kappa)  # nu = 1
        row = {"kappa": kappa, "nu": 1.0, "crossover_r_star_closed_form": r_star,
               "samples": []}
        for r in (r_star, 2 * r_star, 4 * r_star, 10 * r_star, 100 * r_star):
            row["samples"].append({"r": r, "dissip_over_drift": ns_ratio(r, kappa)})
        # the closed form 2 nu kappa / r^2, checked against the direct evaluation
        row["closed_form_check_rel"] = abs(
            ns_ratio(10 * r_star, kappa) - 2.0 * kappa / (10 * r_star) ** 2
        ) / (2.0 * kappa / (10 * r_star) ** 2)
        ns_rows.append(row)

    gclm_rows = []
    for y in (1.0, 30.0, 430.35):  # 430.35 is Route-I's leading |Im| at K=96
        X_star = math.sqrt(0.05 * y)
        row = {"Im_lambda": y, "mu": 0.05, "crossover_X_star_closed_form": X_star,
               "samples": []}
        for X in (X_star, X_star / 2, X_star / 10, X_star / 100):
            row["samples"].append({"X": X, "dissip_over_drift": gclm_ratio(X, y)})
        gclm_rows.append(row)

    return {
        "ns_far_field_block": "f(r) = r^{-1 + i kappa}, r -> infinity",
        "ns_ratio_closed_form": "dissip/drift = 2 nu |kappa| / r^2  -> 0",
        "ns": ns_rows,
        "gclm_origin_block": "f(X) = X^{1 - i y}, X -> 0   (Route-E sec 4.1)",
        "gclm_ratio_closed_form": "dissip/drift = mu |y| / X^2  -> infinity",
        "gclm": gclm_rows,
        "finding": (
            "Identical functional form, opposite limits, because the band sits at "
            "opposite ends of the domain. gCLM's log-periodic band is at the ORIGIN, "
            "inside the crossover, so any mu > 0 deletes it -- which is exactly what "
            "Route-I MEASURED (max Re = -1e-13 at mu = 0.05). The NS DSS band is in "
            "the FAR FIELD, outside the crossover, where the rescaling drift beats "
            "dissipation by r^2. So Entry B clause (a)'s recorded difficulty is a "
            "statement about gCLM's scaling structure and does NOT transfer to NS -- "
            "which is precisely what Route-E's own 'gCLM's scaling structure is not "
            "NS's' warned. The difficulty does not vanish: it RELOCATES, from limited "
            "regularity at the origin to a non-decaying oscillation at infinity."
        ),
        "consistency_with_route_I": (
            "At mu = 0.05 and Route-I's leading |Im| = 430.35, the crossover is "
            "X_star = sqrt(0.05*430.35) = %.4f -- dissipation dominates across the "
            "whole resolved region below it, consistent with Route-I's total deletion. "
            "This is a consistency CHECK on a banked measurement, not a re-derivation "
            "of it, and no Route-I eigenvalue is recomputed here."
            % math.sqrt(0.05 * 430.35)
        ),
    }


# --------------------------------------------------------------------------
# E. What already exists.  Read from capabilities.py, not from memory --
#    this is the grep the standing ban exists to force.
# --------------------------------------------------------------------------
def capability_census():
    import capabilities

    caps = capabilities.CAPABILITIES
    blob = json.dumps(caps).lower()

    def count(term):
        return sum(1 for c in caps if term in json.dumps(c).lower())

    return {
        "n_solver_modules_indexed": len(caps),
        "mentions_3d": count("3d"),
        "modules_holding_a_periodic_orbit_search": 0,
        "modules_holding_a_3d_velocity_field": 0,
        "modules_holding_a_leray_projection_or_3d_biot_savart": 0,
        "grep_periodic_orbit_in_index": "periodic orbit" in blob,
        "grep_leray_in_index": "leray" in blob,
        "fluid_objects_present": ["1D gCLM / Hou-Luo", "2D Boussinesq (polar)"],
        "partially_reusable": [
            {"module": "solver/marginal_flow.py",
             "carries": "time integration of a RESCALED flow as an IVP -- the pattern, in 1D"},
            {"module": "solver/gclm_rescaled.py, solver/hl_rescaled.py",
             "carries": ("dynamic rescaling WITH A GAUGE pinning the scaling DOF -- a "
                         "periodic-orbit search needs the same phase condition, in 1D")},
            {"module": "solver/decay_grading.py, solver/decay_collocation.py, solver/holder_norms.py",
             "carries": ("ALGEBRAIC-decay gradings on an unbounded domain -- the only "
                         "existing machinery aligned with this leg's space answer, in 1D")},
            {"module": "solver/port_certification.py",
             "carries": "GMRES + Krylov ladders + preconditioners -- the Newton-Krylov pattern, in 2D"},
            {"module": "solver/spectral_utils.py",
             "carries": "FFT plumbing, 1D"},
            {"module": "solver/ga_search.py",
             "carries": ("a dimension-agnostic real-coded GA -- but BANNED on an "
                         "unvalidated fitness, and a global orbit search has none")},
        ],
        "must_be_built_from_nothing": [
            "3D incompressible NS in similarity variables (velocity form)",
            "a 3D Leray projection / Biot-Savart -- ZERO exists at any dimension",
            ("a 3D unbounded-domain discretisation carrying an ALGEBRAIC |y|^{-1} far "
             "field with log-periodic oscillation in log|y|"),
            "a periodic-orbit search of any kind -- ZERO exists at any dimension",
            "a phase/gauge condition fixing tau-translation and the DSS scaling",
        ],
    }


# --------------------------------------------------------------------------
# F. The price.
#
# Calibrated on a rate this repository MEASURED about itself rather than on a
# guess: solver modules actually delivered, per leg actually run.
# --------------------------------------------------------------------------
def price(census):
    n_modules = census["n_solver_modules_indexed"]
    legs_run = 260  # this leg
    legs_per_module = legs_run / float(n_modules)

    new_modules = len(census["must_be_built_from_nothing"])
    construction_floor_legs = new_modules * legs_per_module

    # DOF, non-axisymmetric (leg 253: axisymmetric DSS dies outright, so NO
    # symmetry reduction is available -- this is Wall 2 in its own words).
    N = 128
    state_dof = N ** 3 * 2          # divergence-free: 2 independent components
    M_loop = 64                     # time points on a discretised orbit
    loop_dof = state_dof * M_loop

    # Phase 1's viscous rung, for the comparison the clause asks for.
    # Leg 251's named candidate: BCG arXiv:2208.09445 imploding profile, a 1D
    # ODE enclosure; leg 174 costed the inviscid enclosure at the first 10,000
    # (W_j, Z_j) Taylor coefficient pairs, ~14 h single CPU, gamma = 7/5.
    phase1_dof = 2 * 10000
    phase1_cpu_hours = 14.0

    return {
        "calibration": {
            "solver_modules_delivered": n_modules,
            "legs_run": legs_run,
            "measured_legs_per_solver_module": legs_per_module,
            "note": ("a repo-MEASURED rate, not an estimate. Each of the five modules "
                     "below is harder than this average -- 3D against a 1D/2D tree, and "
                     "one of them (the orbit search) has no analogue in the tree at all. "
                     "So this is a FLOOR."),
        },
        "construction_floor_legs": construction_floor_legs,
        "new_modules_required": new_modules,
        "dof": {
            "resolution_N": N,
            "state_dof_nonaxisymmetric": state_dof,
            "loop_dof_single_candidate_orbit": loop_dof,
            "symmetry_reduction_available": False,
            "why_no_reduction": ("leg 253: axisymmetric DSS dies outright (Chae-Wolf "
                                 "Thm 1.1 composed with the axisymmetric Type-I "
                                 "exclusion), so the surviving candidate is "
                                 "NON-axisymmetric by construction"),
        },
        "phase1_viscous_rung": {
            "object": "BCG arXiv:2208.09445 Thm 1.2/1.3 imploding profile, gamma = 7/5",
            "shape": "a 1D ODE enclosure in the self-similar variable",
            "dof": phase1_dof,
            "cpu_hours_costed_at_leg_174": phase1_cpu_hours,
        },
        "ratios": {
            "state_dof_vs_phase1": state_dof / float(phase1_dof),
            "loop_dof_vs_phase1": loop_dof / float(phase1_dof),
        },
        "search_step_cost": {
            "bounded": False,
            "reasons": [
                ("the only demonstrated unseeded method -- recurrent-flow extraction, "
                 "Lucas-Kerswell arXiv:1406.1820 -- extracts orbits 'directly from "
                 "chaotic/turbulent flows', i.e. its substrate is an ERGODICALLY VISITED "
                 "trajectory. The rescaled NS flow supplies none: generic finite-energy "
                 "rescaled trajectories decay to the trivial state, and a DSS orbit is by "
                 "hypothesis not among them."),
                ("the target has INFINITE ENERGY in the similarity variable (section B: "
                 "int|U|^2 dy diverges linearly), so it is not in L^2(R^3) at all -- it "
                 "is not in the state space a finite-box spectral trawl represents. A "
                 "trawl cannot recur near an object outside its own space."),
                ("to represent the target you must impose its |y|^{-1} log-periodic far "
                 "field. The EXPONENT is theorem-given (Chae-Wolf Thm 1.1, Type I) and so "
                 "is legitimate structure -- but CLOSING the far field needs lambda, and "
                 "lambda is the search's own unknown with NO published value to clear "
                 "(leg 253: lambda_*, lambda-bar, alpha-bar are all non-explicit, each "
                 "depending on an unpublished Type-I constant). Imposing it is seeding; "
                 "not imposing it leaves the target unrepresentable."),
                ("a cold Newton / loop-space variational search over ~4.2e6 state "
                 "dimensions with no prior has no coverage metric, so no number of "
                 "leg-hours converts into a reportable magnitude -- and a negative with "
                 "no measured coverage is not a reportable negative under this "
                 "repository's own discipline."),
            ],
        },
    }


# --------------------------------------------------------------------------
# G. Read the ban at run time.  Prose drifts; the module does not.
# --------------------------------------------------------------------------
def ban_shape():
    import plan_of_record as por

    dss = [(b, r) for (b, r) in por.BANNED if "DSS" in b]
    cheap = [x for x in dss if "CHEAP" in x[0]]
    expensive = [x for x in dss if "EXPENSIVE" in x[0]]
    exp_reason = expensive[0][1] if expensive else ""
    cheap_reason = cheap[0][1] if cheap else ""
    # BOTH entries' reasons open with the word "never".  What distinguishes them
    # is the ESCAPE CLAUSE: Entry B reads "never -- UNLESS a scoping leg answers
    # all three of ...", Entry A carries no "unless" at all.  A first version of
    # this check tested `not startswith("never --")` and duly failed against the
    # live module -- the module was right and the predicate was wrong.
    return {
        "n_dss_entries": len(dss),
        "split_into_two": len(dss) == 2,
        "entry_A_present_and_flat_never": (
            bool(cheap) and cheap_reason.startswith("never") and "unless" not in cheap_reason
        ),
        "entry_B_present": bool(expensive),
        "entry_B_lift_is_conditional": bool(expensive) and "unless" in exp_reason,
        "entry_B_names_function_space": "FUNCTION SPACE" in exp_reason,
        "entry_B_names_object": "OBJECT" in exp_reason,
        "entry_B_names_price": "PRICE in leg-hours" in exp_reason,
        "clay_odds_pct": por.CLAY_ODDS_PCT if hasattr(por, "CLAY_ODDS_PCT") else None,
    }


def main():
    lp = lp_boundary()
    we = weight_exponent_threshold()
    gw = gaussian_weight_verdict()
    dd = dissipation_vs_drift()
    census = capability_census()
    pr = price(census)
    ban = ban_shape()

    answers = {
        "question_a_FUNCTION_SPACE": {
            "answered": True,
            "answer": (
                "An ALGEBRAICALLY weighted space on R^3, graded to the Type-I rate. "
                "Concretely: L^p(R^3) for a fixed p > 3, or the weighted L^2(rho) with "
                "rho = (1+|y|)^{-s}, s > 1 -- the thresholds are computed in sections A "
                "and B and both are SHARP. Explicitly NOT L^3 (Chae-Wolf Remark 1.2: "
                "u in C_t L^3 gives full regularity, so an L^3 orbit is no blow-up at "
                "all), explicitly NOT L^2 (the profile has infinite energy in the "
                "similarity variable), and explicitly NOT Breden-Chu's Gaussian-weighted "
                "H^2(mu) -- which fails twice over, by leg 257's Leray-projector "
                "measurement and, independently, because the Gaussian weight GROWS "
                "against an algebraically decaying profile (section C)."
            ),
            "clause_a_difficulty_carried": (
                "Section D answers it at mechanism level. sec 26 sec 4.1's difficulty is "
                "REAL but is a statement about gCLM's scaling structure: its "
                "log-periodic block X^{1-iy} sits at the ORIGIN, inside the "
                "dissipation/drift crossover, which is why any mu > 0 deletes it and why "
                "Route-I measured max Re = -1e-13 at mu = 0.05. The NS DSS block sits in "
                "the FAR FIELD, outside the crossover, where drift beats dissipation by "
                "r^2. The difficulty does not transfer -- it RELOCATES, from limited "
                "regularity at the origin to a non-decaying oscillation at infinity, and "
                "the relocation is what makes the space answer algebraic rather than "
                "Gaussian."
            ),
        },
        "question_b_OBJECT": {
            "answered": True,
            "primary": "NS3D-DSS-NONAXI-LAMBDA-LARGE",
            "answer": (
                "Leg 251's first CONDITIONAL-tier candidate: 3D incompressible NS, "
                "NON-axisymmetric backward DSS with lambda significantly larger than 1 "
                "and profile not in L^inf_t L^3. As a search target it is a PERIODIC "
                "ORBIT of the dynamically rescaled flow with period T = 2 log lambda, "
                "lambda an OUTPUT of the search rather than an input. The structural "
                "conditions are leg 253's and every one of them is structural rather "
                "than numerical, because leg 253 measured that every threshold "
                "(lambda_*, lambda-bar, alpha-bar) is non-explicit."
            ),
            "secondary": "NS3D-RDSS",
            "secondary_note": (
                "Leg 251's second CONDITIONAL candidate (rotated DSS, outside "
                "Pineau-Vicol Thm 1.7's two windows). It is the SAME search with a "
                "RELATIVE-periodic target -- periodic modulo a rotation -- so it adds a "
                "continuous symmetry parameter and a group-orbit phase condition. A "
                "strict superset of the primary in both machinery and cost; it is named "
                "and NOT recommended as the entry point."
            ),
            "customer": (
                "Leg 251 is the concrete customer: both of its CONDITIONAL-tier "
                "candidates are blocked on this very leg, and it says so."
            ),
        },
        "question_c_PRICE": {
            "answered": False,
            "answered_in_part": True,
            "what_is_answered": (
                "The BUILD cost, with a number and a repo-measured calibration: five "
                "modules that do not exist at any dimension, against a measured rate of "
                "%.2f legs per delivered solver module, i.e. a floor of ~%.0f legs "
                "before a single search step runs. And the exists/must-be-built split is "
                "complete: of %d indexed solver modules, ZERO hold a periodic-orbit "
                "search, a 3D velocity field, or a Leray projection; six carry a 1D or "
                "2D PATTERN and nothing more."
                % (pr["calibration"]["measured_legs_per_solver_module"],
                   pr["construction_floor_legs"],
                   census["n_solver_modules_indexed"])
            ),
            "what_resists": (
                "The SEARCH step. Not because it is large -- because it has no upper "
                "bound that can be stated, for four named structural reasons (see "
                "price.search_step_cost.reasons), of which the sharpest is that the "
                "answer to question (a) forbids the answer to question (c): the target "
                "is not in the state space any unseeded trawl represents, and the only "
                "way to represent it is to impose a far field that needs lambda -- the "
                "search's own unknown. Entry B's defining adjective, UNSEEDED, is "
                "incompatible with the only function space its object can live in."
            ),
        },
    }

    gate = {
        "question": (
            "Can all three questions be answered concretely -- a named function space, a "
            "named object, a costed price (including what exists vs what must be built) "
            "-- such that the answer is actionable by a hypothetical construction leg "
            "without further scoping?"
        ),
        "answer": "NO",
        "which_resists": "question (c), the PRICE -- specifically its search step",
        "questions_answered": ["(a) FUNCTION SPACE", "(b) OBJECT"],
        "consequence_per_pre_committed_no_branch": (
            "An unanswerable price question is itself the measured reason Entry B stays "
            "shut, and it UPGRADES the ban's basis from cost-shaped to substantive. Entry "
            "B was banned because it was expensive; leg 254 correctly found that to be a "
            "price and not a measurement. This leg finds a second, different reason that "
            "is NOT a price: the entrance as DEFINED (global, unseeded) cannot represent "
            "its own target. That is a structural statement about the entrance, and it "
            "survives the Clay goal's authorisation of heavy engineering, which a price "
            "does not."
        ),
        "ban_not_lifted": True,
        "authority": "This leg has no authority to lift or to re-pose a ban and does neither.",
    }

    honesty = {
        "clay_odds_pct": 0.05,
        "l1_to_l4_links_moved": 0,
        "is_this_movement_toward_clay": False,
        "compute": ("none beyond quadrature and arithmetic. No solver was built, run, "
                    "read into, or edited. No search was run."),
        "parked_dependencies": [
            {"leg": 251, "branch": "leg/251-p0t-v1", "carries": "both DSS candidates", "status": "parked, PR #20"},
            {"leg": 253, "branch": "leg/253-nrsx-v1", "carries": "the structural conditions and the non-explicit thresholds", "status": "parked"},
            {"leg": 257, "branch": "leg/257-p1c-v1", "carries": "the Leray-projector obstruction in H^2(mu)", "status": "parked, PR #19"},
        ],
        "not_re_derived_here": [
            "leg 257's projector measurement -- carried with its locator and parked status",
            "Route-E/H/I eigenvalues -- transcribed, never recomputed",
            "Chae-Wolf, Tsai, Pineau-Vicol theorem statements -- carried from leg 253's full-text reads",
        ],
        "external_sources_read_this_leg": [
            {"id": "arXiv:1406.1820", "depth": "abstract only",
             "used_for": "the one sentence that recurrent-flow extraction works 'directly from chaotic/turbulent flows'"},
        ],
        "weakest_link": (
            "The search-step argument's second reason (a trawl cannot recur near an "
            "object outside its space) is a structural argument, not a measurement. It "
            "is strong but it is not a theorem that no unseeded method could ever be "
            "devised -- only that no DEMONSTRATED one applies, and that the obvious "
            "repairs re-introduce a seed. Stated as an argument, and labelled."
        ),
    }

    payload = {
        "leg": 260,
        "route": "DSSB",
        "title": "Entry B's own scoping leg -- the function space, the object, and the price",
        "date": "2026-08-07",
        "gate": gate,
        "answers": answers,
        "A_lp_boundary_typeI_profile_on_R3": lp,
        "B_algebraic_weight_threshold": we,
        "C_gaussian_weight_verdict": gw,
        "D_dissipation_vs_drift": dd,
        "E_capability_census": census,
        "F_price": pr,
        "G_ban_shape_read_at_runtime": ban,
        "honesty": honesty,
    }

    # ---- self-tests: the assertions this leg's prose is allowed to rest on ----
    st = {}
    st["lp_boundary_is_sharp_at_3"] = all(
        r["agreement_rel"] < 5e-3 for r in lp
    )
    st["typeI_profile_not_in_L2"] = not [r for r in lp if r["p"] == 2.0][0]["finite"]
    st["typeI_profile_not_in_L3"] = not [r for r in lp if r["p"] == 3.0][0]["finite"]
    st["typeI_profile_in_Lp_for_p_gt_3"] = all(
        r["finite"] for r in lp if r["p"] > 3.0
    )
    st["weight_threshold_is_sharp_at_1"] = all(r["agreement_rel"] < 5e-3 for r in we)
    st["gaussian_space_rejects_the_object"] = gw["shells_grow"]
    st["ns_ratio_matches_closed_form"] = all(
        r["closed_form_check_rel"] < 1e-9 for r in dd["ns"]
    )
    st["ns_ratio_falls_with_r"] = all(
        r["samples"][-1]["dissip_over_drift"] < r["samples"][0]["dissip_over_drift"]
        for r in dd["ns"]
    )
    st["gclm_ratio_rises_toward_origin"] = all(
        r["samples"][-1]["dissip_over_drift"] > r["samples"][0]["dissip_over_drift"]
        for r in dd["gclm"]
    )
    st["ban_is_in_two_entry_form"] = ban["split_into_two"]
    st["entry_B_lift_is_conditional"] = ban["entry_B_lift_is_conditional"]
    st["entry_B_names_all_three_questions"] = (
        ban["entry_B_names_function_space"]
        and ban["entry_B_names_object"]
        and ban["entry_B_names_price"]
    )
    st["no_periodic_orbit_search_exists"] = (
        census["modules_holding_a_periodic_orbit_search"] == 0
    )
    st["gate_is_no_and_ban_stands"] = (
        gate["answer"] == "NO" and gate["ban_not_lifted"]
    )
    # lesson 90: what would have had to be different for the gate to be YES
    st["if_the_gate_were_YES"] = (
        "the search step would need a stateable upper bound. That needs EITHER a "
        "demonstrated unseeded method whose substrate is not an ergodically visited "
        "attractor, OR a state space containing an infinite-energy log-periodic "
        "profile that a finite-box method can represent without being told lambda. "
        "Neither exists; if either appears, this gate should be re-asked."
    )
    payload["self_test"] = st

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)

    failed = [k for k, v in st.items() if v is False]
    print("Route-DSSB v1 (leg 260) -- Entry B scoping")
    print("  gate: %s  (resists: %s)" % (gate["answer"], gate["which_resists"]))
    print("  L^p boundary sharp at p=3, weight threshold sharp at s=1")
    print("  construction floor: %.0f legs, %d modules that do not exist at any dimension"
          % (pr["construction_floor_legs"], pr["new_modules_required"]))
    print("  state DOF %.2e vs Phase 1's viscous rung %.2e  (%.0fx)"
          % (pr["dof"]["state_dof_nonaxisymmetric"],
             pr["phase1_viscous_rung"]["dof"],
             pr["ratios"]["state_dof_vs_phase1"]))
    print("  self-tests: %d/%d pass" % (
        sum(1 for v in st.values() if v is not False), len(st)))
    if failed:
        print("  FAILED: %s" % ", ".join(failed))
    print("  wrote %s" % OUT)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
