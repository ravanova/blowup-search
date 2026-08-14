"""PROG-R4, unit E -- THE H-HARD DIAGNOSTIC. Lane R, instrument task.

  ####################################################################
  ##  THIS FILE IS COMMITTED BEFORE THE FIRST ATTEMPT IS RUN.       ##
  ##  The three diagnostics, their verdict RULES, their planted     ##
  ##  controls and the seed-selection rule are all fixed here so    ##
  ##  that no reading can be chosen after an outcome is seen. The   ##
  ##  commit order is the evidence. Nothing below is adjusted after ##
  ##  a number exists; an erratum is recorded in the journal.       ##
  ####################################################################

THE GATE, in its final wording (STATE.md, WAVE 1 item 4, committed before
dispatch and not re-scoped here):

    On the 200 banked attempts, do all three named diagnostics return, each
    with a planted control demonstrated firing in BOTH directions:
      (1) the converged-|s| distribution against seed |s|;
      (2) whether the low-|s| solutions are attractors of the HOOKSTEP
          ITERATION or of the MINIMISATION;
      (3) whether the named Table IV rows are reachable AT ALL when seeded
          directly at their published (T, s)?
    yes -> report all three.
    no  -> name which diagnostic the banked data cannot support, and what it
           would take -- a cost, not a verdict (section 3d).

THE GATE IS ABOUT THE DIAGNOSTICS RETURNING, NOT ABOUT CONVERGENCE. A clean
non-convergence with working controls is a PASS of this gate.

THE PRIOR, STATED NOT REDISCOVERED. Leg 353 already attempted UPO37 (x2),
UPO35, UPO9 and UPO22 -- ALL FIVE FAILED, reason=line_search_failed, final
||R|| in [22.5, 29.5], basin radius never measured. This unit is not a re-walk
of that, and the two differences are named before the run rather than after:
  (a) REALIZATION/SUPPLY. Leg 353 ran on a T_total = 2000 DNS; the fields here
      come from unit U2's T = 1e5 DNS (MILESTONE M2), a 50x longer trajectory,
      so the near-recurrence supply at any published (T, s) is a different and
      much larger object.
  (b) GLOBALISATION. Leg 353 used newton_krylov_rpo -- plain Newton with a
      step-halving line search. This unit uses newton_hookstep_rpo, the genuine
      Viswanath trust-region hookstep U1 built as MILESTONE M1, which ROTATES
      the step inside the Krylov subspace rather than merely rescaling it.
      `line_search_failed` is not even a reachable exit reason here.
If this run reproduces leg 353's failure at the same budget, the journal says
so in those words.

WHAT A PUBLISHED ROW DOES AND DOES NOT DETERMINE -- branch E-iv, named in
advance. Lucas & Kerswell 2015 Table IV supplies (T, s, m) for each row. IT
DOES NOT SUPPLY A FIELD. Every attempt below therefore plants a FIELD drawn
from this repository's own DNS together with (T, s) PINNED at the published
values. That is a field-plus-pinned-(T,s) seed and this file never calls it
"seeding at the published orbit". What is planted, exactly:
  basis       : real vorticity w(x, y) on a uniform 24 x 24 collocation grid,
                the state variable of solver/kolmogorov2d_nkbasin.Kolmogorov2D
                (2/3-rule dealiased pseudospectral, Re = 60, forcing n = 4,
                dt = 0.01, Lie-Trotter split, globally FIRST order in time).
  field       : an exact re-integration (u2_m2_dns_recurrence.regenerate, bit
                for bit) of one snapshot of U2's T = 1e5 trajectory, selected
                by the rule in select_seeds() below.
  T           : the PUBLISHED period, exactly. Not the candidate's measured
                period, which is quantised to the 0.25 snapshot spacing.
  s           : +/- the PUBLISHED shift wrapped to (-pi, pi]. The SIGN IS
                MEASURED, not assumed -- both signs are evaluated in the
                extended residual and the smaller is taken, exactly as U3 and
                U5 do, because this module already cost the repository one real
                sign bug (leg 353's FFT cross-correlation peak).
  m           : 0. All eight named rows have m_published = 0, and the extended
                residual carries a continuous x-shift only.

THE ADMISSION WINDOW IS DELIBERATELY NOT APPLIED. U3 section 5 measured that
the recurrence score R is monotone in |s| (rank correlation 0.50) and that the
R < 0.25 window admits 44% of |s| < 0.15 candidates against 11% in the
published band. That window is the biased filter, and this unit is the one
entitled to ignore it: arm S below draws its fields from the FULL m = 0
library, window or no window, which neither U3 nor U5 ever did.

LEG 349'S BAN, CONFIRMED COMPLIANT. `GA compute on an unvalidated fitness` is
live and a LEARNED or EVOLVED seed-scoring fitness is banned territory. Every
score touched here is deterministic and pre-existing: the recurrence score R as
banked by U2, and the extended residual ||R|| as defined by the solver. Nothing
is fitted, learned, evolved or tuned to an outcome, and this unit proposes no
such thing.

Usage:
    .venv/bin/python experiments/programme_r4/e_hhard_diagnostic.py --stage 12
    .venv/bin/python experiments/programme_r4/e_hhard_diagnostic.py --stage 3
"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import os
import pickle
import sys
import time
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from solver.kolmogorov2d_nkbasin import (  # noqa: E402
    Kolmogorov2D, extended_residual, pack,
)
from experiments.programme_r4.u2_m2_dns_recurrence import (  # noqa: E402
    CKPT, DT, DT_SAVE, LIB, N_FORCING, N_GRID, RE, regenerate,
)
# The stall exit and the caps are U5's, imported rather than copied so the
# algorithm is IDENTICAL to the one the 200 banked attempts ran under. A copy
# would be a second realization masquerading as the same one.
from experiments.programme_r4.u5_stratified_attempts import (  # noqa: E402
    MAX_GMRES, MAX_NEWTON, GMRES_RTOL, STALL_HALVE, STALL_K, STALL_W,
    TOL, solve_with_stall_exit, wrap_abs,
)
from experiments.programme_r4 import u3_controls  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CURATED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_e_v1.json")
LEDGER = os.path.join(HERE, "e_hhard_ledger.json")
ORBITS = os.path.join(HERE, "e_hhard_converged_orbits.npz")
# Per-attempt checkpoint directory. Diagnostic (3)'s first launch was killed by
# the host after ~2 h of an unattended multi-hour run, losing 16 completed-or-
# in-flight attempts because results were only assembled at the end. The solve
# is deterministic and per-attempt independent, so each finished attempt is now
# written out the moment it returns and a relaunch skips it. THIS CHANGES NO
# ALGORITHM AND NO SEED: same fields, same (T, s), same caps, same stall rule.
PARTIAL = os.path.join(HERE, "e_hhard_partial")
U3_BANKED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
U5_BANKED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_m3_v1.json")
U5_LEDGER = os.path.join(HERE, "u5_m3_ledger.json")
U5_ORBITS = os.path.join(HERE, "u5_m3_converged_orbits.npz")

TWO_PI = 2.0 * np.pi

# The eight named Lucas & Kerswell Table IV rows, taken from THIS REPOSITORY's
# existing transcription (u3_g1_attempts.TABLE_IV, line ~120) and asserted
# against it at import time rather than re-transcribed from the paper.
TABLE_IV = [
    ("UPO37", 19.334, 0.375, 0), ("UPO35", 18.912, 5.576, 0),
    ("UPO34", 18.878, 0.418, 0), ("UPO32", 18.694, 0.434, 0),
    ("UPO22", 17.160, 0.361, 0), ("UPO20", 16.908, 0.553, 0),
    ("UPO17", 16.753, 0.482, 0), ("UPO9", 14.776, 0.295, 0),
]
T_ANCHOR_TOL = 1.0          # U3's anchor rule, unchanged
MATCH_T_TOL, MATCH_S_TOL = 0.05, 0.05   # the matching predicate of record
PUBLISHED_BAND = (0.295, 0.707)
LOW_S = 0.15                # "low |s|" as U5 section 6.4 uses the word
PERM_SEED = 380             # the programme's leg number; fixed, never tuned
N_PERM = 20000


def _assert_table_iv():
    from experiments.programme_r4.u3_g1_attempts import (
        TABLE_IV as _U3_TABLE, T_ANCHOR_TOL as _U3_TOL,
        MATCH_T_TOL as _U3_MT, MATCH_S_TOL as _U3_MS)
    assert TABLE_IV == _U3_TABLE, "Table IV disagrees with u3_g1_attempts"
    assert T_ANCHOR_TOL == _U3_TOL, "anchor tolerance disagrees with U3"
    assert (MATCH_T_TOL, MATCH_S_TOL) == (_U3_MT, _U3_MS), \
        "matching predicate disagrees with U3"


# ==========================================================================
# small statistics, from scratch (no scipy dependency is added for this)
# ==========================================================================

def _ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = 0.5 * (i + j) + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(x, y):
    n = len(x)
    if n < 3:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def spearman(x, y):
    return pearson(_ranks(list(x)), _ranks(list(y)))


def binom_two_sided(k, n, p=0.5):
    """Exact two-sided binomial test by the method of small probabilities."""
    if n == 0:
        return 1.0
    def pmf(i):
        return math.comb(n, i) * p ** i * (1 - p) ** (n - i)
    p0 = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n + 1)
                        if pmf(i) <= p0 * (1 + 1e-12)))


# ==========================================================================
# DIAGNOSTIC (1) -- the converged-|s| distribution against seed |s|
# ==========================================================================
# VERDICT RULE, fixed before the run. Over the CONVERGED attempts of the 200
# banked ones, with drift d_i = |s|_converged,i - |s|_seed,i:
#
#   PULL_TO_LOW_S  iff  median(d) < 0
#                  AND  fraction(|s|_converged < 0.15) >= 0.5
#                  AND  two-sided sign test on d has p < 0.05
#   NO_PULL        otherwise.
#
# Spearman rho between |s|_seed and |s|_converged is reported alongside as a
# magnitude; it does NOT enter the rule, because a rule with four clauses
# tuned after the fact is not a pre-registration.

def classify_pull(seed_abs, conv_abs):
    d = [c - s for s, c in zip(seed_abs, conv_abs)]
    n_neg = sum(1 for v in d if v < 0)
    n_pos = sum(1 for v in d if v > 0)
    p_sign = binom_two_sided(n_neg, n_neg + n_pos)
    med = float(np.median(d)) if d else float("nan")
    frac_low = (sum(1 for c in conv_abs if c < LOW_S) / len(conv_abs)
                if conv_abs else float("nan"))
    verdict = ("PULL_TO_LOW_S"
               if (med < 0 and frac_low >= 0.5 and p_sign < 0.05)
               else "NO_PULL")
    return dict(verdict=verdict, n=len(d), median_drift=med,
                mean_drift=float(np.mean(d)) if d else None,
                n_drift_negative=n_neg, n_drift_positive=n_pos,
                sign_test_p=p_sign, frac_converged_below_0p15=frac_low,
                spearman_seed_vs_converged=spearman(seed_abs, conv_abs),
                seed_abs_range=[min(seed_abs), max(seed_abs)] if seed_abs else None,
                conv_abs_range=[min(conv_abs), max(conv_abs)] if conv_abs else None)


def diagnostic_1_controls(seed_abs):
    """PLANTED CONTROLS, and they fire in BOTH directions through the SAME
    classifier. Positive: converged |s| planted at 0.10 regardless of the seed
    -- classify_pull MUST answer PULL_TO_LOW_S. Negative: converged |s| planted
    equal to the seed with an alternating jitter -- it MUST answer NO_PULL.
    Both use the REAL seed |s| values, so the only thing planted is the
    outcome."""
    pos_conv = [0.10 + 0.001 * (i % 3) for i in range(len(seed_abs))]
    neg_conv = [s + 0.001 * (1 if i % 2 else -1)
                for i, s in enumerate(seed_abs)]
    pos = classify_pull(seed_abs, pos_conv)
    neg = classify_pull(seed_abs, neg_conv)
    fired = (pos["verdict"] == "PULL_TO_LOW_S"
             and neg["verdict"] == "NO_PULL")
    return dict(positive=pos, negative=neg, fired_both_ways=bool(fired),
                planted_positive="converged |s| := 0.10 for every attempt",
                planted_negative="converged |s| := seed |s| +/- 0.001")


# ==========================================================================
# DIAGNOSTIC (2) -- hookstep ITERATION attractor or MINIMISATION attractor?
# ==========================================================================
# The hookstep's accepted step is chosen by ONE of two mechanisms per epoch,
# and the ledger records which:
#
#   UNCONSTRAINED epoch: the accepted trial has on_boundary = False (mu = 0),
#       i.e. the full GMRES/Newton step lay INSIDE the trust region and was
#       taken as-is. Motion here is the NEWTON ITERATION acting.
#   CONSTRAINED epoch:   the accepted trial has on_boundary = True (mu > 0),
#       i.e. the step was selected by MINIMISING the local model of ||R||^2
#       subject to a radius -- rotated, not merely rescaled. Motion here is
#       the MINIMISATION acting.
#
# STATISTIC: the per-epoch drift in |s|, split by class, pooled over attempts.
# VERDICT RULE, fixed before the run:
#
#   MINIMISATION_ATTRACTOR  iff mean per-epoch d|s| on CONSTRAINED epochs is
#       more negative than on UNCONSTRAINED epochs AND the within-attempt
#       label permutation test on that difference gives p < 0.05.
#   ITERATION_ATTRACTOR     iff the reverse holds with p < 0.05.
#   MIXED                   otherwise (this includes "both classes descend in
#       |s| and neither dominates", which is a real and reportable outcome).
#
# COVERAGE, stated because it limits the diagnostic: per-epoch (T, s) are
# carried in the ledger only from U5 onward. U3's banked ledger records
# residual_before / krylov_dim / n_radius_trials / trials but NOT T_before or
# s_before, so the |s| PATH is recoverable for U5's 100 attempts and NOT for
# U3's 100. Diagnostic (2) therefore returns on 100 of the 200 banked
# attempts, and the cost of the other 100 is priced in the journal.

def epoch_drifts(u5_ledger, u5_attempts):
    """Per-epoch (class, d|s|, d||R||) triples over U5's banked attempts."""
    by_attempt = {a["attempt"]: a for a in u5_attempts}
    rows = []
    per_attempt = []
    for rec in u5_ledger["attempts"]:
        att = by_attempt[rec["attempt"]]
        led = [e for e in rec["ledger"] if e.get("accepted")]
        if not led:
            continue
        # s after epoch k is s_before of epoch k+1; after the last accepted
        # epoch it is the solve's final s, which the curated record carries.
        s_seq = [e["s_before"] for e in led] + [att["s_converged"]]
        r_seq = [e["residual_before"] for e in led] + [att["final_residual"]]
        local = []
        for k, e in enumerate(led):
            acc = e["trials"][-1]
            cls = "constrained" if acc["on_boundary"] else "unconstrained"
            d_abs_s = wrap_abs(s_seq[k + 1]) - wrap_abs(s_seq[k])
            d_r = r_seq[k + 1] - r_seq[k]
            local.append((cls, d_abs_s, d_r))
        rows.extend(local)
        per_attempt.append(local)
    return rows, per_attempt


