# Continuation prompt (copy into a fresh session)

*Written 2026-07-28 at the end of the session that ran the **Route-D v2 float dress
rehearsal** — the gating test §10 called for — and got an **honest structural
NEGATIVE with a constructive repair**: the Newton–Kantorovich ball does NOT close
at the a=0 anchor, at any truncation, under any gauge, with any weight; the cause
is isolated by ablation (the transport term degenerates at X=∞); and the fix is
identified and measured (an asymmetric decay-graded space pair in which ‖A‖=3.000
flat). Everything below is banked + pushed on branch
`claude/continuation-prompt-work-e7xluq`. The RECOMMENDED next thing is **the
graded-space rebuild (Route-D v3)** — but read the "IS THIS STILL THE RIGHT LANE?"
box first and put a short options menu to the user, because v2 changed the odds on
this leg.*

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
(fig19) and v2 (fig20) are tooling + scoping/negative results on the way there,
NOT certificates.** Level-3 = Clay.

TERMINOLOGY GUARD (do not drop): the dynamic-rescaling numerics + the GA framework
are Route-A TOOLING (built to FEED Route D). "Route D" proper is the Tier-3
computer-assisted-proof leg; a successful interval-Newton certification is its first
concrete step. A GA proves nothing (Tier-1/2 only).

ORIENTATION (read in this order): PROJECT.md, WIN_CONDITION.md, CLAY_ROADMAP.md.
writeup/ has arc subfolders (1_gclm_1d, 2_phase1_2d, 3_spikes, 4_p2_lottery; data/ +
figures/ stay central; writeup/README.md is the ordered index). Phase 1 (concluded
negative): writeup/2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md. P2 — READ:
PHASE2_P2_NOTES.md (TOP STATUS + §2 anchor, §6 degenerate gauge, §7 reframe, §8 B1,
§9 GA framework, §9-cont TWO-SCALE, §9-cont2 a_p(K) map, §10 ROUTE-D v1,
**§11 ROUTE-D v2 = newest**). Per-leg writeups + figs under writeup/4_p2_lottery/:
TECHNICAL/BLOG_P2_{HL_ANCHOR(fig12),CONJ24(fig13),SCENARIO2(fig14/15),
GA_FRAMEWORK(fig16),TWO_SCALE(fig17),KLADDER(fig18),ROUTED(fig19),
ROUTED_DRESS(fig20)}.md. Then experiments/JOURNAL.md (newest first) and LOGGING.md.

STATE (all banked + pushed):
- Phase 1 CONCLUDED. Spike 0/1 DONE. P2 anchor (§2), §6 degenerate-gauge, §7 reframe,
  §8 B1 (Scenario-2), §9 GA framework, §9-cont two-scale a-sweep (5/6), §9-cont2
  a_p(K) convergence map (7/7), §10 Route-D v1, §11 Route-D v2 — all DONE + banked.
- The gCLM two-scale survival boundary is GENUINE (a*≈0.5–0.55, a SOFT crossing),
  not genome-limited (§9-cont2 earned this via GA-/genome-/basis-convergence).

