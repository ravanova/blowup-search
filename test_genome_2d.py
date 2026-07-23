"""Tests for the smooth 2D genome (ga/genome2d_smooth.py, Gate 3) and its
nu_crit-analog fitness wiring (ga/fitness2d.py). The 2D analog of test_ga.py's
genome invariants, following test_genome_rough_2d.py:

  - realized fields sit in the correct parity subspace (odd-x/odd-y for omega,
    even-x/odd-y for theta) and hit the total energy budget,
  - the joint energy normalization is idempotent and amplitude-scale invariant
    (the genome-hash / fitness-cache key property),
  - random draws and realization are deterministic under a fixed seed,
  - the four descriptors land in their ranges and respond correctly to known
    shapes (x-heavy -> anisotropy > 0, low modes -> small centroid, etc.),
  - the bandwidth-vs-grid guard fires,
  - a light fitness smoke: a non-buoyant (2D Euler) control conserves max|omega|
    -> amp ~ 1 < A_CRIT -> nu_crit censored low (the anti-self-deception anchor,
    one cheap solver run).

Run: .venv/bin/python test_genome_2d.py
"""

import numpy as np

from ga.fitness2d import nu_crit
from ga.genome2d import ENERGY_BUDGET_2D, energy2d
from ga.genome2d_smooth import (
    MAP_ELITES_2D,
    TOTAL_BUDGET_2D,
    Genome2D,
    genome2d_hash,
    normalize,
    random_genome,
    realize,
    shape_descriptors,
)
from solver.boussinesq import grid2d, parity_residual


def _rng(seed=0):
    return np.random.default_rng(seed)


def test_realized_fields_parity_and_energy():
    rng = _rng(1)
    for _ in range(6):
        g = random_genome(rng)
        om, th = realize(g, 128)
        assert parity_residual(om, "odd_odd") < 1e-12, "omega parity"
        assert parity_residual(th, "even_odd") < 1e-12, "theta parity"
        total = energy2d(om) + energy2d(th)
        assert abs(total - TOTAL_BUDGET_2D) < 1e-9, (total, TOTAL_BUDGET_2D)


def test_split_half_puts_each_field_at_budget():
    # A genome with equal raw energy in omega and theta normalizes to split=0.5,
    # each field then carrying ENERGY_BUDGET_2D (the ga/genome2d.py convention).
    K = 4
    a = np.zeros((K, K)); a[0, 0] = 1.0            # sin x sin y
    b = np.zeros((K + 1, K)); b[1, 0] = 1.0        # cos x sin y (same L2 weight)
    g = Genome2D(a=a, b=b)
    d = shape_descriptors(g)
    assert abs(d["split"] - 0.5) < 1e-12, d["split"]
    om, th = realize(g, 128)
    assert abs(energy2d(om) - ENERGY_BUDGET_2D) < 1e-9
    assert abs(energy2d(th) - ENERGY_BUDGET_2D) < 1e-9


def test_normalize_idempotent_and_scale_invariant():
    rng = _rng(2)
    for _ in range(5):
        g = random_genome(rng)
        # idempotent: already normalized, re-normalizing changes nothing
        g2 = normalize(g)
        assert np.max(np.abs(g2.a - g.a)) < 1e-12
        assert np.max(np.abs(g2.b - g.b)) < 1e-12
        # energy hits budget
        e_om, e_th = energy2d(realize(g, 96)[0]), energy2d(realize(g, 96)[1])
        assert abs(e_om + e_th - TOTAL_BUDGET_2D) < 1e-9
        # amplitude-scale invariance: a 3.7x raw copy normalizes back to the
        # same coeffs (up to float rounding -- not bytewise, so not the same
        # hash; the cache keys on byte-identical genomes, as in 1D).
        gs = normalize(Genome2D(a=3.7 * g.a, b=3.7 * g.b))
        assert np.max(np.abs(gs.a - g.a)) < 1e-10
        assert np.max(np.abs(gs.b - g.b)) < 1e-10
        # the hash is deterministic on identical bytes and distinguishes shapes
        assert genome2d_hash(g) == genome2d_hash(Genome2D(a=g.a.copy(), b=g.b.copy()))


def test_determinism():
    a1 = random_genome(_rng(7))
    a2 = random_genome(_rng(7))
    assert np.array_equal(a1.a, a2.a) and np.array_equal(a1.b, a2.b)
    # realization is bytewise deterministic
    o1, t1 = realize(a1, 128)
    o2, t2 = realize(a2, 128)
    assert np.array_equal(o1, o2) and np.array_equal(t1, t2)
    # a different seed gives a different genome
    b = random_genome(_rng(8))
    assert not np.array_equal(a1.a, b.a)


def test_descriptor_ranges():
    rng = _rng(3)
    for _ in range(50):
        d = shape_descriptors(random_genome(rng))
        assert -1.0 <= d["anisotropy"] <= 1.0, d
        lo, hi = MAP_ELITES_2D["descriptor_bounds"]["centroid"]
        assert lo - 1e-9 <= d["centroid"] <= hi + 1e-9, d
        assert 0.0 < d["split"] < 1.0, d
        assert -1.0 <= d["alignment"] <= 1.0, d