def classify_attractor(per_attempt, rng_seed=PERM_SEED, n_perm=N_PERM):
    flat = [t for a in per_attempt for t in a]
    con = [d for c, d, _ in flat if c == "constrained"]
    unc = [d for c, d, _ in flat if c == "unconstrained"]
    if not con or not unc:
        return dict(verdict="UNDETERMINED",
                    reason="one of the two epoch classes is empty",
                    n_constrained=len(con), n_unconstrained=len(unc))
    obs = float(np.mean(con) - np.mean(unc))
    # Permutation: shuffle the class labels WITHIN each attempt, so the test
    # cannot be carried by between-attempt differences in how far |s| moves.
    rng = np.random.default_rng(rng_seed)
    count = 0
    for _ in range(n_perm):
        cs, us = [], []
        for a in per_attempt:
            labels = [c for c, _, _ in a]
            vals = [d for _, d, _ in a]
            perm = rng.permutation(len(labels))
            for i, j in enumerate(perm):
                (cs if labels[i] == "constrained" else us).append(vals[j])
        if cs and us and abs(np.mean(cs) - np.mean(us)) >= abs(obs):
            count += 1
    p = (count + 1) / (n_perm + 1)
    if obs < 0 and p < 0.05:
        verdict = "MINIMISATION_ATTRACTOR"
    elif obs > 0 and p < 0.05:
        verdict = "ITERATION_ATTRACTOR"
    else:
        verdict = "MIXED"
    return dict(verdict=verdict, n_constrained=len(con),
                n_unconstrained=len(unc),
                mean_d_abs_s_constrained=float(np.mean(con)),
                mean_d_abs_s_unconstrained=float(np.mean(unc)),
                net_d_abs_s_constrained=float(np.sum(con)),
                net_d_abs_s_unconstrained=float(np.sum(unc)),
                observed_difference=obs, permutation_p=p, n_perm=n_perm)


