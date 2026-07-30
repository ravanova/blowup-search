"""Known-answer tests for the Route-D UPPER bounds (solver/nk_bounds.py).

Every quantity in that module claims to DOMINATE something, so every gate here is
a domination test against an independently computed measurement -- and, where the
quantity is a norm over a ball, against an ADVERSARY rather than a random or
smooth family (banked lesson 9).  Two gates additionally test the module's own
central warning: that duality over a DISCRETE Holder ball is unsound.

Pre-committed predicates:
  (1) DISCRETE-BALL TRAP: the vector that discrete-ball duality selects as the
      extremizer has a continuum norm inflated by >= 1e3 over its discrete norm,
      and the inflation GROWS with J -- so it is not in the true unit ball, while
      a smooth profile's inflation stays ~1.
  (2) TWO-POINT DUAL IS VALID: for random codomain vectors g, the predicted
      bound |c.g| <= two_point_dual(c) * ||g||_Y holds, using the REFINED-grid
      (continuum) norm of g -- i.e. the bound is valid against the true ball.
  (3) THE MODELLING IDENTITY: DF - L = diag(1/(X(1+X^2))) - H/(1+X^2) exactly.
  (4) LOCAL HOLDER ENVELOPE: |h(y1)-h(y2)| <= holder_local_X_constant *
      |y1-y2|^gamma for unit-ball h, over grid-resolved pairs.
  (5) HILBERT + MODELLING BOUNDS DOMINATE: on nodes the grid resolves in X
      (|X| dtheta <= 1, the project's standing convention), the measured
      |H(h)(X)| and ||(DF-L)h||_Y stay under their bounds for an adversarial test
      set, and the H bound reproduces the sharp far-field constant M_alpha/(pi X)
      and stays FINITE as X -> 0 (where the true value is 0 by parity).
  (6) PREDICTED DECAY + BUDGET ALGEBRA: the modelling-error bound falls like
      X0^{alpha-2} with the supremum at X0, and `budget` closes/fails correctly.

Run: python test_nk_bounds.py    (no scipy; ~2 min)
"""

import numpy as np

from solver.decay_collocation import Collocation, C_ANCHOR
from solver.holder_norms import HolderNorm, square_wave_partial_sum
from solver.nk_bounds import (
    two_point_dual, sup_part_upper, discrete_ball_inflation, refine,
    holder_local_X_constant, hilbert_farfield_bound,
    farfield_modelling_error_bound, quadratic_constant_upper, farfield_mass,
    budget,
)

ALPHA, GAMMA = 1.5, 0.5


def _gauged_inverse(col, alpha):
    """A = inv([gauge row ; DF rows 1..]) and the codomain weight/kernel."""
    J = col.J
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    A = np.linalg.inv(M)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, GAMMA)
    cod.w[0] = 1.0                       # the gauge slot is a plain scalar
    q = cod.pair.copy()
    return A, cod.w.copy(), q


def _far_field_model(col, c=C_ANCHOR):
    return -np.diag(1.0 / col.X) - c * col.transport


def _resolved(col):
    """Nodes the grid resolves in X: |X| dtheta <= 1 (project convention)."""
    return col.X * (np.pi / col.J) <= 1.0


def test_discrete_ball_trap():
    """(1) the discrete-ball extremizer is not in the continuum ball."""
    nf = lambda th, X: HolderNorm(th, X, ALPHA + 1.0, GAMMA)      # noqa: E731
    infl, smooth = [], []
    for J in (125, 250, 500):
        col = Collocation(J)
        A, v, _ = _gauged_inverse(col, ALPHA)
        B = A / v[None, :]
        g = np.sign(B[0] - B[1]) / v                # what duality picks
        g[0] = 0.0                                  # gauge slot is not a nodal value
        infl.append(discrete_ball_inflation(col.to_coef, J, g, nf)["inflation"])
        # a smooth element OF THE CODOMAIN CLASS (decaying at the codomain's
        # own rate) -- using the anchor here instead would measure the weight
        # mismatch (it decays like X^-2 against an X^-2.5 weight), not fidelity
        smooth.append(discrete_ball_inflation(
            col.to_coef, J,
            (1.0 + col.X ** 2) ** (-0.5 * (ALPHA + 1.0)), nf)["inflation"])
    assert min(infl) > 1e3, f"expected massive inflation, got {infl}"
    assert infl[-1] > infl[0], f"inflation must grow with J: {infl}"
    assert max(smooth) < 1.05, f"a smooth profile must be faithful: {smooth}"
    print(f"[ok] (1) discrete-ball trap: extremizer inflation "
          f"{infl[0]:.1e} -> {infl[-1]:.1e} over J=125..500 "
          f"(smooth profile: {max(smooth):.4f})")


