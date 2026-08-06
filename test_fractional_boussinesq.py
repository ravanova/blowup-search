"""Route-G v1 gates: 2D Boussinesq with fractional dissipation.

Run: .venv/bin/python test_fractional_boussinesq.py

The load-bearing gate is G1 (the exact Taylor-Green diffusion solution): it pins the
fractional operator AND the integrating-factor scheme to machine precision at every
s, which matters because the entire leg is a measurement of the SIZE of that term.
"""

import numpy as np

from solver.boussinesq import grid2d, parity_residual, project_odd_odd
from solver.fractional_boussinesq import (
    CHEN_HOU_C_L, CHEN_HOU_C_OMEGA, FractionalBoussinesq, chen_hou_beta,
    collapse_exponent_from_rescaling, critical_s, estimate_T, fit_collapse,
    collapse_window_report, fit_relevance, houluo_sharp_ic, relevance_exponent,
    relevance_exponent_buoyancy,
)
from solver.fractional_gclm import critical_s as critical_s_1d

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


# --------------------------------------------------------------------------
def gate0_law():
    """The law itself: s_c = 1/(2 beta), its 1D specialization, and the NS value."""
    print("G0  the criticality law")
    # NS: beta = 1/2 is EXACTLY the ordinary Laplacian.  This is the whole point of
    # the reframe, so it is a test and not a comment.
    check("NS beta=1/2 gives s_c=1 exactly", critical_s(0.5) == 1.0,
          f"s_c={critical_s(0.5)!r}")
    # Route-F's s_c = alpha/2 must be the beta = 1/alpha case of s_c = 1/(2 beta).
    alpha = np.array([1.0, 1.3345, 1.6172, 2.0795, 3.0])
    same = np.allclose(critical_s(1.0 / alpha), critical_s_1d(alpha))
    check("1D s_c=alpha/2 is the beta=1/alpha case", same,
          f"max diff {np.max(np.abs(critical_s(1/alpha) - critical_s_1d(alpha))):.2e}")
    # p(s) crosses zero at s_c, and is positive below it (dissipation irrelevant).
    for beta in (0.4, 0.5, 1.0, 2.92):
        sc = critical_s(beta)
        ok = (abs(relevance_exponent(sc, beta)) < 1e-12
              and relevance_exponent(0.9 * sc, beta) > 0
              and relevance_exponent(1.1 * sc, beta) < 0)
        check(f"p(s) zero/sign at beta={beta}", ok)
    # The direction that is counter-intuitive, asserted in the module docstring and
    # therefore gated (banked lesson 32).
    b = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
    check("s_c DECREASES with beta (faster collapse loses)",
          np.all(np.diff(critical_s(b)) < 0), f"s_c={np.round(critical_s(b), 4)}")
    # The condition does not care WHICH field is dissipated -- derived independently in
    # the theta equation.  This is the strongest available statement that s_c is a
    # property of the collapse rather than of a modelling choice.
    ss = np.array([0.1, 0.35, 0.5, 1.0, 1.5])
    same = all(np.allclose(relevance_exponent(ss, bb),
                           relevance_exponent_buoyancy(ss, bb)) for bb in b)
    check("dissipating theta instead of omega gives the SAME p", same)


