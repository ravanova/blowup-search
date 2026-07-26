"""P2 Route-D v1 -- interval-arithmetic core + a=0 operator-framing SCOPING PROBE.

This is the FIRST Level-2 (rigorous / computer-assisted) brick of the project: a
hand-rolled interval-arithmetic core (solver/interval.py) plus the deterministic
a=0 measurements that decide HOW a Newton-Kantorovich certification of the gCLM
two-scale traveling wave should be set up. It makes NO certificate claim -- it is
validated tooling + a scoping result (the Route-D "guess -> can it be certified?"
framing), and Clay odds are unchanged.

NOT a logged Tier-1/2 experiment: every number here is a DETERMINISTIC property of
the a=0 anchor and the fixed operators (no GA, no seeds, no predicate lock). It is
committed so the writeup rebuilds without re-derivation. Run:
    .venv/bin/python experiments/p2_route_d_probe.py
    -> writes writeup/data/p2_route_d_probe.json ; figure via
       .venv/bin/python writeup/p2_route_d_evidence.py   (fig19)

Three measurements (see writeup/TECHNICAL_P2_ROUTED.md for the framing):

  Q1  ARITHMETIC PRECISION. Rigorously enclose the two-scale residual
      R2(Omega) = Omega H(Omega) - c_tw Omega_X at the exact a=0 anchor
      Omega_2 = -1/(1+X^2), c_tw = 1/2, with the interval core. The enclosure
      width vs the ~1e-9 defect is the arithmetic OVERHEAD -- it must be << the
      defect for the interval layer to carry a Newton-Kantorovich defect bound
      Y0. Plus a genome-box sweep (how the enclosure grows over a parameter box).

  Q2  DEGENERACY COUNT. The a=0 zero set is a 2-parameter scaling valley
      {A/(1+B X^2)}, so the linearized operator is SINGULAR -- a gauge quotient
      is not optional. Singular values of the finite genome map's Jacobian, both
      with c_tw SLAVED to the projection and with c_tw FIXED = 1/2, COUNT the
      kernel: 2 (both directions) -> 1 (one direction) as the speed gauge is
      added. Tells us exactly how many gauge conditions isolate a nondegenerate
      zero.

  Q3  DIAGONALIZATION. Under the tangent map X = tan(theta/2) the LINE Hilbert
      transform equals the CIRCULAR conjugate-function operator (cos k*theta ->
      sin k*theta). Verified on the decaying subspace for k = 1..6; this is the
      structural fact that makes the anchor a 2-term Fourier object and the
      linearized operator banded + rank-1 -- the reason Z0 + Z1 < 1 is plausible.
"""

import json
from pathlib import Path

import numpy as np

from solver.gclm_family import (
    GCLMResidual, clm_two_scale, even_lorentz, _drho_centered4,
)
from solver.interval import Interval, matvec

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_probe.json"


