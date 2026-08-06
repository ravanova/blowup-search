"""Leg 169 (Route-HHB) -- the INDEPENDENT post-repair regression check on hilbert_holder.py.

THE GATE (verbatim, DIRECTION.md section "### 169 -- ROUTE-HHB"):

    Post-repair, does solver/hilbert_holder.py (a) either raise on leg 119's failing
    configuration or provably dominate the true value there, and (b) reproduce every
    previously-validated result bit-identically?

      yes -> Repair confirmed solid and non-regressive. Bank leg 119's battery as a permanent
             regression suite.
      no  -> An incomplete fix or a repair regression. Report the exact case and magnitudes;
             escalate as a priority finding, do not patch under this leg's own authority.

`solver/hilbert_holder.py` is READ-ONLY under this leg and is NOT edited under EITHER branch.

--------------------------------------------------------------------------------
WHY THIS LEG EXISTS, IN ONE PARAGRAPH (see writeup/novelty/leg_169.md for the pass)
--------------------------------------------------------------------------------
`git log -- solver/hilbert_holder.py` is exactly two commits: `07f2b03` (construction) and
`a9eb12b` (leg 153's repair).  Leg 153 wrote the guard, its five pin inversions in
test_hilbert_holder_adversarial.py, and two brand-new gates in that SAME commit.  So every
number on `main` asserting the repair is non-regressive was produced by the agent that wrote
the repair, from a test file it also wrote.  Nothing has independently re-run it.  This leg
re-derives those numbers rather than quoting them, and where a re-derivation disagrees, the
disagreement is the finding (leg 147's precedent, the one post-repair leg of twelve that
answered NO).

--------------------------------------------------------------------------------
METHOD, FIXED IN THE NOVELTY PASS BEFORE ANY OF THIS WAS WRITTEN
--------------------------------------------------------------------------------
B0  The frozen-runner abort census.  Leg 119's own runner is executed as a subprocess against
    the landed module and its abort point is measured, because a battery that does not run is
    not evidence.  Pre-registered in the novelty pass, not discovered here.

B1  Clause (a), re-driven from leg 119's own failing configurations at BOTH entry points, with
    per-case exception capture.  A per-case verdict table, never an aggregate: leg 147's NO
    came from heterogeneity hidden inside a clean headline count, so the table is the product
    and the count is a summary of it.

B2  Clause (a)'s second half -- "or provably dominate".  Under `on_unsound='inflate'` the
    returned pair must dominate; under `'extrapolate'` leg 119's adversary must STILL be able
    to exceed the returned pair, which is what proves the guard is necessary rather than
    decorative.  The adversary machinery is imported verbatim from leg 119's runner.

B3  Clause (b), a same-process two-arm BITWISE differential against the pre-repair module read
    out of git at `07f2b03` and exec'd into a private module object.  Compared with `==` on
    float64 -- not `allclose`, not a tolerance.  capabilities.py:368-371 records this module as
    "no known-answer gate", so no banked absolute number is an admissible referent and the
    two-arm differential is forced, not chosen.  `solver/nk_seminorm.py` (the module's only
    solver import) is verified byte-identical at `07f2b03`, so the differential isolates
    hilbert_holder.py.

B4  The lesson-90 control, wired as a HARD ABORT rather than a reported statistic: the
    pre-repair arm must ACCEPT what the repaired arm rejects.  If both arms agree on the
    unsound configurations the harness is loading one module twice and the whole run is void.

B5  Leg 153's own headline claims, re-derived independently.

Run:  .venv/bin/python experiments/p2_route_hhb_v1_postrepair.py
Writes: writeup/data/p2_route_hhb_v1_postrepair.json
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
import time
import types
import warnings

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from solver import hilbert_holder as HH                                      # noqa: E402

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_hhb_v1_postrepair.json")

PRE_REPAIR_PIN = "07f2b03"        # the module's construction commit; see novelty pass section 2
REPAIR_COMMIT = "a9eb12b"         # leg 153

ALPHA, GAMMA = 1.5, 0.5           # the shipped Route-D pair
PROD_ALPHA, PROD_GAMMA = 1.4, 0.15   # the map's production optimum


# ---------------------------------------------------------------------------
# the two arms
# ---------------------------------------------------------------------------


def load_pre_repair():
    """exec the pre-repair module source out of git into a private module object.

    Same-process, so the comparison is bitwise on the same libm/BLAS in the same run --
    leg 105's finding that a banked JSON is the wrong referent for this kind of quantity,
    and leg 103's template.
    """
    src = subprocess.check_output(
        ["git", "show", "%s:solver/hilbert_holder.py" % PRE_REPAIR_PIN],
        cwd=ROOT)
    mod = types.ModuleType("hilbert_holder_prerepair")
    mod.__file__ = "<git:%s:solver/hilbert_holder.py>" % PRE_REPAIR_PIN
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, hashlib.sha256(src).hexdigest()


def isolation_check():
    """The A/B is only about hilbert_holder.py if its solver import did not move too."""
    out = {}
    for rel in ("solver/nk_seminorm.py",):
        old = subprocess.check_output(["git", "show", "%s:%s" % (PRE_REPAIR_PIN, rel)],
                                      cwd=ROOT)
        with open(os.path.join(ROOT, rel), "rb") as fh:
            new = fh.read()
        out[rel] = {"sha256_at_pin": hashlib.sha256(old).hexdigest(),
                    "sha256_now": hashlib.sha256(new).hexdigest(),
                    "byte_identical": old == new}
    return out


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def call_verdict(fn):
    """Run fn and classify the outcome.  Never returns a boolean verdict -- a tag and a value.

    The tag distinguishes the three outcomes clause (a) cares about, and records the exception
    TYPE and whether the message states a reason, because leg 147's NO was exactly a
    heterogeneity between rejections that a pass/fail count could not see.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            v = fn()
        except Exception as exc:                                   # noqa: BLE001
            return {"outcome": "raised", "exc_type": type(exc).__name__,
                    "exc_module": type(exc).__module__,
                    "is_domain_error": isinstance(exc, HH.HilbertHolderDomainError),
                    "is_value_error": isinstance(exc, ValueError),
                    "message_len": len(str(exc)), "message_head": str(exc)[:160],
                    "n_warnings": len(caught)}
    warn_types = sorted({type(w.message).__name__ for w in caught})
    flat = flatten(v)
    finite = [x for x in flat if x is not None]
    all_finite = bool(finite) and all(math.isfinite(x) for x in finite)
    any_inf = any((not math.isfinite(x)) and not math.isnan(x) for x in finite)
    any_nan = any(math.isnan(x) for x in finite)
    if all_finite:
        outcome = "returned_finite"
    elif any_inf and not any_nan:
        outcome = "returned_infinite"
    else:
        outcome = "returned_nan"
    return {"outcome": outcome, "value": jsonable(v), "leaves": len(flat),
            "n_warnings": len(caught), "warning_types": warn_types}


