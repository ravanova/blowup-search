# Leg 430 — unit `R5`(i) PRE-REGISTRATION: THE LEADING-ORDER PROFILE, BUILT FROM THE PAPER'S SCHEDULE

**COMMITTED BEFORE THE RUNNER EXISTS AND BEFORE ANY NUMBER IS PRODUCED.** SERIAL, the Conductor's.
Charter: *"(i) the leading-order self-similar concentrating axisymmetric vortex (§4); check
exponents and profile against the paper's."* Everything below is fixed. A change after a number
exists is a `CORRECTIONS.md` entry, not an edit. **This is Tier 2. Nothing here is a proof and
nothing here verifies the theorem.**

## 1. What is built

**The outer reference profile of Lemma 4.8 / Proposition A.4**, in the paper's own variables, from
the paper's own schedule (Appendix A.2), with its moments closed as in A.3 and its stress cone
tested as in A.5 — *not* a profile of my own with the paper's scalings (that was `U4`, leg 420).
Concretely, on the logarithmic radius `y = log(X/X_R)` and the axial parameter `η ∈ [−1, 1]`:

- **prescribed:** `l = X∂_X log H` stage by stage per A.2 — inner reference `l = 3/5` (`E = P_* f x^{1/10}`,
  `U = 4η`, `f = (1+η²)^{-1}`), axial transition `l = (3/5)(1−σ)` then `l = 0` with `U = k(y)η` on
  `[0, T_d]`, intermediate `l = −λσ` then `l = −λ` for `T_w = 60 log(1/λ)`, axial pulse `U = E R_b`
  with `R_b = Amp(η)R_0(λy) + c_1β_1 + c_2β_2`, profile interpolation (A.10) then the
  η-independent hold `30 log(1/λ)` with two relative `E` bumps (A.11), exterior transition
  `−λ → −1` (held `4 log(1/h)`) `→ −h` (held until `Q_s = Q_p`), terminal tail (A.12)–(A.13);
- **derived:** `E` from `log E = ∫(l − 1/2)dy`; `H = √(2X)E`; the five cumulative integrals (4.15)
  carried as the **normalised ratios** `M/X, I/(XH), J/(XH), S/(XE²)` (so nothing overflows across
  ~400 units of `y`) with the inner branch `x ≤ 1` in closed form; `Π` normalised to vanish at
  infinity (4.25); `V_0`, `W` from (4.7)–(4.8); `Q_s, N_s` from the explicit formulas (4.16) with
  η-derivatives taken spectrally on a Chebyshev grid; `a = 2 − 2l`, `b_s = 2D_X U/E`, `p_s`, `T_0`
  from (4.11); the cone quantities (4.20) and the sufficient test (A.24) with `w = N_s/(EQ_s)`.
- **closed:** `c_1, c_2` from `M = J = 0` at pulse end (affine in `Amp`); `Amp(η)` from `S(∞) = 0`
  by bracketed root-finding on **[.9, 1.2]**, the paper's bracket; the two (A.11) bumps by the
  Lemma A.2 iteration; the exterior `−h` hold length by integrating `Q′ + (1+l)Q = −l − h` to `Q_p`.

