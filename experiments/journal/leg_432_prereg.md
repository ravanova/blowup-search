# Leg 432 — unit `R5`(ii) PRE-REGISTRATION: THE RESIDUAL STRESS THE OUTER PROFILE LEAVES

**COMMITTED BEFORE THE RUNNER EXISTS AND BEFORE ANY NUMBER IS PRODUCED.** SERIAL, the Conductor's.
Charter: *"(ii) the residual stress this profile leaves: `T_0 = F(p_s − s)` on the annulus, its support
`(X_a, X_b)`, the flat weight at the outer edge (A.48)–(A.51) and its size and scaling in `q`."*
Everything below is fixed. A change after a number exists is a `CORRECTIONS.md` entry, not an edit.
**This is Tier 2. Nothing here is a proof and nothing here verifies the theorem.**

## 1. What is built, and why it is computable at every `λ`

The **terminal tail** of the outer profile — `y = log(X/X_tail) ∈ [0, 3]`, `X_b = e^3 X_tail` — where
`U = 0`, `E = E_pow f_o`, `E_pow = c_∞ X^{−A}`, `A = ½ + h`, and `f_o = 1 − ρ_o ψ_o`,
`ψ_o = 1 − σ((y−1)/2)`, `ρ_o = c_o h` (A.12), with the (A.5) step `σ` — exactly the tail
`experiments/arc6_profile_v1.py` already builds (`Schedule.f_o`). Writing `δ = 3 − y`,
`ψ_o = e^{−4/δ²} g(δ)`, `g(δ) = 1/(e^{−(1−δ/2)^{−2}} + e^{−4/δ²})`, `g(0) = e` (p. 143).

Lemma A.8 (p. 140) gives the stress on `y ≥ ½` by integrals **from `X` to infinity** under the exact
moment hypotheses `M(∞) = J(∞) = S(∞) = 0`, `∫(H − H_pow) dX = 0`. Under those hypotheses the tail
stress depends on the tail alone, so **the closure failure of `R5`(i) at computable `λ` does not
touch this unit**: the moment conditions are *imposed* here, as Lemma A.8 imposes them, and what
`R5`(i) found about closing them at finite `λ` is not re-litigated. `λ` enters only through `X_tail`
and `c_∞`, which scale the answer and are reported; **`λ = 0.1`, `h ∈ {10^{−7}, 10^{−3}}`**, `c_o = 0.1`,
`X_R = 10^{12}` as in leg 430; grid `dy = 10^{−3}` on `y ∈ [0, 3]`, Chebyshev `N_η = 16`.
The heat factor `H(2d/X)` of (A.39) is **set to 1**: `|H − 1| ≤ C h Z`, `Z = 2d/X ≤ 2d e^{−y_tail}/X_R`
(A.36), which at these scales is below `10^{−100}` for any `d ≤ 10^{10}`; the bound is reported.

**Two routes to the same stress**, both computed, in scaled form `T̂ = e^{4/δ²} T_0` so nothing underflows:
- **Route A, (4.11):** `T_0 = F(p_s − s)`, `p_s = (X Q_s/L, X N_s/(L E))`, `s = (a, −b_s)`, `a = 2 − 2l`,
  `b_s = 0`, with `Q_s`, `N_s` from Lemma A.8's representations `I(X) = X H_pow/(1−h) − ∫_X^∞ (H − H_pow) dx`,
  `S(X) = ½ ∫_X^∞ E² dx`, `Q_s = −1 + ((1−h) I − D η I_η)/(X H)`, `N_s = (4hηS − d S_η)/X + 4Aη Π − d Π_η`,
  `Π = −½ ∫_X^∞ E²/x dx` (p. 140), `W = 1`.