def flatten(obj, acc=None):
    """Every float64 leaf, in a deterministic order."""
    if acc is None:
        acc = []
    if isinstance(obj, dict):
        for k in sorted(obj):
            flatten(obj[k], acc)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            flatten(v, acc)
    elif isinstance(obj, np.ndarray):
        for v in obj.ravel():
            acc.append(float(v))
    elif isinstance(obj, (float, int, np.floating, np.integer)) and not isinstance(obj, bool):
        acc.append(float(obj))
    elif obj is None:
        acc.append(None)
    return acc


def jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return [jsonable(v) for v in obj.tolist()]
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        if math.isnan(f):
            return "NaN"
        if math.isinf(f):
            return "Infinity" if f > 0 else "-Infinity"
        return f
    if isinstance(obj, (np.integer, int)) and not isinstance(obj, bool):
        return int(obj)
    if isinstance(obj, (bool, np.bool_)):
        return bool(obj)
    if obj is None or isinstance(obj, str):
        return obj
    return repr(obj)


def bit_equal(a, b):
    """float64 identity, == not allclose, with NaN counted equal to NaN and None to None."""
    if a is None or b is None:
        return a is None and b is None
    if math.isnan(a) and math.isnan(b):
        return True
    return a == b


# ---------------------------------------------------------------------------
# the configurations, taken from leg 153's own banked JSON, not re-invented
# ---------------------------------------------------------------------------

FAILING = {                     # leg 119's failing set, as leg 153 enumerated it
    "V1_gamma_0.0":  (1.5, 0.0),
    "V2_gamma_-0.5": (1.5, -0.5),
    "gamma_-1.0":    (1.5, -1.0),
    "gamma_-0.3":    (1.5, -0.3),
    "gamma_nan":     (1.5, float("nan")),
    "gamma_inf":     (1.5, float("inf")),
    "alpha_nan":     (float("nan"), 0.5),
    "alpha_inf":     (float("inf"), 0.5),
}

SOUND = {                       # the six that must NOT be rejected
    "shipped_1.5_0.5":     (ALPHA, GAMMA),
    "production_1.4_0.15": (PROD_ALPHA, PROD_GAMMA),
    "gamma_0.9":           (1.5, 0.9),
    "gamma_0.05":          (1.5, 0.05),
    "gamma_0.01":          (1.5, 0.01),
    "gamma_1e-3":          (1.5, 1e-3),
}


# ---------------------------------------------------------------------------
# B0 -- the frozen-runner abort census
# ---------------------------------------------------------------------------


def block_B0():
    """Does leg 119's OWN runner still execute against the repaired module?  Measured, not assumed."""
    runner = os.path.join(ROOT, "experiments", "p2_route_hha_v1_adversarial.py")
    t0 = time.time()
    proc = subprocess.run([sys.executable, runner], cwd=ROOT, capture_output=True,
                          text=True, timeout=1800)
    wall = time.time() - t0
    all_gates = ["A1_known_answer", "A2_degenerate_input_inventory",
                 "A3_eps_truncation_mechanism", "A4_VIOLATION_gamma_zero",
                 "A5_VIOLATION_gamma_negative",
                 "A6_CONTROL_shipped_and_production_are_safe",
                 "A7_alpha_inf_is_vacuous_not_a_finding", "A8_soundness_predicate"]
    text = proc.stdout + proc.stderr
    started = [g for g in all_gates if ("running %s" % g) in text]
    completed = []
    for g in started:
        idx = text.find("running %s" % g)
        tail = text[idx:]
        nxt = min([tail.find("running %s" % h) for h in all_gates
                   if tail.find("running %s" % h) > 0] or [len(tail)])
        if "done in" in tail[:nxt]:
            completed.append(g)
    aborted_in = [g for g in started if g not in completed]
    exc_line = ""
    for ln in text.splitlines():
        if "Error" in ln and ":" in ln:
            exc_line = ln.strip()
    return {"returncode": proc.returncode, "wall_seconds": wall,
            "n_gates_total": len(all_gates), "n_gates_started": len(started),
            "n_gates_completed": len(completed),
            "n_gates_never_executed": len(all_gates) - len(started),
            "gates_completed": completed, "aborted_in_gate": aborted_in,
            "gates_never_executed": [g for g in all_gates if g not in started],
            "terminating_exception": exc_line,
            "stderr_tail": proc.stderr[-700:],
            "note": ("leg 119's frozen battery is not a runnable post-repair regression "
                     "suite in its shipped form: the guard it verifies is the thing that "
                     "stops it.  Third instance of the shape leg 131 found and leg 147 "
                     "confirmed.  This is a statement about the HARNESS, not about the "
                     "repair's correctness -- the abort is the guard behaving as designed.")}


