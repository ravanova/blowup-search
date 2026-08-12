"""Admissibility screen for DSSP candidates. Route-DSSP brick B7 (DSSP-SCREEN).

WHAT THIS MODULE IS FOR
------------------------------------------------------------------------------
B7's gate (TECHNICAL_P2_ROUTEDSSP_V1.md Sec 5.1): does every candidate carry
its admissibility screen, computed at EVERY step of whatever iterative
process produces it --

    ||V||_L3(R^3), the fitted far-field decay exponent, lambda, and an
    axisymmetry diagnostic

-- and does the rigidity ledger (NRS/Tsai; Chae-Tsai; Pineau-Vicol) get
MACHINE-READ against those measurements, rather than transcribed as prose?

This module is diagnostics only. It builds NO new candidate (leg 313's
NS3D-DSS-NONAXI-LAMBDA-LARGE search target is unchanged, and B6 -- the
Newton-Krylov/multiple-shooting layer that would actually PRODUCE a candidate
-- is user-gated and has not landed). It is exercised here on the two
DSSP-family objects that HAVE landed: leg 351's closed-form Type-I
Biot-Savart witness (solver/dssp_biot_savart.py) and leg 354's single-mode
Galerkin trajectory built on it (solver/dssp_step.py). Both are imported
read-only; nothing in either module is redefined here.

THE FOUR SCREEN QUANTITIES
------------------------------------------------------------------------------
1. l3_norm_ladder(field_fn, ...) -- ||V||_L3(R^3) by spherical quadrature
   (Gauss-Legendre in r and in cos(theta), equally-spaced trapezoid in phi --
   the same scheme legs 332/351/354 already use), summed over a shell
   ladder in R_hi and checked for convergence of the cumulative integral.
   An algebraic 1/|x|-type tail makes the |V|^3 integrand ~ 1/|x| at large
   |x|, so its R^3-volume integral is LOGARITHMICALLY DIVERGENT -- the
   ladder is expected NOT to converge for such a candidate, and non-
   convergence is reported as a measurement (DIVERGENT), not an error.

2. fitted_far_field_decay_exponent(field_fn, ...) -- samples |V| along a
   generic (non-axis-aligned) ray and fits log|V| vs log(r) by least
   squares, exactly as leg 332 did ("fitted decay exponent of |u_B| on a
   generic off-axis ray").

3. lambda_from_trajectory(...) -- leg 330's landed record (writeup/data/
   p2_route_pvlx_v1.json) pins S0 = 2*log(lambda) as the period of the
   rescaled flow's non-trivial periodic orbit. Given a trajectory c(s) (the
   one-parameter amplitude this repository's only landed stepper produces,
   solver/dssp_step.py), this function looks for a non-trivial RETURN to
   the initial amplitude -- a candidate period -- and reports lambda =
   exp(S0/2) if one is found. If the trajectory instead relaxes
   monotonically toward the trivial state Omega=0 (leg 354's OWN landed
   gate finding, brick B4), there is no period to measure and lambda is
   reported as UNDEFINED FOR THIS CANDIDATE, with the reason stated -- this
   is itself a diagnostic result, not a missing one.

4. axisymmetry_residual(field_fn, ...) -- an axisymmetric vector field's
   cylindrical components (V_rho, V_phi, V_z) must be independent of the
   azimuthal angle phi. This function samples V on phi-rings at a ladder of
   (rho, z) and reports the worst relative spread of each cylindrical
   component across phi -- a MEASURED quantity, not an assumption that the
   ansatz used to build the candidate was axisymmetric.

THE MACHINE-READ RIGIDITY LEDGER
------------------------------------------------------------------------------
Three entries, each read from a LANDED, machine-parseable record rather than
retyped as a summary sentence:

* NRS/Tsai -- not a leg-specific file (it is the general fact stated in the
  plan and used by leg 332's own gate: u in L^3(R^3) forces u=0 for backward
  self-similar 3D Navier-Stokes). Machine-read directly against THIS
  candidate's OWN l3_norm_ladder() result: EXCLUDED iff the ladder converged
  to a finite value.

* Chae-Tsai -- parsed from writeup/data/p2_route_ctrx_v1.json (leg 326,
  landed c541cdb), specifically gate.clause_ledger.alpha_equation.verdict
  and gate.branch, programmatically, not by re-stating "measured silent" as
  a fixed string.

* Pineau-Vicol -- parsed from writeup/data/p2_route_pvlx_v1.json (leg 330,
  landed 5496bbc): the H5 clause entry in clause_by_clause (the deciding
  clause, "if 1 < lambda < lambda_underline") and the WLOG ceiling on
  lambda_underline from magnitudes_of_near_1 (M1, value_lambda_ceiling).
  Compared PROGRAMMATICALLY against the candidate's OWN measured lambda
  (from lambda_from_trajectory): a candidate with lambda >= the ceiling, or
  with no measured lambda at all, is reported OUTSIDE / NOT APPLICABLE; a
  candidate with lambda inside the ceiling is flagged for re-adjudication
  (the exact lambda_underline is data-dependent on C_{U,0}, so a candidate
  landing inside the WLOG bound is not auto-excluded by this module -- see
  leg 330's own GAP-330-B/GAP-330-C corrections, read but not re-derived
  here).

WHAT THIS MODULE DOES NOT CLAIM
------------------------------------------------------------------------------
This is a screening instrument, not a new candidate and not a certificate.
Surviving every ledger entry means "not already excluded by a published
theorem reachable on this repository's record" -- it is NOT evidence for
existence and NOT a proof or a Clay claim. CEILING: TIER 2.
"""
from __future__ import annotations

import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTRX_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_ctrx_v1.json")
PVLX_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_pvlx_v1.json")
VORT_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_vort_v1.json")


# =============================================================================
# 1. ||V||_L3(R^3)
# =============================================================================

def _spherical_shell_nodes(R_lo, R_hi, n_r=200, n_c=32, n_phi=8):
    """Gauss-Legendre in r in [R_lo,R_hi], in cos(theta) in [-1,1],
    equally-spaced trapezoid in phi in [0,2*pi) -- the same scheme legs
    332/351/354 already use for R^3 quadrature."""
    gr, wr = np.polynomial.legendre.leggauss(n_r)
    r = 0.5 * (R_hi - R_lo) * gr + 0.5 * (R_hi + R_lo)
    wr = wr * 0.5 * (R_hi - R_lo)
    gc, wc = np.polynomial.legendre.leggauss(n_c)
    phi = (np.arange(n_phi) + 0.5) * (2.0 * np.pi / n_phi)
    wphi = np.full(n_phi, 2.0 * np.pi / n_phi)
    R, C, P = np.meshgrid(r, gc, phi, indexing="ij")
    WR, WC, WP = np.meshgrid(wr, wc, wphi, indexing="ij")
    sinth = np.sqrt(np.maximum(1.0 - C * C, 0.0))
    x = R * sinth * np.cos(P)
    y = R * sinth * np.sin(P)
    z = R * C
    pts = np.stack([x, y, z], axis=-1)
    weights = WR * WC * WP * R * R  # r^2 dr d(cos theta) dphi
    return pts, weights


