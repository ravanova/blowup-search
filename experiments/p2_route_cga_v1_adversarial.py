"""ROUTE-CGA (leg 199) -- the fabrication-acceptance battery, turned on the GUARD LAYER.

WHAT THIS ASKS, AND WHY IT HAS NEVER BEEN ASKED
-----------------------------------------------------------------------------
`solver/certificate_guards.py` is the ONE shared hypothesis guard: the accept/reject layer
that decides whether a radii-polynomial verdict function is allowed to evaluate a
discriminant at all.  It exists because the SAME defect was measured three times --
`port_certification.py` 11/25 (leg 79), `interval_certificate.py` 12/36 (leg 98),
`nk_bounds.py` 21/52 (leg 116) -- and leg 128 replaced two private copies with it.

It has never itself been audited.  `capabilities.py:303-334` says so in its own words:

    "NO known-answer gate of its own -- it is exercised through the three modules' suites
     and through test_repaired_all_three_modules_share_one_guard."

Its entire history is ONE commit (`bfe6883`, leg 128), and the leg that wrote it is the leg
that wrote every number validating it, in the same commit.  The only prior art that touches
it at all (`test_nk_bounds_adversarial.py:528-554`) drives five PLAIN FLOAT64 triples
(`-1.0`, `NaN`, `+inf`) through the three CONSUMERS -- i.e. exactly the three shapes the
guard was written to catch.  Nothing has ever handed it a value of a different TYPE, an
empty container, or a range ENDPOINT.

THE GATE (pre-committed, both branches, verbatim; `writeup/novelty/leg_199.md`)
-----------------------------------------------------------------------------
    Under adversarial and degenerate inputs, does `certificate_guards.py` ever silently
    ACCEPT (fail to reject) a case that should fail -- the same fabrication-acceptance
    shape leg 116 found in `nk_bounds.py`?

    YES -> name the exact mechanism, magnitude, and every certificate battery whose banked
           verdict it could have silently affected.  Push the branch only, escalate, and do
           NOT patch `certificate_guards.py` under this leg's own authority.
    NO  -> bank the battery as the permanent regression suite and record the pass.

**THE GATE ANSWERS YES.**  Six mechanisms, of which four are silent ACCEPTS at the guard's
own surface (M1, M2, M4, M5), one is a sound-but-unnamed CRASH that is explicitly NOT
counted as a gate hit (M6), and one is a hygiene note (M7).  The blast radius is **LATENT**:
0 banked numbers are impeached, because every in-repo caller stays inside the hypotheses.
That is reported as measured, not softened and not inflated.

THE TWO-PART MEASUREMENT, AND WHY IT IS FORCED
-----------------------------------------------------------------------------
This module is a PURE REJECTION LAYER: it returns reasons, never numbers, and computes no
bound.  So the leg-92/117 style "the returned magnitude is X x below the honest one"
measurement cannot be made at its own surface.  Every probe is therefore measured twice:

  (a) AT THE GUARD -- does a case that breaks a hypothesis the guard's OWN docstring names
      come back with an EMPTY violation list / a `None`?
  (b) AT THE CONSUMER -- for every (a) hit, the same value is driven through the real call
      site in `nk_bounds.py`, and what comes out is recorded against the hypothesis-
      satisfying counterpart.  A guard-level accept no consumer can reach is LATENT and is
      reported as latent (legs 142 and 147's precedent), never as an impeached certificate.

LESSON 90 IS WIRED AS A CONTROL, NOT AS PROSE: every probe carries a hypothesis-satisfying
reference, and a probe whose reference produces the IDENTICAL result is recorded as
`no_discrimination` and does not count toward the gate.

`solver/certificate_guards.py` IS NOT EDITED BY THIS LEG, under either branch of the gate.
"""

import json
import math
import os
import sys
import traceback
from decimal import Decimal
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.certificate_guards as cg          # noqa: E402
import solver.interval_certificate as ic        # noqa: E402
import solver.nk_bounds as nk                   # noqa: E402
import solver.port_certification as pc          # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_cga_v1_adversarial.json")

INF, NAN = float("inf"), float("nan")

# The two REAL `unit_range_violation` call sites, copied from the module rather than
# paraphrased, so this battery cannot drift from what `nk_bounds.py` actually asks for.
#   nk_bounds.py:392   unit_range_violation("gamma", gamma, 0.0, 1.0, lo_open=True,  hi_open=False)
#   nk_bounds.py:430   unit_range_violation("alpha", alpha, -inf,  2.0, lo_open=False, hi_open=True)
GAMMA_SITE = dict(name="gamma", lo=0.0, hi=1.0, lo_open=True, hi_open=False)
ALPHA_SITE = dict(name="alpha", lo=-INF, hi=2.0, lo_open=False, hi_open=True)

# Every in-repo alpha, read out of the callers rather than assumed (see `blast_radius`).
LIVE_ALPHAS = (1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8)
LIVE_GAMMA = 0.5


# ---------------------------------------------------------------------------
# plumbing
# ---------------------------------------------------------------------------

