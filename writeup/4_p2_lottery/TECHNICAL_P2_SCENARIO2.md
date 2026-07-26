# Phase-2 P2 (B1) — CHL Scenario 2: the modified rescaling (4.1)/(4.2), reproduced

*1D Hou–Luo singular-profile machinery. This leg implements Chen–Huang–Li's **modified** dynamic
rescaling (their (4.1)/(4.2)) and reproduces their **Scenario 2**: the regular, strictly-positive
self-similar profile and its contraction exponent. It is a Tier-2 consolidation — an independent
reproduction of a **published (numerical) result**, **not novel, not a proof.** Its real value is
the **validated origin-pinned gauge** that the next leg (the gCLM two-scale↔two-stage probe) needs.*

Data: `writeup/data/p2_scenario2_relax.json` (committed; the figure rebuilds with no re-run).
Figure: `writeup/figures/fig15_p2_scenario2.png` via `python writeup/4_p2_lottery/p2_scenario2_evidence.py`.
Harness (predicate locked in git before the run, commit `b5294ff`): `experiments/p2_scenario2_relax.py --logged`.
Machinery: `solver/hl_rescaled.py::RescaledHLScenario2`; validated by `test_hl_rescaled.py` (9/9).

## 1. Why this brick, and the honest ceiling up front

CHL (arXiv:2604.01868) describe two objects in the 1D Hou–Luo (HL) model:

- **Scenario 1 / Stage 2** — the *singular* self-similar profile `Ω̄=(X−1)^{−1/2}1_{X>1}` with
  `(c_l,c_ω)=(2,−1)`. Our anchor (`TECHNICAL_P2_HL_ANCHOR.md`) reproduced this *proven* object; the
  dynamic-relaxation leg (`TECHNICAL_P2_CONJ24.md`) reproduced its *local* asymptotic stability
  (Conjecture 2.4) at POC fidelity.
- **Scenario 2 / Stage 1** — a *regular, strictly-positive, non-symmetric* self-similar profile with
  contraction exponent `c_l/c_ω = −2.5114` (their Fig 4.2). CHL reach it with a **modified** dynamic
  rescaling that adds a spatial-shift degree of freedom, normalized at a moving origin.

The reframe scout (`PHASE2_P2_NOTES.md` §7) showed our earlier "generic → a different state" run was
already landing near this regular profile — but the **degenerate gauge could not hold it**, because
that gauge pins the transport stagnation at `X=1` while the Scenario-2 profile is peaked *away* from
`X=1`. B1 fixes exactly that by implementing CHL's origin-pinned gauge.

**The ceiling, said out loud:** reproducing Scenario 2 is Tier-2 — it reproduces a CHL object, it is
not new mathematics and not a proof. We pursued it only because the machinery it builds — the
**origin-pinned 3-constant gauge** — is the piece a genuinely-new gCLM two-scale↔two-stage sweep
requires to hold regular profiles across the parameter `a`. B1 is "the gCLM-ready gauge, validated
against a known answer," not a trophy.

## 2. The formulation (CHL (4.1)/(4.2))

CHL introduce a time-dependent spatial shift `r(τ)` (translation invariance of the HL equations) so
the origin can act as a movable "source of stability" for the non-symmetric profile. Writing
`V := Θ_X` (better far-field decay), their reformulated system (4.1) is

```
Ω_τ + (U + c_l X + c_r) Ω_X = c_ω Ω + V
V_τ + (U + c_l X + c_r) V_X = (2 c_ω − U_X) V
U_X = H(Ω),   U(0) = 0
```

with the extra constant `c_r` the shift rate. The three constants `(c_l, c_ω, c_r)` are fixed by
**normalization (4.2)**: pin the origin values in rescaled time,

```
∂_τ Ω(0) = ∂_τ Ω_X(0) = ∂_τ V(0) = 0,
```

which — with `U(0)=0` — reduces to a 3×3 linear system solved each step (derived independently here
and checked against the paper):

```
Ω_X(0)  c_r −  Ω(0) c_ω                  = V(0)
V_X(0)  c_r − 2V(0) c_ω                  = −U_X(0) V(0)
Ω_XX(0) c_r −  Ω_X(0) c_ω + Ω_X(0) c_l   = V_X(0) − U_X(0) Ω_X(0)
```

Note `c_l` appears only in the third equation, and `Ω_X(0)` is its coefficient — so the gauge
requires `Ω_X(0) ≠ 0`. **Scenario 2 lives at a non-symmetry origin**: unlike the degenerate case
(`Ω_x(0)=0`), the initial data must be origin-*non*degenerate, else the system is singular.

## 3. Implementation (the transferable deliverable)

`solver/hl_rescaled.py::RescaledHLScenario2`:

- **Grid** — origin-clustered symmetric sinh grid `X = c·sinh(ρ)` with **X=0 a node** (n forced
  odd). The gauge reads `Ω(0), Ω_X(0), Ω_XX(0), V(0), V_X(0), U_X(0)=H(Ω)(0)` **at a node** — no
  interpolation of second derivatives off a far cluster (the accuracy this brick buys over the §6
  `X=1`-clustered grid).
