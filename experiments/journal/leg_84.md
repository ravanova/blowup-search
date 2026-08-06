# Leg 84 — Route-TNA: does `target_norm.py` signal a domain violation, or return a number?

**Agent:** LEG-E. **Branch:** `leg/tna-v1`. **Date:** 2026-08-06. **Claim-bearing.**
**Gate answer: YES (SILENT).**

## The gate, verbatim

> Under adversarial inputs that push sample points beyond the validated X_max = 745 window
> (or otherwise into the region capabilities.py already flags as untrustworthy), does
> `target_norm.py` silently return a result with no warning or flag, or does it correctly
> signal the domain violation?

## Order of work

1. `plan_of_record.py` run first; no ban fires on this leg (see `writeup/novelty/leg_84.md`
   §5). The live ban *"building a solver without grepping capabilities.py for the object
   first"* was honoured — the `solver/target_norm.py` entry is quoted in the runner's
   module docstring and is the sentence the whole leg is aimed at.
2. Novelty pass written and **committed before construction** (`0fb7170`).
3. Battery: `experiments/p2_route_tna_v1_domain_audit.py` → curated
   `writeup/data/p2_route_tna_v1_domain_audit.json`.
4. Permanent regression test: `test_target_norm_adversarial.py`, **12/12 gates pass**.
5. `solver/target_norm.py` **not modified** — the yes-branch forbids patching under this
   leg's own authority.

## Method

Every probe runs on `calibration_family(X, alpha=0.4)`, whose exponent is `p = 1 + alpha =
1.4` *exactly* (the module's own known-answer curve), so every silently-returned answer is
scored against a truth and reported as a magnitude. `alpha = 0.4` was chosen because the
target's own measured exponent is 1.3937, so the probes sit at the target's difficulty.
All three signalling channels are checked: exceptions, `warnings.catch_warnings(record=True)`
with `simplefilter("always")`, and enumeration of every returned dict's keys against 12
violation-name stems.

## Numbers

| quantity | value |
|---|---|
| ladder rungs putting samples outside the data | 6 of 7 (`X_max = 13.6 .. 5.5e+03`) |
| of those, raising or warning | **0** |
| max fraction of theta-samples outside the data | 4.66% |
| domain hazards returning a number silently | **8 of 8** |
| argument hazards raising `ValueError` | **4 of 4** (the positive control) |
| samples outside the data at the shipped `X_max = 745.2` | 14 of 16384 (0.085%) |
| `p` at 745 by closure: power / clamp / zero | 1.4039 / 1.5654 / 1.1488 |
| closure spread in `p` at 745 | **0.4166** (worst error vs 1.4: **0.2512**) |
| same, with the exactly-correct power closure | error **0.0039** (control) |
| exponent-/norm-bearing surfaces carrying a domain field | **0 of 6** |
| keys shared between `spectrum`'s dict and `fit_exponent`'s | **0** |
| width in `s` of the silent FINITE-vs-DIVERGENT flip | **0.1616** |
| literal `745` in the module: prose / executable code | 2 / **0** |

## What it means

The module has exactly one domain diagnostic — `n_outside_grid`, a raw count returned by
`compactify` and `spectrum` — and it is real and works (14 at the shipped domain, 0 at the
headline). It is compared by the module against no threshold, it is documented nowhere in
the module's signatures as a trust signal, and it propagates nowhere: `fit_exponent`,
`analytic_tail`, `norm_verdict` and `weighted_partial_sums` share zero keys with it. So a
caller who obtains `p` has no in-band way to learn which domain it came from, and the
consequence is not hypothetical: over a window of width 0.1616 in the weight exponent `s`,
the untrustworthy domain reports the target's norm FINITE where the headline domain reports
it DIVERGENT — a verdict about membership in the certificate's space, from a number
`capabilities.py` calls untrustworthy, with no signal attached.

The four `ValueError`s the module does raise are all about argument shape. The guard surface
is entirely argument-shaped and contains nothing domain-shaped, which matches the structural
finding that no executable constant in the module encodes the window at all.

## Honesty notes

* The exponent shift at the shipped domain is **leg 55's** measurement. This leg re-runs it
  on a calibration object only to give the audit a truth value, and claims none of it.
* The kind case is banked next to the harsh one: with the exactly-right closure the same
  domain violation costs 0.0039 in `p`. The damage is the closure *choice*, which a caller
  cannot make correctly without precisely the knowledge the window is defined by.
* `warnings.warn` appears in **0 of 43** solver modules, so "no warning is emitted" is not a
  deviation from a repo idiom — the repo has no warning idiom. The finding is stated as
  "no threshold, and no propagation", not as "no warning".
* No domain was extended and no gap was closed; `X_max` is varied only as the adversarial
  knob.

## Disposition

Escalated to the orchestrator per the gate's yes-branch, **not patched**. Branch pushed;
not merged to main under this leg's authority. `test_target_norm_adversarial.py` gates 1–4
and 6–11 pin the current silence on purpose and **should fail the day a domain guard lands**
— the correct response then is to invert them, not weaken them.
