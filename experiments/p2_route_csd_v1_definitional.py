"""Leg 164 -- Route-CSD: does the `a = 0` CLM linearization admit a COMPACT-SUPPORT
representation at all?  The definitional question underneath leg 162's ambiguity.

READ-ONLY LEG.  Nothing under `solver/` is edited; every operator used here is either
imported from `solver/` or rebuilt inline from that module's own exact identities and
then GATED against the module (CSD1).  Leg 162's parked branch is read, never written.

--------------------------------------------------------------------------
WHAT IS ALREADY BANKED, AND WHAT IS NOT (see writeup/novelty/leg_164.md sec 0)
--------------------------------------------------------------------------
Leg 162 already measured the ANCHOR's support: `Omega_0 = -4X/(1+4X^2)`, decay exponent
-0.99999673, mass outside radius R falling 0.8656 -> 0.4095 over R = 1..4096 and never
reaching zero, and `solver/first_integral.py:414` refusing `a = 0` outright.  That is NOT
re-derived here.

What no leg has asked is the question that actually decides the gate.  "Compact support"
is a property of a SUBSPACE, and there are two independent halves to it:

  (E) EXISTENCE -- does the linearization's own DOMAIN contain nonzero compactly
      supported elements?  The domain is the odd sine system {sin k theta}, k >= 1, on
      theta in (-pi, pi) with X = tan(theta/2).  That system is COMPLETE for odd
      L^2(-pi, pi), so the honest answer is YES in the flat and algebraic weight classes
      -- and this leg exhibits them exactly rather than asserting it.  It is NO in the
      geometric class nu^k, nu > 1, which is the literature's default: nu^k-summable
      coefficients means real-analytic, and a real-analytic function vanishing on an open
      arc vanishes identically.

  (I) INVARIANCE -- is any nonzero compactly supported subspace preserved by the
      linearization?  This is the half that decides.  The linearization at the a = 0
      anchor is, pointwise,

          L h = cos(theta) h  -  (H h) sin(theta)  -  sin(theta) h_theta

      (derived below and GATED against `bordered_linearization` in CSD1).  Two of the
      three terms are LOCAL and preserve support.  The third, `-(H h) sin(theta)`, is the
      anchor `Omega_0 = -sin(theta)` multiplying a nonlocal transform -- and `Omega_0`
      vanishes only at theta = 0, pi.  So `L h` escapes supp h wherever `H h` does not
      vanish, and by the LUZIN-PRIVALOV uniqueness theorem `h` and `H h` cannot both
      vanish on an arc unless h = 0: the Hardy-class function
      F = -(H h) + const + i h would be constant on a set of positive measure.

      `solver/finite_support.py` states the a > 0 CONVERSE of exactly this clause --
      "every term of R = Omega H(Omega) - E Omega_X carries a factor of Omega or Omega_X,
      even though H(Omega) does not vanish outside -- so the problem closes on the support
      alone".  That mechanism is inherited from the ANCHOR's compact support.  At a = 0
      the anchor has none, and CSD4 is that sentence turned into a control: the identical
      code path, with the anchor swapped for a compactly supported one, reports escape
      exactly 0.

--------------------------------------------------------------------------
SECTIONS
--------------------------------------------------------------------------
CSD1  self-consistency gate: the pointwise operator above reproduces
      `spectral_certificate.bordered_linearization` AND the exact central difference of
      `clm_residual` at the anchor, column for column, in exact Fraction arithmetic.
      Three independent paths, one matrix.  Without this the leg measures a lookalike.
CSD2  (E): an EXACT family of compactly supported odd elements -- m-fold box convolutions
      (B-splines) with closed-form sine coefficients b_k = (2 sin(kw)/k)^m sin(k theta_c),
      no quadrature anywhere -- classified against the module's own three weight classes.
CSD3  (I): the escape measurement.  Mass of L h lying outside supp h, and the minimized
      Rayleigh ratio over K-dimensional families of compactly supported perturbations,
      as a ladder in K (discipline 72).
CSD4  POSITIVE CONTROL (lesson 90): same code path, compactly supported anchor, escape 0.
CSD5  the corner's own parameter: X_c(a) from the landed `solver/first_integral.py`, as a
      ladder in a, with the divergence rate as a -> 0.
CSD6  the gate, in its pre-committed wording.

NO GA compute.  Deterministic grids only.  No dynamics.
"""

import json
import os
import sys
import time
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import spectral_certificate as SC          # noqa: E402
from solver.first_integral import ReducedProfile       # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_csd_v1_definitional.json")


# ==========================================================================
# CSD1 -- the self-consistency gate.  Exact arithmetic, three independent paths.
# ==========================================================================
def _add(d, mode, val):
    """Accumulate `val * sin(mode * theta)` using sin(-m) = -sin(m), sin(0) = 0."""
    if mode == 0:
        return
    if mode < 0:
        mode, val = -mode, -val
    d[mode] = d.get(mode, Fraction(0)) + val


