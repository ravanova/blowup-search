# Route-PORT v2 — reach makes the truncation gap *worse*, so the tail lemma is forced

*Phase 2 / P2, leg 47. Code: `experiments/p2_route_port_v2_reach.py` →
`writeup/data/p2_route_port_v2_reach.json`. Working notes: `PHASE2_P2_NOTES.md` §36.
4.4 s, 3/3 pre-committed clauses.*

**Leg 46 left one number unmeasured and the whole road depended on it. Measured: extending
the domain does not close the truncation gap — it opens it, by half an order of magnitude
per unit of reach. A rigorous analytic far-field enclosure is FORCED, not optional. No chain
link moved; Clay unchanged at ~0.05%.**

---

## 1. The question, and why it was open

Leg 46's certificate closes around the *truncated* object, at `1.55e+08 ×` the ball radius.
I initially called that "not close to affordable" and then corrected myself: the grid is
**log-radial**, so reach costs *logarithmically*, and if the distance kept falling like leg
46's power law the gap might be a handful of extra grid points rather than a wall.

That correction rested on applying leg 46's `X_max^−0.437` law — which was measured for the
**contraction ratio**, not for the weighted distance — to a quantity it was never fitted to.
Both readings were guesses. This leg measures the thing itself.

**Pre-committed before the run, with both branches actionable so it could not be argued
either way afterwards:** fit `log₁₀(distance / r_max)` against `ρ_max`. Slope `≤ −0.05` →
brute force closes, report the cost. Slope `> −0.05` → tail lemma forced, and *do not*
propose "just refine" as the next leg.

## 2. The measurement

Radial resolution held fixed at `dρ = 0.02` so the ladder varies reach and nothing else.

| `ρ_max` | `X_max` | `n` | distance | `r_max` | ratio |
|---|---|---|---|---|---|
| 6 | 100.9 | 301 | 3.678e−01 | 5.296e−09 | 6.94e+07 |
| 7 | 274.2 | 351 | 2.598e−01 | 4.626e−09 | 5.62e+07 |
| 8 | 745.2 | 401 | 1.836e−01 | 1.182e−09 | 1.55e+08 |
| 9 | 2025.8 | 451 | 2.049e−01 | 2.866e−10 | 7.15e+08 |
| 10 | 5506.6 | 501 | 3.306e−01 | 7.558e−11 | 4.37e+09 |

```
d log10(distance) / dρ  =  −0.0196
d log10(r_max)    / dρ  =  −0.4899
d log10(ratio)    / dρ  =  +0.4703      (gate: −0.05)
```

**Both of my guesses were wrong, in opposite directions.**

**The distance does not fall.** It is essentially flat — slope `−0.02` per unit `ρ` — and
over the last three rungs it *rises*, 0.184 → 0.205 → 0.331. That is what an **algebraic**
far field does: every unit of reach exposes more un-resolved tail, and the two truncations
keep differing by about the same weighted amount. The `X_max^−0.437` law I extrapolated
belonged to the contraction ratio and does not transfer.

**And the ball shrinks fast.** `r_max` falls `−0.49` per unit `ρ`, a factor of ~70 across the
ladder. That is not mysterious: the tuned weight is `w_l = 0.01·X_max` *by construction*, so
the norm the ball is measured in changes as the domain grows, and `Z₂` grows with it.

**Net: the ratio rises `+0.47` per unit `ρ`.** Every unit of reach costs a factor of ~3 *in
the wrong direction*. The gap at `ρ = 10` is **63× worse** than at `ρ = 6`
(`4.374e+09 / 6.944e+07 = 62.99`; a leg-60 reproduction audit caught this cell quoting the
`ρ = 8 → 10` factor, 28.16×, instead — the wrong baseline, understating the effect by 2.25×).

## 3. The verdict

**Reach cannot close this at any size.** Not expensively — *at all*. The trend has the wrong
sign, so there is no `X_max`, however large, at which the float ball contains the true
object. The pre-committed gate fires on the tail-lemma branch.

**What that means concretely.** Certifying `HL_S2_nonsymmetric` on the whole line requires an
**analytic far-field enclosure**: for `|X| > X_max`, a rigorous bound on the solution from
its asymptotic expansion, with the error controlled and folded into the budget, so that the
finite-dimensional certificate plus the tail estimate covers `ℝ`. This is standard apparatus
in validated numerics on unbounded domains. It is also **real mathematics rather than more
compute**, and this leg is what promotes it from "one of the things we'd need" to "the thing
that decides whether L1 is reachable."

**And it re-prices the L1 road**, which is the actionable output. Before this leg the two
gaps between here and a certified L1 were interval arithmetic (engineering) and truncation
(unknown). Now: interval arithmetic (engineering, and `solver/interval.py` exists as an
arithmetic layer that has never been wired to a certificate), and a **tail lemma**
(mathematics, forced, and nobody here has written one).

## 4. What this does not say

* It does not say the object cannot be certified — Chen–Huang–Li's profile is presumably as
  certifiable as any, and groups doing validated numerics write tail lemmas routinely.
* It does not invalidate leg 46. The certificate still closes in float at every rung; what
  changes is that "extend the domain" is now *known* not to be the way to make it mean
  something.
* It says nothing about Clay. `L1` is a 1D toy, and `L2`/`L3` are occupied by Chen–Hou while
  `L4` is out of reach of interval arithmetic entirely.

## 5. Reproduce

```bash
.venv/bin/python -u experiments/p2_route_port_v2_reach.py   # 4.4 s
```

`Q1` every rung converges or is refused, `Q2` distance falls with reach *(passes only on the
first-to-last comparison — see §2, it is not monotone and the writeup says so)*, `Q3` the
verdict is decided. 3/3.