# ---------------------------------------------------------------------------
# B1 -- clause (a), per-case, both entry points, both policies
# ---------------------------------------------------------------------------


def block_B1():
    low, asm, infl = {}, {}, {}
    for name, (a, g) in FAILING.items():
        low[name] = call_verdict(
            lambda a=a, g=g: HH.increment_pair_bound(1.0, 0.05, a, g))
        asm[name] = call_verdict(
            lambda a=a, g=g: HH.hilbert_holder_constant(a, g, n_theta=16, n_d=10,
                                                        n_quad=100))
        infl[name] = call_verdict(
            lambda a=a, g=g: HH.increment_pair_bound(1.0, 0.05, a, g,
                                                     on_unsound="inflate"))
    sound = {}
    for name, (a, g) in SOUND.items():
        sound[name] = call_verdict(
            lambda a=a, g=g: HH.increment_pair_bound(1.0, 0.05, a, g))

    n_low_rejected = sum(1 for v in low.values() if v["outcome"] == "raised")
    n_asm_rejected = sum(1 for v in asm.values() if v["outcome"] == "raised")
    n_sound_wrongly_rejected = sum(1 for v in sound.values() if v["outcome"] == "raised")
    # the leg-147 heterogeneity probe: are the rejections ALIKE?
    exc_types_low = sorted({v.get("exc_type") for v in low.values()
                            if v["outcome"] == "raised"})
    all_domain = all(v.get("is_domain_error") for v in low.values()
                     if v["outcome"] == "raised")
    silent_reasons = [k for k, v in low.items()
                      if v["outcome"] == "raised" and v.get("message_len", 0) < 40]
    # inflate must be honest, never a finite non-dominating number
    n_inflate_finite = sum(1 for v in infl.values() if v["outcome"] == "returned_finite")
    return {"low_level_increment_pair_bound": low,
            "assembly_hilbert_holder_constant": asm,
            "inflate_policy": infl,
            "sound_configurations": sound,
            "n_failing_probed": len(FAILING),
            "n_failing_rejected_at_low_level": n_low_rejected,
            "n_failing_rejected_at_assembly": n_asm_rejected,
            "n_sound_wrongly_rejected": n_sound_wrongly_rejected,
            "n_sound_probed": len(SOUND),
            "n_inflate_returning_finite": n_inflate_finite,
            "rejection_homogeneity": {
                "distinct_exception_types": exc_types_low,
                "all_are_HilbertHolderDomainError": all_domain,
                "cases_whose_message_states_no_reason": silent_reasons,
                "why": ("leg 147's NO came from a heterogeneity INSIDE a clean headline "
                        "count -- 3 of 4 survivors flagged, 1 silent.  The same probe is "
                        "run here rather than trusting the aggregate.")},
            "note": ("every entry is a TAG plus the returned value or the exception type, "
                     "never a boolean; 'raised' and 'returned_infinite' both satisfy "
                     "clause (a), 'returned_finite' on a failing configuration does not")}


# ---------------------------------------------------------------------------
# B2 -- clause (a) second half: the adversary must still exceed the pre-repair number
# ---------------------------------------------------------------------------


def block_B2():
    """Import leg 119's adversary verbatim and re-attain its violation through 'extrapolate'.

    This is the control that proves the guard is NECESSARY: if the extrapolated (pre-repair)
    pair could not be exceeded, the guard would be rejecting sound inputs.
    """
    sys.path.insert(0, os.path.join(ROOT, "experiments"))
    import importlib
    hha = importlib.import_module("p2_route_hha_v1_adversarial")

    def ratio_through(alpha, gamma, delta, theta1=1.0, sigma=0.05, policy="extrapolate"):
        th2 = theta1 + sigma
        psi1 = hha.psi_generic(theta1, theta1, delta, alpha)
        psi2 = hha.psi_generic(th2, theta1, delta, alpha)
        T = hha.T_seminorm(theta1, delta, alpha, gamma)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            uS, uT = HH.increment_pair_bound(theta1, sigma, alpha, gamma,
                                             n_quad=4000, eps=1e-10,
                                             on_unsound=policy)
        inner = min(abs(theta1), abs(th2))
        w = np.cos(0.5 * inner) ** -(1.0 - gamma)
        lhs = w * abs(psi1 - psi2) / abs(sigma) ** gamma
        bound = uS * 1.0 + uT * T
        return {"alpha": alpha, "gamma": gamma, "delta": delta, "T": float(T),
                "u_S": float(uS), "u_T": float(uT),
                "true_weighted_increment": float(lhs), "bound": float(bound),
                "ratio_true_over_bound": float(lhs / bound) if bound > 0 else None,
                "n_warnings": len(caught),
                "warning_types": sorted({type(w_.message).__name__ for w_ in caught})}

    deltas = (1e-3, 1e-20, 1e-40, 1e-45, 1e-50)
    v1 = [ratio_through(1.5, 0.0, d) for d in deltas]
    v2 = [ratio_through(1.5, -0.5, d) for d in deltas]
    ship = [ratio_through(ALPHA, GAMMA, d, policy="raise") for d in deltas]
    prod = [ratio_through(PROD_ALPHA, PROD_GAMMA, d, policy="raise") for d in deltas]
    worst_v = max([r["ratio_true_over_bound"] for r in v1 + v2
                   if r["ratio_true_over_bound"] is not None])
    worst_sound = max([r["ratio_true_over_bound"] for r in ship + prod
                       if r["ratio_true_over_bound"] is not None])
    return {"V1_gamma_0.0_through_extrapolate": v1,
            "V2_gamma_-0.5_through_extrapolate": v2,
            "CONTROL_shipped_1.5_0.5": ship,
            "CONTROL_production_1.4_0.15": prod,
            "worst_ratio_still_attainable_through_extrapolate": worst_v,
            "worst_ratio_on_sound_configurations": worst_sound,
            "leg_153_banked_worst_ratio": 1.231122838838451,
            "note": ("the extrapolated pre-repair pair is STILL exceeded by leg 119's "
                     "adversary, so the guard removes a real violation and is not "
                     "decorative; on both sound configurations the ratio stays below 1 "
                     "and FALLS as delta shrinks, the opposite asymptotics, which is the "
                     "control that can report the other answer")}


