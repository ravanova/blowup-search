"""Route-I v1: the marginal flow DRIVEN -- the augmented system as an initial-value problem.

THE QUESTION.  Route-H v1 (§29) wrote the augmented flow

    Omega_tau = (c_omega + H Omega) Omega - X Omega_X - a U Omega_X - mu Lambda^{2s} Omega
    mu_tau    = (2 s - alpha[Omega, mu]) mu ,        alpha = -c_omega

and read it STATICALLY: Newton at frozen mu, alpha off the branch, the dynamics inferred.
Two numbers came out that way and neither was ever integrated -- lambda_mu = 2s - alpha_0
(Route-F's critical exponent, as a growth rate) and alpha_1 = d alpha/d mu (the marginal
case, as a curvature).  This leg integrates the coupled system and measures both from a
TRAJECTORY, which also answers the piece of ranked item (2) that §27/§28 left open:

    the scaling says which term dominates GIVEN the self-similar form.  Does a viscous
    solution actually REACH it?

EIGHT MEASUREMENTS:
  I1  the integrator against the one exact answer in the problem -- the a = 0 line of
      viscous self-similar blow-ups, which must be a LINE OF FIXED POINTS of both
      equations at once -- plus the BDF2 order and the gauge invariant;
  I2  lambda_mu = 2s - alpha_0 measured as d(log mu)/d tau, at four s and two signs;
  I3  THE TAR PIT, DRIVEN: mu(tau) at criticality against 1/(alpha_1 tau), with alpha_1
      read off the trajectory and compared to Route-H's static value at MATCHED K;
  I4  ADIABATICITY -- how far the driven trajectory sits from the frozen-mu branch the
      static reading assumed it would hug, and whether an OFF-branch start joins it;
  I5  THE STABILITY INVERSION.  The inviscid fixed point has ~K unstable directions
      (max Re +4.55 at a = 1/2, i.e. §26's essential spectrum); any mu > 0 has none.
      With the crossover mu*(K) ~ maxRe/K^p that says the limits do not commute, which
      is the reading an artifact cannot have;
  I6  WHERE THE INSTABILITY LIVES: Re against |Im|.  The leading inviscid eigenvalue is
      4.55 + 430i and max|Im| grows with K -- these are Route-E's log-periodic modes,
      i.e. the DSS-shaped directions, and they are the fastest-growing ones;
  I7  THE NONLINEAR CONTROL: twin trajectories through the nonlinear flow, against the
      spectral gap;
  I8  the verdict and its time scales.

Deterministic, NOT a logged Tier run (~15 min).  Writes writeup/data/p2_route_i_v1_driven.json.

Run: .venv/bin/python -u experiments/p2_route_i_v1_driven.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.critical_dissipation import (  # noqa: E402
    alpha_slope, marginal_verdict, mu_branch, mu_decay_time,
)
from solver.marginal_flow import (  # noqa: E402
    AugmentedFlow, admissible_direction, crossover_mu, dt_ladder, dynamic_alpha_1,
    dynamic_lambda_mu,
    frequency_profile, integrate, perturbation_decay, resolution_guard, rung_gate,
    stability_ladder, stability_verdict, tar_pit_law,
)

OUT = ROOT / "writeup" / "data" / "p2_route_i_v1_driven.json"

A_CRIT, P_CRIT, ALPHA_0 = 0.5, 3, 3.0        # the one resonance where p = 2s is reachable
# Route-H's static K-ladder for alpha_1 at (a, p) = (1/2, 3), for the matched comparison
STATIC_ALPHA_1 = {96: 0.132770, 144: 0.133470, 192: 0.133628, 240: 0.133683}


def _tick(name):
    print(f"\n--- {name} ---", flush=True)


def i1_integrator(res):
    """The a = 0 neutral line, the BDF2 order, and the gauge."""
    _tick("I1 the integrator against the exact answer")
    rows = []
    # a LADDER, not five separate solves: Newton misses the branch if it is asked to
    # jump from the inviscid anchor straight to mu = 2, and the garbage seed then
    # overflows the integrator.  Continuation FOLLOWS the family instead.
    seeds = mu_branch(0.0, 1, [0.25, 0.5, 1.0, 2.0, 4.0], K=96)
    for seed in seeds:
        mu0, b = seed["mu"], seed["b"]
        A = AugmentedFlow(0.0, 1, K=96)
        rec = integrate(A, b, mu0, 40.0, 0.5, n_sample=20)
        rows.append({"mu0": mu0, "mu_end": rec["mu_end"],
                     "d_mu": rec["mu_end"] - mu0,
                     "d_omega": float(np.max(np.abs(rec["b_end"] - b))),
                     "gauge_drift": rec["gauge_drift"]})
        print(f"  a=0 mu0={mu0:<5g} dmu {rows[-1]['d_mu']:+.2e}  "
              f"dOmega {rows[-1]['d_omega']:.2e}  gauge {rows[-1]['gauge_drift']:+.1e}")

    L = dt_ladder(A_CRIT, P_CRIT, 96, 0.3, 60.0, [1.0, 0.5, 0.25, 0.125],
                  mu_max=0.3, n_sample=120)
    print(f"  BDF2 order {L['observed_order']:.3f}; alpha_1 spread over the dt-ladder "
          f"{L['spread']:.2e}; signal/discretization {L['signal_over_discretization']:.0f}")

    b = mu_branch(A_CRIT, P_CRIT, [0.1, 0.2, 0.3], K=96)[-1]["b"]
    on = integrate(AugmentedFlow(A_CRIT, P_CRIT, K=96, gauge_project=True),
                   b, 0.3, 60.0, 0.25, n_sample=60)
    off = integrate(AugmentedFlow(A_CRIT, P_CRIT, K=96, gauge_project=False),
                    b, 0.3, 60.0, 0.25, n_sample=60)
    gauge = {"drift_projected": on["gauge_drift"], "drift_raw": off["gauge_drift"],
             "cos_violation": on["gauge_violation"], "rhs_scale": on["rhs_scale"],
             "mu_end_projected": on["mu_end"], "mu_end_raw": off["mu_end"],
             "headline_shift_rel": abs(on["mu_end"] - off["mu_end"]) / on["mu_end"]}
    print(f"  gauge: {gauge['drift_projected']:+.1e} projected vs "
          f"{gauge['drift_raw']:+.1e} raw; the headline moves "
          f"{gauge['headline_shift_rel'] * 100:.3f}%")
    res["i1_integrator"] = {"neutral_line": rows, "dt_ladder": L, "gauge": gauge}


def i2_lambda_mu(res):
    """Route-F's s_c, measured as the growth rate of mu."""
    _tick("I2 lambda_mu = 2s - alpha_0 as a growth rate")
    rows = []
    # ALPHA_0_OFF is Route-E's inviscid exponent at a = 0.3, an OUTPUT of a different
    # module -- so the off-resonance prediction is not read off this computation either.
    ALPHA_0_OFF = 1.6172
    for a, alpha_0, ps in ((A_CRIT, ALPHA_0, (1, 2, 3, 4, 5)),
                           (0.3, ALPHA_0_OFF, (1, 2, 3))):
        for p in ps:
            seed = mu_branch(a, p, [2e-3], K=96)[0]
            gate = rung_gate(seed)
            rec = integrate(AugmentedFlow(a, p, K=96), seed["b"], 2e-3, 3.0, 0.02,
                            n_sample=60)
            d = dynamic_lambda_mu(rec)
            refused = bool(d.get("refused")) or not gate["passed"]
            reason = d.get("reason") or gate["reason"]
            rows.append({"a": a, "p": p, "s": 0.5 * p, "alpha_0": float(alpha_0),
                         "predicted": float(p - alpha_0), "measured": d["lambda_mu"],
                         "refused": refused, "reason": reason,
                         "seed_residual": gate["residual"],
                         "lambda_truncation": gate["lambda_truncation"],
                         "fit_residual": d.get("fit_residual"),
                         "n_points": d["n_points"],
                         "abs_error": abs(d["lambda_mu"] - (p - alpha_0))})
            mark = "REFUSED: " if refused else ""
            print(f"  a={a} p={p} (s={p/2}): predicted {p - alpha_0:+.4f}  "
                  f"{mark}measured {d['lambda_mu']:+.5f}  "
                  f"|err| {rows[-1]['abs_error']:.1e}  "
                  f"[res {gate['residual']:.1e}, trunc {gate['lambda_truncation']:.2e}]")
            if refused:
                print(f"        -> {reason}")
    # the line: slope in s and the zero, both against the prediction
    kept = [r for r in rows if not r["refused"]]
    sub = [r for r in kept if r["a"] == A_CRIT]
    s = np.array([r["s"] for r in sub])
    m = np.array([r["measured"] for r in sub])
    c = np.polyfit(s, m, 1)
    res["i2_lambda_mu"] = {
        "rows": rows, "slope": float(c[0]), "slope_predicted": 2.0,
        "zero": float(-c[1] / c[0]), "zero_predicted": float(ALPHA_0 / 2),
        "n_refused": int(len(rows) - len(kept)),
        "worst_abs_error": float(max(r["abs_error"] for r in kept))}
    print(f"  the line at a={A_CRIT}: slope {c[0]:+.5f} (predicted +2), "
          f"zero at s = {-c[1] / c[0]:.5f} (predicted {ALPHA_0 / 2})")