def l3_norm_shell(field_fn, R_lo, R_hi, n_r=200, n_c=32, n_phi=8):
    """Int_{R_lo<|x|<R_hi} |V(x)|^3 dx, by spherical quadrature."""
    pts, w = _spherical_shell_nodes(R_lo, R_hi, n_r, n_c, n_phi)
    V = field_fn(pts)
    mag3 = np.sum(V * V, axis=-1) ** 1.5
    return float(np.sum(w * mag3))


def l3_norm_ladder(field_fn, R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                    inner_R=1e-6, rel_tol=1e-4, n_r=300, n_c=48, n_phi=16):
    """||V||_L3(R^3), cumulative over a shell ladder in R_hi, with a
    convergence check on the LAST step's relative change. An algebraic
    Type-I tail (|V| ~ C/|x|) makes |V|^3 dx ~ (1/|x|) dx at large |x|,
    logarithmically divergent -- non-convergence over this ladder is
    reported as DIVERGENT, which is a measurement, not a failure."""
    rows = []
    cube = 0.0
    prev_R = inner_R
    for R in R_hi_ladder:
        shell = l3_norm_shell(field_fn, prev_R, R, n_r, n_c, n_phi)
        cube += shell
        rows.append({"R_hi": R, "shell_integral_cube": shell, "cumulative_cube": cube})
        prev_R = R
    if len(rows) >= 2 and rows[-1]["cumulative_cube"] != 0:
        rel_change = abs(rows[-1]["cumulative_cube"] - rows[-2]["cumulative_cube"]) \
            / abs(rows[-1]["cumulative_cube"])
    else:
        rel_change = float("inf")
    converged = bool(rel_change < rel_tol)
    cube = rows[-1]["cumulative_cube"]
    norm = float(cube ** (1.0 / 3.0)) if cube >= 0 else float("nan")
    return {
        "ladder": rows,
        "L3_cubed": cube,
        "L3_norm": norm,
        "rel_change_last_step": rel_change,
        "rel_tol": rel_tol,
        "converged": converged,
    }


# =============================================================================
# 2. Fitted far-field decay exponent
# =============================================================================

def fitted_far_field_decay_exponent(field_fn, direction=(0.4, 0.5, np.sqrt(1.0 - 0.4 ** 2 - 0.5 ** 2)),
                                     r_values=None):
    """Fits log|V(r*direction)| vs log(r) by least squares on a generic
    off-axis ray (not aligned with any coordinate axis, so an axisymmetric
    candidate's swirl structure does not accidentally vanish along it)."""
    direction = np.asarray(direction, dtype=float)
    direction = direction / np.linalg.norm(direction)
    if r_values is None:
        r_values = np.logspace(1.0, 3.0, 12)
    r_values = np.asarray(r_values, dtype=float)
    pts = r_values[:, None] * direction[None, :]
    V = field_fn(pts)
    mag = np.linalg.norm(V, axis=-1)
    slope, intercept = np.polyfit(np.log(r_values), np.log(np.maximum(mag, 1e-300)), 1)
    return {
        "direction": direction.tolist(),
        "r_values": r_values.tolist(),
        "magnitudes": mag.tolist(),
        "fitted_exponent": float(slope),
        "fitted_log_intercept": float(intercept),
    }


# =============================================================================
# 3. lambda from a trajectory
# =============================================================================

def lambda_from_trajectory(s_vals, c_vals, return_tol=1e-3, decay_tol=1e-2):
    """Looks for a non-trivial return of |c(s)|/|c(0)| to near 1 -- a
    candidate period S0, giving lambda = exp(S0/2) per leg 330's landed
    S0 = 2*log(lambda) convention (writeup/data/p2_route_pvlx_v1.json,
    clause H3). If the trajectory instead relaxes monotonically toward 0
    (leg 354's own landed B4 gate finding), there is no period and lambda
    is reported as undefined for this candidate."""
    s_vals = np.asarray(s_vals, dtype=float)
    c_vals = np.asarray(c_vals, dtype=float)
    c0 = c_vals[0]
    if abs(c0) < 1e-300:
        return {"lambda": None, "S0": None, "measured": False,
                "reason": "trivial initial data (c0 = 0); no orbit to measure"}
    ratio = np.abs(c_vals) / abs(c0)
    decayed = bool(ratio[-1] < decay_tol)
    # a "return" is a sample, AFTER the trajectory has first left the
    # near-c0 band, whose ratio comes back within return_tol of 1 -- this
    # excludes the trivial "return" of a smooth curve's own neighbourhood
    # of s=0, which would otherwise fire on the very next sample
    left_band = np.where(ratio[1:] < 1.0 - return_tol)[0]
    if left_band.size == 0:
        returns = np.array([], dtype=int)
    else:
        after_leaving = left_band[0]
        tail = ratio[1:][after_leaving:]
        returns_in_tail = np.where(tail > 1.0 - return_tol)[0]
        returns = returns_in_tail + after_leaving if returns_in_tail.size else np.array([], dtype=int)
    if returns.size == 0:
        return {
            "lambda": None, "S0": None, "measured": False,
            "final_ratio_c_over_c0": float(ratio[-1]),
            "relaxes_monotonically_to_trivial": decayed,
            "reason": (
                "trajectory relaxes toward the trivial state Omega=0 rather "
                "than returning to a non-trivial periodic value (matches "
                "leg 354's landed B4 gate finding); no non-trivial period "
                "S0 was found, so lambda is UNDEFINED for this candidate"
            ),
        }
    S0 = float(s_vals[1:][returns[0]])
    lam = float(np.exp(S0 / 2.0))
    return {"lambda": lam, "S0": S0, "measured": True,
            "reason": "a non-trivial return to |c|/|c0| within tolerance was found"}


# =============================================================================
# 4. Axisymmetry diagnostic
# =============================================================================

