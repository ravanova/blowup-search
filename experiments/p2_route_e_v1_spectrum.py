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
  E7  where the branch ends;
  E8  the THIRD eigenvalue E5 found at a = 1/2 that nothing predicted, on a K-ladder;
  E8b whether a = 1/2 is the only analytic resonance or alpha = 5 gives another;
  E8c the alpha = 5 point located by secant and put on a K-ladder;
  E9  WHERE THE CONTINUUM LIVES -- the edge formula that turned E8's "third mode"
      into an artefact, with a = 0 as the control point that makes it unarguable.

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


def canonical_order(kept, dist, round_dp=6):
    """Re-sort `match_filter`'s output onto a library/environment-INDEPENDENT key.

    `match_filter` (solver/rescaled_spectrum.py) sorts by `-Re(lambda)`, which is
    the right key for the two isolated structural modes (0 and -1) but a BROKEN
    one for the discretized essential spectrum: those eigenvalues are pinned to
    the imaginary axis in exact arithmetic (Re lambda = 0), so their numerically
    computed real parts are pure floating-point noise at the 1e-11 .. 1e-17
    level, with a sign that flips between LAPACK/BLAS builds -- leg 356 (ROUTE-
    ESPX) measured exactly this: the multiset of eigenvalues found is bit-for-bit
    identical between two environments, but sorting on that noise permutes WHICH
    array index each conjugate pair lands at, which is why leg 287's census read
    a same-content spectrum as a `max_rel_move = 1.880` disagreement.

    The fix stays entirely at the array-ordering step (no change to the filter's
    admission rule, no change to which eigenvalues are kept): round the real part
    to `round_dp` decimals -- far coarser than the noise floor, far finer than
    any genuine isolated real part this module has ever measured (0, -1, or a
    would-be Hopf pair's Re > 1e-3) -- and break ties on the SIGNED imaginary
    part, which is not noise (it is the content itself for the essential
    spectrum).  A rounded real part of 0 with no genuine content there sorts
    purely by Im, so conjugate pairs land in a fixed +Im-before--Im order
    regardless of which environment computed them.
    """
    order = sorted(range(len(kept)),
                    key=lambda i: (-round(float(kept[i].real), round_dp),
                                    -float(kept[i].imag)))
    kept2 = np.array([kept[i] for i in order]) if len(kept) else np.array([], complex)
    dist2 = np.array([dist[i] for i in order]) if len(dist) else np.array([])
    return kept2, dist2


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
            kept, dist = canonical_order(kept, dist)
            counts["%g" % t] = int(kept.size)
            keeps["%g" % t] = jl(kept)
        kept_ref, dist_ref = match_filter(ev_c, ev_f, 1e-2)
        kept_ref, dist_ref = canonical_order(kept_ref, dist_ref)
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


def e8_third_mode(Ks=(96, 144, 192, 256, 320), a=0.5):
    """E8a: the THIRD eigenvalue at a = 1/2, which E5 found and nobody predicted.

    E5's filter kept 0, -1 AND a third real eigenvalue near -2 at the analytic
    resonance -- at a looser distance (5.6e-3) than the two structural ones (1e-5),
    which is exactly the situation where a K-ladder is the difference between a mode
    and an artefact.  It is NOT symmetry: the two symmetry identities account for 0
    and -1 and nothing else.  If it converges, the fixed point has a genuine
    non-symmetry discrete eigenvalue, and the honest verdict changes from "only
    symmetry survives" to "one real, stable, non-symmetry mode exists and is nowhere
    near the axis".
    """
    print("\n[E8a] the third eigenvalue at a = 1/2")
    rows = []
    for K in Ks:
        flow, out = continuation(a, K=K, da=0.02)
        ev = np.linalg.eigvals(flow.generator(out["b"]))
        near = {}
        for target in (0.0, -1.0, -2.0):
            j = int(np.argmin(np.abs(ev - target)))
            near["%.0f" % target] = [float(ev[j].real), float(ev[j].imag)]
        rows.append({"K": K, "residual": out["residual"], "c_omega": out["c_omega"],
                     "near": near})
        print("   K=%4d |R|=%.2e   nearest to 0: %+.9f   to -1: %+.9f   to -2: %+.9f"
              % (K, out["residual"], near["0"][0], near["-1"][0], near["-2"][0]))
    seq = [r["near"]["-2"][0] for r in rows]
    print("   third-mode drift over the ladder: %.2e" % (max(seq) - min(seq)))
    return {"a": a, "rows": rows, "drift": float(max(seq) - min(seq))}


def e8b_second_resonance(K=256, a_lo=0.560, a_hi=0.600, n=17):
    """E8b: is a = 1/2 the only analytic resonance, or is there one at alpha = 5?

    alpha(a) is monotone and passes through 5 somewhere near a ~ 0.58.  If odd-integer
    alpha is what makes the profile analytic, the residual must dip there the way it
    does at a = 1/2 -- and a second spectrally-clean point would give the Hopf question
    a second place where it can actually be asked.  A flat scan says the a = 1/2
    resonance is NOT simply "alpha hit an odd integer", which is worth knowing before
    anyone builds a theory on it.
    """
    print("\n[E8b] scanning for a second analytic resonance (alpha = 5)")
    flow, out = continuation(a_lo, K=K, da=0.02)
    b = out["b"]
    rows = []
    for a in np.linspace(a_lo, a_hi, int(n)):
        flow = RescaledFlow(float(a), K=K)
        o = flow.newton(b0=b)
        b = o["b"]
        rows.append({"a": float(a), "alpha": -o["c_omega"], "residual": o["residual"]})
        print("   a=%.4f  alpha=%.6f  |R|=%.3e" % (a, -o["c_omega"], o["residual"]))
    al = np.array([r["alpha"] for r in rows])
    rs = np.array([r["residual"] for r in rows])
    i5 = int(np.argmin(np.abs(al - 5.0)))
    out_d = {"rows": rows, "K": K,
             "a_at_alpha5": rows[i5]["a"], "residual_at_alpha5": rows[i5]["residual"],
             "min_residual": float(rs.min()),
             "a_at_min_residual": rows[int(np.argmin(rs))]["a"],
             "dip_factor_vs_neighbours": float(np.median(rs) / rs.min())}
    print("   alpha = 5 at a ~ %.4f, residual there %.2e; scan min %.2e at a=%.4f; "
          "median/min = %.1f  (at a=1/2 that ratio is ~1e10)"
          % (out_d["a_at_alpha5"], out_d["residual_at_alpha5"], out_d["min_residual"],
             out_d["a_at_min_residual"], out_d["dip_factor_vs_neighbours"]))
    return out_d


