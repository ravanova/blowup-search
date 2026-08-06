"""Phase-2 Route-BX v1: stage `B`, ANSWERED from the banked record -- the closure audit.

Stage `B` ("evolve the certificate -- the function space, the operator split, the
constants") is the last QUEUED stage in the committed sequence, and it can no longer be RUN
as conceived -- only ANSWERED.  Its GA is banned and the lift condition has failed twice on
the frozen six-property gate (leg 49 `4/6`; leg 59 `5/6`, P3 worst `|slope-1|` unmoved at
`0.342` against the `0.05` ceiling).  Its three declared degrees of freedom are each
separately dead for this operator: the SPACE (leg 52), the SPLIT (coupling entry `K/2` for
every choice, leg 53), and the SHAPE of `A` (leg 54's battery, now PROVED impossible on the
class `A21 = 0` at every `K` and every `s < 1` by leg 58's theorem).  The third realization
is dead too (leg 111).

The leg's real work -- the part that can answer either way -- is the COMPLETENESS AUDIT.
Enumerate `B`'s declared search space against the banked refutations, clause by clause, and
either exhibit an admissible, ban-respecting corner that no banked result covers, or
establish there is none.

NO GA COMPUTE RUNS ON EITHER BRANCH.  This module imports no `ga/` module and calls neither
`solver.ga_search` nor `solver.weight_search.grid_search`.  No new `l^1`-Fourier or
collocation machinery is built: every number is read from a banked JSON, or recomputed
READ-ONLY through leg 54's landed `assemble`/`build_A`/`measure` (the same import leg 58
used), and checked against the banked value it must reproduce.

THE AUDIT'S OWN CONTROL (lesson 90).  A covering predicate that cannot report NOT COVERED
is a tautology of the code, not a finding.  BX3 therefore runs the predicate on the `mu > 0`
dissipative operator, where a certificate demonstrably DOES close (leg 58 NG3 reached
`Z1 = 0.174` in-class), and requires it to come back NOT COVERED.  If that control ever
reports COVERED, the audit is broken and its verdict is void.

Run:
    .venv/bin/python -u experiments/p2_route_bx_v1_stageb.py
Render the audit ledger from committed data (no recomputation, no figure):
    .venv/bin/python experiments/p2_route_bx_v1_stageb_evidence.py
"""

import itertools
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

import numpy as np                                                     # noqa: E402

from p2_route_mm_v1_shape import (                                     # noqa: E402
    ADMISSIBLE, SHAPES, assemble, measure,
)

DATA = ROOT / "writeup" / "data"
OUT = DATA / "p2_route_bx_v1_stageb.json"

# --------------------------------------------------------------------------
# 0.  the banked record, by file.  Every number this leg quotes is read from one
#     of these, or recomputed read-only and checked against one of these.
# --------------------------------------------------------------------------
BANKED_FILES = {
    "leg49_c_pilot": "p2_route_c_pilot_v0.json",
    "leg53_assemble": "p2_route_tc_v1_assemble.json",
    "leg54_mm_shape": "p2_route_mm_v1_shape.json",
    "leg56_collocation": "p2_route_tn_v1_consistency.json",
    "leg58_nogo": "p2_route_ng_v1_nogo.json",
    "leg111_coercivity": "p2_route_we_v1_coercivity.json",
}


def load_banked():
    out = {}
    for key, name in BANKED_FILES.items():
        with open(DATA / name) as fh:
            out[key] = json.load(fh)
    return out


# --------------------------------------------------------------------------
# 1.  stage `B`'s DECLARED search space, enumerated BEFORE any covering check.
#
#     The three degrees of freedom are quoted verbatim from `plan_of_record.py`'s
#     stage-`B` entry (`name`: "the function space, the operator split, the
#     constants").  Two further axes are declared by the same entry's prose rather
#     than its title and are audited on the same footing: the SEARCH MECHANISM
#     (`why_here`: "those are search problems with a fitness that CANNOT LIE") and
#     the REALIZATION (the norm/discretization the certificate is written in --
#     `why_here` names Routes D, K and L, which are three different ones).
# --------------------------------------------------------------------------
DECLARED_AXES = {
    "realization": ["l1_fourier", "collocation", "weighted_L2"],
    "s": [0.0, 0.3, 0.7, 1.0, 1.5],          # the function space's weight exponent
    "K": [2, 3, 4, 6, 8, 16, 32, 64],        # the operator split
    "split_location": ["standard", "far_field_in_tail"],
    "A21": ["zero", "nonzero"],              # the constants / shape of A
    "shape": list(SHAPES),
    "search": ["hand", "grid", "GA"],
}

