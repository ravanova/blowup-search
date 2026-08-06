# Leg 88 novelty pass — Route-GCA: adversarial audit of `solver/gclm_family.py`

Run BEFORE construction, per the leg contract.

## Question being claimed

Under an adversarial battery (NaN/Inf-poisoned `c_l`/`c_omega`, `a` far outside `[0,1]`), does
`solver/gclm_family.py`'s residual computation ever silently return a finite, plausible-looking
value instead of propagating the invalid input or flagging it?

## In-repo prior art

| source | what it covers | overlap with leg 88 |
|---|---|---|
| `test_gclm_family.py` (12 tests) | a=0 one-scale known-answer gate (RMS 2.2e-7), velocity operator, parity, GA recovery, two-scale gate, relnorm scale-invariance, mixed genome, sq-Lorentzian basis | none — every test uses well-formed finite profiles and finite in-range coefficients. Grep for `nan`/`inf`/`adversarial` over the file: zero hits. |
| `test_nk_fourier.py` | imports `gclm_family` for a Newton-Kantorovich cross-check | correctness on well-behaved data; no malformed input |
| leg 66 (`writeup/novelty/leg_66.md`) | test-coverage census; lists `gclm_family` only as a *consumer* test of `solver/gclm.py` | census, not an audit |
| leg 69 | adversarial audit of `solver/interval.py` | same *pattern*, different module. Found a real gap (repaired later, closed by leg 87) |
| leg 79, leg 80 | adversarial audits of other modules | same pattern, different modules |
| leg 83, leg 85 | adversarial audits; both cleared the leg-42 gCLM-measurement ban on the same robustness-vs-measurement distinction | precedent for the ban ruling below; neither touched `gclm_family.py` |
| `test_bordered_hl_adversarial.py`, `experiments/p2_route_bhn_v1_adversarial.py` | the only adversarial battery files currently on main | bordered HL object, not the gCLM a-family residual |

No file in the repository passes a non-finite coefficient or an out-of-range `a` into
`GCLMResidual`. The question is unasked here.

## Ban check (plan_of_record.py)

The live ban reads "another gCLM measurement leg (lifted by: never -- the model is exhausted
(Stage 3.5, leg 42))". This leg measures **the residual code's response to malformed input**, not
the gCLM model's physics: it produces no new profile, no new `a`-sweep, no new self-similar
exponent, and no claim about blow-up in the a-family. It reads `solver/gclm_family.py` and edits
it under no outcome. That is the same robustness-vs-measurement distinction that cleared legs 83
and 85, and I confirm it independently here rather than inheriting it. Verified directly against
the printed ban list: none of the other nine live bans (Route-D sharpening, DSS, 2D beta, scaling
gauge, GA-on-unvalidated-fitness, the four leg-51/53 reading bans, Chen-Hou-as-target) touches an
input-validation audit.

The tenth ban — "building a solver without grepping `capabilities.py` for the object first" — is
discharged: `capabilities.py:64-68` registers `solver/gclm_family.py` as "gCLM a-family, rescaled
steady residual" with `test: test_gclm_family.py`. No adversarial/validation capability is
registered for it, and no other module offers one to reuse.

## External literature

Input-validation robustness of a research residual evaluator is an engineering property of this
specific file. There is no external claim to resolve: the finding is about this repository's code,
not about the gCLM equation, so no arXiv precedence question arises. (Contrast leg 57/VER-D, where
the claim was mathematical and Cadiot arXiv:2505.03091 had to be resolved.)

## Verdict

Novel within the repository. Proceed to construction.
