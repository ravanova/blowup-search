# Reformulated Gate 4 predicate — inviscid rank-based growth-rate currency

**STATUS: DRAFT — for review, NOT yet frozen.** This is the pre-run contract for a
reformulated Gate 4 on the `g_frac` currency, drafted after the 256→512 rank check
passed (Spearman +0.905; PHASE1_GSUSTAINED_RESULTS.md "RESOLVED"). It is committed
as a draft so it can be reviewed *before* it is frozen and run — per the banked
lesson that a pre-committed predicate is necessary but not sufficient, and that a
*reformulated* anti-self-deception predicate must not be rewritten and run in one
unreviewed motion (Gate 4 already produced one false 6/6 pass, PHASE1_GATE4_RESULTS.md).
Nothing runs until this is signed off. Once frozen, the constants below are
committed BEFORE the 40-shape gate so any rail is a finding, not a nudge.

## The fitness under test

`g_frac(shape, N)` = inviscid sustained log-growth-rate of `max|ω|`:

    g_frac = [ log max|ω|(t_res) − log max|ω|(0.5·t_res) ] / (0.5·t_res)

with ν = κ = 0 (no dissipation wall, no ω₀ denominator — it is a *rate*, not a
resistance or a ratio), Hou–Luo parity, measured strictly inside the
tail_guard-trusted window; `t_res` = trusted-window end. **Used as a RANK**, not a
magnitude — its magnitude is on the uniform-grid resolution wall (established in
LEG 1; the rank is what survives, +0.90 at 128↔256 and +0.905 at 256↔512).

- **Grower (uncensored):** under-resolves within [0, T_MAX] — tail_guard trips,
  `t_res < T_MAX − ε` (the shape generates small scales, i.e. heads toward a
  singularity inside the trusted window).
- **Non-grower (censored):** saturates, `t_res = T_MAX`, outcome `no_blowup`.

## Roster (needs a small adversarial extension — see "Open decisions")

The Gate-4 principle is a roster designed to *test* property 6, not dodge it. The
ν_crit gate used 40 shapes (3 controls, 6 trivial low-(1,1) cheats, 3 structured,
28 random spanning centroid×anisotropy×split). For `g_frac` the relevant cheats
differ, so the roster must additionally seed the currency's *own* known failure
modes: **explicit high-split shapes** (test the split→1 rail) and **explicit
low-ω₀ shapes** (test the ω₀ cheat, mechanically entangled with high split at
fixed energy). Measured at **N ∈ {256, 512}** (the de-risked rank pair; property 6
evaluated at N=512).

## The six reformulated properties

Old → new mapping is explicit; only what *must* change for a rank-based inviscid
rate is changed, so the gate stays recognizably the same six.

### 1. Nonzero / discriminating  *(role unchanged: the fitness actually varies)*
≥ `NONZERO_FRAC` of growers have `g_frac > G_MIN`, and the grower g_frac spread is
non-degenerate. Guards against a dead-flat, non-selecting fitness.

### 2. Direction + controls censored  *(replaces "Finite — survives ν=hi")*
The ν=hi "finite" test is **retired as inapplicable** (there is no viscosity in an
inviscid rate). Its role — *the fitness rewards real blow-up propensity, not a
censor-removable artifact* — is carried by an anchor on the labeled ground truth:
- (a) `g_frac(smooth_sharp) > g_frac(smooth_mild) > g_frac(euler_control)` at every
  tested N (direction correct);
- (b) `euler_control` censored low: `g_frac(euler_control) < G_MIN` (an inviscid,
  non-buoyant control must not look like growth).

### 3. Well-posed measurement  *(replaces "Monotone — bisection probes")*
There is no bisection, so the ν_crit monotonicity probe is **retired**. Its role —
*the measurement instrument is well-posed, not an artifact of an arbitrary knob* —
is carried by the currency's one free knob, the window fraction:
- (a) every grower's g_frac is finite (the trusted window covers [0.5·t_res,
  t_res]; no NaN rails);
- (b) window-robustness: `Spearman(rank by g over [0.5·t_res, t_res], rank by g
  over [0.6·t_res, t_res]) ≥ WINDOW_ROBUST`. The ranking must not be driven by the
  arbitrary window fraction. (Free — reuses the same trajectories, no new solves.)

