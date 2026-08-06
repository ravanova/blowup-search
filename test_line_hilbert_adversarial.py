"""Adversarial gates for `solver/line_hilbert.py` on near-degenerate grids (leg 96, Route-LHA).

`test_line_hilbert.py` validates the module on WELL-BEHAVED data: smooth sinh-stretched or
uniform meshes, the CLM known-answer pair, a refinement ladder. Every grid in that file is
monotone, bounded and gently graded. This file validates the other half — what the module
does when the grid is hostile — and banks leg 96's battery so the answer cannot silently
regress.

The gate leg 96 answered, verbatim:

  "Under an adversarial battery of near-degenerate non-uniform grids (near-duplicate
   points, extreme local stretching ratios), does solver/line_hilbert.py's dense operator
   or its cached slope_matrix ever silently return a finite, plausible-looking wrong
   result instead of propagating or flagging the ill-conditioning?"

Answered NO over 25 in-scope cases, 0 silent corruptions. `solver/line_hilbert.py` was not
edited.

HOW "SILENT" IS DECIDED HERE, AND WHY IT IS NOT "INACCURATE"
------------------------------------------------------------
A degenerate grid makes the cubic spline interpolant a poor representation of the field,
so a large error against the ANALYTIC answer is what any correct implementation of this
method must produce — it is a property of the grid, not a fault of the code. Scoring
against the analytic answer alone would have produced a FALSE YES here (three in-scope
cases miss the analytic answer by 4.1e-02, 2.9e-01 and 1.3e+02 while the code is exact).

So these tests compare the module against an INDEPENDENT IMPLEMENTATION of the same
discretization, from `experiments/p2_route_lha_v1_adversarial.py`: pivoted dense LU instead
of the module's unpivoted Thomas sweeps, and exact per-cell Cauchy integration by
polynomial deflation instead of the module's A(s)/B(s) closed forms. Silent corruption is
then: all-finite AND plausible in magnitude AND nothing raised AND disagreeing with that
reference by more than 1e-8. `test_reference_selfcheck` gates the reference itself first —
if that test fails, none of the others mean anything.

TWO KINDS OF TEST LIVE IN THIS FILE, AND THEY MUST NOT BE CONFUSED
------------------------------------------------------------------
1. SOUNDNESS gates (`test_no_silent_*`, `test_exact_duplicate_*`, `test_slope_*`). These
   assert the property. If one ever fails, the module has started returning quietly wrong
   operators on degenerate grids.

2. CHARACTERIZATION gates (`test_characterize_*`). These pin behaviour leg 96 MEASURED and
   REPORTED but was not authorised to repair: that `slope_matrix`'s documented agreement
   with the Thomas sweeps is grid-dependent and not the flat 2.7e-13 that `capabilities.py`
   records; that grid MONOTONICITY is an unstated precondition whose violation returns a
   plausible sign-flipped answer; and that a grid bad enough to cost 29% accuracy is not
   flagged in any way. They PASS today because they describe today's code. When a leg is
   authorised to repair any of them these tests will start FAILING, and that is the
   intended signal — the discipline leg 69 set for `test_interval_stress.py` and leg 80
   reused. THEY MUST NOT BE WEAKENED TO MAKE A REPAIR LOOK UNNECESSARY, and they are not
   endorsements.

Run: .venv/bin/python test_line_hilbert_adversarial.py
"""

import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.p2_route_lha_v1_adversarial import (   # noqa: E402
    REL_TOL,
    ref_hilbert_matrix,
    ref_slopes_matrix,
    run_case,
    sinh_grid,
)
from solver.line_hilbert import (                       # noqa: E402
    line_hilbert_matrix,
    natural_spline_slopes,
    slope_matrix,
)

N = 101                      # keeps the O(n^2) reference under a couple of seconds
EXACT_PEAK = 2.0


def _clm(X):
    return -4.0 * X / (1.0 + 4.0 * X ** 2), 2.0 / (1.0 + 4.0 * X ** 2)


