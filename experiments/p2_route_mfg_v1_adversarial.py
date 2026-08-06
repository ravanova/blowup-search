"""Route-MFG v1 (leg 83): ADVERSARIAL AUDIT of gate 11's catch coverage.

WHAT IS UNDER TEST, EXACTLY
---------------------------------------------------------------------------
`capabilities.py` line 85 records, for `solver/marginal_flow.py`:

    "`integrate` reports `converged` and gate 11 enforces it (the NaN of leg 41)"

The predicate itself is three clauses, at the bottom of `integrate`:

    converged = finite(y)  AND  "diverged_at_tau" not in rec  AND  worst_res < 1e8

with `worst_res = max over steps of (Newton residual / its floor)`.  Gate 11 is
`test_marginal_flow.py::test_11_small_is_norm_dependent_and_divergence_is_refused`,
whose (b) half asserts that predicate on exactly two trajectories: the leg-41
naive-perturbation trap, which ends in a **NaN**, and one healthy on-branch run.

Every clause of the predicate is an observable of the *inner nonlinear solve* or of
IEEE finiteness.  Not one of them is an observable of the *state*.  The novelty pass
(`writeup/novelty/leg_83.md`, Q2/Q3) recorded this before construction, together with
the prediction it implies: a trajectory that diverges while keeping its inner Newton
well-conditioned will be classified `converged = True`.  This module measures that,
rather than arguing it.

METHOD
---------------------------------------------------------------------------
`integrate` is called on its REAL code path.  What is swapped is the flow object: a
`SyntheticFlow` duck-types `AugmentedFlow` (`.K/.a/.p/.s/.rhs/.jacobian/.alpha/.gauge/
.gauge_violation/.gauge_correction/.rhs_scale`) and supplies a right-hand side whose
exact solution is known in closed form.  So for every battery member:

  * the GROUND TRUTH is analytic -- "divergent" means the exact solution is unbounded
    in tau or has no limit, not "it looked big";
  * the integrator's fidelity is measured and ENFORCED.  A case counts toward the
    catch statistic only if the COMPUTED trajectory is verified to still exhibit the
    divergence its exact solution has.  This is not bookkeeping: measured here,
    `osc_stiff_underresolved` (omega dt = 4 rad/step) is damped to amplitude 0 by
    BDF2's own L-stability, so the trajectory the gate actually saw DID converge and
    calling it a miss would be blaming the gate for the integrator.  It is excluded
    from the statistic and reported separately as a distinct hazard;
  * the gate's own discriminator is reported as a MAGNITUDE, not a boolean:
    `newton_headroom = 1e8 / worst_newton_residual_over_floor` says by what factor the
    trajectory failed to trip the threshold.

Two LIVE controls run the real `AugmentedFlow` -- the leg-41 NaN trap and the healthy
on-branch trajectory, byte-for-byte the two inside gate 11 -- so that a "miss" cannot
be an artifact of the synthetic harness: the harness must reproduce gate 11's known
verdicts before its new verdicts mean anything.

Run:  python experiments/p2_route_mfg_v1_adversarial.py
Out:  writeup/data/p2_route_mfg_v1_adversarial.json
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.critical_dissipation import mu_branch                       # noqa: E402
from solver.marginal_flow import AugmentedFlow, integrate               # noqa: E402

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "writeup", "data", "p2_route_mfg_v1_adversarial.json")

# The threshold the predicate under test uses, mirrored here so the audit reports a
# headroom rather than re-deriving it.  Kept in sync by `test_marginal_flow_adversarial`.
NEWTON_STAGNATION = 1e8


# --------------------------------------------------------------------------
# FIDELITY: did the COMPUTED trajectory actually do what the exact one does?
#
# One criterion per battery member, keyed by name, each returning (ok, description).
# A divergent member that fails its criterion is EXCLUDED from the catch statistic:
# the gate cannot be charged with missing a divergence the integrator never produced.
# The criteria are stated in whatever quantity is meaningful for the member -- a
# relative endpoint error for polynomial growth, a FITTED RATE for exponential growth
# (where an endpoint error over 130 decades is meaningless), a retained amplitude for
# oscillation, an absolute smallness for decay.
# --------------------------------------------------------------------------
FIDELITY = {
    "mu_linear": lambda o: (o["rel_err_vs_exact"] < 1e-6,
                            "rel_err_vs_exact %.2e < 1e-6" % o["rel_err_vs_exact"]),
    "mu_quartic": lambda o: (o["rel_err_vs_exact"] < 0.05,
                             "rel_err_vs_exact %.2e < 0.05" % o["rel_err_vs_exact"]),
    "b_quadratic": lambda o: (o["rel_err_vs_exact"] < 0.05,
                              "rel_err_vs_exact %.2e < 0.05" % o["rel_err_vs_exact"]),
    "mu_exp_mild": lambda o: (abs(o["fit_exponential_rate"] / 0.5 - 1.0) < 0.05,
                              "fitted rate %.4f vs exact 0.5" % o["fit_exponential_rate"]),
    "mu_exp_extreme": lambda o: (abs(o["fit_exponential_rate"] / 5.0 - 1.0) < 0.05,
                                 "fitted rate %.4f vs exact 5.0" % o["fit_exponential_rate"]),
    "mu_negative_runaway": lambda o: (
        abs(o["fit_exponential_rate"] / 0.5 - 1.0) < 0.05 and o["mu_end"] < 0.0,
        "fitted rate %.4f vs exact 0.5, and mu_end %.3e stayed negative"
        % (o["fit_exponential_rate"], o["mu_end"])),
    "osc_sustained": lambda o: (0.5 <= o["numerical_damping_factor"] <= 2.0,
                                "amplitude retained %.3f of exact"
                                % o["numerical_damping_factor"]),
    "osc_growing": lambda o: (0.5 <= o["numerical_damping_factor"] <= 2.0,
                              "amplitude retained %.3f of exact"
                              % o["numerical_damping_factor"]),
    "osc_stiff_underresolved": lambda o: (0.5 <= o["numerical_damping_factor"] <= 2.0,
                                          "amplitude retained %.3e of exact"
                                          % o["numerical_damping_factor"]),
    "nan_finite_time_blowup": lambda o: (
        (not o["clause_finite"]) or (not o["clause_no_nan_break"])
        or o["worst_newton_iters"] >= 10,
        "the blowup was reached: worst Newton iters %d, finite=%s"
        % (o["worst_newton_iters"], o["clause_finite"])),
    "decay_to_zero": lambda o: (abs(o["mu_end"]) < 1e-6 * 0.3,
                                "|mu_end| %.2e < 1e-6 mu0" % abs(o["mu_end"])),
    "exact_fixed_point": lambda o: (o["rel_err_vs_exact"] < 1e-12,
                                    "rel_err_vs_exact %.2e < 1e-12"
                                    % o["rel_err_vs_exact"]),
    "damped_oscillation": lambda o: (o["amp_end_computed"] < 1e-3,
                                     "amp_end %.2e < 1e-3" % o["amp_end_computed"]),
}


# --------------------------------------------------------------------------
# the harness: a flow object `integrate` cannot tell from AugmentedFlow
# --------------------------------------------------------------------------
class SyntheticFlow:
    """Minimal duck-type of `AugmentedFlow` carrying an arbitrary smooth rhs.

    `a`, `p`, `s` are carried only because `integrate` copies them into the record;
    nothing here depends on their values.  `gauge`/`alpha`/`gauge_violation` return
    constants: they are diagnostics `integrate` records but the CONVERGED PREDICATE
    NEVER READS, which is itself part of what this audit is measuring.
    """

    def __init__(self, K, rhs_fn, jac_fn, a=0.5, p=3):
        self.K = int(K)
        self.a, self.p, self.s = float(a), int(p), 0.5 * int(p)
        self._rhs_fn, self._jac_fn = rhs_fn, jac_fn
        self.gauge_correction = 0.0
        self.gauge_abs = 0.0
        self.rhs_scale = 0.0
        self.n_rhs = 0

    def rhs(self, y):
        g = np.asarray(self._rhs_fn(np.asarray(y, float)), float)
        self.n_rhs += 1
        if np.all(np.isfinite(g)):
            self.rhs_scale = max(self.rhs_scale, float(np.linalg.norm(g[:-1])))
        return g

    def jacobian(self, y):
        return np.asarray(self._jac_fn(np.asarray(y, float)), float)

    @property
    def gauge_violation(self):
        return 0.0

    def gauge(self, y):
        return 0.0

    def alpha(self, y):
        return 0.0


# --------------------------------------------------------------------------
# the battery.  Every member has a closed-form exact solution.
# --------------------------------------------------------------------------
def _scalar_mu(f, df):
    """rhs/jac for K=1 with all motion in the mu slot: y = [b, mu]."""
    def rhs(y):
        return np.array([0.0, f(y[1])])

    def jac(y):
        return np.array([[0.0, 0.0], [0.0, df(y[1])]])
    return rhs, jac


def _scalar_b(f, df):
    """rhs/jac for K=1 with all motion in the b slot: y = [b, mu], mu frozen."""
    def rhs(y):
        return np.array([f(y[0]), 0.0])

    def jac(y):
        return np.array([[df(y[0]), 0.0], [0.0, 0.0]])
    return rhs, jac


def _rotation(omega, sigma):
    """K=2 linear block b' = (sigma I + omega J) b, mu frozen.  Exact amplitude e^{sigma tau}."""
    M = np.array([[sigma, -omega], [omega, sigma]])

    def rhs(y):
        return np.array([M[0, 0] * y[0] + M[0, 1] * y[1],
                         M[1, 0] * y[0] + M[1, 1] * y[1], 0.0])

    def jac(y):
        J = np.zeros((3, 3))
        J[:2, :2] = M
        return J
    return rhs, jac


