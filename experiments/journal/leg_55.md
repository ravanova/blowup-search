# Leg 55 — Route-NB v1. Journal.

**Branch `leg/nb-v1`. Exploration route, not critical path. Gate answered `yes`.**

Integration-owned ledgers untouched: `experiments/JOURNAL.md`, `LITERATURE_CHECK.md`,
`plan_of_record.py`, `CONTINUATION_PROMPT.md`, `PHASE2_P2_NOTES.md`. This file and
`writeup/novelty/leg_55.md` are where this leg writes.

---

## What the leg was for

Legs 51–53 measured everything on the `a = 0` CLM anchor. A live ban asserted of the real
target that it *"does not have finite norm in the class where the operator is least bad"*.
That clause had never been computed — it was
`spectral_certificate.coefficient_decay_exponent`'s docstring derivation applied to an `α`
read off a solve. This leg measures it.

**Result: `p = 1.3937` (headline domain) / `1.3963` (largest domain), against the predicted
`1 + α`. Norm FINITE at `s = 0` and `s = 0.3`; DIVERGENT at `s = 1`. Window empty by
`+0.603`.**

## Order of work (novelty pass really was first)

1. `plan_of_record.py`, `CONTINUATION_PROMPT.md`. `DIRECTION.md` in this worktree is still
   the SEED — **there is no `### 55` entry to read**; the condensed thesis and the
   verbatim gate came from the spawn prompt. Recorded because the assignment said to read
   an entry that does not exist in the tree.
2. Grepped `capabilities.py` for the object before building anything — **but only did half
   of that instruction.** I read the index and then never appended my own entry, so
   `test_capabilities.py` failed at the merge gate with
   `solver modules with no capability entry: ['solver/target_norm.py']`. Caught by the
   coordinator, not by me: I ran my own gates and the neighbouring ones and never ran the
   repo's drift detector. **The rule is grep AND register** — the index is what stops the
   next leg rebuilding this, which is the whole reason the file exists (leg 45). Entry
   appended at the end of the certificate section, append-only, 29 insertions / 0
   deletions, no existing entry reordered.
3. **NB-0 novelty pass, committed before any construction** (`95dc055`), six queries with
   links. Verdict `PROCEED`. Leg 52's search-index flag explicitly NOT touched.
4. Built `solver/target_norm.py`, then the gates, then the runner.

## Findings, in the order they landed

**The prediction is right, but not at the shipped domain.** At `X_max = 745` the exponent
measures `1.369`, not `1.394`. The resolution ladder `n = 201/401/801` is flat (drift
`3.8e-04`), so it is not a resolution effect. The **domain** ladder is what moves:
`(p−1) − α` runs `−0.0243 → −0.0086 → −0.0036 → −0.0015` as `X_max` goes `745 → 3.0e+05`.
The profile has simply not reached its asymptotic tail by `X = 745`. Three independent
measurements (Fourier fit, physical-space log-log fit, ratio of Newton unknowns) converge
together — the `k^{−1−α}` law is confirmed to `1.5e-03` rather than assumed.

**The shipped domain cannot answer this question at all.** The far-field closure ablation
*decides* there: power/clamp/zero give `1.369 / 1.423 / 1.233`, spread **0.190**. 14 sample
points of an `M = 16384` transform fall outside `|X| ≤ 745`. The headline is measured at
`X_max = 4.1e+04`, where **zero** points fall outside and no closure is consulted.

**The instrument was wrong twice and a control caught it both times — not a test.** See
below; this is the part of the leg I would want a reviewer to look at first.

## Three things that went wrong, kept visible

**(a) `fit_exponent` v1 returned `p = −0.06` for a spectrum whose exponent is 2.** Negative
control `1/(1+|X|)` satisfies `h(θ) + h(π−θ) = 1`, annihilating every even mode; the FFT
returns `~1e-18` there and the log-average took logs of them. A `> 0` filter does not catch
`1e-18`. **Caught because the control had a known answer**, and I checked the raw spectrum
(`k²|ĥ_k|` flat at 0.6355–0.6366 for `k ≥ 33`) instead of believing the fit.

**(b) v2 still returned `−0.25`.** Linear means inside log bins fixed the arithmetic; one
sparse bin catching a *single* annihilated mode (`k = 10`, `9.8e-19`) still captured the
least squares. **(c) equal-count bins** then biased the exponent by up to `+0.06` because
their `k`-widths drift along the band. Shipped: log-spaced bins **merged** to ≥ 8 modes,
linear mean inside. Both failures are regression gates 14–15.

