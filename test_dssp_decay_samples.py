"""Tests for solver/dssp_decay_samples.py — the samples→cells adapter (leg 385).

Self-running, per this repository's convention:  .venv/bin/python test_dssp_decay_samples.py

The property that matters and is easy to fake here is not accuracy, it is REFUSAL.  An
adapter that quietly invents an enclosure from bare samples would look identical to a correct
one on every honest input and would be worthless on every real one.  So the battery is built
around three things:

  1  the adapter REFUSES an input carrying neither hypothesis, and refuses a declared
     hypothesis that the samples themselves already contradict;
  2  under a TRUE hypothesis it is SOUND — the true profile stays inside every cell — and
     under PATH A it is TIGHT, reproducing leg 382's exact-power width to the bit;
  3  under a FALSE-but-undetectable hypothesis it accepts and the resulting certificate is
     WRONG, which is the whole reason the hypothesis is recorded in the row.  A test suite
     that only showed (1) and (2) would be hiding (3).
"""

import numpy as np

from solver.dssp_decay_enclosure import (
    VERDICT_INTERVAL, certified_decay_interval, planted_power_law,
)
from solver.dssp_decay_samples import (
    HYP_BOTH, HYP_MODULUS, HYP_MONOTONE, Modulus, VERDICT_CELLS, VERDICT_INCAPACITY,
    certified_decay_from_samples, containment_audit, planted_node_aligned_wiggle,
    planted_sampled_power_law, samples_to_cells,
)

R0, R1, NCELL = 10.0, 1000.0, 1000
GRID = np.geomspace(R0, R1, NCELL + 1)


def _s1_samples(C=3.0, p=1.0):
    return planted_sampled_power_law(C, p, GRID)


# ---------------------------------------------------------------------------
# 1.  refusal
# ---------------------------------------------------------------------------

def test_no_hypothesis_is_refused_not_guessed():
    f_lo, f_hi, _ = _s1_samples()
    out = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi)
    assert out["verdict"] == VERDICT_INCAPACITY, "bare samples produced an enclosure"
    assert out["r_lo"] is None and out["f_lo"] is None, "a refusal still returned cells"
    assert "NO HYPOTHESIS SUPPLIED" in out["reason"]
    print("[ok] samples with neither hypothesis return INCAPACITY and no cells")


def test_no_hypothesis_never_reaches_leg_382():
    f_lo, f_hi, _ = _s1_samples()
    out = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi)
    assert out["verdict"] == VERDICT_INCAPACITY and out["enclosure_called"] is False
    assert out["p_lo"] is None and out["width"] is None
    print("[ok] with no hypothesis leg 382's routine is never called and no exponent exists")


def test_visible_monotonicity_violation_is_refused_with_an_index():
    f_lo, f_hi, _ = _s1_samples()
    f_lo, f_hi = f_lo.copy(), f_hi.copy()
    f_lo[500] *= 1.05
    f_hi[500] *= 1.05
    out = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, monotone="nonincreasing")
    assert out["verdict"] == VERDICT_INCAPACITY
    assert out["necessary_condition_checks"]["monotone_worst_index"] == 499
    assert out["necessary_condition_checks"]["monotone_worst_violation"] > 0.0
    print("[ok] samples contradicting the declared direction refuse, naming cell 499")


def test_understated_modulus_is_refused_when_the_samples_already_break_it():
    f_lo, f_hi, _ = _s1_samples(1.0, 2.0)
    out = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi,
                           modulus=Modulus(0.1, 1.0, "loglog"))
    assert out["verdict"] == VERDICT_INCAPACITY
    ratio = out["necessary_condition_checks"]["modulus_worst_ratio"]
    assert 15.0 < ratio < 25.0, f"expected ratio near 20 (true slope 2 vs declared 0.1), got {ratio}"
    print(f"[ok] an understated modulus visible at the samples refuses; ratio {ratio:.4f}")


def test_bad_inputs_refuse_rather_than_proceed():
    f_lo, f_hi, _ = _s1_samples()
    cases = {
        "non-monotone radii": dict(r=GRID[::-1], f_lo=f_lo[::-1] * 0 + f_lo, f_hi=f_hi),
        "radius below 1": dict(r=np.linspace(0.5, 10.0, 11),
                               f_lo=np.linspace(1.0, 0.1, 11), f_hi=np.linspace(1.0, 0.1, 11)),
        "single sample": dict(r=GRID[:1], f_lo=f_lo[:1], f_hi=f_hi[:1]),
        "negative sample": dict(r=GRID, f_lo=-f_lo, f_hi=f_hi),
        "both f and f_lo": dict(r=GRID, f=f_lo, f_lo=f_lo, f_hi=f_hi),
    }
    for name, kw in cases.items():
        r = kw.pop("r")
        out = samples_to_cells(r, monotone="nonincreasing", **kw)
        assert out["verdict"] == VERDICT_INCAPACITY, f"{name} was accepted"
    print(f"[ok] all {len(cases)} malformed inputs refuse")


