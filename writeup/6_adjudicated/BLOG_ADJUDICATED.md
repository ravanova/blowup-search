# We read the proof of the century. Here is what we can actually say about it.

*Arc 6 of a search programme for finite-time blowup in 3D Navier–Stokes. Six legs, one session,
2026-09-09. Companion to [`TECHNICAL_ADJUDICATED.md`](TECHNICAL_ADJUDICATED.md), which carries
every number and its provenance.*

---

## The situation

On 8 September 2026 a 166-page manuscript appeared claiming finite-time blowup for the forced
three-dimensional Navier–Stokes equations, with a Lean 4 project alongside it. That is the exact
statement this programme had been aiming at for 416 legs, and it was answered somewhere else.

The previous arc wrote that down honestly and then did something more useful than mourn: it set
this arc two questions.

> **Is the claimed result correct, on our own reading and our own compile?**
> **Does its mechanism move `W4` — our own named wall — under `W4`'s own test?**

The second question is the one that is ours. Nobody else has our wall.

---

## The first thing we found was our own mistake

We fetched the manuscript, hashed it, and compared its Theorem 1.1 against what the previous arc
had banked from press coverage. Eight things matched. **Seven differed**, and one of the seven
mattered a great deal.

The previous arc had written: *"(A) and (B) are untouched. The unforced problem is open. So is
(D)."* Statement (D) is the torus version of the same problem, and it happens to be **the only
unbroken way our own wall `W4` can be broken.** We had a whole lane parked behind it, on the
premise that (D) was the nearest *unclaimed* target.

Theorem 1.1's last sentence reads: *"Compact support also yields the corresponding construction on
`T³ = ℝ³/ℤ³`, establishing alternative (D); see Corollary 10.6."*

**It is claimed.** Not proved-to-our-satisfaction — we have not checked the proof — but claimed, in
the same document, as a corollary. Our premise for that lane was false on the manuscript's own
text, and we had been reading press summaries instead of the primary source.

Fixing that took an afternoon and one `curl`. It had been sitting there since the day the paper
went up.

---

## The Lean project: what a "verified proof" does and does not mean

The project has 2,486 Lean files. We could not compile it. The reason is worth stating precisely,
because "we couldn't build it" and "it doesn't build" are different claims and only one of them is
ours to make.

Lean's mathematics library is normally downloaded pre-compiled from a cache. **That cache's host is
blocked by this environment's network policy** — the proxy logs a 502, we reported it, and we did
not route around it. So the library has to be compiled from scratch first, which is hours of
four-core work before a single line of the *project* is looked at. **We started it, left it
running, and answered the build question `NOT-ESTABLISHED` with the blocker named.**

That leaves three questions we *could* answer by reading, and they turn out to be the interesting
ones.

**Is the top-level statement the theorem?** Yes — and the good news is not ours. The definitions
the statement is built from are **not the authors'**. They are Google DeepMind's independent
formalisation of the Clay problem, and we fetched that file at the exact commit the project pins
and diffed it. **Every definition and both theorem statements are character-for-character
identical.** The only differences are a namespace, two notation lines and some attributes.

This matters more than it sounds. The most common way a formalisation is *true but not the theorem*
is that someone writes their own encoding and a hypothesis quietly gets weaker. Here that cannot
happen, and we checked it at the upstream source rather than believing the comment that says so.

**Is it free of holes?** In the project's own files: four `sorry` placeholders, all in the
*reference* statements, none in the 580-module dependency graph of the actual theorem. Zero axioms.
We verified the "no holes reach the theorem" claim ourselves by parsing every `import` line in all
2,486 files rather than taking the header's word for it.

We also nearly reported a scandal that wasn't there. A naive count finds **29 `sorry`s and 6
axioms** — all of them inside the *verification tool's own adversarial test suite*, in directories
called things like `def_hole_axiom_issue`. That is a tool testing that it catches cheating, and it
would have looked terrible in a headline.

**And how much of the paper is formalised?** Here the answer is genuinely two answers, and giving
one would be dishonest. **The theorem: entirely** — that is what a formalisation is for. **The
argument: not measurably.** The project maps four statements to the papers and nothing finer. When
we looked for cross-references, we found the Lean cites `Lemma 11.3` and `Proposition 11.7` and
calls its source *"the candidate manuscript"* — **but the published paper has ten sections and no
Section 11.** The formalisation was written against a different draft.

That is completely normal for a project developed alongside a paper. It is also decisive for the
question people actually want answered. If the build passes and the axioms check out, **the theorem
is proved and the 166 pages stop mattering for whether it is true.** But if you want to know
whether *the paper's proof* is right, the Lean tells you almost nothing, because it never says
which of its 23,604 lemmas is which page.

---

## What actually buys the compact support

