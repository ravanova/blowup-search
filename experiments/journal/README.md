# Per-leg journal entries

`experiments/JOURNAL.md` is append-only and was written by one leg per day. With several legs
running in parallel (see `ORCHESTRATION.md` §2) it became the single worst merge-conflict
point in the repo.

**Each leg now writes `leg_<N>.md` here instead** — same content, same care, one file per leg.
The orchestrator adds a one-line pointer to `JOURNAL.md` at integration, so the ledger still
reads top-to-bottom and still has exactly one writer.

Same shape as the entries in `JOURNAL.md`: what ran and where its outputs went, why the leg
exists, what a human should notice, and what it cost. `LOGGING.md` covers the structured
logs — this is the *why*.
