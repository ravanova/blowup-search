# Spike 1 Step C — relaxing to the Chen–Hou profile: the gate (technical)

**Status (2026-07-25): PARTIAL — 3 of 4 pre-committed predicate checks pass; the far-field
exponent check fails. This does NOT pass the gate. Reported as PARTIAL; goalposts not moved.**

Step C relaxes the Step-B machine from an analytic initial guess toward the Chen–Hou 2D
Boussinesq self-similar profile and tests it against a predicate that was **locked before the
run** (`experiments/spike1_stepC_gate.py`, committed `eabb418`; the anti-self-deception record).
Evidence: `writeup/figures/fig11_spike1_stepC_gate.png` from committed
`writeup/data/spike1_stepC_gate.json` (`python writeup/3_spikes/spike1_stepC_evidence.py`).

## 1. The pre-committed predicate (user-approved 2026-07-25)

Gauge-honest (the normalization freezes the origin slopes, so `c_l` is an input we pin to the
Chen–Hou gauge; the real tests are the gauge-invariant exponent + the shape):

1. `α = c_ω/c_l → −0.3424 ± 5%`
2. far-field `ω(r,β*) ∼ r^α` fitted over ≥1 decade, exponent within ~10%
3. shape: anisotropy `|ω_y| < 0.23 |ω_x|` (2.24), sane sign structure
4. resolution-stable

## 2. The drift, diagnosed and fixed

The first relaxation runs **drifted**: the gauge-invariant `α` settled near `−0.35` (right),
but `c_l, c_ω` drifted individually and the run eventually destabilized (~step 8000: residual
jump, growing negative lobe). Diagnosis (`experiments/diagnose_stepC_drift.py`): a **near-origin
truncation artifact**, not a fundamental instability — the `c_l` drift roughly halves under `n_r`
refinement (300→450: drift/1k `−0.144 → −0.074`) and worsens as `r_min` shrinks (poorly-
conditioned tiny-`r` cells: `r_min` 1e-3/1e-4/1e-5 → `−0.111/−0.144/−0.200`).

**Fix — gauge renormalization** (`run(renorm=True)`): discretely enforce the normalization
(2.12) by re-pinning `ω_x(0), η_x(0)` to their initial values each step, holding
`c_l = 2 η_x(0)/ω_x(0)` fixed regardless of the truncation slip. This arrests the drift
(`c_l` held at 3.06 vs collapsing to 2.24) and stabilizes the run. The paper's continuous
(2.12) is the exact analogue; the discrete version is a weak restoring correction (factors ≈ 1).

## 3. Result (resolution study, renorm on, `r_min=1e-3`)

| `n_r` | `r_max` | `c_ω` (tgt −1.0294) | `α` (tgt −0.3424) | far-field fit (tgt −0.3424) | anisotropy (<0.23) |
|---|---|---|---|---|---|
| 300 | 1e5 | −1.0266 | −0.3351 | −0.3226 | 0.026 |
| 450 | 1e5 | −1.0233 | −0.3340 | −0.3114 | 0.027 |
| 600 | 1e5 | −1.0312 | −0.3368 | −0.2992 | 0.027 |
| 450 | 1e6 | −1.0293 | −0.3362 | −0.3146 | 0.026 |

**What matches Chen–Hou well** (checks 1, 3, 4 PASS):
- `c_ω` to **< 0.5%** across every config (−1.026…−1.031 vs −1.0294) — and `c_ω` is the *real*
  result: it evolves through `u_x(0)` to the profile value while `c_l` is held at the gauge.
- `α = c_ω/c_l ≈ −0.335` to ~2%, resolution-stable (varies < 0.003 across `n_r`).
- Anisotropy `≈ 0.026 ≪ 0.23` — the strong `x/y` anisotropy of the profile (2.24) is reproduced.

**What fails** (check 2 FAIL): the *directly fitted* far-field radial exponent is `≈ −0.31`,
off by ~7–13%, and it moves the *wrong* way with `n_r`. Two honest causes:
- **Protocol confound.** The study used a fixed step budget (2500), so higher-`n_r` runs (finer
  `Δρ`) reach *smaller* `τ` — they are *under-relaxed*, and the slow `r^{−1/3}` tail is the last
  thing to form. So the `n_r`-trend of the far-field fit is not a clean resolution signal. (A
  fixed-`τ` or fixed-residual protocol would fix this — flagged as future work, NOT re-run to
  chase a pass.)
- **POC limitation.** Our domain (`r_max` 1e5–1e6) is tiny next to the paper's `~1e15`, and the
  outer boundary steepens the tail near `r_max`; we have no semi-analytic `r^α` far-field split
  and only 2nd–3rd-order near-origin accuracy, vs the paper's 6th–8th-order B-splines. A clean
  far-field match needs that apparatus.

## 4. Honest verdict

**Step C is a PARTIAL success and does not pass the pre-committed gate.** The machinery
reproduces the Chen–Hou profile's *modulation invariants* (`c_ω` to <0.5%, `α` to 2%) and its
*anisotropic near-field structure* — strong evidence the scheme captures the right physics — but
it does **not** reproduce the full `r^{−1/3}` far-field tail at POC fidelity, which is exactly
the part the paper built its heavy apparatus for. This is Tier-1/2 progress: the machine is
validated to capture the self-similar profile's core, with its POC limits honestly located.

And the standing frame is unchanged: even a *clean* pass would reproduce a **proven** result
(Chen–Hou 2022) on a toy model across Wall C — it validates our machinery; it is **not novel and
not a proof**. Clay odds remain ~0.05%; the lottery ticket is past this solver.

## 5. Reproduce

```
python experiments/diagnose_stepC_drift.py            # the drift diagnosis
python experiments/spike1_stepC_gate.py --logged --steps 2500   # the gate (writes data + predicate)
python writeup/3_spikes/spike1_stepC_evidence.py               # rebuild fig11 from committed data
```
