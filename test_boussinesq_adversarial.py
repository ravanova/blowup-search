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

ANSWERED **YES** by leg 89, on 19 of 82 gate-deciding cases (plus 4 of 8 secondary).
SILENT CORRUPTION is defined here exactly as it was pre-committed in
writeup/novelty/leg_89.md section 3, before any number was seen:

  the call returns NORMALLY (no exception) AND every field a caller reads to judge
  validity -- outcome, conservation_drift, mean_drift, energy_balance_residual, the
  max_omega trajectory -- is FINITE and PLAUSIBLE, AND the run is nevertheless invalid,
  because the returned state is non-finite or an invalid parameter was silently DROPPED
  while `params` records the value that was ignored.

**THE ANSWER IS NOW NO. THE REPAIR HAS LANDED** (bench-repair branch
`bench/fix-boussinesq-silent-corruption`, "Leg 0: ORCH"). Re-running leg 89's
UNCHANGED 90-case battery against the repaired module gives 0 gate-deciding silent
cases and 0 secondary, and `conservation_drift` masks a NaN limb in 0 of 90 rather
than 13 of 90. Leg 89's own artifact is deliberately left as it was measured; the
repair's evidence is writeup/data/bench_boussinesq_silent_corruption_check.json.

THREE KINDS OF TEST LIVE IN THIS FILE, AND THEY MUST NOT BE CONFUSED
---------------------------------------------------------------------
1. SOUNDNESS gates (`test_soundness_*`). These assert a property that HOLDS and must
   keep holding. NaN/Inf-seeded vorticity is the gate's own first clause and the
   module handled it cleanly even before the repair: all 30 cases reach outcome
   "diverged". If one of these ever fails, the module has started swallowing a
   poisoned vorticity field.

2. REPAIR gates (`test_repaired_*`). These were leg 89's `test_characterize_*` gates,
   which PINNED each defect as it was measured because leg 89 was not authorised to
   fix it. They are now INVERTED, not weakened, following the conversion legs 66/79/
   83/85 used: every magnitude leg 89 measured is still computed and still asserted
   at the same threshold, and what flipped is only the verdict -- from "the module
   accepts this" to "the module refuses this". The pre-fix numbers stay in each
   docstring as the record of what was repaired, so the file cannot later be read as
   though the defect never existed. THEY MUST NOT BE WEAKENED.

3. CONTROL gates (`test_control_*`). These prove the battery can tell right from wrong:
   the zero guard fires where it is armed, an in-domain coefficient does change the
   run, and a dull-but-correct answer is not called a failure. Without these, the
   repair gates would be unfalsifiable -- a module that refused EVERYTHING would pass
   every gate in section 2 and fail every one of these.

Run: .venv/bin/python test_boussinesq_adversarial.py
Evidence (pre-fix): writeup/data/p2_route_boa_v1_adversarial.json
Evidence (repair):  writeup/data/bench_boussinesq_silent_corruption_check.json
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

    Before the repair this was weaker than it sounds: conservation_drift, the field the
    docstring calls "the logged guard value", stayed small on all 15. That hole is now
    closed -- see check_repaired_conservation_drift_propagates_a_nan_limb -- and three
    of the drift_guard cases consequently now stop as "under_resolved" instead of
    running to completion. Both stopping and propagating are PASSES here; the gate is
    that the invalid input is never fully hidden.
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
# 2. REPAIR -- leg 89's characterization gates, INVERTED once the fix landed
# ===========================================================================

def _rejects(fn):
    """Run fn(); return the ValueError message, or None if it did not raise."""
    try:
        fn()
    except ValueError as exc:
        return str(exc)
    return None


