# TECHNICAL — Route-P0TCV v1 (leg 300): independent verification of leg 266's GATE-YES correction

**Gate answer: NO**, on clause (c), on one of five magnitudes. Clauses (a) and (b) pass in
full. Every number below is in `writeup/data/p2_route_p0tcv_v1_verify.json` and is
re-asserted from that JSON by `experiments/p2_route_p0tcv_v1_verify_evidence.py` (29/29).

---

## 1. The object under verification

`leg/266-p0tc-v1`, commit `873a15f`, whose parent `bef1d5e` is leg 251's escalated tip.
Leg 266 re-posed leg 251's certificate obligation #1 per `writeup/novelty/verify_251.md`
§C and reported GATE YES in a session that terminated before any paired verification ran.
`writeup/novelty/verify_266.md` does not exist. Leg 275 (`2aac47a`) is stacked directly on
`873a15f`, so `leg/251-p0t-v1`'s tip currently rests on an unverified rework.

Neither `bef1d5e` nor `873a15f` is an ancestor of `origin/main`: leg 251's packet is
parked in its entirety and this leg does not change that.

## 2. The pre-committed gate (quoted from the leg's dispatch)

> Does an independent line-by-line verification of `leg/266-p0tc-v1` confirm (a) the
> re-posed obligation matches the papers' actual architecture exactly as
> `writeup/novelty/verify_251.md` states it (F_dis as non-autonomous forcing on the Euler
> profile system; the enclosure obligation living in the stability step's r-restriction
> argument), (b) every verifier-confirmed claim in 251's report is byte-untouched on the
> branch, and (c) the window endpoints (1.1666667, 1.1909830) and the 6.855x width ratio
> re-derive from BCG's own stated inequalities, at the quoted precision?

## 3. Provenance — nothing inherited

BCG `arXiv:2208.09445` re-downloaded from `arxiv.org/e-print` into a **leg-private**
scratch directory (leg 265 recorded a provenance defect caused by a *shared* scratchpad;
that lesson is honoured here).

| | |
|---|---|
| tarball md5 | `45ea63c45a1a199ecfb4dc4a15431600` — **matches the pin** |
| tarball bytes | `1520724` |
| TeX file | `RadialImplosion31_FinalArxiv.tex`, **6898** lines (leg 266 claimed 6898) |
| independent downloads now agreeing | **4** (verify_251, leg 266, verify_265, leg 300) |

The git blobs are read from the object store via `git show`, not from any leg's prose.

## 4. Clause (a) — architecture. **PASS, 3/3 sub-claims, 10/10 locators**

| line | what is literally on it | confirmed |
|---|---|---|
| 180 | `\alpha=\frac{\gamma-1}{2}` — so `α = 0.2` at `γ = 7/5` | yes |
| 217 | Thm 1.2 (`th:mainr3`): smooth solution to `(eq:DS)`, `γ=7/5`, odd `n` large enough | yes |
| 220 | Thm 1.3 (`th:stability`): *"Let `(U^E, S^E)` be the profiles of Theorem 1.2, **solving** `(eq:DS)`"* | yes |
| 353 | `(eq:rstar)`, the standing restriction `1 < r < r*(γ)` | yes |
| 489 | *"The last term can be treated as an error so long as"* — the conditional | yes |
| 493 | `(eq:r:restriction)`: `r > 2γ/(γ+1)` | yes |
| 2085 | BCG §7's opening: *"in the Navier-Stokes case we need to restrict the parameter `r` to a regime where the self-similar profile dominates the dissipation"* | yes |
| 2130 | `\mc F_{\rm dis} =` — `F_dis` **defined**, in the dynamically rescaled system | yes |
| 2138 | `=\mc F_{\rm dis}+\mc F_{\mathrm{nl},\widetilde W}` — `F_dis` on the **RHS** | yes |
| 2142 | the paper's own words: *"the dissipative forcing"* | yes |

The three sub-claims of the re-posed obligation, each tied to confirmed lines:

1. the stationary system Thms 1.2/1.3 rest on is the **Euler** one (l.217, l.220) — **confirmed**;
2. dissipation enters **only** the dynamically rescaled system, as the non-autonomous
   forcing `F_dis` (l.2130, l.2138, l.2142) — **confirmed**;
3. the enclosure obligation therefore lives in the **stability step's** `r`-restriction
   argument: BCG treat `F_dis` as an error only when `δ_dis > 0` (l.180, l.489, l.493) and
   say so in §7 (l.2085) — **confirmed**.

Target window non-empty: **yes** (`w_tgt = 1/6 > 0`). Clause (a) **passes**.

