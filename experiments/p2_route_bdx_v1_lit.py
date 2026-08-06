#!/usr/bin/env python3
"""Leg 158 -- ROUTE-BDX: BDL arXiv:1503.06315 at full-text depth against the
ZERO-DIAGONAL case.

This is a LITERATURE AUDIT, not a construction.  It builds no certificate, computes
no Z_1, and touches no solver module -- it imports `solver.spectral_certificate`
READ-ONLY, purely to read this repository's tail operator's own coefficients out of
the landed code rather than re-deriving them from memory (leg 45's lesson).

What it measures, one BDL hypothesis at a time, as MAGNITUDES not booleans:

  (A) The tail operator IS in BDL's form (3):  L_k(x) = lam_k x_{k-1} + mu_k x_k
      + bet_k x_{k+1}.  Verified entrywise against `tail_block`, not asserted.
  (B) BDL assumption (4) -- the diagonal bounded BELOW: where C1 lands here.
  (C) BDL assumption (5) -- the dominance ratio delta < 1/2: where delta lands here.
  (D) BDL's LU machinery (their eq (9)-(10), Ciarlet Thm 4.3-2 p.142) evaluated on
      a zero diagonal: the Ciarlet continuants delta_n, and BDL's scalar w~ of their
      eq (20).  This is the part leg 57 did not do: not "the hypothesis fails" but
      "here is the exact arithmetic the construction executes, and here is the entry
      at which it divides by zero".
  (E) The 2x2 BLOCK recast (classical cyclic / odd-even reduction -- see
      writeup/novelty/leg_158.md FINDING 1; claimed by nobody here), which is the
      class BDL's own Section 5 names as future work.  Where do (4) and (5) land
      AFTER the recast?  Both pairing offsets are computed -- a control that can
      come out differently (lesson 90).
  (F) The price of the recast: the parity-imbalanced diagonal gauge needed to push
      the recast ratio below BDL's 1/2, measured as a growth exponent.

  (G) POSITIVE CONTROL: a synthetic BDL-ADMISSIBLE operator (mu_k = k, lam_k =
      bet_k = 0.2 k) run through the identical pipeline.  Every predicate below
      must come out the OTHER way on it, or the negatives above are statements
      about the code (lesson 90 / the standing positive-control rule).

Run:  /home/andy/projects/Unsolved/.venv/bin/python experiments/p2_route_bdx_v1_lit.py
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.spectral_certificate import tail_block  # READ-ONLY import

S_L = 1.0          # the tail's growth rate: entries ~ k/2, so omega_k^{sL} = k
K_MIN = 8          # stay clear of the low-mode accidents (lam_3 = 0 exactly)
K_MAX = 4096


# ---------------------------------------------------------------------------
# (A) read the operator's own coefficients OUT OF the landed module
# ---------------------------------------------------------------------------
def coefficients_from_module(K=4, M=64):
    """Extract (lam_k, mu_k, bet_k) of BDL's form (3) from `tail_block` itself.

    Returns dict mode -> (lam, mu, bet) for interior modes only (the window's two
    boundary rows are truncated and are not the operator's coefficients).
    """
    T = tail_block(K, M)
    out = {}
    for k in range(K + 2, M):          # interior rows only
        j = k - K - 1
        out[k] = (float(T[j, j - 1]), float(T[j, j]), float(T[j, j + 1]))
    return out


def coefficients_closed_form(k):
    """lam_k = 1 - (k-1)/2,  mu_k = 0,  bet_k = (k+1)/2  -- CHECKED against the module."""
    return (1.0 - (k - 1) / 2.0, 0.0, (k + 1) / 2.0)


def check_form_3():
    mod = coefficients_from_module()
    worst = 0.0
    for k, (lam, mu, bet) in mod.items():
        c = coefficients_closed_form(k)
        worst = max(worst, max(abs(lam - c[0]), abs(mu - c[1]), abs(bet - c[2])))
    return {
        "modes_checked": len(mod),
        "max_abs_discrepancy_vs_closed_form": worst,
        "diagonal_entries_all_exactly_zero": all(m == 0.0 for _, m, _ in mod.values()),
        "sample_mode": 20,
        "sample_lam_mu_bet": list(mod[20]),
    }


# ---------------------------------------------------------------------------
# (B)+(C) BDL assumptions (4) and (5), scalar form
# ---------------------------------------------------------------------------
def scalar_hypotheses(coef, k_min=K_MIN, k_max=K_MAX):
    ks = [k for k in range(k_min, k_max)]
    C2 = 0.0
    C1 = np.inf
    delta = 0.0
    for k in ks:
        lam, mu, bet = coef(k)
        w = float(k) ** S_L
        C2 = max(C2, abs(lam) / w, abs(mu) / w, abs(bet) / w)
        C1 = min(C1, abs(mu) / w)
        if mu == 0.0:
            delta = np.inf
        else:
            delta = max(delta, abs(lam / mu), abs(bet / mu))
    return {
        "k_range": [k_min, k_max],
        "s_L": S_L,
        "assumption_4_C2_upper": C2,
        "assumption_4_C1_lower": C1,
        "assumption_4_holds": bool(C1 > 0.0),
        "assumption_5_delta": (None if np.isinf(delta) else delta),
        "assumption_5_delta_is_infinite": bool(np.isinf(delta)),
        "assumption_5_threshold": 0.5,
        "assumption_5_holds": bool((not np.isinf(delta)) and delta < 0.5),
    }


# ---------------------------------------------------------------------------
# (D) BDL's own LU arithmetic, executed on this operator
# ---------------------------------------------------------------------------
def ciarlet_continuants(coef, m, n_terms=12):
    """BDL p.4: a_{i+1} = lam_{m+i}, b_i = mu_{m+i-1}, c_i = bet_{m+i-1};
    delta_0 = 1, delta_1 = b_1, delta_n = b_n delta_{n-1} - a_n c_{n-1} delta_{n-2}.
    """
    a = {}
    b = {}
    c = {}
    for i in range(1, n_terms + 2):
        lam, mu, bet = coef(m + i - 1)
        b[i] = mu
        c[i] = bet
        a[i + 1] = coef(m + i)[0]
    d = [1.0, b[1]]
    for n in range(2, n_terms + 1):
        d.append(b[n] * d[n - 1] - a[n] * c[n - 1] * d[n - 2])
    return d


def lu_diagnosis(coef, m=64, n_terms=12):
    d = ciarlet_continuants(coef, m, n_terms)
    # U_I's diagonal (BDL eq (10)) is delta_n / delta_{n-1}; L_I's entries divide by
    # delta_n as well.  A vanishing delta_n is a breakdown of the factorization
    # itself, not a failure of an estimate.
    zeros = [n for n, v in enumerate(d) if v == 0.0]
    first_zero = zeros[0] if zeros else None
    # BDL eq (20): w~ = delta_0/delta_1 + sum_{l=1}^{L-1} delta_0^2/(delta_l delta_{l+1}) * ...
    # Its LEADING term is delta_0/delta_1.
    w_leading_defined = (d[1] != 0.0)
    return {
        "m": m,
        "continuants_delta_n": d,
        "zero_continuant_indices": zeros,
        "first_vanishing_continuant": first_zero,
        "all_odd_continuants_vanish": all(v == 0.0 for i, v in enumerate(d) if i % 2 == 1),
        "u_diagonal_delta1_over_delta0": (d[1] / d[0]) if d[0] != 0 else None,
        "bdl_eq20_leading_term_delta0_over_delta1_defined": bool(w_leading_defined),
        "bdl_eq20_leading_term_value": (d[0] / d[1]) if w_leading_defined else None,
    }


# ---------------------------------------------------------------------------
# (E) the 2x2 block recast
# ---------------------------------------------------------------------------
def block_hypotheses(coef, offset, k_min=K_MIN, k_max=1024):
    """Pair modes (k, k+1) for k = offset (mod 2).  Then

        D_j   = [[mu_k, bet_k], [lam_{k+1}, mu_{k+1}]]      (block diagonal)
        L_j   = [[0, lam_k], [0, 0]]                        (coupling to block j-1)
        U_j   = [[0, 0], [bet_{k+1}, 0]]                    (coupling to block j+1)

    With mu == 0, D_j is ANTI-diagonal, det D_j = -bet_k lam_{k+1}, and the block
    dominance ratios ||D_j^{-1} L_j||, ||D_j^{-1} U_j|| reduce to |lam_k/bet_k| and
    |bet_{k+1}/lam_{k+1}| -- ratios of the two OFF-diagonals, with the (zero)
    diagonal no longer appearing.  That is the whole content of the recast.
    """
    ks = [k for k in range(k_min, k_max) if k % 2 == offset % 2]
    C1b, C2b, dlt = np.inf, 0.0, 0.0
    ratios = []
    dets = []
    for k in ks:
        lam_k, mu_k, bet_k = coef(k)
        lam_k1, mu_k1, bet_k1 = coef(k + 1)
        D = np.array([[mu_k, bet_k], [lam_k1, mu_k1]], float)
        Lj = np.array([[0.0, lam_k], [0.0, 0.0]])
        Uj = np.array([[0.0, 0.0], [bet_k1, 0.0]])
        det = float(np.linalg.det(D))
        dets.append(det)
        if det == 0.0:
            C1b = 0.0
            dlt = np.inf
            continue
        Dinv = np.linalg.inv(D)
        w = float(k) ** S_L
        smin = float(np.linalg.svd(D, compute_uv=False)[-1])
        C1b = min(C1b, smin / w)
        C2b = max(C2b, float(np.linalg.norm(D, np.inf)) / w)
        r_lo = float(np.linalg.norm(Dinv @ Lj, np.inf))
        r_hi = float(np.linalg.norm(Dinv @ Uj, np.inf))
        ratios.append((k, r_lo, r_hi))
        dlt = max(dlt, r_lo, r_hi)
    tail_r = ratios[-1] if ratios else (None, None, None)
    return {
        "pairing_offset": offset % 2,
        "k_range": [k_min, k_max],
        "blocks": len(ks),
        "block_assumption_4_C1_lower": (None if np.isinf(C1b) else C1b),
        "block_assumption_4_C2_upper": C2b,
        "block_assumption_4_holds": bool(C1b > 0.0),
        "min_abs_det_block_diagonal": float(np.min(np.abs(dets))),
        "block_delta": (None if np.isinf(dlt) else dlt),
        "block_delta_is_infinite": bool(np.isinf(dlt)),
        "block_delta_threshold": 0.5,
        "block_assumption_5_holds": bool((not np.isinf(dlt)) and dlt < 0.5),
        "largest_k_ratios_lower_upper": [tail_r[1], tail_r[2]],
        "ratio_limit_estimate": (max(tail_r[1], tail_r[2]) if ratios else None),
    }


# ---------------------------------------------------------------------------
# (F) the price: the parity-imbalanced gauge needed to reach delta_block < 1/2
# ---------------------------------------------------------------------------
def gauge_price(coef, offset, target, k_min=K_MIN, n_blocks_list=(4, 8, 16, 32, 64)):
    """A diagonal gauge s_k rescales lam_k -> lam_k s_{k-1}/s_k, bet_k -> bet_k s_{k+1}/s_k.
    The lower ratio |lam_k/bet_k| then carries a factor s_{k-1}/s_{k+1} (an ODD-chain
    step when k is odd, EVEN when even) and the upper ratio |bet_{k+1}/lam_{k+1}| carries
    s_{k+2}/s_k -- the OTHER chain.  So both can be shrunk at once, but only by driving
    the two parity chains apart.  Forcing both ratios <= `target` over J consecutive
    blocks forces the parity imbalance
        R(J) = (s_odd chain) / (s_even chain)
    to grow like prod_j (r_lo,j r_hi,j) / target^{2J}.  This measures log R(J)/J.
    """
    out = []
    for J in n_blocks_list:
        ks = [k for k in range(k_min, k_min + 4 * J) if k % 2 == offset % 2][:J]
        log_r = 0.0
        for k in ks:
            lam_k, _, bet_k = coef(k)
            lam_k1, _, _ = coef(k + 1)
            _, _, bet_k1 = coef(k + 1)
            r_lo = abs(lam_k / bet_k)
            r_hi = abs(bet_k1 / lam_k1)
            log_r += np.log(max(r_lo, 1e-300)) + np.log(max(r_hi, 1e-300))
        log_R = log_r - 2 * J * np.log(target)
        out.append({
            "blocks_J": J,
            "log_parity_imbalance": float(log_R),
            "imbalance_per_block": float(log_R / J),
            "imbalance_factor_per_block": float(np.exp(log_R / J)),
        })
    return {
        "target_delta": target,
        "pairing_offset": offset % 2,
        "rows": out,
        "geometric_growth_rate_per_block": out[-1]["imbalance_factor_per_block"],
    }


# ---------------------------------------------------------------------------
# (G) positive control -- a BDL-ADMISSIBLE operator through the same pipeline
# ---------------------------------------------------------------------------
def control_coefficients(k):
    """mu_k = k (diagonal bounded below at C1 = 1), lam_k = bet_k = 0.2 k
    => BDL assumption (4) holds with C1 = 1, C2 = 1; assumption (5) holds, delta = 0.2."""
    return (0.2 * k, 1.0 * k, 0.2 * k)


def main():
    res = {
        "leg": 158,
        "route": "ROUTE-BDX",
        "kind": "literature audit -- no construction, no certificate, no Z_1",
        "source": {
            "arxiv": "1503.06315",
            "url": "https://arxiv.org/abs/1503.06315",
            "pdf": "https://arxiv.org/pdf/1503.06315",
            "title": "Rigorous numerics for nonlinear operators with tridiagonal "
                     "dominant linear part",
            "authors": "M. Breden, L. Desvillettes, J.-P. Lessard",
            "read_at": "full text (27 pp.), pdftotext -layout",
        },
        "object": {
            "module": "solver/spectral_certificate.py",
            "function": "tail_block(K, M, mu=0.0)",
            "docstring_quote": "Bidiagonal, zero diagonal.",
            "note": "It is in fact TRIDIAGONAL with an identically zero diagonal, "
                    "i.e. exactly BDL's form (3) with mu_k == 0.",
        },
        "A_form_3_check": check_form_3(),
        "B_C_scalar_hypotheses": scalar_hypotheses(coefficients_closed_form),
        "D_lu_diagnosis": lu_diagnosis(coefficients_closed_form),
        "E_block_recast": {
            "offset_0": block_hypotheses(coefficients_closed_form, 0),
            "offset_1": block_hypotheses(coefficients_closed_form, 1),
        },
        "F_gauge_price": gauge_price(coefficients_closed_form, 0, 0.49),
        "G_positive_control": {
            "operator": "mu_k = k, lam_k = bet_k = 0.2 k",
            "scalar_hypotheses": scalar_hypotheses(control_coefficients),
            "lu_diagnosis": lu_diagnosis(control_coefficients),
            "block_recast_offset_0": block_hypotheses(control_coefficients, 0),
        },
    }

    sc = res["B_C_scalar_hypotheses"]
    bl = res["E_block_recast"]["offset_0"]
    ct = res["G_positive_control"]["scalar_hypotheses"]
    res["verdict"] = {
        "scalar_assumption_4_C1": sc["assumption_4_C1_lower"],
        "scalar_assumption_5_delta": "infinite" if sc["assumption_5_delta_is_infinite"] else sc["assumption_5_delta"],
        "block_assumption_4_C1": bl["block_assumption_4_C1_lower"],
        "block_assumption_5_delta": bl["block_delta"],
        "block_delta_still_above_bdl_threshold": bool(
            bl["block_delta"] is not None and bl["block_delta"] >= 0.5),
        "control_reports_the_other_answer": bool(
            ct["assumption_4_holds"] and ct["assumption_5_holds"]),
        "statement": (
            "BDL's scalar hypotheses fail on this operator INFINITELY (C1 = 0, delta = "
            "infinity) and their LU construction divides by zero at its first step. "
            "The 2x2 block recast named by BDL's own Section 5 as future work restores "
            "an invertible block diagonal and replaces delta = infinity by a FINITE "
            "ratio, but that ratio is >= 1/2, so BDL's threshold is still not met, and "
            "buying it down costs a geometrically parity-imbalanced weight."
        ),
    }

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_bdx_v1_lit.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=False)
    print(json.dumps(res["verdict"], indent=2))
    print("\nwrote", out)


if __name__ == "__main__":
    main()
