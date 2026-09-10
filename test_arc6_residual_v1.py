"""Self-running checks for experiments/arc6_residual_v1.py (arc 6, R5(ii), leg 432).

    .venv/bin/python test_arc6_residual_v1.py

The planted controls of leg_432_prereg.md §3 and its amendment (K6), on a coarse grid
(dy = 4e-3, 9 eta points, h = 1e-3), each against its unmodified twin. The banked gate
numbers are checked by writeup/arc6_residual_evidence.py, not here.
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent / "experiments"))
import arc6_residual_v1 as R  # noqa: E402

_fails = []
def check(ok, label):
    print(f"  [{'ok' if ok else 'FAIL'}] {label}")
    if not ok: _fails.append(label)

KW = dict(h=1e-3, dy=4e-3, n_eta=8)
print("== the tail cutoff (A.12) and its flat factorisation")
T = R.Tail(1e-3)
y = np.linspace(0, 3.5, 3501); d = 3 - y
check(np.all(T.psi(y[y <= 1]) == 1.0) and np.all(T.psi(y[y >= 3]) == 0.0) and np.all(np.diff(T.psi(y)) <= 1e-12), "psi_o = 1 on [0,1], 0 beyond 3, non-increasing")
m = (y > 1) & (y < 2.9)
check(np.allclose(T.psi_hat(y[m]) * np.exp(-4 / d[m] ** 2), T.psi(y[m]), rtol=1e-12), "psi_hat e^{-4/delta^2} = psi_o")
g0 = T.psi_hat(np.array([2.999]))[0]
check(abs(g0 - np.e) < 0.01, f"g(delta) -> e as delta -> 0: g(0.001) = {g0:.4f}")
fh = T.fop_hat(np.array([2.95])); check(abs(fh[0] * 0.05 ** 3 / (8 * T.rho * np.e) - 1) < 0.2, "f_o' hat ~ 8 rho e / delta^3 near the edge (p. 143)")
check(abs(T.integral(np.array([2.0]), 0.0, lambda yp: np.ones_like(yp))[0] - (np.exp(4 / 1.0 ** 2) * 0 + (lambda: __import__('scipy.integrate', fromlist=['quad']).quad(lambda t: np.exp(4 / 1 - 4 / (3 - t) ** 2), 2.0, 3.0)[0])())) < 1e-8, "the v-substituted tail integral matches scipy.quad on a smooth test integrand")

print("== baseline (the twin)")
base = R.build(**KW); gb = R.gates(base)
check(all(v[0] == "YES" for v in gb.values()), f"all eight gates YES on the coarse grid: { {k: v[0] for k, v in gb.items()} }")
check(abs(base["H4"]["fop_over_fo_max_over_h"] - 0.4) < 0.01, f"f_o'/f_o max = {base['H4']['fop_over_fo_max_over_h']:.3f} h at c_o = 0.1 — above the paper's h/4 (leg 430's prereg claimed otherwise; leg_432.md)")

print("== K1: polynomial cutoff (no flat factor) — H7's slope test and H2 MUST fail")
c1 = R.build(cutoff="poly", **KW); g1 = R.gates(c1)
check(g1["H7"][0] == "NO" and abs(c1["H7"]["delta3_dlogT_ddelta_at_0.05"] - 8) > 1, f"delta^3 d log T/d delta = {c1['H7']['delta3_dlogT_ddelta_at_0.05']:.3f}, not 8")
check(g1["H2"][0] == "NO", "H2 fails: the boundary term does not factor as e^{-4/delta^2} delta^{-3}")

print("== K2: D = A in the axial scaling — H6 (q-invariance of T_z) MUST fail")
c2 = R.build(D_wrong=True, **KW); g2 = R.gates(c2)
check(g2["H6"][0] == "NO" and c2["H6"]["1000.0"]["Tz_rel"] > 1e-4 and c2["H6"]["1000.0"]["Ttheta_rel"] < 1e-10, f"T_z changes by {c2['H6']['1000.0']['Tz_rel']:.2e} between q = 1 and 1000 (~2h log q); T_theta does not")

print("== K3: a residual angular moment — H7 (vanishing beyond X_b) MUST fail")
c3 = R.build(eps_moment=1e-3, **KW); g3 = R.gates(c3)
check(g3["H7"][0] == "NO" and c3["H7"]["A_beyond_Xb"] == 1e-3, "A(y >= 3) = eps != 0")

print("== K4: reversed cutoff — H1 (positivity) MUST fail")
c4 = R.build(flip=True, **KW); g4 = R.gates(c4)
check(g4["H1"][0] == "NO" and c4["H1"]["min_A"] < 0, f"min A = {c4['H1']['min_A']:.3e} < 0")

print("== K5: h -> -h — H4 (the shear bracket) MUST fail")
c5 = R.build(**{**KW, "h": -1e-3}); g5 = R.gates(c5)
check(g5["H4"][0] == "NO" and c5["H4"]["a_minus_2_max"] > 2 * c5["H4"]["h"], f"a - 2 in [{c5['H4']['a_minus_2_min']:.2e}, {c5['H4']['a_minus_2_max']:.2e}] is not <= 2h = {2 * c5['H4']['h']:.2e}")

print("== K6: no heat factor — H7 MUST fail with B(y >= 3) = -(2+2h)")
c6 = R.build(heat=False, **KW); g6 = R.gates(c6)
check(g6["H7"][0] == "NO" and abs(c6["H7"]["B_beyond_Xb"] + (2 + 2e-3)) < 1e-12, f"B beyond X_b = {c6['H7']['B_beyond_Xb']:.6f}")
check(R.gates(c6)["H0"][0] == "NO" and c6["H0"]["A_rel"] < 1e-6, "and (A.54), which presupposes the heat solution, no longer matches (4.11): the routes differ by the power law's viscous term while the inviscid bracket still agrees")

print()
if _fails:
    print(f"FAILED {len(_fails)}:"); [print("  -", f) for f in _fails]; sys.exit(1)
print("test_arc6_residual_v1: all checks pass")
