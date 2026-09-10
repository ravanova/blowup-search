# Leg 432 — AMENDMENT to `leg_432_prereg.md`, COMMITTED BEFORE THE RUNNER EXISTS AND BEFORE ANY NUMBER

**Why an amendment and not a correction:** no number exists yet. Writing the runner's algebra by hand
from Lemma A.8's tail representation (p. 140) showed that two pre-registered gates test a limit that
no float64 grid can reach, and that one modelling choice ("`H(2d/X)` set to 1") is wrong for route A.
The original file is not edited. Everything here was derived, not measured; the derivation is what the
runner implements, and **H0 is the check that the derivation is the paper's**.

## 1. The derivation (tail: `U = 0`, `E = E_pow f_o H_Z`, `E_pow = c_∞ X^{−A}`, `H_Z = 1 − κ/X`, `κ = 2h(1+h)d`, `d = 1 − η²`)

The heat factor **must be kept to first order in `Z = 2d/X`** because (4.11) multiplies `Q_s` by `X`:
`X · O(1/X) = O(1)`. With `P = ρ_o J_ψ`, `J_ψ(y) = ∫_y^3 e^{(1−h)(y′−y)} ψ_o dy′`, `G_ψ = ∫_y^3 e^{−h(y′−y)} ψ_o dy′`:

- `I = X H_pow [1/(1−h) + P + κ G/X]`, `G = 1/h − ρ_o G_ψ`; `I_η = H_pow κ_η G`.
- `Q_s = 𝒜/f_o + Q⁽¹⁾/(X f_o) + O(X⁻²)`, **`𝒜 = ρ_o[ψ_o + (1−h)J_ψ]`**, `Q⁽¹⁾ = κ[1 + (1−h)P + (1−h)G] − Dη κ_η G`.
- Beyond `X_b`: `X Q_s → κ/h − Dη κ_η/h = 2(1+h)(1 − 2hη²) = a L` **exactly** — so `T_{0,θ} = F(XQ_s/L − a) = 0`
  there *only with the heat factor*; with `H ≡ 1`, `T_{0,θ} → −F a ≠ 0` (the power law's own viscous residual).
- **`T_{0,θ} = E_pow √(X/2) [ 𝒜/L + ℬ/X ]`**, `ℬ = (2+2h)ρ_oψ_o + 2f_o′ − [κρ_oψ_o + ρ_oG_ψ(κ(1−h) − Dηκ_η)]/L`.
- **`T_{0,z} = (c_∞² X^{1/2−2A}/(√2 L)) · η [2A 𝒮_{2A} − 2h 𝒮_{2h}] + O(1/X)`**, `𝒮_α(y) = ∫_0^{3−y} e^{−αs} Φ(y+s) ds`,
  `Φ = 1 − f_o² = ρ_oψ_o(2 − ρ_oψ_o)`; the `1/α` parts cancel identically, the heat terms are `O(1/X)`.
- Route B, translated (`s = r²/2 = qX`, `y_t = 1/(qL)`, `y_z = −2η/(q^D L)` — `q^D`, an exponent, not a product):
  third term of (A.54) `= E_pow√(X/2)·𝒜/L` (by parts, exactly); boundary `= E_pow√(X/2)·2f_o′/X`;
  second `= E_pow√(X/2)·(2+2h)[ρ_oψ_o − hρ_oG_ψ]/X`; the heat piece of the third `= −E_pow√(X/2)·κ[ρ_oψ_o − hρ_oG_ψ]/(LX)`.
  Route A and route B agree in `ℬ` through `O(h)`; **they may differ at `O(h²)`, which `h = 10⁻³` resolves at `10⁻⁶`.**
  `T_z`: `(A.53)+(A.46)` give `√2 η c_∞² X^{1/2−2A} ∫_0^{3−y} e^{−2As}(e^s − 1) f_o f_o′ ds / L`, equal to route A by parts.

**Consequence for (A.48)–(A.50).** The inviscid term carries `δ⁰` (Lemma A.9 with `j = 3`), the boundary
term `δ⁻³`; their ratio is `≈ X δ³/(8 g(0) L)`. The collar where the boundary term dominates, hence
where `T_{0,θ} ∝ δ⁻³` and `T_z/T_θ ∝ δ⁶`, is **`δ ≲ (8L/X)^{1/3}`** — at this profile's `X_b ≈ 10^{207}`,
`δ ≲ 10^{−69}`. At every resolvable `δ`: `T_{0,θ} ∝ e^{−4/δ²} δ⁰`, `T_{0,z} ∝ e^{−4/δ²} δ³`, ratio `∝ δ³`.
The paper's *conclusions* (positivity, the direction `→ (1,0)`, smooth extension, `(a−2)(T_z/T_θ)² < 2`
with slack) hold either way; its *quoted powers* are the `δ → 0` limit. **This is what the runner will
measure; it is written down here before it is measured.**

## 2. The gates, amended (H1, H4, H5, H6 unchanged)
- **H0** two routes: `T_{0,θ}` totals to relative `10⁻⁶`; **the sub-dominant brackets `ℬ^A` vs `ℬ^B` to `10⁻⁶`
  separately** (the total cannot see them: `ℬ/X ≈ 10^{−207}`); `T_{0,z}` to `10⁻⁶`; both `h`.
- **H2** (i) the boundary term alone, `e^{4/δ²}δ³ · 2E_pow f_o′/√(2X)`, against `b_θ(0,η) = 16ρ_oE_pow(X_b)g(0)/√(2X_b)`:
  within 0.5 at `δ = 0.05` and improving over `δ ∈ {0.4, 0.2, 0.1, 0.05}`; (ii) the local `δ`-power of
  `e^{4/δ²}T_{0,θ}` at `δ = 0.05` in `[−0.5, 0.5]`; (iii) the boundary fraction `ℬ/(X𝒜)` and the crossover
  `δ_× = (8g(0)L·𝒜̂⁻¹…)^{1/3}` **reported**; (iv) the original "`T̂_θδ³ → b_θ(0,η)`" is recorded **NOT TESTABLE**.
- **H3** local `δ`-power of `|T_z/T_θ|` at `δ = 0.05` in `[2.5, 3.5]`; `sup |T_z/T_θ|/E_pow = C` reported, `< 10`;
  the original `[5.5, 6.5]` recorded **NOT TESTABLE**.
- **H7** `𝒜 = ℬ = 0` and the `T_z` bracket `= 0` **exactly** for `y ≥ 3`; `δ³∂_δ log T_{0,θ} ∈ [7, 9]` at `δ = 0.05`.
- **K6 (new control)** `κ → 0` (drop the heat factor): **H7 must fail** with `ℬ(y ≥ 3) = −(2+2h)`.
  K1–K5 unchanged. Each control's twin is the unmodified run.

## 3. Inputs pinned
`log X_tail = log X_R + y_tail` and `c_∞` from the banked `λ = 0.1` run of leg 430 (`params.tail_start`,
`G5.c_inf`); `h ∈ {10⁻⁷, 10⁻³}`, `c_o = 0.1`, `ρ_o = c_o h`; `y ∈ [0, 3.5]`, `dy = 10⁻³`; Chebyshev 17 points in
`η`; `q ∈ {1, 10, 10³}` for route B. All flat quantities are carried as `e^{4/δ²} × (·)`; nothing underflows.
**Tier 2. Not a proof. Moves no wall.**