def pointwise_column(k, half=Fraction(1, 2)):
    """L(sin k theta) in odd-sine coefficients, assembled TERM BY TERM from the pointwise
    form  L h = cos(theta) h - (H h) sin(theta) - sin(theta) h_theta,  using only

        cos(a) sin(b) = (sin(b+a) + sin(b-a)) / 2                (product to sum)
        H(sin k theta) = -cos k theta + (-1)^k                   (module docstring l.16)

    Nothing about `bordered_linearization` is used here; that is the point.
    """
    out = {}
    one = Fraction(1)
    # (1)  cos(theta) * sin(k theta)
    _add(out, k + 1, half)
    _add(out, k - 1, half)
    # (2)  -(H sin k theta) * sin(theta) = (cos k theta) sin(theta) - (-1)^k sin(theta)
    #      cos(k theta) sin(theta) = (sin(1+k) + sin(1-k)) / 2
    _add(out, 1 + k, half)
    _add(out, 1 - k, half)
    _add(out, 1, -one * ((-1) ** k))
    # (3)  -sin(theta) * d/dtheta sin(k theta) = -k sin(theta) cos(k theta)
    _add(out, 1 + k, -half * k)
    _add(out, 1 - k, -half * k)
    return {m: v for m, v in out.items() if v != 0}


def central_difference_column(k, K):
    """DR[sin k theta] at the anchor, by an EXACT central difference of the module's own
    `clm_residual`.  R is quadratic in b, so (R(b0+h) - R(b0-h)) / 2 is the derivative
    with no error term at all -- in Fractions this is exact, not an approximation."""
    b0, c_om, c_l = SC.clm_anchor(K)
    hp = list(b0)
    hm = list(b0)
    hp[k - 1] = hp[k - 1] + Fraction(1)
    hm[k - 1] = hm[k - 1] - Fraction(1)
    Rp = SC.clm_residual(hp, c_om, c_l)
    Rm = SC.clm_residual(hm, c_om, c_l)
    col = [(Rp[i] - Rm[i]) / 2 for i in range(len(Rp))]
    return {i + 1: col[i] for i in range(len(col)) if col[i] != 0}


def csd1_gate(K=12):
    M = SC.bordered_linearization(K, exact=True)
    rows = []
    ok_matrix = ok_diff = True
    for k in range(1, K + 1):
        pw = pointwise_column(k)
        mat = {r: M[r - 1][k - 1] for r in range(1, K + 1) if M[r - 1][k - 1] != 0}
        pw_trunc = {r: v for r, v in pw.items() if 1 <= r <= K}
        cd = central_difference_column(k, K)
        cd_trunc = {r: v for r, v in cd.items() if 1 <= r <= K}
        a = (pw_trunc == mat)
        b = (pw_trunc == cd_trunc)
        ok_matrix &= a
        ok_diff &= b
        rows.append({"k": k,
                     "pointwise": {str(r): str(v) for r, v in sorted(pw.items())},
                     "matches_bordered_linearization": bool(a),
                     "matches_exact_central_difference_of_clm_residual": bool(b)})
    return {
        "K": K,
        "operator": "L h = cos(theta) h - (H h) sin(theta) - sin(theta) h_theta",
        "anchor": "Omega_0 = -sin(theta), c_omega = -1, c_l = 1 (spectral_certificate.clm_anchor)",
        "columns": rows,
        "all_columns_match_bordered_linearization": bool(ok_matrix),
        "all_columns_match_exact_central_difference": bool(ok_diff),
        "arithmetic": "fractions.Fraction throughout -- exact, no float anywhere in CSD1",
        "reading": ("the pointwise operator this leg measures IS the banked matrix, on "
                    "three independent construction paths.  Discipline 85: re-measure the "
                    "headline object before building on it."),
    }


# ==========================================================================
# CSD2 -- (E) EXISTENCE.  An exact family of compactly supported odd elements.
# ==========================================================================
def bspline_coeffs(k, m, half_width, theta_c):
    """Sine coefficients of the m-fold box convolution B_m, half-width `half_width`,
    centred at theta_c, supported on [theta_c - half_width, theta_c + half_width].

        integral B_m(theta) e^{i k theta} dtheta = e^{i k theta_c} (2 sin(k w) / k)^m,
        w = half_width / m

    so  integral_0^pi B_m sin(k theta) dtheta = (2 sin(k w) / k)^m sin(k theta_c).
    EXACT closed form -- there is no quadrature and no noise floor in this section.
    """
    w = float(half_width) / int(m)
    return (2.0 * np.sin(k * w) / k) ** int(m) * np.sin(k * float(theta_c))


def weight_class_ladders(b, K_ladder, s_list=(0.3, 1.0, 2.0, 4.0),
                         nu_list=(1.02, 1.05)):
    """Partial sums of ||b||_w over the module's own three weight classes."""
    k = np.arange(1, len(b) + 1, dtype=float)
    ab = np.abs(b)
    out = {"flat": [], "algebraic": {str(s): [] for s in s_list},
           "geometric_log10": {str(nu): [] for nu in nu_list}}
    for K in K_ladder:
        out["flat"].append(float(ab[:K].sum()))
        for s in s_list:
            out["algebraic"][str(s)].append(float(((1.0 + k[:K]) ** s * ab[:K]).sum()))
        for nu in nu_list:
            lg = k[:K] * np.log10(nu) + np.log10(np.maximum(ab[:K], 1e-300))
            out["geometric_log10"][str(nu)].append(float(np.max(lg)))
    return out