def i3_tar_pit(res):
    """The marginal trajectory, and alpha_1 from it."""
    _tick("I3 the tar pit, driven")
    K_LADDER = (96, 144, 192)
    ladder, traj = [], None
    for K in K_LADDER:
        b = mu_branch(A_CRIT, P_CRIT, [0.05, 0.1, 0.2, 0.3], K=K)[-1]["b"]
        A = AugmentedFlow(A_CRIT, P_CRIT, K=K)
        t0 = time.time()
        rec = integrate(A, b, 0.3, 120.0, 0.25, n_sample=240)
        d = dynamic_alpha_1(rec, mu_max=0.3)
        static = STATIC_ALPHA_1[K]
        ladder.append({"K": K, "dynamic": d["alpha_1"], "static": static,
                       "rel_diff": abs(d["alpha_1"] - static) / static,
                       "fit_residual_rel": d["fit_residual_rel"],
                       "seconds": time.time() - t0})
        print(f"  K={K}: dynamic {d['alpha_1']:.6f}  static {static:.6f}  "
              f"{ladder[-1]['rel_diff'] * 100:.3f}% apart  ({ladder[-1]['seconds']:.1f}s)")
        if K == 96:
            traj = rec
    # the window sweep: is the number the window, or the number?
    windows = []
    for mm in (0.3, 0.25, 0.2, 0.15, 0.1):
        d = dynamic_alpha_1(traj, mu_max=mm)
        windows.append({"mu_max": mm, "alpha_1": d["alpha_1"], "n": d["n_points"]})
    spread = max(w["alpha_1"] for w in windows) - min(w["alpha_1"] for w in windows)
    print(f"  fit-window sweep mu<=0.30..0.10: spread {spread:.2e} "
          f"(Route-F's dominant systematic is NOT dominant here)")
    # the long run: the trajectory against the closed law
    A = AugmentedFlow(A_CRIT, P_CRIT, K=96)
    b = mu_branch(A_CRIT, P_CRIT, [0.05, 0.1, 0.2, 0.3], K=96)[-1]["b"]
    long = integrate(A, b, 0.3, 600.0, 0.5, n_sample=300, branch_every=10)
    a1 = ladder[0]["dynamic"]
    law = tar_pit_law(a1, 0.3, np.array(long["tau"]))
    dev = float(np.max(np.abs(np.array(long["mu"]) - law) / law))
    print(f"  tau = 0 .. 600: mu {0.3:.3f} -> {long['mu_end']:.6f}; "
          f"worst deviation from 1/(alpha_1 tau) is {dev * 100:.2f}%")
    res["i3_tar_pit"] = {
        "k_ladder": ladder, "window_sweep": windows, "window_spread": float(spread),
        "long_run": {"tau": long["tau"], "mu": long["mu"], "alpha": long["alpha"],
                     "mu_end": long["mu_end"], "law_max_rel_dev": dev,
                     "alpha_1_used": a1, "gauge_drift": long["gauge_drift"]},
        "branch": {"tau": long["branch_tau"], "dist": long["branch_dist"]}}
    res["_long"] = long


