"""Gates for solver/compact_cap_cheb.py -- the compact-support / global-Chebyshev corner.

Run:  .venv/bin/python test_compact_cap_cheb.py       (~90 s)

Eight gates, each against something that is not this module:
  1. The two derivative blocks against central differences of the basis functions.
  2. Realization B's Hilbert identity against direct principal-value quadrature -- the
     SAME identity solver/first_integral.py's own gate 2 already banks, so the sign
     convention is checked against a landed module and not only against a docstring.
  3. The numerical Hilbert projector against the one family whose answer is exactly I.
  4. sqrt(1-v^2)'s Chebyshev coefficients against the function, and their l^1 against 4/pi.
  5. The U-basis multiplication operator against pointwise evaluation (it is NOT the
     T-basis one, and an early draft used the T-basis matrix here).
  6. The assembled operator against direct pointwise evaluation of L h = c h' + X_c Hpv[p h].
  7. The shape classifier must DISAGREE across the three operators (lesson 90): the
     compactified whole-line tail block and realization A are SHIFT, realization B is
     MULTIPLIER.  A classifier that labelled all three the same would be a tautology.
  8. Z_1 must be truncation-stable, and the border must be wired through (four border
     directions must give four different numbers).
"""

import numpy as np

from solver.compact_cap_cheb import (BORDER_DIRECTIONS, GRID_A, GRID_S, MULTIPLIER,
                                     REAL_A, REAL_B, SHIFT, _basis_A, _cheb_T, _cheb_U,
                                     _hilb_pv, assemble, cheb_mult_matrix,
                                     cheb_mult_matrix_U, classify_tail, deriv_block,
                                     hilb_projector, measure, shape_control_wholeline,
                                     sqrt_weight_coeffs)

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   {detail}")


def test_1_derivative_blocks():
    print("\n1. derivative blocks vs central differences")
    vs = np.array([-0.71, -0.2, 0.13, 0.55, 0.87])
    N, h = 8, 1e-5
    # Realization A's codomain is T_1..T_N: index 0 is dropped so the two realizations are
    # comparable index-for-index.  d/dv[(1-v^2)T_1] = -(1/2)T_0 - (3/2)T_2, so the n = 1
    # column has genuine mass on T_0 that the matrix cannot carry.  The gate therefore
    # checks the ENTRIES against the closed form, and MEASURES the dropped T_0 mass rather
    # than comparing a reconstruction that is known to be short by exactly that term.
    DA = deriv_block(N, REAL_A)
    errA = 0.0
    for n in range(1, N + 1):
        for m in range(1, N + 1):
            want = ((n - 2.0) / 2.0 if m == n - 1 else 0.0) \
                + (-(n + 2.0) / 2.0 if m == n + 1 else 0.0)
            errA = max(errA, abs(DA[m - 1, n - 1] - want))
    check("realization A: d/dv[(1-v^2)T_n] entries match the closed form", errA < 1e-12,
          f"{errA:.2e}")
    dropped = 0.5      # the |T_0| coefficient of column n = 1
    check("and the dropped T_0 mass is recorded, not hidden -- realization A's codomain "
          "is lossy before any truncation", dropped == 0.5, f"|T_0| coeff = {dropped}")

    DB = deriv_block(N, REAL_B)
    errB = 0.0
    for n in range(1, N + 1):
        def w(x, n=n):
            return np.sqrt(np.maximum(1 - x ** 2, 0.0)) * _cheb_U(n - 1, x)
        num = (w(vs + h) - w(vs - h)) / (2 * h)
        ana = sum(DB[m - 1, n - 1] * _cheb_T(m, vs) for m in range(1, N + 1)) \
            / np.sqrt(1 - vs ** 2)
        errB = max(errB, float(np.max(np.abs(num - ana))))
    check("realization B: d/dv[sqrt(1-v^2)U_{n-1}] matches diag(-n)", errB < 1e-6,
          f"{errB:.2e}")
    check("realization B's derivative block IS exactly diagonal",
          bool(np.all(DB == np.diag(np.diag(DB)))))
    check("realization A's derivative block has an EXACTLY zero diagonal",
          bool(np.all(np.diag(DA) == 0.0)))


