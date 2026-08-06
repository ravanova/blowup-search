# Leg 97 — Route-WSA: adversarial audit of `weight_search.py`'s FitnessEngine

**Agent:** LEG-G. **Branch:** `leg/wsa-v1`. **Date:** 2026-08-06. **Claim-bearing.**
**Gate answer: NO — confirmed robust.** Battery banked as a permanent regression test.

## The gate, verbatim

> Under an adversarial battery (a batch member driving the shared Jacobian toward
> near-singularity, NaN-poisoned weight parameters), does FitnessEngine ever silently
> return a finite, plausible-looking fitness value instead of propagating or flagging the
> ill-conditioning?

**NO.** Over 100+ adversarial cases: 0 silent finite values, 0 certificates accepted that a
higher-precision recomputation would reject, worst flattering of a weight **+2.1e-11
decades** against a pre-committed 0.5-decade threshold.

## Scope, stated before the result

Stage B's / leg 49's / leg 59's frozen gate verdicts are **not** reopened, contested or
re-scored. This leg audits code robustness, not the fitness's scientific viability. The
ban *"any GA compute on an unvalidated fitness"* is respected literally: no GA, no
`grid_search`, no `roster` scoring, no six-property property re-measured — the engine is
called directly on hand-built inputs. `solver/weight_search.py` was READ-ONLY throughout
and is byte-identical to `origin/main`; the two gaps found (below) were **pinned, not
patched**.

## What was measured

Ten gates, `experiments/p2_route_wsa_v1_adversarial.py`, 53 s at `n = 101`; the fast subset
is `test_weight_search_adversarial.py`, 14 gates in 6 s at `n = 81`.

**The thesis's channel does not exist, and that is the first finding.** `J = jacobian(z)`
and `A = inv(J)` take no `theta` argument, so *no batch member can move the shared
Jacobian* — the conditioning hazard enters through the **state**, never through a weight.
Checked rather than asserted: 5 clean weights evaluated beside 4 poisoned ones (NaN gene,
inf gene, `|p| = 1e6`, a 600-decade weight range), in both orderings, deviation **exactly
0.0** — bitwise. The one batching artefact that does exist is benign and separate: `k = 1`
and `k = 6` take different BLAS paths, so summation order shifts a clean answer by **1.0
ulp** (2.2e-16 in `log10` fitness) *with no poison in the batch at all*.

**The conditioning ladder** (interior state scaled by `s`; `J`'s interior block is
homogeneous of degree one, the border rows are not, so `cond(J) ~ 1/s`), 12 rungs:

| cond(J) | 2.7e5 | 2.4e13 | 2.4e15 | 2.4e17 | 2.4e18 | 2.4e19 | ∞ |
|---|---|---|---|---|---|---|---|
| `Z_1` | 1.1e-10 | 4.3e-05 | 1.4e-03 | 3.5e-01 | 1.55 | 381 | — |
| fitness | -5.744 | 15.076 | 17.077 | 19.443 | +inf | +inf | `LinAlgError` |

`Z_1` is **monotone in the conditioning over 13 decades** and crosses 1 at `cond(J) =
2.4e18`. This is the whole robustness mechanism, and it is the module's own comment
(lines 486-495, `Z_1 ~ eps * kappa * range`) checked as a measurement rather than quoted.
The reason it is sound: in Newton–Kantorovich `A` is an *arbitrary* operator, so a garbage
inverse is not an unsound certificate — it is a large defect `‖I − A·DF‖`, and the engine
reports that defect faithfully.

**Faithfully** is the load-bearing word, so it was checked twice. 42 (state, weight) pairs
against a `np.longdouble` recomputation of the **identical** `A` and `J`: max relative
deviation `Z_1` **5.6e-03**, `Y_0` ~1e-16, and **0** finite answers whose true `Z_1 ≥ 1`.
Then the reference itself against **exact rational arithmetic** (`Fraction`; float64 values
are exactly rational, so `I − A J` has no rounding at all): float64 within **1.6e-12**
relative of exact at `cond = 1.8e14`, and never a material understatement of the exact
defect. The batched path also agrees with the documented per-theta `certificate_constants`
to **≤ 5.6e-16** relative at every rung, so the shortcut is the same computation, not a
cheaper approximation.

**Poisoned inputs, 32 cases, 0 numbers returned.** 17 poisoned genomes (NaN/±inf in each of
five genes, all five at once, a NaN buried in a legal genome) → `+inf` every time, with the
box on *and* off: the poison reaches `Y_0`/`Z_1` as NaN, `Z1 < 1.0` is false for NaN, and
the budget branch falls to `-1` → `+inf`. Refusal by IEEE-754 semantics rather than by a
check, which is worth knowing but is the correct outcome. 8 poisoned states → 2
`LinAlgError`, 6 `+inf`. 5 extreme-range weights (up to **217 decades** of dynamic range) →
`Z_1` **overflows** to 1e35..1e291 and the engine refuses; **0** underflowed `Z_1` to zero,
which is the one arithmetic outcome that would have made the max-of-products shortcut
dangerous (a `Z_1` of 0 is a certificate that closes for free).

## Two gaps found, pinned not patched (this leg had no patch authority)

1. **`in_box` admits a NaN genome — 7/7.** Its comparisons are `<`/`>`, and every
   comparison against NaN is false (IEEE-754 §5.11), so a NaN genome passes the box. **Not
   a corruption**: `fitness` still returns `+inf` for all of them. Pinned in gate 12, which
   fails the day the box admits NaN *and* the fitness returns a number.
2. **`LOG_NU_CLIP` is a silent weight substitution — but unreachable from inside the box.**
   Where the clip fires, the returned fitness describes a weight the caller did not ask
   for. Over **122473** box-admitted genomes, `max|log ν| = 94.3` against `LOG_NU_CLIP =
   500` — a **5.3x headroom**. Gate 13 guards the headroom, not the number.

Neither is an escalation. Both are recorded here so a future change is noticed rather than
discovered (lesson 68).

## Deliverables

* `experiments/p2_route_wsa_v1_adversarial.py` — the ten-gate battery runner.
* `writeup/data/p2_route_wsa_v1_adversarial.json` — curated magnitudes, every case.
* `test_weight_search_adversarial.py` — 14 permanent regression gates, 6 s.
* `writeup/novelty/leg_97.md` — novelty pass, committed **before** construction.

## What this leg does NOT license

That the weight fitness is scientifically viable (out of scope, frozen elsewhere); that any
weight is good or bad; that `Z_1 < 1` at `cond(J) = 2.4e17` means the *state* is
trustworthy — it means the certificate reported there is a true statement about a badly
conditioned `A`, which is a different and much weaker thing. A caller cannot distinguish
"bad weight" from "bad state" by the fitness alone: both read as a large number. That is a
property of a one-number fitness, not a defect of the engine, and it is stated so nobody
re-derives it as a finding.