def axisymmetry_residual(field_fn, rhos=(0.5, 1.0, 2.0, 5.0, 10.0), zs=(0.0, 0.5, -1.0, 2.0),
                          n_phi=24, scale_floor=1e-12):
    """An axisymmetric vector field's cylindrical components (V_rho, V_phi,
    V_z) do not depend on the azimuthal angle phi. Samples V on phi-rings
    at a ladder of (rho, z) and reports the worst relative spread of each
    cylindrical component across phi -- a measured quantity.

    Each component's spread is normalised by the RING'S OWN overall field
    magnitude (max|V| over the ring), not by that component's own max: a
    component that is identically zero for a genuinely axisymmetric field
    (e.g. V_phi for a pure meridional flow) is then pure roundoff on both
    the numerator and denominator, and dividing noise by noise produces an
    O(1) false-positive residual -- this was caught by running this
    function on leg 351's own swirl witness, whose V_phi is analytically
    zero, before this normalisation fix (see test_dssp_screen.py)."""
    rows = []
    max_rel = 0.0
    for rho in rhos:
        for z in zs:
            phis = np.linspace(0.0, 2.0 * np.pi, n_phi, endpoint=False)
            pts = np.stack([rho * np.cos(phis), rho * np.sin(phis),
                             np.full_like(phis, z)], axis=-1)
            V = field_fn(pts)
            cphi, sphi = np.cos(phis), np.sin(phis)
            V_rho = V[..., 0] * cphi + V[..., 1] * sphi
            V_phi = -V[..., 0] * sphi + V[..., 1] * cphi
            V_z = V[..., 2]
            ring_scale = float(max(np.max(np.linalg.norm(V, axis=-1)), scale_floor))
            row = {"rho": rho, "z": z, "ring_scale": ring_scale}
            for comp, name in ((V_rho, "V_rho"), (V_phi, "V_phi"), (V_z, "V_z")):
                spread = float(np.max(comp) - np.min(comp))
                rel = spread / ring_scale
                row[f"{name}_rel_spread_over_phi"] = rel
                max_rel = max(max_rel, rel)
            rows.append(row)
    return {"rows": rows, "max_rel_residual_over_phi": max_rel}


# =============================================================================
# The machine-read rigidity ledger
# =============================================================================

def _load_json(path):
    with open(path) as f:
        return json.load(f)


def ledger_nrs_tsai(l3_result, decay_result=None, ansatz_result=None):
    """NRS/Tsai, ORIGINAL (leg 357) TWO-WAY reading, UNCHANGED when called
    the original way -- i.e. with only l3_result: u in L^3(R^3) forces
    u = 0 for backward self-similar 3D Navier-Stokes. Machine-read directly
    against THIS candidate's OWN l3_norm_ladder() result -- not a
    transcribed summary. Every existing call site (test_dssp_screen.py,
    experiments/p2_route_dsspb7_v1.py, machine_read_ledger() below) calls
    it this way, so this branch's OUTPUT DICT IS BYTE-FOR-BYTE IDENTICAL to
    leg 357's landed code -- this is what makes leg 357's banked verdicts
    in writeup/data/p2_route_dsspb7_v1.json reproduce unmoved (leg 362's
    regression control).

    Leg 359 (writeup/data/p2_route_l3bd_v1.json, experiments/journal/
    leg_359.md) adjudicated that this L3-only reading UNDER-FIRES in one
    direction: it conflates Tsai 1998's TWO theorems (Theorem 1, the L^q
    route this L3-only test implements; and Theorem 2, the local-energy-
    estimates route, which needs only decay-at-infinity, no L^q membership
    at all) into one binary EXCLUDED/NOT-EXCLUDED bit. A genuinely exact-
    self-similar candidate at THIS repo's own measured decay rate (~-1,
    log-divergent in L3) would read "NOT EXCLUDED" here even though Tsai's
    Theorem 2 decisively excludes it (leg 359 sub_question_2: "(i) REACHES
    the boundary case -- decisively, and the paper's own worked example is
    essentially this exact decay rate").

    Pass BOTH decay_result (from decays_to_zero_at_infinity()) and
    ansatz_result (from classify_ss_ansatz()) to get the CORRECTED,
    leg-362 three-way reading instead: EXCLUDED-BY-T1 / EXCLUDED-BY-T2 /
    NOT-REACHED-BY-ANSATZ. See _ledger_nrs_tsai_three_way() below for the
    quoted deciding clauses."""
    if decay_result is not None and ansatz_result is not None:
        return _ledger_nrs_tsai_three_way(l3_result, decay_result, ansatz_result)
    if l3_result["converged"] and np.isfinite(l3_result["L3_norm"]):
        return {
            "excludes": True,
            "verdict": "EXCLUDED",
            "reason": (
                f"||V||_L3(R^3) converged to {l3_result['L3_norm']!r} "
                f"(rel_change_last_step={l3_result['rel_change_last_step']!r} "
                f"< tol {l3_result['rel_tol']!r}) -- the candidate lands "
                "inside NRS/Tsai's hypothesis; if it is genuinely backward "
                "self-similar it must be trivial."
            ),
        }
    return {
        "excludes": False,
        "verdict": "NOT EXCLUDED",
        "reason": (
            f"||V||_L3(R^3) did NOT converge over the measured ladder "
            f"(rel_change_last_step={l3_result['rel_change_last_step']!r} "
            f"> tol {l3_result['rel_tol']!r}) -- the candidate is outside "
            "NRS/Tsai's hypothesis; the theorem is silent on it."
        ),
    }


# =============================================================================
# Leg 362 extension: Theorem 2 (local energy estimates) + SS/DSS ansatz
# =============================================================================
#
# Leg 359's three-part finding (experiments/journal/leg_359.md,
# writeup/data/p2_route_l3bd_v1.json), quoted verbatim at the cited primary-
# text locators, never paraphrased or re-derived here:
#
#   NRS 1996 -- the q=3 exact-L^3 result the l3_norm_ladder() test below
#   actually implements. RE-ATTRIBUTED here (leg 366, Route-LCB5, source:
#   leg 364's citation-verification finding, experiments/journal/leg_364.md
#   and writeup/data/p2_route_nrsv_v1.json): this was previously captioned
#   as "Tsai 1998 Theorem 1", but Theorem 1's own stated hypothesis range
#   q in (3,infinity] is OPEN AT 3 and explicitly excludes q=3 -- the q=3
#   case is NRS 1996's own, earlier, disjoint result, which Tsai's Theorem 1
#   deliberately does NOT re-prove. NRS 1996 itself (Necas, J., Ruzicka, M.
#   & Sverak, V., "On Leray's self-similar solutions of the Navier-Stokes
#   equations," Acta Math. 176 (1996) 283-294) remains genuinely paywalled/
#   unobtainable (three independent refusal-to-obtain attempts: legs 253,
#   359, 364) -- this attribution is attested SECONDHAND at two independent
#   obtainable sources:
#     "The main result of [NRS] is that the only weak solution of (1.3)
#     belonging to L^3(R^3) is U == 0." (Tsai 1998, p.30, restating NRS
#     1996's own result, immediately before stating his own disjoint
#     Theorem 1)
#     "His original problem ... was excluded in Necas, Ruzicka, and Sverak
#     in [35]. ... Tsai proved a localized non-existence result in [38] for
#     solutions v satisfying v(t) in L^q(R^3), 3 < q <= infinity ..."
#     (Bradshaw & Tsai survey, arXiv:1802.00038, p.3)
#   Tsai's OWN Theorem 1 (Tsai 1998, p.30), quoted here for contrast since
#   it is the theorem the ledger used to (mis-)cite for this test:
#     "Theorem 1. If a weak solution U of (1.3) belongs to L^q(R^3), for
#     some q in (3,infinity], then it must be constant (and hence
#     identically zero if q < infinity)."
#
#   Theorem 2 (Tsai 1998, p.30-31):
#     "Theorem 2. Suppose u is a weak solution of (1.1) satisfying the
#     local energy estimates (1.4) in the cylinder Q_1(0,T). If u is of
#     the form (1.2)_1, then u is identically zero."
#     -- with the headline motivating corollary, decay (1.5):
#     "A particular corollary of these results is that a weak solution U
#     of (1.3) with the decay (1.5) must be zero," where (1.5) is
#     "U(y) = A(y/|y|) * 1/|y| + o(1/|y|) as y -> infinity" (p.31).
#     The finishing step needs only "U -> 0 at infinity" (p.49: "Since
#     U in L^q(R^3) in Theorem 1 [and] U -> 0 at infinity in Theorem 2,
#     the usual Liouville theorem implies U_i = 0") -- NO integrability
#     anywhere in Theorem 2's hypothesis or finish.
#
#   The ansatz gate, binding BOTH theorems (Tsai 1998, eq (1.2), p.29-30,
#   Leray's backward self-similar ansatz -- "Leray's (backward) self-
#   similar solutions are of the form u(x,t) = ..."): both Theorem 1 and
#   Theorem 2 are stated "If u is of the form (1.2)_1" -- a SINGLE
#   stationary profile U under one rescaling parameter a. Leg 359, reading
#   Theorem 2's proof (Section 4-5) at primary text directly: "Both
#   Theorem 1 and Theorem 2 require SS ansatz (1.2); neither [is] stated
#   for, nor... obviously extends to, DSS ansatz." A candidate that is
#   DISCRETELY self-similar (a periodic-in-log-time orbit at some lambda
#   > 1, not a fixed point of the rescaled flow) therefore fails the
#   hypothesis of BOTH theorems, regardless of its decay or L^q status.
# =============================================================================

