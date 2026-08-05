# Leg 78 — Route-HLB: how precise is the known answer itself?

Literature search plus a known-answer re-measurement. **Nothing in `solver/` was modified**:
`solver/hl_rescaled.py` was read (never opened for writing) and `solver/bordered_hl.py` was
imported read-only to re-run its reach ladder live. `capabilities.py` was grepped first, per the
plan of record — entries at line 45–52 (`hl_rescaled`, the `~1%` annotation under audit) and line
296–307 (`bordered_hl`, the same anchor at 2.1e−04). No shared ledger was touched. Runner:
`experiments/p2_route_hlb_v1_contraction_lit.py` → `writeup/data/p2_route_hlb_v1_contraction_lit.json`
(210 s). Full prose and every query string is in `writeup/novelty/leg_78.md`.

## The gate, answered

> **Does a primary source publish the Scenario-2 contraction ratio to tighter precision than the
> ~1% figure this repository currently checks against, and if so does our number still agree at
> that tighter tolerance?**

**NO TIGHTER VALUE FOUND, as of 2026-08-06.** Five channels, **0** returning a sixth digit or an
independent replication. The no-branch lands: `−2.5114` is banked as the best precision on record
and **no file changes**.

But the interesting half is *why* the answer is "no", and it is not the shape the leg brief
anticipated.

## §1 — The `~1%` was never the anchor's precision. It is ours.

The anchor `−2.5114` is five significant figures: last printed digit `1e−4` absolute =
**3.98e−05 relative**. That is **251× tighter** than the `~1%` tolerance
`capabilities.py`:51 records the check at. The loose side of that comparison was never
Chen–Huang–Li — it is this repository's relaxation line. So the premise "a loose tolerance that
has sat unrevisited" is correct, but the looseness is **ours to fix, not theirs to publish**.

## §2 — The anchor cannot be tightened from outside, on five independent channels

| # | channel | result |
|---|---|---|
| P1 | full text of arXiv:2604.01868 | the constant occurs **twice**, `−2.5114` both times; **no table of constants**, no error bar, no resolution or domain study; the second occurrence carries an explicit `≈` |
| P2 | the figures | **raster, not vector** — 90 embedded images, Fig 4.2 at 3125×2500 px, so reading the dashed limit line gives **4.0e−04** relative at best, ~10× coarser than the caption. Leg 48's `read_df_figure` route is closed here |
| P3 | released artifacts | **none** — 0 grep hits for github / code availability / data availability / supplementary / zenodo |
| P4 | version + journal record | **v1 only**, 2 Apr 2026, `51 pages`, **no journal-ref** — 126 days, and a journal version is where a constants table would appear |
| P5 | replication | **0 citing works** (Semantic Scholar); 1 new "Hou-Luo" arXiv entry since (2605.16322, a boundary-jet Riccati argument, reports no ratio); **0** author submissions after the source; the companion 2603.25104's **v2 (16 Jun 2026)** was pulled and grepped — 0 hits |

## §3 — The number CHL publish is a print precision, not an error bar

Worth stating because it is the thing that would be mis-read next. CHL report `−2.5114` from a
relaxation stopped at `max{‖Ω_t‖_∞, ‖V_t‖_∞} < 1e−6`, with **no** error bar, **no** resolution
study and **no** domain-size study for the constant, and print it once as `≈`. This leg claims
the figure is the **best available**, and explicitly does **not** claim it is accurate to five
digits. Digit granularity is not an error bar and was not converted into one.

## §4 — The counterfactual, answered with a number: a sixth digit would be unusable today

The obvious follow-up question — "so should we go get a tighter anchor?" — is settled by our own
side of the comparison. The bordered line's limit, extrapolated in reach, spreads by
**9.74e−05 relative across its extrapolation windows**, i.e. **2.4×** the anchor's print
granularity. The comparison is already saturated on our side at ~1e−04. `−2.5114` is not merely
the best anchor available; it is **finer than this repository's best line can currently resolve
against**.

## §5 — The measured magnitudes (re-measured, not quoted)

The bordered reach ladder was **re-run live** by this leg's script at `n = 301`,
`rho_max = 7…11` (`X_max = 274 … 14969`), Newton residuals **9.3e−15 / 6.9e−15 / 6.1e−15 /
7.9e−15 / 5.0e−15**; the relaxation line is read from its own logged run
(`writeup/data/p2_scenario2_relax.json`, n=801, 14000 steps).

| line | ratio | rel. err vs −2.5114 | × the anchor's 3.98e−05 granularity |
|---|---|---|---|
| relaxation, `RescaledHLScenario2` | −2.53344 | **8.78e−03** | **220×** |
| bordered Newton, extrapolated in reach | −2.51192 | **2.09e−04** | **5.3×** |
| our extrapolation's own window spread | — | 9.74e−05 | **2.4×** |

Two independent ICs on the relaxation line (x0 = 0.30 / 0.45) agree to **7.0e−04** relative, well
inside their own 8.8e−03 offset — the line is converged to its own floor, and that floor, not
resolution, is what the 0.88% measures. An independent short re-run of the same line
(3000 steps instead of 14000) sits at **−2.6940, residual 7.2e−02 = 7.3e−02 relative**, i.e. still
in transit: the 0.88% is a property of the *fully relaxed* line.

**One method note, banked.** The first execution of this script cold-started a `rho_max = 6.0`
rung that **stalled at residual 3.3e−02** and still returned a plausible-looking ratio
(−2.551364 against the warm-started reference's −2.583087). Fed into the Aitken extrapolation it
moved the limit from 2.09e−04 to **3.07e−04** — a 47% inflation of the headline error from one
silently-unconverged rung. The script now admits only rungs with residual ≤ 1e−12 into the
extrapolation and records what it dropped. *A ladder point that did not converge is a different
object, and an extrapolator cannot tell.*

## §6 — Flag raised, NOT acted on

`capabilities.py`:51 reads *"the Scenario-2 contraction ratio reproduces CHL's −2.5114 to ~1%"*.
True of `hl_rescaled.py`. But line 304 already records `bordered_hl.py` reaching **2.1e−04**
against the same anchor, so the line-51 phrasing understates this repository's best agreement
with CHL by **42×**. This is a **report-only** flag for whichever leg owns `capabilities.py`.
**This leg did not edit it**, and there is no bug: nothing disagrees, the two lines bracket the
anchor from the same side at two different accuracies.

## What did not move

No link of the L1→L4 chain. Clay stays ~0.05%. No novelty claimed about the Hou–Luo model; the
leg's output is a dated statement about the published record's precision, and a pair of
magnitudes for our own.
