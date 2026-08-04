# Route-J v1 — the primary-source pass

*Phase 2 / P2, leg 42. Figure: `writeup/figures/fig39_route_j_v1_literature.png`.
Code: `solver/literature_gates.py`, `test_literature_gates.py` (9/9),
`experiments/p2_route_j_v1_literature.py` → `writeup/data/p2_route_j_v1_literature.json`.
Working notes: `PHASE2_P2_NOTES.md` §31. Literature record: `LITERATURE_CHECK.md`, sixth
pass (the first primary-source pass).*

**No new science. This leg reads the papers that six previous legs were blocked from
reading, and retracts what they pre-empt. Seven standing claims are pre-empted, one is
partial, two remain unsearched, and one result arrives *from* the literature that this
project did not have. No link of the L1→L4 chain moved. Clay odds unchanged at ~0.05%.**

---

## 0. What this leg is, in one paragraph

For six legs `LITERATURE_CHECK.md` grew — five passes — while `Papers/` stayed empty,
because the environment's egress allowlist did not include `arxiv.org`. Every novelty
claim this project has ever made was search-level: assembled from search-engine summaries
of papers nobody here had opened. This session egress worked. `bash Papers/fetch.sh`
pulled all fourteen manifest entries on the first try; Tier 1 is read; and this leg is
what the reading leaves behind. The deliverable is not a paragraph saying "we checked" —
that is exactly as durable as a figure looked at once, which Route-I established is not
durable at all. It is a module of **executable gates**: each one re-derives a published
number from the published equations and compares it to ours, so the check survives the
session that made it.

The headline is a subtraction. **Route-F v1's `s_c = α/2` — the leg the project called
"the only item that probes the actual obstruction between a toy certificate and NS" — is
in the literature, as `s*(a) = 1/c_l(a)`, posted eleven days before we did it.**

---

## 1. The sources, and the exponent dictionary that makes them comparable

Four papers do the work.

| tag | arXiv | what it is |
|---|---|---|
| **ALS** | 2207.07548 | Ambrose, Lushnikov, Siegel, Silantyev, *Global existence and singularity formation for the gCLM equation with dissipation: the real line vs. periodic domains*, Nonlinearity (2022) |
| **XU** | 2607.19762 | Xu, *The spectral picture of self-similar collapse in the CLM equation* (22 Jul 2026) |
| **CH** | 2210.07191 | Chen & Hou, *Stable nearly self-similar blowup of the 2D Boussinesq and 3D Euler equations with smooth data I* (v3, 2023) |
| **HTW** | 2209.08232 | Huang, Tong, Wei, *On self-similar finite-time blowups of the De Gregorio model on the real line* (2022) |

Before any comparison there is a translation, and getting it wrong is the only way to
misread this literature. ALS and XU write

```
omega ~ tau^{-beta} f( x / tau^{c_l} ) ,     tau = t_c - t
```

so their `c_l` (ALS call it `alpha`, XU call it `c_l`) is the **length** exponent — what
this project calls `beta`. Our `alpha` is the profile's far-field decay exponent, and
§26's rescaling ODEs give `beta = 1/alpha`. Therefore

```
alpha_ours  ==  1 / c_l ,
```

and because their dissipation is `Lambda^sigma` while ours is `(-Delta)^s` with symbol
`|k|^{2s}`, we have `sigma = 2s`. Gate 1 of the suite is nothing but this dictionary,
checked to be self-inverse on both anchors, and it goes first because **every other
verdict in this leg inverts if it is wrong while still passing its own test.**

---

## 2. J1 — the constant ALS corrected in Schochet (1986), settled from our side

ALS §5.1 reproduce Schochet's exact `a = 0`, `sigma = 2` pole-dynamics solution and note,
parenthetically, that they are **correcting** the 1986 constant: `K_pm = 24(3 ± √6)`,
where Schochet printed `12(6 ± √6)`.

That is a checkable claim, and checking it is free. Substituting the ansatz (37)–(41) into
ALS (36) — the complex Burgers equation `omega_+t = -i omega_+^2 + nu omega_+xx` — with
**analytic** `∂_t` and `∂_xx` (no differencing anywhere, so the residual tests the
solution rather than a discretization of it):

| constant | worst relative residual |
|---|---|
| `24(3+√6)` (ALS, corrected) | **5.24e-16** |
| `24(3−√6)` (ALS, corrected) | **2.85e-16** |
| `12(6+√6)` (Schochet 1986, as printed) | **2.40e-2** |
| `12(6−√6)` (Schochet 1986, as printed) | **8.36e-2** |

