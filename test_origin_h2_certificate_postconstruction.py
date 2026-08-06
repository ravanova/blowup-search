#!/usr/bin/env python3
"""Tests for leg 249's INDEPENDENT VERIFICATION of leg 176's origin-`H^2` certificate.

These pin the VERIFIER's own machinery, not leg 176's -- `test_origin_h2_certificate.py`
already covers the module.  What has to be trustworthy here is different: the
exact-rational re-derivation, the realification that makes it affordable, the
inertia bracketing, and the quadrature that ties the Gram to Xu's Definition 4.1.

Self-running script, per this repo's convention:  .venv/bin/python test_origin_h2_certificate_postconstruction.py
"""

import math
import os
import sys
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiments"))

import solver.origin_h2_certificate as H
import p2_route_h2cv_v1_postconstruction as V

FAILS = []


def check(name, cond, detail=""):
    ok = bool(cond)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'  ' + detail if detail else ''}")
    if not ok:
        FAILS.append(name)


def approx(name, got, want, tol):
    rel = abs(got - want) / max(abs(want), 1e-300)
    check(name, rel <= tol, f"got {got:.12g} want {want:.12g} rel {rel:.2e} tol {tol:.1e}")


print("T1  the exact-rational realization reproduces the module EXACTLY")
Lc = V.lag_coeffs(12)
mism = []
for n in range(8):
    tot = V.l0_column_poly(Lc[n])
    for m in range(11):
        got = V.int_e1(V.pmul(tot, Lc[m]))
        want = F(0)
        if m == n - 1: want = F(-n, 2)
        if m == n:     want = F(1, 2)
        if m == n + 1: want = F(n - 1, 2)
        if got != want: mism.append((m, n))
check("L_0^+ tridiagonal entries are exact rationals, derived by calculus", not mism,
      f"{len(mism)} mismatches")
ell_ex = [V.int_ehalf(V.padd(Lc[n], [F(0)] + [-c * F(1, 4) for c in Lc[n]]))
          for n in range(10)]
check("border row equals i(-1)^n(1-2n) exactly",
      all(ell_ex[n] == F((-1) ** n * (1 - 2 * n)) for n in range(10)))
check("border row matches the module", float(np.abs(
    H.border_row(10) - 1j * np.array([float(v) for v in ell_ex])).max()) == 0.0)

bad = []
for m in range(12):
    for n in range(m, 12):
        pr = V.pmul(Lc[m], Lc[n])
        val = V.int_e1(V.padd(pr, [F(0)] * 4 + pr))
        if val != F(int(round(H.x_gram(12)[m, n]))): bad.append((m, n))
check("X Gram = I + J^4 as exact integers", not bad, f"{len(bad)} mismatches")

print("T2  the y-space identity, exactly, from Xu (4.21) -- a disjoint second proof")
r = V.w1b_y_space_identity(NB=10)
check("L_0^+ phi_n = -(n/2)phi_{n-1} + (1/2)phi_n + ((n-1)/2)phi_{n+1} exactly",
      r["exact_identity_holds"], f"{len(r['mismatches'])} mismatches")
check("the transform pair reproduces the module's to_y",
      r["transform_pair_vs_module_to_y_max_rel"] < 1e-12,
      f"{r['transform_pair_vs_module_to_y_max_rel']:.2e}")
check("two independent 2nd-derivative derivations agree",
      r["second_derivative_two_derivations_max_rel"] < 1e-11,
      f"{r['second_derivative_two_derivations_max_rel']:.2e}")

print("T3  the Gram IS Xu Definition 4.1's X norm (the link leg 176 never checked)")
w2 = V.w2_gram_is_the_x_norm(nmax=6)
check("L^2 orthonormality with constant 2 pi",
      w2["l2_orthonormality_max_abs_defect_over_2pi"] < 1e-12,
      f"{w2['l2_orthonormality_max_abs_defect_over_2pi']:.2e}")
check("the second-derivative Gram is 2 pi J^4",
      w2["second_derivative_gram_max_rel_defect"] < 1e-10,
      f"{w2['second_derivative_gram_max_rel_defect']:.2e}")
check("CONTROL: dropping the 2 pi breaks the identity by ~6.28x (so the test can fail)",
      w2["control_wrong_constant_rel_error_if_2pi_omitted"] > 0.8,
      f"{w2['control_wrong_constant_rel_error_if_2pi_omitted']:.3f}")

print("T4  the realification is a unitary change of variable, so it moves nothing")
N = 48
Nr = N + 2
Ax = np.zeros((Nr + 1, N + 1), dtype=complex)
Ax[:Nr, :N] = H.l0_plus(Nr)[:, :N]
Ax[:Nr, N] = H.symmetry_modes(Nr)[1]
Ax[Nr, :N] = H.border_row(N)
wv, U = np.linalg.eigh(H.bordered_gram(N, H.x_gram(N)))
Gdih = (U * (1.0 / np.sqrt(wv))) @ U.T
wv, U = np.linalg.eigh(H.bordered_gram(Nr, H.x_gram(Nr)))
Gch = (U * np.sqrt(wv)) @ U.T
sig_cplx = float(np.linalg.svd(Gch @ Ax @ Gdih, compute_uv=False).min())
approx("complex (module) and realified (mine) sections give the same sigma_min",
       V.sig_eigh(N), sig_cplx, 1e-11)

