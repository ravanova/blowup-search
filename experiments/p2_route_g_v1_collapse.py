"""Route-G v1: the critical dissipation exponent on the 2D object.

Ranked items (2)+(3), merged: port Route-F's critical-dissipation question off the 1D
toy and onto 2D Boussinesq in the Hou-Luo geometry -- the system the 1D model is a model
OF, and the one where certification results count.

WHAT THIS PRODUCES, in the order the leg discovered it:

  G0  THE LAW, in the form that survives the port.  s_c = 1/(2 beta) with beta the
      COLLAPSE EXPONENT of L ~ (T-t)^beta.  Route-F's s_c = alpha/2 is the beta = 1/alpha
      case.  beta = 1/2 is Navier-Stokes and gives s_c = 1 exactly.  Exact arithmetic.

  G1  WHERE THE PROVEN 2D BLOW-UP SITS, from published constants.  Chen-Hou's
      c_l = 3.00649898, c_omega = -1.02942516 give beta = 2.9206 and s_c = 0.1712.

  G2  THE SAME NUMBER FROM OUR OWN MACHINE.  Relax the Spike-1 dynamically-rescaled 2D
      Boussinesq system and read beta = -c_l/c_omega off the MODULATION CONSTANTS -- no
      fit, no window, no singular-time estimate.  Steps ladder (is it relaxed?) then a
      resolution/domain ladder (is it converged?).

  G3  THE DIRECT ROUTE, PRICED AND REFUSED.  Do what Route-F did in 1D: run the
      time-dependent system with (-Delta)^s dissipation and fit D/N ~ (T-t)^p.  In 1D
      that gave four decades of (T-t).  Here it gives less than one, and beta moves by
      more than a factor of two across sub-windows, so the code refuses to quote it.
      Reported WITH the D/N exponents anyway, labelled underpowered, because the sign
      structure is still informative and the number is what a future leg would improve.

  G4  THE CROSS-MODEL CALIBRATION, and it is the uncomfortable one.  gCLM's beta is a
      dial: beta(a) = 1/alpha(a) from Route-E.  Over the a in [0, 0.5] range this project
      has worked in, beta runs 1.00 down to 0.33 and crosses the NS line beta = 1/2 at
      a ~ 0.383.  The 2D Boussinesq object it is supposed to model sits at beta = 2.92,
      which is OUTSIDE that range entirely -- and reaching it needs a < 0.

Usage:  .venv/bin/python -u experiments/p2_route_g_v1_collapse.py [--quick]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.fractional_boussinesq import (  # noqa: E402
    CHEN_HOU_C_L, CHEN_HOU_C_OMEGA, FractionalBoussinesq, chen_hou_beta,
    collapse_exponent_from_rescaling, collapse_window_report, critical_s, estimate_T,
    fit_collapse, fit_relevance, houluo_sharp_ic, relevance_exponent,
)

DATA = Path(__file__).resolve().parent.parent / "writeup" / "data"

# Route-E v1's measured alpha(a) for gCLM (writeup/data, §26).  beta = 1/alpha.
ROUTE_E_ALPHA = {0.0: 1.0000, 0.1: 1.1414, 0.2: 1.3345, 0.3: 1.6172,
                 0.4: 2.0795, 0.5: 3.0000}


# --------------------------------------------------------------------------
def g0_the_law():
    """The law and its two anchors, as exact arithmetic."""
    rows = []
    for label, beta in [("gCLM a=0 (alpha=1)", 1.0),
                        ("gCLM a~0.383 (alpha=2) = NS-critical", 0.5),
                        ("NAVIER-STOKES (dimensional analysis)", 0.5),
                        ("gCLM a=0.5 (alpha=3)", 1.0 / 3.0),
                        ("Chen-Hou 2D Boussinesq", chen_hou_beta())]:
        rows.append({"object": label, "beta": float(beta),
                     "s_c": float(critical_s(beta)),
                     "p_at_s1": float(relevance_exponent(1.0, beta))})
    return {"rows": rows,
            "note": ("s_c = 1/(2 beta).  p(s) = 1 - 2 beta s is the relevance exponent "
                     "of D/N ~ (T-t)^p; p > 0 means dissipation loses.  p_at_s1 is the "
                     "value at the ORDINARY Laplacian, so its sign says directly whether "
                     "the object beats ordinary viscosity.")}


def g1_chen_hou():
    beta = chen_hou_beta()
    return {"c_l": CHEN_HOU_C_L, "c_omega": CHEN_HOU_C_OMEGA,
            "alpha_2D": CHEN_HOU_C_OMEGA / CHEN_HOU_C_L,
            "beta": beta, "s_c": float(critical_s(beta)),
            "ratio_to_NS": float(beta / 0.5),
            "p_at_ordinary_laplacian": float(relevance_exponent(1.0, beta))}


# --------------------------------------------------------------------------
def g2_our_own_beta(quick=False):
    """beta from the dynamically-rescaled 2D Boussinesq machine (Spike 1, Step C).

    THE INSTRUMENT IS THE POINT.  In dynamic rescaling the collapse exponent is a
    MODULATION CONSTANT: c_l and c_omega are computed from the origin slopes at every
    step, and beta = -c_l/c_omega.  Nothing is fitted, no window is chosen, and the
    singular time never appears -- which is exactly the three things that make the
    direct route (G3) unusable here.

    GAUGE HONESTY, inherited from Spike 1: the normalization freezes theta_xx(0) and
    omega_x(0), so c_l is an INPUT we pin to the Chen-Hou gauge; c_omega is the output,
    and beta is therefore a measurement of c_omega at a pinned c_l.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from spike1_stepC_gate import run_gate

    # steps=2500 is Spike-1 Step C's own protocol, kept deliberately so that the
    # resolution ladder here can be compared against the committed
    # writeup/data/spike1_stepC_gate.json -- a free reproducibility check on a run
    # made three legs ago by different code paths.
    steps_ladder = [400, 1200] if quick else [400, 1200, 2500, 4000]
    res_ladder = ([(300, 48, 1e5)] if quick else
                  [(300, 48, 1e5), (450, 48, 1e5), (600, 48, 1e5), (450, 48, 1e6)])
    final_steps = 1200 if quick else 2500

    out = {"steps_ladder": [], "resolution_ladder": [], "gauge_note":
           "c_l is PINNED by the frozen normalization; c_omega is the measured output."}
    for st in steps_ladder:
        t0 = time.time()
        r = run_gate(300, 48, 1e-3, 1e5, steps=st)
        beta = -r["c_l"] / r["c_omega"]
        out["steps_ladder"].append(
            {"steps": st, "residual": r["residual"], "c_l": r["c_l"],
             "c_omega": r["c_omega"], "alpha": r["alpha"], "beta": beta,
             "s_c": float(critical_s(beta)), "seconds": time.time() - t0})
        print(f"  [G2 steps] {st:5d}: res={r['residual']:.2e} c_om={r['c_omega']:+.5f} "
              f"alpha={r['alpha']:+.6f} beta={beta:.5f} s_c={critical_s(beta):.5f} "
              f"({time.time() - t0:.0f}s)", flush=True)

    for (n_r, n_b, r_max) in res_ladder:
        t0 = time.time()
        r = run_gate(n_r, n_b, 1e-3, r_max, steps=final_steps)
        beta = -r["c_l"] / r["c_omega"]
        out["resolution_ladder"].append(
            {"n_r": n_r, "n_beta": n_b, "r_max": r_max, "steps": final_steps,
             "residual": r["residual"], "c_l": r["c_l"], "c_omega": r["c_omega"],
             "alpha": r["alpha"], "alpha_far": r["alpha_far"], "beta": beta,
             "s_c": float(critical_s(beta)),
             "anisotropy_median": r["anisotropy_median"], "seconds": time.time() - t0})
        print(f"  [G2 res] n_r={n_r} n_b={n_b} r_max={r_max:.0e}: "
              f"c_om={r['c_omega']:+.5f} alpha={r['alpha']:+.6f} beta={beta:.5f} "
              f"s_c={critical_s(beta):.5f} ({time.time() - t0:.0f}s)", flush=True)

    betas = [x["beta"] for x in out["resolution_ladder"]]
    scs = [x["s_c"] for x in out["resolution_ladder"]]
    out["beta_mean"] = float(np.mean(betas))
    out["beta_spread"] = float(max(betas) - min(betas))
    out["s_c_mean"] = float(np.mean(scs))
    out["s_c_spread"] = float(max(scs) - min(scs))
    out["published_beta"] = chen_hou_beta()
    out["relative_error_vs_published"] = float(
        abs(out["beta_mean"] - chen_hou_beta()) / chen_hou_beta())
    return out


