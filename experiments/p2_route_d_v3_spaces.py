"""P2 Route-D v3 -- THE SPACE-PAIR SCOPING LEG.

Route-D v2 (experiments/p2_route_d_dress.py, fig20) ended with a constructive
suggestion: the gauged finite-section inverse A loses exactly one power of decay,
so GRADE THE CODOMAIN by one mode power and ||A|| goes flat at 3.000 -- "the
asymmetric space pair a working certificate must use".  The continuation note
attached a condition to that suggestion, and this probe discharges it:

    the quadratic term D^2F[h,h] = 2 h H(h) must ALSO land in the graded
    codomain; do this on paper first, and if no consistent pair exists, that is
    itself the answer and the leg stops cheaply.

It does not exist -- in the weighted-ell^1 category.  And the same measurements
show what does: a DECAY-graded pair, which is not a weighted-ell^1 pair at all.
Both halves are measured here, each against an independent oracle.

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Every number is a property of the fixed anchor and the fixed operators.
Run:

    .venv/bin/python experiments/p2_route_d_v3_spaces.py
    -> writeup/data/p2_route_d_v3_spaces.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v3_evidence.py     (fig21)

SIX measurements.

  S1  THE EXACT QUADRATIC.  Q(h) = h H(h) is a PURE CONVOLUTION,
      q_m = (1/2) sum_{j+k=m} h_j h_k -- no difference frequencies (h + iH(h) is a
      Hardy boundary value and 2hH(h) = Im of its square).  Checked against the
      independent sum/difference build in solver/nk_fourier.  Consequence: the
      sharp weighted bound constant is S = sup_{j,k} v_{j+k}/(u_j u_k), which is
      also 2x better than the Wiener-algebra constant v2 used.

  S2  WHAT THE INVERSE NEEDS.  The mode-by-mode geometry of A: where the mass of
      A e_m actually sits, and the MINIMAL admissible codomain weight
      v_m^min(u) = ||A e_m||_{ell^1_u}.  Reported as the ratio v_m^min/(m u_m),
      i.e. "is one mode power really what the inverse costs, for weighted u too?"

  S3  THE (s,t) MAP (the money measurement).  For u_k = (1+k)^s, v_m = (1+m)^t,
      sweep the plane and measure BOTH requirements:
        region I  (A bounded)      : growth exponent of ||A_N||_{Y->X} in N
        region II (quadratic bounded): growth exponent of S_K in K
      Region I turns out to need t >= s+1 and region II t <= s.  They are
      DISJOINT, by exactly the one power the far field loses.  No weighted-ell^1
      pair certifies -- and the reason is not the truncation, the gauge, or the
      arithmetic.

  S4  THE CONTROL.  Redo S3 for the v2 surrogate operator, transport symbol
      (1 + cos theta) -> 1, changing nothing else.  If the gap closes (region I
      drops to t >= s, so the two regions touch at t = s and the unweighted
      ell^1 pair is admissible), then the obstruction is the far-field
      degeneracy, not the method.  This is the D4 ablation, re-run on the
      space-pair question.

  S5  THE RESONANCE.  The far-field model L h = -c h_X - h/X between DECAY-graded
      sup norms: ||L^{-1}|| = 2/|alpha - 2|, measured against a discretization
      AND against the operator-side coefficient lim X^{a+1} DF[f_a] = c a - 1.
      The pole at alpha = 2 is not an accident: X^{-2} is both the homogeneous
      solution at c = 1/2 and the decay of the anchor Omega_2 = -1/(1+X^2).  The
      "one lost power" of v2 is this resonance seen at integer grading.

  S6  THE PAIR THAT WORKS, AND ITS PRICE.  In the decay-graded pair
      X = {|h| <~ X^{-a}}, Y = {|g| <~ X^{-a-1}} BOTH requirements hold at once:
      the far-field inverse costs 2/(2-a) and the quadratic GAINS one power,
      with constant (int f_a)/pi.  Their product is the Z2-analogue, and it has
      an INTERIOR OPTIMUM in a: the far-field factor wants a away from 2, the
      quadratic factor wants a away from 1.  Reported as a scoping estimate --
      leading-order far-field constants only, no compact-core contribution and
      nothing interval-enclosed.
"""

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.nk_fourier import (  # noqa: E402
    C_ANCHOR, anchor, jacobian, gauged_system, gauge_row, ell1_op_norm,
)
from solver.decay_grading import (  # noqa: E402
    quadratic_coeffs, algebra_constant, cos_power_coeffs, eval_sin_series,
    theta_of_X, cos_power_mass, farfield_inverse_norm, farfield_symbol_coefficient,
    farfield_inverse_norm_finite,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v3_spaces.json"

N_LADDER = [8, 16, 32, 64, 128, 256]
S_GRID = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
T_GRID = [-1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75,
          1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]
ALPHA_GRID = [1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9,
              2.1, 2.2, 2.4, 2.6, 3.0]


# ---------------------------------------------------------------------------
# operators
# ---------------------------------------------------------------------------


def jacobian_surrogate(a, c, M, n_cols):
    """DF with the transport factor (1 + cos theta) replaced by 1 (v2 D4)."""
    J = jacobian(a, 0.0, M=M, n_cols=n_cols)      # c=0 -> product terms only
    for k in range(1, n_cols):
        if k <= M:
            J[k - 1, k] += c * k
    return J


def inverse_at(N, gauge="origin", surrogate=False, c=C_ANCHOR):
    a = anchor(N)
    if surrogate:
        grad, _ = gauge_row(gauge, N)
        J = np.empty((N + 1, N + 1))
        J[0, :] = grad
        J[1:, :] = jacobian_surrogate(a, c, M=N, n_cols=N + 1)
    else:
        _, J = gauged_system(a, c, N, gauge=gauge)
    return np.linalg.inv(J)


def weights(s, t, N):
    """Domain weight on cosine modes 0..N; codomain weight on [gauge row, sin 1..N].

    The gauge row carries weight 1 in every pairing (it is a scalar normalization,
    not a mode), exactly as in the v2 D6 measurement.
    """
    u = (1.0 + np.arange(N + 1)) ** s
    v = np.ones(N + 1)
    v[1:] = (1.0 + np.arange(1, N + 1)) ** t
    return u, v


def op_norm(A, u, v):
    """||A||_{Y->X} = max over codomain slots of (weighted column sum)/v."""
    cols = (np.abs(A) * np.asarray(u)[:, None]).sum(axis=0)
    return float((cols / np.asarray(v)).max())


def power_fit(xs, ys):
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    m = xs >= xs[len(xs) // 2]
    if m.sum() < 3 or np.any(ys[m] <= 0):
        return float("nan")
    return float(np.polyfit(np.log(xs[m]), np.log(ys[m]), 1)[0])


# ---------------------------------------------------------------------------
# S1 / S2
# ---------------------------------------------------------------------------


def s1_quadratic_identity():
    from solver.nk_fourier import residual
    rng = np.random.default_rng(3)
    worst = 0.0
    for K in (1, 3, 6, 12):
        for _ in range(8):
            h = rng.standard_normal(K + 1)
            mine, theirs = quadratic_coeffs(h), residual(h, 0.0)
            n = min(mine.size, theirs.size)
            worst = max(worst, float(np.max(np.abs(mine[:n] - theirs[:n])))
                        / float(np.abs(h).sum()) ** 2)
    S_flat, M_lo, M_hi, _ = algebra_constant(np.ones(41), np.ones(80))
    return {
        "identity": "Q(h)_m = (1/2) sum_{j+k=m} h_j h_k   (no difference frequencies)",
        "max_disagreement_with_independent_build": worst,
        "sharp_constant_unweighted": M_hi,
        "wiener_constant_used_in_v2": 1.0,
        "improvement_factor": 1.0 / M_hi,
        "note": "sup_{j,k} v_{j+k}/(u_j u_k) = S gives M in [S/4, S/2]; unweighted "
                "S = 1 so M = 1/2, half the Wiener bound v2 used (which changes no "
                "v2 conclusion: its budget was identically zero).",
    }


def s2_inverse_geometry(N=256):
    A = inverse_at(N)
    col = np.abs(A)                                   # |A e_m| over domain modes k
    out = {"N": N, "modes": [], "note":
           "v_m^min(u) = ||A e_m||_{ell^1_u} is the SMALLEST codomain weight that "
           "keeps A bounded; the ratio to m*u_m tests the 'one mode power' claim "
           "for weighted u as well as flat u."}
    k = np.arange(N + 1)
    for s in (0.0, 0.5, 1.0, 2.0):
        u = (1.0 + k) ** s
        vmin = (col * u[:, None]).sum(axis=0)         # per codomain slot
        ms = [m for m in (2, 4, 8, 16, 32) if m <= N // 8]
        rat = [float(vmin[m] / (m * (1.0 + m) ** s)) for m in ms]
        centroid = [float((k * col[:, m]).sum() / col[:, m].sum()) for m in ms]
        mass_below_half = [float(col[:m // 2 + 1, m].sum() / col[:, m].sum())
                           for m in ms]
        out["modes"].append({
            "s": s, "m": ms, "vmin_over_m_u": rat,
            "mass_centroid_k": centroid,
            "fraction_of_mass_below_m_over_2": mass_below_half,
        })
    return out


# ---------------------------------------------------------------------------
# S3 / S4 -- the (s,t) map, true operator and surrogate control
# ---------------------------------------------------------------------------


def st_map(surrogate=False):
    invs = {N: inverse_at(N, surrogate=surrogate) for N in N_LADDER}
    exp_A = np.zeros((len(S_GRID), len(T_GRID)))
    val_A = np.zeros_like(exp_A)
    for i, s in enumerate(S_GRID):
        for j, t in enumerate(T_GRID):
            ys = []
            for N in N_LADDER:
                u, v = weights(s, t, N)
                ys.append(op_norm(invs[N], u, v))
            exp_A[i, j] = power_fit(N_LADDER, ys)
            val_A[i, j] = ys[-1]
    return exp_A.tolist(), val_A.tolist()


def algebra_map():
    """Growth exponent of the sharp quadratic constant S_K in the truncation K."""
    Ks = [32, 48, 64, 96, 128, 192, 256]
    exp_S = np.zeros((len(S_GRID), len(T_GRID)))
    val_S = np.zeros_like(exp_S)
    for i, s in enumerate(S_GRID):
        for j, t in enumerate(T_GRID):
            ys = []
            for K in Ks:
                u = (1.0 + np.arange(K + 1)) ** s
                v = (1.0 + np.arange(1, 2 * K + 1.0)) ** t
                ys.append(algebra_constant(u, v)[0])
            exp_S[i, j] = power_fit(Ks, ys)
            val_S[i, j] = ys[-1]
    return exp_S.tolist(), val_S.tolist(), Ks


def diagonal_checks(surrogate=False):
    """Grid-independent form of the two boundaries: evaluate ON the candidate lines.

    The coarse (s,t) scan can only locate a boundary to within its 0.25 step, so
    the claims "A needs t >= s+1" and "the quadratic needs t <= s" are pinned here
    by measuring the growth exponents exactly at t = s, t = s+1 and one step
    short of each.  A bounded requirement reads ~0; an unbounded one reads ~1.
    """
    invs = {N: inverse_at(N, surrogate=surrogate) for N in N_LADDER}
    Ks = [32, 48, 64, 96, 128, 192, 256]
    out = []
    for s in S_GRID:
        row = {"s": s}
        for tag, t in (("t=s-1", s - 1.0), ("t=s", s), ("t=s+0.75", s + 0.75),
                       ("t=s+1", s + 1.0)):
            ys = []
            for N in N_LADDER:
                u, v = weights(s, t, N)
                ys.append(op_norm(invs[N], u, v))
            row[f"A_exponent_{tag}"] = power_fit(N_LADDER, ys)
        for tag, t in (("t=s", s), ("t=s+0.25", s + 0.25)):
            ys = []
            for K in Ks:
                u = (1.0 + np.arange(K + 1)) ** s
                v = (1.0 + np.arange(1, 2 * K + 1.0)) ** t
                ys.append(algebra_constant(u, v)[0])
            row[f"algebra_exponent_{tag}"] = power_fit(Ks, ys)
        out.append(row)
    return out


def gap_sweep(s_values=(0.0, 1.0), gs=None):
    """Both exponents as functions of the GAP g = t - s alone.

    The (s,t) map shows both requirements depend only on t - s (to two decimals),
    which reduces the whole question to one variable: how many grading powers the
    codomain carries over the domain.  A bounded inverse needs g >= 1, a bounded
    quadratic needs g <= 0, and the surrogate needs only g >= 0.
    """
    gs = list(np.arange(-1.75, 1.501, 0.125)) if gs is None else list(gs)
    Ks = [32, 48, 64, 96, 128, 192, 256]
    invs = {N: inverse_at(N) for N in N_LADDER}
    sur = {N: inverse_at(N, surrogate=True) for N in N_LADDER}
    out = []
    for s in s_values:
        rec = {"s": s, "g": [float(g) for g in gs],
               "A_exponent": [], "A_surrogate_exponent": [], "algebra_exponent": []}
        for g in gs:
            t = s + g
            ysA, ysS = [], []
            for N in N_LADDER:
                u, v = weights(s, t, N)
                ysA.append(op_norm(invs[N], u, v))
                ysS.append(op_norm(sur[N], u, v))
            rec["A_exponent"].append(power_fit(N_LADDER, ysA))
            rec["A_surrogate_exponent"].append(power_fit(N_LADDER, ysS))
            ysQ = []
            for K in Ks:
                u = (1.0 + np.arange(K + 1)) ** s
                v = (1.0 + np.arange(1, 2 * K + 1.0)) ** t
                ysQ.append(algebra_constant(u, v)[0])
            rec["algebra_exponent"].append(power_fit(Ks, ysQ))
        # THE CONSERVATION LAW.  A certificate needs BOTH exponents to be 0.  For
        # the true operator their sum is >= 1 at every g (and exactly 1 on
        # 0 <= g <= 1): the one power the far field loses must be paid by one bound
        # or the other, and the grading only chooses WHICH.  For the surrogate the
        # sum touches 0.  This single number is the whole no-go.
        rec["exponent_sum"] = [a + b for a, b in
                               zip(rec["A_exponent"], rec["algebra_exponent"])]
        rec["exponent_sum_surrogate"] = [a + b for a, b in
                                         zip(rec["A_surrogate_exponent"],
                                             rec["algebra_exponent"])]
        rec["min_exponent_sum"] = float(min(rec["exponent_sum"]))
        rec["min_exponent_sum_surrogate"] = float(min(rec["exponent_sum_surrogate"]))
        out.append(rec)
    return out


def boundary_from_map(exp_map, tol=0.05):
    """For each s, the smallest t whose growth exponent is <= tol (else None)."""
    out = []
    for i, s in enumerate(S_GRID):
        hit = None
        for j, t in enumerate(T_GRID):
            if exp_map[i][j] <= tol:
                hit = t
                break
        out.append({"s": s, "t_min_bounded": hit})
    return out


def boundary_from_algebra(exp_map, tol=0.05):
    """For each s, the LARGEST t whose algebra exponent is <= tol (else None)."""
    out = []
    for i, s in enumerate(S_GRID):
        hit = None
        for j, t in enumerate(T_GRID):
            if exp_map[i][j] <= tol:
                hit = t
        out.append({"s": s, "t_max_algebra": hit})
    return out


# ---------------------------------------------------------------------------
# S5 / S6 -- the decay-graded pair
# ---------------------------------------------------------------------------


def s5_resonance():
    rows = []
    for alpha in ALPHA_GRID:
        got, want = farfield_inverse_norm(alpha, n=8001, Xmax=1e12)
        fin = farfield_inverse_norm_finite(alpha, Xmax=1e12)
        rows.append({"alpha": alpha, "inverse_norm_measured": got,
                     "inverse_norm_law_2_over_abs_alpha_minus_2": want,
                     "inverse_norm_law_finite_domain": fin,
                     "rel_err_vs_finite_domain_law": abs(got - fin) / fin,
                     "rel_err": abs(got - want) / want})
    # operator side, from the exact Fourier coefficients (no quadrature)
    K = 200000
    op = []
    X = np.array([3e3, 1e4])
    for alpha in (1.2, 1.4, 1.6, 1.8):
        a = cos_power_coeffs(alpha, K)
        f = (1.0 + X ** 2) ** (-0.5 * alpha)
        fX = -alpha * X * (1.0 + X ** 2) ** (-0.5 * alpha - 1.0)
        Hf = eval_sin_series(a, theta_of_X(X))
        Om, HOm = -1.0 / (1.0 + X ** 2), -X / (1.0 + X ** 2)
        DF = f * HOm + Om * Hf - C_ANCHOR * fX
        got = float((X ** (alpha + 1.0) * DF
                     + (cos_power_mass(alpha) / math.pi) * X ** (alpha - 2.0))[-1])
        op.append({"alpha": alpha, "leading_coeff_measured": got,
                   "leading_coeff_law_c_alpha_minus_1":
                       farfield_symbol_coefficient(alpha, C_ANCHOR)})
    return {"inverse_side": rows, "operator_side": op,
            "resonance_alpha": 2.0,
            "why": "X^{-1/c} = X^{-2} at c=1/2 is BOTH the homogeneous far-field "
                   "solution and the decay of the anchor Omega_2 = -1/(1+X^2); the "
                   "space boundary sits exactly on the kernel."}


def s6_decay_pair():
    """Both requirements in the decay pair, and the resulting design curve in alpha."""
    K = 200000
    rows = []
    Xs = np.array([1e3, 2e3, 5e3, 1e4])
    for alpha in [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]:
        a = cos_power_coeffs(alpha, K)
        f = (1.0 + Xs ** 2) ** (-0.5 * alpha)
        Hf = eval_sin_series(a, theta_of_X(Xs))
        got = Xs ** (alpha + 1.0) * f * Hf
        A = np.column_stack([np.ones_like(Xs), Xs ** (1.0 - alpha)])
        CQ_meas = float(np.linalg.lstsq(A, got, rcond=None)[0][0])
        CQ_law = cos_power_mass(alpha) / math.pi
        Afar, Afar_law = farfield_inverse_norm(alpha, n=8001, Xmax=1e12)
        rows.append({
            "alpha": alpha,
            "quadratic_gain_constant_measured": CQ_meas,
            "quadratic_gain_constant_law": CQ_law,
            "farfield_inverse_norm": Afar,
            # Z2-analogue with the same 2||A||M convention as v2/S1:
            "Z2_scoping_estimate": 2.0 * Afar * CQ_meas,
            "budget_scoping_estimate": 1.0 / (4.0 * 2.0 * Afar * CQ_meas),
        })
    best = max(rows, key=lambda r: r["budget_scoping_estimate"])
    # closed-form optimum of (2-a)/m0(a):  m0 ~ 2/(a-1) near 1, so the product
    # (2-a)(a-1) peaks at a = 3/2; report the measured argmax on a fine grid too
    fine = np.linspace(1.02, 1.98, 193)
    score = [(2.0 - al) * math.pi / (4.0 * 2.0 * 2.0 * cos_power_mass(al))
             for al in fine]
    return {
        "rows": rows,
        "argmax_alpha_measured": best["alpha"],
        "argmax_alpha_closed_form": float(fine[int(np.argmax(score))]),
        "caveat": "SCOPING ESTIMATE ONLY: leading-order far-field constants, no "
                  "compact-core contribution, plain float64, nothing "
                  "interval-enclosed. It sizes the next brick; it certifies nothing.",
    }


# ---------------------------------------------------------------------------


def main():
    s1 = s1_quadratic_identity()
    s2 = s2_inverse_geometry()

    expA, valA = st_map(surrogate=False)
    expA_sur, valA_sur = st_map(surrogate=True)
    expS, valS, Ks = algebra_map()

    bI = boundary_from_map(expA)
    bI_sur = boundary_from_map(expA_sur)
    bII = boundary_from_algebra(expS)

    gapsw = gap_sweep()
    diag = diagonal_checks(surrogate=False)
    diag_sur = diagonal_checks(surrogate=True)

    gaps = [b["t_min_bounded"] - b["s"] for b in bI if b["t_min_bounded"] is not None]
    gaps_sur = [b["t_min_bounded"] - b["s"] for b in bI_sur if b["t_min_bounded"] is not None]
    over = [(a["s"], a["t_min_bounded"], b["t_max_algebra"])
            for a, b in zip(bI, bII)
            if a["t_min_bounded"] is not None and b["t_max_algebra"] is not None
            and a["t_min_bounded"] <= b["t_max_algebra"]]
    over_sur = [(a["s"], a["t_min_bounded"], b["t_max_algebra"])
                for a, b in zip(bI_sur, bII)
                if a["t_min_bounded"] is not None and b["t_max_algebra"] is not None
                and a["t_min_bounded"] <= b["t_max_algebra"]]

    data = {
        "meta": {
            "leg": "P2 Route-D v3 (space-pair scoping: does the graded pair of v2 D6 "
                   "carry a certificate?)",
            "tier": "Level-1 tooling + a NO-GO theorem with its numerical face "
                    "(NOT a certificate)",
            "anchor": "Omega_2 = -(1+cos theta)/2 (= -1/(1+X^2)), c_tw = 1/2, a = 0",
            "gauge": "c fixed at 1/2 + one scalar normalization (Route-D v1 Q2)",
            "reproduce": "python experiments/p2_route_d_v3_spaces.py",
            "arithmetic": "plain float64 -- nothing here is interval-enclosed and "
                          "nothing here is claimed as rigorous",
            "headline": "In the weighted-ell^1 category the two NK requirements are "
                        "DISJOINT by exactly one grading power: a bounded inverse "
                        "needs t >= s+1, a bounded quadratic needs t <= s. The "
                        "repair v2 proposed cannot be implemented with diagonal "
                        "weights. The decay-graded pair (not a weighted-ell^1 pair) "
                        "satisfies both, at a cost 2/(2-alpha) with an interior "
                        "optimum near alpha = 3/2.",
        },
        "s1_quadratic_identity": s1,
        "s2_inverse_geometry": s2,
        "s3_st_map": {
            "s_grid": S_GRID, "t_grid": T_GRID, "N_ladder": N_LADDER,
            "K_ladder_algebra": Ks,
            "growth_exponent_A": expA, "A_at_N_max": valA,
            "growth_exponent_algebra": expS, "algebra_at_K_max": valS,
            "region_I_boundary": bI, "region_II_boundary": bII,
            "overlap": over,
            "gap_in_t": sorted(set(round(g, 3) for g in gaps)),
            "diagonal_checks": diag,
            "gap_sweep": gapsw,
        },
        "s4_surrogate_control": {
            "growth_exponent_A": expA_sur, "A_at_N_max": valA_sur,
            "region_I_boundary": bI_sur,
            "overlap": over_sur,
            "gap_in_t": sorted(set(round(g, 3) for g in gaps_sur)),
            "diagonal_checks": diag_sur,
        },
        "s5_resonance": s5_resonance(),
        "s6_decay_pair": s6_decay_pair(),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    # ---- console summary ----------------------------------------------------
    print("S1 Q(h) = h H(h) is a pure convolution; independent builds agree to "
          f"{s1['max_disagreement_with_independent_build']:.1e}")
    print(f"   sharp unweighted constant M = {s1['sharp_constant_unweighted']:.3f} "
          f"({s1['improvement_factor']:.0f}x better than the Wiener bound v2 used)")
    print("\nS2 what the inverse costs (v_m^min / (m u_m), should be O(1) if the "
          "price is exactly one mode power):")
    for row in s2["modes"]:
        print(f"   s={row['s']:.2f}: " + ", ".join(
            f"m={m}: {r:.2f}" for m, r in zip(row["m"], row["vmin_over_m_u"])))

    print("\nS3 the (s,t) map -- for u_k=(1+k)^s, v_m=(1+m)^t:")
    print("      s   t_min for bounded A   t_max for bounded quadratic   overlap?")
    for a, b in zip(bI, bII):
        tm = "none" if a["t_min_bounded"] is None else f"{a['t_min_bounded']:.2f}"
        tx = "none" if b["t_max_algebra"] is None else f"{b['t_max_algebra']:.2f}"
        ok = (a["t_min_bounded"] is not None and b["t_max_algebra"] is not None
              and a["t_min_bounded"] <= b["t_max_algebra"])
        print(f"   {a['s']:>4.2f}   {tm:>18}   {tx:>27}   {'YES' if ok else 'no'}")
    print(f"   -> the two requirements are disjoint; gap in t = "
          f"{data['s3_st_map']['gap_in_t']}; overlap at {len(over)} of "
          f"{len(S_GRID)} values of s")
    print("   grid-independent check (growth exponent; ~0 = bounded, ~1 = not):")
    print("      s  ||A|| at t=s-1   t=s  t=s+0.75  t=s+1  | algebra at t=s  t=s+0.25")
    for r in diag:
        print(f"   {r['s']:>4.2f}  {r['A_exponent_t=s-1']:>12.2f} "
              f"{r['A_exponent_t=s']:>5.2f} "
              f"{r['A_exponent_t=s+0.75']:>9.2f} {r['A_exponent_t=s+1']:>6.2f}  |"
              f"{r['algebra_exponent_t=s']:>13.2f} {r['algebra_exponent_t=s+0.25']:>10.2f}")

    gz = gapsw[0]
    print("   collapse onto the gap g = t - s (s=0):")
    print("      g:  " + " ".join(f"{g:>6.3f}" for g in gz["g"][::2]))
    print("   ||A||:  " + " ".join(f"{e:>6.2f}" for e in gz["A_exponent"][::2]))
    print("   quad :  " + " ".join(f"{e:>6.2f}" for e in gz["algebra_exponent"][::2]))
    print("   surr :  " + " ".join(f"{e:>6.2f}" for e in gz["A_surrogate_exponent"][::2]))
    print("   SUM  :  " + " ".join(f"{e:>6.2f}" for e in gz["exponent_sum"][::2]))
    print(f"   -> a certificate needs BOTH exponents 0, i.e. sum 0; the measured "
          f"minimum over the whole family is {gz['min_exponent_sum']:.2f} "
          f"(surrogate: {gz['min_exponent_sum_surrogate']:.2f})")

    print("\nS4 CONTROL (transport symbol 1+cos -> 1, nothing else changed):")
    print(f"   gap in t = {data['s4_surrogate_control']['gap_in_t']}; "
          f"overlap at {len(over_sur)} of {len(S_GRID)} values of s")
    print("      s  ||A|| at t=s-1   t=s  t=s+0.75  t=s+1")
    for r in diag_sur:
        print(f"   {r['s']:>4.2f}  {r['A_exponent_t=s-1']:>12.2f} "
              f"{r['A_exponent_t=s']:>5.2f} "
              f"{r['A_exponent_t=s+0.75']:>9.2f} {r['A_exponent_t=s+1']:>6.2f}")
    print("   -> the gap is caused by the far-field degeneracy, not by the method")

    print("\nS5 the far-field resonance at alpha = 2 (X^-2 = homogeneous solution "
          "= anchor decay):")
    for r in data["s5_resonance"]["inverse_side"][:4] + data["s5_resonance"]["inverse_side"][-2:]:
        print(f"   alpha={r['alpha']:.2f}: ||L^-1|| = "
              f"{r['inverse_norm_measured']:8.3f}  vs law 2/|a-2| = "
              f"{r['inverse_norm_law_2_over_abs_alpha_minus_2']:8.3f} "
              f"(finite-domain exact: {100 * r['rel_err_vs_finite_domain_law']:.3f}%)")

    print("\nS6 the decay-graded pair -- BOTH requirements hold; the price in alpha:")
    for r in data["s6_decay_pair"]["rows"]:
        print(f"   alpha={r['alpha']:.2f}: ||A_far||={r['farfield_inverse_norm']:7.3f}  "
              f"C_quad={r['quadratic_gain_constant_measured']:7.3f}  "
              f"Z2~{r['Z2_scoping_estimate']:8.3f}  budget~"
              f"{r['budget_scoping_estimate']:.4f}")
    print(f"   interior optimum: alpha ~ {data['s6_decay_pair']['argmax_alpha_measured']:.2f} "
          f"(grid) / {data['s6_decay_pair']['argmax_alpha_closed_form']:.3f} (closed form)"
          f"  -- profiles decaying like X^-3/2, residual measured in X^-5/2")
    print(f"[done] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