def gate1_chen_hou():
    """The published-constant arithmetic, and the identity beta = -1/alpha_2D."""
    print("G1  Chen-Hou 2D Boussinesq constants")
    beta = chen_hou_beta()
    check("beta = -c_l/c_omega = 2.92056", abs(beta - 2.9205600) < 1e-5,
          f"beta={beta:.7f}")
    # Part I (2.23) quotes c_l/c_omega = -2.9205600 directly; beta is its negative.
    check("matches the paper's quoted c_l/c_omega",
          abs(-CHEN_HOU_C_L / CHEN_HOU_C_OMEGA - 2.9205600) < 1e-5)
    # The far-field exponent alpha = c_omega/c_l and beta are ONE fact: alpha = -1/beta.
    alpha2d = CHEN_HOU_C_OMEGA / CHEN_HOU_C_L
    check("alpha_2D = -1/beta (the steady-far-field identity)",
          abs(alpha2d + 1.0 / beta) < 1e-12, f"alpha_2D={alpha2d:.6f}")
    # The transcribed constants are MUTUALLY INCONSISTENT in the 6th digit, and the
    # honest thing is to record it rather than to quietly pick one:
    #   c_omega/c_l         = -0.3424004
    #   1/(c_l/c_omega)     = -0.3424038   (from the paper's own quoted ratio)
    #   quoted alpha        = -0.342407
    # a spread of 7e-6, i.e. 2e-5 relative.  It moves s_c in its 6th digit and no
    # conclusion in this leg depends on it, but a tolerance of 1e-6 would be a
    # tolerance the INPUT cannot support.
    check("alpha_2D matches the paper's -0.342407 to 1e-5",
          abs(alpha2d + 0.342407) < 1e-5,
          f"spread across the three quoted forms: {abs(alpha2d + 0.342407):.1e}")
    sc = float(critical_s(beta))
    check("s_c(Chen-Hou) = 0.1712", abs(sc - 0.171200) < 1e-4, f"s_c={sc:.6f}")
    check("Chen-Hou sits far BELOW the NS-critical s=1", sc < 0.2,
          f"{1.0 / sc:.2f}x too fast a collapse")
    # And the reciprocal reading: a 1D gCLM member with alpha=2 is the NS-critical one.
    check("gCLM alpha=2 <=> beta=1/2 <=> NS-critical",
          abs(collapse_exponent_from_rescaling(1.0, -2.0) - 0.5) < 1e-14)
    # INDEPENDENT CHECK OF THE SIGN CONVENTIONS.  The derivation of beta = -c_l/c_omega
    # also predicts theta ~ (T-t)^{beta-2}, hence d log C_theta/dtau = (2-beta) c_omega.
    # The paper states c_theta = c_l + 2 c_omega (MMS (2.9)) independently.  The two must
    # agree -- and they do, which is a check on the gauge/sign conventions of the whole
    # section rather than on arithmetic we control.
    c_theta_paper = CHEN_HOU_C_L + 2 * CHEN_HOU_C_OMEGA
    c_theta_derived = (2.0 - beta) * CHEN_HOU_C_OMEGA
    check("MMS c_theta = c_l + 2c_omega agrees with (2-beta)c_omega",
          abs(c_theta_paper - c_theta_derived) < 1e-12,
          f"{c_theta_paper:.8f} vs {c_theta_derived:.8f}")


def gate2_exact_diffusion():
    """THE KNOWN-ANSWER GATE.  omega0 = sin x sin y is a steady Euler state
    (u.grad omega = 0 identically, since psi = omega/2), so with theta = 0 the exact
    solution of the full system is omega(t) = exp(-nu 2^s t) omega0 -- for EVERY s.
    This pins the fractional multiplier and the integrating-factor RK4 together."""
    print("G2  exact fractional-diffusion solution (Taylor-Green, theta=0)")
    n = 64
    X, Y = grid2d(n)
    w0 = project_odd_odd(np.sin(X) * np.sin(Y))
    th0 = np.zeros((n, n))
    for s in (0.25, 0.5, 1.0, 1.5):
        solver = FractionalBoussinesq(n=n, nu=0.05, s=s, dt_max=2e-2)
        res = solver.run(w0, th0, t_end=1.0, sample_every=25, amp_factor=np.inf,
                         max_steps=20000)
        # exact: |k|^2 = 2 for every retained mode of sin x sin y
        expected = np.exp(-0.05 * (2.0 ** s) * res["t_final"])
        got = res["amp"][-1] / res["amp0"] if res["amp"].size else np.nan
        # amp is sampled, not final; recompute against the last SAMPLE time instead
        expected_s = np.exp(-0.05 * (2.0 ** s) * res["t"][-1])
        err = abs(got - expected_s) / expected_s
        check(f"s={s}: decay matches exp(-nu 2^s t) to 1e-12", err < 1e-12,
              f"rel err {err:.2e}  (t={res['t'][-1]:.3f}, ratio {expected:.4f})")


