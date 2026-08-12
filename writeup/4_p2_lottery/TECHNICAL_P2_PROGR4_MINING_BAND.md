# PROG-R4 U2 — MILESTONE M2, and the selection bias in globally-ranked recurrence mining

**Unit:** PROG-R4 U2 (leg 380), `ORCHESTRATION.md` §3c programme lane. Build unit, MILESTONE M2.
**No gate is answered here.** G1 is unit U3.
**Mode:** §3f SOLO. **UNVERIFIED** — built and checked in one session, no paired verifier.
**Data of record:** `experiments/programme_r4/u2_recurrence_library.json`,
`experiments/programme_r4/u2_dns_meta.json`.
**Pre-registration:** `experiments/journal/prog_r4_prereg.md`;
`experiments/journal/prog_r4_u2u3_prereg_addendum.md` §3d (AMENDMENT 4).

---

## 1. The DNS

2-D Kolmogorov flow, vorticity formulation, `N = 24` (578 real unknowns in the RPO extended
system), `Re = 60`, forcing wavenumber `n = 4`, `dt = 0.01`, `T_BURN = 500` discarded,
`dt_save = 0.25`, run to `T_TOTAL = 1e5`.

| quantity | measured |
|---|---|
| snapshots | 400,000 |
| wall | 3.44 h |
| per step | 1.2379 ms |
| `D / D_lam` | 0.0645 ± 0.0253 |

`D/D_lam` is a planted check on the trajectory, not a reported statistic: collapse onto the
laminar fixed point reads exactly `1.0` with zero variance. `0.0645` at 39% relative spread,
sustained over the full `1e5`, is the chaotic attractor. Without that, there is nothing to mine
and every number downstream would be about a fixed point.

**The `T = 1e5` figure is not a choice made here.** It is the pre-registered compliant scale, set
against Chandler & Kerswell 2013 (arXiv:1207.4682) and Lucas & Kerswell 2015 (arXiv:1406.1820v2),
both of which mine trajectories of this order. Leg 353's `T = 2000` with 5 attempts gives
`P(0 successes) = 0.59–0.77` under the sourced per-attempt rates; `T = 1e5` with 100 attempts
gives `1.2e-2` at Chandler & Kerswell's 4.3% and `3e-5` at Lucas & Kerswell's ~10%. That is the
difference between a null that means nothing and a null that fires §3d.

## 2. The recurrence measure and the lossless prefilter

The measure is Chandler & Kerswell eq. (23) in squared relative form, minimised over the
continuous streamwise shift `s ∈ [0, L_x)` and the discrete cross-stream shift `m`:

```
R(t, T) = min_{s, m}  ‖ σ_{s,m} Ω(t) − Ω(t−T) ‖²  /  ‖ Ω(t) ‖²
```

Evaluating that minimisation at each of `9.55e7` grid pairs is not affordable. It is also
unnecessary. Define

```
R_red(t, T) = Σ_k ( |Ω_k(t)| − |Ω_k(t−T)| )²  /  Σ_k |Ω_k(t)|²
```

**Claim (lossless prefilter): `R_red(t, T) ≤ R(t, T)` pointwise.**
Every symmetry in `σ_{s,m}` acts on each Fourier coefficient by multiplication by a
unit-modulus phase, so `|σ_{s,m} Ω|_k = |Ω_k|` for all `s, m`. Then, coefficientwise,
`|a − b| ≥ | |a| − |b| |`, and summing gives `‖σ_{s,m}Ω(t) − Ω(t−T)‖² ≥ Σ(|Ω_k(t)| −
|Ω_k(t−T)|)²` for **every** `(s, m)`, hence for the minimiser. Dividing by the common
normalisation gives the claim. ∎

Consequence: thresholding `R_red` at a value `θ` discards nothing that could have passed `R ≤ θ`.
The statement is banked verbatim in `prefilter.statement` in the library JSON, because everything
downstream rests on it.

Thresholds are the source papers': `R_thres_record = 0.30`, `R_thres_window = 0.25` (L&K's Newton
window), `T ∈ (0.5, 60.0)`.

## 3. Selection criterion: strict interior local minima

Candidates are **strict interior local minima of `R_red` in the `(t, T)` plane**, the criterion
used in both source papers, not a top-N by value.

This is load-bearing. Ranking by `R_red` value alone fills the budget with `T → T_min` cells,
where the trajectory has barely advanced and `R_red` is small for trivial reasons. Those cells sit
on the boundary of the `T` window, so the interior-minimum criterion excludes them **structurally**
rather than by a tuned cutoff. Recorded in `prefilter.selection`.

Scan result:

| quantity | value |
|---|---|
| pairs scanned | 95,542,640 |
| below `R_thres_record` | 31,244,629 |
| strict interior local minima | 913,301 |
| scan wall | 71.0 s |
| best `R` after full `(s, m)` minimisation | **0.016543** |

