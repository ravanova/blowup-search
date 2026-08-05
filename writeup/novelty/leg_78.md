# Leg 78 (Route-HLB) — novelty pass and precision search: is CHL's Scenario-2 contraction ratio published anywhere to more than five significant figures?

**Pass date: 2026-08-06.** This leg is a literature search with a known-answer re-measurement
attached, so the novelty pass and the leg's deliverable overlap — but they answer two different
questions and both are recorded separately:

0. **Novelty of the *method*** (§0) — is "audit the *precision* of a known-answer anchor, rather
   than its existence" something this repository already did? Leg 61 (KA) did it for CLN's
   Kawahara radius; **this leg claims zero mathematical novelty** and discovers nothing about the
   Hou–Luo model. Its output is a *dated measurement of the published record's precision*.
1. **The gate** (§1–§4) — the search, and what our own line measures against what it finds.

Query strings, endpoints and links (**links, not counts**, per this directory's README rule after
leg 53) are in `experiments/p2_route_hlb_v1_contraction_lit.py` and re-emitted to
`writeup/data/p2_route_hlb_v1_contraction_lit.json`. Every arXiv-API URL there re-runs verbatim.

`capabilities.py` was grepped first, as the plan of record requires. The relevant entries are
**line 45–52** (`solver/hl_rescaled.py`, whose `validated` string carries the `~1%` annotation
this leg is auditing) and **line 296–307** (`solver/bordered_hl.py`, whose `validated` string
carries a *different and much tighter* number for the same anchor). Nothing was built; the only
new executable is the query log. **`solver/hl_rescaled.py` was read and not edited.**

---

## 0. What this leg claims, and what it does not

**Claimed:** that as of **2026-08-06**, the entire published record for the Scenario-2 contraction
ratio `c_l/c_ω` of the 1D Hou–Luo model's non-symmetric regular profile consists of **two
occurrences of the same five-significant-figure number, −2.5114, in one preprint** — Chen–Huang–Li
arXiv:2604.01868, still at v1 — with **no table, no supplementary data, no code release, and no
vector figure** from which a sixth digit could be recovered, and **no replication by anyone**.

**Not claimed:** that −2.5114 is *accurate* to five digits. It is *printed* to five digits. Its
own paper reports it from a relaxation stopped at `max{‖Ω_t‖_∞, ‖V_t‖_∞} < 1e−6` with no error
bar and no resolution study, and states it once with an explicit `≈`. Digit granularity is not an
error bar, and this leg does not convert one into the other.

**Not touched:** `solver/hl_rescaled.py` (read only), `capabilities.py`, and all five shared
ledgers.

---

## 1. The gate, answered

> **Does a primary source publish the Scenario-2 contraction ratio to tighter precision than the
> ~1% figure this repository currently checks against, and if so does our number still agree at
> that tighter tolerance?**

**NO — no tighter value exists to be found.** The tightest published figure is the source paper's
own **−2.5114**, whose last printed digit is `1e−4` absolute = **3.98e−05 relative**. That is
already **~250× tighter than the `~1%` this repository checks at**, and it has been the tightest
available figure for **126 days**. Five channels, **0 of 5** produced a sixth digit or an
independent replication.

**The `~1%` is therefore ours, not theirs.** It is a *tolerance*, not a *precision*: the loose side
of the comparison is our relaxation line, not CHL's number. That distinction is the leg's actual
finding and it is recorded in §4 as a report-only flag.

---

## 2. The channels, with their magnitudes

| # | channel | what was enumerated | tighter value found |
|---|---|---|---|
| P1 | the source paper, **full text** | every occurrence of the constant in arXiv:2604.01868 | **0** (2 occurrences, both `−2.5114`) |
| P2 | the source paper, **figures** | Fig 4.2, the panel the value is read off | **0** (raster, not vector — see §2.2) |
| P3 | the source paper, **artifacts** | code/data availability, GitHub, Zenodo, supplement | **0** (no such statement anywhere) |
| P4 | **versions and journal record** | arXiv version history, journal-ref, DOI | **0** (v1 only, 2 Apr 2026, no journal-ref) |
| P5 | **replication** | citation graph + the Hou–Luo corpus + the authors' own feeds | **0** citing works |

### 2.1 P1 — the constant appears exactly twice, at five significant figures both times

Full text extracted from the PDF (`pdftotext`, not the abstract, not the listing page). `−2.5114`
occurs at **two** places and nowhere else:

* **§4, body:** *"The computed limiting value of `c_l/c_ω` is −2.5114. Notably, this value is
  distinct from the ratio of approximately −2.9987 reported in [CHH22] for the odd-symmetric
  non-degenerate case."*
* **Fig 4.2, caption:** *"The black dashed lines represent the computed limiting values
  `(c_l, c_ω, c_r, c_l/c_ω) ≈ (1.0636, −0.4235, 0.0765, −2.5114)`, respectively."* — note the `≈`.

The companion constants are printed at the same granularity: `1.0636`, `−0.4235`, `0.0765` — four
decimals each. **There is no table of constants in the paper.** The stated stopping criterion is
`max{‖Ω_t‖_∞, ‖V_t‖_∞} < 1e−6` over grid points; **no resolution study of the constants, no
domain-size study, and no error bar** accompanies them. So the five digits are the *print
precision of a single converged run*, which is exactly the thing this leg was sent to check and
exactly the thing that cannot be tightened from outside.

### 2.2 P2 — the figures are raster, so leg 48's read-the-figure trick does not apply here