def decays_to_zero_at_infinity(decay_result, tol=0.0):
    """Tests Theorem 2's finishing-step hypothesis directly: "U -> 0 at
    infinity" (Tsai 1998, p.49, quoted above) -- strictly weaker than any
    L^q/integrability condition (Theorem 1's finish). Reuses
    fitted_far_field_decay_exponent()'s own measurement rather than
    re-sampling: a strictly negative fitted exponent, CONFIRMED by the
    sampled magnitude actually decreasing from the first to the last
    sampled radius (not merely a negative least-squares slope on noisy or
    non-monotonic data), is read as U -> 0 at infinity."""
    mags = decay_result["magnitudes"]
    exponent = decay_result["fitted_exponent"]
    monotonic_decrease = bool(mags[-1] < mags[0])
    decays = bool(exponent < -tol and monotonic_decrease)
    return {
        "decays_to_zero": decays,
        "fitted_exponent": exponent,
        "magnitude_first_sample": mags[0],
        "magnitude_last_sample": mags[-1],
        "reason": (
            f"fitted far-field exponent {exponent!r} "
            f"{'< 0' if exponent < -tol else '>= 0'} and sampled |V| "
            f"{'decreases' if monotonic_decrease else 'does NOT decrease'} "
            f"from {mags[0]!r} (r_min) to {mags[-1]!r} (r_max) -- "
            + ("Theorem 2's finishing-step hypothesis \"U -> 0 at "
               "infinity\" (Tsai 1998, p.49) is satisfied by this "
               "measurement" if decays else
               "Theorem 2's finishing-step hypothesis \"U -> 0 at "
               "infinity\" (Tsai 1998, p.49) is NOT confirmed by this "
               "measurement")
        ),
    }


def classify_ss_ansatz(lambda_result):
    """Classifies whether a candidate satisfies Tsai 1998's exact
    self-similar ansatz (1.2)_1 -- a single stationary profile U under one
    rescaling parameter a, which BOTH Theorem 1 and Theorem 2 require --
    or is instead DISCRETELY self-similar at some lambda > 1 (a genuinely
    periodic-in-log-time orbit, NOT a fixed point of the rescaled flow),
    which fails the hypothesis of both theorems regardless of decay or
    L^q status (leg 359's confirmed reading of Tsai 1998 Sections 4-5,
    quoted in this module's header comment above).

    Driven off the SAME lambda_result that ledger_pineau_vicol() already
    consumes (lambda_from_trajectory()'s output) -- this is the repo's
    only landed operational signature of "periodic return under the
    rescaled flow" (leg 330's own S0 = 2*log(lambda) convention). A
    MEASURED non-trivial period at lambda > 1 IS the DSS-not-SS signature
    (a fixed point of the rescaled flow has, by definition, no period to
    find). No trajectory measured at all (a static candidate field, or one
    that was never handed a trajectory to test) is read as the exact-SS
    case: Tsai's ansatz (1.2)_1 literally IS "hand me a single stationary
    profile U(y)", which is exactly what a static field represents -- this
    module does not invent a third state for "maybe secretly DSS but never
    measured"; if a caller wants that possibility screened, it must supply
    s_vals/c_vals to lambda_from_trajectory() first."""
    if not lambda_result.get("measured", False):
        return {
            "ansatz": "EXACT-SS",
            "satisfies_theorem_ansatz": True,
            "measured_lambda": None,
            "reason": (
                "no non-trivial period was measured for this candidate "
                f"({lambda_result.get('reason', 'no trajectory supplied')}); "
                "Tsai 1998's ansatz (1.2)_1 describes a SINGLE stationary "
                "profile U under one rescaling parameter a, exactly what a "
                "static (or non-periodic) candidate with no measured "
                "periodic orbit represents"
            ),
        }
    lam = lambda_result.get("lambda")
    if lam is not None and lam > 1.0:
        return {
            "ansatz": "DSS",
            "satisfies_theorem_ansatz": False,
            "measured_lambda": lam,
            "reason": (
                f"a non-trivial return to the initial amplitude was "
                f"measured (S0={lambda_result['S0']!r}, "
                f"lambda={lam!r} > 1) -- a genuinely DISCRETELY "
                "self-similar, periodic-in-log-time orbit, NOT a fixed "
                "point of the rescaled flow, so NOT expressible as Tsai "
                "1998's ansatz (1.2)_1's single stationary profile U "
                "under one parameter a; both Theorem 1 and Theorem 2 "
                "require this ansatz (leg 359's confirmed reading of "
                "Tsai 1998 Sections 4-5), so NEITHER theorem's hypothesis "
                "is met, regardless of decay or L^q status"
            ),
        }
    return {
        "ansatz": "UNKNOWN",
        "satisfies_theorem_ansatz": None,
        "measured_lambda": lam,
        "reason": (
            f"a period was measured but its lambda={lam!r} is outside "
            "the expected DSS-at-lambda>1 range (or undefined); this "
            "module does not guess, it flags for the next adjudicating "
            "leg rather than auto-classifying"
        ),
    }


