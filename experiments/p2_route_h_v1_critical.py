"""Route-H v1: the MARGINAL case -- what happens AT s = s_c, where scaling says nothing.

THE QUESTION.  Route-F v1 (§27) and Route-G v1 (§28) located the critical dissipation
exponent, and both ended at the same wall: AT s = s_c the two terms balance
identically and the scaling argument returns zero information.  That is precisely
where Navier-Stokes sits (beta = 1/2 => s_c = 1, the ordinary Laplacian).  So the
marginal case is not a corner of the map -- it is the case.

THE REFRAME.  Keeping the dissipative term through the dynamic rescaling makes its
coefficient mu = nu/(A L^{2s}) an autonomous DYNAMICAL VARIABLE:

    Omega_tau = (c_omega + H Omega) Omega - X Omega_X - a U Omega_X - mu Lambda^{2s} Omega
    mu_tau    = (2 s - alpha[Omega, mu]) mu ,          alpha = -c_omega .

Two consequences, and the leg is about the second:
  * Route-F's s_c is the EIGENVALUE 2s - alpha_0 of the inviscid fixed point in the
    mu-direction.  A scaling exponent becomes a stability exponent.
  * AT criticality that eigenvalue is exactly zero, so the outcome is set by the
    QUADRATIC term: mu_tau = -alpha_1 mu^2 with alpha_1 = d alpha/d mu.  ONE NUMBER.

SEVEN MEASUREMENTS:
  H1  the known answer -- the closed-form viscous CLM blow-up (E) and its PDE residual;
  H2  the a = 0 marginal branch: alpha == 1 at every mu, so alpha_1 = 0 EXACTLY -- a
      LINE of viscous self-similar blow-ups, neutral to all orders;
  H3  the a = 1/2, s = 3/2 marginal branch (Lambda^3 exact): alpha_1 > 0, K-laddered;
  H4  the third critical point a = 0.5821792673, s = 5/2 -- NOT REACHED, reported as a
      failure because "we could not reach it" is data too, and because the REFUSAL
      PREDICATE is the lesson: the K = 288 rung converges to a respectable 1e-4 and
      returns the OPPOSITE sign for alpha_1 off an alpha excursion of 1e-5.  Refusing
      on the residual alone would have shipped that;
  H5  THE DSS RE-ASK.  Route-E shut the DSS lane's cheap entrance with the mechanism
      "the non-symmetry spectrum is CONTINUOUS, and a continuum has no eigenvalue to
      move".  Critical dissipation is exactly the perturbation that could repair that.
      Does it discretize the continuum, and does anything then move or go complex?
  H6  the marginal verdict, with the mu-decay time (algebraic, not exponential);
  H7  THE CROSS-CHECK, through unrelated machinery: Route-F's time-dependent PERIODIC
      pseudo-spectral solver at a = 0, s = 1/2 exactly.  The plateau prediction is
      p = 0, and nothing about the compactified steady solve enters it.

Deterministic, NOT logged (~10 min).  Writes writeup/data/p2_route_h_v1_critical.json.

Run: .venv/bin/python -u experiments/p2_route_h_v1_critical.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.critical_dissipation import (  # noqa: E402
    CRITICAL_POINTS, CriticalDissipativeFlow, alpha_slope, amplitude_eigenvalue,
    converged_dissipative_spectrum, exact_a0_family, exact_a0_residual,
    exact_a0_spacetime, inviscid_seed, lambda_truncation, marginal_verdict,
    mu_branch, mu_decay_time, planted_dissipative_control,
)
from solver.fractional_gclm import (  # noqa: E402
    FractionalGCLM, clm_blowup_time, estimate_T, fit_relevance,
)
from solver.rescaled_spectrum import OddCompactBasis  # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_h_v1_critical.json"


def _tick(name):
    print(f"\n--- {name} ---", flush=True)
    return time.time()


def _done(t0):
    print(f"    [{time.time() - t0:.1f}s]", flush=True)


# --------------------------------------------------------------------------
def h1_exact_solution():
    """(E) as a solution of the PDE, in closed form -- the leg's known answer."""
    t0 = _tick("H1  the closed-form viscous blow-up")
    x = np.linspace(-60.0, 60.0, 6001)
    rows = []
    for nu in (0.05, 0.5, 2.0):
        for mu0 in (0.1, 1.0, 3.0):
            r = max(exact_a0_residual(x, t, nu, mu0) for t in (0.0, 0.5, 0.9, 0.99))
            rows.append({"nu": nu, "mu0": mu0, "pde_residual": r})
            print(f"    nu={nu:5.2f} mu0={mu0:4.1f}  |PDE residual| = {r:.2e}", flush=True)
    # the amplitude law, measured rather than asserted
    amp = []
    for t in (0.5, 0.9, 0.99, 0.999):
        q = exact_a0_spacetime(np.linspace(-8, 8, 400001), t, 0.5, 1.0)
        amp.append({"t": t, "amp": float(np.max(np.abs(q["omega"]))),
                    "predicted": 2.0 / (1.0 - t)})
    print(f"    ||omega||_inf vs (1+mu_0)/(T-t): "
          + " ".join("%.1f/%.1f" % (a["amp"], a["predicted"]) for a in amp), flush=True)
    _done(t0)
    return {"pde_residual": rows, "amplitude_law": amp,
            "worst_residual": max(r["pde_residual"] for r in rows)}


