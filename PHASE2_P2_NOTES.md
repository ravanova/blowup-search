# Phase-2 P2 working notes — the lottery-ticket leg (1D Hou–Luo singular profiles)

Status as of 2026-07-25. Newest context on top. This is the working doc; the banked
record is writeup/TECHNICAL_P2_HL_ANCHOR.md + BLOG_P2_HL_ANCHOR.md + fig12 (rebuilds from
committed writeup/data/p2_hl_anchor.json via `python writeup/p2_hl_anchor_evidence.py`).

## TOP STATUS — anchor DONE (§2); HH23 scout DONE (§5, NO-GO on the literal link); dynamic-
## relaxation leg DONE (§6, Conjecture-2.4 LOCAL attractor confirmed at POC, global basin not —
## PARTIAL/Tier-2, not novel, not a proof). NEXT = reassess: heavier numerics for the two-scale
## probe, or bank + pivot. (Older context below is preserved; read §5 then §6 first.)

After Spike 1 (the 2D Boussinesq dynamic-rescaling machine, which reproduced the *proven*
Chen–Hou regular profile), we scoped P2 = the actual novelty frontier. Decision (with the
user, from evidence): **attack the 1D Hou–Luo (HL) model, not 2D Boussinesq.**

Target paper: **Chen–Huang–Li, arXiv:2604.01868** (Papers/, gitignored — `Read` page by page).
Their novel result: *degenerate* initial data (ω⁰ₓ(0)=θ⁰ₓₓ(0)=0) develops **singular**
self-similar profiles via a **two-stage** L^∞-then-L^p blowup. This is a **not-rigorously-proven
frontier** — only *weak existence* of the explicit profile is proven (their Thm 2.3); the
*asymptotic stability* (that generic degenerate data converges to it) is **numerical only**.
That gap is where a lottery ticket could live.

### Why 1D-HL over 2D (the scout, §1)
- The novel phenomenon lives first in the 1D HL model (ωₜ+uωₓ=θₓ, θₜ+uθₓ=0, uₓ=H(ω)),
  which "models the boundary behaviour of the Hou–Luo / 3D-axisymmetric-Euler scenario."
- 1D reuses machinery we already have (solver/line_hilbert.py 6/6, gclm rescaling 5/5).
- 2D would compound the exact far-field-tail problem Spike-1 Step C already hit, at higher cost.
- **Feasibility probe (decisive):** our line-Hilbert operator **survives** the singular profile.
  Against the exact H I derived (below), the (X−1)^{−1/2} *core* is representable to a few %
  and improving; the only real error is the slow X^{−1/2} *tail*, which is **truncation-limited**
  (halves with domain reach M, immune to node clustering) — the known semi-analytic-outer-patch
  gap, NOT a failure to resolve the singularity. (fig12 panel C.)

## §2 — The validation anchor (DONE, 2026-07-25). VALIDATION, not novelty.

