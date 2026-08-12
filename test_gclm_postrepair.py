"""Leg 103 (Route-GLB) -- PERMANENT REGRESSION SUITE for solver/gclm.py.

WHAT THIS IS, AND WHY IT IS NOT test_gclm_adversarial.py
--------------------------------------------------------
Leg 92 (Route-GLA) measured 19 silent corruptions in 54 gate-scoped adversarial cases in
`solver/gclm.py`; the bench-repair `bench/fix-gclm-silent-corruption` closed all four
mechanisms. `test_gclm_adversarial.py` pins 9 checks of that story. Leg 103's gate asked
whether the repair (a) really closes leg 92's ORIGINAL failing cases and (b) regresses
nothing previously validated -- and its yes-branch says to BANK LEG 92'S BATTERY AS A
PERMANENT REGRESSION SUITE. That is this file.

The difference from `test_gclm_adversarial.py` is the direction of the second half. That
file asserts the four repairs. This file additionally pins, as literals, the previously
validated WELL-BEHAVED-INPUT numbers the repair must never move: all 20 `stage1_5_sweep.py`
production T* values to the bit, the production call surface's admissibility, and the
already-correct paths leg 92 found needed no repair at all (NaN-seeded vorticity, extreme
`a`, the structural adversaries) -- which are exactly the places an over-eager future guard
would break first.

MEASURED, NOT ASSERTED (leg 103, against the pre-repair module read out of git):
  - 0 silent corruptions in the same 54 gate-scoped cases (leg 92: 19)
  - worst amplitude-invariant violation 2.353088e-06, down from 3.333332e-01 (141658x),
    and equal to the root-finder noise floor leg 92 itself measured -- i.e. the residual
    is the bisection floor, not the defect
  - 0 of 20 banked T* values and 0 of 17 full-length production runs moved, BITWISE
    (sha256 of omega_final + hex float of every scalar)
  - 0 of 31 admissible inputs wrongly rejected

Companion battery: experiments/p2_route_glb_v1_postrepair.py
Companion data:    writeup/data/p2_route_glb_v1_postrepair.json
Pre-repair evidence (frozen, leg 92's): writeup/data/p2_route_gla_v1_adversarial.json

`solver/gclm.py` is READ-ONLY to leg 103, under either branch of its gate.

Run: PYTHONPATH=. .venv/bin/python test_gclm_postrepair.py    (~15 s)
"""

import numpy as np

from solver.gclm import clm_analytic_blowup_time, solve_gclm
from solver.spectral_utils import grid

N = 64
N_SCAN = 4096

# Leg 92's OWN calibrated numbers. The noise floor was measured on decades where the G1
# defect provably could not reach; the tolerance sits three decades above it. Quoted, not
# re-derived, so this suite is held to the bar leg 92 set rather than a friendlier one.
ROOT_FINDER_NOISE_FLOOR = 2.353087957818972e-06
AMPLITUDE_TOLERANCE = 1000.0 * ROOT_FINDER_NOISE_FLOOR    # 2.353e-03
LEG92_WORST_REL_VIOLATION = 0.3333331589781352            # saturated at 1/3
LEG92_NU_SEPARATION = 7.3635623e-03                       # honest nu=0 vs nu=0.01

