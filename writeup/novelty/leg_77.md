# Leg 77 — Route-EXT2: novelty / literature pass on the rank-2 target object

**Leg 77, Route-EXT2 v1. Date of pass: 2026-08-06.** Pure literature leg — no computation, no
gCLM measurement, no solver touched. The standing ban ("another gCLM measurement leg", lifted
by never) is respected in full: nothing here evaluates a gCLM quantity. `capabilities.py` was
grepped before anything was written (row `solver/target_selection.py`, line 340) and **not**
edited; `solver/target_selection.py` itself is leg 63's exclusive territory and was read only.

**The gate, verbatim:**

> Has a certificate (computer-assisted or analytic) for arXiv:2603.25104's
> `gCLM_degenerate_one_scale` branch been published since March 2026?

**Answer: NO.** As of the search date **2026-08-06**, **133 days** after the object was first
posted (v1, 2026-03-26), no certificate — computer-assisted or analytic — has appeared for the
`a > 0` one-scale regular self-similar profiles from derivative-degenerate data (vanishing
order `k = 3`). The strongest single piece of evidence is not an absence: it is that the
**authors themselves revised the paper on 2026-06-16 (v2, 82 days after v1, 51 days before
this pass) and the `a > 0` case is still stated as observation.** The `target_selection.py`
ledger's `"certified": "NO"` entry for `gCLM_degenerate_one_scale` is therefore **not stale**;
it is current as of this date, and this leg banks the dated watch entry.

---

## 1. The query log — links, not counts

Issued verbatim on **2026-08-06**. Listed links are the items actually opened or judged
relevant; off-topic returns (degenerate parabolic / porous-medium / semilinear-heat blowup,
which the word "degenerate" reliably drags in) are not listed.

**Q1** `arXiv 2603.25104 Huang Tong Wang generalized Constantin-Lax-Majda degenerate self-similar`
- https://arxiv.org/html/2603.25104 — the object itself
- https://sites.google.com/view/de-huang/research — first author's page (stale for 2026 AP work; lists only a Bernoulli probability paper for 2026, so it is not usable as a negative)
- https://arxiv.org/pdf/2401.14615 — Huang–Qin–Wang, multi-scale CLM (the *non*-degenerate two-scale object; different setting)
- https://arxiv.org/pdf/2305.05895 — Huang–Qin–Wang–Wei, smooth *non-degenerate* profiles (the branch the ledger already excludes)

**Q2** `gCLM self-similar profiles degenerate data computer-assisted proof 2026`
- https://arxiv.org/pdf/2604.01868 — Hou-Luo / 2D Boussinesq singular profiles, numerical, Apr 2026 (adjacent object, **not** this one; and it is itself numerical)
- https://arxiv.org/pdf/2605.15149 , https://arxiv.org/pdf/2605.15130 — Chen–Hou C^{1,1/3-} Euler I/II (different model)
- https://arxiv.org/html/2308.01528 — Hou-Luo exact self-similar, smooth profiles

**Q3** `"Constantin-Lax-Majda" degenerate blowup rigorous proof interval arithmetic 2026 arXiv new`
- no new object; returns the pre-2026 gCLM corpus (2010.01201, 1908.09385, 2207.07548, 2411.01891, 2306.04146, 2506.02800)

**Q4** `computer-assisted proof self-similar blowup 2026 arXiv "degenerate" profile Hou Chen Cadiot Lessard fluid model`
- https://arxiv.org/pdf/2310.19781 , https://doi.org/10.1137/23M1607507 — the CAP machinery papers (Cadiot–Lessard-lineage), none applied to gCLM degenerate profiles

**Q5** `"2603.25104" cited OR references gCLM degenerate blowup`
- returns the paper itself and unrelated degenerate-parabolic blowup work; **no citing fluid paper surfaced**

**Corpus enumerations (API, not keyword luck):**
- http://export.arxiv.org/api/query?search_query=all:%22Constantin-Lax-Majda%22 (60-result cap, submittedDate descending)
- http://export.arxiv.org/api/query?search_query=abs:%22Constantin-Lax-Majda%22+AND+abs:%22self-similar%22 (60-result cap) — returns **10** entries total, of which **3** are 2026: 2607.19762 (Xu), 2603.25104v2 (the object), 2603.26715v5 (Shi, Boussinesq/Euler (1+1)D reductions, unrelated to degenerate gCLM profiles)
- http://export.arxiv.org/api/query?search_query=au:%22Jiajun_Tong%22+OR+au:%22De_Huang%22+OR+au:%22Xiuyuan_Wang%22 — the only 2026 AP entry among the three authors is 2603.25104v2 itself; **no follow-up preprint by the discoverers**
- https://api.semanticscholar.org/graph/v1/paper/arXiv:2603.25104/citations — **empty `data` array: zero indexed citations**

**Primary-source reads (v2 full text, not abstract):**
- https://arxiv.org/abs/2603.25104 — version history
- https://arxiv.org/html/2603.25104v2 — theorem inventory and §4
- https://arxiv.org/abs/2607.19762v1 — full abstract, and a keyword check for `degenerate` / `degeneracy` / `vanishing order` / `Huang-Tong-Wang`

---

## 2. What the object's own v2 actually proves — the decisive read

arXiv:2603.25104v2 (De Huang, Jiajun Tong, Xiuyuan Wang), *Self-similar finite-time blowups
with singular profiles of the generalized Constantin–Lax–Majda model: theoretical and
numerical investigations*. **v1 2026-03-26, v2 2026-06-16.**