def _perturbed(kind, arg, n=N):
    """The battery's grids, rebuilt here so the test is readable on its own."""
    X0 = sinh_grid(n)
    k = n // 2 + n // 10
    h = X0[k + 1] - X0[k]
    X = X0.copy()
    if kind == "near_dup":
        X[k + 1] = X0[k] + arg * h
    elif kind == "crossed":
        X[k + 1] = X0[k] - arg * h
    elif kind == "compressed":
        X[k + 1:] -= h * (1.0 - arg)
    elif kind == "multi":
        for j in range(15, n - 15, 7):
            X[j + 1] = X0[j] + arg * (X0[j + 1] - X0[j])
    elif kind == "graded":
        m = n // 2
        d = np.cumsum(arg ** np.arange(m, dtype=float))
        d = d / d[-1] * X0[-1]
        X = np.concatenate([-d[::-1], [0.0], d])[: 2 * m + 1]
    else:
        raise ValueError(kind)
    return X


# ==========================================================================
# 1. SOUNDNESS
# ==========================================================================

def test_reference_selfcheck():
    """The independent reference reproduces the module on HEALTHY grids.

    This gates every other test in the file: a reference that disagreed here would make
    the soundness gates below vacuous (or spuriously loud). It is also the check that
    caught the reference's own first bug — a dropped log-cancellation between adjoining
    cells, which showed up as a clean O(h) bias."""
    worst_H = worst_S = 0.0
    for n in (61, 101):
        X = sinh_grid(n)
        Hm, Hr = line_hilbert_matrix(X), ref_hilbert_matrix(X)
        Sm, Sr = np.array(slope_matrix(X)), ref_slopes_matrix(X)
        worst_H = max(worst_H, np.abs(Hm - Hr).max() / np.abs(Hr).max())
        worst_S = max(worst_S, np.abs(Sm - Sr).max() / np.abs(Sr).max())
    print(f"    healthy-grid agreement: dense operator {worst_H:.2e}, slopes {worst_S:.2e}")
    assert worst_H < 1e-12, f"reference disagrees with the module on a healthy grid: {worst_H:.2e}"
    assert worst_S < 1e-12, f"reference slopes disagree on a healthy grid: {worst_S:.2e}"
    print("[ok] independent reference reproduces the module on healthy grids")


def test_no_silent_corruption_near_duplicates():
    """Near-duplicate nodes never make the dense operator quietly wrong.

    Separations swept from 1e-1 h down to 2.2e-16 (ONE ULP), in both orientations —
    including the crossed case a grid generator produces when roundoff inverts a pair —
    plus 12 simultaneous collapsed spacings."""
    worst = 0.0
    for kind, args in (("near_dup", (1e-1, 1e-3, 1e-6, 1e-9, 1e-12, 1e-14, 1e-15)),
                       ("crossed", (1e-6, 1e-12, 1e-14)),
                       ("multi", (1e-11,))):
        for a in args:
            X = _perturbed(kind, a)
            r = run_case(f"{kind}_{a:.0e}", "near_duplicate", X)
            assert not r["silent_corruption"], (
                f"SILENT CORRUPTION on {kind} {a:.0e}: module disagrees with the "
                f"independent reference by {r['rel_vs_ref']:.3e} (dense) / "
                f"{r['slope_rel_vs_ref']:.3e} (slopes) while returning a finite, "
                f"plausible, unflagged operator")
            worst = max(worst, r["rel_vs_ref"], r["slope_rel_vs_ref"])
    print(f"    worst module-vs-reference disagreement over near-duplicates: {worst:.2e}")
    assert worst < REL_TOL
    print("[ok] near-duplicate nodes (down to 1 ulp): no silent corruption")


def test_no_silent_corruption_extreme_stretching():
    """Extreme local stretching never makes the dense operator quietly wrong.

    Spacing ratios up to ~1e74 (geometric grading r=10) and a single cell compressed by
    1e-13 relative to its neighbours."""
    worst = 0.0
    for kind, args in (("compressed", (1e-2, 1e-6, 1e-10, 1e-13)),
                       ("graded", (2.0, 10.0))):
        for a in args:
            X = _perturbed(kind, a)
            r = run_case(f"{kind}_{a:g}", "stretching", X)
            assert not r["silent_corruption"], (
                f"SILENT CORRUPTION on {kind} {a:g}: disagrees with the independent "
                f"reference by {r['rel_vs_ref']:.3e} at spacing ratio "
                f"{r['max_spacing_ratio']:.2e}")
            worst = max(worst, r["rel_vs_ref"], r["slope_rel_vs_ref"])
    print(f"    worst module-vs-reference disagreement over stretched grids: {worst:.2e}")
    assert worst < REL_TOL
    print("[ok] extreme local stretching (ratios to ~1e74): no silent corruption")