Leg 353's best over `T = 2000` was `R = 0.177` (UPO37). One order of magnitude, bought by length.

**MILESTONE M2 is ANSWERED.** It asserts the existence of the instrument and the data at the
pre-registered scale, nothing about orbit recovery.

## 4. The selection bias

913,301 local minima is an abundance. The seed funnel, counted end to end on the global top-400:

| stage | count | filter |
|---|---|---|
| passed to full `(s, m)` minimisation | 400 | `--max-candidates` |
| `R < 0.25` | 260 | L&K Newton window |
| `m = 0` | 102 | realization limit, §5 |
| `\|T − T_published\| ≤ 1.0` for some named row | **1** | anchor rule (Ban 2) |

One seed against a pre-registered 100.

### 4.1 Mechanism

Let `τ` be the recurrence interval. Two effects compound, both monotone in `τ`:

1. **Divergence.** On a chaotic attractor with leading Lyapunov exponent `λ ≈ 0.35` (measured on
   this attractor in the U3 control work), an initial separation `ε` grows as `ε e^{λτ}`. Over
   `τ = 19.33` that is an amplification of `8.73e2`; over `τ = 2` it is `2.01`. A genuine near-miss
   of a `T ≈ 19` orbit therefore *scores* two to three orders of magnitude worse than an
   incidental near-repeat at `τ = 2`, purely from the interval.
2. **Multiplicity.** The number of `(t, τ)` cells available at interval `τ` is
   `N_snap − τ/dt_save`, and more importantly the number of *distinct* near-repeat opportunities
   at small `τ` is far larger, because the trajectory passes near its own recent past constantly.

So the global order statistic on `R_red` is dominated by `τ ∈ [1.25, 2.5]`. The named orbits live
in `τ ∈ [14.776, 19.334]`. A global top-N spends its budget an order of magnitude below the band
of interest, and the starvation gets *worse* as the DNS gets longer, because longer runs supply
proportionally more short-interval cells.

This is not a defect in the ranking. `R_red` is a faithful similarity measure and the ranking
faithfully reports it. The failure is that the downstream filters (`m = 0`, anchoring) select on
properties the ranking has no knowledge of, so the ranking's output and the filters' acceptance
region are close to disjoint.

### 4.2 AMENDMENT 4 — stratified budget

Rule, from the addendum §3d: keep the global top-`max_candidates` **whole**, removing nothing, and
*additionally* take the best `per_anchor` strict local minima within `T_ANCHOR_TOL = 1.0` of each
of the eight named periods. Added candidates face the identical downstream tests: full `(s, m)`
minimisation, `R < R_thres_window`, `m = 0`, anchor rule.

```python
T_of_lag = (np.asarray(jj, dtype=np.float64) + 1 + lag_lo) * DT_SAVE
picked = {o: None for o in order[:args.max_candidates]}
for name, T_pub in TABLE_IV_PERIODS:
    band = np.abs(T_of_lag[order] - T_pub) <= T_ANCHOR_TOL
    take = [o for o, b in zip(order, band) if b][:args.per_anchor]
    for o in take:
        if o not in picked:
            picked[o] = None
            chosen.append(cell(o))
```

Realised:

| stage | global only | `per_anchor = 80` | `per_anchor = 500` |
|---|---|---|---|
| to full minimisation | 400 | 634 | 2014 |
| `R < 0.25` | 260 | 333 | 579 |
| `m = 0` | 102 | 131 | 234 |
| anchored | **1** | **30** | **133** |

`133 ≥ 100`, so U3 runs at the pre-registered attempt count.

**Sublinearity.** `8 × 500 = 4000` band takes deduplicate to 1614 added cells, because
`T_ANCHOR_TOL = 1.0` exceeds the spacing within two of the three named clusters
(`{16.753, 16.908, 17.160}` and `{18.694, 18.878, 18.912, 19.334}`), so the bands overlap heavily.
This is why `per_anchor = 80` was insufficient and why the growth from 30 to 133 is far below the
6.25× the parameter suggests.

**Per-anchor realised pool** (`m = 0`, in window, nearest-anchor assignment):
`UPO9 42, UPO32 21, UPO22 21, UPO37 20, UPO17 19, UPO20 6, UPO35 4, UPO34 0`.

`UPO34 = 0` is an artefact of nearest-anchor assignment, not of the flow: `T = 18.878` lies
between `18.912` and `18.694`, both within `T_ANCHOR_TOL`, so no candidate ever has UPO34 as its
*nearest* named row. Recorded so it is not misread. G1 asks whether **at least one** named row
recovers, so this does not affect the gate.

### 4.3 Why this cannot bias G1 toward `YES`