def check_repaired_dealias_annihilated_vorticity_is_rejected():
    """REPAIRED (defect 1, the most consequential). A vorticity that is zero in the
    represented subspace used to yield outcome == "blowup_candidate" -- the most
    consequential label this solver emits -- with every validity field pristine and no
    exception. It is now refused at entry.

    PRE-FIX, MEASURED BY LEG 89 AND STILL COMPUTED BELOW: omega0 = sin(15x)sin(15y) on
    n=32 lies entirely above the 2/3 dealias cut (n/3 = 10.67), so the represented
    vorticity is zero to roundoff -- max|w| = 1.797e-16, NOT 0.0 -- and the documented
    `omega0 is identically zero` guard, which tested `== 0.0` exactly, missed it by
    1.8e-16. The blow-up trigger was then amplification_factor * m0 = 1.797e-13, which
    the ordinary O(1) buoyancy forcing th_x cleared in ONE step, reaching max|w| = 1e-2
    for a reported amplification of 5.566e13, with mean_drift 5.28e-18 and
    energy_balance_residual 1.30e-10 -- a run that looked textbook-healthy.

    POST-FIX: the guard is scale-aware (ZERO_OMEGA_REL_TOL = 1e-13 relative to the
    initial state's own scale) and raises ValueError. The roundoff-level represented m0
    is STILL measured here at the same threshold, so this gate keeps testing the
    condition that produced the defect and not merely "some exception happens".
    """
    out = {}
    _, th0 = _fields()
    X, Y = grid2d(N)
    mask = dealias_mask2d(N)
    for kx, ky in ((15, 15), (12, 12), (14, 3)):
        wkill = np.sin(kx * X) * np.sin(ky * Y)
        represented = float(np.max(np.abs(np.fft.ifft2(np.fft.fft2(wkill) * mask).real)))
        out[f"represented_m0_k{kx}x{ky}"] = represented
        # unchanged from leg 89: the input really is dealias-annihilated, and really is
        # NOT bit-zero, so the old exact-zero guard genuinely could not see it.
        assert represented > 0.0, "the mask left a bit-exact zero; the old guard would fire"
        assert represented < 1e-13, represented
        msg = _rejects(lambda: solve_boussinesq(wkill, th0, t_max=T_MAX))
        out[f"rejected_k{kx}x{ky}"] = 1.0 if msg else 0.0
        assert msg is not None, f"k{kx}x{ky}: still returns instead of raising"
        assert "numerically zero" in msg, msg
    # and under the Hou-Luo projection too (leg 89's fourth silent case in this family)
    wkill = np.sin(15 * X) * np.sin(15 * Y)
    msg = _rejects(lambda: solve_boussinesq(wkill, th0, t_max=T_MAX, symmetry="houluo"))
    out["rejected_houluo"] = 1.0 if msg else 0.0
    assert msg is not None, "houluo path still returns instead of raising"
    return out


def check_repaired_denormal_vorticity_is_rejected():
    """REPAIRED (defect 1, second family). max|omega0| = 1e-300 is numerically zero but
    not bit-zero, so the exact-zero guard did not fire and the blow-up threshold
    1e3 * 1e-300 was cleared in one step by the buoyancy forcing.

    PRE-FIX: outcome "blowup_candidate", reported amplification 1.0e+298 (and the same
    at 1e-18), every validity field finite.

    POST-FIX: rejected. Amplification measured against an m0 that the state scale cannot
    distinguish from zero is not amplification of the data -- it is forcing response --
    so no blow-up verdict can be given, and the module now says so instead of emitting
    the strongest label it has.
    """
    out = {}
    w0, th0 = _fields()
    for amp in (1e-300, 1e-18):
        msg = _rejects(lambda a=amp: solve_boussinesq(a * w0, th0, t_max=T_MAX))
        out[f"rejected_amp{amp:.0e}"] = 1.0 if msg else 0.0
        assert msg is not None, f"amp={amp:.0e} still returns instead of raising"
        assert "numerically zero" in msg, msg
    # The boundary is not a blanket ban on small vorticity: a uniformly scaled-down but
    # RESOLVABLE field (1e-6 of the theta scale, far above the 1e-13 tolerance) still
    # runs, and runs to a normal outcome. Without this the gate above would be passed
    # by a module that simply refused every small omega0.
    r = solve_boussinesq(1e-6 * w0, th0, t_max=T_MAX)
    out["small_but_resolvable_outcome"] = r.outcome
    assert r.outcome in ("no_blowup", "blowup_candidate"), r.outcome
    assert _all_validity_fields_finite(r)
    return out