Theorem inventory of v2, and which side of the `a` axis each lives on:

| statement | case | status |
|---|---|---|
| Proposition 2.1 | all `a` | asymptotic self-similarity **conditional** on profile convergence to a steady state — a conditional implication, not an existence certificate |
| Theorem 2.4 | `a = 0` | convergence of the **outer** profile to an explicit **singular** function |
| Corollary 2.5 | `a = 0` | same, half-line degenerate variant |
| Theorem 2.6 | `a < 0` | exact **singular** self-similar solutions, explicit family |
| Theorem 2.7 | `a < 1` | existence of the inner **traveling wave**, by a fixed-point method |
| — | **`a > 0` regular one-scale profile** | **no theorem** |

The `a > 0` degenerate branch — the ledger's `gCLM_degenerate_one_scale`, the object of this
gate — is carried entirely by **§4, titled "Numerical results with degenerate initial data for
`a > 0`"**, and by the abstract sentence, verbatim from v2:

> "For $a>0$, we observe one-scale self-similar blowups with regular profiles that have not
> been found in previous studies."

and in the body, verbatim:

> "In the case $a>0$, our numerical simulation indicates that odd-symmetric degenerate initial
> data ... can lead to ordinary self-similar finite-time blowups but with new regular
> profiles."

`observe` / `our numerical simulation indicates`, in a v2 that *did* upgrade other parts to
theorems. The paper mentions "computer-assisted proof" only in its **related-work** discussion
of the De Gregorio model and axisymmetric Euler — never applied to its own `a > 0` case. So
the negative is not merely "nobody else has certified it": **the discoverers had 82 days and a
revision cycle, proved the `a ≤ 0` side in that window, and left the `a > 0` side numerical.**

---

## 3. The one near-miss, and why it is not the certificate (a false friend)

**Xu, arXiv:2607.19762v1, 2026-07-22**, *The spectral picture of self-similar collapse in the
Constantin-Lax-Majda equation* — the newest gCLM paper in the corpus, posted **118 days after**
the object, and it contains the phrase "For $a>0$ we prove". It is **not** a certificate for
this branch, on three independent counts:

1. **Different profile family.** Xu's `a > 0` sentence reads, verbatim: *"For $a>0$ we prove a
   conditional two-line inclusion for each admissible smooth focusing profile, recompute the
   branch $c_l(a)$ of Lushnikov, Silantyev, and Siegel as a cross-check..."* — the **smooth
   focusing / LSS** branch, i.e. exactly the *non*-degenerate family that `target_selection.py`
   already excludes in its `q1` note. Huang-Tong-Wang's object is the `k = 3` derivative-
   degenerate branch, a different set of profiles at the same `a`.
2. **Conditional, and about the linearization, not existence.** A "conditional two-line
   *inclusion*" is a spectral-localization statement *for a profile assumed to exist*. Even on
   its own family it certifies no profile.
3. **The words are absent.** A keyword check of the Xu page for `degenerate`, `degeneracy`,
   `vanishing order`, and `Huang-Tong-Wang` returns **0 hits on all four**. Xu does not cite
   or address the object.

This is the trap that would have produced a wrong `yes` from an abstract-only pass: the newest
paper in the corpus, the right model, the right sign of `a`, the word "prove", and the wrong
branch. Recorded so the next watch does not re-trip it.

---

## 4. Independence from leg 74 (EXT)

Different object (`gCLM_degenerate_one_scale`, rank 2, 1D scalar + one Hilbert transform),
different paper (arXiv:2603.25104), different authors, different search corpus (the
Constantin-Lax-Majda enumeration, not the Hou-Luo one). No query above targets
`HL_S2_nonsymmetric` and no source located here is a Hou-Luo source except as a listed
off-target return. The two legs' findings stand or fall separately.

---

## 5. What is reported, and to whom

**No self-edit anywhere outside this leg's four files.** For leg 63 (M2) or a future ledger
leg, the reportable facts are:

- `solver/target_selection.py`'s `gCLM_degenerate_one_scale` entry, field `"certified": "NO"` —
  **still correct**, re-confirmed 2026-08-06. No stale-entry correction is owed.
- The entry's `"source"` field reads `arXiv:2603.25104 section 4, Table 4.1`. The paper is now
  at **v2 (2026-06-16)**; the ledger does not record a version. A future ledger leg may wish to
  pin the version, since the `a ≤ 0` theorem content grew between v1 and v2 while §4 did not.
  This is a **precision suggestion, not a correctness defect**, and is not applied here.
- The `q1` note's claim that "Huang-Qin-Wang-Wei's analytic gCLM branch is the NON-degenerate
  one and does not cover these" survives contact with the newest source: **Xu 2607.19762
  likewise works the non-degenerate LSS branch**, so the same exclusion now covers two papers,
  not one.

---

## 6. Watch metadata (for the next re-ask)

- object first posted **2026-03-26**; last revised **2026-06-16**; searched **2026-08-06**
- elapsed at this pass: **133 days** since v1, **51 days** since v2
- indexed citations at pass time: **0**
- 2026 entries in the `Constantin-Lax-Majda` ∩ `self-similar` arXiv enumeration: **3**, of
  which **0** address the degenerate `a > 0` branch
- cheapest re-ask for a future leg: re-run the Semantic Scholar citations endpoint and the
  two arXiv API enumerations above; a non-empty citation list or a 4th 2026 entry is the only
  trigger worth a full pass.
