# Leg 79 — Route-PC v1: adversarial fabrication-rejection audit of the L1→L2 port

**Branch** `leg/pc-v1`. **Exploration leg (light), CLAIM-BEARING** (soundness of shared
certificate-adjacent infrastructure).
**Gate: NO — stop-the-line.** Branch pushed; **not merged to `main`**, per the gate's `no`
branch. Escalated to the orchestrator as a priority finding.

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `NG` is NEXT. Every live ban noted; **none binds this leg** — it
   builds no gCLM measurement, no Route-D bound sharpening, no DSS re-ask, no GA compute, no
   ℓ¹-Fourier machinery. It adds no mathematics at all. The ban that *did* apply is *"build
   nothing without grepping `capabilities.py` first"* — done, entry at line 99, and the claim
   under audit is its `validated` line 103–105.
2. `DIRECTION.md` — **has a leg 79 entry** (line 898), read in full; thesis, gate and territory
   match the dispatch prompt verbatim. (Noted because legs 57 and 69 both had to flag the entry
   as missing; this one was present.)
3. **Novelty pass FIRST**, committed before any construction (commit `5020fc8`,
   `writeup/novelty/leg_79.md`), four queries, **links not counts**.
4. Then: battery runner, curated data, permanent regression test, findings.

## What the novelty pass changed about the leg

It supplied the **standard**, and without it this leg would have had none. The obvious naive
framing — "is a negative `Y_0` bad?" — is a matter of taste until Q1/Q2 establish that `Y_0`,
`Z_1`, `Z_2` are *upper bounds on norms in the theorem the function implements*
(van den Berg–Lessard, AMS Notices 62(9):1057, 2015; Hungria–Lessard–Mireles James, Math.
Comp.). That converts "bad input" into **"outside the hypotheses of the imported result"**, which
is a decidable predicate — and it is exactly the predicate `violates_hypotheses()` in the runner
implements. Every case in the battery is judged against a published hypothesis, not against my
opinion.

It also pre-emptively removed two novelty claims. The NaN-bypasses-a-comparison-guard hazard is
documented verbatim in *Verifying Floating-Point Programs in Stainless* (arXiv:2601.14059), and
the method — adversarial batteries against trusted-base components — is routine (QED at Large,
arXiv:2003.06458). This leg claims neither as a discovery.

## What was actually measured

**39 calls to `radii_polynomial_status`, in four families** (honest control / sign violation /
non-finite / type confusion). Pure logic, no solver state, sub-second, fully deterministic.
**25 of the 39 are outside the theorem's hypotheses** by the decidable predicate above.

| magnitude | value |
|---|---|
| cases | 39 |
| outside the theorem's hypotheses | 25 |
| **accepted as `closes=True` anyway** | **11 (44.0% of the 25)** |
| raised loudly (`TypeError`/`ValueError`) | 5 |
| `BLOCKED_AT_STEP_ONE` calls | 3 |
| …of those, carrying a fabricated `Y_0` or `Z_1` | **0** |
| honest-path branches still classifying correctly | 7/7 |

## The finding, in one sentence

`capabilities.py`'s validated line is **half right**: `radii_polynomial_status` genuinely
*refuses to invent* numbers it does not have — 0 of 3 blocked calls carry a bound, and a poisoned
`Z_2` does not unblock it — but it performs **no domain validation on numbers a caller does
supply**, so 11 fabricated inputs (negative `Y_0`, negative `Z_1`, negative `Z_2`, `−inf` in any
slot, a negative numpy scalar) are converted into an asserted contraction.

The sharpest single witness: `radii_polynomial_status(-1.0, 0.9, 1e4)` returns `closes=True`,
while the identical call with the sign of `Y_0` corrected — `(+1.0, 0.9, 1e4)` — correctly
returns `closes=False`. **A single sign flip upstream turns a correctly-reported non-closure into
a certificate closure, silently.**

## Severity, stated as a magnitude and not as alarm

**Latent, not active. No stored result is affected.** Both call sites in the repository —
`experiments/p2_route_k_v1_port.py:203` and `experiments/p2_route_l_v1_precond.py:289` — pass
`(None, None)` and land on the blocked branch, which is the half that holds. **Nothing has ever
been evaluated through the unvalidated path.**

The exposure is prospective and it is getting nearer, which is why this is worth stopping for:
Route-L's `line_sweep_solve` made `A` constructible and unblocked step (iii), so the day real
`Y_0`/`Z_1` numbers start flowing into this function is no longer hypothetical. It is the last
gate before a `closes=True` in the certificate chain and it currently trusts its caller
completely.

## What I did NOT do

**I did not patch `solver/port_certification.py`** — forbidden by both the gate's `no` branch and
the territory. The repair is small and obvious (reject non-finite and negative constants with
their own status, ahead of the discriminant) but it redefines what `EVALUATED` means and must be
made by the module's owner together with an update to `capabilities.py`'s validated line. Handing
the orchestrator a patched module *and* a claim that the module was broken would have destroyed
the evidence for the claim.

## The regression test is a CHARACTERISATION, and that is deliberate

`test_port_certification_regression.py` passes today by asserting the behaviour **as measured on
2026-08-06**, including the 11 false closes by exact label. It is not a clean bill of health and
its docstring says so at the top. The moment someone adds the missing guard, `test_3` and
`test_4` **fail** — and that failure is the intended alarm: it forces the fix, this file, and
`capabilities.py`'s validated line to be reconciled in one commit rather than drifting apart.
Writing it as an aspirational (currently-failing) test instead would have meant pushing a red
merge gate, which the contract forbids.

## Artifacts

- `experiments/p2_route_pc_v1_regression.py` — the 39-case battery, PC1–PC5.
- `writeup/data/p2_route_pc_v1_regression.json` — every case with its inputs, its verdict, and
  which hypothesis it breaks.
- `test_port_certification_regression.py` — 5 permanent gates.
- `writeup/novelty/leg_79.md` — the pre-construction pass, plus the findings section.

No figure; none was required and none would carry information a table does not.

---

**STATUS UPDATE (2026-08-06, Leg 0 / ORCH, branch `bench/fix-port-certification-validation`).**
The gap above is CLOSED. `radii_polynomial_status` now rejects negative and non-finite
`Y_0`/`Z_1`/`Z_2` with status `INVALID_INPUT` ahead of the discriminant, so all **11 false
closes became REJECTED: 11/25 -> 0/25**, and the NaN bypass of the `Z1 >= 1.0` guard went with
them. The blocked branch is checked first and is byte-identical, so both call sites and both
stored artifacts are unaffected. `test_port_certification_regression.py` was flipped from
characterising the defect to gating its absence, keeping the 11 labels as the regression
target; `capabilities.py`'s validated line was corrected in the same commit. This leg's report
above is left exactly as written — it is the record of the pre-fix measurement.
