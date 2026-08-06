"""Route-WVR v1 (leg 160) — A GENUINELY DIFFERENT FITNESS *DEFINITION* FOR STAGE-B-STYLE
GA, PUT THROUGH THE FROZEN SIX-PROPERTY VIABILITY GATE.

    ***  NO GA COMPUTE RUNS IN THIS FILE, ON EITHER BRANCH OF THE GATE.  ***

`plan_of_record.py` bans "any GA compute on an unvalidated fitness", lifted by "never --
only a re-run of the six-property gate that PASSES on a repaired fitness". This module
re-runs that gate. Running the gate is not GA compute: it evaluates fitness properties on
a FIXED roster and a deterministic grid, exactly as legs 49/50/59 did. Nothing here
imports `ga/`. A PASS would MEET the ban's recorded lift condition; it would not lift it.
Lifting it is the user's call.

WHY A DEFINITIONAL CHANGE, AND WHAT THE RECORD SAYS
-----------------------------------------------------------------------------
    leg 49  4/6   P2 finite 0.775, P3 max|slope-1| 0.3656058258949979
    leg 50  4/6   1-D wall repair:  P2 0.875,  P3 0.3421493449940881
    leg 59  5/6   2-D wall repair:  P2 0.975,  P3 0.3421493449940881

P2 moved twice. **P3 did not move by one ulp between leg 50 and leg 59** -- a repair to
the weight BOX changed which weights are admissible and did not change the defect-tracking
error at all. Leg 59's own forward-pointer: any future proposal must change the fitness's
DEFINITION, not its wall model. That is what this file does.

THE THREE PRE-NAMED DEFINITIONS (fixed here BEFORE any number was computed -- leg 111's
pre-naming discipline; this file's first commit is the record)
-----------------------------------------------------------------------------
Write the incumbent as

    f_0(theta) = log10( Y_0(theta) / budget(theta) ),  budget = (1-Z_1)^2/(2 Z_2),
    Y_0(theta) = max_i w_i |(A F(z))_i|.

  IDENTITY   (control, not a candidate)  f_0 verbatim. Injected through the SAME
             substitution mechanism the candidates use, so that reproducing leg 59's
             numbers bit-for-bit certifies the mechanism before it is trusted.

  WVR-1 "COERCIVITY-ONLY"   (definitional)
             f_1(theta) = log10( 2 Z_2 / (1-Z_1)^2 ) = -log10(budget).
             Y_0 is DROPPED. The weight is scored on the norm's own coercivity -- how
             much defect the certificate could absorb -- rather than on how large the
             current numerical state's residual happens to be in that norm. This is
             DIRECTION.md's "resolution-normalized coercivity measure", and it is the
             fitness a GA searching a *certificate's norm* arguably always wanted: leg
             49's own gauge ablation put the whole 5604x of f_0 in the border rows of
             Y_0, i.e. in preconditioning, not in the space.

  WVR-2 "FLOOR-QUOTIENTED DEFECT"   (definitional)
             tau  = FLOOR_SAFETY * |A| @ |F_float64(z) - F_longdouble(z)|   (state units)
             f_2(theta) = log10( ( max_i w_i max(|(A F(z))_i| - tau_i, 0)
                                   + max_i w_i tau_i ) / budget(theta) ).
             The defect is measured ABOVE the state's own arithmetic floor,
             COMPONENTWISE, and the floor is then added back once as an explicit,
             defect-independent anchor so the fitness stays finite and weight-dependent
             at the converged state. Both pieces are necessary and the reason is stated
             in section C3 below; `tau` is computed by each engine at ITS OWN state, so
             the definition needs no reference state and is usable by a searcher.

  WVR-3 "HIGH-PRECISION RESIDUAL"   (MECHANISM CONTROL, *not* a candidate)
             f_0 verbatim, with Y_0's residual evaluated in longdouble. NOT a
             definitional change -- a change of REALIZATION (standing discipline 70).
             It is here because it can report the other answer: if P3's residual is the
             fitness's own evaluation floor, this must move |slope-1| DOWN; if P3's
             residual is definitional, this must leave it where leg 50 and leg 59 left it.

C2 -- THE MECHANISM, AND IT IS NOT THIS LEG'S (see writeup/novelty/leg_160.md)
-----------------------------------------------------------------------------
A finite-difference probe of a noisy function has a TWO-SIDED usable window: capped above
by truncation error, floored below by the function's own noise level. That is standard
numerical-optimization knowledge -- More & Wild's ECnoise (Estimating Computational Noise,
2011) states the noise level is a lower bound on the roundoff error in f; Berahas-Byrd-
Nocedal (arXiv:2102.09762) and Shi-Xie-Xuan-Nocedal (arXiv:2110.06380) set the differencing
interval from it. This leg CITES that and does not claim it.

What is this leg's is the application. The frozen probe `defect_ladder` was repaired at the
UPPER end only (leg 50: `DEFECT_WINDOW_C = 0.1 / ||A||_w`, derived from nonlinearity) and
has NO lower cut: the grid runs to eps = 1e-11. Writing the perturbed state's Newton step as

    A F(z* + eps d)  =  eps d  +  rho  +  O(eps^2),        rho := A F(z*),

`rho` is the float64 residual mapped to state units, and the probe measures `rho` rather
than the fitness wherever eps |d_i| < |rho_i| at the component the weighted max selects.
Note the mechanism is COMPONENTWISE and the max makes it weight-selected: a weight that
puts its mass where the probe direction is small sees a floor-dominated signal. This
predicts, before any run, a tell in leg 50/59's own banked ladder: if the slope depends only on
WHICH index the weighted max selects, then weights selecting the same index must share a slope,
and the 21 resolved slopes must CLUSTER rather than spread.

    CORRECTION, recorded here because this leg got it wrong first. The prediction as
    originally written in this docstring was that the slopes would be IDENTICAL to 16
    digits, and it cited leg 59's `0.8378100167662509` as appearing twice. That is false
    and the data refutes it: leg 59's 21 finite slopes have ZERO exact duplicates, and the
    two entries in question are 0.83781001 and 0.83781002, differing in the 8th digit.
    Lesson 90's "identical numbers are a tell" does NOT apply here. What is true is the
    weaker, measured statement `slope_degeneracy` now reports: the 21 slopes fall into 10
    clusters at a relative tolerance of 1e-3. The index selection is shared; the residual
    spread is the O(eps^2) term and the budget's own eps-dependence, which differ per weight.

C3 -- WHY THE ANCHOR IN WVR-2 IS NOT OPTIONAL
-----------------------------------------------------------------------------
P1 and P5 require >= 1 and >= 2 decades of fitness SPREAD over the roster AT the converged
state. P3 requires the fitness to fall with slope exactly 1 per decade of injected defect,
on a grid reaching eps = 1e-11. A fitness positively homogeneous of degree 1 in the defect
VANISHES at the converged state, so it has no spread there and fails P1/P5 outright. Hence
any fitness satisfying P1/P5 has a nonzero floor at z*, and any such floor saturates the
ladder's small-eps end and costs P3. The two properties are in tension, and the tension is
resolved only if the floor sits BELOW the window's bottom decade. That is a quantitative,
falsifiable target -- measured in section D -- and it is what the candidates are aimed at.

FROZEN, AND UNTOUCHED BY THIS LEG
-----------------------------------------------------------------------------
Everything leg 59's TECHNICAL froze, verbatim: all six thresholds, the roster construction
(2 controls + 6 degenerates + 32 random, seed 0), the resolutions (n = 201 / 401), the
search settings (per_gene=9, refine=4), the defect grid `DEFECT_EPS_DEFAULT`, the window
constant `DEFECT_WINDOW_C = 0.1`, `DEFECT_MIN_WINDOW = 3`, the probe direction, and the
2-D wall model. NOT ONE THRESHOLD IS IMPORTED AS A LITERAL HERE -- the gate function
`solver.weight_search.six_property_gate` is executed UNMODIFIED, and the only thing this
module changes is which engine class it constructs. `solver/weight_search.py` is READ-ONLY
under this leg (DIRECTION.md leg 160 territory).

Usage:  .venv/bin/python experiments/p2_route_wvr_v1_fitness.py [--quick]
"""

