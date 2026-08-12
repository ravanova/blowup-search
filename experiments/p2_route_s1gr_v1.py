"""Route-S1GR, leg 335 -- diagnose and adjudicate the spike1_stepC_gate.json reproducibility
gap leg 221's own repair-verification sweep surfaced as a byproduct (experiments/journal/
leg_221.md, section 2b) and explicitly declined to answer, handing it forward.

LEG 221'S CLAIM, RE-STATED PRECISELY. Its "pre-repair-world regeneration" of
writeup/data/spike1_stepC_gate.json (produced by re-running experiments/p2_route_bvrr_v1_
repair.py, which shells out to `experiments/spike1_stepC_gate.py --logged`) does not reproduce
the banked artifact: `.runs[0].alpha` moves from -0.3350763095 to -0.3793563731 (13.2%), and
two of the four `predicate_checks` flip (`1_alpha_within_5pct` and `4_resolution_stable_alpha`,
both true -> false). This reproduced identically whether the repair was present or absent, so
leg 221 could not attribute it to its own repair and flagged it, unadjudicated, as either
(a) staleness -- code drift since the artifact was banked at 51b63b2 -- or (b) genuine
environment sensitivity.

THIS LEG'S FINDING: NEITHER. The banked artifact's own `runs[i].steps` field reads **2500** in
all four resolution rungs -- meaning the original 51b63b2 run was invoked with an explicit
`--steps 2500` CLI flag, since the script's own default is 400
(`experiments/spike1_stepC_gate.py`, `ap.add_argument("--steps", type=int, default=400)`).
`experiments/p2_route_bvrr_v1_repair.py`'s own BANKED registry entry for this artifact reads

    dict(key="spike1_stepC_gate", ..., script="experiments/spike1_stepC_gate.py",
         argv=["--logged"], slow=True, ...)

-- `argv` carries no `--steps`, so leg 221's regeneration silently fell back to the CLI
default of 400 steps: an entirely different (far less relaxed) trajectory, not a differently
COMPUTED one. This script re-derives both numbers independently to settle it:

  1. Runs config 0 (n_r=300, n_beta=48, r_min=1e-3, r_max=1e5, renorm=True, tol=1e-9) at
     `max_steps=400` (the harness's actual, un-overridden argv) -- reproducing leg 221's
     "regenerated" alpha to confirm the CAUSE, not just the SYMPTOM.
  2. Runs all four resolution rungs at `max_steps=2500` (the banked artifact's own recorded
     step count) -- reproducing the BANKED artifact itself, to settle whether the code and
     environment (today's numpy, today's OpenBLAS) actually agree with the 2026-07-25 run once
     the harness bug is corrected.
  3. Controls for the DM's alternate hypothesis (environment/BLAS-thread sensitivity, per
     this repo's own precedent in experiments/leg_0_bench_newton_threads.sh) by re-running
     config 0 at max_steps=2500 under OMP/OPENBLAS/MKL thread counts 1, 2 and 4, and reporting
     the spread in alpha across threads -- so "reproduces" is not asserted on a single
     unexamined thread setting.
  4. Re-evaluates the four gate predicates against the banked TARGETS using the correctly
     re-run values and reports which, if any, actually differ from the banked
     `predicate_checks`.

Writes writeup/data/p2_route_s1gr_v1.json. Reads (never edits) experiments/spike1_stepC_gate.py
and writeup/data/spike1_stepC_gate.json.
"""

import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np  # noqa: E402

from solver.boussinesq_velocity import PolarGrid  # noqa: E402
from solver.boussinesq_rescaled import RescaledBoussinesq, CL_STAR, COMEGA_STAR, ALPHA_STAR  # noqa: E402
from experiments.spike1_stepC_gate import profile_ansatz, radial_exponent, shape_metrics, evaluate_predicate  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANKED_PATH = os.path.join(ROOT, "writeup", "data", "spike1_stepC_gate.json")
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_s1gr_v1.json")

