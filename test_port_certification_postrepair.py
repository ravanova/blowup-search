"""Leg 86 (Route-PCB) -- the PERMANENT post-repair regression gate for the line sweep.

Leg 79's bench-repair added domain validation to `radii_polynomial_status` (11 of 25
hypothesis-violating inputs came back closes=True before, 0 of 25 after) inside
`solver/port_certification.py` -- a module whose OTHER claim, the one `capabilities.py`
advertises, is that `line_sweep_solve` inverts the full transport operator to 9.5e-16.
This file gates the second claim against the first repair, and against any future one.

WHY THIS FILE EXISTS ALONGSIDE test_port_certification.py's test_7.  test_7 asserts
`err < 1e-11` on one configuration while the advertised figure is 9.5e-16 -- about four
decades of slack, i.e. a precision regression of four orders of magnitude would pass it
silently.  These gates close that gap in two ways: the canonical configuration is held to
the ADVERTISED number, and the sweep's output is compared BIT-FOR-BIT against the module
as it stood before the repair, recovered from git.  "Both are small" is not the statement;
"nothing moved" is.

Pre-committed predicates:
  (1) THE ADVERTISED NUMBER, NOT A LOOSE ONE: test_7's exact configuration (seed 11, 48x16,
      drho 0.09, dbeta 0.033, c -1.0145) returns the full transport operator's own right-hand
      side to <= 9.5e-16 relative.  Measured 9.472e-16 at leg 86.
  (2) NOTHING MOVED ACROSS THE REPAIR: over a battery spanning grids 48x16 to 300x48 and the
      marginal-s_rho regime, the sweep's output is bit-for-bit identical to the pre-repair
      module's.  Skipped, loudly, only if git cannot recover the parent revision.
  (3) THE REPAIR'S TEXT IS DISJOINT FROM THE SWEEP: the set of top-level definitions the
      repair commit touched contains neither `line_sweep_solve` nor anything on its path.
      This corroborates (2) from the source side rather than resting on it.
  (4) NO PERFORMANCE REGRESSION, JUDGED AGAINST A MEASURED NULL: interleaved pre / post /
      post-null timing rounds; |post/pre - 1| must sit inside max(4 x the null arm's own
      deviation, 25%).  A bare speed ratio with no null arm would be a timing anecdote, which
      is what test_route_g_perf.py's doc-string already refuses; the tolerance is deliberately
      wider than leg 86's measurement (1.12% against a 0.29% null) because a CI machine is
      noisier than a bench, and the null arm is what adapts to that.
  (5) THE ARTIFACT CARRIES THE FINDING, and carries the scope caveat with it: the battery-wide
      worst residual is ~10.6x the 9.5e-16 figure on the LARGEST grids, in BOTH module versions
      identically.  That is a caveat on how the claim is worded, not a regression, and the
      artifact must keep both readings distinguishable.

Run: python test_port_certification_postrepair.py      (~40 s, no scipy)
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from experiments.p2_route_pcb_v1_postrepair import (      # noqa: E402
    CANONICAL, CLAIMED_PRECISION, apply_transport, clause_P1_static, clause_P3_timing,
    find_repair_commit, load_module, make_case, _git,
)
from solver.boussinesq_velocity import _thomas            # noqa: E402

ARTIFACT = ROOT / "writeup/data/p2_route_pcb_v1_postrepair.json"


def _pre_repair_module():
    """The module as it stood immediately before leg 79's repair, or None if git cannot."""
    try:
        commits = find_repair_commit()
        return load_module(_git("show", f"{commits['parent']}:solver/port_certification.py"),
                           "pcb_pre_repair_test"), commits
    except Exception as exc:                                # pragma: no cover -- CI without git
        print(f"  [skip] could not recover the pre-repair revision from git: {exc!r}")
        return None, None


def _residual(mod, case):
    s_rho, s_beta, rhs = case["arrays"]
    x = mod.line_sweep_solve(rhs, s_rho, s_beta, case["drho"], case["dbeta"],
                             case["c"], _thomas)
    back = apply_transport(x, s_rho, s_beta, case["drho"], case["dbeta"], case["c"])
    return x, float(np.max(np.abs(back - rhs)) / np.max(np.abs(rhs)))


def test_1_canonical_configuration_still_hits_the_advertised_number():
    """(1) 9.5e-16 is what capabilities.py claims, so 9.5e-16 is what is asserted."""
    from solver import port_certification as post
    case = make_case(CANONICAL["seed"], CANONICAL["n_r"], CANONICAL["n_b"],
                     CANONICAL["drho"], CANONICAL["dbeta"], CANONICAL["c"])
    _, err = _residual(post, case)
    assert err <= CLAIMED_PRECISION, (
        f"the line sweep returns the rhs to {err:.4e}, above the advertised "
        f"{CLAIMED_PRECISION:.1e} -- capabilities.py's claim for "
        f"solver/port_certification.py no longer holds on its own configuration")
    print(f"  (1) canonical configuration: rhs recovered to {err:.4e} against the advertised "
          f"{CLAIMED_PRECISION:.1e} ({CLAIMED_PRECISION / err:.2f}x margin)  OK")


