"""Leg 105 (Route-ICB) -- PERMANENT REGRESSION SUITE for solver/interval_certificate.py.

WHAT THIS IS, AND WHY IT IS NOT test_interval_certificate_adversarial.py
-----------------------------------------------------------------------------
Leg 98 (Route-ICA) measured a fabrication-acceptance gap in `interval_constants` /
`radii_verdict`: 12 of 36 hypothesis-violating inputs closed, 8 load-bearing. The bench-repair
`bench/fix-interval-certificate-validation` closed it, and in the SAME COMMIT rewrote
`test_interval_certificate_adversarial.py` to invert leg 98's seven GAP-PIN gates and to gate
the battery total. That file is a legitimate regression pin, but it is the repair grading its
own homework, and it says nothing about whether leg 61's separate Kawahara known-answer gate
survived. This file is this leg's INDEPENDENT check, mirroring the role leg 87 played for the
sibling arithmetic primitive (`solver/interval.py`, leg 69's repair) and leg 103 played for
`solver/gclm.py` (leg 92's repair):

  GATE (a). Re-derive leg 98's 12/36 -> 0/36 count from a source outside the repair's own
  territory -- bound to the pre-repair module read straight out of git, as a negative control,
  and separately to the current module.

  GATE (b). A BITWISE, SAME-PROCESS pre/post differential of `kawahara_certificate()`'s output
  -- the strongest available "zero regression" statement, and one that deliberately does NOT
  rely on matching the banked `writeup/data/p2_route_ka_v1_kawahara.json` (see
  `writeup/novelty/leg_105.md` sec 3: that JSON is not bit-reproducible even from the literal
  leg-61-original source in this environment, because `Y_0 ~ 3e-17` sits at the float64 noise
  floor of a fully-converged Newton iterate -- an environment sensitivity that predates both
  repairs and is not a regression signal).

MEASURED, NOT ASSERTED (leg 105, against the pre-repair module read out of git):
  - the pre-repair module, run through leg 98's OWN battery, reproduces 12/36 false accepts
    (8 load-bearing) EXACTLY -- the negative control that makes the post-repair 0/36 trustworthy
  - the post-repair module gives 0/36 false accepts, independently of the repair's own test
  - every returned field of kawahara_certificate() (Y_0, Z_1, Z_2, budget, r_min, r_max,
    Y0_over_budget, every conversion factor, the full Newton history, the converged
    coefficient vector) is BIT-IDENTICAL between the pre-repair and post-repair module
  - leg 61's own known-answer gate (test_interval_certificate.py gate 16) still passes on the
    current module: CLN's published r0 is a certified radius, the certificate reaches CLN's
    uniqueness ball, and r_min sits 0.53 decades below r0 -- the same figure that test's own
    docstring records as banked

Companion runner: experiments/p2_route_icb_v1_postrepair.py
Companion data:   writeup/data/p2_route_icb_v1_postrepair.json
Leg 98's frozen pre-repair evidence (untouched here): writeup/data/p2_route_ica_v1_adversarial.json
Leg 61's frozen Kawahara evidence (untouched here): writeup/data/p2_route_ka_v1_kawahara.json

`solver/interval_certificate.py` is READ-ONLY to this leg, under either branch of its gate.

Run: PYTHONPATH=. .venv/bin/python test_interval_certificate_postrepair.py   (~70 s)
"""

import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import solver.interval_certificate as post_mod
from experiments.p2_route_icb_v1_postrepair import (kawahara_bitwise_diff,
                                                     known_answer_gate_check,
                                                     load_prerepair_module,
                                                     run_battery_against)

# Leg 98's own frozen headline, quoted rather than restated -- if this ever needs to change
# the finding itself changed, and this file and leg 98's JSON must change together.
LEG98_PRE_FIX = {"cases": 39, "hypothesis_violating": 36, "false_accepts": 12,
                 "false_accepts_load_bearing": 8, "rejected": 20, "raised": 4}
BANKED_POST_FIX = {"cases": 39, "hypothesis_violating": 36, "false_accepts": 0,
                   "false_accepts_load_bearing": 0, "rejected": 29, "raised": 7}

_CACHE = {}


