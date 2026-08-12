"""Route-CRVB v1 (leg 388) -- the curvature blind spot of the certified decay
enclosure, bounded from BELOW.

=============================================================================
WIP -- THIS RUNNER WAS **NEVER EXECUTED**.  IT PRODUCED NO NUMBERS AT ALL.
=============================================================================
The run was stopped by a wind-down instruction before the first measurement.
Concretely, and this is the whole status:

  * `main()` has NEVER been called.  `writeup/data/p2_route_crvb_v1.json` DOES
    NOT EXIST and no figure was drawn.
  * NOT ONE LADDER RUNG WAS MEASURED, at any working precision, on any grid.
    Leg 382's `<= 1e-6` therefore still stands EXACTLY as it stood: the
    curvature blind spot has a ceiling and NO FLOOR, and this leg did not
    move it.
  * **THE GATE IS UNANSWERED.**  Not YES, not NO.  See
    `experiments/journal/leg_388.md` Part II.
  * Every number appearing in this file is a **PRE-REGISTERED PREDICTION**
    (journal Part I Section 2), never a measurement:  kappa* = 8*h_eff/W^2,
    the float64 prediction ~5.8e-16, the predicted bracket [1e-16, 1e-15],
    the -1.00 slope per Decimal digit, the window ratios x2.67 / x0.32 and
    the tolerance coefficient 0.377435 on [10,1000].  **NONE OF THEM HAS
    BEEN TESTED.  DO NOT QUOTE ANY OF THEM AS A RESULT.**
  * The code itself is UNTESTED and unrun: it has never been imported,
    executed, or syntax-exercised beyond being written.  A successor must
    assume it is broken until it runs.

WHAT A SUCCESSOR MUST REDO: everything downstream of construction.  What is
reusable without re-derivation is the novelty pass (commit 5cbe659, which
found that `solver/interval_mp.py` ALREADY holds rigorous Decimal
directed-rounded intervals, so none must be written) and the pre-registration
(commit f2084ae), both of which were committed BEFORE any measurement -- and,
since no measurement ever happened, no number in this branch is at risk of
having outrun its pre-registration.
=============================================================================

WHAT THIS IS.  Leg 382 built `solver/dssp_decay_enclosure.py` and probed its resolving
power with a planted-curvature ladder whose smallest non-zero rung was `kappa = 1e-6`.
Every rung was detected, so its banked answer -- `smallest_kappa_certified_empty = 1e-06`
-- is a statement about the LADDER, not the instrument: the blind spot had a ceiling and
no floor.  This runner supplies the floor, as a two-sided bracket [fail, detect] measured
on a ladder stepping exactly one decade, at three arithmetics.

WHAT "FAIL" MEANS, AND WHAT IT DOES NOT.  For every kappa > 0 the certified set P_cert is
genuinely empty, so a returned INTERVAL is the SOUND-BUT-UNINFORMATIVE answer, never an
unsound one: emptiness is a proof and non-emptiness never was.  The blind spot is a loss
of RESOLVING POWER, not of rigour.

NOTHING NEW IS BUILT.  Per the standing ban (`plan_of_record.py`: "building a solver
without grepping capabilities.py for the object first"), the capabilities grep was run
BEFORE construction and recorded in `writeup/novelty/leg_388.md` Section 2.  It found:

  * `solver/interval.py`      -- float64 outward-rounded intervals  (leg 382's substrate)
  * `solver/interval_mp.py`   -- RIGOROUS arbitrary-precision directed-rounded interval
                                 arithmetic backed by `decimal.Decimal` (Route-APIA, leg
                                 312), Section 1 `MPInterval` / `mp_add` / `mp_sub` /
                                 `mp_mul` / `mp_div`

so the arbitrary-precision layer this leg needs ALREADY EXISTS and is imported, not
written.  The Fourier-Motzkin elimination is likewise imported from leg 382's module
(`_fourier_motzkin_p_range`) for the float arms.  The ONE new routine is that same
elimination re-expressed over `MPInterval`, which is unavoidable because the landed one is
numpy/float64 by construction; it mirrors the landed code line for line and is
cross-validated against it (control AGREEMENT).

`solver/` IS READ-ONLY ON THIS BRANCH.  Nothing here imports for mutation.

COORDINATES.  With `t = log r` and `g = log f`, a power law is an affine `c - p*t`.  Arm A
uses leg 382's own multiplicative generator `f = C r^-p (1 + kappa*u^2)`, `u = t - t_mid`,
through the landed entry point unmodified.  Arms B and C plant the curvature ADDITIVELY in
the log-log plane, `g(t) = log C - p0*t + kappa*u^2` (i.e. `f = C r^-p exp(kappa u^2)`),
because `solver/interval_mp.py` HAS NO LOGARITHM -- see the novelty pass.  `g` is then a
polynomial in `t` and no transcendental is ever needed at high precision.  The two forms
differ at order kappa^2 and the AGREEMENT control measures that they give the same
threshold.

Pre-registration: `experiments/journal/leg_388.md` Part I, commit f2084ae, which is the
parent of this file's commit.  Every prediction it makes is checked here and reported
whether or not it held.

CEILING.  Measuring an instrument's blind spot moves NO link of the L1->L4 chain.
`CLAY_OBLIGATIONS.md` Section 6 items 1 and 2 stay OPEN.  No profile of route 4's object
exists; every profile here is a planted analytic known.  TIER 2.  Clay ~0.05%.
"""