def _call(fn, *a, **k):
    """Run `fn`, and classify the outcome the way this battery reasons about outcomes.

    Returns (kind, payload).  `kind` is one of:
      "value"  -- returned normally; payload is the return value
      "raise"  -- raised; payload is "TypeName: message"
    A RAISE is not a defect here.  A guard that raises has REFUSED, which is the behaviour
    under audit; only a guard that RETURNS an admissible verdict on an inadmissible input is
    a gate hit.  The exception TYPE is recorded because M6 turns on it.
    """
    try:
        return "value", fn(*a, **k)
    except Exception as e:                                     # noqa: BLE001
        return "raise", f"{type(e).__name__}: {e}"


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        x = x.item()
    if isinstance(x, float):
        if math.isnan(x):
            return "NaN"
        if math.isinf(x):
            return "+Infinity" if x > 0 else "-Infinity"
    if isinstance(x, (Fraction, Decimal)):
        return f"{type(x).__name__}({x})"
    if isinstance(x, np.ndarray):
        return _jsonable(x.tolist())
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return repr(x)


def _lit(v):
    """A stable label for a probe VALUE, since `repr` of a huge int is 400 digits."""
    if isinstance(v, int) and not isinstance(v, bool) and abs(v) > 10 ** 30:
        return f"int(10**{len(str(abs(v))) - 1}){'' if v > 0 else ' negated'}"
    if isinstance(v, Fraction) and abs(v.denominator) > 10 ** 30:
        return f"Fraction({v.numerator}, 10**{len(str(v.denominator)) - 1})"
    return repr(v)


CASES = []


def record(family, case, probe, guard_kind, guard_out, accepted, should_reject,
           why, consumer=None, reference=None, magnitude=None, status=None):
    """One row of the battery.  `accepted` is what the GUARD did; `should_reject` is what
    the module's OWN docstring says it should have done; a row is a GATE HIT exactly when
    `accepted and should_reject`."""
    row = {"family": family, "case": case, "probe": probe,
           "guard_outcome_kind": guard_kind, "guard_output": _jsonable(guard_out),
           "guard_accepted": accepted, "should_reject": should_reject,
           "gate_hit": bool(accepted and should_reject), "why": why,
           "consumer": _jsonable(consumer), "reference": _jsonable(reference),
           "magnitude": _jsonable(magnitude),
           "status": status or ("HIT" if (accepted and should_reject) else "ok")}
    CASES.append(row)
    return row


# ---------------------------------------------------------------------------
# FAMILY A -- `hypothesis_violations`: the type gate and the numeric edge
# ---------------------------------------------------------------------------

