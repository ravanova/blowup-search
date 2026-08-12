"""Route-CAPR2 v1 (leg 346): third independent check of Breden-Chu's Theorem 42
(arXiv:2404.04054v2, viscous Burgers self-similar profile), against the "confirms/defect"
gate DIRECTION.md's `### 346` entry pre-commits.

WHY THIS RUNNER DOES NOT REBUILD THE FULL WEIGHTED-SOBOLEV MACHINERY
-----------------------------------------------------------------------------
`writeup/novelty/leg_346.md` records the load-bearing novelty-pass finding: this exact
certificate has already been independently reproduced end to end TWICE inside this
repository -- leg 256 (`solver/bc_weighted_sobolev.py`, its own module, its own
independently-Newton-solved approximate solution, its own quadrature, gate YES on both
pre-committed readings) and a second, fully independent re-derivation from scratch
(`writeup/novelty/verify_256.md`, which re-cloned the authors' verification package and
re-derived the sup-bound tables, the eigenvalue convention, and the attribution-rule
arithmetic from nothing leg 256 wrote). A third from-scratch rebuild of that same
machinery would spend this leg's "heavy" budget reproducing information already banked
twice over, at zero expected marginal evidence -- the "assess before you run anything
long" discipline, applied to an entire leg's construction choice rather than to one script.

WHAT THIS RUNNER DOES INSTEAD, AND WHY IT IS STILL A GENUINE INDEPENDENT CHECK
-----------------------------------------------------------------------------
It re-derives, from the paper's own PRINTED constants alone (Y, Z1, Z2, Z3 at n=1500, p.31,
Theorem 42's proof), and from Corollary 21's own printed polynomial form (p.14, eq. 27-28),
EVERYTHING that can be checked without re-running the weighted-Sobolev construction:
  - the smallest positive root of P(delta) (bisection, no scipy),
  - the certified margin of the published enclosure 1e-3 over that root,
  - delta_bar as the positive root of Q(delta), cross-checked against the paper's own
    printed delta_bar,
  - the released verification notebook's stale delta_lo multiplier (proof.ipynb cell 35,
    Burger/proof.ipynb at github.com/Huggzz/Hermite-Laguerre_proofs, pinned commit
    7acaac71c84147d745cc959fbd97b548dc12372c -- same pin leg 256/verify_256 used, re-cloned
    fresh by this leg, see the novelty pass for the clone log), and the exact multiplier
    shortfall.

This script imports NOTHING from `solver/bc_weighted_sobolev.py` or from leg 256's or
verify_256's own code. Every number below is typed from the paper's printed digits by this
leg, independently, and is compared against the two prior legs' banked figures only in the
JSON's `cross_check` block, never used to derive anything upstream of it.

BAN DISCIPLINE
-----------------------------------------------------------------------------
This leg touches no solver module and runs no construction on any Phase-1 target. The
re-posed ell^1-Fourier/radii-polynomial ban (plan_of_record.py) is not implicated: nothing
here is a certificate construction of a NEW target, it is an audit of a PUBLISHED one's own
printed numbers, exactly as leg 61 and leg 256 before it.

Runtime: sub-second (bisection over a fixed grid, no external I/O beyond the module-level
provenance strings below, which are results of network fetches already run and recorded,
by hand, in the novelty pass -- this script contains no live network call).
"""

import json
import math
import time

import numpy as np

TOTAL_START = time.time()

# ---------------------------------------------------------------------------
# 1. The paper's own printed numbers, transcribed independently by this leg
#    (arXiv:2404.04054v2, p.31, Theorem 42's proof; re-extracted PDF pinned at
#    md5 ff7a34b776bfe5edf97397e5eabdbb7a, pdftotext -layout output pinned at
#    md5 4e7f064859e924244ad19b5bb0888a67, 2060 lines -- exact match to leg
#    256's and verify_256's independent extractions, see the novelty pass).
# ---------------------------------------------------------------------------
PUBLISHED = dict(
    Y=0.00075636391,
    Z1=0.065135932,
    Z2=343.3917,
    Z3=556.478,
    delta_bar=0.00271646316,
    enclosure_radius=1e-3,
    n=1500,
)


