# TECHNICAL — Route-DEXC v1: a certified far-field decay enclosure

**Leg 382, construction class, floor-eligible.** Enforces `CLAY_OBLIGATIONS.md` §8 bullet 2
("Produce far-field decay as a **certified enclosure**, not a fit") as a build.

| | |
|---|---|
| Module | `solver/dssp_decay_enclosure.py` (new) |
| Tests | `test_dssp_decay_enclosure.py`, **12/12** |
| Runner | `experiments/p2_route_dexc_v1.py` |
| Curated data | `writeup/data/p2_route_dexc_v1.json` |
| Figure | **fig100**, `experiments/p2_route_dexc_v1_evidence.py`, registered in `writeup/build_figures.py` |
| Novelty pass | `writeup/novelty/leg_382.md` (committed BEFORE construction) |
| Pre-registration | `experiments/journal/leg_382.md` Part I (committed BEFORE the module existed) |
| Reads, edits nowhere | `solver/dssp_screen.py` |
| Ceiling | **TIER 2**. No `L1 → L4` link moved. Clay ~0.05%. |

---

## 1. The gate, and its answer

> **Q.** Does the enclosure reproduce a planted profile's EXACT known exponent within its
> certified interval on the pre-registered window, AND fail (interval excludes truth or
> reports incapacity) on a planted mismatched control — with the fitted column left in place
> and the certified column recorded ALONGSIDE it, never replacing it?

> **A. YES.**
> *The §4 obligation has a named instrument; its first real consumer is whatever future unit
> produces a profile — none exists yet and this leg claims nothing about one.*

The yes-branch text is the gate's own, unedited. §7 below states, in the same detail, what the
YES does not buy.

## 2. What is certified

For a supplied positive profile magnitude `f` on a radial window `[R₀, R₁]`:

```
P_cert(f, R₀, R₁) := { p ≥ 0 : ∃ C > 0 with C·r^(−p) = f(r) for ALL r ∈ [R₀, R₁] }
```

The routines return an **outer enclosure** `[p_lo, p_hi] ⊇ P_cert`, or `EMPTY`, or
`INCAPACITY`. The asymmetry is the whole content and is stated in the module docstring:

* **`EMPTY` is a proof of a negative** — no exponent in the search bracket works.
* **a nonempty interval is not a proof of a positive** — it says only that no exponent
  *outside* the interval can work. A profile with a power-law envelope and a wiggle inside the
  tube is not excluded.

That asymmetry is what makes it fit for §4: the cutoff analysis needs a *bound* on the
exponent, and an outer enclosure of `P_cert` is exactly a bound.

## 3. Method

`t = log r`, `g = log f`; a power law is the affine relation `g(t) = c − p·t` with `c = log C`.
Each cell contributes an enclosure of `g`, hence linear inequalities in `(c, p)`. Eliminating
`c` pairwise — Fourier–Motzkin, **exact in two variables**, so the survivor is precisely the
projection of the feasible polygon onto the `p` axis — gives, for constraint points `k, m`:

```
g_lo_k + p·t_lo_k  ≤  c  ≤  g_hi_m + p·t_hi_m
      ⟺   p·(t_lo_k − t_hi_m) ≤ g_hi_m − g_lo_k        ⟺   p·A_km ≤ B_km
```

`A > 0` gives an upper bound `p ≤ B/A`; `A < 0` a lower bound; `A` straddling zero is
**dropped**, which can only enlarge the returned set. All directed rounding is **outward**
(lower bounds down, upper bounds up), so emptiness is proved on a *relaxed* system and holds a
fortiori on the exact one.

**Substrate:** `solver/interval.py` — `Interval`, `ilog`, outward-rounded arithmetic. The
`capabilities.py` grep was performed first, per the standing requirement: four modules import
`Interval` (`interval`, `interval_mp`, `interval_certificate`, `nk_fourier`) and none of them
touches decay. The **only** new primitive is `isqrt` (one outward-rounded `np.sqrt`, rigorous
because IEEE-754 `sqrt` is correctly rounded), and it is used only by the planted-profile
generator for half-integer exponents — never by the enclosure.