# ---------------------------------------------------------------------------
# B3 -- clause (b): the same-process bitwise two-arm differential
# ---------------------------------------------------------------------------


def surfaces(mod, reduced=False):
    """Every previously-validated surface, evaluated on ONE arm.

    Only gamma > 0 configurations appear: those are exactly the inputs the pre-repair module
    also accepted, i.e. the 'previously-validated' surface clause (b) is about.  A surface
    the pre-repair module could not evaluate is not a regression candidate.
    """
    out = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # S1 -- the low-level bound over a dense sound grid
        s1 = {}
        thetas = (0.3, 0.7, 1.0, 1.6, 2.0, 2.5, 2.9, np.pi - 0.2)
        sigmas = (0.005, 0.01, 0.05, 0.2, 0.6)
        for a in (1.05, 1.2, 1.4, 1.5, 1.8, 2.4):
            for g in (1e-6, 1e-3, 0.01, 0.05, 0.15, 0.3, 0.5, 0.9):
                rows = []
                for th in thetas:
                    for sg in sigmas:
                        rows.append(list(mod.increment_pair_bound(th, sg, a, g)))
                s1["alpha=%s,gamma=%s" % (a, g)] = rows
        out["S1_increment_pair_bound_sound_grid"] = s1

        # S2 -- the assembly at the PRODUCTION grid, the number Route-D actually ships
        s2 = {}
        for label, (a, g) in (("shipped_1.5_0.5", (ALPHA, GAMMA)),
                              ("production_1.4_0.15", (PROD_ALPHA, PROD_GAMMA))):
            r = mod.hilbert_holder_constant(a, g)
            s2[label] = {k: r[k] for k in ("b_sup", "b_semi", "argmax_sup", "argmax_semi",
                                           "n_increment_route", "alpha", "gamma")}
        out["S2_hilbert_holder_constant_default_grid"] = s2

        # S3 -- all three rules, reduced grid
        s3 = {}
        for rule in ("increment", "sum", "pointwise"):
            r = mod.hilbert_holder_constant(ALPHA, GAMMA, n_theta=24, n_d=14,
                                            n_quad=200, rule=rule)
            s3[rule] = {k: r[k] for k in ("b_sup", "b_semi", "argmax_sup", "argmax_semi",
                                          "n_increment_route")}
        out["S3_hilbert_holder_constant_all_rules"] = s3

        # S4 -- the refinement sweep
        out["S4_sweep_convergence"] = mod.sweep_convergence(
            ALPHA, GAMMA, levels=((16, 10), (24, 14)), n_quad=200)

        # S5 -- the pointwise route
        s5 = {}
        for a, g in ((ALPHA, GAMMA), (PROD_ALPHA, PROD_GAMMA), (1.5, 0.05)):
            s5["alpha=%s,gamma=%s" % (a, g)] = [
                list(mod.pointwise_pair_bound(th, sg, a, g))
                for th in thetas for sg in sigmas]
        out["S5_pointwise_pair_bound"] = s5

        # S6 -- the pure geometry and the algebra downstream of the bound
        out["S6_pair_grid"] = [list(p) for p in mod.pair_grid(n_theta=12, n_d=8)]
        out["S6_near_padding"] = [mod.near_padding(d) for d in
                                  (0.01, 0.1, 0.5, 1.0, 2.0, 2.5, 3.0)]
        out["S6_increment_regime"] = [bool(mod.increment_regime(th, sg))
                                      for th in thetas for sg in sigmas]
        out["S6_wrap"] = [float(x) for x in mod.wrap(np.linspace(-8.0, 8.0, 33))]
        out["S6_cos_half"] = [float(x) for x in mod.cos_half(np.linspace(-8.0, 8.0, 33))]
        out["S6_conjugate"] = [float(x) for x in
                               mod.conjugate(np.array([0.0, 1.0, 0.5, 0.25]),
                                             np.linspace(0.0, np.pi, 17))]
        out["S6_weighted_seminorm"] = float(mod.weighted_seminorm(
            np.cos(np.linspace(0.05, np.pi - 0.05, 40)),
            np.linspace(0.05, np.pi - 0.05, 40), 1.0, 0.5))
        out["S6_quadratic_constant_full"] = mod.quadratic_constant_full(
            ALPHA, GAMMA, 1.0, 2.0, 1.19, 4.94)
        out["S6_cq_sup_split"] = mod.cq_sup_split(ALPHA, GAMMA)
        out["S6_decomposition_exact"] = mod.decomposition_exact(
            np.array([0.0, 1.0, 0.5]), 1.0, 0.05)

        # S7 -- the eps ladder, on SOUND gammas only
        s7 = {}
        for g in (1e-3, 0.05, 0.15, 0.5):
            s7["gamma=%s" % g] = [list(mod.increment_pair_bound(1.0, 0.05, 1.5, g,
                                                                n_quad=4000, eps=e))
                                  for e in (1e-6, 1e-10, 1e-14, 1e-16)]
        out["S7_eps_ladder_sound"] = s7
    return out


