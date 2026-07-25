# Phase-2 P2 — the dynamic-relaxation leg: Conjecture 2.4 (Chen–Huang–Li) at POC fidelity

*1D Hou–Luo singular-profile machinery. This is the first genuine swing of the "lottery-ticket"
leg — the dynamic relaxation. It reproduces (partially, at proof-of-concept fidelity) a
**numerical-only** claim of Chen–Huang–Li. That makes it Tier-2-style: an independent
confirmation, **not novel, not a proof.** Honest framing preserved throughout.*

Data: `writeup/data/p2_conj24_relax.json` (committed; the figure rebuilds with no re-run).
Figure: `writeup/figures/fig13_p2_conj24_relax.png` via `python writeup/p2_conj24_evidence.py`.
Harness (predicate locked in git before the run): `experiments/p2_conj24_relax.py --logged`.
Machinery: `solver/hl_rescaled.py::RescaledHLDynamic`; validated by `test_hl_rescaled.py` (7/7).

## 1. What we set out to test

The P2 anchor (see `TECHNICAL_P2_HL_ANCHOR.md`) validated our *singular* machinery against the
**proven** (weak-existence) explicit steady state of Chen–Huang–Li (CHL, arXiv:2604.01868),
their Theorem 2.3:

```
Omega_bar(X) = (X-1)^{-1/2} 1_{X>1},   Theta_bar = (pi/2) 1_{X>1},   c_l = 2,  c_omega = -1.
```

CHL's **Conjecture 2.4** goes further and is *not* proven — it is asserted from their numerics:

> The singular steady state `(Omega_bar, Theta_bar, 2, -1)` is **asymptotically stable**: under
> suitable normalization, generic smooth *degenerate* data converges to it as `tau -> +infty`.

That asymptotic-stability gap is the frontier the continuation plan flagged. This leg asks: **what
can a fixed-grid proof-of-concept honestly say about it?** The answer is a clean *local* result and
an honest boundary — a Tier-2-style partial confirmation, exactly the ceiling we predicted out loud.

## 2. The genuinely new piece: the degenerate normalization gauge (validated first)

Dynamic rescaling is a **gauge**. The CHH22 non-degenerate scheme fixes the amplitude by pinning
the origin slope `Omega_x(0)` — which is **identically zero** for degenerate data
(`Omega_x(0)=0`), so that gauge is itself degenerate. CHL's fix (their (3.2)) is the crux, and it
is what we implemented:

```
c_l      = -U(1)                                  (pins the transport stagnation U+c_l X at X=1)
c_omega  = H( Theta_X - (U + c_l X) Omega_X )(0)   (holds U_X(0)=H(Omega)(0) fixed in tau)
```

The amplitude is read from the **nonlocal** velocity gradient `U_X(0) = H(Omega)(0)`, which is
generically nonzero even when the *local* slope vanishes. That single substitution — local slope
→ nonlocal Hilbert value — is what makes the degenerate case tractable.

**Known-answer validation** (`test_hl_rescaled.py`, two new tests, suite now 7/7). Feeding the
exact Thm-2.3 anchor through the *fully-consistent discrete pipeline*:

| quantity | target | measured (n=2001) |
|---|---|---|
| `c_l = -U(1)` | 2 | **1.949** |
| `c_omega = H(Theta_X-(U+c_l X)Omega_X)(0)` | -1 | **-0.969** |

(The clean identity behind the second row: at the anchor `Theta_X-(U+c_l X)Omega_X = Omega_bar`,
and `H(Omega_bar)(0) = -1` exactly — the delta at X=1 cancels analytically.) A second test confirms
the gauge sidesteps the degeneracy: on smooth degenerate data `|Omega_x(0)| ~ 1e-4` (the old gauge
is dead) while `|H(Omega)(0)| ~ 1.24` (the CHL gauge is alive).

## 3. The dynamic stepper, and the numerical wall

`RescaledHLDynamic` time-steps system (2.4) with SSPRK3 in rescaled time `tau`; advection
`(U+c_l X) d/dX` is upwinded in the uniform sinh coordinate `s` (`X = 1 + delta*sinh s`) so the
dilation CFL stays `~ds` independent of the reach `M`.

**The wall (diagnosed, not hand-waved).** With no dissipation the scheme is **unstable at the
singular profile**: starting *exactly at* the regularized anchor the residual grows from step 0
(`25 -> 3e3 -> 1e6 -> 1e9`) and blows up by `tau ~ 1.4`. Cause: the non-dissipative spline slopes
**ring at the X=1 discontinuity** of the profile, and the stiff `Theta_X` delta-source amplifies
the ringing. This is the same class of difficulty that drove CHL to adaptive-mesh + WENO.

