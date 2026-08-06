"""Permanent adversarial regression test for solver/gclm.py (leg 92, Route-GLA).

HISTORY, IN TWO STEPS.

  1. Leg 92 ran the adversarial battery and THE GATE ANSWERED **YES**: 19 silent
     corruptions in 54 gate-scoped cases, four independent mechanisms. Forbidden from
     editing solver/gclm.py under any gate outcome, it banked this file as a
     CHARACTERIZATION test -- 4 checks pinning the robustness that DID hold, and 4
     pinning the gaps AS MEASURED, each labelled `KNOWN GAP`, so that a later repair
     would fail the test and be forced to record itself deliberately.

  2. The bench-repair (`Leg 0: ORCH`) fixed all four mechanisms. This file is therefore
     now an ASSERTION-OF-THE-FIX test: the four `KNOWN GAP` checks are **INVERTED, not
     weakened**. Every magnitude leg 92 measured is still asserted here at the same
     threshold -- the same 2.353e-03 amplitude tolerance it calibrated by measurement,
     the same `nu = 0.01` separation of 1e-3, the same `a = 1e12` run reaching
     max|w| ~ 1e+144 -- and only the SIGN of the corruption claim is flipped. Nothing
     was made easier to pass. All 19 corruptions are replayed and all 19 are closed.

A ninth check is new: it verifies the four guards did not OVERSHOOT onto admissible
input (nu = 0 and nu = -0.0 are still legal, the blow-up detector still fires, and the
production-scale blow-up time is unmoved).

THE GATE, VERBATIM
------------------
"Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
degenerate transform input, extreme a), does solver/gclm.py ever silently return a
finite, plausible-looking result instead of propagating or flagging the invalid input?"

ANSWER AT THE TIME (leg 92): yes -- 19 silent corruptions, four mechanisms.
ANSWER NOW (post-repair): no -- all four mechanisms refuse or flag; see below.

test_gclm_dedicated.py (14 checks, leg 66) covers correctness on well-formed data and is
untouched by this file; this is the robustness complement, not a replacement.

Repo convention: self-running script, no pytest.
  Run: PYTHONPATH=. .venv/bin/python test_gclm_adversarial.py

Companion battery: experiments/p2_route_gla_v1_adversarial.py  (leg 92's, deliberately
                   left untouched -- it is the evidence of the PRE-repair behaviour and
                   must keep reading the module as it was measured)
Companion data:    writeup/data/p2_route_gla_v1_adversarial.json
Findings:          writeup/novelty/leg_92.md
"""

import numpy as np

from solver.gclm import clm_analytic_blowup_time, solve_gclm
from solver.spectral_utils import grid

N = 64
N_SCAN = 4096

# Leg 92's OWN calibrated numbers, quoted here so the inverted checks are held to the
# same bar the gap pins were. The noise floor was measured on decades where the G1
# defect provably could not reach; the tolerance sits three decades above it.
ROOT_FINDER_NOISE_FLOOR = 2.353087957818972e-06
AMPLITUDE_TOLERANCE = 1000.0 * ROOT_FINDER_NOISE_FLOOR   # 2.353e-03


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


def _raises_value_error(fn):
    try:
        fn()
    except ValueError:
        return True
    return False


