"""Route-F v1: the critical dissipation exponent for gCLM -- can a blow-up beat viscosity?

THE QUESTION.  Ranked item (2) of "what would actually be worthwhile", and the only
item that probes the ACTUAL obstruction between a toy-model certificate and
Navier-Stokes: take a blow-up that exists, add dissipation `nu (-Delta)^s`, and find
the exponent `s` at which dissipation wins.

THE PREDICTION (derived, then tested).  Route-E v1's by-product was the far-field
decay exponent alpha(a) of the self-similar profile.  The rescaling ODEs give
L ~ (T-t)^{1/alpha}, so comparing `nu omega / L^{2s}` with `omega^2`:

    D/N ~ nu (T-t)^{1 - 2 s / alpha}     =>    s_c(a) = alpha(a)/2 .

SIX MEASUREMENTS:
  F1  the known answer -- the exact a = 0 solution, and how well a run recovers its
      own singular time;
  F2  the RELEVANCE EXPONENT p(s) at a = 0 against the predicted line 1 - 2s;
  F3  THE CROSS-CHECK: does alpha(a) -- measured on the LINE by a compactified
      STEADY solve in a different module -- predict the slope dp/ds = -2/alpha in
      direct TIME-DEPENDENT PERIODIC simulation?  Two computations with almost
      nothing in common;
  F4  the nu-INDEPENDENCE control (the prediction involves s and alpha, not nu);
  F5  a resolution ladder;
  F6  the s_c(a) map, and where it crosses the ordinary Laplacian s = 1.

Deterministic, NOT logged.  Writes writeup/data/p2_route_f_v1_viscosity.json.

Run: .venv/bin/python -u experiments/p2_route_f_v1_viscosity.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.fractional_gclm import (  # noqa: E402
    FractionalGCLM, clm_blowup_time, clm_exact, critical_s, estimate_T,
    fit_relevance, relevance_exponent,
)

OUT = ROOT / "writeup" / "data" / "p2_route_f_v1_viscosity.json"
ROUTE_E = ROOT / "writeup" / "data" / "p2_route_e_v1_spectrum.json"
N_DEFAULT = 4096
AMP = 1000.0


def initial(n):
    x = np.arange(n) * 2.0 * np.pi / n
    return np.sin(x) + 0.4 * np.sin(2.0 * x)


def one_run(a, nu, s, n=N_DEFAULT, amp=AMP):
    g = FractionalGCLM(n=n, a=a, nu=nu, s=s)
    r = g.run(initial(n), amp_factor=amp, sample_every=5, max_steps=600000)
    T = estimate_T(r)
    fit = fit_relevance(r, T)
    return {"a": a, "nu": nu, "s": s, "n": n, "outcome": r["outcome"],
            "T_est": T, "p": fit["p"], "fit_rms": fit.get("fit_rms", float("nan")),
            "n_points": fit.get("n_points", 0), "amp_final": float(r["amp"][-1])
            if r["amp"].size else float("nan"), "max_tail": r["max_tail"],
            "steps": r["steps"]}


def alpha_map():
    """alpha(a) from Route-E v1's committed data -- the input this leg depends on."""
    d = json.loads(ROUTE_E.read_text())
    return {round(r["a"], 3): r["alpha"] for r in d["E2_branch"]}


# --------------------------------------------------------------------------
def f1_known_answer():
    print("\n[F1] the known answer")
    n = N_DEFAULT
    w0 = initial(n)
    T0 = clm_blowup_time(w0)
    g = FractionalGCLM(n=n, a=0.0, nu=0.0, s=1.0)
    mid = g.run(w0, t_end=2.5, amp_factor=1e12, sample_every=5)
    err = float(np.max(np.abs(mid["omega"] - clm_exact(w0, mid["t_final"]))))
    r = g.run(w0, amp_factor=AMP, sample_every=5)
    Te = estimate_T(r)
    print("   exact T = %.10f ; solver vs exact solution at t=2.5: %.2e" % (T0, err))
    print("   run's own T estimate = %.8f  (relative error %.2e), tail %.1e"
          % (Te, abs(Te - T0) / T0, r["max_tail"]))
    return {"T_exact": T0, "solver_vs_exact_at_2.5": err, "T_est": Te,
            "T_rel_err": abs(Te - T0) / T0, "max_tail": r["max_tail"]}


def f2_relevance_line(a=0.0, nu=1e-3, s_values=(0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75)):
    print("\n[F2] the relevance exponent at a = %.2f" % a)
    alpha = 1.0
    rows = []
    for s in s_values:
        r = one_run(a, nu, s)
        r["p_pred"] = float(relevance_exponent(s, alpha))
        rows.append(r)
        print("   s=%.2f  p = %+.4f  (predicted %+.4f)  rms %.3f  tail %.1e"
              % (s, r["p"], r["p_pred"], r["fit_rms"], r["max_tail"]))
    ss = np.array([r["s"] for r in rows])
    pp = np.array([r["p"] for r in rows])
    c = np.polyfit(ss, pp, 1)
    zero = float(-c[1] / c[0])
    print("   fitted slope %+.4f (predicted %+.4f);  p = 0 at s = %.4f "
          "(predicted s_c = %.4f)" % (c[0], -2.0 / alpha, zero, 0.5 * alpha))
    return {"a": a, "nu": nu, "alpha": alpha, "rows": rows, "slope": float(c[0]),
            "slope_pred": -2.0 / alpha, "s_zero": zero, "s_c_pred": 0.5 * alpha}


