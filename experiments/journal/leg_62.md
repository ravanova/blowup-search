# Leg 62 — Route-CP: the Cadiot pre-emption, settled from the full text

**Branch** `leg/cp-v1`. **Slot** LEG-B, exploration (not critical path). **Difficulty**
standard. **Gate answer: NO.**

> **Gate (`DIRECTION.md`, verbatim).** Does Cadiot arXiv:2505.03091's construction cover an
> operator whose unbounded part is off-diagonal with a non-decaying tail inverse — i.e.
> does it already contain leg 58's no-go, or a positive result that contradicts it?
>
> **no →** The gap leg 57's ledger measured is confirmed at full-text depth for the one
> paper most likely to close it. Bank the located hypotheses as an executable ledger entry;
> NG may claim novelty against this paper and no further.

## Sequence

1. **Novelty pass FIRST**, committed before construction (commit `d2e29f5`,
   `writeup/novelty/leg_62.md`, verdict `PROCEED_AS_BOOKKEEPING`, four verbatim queries
   with links not counts). This leg claims **no mathematical novelty of its own**.
2. Grepped `capabilities.py` before building — `solver/certificate_shapes.py` (leg 57) and
   `solver/literature_gates.py` (Route-J) were already indexed; nothing was rebuilt.
3. Primary source fetched, not searched: `bash Papers/fetch.sh 2505.03091`, 30 pp., pypdf.
4. Construction, then the quartet.

## What was built

* `solver/certificate_shapes.py` — **additive only**. `CADIOT_SCOPE` (six located clauses),
  `CP_FORWARD` (two forward citations + one independent candidate), `CP_NOT_OBTAINED`
  (Farid–Lancaster, paywalled, recorded rather than glossed), `CADIOT_EXAMPLES` (his four
  worked symbols), `cadiot_symbol_admissibility`, `gershgorin_rows`,
  `gershgorin_dominance_ratio`, `cadiot_shift_requirement`, `shift_requirement_ladder`,
  `cadiot_whitham_matrix`, `cadiot_ratio_ladder`, `our_operator_gershgorin`,
  `cadiot_vs_bdl_thresholds`, `cadiot_covers`, `CP_SYNTHETIC_COVERING_SCOPE`.
* `test_certificate_shapes.py` — gates **16–25** appended. Gates 1–15 (leg 57) untouched
  and still pass. Full file: **25/25**.
* `experiments/p2_route_cp_v1_cadiot.py` → `writeup/data/p2_route_cp_v1_cadiot.json` (2 s).
* `experiments/p2_route_cp_v1_cadiot_evidence.py` → `writeup/figures/fig56_route_cp_v1_cadiot.png`,
  registered in `writeup/build_figures.py` (appended; the file stays append-only).
* `writeup/4_p2_lottery/{BLOG,TECHNICAL}_P2_ROUTECP_V1.md`.

## The finding, as magnitudes

* Cadiot's construction fails to reach our operator on **6 of 6 located clauses**, the
  strongest being the class definition itself (eq. (1)–(2): `L` is a Fourier multiplier,
  hence diagonal in the Fourier index) — reached *before* Assumption 1.
* **Assumption 1 re-derived from his own symbols**, not quoted: `l_min = 0.280000 / 0.320000
  / 0.200000 / 0.999938` for §5.1.1 / §5.1.2 / §5.2 / §5.3, matching the numbers he states
  in words to `1.42e−07` (Swift–Hohenberg, grid resolution at the minimum) and `5.6e−17`
  (Whitham). Ours: **`0.0` exactly**.
* **§5.3, his one systems example** — the only place an off-diagonal entry appears in the
  paper: entry is the constant `λ₁λ₂−1 = 1/9`, diagonal growth `+2.0000`, ratio exponent
  **`−2.0000`**, `2.53e−10` at `|ξ| = 1e4`. Ours is flat.
