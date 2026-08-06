# TECHNICAL — Route-M2CI v1 (leg 187): Object A against every certificate hypothesis

**Gate (pre-committed, verbatim).** *"Does a full radii-polynomial certificate close on
Chen's γ = 2 inviscid profile (Object A), using leg 125's own transcribed constants and
recovered shape as the starting construction, with every hypothesis of the certificate
framework satisfied (not just the budget comparison leg 125 already made)?"*

**Answer: NO.** Three clauses fail — **H3 (isolation)**, **H5 (contraction, $Z_0+Z_1<1$)**,
**H7 ($Z_2$ bounded)** — while the clause leg 125 measured, $Y_0$, is not merely favourable
but **exactly zero**.

| artifact | path |
|---|---|
| module | `solver/chen_inviscid_certificate.py` |
| tests (45 checks) | `test_chen_inviscid_certificate.py` |
| runner | `experiments/p2_route_m2ci_v1_construction.py` |
| evidence (30 checks, no re-run) | `experiments/p2_route_m2ci_v1_construction_evidence.py` |
| curated data | `writeup/data/p2_route_m2ci_v1_construction.json` |
| figure | `writeup/figures/fig65_route_m2ci_v1_construction.png` |
| novelty pass (committed BEFORE construction) | `writeup/novelty/leg_187.md` |

---

## 0. Scope, stated before the numbers

* **Object A is INVISCID**, ν = 0 — Chen arXiv:1908.09385 sec 1.5. This leg bears on the
  viscous "missing rung" question **not at all**. That question stands exactly where leg 125
  left it. The γ = 2 in the route name is the dissipation exponent of the *dynamics* Chen's
  Theorem 1.1 concerns; the *profile* his theorem converges to is inviscid.
* **Object A is a published closed form** — Chen eq (2.2) p.4; the entire branch $a \le 1$ in
  HQWW arXiv:2305.05895. Recorded as novelty finding **N2 PRE-EMPTED** before construction.
  Consequence: $Y_0 \equiv 0$, and the YES branch would have carried **nil existence
  content**. See §6.
* **The symmetry zero mode is published** — Xu arXiv:2607.19762 gives point spectrum
  $\{0,1\}$ (scaling and time-shift modes) for the $a = 0$ sibling. Novelty finding **N3
  PRE-EMPTED in general form**. This leg *cites* it; the contribution is the
  certificate-clause audit at $a = 1/2$ with magnitudes.

## 1. The object, and what was reused

$$\Omega(X) = \frac{-2bX}{(X^2+b^2)^2},\quad b^2=\tfrac38,\quad a=\tfrac12,\quad c_l=\tfrac13,\quad c_\omega=-1,\quad \nu=0.$$