def h2_a0_branch(K=96):
    """alpha == 1 along the whole mu-branch: alpha_1 = 0, the neutral line."""
    t0 = _tick("H2  the a = 0 marginal branch (s = 1/2, Lambda exact)")
    mus = [0.0, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0]
    rows = mu_branch(0.0, 1, mus, K=K)
    B = OddCompactBasis(K)
    out = []
    for r in rows:
        exact, mu0, lam = exact_a0_family(r["mu"], B.X)
        out.append({"mu": r["mu"], "alpha": r["alpha"], "residual": r["residual"],
                    "mu_growth": r["mu_growth"], "mu0": float(mu0), "width": float(lam),
                    "closed_form_error": float(np.max(np.abs(B.S @ r["b"] - exact)))})
        print(f"    mu={r['mu']:5.2f}  alpha={r['alpha']:.14f}  "
              f"res={r['residual']:.1e}  |num-exact|={out[-1]['closed_form_error']:.1e}",
              flush=True)
    sl = alpha_slope(rows)
    print(f"    alpha_1 = {sl['alpha_1']:.3e}   verdict: "
          f"{marginal_verdict(sl['alpha_1'])}", flush=True)
    _done(t0)
    return {"K": K, "rows": out, "slope": sl,
            "verdict": marginal_verdict(sl["alpha_1"])}


def h3_a_half_branch(Ks=(96, 144, 192, 240)):
    """The a = 1/2, s = 3/2 branch: does the a = 0 degeneracy survive?"""
    t0 = _tick("H3  the a = 1/2 marginal branch (s = 3/2, Lambda^3 exact)")
    mus = [0.0, 0.025, 0.05, 0.1, 0.2]
    ladder = []
    for K in Ks:
        rows = mu_branch(0.5, 3, mus, K=K)
        sl = alpha_slope(rows)
        ladder.append({
            "K": int(K), "alpha_1": sl["alpha_1"], "alpha_2": sl["alpha_2"],
            "alpha_1_chord": sl["alpha_1_chord"], "secants": sl["secants"],
            "alpha_0": sl["alpha_0"],
            "alpha": [r["alpha"] for r in rows], "mu": [r["mu"] for r in rows],
            "residual": [r["residual"] for r in rows],
            "truncation": [r["lambda_truncation"] for r in rows]})
        print(f"    K={K:4d}  alpha_0={sl['alpha_0']:.10f}  alpha_1={sl['alpha_1']:.6f}  "
              f"(chord {sl['alpha_1_chord']:.6f})  max trunc="
              f"{max(r['lambda_truncation'] for r in rows):.4f}", flush=True)
    a1 = ladder[-1]["alpha_1"]
    print(f"    verdict: {marginal_verdict(a1)}", flush=True)
    _done(t0)
    return {"ladder": ladder, "alpha_1": a1, "verdict": marginal_verdict(a1),
            "K_spread": float(max(d["alpha_1"] for d in ladder)
                              - min(d["alpha_1"] for d in ladder))}