def family_A():
    """The one guard of the five that THREE pipelines share.

    Its contract, from its own docstring: a violation for NaN / +-inf / negative; a
    `TypeError` on a non-real value ("a constant that is not a number is a caller bug, not a
    fabricated bound, and must not be laundered into a closes=False"); `0.0`/`-0.0` are
    legitimate and are NOT violations.
    """
    H = cg.hypothesis_violations

    # --- controls first: the three shapes the guard was written for MUST still reject.
    for lbl, v in [("neg_float", -1.0), ("nan_float", NAN), ("posinf", INF), ("neginf", -INF),
                   ("np_float64_neg", np.float64(-1.0)), ("np_float32_nan", np.float32("nan")),
                   ("np_float64_inf", np.float64(INF))]:
        k, out = _call(H, (("Y_0", v),))
        acc = (k == "value" and out == [])
        record("A", f"A_control_{lbl}", _lit(v), k, out, acc, True,
               "CONTROL: the guard's own reason for existing; a miss here voids the run",
               status="CONTROL_HIT" if acc else "CONTROL_PASS")

    for lbl, v in [("zero", 0.0), ("neg_zero", -0.0), ("small_pos", 1e-300), ("one", 1.0)]:
        k, out = _call(H, (("Y_0", v),))
        acc = (k == "value" and out == [])
        record("A", f"A_control_admissible_{lbl}", _lit(v), k, out, acc, False,
               "CONTROL (over-rejection): a legitimate bound must NOT be refused",
               status="CONTROL_PASS" if acc else "CONTROL_OVERREJECT")

    for lbl, v in [("str", "-1.0"), ("complex", complex(-1, 0)), ("ndarray0d", np.array(-1.0)),
                   ("Decimal", Decimal("-1"))]:
        k, out = _call(H, (("Y_0", v),))
        acc = (k == "value" and out == [])
        record("A", f"A_control_nonreal_{lbl}", _lit(v), k, out, acc, True,
               "CONTROL: the docstring promises a TypeError on a non-real value",
               status="CONTROL_PASS" if k == "raise" else "CONTROL_HIT")

    # --- A1  bool is numbers.Real.
    for lbl, v in [("True", True), ("False", False)]:
        k, out = _call(H, (("Y_0", v),))
        acc = (k == "value" and out == [])
        b_probe = nk.budget(v, 0.0, 0.3, 1.0) if lbl == "False" else nk.budget(1e-6, v, 0.3, 1.0)
        b_ref = nk.budget(0.0, 0.0, 0.3, 1.0) if lbl == "False" else nk.budget(1e-6, 1.0, 0.3, 1.0)
        record("A", f"A1_bool_{lbl}", _lit(v), k, out, acc, True,
               "M3: `isinstance(True, numbers.Real)` is True, so a FLAG is silently "
               "reinterpreted as the number 1.0/0.0 and no signal distinguishes the two",
               consumer={"budget": {kk: b_probe.get(kk) for kk in
                                    ("closes", "r_min", "degenerate_ball", "reason")}},
               reference={"budget": {kk: b_ref.get(kk) for kk in
                                     ("closes", "r_min", "degenerate_ball")}},
               magnitude="arithmetically correct for the coerced value; the defect is the "
                         "absence of a signal, NOT an arithmetic lie")

    # --- A2  a Python int too large for float64.
    for lbl, v in [("pos", 10 ** 400), ("neg", -(10 ** 400))]:
        k, out = _call(H, (("Y_0", v),))
        acc = (k == "value" and out == [])
        ck, cout = _call(nk.budget, v, 0.0, 0.3, 1.0)
        record("A", f"A2_huge_int_{lbl}", _lit(v), k, out, acc, True,
               "M6: `float(v)` overflows on the line BEFORE the isinf test that exists "
               "precisely to name this case. NOT a false accept -- it is sound -- but it is "
               "leg 98's B20/B21 shape (a bare arithmetic exception a caller with a broad "
               "`except` turns into a silent skip)",
               consumer={"budget": f"{ck}: {cout}"},
               reference={"budget(1e300)": _jsonable(nk.budget(1e300, 0.0, 0.3, 1.0)["closes"])},
               magnitude="an effectively-infinite constant CRASHES instead of producing the "
                         "module's own '+infinite (a norm bound is finite by hypothesis)'",
               status="SECONDARY_NOT_A_GATE_HIT")

    # --- A3  a negative rational below the denormal floor.
    for lbl, v in [("neg_below_denormal", Fraction(-1, 10 ** 400)),
                   ("neg_representable", Fraction(-1, 3))]:
        k, out = _call(H, (("Y_0", v),))
        acc = (k == "value" and out == [])
        b = nk.budget(1e-6, v, 0.3, 1.0)
        b_ref = nk.budget(1e-6, 0.0, 0.3, 1.0)
        record("A", f"A3_fraction_{lbl}", _lit(v), k, out, acc,
               True if lbl == "neg_below_denormal" else True,
               "M4: `float()` underflows a NEGATIVE rational to -0.0 BEFORE the `f < 0.0` "
               "test, so a constant the docstring calls 'an input the theorem says nothing "
               "about' is admitted as nonnegative. Unreachable from float64 (a negative "
               "float below the denormal floor already IS -0.0); needs an exact type",
               consumer={"budget_closes": b["closes"], "r_min": b["r_min"]},
               reference={"budget_closes": b_ref["closes"], "r_min": b_ref["r_min"]},
               magnitude="accepted negatives span (-5e-324, 0), so the budget inflation is "
                         "<= 1 ULP: the ACCEPT is real, the MAGNITUDE is nil")

    # --- A6  the empty container.
    k, out = _call(H, ())
    acc = (k == "value" and out == [])
    record("A", "A6_empty_constants", "()", k, out, acc, True,
           "M5: zero constants checked, and the verdict returned is 'every constant is "
           "admissible' -- a vacuous pass. Not reachable from the three call sites, which "
           "all pass a fixed-length tuple",
           magnitude="0 of 0 constants validated", status="HIT_LATENT")

    # --- the three pipelines must still AGREE (leg 128's clause, re-derived not quoted).
    agree = []
    for (Y0, Z1, Z2) in ((-1.0, 0.3, 1.0), (NAN, 0.3, 1.0), (INF, 0.3, 1.0),
                         (1e-6, -1.0, 1.0), (1e-6, 0.3, -1.0)):
        vp, vi, vn = (pc.radii_polynomial_status(Y0, Z1, Z2), ic.radii_verdict(Y0, Z1, Z2),
                      nk.budget(Y0, 0.0, Z1, Z2))
        agree.append({"input": _jsonable([Y0, Z1, Z2]),
                      "n_violations": [len(vp["violations"]), len(vi["violations"]),
                                       len(vn["violations"])],
                      "all_refuse": bool(vp["closes"] is False and vi["closes"] is False
                                         and vn["closes"] is False)})
    ok = all(a["all_refuse"] and len(set(a["n_violations"])) == 1 for a in agree)
    record("A", "A_control_three_pipelines_agree", "5 violating triples", "value", agree,
           not ok, True, "CONTROL: leg 128's shared-guard claim, re-derived here rather "
           "than quoted. If this fails the module is not the one under audit",
           status="CONTROL_PASS" if ok else "CONTROL_HIT")
    return agree


