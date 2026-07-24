# Spike 0 (technical) — A dynamic-rescaling solver, validated against a closed-form answer

### The 1D on-ramp works: CLM self-similar rescaling on a stretched whole-line grid recovers the exact profile and rate

*Results companion to [TECHNICAL_PHASE2_RESCALING.md](TECHNICAL_PHASE2_RESCALING.md)
(the decision + derivation) and the working notes
[../PHASE2_SPIKE0_NOTES.md](../PHASE2_SPIKE0_NOTES.md). Code:
[`../solver/line_hilbert.py`](../solver/line_hilbert.py),
[`../solver/gclm_rescaled.py`](../solver/gclm_rescaled.py); tests
[`../test_line_hilbert.py`](../test_line_hilbert.py) (6/6),
[`../test_gclm_rescaled.py`](../test_gclm_rescaled.py) (5/5). Figure + committed
evidence: [`figures/fig8_spike0_rescaling.png`](figures/fig8_spike0_rescaling.png),
[`data/spike0_rescaling.json`](data/spike0_rescaling.json), rebuilt by
[`spike0_rescaling_evidence.py`](spike0_rescaling_evidence.py). References in [§7](#7-references).*

---

## 1. What Spike 0 had to prove, and against what

The Phase-1 wall was that on a **uniform grid** the singular structure forms below grid
scale, so no fitness read off the trusted window can isolate it
([NEGATIVE_RESULT_TWO_CURRENCIES.md](NEGATIVE_RESULT_TWO_CURRENCIES.md)). The agreed exit
was **dynamic self-similar rescaling** (P1): integrate the PDE in a frame that continuously
zooms into the singularity, so a finite-time blow-up becomes a **steady profile** held
resolved on a fixed grid. Spike 0's job was to de-risk that technique in 1D **against a
known answer** before the expensive 2D port — the project's standing discipline of
building on a substrate where the answer is already known.

The known answer is CLM (`a=0`). The physical model `ω_t = ω·H(ω)` from `ω_0 = -sin x`
blows up at `x=0`, `T*=2`, and its **local** self-similar structure has the exact,
closed-form profile

$$\bar\Omega_0(X) = \frac{-4X}{1+4X^2}, \qquad H(\bar\Omega_0)(X) = \frac{2}{1+4X^2},$$

with self-similar rate `c_ω = -1` (amplitude `~ (T-t)^{-1}`) and length rate `c_l = 1`
(length `~ (T-t)`). This profile, its Hilbert transform, and the rate are the pre-committed
targets. (Source for the exact pair and the scheme: Huang–Tong–Wang, arXiv:2603.25104.)

The pre-committed predicates were: **(P-steady)** `\bar\Omega_0` is a numerical steady state
of the rescaled equation; **(P-converge)** perturbed odd data relaxes onto `\bar\Omega_0`
with `c_ω → -1`; **(P-res)** both are resolution-stable. Note what is *deliberately not* a
predicate: the physical `T*=2` — see [§6](#6-honest-scope).

---

## 2. The scheme, reduced for CLM

The rescaled gCLM equation (convention `ω(x,t)=C_ω(τ)^{-1}Ω(X,τ)`, `X=C_l x`,
`dτ/dt=C_ω^{-1}`) is

$$\Omega_\tau + (c_l X + aU)\,\Omega_X = (c_\omega + U_X)\,\Omega, \qquad U_X = H\Omega,$$

with the **value-based normalization** (fix the origin slope `Ω_X(0)` and the amplitude
gauge): `c_l = c_ω + (1-a)U_X(0)`, and for `a=0`, `c_ω = 1 - H\Omega(0)`. Together these
give, for CLM, `c_l ≡ 1` (a constant) and `c_ω = 1 - H\Omega(0)`.

Two reductions make the 1D CLM case clean:

1. **Evolve `f = Ω/X` (k=1).** The non-degenerate CLM profile vanishes to order 1 at the
   origin (`\bar\Omega_0 ≈ -4X`), so dividing by `X` protects that vanishing exactly.
   Substituting `Ω = Xf`, `c_l=1`, `a=0`:
   $$f_\tau = -X f_X + \big(H\Omega - H\Omega(0)\big) f, \qquad \Omega = Xf.$$

2. **Work in the computational coordinate `ρ`, `X = c\,\sinh ρ`.** Then
   `X\,\partial_X = \tanh(ρ)\,\partial_ρ`, so the dilation becomes a **bounded** advection
   (speed `|\tanh ρ| ≤ 1`):
   $$\boxed{\; f_\tau = -\tanh(ρ)\,f_ρ + \big(H\Omega - H\Omega(0)\big) f \;}$$
   The CFL is `dτ ≲ Δρ`, **independent of the reach `M`**. This is the cure for the
   uniform-grid CFL death (where the dilation speed was `X` up to `M`, forcing
   `dτ < dX/M`; a fixed uniform mesh was ~20× over-budget and NaN'd even initialized *at*
   the exact profile — see the notes).

Three analytic facts pin the scheme (all verified by hand and in-test):

- `\bar\Omega_0` is an **exact steady state** (`-X f_X + (H\Omega-H\Omega(0))f = 0`
  identically for `f = -4/(1+4X^2)`).
- The origin value `f(0) = Ω_X(0) = -4` is **frozen exactly by the scheme**: at `ρ=0` both
  the advection speed `\tanh(0)` and the source `H\Omega(0)-H\Omega(0)` vanish, so
  `f_τ(0)=0`. This *is* the slope normalization, realized structurally rather than imposed.
- At the fixed point `H\Omega(0)=2 ⟹ c_ω = 1-2 = -1`, self-consistently.

---

## 3. The crux component: a line Hilbert transform on a non-uniform grid

The stretched grid forces the one component the periodic solver cannot supply. The profile
is a whole-line, `~1/X`-decaying function; its Hilbert transform must be computed on a
non-uniform mesh reaching large `|X|`, so the FFT multiplier `H(e^{ikx}) = -i\,\mathrm{sign}(k)`
does **not** apply (a periodic `H` converges to the *wrong* profile for such slow tails —
one of the banked reconnaissance findings).

We implement Appendix C.1 of arXiv:2603.25104: represent `f` in a `C^1_0` cubic-spline
Hermite basis `{P_i, Q_i}` (value-hat and slope-hat) whose Hilbert transforms are **bounded
and known in closed form**, `H(P_i)(x) = A(l) - A(r)`,
`H(Q_i)(x) = (x_{i-1}-x_i)B(l) - (x_{i+1}-x_i)B(r)`, with

$$A(s)=\frac{-5s^3-12s^2+12s+6(s^3-3s+2)\ln|1-s|}{6\pi s^3}, \quad
  B(s)=\frac{2s^3-9s^2+6s+6(s-1)^2\ln|1-s|}{6\pi s^3}.$$

**One implementation choice worth recording.** As `s→0` these numerators suffer
catastrophic cancellation (the `\ln` Taylor-cancels the polynomial to `O(s^4)`); the paper
handles it with a 23-term Mathematica minimax whose coefficient list `pdftotext` mangles.
Rather than transcribe it, we removed the cancellation **analytically** by substituting
`\ln|1-s| = L(s) - s - s^2/2 - s^3/3` with `L(s) = -\sum_{n\ge4} s^n/n`, which collapses the
numerators exactly to

$$A(s)=\frac{(s^3-3s+2)L(s)}{\pi s^3}-\frac{3s^2+2s^3}{6\pi}, \qquad
  B(s)=\frac{(s-1)^2 L(s)}{\pi s^3}+\frac{s-2s^2}{6\pi},$$

evaluated by a series for `L` when `|s|<0.5` (never near the `s=1` log singularity) and by
the direct form otherwise. This reproduces the paper's minimax to machine precision without
its coefficient table; it is verified two ways in the tests (branch continuity across
`|s|=0.5`, and agreement with the raw closed form at moderate `|s|`). Node slopes `f'_i` come
from a hand-rolled natural cubic spline (`f''=0` at both ends; no `scipy` in the environment),
and the whole linear map is assembled once into a fixed-grid `N×N` operator reused every RHS
evaluation.

**Validation (the crux, self-contained).** On a sinh-stretched grid the transform maps the
known pair `-4X/(1+4X^2) → 2/(1+4X^2)` to **relative error 1.6×10⁻⁴** (POC target: 1%), with
monotone whole-line convergence (max abs err **2.3×10⁻³ → 5.2×10⁻⁴ → 1.2×10⁻⁴** as core
resolution and reach `M` grow together). The dominant error is the `~1/M` tail truncation of
the profile's `1/X` decay — expected, and fine at POC level.

---

## 4. Time-stepping

The profile is smooth, so the paper's nonlinear WENO limiter is unnecessary at POC level:
we use a **3rd-order upwind-biased** finite difference for `f_ρ`, selected by `sign` of the
speed `\tanh ρ`. Because the flow is **outward at both domain ends** (characteristics leave),
the upwind stencil always reaches *inward* — no ghost points, only a single one-sided
fallback at each outermost node. Time advance is **SSPRK3** (Shu–Osher), `dτ = 0.4\,Δρ`.
Convergence is declared at `‖f_τ‖_∞ < 10^{-7}`.

---

## 5. Results

All five `test_gclm_rescaled.py` predicates pass; figure
[`fig8_spike0_rescaling.png`](figures/fig8_spike0_rescaling.png).

| Predicate | Result |
|---|---|
| **P-steady** — `\bar\Omega_0` a steady state | `‖f_τ‖=4.0×10⁻⁶`, `c_ω=-0.999`, `H\Omega(0)=1.999` |
| **origin slope frozen** | `f(0)=-4` held to machine precision (0 drift / 300 steps) |
| **P-converge** — perturbed IC → profile | Gaussian IC and a narrower Lorentzian IC (both slope `-4`) each relax to `\bar\Omega_0`: shape err **~2×10⁻⁶**, `c_ω → -0.999` in ~3050 steps |
| **P-res** — resolution stability | `c_ω = -0.9986` (n=901) → `-0.9995` (n=1801), trending to `-1`; shape err **4.0×10⁻⁶ → 7.7×10⁻⁷** under refinement |

**The headline finding (overturns a reconnaissance worry).** The recon had flagged that
one-scale rescaling *looked* unstable — the profile overshot and blew up in the rescaled
frame, seemingly the very scaling instability that motivated Chen–Hou's two-scale
formulation. Spike 0 shows that instability was an **artifact of the wrong (periodic)
Hilbert transform and integral-based modulation**, not fundamental. With the correct **line**
Hilbert transform and value-based normalization (`c_ω=1-H\Omega(0)`, `c_l≡1`), `\bar\Omega_0`
is a clean **attractor**: two differently-shaped perturbations both land on it. One-scale
suffices for CLM. Whether Boussinesq / De Gregorio re-introduces the two-scale need is a
Spike-1 question — a genuinely different blow-up mechanism — but the CLM case is now settled
and stable.

---

## 6. Honest scope

- **This reproduces a *proven, closed-form* result in a 1D toy model, across "Wall C".** It
  validates the machinery — the line Hilbert transform, the stretched-grid CFL cure, the
  normalization, the attractor behaviour. It is **not novel and not a proof.** The novelty
  frontier remains downstream (P2 construction of *unstable / singular* profiles; see the
  decision doc's own caveat).
- **The physical `T*=2` is deliberately not claimed from this run.** `T*` is a property of
  the *global periodic* solve (validated separately by `test_solver_clm.py`); a whole-line
  rescaling's initial amplitude is a **free gauge**, so `T* = ∫_0^∞ C_ω dτ` is not
  determined by it. The correct *local* analogue is the **rate** `c_ω → -1`
  (⟺ `ω ~ (T-t)^{-1}`), which the run recovers. Claiming `T*=2` here would be exactly the
  kind of over-reading the win-condition contract exists to prevent.
- **The log-kernel velocity `U`** (Appendix C.1 `C, D` integral elements) was correctly
  deferred — CLM (`a=0`) does not use it. It is the first thing the `a≠0` path or the 2D
  port will need.

---

## 7. References

- **[2603.25104]** D. Huang, J. Tong, X. Wang, *Self-similar finite-time blowups with
  singular profiles of the generalized Constantin–Lax–Majda model* — the exact CLM profile,
  the value-based normalization, and the Appendix-C.1 spline-analytic Hilbert transform +
  stretched grid this build follows.
- **[CH22b]** J. Chen, T. Hou, *Stable nearly self-similar blowup … II: Rigorous Numerics*,
  arXiv:2305.05660 — the two-scale dynamic rescaling and the scaling instability it addresses
  (for Boussinesq/De Gregorio, not CLM).
- Prior project records: [TECHNICAL_PHASE2_RESCALING.md](TECHNICAL_PHASE2_RESCALING.md)
  (decision + derivation), [NEGATIVE_RESULT_TWO_CURRENCIES.md](NEGATIVE_RESULT_TWO_CURRENCIES.md)
  (the uniform-grid wall), [../PHASE2_SPIKE0_NOTES.md](../PHASE2_SPIKE0_NOTES.md) (the full
  working record and the three banked false starts).
