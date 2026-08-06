"""Route-PNA v1 -- the adversarial battery against solver/profile_newton.py (leg 202).

THE GATE (pre-committed, verbatim)
----------------------------------
Under adversarial and degenerate inputs (near-singular Jacobian, poor initial guess,
boundary-of-convergence parameters), does `solver/profile_newton.py` ever silently report a
converged solution that is not (a false-positive convergence claim), or silently return a
wrong value rather than reject/flag?

  yes -> Name the exact mechanism and magnitude, list every calling construction leg whose
         banked convergence claim could be affected, escalate as a priority finding, push
         the branch only, do NOT patch.
  no  -> Bank the battery as the permanent regression suite and record the pass in
         capabilities.py.

ANSWER: **YES**.  See `experiments/journal/leg_202.md`.  The headline is *not* the
convergence flag -- it is that `relres` and `converged` are both **perfect** (4.2e-16, True)
on profiles that have left the decay class by six orders of magnitude.

READ-ONLY.  `solver/profile_newton.py` is byte-identical to this leg's merge base under BOTH
branches of the gate and is not edited here.  Every probe below is a measurement; the ones
that FAIL are pinned in `test_profile_newton_adversarial.py`, not patched.

THE PROBES ARE FROZEN.  `writeup/novelty/leg_202.md` §3 names six groups G1..G6 and three
controls C1..C3 and was committed (`5a9f83a`) BEFORE this file existed.  Nothing outside that
list is reported as this leg's finding, and the groups that came back CLEAN (G2, G4, and the
leg-114-M2 half of G3) are reported at the same weight as the one that fired.

WHAT "WRONG" MEANS HERE, AND WHERE THE REFERENT COMES FROM -- decided before running
------------------------------------------------------------------------------------
Not this leg's invention.  `solver/profile_newton.py`'s own docstring states the object it
solves for: a *traveling wave* deforming the exact `a = 0` anchor `Omega = -1/(1+X^2)`
("the a != 0 profile (if it exists) is a deformation of the exact a = 0 anchor, so the honest
test is to FOLLOW it", `continuation`'s docstring).  That anchor DECAYS: on the module's own
default sinh grid (`rho_max = 8`, so `X_max = 0.5 sinh 8 = 745.24`) its far-field supremum
over the outer half of the grid is 6.48e-06 against an origin amplitude pinned by the module's
own gauge at exactly 1.  A returned `Omega` whose far field is O(1) -- or, as measured below,
LARGER than its origin value -- is not a deformation of that anchor whatever its residual is.

So the decay-class diagnostics below are the module's own stated object, made numerical.  They
are also not novel as a *kind*: `experiments/p2_route_d_v11_anchor.py` already computes a
`weighted_defect` externally, and this leg's finding is precisely that the diagnostic lives in
the EXPERIMENT and never in the MODULE, so the two consumers that do not compute one have no
way to tell the branches apart.

Deterministic apart from one seeded RNG start (G3, `default_rng(202)`).  Plain float64.
Nothing here is interval-enclosed and nothing is rigorous.  Runtime ~4 min single-threaded.

Run: .venv/bin/python experiments/p2_route_pna_v1_adversarial.py
"""

import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.profile_newton import TwoScaleNewton, continuation  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_pna_v1_adversarial.json")

# The ladder and grids.  n = 101/201/301 is deliberate: the defect is GRID DEPENDENT and a
# single n would report it as a property of `a`, which it is not.
LADDER = [0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.35, 1.50]
GRIDS = [101, 201, 301]

# Verdict taxonomy -- leg 114's, deliberately, so the audits of the two sibling Newton
# modules are comparable side by side.
SILENT_WRONG = "SILENT_WRONG"        # converged + clean relres + materially wrong answer
SILENT_DEGRADED = "SILENT_DEGRADED"  # converged=True on a stall that did not meet tol
NONFINITE = "NONFINITE"              # NaN/Inf reached the caller
RAISED = "RAISED"                    # rejected loudly -- the CORRECT behaviour for bad input
CLEAN = "CLEAN"                      # behaved


