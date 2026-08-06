# The search space was never big enough to matter

*Route-BX, leg 126. Companion to `TECHNICAL_P2_ROUTEBX_V1.md`. Data:
`writeup/data/p2_route_bx_v1_stageb.json`. No figure, by design — this leg measures no new
corner, and the repository's convention is that an audit that measures nothing registers
nothing.*

---

There is a particular way a research plan dies, and it is worth writing down because it does
not look like failure from the inside.

Two years of legs ago — well, 125 legs ago — this project committed to a sequence of stages.
The last one, stage `B`, was the optimistic one. Its name was *"evolve the certificate — the
function space, the operator split, the constants"*, and its argument was genuinely good:

> The bottleneck has not been finding the object; it has been closing a certificate around an
> object we already have. Route-D hand-tuned a function space for eleven legs. Routes K and L
> hand-picked preconditioners. **Those are search problems with a fitness that cannot lie** —
> "does the radii polynomial close, and by how much" is a theorem, not a plot, and an
> under-resolved run cannot fake it.

That is a real insight. Hand-tuning is exactly the kind of labour a search should eat. And the
fitness really cannot lie: unlike most machine-learning objectives, this one is a quantity that
either goes below 1 or does not, and no amount of overfitting makes a false certificate true.

So why was stage `B` never run?

## Because every degree of freedom it was going to search got measured dead first

Not by stage `B`. By the eight legs that ran while `B` sat in the queue, each of which was
aimed at something else and each of which happened to close one of `B`'s doors on the way past.

- **The function space.** Leg 52 found the weight exponent's repair works at `s = 0` and `0.3`
  and fails at `s = 1` and `1.5`. Leg 55 measured the target's own norm and found it finite
  only below `s ≈ 0.394`.
- **The operator split.** Leg 53 found the coupling entry is `K/2` for *every* choice of split,
  and the sweep `K = 4…64` bottoms at the smallest `K` with `43.15`.
- **The shape of the approximate inverse.** Leg 54 spent seven shapes and got a `1.167×`
  improvement where more than `8×` was needed. Leg 58 turned the relevant half of that into a
  **theorem**.
- **The fitness that would have steered the search.** Legs 49 and 59 ran a frozen six-property
  viability gate on it. It failed both times.
- **And the realizations.** Leg 56 killed the collocation one. Leg 111 killed the weighted-`L²`
  energy one.

Any one of those is a setback. All of them together is something else, and the honest question
is no longer "can we run stage `B`" but "**is there anything left in stage `B` to run**".

That question has an answer, and this leg's whole job was to get it. Not by arguing. By
enumerating.

## What an audit is, when done properly

The temptation here is to write a paragraph saying "we looked and there's nothing left" and
move on. That paragraph is worthless, because it is unfalsifiable and because it is exactly
what a tired researcher writes whether or not it is true.

So instead: write down stage `B`'s declared search space as a set of **axes**, before checking
anything. Write down each banked refutation as a **clause** with a predicate saying which
configurations it covers. Take the product. Ask, mechanically, of every configuration: which
clause covers you?

**1,686 configurations. Zero uncovered.**

The breakdown matters more than the total, because not all coverage is the same kind of thing:

| coverage | count | what it means |
|---|---|---|
| **THEOREM** | 144 | proved; the configuration cannot close, as mathematics |
| **STRUCTURAL** | 1,032 | not a legal certificate at all — the target isn't in its own space, or the finite block is singular |
| **MEASURED** | 510 | tried, didn't close. Coverage, but not proof |

## The part where I nearly fooled myself

A covering predicate that always returns "covered" would produce exactly the table above, and
it would be worthless. This repository has a standing lesson about precisely that failure —
*a control that cannot come out differently is not a control* — so the audit has to be fed a
configuration it ought to fail on.

The natural one: turn on dissipation. Every banked refutation here is about the **inviscid**
operator. With `μ > 0` a certificate demonstrably *does* close — leg 58 measured `Z₁ = 0.174`.
So the audit was pointed at the dissipative operator and required to answer **NOT COVERED**.

It answered "covered". The predicate was a tautology, and I'd have shipped it.

