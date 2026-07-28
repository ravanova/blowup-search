"""P2 Route-D v2 -- the FLOAT DRESS REHEARSAL of the Newton-Kantorovich bounds.

The brick Route-D v1 (experiments/p2_route_d_probe.py, fig19) said was next: build
the linearized operator DF at the exact a=0 anchor as a finite (N+1)-mode matrix in
PLAIN FLOATING POINT, gauge it, invert the finite section, and compute the
radii-polynomial bounds Y0, Z0, Z1, Z2 across an N-ladder.  The one question that
gates the whole Route-D programme:

    does  Z0 + Z1 < 1,  and does the certification ball CLOSE at the anchor?

Answering it in float costs seconds; only if it closes with margin is it worth
hardening every bound with the interval core (solver/interval.py).

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock) -- every number is a property of the fixed anchor and the fixed operators.
Committed so the writeup rebuilds without re-derivation.  Run:

    .venv/bin/python experiments/p2_route_d_dress.py
    -> writeup/data/p2_route_d_dress.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_dress_evidence.py   (fig20)

FIVE measurements:

  D1  N-LADDER of the gauged finite section.  sigma_min, condition number and --
      the quantity NK actually needs -- the induced ell^1 norm ||A_N|| of the
      finite-section inverse.  If ||A_N|| saturates, the operator is boundedly
      invertible in this space and NK has a chance; if it GROWS, it is not, and no
      truncation will ever certify.

  D2  RADII POLYNOMIAL at each N: Y0 (the defect -- exactly 0 at the anchor, so we
      also report the CERTIFICATION BUDGET Y0_max = (1-Z0-Z1)^2/(4 Z2), the largest
      defect these bounds could tolerate), Z0, Z1 (finite + far-field parts), Z2.
      Y0_max is what decides whether an a != 0 profile, whose residual floor is
      ~1e-2, could ever be certified this way.

  D3  GAUGE SENSITIVITY.  Repeat D1 for three different scalar normalizations
      (origin / a0 / a1).  Open sub-task G asked whether the gauge choice is what
      blocks closure; if all three ladders behave identically, G is exonerated.

  D4  CAUSAL ISOLATION.  Rebuild the ladder with the transport factor
      (1 + cos theta) replaced by 1 (a non-degenerate surrogate transport, all
      other terms untouched).  If the surrogate saturates where the true operator
      grows, the far-field degeneracy at theta = +-pi (X = infinity) is PROVEN to
      be the cause, not merely the suspect.

  D5  FAR-FIELD ALGEBRA.  The exact Z1 column weight vs mode, under both tail
      diagonal models, and the weighted-ell^1 repair attempt -- showing the
      marginality is structural and no weight removes it.

  D6  THE DECAY-GRADED REPAIR (the constructive half).  Measure the mode-by-mode
      amplification ||A e_m||_1 of the finite-section inverse, and then re-measure
      ||A|| between ASYMMETRIC spaces whose norms differ by one mode power.  If
      the inverse loses exactly one power of decay -- the prediction from the
      far-field ODE -c h_X - h/X = g -- then ||A e_m||_1 grows like m and
      ||A||_{Y -> X} SATURATES when the codomain Y carries the extra power.  That
      identifies the functional setting a working certificate must use.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.nk_fourier import (  # noqa: E402
    C_ANCHOR, anchor, residual, jacobian, gauged_system, gauge_row,
    ell1_op_norm, radii_polynomial, tail_Z1_column, tail_weight_obstruction,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_dress.json"

N_LADDER = [4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256]


# ---------------------------------------------------------------------------
# the surrogate operator used for the causal-isolation test (D4)
# ---------------------------------------------------------------------------


def jacobian_surrogate(a, c, M, n_cols):
    """DF with the transport factor (1 + cos theta) replaced by 1.

    i.e. the transport term becomes -c h_theta instead of -c (1 + cos theta)
    h_theta, so mode k feeds ONLY sin(k) with weight c k.  Everything else (the
    two Hilbert/product terms) is untouched.  This is not a physical operator --
    it is a controlled surrogate that removes exactly one feature, the vanishing
    of the transport symbol at theta = +-pi, so that its effect can be isolated.
    """
    J = jacobian(a, 0.0, M=M, n_cols=n_cols)      # c=0 -> product terms only
    for k in range(1, n_cols):
        if k <= M:
            J[k - 1, k] += c * k                  # plain diagonal transport
    return J


def gauged_system_surrogate(a, c, N, gauge="origin"):
    grad, target = gauge_row(gauge, N)
    J = np.empty((N + 1, N + 1))
    J[0, :] = grad
    J[1:, :] = jacobian_surrogate(a, c, M=N, n_cols=N + 1)
    return J


# ---------------------------------------------------------------------------
# D1 / D2 -- the ladder and the radii polynomial
# ---------------------------------------------------------------------------


def far_field_Z1(N, c=C_ANCHOR):
    """sup_{k>N} of the exact far-field Z1 column weight, both tail models."""
    ks = np.arange(N + 1, max(N + 1, 20 * N) + 1)
    lo = max(tail_Z1_column(int(k), c, diag="transport") for k in ks)
    hi = max(tail_Z1_column(int(k), c, diag="exact") for k in ks)
    return float(lo), float(hi)


def ladder(gauge="origin", surrogate=False, c=C_ANCHOR):
    rows = []
    for N in N_LADDER:
        a = anchor(N)
        if surrogate:
            J = gauged_system_surrogate(a, c, N, gauge=gauge)
            G = np.zeros(N + 1)
            G[0] = float(np.dot(gauge_row(gauge, N)[0], a)) - gauge_row(gauge, N)[1]
        else:
            G, J = gauged_system(a, c, N, gauge=gauge)
        s = np.linalg.svd(J, compute_uv=False)
        A = np.linalg.inv(J)
        A_norm = ell1_op_norm(A)

        # --- NK bounds ---------------------------------------------------
        # Y0: the finite part ||A G|| plus the tail defect sum_{m>N} |b_m|/(c m).
        # At the exact anchor BOTH are 0 (the anchor is a degree-1 trig polynomial
        # and an exact zero), so Y0 is pure rounding -- which is the point: the
        # informative quantity is the BUDGET Y0_max, computed below.
        b_full = residual(a, c)                       # untruncated residual
        tail_defect = float(sum(abs(b_full[m - 1]) / (c * m)
                                for m in range(N + 1, b_full.size + 1)))
        Y0 = float(np.abs(A @ G).sum()) + tail_defect

        # Z0: finite-block consistency of the numerical inverse (rounding only).
        Z0 = ell1_op_norm(np.eye(N + 1) - A @ J)

        # Z1: finite rows fed by tail columns, + the far-field column weight.
        # columns k = N+1 .. 2N+2 restricted to rows m <= N (the FT block)
        n_extra = N + 2
        J_ext = jacobian(a, c, M=N, n_cols=N + 1 + n_extra)
        E_ft = np.zeros((N + 1, n_extra))
        E_ft[1:, :] = J_ext[:, N + 1:]
        Z1_ft = ell1_op_norm(A @ E_ft)
        Z1_tail_lo, Z1_tail_hi = far_field_Z1(N, c)
        Z1 = Z1_ft + Z1_tail_lo                      # the OPTIMISTIC tail model

        # Z2: F is quadratic; D2F[h,h] = 2 h H(h) and ||H h|| <= ||h|| in the
        # Wiener (ell^1 Fourier) algebra, so ||D2F|| <= 2 and Z2 = 2 ||A||.
        Z2 = 2.0 * A_norm

        rp = radii_polynomial(Y0, Z0, Z1, Z2)
        rp_nofar = radii_polynomial(Y0, Z0, Z1_ft, Z2)   # finite-section-only fiction
        rows.append({
            "N": N,
            "sigma_min": float(s[-1]), "sigma_max": float(s[0]),
            "cond": float(s[0] / s[-1]),
            "A_norm_ell1": A_norm,
            "Y0": Y0, "Z0": Z0,
            "Z1": Z1, "Z1_finite_tail_coupling": Z1_ft,
            "Z1_far_field_transport_model": Z1_tail_lo,
            "Z1_far_field_exact_model": Z1_tail_hi,
            "Z2": Z2,
            "one_minus_Z": rp["one_minus_Z"], "closes": rp["closes"],
            "Y0_max": rp["Y0_max"],
            "closes_if_far_field_ignored": rp_nofar["closes"],
            "Y0_max_if_far_field_ignored": rp_nofar["Y0_max"],
            "r_min_if_far_field_ignored": rp_nofar["r_min"],
        })
    return rows


def graded_norms(N, gauge="origin", c=C_ANCHOR):
    """D6: mode-by-mode amplification of A, and ||A|| in three space pairings.

    Codomain slots are [gauge row, sine modes 1..N]; the "graded" codomain weight
    puts v_m = m on sine mode m (and 1 on the gauge row), i.e. one extra power of
    the mode number -- equivalently, since Fourier mode m resolves the scale
    X ~ m under X = tan(theta/2), one extra power of X-DECAY.  The domain weight
    w_k = 1 + k is the same grading on the profile side.

      P1  ||A||: graded codomain -> plain ell^1 domain
      P2  ||A||: plain ell^1 codomain -> graded domain
      P3  ||A||: graded -> graded
    """
    a = anchor(N)
    _, J = gauged_system(a, c, N, gauge=gauge)
    A = np.linalg.inv(J)
    w_dom = 1.0 + np.arange(N + 1)
    v_cod = np.ones(N + 1)
    v_cod[1:] = np.arange(1, N + 1)
    col_flat = np.abs(A).sum(axis=0)              # ||A e_m||_1 per codomain slot
    col_graded = (np.abs(A) * w_dom[:, None]).sum(axis=0)
    return {
        "N": N,
        "P1_graded_cod_to_l1_dom": float((col_flat / v_cod).max()),
        "P2_l1_cod_to_graded_dom": float(col_graded.max()),
        "P3_graded_to_graded": float((col_graded / v_cod).max()),
        "col_l1": [float(x) for x in col_flat],
        # slope of ||A e_m||_1 vs m on the CLEAN interior window m <= N/8. The
        # profile rolls over as m -> N: that is a finite-section EDGE effect (the
        # last column is truncated, ||A e_N||_1 == 4 exactly at every N), not the
        # asymptotics, so fitting through it would understate the true slope.
        "amplification_slope": float(np.polyfit(
            np.arange(1, max(N // 8, 3) + 1),
            col_flat[1:max(N // 8, 3) + 1], 1)[0]),
        "amplification_window": [1, max(N // 8, 3)],
        "col_l1_last": float(col_flat[N]),
    }


def power_fit(N, y):
    """Least-squares slope of log y vs log N over the upper half of the ladder."""
    N = np.asarray(N, dtype=float)
    y = np.asarray(y, dtype=float)
    m = N >= N[len(N) // 2]
    if m.sum() < 3 or np.any(y[m] <= 0):
        return float("nan")
    p = np.polyfit(np.log(N[m]), np.log(y[m]), 1)
    return float(p[0])


def main():
    c = C_ANCHOR

    # D1 + D2 -----------------------------------------------------------------
    main_rows = ladder(gauge="origin")
    Ns = [r["N"] for r in main_rows]

    # D3 gauge sensitivity ----------------------------------------------------
    gauges = {}
    for g in ("origin", "a0", "a1"):
        rows = ladder(gauge=g)
        gauges[g] = {
            "A_norm_ell1": [r["A_norm_ell1"] for r in rows],
            "sigma_min": [r["sigma_min"] for r in rows],
            "growth_exponent_A_norm": power_fit(Ns, [r["A_norm_ell1"] for r in rows]),
        }

    # D4 causal isolation -----------------------------------------------------
    sur_rows = ladder(gauge="origin", surrogate=True)

    # D5 far-field algebra ----------------------------------------------------
    ks = [3, 4, 5, 10, 20, 50, 100, 300, 1000, 3000]
    far_field = {
        "k": ks,
        "z_transport_model": [tail_Z1_column(k, c, diag="transport") for k in ks],
        "z_exact_model": [tail_Z1_column(k, c, diag="exact") for k in ks],
    }
    weights = {}
    for name, w in (("w=k^0.5", lambda k: k ** 0.5),
                    ("w=k (flat u)", lambda k: float(k)),
                    ("w=k(1+k) (affine u)", lambda k: k * (1.0 + k)),
                    ("w=k^1.5", lambda k: k ** 1.5),
                    ("w=1.05^k", lambda k: 1.05 ** k)):
        sup, _, _ = tail_weight_obstruction(w, 5, 2000, c)
        weights[name] = float(sup)

    # D6 decay-graded repair ---------------------------------------------------
    graded = [graded_norms(N) for N in N_LADDER]

    data = {
        "meta": {
            "leg": "P2 Route-D v2 (float dress rehearsal of the NK bounds)",
            "tier": "Level-1 tooling + a NEGATIVE structural result (NOT a certificate)",
            "anchor": "Omega_2 = -(1+cos theta)/2 (= -1/(1+X^2)), c_tw = 1/2, a = 0",
            "space": "unweighted ell^1 (Wiener) cosine coefficients (+) R for c",
            "gauge": "c fixed at 1/2 + one scalar normalization (Route-D v1 Q2)",
            "reproduce": "python experiments/p2_route_d_dress.py",
            "arithmetic": "plain float64 -- a DRESS REHEARSAL; nothing here is "
                          "interval-enclosed, and nothing here is claimed as rigorous",
        },
        "d1_d2_ladder": main_rows,
        "d1_growth_exponents": {
            "A_norm_ell1": power_fit(Ns, [r["A_norm_ell1"] for r in main_rows]),
            "cond": power_fit(Ns, [r["cond"] for r in main_rows]),
            "sigma_min": power_fit(Ns, [r["sigma_min"] for r in main_rows]),
        },
        "d3_gauge_sensitivity": gauges,
        "d4_surrogate_ladder": sur_rows,
        "d4_growth_exponents": {
            "A_norm_ell1": power_fit(Ns, [r["A_norm_ell1"] for r in sur_rows]),
            "sigma_min": power_fit(Ns, [r["sigma_min"] for r in sur_rows]),
        },
        "d5_far_field": far_field,
        "d5_weight_repair": weights,
        "d6_graded": graded,
        "d6_growth_exponents": {
            "P1_graded_cod_to_l1_dom": power_fit(
                Ns, [g["P1_graded_cod_to_l1_dom"] for g in graded]),
            "P2_l1_cod_to_graded_dom": power_fit(
                Ns, [g["P2_l1_cod_to_graded_dom"] for g in graded]),
            "P3_graded_to_graded": power_fit(
                Ns, [g["P3_graded_to_graded"] for g in graded]),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    # ---- console summary ----------------------------------------------------
    print(f"{'N':>5} {'sigma_min':>11} {'cond':>11} {'||A||_1':>11} "
          f"{'Z1_ft':>10} {'Z1':>8} {'1-Z':>9} {'Y0_max':>10} closes")
    for r in main_rows:
        print(f"{r['N']:>5} {r['sigma_min']:>11.3e} {r['cond']:>11.3e} "
              f"{r['A_norm_ell1']:>11.3e} {r['Z1_finite_tail_coupling']:>10.3e} "
              f"{r['Z1']:>8.4f} {r['one_minus_Z']:>9.2e} {r['Y0_max']:>10.3e} "
              f"{'YES' if r['closes'] else 'no'}")
    ge = data["d1_growth_exponents"]
    print(f"\nD1 growth exponents (upper half of ladder): "
          f"||A||_1 ~ N^{ge['A_norm_ell1']:.2f}, cond ~ N^{ge['cond']:.2f}, "
          f"sigma_min ~ N^{ge['sigma_min']:.2f}")
    print("D3 gauge sensitivity (||A||_1 exponent): "
          + ", ".join(f"{g}: N^{v['growth_exponent_A_norm']:.2f}"
                      for g, v in gauges.items()))
    gs = data["d4_growth_exponents"]
    print(f"D4 SURROGATE (transport symbol 1+cos -> 1): ||A||_1 ~ N^"
          f"{gs['A_norm_ell1']:.2f}   [true operator: N^{ge['A_norm_ell1']:.2f}]")
    print(f"    surrogate ||A||_1 at N={sur_rows[-1]['N']}: "
          f"{sur_rows[-1]['A_norm_ell1']:.3e}  vs true "
          f"{main_rows[-1]['A_norm_ell1']:.3e}")
    trio = list(zip(ks, far_field["z_transport_model"],
                    far_field["z_exact_model"]))[-3:]
    print("D5 far-field Z1 column weight -> 1 (both tail models): "
          + ", ".join(f"k={k}: [{lo:.4f}, {hi:.4f}]" for k, lo, hi in trio))
    print("D5 weighted repair attempts (sup z_w, need < 1): "
          + ", ".join(f"{k}: {v:.6f}" for k, v in weights.items()))
    g6 = data["d6_growth_exponents"]
    print(f"\nD6 decay-graded pairings (||A||, exponent over the upper ladder):")
    print(f"    P1 graded codomain -> l1 domain : "
          f"{graded[-1]['P1_graded_cod_to_l1_dom']:.4f} at N={graded[-1]['N']}"
          f"   ~ N^{g6['P1_graded_cod_to_l1_dom']:.2f}   <-- SATURATES")
    print(f"    P2 l1 codomain -> graded domain : "
          f"{graded[-1]['P2_l1_cod_to_graded_dom']:.4f}"
          f"   ~ N^{g6['P2_l1_cod_to_graded_dom']:.2f}")
    print(f"    P3 graded -> graded             : "
          f"{graded[-1]['P3_graded_to_graded']:.4f}"
          f"   ~ N^{g6['P3_graded_to_graded']:.2f}")
    print(f"    mode amplification ||A e_m||_1 ~ {graded[-1]['amplification_slope']:.3f} m "
          f"(one lost power of X-decay; mode m resolves X ~ m)")
    print(f"[done] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