import contextlib
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import weight_search as ws          # noqa: E402
from solver.weight_search import BorderedCLM, FitnessEngine   # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_wvr_v1_fitness.json")

# The one constant this leg introduces, and it is inherited, not fitted: the same
# safety factor `BorderedCLM.residual_floor` already uses to turn the measured
# float64/longdouble discrepancy into a floor. Fixed before any number was computed.
FLOOR_SAFETY = 8.0

MODES = ("identity", "coercivity", "floorquot", "hiprec")
MODE_KIND = {"identity": "control (reproduction)",
             "coercivity": "CANDIDATE (definitional)",
             "floorquot": "CANDIDATE (definitional)",
             "hiprec": "control (realization, not definitional)"}

# Leg 59's banked numbers, quoted here so the identity control has something to be
# checked against that was written down before this run (writeup/data/p2_weight_repairs_v2.json).
LEG59 = {"P2_finite_fraction": 0.975,
         "P3_max_slope_error": 0.3421493449940881,
         "P3_violations": 8,
         "P3_n_resolved": 21,
         "P1_spread_decades": 14.330842101913802,
         "n_pass": 5}


# --------------------------------------------------------------------------
# the fitness definitions
# --------------------------------------------------------------------------
class WVREngine(FitnessEngine):
    """`FitnessEngine` with the SCORE swapped and nothing else.

    Every mode reuses the parent's Jacobian, inverse, residual and box logic
    untouched; `MODE` selects the score. `identity` is byte-for-byte the parent's
    formula and exists to certify the substitution mechanism.
    """

    MODE = "identity"

    def __init__(self, problem, z, lower_wall_power=None, wall2d=None):
        super().__init__(problem, z, lower_wall_power=lower_wall_power, wall2d=wall2d)
        mode = type(self).MODE
        self.tau = None
        self.aAF_sub = None
        if mode in ("floorquot", "hiprec"):
            F_fl = problem.F(self.z)
            F_ld = np.asarray(problem._F_longdouble(self.z), dtype=float)
            self.noise = np.abs(F_fl - F_ld)
            if mode == "hiprec":
                # SAME definition, better residual. `aAF` is what `constants_many`
                # reads, so the parent's Y_0 formula is reused verbatim.
                self.aAF = np.abs(self.A @ F_ld)
            else:
                # the arithmetic floor of the residual, carried into STATE units by
                # the same A the Newton step uses -- componentwise, because the
                # contamination is componentwise
                self.tau = FLOOR_SAFETY * (self.absA @ self.noise)
                self.aAF_sub = np.maximum(self.aAF - self.tau, 0.0)

    def _weights(self, thetas):
        W = np.empty((thetas.shape[0], self.pr.N))
        for i, th in enumerate(thetas):
            W[i], _ = self.pr.weight_vector(th)
        return W

    def fitness_many(self, thetas, box=True):
        mode = type(self).MODE
        thetas = np.atleast_2d(np.asarray(thetas, dtype=float))
        Y0, Z1, Z2 = self.constants_many(thetas)
        bud = np.where(Z1 < 1.0, (1.0 - Z1) ** 2 / (2.0 * Z2), -1.0)

        if mode == "coercivity":
            num = np.ones_like(bud)                     # Y_0 dropped entirely
        elif mode == "floorquot":
            W = self._weights(thetas)
            Y0_sub = np.max(W * self.aAF_sub[None, :], axis=1)
            tau_w = np.max(W * self.tau[None, :], axis=1)
            num = Y0_sub + tau_w
        else:                                            # identity, hiprec
            num = Y0

        out = np.where((bud > 0) & (num > 0),
                       np.log10(np.abs(num) / np.abs(bud)), np.inf)
        out = np.where(np.isfinite(out), out, np.inf)
        if box:
            bad = np.array([not ws.in_box(th, self.lower_wall_power, self.wall2d)
                            for th in thetas])
            out = np.where(bad, np.inf, out)
        return out