The previous arc had a theory about why this construction escapes the trap our own programme is
stuck in. The trap, `W4`, is this: the objects we know how to build have infinite total energy, and
the problem demands finite total energy. Cutting the object off to make it finite breaks the
equation, and nobody knows how to repair that.

The manuscript's escape, in one sentence of its §3.5: **"For `t < 1`, we set `f = R(u,p)`."**

The equation being solved is *forced*. The force is a free variable. So you do not have to make the
error small — **you define the error to be the force.** Every term the cutoff creates is absorbed
by that definition rather than estimated.

The previous arc said this was cheap, because the one condition the force must satisfy — decay at
infinity — follows from compact support in three lines. **It does, and we checked those three
lines.** But that reading loses the price.

Cut off an object whose error blows up at the singular time, and you get a *force* that blows up at
the singular time — and that is not an admissible force. To make the trick legal you first have to
build an object whose error vanishes **faster than every power** at the singularity. That estimate
is Sections 4 through 9 plus three appendices: **131 of the manuscript's 166 pages. 78.9%.**

So the door is open, and it is not near. Our own leg 381 had said both halves — that the forcing
"buys no escape" (wrong) and that it is "not a shortcut" (right) — and the previous arc kept the
half that was wrong and dropped the half that was right. **We record that as a split, not a
reversal.** Being wrong in one direction does not make you right in the other.

---

## Then we asked our own wall

This is the part that is ours.

We took our own object — a closed-form witness this repository built and banked legs ago — applied
the manuscript's mechanism to it **literally**, and gave the mechanism every advantage we could
think of. Zero pressure. Force defined as whatever is left, so the equation holds *exactly*. Cutoff
applied to the vector potential so that incompressibility survives untouched. If it was going to
work, nothing in our setup was going to stop it.

**It fails twice, and the second failure is the interesting one.**

**First**, on our own object, the error where the cutoff isn't even active diverges as `τ^{-3/2}` —
we measured the exponent as **`−1.500000`**, with agreement across three resolutions of `3×10⁻⁷`.
That is because our object is not an exact solution of its own profile equation and never was. It
is a fact about us, not about the wall.

**Second**, and this is the one with reach: we granted ourselves an exact profile — imagined the
first problem away — and measured only what the *cutoff itself* generates. The force there does not
blow up like a power. It grows **logarithmically**, forever, and its time derivative diverges like
`1/τ`. Still not an admissible force.

We nearly missed it. A power-law fit returns an exponent of **`−0.005`**, which reads as
*"bounded"*. It is not bounded; that is simply what a logarithm looks like to a power fit. **We had
flagged exactly this in the pre-registration**, written before any number existed, because this
repository has been fooled by a logarithm twice already and wrote down what to check. The check —
are the per-decade increments constant? — is what caught it. They are: `0.7479, 0.7419, 0.7412,
0.7435`.

![fig112](../figures/fig112_arc6_w4_port_v1_log.png)

*fig112 — the same tiny power exponent, twice, and only one of them is bounded. Left: the
cutoff-generated force, a straight line against `log(1/τ)`. Right: the kinetic energy, whose
per-decade increments fall geometrically to a limit.*

**`W4` stands.** We did not raise an escalation, because escalations are for when a wall breaks.

---

## Three things worth keeping

**We confirmed our own pinned number by a route that shares no step with how we pinned it.** The
far-field decay exponent of these objects was fixed at exactly 1 by a literature argument with two
one-sided theorems. We measured it from the closed form: **`−1.000004`**.

**We measured something we had never measured.** The *next* term in the far-field expansion —
`δ = 1.974`. It turns out that the whole question of whether this mechanism can work on a cut
profile reduces to that one number, because the leading term is time-independent and cancels out of
the problem. That reduction is the useful thing this arc produced: it turns *"does the mechanism
port?"* into *"what is the far field of the profile?"*, which is a question you can go and measure.

**And our own pre-registration was wrong, in a way our own control caught.** In an earlier leg we
wrote down a formula for a predicted exponent and one of our own planted controls came back 0.19
off. The formula had dropped a term — invisible at the design point, dominant everywhere else. We
reported the control as **failed**, banked the corrected formula as *post-hoc*, and did **not**
re-score the control against it. Re-scoring after seeing the number is the entire thing a
pre-registration exists to prevent.

---

## What we can honestly say

We can say the statement is Fefferman's alternative (C), that it claims (D) too, and that the Lean
project's top-level theorem is that statement in a third party's own words with no holes reaching
it. **We cannot say the proof is correct.** We did not read Sections 4 through 9. We did not
compile the Lean. Nothing here suggests the proof is wrong either, and nobody should quote it as if
it did.

What we *can* say about our own wall is sharper: the mechanism does not port, we know why in two
independent ways, and one of the two is a statement about the object class rather than about our
particular object.

No wall moved. Nothing moved on the Clay chain. The odds stay where they were.

**But we now know exactly which number would have to change, and that is more than we had
yesterday.**