def h4_third_point(Ks=(192, 288), da=0.005, mus=(0.0, 0.01, 0.02, 0.04)):
    """a = 0.5821792673, alpha = 5, s = 5/2.  Reported either way -- AND the refusal
    predicate is the one that matters, not the obvious one.

    Refusing on the residual alone is not enough here, and the K = 288 rung is why.  At
    that resolution the residual is respectable (1e-4..4e-4) and alpha_slope returns a
    NEGATIVE alpha_1 -- the opposite verdict to a = 1/2, and a headline.  But the whole
    excursion of alpha across the mu-window is 1.3e-5, two orders BELOW the residual:
    the derivative being fitted is smaller than the error bar of the quantity it is
    fitted from.  So the gate is

        drift := max alpha - min alpha   must exceed  SIGNAL_FLOOR * worst residual,

    i.e. "is there any signal at all above the solve error", which is a different and
    stricter question than "did the solve converge".  Both numbers are recorded at every
    rung so the refusal can be checked rather than taken on trust.
    """
    SIGNAL_FLOOR = 10.0
    t0 = _tick("H4  the third critical point (a = 0.58218, s = 5/2, Lambda^5)")
    a = CRITICAL_POINTS[2]["a"]
    ladder = []
    for K in Ks:
        try:
            b, seed = inviscid_seed(a, K=K, da=da)
            rows = mu_branch(a, 5, list(mus), K=K, da=da, b0=b)
            worst = float(max(r["residual"] for r in rows))
            al = [r["alpha"] for r in rows]
            drift = float(max(al) - min(al))
            sl = alpha_slope(rows)
            ok = bool(worst < 1e-5 and drift > SIGNAL_FLOOR * worst)
            rung = {"K": int(K), "reached": ok, "seed_residual": float(seed["residual"]),
                    "seed_alpha": float(-seed["c_omega"]), "worst_residual": worst,
                    "alpha_drift": drift, "signal_to_residual": float(drift / worst),
                    "alpha_1_if_taken": sl["alpha_1"],
                    "verdict_if_taken": marginal_verdict(sl["alpha_1"]),
                    "rows": [{k: r[k] for k in ("mu", "alpha", "residual",
                                                "lambda_truncation")} for r in rows]}
            for r in rows:
                print(f"    K={K:4d} mu={r['mu']:6.3f}  alpha={r['alpha']:.8f}  "
                      f"res={r['residual']:.2e}  trunc={r['lambda_truncation']:.3e}",
                      flush=True)
            print(f"    K={K:4d}  drift {drift:.2e} vs worst residual {worst:.2e} "
                  f"(signal/residual {drift / worst:.2f});  alpha_1 WOULD be "
                  f"{sl['alpha_1']:+.6f} -> {rung['verdict_if_taken']}"
                  f"   ==> {'ACCEPTED' if ok else 'REFUSED'}", flush=True)
        except Exception as exc:                               # noqa: BLE001
            print(f"    K={K:4d}  NOT REACHED ({type(exc).__name__}: {exc})", flush=True)
            rung = {"K": int(K), "reached": False,
                    "error": f"{type(exc).__name__}: {exc}"}
        ladder.append(rung)
    reached = any(r["reached"] for r in ladder)
    out = {"a": a, "reached": bool(reached), "signal_floor": SIGNAL_FLOOR,
           "ladder": ladder}
    if not reached:
        print("    THIRD POINT NOT REACHED at any K on the ladder -- recorded as a "
              "failure, not dropped.  alpha_1 at the third resonance is UNMEASURED, "
              "and the two-point trend has no third point holding it up.", flush=True)
    _done(t0)
    return out