Three `(nu, t, pole)` configurations each, worst quoted. **13.66 decades of separation.**
ALS are right, and we now know that rather than assume it. As a second check on the same
solution, ALS (44) for the blow-up time agrees to 1e-13 with the time the pole trajectory
(40)–(41) actually crosses the real axis, which for poles on the imaginary axis is
available in closed form (`√(1 + (5/3)Kνt) = 3`).

This matters beyond bookkeeping: Route-H's `Papers/MANIFEST.md` lists Schochet CPAM 1986
as gating its closed form and as unavailable (publisher PDF, not on arXiv). It is still
unavailable — but its content is now pinned through ALS, and **the version of the constant
that would have come from the 1986 paper is the wrong one.**

---

## 3. J2 — Route-H's closed form (E) *is* ALS equation (57)–(58)

Route-H v1 introduced, as the known-answer gate its whole leg hangs from,

```
omega(x, t) = -2 (1 + mu_0) kappa x / ( kappa^2 (T-t)^2 + x^2 ) ,    kappa = nu / mu_0    (E)
```

and recorded it as "at high risk of being known", declining to claim it. That was the
right call, and it is now settled rather than suspected. ALS §5.3 solves `a = 0`,
`sigma = 1` by pole dynamics:

```
omega(x,t) = omega_{-1}(t)/(x - i v_c(t)) + conj ,
omega_{-1}(t) = omega_{-1}(0) ,   v_c(t) = (omega_{-1}(0) + nu) t + v_c(0)      (57)-(58)
```

Splitting (E) into partial fractions gives a conjugate pair of **simple** poles at
`x = ± i kappa (T-t)`, i.e. exactly (57), under the parameter map

```
omega_{-1}(0) = -(1 + mu_0) kappa ,      v_c(0) = kappa T .
```

Three independent confirmations, all in the gate suite:

1. **Pointwise agreement.** Three parameter sets `(mu_0, nu, T)` × four times including
   `t = 0.99 T`: worst relative difference **6.5e-15**.
2. **The evolution law, from the other direction.** ALS's `dv_c/dt = omega_{-1}(0) + nu`
   evaluates to `-(1+mu_0)ν/μ_0 + ν = -ν/μ_0 = -kappa`, which is (E)'s own `dv_c/dt`.
   Agreement to 1e-13, and this is a *derivation*, not a fit.
3. **ALS's blow-up time formula (59) returns our `T` exactly** — absolute error `0.0`,
   not "small". And `omega_{-1}(0) < -nu`, so (E) sits on ALS's blow-up branch by their
   own criterion rather than merely near it.

**Verdict: PRE-EMPTED.** What survives is (E)'s *use* as a known-answer gate, which is
what Route-H built it for, and which is strictly better now that it carries a citation.

A second consequence, and a more interesting one. ALS's self-similar form (61) for this
family carries `nu` **inside the profile** with the exponents fixed at `c_l = beta = 1`.
That is a one-parameter family of viscous self-similar blow-ups at `a = 0` — which is
precisely Route-H's `alpha_1 = 0`, the "line of viscous self-similar blow-ups". **Route-H
measured, numerically, the existence of an exactly-known family.** Correct; not new.

---

## 4. J3 — `alpha(1/2) = 3`, from the published `a = 1/2` system, integrated cold

ALS §5.2 gives the `a = 1/2`, `sigma = 1` pole system (double poles this time, and ALS
note the leading `1/(x∓iv_c)^4` poles cancel *only* at `a = 1/2`, which is what selects
that value):

```
dv_c/dt = -( omega_{-2}/(4 v_c) - nu ) ,      d omega_{-2}/dt = omega_{-2}^2 / (4 v_c^2)   (49)-(50)
```

This shares no grid, no basis, no formulation and no line of code with our compactified
Newton solve. Integrating it into the collapse and measuring the local exponent:

| `v_c` | `Omega = omega_{-2}/v_c` | `tau = t_c - t` | `d log v_c / d log tau` |
|---|---|---|---|
| 1.13e-1 | 9.9e+2 | 1.5e-4 | 0.3325202 |
| 2.62e-2 | 1.8e+4 | 1.9e-6 | 0.3332893 |
| 6.11e-3 | 3.3e+5 | 2.4e-8 | 0.3333310 |
| 1.42e-3 | 6.2e+6 | 3.1e-10 | **0.3333076** |
| 7.95e-4 | 2.0e+7 | 5.4e-11 | 0.3332091 |

