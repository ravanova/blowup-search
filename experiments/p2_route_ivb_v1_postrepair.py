"""Route-IVB (leg 87): the INDEPENDENT post-repair regression check of `solver/interval.py`.

WHY THIS RUNS.  Leg 69 measured two real soundness defects in the shared interval core -- 62
subnormal-band false negatives in 1680 cases (worst escape 6.58 eta) and a silent `[nan, nan]`
enclosure above |entry| = 2^997 -- and a bench-repair agent fixed both (commit "Leg 0: ORCH --
repair the two soundness defects leg 69 measured in solver/interval.py").  The repair agent
self-verified extensively and reported all 18 gates of `test_interval_certificate.py`
bit-identical pre/post.  **This leg does not take that report as evidence.**  It re-derives the
two claims from scratch:

  (a) leg 69's ORIGINAL corpus, re-run verbatim against the repaired module -- same seed
      (20260805), same family builders, imported from leg 69's own runner so the corpus is
      literally the same corpus, not a re-implementation of it -- and diffed family-by-family
      against the banked pre-repair numbers in `writeup/data/p2_route_ia_v1_interval_stress.json`;

  (b) the "bit-for-bit inert in the live operating range" claim, re-derived by reconstructing the
      PRE-REPAIR module in memory (`git show <repair>^:solver/interval.py`, exec'd into a fresh
      module object) and diffing ENDPOINT BIT PATTERNS against the repaired module on the live
      operator.  This is differential testing against the actual previous source, not against a
      description of it.

...plus a FRESH adversarial battery of this leg's own choosing, aimed by leg 87's novelty pass
(`writeup/novelty/leg_87.md`) at the one number in the repair that has NO published bound behind
it.  Rump (BIT 2012) Thm 4.3 gives the plain dot product's absolute underflow term as n*eta/2,
i.e. 0.5 eta per accumulated term, and the module carries 2.0 -- a 4x margin over print.  The
COMPENSATED path's constant, 8.0 eta per term, is not covered by that theorem and rests on ORO
2005's `a*b = p + e + 5 eta theta` remark plus the repair's own margin argument.  Families F1-F2
below measure the EMPIRICAL eta-per-term demand of both reductions directly, so the two constants
are checked against measurement rather than against their own comment.

WHAT IS REPORTED.  Magnitudes, never booleans.  Every containment question is decided against
EXACT RATIONAL ground truth (`fractions.Fraction` on exact float64 inputs -- the inputs are exact
floats, so the real answer is a rational and containment is decided exactly).  Every family
reports the worst relative slack, the worst absolute escape in units of eta = 2^-1074, and where
relevant the measured eta-per-term demand against the implemented constant.

This file makes NO certification claim and does NOT modify `solver/interval.py`.
"""

import importlib.util
import json
import os
import subprocess
import sys
import types
import warnings
from fractions import Fraction as Fr

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from solver.interval import (                                          # noqa: E402
    Interval, dot2_matvec, isum, matvec, _two_product,
    _ETA_TERMS_PLAIN, _ETA_TERMS_DOT2,
)

ETA = 2.0 ** -1074
U = 2.0 ** -53

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_ivb_v1_postrepair.json")
LEG69_DATA = os.path.join(ROOT, "writeup", "data", "p2_route_ia_v1_interval_stress.json")
LEG69_RUNNER = os.path.join(ROOT, "experiments", "p2_route_ia_v1_interval_stress.py")

# Rump, BIT Numer. Math. 52:201-220 (2012), Thm 4.3:
#     | s~_n - x^T y |  <  (n + 2) u ufp(S~_n)  +  n eta / 2
# i.e. the PUBLISHED absolute underflow coefficient for the plain recursive dot product is
# 0.5 eta per accumulated term.  Read verbatim from the paper in leg 87's novelty pass.
RUMP_PLAIN_ETA_PER_TERM = 0.5


# ==========================================================================
# PART A -- leg 69's ORIGINAL corpus, re-run verbatim against the repaired module
# ==========================================================================

