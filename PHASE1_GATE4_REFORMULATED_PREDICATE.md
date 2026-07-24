# Reformulated Gate 4 predicate — inviscid rank-based growth-rate currency

**STATUS: FROZEN — 2026-07-24, reviewed and signed off (3 improvements folded in:
rank-stability across all three resolutions, split-dominance promoted to a gate
condition (6g), and a t_res-proxy interrogation (6h); winner-not-at-split-rail
(6b′) added while designing the adversarial roster).** Pre-run contract for the
reformulated Gate 4 on the `g_frac` currency, after the 256→512 rank check passed
(Spearman +0.905; PHASE1_GSUSTAINED_RESULTS.md "RESOLVED"). Implemented by
`analyze_phase1_gate4_reform.py` (the frozen predicate) over
`phase1_gate4_reform.py`'s measurements; both committed BEFORE the run so any rail
is a finding, not a nudge — the same produce/judge discipline as the ν_crit Gate 4.
Per the banked lesson (a pre-committed predicate is necessary but not sufficient;
Gate 4 already produced one false 6/6 pass), the substantive anti-cheat audits are
gate conditions here, not post-hoc diagnostics.

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
fixed energy). Measured at **N ∈ {128, 256, 512}** (property 4 needs both refinement
steps; 128 solves are cheap; property 6 evaluated at N=512).

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
The magnitude is on the wall, so the **ranking** is tested, not the value, and
across **both** refinement steps (128→256→512) so a slow rank-erosion a single
pair would miss is caught:
- (a) `Spearman(rank g_frac @128, @256) ≥ RANK_MIN` **and**
  `Spearman(rank g_frac @256, @512) ≥ RANK_MIN` over the growers;
- (b) **not degrading:** the 256→512 Spearman is not materially below the 128→256
  one (`sp(256,512) ≥ sp(128,256) − RANK_EROSION`) — the ranking is converging or
  flat with N, not drifting onto the wall;
- (c) rail analog: **0** growers may flip grower→non-grower under refinement (a
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
- (b′) **Winner not at a split rail:** `SPLIT_RAIL_LO < winner split <
  SPLIT_RAIL_HI` — a max-split (ω₀→0) shape must not top the landscape. The roster
  deliberately seeds high-split adversarial shapes; if one wins, this fails. (Closes
  the hole where a split-cheat shape passes (a) and (b) because its *base* geometry
  is structured.)
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
- (g) **Structured gradient BEYOND split** *(the key strengthening — split
  dominance is a gate condition, not a caveat):* `g_frac` must discriminate
  ω-geometry after split is controlled, so a split-binned MAP-Elites archive has a
  real within-bin gradient to select on. Decisive condition: partial
  `ρ(g_frac, centroid | split) ≥ RESIDUAL_MIN` (on the random growers). *De-risk
  hint: this partial was only +0.09 — this condition is expected to be stringent
  and may FAIL. A fail is the constructive finding "g_frac is split-dominated →
  usable only with split as a **binned** descriptor axis" (a Gate-3 descriptor
  revisit), not a dead end.*
- (h) **More than a formation-time proxy:** `ρ(g_frac, t_res)` is strong (−0.70),
  so the currency must carry ω-geometry signal beyond "when tail_guard trips":
  partial `ρ(g_frac, centroid | t_res) ≥ RESIDUAL_MIN` (structure survives the
  t_res control). Guards against `g_frac` collapsing to a trivial `−t_res` proxy.

## Frozen thresholds (proposed — set by principle, with observed de-risk values shown)

Thresholds are set by *principle*, not tuned to the observed numbers (tuning a gate
to the data is itself a false-pass mechanism); the observed de-risk value is shown
only to confirm each bar has margin.

| constant | value | principle | observed (de-risk) |
|---|---|---|---|
| `G_MIN` | 0.10 | clearly-positive log-rate, above the flat control (0.0) | control 0.0; mild 0.42 |
| `NONZERO_FRAC` | 0.80 | inherited from ν_crit gate | — |
| `WINDOW_ROBUST` | 0.90 | ranking insensitive to the window knob | (to measure) |
| `RANK_MIN` | 0.85 | de-risk bar; clearly above chance/half-preserved | +0.905 (256→512), +0.90 (128→256) |
| `RANK_EROSION` | 0.10 | 256→512 rank not materially worse than 128→256 | +0.005 (improved) |
| `RESIDUAL_MIN` | 0.15 | g_frac adds real structure signal beyond split | +0.09 (⚠ may FAIL) |
| `WIDEBAND` | 0.30 | top grower ≳1.3×/window faster than slowest | ~1.0 span |
| `WINNER_CENTROID_MIN` | 1.3·√2 | inherited; clearly above the (1,1) floor | winner 1.59 |
| `SPLIT_RAIL_LO/HI` | 0.15 / 0.85 | winner not at a split extreme (ω₀→0 cheat) | winner ~0.5 |
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
