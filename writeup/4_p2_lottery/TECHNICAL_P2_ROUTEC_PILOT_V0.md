# Route-C-PILOT v0 — the certificate-weight fitness, measured on an object whose answer is known

*Phase 2, leg 49. Stage `C-PILOT` of the plan of record: **evolve the Lyapunov weight, on
an object with a KNOWN answer**, with the six-property viability gate re-run on the new
fitness before any GA compute. Code: `solver/weight_search.py`, `test_weight_search.py`
(8/8), `experiments/p2_route_c_pilot_v0.py` → `writeup/data/p2_route_c_pilot_v0.json` →
**fig44**. Deterministic, 70 s.*

**VERDICT: the gate says FAIL, 4 of 6, and the GA was not run.** The two failures are
specific and priced. On the way to them the leg reproduced the premise the stage was
built on, found where that premise actually lives, and measured a second wall on the
search space that nobody had looked for.

---

## 0. What was pre-committed, and what it cost

`plan_of_record.py` carried the gate before the leg started:

> **GATE:** does the new fitness pass the six-property viability gate? **YES** → proceed
> to stage `B`. **NO** → **STOP. Do not run the GA.**

plus a standing ban — *any GA compute on an unvalidated fitness* — whose lifting
condition is this stage. The six thresholds are frozen constants at the top of
`solver/weight_search.py`, written before the gate was run. The gate returned **FAIL**,
so `C0-5`'s search is a **deterministic grid** (295,245 evaluations, 11 s) and not the
GA. That is the ban working, not a shortcut: the grid was needed for property 6 anyway,
and it makes the search reproducible to the last digit.

---

## 1. The novelty check came first, and it narrows the claim

Leg 48 spent one leg on a novelty check and correctly closed an entire stage. The same
habit here, fourteen arXiv queries, ledger in `solver/weight_search.PRECEDENTS`,
verdict computed by `novelty_verdict()` rather than remembered:

| entry | verdict | why |
|---|---|---|
| SOS / neural Lyapunov + barrier synthesis (a **field**) | `ADJACENT` | automatic search for a certificate's free function is mature — but the object searched is `V(x)` for a flow, not the **norm** of a Newton–Kantorovich contraction |
| **Chen–Hou arXiv:2210.07191 §5.3.3** | `PREMISE_CONFIRMED` | "Order of choosing the parameters": an explicit, ordered, **hand** procedure for picking the weights of their weighted `L^∞` estimate |
| Cadiot–Lessard–Nave arXiv:2302.12877 | `EXCLUSION` | the space is a modelling decision, stated and held fixed |
| arXiv:2509.14185 (*Discovery of Unstable Singularities*) | `ADJACENT` | ML finds the **profile**; the certificate's space is still hand-chosen afterwards |

**Verdict `PROCEED_NARROW`.** Nothing found searches the norm of a radii-polynomial
certificate. But the *idea* of searching a certificate is not new, and this leg claims
no originality for it — only for its object. Chen–Hou §5.3.3 is worth quoting because it
is the human version of this stage, written by the people who do it best:

> *"We adjust the parameters in φ₁ so that we have a good damping factor d₁(x) from the
> local term for ω₁. Then we can estimate the nonlocal terms and the constants … we
> choose the exponents of different powers in φ₂ and adjust the parameters so that we
> have better stability factors."*

---

## 2. The substrate: the plan's named object cannot supply the fitness

The plan named Chen–Hou's certified 2D Boussinesq profile as the known-answer substrate.
**It cannot be one**, and this project's own record says why: the 2D relaxation
limit-cycles and its residual **grows** under refinement (Route-K, §32), so there is no
fixed profile to take a defect of, and `port_certification.radii_polynomial_status`
returns `BLOCKED_AT_STEP_ONE` by design. A fitness whose `Y₀` does not exist cannot be
validated at all.

Substituted: the **a = 0 CLM profile**, which carries four known answers where the 2D
object would have carried one.