**Lesson-90 traps, twice, and both were mine.** The first run reported
`far_field_closure spread = 0.00000` and `interpolation_order spread = 0.00000` and the
evaluation had a predicate `P5_far_field_closure_does_not_decide` reading `true` off them.
Both were vacuous: at `ρ_max = 12` no sample point leaves the grid, so the closure is never
consulted, and the identical numbers were a tautology of the code — exactly leg 53's error.
Fixed by (i) running the closure ablation at **both** domains and reporting
`n_theta_points_outside_grid` and `ablation_fires` on every row, (ii) renaming the predicate
to `P5_headline_needs_no_extrapolation` and adding
`P5b_closure_DOES_decide_at_shipped_domain = 0.190`, and (iii) for the interpolation sweep,
reporting the **movement of the interpolant itself** (`8.7e-05` relative) beside the `3.5e-05`
movement in `p`, so a real null is distinguishable from a dead knob.

**A misleading aggregate, caught before it reached prose.** The interpolation "spread" was
first computed across both `ρ_max` values and read `0.0245` — which is the *domain ladder*,
not interpolation sensitivity. Now taken within a domain (`3.5e-05`).

## Environment notes for whoever runs next

* **There is no `pytest` in this environment** (`.venv` has numpy/matplotlib only, and
  `~/.local/bin/pytest` is broken). The repo convention is a self-running gate script with a
  `gate(name, ok, detail)` helper and `sys.exit(1 if n_fail else 0)`; `test_target_norm.py`
  follows it. I wrote the file in pytest style first and had to convert it.
* **The worktree has no `.venv`** — use `/home/andy/projects/Unsolved/.venv/bin/python`.
* Full runner is ~4 min. `n = 3201` solves are ~2 min each and are not in the runner; the
  `n`-convergence check at `ρ_max = 12` (`p = 1.3937 → 1.3938` over `n = 401 → 3201`) was run
  separately and is quoted in the TECHNICAL as a separate confirmation.

## Scope discipline — the bit I most want reviewed

The gate's yes-branch says the ban clause is *"factually wrong"*. **I do not think that is
the right reading and I did not write it that way.** The clause says "in the class where
the operator is least bad", the operator is least bad at `s = 1`, and at `s = 1` the norm
genuinely diverges (margin `−0.606`). The clause is literally correct. What the leg
actually establishes is that the **object side of the window is now measured** (`s_max =
0.397`), that the target **is** in the space at `s = 0` and `s = 0.3` — the classes legs 52
and 53 actually used — and that the window against the operator's `s = 1` is **empty by
0.603**. Flagged for escalation in the PR body; **no ban edited.**

Corollary worth carrying: "the target was never in the space" is **not** available as an
explanation for legs 52–53. Leg 53's block coupling remains the operative reason.

## Bans respected

No gCLM measurement; no Route-D sharpening; no DSS re-ask; no 2D β; no scaling-gauge
re-test; no GA compute; no new `ℓ¹`-Fourier radii-polynomial machinery for this operator
(this leg builds no certificate and touches no approximate inverse — it measures a
property of the PROFILE); no tuning of `s`, weight family, split or border; no reading of
leg 53's result as a statement about the target. The domain ladder is a **diagnostic on the
exponent**, explicitly not an attempt to close the certificate's truncation gap — leg 47's
`+0.47 decades per unit ρ` finding concerns a different quantity and is not contradicted.

Territory: `solver/target_norm.py`, `test_target_norm.py`,
`experiments/p2_route_nb_v1_targetnorm.py`,
`experiments/p2_route_nb_v1_targetnorm_evidence.py`,
`writeup/4_p2_lottery/BLOG_P2_ROUTENB_V1.md`, `.../TECHNICAL_P2_ROUTENB_V1.md`,
`writeup/data/p2_route_nb_v1_targetnorm.json`,
`writeup/figures/fig50_route_nb_v1_targetnorm.png`, `writeup/novelty/leg_55.md`,
`experiments/journal/leg_55.md`, plus the one-line append to `writeup/build_figures.py`
and the append-only entry in `capabilities.py`.
`solver/spectral_certificate.py` and `solver/bordered_hl.py`: **imported read-only, zero
diff.**

**No link of the L1→L4 chain moved. Clay ~0.05%.**