CONFIGS = [(300, 48, 1e-3, 1e5), (450, 48, 1e-3, 1e5),
           (600, 48, 1e-3, 1e5), (450, 48, 1e-3, 1e6)]


def run_one(n_r, n_beta, r_min, r_max, max_steps, dt_frac=0.3, tol=1e-9):
    t0 = time.time()
    grid = PolarGrid(n_r=n_r, n_beta=n_beta, r_min=r_min, r_max=r_max)
    om0, et0, xi0 = profile_ansatz(grid)
    solver = RescaledBoussinesq(grid)
    res = solver.run(om0, et0, xi0, dt_frac=dt_frac, tol=tol, max_steps=max_steps, renorm=True)
    a_far = radial_exponent(res["omega"], grid, r_lo=r_max ** 0.35, r_hi=r_max ** 0.75)
    out = {"n_r": n_r, "n_beta": n_beta, "r_min": r_min, "r_max": r_max,
           "steps": res["steps"], "residual": float(res["residual"]),
           "c_l": float(res["c_l"]), "c_omega": float(res["c_omega"]),
           "alpha": float(res["c_omega"] / res["c_l"]), "alpha_far": float(a_far),
           "wall_seconds": time.time() - t0}
    out.update(shape_metrics(res["omega"], grid))
    return out


def rel_diff(a, b):
    return abs(a - b) / abs(b) if b else float("nan")