**P2 §11 — ROUTE-D v2 DONE + BANKED (this session). The dress rehearsal came back
NEGATIVE, and the negative is the result.** Delivered:
- **solver/nk_fourier.py** — the EXACT closed-form Fourier operator (no grid, no
  quadrature): residual / jacobian / dc_column as closed-form polynomials in the
  cosine coefficients, the gauged square system, ℓ¹ operator norms, the radii
  polynomial, and the far-field band + weight algebra. The anchor a=(−½,−½,0,…),
  c=½ nulls the residual to **0.0 exactly** (vs the grid's 1e-9). **test_nk_fourier.py
  6/6**, gated against THREE oracles (exact anchor, finite differences, the banked
  grid residual). Full suite now **9 files green**.
- **experiments/p2_route_d_dress.py** (deterministic, NON-logged) →
  writeup/data/p2_route_d_dress.json → fig20
  (writeup/4_p2_lottery/p2_route_d_dress_evidence.py). Six results:
  * **D1 the ladder:** ‖A_N‖_ℓ¹ ~ **N^0.97** (5.0→198.7 over N=4→256), σ_min~N^−0.98,
    cond~N^2.03. The gauged finite-section inverse is UNBOUNDED in unweighted ℓ¹.
  * **D2 the bounds:** Y₀=0.0 exactly (anchor is an exact zero AND a degree-1 trig
    poly ⇒ zero convolution tail); Z₀~1e-11 (rounding); **Z₁ ≥ N+1 exactly** from the
    truncation coupling alone (bigger N is strictly WORSE); Z₂=2‖A‖ diverges.
    **Certification budget Y₀^max=(1−Z₀−Z₁)²/(4Z₂) ≡ 0 at every N. Closes 0/13.**
  * **D3 gauge EXONERATED:** origin/a0/a1 normalizations all give N^0.97, curves
    coincident. Sub-task **G** is NOT the blocker.
  * **D4 causal isolation (the decisive test):** replace the transport factor
    (1+cosθ)→1, change nothing else → ‖A_N‖ goes **FLAT at exactly 4.0** (N^0.00).
    Sub-task **R** (the θ=±π ⇔ X=∞ far field) is the **CAUSE**, not a suspect.
  * **D5 far-field marginality is structural:** far-field DF columns are exactly
    tridiagonal (ck/2, ck−½, ck/2−½); the Z₁ column weight → 1 from BELOW under the
    transport-diagonal tail model and from ABOVE under the true diagonal, both O(1/k),
    c-independent ⇒ sup_{k>N}=1 for every N (not a tail-model artifact). Root cause:
    multiplication by the symbol 1+cosφ has ℓ¹ norm 2 = exactly 2× its mean, because
    it VANISHES at φ=π. **No positive weight repairs it** — z_w(k)≈(u_{k−1}+u_{k+1})/
    (2u_k) with u_k=w_k/k; z_w≤1−δ forces a recursion whose characteristic roots lie
    ON the unit circle ⇒ oscillation ⇒ any positive solution goes negative.
  * **D6 THE REPAIR (constructive):** far-field ODE −c h_X − h/X = g with c=½ gives
    (X²h)′=−2X²g ⇒ h=2X^{−2}∫_X^∞ s²g ⇒ **the inverse loses EXACTLY one power of
    decay**. Mode m resolves X~m ⇒ predict ‖A e_m‖_ℓ¹ ∝ m; **MEASURED 1.97·m** (fit on
    m≤N/8; roll-over at m→N is the finite-section edge, ‖A e_N‖=4 exactly). Grading the
    CODOMAIN by one mode power (v_m=m, gauge row 1) gives **‖A‖ = 3.000, FLAT N=8..384**.
    Other pairings diverge (ℓ¹→graded N^1.94; graded→graded N^0.95).
- Also fixed a **k=0 fold bug** in the v1 probe's closed-form band (−1/4 instead of
  −1/2 — v1's cross-check only ran k≥1 so it never exercised the sin(−θ) fold). The two
  independently-written closed forms now agree to 0.0; no v1 conclusion changes. v1
  writeups carry supersede banners (its "Z₀+Z₁<1 is plausible" and its risk ordering
  are superseded; its "decaying subspace" caveat on H(cos kθ)=sin kθ is unnecessary —
  the identity is unconditional by a Hardy/Cayley argument, v2 §1).

**IS THIS STILL THE RIGHT LANE? (raise this with the user BEFORE building v3.)**
v2 is a legitimate, publishable brick, but be honest about what it did to the odds on
Route D. The a=0 certificate was always going to certify a solution already known in
closed form — its only value was as a rehearsal for a≠0. v2 shows the rehearsal fails
in the obvious space and that the repair needs a genuine two-region (compact core +
explicit far-field) apparatus. That is a real, multi-brick build, and at the end of it
the honest best case is still "certifies the a=0 traveling wave", with a≠0 (residual
floor ~1e-2, no exact anchor) still likely out of reach. Put the menu; do not assume.

THE RECOMMENDED NEXT BRICK — **Route-D v3, the graded-space rebuild** (if the user
keeps this lane). Redo the bounds in the asymmetric pair D6 identified: domain = ℓ¹
cosine coefficients, codomain graded by one mode power, with the far-field block
handled by the **exact ODE inverse** above rather than a diagonal model (this is the
standard Chen–Hou / Gómez-Serrano "compact core + explicit far field" structure).
TWO things must be re-derived and NEITHER is free, so scope them first:
  (i) the quadratic D²F[h,h]=2hH(h) must land in the GRADED codomain — the
      Wiener-algebra bound only gives ℓ¹, so the DOMAIN norm will probably have to
      move too, and the whole (X,Y) pair has to be re-chosen consistently. **Do this
      on paper/symbolically BEFORE coding**: if no consistent pair exists, that is
      itself the answer and the leg stops cheaply.
  (ii) the far-field inverse must be interval-ENCLOSED, not asymptotic.
Only after a graded-space float rehearsal closes with margin should solver/interval.py
be brought in. Do NOT skip to claiming a certificate.

Alternative lanes (put these in the menu): (a) the separate coupled-system HL
two-stage leg (whether an HL-type two-stage appears at any scalar gCLM member or
genuinely needs the coupled (ω,θ) system) — the biggest genuinely-novel swing left;
(b) extend the a_p(K) map to the odd/one-scale channel (lower value — refines a
Level-1 map, does not advance Route D); (c) write up the P2 arc as a single coherent
community piece (the 1D gCLM two-scale story + the Route-D negative) rather than
building further.

ENVIRONMENT & WORKFLOW: .venv/bin/python (numpy + matplotlib; NO scipy —
tridiag/solvers/3×3/GA/Hilbert/interval-arith/Fourier-operator all hand-rolled).
8-worker ceiling (OMP_NUM_THREADS=8 pinned). No pytest; run each suite as
`python test_X.py`. Suites (all 9 green): test_interval.py (5/5) +
**test_nk_fourier.py (6/6, NEW)** + test_gclm_family.py (12/12) + test_hl_rescaled.py
(9/9) + test_line_hilbert.py (6/6) + test_gclm_rescaled.py (5/5) +
test_boussinesq_{velocity,transport,rescaled}.py (5/5,5/5,8/8). Scripts under
experiments/ need the `sys.path.insert(0, dirname(dirname(abspath(__file__))))`
bootstrap (both Route-D probes now have it). Before ANY logged experimental run: pass
the test gate + COMMIT + LOCK the predicate in git (dirty-tree guard; gitignored
experiments/*.{log,npz,jsonl,out} fine). Solver dev + unit tests + DETERMINISTIC
scoping probes are NOT "logged gate runs" (both Route-D probes are deterministic — no
predicate lock needed); still add each new solver test to the suite. Papers/ gitignored
([HQW25]=arXiv:2401.14615 → Papers/hqw25.txt). One JOURNAL.md entry per logged
experiment (deterministic tooling probes get a clearly-labelled non-logged entry too,
as §10 and §11 did). Push only when asked.

**WRITEUP STRUCTURE:** evidence rebuilds (each reads committed writeup/data/*.json):
writeup/4_p2_lottery/{p2_route_d_dress_evidence.py(fig20), p2_route_d_evidence.py
(fig19), p2_two_scale_kladder_evidence.py(fig18), p2_two_scale_sweep_evidence.py
(fig17), p2_ga_framework_evidence.py(fig16), p2_scenario2_evidence.py(fig15),
p2_regular_profile_evidence.py(fig14), p2_conj24_evidence.py(fig13),
p2_hl_anchor_evidence.py(fig12)}; writeup/3_spikes/{spike0,spike1_stepA/B/C}_evidence.py;
central writeup/build_figures.py (figs 1–7). writeup/README.md is the ordered index.

OPS: DISK WATCH — root fs has hit 100% mid-session before; `df -h /` if writes fail
with ENOSPC. Never `pgrep -f script.py` while it self-matches (hang). Foreground
`sleep` blocked (use background runs / Monitor until-loop). The GA at the converged
budget (pop150/gen250/8seeds) ≈ 30–45 s/best_of at n=801; base-budget GA ≈ 1 s. The
Route-D v1 probe is ~10 s; the v2 dress ladder is a few seconds. Run `python -u` to a
LOGFILE, wait on a Monitor until-loop — do NOT pipe through tail. Reuse solver
instances (dense Hmat/Vmat cached lazily).

DISCIPLINE LESSONS BANKED (do not relearn): Ground the scheme in the paper; DERIVE
the exact answer where one exists and gate against it. Make the fitness/observable
scale-/gauge-invariant or the optimizer games it (the c_tw→0 amplitude-collapse bug).
Report gauge/genome/budget/basis invariants and upper-bound caveats, never a sharp
claim a fixed genome/budget can't support (the T4 lesson). Near-transition GA floors
are SEARCH-limited at low budget. Fixed-grid dynamic-relaxation FLOORS the residual
(~1e-2). **NEW from §11 — the four that earned their keep:** (1) **Do the cheap float
rehearsal BEFORE hardening.** It cost seconds and saved interval-enclosing a set of
bounds that could never have closed. (2) **Ablate to attribute.** Growth in ‖A_N‖ is a
suspicion; rebuilding the identical ladder with ONE feature removed ((1+cosθ)→1, flat
at 4.0) is an attribution. Always build the control. (3) **Build the same object twice.**
The exact Fourier operator vs the v1 grid-checked band disagreed, and the second build
was right — that is how the k=0 fold bug surfaced. (4) **A negative with a mechanism is
a result**; a negative without one is a failure. Chase the mechanism until it predicts a
number (here: "loses one power of decay" → ‖A e_m‖≈2m, measured 1.97m) and then let the
mechanism tell you what to build next. Do NOT re-run/tune to chase a bound into closing.

HONEST CEILING (say it out loud): Route-D v2 is validated tooling + a structural
negative; it does NOT climb the rigor ladder — it closes one route with a reason and
gives its replacement an address. Everything in it is plain float64: nothing is
interval-enclosed, nothing is rigorous. Even the eventual success it scouts is a
computer-assisted TOY-MODEL certification (Chen–Hou / Gómez-Serrano genre), NOT a Clay
solve. 1D HL is a toy model (boundary behaviour of Hou–Luo / 3D-axisymmetric-Euler).
Overall Clay odds ~0.05%. Keep pursuing the Clay end goal; keep saying the honest
version out loud.
