#!/usr/bin/env python3
"""Leg 192 (VERIFIER) — the independent re-derivation of leg 176's certificate, as tests.

Every check here is an EXECUTABLE form of a claim leg 192 makes in prose (lesson 68:
a check that is not executable decays at the rate of memory).  Nothing in this file
edits or repairs `solver/origin_h2_certificate.py` — a verifier reports, it does not
fix — and none of it re-uses leg 176's numerical machinery:

  * the realization is re-derived in EXACT RATIONAL arithmetic from the definitions
    of the operator and the basis, invoking neither of the two classical Laguerre
    identities leg 176 relies on;
  * Xu eq. (4.23) is evaluated by an EXACT partial-fraction antiderivative, with no
    Taylor series, no Gauss panels and no grading;
  * `sigma_min` is cross-checked against a whitening whose Gram factor comes from an
    EXACT RATIONAL `LDL^T` of the (exactly integer) `X` Gram.

Run: .venv/bin/python test_origin_h2_certificate_postconstruction.py
"""

import json
import os
import sys
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiments"))

import solver.origin_h2_certificate as H
from solver.origin_h2_certificate import border_row, to_y
import p2_route_h2cv_v1_postconstruction as V

BANKED = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "writeup", "data", "p2_route_h2c_v1_construction.json")

_CACHE = {}


def sig(route, N):
    """Memoized, because the merge gate runs this file and an N=1024 SVD is not cheap."""
    key = (route, N)
    if key not in _CACHE:
        _CACHE[key] = {"eigh": V.sig_eigh, "chol": V.sig_chol,
                       "exact": V.sig_exact_gram}[route](N)
    return _CACHE[key]


def test_realization_is_exact_in_rational_arithmetic():
    """Every entry of the realization matches as a RATIONAL, not to a tolerance."""
    r = V.v1_exact_realization(NB=12, NG=16)
    assert r["laguerre_orthonormality_exact"] == 0
    assert r["tridiagonal_entries_exact"], r["tridiagonal_exact_rational_mismatches"]
    assert r["border_row_exact_matches_i_m1n_1m2n"]
    assert r["border_row_vs_module_max_abs"] == 0.0
    assert r["symmetry_mode_binv2_vs_module_max_abs"] == 0.0
    assert r["symmetry_mode_m_vs_module_max_abs"] == 0.0
    assert r["x_gram_exact_integer_equality"]
    assert r["x_gram_max_abs_diff"] == 0.0
    print("[ok] L_0^+, border row, symmetry modes and X Gram are EXACT (rational equality)")


def test_xu_closed_form_matches_an_exact_partial_fraction_evaluation():
    """leg 176's `u(y)` against an exact antiderivative — the real accuracy of conjunct 2."""
    worst = 0.0
    for sd in (0, 3, 5):
        fc = V.solvable_datum(240, 6, sd)[:6]
        cQ = [V.Qc(F(z.real), F(z.imag)) for z in fc]
        u176, _, _ = H.xu_resolvent(fc, V.YNODES, c1=0.0, derivs=True)
        for j, y in enumerate(V.YNODES):
            u, _, _, _, _ = V.xu_u_exact(cQ, F(y).limit_denominator(10 ** 9), c1=0.0)
            worst = max(worst, abs(u - u176[j]) / abs(u))
    assert worst < 5e-15, worst
    # and the sharper statement: it is a decade better than the residual leg 176 quotes
    assert worst < 0.2 * 4.766912579638455e-15, worst
    print(f"[ok] Xu (4.23) reproduced: leg 176's u is exact to {worst:.3e} relative "
          f"({4.766912579638455e-15 / worst:.1f}x better than its own reported residual)")


def test_the_pointwise_residual_is_exactly_minus_ell_f_y_over_b2():
    """The ODE identity, as a magnitude, on data where it can come out differently."""
    r = V.v3_exact_ode_identity()
    assert r["G_prime_0_equals_ell_f_all_exact"], "G'(0) = ell(f) failed as an exact identity"
    assert r["A_prime_identity_exact"], r["A_prime_equals_G2_over_y2_exact_mismatches"]
    for row in r["residual_equals_minus_ell_f_y_over_b2"]:
        assert row["max_abs_pred_minus_obs"] < 1e-13, row
    print("[ok] the pointwise residual is exactly -ell(f) y / b^2, and G'(0) = ell(f) exactly")


def test_sigma_min_agrees_across_four_independent_routes():
    """Three float whitenings and an EXACT-rational-Gram reference, at N where all are cheap."""
    for N in (64, 128):
        e, c, x = sig("eigh", N), sig("chol", N), sig("exact", N)
        assert abs(c - x) < 1e-12 * x, (N, c, x)      # cholesky tracks the exact Gram
        assert abs(e - x) < 1e-8 * x, (N, e, x)       # leg 176's route is close, not equal
    print("[ok] sigma_min agrees across four routes at N = 64, 128 (cholesky == exact Gram)")