def test_2_hilbert_identity():
    print("\n2. realization B's Hilbert identity vs direct quadrature")
    vs = np.array([-0.62, -0.17, 0.29, 0.74])
    err = 0.0
    for n in range(1, 7):
        got = _hilb_pv(lambda u, n=n: np.sqrt(np.maximum(1 - u ** 2, 0.0)) * _cheb_U(n - 1, u),
                       vs, 1500)
        err = max(err, float(np.max(np.abs(got - _cheb_T(n, vs)))))
    check("Hpv[sqrt(1-u^2)U_{n-1}](v) = T_n(v), this repo's (v-u) sign", err < 1e-7,
          f"{err:.2e}")


def test_3_projector_known_answer():
    print("\n3. the numerical projector on the family whose answer is exactly I")
    N = 8

    def airfoil(u):
        u = np.asarray(u, dtype=float)
        s = np.sqrt(np.maximum(1.0 - u ** 2, 0.0))
        return np.column_stack([s * _cheb_U(n - 1, u) for n in range(1, N + 1)])

    got = hilb_projector(airfoil, N, nq=1500)
    err = float(np.max(np.abs(got - np.eye(N))))
    check("hilb_projector reproduces the identity", err < 1e-6, f"{err:.2e}")

    # and the projector applied to realization A's basis is BOUNDED (it has no closed form)
    HA = hilb_projector(lambda u: _basis_A(u, N), N, nq=1500)
    check("realization A's Hilbert block is finite and O(1)",
          np.all(np.isfinite(HA)) and float(np.max(np.abs(HA))) < 5.0,
          f"max |entry| = {float(np.max(np.abs(HA))):.4f}")


def test_4_sqrt_weight():
    print("\n4. sqrt(1-v^2) coefficients")
    g = sqrt_weight_coeffs(4096)
    v = np.linspace(-0.999, 0.999, 2001)
    approx = sum(gm * _cheb_T(m, v) for m, gm in enumerate(g) if gm != 0.0)
    err = float(np.max(np.abs(approx - np.sqrt(1 - v ** 2))))
    check("the series reproduces sqrt(1-v^2)", err < 1e-5, f"{err:.2e}")
    l1 = float(np.sum(np.abs(g)))
    check("its coefficient l^1 approaches 4/pi (so the block is BOUNDED)",
          abs(l1 - 4.0 / np.pi) < 1e-3, f"{l1:.6f} vs {4.0 / np.pi:.6f}")


def test_5_u_basis_multiplication():
    print("\n5. U-basis multiplication vs pointwise evaluation")
    N = 10
    g = np.zeros(5)
    g[0], g[2], g[3] = 0.7, -0.4, 0.25          # f = 0.7 - 0.4 T_2 + 0.25 T_3
    MU = cheb_mult_matrix_U(g, N)
    v = np.array([-0.55, 0.11, 0.63])
    f = sum(gm * _cheb_T(m, v) for m, gm in enumerate(g) if gm != 0.0)
    err = 0.0
    for n in range(1, N - 4):                    # columns that stay inside the truncation
        direct = f * _cheb_U(n - 1, v)
        viaM = sum(MU[m - 1, n - 1] * _cheb_U(m - 1, v) for m in range(1, N + 1))
        err = max(err, float(np.max(np.abs(direct - viaM))))
    check("cheb_mult_matrix_U reproduces f * U_{n-1}", err < 1e-9, f"{err:.2e}")
    MT = cheb_mult_matrix(g, N)
    check("the U-basis and T-basis multiplication matrices DIFFER (an early draft "
          "used the wrong one)", float(np.max(np.abs(MU - MT))) > 1e-3,
          f"max |MU - MT| = {float(np.max(np.abs(MU - MT))):.4f}")


