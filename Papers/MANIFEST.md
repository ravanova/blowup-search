# Papers manifest — what to fetch, in priority order, and what each one gates

**Why this file exists.** `Papers/` is gitignored (we do not commit third-party PDFs), so
a previous session's downloads are **destroyed every time the container is rebuilt** —
which is what happened here: Spike 1's notes cite "Source PDFs live in `Papers/`" and the
directory no longer exists. The manifest and `fetch.sh` are committed so the PDFs can be
re-pulled in one command instead of re-derived from memory. **If you download papers, do
not commit them; commit any change to this manifest instead.**

**Nothing in this list has been read.** Five literature passes in `LITERATURE_CHECK.md`
are all search-level. Every novelty claim in this project is unverified against a primary
source. See the network directive at the top of `CONTINUATION_PROMPT.md` — this is
blocked on egress, not on effort.

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
