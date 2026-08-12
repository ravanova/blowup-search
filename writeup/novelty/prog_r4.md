# PROG-R4 (leg 380) — U0: the ONE programme-level novelty / prior-art pass

**Committed BEFORE any construction**, per `ORCHESTRATION.md` §3c rule 3 and the §0a
novelty-pass calibration. This is the **programme-level** pass: it is run once, at programme
start, in full, and it **binds the whole programme**. There are no per-unit novelty asks.
A later unit that makes a novelty *claim* still runs its own pass (§3c rule 3).

**Scope of this pass, as dispatched:** *spec-compliant hookstep RPO recovery plus
basin-radius measurement on the named seeds* — i.e. (i) recovering published relative
periodic orbits of 2-D Kolmogorov flow with a genuine Newton–GMRES–hookstep at the scale the
question is posed at, and (ii) measuring the radius of the Newton basin around the recovered
orbit. Units U1–U4 all sit inside this scope.

---

## 1. The named seed, carried verbatim, and re-screened

The programme's seed is named per the `plan_of_record.py` Ban-2 **SCOPE ruling of 2026-08-11**
(annotated at commit `bb00a0d`), which requires that *"Any leg claiming scope MUST NAME ITS
SEED in its own pre-registration: source, identifier, why not cheap-entrance construction."*
Carried verbatim from `DIRECTION.md` cycle-11a §4:

> **SOURCE:** Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV.
> **IDENTIFIERS:** the five published RPOs leg 353 pre-registered (including UPO37,
> shift `s=0.375`), as recorded in `writeup/data/p2_route_dsspb5_v1.json`.
> **WHY NOT A CHEAP-ENTRANCE CONSTRUCTION:** these orbits were obtained in the source by
> recurrent-flow analysis of turbulent DNS trajectories converged with hookstep-Newton — not
> by bifurcation off a fixed point of a rescaled flow, Hopf or otherwise; and the present
> search is INITIALISED from that published data, which is exactly the seeded shape the §1
> ruling places outside Ban 2's object.

### 1a. Re-screen against Ban 2 (the DSS EXPENSIVE-ENTRANCE ban)

Ban 2's object, in its own text, is a *"DSS EXPENSIVE GLOBAL periodic-orbit search [on the]
rescaled flow [with] no fixed point nearby [to] seed it"*, and the 2026-08-11 scope ruling
states that a **seeded** search — *"one initialised from a named, published orbit or
equivalently specified starting point"* — is outside the ban's object. Three checks:

1. **Is the seed named and published?** Yes: arXiv:1406.1820v2 Table IV, a refereed source
   (*Phys. Fluids* **27**, 045106 (2015)), rows identified by the paper's own labels.
2. **Is the search initialised from it?** Yes. Every U3 attempt is initialised at a
   near-recurrence candidate selected *against a named Table-IV row's published `(T, s, m)`*,
   which is the seeding relation leg 353 already implemented and this programme inherits.
3. **Is it a global unseeded trawl?** No. The attempt set is enumerated in advance and each
   member is tied to a named row. **If any unit of this programme ever finds itself without a
   named seed, Ban 2 applies in full, the programme STOPS, and the situation escalates.**

### 1b. Re-screen against Ban 1 (the DSS CHEAP-ENTRANCE ban), literal wording

Ban 1 bars *"any attempt [to] obtain [a] DSS orbit by BIFURCATION OFF A FIXED POINT [of the]
rescaled flow (Hopf or otherwise), inviscid or viscous."* Screened literally, step by step:
**no step of any unit of this programme continues a fixed point into an orbit.** U1's
laminar-fixed-point control is a *solver control* — Newton is started 1%-perturbed from the
laminar fixed point and converges *back to that fixed point*, which is a convergence test of
the globalisation layer, not a continuation of a fixed point into an orbit; no parameter is
continued, no branch is followed, and no orbit is produced from it. U3 initialises at
DNS-derived near-recurrences of a *turbulent* trajectory, which is the opposite entrance.
U4 perturbs an already-recovered orbit. This screen is re-applied per unit, not just here.

### 1c. One measured discrepancy in the seed's own wording, recorded not resolved

The spec says *"the five published RPOs leg 353 pre-registered."* Measured against
`writeup/data/p2_route_dsspb5_v1.json` and `experiments/p2_route_dsspb5_v1.py`:

- the runner's `TABLE_IV_TARGETS` pre-registers **eight** named Table-IV rows — UPO37
  (T=19.334, s=0.375), UPO35 (18.912, 5.576), UPO34 (18.878, 0.418), UPO32 (18.694, 0.434),
  UPO22 (17.160, 0.361), UPO20 (16.908, 0.553), UPO17 (16.753, 0.482), UPO9 (14.776, 0.295),
  all with m=0;
- the JSON's `newton_attempts` records **five attempts** spanning **four** distinct rows
  (UPO37 twice, UPO35, UPO9, UPO22).

So "the five published RPOs" matches the **five attempts**, not five distinct identifiers.
This programme does not re-scope the seed: it takes the seed pool to be the **eight named
Table-IV rows already pre-registered by leg 353 in the same JSON and the same source table**,
of which the five attempts are a subset. Every one is a named, published identifier from
arXiv:1406.1820v2 Table IV, so this is the same seed object under both readings, and it is
the reading G1's own wording requires (*"does at least one **named Table-IV RPO** recover"*).
UPO37 remains the primary named target, verbatim as specified.

---

## 2. Instrument check, and one measured instrument limitation

**MF-discipline: no absence claim below is trusted unless this section's controls produced
it.** Three separate instrument facts were measured this session, and the third one is
load-bearing for how every zero in §3 must be read.

### 2a. The arXiv API endpoint was DOWN for this pass (HTTP 429), measured twice

`https://export.arxiv.org/api/query` — the endpoint leg 353's pass used — returned **HTTP 200**
on a single probe at the start of this session (`all:test` → 2 entries) and then returned
**HTTP 429 Too Many Requests** for every subsequent query, persistently, through five rounds
of exponential backoff (12s → 192s). The 429 was then reproduced **from a completely
independent network path** (a different fetcher, different IP), so it is arXiv-side
throttling of the API endpoint, not this host's connectivity. **A zero from that endpoint this
session would have been an artifact.** No result below is taken from it.

### 2b. Fallback instrument, controlled before use

All queries in §3 were run against the **`arxiv.org/search/` web index** (`searchtype=all`).
Four positive controls, all non-empty, run before any zero was trusted:

| control query | n |
|---|---|
| `"Kolmogorov flow"` | 173 |
| `"relative periodic orbit"` | 46 |
| `hookstep` | 7 |
| `"basin of attraction" Newton` | 45 |

The index is current (top hits dated 2026-08), so it is not a stale mirror.

### 2c. MEASURED LIMITATION — this index is abstract/metadata-level, NOT full text

This was measured, by counterexample, not assumed. The query `all:hookstep` returns **exactly
7 papers**: 2603.26382, 2411.05499, 2408.05079, 2306.00165, 1706.05312, 1012.5836, 0809.1498.
**Neither arXiv:1207.4682 (Chandler & Kerswell 2013) nor arXiv:1406.1820 (Lucas & Kerswell
2015) is in that list — and both of them use Newton–GMRES–hookstep as their central method.**
Independently, `"Kolmogorov flow" "Newton-GMRES-hookstep"` returns **0** while 1406.1820 is
literally a Newton–GMRES–hookstep study of Kolmogorov flow.

**Consequence, applied throughout §3:** a zero from this instrument is evidence of absence
**from titles and abstracts only**. It is NOT evidence that no paper's *body* contains the
measurement. This is why the verdict in §4 does not rest on the zeros alone: the nearest
neighbour was additionally read **in full text** (§3b), which is the check the zeros cannot
perform. An MF1 spelling-variant check (`"hook step"` spaced → 0) is recorded for
completeness but inherits the same limitation and carries little weight.

---

## 3. The pass

### 3a. Query table (identifiers banked, not counts — MF2)