# ---------------------------------------------------------------------------
# diagnostics -- every probe reports WHAT CAME BACK, never a bare boolean
# ---------------------------------------------------------------------------
def diagnostics(nw, r):
    """Decay-class and smoothness diagnostics the MODULE never computes."""
    O = np.asarray(r["Omega"], float)
    X = nw.fam.X
    outer = np.abs(X) > 0.5 * np.max(np.abs(X))
    anchor = nw.anchor()
    a_ff = float(np.max(np.abs(anchor[outer])))
    ff = float(np.max(np.abs(O[outer]))) if np.all(np.isfinite(O)) else float("inf")
    sup = float(np.max(np.abs(O))) if np.all(np.isfinite(O)) else float("inf")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        osc = float(np.max(np.abs(np.diff(O))) / sup) if sup > 0 else float("nan")
        mass = float(np.trapezoid(O, X))
    return {
        "farfield_sup": ff,
        "anchor_farfield_sup": a_ff,
        "farfield_inflation": ff / a_ff if a_ff > 0 else float("inf"),
        "sup_abs_Omega": sup,
        "farfield_is_the_max": bool(np.isfinite(ff) and np.isfinite(sup)
                                    and ff >= 0.99 * sup),
        "node_oscillation": osc,
        "mass": mass,
        "gauge1_residual": float(O[nw.i0] + 1.0) if np.isfinite(O[nw.i0]) else float("nan"),
        "gauge2_residual": float(O[nw.i1] + 0.5) if np.isfinite(O[nw.i1]) else float("nan"),
    }


def verdict(r, d):
    """Pre-committed classifier.  Thresholds fixed before the numbers were read.

    Three independent ways to be SILENT_WRONG, all requiring `converged is True`:
      (i)   the returned profile has left the decay class (far field >100x the anchor's)
            while the residual is at machine zero;
      (ii)  the returned profile does not satisfy the gauges the module solved for, so it
            is not the solution that was asked for -- the scaling-family escape;
      (iii) the returned `c` is not finite.
    100x in (i) is 1.3 decades below the smallest inflation actually observed in a firing
    case (2.08e+03) and 1e-6 in (ii) is 5 decades below the smallest violation observed
    (0.25), so neither verdict is threshold-sensitive.
    """
    if not np.isfinite(d["sup_abs_Omega"]) or not np.isfinite(r.get("relres", np.nan)):
        return NONFINITE
    if not r["converged"]:
        return CLEAN
    gauge_broken = (abs(d["gauge1_residual"]) > 1e-6 or abs(d["gauge2_residual"]) > 1e-6)
    if r["relres"] < 1e-10 and d["farfield_inflation"] > 1e2:
        return SILENT_WRONG
    if gauge_broken or not np.isfinite(r["c"]):
        return SILENT_WRONG
    if r["iterations"] >= 40 and r["relres"] > 1e-10:
        return SILENT_DEGRADED
    return CLEAN


def row(nw, r, **extra):
    d = diagnostics(nw, r)
    out = {"converged": bool(r["converged"]),
           "iterations": int(r["iterations"]),
           "hit_iteration_cap": bool(r["iterations"] >= 40),
           "residual_rms": float(r["residual_rms"]),
           "relres": float(r["relres"]),
           "c": float(r["c"])}
    out.update(d)
    out["verdict"] = verdict(r, d)
    out.update(extra)
    return out


# ---------------------------------------------------------------------------
# G1 -- flag semantics under DEFAULT parameters
# ---------------------------------------------------------------------------
def g1_flag_on_stalls():
    """Cold `solve()`, nothing touched.  Is `converged` ever True on a capped stall?"""
    rows = []
    for n in GRIDS:
        for a in [0.30, 0.60, 0.90, 1.20, 1.50]:
            nw = TwoScaleNewton(a=a, n=n)
            rows.append(row(nw, nw.solve(), n=n, a=a))
    caps = [r for r in rows if r["verdict"] == SILENT_DEGRADED]
    return {"rows": rows,
            "n_silent_degraded": len(caps),
            "worst_relres_reported_converged": max([r["relres"] for r in caps],
                                                   default=0.0),
            "reading": "PRIOR ART, not this leg's discovery: test_profile_newton.py item (6) "
                       "already writes out the algebra (converged collapses to the ABSOLUTE "
                       "test residual_rms < 1e-6 because max(1.0, hist[0]) pins the "
                       "denominator at 1) and leg 71 already banked an instance. What is "
                       "added here is that it fires under DEFAULT parameters at several (a, "
                       "n), not only at the single a = 0.9 ladder row those two discuss."}


