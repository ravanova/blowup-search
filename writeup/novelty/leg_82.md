# Leg 82 (Route-EXT3) — novelty pass and literature watch: has anyone certified `Boussinesq_S2_nonsymmetric` since April 2026?

**Pass date: 2026-08-06.** This leg is a literature watch, so the novelty pass and the leg's
deliverable are the same search — but they answer two different questions, and both are recorded
separately below:

1. **Novelty of the *method*** (§0) — is "check whether the target ledger's **rank-3** entry has
   gone stale" a thing this repository already did? **No**, and this leg claims **zero
   mathematical novelty**. It discovers nothing about the 2D Boussinesq equations. Its output is
   a *dated absence*, which is a fact about the literature, not about fluids.
2. **The gate** (§1–§5) — the search itself.

Query strings, endpoints and links (not counts, per this directory's README rule after leg 53)
are in `experiments/p2_route_ext3_v1_target_watch3.py` and re-emitted to
`writeup/data/p2_route_ext3_v1_target_watch3.json`. Every arXiv-API URL there re-runs verbatim.

---

## 0. The novelty pass: what this leg claims, and what it does not

**Claimed:** that as of **2026-08-06**, on **seven independent channels**, the published record
contains **zero** certificates — computer-assisted or analytic — for the non-symmetric,
strictly-positive regular self-similar profile of the **2D Boussinesq** equations reported in
Chen-Huang-Li arXiv:2604.01868 **section 6.2** (their Scenario 2, 2D).

**Not claimed:** anything about whether such a certificate is *possible*; anything about the
profile itself; and — importantly — anything about work that exists but is unposted. The gate
asks about the *published* record, and that is exactly the scope of the answer.

**Prior art inside this repository, and why this leg is not a repeat.** Two dated watches of the
same shape have already run and are on main:

| leg | route | ledger rank | object | dimension | source | verdict |
|---|---|---|---|---|---|---|
| 74 | EXT  | 1 | `HL_S2_nonsymmetric`         | **1D** | arXiv:2604.01868 §2.5 / §4 | NO |
| 77 | EXT2 | 2 | `gCLM_degenerate_one_scale`  | **1D** | arXiv:2603.25104 §4        | NO |
| **82** | **EXT3** | **3** | **`Boussinesq_S2_nonsymmetric`** | **2D** | **arXiv:2604.01868 §6.2** | **this leg** |

Leg 82 shares a *paper* with leg 74 but not a *section*, not an *object*, not an *equation* and
not a *dimension*: leg 74 watched the 1D Hou-Luo model's non-symmetric profile (§2.5/§4); this
leg watches the 2D Boussinesq analogue (§6.2). The two live in different sections of the same
51-page numerical paper and would be certified by different machinery — §6.2 carries a 2D
Biot-Savart law with **no symmetry reduction available** and **three** modulation constants
against the 1D object's two. A certificate for one is not a certificate for the other, so the
watches are genuinely independent. Leg 77 shares neither paper nor object.

**Not touched:** `solver/target_selection.py`. It was **read** for the rank-3 entry's exact
fields and never opened for writing; leg 63 (M2) owns that file, and any ledger edit this watch
implies is that leg's to make. This watch implies **none** — see §5.

**`capabilities.py` was grepped first**, as the plan of record requires ("building a solver
without grepping capabilities.py for the object first" is a standing permanent ban). Result:
`Boussinesq_S2_nonsymmetric` appears **nowhere** in `capabilities.py` — the registered 2D
Boussinesq object at line 88 is explicitly annotated as "the CERTIFIED object", i.e. Chen-Hou's
symmetric profile, which is a *different* object and is the one the plan of record bans as a
target. `solver/target_selection.py` itself is registered at line 353. **Nothing was built, so
nothing was rebuilt.** This leg is pure literature: no computation, no solver call, no gCLM
measurement (the standing ban on further gCLM measurement legs is respected trivially — this leg
touches no model at all).