# --------------------------------------------------------------------------
def g3_direct_route(quick=False):
    """The 1D method, run in 2D, measured, and refused.

    Two separate things are reported and they must not be conflated:
      (a) the COLLAPSE fit -- refused, with the two numbers that make the call;
      (b) the D/N relevance exponents p(s) -- computed, kept, and labelled
          UNDERPOWERED, because they inherit the same thin window.  The sign
          structure survives the caveat; the location of the zero does not.
    """
    n = 192 if quick else 256
    w0, th0 = houluo_sharp_ic(n)
    out = {"n": n}

    t0 = time.time()
    ref = FractionalBoussinesq(n=n, nu=0.0, s=1.0)
    r0 = ref.run(w0, th0, amp_factor=1e4, sample_every=10, max_steps=200000,
                 wall_max=600.0)
    T0 = estimate_T(r0)
    fc = fit_collapse(r0, T0)
    rep = collapse_window_report(r0, T0)
    out["inviscid"] = {
        "outcome": r0["outcome"], "growth": float(r0["amp"][-1] / r0["amp0"]),
        "t_final": r0["t_final"], "T": float(T0), "samples": int(r0["amp"].size),
        "amp_exponent": fc["amp_exponent"], "beta_x": fc["Lx"], "beta_y": fc["Ly"],
        "beta_grad": fc["Lgrad"], "beta_spec": fc["Lspec"],
        "window_report": rep, "seconds": time.time() - t0}
    print(f"  [G3 inviscid] growth={out['inviscid']['growth']:.1f} "
          f"decades={rep['decades']:.2f} measurable={rep['measurable']} "
          f"({rep['reason']})", flush=True)

    s_list = [0.15, 0.5, 1.0] if quick else [0.1, 0.2, 0.35, 0.5, 0.75, 1.0]
    out["relevance"] = []
    for s in s_list:
        t0 = time.time()
        sv = FractionalBoussinesq(n=n, nu=1e-3, s=s)
        r = sv.run(w0, th0, amp_factor=1e4, sample_every=10, max_steps=200000,
                   wall_max=600.0)
        T = estimate_T(r)
        fr = fit_relevance(r, T)
        fcs = fit_collapse(r, T)
        out["relevance"].append(
            {"s": s, "p": fr["p"], "n_points": fr["n_points"],
             "fit_rms": fr.get("fit_rms"), "outcome": r["outcome"], "T": float(T),
             "growth": float(r["amp"][-1] / r["amp0"]),
             "beta_grad": fcs["Lgrad"], "seconds": time.time() - t0})
        print(f"  [G3 p(s)] s={s:.2f}: p={fr['p']:+.4f} (npts {fr['n_points']}, "
              f"growth {r['amp'][-1] / r['amp0']:.1f}, {r['outcome']}) "
              f"({time.time() - t0:.0f}s)", flush=True)

    ss = np.array([x["s"] for x in out["relevance"]])
    ps = np.array([x["p"] for x in out["relevance"]])
    m = np.isfinite(ps)
    if m.sum() >= 3:
        c = np.polyfit(ss[m], ps[m], 1)
        out["p_line"] = {"slope": float(c[0]), "intercept": float(c[1]),
                         "zero": float(-c[1] / c[0]) if c[0] != 0 else None,
                         "beta_implied": float(-c[0] / 2.0)}
        print(f"  [G3 line] slope={c[0]:+.3f} => beta_implied={-c[0] / 2:.3f}, "
              f"zero at s={-c[1] / c[0]:.3f}", flush=True)
    out["verdict"] = ("UNDERPOWERED: the direct route does not port. It is kept because "
                      "the sign structure is real and because it prices what a future "
                      "leg would have to buy (an adaptive or rescaled 2D grid).")
    return out