# ---------------------------------------------------------------------------
# G2 -- gauge blindness (predicted by reading the source; MEASURED CLEAN)
# ---------------------------------------------------------------------------
def g2_gauge_blindness():
    """`converged` never consults the two gauge rows.  Is that reachable?

    Two sub-probes.  The lam-scaled one was the hypothesis the source reading suggested; the
    small-amplitude one is what actually reaches the defect at the DEFAULT budget, and it is
    the gate's own "poor initial guess" clause word for word.
    """
    C_REF = 0.49797481  # the a = 0 gauged speed at n = 201, from the ladder's own a = 0 row
    n = 201
    nw = TwoScaleNewton(a=0.0, n=n)
    ex = nw.anchor()

    # -- sub-probe (a): lam-scaled exact anchors against a finite iteration budget --------
    scaled = []
    for lam in [1.0, 2.0, 10.0]:
        for mi in [0, 1, 2, 4, 40]:
            r = nw.solve(om0=ex * lam, c0=0.5 * lam, max_iter=mi)
            scaled.append(row(nw, r, lam=lam, max_iter=mi))

    # -- sub-probe (b): small-amplitude starts, DEFAULT parameters throughout -------------
    tiny = []
    for n_t in GRIDS:
        nwt = TwoScaleNewton(a=0.0, n=n_t)
        for eps in [1e-6, 1e-7, 1e-8, 1e-9, 1e-10]:
            r = nwt.solve(om0=eps * nwt.anchor(), c0=0.5)
            rr = row(nwt, r, n=n_t, eps=eps)
            rr["c_reference"] = C_REF
            rr["c_relative_error"] = abs(r["c"] - C_REF) / abs(C_REF)
            tiny.append(rr)

    fired = [r for r in tiny if r["verdict"] == SILENT_WRONG]
    full = [r for r in scaled if r["max_iter"] == 40]
    return {
        "lambda_scaled": scaled,
        "small_amplitude_starts": tiny,
        "worst_gauge_residual_lambda_at_full_budget": max(
            abs(r["gauge1_residual"]) for r in full),
        "n_silent_wrong_small_amplitude": len(fired),
        "worst_c_relative_error": max([r["c_relative_error"] for r in fired], default=0.0),
        "worst_gauge1_residual_small_amplitude": max(
            [abs(r["gauge1_residual"]) for r in fired], default=0.0),
        "reading": "REACHABLE AT DEFAULT PARAMETERS, and this CORRECTS an earlier reading in "
                   "this leg's own scouting notes. (a) The lam-scaled sub-probe shows the "
                   "structure but not the reach: at max_iter = 0 the flag is computed from "
                   "hist[0], the residual of the CALLER'S OWN INPUT, so a zero-iteration call "
                   "returns converged=True having done no work -- but at the default "
                   "max_iter = 40 every gauge residual returns to 0.0e+00 exactly, so the "
                   "lam route alone would have been a NEGATIVE. (b) The small-amplitude "
                   "sub-probe reaches it with NO parameter touched: from om0 = 1e-8 * anchor "
                   "the solve slides down the exact scaling degeneracy (Omega -> lam Omega "
                   "with c -> lam c), sacrifices the two gauge rows -- which are only 2 rows "
                   "against n in an overdetermined LEAST-SQUARES solve and are therefore "
                   "tradeable -- and returns Omega(0) = -0.750000 instead of the gauged -1 "
                   "together with a wave speed of order -1e+04 to -1e+06, with "
                   "converged=True. `converged` never consults the gauge rows and `relres` is "
                   "exactly scale-invariant, so neither returned field can see it. The c "
                   "values scale as 1/eps (-6.13e+03, -3.06e+04, -3.06e+05 at eps = 1e-8, "
                   "1e-9, 1e-10), which identifies the scaling family as the mechanism rather "
                   "than roundoff."}