def _ledger_nrs_tsai_three_way(l3_result, decay_result, ansatz_result):
    """The leg-362 corrected reading: EXCLUDED-BY-T1 / EXCLUDED-BY-T2 /
    NOT-REACHED-BY-ANSATZ. The ansatz gate is checked FIRST and is
    dispositive on its own -- per leg 359's finding, BOTH theorems require
    the exact-SS ansatz (1.2)_1, so a candidate that fails it is not
    reached by either theorem regardless of its decay or L^q status. Only
    a candidate that passes the ansatz gate is then checked against
    Theorem 1's stricter L^q route, and failing that, Theorem 2's weaker
    decay-only route."""
    ansatz_ok = ansatz_result.get("satisfies_theorem_ansatz")
    if ansatz_ok is not True:
        return {
            "excludes": False,
            "verdict": "NOT-REACHED-BY-ANSATZ",
            "reason": (
                "neither theorem's hypothesis is met: " + ansatz_result["reason"]
            ),
            "deciding_clause": (
                "Tsai 1998, eq (1.2), p.29-30: both Theorem 1 and Theorem 2 "
                "are stated \"If u is of the form (1.2)_1\" -- Leray's "
                "EXACT (continuous) backward self-similar ansatz"
            ),
            "ansatz_detail": ansatz_result,
        }
    l3_excludes = bool(l3_result["converged"] and np.isfinite(l3_result["L3_norm"]))
    if l3_excludes:
        return {
            "excludes": True,
            "verdict": "EXCLUDED-BY-T1",
            "reason": (
                f"||V||_L3(R^3) converged to {l3_result['L3_norm']!r} "
                f"(rel_change_last_step={l3_result['rel_change_last_step']!r} "
                f"< tol {l3_result['rel_tol']!r}) and the candidate "
                "satisfies the exact-SS ansatz -- inside Theorem 1's "
                "hypothesis, so it must be trivial if genuinely backward "
                "self-similar."
            ),
            "deciding_clause": (
                # RE-ATTRIBUTED (leg 366, Route-LCB5, source: leg 364's
                # citation-verification finding, experiments/journal/
                # leg_364.md and writeup/data/p2_route_nrsv_v1.json): this
                # q=3 exact-L^3 test is NRS 1996's own result, not Tsai
                # 1998 Theorem 1 (whose stated range q in (3,infinity]
                # excludes q=3). NRS 1996 itself remains genuinely
                # paywalled/unobtainable; attested secondhand at two
                # independent obtainable sources (see the header comment
                # above for both quotes in full).
                "NRS 1996 (Necas, Ruzicka & Sverak, Acta Math. 176 (1996) "
                "283-294) -- the q=3 exact-L^3 result, attested secondhand "
                "(NRS 1996 itself unobtainable) via Tsai 1998, p.30: \"The "
                "main result of [NRS] is that the only weak solution of "
                "(1.3) belonging to L^3(R^3) is U == 0.\"; and Bradshaw & "
                "Tsai survey, arXiv:1802.00038, p.3: \"...was excluded in "
                "Necas, Ruzicka, and Sverak in [35].\" NOT Tsai 1998's own "
                "Theorem 1, whose stated range q in (3,infinity] excludes "
                "q=3."
            ),
            "ansatz_detail": ansatz_result,
        }
    decay_excludes = bool(decay_result["decays_to_zero"])
    if decay_excludes:
        return {
            "excludes": True,
            "verdict": "EXCLUDED-BY-T2",
            "reason": (
                "||V||_L3(R^3) did NOT converge (outside Theorem 1's "
                "hypothesis) but the candidate satisfies the exact-SS "
                "ansatz AND decays to 0 at infinity -- " + decay_result["reason"]
            ),
            "deciding_clause": (
                "Tsai 1998, p.30-31: \"Theorem 2. Suppose u is a weak "
                "solution of (1.1) satisfying the local energy estimates "
                "(1.4) in the cylinder Q_1(0,T). If u is of the form "
                "(1.2)_1, then u is identically zero.\" Finishing step "
                "(p.49): \"...U -> 0 at infinity in Theorem 2, the usual "
                "Liouville theorem implies U_i = 0\" -- no L^q/"
                "integrability required. Headline corollary (p.31): "
                "\"A particular corollary of these results is that a weak "
                "solution U of (1.3) with the decay (1.5) must be zero,\" "
                "(1.5): \"U(y) = A(y/|y|) * 1/|y| + o(1/|y|) as "
                "y -> infinity.\""
            ),
            "ansatz_detail": ansatz_result,
            "decay_detail": decay_result,
        }
    return {
        "excludes": False,
        "verdict": "NOT EXCLUDED",
        "reason": (
            "the candidate satisfies the exact-SS ansatz but neither "
            "Theorem 1 (L^q) nor Theorem 2 (decays_to_zero_at_infinity) "
            "fired on this measurement -- the theorems are silent on it"
        ),
        "ansatz_detail": ansatz_result,
        "decay_detail": decay_result,
    }


# =============================================================================
# Leg 370 extension: Theorem 1.2 (Morrey space Ṁq,1) -- the third exact-SS
# ledger entry
# =============================================================================
#
# Leg 368's WIDENS finding (experiments/journal/leg_368.md, writeup/data/
# p2_route_mryx_v1.json), full-text-read against arXiv:2006.15776 (Jiu-Wang-
# Wei, "Leray's backward self-similar solutions to the 3D Navier-Stokes
# equations in Morrey spaces"), quoted verbatim at the cited primary-text
# locators, never paraphrased or re-derived here:
#
#   Morrey norm (Sec 2.1), quoted verbatim: "||f||_{Ṁp,l(Ω)} = sup_{R>0}
#   sup_{x∈Ω} [ R^{3(1/p−1/l)} ∫_{Bx(R)∩Ω} |f(y)|^l dy ]^{1/l}". This is a
#   purely averaged, ball-integral (Lebesgue-measure) scaling condition -- it
#   has NO pointwise-decay content at all. For l=1 (the case Theorem 1.2
#   uses): ||f||_{Ṁq,1} = sup_{R>0} sup_x [ R^{3(1/q−1)} ∫_{Bx(R)} |f(y)| dy ].
#
#   Embedding chain (eq 1.6), quoted verbatim: "we hold the following
#   embedding relation L^q(R³) ↪ L^{q,∞}(R³) ↪ Ṁq,l(R³) ↪ Ṁq,1(R³), 1 ≤ l <
#   q. This fact can be found in [5]." Ṁq,1 is the LARGEST (weakest-
#   hypothesis) space in the entire chain for fixed q, strictly containing
#   L^q.
#
#   Theorem 1.2, quoted verbatim: "Let U ∈ W^{1,2}_loc(R³) be a weak solution
#   of (1.3). If U ∈ Ṁq,1(R³) with 3/2 < q < 6, (1.10), then U ≡ 0."
#
#   Ansatz check, quoted verbatim (leg 368): "Every theorem and every proof
#   step is stated 'If u is of the form (1.2)' -- Leray's exact backward
#   self-similar ansatz, the same gate as Tsai/NRS/Chae-Wolf's exact-SS
#   work. No DSS content anywhere in the primary text." Theorem 1.2's
#   hypothesis, like T1's and T2's, therefore requires the exact-SS ansatz
#   (1.2)_1 -- the SAME gate applied to T1/T2 above applies here, checked
#   FIRST, exactly as for T1/T2.
#
#   Leg 368's own scoping (quoted): "an exact-SS weak solution U that is (a)
#   NOT in L³(R³) (T1 reads NOT-EXCLUDED) AND (b) fails the screen's single-
#   generic-ray fitted-exponent-and-monotonic-decrease test (T2 reads NOT-
#   EXCLUDED ...) BUT whose ball-averaged mass on growing balls is
#   nonetheless controlled at the critical Ṁq,1 scaling rate ... is excluded
#   by Theorem 1.2 and evades both of the screen's current encoded tests."
#   This is the WIDENS gap this extension operationalizes.
# =============================================================================

