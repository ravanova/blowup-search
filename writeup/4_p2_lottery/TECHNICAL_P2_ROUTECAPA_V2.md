# TECHNICAL — Route-CAPA v2: the second-generation freshness audit of `capabilities.py`

**Leg.** 292. **Branch.** `leg/292-capa-v2`. **Base.** `80c0cc4`.
**Runner.** `experiments/p2_route_capa_v2_audit.py`
**Data.** `writeup/data/p2_route_capa_v2_audit.json`
**Figure.** `writeup/figures/fig67_route_capa_v2_audit.png`
**Predecessor.** Leg 71 (Route-CAP), first generation, 42 rows / 40 tests at `e203b52`.

---

## 1. What is under audit, and why an index needs auditing at all

`capabilities.py` is this repository's answer to a question neither `plan_of_record.py`
("what is next") nor `PHASE2_P2_NOTES.md` ("what happened") answers: **what do we
already have.** It exists because Route-M (leg 45) came within about ten minutes of
rebuilding a Scenario-2 integrator that had been sitting in `solver/hl_rescaled.py`,
validated to 4.4e-16, for eleven days. The plan of record carries a standing ban with
no lift condition — *building a solver without grepping `capabilities.py` for the object
first* — and a ban of that shape is only as strong as the index's accuracy.

Each row records four fields: `object` (the mathematical object, the key you search on),
`holds`, `validated` (the strongest known-answer gate it passes, **with the magnitude**,
or "no known-answer gate" said plainly), and `test`.

The automated drift detector `test_capabilities.py` enforces exactly three things:

1. the `test` field is non-empty,
2. the cited path exists on disk,
3. `validated` is longer than 20 characters.

Leg 71 stated the resulting gap precisely. That the gap is *unchanged* is not asserted
from a re-read here — it is measured:

```
git log --oneline e203b52..80c0cc4 -- test_capabilities.py      ->  0 commits
```

**Zero commits have touched the drift detector between leg 71's own merge base and this
one.** It is byte-identical, with the same five tests
(`test_every_solver_module_is_indexed`, `test_entries_are_complete_and_point_at_real_files`,
`test_objects_are_distinct_enough_to_search_on`,
`test_the_search_finds_the_thing_route_m_nearly_rebuilt`, `test_superseded_modules_say_so`),
while the index it guards grew by 6 rows over ~220 legs. So leg 71's statement holds
verbatim today:

> It does not check that the cited test **runs, passes, or has anything to do with the
> module citing it.** Existence is checked; greenness and relevance are not.

Leg 71 closed the *greenness* half by hand, once, ~220 legs ago. This leg re-asks it and
closes the *relevance* half as a standing, executable check.

## 2. Method: five axes, each reported as a count

| axis | question | how measured |
|---|---|---|
| **S1** | module completeness, both directions | set difference between `{row["module"]}` and `solver/*.py` on disk (ex-`__init__.py`) |
| **S2** | cited-test existence | every `*.py` token in every `test` field resolved against disk |
| **S3** | **greenness at HEAD** | every distinct cited test file *executed*, `rc == 0` recorded with wall time |
| **S4** | known-answer-gate presence | `validated` classified: names a magnitude / says "no known-answer gate" / prose with no number |
| **S5** | **relevance** | does the cited test's source (plus any sibling helper it imports, one hop) reference `solver.<stem>` at all |

S3 and S5 are the two the drift detector structurally cannot do; S1, S2 and S4 are
re-measurements of things it does partially.

### 2.1 Operational note carried forward from leg 71, and it was earned

Leg 71's second commit (`e742f6d`) recorded a measured, not guessed, execution hazard:
at **6** parallel workers the box thrashed — `test_marginal_flow.py` went
**112 s → >3600 s, a 32x blowup** consistent with BLAS thread oversubscription. At **3**
workers there were no timeouts and the same 40 tests cost **8,426 s against 22,839 s**,
37% of the cumulative time.

This runner therefore pins `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`,
`NUMEXPR_NUM_THREADS` and `VECLIB_MAXIMUM_THREADS` to `1` in **every child process**, and
exposes `--workers` so the number actually used is written into the JSON rather than
assumed by a later reader. This audit ran at 2 workers, on a box already carrying other
legs (load average 14–25 against 12 cores), which inflates wall times and is stated here
so the cost panel of the figure is read as an upper envelope, not a clean benchmark.