@contextlib.contextmanager
def fitness_definition(mode):
    """Run the FROZEN gate against a different fitness DEFINITION.

    The gate, the roster, the walls, the grid search and the defect ladder are all
    executed unmodified -- they construct `weight_search.FitnessEngine` by name, and
    this swaps what that name means for the duration. Nothing in
    `solver/weight_search.py` is edited (that file is read-only under this leg), and
    no threshold is copied into this module as a literal, so a frozen constant cannot
    drift here without drifting there.
    """
    cls = type("WVREngine_" + mode, (WVREngine,), {"MODE": mode})
    old = ws.FitnessEngine
    ws.FitnessEngine = cls
    try:
        yield cls
    finally:
        ws.FitnessEngine = old


# --------------------------------------------------------------------------
# D -- the floor census and the SLOPE PREDICTION (a control that can disagree)
# --------------------------------------------------------------------------
def floor_census(problem, z_star, thetas):
    """Where each roster weight's probe window sits relative to its own floor, and
    what slope the C2 mechanism PREDICTS for it.

    The prediction is a genuine known-answer check and it can come out wrong: it
    reconstructs the ladder from the model

        A F(z* + eps d) = eps d + rho + O(eps^2),     rho = A F(z*),

    i.e. it never evaluates F at a perturbed state at all, then fits the slope in
    exactly the frozen window the real ladder uses. If the measured slopes are NOT
    reproduced, the floor is not the mechanism and this leg says so.
    """
    eng0 = FitnessEngine(problem, z_star)
    rho = eng0.A @ problem.F(z_star)                  # the floor, in state units
    d = _probe_direction(problem)

    eps = np.asarray(ws.DEFECT_EPS_DEFAULT, float)
    le = np.log10(eps)
    thetas = np.atleast_2d(np.asarray(thetas, float))
    a_norms = np.array([
        problem.certificate_constants(z_star, th, A=eng0.A, J=eng0.J)["A_norm"]
        for th in thetas])
    eps_max = ws.DEFECT_WINDOW_C / np.maximum(a_norms, 1.0)

    rows = []
    for j, th in enumerate(thetas):
        w, _ = problem.weight_vector(th)
        # the model's Y_0 ladder: max_i w_i |eps d_i + rho_i|, no PDE evaluation
        model = np.array([np.max(w * np.abs(e * d + rho)) for e in eps])
        mask = eps <= eps_max[j]
        n_win = int(mask.sum())
        resolved = bool(n_win >= ws.DEFECT_MIN_WINDOW)
        slope = (float(np.polyfit(le[mask], np.log10(model[mask]), 1)[0])
                 if resolved else float("nan"))
        wd = w * np.abs(d)
        wrho = w * np.abs(rho)
        i_max = int(np.argmax(wrho))
        # the knee: where the injected defect overtakes the floor at the selected max
        knee = float(np.max(wrho) / max(np.max(wd), 1e-300))
        rows.append({
            "n_window": n_win, "resolved": resolved,
            "eps_max": float(eps_max[j]),
            "A_norm": float(a_norms[j]),
            "floor_weighted": float(np.max(wrho)),
            "knee_eps": knee,
            "log10_knee_over_window_bottom": float(np.log10(knee / eps.min())),
            "decades_of_window_below_knee":
                float(max(0.0, min(np.log10(knee), np.log10(eps_max[j]))
                          - np.log10(eps.min()))),
            "argmax_index_of_floor": i_max,
            "predicted_slope": slope,
        })
    # WHY WVR-2 subtracts too much, measured rather than argued: the floor ESTIMATE the
    # definition can compute (tau = FLOOR_SAFETY * |A| @ |noise|, an absolute-value bound
    # with no cancellation) against the floor that is actually there (rho = A F(z*), which
    # cancels). If the ratio is large, componentwise subtraction annihilates the signal
    # before it removes the floor -- and that is a property of the ESTIMATOR, not of the
    # idea of subtracting.
    noise = np.abs(np.asarray(problem.F(z_star))
                   - np.asarray(problem._F_longdouble(z_star), dtype=float))
    tau = 8.0 * (np.abs(eng0.A) @ noise)
    ratio = tau / np.maximum(np.abs(rho), 1e-300)
    over = {
        "tau_inf": float(tau.max()),
        "rho_inf": float(np.abs(rho).max()),
        "tau_over_rho_inf": float(tau.max() / max(np.abs(rho).max(), 1e-300)),
        "median_componentwise_tau_over_rho": float(np.median(ratio)),
        "fraction_of_components_over_subtracted": float(np.mean(ratio > 1.0)),
        "note": ("tau is an absolute-value bound on a signed quantity, so it carries no "
                 "cancellation; rho does. This is the measured reason WVR-2's "
                 "componentwise subtraction is defect-blind at n=201."),
    }

    return {"over_subtraction": over,
            "rho_inf": float(np.abs(rho).max()),
            "rho_weighted_note": "rho = A F(z*), the float64 residual in state units",
            "residual_floor_of_F": float(problem.residual_floor(z_star)),
            "F_inf_at_z_star": float(np.abs(problem.F(z_star)).max()),
            "F_noise_inf": float(np.abs(np.asarray(problem.F(z_star))
                                        - np.asarray(problem._F_longdouble(z_star),
                                                     dtype=float)).max()),
            "eps_grid_bottom": float(eps.min()),
            "per_weight": rows}


