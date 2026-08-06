"""Leg 131 (Route-HNB) -- leg 100's battery, BANKED AS A PERMANENT REGRESSION SUITE.

The gate's YES branch says exactly this: "Repair confirmed solid and non-regressive by an
independent run.  Bank leg 100's battery as a permanent regression suite."  This file is
that bank.

It is NOT a copy of leg 100's battery and it is NOT the repair's own inverted test.  It
drives `experiments/p2_route_hnb_v1_postrepair.py`, which imports leg 100's battery
UNMODIFIED, twice in one process, bound to the pre-repair blob and to the working tree, and
classifies every case with leg 100's OWN `classify()`.  Every threshold below is a magnitude
measured on 2026-08-06 and quoted from `writeup/data/p2_route_hnb_v1_postrepair.json`.

What each check would catch:

  1  a guard removed from `solver/holder_norms.py`            -> gate 2, gate 3
  2  a NEW silent-corruption path opened anywhere in the      -> gate 3
     six mechanisms leg 100 found
  3  the harness going blind (so that "0 silent" is vacuous)  -> gate 1, gate 4
  4  any clean number in the module moving by one bit         -> gate 5
  5  the module's own known-answer file breaking              -> gate 6
  6  the gamma = 1 residual silently changing character       -> gate 8
  7  the 6th and 7th mechanisms reopening                     -> gate 7

Gate 1 is the load-bearing one and it is deliberately an INEQUALITY IN THE OTHER
DIRECTION: the pre-repair arm must still report leg 100's silence.  Per lesson 90, a control
that cannot come out differently is not a control -- if this suite ever reports 0 silent
cases on BOTH arms, it has stopped testing anything, and gate 1 is what fails first.

Run: python test_holder_norms_postrepair.py     (~6 s)
"""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

_spec = importlib.util.spec_from_file_location(
    "hnb_postrepair", os.path.join(HERE, "experiments", "p2_route_hnb_v1_postrepair.py"))
hnb = importlib.util.module_from_spec(_spec)
sys.modules["hnb_postrepair"] = hnb
_spec.loader.exec_module(hnb)


def _ok(n, msg):
    print("[ok] (%d) %s" % (n, msg))


