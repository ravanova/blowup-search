"""Permanent adversarial regression test for solver/gclm.py (leg 92, Route-GLA).

THE GATE ANSWERED **YES**. This file is therefore NOT a "confirmed robust" bank like
test_gclm_family_adversarial.py (leg 88). It is a CHARACTERIZATION test: it pins both

  (A) the robustness that DOES hold -- so a refactor cannot quietly lose it, and
  (B) the four silent-corruption gaps leg 92 measured -- so that when someone repairs
      solver/gclm.py, this test FAILS and forces them to update it deliberately rather
      than letting the repair go unrecorded.

Leg 92 is forbidden from editing solver/gclm.py under any gate outcome, so the gaps are
pinned as measured, not fixed here. Every pinned gap is marked `KNOWN GAP` in its output.
A FAILURE of a KNOWN GAP check is GOOD NEWS -- it means the module was repaired.

THE GATE, VERBATIM
------------------
"Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
degenerate transform input, extreme a), does solver/gclm.py ever silently return a
finite, plausible-looking result instead of propagating or flagging the invalid input?"

ANSWER: yes -- 19 silent corruptions in 54 gate-scoped cases, four independent
mechanisms. The worst is G1 below: a finite, positive, ordinary-looking blow-up time
that is 1.5x too early, returned without any flag.

test_gclm_dedicated.py (14 checks, leg 66) covers correctness on well-formed data and is
untouched by this file; this is the robustness complement, not a replacement.

Repo convention: self-running script, no pytest.
  Run: PYTHONPATH=. .venv/bin/python test_gclm_adversarial.py

Companion battery: experiments/p2_route_gla_v1_adversarial.py
Companion data:    writeup/data/p2_route_gla_v1_adversarial.json
Findings:          writeup/novelty/leg_92.md
"""

import numpy as np

from solver.gclm import clm_analytic_blowup_time, solve_gclm
from solver.spectral_utils import grid

N = 64
N_SCAN = 4096


def _quiet():
    """The invalid-value warnings ARE the expected behaviour here, not a failure."""
    return np.errstate(all="ignore")


def profile(x):
    """sin x + 0.5 sin 2x -- chosen so max H over the ZERO SET (0.5) differs from the
    GLOBAL max of H (0.75). For sin x alone the two coincide and G1 is invisible."""
    return np.sin(x) + 0.5 * np.sin(2 * x)


def _payload_all_finite(r):
    fields = [r.omega_final, r.max_omega, r.times, r.t_final, r.mean_drift,
              r.energy_balance_residual, r.conservation_drift, r.dt_min]
    return all(bool(np.all(np.isfinite(np.asarray(f, dtype=float)))) for f in fields)