## 5. Clause (b) — byte-untouchedness. **PASS, 29/29**

`git diff bef1d5e 873a15f`: **5 files, 9 hunks** — leg 266's own accounting of "3 files of
leg 251's, 7 hunks" plus its two new files at 1 hunk each, which reconciles exactly.

- `experiments/journal/leg_251.md` (3 hunks: obligation 1; the correction note; the §8 restatement)
- `experiments/p2_route_p0t_v1_targetselection.py` (2 hunks)
- `writeup/data/p2_route_p0t_v1_targetselection.json` (2 hunks)
- `experiments/journal/leg_266.md`, `writeup/novelty/leg_266.md` (new)

**0** paths outside leg 266's declared territory. **0** of the five integration-owned
shared ledgers touched; `plan_of_record.py` not in the diff.

A recursive structural diff of the curated JSON finds the changed paths to be **exactly**
the two leg 266 declared — `certificate_obligation.certificate_must_show.0` and the new
`certificate_obligation.CORRECTION_2026_08_07`. **Zero** undeclared paths changed.

All **29** enumerated verifier-confirmed claims are byte-identical: `gate_answer`,
`verdict`, `escalate`, `escalation_reason`, `named_phase1_candidate` (+ companion),
`fluid_or_vortex_dynamics_adjacent`, both screen authorities, `candidates`, `counts`,
both survivor lists, the certificate-obligation preamble trio, **obligations 2, 3, 4 and
5**, `what_a_certificate_would_NOT_show`, `wall2_position`, `conditionality`,
`rss_blockers`, `dss_ban_state_read_from_plan`, `self_test`, `negative_control`,
`honesty`, `clay`. Clause (b) **passes**.

## 6. Clause (c) — the magnitudes. **FAIL, 4/5**

Formulas hand-transcribed from the TeX, evaluated at `Decimal` precision 60, never copied
from leg 266's arithmetic:

```
(eq:rstar), branch 1 < γ < 5/3, l.353–358:
    r*(γ) = 2 / (√2·√(1/(γ−1)) + 1)² + 1
(eq:delta:dis), l.489–491:   −δ_dis = 2 − r + (1/α)(1−r) < 0,  α = (γ−1)/2  (l.180)
(eq:r:restriction), l.493–495, equivalently:   r > 2γ/(γ+1)
```

Two independent routes to the lower edge agree exactly: `2γ/(γ+1)` and, from
`δ_dis(r) = 0`, `r = (2α+1)/(α+1)`. And `r*` matches its closed form `(7−√5)/4`.

| quantity | claimed by 266 | re-derived (60 digits) | at claimed precision | rel. error |
|---|---|---|---|---|
| dominance lower edge | `1.1666667` | `1.1666666666666666666666` | `1.1666667` | `2.857e-08` ✓ |
| dominance upper edge | `1.1909830` | `1.1909830056250525758977` | `1.1909830` | `4.723e-09` ✓ |
| dominance width | `0.0243163` | `0.0243163389583859092310` | `0.0243163` | `1.602e-06` ✓ |
| target width | `0.1666667` | `0.1666666666666666666666` | `0.1666667` | `2.000e-07` ✓ |
| **width ratio** | **`6.855`** | **`6.8541019662496845446137`** | **`6.854`** | **`1.310e-04` ✗** |

Closed forms, neither previously written down in this repository:

```
dominance width = r* − 7/6 = (7 − 3√5)/12 = 0.0243163389583859…
width ratio     = (1/6)/(r* − 7/6) = 2/(7 − 3√5) = (7 + 3√5)/2 = 6.8541019662496845…
```

**Absolute error `0.00090`; relative error `1.310e-04`, i.e. 0.0131%.** Clause (c) **fails**.

### 6.1 Localising the defect

The discriminator is whether the *formula* or only the *transcription* is wrong. Feeding
the comparator leg 266's **own** rounded endpoints (`1.1666667`, `1.1909830`) and
re-dividing gives `6.8541143…`, which rounds to **`6.854`** — the same 4-s.f. value the
60-digit derivation gives, and not the value leg 266 wrote. `formula_is_sound = True`.

**Conclusion: a slipped final digit, not a misread of the papers.** Nothing downstream
depends on the ratio's fourth digit — the re-posed obligation, the `r ≤ 7/6` coverage
requirement, and leg 275's `r^(3)` re-naming all rest on the *endpoints*, which reproduce
exactly. The ratio is a rhetorical magnitude establishing that the target window is
comfortably non-empty; it is, by `6.854×`.

### 6.2 Propagation surfaces