Per the standing ban, `capabilities.py` was grepped before anything was written. Reused, not
rebuilt: `solver/dissipative_profile.py` (leg 125's territory, **read-only**) for the
transcribed constants, `chen_profile`, the grid, the whole-line Hilbert matrix, the
4th-order derivative/velocity operators and the analytic Jacobian at ν = 0;
`solver/nk_bounds.budget` for the one budget; `solver/certificate_guards.hypothesis_violations`
for the one shared hypothesis guard.

The new module adds only what did not exist: exact rational arithmetic on the defect, the
exact dilation orbit and its generator, the far-field symbol clause, and the battery.

**Convention check (load-bearing).** The module's exact-arithmetic $H\Psi = (g-X^2)/D^2$ and
$U = X/D$ are verified equal to leg 125's returned `U_x` and `U` to < 1e-13
(`test_orbit_matches_leg125_transcription_at_chens_gamma`). Without this the exact defect
would be solving a different equation. `chen_profile` returns the **3-tuple**
`(Omega, U_x, U)` — a first draft of the test compared against the tuple and produced a
spurious 3.394 discrepancy.

## 2. H1 — space membership

Weighted sup norm $\|h\|_s = \sup |(1+X^2)^{s/2}h(X)|$. Finite for $s \le 3$, divergent above.
On a truncated grid this shows as growth with the truncation radius:

| $s$ | $\|\Omega\|_s$ (full grid) | ratio vs inner half |
|---|---|---|
| 1.0 – 3.0 | 1.845 – 2.191 | 1.000000 (converged) |
| 3.1 | 2.373 | 1.0711 |
| 3.5 | 33.43 | 1.4333 |

The $s = 3.5$ row is the control: the norm is being carried by the outermost nodes.

## 3. H2 — the defect, in exact arithmetic

The profile family, with $g$ the squared length scale and $\kappa$ the amplitude:

$$\Psi = \kappa\frac{-2\sqrt{g}X}{D^2},\quad H\Psi = \kappa\frac{g-X^2}{D^2},\quad U = \kappa\frac{X}{D},\quad D = X^2+g.$$

Every term of $R(\Psi) = (c_\omega + H\Psi)\Psi - c_l X\Psi_X - aU\Psi_X$ carries exactly one
factor $\sqrt g$, so $R/\sqrt g$ has rational coefficients and the whole computation stays in
`Fraction`. The distinguished amplitude is $\kappa = 8g/3$.

**Result: the numerator of $R/\sqrt g$ is the ZERO POLYNOMIAL at $g \in \{3/8, 1, 2, 1/7, 9/4\}$.**
$g = 3/8$ with $\kappa = 1$ is Chen eq (2.2) verbatim. Hence $Y_0 = 0$ **exactly**.

Controls, all of which must and do come out nonzero:

| control | numerator |
|---|---|
| amplitude $+1/100$ at $g = 3/8$ | $-\frac{303}{80000}X - \frac{101}{10000}X^3$ |
| $a = 0$ (the CLM sibling) at Chen's constants | nonzero |
| $c_l = 1/2$ instead of $1/3$ | nonzero |

*Leg 125's lead, for the record:* $Y_0/\text{budget} \in [1.325\mathrm{e}{-09},\, 5.800\mathrm{e}{-05}]$
over 9 rows. Correct, and — as §4 shows — never the binding clause.

## 4. H3 / H4 / H5 — the dilation orbit, and why no $A$ repairs it

**The orbit.** $\Psi_g(X) = -\frac{16}{3}g^{3/2}X/(X^2+g)^2$ solves the steady equation for
**every** $g > 0$ at fixed $c_l, c_\omega$: the Hilbert transform commutes with dilation and
the velocity's factor of $\mu$ cancels against $\Omega_X$. §3 proves it exactly.

**H3 fails.** Every ball around Object A contains other exact zeros. By bisection along the
true (nonlinear) orbit at $s = 2$, $n = 401$:

| target radius $r$ | orbit displacement $\delta g$ | distance achieved | competitor residual | centre residual |
|---|---|---|---|---|
| 1e-02 | 3.0349e-03 | 1.0000e-02 | 1.8651e-05 | 1.8886e-05 |
| 1e-04 | 3.0284e-05 | 1.0000e-04 | 1.8884e-05 | 1.8886e-05 |
| 1e-06 | 3.0283e-07 | 1.0000e-06 | 1.8886e-05 | 1.8886e-05 |

The competitors' residuals sit at the centre's own discretisation floor, because they are
exact solutions too. The theorem's *conclusion* (uniqueness in the ball) is false, so by
contraposition its hypotheses cannot all hold, whatever $A$ or space is chosen.

**H4 fails.** $\varphi = d\Psi_g/dg = -\frac{16}{3}\sqrt g\,X(\frac32 X^2 - \frac g2)/D^3$ is an
exact kernel element (checked against a central difference in $g$ to 1e-7 relative).

| $n$ | $\|DF\varphi\|_s/\|\varphi\|_s$ | control (localised bump) | ratio |
|---|---|---|---|
| 401 | 5.2073e-05 | 0.68896 | 1.3231e+04 |
| 601 | 1.0343e-05 | 0.68948 | 6.6661e+04 |
| 801 | 3.2737e-06 | 0.68931 | 2.1056e+05 |

Kernel defect falls with the grid (tracking the 4th-order residual floor 1.889e-05 → 1.187e-06);
the control is flat. This is an operator fact.

**H5 fails, exactly and unrepairably.** $DF\varphi = 0 \Rightarrow (I - A\,DF)\varphi = \varphi$
for every $A$, so

$$\|I - A\,DF\| \ \ge\ 1 \quad\Longrightarrow\quad Z_0 + Z_1 \ \ge\ 1 \quad\Longrightarrow\quad 1 - Z_0 - Z_1 \ \le\ 0,$$

in every norm, for every $A$, in every space containing $\varphi$ — i.e. every $s \le 3$, which
by §2 is every space where the centre itself lives. With $Y_0 = 0$:
$p(r) = Z_2r^2 - (1-Z_0-Z_1)r \ge 0$ for all $r > 0$. **No admissible radius exists.**

### 4.1 The `pinv` trap — reported in two regimes on purpose

| $n$ | $\sigma_{\min}/\sigma_{\max}$ | shadow, default `rcond` | shadow, `rcond` = 1e-6 | 1e-4 |
|---|---|---|---|---|
| 401 | 1.3486e-08 | 2.8737e-09 | 0.9999838 | 0.9999838 |
| 601 | 9.0655e-10 | 5.2883e-08 | 0.9999968 | 0.9999968 |
| 801 | 1.3380e-10 | 1.0316e-07 | 0.9999990 | 0.9999990 |

The default-`rcond` column appears to refute §4's argument. It does not: NumPy's cutoff is a
relative $\sim n\varepsilon \approx 10^{-13}$, **below** $\sigma_{\min}/\sigma_{\max}$, so
`pinv` retains the near-null direction and numerically inverts a kernel the continuum does not
permit. Truncating it — which any rigorous $A$ is *forced* to do — returns the shadow to 1 from
below, converging as the grid refines. A single-resolution number here would have been a
statement about `rcond` (lesson 86). The clause is carried by the exact argument; the float
columns are reported because the gap between them is the measurement.

## 5. H6 / H7

**H6a — the standard repair is available.** Bordering with a phase functional transversal to
$\varphi$ (unknowns $(h, \delta c_l)$) lifts $\sigma_{\min}$:

| $n$ | unbordered $\sigma_{\min}$ | bordered $\sigma_{\min}$ | lift | bordered cond |
|---|---|---|---|---|
| 401 | 3.4003e-07 | 9.2274e-04 | 2.71e+03 | 2.7325e+04 |
| 601 | 3.5315e-08 | 5.1630e-04 | 1.46e+04 | 7.5452e+04 |
| 801 | 7.0532e-09 | 3.3628e-04 | 4.77e+04 | 1.5676e+05 |

Symmetry reduction / phase conditions are standard validated-numerics practice (novelty Q2);
this leg claims none of it. Reported so the NO is not mistaken for "the repair was unavailable."

**H6b — the far-field symbol, the one genuinely open sub-question (novelty N4).** Beyond the
profile's support, $L_\infty h = c_\omega h - c_l X h_X$, acting on $h \sim X^{-s}$ as

$$\sigma(s) = c_\omega + s\,c_l = \tfrac{s}{3} - 1, \qquad \sigma(3) = 0.$$

| $s$ | 1.0 | 2.0 | 2.5 | 2.9 | 2.99 | 3.0 | 3.5 |
|---|---|---|---|---|---|---|---|
| $\sigma(s)$ | −0.6667 | −0.3333 | −0.1667 | −0.03333 | −0.003333 | 0 | +0.1667 |
| $1/\|\sigma\|$ | 1.5 | 3.0 | 6.0 | 30.0 | 300.0 | ∞ | 6.0 |
| admissible | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ (centre unbounded) |

The profile's **measured** decay exponent is **2.999955** (log-log slope over the outer decade,
n = 801); the $X^{-2}$ control measures **−1.999911**. **The symbol vanishes exactly at the
centre's own decay rate.** This is the kernel obstruction seen from the far field: $X^{-3}$ is
the homogeneous solution of the tail operator. The tail inverse norm $3/|3-s|$ diverges as $s$
approaches the only grading at which the centre is comfortably in the space.