# ---------------------------------------------------------------------------
# (A) ROBUSTNESS THAT HELD ALL ALONG -- banked by leg 92, unchanged by the repair
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
    """`a` is deliberately NOT validated: it already propagates honestly, and the repair
    was scoped to the four measured defects rather than widened opportunistically."""
    x = grid(N)
    w0 = profile(x)
    with _quiet():
        for a in (np.nan, np.inf, -np.inf, 1e300):
            r = solve_gclm(w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
            assert r.outcome == "diverged", (a, r.outcome)
    return "a in {nan, +inf, -inf, 1e300} all reach outcome='diverged'"


def check_structural_adversaries_raise():
    with _quiet():
        assert _raises_value_error(lambda: solve_gclm(np.zeros(N), t_max=0.1)), \
            "identically-zero omega0 did not raise"
        assert _raises_value_error(
            lambda: clm_analytic_blowup_time(lambda x: np.sin(x)[:100], n_scan=256)), \
            "length-mismatched profile did not raise"
    return "zero data -> ValueError; length mismatch -> ValueError"


# ---------------------------------------------------------------------------
# (B) THE FOUR REPAIRS. Each was a `KNOWN GAP` pin under leg 92 and is INVERTED here.
# ---------------------------------------------------------------------------
def check_FIXED_zero_tolerance_is_scale_relative():
    """G1, solver/gclm.py. WAS: an ABSOLUTE tolerance `np.abs(w0) < 1e-12` decided which
    grid points count as zeros of w0 without ever measuring w0's scale. Below that
    amplitude the WHOLE grid was classified as the zero set, so the returned time became
    2/max_x H(w0) (GLOBAL max, 0.75) instead of 2/max{H(w0) : w0 = 0} (max over the ZERO
    SET, 0.5) -- a finite, positive, ordinary-looking blow-up time 1.5x too early.

    NOW: the tolerance is relative to max|w0|, so it scales with the data exactly as the
    CLM closed form's degree(-1) homogeneity in amplitude requires.

    Held to leg 92's own bar: all 11 amplitudes it flagged are replayed, and the
    invariant eps*T*(eps*w0) == T*(w0) must now hold to the SAME 2.353e-03 tolerance it
    calibrated by measurement -- and does, to the root-finder's noise floor or better.
    """
    with _quiet():
        t_ref = clm_analytic_blowup_time(profile, n_scan=N_SCAN)
        assert abs(t_ref - 4.0) < 1e-9, t_ref

        # every decade leg 92 flagged, plus three more far past where it stopped looking
        flagged = [1e-8, 1e-9, 1e-10, 1e-11, 3e-12, 1e-12, 6e-13, 5e-13,
                   1e-14, 1e-15, 1e-18]
        deeper = [1e-30, 1e-100, 1e-300]
        rels = {}
        for eps in flagged + deeper:
            t = clm_analytic_blowup_time(lambda x, e=eps: e * profile(x), n_scan=N_SCAN)
            assert t is not None and np.isfinite(t) and t > 0.0, (eps, t)
            rels[eps] = abs(eps * t - t_ref) / t_ref

        worst = max(rels.values())
        assert worst <= AMPLITUDE_TOLERANCE, (worst, rels)

        # and the specific pre-repair signatures are GONE, not merely under tolerance:
        # the 1/3 saturation deep down, and the 3.38e-03 breach at 1e-8.
        assert abs(rels[1e-14] - 1.0 / 3.0) > 0.3, rels[1e-14]
        assert rels[1e-14] < 1e-9, rels[1e-14]
        assert rels[1e-8] < 1e-9, rels[1e-8]

        # amplifying rather than shrinking must be just as invariant
        for eps in (1e2, 1e10, 1e100):
            t = clm_analytic_blowup_time(lambda x, e=eps: e * profile(x), n_scan=N_SCAN)
            assert abs(eps * t - t_ref) / t_ref <= AMPLITUDE_TOLERANCE, eps
    return (f"FIXED: eps*T* invariant over 14 decades down to eps=1e-300 and up to "
            f"1e+100; worst rel violation {worst:.3e} (leg 92's tolerance "
            f"{AMPLITUDE_TOLERANCE:.3e}, its noise floor {ROOT_FINDER_NOISE_FLOOR:.3e}). "
            f"At eps=1e-14 rel is {rels[1e-14]:.3e}, was 1/3; at 1e-8 "
            f"{rels[1e-8]:.3e}, was 3.380e-03.")


def check_FIXED_negative_nu_is_rejected():
    """G2, solver/gclm.py. WAS: dissipation was gated behind `if nu > 0.0`, so a negative
    nu failed that test and an anti-diffusive (ill-posed) request silently ran INVISCID
    and came back 'no_blowup' with an entirely finite payload -- omega_final BITWISE
    identical to the nu = 0 run. NaN nu did the same.

    NOW: ValueError at entry, before any state is built -- matching the guard landed in
    solver/fractional_gclm.py for the same class of defect. nu = 0 and nu = -0.0 stay
    admissible (-0.0 == 0.0, so skipping dissipation there is CORRECT, a false positive
    leg 92 itself caught and removed from its own count)."""
    x = grid(N)
    w0 = profile(x)
    kw = dict(a=0.5, t_max=0.3, max_steps=5000)
    with _quiet():
        for nu in (-1.0, -1e-30, -np.inf, np.nan):
            assert _raises_value_error(lambda v=nu: solve_gclm(w0, nu=v, **kw)), nu

        # not overshot: the admissible boundary is still admissible
        r_inv = solve_gclm(w0, nu=0.0, **kw)
        r_negzero = solve_gclm(w0, nu=-0.0, **kw)
        r_vis = solve_gclm(w0, nu=0.01, **kw)
        assert np.array_equal(r_negzero.omega_final, r_inv.omega_final)

        # leg 92's own magnitude, re-asserted unchanged: a real nu genuinely moves it,
        # which is what made the silent nu = -1.0 case a corruption and not a no-op
        honest = float(np.max(np.abs(r_inv.omega_final - r_vis.omega_final)))
        assert honest > 1e-3, honest
    return (f"FIXED: nu in {{-1.0, -1e-30, -inf, nan}} -> ValueError; nu = 0.0 and -0.0 "
            f"still admissible and bitwise equal; a real nu=0.01 still moves the "
            f"solution by {honest:.3e}")


def check_FIXED_conservation_guard_propagates_nan():
    """G3, solver/gclm.py. WAS: `conservation_drift = max(mean_drift, energy_residual)`.
    Python's builtin max(a, b) returns b only if b > a, and NaN loses every comparison,
    so max(finite, nan) == finite: the ONE number LOGGING.md's `solver_run` event records
    as the artifact guard was exactly the one that swallowed the NaN.

    NOW: an explicit NaN check first, np.nanmax for the ordinary path, and a dedicated
    `guard_nan` flag -- a NaN guard input is its own reportable failure state and the
    logged value is NaN, never a small number."""
    x = grid(N)
    w0 = profile(x)
    with _quiet():
        # the two cases leg 92 measured as silent, at the same `a` values
        for a, was in ((1e12, 4.9262000255399507e-17), (1e16, 1.1874147329819267e-16)):
            r = solve_gclm(w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
            assert not np.isfinite(r.energy_balance_residual), a   # input still NaN
            assert np.isnan(r.conservation_drift), (a, r.conservation_drift)
            assert r.guard_nan is True, a
            assert not _payload_all_finite(r), a
            assert was < 1e-12                # what it used to log: "clean"
            reached = float(np.max(np.abs(r.omega_final)))
            assert reached > 1e140, reached   # on a run this enormous

        # not overshot: when neither input is NaN the guard is the honest max, and the
        # a = 1e8 case (finite residual, reported honestly even before) is unchanged
        r8 = solve_gclm(w0, a=1e8, nu=0.0, t_max=0.3, max_steps=5000)
        assert r8.guard_nan is False
        assert r8.conservation_drift == max(r8.mean_drift, r8.energy_balance_residual)
        assert np.isfinite(r8.conservation_drift)

        r_ok = solve_gclm(w0, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
        assert r_ok.guard_nan is False
        assert r_ok.conservation_drift == max(r_ok.mean_drift,
                                              r_ok.energy_balance_residual)
    return ("FIXED: at a=1e12/1e16 the NaN energy residual now reaches the LOGGED "
            "conservation_drift as NaN with guard_nan=True (was 4.926e-17 / 1.187e-16, "
            f"reading 'clean'); at a=1e8 and a=0.5 the guard is still the honest max "
            f"({r_ok.conservation_drift:.4e})")


def check_FIXED_nan_stop_criteria_are_rejected():
    """G4, solver/gclm.py. WAS: every stop criterion was a bare comparison and every
    comparison against NaN is False, so each criterion was silently DROPPED. `t_max=nan`
    (and `t_max=-1.0`) ended the run before it started -- zero timesteps, and still
    outcome='no_blowup' with conservation_drift=0.0, a clean verdict from a run that
    never happened. `c1=nan`, `c2=nan` and, sharpest of all, `amplification_factor=nan`
    disabled the blow-up DETECTOR itself: at a=1e4 the clean run reports
    'blowup_candidate' and the poisoned one did not.

    NOW: np.isfinite is checked on entry, before any comparison, and a non-finite (or
    non-positive) criterion is refused outright."""
    x = grid(N)
    w0 = profile(x)
    nan = float("nan")
    with _quiet():
        for nm, kw in [("t_max=nan", dict(t_max=nan)),
                       ("t_max=-1.0", dict(t_max=-1.0)),
                       ("t_max=0.0", dict(t_max=0.0)),
                       ("dt_max=nan", dict(t_max=0.3, dt_max=nan)),
                       ("c1=nan", dict(t_max=0.3, c1=nan)),
                       ("c2=nan", dict(t_max=0.3, c2=nan)),
                       ("c1=0.0", dict(t_max=0.3, c1=0.0)),
                       ("max_steps=nan", dict(t_max=0.3, max_steps=nan)),
                       ("amplification_factor=nan",
                        dict(t_max=0.3, amplification_factor=nan))]:
            assert _raises_value_error(
                lambda k=kw: solve_gclm(w0, a=0.5, nu=0.0, **k)), nm

        # not overshot: the detector still fires on exactly the run leg 92 used to show
        # the suppression, and an ordinary run is untouched
        big = dict(a=1e4, nu=0.0, t_max=0.3, max_steps=5000)
        r_clean = solve_gclm(w0, **big)
        assert r_clean.outcome == "blowup_candidate", r_clean.outcome
        r_ord = solve_gclm(w0, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
        assert r_ord.n_timesteps == 30, r_ord.n_timesteps
    return ("FIXED: 9 poisoned stop-criteria configs all -> ValueError (t_max=nan and "
            "t_max=-1.0 used to return 'no_blowup' in 0 steps; c1/c2/"
            "amplification_factor=nan used to return 'no_blowup' in 30 steps); the "
            f"detector still fires ('{r_clean.outcome}' at a=1e4) and an ordinary run "
            f"still takes {r_ord.n_timesteps} steps")


# ---------------------------------------------------------------------------
# (C) THE REPAIR DID NOT OVERSHOOT -- production-path invariance
# ---------------------------------------------------------------------------
def check_repair_did_not_move_the_production_path():
    """The only production consumer of clm_analytic_blowup_time (stage1_5_sweep.py:369)
    energy-normalizes every IC to pi/2, i.e. O(1) amplitude -- about twelve decades above
    the old absolute tolerance -- and every solve_gclm caller passes nu >= 0 with finite
    stop criteria. So the four guards must be entirely invisible there. Asserted against
    the exact closed-form values test_gclm_dedicated.py already banks."""
    with _quiet():
        # closed-form CLM blow-up times. For w0 = A sin x, H(w0) = -A cos x, so the max
        # of H over the zero set {0, pi} is A and T* = 2/A -- the amplitude dependence
        # the closed form genuinely has, as opposed to the spurious one G1 introduced.
        for amp, exact in ((1.0, 2.0), (10.0, 0.2), (1e-9, 2e9), (1e9, 2e-9)):
            got = clm_analytic_blowup_time(lambda x, A=amp: A * np.sin(x))
            assert abs(got - exact) / exact < 1e-14, (amp, got, exact)
        got = clm_analytic_blowup_time(lambda x: -np.sin(x))
        assert abs(got - 2.0) / 2.0 < 1e-14, got
        assert clm_analytic_blowup_time(lambda x: 1.0 + 0.5 * np.sin(x)) is None

        # a production-shaped parameter set runs untouched
        x = grid(N)
        r = solve_gclm(np.sin(x), a=0.7, nu=0.0, t_max=1.0, dt_max=1e-2,
                       c1=0.05, c2=0.4, max_steps=200_000,
                       amplification_factor=100.0,
                       early_decay_exit={"fraction": 0.1, "window": 2.0})
        assert r.outcome in ("no_blowup", "blowup_candidate"), r.outcome
        assert r.guard_nan is False
        assert _payload_all_finite(r)
    return ("no overshoot: T*(A sin x) = 2/A to 1e-14 at A = 1, 10, 1e-9 and 1e9 "
            "(the closed form's own amplitude law, now obeyed on both sides), "
            "T*(1+0.5 sin)=None, and a production-shaped solve_gclm call is unaffected")


CHECKS = [
    check_nan_seeded_vorticity_is_flagged,
    check_extreme_finite_a_is_not_clamped,
    check_nonfinite_a_is_flagged,
    check_structural_adversaries_raise,
    check_FIXED_zero_tolerance_is_scale_relative,
    check_FIXED_negative_nu_is_rejected,
    check_FIXED_conservation_guard_propagates_nan,
    check_FIXED_nan_stop_criteria_are_rejected,
    check_repair_did_not_move_the_production_path,
]


def main():
    n_fixed = 0
    for fn in CHECKS:
        head = fn()
        tag = "PASS"
        if fn.__name__.startswith("check_FIXED"):
            n_fixed += 1
            tag = "FIXED"
        print(f"{tag} {fn.__name__}: {head}")
    print(f"\nall gclm adversarial checks passed ({len(CHECKS)} checks, "
          f"{n_fixed} of them leg 92 KNOWN GAPS now INVERTED into fix assertions).")
    print("All 19 of leg 92's silent corruptions are closed: 11 amplitude (G1), "
          "1 viscosity (G2), 2 conservation guard (G3), 5 stop criteria (G4).")


if __name__ == "__main__":
    main()