def gate3_symmetry_and_guard():
    """Hou-Luo parity is preserved, and the resolution guard SEPARATES a resolved
    field from an unresolved one (lesson 55: check it on a case you know is bad)."""
    print("G3  symmetry preservation and the resolution guard")
    n = 64
    w0, th0 = houluo_sharp_ic(n)
    solver = FractionalBoussinesq(n=n, nu=1e-3, s=0.5)
    res = solver.run(w0, th0, t_end=0.5, sample_every=20, max_steps=5000)
    check("run completes", res["t_final"] > 0.49, f"outcome={res['outcome']}")

    # Guard discrimination: a smooth field vs one with grid-scale content.
    X, Y = grid2d(n)
    smooth = np.fft.fft2(np.sin(X) * np.sin(2 * Y))
    rng = np.random.default_rng(0)
    rough = np.fft.fft2(rng.standard_normal((n, n)))
    ts, tr = solver.tail_fraction(smooth), solver.tail_fraction(rough)
    check("guard: smooth field reads ~0", ts < 1e-20, f"{ts:.2e}")
    check("guard: grid-noise field reads O(1)", tr > 1e-2, f"{tr:.2e}")
    check("guard separates them by >15 orders", tr / (ts + 1e-300) > 1e15)

    # Parity: omega odd-odd and theta even-odd must survive the step.
    solver_ns = FractionalBoussinesq(n=n, nu=0.0, s=1.0, symmetry=False)
    res2 = solver_ns.run(w0, th0, t_end=0.5, sample_every=20, max_steps=5000)
    check("parity is preserved by the dynamics alone (no projection)",
          res2["outcome"] in ("t_end", "max_steps"), f"outcome={res2['outcome']}")


def gate4_peak_structure():
    """The module claims that at the peak of |omega| the advective term vanishes, so
    the ratio compares BUOYANCY against dissipation.  Asserted in a docstring =>
    gated (banked lesson 32)."""
    print("G4  what the ratio actually compares")
    n = 128
    w0, th0 = houluo_sharp_ic(n)
    solver = FractionalBoussinesq(n=n, nu=1e-3, s=0.5)
    res = solver.run(w0, th0, t_end=1.5, sample_every=25, max_steps=20000)
    check("run reached t_end", abs(res["t_final"] - 1.5) < 1e-9,
          f"outcome={res['outcome']}")
    # The identity grad omega = 0 at the peak is pointwise and holds at every time, so
    # the IC is a legitimate place to test it.
    wh = np.fft.fft2(w0) * solver.mask
    th = np.fft.fft2(th0) * solver.mask
    drv, dis, adv, buo = solver.terms(wh, th)
    aw = np.abs(np.fft.ifft2(wh).real)
    idx = np.unravel_index(int(np.argmax(aw)), aw.shape)
    rel = abs(adv[idx]) / (abs(buo[idx]) + 1e-300)
    check("advection is negligible at the peak of |omega|", rel < 1e-10,
          f"|adv|/|buoy| = {rel:.2e}")