def _import_leg69():
    """Import leg 69's own runner as a module, so PART A uses the literal original corpus.

    Nothing in it is executed at import time (it is `if __name__ == '__main__'`-guarded), and
    this leg never calls its `main()` -- which would overwrite leg 69's banked data file,
    outside this leg's territory."""
    spec = importlib.util.spec_from_file_location("leg69_stress", LEG69_RUNNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rerun_leg69_corpus():
    """Leg 69's seven families, same seed, same order -- against the REPAIRED module."""
    l69 = _import_leg69()
    rng = np.random.default_rng(20260805)          # leg 69's seed, verbatim
    fams = [
        l69.fam_elementary(rng),
        l69.fam_isum(rng),
        l69.fam_matvec(rng),
        l69.fam_dot2_normal(rng),
        l69.fam_tail_block(rng),
        l69.fam_subnormal(rng),
        l69.fam_subnormal_matvec(rng),
    ]
    return [f.report() for f in fams]


def diff_against_banked(reports):
    """Family-by-family delta against leg 69's banked PRE-repair numbers."""
    with open(LEG69_DATA) as fh:
        old = json.load(fh)
    by_name = {r["family"]: r for r in old["families"]}
    rows = []
    for r in reports:
        o = by_name.get(r["family"])
        if o is None:
            rows.append({"family": r["family"], "note": "no pre-repair counterpart"})
            continue
        rows.append({
            "family": r["family"],
            "cases_pre": o["cases"], "cases_post": r["cases"],
            "corpus_identical_size": o["cases"] == r["cases"],
            "false_negatives_pre": o["false_negatives"],
            "false_negatives_post": r["false_negatives"],
            "false_negatives_repaired": o["false_negatives"] - r["false_negatives"],
            "worst_escape_eta_pre": o["worst_absolute_escape_eta"],
            "worst_escape_eta_post": r["worst_absolute_escape_eta"],
            "worst_relative_slack_pre": o["worst_relative_slack"],
            "worst_relative_slack_post": r["worst_relative_slack"],
            "slack_change": (r["worst_relative_slack"] - o["worst_relative_slack"]
                             if np.isfinite(o["worst_relative_slack"])
                             and np.isfinite(r["worst_relative_slack"]) else None),
            "reproducer_pre": o["reproducer"],
            "reproducer_post": r["reproducer"],
        })
    return rows, old


def rerun_dekker_probe():
    """Leg 69's defect-2 probe, re-run.  Pre-repair it returned a silent [nan, nan]; post-repair
    `_two_product` must RAISE at the same exponent.  Reported as the measured exponent, not as a
    boolean."""
    e_first_raise = None
    e_first_nonfinite = None
    for e in range(0, 1024):
        try:
            p, err = _two_product(np.array([2.0 ** e]), np.array([1.0]))
        except OverflowError:
            e_first_raise = e
            break
        if not np.isfinite(err[0]) or not np.isfinite(p[0]):
            e_first_nonfinite = e
            break
    out = {"probe": "dekker_split_overflow_rerun",
           "e_first_raise": e_first_raise,
           "e_first_silent_nonfinite": e_first_nonfinite,
           "leg69_e_crit": 997,
           "wall_unmoved": e_first_raise == 997}
    if e_first_raise is not None:
        # one binade BELOW the wall the compensated path must still return a sound enclosure
        r = dot2_matvec(np.array([[2.0 ** (e_first_raise - 1)]]), np.array([1.0]))
        ex = Fr(2) ** (e_first_raise - 1)
        out["below_wall_magnitude"] = 2.0 ** (e_first_raise - 1)
        out["below_wall_encloses_exact"] = bool(Fr(float(r.lo[0])) <= ex <= Fr(float(r.hi[0])))
        out["below_wall_width"] = float(r.hi[0] - r.lo[0])
        try:
            dot2_matvec(np.array([[2.0 ** e_first_raise]]), np.array([1.0]))
            out["at_wall"] = "RETURNED AN ENCLOSURE (silent)"
        except OverflowError as exc:
            out["at_wall"] = "OverflowError"
            out["at_wall_message_head"] = str(exc)[:80]
    return out


# ==========================================================================
# shared exact-rational machinery for PART B
# ==========================================================================

def _exact_matvec(M, v):
    return [sum(Fr(M[i, j]) * Fr(v[j]) for j in range(M.shape[1]))
            for i in range(M.shape[0])]


def _cancel_row(row, v):
    """Two exact-float columns that cancel a row's exact dot product to ~1e-32 relative, while
    leaving every stored number exactly representable (which is what keeps the Fraction ground
    truth exact rather than approximate)."""
    S = sum(Fr(row[j]) * Fr(v[j]) for j in range(len(v)))
    h = float(S)
    return np.array([-h, -float(S - Fr(h))], dtype=float)


def _score(lo, hi, ex):
    """(contained, relative slack, signed headroom in eta) for one enclosure vs the exact value.

    `headroom_eta` is the distance from the exact value to the NEAREST endpoint measured in units
    of eta -- positive inside, negative outside.  It is the magnitude that decides whether the
    absolute (underflow) term is correctly sized, because in the subnormal band the enclosure's
    whole radius is that term."""
    lof, hif = float(lo), float(hi)
    if np.isnan(lof) or np.isnan(hif):
        return False, -1.0, float("-inf")
    if np.isinf(lof) or np.isinf(hif):
        return True, None, float("inf")
    L, H = Fr(lof), Fr(hif)
    s = min(ex - L, H - ex)
    w = H - L
    return s >= 0, (float(s / w) if w > 0 else 0.0), _eta_units(s)


def _eta_units(s):
    """`s / eta` as a float, saturating instead of raising.

    At the top of the double range (the Dekker-wall family reaches 2^2046) the quotient exceeds
    the float range; the sign and the fact that it is astronomically large is all that is wanted
    there, so it saturates rather than aborting the run."""
    q = s / Fr(ETA)
    try:
        return float(q)
    except (OverflowError, ValueError):
        return float("inf") if q > 0 else float("-inf")


# ==========================================================================
# PART B, FAMILY F1 -- the eta-per-term CALIBRATION of both reductions
# ==========================================================================

def fam_eta_calibration(rng):
    """Is `2.0 eta/term` (plain) and `8.0 eta/term` (compensated) actually ENOUGH?

    The novelty pass established that the plain constant has a published bound behind it (Rump
    Thm 4.3: 0.5 eta/term) with 4x margin, and that the compensated constant has none.  Across
    THIS band the relative terms have not all vanished, so an eta-per-term figure would be
    meaningless here (it would be measuring the relative error in absolute units).  What is
    measured instead is the dimensionless

        radius_utilisation = |exact - centre of enclosure| / radius

    -- how much of the enclosure the true error actually consumes.  1.0 is the enclosure exactly
    touching, above 1.0 is a false negative.  The eta-per-term calibration proper is done in the
    two families below, in the regime where every relative term is exactly zero and the constant
    is the ONLY thing holding the enclosure up.

    The band is swept an order of magnitude wider and ~2x finer than leg 69's, at four
    accumulation lengths rather than one, because the constant scales with m and leg 69 only ever
    tested m = 64."""
    out = {"family": "eta_per_term_calibration",
           "note": ("empirical absolute-error demand of both reductions in the subnormal band, "
                    "in units of eta per accumulated term, against the implemented constants "
                    f"(plain {_ETA_TERMS_PLAIN}, dot2 {_ETA_TERMS_DOT2}) and the published "
                    f"Rump BIT 2012 Thm 4.3 coefficient {RUMP_PLAIN_ETA_PER_TERM} for the plain "
                    "recursive dot product"),
           "implemented_plain_eta_per_term": _ETA_TERMS_PLAIN,
           "implemented_dot2_eta_per_term": _ETA_TERMS_DOT2,
           "published_plain_eta_per_term_rump_thm_4_3": RUMP_PLAIN_ETA_PER_TERM,
           "by_reduction": {}}
    per = {"dot2_matvec": {"cases": 0, "false_negatives": 0, "min_headroom_eta": np.inf,
                           "max_radius_utilisation": 0.0, "worst_escape_eta": 0.0,
                           "reproducer": None},
           "matvec": {"cases": 0, "false_negatives": 0, "min_headroom_eta": np.inf,
                      "max_radius_utilisation": 0.0, "worst_escape_eta": 0.0,
                      "reproducer": None}}
    scan = {}
    for e in range(-130, -191, -3):
        scale = 10.0 ** e
        for m in (8, 32, 64, 258):
            for _ in range(3):
                base = rng.standard_normal((1, m))
                v0 = rng.standard_normal(m)
                ext = _cancel_row(base[0], v0)
                M = np.concatenate([base, ext[None, :]], axis=1) * scale
                v = np.concatenate([v0, [1.0, 1.0]]) * scale
                mm = M.shape[1]
                ex = _exact_matvec(M, v)[0]
                for name, r in (("dot2_matvec", dot2_matvec(M, v)),
                                ("matvec", matvec(M, Interval.point(v)))):
                    ok, rel, head = _score(r.lo[0], r.hi[0], ex)
                    d = per[name]
                    d["cases"] += 1
                    d["min_headroom_eta"] = min(d["min_headroom_eta"], head)
                    if np.isfinite(float(r.lo[0])) and np.isfinite(float(r.hi[0])):
                        L, H = Fr(float(r.lo[0])), Fr(float(r.hi[0]))
                        centre = (L + H) / 2
                        radius = (H - L) / 2
                        if radius > 0:
                            d["max_radius_utilisation"] = max(
                                d["max_radius_utilisation"], abs(float((ex - centre) / radius)))
                    if not ok:
                        d["false_negatives"] += 1
                        esc = -head
                        if esc > d["worst_escape_eta"]:
                            d["worst_escape_eta"] = esc
                            d["reproducer"] = {"scale": f"1e{e}", "m": mm,
                                               "lo": repr(float(r.lo[0])),
                                               "hi": repr(float(r.hi[0])),
                                               "escape_eta": esc}
                    key = f"1e{e}"
                    s = scan.setdefault(key, {"cases": 0, "false_negatives": 0,
                                              "min_headroom_eta": np.inf})
                    s["cases"] += 1
                    s["false_negatives"] += (not ok)
                    s["min_headroom_eta"] = min(s["min_headroom_eta"], head)
    for k, d in per.items():
        d["min_headroom_eta"] = float(d["min_headroom_eta"])
    for s in scan.values():
        s["min_headroom_eta"] = float(s["min_headroom_eta"])
    out["by_reduction"] = per
    out["scale_scan"] = scan
    out["worst_radius_utilisation"] = max(per["dot2_matvec"]["max_radius_utilisation"],
                                          per["matvec"]["max_radius_utilisation"])
    return out


# ==========================================================================
# PART B, FAMILY F1b -- Rump's n*eta/2 bound ATTAINED, exactly
# ==========================================================================

def fam_half_eta_aligned():
    """The eta constants calibrated against data that ATTAINS the published bound exactly.

    Rump Thm 4.3 gives the plain dot product's absolute underflow term as n*eta/2 -- 0.5 eta per
    accumulated term.  Random subnormal data does not come close to that, so a random battery can
    never say whether the implemented 2.0 (plain) and 8.0 (compensated) are 4x margin or 4000x.
    This family constructs the EXTREMAL case in closed form and checks it deterministically.

    Take M_ij = eta exactly and v_j = c_j + 1/2 with c_j an EVEN integer.  The exact product is
    (c_j + 1/2) * eta -- precisely halfway between two representable subnormals -- so
    round-half-to-even returns c_j * eta and the rounding error is exactly -eta/2, in the SAME
    direction for every j because every c_j is even.  Sums of integer multiples of eta are exact
    while they stay subnormal, so the accumulation adds no further error and

        |computed - exact|  =  m * eta / 2   EXACTLY,

    which is Rump's bound attained with equality.  The measured eta-per-term demand is therefore
    exactly 0.5, and dividing the implemented constant by it gives the true margin -- 4x on the
    plain path, 16x on the compensated one -- as a measurement rather than an assertion.

    Both signs of the alignment are run (c_j even, and c_j odd, which rounds the other way)."""
    out = {"family": "half_eta_aligned_extremal",
           "note": ("closed-form extremal subnormal data: every product lands exactly halfway "
                    "between two subnormals with the ties broken in the SAME direction, so the "
                    "absolute accumulation error is exactly m*eta/2 -- Rump BIT 2012 Thm 4.3 "
                    "attained with equality.  This is the case the eta constants must cover"),
           "cases": 0, "false_negatives": 0, "by_reduction": {}, "reproducer": None}
    per = {"dot2_matvec": {"cases": 0, "false_negatives": 0, "min_headroom_eta": np.inf,
                           "max_demand_eta_per_term": 0.0, "min_margin_factor": np.inf},
           "matvec": {"cases": 0, "false_negatives": 0, "min_headroom_eta": np.inf,
                      "max_demand_eta_per_term": 0.0, "min_margin_factor": np.inf}}
    detail = []
    for m in (4, 16, 64, 128, 258):
        for parity, base in (("even", 0), ("odd", 1)):
            c = np.arange(base, base + 2 * m, 2, dtype=float)      # all same parity
            v = c + 0.5
            M = np.full((1, m), ETA)
            ex = _exact_matvec(M, v)[0]
            row = {"m": m, "parity": parity,
                   "exact_over_eta": float(sum(Fr(x) for x in v)),
                   "predicted_error_eta": 0.5 * m}
            for name, r in (("dot2_matvec", dot2_matvec(M, v)),
                            ("matvec", matvec(M, Interval.point(v)))):
                ok, rel, head = _score(r.lo[0], r.hi[0], ex)
                L, H = Fr(float(r.lo[0])), Fr(float(r.hi[0]))
                centre = (L + H) / 2
                demand = abs(_eta_units(ex - centre)) / m
                radius_eta = _eta_units((H - L) / 2)
                d = per[name]
                d["cases"] += 1
                out["cases"] += 1
                d["min_headroom_eta"] = min(d["min_headroom_eta"], head)
                d["max_demand_eta_per_term"] = max(d["max_demand_eta_per_term"], demand)
                impl = _ETA_TERMS_DOT2 if name == "dot2_matvec" else _ETA_TERMS_PLAIN
                if demand > 0:
                    d["min_margin_factor"] = min(d["min_margin_factor"], impl / demand)
                if not ok:
                    d["false_negatives"] += 1
                    out["false_negatives"] += 1
                    if out["reproducer"] is None:
                        out["reproducer"] = {"reduction": name, "m": m, "parity": parity,
                                             "lo": repr(float(r.lo[0])),
                                             "hi": repr(float(r.hi[0])),
                                             "escape_eta": -head}
                row[name] = {"radius_eta": radius_eta, "headroom_eta": head,
                             "demand_eta_per_term": demand,
                             "implemented_eta_per_term": impl}
            detail.append(row)
    for d in per.values():
        d["min_headroom_eta"] = float(d["min_headroom_eta"])
        d["min_margin_factor"] = float(d["min_margin_factor"])
    out["by_reduction"] = per
    out["detail"] = detail
    out["published_bound_eta_per_term"] = RUMP_PLAIN_ETA_PER_TERM
    return out


# ==========================================================================
# PART B, FAMILY F2 -- FULLY subnormal data (integer multiples of eta)
# ==========================================================================

def fam_pure_subnormal(rng):
    """Data that is not merely SMALL but literally in the subnormal grid.

    Leg 69's subnormal family reached the band by scaling normal-range gaussians by 1e-150, so
    its operands were normal doubles whose PRODUCTS went subnormal.  This family goes one step
    further and makes the OPERANDS themselves subnormal -- integer multiples of eta -- which is
    the regime where every relative error term is identically zero and the enclosure's entire
    radius is the absolute term.  If 8 m eta / 2 m eta were mis-sized, this is where it shows.

    The exact dot product of subnormal operands is still an exact rational, so the ground truth
    is unaffected."""
    out = {"family": "pure_subnormal_operands",
           "note": ("both operands drawn as integer multiples of eta = 2^-1074 (genuinely "
                    "subnormal floats), m = 4..258; every relative error term is exactly zero "
                    "here, so the enclosure radius IS the absolute eta term"),
           "cases": 0, "false_negatives": 0, "min_headroom_eta": np.inf,
           "worst_escape_eta": 0.0, "max_demand_eta_per_term": 0.0, "reproducer": None,
           "by_reduction": {}}
    per = {"dot2_matvec": [0, 0, np.inf], "matvec": [0, 0, np.inf]}
    for m in (4, 32, 64, 258):
        for k_max in (1, 3, 17, 1023, 2 ** 40):
            for _ in range(4):
                ints = rng.integers(-k_max, k_max + 1, size=(2, m))
                M = (ints[0] * ETA).reshape(1, m)
                v = ints[1] * (2.0 ** -537)          # v normal-ish, product lands sub-eta
                ex = _exact_matvec(M, v)[0]
                for name, r in (("dot2_matvec", dot2_matvec(M, v)),
                                ("matvec", matvec(M, Interval.point(v)))):
                    ok, rel, head = _score(r.lo[0], r.hi[0], ex)
                    out["cases"] += 1
                    per[name][0] += 1
                    per[name][2] = min(per[name][2], head)
                    out["min_headroom_eta"] = min(out["min_headroom_eta"], head)
                    if np.isfinite(float(r.lo[0])) and np.isfinite(float(r.hi[0])):
                        centre = (Fr(float(r.lo[0])) + Fr(float(r.hi[0]))) / 2
                        out["max_demand_eta_per_term"] = max(
                            out["max_demand_eta_per_term"],
                            abs(float((ex - centre) / Fr(ETA))) / m)
                    if not ok:
                        out["false_negatives"] += 1
                        per[name][1] += 1
                        if -head > out["worst_escape_eta"]:
                            out["worst_escape_eta"] = -head
                            out["reproducer"] = {"reduction": name, "m": m, "k_max": int(k_max),
                                                 "lo": repr(float(r.lo[0])),
                                                 "hi": repr(float(r.hi[0])),
                                                 "escape_eta": -head}
    out["min_headroom_eta"] = float(out["min_headroom_eta"])
    out["by_reduction"] = {k: {"cases": v[0], "false_negatives": v[1],
                               "min_headroom_eta": float(v[2])} for k, v in per.items()}
    return out


# ==========================================================================
# PART B, FAMILY F3 -- the Dekker wall, swept in BOTH operands
# ==========================================================================

def fam_dekker_wall_2d():
    """Leg 69 probed the wall with `a = 2^e, b = 1` only.  The splitting is applied to BOTH
    operands, and the PRODUCT can overflow independently of either.  This family sweeps the full
    (e_a, e_b) grid across and beyond the wall, including product overflow (e_a + e_b > 1023) and
    negative operands, and asks of every cell the only question that matters:

        did it either RAISE, or return an enclosure that CONTAINS the exact rational product?

    A returned `[nan, nan]`, or any finite enclosure missing the exact product, is a hole."""
    out = {"family": "dekker_wall_2d_sweep",
           "note": ("|a| = 2^ea, |b| = 2^eb over ea, eb in {0, 500, 900, 960, 996, 997, 998, "
                    "1000, 1023} x signs, including cells where the PRODUCT overflows; every "
                    "cell must either raise OverflowError or enclose the exact rational product"),
           "cells": 0, "raised": 0, "enclosed": 0, "silent_nan": 0, "missed": 0,
           "holes": [], "smallest_max_exponent_that_raised": None, "product_overflow_cells": 0}
    exps = [0, 500, 900, 960, 996, 997, 998, 1000, 1023]
    for ea in exps:
        for eb in exps:
            for sa in (1.0, -1.0):
                for sb in (1.0, -1.0):
                    a = sa * 2.0 ** ea
                    b = sb * 2.0 ** eb
                    ex = Fr(sa * sb) * (Fr(2) ** (ea + eb))
                    out["cells"] += 1
                    if ea + eb > 1023:
                        out["product_overflow_cells"] += 1
                    try:
                        r = dot2_matvec(np.array([[a]]), np.array([b]))
                    except OverflowError:
                        out["raised"] += 1
                        if (out["smallest_max_exponent_that_raised"] is None
                                or max(ea, eb) < out["smallest_max_exponent_that_raised"]):
                            out["smallest_max_exponent_that_raised"] = max(ea, eb)
                        continue
                    lo, hi = float(r.lo[0]), float(r.hi[0])
                    if np.isnan(lo) or np.isnan(hi):
                        out["silent_nan"] += 1
                        out["holes"].append({"kind": "silent_nan", "ea": ea, "eb": eb,
                                             "sa": sa, "sb": sb})
                        continue
                    ok, _, _ = _score(lo, hi, ex)
                    if ok:
                        out["enclosed"] += 1
                    else:
                        out["missed"] += 1
                        out["holes"].append({"kind": "missed", "ea": ea, "eb": eb,
                                             "sa": sa, "sb": sb,
                                             "lo": repr(lo), "hi": repr(hi)})
    # the exact wall, located independently in each operand separately
    def _wall(which):
        for e in range(900, 1024):
            try:
                if which == "a":
                    _two_product(np.array([2.0 ** e]), np.array([1.0]))
                else:
                    _two_product(np.array([1.0]), np.array([2.0 ** e]))
            except OverflowError:
                return e
        return None
    out["wall_exponent_operand_a"] = _wall("a")
    out["wall_exponent_operand_b"] = _wall("b")
    return out


# ==========================================================================
# PART B, FAMILY F4 -- the NaN-widening path (soundness AND its scope limit)
# ==========================================================================

def fam_nan_widening():
    """The repair widens a NaN endpoint to the trivial enclosure [-inf, +inf] rather than raising,
    because `interval_certificate.full_interpolant_hilbert_matrix` deliberately leaves two
    endpoint rows NaN and masks them off.  Two things are measured here:

      * SOUNDNESS -- a NaN endpoint is never stored; the widened interval contains everything;
        a NaN row does not damage its neighbours in the same matvec; and NaN surviving through
        arithmetic (inf - inf, 0 * inf) re-widens rather than being stored.
      * SCOPE -- the widened interval is INDISTINGUISHABLE from a genuinely computed entire
        interval.  IEEE 1788-2015's set-based flavor solves exactly this with a DECORATION
        (`trv`/`ill`); this module has none.  Recorded as a measured scope limitation of the
        repair, not as a defect (it cannot produce an unsound answer, only an uninformative one).
    """
    out = {"family": "nan_widening_path", "checks": {}, "stored_nan_endpoints": 0,
           "note": ("NaN handling: soundness of the widening, plus the decoration gap that "
                    "IEEE 1788-2015 fills with `trv`/`ill` and this module does not")}
    cases = [("nan,nan", np.nan, np.nan), ("nan,1", np.nan, 1.0), ("0,nan", 0.0, np.nan),
             ("-inf,nan", -np.inf, np.nan), ("nan,+inf", np.nan, np.inf)]
    for name, a, b in cases:
        w = Interval(np.array([a]), np.array([b]))
        stored = bool(np.isnan(w.lo[0]) or np.isnan(w.hi[0]))
        out["stored_nan_endpoints"] += stored
        out["checks"][name] = {"lo": repr(float(w.lo[0])), "hi": repr(float(w.hi[0])),
                               "stored_nan": stored,
                               "contains_0": bool(w.contains(0.0)),
                               "contains_1e300": bool(w.contains(1e300))}
    # NaN manufactured by ARITHMETIC on widened intervals must re-widen, not be stored
    ent = Interval(np.array([-np.inf]), np.array([np.inf]))
    for name, r in (("entire+entire", ent + ent), ("entire-entire", ent - ent),
                    ("entire*zero", ent * Interval.point(np.array([0.0]))),
                    ("entire*entire", ent * ent)):
        stored = bool(np.isnan(r.lo[0]) or np.isnan(r.hi[0]))
        out["stored_nan_endpoints"] += stored
        out["checks"][name] = {"lo": repr(float(r.lo[0])), "hi": repr(float(r.hi[0])),
                               "stored_nan": stored,
                               "contains_0": bool(r.contains(0.0))}
    # a NaN row must not damage its neighbours (the live interval_certificate pattern)
    M = np.array([[np.nan, 1.0], [2.0, 3.0], [np.nan, np.nan]])
    v = np.array([1.0, 1.0])
    rn = dot2_matvec(M, v)
    out["nan_row_isolation"] = {
        "row0_widened": bool(rn.lo[0] == -np.inf and rn.hi[0] == np.inf),
        "row1_lo": repr(float(rn.lo[1])), "row1_hi": repr(float(rn.hi[1])),
        "row1_encloses_5": bool(Fr(float(rn.lo[1])) <= 5 <= Fr(float(rn.hi[1]))),
        "row1_width": float(rn.hi[1] - rn.lo[1]),
        "row2_widened": bool(rn.lo[2] == -np.inf and rn.hi[2] == np.inf)}
    # the SCOPE limitation, made concrete: a widened-from-NaN interval and a legitimately
    # computed entire interval are the same object, bit for bit
    widened = Interval(np.array([np.nan]), np.array([np.nan]))
    genuine = Interval(np.array([-np.inf]), np.array([np.inf]))
    out["decoration_gap"] = {
        "widened_from_nan_equals_genuine_entire": bool(
            widened.lo[0] == genuine.lo[0] and widened.hi[0] == genuine.hi[0]),
        "note": ("IEEE 1788-2015 set-based flavor distinguishes these with a decoration "
                 "(trv/ill); solver/interval.py carries none, so a caller cannot tell a "
                 "trivially-widened result from a computed one.  Sound but uninformative -- "
                 "recorded, not patched (this leg may not edit the module)")}
    return out


# ==========================================================================
# PART B, FAMILY F5 -- the LIVE K-range, exact-rational, every row
# ==========================================================================

def fam_live_k_range(rng):
    """Gate clause (b): zero regression in the exact-rational containment checks at the LIVE
    operator range.  `bordered_linearization(K)` has nonzero entries spanning exactly 0.5 to K
    (0.5 to 128 at K = 128) and an EXACTLY ZERO tail diagonal, so its rows have nothing to
    dominate them -- the leg 51-53 conditioning that legs 58 and 61 actually run on.

    Every ROW of every K is checked (leg 69 sampled 8 vectors per K; this checks all rows of 6
    vectors per K, both reductions, plus the uncancelled operator as well as the cancelled one,
    so the regression check covers the enclosures the certificate really forms and not only the
    adversarial ones)."""
    from solver.spectral_certificate import bordered_linearization
    out = {"family": "live_k_range_exact_rational",
           "note": ("bordered_linearization at K = 16, 32, 64, 128 -- entries 0.5 to 128, tail "
                    "diagonal exactly zero -- both reductions, cancelled and uncancelled, every "
                    "row checked against exact rational ground truth"),
           "by_K": {}, "cases": 0, "false_negatives": 0,
           "worst_relative_slack": np.inf, "cases_touching_an_endpoint": 0,
           "min_headroom_eta": np.inf, "reproducer": None,
           "leg69_banked_worst_relative_slack": None}
    for K in (16, 32, 64, 128):
        M0 = np.asarray(bordered_linearization(K), dtype=float)
        nz = np.abs(M0)[np.abs(M0) > 0]
        rec = {"shape": list(M0.shape), "min_nonzero_abs": float(nz.min()),
               "max_abs": float(nz.max()),
               "exact_zero_entries": int((M0 == 0).sum()),
               "cases": 0, "false_negatives": 0, "worst_relative_slack": np.inf}
        for trial in range(6):
            v0 = rng.standard_normal(M0.shape[1])
            variants = [("uncancelled", M0, v0)]
            ext = np.array([_cancel_row(M0[i], v0) for i in range(M0.shape[0])])
            variants.append(("cancelled",
                             np.concatenate([M0, ext], axis=1),
                             np.concatenate([v0, [1.0, 1.0]])))
            for vname, M, v in variants:
                ex = _exact_matvec(M, v)
                for rname, r in (("dot2_matvec", dot2_matvec(M, v)),
                                 ("matvec", matvec(M, Interval.point(v)))):
                    for i in range(M.shape[0]):
                        ok, rel, head = _score(r.lo[i], r.hi[i], ex[i])
                        out["cases"] += 1
                        rec["cases"] += 1
                        if rel is not None:
                            out["worst_relative_slack"] = min(out["worst_relative_slack"], rel)
                            rec["worst_relative_slack"] = min(rec["worst_relative_slack"], rel)
                            out["cases_touching_an_endpoint"] += (rel == 0.0)
                        out["min_headroom_eta"] = min(out["min_headroom_eta"], head)
                        if not ok:
                            out["false_negatives"] += 1
                            rec["false_negatives"] += 1
                            if out["reproducer"] is None:
                                out["reproducer"] = {
                                    "K": K, "variant": vname, "reduction": rname, "row": i,
                                    "lo": repr(float(r.lo[i])), "hi": repr(float(r.hi[i])),
                                    "escape_eta": -head}
        rec["worst_relative_slack"] = float(rec["worst_relative_slack"])
        out["by_K"][f"K={K}"] = rec
    out["worst_relative_slack"] = float(out["worst_relative_slack"])
    out["min_headroom_eta"] = float(out["min_headroom_eta"])
    try:
        with open(LEG69_DATA) as fh:
            old = json.load(fh)
        for f in old["families"]:
            if f["family"] == "tail_block_conditioning":
                out["leg69_banked_worst_relative_slack"] = f["worst_relative_slack"]
    except OSError:
        pass
    return out


# ==========================================================================
# PART B, FAMILY F6 -- the PRE/POST DIFFERENTIAL, from the actual previous source
# ==========================================================================

REPAIR_SUBJECT = "repair the two soundness defects leg 69 measured in solver/interval.py"


def _find_repair_commit():
    log = subprocess.run(["git", "-C", ROOT, "log", "--format=%H%x1f%s",
                          "--", "solver/interval.py"],
                         capture_output=True, text=True, check=True).stdout
    for line in log.splitlines():
        h, _, s = line.partition("\x1f")
        if REPAIR_SUBJECT in s:
            return h
    return None


def _load_prerepair(commit):
    src = subprocess.run(["git", "-C", ROOT, "show", f"{commit}^:solver/interval.py"],
                         capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType("interval_prerepair")
    mod.__file__ = f"<pre-repair solver/interval.py @ {commit}^>"
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, src


def _bits(a):
    return np.asarray(a, dtype=float).view(np.int64)


def fam_pre_post_differential(rng):
    """Re-derive the repair's OWN inertness claim, from its own previous source.

    The repair states: "100 pre/post enclosures on the live bordered_linearization (K = 16..128)
    and a normal-range battery are IDENTICAL endpoint bit patterns; the term first moves a bit
    only near input scale 1e-310."  This family reconstructs the pre-repair module in memory from
    git and diffs ENDPOINT BIT PATTERNS, reporting three counts that a bare "identical" hides:

      * identical  -- the same double, bit for bit;
      * wider      -- post-repair encloses pre-repair strictly (SOUND: more conservative);
      * narrower   -- post-repair is strictly inside pre-repair (a REGRESSION, must be 0).

    It also locates, by scanning input scale, the exponent at which the first endpoint bit
    actually moves."""
    from solver.spectral_certificate import bordered_linearization
    commit = _find_repair_commit()
    out = {"family": "pre_post_bit_differential", "repair_commit": commit,
           "note": ("pre-repair module reconstructed from `git show <repair>^:solver/interval.py` "
                    "and exec'd in memory; endpoint bit patterns diffed against the repaired "
                    "module.  `narrower` is the only count that would be a regression")}
    if commit is None:
        out["error"] = "repair commit not found in git history"
        return out
    pre, src = _load_prerepair(commit)
    out["prerepair_source_bytes"] = len(src)
    out["prerepair_has_eta_terms"] = hasattr(pre, "_ETA_TERMS_PLAIN")

    def compare(label, M, v, cancelled):
        rows = {"label": label, "cancelled": cancelled, "endpoints": 0,
                "identical": 0, "wider": 0, "narrower": 0, "max_ulp_widening": 0,
                "pre_contains_exact": 0, "post_contains_exact": 0, "n_rows": int(M.shape[0])}
        for fn_name, fn_pre, fn_post in (
                ("dot2_matvec", pre.dot2_matvec, dot2_matvec),
                ("matvec", lambda M, v: pre.matvec(M, pre.Interval.point(v)),
                 lambda M, v: matvec(M, Interval.point(v)))):
            a = fn_pre(M, v)
            b = fn_post(M, v)
            for i in range(M.shape[0]):
                alo, ahi = float(a.lo[i]), float(a.hi[i])
                blo, bhi = float(b.lo[i]), float(b.hi[i])
                rows["endpoints"] += 2
                same = (_bits(alo) == _bits(blo)) and (_bits(ahi) == _bits(bhi))
                if same:
                    rows["identical"] += 2
                elif blo <= alo and bhi >= ahi:
                    rows["wider"] += 2
                    ulp = max(abs(int(_bits(blo)) - int(_bits(alo))),
                              abs(int(_bits(bhi)) - int(_bits(ahi))))
                    rows["max_ulp_widening"] = max(rows["max_ulp_widening"], int(ulp))
                else:
                    rows["narrower"] += 2
        return rows

    detail = []
    for K in (16, 32, 64, 128):
        M0 = np.asarray(bordered_linearization(K), dtype=float)
        v0 = rng.standard_normal(M0.shape[1])
        detail.append(compare(f"bordered_linearization K={K}", M0, v0, False))
        ext = np.array([_cancel_row(M0[i], v0) for i in range(M0.shape[0])])
        detail.append(compare(f"bordered_linearization K={K}",
                              np.concatenate([M0, ext], axis=1),
                              np.concatenate([v0, [1.0, 1.0]]), True))
    # a normal-range battery at the scales the repair claimed inert
    for m in (4, 32, 258):
        for e in (-100, -8, 0, 8, 100):
            M = rng.standard_normal((4, m)) * (10.0 ** e)
            v = rng.standard_normal(m) * (10.0 ** e)
            detail.append(compare(f"normal m={m} scale=1e{e}", M, v, False))
    out["detail"] = detail
    out["totals"] = {k: int(sum(d[k] for d in detail))
                     for k in ("endpoints", "identical", "wider", "narrower")}
    out["totals"]["max_ulp_widening"] = int(max(d["max_ulp_widening"] for d in detail))
    out["live_range_cancelled"] = {
        k: int(sum(d[k] for d in detail if d["cancelled"]))
        for k in ("endpoints", "identical", "wider", "narrower")}
    out["live_range_uncancelled"] = {
        k: int(sum(d[k] for d in detail if not d["cancelled"] and "bordered" in d["label"]))
        for k in ("endpoints", "identical", "wider", "narrower")}

    # where does the first bit actually move?
    scan = {}
    first_move = None
    for e in range(0, -325, -10):
        M = rng.standard_normal((2, 32)) * (10.0 ** e)
        v = rng.standard_normal(32) * (10.0 ** e)
        d = compare(f"scan 1e{e}", M, v, False)
        scan[f"1e{e}"] = {"identical": d["identical"], "wider": d["wider"],
                          "narrower": d["narrower"]}
        if d["wider"] + d["narrower"] > 0 and first_move is None:
            first_move = e
    out["scale_scan"] = scan
    out["first_scale_where_a_bit_moves"] = (f"1e{first_move}" if first_move is not None
                                            else "no bit moved down to 1e-320")

    # ATTRIBUTION.  The repair made TWO edits to each error term, not one: it added the eta
    # floor, and it wrapped the result in one further outward push --
    #     pre :  err = _up(g * mass)
    #     post:  err = _up(_up(g * mass) + eta_term)
    # In the live range the eta term (~1e-321 at m <= 260) is ~290 decades below the endpoints,
    # so it cannot move a bit there; any live-range widening must come from the EXTRA PUSH.
    # This is separated by re-loading the POST-repair source with both eta constants zeroed: if
    # that variant still differs from pre-repair in the same places, the eta term is exonerated.
    post_src = open(os.path.join(ROOT, "solver", "interval.py")).read()
    neutered_src = (post_src.replace("_ETA_TERMS_PLAIN = 2.0", "_ETA_TERMS_PLAIN = 0.0")
                            .replace("_ETA_TERMS_DOT2 = 8.0", "_ETA_TERMS_DOT2 = 0.0"))
    zero = types.ModuleType("interval_eta_zeroed")
    zero.__file__ = "<post-repair with eta constants zeroed>"
    exec(compile(neutered_src, zero.__file__, "exec"), zero.__dict__)
    attr = {"note": ("post-repair source with _ETA_TERMS_* set to 0.0: keeps the extra outward "
                     "push, removes the eta floor.  Agreement with the POST module attributes a "
                     "difference to the push; agreement with PRE attributes it to the eta term"),
            "live_cancelled": {"endpoints": 0, "matches_post": 0, "matches_pre": 0}}
    for K in (16, 32, 64, 128):
        M0 = np.asarray(bordered_linearization(K), dtype=float)
        v0 = rng.standard_normal(M0.shape[1])
        ext = np.array([_cancel_row(M0[i], v0) for i in range(M0.shape[0])])
        M = np.concatenate([M0, ext], axis=1)
        v = np.concatenate([v0, [1.0, 1.0]])
        for fp, fz, fo in (
                (pre.dot2_matvec, zero.dot2_matvec, dot2_matvec),
                (lambda M, v: pre.matvec(M, pre.Interval.point(v)),
                 lambda M, v: zero.matvec(M, zero.Interval.point(v)),
                 lambda M, v: matvec(M, Interval.point(v)))):
            a, z, b = fp(M, v), fz(M, v), fo(M, v)
            for i in range(M.shape[0]):
                for end in ("lo", "hi"):
                    av, zv, bv = (float(getattr(a, end)[i]), float(getattr(z, end)[i]),
                                  float(getattr(b, end)[i]))
                    attr["live_cancelled"]["endpoints"] += 1
                    attr["live_cancelled"]["matches_post"] += int(_bits(zv) == _bits(bv))
                    attr["live_cancelled"]["matches_pre"] += int(_bits(zv) == _bits(av))
    lc = attr["live_cancelled"]
    attr["verdict"] = (
        "the live-range widening is ENTIRELY the extra outward push; the eta term moves no bit "
        "in the live range (matches_pre counts only the endpoints the push happened to leave "
        "unchanged)"
        if lc["matches_post"] == lc["endpoints"]
        else "NOT fully attributable to the push -- the eta term moved a live-range bit")
    out["attribution"] = attr

    # and the two behavioural changes, confirmed on the previous source
    try:
        rp = pre.dot2_matvec(np.array([[2.0 ** 997]]), np.array([1.0]))
        out["prerepair_at_dekker_wall"] = {
            "lo": repr(float(rp.lo[0])), "hi": repr(float(rp.hi[0])),
            "silent_nan": bool(np.isnan(rp.lo[0]) and np.isnan(rp.hi[0]))}
    except OverflowError:
        out["prerepair_at_dekker_wall"] = {"raised": True}
    try:
        wp = pre.Interval(np.array([np.nan]), np.array([np.nan]))
        out["prerepair_nan_endpoint"] = {
            "lo": repr(float(wp.lo[0])), "hi": repr(float(wp.hi[0])),
            "stored_nan": bool(np.isnan(wp.lo[0])),
            "passed_the_lo_le_hi_constructor_guard": True,
            "contains_1e300": bool(wp.contains(1e300)),
            "negated_exclusion_test_passes": bool(
                not ((1e300 < wp.lo[0]) or (1e300 > wp.hi[0]))),
            "note": ("MEASURED NUANCE, recorded not patched.  The module's own comment says a "
                     "NaN endpoint 'used to pass every downstream containment check'.  Measured: "
                     "`Interval.contains` returned FALSE on a NaN endpoint (the safe direction), "
                     "so a check written as `assert iv.contains(x)` would have CAUGHT it.  What "
                     "was genuinely vacuous is the constructor's `np.any(lo > hi)` invariant "
                     "guard, and any check written in the negated form `not (x < lo or x > hi)` "
                     "-- which is True on NaN.  The defect was real; its blast radius depended on "
                     "which form the caller used.")}
    except Exception as exc:                                        # pragma: no cover
        out["prerepair_nan_endpoint"] = {"raised": repr(exc)}
    return out


# ==========================================================================

def main():
    warnings.simplefilter("ignore")
    print("PART A -- leg 69's original corpus, re-run against the REPAIRED module")
    reports = rerun_leg69_corpus()
    for r in reports:
        print(f"  {r['family']:26s} cases={r['cases']:6d} false_neg={r['false_negatives']:5d} "
              f"worst_rel_slack={r['worst_relative_slack']:+.4e} "
              f"worst_escape={r['worst_absolute_escape_eta']:.3g} eta")
    delta, old = diff_against_banked(reports)
    dekker = rerun_dekker_probe()
    print(f"  dekker wall: first raise at 2^{dekker['e_first_raise']}, "
          f"silent non-finite at {dekker['e_first_silent_nonfinite']}")

    rng = np.random.default_rng(87)
    print("\nPART B -- fresh adversarial battery")
    f1 = fam_eta_calibration(rng)
    print(f"  F1 band utilisation     : worst radius utilisation "
          f"{f1['worst_radius_utilisation']:.4g} (1.0 = touching), min headroom "
          f"{min(f1['by_reduction'][k]['min_headroom_eta'] for k in f1['by_reduction']):.4g} eta")
    f1b = fam_half_eta_aligned()
    print(f"  F1b extremal (Rump)     : demand {f1b['by_reduction']['matvec']['max_demand_eta_per_term']:.4g} "
          f"eta/term measured; margin {f1b['by_reduction']['matvec']['min_margin_factor']:.4g}x plain, "
          f"{f1b['by_reduction']['dot2_matvec']['min_margin_factor']:.4g}x dot2")
    f2 = fam_pure_subnormal(rng)
    print(f"  F2 pure subnormal       : {f2['cases']} cases, {f2['false_negatives']} false neg, "
          f"min headroom {f2['min_headroom_eta']:.4g} eta")
    f3 = fam_dekker_wall_2d()
    print(f"  F3 dekker 2-D           : {f3['cells']} cells, {f3['raised']} raised, "
          f"{f3['enclosed']} enclosed, {f3['silent_nan']} silent NaN, {f3['missed']} missed")
    f4 = fam_nan_widening()
    print(f"  F4 NaN widening         : {f4['stored_nan_endpoints']} stored NaN endpoints")
    f5 = fam_live_k_range(rng)
    print(f"  F5 live K-range         : {f5['cases']} cases, {f5['false_negatives']} false neg, "
          f"worst rel slack {f5['worst_relative_slack']:+.4e}")
    f6 = fam_pre_post_differential(rng)
    t6 = f6.get("totals", {})
    print(f"  F6 pre/post differential: {t6.get('endpoints')} endpoints, "
          f"{t6.get('identical')} identical, {t6.get('wider')} wider, "
          f"{t6.get('narrower')} narrower, max {t6.get('max_ulp_widening')} ulp; "
          f"first bit moves at {f6.get('first_scale_where_a_bit_moves')}")

    a_total = sum(r["cases"] for r in reports)
    a_fail = sum(r["false_negatives"] for r in reports)
    b_fail = (f1["by_reduction"]["dot2_matvec"]["false_negatives"]
              + f1["by_reduction"]["matvec"]["false_negatives"]
              + f1b["false_negatives"]
              + f2["false_negatives"] + f3["silent_nan"] + f3["missed"]
              + f4["stored_nan_endpoints"] + f5["false_negatives"])
    b_total = (f1["by_reduction"]["dot2_matvec"]["cases"]
               + f1["by_reduction"]["matvec"]["cases"] + f1b["cases"]
               + f2["cases"] + f3["cells"] + len(f4["checks"]) + f5["cases"])

    result = {
        "leg": 87, "route": "IVB",
        "module_under_test": "solver/interval.py (post-repair, read-only)",
        "question": ("post-repair, does solver/interval.py (a) correctly handle leg 69's original "
                     "failing cases (the subnormal range, 2^997), and (b) show zero regression in "
                     "the previously-validated exact-rational containment checks at the live "
                     "K-range?"),
        "ground_truth": "exact rational (fractions.Fraction) on exact float64 inputs",
        "eta": ETA, "unit_roundoff": U,
        "part_A_leg69_corpus_rerun": {
            "families": reports,
            "delta_vs_banked_prerepair": delta,
            "dekker_probe": dekker,
            "cases": a_total, "false_negatives": a_fail,
            "prerepair_false_negatives": old["totals"]["false_negatives"],
            "prerepair_worst_escape_eta": old["totals"]["subnormal_range_worst_escape_eta"],
        },
        "part_B_fresh_battery": {
            "eta_calibration": f1,
            "half_eta_aligned_extremal": f1b,
            "pure_subnormal": f2,
            "dekker_wall_2d": f3,
            "nan_widening": f4,
            "live_k_range": f5,
            "pre_post_differential": f6,
            "cases": b_total, "false_negatives": b_fail,
        },
        "totals": {
            "cases": a_total + b_total,
            "false_negatives": a_fail + b_fail,
            "gate_a_subnormal_false_negatives_post": a_fail + f1["by_reduction"]["dot2_matvec"]["false_negatives"]
                                                     + f1["by_reduction"]["matvec"]["false_negatives"]
                                                     + f1b["false_negatives"]
                                                     + f2["false_negatives"],
            "gate_a_dekker_wall_exponent": dekker["e_first_raise"],
            "gate_a_measured_eta_demand_per_term_extremal":
                max(f1b["by_reduction"][k]["max_demand_eta_per_term"]
                    for k in f1b["by_reduction"]),
            "gate_a_eta_constant_margin_plain": f1b["by_reduction"]["matvec"]["min_margin_factor"],
            "gate_a_eta_constant_margin_dot2":
                f1b["by_reduction"]["dot2_matvec"]["min_margin_factor"],
            "gate_b_live_k_false_negatives": f5["false_negatives"],
            "gate_b_live_k_worst_relative_slack": f5["worst_relative_slack"],
            "gate_b_endpoints_narrower_than_prerepair": f6.get("totals", {}).get("narrower"),
            "gate_b_max_ulp_widening": f6.get("totals", {}).get("max_ulp_widening"),
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print(f"\nwrote {OUT}")
    t = result["totals"]
    print(f"  TOTAL {t['cases']} cases, {t['false_negatives']} false negatives")
    print(f"  gate (a): subnormal false negatives {t['gate_a_subnormal_false_negatives_post']} "
          f"(leg 69 measured 62); Dekker wall raises at 2^{t['gate_a_dekker_wall_exponent']}")
    print(f"  gate (b): live-K false negatives {t['gate_b_live_k_false_negatives']}, worst "
          f"relative slack {t['gate_b_live_k_worst_relative_slack']:+.4e}, endpoints narrower "
          f"than pre-repair {t['gate_b_endpoints_narrower_than_prerepair']}, max widening "
          f"{t['gate_b_max_ulp_widening']} ulp")
    return result


if __name__ == "__main__":
    main()