def _prerepair():
    if "pre" not in _CACHE:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            mod, src, meta = load_prerepair_module()
        _CACHE["pre"] = (mod, src, meta)
    return _CACHE["pre"]


# --------------------------------------------------------------------------
# Part A -- the battery, independently re-derived
# --------------------------------------------------------------------------
def test_prerepair_module_still_has_the_defect_negative_control():
    """The pre-repair module, run through leg 98's OWN unmodified case logic, must reproduce
    leg 98's EXACT numbers. If this ever fails, the differential harness itself is broken --
    not the repair -- and gate (a)'s 0/36 below would be meaningless."""
    pre_mod, _src, _meta = _prerepair()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = run_battery_against(pre_mod)
    t = data["totals"]
    for k, want in LEG98_PRE_FIX.items():
        assert t[k] == want, (f"pre-repair battery total {k} = {t[k]}, expected {want} -- "
                              f"the negative control failed, the harness cannot be trusted")
    assert sorted(data["false_accept_cases"]) == sorted([
        "A1_F_fabricated_zero", "A6_F_shrunk_1e-8_non_containing", "A11_weight_all_negative",
        "A12_weight_one_negative", "B04_Y0_negative_unit", "B05_Y0_negative_tiny",
        "B06_Y0_negative_huge", "B07_Z1_negative", "B08_Z1_negative_rescues_big_Y0",
        "B17_Y0_neg_inf", "B22_Y0_negative_Z1_negative", "B25_Y0_negative_Z1_just_below_one"])
    print(f"[ok] NEGATIVE CONTROL: pre-repair module reproduces leg 98's 12/36 false accepts "
          f"(8 load-bearing) exactly, by name")


