"""Gates for solver/weight_search.py -- Route-C-PILOT's fitness and its substrate.

The leg's whole claim is that a NUMBER can be trusted enough to optimise, so the gates
are the things that would make it untrustworthy:

  (1) THE LEDGER IS WELL-FORMED AND THE VERDICT COMES FROM IT.  Every precedent carries
      the fields the gate reads; `novelty_verdict()` computes rather than remembers, and
      the ADJACENT entries must be present -- the claim is narrow BY CONSTRUCTION.
  (2) THE SUBSTRATE HAS THE KNOWN ANSWER IT CLAIMS.  The closed-form CLM pair
      (Omega_0, H Omega_0) must null the continuum residual, and the discrete Newton
      solution must converge to Omega_0 under refinement.
  (3) F IS EXACTLY QUADRATIC.  F(z+v) = F(z) + DF v + Q(v,v) to machine precision, which
      is what makes Z_2 exact rather than a ball-radius estimate -- and it is a
      known-answer test of the analytic Jacobian that needs no finite differences.
  (4) THE FITNESS IS GAUGE-INVARIANT.  Scaling every weight by one constant must leave
      Y_0/budget unchanged -- the invariance the module derives, checked numerically, so
      a searcher cannot win by making the norm big.
  (5) THE ANALYTIC WALL IS WHERE THE MODULE SAYS.  The true profile's weighted sup norm
      must be finite at p+q = 1 and diverge past it, measured on the exact profile as
      the domain grows.
  (6) THE GAUGE IS LOAD-BEARING.  The naive-vs-tuned gain must exceed 1e3 under the
      implicit gauge and collapse under a gauge that pins c_l directly -- the ablation
      that says the weight effect lives in the border rows.
  (7) THE LOWER WALL IS REAL AND IT MOVES.  Z_1 must cross 1 at a finite far-field power,
      and that crossing must move UP under refinement: the float rehearsal's admissible
      band shrinks, which is why the C-PILOT gate reports FAIL.
  (8) THE GATE RUNS AND IS HONEST ABOUT ITSELF.  six_property_gate must return all six
      properties with their frozen thresholds attached, and its verdict must be the AND
      of them -- a gate whose verdict is not computed from its own properties is a
      decoration.

Run: .venv/bin/python test_weight_search.py
"""

import time

import numpy as np

from solver.weight_search import (
    BOX_LOWER, BOX_UPPER, EXACT_C_OMEGA, EXACT_SLOPE0, GENE_NAMES, PRECEDENTS,
    WALL_POWER, BorderedCLM, FitnessEngine, exact_hilbert, exact_profile,
    hand_weights, lower_wall, novelty_verdict, six_property_gate,
)


def test_ledger_and_verdict():
    """(1) The ledger is well formed and the gate is computed off it."""
    fields = {"id", "who", "what", "object_searched", "verdict", "why_not_preempting"}
    for p in PRECEDENTS:
        assert fields <= set(p), f"precedent {p.get('id')} missing {fields - set(p)}"
        assert p["verdict"] in {"PRE_EMPTS", "ADJACENT", "EXCLUSION", "PREMISE_CONFIRMED"}
        assert len(p["why_not_preempting"]) > 40, "a one-word reason is not a reason"
    answer, note, entries = novelty_verdict()
    assert answer in {"PRE_EMPTED", "PROCEED_NARROW"}
    adj = [p for p in PRECEDENTS if p["verdict"] == "ADJACENT"]
    assert adj, "the ledger must carry the adjacent field, or the claim is not narrow"
    assert any(p["verdict"] == "PREMISE_CONFIRMED" for p in PRECEDENTS)
    print(f"[ok] (1) ledger {len(PRECEDENTS)} entries, verdict {answer} computed off it")


