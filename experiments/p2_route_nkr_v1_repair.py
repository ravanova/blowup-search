"""Route-NKR (leg 128): the SHARED hypothesis guard, and the three gates it has to pass.

WHAT THIS LEG DID, IN ONE PARAGRAPH
-----------------------------------------------------------------------------
Three legs have now measured the same defect in three modules: `port_certification.py`
(leg 79, 11/25 hypothesis-violating inputs returning `closes=True`; repaired in place),
`interval_certificate.py` (leg 98, 12/36, 8 load-bearing; repaired in place -- by COPYING
leg 79's function), and `nk_bounds.py` (leg 116, 21/52, 19 load-bearing, a planted
non-solution surviving inside a certified ball, NOT repaired).  This leg closes the class
repository-wide with ONE shared guard, `solver/certificate_guards.py`, rather than a third
private copy of the same twenty lines.

WHAT THIS FILE MEASURES, AND WHY EACH INSTRUMENT IS THE ONE IT IS
-----------------------------------------------------------------------------
GATE (a) -- REJECTION.  Leg 116's own battery (`p2_route_nka_v1_adversarial.py`) is run
UNMODIFIED against both the pre-repair and the post-repair module, by substituting
`sys.modules['solver.nk_bounds']` for the duration of a fresh load of the battery.  Leg
116's file is never edited or copied; the pre-repair run is the NEGATIVE CONTROL, and it
must still reproduce 21/52 or the instrument is not measuring what it claims (lesson 90 --
a control that cannot come out differently is not a control).  This is leg 105's technique,
cited, not reinvented.

GATE (b) -- ZERO REGRESSION, and the instrument choice is NOT free.  Leg 105 established
that comparing against a banked JSON is the WRONG zero-regression test in this repository:
re-running leg 61's literal original source today gives `Y_0 = 2.9616e-17` against the
committed `3.0243e-17` (~2.1%), a BLAS/environment sensitivity of a quantity converged to
its own noise floor, predating every repair.  So the instrument here is the same one leg
105 chose: a SAME-PROCESS BITWISE differential.  The pre-repair sources of all four files
are read out of git at this branch's merge base, loaded as private modules, and called
side by side with the post-repair ones on the same clean inputs in the same process.  The
comparison is `==` on floats and on `repr`, not a tolerance.

GATE (c) -- ROUTING.  Three checks, because "they share a guard" is otherwise unfalsifiable:
identity (`is`) of the function object each module holds; a source-level check that no
module still contains an inline copy of the predicate; and cross-module AGREEMENT on a
common battery of violating constants.  The identity check is shown coming out FALSE on the
pre-repair modules, so it is a control and not a tautology.

MAGNITUDES, NOT BOOLEANS (discipline 73)
-----------------------------------------------------------------------------
Every clean-input comparison records the two values and their ULP distance, so "bit
identical" is a measured 0 rather than an adjective, and any drift would be quotable.

WHAT THIS LEG DID NOT REPAIR, STATED HERE RATHER THAN OMITTED
-----------------------------------------------------------------------------
One clause of leg 116's repair list -- `_I_out`'s bulk log-grid floor -- CANNOT be closed by
a rejection layer.  Lowering `eps = 1e-12 * max(X, 1)` rebuilds the geomspace grid and
therefore moves 100% of clean `_I_out` values, including every one inside the live operating
range, which this leg's gate forbids outright.  It is closed in the FLAG sense instead (a
`RuntimeWarning` above a validated ceiling) and the margin is reported as a magnitude: the
live range tops out at X = 3.2e7 and leg 116 measured the first crossover at X = 1e11, 3.49
decades above it.  `is_flag_not_recompute` in the JSON records this explicitly.

Run: .venv/bin/python experiments/p2_route_nkr_v1_repair.py
"""

import hashlib
import importlib.util
import json
import math
import os
import struct
import subprocess
import sys
import warnings

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_nkr_v1_repair.json")

TERRITORY = ("solver/certificate_guards.py", "solver/nk_bounds.py",
             "solver/port_certification.py", "solver/interval_certificate.py")

#: The two sibling regression suites this leg is measured against.  Legs 86's and 105's
#: files are RUN, never edited -- a repair that has to edit the test that checks it has not
#: been checked.
SIBLING_SUITES = ("test_port_certification_regression.py",
                  "test_port_certification_postrepair.py",
                  "test_port_certification.py",
                  "test_interval_certificate_postrepair.py",
                  "test_interval_certificate_adversarial.py",
                  "test_nk_bounds.py",
                  "test_op_lower.py")


# ===========================================================================
# pre-repair sources, read out of git at this branch's merge base
# ===========================================================================


