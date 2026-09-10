#!/usr/bin/env bash
export PATH="$HOME/.elan/bin:$PATH"
export MATHLIB_CACHE_DIR=/dev/shm/k1_mlcache
mkdir -p "$MATHLIB_CACHE_DIR"
bash <scratchpad>/wt/scripts/arc7_k1_kernel_check.sh B <scratchpad>/nse <scratchpad>/wt/writeup/data/arc7/k1/phaseB
echo "runner_rc=$?" >> <scratchpad>/wt/writeup/data/arc7/k1/phaseB/k1_B_summary.txt
du -sh "$MATHLIB_CACHE_DIR" >> <scratchpad>/wt/writeup/data/arc7/k1/phaseB/k1_B_summary.txt 2>/dev/null
rm -rf "$MATHLIB_CACHE_DIR"