def _l1_ball_integral_ladder(field_fn, R_hi_ladder, inner_R=1e-6,
                              n_r=300, n_c=48, n_phi=16):
    """Cumulative Int_{B_R(0)} |V(y)| dy over the SAME shell ladder and the
    SAME quadrature convention l3_norm_ladder() already uses (reuses
    _spherical_shell_nodes() directly) -- power 1 (|V|, an L^1-type
    integrand), not power 3 (|V|^3, l3_norm_shell()'s integrand). This is
    the ball-integral half of the Ṁq,1 seminorm's sup_R [...] bracket,
    R^{3(1/q-1)} Int_{B_R(0)} |f(y)| dy, evaluated at x=0 -- the candidate's
    own natural center, the same convention l3_norm_ladder() uses for its
    R^3 quadrature (see morrey_ball_average_sweep()'s docstring for the
    resulting, STATED scope limitation: x=0 only, not the theorem's literal
    sup over all x in R^3)."""
    rows = []
    cum = 0.0
    prev_R = inner_R
    for R in R_hi_ladder:
        pts, w = _spherical_shell_nodes(prev_R, R, n_r, n_c, n_phi)
        V = field_fn(pts)
        mag1 = np.linalg.norm(V, axis=-1)
        shell = float(np.sum(w * mag1))
        cum += shell
        rows.append({"R_hi": R, "shell_integral_l1": shell, "cumulative_l1": cum})
        prev_R = R
    return rows


def morrey_ball_average_sweep(field_fn, q_values=None,
                               R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                               inner_R=1e-6, rel_tol=1e-2,
                               n_r=300, n_c=48, n_phi=16):
    """Operationalizes Theorem 1.2's hypothesis U in Ṁq,1(R^3), 3/2 < q < 6
    (quoted verbatim in the module comment above) as a genuine numerical
    test, at the candidate's own resolution -- REUSING l3_norm_ladder()'s
    own shell-ladder machinery (_spherical_shell_nodes(), the same R_hi
    ladder and n_r/n_c/n_phi quadrature resolution) rather than inventing a
    second discretization convention.

    ||f||_{Ṁq,1} = sup_{R>0} sup_x [ R^{3(1/q-1)} Int_{B_x(R)} |f(y)| dy ]
    (l=1 specialization of the module comment's quoted Sec 2.1 definition).
    This ball-averaged seminorm has NO pointwise-decay requirement -- it is
    a purely Lebesgue-integral quantity, unlike T2's single-ray fitted-decay
    proxy, and it is a strictly weaker (larger-class) membership test than
    T1's global L^3 convergence by the quoted embedding chain (eq 1.6).

    Operationally: sup_x is evaluated at x=0 ONLY (the candidate's own
    natural center -- the SAME scope l3_norm_ladder() already uses for its
    quadrature, not the theorem's literal sup over uncountably many x in
    R^3), and sup_R is evaluated over the SAME finite R ladder
    l3_norm_ladder() uses, for a finite sweep of q values densely sampled
    across the OPEN interval (3/2, 6) (excluding both endpoints, matching
    the theorem's own strict range). Membership is reported TRUE iff ANY
    swept q gives a ladder that does not diverge (a non-increasing log-log
    trend over the ladder, the same "measurement, not an error" convention
    l3_norm_ladder()'s own convergence check uses).

    THIS IS A GENUINE AT-RESOLUTION NUMERICAL TEST, NOT A PLACEHOLDER, BUT
    IT IS NOT A LITERAL, EXHAUSTIVE COMPUTATION OF THE THEOREM'S HYPOTHESIS
    SPACE: a candidate could in principle be excluded by Theorem 1.2 at some
    off-origin x this sweep never samples, or at some q value strictly
    between the swept grid points. This is a KNOWN, STATED limitation of
    this specific operationalization -- not a claim that surviving this
    sweep proves the candidate is genuinely outside Ṁq,1 for every q and
    every x."""
    ball_ladder = _l1_ball_integral_ladder(field_fn, R_hi_ladder, inner_R,
                                            n_r, n_c, n_phi)
    R_arr = np.array([row["R_hi"] for row in ball_ladder], dtype=float)
    I_arr = np.array([row["cumulative_l1"] for row in ball_ladder], dtype=float)
    if q_values is None:
        # densely sampled OPEN interval (3/2, 6), endpoints excluded to
        # match the theorem's own strict range "3/2 < q < 6"
        q_values = np.linspace(1.5, 6.0, 26)[1:-1]
    else:
        q_values = np.asarray(q_values, dtype=float)

    per_q = []
    any_bounded = False
    best_q = None
    best_slope = None
    for q in q_values:
        e_q = 3.0 * (1.0 / q - 1.0)
        morrey_vals = (R_arr ** e_q) * I_arr
        safe = np.maximum(morrey_vals, 1e-300)
        slope, _ = np.polyfit(np.log(R_arr), np.log(safe), 1)
        # a non-increasing (or flat) trend across the ladder means the
        # ball-averaged seminorm is NOT diverging as R grows -- a bounded
        # sup, i.e. Theorem 1.2's Ṁq,1 membership condition at this q. The
        # SAME rel_tol-on-the-tail convention l3_norm_ladder()'s own
        # `converged` flag uses (relative change of the LAST step), applied
        # to the boundedness direction instead of the convergence direction.
        last_vs_first = bool(morrey_vals[-1] <= morrey_vals[0] * (1.0 + rel_tol))
        bounded = bool(slope <= rel_tol and last_vs_first
                        and np.all(np.isfinite(morrey_vals)))
        per_q.append({
            "q": float(q),
            "morrey_exponent_e_q": float(e_q),
            "morrey_values_over_ladder": morrey_vals.tolist(),
            "fitted_loglog_slope": float(slope),
            "bounded": bounded,
        })
        if bounded and not any_bounded:
            any_bounded = True
            best_q = float(q)
            best_slope = float(slope)

    return {
        "in_morrey_class": any_bounded,
        "witnessing_q": best_q,
        "witnessing_slope": best_slope,
        "q_values_swept": [float(q) for q in q_values],
        "per_q": per_q,
        "R_hi_ladder": list(R_hi_ladder),
        "ball_integral_ladder": ball_ladder,
        "reason": (
            f"swept {len(q_values)} q values in the open interval (3/2, 6) "
            "at x=0; "
            + (f"q={best_q!r} gives a bounded ball-averaged Ṁq,1 seminorm "
               f"over the ladder (fitted log-log slope {best_slope!r} <= "
               f"tol {rel_tol!r})" if any_bounded else
               "no swept q gave a bounded ladder over this ball ladder "
               "(fitted log-log slope stayed positive / the seminorm grew "
               "for every sampled q)")
        ),
    }