# ---------------------------------------------------------------------------
# (A) ROBUSTNESS THAT HOLDS -- banked
# ---------------------------------------------------------------------------
def check_nan_seeded_vorticity_is_flagged():
    """A NaN or Inf anywhere in omega0 must reach outcome='diverged', never a clean run."""
    x = grid(N)
    base = profile(x)
    seen = []
    with _quiet():
        for val in (np.nan, np.inf, -np.inf):
            for idx in ([7], [0, 7, 31], list(range(N))):
                w = base.copy()
                w[idx] = val
                r = solve_gclm(w, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
                assert r.outcome == "diverged", (val, idx, r.outcome)
                assert not _payload_all_finite(r), (val, idx)
                seen.append(r.n_timesteps)
    assert max(seen) == 1, seen  # caught on the very first step, every time
    return f"{len(seen)} poisoned-vorticity cases, all outcome='diverged' within 1 step"


def check_extreme_finite_a_is_not_clamped():
    """A wild but finite `a` must produce an honestly huge number, not a tame one."""
    x = grid(N)
    w0 = profile(x)
    mags = []
    with _quiet():
        for a in (1e4, 1e8, 1e12, 1e16):
            r = solve_gclm(w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
            assert r.outcome == "blowup_candidate", (a, r.outcome)
            mags.append(float(np.max(np.abs(r.omega_final))))
    # monotone in a, and enormous -- no saturation, no clamp, no short-circuit
    assert all(b > p for p, b in zip(mags, mags[1:])), mags
    assert mags[-1] > 1e200, mags[-1]
    return ("max|w| = " + ", ".join(f"{m:.3e}" for m in mags)
            + " for a = 1e4..1e16 (monotone, unclamped)")


def check_nonfinite_a_is_flagged():
    x = grid(N)
    w0 = profile(x)
    with _quiet():
        for a in (np.nan, np.inf, -np.inf, 1e300):
            r = solve_gclm(w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
            assert r.outcome == "diverged", (a, r.outcome)
    return "a in {nan, +inf, -inf, 1e300} all reach outcome='diverged'"


def check_structural_adversaries_raise():
    with _quiet():
        try:
            solve_gclm(np.zeros(N), t_max=0.1)
            raise AssertionError("identically-zero omega0 did not raise")
        except ValueError:
            pass
        try:
            clm_analytic_blowup_time(lambda x: np.sin(x)[:100], n_scan=256)
            raise AssertionError("length-mismatched profile did not raise")
        except ValueError:
            pass
    return "zero data -> ValueError; length mismatch -> ValueError"


# ---------------------------------------------------------------------------
# (B) KNOWN GAPS -- pinned as measured by leg 92. Failure here means REPAIRED.
# ---------------------------------------------------------------------------
def check_KNOWN_GAP_absolute_zero_tolerance():
    """G1. solver/gclm.py:289 uses an ABSOLUTE tolerance `np.abs(w0) < 1e-12` to decide
    which grid points count as zeros of w0, without ever measuring the scale of w0.

    Below that amplitude the whole grid is classified as a zero, so the returned time
    becomes 2/max_x H(w0) (GLOBAL max) instead of 2/max{H(w0) : w0 = 0} (max over the
    ZERO SET). The CLM closed form is exactly homogeneous of degree -1 in amplitude, so
    eps*T*(eps*w0) must be independent of eps; it is not.
    """
    with _quiet():
        t_ref = clm_analytic_blowup_time(profile, n_scan=N_SCAN)
        assert abs(t_ref - 4.0) < 1e-9, t_ref

        # deep in the saturated regime: exactly a 1/3 relative violation
        t_deep = clm_analytic_blowup_time(lambda x: 1e-14 * profile(x), n_scan=N_SCAN)
        rel_deep = abs(1e-14 * t_deep - t_ref) / t_ref
        assert abs(rel_deep - 1.0 / 3.0) < 1e-6, rel_deep
        assert np.isfinite(t_deep) and t_deep > 0.0        # finite, positive, plausible

        # and it is already well past the root-finder noise floor at amplitude 1e-8
        t_mid = clm_analytic_blowup_time(lambda x: 1e-8 * profile(x), n_scan=N_SCAN)
        rel_mid = abs(1e-8 * t_mid - t_ref) / t_ref
        assert 1e-3 < rel_mid < 1e-2, rel_mid
    return (f"KNOWN GAP: eps*T* = {1e-14*t_deep:.9f} vs exact {t_ref:.9f} "
            f"(rel {rel_deep:.6f} = 1/3) at amplitude 1e-14; rel {rel_mid:.3e} "
            f"already at amplitude 1e-8. Finite, positive, unflagged.")


def check_KNOWN_GAP_negative_nu_silently_dropped():
    """G2. solver/gclm.py:164 gates dissipation behind `if nu > 0.0`. A negative nu fails
    that test, so an anti-diffusive (ill-posed) request silently runs INVISCID and comes
    back 'no_blowup' with an entirely finite payload."""
    x = grid(N)
    w0 = profile(x)
    kw = dict(a=0.5, t_max=0.3, max_steps=5000)
    with _quiet():
        r_inv = solve_gclm(w0, nu=0.0, **kw)
        r_vis = solve_gclm(w0, nu=0.01, **kw)
        r_neg = solve_gclm(w0, nu=-1.0, **kw)

        honest = float(np.max(np.abs(r_inv.omega_final - r_vis.omega_final)))
        assert honest > 1e-3, honest        # a real nu genuinely moves the solution

        assert r_neg.outcome == "no_blowup", r_neg.outcome
        assert _payload_all_finite(r_neg)
        assert np.array_equal(r_neg.omega_final, r_inv.omega_final)   # bitwise inviscid
        # the ONLY trace is an elevated energy-balance residual
        ratio = r_neg.energy_balance_residual / r_inv.energy_balance_residual
        assert ratio > 1e4, ratio
    return (f"KNOWN GAP: nu=-1.0 -> outcome='no_blowup', bitwise identical to the nu=0 "
            f"run (a real nu=0.01 moves it by {honest:.3e}); only trace is the "
            f"energy-balance residual at {ratio:.3e}x baseline")


def check_KNOWN_GAP_conservation_guard_swallows_nan():
    """G3. solver/gclm.py:226 computes conservation_drift = max(mean_drift,
    energy_balance_residual). Python's builtin max(a, b) returns b only if b > a, and NaN
    loses every comparison -- so max(finite, nan) == finite. The LOGGED artifact-guard
    value reads clean while one of its own two inputs is NaN."""
    x = grid(N)
    w0 = profile(x)
    with _quiet():
        r = solve_gclm(w0, a=1e12, nu=0.0, t_max=0.3, max_steps=5000)
        assert not np.isfinite(r.energy_balance_residual)   # the input is NaN
        assert np.isfinite(r.conservation_drift)            # the logged value is not
        assert r.conservation_drift < 1e-12, r.conservation_drift  # and reads "clean"
        assert max(1.0, float("nan")) == 1.0                # the mechanism, in isolation
    return (f"KNOWN GAP: energy_balance_residual=nan but the LOGGED conservation_drift "
            f"= {r.conservation_drift:.4e} (reads clean) on a run reaching "
            f"max|w| = {np.max(np.abs(r.omega_final)):.3e}")


def check_KNOWN_GAP_nan_stop_criteria_silently_dropped():
    """G4. Every stop criterion is a bare comparison, and every comparison against NaN is
    False. A NaN t_max ends the run before it starts; a NaN amplification_factor disables
    blow-up detection outright."""
    x = grid(N)
    w0 = profile(x)
    with _quiet():
        r = solve_gclm(w0, a=0.5, nu=0.0, t_max=float("nan"), max_steps=5000)
        assert r.n_timesteps == 0 and r.outcome == "no_blowup", (r.n_timesteps, r.outcome)
        assert _payload_all_finite(r) and r.conservation_drift == 0.0

        # the sharp form: the blow-up DETECTOR itself is disabled
        big = dict(a=1e4, nu=0.0, t_max=0.3, max_steps=5000)
        r_clean = solve_gclm(w0, **big)
        r_pois = solve_gclm(w0, amplification_factor=float("nan"), **big)
        assert r_clean.outcome == "blowup_candidate", r_clean.outcome
        assert r_pois.outcome != "blowup_candidate", r_pois.outcome
    return ("KNOWN GAP: t_max=nan -> 0 steps but outcome='no_blowup' with "
            "conservation_drift=0.0; amplification_factor=nan flips a detected "
            f"'{r_clean.outcome}' into '{r_pois.outcome}'")


CHECKS = [
    check_nan_seeded_vorticity_is_flagged,
    check_extreme_finite_a_is_not_clamped,
    check_nonfinite_a_is_flagged,
    check_structural_adversaries_raise,
    check_KNOWN_GAP_absolute_zero_tolerance,
    check_KNOWN_GAP_negative_nu_silently_dropped,
    check_KNOWN_GAP_conservation_guard_swallows_nan,
    check_KNOWN_GAP_nan_stop_criteria_silently_dropped,
]


def main():
    n_gap = 0
    for fn in CHECKS:
        head = fn()
        tag = "PASS"
        if fn.__name__.startswith("check_KNOWN_GAP"):
            n_gap += 1
            tag = "PINNED"
        print(f"{tag} {fn.__name__}: {head}")
    print(f"\nall gclm adversarial checks passed ({len(CHECKS)} checks, "
          f"{n_gap} of them PINNED KNOWN GAPS from leg 92).")
    print("A failure in a PINNED check means solver/gclm.py was REPAIRED -- update this "
          "file and writeup/novelty/leg_92.md deliberately.")


if __name__ == "__main__":
    main()