Rescaled HL dynamics (their (2.4)), fields Ω (vorticity), Θ (buoyancy), velocity U:
```
Ω_τ + (U + c_l X) Ω_X = c_ω Ω + Θ_X
Θ_τ + (U + c_l X) Θ_X = (c_l + 2 c_ω) Θ
U_X = H(Ω),  U(0)=0.
```
Two genuinely new pieces vs the CLM solver: the velocity U is the *integral* of H(Ω) pinned at
U(0)=0 (CLM's transport speed was purely algebraic), and the second buoyancy field Θ.

**Explicit exact anchor — their Theorem 2.3:**
```
Ω̄(X) = (X−1)^{−1/2} 1_{X>1},   Θ̄ = (π/2) 1_{X>1},   c̄_l = 2,  c̄_ω = −1.
```
**Derived here (a small self-contained result):** from the classical Hilbert pair
H(x₊^{−1/2}) = −(−x)₊^{−1/2} (Fourier multiplier −i·sgn(ξ)),
```
H(Ω̄)(X) = −(1−X)^{−1/2} 1_{X<1},    U̅(X) = 2√(1−X) − 2  (X<1),  −2  (X≥1),
```
which satisfies (U̅+2X)Ω̄_X + Ω̄ = 0 on X>1 (the strong steady form; Remark 5.4) and U̅(0)=0,
U̅(1⁻)=−2. A free consistency check: c̄_l+2c̄_ω = 0 exactly ⇒ the Θ steady equation is trivial.

**Built:** solver/hl_rescaled.py (velocity operator, rescaled RHS, steady residual, both grids).
**Tests:** test_hl_rescaled.py **5/5** —
- velocity operator vs analytic arctan(2X): 1.1e−5; full pipeline through the dense H: 1.8e−3
- velocity on the singular anchor → U̅, converges under δ-refinement (½-order — the √-singularity)
- steady residual of the explicit Thm 2.3 profile → 6.2e−3, converging
- c̄_l+2c̄_ω=0 consistency: exactly 0.

## §3 — Performance (line_hilbert.py, the shared operator)
The build bottleneck was in the shared operator, not the new P2 code:
- batched Thomas solve for the slope operator: `_slope_matrix` 6.15s → 0.29s (21×);
- Horner + shared + shortened `L(s)` series (dominant cost): n=4001 matrix build 65s → 19.7s (3.3×);
- lazy Hilbert matrix in RescaledHL (anchors that use exact H never build it).
Net: HL suite >120s → 3.9s. Accuracy **identical** (line_hilbert 6/6, gclm 5/5, hl 5/5 all green).

## §4 — THE OPEN WORK (the actual lottery ticket; NOT yet started)
The anchor above reproduces a *proven* result — it validates the singular machinery, nothing more
(Tier-1/2, not novel, not a proof; same category as Spike 1). Novelty begins with the **dynamic
relaxation + degenerate-case normalization**:
- Build the SSPRK3 time stepper for (2.4) with a normalization that works when the origin slopes
  vanish (CHH22's origin-slope gauge is degenerate for degenerate data — need a higher-order or
  norm-based gauge). LOCK a predicate BEFORE the logged run.
- **Novelty target:** does *generic smooth degenerate data* converge to the singular profile (the
  asymptotic stability CHL only asserted)? A resolution-confirmed yes/no is a Tier-2-style
  contribution. Beyond that: unexplored degeneracy orders / profile families; the flagged-open
  link to Hou–Huang two-scale 3D-axisymmetric-Euler (HH23).
- The slow X^{−1/2} tail will need a fixed-τ protocol + semi-analytic r^α outer patch (same fix
  flagged for Spike-1 Step-C polish). Bounded, known.

Honest odds unchanged: overall Clay ~0.05%. The realistic prize is novel toy-model singularity
research + a shareable, data-backed writeup. This leg is the first genuine swing at it.

## §5 — HH23 SCOUT (2026-07-25). Go/no-go on the flagged-open Hou–Huang link. Verdict: NO-GO on
the literal link; the scout surfaced a SHARPER, 1D-tractable adjacent question. No logged run.

Grounded in CHL (2604.01868) itself (pdftotext → grep, not vibes). Key passages: intro p.6
(the "intriguing question"); §2.3 (two-scale mechanism); §3 conclusion (their two-STAGE finding).

**What [HH23] actually is** — the CHL bibliography (not the paper; HH23 is not in Papers/):
T. Y. Hou & D. Huang, *Potential singularity formation of incompressible axisymmetric Euler
equations with degenerate viscosity coefficients*, MMS 21(1):218–268, 2023. A **numerical
two-SCALE self-similar blowup of 3D axisymmetric Euler on ℝ³, with NO boundary**, smooth data.

**What CHL actually claim about the link** (verbatim, intro): their singular profiles "share
qualitative similarities with those observed in ... Hou–Huang [HH23], which suggested a potential
two-scale self-similar blowup of 3D axisymmetric Euler ... in the absence of a boundary. Whether
these phenomena are fundamentally linked remains an intriguing question." An *aspirational intro
remark about profile appearance* — not a worked reduction.

**The decisive structural mismatch (why NO-GO):**
1. HH23 = two-**SCALE** (spatial multi-scale: a bulk traveling at r(t) in a coarse scale (T−t)^γ
   + a fine inner scale (T−t)^γ̂; connected to traveling waves; the CHL eq-(2.8)/[HQW25] structure).
2. CHL's HL result = two-**STAGE** (temporal: local L^∞ blowup at T̃ off-origin, then weak
   continuation to an L^p blowup at the origin at T). And CHL **explicitly report NO numerical
   evidence of a two-scale mechanism in HL** (§3: "we find no numerical evidence supporting a
   two-scale blowup mechanism for the HL model analogous to that described in [HQW25]"). The very
   feature that DEFINES HH23 (two-scale) is the one CHL looked for in HL and did NOT find.
3. Geometry: 1D HL models the *boundary* behaviour of the Hou–Luo scenario. HH23 is *boundary-free*
   ℝ³. The 1D HL model is not a reduction of the no-boundary 3D scenario.
⇒ A 1D-HL machine cannot address "are they fundamentally linked" without overclaiming — that is a
3D structural question, wrong geometry, and CHL's own data points AWAY from a shared mechanism.
Chasing it as a "link to 3D Euler" would be exactly the self-deception WIN_CONDITION guards against.

**The scout's payoff — the genuinely-open, 1D-tractable question hiding behind the remark:**
the **two-scale-vs-two-stage question inside the 1D CLM/HL family.** The two-scale mechanism (the
thing that *resembles* HH23) is PROVEN for the CLM model (Huang–Qin–Wang [HQW25], SIAM J Math Anal
57(4):4068–4096, 2025) and was **conjectured by Liu [Liu17] for HL** — but CHL found HL is
two-STAGE, not two-scale. That is a LIVE discrepancy (Liu's conjecture vs CHL's numerics), entirely
in 1D, and CHL themselves pose it: "If singular profiles are observed, is their formation related
to a two-scale blowup mechanism?" Our exact machinery (line_hilbert + rescaled HL + the
dynamic-relaxation stepper we're about to build) is precisely the tool to settle it — track the
peak LOCATION and test for a moving bulk at a coarse scale (two-scale signature) vs a τ→∞
convergence to the fixed singular profile at X=1 (two-stage signature), across degeneracy classes.

**Honesty ceiling on that too:** confirming CHL's "no two-scale in HL" = Tier-2 independent
confirmation. Finding two-scale in some HL degeneracy class CHL missed (vindicating Liu) would be a
genuinely new *1D* result — the better lottery ticket — but odds are it's absent (CHL looked), and
even a positive is a 1D analogue, still NOT a proven link to 3D Euler.

## §6 — DYNAMIC-RELAXATION LEG DONE (2026-07-25). Conjecture 2.4 at POC: LOCAL attractor
confirmed, global basin not. PARTIAL / Tier-2-style. Full record: writeup/TECHNICAL_P2_CONJ24.md
+ BLOG_P2_CONJ24.md; fig13 from committed writeup/data/p2_conj24_relax.json
(`python writeup/p2_conj24_evidence.py`). Logged harness (predicate locked in git first):
experiments/p2_conj24_relax.py --logged. Machinery: solver/hl_rescaled.py::RescaledHLDynamic,
test_hl_rescaled.py now 7/7.

**The novel piece BUILT + VALIDATED: CHL's degenerate normalization gauge (their (3.2)).** The
CHH22 gauge pins the origin slope Omega_x(0) = 0 for degenerate data (dead). CHL read the NONLOCAL
U_X(0)=H(Omega)(0) (alive) for amplitude + c_l=-U(1) for location. Known-answer test on the exact
Thm-2.3 anchor → (c_l,c_omega)=(1.949,-0.969)≈(2,-1); degeneracy sidestep: |Omega_x(0)|~1e-4 vs
|H(Omega)(0)|~1.24. Two new unit tests.

**The wall (diagnosed):** non-dissipative SSPRK3+upwind+spline is UNSTABLE at the singular profile
— starting AT the regularized anchor, residual grows 25→1e9 by τ~1.4 (spline slopes ring at the
X=1 discontinuity; the stiff Theta_X delta-source amplifies). Fix = subgrid dissipation nu*d²/ds²
(a POC crutch, O(nu) profile bias, NOT CHL's WENO/adaptive mesh). Added as solver `nu` param.

**Logged result (n=801, nu=0.02, 2500 steps; 9/9 pre-committed clauses PASS, PARTIAL by design):**
- anchor hold → (c_l,c_omega)=(1.939,-0.927), res 180→3.4 plateau (stable HOLD, NOT →0), shape 4.9%.
- 2 perturbations → same fixed point (within 0.06), res drops >5× → LOCAL asymptotic stability.
- nu=0.04 → (1.936,-0.925), unchanged → fixed point robust to the stabilizer (not a nu artifact).
- generic far degenerate IC → (0.680,-0.487), a DIFFERENT self-similar state (low res, wrong
  constants, 29% shape) → GLOBAL basin beyond a fixed-grid POC (the honest predicted negative).

**Honest status:** validated the degenerate gauge + the LOCAL stability of CHL's singular fixed
point (independently reproduces the local content of a numerical-only claim). NOT achieved:
residual→0 (POC dissipation floor) and the global basin. Both need WENO/adaptive mesh +
vanishing-viscosity + semi-analytic X^{-1/2} outer patch (same tail fix as Spike-1 Step C).
Tier-2-style, NOT novel, NOT a proof. 1D HL is a toy (boundary behaviour of Hou–Luo). Clay ~0.05%.

**Next (reassess with user):** the genuinely-new leg is the §5 two-scale-vs-two-stage question
(Liu conjecture vs CHL finding), which needs exactly the global-basin numerics above. Options:
invest in the heavier numerics (WENO/adaptive/tail patch) to reach generic-data convergence + the
two-scale probe, OR bank P2 as a shareable data-backed Tier-2 writeup and pivot.
