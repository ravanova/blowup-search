# Phase-2 P2 — Does HQW25's exact two-scale traveling wave survive gCLM advection? A global GA fixed-point map

**Status: a novel toy-model result (Tier-1/2), NOT a Clay solve.** This note maps
how the Constantin–Lax–Majda (CLM) two-scale self-similar blowup — proved exact by
Huang–Qin–Wang [HQW25], arXiv:2401.14615 — deforms as we turn on advection along
the generalized-CLM (gCLM) `a`-family (a=0 CLM → a=1 De Gregorio). The map is
produced by a **global genetic-algorithm search** over the *two-scale rescaled
residual*, with the predicate locked in git before the logged run. The GA proves
nothing; its worth is the global map plus the profile *guesses* a rigorous
(Route-D) interval-Newton step would later certify.

Rebuild the figure from committed data (no GA re-run):
`python writeup/4_p2_lottery/p2_two_scale_sweep_evidence.py` → `writeup/figures/fig17_two_scale_sweep.png`
(reads `writeup/data/p2_two_scale_sweep.json`; regenerate the data with
`python experiments/p2_two_scale_sweep.py --logged`).

Code: `solver/gclm_family.py`, `solver/ga_search.py`; harness
`experiments/p2_two_scale_sweep.py`; tests `test_gclm_family.py` (11/11; full
suite 7 files green).

---

## 1. The object: a two-scale profile is an exact traveling wave

HQW25 constructs a *two-scale* self-similar blowup of the CLM model
`ω_t = ω H(ω)` of the form

    ω(x,t) = (T−t)^{c_ω} Ω( (x − r(t)(T−t)^{c_s}) / (T−t)^{c_l} ) + o(1),

with **two** spatial scales: the bulk sits at distance `r(t)(T−t)^{c_s}` from the
origin (the *larger*, slower scale, `c_s = 1/2`) while its width shrinks like
`(T−t)^{c_l}` (the *smaller*, faster scale, `c_l = 1`), and `c_ω = −3/2`. Their
key structural result (§2.4) is that the profile Ω is an **exact traveling wave**.

Carrying that moving-frame ansatz through the equation, the leading balance as
`t → T⁻` (order `(T−t)^{−3}`) is a pure traveling-wave equation — the dilation
term `−c_l X Ω_X` and the amplitude term `c_ω Ω` are *subleading* (order
`(T−t)^{−5/2}`) and drop. Including the gCLM advection `a·u·ω_x` (which enters at
the *same* order as the stretching term), the two-scale steady residual is

    R₂(Ω) = Ω H(Ω) − c_tw Ω_X − a U Ω_X,     U(X) = ∫₀ˣ H(Ω) dX',     c_tw = c_s·r.

This is **structurally different** from the one-scale residual used in §9's GA
framework: a pure **translation** `c_tw Ω_X` (constant × derivative), not the
**dilation** `c_l X Ω_X`. `c_tw` is the traveling-wave speed — the gauge/eigen-
parameter, analog of `c_ω`.

**The a=0 anchor.** In HQW25's `a=b=c=1` normalization the exact profile is the
even Lorentzian bump

    Ω₂(X) = −1/(1+X²),     H(Ω₂) = −X/(1+X²),     c_tw = 1/2,

