#!/bin/sh
# H6 discriminator: does a=0.9's 40-iteration stall move with the BLAS thread count?
# One continuation per setting -- the quantity of interest is the STALL LEVEL, and
# three repeats already showed it is deterministic WITHIN a fixed environment.
cd /home/user/blowup-search/.claude/worktrees/agent-a965aef4fc9ea6352 || exit 1
for T in 1 2 4; do
  OMP_NUM_THREADS=$T OPENBLAS_NUM_THREADS=$T MKL_NUM_THREADS=$T \
    /home/user/blowup-search/.venv/bin/python -c "
import json, sys
sys.path.insert(0, '.')
from solver.profile_newton import continuation
r = continuation([0.0, 0.3, 0.6, 0.9], n=601)[-1]
print(json.dumps({'threads': $T, 'converged': r['converged'],
                  'residual_rms': r['residual_rms'], 'relres': r['relres'],
                  'c': r['c'], 'iterations': r['iterations']}))
"
done