print("T5  the exact inertia test brackets sigma_min, and is falsifiable")
# NOTE the tolerance: the enclosure is exact to ~1e-15 while the FLOAT value it is
# compared against carries its own rounding, so the right check is agreement to
# float accuracy, not strict containment of a number that has its own error bar.
for N in (16, 32):
    s = V.sig_chol(N)
    lo, hi = V.sigma_enclosure(N, sig_float=s, half=1e-6, nbis=30)
    mid = 0.5 * (lo + hi)
    check(f"bordered N={N}: exact enclosure agrees with the float value",
          abs(mid - s) < 1e-12, f"[{lo:.14f}, {hi:.14f}] vs float {s:.14f}")
    check(f"bordered N={N}: enclosure is tight", hi - lo < 1e-9, f"width {hi-lo:.2e}")

s_tail = V.sig_chol(64, lo=2, bordered=False)
lo, hi = V.sigma_enclosure(64, lo=2, bordered=False, sig_float=s_tail, half=1e-6, nbis=30)
check("tail N=64: exact enclosure agrees with the float value",
      abs(0.5 * (lo + hi) - s_tail) < 1e-12,
      f"[{lo:.14f}, {hi:.14f}] vs float {s_tail:.14f}")

P, v, Gd, nd = V.build_exact(32, 0, True)
lam_below = F(int(round((V.sig_chol(32) * 0.9) ** 2 * 2 ** 52)), 1 << 52)
lam_above = F(int(round((V.sig_chol(32) * 1.1) ** 2 * 2 ** 52)), 1 << 52)
check("CONTROL: the inertia test says PD below sigma_min^2",
      V._is_pd(P, v, Gd, lam_below, nd, F(1), True) is True)
check("CONTROL: and NOT PD above it (so it can come out either way)",
      V._is_pd(P, v, Gd, lam_above, nd, F(1), True) is False)

print("T6  the sparse LDL agrees with a dense eigenvalue computation")
N = 24
P, v, Gd, nd = V.build_exact(N, 0, True)
S = np.zeros((nd, nd)); G = np.zeros((nd, nd))
for i in range(nd):
    for j, x in P[i].items(): S[i, j] = S[j, i] = float(x)
    for j, x in Gd[i].items(): G[i, j] = G[j, i] = float(x)
vv = np.array([float(x) for x in v])
S = S + np.outer(vv, vv)
A, Gdf, Gcf = V.my_section_float(N)
approx("the exact S reconstructs A^T Gc A", float(np.abs(S - A.T @ Gcf @ A).max()) + 1.0,
       1.0, 1e-12)
Rg = np.linalg.cholesky(G)
lam_min = float(np.linalg.eigvalsh(
    np.linalg.solve(Rg, np.linalg.solve(Rg, S).T).T).min())
approx("lambda_min of the exact pencil = sigma_min^2 of the float section",
       math.sqrt(lam_min), V.sig_chol(N), 1e-10)

print("T7  Xu (4.23): the pointwise residual is exactly -ell(f) y / b^2")
w6 = V.w6_xu_closed_form()
check("G'(0) = ell(f) as an exact rational identity",
      w6["G_prime_0_equals_ell_f_exactly"])
check("leg 176's u(y) matches the exact partial-fraction u(y)",
      w6["worst_rel_diff_leg176_u_vs_exact_closed_form"] < 1e-13,
      f"{w6['worst_rel_diff_leg176_u_vs_exact_closed_form']:.3e}")
rows = w6["residual_equals_minus_ell_f_y_over_b2"]
scaled = [r for r in rows if r["perturbation"] > 0]
check("CONTROL: driving ell(f) over 6 decades leaves the discrepancy flat "
      "(a real defect would grow by 1e8)",
      w6["discrepancy_spread_over_six_decades_of_ell_f"] < 100.0,
      f"spread {w6['discrepancy_spread_over_six_decades_of_ell_f']:.2f}x over "
      f"{max(r['abs_ell_f'] for r in scaled)/min(r['abs_ell_f'] for r in scaled):.1e}x in ell(f)")

print("T8  the ladder shape leg 176 reports, reproduced from my own matrices")
for N, want in ((8, 0.0927566), (16, 0.0911590), (32, 0.0909310), (64, 0.0908878)):
    approx(f"sigma_min at N={N} matches leg 176's published table", V.sig_chol(N), want, 1e-6)
s512_note = "N=512 is checked in the runner, not here (38 s)"
print(f"  note  {s512_note}")

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} -> {FAILS}")
    sys.exit(1)
print("ALL PASS")
