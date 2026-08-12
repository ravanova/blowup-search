"""
Leg 377 -- Route-HCDX: does Boyd (1980)'s coefficient-decay concern kill leg 374's
surviving generalized-Hermite basis candidate (weight (1+x^2)^{-gamma}, Zhang-Guo /
Guo-Zhang family) for route 4's Galerkin-plus-tail bridge?

UNDERDETERMINED-THEN-MEASURED branch. Read alone could not resolve this: every
sourced route to Zhang-Guo (2014)/Guo-Zhang (2015)'s own theorem statement returned
HTTP 403 (ScienceDirect, Springer, ResearchGate, the authors' own faculty mirror --
all blocked this leg, same as leg 374 found). The one open-access, directly-on-topic,
current (2024-2026) literature this leg *could* reach in full (Hu & Yu, arXiv:2412.08044
and arXiv:2602.03083, "(Scaling Optimized) Generalized Hermite/Laguerre Approximation
Methods") turned out, on full read, to define "generalized Hermite functions" as
GAUSSIAN-enveloped (weight |x|^{2mu} e^{-x^2}) with an added *power singularity at the
origin* -- a different basis family from Zhang-Guo's algebraically-enveloped
(1+x^2)^{-gamma} construction that is actually leg 374's candidate. That paper's own
finding (algebraic-decay targets get only algebraic, not geometric, convergence even
under optimal scaling, because Gaussian-enveloped Hermite functions are approximate
Fourier self-dual and can't localize in both space and frequency at once) is real and
load-bearing background, but it does NOT transfer directly to leg 374's actual
candidate, whose basis functions decay algebraically (not via e^{-x^2}) and so are not
subject to that specific Fourier-duality obstruction.

So this leg measures directly. The construction below is the leg's own, exact and
checkable: polynomials orthogonal on R w.r.t. weight (1+x^2)^{-gamma} are, under the
algebraic bijection t = x/sqrt(1+x^2) (R -> (-1,1)), exactly (up to a normalization
constant that does not affect the *decay rate* measured here) Gegenbauer/ultraspherical
polynomials C_n^{(gamma-1)}(t) orthogonal w.r.t. the classical weight (1-t^2)^{alpha-1/2},
alpha = gamma-1. This is elementary and independently checkable (dx = (1+x^2) dtheta
under x=tan(theta), t=sin(theta); worked out in the docstring of `alpha_of`/`g_of_t`
below and cross-checked numerically by the R2 fits themselves, not asserted on faith).

The test: expand g(t) = u(x(t)) * (1+x(t)^2)^{gamma/2} (the "generalized Hermite
function" coefficient integrand) in this Gegenbauer system, for a target
u(x) = 1/(4+x^2)^(s/2) -- analytic on all of R (poles at x=+-2i, off the real axis),
decaying at the SAME algebraic rate |x|^{-s} that route 4's own object is pinned to
(leg 260: rho = (1+|y|)^{-s}, s>1, sharp threshold). Two regimes are measured and
fit against BOTH a geometric model (log|c_n| ~ a*n+b) and an algebraic model
(log|c_n| ~ a*log(n)+b), scored by R^2 of each fit -- an instrument that can, by
construction, tell the two regimes apart (this is the falsifiability check: a random
or badly-designed basis would show neither fit dominating cleanly):

  MATCHED   (basis weight gamma == target's own decay exponent s):
            g(t) is then analytic on the CLOSED interval [-1,1] including both
            endpoints (t=+-1 are the images of x=+-infinity) -- classical spectral
            theory (Bernstein-ellipse argument) then predicts GEOMETRIC decay.
  MISMATCHED (gamma != s, by a fixed offset delta):
            g(t) then carries an explicit (1-t^2)^{(s-gamma)/2} factor, a genuine
            non-integer-power branch point exactly at t=+-1 (the mapped-infinity
            points) unless delta is an even integer -- classical theory then predicts
            only ALGEBRAIC decay, with an order that grows with |delta|.

Both predictions are measured, not assumed: this leg computes c_n via numerical
quadrature (scipy.integrate.quad, tight tolerances) for even n=0..60 (odd
coefficients vanish identically by symmetry -- g is an even function of t for these
targets -- and are not fit), then fits both models via least squares and reports R^2
for each, across a spread of s (matched case) and delta (mismatched case) to check
the result is not a coincidence of one parameter choice.

No ban touched. Nothing beyond this arithmetic-only numerical experiment is claimed:
this measures ONE well-posed instance of the coefficient-decay question for the
Zhang-Guo weight family, on an analytic target with route 4's own decay exponent
class; it does not itself certify a Galerkin-plus-tail bridge, does not touch
solver/, capabilities.py, test_*.py, or plan_of_record.py.
"""

import numpy as np
from scipy.special import eval_gegenbauer, gamma as Gamma
from scipy.integrate import quad
import json
import warnings


def alpha_of(gamma_w):
    """Gegenbauer parameter alpha = gamma_w - 1, per the R->(-1,1) map derivation
    in this file's module docstring (weight (1+x^2)^{-gamma_w} on R becomes weight
    (1-t^2)^{alpha-1/2} on (-1,1) under t = x/sqrt(1+x^2))."""
    return gamma_w - 1.0


def g_of_t(t, s, gamma_w):
    """g(t) = u(x(t)) * (1+x(t)^2)^{gamma_w/2}, for u(x) = 1/(4+x^2)^(s/2),
    x(t) = t/sqrt(1-t^2). Closed form (derived algebraically, not numerically):
        g(t) = (1-t^2)^{(s-gamma_w)/2} / (4 - 3 t^2)^{s/2}
    """
    return (1 - t**2) ** ((s - gamma_w) / 2.0) / (4 - 3 * t**2) ** (s / 2.0)