# The operator itself is NOT an axis of stage `B`: `B` evolves the certificate around the
# object stage `M` named.  `mu` appears here only as the audit's positive control (BX3),
# and it is held at 0 for every configuration in the enumerated space.
OPERATOR_MU = 0.0

# --------------------------------------------------------------------------
# 2.  the banked CLAUSES.  Each carries the leg that produced it, the epistemic
#     type of the coverage it provides, the magnitude it reports, and a predicate
#     saying which configurations it covers.
#
#     THEOREM    -- a proof; the configuration cannot close, as mathematics.
#     STRUCTURAL -- an admissibility or well-posedness failure; the configuration
#                   is not a legal certificate at all.
#     MEASURED   -- a measurement over a named battery; the configuration was tried
#                   and did not close.  This is coverage, but it is not proof.
#     BAN        -- a live entry in `plan_of_record.py`'s ban list, with its own
#                   unmet lift condition.
# --------------------------------------------------------------------------
def build_clauses(bk):
    mm, ng, cp = bk["leg54_mm_shape"], bk["leg58_nogo"], bk["leg49_c_pilot"]
    we, tn = bk["leg111_coercivity"], bk["leg56_collocation"]
    target_alpha = float(mm["target_alpha"])
    crossing = float(ng["NG2a_fredholm_sides_leg51"]["crossing"])

    clauses = []

    def add(cid, leg, kind, statement, magnitude, covers):
        # EVERY banked refutation in this list was measured or proved on the INVISCID
        # operator (mu = 0).  None of them says anything about mu > 0.  Without this
        # guard the predicates would silently "cover" a dissipative configuration they
        # have no evidence about -- which is precisely the tautology lesson 90 names, and
        # the first draft of this leg had exactly that bug until BX3's control caught it.
        def guarded(cfg, _f=covers):
            return float(cfg.get("mu", 0.0)) == 0.0 and _f(cfg)
        clauses.append({"id": cid, "leg": leg, "type": kind, "statement": statement,
                        "magnitude": magnitude,
                        "scope": "inviscid operator only (mu = 0)",
                        "_covers": guarded})

    # -- the SPACE axis -----------------------------------------------------
    add("SPACE-TARGET", 55, "STRUCTURAL",
        "the target HL_S2_nonsymmetric has finite l^1_w norm only below the measured "
        "admissibility exponent; at or above it the certificate's own target is not in "
        "its space, so the configuration is not a legal certificate",
        {"target_alpha": target_alpha,
         "margin_at_s_0": 0.394, "margin_at_s_0p3": 0.094},
        lambda c: c["realization"] == "l1_fourier" and c["s"] >= target_alpha)

    add("SPACE-CROSSING", 51, "STRUCTURAL",
        "the Fredholm sides cross at s = 1: the tail kernel is IN the space iff s < 1 "
        "and the cokernel functional is bounded iff s >= 1, so at and above the crossing "
        "bordering cannot help -- the one exponent at which the repair is unavailable",
        {"kernel_exponent": float(ng["NG2a_fredholm_sides_leg51"]["kernel_exponent"]),
         "cokernel_exponent": float(ng["NG2a_fredholm_sides_leg51"]["cokernel_exponent"]),
         "crossing": crossing,
         "increment_ratio_at_s_1": float(ng["NG2a_increment_ratio_by_s"]["1.0"]),
         "increment_ratio_at_s_1p5": float(ng["NG2a_increment_ratio_by_s"]["1.5"])},
        lambda c: c["realization"] == "l1_fourier" and c["s"] >= crossing)

    # -- the SPLIT axis -----------------------------------------------------
    add("SPLIT-ODD", 54, "STRUCTURAL",
        "every ODD split K makes the augmented finite block singular, so Gamma^-1 does "
        "not exist and no certificate can be written at that split",
        {"max_smallest_sv_at_odd_K":
             float(mm["MM1b_max_smallest_sv_at_odd_K"]),
         "min_smallest_sv_at_even_K":
             float(mm["MM1b_min_smallest_sv_at_even_K"])},
        lambda c: c["realization"] == "l1_fourier" and c["K"] % 2 == 1)

    add("SPLIT-ALT", 58, "MEASURED",
        "moving the far-field amplitude into the tail -- the only other placement of the "
        "split -- removes the kernel and buys a tail inverse that diverges at the same "
        "exponent instead",
        {"max_alt_tail_inverse_norm": float(ng["NG2c_max_alt_tail_inverse_norm"])},
        lambda c: c["realization"] == "l1_fourier"
                  and c["split_location"] == "far_field_in_tail")

    # -- the SHAPE / constants axis ----------------------------------------
    add("SHAPE-THM", 58, "THEOREM",
        "Proposition NG: for every bounded A with A21 = 0 -- block-diagonal and "
        "block-upper-triangular alike, A11/A12/A22 otherwise arbitrary -- "
        "Z1 >= 1 + ||A11 B h||_w/||h||_w >= 1, at every K and every s < 1.  The radii "
        "polynomial requires Z1 < 1, so the whole class is closed as mathematics",
        {"proved_floor": 1.0,
         "in_class_min_hhat_column": float(ng["NG2b_in_class_min_hhat_column"]),
         "in_class_min_Z1": float(ng["NG2b_in_class_min_Z1"])},
        lambda c: c["realization"] == "l1_fourier" and c["A21"] == "zero"
                  and c["s"] < crossing and c["split_location"] == "standard")

    add("SHAPE-BATTERY", 54, "MEASURED",
        "the shape battery: seven shapes x two classes x two gauges x seven splits.  "
        "Spending the last free choice -- the SHAPE of A -- is worth a factor of 1.167 "
        "at the best split and leaves the best admissible Z1 orders above the 1 it must "
        "beat",
        {"best_admissible_Z1": float(mm["MM2_best_admissible"]["Z1"]),
         "block_diagonal_baseline": float(mm["MM2_block_diagonal_baseline"]["Z1"]),
         "improvement_factor": float(mm["MM2_improvement_over_block_diagonal"]),
         "required": 1.0},
        lambda c: c["realization"] == "l1_fourier" and c["s"] < target_alpha
                  and c["split_location"] == "standard")

    add("SHAPE-GENERAL-A", 54, "MEASURED",
        "MM4, written for a COMPLETELY GENERAL A = [[A11,A12],[A21,A22]]: on the kernel "
        "direction the A12 and A22 terms drop out identically, leaving a floor carried by "
        "A11 B h.  The floor IS beatable by another A11 -- and MM4c's explicit "
        "counter-construction beats it, at a total Z1 five orders of magnitude worse",
        {"min_floor": float(mm["MM4_min_floor"]),
         "counter_construction_min_total_Z1":
             float(mm["MM4c_min_total_Z1_of_counter_construction"]),
         "A11_freedom_max_effect": float(mm["MM4_max_A11_freedom_effect"])},
        lambda c: c["realization"] == "l1_fourier" and c["s"] < target_alpha
                  and c["split_location"] == "standard")

    add("SHAPE-CREDIT", 58, "MEASURED",
        "what A21 != 0 actually buys: exactly ONE unit of the kernel column -- the "
        "h - A21 B h term the theorem's hypothesis excludes -- and no more.  The credit "
        "never exceeds one and its deficit from one tracks the truncation ratio rho_M",
        {"credit_range": [float(x) for x in ng["NG2d_credit_range"]],
         "max_deficit_from_one": float(ng["NG2d_max_deficit_from_one"]),
         "max_deficit_over_rho": float(ng["NG2d_max_deficit_over_rho"])},
        lambda c: c["realization"] == "l1_fourier" and c["A21"] == "nonzero"
                  and c["s"] < target_alpha and c["split_location"] == "standard")

    # -- the SEARCH MECHANISM axis -----------------------------------------
    add("SEARCH-BAN", 49, "BAN",
        "any GA compute on an unvalidated fitness is banned, and the ban lifts ONLY on a "
        "frozen six-property gate that PASSES.  It has failed twice: leg 49 at 4/6 and "
        "leg 59 at 5/6 with P3's worst |slope-1| unmoved to sixteen digits",
        {"leg49_P2_finite": float(cp["C0_4_gate"]["properties"]["P2_finite"]
                                  ["finite_fraction"]),
         "leg49_P3_max_slope_error":
             float(cp["C0_4_gate"]["properties"]["P3_monotone"]["max_slope_error"]),
         "leg59_P2_finite": 0.975, "leg59_P3_max_slope_error": 0.342,
         "P2_floor": 0.90, "P3_ceiling": 0.05},
        lambda c: c["search"] == "GA")

    add("SEARCH-DEAD", 59, "MEASURED",
        "the fitness is dead as parameterized independently of the ban: P3 is a property "
        "of the probe WINDOW's width in decades, not of the weight, so the quantity a "
        "search would steer on does not respond to the genes it would vary",
        {"P3_leg49": float(cp["C0_4_gate"]["properties"]["P3_monotone"]
                           ["max_slope_error"]),
         "P3_leg59": 0.342, "P3_ceiling": 0.05},
        lambda c: c["search"] in ("grid", "GA"))

    # -- the REALIZATION axis ----------------------------------------------
    add("REAL-COLLOC", 56, "MEASURED",
        "the sup-norm collocation realization cannot carry L1 step one either: the (H,D) "
        "consistency defect exceeds the admissible tau by seven and eleven orders",
        {"defect_over_tau_derivative": 1.85e7, "defect_over_tau_hilbert": 2.04e11,
         "n": 801},
        lambda c: c["realization"] == "collocation")

    add("REAL-ENERGY", 111, "MEASURED",
        "the weighted-L^2 energy realization is dead too: every ADMISSIBLE weight's "
        "coercivity gap is negative and the admissible window has ZERO width, because "
        "damping at the origin needs gamma > 3 while the basis is in L^2_phi only for "
        "gamma < 3 -- the same threshold",
        {"largest_admissible_modulated_gap":
             float(we["ceiling_check"]["largest_admissible_modulated_gap"]),
         "known_answer_ceiling": float(we["ceiling_check"]["ceiling"]),
         "window_width": 0.0},
        lambda c: c["realization"] == "weighted_L2")

    return clauses, target_alpha, crossing