def check_repaired_out_of_domain_kappa_is_rejected():
    """REPAIRED (defect 2, the sharpest one in the battery). `if kappa > 0.0` meant a
    negative, -inf or NaN thermal diffusivity was neither applied nor rejected: the
    integration that ran was the kappa = 0 one, BIT-FOR-BIT, while params["kappa"]
    recorded the value that had been ignored.

    PRE-FIX: kappa in {-0.5, -1e6, -1e-14, nan, -inf} all returned omega_final and
    theta_final bit-identical to the kappa = 0.0 control, with energy_balance_residual =
    2.2188e-07, exactly the control's value -- ratio 1.000. There was NO tell, because
    the module's energy-balance guard is d/dt E_k = int(v*theta) - nu*int(w^2), which
    does not contain kappa and structurally cannot see it. nu was dropped the same way,
    but the same identity DOES contain nu, so nu = -0.5 moved the residual from
    2.2188e-07 to 4.3812e-01 -- a factor 1.9745e+06. The guard caught the nu half by
    accident of the identity's shape and missed the kappa half entirely.

    POST-FIX: both are validated at entry against the admissible domain (finite, >= 0),
    so the half the energy identity could never see is now refused by the same rule as
    the half it could. The bit-identity witness leg 89 used is retained in the CONTROL
    gate below, where kappa = 0.5 must still change the run.
    """
    out = {}
    w0, th0 = _fields()
    for name in ("kappa", "nu"):
        for val in (-0.5, -1e6, -1e-14, np.nan, -np.inf, np.inf):
            msg = _rejects(lambda n=name, v=val: solve_boussinesq(
                w0, th0, t_max=T_MAX, **{n: v}))
            out[f"{name}_{val!r}_rejected"] = 1.0 if msg else 0.0
            assert msg is not None, f"{name}={val!r} still accepted"
            assert name in msg, msg
    # 0.0 is the boundary of the domain and is the inviscid Euler-analog this module
    # exists to run: it must NOT be rejected.
    r = solve_boussinesq(w0, th0, nu=0.0, kappa=0.0, t_max=T_MAX)
    out["nu_kappa_zero_still_runs"] = 1.0
    assert _all_validity_fields_finite(r)
    return out


