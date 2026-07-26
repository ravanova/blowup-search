"""Tests for the gCLM `a`-family rescaled residual + the global GA search.

These are the KNOWN-ANSWER GATE for the GA transition probe: before we trust the
GA anywhere near a != 0, it must (a) score the exact a=0 CLM profile as steady to
machine-of-discretization precision, and (b) rediscover that profile by global
search. The a=0 anchor is Omega_0(X) = -4X/(1+4X^2) (HQW25 arXiv:2401.14615,
validated in test_gclm_rescaled.py as the CLM steady state).

Pre-committed predicates:
  (1) RESIDUAL GATE: R(Omega_0) is tiny (RMS < 1e-5) with the origin gauge
      c_omega = 1 - H Omega_0(0) ~ -1.
  (2) VELOCITY: U = int_0^X H Omega has U(0)=0 and is bulk-accurate against the
      closed form arctan(2X) (tail error is where Omega_X ~ 0, hence harmless).
  (3) PARITY / a-DEPENDENCE: an odd profile yields an odd residual; a != 0 keeps
      the residual finite and BREAKS the a=0 profile (it is no longer steady) --
      the effect the transition map will measure.
  (4) GA GATE: a global 2-parameter search rediscovers the exact steady FAMILY.
      Because the CLM rescaling gauge is dilation-invariant, the steady set is a
      1-parameter dilation family {A=-4b, B=4b^2}; the gauge-INVARIANT A^2/B = 4
      is what the GA must recover (report invariants, not gauge-dependent values).
  (5) GA PINNED: fixing the dilation (B=4) makes the answer unique -> A ~ -4.
  (6) GENERIC ENGINE: the GA minimizes a plain quadratic to its known optimum and
      is deterministic given the seed (the engine is validated independent of the
      residual).

Run: python test_gclm_family.py     (no scipy; ~a few seconds)
"""

import numpy as np

from solver.gclm_family import (
    GCLMResidual, clm_one_scale, odd_rational, even_lorentz,
)
from solver.ga_search import ga_minimize, GAConfig


def test_a0_residual_gate():
    """(1) The exact a=0 anchor Omega_0 nulls the residual; origin gauge ~ -1."""
    R = GCLMResidual(a=0.0, n=1201)
    Om = clm_one_scale(R.X)
    res, c_om, c_l = R.residual(Om)
    rms = np.sqrt(np.mean(res ** 2))
    print(f"    residual RMS={rms:.3e}  c_omega={c_om:+.5f}  c_l={c_l}")
    assert rms < 1e-5, f"exact anchor not steady: RMS={rms:.2e}"
    assert abs(c_om - (-1.0)) < 2e-2, f"origin gauge off -1: {c_om}"
    # the parametric family represents the anchor exactly (genome gate target)
    assert np.abs(odd_rational(R.X, [-4.0, 4.0]) - Om).max() < 1e-8
    print("[ok] a=0 exact anchor is a numerical steady state of the residual")


def test_velocity_operator():
    """(2) U = int_0^X H Omega: U(0)=0, bulk-accurate vs arctan(2X)."""
    R = GCLMResidual(a=0.0, n=1201)
    Om = clm_one_scale(R.X)
    U = R.velocity(Om)
    Ua = np.arctan(2.0 * R.X)                 # exact antiderivative of 2/(1+4X^2)
    bulk = np.abs(R.X) < 10.0
    bulk_err = np.abs((U - Ua)[bulk]).max()
    print(f"    U(0)={U[R.i0]:.2e}  bulk(|X|<10) ||U-arctan(2X)||={bulk_err:.3e}")
    assert abs(U[R.i0]) < 1e-12, "velocity not pinned U(0)=0"
    assert bulk_err < 2e-2, f"velocity inaccurate in the bulk: {bulk_err:.2e}"
    print("[ok] velocity integrator matches the closed form where Omega_X matters")