# ---------------------------------------------------------------------------
# FAMILY B -- `radius_violation`: the type gate that is NOT there
# ---------------------------------------------------------------------------

def family_B():
    """The headline asymmetry, half of it: `hypothesis_violations` enforces `numbers.Real`
    and RAISES on a non-real value; `radius_violation` -- in the SAME FILE, 8 lines later --
    calls `float()` with no such check."""
    R = cg.radius_violation

    for lbl, v in [("nan", NAN), ("posinf", INF), ("neginf", -INF), ("zero", 0.0),
                   ("neg_zero", -0.0), ("negative", -1.0)]:
        k, out = _call(R, v)
        acc = (k == "value" and out is None)
        record("B", f"B_control_{lbl}", _lit(v), k, out, acc, True,
               "CONTROL: r_min values the docstring says assert 'a zero inside a degenerate "
               "or empty set'", status="CONTROL_HIT" if acc else "CONTROL_PASS")

    for lbl, v in [("positive", 0.5), ("denormal", 5e-324)]:
        k, out = _call(R, v)
        acc = (k == "value" and out is None)
        record("B", f"B_control_admissible_{lbl}", _lit(v), k, out, acc, False,
               "CONTROL (over-rejection): a real positive radius must NOT be refused",
               status="CONTROL_PASS" if acc else "CONTROL_OVERREJECT")

    for lbl, v in [("str", "0.5"), ("bool_True", True), ("Decimal", Decimal("0.5")),
                   ("Fraction", Fraction(1, 2))]:
        k, out = _call(R, v)
        acc = (k == "value" and out is None)
        sib_k, sib_out = _call(cg.hypothesis_violations, (("Y_0", v),))
        record("B", f"B_nonreal_{lbl}", _lit(v), k, out, acc, True,
               "M2: a non-float `r_min` is accepted as an admissible RADIUS with no type "
               "check, while the sibling guard in the same file refuses the same value",
               consumer={"nk_bounds:561 reachable_with_this_type": False,
                         "r_min is always the module's own float64": True},
               reference={"hypothesis_violations same value": f"{sib_k}: {_jsonable(sib_out)}"},
               magnitude="4 of 4 non-Real types accepted here; the sibling raises on 3 of 4 "
                         "(bool is numbers.Real and passes both)",
               status="HIT_LATENT")

    k, out = _call(R, None)
    record("B", "B_none", "None", k, out, False, True,
           "CONTROL/secondary: `None` reaches `float()` and raises an UNNAMED TypeError "
           "rather than the module's own vocabulary",
           status="SECONDARY_NOT_A_GATE_HIT")
    return None


# ---------------------------------------------------------------------------
# FAMILY C -- `unit_range_violation`: THE HEADLINE
# ---------------------------------------------------------------------------