def test_modulus_must_be_a_declared_object_not_a_bare_number():
    f_lo, f_hi, _ = _s1_samples()
    out = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, modulus=1.0)
    assert out["verdict"] == VERDICT_INCAPACITY
    for bad in (0.3, 2.0, -1.0):
        try:
            Modulus(1.0, bad, "loglog")
        except ValueError:
            continue
        raise AssertionError(f"alpha={bad} was accepted; only 1/2 and 1 are proved here")
    print("[ok] a bare number is not a modulus, and alpha outside {1/2, 1} is rejected")


def test_loglog_modulus_too_coarse_for_the_exp_free_bound_refuses():
    f_lo, f_hi, _ = _s1_samples()
    out = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi,
                           modulus=Modulus(1000.0, 1.0, "loglog"))
    assert out["verdict"] == VERDICT_INCAPACITY and ">= 1" in out["reason"]
    print("[ok] omega(dt/2) >= 1 refuses instead of approximating e**x")


# ---------------------------------------------------------------------------
# 2.  soundness, and PATH A's tightness against leg 382
# ---------------------------------------------------------------------------

def test_path_A_reproduces_leg_382_exact_power_widths():
    #  leg 382's own planted knowns K1-K4, and its own banked widths.
    for C, p, ref in ((3.0, 1.0, 7.438494264988549e-15), (1.0, 2.0, 1.5987211554602254e-14),
                      (0.25, 2.5, 1.9984014443252818e-14), (7.0, 3.0, 1.554312234475219e-14)):
        f_lo, f_hi, _ = _s1_samples(C, p)
        got = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi,
                                           monotone="nonincreasing")
        iv_fn, _ = planted_power_law(C, p)
        base = certified_decay_interval(iv_fn, R0, R1, NCELL, "cells")
        assert got["verdict"] == VERDICT_INTERVAL == base["verdict"]
        assert got["p_lo"] <= p <= got["p_hi"], "truth escaped the certified interval"
        assert got["width"] == base["width"], (
            f"p={p}: sampled width {got['width']!r} != leg 382's {base['width']!r}")
        assert got["width"] == ref, \
            f"p={p}: width {got['width']!r} != leg 382's BANKED row {ref!r}"
    print("[ok] PATH A reproduces leg 382's exact-power widths BIT-IDENTICALLY (p = 1, 2, 2.5, 3)")


def test_path_B_is_sound_and_contains_the_truth_but_is_far_wider():
    f_lo, f_hi, _ = _s1_samples()
    got = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi,
                                       modulus=Modulus(1.05, 1.0, "loglog"))
    assert got["verdict"] == VERDICT_INTERVAL
    assert got["p_lo"] <= 1.0 <= got["p_hi"], "truth escaped PATH B's interval"
    assert 7e-4 < got["width"] < 6e-3, f"PATH B width {got['width']} outside the measured band"
    assert got["width"] > 1e6 * 7.44e-15
    print(f"[ok] PATH B is sound, contains p=1, width {got['width']:.4e} — 11 orders "
          "wider than PATH A, as its modulus requires")


def test_path_B_width_scales_like_one_over_N():
    widths = []
    Ns = [100, 250, 1000]
    for N in Ns:
        g = np.geomspace(R0, R1, N + 1)
        f_lo, f_hi, _ = planted_sampled_power_law(3.0, 1.0, g)
        got = certified_decay_from_samples(g, f_lo=f_lo, f_hi=f_hi,
                                           modulus=Modulus(1.05, 1.0, "loglog"))
        widths.append(got["width"])
    slope = np.polyfit(np.log(Ns), np.log(widths), 1)[0]
    assert -1.05 < slope < -0.95, f"PATH B width slope {slope} is not -1"
    print(f"[ok] PATH B width scales as N**({slope:.4f}) — set by the grid, not by rounding")


def test_globally_stated_absolute_modulus_dies_on_a_three_decade_window():
    f_lo, f_hi, _ = _s1_samples()
    cells = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi,
                             modulus=Modulus(0.03, 1.0, "absolute"))
    assert cells["verdict"] == VERDICT_CELLS
    assert cells["n_cells_nonpositive_lower"] > 250
    first = cells["enclosure_parts"]["modulus"]["first_nonpositive_radius"]
    assert 100.0 < first < 420.0, f"first non-positive radius {first} outside the band"
    got = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi,
                                       modulus=Modulus(0.03, 1.0, "absolute"))
    assert got["verdict"] == VERDICT_INCAPACITY and "zero" in got["reason"]
    print(f"[ok] a global absolute modulus goes non-positive from r = {first:.1f} and the "
          "downstream answers INCAPACITY, not a number")


