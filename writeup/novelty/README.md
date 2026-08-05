# Per-leg novelty query logs

The novelty pass runs **before** construction, and its query log is committed — that rule has
closed one stage (48), narrowed four (49, 51, 52, 53) and cleared one standing flag.

`LITERATURE_CHECK.md` is the ledger, and with four parallel legs it cannot have four writers.
**Each leg writes `leg_<N>.md` here**; the orchestrator adds a one-line pointer to
`LITERATURE_CHECK.md` at integration.

Log **links, not counts.** Leg 53 logged result counts, so its claim could not be audited and
was later withdrawn when LIT re-ran the query verbatim. Record the exact query string, the
date, and the links returned.
