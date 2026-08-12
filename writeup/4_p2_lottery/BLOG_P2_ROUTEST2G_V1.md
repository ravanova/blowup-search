# The theorem was in the file. The report never called it.

*Route-ST2G v1 — leg 383. Figure: fig102. Data: `writeup/data/p2_route_st2g_v1.json`.*

## A screen that knew better and said nothing

Hand this repository's DSSP screen a field that looks exactly like the object Tsai's
1998 paper is *about* — `U(y) = A(y/|y|)/|y|`, the headline example in its equation
(1.5), decay exponent exactly −1 — and ask it whether any published theorem excludes it.

On `main` at `104f5b3`, the answer came back: **NOT EXCLUDED**.

That answer is wrong, and the code needed to know it was wrong was sitting in the same
file, forty lines away. Tsai's Theorem 2 excludes that field outright. It does not need
the field to be in any Lebesgue space; it needs only that the field goes to zero at
infinity, which this one does. Leg 359 read the paper at full text and said so back in
August. Leg 362 then wrote the check — `decays_to_zero_at_infinity()` — and wired it in,
and leg 370 added a third theorem on top of it.

So why did the report still say NOT EXCLUDED?

## Because "backward compatible" quietly means "off by default"

Legs 362 and 370 were careful. Each landed its new theorem as an **opt-in argument**,
defaulting to `None`, explicitly so that no existing caller's output shape moved. That
is good engineering discipline, and both legs stated it in their commit messages as a
feature.

The cost was invisible and it landed in exactly one place. `screen_candidate()` is the
single function through which a candidate report is produced — the thing the gate means
when it says "every future candidate report". It looked like this:

```python
    decay = fitted_far_field_decay_exponent(field_fn)      # computed ...
    ...
    ledger = machine_read_ledger(l3, lam)                  # ... then dropped
```

It computed the far-field decay exponent, then threw it away. It never computed the
ansatz classification at all. Two positional arguments, both defaults taken, both new
theorems silently switched off. The functions existed, were tested, were registered as
capabilities — and no report ever reached them.

This is a failure mode worth naming, because nothing in it looks like a bug. Every
individual leg did its job. The tests passed. The capability index was accurate. The
gap lived entirely in the space between "the capability exists" and "the report path
uses it", and it survived two subsequent legs that both touched the same file.

## What this leg did

Made the two columns unconditional. `screen_candidate()` now computes Theorem 2's
decay-to-zero test and the SS/DSS ansatz classification on every call, passes both into
the ledger, and returns them as its own columns. `machine_read_ledger()`'s signature and
defaults are untouched, so legs 362's and 370's compatibility guarantees still hold for
anyone calling it directly — the change is confined to the report path, which is where
the gate lives.

The same planted field now reads **EXCLUDED-BY-T2**, and it says why: Tsai 1998, p.49,
"…U → 0 at infinity in Theorem 2, the usual Liouville theorem implies U_i = 0".

## The half of the battery that has to stay quiet

Six planted controls, written down and committed *before* a line of construction, and
the important thing about them is that **three of them must fail to fire.**

This repository has been burned by an instrument that could only ever say yes (leg 340).
A screen that excludes everything is not a screen; it is a constant function wearing a
theorem's clothes. So:

- a field whose magnitude climbs toward a **non-zero** constant (0.954545 → 0.999500,
  fitted exponent +0.008) must read NOT EXCLUDED — Theorem 2's hypothesis genuinely
  fails on it;
- a field **growing** like |y| (exponent +1.0) must read NOT EXCLUDED with no clause
  claimed at all;
- and the ansatz clause must *not* fire on a static, non-periodic candidate — otherwise
  the headline verdict below would be vacuous.

All three stayed quiet. All four possible verdicts are reachable through the report
path. The instrument can be wrong in both directions, which is the only reason its
being right in one of them means anything.

## The two verdicts the gate asked for

**Tsai's own example is now reached by Theorem 2.** Fitted exponent
−1.0000000000000002 against the source's exact −1 — a difference of 2.2 × 10⁻¹⁶ — with
the L³ ladder genuinely log-divergent, so Theorem 1 does *not* reach it and Theorem 2
does. Verdict moved from NOT EXCLUDED to EXCLUDED-BY-T2.

**This programme's own DSS object is still not reached — for the honest reason.** It
reads NOT-REACHED-BY-ANSATZ, at measured λ = 2.691, and the deciding clause recorded is
Tsai's equation (1.2)₁: the exact, *continuous* self-similar ansatz that both theorems
are stated for. Our object is discretely self-similar — a periodic orbit in log-time, not
a fixed point — so it falls outside the hypothesis of both theorems regardless of how it
decays. Note what this is *not*: it is not the screen saying the object is fine. It is
the screen saying, precisely, that the published theorems do not speak to it, and naming
the sentence in the paper where they stop.

That distinction is the whole point of the leg. Before today, the report path said "NOT
EXCLUDED" for two completely different situations — "no theorem reaches this" and "a
theorem reaches this and I forgot to ask". Those now have different names.

## What this does not buy

Nothing about existence. A candidate that survives this screen has established exactly
one thing: it is not already dead by a published theorem this repository can reach and
has read. That is a filter on wasted effort, not evidence for anything. **Ceiling: Tier
2.** `CLAY_OBLIGATIONS.md` §6's two no-method obligations remain open, untouched by this
leg. The Clay odds stay ~0.05%.

And one thing was deliberately left undone. Leg 382 landed a *certified*,
interval-arithmetic far-field decay enclosure the day before this leg ran. It would be
the natural thing to plug into the Theorem 2 column — a rigorous exponent instead of a
least-squares fit. It was read and left out, on purpose: this gate asks whether the
screen *classifies* correctly, and swapping the estimator mid-leg would have moved the
numbers underneath the very controls that were pre-registered to test the classification.
The fitted column stays. A certified second column is a successor's leg, and it is
written down as such.
