# Leg 65 — VER-H: independent post-landing review of the Route-L1G literature verdict

**Role.** VER-H, trigger (b) (post-landing review of a claim-bearing leg). Leg 65 landed on
`main` as `de533d9`, `cda8edc`, `09728ec`. **I report gaps; I do not repair.** I have edited
none of leg 65's files, none of `solver/`, and none of the integration-owned ledgers.

**Independence of this pass.** I did not read leg 65's extracted texts. I re-fetched all four
PDFs from arXiv myself (`bash Papers/fetch.sh 2312.01702 1908.09385 2607.15256 2005.14027`,
egress HTTP 200, 4 fetched / 0 failed), re-extracted them with `pdftotext -layout`, and
recomputed every count and re-read every quoted passage from my own copies. The forward-citation
sweep was re-queried live against the Semantic Scholar API.

---

## Verdict

**THE FINDING STANDS.** The gate answer `NO` — neither the weighted-`ℓ¹` no-go (C1) nor the
discrete-ball trap (C2) is published in the two remaining Tier-2 papers or anything they cite
forward — is **confirmed on all four key claims**, at the precision leg 65 stated them. Three
precision nits and one additive observation are recorded below; **none of them touches the gate
answer, and none warrants a rework leg.**

---

## 1. Do the term counts hold, and does 2005.14027 run opposite to a no-go?

**Term counts: confirmed exactly, all four papers, on my own freshly-fetched extractions.**

| paper | weight | computer-assist | duality | leg 65 said | verdict |
|---|---|---|---|---|---|
| 2312.01702 | 0 | 0 | 0 | 0 / 0 / 0 | **exact** |
| 1908.09385 | 14 | 0 | 0 | 14 / 0 / 0 | **exact** |
| 2607.15256 | 108 | 12 | 0 | 108 / 12 / 0 | **exact** |
| 2005.14027 | 1 | 0 | 0 | 1 / 0 / 0 | **exact** |

Also confirmed on my copies: `Banach` 0 and `validated` 0 in 2312.01702; `Fourier` exactly 3 in
1908.09385; `Wiener` and `Besov` 0 in all four. The **character counts** in the committed JSON
(102610 / 66790 / 105271 / 108587) reproduce **byte-identically** against my independent fetch —
i.e. leg 65 and I extracted the same documents, and the counts are not transcription.

**2005.14027 works in a Hilbert grading and proves the bilinear term BOUNDED: confirmed
verbatim.** Line 686 of my extraction, exactly as quoted:

> "Operator B is a bounded bilinear operator in hm – see the proof in Appendix B."

restated as Lemma 16 (line 1312–1316): "`B : hm × hm → hm` is a bounded bilinear …". The space
is confirmed Hilbert, not `ℓ¹`: "Clearly, the space `hm` is a Hilbert space endowed with the
inner product `(u,v)_{hm} = (D^m u, D^m v)`", with `V^m = {u ∈ h^m | ∇·u = 0}` (38) "endowed
with the `hm` norm". The proof's stated mechanism — "exploits the locality of the nonlinear
interactions on the logarithmic lattice, which turns the convective term into the action of a
**bounded** operator" — is indeed the structural **opposite** of a no-go. Leg 65's
characterisation is accurate, and its `§M-4`-style reasoning (Hilbert grading, so it narrows
rather than closes C1) transfers correctly.

## 2. Does 1908.09385 really make no statement about admissible weight classes?

**Confirmed.** Eq. (2.12) reproduces verbatim on my copy (line 320–329):

> "We choose the following weights … `ϕ = (x²+b²)³/(2bx⁴) = −(1/ω̄)(x²+b²)/x³`,
> `ψ = (x²+b²)³/(2b) = −x(x²+b²)/ω̄`, and will perform weighted `L²` and weighted `H⁴` estimates
> to establish the nonlinear stability. … In the following discussion, we assume
> `ω ∈ L²(ϕ) ∩ H⁴(ψ)`."

so `ϕ = ψ/x⁴` **exactly** (denominators `2bx⁴` vs `2b`) — leg 65's "differ by exactly `x⁻⁴`" is
right to the letter. I read **all 14** occurrences of "weight" in the paper. Every one is a
working usage — *"We choose the following weights"*, *"the singular weight ϕ"*, *"we separate the
singular and less singular part of the weight ϕ"*, *"the weight ψ is not singular"*. **There is
no theorem, remark, or sentence anywhere in the paper about which weights are admissible**, and
none asserting that any weight pair is impossible. Leg 65's claim holds.