### 3.1 Two modes, answering different questions

| mode | statement | use |
|---|---|---|
| **`cells`** | profile evaluated over each WHOLE cell; covers every `r ∈ [R₀,R₁]` with no inter-sample gap | **gate-deciding** |
| `nodes` | profile evaluated at exact nodes; "consistent with `r^(−p)` at these nodes" — strictly weaker | reference only, never quoted as a certified decay bound |

### 3.2 Declared limitations

* **Search bracket `p ∈ [0, 12]`.** Fixing `p ≥ 0` is what makes `max_{t∈T}(p·t)` attain at a
  fixed endpoint and every constraint linear in `p`; it also requires `R₀ > 1` so every
  `t = log r` is positive. Both are checked at entry.
* **A bracket-limited answer is `INCAPACITY`, never `EMPTY`.** An exponent outside the bracket
  drives `p_lo` past `p_hi` by the same arithmetic that a genuine mismatch does, and calling
  that "no power law exists" would be false. Measured: a planted `p₀ = 13` returns
  `INCAPACITY` under `[0,12]` and is recovered as `[13.000000000000, 13.000000000000]` under
  `[0,20]` (`test_exponent_outside_the_bracket_is_incapacity_not_empty`).
* **Half-integer restriction is on the planted-profile GENERATOR only**, because
  `solver/interval.py` has `ilog` but no `iexp` and this leg chose not to write an unproved
  transcendental. The enclosure itself accepts any interval-valued callable and searches the
  continuum.

## 4. Pre-registration and the anti-tautology discipline

Committed before the module existed (`experiments/journal/leg_382.md` Part I; commit order
novelty → pre-registration → construction is in the git log):

* **Window `[R₀, R₁] = [10.0, 1000.0]`**, chosen for one reason: it is the span of
  `dssp_screen`'s own fitted ladder `np.logspace(1.0, 3.0, 12)`, so the certified and fitted
  columns are measured on the same window. Leverage `W = log 100 = 4.60517`. **Not moved
  during the leg.**
* Gate cell count `N = 1000`; ladder `N ∈ {50,…,2000}` measures a rate, does not pick a winner.
* Planted knowns K1–K4 at exact `p₀ = 1, 2, 2.5, 3`.
* Gate controls C1, C2 that **must** fire, with a control that does not fire declared a
  STOP-and-report (leg 340: an instrument that cannot fail is a tautology; leg 361: never widen
  the window to make something pass).
* C3 and the curvature ladder declared **non-gate-deciding before the run**, so a null there
  could not be reinterpreted afterwards.

All four anti-tautology checks pass (JSON `anti_tautology_checks`): no known returns the full
bracket; no gate control returns a nonempty interval; no known is certified EMPTY; `nodes` mode
is reported for every row.

## 5. Results

### 5.1 Planted knowns — certified alongside fitted, `N = 1000`, `cells`

| id | profile | truth `p₀` | certified interval | width | **fitted** `p` (dssp_screen, unmodified) |
|---|---|---|---|---|---|
| K1 | `3.0 r^(−1)` | 1.0 | `[0.9999999999999963, 1.0000000000000038]` | `7.438e-15` | `1.000000000000` |
| K2 | `1.0 r^(−2)` | 2.0 | `[1.999999999999992, 2.000000000000008]` | `1.599e-14` | `2.000000000000` |
| K3 | `0.25 r^(−5/2)` | 2.5 | `[2.49999999999999, 2.5000000000000098]` | `1.998e-14` | `2.500000000000` |
| K4 | `7.0 r^(−3)` | 3.0 | `[2.9999999999999916, 3.000000000000007]` | `1.554e-14` | `3.000000000000` |

All four contain the exact truth; none reaches the `[0,12]` bracket. The half-integer K3 rules
out integer snapping.

### 5.2 Gate controls — both fired