def diagnostic_2_controls():
    """PLANTED CONTROLS, firing BOTH ways through the SAME classifier. Each
    control is a synthetic set of 20 attempts of 10 epochs, alternating epoch
    class, with the |s| drift placed on ONE class only."""
    def synth(which):
        out = []
        for _a in range(20):
            local = []
            for k in range(10):
                cls = "constrained" if k % 2 else "unconstrained"
                d = -0.02 if cls == which else 0.0
                local.append((cls, d, -0.1))
            out.append(local)
        return out
    pos = classify_attractor(synth("constrained"), n_perm=2000)
    neg = classify_attractor(synth("unconstrained"), n_perm=2000)
    fired = (pos["verdict"] == "MINIMISATION_ATTRACTOR"
             and neg["verdict"] == "ITERATION_ATTRACTOR")
    return dict(planted_minimisation=pos, planted_iteration=neg,
                fired_both_ways=bool(fired),
                planted="d|s| = -0.02 on one epoch class only, 0.0 on the other")


def score_vs_shift():
    """SUPPLEMENTARY to (2), and the reading the ban clause is about: the SEED
    SCORE's own bias. Rank correlation between the deterministic recurrence
    score R and |s| over the m = 0 library, re-derived from U2's banked
    library. Nothing here is learned, evolved or fitted -- it is a measurement
    of a score that already exists."""
    with open(LIB) as f:
        lib = json.load(f)
    m0 = [c for c in lib["candidates"] if c["m"] == 0]
    abs_s = [wrap_abs(c["s"]) for c in m0]
    R = [c["R"] for c in m0]
    bands = []
    for lo, hi in [(0.0, 0.15), (0.15, 0.295), (0.295, 0.707),
                   (0.707, np.pi)]:
        g = [c for c, a in zip(m0, abs_s) if lo <= a < hi]
        bands.append(dict(band=[lo, hi], n=len(g),
                          median_R=float(np.median([c["R"] for c in g]))
                          if g else None,
                          admitted_fraction=(sum(1 for c in g
                                                 if c["in_newton_window"])
                                             / len(g)) if g else None))
    return dict(n_m0=len(m0), spearman_absS_vs_R=spearman(abs_s, R),
                by_band=bands,
                note=("deterministic, pre-existing score; leg 349's ban on a "
                      "learned or evolved seed-scoring fitness is not "
                      "approached, and this unit proposes no learned score"))