A search over `origin/main` and both branch tips (`*.md`, `*.py`, `*.json`) returns
**8** surfaces, all restatements of the one computation, **7 of them on `main`**:

| surface | on `main`? | inside leg 300's territory? |
|---|---|---|
| `experiments/journal/leg_266.md:70` — **the source** | no (branch only) | yes |
| `experiments/JOURNAL.md:3730` | **yes** | **no** — integration-owned ledger |
| `DIRECTION.md:11156` — the DM's record of 266 landing | **yes** | **no** — DM-owned |
| `DIRECTION.md:13289` — the user-facing packet summary | **yes** | **no** |
| `DIRECTION.md:13328`, `:13336` — **leg 300's own dispatched gate text** | **yes** | **no** |
| `DIRECTION.md:13474`, `:13479` — **reserve leg 305 (Route-DWM)**, whose *title* reads *"IS THE 6.855x DOMINANCE-WINDOW DEFICIT SHARP OR SLACK?"* | **yes** | **no** |

Two of these deserve separate comment.

- `:13328`/`:13336` are this leg's own gate, which *quotes* `6.855` as the claim under
  test. That is correct as written and must **not** be edited: a pre-committed gate is a
  historical record of what was asked, not a live magnitude.
- `:13474`/`:13479` are the more consequential ones. Reserve leg 305 is a **drafted,
  queued** leg whose title and thesis are both built on the wrong digit. Its own gate
  ("does the re-derivation reproduce the window endpoints…") is unaffected — the endpoints
  are exact — but its framing needs the corrected figure before it dispatches.

Every one of the seven `main`-side surfaces is outside this leg's territory, which is why
the gate's no-branch prescribes a rework leg rather than an in-place fix here.

## 7. Negative controls (lesson 90). **5/5 behaved**

| control | planted defect | required | result |
|---|---|---|---|
| `locator_off_by_one` | look for `F_dis`'s definition at l.2131 instead of l.2130 | caught | caught |
| `byte_identity_planted_edit_to_obligation_2` | append `" [PLANTED DEFECT]"` to `certificate_must_show[1]` on the tip blob | caught, and clause (b) flipped to FAIL | caught |
| `silent_gate_answer_flip` | flip `gate_answer` YES→NO on the tip blob | flagged as an **undeclared** change | caught |
| `wrong_eq_rstar_branch` | evaluate the `γ ≥ 5/3` branch of `(eq:rstar)` at `γ = 7/5` (gives `1.1883…`) | must **not** reproduce `1.1909830` | caught |
| `comparator_accepts_the_true_ratio` | feed the comparator the correct ratio | must **pass** — a comparator that rejects everything is not a comparator | passed |

The third and fourth are the ones that can genuinely embarrass the run: they establish
that the byte-identity auditor would have caught a silent claim change, and that the
window derivation is branch-sensitive rather than fitted to the expected answer.

## 8. The gate's no-branch, executed

> no → Name the failing clause and magnitude; cut a rework leg at top of queue (same
> territory, gate pre-committed to the corrected reading); 266 stays unmerged.

**Failing clause:** (c). **Failing magnitude:** the width ratio, claimed `6.855`,
re-derives `6.8541019662496845446` `= (7 + 3√5)/2`, i.e. `6.854` at the quoted precision;
absolute error `0.00090`, relative `1.310e-04`.

**266 stays unmerged.** No merge of `873a15f` to `main` was attempted, and leg 251's
parked packet is untouched — this leg pushes only its own artifacts.

**Rework leg, drafted for the DM to place** (this leg may not write `DIRECTION.md`); the
full spec is in `experiments/journal/leg_300.md` §7. In one line: same territory as 266
plus the two `main`-side surfaces, gate pre-committed to *"does every surface carrying the
width ratio read `6.854`, and does the closed form `(7 + 3√5)/2` appear beside it?"*

## 9. Scope — what this leg deliberately did not do

- It did **not** re-verify leg 251's screen (`verify_251.md` did that at source).
- It did **not** reopen the named candidate, the compressible-vs-Clay flag, Wall 2, the
  Leray-projector finding, the CONDITIONAL tier, or the Clay odds.
- It did **not** touch, comment on, or re-raise the Phase-1 packet parked with the user.
- It did **not** verify leg 275, a separate correction stacked on top of 266 that carries
  its own unverified status. That is a distinct, still-open gap.

## 10. Clay

No link of the L1→L4 chain moved. This leg verifies the wording and arithmetic of a
certificate obligation for a **compressible** Navier–Stokes target; compressible NS is not
the incompressible system the Clay problem asks about, and verifying a correction is
hygiene, not progress. Clay odds stay **~0.05%**.