def gegenbauer_norm2(n, alpha):
    """L^2 norm^2 of C_n^alpha under the standard weight (1-t^2)^{alpha-1/2} on
    [-1,1] (Abramowitz & Stegun 22.2.3 / standard Gegenbauer normalization)."""
    num = np.pi * (2 ** (1 - 2 * alpha)) * Gamma(n + 2 * alpha)
    den = (n + alpha) * Gamma(n + 1) * (Gamma(alpha) ** 2)
    return num / den


def coeff(n, alpha, s, gamma_w):
    f = lambda t: g_of_t(t, s, gamma_w) * eval_gegenbauer(n, alpha, t) * (1 - t**2) ** (alpha - 0.5)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        val, err = quad(f, -1, 1, limit=400, epsabs=1e-13, epsrel=1e-13)
    return val / gegenbauer_norm2(n, alpha)


def run(s, gamma_w, N):
    alpha = alpha_of(gamma_w)
    return np.array([coeff(n, alpha, s, gamma_w) for n in range(N + 1)])


def fit_both(ns, c):
    """Fit log|c_n| vs n (geometric model) and vs log(n) (algebraic model) by
    least squares; return (geo_slope, geo_R2, alg_slope, alg_R2)."""
    mask = ns > 0
    n_ = ns[mask]
    logn = np.log(n_)
    logc = np.log(np.abs(c[mask]))
    ss_tot = np.sum((logc - logc.mean()) ** 2)

    A1 = np.vstack([n_, np.ones_like(n_)]).T
    sol1, *_ = np.linalg.lstsq(A1, logc, rcond=None)
    r2_geo = 1 - np.sum((logc - A1 @ sol1) ** 2) / ss_tot

    A2 = np.vstack([logn, np.ones_like(logn)]).T
    sol2, *_ = np.linalg.lstsq(A2, logc, rcond=None)
    r2_alg = 1 - np.sum((logc - A2 @ sol2) ** 2) / ss_tot

    return sol1[0], r2_geo, sol2[0], r2_alg


def main():
    N = 60
    ns = np.arange(0, N + 1, 2)  # even only; odd coefficients vanish by symmetry
    results = {"N": N, "s_sweep_matched": [], "delta_sweep_mismatched": []}

    print("=== MATCHED case: basis weight exponent gamma_w == target decay exponent s ===")
    print("(prediction: g(t) analytic on closed [-1,1] -> geometric coefficient decay)")
    for s in [1.1, 1.5, 2.0, 3.0]:
        cs = run(s, s, N)
        geo_slope, geo_r2, alg_slope, alg_r2 = fit_both(ns, cs[ns])
        print(f"  s={s:4.2f}  geo_slope={geo_slope:8.4f}  geo_R2={geo_r2:.6f}   "
              f"alg_R2={alg_r2:.4f}   -> {'GEOMETRIC' if geo_r2 > alg_r2 else 'ALGEBRAIC'} dominates")
        results["s_sweep_matched"].append(dict(s=s, geo_slope=geo_slope, geo_R2=geo_r2, alg_R2=alg_r2))

    print()
    print("=== MISMATCHED case: gamma_w = s + delta, s=1.5 fixed (route 4's own s>1 class) ===")
    print("(prediction: g(t) has a (1-t^2)^{(s-gamma_w)/2} branch point at t=+-1 -> algebraic decay)")
    s0 = 1.5
    for delta in [0.25, 0.5, 1.0, 2.0]:
        cs = run(s0, s0 + delta, N)
        geo_slope, geo_r2, alg_slope, alg_r2 = fit_both(ns, cs[ns])
        print(f"  delta={delta:4.2f}  alg_slope={alg_slope:7.3f}  alg_R2={alg_r2:.6f}   "
              f"geo_R2={geo_r2:.4f}   -> {'ALGEBRAIC' if alg_r2 > geo_r2 else 'GEOMETRIC'} dominates")
        results["delta_sweep_mismatched"].append(
            dict(delta=delta, alg_slope=alg_slope, alg_R2=alg_r2, geo_R2=geo_r2)
        )

    print()
    print("=== Verdict ===")
    matched_all_geo = all(r["geo_R2"] > r["alg_R2"] for r in results["s_sweep_matched"])
    mismatched_all_alg = all(r["alg_R2"] > r["geo_R2"] for r in results["delta_sweep_mismatched"])
    verdict = "ADEQUATE" if (matched_all_geo and mismatched_all_alg) else "INADEQUATE-OR-INCONCLUSIVE"
    print(f"matched-case geometric-dominates-in-all-s: {matched_all_geo}")
    print(f"mismatched-case algebraic-dominates-in-all-delta: {mismatched_all_alg}")
    print(f"VERDICT: {verdict}")
    results["verdict"] = verdict
    results["matched_all_geometric"] = bool(matched_all_geo)
    results["mismatched_all_algebraic"] = bool(mismatched_all_alg)

    # Territory note: this script prints its full numeric result to stdout only.
    # The numbers are transcribed by hand into writeup/data/p2_route_hcdx_v1.json
    # (this leg's declared territory file) -- no file outside declared territory
    # is written by this script.
    print("\n(Full result dict, for manual transcription into "
          "writeup/data/p2_route_hcdx_v1.json:)")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