def ledger_morrey(morrey_result, ansatz_result):
    """The third exact-SS ledger entry: Theorem 1.2 (Jiu-Wang-Wei,
    arXiv:2006.15776), operationalized above. The ansatz gate is checked
    FIRST and is dispositive on its own, EXACTLY as _ledger_nrs_tsai_
    three_way() already does for T1/T2 -- per leg 368's confirmed reading,
    Theorem 1.2 is likewise stated only "If u is of the form (1.2)" (quoted
    in the module comment above), so a candidate that fails the exact-SS
    ansatz is not reached by this theorem either, regardless of its Ṁq,1
    membership."""
    ansatz_ok = ansatz_result.get("satisfies_theorem_ansatz")
    if ansatz_ok is not True:
        return {
            "excludes": False,
            "verdict": "NOT-REACHED-BY-ANSATZ",
            "reason": (
                "Theorem 1.2's hypothesis is not met: " + ansatz_result["reason"]
            ),
            "deciding_clause": (
                "leg 368 (experiments/journal/leg_368.md), quoted verbatim: "
                "\"Every theorem and every proof step is stated 'If u is of "
                "the form (1.2)' -- Leray's exact backward self-similar "
                "ansatz, the same gate as Tsai/NRS/Chae-Wolf's exact-SS "
                "work. No DSS content anywhere in the primary text.\""
            ),
            "ansatz_detail": ansatz_result,
        }
    if morrey_result["in_morrey_class"]:
        return {
            "excludes": True,
            "verdict": "EXCLUDED-BY-MORREY",
            "reason": (
                "the candidate satisfies the exact-SS ansatz and its "
                "ball-averaged L^1 mass over growing balls is bounded at "
                f"the Ṁq,1 scaling rate for q={morrey_result['witnessing_q']!r} "
                "-- " + morrey_result["reason"]
            ),
            "deciding_clause": (
                "leg 368 (experiments/journal/leg_368.md), quoting "
                "arXiv:2006.15776 (Jiu-Wang-Wei) verbatim -- Theorem 1.2: "
                "\"Let U ∈ W^{1,2}_loc(R³) be a weak solution of (1.3). If "
                "U ∈ Ṁq,1(R³) with 3/2 < q < 6, (1.10), then U ≡ 0.\" "
                "Embedding chain (eq 1.6): \"we hold the following "
                "embedding relation L^q(R³) ↪ L^{q,∞}(R³) ↪ Ṁq,l(R³) ↪ "
                "Ṁq,1(R³), 1 ≤ l < q. This fact can be found in [5].\" "
                "Ṁq,1 definition (Sec 2.1, l=1 specialization): "
                "\"||f||_{Ṁp,l(Ω)} = sup_{R>0} sup_{x∈Ω} [ R^{3(1/p−1/l)} "
                "∫_{Bx(R)∩Ω} |f(y)|^l dy ]^{1/l}\"."
            ),
            "ansatz_detail": ansatz_result,
            "morrey_detail": morrey_result,
        }
    return {
        "excludes": False,
        "verdict": "NOT EXCLUDED",
        "reason": (
            "the candidate satisfies the exact-SS ansatz but no swept q in "
            "(3/2, 6) gave a bounded Ṁq,1 seminorm over the measured "
            "ladder -- " + morrey_result["reason"]
        ),
        "ansatz_detail": ansatz_result,
        "morrey_detail": morrey_result,
    }


def ledger_chae_tsai(ctrx_path=CTRX_JSON):
    """Parses leg 326's landed record (writeup/data/p2_route_ctrx_v1.json)
    programmatically. Chae-Tsai's hypothesis is the rescaled EULER system
    (1.6); every DSSP-family candidate here solves rescaled NAVIER-STOKES
    ((*) in solver/dssp_step.py), so this entry's verdict does not depend
    on the specific candidate -- it depends only on which equation the
    candidate solves, read from leg 326's own clause ledger."""
    d = _load_json(ctrx_path)
    gate = d["gate"]
    clause = gate["clause_ledger"]["alpha_equation"]
    silent = bool(clause["verdict"] == "FAILS_HYPOTHESIS" and gate["branch"] == "(ii)")
    return {
        "excludes": False if silent else None,
        "verdict": gate["verdict"],
        "branch": gate["branch"],
        "clause_alpha_equation_verdict": clause["verdict"],
        "clause_alpha_equation_reason": clause["reason"],
        "consumed_from": ctrx_path,
        "consumed_leg": d["leg"],
    }


def ledger_pineau_vicol(lambda_result, pvlx_path=PVLX_JSON):
    """Parses leg 330's landed record (writeup/data/p2_route_pvlx_v1.json)
    programmatically: the H5 clause (the deciding clause, 1 < lambda <
    lambda_underline) and the WLOG ceiling on lambda_underline (M1,
    value_lambda_ceiling). Compares that ceiling against the CANDIDATE's
    own measured lambda from lambda_from_trajectory(), not a hardcoded
    number."""
    d = _load_json(pvlx_path)
    h5 = next(c for c in d["clause_by_clause"] if c["id"] == "H5")
    m1 = next(m for m in d["magnitudes_of_near_1"] if m["id"] == "M1")
    lam_ceiling = m1["value_lambda_ceiling"]
    lam = lambda_result.get("lambda")
    if lam is None:
        return {
            "excludes": False,
            "verdict": "NOT APPLICABLE",
            "reason": (
                "no lambda was measured for this candidate "
                f"({lambda_result.get('reason')}); Pineau-Vicol's H5 "
                "hypothesis (1 < lambda < lambda_underline) cannot be "
                "evaluated without a measured lambda"
            ),
            "lambda_ceiling_from_source": lam_ceiling,
            "deciding_clause_h5": h5,
            "consumed_from": pvlx_path,
            "consumed_leg": d["leg"],
        }
    inside_ceiling = bool(1.0 < lam < lam_ceiling)
    if not inside_ceiling:
        return {
            "excludes": False,
            "verdict": "OUTSIDE Pineau-Vicol's lambda window -- theorem silent",
            "reason": (
                f"measured lambda={lam!r} is outside (1, {lam_ceiling!r}), "
                "the paper's own WLOG ceiling on lambda_underline; H5's "
                "hypothesis fails for this candidate exactly as leg 330 "
                "found for NS3D-DSS-NONAXI-LAMBDA-LARGE"
            ),
            "measured_lambda": lam,
            "lambda_ceiling_from_source": lam_ceiling,
            "deciding_clause_h5": h5,
            "consumed_from": pvlx_path,
            "consumed_leg": d["leg"],
        }
    return {
        "excludes": None,
        "verdict": "INSIDE the WLOG lambda ceiling -- re-adjudication needed",
        "reason": (
            f"measured lambda={lam!r} is inside (1, {lam_ceiling!r}); "
            "lambda_underline's EXACT value is data-dependent (a function "
            "of C_{U,0}, leg 330's GAP-330-B/GAP-330-C corrections), so "
            "this module does not auto-exclude -- it flags for the next "
            "adjudicating leg rather than guessing"
        ),
        "measured_lambda": lam,
        "lambda_ceiling_from_source": lam_ceiling,
        "deciding_clause_h5": h5,
        "consumed_from": pvlx_path,
        "consumed_leg": d["leg"],
    }