def check_repaired_conservation_drift_propagates_a_nan_limb():
    """REPAIRED (defect 3). conservation_drift is documented as "max of the two above;
    the logged guard value", but it was built with Python's builtin max, which is
    order-dependent on NaN: max(finite, nan) returns the finite operand.

    PRE-FIX: with a NaN-poisoned theta0 and buoyancy off, theta_final was 100% NaN and
    energy_balance_residual was NaN, yet conservation_drift reported 8.077e-18 -- and the
    identical max() expression inside the loop meant drift_guard=1e-9 NEVER FIRED. A
    caller reading only the logged guard saw a pristine run.

    POST-FIX: every guard limb goes through _guard_max, which propagates NaN
    deliberately, and a non-finite running drift is its own reportable failure
    (outcome "under_resolved", early_exit_reason "nonfinite_drift") rather than a
    comparison that quietly evaluates False.
    """
    out = {}
    w0, th0 = _fields()
    thbad = _poison(th0, (5, 6), np.nan)
    r = solve_boussinesq(w0, thbad, buoyancy=False, t_max=T_MAX, drift_guard=1e-9)
    out["nan_fraction_theta_final"] = float(np.mean(~np.isfinite(r.theta_final)))
    out["conservation_drift_is_nan"] = 1.0 if not np.isfinite(r.conservation_drift) else 0.0
    out["outcome"] = r.outcome
    out["early_exit_reason"] = r.early_exit_reason
    assert out["nan_fraction_theta_final"] == 1.0
    assert not np.isfinite(r.energy_balance_residual), "the energy limb is no longer NaN"
    assert not np.isfinite(r.conservation_drift), \
        f"conservation_drift still hides the NaN limb: {r.conservation_drift!r}"
    assert r.outcome == "under_resolved", r.outcome
    assert r.early_exit_reason == "nonfinite_drift", r.early_exit_reason
    # Without a drift_guard the run is not stopped, but the poisoned limb still reaches
    # the reported field -- it is never absorbed.
    r2 = solve_boussinesq(w0, thbad, buoyancy=False, t_max=T_MAX)
    out["no_guard_conservation_drift_is_nan"] = \
        1.0 if not np.isfinite(r2.conservation_drift) else 0.0
    assert not np.isfinite(r2.conservation_drift), float(r2.conservation_drift)
    # And on a clean run the value is unchanged: _guard_max must agree with builtin max
    # everywhere both are defined, or every banked drift number would move.
    clean = solve_boussinesq(w0, th0, t_max=T_MAX)
    out["clean_conservation_drift"] = float(clean.conservation_drift)
    assert clean.conservation_drift == max(clean.mean_drift,
                                           clean.energy_balance_residual)
    return out


def check_repaired_nonfinite_cfl_factor_is_rejected():
    """REPAIRED (defect 3, the `min` side). dt = min(dt_max, c2*dx/speed, c1/max|w|) was
    built with Python's builtin min, which drops a NaN the same way max does, so a
    non-finite CFL safety factor REMOVED its constraint instead of failing.

    PRE-FIX, on a run where the CFL is binding (5x amplitude, dt_max = 1.0): c1 = nan
    relaxed dt_min from 1.7774e-03 to 9.9324e-03 -- a factor 5.588, cutting 30 steps to
    10 and raising energy_balance_residual 9.67x. c1 = c2 = nan gave a SINGLE step of
    dt = 0.3, a relaxation factor of 168.8 and an energy residual 801.7x the control,
    yet still only 1.9e-03 in absolute terms, i.e. small enough to read as healthy.
    outcome "no_blowup" every time, no exception, every validity field finite.

    POST-FIX: dt_max, c1 and c2 must be finite and strictly positive. The control run is
    still executed and its dt_min still recorded, so the gate keeps a live measurement of
    the timestep the CFL actually chooses.
    """
    out = {}
    w0, th0 = _fields()
    big = 5.0 * w0
    ctrl = solve_boussinesq(big, th0, t_max=T_MAX, dt_max=1.0)
    out["control_dt_min"] = float(ctrl.dt_min)
    out["control_n_timesteps"] = float(ctrl.n_timesteps)
    assert ctrl.dt_min < 1.0, "the CFL is no longer binding; the gate measures nothing"
    for lab, kw in (("c1_nan", dict(c1=np.nan)),
                    ("c1_inf", dict(c1=np.inf)),
                    ("c1_and_c2_nan", dict(c1=np.nan, c2=np.nan)),
                    ("c2_nan", dict(c2=np.nan)),
                    ("c2_inf", dict(c2=np.inf)),
                    ("dt_max_nan", dict(dt_max=np.nan)),
                    ("dt_max_zero", dict(dt_max=0.0)),
                    ("dt_max_negative", dict(dt_max=-1e-3)),
                    ("c1_zero", dict(c1=0.0)),
                    ("c1_negative", dict(c1=-0.05)),
                    ("c2_negative", dict(c2=-0.4))):
        base = dict(t_max=T_MAX, dt_max=1.0)
        base.update(kw)
        msg = _rejects(lambda b=base: solve_boussinesq(big, th0, **b))
        out[f"{lab}_rejected"] = 1.0 if msg else 0.0
        assert msg is not None, f"{lab}: still accepted"
    return out