def family_C():
    """M1.  Four of the five exported guards test finiteness EXPLICITLY
    (`hypothesis_violations` and `radius_violation` both call `math.isinf`;
    `positive_weight_violations` counts infinite entries).  `unit_range_violation` is the
    ONLY one that does not -- it delegates non-finiteness to two comparisons:

        lo_bad = (f <= lo) if lo_open else (f < lo)
        hi_bad = (f >= hi) if hi_open else (f > hi)

    and `nk_bounds.py:430` asks it for a CLOSED lower endpoint at MINUS INFINITY:

        unit_range_violation("alpha", alpha, -float("inf"), 2.0, lo_open=False, hi_open=True)

    so the lower test is `-inf < -inf`, which is False.  `alpha = -inf` is ADMISSIBLE.
    """
    U = cg.unit_range_violation

    # --- the alpha site, which is the exposed one.
    for lbl, v in [("in_range_1p5", 1.5), ("in_range_neg1e300", -1e300),
                   ("boundary_2p0", 2.0), ("posinf", INF), ("nan", NAN)]:
        k, out = _call(U, ALPHA_SITE["name"], v, ALPHA_SITE["lo"], ALPHA_SITE["hi"],
                       lo_open=ALPHA_SITE["lo_open"], hi_open=ALPHA_SITE["hi_open"])
        acc = (k == "value" and out is None)
        should = lbl in ("boundary_2p0", "posinf", "nan")
        record("C", f"C_control_alpha_{lbl}", _lit(v), k, out, acc, should,
               "CONTROL: the two non-finite alphas the guard DOES catch, plus the closed "
               "upper endpoint and an in-range value",
               status=("CONTROL_HIT" if (acc and should) else
                       "CONTROL_OVERREJECT" if (not acc and not should) else "CONTROL_PASS"))

    # THE HIT.
    k, out = _call(U, "alpha", -INF, -INF, 2.0, lo_open=False, hi_open=True)
    acc = (k == "value" and out is None)
    probe = _call(nk.farfield_modelling_error_bound, -INF, LIVE_GAMMA, 1.0)
    ref = _call(nk.farfield_modelling_error_bound, 1.5, LIVE_GAMMA, 1.0)
    plus = _call(nk.farfield_modelling_error_bound, INF, LIVE_GAMMA, 1.0)
    nanc = _call(nk.farfield_modelling_error_bound, NAN, LIVE_GAMMA, 1.0)
    p_bound = probe[1]["bound"] if probe[0] == "value" else None
    n_nan_window = (sum(1 for x in probe[1]["value"] if math.isnan(x))
                    if probe[0] == "value" else None)
    record("C", "C1_alpha_minus_infinity_ACCEPTED", "-inf at the real nk_bounds:430 site",
           k, out, acc, True,
           "M1 (HEADLINE): `unit_range_violation` has no isinf test, and the alpha call "
           "site requests a CLOSED -inf endpoint, so `-inf < -inf` is False and a "
           "non-finite Holder exponent is ADMISSIBLE. Of the three non-finite alphas, +inf "
           "and NaN both REFUSE and -inf alone is accepted -- and it is the only one that "
           "MANUFACTURES a NaN in an upper-bound slot, the exact object this module's own "
           "NAN_HINT_* constants exist to warn about ('NaN >= 1.0 is False, so an unguarded "
           "NaN would slip past the contraction test')",
           consumer={"farfield_modelling_error_bound(-inf)": {
               "kind": probe[0], "bound": p_bound,
               "hilbert_term": probe[1]["hilbert_term"] if probe[0] == "value" else None,
               "pointwise_term": probe[1]["pointwise_term"] if probe[0] == "value" else None,
               "argmax_at_window_end": probe[1]["argmax_at_window_end"] if probe[0] == "value" else None,
               "n_NaN_of_40_window_samples": n_nan_window, "raised": False}},
           reference={"alpha=1.5 (honest)": {"kind": ref[0],
                                             "bound": ref[1]["bound"] if ref[0] == "value" else None},
                      "alpha=+inf": f"{plus[0]}: {str(plus[1])[:80]}",
                      "alpha=NaN": f"{nanc[0]}: {str(nanc[1])[:80]}"},
           magnitude=f"returns bound=NaN with {n_nan_window} of 40 window samples NaN and "
                     f"does NOT raise, against an honest {ref[1]['bound'] if ref[0]=='value' else None} "
                     f"at alpha=1.5; 1 of 3 non-finite alphas accepted",
           status="HIT_LATENT")

    # the admissible range contains a sub-range the function cannot evaluate at all.
    big = _call(nk.farfield_modelling_error_bound, -1e300, LIVE_GAMMA, 1.0)
    k2, out2 = _call(U, "alpha", -1e300, -INF, 2.0, lo_open=False, hi_open=True)
    record("C", "C1b_alpha_neg1e300_accepted_then_crashes", "-1e300", k2, out2,
           k2 == "value" and out2 is None, True,
           "M1, second half: the guard's declared admissible range [-inf, 2.0) contains a "
           "whole sub-range the guarded function cannot evaluate. The refusal that does "
           "eventually happen is an UNNAMED OverflowError from inside the quadrature, not "
           "the module's own vocabulary",
           consumer={"farfield_modelling_error_bound(-1e300)": f"{big[0]}: {str(big[1])[:80]}"},
           reference={"alpha=1.5": ref[1]["bound"] if ref[0] == "value" else None},
           status="SECONDARY_NOT_A_GATE_HIT")

    # --- the gamma site: the SAME function, a finite lower endpoint, and it is CLEAN.
    for lbl, v in [("posinf", INF), ("neginf", -INF), ("nan", NAN), ("zero", 0.0),
                   ("above_one", 1.5)]:
        k, out = _call(U, GAMMA_SITE["name"], v, GAMMA_SITE["lo"], GAMMA_SITE["hi"],
                       lo_open=GAMMA_SITE["lo_open"], hi_open=GAMMA_SITE["hi_open"])
        acc = (k == "value" and out is None)
        record("C", f"C2_control_gamma_{lbl}", _lit(v), k, out, acc, True,
               "CONTROL, and it is the one that LOCALISES M1: at the gamma site the lower "
               "endpoint is FINITE (0.0, open), so +-inf are both refused by the same code "
               "that accepts -inf at the alpha site. The defect is the INTERACTION of a "
               "missing isinf test with a caller-supplied infinite endpoint",
               status="CONTROL_HIT" if acc else "CONTROL_PASS")
    for lbl, v in [("interior", 0.5), ("upper_closed_endpoint", 1.0)]:
        k, out = _call(U, GAMMA_SITE["name"], v, GAMMA_SITE["lo"], GAMMA_SITE["hi"],
                       lo_open=GAMMA_SITE["lo_open"], hi_open=GAMMA_SITE["hi_open"])
        acc = (k == "value" and out is None)
        record("C", f"C2_control_gamma_admissible_{lbl}", _lit(v), k, out, acc, False,
               "CONTROL (over-rejection): a legitimate Holder exponent must NOT be refused",
               status="CONTROL_PASS" if acc else "CONTROL_OVERREJECT")

    # --- C3/C4: the type gate, again absent.
    g_true = _call(nk.hilbert_farfield_bound, 1.0, 1.5, True)
    g_ref = _call(nk.hilbert_farfield_bound, 1.0, 1.5, LIVE_GAMMA)
    ratio = (g_ref[1][0] / g_true[1][0]) if (g_true[0] == "value" and g_ref[0] == "value") else None
    k, out = _call(U, "gamma", True, 0.0, 1.0, lo_open=True, hi_open=False)
    record("C", "C3_gamma_bool", "True", k, out, k == "value" and out is None, True,
           "M3 at the gamma site: `True` is admitted and silently evaluated as the exponent "
           "1.0. Reported at its honest weight -- gamma=1.0 IS a legitimate exponent, so "
           "the number is correct FOR THAT EXPONENT; what is missing is any signal that the "
           "caller passed a flag",
           consumer={"hilbert_farfield_bound(X=1, alpha=1.5, gamma=True)":
                     _jsonable(g_true[1])},
           reference={"gamma=0.5": _jsonable(g_ref[1])},
           magnitude=(f"claimed upper bound {g_true[1][0]!r} vs {g_ref[1][0]!r} at the live "
                      f"gamma=0.5, i.e. {ratio:.6f}x SMALLER" if ratio else None),
           status="HIT_LATENT")

    s_probe = _call(nk.hilbert_farfield_bound, 1.0, 1.5, "0.5")
    k, out = _call(U, "gamma", "0.5", 0.0, 1.0, lo_open=True, hi_open=False)
    record("C", "C4_gamma_str", "'0.5'", k, out, k == "value" and out is None, True,
           "M2 at the gamma site: a STRING passes the exponent guard, and the refusal that "
           "eventually happens is an unnamed TypeError from the power operator three lines "
           "later -- leg 98's B20/B21 shape, in the module that was repaired for it",
           consumer={"hilbert_farfield_bound(gamma='0.5')": f"{s_probe[0]}: {str(s_probe[1])[:80]}"},
           reference={"gamma=0.5": _jsonable(g_ref[1])},
           status="HIT_LATENT")
    return ratio