def block_B3(pre):
    t0 = time.time()
    post_s = surfaces(HH)
    t_post = time.time() - t0
    t0 = time.time()
    pre_s = surfaces(pre)
    t_pre = time.time() - t0

    per_surface, total, moved_total = {}, 0, 0
    moved_examples = []
    for key in sorted(post_s):
        a = flatten(post_s[key])
        b = flatten(pre_s[key])
        if len(a) != len(b):
            per_surface[key] = {"n_leaves_post": len(a), "n_leaves_pre": len(b),
                                "SHAPE_MISMATCH": True}
            continue
        moved = [i for i in range(len(a)) if not bit_equal(a[i], b[i])]
        per_surface[key] = {"n_leaves": len(a), "n_moved": len(moved)}
        total += len(a)
        moved_total += len(moved)
        for i in moved[:5]:
            moved_examples.append({"surface": key, "index": i,
                                   "post": jsonable(a[i]), "pre": jsonable(b[i])})

    dump = "\n".join("%s:%s" % (k, ",".join(
        "None" if x is None else float(x).hex() for x in flatten(post_s[k])))
        for k in sorted(post_s))
    digest = hashlib.sha256(dump.encode()).hexdigest()

    return {"n_surface_groups": len(post_s),
            "n_float64_leaves_compared": total,
            "n_leaves_moved": moved_total,
            "per_surface": per_surface,
            "moved_examples": moved_examples[:25],
            "comparison_operator": "== on float64 (NOT allclose, NOT a tolerance)",
            "sha256_of_post_repair_hex_dump": digest,
            "seconds_post_arm": t_post, "seconds_pre_arm": t_pre,
            "note": ("both arms evaluated in ONE process on the same libm/BLAS, so a moved "
                     "leaf can only come from the module's own source; capabilities.py "
                     "records this module as 'no known-answer gate', which is why the "
                     "referent is the other arm and not a banked absolute number")}


# ---------------------------------------------------------------------------
# B4 -- the lesson-90 control: the pre-repair arm MUST come out differently
# ---------------------------------------------------------------------------


def block_B4(pre):
    """What would have had to change in the code for this to report the other answer?

    Answer: the pre-repair arm must ACCEPT gamma = 0.0 and gamma = -0.3 and hand back a
    finite pair where the repaired arm raises.  If it does not, the two arms are the same
    object and every zero in B3 is a tautology.  Wired as a hard abort.
    """
    out = {}
    for name, (a, g) in FAILING.items():
        out[name] = {
            "pre_repair": call_verdict(
                lambda a=a, g=g: pre.increment_pair_bound(1.0, 0.05, a, g)),
            "post_repair": call_verdict(
                lambda a=a, g=g: HH.increment_pair_bound(1.0, 0.05, a, g)),
        }
    # the assembly's split polarity leg 153 names: ZeroDivisionError at 0.0, silent finite at -0.3
    asm = {}
    for name, (a, g) in (("V1_gamma_0.0", (1.5, 0.0)), ("gamma_-0.3", (1.5, -0.3))):
        asm[name] = {
            "pre_repair": call_verdict(
                lambda a=a, g=g: pre.hilbert_holder_constant(a, g, n_theta=24, n_d=14,
                                                             n_quad=200)),
            "post_repair": call_verdict(
                lambda a=a, g=g: HH.hilbert_holder_constant(a, g, n_theta=24, n_d=14,
                                                            n_quad=200)),
        }
    n_pre_accept = sum(1 for v in out.values()
                       if v["pre_repair"]["outcome"].startswith("returned"))
    n_pre_silent_finite = sum(1 for v in out.values()
                              if v["pre_repair"]["outcome"] == "returned_finite")
    n_diverge = sum(1 for v in out.values()
                    if v["pre_repair"]["outcome"] != v["post_repair"]["outcome"])
    return {"low_level": out, "assembly_split_polarity": asm,
            "n_failing_where_pre_repair_ACCEPTS": n_pre_accept,
            "n_failing_where_pre_repair_returns_a_SILENT_FINITE_pair": n_pre_silent_finite,
            "n_failing_where_the_two_arms_DIVERGE": n_diverge,
            "CONTROL_IS_LIVE": n_diverge > 0,
            "why": ("lesson 90: a control that cannot come out differently is not a "
                    "control.  The thing that had to change for this to report the other "
                    "answer is named in advance -- the pre-repair arm accepting what the "
                    "repaired arm rejects -- and the run aborts if it does not.")}


# ---------------------------------------------------------------------------
# B5 -- leg 153's headline claims, re-derived rather than quoted
# ---------------------------------------------------------------------------


