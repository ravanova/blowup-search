# Route-E v1 — the rescaled gCLM flow has no eigenvalue available for a Hopf bifurcation

*Phase-2 P2, Route E (the DSS lane), leg 1. Figure: `writeup/figures/fig34_p2_route_e_v1_spectrum.png`.
Data: `writeup/data/p2_route_e_v1_spectrum.json`. Module: `solver/rescaled_spectrum.py`
(gates: `test_rescaled_spectrum.py`, 7/7).*

**Level-1 numerics plus one small exact computation. Not a certificate, not a proof, not
Clay progress. Plain float64 throughout; nothing here is interval-enclosed.**

---

## 0. Why this leg exists, and what it was allowed to conclude

Route D spent sixteen legs on link **L1** of the chain — a certified self-similar blow-up
profile for a 1D toy model. Leg v15 (the literature check) found that L1 is very probably
occupied territory: computer-assisted interval/Newton–Kantorovich certification is routine
for the groups working this family. That did not invalidate a single measurement, but it did
re-price the lane, and it promoted a different item to "the swing":

> **Nečas–Růžička–Šverák (1996), extended by Tsai**: exactly self-similar blow-up for 3D
> Navier–Stokes in the natural scaling class is *ruled out*. Therefore the entire
> "find a self-similar profile and certify it" template cannot be pointed at NS as posed.
> The candidate class that survives is **discretely self-similar (DSS)**.

In dynamic-rescaling variables the translation is exact and it is the reason this leg is
cheap:

| object | in rescaled variables |
| --- | --- |
| self-similar blow-up | a **fixed point** of the rescaled flow |
| DSS blow-up | a **periodic orbit** of the rescaled flow |

A global search for a periodic orbit is expensive and needs somewhere to start. But there is
one mechanism that would both *produce* a periodic orbit and *tell you where it is*: a **Hopf
bifurcation** off the self-similar branch — a complex-conjugate pair of eigenvalues of the
linearized rescaled flow crossing the imaginary axis as the model parameter `a` moves. If
such a pair exists, the DSS lane opens with a concrete starting point. If there is no
eigenvalue capable of crossing, that particular route is closed and the lane has to be
entered some other way.

That is a question about a spectrum, and a spectrum is one dense eigenvalue solve. This leg
is the answer.

**Gate-check, answered rather than re-pasted.**
*(a) Which link does this move?* **None.** It does not advance L1→L4. It is lane scoping:
it decides whether the cheapest entrance to the DSS lane is open.
*(b) Is another L1 leg better?* No — v15 re-priced L1 downward and named this as the swing.
*(c) Is there a cheaper experiment that would tell us the route is dead?* **This was it**, and
it is the reason the leg was worth doing before any DSS search machinery was built.

---

## 1. The flow, and the one modelling choice in it

gCLM on the line: `omega_t + a u omega_x = omega u_x`, `u_x = H(omega)`. Dynamic rescaling
`omega(x,t) = A(t) Omega(X,tau)`, `X = x/L(t)`, `dtau/dt = A` gives

```
Omega_tau = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X ,   U(X) = int_0^X H(Omega) dX'
```

The two gauge functions `(c_omega, c_l)` carry the two scaling freedoms. This leg fixes
`c_l = 1` — **a choice, and it is stated as one** — and determines `c_omega` from the
normalization that freezes the origin slope. Requiring `(Omega_tau)_X(0) = 0` for odd `Omega`
gives, exactly,

```
c_omega[Omega] = 1 + (a - 1) H(Omega)(0) .                                        (N)
```

At `a = 0` this **is** the value-based normalization the project has used since Spike 0
(`solver/gclm_rescaled.py`), so this is the same flow continued in `a` rather than a new
convention. Worth saying out loud: the project's existing residual used `c_omega = 1 - H(Omega)(0)`
at every `a`, and that version has **no fixed point at all** for `a != 0` — differentiating the
residual at the origin gives `R_X(0) = -a H(Omega)(0) Omega_X(0) != 0`. (N) is the repair, and
it is forced, not chosen.

With `c_l` fixed, **dilation survives as a symmetry**: `Omega(X) -> Omega(X/mu)` is again a
fixed point, and `H(Omega)(0)` is dilation-invariant so (N) is untouched. That is where the
exact zero eigenvalue below comes from.

---