**The fix (POC-level).** A subgrid dissipation `nu * d^2/ds^2` holds it. This is a
proof-of-concept stabilizer with an honest `O(nu)` profile bias — *not* the WENO/adaptive-mesh
treatment CHL use — but it is enough to ask the stability question.

## 4. The logged result — a pre-committed, gauge-invariant predicate

The predicate was **locked in git before the run** (`experiments/p2_conj24_relax.py`, commit
preceding the logged run), tests only gauge-invariant quantities, and was declared **PARTIAL by
construction**. All numbers below are from the committed JSON (n=801, delta=0.02, M=150,
dt_frac=0.15, 2500 steps).

| run | c_l (→2) | c_omega (→−1) | residual `res0 → floor` | shape rel-L2 | blew up? |
|---|---|---|---|---|---|
| anchor hold (ν=0.02) | **1.939** | **−0.927** | 1.8e2 → 3.4 | 0.049 | no |
| perturb + (ν=0.02) | 1.935 | −0.918 | 1.7e2 → 3.7 | 0.048 | no |
| perturb − (ν=0.02) | 1.940 | −0.928 | 1.7e2 → 3.4 | 0.046 | no |
| hold (ν=0.04) | 1.936 | −0.925 | 3.5e2 → 2.4 | 0.048 | no |
| generic degenerate IC | **0.680** | **−0.487** | 2.2 → 0.32 | 0.293 | no |

**All 9 locked clauses hold (9/9):**
- **P1 (fixed-point consistency).** Initialized at the regularized anchor, the gauge constants
  settle at `(1.94, -0.93)` — within `~3%`/`~7%` of `(2, -1)` — and the residual **drops ~50×
  and plateaus** (a stable *hold* at a nonzero POC floor; explicitly **not** convergence-to-zero).
- **P2 (local stability).** Two distinct smooth perturbations of the anchor **both relax to the
  same fixed point** (`c_l, c_omega` within `0.06` of the unperturbed endpoint), residual dropping
  `>5×`. This is the local-attractor content of Conjecture 2.4.
- **P3 (robust to the stabilizer).** At `nu=0.04` the held constants are unchanged `(1.94, -0.93)`
  — the fixed point is not an artifact of one `nu`. The residual floor scales with `nu`
  (`3.4` at 0.02, `2.4` at 0.04), consistent with a controllable dissipation floor.
- **P4 (honest negative — predicted).** A generic far degenerate IC does **not** reach the anchor:
  it settles instead at `(0.68, -0.49)`, a *different* self-similar state (low residual, wrong
  constants, 29% shape distance). The **global basin** — the strong form of Conjecture 2.4 — is
  beyond a fixed-grid POC.

See `writeup/figures/fig13_p2_conj24_relax.png`: (A) all trajectories → (2,−1); (B) hold/perturb
residuals drop-and-plateau while the generic IC never approaches; (C) hold+perturbations cluster on
the target while the generic endpoint sits far off.

## 5. Honest status

- **What is validated:** CHL's degenerate normalization gauge (known-answer), and the **local
  asymptotic stability** of their singular fixed point — perturbations relax back to `(2,-1)` with
  `~5%` shape fidelity, robust to the numerical stabilizer. This independently reproduces the local
  content of a claim CHL only asserted numerically.
- **What is not:** (i) convergence of the residual to zero — it plateaus at a POC dissipation floor;
  (ii) the **global basin** (generic degenerate data → the singular profile), which this fixed-grid
  POC does not reach. Both need the heavier numerics CHL used: WENO / adaptive mesh, a
  vanishing-viscosity limit, and a semi-analytic `X^{-1/2}` outer-tail patch (the same tail fix
  flagged for Spike-1 Step C).
- **Tier:** Tier-2-style independent confirmation (partial, local). **Not novel, not a proof.** The
  1D HL model is itself a toy (it models the *boundary* behaviour of the Hou–Luo / 3D-axisymmetric-
  Euler scenario). Overall Clay odds unchanged (~0.05%).

## 6. Where the genuinely-new math would begin (for the reassessment)

This run reproduces CHL. The two-scale-vs-two-stage question surfaced by the HH23 scout (see
`PHASE2_P2_NOTES.md` §5) is the nearest *open, 1D-tractable* target: HQW25 proved a **two-scale**
blowup for the CLM model and Liu conjectured it for HL, but CHL found HL is two-**stage**. Settling
that discrepancy — track the peak *location* for a moving bulk on a coarse scale — would be a
genuinely new 1D result rather than a reproduction. Reaching it first needs the global-basin
numerics above (so that generic data, not a near-anchor start, drives the dynamics).
