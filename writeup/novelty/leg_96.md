# Leg 96 novelty pass — Route-LHA: adversarial audit of `solver/line_hilbert.py`

Run BEFORE construction, per the leg contract. Pass date: 2026-08-06.

## Question being claimed

> "Under an adversarial battery of near-degenerate non-uniform grids (near-duplicate points,
> extreme local stretching ratios), does `solver/line_hilbert.py`'s dense operator or its cached
> `slope_matrix` ever silently return a finite, plausible-looking wrong result instead of
> propagating or flagging the ill-conditioning?"

## In-repo prior art

| source | what it covers | overlap with leg 96 |
|---|---|---|
| `test_line_hilbert.py` (7 tests) | `d/dx sin` slopes on a sinh grid; `A`/`B` special values and a direct-quadrature cross-check; the CLM known-answer pair (rel 1.6e-4); a resolution ladder; matrix reuse; `slope_matrix` vs the Thomas sweeps (2.7e-13) | none. Every grid in the file is a smooth `sinh`-stretched or uniform mesh, i.e. bounded, monotone, gently graded. Grep over the file for `nan`, `inf`, `duplicate`, `adversarial`, `cond`: **zero hits**. No malformed, repeated, or violently graded grid is ever constructed. |
| leg 75 (Route-M, `slope_matrix`) | built and benchmarked the cached dense slope operator; 10x on the Scenario-2 step | **speed only.** Its exactness claim is an association-change claim on the *same well-behaved sinh grids*, not a conditioning claim. |
| `solver/hl_rescaled.py`, `solver/gclm_rescaled.py`, `solver/gclm_family.py`, `solver/bordered_hl.py`, `solver/interval_certificate.py`, `solver/weight_search.py` | six downstream consumers, all of which build their grid with the same monotone `sinh` stretch | consumers, not audits. None validates the grid it hands in; none checks `line_hilbert_matrix` for conditioning. |
| legs 69 / 79 / 80 / 83 / 85 / 88 / 89 / 91 / 92 | adversarial audits of other modules (`interval.py`, `bordered_hl.py`, `gclm_family.py`, …) | same *pattern*, different module. Leg 69's found a real gap; leg 88's answered NO over 37 cases. Precedent for the method and for the robustness-vs-measurement ban ruling below. |
| `test_bordered_hl_adversarial.py`, `test_gclm_family_adversarial.py`, `test_target_norm_adversarial.py` | the adversarial batteries already on main | different objects. **No file in the repository ever hands `line_hilbert_matrix` or `natural_spline_slopes` a non-monotone, repeated, or extremely graded grid.** |

The question is unasked in this repository. The gap is sharper than a generic "untested path"
because `capabilities.py:57-62` registers the module's `holds` as "spline-analytic H on a
**NON-uniform** grid" — non-uniformity is an advertised capability, and the advertised capability
is the one with untested degenerate cases.

## Capabilities grep (ban 10, discharged)

`grep -n -i "hilbert" capabilities.py` → `capabilities.py:57` registers
`solver/line_hilbert.py`, object "Hilbert transform on the whole line", `holds` as quoted above,
`validated` "the CLM known-answer pair to rel 1.6e-4; the cached slope operator matches the Thomas
sweeps to 2.7e-13", `test: test_line_hilbert.py`. Also present: `solver/hilbert_holder.py`
(weighted-Hölder *bound*, not a discrete operator) and `solver/hilbert_pointwise.py` (pointwise
`|H(h)|` bound, "no known-answer gate; sampled"). Neither is a discrete non-uniform-grid Hilbert
transform and neither registers a grid-validation or conditioning capability. **Nothing to reuse;
nothing to rebuild.** This leg builds no solver — it builds a battery around an existing one.

## Ban check (`plan_of_record.py`, printed 2026-08-06)

All ten live bans read against this leg:

- *another gCLM measurement leg* — not engaged. This leg produces no profile, no `a`-sweep, no
  self-similar exponent, and makes no claim about the gCLM model. It measures a **numerical
  linear-algebra property of a transform routine** on synthetic grids. Same
  robustness-vs-measurement distinction that cleared legs 83, 85, 88; verified here independently
  rather than inherited. The one physics object that appears — the CLM pair
  `f = -4X/(1+4X²) → H(f) = 2/(1+4X²)` — appears only as a **known answer to score the code
  against**, exactly as `test_line_hilbert.py` already uses it.
- *Route-D bound-sharpening*, *DSS re-ask*, *2D beta*, *scaling gauge*, *GA on unvalidated
  fitness*, *the four leg-51/53 reading bans*, *Chen-Hou as target* — none touches a discrete
  Hilbert operator's grid conditioning.
- *building a solver without grepping `capabilities.py`* — discharged above.

## External literature

The claim is about **this repository's discretization**, not about mathematics. The underlying
analytic content — the C¹₀ Hermite basis with closed-form bounded Hilbert transforms — is
Appendix C.1 of Huang–Tong–Wang arXiv:2603.25104, already cited in the module docstring and
already resolved by the repository. This leg does not extend, contest, or re-derive it: A(s), B(s)
and the diagonal limits are taken as given and are the *reference*, not the claim. What is being
measured is whether **this implementation's** finite-precision behaviour degrades loudly or
quietly when the grid violates the implicit well-gradedness assumption that the published method
carries but never states as a hypothesis in the form the code needs it. No arXiv precedence
question arises, for the same reason recorded at leg 88.

One reading note that shapes the design and is worth recording, since it is the difference between
an honest audit and a rigged one: a near-degenerate grid makes the *interpolant itself* a poor
representation of `f`, so a large error there is not automatically a code fault. The battery must
therefore separate (i) error the mathematics forces on any correct implementation from (ii) error
this implementation introduces or hides. That separation is made by scoring **only at nodes far
from the perturbation**, by carrying an unperturbed control grid of the same size, and by asking
whether the returned numbers are *finite and plausible* rather than merely *inaccurate*.

## Verdict

Novel within the repository. Proceed to construction.

---

# Leg 96 findings (written after the run)

*(to be filled after the battery runs)*