from __future__ import annotations

import json
import os
import sys
from decimal import Decimal

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.dssp_decay_enclosure import (  # noqa: E402
    DEFAULT_P_BRACKET,
    VERDICT_EMPTY,
    VERDICT_INCAPACITY,
    VERDICT_INTERVAL,
    _fourier_motzkin_p_range,
    certified_decay_from_cell_enclosures,
    certified_decay_interval,
    planted_curvature,
)
from solver.interval import Interval, _down, _up  # noqa: E402
from solver.interval_mp import (  # noqa: E402
    MPInterval,
    _ceil_ctx,
    _floor_ctx,
    mp_add,
    mp_div,
    mp_mul,
    mp_sub,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_crvb_v1.json")

# ---------------------------------------------------------------------------
# PRE-REGISTERED SETTINGS (journal Part I Section 4) -- IMMUTABLE FOR THIS LEG
# ---------------------------------------------------------------------------
R0_PRIMARY, R1_PRIMARY = 10.0, 1000.0      # leg 382's window, unchanged
N_GATE = 1000                              # leg 382's gate cell count
P0 = 2.0                                   # planted exponent
C_AMP = 1.0                                # planted amplitude
KAPPA_RED = 1e-3                           # ZC-RED: the demonstrated red path
JITTER_SEEDS = (388, 389, 390, 391, 392)
PRECISIONS = (20, 30, 50)
N_ARM_C = 50                               # Decimal elimination is O(N^2) scalar ops
N_LIST_SMOOTH = (50, 100, 200, 500, 1000, 2000)
N_LIST_COMMENSURABILITY = (97, 100, 101, 110, 997, 1000, 1001, 1010, 1100, 1500)

# Arms B/C run in EXACT DECIMAL t-coordinates.  Leg 382's window has
# t0 = log 10 = 2.302585092994046..., W = log 100 = 4.605170185988091..., both
# transcendental and so not exactly representable in Decimal at any precision.  The
# t-space arms therefore use the DECLARED EXACT DECIMAL window below, which differs from
# leg 382's in the 7th significant figure (relative 4.0e-8 in W).  Declared, not hidden:
# the model's prediction depends on the window only through W^2 and |g|_max, so a 4e-8
# relative shift is 8 orders of magnitude below the one-decade granularity of the gate,
# and every arm quotes its OWN W (leg 386: no bare constant, every width names its
# window).
T0_EXACT = Decimal("2.302585")
W_EXACT = Decimal("4.605170")
T1_EXACT = T0_EXACT + W_EXACT
TMID_EXACT = T0_EXACT + W_EXACT / 2


def _hyp(kind, detail):
    """The three fields EVERY row of this leg carries (standing rule, DM cycle 11g).

    Leg 385's X3 produced a certificate of width 7.438494264988549e-15,
    bit-indistinguishable from a true one and false about its profile; only the recorded
    hypothesis separated them.  These rows report an INSTRUMENT'S LIMITS, so the
    conditions they were measured under are the whole content of the row."""
    return {
        "hypothesis": kind,
        "hypothesis_detail": detail,
        "conditional_on": (
            "This row is a statement about the RESOLVING POWER of the certified decay "
            "enclosure under the stated arithmetic, window, cell count and tolerance, on "
            "a PLANTED analytic profile. It is NOT a statement about any profile of "
            "route 4's object (none exists), and a verdict of INTERVAL below the "
            "threshold is the SOUND-but-uninformative answer, not an unsound one: "
            "emptiness is a proof, non-emptiness never was. " + detail),
    }


# ===========================================================================
# 1.  ARM A -- leg 382's landed instrument, unmodified
# ===========================================================================

def arm_a_row(kappa, r0=R0_PRIMARY, r1=R1_PRIMARY, n_cells=N_GATE, delta=0.0):
    """One rung through the LANDED entry point, with leg 382's own generator."""
    t_mid = 0.5 * (np.log(r0) + np.log(r1))
    iv_fn, _ = planted_curvature(C_AMP, P0, kappa, t_mid)
    res = certified_decay_interval(iv_fn, r0, r1, n_cells=n_cells, mode="cells",
                                   rel_tolerance=delta)
    return {
        "arm": "A", "kappa": float(kappa), "r0": float(r0), "r1": float(r1),
        "n_cells": int(n_cells), "delta": float(delta),
        "verdict": res["verdict"], "p_lo": res["p_lo"], "p_hi": res["p_hi"],
        "width": res["width"], "leverage_W": float(np.log(r1 / r0)),
        "detected": res["verdict"] == VERDICT_EMPTY,
        **_hyp("EXACT-INTERVAL-EVALUATION/ARM-A-LANDED",
               "Arm A: leg 382's certified_decay_interval and planted_curvature "
               "(multiplicative form f = C r^-p (1 + kappa u^2)), float64, cells mode, "
               "called unmodified."),
    }


def arm_a_row_jittered(kappa, seed, n_cells=200, r0=R0_PRIMARY, r1=R1_PRIMARY):
    """Arm A on a JITTERED, non-geometric grid -- the commensurability killer.

    Leg 385 measured that refusal of a node-aligned violation on this instrument's family
    is a COMMENSURABILITY effect: it fired at N = 1100/1500 and not at
    N = 500/997/1001/1010/2000, so a violating profile can hide from any FIXED grid.  A
    random grid has no commensurability to have, so a threshold that survives it unchanged
    is not a grid artefact.  This calls the landed cell-enclosure entry point
    `certified_decay_from_cell_enclosures` directly, because the landed
    `certified_decay_interval` builds its own geomspace grid."""
    rng = np.random.default_rng(int(seed))
    t0, t1 = np.log(r0), np.log(r1)
    inner = rng.uniform(t0, t1, size=int(n_cells) - 1)
    edges = np.exp(np.concatenate([[t0], np.sort(inner), [t1]]))
    lo, hi = edges[:-1], edges[1:]
    t_mid = 0.5 * (t0 + t1)
    iv_fn, _ = planted_curvature(C_AMP, P0, kappa, t_mid)
    F = iv_fn(Interval(lo, hi))
    res = certified_decay_from_cell_enclosures(
        lo, hi, F.lo, F.hi, DEFAULT_P_BRACKET, 0.0,
        hypothesis="EXACT-INTERVAL-EVALUATION",
        hypothesis_detail="jittered non-geometric grid")
    return {
        "arm": "A-jitter", "kappa": float(kappa), "seed": int(seed),
        "n_cells": int(n_cells), "r0": float(r0), "r1": float(r1), "delta": 0.0,
        "min_cell_log_width": float(np.min(np.diff(np.log(edges)))),
        "max_cell_log_width": float(np.max(np.diff(np.log(edges)))),
        "verdict": res["verdict"], "p_lo": res["p_lo"], "p_hi": res["p_hi"],
        "width": res["width"], "detected": res["verdict"] == VERDICT_EMPTY,
        **_hyp("EXACT-INTERVAL-EVALUATION/ARM-A-JITTERED-GRID",
               "Arm A on a SEEDED RANDOM non-geometric cell grid (endpoints pinned); "
               "cell log-widths are unequal by construction, so no commensurability "
               "between the grid and the planted profile is possible."),
    }


# ===========================================================================
# 2.  ARMS B and C -- identical algorithm, two arithmetics
# ===========================================================================

def _t_edges_float(n_cells):
    t0, t1 = float(T0_EXACT), float(T1_EXACT)
    e = np.linspace(t0, t1, int(n_cells) + 1)
    return e[:-1], e[1:]


def _classify(p_lo, p_hi, bracket=DEFAULT_P_BRACKET):
    """Verdict classification, mirroring the landed module's own order exactly."""
    if p_lo > bracket[1] or p_hi < bracket[0]:
        return VERDICT_INCAPACITY
    if p_lo > p_hi:
        return VERDICT_EMPTY
    if p_lo <= bracket[0] or p_hi >= bracket[1]:
        return VERDICT_INCAPACITY
    return VERDICT_INTERVAL


def arm_b_row(kappa, n_cells=N_GATE, delta=0.0, t_edges=None):
    """Arm B: the LANDED Fourier-Motzkin elimination, fed t-space coordinates.

    g(t) = -P0*t + kappa*(t - t_mid)^2 (log C = 0).  Over a cell [a, b], g is strictly
    decreasing whenever |2*kappa*u| < P0 everywhere on the window -- asserted below -- so
    the cell enclosure is exactly [g(b), g(a)], pushed outward one ulp.  That the binding
    enclosure is attained at the cell EDGES for a monotone profile is leg 382's own
    measured finding (its journal Section 12a, which is why its certified width was
    N-independent)."""
    ta, tb = _t_edges_float(n_cells) if t_edges is None else t_edges
    tm = float(TMID_EXACT)
    slope_margin = 2.0 * abs(kappa) * float(W_EXACT) / 2.0
    if slope_margin >= P0:
        raise ValueError("g is not monotone on this window at kappa=%g; the edge "
                         "enclosure would be unsound" % kappa)

    def g_at(t):
        u = t - tm
        return -P0 * t + kappa * u * u

    g_hi = _up(g_at(ta))
    g_lo = _down(g_at(tb))
    if delta > 0.0:
        h = float(np.log1p(delta))
        g_hi, g_lo = _up(g_hi + h), _down(g_lo - h)
    p_lo, p_hi, n_drop, n_pairs = _fourier_motzkin_p_range(ta, tb, g_lo, g_hi,
                                                           DEFAULT_P_BRACKET)
    verdict = _classify(p_lo, p_hi)
    return {
        "arm": "B", "kappa": float(kappa), "n_cells": int(n_cells),
        "delta": float(delta), "verdict": verdict, "p_lo": float(p_lo),
        "p_hi": float(p_hi), "width": float(p_hi - p_lo), "n_dropped": int(n_drop),
        "n_pairs": int(n_pairs), "leverage_W": float(W_EXACT),
        "detected": verdict == VERDICT_EMPTY,
        **_hyp("EXACT-INTERVAL-EVALUATION/ARM-B-TSPACE-FLOAT64",
               "Arm B: additive log-plane curvature g(t) = -p0 t + kappa u^2, float64, "
               "cell enclosure by monotonicity (asserted) with one-ulp outward push, "
               "eliminated by leg 382's OWN _fourier_motzkin_p_range."),
    }


def _mp_fm(t_lo, t_hi, g_lo, g_hi, prec, bracket=DEFAULT_P_BRACKET):
    """THE ONE NEW ROUTINE: leg 382's elimination over `MPInterval`.

    Mirrors `solver/dssp_decay_enclosure._fourier_motzkin_p_range` statement for
    statement -- same relaxation, same pair loop, same drop rule, same outward direction.
    Only the arithmetic differs: `solver/interval_mp.py`'s Decimal-backed directed
    rounding replaces numpy's one-ulp `nextafter` push.  Scalar, because `MPInterval` is
    scalar by design (its own docstring says an array generalization is out of scope), so
    the cost is O(K^2) Python-level Decimal operations and the cell count is chosen
    accordingly."""
    K = len(t_lo)
    p_lo = Decimal(bracket[0])
    p_hi = Decimal(bracket[1])
    n_dropped = 0
    n_pairs = 0
    for k in range(K):
        tlk, glk = t_lo[k], g_lo[k]
        for m in range(K):
            n_pairs += 1
            a = mp_sub(tlk, t_hi[m], prec)      # A = t_lo_k - t_hi_m
            b = mp_sub(g_hi[m], glk, prec)      # B = g_hi_m - g_lo_k
            if a.lo > 0:
                q = mp_div(b, a, prec)
                if q.hi < p_hi:
                    p_hi = q.hi
            elif a.hi < 0:
                q = mp_div(b, a, prec)
                if q.lo > p_lo:
                    p_lo = q.lo
            else:
                n_dropped += 1                  # straddles zero: no usable half-line
    return p_lo, p_hi, n_dropped, n_pairs


def arm_c_row(kappa, prec, n_cells=N_ARM_C):
    """Arm C: the SAME algorithm as arm B, in Decimal at working precision `prec`.

    Every input is an EXACT Decimal -- the t-grid, t_mid, kappa and P0 -- so the working
    precision is spent entirely on the arithmetic and nothing is lost in the inputs.  That
    is the whole point of the arm: if the threshold moves one decade per added digit, the
    mechanism is the arithmetic's rounding floor and nothing else."""
    prec = int(prec)
    kd = Decimal(str(kappa))
    p0d = Decimal(str(P0))
    step_fl = _floor_ctx(prec)
    step_ce = _ceil_ctx(prec)
    n = int(n_cells)
    # exact grid: t_i = T0 + i*W/n, formed with directed rounding so the cell edges are
    # themselves enclosures (they are exact for these operands, but the rounding is not
    # assumed away).
    t_lo, t_hi, g_lo, g_hi = [], [], [], []
    for i in range(n):
        a = MPInterval(step_fl.add(T0_EXACT, step_fl.divide(step_fl.multiply(W_EXACT, i), n)),
                       step_ce.add(T0_EXACT, step_ce.divide(step_ce.multiply(W_EXACT, i), n)))
        b = MPInterval(step_fl.add(T0_EXACT, step_fl.divide(step_fl.multiply(W_EXACT, i + 1), n)),
                       step_ce.add(T0_EXACT, step_ce.divide(step_ce.multiply(W_EXACT, i + 1), n)))

        def g_of(x):
            u = mp_sub(x, MPInterval.point(TMID_EXACT), prec)
            return mp_add(mp_mul(MPInterval.point(-p0d), x, prec),
                          mp_mul(MPInterval.point(kd), mp_mul(u, u, prec), prec), prec)

        ga, gb = g_of(a), g_of(b)
        t_lo.append(MPInterval.point(a.lo))
        t_hi.append(MPInterval.point(b.hi))
        g_hi.append(MPInterval.point(ga.hi))   # g decreasing: max at left edge
        g_lo.append(MPInterval.point(gb.lo))   # min at right edge
    p_lo, p_hi, n_drop, n_pairs = _mp_fm(t_lo, t_hi, g_lo, g_hi, prec)
    verdict = _classify(float(p_lo), float(p_hi))
    return {
        "arm": "C", "kappa": float(kappa), "prec": prec, "n_cells": n,
        "delta": 0.0, "verdict": verdict, "p_lo": float(p_lo), "p_hi": float(p_hi),
        "width": float(p_hi - p_lo), "width_decimal_str": str(p_hi - p_lo),
        "n_dropped": int(n_drop), "n_pairs": int(n_pairs),
        "leverage_W": float(W_EXACT), "detected": verdict == VERDICT_EMPTY,
        **_hyp("EXACT-INTERVAL-EVALUATION/ARM-C-TSPACE-DECIMAL-P%d" % prec,
               "Arm C: identical algorithm to arm B with solver/interval_mp.py's "
               "Decimal directed-rounded arithmetic at %d working digits; every input "
               "(t-grid, t_mid, kappa, p0) is an EXACT Decimal." % prec),
    }


# ===========================================================================
# 3.  THE LADDER, THE BRACKET, AND THE STEP ASSERTION (leg 384's trap)
# ===========================================================================

def decade_ladder(lo_exp, hi_exp):
    """kappa = 10^e for integer e, so consecutive rungs are EXACTLY one decade."""
    return [10.0 ** e for e in range(hi_exp, lo_exp - 1, -1)]


def bracket_from_ladder(rows):
    """[kappa_fail, kappa_detect] with the step ASSERTED, never assumed.

    Leg 384 banked rows that stepped 2 decades while its control assumed 1, which turned a
    false MATCH into a genuine finding only once someone looked.  So: the separation is
    COMPUTED from the kappa values actually run, the endpoints must be ADJACENT rungs, and
    an INCAPACITY rung can never be an endpoint (pre-registration Section 7)."""
    ladder = [r for r in rows if r["kappa"] > 0]
    ladder.sort(key=lambda r: -r["kappa"])
    exps = [round(np.log10(r["kappa"])) for r in ladder]
    steps = {int(exps[i] - exps[i + 1]) for i in range(len(exps) - 1)}
    step_ok = steps == {1}
    detect = [r for r in ladder if r["verdict"] == VERDICT_EMPTY]
    fail = [r for r in ladder if r["verdict"] == VERDICT_INTERVAL]
    incap = [r for r in ladder if r["verdict"] == VERDICT_INCAPACITY]
    monotone = True
    seen_fail = False
    for r in ladder:                      # descending kappa
        if r["verdict"] == VERDICT_INTERVAL:
            seen_fail = True
        elif r["verdict"] == VERDICT_EMPTY and seen_fail:
            monotone = False              # detection returned BELOW a failure
    out = {
        "ladder_step_decades_measured": sorted(steps),
        "ladder_step_assertion_holds": bool(step_ok),
        "n_rungs": len(ladder),
        "n_detect": len(detect), "n_fail": len(fail), "n_incapacity": len(incap),
        "detection_monotone_in_kappa": bool(monotone),
        "incapacity_kappas": [r["kappa"] for r in incap],
    }
    if detect and fail:
        k_detect = min(r["kappa"] for r in detect)
        k_fail = max(r["kappa"] for r in fail)
        sep = float(np.log10(k_detect / k_fail))
        out.update({
            "bracket_found": True,
            "kappa_fail": k_detect / (10.0 ** sep) if False else k_fail,
            "kappa_detect": k_detect,
            "bracket_separation_decades": sep,
            "endpoints_are_adjacent_rungs": bool(abs(sep - 1.0) < 1e-9),
            "bracket_meets_one_decade_requirement": bool(sep >= 1.0 - 1e-9),
        })
    else:
        out.update({"bracket_found": False, "kappa_fail": None, "kappa_detect": None,
                    "bracket_separation_decades": None,
                    "endpoints_are_adjacent_rungs": False,
                    "bracket_meets_one_decade_requirement": False,
                    "why_no_bracket": ("every rung detected (no FAIL rung: the ladder "
                                       "bottomed out above the floor, exactly leg 382's "
                                       "situation)" if not fail else
                                       "no rung detected (the ladder started below the "
                                       "floor)")})
    return out


def bisect_threshold(verdict_fn, lo_exp, hi_exp, iters=40):
    """Locate kappa* in log10 by bisection.  REPORTED, NOT GATE-DECIDING (Part I Sec 5).

    Valid only where detection is monotone in kappa, which the decade ladder checks and
    reports either way."""
    a, b = float(lo_exp), float(hi_exp)          # a: fails, b: detects
    if verdict_fn(10.0 ** b) != VERDICT_EMPTY:
        return {"located": False, "reason": "top of bisection range does not detect"}
    if verdict_fn(10.0 ** a) == VERDICT_EMPTY:
        return {"located": False, "reason": "bottom of bisection range already detects"}
    for _ in range(int(iters)):
        m = 0.5 * (a + b)
        if verdict_fn(10.0 ** m) == VERDICT_EMPTY:
            b = m
        else:
            a = m
    return {"located": True, "log10_kappa_star_lo": a, "log10_kappa_star_hi": b,
            "kappa_star": 10.0 ** (0.5 * (a + b))}


# ===========================================================================
# 4.  MODEL PREDICTIONS (pre-registered, Part I Section 2)
# ===========================================================================

def model_kappa_star(h_eff, W):
    """kappa* = 8 * h_eff / W^2 -- the ONE closed form all four predictions come from."""
    return 8.0 * float(h_eff) / (float(W) ** 2)


def predicted_kappa_star_precision(u_arith, r0, r1, p0=P0):
    W = np.log(r1 / r0)
    g_max = p0 * np.log(r1)
    return model_kappa_star(u_arith * g_max, W)


# ===========================================================================
# 5.  CONTROLS
# ===========================================================================

def control_pair(label, run_fn):
    """ZC and ZC-RED through the IDENTICAL code path, in one place.

    NO GREEN WITHOUT A DEMONSTRATED RED PATH.  `run_fn(kappa)` is called twice and nothing
    else changes between the two calls: kappa = 0 must give INTERVAL containing p0, and
    kappa = KAPPA_RED must give EMPTY.  A ZC green is REPORTABLE ONLY where ZC-RED went
    red; if ZC-RED does not fire the leg STOPS and reports it verbatim."""
    zc = run_fn(0.0)
    red = run_fn(KAPPA_RED)
    zc_ok = (zc["verdict"] == VERDICT_INTERVAL
             and zc["p_lo"] <= P0 <= zc["p_hi"])
    red_ok = red["verdict"] == VERDICT_EMPTY
    return {
        "config": label,
        "zc_verdict": zc["verdict"], "zc_p_lo": zc["p_lo"], "zc_p_hi": zc["p_hi"],
        "zc_width": zc["width"],
        "zc_contains_p0": bool(zc["p_lo"] <= P0 <= zc["p_hi"]),
        "zc_empty_free": bool(zc["verdict"] != VERDICT_EMPTY),
        "zc_green": bool(zc_ok),
        "red_kappa": KAPPA_RED, "red_verdict": red["verdict"], "red_fired": bool(red_ok),
        "green_is_reportable": bool(zc_ok and red_ok),
        **_hyp("CONTROL-PAIR",
               "ZC (kappa=0, must be INTERVAL containing p0=2) and ZC-RED "
               "(kappa=1e-3, must be EMPTY) through the identical code path with "
               "nothing else changed. config=" + label),
    }


# ===========================================================================
# 6.  THE RUN
# ===========================================================================

def main():
    out = {
        "leg": 388, "route": "CRVB", "title":
            "The certified decay enclosure's curvature blind spot, bounded from BELOW",
        "preregistration": {
            "journal": "experiments/journal/leg_388.md Part I",
            "novelty_commit": "5cbe659", "prereg_commit": "f2084ae",
            "gate": ("is a two-sided bracket [fail, detect] measured with at least one "
                     "decade's separation ruled out or confirmed, with a planted "
                     "zero-curvature control staying EMPTY-free at every rung?"),
            "model": "kappa* = 8 * h_eff / W^2, h_eff = max(log(1+delta), h_round)",
        },
        "inherited": {
            "leg_382_ladder_bottom_rung": 1e-06,
            "leg_382_claim": ("smallest_kappa_certified_empty = 1e-06 is the BOTTOM RUNG "
                              "of leg 382's ladder, not a located threshold; its own "
                              "journal Section 15 says the threshold is 'only bounded "
                              "(<= 1e-6), not located'"),
            "leg_386_width_law": "width = 4*log(1+delta)/log(R1/R0) -- a WINDOW property",
            "leg_386_0p8686_is": "4/log(100), the value on [10,1000] ONLY; 1.7457 on [10,100]",
            "leg_385_commensurability": ("refusal of a node-aligned violation fired at "
                                         "N=1100/1500 and NOT at N=500/997/1001/1010/2000"),
        },
        "settings": {
            "window_primary": [R0_PRIMARY, R1_PRIMARY],
            "leverage_W_primary": float(np.log(R1_PRIMARY / R0_PRIMARY)),
            "W_squared_primary": float(np.log(R1_PRIMARY / R0_PRIMARY) ** 2),
            "n_cells_gate": N_GATE, "p0": P0, "C": C_AMP,
            "tspace_window_exact_decimal": [str(T0_EXACT), str(T1_EXACT)],
            "tspace_W_exact_decimal": str(W_EXACT),
            "tspace_window_relative_offset_from_leg382": float(
                abs(float(W_EXACT) - np.log(100.0)) / np.log(100.0)),
            "kappa_red_control": KAPPA_RED,
            "arm_c_n_cells": N_ARM_C, "precisions": list(PRECISIONS),
        },
    }

    # ---- controls FIRST: no green is reportable before its red path is shown ----
    print("[1/7] controls (ZC / ZC-RED) ...")
    controls = []
    for n in N_LIST_SMOOTH:
        controls.append(control_pair("armA/N=%d/W=[10,1000]/delta=0" % n,
                                     lambda k, n=n: arm_a_row(k, n_cells=n)))
    for (r0, r1) in ((10.0, 100.0), (10.0, 1000.0), (10.0, 1e6)):
        controls.append(control_pair("armA/N=200/W=[%g,%g]/delta=0" % (r0, r1),
                                     lambda k, r0=r0, r1=r1: arm_a_row(
                                         k, r0=r0, r1=r1, n_cells=200)))
    for d in (0.0, 1e-9, 1e-6, 1e-3):
        controls.append(control_pair("armA/N=200/W=[10,1000]/delta=%g" % d,
                                     lambda k, d=d: arm_a_row(k, n_cells=200, delta=d)))
    for s in JITTER_SEEDS:
        controls.append(control_pair("armA-jitter/N=200/seed=%d" % s,
                                     lambda k, s=s: arm_a_row_jittered(k, s)))
    controls.append(control_pair("armB/N=1000/W=exact/delta=0",
                                 lambda k: arm_b_row(k, n_cells=N_GATE)))
    for p in PRECISIONS:
        controls.append(control_pair("armC/N=%d/prec=%d" % (N_ARM_C, p),
                                     lambda k, p=p: arm_c_row(k, p)))
    n_green = sum(c["zc_green"] for c in controls)
    n_red = sum(c["red_fired"] for c in controls)
    out["controls"] = {
        "rows": controls, "n_configs": len(controls),
        "n_zc_green": n_green, "n_zc_empty_free": sum(c["zc_empty_free"] for c in controls),
        "n_red_fired": n_red,
        "all_zc_green": bool(n_green == len(controls)),
        "all_red_fired": bool(n_red == len(controls)),
        "every_green_has_a_demonstrated_red_path":
            bool(all(c["green_is_reportable"] for c in controls)),
        "stop_condition_triggered": bool(n_red != len(controls)),
    }
    print("      %d configs, ZC green %d, ZC-RED fired %d"
          % (len(controls), n_green, n_red))
    if n_red != len(controls):
        print("      *** ZC-RED DID NOT FIRE EVERYWHERE -- pre-registration Section 7 "
              "says STOP AND REPORT ***")

    # ---- the gate ladder: arm A, N=1000, [10,1000], delta=0 ----
    print("[2/7] arm A decade ladder (gate) ...")
    rows_a = [arm_a_row(k) for k in decade_ladder(-20, -6)]
    rows_a.append(arm_a_row(0.0))
    out["arm_A_gate_ladder"] = {
        "rows": rows_a, "bracket": bracket_from_ladder(rows_a),
        "note": ("THE GATE-DECIDING ARM: leg 382's landed instrument and generator, its "
                 "window and its cell count, extended below its bottom rung."),
    }
    print("      ", out["arm_A_gate_ladder"]["bracket"].get("kappa_fail"),
          out["arm_A_gate_ladder"]["bracket"].get("kappa_detect"))

    # ---- arm B: the bridge ----
    print("[3/7] arm B decade ladder ...")
    rows_b = [arm_b_row(k) for k in decade_ladder(-20, -6)] + [arm_b_row(0.0)]
    out["arm_B_ladder"] = {"rows": rows_b, "bracket": bracket_from_ladder(rows_b)}

    # ---- arm C: the precision lever ----
    print("[4/7] arm C decade ladders (Decimal) ...")
    arm_c = {}
    for p in PRECISIONS:
        rows = [arm_c_row(k, p) for k in decade_ladder(-(p + 12), -(max(1, p - 14)))]
        rows.append(arm_c_row(0.0, p))
        arm_c["prec_%d" % p] = {"rows": rows, "bracket": bracket_from_ladder(rows)}
        print("      prec=%d -> %s" % (p, arm_c["prec_%d" % p]["bracket"].get("kappa_detect")))
    out["arm_C_precision_ladders"] = arm_c

    # ---- bisections and the scaling laws ----
    print("[5/7] bisections (reported, NOT gate-deciding) ...")
    bis = {}
    bis["arm_A_primary"] = bisect_threshold(
        lambda k: arm_a_row(k)["verdict"], -20, -6)
    bis["arm_B_primary"] = bisect_threshold(
        lambda k: arm_b_row(k)["verdict"], -20, -6)
    for p in PRECISIONS:
        bis["arm_C_prec_%d" % p] = bisect_threshold(
            lambda k, p=p: arm_c_row(k, p)["verdict"], -(p + 12), -(max(1, p - 14)), iters=30)
    out["bisections"] = bis

    a_star = bis["arm_A_primary"].get("kappa_star")
    b_star = bis["arm_B_primary"].get("kappa_star")
    out["control_agreement_A_vs_B"] = {
        "kappa_star_A": a_star, "kappa_star_B": b_star,
        "ratio": (a_star / b_star) if (a_star and b_star) else None,
        "within_factor_10": bool(a_star and b_star and
                                 0.1 <= a_star / b_star <= 10.0),
        "requirement": ("pre-registered Section 3: arms A and B must agree within a "
                        "factor of 10 or arm C is reported as NOT comparable to leg 382's "
                        "ladder and the gate is answered on arm A alone"),
    }

    # ---- mechanism: N-dependence (conditioning vs commensurability) ----
    print("[6/7] mechanism probes ...")
    n_rows = []
    for n in sorted(set(N_LIST_SMOOTH) | set(N_LIST_COMMENSURABILITY)):
        r = bisect_threshold(lambda k, n=n: arm_a_row(k, n_cells=n)["verdict"], -20, -6)
        n_rows.append({"n_cells": n, **r,
                       **_hyp("MECHANISM-N-SWEEP",
                              "arm A, window [10,1000], delta=0, N=%d" % n)})
    ks = [r["kappa_star"] for r in n_rows if r.get("located")]
    jit_rows = []
    for s in JITTER_SEEDS:
        r = bisect_threshold(lambda k, s=s: arm_a_row_jittered(k, s)["verdict"], -20, -6)
        jit_rows.append({"seed": s, **r,
                         **_hyp("MECHANISM-JITTERED-GRID",
                                "arm A, jittered non-geometric grid, N=200, seed=%d" % s)})
    kj = [r["kappa_star"] for r in jit_rows if r.get("located")]
    out["mechanism"] = {
        "n_sweep": n_rows,
        "n_sweep_spread_decades": (float(np.log10(max(ks) / min(ks))) if ks else None),
        "jittered_grid": jit_rows,
        "jitter_spread_decades": (float(np.log10(max(kj) / min(kj))) if kj else None),
        "jitter_vs_geometric_ratio": (
            float(np.median(kj) / np.median(ks)) if (kj and ks) else None),
        "signatures_preregistered": {
            "PRECISION_FLOOR": "kappa* falls ~1 decade per added Decimal digit; N-independent",
            "CONDITIONING": "kappa* moves smoothly/monotonically with N",
            "COMMENSURABILITY": ("kappa* moves NON-monotonically with N, differs between "
                                 "neighbours 997/1000/1001/1010, and CHANGES on a "
                                 "jittered grid"),
        },
    }

    # ---- precision law, window law, tolerance law ----
    print("[7/7] scaling laws ...")
    prec_pts = []
    for p in PRECISIONS:
        r = bis["arm_C_prec_%d" % p]
        if r.get("located"):
            prec_pts.append((p, np.log10(r["kappa_star"])))
    if len(prec_pts) >= 2:
        xs = np.array([q[0] for q in prec_pts], dtype=float)
        ys = np.array([q[1] for q in prec_pts], dtype=float)
        slope = float(np.polyfit(xs, ys, 1)[0])
    else:
        slope = None
    out["law_precision"] = {
        "points_prec_vs_log10_kappa_star": [[int(q[0]), float(q[1])] for q in prec_pts],
        "measured_slope_per_digit": slope,
        "predicted_slope_per_digit": -1.0,
        "float64_kappa_star_measured": a_star,
        "float64_kappa_star_predicted": predicted_kappa_star_precision(
            2.0 ** -53, R0_PRIMARY, R1_PRIMARY),
        "prediction_P1_bracket": [1e-16, 1e-15],
    }

    win_rows = []
    for (r0, r1) in ((10.0, 100.0), (10.0, 1000.0), (10.0, 1e6)):
        r = bisect_threshold(
            lambda k, r0=r0, r1=r1: arm_a_row(k, r0=r0, r1=r1, n_cells=200)["verdict"],
            -20, -5)
        W = float(np.log(r1 / r0))
        win_rows.append({
            "r0": r0, "r1": r1, "W": W, "W_squared": W * W,
            "predicted_kappa_star": predicted_kappa_star_precision(2.0 ** -53, r0, r1),
            **r,
            **_hyp("LAW-WINDOW", "arm A, N=200, delta=0, window [%g,%g], W=%.6f"
                   % (r0, r1, W))})
    base = [w for w in win_rows if w["r1"] == 1000.0]
    b0 = base[0]["kappa_star"] if base and base[0].get("located") else None
    for w in win_rows:
        w["ratio_to_primary_measured"] = (w["kappa_star"] / b0
                                          if (b0 and w.get("located")) else None)
        w["ratio_to_primary_predicted"] = (w["predicted_kappa_star"]
                                           / predicted_kappa_star_precision(
                                               2.0 ** -53, 10.0, 1000.0))
    out["law_window"] = {
        "rows": win_rows,
        "prediction_P3": ("kappa* proportional to |g|_max/W^2 = 2 log R1 / (log R1/R0)^2; "
                          "ratios vs [10,1000]: [10,100] x2.67, [10,1e6] x0.32"),
        "note_leg_386": ("every threshold here NAMES ITS WINDOW; the span across these "
                         "three windows is under one decade, which is why this law is "
                         "measured by bisection and not by the decade ladder"),
    }

    tol_rows = []
    for d in (1e-12, 1e-9, 1e-6, 1e-3):
        r = bisect_threshold(
            lambda k, d=d: arm_a_row(k, n_cells=200, delta=d)["verdict"], -20, -1)
        W = float(np.log(R1_PRIMARY / R0_PRIMARY))
        tol_rows.append({
            "delta": d, "predicted_kappa_star": model_kappa_star(np.log1p(d), W),
            **r,
            **_hyp("LAW-TOLERANCE",
                   "arm A, N=200, window [10,1000] (W=%.6f, so the coefficient 8/W^2 = "
                   "%.6f belongs to THIS window and no other), delta=%g"
                   % (W, 8.0 / W ** 2, d))})
    for t in tol_rows:
        t["measured_over_predicted"] = (t["kappa_star"] / t["predicted_kappa_star"]
                                        if t.get("located") else None)
    out["law_tolerance"] = {
        "rows": tol_rows,
        "prediction_P4": "kappa*(delta) = 8 log(1+delta)/W^2 = 0.377435*delta on [10,1000]",
        "coefficient_8_over_W2_on_primary_window": float(
            8.0 / np.log(R1_PRIMARY / R0_PRIMARY) ** 2),
        "coefficient_8_over_W2_on_10_100": float(8.0 / np.log(100.0 / 10.0) ** 2),
        "why_this_is_the_consumer_number": (
            "leg 382 Section 12b established that delta = 0 is unusable on numerical "
            "data (the exact instrument answers EMPTY for ANY perturbed profile), so "
            "every real consumer runs at delta > 0, where the blind spot is set by the "
            "TOLERANCE and not by the precision -- and is many decades larger."),
    }

    out["ceiling"] = {
        "L1_to_L4_link_moved": False,
        "clay_obligations_sec6_item1": "OPEN", "clay_obligations_sec6_item2": "OPEN",
        "tier": 2, "clay_probability": "~0.05%",
        "statement": ("Measuring an instrument's blind spot moves no link of the L1->L4 "
                      "chain. No profile of route 4's object exists; every profile here "
                      "is a planted analytic known."),
    }

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=False)
    print("wrote", OUT)
    return out


if __name__ == "__main__":
    main()