**`c_l = 0.3333076` against the exact `1/3`, relative error 7.7e-5**, so
`alpha(1/2) = 3.000232`. The independent structural check on the same trajectory:
`Omega ~ v_c^{-2.000144}` against the exact `-2`.

So Route-E's twelve-digit `alpha(1/2) = 3` is **right, exact, and known** — it is
`c_l(1/2) = 1/3` from the exact pole-dynamics solution, attributed by both ALS and XU to
Lushnikov–Silantyev–Siegel and to J. Chen.

**And this answers a question Route-E left open and flagged as unexplained.** Route-E
found `alpha` passes through odd integers at isolated `a` — `alpha = 1` at `a = 0`,
`alpha = 3` at `a = 1/2` (twelve digits), `alpha = 5` at `a = 0.5821792673` — and recorded
that *"what stays unexplained is why alpha = 3 lands on a round rational while alpha = 5
does not."* ALS §1 states it plainly: exact solutions as superpositions of pole
singularities exist at `a = 0` and `a = 1/2` **and, per Lushnikov et al., nowhere else**.
`alpha = 3` is a round rational because there is an exact solution behind it. `alpha = 5`
is not because there is not. The `alpha = 5` "resonance" is a property of **our
instrument** — `Lambda^5` happens to be a finite matrix there — and not of the problem.

### 4.1 The refusal predicate, and the loose first version of it

The first version of this measurement had a gate on `tau`: refuse a rung once `tau` falls
below `1e3 · eps · max|S|`, `S` being the accumulated quadrature. It passed, and it read
**`c_l = 0.222` at its deepest "resolved" rung** while reading `0.33333` in the middle.

The gate was on the wrong quantity. The local exponent is a **difference quotient**, so
what must stay resolvable is `d tau`, not `tau` — and `tau` at the bad rungs is `1e-11`,
enormous compared to underflow, so no threshold on `tau` could ever have caught it.
Gating `d tau > 1e3 · eps · max|S|` instead cuts the ladder at `d tau ≈ 3.5e-14` and
refuses the entire tail below it (157 161 of 200 001 samples in the driver's run, which is
most of them because the reparametrised integration spends most of its steps there); the
deepest refused rungs read `c_l` off by `≥ 0.32`. Panel C draws the refused branch in red
rather than truncating the axis, because a gate you cannot see is a gate you cannot audit.

This is banked lesson 57 (*"is the signal above the solve error?"*) one level down:
**gate the quantity the measurement divides by.**

---

## 5. J4 — what lies *above* criticality: the one thing the literature gave us

Routes F, H and I all stop at `s ≤ s_c`. Route-F's sentence was *"the scaling says which
term dominates given the self-similar form"* — and it had no second half. ALS §5.1 has the
second half, in the one case where it is exactly solvable.

Substituting `omega ~ tau^{-beta} f(x/tau^{c_l})` into the equation term by term:

```
omega_t                ~ tau^{-beta - 1}
omega H(omega)         ~ tau^{-2 beta}
nu Lambda^sigma omega  ~ tau^{-beta - sigma c_l}
```

Below criticality `omega_t` balances stretching, forcing `beta = 1`, and dissipation is a
correction — that is the regime every leg of this project has lived in. **Above
criticality the balance switches: dissipation balances stretching, giving**

```
beta = sigma * c_l ,
```

**and the time derivative becomes subdominant.** Schochet is the witness: `a = 0` gives
`c_l = 1`, so `sigma_c = 1/c_l = 1` and `sigma = 2` is supercritical; the balance predicts
`beta = 2`; and ALS (45) reports exactly `omega ~ tau^{-2} f(x/tau)`.

We measure it rather than quote it. Rescaling the exact solution on a `tau`-ladder
`{1e-3, 3e-4, 1e-4, 3e-5, 1e-5}` and reporting the spread of `tau^beta omega` across the
ladder:

| `beta` | 1.0 | 1.5 | **2.0** | 2.5 |
|---|---|---|---|---|
| spread | 0.990 | 0.898 | **0.0202** | 0.902 |

`beta = 2` wins by **49×**. But a minimum over four guesses is a fit, not a measurement,
so the check that makes it one: ALS state (45) carries an `O(tau^{-1})` correction, so the
`beta = 2` residual must **shrink** on deeper sub-ladders. It does — `0.0202 → 0.0060 →
0.00187` as the ladder deepens, falling like `tau^1` relative to `tau^{-2}`, which is the
stated correction behaving as stated.

