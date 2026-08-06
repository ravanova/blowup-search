# The certificate that could not close on a solution we already had

**Route-M2CI, leg 187. Gate answered NO.**

Leg 125 left a lead lying on the table. It had gone looking for a viscous (γ = 2) blow-up
profile for the generalized Constantin–Lax–Majda equation, answered NO on both of its
clauses, and in the process transcribed a different object entirely: the profile Chen's
theorem actually converges to, which is **inviscid**. Chen's own words, section 1.5: *"we
study the inviscid problem, i.e. ν = 0."* Call it **Object A**:

$$\Omega(X) = \frac{-2bX}{(X^2+b^2)^2}, \qquad b^2 = \tfrac38, \quad c_l = \tfrac13, \quad c_\omega = -1.$$

Leg 125 measured Object A against the radii-polynomial *budget* at nine rows and found it
comfortably inside — the residual bound $Y_0$ came in between **1.325e-09** and
**5.800e-05** of the available budget. That looks like a certificate waiting to be written.
Chen's proof of this profile is analytic, not computer-assisted, and leg 125's literature
pass found no computer-assisted proof of any self-similar gCLM profile at this parameter.
So the prize on offer was real: upgrade an analytic proof to a computer-assisted one.

This leg went to write that certificate. It does not close. And the reason it does not close
is the interesting part.

## Say the disappointing thing first

Two things must be said up front, because both were written down *before* any number in this
leg was computed (`writeup/novelty/leg_187.md`, committed ahead of the construction).

**One: this is inviscid, and it says nothing about the viscous question.** Object A has
ν = 0. The "missing rung" — whether a *dissipative* gCLM profile exists and can be certified
— is exactly as open as leg 125 left it. Nothing here touches it. The γ = 2 in the route name
refers to the dissipation exponent of the *dynamics* Chen's theorem is about; the *profile*
is inviscid.

**Two: Object A is already published in closed form.** Not just by Chen — Huang–Qin–Wang–Wei
(arXiv:2305.05895) give the whole branch $a \le 1$ in closed form. So a certificate centred
on Object A has $Y_0$ **exactly zero**, because the centre *is* an exact solution. It would
prove no existence that the closed form did not already hand us. The novelty pass flagged
this as a pre-emption before the module existed, and it means the YES branch of this gate was
always going to be hollow.

Which makes the NO more useful than the YES would have been.

## What actually fails

Not the budget. The budget is as good as a budget can get: $Y_0 = 0$, exactly, verified in
exact rational arithmetic rather than measured in floating point.

What fails is **isolation**. The radii-polynomial theorem does not merely conclude that a
zero exists near your centre; it concludes that the zero is *unique* in a ball. Object A is
not alone in any ball. It sits on a one-parameter continuum of exact solutions:

$$\Psi_g(X) = -\tfrac{16}{3}\, g^{3/2}\, \frac{X}{(X^2+g)^2}, \qquad g > 0,$$

with $\Psi_{3/8}$ being Chen's profile exactly. This is the **dilation orbit** — the steady
equation's own scaling symmetry, which fixes $c_l$ and $c_\omega$ and slides the profile
through a family of length scales. We verified it the honest way: the residual's numerator is
the **zero polynomial**, in exact `Fraction` arithmetic, at five different values of $g$ —
and the control, where the amplitude is nudged by 1/100, is emphatically nonzero every time.

The consequence is not numerical, and no amount of tuning escapes it. Let $\varphi = d\Psi_g/dg$
be the tangent to the orbit. It is an exact kernel element of the linearisation: $DF\,\varphi = 0$.
So for **any** approximate inverse $A$ whatsoever,

$$(I - A\,DF)\varphi = \varphi - A\cdot 0 = \varphi \quad\Longrightarrow\quad \|I - A\,DF\| \ge 1 \quad\Longrightarrow\quad Z_0 + Z_1 \ge 1.$$

The contraction factor $1 - Z_0 - Z_1$ is never positive. Not for a better $A$, not for a
better weight, not for a finer grid, not in any space that contains $\varphi$ — which is
every space in which the centre itself has a finite norm. With $Y_0 = 0$ the radii polynomial
collapses to $p(r) = Z_2 r^2 - (1 - Z_0 - Z_1)r$, which is non-negative for every $r > 0$.
There is no radius. The certificate has nothing to conclude.

