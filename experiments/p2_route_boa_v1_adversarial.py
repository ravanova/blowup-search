"""Route-BOA v1 -- an ADVERSARIAL BATTERY against solver/boussinesq.py, the physical-space
2D Boussinesq pseudo-spectral solver, and the audit of what its returned
`BoussinesqResult` actually certifies.

Leg 89. Seventh leg of the adversarial-audit family (after 69/IA on solver/interval.py,
79/PC on the port certification, 80/BHN on the bordered Newton, 83, 85, and 88/GCA on
solver/gclm_family.py), applied to the one physical-space evolution solver whose entire
validation rests on WELL-BEHAVED inputs: capabilities.py's entry for solver/boussinesq.py
advertises "dedicated: test_boussinesq_dedicated.py (17 checks) + test_solver_boussinesq.py",
and leg 89's novelty pass (writeup/novelty/leg_89.md §1) establishes that not one of those
checks ever passes a non-finite value, a degenerate grid size, or an out-of-domain physical
coefficient into solve_boussinesq.

THE GATE, VERBATIM
------------------
"Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
degenerate/zero stream function, extreme grid-stretching), does solver/boussinesq.py ever
silently return a finite, plausible-looking result instead of propagating or flagging the
invalid input?"

WHAT "SILENTLY" MEANS HERE, PRE-COMMITTED IN writeup/novelty/leg_89.md §3 BEFORE THE RUN
-----------------------------------------------------------------------------------------
    SILENT CORRUPTION := the call returns NORMALLY (no exception raised)
      AND every field a caller reads to judge validity -- outcome, conservation_drift,
          mean_drift, energy_balance_residual, the max_omega trajectory -- is FINITE and in
          a PLAUSIBLE range
      AND the run is nevertheless invalid, because either
          (a) the returned state omega_final/theta_final is not all-finite, or
          (b) an invalid parameter was silently DROPPED -- the integration that ran is not
              the one requested -- while `params` records the value that was ignored.

Two readings are deliberately EXCLUDED from deciding the gate, and both are measured and
reported anyway:
  - LOUD FAILURE IS A PASS, whatever its form. A raised ValueError, an outcome of
    "diverged"/"under_resolved"/"max_steps_hit", or a NaN that reaches a field the caller
    reads -- all propagate or flag. This leg does not grade the quality of the flag.
  - A PHYSICALLY DULL-BUT-CORRECT ANSWER IS A PASS. Constant vorticity really does have
    u == 0 and really does sit still; reporting "no_blowup" there is right, not corrupt.

Every "silent" verdict in this file is therefore backed by an explicit WITNESS -- a second,
independent computation that establishes the returned run is not the requested one. For a
dropped parameter the witness is bit-for-bit array equality against the control run with
that parameter set to its neutral value ("both are small" is not accepted). For a wrong
label the witness is the represented initial state recomputed through the module's own
dealias mask.

MAPPING THE GATE'S THIRD CLAUSE
-------------------------------
solver/boussinesq.py is a UNIFORM 2*pi-periodic pseudo-spectral code (grid2d is
2*pi*arange(n)/n) and has no grid-stretching parameter whatsoever. Per novelty pass §2,
fixed before any run, "extreme grid-stretching" is mapped to the nearest thing in kind:
extreme discretization parameters (n at degenerate values; dt_max/c1/c2 at zero, negative
and non-finite) and physical coefficients (nu/kappa) outside their admissible domain.
"Degenerate/zero stream function" is mapped to what produces psi == 0 in this module:
Laplace(psi) = w with inv_Ksq zeroed at the mean mode, so a CONSTANT w, and any w
annihilated by the 2/3 dealias mask, both give psi == 0, u == 0.

DISCIPLINE
----------
Magnitudes, never booleans. Every family reports its case count, how many returned
normally, and the SIZE of the thing that could have gone wrong: the amplification the
false blow-up label was computed from, the ratio between the requested and the executed
coefficient, the energy residual that did or did not move, the fraction of the returned
state that is NaN while the logged guard reads healthy.

MODULE IS READ-ONLY. solver/boussinesq.py is not edited by this leg under any gate
outcome. A silent-corruption finding is escalated, never patched here.

Run: .venv/bin/python experiments/p2_route_boa_v1_adversarial.py
Writes: writeup/data/p2_route_boa_v1_adversarial.json
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.boussinesq import (  # noqa: E402
    dealias_mask2d,
    grid2d,
    solve_boussinesq,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_boa_v1_adversarial.json")

N = 32
T_MAX = 0.3

# Verdict vocabulary. The first three are PASSES of the gate; only SILENT is a failure.
RAISED = "raised"            # an exception -- the loudest possible flag
FLAGGED = "flagged"          # outcome in {diverged, under_resolved, max_steps_hit}
PROPAGATED = "propagated"    # returned normally, but a non-finite reached a validity field
BENIGN = "benign"            # returned normally and the answer is correct
SILENT = "silent"            # returned normally, all validity fields healthy, answer wrong

PASSING = (RAISED, FLAGGED, PROPAGATED, BENIGN)


def fields(w0, th0):
    X, Y = grid2d(N)
    return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)


def _base_fields(n=N):
    X, Y = grid2d(n)
    return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)


def _jsonable(x):
    if isinstance(x, float):
        if np.isnan(x):
            return "nan"
        if np.isinf(x):
            return "inf" if x > 0 else "-inf"
    return x


def run_case(label, family, w0, th0, kwargs, invalid_because, witness=None):
    """Run one case, record every validity field, and classify.

    `witness`, when given, is called as witness(result) -> (is_wrong, detail_dict) and is
    the ONLY thing allowed to turn a normal-looking return into a SILENT verdict.

    NOTE on `n_runtime_warnings`: it is recorded but DECIDES NOTHING, and it must not be
    read as "no warning was emitted". numpy raises its invalid-value RuntimeWarnings from
    C with a once-per-code-location registry that `warnings.simplefilter("always")` does
    not reliably reset, so this counter was measured to return 0 even on a case that does
    emit warnings on a fresh interpreter. It is a LOWER BOUND, kept only for the record.
    The "silently" half of the gate is decided structurally instead -- by whether every
    validity field is finite and plausible -- which needs no warning instrumentation, and
    which for the silent cases found here is unambiguous because those runs perform no
    non-finite arithmetic at all (their returned states are 100% finite).
    """
    rec = {"label": label, "family": family, "invalid_because": invalid_because,
           "kwargs": {k: _jsonable(v) for k, v in kwargs.items()}}
    t0 = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            r = solve_boussinesq(w0, th0, **kwargs)
        except Exception as exc:  # noqa: BLE001 -- classifying the exception IS the point
            rec.update(verdict=RAISED, exception=f"{type(exc).__name__}: {exc}",
                       n_runtime_warnings=len(caught),
                       wall_seconds=time.perf_counter() - t0)
            return rec
        rec["n_runtime_warnings"] = len(caught)
    rec["wall_seconds"] = time.perf_counter() - t0

    nan_w = float(np.mean(~np.isfinite(r.omega_final)))
    nan_th = float(np.mean(~np.isfinite(r.theta_final)))
    traj_finite = bool(np.all(np.isfinite(r.max_omega)))
    validity_finite = bool(
        np.isfinite(r.mean_drift) and np.isfinite(r.energy_balance_residual)
        and np.isfinite(r.conservation_drift) and traj_finite and np.isfinite(r.t_final)
    )
    rec.update(
        outcome=r.outcome,
        n_timesteps=int(r.n_timesteps),
        t_final=_jsonable(float(r.t_final)),
        m0=_jsonable(float(r.max_omega[0])),
        m_final=_jsonable(float(r.max_omega[-1])),
        amplification=_jsonable(float(r.max_omega[-1] / r.max_omega[0])
                                if r.max_omega[0] != 0 else float("inf")),
        mean_drift=_jsonable(float(r.mean_drift)),
        energy_balance_residual=_jsonable(float(r.energy_balance_residual)),
        conservation_drift=_jsonable(float(r.conservation_drift)),
        max_tail_fraction=_jsonable(float(r.max_tail_fraction)),
        nan_fraction_omega_final=nan_w,
        nan_fraction_theta_final=nan_th,
        all_validity_fields_finite=validity_finite,
    )

    # conservation_drift is DOCUMENTED (solver/boussinesq.py:141) as "max of the two
    # above". Measure whether it actually is, since Python's builtin max drops a NaN.
    limbs = (float(r.mean_drift), float(r.energy_balance_residual))
    any_limb_nan = bool(np.any(~np.isfinite(limbs)))
    rec["guard_masks_a_nan_limb"] = bool(
        any_limb_nan and np.isfinite(r.conservation_drift))

    if r.outcome in ("diverged", "under_resolved", "max_steps_hit"):
        rec["verdict"] = FLAGGED
        return rec

    wrong, detail = (False, {}) if witness is None else witness(r)
    rec["witness"] = detail
    if not wrong:
        rec["verdict"] = BENIGN
        return rec
    rec["verdict"] = SILENT if validity_finite else PROPAGATED
    return rec


# ---------------------------------------------------------------------------
# FAMILY A -- degenerate / zero stream function (gate clause 2)
# ---------------------------------------------------------------------------
def family_a():
    """psi == 0 states, and the exact-zero guard's blind spot around them.

    The module raises ValueError("omega0 is identically zero") on max|w| == 0.0 EXACTLY.
    The question this family asks is what happens just next to that test: a vorticity that
    is zero in the represented (post-dealias) subspace but not bit-zero after a round trip
    through fft2/ifft2, and a vorticity that is numerically zero but not mathematically so.
    """
    cases = []
    w0, th0 = _base_fields()
    X, Y = grid2d(N)
    mask = dealias_mask2d(N)

    def represented(w):
        return float(np.max(np.abs(np.fft.ifft2(np.fft.fft2(w) * mask).real)))

    def false_blowup_witness(r):
        """A "blowup_candidate" label whose threshold was set by roundoff is wrong.

        amplification_factor * m0 is the trigger. When m0 is at roundoff level the
        threshold is meaningless: the buoyancy forcing th_x, which is O(1) and entirely
        ordinary, clears it in one step. The witness is the represented initial vorticity
        recomputed independently through the module's own mask.
        """
        wrong = r.outcome == "blowup_candidate" and float(r.max_omega[0]) < 1e-12
        return wrong, {"represented_m0": _jsonable(float(r.max_omega[0])),
                       "trigger_threshold": _jsonable(
                           1e3 * float(r.max_omega[0])),
                       "m_at_trigger": _jsonable(float(r.max_omega[-1])),
                       "note": ("blowup_candidate declared off a roundoff-level m0; "
                                "the growth is ordinary buoyancy spin-up")}

    # A1-A3: vorticity annihilated by the 2/3 dealias mask (cut = n/3 = 10.67 at n=32).
    for kx, ky in ((15, 15), (12, 12), (14, 3)):
        w_kill = np.sin(kx * X) * np.sin(ky * Y)
        cases.append(run_case(
            f"dealias_annihilated_vorticity_k{kx}x{ky}", "A_degenerate_streamfunction",
            w_kill, th0, dict(t_max=T_MAX),
            invalid_because=("omega0 lies entirely above the 2/3 dealias cut: the "
                             "represented vorticity is zero to roundoff "
                             f"(|w|_rep = {represented(w_kill):.4e}), so psi == 0, u == 0"),
            witness=false_blowup_witness))

    # A4: the same field, with the wall symmetry on.
    w_kill = np.sin(15 * X) * np.sin(15 * Y)
    cases.append(run_case(
        "dealias_annihilated_vorticity_houluo", "A_degenerate_streamfunction",
        w_kill, th0, dict(t_max=T_MAX, symmetry="houluo"),
        invalid_because="as above, under the Hou-Luo parity projection",
        witness=false_blowup_witness))

    # A5-A6: numerically-zero vorticity that is not bit-zero.
    for amp in (1e-300, 1e-18):
        cases.append(run_case(
            f"denormal_vorticity_amp{amp:.0e}", "A_degenerate_streamfunction",
            amp * w0, th0, dict(t_max=T_MAX),
            invalid_because=(f"max|omega0| = {amp:.0e} is numerically zero; the "
                             "exact-zero guard tests == 0.0 and does not fire"),
            witness=false_blowup_witness))

    # A7: the control -- an EXACTLY zero omega0 must raise. Establishes the guard works
    # where it is armed, so A1-A6 are a blind spot and not a missing feature.
    cases.append(run_case(
        "CONTROL_exactly_zero_vorticity", "A_degenerate_streamfunction",
        np.zeros((N, N)), th0, dict(t_max=T_MAX),
        invalid_because="max|omega0| == 0.0 exactly -- the documented ValueError branch",
        witness=None))

    # A8: constant vorticity -- psi == 0 too, but the answer is CORRECT. Guards the
    # battery against calling a dull-but-right run a failure.
    cases.append(run_case(
        "CONTROL_constant_vorticity_psi_zero", "A_degenerate_streamfunction",
        np.full((N, N), 2.0), th0, dict(t_max=T_MAX),
        invalid_because=("all energy in the (0,0) mode, inv_Ksq is 0 there, so psi == 0 "
                         "and u == 0 -- but this is genuinely a steady state"),
        witness=None))
    return cases


# ---------------------------------------------------------------------------
# FAMILY B -- NaN/Inf-seeded vorticity (gate clause 1)
# ---------------------------------------------------------------------------
def family_b():
    cases = []
    w0, th0 = _base_fields()

    def poisoned_state_witness(r):
        bad = float(np.mean(~np.isfinite(r.omega_final)))
        return bad > 0.0, {"nan_fraction_omega_final": bad}

    variants = {
        "single_nan": lambda: _poison(w0, (3, 4), np.nan),
        "single_posinf": lambda: _poison(w0, (3, 4), np.inf),
        "single_neginf": lambda: _poison(w0, (3, 4), -np.inf),
        "all_nan": lambda: np.full((N, N), np.nan),
        "corner_nan": lambda: _poison(w0, (0, 0), np.nan),
        "huge_1e308": lambda: _poison(w0, (3, 4), 1e308),
    }
    switches = {
        "full": dict(),
        "nonlinear_off": dict(nonlinear=False),
        "nonlinear_off_buoyancy_off": dict(nonlinear=False, buoyancy=False),
        "houluo": dict(symmetry="houluo"),
        "frozen_u": dict(frozen_u=(0.3, -0.2)),
    }
    for vname, build in variants.items():
        for sname, extra in switches.items():
            kw = dict(t_max=T_MAX, **extra)
            cases.append(run_case(
                f"omega0_{vname}__{sname}", "B_nan_seeded_vorticity",
                build(), th0, kw,
                invalid_because=f"omega0 carries a non-finite value ({vname})",
                witness=poisoned_state_witness))
    return cases


def _poison(f, idx, val):
    g = f.copy()
    g[idx] = val
    return g


# ---------------------------------------------------------------------------
# FAMILY C -- NaN/Inf-seeded temperature
# ---------------------------------------------------------------------------
def family_c():
    """theta0 is the other physical-space input, and it has a decoupling switch.

    With buoyancy=False the vorticity never sees theta, so a NaN-poisoned theta cannot
    reach max_omega. Whether it reaches any field a caller reads is the question.
    """
    cases = []
    w0, th0 = _base_fields()

    def poisoned_state_witness(r):
        bad = float(np.mean(~np.isfinite(r.theta_final)))
        return bad > 0.0, {"nan_fraction_theta_final": bad}

    variants = {"single_nan": _poison(th0, (5, 6), np.nan),
                "single_inf": _poison(th0, (5, 6), np.inf),
                "all_nan": np.full((N, N), np.nan)}
    switches = {
        "full": dict(),
        "buoyancy_off": dict(buoyancy=False),
        "buoyancy_off_nonlinear_off": dict(buoyancy=False, nonlinear=False),
        "buoyancy_off_drift_guard_1e-9": dict(buoyancy=False, drift_guard=1e-9),
        "buoyancy_off_tail_guard_1e-6": dict(buoyancy=False, tail_guard=1e-6),
    }
    for vname, th_bad in variants.items():
        for sname, extra in switches.items():
            cases.append(run_case(
                f"theta0_{vname}__{sname}", "C_nan_seeded_temperature",
                w0, th_bad, dict(t_max=T_MAX, **extra),
                invalid_because=f"theta0 carries a non-finite value ({vname})",
                witness=poisoned_state_witness))
    return cases


# ---------------------------------------------------------------------------
# FAMILY D -- out-of-domain physical coefficients (gate clause 3, coefficient half)
# ---------------------------------------------------------------------------
def family_d():
    """nu and kappa outside [0, inf).

    The evolution applies them behind `if nu > 0.0` / `if kappa > 0.0`, so a negative or
    NaN coefficient is not applied. The witness is bit-for-bit equality of the returned
    arrays against the neutral control (coefficient = 0.0): identical arrays prove the
    integration that ran is the coefficient-free one, i.e. the requested integration never
    happened, while params records the requested value.
    """
    cases = []
    w0, th0 = _base_fields()
    ctrl = solve_boussinesq(w0, th0, t_max=T_MAX)
    ctrl_w, ctrl_th = ctrl.omega_final.copy(), ctrl.theta_final.copy()
    ctrl_en = float(ctrl.energy_balance_residual)

    def dropped_witness(name):
        def w(r):
            same_w = bool(np.array_equal(r.omega_final, ctrl_w))
            same_th = bool(np.array_equal(r.theta_final, ctrl_th))
            en = float(r.energy_balance_residual)
            detail = {
                "bit_identical_omega_final_to_zero_coefficient_run": same_w,
                "bit_identical_theta_final_to_zero_coefficient_run": same_th,
                "requested_coefficient": _jsonable(float(r.params[name])),
                "executed_coefficient": 0.0,
                "energy_residual": _jsonable(en),
                "energy_residual_of_control": ctrl_en,
                "energy_residual_ratio_to_control": _jsonable(
                    en / ctrl_en if np.isfinite(en) else float("nan")),
            }
            return (same_w and same_th), detail
        return w

    for name in ("nu", "kappa"):
        for val, why in ((-0.5, "negative: anti-diffusion, ill-posed"),
                         (-1e6, "hugely negative"),
                         (-1e-14, "negative at roundoff scale"),
                         (np.nan, "NaN"),
                         (-np.inf, "-inf")):
            cases.append(run_case(
                f"{name}_{val!r}", "D_out_of_domain_coefficient",
                w0, th0, {name: val, "t_max": T_MAX},
                invalid_because=f"{name} = {val!r} is outside [0, inf) -- {why}",
                witness=dropped_witness(name)))
    # Controls: the coefficient in-domain must NOT be dropped.
    for name in ("nu", "kappa"):
        cases.append(run_case(
            f"CONTROL_{name}_0.5_in_domain", "D_out_of_domain_coefficient",
            w0, th0, {name: 0.5, "t_max": T_MAX},
            invalid_because="in-domain -- must change the run",
            witness=dropped_witness(name)))
    cases.append(run_case(
        "nu_posinf", "D_out_of_domain_coefficient", w0, th0,
        dict(nu=np.inf, t_max=T_MAX),
        invalid_because="nu = +inf: exp(-inf*0*dt) at the mean mode is nan",
        witness=dropped_witness("nu")))
    return cases


# ---------------------------------------------------------------------------
# FAMILY E -- degenerate grid and discretization parameters (gate clause 3, grid half)
# ---------------------------------------------------------------------------
def family_e():
    cases = []
    w0, th0 = _base_fields()

    # E1: degenerate grid sizes. At n <= 2 the 2/3 mask (cut = n/3) retains only the mean
    # mode, so the "spectral method" has no spatial resolution at all.
    for n in (1, 2, 3, 4, 5):
        Xn, Yn = grid2d(n)
        wn = np.sin(Xn) * np.sin(Yn) + 0.5   # + 0.5 so max|w| != 0 at n = 1
        thn = np.cos(Xn) * np.sin(Yn) + 0.5
        cut = n / 3.0
        n_modes = int(np.sum(dealias_mask2d(n)))

        def grid_witness(r, n=n, n_modes=n_modes, cut=cut):
            # Wrong iff the run reports a normal outcome from a grid that retains no
            # spatial structure whatsoever (mean mode only).
            return n_modes <= 1, {"retained_modes_after_dealias": n_modes,
                                  "dealias_cut": cut,
                                  "note": ("a grid whose mask retains only the (0,0) mode "
                                           "cannot represent any dynamics")}
        cases.append(run_case(
            f"grid_n{n}", "E_degenerate_discretization", wn, thn, dict(t_max=T_MAX),
            invalid_because=(f"n = {n}: the 2/3 mask retains {n_modes} mode(s); "
                             "no spatial resolution"),
            witness=grid_witness))

    # E2: the CFL safety factors made non-finite. Python's builtin min drops a NaN, so a
    # NaN factor silently REMOVES its limb of the timestep constraint instead of failing.
    # Measured on a run where the CFL is actually binding (dt_max = 1.0 >> CFL dt).
    big = 5.0 * w0
    ref = solve_boussinesq(big, th0, t_max=T_MAX, dt_max=1.0)
    ref_dt, ref_steps = float(ref.dt_min), int(ref.n_timesteps)
    ref_en = float(ref.energy_balance_residual)

    def cfl_witness(r):
        dt = float(r.dt_min)
        en = float(r.energy_balance_residual)
        relaxed = dt > ref_dt * (1.0 + 1e-9)
        return relaxed, {"dt_min": _jsonable(dt), "dt_min_of_control": ref_dt,
                         "dt_relaxation_factor": _jsonable(dt / ref_dt),
                         "n_timesteps": int(r.n_timesteps),
                         "n_timesteps_of_control": ref_steps,
                         "energy_residual": _jsonable(en),
                         "energy_residual_of_control": ref_en,
                         "energy_residual_ratio": _jsonable(
                             en / ref_en if np.isfinite(en) else float("nan")),
                         "note": ("the CFL limb was dropped, not applied; the step grew "
                                  "and no field says so")}

    for lab, kw in (("c1_nan", dict(c1=np.nan)),
                    ("c2_nan", dict(c2=np.nan)),
                    ("c1_and_c2_nan", dict(c1=np.nan, c2=np.nan)),
                    ("c1_inf", dict(c1=np.inf)),
                    ("c2_inf", dict(c2=np.inf))):
        cases.append(run_case(
            f"cfl_{lab}", "E_degenerate_discretization", big, th0,
            dict(t_max=T_MAX, dt_max=1.0, **kw),
            invalid_because=f"CFL safety factor non-finite ({lab})",
            witness=cfl_witness))

    # E3: timestep parameters at zero / negative / NaN.
    for lab, kw in (("dt_max_zero", dict(dt_max=0.0)),
                    ("dt_max_negative", dict(dt_max=-1e-3)),
                    ("dt_max_nan", dict(dt_max=np.nan)),
                    ("c1_zero", dict(c1=0.0)),
                    ("c1_negative", dict(c1=-0.05)),
                    ("c2_negative", dict(c2=-0.4))):
        cases.append(run_case(
            f"step_{lab}", "E_degenerate_discretization", w0, th0,
            dict(t_max=T_MAX, max_steps=200, **kw),
            invalid_because=f"timestep parameter out of domain ({lab})",
            witness=lambda r: (False, {"note": "classified by outcome alone"})))
    return cases


# ---------------------------------------------------------------------------
# FAMILY F -- detection thresholds made non-finite (SECONDARY: reported, not gate-deciding)
# ---------------------------------------------------------------------------
def family_f():
    """t_max, amplification_factor and the two guards, made non-finite.

    These are DETECTION parameters, not physical-space inputs, so per the novelty pass's
    §2 mapping they are outside the gate's three clauses and are reported separately. They
    are measured because they decide what conclusion the caller is handed.
    """
    cases = []
    w0, th0 = _base_fields()

    # F1: t_max non-finite/negative -> `while t < t_max` is False at once.
    # t_max = 0.0 is included as a CONTROL, not as a failure: asking for zero integration
    # time is a legitimate degenerate request and returning at once is the right answer.
    # Only the malformed values (NaN, negative) are graded.
    def t_max_witness(r):
        return (r.n_timesteps == 0 and r.outcome == "no_blowup"), {
            "n_timesteps": int(r.n_timesteps),
            "note": ("outcome 'no_blowup' is a scientific conclusion returned from a "
                     "zero-step run")}

    for lab, tv in (("nan", np.nan), ("negative", -1.0)):
        cases.append(run_case(
            f"t_max_{lab}", "F_detection_thresholds", w0, th0, dict(t_max=tv),
            invalid_because=f"t_max = {tv!r}: no step can be taken",
            witness=t_max_witness))
    cases.append(run_case(
        "CONTROL_t_max_zero", "F_detection_thresholds", w0, th0, dict(t_max=0.0),
        invalid_because="t_max = 0.0 is a legitimate degenerate request, not malformed",
        witness=None))

    # F2: amplification_factor non-finite -> `m >= amplification_factor*m0` never True.
    # Measured against a control that DOES fire, so the disabling is demonstrated, not
    # argued: same initial data, same t_max, only the threshold differs.
    fired = solve_boussinesq(w0, th0, t_max=6.0, amplification_factor=2.0)
    fired_t, fired_m = float(fired.t_final), float(fired.max_omega[-1])

    def detector_witness(r):
        peak = float(np.max(r.max_omega))
        ratio = peak / float(r.max_omega[0])
        return (r.outcome == "no_blowup" and ratio >= 2.0), {
            "control_amplification_factor": 2.0,
            "control_outcome": fired.outcome,
            "control_t_at_trigger": fired_t,
            "control_max_omega_at_trigger": fired_m,
            "peak_amplification_reached": _jsonable(ratio),
            "note": ("the same trajectory that trips the control's threshold is reported "
                     "no_blowup when the threshold is non-finite")}

    for lab, av in (("nan", np.nan), ("inf", np.inf), ("negative", -1.0)):
        cases.append(run_case(
            f"amplification_factor_{lab}", "F_detection_thresholds", w0, th0,
            dict(t_max=6.0, amplification_factor=av),
            invalid_because=f"amplification_factor = {av!r} disables blow-up detection",
            witness=detector_witness))

    # F3: the guards themselves made NaN -- every comparison is False, so they never fire.
    for lab, kw in (("drift_guard_nan", dict(drift_guard=np.nan)),
                    ("tail_guard_nan", dict(tail_guard=np.nan))):
        cases.append(run_case(
            f"guard_{lab}", "F_detection_thresholds", w0, th0, dict(t_max=T_MAX, **kw),
            invalid_because=f"{lab}: every `> guard` comparison is False",
            witness=lambda r: (False, {"note": "guard never fires; no wrongness witness "
                                               "on well-formed data -- reported only"})))
    return cases


def main():
    t_start = time.perf_counter()
    cases = []
    for fn in (family_a, family_b, family_c, family_d, family_e, family_f):
        cases.extend(fn())

    families = {}
    for c in cases:
        f = families.setdefault(c["family"], {"n_cases": 0, "verdicts": {},
                                              "silent_labels": []})
        f["n_cases"] += 1
        f["verdicts"][c["verdict"]] = f["verdicts"].get(c["verdict"], 0) + 1
        if c["verdict"] == SILENT:
            f["silent_labels"].append(c["label"])

    gate_families = ["A_degenerate_streamfunction", "B_nan_seeded_vorticity",
                     "C_nan_seeded_temperature", "D_out_of_domain_coefficient",
                     "E_degenerate_discretization"]
    n_silent_gate = sum(1 for c in cases
                        if c["verdict"] == SILENT and c["family"] in gate_families)
    n_silent_secondary = sum(1 for c in cases
                             if c["verdict"] == SILENT and c["family"] not in gate_families)
    n_masked = sum(1 for c in cases if c.get("guard_masks_a_nan_limb"))

    payload = {
        "leg": 89,
        "route": "BOA",
        "module_under_audit": "solver/boussinesq.py",
        "module_edited": False,
        "gate_verbatim": (
            "Under an adversarial battery of malformed physical-space inputs (NaN-seeded "
            "vorticity, degenerate/zero stream function, extreme grid-stretching), does "
            "solver/boussinesq.py ever silently return a finite, plausible-looking result "
            "instead of propagating or flagging the invalid input?"),
        "silent_corruption_definition": (
            "returns normally AND outcome/conservation_drift/mean_drift/"
            "energy_balance_residual/max_omega are all finite and plausible AND the run is "
            "invalid, because the returned state is non-finite or an invalid parameter was "
            "silently dropped while params records it. Pre-committed in "
            "writeup/novelty/leg_89.md section 3 before the run."),
        "n_runtime_warnings_caveat": (
            "per-case n_runtime_warnings is a LOWER BOUND and decides nothing: numpy's "
            "C-level once-per-location warning registry is not reliably reset by "
            "simplefilter('always'), measured to report 0 on a case that does warn on a "
            "fresh interpreter. The gate's 'silently' clause is decided structurally, on "
            "whether every validity field is finite and plausible."),
        "gate_answer": "YES" if n_silent_gate > 0 else "NO",
        "n_cases": len(cases),
        "n_silent_gate_deciding": n_silent_gate,
        "n_silent_secondary": n_silent_secondary,
        "n_cases_where_conservation_drift_masks_a_nan_limb": n_masked,
        "gate_deciding_families": gate_families,
        "families": families,
        "cases": cases,
        "wall_seconds": time.perf_counter() - t_start,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)

    print(f"cases: {len(cases)}   wall: {payload['wall_seconds']:.1f}s")
    for fname, f in families.items():
        print(f"  {fname:32s} n={f['n_cases']:3d}  {f['verdicts']}")
        for lab in f["silent_labels"]:
            print(f"      SILENT: {lab}")
    print(f"conservation_drift masks a NaN limb in {n_masked} case(s)")
    print(f"GATE ANSWER: {payload['gate_answer']}  "
          f"({n_silent_gate} gate-deciding silent, {n_silent_secondary} secondary)")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
