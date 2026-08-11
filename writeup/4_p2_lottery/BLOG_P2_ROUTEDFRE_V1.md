# Grading someone else's proof, without running any of their software

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. This is the
first entry of a new standing habit: once a cycle, take a published computer-assisted proof
and see if this project can independently check it. Not a step toward Navier–Stokes — a
different kind of usefulness, and this post says exactly which kind.*

## The habit, and why it exists

Twice now, checking someone else's published, refereed, computer-assisted proof has turned
up something real: a sign convention that was silently flipping which problem a bound was
actually proving, and a stale multiplier in a released Jupyter notebook that no longer
matches the paper's own printed numbers. Both times the theorems survived — nothing here
is a "gotcha" project — but both times the released *artifact* had drifted from the
*paper*, in a way nobody had apparently checked before.

So it's a lane now: once a cycle, reproduce one published computer-assisted proof, in the
open, with the finding banked either way. This entry: a 2024 paper by Joel Dähne and
Jordi-Lluís Figueras, proving that a certain nonlinear wave equation — the complex
Ginzburg–Landau equation, which is the Schrödinger equation plus a dissipation term, the
same kind of term that separates the "solved" fluid equation from the trillion-dollar open
one — has whole continuous families of solutions that blow up in finite time, *as
dissipation is turned on*. This project used that exact result once before, to close off a
different question (does turning dissipation on kill a certificate's margin — someone had
already answered that, so this project didn't have to). This time it's a different
question: is their own released proof output internally consistent with their own theorem?

## What "reproduce" means when you have no proof software

Their paper's rigorous computations run in Julia, calling a library called Arb for
interval arithmetic, and a C++ library called CAPD for the underlying differential
equations. This project's environment has none of those three. So step one had to be
figuring out what "reproducing" a proof like this could even mean without the ability to
run any of it.

The paper's authors released their code. Buried in it — not mentioned in the paper's
prose, only findable by opening the repository at the exact commit the paper's own
bibliography names — are the actual data files their proof produced: hundreds of thousands
of numbers, each one a tiny interval that a piece of their machinery has *proved* contains
a real mathematical object (the coefficient of a solution). These numbers are stored in a
raw, undocumented-in-the-paper binary-ish text format: two integers per number, meaning
"this many times two-to-this-power," read straight out of the library's own source code to
get the format right.

That turns out to be exactly enough. Their theorem's whole argument, once you strip away
the analysis that produced the numbers, comes down to a purely geometric fact: hundreds of
small boxes, each one guaranteed to contain a real solution, have to link up end to end —
box two's "for sure a solution is here" region has to sit inside box one's "and it's the
*only* solution here" region, and so on down the chain — for the boxes to add up to one
continuous curve of solutions instead of a scattered pile of disconnected ones. That
condition doesn't need Julia, Arb, or CAPD to check. It needs exact arithmetic on the two
integers each box is made of, and a comparison. Python's standard library does exact
arithmetic on integers for free.

## The number

**49,465** of these proved boxes, across the one branch of solutions this leg pre-committed
to checking, decoded with no approximation at all — the same integers their software
produced, not a rounded or re-derived version of them — and checked against the paper's own
stated linking condition.

**Every single one links up.** Zero failures, zero near-misses close enough to worry about.
And a second, independent check catches the kind of dumb mistake that would make this whole
exercise meaningless — a wrong byte offset, a flipped sign — by comparing the very first
box's centre against the one number the paper actually prints in its own prose (not buried
in the released data): they agree to six decimal places, comfortably inside the box's own
proven width.

## What this is not

This did not re-check whether their *interval arithmetic itself* is trustworthy — that
rests on the correctness of Arb and CAPD, which this leg didn't touch. It checked one
specific, necessary, purely combinatorial condition on their *own reported output*, for
one of twelve solution branches their paper proves exist. It is not evidence about
Navier–Stokes; the equation here is a different, gentler one (it doesn't have the boundary
and transport structure that makes the real target hard), and nothing about this leg moves
any part of the actual chain toward the million-dollar problem. It cost about thirty
seconds of computer time once the data was downloaded.

What it is: one more real, checkable, independently-run confirmation of a genuine result in
a field where — as an earlier leg in this project measured directly — essentially nobody
is doing this kind of check on anybody else's work. Twice out of two prior tries, that check
found something. This time it didn't. That's worth recording too — a clean pass isn't a
failure of the exercise, it's the other half of what the exercise is for.
