# Route-NB v1 — we finally measured whether the thing we were trying to certify is even in the space

*Leg 55. Exploration route, not the critical path. Every number below is in
`writeup/data/p2_route_nb_v1_targetnorm.json`; the figure is
`writeup/figures/fig50_route_nb_v1_targetnorm.png`.*

---

## The sentence that had never been checked

For four legs this project has been trying to build a certificate around a 1D Hou–Luo
self-similar profile called `HL_S2_nonsymmetric`. Every one of those legs actually did its
arithmetic on a *different* object — the `a = 0` CLM anchor, a stand-in chosen because it
is exactly one Fourier mode and therefore trivially inside every function space anyone
might want.

Sitting in the project's ban list, as justification for not re-running on the real target,
was this clause:

> *the non-symmetric Hou–Luo profile is not [one basis mode], and **does not have finite
> norm in the class where the operator is least bad***

That is a claim about a number. Nobody had computed the number. It was a derivation — a
docstring formula, applied to a decay rate read off a solve — dressed as a measurement.

This leg computes it.

## What "finite norm" means here, in one paragraph

The certificate lives in a space of Fourier coefficients. You compactify the real line
with `X = tan(θ/2)`, so the whole infinite line becomes one circle, expand the profile in
Fourier modes on that circle, and ask whether the weighted sum

    ‖h‖ = Σ_k (1+k)^s · |ĥ_k|

converges. If the coefficients decay like `|ĥ_k| ~ C k^{-p}`, this is finite exactly when
**`p - s > 1`**. So the entire question — a whole clause of a ban list — is one exponent.

There is a prediction for what that exponent should be. The profile decays in physical
space like `|X|^{-α}`. Under the compactification, `X → ∞` is `θ → π`, and an algebraic
far field becomes a *branch point* of order `α` sitting at one point of the circle. Branch
points of order `α` have coefficients that decay like `k^{-1-α}`. So `p` should be `1 + α`,
and `α ≈ 0.394` for this object.

Prediction. Not measurement. The difference is this leg.

## The answer

**`p = 1.394`**, and the target's norm is **finite** for every `s < 0.394` — including
`s = 0` and `s = 0.3`, which are the two classes legs 52 and 53 actually did their work in.

It is **divergent** at `s = 1`.

Both halves are the result, and the second one is why the original clause is not simply
wrong.

## The ladder, which is the part worth reading

The instruction that binds every leg here is *report the shape of a ladder, not its
endpoint*. There were two ladders, and only one of them moved.

**The resolution ladder did nothing.** Refining the Newton grid `n = 201 → 401 → 801` moved
the exponent by `3.8e-04`. Push it to `n = 3201` and it moves in the fifth decimal. The
measurement is not resolution-limited.

**The domain ladder moved, and then stopped.** The shipped object is solved on `|X| ≤ 745`.
At that domain the measured exponent is `p = 1.369` — visibly short of the predicted
`1.394`. Extend the domain and:

| `X_max` | `p − 1` | far-field exponent, measured in *physical* space | `α = −c_ω/c_l` |
|---|---|---|---|
| 745 | 0.3692 | 0.3609 | 0.3936 |
| 5 507 | 0.3876 | 0.3795 | 0.3963 |
| 40 689 | 0.3937 | 0.3893 | 0.3974 |
| 300 651 | 0.3963 | 0.3941 | 0.3978 |

The gap between the coefficient exponent and `α` closes monotonically: `−0.024 → −0.009 →
−0.004 → −0.0015`. Three quantities measured three different ways — a Fourier fit on the
circle, a log-log fit in physical space, and a ratio of two Newton unknowns — converge on
the same number.

So the `k^{-1-α}` law is not assumed here. It is **confirmed to 1.5e-03**, and the shortfall
at the shipped domain turns out to be the profile simply not having reached its asymptotic
tail by `X = 745`.

## The controls, including the one that broke the instrument twice

A negative result needs a positive control that can report the other answer; a positive
result needs negative controls that can fail. This leg's headline is positive, so the
negative controls carry the weight.

**Positive control.** The `a = 0` CLM anchor is exactly one basis mode, so the pipeline must
return `|ĥ_1| = 1` and nothing else. It does, to `3.4e-15`, with every other mode under
`1.7e-12`. The window was written down first.

**Negative control 1.** `Ω = 1/(1+|X|)` has far field exactly `|X|^{-1}` and a kink at
`θ = π`, so its exponent is exactly 2 — which is precisely the divergence threshold of the
class `s = 1`. Measured: **1.989**.

