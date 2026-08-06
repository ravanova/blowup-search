# Leg 88 — Route-GCA: adversarial audit of `solver/gclm_family.py`

Branch `leg/gca-v1`. Claim-bearing, standard difficulty. Sixth of the adversarial-audit family
(legs 69, 79, 80, 83, 85), applied to a module none of them had touched.

## Gate, verbatim

> "Under an adversarial battery (NaN/Inf-poisoned `c_l`/`c_omega`, `a` far outside `[0,1]`), does
> `solver/gclm_family.py`'s residual computation ever silently return a finite, plausible-looking
> value instead of propagating the invalid input or flagging it?"

**Answer: NO.** 0 silent corruptions in 37 gate-scoped cases. Confirmed robust → battery banked as
a permanent regression test, lands normally on main. `solver/gclm_family.py` edited under no
outcome, as required.

## Ban check

Ran `plan_of_record.py` first. The live ban is "another gCLM measurement leg". This leg produces no
profile, no `a`-sweep, no self-similar exponent and no blow-up claim — it measures the *code's*
response to malformed input. That is the robustness-vs-measurement distinction that cleared legs 83
and 85, confirmed here independently rather than inherited. The `capabilities.py` grep ban is
discharged: `capabilities.py:64-68` registers the module with `test_gclm_family.py` as its only
validation, and no adversarial capability exists to reuse. Novelty pass committed before
construction (`writeup/novelty/leg_88.md`, commit `b4a0975`).

## What was built

| file | role |
|---|---|
| `experiments/p2_route_gca_v1_adversarial.py` | the battery runner (8 families), 11.8 s |
| `writeup/data/p2_route_gca_v1_adversarial.json` | curated data, all magnitudes |
| `test_gclm_family_adversarial.py` | permanent regression test, 13 tests, self-running (repo convention: no pytest) |
| `writeup/novelty/leg_88.md` | novelty pass + findings |

## Headline magnitudes

- Every NaN/±Inf in `c_l`, `c_omega`, `c_tw`, `a` reached **100.0%** of 401 residual nodes and gave
  a non-finite scalar norm. All 9 joint `c_l`×`c_omega` pairs propagate; **+Inf/−Inf does not
  cancel** to a finite value.
- `a` nine decades outside [0,1] (|a| = 1e1…1e9, both signs): matches an **independent
  recomputation** of the documented formula to **1.96e-16** relative.
- No saturation: `||R||/|a|` → `k = 0.2768551` with deviation decaying as **1/|a|** (dev×|a| held
  at 8.0697e-07 across six decades). A clamp would make that product grow.
- `a = 1e300` overflows to `inf` — honest, not a plausible finite number.
- All 4 malformed-shape adversaries **raise**. A per-node `c_l` array with one NaN poisons
  **exactly 1** of 401 nodes: neither spreads nor vanishes.
- Baseline: one-scale anchor RMS **7.347e-07**, two-scale RMS **1.229e-07**, `c_tw = 0.500000`.

## The mistake I made, and what it cost

The magnitude branch was first pre-registered as "departs from a pure linear law `||R|| = |a|·k` by
>1e-9 relative". First run: **2 of 8 cases flagged, `GATE: yes`**. Rather than report an escalation,
I checked the failure's *shape* — the deviation fell 8.07e-08 → 8.88e-16 as |a| ran 1e1→1e9, i.e.
exactly 1/|a|, which is the additive O(1) stretching/dilation term, not a clamp (a clamp's deviation
grows). The criterion was mine and it was wrong. Replaced with agreement against an independent
reassembly of the documented formula: strictly stronger (401 nodes vs one scalar asymptote, and it
covers the whole battery). Both the original criterion and the reason for its replacement are
recorded in the runner docstring and the findings — the near-miss is the kind of thing that should
be visible, since a less careful pass would have escalated a false positive with maximum urgency.

## Two caveats, neither the gated question — flagged, not patched

1. **`gauge_c_tw` returns a finite `0.0` on a NaN-poisoned profile.** The three
   `if denom > 0 else 0.0` guards (lines 190/204/233) compare `False` on a NaN denominator. Not the
   gate: profile poisoning is not the gated input class, and the accompanying residual is still
   100% non-finite, so nothing downstream sees a clean residual. Pinned in the test.

2. **`residual_two_scale_relnorm` loses its advertised scale-invariance below |Ω| ~ 1e-15.**
   The `max(scale, 1e-30)` floor (line 236) stops the denominator tracking ε² while the numerator
   keeps falling. Invariance exact to ε=1e-14; ratio **1.179e-01** at ε=1e-15; **exactly 0.0** by
   ε=1e-78 — a perfect "exact traveling wave" score from a garbage amplitude, which is exactly the
   trivial-null cheat the docstring says the normalization prevents. **Latent, not active**: GA
   genome amplitudes are O(1), many decades above the break. No GA run was done to check drift —
   that would be a gCLM measurement, which this leg is banned from. This is the one item worth an
   orchestrator's attention; it belongs to whoever next owns the GA fitness, not to this leg.

## Test quality

Mutation-checked, so the suite is not vacuous: injecting a `nan_to_num` swallow into
`GCLMResidual.residual` is caught by 2 tests; clipping `a` into [0,1] is caught by 3. A live anchor
check guards against the suite passing because the anchors went dead.

## Reading

`solver/gclm_family.py` has no validation layer at all — and on the gated question it does not need
one, because pure float64 arithmetic with no defensive fallbacks propagates poison faithfully by
construction. The exposure in this module is not where a validation layer would go; it is the two
places someone *did* write a fallback (`denom > 0 else 0.0`, `max(scale, 1e-30)`). That is the
transferable lesson for the remaining audit legs: the silent-corruption risk concentrates in the
defensive code, not in the bare arithmetic.
