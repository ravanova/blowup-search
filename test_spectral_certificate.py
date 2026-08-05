"""Gates for solver/spectral_certificate.py -- the certificate in the compactified basis.

The claims under test are the ones the leg's conclusion rests on, in the order they are
used: the basis algebra is exact, the anchor is an exact zero, the tail operator has no
diagonal, the divergence is mathematics and not float, and the positive control can
report "bounded".
"""

import sys
from fractions import Fraction

import numpy as np

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


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
sys.exit(1 if n_fail else 0)
