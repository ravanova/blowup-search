# Route-EGRB v1 — the truncation-controlled one-sided bound, in exact rational+π arithmetic

**Leg 340.** Runner `experiments/p2_route_egrb_v1.py`; data
`writeup/data/p2_route_egrb_v1.json`; figure + evidence
`writeup/figures/fig89_route_egrb_v1_evidence.py` →
`fig89_route_egrb_v1_ladder.png`; novelty pass `writeup/novelty/leg_340.md`;
running record `experiments/journal/leg_340.md`.

---

## 1. Gate

> Does the truncation-controlled one-sided bound hold `gap ≤ 1/2 + 1e-9` at
> every ladder rung, with the margin's dependence on the truncation parameter
> measured and reported (magnitudes, not booleans)?

**Answer: YES**, with the mandatory second reading in §7, which is part of the
answer and not a caveat attached to it.

## 2. The object

`a = 0` Constantin–Lax–Majda linearisation on `[0,π]`,

```
L h = cos θ · h  −  sin θ · H h  −  sin θ · h′,      H(sin kθ) = −cos kθ + (−1)^k
```

trial space `h = Σ_{k=1}^{n} c_k sin kθ`; constraint class `T2_egm` =
`{h′(0) = 0, (Hh)(0) = 0}`, i.e. `Σ k c_k = 0` and `Σ_{k odd} c_k = 0`; weighted
form `G_jk = ⟨e_j,e_k⟩_φ`, `B_jk = ⟨e_j, L e_k⟩_φ`;
`gap := −λ_max(Sym B, G) = −sup_h R(h)` with `R(h) = ⟨h,Lh⟩_φ/⟨h,h⟩_φ`.

Weights: family A γ = `(2 sin(θ/2))^{−γ}`; family B γ = same `×(2cos(θ/2))^{−2}`;
family E = EGM's own `(1+X²)³/(2X⁴)`.

**Prior art, not this repository's.** Elgindi–Ghoul–Masmoudi arXiv:1906.05811
Prop. 2.1 asserts `∫ f M_a f φ ≤ (−1/2 − C|a|)∫f²φ` under exactly these
hypotheses — the `−1/2` at `a = 0` is theirs. Xu arXiv:2607.19762 §3.1 gives
point spectrum `{0,1}` and essential spectrum on `Re λ = −1/2`, which is the
source of `KNOWN_ANSWER_CEILING = 0.5`.

## 3. Why the previous measurement could not settle it

| leg | quantity | value |
|---|---|---|
| 178 | `gap` at `n=256`, float64 | `+0.4999930` → gate `NO` |
| 329 | `gap` at `n=256`, 200-digit patch, `T2_egm\|B4_egm` | `0.4999913080184024` |
| 329 | C4: `−R_mp(x) − 1/2` at the float64 maximiser, B4 / E | `−5.18779822259e−18` / `−1.42393407007e−18` |
| 329 | C5: relative spread over `rcond ∈ {1e-14…1e-8}`, B4 / E | `3.853e−05` / `5.394e−05` |
| 329 | `cond(G)` at `n=256` | `2.554e+11` (`cond·eps = 5.671e−05`) |

DM cycle 8e: the C4 margin is thirteen orders below the C5 sensitivity, so it
cannot carry clause 5. The bound reading must earn its own gate.

## 4. Instrument

Let `X = tan(θ/2)`, `u = 1 + X²`, and define `R_k, P_k ∈ ℤ[X]` by
`(1+iX)^{2k} = R_k(X) + i P_k(X)`, so `cos kθ = R_k/u^k`, `sin kθ = P_k/u^k`.
For `h = Σ_{k≤n} c_k sin kθ` with `c ∈ ℤⁿ`, accumulate by Horner in `u`:

```
h  = A/u^n ,   Hh = C/u^n ,   h′ = D/u^n
A  = Σ_k c_k P_k u^{n−k}
C  = Σ_k (−c_k) R_k u^{n−k}  +  (Σ_k c_k(−1)^k) u^n
D  = Σ_k k c_k R_k u^{n−k}
L h = [ (1−X²)A − 2X(C+D) ] / u^{n+1}
```

Weights are exactly rational in `X`, with `φ = u^w/(cst·X⁴)`:

| weight | `w` | `cst` |
|---|---|---|
| `B4_egm` | 3 | 64 |
| `E_egm` | 3 | 2 |
| `A4_chen_hou` | 2 | 16 |

so `φ_E = 32 φ_B4` **exactly**. With `dθ = 2dX/u` and `M := 2n+2−w`:

```
⟨h,Lh⟩_φ = (2/cst) ∫₀^∞ A·[(1−X²)A − 2X(C+D)] · X^{−4} u^{−M}   dX
⟨h,h⟩_φ  = (2/cst) ∫₀^∞ A²                    · X^{−4} u^{−(M−1)} dX
N(h)     = (4/cst) ∫₀^∞ A·C                   · X^{−3} u^{−M}   dX
```

and every one reduces to the moment

```
∫₀^∞ X^a (1+X²)^{−M} dX = ½ B((a+1)/2, M−(a+1)/2)
   = ½ · p!(M−p−2)! / (M−1)!                                 a = 2p+1  (RATIONAL)
   = ½ · (2p)!(2q)! π / (4^{M−1} p! q! (M−1)!),  q = M−1−p    a = 2p    (RATIONAL·π)
```

Hence `R = (r₁+q₁π)/(r₂+q₂π)` exactly, with `r_i, q_i ∈ ℚ` via
`fractions.Fraction`. **No float enters the exact path.** `π` is enclosed by
`solver/interval_mp.mp_pi` at 60 digits and propagated through `mp_add/mp_mul/
mp_div`, so the reported bound is an `MPInterval`. A monomial whose exponent
makes the integral divergent at `X=0` or `X=∞` raises `Divergent`; it is never
silently dropped.

**Trial vectors.** Each rung's own float64/MP maximiser `x` (from leg 329's
`assemble_gap`, imported, not copied) is rounded to integers at `2^30` and
mapped through the integer constrained basis, `c = V z`. Admissibility is
**exact**, not approximate: `V`'s columns are integer and satisfy the integer
constraint rows identically, so the reported `dprime` and `hilbert` residuals
are integer `0`. Rounding moves the vector by `≈4.6e−10` relative and is
reported (`rel_rounding_of_maximiser`), not hidden — it is harmless because the
bound is valid for *any* admissible vector.

## 5. Validity on the operator quantity (gate part i)

Fixed in `writeup/novelty/leg_340.md` §7d **before any number existed**:

```
gap_op  ≤  gap_trunc  ≤  −R(x)      for any admissible trial vector x
```

because a truncation restricts the supremum defining `gap` to a *subspace*, so
`sup_trunc R ≤ sup_op R`. The chain is strictly one-directional: it can bound a
gap from above but can never certify one is achieved. Clause 5 is a one-sided
ceiling, so this is the side that decides it.

The structural control in §6.3 strengthens this from a bound to an identity.

## 6. Results

### 6.1 The ladder — 19 rungs

`n ∈ {32,64,128,256} × rcond ∈ {1e-14,1e-12,1e-10,1e-8}` at `n_grade = 24`,
plus `n_grade ∈ {12,24,48,96}` at `n = 128, rcond = 1e-12`. Runtime 59.3 s.

| quantity | value |
|---|---|
| exact `−R(x)` at every rung, `B4_egm` **and** `E_egm` | **exactly `1/2`** (distinct-value set = `{−1/2}`) |
| ceiling | `1/2 + 1e-9`, leg 178's own slack, not widened |
| margin | **exactly `1e-9`** |
| **margin's dependence on the truncation parameter** | **exactly `0`** |
| max enclosure width over all rungs | `1.4e−59` |
| truncated eigensolve `gap`, absolute spread over the same rungs | `1.9266e−05` (B4), `2.6970e−05` (E) |
| ...as relative spread | `3.8533e−05` / `5.3940e−05` — reproducing leg 329's banked `3.853e−05` / `5.394e−05` |

Representative rung `n=256, n_grade=24, rcond=1e-12, B4_egm`:

```
exact_num = 0 + (−591703392682528784640)·π
exact_den = 0 + ( 1183406785365057569280)·π
R         = −1/2                    (π cancels; the quotient is a plain rational)
enclosure of −R : [0.4999…95, 0.5000…05], width 1.0e−59
gap_eigensolve = 0.4999913080184024 ; cond_G = 2.554e+11 ; dropped = 1
nonlocal term = 0 exactly ; constraint residuals = (0, 0) integer
```

### 6.2 The mechanism

`D_φ ≡ −1/2` identically for `B4` and `E`, so
`⟨Lh,h⟩_φ = −½‖h‖²_φ − N(h)`, `N(h) = ∫₀^π sinθ·φ·(Hh)·h dθ`. Measured exactly:
**`N(h) = 0` at every rung**, for every trial vector. The nonlocal term — the
only place the Hilbert transform enters — vanishes identically on `T2_egm`.

### 6.3 The structural control: the matrix, not one quotient

Computing `⟨v_a, L v_b⟩_φ` and `⟨v_a, v_b⟩_φ` exactly for **all pairs** of
`T2_egm` basis columns:

| `n` | dim | pairs | nonzero entries of `Sym(B) + G/2` |
|---|---|---|---|
| 4 | 2 | 4 | **0** |
| 6 | 4 | 16 | **0** |
| 9 | 7 | 49 | **0** |
| 14 | 12 | 144 | **0** |
| 20 | 18 | 324 | **0** |

> **`Sym(B) = −G/2` exactly.** The truncated pencil is identically `−I/2`, so
> `gap_trunc = 1/2` at every `n`, `rcond` and quadrature depth.

### 6.4 Controls

| id | what it is | result |
|---|---|---|
| K1 | reproduce leg 329's banked C4/C5 | `abs_difference = 0.0` on both headline rows; C5 spreads reproduced |
| K1b | leg 329's 200-digit node-by-node quotient **at the identical trial function** | `4.330e−17` (B4), `1.131e−16` (E), `3.109e−18` (A4). *The A4 row is load-bearing: both arithmetics agree on a value that is **not** `−1/2`* |
| K2 | `A4_chen_hou` has non-constant `D_φ`, so must differ | exact `R = −0.5001506…` (e.g. `−542608274568675296122725484/1084889760734792694474794953`); **fails the ceiling at every rung** |
| K3 | inadmissible vectors must diverge | `[1,0,−1]`, `[1]`, `[1,1]` all raise `Divergent` |
| K4 | Xu's point spectrum `{0,1}` | `[2,−1]` gives exactly `R = +1` |
| K5 | `φ_E = 32φ_B4` ⇒ identical exact `R` | identical at all 19 rungs |
| K6 | ladder coverage | 19 rungs / 38 primary rows, all bounds hold |
| K7 | enclosure width < distance to ceiling | `1.4e−59` ≪ `1e−9` |
| K8 | independent 200-digit `Decimal` path | agrees to `<1e−190` |
| K9 | by-parts identity `num + den/2 + 2·nonlocal = 0` | **0 exactly** for B4/E; **nonzero for A4** — two-sided |
| — | structural matrix identity | §6.3 |

**All eleven pass.** Five (K2, K3, K4, K5, K9) and K7 were pre-registered as
able to come out against the leg's headline.

**Corollary that settles a question leg 329 left open:** since `φ_E = 32φ_B4`
exactly, the exact quotient is identical for the two weights, so leg 329's C4
difference between its two rows (`−5.19e−18` vs `−1.42e−18`) is **noise, not
signal**.

## 7. The mandatory second reading

Pre-registered in `writeup/novelty/leg_340.md` §7e before the run, and reported
here as part of the answer:

> Because `R = −1/2` is an **identity** on `T2_egm`, clause 5
> (`gap ≤ 1/2 + 1e-9`) is a **tautology** on this class. It cannot come out any
> other way, for any admissible trial function, at any truncation, in any
> arithmetic. The quantity carries **no information about the operator** beyond
> the two constraints themselves — lesson 90 in its purest form, met as an exact
> matrix identity rather than a suspicion. **A flip of leg 178's `NO` on this
> clause would be a flip ON AN IDENTITY, not a measurement of a coercivity gap.**

Both readings are the leg's output. Neither is suppressed.

Leg 178's `+0.4999930` is now fully explained rather than merely suspected: the
continuum value is exactly `1/2`, `cond(G) ≈ 2.55e+11`, and the deficit is
arithmetic. Leg 329's artifact explanation stands **refined, not overturned**.

## 8. What this does not establish

- **No usable coercivity gap.** The estimate is *saturated*, not strict; there
  is no slack for the perturbation argument a blow-up proof requires.
- **Nothing about `a ≠ 0`**, where EGM's `−C|a|` term lives and where the
  estimate does work.
- **No Stage claim**; no `L1`–`L4` link moves; `plan_of_record.py` untouched.
- **No resolution of parked escalation #3** — the DM's cycle-8e ruling makes
  that the user's decision. Leg 178's gate text is byte-identical and untouched.
- **No mathematical novelty.** The inequality is EGM's; the ceiling is Xu's; the
  half-angle substitution and Beta-function moments are elementary. This leg
  owns only the measurement that the quantity is an identity.

## 9. Reproduce

```
python3 experiments/p2_route_egrb_v1.py             # ~59 s, writes the JSON
python3 writeup/figures/fig89_route_egrb_v1_evidence.py   # 28 checks + fig89
```

`writeup/build_figures.py` is deliberately not edited — it is outside this leg's
declared territory, so the evidence script runs standalone and registration is
left to integration, the same choice leg 329 recorded for `fig81`.
