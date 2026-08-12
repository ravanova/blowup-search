# Route-DTOR v1 (leg 390) — does Fefferman statement (D) delete `CLAY_OBLIGATIONS` §4, or re-price it?

**Gate, in the gate's own wording.** *Does the (D)-variant ledger re-derive with every §1–§5
obligation either named-as-vacated or priced-as-transferred, AND does the §2 enumeration close with
each row's ℝ³-only/carries-to-T³ verdict tied to its landed record?* — **YES.**

**CEILING: TIER 2**, in this branch and in the other one. §6's two no-method obligations stay
**OPEN**. No link of the `L1 → L4` chain moved. **Clay stays ~0.05%.**

> **THE RETARGET DECISION IS THE USER'S AND THIS LEG MAKES NONE.** This leg prices an option; it
> does not exercise it. Nothing below is a recommendation and nothing below should be read as one.
> The magnitudes point in both directions and they are reported at the same strength in both.

* Runner: `experiments/p2_route_dtor_v1.py`
* Ledger: `writeup/data/p2_route_dtor_v1.json`
* Evidence script (rebuilds every claim from the JSON, re-runs nothing):
  `experiments/p2_route_dtor_v1_evidence.py`
* Figure: **fig106** (`writeup/figures/fig106_route_dtor_v1.png`), registered in
  `writeup/build_figures.py`
* Novelty pass: `writeup/novelty/leg_390.md`, committed **before** the runner existed (`68b027f`)
* Journal, with the pre-committed immutable gate: `experiments/journal/leg_390.md`
* `CLAY_OBLIGATIONS.md`: **read, never edited.** sha256 at read time
  `f47a73ac27903d79f63435ba8f4726245059e0c09f931e15cb9c0ed7a2923bde`, banked in the JSON.
  Three corrections are routed to integration **verbatim** and applied nowhere by this leg.

---

## 1. What (D) actually says, machine-read

Leg 381 banked Fefferman's statements verbatim. This leg does not retype them: it **parses** them
out of `writeup/data/p2_route_cloc_v1.json`, splitting each breakdown statement at the phrase
*"for which there exist no solutions"* into the conditions the **data** must satisfy and the
conditions a **solution** would have to satisfy.

| statement | data conditions | solution conditions |
|---|---|---|
| **(C)** breakdown on ℝ³ | (4), (5) | (1), (2), (3), **(6)**, **(7)** |
| **(D)** breakdown on ℝ³/ℤ³ | (8), (9) | (1), (2), (3), **(10)**, **(11)** |

Going (C) → (D), the solution side drops `{6, 7}` and adds `{10, 11}`. But **(6) and (11) are the
same text** — machine-compared, `p, u ∈ C^∞(ℝⁿ × [0,∞))` both — so the diff is exactly one
condition out and one condition in:

> **(7) bounded energy OUT, (10) periodicity IN.**

(7) is confirmed to be the bounded-energy condition from its own banked text (it contains the
string *"bounded energy"*); (10) is confirmed to be the periodicity condition the same way.
**§4's premise is therefore ABSENT from (D)'s own text.** That much of leg 381's note survives
verification intact.

**Red path.** Planting the string `(7),` back into (D)'s solution list makes the parser report the
bounded-energy premise **present** — the check fires, so its green is worth something.

**The gap this leg cannot close, stated rather than hidden.** (D)'s *data* conditions **(8)** and
**(9)** are **not in this repository at all**: leg 381 banked (4),(5),(6),(7),(10),(11),(A),(C),(D)
and did not bank (8),(9), and this leg has no outreach. They are treated as
**UNREAD-IN-REPOSITORY** and **nothing below is priced from them.** Every magnitude here rests on
(D)'s solution conditions and on the machine-checked absence of (7).

---

## 2. The rigidity that decides the shape of the question

Before any price can be quoted, one thing has to be settled: *what would a torus target even be?*