# ==========================================================================
# DIAGNOSTIC (3) -- direct seeding at the published (T, s)
# ==========================================================================
# SEED SELECTION RULE, fixed before the run. For each of the eight named rows,
# from the FULL m = 0 candidate set of U2's banked library (2014 candidates,
# 1153 with m = 0) restricted by U3's own anchor rule |T_c - T_pub| <= 1.0:
#
#   ARM S ("shift-matched field"): among candidates whose measured |s| agrees
#       with the published |s| to within the MATCHING PREDICATE'S OWN
#       tolerance (0.05), take the LOWEST recurrence score R. If that subset
#       is empty, fall back to minimising | |s|_c - |s|_pub |.
#   ARM Q ("score-optimal field"): take the LOWEST R outright -- U3's own
#       ranking, i.e. the field U3 would have chosen for that row.
#
# NO FIELD IS REUSED: a snapshot already selected by an earlier (row, arm) is
# skipped, so all 16 attempts carry distinct fields. Rows are processed in the
# TABLE_IV order above, arm S before arm Q. The Newton admission window
# (R < 0.25) is NOT applied to either arm -- see the module docstring.
#
# EVERY attempt is then seeded at (field, T = T_published, s = +/- s_published),
# which is a FIELD-PLUS-PINNED-(T,s) seed and is never called anything else.