**Negative control 2.** `Ω = 2 arctan(X)/π` is the sawtooth: it does not decay at all
(`α = 0`), and its coefficients are exactly `2/(πk)`. So its exponent is exactly 1 — the
divergence threshold of the flat class. Measured: **1.001**, with the coefficient *values*
matching the closed form to `1.0e-04`.

**And a calibration curve.** `(1+X²)^{-α/2}` has far field exactly `|X|^{-α}` for any `α` you
like. Sweeping `α = 0.1 … 1.5` and asking the fitter to recover `1 + α` — an exponent it
was never told — gives a worst-case error of **0.006**. That is the instrument's error bar,
and the target's exponent is quoted against it.

### The instrument was wrong twice, and a control caught it both times

Negative control 1 is retained in the artifact specifically because it *broke* the code.
`1/(1+|X|)` happens to satisfy `h(θ) + h(π−θ) = 1`, an identity that annihilates **every
even Fourier mode**. The first version of the exponent fitter averaged logarithms, took the
log of a roundoff zero, and confidently reported `p = −0.06` for a spectrum whose `k²|ĥ_k|`
is flat to 2.3% over `k = 9 … 129`, and to three digits from `k = 33` on. The second
version still returned `−0.25`,
because one sparse bin caught a single annihilated mode.

Neither failure crashed. Both produced a plausible-looking number. If that control had not
been in the battery, the target's exponent would have been reported by a broken fitter.
Both failure modes are now pinned as executable regression gates.

## The honest negative: the shipped domain cannot answer this question

The far-field closure — what you assume beyond the last grid point — is an ablation, and at
the shipped domain **it decides the answer**:

| closure beyond `X_max = 745` | measured `p` |
|---|---|
| continue the equation's own power law | 1.369 |
| hold the last value (injects `α = 0`) | 1.423 |
| set zero (injects a jump) | 1.233 |

A spread of **0.19** on a quantity whose whole meaning is its third decimal. At `X_max = 745`
with a 16 384-point transform, 14 sample points fall outside the grid and something has to
be invented for them.

The headline is therefore not measured there. At `X_max = 4.1e+04`, **zero** sample points
fall outside the grid, no closure is ever consulted, and all three ablations return
byte-identical numbers — for the honest reason that the code never reaches them.

That distinction matters, and this project has been burned by exactly its opposite: leg 53
reported four identical numbers as its sharpest finding when the identity was a tautology
of the code. Identical numbers are a question, not an answer. Here the identity is
explained and the row that actually varies is reported beside it.

## So is the ban clause wrong?

**On the gate's own wording, yes — and the gate answers YES.** The target *is* in an
admissible class: finite at `s = 0` with margin `+0.394`, and at `s = 0.3` with margin
`+0.094`.

**But the clause as literally written is about `s = 1`, and there it is correct.** `s = 1`
is where leg 51 measured the operator to be least bad, and at `s = 1` the target's norm
**diverges**, margin `−0.606`. The clause said "does not have finite norm *in the class
where the operator is least bad*". That is true.

So what is actually established is narrower and, I think, more useful than "the ban is
wrong". It is that **the window is empty, and now both sides of it are measured**:

- the **object** needs `s < 0.397`,
- the **operator** wants `s = 1`,
- the gap is **`+0.603` in exponent units**, and there is no `s` that satisfies both.

Before this leg, one side of that window was a measurement and the other was a docstring.
Now both are measurements. **Correcting the clause's text is not mine to do** — it is the
Decision Maker's, and it is flagged for escalation in the PR body rather than edited here.

## What this changes, and what it does not

It removes one candidate explanation for why legs 52–53 failed. At `s = 0` and `s = 0.3` —
the classes those legs actually used — the target is comfortably inside the space. So
"the target was never in the space" is **not** why `Z₁` came out at 43. Leg 53's block
coupling remains the operative reason, untouched.

It does not say a certificate closes. It does not touch `MM`'s gate. A finite norm says the
target is *in* the room; the whole of legs 51–53 is about the operator being badly behaved
*inside* that room.

And the second unknown is not the problem either: `V` decays with `p = 1.837` against a
predicted `1.795`, roughly twice as fast as `Ω`, so `Ω` alone sets the window.

**No link of the L1→L4 chain moved. Clay stays at ~0.05%.**

---

*Everything reproducible: `.venv/bin/python experiments/p2_route_nb_v1_targetnorm.py`
regenerates the data in about four minutes;
`.venv/bin/python writeup/4_p2_lottery/p2_route_nb_v1_targetnorm_evidence.py` rebuilds the
figure from the committed JSON without recomputing anything;
`.venv/bin/python test_target_norm.py` runs 23 gates.*
