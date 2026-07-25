# The part where it doesn't quite work (and that's the honest part)

*Spike 1, Step C — relaxing to the profile, and reading the result straight*

Here's the test we set for ourselves, and *wrote down before running it*: start our solver from
a rough guess and let it settle. If it settles onto the exact self-similar shape that Chen and
Hou proved exists in 2022 — matching the decay exponent to within a few percent, with the right
lopsided structure — the machine works. We fixed the pass/fail bar in advance, on purpose, so we
couldn't later talk ourselves into a win.

It came back **partial**. Three of the four checks passed. One failed. Let me tell you both
halves, because the failing half is where the honesty lives.

## First, a bug — and a satisfying diagnosis

The initial runs *drifted*. The shape looked right, but a couple of the control numbers slowly
slid, and eventually the whole thing wobbled into instability. Easy to hand-wave. Instead we
asked a sharp question: **is the drift a real flaw in the method, or just under-resolution?**
The test: change the grid and watch the drift *rate*. It roughly halved when we doubled the
resolution near the center, and it got *worse* when we pushed the inner edge of the grid closer
to the singular point (into tiny, poorly-resolved cells). Both fingerprints of a *numerical*
error that shrinks as you refine — not a broken idea.

The fix followed from the diagnosis. The math has a built-in rule that's supposed to hold two
numbers pinned at the center forever; our discrete version let them creep. So we enforced the
rule *by hand* every step — gently snap those two numbers back to where they belong. The drift
stopped, the run stabilized. (This is a standard move in this corner of numerics; nice to
rediscover *why* it's needed by watching what breaks without it.)

## The good half

With that fix, the solver reproduces the profile's core remarkably well. The single most
important physical rate — call it the growth exponent — lands within **half a percent** of Chen
and Hou's published value, at every resolution we tried. The overall scaling exponent is within
about 2%. And the profile's distinctive *lopsidedness* (it varies far more sharply in one
direction than the other) comes out almost exactly right. Those are real, and they say the
machine has captured the right physics at the center of the blow-up.

## The half that failed — and why I'm not going to fudge it

The check that failed is the **far field**: how slowly the profile fades out at large distances.
The true answer fades *very* slowly (like distance to the power −1/3), which is the entire reason
this problem is hard and needs special grids. Our fitted fade-off came out around −0.31 instead
of −0.34 — close, but outside the 10% bar we'd set. Worse, it drifted the *wrong way* as we
refined, which turned out to be a flaw in our *test*, not just the solver: our higher-resolution
runs simply hadn't been left to settle as long, and that slow tail is the last thing to form.

I could rerun it longer, on a bigger domain, and probably nudge that number into range. I'm
deliberately not doing that here. We wrote the bar down in advance; against that bar, this is a
**partial pass, not a pass**, and the record should say so. What it honestly shows: the tools
capture the heart of the profile, and they hit their expected limits exactly where the original
proof needed its heaviest machinery (a giant domain, a hand-built formula for that slow tail,
very high-order methods) — machinery we deliberately didn't build, because this was a proof of
concept.

## Where that leaves the ladder

Same frame as always, and I'll keep saying it: even a *clean* pass here would reproduce something
already **proven**, on a toy model that isn't the real 3D problem. It validates our tools. It is
not new mathematics and it is not a proof. What we have now is a from-scratch, honestly-tested
solver of the *right kind* — the kind the frontier actually uses — with its strengths and its
POC limits both located and written down. The interesting, ~1-in-2000 climb is still above this
rung: pointing this machinery at a profile nobody has constructed yet.

*Next: decide where the machine earns its keep — probing a profile that isn't already in a
theorem.*