def test_both_hypotheses_intersect_and_the_tighter_one_wins():
    f_lo, f_hi, _ = _s1_samples()
    got = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi,
                                       monotone="nonincreasing",
                                       modulus=Modulus(1.05, 1.0, "loglog"))
    iv_fn, _ = planted_power_law(3.0, 1.0)
    base = certified_decay_interval(iv_fn, R0, R1, NCELL, "cells")
    assert got["hypothesis"] == HYP_BOTH
    assert abs(got["width"] - base["width"]) < 1e-15
    print("[ok] declaring both hypotheses intersects the enclosures; PATH A dominates")


def test_containment_audit_can_report_clean():
    f_lo, f_hi, true_fn = _s1_samples()
    for kw in (dict(monotone="nonincreasing"),
               dict(modulus=Modulus(1.05, 1.0, "loglog")),
               dict(modulus=Modulus(0.03, 1.0, "absolute"))):
        cells = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, **kw)
        audit = containment_audit(cells, true_fn)
        assert audit["contained"] and audit["worst_signed_excess"] < 0.0, \
            "the audit fired on an honest row — it is not a rubber stamp in reverse"
    print("[ok] the audit reports CLEAN on all three honest rows (it can say no)")


# ---------------------------------------------------------------------------
# 3.  the hypothesis is a hypothesis: false-but-undetectable inputs are accepted
#     and the resulting certificate is WRONG
# ---------------------------------------------------------------------------

def test_secretly_non_monotone_input_is_accepted_and_the_certificate_is_false():
    f_lo, f_hi, _ = _s1_samples()
    truth = planted_node_aligned_wiggle(3.0, 1.0, 0.05, GRID)
    cells = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi, monotone="nonincreasing")
    assert cells["verdict"] == VERDICT_CELLS, \
        "the adapter claimed to detect a violation it provably cannot see"
    audit = containment_audit(cells, truth)
    assert not audit["contained"], "the audit missed a 5% excursion"
    assert 0.03 < audit["worst_signed_relative_excess"] < 0.06
    assert audit["n_cells_violated"] == NCELL
    got = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi, monotone="nonincreasing")
    assert got["verdict"] == VERDICT_INTERVAL and got["width"] < 1e-13
    assert got["hypothesis"] == HYP_MONOTONE and "nonincreasing" in got["conditional_on"]
    print(f"[ok] a secretly non-monotone profile yields a width-{got['width']:.2e} certificate "
          f"that is FALSE about it (audit +{audit['worst_signed_relative_excess']:.4f} in every "
          "cell) — and the row says what it is conditional on")


def test_understated_modulus_invisible_at_the_samples_is_accepted_and_containment_fails():
    f_lo, f_hi, _ = _s1_samples()
    truth = planted_node_aligned_wiggle(3.0, 1.0, 0.05, GRID)
    cells = samples_to_cells(GRID, f_lo=f_lo, f_hi=f_hi,
                             modulus=Modulus(1.05, 1.0, "loglog"))
    assert cells["verdict"] == VERDICT_CELLS
    audit = containment_audit(cells, truth)
    assert not audit["contained"]
    assert 0.035 < audit["worst_signed_log_excess"] < 0.055
    print(f"[ok] an understated modulus invisible at the samples is accepted and the truth "
          f"escapes by {audit['worst_signed_log_excess']:.5f} in log f")


def test_every_returned_row_carries_its_hypothesis():
    f_lo, f_hi, _ = _s1_samples()
    for kw, expect in ((dict(monotone="nonincreasing"), HYP_MONOTONE),
                       (dict(modulus=Modulus(1.05, 1.0, "loglog")), HYP_MODULUS),
                       (dict(monotone="nonincreasing",
                             modulus=Modulus(1.05, 1.0, "loglog")), HYP_BOTH)):
        got = certified_decay_from_samples(GRID, f_lo=f_lo, f_hi=f_hi, **kw)
        assert got["hypothesis"] == expect
        assert got["conditional_on"] and got["conditional_on"].startswith("These cell enclosures")
        assert got["sample_exactness"] == "enclosed"
    got = certified_decay_from_samples(GRID, f=f_hi, monotone="nonincreasing")
    assert got["sample_exactness"] == "declared-exact" and "EXACT" in got["conditional_on"]
    print("[ok] every row carries hypothesis, detail, sample_exactness and conditional_on")


def test_mutually_inconsistent_declarations_refuse():
    #  a modulus so tight that no monotone step could satisfy it, declared alongside
    #  monotonicity: the two enclosures are disjoint and neither is silently preferred.
    f_lo, f_hi, _ = _s1_samples()
    f_lo2, f_hi2 = f_lo.copy(), f_hi.copy()
    f_lo2[400] = f_hi2[400] = f_lo[400] * 0.5      # a certified cliff at one sample
    out = samples_to_cells(GRID, f_lo=f_lo2, f_hi=f_hi2, monotone="nonincreasing",
                           modulus=Modulus(1.05, 1.0, "loglog"))
    assert out["verdict"] == VERDICT_INCAPACITY
    print("[ok] declarations that cannot both hold refuse instead of picking one")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)}/{len(tests)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