def battery():
    """Every member: name, family, ground truth, exact solution, and why it is here."""
    cases = []

    def add(**kw):
        cases.append(kw)

    # ---- family: SLOW / POLYNOMIAL UNBOUNDED GROWTH ----------------------
    # mu' = 1.  The slowest unbounded growth there is.  Newton sees a linear
    # problem; if any divergence trips the predicate, this one must not.
    r, j = _scalar_mu(lambda u: 1.0, lambda u: 0.0)
    add(name="mu_linear", family="polynomial", truth="divergent", K=1,
        b0=[1.0], mu0=0.3, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=lambda t, y0: y0[1] + t, exact_slot=-1,
        why="mu(tau) = mu0 + tau, unbounded; the mildest possible non-NaN divergence")

    # mu' = 4 mu^{3/4}  =>  mu = (mu0^{1/4} + tau)^4.  Genuine polynomial blowup in
    # amplitude, smooth and autonomous, Jacobian bounded and shrinking.
    r, j = _scalar_mu(lambda u: 4.0 * abs(u) ** 0.75,
                      lambda u: 3.0 * abs(u) ** (-0.25) * np.sign(u))
    add(name="mu_quartic", family="polynomial", truth="divergent", K=1,
        b0=[1.0], mu0=1.0, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=lambda t, y0: (y0[1] ** 0.25 + t) ** 4, exact_slot=-1,
        why="mu = (1+tau)^4, 7 decades of growth with a perfectly conditioned Newton")

    # the same growth put in the STATE (b) instead of mu, in case the predicate
    # treats the two blocks differently.  b = (1+tau)^2.
    r, j = _scalar_b(lambda u: 2.0 * abs(u) ** 0.5,
                     lambda u: abs(u) ** (-0.5) * np.sign(u))
    add(name="b_quadratic", family="polynomial", truth="divergent", K=1,
        b0=[1.0], mu0=0.3, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=lambda t, y0: (y0[0] ** 0.5 + t) ** 2, exact_slot=0,
        why="Omega-block growth b = (1+tau)^2 with mu frozen: does the block matter?")

    # ---- family: EXPONENTIAL, FINITE, NO NaN -----------------------------
    r, j = _scalar_mu(lambda u: 0.5 * u, lambda u: 0.5)
    add(name="mu_exp_mild", family="exponential", truth="divergent", K=1,
        b0=[1.0], mu0=0.3, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=lambda t, y0: y0[1] * np.exp(0.5 * t), exact_slot=-1,
        why="mu = 0.3 e^{tau/2}, 13 decades, still nowhere near overflow")

    r, j = _scalar_mu(lambda u: 5.0 * u, lambda u: 5.0)
    add(name="mu_exp_extreme", family="exponential", truth="divergent", K=1,
        b0=[1.0], mu0=0.3, tau_end=60.0, dt=0.02, rhs=r, jac=j,
        exact=lambda t, y0: y0[1] * np.exp(5.0 * t), exact_slot=-1,
        why="mu = 0.3 e^{5 tau} ~ 1e129 at tau=60: 130 decades and STILL finite")

    # the documented failure shape -- 'the off-branch trap ended at mu = -1.6e24 with
    # every value finite' -- reproduced as a SMOOTH trajectory, so nothing about the
    # inner solve is unhealthy.  Negative mu is anti-dissipation: physically invalid.
    r, j = _scalar_mu(lambda u: 0.5 * u, lambda u: 0.5)
    add(name="mu_negative_runaway", family="exponential", truth="divergent", K=1,
        b0=[1.0], mu0=-0.3, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=lambda t, y0: y0[1] * np.exp(0.5 * t), exact_slot=-1,
        why="mu -> -3e12: the documented 'finite but garbage' shape, made smooth")

    # ---- family: SUSTAINED, NON-DECAYING OSCILLATION ---------------------
    # sigma = 0 exactly: the amplitude is 1 for all time, so the trajectory has no
    # limit and never decays.  dt resolves the period ~50x, so BDF2's own damping is
    # measured (`amp_end`) rather than assumed away.
    r, j = _rotation(2.0 * np.pi, 0.0)
    add(name="osc_sustained", family="oscillation", truth="divergent", K=2,
        b0=[1.0, 0.0], mu0=0.3, tau_end=20.0, dt=0.02, rhs=r, jac=j,
        exact=None, exact_slot=None, amp_slots=(0, 1), amp_exact=1.0,
        why="pure rotation, 20 periods, |b| == 1 forever: no limit, never a NaN")

    r, j = _rotation(2.0 * np.pi, 0.05)
    add(name="osc_growing", family="oscillation", truth="divergent", K=2,
        b0=[1.0, 0.0], mu0=0.3, tau_end=20.0, dt=0.02, rhs=r, jac=j,
        exact=None, exact_slot=None, amp_slots=(0, 1), amp_exact=np.exp(0.05 * 20.0),
        why="rotation with Re = +0.05: oscillating AND unbounded")

    # deliberately under-resolved: omega dt = 4 rad/step.  This is the member built to
    # FALSIFY the leg's prediction -- if any oscillation can stress the inner Newton
    # into tripping the threshold, it is this one.
    r, j = _rotation(200.0, 0.0)
    add(name="osc_stiff_underresolved", family="oscillation", truth="divergent", K=2,
        b0=[1.0, 0.0], mu0=0.3, tau_end=20.0, dt=0.02, rhs=r, jac=j,
        exact=None, exact_slot=None, amp_slots=(0, 1), amp_exact=1.0,
        why="omega dt = 4 rad/step: the hardest case for the inner solve in the battery")

    # ---- family: THE DESIGN CASE (must be caught) ------------------------
    r, j = _scalar_mu(lambda u: u * u, lambda u: 2.0 * u)
    add(name="nan_finite_time_blowup", family="nan_control", truth="divergent", K=1,
        b0=[1.0], mu0=1.0, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=None, exact_slot=None,
        why="mu' = mu^2 blows up at tau = 1: the synthetic analogue of leg 41's NaN")

    # ---- family: GENUINELY CONVERGENT (must NOT be flagged) --------------
    r, j = _scalar_mu(lambda u: -u, lambda u: -1.0)
    add(name="decay_to_zero", family="convergent_control", truth="convergent", K=1,
        b0=[1.0], mu0=0.3, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=lambda t, y0: y0[1] * np.exp(-t), exact_slot=-1,
        why="mu -> 0: a real limit; a false positive here would be worse than a miss")

    r, j = _scalar_mu(lambda u: 0.0, lambda u: 0.0)
    add(name="exact_fixed_point", family="convergent_control", truth="convergent", K=1,
        b0=[1.0], mu0=0.3, tau_end=60.0, dt=0.25, rhs=r, jac=j,
        exact=lambda t, y0: y0[1] + 0.0 * t, exact_slot=-1,
        why="rhs == 0: the trivial limit")

    r, j = _rotation(2.0 * np.pi, -0.5)
    add(name="damped_oscillation", family="convergent_control", truth="convergent", K=2,
        b0=[1.0, 0.0], mu0=0.3, tau_end=20.0, dt=0.02, rhs=r, jac=j,
        exact=None, exact_slot=None, amp_slots=(0, 1), amp_exact=np.exp(-0.5 * 20.0),
        why="spiral in: oscillatory but WITH a limit, the near-miss of osc_sustained")

    return cases