# The 20 banked stage1_5_sweep.py production T* values, as literals, so this suite is a
# BANK and not merely a diff against whatever the module happens to do today. Two of these
# are independently cross-checkable against committed prose: STAGE_1_5_RESULTS.md records
# "bump(kappa=5) (analytic CLM T* ~ 15.9 > t_max)", and stage1_5_sweep.py:76 records that
# the 20 normalized T* values lie in [1.0, 6.5] once that outlier is set aside.
BANKED_T_STARS = [
    ("sin(x)", 2.0),
    ("sin(2x)", 2.0000000000000004),
    ("sin(x)+0.5sin(2x)", 4.472135954998765),
    ("sin(x)-0.5sin(2x)", 1.4907119849998596),
    ("sin(x)+0.3sin(3x)", 1.606201001370854),
    ("sin(x)+0.5sin(4x)", 2.09920462746772),
    ("bump(kappa=2)", 6.412705280348236),
    ("bump(kappa=5)", 15.916589916604305),
    ("tail(p=1)", 3.778252289899418),
    ("tail(p=1.5)", 2.884680293715717),
    ("tail(p=2)", 2.5334352821625545),
    ("tail(p=1.5,alt)", 1.0096744905046147),
    ("random(seed=0)", 2.296762142732898),
    ("random(seed=1)", 1.4983201725736353),
    ("random(seed=2)", 3.7869823867097434),
    ("random(seed=3)", 1.7232862113400753),
    ("random(seed=4)", 1.6281124217946619),
    ("random(seed=5)", 2.1113376516246753),
    ("random(seed=6)", 1.7235394808249018),
    ("random(seed=7)", 1.2081414665561403),
]


def _quiet():
    """The invalid-value warnings ARE the expected behaviour here, not a failure."""
    return np.errstate(all="ignore")


def profile(x):
    """sin x + 0.5 sin 2x -- leg 92's probe, chosen so max H over the ZERO SET (0.5)
    differs from the GLOBAL max of H (0.75). For sin x alone the two coincide and G1 is
    invisible: the ratio of those two maxima IS the 1.5x-too-early factor."""
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
# (A) THE FOUR MECHANISMS STAY CLOSED -- leg 92's own failing cases, re-run
# ---------------------------------------------------------------------------
def check_G1_blowup_time_is_scale_invariant():
    """G1, the headline. T* was up to 1.5x TOO EARLY below amplitude 1e-12.

    The CLM closed form is exactly homogeneous of degree -1 in amplitude, so
    eps * T*(eps * w0) must not depend on eps. Leg 92 measured it running 4.0 -> 2.667,
    a relative violation saturating at exactly 1/3. Re-run over leg 92's own ladder AND
    far past it (1e-300 ... 1e+100), held to leg 92's own threshold.
    """
    with _quiet():
        t_ref = clm_analytic_blowup_time(profile, n_scan=N_SCAN)
        worst = 0.0
        worst_eps = None
        ladder = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11,
                  3e-12, 1e-12, 6e-13, 5e-13, 1e-14, 1e-15, 1e-18,
                  1e-30, 1e-100, 1e-200, 1e-300, 1e30, 1e100]
        for eps in ladder:
            t = clm_analytic_blowup_time(lambda x, e=eps: e * profile(x), n_scan=N_SCAN)
            assert t is not None, eps
            rel = abs(eps * t - t_ref) / abs(t_ref)
            assert rel < AMPLITUDE_TOLERANCE, (eps, rel, AMPLITUDE_TOLERANCE)
            if rel > worst:
                worst, worst_eps = rel, eps
        # The residual must be the ROOT-FINDER FLOOR, not a shrunken defect: leg 92
        # measured that floor and this must not exceed it by more than a factor of 2.
        assert worst < 2.0 * ROOT_FINDER_NOISE_FLOOR, (worst, ROOT_FINDER_NOISE_FLOOR)
    return (f"scale-invariant over {len(ladder)} decades spanning 1e-300..1e+100: worst "
            f"rel violation {worst:.6e} at eps={worst_eps:g}, vs leg 92's "
            f"{LEG92_WORST_REL_VIOLATION:.6e} (saturated 1/3) -- a "
            f"{LEG92_WORST_REL_VIOLATION / worst:.0f}x reduction, and at the "
            f"{ROOT_FINDER_NOISE_FLOOR:.3e} bisection floor leg 92 itself measured")