def i4_adiabaticity(res):
    """Does the driven trajectory hug the frozen-mu branch, and does an off-branch
    start join it?"""
    _tick("I4 adiabaticity, and the off-branch start")
    long = res.pop("_long")
    d = np.array(long["branch_dist"])
    print(f"  distance to the frozen-mu branch: {d[0]:.2e} -> {d[-1]:.2e} "
          f"over tau = 0 .. {long['tau_end']:.0f}")
    # start OFF the branch: perturb Omega and let mu run
    K = 96
    b = mu_branch(A_CRIT, P_CRIT, [0.05, 0.1, 0.2, 0.3], K=K)[-1]["b"]
    A0 = AugmentedFlow(A_CRIT, P_CRIT, K=K)
    # NORMALIZED IN THE FUNCTIONAL THE GAUGE READS, not in coefficient sup-norm.  The
    # first version of this stage used the latter, which made "eps = 1e-3" a 3.6e5
    # relative perturbation of (Lambda^p Omega)_X(0) and overflowed every run; see
    # `admissible_direction` for the measurement.  The ratio is reported so the
    # correction is visible rather than silently applied.
    v = admissible_direction(A0, b, seed=7)
    lam = A0.flow.lam_dx0
    naive = np.random.default_rng(7).standard_normal(K) * np.exp(
        -0.25 * np.arange(K))
    naive = naive - (A0.kk @ naive) / (A0.kk @ A0.kk) * A0.kk
    naive = naive / np.max(np.abs(naive))
    norm_ratio = abs(float(lam @ naive)) / abs(float(lam @ b))
    print(f"  perturbation normalized in |(Lambda^p Om)_X(0)|, not in max|v_k|: the "
          f"coefficient-normalized direction is {norm_ratio:.1e}x larger in that "
          f"functional")
    # AND SAY HOW BIG THE ADMISSIBLE PERTURBATION ACTUALLY IS IN PROFILE TERMS, because
    # it is the qualification the headline needs.  lam_dx0 weights mode k by ~k^p with
    # one more power from d/dX at the origin, so the functional's condition number is
    # ~K^4 -- the SAME k^p amplification Route-H (H4) found killing Lambda^5.  A 5%
    # perturbation of the gauge functional is therefore a ~1e-11 relative change in the
    # profile: this is a strong test of the gauge-sensitive direction and a WEAK test of
    # profile-scale robustness.  I7's twin trajectories are the profile-scale one.
    profile_rel = float(np.max(np.abs(v)) / np.max(np.abs(b)))
    print(f"  BUT in profile terms the admissible direction is tiny: eps=0.05 is a "
          f"{0.05 * profile_rel:.1e} relative change in Omega -- the gauge functional is "
          f"ill-conditioned by ~K^4, so this tests the gauge direction, NOT the basin")
    rows = []
    ref = integrate(AugmentedFlow(A_CRIT, P_CRIT, K=K), b, 0.3, 120.0, 0.25, n_sample=120)
    for eps in (1e-3, 1e-2, 5e-2):
        rec = integrate(AugmentedFlow(A_CRIT, P_CRIT, K=K), b + eps * v, 0.3, 120.0,
                        0.25, n_sample=120)
        row = {"eps": eps, "converged": bool(rec["converged"]),
               "mu_end": rec["mu_end"],
               "diverged_at_tau": rec.get("diverged_at_tau")}
        if rec["converged"]:
            row["rel_to_on_branch"] = abs(rec["mu_end"] - ref["mu_end"]) / ref["mu_end"]
            row["alpha_1"] = dynamic_alpha_1(rec, mu_max=0.3)["alpha_1"]
            print(f"  off-branch start eps={eps:<6g}: mu(120) {rec['mu_end']:.6f} vs "
                  f"{ref['mu_end']:.6f} on-branch  "
                  f"({row['rel_to_on_branch'] * 100:.3f}%)"
                  f"   alpha_1 {row['alpha_1']:.6f}")
        else:
            # REFUSED, and recorded -- never emitted as a NaN into a figure legend.
            row["rel_to_on_branch"] = None
            row["alpha_1"] = None
            print(f"  off-branch start eps={eps:<6g}: REFUSED -- trajectory left the "
                  f"finite range at tau = {rec.get('diverged_at_tau')}")
        rows.append(row)
    res["i4_adiabaticity"] = {
        "branch_tau": long["branch_tau"], "branch_dist": long["branch_dist"],
        "dist_first": float(d[0]), "dist_last": float(d[-1]),
        "off_branch": rows, "on_branch_mu_end": ref["mu_end"],
        "norm_ratio_coeff_vs_gauge_functional": float(norm_ratio),
        "off_branch_profile_relative_at_eps_0.05": float(0.05 * profile_rel),
        "off_branch_tests": "the GAUGE direction, not the basin (see i7 for profile scale)",
        "n_off_branch_refused": int(sum(1 for r in rows if not r["converged"]))}