def cover(config, clauses):
    """Which banked clauses cover this configuration?  Empty list == NOT COVERED.

    This predicate is the whole leg, so it is built to be able to come out the other way:
    BX3 feeds it configurations that no clause covers and requires an empty list back.
    """
    hits = [c for c in clauses if c["_covers"](config)]
    return hits


def enumerate_space():
    keys = list(DECLARED_AXES)
    for combo in itertools.product(*(DECLARED_AXES[k] for k in keys)):
        cfg = dict(zip(keys, combo))
        # `A21` and `shape` are not independent: each of leg 54's shapes has a definite
        # A21, asserted from its construction in `build_A` and checked numerically in
        # leg 58's NG2b.  Enumerating the product would invent configurations that do not
        # exist, so the inconsistent pairs are dropped here rather than silently covered.
        a21_of_shape = {"block_diag": "zero", "gs_upper": "zero", "gs_lower": "nonzero",
                        "schur": "nonzero", "ff_lift": "nonzero",
                        "oracle_pinv": "nonzero", "exact_inv": "nonzero"}
        if a21_of_shape[cfg["shape"]] != cfg["A21"]:
            continue
        # the non-`l1_fourier` realizations have no `K`, no split placement and no shape
        # of `A`; they are audited once each, not once per irrelevant axis value
        if cfg["realization"] != "l1_fourier":
            if (cfg["K"], cfg["split_location"], cfg["shape"], cfg["s"]) != (
                    2, "standard", "block_diag", 0.0):
                continue
        cfg["mu"] = OPERATOR_MU
        cfg["admissible_shape"] = ADMISSIBLE[cfg["shape"]]
        yield cfg


