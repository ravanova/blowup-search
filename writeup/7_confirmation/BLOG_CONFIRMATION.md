# We ran the kernel. It went green. Here is exactly how much that is worth.

**Arc 7, legs 436–440, 2026-09-10.**

## The verdict, before anything else

On one pinned commit, in three environments, and by two independently written proof kernels, both
exported Lean theorems are accepted depending on no axiom beyond `propext`, `Classical.choice` and
`Quot.sound`, with `sorryAx` unreachable.

**That is the whole of what we confirm.** It confirms the Lean project proves what its own statements
say. Those statements are Fefferman's alternatives (C)/(D) — **strictly weaker** than the manuscript's
Theorem 1.1. It is not a confirmation that the 166-page proof is correct. And our own independent attempt
to check the construction numerically produced **zero** surviving evidence, in either direction.

Everything after this paragraph makes that verdict smaller and more precise. None of it makes it bigger.

**On the priority dispute around the manuscript, this repository takes no position whatsoever.** Nothing
we can measure reaches that question, so we say nothing about it.

## Why a kernel run was the right thing to attempt

In September 2026 a 166-page manuscript claimed finite-time blowup for the **forced** 3D Navier–Stokes
equations, together with a Lean formalisation. Out-refereeing 166 pages of hard analysis is beyond this
project. Running a proof kernel to completion is not — and nobody had published one.

So that became the goal: not to re-derive the result, but to **check the machine-checkable part of it**.

## What went green

A fresh clone, a full build, then `#print axioms`. Three times:

- a remote container, resumed — 2047 s of build;
- a **different** remote container, from a clean clone — **5605 s** end to end;
- the operator's laptop, from a clean clone — **4272 s** end to end.

`Build completed successfully (11251 jobs).` in all three, zero error lines, identical pin, identical
mathlib revision, identical toolchain, 2486 oleans. Both theorems printed the standard three axioms.
`sorryAx`: not reachable, anywhere.

Then a second, blind agent — no memory of how any of it was produced — re-derived the result from the raw
build and axiom logs rather than our summaries, and agreed. That, and only that, is why the result is
labelled `VERIFIED` rather than `GREEN, UNVERIFIED`. Three runs by one lineage would not have earned it:
**a second machine is not a second agent.**

## The part that surprised us: a second kernel

The Comparator harness replays the entire solution environment through **nanoda**, an independently
written Rust implementation of the Lean kernel. Both kernels accept. That is a genuinely different
implementation agreeing on the same proof object, and it closed a limit we had banked as open: the cached
mathlib libraries are **kernel-valid** and use no forbidden axiom.

It did **not** close the neighbouring question. "Are these cached binaries *labelled* as built from these
sources" (yes, content-addressed, 8747 cache files, every key matching), "are they kernel-valid" (yes,
twice over) and "do they **mean** what mathlib's source text says" are three different claims. The third
needed a recompile, and when we first published this page we had costed it — about four hours — and
**not run it**, because scheduling it was the operator's call.

**They scheduled it. It ran on 2026-09-11, and the third claim is now closed too.** mathlib was compiled
from its own published source on the same laptop, with `lake exe cache get` **never invoked** — 8370
`Built Mathlib.` lines, zero replayed — and both theorems returned the same three axioms, byte for byte:
the `depends on axioms` lines from the rebuild and from both cached runs hash to the same md5. So the
cached binaries were not load-bearing. It cost 11578 s against 4272 s cached — **2.71×** — and a 28.5 GB
build tree. What it does **not** do is make any of this independent: same lineage, same laptop. And the
end of the trust path simply moved — it now stops at the Lean compiler binary, which we installed rather
than built.

## The part that went badly, and why we are leading with it anyway

We also re-ran our own numerical attack on the paper's construction, under one rule fixed in advance:

> *Evidence is a two-route agreement on a quantity the adversary cannot choose.*

Five workers took five gates. A sixth agent — blind, told only the gate wordings — was paid to **fake**
them: to make each gate say `YES` from a run it knew to be wrong.

It faked all five.

And while checking the workers, we found something worse in our own pre-registration. One gate, `Q5`,
compared "two routes" that were the same closed-form expression evaluated twice. The tell was the error:
exactly `0.0`, in all four cells, where an independent numerical route would have given something like
`1e-16`. A quantity that does not move when you replace the profile is not measuring the profile. The
blind adversary found the same defect independently.

Two more pre-registration defects surfaced the same way: a second parameter scale that **violates the
construction's own hypotheses** (the builder refuses to run there, and said so), and a gate citing a table
that does not contain the quantity it gates.

All three defects are ours, not the workers'. The workers executed what they were given, reported their
own failures — including a planted control that did not fire as planted — and one of them found the
scale defect unaided and declared it.

**So: zero of five gates survived as evidence.** That is a finding about **our gates**, not about the
manuscript. Nothing in it suggests the paper is wrong. It says our instrument could be spoofed, so its
readings do not count.

## Why that does not change the headline

The kernel check and the construction wave are answering different questions. The kernel says the formal
statements follow from the formal axioms. The construction wave was an attempt to independently probe the
paper's analysis numerically, and it failed to produce trustworthy signal in either direction.

A reader who takes only one sentence should take the first one. A reader who takes two should take that
the statements checked are weaker than the paper's theorem.

## What this still is not

Not a solution to Navier–Stokes, by us or anyone — the Clay problem has four conditions and none is met.
Not a proof that the manuscript is correct. Not a claim that it is wrong. No wall in this project moved;
no link in its `L1→L4` chain moved, after 440 legs. Everything here is **Tier 2**, and Tier 2 is never a
proof.

If you quote a number from this project, quote its status with it. A number without its tier and its
verification label is a misquotation.

---

*Full record with every number cited by field:*
[`TECHNICAL_CONFIRMATION.md`](TECHNICAL_CONFIRMATION.md). *Rebuild it:*
`.venv/bin/python writeup/7_confirmation/confirmation_evidence.py`.
*Reuse terms and attribution:* [`NOTICE.md`](../../NOTICE.md) — credit **Andy**, and link
<https://github.com/ravanova/blowup-search>.