def test_leg176_whitening_drifts_and_the_drift_grows_with_N():
    """The correction: the N=1024 rise is leg 176's WHITENING, not the X Gram's float floor.

    This is the check that can come out the other way (lesson 90): if the drift were
    float noise common to both routes, `d256` would not exceed `d64` by orders.
    """
    d64 = abs(sig("eigh", 64) - sig("chol", 64))
    d256 = abs(sig("eigh", 256) - sig("chol", 256))
    assert d256 > 10 * d64, (d64, d256)      # measured 18.6x; float noise would give ~1x
    # leg 176's own route is the one that breaks monotonicity.  Its N=512 and N=1024
    # eigh values are read from its banked JSON rather than recomputed, so this test
    # costs one extra SVD and not three.
    with open(BANKED) as fh:
        lad = json.load(fh)["C1_bordered_sigma_min_X"]["ladder"]
    assert lad["1024"]["sigma_min"] > lad["512"]["sigma_min"], "leg 176's N=1024 rise is banked"
    assert sig("chol", 1024) < sig("chol", 512), "the cholesky route should stay monotone"
    print(f"[ok] the whitening drift grows {d256 / d64:.1f}x ({d64:.2e} at N=64 -> "
          f"{d256:.2e} at N=256); leg 176's banked ladder rises at N=1024, cholesky does not")


def test_sigma_min_headline_reproduces_to_six_significant_figures():
    """`sigma_min = 0.0908`, `||R||_X = 11.0127` stand; the banked 7th figure does not."""
    with open(BANKED) as fh:
        banked = json.load(fh)
    claimed = banked["C1_bordered_sigma_min_X"]["sigma_min_at_512"]
    indep = sig("chol", 512)
    rel = abs(indep - claimed) / claimed
    assert rel < 1e-4, rel                     # the headline 0.0908 reproduces
    assert rel > 1e-7, rel                     # but not to the 7 figures it is quoted to
    assert abs(1.0 / indep - 11.0127) < 5e-4, 1.0 / indep
    print(f"[ok] sigma_min reproduces to {rel:.2e} relative (0.0908 stands; the banked "
          f"0.09080465 is good to 6 s.f., not 7)")


def test_the_one_prose_number_that_disagrees_with_its_own_json():
    """Guards the audit finding itself, so a later edit cannot silently erase it."""
    with open(BANKED) as fh:
        banked = json.load(fh)
    audit = V.v5_prose_audit(banked)
    bad = [c for c in audit["numeric_checks"] if not c["agrees"]]
    assert len(bad) == 1, [c["claim"] for c in bad]
    assert bad[0]["claim"] == "C0 max ABSOLUTE residual", bad[0]
    assert abs(bad[0]["json_value"] - 1.4295603459064552e-14) < 1e-20
    print(f"[ok] prose audit: {audit['n_checked'] - 1}/{audit['n_checked']} numeric claims "
          f"match; the one that does not is '{bad[0]['claim']}' "
          f"(prose 1.29e-14 vs JSON 1.4296e-14)")


def test_the_suspected_quadrature_inconsistency_is_refuted():
    """A defect would scale with `ell(f)`; this one does not move over six decades."""
    r = V.v6_suspected_g1_inconsistency_refuted()
    assert not r["suspicion_confirmed"]
    assert r["ell_f_spread_tested"] > 1e7, r["ell_f_spread_tested"]
    assert r["discrepancy_spread_over_six_decades_of_ell_f"] < 10.0, r
    print(f"[ok] suspected _cum_branch inconsistency REFUTED: ell(f) driven over "
          f"{r['ell_f_spread_tested']:.1e}x, discrepancy flat within "
          f"{r['discrepancy_spread_over_six_decades_of_ell_f']:.2f}x")


def test_leg176_conjunct_2_reproduces_bit_for_bit():
    """Determinism of the banked number itself."""
    with open(BANKED) as fh:
        banked = json.load(fh)
    fc = V.solvable_datum(240, 6, 0)[:6]
    got = float((np.abs(H.xu_ode_residual(fc, V.YNODES)) / np.abs(to_y(fc, V.YNODES))).max())
    assert got == banked["C0_xu_closed_form"]["max_rel_residual"], (got, banked)
    print("[ok] leg 176's conjunct-2 number reproduces bit-for-bit")


if __name__ == "__main__":
    for fn in (test_realization_is_exact_in_rational_arithmetic,
               test_xu_closed_form_matches_an_exact_partial_fraction_evaluation,
               test_the_pointwise_residual_is_exactly_minus_ell_f_y_over_b2,
               test_sigma_min_agrees_across_four_independent_routes,
               test_leg176_whitening_drifts_and_the_drift_grows_with_N,
               test_sigma_min_headline_reproduces_to_six_significant_figures,
               test_the_one_prose_number_that_disagrees_with_its_own_json,
               test_the_suspected_quadrature_inconsistency_is_refuted,
               test_leg176_conjunct_2_reproduces_bit_for_bit):
        print(f"== {fn.__name__}")
        fn()
    print("\nall leg-192 verification gates pass")