## 2. The discretization: the far field costs nothing here

Compactify with `X = tan(theta/2)` and expand the **odd** profile in sines. Three operators
are then exact on the whole line, with no domain truncation and no quadrature:

```
H(sin k theta) = -cos k theta + (-1)^k
X d/dX         = sin(theta) d/d theta          <- the DILATION term is bounded and exact
d/dX           = (1 + cos theta) d/d theta
```

The `(-1)^k` is not decoration: `H^2 = -1` only modulo constants on the line, and that
constant is exactly what makes `H(Omega)` vanish at `X = infinity`.

The velocity is exact too. Writing `N_k(t) := ((-1)^k - cos k t)/(1 + cos t)`, the three-term
identity `2 cos t cos kt = cos(k+1)t + cos(k-1)t` gives

```
N_{k+1} = -2 N_k - N_{k-1} - 2 cos k t ,      N_0 = 0,  N_1 = -1,
```

so **every `N_k` is a trig polynomial** — the `1 + cos t` in the denominator always cancels —
and `U = sum_k b_k int_0^theta N_k` is elementary. There is no quadrature anywhere in the
build. (Gate 2 checks this as a polynomial identity out to `k = 30`, not merely at the anchor,
because a three-term recursion is exactly the kind of thing that drifts silently.)

**The `a = 0` fixed point is a single mode.** `Omega_0 = -sin theta = -2X/(1+X^2)`, with
`H(Omega_0) = 1 + cos theta = 2/(1+X^2)` and `c_omega = -1`. It nulls the residual to
**1.1e-16**, which is the module's first gate. Sixteen Route-D legs worked in this same
compactified variable; this is the first time the *self-similar* (dilation) anchor has been
written in it, and it is one Fourier mode.

---

## 3. Two eigenvalues are exact, at every `a`, and they are symmetry

Before computing anything, write down what has to be there. Let `L` be the linearization of
the flow at a fixed point. Then

```
L (X Omega_X) = 0                              (dilation)
L (Omega)     = -Omega + X Omega_X             (amplitude)
```

The first is the dilation symmetry: the orbit is a curve of fixed points, so its generator is
in the kernel. The second follows by substituting the profile equation into `L(Omega)` and
using (N):

```
L Omega = (H Omega) Omega + (a-1) H(Omega)(0) Omega - a U Omega_X + [profile equation]
        = -c_omega Omega + X Omega_X + (c_omega - 1) Omega   =  -Omega + X Omega_X .
```

So `span{Omega, X Omega_X}` is invariant with matrix `[[-1,0],[1,0]]`, giving

> **lambda = 0 (dilation) and lambda = -1 (amplitude), for every `a`.**

These are a Jordan-like pair, they are present at every parameter value, and **they carry no
dynamical information**. Any DSS-relevant eigenvalue has to be something else. Rather than
trust the derivation, `structural_pair_defect` measures both identities; gate 4 reports
**1.2e-15 / 8.9e-17** at `a = 0` and **2.0e-13 / 4.6e-15** at `a = 1/2`, and the `2x2` block
itself is exact to **6.1e-16**.

---

## 4. At `a = 0` the rest of the spectrum is known in closed form

Set `w = e^{-i theta}` and `Z = H Omega + i Omega`, so the anchor is `Z_0 = 1 + w`. Writing
the `a = 0` linearization in `s = delta Z`:

```
L s = w s - ((w^2 - 1)/2) s_w - s(w=1) (1 + w) .
```

For `s(1) = 0` the homogeneous problem `L s = lambda s` is a first-order ODE and integrates:

```
s_lambda(w) = (w - 1)^{1 - lambda} (w + 1)^{1 + lambda} .
```

The verification is one line — `((w^2-1)/2) s_w = s (w - lambda)`, hence `L s = w s - s(w-lambda)
= lambda s` — and admissibility does the rest:

* `s -> 0` at `w = -1` (i.e. decay at `X = infinity`) needs `Re lambda > -1`;
* `s` bounded and vanishing at `w = 1` (i.e. at `X = 0`) needs `Re lambda < 1`.

So the `a = 0` linearization carries a **continuum of eigenvalues filling the strip
`-1 < Re lambda < 1`**, and every one of its eigenfunctions carries a **fractional power**
`(w-1)^{1-lambda}` at the origin. Demanding analyticity at `X = 0` forces `1 - lambda` to be a
non-negative integer, and combined with `Re lambda > -1` that leaves exactly `lambda = 0` and
`lambda = -1` — **the two structural modes and nothing else.**