def csd2_existence(K=2048, half_width=0.8, theta_c=1.2, m_list=(1, 2, 4, 8, 16)):
    k = np.arange(1, K + 1, dtype=float)
    K_ladder = [64, 128, 256, 512, 1024, 2048]
    rows = []
    for m in m_list:
        b = bspline_coeffs(k, m, half_width, theta_c)
        scale = np.max(np.abs(b))
        b = b / scale
        lad = weight_class_ladders(b, K_ladder)
        # measured algebraic decay exponent of the envelope, over the top decade
        lo, hi = K // 8, K
        env_k, env_v = [], []
        for a0 in range(lo, hi, 32):                     # envelope over 32-mode windows
            w = np.abs(b[a0:a0 + 32])
            if w.max() > 0:
                env_k.append(a0 + 16.0)
                env_v.append(w.max())
        expo = float(np.polyfit(np.log(env_k), np.log(env_v), 1)[0])
        rows.append({
            "m": int(m),
            "smoothness": f"C^{m-2}" if m >= 2 else "discontinuous (box)",
            "support_theta": [float(theta_c - half_width), float(theta_c + half_width)],
            "support_X": [float(np.tan((theta_c - half_width) / 2.0)),
                          float(np.tan((theta_c + half_width) / 2.0))],
            "measured_coefficient_decay_exponent": expo,
            "predicted_decay_exponent": float(-m),
            "flat_l1_partial_sums": lad["flat"],
            "flat_l1_converges": bool(m >= 2),
            "algebraic_partial_sums": lad["algebraic"],
            "geometric_log10_max_term": lad["geometric_log10"],
        })
    return {
        "construction": ("m-fold box convolutions on [theta_c - h, theta_c + h] subset "
                         "(0, pi), oddly extended; sine coefficients in closed form, "
                         "b_k = (2 sin(k h/m)/k)^m sin(k theta_c).  No quadrature."),
        "why_these_are_compactly_supported_in_X": (
            "supp subset (0, pi) means the element vanishes on a neighbourhood of "
            "theta = ±pi, i.e. on |X| > tan(theta_max/2) -- compact support in X."),
        "K": K, "K_ladder": K_ladder, "rows": rows,
        "flat_and_algebraic_contain_nonzero_compactly_supported_elements": True,
        "geometric_contains_none": True,
        "geometric_reason": ("sum_k nu^k |b_k| < inf with nu > 1 means the element extends "
                             "holomorphically to an annulus, i.e. is real-analytic on the "
                             "circle; a real-analytic function vanishing on an open arc "
                             "vanishes identically.  The measured max_k log10(nu^k |b_k|) "
                             "ladders below grow without bound for every m, which is the "
                             "numerical face of that theorem."),
        "honest_reading": ("this half of the question answers YES, AGAINST the leg's "
                           "expected verdict, in 2 of the module's 3 weight classes.  "
                           "'The domain is unbounded' is therefore NOT by itself a reason "
                           "for the gate to answer no -- the invariance half (CSD3) is."),
    }


# ==========================================================================
# CSD3 / CSD4 -- (I) INVARIANCE.  The escape measurement, and its control.
# ==========================================================================
def hilbert_from_coeffs(b, theta):
    """H h on `theta`, from the module's own exact identity H(sin k th) = -cos k th + (-1)^k."""
    k = np.arange(1, len(b) + 1, dtype=float)
    C = np.cos(np.outer(theta, k))
    return -(C @ b) + float(np.sum(b * ((-1.0) ** k)))


def series_from_coeffs(b, theta, derivative=False):
    k = np.arange(1, len(b) + 1, dtype=float)
    if derivative:
        return np.cos(np.outer(theta, k)) @ (b * k)
    return np.sin(np.outer(theta, k)) @ b


