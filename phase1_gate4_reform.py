"""Reformulated Gate 4 RUNNER — inviscid rank-based growth-rate currency `g_frac`.

The NON-NEGOTIABLE viability gate, reformulated for the currency that survived the
Gate-4 post-mortem + staged probe + 256->512 rank de-risk. Contract:
PHASE1_GATE4_REFORMULATED_PREDICATE.md (frozen before this runs). This script only
PRODUCES the measurements; analyze_phase1_gate4_reform.py applies the frozen
six-property predicate. Keeping produce/judge separate is the same discipline as
the nu_crit Gate 4 (phase1_gate4.py / analyze_phase1_gate4.py).

WHAT IT MEASURES (all inviscid nu=kappa=0, Hou-Luo parity, tail_guard-trusted):

  MAIN ROSTER (40) at N in {128, 256, 512}
    - 3 labeled analytic ICs (smooth_sharp, smooth_mild, euler_control): the
      ground-truth direction anchor + non-buoyant censor-low control (property 2).
    - 37 genome shapes designed to TEST property 6, not dodge it:
        * 4 trivial  (omega pure (1,1), forced split 0.5): the gCLM low-centroid trap
        * 4 structured (free split): higher-centroid multi-mode omega
        * 5 adv_hisplit (forced split 0.70..0.97 on a structured base): the split->1
          rail AND the low-omega0 cheat (high split = small omega0 at fixed energy)
        * 2 adv_losplit (forced split 0.10, 0.20): the opposite rail
        * 22 random (free/natural split): the clean unbiased correlation sample
    Per solve we log both g_frac windows ([0.5 t_res, t_res] and [0.6 t_res, t_res])
    so the analyzer can test window-robustness (property 3b) with no extra solves.

  SPLIT-SWEEP (18) at N=256: 3 base shapes x 6 splits (0.1..0.97), structure fixed,
    split varied -> property 6f interior-optimum (no rail to split=1/0). Reuses the
    LEG-3 SWEEP_BASES.

Property map (analyzer): 1 nonzero, 2 direction+control (labeled), 3 well-posed
(finite + window-robust), 4 RANK-stable across 128->256->512 (roster growers),
5 wide band, 6 non-trivial optimum controlling for split (winner interrogation on
the 37 genome shapes; correlations on the 22 random growers; interior-optimum on
the sweep). See the frozen predicate doc for exact thresholds.

Cheap-first accounting: one nu=0 solve per (shape, N); no bisection. The 40+3 N=512
solves are the expensive leg (~60-90 min on 8 workers); everything else is fast.

Usage: .venv/bin/python phase1_gate4_reform.py --workers 8
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import argparse
import json
import multiprocessing
import sys
from datetime import datetime, timezone

import numpy as np

from ga.genome2d_smooth import random_genome, realize, shape_descriptors
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from phase1_gate4_probe import _mk, force_split
from phase1_gsustained_probe import (
    T_MAX,
    _labeled_ic,
    _rate,
    _solve,
    currencies,
)

MAIN_RES = (128, 256, 512)      # property 4 needs both refinement steps
SWEEP_RES = 256                 # property 6f interior-optimum (rank-stable, cheaper)
GATE_SEED = 20260724            # random block seed (distinct root from the probe)
N_RANDOM = 22                   # clean natural-split correlation sample

# structured base for the forced-split adversarial shapes (struct_diag geometry)
ADV_BASE = ({(1, 1): 1.0, (3, 3): 0.8}, {(0, 2): 1.0, (2, 2): 1.0})
ADV_HISPLIT = (0.70, 0.80, 0.90, 0.95, 0.97)
ADV_LOSPLIT = (0.10, 0.20)

# controlled split-sweep (property 6f): reuse the LEG-3 bases
SWEEP_BASES = {
    "b_diag": ({(1, 1): 1.0, (2, 2): 0.6}, {(0, 2): 1.0, (2, 2): 1.0}),
    "b_low":  ({(1, 1): 1.0}, {(1, 1): 1.0}),
    "b_high": ({(3, 1): 1.0, (2, 2): 0.6}, {(0, 2): 1.0, (3, 1): 0.7}),
}
SWEEP_SPLITS = (0.10, 0.30, 0.50, 0.70, 0.90, 0.97)

LABELED = ("smooth_sharp", "smooth_mild", "euler_control")


def build_gate_roster():
    """The 37 genome shapes (labeled analytic ICs are handled separately). Each
    dict: label, cls, genome. Designed to TEST property 6 -- see module docstring."""
    roster = []
    for name, th in {
        "triv_th11": {(1, 1): 1.0}, "triv_th22": {(2, 2): 1.0},
        "triv_th31": {(3, 1): 1.0}, "triv_sharpth": {(0, 2): 1.0, (2, 2): 1.0},
    }.items():
        roster.append(dict(label=name, cls="trivial",
                           genome=force_split(_mk({(1, 1): 1.0}, th), 0.5)))
    for name, aa in {
        "struct_diag": {(1, 1): 1.0, (3, 3): 0.8}, "struct_aniso": {(2, 2): 1.0, (1, 3): 0.7},
        "struct_high": {(3, 1): 1.0, (2, 2): 0.6}, "struct_33": {(3, 3): 1.0},
    }.items():
        roster.append(dict(label=name, cls="structured",
                           genome=_mk(aa, {(0, 2): 1.0, (2, 2): 1.0})))  # free split
    for s in ADV_HISPLIT:
        roster.append(dict(label=f"advhi_s{int(s * 100):02d}", cls="adv_hisplit",
                           genome=force_split(_mk(*ADV_BASE), s)))
    for s in ADV_LOSPLIT:
        roster.append(dict(label=f"advlo_s{int(s * 100):02d}", cls="adv_losplit",
                           genome=force_split(_mk(*ADV_BASE), s)))
    rng = np.random.default_rng(GATE_SEED)
    while sum(r["cls"] == "random" for r in roster) < N_RANDOM:
        i = sum(r["cls"] == "random" for r in roster)
        roster.append(dict(label=f"rand_{i:02d}", cls="random", genome=random_genome(rng)))
    return roster


def _windows(t, m, tr):
    """g_frac companion windows for property 3b window-robustness (same trajectory)."""
    return {"g_frac_06": _rate(t, m, 0.6 * tr, tr)}


def _meta(base):
    return {"schema_version": SCHEMA_VERSION, "sweep": "phase1_gate4_reform",
            "timestamp": datetime.now(timezone.utc).isoformat(), **base}


def run_labeled(task):
    name, n, base = task["label"], task["n"], task["base"]
    w0, th0 = _labeled_ic(name, n)
    t, m, tr, outcome = _solve(w0, th0, buoyancy=(name != "euler_control"))
    return {"block": "labeled", "label": name, "shape_class": "control",
            "resolution_N": n, "t_res": tr, "outcome": outcome,
            "max_w0": float(np.max(np.abs(w0))),
            **currencies(t, m, tr), **_windows(t, m, tr), **_meta(base)}


def run_genome(task):
    g, n, base = task["genome"], task["n"], task["base"]
    w0, th0 = realize(g, n)
    t, m, tr, outcome = _solve(w0, th0, buoyancy=True)
    return {"block": task.get("block", "roster"), "label": task["label"],
            "shape_class": task["cls"], "resolution_N": n, "t_res": tr,
            "outcome": outcome, "max_w0": float(np.max(np.abs(w0))),
            "target_split": task.get("target_split"),
            "descriptors": shape_descriptors(g),
            **currencies(t, m, tr), **_windows(t, m, tr), **_meta(base)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_gate4_reform.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not args.allow_dirty:
        sys.exit("working tree is dirty; commit first (or --allow-dirty)")
    base = dict(code_version=code_version(), code_dirty=dirty)

    roster = build_gate_roster()
    labeled_tasks = [dict(label=nm, n=n, base=base) for nm in LABELED for n in MAIN_RES]
    genome_tasks = [dict(**s, n=n, base=base) for s in roster for n in MAIN_RES]
    sweep_tasks = [dict(label=f"{nm}_s{int(s * 100):02d}", cls="sweep", block="sweep",
                        genome=force_split(_mk(*SWEEP_BASES[nm]), s), target_split=s,
                        n=SWEEP_RES, base=base)
                   for nm in SWEEP_BASES for s in SWEEP_SPLITS]

    labeled_jobs = [("L", t) for t in labeled_tasks]
    genome_jobs = [("G", t) for t in genome_tasks + sweep_tasks]
    # run all N=512 first (the long tail) so slow solves aren't stuck behind fast ones
    genome_jobs.sort(key=lambda kt: -kt[1]["n"])
    jobs = labeled_jobs + genome_jobs
    total = len(jobs)
    print(f"reformulated Gate 4: {len(labeled_tasks)} labeled + {len(genome_tasks)} "
          f"genome (37x{len(MAIN_RES)}) + {len(sweep_tasks)} sweep = {total} solves "
          f"on {args.workers} workers (43 N=512 solves are the expensive leg)", flush=True)

    def dispatch(kt):
        kind, t = kt
        return run_labeled(t) if kind == "L" else run_genome(t)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    rows = []
    with open(args.out, "a") as f:
        pool = multiprocessing.get_context().Pool(args.workers)
        try:
            done = 0
            for row in pool.imap_unordered(dispatch, jobs, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush(); os.fsync(f.fileno())
                rows.append(row); done += 1
                g = row.get("g_frac")
                gtxt = f"{g:+.3f}" if isinstance(g, float) and g == g else "  nan"
                print(f"  [{done}/{total}] {row['label']:14s} N={row['resolution_N']:<4} "
                      f"g_frac={gtxt} t_res={row['t_res']:.2f} {row['shape_class'][:10]}",
                      flush=True)
        finally:
            pool.close(); pool.join()

    print(f"\n-> {args.out}\nNow run: .venv/bin/python analyze_phase1_gate4_reform.py", flush=True)


if __name__ == "__main__":
    main()
