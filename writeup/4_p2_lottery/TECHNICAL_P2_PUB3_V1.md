# Thirteen escalations in one cycle: what an adversarial audit family found, and what it did not

**Route PUB3, leg 223, v1. DRAFT — for the user's review. This leg's landing does not approve it.**

**Status.** Third publication-scoping bundle, after leg 179 (`ℓ¹_w`-death) and leg 186
(space-axis). Unlike both of those, **this note contains no certificate mathematics**. It is
about the audit family's own hit-rate discipline: what happens when you point adversarial and
degenerate input at the modules underneath a research codebase's banked claims, and — the part
that is actually load-bearing — how you decide whether any published number moved.

**What this note is not.** It is not a claim that any link of this project's `L1 → L4` chain
moved. None has, in 223 legs. It is not a security or reliability audit of a shipped product.
And, stated first because it is the most important disclaimer, **its general thesis is not
new** — see §0.

**Provenance.** Every magnitude is read from the escalating leg's own banked journal or JSON on
its own branch, or from `experiments/JOURNAL.md`'s orchestrator-audited pointer. Sources are
named inline. Where two banked sources disagree, **both numbers are printed** and the
disagreement is named rather than resolved (§6). The provenance rules were pre-committed in
[`writeup/novelty/leg_223.md`](../novelty/leg_223.md) before this file was written.

---

## 0. The general claim is not novel, and the note is written to a published standard

The tempting headline — *adversarial input against numerical modules reliably surfaces latent
defects that ordinary use never triggers* — is established prior art. Four literatures own it
already:

- **Silent bugs as a named class.** Wrong behaviour with no crash, no hang and no error
  message is a catalogued category with its own incidence studies
  ([arXiv:2112.13314](https://arxiv.org/pdf/2112.13314)).
- **Numerical bugs in exactly this dependency stack.** Franco et al.'s 269-bug dataset is drawn
  from six libraries including NumPy, SciPy and LAPACK.
- **Why construction-time testing misses them.** The oracle problem: for most numerical code
  there is no independent ground truth, so absolute oracles are unavailable and testing must
  use metamorphic relations instead
  ([Kanewala & Bieman, STVR 2016](https://onlinelibrary.wiley.com/doi/10.1002/stvr.1594)).
- **The standard this repository is answerable to.** The computer-assisted-proof literature
  already states in print that *any computer-assisted proof implicitly carries as a hypothesis
  the statement that the software encountered no bugs*, and carries the cautionary cases —
  five papers retracted from a single software bug; a sign error reversing an influential
  economics result ([arXiv:2502.07850](https://arxiv.org/pdf/2502.07850)).

So the finding here is **not** that the defects exist. It is the ledger: a per-cycle census of
a claim-bearing research codebase in which every defect is graded by a pre-committed question —
*does this move a banked number?* — rather than by severity-to-the-code. None of the four prior
literatures grades on that axis. That is a bookkeeping contribution and is claimed as nothing
more.

---

## 1. The census, and the inclusion rule

**Inclusion rule, stated so the count is auditable:** a leg counts as an *audit-family
escalation this cycle* if (a) its work was an adversarial/degenerate-input audit of a `solver/`
module, a consistency audit of a shared ledger, or a repair leg closing one of those findings,
and (b) it ended **parked on its own branch with `main` untouched** rather than landing.

**Count: thirteen.** Not seven.

The dispatch that commissioned this note named seven (188, 198, 199, 200, 201, 204, 205) and
warned that the number had grown. It had — by six. §7 explains why the number was stale, and it
is not because anyone was careless.

**One escalation is deliberately excluded, and named so the exclusion is auditable:** leg 211
(XU11) escalated this cycle, but it is a *literature* cross-validation (Xu arXiv:2607.19762
against leg 185's `a* = 0.38649640`), not an input audit. It is not counted, and the count
would be fourteen under a looser rule.

**Two audit-family legs are not escalations and are counted separately:** legs 206 (GSA) and
207 (DPA) found real defects and **landed directly**, judged not claim-adjacent. They belong in
the denominator, not the escalation list — see §5, where they matter a great deal.

| # | leg | route | module | contamination status |
|---|---|---|---|---|
| 1 | 188 | SURV | dealias floor, 4 modules | *not a contamination question* — a pending ruling |
| 2 | 198 | BHA | `bordered_hl.py` | zero banked impeached (magnitude contested, §6) |
| 3 | 199 | CGA | `certificate_guards.py` | zero banked impeached |
| 4 | 200 | PCA | `port_certification.py` | zero banked impeached |
| 5 | 201 | ICA2 | `interval_certificate.py` | zero banked impeached |
| 6 | **202** | **PNA** | **`profile_newton.py`** | **MATERIALLY EXPOSED — Route-D v11** |
| 7 | 203 | RSA | `rescaled_spectrum.py` | **claim-adjacent**, no number confirmed wrong |
| 8 | 204 | TNA2 | `target_norm.py` | zero banked impeached |
| 9 | 205 | BVR | `boussinesq_rescaled.py` | **UNCERTAIN — never re-run** |
| 10 | 208 | TSA | `target_selection.py` | zero banked impeached |
| 11 | 209 | SCA2 | `spectral_certificate.py` | zero; **proof confirmed safe** |
| 12 | 213 | LGC2 | `literature_gates.py` (ledger) | zero (cosmetic) |
| 13 | 215 | CGR | `nk_bounds.py` (repair) | zero; **repair incomplete, 1 of 16** |

**Critical, and verified at write time rather than assumed: not one repair leg has landed.**
`git log origin/main` carries no `Leg 216/217/218/219/220/221/222/225/226` commit. Legs 218 and
221 have pushed a novelty pass only; 217, 219, 220, 222 and 225 have branches sitting at their
base commit with no leg commit at all. **Every "zero" in the table above is therefore the
finding leg's own measurement, independently re-confirmed by nobody.** That is a weaker
epistemic state than "confirmed zero" and the note does not use that phrase.

---

## 2. The twelve module audits, and what each actually measured

### 202 (PNA) — `profile_newton.py`. The one that is different in kind.

**This is the only item this cycle that materially exposes a banked claim, and it is not
softened here into "latent" for symmetry with the others.**

`continuation` returns off-branch, grid-scale spurious roots as `converged=True`, satisfying
**both gauges to `0.0e+00` exactly** and every residual row to machine precision. The module
computes no decay-class or smoothness diagnostic, so a lattice artifact is indistinguishable
from the physical branch **in every field the module returns**.

| | `a` | `n` | `converged` | `relres` | far-field sup | inflation vs anchor |
|---|---|---|---|---|---|---|
| first departure | 0.45 | 101 | **True** | 1.77e-15 | 1.35e-02 | **2079×** |
| worst | 1.05 | 101 | **True** | 4.17e-16 | 9.02 | **1.39e+06** |

At `a = 1.05` the returned profile's supremum is attained **at the domain edge**, 9× larger
than at the origin, with node-to-node oscillation 0.80 against the anchor's 0.09 — and it is
reported with a *better* residual than the physical branch has. The banked consequence:
`c(a = 1.50)` returns **0.20427 / 0.23717 / 0.97282** at `n = 101 / 201 / 301`, all three
`converged=True` at machine zero (6.0e-16 / 5.8e-16 / 4.1e-15). **376% between the extremes**,
and grid refinement does not close them, because they are different branches.

**The delivery vehicle is the rescue clause.** When the warm start stalls, `continuation`
retries from the cold anchor and accepts the result because `alt["relres"] < r["relres"]` —
which the spurious root satisfies *better than the physical branch does* — then re-seeds the
whole remainder of the ladder from it. A clause written to make the sweep robust is what walks
it off the branch and keeps it off.

**Exposure, from leg 202's own `git grep`, not from its dispatch's candidate list:**

| consumer | exposure |
|---|---|
| **Route-D v11** (`p2_route_d_v11_anchor.py`) — banks `a_max_machine`, `grid_converged_a_max`, `GA_boundary` on a `relres < 1e-8` verdict | **DIRECT AND MATERIAL.** Its own banked `v3_boundary` shows the signature: `relres` oscillating 1e-14 → 1e-7 → 1e-14 as `a` rises (`a = 0.54–0.60` fail, then `0.62/0.64` "converge" at 1e-14) — a branch jump, not a boundary. |
| **Route-D v12** (`p2_route_d_v12_defect.py`) — consumes `sol["relres"]`, `sol["c"]` at `a ≤ 0.55` | **PLAUSIBLY EXPOSED** at its upper rows; M1's first measured departure is `a = 0.45`. **Not re-run.** |
| Route-ASA (leg 122) | **NOT materially affected** — checked, not assumed: substrate is `a = 0.0`/`0.3`, on-branch at every grid measured. |

**The second consumer is recorded here because the shared ledger omits it.**
`experiments/JOURNAL.md`'s pointer and every DM summary name Route-D v11 only. Route-D v12's
plausible exposure appears solely in leg 202's own journal. It is an open, un-re-run question.

**The corroboration that makes this hard to argue with:** Route-D v11 *already computed the
diagnostic that catches this*, externally, as a `weighted_defect`, and banked values that blow
up exactly where leg 202 measures the departure — **0.50 at `a = 0.5`, 4788 at `a = 0.8`,
73372 at `a = 1.0`**. The information needed to reject those profiles was sitting in the
caller's own JSON and never reached the module's verdict, because the diagnostic lived in the
experiment and never in the module. That is the finding, and it generalises past this module.

**Repair leg 226 (PNR) is drafted and ranked first in the whole backlog — and has not been
dispatched.**

Two further mechanisms, latent: **M2**, a small-amplitude start escapes the scaling family at
*default* parameters (`Ω(0) = −0.750000` not −1, gauge residual 0.25, `c` wrong by up to
**6.15e+05×** and a sign, with `c ~ 1/eps` exactly identifying the mechanism as the scaling
degeneracy rather than roundoff); **M3**, `c0` never range-checked — `solve(c0=1e9)` hands
`1e9` straight back as a converged wave speed.

### 203 (RSA) — `rescaled_spectrum.py`. Claim-adjacent, and stated at exactly its own weight.

Eight mechanisms. **R1**: `converged_spectrum` has no guard on `K_fine` vs `K_coarse`, so the
degenerate comparison certifies the entire continuum — `n_kept` goes from the correct **2 to
all `K`** (24/24 at `K = 48`, a **24×** inflation), every match distance identically `0.0`,
including a spurious **±40.4623i** pair — the exact Hopf-crossing signature the module exists
to rule out. This is lesson 90 in the module's own code.

**R2 is the claim-adjacent one, and leg 203's own journal marks it `NOT LATENT`.** `spectrum`
and `converged_spectrum` discard `newton`'s `converged` flag; the worst silently-accepted
iterate sits **2.632e-01** from the exact −1 and puts **44 eigenvalues in the right half plane
(max Re +0.3437)** where the truth has none. **5/7 banked Route-E `E5_sweep` rows** (residuals
6.187e-04 … 1.135e-02) and **7/7 banked Route-G `g4_cross_model` rows** (9.094e-05 … 2.275e-03)
were computed at points whose residual exceeds the module's own 1e-8 threshold.

**Two things cut the other way and are stated because they do:** both routes banked their
residuals alongside their values, so the condition is discoverable from the JSON and was never
hidden; and both are already flagged `converged=False` by the module's own separate,
conservative check. **Leg 203 explicitly does not claim any banked number is wrong** — the sign
and size of any resulting error in those rows is *not measured*, and the one place it could be
checked cheaply (`a = 0.5`) comes out right to 8 digits. The exposure is that those rows are
*discoverably less precise* than a bare convergence label suggests. Repair leg **225 (RSR)** is
dispatched; its branch carries no commit.

### 205 (BVR) — `boussinesq_rescaled.py`. The uncertain one.

Two independent, separately-confirmed silent-fabrication mechanisms in `odd_field_x_slope`.
**Defect A** (second occurrence of leg 99's class, at the exact line leg 99 flagged and
declined to test): an empty fit window sends `lstsq` to return exactly **0.0 against truth
2.0**, 2000× tolerance. **Defect B is the alarming one and is new**: a hard-coded absolute
`r_win = 0.4` with a discarded `lstsq` residual drives `modulation()`'s `c_l` to **+0.188
against truth 1.4** — 86.5% error, 1731× tolerance — **on a fully resolved grid, with rank and
condition number constant throughout**. Leg 99's own fix is provably blind to B.

**Contamination status: UNCERTAIN, and it is not written as zero.** Leg 205's own journal is
explicit: *"This leg did not re-run any banked result and does not claim any banked number
moves."* The unguarded reduction is public and called outside `modulation` by
`p2_route_l_v1_precond.py:222-229` (which additionally *divides* by its return value) and by
`spike1_stepB_evidence.py:84-85`. Whether the Spike-1 Step-B/C numbers were computed on fields
concentrated enough for B to bite *is a separate question needing its own leg*; the profiles in
play use `exp(-r²)`-class envelopes, i.e. the safe scale, which the leg calls **"a reason to
expect no movement but not a measurement of it. Flagging, not claiming."** Repair leg **221
(BVRR)** carries the re-confirmation in its own gate; it is live and has committed a novelty
pass only.

### 198 (BHA) — `bordered_hl.py`. Largest nominal magnitude; contested (§6).

A negative border weight is accepted with no check, and `induced_sup_norm` can return a
**negative "operator norm"** — −1.0 to −4.0e9 on hand-checked cases whose true weighted norm is
**101.0**. The same-magnitude sign flip corrupts `Z₂` by up to **1.189e17×** and can flip a
certificate's own closure verdict (no root → root at 2.217e-11). Three further silent sites
(permuted-grid `velocity_matrix`, arity-truncating pin, NaN-dropping `tail_exponent` mask).
Zero banked numbers impeached: no live caller passes a negative weight.

### 199 (CGA) — `certificate_guards.py`. 16/67 silent accepts, four mechanisms.

**M1**, the headline: four of the five exported guards test finiteness explicitly;
`unit_range_violation` does not, and `nk_bounds.py:430` asks it for a **closed lower endpoint
at minus infinity**, so the test is `-inf < -inf` = `False` and **`alpha = -inf` is
admissible**. At the consumer, `farfield_modelling_error_bound(-inf, 0.5, 1.0)` returns
`bound = NaN`, **40 of 40 window samples NaN, and does not raise** — against an honest
`2.537396530974982` at `alpha = 1.5`. The localisation is itself a gate: the *same function*
refuses both infinities at the `gamma` site, where the endpoint is finite. Zero banked numbers
impeached — **8/8 live alphas lie in [1.1, 1.8]**.

Also: **M2**, `radius_violation` accepts `'0.5'`, `Decimal('0.5')`, `Fraction(1,2)` and `True`
as admissible radii (4 of 4) while its sibling refuses 2 of them; **M3**, `bool` is
`numbers.Real`, so `gamma=True` returns a claimed upper bound **1.2605493138651522× smaller**
than at the live `gamma = 0.5`, and `budget(Y_0=False, …)` narrates the boolean into a
mathematical claim; **M4**, a negative rational underflows to `-0.0` before the sign test —
real accept, **magnitude ≤ 1 ULP**, and leg 199 pins it at that weight rather than inflating
it; **M5**, the empty container is a vacuous pass in two guards.

### 200 (PCA) — `port_certification.py`. Four mechanisms.

`radii_polynomial_status` returns `closes=True` on a ball of radius **exactly 0** at `Y_0 = 0`
(leg 51's own `a=0` CLM value) — it reads the discriminant alone and never forms `r_min`.
`line_sweep_solve` inverts a **different operator** when `s_rho < 0` (**18820×** relative
error, no exception); `leading_order_solve` truncates integer rhs (relative error **1.000**);
`stall_verdict`'s `NaN < 2.0` gives poisoned ladders a confident "bending" verdict. **Two of
the four are catchable by guards that already exist in-repo and are never called here.** Zero
banked numbers move: the live PORT run's `min(s_rho) = 0.3896 > 0` sits in the corner where all
four are dormant.

### 201 (ICA2) — `interval_certificate.py`. An unrepaired clone of leg 69's defect 1.

`matmul_point_interval` silently returns a **non-containing enclosure** in the subnormal band —
containment escape **200 η = 24.63%** of the returned magnitude at the shipped `BorderedHL
N = 405` — driving `Y₀` **19.66% below the quantity it claims to upper-bound** while still
flagged `rigorous=True`. A repaired sibling routine encloses at 0 η on identical input. Zero
banked numbers wrong: the live minimum row mass sits **292.9 decades** above the failing band.

### 204 (TNA2) — `target_norm.py`. A guard that defeats three legs of prior guard work.

The domain guard windows on `max|X|` rather than the true data interval, so an asymmetric grid
silently extrapolates **535 of 16384** θ-samples while reporting `n_outside_grid = 0` and
`domain_valid = True`. Result: `p = -0.0889` against exact **1.4** — a **386× systematic error
of the wrong sign** — defeating legs 55/84/94's guard work while reporting clean. Three further
silent-wrong mechanisms (`frac_outside_grid` threading; a negative `analytic_tail` bound with
`finite=True`; `fit_exponent` overstating `n_points` 3.0× when dropping NaN bins). **0 of 7
mechanisms reachable from the banked call path** — leg 55's `+0.394`/`+0.094` margins
uncontaminated.

### 208 (TSA) — `target_selection.py`. The sixth uncensused guard-class member.

`certificate_guards.py`'s own docstring claims to cover every function of this class; this one
was never on the list. **9/9 forbidden `(Y₀,Z₁,Z₂)` triples return `feasible=True`**, five with
a *negative* certified radius (worst **−1413.71**); `y0_budget(2.0,1.0) == y0_budget(0.0,1.0)
== 0.5` bit-for-bit against a true budget of **0**; `unknowns()` understates the dim-2 count by
**598.5×**. Latent: 85/85 banked `Z₁` records lie in `[0,1)`. Checked and confirmed, not
assumed: leg 63's "exactly one candidate passes" and the whole `γ = 2` line (63/125/174/185/
187/193) are **not** at risk — that predicate lives on a disjoint, parked branch this defect
never touches.

### 209 (SCA2) — `spectral_certificate.py`. The module Theorem NGX is proved against.

Four latent mechanisms. Headline: an unordered NaN comparison (`nan > 0` is `False`) sends
`sigma_min` from **0.0349 to +inf** and inverts `counterexample_norm_floor` from **14.3206 to a
plausible-looking 0.0** — exactly the theorem's own conclusion, reversed. **The proof is
confirmed safe, and this is the careful part:** measured rather than assumed, 0 shipped
`(class, param)` pairs produce NaN/Inf or a negative weight, the nearest shipped `s` is
**0.263852** clear of the failing band, and clean-input float64 matches exact rational
Gauss–Jordan to **7.24e-16**. Theorem NGX rests on an exact folklore inequality and an analytic
tail estimate; neither touches this code path. The theorem is untouched — only the numerical
module has an adversarial-input gap.

### 206 (GSA) and 207 (DPA) — the two that landed directly

Counted in the denominator (§5), not in the escalation list.

**206** — `ga_search.py` returns a wrong value on **12 of 41** adversarial cases across six
mechanisms (a `-inf` optimum demoted to worst rank; a NaN gene surviving in a "converged"
individual at finite fitness; inverted bounds collapsing offspring onto a point; `elite_frac ≥
1` freezing the breeding loop at **864347×** worse while reporting 40 generations). All six are
orthogonal to the standing GA ban, and all 9 live call sites were audited safe by static AST
parse.

**207** — `dissipative_profile.py`, 4 latent sites. Most severe: `Y₀`/`Z₂` are measured at the
constructor's *stored* `a`, not the solved one — inflation up to **1.144e+12×** when they
drift; and a zero profile silently echoes Chen's exact `Δ = −1/3` at `residual_rms` exactly
`0.0`, with no health indicator distinguishing it from real convergence. A static call-site
audit of legs 125/185/187 found 0 exposed sites.

### 188 (SURV) and 213 (LGC2) and 215 (CGR) — the three that are not module audits

**188** is a *necessity* audit, and its status line is not a contamination claim. Its gate
answered **(a) FORCED, (b) NO**: `n = 3`'s exclusion under the strict Bowman 2/3 rule is
mathematically forced. Its real contribution is a **correction to the scope of escalation #4**,
and the correction runs in the direction people do not expect — leg 129's blast radius is
**wider** than originally scoped, not narrower. Four solver modules consume the two masks leg
129 touches (`gclm.py`, `fractional_gclm.py`, `fractional_boussinesq.py`, `boussinesq.py`), and
critically **`solver/gclm.py` has no grid guard at all** — `solve_gclm(n=3)` runs clean today
and would raise post-repair. So the ruling the user owes is about a **four-module refusal
boundary, one of them going from unguarded to raising for the first time**, not a single
Boussinesq verdict.

Leg 188's own novelty pass also caught its dispatch's premise being false before running: the
dispatch asserted the strict rule was "already used elsewhere, e.g. leg 120's own repair", but
**leg 120 wrote no repair** (it escalated, unpatched), and `grep -rn "// 3" solver/*.py`
returns nothing — **no shipped module on `main` uses the strict cut**. It survives only in the
adversarial batteries, which *pin the loose cut as a measured defect* rather than adopt the
strict one. Leg 188 is also the one escalation with **no journal file on its branch** — only a
runner and a novelty pass — so its record lives in DM prose rather than in a leg artifact.

**213** is a ledger-consistency audit and its finding is cosmetic and honestly labelled so:
`EGM_PRIMARY_READ`'s own `sign_correction_leg_190` field describes 5 prose sites as still
carrying the wrong bracket — true when written, false since leg 214 fixed all five
(`2c901c4`). The ledger's claim about the repository's current files is backwards. **0 banked
numbers move**; a one-tense-word fix (reserve leg 227).

**215** is a *repair* leg whose gate answered **NO**, and it is in this list because it escalated
rather than landing. The one-line `isinf` repair at `nk_bounds.py:430` closes leg 199's M1
cleanly — `alpha=-inf` now raises, **8/8 live call sites bit-identical at 0 ULP**. But **M1 is
only 1 of the 16 gaps leg 199 found**; the other 15 live in `certificate_guards.py`, outside
leg 215's territory. **The repair is sound; the gate's premise is what failed** — that all 16
were the missing-`isinf` family. Leg 216 (CGF) owns the remainder and has not started.

---

## 3. The distribution, which is the actual result

Twelve legs this cycle ran a gate of the form *"under adversarial and degenerate input, does
this module ever silently return a wrong value rather than reject or visibly propagate?"* —
legs 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209.

**All twelve answered YES.**

That is the number worth publishing, and it needs stating carefully, because it is a claim
about **this codebase**, not a discovery about method (§0). Twelve modules were selected as
load-bearing and audited; twelve had at least one mechanism that returns a finite, plausible,
wrong value with no exception, no warning and no flag. Several had four to eight. The prior
selection was not adversarial — these are the modules underneath banked results, chosen for
being load-bearing rather than for being suspect.

Against that, the grading:

| grade | count | legs |
|---|---|---|
| materially exposes a banked claim | **1** | 202 |
| claim-adjacent; no number confirmed wrong | **1** | 203 |
| contamination never measured (uncertain) | **1** | 205 |
| zero banked numbers impeached, per the finding leg's own measurement | **9** | 198, 199, 200, 201, 204, 208, 209, 213, 215 |
| not a contamination question (pending ruling) | **1** | 188 |

**Both halves matter, and reporting either alone would be dishonest.** A 12/12 defect rate with
a 1/12 material-exposure rate is a different story from either number by itself. The
contamination discipline — measuring reach at live parameters instead of reasoning from
severity — is what separated them, and it repeatedly reversed the intuitive ranking: leg 198
has the largest nominal magnitude in the cycle (`Z₂` to 1.189e17×) and contaminates nothing,
while leg 202's mechanism produces *machine-zero residuals* — the most innocuous-looking
diagnostic possible — and is the one that reaches a banked headline.

**The mechanism behind that inversion is worth naming.** In every latent case, the defect
needed an input no caller produces: a negative weight, `alpha = -inf`, a subnormal row mass, an
asymmetric grid, `s_rho < 0`. Leg 202's needed nothing — it fires on the module's own default
path, on a warm start, at a parameter the caller genuinely sweeps. **Reachability, not
magnitude, is the variable that predicts contamination**, and it is cheap to measure and was
measured in eleven of twelve cases.

The twelfth is leg 205, and its absence is exactly why its status stays UNCERTAIN.

---

## 4. What the discipline caught that a severity ranking would have missed

Four cases where measuring reach changed the answer:

1. **Leg 209 separated the module from the theorem.** The mechanism reverses Theorem NGX's own
   conclusion (`counterexample_norm_floor` 14.3206 → 0.0). A severity ranking stops there. The
   leg instead established that the theorem rests on an exact folklore inequality and an
   analytic tail estimate, **neither of which touches this code path** — so the proof is
   untouched and only the numerical module has a gap.
2. **Leg 208 checked the γ=2 line rather than assuming it.** The natural fear — leg 63's
   "exactly one candidate passes" — was confirmed safe because that predicate runs on a
   disjoint, parked branch the defect never reaches.
3. **Leg 199 declined to inflate M4.** A real silent accept whose magnitude is **≤ 1 ULP**,
   reported at that weight and explicitly flagged as unreachable from float64.
4. **Leg 202 rejected its own dispatch's candidate list.** The brief named legs 125/185/187;
   `git grep` showed none of them imports the module, and leg 202 recorded leg 187's status as
   *unresolved-at-merge-base* rather than absent, because 187 was in flight elsewhere. It then
   found the real consumers itself.

And one where it cut against the leg's own convenience: leg 202 also recorded a correction
against its **own** intermediate scouting note, in the artifact rather than quietly dropping it.

---

## 5. Where the banked record disagrees with itself

Printed rather than resolved, per this leg's pre-committed provenance rule.

**(a) Leg 198's `Z₁` ratios are contested by leg 218's in-flight re-measurement.**
Leg 198 reports `Z₁` corruption up to **1.198e9×**; leg 218's novelty pass — re-running both
modules in the same process — measures **2.287e8×**, a factor **5.24×** apart, and **1.505e12
vs 2.651e12** (1.76×) on the second case. Leg 218's own explanation: `Z₁ = ‖I − A·DF‖` with
`A = inv(DF)` is a near-total cancellation whose honest and flipped values (5.518e-09,
5.099e-15) **both sit at the round-off floor**, so the *ratio* is environment-dependent while
the *verdict* is not — lesson 86. Leg 198's `‖A‖` (6.671e9×, 6.066e10×) and `Z₂`
(+1.188608e+17 / −1.779456e+07) columns reproduce **exactly to 4–6 s.f.** Neither number is
adopted here; the verdict (a sign flip corrupts these constants catastrophically) is not in
dispute, and the contamination status (zero) is not affected.

**(b) The DM's blast-radius framing for leg 198 is measured false.** DIRECTION.md ranks 218
first "given that this module sits directly upstream of every bordered-certificate battery this
repository has run (54, 58, 127)". Leg 218 measured it: **legs 54/58/127 do not import
`solver/bordered_hl.py` at all** — 0 of 7 of their runners/evidence files mention it; they rest
on `solver/spectral_certificate.py` via `p2_route_tc_v1_assemble`. Answering the gate's clause
(b) on those three would have been a lesson-90 tautology. The live caller set, enumerated by
import, is `port_v1`/`port_v2`/`l1_v1`/`l1rh_v1` plus two test files, **every one of which
passes `w_om = w_r = 1.0`**. The priority ranking stands on other grounds; its stated reason
does not.

**(c) Route-D v12's exposure is absent from every shared ledger.** §2 above. It appears only in
leg 202's own journal and has not been re-run.

**(d) One "the fix is one line" estimate was wrong by 15/16.** Leg 199's report stated its M1
fix was a one-line `isinf` check. It was — and closing M1 closed **1 of 16** gaps (leg 215).
The estimate was accurate about the line and misleading about the finding.

---

## 6. Why the count was stale, which is a finding about the process

The dispatch commissioning this note named **seven** escalations. The true figure at write time
is **thirteen**. The cause is structural, not carelessness, and it is worth recording because
it is the kind of defect this cycle's own audits were looking for — in the bookkeeping rather
than the code.

`DIRECTION.md` states **26 times** that escalations are "recorded in `PROGRESS.md`'s NEEDS
YOU". **`PROGRESS.md` is not in the repository.** `.gitignore:33` excludes it by design, with
the comment *"PROGRESS.md is rewritten every cycle (the committed snapshot is
reports/STATUS.md)"*. No commit in the repository's whole history has ever touched it.

So the committed register is `reports/STATUS.md` — whose header reads *"committed snapshot
(sections 1-3 of PROGRESS.md)"*. It was last refreshed at commit `4b6f4d8`, with the summary
**"6 landings, 3 escalations"**, and its NEEDS YOU section lists exactly three: 188, 199, 198.
`main` has since advanced to `b8eae4f` and the escalation count has gone from **3 to 13**.

**The only committed escalation register is stale by ten items, including the one materially
exposed banked claim.** Anyone reconstructing the backlog must instead read `DIRECTION.md`'s DM
narrative and `experiments/JOURNAL.md`'s pointers in commit order and take the union — which is
what this leg did, and which is why the count moved by six.

This is a bookkeeping observation, not a criticism of any leg: every individual escalation was
recorded correctly *somewhere*, each in at least two places, by legs and an orchestrator working
exactly to spec. What is missing is a single committed place where they are recorded *together*.
The audit family found silent-wrong values in twelve of twelve modules by asking what happens
under input nobody expected; the same question asked of the process finds a register that
silently reports 3 when the answer is 13.

---

## 7. The honest ceiling

- **No link of the `L1 → L4` chain moved.** Not in this cycle, not in 223 legs. Clay stays at
  **~0.05%**, behind Walls 1 and 2.
- **Nothing here is a positive result about the mathematics.** The best case for a repaired
  module is that a guarantee is restored, not that a margin improved.
- **The 12/12 rate is a statement about this codebase**, from a sample of twelve
  non-adversarially-selected load-bearing modules in one repository. It is not an estimate of
  any population rate, and §0's prior art already establishes the phenomenon generally.
- **Nine "zero contamination" statuses rest on the finding leg's own measurement**, since no
  repair leg has landed and none has independently re-confirmed one.
- **One status is uncertain (205) and one is materially exposed (202).** Neither is written as
  zero anywhere in this note.
- **Whether Route-D v11's headline survives is open**, and cannot be settled from here. It
  requires leg 226's re-derivation using a repaired module. Leg 226 is ranked first in the
  entire backlog and has not been dispatched.

---

## Provenance table

| claim | read from |
|---|---|
| 202's mechanisms, tables, exposure, v12 | `experiments/journal/leg_202.md` @ `origin/leg/202-pna-v1` |
| 203's R1–R8 table, R2 `NOT LATENT` | `experiments/journal/leg_203.md` @ `leg/203-rsa-v1` |
| 205's "flagging, not claiming" | `experiments/journal/leg_205.md` @ `leg/205-bvr-v1` |
| 199's M1–M7, blast-radius table | `experiments/journal/leg_199.md` @ `leg/199-cga-v1` |
| 198's magnitudes | `experiments/JOURNAL.md` pointer (leg 198 entry) |
| 198's contested `Z₁`, caller set | novelty commit `7a32718` @ `leg/218-bhr-v1` |
| 188's premise correction, loose-cut grep | `writeup/novelty/leg_188.md` @ `leg/188-surv-v1` |
| 188's 4-module scope | `DIRECTION.md` DM update (no leg journal exists on 188's branch) |
| 200, 201, 204, 206, 207, 208, 209, 213, 215 | `experiments/JOURNAL.md` orchestrator-audited pointers |
| repair-leg landing status | `git log origin/main`; branch tips for 216–222, 225 |
| register staleness | `.gitignore:33`, `reports/STATUS.md` header + NEEDS YOU, `git log --all -- PROGRESS.md` (empty) |