def machine_read_ledger(l3_result, lambda_result, decay_result=None,
                         ansatz_result=None, morrey_result=None):
    """The full rigidity ledger for one candidate, machine-read against its
    own measurements (l3_result, lambda_result) and against legs 326/330's
    landed JSON records. `reportable` is the B7 yes-branch consequence:
    every candidate that reaches this function carries its exclusion status
    attached, whatever that status is.

    decay_result/ansatz_result are OPTIONAL (default None): omitting them
    (every existing call site does) reproduces leg 357's original
    NRS_Tsai reading byte-for-byte via ledger_nrs_tsai()'s own
    backward-compatible branch. Passing both (leg 362's extension) upgrades
    NRS_Tsai to the three-way EXCLUDED-BY-T1/EXCLUDED-BY-T2/
    NOT-REACHED-BY-ANSATZ reading -- see _ledger_nrs_tsai_three_way().

    morrey_result is ALSO OPTIONAL (default None), leg 370's extension:
    omitting it (every existing call site does) reproduces the exact same
    dict shape as before this leg -- no "Morrey" key at all, so
    set(ledger.keys()) is UNCHANGED for every existing caller. Passing it
    (requires ansatz_result to also be supplied, since ledger_morrey() gates
    on the ansatz exactly as NRS_Tsai's three-way reading does) adds a
    "Morrey" key carrying ledger_morrey()'s EXCLUDED-BY-MORREY / NOT
    EXCLUDED / NOT-REACHED-BY-ANSATZ verdict, additively."""
    ledger = {
        "NRS_Tsai": ledger_nrs_tsai(l3_result, decay_result, ansatz_result),
        "Chae_Tsai": ledger_chae_tsai(),
        "Pineau_Vicol": ledger_pineau_vicol(lambda_result),
        "reportable": True,
    }
    if morrey_result is not None and ansatz_result is not None:
        ledger["Morrey"] = ledger_morrey(morrey_result, ansatz_result)
    return ledger


def screen_candidate(field_fn, s_vals=None, c_vals=None,
                      R_hi_ladder=(10.0, 100.0, 1e3, 1e4, 1e5, 1e6),
                      n_r=300, n_c=48, n_phi=16):
    """Runs all four screen quantities on one candidate field and machine-
    reads the ledger against them. If s_vals/c_vals are not given (a static
    field with no trajectory), lambda is reported as undefined -- exactly
    what lambda_from_trajectory(None-case) would say, made explicit here so
    a caller cannot forget to think about it.

    LEG 383 (Route-ST2G) -- THE TWO COLUMNS ARE UNCONDITIONAL HERE.
    Legs 362 and 370 landed Theorem 2's decay-only route
    (decays_to_zero_at_infinity()) and the SS/DSS ansatz classifier
    (classify_ss_ansatz()) as strictly OPT-IN arguments to
    machine_read_ledger(), deliberately, so that no existing call site's
    return-dict key set moved. The side effect was that THIS function -- the
    single end-to-end path through which a candidate report is produced --
    computed `decay` and then dropped it, called machine_read_ledger(l3, lam)
    with two positional arguments, and never computed the ansatz
    classification at all. Leg 359's flagged mis-classification therefore
    stayed live in the report path after legs 362/370: measured on this
    module at 104f5b3, a planted exact-SS field with fitted exponent
    -1.0000000000000002 and a genuinely log-divergent L^3 ladder
    (rel_change_last_step 0.1305, converged False) was reported
    "NOT EXCLUDED", via leg 357's backward-compatible L^3-only branch, while
    Tsai 1998's Theorem 2 excludes it outright.

    So `theorem2_decay_to_zero` and `ss_ansatz` are now computed on EVERY
    call and passed into machine_read_ledger() on EVERY call, and they are
    returned as their own top-level report columns. machine_read_ledger()'s
    own signature and defaults are UNTOUCHED -- legs 362's and 370's
    backward-compatibility guarantees for direct callers still hold, and the
    ledger key set returned here is unchanged (no "Morrey" key: leg 370's
    Morrey sweep is a separate, much more expensive ball-average pass and
    stays opt-in at its own call site).

    Consequence, which is the whole point: this function can now return
    EXCLUDED-BY-T1, EXCLUDED-BY-T2, NOT-REACHED-BY-ANSATZ, or NOT EXCLUDED,
    and it will name the deciding clause in each case. CEILING: TIER 2 --
    a candidate that survives this screen is only "not already excluded by a
    published theorem reachable on this repository's record". That is not
    evidence for existence."""
    l3 = l3_norm_ladder(field_fn, R_hi_ladder=R_hi_ladder, n_r=n_r, n_c=n_c, n_phi=n_phi)
    decay = fitted_far_field_decay_exponent(field_fn)
    axisym = axisymmetry_residual(field_fn)
    if s_vals is None or c_vals is None:
        lam = {"lambda": None, "S0": None, "measured": False,
               "reason": "static candidate, no trajectory supplied"}
    else:
        lam = lambda_from_trajectory(s_vals, c_vals)
    theorem2 = decays_to_zero_at_infinity(decay)
    ansatz = classify_ss_ansatz(lam)
    ledger = machine_read_ledger(l3, lam, decay_result=theorem2,
                                  ansatz_result=ansatz)
    return {
        "l3_norm": l3,
        "far_field_decay": decay,
        "axisymmetry": axisym,
        "lambda": lam,
        "theorem2_decay_to_zero": theorem2,
        "ss_ansatz": ansatz,
        "ledger": ledger,
    }