**K1 — the exact profile is closed form.** `Ω₀(X) = −4X/(1+4X²)`, `H Ω₀ = 2/(1+4X²)`
(CLM 1985; HQW25 arXiv:2401.14615). It nulls the continuum residual identically, so every
defect measured here is ours.

**K2 — two knobs, two ladders, and both have the right sign.**

| `n` | `‖Ω − Ω₀‖_∞` | | `X_max` | `|c_ω + 1|` |
|---|---|---|---|---|
| 201 | 4.13e−05 | | 100.9 | 6.41e−03 |
| 401 | 2.59e−06 | | 745.2 | 8.71e−04 |
| 801 | 4.24e−07 | | 5506.6 | 1.18e−04 |

Refining the **spacing** converges the profile; refining the **reach** converges the
recovered constant, as `1/X_max` (7.4× of reach buys 7.4× of accuracy, twice over). These
are different knobs and they fix different things — the truncated Hilbert transform is
what holds `c_ω` back, and no amount of `n` touches it. `c_l` comes out at 1.0000018
(n = 401) without ever being told.

**K3 — an analytic wall.** `Ω₀ ~ −1/X`, so a weight `ν ~ |X|^(p+q)` gives the **true**
profile an infinite weighted sup norm as soon as `p+q > 1`. `p* = 1` exactly, derived,
not fitted. Gated: past the wall the norm grows with reach as `X_max^(p−1)` — measured
×7.39 against a predicted ×7.39 over a 54.6× reach.

**K4 — an exact invariance of the fitness itself.** Scale every weight by one constant
`s`: `Y₀ → sY₀`, `Z₁` unchanged, `Z₂ → Z₂/s`, so `budget → s·budget` and the ratio is
**invariant**. Verified to 4.4e−16. The overall scale of the norm is a gauge, not a
search direction — a searcher cannot win by making the norm big, and `w_ω = 1` is fixed
rather than searched because of it.

---

## 3. The premise reproduces — and the gauge is what carries it

Leg 46 reported **5186×** in `Y₀/budget` between a naive weight (`w_l = X_max`) and a
hand-tuned one (`w_l = 0.01 X_max`) on the HL object, and called it *"closure is a
property of the space, not of the object"*. That single table is the empirical case for
this whole stage, so it was pre-committed as a claim to be tested rather than assumed.

**On the known-answer object, the same one-constant change is worth 5604×** — naive
`+1.268` (does not close), hand-tuned `−2.480` (closes). The premise is not a one-object
accident.

**But the ablation says where it lives, and it is not the weight family.** Run the
identical weights on the same equation with the gauge changed — `c_l` pinned directly by
a border row instead of coming out implicitly — and the gain collapses to **0.56×**: the
"tuned" weight is now slightly *worse*.

The mechanism is visible in the constants. Pinning `c_l` makes that row of `A = DF⁻¹` a
unit vector, so the weighted operator norm never sees it; leaving `c_l` implicit puts
`‖A‖_w = 1.69e+08` at the naive weight against `1.69e+06` at the tuned one, a clean
factor of 100, and `Z₂` follows it. **The weight is not tuning a function space here; it
is preconditioning the border rows.** That is worth knowing before spending a stage
evolving weight families, and it is exactly the kind of thing a known-answer object with
a switchable gauge can tell you and a certified black box cannot.

---

## 4. The gate

Frozen predicate, `n = 201` against `n = 401`, 40-weight roster (2 controls, 6 designed
degeneracies, 32 random inside the box).

| | property | measured | threshold | |
|---|---|---|---|---|
| P1 | nonzero | 15.02 decades of spread | ≥ 1.0 | **PASS** |
| P2 | finite | 0.775 finite | ≥ 0.90 | **FAIL** |
| P3 | monotone | 0 violations; max |slope−1| = 0.366 | 0; ≤ 0.05 | **FAIL** |
| P4 | resolution-stable | Spearman 0.995, top-3 overlap 2/3 | ≥ 0.90; ≥ 2 | **PASS** |
| P5 | wide band | 15.02 decades | ≥ 2.0 | **PASS** |
| P6 | non-trivial optimum | interior margin 0.161; wall costs 1.5e−04 dec | ≥ 0.05; ≤ 0.05 | **PASS** |