def i5_stability_inversion(res):
    """~K unstable directions at mu = 0, none at any mu > 0, and the crossover."""
    _tick("I5 the stability inversion")
    mus = [0.0, 1e-8, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.05, 0.2, 0.5]
    out = {}
    for K in (48, 96, 144):
        t0 = time.time()
        rows = stability_ladder(A_CRIT, P_CRIT, K, mus)
        cross = crossover_mu(rows)
        clean = [{k: r[k] for k in ("mu", "n_unstable", "max_re", "gap", "min_re",
                                    "max_abs_im", "residual", "dilation_eigenvalue",
                                    "lambda_truncation")} for r in rows]
        pred = rows[0]["max_re"] / K ** P_CRIT
        out[str(K)] = {"rows": clean, "crossover": cross, "crossover_predicted": pred,
                       "verdict": stability_verdict(rows),
                       "n_unstable_inviscid": rows[0]["n_unstable"],
                       "max_re_inviscid": rows[0]["max_re"]}
        print(f"  K={K}: mu=0 -> {rows[0]['n_unstable']}/{K} unstable, max Re "
              f"{rows[0]['max_re']:+.4f}; mu>0 -> "
              f"{[r['n_unstable'] for r in rows[1:]]}")
        print(f"        crossover bracketed by {cross['bracket']}, (C) predicts "
              f"{pred:.1e}   ({time.time() - t0:.0f}s)")
    ratios = {}
    for lo, hi in ((48, 96), (96, 144)):
        ratios[f"{lo}->{hi}"] = {
            "measured": out[str(lo)]["crossover"]["geometric_mid"]
            / out[str(hi)]["crossover"]["geometric_mid"],
            "predicted": (hi / lo) ** P_CRIT}
        print(f"  crossover falls x{ratios[f'{lo}->{hi}']['measured']:.1f} from K={lo} "
              f"to K={hi}; (C) predicts x{ratios[f'{lo}->{hi}']['predicted']:.0f}")
    guard = resolution_guard(A_CRIT, P_CRIT, 96, 0.02,
                             g=out["96"]["max_re_inviscid"])
    print(f"  resolution guard for the I3 trajectory (mu >= 0.02 at K=96): "
          f"K_required {guard['K_required']:.1f}, margin x{guard['margin']:.0f}")
    res["i5_stability"] = {"ladders": out, "crossover_ratios": ratios, "guard": guard,
                           "mus": mus}