def block_B5(pre):
    out = {}

    # (i) the discarded-head shares that set HEAD_WARN_TOL, on TWO grids.
    #
    # Leg 153 measured this on pair_grid(n_theta=24, n_d=14) with n_quad=200 (481
    # increment-regime pairs).  But `hilbert_holder_constant`'s own DEFAULT -- the grid the
    # module actually ships and the one every banked b_sup/b_semi is computed on -- is
    # pair_grid(n_theta=48, n_d=28) with n_quad=400.  Both are computed here: leg 153's grid
    # as a reproduction control, and the shipped grid as the measurement that matters.  A grid
    # supremum can only UNDER-report (test_nk_hilbert_holder.py gate 3's own point), so the
    # finer grid is expected to move the worst share UP, and the question is by how much and
    # whether HEAD_WARN_TOL still separates the two configurations.
    def head_scan(a, g, n_theta, n_d, n_quad):
        worst, arg, n_pairs, n_warn = 0.0, None, 0, 0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for th, sg in HH.pair_grid(n_theta=n_theta, n_d=n_d):
                if not HH.increment_regime(th, sg):
                    continue
                n_pairs += 1
                uS, uT = HH.increment_pair_bound(th, sg, a, g, n_quad=n_quad)
                h = HH._head_bound(th, sg, a, g, 1e-10)
                tot = float(uS) + float(uT)
                if tot <= 0.0:
                    continue
                share = float(h) / tot
                if share > HH.HEAD_WARN_TOL:
                    n_warn += 1
                if share > worst:
                    worst, arg = share, [float(th), float(sg), float(uS), float(uT),
                                         float(h)]
        return {"worst_head_over_value": worst, "argmax": arg, "n_pairs": n_pairs,
                "n_pairs_warned": n_warn,
                "fraction_warned": (n_warn / n_pairs) if n_pairs else 0.0}

    heads = {"HEAD_WARN_TOL": HH.HEAD_WARN_TOL}
    for gname, (nt, nd, nq) in (("leg_153_grid_24x14_nquad200", (24, 14, 200)),
                                ("SHIPPED_default_grid_48x28_nquad400", (48, 28, 400))):
        g_out = {}
        for label, (a, g) in (("shipped_1.5_0.5", (ALPHA, GAMMA)),
                              ("production_1.4_0.15", (PROD_ALPHA, PROD_GAMMA))):
            g_out[label] = head_scan(a, g, nt, nd, nq)
        ws = g_out["shipped_1.5_0.5"]["worst_head_over_value"]
        wp = g_out["production_1.4_0.15"]["worst_head_over_value"]
        g_out["production_over_shipped"] = wp / ws if ws else None
        g_out["margin_below_worst_shipped"] = HH.HEAD_WARN_TOL / ws if ws else None
        g_out["margin_above_worst_production"] = wp / HH.HEAD_WARN_TOL
        g_out["band_still_separates"] = bool(ws < HH.HEAD_WARN_TOL < wp)
        heads[gname] = g_out
    heads["leg_153_banked"] = {
        "worst_shipped": 1.3926124218598773e-05,
        "worst_production": 0.050804197109344515,
        "production_over_shipped": 3648.121782620173,
        "margin_below_worst_shipped": 71.8074881641849,
        "margin_above_worst_production": 50.804197109344514,
        "n_pairs": 481, "grid": "pair_grid(n_theta=24, n_d=14), n_quad=200"}
    rep = heads["leg_153_grid_24x14_nquad200"]
    heads["reproduction_on_leg_153s_OWN_grid"] = {
        "shipped_matches_banked": bit_equal(rep["shipped_1.5_0.5"]["worst_head_over_value"],
                                            1.3926124218598773e-05),
        "production_matches_banked": bit_equal(
            rep["production_1.4_0.15"]["worst_head_over_value"], 0.050804197109344515),
        "why": ("the reproduction control: on leg 153's own grid this leg must recover leg "
                "153's own numbers bitwise, otherwise the shipped-grid disagreement below "
                "would be a harness difference rather than a grid-resolution effect")}
    shp = heads["SHIPPED_default_grid_48x28_nquad400"]
    heads["grid_resolution_effect"] = {
        "worst_shipped_24x14": rep["shipped_1.5_0.5"]["worst_head_over_value"],
        "worst_shipped_48x28": shp["shipped_1.5_0.5"]["worst_head_over_value"],
        "shipped_ratio": (shp["shipped_1.5_0.5"]["worst_head_over_value"]
                          / rep["shipped_1.5_0.5"]["worst_head_over_value"]),
        "worst_production_24x14": rep["production_1.4_0.15"]["worst_head_over_value"],
        "worst_production_48x28": shp["production_1.4_0.15"]["worst_head_over_value"],
        "production_ratio": (shp["production_1.4_0.15"]["worst_head_over_value"]
                             / rep["production_1.4_0.15"]["worst_head_over_value"]),
        "margin_below_shipped_24x14": rep["margin_below_worst_shipped"],
        "margin_below_shipped_48x28": shp["margin_below_worst_shipped"],
        "margin_above_production_24x14": rep["margin_above_worst_production"],
        "margin_above_production_48x28": shp["margin_above_worst_production"],
        "note": ("HEAD_WARN_TOL is a WARNING threshold: it changes no returned value and "
                 "can reject nothing, so a moved margin is not a soundness question and is "
                 "NOT a clause-(a) or clause-(b) failure.  It is reported because leg 153's "
                 "banked margins are quoted on a coarser grid than the module ships.")}
    out["i_head_warning_band"] = heads

    # (ii) leg 119's eps-drift ladder, extended below its own gamma floor of 0.05 -- on BOTH
    # eps pairs, because legs 119 and 153 did not use the same one and that is the whole
    # disagreement.  Leg 119's gate A8, which is where its "1.98x when unsound" floor is
    # banked, compares eps = 1e-8 against 1e-16 (8 decades).  Leg 153's novelty section 4b,
    # which reports "3 SOUND gammas above leg 119's 1.98 floor", tabulates u(1e-16)/u(1e-6)
    # (10 decades).  A drift measured over 10 decades cannot be compared against a floor
    # banked over 8; both are computed here so the comparison can be made like-for-like.
    ladders = {}
    for pname, (lo, hi) in (("leg_119_gate_A8_pair_1e-8_to_1e-16", (1e-8, 1e-16)),
                            ("leg_153_novelty_4b_pair_1e-6_to_1e-16", (1e-6, 1e-16))):
        rows = []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for g in (-1.0, -0.5, -0.1, 0.0, 1e-6, 1e-3, 0.01, 0.05, 0.15, 0.5, 0.9):
                policy = "extrapolate" if g <= 0 else "raise"
                b1 = HH.increment_pair_bound(1.0, 0.05, 1.5, g, n_quad=4000, eps=lo,
                                             on_unsound=policy)
                b2 = HH.increment_pair_bound(1.0, 0.05, 1.5, g, n_quad=4000, eps=hi,
                                             on_unsound=policy)
                s1, s2 = sum(b1), sum(b2)
                rows.append({"gamma": g, "drift": (s2 / s1) if s1 else None,
                             "sound": bool(g > 0.0)})
        sound_d = [r["drift"] for r in rows if r["sound"] and r["drift"] is not None]
        unsound_d = [r["drift"] for r in rows if not r["sound"] and r["drift"] is not None]
        # leg 119's own ladder stopped at gamma = 0.05; this is its max-when-sound
        sound_119 = [r["drift"] for r in rows
                     if r["sound"] and r["gamma"] >= 0.05 and r["drift"] is not None]
        ladders[pname] = {
            "eps_lo": lo, "eps_hi": hi, "rows": rows,
            "max_drift_when_sound_extended_ladder": max(sound_d),
            "max_drift_when_sound_leg_119s_OWN_ladder_gamma_ge_0.05": max(sound_119),
            "min_drift_when_unsound": min(unsound_d),
            "n_sound_above_leg_119_banked_unsound_floor_1.98":
                sum(1 for d in sound_d if d > 1.98),
            "separation_survives_the_extension": bool(max(sound_d) < min(unsound_d)),
            "margin_on_leg_119s_own_ladder": min(unsound_d) / max(sound_119),
            "margin_on_the_extended_ladder": min(unsound_d) / max(sound_d)}
    out["ii_eps_drift_ladder"] = {
        "by_eps_pair": ladders,
        "leg_119_banked": {"max_when_sound": 1.34, "min_when_unsound": 1.98,
                           "margin": 1.98 / 1.34,
                           "measured_on": "gate A8's pair, 1e-8 -> 1e-16"},
        "leg_153_banked": {"max_when_sound": 2.3816, "margin": 1.103,
                           "n_sound_above_1.98": 3,
                           "measured_on": "novelty 4b's pair, 1e-6 -> 1e-16"},
        "adjudication": (
            "Both legs reproduce, and their disagreement is the eps pair, not the module.  "
            "On leg 153's own 10-decade pair its numbers stand: 3 sound gammas above 1.98 "
            "and max-when-sound ~2.38.  But leg 119's 1.98 floor is banked from gate A8's "
            "8-decade pair, and on THAT pair 0 sound gammas cross it -- the separation leg "
            "119 reported is narrowed, not broken.  What is robust across both readings, "
            "and is the only thing the repair rests on, is that the margin COLLAPSES once "
            "the gamma ladder goes below 0.05 (1.478x -> 1.102x on leg 119's own pair) "
            "because the drift is continuous through gamma = 0+.  So leg 153's conclusion "
            "-- no fixed threshold on this diagnostic is safe, use the exact predicate -- "
            "is correct and unaffected; its supporting comparison mixed two eps pairs."),
        "note": ("the diagnostic is a diagnostic, never the guard's predicate, which is the "
                 "exact threshold-free gamma > 0 measured in (iii); nothing in the module's "
                 "behaviour depends on which reading of this table is taken")}

    # (iii) the guard's predicate is exactly gamma > 0 on a fine ladder through the boundary
    fine = []
    for g in (-1e-12, -1e-30, 0.0, 5e-324, 1e-300, 1e-30, 1e-12, 1e-6):
        v = call_verdict(lambda g=g: HH.increment_pair_bound(1.0, 0.05, 1.5, g))
        fine.append({"gamma": jsonable(g), "outcome": v["outcome"],
                     "predicate_says_sound": bool(g > 0.0),
                     "agrees": (v["outcome"] == "raised") != bool(g > 0.0)})
    out["iii_predicate_boundary_ladder"] = {
        "rows": fine, "n_disagreements": sum(1 for r in fine if not r["agrees"]),
        "note": ("the guard is threshold-free: the smallest positive float64, 5e-324, is "
                 "ACCEPTED and 0.0 is rejected, so the implemented predicate is exactly "
                 "the analytic one and not an epsilon-thresholded approximation of it")}
    return out


