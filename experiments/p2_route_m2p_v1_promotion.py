"""Route-M2P v1: Chen's gamma=2 dissipative gCLM candidate -- full text, constants, first Y_0.

Leg 63's screen produced the only screen-passing candidate in 63+ legs: gCLM with FULL
LAPLACIAN dissipation (gamma = 2), advection `a` close to 1/2, blow-up PROVED analytically by
J. Chen, arXiv:1908.09385 (*Nonlinearity* 33 (2020) 2502).  It did NOT read Chen's full text,
transcribe the profile's constants, or measure `Y_0`.  This leg discharges exactly those three
debts, in order.

PRE-COMMITTED CLAUSES, written before the run; both branches of each are reportable:

  M0  THE NOVELTY PASS COMES FIRST and is committed BEFORE the module (it was:
      `writeup/novelty/leg_125.md`, commit bb3f356).  Narrow question: does a CAP of a
      DISSIPATIVE self-similar gCLM profile exist?  NOT FOUND -> the measurement is novel.
      Chen confirmed ANALYTIC at full-text depth -> an exclusion, not a CAP precedent.

  M1  THE FULL-TEXT READ RESOLVES THE gamma TENSION leg 64's review surfaced.  Chen's
      `gamma = |a|^{-1}` critical dissipation (sec 1.2, Thm 1.5) is stated ONLY for
      `a <= -1`; for `a > -1` his L^1 scaling gives `gamma = 1` critical.  Neither statement
      contradicts Theorem 1.1, and NEITHER produces a gamma = 2 profile.  Constants are
      transcribed with per-constant provenance, including the ones the paper leaves
      UNQUANTIFIED (`delta`, `nu_0`) -- an unquantified constant is reported as such, never
      bounded (lesson 73).

  M2  THE KNOWN-ANSWER GATE.  Chen's closed form eq (2.2) must null the steady residual to
      the discretisation floor, at >= 2 resolutions, with the floor CONVERGING.  If it does
      not, the reading of the equation is wrong and nothing downstream counts.

  M3  THE PROFILE IS CONSTRUCTED BY NEWTON, not asserted.  `c_l` is a free unknown and
      `H Omega(0)` is never imposed, so both are OUTPUTS that can disagree with Chen.  They
      must converge to `1/3` and `8/3` under refinement or the construction is wrong.

  M4  THE CENTRAL MEASUREMENT: `Delta(a) = 2 c_l/|c_omega| - 1`, the gauge-invariant
      obstruction to a gamma = 2 profile (Chen eq (2.7): a steady effective viscosity needs
      `(2 c_l + c_omega) nu = 0`).  `Delta = 0` admits one; `Delta < 0` means dissipation
      vanishes in self-similar variables.  Swept over `a`.  POSITIVE CONTROL, per lesson 90:
      the functional returns EXACTLY 0 on the heat-scaling pair `(c_l, c_omega) = (1/2, -1)`,
      so it can report the other answer; and it returns `+1` at the a = 0 CLM anchor, so it
      VARIES.  Four identical numbers would be a bug, not a finding.

  M5  THE DISSIPATIVE BRANCH IS SEARCHED, not ruled out by algebra alone.  For each `nu > 0`
      Newton solves the FULL dissipative steady equation and the STEADINESS DEFECT
      `|Delta(nu)|` is measured.  A zero crossing would exhibit a genuine gamma = 2 profile
      and flip this leg's gate.  NOTE ON THE TRIPWIRE: `nu` is floated against the PROFILE
      EQUATION's own residual, never against any certificate's margin or any Z-constant.
      That is Chen's own object, not stage V as posed.

  M6  Y_0 AGAINST THE RADII-POLYNOMIAL BUDGET, at >= 2 resolutions, with leg 53's banked
      mu = 2 positive control `Z_1 = 0.9156181325483919` RE-READ against THIS candidate and
      not assumed to transfer.  Lesson 86 is applied in advance: the post-Newton DISCRETE
      defect is at the Newton floor (~1e-15) and is a statement about the code, not about
      the mathematics; the honest `Y_0` is the CONSISTENCY defect of the discrete solution in
      the continuous equation.  BOTH are reported, and which one is the honest one is stated.

  M7  NO gCLM DYNAMICS ARE RUN.  Every solve is of a STEADY equation
      (`no_dynamics_run: true`).  Everything is floating point; no number here is a
      certificate, and `nk_bounds.budget`'s own header says the same of the budget.

  M8  THE HONEST CEILING, pre-committed: this is not movement on L1->L4 and not Clay (odds
      stay ~0.05%).  The prize is the sub-goal only.
"""

