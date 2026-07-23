"""Tests for ga/resolution_study.py (Stage 3 Tier-1 -> Tier-2 promotion).

The convergence-verdict logic is tested against synthetic per-resolution run
summaries (converging / drifting / high-drift / non-reproducing), so the
WIN_CONDITION.md Tier-2 contract and the conservation-drift artifact guard are
pinned without paying for solver runs. `run_at_resolution` gets one genuine
small CLM run to prove the solver wiring. The end-to-end driver is exercised
with an injected `run_fn`, checking the LOGGING.md schema #6 event shape and
that a numerically_confirmed hit is mirrored into promoted_candidates.jsonl.
"""

import json
import shutil
import tempfile
from pathlib import Path

import numpy as np

from ga.logbook import PROJECT_ROOT, genome_hash
from ga.resolution_study import (
    assess_convergence,
    load_elites,
    resolution_study,
    run_at_resolution,
    study_points,
)
from win_condition import WinTier


def _minimal_config(gclm_a=0.7):
    """A config.json carrying just the fields resolution_study reads back."""
    return {
        "gclm_a": gclm_a,
        "energy_budget": float(np.pi) / 2.0,
        "bandwidth_cap": None,
        "tier1_r2_threshold": 0.98,
        "stop_criteria": {
            "t_max": 24.0, "max_steps": 400_000,
            "omega_amplification_factor": 100.0,
            "early_decay_exit": {"fraction": 0.1, "window": 2.0},
        },
        "bisection": {"tail_fraction": 0.15},
        "solver_params": {"dt_policy": {"dt_max": 1e-2, "c1": 0.05, "c2": 0.4}},
    }


def _fake_run(N, t_star, drift=1e-5, blew_up=True, r2=0.999):
    return {
        "resolution_N": N, "nu": 0.0, "outcome": "blowup_candidate",
        "blew_up": blew_up, "t_final": 2.1, "max_omega_final": 1e4,
        "n_timesteps": 3000, "dt_min": 1e-4, "conservation_drift": drift,
        "wall_clock_seconds": 1.0,
        "t_star": t_star, "r_squared": (r2 if t_star is not None else None),
        "exponent": (1.0 if t_star is not None else None),
    }


# --- study_points ----------------------------------------------------------

def test_study_points_has_inviscid_anchor_and_viscous_point():
    pts = study_points(0.16, viscous_frac=0.5)
    roles = [r for r, _ in pts]
    assert roles == ["inviscid_anchor", "viscous_resistance"]
    assert pts[0][1] == 0.0
    assert abs(pts[1][1] - 0.08) < 1e-9


def test_study_points_drops_viscous_when_nu_crit_zero():
    assert study_points(0.0) == [("inviscid_anchor", 0.0)]


# --- assess_convergence: the Tier-2 verdict logic --------------------------

def test_converging_sequence_is_numerically_confirmed():
    runs = [_fake_run(256, 2.1730), _fake_run(512, 2.1732), _fake_run(1024, 2.1732)]
    v = assess_convergence(runs)
    assert v["converged"] is True
    assert v["reproduced"] is True
    assert v["drift_exceeded"] is False
    assert v["win_tier"] == WinTier.NUMERICALLY_CONFIRMED.value


def test_drifting_sequence_stays_candidate():
    # T* keeps drifting as the grid refines -> a resolution artifact.
    runs = [_fake_run(256, 2.0), _fake_run(512, 2.5), _fake_run(1024, 3.2)]
    v = assess_convergence(runs)
    assert v["converged"] is False
    assert v["win_tier"] == WinTier.CANDIDATE.value


def test_high_drift_refused_even_when_t_star_converges():
    # Clean-looking T* convergence but invariants drifted -> distrusted.
    runs = [_fake_run(256, 2.1730, drift=5e-3),
            _fake_run(512, 2.1732, drift=5e-3),
            _fake_run(1024, 2.1732, drift=5e-3)]
    v = assess_convergence(runs, drift_threshold=1e-3)
    assert v["drift_exceeded"] is True
    assert v["converged"] is True  # the T* fit itself did converge...
    assert v["win_tier"] != WinTier.NUMERICALLY_CONFIRMED.value  # ...but not promoted


def test_not_reproduced_at_one_resolution_blocks_confirmation():
    runs = [_fake_run(256, 2.1730),
            _fake_run(512, None, blew_up=False),  # regularized at higher N
            _fake_run(1024, 2.1732)]
    runs[1]["outcome"] = "no_blowup"
    v = assess_convergence(runs)
    assert v["reproduced"] is False
    assert v["converged"] is False
    assert v["win_tier"] != WinTier.NUMERICALLY_CONFIRMED.value


# --- load_elites -----------------------------------------------------------

