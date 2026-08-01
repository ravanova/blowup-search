# Route-D v15 — the literature check, and what it does to the lane

*Phase-2 P2, Route-D leg 15. Data: `writeup/data/p2_literature_scope.json`.
**No figure, because there is no measurement** — this leg produced no numbers of its own,
and manufacturing a plot out of a reading list would misrepresent what it is.*

**Rigor level: 0 — this is scoping, not mathematics.** And it carries a limitation severe
enough to belong in the first paragraph rather than a footnote.

---

## 0. The limitation, stated first

**Not one of the papers below was read.** This container's network policy blocks `arxiv.org`
and every publisher domain reached — `WebFetch` and `curl` both return 403 at the proxy's
CONNECT step — so the only instrument available was web *search*, i.e. titles, abstracts and
result-summary paraphrase.

That makes everything here a **lead**, not a fact. Identifiers (titles, authors, arXiv
numbers, DOIs) are reliable; technical statements are paraphrases and need verifying by
someone who can open a PDF. The whole point of doing this leg anyway is that a labelled
unverified lead is useful and an unlabelled one is a liability — so every entry in the data
file carries an explicit `confidence` and a `must_verify` list.

Read the rest with that in front of you.

---

## 1. Why this leg happened now

The standing "what would actually be worthwhile" list has carried the literature search as
item (5) for three legs with the same note attached: *it currently BLOCKS every novelty claim
the project might make*. The previous leg (v14) added a new one to that pile — an exact first
integral of the profile equation — and flagged its own novelty as unchecked. Doing the check
before building anything else on it is the cheap, obvious move, and the continuation prompt
had just promoted it to run in parallel with the next brick.

It came back with more than expected, and the useful part is not about v14.

---

## 2. What the search found

**(a) The object this project has been building a certificate for appears to have a rigorous
existence proof already.**
`arXiv:2603.25104` — Huang, Tong, Wang, March 2026, *Self-similar finite-time blowups with
singular profiles of the generalized Constantin–Lax–Majda model*. Search-level summary: the
two-scale blowup's **inner profile is governed by a traveling wave on the smaller scale, and
the existence of those traveling wave solutions is established rigorously via a fixed-point
method.** 55 pages, 19 figures.

That is this project's object. Route-D's entire premise has been that certifying the
two-scale traveling wave would be a Level-2 result. If the reading is right, existence is
already a theorem — and by an analytic fixed-point argument, not a computer-assisted one.

The same abstract carries a second item that may matter more: the two-scale scenario is
described as the **`a ≤ 0`** case, with `a > 0` giving *one-scale* self-similar blowups with
regular profiles. This project has been working the two-scale object at `a > 0` throughout.
**That single sign is the highest-value thing on the verification list**, because it bears on
whether the object is the right one at all, and it is also the *least* well established of
anything here — it comes from one sentence of a search summary.

**(b) Compactly supported profiles in this family are known, and so is reducing the profile
equation to a scalar fixed point.**
`arXiv:2305.05895` — same group, 2023. gCLM admits exact self-similar blowups with interiorly
smooth profiles for all `a ≤ 1`, **either smooth on the whole line or compactly supported and
smooth in the interior of their closed supports**; existence via the fixed point of an
`a`-dependent nonlinear map `R_a`, where a fixed point `f` gives `Ω(x) = −x f(x)` and the
scaling constants are explicit integrals of `f`. The `a = 0` and `a = 1/2` profiles are
strictly negative on `(0,∞)`; **the `a = 1` profile is compactly supported.**

So: v12's "the profile ends" is inside known territory as a phenomenon, and v14's reduction is
inside known territory as a technique. (Note the pattern differs — theirs is compactly
supported at `a = 1` in the *self-similar* problem; ours is compactly supported at every
`a > 0` in the *two-scale traveling wave* problem. Different objects, and the difference is
itself worth verifying rather than explaining away.)

**(c) gCLM traveling waves have been computed since 2014.**
Okamoto, Sakajo, Wunsch, *Steady-states and traveling-wave solutions of the generalized
Constantin–Lax–Majda equation*, DCDS 34 (2014) 3155–3170 — steady states and traveling waves
computed, asymptotic behaviour described, existence for every `a > 0` argued numerically.

**(d) Compactly supported self-similar De Gregorio solutions on the line.**
`arXiv:2209.08232` — infinitely many, mutually distinct under rescaling, `ω ∈ H¹` odd and
supported on `[−1,1]`.

**(e) The single most decision-relevant item: computer-assisted proofs in this exact family
are routine.**
Interval arithmetic (INTLAB) plus Newton–Kantorovich is established practice here — the
Chen–Hou 2D Boussinesq / 3D Euler rigorous-numerics papers, and, per search summary,
computer-assisted proofs of asymptotically self-similar one-scale blowups for the CLM model
itself.

