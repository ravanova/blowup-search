# Leg 68 (Route-IX) — novelty pass: the on-disk quartet inventory for legs 53–57

This leg is a documentation-index fix, so its "novelty pass" is not a literature pass. It is
the thing the edit is actually claiming: **exactly which quartet pieces exist on disk** for
legs 53 (TC), 54 (MM), 55 (NB), 56 (TN), 57 (XS). Everything below was checked by listing
and stat-ing the files in this worktree, not inferred from a merge log or a commit message.

Quartet convention, as documented at the top of `writeup/INDEX.md` (Arc 4 legend):
R = runner in `experiments/`, D = curated data JSON in `writeup/data/`, B/T = BLOG+TECHNICAL
pair in `writeup/4_p2_lottery/`, E = a `*_evidence.py`, F = a figure present in
`writeup/figures/` and referenced by the docs.

## Counts

**25 of 25 pieces present (5 legs x 5 pieces). 0 missing. 0 zero-byte.**

Per leg: 5/5, 5/5, 5/5, 5/5, 5/5.

## The inventory, file by file

### Leg 53 — Route-TC (5/5)
- R `experiments/p2_route_tc_v1_assemble.py`
- D `writeup/data/p2_route_tc_v1_assemble.json` — 50729 bytes
- B `writeup/4_p2_lottery/BLOG_P2_ROUTETC_V1.md`
- T `writeup/4_p2_lottery/TECHNICAL_P2_ROUTETC_V1.md`
- E `writeup/4_p2_lottery/p2_route_tc_v1_evidence.py` — 11661 bytes
- F `writeup/figures/fig48_route_tc_v1_assemble.png`, referenced as `fig48` by TECHNICAL

### Leg 54 — Route-MM (5/5)
- R `experiments/p2_route_mm_v1_shape.py`
- D `writeup/data/p2_route_mm_v1_shape.json` — 143884 bytes
- B `writeup/4_p2_lottery/BLOG_P2_ROUTEMM_V1.md`
- T `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEMM_V1.md`
- E `experiments/p2_route_mm_v1_shape_evidence.py` — 13413 bytes
- F `writeup/figures/fig49_route_mm_v1_shape.png`, referenced as `fig49` by TECHNICAL
- (extra, not a quartet slot: `experiments/p2_route_mm_v1_headline_verify.py`)

### Leg 55 — Route-NB (5/5)
- R `experiments/p2_route_nb_v1_targetnorm.py`
- D `writeup/data/p2_route_nb_v1_targetnorm.json` — 60766 bytes
- B `writeup/4_p2_lottery/BLOG_P2_ROUTENB_V1.md`
- T `writeup/4_p2_lottery/TECHNICAL_P2_ROUTENB_V1.md`
- E `experiments/p2_route_nb_v1_targetnorm_evidence.py` — 10577 bytes
- F `writeup/figures/fig50_route_nb_v1_targetnorm.png`, referenced as `fig50` by both BLOG
  and TECHNICAL

### Leg 56 — Route-TN (5/5)
- R `experiments/p2_route_tn_v1_consistency.py`
- D `writeup/data/p2_route_tn_v1_consistency.json` — 17883 bytes
- B `writeup/4_p2_lottery/BLOG_P2_ROUTETN_V1.md`
- T `writeup/4_p2_lottery/TECHNICAL_P2_ROUTETN_V1.md`
- E `experiments/p2_route_tn_v1_consistency_evidence.py` — 11111 bytes
- F `writeup/figures/fig51_route_tn_v1_consistency.png`, referenced as `fig51` by both BLOG
  and TECHNICAL

### Leg 57 — Route-XS (5/5)
- R `experiments/p2_route_xs_v1_shapes.py`
- D `writeup/data/p2_route_xs_v1_shapes.json` — 20909 bytes
- B `writeup/4_p2_lottery/BLOG_P2_ROUTEXS_V1.md`
- T `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEXS_V1.md`
- E `experiments/p2_route_xs_v1_shapes_evidence.py` — 8050 bytes
- F `writeup/figures/fig52_route_xs_v1_shapes.png`, referenced as `fig52` by both BLOG
  and TECHNICAL

## Two form deviations, both non-gaps

1. **Evidence-script location.** 4 of the 5 evidence scripts (MM, NB, TN, XS) live in
   `experiments/`, not alongside their docs in `writeup/4_p2_lottery/`. Only TC's sits in
   `writeup/4_p2_lottery/`. Every earlier Arc-4 route in `INDEX.md` puts its `*_evidence.py`
   in `writeup/4_p2_lottery/`. The piece exists in all 5 cases — this is a placement drift,
   4 files' worth, not a missing artifact, so it is recorded as `Y` in the table and noted
   here rather than marked `GAP`.
2. **`fig48` is used twice.** Both `writeup/figures/fig48_route_tc_v1_assemble.png` (leg 53)
   and `writeup/figures/fig48_weight_repairs_v1.png` exist. That is 1 duplicated figure
   number in the registry. Leg 53's own figure is present and correctly referenced by its
   TECHNICAL, so TC's F slot is filled; the numbering collision belongs to whoever owns the
   figure registry and is out of this leg's declared territory.

## Prior-art check on the edit itself

`writeup/INDEX.md` at merge base `925913a` has an Arc 4 table ending at Route-T v1 (leg 52's
route), i.e. **5 route rows short**, and carries a paragraph asserting Route-TC "has no
writeup yet — it is in progress on `leg/tc-v1`", plus a trailing "## Route-TC (in progress...)"
section making the same claim. Both are false as of the inventory above: **2 stale
assertions**, both about a leg whose 5/5 quartet is on disk. No other leg-53..57 rows exist
anywhere in the file (grep for `ROUTETC`/`ROUTEMM`/`ROUTENB`/`ROUTETN`/`ROUTEXS`: 0 hits
before this leg's edit). So the edit is additive and not a duplicate of work already done.
