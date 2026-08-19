#!/usr/bin/env python3
"""Leg 409, unit `L-JVER` -- QUARANTINED BLACK-BOX DRIVER over `L6`'s own code.

This file exists for one reason: the artefact `writeup/data/p2_route_l6_profile_v1.json`
banks `J_L6` at exactly TWO points (branch A and branch B at `n_dof = 6720`) and banks NO
coefficient vector at any coarser rung.  The gate this unit must answer needs `J_L6` at a
non-minimiser and at all five rungs, so those numbers are produced HERE by running
`experiments/p2_route_l6_v1.py` AS A BLACK BOX -- imported, called, never read from and
never modified.

QUARANTINE.  `experiments/p2_route_ljver_v1.py` -- the independent implementation -- does
not import this file and does not import `p2_route_l6_v1`.  This file was committed AFTER
that one (`3229516`), so the git history witnesses that the independent implementation was
not tuned to any number produced here.

It also runs the closed-form control X1 THROUGH `L6`'s machinery, which the self-tests in
`L6` do not do: `L6`'s `T_C`/`T_D` compare `L6` against `L6`.

    Phi(y) = e^{-|y|^2/2} (zhat x y) = curl(psi y),  psi = z e^{-|y|^2/2}
           => in `L6`'s poloidal-toroidal variables this is F == 0 and
              Q(r) = sqrt(4 pi / 3) r e^{-r^2/2} in the (l, m) = (1, 0) slot,
      curl Phi = e^{-|y|^2/2} (y1 y3, y2 y3, 2 - y1^2 - y2^2)      [closed form, by hand]
    Psi(y) = e^{-|y|^2/2} zhat,  ||Psi||_{L3/2(R^3)} = 4 pi / 3    [closed form, by hand]

NO NUMBER PRODUCED HERE IS EVIDENCE ABOUT THE MATHEMATICS.  It is evidence about a program.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import p2_route_l6_v1 as L6                      # noqa: E402  -- BLACK BOX, never read from

ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"
RUNGS = [("J0", 2, 8, 1), ("J1", 2, 12, 1), ("J2", 3, 12, 2),
         ("J3", 3, 16, 2), ("J4", 4, 20, 3)]


def geom(Lmax, Nr, Ks):
    return L6.Geom(Lmax, Nr, Ks)


def J_l6(g, x, branch):
    """Value only.  `objective` returns (value, gradient); the gradient is discarded."""
    v, _ = L6.objective(g, np.asarray(x, float), branch)
    return float(v)


def sigma_l6(g):
    """`L6`'s own column scaling, for the convention comparison (ceiling C-6)."""
    return 1.0 / g.scaleF, 1.0 / g.scaleQ


def control_X1_l6(g):
    """Closed-form curl and closed-form L^{3/2} norm, THROUGH `L6`'s own operators."""
    r = g.r
    nH, nq, ns = g.nH, g.nq_r, g.ns
    h10 = [i for i, (l, m) in enumerate(g.harm) if (l, m) == (1, 0)]
    if not h10:
        raise RuntimeError("(1,0) harmonic absent")
    h10 = h10[0]

    C = math.sqrt(4.0 * math.pi / 3.0)
    e = np.exp(-r ** 2 / 2.0)
    Q0 = C * r * e
    Q1 = C * e * (1.0 - r ** 2)
    Q2 = C * e * r * (r ** 2 - 3.0)
    Q3 = C * e * (3.0 + r ** 2 * (-6.0 + r ** 2))
    F = [np.zeros((nH, nq, ns)) for _ in range(5)]
    Q = [np.zeros((nH, nq, ns)) for _ in range(4)]
    for k, arr in enumerate((Q0, Q1, Q2, Q3)):
        Q[k][h10, :, :] = arr[:, None]

    Vc, _ = L6._vsh_V(g, F, Q)
    wc, _ = L6._vsh_w(g, F, Q)
    V = L6._synth(g, Vc)                          # (nq_r, ns, nP, 3)
    W = L6._synth(g, wc)

    y = g.r[:, None, None] * g.er[None, None, :, :]     # (nq_r, 1, nP, 3)
    ey = np.exp(-(y ** 2).sum(axis=-1) / 2.0)
    V_closed = np.stack([-ey * y[..., 1], ey * y[..., 0], np.zeros_like(ey)], axis=-1)
    curl_closed = np.stack([ey * y[..., 0] * y[..., 2],
                            ey * y[..., 1] * y[..., 2],
                            ey * (2.0 - y[..., 0] ** 2 - y[..., 1] ** 2)], axis=-1)
    sel = (g.r > 1e-3) & (g.r < 8.0)
    Vrel = float(np.max(np.abs(V[sel] - V_closed[sel])) / np.max(np.abs(V_closed[sel])))
    Wrel = float(np.max(np.abs(W[sel] - curl_closed[sel]))
                 / np.max(np.abs(curl_closed[sel])))

    Wtest = np.zeros((nq, ns, g.nP, 3))
    Wtest[..., 2] = np.exp(-(g.r ** 2) / 2.0)[:, None, None]
    Jt = L6.load_bearing_norm(g, Wtest)
    exact = L6.PERIOD * 4.0 * math.pi / 3.0
    return dict(V_vs_closed_form_rel=Vrel,
                curl_vs_closed_form_rel=Wrel,
                norm_value=float(Jt), norm_exact=exact,
                norm_rel_err=abs(float(Jt) - exact) / exact)