def i6_where_the_instability_lives(res):
    """Re against |Im| -- the unstable directions are the log-periodic ones."""
    _tick("I6 where the instability lives")
    rows = []
    for K in (48, 96, 144):
        fp = frequency_profile(A_CRIT, P_CRIT, K, 0.0)
        rows.append(fp)
        caps = ", ".join(f"|Im|<={c}: {v['max_re']:+.3f}"
                         for c, v in fp["caps"].items())
        print(f"  K={K}: leading {fp['max_re']:+.4f} {fp['im_of_max_re']:+.1f}i, "
              f"max|Im| {fp['max_abs_im']:.0f}")
        print(f"        max Re restricted -- {caps}")
    visc = frequency_profile(A_CRIT, P_CRIT, 96, 0.05)
    print(f"  and with mu = 0.05: max Re {visc['max_re']:+.3e}, max|Im| "
          f"{visc['max_abs_im']:.1f} -- the log-periodic band is gone, not damped")
    res["i6_frequency"] = {"inviscid": rows, "viscous": visc}


def i7_nonlinear_control(res):
    """Twin trajectories through the nonlinear flow, against the spectral gap."""
    _tick("I7 the nonlinear control")
    K = 96
    rows = []
    ladder = {str(r["mu"]): r for r in res["i5_stability"]["ladders"]["96"]["rows"]}
    for mu, eps in ((0.0, 1e-9), (1e-3, 1e-8), (0.05, 1e-8), (0.2, 1e-8)):
        r = perturbation_decay(A_CRIT, P_CRIT, K, mu, eps=eps, tau_end=6.0, dt=0.01)
        gap = ladder[str(float(mu))]["gap"]
        rows.append({"mu": mu, "rate": r["rate"], "gap": gap,
                     "rel": abs(r["rate"] - gap) / abs(gap),
                     "fit_residual": r["fit_residual"],
                     "growth_factor": r["growth_factor"],
                     "im_resolved": r["im_resolved"],
                     "tau": r["tau"][::10], "amp": r["amp"][::10]})
        print(f"  mu={mu:<7g}: twin-trajectory rate {r['rate']:+.4f}  spectral gap "
              f"{gap:+.4f}  ({rows[-1]['rel'] * 100:.1f}%)  kick x{r['growth_factor']:.1e}")
    print("  NOTE the mu = 0 row is a LOWER BOUND: dt = 0.01 resolves |Im| <~ 314 and "
          "the leading eigenvalue sits at |Im| = 430")
    res["i7_nonlinear"] = {"rows": rows}


