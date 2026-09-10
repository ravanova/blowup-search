# Somebody claimed a Navier–Stokes result. We checked the part a machine can check.

*Written for someone who does not work on fluid dynamics and has never seen this repository.
No jargon that is not defined here.*

---

## The one-paragraph answer

In September 2026 a research group published a long mathematical manuscript claiming a particular result
about fluid equations, along with a version of the argument written in **Lean** — a language in which
mathematics can be checked mechanically by a computer. We ran that mechanical check to completion, three
times, on two different computers, using two independently written checkers. **It passed every time.**

That means the computer agrees: the Lean argument really does prove the Lean statement, using only
standard, universally accepted logical assumptions, with no gaps left as "to be filled in later".

**It does not mean the fluid-dynamics claim is proved.** The statement written in Lean is *weaker* than
the claim made in the manuscript. Checking it is real and worth doing, and it is not the same thing.

## What was actually verified

Think of it as three separate questions.

1. **Does the formal argument have holes?** In Lean, an unfinished step is marked `sorry`. We found four
   in the project, all in the harness that poses the challenge — **none of them inside the proof that was
   checked**. Nothing was left unproved along the path that matters.
2. **Does it smuggle in extra assumptions?** A Lean proof can be forced through by declaring new axioms.
   We printed every assumption both theorems depend on. There were exactly three, and they are the three
   that essentially all modern formal mathematics uses. No others. Nothing custom, nothing convenient.
3. **Is the checker itself trustworthy?** We replayed the whole thing through a **second** checker,
   written independently in a different programming language by different people. It also accepted. Two
   independent programs agreeing is much stronger than one program run twice.

## What was not verified, stated plainly

- **The manuscript's actual theorem.** The Lean statement is a recognised, weaker version of the target.
  Several existence conditions in the paper's own theorem simply are not present in the formal statement.
  A green check on the weaker statement is not a green check on the stronger one.
- **That the Lean proof follows the paper's reasoning.** It proves its own statement. Whether it does so
  by the argument the manuscript describes is a separate question we did not answer.
- **The mathematics library underneath.** Formal proofs are built on a large shared library. We confirmed
  the copy we used is internally valid and correctly labelled, but not that its pre-compiled files
  *mean* what the library's published source text says. Closing that needs a full recompile. We measured
  what it would cost — roughly four hours — and did not run it.
- **Anything about who did what first.** There is a dispute about priority around this manuscript.
  **This project takes no position on it whatsoever.** We have no evidence bearing on it, so we say
  nothing about it, in either direction.

## The part where we failed, included on purpose

Separately, we tried to check some of the manuscript's *numerical* content ourselves — recomputing
quantities the paper predicts and seeing whether independent routes agree.

We set one rule in advance: a result counts as evidence only if two genuinely different methods agree on
a quantity that a cheater could not simply choose. Then we hired a "cheater": an agent told only what the
tests were, and paid to pass them using calculations it knew were wrong.

**It passed all five tests.**

Worse, when we audited our own tests, we found one where the "two independent methods" were the same
formula written twice. The giveaway was that the two answers agreed *exactly* — not to fifteen decimal
places, but bit-for-bit. Genuine independent computation almost never does that. Two further tests turned
out to be built on mistakes of ours: one asked for a parameter value the mathematics does not permit, and
another cited a table that does not contain the quantity being tested.

So that part of the work produced **no usable evidence at all** — and the fault was in our tests, not in
the manuscript. It is not evidence the paper is wrong. It is evidence our instrument was broken. We are
reporting it because a check you only publish when it agrees with you is not a check.

## How to read anything else from this project

Every claim here carries a **tier** and a **verification label**.

- *Tier 2* means numerically supported. **Tier 2 is never a proof.** Nothing in this project is Tier 3.
- *`VERIFIED`* means a second worker, with no knowledge of how the first got its answer, reproduced it
  from the raw saved data. Anything else is *`UNVERIFIED`* and says so. Most of this repository is
  `UNVERIFIED`.

The kernel result above is Tier 2 and `VERIFIED`. The numerical work is `UNVERIFIED` and produced nothing.

**If you quote a result from here, quote its status with it.** A number without its tier and label is a
misquotation.

## Does this bring anyone closer to solving Navier–Stokes?

No. The Clay Millennium Prize problem has four conditions, and none of them is met by anything in this
repository. This project has run 440 units of work and has not moved a single link of the chain that
would be required. We keep a running estimate of our own probability of success, and it is about 0.05%.

We think that is worth publishing anyway. The kernel check is a small, sharp, reproducible fact that
nobody else had published, and the failed numerical check is a useful warning about how easy it is to
build a test that cannot fail.

---

**Reuse:** prose and data here are CC BY 4.0; code is MIT. Credit **Andy**, and link back to
<https://github.com/ravanova/blowup-search>. Details in [`NOTICE.md`](../../NOTICE.md).

**Reproduce it yourself:** the runner is `scripts/arc7_k1_kernel_check.sh`; the saved evidence is under
`writeup/data/arc7/`; and `writeup/7_confirmation/confirmation_evidence.py` re-derives every number in
our technical write-up from that saved data and fails loudly if any of it has drifted.