The amendment changes which seeds are **offered**. It does not touch any acceptance criterion. A
recovery at G1 requires, unchanged from the pre-registration:

* hookstep-Newton convergence of the extended residual to `‖R‖ ≤ tol = 1e-8`; **and**
* the converged `(T, s)` to match a named Table IV row within
  `MATCH_T_TOL = MATCH_S_TOL = 0.05`.

Neither is a function of pool size. A poor seed fails to converge and is banked as a failed
attempt with its residual history. The direction the amendment *does* have force in is the
opposite one: without it, U3 could only have reported a shortfall on a pool of one, which is
strictly less informative than the `UNDER-RESOURCED` that AMENDMENT 3 already commits to.

### 4.4 The degree of freedom, and how it is closed

**AMENDMENT 4 was made after observing the shortfall.** It is labelled as such in its first
sentence. The disclosure alone is not sufficient, so the rule also fixes the knob: `per_anchor` is
raised **once, in one step**, to 500; if the anchored pool had still fallen below 100, U3 would
run on the pool it had and report the shortfall as a count in
`seed.seed_supply_funnel.short_of_requested`. Without that clause, "raise it until the pool clears
100" is operationally indistinguishable, after the fact, from "raise it until the result comes
out".

The curated G1 record banks the whole funnel
(`n_candidates`, `n_in_newton_window`, `n_zero_y_shift`, `n_anchored`, `n_requested`,
`short_of_requested`) so that a seed-supply shortfall stays distinguishable from AMENDMENT 3's
iteration-cap shortfall. **Neither licenses a `no`.**

## 5. The `m ≠ 0` drop is a realization limit, not a filter choice

345 of the in-window candidates at `per_anchor = 500` carry a nonzero discrete cross-stream shift.
This programme's extended residual is

```
R(w₀, T, s) = σ_s Φ_T(w₀) − w₀
```

with `σ_s` a **continuous streamwise** shift only. There is no `m` unknown. An `m ≠ 0`
near-recurrence therefore cannot be *expressed* as a seed for this system — it is not that it
would be a bad seed, it is that the parametrisation has no slot for it.

Under **lesson 91** (a negative names its realization, trial space and basis), this must travel
with any negative result out of U3. All eight named rows have `m_published = 0`, so nothing named
is lost and the gate is unaffected; but a `no` from this unit would have to read "no named orbit
recovered *using a residual that cannot represent the `m ≠ 0` class*". The count is banked in
`seed.candidates_dropped_for_nonzero_y_shift` rather than silently discarded.

Extending to `m ≠ 0` is a change to the realization and to the Jacobian's unknown vector, not a
tuning. It is recorded as a successor item and was **not** done here, because U1's milestone M1
validated the globalisation layer against *this* residual and changing it would invalidate that
reproduction.

## 6. Drift guard

The period table exists in two modules (`u2_m2_dns_recurrence.py` needs it for stratification;
`u3_g1_attempts.py` needs it for anchoring, and cannot be imported by the former because the
dependency runs the other way). Two copies of a published table is one more than is safe, so they
are checked rather than trusted:

```python
assert [(n, T) for n, T, _, _ in TABLE_IV] == _U2_TABLE_IV_PERIODS, (
    "Table IV periods disagree between u2_m2_dns_recurrence and u3_g1_attempts")
assert T_ANCHOR_TOL == _U2_T_ANCHOR_TOL, "anchor tolerance disagrees with U2"
```

At import time, so no run can begin with the two out of step.

## 7. What is and is not established

**Established (UNVERIFIED, §3f):** a `T = 1e5` DNS on the chaotic attractor at the pre-registered
scale; a recurrence library from a lossless prefilter with the source papers' own thresholds and
selection criterion; a best candidate `R = 0.016543` against leg 353's `0.177`; a characterised
selection bias in globally-ranked recurrence mining, with the funnel counted at three budget
settings; a stratified fix that restores the pre-registered attempt count.

**Not established:** anything about orbit recovery. `R = 0.016543` is a reduced-proxy *seed*
residual, not a converged Newton residual, and the distance between those is exactly what gate G1
measures. No basin radius (G2, U4). `CLAY_OBLIGATIONS` §6's two no-method obligations stay
**OPEN**; §4 stays **OPEN and NOT discharged** pending leg 386's pre-registered δ mode. **Ceiling
TIER 2.** No `L1 → L4` link moved. **Clay ~0.05%.**

**Generalisable finding, stated without the fluid dynamics:** when a pipeline ranks candidates
globally by a similarity score and then filters them by a property the score is blind to, and when
the score is systematically monotone in that property, the ranked output and the filter's
acceptance region can be nearly disjoint — and the pipeline reports abundance right up to the last
stage. The abundance is real. It is just entirely outside the acceptance region.
