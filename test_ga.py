"""Tests for the Stage 2 GA harness (ga/genome.py, ga/operators.py,
ga/fitness.py, ga/evolve.py).

The first test is the one PLAN.md's open-risks section explicitly demands:
energy renormalization is applied after EVERY genetic operator and after the
k^{-p} envelope, so the GA cannot cheat by scaling amplitude. The
sin(x) fitness test is a regression pin against Stage 1.5's measured
nu_crit(sin) = 0.0527 (STAGE_1_5_RESULTS.md). The end-to-end test drives the
real ExperimentWriter + worker pool on a tiny configuration in a temp repo.
"""

import json
import multiprocessing
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from ga.evolve import DEFAULT_CONFIG, Archive, Evolver, literature_genomes, run
from ga.fitness import bisect_critical, evaluate_genome
from ga.genome import (
    ENERGY_BUDGET,
    Genome,
    effective_coeffs,
    from_sine_pairs,
    normalize,
    project_to_sines,
    random_genome,
    realize,
    shape_descriptors,
)
from ga.logbook import ExperimentWriter, genome_hash
from ga.operators import blend_crossover, mutate, tournament_select
from solver.spectral_utils import energy, grid

RNG = np.random.default_rng(20260722)


def _realized_energy(g, n_grid=256):
    return energy(realize(g, n_grid))


# --- energy renormalization (the PLAN.md-mandated unit test) ----------------


def test_energy_renormalized_after_every_operator_and_envelope():
    p_range = [0.0, 3.5]
    g = random_genome(RNG, 32, p_range)
    assert abs(_realized_energy(g) - ENERGY_BUDGET) < 1e-10, "after init"

    m = mutate(g, RNG, scale=0.5, p_scale=0.3, p_range=p_range)
    assert abs(_realized_energy(m) - ENERGY_BUDGET) < 1e-10, "after mutation"

    g2 = random_genome(RNG, 32, p_range)
    c = blend_crossover(g, g2, RNG)
    assert abs(_realized_energy(c) - ENERGY_BUDGET) < 1e-10, "after crossover"

    # After the envelope: changing p redistributes energy across modes; the
    # renormalization must hit the budget POST-envelope, not pre-envelope.
    reshaped = normalize(Genome(coeffs=np.array(g.coeffs),
                                envelope_p=g.envelope_p + 1.7))
    assert abs(_realized_energy(reshaped) - ENERGY_BUDGET) < 1e-10, \
        "after envelope change"
    # And the envelope genuinely moved energy (different field, same energy).
    assert not np.allclose(realize(reshaped, 256), realize(g, 256))