**Measured statement.** If `u(·,t)` is `L`-periodic for every `t` and `u` is exactly `λ`-DSS with
`λ > 1`, then applying the DSS relation shows `u(·,t)` is also `L/λ`-periodic, hence `L/λⁿ`-periodic
for every `n`, hence constant in `x`. **A non-constant exactly-DSS field on T³ does not exist.**

This is elementary (the novelty pass says so). What is measured here is *how fast* it bites, in the
Fourier band `|m|_∞ ≤ M = 64`:

| `λ` | nonzero modes surviving 1 DSS step | surviving 2 steps | steps to annihilate the band | one-step margin |
|---|---|---|---|---|
| `1.7` (leg 381's banked λ; `= 17/10`) | **342** | **0** | **2** | `2.45e-15` |
| `e^{1/2} ≈ 1.6487` (Pineau–Vicol's ceiling; irrational) | **0** | 0 | **1** | `0.01024` |

The rational case is the interesting one: `λ = 17/10` leaves exactly the multiples of 17 alive after
one step (7 per axis, `7³ − 1 = 342` nonzero modes) and kills them at the second. The margin for the
irrational case decays with band width at a **measured exponent `−0.99057`** against a predicted
`−1` — so the incompatibility is *exact* for every `λ > 1` but *not uniform*: a field that is DSS
only to a tolerance can be periodic to that tolerance if its content above wavenumber `~1/tolerance`
is negligible. That is a statement about approximate objects and it does not soften the exact one.

**Red path.** `λ = 1` — no dilation at all — leaves **2 146 688** nonzero modes alive and never
annihilates the band. The check can go red.

**Consequence.** (D) cannot be targeted by a *native* torus DSS object. It can only be targeted by
**periodizing an ℝ³-anchored one**, which is why the price below is a periodization price and not a
relabelling. Two routes exist, and both are priced.

---

## 3. Route 1 — wrap the uncut profile. THE BILL.

The cheapest conceivable move: `u_per(x) = Σ_{k ∈ ℤ³} u(x + Lk)`, no cutoff, no modification. For a
profile with `|u(y)| ≍ (1+|y|)^{−α}` the image at lattice site `k` contributes `~(L|k|)^{−α}` at the
cell centre, so the question is whether `Σ_{k≠0}|Lk|^{−α}` converges.

Measured on the actual `ℤ³` lattice (spherical truncation, `|k|₂ ≤ R`, `R ∈ {12, 24, 48, 96}`),
by the **shell increment** `S(2R) − S(R)` — the partial sum itself is
monotone whatever `α` is and so cannot detect convergence, while the increment's exponent changes
sign exactly at the threshold:

| `α` | measured increment exponent | predicted `3 − α` | \|error\| |
|---|---|---|---|
| 0.5 | 2.50006 | 2.5 | 6.025e-05 |
| 1.0 | 1.99955 | 2.0 | 4.516e-04 |
| 1.5 | 1.49899 | 1.5 | 1.011e-03 |
| 2.0 | 0.99838 | 1.0 | 1.623e-03 |
| 2.5 | 0.49771 | 0.5 | 2.288e-03 |
| 3.0 | −0.00301 | 0.0 | 3.010e-03 |
| 3.5 | −0.50379 | −0.5 | 3.788e-03 |
| 4.0 | −1.00462 | −1.0 | 4.620e-03 |

Worst error **4.620e-03**. Bisection on the measured exponent locates the convergence threshold at
**α = 2.996995** (against the exact 3; 0.10% low, the residual bias of the finite-`R` increment fit).

At `α = 3` exactly the sum is **logarithmically divergent**: increments per doubling of `R` are
`8.74999`, `8.71536`, `8.71356`, spread **0.0364** — the same signature leg 381 measured for the
critical `L³` tail (326.875 per decade, spread 7.4e-10), and now the third appearance of that
signature in this ledger.

**No torus size cures it.** `S(R, α, L) = L^{−α} S(R, α, 1)`: the measured `L`-exponent at `α = 1`
is **−1.0000000000000002** against a predicted −1 (error 2.2e-16). Enlarging the torus buys a
constant prefactor and does not touch the `R`-divergence.

### The bill, in leg 381's own currency

Both obligations are quoted in the **same** unit — the profile's certified far-field decay exponent
`α` — so they are directly comparable. §4's numbers are machine-read from
`p2_route_cloc_v1.json` `check_B3`, not retyped.

| | §4 (bounded energy, `L²`) | periodization (this leg) |
|---|---|---|
| `α` required | **1.5** | **2.996995** |
| `α` available a priori (Type-I, Chae–Wolf) | 1.0 | 1.0 |
| **deficit** | **0.5** | **1.996995** |
| **ratio required/available** | **1.5×** | **2.99700×** |

> **REPURCHASE FACTOR: 3.99399× in deficit, 1.99800× in ratio.**

Statement (D) deletes an obligation that needed `α > 1.5` and, by route 1, reinstates one that needs
`α > 3` — the same currency, **four times the deficit**.

**Red path.** Asserting the `α = 1` exponent against a deliberately wrong prediction (2.25 instead
of 2.0) fails at tolerance 0.02 while the correct prediction passes: error **0.250452** planted
against **4.516e-04** true.

---

## 4. Route 2 — cut off first, then wrap. What it inherits, and what it adds

Since §2 above shows route 1 has no exactly-DSS object to apply to, the realistic route is: cut off
at radius `ρ`, then wrap on a torus of side `L > 2ρ`.

**What it inherits: leg 381's entire cutoff bill, unchanged, every number** (machine-read from
`p2_route_cloc_v1.json`, not retyped): nonlinear residual `ρ^{−1.4993}`, viscous `ρ^{−1.4999}`,
divergence defect `ρ^{−0.4996}`, pressure perturbation at the origin `ρ^{−1.9997}`, and the critical
`L³` tail that **does not shrink** — **326.875 per decade of window, constant to 7.4e-10.**

This is the load-bearing observation of the whole leg:

> **What (D) deletes is the ACCEPTANCE TEST (7), not the cutoff analysis that §4 transferred to §5.**

**What it adds — measured, and smaller than expected.** On a smooth compactly-supported exactly
divergence-free test field (`u = curl(ψ e_z)`, `ψ = exp(−2/(1−|x|²/ρ²))·x·y`; divergence measured on
a refinement ladder `n = 41 → 321`, residual falling `3.09×, 3.75×, 3.92×` per halving, i.e. second-
order truncation error and not a non-solenoidal field):

* **direct image contamination of the cell: exactly `0.0`** at `L/ρ = 3.0, 2.5, 2.0001` — disjoint
  supports. It becomes `0.0389` (1.00× the cell field's own sup) at `L/ρ = 1.5` and `0.1554` (4.00×)
  at `L/ρ = 1.0`, so the check has a demonstrated red path.
* **image pressure interaction, leading multipole.** Modelling the image pressure at the cell centre
  as `Σ_{k≠0} T_ij(Lk) M_ij` with `T_ij = (3k_i k_j/|k|² − δ_ij)/(4π L³|k|³)`: the **magnitude** sum
  is log-divergent (increments per doubling `0.5785, 0.6329, 0.6624, 0.6776`, converging to the
  predicted `log 2 = 0.69315`; relative error 0.022371 at the top rung, `N = 32`), but the
  **signed** sum cancels
  shell by shell on the cubic lattice to **2.82e-17** cumulative at `N = 32`. Breaking the cubic
  symmetry (half-lattice `k_x > 0`) leaves **0.3458** — the cancellation check can go red.

So the pressure non-locality is **not** the obstruction on T³ either — the same verdict leg 381
reached on ℝ³, by a different mechanism. That is a **credit** on (D)'s side and it is reported as
one.

---

## 5. §2's four screen rows, machine-read

**Pre-registered rule** (journal §0, rule 2, fixed before any number was computed): a row is
**ℝ³-ONLY** if the hypothesis text *in its landed record* invokes whole-space structure T³ does not
carry, **or** if the object class it constrains is defined by the dilation action §2 above shows does
not act on T³. Both sub-verdicts are reported separately and **never netted into one word**.

| row | landed record | field read | marker verdict | ansatz verdict | **combined** |
|---|---|---|---|---|---|
| NRS 1996 / Tsai (T1/T2) | `solver/dssp_screen.py` (legs 357/362/370), `ledger_nrs_tsai()` | the verbatim NRS quotation in the module source | CARRIES-TO-T3 | ℝ³-ONLY | **ℝ³-ONLY** |
| Chae–Wolf / Pineau–Vicol | `writeup/data/p2_route_pvlx_v1.json` (leg 330, `5496bbc`) | `clause_by_clause[H1,H2,H5]`, `magnitudes_of_near_1[M1].value_lambda_ceiling` = 1.6487212707 | ℝ³-ONLY (hit: `R^3`) | ℝ³-ONLY | **ℝ³-ONLY** |
| Chae–Tsai | `writeup/data/p2_route_ctrx_v1.json` (leg 326, `c541cdb`) | `gate.clause_ledger.alpha_equation.verdict` (= `FAILS_HYPOTHESIS`, the decisive clause), `theorem_read.equation_1_6_*` | CARRIES-TO-T3 | ℝ³-ONLY | **ℝ³-ONLY** |
| Morrey (Jiu–Wang–Wei arXiv:2006.15776) | `writeup/data/p2_route_mryx_v1.json` (leg 368) + `p2_route_b7m_v1.json` (leg 370) | `paper_theorems_read_at_primary_text.theorem_1_2`, `.morrey_norm_definition` | ℝ³-ONLY (hits: `R^3`, `M(dot)q`, `sup_{R>0}`) | ℝ³-ONLY | **ℝ³-ONLY** |

> **Tally: 4 of 4 rows ℝ³-ONLY. 0 clearances carry to T³.**

The two rows whose *marker* verdict is CARRIES-TO-T3 are instructive and are why the sub-verdicts are
reported separately: NRS/Tsai's and Chae–Tsai's decisive content is not about the ambient space at
all (Chae–Tsai's decisive clause is that its theorems hypothesise the rescaled **Euler** system, and
that silence about NS is domain-independent). They still come out ℝ³-ONLY because the *object class*
they speak about — exactly-self-similar, or DSS — is defined by a dilation that does not act on T³.

`CLAY_OBLIGATIONS.md` §2 calls the screen *"LARGELY DISCHARGED, and this is the programme's strongest
position."* That is true of the ℝ³ target and, on this count, of no torus target: **§2's rigidity
screen re-opens in full**, and a torus screen would have to be rebuilt against a periodic rigidity
literature this repository has never searched (novelty pass §1). This is the known cost side and it
is reported as a count, not as a word.

**Red path.** A planted control row with no whole-space marker and no ansatz marker ("a smooth
solution of the heat equation with bounded gradient") returns **CARRIES-TO-T3**; a planted row with
both returns **ℝ³-ONLY**. The rule is not one that returns ℝ³-ONLY for everything.

---

## 6. The §1–§5 disposition table

Vocabulary closed and pre-registered: `VACATED`, `UNCHANGED`, `TRANSFERRED`; a `TRANSFERRED` without
a magnitude is a NO on the gate's first clause.

| § | disposition | magnitude / pointer |
|---|---|---|
| **§1** the profile exists (rigorous enclosure) | **UNCHANGED** | (D) changes the acceptance conditions of the assembled solution, not the enclosure problem. **Credit on (D)'s side, reported at full strength:** leg 348's named obstruction for §1 is that every located periodic-orbit certification instance closes its tail estimate against a **compact** domain — census **6** compact/periodic, **1** unbounded (stationary, 1D, different apparatus), **0** unbounded periodic-orbit at any weight (`p2_route_pocp_v1.json`, `domain_census`). A torus **is** that domain. **The catch, stated plainly:** the credit is collectable only by an object that *lives* on the torus, and §2 above measures that a non-constant exactly-DSS torus field does not exist. The credit and the obstruction are about different objects and this leg **does not net them**. |
| **§2** the profile is admissible | **TRANSFERRED** | 4 of 4 rows ℝ³-only; **0 clearances carry**. Transferred to a torus rigidity screen against a periodic literature never searched here. Per-row records in the table above. |
| **§3** the profile generates a genuine NS solution | **TRANSFERRED** | Biot–Savart/pressure reconstruction must be redone with the **periodic** Green's function (leg 351's closed-form ℝ³ swirl potential is not the torus one). Magnitudes: image-pressure magnitude sum log-divergent at increments `0.5785 → 0.6776` per doubling toward `log 2`, but the signed sum cancels to **2.82e-17**; direct image contamination at `L > 2ρ` is **0.0**. **§3 is the cheap transfer.** |
| **§4** finite energy / localisation | **VACATED-AS-AN-ACCEPTANCE-TEST, TRANSFERRED-AS-WORK** | Vacated: (7) is absent from (D)'s own text (§1 above, machine-read). Transferred, route 1: `α > 2.996995` required vs §4's `α > 1.5`, on the same available `α = 1.0` — deficit **1.996995** vs **0.5**, **repurchase factor 3.99399×**. Transferred, route 2: leg 381's cutoff bill in full and unchanged, critical `L³` tail **326.875 per decade** included. |
| **§5** stability / persistence under localisation | **UNCHANGED** | Leg 314's residual obligation is a high-frequency resolvent bound on `|Im μ| → ∞` — a statement about the linearisation's spectrum at large frequency, not about the ambient domain. Machine scan of §5's own text in `CLAY_OBLIGATIONS.md` finds **no** ℝ³ markers. Under route 2 the perturbation §5 must survive is the *same* cutoff perturbation, so §5's content is untouched. |

**§6 is unchanged by this leg**, as the spec requires of a scoping answer: item 1 (certified
far-field decay and the admissible cutoff) **OPEN**, item 2 (persistence/stability under
localisation) **OPEN**. If anything item 1 becomes *more* load-bearing under (D), because the
certified far-field exponent `α` is the currency of the periodization bill as well as of the
cutoff bill.

---

## 7. Corrections routed to integration, verbatim, applied nowhere by this leg

1. `CLAY_OBLIGATIONS.md`'s (D) paragraph says (D) *"carries no decay condition and no bounded-energy
   condition"*. Machine-read against (D)'s own banked text, the supportable statement is narrower:
   (D)'s **solution** conditions are (1),(2),(3),(10),(11) and contain no (7); its **data**
   conditions are (8),(9), whose verbatim text is **not in this repository**, so no claim about what
   they do or do not require is supportable here.
2. `writeup/data/p2_route_cloc_v1.json` `check_D_clay_primary_text.verbatim_conditions` banks
   (4),(5),(6),(7),(10),(11),(A),(C),(D) but **not (8),(9)**. A leg with outreach should close that
   gap.
3. `CLAY_OBLIGATIONS.md` §2's "the programme's strongest position" is correct as written for the ℝ³
   target and would need a scope word if (D) were ever adopted.

## 8. What this leg is not

It is not a retarget, not build authority, and not a recommendation. It priced an option in both
directions: (D) genuinely deletes a Clay acceptance condition and genuinely sits on the favourable
side of §1's domain census; and (D) genuinely re-opens §2 to zero clearances, genuinely leaves the
cutoff analysis in place, and — if the uncut profile is wrapped instead — charges the deleted
obligation back at four times the deficit. **The choice between those is the user's, and this leg
makes none of it.**