**(f) One extraordinary claim, recorded so a later session does not rediscover it and get
excited.** `arXiv:2604.09949`, April 2026, single author, claims stable finite-time
singularity formation for 3D Navier–Stokes via a computer-assisted Newton–Kantorovich
validation of a "5D-lifted" profile. **Do not use, do not repeat as a result, do not re-plan
around it.** A solo preprint claiming a Clay Millennium Problem is overwhelmingly likely to
contain an error, and nothing here is in a position to check it.

---

## 3. What this does to L1, said plainly

L1 in the standing chain is: *a certified (Level-2, computer-assisted) self-similar blow-up
profile for the 1D gCLM/HL toy model at some `a > 0`.* Fifteen legs of Route-D have been
aimed at it.

**On the evidence above, L1 is occupied territory.** The technique is routine for the groups
working in this area, and the specific object has (apparently) had its existence proved by
other means five months ago. Finishing the certificate would therefore be:

- a **capability demonstration** — real value, and exactly what standing brick (4) always said
  it was ("worth doing for the capability, not the result"); and
- a **reproduction**, not a novel contribution.

That is not a reason to be gloomy and it is not a reason to stop; it is a reason to stop
calling it the lottery ticket. The honest version: the marginal value of the next Route-D leg
just dropped, and it dropped for a reason external to the work rather than because the work
went badly. v14's kill switch passing was real. It was also, plausibly, a rediscovery.

**What this does NOT do:** it does not touch the two structural walls (a search programme can
only argue *for* blow-up; interval numerics only reaches toy models), it does not change the
~0.05% Clay odds, and it does not invalidate a single measurement in v3–v14. Being second is
not being wrong.

---

## 4. v14's novelty claim, retracted to the right level

v14's writeups said the first integral's novelty was unchecked and that it was "exactly the
sort of thing that is folklore to people who work on gCLM/De Gregorio". That hedge was
correct and is now stronger than a hedge:

> **Presume the first integral is known.** A group has published a fixed-point existence proof
> for this exact traveling wave, and the natural way to build such a fixed point for
> `Ω H(Ω) = E Ω_X` is precisely this reduction. Until `arXiv:2603.25104` and `arXiv:2305.05895`
> are read, the correct posture is that v14 rederived a known structure.

The mathematics of v14 is unaffected — the identity is verified three ways, the kill switch
result stands, the reduced solver works. What changes is the framing, and it has been
corrected in place in both v14 writeups with the change marked rather than silently edited
(banked lesson 35).

---

## 5. Gate-check against the Clay chain

**(a) Which link does this move?** None — it *re-prices* L1, which is arguably more valuable
than moving it. This is the first leg in fifteen to change the estimate of what finishing L1
would be worth, using information from outside the project.

**(b) Is another L1 leg the best use of the next chunk?** **No, not as a novelty play.** The
recommendation changes:
  1. **Verify the two things that are load-bearing** — the `a`-sign question in
     `arXiv:2603.25104`, and whether its fixed point is this first integral. Both need a PDF,
     i.e. a session with network access to arXiv, or a human. Until then, treat the two-scale
     `a > 0` object as *possibly the wrong object*.
  2. **The DSS lane (standing item (1)) is now clearly the best swing.** It was already ranked
     first for a theoretical reason — Nečas–Růžička–Šverák/Tsai rule out exactly self-similar
     NS blowup, so a Clay-relevant candidate must be discretely self-similar or otherwise
     non-generic — and the search did not turn up anyone doing a global *profile search* for
     one. **That last inference is the weakest thing in this document**: absence of search
     hits is not absence of literature, and it must not harden into "nobody has done it".
  3. **Finish the certificate anyway, but as a capability**, cheaply, and stop calling it the
     result. It is still the pipeline every other lane needs.

**(c) Is there a cheaper experiment that kills the whole route?** Reading one paper. That is
now the cheapest decisive act available to this project, and it is blocked by a network
policy rather than by difficulty — which is worth saying out loud, because it means the
binding constraint on the next decision is *access*, not compute and not cleverness.

---

## 6. What is NOT claimed

- **No paper here was read.** Every technical statement is a search-summary paraphrase.
- **"L1 is occupied" is an inference from (e) plus (a)**, both at medium confidence. It should
  change what the project *prioritises*; it should not be written into a public claim.
- **The DSS lane being uncrowded is the weakest inference in this document** and is recorded
  as "not contradicted", never as established.
- **Nothing here is mathematics.** No new object, no new estimate, no new gate. The project's
  rigor ladder is exactly where v14 left it: Level-1 tooling plus one exact identity, no
  certificate, nothing interval-enclosed.
