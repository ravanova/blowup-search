# Phase-2 P2 working notes — the lottery-ticket leg (1D Hou–Luo singular profiles)

Status as of 2026-07-25. Newest context on top. This is the working doc; the banked
record is writeup/4_p2_lottery/TECHNICAL_P2_HL_ANCHOR.md + BLOG_P2_HL_ANCHOR.md + fig12 (rebuilds from
committed writeup/data/p2_hl_anchor.json via `python writeup/4_p2_lottery/p2_hl_anchor_evidence.py`).

## TOP STATUS — anchor DONE (§2); HH23 scout DONE (§5, NO-GO on the literal link); dynamic-
## relaxation leg DONE (§6, Conjecture-2.4 LOCAL attractor confirmed at POC, global basin not —
## PARTIAL/Tier-2). REGULAR-PROFILE REFRAME DONE (§7, 2026-07-25 scout): the §6 "generic → a
## DIFFERENT state" that we filed as an honest NEGATIVE is actually a REGULAR, strictly-positive
## profile = CHL's Stage-1 / Scenario-2 object (qualitatively) — NOT a POC artifact. The scout also
## SCOPED the fork: B1 (implement CHL's modified (4.1)/(4.2) to pin the regular profile; cheap,
## clean known-answer) is the recommended next brick; B2 (the Stage-1→Stage-2 transition) is NOT
## reachable on a fixed grid and mostly re-confirms CHL. **B1 DONE (§8, 2026-07-26): implemented
## CHL's (4.1)/(4.2), logged run 5/5 PARTIAL — the invariant exponent c_l/c_ω → −2.533 (CHL
## −2.5114) as a genuine IC-independent attractor to a regular positive profile; res floors ~2e-2,
## absolute triple normalization-dependent.** **GA FRAMEWORK DONE (§9, 2026-07-26): built + validated
## the GLOBAL-search infrastructure for the gCLM two-scale↔two-stage probe — the gCLM `a`-family
## rescaled residual (solver/gclm_family.py) + a generic GA engine (solver/ga_search.py); a=0
## one-scale known-answer gate PASSES (residual 2.2e-7; GA recovers the exact steady DILATION FAMILY,
## invariant A²/B=4); diagnostic LOCKED. Validated tooling, NOT a science result.** **TWO-SCALE
## a-SWEEP DONE + LOGGED (§9, 2026-07-26): derived the two-scale residual R₂=ΩHΩ−c_tw Ω_X−a U Ω_X
## (HQW25's moving-frame ansatz → leading order = a PURE TRAVELING WAVE; a=0 anchor Ω₂=−1/(1+X²)
## nulls to 1.5e-9, c_tw=1/2), locked predicate T1–T6, logged GA sweep 5/6 PARTIAL. Result: HQW25's
## exact a=0 two-scale traveling wave DEFORMS SMOOTHLY under advection — persists (relres<1e-2) to
## a_p≈0.40, floor rises to 0.18 at a=1 (De Gregorio), STAYS EVEN, no sharp collapse. T4 FAIL (honest):
## mid-range floor is partly GENOME-LIMITED (K=3 cuts a=0.5 floor 4×) → genome-relative upper bound,
## survival boundary not sharply pinned; BUT a=1 degradation robust to K=3. NOVEL toy-model result
## (Tier-1/2), NOT a proof, NOT a Clay solve.** **a_p(K) CONVERGENCE MAP DONE + LOGGED (§9-cont2,
## 2026-07-26): SHARPENS that T4 FAIL. Added even_lorentz_sq cross-check basis (+test, 12/12); a
## pre-run plateau scout caught that near-transition floors are SEARCH-limited at the old budget
## (a=0.6 K4 drops 45% at 2× budget) → fixed budget pop150/gen250/8seeds (converged) + in-JSON
## budget/K6 spot-checks. Locked T1–T7 (commit 44a507c), logged 7/7. RESULT: a_p(K)=0.40→0.50→0.50
## SATURATES; boundary a*≈0.5–0.55 is GA-converged (K4 1.7×-budget within 5%), genome-converged (K6
## does NOT beat K4), and BASIS-independent (mixed Lorentzian+squared within 3× of K3); far-end
## robust (K4 floor 1.28e-1 at a=1); resolution fine (min 35 pts). Honest nuance: a* is a SOFT
## crossing (bases straddle 1e-2 at 0.55), not a razor edge. The T4 "soft boundary" caveat is now a
## converged, genuine feature — NOT genome-limited. Still Tier-1/2, NOT a Clay solve.** Read
## §5→§6→§7→§8→§9→§9-cont2→§10→§11.
## Not novel-enough-to-be-a-proof; a genuine (now convergence-guarded) map.
## **ROUTE-D v1 DONE (§10, 2026-07-26): interval core + a=0 NK framing. Level-1 tooling + scoping, NOT a
## certificate.** Built solver/interval.py (hand-rolled rigorous interval arithmetic, +test 5/5, suite now
## 8 files green) + the deterministic a=0 probe (experiments/p2_route_d_probe.py → fig19). FOUR results:
## Q1 the interval enclosure carries the NK defect Y₀ (overhead ~10%); Q2 the a=0 zero set is a 2-param
## scaling valley → EXACTLY 2 gauge conditions isolate a nondegenerate zero (naive ‖DF⁻¹‖=∞); Q3 under
## X=tan(θ/2) the line Hilbert = circular conjugate (cos kθ↦sin kθ, ~1e-7), anchor = 2-term Fourier;
## Q4 ⇒ DF is TRIDIAGONAL + rank-1 (cos→sin), so finite-section Z₀+Z₁<1 is PLAUSIBLE. Framing =
## radii-polynomial NK; F quadratic ⇒ Z₂ constant. Open risks G(gauge/index)/R(θ=±π endpoint)/T(tail)/
## a≠0(no exact anchor off 0). BLOG/TECHNICAL_P2_ROUTED.md.
## **ROUTE-D v2 DONE (§11, 2026-07-28): the FLOAT DRESS REHEARSAL — the NK ball does NOT close, and CANNOT
## (0/13 on N=4..256; at any N, any gauge, any weight). Cause ISOLATED BY ABLATION: the transport term
## c(1+cosθ)∂_θ degenerates at θ=±π (X=∞) — replace (1+cosθ)→1 and ‖A_N‖ goes flat at 4.0 vs N^0.97.
## Sub-task G (gauge) EXONERATED, sub-task R (far field) promoted to blocker. Certification budget
## Y₀^max ≡ 0 at every N. CONSTRUCTIVE HALF: the inverse loses EXACTLY one power of decay (‖A e_m‖≈1.97m,
## predicted by the far-field ODE), so grading the codomain by one mode power gives ‖A‖=3.000 FLAT in N —
## the asymmetric space pair a working certificate must use. New solver/nk_fourier.py + test_nk_fourier.py
## (6/6; suite 9 files green); fig20; BLOG/TECHNICAL_P2_ROUTED_DRESS.md. Level-1 tooling + a structural
## negative, NOT a certificate.**

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
confirmed, global basin not. PARTIAL / Tier-2-style. Full record: writeup/4_p2_lottery/TECHNICAL_P2_CONJ24.md
+ BLOG_P2_CONJ24.md; fig13 from committed writeup/data/p2_conj24_relax.json
(`python writeup/4_p2_lottery/p2_conj24_evidence.py`). Logged harness (predicate locked in git first):
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