Two things follow, and they are the reason the rest of this leg is trustworthy:

1. **The `a = 0` answer is known independently of any discretization.** That is the anchor
   the numerics is gated against.
2. **A convergence filter is mandatory, not decoration.** The discrete eigenvalues are the
   ones that stop moving under refinement; the continuum is the part that never does.

The numerics reproduces it exactly: of `K = 96` eigenvalues, **exactly one sits off the
imaginary axis (`lambda = -1`, isolated to 1e-14)** and the other 95 are pinned to the axis to
1e-9 and move with `K`. Under the `K = 96 -> 144` filter at tolerance `1e-3`, **exactly two
survive: `0` (distance 8e-16) and `-1` (distance 6e-15).**

---

## 5. The branch: `alpha(a)` is an output, and it runs away

Following the fixed point from the exact anchor by continuation in `a`, the far-field decay
exponent is not a parameter but a result. The far-field balance is
`c_omega Omega = (X + a U_inf) Omega_X`, so

```
Omega ~ X^{-alpha},   alpha(a) = -c_omega(a).
```

`alpha` starts at 1 (CLM) and **increases with `a`**, and `1/alpha` extrapolates linearly to
zero at a finite `a` — the profile's tail becomes infinitely steep and the branch, as posed on
the whole line, ends. This is the self-similar analogue of what Route-D v12/v14 found for the
*traveling-wave* object (where the profile ends at a finite radius `X_c`), and it is a
different object, so the agreement of the two pictures is a check rather than a repetition.

**One consequence matters for everything numerical here.** A branch point of order `alpha` at
`X = infinity` means the sine coefficients decay *algebraically*, and so does everything built
from them (measured: residual `~ K^-2` at `a = 0.3`). The exceptions are the values of `a`
where `alpha` is an **odd integer**, where `Omega ~ (pi - theta)^alpha` is smooth and the method
is spectral again. Two of them are visible:

* `a = 0`, `alpha = 1` — exact, one mode;
* **`a = 1/2`, `alpha = 3` — exact to 11 digits** (`c_omega = -3.0000000000098` at `K = 128`,
  residual `1.4e-14` at `K = 192`, geometric coefficient decay).