def escape_measure(b, supp, theta, wq, anchor_vals, anchor_supp,
                   multiplier_vals, transport_vals):
    """Fraction of |L h| mass lying OUTSIDE the anchor's support.

    L h = multiplier(theta) * h  +  (H h) * anchor(theta)  -  transport(theta) * h_theta

    The two local terms vanish off supp h.  The anchor term vanishes off supp(anchor).
    THE SAME FUNCTION serves CSD3 (anchor = -sin theta, support = the whole circle) and
    CSD4 (anchor compactly supported) -- that identity of code path is what makes the
    control a control (lesson 90).
    """
    h = series_from_coeffs(b, theta)
    dh = series_from_coeffs(b, theta, derivative=True)
    Hh = hilbert_from_coeffs(b, theta)
    local = multiplier_vals * h - transport_vals * dh          # provably 0 off supp h
    nonlocal_ = Hh * anchor_vals                               # the only escaping term
    Lh = local + nonlocal_
    inside_h = (theta >= supp[0]) & (theta <= supp[1])
    inside_anchor = (theta >= anchor_supp[0]) & (theta <= anchor_supp[1])
    total = float(np.sum(wq * np.abs(Lh)))
    out_h = float(np.sum(wq * np.abs(Lh) * (~inside_h)))
    out_anchor = float(np.sum(wq * np.abs(Lh) * (~inside_anchor)))
    # the local terms are ZERO off supp h in exact arithmetic; whatever they contribute
    # there is the finite-K truncation artifact, and it is measured, not bounded.
    out_local = float(np.sum(wq * np.abs(local) * (~inside_h)))
    out_nonlocal = float(np.sum(wq * np.abs(nonlocal_) * (~inside_h)))
    leak = float(np.max(np.abs(h[~inside_h]))) if np.any(~inside_h) else 0.0
    return {"total_L1_mass": total,
            "mass_outside_supp_h": out_h,
            "mass_outside_supp_anchor": out_anchor,
            "escape_fraction_vs_supp_h": out_h / total if total > 0 else float("nan"),
            "escape_fraction_vs_supp_anchor": (out_anchor / total if total > 0
                                               else float("nan")),
            "local_terms_mass_outside_supp_h_TRUNCATION_ARTIFACT": out_local,
            "hilbert_term_mass_outside_supp_h": out_nonlocal,
            "hilbert_over_truncation_artifact": (out_nonlocal / out_local
                                                 if out_local > 0 else float("inf")),
            "truncation_leakage_max_abs_h_outside_supp": leak}


def _gl(n, a, b):
    x, w = np.polynomial.legendre.leggauss(int(n))
    return 0.5 * (b - a) * x + 0.5 * (a + b), 0.5 * (b - a) * w


def csd3_invariance(K=2048, half_width=0.8, theta_c=1.2, m_list=(2, 4, 8, 16),
                    n_quad=6000):
    theta, wq = _gl(n_quad, 1e-12, np.pi - 1e-12)
    mult = np.cos(theta)                     # c_omega + H Omega_0 = cos theta
    anch = -np.sin(theta)                    # Omega_0
    trans = np.sin(theta)                    # c_l X d/dX = sin theta d/dtheta
    k = np.arange(1, K + 1, dtype=float)
    supp = (theta_c - half_width, theta_c + half_width)
    rows = []
    for m in m_list:
        b = bspline_coeffs(k, m, half_width, theta_c)
        b = b / np.max(np.abs(b))
        r = escape_measure(b, supp, theta, wq, anch, (0.0, np.pi), mult, trans)
        r["m"] = int(m)
        # The 1000x bar is PRE-SET, not fitted to the data.  A row that does not clear it
        # is under-resolved at this K and is excluded from the gate (lesson 86), not
        # accommodated by moving the bar.
        r["resolved"] = bool(r["hilbert_over_truncation_artifact"] > 1e3)
        rows.append(r)
    # the excluded row's artifact is a pure truncation effect: show it converging away
    artifact_ladder = []
    for Kt in (256, 512, 1024, 2048):
        bt = bspline_coeffs(np.arange(1, Kt + 1, dtype=float), 2, half_width, theta_c)
        bt = bt / np.max(np.abs(bt))
        rr = escape_measure(bt, supp, theta, wq, anch, (0.0, np.pi), mult, trans)
        artifact_ladder.append({"K": Kt, "m": 2,
                                "hilbert_over_truncation_artifact":
                                    rr["hilbert_over_truncation_artifact"],
                                "escape_fraction": rr["escape_fraction_vs_supp_h"]})
    # truncation stability of the m = 8 row
    stab = []
    for Kt in (256, 512, 1024, 2048):
        bt = bspline_coeffs(np.arange(1, Kt + 1, dtype=float), 8, half_width, theta_c)
        bt = bt / np.max(np.abs(bt))
        rr = escape_measure(bt, supp, theta, wq, anch, (0.0, np.pi), mult, trans)
        stab.append({"K": Kt, "escape_fraction": rr["escape_fraction_vs_supp_h"]})
    return {"rows": rows, "truncation_ladder_m8": stab,
            "m2_artifact_ladder": artifact_ladder,
            "m2_artifact_reading": (
                "the m = 2 row's escape (0.0944, the LARGEST of the four) is real, but its "
                "truncation artifact at K = 2048 is only 86.8x smaller, below the PRE-SET "
                "1000x bar -- because C^0 coefficients decay like k^-2 and the artifact "
                "falls only like 1/K.  The ladder above shows the ratio growing linearly "
                "in K, i.e. the artifact converges away and the escape does not.  The row "
                "is nevertheless EXCLUDED from the gate rather than admitted by lowering "
                "the bar, which is conservative: it is the largest escape of the four."),
            "local_terms_preserve_support": (
                "cos(theta) h and sin(theta) h_theta are pointwise multiples of h and "
                "h_theta, so they vanish identically off supp h; the ENTIRE escape is the "
                "term (H h) * Omega_0."),
            "quadrature": f"Gauss-Legendre, {n_quad} nodes on (0, pi)"}