## §7 — REGULAR-PROFILE REFRAME + B1/B2 SCOUT (2026-07-25). EXPLORATORY (non-logged scout), but
it upgrades §6's most important caveat and scopes the fork. Evidence: writeup/
p2_regular_profile_evidence.py → fig14 from committed writeup/data/p2_regular_profile.json (two
fixed-point fields) + p2_regular_profile_traj.json (8000-step generic trajectory). No new solver
code; used RescaledHLDynamic as-is. NOT a logged gate run (no pre-committed predicate).

**The reframe (grounded in CHL §2.5 + §4).** CHL's rescaled HL system has TWO fixed points, not one:
- the SINGULAR anchor (§2 / §6): Ω̄=(X−1)^{−1/2}1_{X>1}, (c_l,c_ω)=(2,−1) — CHL's Stage-2 attractor;
- a REGULAR, strictly-positive profile (their Scenario 2, §4) — CHL's Stage-1 attractor: "a
  non-symmetric regular profile that remains strictly positive throughout," peaked off the singular pt.
The §6 logged run's "generic far degenerate IC → (0.680,−0.487), a DIFFERENT self-similar state
(honest predicted NEGATIVE)" is NOT a POC artifact: characterizing that final field shows it is
**smooth (max|Ω_X|/peak≈0.3 vs 1061 for the singular anchor), strictly positive (single-signed),
peaked at X≈0.35 (away from X=1), finite** — i.e. qualitatively CHL's Stage-1 regular profile. So our
machinery reaches BOTH CHL fixed points; the "negative" is really the first half of CHL's two-STAGE
structure, captured independently. (fig14 panels A vs B.)

**HONESTY GUARDS.** (1) Reached with the STANDARD (2.4)+degenerate-gauge, NOT CHL's modified
Scenario-2 formulation (2.9)/(4.1) — so this is a QUALITATIVE match (regular, +ve, peak off X=1),
NOT a proven identity to their profile. (2) The raw constants differ as expected under a different
normalization (ours c_l≈0.5, c_ω≈−0.45; theirs (c_l,c_ω,c_r)=(1.0636,−0.4235,0.0765), ratio
−2.5114). (3) It does NOT converge under our gauge — see the trajectory below. Not novel, not a proof.