# --------------------------------------------------------------------------
def g4_cross_model(quick=False):
    """Where does the 1D toy's beta sit relative to the 2D object it models?

    beta(a) = 1/alpha(a) from Route-E for a >= 0, and a continuation to a < 0 to ask
    the calibration question: is there a gCLM member whose COLLAPSE RATE matches the
    Chen-Hou 2D Boussinesq blow-up at all?

    The a < 0 continuation is reported WITH its Newton residual, because the
    compactified odd-sine basis is spectral only at odd-integer alpha and alpha < 1
    there -- so this row may be basis-limited rather than converged, and a K-ladder is
    run to say which.
    """
    from solver.rescaled_spectrum import continuation

    out = {"positive_a": [], "negative_a": [], "target_beta": chen_hou_beta()}
    for a, alpha in sorted(ROUTE_E_ALPHA.items()):
        beta = 1.0 / alpha
        out["positive_a"].append({"a": a, "alpha": alpha, "beta": beta,
                                  "s_c": float(critical_s(beta))})
    # where beta crosses the NS line 1/2, i.e. alpha = 2
    aa = np.array(sorted(ROUTE_E_ALPHA))
    al = np.array([ROUTE_E_ALPHA[x] for x in aa])
    out["a_at_NS_line"] = float(np.interp(2.0, al, aa))

    # The a-sweep at one K, plus a K-LADDER at the single a that matters (the one
    # nearest the 2D object's beta).  A full grid of K x a costs ~K^3 per Newton and
    # would buy nothing the ladder does not.
    a_list = [-1.0, -2.0] if quick else [-1.0, -1.5, -2.0, -2.5]
    jobs = [(96, a) for a in a_list]
    if not quick:
        jobs += [(144, -2.0), (192, -2.0), (144, -1.0)]
    for K, a in jobs:
        if True:
            t0 = time.time()
            try:
                flow, res = continuation(a, K=K, da=-0.02, max_iter=300)
                alpha = float(-flow.c_omega(res["b"]))
                beta = 1.0 / alpha
                row = {"K": K, "a": a, "alpha": alpha, "beta": beta,
                       "s_c": float(critical_s(beta)), "residual": res["residual"],
                       "converged": bool(res["converged"]), "seconds": time.time() - t0}
            except Exception as ex:  # noqa: BLE001
                row = {"K": K, "a": a, "error": f"{type(ex).__name__}: {ex}"[:120]}
            out["negative_a"].append(row)
            print(f"  [G4] K={K} a={a:+.2f}: " +
                  (f"alpha={row['alpha']:.6f} beta={row['beta']:.5f} "
                   f"res={row['residual']:.1e} conv={row['converged']}"
                   if "alpha" in row else row["error"]), flush=True)

    # Does the residual FALL with K?  That distinguishes "basis truncation" (a rate we
    # can quote an error bar from) from "the Newton is not finding the object".
    by_a = {}
    for r in out["negative_a"]:
        if "alpha" in r:
            by_a.setdefault(r["a"], []).append((r["K"], r["residual"], r["alpha"]))
    out["K_convergence"] = {
        str(a): {"K": [k for k, _, _ in v], "residual": [x for _, x, _ in v],
                 "alpha": [x for _, _, x in v],
                 "residual_falls_with_K": bool(len(v) > 1 and v[-1][1] < v[0][1]),
                 "alpha_spread": float(max(x for _, _, x in v) - min(x for _, _, x in v))}
        for a, v in by_a.items()}
    return out