def h5_dss_reask(mus=(0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0), tol=1e-3):
    """Route-E's negative, re-asked with dissipation on.

    Route-E: the only grid-converged isolated eigenvalues are 0 and -1, the two exact
    symmetry modes; everything else is CONTINUOUS spectrum, and a continuum has no
    eigenvalue to move.  Dissipation is exactly the perturbation that could give it
    some -- so the question is whether the continuum discretizes, and if it does,
    whether anything moves or goes complex.
    """
    t0 = _tick("H5  the DSS re-ask: does dissipation give the continuum eigenvalues?")
    rows = []
    for mu in mus:
        d = converged_dissipative_spectrum(0.0, 1, float(mu), K_coarse=96, K_fine=144,
                                           tol=tol)
        kept = d["kept"]
        n_complex = int(np.sum(np.abs(np.imag(kept)) > 1e-8))
        # A BOOLEAN "any complex?" IS THE WRONG REPORT and the run showed why: at
        # mu = 2 the filter keeps a pair at Re = -3 split by |Im| = 1.8e-5, which is a
        # near-degenerate real pair resolved to noise, not a Hopf.  Quote the LARGEST
        # |Im| so the reader sees 1.8e-5 rather than a True.
        max_im = float(np.max(np.abs(np.imag(kept)))) if kept.size else float("nan")
        max_re = float(np.max(np.real(kept))) if kept.size else float("nan")
        # the mover: the amplitude mode, predicted (empirically) at -sqrt(1+4mu)
        pred = float(amplitude_eigenvalue(mu))
        near = kept[np.argmin(np.abs(np.real(kept) - pred))] if kept.size else np.nan
        # the ladder: converged eigenvalues that sit on negative integers
        ints = sorted({int(round(z.real)) for z in kept
                       if abs(z.real - round(z.real)) < 5e-4 and abs(z.imag) < 1e-8})
        rows.append({"mu": float(mu), "n_kept": int(kept.size),
                     "n_complex_converged": n_complex, "max_real": max_re,
                     "max_abs_imag": max_im,
                     "amplitude_predicted": pred,
                     "amplitude_measured": float(np.real(near)),
                     "integer_ladder": ints,
                     "kept_real": [float(z.real) for z in kept],
                     "kept_imag": [float(z.imag) for z in kept],
                     "n_total": d["n_total"], "alpha_fine": d["alpha_fine"]})
        print(f"    mu={mu:5.2f}  kept {kept.size:2d}/{d['n_total']}  complex {n_complex}"
              f" (max |Im| {max_im:.1e})  max Re {max_re:+.2e}  "
              f"amplitude {float(np.real(near)):+.6f} "
              f"(pred {pred:+.6f})  ladder {ints}", flush=True)
    ctl = planted_dissipative_control(a=0.0, p=1, mu=0.5, strength=6.0, tol=tol)
    print(f"    positive control: {ctl['n_plain']} -> {ctl['n_planted']} converged, "
          f"max Re {float(np.max(np.real(ctl['planted']))):+.3f}", flush=True)
    amp_err = max(abs(r["amplitude_measured"] - r["amplitude_predicted"])
                  for r in rows)
    _done(t0)
    return {"rows": rows, "tol": tol,
            "any_complex_converged": bool(any(r["n_complex_converged"] for r in rows)),
            "worst_abs_imag": float(max(r["max_abs_imag"] for r in rows)),
            "any_positive_real": bool(any(r["max_real"] > 1e-6 for r in rows)),
            "amplitude_formula_worst_error": float(amp_err),
            "control": {"n_plain": ctl["n_plain"], "n_planted": ctl["n_planted"],
                        "max_real_planted": float(np.max(np.real(ctl["planted"])))}}


def h6_verdict(h2, h3):
    """What (M) actually does, with the time scale spelled out."""
    t0 = _tick("H6  the marginal verdict")
    out = []
    for label, a1 in (("a=0 (s=1/2)", h2["slope"]["alpha_1"]),
                      ("a=1/2 (s=3/2)", h3["alpha_1"])):
        row = {"point": label, "alpha_1": a1, "verdict": marginal_verdict(a1),
               "tau_mu_0.2_to_0.02": mu_decay_time(a1, 0.2, 0.02),
               "tau_mu_0.2_to_0.002": mu_decay_time(a1, 0.2, 0.002)}
        out.append(row)
        print(f"    {label:14s}  alpha_1 = {a1:+.6f}  -> {row['verdict']}  "
              f"(tau for mu 0.2->0.02: {row['tau_mu_0.2_to_0.02']:.0f}, "
              f"->0.002: {row['tau_mu_0.2_to_0.002']:.0f})", flush=True)
    _done(t0)
    return out


