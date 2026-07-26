# Chasing a singular attractor: what a laptop-scale solver can (and can't) say about a conjecture

*Phase-2 P2, the dynamic-relaxation leg. Companion to `TECHNICAL_P2_CONJ24.md`. Honest tier:
a partial, local, proof-of-concept confirmation of a numerical claim — not novel, not a proof.*

Our anchor last time reproduced a *proven* result: the explicit singular self-similar profile of
the 1D Hou–Luo model that Chen–Huang–Li (CHL) wrote down and proved exists. Reproducing a theorem
validates your machinery but breaks no new ground. The interesting thing in CHL's paper isn't the
theorem — it's the **conjecture** next to it: that this singular profile is *asymptotically
stable*, i.e. generic degenerate data flows into it. They assert that from their numerics; nobody
has proven it. So we pointed our solver at it.

### The one idea that makes the degenerate case work

Dynamic-rescaling solvers keep a blowing-up solution on-screen by continuously zooming; the "zoom
rate" is a **gauge** you have to pin down with a normalization. The standard trick pins the slope
of the vorticity at the origin. For the *degenerate* data CHL study, that slope is **exactly zero**
— the standard gauge divides by zero and dies.

CHL's fix is elegant: read the amplitude not from the local slope but from the **nonlocal**
velocity gradient at the origin, `H(Omega)(0)` (a Hilbert-transform integral). That quantity stays
comfortably nonzero even when the local slope vanishes. We implemented it and checked it against
the one profile where we know the answer: on CHL's exact singular profile it returns the scaling
constants `(c_l, c_omega) = (2, -1)` to within a few percent. On degenerate data the old gauge reads
`~1e-4` (dead) while the new one reads `~1.2` (alive). That's the whole ballgame for the degenerate
regime, and it works.

### The wall

Then we tried to actually *evolve* toward the singular profile — and hit a wall, honestly. The
target profile has a hard edge (it's `(X-1)^{-1/2}`, infinite at one point, zero next to it). Our
straightforward scheme rings against that edge like a struck bell, the ringing feeds a stiff source
term, and the whole thing blows up within a fraction of a time unit — even when you *start it
sitting exactly on the profile*. This is the same difficulty that pushed CHL to heavy machinery
(adaptive meshes, WENO limiters). We added a modest dose of numerical dissipation to damp the
ringing. That's a proof-of-concept crutch, not their industrial solution — but it let us ask the
question.

### What the solver actually showed

With the dissipation in, the picture is clean and, we think, genuinely informative at its level:

- **Start on the profile → it stays.** The scaling constants hold at `(1.94, -0.93)` ≈ `(2, -1)`
  and the residual drops ~50× and levels off. The profile is a numerical fixed point.
- **Kick it → it comes back.** Two different smooth perturbations both relax **to the same fixed
  point**. That "comes back" is the actual content of *local* asymptotic stability — the local
  version of CHL's conjecture, independently reproduced.
- **It's not a fluke of one knob.** Double the dissipation and the constants don't move; only the
  residual floor shifts, the way a controllable numerical artifact should.
- **But throw generic far data at it → it goes somewhere else.** A generic degenerate bump doesn't
  find the singular profile; it settles into a *different* self-similar state. The **global** basin
  — the full strength of CHL's conjecture — is beyond what a fixed-grid laptop solver reaches.

Everything above was decided against a predicate we wrote down and committed to git *before*
running. Nine clauses, nine held — including the one that predicted the negative. We didn't tune
our way to a pass.

### The honest ledger

We reproduced the **local** part of a numerical conjecture and drew a clear line where our tools
stop. That's a Tier-2-style independent confirmation: useful, shareable, backed by committed data
that rebuilds the figure — and explicitly **not** a new theorem, not new mathematics, and (since
1D Hou–Luo is a toy model of the *boundary* behaviour of the real 3D problem) not a dent in the
Clay problem. The genuinely-new math would start one rung up: the "two-scale vs two-stage" question
a scout of the Hou–Huang link turned up, which needs exactly the global-basin numerics we don't yet
have. Knowing precisely which rung you're on is the point.

### Postscript: that "somewhere else" wasn't a dead end

A follow-up look at *where* the generic data actually went changed the reading of the one negative
above. That "different self-similar state" isn't numerical junk — it's a **smooth, strictly-positive
profile peaked away from the singular point**. Chen–Huang–Li describe exactly such an object: it's
the **first stage** of their two-stage blow-up (their "Scenario 2"), the regular profile that forms
*before* the singular one. So our solver, from generic data, lands on CHL's Stage-1 profile on its
own — and from near-singular data it holds the Stage-2 singular profile. Two attractors, both CHL,
both reproduced.

The honest asterisks stay firmly attached. We reached the regular profile with our *original* gauge,
not CHL's purpose-built one — so this is a family-resemblance match (regular, positive, peaked off
the singular point), not a proof that it's the *same* profile down to the constants. In fact, watched
long enough, our solver drifts *through* the neighborhood of CHL's published numbers and can't quite
stand still there — a tell that we're using the wrong normalization for this profile, and a clean
pointer to the next small, well-posed piece of work: adopt CHL's Stage-1 normalization and check we
land exactly on their numbers. Still a reproduction, not new mathematics. But the map got sharper.
