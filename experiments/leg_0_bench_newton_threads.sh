#!/bin/sh
# H6 discriminator: does a=0.9's 40-iteration stall move with the BLAS thread count?
cd /home/user/blowup-search/.claude/worktrees/agent-a965aef4fc9ea6352 || exit 1
for T in 1 2 4 8; do
  echo "=== THREADS=$T ==="
  OMP_NUM_THREADS=$T OPENBLAS_NUM_THREADS=$T MKL_NUM_THREADS=$T \
    /home/user/blowup-search/.venv/bin/python experiments/leg_0_bench_newton_probe.py h6 2>&1 | tail -40
done