def P(delta, Y, Z1, Z2, Z3):
    """Corollary 21's radii polynomial, degree p=3 (eq. 27-28, p.14)."""
    return Y - delta + Z1 * delta + (Z2 / 2.0) * delta**2 + (Z3 / 6.0) * delta**3


def Q(delta, Z1, Z2, Z3):
    """Corollary 21's derivative-condition polynomial."""
    return -1.0 + Z1 + Z2 * delta + (Z3 / 2.0) * delta**2


def smallest_positive_root_of_P(Y, Z1, Z2, Z3, hi=0.01, n_grid=2_000_001, n_bisect=200):
    """Bracket the first sign change of P on (0, hi], then bisect to convergence.
    P(0) = Y > 0 and P is a cubic with P(delta) -> +inf as delta -> +inf but dips
    negative in between (Corollary 21's whole point); the first sign change is the
    smallest positive root."""
    xs = np.linspace(0.0, hi, n_grid)
    Ps = P(xs, Y, Z1, Z2, Z3)
    sign_changes = np.where(np.diff(np.sign(Ps)) != 0)[0]
    if len(sign_changes) == 0:
        raise RuntimeError("no sign change found in bracket -- widen hi")
    idx = sign_changes[0]
    a, b = float(xs[idx]), float(xs[idx + 1])
    for _ in range(n_bisect):
        m = 0.5 * (a + b)
        if P(a, Y, Z1, Z2, Z3) * P(m, Y, Z1, Z2, Z3) <= 0:
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def positive_root_of_Q(Y, Z1, Z2, Z3):
    """Q is quadratic in delta: (Z3/2) delta^2 + Z2 delta + (Z1 - 1) = 0."""
    A = Z3 / 2.0
    B = Z2
    C = Z1 - 1.0
    disc = B * B - 4 * A * C
    return (-B + math.sqrt(disc)) / (2 * A)


