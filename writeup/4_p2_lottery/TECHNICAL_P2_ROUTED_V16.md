# Route-D v16 — the float rehearsal: what the reduced space fixed, and what it did not

*Phase-2 P2, Route-D leg 16. Figure: `writeup/figures/fig33_route_d_v16_rehearsal.png`.
Data: `writeup/data/p2_route_d_v16_rehearsal.json` (rebuild the figure with
`writeup/4_p2_lottery/p2_route_d_v16_evidence.py`; regenerate with
`experiments/p2_route_d_v16_rehearsal.py`, ~5 min, deterministic).
Code: `solver/reduced_certificate.py` + `test_reduced_certificate.py` (16/16; suite 22 files).*

**Rigor level: 1. This leg's headline is a NEGATIVE with a named repair.** Nothing here is
interval-enclosed, nothing is a certificate, and — per v15 — even a successful certificate in
this family would be a capability demonstration rather than a novel result.

---

## 0. What this leg is and why it is small

v15 re-priced the whole lane: computer-assisted certification of 1D toy-model profiles is
routine for the groups working this family, and the two-scale traveling wave's existence
appears already proved. So the certificate was demoted to a **one-chunk capability build** —
do the float rehearsal, find out whether the pipeline closes, stop. That is exactly what this
is, and the answer is *no, and here is precisely why*, which is worth more than a yes would
have been.

The rule being honoured is banked lesson 1: **do the cheap float rehearsal before hardening.**
`solver/interval.py` has existed since v1 and has still never been pointed at anything,
correctly.

---

## 1. Y₀ reaches machine precision — the first genuinely good number in the ledger

The defect that matters is the residual of the **interpolant as a function**, not the nodal
vector Newton zeroed. That distinction is v12's, and it survives the change of formulation:
Newton enforces `K` conditions, the certificate asks about `F` on all of `[0,1]`.

| K | 16 | 24 | 32 | 48 | 64 | 96 | 128 |
|---|---|---|---|---|---|---|---|
| a=0.3, off-node `sup|F|` | 1.5e−2 | 8.0e−4 | 4.0e−5 | 9.1e−8 | 2.0e−10 | **1.5e−12** | 2.2e−12 |
| a=0.3, nodal residual | 1e−14 | 1e−14 | 1e−14 | 1e−14 | 1e−14 | 1e−14 | 1e−14 |
| a=0.4, off-node `sup|F|` | 1.0e−4 | 3.5e−7 | 1.1e−9 | **7.8e−13** | 7.7e−13 | 1.5e−12 | 2.2e−13 |

Fitted above the float floor: `K^−13.0` (a=0.3) and `K^−16.3` (a=0.4), both steeper than the
`K^−(2/a+1)` the `(1−v)^{1/a}` endpoint branch predicts (−7.7 and −6.0) — the fits are taken
only over points above `1e−11`, but they are still contaminated by proximity to the floor, so
**the honest statement is "faster than algebraic and it reaches machine precision", not a
rate.** The nodal row is there as the control: it is flat at `1e−14` by construction, and the
off-node value is nine orders larger at K=32, which is what tells you the measurement is about
the function rather than the grid.

For scale: the GA carried a defect floor of `~1e−2` for five legs, v11's Newton took the
whole-line nodal residual to `1e−14` but the *interpolant* defect stayed at `1e−4`–ish, and
v12's budget — computed at the anchor and therefore wrong anyway — was `2.4e−4`. **`1.5e−12`
is the first time the number a certificate actually needs has been at machine level.**

`Z₀ = ‖I − A·DF‖` is roundoff (`1.6e−11`), as it must be when `A` is the numerical inverse of
the same matrix. Reported for ledger completeness, not because it is informative.

---

## 2. Z₂ does not exist in the sup setting, and the far field is not why

This is the leg's result. Two independent obstructions.

### 2a. The finite Hilbert transform is unbounded on the sup norm — on a **bounded** interval

Removing the far field killed the **decay** grading that v3–v11 needed. It did nothing
whatever to the **smoothness** one. `H` unbounded on `L^∞` is v4's W3, and it is a local
statement about a jump; a bounded domain does not repair it.

Sampling cannot establish this and cannot refute it (banked lesson 9) — the adversary has to
be built. Inside the actual perturbation space `δe = (1−v²)δs`, take Chebyshev partial sums of
a step:

| K | 8 | 16 | 32 | 64 | 128 | 256 |
|---|---|---|---|---|---|---|
| `sup|H δe| / sup|δe|` | 1.350 | 1.601 | 2.061 | 2.351 | 2.727 | 3.040 |

Linear in `log K` at **+0.499 per e-fold** (max fit residual 0.068). The classical constant for
a clean jump is `2/π = 0.637`; the deficit is the `(1−v²)` factor damping the jump region.

**The instrument check that makes this trustworthy.** The naive probe — a single high Chebyshev
mode — *also* reports a divergence: 0.998 → 2.935 → 6.436 at K = 64/128/256. It is entirely the
quadrature. Refine the rule and it collapses:

| rule (levels/order) | 20/20 | 20/40 | 24/60 | 30/80 |
|---|---|---|---|---|
| naive probe, K=256 | 6.436 | 3.007 | 2.985 | **0.999** |
| adversary, K=256 | 2.991 | 3.038 | 3.040 | **3.041** |

One row moves under a 4× refinement of the instrument and one does not. That is banked lessons
9 and 14 in a single table, which is why both rows are kept in the module and in the figure
rather than only the one that supports the conclusion.

### 2b. The nonlinearity's second derivative is bounded exactly for a ≤ 1/2