| query (`arxiv.org/search`, `searchtype=all`) | n | hits that matter |
|---|---|---|
| `"Kolmogorov flow" "relative periodic orbit"` | 3 | [2601.21970](https://arxiv.org/abs/2601.21970) Zhigunov & Page, ECS as building blocks on large domains; [2502.06475](https://arxiv.org/abs/2502.06475) Cleary & Page, dynamical relevance of POs vs Re; [2210.16708](https://arxiv.org/abs/2210.16708) Pérez De Jesús & Graham, data-driven low-dim model |
| `"recurrent flow analysis"` | 4 | [2408.05079](https://arxiv.org/abs/2408.05079); [1906.01310](https://arxiv.org/abs/1906.01310) DMD-based PO search; [1706.02536](https://arxiv.org/abs/1706.02536); **[1406.1820](https://arxiv.org/abs/1406.1820) — the seed source** |
| `hookstep` | 7 | [2306.00165](https://arxiv.org/abs/2306.00165); [2408.05079](https://arxiv.org/abs/2408.05079); [2603.26382](https://arxiv.org/abs/2603.26382); [2411.05499](https://arxiv.org/abs/2411.05499); [1706.05312](https://arxiv.org/abs/1706.05312); [0809.1498](https://arxiv.org/abs/0809.1498); [1012.5836](https://arxiv.org/abs/1012.5836) |
| `"Kolmogorov flow" "periodic orbit" Newton` | 1 | **[2108.12219](https://arxiv.org/abs/2108.12219) Parker & Schneider — the nearest neighbour, see §3b** |
| `"Kolmogorov flow" "Newton" "convergence" "initial guess"` | 1 | 2108.12219 again |
| `"invariant solutions" "initial guess" convergence shear flow` | 1 | [2306.00165](https://arxiv.org/abs/2306.00165) Ashtari & Schneider |
| `"Lucas" "Kerswell" "Kolmogorov"` | 2 | 1406.1820 (seed source) and [1308.3356](https://arxiv.org/abs/1308.3356) (its DNS companion) |
| `"convergence basin" Newton periodic orbit` | **0** | control: `"convergence basin"` alone → 24, non-empty |
| `"periodic orbit" "basin of attraction" Newton turbulence` | **0** | components controlled non-empty above |
| `"periodic orbit" "success rate" Newton turbulence` | **0** | — |
| `"convergence radius" "periodic orbit" Navier-Stokes` | **0** | — |
| `"fractal" "basin" "Newton" "periodic orbits" fluid` | **0** | — |
| `"Kolmogorov flow" "Newton-GMRES-hookstep"` | **0** | **known-false zero** — see §2c, this is the counterexample |
| `"hook step" Newton flow` (MF1 variant) | **0** | inherits §2c's limitation |
| `"self-similar" "periodic orbit" "Navier-Stokes" blow-up` | **0** | scope check: nothing pre-empts the route-4 framing |

### 3b. The nearest neighbour, read in FULL TEXT — and exactly how close it gets

**arXiv:2108.12219 — Parker & Schneider, "Variational methods for finding periodic orbits in
the incompressible Navier–Stokes equations", *J. Fluid Mech.* (2022), doi:10.1017/jfm.2022.299.**
Same flow (2-D Kolmogorov), and it explicitly benchmarks against *"existing Newton
iteration-based shooting methods"*. This is the closest published work to U4's measurement and
it is named here rather than discovered later. Read via the full-text HTML rendering:

- **§4, Figure 4 — the perturbation sweep exists, and Newton is NOT in it.** They interpolate
  between a known orbit and a recurrence-derived candidate,
  `u_initial = (1-γ)·u_solution + γ·u_candidate`, with `γ=0` the exact orbit, `γ=1` the
  candidate, and `γ>1` extrapolating *past* the candidate; they plot final residual and final
  period `T` against `γ`. **This sweep is run only on the three variational formulations
  (PV, PV-LP, SV). Newton is absent from that figure.**
- **§4.1 — the Newton comparison is anecdotal, on two candidates.** Newton *"does not
  converge"* on the first; on the second it lands on *"a simple travelling wave solution
  ('T1')"* instead of the target RPO.
- **Figure 5 — a guess-quality proxy, but the abscissa is iteration count, not distance.**
  Newton is started from a halted PV run; measured are the Newton residual and the iterations
  Newton needs *"for convergence to a residual of 10⁻⁵"*, against PV iteration number.
- **Table 1 (§4.2) — aggregate counts only.** From 106 recurrence candidates: 57 (PV),
  55 (PV-LP), 36 (SN) converged, 14 / 9 / 6 unique solutions, threshold residual `< 1e-8`,
  each attempt capped at 72 h.

**The gap this leaves, stated precisely:** there is **no controlled plot or table of
Newton(-hookstep) success versus perturbation magnitude about a known orbit** in this paper.
The γ-sweep — the one experiment with the right shape — is run on the variational side only.
The "larger basin" claim for the variational methods is supported by counts and by that
one-sided sweep, never by a measured Newton radius.

**arXiv:2306.00165 — Ashtari & Schneider (2023), plane Couette, adjoint-based variational.**
Reports that the method *"outperforms Newton(-hookstep) iterations in successfully converging
from poor initial guesses"*, and the abstract's own hedge is *"suggesting a larger convergence
radius."* **"Suggesting" is the operative word: no metric, threshold, or measured extent is
given, and the guesses are described only as "extracted from a turbulent time series" — they
are not parameterised by distance from a reference solution.** Different flow (3-D plane
Couette, not 2-D Kolmogorov), so it does not touch the seed set either.

**arXiv:2408.05079 — Page et al., recurrent flows from 2-D turbulence via a nonlinear
recurrence function.** Uses *"a standard Newton-GMRES-hookstep method"* and reports greater
*diversity* of recovered orbits than previous recurrent-flow analyses. **No success-rate
percentages and no basin measurement** in the abstract; the contribution is the recurrence
*diagnostic* (nonlinear triads, with continuous-symmetry reduction built in), which is a
different object from a convergence-basin radius. Worth flagging as a *method* neighbour for
U2's recurrence-candidate extraction, not as a pre-emption of U4.

### 3c. One thing the literature says that bears directly on G2's pre-committed branches

Parker & Schneider's own text describes *"the complex, fractal regions of convergence"* for
this problem class, and records cases where Newton succeeded where the variational methods
did not. **This is recorded HERE, before any measurement, because it makes G2's `no` branch a
live and literature-anticipated outcome rather than a defect to tune away.** G2 asks whether a
radius is measured *with a coherent (monotone) failure boundary*; a published qualitative
expectation of fractal convergence regions is exactly the reason that gate was written with
two real branches, and the programme will not treat an incoherent boundary as a bug. No
number is imported from that sentence — it is qualitative, and it is not this repository's
measurement.

---

## 4. Verdict

**`PROCEED`** — with three named neighbours carried forward, not a clean field.

1. **U4's measurement (the Newton-hookstep basin radius about a published 2-D Kolmogorov-flow
   RPO, as a swept function of perturbation magnitude) is not published.** The nearest work
   (2108.12219) runs the correctly-shaped sweep on *variational* solvers with Newton absent
   from it, and its Newton comparison is anecdotal (two candidates) plus aggregate counts.
   The second-nearest (2306.00165) says only *"suggesting a larger convergence radius"*, on a
   different flow, with no metric.
2. **U1–U3 are reproduction, and are not claimed as novel.** A genuine Newton–GMRES–hookstep
   is Viswanath 2007 (arXiv:physics/0604062) and Chandler & Kerswell 2013 (arXiv:1207.4682);
   T=1e5 DNS with recurrence extraction at Re=60, n=4 is Chandler & Kerswell's own Series-A/B
   protocol. **This programme re-implements known method on a known object at the scale the
   source poses it, and its U1/U2 units are declared MILESTONES precisely because they make no
   claim.** The only thing U3 claims is *this realization's own* success/failure count against
   the sources' published rates — which is a measurement of this repository's apparatus, not a
   novel result about Kolmogorov flow.
3. **Correction to the prior pass, recorded rather than buried.** Leg 353's novelty pass
   (`writeup/novelty/leg_353.md`) concluded *"no paper on arXiv measures the radius of the
   Newton basin"* and did not surface 2108.12219 or 2306.00165, whose abstracts do not contain
   the word "basin" — its `abs:"...basin..."` queries could not have found them. That verdict
   **survives** (neither paper measures the radius), but it was reached on thinner evidence
   than it appeared, and the two neighbours are named here so no later unit of this programme
   can present the field as emptier than it is.

**Ceiling unchanged: TIER 2.** `CLAY_OBLIGATIONS.md` §6's two no-method obligations —
(i) certified far-field decay + admissible cutoff, (ii) persistence/stability under
localisation — are **OPEN** and this pass relaxes neither. **§4 is OPEN and NOT discharged**
(user ruling, 2026-08-12; see the pre-registration `experiments/journal/prog_r4_prereg.md` §3
for the amendment's full text and reasoning). Nothing in this pass moves any link of the
`L1 → L4` chain; **Clay stays ~0.05%.**

---

*Sources pinned for the programme's construction sections:* arXiv:1406.1820v2 (seed source,
Table IV), arXiv:1207.4682 (recurrence + Newton–GMRES–hookstep protocol, and the 4.3% = 7/163
nonzero-shift RPO success rate G1's resourcing argument uses), arXiv:physics/0604062
(Viswanath 2007, the hookstep's origin and the diagnosis that plain/damped Newton steps are
ineffective on this problem class), arXiv:2108.12219 and arXiv:2306.00165 (nearest neighbours
to U4), arXiv:2408.05079 (method neighbour for U2's extraction).
