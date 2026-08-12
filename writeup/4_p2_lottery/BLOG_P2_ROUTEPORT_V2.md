# Reach doesn't close the gap. It makes it 63× worse — and that number was wrong once already.

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. The
[previous post](BLOG_P2_ROUTEPORT_V1.md) found a certificate that closes, but around the
*wrong* object — the truncated one, a hundred and fifty million times too small for the
ball I'd proved. The obvious next question: does pushing the domain outward shrink that
gap? I measured it. It doesn't shrink. It grows, by half an order of magnitude for every
unit of extra reach, and there is no size at which it stops growing. Still a toy model.
Still not a breakthrough.*

## The question I'd already half-answered wrong, twice

Last post left one number unmeasured, and the whole next step depended on it. The
certificate closes around a truncated domain, and the *true* object — on the infinite
line — sits outside the ball by a factor of 1.55×10⁸. Push the domain out and does that
factor shrink?

I had two guesses, in two different posts, and both were wrong. The first: "not close to
affordable." The second, a correction of the first: the grid is log-radial, so reach is
cheap, and if the gap kept falling the way an earlier measurement's contraction ratio did,
closing it might cost only a handful of extra grid points.

Both were guesses about a quantity neither one had actually measured — the second one
borrowed a power law (`X_max^−0.437`) that had been fit to a *different* quantity (the
contraction ratio) and applied it to the weighted distance, which it was never fitted to.
This post measures the thing itself, and commits to the gate before running anything:
fit `log₁₀(distance / r_max)` against `ρ_max`. Slope `≤ −0.05` and brute force closes,
report the cost. Slope `> −0.05` and a rigorous far-field enclosure — a tail lemma — is
forced, full stop, no "just refine and try again."

## The measurement

Five rungs, radial resolution held fixed so only the reach varies:

| `ρ_max` | `X_max` | distance | `r_max` | ratio (distance / r_max) |
|---|---|---|---|---|
| 6 | 100.9 | 3.678×10⁻¹ | 5.296×10⁻⁹ | 6.94×10⁷ |
| 7 | 274.2 | 2.598×10⁻¹ | 4.626×10⁻⁹ | 5.62×10⁷ |
| 8 | 745.2 | 1.836×10⁻¹ | 1.182×10⁻⁹ | 1.55×10⁸ |
| 9 | 2025.8 | 2.049×10⁻¹ | 2.866×10⁻¹⁰ | 7.15×10⁸ |
| 10 | 5506.6 | 3.306×10⁻¹ | 7.558×10⁻¹¹ | 4.37×10⁹ |

Two slopes, fit across all five rungs:

```
d log10(distance) / dρ  =  −0.0196
d log10(r_max)    / dρ  =  −0.4899
d log10(ratio)    / dρ  =  +0.4703      (gate: −0.05)
```

**Both of my earlier guesses were wrong, in opposite directions.**

The distance barely moves — slope `−0.02` per unit `ρ`, essentially flat — and it is not
even monotone: over the last three rungs it *rises*, `0.184 → 0.205 → 0.331`. That's the
signature of an algebraic (power-law) far field rather than an exponential one: every
unit of extra reach exposes roughly as much un-resolved tail as it removed.

Meanwhile the ball shrinks fast — `r_max` falls `−0.49` per unit `ρ`, about a factor of 70
across the five rungs. That side isn't mysterious: the weight is built as `w_l =
0.01·X_max`, so the very norm the ball is measured in tightens as the domain grows, and
the curvature term (`Z₂`) grows with it.

**Net: the ratio climbs `+0.47` decades per unit `ρ`.** Every unit of extra domain costs
close to a factor of 3, in the *wrong* direction.

## The headline number, and the number that was wrong before I got here

**The gap at `ρ = 10` is 63× worse than at `ρ = 6`** — `4.374×10⁹ / 6.944×10⁷ = 62.99`.

I'm stating that number carefully because a reproduction audit on this exact record
already caught it wrong once: an earlier pass quoted the `ρ = 8 → 10` factor, `28.16×`,
as if it were the full-ladder comparison — the wrong baseline, understating the true
effect by more than half. The number above is the `ρ = 6 → 10` comparison, the one the
pre-registered gate actually asks for, and it is the one that stands.

## The verdict: not expensive. Impossible, at any size.

The slope has the wrong sign. That's not "the brute-force approach is costly" — it's
"there is no `X_max`, however large, at which the finite-domain ball contains the true
object." Reach cannot close this gap. Not slowly. Not at all.

The pre-committed gate fires on its tail-lemma branch: certifying the target object
(`HL_S2_nonsymmetric`) on the whole real line needs an **analytic far-field enclosure** —
a rigorous bound on the solution's asymptotic tail for `|X| > X_max`, with its error
folded into the certification budget, so the finite-dimensional certificate plus the
tail estimate together cover all of `ℝ`. That's standard apparatus in validated
numerics on unbounded domains; groups doing this kind of work write tail lemmas
routinely. Nobody here has written one yet.

That re-prices the whole road to a certified 1D object. Before this leg there were two
gaps: interval arithmetic (an engineering job — the arithmetic layer exists in
`solver/interval.py` but has never been wired to a certificate) and truncation (unknown
size, unknown difficulty). Now truncation has a name and a direction: it is a genuine
piece of mathematics, forced, and not yet attempted.

## What this doesn't say

It doesn't say the object can't be certified. Groups doing validated numerics write tail
lemmas for exactly this kind of algebraic far field as a matter of course; there's no
reason to think this one is special.

It doesn't invalidate the earlier certificate. That certificate still closes, in float,
at every rung tried — what's now known is that "just extend the domain" was never going
to be the way to make it mean something about the true, untruncated object.

And it says nothing new about the Clay problem. This is a 1D toy model; the odds stay
where they've been for the whole project, at about **0.05%**, for the same structural
reasons as always — this kind of search can only argue *for* a singularity, never
against one, and the certification technology here reaches one- and two-dimensional toy
problems, nowhere close to the real three-dimensional equation. No link of the chain
moved this session either.

## Reproduce

```
.venv/bin/python -u experiments/p2_route_port_v2_reach.py   # 4.4 s
```

Three pre-committed checks, three passes: every rung converges or is explicitly refused;
the verdict is decided one way or the other; and the "does distance fall with reach"
check passes only in the weak, first-to-last sense the writeup flags — it is not
monotone, and the post above says so rather than smoothing it out.