def _git(args):
    return subprocess.run(["git"] + args, cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def merge_base():
    """The commit this branch forked from -- the pre-repair state of all four files."""
    for base in ("origin/main", "main"):
        try:
            return _git(["merge-base", "HEAD", base]).strip()
        except subprocess.CalledProcessError:
            continue
    raise RuntimeError("no origin/main or main to take a merge base against")


def load_module_from_source(src, name):
    """Load `src` as a standalone module named `name`, via a temp file (removed at once).

    All four modules import their `solver.*` dependencies ABSOLUTELY, which resolve against
    the real installed package regardless of this module's own name, so no package
    shadowing is needed.  Leg 105's helper, reused verbatim in spirit."""
    path = os.path.join(ROOT, f".{name}.tmp.py")
    with open(path, "w") as fh:
        fh.write(src)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        os.remove(path)
    return mod


def prerepair_sources(rev):
    out = {}
    for path in TERRITORY:
        try:
            out[path] = _git(["show", f"{rev}:{path}"])
        except subprocess.CalledProcessError:
            out[path] = None                      # did not exist yet (certificate_guards)
    return out


# ===========================================================================
# the bitwise comparator
# ===========================================================================


def _ulps(a, b):
    """Distance in representable doubles between `a` and `b`; 0 iff bit-identical.

    Reported instead of a relative difference because the gate's word is "bit-identical",
    and a relative difference of 1e-16 is not distinguishable from 0 by eye while an ULP
    count of 1 is."""
    if a == b:
        return 0
    if math.isnan(a) and math.isnan(b):
        return 0
    if math.isnan(a) or math.isnan(b) or math.isinf(a) or math.isinf(b):
        return None
    ia, ib = (struct.unpack("<q", struct.pack("<d", x))[0] for x in (a, b))
    ia = ia if ia >= 0 else (1 << 63) - ia
    ib = ib if ib >= 0 else (1 << 63) - ib
    return abs(ia - ib)


def compare(label, pre, post, rows):
    """Record one pre/post comparison of arbitrarily nested floats/dicts/lists."""
    def walk(p, q, path):
        if isinstance(p, dict) and isinstance(q, dict):
            for k in p:                       # only keys the PRE-repair value had:
                if k in q:                    # new diagnostic keys are additions, not drift
                    walk(p[k], q[k], f"{path}.{k}")
            return
        if isinstance(p, (list, tuple)) and isinstance(q, (list, tuple)):
            if len(p) != len(q):
                rows.append({"where": path, "identical": False,
                             "note": f"length {len(p)} -> {len(q)}"})
                return
            for i, (a, b) in enumerate(zip(p, q)):
                walk(a, b, f"{path}[{i}]")
            return
        if isinstance(p, float) and isinstance(q, float):
            u = _ulps(p, q)
            rows.append({"where": path, "pre": p, "post": q, "ulps": u,
                         "identical": bool(u == 0)})
            return
        rows.append({"where": path, "pre": repr(p), "post": repr(q),
                     "identical": bool(repr(p) == repr(q))})
    walk(pre, post, label)


# ===========================================================================
# GATE (a) -- leg 116's battery, unmodified, against both modules
# ===========================================================================


def _load_leg116_battery(nk_module):
    """Leg 116's own battery bound to `nk_module`, without editing or copying its file.

    `p2_route_nka_v1_adversarial.py` does `from solver.nk_bounds import (...)`, which Python
    resolves through `sys.modules['solver.nk_bounds']` if present.  Substituting that entry
    for the duration of a fresh load under a private name redirects every case to
    `nk_module` without touching leg 116's territory file.  Leg 105's technique."""
    real = sys.modules.get("solver.nk_bounds")
    sys.modules["solver.nk_bounds"] = nk_module
    try:
        path = os.path.join(ROOT, "experiments", "p2_route_nka_v1_adversarial.py")
        spec = importlib.util.spec_from_file_location(
            f"nkr_battery_probe_{id(nk_module)}", path)
        battery = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(battery)
    finally:
        if real is not None:
            sys.modules["solver.nk_bounds"] = real
        else:
            del sys.modules["solver.nk_bounds"]
    return battery


def _b2_cases(battery):
    """Leg 116's B2 family, with the per-case `try/except` its own version does not have.

    THIS IS THE ONE PLACE THE BATTERY IS NOT RUN VERBATIM, and it is stated rather than
    hidden.  Leg 116 wrote B2 (`alpha >= 2`, outside the documented scope) without a
    `try/except` because, pre-repair, nothing in that path could raise -- the whole point of
    the family was that the module evaluated happily outside its own stated hypothesis.
    Post-repair it raises, which is leg 116's own pre-committed `raised` outcome ("sound but
    loud"), so the family is re-expressed here with the guard its siblings B5/B6 already
    have.  Everything else -- the alphas, the reference, the ratio, the outcome rule -- is
    leg 116's, unchanged, and BOTH sides of the differential go through this same code."""
    cases = []
    for a in (2.0, 2.25, 2.5, 3.0):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                m = battery.farfield_modelling_error_bound(a, battery.LIVE_GAMMA, 1.0)
                ref, ref_X = battery._reference_sup(a, battery.LIVE_GAMMA, 1.0)
                ratio = ref / m["bound"]
                rec = {"module_bound": m["bound"], "module_argmax_X": m["argmax_X"],
                       "reference_sup_lower_bound": ref, "reference_argmax_X": ref_X,
                       "reference_over_module": ratio,
                       "argmax_at_window_end": bool(abs(m["argmax_X"] - 1e4) <= 1e-9 * 1e4)}
                outcome = "false_bound" if ratio > 1.0 else "sound"
                exc = ""
            except Exception as ex:                                     # noqa: BLE001
                rec, outcome, exc = {}, "raised", f"{type(ex).__name__}: {ex}"
        cases.append({"case": f"B2_unguarded_alpha_{a}", "family": "B",
                      "hypothesis_violating": True, "alpha": a,
                      "gamma": battery.LIVE_GAMMA, "X0": 1.0, **rec,
                      "exception": exc, "outcome": outcome})
    return cases


def run_leg116_battery_against(nk_module):
    """Assemble leg 116's battery, identically on both sides of the differential."""
    battery = _load_leg116_battery(nk_module)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cases = battery.family_P() + battery.family_A()
        cases += battery.family_B(out_alphas=())     # B2 re-expressed just below
        cases += _b2_cases(battery)
        cC, reach = battery.family_C()
        cases += cC

    false_accepts = [c for c in cases if c["outcome"] == "false_accept"]
    false_bounds = [c for c in cases if c["outcome"] == "false_bound"]
    raised = [c for c in cases if c["outcome"] == "raised"]
    poisoned = [c for c in cases if c["hypothesis_violating"]]
    load_bearing = [c for c in cases if c.get("load_bearing")]
    degenerate = [c for c in cases if c.get("degenerate_ball")]
    survivors = [c for c in cases
                 if c["outcome"] == "false_accept" and c["family"] == "P"
                 and c["ball"]["contains_a_zero"] is False]
    return {
        "totals": {"cases": len(cases), "hypothesis_violating": len(poisoned),
                   "false_accepts": len(false_accepts), "false_bounds": len(false_bounds),
                   "load_bearing": len(load_bearing),
                   "degenerate_balls": len(degenerate), "raised": len(raised)},
        "false_accept_cases": [c["case"] for c in false_accepts],
        "false_bound_cases": [c["case"] for c in false_bounds],
        "load_bearing_cases": [c["case"] for c in load_bearing],
        "degenerate_ball_cases": [c["case"] for c in degenerate],
        "raised_cases": [c["case"] for c in raised],
        "planted_point_survivor_cases": [c["case"] for c in survivors],
        "holder_norm_reachability": reach,
        "cases": cases,
    }


def gate_a(pre_nk, post_nk):
    pre = run_leg116_battery_against(pre_nk)
    post = run_leg116_battery_against(post_nk)

    by_case_pre = {c["case"]: c for c in pre["cases"]}
    by_case_post = {c["case"]: c for c in post["cases"]}
    moved = []
    for name, cpre in by_case_pre.items():
        cpost = by_case_post.get(name)
        if cpost is None:
            continue
        if cpre["outcome"] != cpost["outcome"]:
            moved.append({"case": name, "hypothesis_violating": cpre["hypothesis_violating"],
                          "pre": cpre["outcome"], "post": cpost["outcome"],
                          "load_bearing_pre": bool(cpre.get("load_bearing"))})
    # A clean case whose outcome moved is a STOP, not a success.
    clean_moved = [m for m in moved if not m["hypothesis_violating"]]

    # THE SURVIVORS, CHARACTERISED RATHER THAN COUNTED.  Every case that still returns
    # closes=True is recorded with its constants, so the claim "no validation layer could
    # have caught these" is checkable from the JSON instead of asserted.  A constant tuple
    # that is nonnegative and finite in every slot SATISFIES the theorem's hypotheses: the
    # fabrication is in the VALUE, not the type, and `interval_certificate.py`'s own
    # docstring already states the general fact -- "Validity checking cannot catch this and
    # no amount of it ever will."
    survivors_post = []
    for name in post["false_accept_cases"]:
        c = by_case_post[name]
        k = c.get("constants", {})
        vals = [float(v) for v in k.values()] if k else []
        survivors_post.append({
            "case": name, "constants": k, "verdict": c.get("verdict"),
            "poison": c.get("poison"),
            "all_constants_nonnegative_and_finite": bool(
                vals and all(math.isfinite(v) and v >= 0.0 for v in vals)),
            "flagged_degenerate_ball": bool(
                (c.get("verdict") or {}).get("degenerate_ball")),
            "note": c.get("note", ""),
        })
    return {
        "post_survivors": survivors_post,
        "post_survivors_all_hypothesis_satisfying": bool(
            survivors_post
            and all(s["all_constants_nonnegative_and_finite"] for s in survivors_post)),
        "pre_totals": pre["totals"], "post_totals": post["totals"],
        "pre_false_accept_cases": pre["false_accept_cases"],
        "post_false_accept_cases": post["false_accept_cases"],
        "pre_planted_point_survivors": pre["planted_point_survivor_cases"],
        "post_planted_point_survivors": post["planted_point_survivor_cases"],
        "pre_load_bearing_cases": pre["load_bearing_cases"],
        "post_load_bearing_cases": post["load_bearing_cases"],
        "pre_degenerate_ball_cases": pre["degenerate_ball_cases"],
        "post_degenerate_ball_cases": post["degenerate_ball_cases"],
        "outcomes_that_moved": moved,
        "clean_case_outcomes_that_moved": clean_moved,
        "negative_control_reproduces_leg_116": bool(
            pre["totals"]["false_accepts"] == 21
            and pre["totals"]["load_bearing"] == 19
            and pre["totals"]["degenerate_balls"] == 14),
        "sharpest_pre_ball": next(
            (c["ball"] for c in pre["cases"]
             if c["case"] == "P04_Z0_negative_unit"), None),
        "sharpest_post_verdict": next(
            (c["verdict"] for c in post["cases"]
             if c["case"] == "P04_Z0_negative_unit"), None),
    }


# ===========================================================================
# GATE (b) -- the same-process bitwise differential on CLEAN inputs
# ===========================================================================

# Clean = hypothesis-satisfying.  Read off the in-repo callers (leg 116's
# `live_operating_range`) rather than invented: alpha in [1.1, 1.8], gamma = 0.5,
# X0 in [50, 3200], and every caller passes Y0 = 0.0 literally.
CLEAN_ALPHAS = (1.1, 1.3, 1.5, 1.8)
CLEAN_GAMMAS = (0.15, 0.5, 0.9)
CLEAN_X0S = (50.0, 200.0, 800.0, 3200.0)
CLEAN_XS = (1e-3, 1.0, 10.0, 1e2, 1e3, 1e5, 1e7, 3.2e7)

CLEAN_CONSTANTS = [
    # (Y0, Z0, Z1, Z2) -- all hypothesis-satisfying, spanning closes and does-not-close
    (0.0, 1e-12, 0.3, 13.0),          # the banked gate in test_nk_bounds.py
    (0.0, 0.0, 1.05, 13.0),           # honest refusal: no contraction
    (1e-6, 0.0, 0.3, 1.0),
    (1.0, 0.0, 0.3, 1.0),             # honest refusal: Y0 over budget
    (0.25510204081632654, 0.0, 0.3, 1.0),
    (0.35714285714285715, 0.14285714285714279, 0.0, 0.7142857142857143),
    (0.0, 0.0, 0.0, 1.0),
    (1e-30, 0.5, 0.4, 2.0),
    (0.0, 0.9999, 0.0, 1.0),
]

CLEAN_PORT = [
    (None, None, None), (None, None, 1.0), (1e-6, None, None), (1e-6, 0.3, None),
    (1e-6, 1.5, 1.0), (1e-6, 0.3, 1.0), (1.0, 0.3, 1.0), (0.0, 0.0, 1.0),
    (0.2551, 0.3, 1.0), (1e-30, 0.999, 1e6),
]

CLEAN_INTERVAL = [
    (1e-6, 0.3, 1.0), (1.0, 0.3, 1.0), (0.0, 0.3, 1.0), (1e-6, 1.5, 1.0),
    (1e-6, 0.3, 0.0), (0.2551, 0.3, 1.0), (1e-30, 0.999, 1e6), (0.0, 0.0, 1.0),
]


def _weights(J=125, alpha=1.5, gamma=0.5, seed=0):
    """The module's OWN weight source, so the dual-bound differential is on real input."""
    from solver.decay_collocation import grid
    from solver.holder_norms import HolderNorm
    th, X = grid(J)
    h = HolderNorm(th, X, alpha + 1.0, gamma)
    rng = np.random.default_rng(seed)
    C = rng.normal(size=(6, J))
    cand = np.unique(np.linspace(1, J - 1, 24).astype(int))
    return C, h.w, h.pair, cand


def gate_b(pre, post):
    rows = []
    counters = {}

    def bucket(name, fn_pre, fn_post, args_list):
        start = len(rows)
        for args in args_list:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                a = fn_pre(*args)
                b = fn_post(*args)
            compare(f"{name}{args!r}", a, b, rows)
        seg = rows[start:]
        counters[name] = {"comparisons": len(seg),
                          "identical": sum(1 for r in seg if r["identical"]),
                          "worst_ulps": max((r.get("ulps") or 0 for r in seg), default=0)}

    # --- nk_bounds --------------------------------------------------------------
    bucket("nk_bounds.budget", pre["nk"].budget, post["nk"].budget, CLEAN_CONSTANTS)
    bucket("nk_bounds.farfield_modelling_error_bound",
           pre["nk"].farfield_modelling_error_bound,
           post["nk"].farfield_modelling_error_bound,
           [(a, g, X0) for a in CLEAN_ALPHAS for g in CLEAN_GAMMAS for X0 in CLEAN_X0S])
    bucket("nk_bounds.hilbert_farfield_bound",
           pre["nk"].hilbert_farfield_bound, post["nk"].hilbert_farfield_bound,
           [(X, a, g) for X in CLEAN_XS for a in CLEAN_ALPHAS for g in CLEAN_GAMMAS])
    bucket("nk_bounds._I_out", pre["nk"]._I_out, post["nk"]._I_out,
           [(X, a) for X in CLEAN_XS for a in CLEAN_ALPHAS])
    bucket("nk_bounds.quadratic_constant_upper",
           pre["nk"].quadratic_constant_upper, post["nk"].quadratic_constant_upper,
           [(a, g, 1e-3, 1e6, 40, 401) for a in CLEAN_ALPHAS for g in CLEAN_GAMMAS])
    bucket("nk_bounds.holder_local_X_constant",
           lambda *a: float(pre["nk"].holder_local_X_constant(*a)),
           lambda *a: float(post["nk"].holder_local_X_constant(*a)),
           [(a, g, X) for a in CLEAN_ALPHAS for g in CLEAN_GAMMAS for X in CLEAN_XS])

    C, v, q, cand = _weights()
    bucket("nk_bounds.two_point_dual",
           lambda: [float(x) for x in pre["nk"].two_point_dual(C, v, q, cand)],
           lambda: [float(x) for x in post["nk"].two_point_dual(C, v, q, cand)],
           [()])
    bucket("nk_bounds.sup_part_upper",
           lambda: float(pre["nk"].sup_part_upper(C, np.ones(C.shape[0]), v, q)),
           lambda: float(post["nk"].sup_part_upper(C, np.ones(C.shape[0]), v, q)),
           [()])

    # --- the two already-repaired siblings ---------------------------------------
    bucket("port_certification.radii_polynomial_status",
           pre["pc"].radii_polynomial_status, post["pc"].radii_polynomial_status,
           CLEAN_PORT)
    bucket("port_certification._hypothesis_violations",
           pre["pc"]._hypothesis_violations, post["pc"]._hypothesis_violations,
           CLEAN_PORT)
    bucket("interval_certificate.radii_verdict",
           pre["ic"].radii_verdict, post["ic"].radii_verdict, CLEAN_INTERVAL)
    bucket("interval_certificate._hypothesis_violations",
           pre["ic"]._hypothesis_violations, post["ic"]._hypothesis_violations,
           CLEAN_INTERVAL)

    drifted = [r for r in rows if not r["identical"]]
    return {
        "per_function": counters,
        "total_comparisons": len(rows),
        "total_identical": sum(1 for r in rows if r["identical"]),
        "worst_ulps": max((r.get("ulps") or 0 for r in rows), default=0),
        "drifted": drifted,
        "clean_inputs_bit_identical": bool(not drifted),
        "rows": rows,
    }


def gate_b_suites():
    """Legs 86's and 105's regression suites, RUN (never edited), plus the clean gates."""
    out = []
    for t in SIBLING_SUITES:
        path = os.path.join(ROOT, t)
        if not os.path.exists(path):
            out.append({"suite": t, "status": "MISSING"})
            continue
        r = subprocess.run([sys.executable, path], cwd=ROOT,
                           capture_output=True, text=True)
        out.append({"suite": t, "status": "PASS" if r.returncode == 0 else "FAIL",
                    "returncode": r.returncode,
                    "last_line": (r.stdout.strip().splitlines() or [""])[-1][:300]})
    return out


# ===========================================================================
# GATE (c) -- do all three modules route through the ONE guard?
# ===========================================================================

INLINE_PREDICATE_MARKERS = (
    'is negative ({f!r}); it is an upper bound on a norm',
    'a norm bound is finite ',
)

# One battery of violating constants, fed to all three verdict functions, so "they agree"
# is measured rather than asserted.
DRIFT_BATTERY = [(-1.0, 0.3, 1.0), (float("nan"), 0.3, 1.0), (float("inf"), 0.3, 1.0),
                 (1e-6, -1.0, 1.0), (1e-6, 0.3, -1.0), (1e-6, 0.3, float("-inf")),
                 (-1.0, -1.0, -1.0)]


def gate_c(pre, post, srcs_pre, srcs_post):
    import solver.certificate_guards as cg

    shared = cg.hypothesis_violations
    identity_post = {
        "port_certification": bool(
            getattr(post["pc"], "_shared_hypothesis_violations", None) is shared),
        "interval_certificate": bool(
            getattr(post["ic"], "_shared_hypothesis_violations", None) is shared),
        "nk_bounds": bool(
            getattr(post["nk"], "hypothesis_violations", None) is shared),
    }
    # THE CONTROL: on the pre-repair modules the same check must come out FALSE, or it is
    # a tautology of the code rather than evidence (lesson 90).
    identity_pre = {
        "port_certification": bool(
            getattr(pre["pc"], "_shared_hypothesis_violations", None) is shared),
        "interval_certificate": bool(
            getattr(pre["ic"], "_shared_hypothesis_violations", None) is shared),
        "nk_bounds": bool(
            getattr(pre["nk"], "hypothesis_violations", None) is shared),
    }

    inline_copies = {}
    for path in ("solver/port_certification.py", "solver/interval_certificate.py",
                 "solver/nk_bounds.py"):
        pre_src, post_src = srcs_pre.get(path) or "", srcs_post.get(path) or ""
        inline_copies[path] = {
            "pre": sum(1 for m in INLINE_PREDICATE_MARKERS if m in pre_src),
            "post": sum(1 for m in INLINE_PREDICATE_MARKERS if m in post_src),
        }

    # Cross-module agreement: same violating constants, same set of offending NAMES and the
    # same violation KIND, differing only in the documented `nan_hint` parameter.
    agreement = []
    for (Y0, Z1, Z2) in DRIFT_BATTERY:
        vp = post["pc"]._hypothesis_violations(Y0, Z1, Z2)
        vi = post["ic"]._hypothesis_violations(Y0, Z1, Z2)
        vn = post["nk"].budget(Y0, 0.0, Z1, Z2).get("violations", [])

        def kinds(vs):
            return tuple(sorted((v.split(" is ")[0],
                                 "NaN" if " is NaN" in v else
                                 "infinite" if "infinite" in v else "negative")
                                for v in vs))
        agreement.append({
            "constants": {"Y_0": Y0, "Z_1": Z1, "Z_2": Z2},
            "port": kinds(vp), "interval": kinds(vi), "nk": kinds(vn),
            "agree": bool(kinds(vp) == kinds(vi) == kinds(vn)),
            "n_violations": [len(vp), len(vi), len(vn)],
        })

    return {
        "shared_guard_module": "solver/certificate_guards.py",
        "identity_post_repair": identity_post,
        "identity_pre_repair_CONTROL": identity_pre,
        "control_can_come_out_differently": bool(
            all(identity_post.values()) and not any(identity_pre.values())),
        "inline_predicate_copies": inline_copies,
        "cross_module_agreement": agreement,
        "all_agree": bool(all(a["agree"] for a in agreement)),
        "all_three_route_through_one_guard": bool(
            all(identity_post.values())
            and all(v["post"] == 0 for v in inline_copies.values())
            and all(a["agree"] for a in agreement)),
    }


# ===========================================================================
# the clause that is FLAGGED rather than recomputed, measured
# ===========================================================================


def iout_floor_clause(pre_nk, post_nk):
    """Why `_I_out`'s floor was not lowered, as a magnitude rather than an excuse.

    Measures what a lowered floor WOULD do to clean values inside the live range, by
    re-running the module's own quadrature with a smaller `eps`.  If that number is not
    tiny, "lowering the floor moves clean results" is measured, not argued."""
    from solver.decay_grading import cos_power_mass

    def iout_with_floor(X, alpha, floor, n=1201):
        X = float(X)

        def q(y):
            K = np.abs(2.0 * X / (X * X - y * y))
            return float(np.trapezoid((1.0 + y ** 2) ** (-0.5 * alpha) * K, y))
        eps = floor * max(X, 1.0)
        total = q(np.concatenate(([0.0], np.geomspace(eps, 0.5 * X, n))))
        total += q(np.geomspace(1.5 * X, 1e8 * max(X, 1.0), n))
        return total

    rows = []
    for X in (1.0, 1e3, 1e5, 1e7, 3.2e7):
        for a in (1.2, 1.5, 1.8):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                cur = post_nk._I_out(X, a)
            low = iout_with_floor(X, a, 1e-18)
            rows.append({"X": X, "alpha": a, "current_floor_1e-12": cur,
                         "lowered_floor_1e-18": low,
                         "relative_change": (low - cur) / cur,
                         "ulps": _ulps(cur, low),
                         "identical": bool(cur == low)})
    return {
        "clause": "lower _I_out's bulk floor or bound the [0, eps] panel",
        "resolution": "FLAG, not recompute",
        "why": ("lowering eps rebuilds the geomspace bulk grid, so every clean value in the "
                "live operating range moves; leg 128's gate forbids any clean-input result "
                "moving AT ALL"),
        "n_live_range_values_that_would_move": sum(1 for r in rows if not r["identical"]),
        "n_live_range_values_tested": len(rows),
        "worst_relative_change_if_lowered": max(abs(r["relative_change"]) for r in rows),
        "validated_ceiling_X": post_nk._I_OUT_VALIDATED_X_MAX,
        "leg_116_first_crossover_X": 1e11,
        "leg_116_worst_under_report_percent": 2.124130335509977,
        "live_range_max_X": 3.2e7,
        "decades_of_margin": math.log10(1e11 / 3.2e7),
        "farfield_mass_at_alpha_1p5": float(cos_power_mass(1.5)),
        "rows": rows,
    }


# ===========================================================================
# ASSEMBLY
# ===========================================================================


def run(write=True, verbose=True, run_suites=True):
    import solver.interval_certificate as post_ic
    import solver.nk_bounds as post_nk
    import solver.port_certification as post_pc

    rev = merge_base()
    srcs_pre = prerepair_sources(rev)
    srcs_post = {p: open(os.path.join(ROOT, p)).read() for p in TERRITORY}

    pre = {
        "nk": load_module_from_source(srcs_pre["solver/nk_bounds.py"], "nkr_pre_nk_bounds"),
        "pc": load_module_from_source(srcs_pre["solver/port_certification.py"],
                                      "nkr_pre_port_certification"),
        "ic": load_module_from_source(srcs_pre["solver/interval_certificate.py"],
                                      "nkr_pre_interval_certificate"),
    }
    post = {"nk": post_nk, "pc": post_pc, "ic": post_ic}

    a = gate_a(pre["nk"], post["nk"])
    b = gate_b(pre, post)
    b["sibling_suites"] = gate_b_suites() if run_suites else []
    c = gate_c(pre, post, srcs_pre, srcs_post)
    floor = iout_floor_clause(pre["nk"], post["nk"])

    suites_ok = all(s.get("status") == "PASS" for s in b["sibling_suites"]) \
        if b["sibling_suites"] else None

    data = {
        "leg": 128, "route": "NKR",
        "question": ("Does ONE shared hypothesis guard close the Y0/Z0/Z1 "
                     "fabrication-acceptance gap in all three certificate-assembly "
                     "modules, without moving a single clean-input result?"),
        "merge_base": rev,
        "territory": list(TERRITORY),
        "source_sha256": {p: {"pre": (hashlib.sha256(srcs_pre[p].encode()).hexdigest()
                                      if srcs_pre[p] else None),
                              "post": hashlib.sha256(srcs_post[p].encode()).hexdigest(),
                              "pre_existed": srcs_pre[p] is not None}
                          for p in TERRITORY},
        "gate_a_rejection": a,
        "gate_b_zero_regression": b,
        "gate_b_sibling_suites_all_pass": suites_ok,
        "gate_c_routing": c,
        "iout_floor_clause": floor,
        "gate_answer": {
            "a_false_accepts_pre": a["pre_totals"]["false_accepts"],
            "a_false_accepts_post": a["post_totals"]["false_accepts"],
            "a_rejected_by_the_repair": (a["pre_totals"]["false_accepts"]
                                         - a["post_totals"]["false_accepts"]),
            "a_survivors_are_all_hypothesis_satisfying":
                a["post_survivors_all_hypothesis_satisfying"],
            "a_all_false_accepts_now_reject": bool(a["post_totals"]["false_accepts"] == 0),
            "a_negative_control_holds": a["negative_control_reproduces_leg_116"],
            "b_clean_inputs_bit_identical": b["clean_inputs_bit_identical"],
            "b_sibling_suites_pass": suites_ok,
            "c_one_shared_guard": c["all_three_route_through_one_guard"],
        },
    }
    data["gate_answer"]["YES"] = bool(
        data["gate_answer"]["a_all_false_accepts_now_reject"]
        and data["gate_answer"]["a_negative_control_holds"]
        and data["gate_answer"]["b_clean_inputs_bit_identical"]
        and (suites_ok is not False)
        and data["gate_answer"]["c_one_shared_guard"])

    if write:
        with open(OUT, "w") as fh:
            json.dump(data, fh, indent=2, default=float)

    if verbose:
        print(f"merge base (pre-repair state): {rev}")
        print()
        print("GATE (a) REJECTION -- leg 116's battery, unmodified, both sides")
        print(f"  pre-repair  (negative control): "
              f"{a['pre_totals']['false_accepts']}/{a['pre_totals']['hypothesis_violating']} "
              f"false accepts, {a['pre_totals']['load_bearing']} load-bearing, "
              f"{a['pre_totals']['degenerate_balls']} degenerate balls, "
              f"{len(a['pre_planted_point_survivors'])} planted-point survivors")
        print(f"  post-repair                   : "
              f"{a['post_totals']['false_accepts']}/{a['post_totals']['hypothesis_violating']}"
              f" false accepts, {a['post_totals']['load_bearing']} load-bearing, "
              f"{a['post_totals']['degenerate_balls']} degenerate balls, "
              f"{len(a['post_planted_point_survivors'])} planted-point survivors")
        print(f"  outcomes that moved: {len(a['outcomes_that_moved'])} "
              f"({len(a['clean_case_outcomes_that_moved'])} of them on CLEAN cases -- "
              f"must be 0)")
        sb = a["sharpest_pre_ball"]
        if sb and sb.get("ball_lo") is not None:
            print(f"  sharpest case P04 (Z_0 = -1) pre : certified ball "
                  f"[{sb['ball_lo']:.4f},{sb['ball_hi']:.4f}], contains a zero of F: "
                  f"{sb['contains_a_zero']}, misses sqrt(2) by "
                  f"{sb['gap_in_ball_radii']:.3f} ball radii")
        print(f"  sharpest case P04 (Z_0 = -1) post: closes="
              f"{a['sharpest_post_verdict']['closes']}")
        print(f"  SURVIVORS ({len(a['post_survivors'])}), all hypothesis-SATISFYING: "
              f"{a['post_survivors_all_hypothesis_satisfying']}")
        for s in a["post_survivors"]:
            print(f"    {s['case']:28s} poison={s['poison']} "
                  f"nonneg+finite={s['all_constants_nonnegative_and_finite']} "
                  f"flagged_degenerate={s['flagged_degenerate_ball']}")
        print()
        print("GATE (b) ZERO REGRESSION -- same-process bitwise differential, clean inputs")
        for name, ct in b["per_function"].items():
            print(f"  {name:48s} {ct['identical']:5d}/{ct['comparisons']:<5d} identical, "
                  f"worst {ct['worst_ulps']} ULP")
        print(f"  TOTAL {b['total_identical']}/{b['total_comparisons']} bit-identical, "
              f"worst {b['worst_ulps']} ULP")
        for s in b["sibling_suites"]:
            print(f"  suite {s['suite']:44s} {s['status']}")
        print()
        print("GATE (c) ROUTING -- do all three go through the one guard?")
        print(f"  identity post-repair: {c['identity_post_repair']}")
        print(f"  identity pre-repair (CONTROL, must be all False): "
              f"{c['identity_pre_repair_CONTROL']}")
        print(f"  inline predicate copies: "
              + ", ".join(f"{os.path.basename(k)} {v['pre']}->{v['post']}"
                          for k, v in c["inline_predicate_copies"].items()))
        print(f"  cross-module agreement on {len(c['cross_module_agreement'])} violating "
              f"inputs: {c['all_agree']}")
        print()
        f = floor
        print("THE CLAUSE THAT IS FLAGGED, NOT RECOMPUTED (_I_out's bulk floor)")
        print(f"  lowering eps 1e-12 -> 1e-18 moves "
              f"{f['n_live_range_values_that_would_move']}/"
              f"{f['n_live_range_values_tested']} clean live-range values "
              f"(worst {f['worst_relative_change_if_lowered']:.3e} relative)")
        print(f"  so the floor is UNCHANGED and X > {f['validated_ceiling_X']:.0e} warns; "
              f"live range tops out at {f['live_range_max_X']:.1e}, "
              f"{f['decades_of_margin']:.2f} decades below leg 116's first crossover")
        print()
        print(f"GATE ANSWER: {data['gate_answer']}")
        if write:
            print(f"\nwrote {OUT}")
    return data


if __name__ == "__main__":
    run()