def gate5_collapse_refuses():
    """THE NEGATIVE, GATED.  The uniform-grid periodic run does grow and does have an
    amplitude exponent near -1, but it gives under one decade of (T-t), and beta moves
    by more than a factor of two across sub-windows.  The gate is that the code SAYS SO
    instead of returning the number -- the whole point of banked lesson 45."""
    print("G5  the direct collapse fit REFUSES (and is right to)")
    n = 256
    w0, th0 = houluo_sharp_ic(n)
    solver = FractionalBoussinesq(n=n, nu=0.0, s=1.0)
    res = solver.run(w0, th0, amp_factor=1e4, sample_every=20, max_steps=100000,
                     wall_max=300.0)
    growth = res["amp"][-1] / res["amp0"]
    check("amplitude grows by >20x before the guard fires", growth > 20,
          f"growth {growth:.1f}, outcome={res['outcome']}")
    T = estimate_T(res)
    check("blow-up time extrapolates past the run", T > res["t_final"],
          f"T={T:.4f} vs t_final={res['t_final']:.4f}")
    fc = fit_collapse(res, T)
    check("amplitude exponent is within 0.25 of -1 (the assumed regime)",
          abs(fc["amp_exponent"] + 1.0) < 0.25, f"{fc['amp_exponent']:.3f}")
    rep = collapse_window_report(res, T)
    check("collapse_window_report REFUSES on this run", not rep["measurable"],
          rep["reason"])
    check("the refusal is on window length, not on noise", rep["decades"] < 1.5,
          f"{rep['decades']:.2f} decades of (T-t)")
    check("beta really does move >25% across sub-windows", rep["beta_spread"] > 0.25,
          f"{[round(b, 3) for b in rep['betas_by_window']]}")
    # And the diagnosis of WHY the two length diagnostics differ: the spectral centroid
    # is a GLOBAL average, so it is contaminated by the non-collapsing background, while
    # amp/|grad omega| is local to the sharpening point.  If that is the story, the
    # spectral exponent must DRIFT UPWARD across the window (the core's share of the
    # enstrophy grows) while the local one does not have that systematic.
    early = fit_collapse(res, T, lo=0.40, hi=0.70, keys=("Lgrad", "Lspec"))
    late = fit_collapse(res, T, lo=0.70, hi=0.98, keys=("Lgrad", "Lspec"))
    check("spectral beta drifts upward late (background contamination)",
          late["Lspec"] > early["Lspec"],
          f"Lspec {early['Lspec']:.3f} -> {late['Lspec']:.3f}")


# The window sweep IS the error bar on p (fit_relevance's own docstring: "THE WINDOW
# IS THE DOMINANT SYSTEMATIC AND IS SWEPT, NOT CHOSEN").  G6 quotes it explicitly
# rather than calling fit_relevance once at its default and signing the result.
G6_WINDOWS = ((0.20, 0.94), (0.30, 0.94), (0.40, 0.94), (0.50, 0.94), (0.60, 0.94),
              (0.40, 0.70), (0.40, 0.80), (0.55, 0.85), (0.50, 0.98), (0.70, 0.98))