| id | profile | certified | contradiction gap `p_lo − p_hi` | **fitted** `p` |
|---|---|---|---|---|
| C1 | `r^(−2) + 0.01 r^(−1)`, crossover `r* = 100` **inside** the window | **EMPTY** | `+0.817419` | `1.500000` |
| C2 | `r^(−2)/(1 + (r/300)^4)` | **EMPTY** | `+3.966962` | `2.808892` |

C1's crossover was placed inside the window deliberately: a mixture whose crossover lay outside
would have been an un-fireable control, i.e. exactly the leg-340 tautology.

### 5.3 Resolving-power probes (declared non-gate-deciding)

* **C3**, `r^(−2)·log r`: **EMPTY**, gap `+0.244817`; fitted returns `1.768252`.
* **Curvature ladder**, `r^(−2)(1 + κ(log r − t_mid)²)`, `t_mid = log 100`: EMPTY at every
  `κ > 0` tried. **Smallest `κ` certified EMPTY = 1e-6**, the smallest nonzero rung on the
  ladder — so the ladder did **not** reach the detection threshold and the true threshold is
  *below* 1e-6. Recorded as a bound, not as the threshold. Gaps scale linearly:
  `κ = 1e-6 → 8.794e-6`, `1e-4 → 8.789e-4`, `1e-1 → 5.856e-1`.

### 5.4 Cell-count ladder — the pre-committed prediction is REFUTED

Predicted: `width ≈ 2p₀/N` (`4.0e-3` at `N = 1000`), log-log slope `−1.00 ± 0.05`.

| `N` | 50 | 100 | 200 | 500 | 1000 | 2000 |
|---|---|---|---|---|---|---|
| width | `1.754e-14` | `1.688e-14` | `1.665e-14` | `1.643e-14` | `1.599e-14` | `1.554e-14` |
| max log-tube width | `1.842e-01` | `9.210e-02` | `4.605e-02` | `1.842e-02` | `9.210e-03` | `4.605e-03` |

**Measured log-log slope `−0.0295`, against a predicted `−1.00`. The prediction is wrong and is
recorded as wrong, not amended.** Mechanism: for a monotone profile the cell enclosure's
endpoints coincide with the *exact* pointwise values at the cell edges, so the binding
Fourier–Motzkin pairs are already sharp and no cell-width penalty is paid. The instrument is
better than predicted; the log-tube width does fall as `1/N` exactly as expected, but that
width does not propagate into the projection.

### 5.5 The finding that mattered — zero tolerance is unusable on numerical data

`K2ε`: `f = r^(−2)(1 + ε(r/R₁ − 1/2))` at `N = 1000`, `δ = 0`:

| `ε` | 0 | 1e-12 | 1e-9 | 1e-6 | 1e-3 | 1e-2 |
|---|---|---|---|---|---|---|
| verdict | INTERVAL | **EMPTY** | **EMPTY** | **EMPTY** | **EMPTY** | **EMPTY** |
| signed width | `+1.643e-14` | `−6.675e-13` | `−8.597e-10` | `−8.602e-7` | `−8.598e-4` | `−8.564e-3` |

**EMPTY here is mathematically CORRECT** — a perturbed power law has no exact exponent, so
`P_cert` is genuinely empty — and it is **not** an instrument defect. The pre-registration
called "the truth stays inside for every ε" a soundness requirement whose violation would be a
defect; that was a **mis-statement of the certified object**, and it is recorded rather than
quietly corrected.

The consequence is the real result: **no numerical profile is ever exactly a power law, so the
zero-tolerance instrument would answer EMPTY for every real input it was ever handed.** It
would be rigorous and useless. This is pinned as a regression test
(`test_zero_tolerance_rejects_any_perturbation`) so it cannot be "fixed" into silence.

## 6. The tolerance extension — **POST-HOC, NOT PRE-REGISTERED, NOT GATE-DECIDING**

Added *after* the run, in response to §5.5. Flagged as post-hoc in the module docstring, the
runner docstring, and the JSON (`post_hoc_tolerance_extension.status`). **The gate was answered
on the zero-tolerance runs in §5.1–5.2 and nothing here changes it.**