def test_anisotropy_known_shapes():
    K = 4
    b = np.zeros((K + 1, K)); b[0, 0] = 1.0
    # pure sin(4x) sin(1y): x-heavy -> anisotropy = (16-1)/(16+1) > 0
    a = np.zeros((K, K)); a[3, 0] = 1.0
    assert abs(shape_descriptors(Genome2D(a=a.copy(), b=b))["anisotropy"]
               - 15.0 / 17.0) < 1e-12
    # pure sin(1x) sin(4y): y-heavy -> negative mirror
    a = np.zeros((K, K)); a[0, 3] = 1.0
    assert abs(shape_descriptors(Genome2D(a=a.copy(), b=b))["anisotropy"]
               + 15.0 / 17.0) < 1e-12
    # j==k is isotropic
    a = np.zeros((K, K)); a[2, 2] = 1.0
    assert abs(shape_descriptors(Genome2D(a=a.copy(), b=b))["anisotropy"]) < 1e-12


def test_centroid_known_shapes():
    K = 4
    b = np.zeros((K + 1, K)); b[0, 0] = 1.0
    # lowest mode (1,1) -> centroid = sqrt(2) (the minimum)
    a = np.zeros((K, K)); a[0, 0] = 1.0
    assert abs(shape_descriptors(Genome2D(a=a.copy(), b=b))["centroid"]
               - np.sqrt(2.0)) < 1e-12
    # highest mode (4,4) -> centroid = sqrt(32) (the maximum)
    a = np.zeros((K, K)); a[3, 3] = 1.0
    assert abs(shape_descriptors(Genome2D(a=a.copy(), b=b))["centroid"]
               - np.sqrt(32.0)) < 1e-12


def test_alignment_sign():
    # omega = sin x sin y; theta = cos x sin y -> theta_x = -sin x sin y = -omega,
    # so the buoyancy torque is perfectly anti-aligned: alignment = -1.
    K = 4
    a = np.zeros((K, K)); a[0, 0] = 1.0
    b = np.zeros((K + 1, K)); b[1, 0] = 1.0
    assert abs(shape_descriptors(Genome2D(a=a, b=b))["alignment"] + 1.0) < 1e-10
    # flip theta sign -> perfectly aligned: alignment = +1.
    b = np.zeros((K + 1, K)); b[1, 0] = -1.0
    assert abs(shape_descriptors(Genome2D(a=a, b=b))["alignment"] - 1.0) < 1e-10


def test_descriptor_grid_resolution_free():
    # anisotropy/centroid are analytic; split/alignment must not move with the
    # (internal) descriptor grid. Recompute on a finer grid via a temporary field
    # build and confirm agreement is exact for bandlimited K<<N/2.
    rng = _rng(9)
    g = random_genome(rng)
    d = shape_descriptors(g)
    # realize at two resolutions and check the split (energy ratio) is stable
    om1, th1 = realize(g, 96)
    om2, th2 = realize(g, 192)
    s1 = energy2d(th1) / (energy2d(om1) + energy2d(th1))
    s2 = energy2d(th2) / (energy2d(om2) + energy2d(th2))
    assert abs(s1 - s2) < 1e-10 and abs(s1 - d["split"]) < 1e-9


def test_bandwidth_exceeds_grid_raises():
    g = random_genome(_rng(4))  # K=4
    # N=9 -> dealiased band k <= 9//3 = 3 < 4: must refuse
    try:
        realize(g, 9)
        raise AssertionError("expected ValueError for K=4 at N=9")
    except ValueError:
        pass
    # N=12 -> band k <= 4 exactly: allowed
    realize(g, 12)


def test_zero_omega_rejected():
    K = 4
    a = np.zeros((K, K))
    b = np.zeros((K + 1, K)); b[0, 0] = 1.0
    try:
        shape_descriptors(Genome2D(a=a, b=b))
        raise AssertionError("expected ValueError for zero-omega genome")
    except ValueError:
        pass


def test_fitness_nonbuoyant_control_censored_low():
    # 2D Euler (buoyancy off): vorticity is materially conserved, so max|omega|
    # does not amplify -> amp ~ 1 < A_CRIT at nu=0 -> the bisection censors the
    # low edge with nu_crit = 0. The anti-self-deception anchor: the fitness must
    # respond to the buoyancy mechanism, not merely to carrying a vortex. One
    # cheap solver run (N=64, short t_max).
    g = random_genome(_rng(5))
    om, th = realize(g, 64)
    cfg = {"t_max": 2.0, "max_steps": 1500}
    bis = nu_crit(om, th, config=cfg, buoyancy=False)
    assert bis["bracket_censored"] == "low", bis
    assert bis["critical_value"] == 0.0, bis["critical_value"]
    # the single nu=0 run must indeed be sub-A_CRIT
    amp0 = bis["runs"][0]["amp"]
    assert amp0 < 2.0, amp0


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
