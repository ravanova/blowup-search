#!/usr/bin/env bash
# leg 437 phase C — FROM-SOURCE rebuild. Derived from scripts/arc7_k1_kernel_check.sh phase B,
# with ONE deliberate difference, which is the entire point of phase C:
#
#     `lake exe cache get` IS NEVER RUN. Not once. Not to "warm" anything.
#
# so mathlib is compiled from its own source and the official olean cache is not in the trust path.
# NO TIME CAP. Never kill this to fit a wall-clock guess (leg 431 §3 item 1).
set -u
PIN=8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538
REPO=https://github.com/openai/NavierStokesAndEuler.git
WORK=$1; LOG=$2; mkdir -p "$LOG"
export PATH="$HOME/.elan/bin:$PATH"
S="$LOG/k1_C_summary.txt"; BL="$LOG/k1_C_build.log"; AX="$LOG/k1_C_axioms.log"
CHECK="$LOG/k1_axioms_check.lean"
cat > "$CHECK" <<'LEAN'
import NavierStokes.ComparatorSolution
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_R3
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_periodic
LEAN
{ echo "phase=C"; echo "t_start=$(date -u +%FT%TZ)"; echo "nproc=$(nproc)"; grep -m1 'model name' /proc/cpuinfo
  free -g | sed -n 2p; df -B1 --output=avail / | tail -1 | sed 's/^/disk_avail_bytes_at_start=/'; } > "$S"
T0=$(date +%s)
git clone "$REPO" "$WORK" >> "$BL" 2>&1 || { echo "clone_rc=$?" >> "$S"; exit 1; }
echo "upstream_head_at_clone=$(git -C "$WORK" rev-parse HEAD)" >> "$S"
git -C "$WORK" checkout -q "$PIN" >> "$BL" 2>&1 || { echo "checkout_rc=$?" >> "$S"; exit 1; }
echo "t_clone_done=$(date -u +%FT%TZ) clone_s=$(( $(date +%s) - T0 ))" >> "$S"
cd "$WORK" || exit 1
echo "tree_head=$(git rev-parse HEAD)" >> "$S"
echo "toolchain=$(cat lean-toolchain)" >> "$S"
lean --version >> "$S" 2>&1; lake --version >> "$S" 2>&1
echo "cache_get=NEVER-RUN (phase C: the cache is deliberately not in the trust path)" >> "$S"
# `lake build` resolves the deps (fetches mathlib SOURCE via git) and compiles everything from source.
T2=$(date +%s); echo "=== BUILD_T0 $(date -u +%FT%TZ)" >> "$BL"
lake build >> "$BL" 2>&1; RC=$?
echo "=== BUILD_RC=$RC $(date -u +%FT%TZ)" >> "$BL"
echo "build_rc=$RC build_s=$(( $(date +%s) - T2 ))" >> "$S"
echo "mathlib_rev=$(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)" >> "$S"
echo "comparator_rev=$(git -C .lake/packages/Comparator rev-parse HEAD 2>/dev/null)" >> "$S"
echo "build_error_lines=$(grep -cE '(^|[[:space:]])error:' "$BL")" >> "$S"
echo "mathlib_built_lines=$(grep -c 'Built Mathlib\.' "$BL")" >> "$S"
echo "mathlib_replayed_lines=$(grep -c 'Replayed Mathlib\.' "$BL")" >> "$S"
T3=$(date +%s)
{ echo "=== AXIOMS_T0 $(date -u +%FT%TZ)"; lake env lean "$CHECK"; echo "=== AXIOMS_RC=$? $(date -u +%FT%TZ)"; } > "$AX" 2>&1
echo "axioms_s=$(( $(date +%s) - T3 ))" >> "$S"
echo "olean_count=$(find .lake/build/lib/lean -name '*.olean' 2>/dev/null | wc -l)" >> "$S"
echo "disk_avail_bytes_at_end=$(df -B1 --output=avail / | tail -1)" >> "$S"
echo "t_end=$(date -u +%FT%TZ) total_s=$(( $(date +%s) - T0 ))" >> "$S"
