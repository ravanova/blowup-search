# The other half of the gap: what "the operators are exact data" was hiding

*Route-TN v1, leg 56. Gate answered NO. Figure: `fig51_route_tn_v1_consistency.png`.
Data: `writeup/data/p2_route_tn_v1_consistency.json`.*

---

## A theorem that says exactly what it does not say

Six legs ago this project got a real result: `solver/interval_certificate.py` closes a radii
polynomial on the target profile `HL_S2_nonsymmetric`, in interval arithmetic, at
n = 201, 401 and 801. Not a float rehearsal — a rigorous enclosure.

And it came with an unusually honest docstring. Here is the theorem it claims, in its own
words:

> Let `H`, `D` be the stored float matrices ... **with THOSE matrices as exact data**. Then
> ... there is a TRUE ZERO of that polynomial system within `r` of the stored float iterate.
>
> **WHAT IT DOES NOT SAY.** Nothing about the continuum profile. The gap between the discrete
> system and the PDE is two further terms — the consistency of `(H, D)` with the operators
> they discretise, and the far-field tail beyond `X_max` — and neither is bounded here.

Two named gaps. Legs 51–53 spent themselves on the second one, in a different (Fourier)
basis, and it ended badly — the block coupling of the approximate inverse came out at 43
where it needed to be under 1.

The first gap had never been measured at all. `H` and `D` are *discretisations*: `H` of the
Hilbert transform, `D` of `∂_X`, on a `sinh`-graded grid reaching |X| ≈ 745. The certificate
treats them as exact. This leg asks what that costs.

**It is not the banned move.** "Closing the truncation gap by extending the domain" is
banned in this repository — leg 47 measured that trend and it runs the wrong way. The domain
here is *frozen* at X_max = 745.24 in every single run. The quantity is a discretisation
defect at fixed reach, and the far-field term is computed only so it can be subtracted off
and reported in its own column.

---

## First: the quantity does not exist until you say what it means

The obvious phrasing — "bound ‖H_disc − H‖" — is not a thing. `H_disc` is an
n × n matrix taking grid vectors to grid vectors. `H` takes functions to functions.
Subtracting them is a type error.

The difference only becomes a number once you name a **class of functions**, and then the
number depends on the class you named. A function wiggling faster than the local mesh has an
enormous defect; a smooth one has a tiny defect. Same grid, same matrix. So this leg reports
the defect as a *curve* over a named class (panel C), never as a single number wearing an
operator norm's clothes.

The class is the rational pair whose Hilbert transform, **truncated** Hilbert transform and
derivative are all closed-form — which happens to include the exact CLM profile the repo
already tests against.

## Then: the two operators turn out **not** to be the same operator

> **I got this backwards on the first pass, and the correction is the most useful thing in
> the leg.** My first draft said `H_disc` and `D_disc` were the exact Hilbert transform and
> the exact derivative of *the same* spline interpolant, so both defects were "one
> interpolation error through two operators". That is false, review caught it, and the
> ablation further down had already contradicted it — I just hadn't reconciled the two.

Reading `solver/line_hilbert.py` closely does change the shape of the problem, but not the
way I first wrote it down. `line_hilbert_matrix` is indeed **not a quadrature rule**: it
represents the data by a C¹ cubic spline and applies the *exact* Hilbert transform of that
spline.

**But it builds source columns for interior nodes only.** The two endpoint basis functions
are dropped. So the spline it actually transforms is not the natural-spline interpolant
`Π f` that `slope_matrix` differentiates — it is `Π⁰ f`, the one pinned to **zero value and
zero slope at ±M**:

```
H_disc f  =  H(Π⁰ f)          D_disc f  =  (Π f)'
                  ^^ a different, endpoint-zeroed interpolant
```

Handed a function that is ≈ 1/X out there, `H_disc` silently sets it to zero over the two
edge cells. At n = 201, node 1:

| | value |
|---|---|
| `H_disc f` | −1.8584719686e−03 |
| `H(Π⁰ f)` by quadrature | −1.8584719686e−03 — agrees to **2.6e−15** |
| `H(Π f)` by quadrature | −1.4880639571e−03 — differs by 3.7e−04 |
| the true reference `H_M f` | −1.4885580e−03 |

So the defect is really two defects stacked:

```
H_disc f − H_M f  =  [endpoint zeroing]  +  [genuine interpolation error]
                      4.70e−03, flat        4.42e−07, order 1.95
```

The artifact is **the entire measured defect** (99.99% of it), which is exactly why the total
refuses to converge. And the genuine interpolation part is still why `H` cannot be bounded
from `‖e‖_sup` the way `D`'s can — the Hilbert transform is unbounded on `L^∞`, so it has to
be *evaluated*. Hence the closed forms, and hence the rigorous `log` and `arctan` this leg had
to build (series with proved remainders — `np.log` carries no ULP guarantee this project is
entitled to assume).

## The number the defect has to beat, and why it is so small

A consistency defect is an addition to the residual. The certificate can absorb

```
τ  =  budget / ‖A‖_w
```

and nothing more. At n = 801 the budget is 3.5547e−10 and ‖A‖_w is 1.5418e+04, so

