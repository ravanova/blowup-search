"""Gates for solver/spectral_certificate.py -- the certificate in the compactified basis.

The claims under test are the ones the leg's conclusion rests on, in the order they are
used: the basis algebra is exact, the anchor is an exact zero, the tail operator has no
diagonal, the divergence is mathematics and not float, and the positive control can
report "bounded".
"""

import os
import sys
from fractions import Fraction

# Pin BLAS to one thread BEFORE numpy is imported.  These gates invert and decompose dense
# matrices of a few thousand rows; on a loaded machine a multi-threaded LAPACK thrashes
# badly (a 1100x1100 `inv` measured 11.07s against 0.71s single-threaded), which is what
# turns this file from a fast gate into a slow one.  It also fixes the reduction order, so
# the printed digits do not depend on how many cores happened to be free.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np                                                     # noqa: E402

sys.path.insert(0, ".")

from solver.spectral_certificate import (
    algebra_constant, bordered_linearization, clm_anchor, clm_residual,
    clm_residual_exact, dissipative_control, exact_inverse_norm,
    finite_section_inverse_norm, hilbert_identity_defect, homogeneous_tail_mode,
    quadratic_bound, rigorous_finite_block, tail_block, tail_diagonal,
    tail_inverse_norm,
    velocity_constant_terms, weight_window, weighted_l1_opnorm, weight_vector,
    bordered_tail_inverse_norm, fredholm_sides, tail_left_null, tail_right_null,
    tail_singular_pair,
    block_upper_triangular_bound, kernel_membership_ladder, nogo_hypotheses,
    tail_kernel_defect,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


# 1 -- the basis identities are exact, not approximate
d = [hilbert_identity_defect(k) for k in (1, 2, 3, 5, 9)]
worst = max(max(a, b) for a, b in d)
gate("hilbert identities exact", worst < 1e-14,
     f"max |Re w^k - cos k th|, |Im w^k - sin k th| = {worst:.2e} over k = 1,2,3,5,9")

# 2 -- the velocity recursion's constant terms are exactly (-1)^k k
c = velocity_constant_terms(16)
closed = np.array([(-1.0) ** k * k for k in range(1, 17)])
gate("velocity constants closed form", np.array_equal(c, closed),
     f"c_k = (-1)^k k exactly for k = 1..16 (max defect {np.max(np.abs(c - closed)):.1e}) "
     "-- so U carries a theta-linear (sawtooth) part")

# 3 -- the anchor's residual is EXACTLY zero in rational arithmetic
R = clm_residual_exact(8)
gate("anchor residual exactly zero", all(x == 0 for x in R),
     f"{len(R)} modes, all Fraction(0) -- Y_0 = 0 exactly, not 1e-16")

# 4 -- and a perturbed profile is NOT a zero (the negative control for gate 3)
b, c_om, c_l = clm_anchor(6)
b[3] = Fraction(1, 500)
Rp = clm_residual(b, c_om, c_l)
gate("perturbed profile rejected", any(x != 0 for x in Rp),
     f"{sum(1 for x in Rp if x != 0)} nonzero modes after a 2e-3 perturbation of b_4")

# 5 -- the linearization matches a central difference of the residual
K = 10
b0 = np.array([-1.0] + [0.0] * (K - 1))


def Rf(bv, cv):
    return np.array([float(x) for x in clm_residual(list(bv), cv, 1.0)])[:K]


M = bordered_linearization(K)
eps = 1e-5
J = np.zeros((K, K + 1))
for j in range(K):
    bp, bm = b0.copy(), b0.copy()
    bp[j] += eps
    bm[j] -= eps
    J[:, j] = (Rf(bp, -1.0) - Rf(bm, -1.0)) / (2 * eps)
J[:, K] = (Rf(b0, -1.0 + eps) - Rf(b0, -1.0 - eps)) / (2 * eps)
fd = float(np.max(np.abs(J - M[:K, :])))
gate("linearization vs central difference", fd < 1e-9,
     f"max |DF - FD| = {fd:.2e} (the residual is exactly quadratic, so this is roundoff)")

# 6 -- THE STRUCTURAL FACT: the tail operator's diagonal is exactly zero
diag = tail_diagonal(64, 160)
gate("tail diagonal is exactly zero", float(np.max(np.abs(diag))) == 0.0,
     "max|diag(T_tail)| = 0 -- no diagonal A_tail exists, which is what every standard "
     "radii-polynomial tail estimate assumes")

# 7 -- the homogeneous tail mode decays like m^-2, i.e. the |X|^-1 far field
h = homogeneous_tail_mode(801)
m = np.arange(1, 802)
sel = (np.abs(h) > 0) & (m > 100)
p = float(np.polyfit(np.log(m[sel]), np.log(np.abs(h[sel])), 1)[0])
gate("tail kernel is the 1/X far field", abs(p + 2.0) < 0.05,
     f"h_m ~ m^{p:.3f}, i.e. Omega ~ |X|^-{-p - 1:.3f} -- in l^1 for s < 1, so the tail "
     "operator is not injective there")

# 8 -- the divergence is mathematics: exact rational arithmetic reproduces the float
rows = [(K, float(exact_inverse_norm(K, Fraction(11, 10))),
         finite_section_inverse_norm(K, "geometric", 1.1)) for K in (16, 64, 96)]
gap = max(abs(a - b) / a for _, a, b in rows)
gate("exact rational == float", gap < 1e-12,
     f"max relative gap {gap:.2e} over K = 16, 64, 96 at nu = 1.1 "
     f"(K=96: exact {rows[-1][1]:.4f})")

# 9 -- the positive control: dissipation saturates the same code path.  Measured on the
# TAIL block, which is the term that decides the leg, and required to be a CONTRAST:
# the inviscid ratio must grow and the dissipative one must not.
ratios = {}
for kind, p in (("flat", 0.0), ("algebraic", 1.0)):
    for mu in (0.0, 0.5):
        v = [tail_inverse_norm(64, M, kind, p, mu=mu) for M in (320, 1088)]
        ratios[(kind, mu)] = v[1] / v[0]
ok = (all(ratios[(k, 0.0)] > 1.5 for k in ("flat", "algebraic"))
      and all(ratios[(k, 0.5)] < 1.02 for k in ("flat", "algebraic")))
gate("positive control saturates", ok,
     "M: 320 -> 1088, ratio  " + ", ".join(
         f"{k} mu={mu}: {v:.3f}" for (k, mu), v in ratios.items()))

# 10 -- the tail term diverges in every class tested, inviscid
tails = {(k, p): [tail_inverse_norm(64, M, k, p) for M in (128, 320, 576)]
         for k, p in (("flat", 0.0), ("algebraic", 0.394), ("algebraic", 1.0),
                      ("geometric", 1.05))}
ok = all(v[-1] > 2.0 * v[0] for v in tails.values())
gate("tail diverges in every class", ok,
     "; ".join(f"{k}{p}: {v[0]:.2f}->{v[-1]:.3g}" for (k, p), v in tails.items()))

# 11 -- the finite block is rigorous and small, and Y_0 is zero
r = rigorous_finite_block(128, "algebraic", 1.0)
Z2 = 2.0 * r["A_norm"] * quadratic_bound("algebraic", 1.0, K=96)
gate("finite block closes rigorously", r["Z1_finite"] < 1e-6 and r["Y0"] == 0.0,
     f"Y_0 = 0 exactly, rigorous Z_1 = {r['Z1_finite']:.2e}, ||A||_w = {r['A_norm']:.3f}, "
     f"Z_2 = {Z2:.3g}")

# 12 -- the algebra constant is <= 1 in every class (what Z_2 rests on)
ac = {f"{k}({p})": algebra_constant(k, p) for k, p in
      (("flat", 0.0), ("algebraic", 1.0), ("algebraic", 0.394), ("geometric", 1.1))}
gate("weighted l^1 is a Banach algebra", all(v <= 1.0 + 1e-12 for v in ac.values()),
     ", ".join(f"{k}: {v:.4f}" for k, v in ac.items()))

# 13 -- the weight window is empty for the target's far field
w = weight_window(0.394, 1.0)
gate("weight window empty at alpha = 0.394", w["empty"],
     f"object side s < {w['s_max_object']}, operator side s = {w['s_operator']}, "
     f"gap {w['gap']:+.3f} in exponent units")

# 14 -- the norm helper agrees with an explicit sum (no silent transpose)
A = np.array([[1.0, -2.0], [3.0, 4.0]])
wv = np.array([1.0, 2.0])
explicit = max((1 * 1 + 2 * 3) / 1, (1 * 2 + 2 * 4) / 2)
gate("weighted l^1 operator norm", abs(weighted_l1_opnorm(A, wv, wv) - explicit) < 1e-15,
     f"{weighted_l1_opnorm(A, wv, wv):.6f} == {explicit:.6f} (column sums, not rows)")

# ---------------------------------------------------------------------------
# ROUTE T -- the bordered tail (leg 52)
# ---------------------------------------------------------------------------

# 15 -- the analytic kernel really is annihilated by the tail block
K, M = 64, 576
T = tail_block(K, M)
h = tail_right_null(K, M)
# the recursion is built for the interior rows; the last row closes the truncation
resid = np.abs(T[:-1] @ h).max() / np.abs(h).max()
gate("analytic right null vector is a kernel", resid < 1e-12,
     f"||T h|| / ||h|| = {resid:.2e} on the interior rows")

# 16 -- and the cokernel lives on the OPPOSITE parity chain.  Column 0 is excluded on
# the same grounds the kernel's last row is: it is the one column that reaches the mode
# K lying OUTSIDE the block, which is exactly what makes each null space 1-dimensional.
u = tail_left_null(K, M)
lresid = np.abs(u @ T[:, 1:]).max() / np.abs(u).max()
outside = np.abs(u @ T[:, 0]) / np.abs(u).max()
overlap = float(np.abs(np.sign(np.abs(h)) @ np.sign(np.abs(u))))
gate("analytic left null vector is a cokernel, opposite parity",
     lresid < 1e-12 and overlap == 0.0 and outside > 1e-3,
     f"||u^T T|| / ||u|| = {lresid:.2e} on the interior columns, support overlap = "
     f"{overlap:.0f}; the one column reaching outside the block gives {outside:.2e}, "
     f"which is why the null space is 1-dimensional")

# 17 -- the kernel is ONE-dimensional: sigma_min -> 0, sigma_2 stays away
smin, s2, align = zip(*[tail_singular_pair(64, M, "flat", 0.0)
                        for M in (320, 1088, 3136)])
gate("kernel is one-dimensional", smin[-1] < 0.05 * smin[0] and min(s2) > 1.0,
     f"sigma_min {smin[0]:.2e} -> {smin[-1]:.2e}, sigma_2 stays > {min(s2):.3f}")

# 18 -- and the optimal direction IS the analytic far field
gate("optimal border direction is the far field", align[-1] > 0.999,
     f"|cos| -> {align[-1]:.5f} at M = 3136")

# 19 -- THE GATE: bordering bounds the tail in the ADMISSIBLE classes
lad = {(k, p): [bordered_tail_inverse_norm(64, M, k, p, border="analytic")
                for M in (320, 1088, 3136)]
       for k, p in (("flat", 0.0), ("algebraic", 0.3))}
unb = {(k, p): [tail_inverse_norm(64, M, k, p) for M in (320, 1088, 3136)]
       for k, p in (("flat", 0.0), ("algebraic", 0.3))}
ok = all(v[-1] < 1.6 * v[0] for v in lad.values()) and \
     all(unb[key][-1] > 3.0 * unb[key][0] for key in unb)
gate("bordering bounds the tail where the object has finite norm", ok,
     "; ".join(f"{k}{p}: bordered {v[0]:.2f}->{v[-1]:.2f} vs unbordered "
               f"{unb[(k, p)][0]:.2f}->{unb[(k, p)][-1]:.2f}"
               for (k, p), v in lad.items()))

# 20 -- and it does NOT at s >= 1, which is the prediction, not a fit
hi = [bordered_tail_inverse_norm(64, M, "algebraic", 1.0) for M in (320, 1088, 3136)]
gate("bordering fails at s = 1, as the Fredholm sides predict", hi[-1] > 1.9 * hi[0],
     f"s=1: {hi[0]:.2f} -> {hi[-1]:.2f} (still growing)")

# 21 -- the two failure modes swap at s = 1
fs = fredholm_sides(64, 3136)
gate("kernel decays like m^-2, cokernel grows like m",
     abs(fs["kernel_exponent"] + 2.0) < 0.02 and abs(fs["cokernel_exponent"] - 1.0) < 0.02,
     f"kernel m^{fs['kernel_exponent']:.4f} (in space iff s<1), "
     f"cokernel m^{fs['cokernel_exponent']:+.4f} (bounded iff s>=1)")

# 22 -- NEGATIVE CONTROLS: the wrong border direction is worth nothing
second = [bordered_tail_inverse_norm(64, M, "flat", 0.0, border="second")
          for M in (320, 1088, 3136)]
rand = [bordered_tail_inverse_norm(64, M, "flat", 0.0, border="random")
        for M in (320, 1088, 3136)]
gate("negative controls keep diverging",
     second[-1] > 2.0 * second[0] and rand[-1] > 1.5 * rand[1],
     f"second {second[0]:.2f}->{second[-1]:.2f}, random {rand[0]:.0f}->{rand[-1]:.0f}")

# 23 -- the analytic border matches the optimal one where it matters
a_n = bordered_tail_inverse_norm(64, 3136, "algebraic", 0.3, border="analytic")
a_s = bordered_tail_inverse_norm(64, 3136, "algebraic", 0.3, border="svd")
gate("analytic border achieves the SVD optimum", a_n / a_s < 1.02,
     f"analytic / SVD = {a_n / a_s:.4f} (a proof cannot border with a singular vector)")


# -------------------------------------------------------------------------
# LEG 54 (Route-MM): the two structural facts the shape argument rests on.
# Both are properties of the OPERATOR, so they belong here and not in the runner.
# -------------------------------------------------------------------------

# 24 -- the tail operator annihilates the far field, and the ONLY obstruction is the
# truncation edge.  This is what makes MM-4's floor shape-independent:
# (I - A L)_{Gamma,tail} applied to the kernel direction is -A11 B hhat, in which the
# off-diagonal block A12 has dropped out.  The identity is EXACT for the infinite operator;
# on the computed one it holds up to a defect supported on the LAST mode alone and falling
# like M^-1, which is what this gate pins -- reporting the SHAPE of the ladder (72) rather
# than asserting an exact zero that the truncation does not deliver.
_K = 16
_lad = []
for _Mx in (256, 512, 1024, 2048):
    _T = tail_block(_K, _K + _Mx)
    _h = tail_right_null(_K, _K + _Mx)
    _r = _T @ _h
    _nz = np.nonzero(np.abs(_r) > 1e-14)[0]
    _lad.append((_Mx, float(np.sum(np.abs(_r)) / np.sum(np.abs(_h))),
                 list(_nz) == [len(_r) - 1]))
_edge_only = all(t[2] for t in _lad)
_halves = all(abs(_lad[i][1] / _lad[i + 1][1] - 2.0) < 0.05 for i in range(len(_lad) - 1))
gate("the far field is annihilated except at the truncation edge, and that falls like 1/M",
     _edge_only and _halves,
     "relative l1 defect " + " -> ".join(f"{t[1]:.2e}" for t in _lad) +
     f" over M-K = 256..2048 (halves per doubling); supported on the LAST mode only: "
     f"{_edge_only} -- so ker T is the far field for the infinite operator, and A12 cannot "
     f"reach that direction up to O(1/M) (leg 54 MM-4)")

# 25 -- EVERY ODD SPLIT has a singular finite block, so the split must be EVEN.  This is
# what shrinks the corner MM-1's |1 - K/2| prefactor leaves open from {2,3,4} to {2}.
_odd_sv, _even_sv = [], []
for _k in (3, 5, 7, 9, 11):
    _F = bordered_linearization(_k)
    _odd_sv.append(float(np.linalg.svd(_F, compute_uv=False)[-1]))
for _k in (2, 4, 6, 8, 10, 12):
    _F = bordered_linearization(_k)
    _even_sv.append(float(np.linalg.svd(_F, compute_uv=False)[-1]))
gate("every ODD split has a singular finite block; every even one does not",
     max(_odd_sv) < 1e-14 and min(_even_sv) > 1e-4,
     f"odd K=3..11: smallest singular value <= {max(_odd_sv):.1e}; "
     f"even K=2..12: >= {min(_even_sv):.1e} -- the split must be EVEN (leg 54 MM-1b)")

# 26 -- the dilation zero mode is EXACTLY e_2, which is what the "null" gauge pins.  Leg
# 53 asserted this in its runner; it is checked here so it decays at the rate of code.
_F = bordered_linearization(32)
_e2 = np.zeros(33)
_e2[1] = 1.0
gate("the dilation zero mode is exactly e_2",
     float(np.max(np.abs((_F @ _e2)[:32]))) == 0.0,
     f"||L e_2||_inf over the unbordered rows = "
     f"{float(np.max(np.abs((_F @ _e2)[:32]))):.1e} (exactly zero)")


# --------------------------------------------------------------------------
# ROUTE NG (leg 58) -- the gates the PROPOSITION rests on.  If any of 27-31 fails,
# Proposition NG is false and its writeups must be withdrawn, not softened.
# --------------------------------------------------------------------------

# 27 -- (H2) the tail kernel is IN l^1_w exactly where fredholm_sides says it is.  The
# proposition is UNCONDITIONAL for s < 1 and has no content at s >= 1; both halves are
# gated, because a hypothesis that cannot fail is not a hypothesis.
_in_space = kernel_membership_ladder(8, (256, 1024, 4096, 16384), "flat", 0.0)
_in_space_03 = kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", 0.3)
_out_10 = kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", 1.0)
_out_15 = kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", 1.5)
_slow = kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", 0.7)
gate("the tail kernel is in l^1_w for s < 1 (INCLUDING the slow case s = 0.7) and not for "
     "s >= 1",
     _in_space["in_l1_w"] and _in_space_03["in_l1_w"] and _slow["in_l1_w"]
     and _out_10["verdict"] == "log_divergent"
     and _out_15["verdict"] == "power_divergent",
     f"increment ratio -> verdict: s=0 {_in_space['last_increment_ratio']:.3f} converges "
     f"(norm {_in_space['partial_norm'][-1]:.4f}), s=0.3 "
     f"{_in_space_03['last_increment_ratio']:.3f} converges "
     f"(norm {_in_space_03['partial_norm'][-1]:.4f}), s=0.7 "
     f"{_slow['last_increment_ratio']:.3f} converges to ~"
     f"{_slow['geometric_limit_estimate']:.1f} though its partial sum "
     f"({_slow['partial_norm'][-1]:.1f} at M=16384) still looks like it is rising, "
     f"s=1 {_out_10['last_increment_ratio']:.3f} log-divergent, s=1.5 "
     f"{_out_15['last_increment_ratio']:.3f} power-divergent -- the s < 1 threshold of "
     f"fredholm_sides, checked on the vector rather than inferred from the exponent")

# 28 -- the finite-M defect is a TRUNCATION artifact and vanishes; on the infinite tail
# T h = 0 exactly.  This is what lets the finite-M measurement stand for the operator.
_rho = [tail_kernel_defect(8, 8 + e, "flat", 0.0) for e in (128, 256, 512, 1024, 2048)]
_slope = float(np.polyfit(np.log([128, 256, 512, 1024, 2048]), np.log(_rho), 1)[0])
gate("the kernel defect rho_M vanishes like M^-1 in the flat class",
     _rho[-1] < _rho[0] and abs(_slope + 1.0) < 0.05,
     f"rho_M = {_rho[0]:.3e} -> {_rho[-1]:.3e} over M-K = 128..2048, fitted M^({_slope:+.4f}) "
     f"-- an edge effect of the truncation, not a defect of the kernel")

# 29 -- the defect does NOT vanish once mu > 0: that is the sharpness control's mechanism,
# and it is the reason the mu > 0 measurement can come out the other way (lesson 90).
_rho_mu = [tail_kernel_defect(8, 8 + e, "flat", 0.0, mu=2.0)
           for e in (128, 256, 512, 1024, 2048)]
gate("mu = 2 destroys the kernel: the defect GROWS instead of vanishing",
     _rho_mu[-1] > _rho_mu[0] and min(_rho_mu) > 1.0,
     f"rho_M(mu=2) = {_rho_mu[0]:.4f} -> {_rho_mu[-1]:.4f} over the same ladder "
     f"(growing, and never below 1), against {_rho[0]:.3e} -> {_rho[-1]:.3e} at mu = 0 "
     f"-- a factor {_rho_mu[-1] / _rho[-1]:.3g} apart at M-K = 2048")

# 30 -- the bound is arithmetic and reduces to Z1 >= 1 on the infinite tail.  Gated so the
# proposition's one line cannot be silently edited.
gate("block_upper_triangular_bound is Z1 >= 1 + floor when rho = 0",
     block_upper_triangular_bound(0.0, 1e9, 0.0) == 1.0
     and block_upper_triangular_bound(0.0, 1e9, 2.5) == 3.5
     and abs(block_upper_triangular_bound(0.01, 20.0, 0.0) - 0.8) < 1e-12,
     "rho=0 gives 1 for ANY ||A22|| (1e9 tested), 1+floor with a floor, and the "
     "finite-M form 1 - rho*||A22|| otherwise -- A12 never appears, which is why the "
     "class is larger than block-diagonal")

# 31 -- the hypotheses report MAGNITUDES and the mu dial flips H2.  A boolean-only
# hypothesis check would hide the two orders of magnitude that do the work.
_h0 = nogo_hypotheses(16, 16 + 1024, "algebraic", 0.3, mu=0.0)
_h2 = nogo_hypotheses(16, 16 + 1024, "algebraic", 0.3, mu=2.0)
gate("nogo_hypotheses separates mu = 0 from mu = 2 by orders of magnitude",
     _h0["H2_holds_on_the_infinite_tail"] and not _h2["H2_holds_on_the_infinite_tail"]
     and _h2["sigma_min"] > 100.0 * _h0["sigma_min"],
     f"sigma_min(T): {_h0['sigma_min']:.4e} at mu=0 vs {_h2['sigma_min']:.4e} at mu=2 "
     f"({_h2['sigma_min'] / _h0['sigma_min']:.0f}x); kernel norm {_h0['kernel_norm_l1_w']:.4f}")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
sys.exit(1 if n_fail else 0)