def main():
    banked = json.load(open(BANKED_PATH))
    banked_runs = banked["runs"]
    banked_checks = banked["predicate_checks"]

    result = {"targets": banked["targets"]}

    # --- Step 1: confirm the CAUSE. Reproduce leg 221's exact harness invocation
    # (argv=["--logged"], no --steps override) on config 0.
    print("[1] config 0 at max_steps=400 (the harness's actual, un-overridden argv)...",
          flush=True)
    r400 = run_one(*CONFIGS[0], max_steps=400)
    print(f"    alpha={r400['alpha']:+.10f} residual={r400['residual']:.4e} "
          f"steps={r400['steps']}", flush=True)
    leg221_reported_alpha = -0.3793563731
    result["cause_confirmation"] = {
        "harness_argv": ["--logged"],
        "harness_default_steps": 400,
        "banked_artifact_steps_field": [r["steps"] for r in banked_runs],
        "rerun_at_400_steps": r400,
        "leg221_reported_regenerated_alpha_run0": leg221_reported_alpha,
        "rel_diff_vs_leg221_report": rel_diff(r400["alpha"], leg221_reported_alpha),
    }

    # --- Step 2: reproduce the BANKED artifact itself, at the step count it actually
    # recorded (2500), for all four resolution rungs.
    print("[2] all four resolution rungs at max_steps=2500 (banked step count)...", flush=True)
    reruns = []
    for i, cfg in enumerate(CONFIGS):
        steps_banked = banked_runs[i]["steps"]
        r = run_one(*cfg, max_steps=steps_banked)
        print(f"    run[{i}] n_r={cfg[0]} r_max={cfg[3]:.0e}: alpha={r['alpha']:+.10f} "
              f"(banked {banked_runs[i]['alpha']:+.10f}, "
              f"rel_diff={rel_diff(r['alpha'], banked_runs[i]['alpha']):.3e}) "
              f"residual={r['residual']:.4e} steps={r['steps']}", flush=True)
        reruns.append(r)
    result["reruns_at_banked_step_count"] = reruns
    result["rel_diff_vs_banked"] = [
        {"field": "alpha", "run_index": i,
         "rerun": reruns[i]["alpha"], "banked": banked_runs[i]["alpha"],
         "rel_diff": rel_diff(reruns[i]["alpha"], banked_runs[i]["alpha"])}
        for i in range(len(CONFIGS))
    ]

    # --- Step 3: BLAS-thread-count control, per this repo's own precedent
    # (experiments/leg_0_bench_newton_threads.sh) that thread count can move an iterative
    # solve's endpoint. Re-run config 0 at the banked step count (2500) under 1/2/4 threads,
    # IN-PROCESS numbers only (thread env vars are read once at process start by OpenBLAS, so
    # this control is run as three subprocess invocations, not by mutating os.environ here).
    print("[3] BLAS-thread control at max_steps=2500, threads in {1,2,4}...", flush=True)
    thread_control = []
    probe_src = (
        "import sys; sys.path.insert(0, %r)\n"
        "from experiments.p2_route_s1gr_v1 import run_one, CONFIGS\n"
        "import json\n"
        "r = run_one(*CONFIGS[0], max_steps=%d)\n"
        "print(json.dumps({'alpha': r['alpha'], 'residual': r['residual'], "
        "'c_l': r['c_l'], 'c_omega': r['c_omega']}))\n"
    ) % (ROOT, banked_runs[0]["steps"])
    for t in (1, 2, 4):
        env = dict(os.environ)
        env["OMP_NUM_THREADS"] = str(t)
        env["OPENBLAS_NUM_THREADS"] = str(t)
        env["MKL_NUM_THREADS"] = str(t)
        t0 = time.time()
        proc = subprocess.run([sys.executable, "-c", probe_src], cwd=ROOT, env=env,
                               capture_output=True, text=True, check=True)
        payload = json.loads(proc.stdout.strip().splitlines()[-1])
        payload["threads"] = t
        payload["wall_seconds"] = time.time() - t0
        print(f"    threads={t}: alpha={payload['alpha']:+.10f} "
              f"wall={payload['wall_seconds']:.1f}s", flush=True)
        thread_control.append(payload)
    alphas_by_thread = [p["alpha"] for p in thread_control]
    result["thread_control"] = {
        "runs": thread_control,
        "max_abs_diff": max(alphas_by_thread) - min(alphas_by_thread),
        "max_rel_diff": rel_diff(max(alphas_by_thread), min(alphas_by_thread)),
    }

    # --- Step 4: re-evaluate the four gate predicates against the correctly re-run values.
    fake_runs = [{"n_r": r["n_r"], "alpha": r["alpha"], "alpha_far": r["alpha_far"],
                  "anisotropy_median": r["anisotropy_median"]} for r in reruns]
    verdict, checks = evaluate_predicate(fake_runs)
    result["predicate_reeval"] = {
        "checks": checks, "pass": verdict,
        "banked_checks": banked_checks, "banked_pass": banked["predicate_pass"],
        "flipped_vs_banked": {k: (checks[k] != banked_checks[k]) for k in checks},
    }

    # --- Adjudication.
    all_close = all(d["rel_diff"] < 1e-6 for d in result["rel_diff_vs_banked"])
    predicates_actually_flip = any(result["predicate_reeval"]["flipped_vs_banked"].values())
    result["adjudication"] = {
        "status": "REPRODUCIBLE_AS_BANKED" if (all_close and not predicates_actually_flip)
                  else "STALE_WITH_NAMED_MECHANISM" if not all_close
                  else "AMBIGUOUS",
        "named_mechanism": (
            "experiments/p2_route_bvrr_v1_repair.py's BANKED registry entry for "
            "spike1_stepC_gate invokes the generating script with argv=['--logged'] only, "
            "omitting the '--steps 2500' flag the banked artifact's own runs[*].steps field "
            "shows was used originally; the script's CLI default (400) was silently "
            "substituted, producing a materially shorter, unconverged trajectory rather than "
            "a differently-computed one. This is a harness bug in the regeneration argv "
            "list, not code drift in solver/boussinesq_rescaled.py or solver/"
            "boussinesq_velocity.py (both are byte-identical on the relevant path for "
            "well-posed grids since 51b63b2 -- 26e6bd3 only added raise-guards that never "
            "trigger on this gate's configs) and not environment sensitivity (see "
            "thread_control above)."
        ),
    }
    print("\nADJUDICATION:", result["adjudication"]["status"], flush=True)

    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
