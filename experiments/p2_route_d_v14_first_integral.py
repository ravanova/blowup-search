"""Route-D v14: the first integral, and the kill switch it makes cheap.

Deterministic scoping probe -- NOT a logged gate run, no predicate lock needed.

    .venv/bin/python -u experiments/p2_route_d_v14_first_integral.py

Writes writeup/data/p2_route_d_v14_first_integral.json, from which
writeup/4_p2_lottery/p2_route_d_v14_evidence.py rebuilds fig32 with no re-runs.

Five blocks:
  A  the identity |Omega| = C E^{1/a} on an INDEPENDENT whole-line build (J-ladder)
     plus its exact a -> 0 limit against the anchor
  B  the profile on its own support: shape, edge exponent, edge amplitude
  C  THE KILL SWITCH -- ||A|| against the number of modes, with v12's whole-line
     J-ladder alongside it as the control
  D  X_c(a) against the far-field law evaluated with the profile's OWN (m, U_0)
  E  large-a K-convergence (what it does to v11's reading of a*)

Runtime ~6 min, dominated by the whole-line control in block C.
"""

import json
import sys
from os.path import abspath, dirname

import numpy as np

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from solver.collocation_newton import ACollocation                    # noqa: E402
from solver.first_integral import (ReducedProfile, anchor_limit,      # noqa: E402
                                   first_integral_defect)
from solver.turning_point import graded_norm_by_radius                 # noqa: E402

OUT = (dirname(dirname(abspath(__file__)))
       + "/writeup/data/p2_route_d_v14_first_integral.json")


def block_a():
    """The identity, on a discretization that knows nothing about it."""
    print("\n[A] the first integral on the whole-line build")
    rows = {}
    for a in (0.2, 0.3):
        devs, res, Js = [], [], (200, 400, 800, 1600)
        for J in Js:
            col = ACollocation(J=J, a=a)
            r = col.newton_gauged(c=0.5, tol=1e-14)
            om = r["Omega"]
            mask = (np.abs(om) > 1e-11) & (col.X > 0) & (col.X < 3.0)
            devs.append(first_integral_defect(om, col.V @ om, a, 0.5, mask))
            res.append(r["relres"])
            print(f"    a={a} J={J:5d}  defect {devs[-1]:.3e}  relres {res[-1]:.3e}")
        rows[str(a)] = {"J": list(Js), "defect": devs, "relres": res}
    X = np.linspace(0.0, 200.0, 40001)
    got, exact = anchor_limit(X, c=0.5)
    rows["anchor_limit_max_err"] = float(np.max(np.abs(got - exact)))
    print(f"    a->0 limit vs the exact anchor: {rows['anchor_limit_max_err']:.2e}")
    return rows


def block_b():
    """The profile on [0, X_c]: shape, edge exponent, edge amplitude."""
    print("\n[B] the profile on its own support")
    out = {"a": [], "Xc": [], "edge_exponent": [], "edge_amplitude": [],
           "v": np.linspace(0.0, 1.0, 401).tolist(), "Omega": {}}
    s = np.geomspace(1e-7, 1e-4, 60)
    for a in (0.25, 0.3, 0.4, 0.5, 0.8):
        rp = ReducedProfile(a, K=96)
        r = rp.solve(Xc0=10.0)
        assert r["converged"], (a, r)
        om_edge = np.abs(rp.omega_of(r["b"], 1.0 - s))
        q = float(np.polyfit(np.log(s), np.log(om_edge), 1)[0])
        out["a"].append(a)
        out["Xc"].append(r["Xc"])
        out["edge_exponent"].append(q)
        out["edge_amplitude"].append(rp.edge_amplitude(r["b"], r["Xc"]))
        out["Omega"][str(a)] = rp.omega_of(r["b"], np.asarray(out["v"])).tolist()
        print(f"    a={a}  X_c/c={r['Xc']:.6f}  edge exponent {q:.6f} "
              f"(1/a = {1/a:.6f})  amplitude {out['edge_amplitude'][-1]:.4e}"
              f"  Newton {r['iterations']} it, res {r['residual']:.1e}")
    return out