### 4. RANK-resolution-stable  *(REFORMULATED — was |Δν_crit| ≤ 2·tol)*
The magnitude is on the wall, so the **ranking** is tested, not the value:
- (a) `Spearman(rank g_frac @256, rank g_frac @512) ≥ RANK_MIN` over the growers;
- (b) rail analog: **0** growers may flip grower→non-grower under refinement (a
  shape heading to blow-up must not stop under-resolving at finer N; finer N
  resolves *more*, so this is a hard, one-sided bar).

### 5. Wide band  *(role unchanged: a real selection gradient exists)*
Grower g_frac spread `(max − min) ≥ WIDEBAND` — enough dynamic range that
MAP-Elites elite-selection is meaningful (not all shapes tied).

### 6. Non-trivial optimum, CONTROLLING FOR SPLIT  *(REFORMULATED + audits baked in)*
Property 6 has twice been a false pass, so the substantive anti-cheat audits are
**promoted from post-hoc diagnostics to first-class gate conditions** (directly
implementing "pre-committing a predicate is necessary but not sufficient"). ALL of:
- (a) **Winner is a grower** (`t_res < T_MAX`) — caught accel_ratio (winner a
  non-grower).
- (b) **Winner structured, not trivial low-mode:** winner class ≠ trivial AND
  winner centroid ≥ `WINNER_CENTROID_MIN` (the gCLM low-(1,1) trap).
- (c) **Top-5 are growers:** ≥ 4/5 of the top-5 under-resolve.
- (d) **No ω₀ cheat:** `|ρ(g_frac, log max|ω₀|)| ≤ RHO_W0` **and** partial
  `ρ(g_frac, log|ω₀| | split) ≤ PARTIAL_W0` (the ν_crit killer must be absent even
  after freeing split).
- (e) **Structure not dissipation-penalized:** `ρ(g_frac, centroid) > −RHO_MAX`
  (inherited; here expected positive).
- (f) **Split preference is genuine physics, not a rail or an ω₀ artifact:**
  controlled split-sweep (structure fixed, split varied) has an **interior**
  argmax (∉ sweep endpoints — no rail to split=1/0) **and** partial
  `ρ(g_frac, split | log|ω₀|) > 0` (split acts through buoyancy, not by driving
  ω₀→0). Reuses the LEG-3 split-sweep + free-roster instruments.

## Frozen thresholds (proposed — set by principle, with observed de-risk values shown)

Thresholds are set by *principle*, not tuned to the observed numbers (tuning a gate
to the data is itself a false-pass mechanism); the observed de-risk value is shown
only to confirm each bar has margin.

| constant | value | principle | observed (de-risk) |
|---|---|---|---|
| `G_MIN` | 0.10 | clearly-positive log-rate, above the flat control (0.0) | control 0.0; mild 0.42 |
| `NONZERO_FRAC` | 0.80 | inherited from ν_crit gate | — |
| `WINDOW_ROBUST` | 0.90 | ranking insensitive to the window knob | (to measure) |
| `RANK_MIN` | 0.85 | de-risk bar; clearly above chance/half-preserved | +0.905 |
| `WIDEBAND` | 0.30 | top grower ≳1.3×/window faster than slowest | ~1.0 span |
| `WINNER_CENTROID_MIN` | 1.3·√2 | inherited; clearly above the (1,1) floor | winner 1.59 |
| `RHO_W0` | 0.40 | ω₀ explains < ~16% of variance (0.4²) | +0.21 |
| `PARTIAL_W0` | 0.25 | residual ω₀ effect negligible after split | +0.04 |
| `RHO_MAX` | 0.70 | inherited; structure not strongly anti-correlated | +0.31 |
| top-5 growers | ≥ 4/5 | structure, not saturation, dominates the top | 5/5 |

## Pass rule
All six properties must PASS (none failing, none N/A) to clear the gate and
authorize the GA campaign. Any fail is a **finding, not a push-harder signal**.

## Honest framing (unchanged)
Even a full pass buys only a resolution-stable shape→growth QD map with **Tier-1**
candidates on a *toy* model (2D Boussinesq, not 3D NS); the fitness magnitude
remains on the uniform-grid wall, and uniform-grid Tier-2 of the true Hou–Luo
singularity stays out of reach (Route D). Overall Clay odds ~0.05%.