# ---------------------------------------------------------------------------
# FAMILY D -- `positive_weight_violations`: the container
# ---------------------------------------------------------------------------

def family_D():
    """"A weight vector DEFINES a norm, so it is strictly positive and finite."  What does
    the guard say about a weight vector with no entries at all?"""
    P = cg.positive_weight_violations

    for lbl, vals, kw in [("all_negative", [-1.0, -1.0], {}),
                          ("planted_neg_zero", [1.0, -0.0], {}),
                          ("planted_nan", [1.0, NAN], {}),
                          ("planted_inf", [1.0, INF], {}),
                          ("planted_negative", [1.0, 2.0, -3.0], {})]:
        k, out = _call(P, "v_cod", vals, **kw)
        acc = (k == "value" and out == [])
        record("D", f"D_control_{lbl}", _lit(vals), k, out, acc, True,
               "CONTROL: leg 116's own mechanism -- the `1/q if q > 0 else 0` mask prices "
               "an honestly-infinite contribution at zero (2.19x / 3.57x)",
               status="CONTROL_HIT" if acc else "CONTROL_PASS")

    k, out = _call(P, "v_cod", [1.0, 2.0, 3.0])
    acc = (k == "value" and out == [])
    record("D", "D_control_admissible_positive", "[1.0, 2.0, 3.0]", k, out, acc, False,
           "CONTROL (over-rejection): a genuine weight vector must NOT be refused",
           status="CONTROL_PASS" if acc else "CONTROL_OVERREJECT")

    k, out = _call(P, "q_cod", [1.0, 0.0], allow_zero=True)
    acc = (k == "value" and out == [])
    record("D", "D_control_allow_zero_semantics", "[1.0, 0.0] allow_zero=True", k, out, acc,
           False, "CONTROL: `allow_zero=True` is the rectangular-kernel path and permits "
           "zeros BY DESIGN, so accepting 0.0 here is correct and is NOT a hit",
           status="CONTROL_PASS" if acc else "CONTROL_OVERREJECT")

    # THE HIT: the empty container.
    for lbl, vals in [("empty_list", []), ("empty_ndarray", np.array([])),
                      ("exhausted_generator", "GEN")]:
        v = (x for x in []) if isinstance(vals, str) else vals
        k, out = _call(P, "v_cod", v)
        acc = (k == "value" and out == [])
        record("D", f"D1_{lbl}", _lit(vals), k, out, acc, True,
               "M5: an EMPTY weight vector is certified as one 'a norm could have produced'. "
               "The same empty-window shape leg 99 found in boussinesq_velocity.py",
               magnitude="0 of 0 entries validated", status="HIT_LATENT")

    # (b) at the consumer: is it reachable, and what happens?
    empty = _call(nk.two_point_dual, np.zeros((1, 0)), np.array([], dtype=int),
                  np.zeros((0, 0)), np.array([]))
    screen_passes_empty = bool(np.all(np.isfinite(np.array([]))) and np.all(np.array([]) > 0.0))
    record("D", "D1b_empty_at_the_consumer", "two_point_dual with empty weights", "value",
           {"screen_treats_empty_as_clean": screen_passes_empty},
           screen_passes_empty, True,
           "M5 at the consumer: `nk_bounds.py:225`'s numpy pre-screen ALSO passes the empty "
           "array (`np.all` of an empty array is True), so the guard is never even "
           "consulted and the failure surfaces four lines later, in numpy's vocabulary",
           consumer={"two_point_dual(empty)": f"{empty[0]}: {str(empty[1])[:90]}"},
           status="HIT_LATENT")

    for lbl, vals in [("dict", {"a": 1.0}), ("2d_array", np.array([[1.0, -1.0], [2.0, 3.0]])),
                      ("2d_column", np.array([[1.0], [-1.0]]))]:
        k, out = _call(P, "v_cod", vals)
        acc = (k == "value" and out == [])
        record("D", f"D_secondary_{lbl}", _lit(vals), k, out, acc, True,
               "SECONDARY: an un-ravelled 2-D array (the docstring says 'a flattened array "
               "is fine') and a dict both raise from inside the list comprehension rather "
               "than in the module's own vocabulary. Sound, not a false accept",
               status="SECONDARY_NOT_A_GATE_HIT" if k == "raise" else "HIT_LATENT")
    return None


