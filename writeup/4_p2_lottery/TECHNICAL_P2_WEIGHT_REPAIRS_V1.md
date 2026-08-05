# Weight-repairs v1 — the two named C-PILOT repairs, re-run on the frozen gate

*Prep leg, `prep/weight-repairs`. Repairs P2 and P3 named in
[`TECHNICAL_P2_ROUTEC_PILOT_V0.md`](TECHNICAL_P2_ROUTEC_PILOT_V0.md) §4, implemented in
`solver/weight_search.py`, gated in `test_weight_search.py`. Code:
`experiments/p2_weight_repairs_v1.py` → `writeup/data/p2_weight_repairs_v1.json` →
**fig48**. Deterministic, ~140s.*

**VERDICT: still FAIL, 4/6 — unchanged in count, moved in substance.** P2's finite
fraction rises from 0.775 to 0.875 (threshold 0.90). P3's raw numbers are now an
honest accounting of what a floating-point probe can validate at all, rather than an
assumption that one global grid was linear for all forty roster weights. **Neither
repair was tuned against this run's own numbers; both constants were fixed in the
code before it ran.** The GA remains banned, and a same-day PASS would not have
lifted the ban either — only the next planning pass may act on a gate result
(`ORCHESTRATION.md` lane 6, `plan_of_record.py`).

---

## 0. What was named, and where

`TECHNICAL_P2_ROUTEC_PILOT_V0.md` §4 ran the frozen six-property gate on the
certificate-weight fitness `log10(Y0/budget)` and reported:

| | property | measured | threshold | |
|---|---|---|---|---|
| P2 | finite | 0.775 finite | ≥ 0.90 | **FAIL** |
| P3 | monotone | 0 violations; max \|slope−1\| = 0.366 | 0; ≤ 0.05 | **FAIL** |

and closed with: *"The repairs are named and neither is research: carry the measured
lower wall in the box as the analytic one already is (P2), and state the fitness's
defect-tracking accuracy as a resolution rather than assuming it is exact (P3)."* This
leg implements both, exactly as named, and re-runs the identical frozen predicate.

---

## 1. P2 — carrying the measured lower wall

### 1a. The mechanism

`solver/weight_search.py` already had an analytic upper wall on the search box:
`Ω₀ ~ −1/X`, so a weight `ν ~ |X|^(p+q)` gives the TRUE profile infinite weighted sup
norm past `p+q = 1`, and `in_box()` enforced `p+q ≤ WALL_POWER − WALL_DELTA` as a hard
constraint, derived before any run.

It also already had `lower_wall()` — leg 49's §5 measurement of a *second*, non-analytic
wall: bisect the far-field power on a single-power slice and find where `Z₁` crosses 1.
Past that point `A = DF⁻¹` stops being an approximate inverse in the norm at all, so the
fitness has no budget to report at ANY residual — this is float conditioning
(`κ(DF)·ε_mach`), not a property of the equation. `lower_wall()` was measured but never
carried into `in_box()`, so the roster (and the grid search) kept sampling into a region
already known, before the run, to be doomed. Every one of leg 49's 9 censored roster
weights had far-field power `p+q ≤ −2.41`, below `lower_wall()`'s measured `p₋ = −3.68`
to `−3.74` at `n=201`.

### 1b. The repair

```python
def in_box(theta, lower_wall_power=None):
    ...
    if ffp > WALL_POWER - WALL_DELTA:
        return False
    if lower_wall_power is not None and ffp < lower_wall_power + WALL_LOWER_DELTA:
        return False
    return True
```

`WALL_LOWER_DELTA = 0.05`, symmetric with the existing `WALL_DELTA` margin on the upper
wall. `FitnessEngine` carries `lower_wall_power` as an attribute (`None` reproduces the
pre-repair behaviour exactly — every existing caller that does not pass it is
unaffected); `roster()` and `FitnessEngine.fitness_many`'s box filter both thread it
through. `six_property_gate` measures `lower_wall(eng_c)` and `lower_wall(eng_f)` once
per resolution and sets it on the corresponding engine before drawing the roster.

### 1c. The result — real, and honestly incomplete

| | before (leg 49) | after (this leg) | threshold |
|---|---|---|---|
| P2 finite fraction | 0.775 | **0.875** | ≥ 0.90 |

Still `FAIL`. The wall carried here is a **one-parameter slice** — `lower_wall()`
bisects on `ν = (1+X²)^(p/2)`, i.e. `q=0, L=l=1` — and leg 49 §4b already recorded the
converse does not hold in general: *"a finite weight exists at −4.04"* below the
measured wall, because the search's actual two length scales `L, l` decide *where* the
decay begins, not just how fast. Carrying a 1-D proxy for a genuinely higher-dimensional
boundary buys real ground (9 censored → 5) without closing it. Fig48 panel B shows the
roster against both walls: the repaired box has no draws left in the region the 1-D wall
rules out, and the remaining censored weights are ones the slice approximation misses.

---

## 2. P3 — the defect-tracking accuracy is a resolution, not an exactness

### 2a. The mechanism

Leg 49's `defect_ladder` pushed the converged state off the solution by `ε` in a fixed
direction and checked `Y₀` fell linearly (`F(z*+εd) = εDF·d + O(ε²)`, so the fitness must
fall with slope exactly 1 per decade — a real known answer). It tested every roster
weight on **one** global `ε` grid, `10⁻²…10⁻⁶`.