and one checks `Ω₂ H(Ω₂) = ½ Ω₂'` identically. More: *every* single Lorentzian
`A/(1+B X²)` is an exact a=0 traveling wave with speed `c_tw = −A/(2√B)`, so the
a=0 two-scale steady set is a **2-parameter scaling valley** (amplitude and width
are both free by the model's scaling symmetry) — only invariants are physical, the
deeper form of §9's "report gauge-invariants, not gauge values" lesson.

## 2. The known-answer gate (a=0)

The residual is validated exactly as §9's was — against the one answer we have.
On the `c=0.5` sinh grid (n=801), reusing the dense line-Hilbert operator:

- `H(Ω₂)` matches `−X/(1+X²)` to `1×10⁻⁸` in the bulk;
- `R₂(Ω₂)` nulls to **`1.5×10⁻⁹`** (cleaner than the one-scale anchor's `2×10⁻⁷`);
- the least-squares gauge recovers `c_tw = 0.5000000`;
- every tested Lorentzian nulls R₂ with `c_tw = −A/(2√B)` to `~10⁻⁸`.

(Fig17 Panel A; `test_gclm_family.py::test_a0_two_scale_gate`,
`test_two_scale_family_and_a_break`.)

## 3. The fitness must be scale-invariant

The absolute RMS `‖R₂‖` is **not** scale-invariant: scaling Ω → εΩ sends
`R₂ ~ ε²` *and* the gauge speed `c_tw ~ ε → 0`, so a plain-RMS GA cheats by
shrinking the amplitude toward zero (a trivial null with `c_tw ≈ 0`). This
actually surfaced in a pre-run scratch — the GA drove `c_tw → 0` at every `a`. The
correct fitness is the **relative residual**

    relres(Ω) = ‖R₂(Ω)‖ / ‖Ω H(Ω)‖,

the fraction of the stretching term left unaccounted by translation + advection —
invariant under the family's scaling symmetry, `~0` for the exact traveling wave,
`O(1)` for a mismatched profile (e.g. the one-scale Ω₀ scores `>0.1`, not gamed to
zero). (`solver/gclm_family.py::residual_two_scale_relnorm`;
`test_two_scale_relnorm_scale_invariant`.)

## 4. Pre-run robustness scout (why the floor curve is trustworthy)

Before locking the predicate we checked the two variables the verdict hinges on —
these are *not* logged runs, just grounding:

- **Resolution / domain: the floor is physical.** `relres(a)` is invariant across
  `n = 601/801/1201` and `rho_max = 8/10` (a=0.3: `~1.3×10⁻³`; a=0.5: `2.56×10⁻²`
  to three digits; a=1.0: `~1.84×10⁻¹`). The rising floor is **not** a slow-decay
  tail or grid artifact. → `n = 801` chosen (no gain from finer).
- **GA convergence: the floor is the true genome optimum.** 2.5× more GA budget
  barely moves it (a=0.3: `1.38→1.04×10⁻³`; a=1.0: `1.85→1.82×10⁻¹`).

## 5. The logged sweep and the locked predicate

**Config (locked):** `a ∈ {0, 0.1, …, 1.0}` refined to 13 points near the edge;
n=801; genomes `even_lorentz` K=2 (strict two-scale symmetry) and `rational_mixed`
K=2 (even+odd, free to skew) + an even K=3 ladder at `a ∈ {0, 0.3, 0.5, 1.0}`;
fitness = relres; 6 GA seeds/a, best-of; `c_tw` = least-squares speed.

Predicate T1–T6 (scale-/gauge-invariant observables), verdict **descriptive
(PARTIAL by construction)**, no clause-chasing. **Result: 5/6.**

| # | Clause | Outcome |
|---|--------|---------|
| **T1** | a=0 both genomes `relres < 1e-4` | **PASS** (5.8e-8 / 3.4e-7) |
| **T2** | persistence window `a ≤ a_p`, `relres < 1e-2` | **PASS**, `a_p = 0.40` |
| **T3** | monotone rise, `relres > 5e-2` by a=1 | **PASS** (`1.8e-1`) |
| **T4** | *genuine, not genome-limited* (K=3 ≥ ⅓·K=2) | **FAIL** — genome-limited |
| **T5** | symmetry preserved, odd-fraction `< 0.05` ∀a | **PASS** (max `0.013`) |
| **T6** | resolution guard, width `> 8` pts in verdict window | **PASS** (min 49 pts) |

## 6. What the map says (honestly)

**HQW25's exact a=0 two-scale traveling wave deforms _smoothly_ under advection —
there is no sharp collapse at a critical `a*`.** (Fig17 Panel B.) The scale-
invariant residual floor is machine-zero at a=0, stays `< 10⁻²` out to `a_p ≈ 0.4`
(a deformed-but-present traveling two-scale profile), then rises monotonically to
`≈ 0.18` at a=1 (De Gregorio). The profile **stays even** the whole way — the
mixed genome, free to skew, keeps odd-fraction `< 0.013` (Panel D), so the
mechanism weakens by residual-floor rise, **not** by symmetry-breaking. Advection
also **selects a finite scale**, lifting the a=0 two-parameter scaling valley (the
selected width drops from ~220 grid pts at a=0 to a definite `O(50–140)` for `a>0`;
Panel D).

**The honest failure (T4) is the real headline.** At intermediate `a` the floor is
partly **genome-limited**: a richer even K=3 ansatz cuts the a=0.5 floor **4×**
(`2.45×10⁻² → 5.6×10⁻³`, back below the persistence threshold). So the K=2 floor
curve is a **genome-relative upper bound**, and the precise survival boundary is
*not* pinned by this map — a richer ansatz pushes persistence further out. This is
exactly the pre-committed INCONCLUSIVE branch, reported not hidden: **sharpening
the mid-range needs a richer basis or a rigorous (Route-D)/adaptive step.**
Crucially, at **a=1 the K=3 genome does _not_ rescue** the floor
(`1.83×10⁻¹ → 1.43×10⁻¹`, still large) — so the De Gregorio-end degradation is
robust to genome enrichment, while the middle is not.

## 7. Scope: what this is and isn't

New, to our knowledge: nobody has mapped how CLM's proven two-scale traveling wave
behaves under gCLM advection. It uses HQW25's exact anchor and the §9 GA
machinery. But:

- a GA minimizing a residual **proves nothing** — this is Tier-1/2 evidence, not a
  Tier-3 proof;
- the map is **genome-relative** (T4) — an upper bound on the true residual;
- the value toward the roadmap is (i) the global picture and (ii) the a=0 exact
  and near-CLM deformed profiles as **certifiable guesses** for a later interval-
  Newton (Route-D) step, plus the reusable two-scale residual object.

The genuine next questions: a richer/spectral genome to sharpen `a_p`; and the
separate coupled-system leg (whether an HL-type two-stage appears — HL is not a
scalar gCLM member). Neither changes the ceiling: **novel toy-model research, not
a Clay solve.**