def test_bandwidth_cap_enforced_after_every_operator():
    # Stage 2.5 candidate B: energy fraction in k <= k_max capped at
    # normalization; both the cap AND the energy budget must hold after
    # every operator (PLAN.md Stage 2.5's mandated unit test).
    cap = {"k_max": 2, "max_frac": 0.5}
    p_range = [0.0, 3.5]

    def low_frac(g):
        b = effective_coeffs(g, ENERGY_BUDGET, cap)
        return float(np.sum(b[:cap["k_max"]] ** 2) / np.sum(b * b))

    def check(g, label):
        assert abs(energy(realize(g, 256, ENERGY_BUDGET, cap))
                   - ENERGY_BUDGET) < 1e-10, f"energy after {label}"
        assert low_frac(g) <= cap["max_frac"] + 1e-9, f"cap after {label}"

    # A deliberately low-k-heavy genome: sin(x) + a whisper of sin(5x).
    heavy = normalize(Genome(coeffs=np.array([1.0, 0, 0, 0, 0.05] + [0.0] * 27),
                             envelope_p=0.0), ENERGY_BUDGET, cap)
    check(heavy, "normalize")
    assert abs(low_frac(heavy) - cap["max_frac"]) < 1e-9, \
        "over-cap genome projects exactly onto the cap boundary"
    # Idempotent: re-normalizing a capped genome is the identity.
    again = normalize(heavy, ENERGY_BUDGET, cap)
    assert np.allclose(again.coeffs, heavy.coeffs, rtol=1e-10)

    g = random_genome(RNG, 32, p_range, ENERGY_BUDGET, cap)
    check(g, "init")
    check(mutate(g, RNG, 0.5, 0.3, p_range, ENERGY_BUDGET, cap), "mutation")
    check(blend_crossover(g, heavy, RNG, ENERGY_BUDGET, cap), "crossover")

    # An under-cap genome passes through the cap unchanged.
    rough = normalize(Genome(coeffs=np.ones(32), envelope_p=0.0),
                      ENERGY_BUDGET)
    assert np.allclose(normalize(rough, ENERGY_BUDGET, cap).coeffs,
                       rough.coeffs, rtol=1e-10)

    # Pure low-band data cannot satisfy the cap: infeasible, not zeroed.
    try:
        normalize(Genome(coeffs=np.array([1.0] + [0.0] * 31), envelope_p=0.0),
                  ENERGY_BUDGET, cap)
        raise AssertionError("pure-sin(x) genome must be infeasible under cap")
    except ValueError:
        pass

    # literature_genomes skips infeasible profiles instead of crashing.
    labels = [label for label, _ in literature_genomes(32, ENERGY_BUDGET, cap)]
    assert "sin(x)" not in labels and "sin(2x)" not in labels
    assert any(label.startswith("tail") for label in labels)


def test_normalize_and_hash_identity():
    # Amplitude-rescaled copies of a shape normalize back to the same
    # coefficients (up to float rounding): amplitude carries no identity.
    g = random_genome(RNG, 16, [0.5, 2.0])
    scaled = Genome(coeffs=np.array(g.coeffs) * 7.31, envelope_p=g.envelope_p)
    assert np.allclose(normalize(scaled).coeffs, g.coeffs, rtol=1e-12)
    # The bitwise cache identity: byte-identical genomes hash equal, and the
    # envelope exponent is part of the identity.
    assert genome_hash(g.coeffs, g.envelope_p) == \
        genome_hash(np.array(g.coeffs), g.envelope_p)
    assert genome_hash(g.coeffs, g.envelope_p) != \
        genome_hash(g.coeffs, g.envelope_p + 0.1)


def test_literature_resampling():
    # sin(x) has L2 energy exactly ENERGY_BUDGET: re-sampled genome must
    # reproduce it on the grid.
    g = from_sine_pairs([(1, 1.0)], 8)
    x = grid(256)
    assert np.allclose(realize(g, 256), np.sin(x), atol=1e-12)
    # Projection of the bump profile matches the (normalized) analytic field.
    kappa = 2.0
    fn = lambda x: np.sin(x) * np.exp(kappa * (np.cos(x) - 1.0))
    g = project_to_sines(fn, 32)
    w_ref = fn(x)
    w_ref *= np.sqrt(ENERGY_BUDGET / energy(w_ref))
    assert np.max(np.abs(realize(g, 256) - w_ref)) < 1e-6
    # Every literature profile hits the budget after re-sampling.
    for label, g in literature_genomes(32, ENERGY_BUDGET):
        assert abs(_realized_energy(g) - ENERGY_BUDGET) < 1e-10, label


def test_shape_descriptors():
    d = shape_descriptors(from_sine_pairs([(1, 1.0)], 32))
    assert d["n_sign_changes"] == 2
    assert d["energy_top_k_frac"] == 1.0
    # Steeper envelope -> more negative tail slope, monotonically.
    coeffs = RNG.standard_normal(32)
    slopes = [shape_descriptors(normalize(Genome(coeffs.copy(), p)))
              ["spectral_tail_slope"] for p in (0.0, 1.0, 2.0, 3.0)]
    assert all(s2 < s1 for s1, s2 in zip(slopes, slopes[1:])), slopes


# --- bisection oracle -------------------------------------------------------