The diagnosis in §4a already located the problem: `‖A‖_w` — the operator norm the
linearization's remainder is measured against — spans **three orders of magnitude**
across the roster (naive `1.69e8`, leg 46's tuned `1.69e6`, the searched optimum
`3.37e5`). The linear regime only begins once `ε ≲ 1/‖A‖_w`. A single grid that is
comfortably linear for the searched weight (`ε_max ≈ 3e-7`) is already well past
linearity for the naive weight (`ε_max ≈ 6e-9`) at the SAME grid points — so testing all
weights on one grid measures the probe's own breakdown at the high-`‖A‖_w` end, not a
genuine fitness defect there.

### 2b. The repair

```python
DEFECT_WINDOW_C = 0.1
DEFECT_EPS_DEFAULT = (1e-2, ..., 1e-11)   # extended to 10 points
DEFECT_MIN_WINDOW = 3

def defect_ladder(problem, z_star, engine_thetas, direction=None, eps=None):
    ...
    a_norms = [certificate_constants(...)['A_norm'] for each theta]
    eps_max = DEFECT_WINDOW_C / a_norms          # PER-WEIGHT window
    for each weight:
        mask = eps <= eps_max[weight]
        resolved = (mask.sum() >= DEFECT_MIN_WINDOW) and all finite
        if resolved: fit slope, check monotonicity WITHIN the window
```

`DEFECT_WINDOW_C = 0.1` is a factor of 10 inside the empirically-located onset of
nonlinearity (`ε ~ 1/‖A‖_w`), fixed once in the module before this leg's numbers were
measured. The `ε` grid was extended down to `10⁻¹¹` so that even the highest-`‖A‖_w`
roster weights (up to `~1e9`) can have at least `DEFECT_MIN_WINDOW = 3` grid points
inside their own window — `10⁻¹¹` still perturbs an `O(1)` state by far more than
double-precision roundoff (`~2e-16` relative), so this does not trade one numerical
artifact for another.

`six_property_gate` now reports, per weight: whether it was `resolved` at all (window
had ≥3 usable points), and if so, its fitted slope and whether it decreased monotonically
INSIDE that window. Weights with too few points are reported as `unresolved` rather than
silently included in a global pass/fail — this is the "resolution" the repair asks for:
not "the fitness is exact everywhere," but "here is how much of the roster this probe
can even certify, and how well the certified part tracks the known answer."

### 2c. The result — the honest number is worse-looking and more trustworthy

| | before (leg 49, one global grid) | after (per-weight windows) |
|---|---|---|
| max \|slope−1\| | 0.366 (all 40 weights) | 0.342 (21/40 **resolved** weights) |
| monotonicity violations | 0 (all 40, on the old grid) | 8 (of the 21 resolved) |
| weights validated at all | 40 (implicitly) | **21/40** |

Still `FAIL` against the frozen 0.05 threshold. The repair does not manufacture a pass —
it exposes that **19 of 40 roster weights cannot be validated by this probe design at
all**, because their `‖A‖_w` is high enough that even `ε = 10⁻¹¹` does not buy three
usable points inside the linear window. Among the 21 that CAN be validated, 8 now show
monotonicity violations that leg 49's coarser, ε≥10⁻⁶ grid never saw — the most likely
reading is float64 roundoff noise at the smallest usable `ε` for those weights (a
different failure mode than leg 49's diagnosed nonlinearity, and this leg does not claim
to have fixed it; it is reported as found). Fig48 panel C shows the window-size
distribution across the roster: it is bimodal, not a smooth degradation, which is
itself worth recording rather than averaging away.

---

## 3. What moved, what didn't, and why the gate still says no

Neither repair was chosen, retroactively, to make a threshold. Both constants
(`WALL_LOWER_DELTA = 0.05`, `DEFECT_WINDOW_C = 0.1`) are committed in
`solver/weight_search.py` and were fixed before `six_property_gate` was re-run — the
same discipline the frozen thresholds themselves follow, and the one leg 49 explicitly
invoked when it declined to retune P3's threshold after seeing it miss.

`P4`–`P6`, `P1` and `P5` are unaffected in verdict (all still `PASS`) though `P1`/`P5`'s
spread number shifts slightly (`15.02 → 12.69` decades) because the roster itself is
different — the P2 repair removed the lowest-far-field-power draws, which were also
some of the most negative (best) fitness values, so the spread narrows a little as a
direct, expected consequence of the repair working.

**The gate is FAIL, 4/6, honestly measured, with both named repairs done.** The
remaining gap on P2 is a dimensionality problem (a 1-D wall proxy for a 2-D boundary);
the remaining gap on P3 is that fewer than half the roster is even probe-able at
double-precision, and the probe-able half still misses the 5% threshold at its worst
point. Both are further, specific engineering questions — not the same two questions
this leg answered, and not answered here.

---

## 4. The ceiling

No link of the `L1 → L4` chain moved. The object underneath this fitness is the `a=0`
CLM profile, closed form since 1985; nothing here is a certificate, and no novelty is
claimed for the repairs (they are named engineering, not method). Per
`ORCHESTRATION.md` lane 6 and `plan_of_record.py`, the GA ban stands regardless of this
result — a same-day 6/6 would not have authorized GA compute today either; only the
next planning pass may act on a gate result, and this one still says FAIL.
