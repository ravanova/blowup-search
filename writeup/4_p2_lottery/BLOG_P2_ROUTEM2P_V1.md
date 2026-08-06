# The best candidate we had, read properly

For sixty-odd legs, one line sat at the top of our target ledger. It said, in effect: *there is
a fluid model where blow-up is **proved**, where the equation has **real dissipation** — a full
Laplacian — and where nobody has ever built a computer-assisted proof of the profile. Go
certify it.*

It came from J. Chen's paper, [arXiv:1908.09385](https://arxiv.org/abs/1908.09385)
(*Nonlinearity* **33** (2020) 2502), on the generalized Constantin–Lax–Majda equation

> ω_t + a u ω_x = u_x ω − ν Λ^γ ω,  u_x = Hω

whose abstract says it proves *"finite time self-similar blowup for a close to ½ and γ = 2."*
That is exactly the shape of thing we wanted: dissipative, proved, uncertified.

We had never read the paper past the abstract. This leg did.

## The sentence

It is the last line of the proof of Theorem 1.1, on page 12:

> *"Since ν(t) converges to 0, such profile is the same as the inviscid profile associated
> with a."*

And, from the other direction, Remark 2.1 on page 11: *"the diffusion term … vanishes as
t → +∞."* And §1.5's own roadmap, which announces the plan on page 4: *"In Section 2, we
construct the self-similar profile for the **inviscid** gCLM."*

**There is no γ = 2 dissipative profile in the paper.** The theorem is real, the blow-up is
real, the full Laplacian is really there — but the object the solution converges to is the
*inviscid* profile, and Chen writes it down in closed form on page 4:

> Ω(x) = −2bx / (x² + b²)²,  b = √(3/8),  c_l = 1/3,  c_ω = −1

The dissipation is carried along as a perturbation that dies. That is why the proof works. It
is a beautiful argument and it is not the argument our ledger thought it was.

## Why the dissipation dies, in one number

Chen's own rescaling (his equation 2.7) says the effective viscosity in self-similar
coordinates evolves as `exp(∫ (2c_l + c_ω))`. So a *steady* dissipative profile needs
`2c_l + c_ω = 0`. Strip out the arbitrary time normalisation and that is

**Δ := 2 c_l / |c_ω| − 1 = 0** — equivalently `c_l/|c_ω| = 1/2`, the heat scaling.

At Chen's profile, `c_l = 1/3` and `c_ω = −1`, so **Δ = −1/3, exactly**. The structure
collapses like `(T−t)^{1/3}`, and the diffusive length shrinks like `(T−t)^{1/2}` — faster. The
singularity outruns the diffusion. Chen's own bootstrap finds the same −1/3 independently.

We did not take that on trust. We rebuilt the profile numerically — Newton on the steady
equation, with `c_l` left as a *free unknown* and the value of `HΩ(0)` never imposed, so both
could have disagreed with the paper. They did not:

| resolution | `c_l` (Chen: 1/3) | `HΩ(0)` (Chen: 8/3) | shape error |
|---|---|---|---|
| 601 | 0.333334952 | 2.666665062 | 4.18e−06 |
| 801 | 0.333333846 | 2.666666160 | 1.32e−06 |
| 1201 | 0.333333435 | 2.666666568 | 2.61e−07 |

Chen's constants come back out as predictions, converging cleanly.

## The number we were sent to get

The question the leg was dispatched to answer: does `Y₀` — the residual a computer-assisted
proof has to fit inside its contraction budget — come in under budget?

**No, and it gets worse with effort.** At the finest resolution `Y₀ = 2.36e−07` against a
budget of `4.85e−18`: over by a factor of **4.9 × 10¹⁰**. And refining the grid *widens* the
gap (8.1 × 10⁹ → 1.7 × 10¹⁰ → 4.9 × 10¹⁰), because the quadratic constant `Z₂` grows faster
than the residual falls.

We are careful about what that number means. Much of that `Z₂` is an artefact of a
discretisation that does not border out the two gauge directions of the problem, not a
statement about the mathematics. But the direction of travel is the honest finding: this is
not a candidate that was one good week of numerics away from closing.

## And it wouldn't have mattered if it had

Suppose `Y₀` had come in under budget. What would the certificate have certified? The
*inviscid* a = ½ profile — a rational function that Chen writes out in closed form and verifies
by hand in five lines on page 4. A computer-assisted existence proof of an object you already
have an exact formula for is worth nothing.

So the candidate leaves the top of the ledger on **literature** grounds, not numerical ones.
That is the finding, and the gate we wrote before starting anticipated exactly this exit.

## One thing we did not expect

We swept Δ across the advection parameter `a`, and **it crosses zero** — at `a* ≈ 0.38650`,
found two independent ways that agree to 1.5e−04. There *is* an advection value where the γ = 2
scaling is admissible. It is not Chen's a ≈ ½, which sits a full 1/3 away in Δ, and Chen's
theorem says nothing about it.

We then tried to build a profile there, and this is the part worth being honest about. Δ = 0 is
*necessary*, not sufficient. Solutions appeared at every viscosity we tried — and two controls
said don't trust them yet:

* At ν = 1, Newton **collapsed to Ω ≡ 0**. The trivial null solves the equation exactly, so its
  residual is *zero*. Only a scale-invariant residual caught it. Had we quoted absolute
  residuals, we would have reported a perfect solve of nothing.
* A dilation of a solution at one viscosity must be a solution at another, with the *same* `a`.
  Ours moved. So Newton is landing on arbitrary points of an under-determined set, not tracing
  a branch.

So: an unclaimed corner exists at `a*`, we can see it, and **we have not shown a profile lives
there.** It goes into the record as an open lead with its failed check attached, not as a
result. That distinction is the whole discipline.

## The ledger entry, rewritten

The old entry said: *dissipative profile, proved, uncertified — go get it.*

The honest one says: *Chen's γ = 2 theorem is real and its profile is inviscid and explicit;
`Y₀` is over budget by 4.9 × 10¹⁰ and the gap widens under refinement; the γ = 2 scaling is
admissible only at `a* ≈ 0.3865`, where nothing is proved and where a profile has not been
demonstrated.*

Three legs have now been burned by reading abstracts instead of theorems. This is the first one
where we checked before building on it rather than after.

**Nothing here moves the chain toward Navier–Stokes.** Clay odds stay ~0.05%. In 125 legs no
link has moved, and this leg does not move one. What it does is retire the best-looking
candidate we had, for a reason we can quote a page number for.

---

*Data: `writeup/data/p2_route_m2p_v1_promotion.json`. Figure:
`writeup/figures/fig61_route_m2p_v1_promotion.png`. Method and every constant with its
provenance: `TECHNICAL_P2_ROUTEM2P_V1.md`.*
