# The free lunch, priced (leg 390)

There is a version of the Clay Navier–Stokes problem that quietly deletes the hardest thing on our
obligations list. Fefferman's official statement comes in four parts, and part **(D)** asks for
breakdown on the **torus** — periodic boundary conditions — instead of on all of ℝ³. Part (C), the
ℝ³ version, requires a hypothetical blow-up solution to have **bounded energy**. Part (D) does not.

Our `CLAY_OBLIGATIONS.md` §4 is *entirely* the bounded-energy obligation and the localisation work it
generates. If (D) deletes the premise, §4 evaporates. That is what a free lunch looks like.

Free lunches in this repository have a history of turning up on a later bill. So this leg did one
thing: **it read the price tag.** It authorises nothing, it changes no target, and it makes **no
recommendation**. When you finish this page you will know the magnitudes and you will still be facing
the choice, which is the point.

## The deletion is real

We didn't take the earlier note's word for it. The runner parses Fefferman's own banked text and
splits each breakdown statement into what the *data* must satisfy and what a *solution* would have
to satisfy:

* **(C)** solution conditions: (1), (2), (3), (6), **(7)**
* **(D)** solution conditions: (1), (2), (3), **(10)**, (11)

Conditions (6) and (11) turn out to be the same text. So going from (C) to (D) exactly one condition
leaves and exactly one arrives: **(7) bounded energy out, (10) periodicity in.** §4's premise is
genuinely absent from (D). (Plant (7) back into the list and the check reports it present — the green
light can go red.)

One honest gap: (D)'s *data* conditions (8) and (9) are not in this repository, and this leg has no
outreach. Nothing here is priced from them.

## Then the rigidity bites

Here is the thing that shapes everything else. Our target object is **discretely self-similar** — it
reproduces itself under a zoom by a fixed factor λ. Zoom is exactly the thing a torus does not have.

If a field is both periodic on a box of side L and exactly λ-DSS, then it is also periodic on a box
of side L/λ, and L/λ², and so on forever — which means it is **constant**. A non-constant exactly-DSS
field on the torus does not exist.

We measured how fast that bites, in a Fourier band of 64 modes per axis. For λ = 1.7, one zoom step
leaves **342** modes alive and the second step leaves **zero**. For λ ≈ 1.6487 (an irrational ceiling
from the literature) the first step already leaves zero. Control: λ = 1 — no zoom at all — leaves
2.1 million modes alive forever, so the check works.

So (D) cannot be attacked with a torus-native object. You have to take the ℝ³ object and **wrap it**.
That is where the bill is.

## The bill

Wrapping means summing infinitely many copies of your profile, one per lattice site. If the profile
decays like distance^(−α), the copies sum like Σ|Lk|^(−α) over the 3D lattice, and that converges
only when **α > 3**.

We measured it rather than quoting it. Using shell increments (a running total of positive terms is
increasing whatever α is, so its slope can't detect convergence; the *increment's* exponent flips
sign exactly at the threshold), out to a truncation radius of 96 lattice spacings, the measured
threshold is **α = 2.996995** — the exact 3, to a tenth of a percent. Worst error anywhere in the
table: 0.00462.
At α = 3 exactly it is logarithmically divergent, adding a near-constant 8.71 per doubling.

Now put both obligations in the same unit, the profile's certified far-field decay exponent α:

| | §4 (bounded energy) | wrapping (this leg) |
|---|---|---|
| α required | **1.5** | **2.997** |
| α available, a priori | 1.0 | 1.0 |
| **deficit** | **0.5** | **1.997** |

**The deleted obligation comes back at 3.99× the deficit.** Making the torus bigger does not help:
the L-dependence is a pure prefactor, measured exponent −1.0000000000000002 against a predicted −1.

## Unless you cut first — in which case §4's work never left

The realistic route is: cut the profile off at radius ρ, *then* wrap. Do that and the wrapping bill
vanishes (with a box wider than the support, the copies don't overlap at all — contamination measured
**exactly 0.0**, and 4× the cell's own field strength when we deliberately shrink the box, so the
check can fail).

But cutting off is *precisely* the work leg 381 already priced. Every number carries over unchanged,
including the one that hurt: the **critical L³ tail does not shrink**, 326.875 per decade of window,
constant to 7 parts in 10¹⁰.

So the sharpest way to say what (D) does:

> **(D) deletes the acceptance test, not the work.**

## And it re-opens the thing we were proudest of

`CLAY_OBLIGATIONS.md` §2 — the rigidity screen, four theorems from the literature that could have
killed our object and don't — is described there as *"the programme's strongest position."*

We machine-read all four against their landed records, by a rule fixed in writing before any number
was computed:

| row | verdict |
|---|---|
| NRS 1996 / Tsai | ℝ³-only |
| Chae–Wolf / Pineau–Vicol | ℝ³-only |
| Chae–Tsai | ℝ³-only |
| Morrey (Jiu–Wang–Wei) | ℝ³-only |

**Four of four. Zero clearances carry to the torus.** Two of them are ℝ³-only not because of the
ambient space but because the *class of object* they talk about is defined by the zoom that the torus
doesn't have. A torus target would need that whole screen rebuilt against a periodic-rigidity
literature we have never searched. (Planted control rows come out "carries", both directions, so the
rule isn't just saying ℝ³-only to everything.)

## The credits, at full strength

It would be dishonest to list only the debits.

* **(7) really is gone.** Measured, not asserted.
* **§1's named obstruction points the other way.** The reason our profile-existence route is stuck is
  that every periodic-orbit certification method we could locate closes its tail estimate against a
  **compact** domain: census of **6** compact/periodic instances, **1** unbounded (stationary, 1D,
  different machinery), **0** unbounded periodic-orbit at any weight. A torus is the domain those
  methods want. The catch, stated plainly: that credit is collectable only by an object that *lives*
  on the torus, and the rigidity above says no such exact object exists. We report both and net
  neither.
* **Pressure non-locality is not the torus obstruction either.** The image-pressure magnitude sum is
  log-divergent, but on a cubic lattice the **signed** sum cancels shell by shell to **2.8e-17**.
  Break the symmetry and it jumps to 0.3458, so the cancellation check is real.

## Where that leaves it

Statement (D) is neither the free lunch nor a dead end. It removes a genuine Clay acceptance
condition and sits on the favourable side of our §1 domain census; it also empties the rigidity screen
to zero clearances, leaves the cutoff analysis exactly where it was, and — if you wrap the uncut
profile — charges the deleted obligation back at four times the deficit.

**Ceiling: Tier 2.** §6's two no-method obligations stay open in every branch. No link of the
`L1 → L4` chain moved. **Clay stays ~0.05%.**

**No retarget recommendation is made here. The decision is the user's, and this leg makes none of
it.**

*Numbers: `writeup/data/p2_route_dtor_v1.json`. Full derivation:
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDTOR_V1.md`. Figure: fig106.*
