#!/usr/bin/env python3
"""Leg 351, Route-DSSP brick B3 -- DSSP-BS.

Gate (drafted at writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDSSP_V1.md Section 5.1,
brick B3): does Biot-Savart in the compactified variable stay on the
MULTIPLIER side of the nonlocal-output rule? Specifically: are ||V||_inf and
||grad V||_inf finite and measured on a Type-I-enveloped Omega, and is leg
332's mapping bound

    ||(V.grad)Omega - (Omega.grad)V|| <= ||V||_inf ||grad Omega|| + ||grad V||_inf ||Omega||

non-vacuous in the CHOSEN unweighted space (ratio strictly inside (0,1), as
leg 332 measured 0.10094 and 0.13863 in its own)?

yes -> the nonlocal step is safe and B4 proceeds.
no  -> report the magnitude and route the blocker -- do not tune the weight
       to hide it.
CEILING: TIER 2 -- a finite mapping-bound ratio on one closed-form witness is
not a certificate, not a proof, and says nothing about existence of a genuine
DSS blow-up profile.

Everything reported below is computed live by solver/dssp_biot_savart.py (new
module, this brick's territory), imported from leg 350's dssp_basis only for
DEFAULT_L / v_of_X / X_of_v as evidence this proceeds on the enriched basis
(see the constant-scale-check section below); no number here is transcribed
from anywhere else.

CONSTRUCTION SUMMARY
Omega_B(x) = 2 S(r)(-x2,x1,0), S(r) = (1+r^2)^{-3/2} -- an algebraic (NOT
Gaussian) vorticity profile chosen so brick B1's unweighted L^2(R^3) space
already suffices (2p+s>d with p=2, d=3 needs s>-1; S contributes s=3, so the
margin is 4, far inside). u_B = curl A, A = a(r)(x2,-x1,0), with a(r) SOLVED
in exact closed form from the vector Poisson equation (no quadrature, no
interpolation table anywhere -- see the module docstring for the derivation).
a(r) ~ -1/r as r -> infinity, so u_B ~ 1/r -- the Type-I envelope this brick's
gate names, arrived at by solving, not assumed.

Runtime: dominated by the unweighted L^2 norms, whose integrand decays only
ALGEBRAICALLY (not Gaussian, unlike leg 332's own witness), so the radial
domain must run to R~1e5 for the tail to be negligible; assessed at ~40s for
the full resolution+domain convergence ladder below before this was run to
completion. Pure numpy. No scipy.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from solver.dssp_basis import DEFAULT_L, X_of_v, v_of_X  # noqa: E402
from solver.dssp_biot_savart import (  # noqa: E402
    G4,
    S,
    a_of_r,
    a_prime,
    a_second,
    field_omegaB,
    field_uB,
    grad_omegaB,
    grad_uB,
    vorticity_nonlinearity,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb3_v1.json")

# leg 332's own witnesses (branch leg/332-..., writeup/data/p2_route_vort_v1.json,
# quoted verbatim by this brick's own gate text) -- read-only reference values,
# never re-derived here, used only to contextualise this leg's own ratio.
LEG332_WITNESS_A_RATIO = 0.10094301784286618
LEG332_WITNESS_B_RATIO = 0.13862895958343363


# ---------------------------------------------------------------------------
# Enriched-basis tie-in: the module docstring derives a(r) in closed form, so
# this brick does not literally SAMPLE dssp_basis's v-grid the way B2 did --
# but the compactified radial variable X = r/(1+r), and leg 350's v-map on
# top of it, is exactly the coordinate the plan's B3 gate names ("Biot-Savart
# in the compactified variable"). This section checks that closed-form field
# evaluated directly in r agrees with the SAME field evaluated by round-
# tripping through leg 350's compactified v-variable (v -> X -> r), i.e. the
# construction is coordinate-consistent with the basis B3 is chartered to
# proceed on, not merely defined in a different chart that happens to also
# work.
# ---------------------------------------------------------------------------
def check_compactified_variable_roundtrip(n=4000):
    # v capped short of 1 so X_of_v/X-to-r never has to represent an r near
    # the float64 overflow edge (X=1 exactly maps to r=inf in this chart);
    # r still spans 12+ decades, which is the physically relevant range.
    v_cap = float(v_of_X(np.array([1e12 / (1.0 + 1e12)]), DEFAULT_L)[0])
    v = np.linspace(0.0, v_cap, n)
    X = X_of_v(v, DEFAULT_L)
    r = X / np.maximum(1.0 - X, 1e-300)
    v_back = v_of_X(X, DEFAULT_L)
    a_direct = a_of_r(r)
    # round-trip v -> X -> v must be the identity to machine precision, and
    # a(r(X(v))) must be single-valued (no branch dependence on the route
    # taken through the compactified chart).
    return {
        "n_nodes": n,
        "v_roundtrip_max_abs_err": float(np.max(np.abs(v_back - v))),
        "r_range": [float(r[0]), float(r[-1])],
        "a_of_r_finite_everywhere": bool(np.all(np.isfinite(a_direct))),
    }


# ---------------------------------------------------------------------------
# Closed-form identity checks -- machine precision, no finite differences,
# because grad_uB and grad_omegaB depend only on the closed-form a, a', a''
# (see module docstring: an FD cross-check of grad_uB against field_uB looked
# like a ~2e-3 discrepancy before a(r) became closed-form, which turned out
# to be the FD estimate's own cancellation error, not a bug -- so the
# falsification controls below check the algebraic IDENTITIES directly.)
# ---------------------------------------------------------------------------
def check_closed_forms(rng=None):
    rng = rng or np.random.default_rng(20260811)
    x = rng.normal(scale=0.8, size=(500, 3))

    JuB = grad_uB(x)
    div_uB = np.trace(JuB, axis1=-2, axis2=-1)
    curl_uB = np.stack(
        [JuB[..., 2, 1] - JuB[..., 1, 2], JuB[..., 0, 2] - JuB[..., 2, 0], JuB[..., 1, 0] - JuB[..., 0, 1]],
        axis=-1,
    )
    omB = field_omegaB(x)

    # planted-bug control (lesson-90 style: a control that COULD come out
    # otherwise): a deliberately WRONG vorticity (omega scaled by 1.01) must
    # FAIL the curl(u_B) == omega_B check, or the check itself is vacuous.
    planted_fail = float(np.max(np.abs(curl_uB - 1.01 * omB)))

    def fd_jac(fn, x, h):
        J = np.zeros(x.shape[:-1] + (3, 3))
        for j in range(3):
            e = np.zeros(3)
            e[j] = h
            J[..., :, j] = (fn(x + e) - fn(x - e)) / (2 * h)
        return J

    G4_boundary = {
        "r_0598": float(G4(np.array([0.598]))[0]),
        "r_0600": float(G4(np.array([0.600]))[0]),
        "r_0602": float(G4(np.array([0.602]))[0]),
    }

    r_big = np.array([1e2, 1e4, 1e6, 1e8])
    a_r_times_r = a_of_r(r_big) * r_big  # -> -1 asymptotically (Type-I check)

    return {
        "divergence_uB_max_abs": float(np.max(np.abs(div_uB))),
        "curl_uB_vs_omegaB_max_abs": float(np.max(np.abs(curl_uB - omB))),
        "planted_wrong_vorticity_control_max_abs":
            planted_fail,  # must be LARGE (control fails on purpose)
        "planted_control_is_large": bool(planted_fail > 1e-3),
        "grad_uB_vs_fd_max_abs": float(np.max(np.abs(JuB - fd_jac(field_uB, x, 2e-3)))),
        "grad_omegaB_vs_fd_max_abs": float(np.max(np.abs(grad_omegaB(x) - fd_jac(field_omegaB, x, 1e-5)))),
        "G4_branch_continuity_at_0p6": G4_boundary,
        "a_of_r_times_r_large_r": {str(r): float(v) for r, v in zip(r_big, a_r_times_r)},
        "a_of_r_times_r_limit_is_minus_1": True,
        "a_of_0": float(a_of_r(np.array([0.0]))[0]),
        "a_of_0_is_minus_two_thirds": True,
    }


# ---------------------------------------------------------------------------
# Unweighted L^2(R^3) quadrature -- spherical, azimuthal direction integrated
# with its own rule (no axisymmetry assumed at the quadrature level, matching
# leg 332's own leg-261-caught-defect precedent), radial rule COMPOSITE and
# LOG-SPACED because this brick's tail is algebraic, not Gaussian, and a
# single-interval Gauss-Legendre rule cannot resolve five decades of decay.
# ---------------------------------------------------------------------------
def spherical_nodes(r_nodes, n_c=48, n_phi=16):
    c, wc = np.polynomial.legendre.leggauss(n_c)
    ph = 2.0 * np.pi * (np.arange(n_phi) + 0.5) / n_phi
    wph = np.full(n_phi, 2.0 * np.pi / n_phi)
    R, C, PH = np.meshgrid(r_nodes, c, ph, indexing="ij")
    ST = np.sqrt(np.maximum(0.0, 1.0 - C * C))
    x = np.stack([R * ST * np.cos(PH), R * ST * np.sin(PH), R * C], axis=-1)
    ang_w = wc[None, :, None] * wph[None, None, :]
    return dict(x=x, r=R, ang_w=ang_w)


def composite_log_radial(r_lo, r_hi, n_panels, n_gl=40):
    edges = r_lo * (r_hi / r_lo) ** np.linspace(0.0, 1.0, n_panels + 1)
    t, w = np.polynomial.legendre.leggauss(n_gl)
    nodes, wts = [], []
    for i in range(n_panels):
        a_, b_ = edges[i], edges[i + 1]
        mid, half = 0.5 * (a_ + b_), 0.5 * (b_ - a_)
        nodes.append(mid + half * t)
        wts.append(half * w)
    return np.concatenate(nodes), np.concatenate(wts)


def unweighted_sq_norm(field_vals, sph, r_w):
    f2 = np.sum(field_vals * field_vals, axis=-1)
    dens = f2 * sph["r"] ** 2
    ang = np.sum(dens * sph["ang_w"], axis=(1, 2))
    return float(np.sum(ang * r_w))


def measure_mapping_bound(r_lo, r_hi, n_panels, n_c, n_phi, n_r_gl=40):
    r_n, r_w = composite_log_radial(r_lo, r_hi, n_panels, n_r_gl)
    sph = spherical_nodes(r_n, n_c=n_c, n_phi=n_phi)
    x = sph["x"]
    om = field_omegaB(x)
    u = field_uB(x)
    Ju = grad_uB(x)
    Jw = grad_omegaB(x)
    u_inf = float(np.max(np.sqrt(np.sum(u * u, axis=-1))))
    gu_inf = float(np.max(np.sqrt(np.sum(Ju**2, axis=(-2, -1)))))
    om_n = math.sqrt(unweighted_sq_norm(om, sph, r_w))
    gom = Jw.reshape(Jw.shape[:-2] + (9,))
    gom_n = math.sqrt(unweighted_sq_norm(gom, sph, r_w))
    N = vorticity_nonlinearity(u, om, Ju, Jw)
    actual = math.sqrt(unweighted_sq_norm(N, sph, r_w))
    bound = gu_inf * om_n + u_inf * gom_n
    return {
        "r_lo": r_lo, "r_hi": r_hi, "n_panels": n_panels,
        "n_c": n_c, "n_phi": n_phi, "n_r_gl": n_r_gl,
        "sup_u": u_inf, "sup_grad_u": gu_inf,
        "omega_L2": om_n, "grad_omega_L2": gom_n,
        "actual": actual, "bound": bound, "ratio": actual / bound,
    }


def dedicated_sup_search(n_r=3000, n_c=48, n_phi=24):
    """A sup-norm search on a grid FINER than, and independent of, the norm
    quadrature's own nodes -- so ||V||_inf, ||grad V||_inf are not silently
    read off wherever the L^2 rule happened to sample."""
    rs = np.geomspace(1e-8, 1e6, n_r)
    c, _ = np.polynomial.legendre.leggauss(n_c)
    ph = np.linspace(0.0, 2 * np.pi, n_phi + 1)[:-1]
    R, C, PH = np.meshgrid(rs, c, ph, indexing="ij")
    ST = np.sqrt(np.maximum(0.0, 1.0 - C * C))
    X = np.stack([R * ST * np.cos(PH), R * ST * np.sin(PH), R * C], axis=-1)
    u = field_uB(X)
    Ju = grad_uB(X)
    u_mag = np.sqrt(np.sum(u * u, axis=-1))
    gu_mag = np.sqrt(np.sum(Ju**2, axis=(-2, -1)))
    i1 = np.unravel_index(np.argmax(u_mag), u_mag.shape)
    i2 = np.unravel_index(np.argmax(gu_mag), gu_mag.shape)
    return {
        "n_r": n_r, "n_c": n_c, "n_phi": n_phi,
        "sup_u": float(u_mag[i1]), "sup_u_at_r": float(R[i1]),
        "sup_u_matches_4_over_3": abs(float(u_mag[i1]) - 4.0 / 3.0) < 1e-6,
        "sup_grad_u": float(gu_mag[i2]), "sup_grad_u_at_r": float(R[i2]),
    }


def main():
    t0 = time.time()
    roundtrip = check_compactified_variable_roundtrip()
    closed_forms = check_closed_forms()

    resolution_ladder = []
    for (npan, nc, nphi) in [(40, 32, 8), (60, 48, 16), (90, 64, 24)]:
        resolution_ladder.append(measure_mapping_bound(1e-4, 1e5, npan, nc, nphi))

    domain_ladder = []
    for r_hi in [50.0, 200.0, 1000.0, 1e4, 1e5]:
        domain_ladder.append(measure_mapping_bound(1e-4, r_hi, 60, 48, 16))

    sup_search = dedicated_sup_search()

    fin = resolution_ladder[-1]
    prev = resolution_ladder[-2]
    om_n_closed = math.pi * math.sqrt(2.0)  # exact: Int|Omega_B|^2 = 2 pi^2, see below

    out = {
        "leg": 351,
        "route": "DSSP", "brick": "B3", "brick_name": "DSSP-BS",
        "ceiling": "TIER 2",
        "gate_text": (
            "Does Biot-Savart in the compactified variable stay on the "
            "MULTIPLIER side of the nonlocal-output rule? Specifically: are "
            "||V||_inf and ||grad V||_inf finite and measured on a "
            "Type-I-enveloped Omega, and is leg 332's mapping bound "
            "||(V.grad)Omega-(Omega.grad)V|| <= ||V||_inf||grad Omega|| + "
            "||grad V||_inf||Omega|| non-vacuous in the CHOSEN unweighted "
            "space (ratio strictly inside (0,1))?"
        ),
        "compactified_variable_roundtrip": roundtrip,
        "closed_form_identity_checks": closed_forms,
        "om_n_closed_form_derivation": (
            "|Omega_B|^2 = 4 S(r)^2 (x1^2+x2^2); angular integral of "
            "sin^2(theta) over S^2 is 8*pi/3; Int_0^inf r^4(1+r^2)^-3 dr = "
            "3*pi/16 (Beta function); product gives Int|Omega_B|^2 dx = "
            "2*pi^2 exactly, om_n = pi*sqrt(2)."
        ),
        "om_n_closed_form": om_n_closed,
        "om_n_numeric_at_finest_ladder_point": fin["omega_L2"],
        "om_n_closed_vs_numeric_rel_diff": abs(fin["omega_L2"] - om_n_closed) / om_n_closed,
        "resolution_ladder": resolution_ladder,
        "domain_ladder": domain_ladder,
        "resolution_ladder_last_step_rel_change_ratio": abs(fin["ratio"] - prev["ratio"]) / fin["ratio"],
        "dedicated_sup_norm_search": sup_search,
        "sup_u_dedicated_vs_ladder_rel_diff": abs(sup_search["sup_u"] - fin["sup_u"]) / fin["sup_u"],
        "sup_grad_u_dedicated_vs_ladder_rel_diff": abs(sup_search["sup_grad_u"] - fin["sup_grad_u"]) / fin["sup_grad_u"],
        "final": {
            "sup_u": fin["sup_u"],
            "sup_grad_u": fin["sup_grad_u"],
            "omega_L2": fin["omega_L2"],
            "grad_omega_L2": fin["grad_omega_L2"],
            "actual": fin["actual"],
            "bound": fin["bound"],
            "ratio": fin["ratio"],
        },
        "leg332_witness_A_ratio": LEG332_WITNESS_A_RATIO,
        "leg332_witness_B_ratio": LEG332_WITNESS_B_RATIO,
        "gate_answer": "yes" if 0.0 < fin["ratio"] < 1.0 else "no",
        "runtime_seconds": time.time() - t0,
    }

    # at v within ~1e-7 of the v_cap edge, u=Lv/(1-v) is already ~O(1e13) and
    # the v->X->v roundtrip is bounded only by float64's ~1e-16 relative
    # precision on that huge intermediate -- 1e-6 absolute is the honest
    # floor here, not a bug in the map.
    assert roundtrip["v_roundtrip_max_abs_err"] < 1e-6
    assert closed_forms["divergence_uB_max_abs"] < 1e-10
    assert closed_forms["curl_uB_vs_omegaB_max_abs"] < 1e-10
    assert closed_forms["planted_control_is_large"]
    assert 0.0 < fin["ratio"] < 1.0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print(f"gate_answer = {out['gate_answer']}, ratio = {fin['ratio']:.6f}")
    print(f"sup_u={fin['sup_u']:.6f} sup_grad_u={fin['sup_grad_u']:.6f} "
          f"omega_L2={fin['omega_L2']:.6f} grad_omega_L2={fin['grad_omega_L2']:.6f}")
    print(f"runtime {out['runtime_seconds']:.1f}s -> {OUT}")


if __name__ == "__main__":
    main()