def f3_cross_check(a_values=(0.0, 0.2, 0.3, 0.4), nu=1e-3,
                   s_values=(0.2, 0.35, 0.5, 0.65)):
    """THE HEADLINE.  alpha comes from a steady compactified solve on the LINE;
    the slope comes from time-dependent PERIODIC simulation.  Nothing is shared."""
    print("\n[F3] cross-check: does Route-E's alpha(a) predict the slope?")
    am = alpha_map()
    rows = []
    for a in a_values:
        alpha = am.get(round(a, 3))
        if alpha is None:
            continue
        ps = []
        for s in s_values:
            r = one_run(a, nu, s)
            ps.append(r["p"])
        c = np.polyfit(np.array(s_values, float), np.array(ps), 1)
        rows.append({"a": a, "alpha": alpha, "s": list(s_values), "p": ps,
                     "slope": float(c[0]), "slope_pred": -2.0 / alpha,
                     "ratio": float(c[0] / (-2.0 / alpha))})
        print("   a=%.2f  alpha=%.6f  slope %+.4f  (predicted %+.4f)  ratio %.4f"
              % (a, alpha, c[0], -2.0 / alpha, rows[-1]["ratio"]))
    return rows


def f4_nu_control(a=0.0, nus=(1e-2, 1e-3, 1e-4), s_values=(0.25, 0.5, 0.75)):
    """The prediction contains s and alpha, NOT nu.  A slope that moves with nu
    would mean the measurement is about the viscosity, not about the scaling."""
    print("\n[F4] nu-independence control")
    rows = []
    for nu in nus:
        ps = [one_run(a, nu, s)["p"] for s in s_values]
        c = np.polyfit(np.array(s_values, float), np.array(ps), 1)
        rows.append({"nu": nu, "s": list(s_values), "p": ps, "slope": float(c[0])})
        print("   nu=%.0e  p = %s  slope %+.4f" % (nu, ["%+.3f" % v for v in ps], c[0]))
    sl = [r["slope"] for r in rows]
    spread = float(max(sl) - min(sl))
    print("   slope spread over three decades of nu: %.4f  (prediction: 0)" % spread)
    return {"rows": rows, "slope_spread": spread, "slope_pred": -2.0}


def f5_resolution(a=0.0, nu=1e-3, s=0.35, ns=(1024, 2048, 4096, 8192)):
    print("\n[F5] resolution ladder")
    rows = []
    for n in ns:
        r = one_run(a, nu, s, n=n)
        rows.append(r)
        print("   n=%5d  p = %+.5f  tail %.1e  steps %d" % (n, r["p"], r["max_tail"],
                                                            r["steps"]))
    pv = [r["p"] for r in rows]
    fine = abs(pv[-1] - pv[-2])
    print("   spread over the whole 8x ladder: %.2e ; between the two FINEST: %.2e"
          % (max(pv) - min(pv), fine))
    return {"rows": rows, "spread": float(max(pv) - min(pv)),
            "finest_pair_diff": float(fine)}


def f6_sc_map():
    print("\n[F6] the s_c(a) map")
    am = alpha_map()
    aa = sorted(am)
    rows = [{"a": a, "alpha": am[a], "s_c": float(critical_s(am[a]))} for a in aa]
    for r in rows:
        print("   a=%.2f  alpha=%.6f  s_c=%.6f%s"
              % (r["a"], r["alpha"], r["s_c"],
                 "   <- the Laplacian s=1 is SUBcritical here" if r["s_c"] > 1 else ""))
    # where does s_c cross 1 (i.e. alpha = 2)?
    al = np.array([r["alpha"] for r in rows])
    ax = np.array([r["a"] for r in rows])
    a_star = float(np.interp(2.0, al, ax)) if al[-1] > 2.0 else float("nan")
    print("   alpha = 2 (s_c = 1, the ordinary Laplacian) at a ~ %.4f" % a_star)
    return {"rows": rows, "a_at_sc_equals_1": a_star}


def main():
    t0 = time.time()
    d = {"leg": "route_f_v1",
         "title": "critical dissipation exponent s_c = alpha/2 for gCLM",
         "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    d["F1_known_answer"] = f1_known_answer()
    d["F2_relevance_line"] = f2_relevance_line()
    d["F3_cross_check"] = f3_cross_check()
    d["F4_nu_control"] = f4_nu_control()
    d["F5_resolution"] = f5_resolution()
    d["F6_sc_map"] = f6_sc_map()
    d["wall_clock_seconds"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(d, indent=1))
    print("\nwrote %s  (%.1f s)" % (OUT, d["wall_clock_seconds"]))


if __name__ == "__main__":
    main()