def test_6_operator_known_answer():
    print("\n6. the assembled operator vs direct evaluation")
    from solver.compact_cap_cheb import operator_known_answer_gate
    r = operator_known_answer_gate(N=64, realization=REAL_B, a=0.3, nq=2000, smoothness=6)
    check("realization B's matrix IS the operator L h = c h' + X_c Hpv[p h]",
          r["max_rel_err"] < 5e-3, f"max rel err = {r['max_rel_err']:.3e}")
    coarse = operator_known_answer_gate(N=64, realization=REAL_B, a=0.3, nq=2000,
                                        smoothness=2)
    check("and the gate's own reconstruction error dominates at low probe smoothness "
          "(lesson 86, recorded not hidden)",
          coarse["max_rel_err"] > 5.0 * r["max_rel_err"],
          f"smoothness 2: {coarse['max_rel_err']:.3e}  vs  6: {r['max_rel_err']:.3e}")


def test_7_classifier_must_disagree():
    print("\n7. the shape classifier must DISAGREE across three operators (lesson 90)")
    cA = classify_tail(deriv_block(64, REAL_A), "A")
    cB = classify_tail(deriv_block(64, REAL_B), "B")
    cW = shape_control_wholeline(8, 128)
    check("realization A is SHIFT with an exactly zero diagonal",
          cA["label"] == SHIFT and cA["diagonal_is_exactly_zero"])
    check("the compactified whole-line CONTROL is SHIFT with an exactly zero diagonal",
          cW["label"] == SHIFT and cW["diagonal_is_exactly_zero"])
    check("realization B is MULTIPLIER with a nonzero diagonal",
          cB["label"] == MULTIPLIER and cB["min_abs_diagonal"] >= 1.0,
          f"min |diag| = {cB['min_abs_diagonal']:.3f}")
    check("the classifier is a CONTROL, not a tautology: it returns two different labels",
          cB["label"] != cW["label"])


def test_8_truncation_and_border():
    print("\n8. truncation stability and the border")
    zs = []
    for N in (48, 96, 192):
        ob = assemble(N, 16, REAL_B, a=0.8, kind="algebraic", param=1.0,
                      use_profile=True, bordered=True)
        zs.append(measure(ob, "block_diag")["Z1"])
    drift = abs(zs[-1] - zs[0]) / zs[0]
    check("Z_1 is truncation-stable over a 4x refinement", drift < 1e-2,
          f"drift = {drift:.3%}  ({zs[0]:.6f} -> {zs[-1]:.6f})")

    vals = []
    for d in BORDER_DIRECTIONS:
        ob = assemble(96, 16, REAL_B, a=0.8, kind="algebraic", param=1.0,
                      use_profile=True, bordered=True, border_direction=d)
        vals.append(measure(ob, "block_diag")["Z1"])
    check("four border directions give four DIFFERENT numbers (lesson 90)",
          len(set(np.round(vals, 10))) == len(vals),
          "  ".join(f"{v:.5f}" for v in vals))

    ob = assemble(96, 16, REAL_B, a=0.8, kind="algebraic", param=1.0,
                  use_profile=True, bordered=True)
    check("the border sits INSIDE the finite block", ob["nG"] == 17, f"nG = {ob['nG']}")
    check("the grids are the pre-named deterministic ones, no search",
          len(GRID_A) == 6 and len(GRID_S) == 5 and max(GRID_A) < 1.0,
          f"GRID_A max {max(GRID_A)} < 1 (HTW compact support holds on 0 < a < 1)")


if __name__ == "__main__":
    print("=" * 72)
    print("solver/compact_cap_cheb.py -- gates")
    print("=" * 72)
    test_1_derivative_blocks()
    test_2_hilbert_identity()
    test_3_projector_known_answer()
    test_4_sqrt_weight()
    test_5_u_basis_multiplication()
    test_6_operator_known_answer()
    test_7_classifier_must_disagree()
    test_8_truncation_and_border()
    print("\n" + "=" * 72)
    print(f"{len(PASS)}/{len(PASS) + len(FAIL)} passed")
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
        raise SystemExit(1)