# ---------------------------------------------------------------------------
# G3 -- spurious roots and the decay class.  THIS IS THE GROUP THAT FIRES.
# ---------------------------------------------------------------------------
def g3_spurious_roots():
    """Two halves: leg 114's M2 vectors (predicted CLEAN), and the continuation ladder."""
    n = 201
    nw = TwoScaleNewton(a=0.0, n=n)
    ex = nw.anchor()
    rng = np.random.default_rng(202)

    # -- half 1: the poor-initial-guess starts, including leg 114's M2 vector -----------
    starts = [("const_minus_one", -np.ones(n)),
              ("zeros", np.zeros(n)),
              ("1e-8_times_anchor", 1e-8 * ex),
              ("1e-6_times_anchor", 1e-6 * ex),
              ("sign_flipped_anchor", -ex),
              ("random", rng.normal(size=n))]
    guesses = []
    for name, om0 in starts:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = nw.solve(om0=om0, c0=0.5)
        guesses.append(row(nw, r, start=name))

    # -- half 2: the continuation ladder, with the decay diagnostics attached ----------
    ladders = []
    for n_l in GRIDS:
        om, c = None, 0.5
        for a in LADDER:
            nwl = TwoScaleNewton(a=float(a), n=n_l)
            r = nwl.solve(om0=om, c0=c)
            used = "warm"
            # This reproduces `continuation`'s own retry clause (lines 182-189) exactly, so
            # the vehicle can be attributed.  Verified against continuation() itself below.
            if r["relres"] > 1e-10:
                alt = nwl.solve(om0=None, c0=0.5)
                if alt["relres"] < r["relres"]:
                    r, used = alt, "RETRY_FROM_COLD_ANCHOR"
            ladders.append(row(nwl, r, n=n_l, a=float(a), start=used))
            if r["relres"] < 1e-10:
                om, c = r["Omega"], r["c"]

    fired = [r for r in ladders if r["verdict"] == SILENT_WRONG]
    first = min(fired, key=lambda r: (r["a"], r["n"])) if fired else None
    worst = max(fired, key=lambda r: r["farfield_inflation"]) if fired else None
    # the same physical quantity, three grids, all reported converged at machine zero
    at_15 = {r["n"]: r for r in ladders if r["a"] == 1.50}
    cs = [at_15[n]["c"] for n in GRIDS if n in at_15]
    return {
        "poor_initial_guesses": guesses,
        "leg_114_M2_reproduced": any(g["verdict"] == SILENT_WRONG for g in guesses),
        "ladder": ladders,
        "n_silent_wrong": len(fired),
        "first_departure": first,
        "worst_departure": worst,
        "c_at_a_1p50_by_grid": {str(n): at_15[n]["c"] for n in GRIDS if n in at_15},
        "c_at_a_1p50_spread_relative": (max(cs) - min(cs)) / max(cs) if cs else None,
        "reading": "leg 114 M2 predicted this module immune ('one gauge kills the scaling "
                   "symmetry; it does not kill the constant. Two gauges do'). Half 1 CONFIRMS "
                   "the prediction -- the constant start is not returned as converged. Half 2 "
                   "REFUTES its sufficiency: a DIFFERENT spurious root satisfies BOTH gauges "
                   "to 0.0e+00 exactly, drives every residual row to machine zero, and is "
                   "returned with converged=True.",
    }


