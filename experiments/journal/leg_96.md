# Leg 96 — Route-LHA v1: adversarial audit of `solver/line_hilbert.py`'s dense operator

**Branch** `leg/lha-v1`. **Exploration leg, standard, CLAIM-BEARING** (robustness of a shared
module — six solvers import it).
**Gate: NO.** 0 silent corruptions in 25 in-scope cases; worst module-vs-independent-reference
disagreement **3.07e-13** (dense operator) and **7.04e-16** (slope operator) against a
pre-committed 1e-08 threshold. Confirmed robust; battery banked as a permanent regression test.
Lands normally on `main`. **`solver/line_hilbert.py` was not edited.**

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read in full. `NG` is NEXT. All ten live bans read against this leg;
   two are live and neither bites: *another gCLM measurement leg* (this leg produces no profile,
   no `a`-sweep, no exponent, and no claim about blow-up — the CLM pair appears only as a known
   answer to score code against, the same use `test_line_hilbert.py` already makes of it; the
   robustness-vs-measurement distinction that cleared legs 83, 85, 88, verified independently
   rather than inherited), and *build nothing without grepping `capabilities.py` first* —
   discharged, `capabilities.py:57-62` read in full and quoted in the novelty log.
2. `DIRECTION.md` leg-96 entry read and cross-checked against the dispatch prompt. They agree
   verbatim, including the territory list and both gate branches.
3. Prior art read as source, not description: `solver/line_hilbert.py` in full (303 lines, the
   whole docstring including the `L(s)` cancellation-removal derivation), `test_line_hilbert.py`
   in full (7 tests), the `capabilities.py` entry, and the grid construction of all six
   consumers (`hl_rescaled`, `gclm_rescaled`, `gclm_family`, `bordered_hl`, `weight_search`,
   `interval_certificate`) to establish whether any pathology found would be live or latent.
4. **Novelty pass FIRST**, committed before any construction (`fb8fba5`), in
   `writeup/novelty/leg_96.md`. Its verdict: unasked in-repo. Its most load-bearing content is
   not the prior-art table but the design constraint recorded in the "External literature"
   section — that the battery must separate error the mathematics forces on any correct
   implementation from error this implementation introduces. That constraint was written down
   **before** the numbers existed, and it is what stopped the leg reporting a false YES.
5. Exploratory probes, then construction, then the finish protocol.

## What was built

The documentation quartet, all inside declared territory:

- `experiments/p2_route_lha_v1_adversarial.py` — the battery runner, carrying the independent
  reference implementation.
- `writeup/data/p2_route_lha_v1_adversarial.json` — curated data, 28 case records plus the
  reference self-check.
- `test_line_hilbert_adversarial.py` — 8 permanent regression gates (5 soundness, 3
  characterization).
- `writeup/novelty/leg_96.md` — the novelty log and the findings at full depth.

No figure required by the contract, and none was produced.

## The one decision that determined the outcome

The obvious battery — perturb the grid, transform the CLM pair, compare against the exact
`H(f) = 2/(1+4X²)` — **cannot answer this gate**, and running it alone would have produced a
confident, wrong YES. Three in-scope cases miss the analytic answer by **1.3e-02**, **2.9e-01**
and **1.3e+02** relative while the code is exact to rounding. Degenerate grids make the spline
interpolant a bad representation of the field; that error is what any correct implementation of
Huang–Tong–Wang App. C.1 must produce.

So the leg built a second implementation of the same discretization sharing no formula with the
module — pivoted dense LU against the module's unpivoted Thomas sweeps, and exact per-cell Cauchy
integration by polynomial deflation against the module's `A(s)`/`B(s)` closed forms — and made
the verdict criterion a **module-vs-reference** comparison, with the analytic answer demoted to a
grid-quality diagnostic that is reported and never scored.

The reference was gated on healthy grids (full N×N matrix agreement **7.9e-15**) before being
trusted on hostile ones. That gate caught the reference's own first bug: a dropped
log-cancellation between adjoining cells, presenting as a clean O(h) bias at the 2e-02 level,
which without the gate would have been read as a module defect. **The self-check is not
ceremony** — it is the step that makes the construction safe, and it is banked as
`test_reference_selfcheck` so a later leg cannot quietly break the reference and keep the
verdict.

## Result

25 in-scope cases across near-duplicates (separations down to **1 ulp**, forward and crossed,
at the edges, in the tail, and 19 at once) and extreme local stretching (spacing ratios to
**1.0e+148**, minimum spacing **7.4e-146**, `‖S‖∞` to **4.0e+145**). Zero silent corruptions.
The exact-duplicate boundary case is loud: **100% non-finite, 16 warnings**.

The slope half of the gate has a structural answer worth not re-measuring: the interior
tridiagonal system is **strictly diagonally dominant by a factor of exactly 2 for every grid**,
so the unpivoted sweeps can never need a pivot — measured at **7.0e-16** against pivoted LU on
every degenerate grid, and now recorded as a *reason* rather than an observation.

Two out-of-gate findings, reported and pinned as characterizations, neither patched (no edit
authority over the module under any outcome):

- **C1.** `capabilities.py`'s "matches the Thomas sweeps to 2.7e-13" is a healthy-grid figure; on
  a one-ulp grid the same ratio reaches **2.5e-01**. The operator is not losing accuracy —
  normalized by `‖S‖∞‖f‖∞` the disagreement never leaves **1e-16** while `‖S‖∞` spans 144 orders
  of magnitude. Route-M's exactness claim stands; its *number* must not be read as
  grid-independent.
- **C2.** Grid **monotonicity** is an unstated precondition. A descending grid returns exactly
  `−H(f)` — agreeing with the negation to **8.9e-16**, finite, correct peak magnitude, zero
  warnings. Out of the gate's stated scope, so not counted toward the verdict. Latent rather than
  live: all six consumers build ascending `sinh` grids, checked directly. A future leg with edit
  authority could close it with a two-line `np.diff(x) > 0` assertion.

Full magnitudes and the honest limits of the NO are in `writeup/novelty/leg_96.md`.