def _probe_direction(problem):
    """The FROZEN probe direction, reproduced exactly as `defect_ladder` builds it."""
    rng = np.random.default_rng(7)
    d = rng.standard_normal(problem.N)
    d /= np.abs(d).max()
    return d


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------
def summarize(gate):
    p = gate["properties"]
    return {
        "verdict": gate["verdict"],
        "n_pass": int(sum(1 for v in p.values() if v["pass"])),
        "P1_spread_decades": p["P1_nonzero"]["spread_decades"],
        "P1_pass": p["P1_nonzero"]["pass"],
        "P2_finite_fraction": p["P2_finite"]["finite_fraction"],
        "P2_pass": p["P2_finite"]["pass"],
        "P3_max_slope_error": p["P3_monotone"]["max_slope_error"],
        "P3_violations": p["P3_monotone"]["violations"],
        "P3_n_resolved": p["P3_monotone"]["n_resolved"],
        "P3_n_unresolved": p["P3_monotone"]["n_unresolved"],
        "P3_pass": p["P3_monotone"]["pass"],
        "P4_spearman": p["P4_resolution_stable"]["spearman"],
        "P4_top3_overlap": p["P4_resolution_stable"]["top3_overlap"],
        "P4_pass": p["P4_resolution_stable"]["pass"],
        "P5_band_decades": p["P5_wide_band"]["band_decades"],
        "P5_pass": p["P5_wide_band"]["pass"],
        "P6_interior_margin": p["P6_nontrivial_optimum"]["interior_margin"],
        "P6_wall_cost_decades": p["P6_nontrivial_optimum"]["wall_cost_decades"],
        "P6_pass": p["P6_nontrivial_optimum"]["pass"],
        "optimum_theta": gate["optimum_box"]["theta"],
        "optimum_fitness": gate["optimum_box"]["fitness"],
    }