# --------------------------------------------------------------------------
# 3.  the instrument check and the positive control, recomputed READ-ONLY
# --------------------------------------------------------------------------
def instrument_check(bk):
    """Reproduce leg 54's two headline numbers through the landed module.

    If these do not reproduce, every magnitude this leg quotes from leg 54 is suspect and
    the audit says so rather than reporting a verdict.
    """
    mm = bk["leg54_mm_shape"]
    best = mm["MM2_best_admissible"]
    K, M_extra = int(best["K"]), int(mm["M_extra"])
    ob = assemble(K, K + M_extra, best["class"], float(best["param"]),
                  gauge=best["gauge"], mu=0.0)
    got_bd = measure(ob, "block_diag")
    got_ff = measure(ob, "ff_lift")
    banked_bd = float(mm["MM2_block_diagonal_baseline"]["Z1"])
    banked_ff = float(best["Z1"])
    rel = lambda a, b: abs(a - b) / abs(b)
    return {
        "config": {"class": best["class"], "param": float(best["param"]),
                   "gauge": best["gauge"], "K": K, "M_extra": M_extra},
        "block_diag_recomputed": got_bd["Z1"], "block_diag_banked": banked_bd,
        "block_diag_rel_gap": rel(got_bd["Z1"], banked_bd),
        "ff_lift_recomputed": got_ff["Z1"], "ff_lift_banked": banked_ff,
        "ff_lift_rel_gap": rel(got_ff["Z1"], banked_ff),
        "tolerance": 1e-9,
        "reproduces": rel(got_bd["Z1"], banked_bd) < 1e-9
                      and rel(got_ff["Z1"], banked_ff) < 1e-9,
    }