def test_two_point_dual_valid():
    """(2) the two-point dual bound holds against CONTINUUM codomain norms."""
    col = Collocation(300)
    A, v, q = _gauged_inverse(col, ALPHA)
    cand = np.unique(np.linspace(1, col.J - 1, 24).astype(int))
    rows = np.array([0, 7, 40, 150, 299])
    d = two_point_dual(A[rows], v, q, cand)
    rng = np.random.default_rng(11)
    worst = 0.0
    for _ in range(24):
        k = int(rng.integers(1, col.J // 6))
        g = np.cos(k * col.theta) * (1.0 + col.X ** 2) ** (-0.5 * (ALPHA + 1.0))
        gv = np.concatenate(([0.0], g[1:]))
        th_f, X_f, gf = refine(col.to_coef, col.J, np.concatenate(([0.0], g[1:])))
        ng = HolderNorm(th_f, X_f, ALPHA + 1.0, GAMMA)(gf)
        for r, dr in zip(rows, d):
            lhs = abs(float(A[r] @ gv))
            assert lhs <= dr * ng * (1 + 1e-9), \
                f"row {r}: |c.g| = {lhs:.4e} > {dr * ng:.4e}"
            worst = max(worst, lhs / (dr * ng))
    print(f"[ok] (2) two-point dual valid on the continuum ball: "
          f"worst ratio {worst:.4f} <= 1 over 24 x 5 checks")


def test_modelling_identity():
    """(3) DF - L = diag(1/(X(1+X^2))) - H/(1+X^2), exactly."""
    worst = 0.0
    for J in (300, 900):
        col = Collocation(J)
        E = col.jacobian_matrix(col.anchor(), C_ANCHOR) - _far_field_model(col)
        claim = (np.diag(1.0 / (col.X * (1.0 + col.X ** 2)))
                 - col.H / (1.0 + col.X ** 2)[:, None])
        worst = max(worst, float(np.abs(E - claim).max()) / float(np.abs(E).max()))
    assert worst < 1e-13, f"identity relative error {worst:.3e}"
    print(f"[ok] (3) far-field modelling identity exact to {worst:.2e} (relative)")


def _unit_ball_family(col, alpha, gamma, rng, n_random=6):
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    raw = [(1.0 + col.X ** 2) ** (-0.5 * a) for a in (alpha, alpha + 0.5, alpha + 1.5)]
    raw += [square_wave_partial_sum(col.theta, m) for m in (16, 64, 256)]
    for frac in (0.5, 0.8, 0.95):
        i = int(frac * (col.J - 1))
        raw.append(np.sign(col.H[i]) * (1.0 + col.X ** 2) ** (-0.5 * alpha))
    for _ in range(n_random):
        k = int(rng.integers(1, col.J // 4))
        raw.append(np.cos(k * col.theta) * (1.0 + col.X ** 2) ** (-0.5 * alpha))
    return [h / dom(h) for h in raw if dom(h) > 0], dom


def test_local_holder_envelope():
    """(4) the X-side Holder envelope dominates real increments."""
    col = Collocation(600)
    rng = np.random.default_rng(3)
    fam, _ = _unit_ball_family(col, ALPHA, GAMMA, rng)
    X = col.X
    idx = np.where(X < 60.0)[0]
    worst = 0.0
    for h in fam:
        for off in (1, 2, 4):
            j, k = idx[:-off], idx[off:]
            env = holder_local_X_constant(ALPHA, GAMMA, np.minimum(X[j], X[k]))
            worst = max(worst, float(
                (np.abs(h[k] - h[j]) / (env * np.abs(X[k] - X[j]) ** GAMMA)).max()))
    assert worst <= 1.0 + 1e-9, f"envelope violated, ratio {worst:.4f}"
    print(f"[ok] (4) local Holder envelope: worst ratio {worst:.4f} <= 1 "
          f"over {len(fam)} unit-ball elements")


def test_bounds_dominate():
    """(5) |H(h)| and the modelling error stay under their bounds on resolved nodes."""
    col = Collocation(1200)
    rng = np.random.default_rng(5)
    fam, _ = _unit_ball_family(col, ALPHA, GAMMA, rng)
    res = _resolved(col)

    # |H(h)(X)| at several resolved far-field nodes
    hits = []
    for Xt in (20.0, 60.0, 150.0):
        i = int(np.argmin(np.abs(col.X - Xt)))
        assert res[i], f"X={Xt} must be resolved at J={col.J}"
        bnd, _, _ = hilbert_farfield_bound(float(col.X[i]), ALPHA, GAMMA)
        meas = max(abs(float((col.H @ h)[i])) for h in fam)
        assert meas <= bnd, f"X={col.X[i]:.1f}: {meas:.3e} > {bnd:.3e}"
        hits.append((float(col.X[i]), meas, bnd))

    # sharp far-field constant, and finiteness at the origin (true value 0)
    b_far, _, _ = hilbert_farfield_bound(1e5, ALPHA, GAMMA)
    sharp = farfield_mass(ALPHA) / np.pi
    assert abs(1e5 * b_far / sharp - 1.0) < 0.02, \
        f"X*bound -> {1e5*b_far:.4f}, sharp {sharp:.4f}"
    b0, _, _ = hilbert_farfield_bound(1e-3, ALPHA, GAMMA)
    assert np.isfinite(b0) and b0 < 5.0, f"bound must stay finite at X->0, got {b0}"

    # the modelling error itself
    X0 = 20.0
    sel = (col.X >= X0) & res
    w_cod = col.w_codomain(ALPHA)
    E = col.jacobian_matrix(col.anchor(), C_ANCHOR) - _far_field_model(col)
    meas = max(float(np.max(w_cod[sel] * np.abs((E @ h)[sel]))) for h in fam)
    bd = farfield_modelling_error_bound(ALPHA, GAMMA, X0)
    assert meas <= bd["bound"], f"modelling {meas:.4e} > {bd['bound']:.4e}"

    cq = quadratic_constant_upper(ALPHA, GAMMA)
    assert np.isfinite(cq["C_Q_sup_upper"]) and cq["C_Q_sup_upper"] > 0
    print("[ok] (5) bounds dominate: "
          + "; ".join(f"|H| at X={X:.0f}: {m:.2e}<={b:.2e}" for X, m, b in hits)
          + f"; modelling at X0={X0:.0f}: {meas:.3e}<={bd['bound']:.3e}; "
          f"X*bound->{1e5*b_far:.3f} (sharp {sharp:.3f}); "
          f"C_Q_sup <= {cq['C_Q_sup_upper']:.3f}")


def test_decay_and_budget():
    """(6) the bound falls like X0^{alpha-2}; budget algebra correct."""
    X0s = [100.0, 400.0, 1600.0]
    ds = [farfield_modelling_error_bound(ALPHA, GAMMA, X0) for X0 in X0s]
    vals = [d["bound"] for d in ds]
    slope = float(np.polyfit(np.log(X0s), np.log(vals), 1)[0])
    assert abs(slope - (ALPHA - 2.0)) < 0.12, \
        f"decay {slope:.3f} vs predicted {ALPHA-2.0:.3f}"
    for X0, d in zip(X0s, ds):
        assert abs(d["argmax_X"] - X0) / X0 < 1e-9, "sup must sit at X0 for alpha<2"
    b = budget(0.0, 1e-12, 0.3, 13.0)
    assert b["closes"] and abs(b["Y0_max"] - 0.49 / 52.0) < 1e-9
    assert not budget(0.0, 0.0, 1.05, 13.0)["closes"]
    print(f"[ok] (6) modelling bound ~ X0^{slope:.3f} (predicted {ALPHA-2.0:.3f}), "
          f"{vals[0]:.3e} -> {vals[-1]:.3e}; budget algebra correct")


if __name__ == "__main__":
    test_discrete_ball_trap()
    test_two_point_dual_valid()
    test_modelling_identity()
    test_local_holder_envelope()
    test_bounds_dominate()
    test_decay_and_budget()
    print("\nALL NK-BOUNDS TESTS PASSED")