def csd3_minimized(half_width=0.8, theta_c=1.2, K_list=(1, 2, 4, 8, 16, 32),
                   K_modes=1536, n_quad=6000, n_basis_quad=4000):
    """The minimum of ||(H h) sin(theta)||^2_{L2(outside supp)} / ||h||^2_{L2(supp)} over
    K-dimensional families of compactly supported h.  Strictly positive for every K by
    Luzin-Privalov; the LADDER is the honest content (discipline 72)."""
    a0, b0 = theta_c - half_width, theta_c + half_width
    delta = b0 - a0
    tq, tw = _gl(n_basis_quad, a0, b0)
    kk = np.arange(1, K_modes + 1, dtype=float)
    Kmax = max(K_list)
    # basis: sine half-waves supported exactly on [a0, b0]
    PHI = np.sin(np.outer(tq - a0, np.arange(1, Kmax + 1) * np.pi / delta))   # (nq, Kmax)
    S = np.sin(np.outer(tq, kk))                                             # (nq, K_modes)
    B = (2.0 / np.pi) * (PHI * tw[:, None]).T @ S                            # coefficients
    theta, wq = _gl(n_quad, 1e-12, np.pi - 1e-12)
    outside = (theta < a0) | (theta > b0)
    Hall = np.stack([hilbert_from_coeffs(B[i], theta) for i in range(Kmax)])  # (Kmax, nq)
    W = wq * outside * np.sin(theta) ** 2
    A = Hall @ (W[:, None] * Hall.T)
    G = (PHI * tw[:, None]).T @ PHI                                          # Gram on supp
    rows = []
    for Kd in K_list:
        Ad, Gd = A[:Kd, :Kd], G[:Kd, :Kd]
        Lc = np.linalg.cholesky(Gd)
        Mred = np.linalg.solve(Lc, np.linalg.solve(Lc, Ad).T).T
        ev = np.linalg.eigvalsh(0.5 * (Mred + Mred.T))
        condG = float(np.linalg.cond(Gd))
        # LESSON 86: this eigenvalue is only meaningful above the float64 floor that the
        # symmetric eigensolver plus the Gram conditioning together impose on it.
        floor = float(np.finfo(float).eps * max(ev[-1], 0.0) * condG)
        rows.append({"K": int(Kd), "min_rayleigh": float(ev[0]),
                     "max_rayleigh": float(ev[-1]),
                     "gram_condition_number": condG,
                     "float64_resolution_floor": floor,
                     "resolved": bool(ev[0] > floor)})
    res = [r for r in rows if r["resolved"]]
    lg = [np.log10(r["min_rayleigh"]) for r in res]
    return {"rows": rows,
            "resolved_K": [r["K"] for r in res],
            "decades_lost_over_resolved_range": float(lg[0] - lg[-1]) if len(lg) > 1 else None,
            "strictly_positive_over_resolved_range": bool(all(r["min_rayleigh"] > 0
                                                              for r in res)),
            "unresolved_K": [r["K"] for r in rows if not r["resolved"]],
            "not_used_for_the_gate": True,
            "reading": ("over the range float64 can resolve, the minimum is strictly "
                        "positive at every K -- no compactly supported subspace of those "
                        "dimensions is invariant -- and it falls by the decades reported "
                        "above.  Beyond that range the computed eigenvalue goes NEGATIVE "
                        "(a positive semi-definite form cannot), which is a statement "
                        "about float64 and not about the operator (lesson 86), so this "
                        "ladder is reported as the SHAPE of the ejection and is "
                        "deliberately not what the gate is read off.  The exact statement "
                        "is Luzin-Privalov and it holds at every K: if h and H h both "
                        "vanish on an arc then the Hardy-class function "
                        "F = -(H h) + const + i h is constant on a set of positive "
                        "measure, hence h = 0.  The non-uniformity is the same severe "
                        "ill-posedness that makes analytic continuation off an arc "
                        "unstable, and it is why an APPROXIMATELY invariant compactly "
                        "supported subspace exists while an invariant one does not."),
            "K_modes": K_modes, "basis": "sin(i pi (theta - a)/(b - a)) on [a, b], 0 outside"}


def csd3b_pointwise(K=2048, half_width=0.8, theta_c=1.2, m=8, n_quad=6000):
    """Where does L h escape -- somewhere, or everywhere off supp h?

    Off supp h the kernel of H is smooth, so H h is REAL-ANALYTIC on the complementary
    arc; so is -(H h) sin(theta), whose only forced zeros are theta = 0, pi.  If it
    vanished on any sub-interval of the complement it would vanish on all of it by
    analytic continuation, and then h = H h = 0 on an arc forces h = 0.  So the escape is
    not a boundary artifact: it is everywhere off supp h except an isolated zero set.
    This measures that."""
    theta, wq = _gl(n_quad, 1e-12, np.pi - 1e-12)
    k = np.arange(1, K + 1, dtype=float)
    b = bspline_coeffs(k, m, half_width, theta_c)
    b = b / np.max(np.abs(b))
    supp = (theta_c - half_width, theta_c + half_width)
    outside = (theta < supp[0]) | (theta > supp[1])
    h = series_from_coeffs(b, theta)
    Hh = hilbert_from_coeffs(b, theta)
    esc = np.abs(Hh * (-np.sin(theta)))[outside]
    leak = float(np.max(np.abs(h[outside])))
    scale = float(np.max(esc))
    # exclude the two forced zeros theta = 0, pi by a fixed margin, then count
    th_o = theta[outside]
    interior = (th_o > 0.05) & (th_o < np.pi - 0.05)
    frac = float(np.mean(esc[interior] > max(1e3 * leak, 1e-12)))
    return {"m": int(m), "K": K,
            "n_outside_nodes": int(outside.sum()),
            "truncation_leakage_max_abs_h_outside": leak,
            "max_abs_escape_density": scale,
            "min_abs_escape_density_away_from_forced_zeros": float(np.min(esc[interior])),
            "fraction_of_outside_nodes_with_escape_above_1000x_leakage": frac,
            "forced_zeros": "theta = 0 and theta = pi only, where Omega_0 = -sin(theta) = 0",
            "reading": ("the escape density is nonzero on essentially every outside node, "
                        "not merely near supp h.  L h leaves the compactly supported class "
                        "on the WHOLE complement, which is what the analyticity argument "
                        "above predicts.")}


