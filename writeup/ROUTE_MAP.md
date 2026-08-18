# ROUTE_MAP — the problem-space diagram, and how to regenerate it

**`writeup/ROUTE_MAP.html`** is a single self-contained page: a decision tree of every route from the
Clay Navier–Stokes problem down to this programme's targets, showing which branches are **closed by
measurement**, which are **live**, and which have a **unit in flight**. Published as an artifact and
kept in the repository so the source of every status is auditable.

**What it is for.** Answering *"what have we closed off, and what is left?"* in one screen. The prose
files answer that too, but they answer it across four documents and a dozen journals, and a reader
has to assemble the tree themselves. The map is worth its maintenance cost only while that is true.

---

## THE RULE: THIS FILE IS NOT REGENERATED AUTOMATICALLY

**A Conductor MUST NOT rebuild this diagram as part of a wave.** Two reasons, and the second is the
one that matters:

1. It is not on the critical path, and §3j exists because this programme's read surface grows without
   anybody deciding it should.
2. **Every status on the map is the repository's own recorded verdict in its own pre-committed
   wording.** A diagram regenerated under time pressure drifts toward the drawer's summary of the
   record rather than the record — which is the exact failure mode (`leg 348`'s ceiling, the `C1`
   exemplar, the `8×` units error) that has cost this programme the most.

**What a Conductor SHOULD do instead:** when a wave changes a wall's status, a lane's ranking, or a
break clause, **flag the map as stale in the integration commit** — one line, naming what changed.
Staleness is cheap; a confidently wrong diagram is not.

## Regenerating it — the procedure

Do this when asked for a diagram of progress, or when the staleness flags have accumulated.

1. **Read the record, not this file's previous version.** `WALLS.md` (every wall's live statement and
   status), `STATE.md` (lane table, ranking, what landed), `OPTIONS.md` (deferred items and their
   re-open conditions), `writeup/escalations/` (what is on the user's desk and what has been ruled),
   and `CLAY_OBLIGATIONS.md` §§1–6.
2. **Take every status verbatim.** If a wall says `STANDS, STRENGTHENED`, the map says that. If a
   clause is `SHUT, VERIFIED`, the map says which unit shut it and which verified it. **Never
   paraphrase a gate answer into a status.**
3. **Distinguish four states and no more:** `closed by measurement` · `live` · `unit in flight` ·
   `never explored`. "Deferred by ranking" is **not** closed — a decision is not a measurement, and
   collapsing the two is how a parked branch becomes an invisible one.
4. **Draw the mechanism where there is one.** Figure 2 exists because the clause-(b) closure is a
   pincer of two published theorems on one surviving term; that is a mechanism a reader cannot
   assemble from prose. A box labelled "closed" is not.
5. **Carry the caveats onto the page**, not into a footnote: what is `UNVERIFIED`, what rests on a
   source read at second hand, what is measured on a synthetic object rather than a real one.
6. **Ceiling and odds go in the header.** Tier 2, Clay ~0.05%, and the count of `L1 → L4` links moved
   (zero, in 403 legs). A progress diagram that omits them reads as progress.

## Constraints on the page itself

- **Self-contained.** No external assets except Google Fonts. Inline SVG only, hand-authored, no
  libraries. It must render offline from the file alone.
- **Both themes.** Tokens on bare `:root`, redefined under `prefers-color-scheme: dark` guarded as
  `:root:not([data-theme="light"])`, and again under `:root[data-theme="dark"]`.
- **Not capped by §3j.** This is a leaf artifact, not a read surface — no worker reads it to do a
  unit, so it costs no per-agent tokens. It is exempt from the caps and must never be cited as a
  source by a unit. **The record is the source; this is a view of it.**

## Provenance of the current version

Drawn 2026-08-18 against `main`, after `V5` (leg 402) landed. Known to be current for: W1–W7 statuses,
the W4 clause table, Lane rankings, the W3 wording ruling, and `V5`'s finding that the Grade-A × fluid
occupant is **genuinely 3D** on W2's own test. **Flag anything later than that as unmapped.**
