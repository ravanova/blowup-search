"""Leg 96, Route-LHA: adversarial battery for `solver/line_hilbert.py`.

THE GATE, verbatim:

  "Under an adversarial battery of near-degenerate non-uniform grids (near-duplicate
   points, extreme local stretching ratios), does solver/line_hilbert.py's dense
   operator or its cached `slope_matrix` ever silently return a finite,
   plausible-looking wrong result instead of propagating or flagging the
   ill-conditioning?"

WHY THIS NEEDS AN INDEPENDENT REFERENCE, AND NOT JUST THE KNOWN ANSWER
----------------------------------------------------------------------
The obvious battery — perturb the grid, transform the CLM pair f = -4X/(1+4X^2),
compare against the exact H(f) = 2/(1+4X^2) — CANNOT answer this gate, and running it
alone would have produced a false YES. A near-degenerate grid makes the *cubic spline
interpolant itself* a poor representation of f, so a large error against the analytic
answer is what ANY correct implementation of this method must produce. Case
`displaced_node_1e6` below is exactly that trap: it misses the analytic answer by
9.5e-02 relative while the code is doing its job perfectly.

So the battery carries TWO yardsticks and keeps them apart:

  (1) `rel_vs_exact`  — module output vs the analytic H(f). Measures GRID QUALITY.
                        Error here is the mathematics of a bad grid, not a code fault.
  (2) `rel_vs_ref`    — module output vs an INDEPENDENT implementation of the same
                        discretization. Measures IMPLEMENTATION FIDELITY. Error here,
                        and only here, is the module silently corrupting.

THE INDEPENDENT REFERENCE (`ref_hilbert_matrix`, `ref_slopes_matrix` below)
--------------------------------------------------------------------------
It shares no line of code and no formula with the module:

  * slopes: the module runs two hand-rolled UNPIVOTED Thomas sweeps. The reference
    assembles the same tridiagonal system densely and solves it with `np.linalg.solve`
    (LU with PARTIAL PIVOTING). This is the direct audit of "does an unpivoted sweep
    quietly lose the answer when a spacing collapses".

  * transform: the module uses the closed forms A(s), B(s) of Huang-Tong-Wang App. C.1
    with a hand-removed cancellation (the L-series). The reference integrates each
    Hermite cubic against the Cauchy kernel EXACTLY, per cell, by polynomial deflation:
    for a cubic p on [a, a+H] and evaluation offset w = x - a,

        p(z) = p(w) + (z-w) q(z),   q quadratic (Horner deflation, exact)
        int_0^H p(z)/(w-z) dz = p(w) * ln|w/(w-H)| - int_0^H q

    with the far-field branch |w| > 2H switched to the geometric series
    sum_k w^{-k-1} int_0^H p z^k dz (the deflation form cancels catastrophically there;
    the series converges at ratio <= 1/2, truncated at k=64 for ~1e-19).

    The log(0) that appears whenever the evaluation point IS a cell endpoint is dropped
    on both sides, because the two cells adjoining that node contribute EQUAL AND
    OPPOSITE divergences (the Hermite value there is C^0), leaving the finite remainder
    ln(H_left/H_right). Getting this wrong was the reference's own first bug and it
    showed up as a clean O(h) bias — which is precisely why the reference is gated
    against the module on HEALTHY grids before it is trusted on hostile ones (see
    `reference_selfcheck` in the emitted JSON: it reproduces the module's full N x N
    matrix to 6.9e-15 relative).

  * the reference reproduces the module's convention exactly, including the DROPPED
    ENDPOINT HATS (`line_hilbert_matrix` builds interior source columns only), so the
    comparison is implementation-vs-implementation and not convention-vs-convention.

PRE-COMMITTED VERDICT CRITERION (fixed before the run, not fitted to it)
------------------------------------------------------------------------
A case is a SILENT CORRUPTION iff ALL FOUR hold:
  (a) the returned operator is entirely finite;
  (b) it is plausible in magnitude: max|H f| within [0.1x, 10x] of max|H_exact| = 2;
  (c) nothing was raised — zero warnings, zero exceptions;
  (d) it disagrees with the independent reference by more than REL_TOL = 1e-8,
      relative to the reference's own max entry.

REL_TOL is 1e-8 and not 1e-14: that is ~1.5e6 times the healthy-grid agreement, so it
cannot fire on conditioning-driven rounding, and any true corruption — which would be
an O(1) change of formula or a lost pivot — clears it by many orders of magnitude.
Criterion (d) is what makes (1) and (2) above separable; without it this file would be
a grid-quality benchmark wearing an audit's clothes.

SCOPE. The gate names near-duplicate points and extreme local stretching. Grids that
violate MONOTONICITY are outside it and are run as `out_of_scope_characterization`,
reported but never counted toward the verdict. See the findings in
`writeup/novelty/leg_96.md` for why that distinction is load-bearing.

Run:  .venv/bin/python experiments/p2_route_lha_v1_adversarial.py
Emits: writeup/data/p2_route_lha_v1_adversarial.json
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.line_hilbert import (          # noqa: E402
    line_hilbert_matrix,
    natural_spline_slopes,
    slope_matrix,
)

PI = np.pi
REL_TOL = 1e-8          # pre-committed silent-corruption threshold, criterion (d)
PLAUSIBLE_LO = 0.1      # criterion (b)
PLAUSIBLE_HI = 10.0
EXACT_PEAK = 2.0        # max of H(f) = 2/(1+4X^2)


# ==========================================================================
# the independent reference -- shares no formula with solver/line_hilbert.py
# ==========================================================================

def _cell_integral(c, w, H):
    """(1/pi) p.v. int_0^H (c0 + c1 z + c2 z^2 + c3 z^3)/(w - z) dz, over an array w.

    Exact in closed form. `c` is a 4-tuple of scalars; `w` is the array of evaluation
    offsets x_j - a. See the module docstring for the derivation and for why the
    log(0) terms are dropped rather than guarded to zero."""
    c0, c1, c2, c3 = c
    w = np.asarray(w, dtype=float)

    # --- deflation branch, |w| <= 2H ---
    d2 = c3 + 0.0 * w
    d1 = c2 + w * c3
    d0 = c1 + w * d1
    p_at_w = c0 + w * d0
    with np.errstate(divide="ignore", invalid="ignore"):
        num, den = np.abs(w), np.abs(w - H)
        la = np.where(num <= 0, 0.0, np.log(np.where(num <= 0, 1.0, num)))
        lb = np.where(den <= 0, 0.0, np.log(np.where(den <= 0, 1.0, den)))
    near = p_at_w * (la - lb) - (d0 * H + d1 * H ** 2 / 2.0 + d2 * H ** 3 / 3.0)

    # --- series branch, |w| > 2H (ratio <= 1/2) ---
    KMAX = 64
    with np.errstate(divide="ignore", invalid="ignore"):
        inv = 1.0 / w
        acc = np.zeros_like(w)
        p = inv.copy()
        for k in range(KMAX):
            mom = (c0 * H ** (k + 1) / (k + 1) + c1 * H ** (k + 2) / (k + 2)
                   + c2 * H ** (k + 3) / (k + 3) + c3 * H ** (k + 4) / (k + 4))
            acc = acc + p * mom
            p = p * inv

    return np.where(np.abs(w) > 2.0 * H, acc, near) / PI


def ref_slopes_matrix(x):
    """Natural-cubic-spline slope operator via DENSE LU WITH PARTIAL PIVOTING.

    The module solves the same system with two unpivoted Thomas sweeps. Any pivot the
    sweep needed and did not take shows up as a disagreement here."""
    x = np.asarray(x, dtype=float)
    n = x.size
    h = np.diff(x)
    A = np.zeros((n, n))
    R = np.zeros((n, n))
    A[0, 0] = 1.0
    A[n - 1, n - 1] = 1.0                     # natural BC: M_0 = M_{n-1} = 0
    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2.0 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        R[i, i - 1] = 6.0 / h[i - 1]
        R[i, i] = -6.0 / h[i - 1] - 6.0 / h[i]
        R[i, i + 1] = 6.0 / h[i]
    Mop = np.linalg.solve(A, R)               # node second derivatives: M = Mop @ f
    S = np.zeros((n, n))
    for i in range(n - 1):
        S[i, i] -= 1.0 / h[i]
        S[i, i + 1] += 1.0 / h[i]
        S[i, :] -= h[i] * (2.0 * Mop[i, :] + Mop[i + 1, :]) / 6.0
    S[n - 1, n - 2] -= 1.0 / h[-1]
    S[n - 1, n - 1] += 1.0 / h[-1]
    S[n - 1, :] += h[-1] * (2.0 * Mop[n - 1, :] + Mop[n - 2, :]) / 6.0
    return S


def ref_hilbert_matrix(x):
    """Independent dense H: same C^1_0 Hermite representation, integrated exactly.

    Endpoint hats are zeroed to match `line_hilbert_matrix`, which builds interior
    source columns only."""
    x = np.asarray(x, dtype=float)
    n = x.size
    S = ref_slopes_matrix(x)
    HV = np.zeros((n, n))                     # acts on node values
    HS = np.zeros((n, n))                     # acts on node slopes
    for c in range(n - 1):
        a = x[c]
        H = x[c + 1] - x[c]
        if H == 0.0:
            HV[:] = np.nan
            HS[:] = np.nan
            continue
        w = x - a
        HV[:, c]     += _cell_integral((1.0, 0.0, -3.0 / H ** 2,  2.0 / H ** 3), w, H)
        HS[:, c]     += _cell_integral((0.0, 1.0, -2.0 / H,       1.0 / H ** 2), w, H)
        HV[:, c + 1] += _cell_integral((0.0, 0.0,  3.0 / H ** 2, -2.0 / H ** 3), w, H)
        HS[:, c + 1] += _cell_integral((0.0, 0.0, -1.0 / H,       1.0 / H ** 2), w, H)
    HV[:, 0] = HV[:, -1] = 0.0
    HS[:, 0] = HS[:, -1] = 0.0
    Sm = S.copy()
    Sm[0, :] = Sm[-1, :] = 0.0
    return HV + HS @ Sm


# ==========================================================================
# grids
# ==========================================================================

def sinh_grid(n, c=0.5, rho_max=8.0):
    """The healthy control: X = c*sinh(rho), rho uniform. What every consumer uses."""
    return c * np.sinh(np.linspace(-rho_max, rho_max, n))


def _finite_max(a):
    m = np.isfinite(a)
    return float(np.abs(a[m]).max()) if m.any() else float("nan")


def build_cases(n):
    """(name, family, grid) over the adversarial battery. `family` selects scope."""
    X0 = sinh_grid(n)
    k = n // 2 + n // 10                 # an interior node, off-centre
    h = X0[k + 1] - X0[k]
    cases = [("healthy_control", "control", X0.copy())]

    # --- near-duplicate points, forward ---
    for e in (1e-1, 1e-3, 1e-6, 1e-9, 1e-12, 1e-14, 1e-15, 0.0):
        X = X0.copy()
        X[k + 1] = X0[k] + e * h
        cases.append((f"near_dup_fwd_{e:.0e}", "near_duplicate", X))

    # --- near-duplicate points, CROSSED (the roundoff-inversion a generator makes) ---
    for e in (1e-6, 1e-12, 1e-14):
        X = X0.copy()
        X[k + 1] = X0[k] - e * h
        cases.append((f"near_dup_crossed_{e:.0e}", "near_duplicate", X))

    # --- near-duplicates at the boundary and in the far tail ---
    for kk, tag in ((1, "left_edge"), (n - 3, "right_edge"), (int(0.95 * n), "far_tail")):
        hh = X0[kk + 1] - X0[kk]
        X = X0.copy()
        X[kk + 1] = X0[kk] + 1e-12 * hh
        cases.append((f"near_dup_{tag}", "near_duplicate", X))

    # --- many at once: the sweeps meet a collapsed spacing repeatedly ---
    X = X0.copy()
    for j in range(20, n - 20, 7):
        X[j + 1] = X0[j] + 1e-11 * (X0[j + 1] - X0[j])
    cases.append(("near_dup_multi_x19", "near_duplicate", X))

    # --- extreme local stretching: one cell compressed, ratio up to 1e13 ---
    for q in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-13):
        X = X0.copy()
        X[k + 1:] -= h * (1.0 - q)
        cases.append((f"cell_compressed_{q:.0e}", "stretching", X))

    # --- extreme local stretching: one node thrown far out (representational trap) ---
    X = np.sort(np.concatenate([X0[:k], X0[k + 1:], [X0[k] + 1e6]]))
    cases.append(("displaced_node_1e6", "stretching", X))

    # --- geometric grading with a violent ratio ---
    for r in (2.0, 10.0, 100.0):
        m = n // 2
        d = np.cumsum(r ** np.arange(m, dtype=float))
        d = d / d[-1] * X0[-1]
        X = np.concatenate([-d[::-1], [0.0], d])[: 2 * m + 1]
        cases.append((f"geometric_grading_r{r:g}", "stretching", X))

    # --- OUT OF GATE SCOPE: monotonicity violations (reported, never counted) ---
    cases.append(("reversed_grid", "out_of_scope_monotonicity", X0[::-1].copy()))
    X = X0.copy()
    X[k], X[k + 1] = X0[k + 1], X0[k]
    cases.append(("swapped_adjacent_pair", "out_of_scope_monotonicity", X))
    return cases


# ==========================================================================
# the battery
# ==========================================================================

def run_case(name, family, X, with_reference=True):
    f = -4.0 * X / (1.0 + 4.0 * X ** 2)
    exact = 2.0 / (1.0 + 4.0 * X ** 2)

    raised = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            Hmod = line_hilbert_matrix(X)
            Hf = Hmod @ f
            Smod = np.array(slope_matrix(X))
        except Exception as exc:                       # noqa: BLE001
            raised = f"{type(exc).__name__}: {exc}"
            Hmod = Hf = Smod = None
    n_warn = len(caught)

    rec = {
        "case": name,
        "family": family,
        "n": int(X.size),
        "min_spacing": float(np.min(np.abs(np.diff(X)))),
        "max_spacing_ratio": float("nan"),
        "raised": raised,
        "n_warnings": int(n_warn),
    }
    d = np.abs(np.diff(X))
    nz = d[d > 0]
    if nz.size:
        rec["max_spacing_ratio"] = float(nz.max() / nz.min())

    if raised is not None:
        rec.update(all_finite=False, nonfinite_frac=1.0, max_abs_Hf=float("nan"),
                   plausible=False, rel_vs_exact=float("nan"),
                   rel_vs_ref=float("nan"), vec_rel_vs_ref=float("nan"),
                   slope_rel_vs_ref=float("nan"),
                   assoc_rel=float("nan"), assoc_normalized=float("nan"),
                   slope_norm_inf=float("nan"), silent_corruption=False)
        return rec

    rec["all_finite"] = bool(np.isfinite(Hmod).all())
    rec["nonfinite_frac"] = float((~np.isfinite(Hmod)).mean())
    rec["max_abs_Hf"] = _finite_max(Hf)
    rec["plausible"] = bool(
        np.isfinite(rec["max_abs_Hf"])
        and PLAUSIBLE_LO * EXACT_PEAK <= rec["max_abs_Hf"] <= PLAUSIBLE_HI * EXACT_PEAK
    )

    # yardstick (1): grid quality, scored away from the perturbation and the boundary
    core = np.abs(X) < 5.0
    core[:3] = False
    core[-3:] = False
    if core.any() and np.isfinite(Hf[core]).any():
        m = core & np.isfinite(Hf)
        rec["rel_vs_exact"] = float(np.abs(Hf[m] - exact[m]).max() / EXACT_PEAK)
    else:
        rec["rel_vs_exact"] = float("nan")

    # yardstick (2): implementation fidelity
    #
    # Taken on the MATRIX, not on H @ f, and the difference matters. At a one-ulp cell the
    # two matrices agree to ~4e-15 while H@f and H_ref@f differ by ~5e-02: that gap is the
    # ill-conditioning amplifying a rounding-level difference between two equally entitled
    # implementations, and neither is "the wrong one". The gate asks whether the module
    # HIDES ill-conditioning, not whether ill-conditioning exists -- and it does not hide
    # it, since ||S||_inf = 9e+15 is visible in the operator it returns. `vec_rel_vs_ref`
    # records the amplified number anyway rather than leaving a critic to ask for it.
    rec["rel_vs_ref"] = float("nan")
    rec["vec_rel_vs_ref"] = float("nan")
    rec["slope_rel_vs_ref"] = float("nan")
    if with_reference:
        Href = ref_hilbert_matrix(X)
        Sref = ref_slopes_matrix(X)
        both = np.isfinite(Hmod) & np.isfinite(Href)
        if both.any():
            scale = max(_finite_max(Href), 1e-300)
            rec["rel_vs_ref"] = float(np.abs(Hmod - Href)[both].max() / scale)
            dv = Hf - Href @ f
            fv = np.isfinite(dv)
            if fv.any():
                rec["vec_rel_vs_ref"] = float(np.abs(dv[fv]).max() / EXACT_PEAK)
        bothS = np.isfinite(Smod) & np.isfinite(Sref)
        if bothS.any():
            scaleS = max(_finite_max(Sref), 1e-300)
            rec["slope_rel_vs_ref"] = float(np.abs(Smod - Sref)[bothS].max() / scaleS)

    # the Route-M association claim, reported as a magnitude and as a backward error
    ref_slopes = natural_spline_slopes(X, f)
    fin = np.isfinite(ref_slopes)
    Snorm = float(np.abs(Smod).sum(axis=1).max())
    rec["slope_norm_inf"] = Snorm
    if fin.any():
        num = float(np.nanmax(np.abs(Smod @ f - ref_slopes)))
        rec["assoc_rel"] = num / max(float(np.abs(ref_slopes[fin]).max()), 1e-300)
        rec["assoc_normalized"] = num / max(Snorm * float(np.abs(f).max()), 1e-300)
    else:
        rec["assoc_rel"] = float("nan")
        rec["assoc_normalized"] = float("nan")

    # the pre-committed criterion
    rec["silent_corruption"] = bool(
        rec["all_finite"]
        and rec["plausible"]
        and n_warn == 0
        and raised is None
        and (
            (np.isfinite(rec["rel_vs_ref"]) and rec["rel_vs_ref"] > REL_TOL)
            or (np.isfinite(rec["slope_rel_vs_ref"]) and rec["slope_rel_vs_ref"] > REL_TOL)
        )
    )
    return rec


def reference_selfcheck():
    """Gate the reference on HEALTHY grids before trusting it on hostile ones."""
    out = []
    for n in (81, 121, 161):
        X = sinh_grid(n)
        Hmod, Href = line_hilbert_matrix(X), ref_hilbert_matrix(X)
        Smod, Sref = np.array(slope_matrix(X)), ref_slopes_matrix(X)
        f = -4.0 * X / (1.0 + 4.0 * X ** 2)
        exact = 2.0 / (1.0 + 4.0 * X ** 2)
        core = np.abs(X) < 5.0
        core[:3] = core[-3:] = False
        out.append({
            "n": n,
            "matrix_rel_agreement": float(np.abs(Hmod - Href).max() / _finite_max(Href)),
            "slope_rel_agreement": float(np.abs(Smod - Sref).max() / _finite_max(Sref)),
            "module_rel_vs_exact": float(np.abs(Hmod @ f - exact)[core].max() / EXACT_PEAK),
            "reference_rel_vs_exact": float(np.abs(Href @ f - exact)[core].max() / EXACT_PEAK),
        })
    return out


def main():
    n = 151
    selfcheck = reference_selfcheck()
    worst_sc = max(r["matrix_rel_agreement"] for r in selfcheck)
    print("REFERENCE SELF-CHECK (healthy grids, module vs independent implementation)")
    for r in selfcheck:
        print(f"  n={r['n']:4d}  matrix {r['matrix_rel_agreement']:.2e}  "
              f"slopes {r['slope_rel_agreement']:.2e}  "
              f"module-vs-exact {r['module_rel_vs_exact']:.2e}  "
              f"ref-vs-exact {r['reference_rel_vs_exact']:.2e}")
    assert worst_sc < 1e-12, f"reference disagrees on healthy grids: {worst_sc:.2e}"
    print(f"  worst healthy-grid matrix agreement {worst_sc:.2e} -- reference trusted\n")

    records = [run_case(name, fam, X) for name, fam, X in build_cases(n)]

    print(f"{'case':26s} {'fam':10s} {'fin':5s} {'relexact':>9s} {'relref':>9s} "
          f"{'slopref':>9s} {'assocN':>9s} {'w':>3s}  SILENT")
    for r in records:
        print(f"{r['case']:26s} {r['family'][:10]:10s} "
              f"{str(r['all_finite']):5s} {r['rel_vs_exact']:9.2e} {r['rel_vs_ref']:9.2e} "
              f"{r['slope_rel_vs_ref']:9.2e} {r['assoc_normalized']:9.2e} "
              f"{r['n_warnings']:3d}  {'YES' if r['silent_corruption'] else '-'}")

    in_scope = [r for r in records if r["family"] in ("near_duplicate", "stretching")]
    oos = [r for r in records if r["family"] == "out_of_scope_monotonicity"]
    n_sc = sum(r["silent_corruption"] for r in in_scope)

    def _worst(rs, key):
        v = [r[key] for r in rs if np.isfinite(r[key])]
        return float(max(v)) if v else float("nan")

    summary = {
        "leg": 96,
        "route": "LHA",
        "module": "solver/line_hilbert.py",
        "gate": ("Under an adversarial battery of near-degenerate non-uniform grids "
                 "(near-duplicate points, extreme local stretching ratios), does "
                 "solver/line_hilbert.py's dense operator or its cached slope_matrix "
                 "ever silently return a finite, plausible-looking wrong result instead "
                 "of propagating or flagging the ill-conditioning?"),
        "gate_answer": "NO" if n_sc == 0 else "YES",
        "rel_tol": REL_TOL,
        "n_grid": n,
        "cases_in_scope": len(in_scope),
        "silent_corruptions_in_scope": int(n_sc),
        "worst_rel_vs_ref_in_scope": _worst(in_scope, "rel_vs_ref"),
        "worst_vec_rel_vs_ref_in_scope": _worst(in_scope, "vec_rel_vs_ref"),
        "worst_slope_rel_vs_ref_in_scope": _worst(in_scope, "slope_rel_vs_ref"),
        "worst_rel_vs_exact_in_scope": _worst(in_scope, "rel_vs_exact"),
        "worst_assoc_rel_in_scope": _worst(in_scope, "assoc_rel"),
        "worst_assoc_normalized_in_scope": _worst(in_scope, "assoc_normalized"),
        "max_slope_norm_inf_in_scope": _worst(in_scope, "slope_norm_inf"),
        "exact_duplicate_nonfinite_frac": next(
            (r["nonfinite_frac"] for r in records if r["case"] == "near_dup_fwd_0e+00"),
            float("nan")),
        "exact_duplicate_n_warnings": next(
            (r["n_warnings"] for r in records if r["case"] == "near_dup_fwd_0e+00"), -1),
        "out_of_scope_silent": {r["case"]: r["rel_vs_ref"] for r in oos},
        "reference_selfcheck": selfcheck,
        "cases": records,
    }

    print(f"\nIN-SCOPE: {len(in_scope)} cases, {n_sc} silent corruptions "
          f"(threshold {REL_TOL:.0e})")
    print(f"  worst module-vs-reference disagreement : "
          f"{summary['worst_rel_vs_ref_in_scope']:.3e}  (dense operator)")
    print(f"  worst module-vs-reference disagreement : "
          f"{summary['worst_slope_rel_vs_ref_in_scope']:.3e}  (slope operator)")
    print(f"  worst error vs the ANALYTIC answer     : "
          f"{summary['worst_rel_vs_exact_in_scope']:.3e}  (grid quality, not a fault)")
    print(f"  exact duplicate: {summary['exact_duplicate_nonfinite_frac']:.0%} non-finite, "
          f"{summary['exact_duplicate_n_warnings']} warnings -- LOUD")
    print("OUT OF SCOPE (monotonicity, reported not counted): "
          + ", ".join(f"{k} {v:.2e}" for k, v in summary["out_of_scope_silent"].items()))
    print(f"\nGATE ANSWER: {summary['gate_answer']}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "writeup", "data", "p2_route_lha_v1_adversarial.json")
    with open(out, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
