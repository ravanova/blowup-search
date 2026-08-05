# Leg 63 — Route-M2 v1: target reselection, screened by the measured predicate

**Branch** `leg/m2-v1`. **Exploration leg** (not critical path). **Claim-bearing.**
**Gate: YES — which is escalation #1, so this branch is PARKED: pushed as a branch, `main`
untouched, nothing promoted.**

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read (via the main checkout's `.venv`; the worktree had none, so a
   symlink was made — untracked, `.gitignore`d, not part of the diff). Stage `NG` is `NEXT`;
   every live ban noted. Three bind this leg and are addressed explicitly below.
2. `DIRECTION.md` — leg 63's queue entry read in full; thesis and gate wording taken from it
   and from the dispatch brief, which agree.
3. **Novelty pass FIRST, committed before any construction** — `writeup/novelty/leg_63.md`,
   commit `9efd69c`, five verbatim queries, **links not counts**.
4. `capabilities.py` grepped before building. `solver/spectral_certificate.py` already owned
   `tail_block`, `tail_inverse_norm`, `bordered_tail_inverse_norm` and a `Lambda^1`
   dissipation dial; `solver/certificate_shapes.py` (leg 57) already owned `decay_exponent`,
   `m_divergence` and the shape vocabulary; `solver/fractional_gclm.py` already owned the
   criticality exponent `s_c = alpha/2`. **All four were imported, none rebuilt.** What did
   not exist is a dial in the ORDER of the dissipation, which is the only coordinate that can
   separate candidate models, and that is the whole of the new machinery.
5. Module, tests, runner, data, figure, writeups — in that order.

## What the novelty pass changed about the leg

It changed the expected answer, before anything was built. The leg was dispatched expecting
to confirm exhaustion: the thesis anticipated that the multiplier-shaped candidates would all
be dissipative and therefore blocked. The pass found the sharper fact — **there is a model
where dissipative blow-up is PROVED at an order that is unambiguously multiplier-shaped**
(Chen, arXiv:1908.09385, `a` close to `1/2`, `gamma = 2`, analytically). That single located
sentence is what makes the gate answer YES rather than NO, so it was written into the novelty
file with its provenance and its caveat (abstract, not full text) *before* the measurement
existed to be tempted by.

The pass also re-confirmed, per leg 57, that **the screen itself is not a finding**. The
multiplier/shift dichotomy is folklore in print (Cadiot arXiv:2505.03091 §2, §3). Every
writeup says so at the top rather than in a caveat at the bottom.

## The three bans that bind this leg, and how each is respected

* **"another gCLM measurement leg" (lifted by: never).** No gCLM dynamics were run. The only
  gCLM numbers here are constants already transcribed into stage M's ledger, used in
  arithmetic (`survival_window`), plus a criterion (`s_c = alpha/2`) that
  `solver/fractional_gclm.py` already validated against XU eq (6.3). The runner records
  `no_solver_was_run: true` in the JSON so the next agent does not have to take my word.
* **"re-opening stage V as posed" (lift condition: a FLUID transport model, which needs L1
  first).** This leg does not re-run stage V's question, does not claim viscous survival, and
  does not promote a dissipative row. It *records* that the ban's lift condition is now the
  binding constraint on the only multiplier-shaped rows in the ledger, and that L1 is measured
  dead in both realizations — and it says explicitly that whether that lift can ever be met is
  a **user call this leg surfaces and does not make**.
* **"building a solver without grepping capabilities.py first."** Done; see step 4.

## What was reused rather than rebuilt

`tail_block`, `bordered_tail_inverse_norm` (`solver/spectral_certificate.py`);
`decay_exponent`, `MULTIPLIER`/`SHIFT`/`TRIDIAGONAL_DOMINANT` (`solver/certificate_shapes.py`);
`uncertified_targets`, `cost_ratio_vs_certified`, `TARGET_LEDGER` (this module, stage M).
Written new: the order dial `fractional_tail_block`, its inverse norm, `screen_operator`,
`multiplier_crossover`, the `M2_CANDIDATES` rows, `m2_rank_table`, `m2_gate_verdict`.

**Stage M's `TARGET_LEDGER` was not edited.** It is the record of an answered gate; M2 adds a
parallel layer and a test (`test_stage_M_record_is_untouched_by_M2`) fails if a later pass
writes the new column back into it.

## The engineering detour, recorded because it cost real time

A dense `np.linalg.inv` at `n = 768` costs ~10 s on this machine (no scipy in the venv,
unoptimized BLAS), which priced the crossover bisection out of existence — the first full test
run took over ten minutes. The tail block is **tridiagonal**, so an O(n²) Thomas elimination
replaces it. It is unpivoted and therefore not unconditionally safe, so it returns `None` on a
zero pivot and every caller falls back to the dense path, and
`test_the_fast_tridiagonal_path_agrees_with_the_dense_one` gates fast against dense across the
whole dial. **A fast number that disagrees with the slow one is not an optimization, it is a
second operator** — which is exactly how leg 53 lost a claim.

## Numbers

Every number quoted in the writeups is in `writeup/data/p2_route_m2_v1_targets.json`. The
headline set is in `TECHNICAL_P2_ROUTEM2_V1.md` §2–§5.

## What this leg does NOT establish

* Not that a certificate closes on the top candidate. That needs `Y_0` under budget on a
  profile whose constants this leg deliberately did not transcribe.
* Not a claim about `HL_S2_nonsymmetric`, whose row is unchanged and still shift-shaped.
* Not a full-text reading of arXiv:1908.09385. The `a`-neighbourhood is unquantified and the
  `nu`-dependence unstated in what was read. A promotion leg must discharge that first.
* Not movement on the L1→L4 chain, and not movement on Clay. The odds stay ~0.05%.
