# ESCALATION — leg 265's Phase-1 construction decision packet: build it, or not?

**Raised** 2026-08-07 by leg 265 (Route-P2C), which escalated rather than landed.
**Carrier until 2026-09-10:** GitHub PR **#21**, now CLOSED UNMERGED. The work is preserved on the
pushed branch — see §6. Closing the PR retired the *carrier*, not the question.
**Status: OPEN. RECORDED, NOT RULED.** The journal's last line is the reason: *"Construction needs
the user's go — not this leg's, and not the DM's."*

Read with `ESCALATION_PHASE1_TARGET_2026-08-06.md`: that one asks whether the target is chosen, this
one asks what building it would cost and whether it is worth it. **Both must be Y for anything to be
built.**

---

## 1. The number the leg adds: `k(7/6) = 16.3479210517`

BCG index their branches by the Frobenius ratio `k(r)`, with `r_j` defined by `k(r_j) = j` and
`r^(n) ∈ (r_n, r_{n+1})` for **odd** n. **Nobody had ever evaluated `k` at the borderline** — BCG say
only *"n odd and large enough"* and never quantify it. Computed here in closed form from BCG's own
equations, validated first against **four of BCG's own anchors** (`R₁(1) = 0.8 = 2(γ−1)`, `R₂(1) = 0`,
`k(1) = 1`, `k → ∞` at `r* = (7−√5)/4`), monotone on 38 points.

| | |
|---|---|
| smallest **odd** n BCG's own NS theorem can use | **n ≥ 17** |
| odd branches entirely inside the target window `(1, 7/6]` | **3, 5, 7, 9, 11, 13, 15** (seven) |

## 2. This corrects leg 251, and the correction is load-bearing

Leg 251's ansatz said `r^(n)`, **n odd and LARGE**. But `k` increases to `+∞` at `r*`, so **large n
forces `r → r*`, deep INSIDE the dominance window** — the exact opposite of leg 251's **own
obligation 4** (r-coverage *outside* the dominance regime). **Its ansatz and its obligation pulled in
opposite directions.** The certificate needs **small** odd n. Leg 275 applied this back into leg
251's report.

**Recommended target: `n = 3`**, `r^(3) ∈ (1.070374, 1.094975)`, `δ_dis ∈ (−0.5778, −0.4302)` — the
only branch in the window whose existence is **unconditional** (BCG **Thm 1.1**, all `γ > 1`, no
"large enough"). **`n = 15`** is 31–41× cheaper (`|δ_dis| ≤ 0.0141`) but Thm 1.2's *"large enough"* is
unquantified — left **OPEN, not assumed**.

**The trap, stated:** at `r = 7/6` exactly, `δ_dis = 0` and the viscous system is **autonomous** — the
one exponent giving a stationary viscous profile problem. But `k(7/6)` is not an integer, so it lies
in the **even** gap `(r₁₆, r₁₇)`, and BCG's odd-n construction supplies **no profile there**.

## 3. The question, stated so it can be answered Y or N

**Q. Authorize Phase-1 construction against the `n = 3` BCG target — Y or N?**

- **Y** is `ORCHESTRATION.md` §8 escalation 1 and needs the user's signature. It would be the first
  **Grade-A × fluid-adjacent** certificate — leg 174's still-empty cell.
- **N** closes the packet. Nothing has been built against it, so nothing is wasted.

## 4. What a Y would be buying, and what it would NOT

**Not Clay's equation** (constitutive vs. nonlocal pressure); **not Clay's mechanism** (density
compression, **no vortex stretching** radially); **Wall 2 not crossed**; and **the blow-up is already
proved** (BCG Thm 1.3) — a certificate upgrades DOMINATED → ENCLOSED, it **decides no open yes/no
question**.

> **The irony the leg states explicitly: the absence that makes leg 257 inapplicable here — no Leray
> projector — is the same absence that makes this not Clay's object. One fact, not two.**

**Clay odds stay ~0.05%. No link of the L1→L4 chain moves.**

## 5. What must be built, and the prior art that changes the number

**15 of 18** needed apparatus terms are absent from a 48-row `capabilities.py` (control **0 of 8**);
the 3 non-zero were adjudicated as float-level or different-object. BCG's **16** computer-assisted
statements touch the stability step **0 times**; CGSS has **0**. Leg 174's ~14 h / 10 000-coefficient
figure **confirmed at source** as `13:36:38`.

**`arXiv:2509.12435` (Larson–Penston)**, read at full text, 7 675 lines, **already puts interval
arithmetic inside the mode-stability step** of a radially imploding compressible profile, proves
maximal dissipativity on backward cones, cites BCG, ships **public code** (VNODE-LP) — **run on a
MacBook Air 2013**. Largest downward cost revision *and* a novelty ceiling. It is **inviscid**
(Euler–Poisson), so leg 251's obligation 1 stays unclaimed.

**Leg 257's obstruction was CHECKED, not assumed absent:** it needs a nonlocal operator + a
super-algebraic weight; both are absent and measured (15/16 nonlocal probe terms **0** in both papers
against live controls 167/185; the 16th adjudicated line by line). BCG's space is `H^{2m}(B(0,2))`
unweighted + algebraic `φ^{2K}` — **not** Breden–Chu's `H²(µ)`, **so the pending stage-V lift does not
gate this target.** A different obstruction of the same *type* is present and named — derivative
excess plus vacuum degeneracy `S^{−5}` — and is **repaired by SIGN, not boundedness**, available
because `D_dis` is parabolic where `P[(U·∇)U]` has no sign. The repair is `δ_dis`-independent, so it
survives into the target window. **Had it been of leg 257's severity, this would have been a gate NO.**

**Ban walk:** the re-posed stage-V ban does **not** bite — a BCG-shaped certificate is not a
radii-polynomial certificate. The sting: this repo's five most-developed certificate rows are the
**wrong** apparatus, not merely a banned one.

## 6. Where the work is

Branch **`leg/265-p2c-v1`**, head **`8e592d4685ca2fe9bbf1befcf92b7e491a5846f9`**, 2 commits, never
merged to `main`. Four files, 2,083 insertions: `experiments/journal/leg_265.md`,
`experiments/p2_route_p2c_v1_costing.py` (32/32 self-tests),
`writeup/data/p2_route_p2c_v1_costing.json`, `writeup/novelty/leg_265.md` (committed at `af3d1fc`,
before a line of the runner existed).

## 7. Residues named rather than hidden, kept from the leg

- Whether **n = 15** meets Thm 1.2's unquantified *"large enough"* is **open**; n = 3 does not depend
  on it.
- `arXiv:2509.12435` is an **unrefereed preprint** carrying the feasibility datum.
- `arXiv:2603.10141` read at **abstract depth only**.
- **Provenance defect caught and kept:** the session scratchpad is **shared between concurrent legs**;
  a first novelty attempt would have reported **leg 257's** `nov.json` as this leg's. Nets re-run in a
  leg-private directory, 5 of 8 retried through 503/429.
- Both gate branches reached **live**: an early run returned **NO** on a genuinely failing self-test.
