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
    quadratic_bound, rigorous_finite_block, tail_diagonal, tail_inverse_norm,
    velocity_constant_terms, weight_window, weighted_l1_opnorm, weight_vector,
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

n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
sys.exit(1 if n_fail else 0)