* **Lemma 3.2's shift, the load-bearing measurement.** Minimum `|s|` with
  `|λ_n+s| > r_n/2` at every `n`: his Whitham operator gives **`0.28723` at every
  truncation** `N = 128…1024` (exponent `+6.1e−17`); ours gives `63 → 1023` over
  `M = 128…2048`, exponent **`+1.0051`** — **linear in the truncation, so no finite `s`
  survives the limit.** His `0.28723` is predicted exactly by `sqrt((r/2)² − l_min²)` with
  his own `l_min = 0.2`.
* Dominance ratio ladder: his `−0.816, −0.738, −0.659, −0.605` over `N = 128…1024` (toward
  the analytic `−1/2`); ours `+0.0039` at every `μ > 0` (flat) and **refused** at `μ = 0`
  (all 502 interior rows have an exactly zero diagonal — no referent, discipline 73).
* **Three thresholds kept apart:** Cadiot's Lemma 3.2 admits the `Λ¹`-dissipated family for
  `μ ≥ 0.5`; BDL's assumption (5) only for `μ > 1` (factor exactly 2); leg 57's *operator*
  hinge is `μ = 0`. Both hypotheses vacuous where it matters. Mechanism checked as an
  identity, not assumed: `r_k = k − 1` for interior rows (max err `≤ 5.7e−14`).

## Controls (lesson 90)

* The gate predicate flips to `yes` **two independent ways** (a covering scope; a forward
  citation that relaxes the hypothesis) — gate 18.
* The saturating `|s| = 0.28723` is identical at four truncations, which is the pattern
  lesson 90 says to distrust. It **moves** with the operator (`0.0 → 9.998` as the compact
  part's `ℓ¹` norm goes `0.05 → 10`) while the exponent does **not** (spread `4.1e−15`) —
  gate 23. Level responds, shape does not.
* The `DG(U0)` of the Whitham control is a **surrogate** and is labelled one in the module,
  the JSON, the runner docstring and the TECHNICAL: his `u0` is not distributed with the
  paper. It is built so it cannot carry the conclusion (its `ℓ¹` norm is a dial; its centre
  coefficient is zeroed, which is the choice conservative *against* his framework).

## Deliberate omissions, with reasons

* **`SHAPE_LEDGER` was not touched.** Its "four papers / 15-of-15 gates" count is quoted in
  leg 57's prose, in `PHASE2_P2_NOTES.md` and in `CONTINUATION_PROMPT.md`. Adding the
  Burgers–Hilbert row there would silently falsify three documents this leg may not edit.
  It went into `CP_FORWARD` instead.
* **`solver/literature_gates.py` and `test_literature_gates.py` were not touched**, though
  they are in this leg's declared territory: adding a 13th row to `CLAIM_LEDGER` would
  stale `capabilities.py`'s "twelve standing claims", which is not this leg's to fix.
* **`solver/spectral_certificate.py` was not touched.** The dispatch prompt named it as this
  leg's territory; `DIRECTION.md` assigns it to **leg 58**, which is live and concurrent.
  `DIRECTION.md` is the ground truth the prompt itself defers to, so this leg only *reads*
  `tail_block` from it. **Flagged for the orchestrator** — the prompt and the file disagree.
* **`capabilities.py`** — the `solver/certificate_shapes.py` row's `holds`/`validated`
  fields now under-describe the module (they predate `CADIOT_SCOPE`). Not edited here: leg
  71 (CAP) is live on that file, one row per module is the file's convention, and the row
  is not factually wrong, only incomplete. **Suggested integration edit**, not taken.

## Ceiling

Four papers is a corpus, not a theorem. Every quote is transcribed from a full text by a
human-equivalent process and is exactly as good as that (every row carries its URL so the
next pass can check rather than trust). All numbers are float64 measurements of matrices,
no intervals. This leg is **not** evidence *for* leg 58's proposition — a gap in one paper
is not a theorem — and it does **not** lift the standing ban on re-claiming leg 51's
finding at full strength: answering the ban's named question does not discharge it, and the
correct bookkeeping change is a narrowing annotation, which is integration-owned.

No link of the L1→L4 chain moved.