**The mechanism is the part worth carrying.** The `tau^{-2}` is carried by a **double
pole whose residue is `B = -12 i nu`** — proportional to `nu`, hence absent inviscidly.
Above criticality the blow-up is not the inviscid one surviving viscosity; it is a
*different* singularity that viscosity itself creates. Nothing in Routes F/H/I could have
seen that, because all three are built on the assumption `beta = 1`.

And it sharpens what `s_c` means. XU are explicit, and we should be equally explicit:
`s*` is **not** the sharp blow-up/regularity threshold — "which for this family remains
unknown". At `a = 0`, `s* = 1` and Schochet blows up at `s = 2 > s*`; XU also cite Sakajo,
that at `a = 0` blow-up persists at small viscosity *regardless of the derivative order of
the dissipation*, with global solutions at large viscosity. So `s*` is not even
`nu`-independent as a threshold. It is a relevance exponent for a fixed self-similar form,
and Route-F's map is orientation, exactly as Route-F said — but the reason is now
citeable rather than cautious.

---

## 6. J5 — our `alpha(a)` branch is XU's `s*(a)`, row for row

XU §6.1 eq. (6.3) defines the scaling-critical dissipation exponent by exactly our
argument — dissipation enters the rescaled equation with coefficient `e^{-gamma tau}`,
`gamma = 1 - s c_l`, and `s*` is where `gamma = 0`:

```
s*(a) = 1 / c_l(a) .
```

In our gauge that is `alpha(a)`, and `s_c = alpha/2 = s*/2`. Route-F v1's headline.
Against XU's Table 1, read straight out of Route-F's committed JSON so the comparison
cannot drift from the data:

| `a` | ours `alpha(a)` | XU `s*(a)` | rel. diff |
|---|---|---|---|
| 0.0 | 1.0000000 | 1.000 | 0 (both exact) |
| 0.1 | 1.1413974 | 1.145 | 3.1e-3 |
| 0.2 | 1.3344967 | 1.338 | 2.6e-3 |
| 0.3 | 1.6172442 | 1.619 | 1.1e-3 |
| 0.4 | 2.0794638 | 2.079 | 2.2e-4 |
| 0.5 | 3.0000000 | 3.000 | 3e-16 (both exact) |

Worst row 3.1e-3, mean 1.2e-3 — and XU state their own branch is good to "two or three
significant figures at nonzero `a`", so this is agreement at the accuracy either side
claims, not a discrepancy. The two exactly-known anchors agree to machine precision.

The endpoint is where we come off worst. `a_c` published (Lushnikov–Silantyev–Siegel) is
**0.6890665**; XU's recompute is 0.6888, **0.04%** off; ours is 0.693493, **0.64%** off.
We are the least accurate of the three sources and should quote theirs. There is a gate
asserting exactly that, which will fail if we ever become the better source — at which
point the right response is to say so, not to delete the gate.

Also pre-empted: the ordinary-Laplacian crossing. Ours `a ≈ 0.38281`, XU `a ≈ 0.39`.

---

## 7. J6 — the ledger

Twelve standing claims, with the verdict vocabulary fixed and gated:

| verdict | n |
|---|---|
| PRE-EMPTED | 3 |
| CONFIRMED_AND_PRE-EMPTED (right, and known) | 3 |
| PRE-EMPTED_AND_RE-CLASSIFIED | 1 |
| PARTIAL (scope differs) | 1 |
| UNSEARCHED_AT_PRIMARY_SOURCE | 2 |
| CONFIRMED (never claimed as ours) | 1 |
| OPEN_QUESTION_ANSWERED_BY_THE_LITERATURE | 1 |

Two entries need more than a row.

### 7.1 The re-classification, which has the largest forward consequence

XU's **Proposition 2, the realization dichotomy**, is the item to actually carry forward,
and it is not a pre-emption of a claim so much as a re-description of a measurement.

Route-E measured the essential spectrum of the rescaled linearization as a **continuum**
filling `[0, +1]` at `a = 0` and `[-2, +5]` at `a = 1/2`, and shut the DSS lane with *"a
continuum has no eigenvalue to move"*. XU prove that on the **origin-`H^2`** realization
there is no such continuum in the strip — the point spectrum is exactly `{0, 1}` and the
open strip is empty — while on the **maximal `L^2`** realization the whole strip *is*
spectrum, filled by an explicit family `u_lambda(y) = y^{1-lambda}/(y + i/2)^2` that is
`L^2` but fails `u'' ∈ L^2` at the origin. And they say, in as many words, that *"the
persistent essential smear that the grids without an origin condition place inside the
strip"* is the faithful spectrum of that maximal realization.