def run_at(n_c, n_f, frozen):
    """Every mode's gate at one resolution pair, plus the floor census there.

    `frozen=True` marks the ONE pair the gate answer is read off: n = 201 / 401, leg
    49/50/59's resolutions, unchanged. The other pair is an ABLATION and is labelled
    as one everywhere it appears -- it is not a second chance at the gate.
    """
    pc, pf = BorderedCLM(n=n_c), BorderedCLM(n=n_f)
    block = {"coarse": n_c, "fine": n_f, "is_frozen_configuration": bool(frozen),
             "summary": {}, "gates": {}}
    for mode in MODES:
        t = time.time()
        with fitness_definition(mode):
            g = ws.six_property_gate(pc, pf, wall_model="2d")
        block["gates"][mode] = g
        s = summarize(g)
        s["elapsed_s"] = time.time() - t
        s["kind"] = MODE_KIND[mode]
        block["summary"][mode] = s
        print("  n=%-4d %-11s %-30s %s  %d/6  P2=%.4f  P3=%.6f"
              % (n_c, mode, MODE_KIND[mode], g["verdict"], s["n_pass"],
                 s["P2_finite_fraction"], s["P3_max_slope_error"]))

    zc, _ = pc.newton()
    th = np.array(block["gates"]["identity"]["theta"])
    cen = floor_census(pc, zc, th)
    meas = np.array(block["gates"]["identity"]["defect_ladder"]["slopes"], dtype=float)
    pred = np.array([r["predicted_slope"] for r in cen["per_weight"]], dtype=float)
    both = np.isfinite(meas) & np.isfinite(pred)
    cen["prediction_vs_measurement"] = {
        "n_compared": int(both.sum()),
        "max_abs_diff": float(np.max(np.abs(pred[both] - meas[both]))) if both.any() else None,
        "median_abs_diff": float(np.median(np.abs(pred[both] - meas[both]))) if both.any() else None,
        "measured_max_slope_error": float(np.max(np.abs(meas[both] - 1.0))) if both.any() else None,
        "predicted_max_slope_error": float(np.max(np.abs(pred[both] - 1.0))) if both.any() else None,
        "note": ("the prediction never evaluates F at a perturbed state; it "
                 "reconstructs the ladder from rho = A F(z*) alone. Agreement means "
                 "the floor IS the mechanism; disagreement refutes C2 for this object."),
    }
    block["floor_census"] = cen

    fin = np.sort(meas[np.isfinite(meas)])
    clusters = {}
    for tol in (1e-3, 1e-5, 1e-7):
        c = 1 if fin.size else 0
        for a, b in zip(fin[:-1], fin[1:]):
            if abs(b - a) > tol * max(abs(a), 1e-30):
                c += 1
        clusters["clusters_at_rel_%g" % tol] = int(c)
    block["slope_degeneracy"] = {
        "n_finite_slopes": int(fin.size),
        "n_exact_duplicates": int(fin.size - np.unique(fin).size),
        "clusters": clusters,
        "sorted_slopes": fin.tolist(),
        "note": ("CORRECTED against this leg's own first prediction, which was that the "
                 "slopes would be identical to 16 digits: there are ZERO exact "
                 "duplicates, so lesson 90's identical-numbers tell does NOT apply. The "
                 "measured statement is the clustering above -- weights whose weighted "
                 "max selects the same component share a slope to ~3 significant "
                 "figures, and the residual spread is the O(eps^2) term plus the "
                 "budget's own eps-dependence."),
    }
    return block