**Parameters, in the paper's order (A.6):** `M_d = 1` → `T_d = e + 10`; `P_* = 2e^{T_d}`; `λ ∈ {0.1,
0.05, 0.025}` (three values, for the scaling checks); `h = 10^{-7}` (`< min{1/100, λ, e^{−T_d}}` for
all three); `T_f = 10`; `c_o = 0.1` (so `f_o′/f_o < h/4`); `X_R = 10^{12}`. Grid: `dy = 2·10^{-3}`,
Chebyshev `N_η = 24`. **The runner refuses to run if any ordering constraint in (A.6) is violated.**

## 2. What is measured, and THE PRE-COMMITTED GATES

Every number below is the paper's (page cited); the tolerance is stated now.

| gate | quantity | pre-committed | source |
|---|---|---|---|
| **G1** | `K_b = ∫_0^{13} e^{−2ξ}R_0(ξ)² dξ` | `.20 < K_b ≤ .25` | p. 133 |
| **G2** | principal amplitude function `P(A) = A²K_b − (1+e^{−26})/4` | `P(.9) < −.047`, `P(1.2) > .038`, `P′ ≥ .36` on the bracket | p. 133, (A.19) |
| **G3** | closure `S(∞) = 0`: root `Amp(η)` | one root in `[.9, 1.2]` for every `η`; normalised residual `|λS(∞)/(X_p e_b² f²)| < 10^{-9}`; the remainder `E(Amp, η)` of (A.19) and `∂_η Amp` both scale as `λ(1 + log(1/λ))`: the ratios `|E|/(λ(1+log 1/λ))` and `|∂_ηAmp|/(λ(1+log 1/λ))` change by **less than a factor 2** between `λ = 0.1` and `λ = 0.025` | (A.19)–(A.20) |
| **G4** | `M, J` after the pulse; `I/(XH)` after the angular correction; pressure change of the two (A.11) bumps | `|M|, |J| < 10^{-10}` (relative to `X_p e_b f`, `X_p H e_b f`); `|I/(XH) − 1/(1−λ)| < 10^{-8}`; `|ΔC_p| < 10^{-10}` relative | (A.15), (A.11) |
| **G5** | the angular moment identity `∫_0^∞ (H − H_pow) dX = 0` with `c_∞` read off the tail | `|∫(H−H_pow)dX| / ∫|H−H_pow| dX < 10^{-6}` | (A.8), p. 132 |
| **G6** | exponents: `d log E/dy` on the reserved patches; `U` there; `d log E/dy` in the tail; the decay `e_b` of `E/f` at pulse start across the three `λ` | `−1/2 − λ ± 10^{-9}`, `U = 0` exactly; `−A ± 10^{-9}`; fitted `d log e_b / d log λ ∈ [30, 36]` | (4.30), (A.14): *"`e_b ≤ C_pre λ^{30}`"* |
| **G7** | the sufficient cone test (A.24) on the intermediate interval, the pulse, the interpolation and the exterior transition (to tail coordinate ½); `v_s > 2` there; the pulse margins | **both inequalities at every grid point**; `sup_pulse b_s w < .74`, `sup_pulse (2b_sw + b_s²/a + (a−2)w²) < 1.68`; `sup_int √λ|w| < .25` and decreasing in `λ` | p. 136, (A.27) |
| **G8** | pressure datum | `Π_0/(P_*²f²) ≤ −5/2` at every `η`, `Π_0` even, `ηΠ_0′ > 0` | (A.22) |
| **G9** | relaxed cone on the inner reference interval `x ∈ [e^{−5}, 1]`: `X_R` needed for `P_c > 2` | reported, not gated (it is the *"sufficiently large `X_R`"* of Prop A.4) | p. 131 |

**The gate answer** is the list G1–G8 each `YES`/`NO` with its number, and one sentence:
*"the outer profile of Lemma 4.8 is reproduced from the paper's schedule to these tolerances, or is not,
and here is where"*. **Widening a tolerance after seeing a number is the failure this repository
has caught in itself before (§60, §64). If I feel the pull, the temptation is recorded, not acted on.**

## 3. Planted controls — fixed now, firing in BOTH directions
- **C1** `λ → −λ` on the intermediate interval (`l = +λ`): `v_s = 2 − 2l < 2` — G7 **must fail**.
- **C2** `Amp = 0.5` (outside the bracket): normalised `|λS(∞)/(X_p e_b² f²)| > 0.05` — G3 **must fail**.
- **C3** drop `c_1, c_2`: `|M|` or `|J|` at pulse end `> 10^{-3}` relative — G4 **must fail**.
- **C5** drop the two (A.11) bumps: `|I/(XH) − 1/(1−λ)| > 10^{-3}` at the hold end **and** G5 **must fail**.
- **C6** truncate `R_0` at `ξ_b = 5` instead of `10`: `K_b` leaves `(.20, .25]` or the root leaves the bracket — G1 or G2 **must fail**.
- Each control's twin is the unmodified run, which **must pass** the same check.

## 4. Ceiling, said in advance
Float64, a fixed grid, one parameter triple. A profile that passes G1–G8 is **one instance of Lemma
4.8's outer profile computed to stated tolerances**; it is not Theorem 4.6 (no axis profile, no
heat compensation, no shear modulation), not a proof of anything, and it moves no wall. **It does
not verify the theorem**, and `R4`'s verdicts on Proposition A.4 are independent of it.

## 5. What comes next (pre-commit)
`R5`(ii) — the residual stress this profile leaves: `T_0 = F(p_s − s)` on the annulus, its support
`(X_a, X_b)`, the flat weight `ζ` at the outer edge (A.48)–(A.51) and its size and scaling in `q`.
