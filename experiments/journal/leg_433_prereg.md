# Leg 433 — WAVE 4 PRE-REGISTRATION: `R5`(iii)–(vii) FAN-OUT ×5 (four workers + the adversary)

**COMMITTED AND PUSHED BEFORE ANY AGENT IS DISPATCHED (§3g).** The Conductor's. Every gate below is
quantitative and fixed now; a change after a number exists is a `CORRECTIONS.md` entry. **Every unit is
Tier 2: nothing here is a proof and nothing verifies the theorem.** Wave sizing 5 by user ruling (§67).

## 0. The pinned interface every unit builds on (legs 430, 432 — on `main`)
- **The outer profile** (`writeup/data/arc6_profile_v1.json`, `λ = 0.1`, `h = 10⁻⁷`, `M_d = 1`, `P_* = 2e^{T_d}`,
  `X_R = 10¹²`): its stage boundaries (`params.stage_starts`, `tail_start`), `c_∞` (`G5.c_inf`), the
  reserved patches (`E = c f X^{−1/2−λ}`, `U = 0`), the tail `E = c_∞ X^{−A} f_o`, `A = ½ + h`.
  **Known and not re-litigated:** its closure (G3) and cone (G7) fail at every computable `λ`; the paper's
  regime is `λ ≲ 3·10⁻⁴` and `√λ P_* ≪ 1` (`leg_430.md`). **Every gate answer must say what is
  instantiated at computable `λ` and what is measured only as a scaling toward the paper's regime.**
- **The tail stress** (`writeup/data/arc6_residual_v1.json`, `leg_432.md`): on `y = log(X/X_tail) ∈ [0, 3]`,
  `T_{0,θ} = E_pow √(X/2)[𝒜(y)/L + ℬ/X]`, `𝒜 = ρ_o[ψ_o + (1−h)J_ψ]`, `T_{0,z} = c_∞²X^{½−2A}η[2A𝒮_{2A} − 2h𝒮_{2h}]/(√2L)`,
  both **exactly zero for `X ≥ X_b = e³X_tail`** (with the heat factor), flat weight `e^{−4/δ²}`, `δ = 3 − y`;
  `T = q^{−A−½}T_0` physically. Scaled fields are banked in the artefact (`fields`).