**τ = 2.31e−14.**

That is a brutally small number, and it is *the certificate's own*, not one this leg chose.
It is small because `Z₂ ≈ 1.4e+09`, and the budget goes like `(1−Z₁)²/2Z₂`. Note also that
τ is the **friendliest possible** threshold — it throws away every amplification the real
perturbation would carry. A defect that fails against τ fails against the truth by more.

*(The budget and ‖A‖_w re-derive to all printed digits from leg 46/50's stored run. `Y₀`
itself does not: 9.97e−12 here against 7.35e−12 stored, a Newton iterate landing slightly
differently. It does not enter this leg's comparison, but it is on the figure so nobody has
to take that on trust.)*

---

## The answer

| at n = 801 | defect | vs τ | order per doubling |
|---|---|---|---|
| derivative `D` | 4.274e−07 | **1.85e+07 ×** | **4.01** |
| Hilbert `H` | 4.704e−03 | **2.04e+11 ×** | **0.00** |
| *(far-field truncation — the other gap)* | 2.626e−02 | 1.14e+12 × | −0.22 |

**The gate answers NO, by seven and eleven orders of magnitude. And the two fail for
completely different reasons — that is the actual content of the leg.**

**The derivative behaves perfectly and is simply far too big.** It converges at order 4.01,
4.03 — textbook natural-spline order, measured, not assumed. It is just starting from
4.27e−07 and needs 2.31e−14. At order 4 that is n ≈ 52,000, i.e. a dense N = 104,000 interval
system. Not reachable, but honestly diagnosed: nothing is *wrong* with `D`.

**The Hilbert defect does not converge at all.** 4.7287e−03 → 4.7131e−03 → 4.7041e−03. A
factor of **1.005 over a fourfold refinement.** Refinement is not a lever here. No `n` closes
this.

## Why — ablated, not asserted

The defect sits at the last interior node, next to the cut. `line_hilbert_matrix` builds
source columns for **interior nodes only**, so the function it actually transforms is the one
that vanishes, with vanishing slope, at ±X_max. Handed a function that is ≈ 1/X out there,
it silently sets it to zero over the two edge cells.

That is a story, and this repository has learned the hard way (lesson 90) not to trust a
control that could not have come out differently. So: two test families with **identical
interior smoothness and identical resolution demands**, differing only in their value at the
cut by a factor M/a ≈ 1490. Nothing in the code path knows which one it has.

| | `H` defect | `D` defect |
|---|---|---|
| decays like 1/X at the cut | 4.704e−03 | 4.274e−07 |
| decays like 1/X² at the cut | 3.130e−06 | 3.866e−07 |
| **ratio** | **1503×** | **1.11×** |

The same dial that moves `H` by three orders of magnitude moves `D` by eleven percent, and
the collapse factor matches M/a to within 1%. The mechanism is measured.

**And this table is what should have told me §3 was wrong.** A dial that leaves interior
smoothness completely untouched cannot move a *pure interpolation error* by 1503× while
moving the derivative's by 1.11%. Under the corrected reading it is exactly what has to
happen: the dial changes `f(±M)`, which is precisely what the endpoint-zeroing term is
proportional to and what the interpolation term barely notices. The evidence was sitting in
my own results section, contradicting my own mechanism section, and I shipped both.

And the enclosures are enclosures: width/value is 6.34e−08 for `D` and 1.15e−13 for `H`. These
bounds are not their own evaluation error (lesson 86) — the risk that was flagged as this
leg's central one, and it did not bite.

---

## What this does and does not mean

The gate's no-branch was written before the run and it is honoured: **the collocation
realization cannot carry `L1`, and the coefficient basis is the only lane left for it. No
grid-basis repairs are proposed here** — not the boundary-basis fix the mechanism section
obviously invites, not anything else. The `H` artifact is *why* the no is sharp, but the no
does not depend on it, in two independent ways: even with the Hilbert defect deleted
outright, the derivative alone still needs n ≈ 52,000; and even with the *artifact* deleted
instead, leaving only the genuine interpolation error, the Hilbert side needs **n ≈ 4.4
million**, because order 1.95 is so much weaker than order 4. Correct attribution makes the
answer more negative, not less.

What genuinely changed is the reading of that honest docstring. The two named gaps were
listed as peers. They are not. One of them — the far field — has been the subject of three
legs. The other one, measured here for the first time, is **larger than the certificate's
entire budget by eleven orders of magnitude**, and the far-field term is larger still. The
certificate closes with margin to spare *in the discrete world*, and that margin has no
purchasing power at all against either bridge to the continuum.

Nothing here is a statement about `HL_S2_nonsymmetric` being certified, about the far-field
gap, or about the method in the coefficient basis. **No link of the L1→L4 chain moved.**
In 56 legs, none has. Clay stays at ~0.05%, behind Walls 1 and 2.

The novelty pass ran first and returned `PROCEED_NARROW` with **nothing banked**: rigorous
error bounds for spline-based Hilbert transforms inside computer-assisted proofs are
established practice in exactly this literature — Chen–Hou–Huang do it on these very models.
The links are in `writeup/novelty/leg_56.md`.
