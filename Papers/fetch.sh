#!/usr/bin/env bash
# Re-pull the source PDFs listed in Papers/MANIFEST.md.
#
# Papers/ is gitignored, so these are lost every time the container is rebuilt.  This
# script exists so that is a one-command inconvenience rather than a re-derivation.
#
#   bash Papers/fetch.sh              # everything in priority order
#   bash Papers/fetch.sh 2207.07548   # just one
#
# It FAILS LOUDLY if egress is blocked, and prints the exact thing to ask for, because a
# silent empty Papers/ is how five literature passes stayed search-level.

set -uo pipefail
cd "$(dirname "$0")"

TIER1=(2207.07548 2210.07191 2209.08232 2607.19762)
TIER2=(2302.12877 2312.01702 1908.09385)
TIER3=(2308.01528 2604.01868 2010.01201 2305.05895 2401.14615 2603.25104 2604.09949)

# ARC 6 (leg 417, 2026-09-09): three NON-arXiv primaries.  These are the objects arc 6
# adjudicates, so they are re-pullable by name and their sha256 are banked in
# writeup/data/arc6_acquire_v1.json :: artifacts_fetched.  `bash Papers/fetch.sh openai`
# pulls exactly these three and verifies each hash.
declare -A DIRECT=(
  [openai-navier-stokes.pdf]="https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf"
  [openai-euler.pdf]="https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf"
  [fefferman-navierstokes-clay.pdf]="https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf"
)
declare -A DIRECT_SHA=(
  [openai-navier-stokes.pdf]="0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f"
  [openai-euler.pdf]="a0c234518e6c489e16996805023eb2e75c00b7c03455f7a3a5be2c124954bfdd"
  [fefferman-navierstokes-clay.pdf]="c1b5f27b1a64705cfaf1afceea513db5deedca8a18ca56ab32e7f86445a06d0c"
)

if [ "${1:-}" = "openai" ]; then
  echo "== arc 6 direct primaries (no arXiv, no egress probe) =="
  rc=0
  for out in "${!DIRECT[@]}"; do
    printf '  fetch  %s ... ' "$out"
    if curl -sSL --max-time 300 -o "$out" "${DIRECT[$out]}" && [ -s "$out" ] \
       && head -c 4 "$out" | grep -q '%PDF'; then
      got="$(sha256sum "$out" | cut -d' ' -f1)"
      if [ "$got" = "${DIRECT_SHA[$out]}" ]; then
        echo "ok, sha256 matches"
      else
        echo "FETCHED BUT HASH DIFFERS -- the published file changed under us."
        echo "         banked: ${DIRECT_SHA[$out]}"
        echo "         got:    $got"
        echo "         Do NOT overwrite the banked hash.  A changed primary is a FINDING:"
        echo "         record it in writeup/CORRECTIONS.md against arc6_acquire_v1.json."
        rc=1
      fi
    else
      echo "FAILED"; rm -f "$out"; rc=1
    fi
  done
  echo "Papers/ is gitignored ON PURPOSE -- do not commit the PDFs."
  exit "$rc"
fi

if [ $# -gt 0 ]; then IDS=("$@"); else IDS=("${TIER1[@]}" "${TIER2[@]}" "${TIER3[@]}"); fi

probe() {
  curl -sS -o /dev/null -w '%{http_code}' --max-time 25 "https://arxiv.org/abs/2207.07548" 2>/dev/null
}

echo "== egress probe =="
code="$(probe)"
if [ "$code" = "000" ] || [ "$code" = "403" ]; then
  cat <<'EOF'
BLOCKED: arxiv.org is not reachable from this container.

Diagnosis (verified, do not re-derive): the agent proxy returns 403 to the CONNECT for
non-allowlisted hosts.  github.com IS allowlisted (returns a real HTTP response); arxiv.org,
en.wikipedia.org and api.semanticscholar.org are NOT.  This is the ENVIRONMENT'S NETWORK
POLICY, not a WebFetch bug and not an arXiv-side block -- WebFetch 403s for the same reason.

ASK THE USER TO ADD THESE HOSTS TO THE ENVIRONMENT'S EGRESS ALLOWLIST:
    arxiv.org  export.arxiv.org  api.semanticscholar.org  www.semanticscholar.org
    link.springer.com  onlinelibrary.wiley.com  aimsciences.org  en.wikipedia.org

Network policy is chosen when the environment is created; see
https://code.claude.com/docs/en/claude-code-on-the-web

Re-run this script once that is done.  Do NOT work around it by disabling TLS
verification or unsetting HTTPS_PROXY.
EOF
  exit 2
fi
echo "arxiv.org reachable (HTTP $code) -- fetching"

ok=0; fail=0
for id in "${IDS[@]}"; do
  out="${id}.pdf"
  if [ -s "$out" ]; then echo "  have   $out"; ok=$((ok+1)); continue; fi
  printf '  fetch  %s ... ' "$out"
  if curl -sSL --max-time 120 -o "$out" "https://arxiv.org/pdf/${id}" \
     && [ -s "$out" ] && head -c 4 "$out" | grep -q '%PDF'; then
    echo "ok ($(du -h "$out" | cut -f1))"; ok=$((ok+1))
  else
    echo "FAILED"; rm -f "$out"; fail=$((fail+1))
  fi
done

echo "== $ok fetched/present, $fail failed =="
echo "Papers/ is gitignored ON PURPOSE -- do not commit the PDFs."
[ "$fail" -eq 0 ]