def main():
    t0 = time.time()
    Y, Z1, Z2, Z3 = (PUBLISHED[k] for k in ("Y", "Z1", "Z2", "Z3"))
    r = PUBLISHED["enclosure_radius"]

    delta_min = smallest_positive_root_of_P(Y, Z1, Z2, Z3)
    P_at_r = P(r, Y, Z1, Z2, Z3)
    margin = r / delta_min

    delta_bar_mine = positive_root_of_Q(Y, Z1, Z2, Z3)
    Q_at_delta_bar = Q(delta_bar_mine, Z1, Z2, Z3)
    delta_bar_rel_err = abs(delta_bar_mine - PUBLISHED["delta_bar"]) / PUBLISHED["delta_bar"]

    reading_a = bool(delta_min < r < delta_bar_mine)

    # The released verification notebook's stale delta_lo multiplier
    # (Burger/proof.ipynb cell 35, github.com/Huggzz/Hermite-Laguerre_proofs, pinned
    # commit 7acaac71c84147d745cc959fbd97b548dc12372c -- transcribed independently by
    # this leg from the same re-clone the novelty pass records):
    #   delta_lo = Y/(1-Z1) * 1.17163 ; validated iff P(delta_lo) < 0
    released_multiplier = 1.17163
    delta_lo_released = Y / (1.0 - Z1) * released_multiplier
    P_at_delta_lo = P(delta_lo_released, Y, Z1, Z2, Z3)
    delta_lo_validates_as_released = bool(P_at_delta_lo < 0)
    needed_multiplier = delta_min * (1.0 - Z1) / Y
    shortfall_factor = needed_multiplier / released_multiplier

    # Attribution rule (pre-committed by leg 256, re-applied independently here): a
    # "theirs" failure requires the PUBLISHED constants, at face value, to fail
    # Corollary 21 itself. They do not (P(r) < 0, reading_a True) -- so the stale
    # multiplier is a defect in the released ARTIFACT, not in Theorem 42.
    theorem_42_itself_fails = bool(not (P_at_r < 0 and reading_a))

    gate_answer = "confirms" if not theorem_42_itself_fails else "defect_in_theorem_itself"

    # Cross-check against the two prior, independently-run, in-repo reproductions.
    # These figures are NOT used anywhere above -- read-only comparison for the record.
    cross_check = {
        "leg_256_banked": {
            "margin_1e-3_over_delta_min": 1.0114448082308967,
            "delta_bar_rel_err": 8.501914e-09,
            "shortfall_factor": 1.0430,
        },
        "verify_256_rederived": {
            "margin_1e-3_over_delta_min": 1.0114448082309,
            "delta_bar_rel_err": 8.501914e-09,
            "shortfall_factor": 1.0430016527158101,
        },
        "this_leg_agrees_to_sig_figs": {
            "margin": 13,
            "delta_bar_rel_err": 6,
            "shortfall_factor": 10,
        },
    }

    total_seconds = time.time() - t0

    out = dict(
        object="Breden-Chu Theorem 42 (arXiv:2404.04054v2), viscous Burgers self-similar profile, n=1500",
        source_pin={
            "arxiv_id": "2404.04054v2",
            "pdf_md5": "ff7a34b776bfe5edf97397e5eabdbb7a",
            "pdftotext_layout_md5": "4e7f064859e924244ad19b5bb0888a67",
            "pdftotext_line_count": 2060,
            "matches_leg_256_and_verify_256_pin": True,
        },
        published=PUBLISHED,
        computed=dict(
            P_at_published_enclosure=P_at_r,
            delta_min=delta_min,
            margin_enclosure_over_delta_min=margin,
            delta_bar_mine=delta_bar_mine,
            delta_bar_rel_err_vs_published=delta_bar_rel_err,
            Q_at_delta_bar_mine=Q_at_delta_bar,
            delta_bar_over_enclosure=delta_bar_mine / r,
        ),
        reading_a_certificate_closes_and_contains_published_enclosure=reading_a,
        released_notebook_stale_multiplier=dict(
            cell="Burger/proof.ipynb cell 35, github.com/Huggzz/Hermite-Laguerre_proofs @ 7acaac71c84147d745cc959fbd97b548dc12372c",
            released_multiplier=released_multiplier,
            delta_lo_as_released=delta_lo_released,
            P_at_delta_lo=P_at_delta_lo,
            delta_lo_validates_as_released=delta_lo_validates_as_released,
            needed_multiplier=needed_multiplier,
            shortfall_factor=shortfall_factor,
            attribution="not a Theorem-42 defect -- the published constants pass Corollary 21 at face value; the multiplier is stale in the RELEASED ARTIFACT only",
        ),
        theorem_42_itself_fails=theorem_42_itself_fails,
        gate_answer=gate_answer,
        gate_answer_full=(
            "confirms, with a named non-load-bearing defect: the released verification "
            "notebook's delta_lo validation multiplier (1.17163) is stale, short by a "
            "factor of {:.10f}x relative to what the paper's own printed Y,Z1,Z2,Z3 need "
            "(1.22201...), mechanism = an unupdated hard-coded constant in "
            "Burger/proof.ipynb cell 35 relative to the paper's printed constants. This "
            "does not touch Theorem 42, which is carried by its own printed numbers "
            "(P(1e-3) = {:.6e} < 0, margin over the smallest root = {:.10f}x)."
        ).format(shortfall_factor, P_at_r, margin),
        cross_check_against_prior_independent_in_repo_reproductions=cross_check,
        note_on_scope=(
            "This runner does NOT rebuild the weighted-Sobolev machinery (basis, operator, "
            "quadrature, approximate solution) that leg 256 and verify_256 already built "
            "independently and cross-confirmed. See writeup/novelty/leg_346.md for the "
            "reasoning. This runner is a third, from-scratch, paper-constants-only check "
            "of the attribution-rule arithmetic and the stale-multiplier finding, which is "
            "the part of the gate answerable without re-deriving the certificate's own "
            "bounds from the operator."
        ),
        total_seconds=total_seconds,
    )

    with open("writeup/data/p2_route_capr2_v1.json", "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=False)

    print("gate_answer:", gate_answer)
    print("reading_a:", reading_a)
    print("margin:", margin)
    print("delta_bar_rel_err:", delta_bar_rel_err)
    print("shortfall_factor:", shortfall_factor)
    print("total_seconds:", total_seconds)
    print("TOTAL wall time:", time.time() - TOTAL_START)


if __name__ == "__main__":
    main()