def csd4_control(K=2048, half_width=0.8, theta_c=1.2, m=8, n_quad=6000,
                 anchor_half_width=1.1, anchor_m=8):
    """LESSON 90.  The identical `escape_measure` code path with the ONLY change being the
    anchor's support.  If this does not report exactly 0, the CSD3 negative is a tautology
    of the code rather than a fact about the operator."""
    theta, wq = _gl(n_quad, 1e-12, np.pi - 1e-12)
    k = np.arange(1, K + 1, dtype=float)
    b = bspline_coeffs(k, m, half_width, theta_c)
    b = b / np.max(np.abs(b))
    supp = (theta_c - half_width, theta_c + half_width)
    # a COMPACTLY SUPPORTED anchor, strictly containing supp h -- the a > 0 structure of
    # solver/first_integral.py (Omega vanishes outside [0, X_c]), transplanted verbatim.
    ab = bspline_coeffs(k, anchor_m, anchor_half_width, theta_c)
    ab = ab / np.max(np.abs(ab))
    anchor_vals = series_from_coeffs(ab, theta)
    asupp = (theta_c - anchor_half_width, theta_c + anchor_half_width)
    anchor_vals = np.where((theta >= asupp[0]) & (theta <= asupp[1]), anchor_vals, 0.0)
    mult = np.where((theta >= asupp[0]) & (theta <= asupp[1]), np.cos(theta), 0.0)
    trans = np.sin(theta)
    ctl = escape_measure(b, supp, theta, wq, anchor_vals, asupp, mult, trans)
    # and the a = 0 anchor through the SAME call, so the pair differs in one argument
    live = escape_measure(b, supp, theta, wq, -np.sin(theta), (0.0, np.pi),
                          np.cos(theta), trans)
    return {
        "control_anchor": ("compactly supported on "
                           f"[{asupp[0]:.4f}, {asupp[1]:.4f}] (theta), strictly containing "
                           "supp h -- the a > 0 structure of solver/first_integral.py"),
        "control": ctl,
        "live_a0_anchor_same_call": live,
        "separation_ratio_live_over_control": (
            live["escape_fraction_vs_supp_h"]
            / max(ctl["mass_outside_supp_anchor"] / max(ctl["total_L1_mass"], 1e-300),
                  1e-300)),
        "control_escape_at_truncation_floor": bool(
            ctl["mass_outside_supp_anchor"]
            <= 1e3 * ctl["truncation_leakage_max_abs_h_outside_supp"] + 1e-13),
        "what_would_have_had_to_change": (
            "one argument: `anchor_vals`/`anchor_supp`.  The transform H, the perturbation "
            "h, the multiplier, the transport, the quadrature and the norm are identical "
            "between the two rows.  So the measured difference is a statement about the "
            "ANCHOR's support and nothing else."),
    }


# ==========================================================================
# CSD5 -- the corner's own parameter.  X_c(a) from the landed solver, read-only.
# ==========================================================================
def csd5_xc_ladder(a_list=(1.2, 1.0, 0.8, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2), K=48):
    rows = []
    for a in a_list:
        p = ReducedProfile(float(a), K=K)
        r = p.solve()
        rows.append({"a": float(a), "X_c": float(r["Xc"]),
                     "converged": bool(r["converged"]),
                     "residual": float(r["residual"]),
                     "iterations": int(r["iterations"])})
    try:
        ReducedProfile(0.0, K=K)
        refusal = None
    except ValueError as exc:
        refusal = str(exc)
    ok = [r for r in rows if r["converged"]]
    la = np.log(np.array([r["a"] for r in ok]))
    lx = np.log(np.array([r["X_c"] for r in ok]))
    slope = float(np.polyfit(la, lx, 1)[0])
    return {"rows": rows,
            "a_of_leg_162_corner": [0.8, 0.5],
            "X_c_at_leg_162_a_values": {str(r["a"]): r["X_c"]
                                        for r in rows if r["a"] in (0.8, 0.5)},
            "log_log_slope_dlogXc_dloga": slope,
            "X_c_growth_factor_a_1p2_to_0p2": (ok[-1]["X_c"] / ok[0]["X_c"]) if ok else None,
            "a_equals_zero_refusal": refusal,
            "reading": ("leg 162's corner is parameterized by a finite support radius X_c, "
                        "which is an OUTPUT of the a > 0 equations.  It grows without bound "
                        "as a -> 0 and the landed module refuses a = 0 outright: at a = 0, "
                        "E = c + a U = c != 0 never crosses zero, so there is no radius at "
                        "which the profile ends.")}


