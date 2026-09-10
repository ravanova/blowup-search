"""Self-running checks for experiments/arc6_profile_v1.py (arc 6, R5(i), leg 430).

    .venv/bin/python test_arc6_profile_v1.py

PLANTED CONTROLS, as pre-registered in experiments/journal/leg_430_prereg.md §3:
C1 and C3 fire; C5 and C6 DID NOT FIRE and the test asserts the measured
reason (leg_430.md §3, CORRECTIONS §69) — C2 was not run (see the journal); on a coarse grid (dy = 8e-3, 9 eta
points) so the whole file runs in about two minutes. The gate numbers of the
banked artefact are checked by writeup/arc6_profile_evidence.py, not here.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent / "experiments"))
import arc6_profile_v1 as P  # noqa: E402

_fails = []


def check(ok, label):
    print(f"  [{'ok' if ok else 'FAIL'}] {label}")
    if not ok:
        _fails.append(label)


KW = dict(lam=0.1, dy=8e-3, n_eta=8, verbose=False)

print("== the schedule refuses a violated parameter order (A.6)")
try:
    P.Schedule(1.0, 0.1, 1e-5, 10.0, 0.1)   # h = 1e-5 > e^{-T_d} = 3e-6
    check(False, "h = 1e-5 > e^{-T_d} must be refused")
except AssertionError:
    check(True, "h = 1e-5 > e^{-T_d} is refused")
sch = P.Schedule(1.0, 0.1, 1e-7, 10.0, 0.1)
check(abs(sch.T_d - (np.e + 10)) < 1e-12 and sch.P_star > np.exp(sch.T_d), "T_d = e^{M_d} + 10, P_* > e^{T_d}")
check(abs(sch.T_w - 60 * np.log(10)) < 1e-9, "T_w = 60 log(1/lambda)")
check(sch.k_axial(np.array([sch.T_d - 11.0, sch.T_d]))[0] == 0.0, "k vanishes on the final eleven units of the axial stage")

print("== the smooth step and the pulse shape")
y = np.linspace(-1, 2, 3001)
s = P.sigma(y)
check(s[y <= 0].max() == 0.0 and s[y >= 1].min() == 1.0 and np.all(np.diff(s[(y > 0) & (y < 1)]) >= 0), "sigma is 0 for y<=0, 1 for y>=1, monotone between")
check(abs(P.sigma(np.array([0.5]))[0] - 0.5) < 1e-14, "sigma(1/2) = 1/2 by symmetry")
xi = np.linspace(0, 13, 13001)
R0 = sch.R0(xi)
check(R0.min() >= 0 and R0[xi > 12.5].max() < 1e-12 and abs(R0[np.argmin(np.abs(xi - 5))] - 4.99) < 1e-6, "R_0 >= 0, cut off after xi = 10, equals xi - .01 on the plateau")
check(np.max(np.gradient(R0, xi)) <= 1.2, "d R_0/d xi <= 1.2 (the paper's bound, p. 136)")

print("== baseline (the twin every control is compared with)")
base = P.build(**KW)
gb = P.gates(base)
check(0.20 < base["G1"]["K_b"] <= 0.25, f"G1 K_b = {base['G1']['K_b']:.4f} in (.20, .25]")
check(gb["G2"][0] == "YES", "G2 bracket values as printed on p. 133")
check(gb["G6"][0] == "YES", "G6 exponents on the reserved patches and in the tail")
check(gb["G8"][0] == "YES", "G8 pressure datum bound (A.22)")
check(base["G7"]["int"]["min_vs_minus_2"] > 0.19, "v_s - 2 = 2 lambda on the intermediate interval")
check(base["G4"]["M_pulse_end_over_bump_centre_scale"] < 1e-6 and base["G4"]["rI_hold_end_minus_target"] < 1e-8, "pulse-end moments cancel at the bump-centre scale; (A.11) hits its target")
check(gb["G3"][0] == "NO" and base["G3"]["n_nan"] == 9, "at lambda = 0.1 the bracket [.9, 1.2] holds NO root (the finding, not a defect of the twin)")

print("== C1: flipping the sign of lambda on the intermediate interval breaks v_s > 2 (MUST fail)")
c1 = P.build(flip_lambda=True, **KW)
check(c1["G7"]["int"]["min_vs_minus_2"] < 0, f"v_s - 2 = {c1['G7']['int']['min_vs_minus_2']:.3f} < 0")
check(P.gates(c1)["G6"][0] == "NO", "G6's patch exponent -1/2 - lambda also fails under the flip")

print("== C3: dropping c_1, c_2 leaves M, J nonzero at pulse end (MUST fail)")
c3 = P.build(drop_c12=True, **KW)
check(c3["G4"]["M_pulse_end_over_bump_centre_scale"] > 1e-3, f"M at pulse end / bump-centre scale = {c3['G4']['M_pulse_end_over_bump_centre_scale']:.3e} > 1e-3")

print("== C5: dropping the (A.11) bumps — pre-registered to fail G4/G5; it DID NOT FIRE (leg_430.md §3): the hold relaxes I/(XH) to 1/(1-lambda) before the bumps act, so their coefficients are ~1e-14 and dropping them changes nothing measurable")
c5 = P.build(drop_A11=True, **KW)
check(max(abs(x) for x in base["G4"]["cb"]) < 1e-10, f"the fitted (A.11) bump coefficients are numerically null: {base['G4']['cb']}")
check(c5["G4"]["rI_hold_end_minus_target"] < 1e-8 and abs(c5["G5"]["angular_moment_integral_over_abs"] - base["G5"]["angular_moment_integral_over_abs"]) < 1e-8,
      f"without the bumps rI - 1/(1-lambda) = {c5['G4']['rI_hold_end_minus_target']:.3e} and the angular measure is unchanged ({c5['G5']['angular_moment_integral_over_abs']:.3e} vs {base['G5']['angular_moment_integral_over_abs']:.3e}) — the control cannot fire on this schedule")

print("== C6: truncating R_0 at xi = 5 — pre-registered to fail G1 or G2; it DID NOT FIRE (leg_430.md §3): the e^{-2 xi} weight makes xi in [5, 10] worth ~e^{-10} of K_b")
c6 = P.build(R0_cut=5.0, **KW)
g6 = P.gates(c6)
check(g6["G1"][0] == "YES" and g6["G2"][0] == "YES" and 0 < base["G1"]["K_b"] - c6["G1"]["K_b"] < 1e-3,
      f"K_b = {c6['G1']['K_b']:.5f} vs {base['G1']['K_b']:.5f} (shift {base['G1']['K_b'] - c6['G1']['K_b']:.2e} < 1e-3); G1 {g6['G1'][0]}, G2 {g6['G2'][0]} — the control cannot fire")
_w = np.exp(-2 * xi) * R0 ** 2
_lo, _hi = np.trapezoid(_w[(xi >= 6) & (xi <= 10)], xi[(xi >= 6) & (xi <= 10)]), np.trapezoid(_w[xi >= 5], xi[xi >= 5])
check(_lo <= base["G1"]["K_b"] - c6["G1"]["K_b"] <= _hi, f"and the shift lies between the weighted tail integrals over [6, 10] and [5, inf): {_lo:.3e} <= {base['G1']['K_b'] - c6['G1']['K_b']:.3e} <= {_hi:.3e} (the cut is the smooth step 1 - sigma(xi - 5))")

print()
if _fails:
    print(f"FAILED {len(_fails)}:"); [print("  -", f) for f in _fails]; sys.exit(1)
print("test_arc6_profile_v1: all checks pass")