def e9_essential_edges(a_values=(0.0, 0.5), Ks=(96, 144, 192)):
    """E9: WHERE THE CONTINUUM LIVES -- the measurement that killed E8's third mode.

    The two singular endpoints fix the essential spectrum's extent.  Near X = infinity
    the local operator is c_omega + xi d/dxi (xi = pi - theta), and near X = 0 it is
    (c_omega + H Omega(0)) - theta d/dtheta, so with s the local exponent

        c_omega + s_min  <=  Re lambda  <=  c_omega + H(Omega)(0) ,

    and in THIS space s_min = 1 because every sin(k theta) vanishes linearly at
    theta = pi.  Predicted strip: [c_omega + 1, c_omega + H(Omega)(0)] -- [0, 1] at
    a = 0 and [-2, +5] at a = 1/2.

    THIS IS THE CONTROL THAT EXPOSES E8.  The "third eigenvalue" converging to -2 at
    a = 1/2 is exactly c_omega + 1, the LEFT EDGE, not a mode -- and at a = 0 the same
    edge sits at 0 and carries ~99% of the discretized spectrum, where nobody would
    call it an eigenvalue.  Tightening the convergence filter would have made the
    artefact look better, not worse; only a control point at a known parameter finds it.
    """
    print("\n[E9] the essential spectrum's edges")
    rows = []
    for a in a_values:
        for K in Ks:
            flow, out = continuation(a, K=K, da=0.02)
            ev = np.linalg.eigvals(flow.generator(out["b"]))
            cw = out["c_omega"]
            H0 = 2.0 if a == 0.0 else (cw - 1.0) / (a - 1.0)
            left, right = cw + 1.0, cw + H0
            re = ev.real
            rows.append({"a": float(a), "K": K, "c_omega": cw, "H0": float(H0),
                         "left_pred": float(left), "right_pred": float(right),
                         "re_min": float(re.min()), "re_max": float(re.max()),
                         "residual": out["residual"],
                         "frac_at_left_edge": float(np.mean(np.abs(re - left) < 0.05))})
            print("   a=%.2f K=%3d  predicted strip [%+.4f, %+.4f]  measured Re "
                  "[%+.6f, %+.6f]  fraction sitting on the left edge %.2f"
                  % (a, K, left, right, re.min(), re.max(),
                     rows[-1]["frac_at_left_edge"]))
    return rows


def e8c_alpha5_resonance(K0=256, Ks=(96, 128, 192, 256, 320, 384)):
    """E8c: is "alpha = odd integer => analytic" the rule, or is a = 1/2 special?

    E8b found a residual dip exactly where alpha = 5, but only 13x deep against ~1e10
    at a = 1/2.  Either the scan simply missed the resonance's centre, or a = 1/2 is
    special for a reason beyond alpha being an odd integer.  Secant-solve alpha(a) = 5
    and run a K-ladder there: spectral fall means the rule, algebraic fall means the
    a = 1/2 point is not just "alpha hit 3".
    """
    print("\n[E8c] the alpha = 5 point, located and refined")
    _, out = continuation(0.575, K=K0, da=0.02)
    b = out["b"]

    def am5(a, b0):
        f = RescaledFlow(float(a), K=K0)
        o = f.newton(b0=b0)
        return -o["c_omega"] - 5.0, o["b"], o["residual"]

    a0, a1 = 0.5800, 0.5825
    f0, b, _ = am5(a0, b)
    f1, b, _ = am5(a1, b)
    for _ in range(8):
        a2 = a1 - f1 * (a1 - a0) / (f1 - f0)
        f2, b, r = am5(a2, b)
        a0, f0, a1, f1 = a1, f1, a2, f2
        if abs(f2) < 1e-9:
            break
    a_star = float(a1)
    rows = []
    for K in Ks:
        _, o = continuation(a_star, K=K, da=0.02)
        rows.append({"K": K, "residual": o["residual"], "c_omega": o["c_omega"]})
        print("   a*=%.8f  K=%4d  |R|=%.3e  alpha=%.10f"
              % (a_star, K, o["residual"], -o["c_omega"]))
    return {"a_star": a_star, "K_ladder": rows}


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
    data["E8_third_mode"] = e8_third_mode()
    data["E8b_second_resonance"] = e8b_second_resonance()
    data["E8c_alpha5_resonance"] = e8c_alpha5_resonance()
    data["E9_essential_edges"] = e9_essential_edges()
    data["wall_clock_seconds"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1))
    print("\nwrote %s  (%.1f s)" % (OUT, data["wall_clock_seconds"]))


if __name__ == "__main__":
    main()