- **Route B, (A.54)/(A.46):** the paper's exact backward formula on the heat tail, `T_θ = K f_r +
  r^{−2} ∫_r^∞ (r′K − r′² K_{r′}) f_{r′} dr′ + (qL r²)^{−1} ∫_r^∞ r′² K f′ dr′`, `T_z = r^{−1} ∫_r^∞ r′ p_z dr′`,
  `p_z = (2η/(qDL)) ∫_y^3 K² f f′ dy′` (A.53), with `s = r²/2 = qX`, `K = c_∞ s^{−A}`, `f = f_o`,
  `T = q^{−A−½} T_0`, `D = 1 − A`, `L = 1 − 2hη²`, evaluated at explicit `q`.

## 2. What is measured, and THE PRE-COMMITTED GATES

| gate | quantity | pre-committed | source |
|---|---|---|---|
| **H0** | route A vs route B | `|T̂_θ^A − T̂_θ^B| / T̂_θ^B < 10^{−6}` and `|T̂_z^A − T̂_z^B| / |T̂_z^B| < 10^{−6}` at every grid point of `y ∈ [½, 3 − 0.05]`, every `η` | Prop 4.2, Lemma A.8 |
| **H1** | sign | `T_{0,θ} > 0` at every grid point of `[½, 3)`; each of the three terms of (A.54) `≥ 0` there | p. 142 |
| **H2** | the flat factorisation (A.48) | `T̂_θ δ³ → b_θ(0,η) = 16 ρ_o E_pow(X_b) g(0)/√(2X_b)`: the two integral terms of (A.54) relative to the boundary term are `≤ 2δ³` for `δ ≤ 0.3`, with the log–log slope of that ratio on `δ ∈ [0.05, 0.3]` in `[2.7, 3.3]`; and `|T̂_θ δ³ / b_θ(0,η) − 1| < 0.5` at `δ = 0.05`, decreasing over `δ ∈ {0.4, 0.2, 0.1, 0.05}` | (A.48), p. 143 |
| **H3** | the direction (A.49)–(A.50), (A.55) | local log–log slope of `|T_z/T_θ|` against `δ` at `δ = 0.05` in `[5.5, 6.5]` and nearer 6 than at `δ = 0.2`; `log10 sup_{[½,3)} |T_z/T_θ| / E ≤ log10 C` with `C` reported and `< 10^3` | (A.50), (A.55) |
| **H4** | the shear bracket (A.56) | `2 + h < a ≤ 2 + 2h` at every grid point of `[½, 3)`, both `h` | (A.56) |
| **H5** | the admissible cone on the tail | `v_s = a`; `P_c − v_s = T_{0,θ}/F > 0`; `log10 sup (a−2)(T_z/T_θ)² < −3` on `[½, 3)` | p. 143 |
| **H6** | scaling in `q` | route B at `q ∈ {1, 10, 10³}`: `q^{A+½} T_θ` and `q^{A+½} T_z` agree to relative `10^{−10}`; with `D = A` instead of `D = 1 − A` they do **not** (reported) | p. 143, `q^{1−D−A} = 1` |
| **H7** | support and (A.51) | `T̂_θ = T̂_z = 0` exactly for `y ≥ 3` (the stress vanishes beyond `X_b`); `δ³ ∂_δ log T_{0,θ} ∈ [7, 9]` at `δ = 0.05` (the `e^{−4/δ²}` weight, `8/δ³` leading) | Lemma A.8, (A.51) |
| **H8** | the inner edge `X_a` | reported, not gated: the first `y` on the outer profile at which `|T_0| / (F·max(|p_s|,|s|)) > 10^{−12}` — the paper's `X_a` is fixed by the axis construction (Prop B.2, Cor B.10), which this unit does not build | p. 149 |

**The gate answer** is H0–H7 each `YES`/`NO` with its number and one sentence: *"the residual stress of
Proposition A.10 — its sign, its `e^{−4/δ²} δ^{−3}` outer weight, its `δ⁶` direction, its shear bracket
and its `q`-invariance — is reproduced on the tail to these tolerances, or is not, and here is where."*
**No tolerance is widened after a number exists (§60, §64); a temptation is recorded, not acted on.**

## 3. Planted controls — fixed now, firing in BOTH directions, each with its unmodified twin
- **K1** replace `ψ_o` by the polynomial cutoff `(δ/2)^4` on `[1, 3]` (same endpoints, no flat factor):
  **H7's slope test must fail** (`δ³ ∂_δ log T → 0`, not 8) and **H2 must fail**.
- **K2** exponent bookkeeping `D = A` in route B: **H6 must fail** (relative change `≈ 2h log q`).
- **K3** leave a residual angular moment: `I(X) → I(X) + ε X_b H_pow(X_b)`, `ε = 10^{−3}`: **H7's
  vanishing beyond `X_b` must fail** (`Q_s ≠ 0` there).
- **K4** reverse the cutoff, `f_o → 2 − f_o` (`f_o′ ≤ 0`): **H1 must fail**.
- **K5** `h → −h`: **H4 must fail**.

## 4. Ceiling, said in advance
One tail, two `h`, float64, the moment conditions imposed rather than closed. A pass is **one instance of
Proposition A.10's tail stress computed to stated tolerances**; it says nothing about the annulus's
inner edge, nothing about Theorem 4.6, and **moves no wall. It does not verify the theorem.**

## 5. What comes next (pre-commit)
**Wave 4 = `R5`(iii)–(vii) FAN-OUT ×5** on the interface `R5`(i)–(ii) pin (`λ = 0.1` profile, its tail
stress, the measured `λ`-regime finding of leg 430), slot 5 the adversarial verifier drawn blind, gates
and planted controls in every brief, *this is Tier 2, not a proof* in every gate answer.