def block_c():
    """THE KILL SWITCH: ||A|| vs modes on [0, X_c], with the whole-line control."""
    print("\n[C] the kill switch")
    Ks = (16, 24, 32, 48, 64, 96, 128, 192)
    reduced = {}
    for a in (0.2, 0.3, 0.4, 0.5):
        ne, nO, ng = [], [], []
        for K in Ks:
            rp = ReducedProfile(a, K=K)
            r = rp.solve(Xc0=10.0)
            assert r["converged"], (a, K, r)
            ne.append(rp.operator_norm(r["b"], r["Xc"], measure="e"))
            nO.append(rp.operator_norm(r["b"], r["Xc"], measure="Omega"))
            ng.append(rp.operator_norm(r["b"], r["Xc"], measure="e", alpha=1.4))
        # the whole ladder, and the ladder over the RESOLVED range only: at small a
        # the support radius is ~e^{c/a} while the core stays O(1), so the first
        # one or two K are simply under-resolved and their slope is about that.
        fit = lambda K, y: float(np.polyfit(np.log(K), np.log(y), 1)[0])   # noqa: E731
        res = [i for i, K in enumerate(Ks) if K >= 48]
        reduced[str(a)] = {
            "K": list(Ks), "norm_e": ne, "norm_Omega": nO, "norm_graded": ng,
            "slope_e": fit(Ks, ne), "slope_Omega": fit(Ks, nO),
            "slope_graded": fit(Ks, ng),
            "K_resolved": [Ks[i] for i in res],
            "slope_e_resolved": fit([Ks[i] for i in res], [ne[i] for i in res]),
            "slope_graded_resolved": fit([Ks[i] for i in res], [ng[i] for i in res])}
        q = reduced[str(a)]
        print(f"    a={a}  ||A||_e " + " ".join(f"{x:.4f}" for x in ne)
              + f"   K^{q['slope_e']:+.4f}  (K>=48: K^{q['slope_e_resolved']:+.4f};"
              f"  graded alpha=1.4: K^{q['slope_graded_resolved']:+.4f})")

    # THE CONTROL, measured the way v12/v13 measured it -- the decay-graded norm of
    # solver/turning_point.graded_norm_by_radius at the operating grading alpha=1.4.
    # Anything else would be comparing two different objects and calling it a
    # contrast (banked lesson 29: a constant is attached to a point, and a norm).
    print("    control: whole-line gauged system, DECAY-GRADED (v12's object)")
    control = {}
    for a in (0.0, 0.2, 0.3):
        Js, ns, unw = (100, 200, 400, 800), [], []
        for J in Js:
            col = ACollocation(J=J, a=a)
            r = col.newton_gauged(c=0.5, tol=1e-14)
            g = graded_norm_by_radius(col, r["Omega"], 0.5, 1.4, cutoffs=(np.inf,))
            ns.append(g["by_cutoff"]["inf"])
            unw.append(g["unweighted_row_sum"])
        control[str(a)] = {"J": list(Js), "norm": ns, "unweighted": unw,
                           "slope": float(np.polyfit(np.log(Js), np.log(ns), 1)[0]),
                           "slope_unweighted": float(
                               np.polyfit(np.log(Js), np.log(unw), 1)[0])}
        print(f"      a={a}  graded " + " ".join(f"{x:.3e}" for x in ns)
              + f"   J^{control[str(a)]['slope']:+.3f}"
              + f"   (unweighted J^{control[str(a)]['slope_unweighted']:+.3f})")
    return {"reduced": reduced, "control": control}


def block_d():
    """X_c(a) against the far-field law with the profile's own (m, U_0)."""
    print("\n[D] the radius law, with the constants measured")
    out = {"a": [], "Xc": [], "m": [], "U0": [], "Xc_pred": []}
    for a in (0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1.0):
        K = 128 if a < 0.3 else 64
        rp = ReducedProfile(a, K=K)
        r = rp.solve(Xc0=10.0)
        assert r["converged"], (a, r)
        U0, m = rp.outer_velocity(r["b"], r["Xc"])
        pred = rp.predicted_radius(r["b"], r["Xc"])
        out["a"].append(a)
        out["Xc"].append(r["Xc"])
        out["m"].append(m)
        out["U0"].append(U0)
        out["Xc_pred"].append(pred)
        print(f"    a={a:4.2f}  X_c/c={r['Xc']:10.6f}  m={m:9.6f}  U_0={U0:9.6f}"
              f"  predicted {pred:10.6f}  ratio {pred/r['Xc']:.5f}")
    return out


def block_e():
    """K-convergence past a*, and what it says about v11's fourth confirmation."""
    print("\n[E] large-a K-convergence")
    out = {}
    for a in (0.5, 0.6, 0.8, 1.0, 1.2):
        row = []
        for K in (32, 64, 128, 192):
            r = ReducedProfile(a, K=K).solve(Xc0=4.0)
            row.append(r["Xc"] if r["converged"] else float("nan"))
        out[str(a)] = {"K": [32, 64, 128, 192], "Xc": row,
                       "spread": float(max(row[1:]) / min(row[1:]) - 1.0)}
        print(f"    a={a}: " + "  ".join(f"{x:.10g}" for x in row)
              + f"   spread over K>=64: {out[str(a)]['spread']:.1e}")
    return out


if __name__ == "__main__":
    data = {"note": "Route-D v14 -- first integral + kill switch. Plain float64, "
                    "nothing interval-enclosed, nothing rigorous. Level-1 tooling "
                    "plus a structural identity; NOT a certificate.",
            "A_identity": block_a(),
            "B_profile": block_b(),
            "C_kill_switch": block_c(),
            "D_radius_law": block_d(),
            "E_large_a": block_e()}
    with open(OUT, "w") as f:
        json.dump(data, f, indent=1)
    print("\nwrote " + OUT)