def check_repaired_degenerate_grid_is_rejected():
    """REPAIRED (defect 4). n = 1 and n = 2 leave the 2/3 dealias mask retaining exactly
    ONE mode -- the (0,0) mean -- so the spectral method has no spatial resolution
    whatsoever.

    PRE-FIX: both returned outcome "no_blowup" over 30 steps with mean_drift = 0.0 and
    energy_balance_residual = 0.0 -- the most reassuring numbers in the whole battery,
    produced by a discretization that cannot represent any dynamics at all.

    POST-FIX: a grid whose mask retains no non-zero wavenumber is rejected. n >= 3
    retains more than the mean mode and must keep running, which is asserted here so the
    repair cannot creep into a resolution floor it was never given authority to impose.
    """
    out = {}
    for n in (1, 2):
        Xn, Yn = grid2d(n)
        wn = np.sin(Xn) * np.sin(Yn) + 0.5
        thn = np.cos(Xn) * np.sin(Yn) + 0.5
        n_modes = int(np.sum(dealias_mask2d(n)))
        out[f"n{n}_retained_modes"] = float(n_modes)
        assert n_modes == 1, (n, n_modes)
        msg = _rejects(lambda w=wn, t=thn: solve_boussinesq(w, t, t_max=T_MAX))
        out[f"n{n}_rejected"] = 1.0 if msg else 0.0
        assert msg is not None, f"n={n}: a one-mode grid still runs"
        assert "mean mode" in msg, msg
    assert int(np.sum(dealias_mask2d(3))) > 1, "n=3 should retain more than the mean mode"
    for n in (3, 4, 5):
        Xn, Yn = grid2d(n)
        r = solve_boussinesq(np.sin(Xn) * np.sin(Yn) + 0.5,
                             np.cos(Xn) * np.sin(Yn) + 0.5, t_max=T_MAX)
        out[f"n{n}_outcome"] = r.outcome
        assert _all_validity_fields_finite(r), n
    return out


def check_repaired_nonfinite_detection_thresholds_are_rejected():
    """REPAIRED (defect 4, secondary family -- detection parameters rather than
    physical-space inputs, so these did not decide leg 89's gate, but they decide what
    conclusion the caller is handed).

    PRE-FIX: amplification_factor = nan/inf made `m >= amplification_factor*m0`
    permanently False, disabling blow-up detection outright. Against a control that DOES
    fire on the identical trajectory -- amplification_factor = 2.0 returns
    "blowup_candidate" at t = 3.140 with max|w| = 2.0016 -- amplification_factor = nan
    ran the same data to t = 6.0 and returned "no_blowup" having reached a peak
    amplification of 4.013. And t_max = nan or negative made `while t < t_max` False at
    once: zero steps, outcome "no_blowup", every guard 0.0, a scientific conclusion from
    a run that never happened.

    POST-FIX: all of t_max, amplification_factor, max_steps, drift_guard and tail_guard
    are validated at entry. The firing control is still run and still asserted, because
    a module that rejected every threshold would otherwise pass this gate.
    """
    out = {}
    w0, th0 = _fields()
    fired = solve_boussinesq(w0, th0, t_max=6.0, amplification_factor=2.0)
    out["control_outcome"] = fired.outcome
    out["control_t_at_trigger"] = float(fired.t_final)
    assert fired.outcome == "blowup_candidate", fired.outcome
    cases = {
        "amp_nan": dict(t_max=6.0, amplification_factor=np.nan),
        "amp_inf": dict(t_max=6.0, amplification_factor=np.inf),
        "amp_negative": dict(t_max=6.0, amplification_factor=-1.0),
        "amp_zero": dict(t_max=6.0, amplification_factor=0.0),
        "t_max_nan": dict(t_max=np.nan),
        "t_max_negative": dict(t_max=-1.0),
        "drift_guard_nan": dict(t_max=T_MAX, drift_guard=np.nan),
        "tail_guard_nan": dict(t_max=T_MAX, tail_guard=np.nan),
        "max_steps_zero": dict(t_max=T_MAX, max_steps=0),
        "max_steps_nan": dict(t_max=T_MAX, max_steps=float("nan")),
    }
    for lab, kw in cases.items():
        msg = _rejects(lambda k=kw: solve_boussinesq(w0, th0, **k))
        out[f"{lab}_rejected"] = 1.0 if msg else 0.0
        assert msg is not None, f"{lab}: still accepted"
    # t_max = 0.0 is a legitimate degenerate REQUEST (return at once), not a malformed
    # one -- leg 89 reclassified it as a control mid-run and it stays legal. Negative
    # drift/tail guards likewise stay legal: they are how the dedicated tests force a
    # guard to fire on the first step.
    r0 = solve_boussinesq(w0, th0, t_max=0.0)
    out["t_max_zero_outcome"] = r0.outcome
    out["t_max_zero_n_timesteps"] = float(r0.n_timesteps)
    assert r0.n_timesteps == 0, r0.n_timesteps
    hot = solve_boussinesq(w0, th0, t_max=1.0, drift_guard=-1.0)
    out["negative_drift_guard_outcome"] = hot.outcome
    assert hot.outcome == "under_resolved", hot.outcome
    assert hot.early_exit_reason is None, hot.early_exit_reason  # exceeded, not non-finite
    return out


