#!/usr/bin/env bash
# PROG-R4 / R-prof (leg 405) -- re-run the whole profile from a clean checkout.
#
# An independent verifier needs three things: the solver (in this repo), a numpy,
# and the NAMED reference implementations. The reference is NOT in .venv and must
# not be installed into it -- .venv carries live campaign runs. This script builds
# a throwaway venv, reproduces every raw artefact, and rebuilds the gate JSON.
#
#   bash experiments/programme_r4/profiling/rerun.sh [scratch_dir]
#
# Expect ~15 minutes of single-core CPU. On a QUIET machine the absolute
# microseconds will be smaller than the banked ones -- see the artefact's
# `load_conditions` block. THE GATE ANSWERS ARE RATIOS AND SHOULD REPRODUCE.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRATCH="${1:-/tmp/r_prof_rerun}"
mkdir -p "$SCRATCH"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"

if [ ! -x "$SCRATCH/refvenv/bin/python" ]; then
  echo "== building the reference venv (NOT $REPO/.venv) =="
  python3 -m venv "$SCRATCH/refvenv"
  "$SCRATCH/refvenv/bin/pip" install -q "jax[cpu]==0.11.1" jax-cfd==0.2.1 pyfftw==0.15.1
fi
REFPY="$SCRATCH/refvenv/bin/python"
OURPY="${OURPY:-$REPO/.venv/bin/python}"
P="$REPO/experiments/programme_r4/profiling"

echo "== load average at start: $(cat /proc/loadavg) =="
"$OURPY" "$P/r_prof_v1.py" --part ours   --out "$SCRATCH/ours_venv.json"
"$REFPY" "$P/r_prof_v1.py" --part ref    --out "$SCRATCH/ref.json"
"$REFPY" "$P/r_prof_v1.py" --part paired --rounds 15 --out "$SCRATCH/paired.json"
"$REFPY" "$P/r_prof_v1.py" --part duel   --rounds 60 --out "$SCRATCH/duel.json"
"$REFPY" "$P/r_prof_candidates_v1.py"    --rounds 40 --out "$SCRATCH/cand.json"
# a SECOND `ours` run, deliberately last, so it lands at a different machine load:
# this is what tells a reader which of the numbers are load-robust (ratios) and
# which are not (absolute microseconds).
"$OURPY" "$P/r_prof_v1.py" --part ours   --out "$SCRATCH/ours_venv_r2.json"
"$OURPY" "$P/r_prof_v1.py" --part merge \
    --ours "$SCRATCH/ours_venv.json" --ref "$SCRATCH/ref.json" \
    --paired "$SCRATCH/paired.json" --duel "$SCRATCH/duel.json" \
    --candidates "$SCRATCH/cand.json" \
    --ours-repeat "$SCRATCH/ours_venv_r2.json" \
    --out "$SCRATCH/p2_r_prof_v1.rerun.json"
echo "== load average at end:   $(cat /proc/loadavg) =="
"$OURPY" - "$SCRATCH/p2_r_prof_v1.rerun.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
g = d["gate"]
print("GATE (i)  table sums to %.4f %%" % g["i_where_the_per_step_time_goes"]["sums_to_pct"])
print("GATE (ii) fixed per-call overhead = %.1f%% of the step (cross-check %.1f%%)" % (
    100*g["ii_fixed_per_call_overhead_fraction"]["ANSWER_fixed_fraction_of_step"],
    100*g["ii_fixed_per_call_overhead_fraction"]["cross_check_two_point_extrapolation"]["fixed_fraction_of_step"]))
i3 = g["iii_within_3x_of_reference"]
print("GATE (iii) within 3x of the reference?  %s   (ratio %.2f cpu / %.2f wall)" % (
    i3["ANSWER"], i3["raw_ratio_cpu_clock"]["median"], i3["raw_ratio_wall_clock"]["median"]))
for c in ("ours", "reference_run", "candidates_run"):
    pass
PY
echo "wrote $SCRATCH/p2_r_prof_v1.rerun.json -- compare against writeup/data/p2_r_prof_v1.json"