# ---------------------------------------------------------------------------
# G4 -- poisoned input
# ---------------------------------------------------------------------------
def g4_poisoned():
    n = 101
    nw = TwoScaleNewton(a=0.0, n=n)
    ex = nw.anchor()
    cases = []

    def probe(name, fn):
        t = {"case": name}
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                r = fn()
            t["raised"] = None
            t["keys"] = sorted(r.keys())
            t["converged"] = bool(r["converged"])
            t["reason"] = r.get("reason")
            t["has_relres"] = "relres" in r
            t["c"] = float(r["c"]) if "c" in r else None
            if "relres" in r:
                d = diagnostics(nw, r)
                t.update({k: d[k] for k in ("gauge1_residual", "gauge2_residual",
                                            "farfield_inflation")})
                t["relres"] = float(r["relres"])
                t["verdict"] = verdict(r, d)
            else:
                # the LinAlgError path: an explicit, reasoned rejection -- correct behaviour
                t["verdict"] = CLEAN if not r["converged"] else NONFINITE
        except Exception as e:                                   # noqa: BLE001
            t["raised"] = "%s: %s" % (type(e).__name__, e)
            t["verdict"] = RAISED
        cases.append(t)

    bad_nan = ex.copy(); bad_nan[7] = np.nan
    bad_inf = ex.copy(); bad_inf[7] = np.inf
    probe("om0_has_nan", lambda: nw.solve(om0=bad_nan, c0=0.5, max_iter=5))
    probe("om0_has_inf", lambda: nw.solve(om0=bad_inf, c0=0.5, max_iter=5))
    probe("om0_all_nan", lambda: nw.solve(om0=np.full(n, np.nan), c0=0.5, max_iter=5))
    probe("c0_nan", lambda: nw.solve(om0=ex, c0=float("nan"), max_iter=5))
    probe("c0_inf", lambda: nw.solve(om0=ex, c0=float("inf"), max_iter=5))
    for c0 in (1e6, 1e9, 1e12, 1e15):
        probe("c0_%.0e" % c0, lambda c0=c0: nw.solve(om0=ex, c0=c0, max_iter=5))
    probe("om0_wrong_length", lambda: nw.solve(om0=np.zeros(n - 3), c0=0.5, max_iter=2))
    probe("a_nan", lambda: TwoScaleNewton(a=float("nan"), n=n).solve(max_iter=3))
    probe("a_inf", lambda: TwoScaleNewton(a=float("inf"), n=n).solve(max_iter=3))
    return {"cases": cases,
            "n_nonfinite_absorbed": sum(1 for c in cases if c["verdict"] == NONFINITE),
            "n_silent_wrong": sum(1 for c in cases if c["verdict"] == SILENT_WRONG),
            "reading": "SPLIT. The NaN/Inf half is CLEAN and is banked as such: every "
                       "non-finite input reaches np.linalg.lstsq, which raises LinAlgError, "
                       "which the module catches and turns into an explicit converged=False "
                       "with a `reason`. Nothing non-finite is absorbed into a converged "
                       "answer. (LAPACK prints 'On entry to DLASCL parameter number 4 had an "
                       "illegal value' to stderr on this path; it is noise from the caught "
                       "exception, not a second failure.) The FINITE-but-absurd half is NOT "
                       "clean: `c0` is never range-checked, and solve(om0=anchor, c0=1e9) "
                       "returns converged=True with c = 1.000000e+09 handed straight back -- "
                       "the caller's own garbage input returned as a converged wave speed, "
                       "9 orders from the true 0.498. SEE G6 for the contract defect on the "
                       "rejection path."}


# ---------------------------------------------------------------------------
# G5 -- degenerate parameters
# ---------------------------------------------------------------------------
def g5_degenerate_parameters():
    rows = []

    def probe(name, fn):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                nw, r = fn()
            rows.append(row(nw, r, case=name))
        except Exception as e:                                   # noqa: BLE001
            rows.append({"case": name, "raised": "%s: %s" % (type(e).__name__, e),
                         "verdict": RAISED})

    n = 201
    base = TwoScaleNewton(a=0.3, n=n)
    probe("max_iter_0", lambda: (base, base.solve(max_iter=0)))
    probe("max_iter_1", lambda: (base, base.solve(max_iter=1)))
    probe("damping_off", lambda: (base, base.solve(damping=False)))
    probe("tol_absurdly_loose", lambda: (base, base.solve(tol=1e2)))
    probe("tol_below_eps", lambda: (base, base.solve(tol=1e-30)))
    for nn in [11, 21, 51]:
        probe("tiny_grid_n%d" % nn,
              lambda nn=nn: (TwoScaleNewton(a=0.3, n=nn),
                             TwoScaleNewton(a=0.3, n=nn).solve()))
    for rm in [0.5, 2.0, 16.0]:
        probe("rho_max_%.1f" % rm,
              lambda rm=rm: (TwoScaleNewton(a=0.3, n=n, rho_max=rm),
                             TwoScaleNewton(a=0.3, n=n, rho_max=rm).solve()))
    return {"rows": rows,
            "reading": "MOSTLY CLEAN, and the novelty pass's prediction about max_iter = 0 is "
                       "only HALF borne out -- recorded here rather than quietly dropped. The "
                       "flag is indeed computed from hist[0], the residual of the caller's "
                       "own input, so a zero-iteration call CAN return converged=True; but "
                       "from the cold anchor at a = 0.3 that input residual is 0.164, so this "
                       "group's max_iter = 0 row comes back converged=False. The hole is only "
                       "reachable when the caller's own input already has a small residual, "
                       "which is the lam = 1 row of G2(a). No caller in the repository passes "
                       "max_iter, so it carries no banked claim and is NOT what answers the "
                       "gate. Tiny grids, both rho_max extremes, damping=False and both tol "
                       "extremes are all handled without a false convergence claim."}