**Corroborating detail leg 65 did not use, which strengthens its reading:** in §2.6 (line 686)
Chen picks a *different* weight for the `H³` estimate (`ρ,−x/ω̄ = (x²+b²)²/(2b)`) than the `ψ`
used for `H⁴`. Weights are re-chosen per estimate as convenience demands — which is exactly the
opposite of a classified admissible set. Confirmed also: `computer-assist` 0 and `validated` 0,
re-confirming leg 45's finding from the same text, and C2 is structurally absent (the paper never
discretizes).

## 3. Is 2607.15256 §1.2 the genre-cousin leg 65 says it is?

**Confirmed, verbatim and in every classificatory detail.** The passage at (1.17)–(1.18) on my
copy (lines 190–211) matches leg 65's quotation word for word, including
`‖u_x ϕ^{1/2}‖_{L²} ≤ C(1−β)^{−1/2}‖ω ϕ^{1/2}‖_{L²}` as (1.18). Checking each of leg 65's four
sub-claims:

- **Same genre — one exponent squeezed from both sides: YES.** Finite energy forbids `β ≥ 1`
  from above ("Since the energy must be finite and `η(x,0) ≠ 0`, one cannot choose `β ≥ 1`");
  and as `(1−β) → 0` the nonlocal term's constant `(1−β)^{−1/2}` diverges from below.
- **Weighted `L²`, not weighted `ℓ¹`: YES.** The weight is `ϕ = x^{−α}y^{−β}`, `0 < β < 1`, in a
  "weighted `L²(ϕ)` estimate on the `η` equation". No sequence space anywhere; `Fourier` occurs
  **0** times in the entire paper.
- **Damping vs. finite energy, not smoothness vs. far-field decay: YES.** The two competitors are
  literally the `a₂(1−β)/2` growth term from `y`-advection (i.e. failure to extract damping) and
  the finiteness of the energy. Nothing in the passage concerns far-field decay or smoothness.
- **Resolved by a choice, not stated as a no-go: YES, and explicitly.** The passage's own
  conclusion sentence: *"As a result, one needs to take a very singular weight `x^{−α}y^{−β}` or
  `|(x,y)|^{−α}y^{−β}` with large `α` to extract the desired damping effect."* That is a
  prescription, not an impossibility statement. No sentence in the paper asserts that no
  admissible weight exists.