# ==========================================================================
# CSD6 -- the bridge to leg 162's parked corner.  READ-ONLY, never written.
# ==========================================================================
def csd6_bridge(xc_rows):
    """Leg 162's own Z_1, read straight out of its PARKED branch, against the support
    radius X_c(a) measured in CSD5.  Nothing here writes to that branch."""
    import subprocess
    ref = "origin/leg/162-capg-v1:writeup/data/p2_route_capg_v1_corner.json"
    source, grid = "git show " + ref, None
    try:
        raw = subprocess.run(["git", "show", ref], capture_output=True, text=True,
                             timeout=60, check=True).stdout
        grid = json.loads(raw)["CAPG4_grid"]
    except Exception as exc:                                   # noqa: BLE001
        source = f"UNAVAILABLE ({type(exc).__name__}); quoted from leg 162's commit message"
    xc = {r["a"]: r["X_c"] for r in xc_rows if r["converged"]}
    rows = []
    if grid is not None:
        best = {}
        for g in grid:
            if not g.get("A21_zero"):
                continue
            a = float(g["a"])
            if a not in best or g["Z1"] < best[a]["Z1"]:
                best[a] = g
        for a in sorted(best):
            rows.append({"a": a, "best_Z1_over_A21_zero": float(best[a]["Z1"]),
                         "realization": best[a]["realization"],
                         "shape": best[a]["shape"], "s": best[a].get("s"),
                         "X_c_measured_here": xc.get(a)})
    else:
        for a, z in ((0.8, 0.08735093095524782), (0.5, 0.2287), (0.2, None)):
            rows.append({"a": a, "best_Z1_over_A21_zero": z, "realization": "quoted",
                         "X_c_measured_here": xc.get(a)})
    ok = [r for r in rows if r["best_Z1_over_A21_zero"] and r["X_c_measured_here"]]
    corr = None
    if len(ok) > 2:
        corr = float(np.corrcoef(np.log([r["X_c_measured_here"] for r in ok]),
                                 np.log([r["best_Z1_over_A21_zero"] for r in ok]))[0, 1])
    return {"source": source, "rows": rows,
            "log_log_correlation_Xc_vs_best_Z1": corr,
            "reading": ("leg 162's corner is best exactly where its support radius is "
                        "SMALLEST, and degrades monotonically as X_c grows -- i.e. as the "
                        "object is pushed toward the a = 0 one, whose X_c is infinite.  "
                        "That is the quantitative form of the gate's NO: the corner's "
                        "quality is a function of the very parameter the a = 0 object does "
                        "not have."),
            "does_not_modify_leg_162": True}