# ---------------------------------------------------------------------------
# B6 -- the capabilities-registered validated line, re-run against BOTH arms
# ---------------------------------------------------------------------------


def block_B6():
    """capabilities.py:368-371 names test_nk_hilbert_holder.py as this module's validated line.

    Leg 153 asserts it printed byte-identical output pre- and post-repair.  That assertion was
    made by the agent that wrote the repair; here it is re-measured, by running the test file
    unmodified in two subprocesses whose ONLY difference is which hilbert_holder source is
    bound into sys.modules, and diffing the two stdouts byte-for-byte.
    """
    shim = r'''
import sys, os, types, subprocess, runpy
ROOT = %r
sys.path.insert(0, ROOT)
ARM = sys.argv[1]
import solver
if ARM == "pre":
    src = subprocess.check_output(["git", "show", "%s:solver/hilbert_holder.py"], cwd=ROOT)
    m = types.ModuleType("solver.hilbert_holder")
    m.__file__ = "<git pre-repair>"
    m.__package__ = "solver"
    sys.modules["solver.hilbert_holder"] = m
    exec(compile(src, m.__file__, "exec"), m.__dict__)
    solver.hilbert_holder = m
runpy.run_path(os.path.join(ROOT, "test_nk_hilbert_holder.py"), run_name="__main__")
''' % (ROOT, PRE_REPAIR_PIN)
    path = os.path.join(ROOT, ".hhb_capability_shim.py")
    with open(path, "w") as fh:
        fh.write(shim)
    try:
        runs = {}
        for arm in ("post", "pre"):
            p = subprocess.run([sys.executable, path, arm], cwd=ROOT,
                               capture_output=True, text=True, timeout=1800)
            runs[arm] = {"returncode": p.returncode, "stdout": p.stdout,
                         "sha256_stdout": hashlib.sha256(p.stdout.encode()).hexdigest(),
                         "n_stdout_bytes": len(p.stdout),
                         "stderr_tail": p.stderr[-400:]}
    finally:
        if os.path.exists(path):
            os.remove(path)
    same = runs["post"]["stdout"] == runs["pre"]["stdout"]
    diff_lines = []
    if not same:
        a = runs["post"]["stdout"].splitlines()
        b = runs["pre"]["stdout"].splitlines()
        for i in range(max(len(a), len(b))):
            la = a[i] if i < len(a) else "<absent>"
            lb = b[i] if i < len(b) else "<absent>"
            if la != lb:
                diff_lines.append({"line": i, "post": la, "pre": lb})
    return {"post_repair": {k: v for k, v in runs["post"].items() if k != "stdout"},
            "pre_repair": {k: v for k, v in runs["pre"].items() if k != "stdout"},
            "stdout_byte_identical": same,
            "n_differing_lines": len(diff_lines),
            "differing_lines": diff_lines[:20],
            "post_repair_exit_zero": runs["post"]["returncode"] == 0,
            "note": ("the capabilities-registered validated line, re-run independently "
                     "rather than taken from leg 153's own commit message; the two "
                     "subprocesses differ ONLY in which hilbert_holder source is bound")}