def test_postrepair_battery_rejects_every_case_gate_a():
    """GATE (a). The current module, run through the SAME unmodified battery logic
    (`experiments/p2_route_ica_v1_adversarial.py`, imported not copied), independently of the
    repair's own `test_interval_certificate_adversarial.py`, gives 0/36 false accepts."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = run_battery_against(post_mod)
    t = data["totals"]
    for k, want in BANKED_POST_FIX.items():
        assert t[k] == want, (f"post-repair battery total {k} = {t[k]}, expected {want}. "
                              f"The repair regressed or the finding changed -- do not weaken "
                              f"this assertion, escalate instead.")
    assert data["false_accept_cases"] == [] and data["load_bearing_cases"] == []
    assert data["substrate"]["honest_at_z_closes"] is True
    assert data["substrate"]["honest_at_z_bad_closes"] is False
    print(f"[ok] GATE (a): independently re-derived 0/36 false accepts over "
          f"{t['hypothesis_violating']} hypothesis-violating inputs (was 12/36, 8 "
          f"load-bearing, per the negative control above)")


# --------------------------------------------------------------------------
# Part B -- Kawahara, bitwise, same process -- GATE (b)
# --------------------------------------------------------------------------
def test_kawahara_bitwise_zero_regression_gate_b():
    """GATE (b), the strong form. `kawahara_certificate()` run from the pre-repair and
    post-repair module IN THE SAME PROCESS must return bit-identical Y_0, Z_1, Z_2, budget,
    r_min, r_max, Y0_over_budget, every conversion factor, the full Newton history, and the
    converged coefficient vector. Deliberately NOT compared against the banked
    writeup/data/p2_route_ka_v1_kawahara.json -- see the module docstring and
    writeup/novelty/leg_105.md sec 3 for why that comparison is the wrong test."""
    pre_mod, _src, meta = _prerepair()
    assert not meta["interval_py_changed_since_prerepair_rev"], (
        "solver/interval.py changed between the pre-repair baseline and HEAD -- the "
        "differential would no longer isolate solver/interval_certificate.py's repair alone")
    kdiff = kawahara_bitwise_diff(pre_mod, post_mod)
    for row in kdiff["rows"]:
        assert row["bit_identical"], (
            f"Kawahara field {row['field']} moved across the repair: "
            f"pre={row['pre']!r} post={row['post']!r}")
    assert kdiff["all_bit_identical"] and kdiff["n_fields"] >= 20
    print(f"[ok] GATE (b): {kdiff['n_bit_identical']}/{kdiff['n_fields']} Kawahara fields "
          f"bit-identical pre- vs post-repair (same process, same environment) -- Y_0 = "
          f"{kdiff['post_full']['constants']['Y0']:.6e}, closes="
          f"{kdiff['post_full']['verdict']['closes']}")


def test_prerepair_kawahara_certificate_still_closes():
    """Sanity companion to the differential above: the pre-repair module's own Kawahara
    certificate must independently CLOSE (not just happen to match a broken post-repair
    number) -- otherwise 'bit-identical' would be vacuously comparing two failures."""
    pre_mod, _src, _meta = _prerepair()
    run = pre_mod.kawahara_certificate()
    assert run["verdict"]["closes"], f"pre-repair Kawahara certificate does not close: {run}"
    assert run["constants"]["Z1"] < 1.0
    print(f"[ok] pre-repair Kawahara certificate independently closes: "
          f"Y0={run['constants']['Y0']:.4e}, r_min={run['verdict']['r_min']:.4e}")


def test_known_answer_gate_still_passes_on_current_code():
    """Reproduces test_interval_certificate.py gate 16's own assertions directly (not by
    shelling out to the whole 18-gate, ~15-minute suite) against the CURRENT module: CLN's
    published r0 is a certified radius, the certificate reaches CLN's uniqueness ball, and
    r_min sits under 1.0 decades below r0 (banked at 0.53)."""
    g = known_answer_gate_check(post_mod)
    assert g["closes"] and g["Z1_below_one"]
    assert g["r0_is_a_certified_radius"], g
    assert g["reaches_uniqueness_ball"], g
    assert g["within_decades_budget"], (
        f"r_min is {g['decades_below_r0']:.2f} decades below r0, past the 1.0 budget")
    assert g["gate_16_would_pass"]
    # The specific figure test_interval_certificate.py's own docstring records as banked at
    # leg 61 is 0.53 decades; this must stay in the same ballpark, not drift by an order of
    # magnitude, or gate 16 on `main` would itself be about to fail.
    assert abs(g["decades_below_r0"] - 0.53) < 0.5, (
        f"decades_below_r0 = {g['decades_below_r0']:.4f} has drifted far from the banked "
        f"0.53 -- re-derive, do not just widen this tolerance")
    print(f"[ok] leg 61's known-answer gate still passes on current code: r_min sits "
          f"{g['decades_below_r0']:.4f} decades below CLN's r0 (banked 0.53), certified "
          f"interval {g['certified_interval_Hl']}")


def test_static_diff_is_additive_only():
    """The repair must be a strict ADDITION to the module (new hypothesis/containment
    guards), never a removal of an existing top-level definition -- a removed def would be
    a much larger surface change than the repair's own commit message describes."""
    _pre_mod, pre_src, _meta = _prerepair()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "solver",
                           "interval_certificate.py")) as fh:
        post_src = fh.read()
    import re
    pre_defs = set(re.findall(r"^(?:def|class) (\w+)", pre_src, re.M))
    post_defs = set(re.findall(r"^(?:def|class) (\w+)", post_src, re.M))
    removed = pre_defs - post_defs
    assert removed == set(), f"the repair REMOVED top-level definitions: {removed}"
    added = post_defs - pre_defs
    assert {"CertificateInputError", "_hypothesis_violations",
           "_containment_screen"} <= added, added
    print(f"[ok] static diff is additive-only: 0 removed defs, {len(added)} added "
          f"({sorted(added)})")


if __name__ == "__main__":
    test_prerepair_module_still_has_the_defect_negative_control()
    test_postrepair_battery_rejects_every_case_gate_a()
    test_kawahara_bitwise_zero_regression_gate_b()
    test_prerepair_kawahara_certificate_still_closes()
    test_known_answer_gate_still_passes_on_current_code()
    test_static_diff_is_additive_only()
    print("\nALL POST-REPAIR REGRESSION GATES PASS -- gate (a) 12/36->0/36 independently "
          "re-derived with a working negative control, gate (b) Kawahara bit-identical "
          "pre/post and leg 61's known-answer gate still passes (leg 105, Route-ICB).")