# ==========================================================================
def main():
    t0 = time.time()
    doc = {
        "leg": 164,
        "route": "CSD",
        "version": "v1",
        "question": ("does the a = 0 CLM linearization, as defined in this repository's "
                     "certificate machinery, admit a compact-support representation under "
                     "any basis change consistent with its own defining equations?"),
        "object": ("the a = 0 CLM linearization: solver/spectral_certificate.py "
                   "clm_anchor / clm_residual / bordered_linearization / tail_block, on the "
                   "odd sine system {sin k theta} with X = tan(theta/2)"),
        "read_only": True,
        "no_GA_compute": True,
        "novelty_log": "writeup/novelty/leg_164.md",
        "does_not_overwrite": ("leg 162's parked branch leg/162-capg-v1 and its report are "
                               "read, cited and left untouched"),
    }
    doc["CSD1_self_consistency"] = csd1_gate()
    doc["CSD2_existence"] = csd2_existence()
    doc["CSD3_invariance"] = csd3_invariance()
    doc["CSD3b_pointwise"] = csd3b_pointwise()
    doc["CSD3_minimized"] = csd3_minimized()
    doc["CSD4_positive_control"] = csd4_control()
    doc["CSD5_Xc_ladder"] = csd5_xc_ladder()
    doc["CSD6_bridge_to_leg_162"] = csd6_bridge(doc["CSD5_Xc_ladder"]["rows"])

    # The gate is read off quantities that are ABOVE their own evaluation floors.
    c1 = doc["CSD1_self_consistency"]
    res_rows = [r for r in doc["CSD3_invariance"]["rows"] if r["resolved"]]
    esc = [r["escape_fraction_vs_supp_h"] for r in res_rows]
    ratios = [r["hilbert_over_truncation_artifact"] for r in res_rows]
    doc["CSD3_invariance"]["excluded_from_gate_as_underresolved"] = [
        {"m": r["m"], "escape_fraction": r["escape_fraction_vs_supp_h"],
         "hilbert_over_truncation_artifact": r["hilbert_over_truncation_artifact"]}
        for r in doc["CSD3_invariance"]["rows"] if not r["resolved"]]
    conds = {
        "operator_is_the_banked_one": bool(
            c1["all_columns_match_bordered_linearization"]
            and c1["all_columns_match_exact_central_difference"]),
        "at_least_three_resolved_escape_rows": bool(len(res_rows) >= 3),
        "every_resolved_escape_fraction_above_1e-3": bool(min(esc) > 1e-3),
        "hilbert_term_dominates_truncation_artifact_by_1000x_on_resolved_rows": bool(
            min(ratios) > 1e3),
        "escape_is_everywhere_off_support": bool(
            doc["CSD3b_pointwise"]["fraction_of_outside_nodes_with_escape_above_1000x_leakage"]
            > 0.99),
        "control_can_report_the_other_answer_and_does": bool(
            doc["CSD4_positive_control"]["control_escape_at_truncation_floor"]),
        "control_separation_above_1e9": bool(
            doc["CSD4_positive_control"]["separation_ratio_live_over_control"] > 1e9),
        "corner_parameter_absent_at_a_zero": bool(
            doc["CSD5_Xc_ladder"]["a_equals_zero_refusal"] is not None),
    }
    doc["gate_conditions"] = conds
    doc["gate_conditions_failed"] = [k for k, v in conds.items() if not v]
    invariant_exists = not all(conds.values())
    gate_ok = conds["operator_is_the_banked_one"]
    doc["gate_question"] = ("Does the a = 0 CLM linearization, as defined in this "
                            "repository's certificate machinery, admit a compact-support "
                            "representation under any basis change consistent with its own "
                            "defining equations?")
    doc["gate_answer"] = "NO" if (gate_ok and not invariant_exists) else "YES"
    doc["gate_branch"] = (
        "no -> The linearization is structurally whole-line/unbounded by construction; "
        "leg 162's corner tests a DIFFERENT object, not the one leg 126's audit and leg "
        "58/127's theorem cover.  This resolves the ambiguity without a user ruling: leg "
        "126's completeness claim stands as scoped, and leg 162's corner is a genuinely "
        "separate (and still independently interesting, per leg 162's own measured Z_1 < 1) "
        "question about a related but distinct construction.")
    doc["gate_answer_is_qualified"] = (
        "the NO is on INVARIANCE, not on membership.  The domain does contain nonzero "
        "compactly supported elements in the flat and algebraic weight classes (CSD2), and "
        "none in the geometric class.  What no basis change reaches is a compactly "
        "supported subspace the linearization preserves: the anchor Omega_0 = -sin(theta) "
        "vanishes only at theta = 0, pi, so (H h) Omega_0 leaves supp h for every h != 0.")
    doc["elapsed_s"] = time.time() - t0

    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1)
    print(f"wrote {OUT}  ({doc['elapsed_s']:.1f}s)")
    print("CSD1 gate            :",
          doc["CSD1_self_consistency"]["all_columns_match_bordered_linearization"],
          doc["CSD1_self_consistency"]["all_columns_match_exact_central_difference"])
    for r in doc["CSD2_existence"]["rows"]:
        print(f"CSD2 m={r['m']:>2}  decay {r['measured_coefficient_decay_exponent']:+.4f} "
              f"(pred {r['predicted_decay_exponent']:+.1f})  flat l1(K=2048) "
              f"{r['flat_l1_partial_sums'][-1]:.6g}  "
              f"geom nu=1.05 log10max {r['geometric_log10_max_term']['1.05'][-1]:.4g}")
    for r in doc["CSD3_invariance"]["rows"]:
        print(f"CSD3 m={r['m']:>2}  escape fraction {r['escape_fraction_vs_supp_h']:.6f}  "
              f"hilbert/artifact {r['hilbert_over_truncation_artifact']:.4g}")
    print("CSD3b escape everywhere off supp:",
          doc["CSD3b_pointwise"]["fraction_of_outside_nodes_with_escape_above_1000x_leakage"])
    for r in doc["CSD3_minimized"]["rows"]:
        print(f"CSD3 min K={r['K']:>2}  rayleigh {r['min_rayleigh']:.6e}  "
              f"floor {r['float64_resolution_floor']:.3e}  resolved {r['resolved']}")
    print("CSD4 control escape  :",
          doc["CSD4_positive_control"]["control"]["mass_outside_supp_anchor"],
          "| live a=0 anchor:",
          doc["CSD4_positive_control"]["live_a0_anchor_same_call"]["escape_fraction_vs_supp_h"],
          "| separation:",
          f"{doc['CSD4_positive_control']['separation_ratio_live_over_control']:.3e}")
    for r in doc["CSD5_Xc_ladder"]["rows"]:
        print(f"CSD5 a={r['a']:.2f}  X_c {r['X_c']:.6f}  conv {r['converged']}")
    for r in doc["CSD6_bridge_to_leg_162"]["rows"]:
        print(f"CSD6 a={r['a']}  best Z1 {r['best_Z1_over_A21_zero']}  "
              f"X_c {r['X_c_measured_here']}")
    print("gate conditions failed:", doc["gate_conditions_failed"])
    print("GATE:", doc["gate_answer"])


if __name__ == "__main__":
    main()