# ---------------------------------------------------------------------------


def main():
    t_start = time.time()
    pre, pre_sha = load_pre_repair()

    res = {"leg": 169, "route": "HHB",
           "module_checked": "solver/hilbert_holder.py",
           "module_edited": False,
           "read_only": True,
           "gate": ("Post-repair, does solver/hilbert_holder.py (a) either raise on leg "
                    "119's failing configuration or provably dominate the true value "
                    "there, and (b) reproduce every previously-validated result "
                    "bit-identically?"),
           "pre_repair_pin": PRE_REPAIR_PIN,
           "repair_commit": REPAIR_COMMIT,
           "pre_repair_source_sha256": pre_sha,
           "ab_isolation": isolation_check(),
           "capabilities_entry": {
               "line": "capabilities.py:368-371",
               "validated": "no known-answer gate; bounds checked against dense sampling",
               "test": "test_nk_hilbert_holder.py",
               "consequence": ("no banked absolute number is an admissible referent for "
                               "clause (b); the two-arm differential is forced")}}

    print("  B0 frozen-runner abort census ...", flush=True)
    res["B0_frozen_runner_abort_census"] = block_B0()
    print("     done", flush=True)

    print("  B4 lesson-90 control (run EARLY -- it can void the run) ...", flush=True)
    res["B4_lesson_90_control"] = block_B4(pre)
    if not res["B4_lesson_90_control"]["CONTROL_IS_LIVE"]:
        raise SystemExit("VOID: the two arms never diverge -- the harness is loading one "
                         "module twice.  Nothing in this run is evidence.")
    print("     control LIVE: %d of %d failing configurations diverge between the arms"
          % (res["B4_lesson_90_control"]["n_failing_where_the_two_arms_DIVERGE"],
             len(FAILING)), flush=True)

    print("  B1 clause (a), per-case ...", flush=True)
    res["B1_clause_a_per_case"] = block_B1()
    print("     done", flush=True)

    print("  B2 clause (a), dominance through the adversary ...", flush=True)
    res["B2_clause_a_dominance"] = block_B2()
    print("     done", flush=True)

    print("  B3 clause (b), bitwise two-arm differential ...", flush=True)
    res["B3_clause_b_bitwise"] = block_B3(pre)
    print("     %d leaves, %d moved"
          % (res["B3_clause_b_bitwise"]["n_float64_leaves_compared"],
             res["B3_clause_b_bitwise"]["n_leaves_moved"]), flush=True)

    print("  B5 leg 153's claims, re-derived ...", flush=True)
    res["B5_leg_153_claims_rederived"] = block_B5(pre)
    print("     done", flush=True)

    print("  B6 capabilities-registered validated line, both arms ...", flush=True)
    res["B6_capabilities_validated_line"] = block_B6()
    print("     byte-identical stdout: %s (post exit %d)"
          % (res["B6_capabilities_validated_line"]["stdout_byte_identical"],
             res["B6_capabilities_validated_line"]["post_repair"]["returncode"]),
          flush=True)

    b1, b3 = res["B1_clause_a_per_case"], res["B3_clause_b_bitwise"]
    clause_a = (b1["n_failing_rejected_at_low_level"] == b1["n_failing_probed"]
                and b1["n_failing_rejected_at_assembly"] == b1["n_failing_probed"]
                and b1["n_sound_wrongly_rejected"] == 0
                and b1["n_inflate_returning_finite"] == 0
                and not b1["rejection_homogeneity"]["cases_whose_message_states_no_reason"])
    b6 = res["B6_capabilities_validated_line"]
    clause_b = (b3["n_leaves_moved"] == 0
                and not any(v.get("SHAPE_MISMATCH") for v in b3["per_surface"].values())
                and b6["stdout_byte_identical"]
                and b6["post_repair_exit_zero"])
    res["gate_answer"] = {
        "clause_a_reject_or_dominate": "YES" if clause_a else "NO",
        "clause_b_bit_identical": "YES" if clause_b else "NO",
        "gate": "YES" if (clause_a and clause_b) else "NO",
        "branch": ("Repair confirmed solid and non-regressive. Bank leg 119's battery as a "
                   "permanent regression suite."
                   if (clause_a and clause_b) else
                   "An incomplete fix or a repair regression. Report the exact case and "
                   "magnitudes; escalate as a priority finding, do not patch under this "
                   "leg's own authority.")}
    res["wall_seconds"] = time.time() - t_start

    with open(OUT, "w") as fh:
        json.dump(jsonable(res), fh, indent=1, sort_keys=True)
    print("\nGATE: (a) %s  (b) %s  ->  %s"
          % (res["gate_answer"]["clause_a_reject_or_dominate"],
             res["gate_answer"]["clause_b_bit_identical"],
             res["gate_answer"]["gate"]))
    print("wrote %s in %.1fs" % (OUT, res["wall_seconds"]))


if __name__ == "__main__":
    main()