def h7_time_dependent_crosscheck(n=8192, nus=(1e-2, 1e-3, 1e-4)):
    """AT s = 1/2 exactly, does the time-dependent solver see a PLATEAU (p = 0)?

    Different machinery in every respect: periodic pseudo-spectral, RK4, integrating
    factor, a fitted singular time.  Nothing about the compactified steady solve
    enters it.  Banked lesson 53: a cross-check through unrelated machinery is worth
    more than either side's internal error bar.
    """
    t0 = _tick("H7  time-dependent cross-check at s = 1/2 exactly")
    x = np.arange(n) * 2.0 * np.pi / n
    w0 = np.sin(x) + 0.4 * np.sin(2.0 * x)
    rows = []
    for nu in nus:
        g = FractionalGCLM(n=n, a=0.0, nu=float(nu), s=0.5)
        r = g.run(w0.copy(), amp_factor=1000.0, sample_every=5, max_steps=600000)
        T = estimate_T(r)
        fits = {}
        for lo, hi in ((0.30, 0.90), (0.40, 0.94), (0.50, 0.96)):
            fits[f"{lo}-{hi}"] = fit_relevance(r, T, lo=lo, hi=hi)["p"]
        # EVERY run ends `under_resolved` -- the solver refuses rather than integrate
        # past the tail criterion (banked lesson 45), so record how much of the
        # approach to T was actually captured instead of leaving "under_resolved" to
        # be read as either a failure or a formality.  It is neither: the history up
        # to the break is resolved, and `reached` says how close to T it got.
        rows.append({"nu": float(nu), "outcome": r["outcome"], "T": float(T),
                     "T0": float(clm_blowup_time(w0)), "max_tail": r["max_tail"],
                     "steps": int(r["steps"]),
                     "reached": float(r["t_final"] / T),
                     "p_windows": fits,
                     "p": float(np.mean([v for v in fits.values() if np.isfinite(v)])),
                     "ratio_last": float(r["ratio"][-1]) if r["ratio"].size else None})
        print(f"    nu={nu:.0e}  {r['outcome']:18s} T={T:.5f} (inviscid {rows[-1]['T0']:.5f})"
              f"  p = " + "/".join(f"{v:+.3f}" for v in fits.values())
              + f"   tail {r['max_tail']:.1e}  reached {rows[-1]['reached']:.4f}T",
              flush=True)
    ps = [r["p"] for r in rows if np.isfinite(r["p"])]
    _done(t0)
    return {"rows": rows, "n": n,
            "all_under_resolved": bool(all(r["outcome"] == "under_resolved"
                                           for r in rows)),
            "worst_reached": float(min(r["reached"] for r in rows)),
            "p_mean": float(np.mean(ps)) if ps else float("nan"),
            "p_spread": float(max(ps) - min(ps)) if len(ps) > 1 else float("nan"),
            "predicted_p": 0.0}


# --------------------------------------------------------------------------
def main():
    t_all = time.time()
    res = {"leg": "route_h_v1", "what": "the marginal case: s = s_c exactly"}
    res["h1_exact"] = h1_exact_solution()
    res["h2_a0"] = h2_a0_branch()
    res["h3_a_half"] = h3_a_half_branch()
    res["h4_third_point"] = h4_third_point()
    res["h5_dss"] = h5_dss_reask()
    res["h6_verdict"] = h6_verdict(res["h2_a0"], res["h3_a_half"])
    res["h7_time_dependent"] = h7_time_dependent_crosscheck()
    res["seconds"] = time.time() - t_all
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1, default=float))
    print(f"\nwrote {OUT}  [{res['seconds']:.0f}s]")


if __name__ == "__main__":
    main()