### 2.2 Flake diagnosis before belief

Per `ORCHESTRATION.md` §9g, a non-zero return under a loaded parallel sweep is **not**
evidence of red-at-HEAD. The runner exposes `--recheck`, which re-runs named tests alone,
serially, under the same pinned environment, and records the solo verdict *alongside* the
sweep verdict rather than replacing it — the two disagreeing is itself the finding (a
flake), not an inconvenience to be smoothed away. This is the discipline that produced
`94bde64` ("Newton item (6) RECONCILED: not red, not green, FLAKY").

<!--S3RESULTS-->

## 3. S1 — module completeness

| quantity | count |
|---|---|
| rows | 48 |
| distinct `module` values | 48 (0 duplicates) |
| `solver/*.py` on disk (ex-`__init__.py`) | 48 |
| missing (on disk, no row) | **0** |
| ghost (row, not on disk) | **0** |

Exact set equality both ways. Leg 71 audited 42 rows; six modules have been added since,
across ~220 legs, with zero completeness defects. The novelty pass predicted this in
writing before measuring, on the grounds that `ORCHESTRATION.md` §5a makes a landing leg
append its own row **on the commit that adds its module**, so completeness is
self-maintaining rather than something 220 legs of drift can erode. That prediction is
confirmed.

`solver/bc_weighted_sobolev.py` — the module the leg brief named explicitly as the test
case — is present with a full magnitude-bearing `validated` field (Breden-Chu Theorem 42
reproduced end to end at their own n = 1500; independently shot-and-Newton'd `ubar`
matching their released coefficients to 4.36e-10 in H²(mu); Y to 6.0e-05 relative; the
Z1/Z2 discrepancies 1.31x/0.81x localised by ablation to their L^∞ bounds on psi_m,
where their own code overshoots the measured sup by up to 136x; ceiling stated as
float64, not interval arithmetic).

## 4. S2 — cited-test existence

0 rows with an empty `test` field; 0 rows citing a file absent from disk; 46 distinct
cited test files. This is the one axis the drift detector genuinely enforces, so the
clean result is a check on the detector rather than on the index.

## 5. S4 — the `validated` contract, measured

| class | count of 48 | share |
|---|---|---|
| names a magnitude | 33 | 69% |
| says "no known-answer gate" plainly | 3 | 6% |
| claims validation, names no number | 12 | 25% |

The file's own header defines the contract: `validated` is "the strongest KNOWN-ANSWER
gate it passes, **with the magnitude**, or 'no known-answer gate' said plainly". So 36
of 48 rows (75%) satisfy it *in the letter*, and 12 satisfy it only in spirit:
`op_lower`, `decay_collocation`, `collocation_newton`, `reduced_certificate`,
`nk_fourier`, `nk_seminorm`, `turning_point`, `profile_newton`, `advection_scope`,
`target_selection`, `ga_search`, `finite_support`.

**These 12 are reported as a shape, not as 12 defects, and are deliberately not
rewritten.** Read individually most are honest about their own limits in words rather
than numbers — `reduced_certificate` says "explicitly NOT a proof — float64 throughout";
`nk_fourier` and `nk_seminorm` both say "no independent published known answer";
`finite_support` says "nothing — SUPERSEDED". Supplying magnitudes for another leg's
module from an audit chair would be fabricating exactly the kind of claim the
`validated` field exists to constrain. The useful, reportable quantity is the rate —
**75% of rows carry a number or an explicit disclaimer** — and the named list of 12, so
that any future leg touching one of those modules knows its row is the cheapest place in
the repository to bank a magnitude it already has.

There is a visible correlation worth recording: 11 of the 12 are Route-D-era or
plumbing modules (the `nk_*`/`collocation_*`/`decay_*`/`op_lower`/`turning_point`/
`advection_scope` cluster plus `ga_search` and the superseded `finite_support`), i.e.
the oldest and the most auxiliary. Every module registered since leg ~110 —
`energy_coercivity`, `certificate_guards`, `chen_inviscid_certificate`, `target_norm`,
`bc_weighted_sobolev`, `certificate_shapes` — carries magnitudes, usually several, and
an explicit CEILING clause. The `validated` convention has tightened over the
repository's life, and the 12 are its sediment rather than its current practice.