```
P_cert^δ := { p ≥ 0 : ∃ C > 0 with f(r)/(1+δ) ≤ C·r^(−p) ≤ f(r)(1+δ)  ∀ r ∈ [R₀,R₁] }
```

`δ` is **not a fitting knob**. It is an input the caller owes: the relative accuracy to which
the caller's own profile is itself certified. Two properties make that auditable, and both are
tested: widening `δ` can only *enlarge* the feasible set (widths monotone, EMPTY downward
closed), and pairing `δ` to a profile's own perturbation size recovers the truth.

**Certified width vs `δ`** (exact `r^(−2)`, `N = 200`):

| `δ` | 0 | 1e-12 | 1e-9 | 1e-6 | 1e-3 | 1e-2 | 1e-1 |
|---|---|---|---|---|---|---|---|
| width | `1.665e-14` | `8.928e-13` | `8.730e-10` | `8.730e-7` | `8.725e-4` | `8.686e-3` | `8.320e-2` |

i.e. **width ≈ (4/W)·δ = 0.8686·δ**, half-width ≈ `0.434·δ`. Perturbed profiles with `δ` set
equal to `ε` recover truth `2.0` at every rung (widths `8.869e-13` … `8.595e-3`).

**Critical tolerances `δ*`** — the sloppiness at which each mismatch stops being excluded
(bisected to ~1e-13, `N = 200`):

| id | mismatch | `δ*` |
|---|---|---|
| C2 | rational far cutoff | **3.352868** |
| C1 | two-power mixture | **0.315697** |
| C3 | log correction | **0.069739** |
| K2 | exact power law | **0** (never excluded, at any tolerance) |

The `K2` row is the direction-sensitivity check: the instrument is not merely fail-happy.

## 7. What this does NOT establish — pre-committed, and unchanged by the YES

1. **No profile exists.** Route 4 has produced no profile of its object. Validation is on
   **planted analytic knowns only**. The instrument's first real consumer is a future unit that
   does not exist, and this leg claims nothing about one.
2. **§4 is not discharged.** §4 requires the certified exponent **and** the admissible cutoff
   radius **and** the size of the perturbation the cutoff introduces. This leg supplies the
   first of three. The cutoff analysis is **entirely unattempted**.
3. **`CLAY_OBLIGATIONS.md` §6's two no-method items both stay OPEN.** Item 1 because only half
   of it was attempted; item 2 (§5 persistence/stability under localisation) because it was not
   attempted at all and, per leg 314, is *"a theorem, not a computation"*.
4. **The fitted column is untouched.** `solver/dssp_screen.py` is read and edited nowhere on
   this branch; the certified column is recorded alongside it in the same JSON row, which is
   the only arrangement in which §5.2's comparison exists at all.
5. **No `L1 → L4` link moved. Ceiling TIER 2. Clay ~0.05%.**
6. **A hole in the novelty pass, disclosed.** arXiv and Semantic Scholar both returned
   HTTP 429 this leg, so the external prior-art question — whether a published method exists
   for exactly the §4 obligation — was **not** answered and is left open for a successor with
   working network access. The in-repo half of the pass *was* completed and is conclusive:
   every log-log exponent in the tracked tree is a least-squares fit.

## 8. Left to a successor

* **The cutoff half of §4.** Given a certified `[p_lo, p_hi]`, derive the admissible cutoff
  radius and bound the perturbation. That is the remainder of §6 item 1 and it is the natural
  next construction; this leg deliberately did not start it.
* **The samples→cells bridge.** `certified_decay_from_cell_enclosures` is the entry point a
  profile-producing unit should call, and it takes *certified cell enclosures*. A unit holding
  only pointwise samples must first convert them via a certified modulus of continuity or a
  stated monotonicity hypothesis. The module names that obligation rather than burying it, but
  **does not provide the conversion**.
* **The curvature detection threshold** is bounded above by `κ = 1e-6` and not located; the
  ladder bottomed out.
* **The external prior-art question** in §7 item 6.