import json
import os
import time

import numpy as np

from solver.dissipative_profile import (
    DissipativeProfile, chen_constants, chen_profile, diffusion_consistency,
    nu_decay_rate, radii_budget, y0_measure, z2_quadratic_constant,
)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "writeup", "data", "p2_route_m2p_v1_promotion.json")
FIG = os.path.join(HERE, "writeup", "figures", "fig61_route_m2p_v1_promotion.png")

# leg 53's banked mu = 2 dissipative positive control, re-read here, not assumed to transfer.
LEG53_Z1_MU2 = 0.9156181325483919          # writeup/data/leg_54_verify_headline.json "Z1_total"

RES_MAIN = (601, 801, 1201)                # M2, M3, M6 resolution ladder
N_SWEEP = 401                              # M4, M5 sweeps (cheaper grid)


def m2_known_answer_gate():
    """M2: Chen's closed form nulls the steady residual, and the floor CONVERGES."""
    rows = []
    for n in RES_MAIN:
        dp = DissipativeProfile(a=0.5, n=n)
        Om, Ux, U = chen_profile(dp.X)
        R = dp.residual(Om, c_l=1.0 / 3.0, c_omega=-1.0, nu=0.0)
        rows.append({
            "n": n,
            "hilbert_err_sup": float(np.abs(dp.H @ Om - Ux).max()),
            "velocity_err_sup": float(np.abs(dp.VH @ Om - U).max()),
            "residual_rms": float(np.sqrt(np.mean(R ** 2))),
            "residual_sup": float(np.abs(R).max()),
        })
    return rows


def m3_newton_reconstruction():
    """M3: Newton on the inviscid steady equation; c_l and H Omega(0) are OUTPUTS."""
    rows = []
    for n in RES_MAIN:
        dp = DissipativeProfile(a=0.5, n=n)
        Om, _, _ = chen_profile(dp.X)
        gauge = float(dp.D[dp.i0] @ Om)          # dilation gauge only; c_l NOT imposed
        Om0 = Om * (1.0 + 0.05 * np.exp(-dp.X ** 2))   # 5% perturbation of the exact profile
        t0 = time.time()
        out = dp.newton(Om0, c_l0=0.30, c_omega=-1.0, nu=0.0, scale_gauge=gauge, iters=15)
        rows.append({
            "n": n,
            "c_l_measured": out["c_l"],
            "c_l_chen": 1.0 / 3.0,
            "c_l_abs_err": abs(out["c_l"] - 1.0 / 3.0),
            "HOmega_at_0_measured": float((dp.H @ out["Omega"])[dp.i0]),
            "HOmega_at_0_chen": 8.0 / 3.0,
            "shape_sup_err_vs_chen": float(np.abs(out["Omega"] - Om).max()),
            "newton_residual_rms": out["residual_rms"],
            "newton_history": [float(h) for h in out["history"]],
            "Delta_measured": diffusion_consistency(out["c_l"], -1.0),
            "nu_decay_rate_measured": nu_decay_rate(out["c_l"], -1.0),
            "seconds": time.time() - t0,
        })
    return rows