_BISECT_CFG = {
    "range": [0.0, 0.1],
    "tolerance": 1e-3,
    "warm_start": {"margin": 0.01, "fallback": "full_range"},
    "probe_fractions": [0.05, 0.15],
    "max_iters": 30,
}


def _oracle(critical, pocket=None):
    def run_at(param):
        blow = param < critical or (pocket is not None
                                    and pocket[0] < param < pocket[1])
        return blow, {"outcome": "stub", "early_exit_reason": None,
                      "t_final": 0.0, "n_timesteps": 0, "dt_min": 0.0,
                      "conservation_drift": 0.0, "wall_clock_seconds": 0.0,
                      "estimate": None, "fit_below_floor": False}
    return run_at


def test_bisection_recovers_critical_value():
    out = bisect_critical(_oracle(0.0333), _BISECT_CFG)
    assert out["bracket_censored"] is None
    assert abs(out["critical_value"] - 0.0333) <= 1e-3
    assert out["critical_value_monotone"] is True
    assert out["n_bracket_expansions"] == 0
    assert out["initial_bracket"] == [0.0, 0.1]


def test_bisection_warm_start_narrows_and_expands():
    # Good warm center: far fewer runs than the cold bisection.
    cold = bisect_critical(_oracle(0.0333), _BISECT_CFG)
    warm = bisect_critical(_oracle(0.0333), _BISECT_CFG, warm_center=0.03)
    assert abs(warm["critical_value"] - 0.0333) <= 1e-3
    assert warm["n_bracket_expansions"] == 0
    assert len(warm["runs"]) < len(cold["runs"])
    assert np.allclose(warm["initial_bracket"], [0.02, 0.04])

    # Bad warm center (both warm edges regular): the failed edge becomes the
    # new upper bound — one expansion, and the answer still comes back right.
    bad = bisect_critical(_oracle(0.0333), _BISECT_CFG, warm_center=0.08)
    assert abs(bad["critical_value"] - 0.0333) <= 1e-3
    assert bad["n_bracket_expansions"] == 1

    # Warm center below the true critical (both warm edges blow up).
    low = bisect_critical(_oracle(0.0333), _BISECT_CFG, warm_center=0.005)
    assert abs(low["critical_value"] - 0.0333) <= 1e-3
    assert low["n_bracket_expansions"] == 1


def test_bisection_censoring():
    never = bisect_critical(_oracle(-1.0), _BISECT_CFG)  # never blows up
    assert never["bracket_censored"] == "low"
    assert never["critical_value"] == 0.0

    always = bisect_critical(_oracle(2.0), _BISECT_CFG)  # always blows up
    assert always["bracket_censored"] == "high"
    assert always["critical_value"] == 0.1

    # Censored even when the warm bracket said otherwise first.
    warm_low = bisect_critical(_oracle(-1.0), _BISECT_CFG, warm_center=0.05)
    assert warm_low["bracket_censored"] == "low"
    assert warm_low["n_bracket_expansions"] == 1


def test_bisection_probes_catch_non_monotone_response():
    # Blow-up pocket beyond the located critical value, positioned where the
    # first probe (critical + 0.05 * range width) lands.
    out = bisect_critical(_oracle(0.01, pocket=(0.014, 0.018)), _BISECT_CFG)
    assert abs(out["critical_value"] - 0.01) <= 1e-3
    assert out["critical_value_monotone"] is False


# --- fitness evaluation (regression pin against Stage 1.5) ------------------


def _stage2_config(**overrides):
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    cfg["random_seed"] = 1
    cfg.update(overrides)
    return cfg


