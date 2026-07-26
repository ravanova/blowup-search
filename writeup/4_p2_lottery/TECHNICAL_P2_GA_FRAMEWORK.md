# Phase-2 P2 — A genetic-algorithm global search for gCLM self-similar profiles: the framework and its a=0 known-answer gate

**Status: validated infrastructure, not a new blowup result.** This note documents
the search machinery built for the gCLM two-scale↔two-stage transition probe and
its validation against the one exact answer we have (the a=0 CLM profile). No
logged experimental run was performed; there is no new singularity claim here.
Its value is a *validated, gauge-aware global search* and a clearly-defined
diagnostic, ready for the logged sweep that comes next.

Rebuild the figure from committed data (no recompute):
`python writeup/4_p2_lottery/p2_ga_framework_evidence.py` → `writeup/figures/fig16_p2_ga_framework.png`
(reads `writeup/data/p2_ga_framework.json`; `--generate` recomputes it).

Code: `solver/gclm_family.py`, `solver/ga_search.py`, tests `test_gclm_family.py`
(6/6; full suite 7/7).

---

## 1. Why a global search, and why now

The self-similar blowup problem is a fixed-point problem: find a profile Ω and
scaling exponents such that the *rescaled* residual R(Ω) = 0. The family of 1D
models we study can have **several** fixed points — different blowup mechanisms
(one-scale, two-scale, …) are different steady states of the same rescaled flow.

Our existing tool, dynamic-rescaling *relaxation* (`solver/gclm_rescaled.py`,
`solver/hl_rescaled.py`), is a **local** method: it time-steps into whichever
attractor you seed near, and is blind to the others and to the unstable ones. To
*map* which fixed point a family selects as a parameter varies — and where it
bifurcates — a **global** search over (profile shape + exponents) is the natural
tool. That map is exactly the open question the probe targets (§5).

A genetic algorithm cannot produce a proof — nothing numerical can; per
`WIN_CONDITION.md` this is Tier-1/Tier-2 machinery only. It has two honest roles:
(i) the global fixed-point mapper here, and (ii) later, the "guess" stage of a
computer-assisted proof (Route D) — a GA-found approximate profile is exactly
what a rigorous interval-Newton step would certify. The framework is built so the
same residual object serves both (§2).

## 2. The problem object: the gCLM `a`-family rescaled residual

The generalized CLM family on the whole line (Okamoto–Sakajo–Wunsch convention):

    ω_t + a u ω_x = ω H(ω),     u_x = H(ω),  u(0) = 0,

with `a` the advection parameter — a=0 is CLM (exactly solvable; the anchor
below), a=1 is De Gregorio. Dynamic self-similar rescaling
ω(x,t) = C_ω⁻¹ Ω(X), X = C_l x, dτ/dt = C_ω⁻¹ carries this to the rescaled
evolution

    Ω_τ = (c_ω + H Ω) Ω − c_l X Ω_X − a U Ω_X,    U(X) = ∫₀ˣ H(Ω) dX′,   (∗)

so the steady **residual** scored by the search is

    R(Ω; c_ω, c_l, a) = (c_ω + H Ω) Ω − c_l X Ω_X − a U Ω_X.

`GCLMResidual` (`solver/gclm_family.py`) evaluates R on a fixed sinh-stretched
whole-line grid (`sinh_grid`, X = c·sinh ρ, X=0 a node), reusing the validated
dense line-Hilbert operator (`solver/line_hilbert.py`) and a cached cumulative-
trapezoid velocity operator `Vmat` (U = Vmat·HΩ, pinned U(0)=0). It is
deliberately **separate** from the relaxation solvers: those *time-step*; this
*evaluates the residual of an arbitrary candidate* so a global optimizer — or a
future interval-Newton — can score it. `a` is a **sweep parameter** (fixed per
instance); the transition map is built by instantiating across a range of `a`.

**Gauge.** `c_ω, c_l` are a normalization gauge, not results. We reuse the a=0
anchor's origin convention `c_ω = 1 − HΩ(0)`, `c_l = 1`; the physical, gauge-
invariant self-similar exponent is the ratio `c_l/c_ω` and the profile shape.

**Derived-and-tested pieces** (discipline: derive the exact answer, test against it):
- **Residual, a=0**: with the origin gauge and c_l=1, the exact CLM steady state
  Ω₀(X) = −4X/(1+4X²) nulls R to **RMS 2.2e-7** (discretization-limited), with
  c_ω = −0.99914 (the ~0.09% is the numerical HΩ(0)). This is the same steady
  equation validated by `test_gclm_rescaled.py`.
- **Velocity**: U = ∫₀ˣ HΩ integrates HΩ₀ = 2/(1+4X²) to the closed form
  arctan(2X); bulk (|X|<10) error **8.5e-3**, U(0)=0 exactly. The tail deviation
  is a Hilbert-transform truncation effect *where Ω_X ~ 1/X² → 0*, so it is
  harmless in the advection term a U Ω_X.