def select_seeds():
    with open(LIB) as f:
        lib = json.load(f)
    m0 = [c for c in lib["candidates"] if c["m"] == 0]
    used = set()
    jobs = []
    for name, Tp, sp, mp_ in TABLE_IV:
        aps = wrap_abs(sp)
        anch = [c for c in m0 if abs(c["T"] - Tp) <= T_ANCHOR_TOL]
        for arm in ("S", "Q"):
            pool = [c for c in anch if c["snapshot_earlier"] not in used]
            if not pool:
                continue
            if arm == "S":
                near = [c for c in pool
                        if abs(wrap_abs(c["s"]) - aps) <= MATCH_S_TOL]
                if near:
                    c = min(near, key=lambda c: c["R"])
                    rule = ("min R among |s|-matched (<= 0.05) anchored "
                            "m=0 candidates")
                else:
                    c = min(pool, key=lambda c: abs(wrap_abs(c["s"]) - aps))
                    rule = ("no |s|-matched candidate; min | |s|_c - |s|_pub | "
                            "over anchored m=0 candidates")
                n_near = len(near)
            else:
                c = min(pool, key=lambda c: c["R"])
                rule = "min R among anchored m=0 candidates (U3's own ranking)"
                n_near = None
            used.add(c["snapshot_earlier"])
            jobs.append(dict(
                row=name, arm=arm, T_published=Tp, s_published=sp,
                m_published=mp_, abs_s_published=aps,
                selection_rule=rule, n_shift_matched_available=n_near,
                n_anchored_m0=len(anch),
                R_seed=c["R"], T_candidate=c["T"],
                abs_s_candidate=wrap_abs(c["s"]),
                delta_abs_s_candidate_to_published=abs(wrap_abs(c["s"]) - aps),
                delta_T_candidate_to_published=abs(c["T"] - Tp),
                candidate_in_newton_window=bool(c["in_newton_window"]),
                snapshot_earlier=int(c["snapshot_earlier"])))
    return jobs


def seed_residual(w0, T, s, solver):
    ref_rhs = solver.rhs_physical(w0)
    ref_dwdx = np.fft.ifft2(1j * solver.KX
                            * (np.fft.fft2(w0) * solver.mask)).real
    return float(np.linalg.norm(
        extended_residual(pack(w0, T, s), solver, w0, ref_rhs, ref_dwdx)))


def match_named(T, s, success):
    """The matching predicate of record, U3's, applied UNCHANGED. Returns the
    matched row name or None. The |s|-only variant is computed separately and
    is labelled SECONDARY everywhere it appears -- it is not this predicate."""
    if not success:
        return None
    for name, Tp, sp, _ in TABLE_IV:
        ds = abs(((s - sp + np.pi) % TWO_PI) - np.pi)
        if abs(T - Tp) < MATCH_T_TOL and ds < MATCH_S_TOL:
            return name
    return None


def match_named_abs(T, s, success):
    """SECONDARY, sign-agnostic variant: matches on |s| instead of signed s.
    Reported because the sign convention of the published shift relative to
    this realization's is not established by anything in the repository. It
    does NOT replace match_named and no verdict rests on it alone."""
    if not success:
        return None
    a = wrap_abs(s)
    for name, Tp, sp, _ in TABLE_IV:
        if (abs(T - Tp) < MATCH_T_TOL
                and abs(a - wrap_abs(sp)) < MATCH_S_TOL):
            return name
    return None


def _partial_path(idx):
    return os.path.join(PARTIAL, f"attempt{idx:03d}.pkl")