def main(quick=False):
    t0 = time.time()

    out = {
        "route": "Route-WVR v1 (leg 160)",
        "question": ("Does a genuinely different fitness DEFINITION pass the FROZEN "
                     "six-property viability gate unchanged (all six, including "
                     "P2 >= 0.90 and P3 max|slope-1| <= 0.05)?"),
        "ga_run": False,
        "ga_reason": ("plan_of_record bans GA compute on an unvalidated fitness, on "
                      "EITHER branch. Nothing in this run imports ga/. A PASS would "
                      "MEET the ban's recorded lift condition; lifting it is the "
                      "user's call, not this leg's."),
        "frozen": ("thresholds, roster construction, resolutions, seed 0, per_gene 9, "
                   "refine 4, DEFECT_EPS_DEFAULT, DEFECT_WINDOW_C, DEFECT_MIN_WINDOW, "
                   "probe direction, 2-D wall model -- all unchanged from leg 50/59. "
                   "six_property_gate() is executed UNMODIFIED; only the engine class "
                   "it constructs is substituted."),
        "floor_safety": FLOOR_SAFETY,
        "definitions": MODE_KIND,
        "frozen_resolutions": {"coarse": 201, "fine": 401},
        "leg59_reference": LEG59,
    }

    print("THE GATE -- frozen configuration, n = 201 / 401:")
    out["frozen"] = out.pop("frozen")           # keep key order readable
    out["gate_run"] = run_at(201, 401, frozen=True)
    print("ABLATION -- NOT the gate, n = 101 / 151:")
    out["resolution_ablation"] = run_at(101, 151, frozen=False)
    out["resolution_ablation"]["warning"] = (
        "THIS IS NOT A SECOND CHANCE AT THE GATE. The frozen configuration is n = "
        "201/401 and the leg's answer is read off `gate_run` only. This block exists "
        "because it is the sharpest available control on the C2 mechanism: ||A||_w "
        "falls with the grid, the floor rho = A F(z*) falls with it, and the frozen "
        "eps-window's bottom does not move -- so if the floor is what P3 measures, "
        "every mode's P3 must improve here, and a fitness can 'pass' at a coarse grid "
        "while failing at the resolution the gate names. That is a statement about "
        "the probe, not a validated fitness.")

    # convenience aliases so the prose and the evidence script read off ONE place
    out["gates"] = out["gate_run"]["gates"]
    out["summary"] = out["gate_run"]["summary"]
    out["floor_census"] = out["gate_run"]["floor_census"]
    out["slope_degeneracy"] = out["gate_run"]["slope_degeneracy"]

    # the identity control, checked against leg 59's banked numbers
    ident = out["summary"]["identity"]
    out["identity_control"] = {
        "note": ("the substitution mechanism must reproduce leg 59 exactly before any "
                 "candidate is believed"),
        "checks": {k: {"leg59": v, "here": ident[k], "exact": bool(ident[k] == v)}
                   for k, v in LEG59.items() if k in ident},
    }
    out["identity_control"]["all_exact"] = all(
        c["exact"] for c in out["identity_control"]["checks"].values())

    # the C2 mechanism, read across the two resolutions -- magnitudes, not booleans
    fz, ab = out["gate_run"], out["resolution_ablation"]
    out["c2_resolution_response"] = {
        "note": ("leg 59 CORRELATED window width with slope error (Spearman -0.878) and "
                 "left it out of the frozen gate; this is the same mechanism read as a "
                 "response to a knob that moves the floor and not the window"),
        "per_mode": {
            m: {"P3_at_201": fz["summary"][m]["P3_max_slope_error"],
                "P3_at_101": ab["summary"][m]["P3_max_slope_error"],
                "improvement_factor":
                    (fz["summary"][m]["P3_max_slope_error"]
                     / max(ab["summary"][m]["P3_max_slope_error"], 1e-300)),
                "n_pass_at_201": fz["summary"][m]["n_pass"],
                "n_pass_at_101": ab["summary"][m]["n_pass"]}
            for m in MODES},
        "floor_201": fz["floor_census"]["rho_inf"],
        "floor_101": ab["floor_census"]["rho_inf"],
        "window_bottom": fz["floor_census"]["eps_grid_bottom"],
    }

    out["elapsed_s"] = time.time() - t0
    out["ceiling"] = (
        "No link of the L1->L4 chain moved. This is a property check on a FLOAT fitness "
        "over the a=0 CLM linearisation, whose profile has been closed form since CLM "
        "1985. It is not a certificate and says nothing about HL_S2_nonsymmetric. The "
        "C2 mechanism is More-Wild/Berahas-Shi's, cited not claimed "
        "(writeup/novelty/leg_160.md).")

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=False)
    print("\nwrote %s  (%.1f s)" % (OUT, out["elapsed_s"]))
    return out


if __name__ == "__main__":
    main(quick="--quick" in sys.argv)
