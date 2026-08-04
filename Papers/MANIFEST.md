# Papers manifest — what to fetch, in priority order, and what each one gates

**Why this file exists.** `Papers/` is gitignored (we do not commit third-party PDFs), so
a previous session's downloads are **destroyed every time the container is rebuilt** —
which is what happened here: Spike 1's notes cite "Source PDFs live in `Papers/`" and the
directory no longer exists. The manifest and `fetch.sh` are committed so the PDFs can be
re-pulled in one command instead of re-derived from memory. **If you download papers, do
not commit them; commit any change to this manifest instead.**

**STATUS 2026-08-04 (leg 45, Route-M): TIER 2 AND TIER 3 ARE NOW READ FOR WHAT THEY GATE.**
The target ledger they produced is `solver/target_selection.py` (`test_target_selection.py`
9/9), and `LITERATURE_CHECK.md`'s **seventh pass** is the summary. What changed:

* **2302.12877 (CLN)** — the completed unbounded-domain certificate. Their Kawahara `r₀` is
  now a gate on our own radii-polynomial algebra (reproduced exactly). **They work in
  Hilbert/Fourier `H^l`, not weighted `ℓ¹`**, so Route-D's weighted-`ℓ¹` no-go and
  discrete-ball trap are **narrowed, not closed** — still unsearched at primary source.
* **2604.01868 (CHL)** — carries the **top two uncertified targets**, and its §4 Scenario-2
  formulation is the three-constant bordered system the port is now aimed at.
* **2603.25104 (HTW26)** — the third: gCLM one-scale profiles from degenerate data, `a>0`,
  numerical only, with `c_l` changing sign at `a ≈ 0.2329`.
* **2308.01528 / 2305.05895 (HQWW)** — the **exclusion list grew**: the Hou–Luo odd
  non-degenerate profile is proved analytically as well as by CAP, and the **entire smooth
  gCLM branch for all `a ≤ 1`** is analytic. Certifying either contributes nothing.
* **1908.09385 (J. Chen)** — checked and it is **analytic**, no computer assistance. Not a
  CAP precedent; it is an exclusion.
* **2604.09949** — a 3D Navier–Stokes singularity claim. Audited; see LITERATURE_CHECK §7th
  pass. Recorded as `CLAIMED_UNUSABLE`, not as certified and not as open.

**STATUS 2026-08-04: EGRESS WORKS. ALL 14 FETCHED ON THE FIRST ATTEMPT. TIER 1 IS READ.**
See `LITERATURE_CHECK.md` **sixth pass** (the first primary-source pass) and Route-J v1
(`solver/literature_gates.py`, `test_literature_gates.py` 9/9, fig39). Verdict: seven
standing claims pre-empted, one partial, two still unsearched, one result inbound.

**READ:** 2207.07548 (full; §1, §5, §7.3, §8 closely), 2607.19762 (full; abstract, §2, §3,
§6, §7 closely), 2210.07191 (abstract, §1, the `c_l/c_omega` profile section),
2209.08232 (§1, §2 closely).
**FETCHED AND TEXT-EXTRACTED BUT NOT READ:** everything in Tier 2 and Tier 3. **Tier 2 is
the next literature spend and it is now cheap** — it gates the Route-D methodological
claims, the only ones with a real chance of being new.

**TWO CORRECTIONS TO THIS MANIFEST'S OWN PRIORITIES, from having read Tier 1:**
* **2207.07548 does NOT gate `s_c = α/2`.** Its §8 explicitly leaves the critical-σ
  question open. **2607.19762 §6.1 eq (6.3) is the pre-emption** — it was filed here as a
  spectral paper, and its §6 is the one that matters.
* **2207.07548 turned out to matter for something nobody asked it about:** §5.1 (Schochet,
  corrected) is the only primary source in this list on the **supercritical** balance,
  which no leg of this project had. Lesson (69).

Fetch everything: `bash Papers/fetch.sh` (needs the hosts below allowlisted).
Fetch one: `bash Papers/fetch.sh 2207.07548`

---

## Tier 1 — read these first; each one settles standing claims

| arXiv | what it is | what it gates |
|---|---|---|
| **2207.07548** | dissipative gCLM / relevance exponent | **THE most important one. Gates FOUR claims across THREE legs**: Route-F v1's `s_c = α/2` (§27), Route-H v1's `λ_μ = 2s − α₀` (§29), Route-I v1's growth-rate remeasurement (§30), and `α(1/2) = 3`. If this paper contains `s*(a) = 1/c_l(a)`, most of Routes F/H/I phenomenology is pre-empted and the writeups must say so. |
| **2210.07191** | Chen–Hou Part I — 2D Boussinesq finite-time blow-up | **The L1→L2 port's source of truth.** Spike 1 transcribed §2/§7 from it; the certification half still needs it. Also pins `β = 2.92` (Route-G's anchor). |
| **2209.08232** | (per LITERATURE_CHECK) | Gates the **finite-support** finding of Route-D v12/v13 — already assessed as *likely pre-empted*. Confirm or retract. |
| **2607.19762** | (per LITERATURE_CHECK) | Gates **Route-E v1's spectral picture** — already assessed as *likely pre-empted*. Confirm or retract. |

## Tier 2 — the methodological candidates, i.e. where novelty plausibly survives

| arXiv | what it is | what it gates |
|---|---|---|
| **2302.12877** | radii-polynomial / computer-assisted proof methodology | Gates the **only** claims with a real chance of being new: Route-D v6's discrete-ball trap, v3's weighted-`ℓ¹` no-go, and the elasticity discipline. Standard work uses geometric weights on bounded domains; ours is algebraic decay on an unbounded one. |
| **2312.01702** | tracking complex singularities on log-lattices | Gates "measure the exponent, not the threshold" (Route-F's method) and Route-I's log-periodic-band observation. The log-lattice programme is the most likely prior art for both. |
| **1908.09385** | dissipative gCLM | Second source on the relevance exponent; back-up for 2207.07548. |

## Tier 3 — would change numbers rather than claims

| arXiv | what it is | why |
|---|---|---|
| **2308.01528** | exact self-similar blow-up of the Hou–Luo model, smooth profiles | An *exact* profile gives an **exact `β`**, turning Route-G's `s_c = 1/(2β)` into a closed form for that model and giving the 2D leg a known-answer gate it does not currently have. |
| **2604.01868** | novel self-similar blow-ups, 1D Hou–Luo and 2D Boussinesq | If it exhibits **other** self-similar branches, Route-G's "the 2D scenario sits at `β = 2.92`" needs restating as "the Chen–Hou branch sits at 2.92" and the map needs more points. |
| 2010.01201, 2305.05895, 2401.14615, 2603.25104, 2604.09949 | assorted, cited in LITERATURE_CHECK | Context; lowest priority. |

## Not on arXiv — need another route

- **Schochet, CPAM 1986** — explicit solutions of the *viscous* CLM equation by
  complexification. **Gates Route-H's closed-form solution (E) directly**, which the leg
  already declines to claim. Publisher PDF; will not come from arXiv.
- **Nečas–Růžička–Šverák** (self-similar NS non-existence) and **Jia–Šverák**
  (the escaping class) — cited for framing in Routes H/I. Context, not gating.

---

## Host allowlist these need

`arxiv.org`, `export.arxiv.org`, `api.semanticscholar.org`, `www.semanticscholar.org`,
`link.springer.com`, `onlinelibrary.wiley.com`, `aimsciences.org`, `en.wikipedia.org`.