# --------------------------------------------------------------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)

    payload = {"leg": "Route-G v1", "quick": args.quick}
    print("G0/G1  the law and the published constants", flush=True)
    payload["g0_law"] = g0_the_law()
    payload["g1_chen_hou"] = g1_chen_hou()
    for r in payload["g0_law"]["rows"]:
        print(f"  {r['object']:42s} beta={r['beta']:8.5f} s_c={r['s_c']:8.5f} "
              f"p(s=1)={r['p_at_s1']:+8.4f}")

    want = set(args.only.split(",")) if args.only else {"g2", "g3", "g4"}
    if "g2" in want:
        print("G2  beta from our own dynamically-rescaled 2D machine", flush=True)
        payload["g2_our_beta"] = g2_our_own_beta(args.quick)
    if "g3" in want:
        print("G3  the direct time-dependent route (expected: refused)", flush=True)
        payload["g3_direct"] = g3_direct_route(args.quick)
    if "g4" in want:
        print("G4  cross-model calibration (where is the 2D object on gCLM's dial?)",
              flush=True)
        payload["g4_cross_model"] = g4_cross_model(args.quick)

    path = DATA / "p2_route_g_v1_collapse.json"
    path.write_text(json.dumps(payload, indent=1))
    print(f"\nwrote {path}")