def test_evaluate_genome_reproduces_stage1_5_sin_nu_crit():
    cfg = _stage2_config()
    g = from_sine_pairs([(1, 1.0)], cfg["genome_length_N"])
    task = {"coeffs": g.coeffs, "envelope_p": g.envelope_p,
            "genome_id": "t-sin", "operator": "init", "parent_ids": [],
            "warm_center": None, "generation_index": 0, "config": cfg,
            "sink": None}
    row = evaluate_genome(task)
    # Stage 1.5 measured nu_crit(sin) = 0.0527 in [0,1] at tol 3.9e-3; the
    # Stage 2 bracket/tolerance differ, so agreement is to the coarser tol.
    assert row["bracket_censored"] is None
    assert abs(row["critical_value"] - 0.0527) < 4e-3, row["critical_value"]
    assert row["critical_value_monotone"] is True
    assert row["fitness_resolution_N"] == 256
    assert row["fitness_axis"] == "nu_crit"
    assert row["energy"] == ENERGY_BUDGET or \
        abs(row["energy"] - ENERGY_BUDGET) < 1e-10
    assert row["best_estimate"] is not None
    assert row["shape_descriptors"]["n_sign_changes"] == 2

    # Warm-started re-evaluation: same answer, fewer solver runs.
    task2 = dict(task, genome_id="t-sin-warm",
                 warm_center=row["critical_value"])
    row2 = evaluate_genome(task2)
    assert abs(row2["critical_value"] - row["critical_value"]) <= 1e-3
    assert row2["n_solver_runs"] < row["n_solver_runs"]
    assert row2["n_bracket_expansions"] == 0


# --- archive + cache --------------------------------------------------------


def _payload(genome_id, fitness, censored=None, monotone=True,
             descriptors=None):
    return {
        "genome_id": genome_id, "critical_value": fitness,
        "bracket_censored": censored, "critical_value_monotone": monotone,
        "shape_descriptors": descriptors or
        {"spectral_tail_slope": -2.0, "n_sign_changes": 4,
         "energy_top_k_frac": 0.9},
    }


def test_archive_insertion_rules():
    archive = Archive(DEFAULT_CONFIG["ga_operators"]["map_elites"])
    g = random_genome(RNG, 8, [0.0, 3.5])

    ok, cell, displaced = archive.maybe_insert(_payload("a", 0.02), g)
    assert ok and displaced is None

    # Censored fitness never enters (LOGGING.md schema #3).
    ok, _, _ = archive.maybe_insert(_payload("b", 0.09, censored="high"), g)
    assert not ok
    # Non-monotone fitness signal is broken; never enters.
    ok, _, _ = archive.maybe_insert(_payload("c", 0.09, monotone=False), g)
    assert not ok
    # Worse fitness in the same cell does not displace.
    ok, _, _ = archive.maybe_insert(_payload("d", 0.01), g)
    assert not ok
    # Better fitness displaces and reports the displaced elite.
    ok, cell2, displaced = archive.maybe_insert(_payload("e", 0.03), g)
    assert ok and cell2 == cell and displaced == "a"
    # Different descriptors -> different cell, coexists.
    ok, cell3, _ = archive.maybe_insert(_payload(
        "f", 0.001, descriptors={"spectral_tail_slope": 0.5,
                                 "n_sign_changes": 30,
                                 "energy_top_k_frac": 0.5}), g)
    assert ok and cell3 != cell
    assert len(archive.cells) == 2
    assert abs(archive.qd_score() - 0.031) < 1e-12

    # Out-of-range descriptors clip into edge cells, never crash.
    assert archive.cell_of({"spectral_tail_slope": -99.0,
                            "n_sign_changes": 500}) == "0,7"


class _FakeWriter:
    sink = None

    def __init__(self):
        self.events = []

    def append_event(self, event_type, payload):
        self.events.append((event_type, payload))