def test_2_nothing_moved_across_the_repair_bit_for_bit():
    """(2) pre-repair vs post-repair, on the bit patterns, not on the magnitudes."""
    from solver import port_certification as post
    pre, _ = _pre_repair_module()
    if pre is None:
        return
    cases = [make_case(CANONICAL["seed"], CANONICAL["n_r"], CANONICAL["n_b"],
                       CANONICAL["drho"], CANONICAL["dbeta"], CANONICAL["c"]),
             make_case(1, 96, 32, 0.09, 0.033, -1.0145),
             make_case(5, 96, 32, 0.09, 0.033, -1.0145, s_rho_lo=1e-3, s_rho_hi=5e-3),
             make_case(8, 300, 48, 0.0334, 0.0654, -1.0145),
             make_case(9, 300, 48, 0.0334, 0.0654, -2.029)]
    worst_pre = worst_post = 0.0
    entries = differing = 0
    for case in cases:
        x_pre, e_pre = _residual(pre, case)
        x_post, e_post = _residual(post, case)
        worst_pre, worst_post = max(worst_pre, e_pre), max(worst_post, e_post)
        d = int(np.count_nonzero(x_pre.view(np.uint64) != x_post.view(np.uint64)))
        entries += x_pre.size
        differing += d
        assert d == 0, (f"{case['label']}: {d} of {x_pre.size} entries differ from the "
                        f"pre-repair module's output; relative residual {e_pre:.4e} -> "
                        f"{e_post:.4e}")
    print(f"  (2) {len(cases)} configurations, {entries} entries: {differing} differ from the "
          f"pre-repair module; worst relative residual {worst_pre:.4e} -> {worst_post:.4e}  OK")


def test_3_the_repairs_text_is_disjoint_from_the_sweep():
    """(3) the source-side corroboration of (2)."""
    try:
        commits = find_repair_commit()
    except Exception as exc:                                # pragma: no cover
        print(f"  [skip] git unavailable: {exc!r}")
        return
    p1 = clause_P1_static(commits)
    assert not p1["defs_touched_on_sweep_path"], p1
    assert not p1["defs_touched_adjacent"], p1
    print(f"  (3) the repair moved +{p1['lines_added']}/-{p1['lines_removed']} lines across "
          f"{p1['top_level_defs_touched']}; 0 of them on the sweep's call path or the "
          f"adjacent hot path  OK")


def test_4_no_performance_regression_against_a_measured_null():
    """(4) the timing arm -- and it carries its own noise floor, measured in the same run."""
    from solver import port_certification as post
    pre, _ = _pre_repair_module()
    if pre is None:
        return
    t = clause_P3_timing(pre, post, rounds=7, calls=3)
    for grid, row in t.items():
        dev = abs(row["post_over_pre_median"] - 1.0)
        null = abs(row["null_over_post_median"] - 1.0)
        budget = max(4.0 * null, 0.25)
        assert dev <= budget, (
            f"{grid}: post-repair median {row['median_s_post']*1e3:.3f} ms against pre-repair "
            f"{row['median_s_pre']*1e3:.3f} ms, deviation {dev:.2%}, outside a budget of "
            f"{budget:.2%} set by a null (post vs post) arm of {null:.2%}")
        print(f"  (4) {grid}: pre {row['median_s_pre']*1e3:.2f} ms, post "
              f"{row['median_s_post']*1e3:.2f} ms, deviation {dev:.2%} inside a "
              f"{budget:.2%} budget (null arm {null:.2%})  OK")


def test_5_artifact_carries_the_finding_and_its_scope_caveat():
    """(5) the banked numbers, including the caveat that must not read as a regression."""
    assert ARTIFACT.exists(), f"missing {ARTIFACT}"
    d = json.loads(ARTIFACT.read_text())
    g = d["gate_answer"]
    assert g["answer"] == "yes", g
    a, b = g["a_precision"], g["b_timing"]
    assert a["canonical_case_post"] <= CLAIMED_PRECISION, a
    assert a["canonical_case_post"] == a["canonical_case_pre"], a
    assert a["nothing_moved_across_the_repair"] is True, a
    assert a["total_entries_differing"] == 0 and a["worst_ulp_gap"] == 0, a
    # the scope caveat is banked, and banked as PRE-EXISTING: identical in both versions
    scope = a["battery_scope_caveat"]
    assert scope["moved_across_the_repair"] is False, scope
    assert scope["worst_rel_residual_post"] == scope["worst_rel_residual_pre"], scope
    assert scope["worst_over_claimed_gate"] > 1.0, scope
    # timing, judged against the null arm rather than against a bare threshold
    assert b["within_variance"] is True, b
    assert b["worst_abs_pre_post_deviation"] < 0.10, b
    # the consequence arm: every rung of the preconditioned ladder identical
    p4 = d["P4_ladder"]["comparison"]
    assert p4["rungs_identical"] == p4["rungs_total"], p4
    print(f"  (5) artifact: canonical {a['canonical_case_post']:.4e} pre and post, "
          f"{a['bit_identical_cases']} cases bit-identical, timing deviation "
          f"{b['worst_abs_pre_post_deviation']:.2%} against a {b['worst_null_arm_deviation']:.2%} "
          f"null; battery worst {scope['worst_over_claimed_gate']:.2f}x the advertised figure "
          f"and IDENTICAL pre/post, i.e. a scope caveat, not a regression  OK")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_canonical_configuration_still_hits_the_advertised_number,
               test_2_nothing_moved_across_the_repair_bit_for_bit,
               test_3_the_repairs_text_is_disjoint_from_the_sweep,
               test_4_no_performance_regression_against_a_measured_null,
               test_5_artifact_carries_the_finding_and_its_scope_caveat):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