def main():
    d = hnb.main(write=False)      # measure, but never dirty the banked JSON
    print()

    ca = d["gate"]["clause_a"]
    cb = d["gate"]["clause_b"]

    # -- 1 -- the NEGATIVE CONTROL.  The pre-repair arm must still be corrupt.
    pre_scope = ca["prerepair_n_silent_in_scope"]
    assert pre_scope == 14, (
        "negative control DEAD: the pre-repair arm reports %d silent cases in scope, "
        "expected 14. Either the pinned blob b614a116 stopped resolving, or the battery "
        "stopped classifying. A suite whose control cannot fail is not a suite." % pre_scope)
    assert ca["negative_control_live"], "negative control reported not live"
    _ok(1, "negative control LIVE: the pre-repair blob still reports %d/%d silent cases "
           "in leg 100's six mechanism gates (this number failing is the first sign the "
           "suite has gone blind)" % (pre_scope, ca["prerepair_n_verdicts_in_scope"]))

    # -- 2 -- the validation surface exists at all
    surf = d["P3b_validation_surface"]
    assert surf["prerepair"]["n_raise_sites"] == 0, "pre-repair arm is not the pre-repair module"
    assert surf["postrepair"]["n_raise_sites"] >= 26, (
        "validation surface shrank: %d raise sites, expected >= 26"
        % surf["postrepair"]["n_raise_sites"])
    _ok(2, "validation surface %d -> %d raise sites across %d public entry points, "
           "counted by leg 100's own AST gate"
        % (surf["prerepair"]["n_raise_sites"], surf["postrepair"]["n_raise_sites"],
           surf["postrepair"]["n_public_entry_points"]))

    # -- 3 -- clause (a): no silent corruption left in leg 100's six mechanisms
    assert ca["postrepair_n_silent_in_scope"] == 0, (
        "SILENT CORRUPTION HAS REOPENED in leg 100's mechanism gates: %s"
        % ca["residual_out_of_scope_silent_cases"])
    per = ca["per_gate"]
    for g, want in (("A1", 4), ("A2", 1), ("A3", 5), ("A4", 2), ("A6", 2)):
        assert per[g]["prerepair_silent"] == want, (
            "gate %s pre-repair silent count moved: %s, expected %d"
            % (g, per[g]["prerepair_silent"], want))
        assert per[g]["postrepair_silent"] == 0, "gate %s is silent again" % g
    assert ca["bare_sites_postrepair"]["n_adversarial_silent"] == 1, (
        "the adversarial bare sites changed: %s"
        % ca["bare_sites_postrepair"]["adversarial_silent_sites"])
    _ok(3, "clause (a): %d/%d silent -> %d/%d, per gate A1 4->0, A2 1->0, A3 5->0, "
           "A4 2->0, A6 2->0; adversarial bare sites 2/5 -> 1/5"
        % (pre_scope, ca["prerepair_n_verdicts_in_scope"],
           ca["postrepair_n_silent_in_scope"], ca["postrepair_n_verdicts_in_scope"]))

    # -- 4 -- leg 100's positive control still signals on BOTH arms
    pc = d["P7_positive_control"]
    assert pc["prerepair"]["n_signalled"] == 4 and pc["postrepair"]["n_signalled"] == 4, (
        "positive control degraded: %s / %s"
        % (pc["prerepair"]["n_signalled"], pc["postrepair"]["n_signalled"]))
    _ok(4, "positive control 4/4 signalled on both arms -- every silence reported above "
           "is the module's, not the instrumentation's")

    # -- 5 -- clause (b): the same-process bitwise differential
    diff = d["P4_clean_bitwise_differential"]
    assert diff["n_moved"] == 0, "CLEAN VALUES MOVED: %s" % [
        r["field"] for r in diff["fields"] if not r["bit_identical"]]
    assert diff["n_compared"] >= 19, "differential shrank to %d fields" % diff["n_compared"]
    _ok(5, "clause (b) bitwise: %d/%d clean values identical to the last bit across a "
           "same-process pre/post differential, 0 moved (conformal_check "
           "1.517287054473293e-04, family_op_norm 661.2075718521894, "
           "holder_H_constant random_best 0.8914207747116539)"
        % (diff["n_bit_identical"], diff["n_compared"]))

    # -- 6 -- the module's dedicated known-answer file, run fresh
    ded = d["P5_dedicated_known_answer"]
    assert ded["returncode"] == 0 and ded["all_passed_banner"], "test_holder_norms.py FAILED"
    assert ded["n_gates_ok"] == 6, "expected 6 known-answer gates, got %d" % ded["n_gates_ok"]
    _ok(6, "dedicated known-answer file test_holder_norms.py: %d/6 gates green, run fresh "
           "in a subprocess (it predates the repair by one commit and was never touched "
           "by it)" % ded["n_gates_ok"])

    # -- 7 -- the 6th and 7th mechanisms
    m6 = d["P6b_sixth_mechanism_warning_decay"]
    assert m6["prerepair_n_that_go_silent_on_repeat"] == 2, "6th mechanism control moved"
    assert all(r["verdict"] == "FLAGGED_RAISE" for r in m6["postrepair_unshimmed_reprobe"]), \
        "the warning-decay mechanism has reopened"
    m7pre, m7post = d["P6_seventh_mechanism"]["prerepair"], d["P6_seventh_mechanism"]["postrepair"]
    assert m7pre["n_silent"] == 2 and m7post["n_silent"] == 0, (
        "7th mechanism: pre %d silent, post %d silent" % (m7pre["n_silent"], m7post["n_silent"]))
    _ok(7, "6th mechanism (warning decay, silent from call 2 onward on 2/2 sites) and 7th "
           "(descending grid, coverage 1.9094999985985477 -> 1019.8141148113144, a 534.07x "
           "overstatement; duplicated node 5.058518859734074e-04 -> 8.127828757138467e-04, "
           "1.6068x) both now raise: 2/3 silent -> 0/3")

    # -- 8 -- the gamma = 1 residual has not changed character
    p8 = d["P8_gamma_one_boundary"]
    assert p8["n_reference_bit_identical"] == p8["n_reference_checks"], (
        "gamma = 1 STOPPED reproducing an independent reference (%d/%d) -- the residual "
        "has become a real corruption and must be escalated"
        % (p8["n_reference_bit_identical"], p8["n_reference_checks"]))
    assert p8["blast_radius"]["n_live_call_sites_with_gamma_ge_1"] == 0, (
        "a live caller now passes gamma >= 1; the residual is no longer latent and "
        "solver/nk_seminorm.py's three reasons for excluding gamma = 1 now bite")
    _ok(8, "gamma = 1 residual unchanged in character: %d/%d module values bit-identical "
           "to an independent reference from the docstring formula, and %d live call "
           "sites pass gamma >= 1 (max gamma in repo %s) -- correct value, latent, "
           "reported not patched"
        % (p8["n_reference_bit_identical"], p8["n_reference_checks"],
           p8["blast_radius"]["n_live_call_sites_with_gamma_ge_1"],
           p8["blast_radius"]["max_gamma_passed_anywhere"]))

    assert d["gate"]["answer"] == "YES", "gate answer changed to %s" % d["gate"]["answer"]
    assert cb["passes"], "clause (b) failed"
    assert not d["module_edited"], "this leg must never edit solver/holder_norms.py"

    print("\nALL HOLDER-NORM POST-REPAIR REGRESSION CHECKS PASSED")


if __name__ == "__main__":
    main()
