#!/usr/bin/env bash
# Wait for the running `lake exe cache get` to finish, then run the full build,
# logging module-by-module progress with timestamps so the wall time and the
# rate are MEASURED, not estimated.
export PATH="$HOME/.elan/bin:$PATH"
S=/tmp/claude-0/-home-user-blowup-search/f04cf05e-679d-5fc5-8545-c07be1caa01d/scratchpad
cd "$S/nse" || exit 1
# wait for cache get to report its rc
for _ in $(seq 1 720); do
  grep -q "^=== CACHE_RC=" "$S/lean_cache.log" && break
  sleep 10
done
{
  echo "=== BUILD_T0 $(date -u +%FT%TZ)"
  nproc
  lean --version
  lake build
  echo "=== BUILD_RC=$? $(date -u +%FT%TZ)"
} > "$S/lean_build.log" 2>&1
