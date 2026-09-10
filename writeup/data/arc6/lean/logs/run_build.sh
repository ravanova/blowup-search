#!/usr/bin/env bash
export PATH="$HOME/.elan/bin:$PATH"
S=/tmp/claude-0/-home-user-blowup-search/f04cf05e-679d-5fc5-8545-c07be1caa01d/scratchpad
cd "$S/nse" || exit 1
{
  echo "=== BUILD_T0 $(date -u +%FT%TZ)"
  echo "=== cores $(nproc)  lean $(lean --version)"
  echo "=== NOTE: lake exe cache get is UNAVAILABLE here — mathlib4.blob.core.windows.net"
  echo "===       is denied by this environment's egress policy (502 to CONNECT)."
  echo "===       mathlib is therefore compiled FROM SOURCE."
  lake build
  echo "=== BUILD_RC=$? $(date -u +%FT%TZ)"
} >> "$S/lean_build.log" 2>&1