def test_load_elites_ranks_by_fitness_and_carries_config():
    tmp = Path(tempfile.mkdtemp())
    try:
        exp = tmp / "run_logs" / "fake-exp"
        (exp / "checkpoints").mkdir(parents=True)
        (exp / "config.json").write_text(json.dumps(_minimal_config()))
        archive = {
            "5,0": {"genome_id": "gA", "fitness": 0.10, "coeffs": [1.0, 0.2],
                    "envelope_p": 1.0, "descriptors": {"n_sign_changes": 2}},
            "9,0": {"genome_id": "gB", "fitness": 0.16, "coeffs": [1.0, -0.5],
                    "envelope_p": 1.5, "descriptors": {"n_sign_changes": 2}},
            "7,2": {"genome_id": "gC", "fitness": 0.14, "coeffs": [0.3, 1.0],
                    "envelope_p": 0.8, "descriptors": {"n_sign_changes": 4}},
        }
        (exp / "checkpoints" / "gen_00024.json").write_text(json.dumps({
            "experiment_id": "fake-exp", "generation_index": 24,
            "archive": archive,
        }))
        elites = load_elites(exp, top_k=2)
        assert [e["genome_id"] for e in elites] == ["gB", "gC"]  # by fitness desc
        assert elites[0]["nu_crit"] == 0.16
        assert elites[0]["map_cell"] == "9,0"
        assert elites[0]["source_experiment_id"] == "fake-exp"
        assert elites[0]["config"]["gclm_a"] == 0.7
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- run_at_resolution: real solver wiring (CLM sin(x), a=0) ----------------

def test_run_at_resolution_real_clm_blowup():
    # sin(x) under CLM (a=0, nu=0) has a closed-form singularity at T*=2.
    cfg = _minimal_config(gclm_a=0.0)
    cfg["stop_criteria"]["t_max"] = 5.0
    summary = run_at_resolution([1.0], 0.0, 256, cfg, nu=0.0,
                                study_amplification_factor=1e3)
    assert summary["blew_up"] is True
    assert summary["t_star"] is not None
    # Loose sanity band only: the exponent search over-fits alpha on the plain
    # CLM tail so T* is biased at coarse N (the very drift the study measures);
    # tight T* convergence is checked on the real a=0.7 elites, not here.
    assert 1.8 < summary["t_star"] < 2.7
    assert summary["resolution_N"] == 256


# --- end-to-end driver with an injected run_fn -----------------------------

def _stub_run_fn(task):
    """Deterministic canned run: the two seeded genomes converge cleanly,
    so both should reach NUMERICALLY_CONFIRMED."""
    N = task["N"]
    t_star = {256: 2.1730, 512: 2.1732, 1024: 2.1732}[N]
    summary = _fake_run(N, t_star)
    summary["nu"] = task["nu"]
    summary["_group"] = task["_group"]
    return summary


def test_resolution_study_end_to_end_logs_and_promotes():
    tmp = Path(tempfile.mkdtemp())
    try:
        # A source acceptance run with one elite in its archive.
        exp = tmp / "run_logs" / "src-exp"
        (exp / "checkpoints").mkdir(parents=True)
        (exp / "config.json").write_text(json.dumps(_minimal_config()))
        (exp / "checkpoints" / "gen_00024.json").write_text(json.dumps({
            "experiment_id": "src-exp", "generation_index": 24,
            "archive": {"9,0": {"genome_id": "gB", "fitness": 0.16,
                                "coeffs": [1.0, -0.5], "envelope_p": 1.5,
                                "descriptors": {"n_sign_changes": 2}}},
        }))

        events = resolution_study(
            [exp], experiments_root=tmp, repo_root=PROJECT_ROOT,
            resolutions=(256, 512, 1024), top_k=1, n_workers=1,
            allow_dirty=True, run_fn=_stub_run_fn,
            experiment_id="stage3-test",
        )
        # inviscid anchor + viscous point = 2 events for the single elite.
        assert len(events) == 2
        for e in events:
            # LOGGING.md schema #6 required fields.
            for key in ("genome_id", "resolutions_tested",
                        "t_star_by_resolution", "converged", "win_tier"):
                assert key in e, key
            assert e["resolutions_tested"] == [256, 512, 1024]
            assert e["win_tier"] == WinTier.NUMERICALLY_CONFIRMED.value
            assert e["genome_hash"] == genome_hash(np.asarray([1.0, -0.5]), 1.5)

        # Events landed in the Stage-3 experiment's events.jsonl.
        logged = [json.loads(l) for l in
                  (tmp / "run_logs" / "stage3-test" / "events.jsonl")
                  .read_text().splitlines()]
        assert sum(1 for r in logged if r["event"] == "resolution_study") == 2

        # Both confirmations mirrored into the cross-experiment file.
        promoted = [json.loads(l) for l in
                    (tmp / "promoted_candidates.jsonl").read_text().splitlines()]
        assert len(promoted) == 2
        assert all(r["win_tier"] == WinTier.NUMERICALLY_CONFIRMED.value
                   for r in promoted)
        assert all(r["genome_id"] == "gB" for r in promoted)

        # Index row closed out with the promotion count.
        idx = [json.loads(l) for l in
               (tmp / "index.jsonl").read_text().splitlines()]
        row = [r for r in idx if r["experiment_id"] == "stage3-test"][0]
        assert row["status"] == "completed"
        assert row["n_tier2_promotions"] == 2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