def test_known_answer_substrate():
    """(2) The closed-form profile nulls the residual, and Newton converges to it."""
    pr = BorderedCLM(n=401)
    assert np.abs(pr.H @ exact_profile(pr.X) - exact_hilbert(pr.X)).max() < 5e-3, \
        "the discrete Hilbert transform does not reproduce its own closed form"
    R = pr.F(pr.exact_state())[:pr.n]
    assert np.sqrt(np.mean(R ** 2)) < 1e-3, "the exact profile is not near-steady"
    dists, floors = [], []
    for n in (201, 401, 801):
        p = BorderedCLM(n=n)
        z, info = p.newton()
        assert info["converged"], f"Newton did not converge at n={n}"
        # and the residual it reaches is at the ARITHMETIC floor, not merely under a
        # hard-coded constant: the float64 evaluation noise of F GROWS with n and
        # passes 1e-14 around n = 800, so a fixed tolerance there tests the arithmetic
        # rather than the solve (banked lesson 86).
        assert len(info["residual_ladder"]) - 1 <= 4, \
            f"Newton took {len(info['residual_ladder']) - 1} iterations at n={n}"
        assert info["residual_ladder"][-1] <= info["residual_floor"], \
            f"n={n}: residual {info['residual_ladder'][-1]:.2e} is above the measured " \
            f"evaluation floor {info['residual_floor']:.2e} -- a real solve failure"
        floors.append(info["residual_floor"])
        dists.append(float(np.abs(z[:p.n] - exact_profile(p.X)).max()))
        assert abs(z[p.n] - 1.0) < 1e-2, "c_l is not recovered near its exact value"
        assert abs(z[p.n + 1] - EXACT_C_OMEGA) < 1e-2, "c_omega is not recovered"
    assert dists[0] > dists[1] > dists[2], f"no convergence to the exact profile: {dists}"
    assert floors[0] < floors[1] < floors[2], \
        f"the evaluation floor is supposed to grow with n: {floors}"
    print(f"[ok] (2) |Omega - Omega_0|_sup falls "
          + " -> ".join(f"{d:.2e}" for d in dists) + " over n = 201, 401, 801; "
          "residual floor " + " -> ".join(f"{f:.1e}" for f in floors))


def test_exactly_quadratic():
    """(3) F(z+v) = F(z) + DF v + Q(v,v) to machine precision."""
    pr = BorderedCLM(n=151)
    rng = np.random.default_rng(0)
    z = pr.exact_state()
    worst = 0.0
    for _ in range(5):
        v = rng.standard_normal(pr.N) * 0.1
        lhs = pr.F(z + v)
        rhs = pr.F(z) + pr.jacobian(z) @ v + pr.quadratic(v)
        worst = max(worst, float(np.abs(lhs - rhs).max() / max(np.abs(lhs).max(), 1e-300)))
    assert worst < 1e-12, f"F is not exactly quadratic: rel {worst:.2e}"
    print(f"[ok] (3) exact quadratic identity to {worst:.2e} relative -- Z_2 is exact")


def test_fitness_gauge_invariance():
    """(4) Y_0/budget is invariant under a global rescaling of the norm."""
    pr = BorderedCLM(n=201)
    z, _ = pr.newton()
    base = np.array([0.4, 0.3, -0.1, 1.0, -2.0])
    c0 = pr.certificate_constants(z, base)
    ratio0 = c0["Y0"] / c0["budget"]
    worst = 0.0
    for s in (1e-3, 1e-1, 10.0, 1e3):
        # a global scale is exactly a shift of w_om, w_l and nu together; nu carries it
        # through an added constant power, so it is applied to the weight vector here
        w, nu = pr.weight_vector(base)
        w2, nu2 = w * s, nu * s
        Fz, J = pr.F(z), pr.jacobian(z)
        A = np.linalg.inv(J)
        Y0 = float(np.max(w2 * np.abs(A @ Fz)))
        Z1 = float(np.max(w2 * (np.abs(np.eye(pr.N) - A @ J) @ (1.0 / w2))))
        A_n = float(np.max(w2 * (np.abs(A) @ (1.0 / w2))))
        H_ni = float(np.max(np.abs(pr.H) @ (1.0 / nu2)))
        XD_nn = float(np.max(nu2 * (np.abs(pr.XD) @ (1.0 / nu2))))
        B = H_ni + 1.0 / w2[pr.n + 1] + XD_nn / w2[pr.n]
        Z2 = 2.0 * A_n * B
        ratio = Y0 / ((1.0 - Z1) ** 2 / (2.0 * Z2))
        worst = max(worst, abs(ratio / ratio0 - 1.0))
    assert worst < 1e-10, f"the fitness is not gauge invariant: rel {worst:.2e}"
    print(f"[ok] (4) fitness invariant under global weight scaling to {worst:.2e}")


