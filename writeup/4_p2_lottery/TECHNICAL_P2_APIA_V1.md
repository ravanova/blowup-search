# Route-APIA v1 (leg 312): arbitrary-precision re-measurement of leg 178 and leg 176

**Branch** `leg/312-apia-v1`. **Agent:** LEG (heavy, construction-eligible).
**Gate answer: YES.** Data: `writeup/data/p2_route_apia_v1.json`. Runner:
`experiments/p2_route_apia_v1.py`. Evidence/figure: `experiments/p2_route_apia_v1_evidence.py`,
`fig73`. Novelty: `writeup/novelty/leg_312.md`.

## 0. The gate, verbatim (pre-committed by the DM)

> Do the two pre-registered re-measurements (leg 178, leg 176), run at arbitrary precision,
> change the banked headline of leg 178 (the `3.1e+03` contamination) or leg 176 (the lost
> `N=1024` row) — magnitudes, not booleans?

Answer: **YES**, both change.

## 1. Territory and what this leg builds

`solver/interval_mp.py` (NEW): a `decimal.Decimal`-backed rigorous interval type
`MPInterval`, mirroring `solver/interval.py`'s directed-rounding design but using
`Decimal`'s native `Context(rounding=ROUND_FLOOR/ROUND_CEILING)` instead of float64's
`np.nextafter` one-ulp workaround. Two sections:

- **Section 1** (leg 178): `+ - * /`, `isum`/`dot`, and Taylor-series transcendentals
  (`dsin`, `dcos`, `dtan_ratio`, `mp_pi`) with proved remainder bounds, all rigorous
  (endpoints, not point values).
- **Section 2** (leg 176): banded Cholesky, banded triangular inverse, banded matmul —
  flagged non-rigorous (high working precision, not interval-enclosed), exploiting
  `x_gram`'s exact bandwidth-4 structure.

`test_interval_mp.py` (NEW): 13-test adversarial battery against `fractions.Fraction`
ground truth, extending `test_interval_stress.py`'s pattern. It caught three real bugs
before either re-measurement ran on top of them — see §4.