**H7 fails — $Z_2$ is not an operator constant here.** $F$ is exactly quadratic, so
$B(u,v) = (Hu)v + (Hv)u - a[(V\!Hu)v_X + (V\!Hv)u_X]$ is constant and $Z_2 = \|A\|\,\|B\|$.
$B$ contains $v_X$, which the weighted sup norm does not control:

| $n$ | 201 | 301 | 401 | 601 | 801 | 1201 |
|---|---|---|---|---|---|---|
| $Z_2$ | 9.438e10 | 2.229e11 | 4.311e11 | 1.134e12 | 2.296e12 | 6.309e12 |
| $\|A\|$ | 686.5 | 1079.8 | 1565.3 | 2745.2 | 4167.5 | 7633.4 |
| $\|B\|_s$ | 1.375e8 | 2.065e8 | 2.754e8 | 4.132e8 | 5.510e8 | 8.266e8 |
| $\sigma_{\min}/\sigma_{\max}$ | 1.376e-06 | 9.182e-08 | 1.349e-08 | 9.066e-10 | 1.338e-10 | 9.032e-12 |

Least-squares slopes in $\log n$: $Z_2 \sim n^{2.36}$ (66.9× over the ladder, monotone at every
step), $\|A\| \sim n^{1.36}$, $\|B\| \sim n^{1.00}$. The negative control that *could* have come
out flat: $\sigma_{\min}/\sigma_{\max} \sim n^{-6.68}$, collapsing by 1.52e05× — it does not
settle, confirming the kernel is the operator, not the grid.

