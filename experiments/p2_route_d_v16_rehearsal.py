"""Route-D v16: the float rehearsal of the certificate in the reduced space.

Deterministic scoping probe -- NOT a logged gate run, no predicate lock needed.

    .venv/bin/python -u experiments/p2_route_d_v16_rehearsal.py

Writes writeup/data/p2_route_d_v16_rehearsal.json, from which
writeup/4_p2_lottery/p2_route_d_v16_evidence.py rebuilds fig33 with no re-runs.

Four blocks:
  A  Y_0 -- the interpolant defect vs K, with the nodal residual as the flat control
  B  the sup-norm obstruction: the ADVERSARY vs the NAIVE PROBE under quadrature
     refinement (one is real, one is the instrument)
  C  the Holder repair -- the same adversary against ||.||_gamma, gamma swept
  D  the nonlinearity: sup|N''| by edge cutoff across a, and the a <= 1/2 threshold

Runtime ~5 min.
"""

import json
import sys
from os.path import abspath, dirname

import numpy as np

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from solver.first_integral import ReducedProfile                        # noqa: E402
from solver.reduced_certificate import (holder_ratio, interpolant_defect,  # noqa: E402
                                        rehearsal, second_derivative_sup,
                                        step_adversary, z0_defect)

OUT = (dirname(dirname(abspath(__file__)))
       + "/writeup/data/p2_route_d_v16_rehearsal.json")


def block_a():
    print("\n[A] Y_0: the interpolant defect vs K")
    out = {}
    for a in (0.3, 0.4):
        Ks, defect, nodal, opn = (16, 24, 32, 48, 64, 96, 128), [], [], []
        for K in Ks:
            rp = ReducedProfile(a, K=K)
            r = rp.solve(Xc0=10.0)
            assert r["converged"], (a, K)
            defect.append(interpolant_defect(rp, r["b"], r["Xc"]))
            nodal.append(float(np.max(np.abs(rp.residual(r["b"], r["Xc"])))))
            opn.append(rp.operator_norm(r["b"], r["Xc"]))
            print(f"    a={a} K={K:4d}  off-node {defect[-1]:.3e}  "
                  f"nodal {nodal[-1]:.2e}  ||A|| {opn[-1]:.4f}")
        # fit only where the defect is above the float floor
        keep = [i for i, d in enumerate(defect) if d > 1e-11]
        slope = (float(np.polyfit(np.log([Ks[i] for i in keep]),
                                  np.log([defect[i] for i in keep]), 1)[0])
                 if len(keep) > 2 else float("nan"))
        out[str(a)] = {"K": list(Ks), "defect": defect, "nodal": nodal,
                       "opnorm": opn, "slope_above_floor": slope,
                       "K_above_floor": [Ks[i] for i in keep],
                       "predicted_slope": -(2.0 / a + 1.0)}
        print(f"    a={a}: K^{slope:+.2f} above the 1e-11 float floor "
              f"(the (1-v)^{{1/a}} branch predicts K^{-(2/a+1):+.2f})")
    return out


def block_b():
    print("\n[B] the sup-norm obstruction, and the instrument check")
    rules = [(20, 20), (20, 40), (24, 60), (30, 80)]
    out = {"rules": rules, "adversary": {}, "naive": {}}
    for kind, key in (("step", "adversary"), ("single", "naive")):
        for K in (64, 128, 256):
            row = [step_adversary(K, lv, od, kind=kind) for lv, od in rules]
            out[key][str(K)] = row
            print(f"    {key:9s} K={K:4d}: " + "  ".join(f"{x:8.4f}" for x in row))
    Ks = (8, 16, 32, 64, 128, 256)
    sup = [step_adversary(K, 24, 60, kind="step") for K in Ks]
    out["K"] = list(Ks)
    out["sup_ratio"] = sup
    out["sup_slope"] = float(np.polyfit(np.log(Ks), sup, 1)[0])
    print(f"    sup ratio " + " ".join(f"{x:.4f}" for x in sup)
          + f"   slope {out['sup_slope']:+.4f}/e-fold in log K")
    return out


def block_c():
    print("\n[C] the Holder repair")
    Ks = (8, 16, 32, 64, 128, 256)
    out = {"K": list(Ks), "gamma": {}}
    for g in (0.15, 0.25, 0.35, 0.5, 0.65, 0.85):
        row = [holder_ratio(K, g) for K in Ks]
        sl = float(np.polyfit(np.log(Ks), row, 1)[0])
        out["gamma"][str(g)] = {"ratio": row, "slope": sl}
        print(f"    gamma={g:4.2f}: " + " ".join(f"{x:.4f}" for x in row)
              + f"   slope {sl:+.4f}")
    return out


def block_d():
    print("\n[D] the nonlinearity: sup|N''| by edge cutoff")
    cuts = (1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 1e-10)
    out = {"cutoffs": list(cuts), "a": [], "rows": {}, "finite": {}}
    # Continuation in a.  The cold start (X_c0 = 10 at every a) converges at almost
    # every value but misses the basin at a = 0.7 -- reported rather than hidden,
    # because "the cold start always works" was a claim v14 made and it is not quite
    # true.  Walking X_c0 in from the previous a fixes it.
    prev = None
    for a in (0.2, 0.25, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8):
        rp = ReducedProfile(a, K=96)
        r = rp.solve(Xc0=10.0)
        if not r["converged"] and prev is not None:
            r = rp.solve(Xc0=prev)
            print(f"    (a={a}: cold start missed the basin; continuation from "
                  f"X_c0={prev:.4f} converged)")
        assert r["converged"], a
        prev = r["Xc"]
        row = second_derivative_sup(rp, r["b"], edge_cutoffs=cuts)
        out["a"].append(a)
        out["rows"][str(a)] = row
        out["finite"][str(a)] = bool(max(row) / min(row) < 1.001)
        print(f"    a={a:4.2f} (p-2={rp.p-2:+7.4f}): "
              + " ".join(f"{x:.3e}" for x in row)
              + ("   FINITE" if out["finite"][str(a)] else "   DIVERGENT"))
    return out


if __name__ == "__main__":
    data = {"note": "Route-D v16 -- the float rehearsal. Its headline is a NEGATIVE: "
                    "the sup-to-sup budget does NOT close, because H is unbounded on "
                    "sup even on a bounded interval, and separately sup|N''| is finite "
                    "only for a <= 1/2. Z_1 (the infinite-dimensional tail) is not "
                    "computed at all. Plain float64, nothing interval-enclosed, nothing "
                    "rigorous, NOT a certificate.",
            "A_Y0": block_a(),
            "B_sup_obstruction": block_b(),
            "C_holder_repair": block_c(),
            "D_nonlinearity": block_d(),
            "E_rehearsal": {str(a): rehearsal(a, K=96) for a in (0.3, 0.5, 0.8)}}
    for k, v in data["E_rehearsal"].items():
        v.pop("detail", None)
    with open(OUT, "w") as f:
        json.dump(data, f, indent=1)
    print("\nwrote " + OUT)