def restrict_box(x, Lmax, Nr, Ks, Lt, Nt, Kt, out_space=None):
    """Zero everything outside a coarser rung's index box; optionally re-express it there."""
    nH = Lmax * (Lmax + 2)
    nK = 2 * Ks + 1
    harm = [(l, m) for l in range(1, Lmax + 1) for m in range(-l, l + 1)]
    aF = np.asarray(x[:nH * Nr * nK], float).reshape(nH, Nr, nK).copy()
    aQ = np.asarray(x[nH * Nr * nK:], float).reshape(nH, Nr, nK).copy()
    keep = np.array([l <= Lt for (l, m) in harm])
    aF[~keep] = 0.0
    aQ[~keep] = 0.0
    aF[:, Nt:, :] = 0.0
    aQ[:, Nt:, :] = 0.0
    aF[:, :, 2 * Kt + 1:] = 0.0
    aQ[:, :, 2 * Kt + 1:] = 0.0
    if out_space is None:
        return np.concatenate([aF.ravel(), aQ.ravel()])
    nHt = Lt * (Lt + 2)
    bF = aF[:nHt, :Nt, :2 * Kt + 1]
    bQ = aQ[:nHt, :Nt, :2 * Kt + 1]
    return np.concatenate([bF.ravel(), bQ.ravel()])


def main():
    doc = json.load(open(ART))
    out = {"what": "quarantined black-box reference values from experiments/p2_route_l6_v1.py",
           "class": "recompute-from-primary (L6's own code re-executed), NOT re-read-own-artefact"}

    gJ4 = geom(4, 20, 3)
    out["control_X1_through_L6"] = control_X1_l6(gJ4)
    print("X1 through L6:", out["control_X1_through_L6"], flush=True)

    sF, sQ = sigma_l6(gJ4)
    out["sigmaF_L6"] = sF.tolist()
    out["sigmaQ_L6"] = sQ.tolist()

    xB = np.array(doc["banked_profile"]["B"]["coefficients"])
    xA = np.array(doc["banked_profile"]["A"]["coefficients"])

    # -- the two banked points, RE-EXECUTED (not re-read) ---------------------------------
    out["P1_bankedB_J4"] = J_l6(gJ4, xB, "B")
    out["P2_bankedA_J4"] = J_l6(gJ4, xA, "A")
    print("P1 recomputed:", out["P1_bankedB_J4"], flush=True)
    print("P2 recomputed:", out["P2_bankedA_J4"], flush=True)

    # -- P3: the J0 index box of banked B, held in the n_dof = 6720 space -----------------
    xP3 = restrict_box(xB, 4, 20, 3, 2, 8, 1)
    out["P3_J0box_of_B_in_6720"] = J_l6(gJ4, xP3, "B")
    print("P3:", out["P3_J0box_of_B_in_6720"], flush=True)

    # -- P4: a deterministic pseudo-random point, seed 409 --------------------------------
    xP4 = np.random.default_rng(409).standard_normal(gJ4.n_dof) * 0.3
    out["P4_random_seed409"] = J_l6(gJ4, xP4, "B")
    print("P4:", out["P4_random_seed409"], flush=True)

    # -- the five rungs: the same vector restricted and re-expressed in each rung ---------
    rung = {}
    for name, Lm, Nr, Ks in RUNGS:
        g = geom(Lm, Nr, Ks)
        xr = restrict_box(xB, 4, 20, 3, Lm, Nr, Ks, out_space=True)
        rung[name] = {"Lmax": Lm, "Nr": Nr, "Ks": Ks, "n_dof": int(g.n_dof),
                      "J_L6": J_l6(g, xr, "B")}
        print(name, rung[name], flush=True)
    out["rungs"] = rung

    dest = ROOT / "writeup" / "data" / "p2_route_ljver_v1_ref.json"
    dest.write_text(json.dumps(out, indent=1))
    print("wrote", dest)


if __name__ == "__main__":
    main()