def i8_verdict(res):
    _tick("I8 the verdict")
    a1 = res["i3_tar_pit"]["k_ladder"][-1]["dynamic"]
    v = marginal_verdict(a1)
    times = {str(t): mu_decay_time(a1, 0.3, t) for t in (0.1, 0.03, 0.01, 0.003, 0.001)}
    print(f"  alpha_1 (dynamic, finest K) = {a1:.6f} -> {v}")
    for t, tau in times.items():
        print(f"    mu 0.3 -> {t}: tau = {tau:.0f}")
    res["i8_verdict"] = {"alpha_1": a1, "verdict": v, "decay_times": times,
                         "stability_verdict":
                         res["i5_stability"]["ladders"]["144"]["verdict"]}


def main():
    t0 = time.time()
    res = {"leg": "route_i_v1", "a_crit": A_CRIT, "p_crit": P_CRIT,
           "alpha_0": ALPHA_0, "static_alpha_1": STATIC_ALPHA_1}
    i1_integrator(res)
    i2_lambda_mu(res)
    i3_tar_pit(res)
    i4_adiabaticity(res)
    i5_stability_inversion(res)
    i6_where_the_instability_lives(res)
    i7_nonlinear_control(res)
    i8_verdict(res)
    res["seconds"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['seconds']:.0f}s)")


if __name__ == "__main__":
    main()