# ===========================================================================
# 3. CONTROLS -- the battery can tell right from wrong
# ===========================================================================

def check_control_exact_zero_vorticity_still_raises():
    """The original guard is still armed and still says what it always said. A
    bit-exactly zero omega0 raises ValueError with the documented "identically zero"
    message -- the scale-aware guard added by the repair is layered BEHIND it, not
    substituted for it, so the exact-zero branch keeps its own diagnosis."""
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
    check_repaired_dealias_annihilated_vorticity_is_rejected,
    check_repaired_denormal_vorticity_is_rejected,
    check_repaired_out_of_domain_kappa_is_rejected,
    check_repaired_conservation_drift_propagates_a_nan_limb,
    check_repaired_nonfinite_cfl_factor_is_rejected,
    check_repaired_degenerate_grid_is_rejected,
    check_repaired_nonfinite_detection_thresholds_are_rejected,
    check_control_exact_zero_vorticity_still_raises,
    check_control_in_domain_coefficients_do_change_the_run,
    check_control_dull_but_correct_answers_are_not_failures,
]


def test_soundness_nan_seeded_vorticity_always_diverges():
    check_soundness_nan_seeded_vorticity_always_diverges()


def test_soundness_nan_temperature_reaches_a_field_the_caller_reads():
    check_soundness_nan_temperature_reaches_a_field_the_caller_reads()


def test_repaired_dealias_annihilated_vorticity_is_rejected():
    check_repaired_dealias_annihilated_vorticity_is_rejected()


def test_repaired_denormal_vorticity_is_rejected():
    check_repaired_denormal_vorticity_is_rejected()


def test_repaired_out_of_domain_kappa_is_rejected():
    check_repaired_out_of_domain_kappa_is_rejected()


def test_repaired_conservation_drift_propagates_a_nan_limb():
    check_repaired_conservation_drift_propagates_a_nan_limb()


def test_repaired_nonfinite_cfl_factor_is_rejected():
    check_repaired_nonfinite_cfl_factor_is_rejected()


def test_repaired_degenerate_grid_is_rejected():
    check_repaired_degenerate_grid_is_rejected()


def test_repaired_nonfinite_detection_thresholds_are_rejected():
    check_repaired_nonfinite_detection_thresholds_are_rejected()


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
