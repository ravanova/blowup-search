"""ROUTE-CGF (leg 216) -- the REST of leg 199's finding, repaired in `certificate_guards.py`.

WHAT THIS LEG IS FOR
-----------------------------------------------------------------------------
Leg 199 (`leg/199-cga-v1`, unmerged) turned the fabrication-acceptance battery on the ONE
shared hypothesis guard and found **16 silent accepts across five mechanisms** in 67 cases,
all LATENT, 0 banked numbers impeached.  Its gate forbade it from patching the module it
audited.  Leg 215 (`leg/215-cgr-v1`, unmerged) repaired **M1 only** -- a missing `isinf`
test at `nk_bounds.py:430` -- and its gate then failed on its own arithmetic, because it was
asked for 16 and only 1 of the 16 was M1.  Its report named the other 15 exactly, and every
one of them lives at a surface inside `solver/certificate_guards.py`:

    M2  (5)  no `numbers.Real` gate in `radius_violation` / `unit_range_violation`,
             while `hypothesis_violations` in the SAME FILE raises on the same values
    M3  (3)  `bool` IS `numbers.Real`, so a FLAG passes every guard here silently
    M4  (1)  `float()` underflows a negative rational to `-0.0` BEFORE the `f < 0.0` test
    M5  (5)  an EMPTY container is a vacuous pass in two guards
    M7  (1)  `invalid_input_reason([])` assembles a rejection naming zero violations

This leg repairs those surfaces and measures what moved.  `solver/nk_bounds.py` is
READ-ONLY here (leg 215's territory), as is every consumer.

THE GATE (pre-committed, both branches, verbatim)
-----------------------------------------------------------------------------
    Does repairing the remaining mechanisms in `certificate_guards.py` (per leg 199's own
    identified defects) cause all 15 remaining previously-silently-accepted adversarial
    cases to now raise/reject, while every one of leg 199's own confirmed-safe live call
    sites stays bit-identical to its pre-repair banked value?

    YES -> bank the repair; leg 199's finding is fully closed (16/16 with leg 215's M1).
           Normal landing straight to `main`; flag a postrepair-verification leg.
    NO  -> report exactly which mechanism resists repair or which live call site's value
           moved; escalate rather than declare the module fully closed on a partial fix.
           Push the branch only, never `main`.

HOW THE TWO CLAUSES ARE MEASURED
-----------------------------------------------------------------------------
Clause 1.  Each of the 15 is re-driven **at the surface leg 199 measured it at** -- leg
215's correction, adopted here as method: scoring a downstream crash, or a different
surface, as a repair would be claiming a case this leg never touched.  The "before" column
is not retyped: it is READ from leg 199's own banked JSON on its own branch
(`git show leg/199-cga-v1:writeup/data/p2_route_cga_v1_adversarial.json`), so the before/after
table cannot drift from the finding it repairs.

Clause 2.  The live battery is measured TWICE in two separate interpreters: once against
the pre-repair `certificate_guards.py` (reconstructed from the merge-base blob and injected
into `sys.modules` BEFORE any consumer imports it), once against the repaired tree.  Values
are compared as `float.hex()`, not `==`, so "bit-identical" means bit-identical and 0 ULP is
a measurement rather than a phrase.

Run:  .venv/bin/python experiments/p2_route_cgf_v1_repair.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import traceback
from decimal import Decimal
from fractions import Fraction

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_cgf_v1_repair.json")
LEG199_BRANCH = "leg/199-cga-v1"
LEG199_JSON = "writeup/data/p2_route_cga_v1_adversarial.json"
GUARD_PATH = "solver/certificate_guards.py"

# Leg 199's live parameters, from its own blast-radius table: "every in-repo alpha is in
# [1.1, 1.8]", gamma = 0.5, and `budget` at the banked `test_nk_bounds.py::test_decay_and_budget`
# constants.  None of these is invented here.
LIVE_ALPHAS = (1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8)
LIVE_GAMMA, LIVE_X0, LIVE_NX = 0.5, 1.0, 8
LIVE_BUDGET = (0.0, 1e-12, 0.3, 13.0)          # test_nk_bounds.py:214
LIVE_BUDGET_OPEN = (0.0, 0.0, 1.05, 13.0)      # test_nk_bounds.py:216
LIVE_TRIPLE = (1e-6, 0.3, 13.0)                # a hypothesis-satisfying (Y0, Z1, Z2)


def _git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def _hex(x):
    """A float as its exact bit pattern; ints/bools/None pass through unchanged."""
    if isinstance(x, float):
        return float.hex(x)
    if isinstance(x, (bool, int, type(None), str)):
        return x
    if isinstance(x, np.floating):
        return float.hex(float(x))
    if isinstance(x, (list, tuple)):
        return [_hex(v) for v in x]
    if isinstance(x, dict):
        return {k: _hex(v) for k, v in x.items()}
    return repr(x)


# ---------------------------------------------------------------------------
# CLAUSE 2 -- the live battery, run in both variants by the same code
# ---------------------------------------------------------------------------

def measure_live():
    """Every live call path leg 199 confirmed safe, at its own live parameters.

    Returned as a flat {label: hex} map so the pre/post comparison is a dict diff and a
    silently-missing entry cannot be mistaken for agreement.
    """
    import solver.certificate_guards as cg
    import solver.interval_certificate as ic
    import solver.nk_bounds as nk
    import solver.port_certification as pc

    live = {}

    # (a) the 8 alpha call paths -- leg 199's M1/M2/M3 blast-radius table, leg 215's 8 hexes
    for a in LIVE_ALPHAS:
        d = nk.farfield_modelling_error_bound(a, LIVE_GAMMA, LIVE_X0, n_X=LIVE_NX)
        live[f"farfield_bound[alpha={a}]"] = _hex(float(d["bound"]))
        live[f"farfield_argmaxX[alpha={a}]"] = _hex(float(d["argmax_X"]))

    # (b) the gamma call site -- the surface M3's 1.2605x lived at, driven at the LIVE gamma
    b = nk.hilbert_farfield_bound(1.0, 1.5, LIVE_GAMMA)
    for i, v in enumerate(b):
        live[f"hilbert_farfield_bound[{i}]"] = _hex(float(v))

    # (c) `budget` -- the `hypothesis_violations` + `invalid_input_reason` + `radius_violation`
    #     consumer, at both banked tuples
    for lbl, args in (("closing", LIVE_BUDGET), ("open", LIVE_BUDGET_OPEN)):
        out = nk.budget(*args)
        for k in ("one_minus_Z", "Y0_max", "closes", "r_min", "degenerate_ball"):
            live[f"budget[{lbl}].{k}"] = _hex(out[k])
        live[f"budget[{lbl}].reason"] = out.get("reason")

    # (d) the two other pipelines' verdict functions, same shared guard
    live["port_certification.radii_polynomial_status"] = _hex(
        _flat(pc.radii_polynomial_status(*LIVE_TRIPLE)))
    live["interval_certificate.radii_verdict"] = _hex(
        _flat(ic.radii_verdict(*LIVE_TRIPLE)))

    # (e) the guard's own surface on the clean constants tuple every consumer passes
    live["hypothesis_violations[clean 4-tuple]"] = cg.hypothesis_violations(
        (("Y_0", 0.0), ("Z_0", 1e-12), ("Z_1", 0.3), ("Z_2", 13.0)))
    live["hypothesis_violations[clean 3-tuple, allow_none]"] = cg.hypothesis_violations(
        (("Y_0", 1e-6), ("Z_1", 0.3), ("Z_2", None)), allow_none=True)
    live["radius_violation[live r_min]"] = cg.radius_violation(
        nk.budget(*LIVE_BUDGET)["r_min"])
    live["unit_range_violation[live gamma]"] = cg.unit_range_violation(
        "gamma", LIVE_GAMMA, 0.0, 1.0, lo_open=True, hi_open=False)
    live["unit_range_violation[live alpha]"] = cg.unit_range_violation(
        "alpha", 1.5, -float("inf"), 2.0, lo_open=False, hi_open=True)

    # (f) `positive_weight_violations` on a NON-empty dirty vector: the message builder is
    #     the thing the empty-container fix must not have moved
    live["positive_weight_violations[dirty]"] = cg.positive_weight_violations(
        "v_cod", [1.0, -3.0, float("nan"), float("inf")])
    live["positive_weight_violations[clean]"] = cg.positive_weight_violations(
        "v_cod", [1.0, 2.0, 3.0])
    live["positive_weight_violations[allow_zero]"] = cg.positive_weight_violations(
        "q_cod", [1.0, 0.0], allow_zero=True)

    # (g) `two_point_dual` on a clean, non-empty, live-shaped weight set: the guard is not
    #     consulted on the clean path, and the returned bound must not move
    rng = np.random.default_rng(216)
    C = rng.standard_normal((3, 12))
    v = np.linspace(1.0, 4.0, 12)
    q = np.abs(rng.standard_normal((12, 12))) + 0.5
    np.fill_diagonal(q, 0.0)
    d = nk.two_point_dual(C, v, q, np.arange(1, 11))
    live["two_point_dual[clean]"] = _hex([float(x) for x in np.ravel(d)])

    # (h) the rejection sentence on a NON-empty violation list -- M7's fix must not move it
    live["invalid_input_reason[one violation]"] = cg.invalid_input_reason(
        cg.hypothesis_violations((("Y_0", -1.0), ("Z_1", 0.3), ("Z_2", 13.0))))
    return live


def _flat(obj):
    """Verdict dicts carry nested dicts; flatten to a comparable, JSON-safe shape."""
    if isinstance(obj, dict):
        return {k: _flat(v) for k, v in sorted(obj.items())}
    if isinstance(obj, (list, tuple)):
        return [_flat(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return [_flat(v) for v in obj.tolist()]
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    return obj


def _run_pre_variant():
    """Measure the live battery against the PRE-repair guard, in this interpreter.

    The merge-base blob is written to a temp file and installed as
    `sys.modules['solver.certificate_guards']` BEFORE any consumer is imported, so
    `nk_bounds`, `port_certification` and `interval_certificate` bind the old functions at
    import time exactly as they did before the edit.
    """
    base = _git("merge-base", "HEAD", "origin/main").strip()
    src = _git("show", f"{base}:{GUARD_PATH}")
    import solver                                    # the package, not the module
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(src)
        tmp = fh.name
    spec = importlib.util.spec_from_file_location("solver.certificate_guards", tmp)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["solver.certificate_guards"] = mod
    spec.loader.exec_module(mod)
    solver.certificate_guards = mod
    out = {"merge_base": base, "live": measure_live()}
    os.unlink(tmp)
    return out


# ---------------------------------------------------------------------------
# CLAUSE 1 -- leg 199's 15 remaining cases, at leg 199's own surfaces
# ---------------------------------------------------------------------------

def _call(fn, *a, **kw):
    try:
        return ("value", fn(*a, **kw))
    except Exception as e:                                            # noqa: BLE001
        return ("raise", f"{type(e).__name__}: {e}")


def _accepted_list(kind, out):
    """Guard-level ACCEPT for the list-returning guards: an EMPTY violation list."""
    return kind == "value" and out == []


def _accepted_reason(kind, out):
    """Guard-level ACCEPT for the `None`-returning guards: `None` means admissible."""
    return kind == "value" and out is None


def clause_one():
    import solver.certificate_guards as cg
    import solver.nk_bounds as nk

    Y0Z = (("Z_0", 0.0), ("Z_1", 0.3), ("Z_2", 13.0))
    cases = []

    def rec(case, mech, surface, probe, kind, out, accepted, note, consumer=None):
        cases.append({
            "case": case, "mechanism": mech, "surface": surface, "probe": probe,
            "after_outcome_kind": kind, "after_output": str(out)[:220],
            "after_accepted": bool(accepted),
            "now_rejects": (not accepted),
            "consumer_after": consumer, "note": note})

    # --- M3 (3): bool is numbers.Real -------------------------------------------------
    for lbl, val in (("A1_bool_True", True), ("A1_bool_False", False)):
        k, o = _call(cg.hypothesis_violations, (("Y_0", val),) + Y0Z)
        c = _call(nk.budget, val, 0.0, 0.3, 13.0)
        rec(lbl, "M3", "hypothesis_violations", repr(val), k, o, _accepted_list(k, o),
            "a FLAG in a norm slot is now refused by type, before any coercion to 1.0/0.0",
            consumer={"budget": str(c[1])[:160]})
    k, o = _call(cg.unit_range_violation, "gamma", True, 0.0, 1.0,
                 lo_open=True, hi_open=False)
    c = _call(nk.hilbert_farfield_bound, 1.0, 1.5, True)
    rec("C3_gamma_bool", "M3", "unit_range_violation", "True", k, o,
        _accepted_reason(k, o),
        "the 1.2605493138651522x-smaller claimed bound is no longer reachable: the flag is "
        "refused at the guard, not evaluated as the exponent 1.0",
        consumer={"hilbert_farfield_bound(gamma=True)": str(c[1])[:160]})

    # --- M2 (5): the missing type gate ------------------------------------------------
    for lbl, val in (("B_nonreal_str", "0.5"), ("B_nonreal_bool_True", True),
                     ("B_nonreal_Decimal", Decimal("0.5")),
                     ("B_nonreal_Fraction", Fraction(1, 2))):
        k, o = _call(cg.radius_violation, val)
        sib = _call(cg.hypothesis_violations, (("Y_0", val),))
        agrees = ((k == "raise") == (sib[0] == "raise"))
        rec(lbl, "M2", "radius_violation", repr(val), k, o, _accepted_reason(k, o),
            f"sibling `hypothesis_violations` on the same value: {str(sib[1])[:80]!r}; "
            f"the two guards now AGREE: {agrees}")
        cases[-1]["siblings_agree"] = bool(agrees)
    k, o = _call(cg.unit_range_violation, "gamma", "0.5", 0.0, 1.0,
                 lo_open=True, hi_open=False)
    c = _call(nk.hilbert_farfield_bound, 1.0, 1.5, "0.5")
    rec("C4_gamma_str", "M2", "unit_range_violation", "'0.5'", k, o,
        _accepted_reason(k, o),
        "the unnamed TypeError from the power operator three lines downstream (leg 98's "
        "B20/B21 shape) is replaced by a NAMED refusal at the guard",
        consumer={"hilbert_farfield_bound(gamma='0.5')": str(c[1])[:160]})

    # --- M4 (1): the float() underflow ------------------------------------------------
    neg = Fraction(-1, 10 ** 400)
    k, o = _call(cg.hypothesis_violations, (("Y_0", neg),) + Y0Z)
    c = _call(nk.budget, neg, 0.0, 0.3, 13.0)
    rec("A3_fraction_neg_below_denormal", "M4", "hypothesis_violations",
        "Fraction(-1, 10**400)", k, o, _accepted_list(k, o),
        "the sign is now read from the EXACT value, not from its float64 shadow -0.0; "
        "leg 199's magnitude for this one is <= 1 ULP and is not inflated here",
        consumer={"budget.closes": _flat(c[1]).get("closes") if c[0] == "value" else c[1],
                  "budget.r_min": (_hex(_flat(c[1])["r_min"]) if c[0] == "value" else None)})

    # --- M5 (5): the empty container --------------------------------------------------
    k, o = _call(cg.hypothesis_violations, ())
    rec("A6_empty_constants", "M5", "hypothesis_violations", "()", k, o,
        _accepted_list(k, o), "zero constants examined is no longer 'every constant is "
        "admissible'")
    for lbl, vals in (("D1_empty_list", []), ("D1_empty_ndarray", np.array([])),
                      ("D1_exhausted_generator", "GEN")):
        v = (x for x in []) if isinstance(vals, str) else vals
        k, o = _call(cg.positive_weight_violations, "v_cod", v)
        rec(lbl, "M5", "positive_weight_violations", str(vals)[:40], k, o,
            _accepted_list(k, o), "an empty weight vector defines no norm and is refused")
    # D1b was measured by leg 199 AT THE CONSUMER, and its accept flag IS the numpy
    # pre-screen at `nk_bounds.py:225` -- a property of a file this leg may not edit.
    screen_passes_empty = bool(np.all(np.isfinite(np.array([])))
                               and np.all(np.array([]) > 0.0))
    c = _call(nk.two_point_dual, np.zeros((1, 0)), np.array([], dtype=int),
              np.zeros((0, 0)), np.array([]))
    rec("D1b_empty_at_the_consumer", "M5", "nk_bounds.py:225 numpy pre-screen",
        "two_point_dual with empty weights", "value",
        {"screen_treats_empty_as_clean": screen_passes_empty}, screen_passes_empty,
        "OUT OF TERRITORY: leg 199's accept flag for this case is literally "
        "`np.all(isfinite([])) and np.all([] > 0)`, evaluated in `solver/nk_bounds.py`. "
        "The guard is never consulted, so no edit to `certificate_guards.py` can move it; "
        "the repaired guard DOES now refuse the same empty vector at its own surface "
        "(D1_empty_ndarray).",
        consumer={"two_point_dual(empty)": str(c[1])[:120]})

    # --- M7 (1): the empty rejection sentence -----------------------------------------
    k, o = _call(cg.invalid_input_reason, [])
    rec("E_empty_violation_list", "M7", "invalid_input_reason", "[]", k, o,
        k == "value", "an accusation with no charge is no longer representable")
    return cases


# ---------------------------------------------------------------------------
# CONTROLS -- over-rejection is the failure mode a rejection layer creates
# ---------------------------------------------------------------------------

def controls():
    import solver.certificate_guards as cg
    out = []

    def rec(name, ok, detail):
        out.append({"control": name, "pass": bool(ok), "detail": str(detail)[:200]})

    # the types the repair must NOT start refusing
    for lbl, v in (("float", 0.5), ("np.float64", np.float64(0.5)),
                   ("int", 1), ("np.int64", np.int64(1)),
                   ("Fraction", Fraction(1, 2))):
        k, o = _call(cg.hypothesis_violations, (("Y_0", v),))
        rec(f"admissible_type_{lbl}_not_refused", k == "value" and o == [], (k, o))
        k2, o2 = _call(cg.radius_violation, v)
        rec(f"radius_admissible_type_{lbl}_not_refused", k2 == "value" and o2 is None,
            (k2, o2))

    # leg 199's own M4 discrimination control: a Fraction is judged on its VALUE, not
    # refused on its type.  If this flipped to a TypeError the repair would have
    # re-litigated leg 199's measurement instead of repairing it.
    k, o = _call(cg.hypothesis_violations, (("Y_0", Fraction(-1, 3)),))
    rec("M4_control_Fraction_minus_one_third_still_refused_BY_VALUE",
        k == "value" and len(o) == 1 and "negative" in o[0], (k, o))

    # -0.0 is a legitimate bound and must stay admissible
    k, o = _call(cg.hypothesis_violations, (("Y_0", -0.0), ("Z_1", 0.0), ("Z_2", 0.0)))
    rec("minus_zero_still_admissible", k == "value" and o == [], (k, o))

    # `allow_none` semantics (port_certification's kill switch) unmoved
    k, o = _call(cg.hypothesis_violations, (("Y_0", None), ("Z_1", 0.3), ("Z_2", 13.0)),
                 allow_none=True)
    rec("allow_none_kill_switch_unmoved", k == "value" and o == [], (k, o))
    k, o = _call(cg.hypothesis_violations, (("Y_0", None),), allow_none=False)
    rec("None_still_raises_without_allow_none", k == "raise" and "TypeError" in o, (k, o))

    # the pre-existing rejection MESSAGES are byte-identical (no quoted string moved)
    k, o = _call(cg.hypothesis_violations, (("Y_0", "0.5"),))
    rec("str_message_byte_identical",
        o == "TypeError: Y_0 must be a real number, got str; the radii polynomial's "
             "constants are norms.", o)
    k, o = _call(cg.hypothesis_violations, (("Y_0", -1.0),))
    rec("negative_message_byte_identical",
        o == ["Y_0 is negative (-1.0); it is an upper bound on a norm"], o)

    # a one-element container is NOT empty and must still be evaluated
    k, o = _call(cg.positive_weight_violations, "v_cod", [1.0])
    rec("single_entry_weight_not_refused_as_empty", k == "value" and o == [], (k, o))
    return out


def main():
    if "--pre-variant" in sys.argv:
        json.dump(_run_pre_variant(), sys.stdout)
        return

    post_live = measure_live()
    pre = json.loads(subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--pre-variant"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    pre_live = pre["live"]

    moved = [k for k in sorted(set(pre_live) | set(post_live))
             if pre_live.get(k, "<MISSING>") != post_live.get(k, "<MISSING>")]
    bit_identical = {k: {"pre": pre_live.get(k), "post": post_live.get(k),
                         "identical": pre_live.get(k) == post_live.get(k)}
                     for k in sorted(post_live)}

    cases = clause_one()
    ctrl = controls()

    # leg 199's own banked before-column, read from its branch rather than retyped
    banked = json.loads(_git("show", f"{LEG199_BRANCH}:{LEG199_JSON}"))
    before = {c["case"]: c for c in banked["cases"]}
    for c in cases:
        b = before.get(c["case"])
        c["before_accepted"] = (bool(b["guard_accepted"]) if b else None)
        c["before_output"] = (str(b["guard_output"])[:160] if b else None)
        c["before_status"] = (b["status"] if b else None)
        c["repaired_by_this_leg"] = bool(c["before_accepted"] and c["now_rejects"])

    n_repaired = sum(1 for c in cases if c["repaired_by_this_leg"])
    resist = [c["case"] for c in cases if not c["now_rejects"]]
    ctrl_fail = [c["control"] for c in ctrl if not c["pass"]]

    gate_yes = (n_repaired == len(cases)) and (not moved) and (not ctrl_fail)
    payload = {
        "leg": 216, "route": "CGF",
        "module_repaired": GUARD_PATH,
        "modules_read_only": ["solver/nk_bounds.py", "solver/port_certification.py",
                              "solver/interval_certificate.py",
                              "solver/chen_inviscid_certificate.py"],
        "repairs_the_finding_of": {"leg": 199, "branch": LEG199_BRANCH,
                                   "gate_hits": banked["totals"]["gate_hits"]},
        "m1_repaired_elsewhere_by": {"leg": 215, "branch": "leg/215-cgr-v1",
                                     "file": "solver/nk_bounds.py",
                                     "landed_on_main": _m1_on_main()},
        "gate": ("Does repairing the remaining mechanisms in certificate_guards.py cause "
                 "all 15 remaining previously-silently-accepted adversarial cases to now "
                 "raise/reject, while every one of leg 199's own confirmed-safe live call "
                 "sites stays bit-identical to its pre-repair banked value?"),
        "gate_answer": "YES" if gate_yes else "NO",
        "clause_1_cases_now_rejecting": n_repaired,
        "clause_1_cases_total": len(cases),
        "clause_1_cases_resisting": resist,
        "clause_2_live_sites_compared": len(post_live),
        "clause_2_live_sites_moved": moved,
        "clause_2_merge_base": pre["merge_base"],
        "controls_total": len(ctrl), "controls_failed": ctrl_fail,
        "cases": cases, "live_bit_identity": bit_identical, "controls": ctrl,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=False)
        fh.write("\n")

    print(f"CLAUSE 1  {n_repaired} of {len(cases)} previously-accepted cases now reject")
    for c in cases:
        flag = "REPAIRED" if c["repaired_by_this_leg"] else "STILL ACCEPTS"
        print(f"  [{flag:13s}] {c['case']:32s} {c['mechanism']}  {c['surface']}")
    print(f"CLAUSE 2  {len(post_live)} live values compared as float.hex(); "
          f"moved: {len(moved)}")
    for k in moved:
        print(f"  MOVED {k}: {pre_live.get(k)} -> {post_live.get(k)}")
    print(f"CONTROLS  {len(ctrl) - len(ctrl_fail)} of {len(ctrl)} pass"
          + ("" if not ctrl_fail else f"; FAILED: {ctrl_fail}"))
    print(f"GATE ANSWER: {payload['gate_answer']}")
    print(f"wrote {OUT}")


def _m1_on_main():
    try:
        src = _git("show", "origin/main:solver/nk_bounds.py")
    except Exception:                                                 # noqa: BLE001
        return None
    return "isinf(float(alpha))" in src


if __name__ == "__main__":
    try:
        main()
    except Exception:                                                 # noqa: BLE001
        traceback.print_exc()
        sys.exit(1)