- **Scales:** `s = r²/2 = qX`, `q ↓ 0` as `t ↑ 1` (each unit states the paper's `q(t)` with page), `y_t = 1/(qL)`,
  `y_z = −2η/(q^D L)`, `D = 1 − A`, `L = 1 − 2hη²`, `d = 1 − η²`.
- **Tools:** `.venv/bin/python` (numpy 2 → `np.trapezoid`, scipy); the manuscript text
  `writeup/data/arc6/manuscript_pages.txt` (`<<<PAGE n>>>` markers) and the ledger `writeup/data/arc6/ledger.json`
  (79 statements: hypotheses, conclusions, constants, pages); `experiments/arc6_profile_v1.py`,
  `experiments/arc6_residual_v1.py` (import their functions; do not edit them).

## 1. Ownership (ONE FILE, ONE OWNER — two files each, nothing else)
| slot | unit | runner (owned) | artefact (owned) | branch |
|---|---|---|---|---|
| 1 | (iii) pulses | `experiments/arc6_w4_pulses.py` | `writeup/data/arc6/wave4/agent_3_pulses.json` | worktree |
| 2 | (iv) iteration | `experiments/arc6_w4_iteration.py` | `writeup/data/arc6/wave4/agent_4_iteration.json` | worktree |
| 3 | (v) headline | `experiments/arc6_w4_headline.py` | `writeup/data/arc6/wave4/agent_5_headline.json` | worktree |
| 4 | (vi) support | `experiments/arc6_w4_support.py` | `writeup/data/arc6/wave4/agent_6_support.json` | worktree |
| 5 | (vii) adversary | `experiments/arc6_w4_adversary.py` | `writeup/data/arc6/wave4/agent_7_adversary.json` | worktree |
Each agent commits its two files on its own worktree branch (`Leg 433: W4 agent <n> — <what>`), pushes
nothing, edits nothing else. **Slot 5 never sees slots 1–4's files; slots 1–4 never see slot 5's.**
Every artefact carries `schema: arc6_wave4_v1`, `agent`, `leg: 433`, the paper pages read, a
`claimed` block quoting the paper (page, equation) **written before the run**, a `measured` block,
`gates` (`YES`/`NO` each with its number), `controls` (fired / did not fire, with numbers),
`instantiated_vs_scaled` (one paragraph), `could_not_determine` (list; *"I could not determine X,
because Y"* is an acceptable answer, inventing X is not), and the sentence **"This is Tier 2, not a proof."**

## 2. Gates, pre-committed

### (iii) Oscillatory realization (§6–§7, pp. 57–99): do the annulus pulses' Reynolds stress cancel the residual at the claimed order?
Build the paper's oscillatory field on the tail annulus `y ∈ [½, 2.9]`: extract **Definition 6.4 / Lemma
6.3 / Proposition 6.6 / Proposition 7.5** (the pulse ansatz: phases, amplitudes, the averaged quadratic
products that realise a prescribed symmetric stress) and instantiate it for the pinned target
`T = (T_{0,θ}, T_{0,z})` at three frequencies `N ∈ {N₀, 2N₀, 4N₀}` (`N₀` the agent's choice, stated).
- **P1** the averaged product `⟨u_osc ⊗ u_osc⟩` reproduces `T` in the two required entries: relative
  `L²` error over the annulus `< 10⁻²` at `4N₀`, and the **convergence exponent in `N`** (fit over the
  three `N`) within **±0.3** of the order the paper claims (the agent quotes the claimed order with page
  and equation in `claimed` before running).
- **P2** the residual after absorption, `‖div⟨u_osc ⊗ u_osc⟩ − div T‖ / ‖div T‖`, decreases with `N` at
  the same exponent (±0.3).
- **P3** the pulses' own leading-order momentum residual is what the paper says it is: the terms the
  paper calls lower order (its `q^{2h}` hierarchy) are measured smaller than the leading term by the
  claimed factor at `q ∈ {10⁻², 10⁻³, 10⁻⁴}` (exponent ±0.05).
- **Controls (both directions):** phase of one component shifted by `π/2` → **P1 must fail** (relative
  error `> 0.3`); amplitude halved → **P1 must fail** with error `≈ 0.75`; the unmodified twin must pass.
- Instantiated vs scaled: the target stress is the computable-`λ` tail's; the annulus pulses' scaling in `q` is a scaling.

### (iv) The iteration (§9, pp. 100–118): does the residual improve at the claimed rate over successive corrections?
Extract **Definition 9.4, Propositions 9.5, 9.6 (the `+1/10` per stage and the closing margins), Lemma
9.7, Proposition 9.9** and the linear problem one correction stage solves (the mean-correction equations
of §8–§9 in the radial profile variables, sourced by the previous residual). Instantiate **at least one
correction stage numerically** on the annulus with the pinned leading residual as source, at
`q ∈ {10⁻², 10⁻³, 10⁻⁴}`, and, if a second stage is feasible, two.
- **I1** the measured residual after one stage over the residual before, as a power of `q`: exponent
  gain within **±0.02 of the paper's claimed `1/10`** (quoted with page in `claimed`).
- **I2** the exponent ledger: implement Prop 9.6's recursion as arithmetic on the paper's constants
  (`h`, the stage index, the margins) and check that Prop 9.9's summation converges with the margin
  the paper states — every margin `> 0` with the smallest quoted (leg 429 found `0.07`).
- **I3** if a second stage runs: the gain repeats within ±0.02.
- **Controls:** zero the correction (skip the solve) → **I1 must fail** (gain `≈ 0`); replace the source by
  its negative → the residual **grows**; twin passes.
- If one stage's linear problem cannot be instantiated in the session: say so, why, and deliver I2 alone with the gate marked `NOT-INSTANTIATED`.

### (v) The two headline quantities (§3–§4): `‖u(t)‖_{L²}` bounded while `‖u(t)‖_{L∞} → ∞` as `t ↑ 1`
For the **leading-order field** `u⁽⁰⁾(x, t)` built from the pinned profile through (4.7)–(4.8) and the
paper's `q(t)` (state it, with page): compute `‖u⁽⁰⁾(t)‖_{L²(ℝ³)}` and `‖u⁽⁰⁾(t)‖_{L∞}` on `t ∈ [1 − 10⁻¹, 1 − 10⁻⁶]`
at **three radial resolutions** (`dy ∈ {4, 2, 1}·10⁻³`) and fit exponents.
- **V1** `L∞` exponent `= −A` (the paper's `q^{−A}` scaling) within `10⁻⁴`, and the `L²` exponent equals the
  exact bookkeeping value the agent derives from `dx dy dz → q dX · q^D dη` **before running** (written in
  `claimed`), within `10⁻⁴`; both stable across the three resolutions to `10⁻⁶` relative in the norm.
- **V2** the force the leading order alone would need, `f⁽⁰⁾ := NS(u⁽⁰⁾)`: its `L∞` exponent in `q` measured
  (±0.01) and reported as **the gap the corrections must close** — the paper's corrected `f` is bounded
  and flat at `t = 1` (Theorem 3.1(iii)); the leading order's is not. Say this plainly.
- **V3** `T* = 1` is *prescribed*; the agent states in the gate answer that "T* stable under refinement"
  in `WIN_CONDITION.md`'s Tier-2 sense **cannot be tested on a prescribed field**, and reports only
  whether the norms' fits are refinement-stable. Conservation drift of the quadratures reported.
- **Controls:** set `A → 3/4 + 0.1` → the `L²` norm **must diverge** (exponent changes sign); set
  `U → 0` in (4.7) → `V_0` changes and the `L∞` norm's location moves (reported); twin passes.
- Instantiated vs scaled: the norms are exact scalings of a prescribed field; **this signal is not evidence of Navier–Stokes blowup by itself** (any prescribed `u` solves NS with `f := NS(u)`); (vii) will say so too.

### (vi) Compact support of `f` (§10, pp. 118–125): check it, do not assume it
- **S1** the leading residual `R⁽⁰⁾ = −div(q^{−A−½}T_0)` (Prop 4.2) is **exactly zero for `X ≥ X_b`** with the
  heat exterior (Lemma A.8): measured from the pinned stress — `max_{X ≥ X_b}|R⁽⁰⁾| = 0` exactly — and its
  physical support radius `r_b(t) = √(2q(t)X_b) → 0` as `t ↑ 1` (reported at three `t`).
- **S2** the support in the *paper's* variables: extract §10's statement of where `f` lives (`X ≤ X_ext`,
  the time window, and the extension by zero at `t = 1`, pp. 118–125, with equation numbers) and check
  each clause the leading order can check; **flatness at `t = 1`** (Theorem 3.1(iii), `|∂R| ≤ C q^N ∀N`)
  is **carried by the corrections, not the leading order**: measure the leading residual's own `q`-exponent
  (a power, not flat) and report the gap; do not claim flatness.
- **S3** the `e^{−4/δ²}` cutoff's role: every fixed derivative of `T_0` at the outer edge is bounded by
  `C e^{−4/δ²}δ^{−N}` (A.51) — measured for `∂_y, ∂_y²` at `δ ∈ {0.4, 0.2, 0.1, 0.05}`: `δ^N·e^{4/δ²}|∂^k T_0|`
  bounded for some `N ≤ 3k + 3`.
- **Controls:** drop the heat factor → **S1 must fail** (residual `= (2+2h)`-sized beyond `X_b`, leg 432's K6);
  polynomial cutoff → **S3 must fail**; twin passes.

### (vii) ADVERSARY: can (iii)–(vi)'s signals be faked?
Given **only §2's gate definitions above** (never the four agents' files or methods), try to produce each
gate's `YES` from a deliberately **under-resolved or mis-specified** run: e.g. (iii) a phase-wrong pulse
field at one `N` with coarse averaging (aliasing); (iv) an ansatz that assumes the `1/10` it then
"measures"; (v) any prescribed profile with `A < 3/4` and `f := NS(u)`; (vi) any smooth cutoff.
- **X1** for each of P1–P3, I1–I3, V1–V3, S1–S3: `FAKEABLE` / `NOT FAKEABLE` / `NOT ATTEMPTED`, with the
  faking run's numbers where fakeable, and **what would make it non-fakeable** (a resolution study, a
  control, a sign, a second route).
- **X2** the verdict sentence: which of (iii)–(vi)'s signals are evidence and which are not, and why.
- The adversary's own runs need no twin; it must state honestly when it could not fake a signal.

## 3. What the Conductor does at integration (pre-committed)
Cherry-pick the ten files unedited; `experiments/arc6_wave4_merge.py` → `wave4/merged.json`; the gate table
(iii)–(vi) with each number, (vii)'s verdict row by row, and the sentence **"this is Tier 2, not a
proof"**; every disagreement between a worker and the adversary is recorded, not adjudicated. A signal
the adversary faked is marked `NOT EVIDENCE` in `STATE.md` whatever the worker's gate said. Then `R7`.