**VERDICT FAIL. The GA was not run.**

### 4a. P3 — the failure is partly the probe's, and saying so is the point

The probe pushes the converged state off the solution by `ε` in a fixed direction. Since
`F(z*) ≈ 0`, `A F(z*+εd) = εd + O(ε²)`, so `Y₀` is linear in `ε` and the fitness must fall
with slope **exactly 1** per decade — a known answer, not merely a known direction.

It does not, at `ε = 10⁻²…10⁻⁶`. The diagnosis is `‖A‖`:

| `ε` | `‖A F(z+εd) − εd‖ / ε` |
|---|---|
| 1e−02 | 16.3 |
| 1e−04 | 4.39 |
| 1e−06 | 0.059 |
| 1e−08 | 0.0085 |

The linear regime does not begin until `ε ≲ 1/‖A‖ = 5.9e−07`. Inside the corrected
window `ε ∈ [10⁻⁹, 10⁻⁶]` the known answer comes back: **0 monotonicity violations,
median |slope−1| = 0.0018, worst 0.092** over 20 finite weights.

So P3 splits: **monotonicity passes, the slope-1 known answer passes at the median and
fails at the worst weight** against the frozen 5% threshold. The frozen predicate is
reported as it stands — `FAIL` — because retuning a threshold after seeing it miss is the
move this project keeps a plan-of-record to prevent. What the corrected window buys is
not a pass; it is a **number for how well the fitness tracks a defect**: to 0.2% typically
and 9% at worst, which is the resolution at which two weights can honestly be compared.

### 4b. P2 — the censoring is real, and it has a mechanism

Nine of 40 roster weights return no fitness. **Every one of them has `Z₁ ≥ 1`** — `A`
stops being an approximate inverse in that norm, so there is no budget at any residual.
All nine have far-field power `p+q ≤ −2.41`; the converse does not hold (a finite weight
exists at `−4.04`), because the two scales `L, l` decide *where* the decay begins. And
**no censored point lies within 10% of the box near the optimum** (0 of 400 sampled).

The censoring is therefore informative rather than pathological — but the frozen
threshold was 0.90 and the measurement is 0.775, and a fitness that is undefined on 22%
of its own box is not one to hand an optimizer without carrying that boundary explicitly.

### 4c. What P4 passes, and what it does not cover

P4 as written asks whether the **ranking** survives refinement. It does, comfortably:
Spearman 0.995 between `n = 201` and `n = 401`. The **level** does not, and the gate never
asked it to — see §5, which is the leg's most consequential number.

### 4d. The substantive diagnostic

Gate 4's lesson was that a 6/6 can still be a false pass and that what catches it is a
correlation nobody gated. Run here: the best single-gene predictor of the roster fitness
explains `R² = 0.163` (`log₁₀ w_l/X_max`), and the far-field power `p+q` explains 0.211.
**No single coordinate organizes this landscape** — which is the opposite of the `ν_crit`
failure, where `max|ω₀|` explained 75%. This landscape is genuinely five-dimensional.

---

## 5. Two walls, and only one of them is mathematics

The analytic wall `p+q ≤ 1` was known before the run. Whether anything else bounds the
search space was a measurement — bisect the far-field power on the single-power slice
`ν = (1+X²)^(p/2)` and find where `Z₁` crosses 1:

| `n` | lower wall `p₋` | `Z₁` at `p = 0` | fitness (leg 46's weight) | closes? |
|---|---|---|---|---|
| 201 | **−3.684** | 9.92e−09 | **−2.480** | ✓ |
| 401 | −2.854 | 1.25e−06 | +1.490 | ✗ |
| 801 | −1.640 | 4.13e−04 | +5.381 | ✗ |
| 1601 | −1.003 | 7.55e−02 | +7.933 | ✗ |
| 3201 | **≥ +3** | **1.64e+01** | `+∞` | ✗ |

**The admissible band is `(p₋, 1]`, and it shuts.** At `n = 3201` there is no weight at
all: `Z₁ > 1` everywhere on the slice, and the Newton solve itself has degraded to a
residual of 1.3e−10. The lower wall is not a property of the equation — it is the float
rehearsal's conditioning, `κ(DF)·ε_mach`, and it climbs until it meets the analytic wall
from below.

**The certificate on this object closes only at the coarsest grid.** That is the honest
reading of row 1 against rows 2–5, and it re-prices two things at once. It says the
5604× of §3 is measured where `Z₁` is 1e−09 and therefore where the weight is fighting
`Y₀` and `Z₂` alone. And it puts a number on why stage `L1` needs interval arithmetic
rather than more care: **the float stand-in for `Z₁` fails at a measurable resolution**,
and on this object that resolution is ≈ 3.2e+03.

---

## 6. The search, and what it actually bought

Deterministic grid, five genes, 295,245 evaluations. `ν(X) = (1+(X/L)²)^(p/2)
(1+(X/l)²)^(q/2)`, the discrete cousin of Chen–Hou's "different powers".

| weight | `Y₀` | `Z₁` | `Z₂` | `‖A‖_w` | `Y₀/budget` |
|---|---|---|---|---|---|
| naive (`w_l = X_max`) | 3.40e−09 | 9.92e−07 | 2.72e+09 | 1.69e+08 | **18.6** ✗ |
| leg 46's hand constant | 3.40e−11 | 9.92e−09 | 4.86e+07 | 1.69e+06 | **3.31e−03** ✓ |
| **searched** | 4.57e−12 | 4.24e−09 | 4.21e+07 | 3.37e+05 | **3.84e−04** ✓ |

`θ* = (p, log₁₀L, q, log₁₀l, log₁₀(w_l/X_max)) = (−1.788, −0.750, 2.711, −0.274, −2.878)`
— **48,270× over the naive weight and 8.61× over the hand-tuned one**, interior in every
gene (margin 0.161), and with far-field power 0.923, inside the analytic wall. Removing
the wall entirely moves the optimum by 1.5e−04 decades: **the wall never binds on this
object**, which is worth recording because it was the one constraint the plan told this
stage to respect.

Where the 8.61× comes from is not where a reader would guess. The searched weight's
`budget` is barely better than the hand-tuned one's (1.19e−08 against 1.03e−08); `B` is
4.3× **worse**. The entire win is `Y₀`, 7.45× smaller, bought by shrinking `‖A‖_w` a
further 5× with `w_l ≈ 0.99` — a factor 750 below `X_max`, where the hand had stopped at
100. **The hand was searching the right direction and stopped early.**

---

## 7. What this does and does not mean

**Does:** the fitness is one number, it is gauge-invariant, it tracks a known defect to
0.2%, its landscape is genuinely five-dimensional, and a deterministic search beats the
best hand-picked weight this project has by 8.6× on an object whose answer is known.

**Does not:** pass its own viability gate. Two of six properties fail on the frozen
predicate, and per the plan of record the GA does not run and stage `B` does not start.
The repairs are named and neither is research: carry the **measured** lower wall in the
box as the analytic one already is (P2), and state the fitness's defect-tracking accuracy
as a resolution rather than assuming it is exact (P3).

**And the ceiling.** No link of the `L1→L4` chain moved. The object is CLM, in closed
form since 1985; nothing here is certified, and no novelty is claimed for the idea of
searching a certificate. What the leg produced is a measurement about a **method**, taken
where the answer was checkable — which is what a pilot is for, including when it says no.
