# The wall we were measuring was a shadow of the wall that was there

*Route-WV, leg 59. Figure: `writeup/figures/fig58_weight_repairs_v2.png`. Data:
`writeup/data/p2_weight_repairs_v2.json`. Runner:
`experiments/p2_weight_repairs_v2.py`.*

## The setup, in one paragraph

We have a number that scores a function space. Given a weight — the thing that decides
what "small" means for the Newton–Kantorovich argument — the number is
`log10(Y_0/budget)`, and it is negative exactly when the certificate closes. Before
letting a search loose on it, we froze a six-property viability gate and asked whether
the number is safe to optimise at all. It answered FAIL 4/6 (leg 49). Two named
repairs moved it to 4/6 with better internals (leg 50): the fraction of weights
returning a finite score went 0.775 -> 0.875 against a 0.90 floor, and the worst
defect-tracking slope error went 0.366 -> 0.342 against a 0.05 ceiling.

Leg 50 left a note naming the suspect for the first of those: the wall we were
measuring is a **1-D slice of a 2-D boundary**, so weights were being scored against
the wrong geometry. This leg models the wall in both weight factors and re-runs the
frozen gate. The gate does not move. Repairing the fitness is allowed; moving the
goalposts is not.

## What the wall actually is

The weight is a product of two algebraic factors,
`nu(X) = (1+(X/L)^2)^(p/2) (1+(X/l)^2)^(q/2)`, plus two scalar weights on the border
rows. The old model watched one number: the far-field power `p+q`. Below a measured
crossing, `Z_1 >= 1` and no certificate exists at any residual, so the box excluded
everything with `p+q` under that line.

But in this float rehearsal `M = I - A·DF` is roundoff, and

    Z_1 = max_i w_i Σ_j |M_ij| / w_j  ~  ε · κ · (max_i w_i / min_j w_j),

which is governed by the weight's **dynamic range**, not by its far-field power. Two
weights with identical `p+q` do not share a range as soon as the two factors carry
different scales — the weight then dips or peaks *inside* the domain — and the border
weight `w_l` enters the range too. The admissible set is a level set of the range: a
curve in the `(p,q)` plane. The 1-D model was that curve's intersection with one line.

Panel (a) of the figure is the whole argument. Four hundred in-box weights, red where
`Z_1 >= 1`. The horizontal green line — the 2-D wall — separates the colours. The
vertical purple line — the 1-D wall — runs straight through the middle of both.

**The calibration is inherited, not refitted.** The 2-D wall's one number is the
log-range *at the same bisected crossing the 1-D wall already measured*
(`p_- = -3.7370` becomes `r_crit = 11.6060` decades). Nothing is fitted to this leg's
data, so the comparison below is a comparison of geometry, not of tuning.

## The known-answer window, and where the old law is simply the wrong branch

Before trusting a new geometry we made it reproduce an answer we already had. Past the
analytic wall the true profile's weighted sup norm grows like `X_max^(p+q-1)`; over a
54.6x reach that predicted x7.39 and measured x7.39. The 2-D re-derivation reproduces
it to a relative **6.7e-16**, and over a five-case battery its worst relative error is
**1.9e-10**.

The interesting part is the cases where the two laws disagree. Give the two factors
opposite-sign powers and the weight develops an interior peak; the supremum sits there
rather than at the domain edge, and `X_max^(p+q-1)` is not merely imprecise, it is the
wrong branch of the maximum. At **identical `p+q` = 1.5**, the measured growth is
x1.00 where the 1-D law says x7.39 — off by **7.39x**, with a second case off by 4.83x.
The far-field power alone does not determine the growth rate. That is the same fact
panel (a) shows, seen from the analytic side.

## What the 2-D wall buys, and what it does not

On the same 400 weights (123 of which fail):

| wall model | admits | of which fail | misclassified |
|---|---|---|---|
| 1-D (`p+q`) | 311 | **51 (16.4%)** | 68 |
| 2-D (log-range) | 278 | **2 (0.72%)** | 3 |

A **22.7x** reduction in misclassification, from a model with no new free constant.

Then the frozen gate, thresholds untouched:

- **P2 (finite fraction): 0.875 -> 0.975**, against the 0.90 floor. **Passes.** Exactly
  one roster weight is left without a score.
- **P3 (defect tracking, worst |slope-1|): 0.342 -> 0.342.** Unmoved to sixteen digits,
  against the 0.05 ceiling. **Fails.**
- P1, P4, P5, P6 unchanged and passing.

**Verdict: FAIL, 5/6.** The gate's question was "does it pass 6/6". The answer is no.

## The part worth more than the pass we did not get

P3's number did not move by a hair, across two rosters that share almost no weights.
That is not a coincidence, and it is not the wall's fault. The defect probe gives each
weight an upper limit on the perturbation `ε` — leg 50's own repair, `ε <= C/||A||_w`
— and *no lower limit*. But `Y_0(ε)` stops tracking `ε` once the perturbation falls
under the roundoff already sitting in `A·F(z*)`, at

    ε_min(w) = Y_0(z*, w) / max_i w_i |d_i|.

So every weight has a probe **window**, and the fitted slope is a function of that
window's width rather than of the weight: Spearman **-0.878** over the resolved
weights. Five-decade windows fit slope 0.999. Three-decade windows fit 0.83. Two-decade
windows fit 0.658 — the same 0.658, to five digits, for five different weights. P3 has
been measuring the probe's noise floor.

That is a defect in the fitness's **definition**, not in the box a wall model draws.
Which is exactly what the gate's no-branch pre-committed to concluding: Stage B's
fitness is dead as parameterized, and a future B proposal has to change what the
fitness *is*, not where its wall sits.

## No GA was run, and a pass would not have been a route

`plan_of_record.py` bans GA compute on an unvalidated fitness on **either** branch of
this gate. None ran here.

And the caveat this leg is required to carry: leg 54 measured the shape of `A` dead on
top of leg 53's split and leg 52's space, so even a 6/6 here would have unblocked a
stage whose three degrees of freedom are all separately measured worthless for this
operator. A 2-D wall is worth having because it is a measured geometry of a search
space. It is not a route to a certificate, and nothing here says anything about
Hou–Luo: the substrate is the a=0 CLM linearisation, closed form since 1985, and the
arithmetic is float.