# --------------------------------------------------------------------------
# running one member
# --------------------------------------------------------------------------
def run_case(c):
    A = SyntheticFlow(c["K"], c["rhs"], c["jac"])
    t0 = time.time()
    rec = integrate(A, c["b0"], c["mu0"], c["tau_end"], c["dt"],
                    n_sample=min(400, int(c["tau_end"] / c["dt"])))
    wall = time.time() - t0

    tau = np.asarray(rec["tau"], float)
    mu = np.asarray(rec["mu"], float)
    b_end = np.asarray(rec["b_end"], float)
    y0 = np.asarray(list(c["b0"]) + [c["mu0"]], float)

    out = {
        "name": c["name"], "family": c["family"], "ground_truth": c["truth"],
        "why": c["why"],
        "K": c["K"], "tau_end": c["tau_end"], "dt": c["dt"],
        "steps": rec["steps"], "wall_s": round(wall, 3),
        # --- the predicate under test, clause by clause -------------------
        "gate11_converged": bool(rec["converged"]),
        "clause_finite": bool(rec["finite"]),
        "clause_no_nan_break": "diverged_at_tau" not in rec,
        "worst_newton_residual_over_floor": float(rec["worst_newton_residual_over_floor"]),
        "newton_headroom": float(NEWTON_STAGNATION
                                 / (rec["worst_newton_residual_over_floor"] + 1e-300)),
        "worst_newton_iters": int(rec["worst_newton_iters"]),
        # --- what the STATE actually did ----------------------------------
        "mu_end": float(rec["mu_end"]),
        "mu_growth_factor": float(abs(rec["mu_end"]) / (abs(c["mu0"]) + 1e-300)),
        "b_end_absmax": float(np.max(np.abs(b_end))) if b_end.size else 0.0,
        "b_growth_factor": float(np.max(np.abs(b_end))
                                 / (np.max(np.abs(c["b0"])) + 1e-300)),
        "max_abs_mu_sampled": float(np.max(np.abs(mu[np.isfinite(mu)]))
                                    if np.any(np.isfinite(mu)) else float("inf")),
    }
    out["state_growth_factor"] = float(max(out["mu_growth_factor"],
                                           out["b_growth_factor"]))

    # --- fidelity: is the computed trajectory really the exact one? -------
    if c.get("exact") is not None:
        slot = c["exact_slot"]
        ex_end = float(c["exact"](rec["tau_end"], y0))
        got = float(rec["mu_end"]) if slot == -1 else float(b_end[slot])
        out["exact_end"] = ex_end
        out["computed_end"] = got
        out["rel_err_vs_exact"] = float(abs(got - ex_end) / (abs(ex_end) + 1e-300))
        # growth exponent of the exact law, read off the computed samples
        m = np.isfinite(mu) & (np.abs(mu) > 0) & (tau > 1.0)
        if slot == -1 and m.sum() >= 4:
            lo = m.sum() // 2
            t_, u_ = tau[m][lo:], np.log(np.abs(mu[m][lo:]))
            out["fit_exponential_rate"] = float(np.polyfit(t_, u_, 1)[0])
            out["fit_polynomial_exponent"] = float(np.polyfit(np.log(t_), u_, 1)[0])
    elif c.get("amp_slots") is not None:
        i, k = c["amp_slots"]
        amp = float(np.hypot(b_end[i], b_end[k]))
        out["amp_end_computed"] = amp
        out["amp_end_exact"] = float(c["amp_exact"])
        out["rel_err_vs_exact"] = float(abs(amp - c["amp_exact"])
                                        / (abs(c["amp_exact"]) + 1e-300))
        out["numerical_damping_factor"] = float(amp / (c["amp_exact"] + 1e-300))

    # --- fidelity, BEFORE the verdict ------------------------------------
    ok, desc = FIDELITY[c["name"]](out)
    out["fidelity_ok"] = bool(ok)
    out["fidelity_criterion"] = desc

    # --- the verdict ------------------------------------------------------
    should_flag = (c["truth"] == "divergent")
    out["gate_should_flag"] = should_flag
    out["gate_flagged"] = not out["gate11_converged"]
    if not out["fidelity_ok"]:
        out["verdict"] = "EXCLUDED_INTEGRATOR_DID_NOT_REPRODUCE_THE_CASE"
    elif should_flag:
        out["verdict"] = "CAUGHT" if out["gate_flagged"] else "MISSED"
    else:
        out["verdict"] = "FALSE_POSITIVE" if out["gate_flagged"] else "PASSED"
    return out