**Our discretization has no origin condition. We were rendering the loose realization.**
So "the non-symmetry spectrum is continuous" is not a property of the operator; it is a
property of which operator we discretized. The DSS conclusion survives — in the tight
realization there is no continuum *and* no complex pair, so there is still nothing to
bifurcate, and the lane stays shut on better evidence than before.

**But Route-I's headline inherits the problem in full.** Route-I reported that the
inviscid rescaled fixed point at `a = 1/2` has **141 of 144 unstable directions**, and read
that as "§26's essential spectrum as a count". If the essential spectrum in question is
the maximal realization's strip, then the count is a count of *that realization's*
spectrum — a realization whose eigenfunctions are precisely the ones failing the
regularity condition at the collapse point. **This does not make Route-I wrong, and it
does not by itself change the `mu > 0` half of the inversion** (that half is about
dissipation collapsing the spectrum onto a discrete negative ladder, and a discrete ladder
is not realization-smear). It does mean the `mu = 0` count is quoted in a realization
nobody would choose deliberately, and **the honest statement of Route-I's inversion needs
the realization named in it.** That is now the top-ranked correction item, and §8 says so.

### 7.2 The partial: finite support

HTW Proposition 2.3 — any `H^1` solution of the profile equation with `c_omega/c_l > 0`
must be compactly supported — is proved for the **De Gregorio model, `a = 1`**, where
non-degeneracy at the origin *forces* `c_l = c_omega`. The mechanism is the same one
Route-D v12/v13 found: the profile is locally proportional to `u + c_omega x`, and the
support ends where that vanishes. So the phenomenon and the mechanism are published.

What is not in HTW is the `a`-dependence: `X_c` as the zero of `c + aU` across
`a ∈ (0, 1/2)`, and the algebraic order `1/a` of that zero. And the use we actually made
of it — that a compactly supported profile in a *global spectral basis* puts its worst
representation error exactly where the decay-graded codomain weight is largest — is a
certification-space statement that no PDE paper would make. **PARTIAL, with the surviving
part narrower than "the profile ends".**

---

## 8. What this changes, and what it does not

**Does not change:** any number in any committed artifact. Every measurement this project
has made stands; nothing was found to be *wrong*. What changed is who found it first.

**Changes, in priority order:**

1. **Route-I's stability inversion must name its realization.** The `mu = 0` count of 141
   unstable directions out of 144 is a count in the maximal `L^2` realization. Flagged in
   the ledger and in `PHASE2_P2_NOTES.md` §31; the writeup correction is the first item of
   the next leg, and it may require re-running I5 with an origin condition to say what the
   count is in the realization one would actually choose.
2. **Route-F v1's writeups must lead with the pre-emption**, not bury it. Done in
   `LITERATURE_CHECK.md`; the `TECHNICAL_P2_ROUTEF_V1.md` header now carries it.
3. **Route-E's open question is closed** — by ALS, not by us — and its `a_c` should quote
   the published value.
4. **Route-H's (E) has a citation** and stops being "at high risk".

**Still unsearched at primary source:** the Route-D methodological claims (the
discrete-ball trap, the weighted-`ℓ¹` no-go, the elasticity discipline), which remain the
only claims in this project with a real chance of being new. Tier 2 (`2302.12877`,
`2312.01702`, `1908.09385`) is fetched and text-extracted but not read closely. **That is
now a cheap spend and it is the obvious next literature action** — but it is a literature
action, and Directive 2 (the L1→L2 certification port) has now been deferred six times.

**Clay:** nothing here moves a link of the L1→L4 chain. The realistic prize is still a
novel result on a model where blow-up is provable, and this leg made the "novel" half
materially harder by deleting the candidates that were not.

---

## 9. Reproduce

```bash
bash Papers/fetch.sh                                          # 14 PDFs, gitignored
.venv/bin/python -u experiments/p2_route_j_v1_literature.py   # ~5 s
.venv/bin/python writeup/4_p2_lottery/p2_route_j_v1_evidence.py
.venv/bin/python test_literature_gates.py                     # 9/9
```