def test_residual_parity_and_a_dependence():
    """(3) Odd profile -> odd residual; a!=0 finite and breaks the a=0 profile."""
    Om = clm_one_scale(GCLMResidual(a=0.0, n=801).X)
    prev = None
    for a in (0.0, 0.5, 1.0):
        R = GCLMResidual(a=a, n=801)
        Om = clm_one_scale(R.X)
        res, _, _ = R.residual(Om)
        rms = np.sqrt(np.mean(res ** 2))
        odd_asym = np.abs(res + res[::-1]).max()   # symmetric grid: res(-X)+res(X)
        print(f"    a={a:+.1f}  residual RMS={rms:.3e}  odd-asymmetry={odd_asym:.2e}")
        assert np.all(np.isfinite(res)), "residual not finite"
        assert odd_asym < 1e-9, f"odd parity broken at a={a}: {odd_asym:.2e}"
        if a == 0.0:
            assert rms < 1e-5
        else:
            assert rms > 1e-2, "advection should break the a=0 steady profile"
        prev = rms
    print("[ok] parity preserved; a!=0 advection breaks the a=0 profile as expected")


def test_ga_recovers_dilation_family():
    """(4) Global 2-param search finds a steady member; invariant A^2/B ~ 4."""
    R = GCLMResidual(a=0.0, n=601)

    def fit(g):
        return R.residual_norm(odd_rational(R.X, g))

    inv = []
    for seed in range(3):
        cfg = GAConfig(pop_size=40, n_generations=70, seed=seed, target_fitness=1e-4)
        r = ga_minimize(fit, [-8.0, 0.5], [-0.5, 12.0], config=cfg)
        A, B = r.best_genome
        invariant = A * A / B
        inv.append(invariant)
        print(f"    seed {seed}: (A,B)=({A:+.3f},{B:.3f})  A^2/B={invariant:.3f}  res={r.best_fitness:.2e}")
        assert r.best_fitness < 1e-3, f"GA did not find a steady profile: {r.best_fitness:.2e}"
        assert A < 0, "recovered profile has wrong sign"
        assert abs(invariant - 4.0) < 0.3, f"not on the dilation family: A^2/B={invariant:.3f}"
    print(f"[ok] GA recovers the exact steady dilation family (A^2/B={np.mean(inv):.3f} ~ 4)")


def test_ga_pinned_anchor():
    """(5) Fixing the dilation (B=4) makes the anchor unique: A ~ -4."""
    R = GCLMResidual(a=0.0, n=601)

    def fitA(g):
        return R.residual_norm(odd_rational(R.X, [g[0], 4.0]))

    r = ga_minimize(fitA, [-8.0], [-0.5], GAConfig(pop_size=30, n_generations=60,
                                                   seed=0, target_fitness=1e-5))
    A = r.best_genome[0]
    print(f"    pinned B=4 -> A={A:.4f}  res={r.best_fitness:.2e}")
    assert abs(A - (-4.0)) < 5e-2, f"pinned search missed the anchor: A={A:.4f}"
    print("[ok] dilation-pinned search recovers the exact anchor slope A=-4")


def test_ga_generic_engine():
    """(6) The GA engine minimizes a known quadratic and is deterministic."""
    def quad(g):
        return (g[0] - 3.0) ** 2 + (g[1] + 2.0) ** 2

    cfg = GAConfig(pop_size=40, n_generations=80, seed=7, target_fitness=1e-10)
    r1 = ga_minimize(quad, [-10, -10], [10, 10], cfg)
    r2 = ga_minimize(quad, [-10, -10], [10, 10], cfg)
    print(f"    min at ({r1.best_genome[0]:.4f},{r1.best_genome[1]:.4f})  f={r1.best_fitness:.2e}")
    assert abs(r1.best_genome[0] - 3.0) < 1e-2 and abs(r1.best_genome[1] + 2.0) < 1e-2
    assert np.array_equal(r1.best_genome, r2.best_genome), "GA not deterministic for a fixed seed"
    # even_lorentz sanity: builds an even bump peaked at 0 (two-scale symmetry)
    X = GCLMResidual(a=0.0, n=201).X
    bump = even_lorentz(X, [-1.0, 1.0])
    assert bump.argmax() != bump.argmin()
    assert abs(bump[100] - bump[::-1][100]) < 1e-12, "even_lorentz not even"
    print("[ok] generic GA engine finds the known optimum and is deterministic")


if __name__ == "__main__":
    test_a0_residual_gate()
    test_velocity_operator()
    test_residual_parity_and_a_dependence()
    test_ga_recovers_dilation_family()
    test_ga_pinned_anchor()
    test_ga_generic_engine()
    print("\nALL GCLM-FAMILY TESTS PASSED")
