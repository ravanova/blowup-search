# Continuation prompt (copy into a fresh session)

*Written 2026-07-26 at the end of the session that built **Route-D v1** — the
rigorous interval-arithmetic core + the a=0 Newton–Kantorovich framing (the FIRST
brick on the Level-1→Level-2 rigor ladder) — and banked + pushed the full writeup
AND reorganized writeup/ into arc subfolders. Everything below is banked + pushed;
origin/main at commit **c91bfd3**. The RECOMMENDED next thing is the **float dress
rehearsal** of the Newton–Kantorovich bounds (does the certification ball close at
the a=0 anchor, in plain float, BEFORE any interval hardening?). Surface a short
options menu before committing to a heavy build.*

Continue the Navier–Stokes blow-up search project in /home/andy/projects/Unsolved.
End goal: the Clay Millennium problem — a genuine, honest attempt via
singular-profile / self-similar-blowup research — while never fooling ourselves with
a numerical artifact. WIN_CONDITION.md is the anti-self-deception contract: only
Tier 3 / Level 3 (rigorous proof) solves it; Tier 1 (candidate) and Tier 2
(resolution-confirmed) are progress. Preserve that honesty — do not oversell. Raise
genuine scope decisions for review with a short options menu rather than deciding
unilaterally.

USER'S STANDING STEER (honor it): Keep pursuing the Clay end goal. The realistic
prize is novel toy-model singularity research + a tiny (~0.05%) Clay "lottery
ticket," NOT a Clay solve. Keep the lottery ticket the true focus; when something
does NOT contribute to it, say so and be willing to pivot. Gate-check every new
brick against "does this help the real direction" BEFORE building. The chosen
vehicle is a GENETIC ALGORITHM as the global fixed-point mapper for gCLM
self-similar profiles, built to ALSO feed Route D (the GA-found approximate profile
is the "guess" a rigorous interval-Newton certifies). Produce blog + community
writeups WITH ATTACHED DATA (writeup/ + committed writeup/data/*.json that rebuilds
figures without re-runs).

THE LEVEL / RIGOR LADDER (the user's framing, honor it): Level-0 = reproduce known
results. Level-1 = a novel numerical map (where ALL gCLM work through fig18 sits).
Level-2 = a rigorous computer-assisted statement (interval / Newton–Kantorovich
certification) = the FIRST rung that is genuinely "novel maths" — **Route-D v1
(fig19) is the first brick here, but it is validated TOOLING + a framing/scoping
result, NOT yet a certificate.** Level-3 = Clay.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling numerics + the GA framework
are Route-A TOOLING (built to FEED Route D). "Route D" proper is the Tier-3
computer-assisted-proof leg; a successful interval-Newton certification is its first
concrete step. A GA proves nothing (Tier-1/2 only).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md.
**NOTE the writeup/ folder was reorganized into arc subfolders this session**
(1_gclm_1d, 2_phase1_2d, 3_spikes, 4_p2_lottery; data/ + figures/ stay central; see
writeup/README.md for the full ordered index). Phase 1 (concluded negative):
writeup/2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md. P2 — READ: PHASE2_P2_NOTES.md
(TOP STATUS + §2 anchor, §6 degenerate gauge, §7 reframe, §8 B1, §9 GA framework,
§9-cont TWO-SCALE, §9-cont2 a_p(K) map, **§10 ROUTE-D v1 = newest**). Per-leg
writeups + figs all under writeup/4_p2_lottery/: TECHNICAL/BLOG_P2_{HL_ANCHOR(fig12),
CONJ24(fig13),SCENARIO2(fig14/15),GA_FRAMEWORK(fig16),TWO_SCALE(fig17),KLADDER(fig18),
ROUTED(fig19)}.md. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed; origin/main at c91bfd3):
- Phase 1 CONCLUDED. Spike 0/1 DONE. P2 anchor (§2), §6 degenerate-gauge, §7 reframe,
  §8 B1 (Scenario-2), §9 GA framework, §9-cont two-scale a-sweep (5/6), §9-cont2
  a_p(K) convergence map (7/7) — all DONE + banked.
- The gCLM two-scale survival boundary is GENUINE (a*≈0.5–0.55, a SOFT crossing),
  not genome-limited (§9-cont2 earned this via GA-/genome-/basis-convergence).

**P2 §10 — ROUTE-D v1 DONE + BANKED (this session). Level-1 tooling + a Level-2
scoping/framing result, NOT a certificate.** The first brick on the rigor ladder.
Delivered:
- **solver/interval.py** — hand-rolled RIGOROUS interval arithmetic (no scipy/mpmath;
  outward-rounded +−×÷ via np.nextafter one-ulp push, reciprocal with zero-guard,
  and isum/dot/matvec with the γ_m = m·u/(1−m·u) accumulation bound). **test_interval.py
  5/5**, gated with `fractions` as the exact oracle. Full suite now **8 files green**.
- **experiments/p2_route_d_probe.py** (deterministic, NON-logged — no GA/seeds/predicate)
  → writeup/data/p2_route_d_probe.json → fig19
  (writeup/4_p2_lottery/p2_route_d_evidence.py). Four results:
  * **Q1 (arithmetic precision):** at the exact a=0 anchor Ω₂=−1/(1+X²), c_tw=1/2, the
    rigorous enclosure width (8.5e-11) is ~10% of the defect (8.9e-10) → the interval
    core comfortably carries the NK defect bound Y₀.
  * **Q2 (degeneracy COUNTED):** the a=0 zero set is a 2-parameter scaling valley
    (amplitude (Ω,c)↦(λΩ,λc) + dilation (Ω,c)↦(Ω(·/μ),μc)). Jacobian singular values:
    gauge-slaved c → 2-dim kernel; fixed c=1/2 → 1-dim kernel. ⇒ EXACTLY TWO gauge
    conditions (speed + one normalization, e.g. c=1/2 & Ω(0)=−1 forcing μ=1) isolate a
    nondegenerate zero. The naive un-gauged interval-Newton has ‖DF⁻¹‖=∞.
  * **Q3 (diagonalization — the structural gift):** under X=tan(θ/2) the LINE Hilbert
    transform = the CIRCULAR conjugate (cos kθ↦sin kθ), verified ~1e-7 for k=1..6 on the
    decaying subspace. The anchor is then a 2-term Fourier object Ω₂=−(1+cosθ)/2,
    H(Ω₂)=−½sinθ.
  * **Q4 (banded operator):** R₂ is ODD (Ω even ⇒ ΩHΩ, Ω_X odd) ⇒ DF maps cosine→sine
    coeffs and is TRIDIAGONAL (bandwidth 1) + a rank-1 c_tw column. Closed-form band
    (built in the probe) cross-checks the grid operator to 3.9e-2 (= the flagged θ=±π
    Cayley endpoint correction). Banded ⇒ finite-section Z₀+Z₁<1 is PLAUSIBLE.
- **THE FRAMING** (writeup/4_p2_lottery/TECHNICAL_P2_ROUTED.md §7): standard
  radii-polynomial NK — Y₀≥‖A F(x̄)‖, Z₀≥‖I−AA†‖, Z₁≥‖A(A†−DF)‖, Z₂≥‖A·D²F‖;
  p(r)=Z₂r²−(1−Z₀−Z₁)r+Y₀; CLOSES iff Z₀+Z₁<1 and (1−Z₀−Z₁)²≥4Y₀Z₂. F QUADRATIC ⇒ Z₂
  CONSTANT (no 3rd-order term); anchor a finite trig poly ⇒ zero convolution tail. Space:
  weighted ℓ¹_ν cosine coeffs ⊕ ℝ. OPEN RISKS (do not drop): **G** = the exact
  gauge/Fredholm-index square system (fixed-c+1-norm vs c-floating-bordered for the 1-D
  cokernel) = THE CRUX; **R** = the θ=±π endpoint rank-1 correction; **T** = a rigorous
  O(1/(cN)) tridiagonal tail-inverse bound; **a≠0** = no exact anchor off a=0 (Y₀ jumps
  ~1e-9→~1e-2) so a boundary certificate likely will NOT close → probable honest
  "certifies at a=0, not yet at a≈0.5".

THE NEXT BRICK — THE FLOAT DRESS REHEARSAL (recommended; surface a menu first).
Build DF as a finite (N+1)-mode matrix in PLAIN FLOATING POINT (using the closed-form
cos→sin band from probe q4_operator_structure, validated there), invert the finite
section, and compute Y₀, Z₀, Z₁, Z₂ and the radii polynomial across a small N-ladder
with the §Q2 gauge (fix c=1/2, Ω(0)=−1). This answers the ONE question that gates
everything — **does Z₀+Z₁<1 and does the ball close at the anchor?** — at near-zero
cost, BEFORE spending effort on the verified interval enclosure (solver/interval.py).
If it closes in float with margin → green-light the interval build (harden Y₀/Z₀ with
matvec/verified-inverse enclosures). If it does NOT close → inspect which sub-task
(G/R/T) blocks it and report the honest, publishable negative ("why the naive NK
doesn't close here yet"). Either outcome is a legitimate result. Do NOT skip to
claiming a certificate. Overall Clay odds unchanged (~0.05%).

Alternative bricks (put a short menu to the user if the dress rehearsal stalls or
they want a different lane): (a) nail sub-task **G** (the gauge/index bordered
operator) on paper first if the float rehearsal is ambiguous; (b) the separate
coupled-system HL two-stage leg (whether an HL-type two-stage appears at any scalar
gCLM member or genuinely needs the coupled (ω,θ) system); (c) extend the a_p(K) map
to the odd/one-scale channel (lower value — refines a Level-1 map, does not advance
Route D).

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy —
tridiag/solvers/3×3/GA/Hilbert/interval-arith all hand-rolled). 8-worker ceiling
(OMP_NUM_THREADS=8 pinned). No pytest; run each suite as `python test_X.py`. Suites
(all 8 green): **test_interval.py (5/5, NEW)** + test_gclm_family.py (12/12) +
test_hl_rescaled.py (9/9) + test_line_hilbert.py (6/6) + test_gclm_rescaled.py (5/5) +
test_boussinesq_{velocity,transport,rescaled}.py (5/5,5/5,8/8). Before ANY logged
experimental run: pass the test gate + COMMIT + LOCK the predicate in git (dirty-tree
guard; gitignored experiments/*.{log,npz,jsonl,out} fine). Solver dev + unit tests +
DETERMINISTIC scoping probes are NOT "logged gate runs" (the Route-D probe is
deterministic — no predicate lock needed); still add each new solver test to the
suite. Papers/ gitignored ([HQW25]=arXiv:2401.14615 → Papers/hqw25.txt). One
JOURNAL.md entry per logged experiment (deterministic tooling probes may get a
clearly-labelled non-logged entry too, as §10 did). Push only when asked.

**WRITEUP STRUCTURE (reorganized this session — use the new paths):** writeup/ now
has arc subfolders. Evidence rebuilds (each reads committed writeup/data/*.json):
writeup/4_p2_lottery/{p2_route_d_evidence.py(fig19), p2_two_scale_kladder_evidence.py
(fig18), p2_two_scale_sweep_evidence.py(fig17), p2_ga_framework_evidence.py(fig16),
p2_scenario2_evidence.py(fig15), p2_regular_profile_evidence.py(fig14),
p2_conj24_evidence.py(fig13), p2_hl_anchor_evidence.py(fig12)};
writeup/3_spikes/{spike0,spike1_stepA/B/C}_evidence.py; central
writeup/build_figures.py (figs 1–7). writeup/README.md is the ordered index.

OPS: DISK WATCH — root fs has hit 100% mid-session before (scratch + project share
/dev/nvme0n1p3); `df -h /` if writes fail with ENOSPC. Never `pgrep -f script.py`
while it self-matches (hang). Foreground `sleep` blocked (use background runs /
Monitor until-loop). The GA at the converged budget (pop150/gen250/8seeds) ≈ 30–45
s/best_of at n=801; base-budget GA ≈ 1 s. The Route-D probe is ~10 s. Run `python -u`
to a LOGFILE, wait on a Monitor until-loop — do NOT pipe through tail. Reuse solver
instances (dense Hmat/Vmat cached lazily).

DISCIPLINE LESSONS BANKED (do not relearn): Ground the scheme in the paper; DERIVE
the exact answer where one exists and gate against it (Ω₀→2.2e-7, Ω₂→1.5e-9; for
Route D, gate the interval arithmetic + the NK bounds against the a=0 anchor). Make
the fitness/observable scale-/gauge-invariant or the optimizer games it (the c_tw→0
amplitude-collapse bug). Report gauge/genome/budget/basis invariants and upper-bound
caveats, never a sharp claim a fixed genome/budget can't support (the T4 lesson).
Near-transition GA floors are SEARCH-limited at low budget — use a converged budget +
a budget spot-check for any floor/boundary claim. Fixed-grid dynamic-relaxation FLOORS
the residual (~1e-2) and can't resolve a collapsing FINE inner scale — the GA static
map sidesteps the time-stepping floor. For Route D specifically: a Level-2 claim is
only as honest as its arithmetic — the bounds MUST be interval-enclosed (float is for
the dress rehearsal only), and the gauge quotient is NOT optional (Q2). Do a FLOAT
dress rehearsal before hardening. Do NOT re-run/tune to chase a bound into closing —
report honestly if it does not.

HONEST CEILING (say it out loud): Route-D v1 is validated tooling + a scoping/framing
result; it does NOT itself climb the rigor ladder — it makes the certification attempt
concrete and grounded (the central operator is banded, said with evidence). Even the
eventual success it aims at is a computer-assisted TOY-MODEL certification (Chen–Hou /
Gómez-Serrano genre), NOT a Clay solve. 1D HL is a toy model (boundary behaviour of
Hou–Luo / 3D-axisymmetric-Euler). Overall Clay odds ~0.05%. Keep pursuing the Clay end
goal; keep saying the honest version out loud.