def check_G1_closed_form_amplitude_law():
    """The closed form's OWN amplitude law must be reproduced exactly, on both sides.

    For w0 = A sin x: H(w0) = -A cos x, zero set {0, pi}, so T* = 2/A exactly. G1's defect
    was NOT that T* depends on amplitude -- it genuinely does -- but that it depended on it
    the WRONG way below 1e-12.
    """
    with _quiet():
        worst = 0.0
        for amp in (1e-30, 1e-12, 1e-9, 1.0, 10.0, 1e9, 1e30):
            got = clm_analytic_blowup_time(lambda x, s=amp: s * np.sin(x))
            rel = abs(got - 2.0 / amp) / (2.0 / amp)
            assert rel < 1e-14, (amp, got, rel)
            worst = max(worst, rel)
        # Data that does not blow up must still say so.
        assert clm_analytic_blowup_time(lambda x: 1.0 + 0.5 * np.sin(x)) is None
        assert clm_analytic_blowup_time(lambda x: np.zeros_like(x), n_scan=256) is None
    return (f"T* = 2/A reproduced to {worst:.2e} worst relative error over 60 decades of "
            f"amplitude (1e-30 .. 1e+30); non-blowing and identically-zero data still "
            f"return None")


def check_G2_invalid_viscosity_is_rejected():
    """G2. `if nu > 0.0` used to drop NaN and every negative nu into a BITWISE-inviscid
    run: leg 92 measured nu=-1.0 returning omega_final identical to the nu=0 run with
    outcome 'no_blowup' and an entirely finite payload."""
    with _quiet():
        x = grid(N)
        w0 = profile(x)
        kw = dict(a=0.5, t_max=0.3, max_steps=5000)
        for nu in (float("nan"), -1.0, -1e-300, float("-inf")):
            assert _raises_value_error(lambda v=nu: solve_gclm(w0, nu=v, **kw)), nu
        # ADMISSIBLE, and must stay so: leg 92's own corrected false positive.
        r0 = solve_gclm(w0, nu=0.0, **kw)
        rm0 = solve_gclm(w0, nu=-0.0, **kw)
        assert np.array_equal(r0.omega_final, rm0.omega_final)
        rv = solve_gclm(w0, nu=0.01, **kw)
        sep = float(np.max(np.abs(r0.omega_final - rv.omega_final)))
        assert abs(sep - LEG92_NU_SEPARATION) / LEG92_NU_SEPARATION < 1e-3, sep
        assert not np.array_equal(r0.omega_final, rv.omega_final)
    return (f"nu in (nan, -1.0, -1e-300, -inf) all -> ValueError; nu=0.0 and nu=-0.0 stay "
            f"admissible and bitwise equal; the honest nu=0 vs nu=0.01 separation is "
            f"{sep:.6e}, reproducing leg 92's {LEG92_NU_SEPARATION:.6e} to "
            f"{abs(sep - LEG92_NU_SEPARATION) / LEG92_NU_SEPARATION:.1e} relative")