# --------------------------------------------------------------------------
# the live controls: the harness must reproduce gate 11's own two verdicts
# --------------------------------------------------------------------------
def live_controls(a=0.5, p=3, K=96, tau_end=60.0, dt=0.25):
    """The two trajectories inside gate 11 itself, run on the REAL AugmentedFlow."""
    b = mu_branch(a, p, [0.05, 0.1, 0.2, 0.3], K=K)[-1]["b"]
    naive = np.random.default_rng(7).standard_normal(K) * np.exp(-0.25 * np.arange(K))
    A0 = AugmentedFlow(a, p, K=K)
    naive = naive - (A0.kk @ naive) / (A0.kk @ A0.kk) * A0.kk
    naive = naive / np.max(np.abs(naive))

    rows = []
    for name, b0, expect in (("live_leg41_naive_trap", b + 1e-3 * naive, False),
                             ("live_on_branch", b, True)):
        t0 = time.time()
        rec = integrate(AugmentedFlow(a, p, K=K), b0, 0.3, tau_end, dt, n_sample=60)
        rows.append({
            "name": name, "family": "live_control",
            "expected_converged": expect,
            "gate11_converged": bool(rec["converged"]),
            "reproduces_gate11": bool(rec["converged"]) is expect,
            "clause_finite": bool(rec["finite"]),
            "clause_no_nan_break": "diverged_at_tau" not in rec,
            "diverged_at_tau": rec.get("diverged_at_tau"),
            "worst_newton_residual_over_floor":
                float(rec["worst_newton_residual_over_floor"]),
            "newton_headroom": float(NEWTON_STAGNATION
                                     / (rec["worst_newton_residual_over_floor"] + 1e-300)),
            "mu_end": float(rec["mu_end"]),
            "b_end_absmax": float(np.max(np.abs(rec["b_end"]))),
            "wall_s": round(time.time() - t0, 2)})
    return rows


