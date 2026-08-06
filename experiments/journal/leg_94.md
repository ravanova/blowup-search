# Leg 94 — Route-TNB v1: the false-positive check on `solver/target_norm.py`'s new domain guard

**Branch** `leg/tnb-v1`. **Exploration leg, light, CLAIM-BEARING** (soundness of a shared module).
**Gate: NO.** The guard is precise — it catches violations without rejecting valid input.
Banked as a permanent regression test alongside leg 84's own battery. Lands normally on `main`.

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read in full. `NG` is NEXT. Every live ban noted; two bind and
   neither bites: *build nothing without grepping `capabilities.py` for the object first*
   — done, the `solver/target_norm.py` entry read in full including the leg-84 domain-guard
   sentences appended to its `validated` line, and quoted verbatim in the runner; *closing
   the truncation gap by extending the domain* — this leg varies `X_max` and `M` only as
   guard probes and extends nothing.
2. `DIRECTION.md` — has a leg 94 entry; thesis and gate read from it and cross-checked
   against the dispatch prompt. They agree verbatim.
3. Prior art read as source, not description: `writeup/novelty/leg_84.md` in full,
   `test_target_norm_adversarial.py` (leg 84's ten silence-pins, inverted after the
   repair), `experiments/bench_target_norm_domain_guard_check.py` and its JSON, and
   `solver/target_norm.py`'s guard in full (docstring §"THE DOMAIN GUARD",
   `TargetNormDomainWarning`, `domain_fields`, `_warn_if_outside`, the `compactify` call
   site, and the `n_outside_grid=` argument on all four downstream surfaces).
4. **Novelty pass FIRST**, committed before any construction (`731659d`,
   `writeup/novelty/leg_94.md`).
5. Then: runner, curated data, permanent regression gates, findings, this note.

## What the novelty pass changed about the leg

It made the gap quantitative and therefore made the leg worth its hour. Before this leg the
guard's false-positive direction rested on **exactly one in-window configuration** —
`rho_max = 12`, `M = 16384`, `far_field='power'`, `alpha = 0.4` — asserted from three
places (the bench A/B's one in-window case, adversarial gates 3 and 9). There were **0**
probes at the `<=` boundary the guard's own comparison hinges on, **0** at any other `M`,
**0** on any profile but the calibration family, and **0** anywhere across the validated
range up to `X_max = 745` that the gate explicitly names. That is what the battery was
aimed at, rather than at re-running the one configuration that was already known clean.

## The one thing that went wrong, and what it taught

The runner's first pass reported **2 false positives** in the boundary block. They were
real firings of the guard on grids I had classified as in-window — and my classifier was
wrong. I had defined the largest theta-sample by the closed form
`X_reach(M) = cot(pi/(2M))`. `tan` is catastrophically ill-conditioned as
`theta/2 -> pi/2`, so at `M = 512` the closed form gives `325.94830079770134` while the
grid's actual largest sample, computed the way `compactify` computes it, is
`325.94830079770776` — a gap of **113 ulp, relative 1.97e-14**. Grids landing inside that
band genuinely do put a sample outside the data. The guard was right; the instrument was
wrong.

Fixing it required care about which direction the fix ran. The temptation was to widen a
tolerance until the two rows went green, which would have made the battery incapable of
detecting the very over-rejection it exists to detect. Instead the criterion is now built
from the module's own grid constructors (`midpoint_theta_grid`, `X_of_theta`) — never from
the guard itself, so it stays independent — and the 113 ulp is **pinned as gate 3** of the
permanent test, with the reasoning in the docstring, so a future maintainer who "simplifies"
it back to the closed form fails the gate and reads why. This is the second time on this
route that the instrument, not the module, was the thing that had to be corrected first.

## Result

163 legitimate in-window probes, 1088 domain-field reads across `spectrum` and all four
downstream surfaces: **0 false positives, 0 warnings, 0 exceptions, 0 numbers changed**.
The `<=` is verified at bit-exact equality (a `<` would have been caught). The threshold is
sharp to **-9.8e-15** relative, where 1 of 512 samples leaves. Negative controls fire 3 of
3 and reproduce leg 84's **14 of 16384** at the shipped domain exactly, so the clean sweep
is a measurement of precision and not of a disabled guard.

Banked context, explicitly not a claim: staying in-window at `X_max = 745.2` caps `M` at
1024, where the calibration family's exponent is `1.5207` against an exact `1.4` (error
`0.121`, versus `0.743` at `M = 512` and `1.195` at `M = 256`). That is leg 55's own
tension — the trustworthy domain and the resolved exponent pull apart — as a magnitude. It
argues for nothing; in particular it does not argue for widening the domain, which a live
ban forbids.

`solver/target_norm.py` was **not modified**; the diff confirms it.

## Deliverables

* `experiments/p2_route_tnb_v1_postrepair.py` — the battery (B1 ladder, B2 boundary,
  B3 profiles and argument edges, B4 `domain_fields`, B5 invariance, B6 negative controls).
* `writeup/data/p2_route_tnb_v1_postrepair.json` — curated data, verdict computed from the
  counts rather than asserted.
* `test_target_norm_postrepair.py` — 9 permanent gates, 9/9 in 2.3 s. Pins the guard's
  PRECISION; `test_target_norm_adversarial.py` pins its SENSITIVITY. A failure here means
  drift toward over-rejection, and the fix belongs in the module, never in the gate.
* `writeup/novelty/leg_94.md` — the pass (committed first) and the findings.