def build_derivative_matrix(n, drho):
    """Point matrix D with Omega_rho = D @ Omega (the 4th-order centered stencil)."""
    D = np.zeros((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = 1.0
        D[:, j] = _drho_centered4(e, drho)
    return D


def q1_arithmetic_precision(R, D, c_tw=0.5):
    """Enclose R2 at the exact anchor + a genome-box sweep."""
    X, Xr = R.X, R.X_rho
    Om = clm_two_scale(X)
    HOm = R.Hmat @ Om
    Om_X = (D @ Om) / Xr
    R2_float = Om * HOm - c_tw * Om_X
    defect_inf = float(np.abs(R2_float).max())
    defect_rms = float(np.sqrt(np.mean(R2_float ** 2)))

    # rigorous interval enclosure at the point anchor
    Om_iv = Interval.point(Om)
    HOm_iv = matvec(R.Hmat, Om_iv)
    OmX_iv = matvec(D, Om_iv) * Interval.point(1.0 / Xr)
    R2_iv = Om_iv * HOm_iv - Interval.point(c_tw) * OmX_iv
    encl_sup = float(R2_iv.mag().max())
    encl_width = float(R2_iv.width.max())

    # enclosure over a genome box p=(A,B) around the anchor (-1, 1)
    p0 = (-1.0, 1.0)
    box = []
    for r in (1e-6, 1e-4, 1e-2):
        A_iv = Interval.from_mid_rad(p0[0], r)
        B_iv = Interval.from_mid_rad(p0[1], r)
        denom = Interval.point(1.0) + B_iv * Interval.point(X * X)
        Om_box = A_iv * denom.reciprocal()
        HOm_box = matvec(R.Hmat, Om_box)
        OmX_box = matvec(D, Om_box) * Interval.point(1.0 / Xr)
        R2_box = Om_box * HOm_box - Interval.point(c_tw) * OmX_box
        box.append({"radius": r, "sup_R2_over_box": float(R2_box.mag().max())})

    return {
        "defect_inf": defect_inf,
        "defect_rms": defect_rms,
        "enclosure_sup": encl_sup,
        "enclosure_width": encl_width,
        "overhead_ratio": encl_width / max(defect_inf, 1e-300),
        "genome_box": box,
    }


def q2_degeneracy(R, D):
    """Singular values of the finite genome map Jacobian: gauge-slaved vs fixed c."""
    X, Xr = R.X, R.X_rho
    p0 = np.array([-1.0, 1.0])

    def R2_of_p(p, fixed_ctw):
        Om = even_lorentz(X, p)
        HOm = R.Hmat @ Om
        OmX = (D @ Om) / Xr
        stretch = Om * HOm
        c = fixed_ctw if fixed_ctw is not None else float(
            np.dot(stretch, OmX) / np.dot(OmX, OmX))
        return stretch - c * OmX

    def jac(fixed_ctw, h=1e-6):
        base = R2_of_p(p0, fixed_ctw)
        J = np.zeros((base.size, 2))
        for k in range(2):
            pp = p0.copy()
            pp[k] += h
            J[:, k] = (R2_of_p(pp, fixed_ctw) - base) / h
        return J

    svals = {}
    for label, fc in (("gauge_slaved", None), ("fixed_ctw_half", 0.5)):
        svals[label] = np.linalg.svd(jac(fc), compute_uv=False)
    # classify kernel directions against a SHARED O(1) operator scale (the
    # dominant singular value across both linearizations) -- a direction whose
    # sigma is tiny relative to that scale is a symmetry (valley tangent).
    ref = float(max(svals["gauge_slaved"].max(), svals["fixed_ctw_half"].max()))
    out = {"reference_scale": ref}
    for label, s in svals.items():
        out[label] = {
            "sigma": [float(v) for v in s],
            "ratio": float(s[0] / max(s[1], 1e-300)),
            "kernel_dim": int(np.sum(s < 1e-4 * ref)),
        }
    return out


def q3_diagonalization(R):
    """Circular-Hilbert covariance of the line Hilbert transform under X=tan(th/2)."""
    X, H = R.X, R.Hmat
    theta = 2.0 * np.arctan(X)
    m = np.abs(X) < 20.0                       # resolved bulk

    def rel_err(ks, cs):
        f = sum(c * np.cos(k * theta) for k, c in zip(ks, cs))       # endpoint-vanishing
        target = sum(c * np.sin(k * theta) for k, c in zip(ks, cs))  # circular conjugate
        Hf = H @ f
        denom = max(np.abs(target[m]).max(), 1e-300)
        return float(np.abs(Hf[m] - target[m]).max() / denom)

    modes = [[1, 3], [2, 4], [1, 5], [0, 2], [2, 6]]
    per_mode = [{"modes": ks, "rel_err": rel_err(ks, [1, -1])} for ks in modes]
    # the plain anchor as the k=1 gate
    f = -(1.0 + np.cos(theta)) / 2.0
    tgt = -0.5 * np.sin(theta)
    anchor_err = float(np.abs((H @ f)[m] - tgt[m]).max() / np.abs(tgt[m]).max())
    return {
        "per_mode": per_mode,
        "anchor_rel_err": anchor_err,
        "anchor_fourier": {"a0": -0.5, "a1": -0.5, "higher": 0.0},
        "note": "line Hilbert = circular conjugate (cos k.theta -> sin k.theta) "
                "on the decaying subspace; anchor is a 2-term cosine object.",
    }


def q4_operator_structure(R, D, N=12, c_tw=0.5):
    """The linearized operator DF at the anchor in the cos->sin Fourier basis.

    R2 is ODD (Omega even => Omega H(Omega) and Omega_X odd), so DF maps the
    EVEN profile perturbation h = sum_k a_k cos(k*theta) to an ODD residual
    sum_m b_m sin(m*theta). With the anchor Omega_2 = -(1+cos theta)/2 and
    H(Omega_2) = -(1/2) sin theta, each of the three terms of
        DF[h] = h H(Omega_2) + Omega_2 H(h) - c_tw h_X,  h_X = (1+cos theta) h_theta
    couples cosine mode k only to sine modes k-1, k, k+1 -> DF is TRIDIAGONAL,
    plus a rank-1 column d/d(c_tw) = -Omega_{2,X} = -(1/2)sin theta - (1/4)sin 2theta.
    Built here in closed form (exact) and CROSS-CHECKED against the dense grid
    operator so the analytic operator the next brick will use is validated."""
    # closed-form banded matrix B[m-1, k]: coeff of sin(m theta) from cos(k theta)
    B = np.zeros((N, N + 1))                    # rows m=1..N, cols k=0..N

    def add(m, k, val):                         # accumulate coeff of sin(m) from cos(k)
        if 1 <= m <= N and 0 <= k <= N:
            B[m - 1, k] += val

    for k in range(0, N + 1):
        # term 1: h H(Omega_2) = cos(k) * (-1/2 sin) = -1/4 [sin(k+1) - sin(k-1)]
        add(k + 1, k, -0.25)
        add(k - 1, k, +0.25)
        if k >= 1:
            # term 2: Omega_2 H(cos k) = (-1/2 - 1/2 cos) sin(k)
            add(k, k, -0.5)
            add(k + 1, k, -0.25)
            add(k - 1, k, -0.25)
            # term 3: -c_tw (1+cos) d_theta cos(k) = c_tw k (1+cos) sin(k)
            add(k, k, c_tw * k)
            add(k + 1, k, 0.5 * c_tw * k)
            add(k - 1, k, 0.5 * c_tw * k)

    # rank-1 c_tw column: -Omega_{2,X}; Omega_{2,X}=(1/2)(1+cos)sin = 1/2 sin + 1/4 sin2
    dcol = np.zeros(N)
    dcol[0] = -0.5
    if N >= 2:
        dcol[1] = -0.25

    # cross-check the analytic B against the dense grid linearization L
    X, Xr = R.X, R.X_rho
    theta = 2.0 * np.arctan(X)
    Om = clm_two_scale(X)
    HOm = R.Hmat @ Om
    L = np.diag(HOm) + np.diag(Om) @ R.Hmat - c_tw * (D / Xr[:, None])  # L h on grid
    msk = np.abs(X) < 15.0
    w = np.gradient(theta)                       # d theta measure for projection
    max_mismatch = 0.0
    for k in range(1, min(N, 6) + 1):            # check a few interior cosine modes
        h = np.cos(k * theta)
        Lh = L @ h
        # project Lh onto sin(m theta): b_m = <Lh, sin m> / <sin m, sin m>
        for m in range(1, min(N, 6) + 1):
            s = np.sin(m * theta)
            num = np.sum((Lh * s * w)[msk])
            den = np.sum((s * s * w)[msk])
            b_num = num / den
            max_mismatch = max(max_mismatch, abs(b_num - B[m - 1, k]))

    bandwidth = int(np.max([abs(m - k) for m in range(1, N + 1)
                            for k in range(N + 1) if abs(B[m - 1, k]) > 1e-12]))
    return {
        "N_modes": N,
        "B_cos_to_sin": B.tolist(),
        "dc_column": dcol.tolist(),
        "bandwidth": bandwidth,
        "grid_crosscheck_max_mismatch": float(max_mismatch),
        "note": "DF is tridiagonal (bandwidth 1) cos->sin + a rank-1 c_tw column; "
                "closed form matches the grid operator to discretization error.",
    }


def main():
    n = 2001
    R = GCLMResidual(a=0.0, n=n)
    D = build_derivative_matrix(n, R.drho)

    data = {
        "meta": {
            "leg": "P2 Route-D v1 (interval core + a=0 framing probe)",
            "tier": "Level-1 tooling + scoping (NOT a certificate)",
            "n_grid": n,
            "c_grid": R.c,
            "anchor": "Omega_2 = -1/(1+X^2), c_tw = 1/2",
            "reproduce": "python experiments/p2_route_d_probe.py",
        },
        "q1_arithmetic_precision": q1_arithmetic_precision(R, D),
        "q2_degeneracy": q2_degeneracy(R, D),
        "q3_diagonalization": q3_diagonalization(R),
        "q4_operator_structure": q4_operator_structure(R, D),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    q1 = data["q1_arithmetic_precision"]
    q2 = data["q2_degeneracy"]
    q3 = data["q3_diagonalization"]
    print(f"Q1  defect_inf={q1['defect_inf']:.3e}  enclosure_width={q1['enclosure_width']:.3e}"
          f"  overhead={q1['overhead_ratio']:.2e}")
    for b in q1["genome_box"]:
        print(f"    box r={b['radius']:.0e}: sup|R2|<= {b['sup_R2_over_box']:.3e}")
    print(f"Q2  gauge-slaved sigma={q2['gauge_slaved']['sigma']}  "
          f"kernel_dim={q2['gauge_slaved']['kernel_dim']}")
    print(f"    fixed c_tw   sigma={q2['fixed_ctw_half']['sigma']}  "
          f"kernel_dim={q2['fixed_ctw_half']['kernel_dim']}")
    print(f"Q3  anchor covariance rel_err={q3['anchor_rel_err']:.3e}; "
          f"per-mode max={max(pm['rel_err'] for pm in q3['per_mode']):.3e}")
    q4 = data["q4_operator_structure"]
    print(f"Q4  DF bandwidth={q4['bandwidth']} (cos->sin) + rank-1 c_tw col; "
          f"grid cross-check mismatch={q4['grid_crosscheck_max_mismatch']:.3e}")
    print(f"[done] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