`N(e) = e^{1/a}` has `N''(e) = p(p−1)e^{p−2}` with `p = 1/a`, and `e` vanishes **linearly** at
the support edge. So `sup|N''|` is finite iff `p ≥ 2` iff **`a ≤ 1/2`** — which is exactly
where `Ω = −e^{1/a}` loses `C²`.

Displayed as growth under an edge cutoff tightened over eight decades (`1e−2 → 1e−10`), because
quoting whatever value a grid happened to reach would hide the divergence:

| a | 0.20 | 0.25 | 0.30 | 0.40 | 0.45 | 0.50 | 0.55 | 0.60 | 0.70 | 0.80 |
|---|---|---|---|---|---|---|---|---|---|---|
| value at cutoff `1e−2` | 20.00 | 12.00 | 7.778 | 3.750 | 2.716 | 2.000 | 3.711 | 5.793 | 9.63 | 10.65 |
| growth over 8 decades | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | **28.5** | **466** | **3.8e4** | **1.0e6** |

Flat to every displayed digit for `a ≤ 1/2`; growing without bound above. At `a = 1/2` the value
is `p(p−1) = 2` exactly, checkable by hand, and the code reproduces `2.000000000000`.

**Three things this is not.**
- It is **not a statement about the equation.** v14 solves the profile cleanly and
  grid-converged to `a = 1.2`. The traveling wave exists; it is the *certificate's norm* that
  fails.
- It is **norm-dependent.** A domain weight vanishing like `(1−v)^{(2−1/a)/2}` restores
  finiteness, at the price of requiring perturbations to vanish at the edge. That is the v5-U3c
  trade in a new place: check which side of the inequality a marginality lives on before
  pricing it (lesson 13).
- It is **not an explanation of `a*`.** The coincidence with the independently measured survival
  boundary `a* ≈ 0.5–0.55` is striking and is recorded for exactly that reason — recording it is
  how the next person gets to disprove it. v12's `a = 1/3` control is the precedent: a
  tantalising arithmetic coincidence at `a*` that a control killed. No control has been run
  here, so it stays an observation.

---

## 3. Z₁ is not computed at all

The infinite-dimensional tail — the part of the operator outside the `K`-mode subspace — is the
entire content of a real computer-assisted proof, and nothing in this leg bounds it. It is
reported as `None` in the assembled rehearsal rather than as zero, and `rehearsal()`
deliberately **refuses to return a radii polynomial**: assembling one from a ledger with an
uncomputed entry, or with an infinity in it, is the exact failure mode banked as lesson 15.

---

## 4. The verdict, and the next brick

**The sup-to-sup rehearsal does not close.** Not because of the far field — v14 genuinely
removed that — but because the smoothness half of the requirement was never about the far
field in the first place.

The repair is v5's, and it is **measured here** rather than assumed. Re-running the same
adversary against `‖δe‖_γ = sup|δe| + [δe]_γ`:

| γ | 0.15 | 0.25 | 0.35 | 0.50 | 0.65 | 0.85 |
|---|---|---|---|---|---|---|
| slope in `log K` | **+0.066** | +0.014 | **−0.021** | −0.049 | −0.057 | −0.050 |

The divergence stops at **γ ≳ 0.35** — and `γ = 0.15` still creeps, which matters: it shows the
threshold is a real threshold and not an artefact of dividing by any seminorm at all.

**v5 U1 found the same `γ ≳ 0.35` on the whole line.** That is a genuine independent check
rather than a restatement, because v5's norm *also* carried a decay grading and this one has
none — so the threshold belongs to the smoothness half, which is what one would want to be
true and had not been separated before.

So the next brick is the **Hölder version of the reduced space**, and the good news is that it
is a smaller job than the whole-line one was: v5's `holder_norms`, v7's derivative-gain closure
and v8's weighted-Hölder bound on `H` all adapt, and on a compact interval there is **no decay
grading, no resonance, no matching radius `X₀`, and no tail bound** to price. Roughly: v7–v9
without the half that was expensive.

---

## 5. Gate-check against the Clay chain

**(a) Which link?** L1, and only in the sense of making the pipeline honest. v15 already
established that L1 is occupied territory, so this is capability work by design.

**(b) Is another L1 leg the best use of the next chunk?** **No.** One more would be defensible
— the Hölder version is well-specified and cheap — but v15's ranking stands: the DSS lane is
the swing, and verifying the two load-bearing readings from the literature (blocked on PDF
access in this container) beats both. If a session *does* do the Hölder leg, it should be
framed as finishing the capability, not as chasing a result.

**(c) Cheaper experiment that kills the route?** Still "read one paper", still blocked on
access. That has not changed and should keep being said.

---

## 6. What is NOT claimed

- **No certificate.** `Z₁` uncomputed, `Z₂` infinite in the setting tested, no radii polynomial
  assembled, nothing interval-enclosed.
- **`Y₀ = 1.5e−12` is not a budget.** It is one input, and the budget it would feed does not
  exist yet. A number under a budget is not a result until the budget was computed for the same
  object (lesson 30) — and here there is no budget at all.
- **The `a ≤ 1/2` threshold is about the norm, not the equation**, and is not offered as an
  explanation of `a*`.
- **The `K^−13` fit is not a rate.** It is contaminated by the float floor; the defensible claim
  is "faster than the algebraic prediction, and it reaches machine precision".
- **v14's "cold start converges at every a" is slightly overstated** and is corrected here: at
  `a = 0.7` the cold start misses the basin and continuation from the neighbouring `a` is
  needed. Every other value in 0.2…1.2 converges cold. Small, but it was a claim.