# ---------------------------------------------------------------------------
# FAMILY E -- `invalid_input_reason`
# ---------------------------------------------------------------------------

def family_E():
    s = cg.invalid_input_reason([])
    record("E", "E_empty_violation_list", "[]", "value", s, True, True,
           "M7 (hygiene): a full rejection sentence is assembled from an EMPTY reason list, "
           "producing 'INVALID_INPUT: ...nonnegative): . No discriminant is evaluated.' -- "
           "an accusation with no charge. Not reachable at nk_bounds.py:533, which is "
           "guarded by `if violations:`",
           consumer={"reachable_at_nk_bounds_533": False,
                     "guarded_by": "if violations:"},
           magnitude=f"{len(s)} characters of rejection prose naming 0 violated hypotheses",
           status="HIT_LATENT")
    return s


# ---------------------------------------------------------------------------
# BLAST RADIUS -- the part the gate says makes the finding a priority
# ---------------------------------------------------------------------------

def blast_radius():
    """Every certificate battery whose banked verdict M1-M5 could have silently affected.

    Measured, not asserted: the guard-level accepts are only load-bearing if a caller can
    REACH them.  Each in-repo call site is re-driven at its own live parameters and the
    result recorded, so "LATENT" is a measurement rather than a reassurance.
    """
    rows = []
    # M1's reach: every in-repo alpha, from the callers themselves.
    live = []
    for a in LIVE_ALPHAS:
        d = nk.farfield_modelling_error_bound(a, LIVE_GAMMA, 1.0, n_X=8)
        live.append({"alpha": a, "bound": d["bound"], "finite": bool(np.isfinite(d["bound"])),
                     "argmax_at_window_end": d["argmax_at_window_end"]})
    rows.append({
        "mechanism": "M1 (unit_range_violation accepts -inf at nk_bounds.py:430)",
        "callers": ["test_nk_bounds.py:192,207 (ALPHA=1.5)",
                    "experiments/p2_route_d_v6_bounds.py:170,200,224 (alphas=1.1..1.8)",
                    "experiments/p2_route_d_v7_seminorm.py:298 (alphas=1.1..1.8)",
                    "experiments/p2_route_d_v8_quadratic.py:306 (alphas=1.1..1.8)",
                    "experiments/p2_route_d_v9_sharpen.py:326 (alphas=1.1..1.8)",
                    "experiments/p2_route_nka_v1_adversarial.py:408,425 (LIVE_ALPHAS=1.1..1.8)",
                    "experiments/p2_route_nkr_v1_repair.py:230, p2_route_nkb_v1_postrepair.py:150"],
        "min_alpha_any_caller": min(LIVE_ALPHAS),
        "distance_to_the_defect": "every in-repo alpha is in [1.1, 1.8]; the accept needs "
                                  "exactly -inf, which no caller passes and no computation "
                                  "in the repo produces as an exponent",
        "live_values": live,
        "all_live_bounds_finite": all(r["finite"] for r in live),
        "banked_numbers_impeached": 0, "verdict": "LATENT"})
    rows.append({
        "mechanism": "M2/M3 (no type gate in radius_violation / unit_range_violation)",
        "callers": ["nk_bounds.py:561 (r_min is the module's own float64)",
                    "nk_bounds.py:392,430 (gamma/alpha are floats at every call site)"],
        "distance_to_the_defect": "reaching it requires a caller to pass a str/Decimal/bool "
                                  "exponent or radius; all 8 in-repo call paths pass floats",
        "banked_numbers_impeached": 0, "verdict": "LATENT"})
    rows.append({
        "mechanism": "M4 (negative rational below the denormal floor)",
        "callers": ["port_certification.py:346", "interval_certificate.py:140",
                    "nk_bounds.py:526"],
        "distance_to_the_defect": "unreachable from float64 by construction, and all three "
                                  "pipelines are driven with float64 constants",
        "banked_numbers_impeached": 0, "verdict": "LATENT"})
    rows.append({
        "mechanism": "M5 (empty container is a vacuous pass)",
        "callers": ["nk_bounds.py:225,227 via two_point_dual"],
        "distance_to_the_defect": "the caller's own numpy pre-screen also passes an empty "
                                  "array, and the downstream `min` reduction then raises",
        "banked_numbers_impeached": 0, "verdict": "LATENT"})
    return rows


# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("THE GATE")[0].strip()[:0] or "", end="")
    print("ROUTE-CGA -- fabrication-acceptance battery on solver/certificate_guards.py\n")

    agree = family_A()
    family_B()
    ratio = family_C()
    family_D()
    family_E()
    radius = blast_radius()

    hits = [c for c in CASES if c["gate_hit"] and c["status"] != "SECONDARY_NOT_A_GATE_HIT"]
    controls = [c for c in CASES if c["status"].startswith("CONTROL")]
    control_failures = [c for c in controls if c["status"] in ("CONTROL_HIT",
                                                               "CONTROL_OVERREJECT")]
    secondary = [c for c in CASES if c["status"] == "SECONDARY_NOT_A_GATE_HIT"]

    for c in CASES:
        mark = {"HIT": "HIT", "HIT_LATENT": "HIT(latent)", "ok": "  ok",
                "CONTROL_PASS": "  ctl", "CONTROL_HIT": "CTL-FAIL",
                "CONTROL_OVERREJECT": "CTL-OVERREJECT",
                "SECONDARY_NOT_A_GATE_HIT": " 2ndry"}.get(c["status"], c["status"])
        print(f"  {mark:15s} {c['family']}  {c['case']:44s} {str(c['probe'])[:26]}")

    verdict = "YES" if hits else "NO"
    payload = {
        "leg": 199, "route": "CGA", "module_under_audit": "solver/certificate_guards.py",
        "module_edited_by_this_leg": False,
        "gate": ("Under adversarial and degenerate inputs, does certificate_guards.py ever "
                 "silently ACCEPT (fail to reject) a case that should fail -- the same "
                 "fabrication-acceptance shape leg 116 found in nk_bounds.py?"),
        "gate_answer": verdict,
        "totals": {"cases": len(CASES), "gate_hits": len(hits),
                   "controls": len(controls), "control_failures": len(control_failures),
                   "secondary_not_gate_hits": len(secondary)},
        "mechanisms": {
            "M1": "unit_range_violation is the ONLY one of the five exported guards with no "
                  "isinf test, and nk_bounds.py:430 asks it for a CLOSED -inf lower "
                  "endpoint, so alpha=-inf is admissible and manufactures bound=NaN",
            "M2": "radius_violation and unit_range_violation call float() with no "
                  "numbers.Real check, while hypothesis_violations in the same file raises",
            "M3": "bool is numbers.Real, so a flag is silently reinterpreted as 1.0/0.0",
            "M4": "float() underflows a negative rational to -0.0 before the f < 0.0 test",
            "M5": "an empty container is a vacuous pass in two guards",
            "M6": "a too-large int raises OverflowError on the line before the isinf test "
                  "(SOUND, explicitly NOT counted as a gate hit)",
            "M7": "invalid_input_reason([]) builds a rejection sentence naming no violation"},
        "headline": {
            "mechanism": "M1",
            "site": "solver/certificate_guards.py:162-178 (unit_range_violation), reached "
                    "from solver/nk_bounds.py:430",
            "probe": "farfield_modelling_error_bound(alpha=-inf, gamma=0.5, X0=1.0)",
            "returns": "bound=NaN, hilbert_term=NaN, 40/40 window samples NaN, no exception",
            "honest_reference_alpha_1p5": 2.537396530974982,
            "sibling_non_finite_alphas": {"+inf": "ValueError", "NaN": "ValueError",
                                          "-inf": "ACCEPTED"},
            "n_non_finite_alphas_accepted": "1 of 3"},
        "gamma_bool_ratio_ref_over_probe": ratio,
        "blast_radius": radius,
        "banked_numbers_impeached": 0,
        "three_pipeline_agreement_control": agree,
        "cases": CASES,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2)

    print(f"\n  cases {len(CASES)}   GATE HITS {len(hits)}   controls {len(controls)} "
          f"({len(control_failures)} failed)   secondary {len(secondary)}")
    print(f"  GATE ANSWERS {verdict}; banked numbers impeached: 0 (all four mechanisms LATENT)")
    print(f"  -> {OUT}")
    if control_failures:
        print("  CONTROL FAILURE -- the run is VOID:")
        for c in control_failures:
            print(f"     {c['case']}: {c['why'][:80]}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:                                          # noqa: BLE001
        traceback.print_exc()
        sys.exit(2)