def test_fitness_cache_hits_are_logged_not_rerun():
    cfg = _stage2_config(genome_length_N=8, fitness_resolution_N=64)
    cfg["stop_criteria"] = dict(cfg["stop_criteria"], t_max=6.0)
    writer = _FakeWriter()
    ev = Evolver(cfg, writer, pool=None)
    g = from_sine_pairs([(1, 1.0)], 8)

    def entry(gid):
        return {"genome": g, "genome_id": gid, "operator": "init",
                "parent_ids": [], "warm_center": None}

    rows1 = ev.evaluate_and_log([entry("g1")], 0)
    rows2 = ev.evaluate_and_log([entry("g2")], 1)  # identical genome
    assert rows1[0]["cache_hit"] is False
    assert rows2[0]["cache_hit"] is True
    assert rows2[0]["n_solver_runs"] == 0
    assert rows2[0]["critical_value"] == rows1[0]["critical_value"]
    assert rows2[0]["genome_hash"] == rows1[0]["genome_hash"]
    assert rows2[0]["genome_id"] == "g2"
    # Both logged: evaluation counts stay honest for budget matching.
    assert sum(1 for t, _ in writer.events if t == "genome_eval") == 2
    assert ev.n_evals_ga == 2 and ev.n_cache_hits == 1


# --- end-to-end through the real writer + pool ------------------------------


def test_end_to_end_tiny_run():
    tmp = Path(tempfile.mkdtemp(prefix="ga_e2e_"))
    try:
        repo = tmp / "repo"
        repo.mkdir()
        git = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True,
                                        capture_output=True)
        git("init", "-q")
        git("config", "user.email", "t@t")
        git("config", "user.name", "t")
        (repo / "f.py").write_text("pass\n")
        git("add", "f.py")
        git("commit", "-qm", "init")

        cfg = _stage2_config(genome_length_N=8, fitness_resolution_N=64,
                             population_size=3, n_generations=2,
                             checkpoint_every_k=2, n_workers=2)
        cfg["stop_criteria"] = dict(cfg["stop_criteria"], t_max=6.0)
        cfg["bisection"] = dict(cfg["bisection"], tolerance=4e-3)

        writer = ExperimentWriter(cfg, experiments_root=tmp / "experiments",
                                  repo_root=repo)
        eid = writer.experiment_id
        run(cfg, writer, seed=7, n_workers=2)

        events_path = tmp / "experiments" / "run_logs" / eid / "events.jsonl"
        rows = [json.loads(l) for l in events_path.read_text().splitlines()]
        by_type = {}
        for r in rows:
            by_type.setdefault(r["event"], []).append(r)

        evals = by_type["genome_eval"]
        lit = [r for r in evals if r["operator"] == "baseline_literature"]
        rand = [r for r in evals if r["operator"] == "baseline_random"]
        ga = [r for r in evals if r["operator"] in
              ("init", "mutation", "crossover")]
        assert len(lit) == 12
        assert all("label" in r for r in lit)
        assert len(ga) == 6  # 3 pop x 2 gens
        assert len(rand) == len(ga)  # budget-matched, interleaved
        for r in evals:
            assert r["fitness_resolution_N"] == 64
            assert r["fitness_axis"] == "nu_crit"
            assert "genome_coeffs" in r and "eval_seed" in r
            assert "map_cell" in r and "shape_descriptors" in r
        assert len(by_type["generation"]) == 2
        gen_last = by_type["generation"][-1]
        assert gen_last["cumulative_evals_ga"] == 6
        assert gen_last["cumulative_evals_baseline"] == 18  # 12 lit + 6 rand
        assert len(by_type["solver_run"]) > 0
        for r in by_type["solver_run"]:
            assert r["a"] == 0.0 and "nu" in r and "conservation_drift" in r

        ckpts = list((tmp / "experiments" / "run_logs" / eid /
                      "checkpoints").glob("*.json"))
        assert len(ckpts) == 1
        ck = json.loads(ckpts[0].read_text())
        assert "ga" in ck["rng_state"] and "baseline" in ck["rng_state"]
        assert ck["archive"] is not None

        index_rows = [json.loads(l) for l in
                      (tmp / "experiments" / "index.jsonl")
                      .read_text().splitlines()]
        row = next(r for r in index_rows if r["experiment_id"] == eid)
        assert row["status"] == "completed"
        assert row["config_summary"]["fitness_axis"] == "nu_crit"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