- **Parity / a-dependence**: an odd Ω yields an odd R (asymmetry ~1e-13); a≠0
  keeps R finite and **breaks** the a=0 profile — R climbs ≈ linearly in a
  (Fig 16D). That breaking is precisely the effect the transition map measures.

## 3. The search engine

`solver/ga_search.py` is a small, problem-agnostic real-coded GA: uniform box
initialization, tournament selection, BLX-α crossover, annealed Gaussian
mutation, elitism (no scipy; numpy + a seeded Generator, deterministic). It
minimizes an arbitrary `fitness(genome)→float`; it knows nothing about the
physics. The genome→Ω map is a compact parametric family — a GA over hundreds of
raw grid values is just slow gradient descent, so it earns its keep only over a
low-dimensional parameterization that can still represent the anchor exactly:

    odd_rational:  Ω(X) = Σ_k A_k X/(1 + B_k X²)      (one-scale / De-Gregorio type)
    even_lorentz:  Ω(X) = Σ_k A_k /(1 + B_k X²)       (two-scale bump type)

with K=1 `odd_rational` at (A,B)=(−4,4) reproducing Ω₀ exactly.

Engine validation: minimizes a plain quadratic to its known optimum
(f ~ 5e-11) and is bit-for-bit deterministic per seed (`test_ga_generic_engine`).

## 4. The known-answer gate — and a gauge lesson the search surfaced on its own

The gate asks: can the *global* search rediscover the exact steady profile from a
bounded box? It does — but not as the single point (−4,4). Across seeds it lands
on **different** (A,B) that all satisfy the invariant

    A²/B = 4.000    (to 3–4 digits, Fig 16A/C)

because the CLM rescaling gauge is **dilation-invariant**: if Ω(X) is steady so
is Ω(βX) for any β>0 (the equation and the c_l=1, origin-c_ω gauge are both
dilation-invariant; the amplitude is pinned to 1, only β is free). The steady set
is therefore a **1-parameter dilation family** {A=−4β, B=4β²}, and only the
invariant A²/B — equivalently the profile *shape* — is a meaningful "match". This
is the banked "report only gauge-invariants" discipline appearing directly in the
optimization landscape (Fig 16A is a valley, not a basin). Pinning the dilation
(fix B=4) makes the answer unique: the GA recovers A = −3.9999 (Fig 16B, dashed).

This matters for the science ahead: when we sweep `a`, we must read off
gauge-invariant signatures (exponent ratio, scale-separation), never a
gauge-dependent constant — exactly the trap that B1's absolute triple illustrated.

## 5. The discriminating diagnostic (locked before any logged run)

Grounded in HQW25 (arXiv:2401.14615), the two-scale vs one-scale signatures are:

- **D1 — scale separation (primary).** Track the peak *location*
  L_loc ~ (T−t)^{c_s} and peak *width* L_wid ~ (T−t)^{c_l}. **Two-scale ⟺
  L_wid/L_loc → 0** with log-log slope c_l/c_s = 2 (width ~ location²);
  **one-scale ⟺ ratio O(1)**.
- **D2 — blowup power (independent confirm).** Gauge-invariant c_l/c_ω: **−2/3**
  two-scale (c_ω=−3/2), **−1** one-scale. Two-scale blows up *faster* (HQW25's
  weaker-alignment mechanism).
- **Resolution guard (mandatory).** D1 is valid *only while* L_wid spans ≳ 8 grid
  points. Below that → **INCONCLUSIVE / "needs adaptive mesh"**, never "scales
  merged". The two-scale inner width collapses faster than the location, so a
  fixed grid may lose it — the same floor that capped B1/§6.

The transition in `a` is where D1's separation collapses and/or D2 departs −3/2.

## 6. Honest scope and the next brick

The residual (∗) encodes the **one-scale** ansatz; HQW25's **two-scale** object
has a moving frame r(t)(T−t)^{1/2} and the extra exponent c_s, a richer ansatz
**not yet built**. So the exact two-scale anchor Ω₂ (the even Lorentzian bump,
`even_lorentz` provides its symmetry) is not yet a residual-null in this
machinery — only the one-scale anchor is. Building the two-scale residual and
anchoring it on Ω₂ at a=0 is the real next brick and where the difficulty lives.

**What this session earned:** a validated, gauge-aware global-search framework
with an exact a=0 one-scale gate, a generic Route-D-reusable GA engine, and a
locked diagnostic — the tooling for the transition probe, honestly short of the
probe's first scientific result. Overall Clay odds unchanged (~0.05%); this is
toy-model infrastructure, and the lottery ticket still lives in the sweep to come.