- **Gauge** — a hand-rolled 3×3 Gaussian-elimination solve (`_solve_3x3`, no scipy) of (4.2) each
  step, with partial pivoting and a singular-system guard.
- **Time stepping** — SSPRK3 in rescaled time, transport upwinded in the uniform `ρ` coordinate so
  the dilation speed stays bounded independent of the domain reach.
- **`scenario2_ic`** — generic non-symmetric positive, origin-nondegenerate data (`Ω(0)>0`,
  `Ω_X(0)≠0`); the amplitude is *not* separately renormalized (the (4.2) gauge holds `Ω(0),Ω_X(0),
  V(0)` at their initial values).

**Known-answer unit test** (`test_hl_rescaled.py`, now 9/9): the (4.2) solve, by construction, must
null `∂_τ{Ω(0), Ω_X(0), V(0)}`. On generic non-symmetric data the three continuous origin
time-derivatives vanish to **4.4×10⁻¹⁶** — exact linear algebra, the defining property of the gauge.
A separate test confirms `_solve_3x3` matches numpy to 7×10⁻¹⁴ and raises on singular systems.

## 4. The logged result (5/5, PARTIAL by construction)

Config: `n=801`, `nu=0.02`, two distinct ICs (`x0=0.30`; `x0=0.45`, different width), 14000 steps
with **adaptive dt** (recompute the CFL as the initial `c_l≈13` transient decays), reaching `τ≈42`.
Predicate locked in git before the run.

| clause | content | result |
|---|---|---|
| **S1** ratio known-answer | generic IC → `\|c_l/c_ω − (−2.5114)\| ≤ 0.05` | **PASS** — `−2.5334` (~0.9%) |
| **S2** attractor | 2nd IC → same ratio within 0.05 | **PASS** — `−2.5352` |
| **S3** regular positive | `minΩ,minV > 0`; smooth (`max\|Ω_X\|/peak ≤ 5`); peaked at `X*>0.15` | **PASS** — `minΩ=5.6e−2`, smooth `0.73`, `X*=0.82` |
| **S4** residual bounded+falling | res drops ≥50× from step 0, no blowup | **PASS** — `15 → 2.2e−2` (≈680×) |
| **S5** honest ceiling (predicted) | res floors `>1e−4` **and** `c_l>1.2` (off CHL raw) | **PASS** — floors `2.2e−2`; triple `(1.59,−0.63,0.21)` |

The **amplitude-invariant contraction exponent** `γ = c_l/c_ω` — the physical Scenario-2 prediction
— is reproduced to ~1% as a genuine **IC-independent attractor** to a regular strictly-positive
profile (fig15 panels A, C). Both ICs spiral onto the same value.

## 5. What is honest, and what is not

- **Gauge-invariant, reproduced:** the ratio `γ ≈ −2.53` (CHL `−2.5114`) and the qualitative
  profile — strictly positive, smooth, non-symmetric, peaked at `X*≈0.82`. This is `≈ 1061×` smoother
  (by `max|Ω_X|/peak`) than the singular Stage-2 anchor: a genuinely different, regular object.
- **Normalization-dependent, NOT matched:** the *absolute* `(c_l,c_ω,c_r)` drift to
  `(1.59,−0.63,0.21)`, off CHL's raw `(1.0636,−0.4235,0.0765)`. The (4.2) gauge holds the origin
  values at *our* IC's normalization; matching CHL's raw triple would require matching their IC
  normalization of `Ω(0),V(0)`. Only the ratio and shape are gauge-invariant, so those are what we
  claim.
- **Fixed-grid ceiling (S5):** the residual floors at `~2×10⁻²`; it does **not** reach CHL's `10⁻⁶`
  stopping criterion, which they meet with an adaptive mesh. This is the same fixed-grid boundary the
  Conjecture-2.4 leg hit — expected, and marked in the predicate rather than papered over.

## 6. Where this leaves the project

**Both CHL scenarios are now reproduced** — the singular Stage-2 anchor (§2/anchor + Conj-2.4 leg)
and the regular Scenario-2 exponent (this leg). That is a clean Tier-2 consolidation of CHL's 1D-HL
picture, backed by committed data and a rebuildable figure.

The lottery ticket does **not** live here. It lives in genuinely-new mathematics: most promisingly
the **gCLM-family two-scale↔two-stage transition** — where in the parameter `a` does CLM's *proven*
two-scale blowup (Huang–Qin–Wang, [HQW25]) give way to HL's two-stage blowup (CHL)? Nobody has
mapped it, we have `solver/gclm_rescaled.py`, and B1 just delivered the origin-pinned gauge that
sweep needs to hold the regular profiles it will encounter. That, or a rigor step on Conjecture 2.4,
is the next real swing. Overall Clay odds unchanged (~0.05%); this leg de-risks the swing, it is not
the swing.