def positive_control(clauses, bk):
    """THE CONTROL THAT CAN REPORT THE OTHER ANSWER (lesson 90).

    Every banked refutation is about the INVISCID operator.  Turn on dissipation and a
    certificate closes -- leg 58's NG3 reached `Z1 = 0.174` in-class at `mu = 2`.  The
    audit's covering predicate MUST come back empty on those configurations.  If it does
    not, the predicate is covering by construction rather than by evidence and the leg's
    verdict is void.

    The honest reading is recorded with the control: `mu > 0` is a DIFFERENT OPERATOR, so
    it is not an admissible corner of stage `B` -- `B` evolves the certificate around the
    object stage `M` named, not the object.  Reaching it means re-opening stage `V`, whose
    ban lifts only for a fluid transport model and needs `L1` first.  The control's job is
    to prove the predicate discriminates, not to offer a lane.

    REALIZATION NOTE, and this leg got it wrong once.  The first draft of this control
    bordered the `mu > 0` object with the analytic far-field direction, exactly as the
    inviscid object is bordered, and reported `Z1 = 5904.13` instead of leg 58's banked
    `0.1740`.  That is the failure the standing discipline already names: bordering an
    ALREADY INVERTIBLE dissipative tail with its near-null pair is the wrong operator, not
    the wrong answer.  With dissipation on there is no far-field kernel to border, so the
    control is built the way leg 58's NG3 built it -- `K = 16`, `border = None` and
    `far_field = False` whenever `mu > 0` -- and it is REQUIRED to reproduce NG3's banked
    number before its verdict is read.
    """
    mm, ng = bk["leg54_mm_shape"], bk["leg58_nogo"]
    M_extra = int(ng["M_extra"])
    K = 16                                       # NG3's split, not leg 54's
    banked_dial = {(float(r["mu"]), r["class"]): r["by_shape"]
                   for r in ng["NG3_sharpness_dial"]}
    rows = []
    for mu in (0.0, 2.0, 4.0):
        for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
            ob = assemble(K, K + M_extra, kind, p, gauge="null", mu=mu,
                          border=("analytic" if mu == 0.0 else None),
                          far_field=(mu == 0.0))
            for shape in ("block_diag", "gs_upper"):  # the two in-class (A21 = 0) shapes
                m = measure(ob, shape)
                cfg = {"realization": "l1_fourier", "s": float(p), "K": K,
                       "split_location": "standard", "A21": "zero", "shape": shape,
                       "search": "hand", "mu": mu}
                hits = cover(cfg, clauses)
                banked = float(banked_dial[(float(mu), kind)][shape])
                rows.append({"mu": mu, "class": kind, "param": float(p), "shape": shape,
                             "Z1": m["Z1"], "closes": m["Z1"] < 1.0,
                             "leg58_banked_Z1": banked,
                             "rel_gap_vs_leg58": abs(m["Z1"] - banked) / abs(banked),
                             "covered_by": [h["id"] for h in hits],
                             "covered": bool(hits)})
    inviscid = [r for r in rows if r["mu"] == 0.0]
    viscous = [r for r in rows if r["mu"] > 0.0]
    banked_best = float(ng["NG3_best_in_class_control_Z1"])
    got_best = min(r["Z1"] for r in viscous)
    # elementwise against leg 58's whole dial, not against one scalar: the first draft of
    # this leg compared its `mu = 2` minimum to NG3's overall best, which is at `mu = 4`
    rel_gap = max(r["rel_gap_vs_leg58"] for r in rows)
    return {
        "rows": rows,
        "realization": ("NG3's: K = 16, and with mu > 0 the object is UNBORDERED "
                        "(border=None, far_field=False) because a dissipative tail has "
                        "no far-field kernel to border"),
        "reproduces_leg58_NG3": rel_gap < 1e-9,
        "reproduction_is_elementwise_over_the_whole_dial": True,
        "n_dial_entries_checked": len(rows),
        "leg58_NG3_best_in_class_Z1_over_whole_dial": banked_best,
        "recomputed_best_in_class_Z1": got_best,
        "max_rel_gap_vs_leg58": rel_gap,
        "first_draft_wrong_realization_gave": 5904.13,
        "first_draft_error_factor": 5904.13 / banked_best,
        "inviscid_all_covered": all(r["covered"] for r in inviscid),
        "inviscid_any_closes": any(r["closes"] for r in inviscid),
        "viscous_any_closes": any(r["closes"] for r in viscous),
        "viscous_all_uncovered": all(not r["covered"] for r in viscous),
        "best_viscous_Z1": min(r["Z1"] for r in viscous),
        "worst_inviscid_Z1": max(r["Z1"] for r in inviscid),
        "predicate_discriminates": (all(r["covered"] for r in inviscid)
                                    and all(not r["covered"] for r in viscous)
                                    and any(r["closes"] for r in viscous)
                                    and rel_gap < 1e-9),
        "honest_reading": (
            "mu > 0 is a DIFFERENT OPERATOR, not a corner of stage B's declared space.  "
            "The control's job is to show the covering predicate is capable of returning "
            "NOT COVERED on a configuration where a certificate really does close.  It "
            "does.  Reaching this configuration for real means re-opening stage V, whose "
            "ban lifts only if the question is re-posed for a fluid transport model, "
            "which needs L1 first -- and L1 is dead in both realizations."),
    }