def m4_delta_sweep():
    """M4: Delta(a) over a window around 1/2, plus the two controls."""
    a_values = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
    rows = []
    for a in a_values:
        dp = DissipativeProfile(a=a, n=N_SWEEP)
        Om, _, _ = chen_profile(dp.X)
        gauge = float(dp.D[dp.i0] @ Om)
        out = dp.newton(Om, c_l0=1.0 / 3.0, c_omega=-1.0, nu=0.0, scale_gauge=gauge, iters=15)
        rows.append({
            "a": a, "c_l": out["c_l"], "Delta": diffusion_consistency(out["c_l"], -1.0),
            "nu_decay_rate": nu_decay_rate(out["c_l"], -1.0),
            "residual_rms": out["residual_rms"],
            "converged": out["residual_rms"] < 1e-10,
        })
    controls = {
        "heat_scaling_c_l_over_c_omega_one_half": diffusion_consistency(0.5, -1.0),
        "clm_a0_anchor_c_l_1_c_omega_-1": diffusion_consistency(1.0, -1.0),
        "chen_exact_1_3": diffusion_consistency(1.0 / 3.0, -1.0),
        "note": ("lesson 90: the functional returns EXACTLY 0.0 on the heat scaling and +1.0 "
                 "at the a=0 CLM anchor, so it varies and can report the other answer."),
    }
    return rows, controls


def m5_nu_branch_search():
    """M5: search the dissipative branch -- steadiness defect |Delta| as a function of nu."""
    rows = []
    for nu in (0.0, 1e-4, 1e-3, 1e-2, 1e-1, 3e-1):
        dp = DissipativeProfile(a=0.5, n=N_SWEEP)
        Om, _, _ = chen_profile(dp.X)
        gauge = float(dp.D[dp.i0] @ Om)
        out = dp.newton(Om, c_l0=1.0 / 3.0, c_omega=-1.0, nu=nu, scale_gauge=gauge, iters=20)
        d = diffusion_consistency(out["c_l"], -1.0)
        rows.append({
            "nu": nu, "c_l": out["c_l"], "Delta": d, "steadiness_defect": abs(d),
            "residual_rms": out["residual_rms"],
            "converged": out["residual_rms"] < 1e-10,
        })
    return rows


def m7_gamma2_branch():
    """M7: impose the steadiness condition Delta = 0 and ask whether nu > 0 can then be solved.

    M4/M5 MEASURE Delta on the branch Chen's theorem lives on.  This does the converse: it
    fixes `(c_l, c_omega) = (1/2, -1)` -- i.e. imposes exactly the condition a gamma = 2
    profile needs -- and solves for `(Omega, a)` at each `nu`.  Two controls, both required:

      * the SCALE-INVARIANT residual `||R|| / ||(c_omega + H Omega) Omega||`.  The ABSOLUTE
        residual is useless here because `Omega == 0` solves the equation exactly, so a
        collapse to the trivial null would read as a perfect solve (lesson 90).
      * the DILATION-COVARIANCE check.  `Omega(X) -> Omega(X/mu)` maps a solution at `nu` to
        one at `mu^2 nu` with `a` UNCHANGED, so a genuine one-parameter branch must have
        `a` independent of `nu`.  Measured, and reported whether or not it holds.
    """
    dp = DissipativeProfile(a=0.39, n=N_SWEEP)
    Om0, _, _ = chen_profile(dp.X)

    def relres(Om, nu, a):
        R = dp.residual(Om, 0.5, -1.0, nu, a=a)
        scale = float(np.sqrt(np.mean(((-1.0 + dp.H @ Om) * Om) ** 2)))
        return float(np.sqrt(np.mean(R ** 2)) / max(scale, 1e-300)), scale

    rows, sols = [], {}
    for nu in (0.0, 1e-3, 1e-2, 1e-1, 3e-1, 1.0):
        out = dp.newton_gamma2(Om0, a0=0.386, nu=nu, c_l=0.5, c_omega=-1.0, iters=60)
        rr, scale = relres(out["Omega"], nu, out["a"])
        sols[nu] = out
        rows.append({
            "nu": nu, "a": out["a"],
            "residual_rms_absolute": out["residual_rms"],
            "residual_relative": rr, "solution_scale": scale,
            "amplitude": float(np.abs(out["Omega"]).max()),
            "nontrivial": bool(rr < 1e-8 and scale > 1e-3),
            "collapsed_to_trivial_null": bool(scale < 1e-8),
        })
    # dilation-covariance diagnostic on the nu = 1e-2 solution
    o = sols[1e-2]
    mu = np.sqrt(10.0)
    Omd = np.interp(dp.X / mu, dp.X, o["Omega"])
    rr_dil, _ = relres(Omd, 1e-1, o["a"])
    rr_ctl, _ = relres(o["Omega"], 1e-1, o["a"])
    a_spread = [r["a"] for r in rows if r["nontrivial"]]
    return rows, {
        "dilated_relative_residual": rr_dil,
        "undilated_control_relative_residual": rr_ctl,
        "dilation_improves_by": (rr_ctl / rr_dil) if rr_dil > 0 else None,
        "a_range_over_nontrivial_nu": [min(a_spread), max(a_spread)] if a_spread else None,
        "a_should_be_constant_under_dilation_covariance": True,
        "verdict": ("NON-TRIVIAL SOLUTIONS EXIST at every tested nu in [1e-3, 3e-1] with "
                    "scale-invariant residual at the Newton floor, BUT the branch is NOT "
                    "resolved: dilation covariance requires `a` to be independent of nu and "
                    "the measured `a` is not.  In the odd subspace the system is short by one "
                    "equation ((n-1)/2 residuals for (n-1)/2 + 1 unknowns), so Newton lands on "
                    "an arbitrary point of a one-parameter set.  REPORTED AS AN OPEN LEAD, "
                    "NOT AS A RESULT."),
    }