We should be clear about what is and is not ours here. That an exact self-similar CLM profile
carries a scaling zero mode is **published**: Xu (arXiv:2607.19762) states for the $a = 0$
sibling that the point spectrum is exactly $\{0, 1\}$, the scaling and time-shift symmetry
modes. We cite it; we do not claim it. What is ours is the certificate-side accounting — the
specific clause that breaks at $a = 1/2$, and the constant it breaks by.

## Two ways of checking we were not fooling ourselves

**The kernel is an operator fact, not a grid artifact.** As the grid refines, the orbit
tangent's relative defect falls — 5.21e-05 → 1.03e-05 → 3.27e-06 across n = 401, 601, 801 —
while a localised bump used as a control stays flat at 0.689. Their separation grows from
1.3e04 to **2.11e05**. Independently, the Jacobian's conditioning collapses like $n^{-6.68}$,
from 1.38e-06 down to 9.03e-12 across a sixfold range of resolution. The operator is becoming
singular in the continuum limit, exactly as an exact kernel demands.

**A trap worth naming.** The obvious numerical check of the $Z_0 + Z_1 \ge 1$ argument is to
build $A = \mathrm{pinv}(DF)$ and measure $\|\varphi - A\,DF\varphi\|/\|\varphi\|$. It comes
out at **1.03e-07** — apparently refuting the whole argument. It does not. NumPy's default
cutoff for discarding singular directions is a relative $\sim 10^{-13}$, while the near-null
direction sits at $\sigma_{\min}/\sigma_{\max} = 1.34\mathrm{e}{-10}$ — *above* the cutoff. So
`pinv` keeps it, numerically inverts a direction that is not invertible in the continuum, and
returns $AJ = I$ to round-off. Truncate it at any honest cutoff and the shadow returns to 1
from below: **0.99998** at n = 401, **0.9999990** at n = 801. We report both columns, because
the gap between them *is* the measurement.

## A second, independent failure

Even setting the kernel aside, the quadratic constant $Z_2$ does not exist as an operator
constant in this space. Across n = 201 → 1201 it grows as $n^{2.36}$, from 9.44e10 to
6.31e12 — a factor of **66.9**, monotone at every step. Any single-resolution value for it
would have been a statement about the grid, not about the operator.

## The one thing that was genuinely open

The novelty pass identified exactly one sub-question with no answer in the literature: how the
profile's far-field decay rate pairs against the far-field symbol of the self-similar transport
operator. Beyond the profile's support that operator is $L_\infty h = c_\omega h - c_l X h_X$,
which acts on $h \sim X^{-s}$ as multiplication by

$$\sigma(s) = c_\omega + s\,c_l = \tfrac{s}{3} - 1,$$

vanishing exactly at $s = 3$. And the profile's own decay exponent, **measured** off the grid
rather than asserted, is **2.999955** — with an $X^{-2}$ control measuring −1.999911, so the
measurement is real. The symbol vanishes precisely at the centre's own decay rate. The tail
inverse has norm $3/|3-s|$, which diverges as the grading approaches the only grading at which
the centre still comfortably lives in the space.

That is the same obstruction as the kernel, seen from the far field: $X^{-3}$ *is* the
homogeneous solution of the tail operator. Two clauses, one mechanism.

## So what was the lead worth?

The standard repair — bordering the symmetry with a phase condition — does work numerically:
it lifts the smallest singular value by a factor of **4.77e04** at n = 801. It is standard
practice in validated numerics and we claim none of it. But bordering certifies the
orbit-transverse *slice*, not Object A; and with $Y_0 = 0$ any bordered $Z_0 + Z_1 < 1$ would
close a polynomial asserting a zero at a point already known in closed form. The existence
content would still be nil.

The honest summary is that leg 125's budget number was correct and load-free. $Y_0$ being
small was never evidence about the clauses that decide this certificate — and we now know
that in the strongest possible form, because $Y_0$ here is not merely small but exactly zero,
the best value the framework admits, and the certificate still cannot close.

That is a shape worth remembering: *budget-under is not certificate-ready.* It is the third
time this repository has met it, and the first time with the budget pinned at zero.

---

*Figure: `writeup/figures/fig65_route_m2ci_v1_construction.png`. Data:
`writeup/data/p2_route_m2ci_v1_construction.json`. Technical companion:
`TECHNICAL_P2_ROUTEM2CI_V1.md`. Novelty pass, committed before construction:
`writeup/novelty/leg_187.md`.*
