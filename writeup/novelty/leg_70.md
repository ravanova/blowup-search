# Leg 70 (Route-RC) — novelty pass: the realization audit of `solver/rescaled_spectrum.py`

Run BEFORE the audit, as the leg contract requires. This leg is a labeling correction on
numbers already on file, so the pass has two jobs: (1) establish that the *observation* being
applied is not being claimed as ours, and (2) establish whether the one thing the audit adds
that is not already written down — the K-scaling arithmetic — is itself novel. Both answers
are **no novelty claimed**, and the pass is recorded so that no later leg mistakes this
correction for a discovery.

## 1. The dichotomy being applied is Xu's, and it is already banked

The statement "a spectrum is not a property of a differential expression until you name the
realization, and for this operator the maximal `L²` realization and the origin-`H²`
realization differ by the whole open strip" is **arXiv:2607.19762 Proposition 2** (Xu).

It is already in this repository in five places, none of them written by this leg:

| where | what it already says |
|---|---|
| `PHASE2_P2_NOTES.md` J-4 (line ~2370) | full statement of the dichotomy; "**OUR DISCRETIZATION HAS NO ORIGIN CONDITION**"; names re-running I5 as top-ranked correction |
| `LITERATURE_CHECK.md` item 4 (line ~149) | same, in the literature ledger's own words |
| `writeup/README.md` (lines ~380–383) | same, as a correction note |
| `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEJ_V1.md` (~336, ~371) | same, as Route-J's forward consequence |
| `solver/literature_gates.py` (~57, ~504) | same, as a machine-checked gate row |

**So this leg claims zero novelty for the dichotomy, for its application to gCLM, or for the
observation that our grid lacks an origin condition.** All four were established by the
Route-J primary-source pass (2026-08-04). What was *not* done then is the thing this leg does:
read the discretization source and confirm the claim from the code rather than from the paper,
and check whether every site that quotes the count actually carries the disclosure.

**Consequence for the gate's yes-branch:** the yes-branch would require J-4 to be wrong. The
audit below does not find that (see §2 of `experiments/journal/leg_70.md`), so J-4 stands and
no correction to it is reported.

## 2. Prior art on the one piece of arithmetic this leg adds

The audit's only new *reasoning* is that the banked counts scale as `K − 3`:

| K | banked unstable count | `K − 3` | unstable fraction |
|---|---|---|---|
| 48 | 45 | 45 | 0.9375 |
| 96 | 93 | 93 | 0.96875 |
| 144 | 141 | 141 | 0.979166… |

The count is **exactly** `K − 3` at all three resolutions and the fraction **rises** with `K`;
it does not saturate. That is a dimension-proportional count, which is the standard signature
of a discretized *continuous* spectrum rather than a finite-dimensional unstable manifold.

This inference is textbook and is **not claimed as novel**:

- **Spectral pollution / discretized essential spectrum.** That finite sections of an operator
  with non-empty essential spectrum produce eigenvalue counts growing with the truncation
  dimension, and that these are not eigenvalues of the operator, is standard — Davies & Plum,
  *Spectral pollution* (IMA J. Numer. Anal. 24 (2004) 417–438); Trefethen & Embree,
  *Spectra and Pseudospectra* (2005), ch. on finite sections.
- **The module already says it.** `solver/rescaled_spectrum.py`'s own docstring (lines ~110–119)
  states that the continuum is "the part that never does [stop moving under refinement]" and
  that "THAT IS WHY A CONVERGENCE FILTER IS MANDATORY". The `K − 3` arithmetic is that same
  sentence read quantitatively off numbers that were already banked, not a new fact about the
  operator.
- **Nothing was recomputed.** The three rows above are lifted verbatim from
  `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEI_V1.md` §1's table. The only operation performed on
  them is subtraction and division. No solve, no eigenproblem, no gCLM measurement — the
  leg-42 ban is untouched.

## 3. What this leg is therefore permitted to say

Only this: *the code confirms, from the source, what J-4 asserted from the paper; and of the
ten places the count is quoted, N carry the realization disclosure and M do not.* That is a
bookkeeping statement about our own documents. It upgrades no claim, moves no link of the
L1→L4 chain, and adds no number to the record.

## 4. Searched-and-not-found

One thing was looked for and not found, recorded so a later leg does not re-search it: **no
published origin-`H²` unstable-direction count for the gCLM rescaled fixed point at `a = 1/2`.**
Xu's Proposition 2 gives the dichotomy and states the origin-`H²` strip is empty apart from
`{0, 1}`, but does not publish a Morse index for the `a = 1/2` rescaled fixed point that our
`K − 3` count could be checked against. So the corrected label is "the maximal `L²`
realization's essential spectrum, as a count, at `K = 144`" — and there is no external number
to compare it to in either realization. That is the honest ceiling on the corrected statement.
