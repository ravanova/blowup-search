#!/bin/bash
# On-demand retrieval of the grounding papers.
#
# The Papers/ directory is gitignored on purpose — copyrighted PDFs are not
# redistributed through the repo — so a fresh clone (including every cloud
# session) starts without it. This script pulls the papers from their canonical
# arXiv source only when a session actually needs to consult one. The PDFs land
# in the gitignored Papers/, so they are never committed.
#
# CLOUD NETWORK NOTE: arxiv.org is NOT in the default cloud allowlist. Before
# running this in a "Claude Code on the web" session, open that environment in
# the app, set Network access to **Custom**, add `arxiv.org` (keep the default
# package registries ticked), and save. Local laptop runs need no such step.
#
# Usage:
#   scripts/fetch_papers.sh              # fetch every known paper
#   scripts/fetch_papers.sh 2401.14615   # fetch one (or several) by arXiv id

set -u
DEST="$(cd "$(dirname "$0")/.." && pwd)/Papers"
mkdir -p "$DEST"

# arXiv id -> local filename (matches the names the writeup + notes reference).
# 2401.14615 = [HQW25], the primary grounding paper for the P2 / Route-D work.
declare -A PAPERS=(
  [2401.14615]="2401.14615v_HQW25.pdf"
  [2210.07191]="2210.07191v3.pdf"
  [2305.05660]="2305.05660v2.pdf"
  [2604.01868]="2604.01868v1.pdf"
)

have_dl=""
if command -v curl >/dev/null 2>&1; then have_dl="curl"
elif command -v wget >/dev/null 2>&1; then have_dl="wget"
else echo "ERROR: neither curl nor wget is available" >&2; exit 1
fi

fetch() {
  local id="$1" out="$DEST/${PAPERS[$1]:-$1.pdf}"
  if [ -s "$out" ]; then echo "have   $id -> $out"; return 0; fi
  echo "fetch  $id -> $out"
  local ok=1
  if [ "$have_dl" = "curl" ]; then
    curl -fsSL "https://arxiv.org/pdf/$id" -o "$out" && ok=0
  else
    wget -q "https://arxiv.org/pdf/$id" -O "$out" && ok=0
  fi
  if [ "$ok" -eq 0 ] && [ -s "$out" ]; then
    echo "  ok ($(du -h "$out" | cut -f1))"
  else
    echo "  FAILED — network blocked? In a cloud session, allowlist arxiv.org (see header)." >&2
    rm -f "$out"
  fi
}

if [ "$#" -ge 1 ]; then
  for id in "$@"; do fetch "$id"; done
else
  for id in "${!PAPERS[@]}"; do fetch "$id"; done
fi