**THE B1/B2 SCOUT (8000-step generic trajectory, fig14 panel C).** Under the degenerate gauge the
trajectory TRANSITS the CHL-S2 neighborhood (c_l≈1.06, c_ω≈−0.45 near step 1200 — the constants
nearly coincide) but CANNOT hold it, then WANDERS in the low-c_l regular regime (c_l oscillates
0.38–0.49, res floor ~0.12), and **NEVER approaches the singular anchor c_l=2.** Diagnosis: our gauge
pins c_l=−U(1) (stagnation at X=1) — a MISMATCH for a regular profile peaked at X≈0.35. CHL's (4.2)
normalization instead pins behavior at the ORIGIN (∂_τΩ(0)=∂_τΩ_X(0)=∂_τV(0)=0), exactly the right
stabilizer for the regular profile. Two decisive reads for the fork:
- **B1 (implement CHL's modified formulation) is the recommended next brick and is CHEAP + clean.**
  Formulation (4.1) = our (2.4) with ONE extra constant c_r in the transport speed (U+c_l X+c_r) +
  the V:=Θ_X change of variable; normalization (4.2) = a 3×3 linear solve for (c_l,c_ω,c_r) each step.
  KNOWN-ANSWER target: (c_l,c_ω,c_r,c_l/c_ω)=(1.0636,−0.4235,0.0765,−2.5114) (their Fig 4.2). We
  already fly within ~0.005 of c_l=1.0636 at the transit, so pinning there is very plausible. Outcome
  = "both CHL scenarios reproduced" + a shape overlay confirming the Stage-1 identification. Tier-2.
- **B2 (the Stage-1→Stage-2 transition / two-scale-vs-two-stage probe) is NOT reachable on this fixed
  grid** (the trajectory heads AWAY from c_l=2) and needs the adaptive-mesh rebuild; even a clean B2
  mostly RE-CONFIRMS CHL's already-published two-stage finding (low novel upside). Wrong brick now.

**Honest ceiling (unchanged).** B1 reproduces a CHL object → Tier-2, not the lottery ticket. The
genuinely-new math is elsewhere: (i) the gCLM-family two-scale-vs-two-stage transition — where in the
parameter 'a' does CLM's PROVEN two-scale (HQW25) give way to HL's two-stage (CHL)? Nobody has mapped
this, and we already have solver/gclm_rescaled.py; or (ii) a rigor step on Conjecture 2.4. Both are
harder + longer odds. B1 is the grounded consolidation brick that de-risks either.

## §8 — B1 DONE (2026-07-26). CHL Scenario 2 reproduced: the modified rescaling (4.1)/(4.2).
LOGGED run, predicate LOCKED in git before the run (commit b5294ff). PARTIAL/Tier-2 by design —
NOT novel, NOT a proof. Full data: committed `writeup/data/p2_scenario2_relax.json`; harness
`experiments/p2_scenario2_relax.py --logged`.

**What was built (the transferable deliverable).** `solver/hl_rescaled.py::RescaledHLScenario2` —
CHL's modified formulation (4.1): transport `(U+c_l X)→(U+c_l X+c_r)` with a spatial-shift DOF
`c_r`, evolving `V:=Θ_X`. Normalization (4.2): pin `∂_τΩ(0)=∂_τΩ_X(0)=∂_τV(0)=0` at the shifted
ORIGIN via a hand-rolled 3×3 solve (`_solve_3x3`, no scipy) each step for `(c_l,c_ω,c_r)`. Grid is
origin-clustered with **X=0 a node** (so the gauge reads Ω(0),Ω_X(0),Ω_XX(0),V(0),V_X(0),U_X(0)=
H(Ω)(0) at a node — the accuracy this brick buys over §6's X=1 grid). `scenario2_ic` = generic
non-symmetric positive **origin-NONdegenerate** data (Scenario 2 lives at a non-symmetry origin:
Ω_X(0)≠0 is the coefficient of c_l — degenerate_ic would make the gauge singular). Unit tests
`test_hl_rescaled.py` **9/9**: `_solve_3x3` matches numpy (7e-14) + flags singular systems, and the
KNOWN-ANSWER gauge test — the (4.2) solve nulls `∂_τ{Ω(0),Ω_X(0),V(0)}` to **4.4e-16**.

**WHY this is the right brick (honoring the user's steer):** the §6/§7 degenerate gauge pins
`c_l=−U(1)` (stagnation at X=1) — the reframe scout MEASURED that it cannot HOLD a profile peaked
away from X=1. CHL's (4.2) origin-pinned gauge CAN. That origin-pinned gauge is exactly what a gCLM
two-scale↔two-stage sweep (the actual lottery-ticket angle) needs to hold regular profiles across
the parameter `a`. B1 = "the gCLM-ready gauge, VALIDATED against a known answer", not a trophy.

**LOGGED RESULT (n=801, nu=0.02, 2 ICs × 14000 steps, adaptive dt → τ≈42; 5/5 PARTIAL):**
- **S1 ratio known-answer PASS:** generic IC (x0=0.30) → `c_l/c_ω = −2.5334` (CHL −2.5114, ~0.9%).
- **S2 attractor PASS:** 2nd IC (x0=0.45, different width) → −2.5352, same ratio ⇒ genuine
  IC-independent attractor (not a tuned initial condition).
- **S3 regular positive PASS:** min Ω=5.6e-2>0, min V>0, smoothness max|Ω_X|/peak=0.73 (vs ≈1061
  for the singular anchor), peaked at X*=0.82 (non-symmetric). = CHL's Scenario-2 object.
- **S4 residual bounded+falling PASS:** res 15→2.2e-2 (≈680×), no blowup.
- **S5 HONEST CEILING PASS (predicted):** res FLOORS at 2.2e-2 (does NOT reach CHL's 1e-6) AND the
  absolute triple stays off CHL's raw `(1.0636,−0.4235,0.0765)` — ours drift to `(1.59,−0.63,0.21)`.

**THE HONEST READ.** The amplitude-INVARIANT contraction exponent `γ=c_l/c_ω` — the physical
Scenario-2 prediction — is reproduced to ~1% as a real attractor to a regular positive profile.
The ABSOLUTE `(c_l,c_ω,c_r)` are IC-normalization-dependent (the (4.2) gauge holds Ω(0),Ω_X(0),V(0)
at their initial values; matching CHL's raw triple needs matching their IC normalization) AND the
fixed grid floors the residual at ~2e-2 (CHL reach 1e-6 with an adaptive mesh). So: **both CHL
scenarios now reproduced** (§2 singular Stage-2 anchor + §8 regular Stage-2/Scenario-2 exponent).
Tier-2 consolidation. The lottery ticket still lives elsewhere — the gCLM two-scale↔two-stage
transition (uses the now-validated origin-pinned gauge machinery) or a rigor step on Conj 2.4.

## §9 — GA GLOBAL-SEARCH FRAMEWORK DONE (2026-07-26). Validated INFRASTRUCTURE for the gCLM two-scale↔two-stage probe. NOT a science result.

Banked record: writeup/4_p2_lottery/TECHNICAL_P2_GA_FRAMEWORK.md + BLOG_P2_GA_FRAMEWORK.md + fig16 (rebuilds from
committed writeup/data/p2_ga_framework.json via `python writeup/4_p2_lottery/p2_ga_framework_evidence.py`).
Code: solver/gclm_family.py, solver/ga_search.py; tests test_gclm_family.py (6/6; full suite **7/7**).

**The user's steer this session:** pursue the gCLM two-scale↔two-stage transition as the novelty
swing, and do it VIA a genetic algorithm (their idea) — build the GA so it also serves Route D. Target
chosen (with the user): **gCLM axis first (anchored, tractable), then bridge to HL.**

**Why a GA (honest).** The self-similar profile is a fixed point of a rescaled flow; a family can have
MULTIPLE fixed points (different mechanisms). Relaxation (§6, §8) is LOCAL — slides into the attractor
you seed near, blind to the rest. A GLOBAL search over (shape + exponents) can map the fixed-point set
and its bifurcations = the open two-scale↔two-stage question. A GA proves nothing (Tier-1/2 only); its
two honest roles are (i) this global mapper and (ii) the "guess" stage for a Route-D interval-Newton
certification. Framework built to serve both (the residual object is reusable).

**Key upstream fact banked.** The two-scale ANCHOR paper is **[HQW25] = arXiv:2401.14615** (Huang–Qin–
Wang, SIAM J Math Anal 57(4) 2025) — downloaded to Papers/2401.14615v_HQW25.pdf (gitignored). It gives
the EXACT a=0 two-scale profile Ω₂(z) = −a³b^{3/2}c/(a⁴c²+b⁴z²) (an EVEN Lorentzian bump, c_ω=−3/2,
c_l=1, c_s=1/2) — a clean known answer for the two-scale end. NOTE the original "bisect in `a` between
CLM and HL" framing was corrected: HQW25 two-scale is CLM=a=0 (scalar gCLM family); CHL two-stage is
the HL COUPLED (ω,θ) system — NOT the same `a`-axis. So the well-posed gCLM-axis question is: **does
HQW25's a=0 two-scale mechanism survive advection as `a` grows?** (bridge to HL is a separate later leg).

**What was BUILT + VALIDATED:**
- `solver/gclm_family.py::GCLMResidual` — the gCLM `a`-family rescaled steady residual
  R = (c_ω+HΩ)Ω − c_l XΩ_X − a U Ω_X, with velocity U=∫₀ˣHΩ (cached cumulative-trapezoid `Vmat`,
  U(0)=0), on the sinh grid, reusing the dense line-Hilbert operator. SEPARATE from the relaxation
  solvers (this evaluates a candidate's residual; they time-step). `a` is a sweep parameter.
- `solver/ga_search.py::ga_minimize` — generic real-coded GA (tournament + BLX-α + annealed Gaussian
  mutation + elitism; no scipy; deterministic per seed). Problem-agnostic (Route-D reusable).
- Parametric genomes: `odd_rational` (one-scale/De-Gregorio; K=1 @ (−4,4) = exact Ω₀), `even_lorentz`
  (two-scale bump symmetry).

**a=0 KNOWN-ANSWER GATE (passes):** exact Ω₀=−4X/(1+4X²) nulls R to RMS **2.2e-7** (c_ω=−0.99914);
velocity integrates to arctan(2X) (bulk err 8.5e-3; tail error where Ω_X→0, harmless); odd parity
1e-13; a≠0 breaks the a=0 profile (R climbs ~linearly in a — the map's target). The GA recovers the
exact steady set — but as a **1-parameter DILATION FAMILY** {A=−4β,B=4β²}: the rescaling gauge is
dilation-invariant, so only the invariant **A²/B=4.000** (and the shape) is a "match" (Fig16A = a
valley, not a basin). Pinning B=4 → A=−3.9999. This is the banked "report gauge-invariants only"
lesson appearing in the optimization landscape itself.

**DIAGNOSTIC LOCKED (the crux, pre-any-logged-run):**
- **D1 scale separation (primary):** L_wid/L_loc → 0 with log-log slope c_l/c_s=2 ⟺ two-scale;
  O(1) ⟺ one-scale.
- **D2 blowup power (confirm):** invariant c_l/c_ω = −2/3 (two-scale, c_ω=−3/2) vs −1 (one-scale).
- **Resolution guard (mandatory):** D1 valid only while L_wid spans ≳8 grid pts; below → INCONCLUSIVE
  / "needs adaptive mesh", NEVER "scales merged" (same floor that capped B1/§6).

**DIAGNOSTIC REFINED AT DERIVATION TIME (honest correction to the pre-derivation D1/D2 above).** Once
the two-scale residual was actually derived (below), "two-scale" turned out to mean an EVEN, TRAVELING
(c_tw≠0) localized profile — a pure traveling wave, NOT a dilation scale-separation object. So the
logged sweep measures the scale-invariant residual FLOOR + the traveling speed c_tw + the profile
symmetry/width, not the L_wid/L_loc slope. The resolution guard (≳8 grid pts, else INCONCLUSIVE) was
kept verbatim and PASSED (min 49 pts). D1/D2's exponent framing belongs to the *blowup*, not the
traveling-wave *profile* the GA maps; noting the swap here so the record is honest.

### §9 (cont.) — TWO-SCALE RESIDUAL DERIVED + a-SWEEP LOGGED (2026-07-26). 5/6 PARTIAL. Novel, Tier-1/2.

**THE DERIVATION (the hard part, now done).** HQW25 §2.4: the two-scale blowup profile is an EXACT
TRAVELING WAVE. Carry ω=(T−t)^{c_ω}Ω(z), z=(x−r(t)(T−t)^{c_s})/(T−t)^{c_l} (c_ω=−3/2,c_l=1,c_s=1/2)
through gCLM ω_t+a u ω_x=ωHω. Leading (T−t)^{−3} balance: the dilation −c_l XΩ_X and amplitude c_ω Ω
terms are SUBLEADING ((T−t)^{−5/2}) and DROP; the moving-frame term survives as a pure TRANSLATION.
Advection enters at the SAME order as stretching. Result:
  **R₂(Ω) = Ω H(Ω) − c_tw Ω_X − a U Ω_X**,  U=∫₀ˣHΩ,  c_tw=c_s·r  (traveling-wave speed = gauge).
STRUCTURALLY a translation (const×Ω_X), NOT the one-scale dilation (X×Ω_X). a=0 anchor (a=b=c=1 norm):
**Ω₂=−1/(1+X²), H(Ω₂)=−X/(1+X²), c_tw=1/2**; nulls R₂ to **1.5e-9**. EVERY even_lorentz A/(1+BX²) is an
exact a=0 TW with c_tw=−A/(2√B) → a=0 set is a **2-parameter scaling valley** (deeper form of "report
invariants"). Code: solver/gclm_family.py::{residual_two_scale, gauge_c_tw, residual_two_scale_relnorm,
clm_two_scale, rational_mixed}; tests test_gclm_family.py 11/11 (full suite 7 files green).

**THE FITNESS BUG (caught pre-lock).** Plain RMS ‖R₂‖ is NOT scale-invariant — GA drives amplitude→0
(c_tw→0), trivial null (scratch showed it). Use **relres=‖R₂‖/‖ΩHΩ‖** (scale-invariant; one-scale Ω₀
scores >0.1, not gamed). Pre-lock scout: floor INVARIANT across n=601/801/1201 & rho_max=8/10 (physical,
not tail artifact) + GA-converged. Config locked n=801, 6 seeds; predicate T1–T6 in the harness docstring,
committed 6fc1ff0 before the run.

**RESULT (5/6, commit-after-run).** T1 known-answer PASS (a=0 relres 5.8e-8). T2 persistence PASS
(a_p=0.40, relres<1e-2). T3 monotone-degradation PASS (floor→0.18 at a=1). T5 symmetry PASS (odd-frac
<0.013; mixed genome free to skew STAYS EVEN). T6 resolution-guard PASS (min 49 pts). **T4 FAIL =
GENOME-LIMITED (the honest headline):** at a=0.5 even-K3 cuts floor 4× (2.45e-2→5.6e-3) → K=2 map is a
genome-relative UPPER BOUND, survival boundary NOT sharply pinned (pre-committed INCONCLUSIVE branch,
reported). BUT a=1 K=3 does NOT rescue (1.83e-1→1.43e-1) → De Gregorio-end degradation robust.
**Picture:** HQW25's exact a=0 two-scale traveling wave DEFORMS SMOOTHLY under advection — no sharp
collapse, persists small-a, degrades to De Gregorio, stays even, advection SELECTS a scale (lifts the
valley). Fig17 (writeup/4_p2_lottery/p2_two_scale_sweep_evidence.py, rebuilds from writeup/data/p2_two_scale_sweep.json).
TECHNICAL/BLOG_P2_TWO_SCALE.md.

**HONEST CEILING + NEXT.** A GA proves nothing (Tier-1/2); this is a genuine NEW MAP (HQW25 anchor + §9
machinery), the lottery ticket's first scientific brick — but NOT a proof, NOT a Clay solve. Did NOT
re-run to chase T4 (the fail is the machine catching its own limit). NEXT candidates: (a) richer/spectral
genome or a Route-D interval-Newton on these guesses to sharpen a_p; (b) the SEPARATE coupled-system leg
(HL two-stage — HL is not a scalar gCLM member). Clay odds unchanged ~0.05%.

## §10 — ROUTE-D v1 DONE (2026-07-26): interval core + a=0 NK framing. Level-1 tooling + scoping, NOT a certificate.

The first brick on the RIGOR LADDER (Level-1→Level-2). Delivered: (a) a hand-rolled rigorous
interval-arithmetic core solver/interval.py (no scipy/mpmath; outward-rounded +−×÷, reciprocal,
isum/dot/matvec with the γ_m accumulation bound) + test_interval.py 5/5 gated with `fractions` as the
exact oracle (full suite now 8 files green); (b) the deterministic a=0 probe experiments/p2_route_d_probe.py
→ writeup/data/p2_route_d_probe.json → fig19 (writeup/4_p2_lottery/p2_route_d_evidence.py). NOT a logged Tier run (no GA,
no seeds, no predicate lock — every number is a deterministic property of the anchor + fixed operators).
BLOG/TECHNICAL_P2_ROUTED.md.

FOUR evidence pieces (all banked, do not relearn):
  Q1 ARITHMETIC PRECISION. Rigorous interval enclosure of R₂ at the exact anchor Ω₂=−1/(1+X²), c_tw=1/2:
     defect 8.9e-10, enclosure WIDTH 8.5e-11 → overhead ~10% (n=2001). The interval core is precise enough
     to carry the NK defect bound Y₀. Genome-box sup|R₂| grows slope-1 (Lipschitz ~190), not wrapping.
  Q2 DEGENERACY COUNTED. a=0 zero set = 2-parameter scaling valley (amplitude (Ω,c)↦(λΩ,λc) + dilation
     (Ω,c)↦(Ω(·/μ),μc)). Jacobian SVs: gauge-slaved c → [2.0e-7,1.3e-7] (BOTH tiny = 2-dim kernel); fixed
     c=1/2 → [5.90,9.3e-7] (1-dim kernel). ⇒ EXACTLY TWO gauge conditions (speed + one normalization)
     isolate a nondegenerate zero. Concrete: fix c=1/2 + Ω(0)=−1 forces μ=1 (the c-preserving fiber is
     λμ=1, Ω(0)↦(1/μ)Ω(0)). The naive un-gauged interval-Newton has ‖DF⁻¹‖=∞ — gauge quotient NOT optional.
  Q3 DIAGONALIZATION (the structural gift). Under X=tan(θ/2) the LINE Hilbert transform = the CIRCULAR
     conjugate (cos kθ↦sin kθ), verified ~1e-7 for k=1..6 on the DECAYING (endpoint-vanishing at θ=±π)
     subspace. Anchor is then a 2-term Fourier object: Ω₂=−(1+cosθ)/2 (a₀=a₁=−1/2), H(Ω₂)=−½sinθ.
  Q4 BANDED OPERATOR. R₂ is ODD (Ω even ⇒ ΩHΩ,Ω_X odd) ⇒ DF maps cosine→sine coeffs. With Ω₂ degree-1,
     DF is TRIDIAGONAL (bandwidth 1) + a rank-1 c_tw column (−Ω₂,ₓ=−½sinθ−¼sin2θ). Closed-form band built
     in the probe (q4_operator_structure), cross-checks the grid operator to 3.9e-2 (the residual = the
     θ=±π Cayley endpoint correction = flagged sub-task R). Banded ⇒ finite-section NK bounds Z₀+Z₁<1 are
     PLAUSIBLE (tail dominated by c·(ik), O(1/(cN)) inverse bound).

THE FRAMING (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED.md §7; full paper draft was scratch/ROUTE_D_FRAMING.md). Standard
radii-polynomial NK: Y₀≥‖A F(x̄)‖, Z₀≥‖I−AA†‖, Z₁≥‖A(A†−DF)‖, Z₂≥‖A·D²F‖; p(r)=Z₂r²−(1−Z₀−Z₁)r+Y₀;
CLOSES iff Z₀+Z₁<1 and (1−Z₀−Z₁)²≥4Y₀Z₂. Two real simplifications: F QUADRATIC ⇒ Z₂ constant (no 3rd-order
term); anchor a finite trig poly ⇒ zero convolution tail. Space: weighted ℓ¹_ν cosine coeffs ⊕ ℝ.
OPEN RISKS (honest, do not drop): G = the exact gauge/Fredholm-index square system (fixed-c+1-norm vs
c-floating-bordered) — THE CRUX; R = the θ=±π endpoint rank-1 correction (the 3.9e-2); T = rigorous
O(1/(cN)) tail-inverse bound; a≠0 = no exact anchor off a=0 (Y₀ jumps ~1e-9→~1e-2) so a boundary certificate
likely will NOT close — probable honest "certifies at a=0, not yet at a≈0.5".

NEXT BRICK (user-confirmed direction): the FLOAT DRESS REHEARSAL — build DF as a finite (N+1)-mode matrix in
plain float, invert the finite section, compute Y₀/Z₀/Z₁/Z₂ + the radii polynomial across an N-ladder with
the §Q2 gauge. Answers the ONLY gating question — does Z₀+Z₁<1 and does the ball close at the anchor? — at
near-zero cost BEFORE any interval hardening. Green-lights the verified build or surfaces which sub-task
(G/R/T) blocks it (a legit publishable negative either way). Only after it closes in float do we harden with
solver/interval.py. HONEST CEILING unchanged: even full success = computer-assisted TOY-MODEL certification
(Chen–Hou / Gómez-Serrano genre), NOT a Clay solve. Clay odds ~0.05%.

## §11 — ROUTE-D v2 DONE (2026-07-28): the FLOAT DRESS REHEARSAL. **The NK ball does NOT close** — a
## structural NEGATIVE with a constructive repair. Level-1 tooling + scoping, NOT a certificate.

The §10 "next brick", executed. Built solver/nk_fourier.py (the EXACT closed-form Fourier operator — no
grid, no quadrature) + test_nk_fourier.py 6/6 (suite now **9 files green**); ran the deterministic ladder
experiments/p2_route_d_dress.py → writeup/data/p2_route_d_dress.json → fig20
(writeup/4_p2_lottery/p2_route_d_dress_evidence.py). NOT a logged Tier run (deterministic; no GA/seeds/
predicate lock). BLOG/TECHNICAL_P2_ROUTED_DRESS.md.

**HEADLINE: the radii polynomial closes at NO truncation (0/13 on N=4..256), and the measurements show it
CANNOT — at any N, under any gauge, with any positive weight. Cause located and confirmed by ablation:
the transport term c(1+cosθ)∂_θ DEGENERATES at θ=±π (X=∞).** Certification budget
Y₀^max=(1−Z₀−Z₁)²/(4Z₂) is IDENTICALLY ZERO at every N. (So the §10 worry that a≠0's Y₀~1e-2 would be too
big was beside the point: the apparatus cannot certify defect ZERO either.)

Exact operator (banked; supersedes the grid version for Route D):
  H(cos kθ)=sin kθ for EVERY k≥0, H(1)=0 — UNCONDITIONAL (Hardy/Cayley: e^{iθ}=(1+iX)/(1−iX) holomorphic in
  the UHP, G_k=e^{ikθ}−(−1)^k decays, H(Re G)=Im G). §10 Q3's "on the decaying subspace" caveat is
  unnecessary. f_X=(1+cosθ)f_θ. Anchor a=(−1/2,−1/2,0,…), c=1/2 nulls the residual EXACTLY (both terms are
  sinθ/4+sin2θ/8) — a sharper gate than the grid's 1e-9. Kernel directions in closed form: amplitude
  (½,½,0,…;δc=−½), dilation (⅛,0,−⅛,0,…;δc=−¼); fixed-c kernel w=−¼cosθ(1+cosθ)=(−⅛,−¼,−⅛,0,…).

SIX evidence pieces (do not relearn):
  D1 LADDER. ‖A_N‖_{ℓ¹} ~ N^0.97 (5.0→198.7 over N=4→256), σ_min ~ N^−0.98, cond ~ N^2.03. The gauged
     finite-section inverse is UNBOUNDED ⇒ not boundedly invertible in unweighted ℓ¹ ⇒ no truncation can
     certify. Y₀=0.0 exactly (anchor is an exact zero AND a degree-1 trig poly ⇒ zero convolution tail).
  D2 BOUNDS. Z₀~1e-11 (rounding only). Z₁ ≥ N+1 EXACTLY from the truncation coupling alone (5,17,65,257 at
     N=4,16,64,256) — the finite section couples MORE strongly to what it discards as N grows; bigger is
     strictly WORSE. Z₂=2‖A‖ diverges. Even the fiction "ignore the far field" does not close at any N.
  D3 GAUGE EXONERATED. origin / a0 / a1 normalizations ALL give N^0.97, curves on top of each other.
     **Sub-task G is NOT the blocker** (it still must be right for a real certificate, but it is cleared here).
  D4 CAUSAL ISOLATION (the decisive test). Replace the transport factor (1+cosθ)→1, change nothing else:
     ‖A_N‖ goes FLAT at exactly 4.0 (N^0.00) vs 198.7 (N^0.97). **Sub-task R (the θ=±π far field) is the
     CAUSE, not a suspect** — promoted from footnote to blocker.
  D5 FAR-FIELD MARGINALITY. Far-field DF columns are exactly tridiagonal (sub,diag,sup)=(ck/2, ck−½, ck/2−½).
     The Z₁ column weight → 1 from BELOW under the transport-diagonal tail model and from ABOVE under the true
     diagonal, both at O(1/k), c-independently ⇒ sup_{k>N} = 1 for every N; NOT a tail-model artifact. Root
     cause: multiplication by the symbol 1+cosφ has ℓ¹ norm 2 = exactly 2× its mean, because it VANISHES at
     φ=π. **No positive weight repairs it** (proof: z_w(k)≈(u_{k−1}+u_{k+1})/(2u_k), u_k=w_k/k; z_w≤1−δ forces
     u_{k+1}≤2(1−δ)u_k−u_{k−1} whose characteristic roots lie ON the unit circle ⇒ oscillation ⇒ any positive
     solution goes negative). Best possible = u affine (w_k=k(α+βk)) giving z_w≡1. Numerics agree.
  D6 THE REPAIR (the constructive half). Far-field ODE −c h_X − h/X = g with c=1/2 ⇒ (X²h)′=−2X²g ⇒
     h=2X^{−2}∫_X^∞ s²g ⇒ the inverse LOSES EXACTLY ONE POWER OF DECAY. Mode m resolves X~m, so predict
     ‖A e_m‖_{ℓ¹} ∝ m; MEASURED 1.97·m (fit on m≤N/8; the roll-over at m→N is the finite-section edge, where
     ‖A e_N‖=4 exactly at every N). Grade the CODOMAIN by one mode power (v_m=m, gauge row 1):
     **‖A‖ = 3.000, FLAT from N=8 to N=384 (N^0.00).** Other pairings diverge (ℓ¹→graded: N^1.94;
     graded→graded: N^0.95). ⇒ the certificate needs an ASYMMETRIC space pair one decay power apart.

BUG FIXED in the §10 probe: the closed-form band's k=0 column had an unfolded sin(−θ) (−1/4 instead of
−1/2); v1's grid cross-check only ran k≥1 so it never exercised the fold. experiments/p2_route_d_probe.py
fixed + cross-check extended to k=0; the two independently-written closed forms now agree to 0.0. Grid
cross-check unchanged at 3.9e-2 (that residual is the θ=±π endpoint correction, a different thing). Also
added the missing sys.path bootstrap to that probe.

NEXT BRICK (specification, NOT a promise): rebuild the bounds in the GRADED pair — domain ℓ¹ cosine coeffs,
codomain graded by one mode power, far-field block handled by the EXACT ODE inverse above instead of a
diagonal model (the standard "compact core + explicit far field" two-region structure of the Chen–Hou /
Gómez-Serrano genre). TWO things must be re-derived and neither is free: (i) the quadratic D²F[h,h]=2hH(h)
must land in the GRADED codomain — the Wiener-algebra bound only gives ℓ¹, so the DOMAIN norm likely has to
move too; (ii) the far-field inverse must be interval-enclosed, not asymptotic. Alternative lanes if that
stalls: the separate coupled-system HL two-stage leg, or extending the a_p(K) map to the odd/one-scale
channel (lower value). HONEST CEILING unchanged: everything in §11 is plain float64, nothing is
interval-enclosed, nothing is rigorous — running the rehearsal FIRST is exactly what saved hardening a set
of bounds that could never have closed. Clay odds ~0.05%.