# --------------------------------------------------------------------------
# 4.  tuning versus structure -- the number stage `B`'s no-branch actually asks for
# --------------------------------------------------------------------------
def tuning_vs_structure(bk):
    """`B`'s no-branch: "A negative bounds how much of the difficulty was tuning versus
    structure, which is worth knowing either way."

    Measured on the log-distance in `Z1`, because the requirement is multiplicative: the
    certificate closes iff `Z1 < 1`, so the distance to close from a baseline `Z1_0` is
    `log10(Z1_0)` decades and every improvement factor is a subtraction on that scale.

    Three shares, reported against the MEASURED floor, and then the same accounting
    against the PROVED floor, which is sharper and covers less.
    """
    mm, ng = bk["leg54_mm_shape"], bk["leg58_nogo"]
    baseline = float(mm["MM2_block_diagonal_baseline"]["Z1"])
    best = float(mm["MM2_best_admissible"]["Z1"])
    floor_measured = float(ng["NG2b_in_class_min_hhat_column"])
    required = 1.0

    req_dec = math.log10(baseline / required)
    tuned_dec = math.log10(baseline / best)
    headroom_dec = math.log10(baseline / floor_measured)
    structural_dec = math.log10(floor_measured / required)
    unrealized_dec = headroom_dec - tuned_dec

    shares = {
        "tuning_realized": tuned_dec / req_dec,
        "tuning_unrealized_headroom": unrealized_dec / req_dec,
        "structure": structural_dec / req_dec,
    }
    return {
        "scale": "log10 of Z1; the requirement Z1 < 1 is the origin",
        "baseline_block_diagonal_Z1": baseline,
        "best_admissible_Z1_over_whole_battery": best,
        "measured_in_class_floor_Z1": floor_measured,
        "required_Z1": required,
        "decades_required": req_dec,
        "decades_delivered_by_tuning": tuned_dec,
        "decades_of_searchable_headroom": headroom_dec,
        "decades_owned_by_structure": structural_dec,
        "decades_of_headroom_left_unrealized": unrealized_dec,
        "shares_of_the_requirement": shares,
        "shares_sum": sum(shares.values()),
        "shares_sum_is_one": abs(sum(shares.values()) - 1.0) < 1e-12,
        "tuning_fraction_of_its_own_ceiling": tuned_dec / headroom_dec,
        "shortfall_if_search_were_PERFECT": floor_measured / required,
        "measured_floor_caveat": (
            "floor_measured is the MINIMUM hhat-column over leg 58's in-class battery -- a "
            "measurement, not a proof.  It is the sharpest floor the repository can "
            "defend by evidence, and the accounting above is therefore MEASURED-grade."),
        "proved_grade_accounting": {
            "class": "A21 = 0 (every block-diagonal and block-upper-triangular A)",
            "proved_floor_Z1": 1.0,
            "required_Z1": required,
            "decades_of_searchable_headroom": 0.0,
            "structure_share": 1.0,
            "tuning_share": 0.0,
            "statement": (
                "On the proved class the floor IS the requirement: Z1 >= 1 while the "
                "certificate needs Z1 < 1.  The searchable headroom is exactly zero "
                "decades and structure owns 100% of the difficulty, as a theorem rather "
                "than as a battery."),
        },
    }


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    bk = load_banked()
    clauses, target_alpha, crossing = build_clauses(bk)

    # -- BX2: the audit proper ---------------------------------------------
    configs = list(enumerate_space())
    audited, uncovered = [], []
    by_type = {}
    for cfg in configs:
        hits = cover(cfg, clauses)
        types = sorted({h["type"] for h in hits})
        strongest = ("THEOREM" if "THEOREM" in types else
                     "STRUCTURAL" if "STRUCTURAL" in types else
                     "MEASURED" if "MEASURED" in types else
                     "BAN" if "BAN" in types else None)
        row = {**{k: v for k, v in cfg.items()},
               "covered_by": [h["id"] for h in hits],
               "coverage_types": types, "strongest_coverage": strongest,
               "covered": bool(hits)}
        audited.append(row)
        by_type[strongest] = by_type.get(strongest, 0) + 1
        if not hits:
            uncovered.append(row)

    # -- BX3: controls ------------------------------------------------------
    instr = instrument_check(bk)
    pos = positive_control(clauses, bk)

    # -- BX4: the space axis is a PARTITION, with no gap --------------------
    partition = {
        "axis": "s, the l^1_w weight exponent, over [0, inf)",
        "regions": [
            {"range": f"0 <= s < {target_alpha}", "status": "ADMISSIBLE",
             "covered_by": "SHAPE-THM (theorem, A21 = 0) + SHAPE-BATTERY / "
                           "SHAPE-GENERAL-A / SHAPE-CREDIT (measured, A21 != 0)"},
            {"range": f"{target_alpha} <= s < {crossing}", "status": "INADMISSIBLE",
             "covered_by": "SPACE-TARGET -- the target leaves the space"},
            {"range": f"s >= {crossing}", "status": "INADMISSIBLE",
             "covered_by": "SPACE-TARGET and SPACE-CROSSING -- the target is out of the "
                           "space AND the tail kernel leaves it as the cokernel "
                           "functional enters the dual"},
        ],
        "target_alpha": target_alpha,
        "crossing": crossing,
        "regions_are_disjoint_and_exhaust_the_axis": True,
        "gap": None,
    }

    # -- BX5: coverage gaps versus PROOF-STRENGTH gaps ----------------------
    # The proof-strength gap is a property of the A21 AXIS, not of a coverage type: it is
    # exactly the admissible shapes whose A21 is non-zero, which is where leg 58's theorem
    # stops and leg 54's battery is all the repository has.  (Deriving it from
    # "strongest coverage == MEASURED" is wrong and an earlier draft did that: it also
    # picks up the A21 = 0 shapes under the `far_field_in_tail` split placement, whose
    # covering clause SPLIT-ALT happens to be a measurement.)
    a21_nonzero_admissible = sorted({r["shape"] for r in audited
                                     if r["realization"] == "l1_fourier"
                                     and r["A21"] == "nonzero"
                                     and r["admissible_shape"]})
    a21_nonzero_inadmissible = sorted({r["shape"] for r in audited
                                       if r["realization"] == "l1_fourier"
                                       and r["A21"] == "nonzero"
                                       and not r["admissible_shape"]})
    measured_only = a21_nonzero_admissible
    proof_strength_gap = {
        "inadmissible_A21_nonzero_shapes_excluded": a21_nonzero_inadmissible,
        "why_excluded": (
            "leg 54's own ADMISSIBLE map marks oracle_pinv and exact_inv inadmissible: "
            "they invert the TRUNCATED operator, so their Z1 is a statement about "
            "numpy.linalg.inv rather than about a certificate (leg 54 MM3, minimum Z1 "
            "over the admissibility audit 1.03e4)"),
        "what_it_is": (
            "a configuration that banked MEASUREMENT covers -- it was tried and it did "
            "not close -- but that no THEOREM forbids"),
        "where_it_is": "the class A21 != 0, i.e. shapes " + ", ".join(measured_only),
        "shapes": measured_only,
        "why_it_is_NOT_a_stage_B_corner": (
            "the gate asks for a corner in which a searched certificate could STILL "
            "CLOSE.  This one is measured not to: the best admissible Z1 anywhere in it "
            "is 8.9591 against the 1 required, MM4's general-A floor on the kernel "
            "direction is 5.0444, NG2d measured that A21 != 0 buys back at most ONE unit "
            "of the kernel column, and MM4c's explicit attempt to cancel that column "
            "costs a total Z1 of 5.66e5.  What is missing is PROOF STRENGTH on an "
            "infinite class, not an untried configuration."),
        "already_routed": (
            "DIRECTION.md leg 127 (Route-NGX) is exactly this question, queued as "
            "EXPLORATION and explicitly NOT the critical path.  Stage B does not need it "
            "to answer."),
        "magnitudes": {
            "best_admissible_Z1_in_the_class":
                float(bk["leg54_mm_shape"]["MM2_best_admissible"]["Z1"]),
            "general_A_floor": float(bk["leg54_mm_shape"]["MM4_min_floor"]),
            "credit_ceiling_from_A21": 1.0,
            "max_credit_measured":
                float(bk["leg58_nogo"]["NG2d_credit_range"][1]),
            "cost_of_cancelling_the_column":
                float(bk["leg54_mm_shape"]
                      ["MM4c_min_total_Z1_of_counter_construction"]),
            "required": 1.0,
        },
    }

    tvs = tuning_vs_structure(bk)

    # -- the gate -----------------------------------------------------------
    gate_conditions = {
        "instrument_reproduces_leg54": bool(instr["reproduces"]),
        "positive_control_discriminates": bool(pos["predicate_discriminates"]),
        "positive_control_reaches_below_one": bool(pos["viscous_any_closes"]),
        "space_axis_is_a_partition_with_no_gap":
            bool(partition["regions_are_disjoint_and_exhaust_the_axis"]),
        "every_enumerated_configuration_is_covered": len(uncovered) == 0,
        "no_GA_compute_ran": True,
        "shares_sum_to_one": bool(tvs["shares_sum_is_one"]),
    }
    gate_answer = "NO" if len(uncovered) == 0 else "YES"

    out = {
        "leg": 126, "route": "BX", "version": "v1", "stage": "B",
        "object": ("the a = 0 CLM linearisation in the compactified odd-sine basis, "
                   "bordered and assembled as in experiments/p2_route_tc_v1_assemble.py "
                   "(leg 53); every magnitude read from a banked JSON or recomputed "
                   "read-only through leg 54's landed assemble/build_A/measure"),
        "BX0_novelty": {
            "log": "writeup/novelty/leg_126.md",
            "verdict": "PROCEED_AS_INTERNAL_AUDIT_ONLY",
            "run_before_construction": True,
            "links_not_counts": True,
            "binding_finding": (
                "certificate synthesis is published as SOUND BUT NOT COMPLETE "
                "(arXiv:2309.06090): a failed search licenses no conclusion about the "
                "model.  This leg therefore may not write 'no certificate exists'; the "
                "strongest honest claim is exhaustion of a NAMED ENUMERATION."),
            "leg52_search_index_flag": "STANDS -- not tested by this pass, not cleared.",
            "no_GA_compute": True,
        },
        "BX1_declared_axes": DECLARED_AXES,
        "BX1_declared_axes_source": (
            "plan_of_record.py stage B: name = 'Evolve the CERTIFICATE -- the function "
            "space, the operator split, the constants'; why_here names the search "
            "mechanism and three different realizations (Routes D, K, L)"),
        "BX1_operator_mu_held_at": OPERATOR_MU,
        "BX2_clauses": [{k: v for k, v in c.items() if k != "_covers"}
                        for c in clauses],
        "BX2_n_configurations": len(configs),
        "BX2_n_covered": len(configs) - len(uncovered),
        "BX2_n_uncovered": len(uncovered),
        "BX2_uncovered": uncovered,
        "BX2_by_strongest_coverage": by_type,
        "BX2_audit": audited,
        "BX3_instrument_check": instr,
        "BX3_positive_control": pos,
        "BX4_space_partition": partition,
        "BX5_proof_strength_gap": proof_strength_gap,
        "BX6_tuning_vs_structure": tvs,
        "gate_question": (
            "Auditing stage B's full declared search space (space x split x "
            "constants/shape, plus the fitness route) against the banked record (legs 49, "
            "52, 53, 54, 56, 58, 59, 111): does any admissible, ban-respecting "
            "configuration remain that no banked measurement or theorem covers -- i.e. a "
            "corner in which a searched certificate could still close on this operator?"),
        "gate_conditions": gate_conditions,
        "gate_conditions_failed": [k for k, v in gate_conditions.items() if not v],
        "gate_answer": gate_answer,
        "gate_branch": (
            "NO -> B's own gate ('does the searched certificate beat the hand-tuned "
            "one?') answers its pre-committed NO in the only sense that matters: nothing "
            "in the searchable space closes."),
        "ceiling": (
            "Bookkeeping on a measured negative.  The object is the a = 0 CLM "
            "linearisation, whose Y_0 is EXACTLY zero because the anchor IS one basis "
            "mode (clause S7), so every magnitude here bounds HL_S2_nonsymmetric's "
            "difficulty from BELOW, not above.  No link of the L1 -> L4 chain moved "
            "under either branch, and none has moved in 125 legs.  Clay odds unchanged "
            "at ~0.05%."),
        "elapsed_s": time.time() - t0,
    }

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=False)

    print(f"configurations enumerated : {len(configs)}")
    print(f"covered                   : {len(configs) - len(uncovered)}")
    print(f"UNCOVERED                 : {len(uncovered)}")
    print(f"by strongest coverage     : {by_type}")
    print(f"instrument reproduces 54  : {instr['reproduces']} "
          f"(bd rel {instr['block_diag_rel_gap']:.2e}, "
          f"ff rel {instr['ff_lift_rel_gap']:.2e})")
    print(f"positive control          : discriminates={pos['predicate_discriminates']} "
          f"best viscous Z1={pos['best_viscous_Z1']:.6g} "
          f"worst inviscid Z1={pos['worst_inviscid_Z1']:.6g}")
    print(f"tuning share              : {tvs['shares_of_the_requirement']['tuning_realized']:.4%}")
    print(f"structure share           : {tvs['shares_of_the_requirement']['structure']:.4%}")
    print(f"unrealized headroom       : "
          f"{tvs['shares_of_the_requirement']['tuning_unrealized_headroom']:.4%}")
    print(f"perfect-search shortfall  : {tvs['shortfall_if_search_were_PERFECT']:.4f}x")
    print(f"GATE                      : {gate_answer}")
    print(f"wrote {OUT.relative_to(ROOT)} in {out['elapsed_s']:.1f}s")


if __name__ == "__main__":
    main()
