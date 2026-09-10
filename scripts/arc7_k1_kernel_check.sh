#!/usr/bin/env bash
# scripts/arc7_k1_kernel_check.sh — arc 7, unit K1 (leg 437): THE KERNEL CHECK, run to completion, NO TIME CAP.
# Pre-registered in experiments/journal/leg_437_prereg.md and pushed BEFORE either phase ran.
#
#   usage: arc7_k1_kernel_check.sh A <existing-tree> <logdir>   # phase A: resume the arc-6 tree (leg 435) to completion
#          arc7_k1_kernel_check.sh B <fresh-workdir>  <logdir>   # phase B: fresh clone at PIN, `lake exe cache get`, full build
#
# Both phases end with `#print axioms` on the two exported theorems. Progress is checkpointed in
# <logdir>/k1_<phase>_build.log (lake's own "[n/N] Built ..." lines). READ THE LOG; never kill the run
# to stay inside a wall-clock guess — that is what cost arc 6 this answer (leg 431 §3 item 1).
set -u
PHASE=$1; WORK=$2; LOG=$3; mkdir -p "$LOG"
export PATH="$HOME/.elan/bin:$PATH"
PIN=8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538   # the commit arc 6 measured (legs 418/431/435)
REPO=https://github.com/openai/NavierStokesAndEuler.git
S="$LOG/k1_${PHASE}_summary.txt"; BL="$LOG/k1_${PHASE}_build.log"; AX="$LOG/k1_${PHASE}_axioms.log"
CHECK="$LOG/k1_axioms_check.lean"
cat > "$CHECK" <<'LEAN'
import NavierStokes.ComparatorSolution
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_R3
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_periodic
LEAN
{ echo "phase=$PHASE"; echo "t_start=$(date -u +%FT%TZ)"; echo "nproc=$(nproc)"; grep -m1 'model name' /proc/cpuinfo
  free -g | sed -n 2p; df -h "$(dirname "$WORK")" 2>/dev/null | tail -1; } > "$S"
T0=$(date +%s)
if [ "$PHASE" = B ]; then
  git clone "$REPO" "$WORK" >> "$BL" 2>&1 || { echo "clone_rc=$?" >> "$S"; exit 1; }
  echo "upstream_head_at_clone=$(git -C "$WORK" rev-parse HEAD)" >> "$S"
  git -C "$WORK" checkout -q "$PIN" >> "$BL" 2>&1 || { echo "checkout_rc=$?" >> "$S"; exit 1; }
  echo "t_clone_done=$(date -u +%FT%TZ) clone_s=$(( $(date +%s) - T0 ))" >> "$S"
fi
cd "$WORK" || exit 1
echo "tree_head=$(git rev-parse HEAD)" >> "$S"
echo "toolchain=$(cat lean-toolchain)" >> "$S"
lean --version >> "$S" 2>&1; lake --version >> "$S" 2>&1
if [ "$PHASE" = B ]; then
  T1=$(date +%s); echo "=== CACHE_GET_T0 $(date -u +%FT%TZ)" >> "$BL"
  lake exe cache get >> "$BL" 2>&1; RC=$?
  echo "=== CACHE_GET_RC=$RC $(date -u +%FT%TZ)" >> "$BL"
  echo "cache_get_rc=$RC cache_get_s=$(( $(date +%s) - T1 ))" >> "$S"
fi
echo "mathlib_rev=$(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)" >> "$S"
echo "comparator_rev=$(git -C .lake/packages/Comparator rev-parse HEAD 2>/dev/null)" >> "$S"
T2=$(date +%s); echo "=== BUILD_T0 $(date -u +%FT%TZ)" >> "$BL"
lake build >> "$BL" 2>&1; RC=$?
echo "=== BUILD_RC=$RC $(date -u +%FT%TZ)" >> "$BL"
echo "build_rc=$RC build_s=$(( $(date +%s) - T2 ))" >> "$S"
echo "build_error_lines=$(grep -cE '(^|[[:space:]])error:' "$BL")" >> "$S"
T3=$(date +%s)
{ echo "=== AXIOMS_T0 $(date -u +%FT%TZ)"; lake env lean "$CHECK"; echo "=== AXIOMS_RC=$? $(date -u +%FT%TZ)"; } > "$AX" 2>&1
echo "axioms_s=$(( $(date +%s) - T3 ))" >> "$S"
echo "olean_count=$(find .lake/build/lib/lean -name '*.olean' | wc -l)" >> "$S"
echo "t_end=$(date -u +%FT%TZ) total_s=$(( $(date +%s) - T0 ))" >> "$S"