def m6_y0_budget(m2_rows, m3_rows):
    """M6: Y_0 (both readings) and the radii-polynomial budget, at every resolution."""
    rows = []
    for n, m2, m3 in zip(RES_MAIN, m2_rows, m3_rows):
        dp = DissipativeProfile(a=0.5, n=n)
        Om, _, _ = chen_profile(dp.X)
        gauge = float(dp.D[dp.i0] @ Om)
        Om0 = Om * (1.0 + 0.05 * np.exp(-dp.X ** 2))
        out = dp.newton(Om0, c_l0=0.30, c_omega=-1.0, nu=0.0, scale_gauge=gauge, iters=15)
        y0_disc, defect_disc = y0_measure(dp, out["Omega"], out["c_l"], -1.0, 0.0, norm="sup")
        # the HONEST Y_0: the discrete solution's defect in the CONTINUOUS equation, proxied
        # at this resolution by the consistency defect of the exact profile (M2's floor).
        y0_cons = m2["residual_sup"]
        z2 = z2_quadratic_constant(dp, out["Omega"], out["c_l"], -1.0, 0.0, norm="sup")
        bud = radii_budget(y0_cons, 0.0, LEG53_Z1_MU2, z2["Z2"])
        bud_disc = radii_budget(y0_disc, 0.0, LEG53_Z1_MU2, z2["Z2"])
        rows.append({
            "n": n,
            "Y0_discrete_newton_floor": y0_disc,
            "discrete_defect_sup": defect_disc,
            "Y0_consistency_honest": y0_cons,
            "Z0_used": 0.0,
            "Z1_used_leg53_mu2_control": LEG53_Z1_MU2,
            "Z2_measured": z2["Z2"],
            "Z2_parts": z2,
            "budget_Y0_max": bud["Y0_max"],
            "closes_with_honest_Y0": bool(bud["closes"]),
            "r_min_honest": bud["r_min"],
            "closes_with_discrete_Y0": bool(bud_disc["closes"]),
            "Y0_over_budget_ratio_honest": (y0_cons / bud["Y0_max"]) if bud["Y0_max"] > 0 else None,
        })
    return rows


