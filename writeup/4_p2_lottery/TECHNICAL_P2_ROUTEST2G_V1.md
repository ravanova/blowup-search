# TECHNICAL — Route-ST2G v1: the DSSP screen's report path learns Tsai Theorem 2 and the SS/DSS ansatz check

**Leg 383, construction class, floor-eligible.** Repairs leg 359's flagged gap
(`a048de7`) in leg 357's B7 screen (`3f614d7`), at the layer legs 362/370 left open.

| | |
|---|---|
| Instrument | `solver/dssp_screen.py` — `screen_candidate()` rewired; no other function edited |
| Battery | `test_dssp_screen_t2.py`, **8/8** (6 pre-registered controls + regression + both-directions meta-check) |
| Pre-existing battery | `test_dssp_screen.py`, **23/23**, unchanged and still passing |
| Runner | `experiments/p2_route_st2g_v1.py` |
| Curated data | `writeup/data/p2_route_st2g_v1.json` |
| Evidence / figure | `experiments/p2_route_st2g_v1_evidence.py` → **fig102**, registered in `writeup/build_figures.py` |
| Novelty pass + pre-registration | `writeup/novelty/leg_383.md`, committed at `1ca4ce5` **BEFORE construction** |
| Journal | `experiments/journal/leg_383.md` |
| Read, edited nowhere | `solver/dssp_decay_enclosure.py` (leg 382) |
| Ceiling | **TIER 2.** No `L1 → L4` link moved. Clay ~0.05%. |

---

## 1. The gate and its answer

> **Q.** Does the upgraded screen classify (i) Tsai's own headline example as REACHED by
> Theorem 2 (the source's decay exponent matching this repo's measured one, per 359),
> and (ii) this programme's DSS object as NOT REACHED with the deciding clause recorded
> as the exact-SS ansatz hypothesis — with planted controls able to fail in both
> directions?

**Answer: YES.** All six pre-registered controls pass in their pre-registered directions;
no control was widened, relaxed, or re-scoped after the numbers arrived.

The yes-branch consequence, in the gate's own words: *the screen stops under-warning;
every future candidate report carries the two new columns.* **CEILING: TIER 2 — surviving
a screen is not evidence for existence.**

## 2. What was already built, and is not rebuilt here

The novelty pass (§1 of `writeup/novelty/leg_383.md`) found the dispatch thesis
**partially discharged** after leg 359 wrote its flag:

| commit | leg | added |
|---|---|---|
| `3f614d7` | 357 | `ledger_nrs_tsai()` — binary EXCLUDED / NOT EXCLUDED, L³-convergence only |
| `ec48622` | 362 | `decays_to_zero_at_infinity()`, `classify_ss_ansatz()`, `_ledger_nrs_tsai_three_way()` — **opt-in** |
| `3bfe677` | 366 | q=3 row re-attributed to NRS 1996, not Tsai Thm 1 |
| `9a3dd41` | 370 | `morrey_ball_average_sweep()`, `ledger_morrey()` — also **opt-in** |

None of that mathematics is re-derived and none of those functions are rewritten. Tsai
1998 is not re-fetched: leg 359 downloaded and hashed it (sha256 `6d3182d5…`) and leg 362
transcribed the load-bearing clauses verbatim into the module header. This leg quotes
those banked clauses and adds no new citation.

## 3. The gap that was still open

Both extensions were landed as strictly opt-in parameters defaulting to `None`,
deliberately, so that no existing call site's return-dict key set moved. The
per-candidate **report path** was never rewired. On `main` at `104f5b3`,
`solver/dssp_screen.py`:

```python
    decay = fitted_far_field_decay_exponent(field_fn)      # computed ...
    ...
    ledger = machine_read_ledger(l3, lam)                  # ... then dropped
```

`screen_candidate()` computed the decay exponent, discarded it, and never computed the
ansatz classification at all. `grep -rn "machine_read_ledger("` across the repository
shows **every** caller using the two-argument form.

**Re-measured, not recalled.** The BEFORE column in the curated JSON is produced by
calling `machine_read_ledger(l3, lam)` with exactly those two positional arguments — the
literal pre-leg call — on the same measurements, in the same process. It is a
measurement of the old behaviour, not a recollection of it.

Measured baseline: the planted Tsai-headline field returns fitted exponent
`-1.0000000000000002`, L³ ladder `converged=False` with `rel_change_last_step = 0.1305`
against `rel_tol = 1e-4` (genuine log-divergence), and the report path said
**NOT EXCLUDED**.

## 4. The change

`screen_candidate()` now computes both columns unconditionally and returns them:

- `theorem2_decay_to_zero` ← `decays_to_zero_at_infinity(decay)`
- `ss_ansatz` ← `classify_ss_ansatz(lam)`

and passes both into `machine_read_ledger(...)`, which routes to leg 362's three-way
reading. **`machine_read_ledger()`'s signature and defaults are untouched**, so leg 357's
two-argument shape and leg 370's opt-in `Morrey` key both still hold for direct callers
(regression control R below). `screen_candidate()`'s *ledger* key set is likewise
unmoved — `{NRS_Tsai, Chae_Tsai, Pineau_Vicol, reportable}` — which is what leg 357's own
landed test asserts, and it still passes untouched. Morrey stays opt-in: it is a
separate, far more expensive ball-average pass, and wiring it into every report was not
this gate's question.

## 5. The six pre-registered controls

Fixed in `writeup/novelty/leg_383.md` at `1ca4ce5`, before construction. Three must fire;
**three must stay silent** — an instrument that can only fire is a tautology, and this
repository has been burned by exactly that (leg 340).

### Direction A — must fire