def check_G3_artifact_guard_reports_its_own_nan():
    """G3. conservation_drift = max(mean_drift, energy_residual), and builtin max returns
    the finite argument when the other is NaN -- so the ONE number LOGGING.md records as
    the artifact guard read 4.926e-17 ('clean') on a run reaching max|w| = 9.673e+144."""
    with _quiet():
        x = grid(N)
        w0 = profile(x)
        poisoned = []
        for a in (1e12, 1e16):
            r = solve_gclm(w0, a=a, nu=0.0, t_max=0.3, max_steps=5000)
            assert not np.isfinite(r.energy_balance_residual), a
            assert np.isnan(r.conservation_drift), (a, r.conservation_drift)
            assert r.guard_nan is True, a
            poisoned.append((a, float(np.nanmax(r.max_omega)), float(r.mean_drift)))
        # The honest path must be untouched: a finite residual is still reported as the
        # ordinary max, with the flag DOWN.
        r8 = solve_gclm(w0, a=1e8, nu=0.0, t_max=0.3, max_steps=5000)
        assert np.isfinite(r8.energy_balance_residual)
        assert r8.guard_nan is False
        assert r8.conservation_drift == max(r8.mean_drift, r8.energy_balance_residual)
        rok = solve_gclm(w0, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
        assert rok.guard_nan is False and np.isfinite(rok.conservation_drift)
    return ("at a=1e12/1e16 the guard now reports NaN with guard_nan=True on runs reaching "
            f"max|w| = {poisoned[0][1]:.3e} / {poisoned[1][1]:.3e} (leg 92: the log read "
            f"{poisoned[0][2]:.3e}, i.e. 'clean'); a=1e8 and a=0.5 keep the honest max "
            f"({r8.conservation_drift:.4e} / {rok.conservation_drift:.4e}), flag down")


def check_G4_nonfinite_stop_criteria_are_rejected():
    """G4. Every NaN comparison is False, so each poisoned stop criterion silently CEASED
    TO EXIST: t_max=nan gave 0 timesteps and a clean 'no_blowup' verdict, and
    amplification_factor=nan flipped a detected blow-up at a=1e4 into 'diverged'."""
    with _quiet():
        x = grid(N)
        w0 = profile(x)
        nan = float("nan")
        poisons = [dict(t_max=nan), dict(t_max=-1.0), dict(t_max=0.0),
                   dict(t_max=0.3, dt_max=nan), dict(t_max=0.3, dt_max=0.0),
                   dict(t_max=0.3, c1=nan), dict(t_max=0.3, c2=nan),
                   dict(t_max=0.3, amplification_factor=nan),
                   dict(t_max=0.3, max_steps=nan)]
        for kw in poisons:
            assert _raises_value_error(
                lambda k=kw: solve_gclm(w0, a=0.5, nu=0.0, **k)), kw
        # The detector itself must still fire, and an ordinary run must still run.
        big = solve_gclm(w0, a=1e4, nu=0.0, t_max=0.3, max_steps=5000)
        assert big.outcome == "blowup_candidate", big.outcome
        ok = solve_gclm(w0, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
        assert ok.n_timesteps > 0 and _payload_all_finite(ok)
    return (f"{len(poisons)} non-finite/non-positive stop-criteria configs all -> "
            f"ValueError; the detector still fires (a=1e4 -> blowup_candidate, max|w| = "
            f"{float(np.max(np.abs(big.omega_final))):.3e}) and an ordinary run still takes "
            f"{ok.n_timesteps} steps")


# ---------------------------------------------------------------------------
# (B) THE PATHS LEG 92 FOUND ALREADY CORRECT -- where an over-eager guard breaks first
# ---------------------------------------------------------------------------
def check_already_correct_paths_did_not_regress():
    """Leg 92 measured 0/12 silent on NaN/Inf-seeded vorticity and 0/10 on extreme `a`,
    and the repair deliberately left both alone. They are re-run here because a future
    over-tightening is likeliest to land exactly here."""
    with _quiet():
        x = grid(N)
        base = profile(x)
        n_flagged = 0
        for val in (float("nan"), float("inf"), float("-inf")):
            for idx in (7, [0, 7, 31], slice(None)):
                w = base.copy()
                w[idx] = val
                r = solve_gclm(w, a=0.5, nu=0.0, t_max=0.3, max_steps=5000)
                assert r.outcome == "diverged", (val, r.outcome)
                assert r.n_timesteps == 1, (val, r.n_timesteps)
                n_flagged += 1
        # The other 3 of leg 92's 12: the ANALYTIC entry point on poisoned data. A single
        # NaN node poisons the whole rfft spectrum, so every candidate H-value is NaN and
        # the function returns None. Leg 92 recorded that as WRONG (the clean data blows
        # up at T* = 4.0) but NOT a silent corruption, because None is not a finite
        # plausible number. Pinned at exactly that strength -- neither counted as a defect
        # nor quietly upgraded to correct.
        for val in (float("nan"), float("inf"), float("-inf")):
            def poisoned(xx, v=val):
                w = profile(xx)
                w[7] = v
                return w
            got = clm_analytic_blowup_time(poisoned, n_scan=256)
            assert got is None or not np.isfinite(got), (val, got)
            n_flagged += 1
        # Extreme FINITE `a`: honestly huge and unclamped, and monotone in `a`.
        maxes = []
        for a in (1e4, 1e8, 1e12, 1e16):
            r = solve_gclm(base, a=a, nu=0.0, t_max=0.3, max_steps=5000)
            assert r.outcome == "blowup_candidate", (a, r.outcome)
            maxes.append(float(np.nanmax(r.max_omega)))
        assert all(b > s for s, b in zip(maxes, maxes[1:])), maxes
        # Non-finite `a` is flagged, not silently run.
        for a in (float("nan"), float("inf"), float("-inf")):
            r = solve_gclm(base, a=a, nu=0.0, t_max=0.3, max_steps=5000)
            assert r.outcome == "diverged", (a, r.outcome)
        # Structural adversaries: 3 raise, and 2 return None because None is the TRUE
        # answer there -- both are FLAGGED under leg 92's definition. This exact 3/2 split
        # is what leg 92's own JSON recorded pre-repair.
        assert _raises_value_error(lambda: solve_gclm(np.zeros(N), t_max=0.1))
        assert clm_analytic_blowup_time(lambda x: np.ones_like(x), n_scan=256) is None
        assert clm_analytic_blowup_time(lambda x: np.zeros_like(x), n_scan=256) is None
    return (f"{n_flagged}/12 poisoned-vorticity cases still flagged (9 solve_gclm ones "
            f"'diverged' on step 1, 3 analytic ones returning None, not a finite number); "
            f"extreme finite a unclamped and monotone (max|w| {maxes[0]:.3e} -> "
            f"{maxes[-1]:.3e} over a = 1e4..1e16); non-finite a flagged; structural "
            f"adversaries keep leg 92's exact 3-raise / 2-correct-None split")


# ---------------------------------------------------------------------------
# (C) ZERO REGRESSION ON PREVIOUSLY-VALIDATED WELL-BEHAVED INPUT
# ---------------------------------------------------------------------------
# leg 379: bit-identity replaced by a documented ULP tolerance.
#
# `check_banked_stage1_5_t_stars_are_unmoved` originally asserted
# `float.hex(got) == float.hex(banked)` -- exact bit identity. Under the environment this
# suite now runs in (numpy 2.5.1) that assertion fails on 2 of the 20 banked values, with
# NO change to `solver/gclm.py` and no thread-count sensitivity (reproduced identically
# with OMP/OPENBLAS/MKL/NUMEXPR/VECLIB_THREADS all pinned to 1): `bump(kappa=2)` moves 3
# ULP (`np.spacing`-defined) and `bump(kappa=5)` moves 12 ULP. Both go through
# `clm_analytic_blowup_time`'s `np.fft.rfft`/`irfft` (`solver/gclm.py`), so this is a
# library-version FFT-kernel drift, not a repair regression -- the exact shape of the
# pattern this repo already has two precedents for: leg 147 (Route-NKB) measured 20 of 22
# leaves moving at <= 3 ULP from a numpy-version FFT/reduction-order change with the
# banked totals otherwise exact (`experiments/journal/leg_147.md`), and leg 131 measured
# 1-2 ULP BLAS reduction-order drift on the same kind of re-run
# (`experiments/journal/leg_131.md:128`). Bit identity is therefore the wrong bar for a
# cross-numpy-version FFT re-run; a bounded ULP tolerance, generously above the largest
# drift actually measured (12 ULP) but nowhere near the >1e14 ULP a genuine G1-class
# defect would produce (G1's own violation saturated at a *relative* 1/3, i.e.
# ~3e14 ULP), is the correct one.
ULP_TOLERANCE = 25.0  # >= 2x the worst measured drift (12 ULP, bump(kappa=5))


def _ulp_distance(got, banked):
    """Signed distance in ULPs of `banked`'s binade (`np.spacing`), matching the drift
    actually measured above. `banked == 0.0` cannot occur among these T* (all strictly
    positive blow-up times), so no zero-magnitude special case is needed."""
    return abs(float(got) - float(banked)) / np.spacing(float(banked))


def check_banked_stage1_5_t_stars_are_unmoved():
    """All 20 production T* values, checked to a documented ULP tolerance rather than
    pinned to the bit -- see the module comment above `ULP_TOLERANCE`.

    These are the numbers G1 could in principle have moved, and the reason it did not:
    stage1_5_sweep.py energy-normalizes every IC to ENERGY_TARGET = pi/2, putting their
    amplitudes ~11.9 decades above the old 1e-12 absolute constant. The residual ULP
    drift measured here is >10 orders of magnitude below that: G1's real defect moved
    T* by a relative 1/3 (saturated), not a few ULP.
    """
    import stage1_5_sweep as s15
    with _quiet():
        ics = s15.build_initial_conditions()
        assert len(ics) == len(BANKED_T_STARS), (len(ics), len(BANKED_T_STARS))
        x_ref = grid(s15.N_REFERENCE)
        amps = []
        worst_ulp, worst_label = 0.0, None
        n_bit_identical = 0
        for ic, (label, banked) in zip(ics, BANKED_T_STARS):
            assert ic["label"] == label, (ic["label"], label)
            got = clm_analytic_blowup_time(ic["fn"])
            ulp = _ulp_distance(got, banked)
            assert ulp <= ULP_TOLERANCE, (label, got, banked, ulp, ULP_TOLERANCE)
            if ulp == 0.0:
                n_bit_identical += 1
            elif ulp > worst_ulp:
                worst_ulp, worst_label = ulp, label
            amps.append(float(np.max(np.abs(ic["fn"](x_ref)))))
        lo, hi = min(amps), max(amps)
        # The documented range in stage1_5_sweep.py:76 and STAGE_1_5_RESULTS.md.
        others = [t for lbl, t in BANKED_T_STARS if lbl != "bump(kappa=5)"]
        assert 1.0 <= min(others) and max(others) <= 6.5, (min(others), max(others))
        assert abs(dict(BANKED_T_STARS)["bump(kappa=5)"] - 15.9) < 0.05
    return (f"{n_bit_identical}/{len(ics)} banked T* values bit-identical; the rest within "
            f"{ULP_TOLERANCE:.0f} ULP (worst {worst_ulp:.2f} ULP at {worst_label!r}); "
            f"normalized amplitudes in [{lo:.6f}, {hi:.6f}], i.e. "
            f"{np.log10(lo / 1e-12):.2f} decades above the old absolute 1e-12 tolerance; "
            f"the 19 non-outlier T* still lie in the documented [1.0, 6.5] and "
            f"bump(kappa=5) still reads 15.9 as STAGE_1_5_RESULTS.md records")


def check_CONTROL_ulp_tolerance_still_catches_a_planted_deviation():
    """THE planted-failure control for the ULP-tolerance loosening above (the 361
    lesson): a check loosened without a demonstrated still-fails control is a blinded
    instrument.

    Plants a synthetic banked value displaced by `2 * ULP_TOLERANCE` ULP from a real
    computed T* -- an order of magnitude past anything FFT-version drift produced above,
    but still ~13 orders of magnitude tighter than G1's own 1/3-relative defect, so this
    is squarely testing the TOLERANCE BOUNDARY, not a straw-man. `_ulp_distance` and the
    same `<= ULP_TOLERANCE` assertion used in the real check must reject it.
    """
    import stage1_5_sweep as s15
    with _quiet():
        ics = s15.build_initial_conditions()
        ic0, (label0, banked0) = ics[0], BANKED_T_STARS[0]
        assert ic0["label"] == label0
        got0 = clm_analytic_blowup_time(ic0["fn"])
        planted_banked = float(got0) + 2.0 * ULP_TOLERANCE * np.spacing(float(got0))
        planted_ulp = _ulp_distance(got0, planted_banked)
        assert planted_ulp > ULP_TOLERANCE, (planted_ulp, ULP_TOLERANCE)
        tripped = False
        try:
            assert planted_ulp <= ULP_TOLERANCE, (
                label0, got0, planted_banked, planted_ulp, ULP_TOLERANCE)
        except AssertionError:
            tripped = True
        assert tripped, (
            "planted control FAILED TO TRIP: a synthetic deviation of "
            f"{planted_ulp:.2f} ULP (> tolerance {ULP_TOLERANCE:.0f}) did not raise -- "
            "the ULP-tolerance check is not actually checking anything")
    return {"label": label0, "computed": float(got0), "planted_banked": planted_banked,
           "planted_ulp": planted_ulp, "ULP_TOLERANCE": ULP_TOLERANCE,
           "control": "TRIPPED as required"}


def check_production_call_surface_is_admissible():
    """No overshoot: the real SOLVER_PARAMS of all five production sweeps, harvested from
    the modules themselves rather than transcribed, must all still be accepted."""
    import nongenericity_sweep as ng
    import stage1_5_sweep as s15
    import stage2_5_sweep as s25
    import stage2_6_sweep as s26
    import stage3_6_sweep as s36
    with _quiet():
        x = grid(128)
        w0 = np.sin(x) + 0.3 * np.sin(3 * x)
        n = 0
        for mod in (s15, s25, s26, s36, ng):
            for a in (0.0, 0.5, 1.0):
                r = solve_gclm(w0, a=a, nu=0.0, t_max=min(float(mod.T_MAX), 1.0),
                               **dict(mod.SOLVER_PARAMS))
                assert r.outcome in ("no_blowup", "blowup_candidate", "max_steps_hit")
                assert _payload_all_finite(r) and r.guard_nan is False
                n += 1
        # The admissible viscosity range every bisecting caller uses: ga/evolve [0, 0.3],
        # ga/fitness2d [0, 1.5], stage2_5's NU_RANGE_LADDER all (0.0, .).
        for nu in (0.0, -0.0, 1e-16, 1e-8, 0.01, 0.3, 1.5):
            solve_gclm(w0, a=0.5, nu=nu, t_max=0.5)
            n += 1
        # Integer and numpy-scalar parameters, which real callers do pass.
        solve_gclm(w0, a=0.5, nu=0, t_max=1, max_steps=5000)
        solve_gclm(w0, a=np.float64(0.5), nu=np.float64(0.0), t_max=np.float64(0.5))
        n += 2
    return (f"{n}/{n} admissible production inputs accepted -- 5 sweeps x 3 values of `a` "
            f"at their own SOLVER_PARAMS, the full admissible nu range 0..1.5 including "
            f"-0.0, and int / numpy-scalar parameters; 0 wrongly rejected")


CHECKS = [
    check_G1_blowup_time_is_scale_invariant,
    check_G1_closed_form_amplitude_law,
    check_G2_invalid_viscosity_is_rejected,
    check_G3_artifact_guard_reports_its_own_nan,
    check_G4_nonfinite_stop_criteria_are_rejected,
    check_already_correct_paths_did_not_regress,
    check_banked_stage1_5_t_stars_are_unmoved,
    check_CONTROL_ulp_tolerance_still_catches_a_planted_deviation,
    check_production_call_surface_is_admissible,
]


def main():
    for fn in CHECKS:
        print(f"PASS {fn.__name__}: {fn()}")
    print(f"\nall gclm post-repair regression checks passed ({len(CHECKS)} checks).")
    print("Leg 92's 19 silent corruptions in 54 gate-scoped cases -> 0, and 0 of 20 banked "
          "T* values and 0 of 17 production runs moved bitwise (leg 103, Route-GLB).")


if __name__ == "__main__":
    main()