**Not built**: a general arbitrary-precision library. `writeup/novelty/leg_312.md`
names the seven existing ones (INTLAB, MPFI, mpmath's `iv`, Arb/FLINT, kv,
Boost.Interval, Julia's `IntervalArithmetic.jl`) and states why none is importable
(`requirements.txt` dependency ban) and why the scope is deliberately two named
numbers, not their general problem.

## 2. Leg 178's re-measurement

### 2.1 Configuration, read off the banked runner verbatim

`experiments/p2_route_wes_v1_space.py`: `N_QUAD_CHECK = 128`, `GRADE_DEPTHS =
(12, 24, 48, 96)`; the banked reading is `wes_coercivity_gap_exact(128, "T2_egm",
"E", 4.0, n_grade=96)`, i.e. class `T2_egm`, weight family `E` (`E_egm`), `gamma=4`.
`n_unif` defaults to `max(64, 4*128) = 512`. This is the exact call this leg
re-measures — chosen by leg 178's own pre-registration, not by this leg.

### 2.2 Where the precision loss lives

`wes_form_matrices_constrained` forms `F_m = sum_k V[k,m] sin(k*theta)` POINTWISE,
at each of the (here) 7,824 quadrature nodes, before any weight or inner product is
applied — `V` is the exactly-constrained integer basis (`wes_constrained_basis`,
leg 178's own "central instrument finding"), whose columns cancel `F_m` to order
`theta^(2p+1)` by construction. At `theta ~ 3e-31` (the innermost node of the
`n_grade=96` grading), the cancellation needs digits float64's 53-bit mantissa does
not have: the pre-cancellation terms are `O(theta)`, the roundoff floor is
`O(eps*theta) ~ 1e-47`, and the true post-cancellation signal is `O(theta^3) ~
1e-92` — swamped by seven orders of magnitude before it is even that small.

### 2.3 The fix, scoped

Only the 1,640 of 7,824 nodes with `min(theta, pi-theta) < 1e-3` are re-derived
(the rest are far enough from the endpoints that float64's `sin(k*theta)` is
already accurate — verified, not assumed, by leaving them untouched and confirming
the float64-reproduction check in §2.4 matches the banked reading bit-for-bit).
At each unsafe node:

1. `sin(theta)`, `cos(theta)` via an ADAPTIVE-term Taylor series at 120 working
   decimal digits (`_mp_sin_cos` in `experiments/p2_route_apia_v1.py`) — adaptive
   because at `theta ~ 3e-31` a SINGLE term already saturates 120 digits of
   precision (the next term is `~theta^3`, i.e. `~1e-92` relative to the first),
   while the outer end of the graded region (`theta ~ a few e-3`) needs ~15-20
   terms. `solver/interval_mp.py`'s own `dsin`/`dcos` deliberately use a FIXED,
   generous term count (`3*prec+30`) for simplicity and a uniform correctness
   proof; this leg's local adaptive version is a performance optimisation on top
   of that already-tested machinery, not a change to it.
2. `sin(k*theta)`, `cos(k*theta)` for `k=1..128` via the angle-addition recurrence
   (`sk, ck = sk*c1+ck*s1, ck*c1-sk*s1`), `O(k)` Decimal multiplications per node
   instead of re-deriving each `k` from a fresh series.
3. `F_m`, `LF_m` (the linearisation contraction), `HF_m` recomputed as exact
   integer-weighted Decimal sums over `V`'s (at most 4) nonzero entries per column.
4. Converted back to float64 and substituted into the SAME `G`, `B`, contamination,
   and Rayleigh-quotient pipeline `wes_form_matrices_constrained`/
   `wes_coercivity_gap_exact` use (mirrored, not imported, since that pipeline
   does not expose the intermediate `F` this leg needs to patch — `solver/
   energy_coercivity.py` itself is read-only, unedited).

**Certification**: `_mp_sin_cos`'s plain recurrence is spot-checked against
`solver/interval_mp.py`'s RIGOROUS `MPInterval` `dsin`/`dcos` on 6 representative
unsafe nodes; the plain value lands inside the rigorous interval at all 6 (interval
widths `~1e-120`/`~1e-123`) — `spot_check_vs_rigorous_mpinterval.all_contained =
true` in the JSON.

### 2.4 Result

| | banked (float64) | float64 re-derivation (this leg, unpatched) | MP-patched |
|---|---|---|---|
| gap, n_grade=96 | `−230.7108027866136` | `−230.7108027866136` | `+0.4999999874556027` |
| contamination, n_grade=96 | `3066.38495045281` | `3066.38495045281` | `48708.87` (see caveat) |
| gap, n_grade=48 (clean cross-check) | `+0.49999975272293995` | — | — |

The float64 re-derivation matching the banked reading bit-for-bit (row 2 of the
table) confirms this leg's mirror of `wes_form_matrices_constrained` is faithful
before any patch is applied. The MP-patched gap, `+0.4999999875`, agrees with the
clean `n_grade=48` reading (`+0.49999975`) to five significant figures and with
every other clean depth's `+0.5` ceiling.

**Caveat on the "contamination" number after patching**: the `contamination`
diagnostic is `(eps*Fabs)^2*pw / F^2*pw` — a bound on FLOAT64's OWN roundoff
relative to the signal. Applied to the MP-patched `F` (now near its true,
correctly-tiny value rather than float64's spuriously large garbage), the same
formula's denominator shrinks, so the ratio goes UP — this is an artifact of
reusing a float64-specific diagnostic on a corrected numerator, not evidence that
the MP-patched value is itself contaminated (see the rigorous interval spot-check
in §2.3, and the gap's agreement with the clean-depth ladder). The honest reading
of "does arbitrary precision change the contamination number" is: yes, but that
specific diagnostic formula was never designed to answer "is the arbitrary-
precision result trustworthy" — the gap comparison is.

## 3. Leg 176's re-measurement

### 3.1 Configuration

`experiments/p2_route_h2c_v1_construction.py`: `rect_sigma(N, bordered=True,
gram=True, lo_mode=0)` at `N=1024` (`SIG_N`'s own top rung), cross-checked at
`N=512` (`REL_N`'s own top rung, "the float-reliable window").

### 3.2 Where the precision loss lives, and the substitution

`rect_sigma` whitens the bordered operator `A` via `Gch @ A @ Gdih`, where `Gch =
sqrt(Gc)`, `Gdih = sqrt(Gd)^{-1}` are computed by `origin_h2_certificate._sym_sqrt`
— a dense `np.linalg.eigh`-based SYMMETRIC matrix square root. `Gd`, `Gc` are
`bordered_gram(x_gram(...))`: block-diagonal, with `x_gram(N) = I + J^4` exact and
banded (bandwidth 4), condition number reaching `~1e13` at `N=1024`.

**Mathematical substitution, not an approximation**: for SPD `G = R^T R` (ANY
valid factorisation — a Cholesky factor works exactly as well as the symmetric
square root, since two factorisations of the same inner product differ only by a
unitary, which does not change singular values), `||Ax||_G = ||Rx||_2`. So the
singular values of `Rc @ A @ Rd^{-1}` (Cholesky factors) equal those of `sqrt(Gc)
@ A @ sqrt(Gd)^{-1}` (symmetric square roots). This leg computes `Rd = banded_
cholesky(Gx_d, ..., bw=4)`, `Zd = banded_triangular_inverse(Rd, ...)` (`O(N^2*bw)`,
not `O(N^3)`), and applies `Rc` via `banded_matmul` — never forming a dense
eigendecomposition of the ill-conditioned Gram matrix at all.

Since `Gd`, `Gc` are EXACTLY block-diagonal (the border amplitude carries an
uncoupled weight of 1), their Cholesky factors and inverses are block-diagonal too
— the dense (Nr+1)x(nd+1) solve degenerates to one `O(N^2*bw)` banded triangular
inverse plus one `O(N^2)` dense border-row product (the border row itself,
`border_row`, is dense by construction).

`A = A_re + i*A_im` splits cleanly: `A_re` is the REAL tridiagonal `l0_plus` block,
`A_im` carries the (purely imaginary) symmetry-mode column and border row. Every
Decimal matrix operation is therefore on REAL matrices — no complex Decimal
arithmetic anywhere; only the final (by-then well-conditioned) SVD, done in
float64, recombines `W = W_re + i*W_im`.

Working precision: 60 decimal digits (`L176_PREC`), chosen generously above the
~13 decimal digits of condition-number-driven loss `_sym_sqrt` suffers at
`N=1024`.

### 3.3 Result

| N | banked (float64) `sigma_min` | MP-patched `sigma_min` |
|---|---|---|
| 512 (reliable window) | `0.09080465147034879` | `0.0908041438359524` |
| 1024 | `0.09093626075500859` | `0.09079112560266907` |

The banked `N=1024` reading is HIGHER than the banked `N=512` reading — a direct
violation of `rect_sigma`'s own documented monotone-non-increasing shape (nested
trial spaces). The MP-patched `N=1024` reading, `0.09079113`, sits BELOW the
`N=512` value, restoring the expected shape, and is close in magnitude to the
banked value (`0.16%` relative change) — a real but small correction, unlike leg
178's sign flip.

The `N=512` cross-check between float64 and MP agrees to `5e-7` absolute
(`0.09080465` vs `0.09080414`), confirming this leg's banded-Cholesky substitution
reproduces the "reliable window" faithfully before trusting its `N=1024` output.

## 4. Adversarial battery: three bugs found and fixed

`test_interval_mp.py`'s `test_pi_matches_known_digits` — an EXTERNAL ground-truth
comparison (a textbook pi digit string), not an internal self-consistency check —
caught three real bugs in `interval_mp.py`'s transcendental path before either
re-measurement ran on top of them:

1. `_atan_small`'s term recurrence was missing a `(2k-1)/(2k+1)` ratio factor.
2. Several steps used Python's bare `abs()`/unary `-` on `Decimal`, both of which
   silently round to the AMBIENT thread-local decimal context (28-digit default)
   rather than the module's own `prec`-digit context — invisibly truncating any
   value with more than 28 significant digits, no error, no warning. Fixed with
   `Decimal`'s context-independent `.copy_abs()`/`.copy_negate()`.
3. `mp_pi`'s `Decimal(1) / Decimal(239)`, computed OUTSIDE any explicit context:
   1/239 does not terminate in decimal (unlike 1/5), so this division ALSO rounded
   silently to 28 digits and was then treated as an EXACT input by a series that
   assumes exact inputs. Fixed by enclosing `1/239` in a rigorous `MPInterval`
   (via `mp_div`) and generalising `_atan_small` to accept an interval-valued
   input, propagating the tiny-but-real uncertainty through the whole series.

All three fixes are in `solver/interval_mp.py`; `test_interval_mp.py` (13/13
tests) is the battery that would catch a regression of any of them, plus checks
on `dsin`/`dcos` against an independent `Fraction`-based Taylor reference, the
exact leg-178-regime theta (`3e-31`), zero-crossing guards failing closed, and
`banded_cholesky`/`banded_triangular_inverse`/`banded_matmul` against exact
`Fraction` arithmetic on random banded SPD matrices.

## 5. Performance

Both re-measurements were assessed for cost before the long combined run, per
`CONTINUATION_PROMPT.md`'s binding rule:

- Leg 178: initial profiling showed `solver/interval_mp.py`'s own fixed-term-count
  `dsin`/`dcos` would cost `~0.1s`/node — at ~1,640 unsafe nodes, `~3` minutes,
  acceptable but improvable. The runner's local adaptive-term series
  (`_mp_sin_cos`) cuts this to `~0.007s`/node (measured: `25.9s` total for 1,640
  nodes, `15.8ms`/node including the full `F`/`LF`/`HF` dot products over 126
  basis columns) by exploiting that `theta ~ 3e-31` needs only ONE Taylor term at
  120 digits, not the fixed conservative count.
- Leg 176: profiled at `N=64/128/256` first (`0.14s/1.2s/6.5s`) to extrapolate
  before committing to `N=1024`; measured `N=1024` cost was
  **[CORRECTED 2026-08-12, leg 338 — Route-LCB1: originally read `117s`; the
  banked JSON is authoritative and is cited directly below]**
  `100.553s` (`N1024_seconds` in `writeup/data/p2_route_apia_v1.json`), `N=512`
  cross-check **[CORRECTED 2026-08-12, leg 338: originally read `48s`]**
  `35.515s` (`N512_seconds`, same file).
- Combined total measured wall time **[CORRECTED 2026-08-12, leg 338: this
  paragraph originally reported `346s` (`25.9s + 309.0s`), a sum that does not
  itself add up (`25.9 + 309.0 = 334.9`, not `346`), and is non-claim-bearing
  prose — recorded here rather than re-derived]**: `345.478s`
  (`total_seconds` fields in `writeup/data/p2_route_apia_v1.json` — leg-178's
  `36.480s` plus leg-176's `308.998s`, both fields already in the JSON and
  unchanged by this correction), well under the 10-minute budget — no long run
  was needed to answer the gate.

## 6. Integration note (no dependency change proposed)

`solver/interval_mp.py` and this leg's runner use only `decimal` and `fractions`
(stdlib). No addition to `requirements.txt` is proposed.

**Downstream consumers to flag** (this leg reads but does not edit any of these;
territory is `solver/interval_mp.py`, `test_interval_mp.py`,
`experiments/p2_route_apia_v1.py`, `writeup/data/p2_route_apia_v1.json`,
`writeup/novelty/leg_312.md`, `experiments/journal/leg_312.md`, plus this leg's
own quartet files under `writeup/4_p2_lottery/` and `experiments/`):

- **Leg 178's own headline** (`writeup/data/p2_route_wes_v1_space.json`,
  `writeup/4_p2_lottery/{BLOG,TECHNICAL}_P2_WES_V1.md`, `experiments/journal/
  leg_178.md`, `DIRECTION.md`, `experiments/journal/leg_272.md`): all quote the
  `3.1e+03` contamination / `−230.71` reading as the diagnostic that the
  instrument (not the mathematics) breaks past a scoped grading depth. This
  leg's finding SUPPORTS that reading's own interpretation (the −230.71 really
  was an artifact) rather than contradicting it — no change to leg 178's own
  YES gate answer is implied, but a reader following the `3.1e+03` number
  specifically should know it is now independently confirmed as a float64
  artifact, not an open question.
- **Leg 176's own headline** (`writeup/data/p2_route_h2cv_v1_postconstruction.json`
  and siblings, `writeup/CORRECTIONS.md`, `writeup/curate_evidence.py`,
  `DIRECTION.md`): the `N=1024` `sigma_min` row is corrected from `0.09093626`
  to `0.09079113`; any prose that cites the banked `N=1024` value specifically
  (rather than the `N<=512` reliable window, which this leg's `N=512` cross-check
  confirms is unaffected) should be updated to the corrected figure or flagged
  as pending re-derivation.

Neither correction moves a link of the L1→L4 chain — both source legs are
explicitly exploratory, not on the critical path, and the corrections are
internal-consistency repairs (monotonicity restored, an artifact identified),
not new mathematical claims. Clay odds stay ~0.05%.
