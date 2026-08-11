# TECHNICAL — Route-GAF v1 (leg 303): Grade-A/fluid cell freshness sweep, 2026-08-11

**Branch** `leg/303-gaf-v1`. **Role** LEG (novelty pass committed as LIT before construction).
**Claims no stage**; `plan_of_record.py` untouched.

| artefact | path |
|---|---|
| novelty log (pre-committed) | `writeup/novelty/leg_303.md` |
| runner | `experiments/p2_route_gaf_v1_sweep.py` |
| manual adjudications | `experiments/p2_route_gaf_v1_adjudications.py` |
| raw query log (all 35, with links) | `writeup/data/p2_route_gaf_v1_raw.json` |
| curated data | `writeup/data/p2_route_gaf_v1_sweep.json` |
| evidence script (18 checks) | `experiments/p2_route_gaf_v1_sweep_evidence.py` |
| figure | `writeup/figures/fig68_route_gaf_v1_cell.png` (fig68) |
| journal | `experiments/journal/leg_303.md` |

---

## 1. The operator being gated

The occupancy matrix is `solver/viscous_novelty.py::PRECEDENTS`, built by leg 174 and extended
append-only by leg 197. Its two axes, restated so the gate is falsifiable:

- **Grade** — *where the dissipative term sits relative to the object the computer encloses.*
  **Grade A**: the dissipation is a term of the equation inside the enclosure, at leading
  scaling order (`arXiv:2410.05480`, Dahne–Figueras: `eps` in the `(1 - i eps)` Laplacian of
  the certified CGL profile equation; ledger verdict `PRE_EMPTS`). **Grade B**: the enclosed
  object is the inviscid reduction and dissipation is recovered afterwards by domination
  (`arXiv:2208.09445`, Buckmaster–Cao-Labora–Gómez-Serrano: interval arithmetic on the first
  10 000 Taylor coefficient pairs of the profile solving the *inviscid* compressible Euler
  system (1.5); §7 restricts `r` to "a regime where the self-similar profile dominates the
  dissipation"; ledger verdict `EXCLUSION`, `grade: "B"`).
- **Model** — fluid transport model or not.

**Grade-A ∩ fluid was empty.** Phase 1's premise — *no certified viscous blow-up exists in any
model, in any dimension, today* — is precisely the assertion that it is still empty. Leg 174's
own gloss: empty **"for want of a target, not a method."**

## 2. Freshness deficit, dated from `git log` rather than remembered

| leg | closed (UTC) | scope |
|---|---|---|
| 174 (VBS) | 2026-08-06T14:22:38Z | last **broad** topical sweep; 12 queries banked in `SEARCH_LOG` |
| 242 (DFL2) | 2026-08-06T22:11:18Z | **author-scoped**: Dahne and Figueras listings only |
| 291 (HLR2) | 2026-08-07T05:24:39Z | **object-scoped**: `HL_S2_nonsymmetric` (inviscid) only |

`gap_days_since_last_broad_sweep` at run time (2026-08-11T15:29:35Z): **5.05 d** (banked in the JSON's `window` block).
Neither 242 nor 291 re-asks the cell question, so the premise had been carried on leg 174's
reading for that entire interval.

Leg 174's own recorded gap matters more than the elapsed time: **none of its 12 queries
mentions compressible / implosion / imploding**, which is how `arXiv:2208.09445` (a 2022 paper)
stayed out of the ledger until leg 197 transcribed it. This leg's hit condition is therefore
**new-to-ledger, not new-to-arXiv**.

## 3. Method

**35 queries, 5 channels**, every string committed verbatim in `writeup/novelty/leg_303.md` §3
before the first request:

| channel | n | what |
|---|---|---|
| C1 | 12 | leg 174's `SEARCH_LOG` re-run **verbatim**, counts compared to what it banked |
| C2 | 4 | the compressible/implosion axis leg 174 never asked |
| C3 | 7 | dissipation-inside-the-certificate machinery, model-agnostic (radii polynomial, Newton–Kantorovich, validated numerics, interval arithmetic, rigorous numerics) |
| C4 | 7 | fluid transport models by name × certification vocabulary |
| C5 | 5 | the NRS/Tsai screen boundary |

All via `export.arxiv.org/api/query`, `sortBy=submittedDate&sortOrder=descending`,
`max_results=60`, 3.1 s spacing. **68 distinct papers** returned; every query's full link set is
in the curated JSON's `query_log`, and the evidence script asserts
`len(links) == n` for all 35 rows.

**Availability is separated from emptiness.** The first pass returned **6/35 as
UNAVAILABLE** — three HTTP 429, one 503, two read timeouts — including the entire C4 model-name
axis and one of the two channels that later surfaced the hit. `--retry-unavailable` re-queried
those six at 25 s spacing; **final state 35/35 OK, 0 UNAVAILABLE**. Had the first pass been
banked, this leg would have reported a false null on C4.

**Screen then adjudicate, with the screen kept.** A regex screen over title+abstract computes
the four clauses mechanically and its verdict is retained in the JSON as `verdict_mechanical`;
manual adjudications live in a separate committed module and appear as
`overrides_mechanical`. **4 of the verdicts were overridden by hand**, each visible as an
override rather than as a quietly retuned regex.

## 4. The pre-committed hit rule

All four required, judged from title + abstract only (the depth this leg is scoped to):

| clause | content |
|---|---|
| a | computer-assisted / rigorous-numerics certificate |
| b | of a blow-up or singular self-similar profile |
| c | dissipative term **inside** the certified object |
| d | for a fluid transport model |

Three of four → `NEAR`, with the failing clause named. Fewer → `OFF`.

## 5. Result

### 5a. Leg 174's net replicates exactly

**0 of 12 counts grew**; every delta is 0. Two consequences, and they point opposite ways:

1. On leg 174's own instrument, nothing has changed.
2. `SEARCH_LOG` banks `(query, count)` and no links. Seven of the 12 returned non-zero,
   **10 links in total, none recorded**. So it is provable that leg 174's net *saw* the same
   result sets, and **not** recoverable *which* papers it read and rejected. This is method
   finding **MF2** in the JSON.

### 5b. The gate answers YES — one hit, new to the ledger

**[arXiv:2604.09949](https://arxiv.org/abs/2604.09949)** — *Stable Finite-Time Singularity
Formation for 3D Navier–Stokes via 5D-Lifted Axisymmetric Reductions*, Rishad Shahmurov,
math.AP, v1 2026-04-10T23:03:18Z, no comment field, no journal reference.

Clause-by-clause, from the abstract:

| clause | evidence |
|---|---|
| a | "a computer-assisted Newton–Kantorovich validation based on interval arithmetic" |
| b | "finite-time singularity formation"; "a stationary rescaled profile `Ω̄` satisfying a nonlinear elliptic fixed-point equation in an analytically weighted Hilbert space" |
| c | the enclosed object is the rescaled profile equation **of Navier–Stokes itself**, not of an inviscid reduction later dominated — the Grade-A distinction, and the clause no other entrant in this sweep meets |
| d | "the 3D incompressible Navier–Stokes equations on the periodic torus `T³`" |

Found by two channels: leg 174's own C1 query #12
(`abs:"self-similar" AND abs:"Navier-Stokes" AND abs:"computer-assisted"`) and the C4 query
`abs:"Navier-Stokes" AND abs:"computer-assisted proof" AND abs:"singularity"`.

The other mechanical HIT, `arXiv:2509.14185`, is **already** an `EXCLUSION` row in the ledger,
so it is not news.

### 5c. Claimed, not filled — and why this leg stops here

`cell_state` records `grade_A_fluid_occupants_before: 0`,
`grade_A_fluid_occupants_claimed_after: 1`, **`grade_A_fluid_occupants_ESTABLISHED_after: 0`**.

Occupancy cannot be established from an abstract, and the adversarial full-text read is
**reserve leg 309** by explicit dispatch. **Phase 1's premise is not recorded as broken by this
leg.** Four credibility flags are recorded at abstract level, as observations for leg 309 and
not as a verdict:

1. the abstract describes the manuscript as "organized **in the style of** a computer-assisted
   proof paper, with theorem statements, proof packages, and explicit validation constants" —
   a description of presentation, not of a completed verification;
2. single author, v1 only, no page-count comment, no journal reference, no visible uptake in
   the ~4 months since posting;
3. the claim as stated (stable finite-time singularity for 3D incompressible Navier–Stokes on
   `T³`) resolves the Clay problem in the negative, which sets the prior accordingly;
4. the "5D-lifted axisymmetric reduction" device is not one this ledger has seen used in a
   certified construction.

### 5d. Why every other candidate misses

34 near-misses recorded; 9 adjudicated by hand, splitting **5 on clause (a)** and **4 on clause
(c)** — the field's two failure modes:

- **(a) no certificate.** `1704.00560` (Guillod–Šverák, JMFM 25 (2023)) — "we calculate
  numerically", "if the behavior seen here numerically can be proved"; a mechanical HIT
  demoted. `2506.19243` (Wang–Liu–Li–Anandkumar–Hou, PINNs, cs.LG) — mechanical HIT demoted;
  its abstract's "when combined with rigorous computer-assisted proofs" is conditional.
  `2501.15701` — 3D compressible Navier–Stokes blow-up at `γ = 5/3` via self-similar
  compressible Euler profiles: structurally a **new Grade-B/fluid row**, purely analytic.
  `2307.03434` — finite-time blowup for hypodissipative Navier–Stokes model equations for
  `α < log 3 / (6 log 2) ≈ 0.264`: clause (c) holds in the strong sense, (a) does not; the
  closest the literature comes to the cell **from the analytic side**. `2509.10806` — fractional
  NSE via doubly stochastic Yule cascades, and the blow-up is for an associated scalar PDE.
- **(c) inviscid object.** `2607.15256` (2026-07-16, the most recent paper in the sweep) —
  analytic finite-rank corrections for singularly weighted estimates in the Chen–Hou 2D
  Boussinesq / 3D Euler CAP: method-side progress on exactly the machinery the cell needs,
  aimed at an inviscid target. `2511.22819` (Wang–Léger–Lai–Buckmaster) — machine-precision
  unstable singularities, successor to the already-banked `2509.14185`. `2509.12435`
  (Guo–Hadžić–Jang–Schrecker, 149 pp) — Larson–Penston collapse for isothermal Euler–Poisson,
  with "rigorous computer-assisted techniques in the intermediate regime": clause (d) holds on
  adjudication, (c) fails (no dissipation anywhere in Euler–Poisson); the **strongest new
  fluid-side computer-assisted entrant**, and still not Grade A. `2308.01528` — analytic exact
  self-similar Hou–Luo profiles, the inviscid object legs 54/55/57/291 already track.

### 5e. The NRS/Tsai screen boundary

**UNMOVED at the exclusion boundary.** Nečas–Růžička–Šverák plus Tsai exclude nontrivial
*backward* self-similar Leray solutions; five boundary-adjacent works were found and none
weakens that. The only one that moves the line, `1610.09464` (removing discretely self-similar
singularities), moves it **outward** — more excluded, screen stronger. `1704.00560` is
*forward* self-similar (Jia–Šverák non-uniqueness), which NRS/Tsai never covered; `2511.09556`
and `2604.07785` are Type-I-side; `2509.25116` is Leray–Hopf non-uniqueness, on which the
screen is silent.

## 6. Method findings, banked for the next sweep leg

- **MF1 — the LaTeX double hyphen is a systematic false-negative channel.** The single hit
  spells its model `Navier--Stokes` throughout. A regex or search string spelling it
  `Navier-Stokes` does not match it; the mechanical screen scored `c_dissipative` FALSE for
  that reason alone and only a hand override promoted it. Future sweeps must use a hyphen
  class (`Navier[-]{1,2}Stokes`) and must not treat a single spelling's zero as a zero.
- **MF2 — counts without links cost more than they save** (§5a): 10 of leg 174's links are
  unattributable, and the one paper at issue sits behind one of them.
- **MF3 — an UNAVAILABLE is not a zero** (§3): 6/35 first-pass failures, all recovered.

## 7. Landing decision, stated explicitly

The dispatch's yes-branch says: record the pointer(s); escalate **if a hit actually FILLS the
cell**. This leg lands to `main` normally rather than parking, for two stated reasons:

1. "Actually fills" cannot be established at abstract depth, and establishing it is leg 309's
   explicitly assigned job. What this leg banks is a **claim plus a route**, not an occupancy.
2. None of the four escalations (`ORCHESTRATION.md` §8) is triggered: no `plan_of_record.py`
   change, no ban lifted or weakened, no prose claiming movement on the Clay chain or odds
   better than ~0.05%, no banked result deleted or rewritten. Under §8's "everything short of
   these four is decided, not asked", this is decided.

**Leg 309 is now load-bearing and should be prioritised.** If its adversarial read holds the
claim up, Phase 1's premise falls — and *that* is the user's to weigh.

**Clay odds: unchanged at ~0.05%.** No link of the L1→L4 chain moved.

---
*Blog companion: [`BLOG_P2_ROUTEGAF_V1.md`](BLOG_P2_ROUTEGAF_V1.md).*
