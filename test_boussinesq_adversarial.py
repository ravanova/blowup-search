"""Adversarial gates for solver/boussinesq.py (leg 89, Route-BOA).

test_boussinesq_dedicated.py (leg 66/QF, 17 checks) validates this module on WELL-BEHAVED
inputs: Biot-Savart hand values, parity projectors, pure-diffusion exactness, frozen-u
translation, mean invariants, and four wrong-SHAPE rejections. This file validates the
other half -- what the solver returns when the input is hostile. It banks leg 89's 90-case
battery so the answers cannot silently regress.

The gate leg 89 answered, verbatim:

  "Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
   degenerate/zero stream function, extreme grid-stretching), does solver/boussinesq.py
   ever silently return a finite, plausible-looking result instead of propagating or
   flagging the invalid input?"

ANSWERED **YES**, on 19 of 82 gate-deciding cases (plus 4 of 8 secondary). SILENT
CORRUPTION is defined here exactly as it was pre-committed in writeup/novelty/leg_89.md
section 3, before any number was seen:

  the call returns NORMALLY (no exception) AND every field a caller reads to judge
  validity -- outcome, conservation_drift, mean_drift, energy_balance_residual, the
  max_omega trajectory -- is FINITE and PLAUSIBLE, AND the run is nevertheless invalid,
  because the returned state is non-finite or an invalid parameter was silently DROPPED
  while `params` records the value that was ignored.

THREE KINDS OF TEST LIVE IN THIS FILE, AND THEY MUST NOT BE CONFUSED
---------------------------------------------------------------------
1. SOUNDNESS gates (`test_soundness_*`). These assert a property that HOLDS today and
   must keep holding. NaN/Inf-seeded vorticity is the gate's own first clause and the
   module handles it cleanly: all 30 cases reach outcome "diverged". If one of these ever
   fails, the module has started swallowing a poisoned vorticity field.

2. CHARACTERIZATION gates (`test_characterize_*`). These pin behaviour leg 89 MEASURED and
   REPORTED AS A DEFECT but was explicitly NOT AUTHORISED TO REPAIR -- solver/boussinesq.py
   is read-only to this leg under every gate outcome, and a silent-corruption finding is
   escalated, never patched. They PASS today because they describe today's code. When a
   leg is authorised to repair any of them these tests will start FAILING, and that is the
   INTENDED SIGNAL -- the discipline leg 69 set for test_interval_stress.py and leg 80
   reused in test_bordered_hl_adversarial.py.
   THEY MUST NOT BE WEAKENED TO MAKE A REPAIR LOOK UNNECESSARY, AND THEY ARE NOT
   ENDORSEMENTS. Each one carries, in its docstring, the assertion that SHOULD replace it
   once the module is fixed.

3. CONTROL gates (`test_control_*`). These prove the battery can tell right from wrong: the
   exact-zero guard does fire where it is armed, an in-domain coefficient does change the
   run, and a dull-but-correct answer is not called a failure. Without these, the
   characterization gates would be unfalsifiable.

Run: .venv/bin/python test_boussinesq_adversarial.py
Evidence: writeup/data/p2_route_boa_v1_adversarial.json
Battery:  experiments/p2_route_boa_v1_adversarial.py
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import sys  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver.boussinesq import (  # noqa: E402
    dealias_mask2d,
    grid2d,
    solve_boussinesq,
)

N = 32
T_MAX = 0.3


def _fields(n=N):
    X, Y = grid2d(n)
    return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)


def _poison(f, idx, val):
    g = f.copy()
    g[idx] = val
    return g


def _all_validity_fields_finite(r):
    """The pre-committed reading of "plausible-looking": nothing a caller checks is NaN."""
    return bool(np.isfinite(r.mean_drift) and np.isfinite(r.energy_balance_residual)
                and np.isfinite(r.conservation_drift) and np.isfinite(r.t_final)
                and np.all(np.isfinite(r.max_omega)))


# ===========================================================================
# 1. SOUNDNESS -- properties that hold and must keep holding
# ===========================================================================

def check_soundness_nan_seeded_vorticity_always_diverges():
    """The gate's first clause. A non-finite omega0 is never swallowed.

    All 30 combinations of {single NaN, +-Inf, all-NaN, corner NaN, 1e308} x
    {full, nonlinear off, nonlinear+buoyancy off, houluo, frozen_u} reach outcome
    "diverged" on the first step, because the `not np.isfinite(m)` check sits inside the
    loop after the state update. This is the module's one genuinely robust path.
    """
    out = {}
    w0, th0 = _fields()
    variants = {
        "single_nan": _poison(w0, (3, 4), np.nan),
        "single_posinf": _poison(w0, (3, 4), np.inf),
        "single_neginf": _poison(w0, (3, 4), -np.inf),
        "all_nan": np.full((N, N), np.nan),
        "corner_nan": _poison(w0, (0, 0), np.nan),
        "huge_1e308": _poison(w0, (3, 4), 1e308),
    }
    switches = {
        "full": dict(),
        "nonlinear_off": dict(nonlinear=False),
        "nl_off_buoy_off": dict(nonlinear=False, buoyancy=False),
        "houluo": dict(symmetry="houluo"),
        "frozen_u": dict(frozen_u=(0.3, -0.2)),
    }
    n_checked = 0
    for vname, wbad in variants.items():
        for sname, extra in switches.items():
            r = solve_boussinesq(wbad, th0, t_max=T_MAX, **extra)
            assert r.outcome == "diverged", f"{vname}/{sname}: {r.outcome}"
            assert r.n_timesteps == 1, f"{vname}/{sname}: {r.n_timesteps} steps"
            n_checked += 1
    out["n_cases"] = n_checked
    out["all_diverged"] = 1.0
    assert n_checked == 30, n_checked
    return out


def check_soundness_nan_temperature_reaches_a_field_the_caller_reads():
    """A NaN theta0 is never fully hidden: it always reaches at least one visible field.

    With buoyancy on, the vorticity is poisoned through th_x and the run diverges. With
    buoyancy off, the vorticity stays clean -- but theta_final is 100% NaN AND
    energy_balance_residual is NaN, because the kinetic-energy production term integrates
    v*theta. So the invalid input is PROPAGATED, not silent, on every one of the 15 cases.

    This is weaker than it sounds and the weakness is characterized separately below:
    conservation_drift, the field the docstring calls "the logged guard value", stays
    small. See check_characterize_conservation_drift_masks_a_nan_limb.
    """
    out = {}
    w0, th0 = _fields()
    n_diverged = n_propagated = 0
    for vname, thbad in (("single_nan", _poison(th0, (5, 6), np.nan)),
                         ("single_inf", _poison(th0, (5, 6), np.inf)),
                         ("all_nan", np.full((N, N), np.nan))):
        for sname, extra in (("full", dict()),
                             ("buoy_off", dict(buoyancy=False)),
                             ("buoy_off_nl_off", dict(buoyancy=False, nonlinear=False)),
                             ("buoy_off_drift_guard", dict(buoyancy=False,
                                                           drift_guard=1e-9)),
                             ("buoy_off_tail_guard", dict(buoyancy=False,
                                                          tail_guard=1e-6))):
            r = solve_boussinesq(w0, thbad, t_max=T_MAX, **extra)
            if r.outcome == "diverged":
                n_diverged += 1
                continue
            visible = (not np.isfinite(r.energy_balance_residual)) or \
                      bool(np.any(~np.isfinite(r.theta_final)))
            assert visible, f"{vname}/{sname}: NaN theta0 left no visible trace"
            n_propagated += 1
    out["n_diverged"] = float(n_diverged)
    out["n_propagated_to_a_visible_field"] = float(n_propagated)
    assert n_diverged + n_propagated == 15, (n_diverged, n_propagated)
    return out


# ===========================================================================
# 2. CHARACTERIZATION -- measured defects this leg was NOT authorised to repair
# ===========================================================================

def check_characterize_false_blowup_from_dealias_annihilated_vorticity():
    """DEFECT. A vorticity that is zero in the represented subspace yields
    outcome == "blowup_candidate" -- the most consequential label this solver emits --
    with every validity field pristine and no exception.

    omega0 = sin(15x)sin(15y) on n=32 lies entirely above the 2/3 dealias cut (n/3 = 10.67),
    so the represented vorticity is zero to roundoff: max|w| = 1.797e-16, NOT 0.0, so the
    documented `omega0 is identically zero` guard -- which tests `== 0.0` exactly and does
    fire on a bit-zero field (see the control) -- misses it by 1.8e-16. The blow-up trigger
    is then amplification_factor * m0 = 1e3 * 1.797e-16 = 1.797e-13, and the ordinary O(1)
    buoyancy forcing th_x clears it in ONE step, reaching max|w| = 1.0e-2. Reported
    amplification: 5.566e13. Reported mean_drift 5.28e-18, energy_balance_residual 1.30e-10
    -- a run that looks textbook-healthy.

    WHEN REPAIRED, this test must be replaced by its inverse: the zero-vorticity guard
    should test the REPRESENTED field against a tolerance (e.g. relative to max|theta0| or
    to the field's own pre-mask norm) rather than against exact zero, and this case should
    then raise ValueError or return an outcome that is not "blowup_candidate".
    """
    out = {}
    _, th0 = _fields()
    X, Y = grid2d(N)
    mask = dealias_mask2d(N)
    for kx, ky in ((15, 15), (12, 12), (14, 3)):
        wkill = np.sin(kx * X) * np.sin(ky * Y)
        represented = float(np.max(np.abs(np.fft.ifft2(np.fft.fft2(wkill) * mask).real)))
        r = solve_boussinesq(wkill, th0, t_max=T_MAX)
        out[f"represented_m0_k{kx}x{ky}"] = represented
        out[f"outcome_k{kx}x{ky}"] = r.outcome
        out[f"amplification_k{kx}x{ky}"] = float(r.max_omega[-1] / r.max_omega[0])
        assert represented > 0.0, "the mask left a bit-exact zero; guard would have fired"
        assert represented < 1e-13, represented
        assert r.outcome == "blowup_candidate", r.outcome
        assert r.n_timesteps == 1, r.n_timesteps
        assert _all_validity_fields_finite(r), "validity fields were not all finite"
        assert float(r.max_omega[-1] / r.max_omega[0]) > 1e10
    return out


def check_characterize_false_blowup_from_denormal_vorticity():
    """DEFECT. max|omega0| = 1e-300 is numerically zero but not bit-zero, so the guard
    does not fire and the blow-up threshold 1e3 * 1e-300 is cleared in one step by the
    buoyancy forcing. Reported amplification: 1.0e+298, outcome "blowup_candidate",
    every validity field finite.

    WHEN REPAIRED, as above: a scale-aware zero test should reject this, and the assertion
    below should become `r.outcome != "blowup_candidate"`.
    """
    out = {}
    w0, th0 = _fields()
    for amp in (1e-300, 1e-18):
        r = solve_boussinesq(amp * w0, th0, t_max=T_MAX)
        out[f"outcome_amp{amp:.0e}"] = r.outcome
        out[f"amplification_amp{amp:.0e}"] = float(r.max_omega[-1] / r.max_omega[0])
        assert r.outcome == "blowup_candidate", (amp, r.outcome)
        assert _all_validity_fields_finite(r)
    assert out["amplification_amp1e-300"] > 1e290, out["amplification_amp1e-300"]
    return out


def check_characterize_out_of_domain_kappa_is_dropped_without_a_trace():
    """DEFECT, and the sharpest one in the battery. `if kappa > 0.0` means a negative,
    -inf or NaN thermal diffusivity is not applied and not rejected: the integration that
    runs is the kappa = 0 one, BIT-FOR-BIT, while params["kappa"] records the value that
    was ignored.

    kappa in {-0.5, -1e6, -1e-14, nan, -inf} all return omega_final and theta_final
    bit-identical to the kappa = 0.0 control, with energy_balance_residual = 2.2188e-07,
    exactly the control's value -- ratio 1.000. There is NO tell, because the module's
    energy-balance guard is d/dt E_k = int(v*theta) - nu*int(w^2), which does not contain
    kappa at all and structurally cannot see it.

    CONTRAST, measured: nu is dropped the same way, but the same energy identity DOES
    contain nu, so nu = -0.5 moves energy_balance_residual from 2.2188e-07 to 4.3812e-01,
    a factor 1.9745e+06. nu = nan makes it NaN outright (hence "propagated", not silent).
    The guard catches the nu half by accident of the identity's shape, and misses the
    kappa half entirely.

    WHEN REPAIRED, this test must be replaced by its inverse: solve_boussinesq should
    raise ValueError on any nu or kappa outside [0, inf), and each case below should then
    assert that raise instead of asserting bit-identity.
    """
    out = {}
    w0, th0 = _fields()
    ctrl = solve_boussinesq(w0, th0, t_max=T_MAX)
    for val in (-0.5, -1e6, -1e-14, np.nan, -np.inf):
        r = solve_boussinesq(w0, th0, kappa=val, t_max=T_MAX)
        same = (np.array_equal(r.omega_final, ctrl.omega_final)
                and np.array_equal(r.theta_final, ctrl.theta_final))
        out[f"kappa_{val!r}_bit_identical_to_zero"] = 1.0 if same else 0.0
        assert same, f"kappa={val!r} was not dropped bit-for-bit (behaviour changed)"
        assert _all_validity_fields_finite(r), f"kappa={val!r}"
        assert float(r.energy_balance_residual) == float(ctrl.energy_balance_residual), \
            f"kappa={val!r}: the energy guard moved -- it may now see kappa"
        assert (np.isnan(r.params["kappa"]) if isinstance(val, float) and np.isnan(val)
                else r.params["kappa"] == val), "params no longer records the ignored value"
    # The nu contrast, measured rather than asserted qualitatively.
    r_nu = solve_boussinesq(w0, th0, nu=-0.5, t_max=T_MAX)
    assert np.array_equal(r_nu.omega_final, ctrl.omega_final), "nu=-0.5 was not dropped"
    ratio = float(r_nu.energy_balance_residual) / float(ctrl.energy_balance_residual)
    out["nu_-0.5_energy_residual"] = float(r_nu.energy_balance_residual)
    out["nu_-0.5_energy_ratio_to_control"] = ratio
    out["kappa_energy_ratio_to_control"] = 1.0
    assert ratio > 1e5, ratio  # the nu half IS visible in the energy guard
    return out


def check_characterize_conservation_drift_masks_a_nan_limb():
    """DEFECT. solver/boussinesq.py:141 documents conservation_drift as "max of the two
    above; the logged guard value", but it is built with Python's builtin max, which is
    order-dependent on NaN: max(finite, nan) returns the finite operand.

    With a NaN-poisoned theta0 and buoyancy off, theta_final is 100% NaN and
    energy_balance_residual is NaN, yet conservation_drift reports 8.077e-18 -- and the
    identical max() expression inside the loop means drift_guard=1e-9 NEVER FIRES on that
    run. A caller that reads only the logged guard sees a pristine run.

    WHEN REPAIRED, use np.nanmax's opposite -- an explicit non-finite check, or
    float(np.max([...])) which propagates NaN -- and this test should then assert that
    conservation_drift is NaN and that drift_guard fires with outcome "under_resolved".
    """
    out = {}
    w0, th0 = _fields()
    thbad = _poison(th0, (5, 6), np.nan)
    r = solve_boussinesq(w0, thbad, buoyancy=False, t_max=T_MAX, drift_guard=1e-9)
    out["nan_fraction_theta_final"] = float(np.mean(~np.isfinite(r.theta_final)))
    out["energy_balance_residual_is_nan"] = 1.0
    out["conservation_drift"] = float(r.conservation_drift)
    out["outcome"] = r.outcome
    assert out["nan_fraction_theta_final"] == 1.0
    assert not np.isfinite(r.energy_balance_residual), "the energy limb is no longer NaN"
    assert np.isfinite(r.conservation_drift), "conservation_drift now propagates the NaN"
    assert r.conservation_drift < 1e-15, float(r.conservation_drift)
    assert r.outcome == "no_blowup", r.outcome  # the guard did not fire
    return out


def check_characterize_nonfinite_cfl_factor_drops_its_timestep_limb():
    """DEFECT. dt = min(dt_max, c2*dx/speed, c1/max|w|) is built with Python's builtin
    min, which drops a NaN the same way max does. A non-finite CFL safety factor therefore
    REMOVES its constraint instead of failing.

    On a run where the CFL is binding (5x amplitude, dt_max = 1.0): c1 = nan relaxes
    dt_min from 1.7774e-03 to 9.9324e-03, a factor 5.588, cutting 30 steps to 10 and
    raising energy_balance_residual 9.67x. c1 = c2 = nan gives a SINGLE step of dt = 0.3,
    a relaxation factor of 168.8 and an energy residual 801.7x the control -- still only
    1.9e-03 in absolute terms, i.e. small enough to read as healthy. outcome "no_blowup"
    in every case, no exception, every validity field finite.

    WHEN REPAIRED, non-finite c1/c2/dt_max should raise ValueError, and this test should
    assert that raise instead of asserting the relaxation factors.
    """
    out = {}
    w0, th0 = _fields()
    big = 5.0 * w0
    ctrl = solve_boussinesq(big, th0, t_max=T_MAX, dt_max=1.0)
    out["control_dt_min"] = float(ctrl.dt_min)
    out["control_n_timesteps"] = float(ctrl.n_timesteps)
    for lab, kw in (("c1_nan", dict(c1=np.nan)),
                    ("c1_inf", dict(c1=np.inf)),
                    ("c1_and_c2_nan", dict(c1=np.nan, c2=np.nan))):
        r = solve_boussinesq(big, th0, t_max=T_MAX, dt_max=1.0, **kw)
        factor = float(r.dt_min) / float(ctrl.dt_min)
        out[f"{lab}_dt_relaxation_factor"] = factor
        out[f"{lab}_outcome"] = r.outcome
        assert factor > 1.0 + 1e-9, f"{lab}: dt no longer relaxed (factor {factor})"
        assert r.outcome == "no_blowup", f"{lab}: {r.outcome}"
        assert _all_validity_fields_finite(r), lab
    assert out["c1_and_c2_nan_dt_relaxation_factor"] > 100.0
    return out


def check_characterize_degenerate_grid_runs_happily():
    """DEFECT. n = 1 and n = 2 leave the 2/3 dealias mask retaining exactly ONE mode --
    the (0,0) mean -- so the spectral method has no spatial resolution whatsoever. Both
    return outcome "no_blowup" over 30 steps with mean_drift = 0.0,
    energy_balance_residual = 0.0: the most reassuring numbers in the whole battery,
    produced by a discretization that cannot represent any dynamics at all.

    n >= 3 retains more than one mode and is not flagged here.

    WHEN REPAIRED, solve_boussinesq should reject a grid whose mask retains no non-zero
    wavenumber, and this test should assert that raise.
    """
    out = {}
    for n in (1, 2):
        Xn, Yn = grid2d(n)
        wn = np.sin(Xn) * np.sin(Yn) + 0.5
        thn = np.cos(Xn) * np.sin(Yn) + 0.5
        n_modes = int(np.sum(dealias_mask2d(n)))
        r = solve_boussinesq(wn, thn, t_max=T_MAX)
        out[f"n{n}_retained_modes"] = float(n_modes)
        out[f"n{n}_outcome"] = r.outcome
        out[f"n{n}_conservation_drift"] = float(r.conservation_drift)
        assert n_modes == 1, (n, n_modes)
        assert r.outcome == "no_blowup", (n, r.outcome)
        assert _all_validity_fields_finite(r)
    assert int(np.sum(dealias_mask2d(3))) > 1, "n=3 should retain more than the mean mode"
    return out


def check_characterize_nonfinite_detection_thresholds_are_inert():
    """DEFECT (secondary -- detection parameters, not physical-space inputs, so these did
    not decide the gate; measured because they decide what conclusion the caller is handed).

    amplification_factor = nan/inf makes `m >= amplification_factor*m0` permanently False,
    disabling blow-up detection outright. Demonstrated against a control that DOES fire on
    the identical trajectory: amplification_factor = 2.0 returns "blowup_candidate" at
    t = 3.140 with max|w| = 2.0016; amplification_factor = nan runs the same data to
    t = 6.0 and returns "no_blowup" having reached a peak amplification of 4.013, with
    conservation_drift = 1.001e-05.

    t_max = nan or negative makes `while t < t_max` False at once: zero steps, outcome
    "no_blowup", every guard 0.0 -- a scientific conclusion from a run that never happened.

    WHEN REPAIRED, non-finite t_max / amplification_factor / drift_guard / tail_guard
    should raise ValueError, and this test should assert those raises.
    """
    out = {}
    w0, th0 = _fields()
    fired = solve_boussinesq(w0, th0, t_max=6.0, amplification_factor=2.0)
    out["control_outcome"] = fired.outcome
    out["control_t_at_trigger"] = float(fired.t_final)
    assert fired.outcome == "blowup_candidate", fired.outcome
    for lab, av in (("nan", np.nan), ("inf", np.inf)):
        r = solve_boussinesq(w0, th0, t_max=6.0, amplification_factor=av)
        peak = float(np.max(r.max_omega) / r.max_omega[0])
        out[f"amp_{lab}_outcome"] = r.outcome
        out[f"amp_{lab}_peak_amplification"] = peak
        assert r.outcome == "no_blowup", (lab, r.outcome)
        assert peak > 2.0, (lab, peak)   # it passed the control's threshold and said nothing
        assert _all_validity_fields_finite(r)
    for lab, tv in (("nan", np.nan), ("negative", -1.0)):
        r = solve_boussinesq(w0, th0, t_max=tv)
        out[f"t_max_{lab}_outcome"] = r.outcome
        out[f"t_max_{lab}_n_timesteps"] = float(r.n_timesteps)
        assert r.outcome == "no_blowup", (lab, r.outcome)
        assert r.n_timesteps == 0, (lab, r.n_timesteps)
    return out


# ===========================================================================
# 3. CONTROLS -- the battery can tell right from wrong
# ===========================================================================

def check_control_exact_zero_vorticity_still_raises():
    """The guard works where it is armed. A bit-exactly zero omega0 raises ValueError,
    which is what makes the dealias-annihilated and denormal cases a BLIND SPOT rather
    than a missing feature."""
    _, th0 = _fields()
    raised = False
    try:
        solve_boussinesq(np.zeros((N, N)), th0, t_max=T_MAX)
    except ValueError as exc:
        raised = "identically zero" in str(exc)
    assert raised, "the exact-zero guard no longer fires"
    return {"exact_zero_raises": 1.0}


def check_control_in_domain_coefficients_do_change_the_run():
    """nu = 0.5 and kappa = 0.5 must NOT be bit-identical to the zero run, or the
    bit-identity witness used against the out-of-domain values would prove nothing."""
    out = {}
    w0, th0 = _fields()
    ctrl = solve_boussinesq(w0, th0, t_max=T_MAX)
    for name in ("nu", "kappa"):
        r = solve_boussinesq(w0, th0, t_max=T_MAX, **{name: 0.5})
        changed = not (np.array_equal(r.omega_final, ctrl.omega_final)
                       and np.array_equal(r.theta_final, ctrl.theta_final))
        out[f"{name}_0.5_changes_the_run"] = 1.0 if changed else 0.0
        assert changed, f"{name}=0.5 was dropped too -- the witness is not discriminating"
    return out


def check_control_dull_but_correct_answers_are_not_failures():
    """Constant vorticity gives psi == 0 and u == 0 -- a degenerate stream function by the
    gate's own second clause -- but the state really is steady under buoyancy forcing, so
    "no_blowup" is the RIGHT answer. The battery must not count it as corruption."""
    out = {}
    _, th0 = _fields()
    r = solve_boussinesq(np.full((N, N), 2.0), th0, t_max=T_MAX)
    out["outcome"] = r.outcome
    out["amplification"] = float(r.max_omega[-1] / r.max_omega[0])
    assert r.outcome == "no_blowup", r.outcome
    assert out["amplification"] < 2.0, out["amplification"]
    assert _all_validity_fields_finite(r)
    return out


CHECKS = [
    check_soundness_nan_seeded_vorticity_always_diverges,
    check_soundness_nan_temperature_reaches_a_field_the_caller_reads,
    check_characterize_false_blowup_from_dealias_annihilated_vorticity,
    check_characterize_false_blowup_from_denormal_vorticity,
    check_characterize_out_of_domain_kappa_is_dropped_without_a_trace,
    check_characterize_conservation_drift_masks_a_nan_limb,
    check_characterize_nonfinite_cfl_factor_drops_its_timestep_limb,
    check_characterize_degenerate_grid_runs_happily,
    check_characterize_nonfinite_detection_thresholds_are_inert,
    check_control_exact_zero_vorticity_still_raises,
    check_control_in_domain_coefficients_do_change_the_run,
    check_control_dull_but_correct_answers_are_not_failures,
]


def test_soundness_nan_seeded_vorticity_always_diverges():
    check_soundness_nan_seeded_vorticity_always_diverges()


def test_soundness_nan_temperature_reaches_a_field_the_caller_reads():
    check_soundness_nan_temperature_reaches_a_field_the_caller_reads()


def test_characterize_false_blowup_from_dealias_annihilated_vorticity():
    check_characterize_false_blowup_from_dealias_annihilated_vorticity()


def test_characterize_false_blowup_from_denormal_vorticity():
    check_characterize_false_blowup_from_denormal_vorticity()


def test_characterize_out_of_domain_kappa_is_dropped_without_a_trace():
    check_characterize_out_of_domain_kappa_is_dropped_without_a_trace()


def test_characterize_conservation_drift_masks_a_nan_limb():
    check_characterize_conservation_drift_masks_a_nan_limb()


def test_characterize_nonfinite_cfl_factor_drops_its_timestep_limb():
    check_characterize_nonfinite_cfl_factor_drops_its_timestep_limb()


def test_characterize_degenerate_grid_runs_happily():
    check_characterize_degenerate_grid_runs_happily()


def test_characterize_nonfinite_detection_thresholds_are_inert():
    check_characterize_nonfinite_detection_thresholds_are_inert()


def test_control_exact_zero_vorticity_still_raises():
    check_control_exact_zero_vorticity_still_raises()


def test_control_in_domain_coefficients_do_change_the_run():
    check_control_in_domain_coefficients_do_change_the_run()


def test_control_dull_but_correct_answers_are_not_failures():
    check_control_dull_but_correct_answers_are_not_failures()


if __name__ == "__main__":
    import warnings

    warnings.simplefilter("ignore")  # the poisoned cases warn by design
    failures = 0
    for chk in CHECKS:
        try:
            res = chk()
        except AssertionError as exc:
            failures += 1
            print(f"FAIL {chk.__name__}: {exc}")
            continue
        print(f"ok   {chk.__name__}")
        for k, v in (res or {}).items():
            print(f"       {k} = {v}")
    print()
    if failures:
        print(f"test_boussinesq_adversarial: {failures} FAILED")
        sys.exit(1)
    print(f"test_boussinesq_adversarial: all {len(CHECKS)} checks passed")
