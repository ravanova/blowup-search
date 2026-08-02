"""Route-E v1: the spectrum of the dynamically-rescaled gCLM flow at its self-similar
fixed point -- the cheapest experiment that can open or close the Hopf route into the
DSS lane.

THE QUESTION.  A DSS blow-up is a PERIODIC ORBIT of the rescaled flow.  The cheapest
way for one to exist near the objects this project already has is a HOPF BIFURCATION
off the self-similar fixed point: a complex pair of eigenvalues crossing the
imaginary axis as `a` moves.  This script asks whether the gCLM self-similar branch
has any eigenvalue capable of doing that.

SEVEN MEASUREMENTS (each written down before it was run):
  E1  the exact a = 0 anchor and its analytically known spectrum;
  E2  the branch: alpha(a) = -c_omega(a), the far-field decay exponent, with a
      K-ladder and Richardson extrapolation;
  E3  the ANALYTIC RESONANCE at a = 1/2 (alpha = 3 exactly) against the algebraic
      convergence at generic a -- the reason quantitative claims are quoted there;
  E4  the two structural identities L(X Omega_X) = 0 and L(Omega) = -Omega + X Omega_X;
  E5  the converged spectrum vs a, with the tolerance ladder that makes "exactly two"
      a robust statement rather than a choice of cut;
  E6  the POSITIVE CONTROL: plant a bound state and check the filter finds it,
      including in the right half plane;
  E7  where the branch ends.

Deterministic, NOT logged (no GA, no stochasticity).  Writes
writeup/data/p2_route_e_v1_spectrum.json.

Run: .venv/bin/python -u experiments/p2_route_e_v1_spectrum.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.rescaled_spectrum import (  # noqa: E402
    OddCompactBasis, RescaledFlow, continuation, converged_spectrum,
    match_filter, planted_eigenvalue_control, spectrum,
)

OUT = ROOT / "writeup" / "data" / "p2_route_e_v1_spectrum.json"


def jl(x):
    """JSON-safe complex list."""
    return [[float(np.real(z)), float(np.imag(z))] for z in np.atleast_1d(x)]


# --------------------------------------------------------------------------
def e1_anchor():
    """E1: the exact a = 0 fixed point, and the two analytically known eigenvalues."""
    print("\n[E1] the a = 0 anchor")
    rows = []
    for K in [16, 32, 64, 128]:
        f = RescaledFlow(0.0, K=K)
        b = f.B.anchor()
        res = float(np.max(np.abs(f.residual(b))))
        ev = np.linalg.eigvals(f.generator(b))
        d0 = float(np.min(np.abs(ev)))
        d1 = float(np.min(np.abs(ev + 1.0)))
        off = ev[np.abs(ev.real) > 1e-9]
        rows.append({"K": K, "residual": res, "dist_to_0": d0, "dist_to_m1": d1,
                     "n_off_axis": int(off.size),
                     "max_abs_re_on_axis": float(np.max(np.abs(
                         ev[np.abs(ev.real) <= 1e-9].real))) if ev.size else 0.0,
                     "max_abs_im": float(np.max(np.abs(ev.imag)))})
        print("   K=%4d  |R|=%.2e  dist(0)=%.2e  dist(-1)=%.2e  off-axis=%d"
              % (K, res, d0, d1, off.size))
    return rows


def e2_branch(a_values, Ks=(64, 128, 256), da=0.02):
    """E2: alpha(a) = -c_omega(a) with a K-ladder; Richardson where it is clean."""
    print("\n[E2] the branch: alpha(a) = -c_omega(a)")
    rows = []
    for a in a_values:
        entry = {"a": float(a), "K": list(Ks), "c_omega": [], "residual": [],
                 "tail": []}
        for K in Ks:
            _, out = continuation(a, K=K, da=da)
            entry["c_omega"].append(out["c_omega"])
            entry["residual"].append(out["residual"])
            entry["tail"].append(out["tail"])
        c = np.array(entry["c_omega"])
        # fitted order from the triple, then Richardson to that order
        if c.size >= 3 and abs(c[1] - c[0]) > 1e-15 and abs(c[2] - c[1]) > 1e-15:
            ratio = (c[1] - c[0]) / (c[2] - c[1])
            p = float(np.log2(abs(ratio))) if abs(ratio) > 1 else float("nan")
            entry["order"] = p
            entry["c_omega_rich"] = float(c[2] + (c[2] - c[1]) / (2.0 ** p - 1.0)) \
                if np.isfinite(p) and p > 0.05 else float(c[2])
        else:
            entry["order"] = float("nan")
            entry["c_omega_rich"] = float(c[-1])
        entry["alpha"] = -entry["c_omega_rich"]
        rows.append(entry)
        print("   a=%.3f  c_omega(K) = %s  order=%.2f  alpha=%.6f  res=%.1e"
              % (a, " ".join("%.7f" % v for v in c), entry["order"],
                 entry["alpha"], entry["residual"][-1]))
    return rows


def e3_resonance(Ks=(16, 32, 64, 128, 192, 256)):
    """E3: spectral convergence at a = 1/2 vs algebraic at a = 0.3."""
    print("\n[E3] the analytic resonance at a = 1/2")
    out = {}
    for a in (0.3, 0.5):
        cs, rs = [], []
        for K in Ks:
            _, o = continuation(a, K=K, da=0.02)
            cs.append(o["c_omega"])
            rs.append(o["residual"])
            print("   a=%.2f K=%4d  c_omega=%.12f  |R|=%.3e" % (a, K, o["c_omega"], o["residual"]))
        out["a=%.2f" % a] = {"K": list(Ks), "c_omega": cs, "residual": rs}
    # a fine scan for the dip, at one resolution
    print("   fine scan for residual dips (K=192):")
    scan_a, scan_r, scan_c = [], [], []
    K = 192
    flow = RescaledFlow(0.0, K=K)
    b = flow.B.anchor()
    for a in np.arange(0.0, 0.6201, 0.01):
        flow = RescaledFlow(a, K=K)
        o = flow.newton(b0=b)
        b = o["b"]
        scan_a.append(float(a))
        scan_r.append(o["residual"])
        scan_c.append(o["c_omega"])
    out["scan"] = {"a": scan_a, "residual": scan_r, "c_omega": scan_c, "K": K}
    i = int(np.argmin(scan_r[1:])) + 1
    print("      deepest dip (excluding a=0) at a=%.3f, |R|=%.2e, c_omega=%.10f"
          % (scan_a[i], scan_r[i], scan_c[i]))
    return out


def e4_structural(a_values, K=144, da=0.02):
    """E4: gate the two exact identities that produce lambda = 0 and lambda = -1."""
    print("\n[E4] the structural pair, gated")
    rows = []
    for a in a_values:
        flow, out = continuation(a, K=K, da=da)
        d_dil, d_amp = flow.structural_pair_defect(out["b"])
        rows.append({"a": float(a), "K": K, "dilation_defect": d_dil,
                     "amplitude_defect": d_amp, "residual": out["residual"]})
        print("   a=%.2f  |L(X Om_X)|/|X Om_X| = %.2e   |L(Om)+Om-X Om_X|/|Om| = %.2e"
              "   (fixed-point residual %.1e)" % (a, d_dil, d_amp, out["residual"]))
    return rows


def e5_sweep(a_values, K_coarse=96, K_fine=144, tols=(1e-4, 1e-3, 1e-2, 1e-1),
             da=0.02):
    """E5: the converged spectrum vs a, with a tolerance ladder."""
    print("\n[E5] the converged spectrum vs a")
    rows = []
    for a in a_values:
        ev_c, _, out_c = spectrum(a, K_coarse, da=da)
        ev_f, _, out_f = spectrum(a, K_fine, da=da)
        counts, keeps = {}, {}
        for t in tols:
            kept, dist = match_filter(ev_c, ev_f, t)
            counts["%g" % t] = int(kept.size)
            keeps["%g" % t] = jl(kept)
        kept_ref, dist_ref = match_filter(ev_c, ev_f, 1e-2)
        n_unstable = int(np.sum(np.real(kept_ref) > 1e-3))
        rows.append({"a": float(a), "counts": counts, "kept": keeps,
                     "kept_ref": jl(kept_ref),
                     "dist_ref": [float(d) for d in dist_ref],
                     "n_unstable_converged": n_unstable,
                     "residual_coarse": out_c["residual"],
                     "residual_fine": out_f["residual"],
                     "max_re_all_coarse": float(np.max(ev_c.real)),
                     "c_omega": out_f["c_omega"]})
        print("   a=%.2f  kept@(1e-4,1e-3,1e-2,1e-1) = %s   unstable-converged = %d"
              "   kept@1e-2: %s" % (a, [counts["%g" % t] for t in tols], n_unstable,
                                    " ".join("%+.5f%+.5fi" % (z.real, z.imag)
                                             for z in kept_ref[:6])))
    return rows


def e6_control():
    """E6: the positive control for the filter."""
    print("\n[E6] positive control -- plant a bound state")
    out = []
    for strength in (3.0, 6.0, 12.0):
        c = planted_eigenvalue_control(a=0.0, K_coarse=96, K_fine=144,
                                       strength=strength)
        planted = np.asarray(c["planted"])
        plain = np.asarray(c["plain"])
        moved = float(np.max([np.min(np.abs(plain - z)) for z in planted])) \
            if planted.size and plain.size else 0.0
        n_pos = int(np.sum(np.real(planted) > 1e-3))
        out.append({"strength": strength, "n_plain": c["n_plain"],
                    "n_planted": c["n_planted"], "plain": jl(plain),
                    "planted": jl(planted), "max_shift": moved,
                    "n_planted_unstable": n_pos})
        print("   V=%.1f  plain=%d planted=%d  max shift=%.3f  planted with Re>0: %d"
              "   -> %s" % (strength, c["n_plain"], c["n_planted"], moved, n_pos,
                            " ".join("%+.4f" % z.real for z in planted)))
    return out


def e7_end_of_branch(K=192, da=0.005, a_max=0.80):
    """E7: follow the branch until Newton loses it, and report where."""
    print("\n[E7] the end of the branch")
    flow = RescaledFlow(0.0, K=K)
    b = flow.B.anchor()
    rows = []
    last_good = None
    for a in np.arange(0.0, a_max + 1e-12, da):
        flow = RescaledFlow(float(a), K=K)
        o = flow.newton(b0=b)
        ok = o["residual"] < 5e-2 and o["c_omega"] < 0.0
        rows.append({"a": float(a), "c_omega": o["c_omega"],
                     "residual": o["residual"], "ok": bool(ok)})
        if not ok:
            print("   branch lost at a=%.4f (c_omega=%.4f, |R|=%.2e); last good a=%.4f"
                  " with alpha=%.3f" % (a, o["c_omega"], o["residual"],
                                        last_good["a"] if last_good else float("nan"),
                                        -last_good["c_omega"] if last_good else float("nan")))
            break
        b = o["b"]
        last_good = rows[-1]
    # extrapolate 1/alpha -> 0 from the last clean stretch
    aa = np.array([r["a"] for r in rows if r["ok"]])
    inv = np.array([-1.0 / r["c_omega"] for r in rows if r["ok"]])
    a_c = float("nan")
    if aa.size > 6:
        m = aa > aa[-1] - 0.06
        if m.sum() >= 3:
            p = np.polyfit(aa[m], inv[m], 1)
            a_c = float(-p[1] / p[0])
    print("   linear extrapolation of 1/alpha -> 0 gives a_c ~ %.4f" % a_c)
    return {"rows": rows, "a_c_linear_extrapolation": a_c, "K": K, "da": da}


def main():
    t0 = time.time()
    data = {"leg": "route_e_v1",
            "title": "spectrum of the rescaled gCLM flow at the self-similar fixed point",
            "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    data["E1_anchor"] = e1_anchor()
    data["E2_branch"] = e2_branch([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
    data["E3_resonance"] = e3_resonance()
    data["E4_structural"] = e4_structural([0.0, 0.2, 0.3, 0.5])
    data["E5_sweep"] = e5_sweep([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.55])
    data["E6_control"] = e6_control()
    data["E7_end"] = e7_end_of_branch()
    data["wall_clock_seconds"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1))
    print("\nwrote %s  (%.1f s)" % (OUT, data["wall_clock_seconds"]))


if __name__ == "__main__":
    main()