def test_analytic_wall():
    """(5) The true profile's weighted sup norm is finite at p+q = 1 and blows up past."""
    norms = {}
    for power in (0.5, WALL_POWER, 1.5):
        vals = []
        for rho_max in (6.0, 8.0, 10.0):
            pr = BorderedCLM(n=201, rho_max=rho_max)
            nu = (1.0 + pr.X ** 2) ** (0.5 * power)
            vals.append(float(np.max(nu * np.abs(exact_profile(pr.X)))))
        norms[power] = vals
    assert norms[0.5][-1] / norms[0.5][0] < 1.05, "the p<1 norm should be reach-independent"
    assert norms[WALL_POWER][-1] / norms[WALL_POWER][0] < 1.05, \
        "at the wall the sup norm should still be finite"
    # past the wall the growth rate is itself a known answer: |Omega_0| ~ 1/X, so
    # sup nu|Omega_0| ~ X_max^(p-1) and the ratio over a 54.6x reach is 54.6^0.5
    growth = norms[1.5][-1] / norms[1.5][0]
    reach = BorderedCLM(n=201, rho_max=10.0).Xmax / BorderedCLM(n=201, rho_max=6.0).Xmax
    predicted = reach ** (1.5 - 1.0)
    assert abs(growth / predicted - 1.0) < 0.02, \
        f"past the wall the norm must diverge as X_max^(p-1): {growth:.2f} vs {predicted:.2f}"
    print(f"[ok] (5) wall at p+q = {WALL_POWER}: norm flat below/at it; above it "
          f"x{growth:.2f} with reach against the predicted x{predicted:.2f}")


def test_gauge_is_load_bearing():
    """(6) The weight effect lives in the border rows, not in the weight family."""
    pr = BorderedCLM(n=201)
    z, _ = pr.newton()
    eng = FitnessEngine(pr, z)
    hw = hand_weights()
    gain = 10.0 ** (eng.fitness(hw["naive"]) - eng.fitness(hw["tuned_leg46"]))
    assert gain > 1e3, f"leg 46's premise does not reproduce here: {gain:.2f}x"
    from experiments.p2_route_c_pilot_v0 import _stiff_gauge_gain
    stiff = _stiff_gauge_gain(201)
    assert stiff["gain"] < 10.0, \
        f"the stiff gauge should kill the effect, got {stiff['gain']:.2f}x"
    print(f"[ok] (6) naive->tuned gain {gain:.0f}x under the implicit gauge, "
          f"{stiff['gain']:.2f}x when c_l is pinned")


def test_lower_wall_moves_with_resolution():
    """(7) Z_1 crosses 1 at a finite far-field power, and the crossing rises with n."""
    walls = []
    for n in (201, 401, 801):
        pr = BorderedCLM(n=n)
        z, _ = pr.newton()
        walls.append(lower_wall(FitnessEngine(pr, z)))
    assert all(np.isfinite(walls)), "no crossing found"
    assert walls[0] < walls[1] < walls[2], f"the band should shrink under refinement: {walls}"
    assert walls[-1] < WALL_POWER, "the band is already empty at n=801, which it is not"
    print(f"[ok] (7) lower wall p_- = " + ", ".join(f"{w:+.3f}" for w in walls)
          + " at n = 201, 401, 801 -- the admissible band shrinks")


def test_gate_is_computed_from_its_properties():
    """(8) The gate returns six properties with thresholds, and ANDs them."""
    rep = six_property_gate(BorderedCLM(n=201), BorderedCLM(n=401),
                            n_random=8, seed=0, per_gene=5, refine=1)
    props = rep["properties"]
    assert len(props) == 6, f"expected six properties, got {len(props)}"
    for k, v in props.items():
        assert "pass" in v and isinstance(v["pass"], bool), f"{k} has no boolean"
        assert any("threshold" in a for a in v), f"{k} carries no threshold"
    expected = "PASS" if all(v["pass"] for v in props.values()) else "FAIL"
    assert rep["verdict"] == expected, "the verdict is not the AND of the properties"
    assert len(rep["single_predictor_r2"]) == len(GENE_NAMES) + 1
    print(f"[ok] (8) gate returns 6/6 properties with thresholds; verdict "
          f"{rep['verdict']} == AND of them")


if __name__ == "__main__":
    t0 = time.time()
    test_ledger_and_verdict()
    test_known_answer_substrate()
    test_exactly_quadratic()
    test_fitness_gauge_invariance()
    test_analytic_wall()
    test_gauge_is_load_bearing()
    test_lower_wall_moves_with_resolution()
    test_gate_is_computed_from_its_properties()
    print(f"\nall weight-search gates pass ({time.time() - t0:.1f}s)")
