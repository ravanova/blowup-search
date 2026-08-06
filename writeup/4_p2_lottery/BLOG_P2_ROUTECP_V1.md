# Somebody else's paper, read at the right depth

*Route-CP v1 — leg 62. Companion: [`TECHNICAL_P2_ROUTECP_V1.md`](TECHNICAL_P2_ROUTECP_V1.md).
Figure: `fig56_route_cp_v1_cadiot.png`.*

---

Twice now this project has been burned by reading a paper at the wrong depth. Leg 53 read
a dominance hypothesis off a publisher's abstract page, built a claim on it, and had to
withdraw the claim. The correction is a standing ban, and it is the reason this leg exists.

Seven legs of work (51–57) had produced a negative result about a certification method:
the standard tail estimate closes because the unbounded part of the operator is a
*multiplier*, and ours is a *shift*. Leg 57 then found that observation already in print —
in Cadiot, arXiv:2505.03091 — and correctly recommended not claiming it. But it left the
question that actually matters unanswered: **does that paper's construction reach our
case?** Not "does it say the same sentence", but "does its machinery cover an operator
whose unbounded part sits off the diagonal, where the diagonal is exactly zero?"

That question is worth settling because a wrong answer is expensive in both directions. If
Cadiot covers our case, the negative result the repository is assembling is pre-empted
before it is written. If he does not, the claim that can be made is precisely bounded, and
saying so is what keeps the next write-up honest.

**The answer is no**, and it is no for six independent reasons rather than one.

## Fetch the paper, not the abstract

`bash Papers/fetch.sh 2505.03091` — 30 pages, extracted, read. Six clauses located, each
with a section number and the sentence verbatim, because a located statement can be checked
and a paraphrase cannot.

The strongest of them is not a hypothesis at all — it is the definition of the class, on
page 1, before any assumption is stated:

> *we assume that `L` is a Fourier multiplier operator, that is it is given by its symbol
> `l` as `F(Lu)(ξ) = l(ξ)F(u)(ξ)`… If `l` is polynomial, then `L` is a linear differential
> operator with **constant coefficients**.*

A Fourier multiplier is diagonal, by construction. Our unbounded part is a dilation — a
variable-coefficient transport term — which has no symbol at all. We are outside the class
before Assumption 1 is reached.

Then Assumption 1 itself asks for two things: a symbol bounded away from zero
(`|l(ξ)| ≥ l_min > 0`) and a symbol going to infinity. Our diagonal is *identically zero*.
And section 3 does not merely state those; it **uses** both, twice, in the two lemmas that
carry the whole argument.

## But quoting a hypothesis is not measuring it

Here is where this leg tried to do better than "we read it and it doesn't apply". A
hypothesis you can only quote is a sentence. A hypothesis you can **measure on the author's
own examples** has a scale — and it can be checked against what the author himself says.

Cadiot works three examples. For three of them he states the constant `l_min` in words. So
we transcribed his symbols and computed it:

| his example | we measure | he states |
|---|---|---|
| Swift–Hohenberg (square) | `0.280000` | `0.28` |
| Swift–Hohenberg (hexagon) | `0.320000` | `0.32` |
| capillary-gravity Whitham | `0.200000` | `0.2` |
| Gray–Scott | `0.999938` | (not stated) |

Ours is **exactly `0`** — not small, absent.

The third row is the nicest. He writes, in the middle of a proof, *"notice that
`l(ξ) ≥ l(0) = 1 − c = 0.2` for all `ξ ∈ R`."* We reproduce `0.2` to `5.6e−17`. His
hypothesis is not a formality he waves at; it is a number he computes.

## The one place an off-diagonal entry appears in the paper

If the framework reached an off-diagonal *unbounded* part, it would have to be in the
systems example, §5.3, because a system is the only route an off-diagonal entry has into
this machinery at all. So we looked, and measured:

* the off-diagonal entry is the **constant `1/9`**;
* both diagonal entries grow like `|2πξ|²`;
* the ratio of the two decays with exponent **`−2.000`**, reaching `2.5e−10` by `|ξ| = 10⁴`.

Even in the systems case, the unbounded part is the diagonal and the off-diagonal is a
bounded perturbation of it. Ours is the other way round.

## The sharpest form: a shift that does not exist

The load-bearing measurement is about his Lemma 3.2. To use the generalized Gershgorin
theorem he borrows, the proof has to produce **one** complex number `s`, big enough in
amplitude, that makes the shifted diagonal dominate half of every row sum — *simultaneously
at every mode*. In his setting such an `s` exists because the row sums are bounded while
the diagonal runs off to infinity.

So: compute the smallest such `s`, on his operator and on ours, as the truncation grows.

* **His** (the Whitham operator, his symbol, his coordinates): `0.28723`. At every
  truncation. Exactly the same number. One finite shift serves the infinite matrix.
* **Ours**: `63 → 127 → 255 → 511 → 1023`. It grows **linearly** with the truncation.

That linear growth is the whole finding in one line. It does not say the constant is bad.
It says the object his proof needs **does not exist** on our operator.

And there is a detail that closes the loop. His `0.28723` is predicted exactly by
`sqrt((r/2)² − l_min²)` with `l_min = 0.2` — the binding row is the very row Assumption 1
is about. His hypothesis and his shift are the same fact.

## Four identical numbers should read as a bug

This repository has a rule, learned the hard way: a control that cannot come out
differently is not a control, and the tell is that its numbers are *identical*. That
`0.28723` at four different truncations is exactly the pattern the rule warns about.

So we checked what would have to change for it to move — and made it move. Vary the size of
the operator's compact part and the shift goes `0.0 → 0.287 → 1.990 → 9.998`. Meanwhile the
*exponent* of the decay does not move at all, spread `4e−15`, because it belongs to his
symbol rather than to the perturbation. The level responds; the shape does not. That is
saturation, not a tautology of the code.

The gate predicate got the same treatment: it flips to "yes" two independent ways in the
test suite. "No" is a property of the located clauses, not of the code that reads them.

## Three numbers on one dial, and the discipline of keeping them apart

Adding dissipation to our operator gives a one-parameter family, and it turns out that two
different published hypotheses land on that dial at two different places:

* Cadiot's Lemma 3.2 admits the family for **`μ ≥ 1/2`**;
* Breden–Desvillettes–Lessard's assumption (5) admits it only for **`μ > 1`**;
* and the operator's *own* change of character — a different quantity, measured by leg 57 —
  is at **`μ = 0`**, exactly.

Factor of two between the two hypotheses, and both of them vacuous where it matters. Two
hypotheses of two constructions and one property of an operator: three numbers, not one.
Collapsing them would be how a hypothesis of somebody's proof gets misread as a fact about
our operator, and this project has done that before too.

## What this is worth, and what it is not

It is worth exactly one sentence of licence: **the next leg may claim novelty against this
paper, and no further.** Four papers is a corpus, not a theorem. Every quote here is
transcribed by a human-equivalent process and is only as good as that — which is why every
row carries its URL, so the next pass can check rather than trust.

It is **not** evidence that the negative result is true. A gap in one paper is not a
theorem. This leg caps a claim; it does not support one.

And it is not a criticism of Cadiot. Every clause located here is a hypothesis his paper
states plainly and discharges on its own examples — which is precisely why the measurement
against those examples works at all.

*No link of the L1→L4 chain moved. Clay stays at ~0.05%, behind Walls 1 and 2.*