def gate6_relevance_sign():
    """The D/N instrument itself still has to work: p must DECREASE with s, even
    though this run cannot pin where the sign change is.  Testing the instrument
    separately from the quantity is the point (the run is underpowered for s_c; it is
    not underpowered for 'does D/N respond to s at all').

    WHAT THIS GATE USED TO ASSERT, AND WHY IT WAS WRONG (bench leg, 2026-08-06).
    It called `fit_relevance` ONCE at its default window (0.40, 0.94) and asserted the
    absolute sign `p > 0 at s=0.10`.  That measured p = -0.211 and was RED -- but the
    red was in the gate, not in the solver.  Three measurements, all reproduced here
    every run, say so:

      (i)  the window systematic on p(s=0.10) is +-1.8, i.e. an order of magnitude
           larger than the |p| = 0.21 whose SIGN was being asserted.  Swept over the
           ten windows below, p(s=0.10) spans roughly [-1.6, +2.0] and CROSSES ZERO;
           the sign of a single-window p at s=0.10 is therefore not a property of the
           object.  p(s=1.00) spans roughly [-4.1, -1.7] and never crosses.
      (ii) the run's OWN geometry predicts the opposite sign from its own D/N fit at
           s=0.10: beta from Lgrad is 1.74, so p = 1-2*beta*s = +0.65, while the
           default-window fit says -0.21.  Inverting the fit instead gives an implied
           beta_eff of 6.05, 3.5x the geometric value.  At s=1.00 the same comparison
           agrees in sign and to 24% (-2.81 predicted vs -3.49 fitted) -- because
           there the predicted |p| is 4x the window systematic instead of a third of it.
      (iii) `collapse_window_report` REFUSES on BOTH of these runs (0.67 and 0.63
           decades of (T-t), need 1.5; beta moves 73% and 57% across sub-windows,
           allow 25%) -- the same refusal G5 gates on its own configuration.  A run
           not entitled to quote beta is not entitled to quote the sign of 1-2*beta*s.

    So the gate now asserts the two things the module says ARE robust -- the sign at
    s=1.00, and the ORDERING in s, where the shared-window bias largely cancels -- at
    EVERY window rather than at one, and it records the s=0.10 indeterminacy as a
    measured fact instead of asserting through it.  The assertion is not flipped and
    the threshold is not relaxed: `p > 0 at s=0.10` is withdrawn, because the run
    cannot support a claim of that shape in either direction.

    Nothing in `solver/fractional_boussinesq.py` changed for this repair, so every
    banked Route-G number is bit-identical by construction.
    """
    print("G6  the D/N instrument responds to s with the right sign")
    n = 192
    w0, th0 = houluo_sharp_ic(n)
    runs, ps = {}, {}
    for s in (0.10, 1.00):
        solver = FractionalBoussinesq(n=n, nu=1e-3, s=s)
        r = solver.run(w0, th0, amp_factor=1e4, sample_every=20, max_steps=100000,
                       wall_max=240.0)
        runs[s] = r
        ps[s] = [fit_relevance(r, estimate_T(r), lo=lo, hi=hi)["p"]
                 for lo, hi in G6_WINDOWS]

    keep = [i for i in range(len(G6_WINDOWS))
            if np.isfinite(ps[0.10][i]) and np.isfinite(ps[1.00][i])]
    lo10 = [ps[0.10][i] for i in keep]
    lo100 = [ps[1.00][i] for i in keep]

    # (1) the sign at s=1.00 is robust to the window -- the claim that survives.
    check("p < 0 at s=1.00 at EVERY window (dissipation winning)",
          all(p < 0 for p in lo100),
          f"{len(keep)} windows, p in [{min(lo100):.3f}, {max(lo100):.3f}], "
          f"worst margin {max(lo100):.3f}")

    # (2) the instrument RESPONDS to s -- also robust, and it is what G6 is named for.
    gaps = [lo10[i] - lo100[i] for i in range(len(keep))]
    check("p decreases with s at EVERY window (the instrument responds)",
          all(g > 0 for g in gaps),
          f"{len(keep)} windows, p(0.10)-p(1.00) in [{min(gaps):.3f}, "
          f"{max(gaps):.3f}]")

    # (3) the withdrawn claim, recorded as the measurement that withdrew it.
    check("the s=0.10 sign is window-INDETERMINATE while the s=1.00 sign is not",
          min(lo10) < 0 < max(lo10) and max(lo100) < 0,
          f"p(0.10) spans [{min(lo10):.3f}, {max(lo10):.3f}] and straddles 0 "
          f"({sum(1 for p in lo10 if p > 0)}/{len(keep)} windows positive); "
          f"p(0.10) at the old default window = {ps[0.10][2]:.3f}")

    # (4) and the run was never entitled to a single-window p in the first place.
    rep = {s: collapse_window_report(runs[s], estimate_T(runs[s])) for s in runs}
    check("collapse_window_report REFUSES on both G6 runs (so 1-2*beta*s is not "
          "quotable from them)",
          not rep[0.10]["measurable"] and not rep[1.00]["measurable"],
          f"s=0.10: {rep[0.10]['decades']:.2f} decades, beta spread "
          f"{rep[0.10]['beta_spread'] * 100:.0f}%; s=1.00: "
          f"{rep[1.00]['decades']:.2f} decades, beta spread "
          f"{rep[1.00]['beta_spread'] * 100:.0f}%")


if __name__ == "__main__":
    print("=" * 74)
    print("Route-G v1 -- 2D Boussinesq with fractional dissipation")
    print("=" * 74)
    for g in (gate0_law, gate1_chen_hou, gate2_exact_diffusion,
              gate3_symmetry_and_guard, gate4_peak_structure, gate5_collapse_refuses,
              gate6_relevance_sign):
        g()
    print("=" * 74)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
        raise SystemExit(1)