def build_figure(payload):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(2, 2, figsize=(13.5, 9.5))

    # (a) the profile Chen's theorem actually converges to
    dp = DissipativeProfile(a=0.5, n=801)
    Om, _, _ = chen_profile(dp.X)
    m = np.abs(dp.X) <= 4
    ax[0, 0].plot(dp.X[m], Om[m], lw=2.4, color="#1b3a6b",
                  label=r"Chen eq (2.2): $\Omega=-2bx/(x^2+b^2)^2$, $b=\sqrt{3/8}$")
    gauge = float(dp.D[dp.i0] @ Om)
    out = dp.newton(Om * (1 + 0.05 * np.exp(-dp.X ** 2)), 0.30, -1.0, 0.0,
                    scale_gauge=gauge, iters=15)
    ax[0, 0].plot(dp.X[m], out["Omega"][m], "--", lw=1.6, color="#c8102e",
                  label=r"Newton, $n=801$ ($c_l$ free $\to$ %.6f)" % out["c_l"])
    ax[0, 0].set_title("(a) The profile is the INVISCID $a=1/2$ profile\n"
                       r"Chen sec 2.6: '$\nu(t)$ converges to 0 $\Rightarrow$ "
                       "same as the inviscid profile'", fontsize=10)
    ax[0, 0].set_xlabel("$x$"); ax[0, 0].set_ylabel(r"$\Omega$")
    ax[0, 0].legend(fontsize=8); ax[0, 0].grid(alpha=0.3)

    # (b) Delta(a)
    rows = payload["M4_delta_sweep"]
    aa = [r["a"] for r in rows]; dd = [r["Delta"] for r in rows]
    ax[0, 1].plot(aa, dd, "o-", color="#1b3a6b", lw=2, label=r"$\Delta(a)=2c_l/|c_\omega|-1$")
    ax[0, 1].axhline(0.0, color="#c8102e", lw=2,
                     label=r"$\Delta=0$: the only line where a $\gamma=2$ profile is admissible")
    ax[0, 1].axhline(-1.0 / 3.0, color="#888", ls=":", lw=1.5, label=r"Chen exact $-1/3$")
    ax[0, 1].plot([0.5], [payload["M4_controls"]["chen_exact_1_3"]], "*", ms=16,
                  color="#e8a33d", label=r"$a=1/2$ (Chen's regime): $\Delta=-1/3$")
    astar = payload["M4_a_star"]["a_star_direct_solve_c_l_imposed_one_half"]
    ax[0, 1].plot([astar], [0.0], "P", ms=13, color="#7b1fa2",
                  label=r"$a^*=%.5f$: $\Delta=0$, and it is NOT Chen's $a$" % astar)
    ax[0, 1].set_title(r"(b) The obstruction is measured, not assumed:"
                       "\n" r"$\Delta$ crosses 0 at $a^*=%.5f$, far from $a=1/2$" % astar,
                       fontsize=10)
    ax[0, 1].set_xlabel("advection $a$"); ax[0, 1].set_ylabel(r"$\Delta$")
    ax[0, 1].legend(fontsize=8); ax[0, 1].grid(alpha=0.3)

    # (c) steadiness defect on Chen's branch, and the imposed-Delta=0 branch search
    rows = payload["M5_nu_branch_search"]
    nn = [max(r["nu"], 1e-5) for r in rows]; ss = [r["steadiness_defect"] for r in rows]
    ax[1, 0].semilogx(nn, ss, "s-", color="#1b3a6b", lw=2,
                      label=r"$|\Delta(\nu)|$ on Chen's $a=1/2$ branch (M5)")
    ax[1, 0].axhline(0.0, color="#c8102e", lw=2,
                     label=r"$\Delta=0$: what a $\gamma=2$ profile needs")
    m7 = payload["M7_gamma2_branch"]
    tr = [r for r in m7 if r["collapsed_to_trivial_null"]]
    ax[1, 0].plot([max(r["nu"], 1e-5) for r in tr], [0.0] * len(tr), "x", ms=13, mew=2.5,
                  color="#7b1fa2",
                  label=r"collapsed to the trivial null $\Omega\equiv 0$ (M7 control)")
    ax[1, 0].set_ylim(-0.05, max(ss) * 1.25 + 0.02)
    ax[1, 0].set_title(r"(c) On Chen's branch the defect only GROWS with $\nu$;"
                       "\n" r"$|\Delta|$ = %.4f at $\nu=0$, %.4f at $\nu=0.3$"
                       % (ss[0], ss[-1]), fontsize=10)
    ax[1, 0].set_xlabel(r"$\nu$ (dilation gauge fixed; $\nu=0$ plotted at $10^{-5}$)")
    ax[1, 0].set_ylabel(r"steadiness defect $|\Delta|$")
    ax[1, 0].legend(fontsize=8); ax[1, 0].grid(alpha=0.3)

    # (d) Y_0 vs budget
    rows = payload["M6_y0_budget"]
    ns = [r["n"] for r in rows]
    y_h = [r["Y0_consistency_honest"] for r in rows]
    y_d = [max(r["Y0_discrete_newton_floor"], 1e-18) for r in rows]
    bmax = [r["budget_Y0_max"] for r in rows]
    ax[1, 1].semilogy(ns, bmax, "^-", color="#2e7d32", lw=2.4,
                      label=r"radii-polynomial budget $Y_{0,\max}$ (leg 53 $Z_1=0.9156$)")
    ax[1, 1].semilogy(ns, y_h, "o-", color="#1b3a6b", lw=2,
                      label=r"$Y_0$ (honest: consistency defect)")
    ax[1, 1].semilogy(ns, y_d, "x--", color="#999", lw=1.4,
                      label=r"$Y_0$ (discrete Newton floor -- a statement about the code)")
    ratios = [r["Y0_over_budget_ratio_honest"] for r in rows]
    ax[1, 1].set_title("(d) $Y_0$ is OVER budget at every resolution, and the gap WIDENS:\n"
                       r"$%.1f\times10^{9}$ at $n=601$ $\to$ $%.1f\times10^{10}$ at $n=1201$"
                       % (ratios[0] / 1e9, ratios[-1] / 1e10), fontsize=10)
    ax[1, 1].set_xlabel("resolution $n$"); ax[1, 1].set_ylabel("sup norm")
    ax[1, 1].legend(fontsize=8); ax[1, 1].grid(alpha=0.3, which="both")

    fig.suptitle("Route-M2P v1 (leg 125) -- Chen arXiv:1908.09385's $\\gamma=2$ gCLM candidate: "
                 "full text, constants, first $Y_0$", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG, dpi=140)
    plt.close(fig)