def run_attempt(job):
    """Run one direct-seed attempt, or return the banked one if it already ran.

    The checkpoint is keyed on the attempt index AND on the seed it was built
    from, so a stale partial from a different seed selection can never be
    silently reused."""
    idx, w0, T0, s0, meta = job
    path = _partial_path(idx)
    if os.path.exists(path):
        with open(path, "rb") as f:
            rec = pickle.load(f)
        if (rec["row"] == meta["row"] and rec["arm"] == meta["arm"]
                and rec["snapshot_earlier"] == meta["snapshot_earlier"]
                and rec["T_seeded"] == T0 and rec["s_seeded"] == s0):
            print(f"  attempt {idx:2d} {meta['row']:6s} arm {meta['arm']}: "
                  f"reused from checkpoint", flush=True)
            return rec
        raise SystemExit(
            f"stale checkpoint at {path}: it was written for a different "
            "seed. Delete the e_hhard_partial directory and re-run.")
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    t0 = time.time()
    out = solve_with_stall_exit(w0, T0, s0, solver)
    wall = time.time() - t0
    ds = abs(((out["s"] - meta["s_published"] + np.pi) % TWO_PI) - np.pi)
    matched = match_named(out["T"], out["s"], out["success"])
    rec = dict(meta)
    rec.update(
        attempt=idx, reason=out["reason"], success=bool(out["success"]),
        final_residual=out["final_residual"], n_iters=out["n_iters"],
        residual_history=out["residual_history"],
        T_converged=out["T"], s_converged=out["s"],
        abs_s_converged=wrap_abs(out["s"]),
        delta_T_from_published=abs(out["T"] - meta["T_published"]),
        delta_s_from_published=float(ds),
        delta_abs_s_from_published=abs(wrap_abs(out["s"])
                                       - meta["abs_s_published"]),
        matched_row=matched,
        recovered_named_orbit=bool(matched == meta["row"]),
        recovered_any_named_orbit=bool(matched is not None),
        matched_row_abs_secondary=match_named_abs(out["T"], out["s"],
                                                  out["success"]),
        krylov_dims=[e["krylov_dim"] for e in out["ledger"]],
        radius_trials=[e["n_radius_trials"] for e in out["ledger"]],
        wall_seconds=wall)
    rec["_ledger"] = out["ledger"]
    rec["_w0"] = out["w0"]
    os.makedirs(PARTIAL, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(rec, f)
    os.replace(tmp, path)
    print(f"  attempt {idx:2d} {meta['row']:6s} arm {meta['arm']}: "
          f"{out['reason']}, final ||R|| = {out['final_residual']:.4g}, "
          f"{out['n_iters']} epochs, {wall / 3600:.2f} h", flush=True)
    return rec


def stall_rule_replay():
    """The stall exit is U5's, and it is re-validated HERE against BOTH banked
    ledgers before it is used again: the rule must kill ZERO attempt that
    either unit's record shows converged."""
    out = {}
    for tag, path in (("U3", U3_BANKED), ("U5", U5_BANKED)):
        with open(path) as f:
            atts = json.load(f)["attempts"]
        worst = 0.0
        n_conv = 0
        killed = 0
        for a in atts:
            if not a["success"]:
                continue
            n_conv += 1
            h = a["residual_history"]
            for k in range(STALL_K, len(h)):
                if k - STALL_W < 0 or h[k - STALL_W] <= 0:
                    continue
                ratio = h[k] / h[k - STALL_W]
                worst = max(worst, ratio)
                if ratio > STALL_HALVE:
                    killed += 1
                    break
        out[tag] = dict(n_converged=n_conv, n_would_be_killed=killed,
                        worst_10_epoch_ratio_at_k_ge_20=worst,
                        threshold=STALL_HALVE,
                        margin_factor=(STALL_HALVE / worst) if worst > 0 else None)
    return out


def stage_3(args):
    _assert_table_iv()
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    metas = select_seeds()
    ckpt_path = args.ckpt or CKPT
    if not os.path.exists(ckpt_path):
        raise SystemExit(
            f"DNS checkpoint archive not found at {ckpt_path}. It is a "
            "gitignored REGENERABLE intermediate of unit U2; pass --ckpt "
            "pointing at the checkout that holds it.")
    ckpt = np.load(ckpt_path, mmap_mode="r")
    steps_per_snap = int(round(DT_SAVE / DT))
    fields = regenerate([m["snapshot_earlier"] for m in metas], solver, ckpt,
                        steps_per_snap)

    jobs = []
    sign_tally = {"plus": 0, "minus": 0}
    for i, m in enumerate(metas):
        w0 = fields[m["snapshot_earlier"]]
        aps = m["abs_s_published"]
        r_plus = seed_residual(w0, m["T_published"], aps, solver)
        r_minus = seed_residual(w0, m["T_published"], -aps, solver)
        s0 = aps if r_plus <= r_minus else -aps
        sign_tally["plus" if r_plus <= r_minus else "minus"] += 1
        m = dict(m, s_seeded=s0, seed_residual_plus=r_plus,
                 seed_residual_minus=r_minus,
                 seed_extended_residual=min(r_plus, r_minus),
                 T_seeded=m["T_published"])
        metas[i] = m
        jobs.append((i, w0, m["T_published"], s0, m))

    print(f"{len(jobs)} direct-seed attempts queued; sign tally {sign_tally}")
    for m in metas:
        print(f"  {m['row']:6s} arm {m['arm']}  R={m['R_seed']:.4f} "
              f"|s|_c={m['abs_s_candidate']:.4f} vs |s|_p="
              f"{m['abs_s_published']:.4f}  ||R||_seed="
              f"{m['seed_extended_residual']:.3f}  win="
              f"{m['candidate_in_newton_window']}")

    t0 = time.time()
    with mp.Pool(args.workers) as p:
        # imap_unordered with chunksize 1: every finished attempt is banked to
        # its own checkpoint the moment it returns, so a host kill costs at
        # most the attempts still in flight.
        results = sorted(p.imap_unordered(run_attempt, jobs, chunksize=1),
                         key=lambda r: r["attempt"])
    wall = time.time() - t0

    ledgers = [{"attempt": r["attempt"], "row": r["row"], "arm": r["arm"],
                "ledger": r.pop("_ledger")} for r in results]
    states = {}
    for r in results:
        w = r.pop("_w0")
        if r["success"]:
            states[f"attempt{r['attempt']:03d}_{r['arm']}_{r['row']}"] = w
    if states:
        np.savez_compressed(ORBITS, **states)

    # ---- the planted controls on diagnostic (3) --------------------------
    # P and N are u3_controls', imported UNCHANGED. R perturbs one of U5's
    # BANKED converged orbits, which is the sharpest positive available here:
    # it exercises the T and s directions (P cannot) and it demonstrates that
    # this harness's OWN matching predicate can return a recovery.
    print("running the planted controls ...")
    t0c = time.time()
    ctrl_P = u3_controls.control_P(solver, TOL, MAX_NEWTON, MAX_GMRES,
                                   GMRES_RTOL)
    ctrl_N = u3_controls.control_N(
        solver, jobs[0][1], metas[0]["T_published"], metas[0]["s_published"],
        TOL, MAX_NEWTON, MAX_GMRES, GMRES_RTOL, MATCH_T_TOL, MATCH_S_TOL,
        TABLE_IV)
    z = np.load(U5_ORBITS)
    with open(U5_BANKED) as f:
        u5_atts = json.load(f)["attempts"]
    key = sorted(z.keys())[0]
    a_idx = int(key.split("_")[0].replace("attempt", ""))
    a_rec = next(a for a in u5_atts if a["attempt"] == a_idx)
    ctrl_R = u3_controls.control_R(
        solver, z[key], a_rec["T_converged"], a_rec["s_converged"],
        f"U5 {key}", TOL, MAX_NEWTON, MAX_GMRES, GMRES_RTOL)
    # The harness's OWN predicate, exercised on the control-R solve: seeded at
    # a genuine solution of this discrete map, match_named-shaped matching
    # against that solution MUST return it. This is the "can this harness say
    # YES" demonstration, on the harness rather than on the solver.
    ds_R = abs(((ctrl_R["delta_s"] + np.pi) % TWO_PI) - np.pi)
    ctrl_R["harness_predicate_says_recovered"] = bool(
        ctrl_R["converged_to_tol"] and ctrl_R["delta_T"] < MATCH_T_TOL
        and ds_R < MATCH_S_TOL)
    ctrl_wall = time.time() - t0c
    fired, reasons = u3_controls.verdict(ctrl_P, ctrl_N, ctrl_R)
    fired = bool(fired and ctrl_R["harness_predicate_says_recovered"])

    recovered = [r for r in results if r["recovered_named_orbit"]]
    any_named = [r for r in results if r["recovered_any_named_orbit"]]
    converged = [r for r in results if r["success"]]
    payload = dict(
        n_attempts=len(results),
        n_converged=len(converged),
        n_recovered_its_own_row=len(recovered),
        n_recovered_any_named_row=len(any_named),
        n_recovered_abs_secondary=sum(
            1 for r in results if r["matched_row_abs_secondary"]),
        sign_tally=sign_tally,
        reasons=dict(Counter(r["reason"] for r in results)),
        closest_approach=min(
            ({k: r[k] for k in ("row", "arm", "attempt",
                                "delta_T_from_published",
                                "delta_s_from_published",
                                "delta_abs_s_from_published",
                                "final_residual", "success")}
             for r in results),
            key=lambda d: (d["delta_T_from_published"]
                           + d["delta_abs_s_from_published"])),
        controls=dict(P=ctrl_P, N=ctrl_N, R=ctrl_R,
                      fired_as_planted=bool(fired), failures=reasons,
                      wall_seconds=ctrl_wall),
        resourcing=dict(wall_seconds=wall, workers=args.workers,
                        core_hours=wall * args.workers / 3600.0,
                        control_wall_seconds=ctrl_wall,
                        tol=TOL, max_newton=MAX_NEWTON, max_gmres=MAX_GMRES,
                        gmres_rtol=GMRES_RTOL,
                        stall_rule=dict(k=STALL_K, w=STALL_W,
                                        halve=STALL_HALVE),
                        stall_rule_replay=stall_rule_replay(),
                        total_epochs=sum(r["n_iters"] for r in results)),
        attempts=results)
    merge_into_curated({"diagnostic_3": payload})
    with open(LEDGER, "w") as f:
        json.dump(dict(unit="E", programme="PROG-R4",
                       note="per-Newton-iteration ledger for the 16 "
                            "direct-seed attempts",
                       attempts=ledgers), f)
    print(f"\ndiagnostic (3): {len(converged)}/{len(results)} converged, "
          f"{len(recovered)} recovered their own named row, "
          f"{len(any_named)} recovered any named row; "
          f"controls fired as planted: {fired}")
    print(f"wall {wall/3600:.3f} h on {args.workers} workers "
          f"({wall*args.workers/3600:.2f} core-hours), controls "
          f"{ctrl_wall/3600:.3f} h")


# ==========================================================================
# banked-data stage: diagnostics (1) and (2)
# ==========================================================================

def load_banked():
    rows = []
    for tag, path in (("U3", U3_BANKED), ("U5", U5_BANKED)):
        with open(path) as f:
            for a in json.load(f)["attempts"]:
                rows.append(dict(
                    unit=tag, attempt=a["attempt"], anchor=a["anchor"],
                    abs_s_seed=wrap_abs(a["s_seed"]),
                    abs_s_final=wrap_abs(a["s_converged"]),
                    T_final=a["T_converged"], success=bool(a["success"]),
                    R_seed=a["R_seed"],
                    abs_s_published=wrap_abs(a["s_published"])))
    return rows


def stage_12(args):
    _assert_table_iv()
    rows = load_banked()
    conv = [r for r in rows if r["success"]]
    d1 = classify_pull([r["abs_s_seed"] for r in conv],
                       [r["abs_s_final"] for r in conv])
    d1_all = classify_pull([r["abs_s_seed"] for r in rows],
                           [r["abs_s_final"] for r in rows])
    d1_ctrl = diagnostic_1_controls([r["abs_s_seed"] for r in conv])
    in_band = [r for r in conv
               if PUBLISHED_BAND[0] <= r["abs_s_seed"] <= PUBLISHED_BAND[1]]
    d1.update(
        n_attempts_total=len(rows),
        by_unit={t: sum(1 for r in conv if r["unit"] == t)
                 for t in ("U3", "U5")},
        in_band_seeds_converged=len(in_band),
        in_band_seeds_that_left_the_band=sum(
            1 for r in in_band
            if not (PUBLISHED_BAND[0] <= r["abs_s_final"] <= PUBLISHED_BAND[1])),
        secondary_all_200_attempts=d1_all,
        controls=d1_ctrl)

    with open(U5_LEDGER) as f:
        u5_led = json.load(f)
    with open(U5_BANKED) as f:
        u5_atts = json.load(f)["attempts"]
    flat, per_attempt = epoch_drifts(u5_led, u5_atts)
    d2 = classify_attractor(per_attempt)
    d2_ctrl = diagnostic_2_controls()
    d_r = [t for t in flat]
    d2.update(
        coverage=dict(
            n_attempts_with_epoch_path=len(per_attempt),
            n_banked_attempts=200,
            missing=("U3's banked ledger records no T_before / s_before, so "
                     "the per-epoch |s| path exists for U5's 100 attempts "
                     "only. The fields were added to the solver's hookstep "
                     "ledger after U3 ran."),
            cost_to_close=("re-running U3's 100 attempts under the current "
                           "ledger: 4,629 epochs at the measured 95 s/epoch "
                           "= 122.1 core-hours, 15.3 h wall at 8 workers. "
                           "Not bought here and not needed for this gate.")),
        correlation_dR_vs_dabs_s=pearson([t[1] for t in d_r],
                                         [t[2] for t in d_r]),
        n_epochs=len(flat),
        score_bias=score_vs_shift(),
        controls=d2_ctrl)
    merge_into_curated({"diagnostic_1": d1, "diagnostic_2": d2})
    print("diagnostic (1):", d1["verdict"], "| controls fired both ways:",
          d1_ctrl["fired_both_ways"])
    print("diagnostic (2):", d2["verdict"], "| controls fired both ways:",
          d2_ctrl["fired_both_ways"])


def merge_into_curated(new):
    base = {}
    if os.path.exists(CURATED):
        with open(CURATED) as f:
            base = json.load(f)
    base.setdefault("unit", "E")
    base.setdefault("kind", "INSTRUMENT / DIAGNOSTIC -- answers a gate about "
                            "whether three diagnostics RETURN, not about "
                            "convergence")
    base.setdefault("programme", "PROG-R4 (leg 380), Lane R, wave 1 item 4")
    base.setdefault("gate", dict(
        wording=("On the 200 banked attempts, do all three named diagnostics "
                 "return, each with a planted control demonstrated firing in "
                 "BOTH directions: (1) the converged-|s| distribution against "
                 "seed |s|; (2) whether the low-|s| solutions are attractors "
                 "of the HOOKSTEP ITERATION or of the MINIMISATION; and (3) "
                 "whether the named Table IV rows are reachable AT ALL when "
                 "seeded directly at their published (T, s)?"),
        note="the gate is about the diagnostics RETURNING, not about "
             "convergence; a clean non-convergence with working controls "
             "is a PASS"))
    base.setdefault("prior_leg_353", dict(
        attempts="UPO37 x2, UPO35, UPO9, UPO22 -- ALL FIVE FAILED",
        reason="line_search_failed", final_residual_range=[22.5, 29.5],
        basin_radius="never measured",
        why_this_is_a_new_measurement=[
            "leg 353 ran on a T_total = 2000 DNS; the fields here come from "
            "U2's T = 1e5 DNS (MILESTONE M2), 50x longer",
            "leg 353 used plain-Newton line search (newton_krylov_rpo); this "
            "unit uses the genuine Viswanath trust-region hookstep U1 built "
            "as MILESTONE M1 (newton_hookstep_rpo)"]))
    base.setdefault("seed", dict(
        source="Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV",
        rows=[n for n, _, _, _ in TABLE_IV],
        transcription="taken from experiments/programme_r4/u3_g1_attempts.py "
                      "and asserted equal to it at import; NOT re-transcribed "
                      "from the paper",
        what_a_published_row_determines="(T, s, m) ONLY -- NOT a field",
        what_was_planted=("a 24x24 real vorticity field from U2's T = 1e5 DNS "
                          "(exact bit-for-bit regeneration) together with "
                          "T and s PINNED at the published values; this is a "
                          "field-plus-pinned-(T,s) seed and is never "
                          "described as seeding at the published orbit"),
        ban1="PASS -- no step continues a fixed point into an orbit",
        ban2="PASS -- every attempt is anchored to a named row by construction",
        ban_leg349=("COMPLIANT -- every score used is deterministic and "
                    "pre-existing (U2's recurrence score R, the solver's "
                    "extended residual). Nothing learned or evolved is used "
                    "or proposed.")))
    base.setdefault("realization", dict(
        grid="N = 24", Re=60.0, n_forcing=4, dt=0.01,
        stepper="Lie-Trotter split, globally FIRST order (U3's lesson-91 "
                "disclosure, measured global ratio 2.00)",
        globalisation="Newton-GMRES-hookstep (MILESTONE M1)",
        residual="extended residual with a CONTINUOUS x-shift only; m is not "
                 "carried, so the m != 0 class cannot be expressed",
        dns="T = 1e5 (MILESTONE M2)"))
    base.setdefault("open_obligations_carried", dict(
        clay_obligations_6i="OPEN, no known method",
        clay_obligations_6ii="OPEN, no known method",
        clay_obligations_4="OPEN and NOT discharged"))
    base.setdefault("clay_movement", dict(
        links_moved=0, ceiling="TIER 2", clay_odds="~0.05%, unmoved",
        note="a best-in-field orbit finder makes the questions affordable; it "
             "does not move an L1 -> L4 link, and nothing in this unit does"))
    base.update(new)
    with open(CURATED, "w") as f:
        json.dump(base, f, indent=1)
    print(f"wrote {CURATED}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["12", "3"], required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--ckpt", default=None,
                    help="path to U2's gitignored DNS checkpoint archive")
    ap.add_argument("--partial-dir", default=None,
                    help="per-attempt checkpoint directory; a relaunch reuses "
                         "any attempt already banked there. Deterministic, so "
                         "reuse is identical to re-running")
    args = ap.parse_args()
    if args.partial_dir:
        globals()["PARTIAL"] = os.path.abspath(args.partial_dir)
    if args.stage == "12":
        stage_12(args)
    else:
        stage_3(args)


if __name__ == "__main__":
    main()