## 6. Why the YES branch would have been hollow anyway

With $Y_0 = 0$ exactly, $p(r) = Z_2r^2 - (1-Z_0-Z_1)r$, so **any** bordered $Z_0+Z_1 < 1$ closes
it — and would assert a zero at a point already published in closed form (Chen eq (2.2); HQWW
for all $a \le 1$). The existence content is nil. Recorded in `writeup/novelty/leg_187.md`
before any number here was computed.

This leg deliberately does **not** supply a bordered $Z_0 + Z_1$: bounding it rigorously needs
an interval enclosure of the tail block, which this repository's banked ceiling
(`solver/interval_certificate.py`) says it does not have. Reporting a float there as if it were
a bound would be lesson 73. The JSON records it as `NOT MEASURED` with the reason.

## 7. What this banks

1. **A characterized negative.** Budget-under is not certificate-ready — now demonstrated with
   the budget pinned at *exactly zero*, the strongest form available. Leg 125's 1.325e-09 to
   5.800e-05 was correct and load-free.
2. **The failing clause, named with its constant.** $Z_0 + Z_1 \ge 1$ for every $A$, from an
   exact symmetry, verified in exact rational arithmetic with controls that can fail.
3. **The N4 sub-question, answered.** The far-field symbol's zero coincides exactly with the
   profile's decay exponent ($\sigma(3) = 0$; measured 2.999955). Kernel and tail are one
   mechanism.
4. **A reusable trap.** `pinv` with default `rcond` silently inverts a near-kernel whenever
   $\sigma_{\min}/\sigma_{\max}$ exceeds $n\varepsilon$ — which is the normal case for a
   discretised singular operator, not an edge case.

**Not banked, and explicitly not claimed:** anything about the viscous problem; any novel
statement about the scaling zero mode (Xu's, cited); any credit for symmetry reduction
(standard, cited); and any existence result about Object A (Chen's, analytic, and already in
closed form).