The bug was that not one of my twelve clauses mentioned `μ` at all. Every clause silently
claimed authority over an operator its evidence had never seen. Scoping all twelve to `μ = 0`
— which is just writing down what they actually measured — fixed it, and now the control
reports NOT COVERED on all eight dissipative configurations while all four inviscid ones come
back covered.

There was a second, more embarrassing version of the same lesson. My first dissipative control
returned `Z₁ = 5904` where leg 58 banked `0.174` — off by a factor of 34,000. The instinct is
to distrust the banked number. The correct instinct, which this repository also has written
down, is to **suspect your own control's realization first**: I had bordered the dissipative
operator with the far-field direction, exactly as the inviscid one is bordered. But a
dissipative tail is already invertible — it has no far-field kernel to border. I was measuring
the wrong operator. Built the way leg 58 built it, the control now reproduces its entire
twelve-entry dial to `1.25e-15`.

## The number stage `B` actually owed

`B`'s pre-committed no-branch does not just ask for a "no". It asks for something specific:

> A negative bounds **how much of the difficulty was tuning versus structure**, which is worth
> knowing either way.

Here is that number. The requirement is multiplicative — the certificate closes iff `Z₁ < 1` —
so the natural scale is decades of `log₁₀ Z₁`, on which every improvement factor is a
subtraction. From the block-diagonal baseline of `10.4584`, closing needs **1.0195 decades**.

- Tuning — every shape, class, gauge and split the repository ever tried — delivered
  **0.0672 decades**, or **6.59%**.
- The structural floor sits at **0.7812 decades**, or **76.63%**.
- The gap between them, **16.78%**, is headroom the search genuinely never explored.

Which is the interesting bit, actually: **there was real unexplored search space.** Tuning
reached only 28.2% of its own ceiling. Stage `B` was not proposing to search an empty box.

It just wouldn't have mattered. Even a **perfect** search — one that saturated every decade of
available headroom — lands at `Z₁ ≥ 6.0424`, still **6.04× short** of closing.

And on the class where leg 58 has a theorem rather than a battery, the accounting collapses
entirely: the proved floor is `Z₁ ≥ 1` and the requirement is `Z₁ < 1`. The searchable headroom
is exactly **zero** decades. Structure owns **100%**.

## What's left, and what it isn't

One honest gap remains, and it is worth being precise about its shape. Leg 58's theorem covers
approximate inverses with `A₂₁ = 0`. Three admissible shapes have `A₂₁ ≠ 0` — and for those,
the repository has measurements and no theorem.

That is a **proof-strength gap**, not a **coverage gap**, and the audit keeps the two apart on
purpose. The gate asked for a corner where a searched certificate *could still close*. This
isn't one: the best admissible `Z₁` anywhere in that class is `8.9591`, the general-`A` floor on
the kernel direction is `5.0444`, `A₂₁ ≠ 0` buys back at most **one unit** of the offending
column, and the one explicit attempt to cancel that column costs a total `Z₁` of `5.66e5`. What
is missing is a proof over an infinite class, not an untried configuration — and that question
is already queued elsewhere, as exploration, off the critical path.

## The thing I can't say

I want to write "no certificate exists". I can't, and the novelty pass is why.

Automated certificate synthesis is a mature field, and its published epistemics are explicit:
these methods are **sound but not complete**. A found certificate proves the property. A search
that fails to find one licenses *no conclusion whatsoever* about the underlying object. Where
completeness does exist it comes from a converse theorem for the certificate class — and no
converse theorem exists for the radii-polynomial class here.

So the strongest honest claim is narrower than it feels: **the declared search space of stage
`B`, as this repository declared it, is covered clause by clause.** That is exhaustion of a
named enumeration. It is not a statement about the mathematics beyond it.

Which is, I think, the right note to end a committed sequence on. Stage `B` asked whether a
searched certificate beats a hand-tuned one. The answer is that on this operator neither one
closes, the search had about a sixth of a decade of genuine room it never used, and using all
of it would still have left the thing six times too big.

*No link of the `L1 → L4` chain moved. None has moved in 125 legs. Clay odds unchanged at
~0.05%.*