Leg 48 recovered published curve data by reading Dahne–Figueras' **pgf vector** figures back as
numbers (`read_df_figure`). That route is **closed here**: `pdfimages -list` on 2604.01868 reports
**90 embedded raster images**, Fig 4.2's panels among them, at **3125 × 2500 px**. Reading the
black dashed limiting line off a bitmap at that size gives, optimistically, one part in ~2500 of
the plotted axis range — i.e. **4.0e−04 relative at best**, roughly **10× coarser than the
printed −2.5114's 3.98e−05 granularity**. The figure cannot beat the caption. Recorded as a
measured magnitude, not an impression: the file was pulled and `pdfimages -list` run on it.

### 2.3 P3 — there is no artifact behind the number

Grep of the full text for `github`, `code is available`, `data availab`, `supplementary`,
`zenodo`: **zero hits**. There is no repository, no dataset, and no supplement. The number cannot
be re-derived at higher precision from anything the authors released, only by re-running their
scheme — which is what this repository already does independently.

### 2.4 P4 — the paper has not moved

`arXiv:2604.01868` is **v1**, sole submission **2 Apr 2026 10:25:28 UTC**, comment `51 pages`,
**no journal-ref**, no DOI beyond the arXiv DOI. A journal version is the single most likely place
for a constants table to appear, and after **126 days** there is none. (Independently consistent
with leg 74's C1, same day, different question.)

### 2.5 P5 — nobody has replicated it

* **Citation graph:** Semantic Scholar `graph/v1/paper/arXiv:2604.01868/citations` returns an
  **empty `data` array** — 0 citing works.
* **The corpus:** the only arXiv entry matching `all:"Hou-Luo"` submitted after the source paper
  is **arXiv:2605.16322** (Yaoming Shi, 5 May 2026), a Riccati blow-up argument for a closed
  boundary-jet model; it does not cite 2604.01868 and reports **no** `c_l`, `c_ω` or ratio.
* **The authors:** De Huang / Bojin Chen / Xiangyuan Li have **0** arXiv submissions after
  2604.01868. Their nearest companion, **arXiv:2603.25104** (gCLM singular profiles), *did* get a
  **v2 on 16 Jun 2026** — the one post-hoc update in this neighbourhood — and it was pulled and
  searched: it does **not** mention 2604.01868, the non-symmetric profile, or any `2.511…` value.
* **The obvious near-misses were cleared, not assumed:** **arXiv:2605.15149** (Jiajie Chen, 14 May
  2026, 3D Euler `C^{1,1/3−}` profiles) and **arXiv:2604.16842** (the April 2026 singularity-
  formation survey, the likeliest place for a *tabulated* constant) were both fetched, text-
  extracted and grepped for `2.511`, `2604.01868`, `Xiangyuan`, `non-symmetric`: **0 hits in
  either**.

---

## 3. Links (not counts)

* Source paper — https://arxiv.org/abs/2604.01868 · PDF https://arxiv.org/pdf/2604.01868 ·
  HTML https://arxiv.org/html/2604.01868v1
* Citation graph —
  `https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868/citations?fields=title,year,externalIds,abstract&limit=100`
* Corpus enumeration —
  `http://export.arxiv.org/api/query?search_query=all:%22Hou-Luo%22&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending`
* Author enumeration —
  `http://export.arxiv.org/api/query?search_query=au:%22De+Huang%22+OR+au:%22Bojin+Chen%22&start=0&max_results=40&sortBy=submittedDate&sortOrder=descending`
* Companion v2 — https://arxiv.org/abs/2603.25104 (v2, 16 Jun 2026)
* Cleared near-misses — https://arxiv.org/abs/2605.16322 · https://arxiv.org/abs/2605.15149 ·
  https://arxiv.org/abs/2604.16842
* Author page — https://sites.google.com/view/de-huang/research

---

## 4. What follows from a "no", and what does not

**Banked:** as of **2026-08-06**, `−2.5114` (5 s.f., 3.98e−05 relative granularity) is the **best
precision on record** for the Scenario-2 contraction ratio. No change to any solver. No claim
about the Hou–Luo model.

**The measured magnitudes that answer the gate's second clause** (re-measured by this leg, not
quoted — the bordered ladder was re-run live; see `experiments/journal/leg_78.md` §5):

| line | ratio | rel. err vs −2.5114 | in units of the anchor's 3.98e−05 print granularity |
|---|---|---|---|
| relaxation (`solver/hl_rescaled.py`) | −2.53344 | **8.78e−03** | **220×** |
| bordered, extrapolated in reach (`solver/bordered_hl.py`) | −2.51192 | **2.09e−04** | **5.3×** |
| *our own extrapolation's window spread* | — | 9.74e−05 | **2.4×** |

The last row is the one that settles the counterfactual. **Even if CHL published a sixth digit
tomorrow, we could not use it:** the spread of our own limit across its extrapolation windows is
already **2.4×** the anchor's current print granularity. The comparison is saturated on our side
at ~1e−4, so `−2.5114` at 3.98e−05 is not merely the best available anchor — it is a **finer**
anchor than this repository's best line can currently resolve against.

**Report-only flag, for a follow-up leg that owns the file — NOT edited here.** `capabilities.py`
line 51 reads *"the Scenario-2 contraction ratio reproduces CHL's −2.5114 to ~1%"*, while line 304
records the bordered line reaching *"−2.5407 extrapolating to CHL's −2.5114 at 2.1e−04"*. Both are
true of their own modules, and the `~1%` is honest **for the relaxation line**. But the annotation
is easy to read as "this repository's best agreement with CHL is 1%", and that reading is wrong by
**a factor of ~42**. The measured magnitudes are in §5 of `experiments/journal/leg_78.md`. The
correction belongs to whichever leg owns `capabilities.py`; this leg did not touch it.

**Not a bug report.** Nothing disagrees. The two numbers are two different objects — a relaxation
that floors at residual ~1e−2, and a Newton solve extrapolated in reach — and they bracket CHL's
value from the same side at two different accuracies.