## 6. S5 — relevance, the axis leg 71 named and never systematised

For each row the runner scans the cited test's source, plus the source of any sibling
top-level module it imports (one hop, so a dedicated test importing a shared harness is
not falsely flagged), for `solver.<stem>`, `solver/<stem>.py` or `import <stem>`.

**1 of 48 rows fails.**

| row | cited test | occurrences of the module's name |
|---|---|---|
| `solver/finite_support.py` | `test_first_integral.py` | **0** |

Hand-verified rather than trusted to the scanner: `grep -n finite_support
test_first_integral.py` returns nothing whatsoever. The row was pointing the repository's
one SUPERSEDED module at a test that cannot fail when that module breaks — which is
strictly worse than an empty `test` field, because the drift detector passes it and a
reader takes it as coverage.

Simultaneously, `test_finite_support_adversarial.py` (leg 124, 22.6 kB) **exists on
disk, opens with `from solver.finite_support import ...`, and is cited by no row in the
index.** Run alone at HEAD under the pinned environment it returns **rc = 0**, and its
gate **S10** checks precisely the property the row's `validated` field asserts:

```
[ok] S10 zero importers, and the SUPERSEDED / DO NOT USE banner is intact
    importers of solver.finite_support outside leg 124's own files: 0
```

So the corrected pointer is not merely *a* test that loads the module — it is the test
that re-checks the sentence the row makes its claim in.

**Repair applied**, following leg 71's `solver/ga_search.py` precedent to the letter:
the `test` field is repointed to `test_finite_support_adversarial.py` with an inline
comment recording the evidence and the reasoning, and `validated` is **left frozen**.
This leg corrects factual pointers; it does not re-word other legs' claims.

That both instances of this defect (leg 71's `ga_search.py`, this leg's
`finite_support.py`) are *superseded-or-auxiliary* modules is the mechanism, not a
coincidence: a row whose module nobody imports is a row nobody re-reads, so its pointer
is the one most free to rot. The check is now executable, which is the only form of
check this repository trusts (banked lesson 68: *a check that is not executable decays
at the rate of memory*).

## 7. Negative controls that could have fired

1. **The `(N checks)` arithmetic claims.** Three `validated` fields make a literally
   falsifiable claim about a file's contents: `test_boussinesq_dedicated.py (17 checks)`,
   `test_gclm_dedicated.py (14 checks)`, `test_spectral_utils_dedicated.py (10 checks)`.
   The runner counts `^def test_` in each and compares. **3 of 3 agree exactly.** This
   control had a live way to fail — a leg adding a check without touching the row — and
   did not.
2. **The S5 scanner's discrimination.** It clears `solver/certificate_guards.py`, whose
   row cites `test_nk_bounds_adversarial.py`, a file named after a *different* module.
   Hand-check: that file does `import solver.certificate_guards as cg` at line 528. So
   the scanner is not matching filename against module name; it separates a genuinely
   relevant cross-named citation from an irrelevant same-family one. Had it been a
   filename matcher it would have produced a false positive here and a false negative on
   `finite_support`, which cites a same-family file.
3. **The drift detector after the edit** — `test_capabilities.py` re-run post-correction:
   five tests pass, 48 distinct object keys, 1 superseded module correctly labelled.

## 8. Scope and ceiling

- This is an audit of an **index**, not of any mathematical object. No constant is
  banked, no bound is computed, no link of the L1→L4 chain moves. **Clay odds unmoved at
  ~0.05%.**
- **S4 is not closed.** The 12 magnitude-free rows are named and counted, not repaired;
  repairing them requires the leg that owns each module, not this one.
- **S5 is a static scan.** A test that imports a module and then never calls it would
  pass S5. The check is a *lower* bound on irrelevance — it catches pointers that cannot
  possibly exercise the module, not pointers that exercise it weakly.
- **S3's wall times are an upper envelope**, measured on a box concurrently running other
  legs at load 14–25 on 12 cores. The greenness verdicts are unaffected; the timings
  should not be quoted as a benchmark.
- The audit is a **snapshot at `80c0cc4`**. Its half-life is exactly the rate at which
  new modules land — which is why the S5 check ships as code in the runner rather than
  as a paragraph in this document.
