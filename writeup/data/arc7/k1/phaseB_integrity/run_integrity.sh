#!/usr/bin/env bash
# K1 phase B follow-on: comparator integrity check on phase B's prebuilt tree. No time cap.
set -u
TREE=$1; LOG=$2; export PATH="$HOME/.elan/bin:$PATH"
export COMPARATOR_LANDRUN="$TREE/.lake/packages/Comparator/scripts/fake-landrun.sh"
export COMPARATOR_LEAN4EXPORT="$TREE/.lake/packages/lean4export/.lake/build/bin/lean4export"
export COMPARATOR_NANODA="/root/k1B/tools/nanoda_lib/target/release/nanoda_bin"
cd "$TREE" || exit 1
S="$LOG/integrity_summary.txt"
{ echo "t_start=$(date -u +%FT%TZ)"; echo "tree_head=$(git rev-parse HEAD)"; echo "comparator_rev=$(git -C .lake/packages/Comparator rev-parse HEAD)"; echo "lean4export_rev=$(git -C .lake/packages/lean4export rev-parse HEAD)"; echo "nanoda_rev=$(git -C /root/k1B/tools/nanoda_lib rev-parse HEAD) $($COMPARATOR_NANODA --version 2>&1 | head -1)"; echo "nproc=$(nproc)"; free -g | sed -n 2p; } > "$S"
for C in NavierStokes Euler; do
  L="$LOG/comparator_${C}.log"; T0=$(date +%s)
  { echo "=== COMPARATOR_T0 $C $(date -u +%FT%TZ)"; lake env .lake/packages/Comparator/.lake/build/bin/comparator "ComparatorChallenges/$C.json"; echo "=== COMPARATOR_RC=$? $C $(date -u +%FT%TZ)"; } > "$L" 2>&1
  RC=$(grep -o 'COMPARATOR_RC=[0-9]*' "$L" | tail -1 | cut -d= -f2)
  echo "${C}_rc=$RC ${C}_s=$(( $(date +%s)-T0 ))" >> "$S"
done
echo "t_end=$(date -u +%FT%TZ)" >> "$S"