| id | planted object | required | measured | verdict before → after |
|---|---|---|---|---|
| **C1** | Tsai eq (1.5), `U = (y/\|y\|)/\|y\|` | EXCLUDED-BY-T2 | exponent `-1.0000000000000002`; L³ `converged=False`, `rel_change_last_step` 0.1305 | NOT EXCLUDED → **EXCLUDED-BY-T2** |
| **C2** | repo's DSS object: `field_uB` + periodic λ>1 trajectory | NOT-REACHED-BY-ANSATZ | λ = `2.691234472349262`, S₀ = 1.98 = 2·log λ; exponent `-0.997134373688964` | NOT EXCLUDED → **NOT-REACHED-BY-ANSATZ** |
| **C3** | planted exponent −2 field | EXCLUDED-BY-T1 | exponent `-2.0000000000000004`; L³ norm 3195.93, `rel_change_last_step` 0.0 | EXCLUDED (357 binary) → **EXCLUDED-BY-T1** |

C3 is the discrimination control: the field *also* decays to zero, so T2 would have fired
had T1 not been checked first. T1 and T2 are therefore distinguishable, not one flag
wearing two names.

### Direction B — must stay silent

| id | planted object | required | measured | verdict |
|---|---|---|---|---|
| **C4** | field rising to a NON-ZERO limit | NOT EXCLUDED | \|U\| runs 0.954545 → 0.999500; exponent `+0.008377` | **NOT EXCLUDED**, T2 unmet |
| **C5** | the C1 field, read through the ansatz column | ansatz EXACT-SS | `satisfies_theorem_ansatz = True`, `measured_lambda = None` | not deflected; adjudicated on decay |
| **C6** | field growing like \|y\| | NOT EXCLUDED | exponent `+1.0000000000000002` | **NOT EXCLUDED**, *no clause claimed* |

C4 is the anti-tautology control: if the T2 column fired on a field that does not tend
to zero, the column would be excluding everything and measuring nothing. C5 guards C2:
if the ansatz clause fired on any static candidate, C2's NOT-REACHED verdict would be
vacuous — the same classifier, on a λ>1 trajectory, goes the other way in the same
process (`DSS`, `satisfies=False`). C6 checks that no clause is claimed on a field no
theorem in the ledger reaches — `"deciding_clause" not in row` is asserted, not assumed.

### Regression control R

`machine_read_ledger(l3, lam)` with its two original positional arguments still returns
`{NRS_Tsai, Chae_Tsai, Pineau_Vicol, reportable}` with `NRS_Tsai` carrying exactly
`{excludes, verdict, reason}` — leg 357's binary shape, byte-for-byte. Legs 357/362/370's
banked JSON files are untouched.

### Both-directions meta-check

Asserted as a property of the battery rather than claimed in prose: all four verdicts —
`EXCLUDED-BY-T1`, `EXCLUDED-BY-T2`, `NOT-REACHED-BY-ANSATZ`, `NOT EXCLUDED` — are
reachable through `screen_candidate()` on planted inputs, with ≥2 firing and ≥2 silent.

## 6. The gate's clauses, decided on magnitudes

**Clause (i).** Tsai 1998's headline example (eq 1.5) has exact decay exponent **−1**.
The planted field fits to `-1.0000000000000002`, |diff| **2.22 × 10⁻¹⁶**. This
repository's own measured exponent on leg 351's Type-I Biot-Savart witness is
`-0.997134373688964`, |diff| vs the source **2.87 × 10⁻³** (leg 359 banked `-0.9971`;
re-measured here, agreeing to the banked precision). The source's exponent matches this
repo's measured one at that magnitude, which is the sense in which leg 359 said the old
screen would misclassify a *genuinely* self-similar candidate at this repository's own
decay rate: it would have said NOT EXCLUDED, and it did, until this leg.

**Clause (ii).** The DSS object reads **NOT-REACHED-BY-ANSATZ** at measured λ =
`2.691234472349262`, and the recorded `deciding_clause` is checked programmatically to
contain `(1.2)` and `EXACT` — i.e. Tsai 1998, eq (1.2), p.29–30: *both* Theorem 1 and
Theorem 2 are stated "If u is of the form (1.2)₁", Leray's exact (continuous) backward
self-similar ansatz. The object is *discretely* self-similar — a periodic-in-log-time
orbit, not a fixed point of the rescaled flow — so it fails the hypothesis of both
theorems regardless of decay or L^q status. The deciding clause is the ansatz, not a
decay clause and not an L³ clause; that is asserted, not narrated.

## 7. Scope call: leg 382's certified enclosure, deliberately not wired in

`solver/dssp_decay_enclosure.py` (leg 382, `104f5b3`) provides a certified,
interval-arithmetic far-field decay enclosure, and its own capability row states it "does
NOT replace dssp_screen's fitted column". It was read and **deliberately left out**, as
the dispatch permits and requires to be said explicitly:

1. this gate asks whether the screen **classifies** correctly, not how rigorous the
   exponent it classifies on is;
2. swapping the estimator mid-leg would move the numbers underneath the very controls
   pre-registered to test the classification, confounding the comparison;
3. the fitted column stays in place, unchanged, as instructed.

**Open clause left to a successor:** a second, *certified* Theorem-2 column driven by the
enclosure, recorded alongside the fitted one and never replacing it — the same
alongside-not-instead discipline leg 382 adopted for its own column.

## 8. What this does not claim

Not a proof, not a construction, not evidence for existence. A candidate that survives
this screen is only "not already excluded by a published theorem reachable on this
repository's record". `CLAY_OBLIGATIONS.md` §6's two no-method obligations remain **OPEN**
regardless of this gate's answer. No ban touched, no `plan_of_record.py` or
`DIRECTION.md` edit, no `L1 → L4` link moved. Clay odds unchanged, **~0.05%**.