# ---------------------------------------------------------------------------
# G6 -- the API contract of the failure path
# ---------------------------------------------------------------------------
def g6_failure_path_contract():
    nw = TwoScaleNewton(a=0.0, n=101)
    bad = nw.anchor().copy(); bad[7] = np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = nw.solve(om0=bad, c0=0.5, max_iter=3)
    missing = [k for k in ("residual_rms", "relres") if k not in r]
    return {"returned_keys": sorted(r.keys()),
            "missing_keys_vs_success_path": missing,
            "continuation_reads_relres_unconditionally_at_line": 182,
            "is_loud": True,
            "verdict": CLEAN if not missing else "CONTRACT_GAP",
            "reading": "The LinAlgError branch (lines 145-147) returns a dict WITHOUT "
                       "`residual_rms` and `relres`, which every other return path carries. "
                       "`continuation` reads r['relres'] unconditionally, so a poisoned "
                       "profile anywhere in a sweep raises KeyError instead of being handled. "
                       "This is a LOUD failure -- it cannot by itself answer the gate YES, "
                       "which asks about SILENT wrongness -- and is banked as a robustness "
                       "note, exactly as the novelty pass pre-committed."}


# ---------------------------------------------------------------------------
# controls -- if these move, the battery is measuring itself
# ---------------------------------------------------------------------------
def controls():
    out = {}
    nw = TwoScaleNewton(a=0.0, n=201)
    ex = nw.anchor()
    r = nw.solve(om0=ex * 1.3 + 0.05 * np.exp(-nw.fam.X ** 2), c0=0.4)
    d = diagnostics(nw, r)
    out["C1_anchor_still_converges"] = {
        "converged": bool(r["converged"]), "relres": float(r["relres"]),
        "farfield_inflation": d["farfield_inflation"], "verdict": verdict(r, d)}

    lad = continuation([0.0, 0.15, 0.30], n=201)
    out["C2_a03_reaches_the_floor"] = {
        "rows": [{k: v for k, v in x.items()} for x in lad],
        "a03_relres": lad[-1]["relres"]}

    nw2 = TwoScaleNewton(a=0.3, n=201)
    om = nw2.anchor() * 0.9
    J = nw2.jacobian(om, 0.6)
    rng = np.random.default_rng(4)
    worst = 0.0
    for _ in range(4):
        h = rng.normal(size=201) * 1e-6
        fd = (nw2.residual(om + h, 0.6) - nw2.residual(om - h, 0.6)) / 2.0
        worst = max(worst, float(np.max(np.abs(fd - J[:201, :201] @ h))
                                 / max(np.max(np.abs(fd)), 1e-30)))
    out["C3_jacobian_matches_fd"] = {"worst_relative": worst}
    return out


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    np.seterr(all="ignore")
    data = {
        "meta": {
            "leg": "P2 Route-PNA v1 (leg 202) -- adversarial audit of solver/profile_newton.py",
            "gate": ("Under adversarial and degenerate inputs (near-singular Jacobian, poor "
                     "initial guess, boundary-of-convergence parameters), does "
                     "solver/profile_newton.py ever silently report a converged solution that "
                     "is not (a false-positive convergence claim), or silently return a wrong "
                     "value rather than reject/flag?"),
            "answer": "YES",
            "module_edited": False,
            "reproduce": ".venv/bin/python experiments/p2_route_pna_v1_adversarial.py",
            "arithmetic": "plain float64; no interval arithmetic; nothing here is rigorous",
            "probes_frozen_in": "writeup/novelty/leg_202.md sec 3, commit 5a9f83a",
        },
        "G1_flag_on_stalls": g1_flag_on_stalls(),
        "G2_gauge_blindness": g2_gauge_blindness(),
        "G3_spurious_roots_and_decay_class": g3_spurious_roots(),
        "G4_poisoned_input": g4_poisoned(),
        "G5_degenerate_parameters": g5_degenerate_parameters(),
        "G6_failure_path_contract": g6_failure_path_contract(),
        "controls": controls(),
    }

    g3 = data["G3_spurious_roots_and_decay_class"]
    data["meta"]["seconds"] = round(time.time() - t0, 1)
    g2 = data["G2_gauge_blindness"]
    data["summary"] = {
        "M1_offbranch_roots": (
            "R2 has spurious GRID-SCALE roots that satisfy BOTH gauges to 0.0e+00 and every "
            "residual row to machine precision. Neither solve() nor continuation() computes "
            "any decay-class or smoothness diagnostic, so these are indistinguishable from "
            "the physical branch in every field the module returns. continuation()'s "
            "retry-from-cold-anchor clause (lines 182-189) is the delivery vehicle: it "
            "accepts the spurious root because alt['relres'] < r['relres'], then re-seeds the "
            "remainder of the ladder from it via `if r['relres'] < 1e-10: om, c = ...`."),
        "M2_scaling_family_escape": (
            "From a small-amplitude initial guess at DEFAULT parameters the solve slides down "
            "the exact scaling degeneracy and pays for it with the two gauge rows, which are "
            "only 2 rows against n in an overdetermined least-squares solve. It returns "
            "Omega(0) = -0.75 instead of the gauged -1 and c of order -1e+04..-1e+06, with "
            "converged=True. `converged` never reads the gauge rows; `relres` is exactly "
            "scale-invariant. Neither can see it."),
        "M3_c0_returned_unchecked": (
            "`c0` is never range-checked: solve(om0=anchor, c0=1e9) returns converged=True "
            "with c = 1e9 handed straight back to the caller."),
        "M0_prior_art_flag_degeneracy": (
            "converged=True on iteration-capped stalls, because max(1.0, hist[0]) pins the "
            "denominator at 1 and clause 1 collapses to an absolute residual_rms < 1e-6 test. "
            "NOT this leg's discovery -- test_profile_newton.py item (6) and leg 71 own it."),
        "n_silent_wrong_offbranch": g3["n_silent_wrong"],
        "n_silent_wrong_scaling_family": g2["n_silent_wrong_small_amplitude"],
        "n_silent_wrong_c0": data["G4_poisoned_input"]["n_silent_wrong"],
        "n_silent_degraded": data["G1_flag_on_stalls"]["n_silent_degraded"],
        "worst_farfield_inflation": (g3["worst_departure"]["farfield_inflation"]
                                     if g3["worst_departure"] else None),
        "worst_c_relative_error_scaling_family": g2["worst_c_relative_error"],
        "c_spread_at_a_1p50_relative": g3["c_at_a_1p50_spread_relative"],
        "groups_clean": [
            "G3 half 1 -- leg 114's M2 constant-profile vector IS killed by the two gauges, "
            "exactly as leg 114 predicted",
            "G4 NaN/Inf half -- nothing non-finite is absorbed into a converged answer",
            "G5 -- tiny grids, both rho_max extremes, damping=False and both tol extremes all "
            "handled without a false convergence claim",
            "C1/C2/C3 -- anchor still converges, a = 0.3 still reaches the floor, Jacobian "
            "still matches finite differences",
        ],
    }

    with open(OUT, "w") as fh:
        json.dump(data, fh, indent=1, sort_keys=False)

    s = data["summary"]
    print("Route-PNA v1 -- adversarial audit of solver/profile_newton.py")
    print("  GATE: YES")
    print("  SILENT_WRONG      %d off-branch + %d scaling-family + %d c0"
          % (s["n_silent_wrong_offbranch"], s["n_silent_wrong_scaling_family"],
             s["n_silent_wrong_c0"]))
    print("  SILENT_DEGRADED   %d (prior art: item (6) / leg 71)" % s["n_silent_degraded"])
    print("  M2 worst c error  %.3g relative, worst gauge1 residual %.3g"
          % (s["worst_c_relative_error_scaling_family"],
             g2["worst_gauge1_residual_small_amplitude"]))
    if g3["first_departure"]:
        f = g3["first_departure"]
        print("  first departure   a = %.2f, n = %d: converged=%s, relres = %.2e, "
              "far field x%.0f the anchor's" % (f["a"], f["n"], f["converged"],
                                                f["relres"], f["farfield_inflation"]))
    if g3["worst_departure"]:
        w = g3["worst_departure"]
        print("  worst departure   a = %.2f, n = %d: converged=%s, relres = %.2e, "
              "far field x%.3g, sup|Omega| = %.4g in the FAR FIELD, osc %.2f"
              % (w["a"], w["n"], w["converged"], w["relres"], w["farfield_inflation"],
                 w["sup_abs_Omega"], w["node_oscillation"]))
    print("  c(a=1.50) by grid %s  -> relative spread %.1f%%"
          % (g3["c_at_a_1p50_by_grid"], 100.0 * (g3["c_at_a_1p50_spread_relative"] or 0.0)))
    print("  clean groups      %s" % "; ".join(s["groups_clean"]))
    print("  wrote %s (%.1f s)" % (OUT, data["meta"]["seconds"]))


if __name__ == "__main__":
    main()