# --------------------------------------------------------------------------
def main():
    t_all = time.time()
    print("Route-MFG v1 (leg 83) -- adversarial audit of gate 11's catch coverage")
    print("=" * 78)

    rows = []
    for c in battery():
        r = run_case(c)
        rows.append(r)
        print(f"  {r['name']:<26s} {r['family']:<20s} truth={r['ground_truth']:<10s} "
              f"converged={str(r['gate11_converged']):<5s} "
              f"growth={r['state_growth_factor']:.3e} "
              f"res/floor={r['worst_newton_residual_over_floor']:.2e} "
              f"-> {r['verdict']}")

    print("-" * 78)
    print("  live controls (real AugmentedFlow, K=96) ...")
    live = live_controls()
    for r in live:
        print(f"  {r['name']:<26s} expected={str(r['expected_converged']):<5s} "
              f"got={str(r['gate11_converged']):<5s} "
              f"res/floor={r['worst_newton_residual_over_floor']:.2e} "
              f"-> {'REPRODUCES' if r['reproduces_gate11'] else 'HARNESS BROKEN'}")

    excluded = [r for r in rows if not r["fidelity_ok"]]
    scored = [r for r in rows if r["fidelity_ok"]]
    div = [r for r in scored if r["ground_truth"] == "divergent"]
    conv = [r for r in scored if r["ground_truth"] == "convergent"]
    missed = [r for r in div if r["verdict"] == "MISSED"]
    caught = [r for r in div if r["verdict"] == "CAUGHT"]
    fp = [r for r in conv if r["verdict"] == "FALSE_POSITIVE"]

    # the two magnitudes that decide the gate
    worst_missed = max(missed, key=lambda r: r["state_growth_factor"]) if missed else None
    min_headroom_missed = min((r["newton_headroom"] for r in missed), default=float("nan"))

    summary = {
        "n_divergent": len(div), "n_caught": len(caught), "n_missed": len(missed),
        "n_convergent_controls": len(conv), "n_false_positives": len(fp),
        "missed_names": [r["name"] for r in missed],
        "caught_names": [r["name"] for r in caught],
        "n_excluded_on_fidelity": len(excluded),
        "excluded_names": [r["name"] for r in excluded],
        "excluded_reasons": {r["name"]: r["fidelity_criterion"] for r in excluded},
        "worst_missed_case": (None if worst_missed is None else {
            "name": worst_missed["name"],
            "state_growth_factor": worst_missed["state_growth_factor"],
            "mu_end": worst_missed["mu_end"],
            "worst_newton_residual_over_floor":
                worst_missed["worst_newton_residual_over_floor"],
            "newton_headroom": worst_missed["newton_headroom"]}),
        "min_newton_headroom_among_missed": float(min_headroom_missed),
        "live_controls_reproduce_gate11": all(r["reproduces_gate11"] for r in live),
        "gate_answer": ("yes_catches_all" if not missed else "no_misses_some"),
        "newton_stagnation_threshold": NEWTON_STAGNATION,
    }

    print("=" * 78)
    print(f"  divergent members SCORED: {len(div)}   CAUGHT {len(caught)}   "
          f"MISSED {len(missed)}")
    print(f"  convergent controls: {len(conv)}   false positives {len(fp)}")
    for r in excluded:
        print(f"  EXCLUDED (integrator did not reproduce the case): {r['name']} -- "
              f"{r['fidelity_criterion']}")
    if missed:
        w = summary["worst_missed_case"]
        print(f"  worst miss: {w['name']} -- state grew {w['state_growth_factor']:.3e}x, "
              f"mu_end = {w['mu_end']:.3e}, "
              f"Newton residual/floor {w['worst_newton_residual_over_floor']:.2e} "
              f"= {1.0 / w['newton_headroom']:.2e} of the 1e8 threshold")
        print(f"  smallest headroom among missed cases: {min_headroom_missed:.2e}x")
    print(f"  GATE ANSWER: {summary['gate_answer']}")

    payload = {
        "leg": 83, "route": "MFG", "version": "v1",
        "what": "adversarial audit of gate 11's catch coverage on non-NaN divergence",
        "gate_question": (
            "Under an adversarial battery of non-NaN divergent trajectories (slow "
            "polynomial blowup, sustained non-decaying oscillation), does gate 11 "
            "correctly flag non-convergence, or does it only catch the NaN case it was "
            "built for?"),
        "predicate_under_test": (
            "solver/marginal_flow.py:integrate -> rec['converged'] = finite(y) and no "
            "NaN break and worst_newton_residual_over_floor < 1e8"),
        "summary": summary, "cases": rows, "live_controls": live,
        "wall_s": round(time.time() - t_all, 1),
    }
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
    print(f"  wrote {DATA}  ({payload['wall_s']}s)")
    return payload


if __name__ == "__main__":
    main()