The `a = 1/2` point is *found*, not assumed: a fine scan of the fixed-point residual in `a` at
fixed `K` shows a single sharp dip, ten orders deep, exactly there. **Novelty unchecked** — an
exact-looking exponent at `a = 1/2` in this family is precisely the sort of thing that is
folklore to people who work on gCLM/De Gregorio, and the literature check is still blocked on
PDF access (v15's finding, unchanged).

Because of this, **every quantitative spectral statement in this note is quoted at `a = 0` or
`a = 1/2`**, where the fixed point is analytic and the method is spectral. The generic-`a`
sweep is reported with its (algebraic) accuracy attached, and the verdict is checked against a
tolerance ladder rather than a single cut.

---

## 6. The verdict

Sweeping `a` and applying the `K = 96 -> 144` filter:

> **At every `a` on the branch, the only grid-converged eigenvalues are `0` and `-1` — the two
> exact symmetry modes. There are no others, at any tolerance from `1e-4` to `1e-1`. Nothing
> is available to cross the imaginary axis, so there is no Hopf bifurcation off the gCLM
> self-similar branch.**

The count is stable across the tolerance ladder, which is what makes "exactly two" a
measurement rather than a choice of cut: loosening the cut by three orders of magnitude does
not admit a third eigenvalue, and tightening it does not remove either of the two.

### 6.1 The positive control — the part that makes the negative mean something

"Only two survived the filter" is evidence only if the filter would have reported more. So the
same filter is run on the same operator with a smooth localized potential added — a bump that
binds states in a transport operator. It returns a converged eigenvalue at **`+1.083`**:
in the **right half plane**, and **1.08 away** from anything the plain operator has.

**The instrument can see an unstable eigenvalue. There is not one.**

### 6.2 What this does *not* say

* It does not say gCLM has no DSS solution. It says a DSS solution in this family is **not
  born from a Hopf bifurcation off the self-similar branch that continues from CLM**. A
  periodic orbit can exist without a nearby fixed point that spawned it.
* It does not say anything about NS. gCLM's scaling structure is not NS's, and the whole
  reason DSS is interesting for NS is a theorem about NS.
* The essential spectrum's **location is norm-dependent**, and what is measured here is the
  spectrum of a *discretization*, filtered for grid-independence. A discrete eigenvalue
  embedded in the continuum can be missed by any such method. The `a = 0` closed form is the
  only place where the answer is known independently — and there, it agrees.
* One more honest caveat: the verdict is computed in **one gauge** (`c_l = 1` plus (N)).
  Changing the normalization changes the flow by multiples of the symmetry generators, which
  moves the symmetry eigenvalues but not the transverse spectrum — the argument is standard,
  but it is an *argument* here, not a measurement.

---

## 7. What this cost, and what it bought

Cost: one module, one experiment, seven gates. Bought:

1. **The cheapest DSS mechanism is closed** for the 1D family, with a positive control behind
   the negative. That is exactly the "is there a cheaper experiment that would tell us the
   route is dead" item from the gate-check, executed before any search machinery was built.
2. **The self-similar branch of gCLM in the compactified variable**, with an exact one-mode
   anchor, an exact velocity operator, and a Newton solve that follows the branch.
3. **`alpha(a)`**, the far-field decay exponent map, as an output.
4. **The analytic resonance at `a = 1/2` (`alpha = 3` to 11 digits)** — novelty unchecked.
5. **The closed-form `a = 0` continuum**, which is a small exact result about the CLM
   self-similar linearization and the anchor every later spectral claim can be gated against.

### Where this sits relative to Clay (re-answered, not re-pasted)

Unchanged and stated plainly: **nothing here is a step whose success would resolve the Clay
problem.** This leg does not move L1, L2, L3 or L4. What it does is stop the project from
spending several legs building a DSS search around a mechanism that does not exist in the
family where its tooling lives. The two structural walls (a search programme can only ever
argue *for* blow-up; rigorous certification technology only reaches toy models) are untouched.
Overall odds ~0.05%, unchanged.

The honest summary of the DSS lane after one leg: **the lane is not closed, but the cheap
entrance is.** Entering it now costs a real build — a periodic-orbit search in the rescaled
flow, with no fixed point nearby to seed it — and that is a much bigger commitment than this
leg was. Whether it is the right one is the next decision, and it should be taken against the
alternatives (the Hou–Luo critical-viscosity map; the L1→L2 port to 2D Boussinesq), not by
default.

---

## Appendix — new lessons this leg paid for

**(46) A symmetry audit is cheaper than an eigenvalue solve, and it can predict the whole
answer.** Two of the eigenvalues found here were derivable in five lines from the two
symmetries of the flow. Doing that *first* meant the numerical spectrum arrived with its two
expected members already named — so "exactly two survived" read immediately as "nothing but
symmetry", instead of looking like a result. **Enumerate the symmetry modes before computing a
spectrum; they are the null result's baseline.**

**(47) A null result needs a planted positive, not just a control.** Banked lesson (2) says
"ablate to attribute" and (9) says "build the adversary". This is the third member of the
family: when the finding is *absence*, the instrument must be shown to detect a *presence* of
the same kind. Planting a bound state and recovering it at `+1.083` costs three lines and is
the difference between "there is no unstable eigenvalue" and "we did not find one".

**(48) When you generalize a gauge, re-derive it — do not extend it.** The project's existing
normalization `c_omega = 1 - H(Omega)(0)` is correct at `a = 0` and had been carried at every
`a` in the same function. With `a != 0` it admits **no fixed point at all**: the residual's own
derivative at the origin is nonzero. One line of algebra at the origin catches it. **A gauge is
a condition, and a condition derived at one parameter value is not a condition at another** —
which is banked lesson (29) ("a constant is attached to a point, not to a problem") wearing
the gauge's clothes.

**(49) The regularity of the object sets the convergence rate of everything built on it, and
it can vary with the parameter.** Here the far-field exponent `alpha(a)` is an output, and it
is an odd integer at exactly two points on the branch. At those two points the method is
spectral and at every other point it is second-order — a 10-order accuracy swing driven by
nothing but the parameter. **Find where your object is smooth and quote your sharp numbers
there, rather than quoting one accuracy for a whole sweep.**
