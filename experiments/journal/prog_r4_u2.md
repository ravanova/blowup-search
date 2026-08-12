# PROG-R4, unit U2 — MILESTONE M2: the T=1e5 DNS and its recurrence library

**Programme:** PROG-R4 (`ORCHESTRATION.md` §3c PROGRAMME lane, slot A, leg 380).
**Unit kind:** MILESTONE. A build unit. **No claim is made and no gate is answered here.** The
programme's two gates are G1 (unit U3) and G2 (unit U4), pre-registered verbatim in
`experiments/journal/prog_r4_prereg.md`. Nothing below may be read as bearing on either.

**Preceded by:** U0 (novelty, `writeup/novelty/prog_r4.md`, verdict PROCEED) and U1 (MILESTONE
M1, the hookstep/trust-region globalisation layer, landed at `703b616` and reproduced against
leg 353's laminar control).

**Mode:** `ORCHESTRATION.md` §3f SOLO. No paired verifier, no DM, no orchestrator. Everything
below was built and checked in one session and is therefore **UNVERIFIED** in the repo's sense.
Verification is a fresh session or it is not verification.

---

## 1. What this unit asked

Two things, from the programme spec:

1. a DNS of 2-D Kolmogorov flow at `Re = 60`, `N = 24`, run to `T = 1e5` — the length the
   question is posed at, not the length that is convenient;
2. a recurrence-candidate library mined from it, with every threshold taken from the source
   papers rather than chosen here.

Both delivered. This is what leg 353 did not have, and it is the whole reason G1 can be asked at
a scale at which a null would mean anything.

## 2. Why `T = 1e5` and not `T = 2000`

Leg 353 named DNS length as one of its two declared simplifications and ran to `T = 2000`. At
that length, with five attempts, `P(0 successes)` under the sourced per-attempt rates is
59–77% — a null carries essentially no information. Chandler & Kerswell 2013 (arXiv:1207.4682)
and Lucas & Kerswell 2015 (arXiv:1406.1820v2) both mine trajectories two orders of magnitude
longer. At `T = 1e5` with ~100 attempts, `P(0 successes)` is ~1.2% at Chandler & Kerswell's 4.3%
per-attempt rate for the nonzero-shift RPO class and ~3e-5 at Lucas & Kerswell's ~10%. That gap
is the entire difference between an under-resourced null and a resourced one under §3d.

## 3. The DNS, as measured

Run from `t = 0` to `t = 1e5` at `dt = 0.01`, `N = 24`, `Re = 60`, forcing wavenumber 4, with a
burn-in of `T_BURN = 500` discarded before anything is recorded, and snapshots at
`dt_save = 0.25`.

| quantity | measured |
|---|---|
| snapshots recorded | 400,000 |
| wall time | 3.44 h |
| per step | 1.2379 ms |
| dissipation, `D / D_lam` | **0.0645 ± 0.0253** |

The last row is the one that matters and it is a check, not a statistic: a trajectory that had
collapsed onto the laminar fixed point would read `D / D_lam = 1` with zero spread. `0.0645` with
a 39% relative spread is the chaotic attractor, sustained for the full `1e5`, which is the
precondition for there being any recurrences to mine at all.

**A previous session was wound down with this DNS at 16% (`t = 16,000`) and that partial run was
killed and its output abandoned.** Nothing from it survives in what is banked here. This run
started from `t = 0`.

## 4. The recurrence measure, and the prefilter that makes it affordable

The measure is Chandler & Kerswell eq. (23) in its squared relative form, minimised over **both**
the continuous streamwise shift `s` and the discrete `y`-shift `m`. Thresholds are theirs, not
ours: `R_thres_record = 0.30` for what gets recorded, `R_thres_window = 0.25` for what counts as
inside the Newton window, and a period window `T ∈ (0.5, 60.0)`.

Minimising over `s` and `m` at every one of ~9.6e7 `(t, T)` pairs is not affordable. It is not
necessary either, because of a **lossless** prefilter:

```
R_red(t, T) = Σ (|Ω(t)| − |Ω(t−T)|)² / Σ |Ω(t)|²    ≤   R(t, T)   pointwise
```

The inequality holds because `|a − b| ≥ ||a| − |b||` and because every symmetry in the
minimisation multiplies each Fourier coefficient by a phase of unit modulus, leaving `|Ω|`
invariant. So thresholding the proxy at the same value **discards nothing** — a candidate the
proxy rejects could not have passed the real measure. That statement is banked verbatim in the
library JSON's `prefilter.statement`, because it is the load-bearing claim of this stage.

## 5. Selection: strict interior local minima, not a threshold ranking

Candidates are **strict interior local minima of `R_red` in the `(t, T)` plane** — the papers'
own criterion. This is not a cosmetic choice. Ranking by `R_red` value instead fills the entire
budget with `T ≈ 0.5` cells where the trajectory has barely moved and the measure is small for
trivial reasons; and those cells are boundary points of the window, so they can never be interior
minima. The criterion excludes them structurally rather than by a tuned cutoff.

## 6. What the library came out as

| quantity | measured |
|---|---|
| `(t, T)` pairs scanned | 95,542,640 |
| below `R_thres_record = 0.30` | 31,244,629 |
| strict interior local minima | 913,301 |
| scan wall time | 71.0 s |
| best `R` after full minimisation | **0.016543** |

For scale: **leg 353's best over its whole `T = 2000` trajectory was `R = 0.177` for UPO37.** The
best candidate here is an order of magnitude closer to an exact recurrence. That is what the
extra length bought, and it is the honest way to state the gain — as a magnitude, not as a
promise about G1.

**MILESTONE M2 is ANSWERED.** It says the instrument and the data exist at the pre-registered
scale. It says **nothing** about whether any named Table IV orbit recovers. That is G1, unit U3,
and it is answered by a separate runner against a gate whose wording was fixed before any of this
existed.

## 7. The finding this unit did not expect: the ranking starves the band

After the library was mined, the seed funnel was counted end to end, and the pre-registered 100
attempts turned out to be **unreachable**:

| stage | count |
|---|---|
| candidates passed to full minimisation | 400 |
| of those, inside L&K's Newton window `R < 0.25` | 260 |
| of those, with `m = 0` | 102 |
| of those, anchored to a named Table IV period | **1** (UPO32) |

One seed, not 100.

Two filters do the damage, and they are different in kind.

**The `m = 0` filter is a realization limit** (lesson 91: a negative names its realization). This
programme's extended residual carries a continuous `x`-shift only, so a near-recurrence with a
nonzero discrete `y`-shift cannot be *expressed* as a seed for it. Every named Table IV row has
`m_published = 0`, so nothing named is lost — but 345 of the in-window candidates are, and the
count is banked rather than silently dropped. A successor that wants them needs a residual with a
`y`-shift unknown, which is a change to the realization and not a tuning.

**The anchoring collapse is a mining artefact, and it is the real finding.** The global top-400
ranking is dominated by short-period near-recurrences at `T = 1.25 – 2.5`: they are far more
numerous, and over a shorter interval the trajectory has less opportunity to separate, so they
score lower on `R_red`. Every named orbit lives at `T ≈ 14.8 – 19.3`. A global top-N therefore
spends its whole budget below the band of interest. Nothing about the flow, nothing about Newton.

The fix is `AMENDMENT 4` in the addendum, made **after** observing the shortfall and labelled as
such: stratify the candidate budget across the eight named periods, keeping the global list whole
and adding the best `per_anchor` local minima within `T_ANCHOR_TOL = 1.0` of each. Realised:

| stage | global-only | `per_anchor = 80` | `per_anchor = 500` |
|---|---|---|---|
| candidates | 400 | 634 | 2014 |
| `R < 0.25` | 260 | 333 | 579 |
| `m = 0` | 102 | 131 | 234 |
| anchored | **1** | **30** | **133** |

133 ≥ 100, so U3 runs at the pre-registered count. The amendment argues at length why this cannot
bias G1 toward `YES` — it changes which seeds are *offered*, never what counts as a recovery, and
a recovery still requires an actual convergence to `‖R‖ ≤ 1e-8` whose converged `(T, s)` matches a
named row within 0.05 — and it closes the degree of freedom by fixing `per_anchor` in one step,
once, with U3 running on whatever pool it has if that had still fallen short.

UPO34 draws zero anchored candidates. Anchors are assigned by nearest named period, and 18.878
sits between 18.912 and 18.694 at a spacing far below the tolerance, so it is never the nearest
row for anything. That is a property of the published table's spacing, not of the flow, and it is
recorded here so it is not misread as a statement about UPO34.

## 8. What this unit does not establish

Nothing here bears on G1 or G2. A library of good recurrence candidates is not an orbit; the best
`R = 0.016543` is a *seed* residual on the reduced proxy, not a converged Newton residual, and the
gap between those two numbers is the entire content of gate G1. `CLAY_OBLIGATIONS` §6's two
no-method obligations stay **OPEN**, and §4 stays **OPEN and NOT discharged** until leg 386 lands
with a pre-registered δ mode. **Ceiling TIER 2.** No `L1 → L4` link is moved by anything in this
unit. **Clay stays ~0.05%.**

## 9. Artefacts

- `experiments/programme_r4/u2_m2_dns_recurrence.py` — the runner, both stages (`--stage dns`,
  `--stage recur`)
- `experiments/programme_r4/u2_dns_meta.json` — the DNS metadata and the `D/D_lam` check
- `experiments/programme_r4/u2_recurrence_library.json` — the library, including
  `prefilter.statement` (the losslessness argument), `prefilter.selection` (the local-minimum
  criterion) and `prefilter.stratification` (the AMENDMENT 4 record and per-anchor availability)
- `experiments/journal/prog_r4_u2u3_prereg_addendum.md` §3d — AMENDMENT 4
- trajectory files (`u2_dns_ckpt.npy`, `u2_dns_feat.f32`, 258 MB) are gitignored and are **not**
  on the branch; `regenerate()` in the runner reconstructs any snapshot U3 needs from the
  checkpoint file

**No figure is spent by this unit.** fig97 and fig98 stay reserved for the two claim units, U3
and U4.