The abstract, title, authors (Jiajie Chen, Thomas Y. Hou) and date (`arXiv:2607.15256v1
[math.AP] 16 Jul 2026`) all confirm as quoted, including the abstract sentence leg 65 reproduces
("the weighted norms require exact local vanishing conditions that are not automatically
preserved by the equations nor the numerical construction"). §1.4's quotes ("effectively of order
`|x|^{−3}`", "must vanish cubically", "preserves only quadratic vanishing order") and the
basis-vs-grid-values passage ("the numerical step only determines coefficients in explicit basis
representations … Hence the improved vanishing order is an exact analytic property of the
corrected function") all reproduce verbatim. Leg 65's judgement that this is the *moral* of C2
stated as practice, but **not** C2 — no induced norm computed by duality over a discretized ball,
no extremizer inflation factor, `duality` occurring **0** times — is confirmed.

## 4. The forward-citation sweep, re-queried live

Re-queried against Semantic Scholar during this pass:

- citing **2312.01702**: **8** — matches leg 65 exactly.
- citing **1908.09385**: **31** — matches leg 65 exactly, and **2607.15256 is genuinely in that
  list**, so the provenance of the one on-topic forward citation is real, not asserted.
- total **39**, as claimed.

**I checked the triage, not just the count.** Leg 65 listed 15 of the 31 by ID plus "Chen–Hou
Part II". I pulled titles for the **nine** arXiv-IDed papers it did not name (1910.00173,
2107.02920, 2204.01951, 2306.04146, 2311.11511, 2407.15812, 2408.04319, 2504.14346, 2606.20467)
and the un-IDed remainder. Every one is either a journal-version duplicate of a paper already in
the list (Chen–Hou Part II, the CLM multiscale paper, the `C^{1,α}` papers) or a blowup-corpus
analysis paper (Landau, compressible Euler, β-CCF, electron MHD, complex Ginzburg–Landau); the
single outlier, 2606.20467, is a machine-learning paper on symbolic PDE search. **None is in
weighted-`ℓ¹` sequence-space or discrete-ball-duality territory.** The only methodological
weighted-norm paper in the whole citing set is 2607.15256 — which leg 65 fetched and read.
**Leg 65's "1 on-topic of 39" triage is confirmed; no candidate was missed.**

---

## Precision nits (prose only — none changes the gate)

1. **`writeup/novelty/leg_65.md` overstates one sentence about 2312.01702.** It says the paper's
   "only uses of 'rigorous' are disclaimers that rigour is *absent*". Of the 3 occurrences, two
   are the disclaimers quoted; the third (my line 246) is positive — *"The finite-time
   singularity in the inviscid case was also rigorously established [22]."* It attributes rigour
   to a **cited** work, not to this paper, so the substantive point (2312.01702 proves nothing
   rigorous itself, and has 0 weight / 0 computer-assist / 0 duality) is untouched. Accurate
   wording would be "two of its three uses of 'rigorous' are disclaimers, the third credits a
   cited paper".
2. **`experiments/journal/leg_65.md` places the 2607.15256 tension one space too wide.** It says
   the tension is "in weighted `L²`/`L^∞` energy spaces". The (1.17)–(1.18) tension is
   **purely weighted `L²`**; the weighted `L^∞`/`C^{1/2}` estimates are the route Chen–Hou
   **adopt because of** that tension ("These considerations lead us to use singularly weighted
   `L∞` and weighted `C^{1/2}` estimates for stability"). `writeup/novelty/leg_65.md` states this
   correctly ("a published instance of the genre C1 belongs to, in weighted `L²`"); only the
   journal's one-line summary is loose.
3. **The "`DIRECTION.md` has no leg-65 entry" flag is stale, and is now false against `main`.**
   Both ledger files carry it. `DIRECTION.md` **does** have a leg-65 entry (line 390,
   `### 65 — ROUTE-L1G`), added by `2cb8e8f` at 23:38:25; leg 65's first commit is 23:40:00 —
   **95 seconds later**, so the leg branched before the DM's refresh landed and the flag was
   honest when written. **No divergence resulted:** I diffed the gate leg 65 executed against
   `DIRECTION.md`'s, and they are **identical word for word**, as is the four-file territory
   list. Bookkeeping artifact only.

## Additive observation (not a gap)

The germ of 2607.15256's obstruction is already in 1908.09385 itself, one line leg 65 did not
record: at my line 679, *"We remark that `E(0) < +∞` implies `ωx(0,0) = 0` due to the singular
weight `ϕ`."* That is finite-energy forcing a vanishing order — the same mechanism 2607.15256
makes its whole subject seven years later. It is a **consequence**, not an obstruction and not a
weight-class statement, so it does not move the gate; but a future write-up of C1 tracing the
cousin's lineage should cite Chen 2019 line 679 alongside Chen–Hou §1.2, not only the latter.

## Quartet check (DOCS)

Leg 65's leg-appropriate quartet is **complete on disk** — script + JSON + novelty log, no figure
required for a pure literature leg, per the established convention:

| piece | path | status |
|---|---|---|
| runner | `experiments/p2_route_l1g_v1_lit.py` | present, 456 lines, **runs clean** |
| data | `writeup/data/p2_route_l1g_v1_lit.json` | present, 346 lines, regenerates **byte-identical** (`git status` clean after re-run) |
| novelty log | `writeup/novelty/leg_65.md` | present, 334 lines |
| journal | `experiments/journal/leg_65.md` | present, 93 lines |
| figure | — | correctly absent (literature-only leg) |

**`writeup/novelty/leg_65.md` is links, not counts: confirmed.** All six query records (Q1–Q6)
carry verbatim query strings and the actual URLs returned; where a query returned nothing
on-topic it says so in words ("On-topic for C1: none.", "Nothing on-topic for C2.") rather than
reporting a bare number. No query record anywhere in the file reports a hit count in place of a
link.

**One quartet detail worth crediting:** the runner does not hardcode its term counts. It
recomputes them from `Papers/<id>.txt` when the gitignored PDFs are present and falls back to
recorded values with an honest `"recorded (Papers/ is gitignored; …)"` provenance label when they
are not. On my machine all four read `"recomputed"`, and the regenerated JSON matched the
committed one exactly.