def test_exact_duplicate_fails_loudly():
    """An EXACTLY repeated node propagates — it does not return a plausible answer.

    This is the boundary of the graceful-degradation regime and the one place the module
    can do nothing sensible. It must stay loud: 100% non-finite AND warnings raised."""
    X = _perturbed("near_dup", 0.0)
    assert X[X.size // 2 + X.size // 10 + 1] == X[X.size // 2 + X.size // 10]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        H = line_hilbert_matrix(X)
        S = np.array(slope_matrix(X))
    frac_H = (~np.isfinite(H)).mean()
    frac_S = (~np.isfinite(S)).mean()
    print(f"    exact duplicate: H {frac_H:.0%} non-finite, S {frac_S:.0%} non-finite, "
          f"{len(caught)} warnings")
    assert frac_H == 1.0, f"only {frac_H:.0%} of the dense operator went non-finite"
    assert frac_S > 0.0, "the slope operator absorbed an exactly repeated node"
    assert len(caught) > 0, "an exactly repeated node was consumed without a single warning"
    print("[ok] exactly duplicated node: 100% non-finite and warned — propagates, not silent")


def test_slope_sweeps_never_needed_a_pivot():
    """The unpivoted Thomas sweeps match pivoted dense LU on every degenerate grid.

    This is the sharpest form of the slope half of the gate. It holds for a structural
    reason worth recording rather than rediscovering: the interior system has diagonal
    2(h_{i-1}+h_i) against off-diagonals summing to h_{i-1}+h_i, so it is strictly
    diagonally dominant by a factor of exactly 2 FOR EVERY GRID, however degenerate. No
    pivot is ever required, so omitting pivoting cannot cost anything."""
    worst = 0.0
    grids = [("healthy", sinh_grid(N))]
    grids += [(f"near_dup_{a:.0e}", _perturbed("near_dup", a))
              for a in (1e-6, 1e-12, 1e-14, 1e-15)]
    grids += [(f"compressed_{a:.0e}", _perturbed("compressed", a)) for a in (1e-10, 1e-13)]
    grids += [("multi", _perturbed("multi", 1e-11))]
    for tag, X in grids:
        S, Sr = np.array(slope_matrix(X)), ref_slopes_matrix(X)
        rel = np.abs(S - Sr).max() / np.abs(Sr).max()
        assert np.isfinite(S).all(), f"slope operator non-finite on {tag}"
        assert rel < REL_TOL, f"unpivoted sweeps disagree with pivoted LU on {tag}: {rel:.3e}"
        worst = max(worst, rel)
    print(f"    worst |S_thomas - S_pivotedLU| / |S| over 8 grids = {worst:.2e}")
    print("[ok] unpivoted Thomas sweeps == pivoted LU on every degenerate grid")


# ==========================================================================
# 2. CHARACTERIZATION — measured, reported, NOT repaired under leg 96
# ==========================================================================

def test_characterize_association_claim_is_grid_dependent():
    """`slope_matrix`'s "matches the sweeps to 2.7e-13" is a HEALTHY-GRID number.

    `capabilities.py` records the cached slope operator as matching the Thomas sweeps to
    2.7e-13, and `test_line_hilbert.py` gates it at 1e-12 on sinh grids. On a grid with a
    one-ulp cell the same quantity reaches 2.5e-01 — eleven orders worse — because
    ||S||_inf grows from 4.1e+01 to 9.0e+15 and the gemv sums the same terms in a
    different order.

    THE OPERATOR IS NOT LOSING ACCURACY: normalized by ||S||_inf ||f||_inf, which is the
    quantity a backward-stable gemv actually bounds, the disagreement never leaves 1e-16
    across that whole range. What this test pins is that the 2.7e-13 figure MUST NOT be
    read as grid-independent by a consumer that builds its own mesh."""
    rows = []
    for tag, X in (("healthy", sinh_grid(N)),
                   ("near_dup_1e-12", _perturbed("near_dup", 1e-12)),
                   ("near_dup_1e-15", _perturbed("near_dup", 1e-15))):
        f, _ = _clm(X)
        S = np.array(slope_matrix(X))
        ref = natural_spline_slopes(X, f)
        num = np.abs(S @ f - ref).max()
        naive = num / max(np.abs(ref).max(), 1e-300)
        Snorm = np.abs(S).sum(axis=1).max()
        backward = num / max(Snorm * np.abs(f).max(), 1e-300)
        rows.append((tag, naive, backward, Snorm))
        print(f"    {tag:16s} |Sf-sweeps|/|slopes| {naive:.2e}   "
              f"/(|S|inf |f|inf) {backward:.2e}   |S|inf {Snorm:.2e}")
    healthy, worst = rows[0], rows[-1]
    assert healthy[1] < 1e-12, "the healthy-grid association claim has regressed"
    assert worst[1] > 1e-3, (
        "the degenerate-grid disagreement is no longer large — if slope_matrix was "
        "repaired to be grid-robust, DELETE this characterization, do not weaken it")
    assert max(r[2] for r in rows) < 1e-14, (
        "backward error left rounding — this WOULD be a real accuracy loss, not an "
        "artefact of the normalization")
    print("[ok] characterized: the 2.7e-13 association figure is grid-dependent; "
          "backward error is not")


def test_characterize_monotonicity_is_an_unstated_precondition():
    """A DESCENDING grid returns exactly -H(f), finite and plausible, with no flag.

    Out of the leg-96 gate's scope (which names near-duplicates and stretching, not
    ordering) and reported separately rather than as the gate's answer. It is a property
    of the METHOD's orientation convention, not a coding error unique to this module —
    the independent reference sign-flips too — but the module documents no monotonicity
    precondition anywhere, and a caller cannot tell from the output that it was violated.

    Latent, not live: every consumer in the repository (`hl_rescaled`, `gclm_rescaled`,
    `gclm_family`, `bordered_hl`, `weight_search`, `interval_certificate`) builds its grid
    as `sinh` of an ascending `linspace`, so all are strictly increasing today."""
    X = sinh_grid(N)
    f, exact = _clm(X)
    Hasc = line_hilbert_matrix(X) @ f
    Xd = X[::-1].copy()
    fd, _ = _clm(Xd)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        Hdesc = line_hilbert_matrix(Xd) @ fd
    flip = np.abs(Hdesc + Hasc[::-1]).max()
    core = np.abs(Xd) < 5.0
    core[:3] = core[-3:] = False
    rel = np.abs(Hdesc - (2.0 / (1.0 + 4.0 * Xd ** 2)))[core].max() / EXACT_PEAK
    print(f"    descending grid: max|H_desc + H_asc[::-1]| = {flip:.2e}; "
          f"rel error vs the true H(f) = {rel:.3e}; finite={np.isfinite(Hdesc).all()}; "
          f"max|H| = {np.abs(Hdesc).max():.3f}; warnings = {len(caught)}")
    assert np.isfinite(Hdesc).all(), "descending grid now propagates — update this test"
    assert len(caught) == 0, "descending grid now warns — the precondition became explicit"
    assert flip < 1e-13, "the descending-grid answer is no longer the exact negation"
    assert rel > 0.5, "descending grid now gives the right answer — DELETE this test"
    print("[ok] characterized: monotonicity is an unstated precondition; "
          "violating it returns a plausible sign-flipped answer")


def test_characterize_bad_grid_accuracy_is_never_flagged():
    """A grid bad enough to cost 1.3%–29% accuracy still returns a finite, plausible operator.

    This is the honest limit of the NO answer, and it is deliberately kept visible. The
    module carries no grid-quality diagnostic: it faithfully transforms the spline it was
    handed, and the inaccuracy is the spline's own inability to represent the field on
    that mesh. A caller who supplies a bad grid gets a wrong answer that looks fine — the
    module is CORRECT and the answer is still USELESS, and only the caller can tell the
    difference.

    The primary case is the one-ulp grid, where the independent reference is finite on
    100% of entries so the attribution is airtight: 1.3e-02 against the analytic answer,
    4.7e-15 against the reference. Note also the amplified vector-level figure — the two
    implementations' transformed VECTORS differ by ~5e-02 there, which is the conditioning
    (||S||_inf ~ 9e+15) magnifying a rounding-level matrix difference, not either
    implementation being wrong. The gate is about hiding ill-conditioning; nothing is
    hidden, since that norm is visible in the returned operator.

    The one consolation, also pinned: push the grading far enough (r=100) and the failure
    stops being plausible — the peak grows to 141x the true peak, which IS visible."""
    Xu = _perturbed("near_dup", 1e-15)
    fu, exu = _clm(Xu)
    with warnings.catch_warnings(record=True) as caught_u:
        warnings.simplefilter("always")
        Hu = line_hilbert_matrix(Xu) @ fu
    Hur = ref_hilbert_matrix(Xu)
    coreu = np.abs(Xu) < 5.0
    coreu[:3] = coreu[-3:] = False
    ru_exact = np.abs(Hu - exu)[coreu].max() / EXACT_PEAK
    ru_mat = np.abs(line_hilbert_matrix(Xu) - Hur).max() / np.abs(Hur).max()
    ru_vec = np.abs(Hu - Hur @ fu).max() / EXACT_PEAK
    print(f"    one-ulp cell: vs analytic {ru_exact:.3e}, matrix vs reference "
          f"{ru_mat:.3e} (reference finite on {np.isfinite(Hur).mean():.0%}), "
          f"vector vs reference {ru_vec:.3e}, max|Hf| {np.abs(Hu).max():.3f}, "
          f"warnings {len(caught_u)}")
    assert np.isfinite(Hu).all() and len(caught_u) == 0
    assert ru_exact > 1e-3, "the one-ulp grid stopped being inaccurate — re-derive this case"
    assert ru_mat < REL_TOL, (
        "the module and the independent reference now disagree ENTRYWISE here — that "
        "would be a REAL silent corruption and must be escalated, not accommodated")
    assert ru_vec > 10.0 * ru_mat, (
        "the vector-level gap is no longer conditioning-dominated — re-derive the "
        "attribution before trusting this test's reading")

    X = _perturbed("graded", 10.0)
    f, exact = _clm(X)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        Hf = line_hilbert_matrix(X) @ f
    Href = ref_hilbert_matrix(X) @ f
    core = np.abs(X) < 5.0
    core[:3] = core[-3:] = False
    rel_exact = np.abs(Hf - exact)[core].max() / EXACT_PEAK
    # The reference itself underflows on part of this mesh (spacings reach ~1e-72, and
    # its far-field series divides by them), so the comparison is taken where BOTH are
    # finite -- and the finite fraction is printed rather than hidden.
    both = np.isfinite(Hf) & np.isfinite(Href)
    rel_ref = (np.abs(Hf - Href)[both].max()
               / max(np.abs(Href[np.isfinite(Href)]).max(), 1e-300)) if both.any() else np.nan
    print(f"    grading r=10 (spacing ratio {np.diff(X).max()/np.diff(X).min():.1e}): "
          f"vs analytic {rel_exact:.3e}, vs independent reference {rel_ref:.3e} "
          f"(on {both.mean():.0%} of nodes where the reference is finite), "
          f"max|Hf| {np.abs(Hf).max():.3f}, warnings {len(caught)}")
    assert np.isfinite(Hf).all() and len(caught) == 0
    assert rel_exact > 1e-2, "the bad grid stopped being inaccurate — re-derive this case"
    assert rel_ref < REL_TOL, (
        "the module and the independent reference now disagree here — that would be a "
        "REAL silent corruption and must be escalated, not accommodated")

    Xw = _perturbed("graded", 100.0)
    fw, _ = _clm(Xw)
    Hw = line_hilbert_matrix(Xw) @ fw
    print(f"    grading r=100: max|Hf| = {np.abs(Hw).max():.3g} "
          f"({np.abs(Hw).max()/EXACT_PEAK:.0f}x the true peak) — implausible, i.e. visible")
    assert np.abs(Hw).max() > 10.0 * EXACT_PEAK
    print("[ok] characterized: representational error is unflagged and plausible up to "
          "~29%; beyond that the magnitude itself gives it away")


if __name__ == "__main__":
    test_reference_selfcheck()
    test_no_silent_corruption_near_duplicates()
    test_no_silent_corruption_extreme_stretching()
    test_exact_duplicate_fails_loudly()
    test_slope_sweeps_never_needed_a_pivot()
    test_characterize_association_claim_is_grid_dependent()
    test_characterize_monotonicity_is_an_unstated_precondition()
    test_characterize_bad_grid_accuracy_is_never_flagged()
    print("\nAll leg-96 adversarial gates passed: 0 silent corruptions in scope.")
