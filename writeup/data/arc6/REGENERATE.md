# Two files in this directory are not in the repository

`manuscript_pages.txt` and `manuscript_pages.jsonl` are the per-page extracted text
of *"Finite Time Blowup for Navier–Stokes"* (OpenAI, 166 pp). **We do not own that
text and do not redistribute it**, so — like every third-party PDF in this project —
it is gitignored rather than committed. See [`NOTICE.md`](../../../NOTICE.md) §3.

Everything else in this directory *is* committed: the ledger, the DAG, the spine,
the Lean measurements, and `extract_manifest.json`, which pins the sha256 of the
source PDF and of both regenerated outputs. So a fresh clone can verify that what it
regenerates is byte-identical to what the arcs were read from.

## Regenerate, two commands

```bash
bash Papers/fetch.sh openai                              # pulls the PDF, verifies sha256
.venv/bin/python experiments/arc6_extract_pages.py       # writes both files + manifest
```

Expected: 166 pages, 599,585 bytes of `.txt`, 876,552 bytes of `.jsonl`, and the
hashes in `extract_manifest.json` reproduced exactly. Source PDF sha256:

```
0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f  navier-stokes.pdf
fe32a61fac197fa073bb2e9305ab0b22c2442c6ab775daafe029c0982941a8a2  manuscript_pages.txt
3418c38c48ba796f858dae7395d48dc0a1e703fdadf1509035225dd238d88422  manuscript_pages.jsonl
```

Check with `sha256sum writeup/data/arc6/manuscript_pages.*`. All three are also in
`extract_manifest.json`, which is committed — so the hashes are not taken on trust
from this page.

## If a script here fails with FileNotFoundError

That is the expected failure and it is loud on purpose. `experiments/arc6_dag.py`
and `writeup/arc6_extract_evidence.py` both read these files. Run the two commands
above and re-run. A silent empty extraction is how a literature pass stays
search-level — this project has the scar and prefers the crash.

## Why the extraction is per-page rather than concatenated

Naive concatenation corrupts statements that straddle a page break and injects
running headers mid-sentence; Corollary 10.6 (pp. 125–126) is the demonstrated case.
Every line carries its page number, which is what makes every quotation in arcs 6
traceable to a page.