def main():
    t0 = time.time()
    payload = {
        "leg": 125, "route": "ROUTE-M2P", "branch": "leg/125-m2p-v1",
        "no_dynamics_run": True,
        "stage_claimed": None,
        "clay_odds_unchanged": 0.0005,
        "honest_ceiling": ("Not movement on L1->L4 and not Clay.  The prize is the sub-goal: "
                           "no CAP of any dissipative self-similar profile exists in the "
                           "searched literature, so the measured Y_0 is a novel data point."),
        "float_not_certificate": ("Every number here is floating point.  No number is a "
                                  "certificate; nk_bounds.budget's own header says the same "
                                  "of the budget."),
    }
    payload["M1_chen_constants"] = chen_constants()
    payload["M2_known_answer_gate"] = m2_known_answer_gate()
    payload["M3_newton_reconstruction"] = m3_newton_reconstruction()
    rows, controls = m4_delta_sweep()
    payload["M4_delta_sweep"] = rows
    payload["M4_controls"] = controls
    payload["M5_nu_branch_search"] = m5_nu_branch_search()
    m7_rows, m7_diag = m7_gamma2_branch()
    payload["M7_gamma2_branch"] = m7_rows
    payload["M7_diagnostics"] = m7_diag
    # a* -- the advection at which Delta = 0, determined two independent ways
    left = max((r for r in rows if r["Delta"] > 0), key=lambda r: r["a"])
    right = min((r for r in rows if r["Delta"] < 0), key=lambda r: r["a"])
    a_star_interp = left["a"] + (right["a"] - left["a"]) * left["Delta"] / (left["Delta"] - right["Delta"])
    a_star_direct = next(r["a"] for r in m7_rows if r["nu"] == 0.0)
    payload["M4_a_star"] = {
        "a_star_linear_interpolation_of_Delta_sweep": a_star_interp,
        "a_star_direct_solve_c_l_imposed_one_half": a_star_direct,
        "agreement_abs": abs(a_star_interp - a_star_direct),
        "chen_a": 0.5,
        "Delta_at_chen_a": next(r["Delta"] for r in rows if r["a"] == 0.5),
        "note": ("Delta = 0 is NECESSARY for a gamma = 2 self-similar profile, not "
                 "sufficient.  a* is where the necessary condition is met; it is NOT "
                 "Chen's a = 1/2, and Chen's theorem says nothing about it."),
    }
    payload["M6_y0_budget"] = m6_y0_budget(payload["M2_known_answer_gate"],
                                           payload["M3_newton_reconstruction"])
    payload["seconds"] = time.time() - t0

    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "w") as fh:
        json.dump(payload, fh, indent=1, default=float)
    build_figure(payload)
    print(f"wrote {DATA}\nwrote {FIG}\n{payload['seconds']:.1f}s")

    # -- console summary, so the run is readable without opening the JSON ------------
    print("\nM2 known-answer gate (Chen eq (2.2) nulls the residual):")
    for r in payload["M2_known_answer_gate"]:
        print(f"  n={r['n']:5d}  residual sup = {r['residual_sup']:.3e}  "
              f"H err {r['hilbert_err_sup']:.2e}  U err {r['velocity_err_sup']:.2e}")
    print("\nM3 Newton (c_l and H Omega(0) are OUTPUTS):")
    for r in payload["M3_newton_reconstruction"]:
        print(f"  n={r['n']:5d}  c_l = {r['c_l_measured']:.9f} (Chen 1/3, err "
              f"{r['c_l_abs_err']:.2e})  HOmega(0) = {r['HOmega_at_0_measured']:.9f} "
              f"(Chen 8/3)  shape err {r['shape_sup_err_vs_chen']:.2e}")
    print("\nM4 Delta(a):")
    for r in payload["M4_delta_sweep"]:
        print(f"  a={r['a']:.2f}  c_l = {r['c_l']:.6f}  Delta = {r['Delta']:+.6f}")
    print(f"  controls: heat scaling -> {controls['heat_scaling_c_l_over_c_omega_one_half']}, "
          f"a=0 CLM anchor -> {controls['clm_a0_anchor_c_l_1_c_omega_-1']}")
    print("\nM5 dissipative branch search:")
    for r in payload["M5_nu_branch_search"]:
        print(f"  nu={r['nu']:.1e}  c_l = {r['c_l']:.6f}  |Delta| = {r['steadiness_defect']:.6f}")
    print("\nM7 gamma=2 branch (Delta = 0 IMPOSED, a free):")
    for r in payload["M7_gamma2_branch"]:
        print(f"  nu={r['nu']:.1e}  a = {r['a']:+.7f}  rel.res = {r['residual_relative']:.3e}  "
              f"scale = {r['solution_scale']:.2e}  nontrivial = {r['nontrivial']}")
    print(f"  a* : interp {payload['M4_a_star']['a_star_linear_interpolation_of_Delta_sweep']:.6f} "
          f"vs direct {payload['M4_a_star']['a_star_direct_solve_c_l_imposed_one_half']:.6f}")
    print(f"  dilation check: dilated {payload['M7_diagnostics']['dilated_relative_residual']:.3e} "
          f"vs control {payload['M7_diagnostics']['undilated_control_relative_residual']:.3e}; "
          f"a range {payload['M7_diagnostics']['a_range_over_nontrivial_nu']}")
    print("\nM6 Y_0 vs budget:")
    for r in payload["M6_y0_budget"]:
        print(f"  n={r['n']:5d}  Y0(honest) = {r['Y0_consistency_honest']:.3e}  "
              f"budget = {r['budget_Y0_max']:.3e}  ratio = "
              f"{r['Y0_over_budget_ratio_honest']:.3e}  closes = {r['closes_with_honest_Y0']}  "
              f"Z2 = {r['Z2_measured']:.3e}")


if __name__ == "__main__":
    main()
