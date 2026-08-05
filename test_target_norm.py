"""Gates for solver/target_norm.py -- Route-NB, leg 55.

The claims under test are the ones the leg's gate answer rests on, in the order they are
used: the compactification is the SAME map the certificate basis uses, the interpolator
is accurate and its order knob is really wired, the exponent fitter recovers exponents it
was not told, the controls sit on their thresholds, and the far-field closure is a real
choice that really can change the answer.

Gates 14-16 are REGRESSIONS.  The exponent fitter was wrong twice during this leg, both
times returning a plausible number rather than crashing, and both times it was a control
and not a test that caught it.  A check that is not executable decays at the rate of
memory (lesson 68), so both failures are pinned here.
"""

import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, ".")

from solver.hl_rescaled import sinh_grid_origin
from solver.spectral_certificate import (
    coefficient_decay_exponent, moebius_power, sawtooth_coefficients, weight_vector,
)
from solver.target_norm import (
    analytic_tail, calibration_family, clm_anchor_profile, coefficient_magnitudes,
    compactify, fit_exponent, inverse_X_profile, lagrange_interp_uniform,
    midpoint_theta_grid, norm_verdict, sawtooth_exact, sawtooth_profile, spectrum,
    theta_of_X, weighted_partial_sums, X_of_theta,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


# 1 -- the map round-trips, and the precision it loses at large |X| is a REAL LIMIT
# on how far the domain ladder can be pushed, so it is measured rather than assumed:
# at |X| = 3e+05 the image theta sits 6.7e-06 from pi, and float64 tan/arctan lose
# about five digits there.  At the headline domain (|X| = 4.1e+04) it is ~1e-12.
X = np.array([-3.0e5, -745.0, -3.0, -0.2, 0.0, 0.7, 5.0, 1e4])
err = float(np.max(np.abs(X_of_theta(theta_of_X(X)) - X) / np.maximum(np.abs(X), 1.0)))
X_head = np.array([-4.1e4, -745.0, -1.0, 0.0, 1.0, 745.0, 4.1e4])
err_head = float(np.max(np.abs(X_of_theta(theta_of_X(X_head)) - X_head)
                        / np.maximum(np.abs(X_head), 1.0)))
gate("theta <-> X round trip", err < 1e-9 and err_head < 1e-11,
     f"max relative defect {err:.2e} to |X| = 3.0e+05, {err_head:.2e} to the headline "
     "4.1e+04 -- the loss is the float resolution of theta near pi, and it is why the "
     "domain ladder stops where it does")

# 2 -- and it is the SAME half-angle convention spectral_certificate.py uses
worst = 0.0
for x in (Fraction(1, 3), Fraction(2), Fraction(-7, 5), Fraction(11, 2)):
    th = theta_of_X(float(x))
    for k in (1, 3, 7):
        re, im = moebius_power(k, x)
        worst = max(worst, abs(float(re) - np.cos(k * th)),
                    abs(float(im) - np.sin(k * th)))
gate("compactification matches moebius_power", worst < 1e-13,
     f"max |Re w^k - cos k th|, |Im w^k - sin k th| = {worst:.2e} -- the projection "
     "lands in the certificate's basis, not a different one")

# 3 -- the staggered grid never lands on the branch point
ok = all(np.all(np.abs(np.abs(midpoint_theta_grid(M)) - np.pi) > 1e-12)
         and np.all(np.isfinite(X_of_theta(midpoint_theta_grid(M))))
         for M in (16, 1024, 16384))
gate("grid avoids theta = +-pi", ok,
     "X = tan(theta/2) is finite at every sample point for M = 16, 1024, 16384")

# 4 -- the interpolator is exact on polynomials below its order
n_, order_ = 60, 6
i_ = np.arange(n_, dtype=float)
y_ = 3.0 - 0.4 * i_ + 0.02 * i_ ** 2 - 1e-4 * i_ ** 3
t_ = np.array([5.5, 20.25, 41.75])
exact_ = 3.0 - 0.4 * t_ + 0.02 * t_ ** 2 - 1e-4 * t_ ** 3
d4 = float(np.max(np.abs(lagrange_interp_uniform(y_, t_, order=order_) - exact_)))
gate("lagrange exact on cubics at order 6", d4 < 1e-9, f"max defect {d4:.2e}")

# 5 -- THE ORDER KNOB IS REALLY WIRED (an ablation on a dead knob proves nothing)
y2 = np.sin(np.linspace(0.0, 6.0, 201))
t2 = np.array([10.5, 40.3, 150.7])
ex2 = np.sin(t2 * 6.0 / 200.0)
e2 = float(np.max(np.abs(lagrange_interp_uniform(y2, t2, order=2) - ex2)))
e12 = float(np.max(np.abs(lagrange_interp_uniform(y2, t2, order=12) - ex2)))
gate("interpolation order is wired", e2 > 1e-6 and e12 < 1e-12 and e2 > 1e3 * e12,
     f"order 2 errs {e2:.2e}, order 12 errs {e12:.2e} -- ratio {e2 / e12:.1e}")

# 6 -- the two norm conventions bracket each other, so the exponent cannot depend on it
th_ = midpoint_theta_grid(4096)
_, cplx, real = coefficient_magnitudes(calibration_family(X_of_theta(th_), 0.4))
m_ = cplx > 1e-14
lo = float(np.min(real[m_] / cplx[m_]))
hi = float(np.max(real[m_] / cplx[m_]))
gate("complex and real conventions bracket", lo >= 1.0 - 1e-9 and hi <= np.sqrt(2) + 1e-9,
     f"(|a_k|+|b_k|) / 2|c_k| in [{lo:.4f}, {hi:.4f}] subset [1, sqrt2] -- a change of "
     "convention is worth at most sqrt2 in the norm and NOTHING in the exponent")

# 7 -- the flat class IS the algebraic class at s = 0
gate("flat class == algebraic s = 0",
     bool(np.allclose(weight_vector(12, kind="flat"),
                      weight_vector(12, kind="algebraic", param=0.0))),
     "spectral_certificate.weight_vector agrees entry for entry over k = 1..12")

# 8 -- POSITIVE CONTROL, in its pre-registered window (lesson 84)
_, Xa = sinh_grid_origin(801)
hk_a = spectrum(Xa, clm_anchor_profile(Xa), M=8192,
                far_field="power", tail_exponent=-1.0)["hk"]
e1, rest = float(abs(hk_a[0] - 1.0)), float(hk_a[1:].max())
gate("positive control: CLM anchor is exactly one mode", e1 < 1e-10 and rest < 1e-08,
     f"| |h_1| - 1 | = {e1:.2e} (window 1e-10), max_(k>=2) |h_k| = {rest:.2e} "
     "(window 1e-08) -- p = infinity, exact truncation")

# 9 -- NEGATIVE CONTROL 2 matches its CLOSED FORM, not just its exponent
th2 = midpoint_theta_grid(16384)
ks, hs, _ = coefficient_magnitudes(sawtooth_profile(X_of_theta(th2)))
sel = ks <= 512
rel = float(np.max(np.abs(hs[sel] - sawtooth_exact(ks[sel])) / sawtooth_exact(ks[sel])))
gate("sawtooth matches 2/(pi k) in closed form", rel < 2e-3,
     f"max relative defect {rel:.2e} over k <= 512")

# 10 -- and the closed form is the repo's own helper, up to the 2/pi
gate("sawtooth_exact == (2/pi) * sawtooth_coefficients",
     bool(np.allclose(sawtooth_exact(np.arange(1, 9)),
                      (2.0 / np.pi) * sawtooth_coefficients(8))),
     "the leg's control and spectral_certificate.py agree on the same object")

# 11 -- the sawtooth sits on the FLAT class's divergence threshold
p_saw = fit_exponent(ks, hs, 32, 256)["p"]
gate("sawtooth sits at p = 1 (flat threshold)", abs(p_saw - 1.0) < 0.02,
     f"p = {p_saw:.5f} vs 1 exactly -- alpha = 0, a jump, ||.||_(l^1) divergent")

# 12 -- 1/(1+|X|) sits on the s = 1 class's divergence threshold
ki, hi_, _ = coefficient_magnitudes(inverse_X_profile(X_of_theta(th2)))
p_inv = fit_exponent(ki, hi_, 32, 256)["p"]
gate("1/(1+|X|) sits at p = 2 (s = 1 threshold)", abs(p_inv - 2.0) < 0.02,
     f"p = {p_inv:.5f} vs 2 exactly -- and s = 1 is the class the ban clause names")

# 13 -- THE CALIBRATION CURVE: an exponent nobody supplied
cal_worst, cal_rows = 0.0, []
for a in (0.1, 0.3935, 0.6, 1.0):
    kc, hc, _ = coefficient_magnitudes(calibration_family(X_of_theta(th2), a))
    p_c = fit_exponent(kc, hc, 32, 256)["p"]
    cal_worst = max(cal_worst, abs(p_c - 1.0 - a),
                    abs(p_c - (-coefficient_decay_exponent(a))))
    cal_rows.append(f"{a:.4f}->{p_c:.4f}")
gate("calibration family recovers 1 + alpha", cal_worst < 0.02,
     "alpha->p: " + ", ".join(cal_rows) + f"; worst defect {cal_worst:.4f} "
     "(also vs spectral_certificate.coefficient_decay_exponent)")

# 14 -- REGRESSION: an annihilated sub-sequence must not capture the fit
kk = np.arange(1, 4096, dtype=float)
hh = 0.6 * kk ** -2.0
hh[1::2] = 0.0
p_ann = fit_exponent(kk, hh, 32, 1024)["p"]
gate("REGRESSION exact-zero sub-sequence", abs(p_ann - 2.0) < 0.02,
     f"every EVEN mode zeroed, p = {p_ann:.5f} vs 2 -- version 1 of the fitter returned "
     "-0.06 here because it took logs of the zeros")

# 15 -- REGRESSION: and roundoff zeros, which a `> 0` filter does NOT catch
hh2 = 0.6 * kk ** -2.0
hh2[1::2] = 1e-18
p_ann2 = fit_exponent(kk, hh2, 32, 1024)["p"]
gate("REGRESSION roundoff-zero sub-sequence", abs(p_ann2 - 2.0) < 0.02,
     f"every EVEN mode at 1e-18, p = {p_ann2:.5f} vs 2 -- version 2 still returned -0.25 "
     "because one sparse log-bin caught a single such mode")

# 16 -- and a clean power law is still recovered to 5e-3
worst_pl = 0.0
for p_true in (1.0, 1.3935, 2.0, 2.5):
    worst_pl = max(worst_pl,
                   abs(fit_exponent(kk, 0.48 * kk ** (-p_true), 32, 1024)["p"] - p_true))
gate("clean power laws recovered", worst_pl < 5e-3,
     f"worst defect {worst_pl:.2e} over p = 1.0, 1.3935, 2.0, 2.5")

# 17 -- the far-field closure fires only when the grid is too short
_, Xs = sinh_grid_origin(801, rho_max=8.0)
_, Xl = sinh_grid_origin(801, rho_max=12.0)
n_short = compactify(Xs, calibration_family(Xs, 0.4), 16384,
                     far_field="power", tail_exponent=-0.4)[2]
n_long = compactify(Xl, calibration_family(Xl, 0.4), 16384,
                    far_field="power", tail_exponent=-0.4)[2]
gate("closure fires at X_max = 745 and not at 4e+04", n_short > 0 and n_long == 0,
     f"{n_short} sample points outside the short grid, {n_long} outside the long one -- "
     "which is why the headline is measured on the long one")

# 18 -- AND IT REALLY CHANGES THE ANSWER WHEN IT FIRES (lesson 90)
ps = []
for mode in ("power", "clamp", "zero"):
    sp_ = spectrum(Xs, calibration_family(Xs, 0.4), M=16384,
                   far_field=mode, tail_exponent=-0.4)
    ps.append(fit_exponent(sp_["k"], sp_["hk"], 32, 256)["p"])
gate("closure changes p when it fires", max(ps) - min(ps) > 0.02,
     f"power/clamp/zero give p = {ps[0]:.4f} / {ps[1]:.4f} / {ps[2]:.4f}, spread "
     f"{max(ps) - min(ps):.4f} -- this ablation is not a tautology of the code")

# 19 -- and 'none' refuses to guess
_, h_none, n_none = compactify(Xs, calibration_family(Xs, 0.4), 16384, far_field="none")
raised = False
try:
    coefficient_magnitudes(h_none)
except ValueError:
    raised = True
gate("far_field='none' refuses to invent data",
     n_none > 0 and int(np.isnan(h_none).sum()) == n_none and raised,
     f"{n_none} points left NaN and the transform refuses them")

# 20 -- partial sums reduce to a plain sum at s = 0
kp = np.arange(1, 65, dtype=float)
hp = 1.0 / kp ** 2
got = weighted_partial_sums(kp, hp, 0.0, [8, 64])
gate("partial sums reduce at s = 0",
     abs(got[0]["S_N"] - hp[:8].sum()) < 1e-14 and abs(got[1]["S_N"] - hp.sum()) < 1e-14,
     f"S_8 = {got[0]['S_N']:.6f}, S_64 = {got[1]['S_N']:.6f}")

# 21 -- the tail REFUSES to bound a divergent sum (lesson 73)
div = analytic_tail(p=1.3935, C=0.5, N=1024, s=1.0)
fin = analytic_tail(p=1.3935, C=0.5, N=1024, s=0.3)
gate("divergent tail has no value, and says so",
     div["finite"] is False and div["bound"] is None and fin["finite"] is True
     and fin["bound"] > 0.0,
     f"s = 1 -> {div['reason']}; s = 0.3 -> bound {fin['bound']:.4f}")

# 22 -- and where it is finite it DOMINATES the true remainder
kt = np.arange(1, 200_000, dtype=float)
ht = 0.5 * kt ** -1.4
dom = all(analytic_tail(1.4, 0.5, 1024, s)["bound"]
          > float(((1.0 + kt[kt > 1024]) ** s * ht[kt > 1024]).sum()) for s in (0.0, 0.3))
gate("analytic tail dominates the true remainder", dom,
     "checked at s = 0 and s = 0.3 against the summed remainder to k = 2e+05")

# 23 -- the verdict is a MARGIN, not a boolean
v = norm_verdict(1.3963, 0.3, alpha=0.3978)
gate("verdict reports a magnitude", v["finite"] is True
     and abs(v["margin_in_exponent_units"] - 0.0963) < 1e-9
     and norm_verdict(1.3963, 1.0)["finite"] is False,
     f"s = 0.3 margin {v['margin_in_exponent_units']:+.4f} in exponent units; "
     "s = 1 finite = False")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
sys.exit(1 if n_fail else 0)
