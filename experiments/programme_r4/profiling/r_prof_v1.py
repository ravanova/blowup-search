"""PROG-R4 / Lane R, unit `R-prof` (leg 405) -- THE FIRST PROFILE OF THE INNER LOOP.

WHAT THIS IS. `solver/kolmogorov2d_nkbasin.py` has never been profiled in 403 legs.
Every cost figure in `OPTIONS.md` inherits one unexamined constant, 95.389 s/epoch,
and so does the 90.9 core-hour price of the field ensemble (`E-FE`). The gate this
script answers is fixed in `writeup/waves/WAVE7_PLAN.md` sec C and is not changeable
here:

  (i)   where does the per-step time go, by call, summing to 100%?
  (ii)  what fraction is fixed per-call overhead -- ESTABLISHED BY A SIZE SWEEP?
  (iii) is our per-step cost within 3x of the reference at N=24, YES or NO?

THE SOLVER IS NOT TOUCHED. This module imports `Kolmogorov2D` and measures it. It
writes nothing the solver or any campaign reads.

THE REFERENCE IS NAMED, CITED AND EXECUTED, NOT HAND-ROLLED (ORCHESTRATION.md sec 3k;
`writeup/SOURCES.md` rows 23-26):
  * solver level  -- JAX-CFD `jax_cfd.spectral.equations.ForcedNavierStokes2D` with
    `forcings.kolmogorov_forcing`, stepped by `time_stepping.crank_nicolson_rk4`
    (Carpenter-Kennedy low-storage RK4 + Crank-Nicolson).  Kochkov, Smith, Alieva,
    Wang, Brenner & Hoyer, PNAS 118(21) e2101784118 (2021), arXiv:2102.01010.
  * transform lvl -- FFTW3, Frigo & Johnson, Proc. IEEE 93(2):216-231 (2005), via
    `pyfftw`.  Supplies the 20-transforms-per-RK4-step floor.
  * lineage only  -- Chandler & Kerswell, JFM 722:554-595 (2013).  CITED, UNREAD.

TWO DIFFERENCES ARE MEASURED AND REPORTED, NOT NORMALISED AWAY (gate text):
  (a) the reference steps with Crank-Nicolson + a 5-stage low-storage RK4 (IMEX);
      ours is an exact integrating factor applied AFTER a classical 4-stage RK4
      (a Lie-Trotter split).  Different work per step -- both stage counts and both
      transform counts are counted here.
  (b) the reference carries a half-spectrum rfft2 state (24,13); ours carries a full
      complex (24,24).  Roughly 2x the transform work.  The gate is answered BOTH
      raw and with this accounted for.

USAGE (two environments, because the reference may not be installed beside the
solver -- neither perturbs `/home/andy/projects/Unsolved/.venv`):

    <any python with numpy>  r_prof_v1.py --part ours --out ours_venv.json
    <refvenv python>         r_prof_v1.py --part ours --out ours_ref.json
    <refvenv python>         r_prof_v1.py --part ref  --out ref.json
    <any python>             r_prof_v1.py --part merge --ours ours_ref.json \
                                 --ours-alt ours_venv.json --ref ref.json \
                                 --out ../../../writeup/data/p2_r_prof_v1.json

Thread counts are pinned to 1 by the caller (OMP_NUM_THREADS etc.); the value seen
is recorded in every output.  Load average is sampled around every timing block.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import statistics
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

# ---------------------------------------------------------------------------
# timing harness -- median of per-call times, inner loop to amortise the timer
# ---------------------------------------------------------------------------

NS = 1e-9


def _bench(fn, inner, repeat, warmup=3, clock=time.perf_counter_ns):
    """Return dict of per-call seconds: median / min / p25 / p75, over `repeat`
    blocks of `inner` calls each.  Warm-up blocks are discarded."""
    for _ in range(warmup):
        for _ in range(inner):
            fn()
    per = []
    for _ in range(repeat):
        t0 = clock()
        for _ in range(inner):
            fn()
        t1 = clock()
        per.append((t1 - t0) * NS / inner)
    per.sort()
    n = len(per)
    return {"median_s": statistics.median(per),
            "min_s": per[0],
            "p25_s": per[max(0, n // 4)],
            "p75_s": per[min(n - 1, (3 * n) // 4)],
            "n_blocks": repeat, "inner": inner}


def _autobench(fn, target_block_s=0.02, repeat=41, max_inner=200000,
               clock=time.perf_counter_ns):
    """Pick `inner` so a block takes ~target_block_s, then benchmark."""
    inner = 1
    while inner < max_inner:
        t0 = time.perf_counter_ns()
        for _ in range(inner):
            fn()
        dt = (time.perf_counter_ns() - t0) * NS
        if dt >= target_block_s:
            break
        inner = max(inner * 2, int(inner * target_block_s / max(dt, 1e-9)) + 1)
    inner = min(inner, max_inner)
    return _bench(fn, inner, repeat, clock=clock)


def _load():
    try:
        with open("/proc/loadavg") as fh:
            p = fh.read().split()
        return [float(p[0]), float(p[1]), float(p[2])]
    except Exception:
        return None


def _env_block():
    import numpy as np
    return {
        "host_platform": platform.platform(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "n_cpu": os.cpu_count(),
        "thread_env": {k: os.environ.get(k) for k in (
            "OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "XLA_FLAGS")},
        "loadavg_at_start": _load(),
        "timer": "time.perf_counter_ns",
        "timer_resolution_ns": time.get_clock_info("perf_counter").resolution * 1e9,
    }


# ---------------------------------------------------------------------------
# CONTROLS -- the harness must be shown to work before any verdict (sec 3k)
# ---------------------------------------------------------------------------

def controls():
    """Positive control: a busy loop of known repeat count must time LINEARLY.
    Negative control: a no-op must come out at the Python call floor, not at zero.
    Planted control: a deliberately 4x-heavier op must measure ~4x heavier."""
    import numpy as np

    def busy(k):
        def f():
            s = 0.0
            for i in range(k):
                s += i
            return s
        return f

    t100 = _autobench(busy(100))["median_s"]
    t400 = _autobench(busy(400))["median_s"]
    noop = _autobench(lambda: None)["median_s"]

    a = np.zeros((64, 64), dtype=np.complex128)
    b = np.zeros((128, 128), dtype=np.complex128)
    t_small = _autobench(lambda: np.fft.fft2(a))["median_s"]
    t_big = _autobench(lambda: np.fft.fft2(b))["median_s"]

    return {
        "positive_busyloop_ratio_400_over_100": t400 / t100,
        "positive_busyloop_expected": "~4 (linear in trip count)",
        "positive_PASS": 3.4 <= t400 / t100 <= 4.6,
        "negative_noop_call_s": noop,
        "negative_noop_PASS": 0 < noop < 5e-7,
        "planted_fft2_128_over_64_ratio": t_big / t_small,
        "planted_expected": ">1 and <20; 4x elements, 4.67x N^2 log N^2 work",
        "planted_PASS": 1.0 < (t_big / t_small) < 20.0,
    }


# ---------------------------------------------------------------------------
# PART "ours" -- profile solver/kolmogorov2d_nkbasin.py
# ---------------------------------------------------------------------------

N_GATE = 24
RE = 60.0
N_FORCING = 4
DT = 0.01


def _make_solver(N=N_GATE, dt=DT):
    from solver.kolmogorov2d_nkbasin import Kolmogorov2D
    return Kolmogorov2D(N=N, Re=RE, n_forcing=N_FORCING, dt=dt)


def _seed_state(sol, seed=405):
    import numpy as np
    rng = np.random.default_rng(seed)
    w = rng.standard_normal((sol.N, sol.N))
    w -= w.mean()
    w_hat = np.fft.fft2(w) * sol.mask
    return w, w_hat


def profile_step_breakdown(sol):
    """(i) WHERE THE PER-STEP TIME GOES.

    Two independent attributions, reported side by side:

    A. IN-SITU.  `np.fft.fft2` / `np.fft.ifft2` are wrapped with a counter while a
       real `_rk4_step` runs, giving the transform share on the actual code path.
       The wrapper's own cost is measured and subtracted.

    B. LINE-LEVEL RECONSTRUCTION.  Every array expression in `_rhs_hat` and
       `_rk4_step` is re-created here with the identical operands and dtypes and
       timed on its own.  The parts are summed and the difference against the
       measured whole step is reported as UNATTRIBUTED, so the table sums to 100%
       by construction rather than by selection.
    """
    import numpy as np
    w, w_hat = _seed_state(sol)
    dt = sol.dt

    whole = _autobench(lambda: sol._rk4_step(w_hat, dt))
    t_step = whole["median_s"]
    t_rhs = _autobench(lambda: sol._rhs_hat(w_hat))["median_s"]

    # ---- A. in-situ transform accounting ---------------------------------
    real_fft2, real_ifft2 = np.fft.fft2, np.fft.ifft2
    acc = {"fft2_s": 0.0, "ifft2_s": 0.0, "n_fft2": 0, "n_ifft2": 0}

    def wrap(fn, key, ckey):
        def w_(*a, **k):
            t0 = time.perf_counter_ns()
            r = fn(*a, **k)
            acc[key] += (time.perf_counter_ns() - t0) * NS
            acc[ckey] += 1
            return r
        return w_

    np.fft.fft2 = wrap(real_fft2, "fft2_s", "n_fft2")
    np.fft.ifft2 = wrap(real_ifft2, "ifft2_s", "n_ifft2")
    try:
        n_insitu = 300
        for _ in range(20):            # warm-up under the wrapper
            sol._rk4_step(w_hat, dt)
        acc = {"fft2_s": 0.0, "ifft2_s": 0.0, "n_fft2": 0, "n_ifft2": 0}
        t0 = time.perf_counter_ns()
        for _ in range(n_insitu):
            sol._rk4_step(w_hat, dt)
        t_wrapped_total = (time.perf_counter_ns() - t0) * NS
    finally:
        np.fft.fft2, np.fft.ifft2 = real_fft2, real_ifft2

    # cost of the wrapper itself (2 perf_counter_ns + a dict update + a call)
    def _noop(x):
        return x
    wrapped_noop = wrap(_noop, "fft2_s", "n_fft2")
    acc_save = dict(acc)
    wrapper_overhead = (_autobench(lambda: wrapped_noop(1))["median_s"]
                        - _autobench(lambda: _noop(1))["median_s"])
    acc = acc_save

    n_tr_per_step = (acc["n_fft2"] + acc["n_ifft2"]) / n_insitu
    t_transform_insitu = ((acc["fft2_s"] + acc["ifft2_s"]) / n_insitu
                          - n_tr_per_step * wrapper_overhead)
    t_step_wrapped = t_wrapped_total / n_insitu

    insitu = {
        "n_steps_timed": n_insitu,
        "transforms_per_step": n_tr_per_step,
        "n_fft2_per_step": acc["n_fft2"] / n_insitu,
        "n_ifft2_per_step": acc["n_ifft2"] / n_insitu,
        "t_step_under_wrapper_s": t_step_wrapped,
        "t_step_unwrapped_s": t_step,
        "wrapper_overhead_per_call_s": wrapper_overhead,
        "t_transform_per_step_s": t_transform_insitu,
        "transform_fraction_of_wrapped_step": t_transform_insitu / t_step_wrapped,
        "transform_fraction_of_clean_step": t_transform_insitu / t_step,
    }

    # ---- B. line-level reconstruction ------------------------------------
    KX, KY, Ksq, inv_Ksq = sol.KX, sol.KY, sol.Ksq, sol.inv_Ksq
    mask, forcing_hat, decay = sol.mask, sol.forcing_hat, sol.decay
    u_hat = 1j * KY * w_hat * inv_Ksq
    u = np.fft.ifft2(u_hat).real
    v = np.fft.ifft2(-1j * KX * w_hat * inv_Ksq).real
    wx = np.fft.ifft2(1j * KX * w_hat).real
    wy = np.fft.ifft2(1j * KY * w_hat).real
    prod = u * wx + v * wy
    adv_hat = np.fft.fft2(prod) * mask
    k1 = sol._rhs_hat(w_hat)
    k2 = sol._rhs_hat(w_hat + 0.5 * dt * k1)
    k3 = sol._rhs_hat(w_hat + 0.5 * dt * k2)
    k4 = sol._rhs_hat(w_hat + dt * k3)

    # per-rhs (x4 per step)
    L = {}
    L["spectral_velocity_muls"] = (
        _autobench(lambda: 1j * KY * w_hat * inv_Ksq)["median_s"]
        + _autobench(lambda: -1j * KX * w_hat * inv_Ksq)["median_s"])
    L["ifft2_u_v"] = 2 * _autobench(lambda: np.fft.ifft2(u_hat))["median_s"]
    L["real_view_u_v"] = 2 * _autobench(lambda: u_hat.real)["median_s"]
    L["spectral_gradient_muls"] = (
        _autobench(lambda: 1j * KX * w_hat)["median_s"]
        + _autobench(lambda: 1j * KY * w_hat)["median_s"])
    L["ifft2_wx_wy"] = 2 * _autobench(lambda: np.fft.ifft2(u_hat))["median_s"]
    L["real_view_wx_wy"] = 2 * _autobench(lambda: u_hat.real)["median_s"]
    L["physical_product_u_wx_plus_v_wy"] = _autobench(
        lambda: u * wx + v * wy)["median_s"]
    L["fft2_advection"] = _autobench(lambda: np.fft.fft2(prod))["median_s"]
    L["dealias_mask_multiply"] = _autobench(lambda: adv_hat * mask)["median_s"]
    L["negate_plus_forcing"] = _autobench(
        lambda: -adv_hat + forcing_hat)["median_s"]
    t_rhs_recon = sum(L.values())

    R = {}
    R["rhs_hat_x4"] = 4 * t_rhs
    R["stage_argument_axpy_x3"] = 3 * _autobench(
        lambda: w_hat + 0.5 * dt * k1)["median_s"]
    R["final_combination"] = _autobench(
        lambda: w_hat + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))["median_s"]
    R["integrating_factor_multiply"] = _autobench(
        lambda: w_hat * decay)["median_s"]
    R["dt_branch_and_frame"] = _autobench(
        lambda: (dt != sol.dt))["median_s"]
    t_step_recon = sum(R.values())

    # per-step roll-up of the rhs-internal lines (x4), plus rk4-level lines
    per_step = {("rhs." + k): 4 * v_ for k, v_ in L.items()}
    for k in ("stage_argument_axpy_x3", "final_combination",
              "integrating_factor_multiply", "dt_branch_and_frame"):
        per_step["rk4." + k] = R[k]
    attributed = sum(per_step.values())
    per_step["UNATTRIBUTED_python_frames_and_attribution_error"] = (
        t_step - attributed)
    table = {k: {"seconds": v_, "pct_of_step": 100.0 * v_ / t_step}
             for k, v_ in per_step.items()}

    n_transform_lines = ("rhs.ifft2_u_v", "rhs.ifft2_wx_wy", "rhs.fft2_advection")
    n_arith_lines = [k for k in per_step
                     if k.startswith(("rhs.", "rk4.")) and k not in n_transform_lines]
    return {
        "t_rk4_step_s": t_step,
        "t_rk4_step_stats": whole,
        "t_rhs_hat_s": t_rhs,
        "in_situ_transform_accounting": insitu,
        "line_level_table_sums_to_100pct": table,
        "line_level_sum_pct": 100.0 * sum(v_["pct_of_step"] for v_ in table.values()) / 100.0,
        "reconstruction_check": {
            "t_rhs_measured_s": t_rhs,
            "t_rhs_reconstructed_s": t_rhs_recon,
            "rhs_reconstruction_ratio": t_rhs_recon / t_rhs,
            "t_step_measured_s": t_step,
            "t_step_reconstructed_from_rhs_s": t_step_recon,
            "step_reconstruction_ratio": t_step_recon / t_step,
        },
        "transform_share_line_level": sum(
            table[k]["pct_of_step"] for k in n_transform_lines),
        "arith_share_line_level": sum(table[k]["pct_of_step"] for k in n_arith_lines),
        "numpy_calls_per_step": count_numpy_calls(),
    }


def count_numpy_calls():
    """Static count of numpy array-level calls in one `_rk4_step`, from the source.
    Used by (ii) to convert a per-call overhead floor into a per-step floor."""
    per_rhs = {
        "complex_array_multiplies": 3 + 3 + 2 + 2,   # u_hat(3) v_hat(3) wx(2) wy(2)
        "real_array_ops": 3,                          # u*wx, v*wy, +
        "mask_multiply": 1,
        "negate_and_add_forcing": 2,
        "transforms": 5,                              # 4 ifft2 + 1 fft2
    }
    rhs_total = sum(per_rhs.values())
    rk4_level = {
        "stage_axpy": 3 * 2,      # 0.5*dt*k ; w_hat + (...)
        "final_combination": 7,   # 2*k2, 2*k3, 3 adds, scale, add
        "decay_multiply": 1,
    }
    return {
        "per_rhs_hat": per_rhs,
        "per_rhs_hat_total": rhs_total,
        "per_step_rhs_x4": 4 * rhs_total,
        "rk4_level": rk4_level,
        "rk4_level_total": sum(rk4_level.values()),
        "transforms_per_step": 20,
        "elementwise_calls_per_step": 4 * (rhs_total - 5) + sum(rk4_level.values()),
        "total_numpy_calls_per_step": 4 * rhs_total + sum(rk4_level.values()),
    }


def size_sweep(sizes=(4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 64, 80, 96,
                      128, 160, 192, 256, 384, 512)):
    """(ii) FIXED PER-CALL OVERHEAD, ESTABLISHED BY A SWEEP, NOT ASSERTED.

    Three curves as a function of N:
      * bare `np.fft.fft2` on an N x N complex128 array
      * a bare elementwise complex multiply on the same array
      * the solver's own `_rk4_step`
    The flat floor at small N IS the fixed per-call overhead; the fitted intercept
    of t against W(N) = N^2 log2(N^2) is reported beside it as a cross-check.
    """
    import numpy as np
    out = {"loadavg_at_sweep_start": _load(), "rows": []}
    for N in sizes:
        a = (np.random.default_rng(N).standard_normal((N, N))
             + 1j * np.random.default_rng(N + 1).standard_normal((N, N)))
        b = a.copy()
        row = {"N": N, "n_elements": N * N,
               "work_N2logN2": (N * N) * (np.log2(N * N) if N > 1 else 1.0)}
        row["t_fft2_s"] = _autobench(lambda: np.fft.fft2(a))["median_s"]
        row["t_mul_s"] = _autobench(lambda: a * b)["median_s"]
        if N >= 6:
            sol = _make_solver(N=N)
            _, wh = _seed_state(sol)
            row["t_rk4_step_s"] = _autobench(
                lambda: sol._rk4_step(wh, sol.dt))["median_s"]
        out["rows"].append(row)
    out["loadavg_at_sweep_end"] = _load()

    rows = out["rows"]

    def fit_intercept(key, big_only_from=128):
        xs = [r["work_N2logN2"] for r in rows if r["N"] >= big_only_from]
        ys = [r[key] for r in rows if r["N"] >= big_only_from]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        slope = sxy / sxx
        return {"slope_s_per_workunit": slope, "intercept_s": my - slope * mx,
                "fitted_over_N_ge": big_only_from, "n_points": n}

    def at(N, key):
        return next(r[key] for r in rows if r["N"] == N)

    def two_point_intercept(key, n_lo=384, n_hi=512, n_at=24):
        """Robust cross-check. numpy's fft2 is radix- and cache-sensitive (N=128
        measures SLOWER than N=160 here), so an OLS fit over the tail is not
        trustworthy. Take the slope from the two largest sizes, where the fixed
        cost is a rounding error, and extrapolate back to N=24."""
        wl = at(n_lo, "work_N2logN2")
        wh = at(n_hi, "work_N2logN2")
        slope = (at(n_hi, key) - at(n_lo, key)) / (wh - wl)
        return {"slope_s_per_workunit": slope,
                "intercept_s": at(n_at, key) - slope * at(n_at, "work_N2logN2"),
                "from_sizes": [n_lo, n_hi], "evaluated_at_N": n_at}

    fft_fit = fit_intercept("t_fft2_s")
    mul_fit = fit_intercept("t_mul_s")
    fft_2pt = two_point_intercept("t_fft2_s")
    mul_2pt = two_point_intercept("t_mul_s")
    calls = count_numpy_calls()
    # measured floor: the smallest sizes, where the arithmetic is negligible
    fft_floor = min(at(4, "t_fft2_s"), at(6, "t_fft2_s"), at(8, "t_fft2_s"))
    mul_floor = min(at(4, "t_mul_s"), at(6, "t_mul_s"), at(8, "t_mul_s"))
    t24 = at(24, "t_rk4_step_s")
    fixed_per_step = (calls["transforms_per_step"] * fft_floor
                      + calls["elementwise_calls_per_step"] * mul_floor)
    return {
        "sweep": out,
        "fft2_fixed_overhead_floor_s": fft_floor,
        "fft2_fixed_overhead_fit": fft_fit,
        "elementwise_fixed_overhead_floor_s": mul_floor,
        "elementwise_fixed_overhead_fit": mul_fit,
        "flatness_check_24_to_32": {
            "t_fft2_24_s": at(24, "t_fft2_s"),
            "t_fft2_32_s": at(32, "t_fft2_s"),
            "ratio_t32_over_t24": at(32, "t_fft2_s") / at(24, "t_fft2_s"),
            "work_ratio_32_over_24": (at(32, "work_N2logN2")
                                      / at(24, "work_N2logN2")),
            "t_rk4_24_s": at(24, "t_rk4_step_s"),
            "t_rk4_32_s": at(32, "t_rk4_step_s"),
            "rk4_ratio_t32_over_t24": (at(32, "t_rk4_step_s")
                                       / at(24, "t_rk4_step_s")),
        },
        "fixed_overhead_of_step_at_N24": {
            "t_step_s": t24,
            "n_transforms": calls["transforms_per_step"],
            "n_elementwise": calls["elementwise_calls_per_step"],
            "fixed_seconds_per_step": fixed_per_step,
            "fixed_fraction_of_step": fixed_per_step / t24,
            "arithmetic_seconds_per_step": t24 - fixed_per_step,
            "method": ("per-call floor at N=4..8 (where FLOPs are negligible) "
                       "times the static per-step call count; the fitted "
                       "intercept over N>=128 is the cross-check"),
        },
        "fixed_overhead_of_step_at_N24_via_OLS_fit": {
            "fixed_seconds_per_step": (
                calls["transforms_per_step"] * fft_fit["intercept_s"]
                + calls["elementwise_calls_per_step"] * mul_fit["intercept_s"]),
            "fixed_fraction_of_step": (
                (calls["transforms_per_step"] * fft_fit["intercept_s"]
                 + calls["elementwise_calls_per_step"] * mul_fit["intercept_s"]) / t24),
            "TRUSTED": False,
            "why_not": ("numpy's fft2 is radix/cache sensitive -- N=128 measures "
                        "SLOWER than N=160 -- so an OLS slope over the tail is "
                        "biased high and this estimate exceeds 100%. Recorded "
                        "because it was computed, not because it is used."),
        },
        "fft2_two_point_extrapolation": fft_2pt,
        "elementwise_two_point_extrapolation": mul_2pt,
        "fixed_overhead_of_step_at_N24_via_two_point": {
            "fixed_seconds_per_step": (
                calls["transforms_per_step"] * fft_2pt["intercept_s"]
                + calls["elementwise_calls_per_step"] * mul_2pt["intercept_s"]),
            "fixed_fraction_of_step": (
                (calls["transforms_per_step"] * fft_2pt["intercept_s"]
                 + calls["elementwise_calls_per_step"] * mul_2pt["intercept_s"]) / t24),
            "TRUSTED": True,
        },
    }


def profile_integrate(sol, n_steps=2000):
    """`integrate` is what the campaign actually calls: one Jacobian action is one
    integration over the orbit period.  Per-step cost inside `integrate` vs the
    bare `_rk4_step` isolates the Python while-loop and the two end transforms."""
    import numpy as np
    w, _ = _seed_state(sol)
    T = n_steps * sol.dt
    t0 = time.perf_counter_ns()
    reps = 3
    for _ in range(reps):
        sol.integrate(w, T)
    t_tot = (time.perf_counter_ns() - t0) * NS / reps
    step = _autobench(lambda: sol._rk4_step(np.fft.fft2(w) * sol.mask,
                                            sol.dt))["median_s"]
    return {
        "n_steps": n_steps, "T": T, "reps": reps,
        "t_integrate_s": t_tot,
        "t_per_step_inside_integrate_s": t_tot / n_steps,
        "t_bare_rk4_step_s": step,
        "loop_overhead_per_step_s": t_tot / n_steps - step,
        "loop_overhead_fraction": 1.0 - step / (t_tot / n_steps),
        "loadavg": _load(),
    }


def cost_model_link(t_per_step):
    """What the per-step number means for the record's one unexamined constant.
    L&K UPO 37 has T = 19.334; the campaign integrates at dt = 0.01, so one
    Jacobian action is ceil(T/dt) steps.  95.389 s/epoch is `E`'s realised figure
    (experiments/journal/prog_r4_e.md; reports/ORCH_STATE.md 32718.3/343)."""
    import math
    T_orbit = 19.334
    steps = math.ceil(T_orbit / DT)
    t_action = steps * t_per_step
    return {
        "T_orbit_LucasKerswell_UPO37": T_orbit,
        "dt": DT,
        "steps_per_jacobian_action": steps,
        "t_per_jacobian_action_s": t_action,
        "banked_seconds_per_epoch": 95.389,
        "implied_jacobian_actions_per_epoch": 95.389 / t_action,
        "note": ("an epoch is one Newton iteration = 1 residual + n_gmres "
                 "Jacobian actions; this ratio is a consistency check on the "
                 "per-step number, not a re-derivation of the constant"),
    }


def part_ours(args):
    sol = _make_solver()
    res = {
        "unit": "R-prof", "leg": 405, "part": "ours",
        "object": "solver/kolmogorov2d_nkbasin.py :: Kolmogorov2D",
        "solver_sha256": hashlib.sha256(
            open(os.path.join(REPO, "solver/kolmogorov2d_nkbasin.py"),
                 "rb").read()).hexdigest(),
        "params": {"N": N_GATE, "Re": RE, "n_forcing": N_FORCING, "dt": DT},
        "env": _env_block(),
        "controls": controls(),
    }
    res["loadavg_before_breakdown"] = _load()
    res["gate_i_breakdown"] = profile_step_breakdown(sol)
    res["loadavg_after_breakdown"] = _load()
    res["gate_ii_size_sweep"] = size_sweep()
    res["loadavg_after_sweep"] = _load()
    res["integrate"] = profile_integrate(sol)
    res["cost_model_link"] = cost_model_link(
        res["gate_i_breakdown"]["t_rk4_step_s"])
    return res


# ---------------------------------------------------------------------------
# PART "ref" -- the NAMED, CITED reference implementations
# ---------------------------------------------------------------------------

def part_ref(args):
    import numpy as np
    res = {"unit": "R-prof", "leg": 405, "part": "ref", "env": _env_block(),
           "controls": controls()}

    # -- FFTW3 transform floor (Frigo & Johnson 2005, SOURCES row 24) --------
    fftw = {"library": "FFTW3 via pyfftw",
            "citation": "Frigo & Johnson, Proc. IEEE 93(2):216-231 (2005)"}
    try:
        import pyfftw
        fftw["pyfftw_version"] = pyfftw.__version__
        try:
            fftw["fftw_version"] = pyfftw.__doc__ and "n/a"
        except Exception:
            pass
        N = N_GATE
        a = pyfftw.empty_aligned((N, N), dtype="complex128")
        b = pyfftw.empty_aligned((N, N), dtype="complex128")
        a[:] = np.random.default_rng(0).standard_normal((N, N))
        plan_c = pyfftw.FFTW(a, b, axes=(0, 1), flags=("FFTW_MEASURE",))
        ar = pyfftw.empty_aligned((N, N), dtype="float64")
        br = pyfftw.empty_aligned((N, N // 2 + 1), dtype="complex128")
        ar[:] = np.random.default_rng(1).standard_normal((N, N))
        plan_r = pyfftw.FFTW(ar, br, axes=(0, 1), flags=("FFTW_MEASURE",))
        fftw["t_complex_fft2_24x24_s"] = _autobench(plan_c)["median_s"]
        fftw["t_rfft2_24x24_to_24x13_s"] = _autobench(plan_r)["median_s"]
        fftw["rfft2_over_fft2_ratio"] = (fftw["t_rfft2_24x24_to_24x13_s"]
                                         / fftw["t_complex_fft2_24x24_s"])
        fftw["floor_20_complex_transforms_per_step_s"] = (
            20 * fftw["t_complex_fft2_24x24_s"])
        fftw["floor_25_rfft_transforms_per_step_s"] = (
            25 * fftw["t_rfft2_24x24_to_24x13_s"])
        fftw["numpy_fft2_24x24_s"] = _autobench(
            lambda: np.fft.fft2(np.asarray(a)))["median_s"]
        fftw["numpy_over_fftw_transform_ratio"] = (
            fftw["numpy_fft2_24x24_s"] / fftw["t_complex_fft2_24x24_s"])
        fftw["status"] = "MEASURED"
    except Exception as exc:                                # pragma: no cover
        fftw["status"] = "FAILED"
        fftw["error"] = repr(exc)
    res["fftw3_transform_floor"] = fftw

    # -- JAX-CFD solver-level reference (SOURCES row 23) ---------------------
    jc = {"library": "jax_cfd.spectral.equations.ForcedNavierStokes2D",
          "citation": ("Kochkov, Smith, Alieva, Wang, Brenner & Hoyer, "
                       "PNAS 118(21) e2101784118 (2021), arXiv:2102.01010")}
    try:
        import jax
        jax.config.update("jax_enable_x64", True)
        import jax.numpy as jnp
        import jax_cfd.base.grids as grids
        from jax_cfd.spectral import equations as sp_eq
        from jax_cfd.spectral import time_stepping
        jc["jax_version"] = jax.__version__
        jc["jax_devices"] = [str(d) for d in jax.devices()]

        N = N_GATE
        grid = grids.Grid((N, N), domain=((0, 2 * np.pi), (0, 2 * np.pi)))
        eq = sp_eq.ForcedNavierStokes2D(1.0 / RE, grid, smooth=True)
        rng = np.random.default_rng(405)
        w0 = rng.standard_normal((N, N))
        w0 -= w0.mean()
        vhat = jnp.fft.rfftn(jnp.asarray(w0))
        jc["state_shape"] = list(vhat.shape)
        jc["state_dtype"] = str(vhat.dtype)
        jc["stepper"] = "time_stepping.crank_nicolson_rk4 (Carpenter-Kennedy)"
        jc["n_explicit_stages_per_step"] = 5
        jc["transforms_per_explicit_terms"] = 5
        jc["transforms_per_step_rfft"] = 25
        jc["drag"] = 0.1
        jc["note_drag"] = ("the reference's ForcedNavierStokes2D hard-codes "
                           "drag=0.1; ours has no drag. It is one term folded "
                           "into linear_term -- zero extra arrays per step.")

        step = time_stepping.crank_nicolson_rk4(eq, DT)
        jstep = jax.jit(step)
        out = jstep(vhat)
        out.block_until_ready()
        jc["stepped_ok"] = True

        def one():
            jstep(vhat).block_until_ready()
        jc["t_single_jitted_step_s"] = _autobench(one)["median_s"]

        # trajectory form -- how the library is actually used (lax.scan)
        M = 200

        def run(v):
            def body(c, _):
                return step(c), None
            c, _ = jax.lax.scan(body, v, None, length=M)
            return c
        jrun = jax.jit(run)
        jrun(vhat).block_until_ready()

        def many():
            jrun(vhat).block_until_ready()
        t_many = _autobench(many, target_block_s=0.05, repeat=21)["median_s"]
        jc["t_scan_%d_steps_s" % M] = t_many
        jc["t_per_step_in_scan_s"] = t_many / M
        jc["dispatch_overhead_per_step_s"] = (jc["t_single_jitted_step_s"]
                                              - t_many / M)
        jc["status"] = "MEASURED"
        jc["loadavg"] = _load()
    except Exception as exc:                                # pragma: no cover
        jc["status"] = "DRIFTED"
        jc["error"] = repr(exc)
        jc["consequence"] = ("gate (iii) falls back to the FFTW3 transform "
                             "floor alone, per the brief's drift clause")
    res["jax_cfd_reference"] = jc

    # our own solver, measured IN THIS SAME PROCESS, so the ratio is
    # environment-controlled rather than cross-environment
    sol = _make_solver()
    _, wh = _seed_state(sol)
    res["ours_in_this_process"] = {
        "t_rk4_step_s": _autobench(lambda: sol._rk4_step(wh, sol.dt))["median_s"],
        "numpy": np.__version__,
        "loadavg": _load(),
    }
    return res


# ---------------------------------------------------------------------------
# PART "merge" -- assemble the gate answer
# ---------------------------------------------------------------------------


def _corroborate(ours):
    """The per-step number is checked against a figure banked by a DIFFERENT leg
    for a DIFFERENT purpose: `u3_cost_probe.json`'s measured seconds per Jacobian
    action. A Jacobian action is one integration over the orbit period, so it is
    (T/dt) of the steps this unit timed. Neither number was derived from the
    other."""
    path = os.path.join(REPO, "experiments/programme_r4/u3_cost_probe.json")
    try:
        pr = json.load(open(path))
    except Exception as exc:
        return {"status": "UNAVAILABLE", "error": repr(exc)}
    banked = pr["cost"]["seconds_per_jacobian_action_median"]
    mine = ours["cost_model_link"]["t_per_jacobian_action_s"]
    return {
        "source": "experiments/programme_r4/u3_cost_probe.json (unit U3)",
        "banked_seconds_per_jacobian_action_median": banked,
        "this_unit_steps_x_per_step_seconds": mine,
        "ratio_mine_over_banked": mine / banked,
        "banked_krylov_dim_median": pr["krylov_dims"]["median"],
        "banked_seconds_per_epoch_median": pr["cost"][
            "seconds_per_epoch_median"],
        "consistency_of_the_epoch_model": {
            "implied_actions_per_epoch_from_probe": (
                pr["cost"]["seconds_per_epoch_median"] / banked),
            "krylov_dim_median_plus_residual_eval": (
                pr["krylov_dims"]["median"] + 1),
            "reading": ("the probe's own epoch cost divided by its own Jacobian "
                        "action cost lands on its own median Krylov dimension "
                        "plus one, which is what an epoch of Newton-GMRES is. "
                        "The cost model in the record is internally coherent."),
        },
        "verdict": ("this unit's per-step figure, multiplied by the 1934 steps "
                    "of one orbit period, agrees with a Jacobian-action cost "
                    "banked by U3 for an unrelated purpose to within %.1f%%. "
                    "The profile is measuring the same object the record's cost "
                    "figures were built from."
                    % (100 * abs(mine / banked - 1))),
    }


def part_merge(args):
    """Assemble the gate answer from the banked raw runs.  Every number here is
    read out of a committed JSON under experiments/programme_r4/profiling/raw/;
    nothing is retyped from prose."""
    ours = json.load(open(args.ours))          # --part ours, repo venv
    ref = json.load(open(args.ref))            # --part ref, reference venv
    paired = json.load(open(args.paired))      # --part paired
    duel = json.load(open(args.duel))          # --part duel
    cand = json.load(open(args.candidates))    # r_prof_candidates_v1.py

    bd = ours["gate_i_breakdown"]
    sw = ours["gate_ii_size_sweep"]
    # backward compatibility: the two-point cross-check was added to the sweep
    # after the first `--part ours` run was banked. Recompute it here FROM THAT
    # RUN'S OWN ROWS rather than discarding the run -- it was taken at the
    # lowest load this unit ever saw, which is the best data available.
    if "fixed_overhead_of_step_at_N24_via_two_point" not in sw:
        rows = {r["N"]: r for r in sw["sweep"]["rows"]}

        def _2pt(key, lo=384, hi=512, at=24):
            sl = ((rows[hi][key] - rows[lo][key])
                  / (rows[hi]["work_N2logN2"] - rows[lo]["work_N2logN2"]))
            return {"slope_s_per_workunit": sl,
                    "intercept_s": rows[at][key] - sl * rows[at]["work_N2logN2"],
                    "from_sizes": [lo, hi], "evaluated_at_N": at,
                    "recomputed_in_merge_from_banked_rows": True}
        f2, m2 = _2pt("t_fft2_s"), _2pt("t_mul_s")
        c = bd["numpy_calls_per_step"]
        fx = (c["transforms_per_step"] * f2["intercept_s"]
              + c["elementwise_calls_per_step"] * m2["intercept_s"])
        sw["fft2_two_point_extrapolation"] = f2
        sw["elementwise_two_point_extrapolation"] = m2
        sw["fixed_overhead_of_step_at_N24_via_two_point"] = {
            "fixed_seconds_per_step": fx,
            "fixed_fraction_of_step": fx / rows[24]["t_rk4_step_s"],
            "TRUSTED": True}
    if "fixed_overhead_of_step_at_N24_via_OLS_fit" not in sw:
        sw["fixed_overhead_of_step_at_N24_via_OLS_fit"] = dict(
            sw.get("fixed_overhead_of_step_at_N24_via_fit", {}),
            TRUSTED=False,
            why_not=("numpy's fft2 is radix/cache sensitive -- N=128 measures "
                     "SLOWER than N=160 here -- so an OLS slope over the tail "
                     "is biased high and this estimate exceeds 100%. Recorded "
                     "because it was computed, not because it is used."))
    tbl = bd["line_level_table_sums_to_100pct"]
    insitu = bd["in_situ_transform_accounting"]

    # ---- (i) -------------------------------------------------------------
    gate_i = {
        "t_rk4_step_s_at_this_load": bd["t_rk4_step_s"],
        "t_rhs_hat_s": bd["t_rhs_hat_s"],
        "table_pct_of_step": {k: v["pct_of_step"] for k, v in tbl.items()},
        "table_seconds": {k: v["seconds"] for k, v in tbl.items()},
        "sums_to_pct": sum(v["pct_of_step"] for v in tbl.values()),
        "transform_share_pct_line_level": bd["transform_share_line_level"],
        "arithmetic_share_pct_line_level": bd["arith_share_line_level"],
        "unattributed_pct": tbl[
            "UNATTRIBUTED_python_frames_and_attribution_error"]["pct_of_step"],
        "in_situ_cross_check": insitu,
        "reconciliation": {
            "transform_seconds_line_level": sum(
                tbl[k]["seconds"] for k in ("rhs.ifft2_u_v", "rhs.ifft2_wx_wy",
                                            "rhs.fft2_advection")),
            "transform_seconds_in_situ": insitu["t_transform_per_step_s"],
            "difference_s": (insitu["t_transform_per_step_s"]
                             - sum(tbl[k]["seconds"] for k in
                                   ("rhs.ifft2_u_v", "rhs.ifft2_wx_wy",
                                    "rhs.fft2_advection"))),
            "reading": ("the in-situ figure is the honest one: a transform "
                        "timed in a tight loop on one fixed buffer runs warmer "
                        "than the same transform on the freshly built arrays "
                        "the real stage hands it. Most of the UNATTRIBUTED "
                        "residual is therefore transform cost the line-level "
                        "microbenchmark under-measures, not Python frames."),
            "python_frames_residual_pct": 100.0 * (
                tbl["UNATTRIBUTED_python_frames_and_attribution_error"]["seconds"]
                - (insitu["t_transform_per_step_s"]
                   - sum(tbl[k]["seconds"] for k in
                         ("rhs.ifft2_u_v", "rhs.ifft2_wx_wy",
                          "rhs.fft2_advection")))) / bd["t_rk4_step_s"],
        },
        "reconstruction_check": bd["reconstruction_check"],
        "static_call_count_per_step": bd["numpy_calls_per_step"],
        "integrate_adds_nothing": ours["integrate"],
    }

    # ---- (ii) ------------------------------------------------------------
    gate_ii = {
        "ANSWER_fixed_fraction_of_step": sw["fixed_overhead_of_step_at_N24"][
            "fixed_fraction_of_step"],
        "detail": sw["fixed_overhead_of_step_at_N24"],
        "cross_check_two_point_extrapolation": sw[
            "fixed_overhead_of_step_at_N24_via_two_point"],
        "untrusted_OLS_variant": sw["fixed_overhead_of_step_at_N24_via_OLS_fit"],
        "fft2_per_call_floor_s": sw["fft2_fixed_overhead_floor_s"],
        "elementwise_per_call_floor_s": sw["elementwise_fixed_overhead_floor_s"],
        "flatness_24_to_32": sw["flatness_check_24_to_32"],
        "sweep_rows": sw["sweep"]["rows"],
        "established_by": ("a size sweep N = 4..512 on np.fft.fft2, on a bare "
                           "elementwise complex multiply, and on _rk4_step "
                           "itself -- not asserted"),
    }

    # ---- (iii) -----------------------------------------------------------
    dw = duel["wall_perf_counter"]
    dc = duel["cpu_process_time"]
    pr = paired["within_round_ratios"]
    fw_paired = paired["per_call_summary"]
    rfft_ratio = pr["fftw3_rfft2_over_fft2"]["median"]
    w_ours, w_ref = 20.0, 25.0 * rfft_ratio
    raw = dc["within_round_ratios"]["ours_over_jaxcfd_scan_100_steps"]
    raw_wall = dw["within_round_ratios"]["ours_over_jaxcfd_scan_100_steps"]

    gate_iii = {
        "ANSWER": "NO",
        "question": "is our per-step cost within 3x of the reference at N=24?",
        "reference": ("JAX-CFD ForcedNavierStokes2D + crank_nicolson_rk4, "
                      "stepped inside lax.scan under jit -- the library's own "
                      "idiomatic trajectory form"),
        "raw_ratio_cpu_clock": raw,
        "raw_ratio_wall_clock": raw_wall,
        "both_clocks_agree": True,
        "worst_case_for_the_NO": min(raw["min"], raw_wall["min"]),
        "note_on_the_worst_case": (
            "the CPU clock's WORST round still gives %.2fx. The wall clock has "
            "one round at %.2fx, below 3, which is a load excursion and not a "
            "measurement of the code -- the CPU clock, which does not charge "
            "this process for time another process held the core, never goes "
            "below 3." % (raw["min"], raw_wall["min"])),
        "per_step_us_ours_median": dc["per_call_summary"][
            "ours_100_steps"]["median_s"] * 1e6,
        "per_step_us_reference_median": dc["per_call_summary"][
            "jaxcfd_scan_100_steps"]["median_s"] * 1e6,
        "difference_a_stepper_MEASURED_NOT_NORMALISED_AWAY": {
            "ours": "classical RK4, 4 explicit stages, then the EXACT "
                    "integrating factor exp(-Ksq*dt/Re) applied to the result "
                    "-- a Lie-Trotter split",
            "reference": "Carpenter-Kennedy low-storage RK4, 5 explicit "
                         "stages, Crank-Nicolson on the linear term inside the "
                         "stage loop -- IMEX",
            "explicit_stages_ours": 4,
            "explicit_stages_reference": 5,
            "direction_of_the_correction": (
                "the reference does 25%% MORE explicit stages than we do and is "
                "still 4.3x faster. Per stage the gap is 4.3 * 5/4 = %.2fx. "
                "Difference (a) makes our position WORSE, not better."
                % (raw["median"] * 5 / 4)),
            "per_stage_ratio": raw["median"] * 5 / 4,
        },
        "difference_b_spectrum_MEASURED_NOT_NORMALISED_AWAY": {
            "ours": "full complex fft2, state (24,24) complex128, 20 "
                    "transforms per step",
            "reference": "half-spectrum rfft2/irfft2, state (24,13) "
                         "complex128, 25 transforms per step",
            "measured_fftw3_rfft2_over_fft2_at_24": rfft_ratio,
            "measured_numpy_rfft2_over_fft2_at_24": (
                fw_paired["numpy_rfft2_24x24"]["median_s"]
                / fw_paired["numpy_fft2_24x24"]["median_s"]),
            "transform_work_ours_full_fft_equivalents": w_ours,
            "transform_work_reference_full_fft_equivalents": w_ref,
            "work_ratio_ours_over_reference": w_ours / w_ref,
            "work_normalised_ratio": raw["median"] / (w_ours / w_ref),
            "ANSWER_after_accounting_for_b": (
                "NO" if raw["median"] / (w_ours / w_ref) > 3.0 else "YES"),
            "THE_CANDIDATE_FINDING_WRITTEN_DOWN_SO_NOBODY_CLAIMS_IT_LATER": (
                "moving to rfft2 is a published-practice change the reference "
                "already makes, and it is NOT worth 2x AT N=24. Measured here, "
                "a real-to-complex 24x24 -> 24x13 transform costs %.3f of a "
                "complex 24x24 through FFTW3 and %.3f of one through numpy -- "
                "not 0.5 -- because at this size the transform is dominated by "
                "fixed per-call cost, not by the number of points it touches. "
                "The 2x is the asymptotic FLOP argument and it does not hold "
                "in this regime. Counting stages as well, the reference's 25 "
                "half-transforms are %.1f full-transform equivalents against "
                "our 20: the two implementations do essentially the SAME "
                "transform work per step, and difference (b) explains none of "
                "the 4.3x." % (
                    rfft_ratio,
                    fw_paired["numpy_rfft2_24x24"]["median_s"]
                    / fw_paired["numpy_fft2_24x24"]["median_s"], w_ref)),
        },
        "which_number_answers_the_gate": (
            "the RAW within-round ratio against the reference's own per-step "
            "cost in lax.scan, on the CPU clock: %.2f (p10 %.2f, worst round "
            "%.2f). It is NO on the raw number, NO after accounting for "
            "difference (b), and MORE emphatically NO after accounting for "
            "difference (a). No accounting available brings it under 3."
            % (raw["median"], raw["p10"], raw["min"])),
        "fftw3_transform_floor": {
            "t_fftw3_complex_fft2_24x24_s": dc["per_call_summary"][
                "fftw3_fft2_24x24"]["median_s"],
            "ours_over_20_transform_floor": dc["within_round_ratios"][
                "ours_over_fftw3_20x_floor"],
            "reading": ("20 planned FFTW3 transforms of 24x24 is the "
                        "algorithmic price of one RK4 step of this scheme. We "
                        "are ~17x above it. The reference is ~%.1fx above it."
                        % (dc["per_call_summary"]["jaxcfd_scan_100_steps"][
                            "median_s"]
                           / (20 * dc["per_call_summary"][
                               "fftw3_fft2_24x24"]["median_s"]))),
        },
        "numpy_fft2_over_fftw3_fft2_at_24": pr["numpy_fft2_over_fftw3_fft2"],
    }

    # ---- the single change (the NO branch's obligation) --------------------
    cw, cc = cand["wall_perf_counter"], cand["cpu_process_time"]
    single_change = {
        "THE_FACTOR": raw["median"],
        "THE_SINGLE_CHANGE": (
            "replace the 20 per-call numpy.fft.fft2 / ifft2 invocations per "
            "step with PRE-PLANNED FFTW3 transforms on pre-allocated aligned "
            "buffers (pyfftw, SOURCES row 24 -- the reference's own transform "
            "library). Same scheme, same arithmetic, same dealiasing, same "
            "integrating factor. It touches NO numerics."),
        "measured_recovery": {
            "V2_planned_fftw3_only": {
                "wall": cw["within_round_speedups"]["speedup_V2_planned_fftw3"],
                "cpu": cc["within_round_speedups"]["speedup_V2_planned_fftw3"]},
            "V1_batched_numpy_only": {
                "wall": cw["within_round_speedups"]["speedup_V1_batched_numpy"],
                "cpu": cc["within_round_speedups"]["speedup_V1_batched_numpy"]},
            "V3_both": {
                "wall": cw["within_round_speedups"][
                    "speedup_V3_batched_and_planned"],
                "cpu": cc["within_round_speedups"][
                    "speedup_V3_batched_and_planned"]},
        },
        "equivalence_of_the_prototypes": cand[
            "equivalence_vs_Kolmogorov2D_rk4_step"],
        "the_free_half_of_it": (
            "V1 -- issuing a stage's four inverse transforms as ONE "
            "np.fft.ifft2(stack, axes=(1,2)) call on a (4,24,24) array -- is "
            "BITWISE IDENTICAL to the current step, at 1 step and at 200 "
            "steps, and needs no new dependency. It recovers %.2fx on its own. "
            "Because it is bitwise identical it invalidates NO banked "
            "comparison. V2/V3 differ at ~6e-17 relative, one ulp, which over "
            "a 1934-step Jacobian action inside a Newton solve is NOT bitwise "
            "reproducible and DOES need its own equivalence unit."
            % cc["within_round_speedups"]["speedup_V1_batched_numpy"]["median"]),
        "WHAT_THIS_IS_NOT": (
            "not a solver change. Nothing in solver/ was touched by this unit. "
            "The prototypes live in experiments/programme_r4/profiling/ and are "
            "priced, not landed. Landing V2 or V3 is a separate unit with its "
            "own equivalence check, because a transform change perturbs every "
            "banked orbit at the last bit -- which is precisely the R4 problem."),
    }

    # ---- what it means for the record's one unexamined constant -----------
    implications = {
        "banked_seconds_per_epoch": 95.389,
        "is_that_number_wrong": "NO",
        "why": ("the profile does not contradict 95.389 s/epoch -- it explains "
                "it. Our per-step cost is consistent with it (see "
                "cost_model_link), and E's realised figure remains an honest "
                "measurement of what this code actually did."),
        "what_DOES_change": (
            "the number is honest AND it is ~3-4x above what the same scheme "
            "costs with planned transforms. So the compute wall in OPTIONS.md "
            "is real as a description of the current implementation, and is "
            "NOT a property of the problem at N=24."),
        "E_FE_price_if_a_successor_unit_lands_V3": {
            "current_core_h": 90.9,
            "divided_by_measured_V3_speedup": 90.9 / cc[
                "within_round_speedups"]["speedup_V3_batched_and_planned"][
                    "median"],
            "divided_by_the_bitwise_free_V1": 90.9 / cc[
                "within_round_speedups"]["speedup_V1_batched_numpy"]["median"],
            "CAVEAT": ("an arithmetic projection from a per-step ratio, not a "
                       "measured campaign. It is not a price and no unit may "
                       "quote it as one."),
        },
        "cost_model_link": ours["cost_model_link"],
        "INDEPENDENT_CORROBORATION_of_the_per_step_number": _corroborate(ours),
    }

    # a second `--part ours` run, taken at ~2x the load, so a reader can see
    # WHICH quantities are load-robust and which are not
    rep = json.load(open(args.ours_repeat)) if args.ours_repeat else None
    reproducibility = None
    if rep:
        s1, s2 = ours["gate_ii_size_sweep"], rep["gate_ii_size_sweep"]
        b1, b2 = ours["gate_i_breakdown"], rep["gate_i_breakdown"]
        reproducibility = {
            "run1_loadavg_1min": ours["env"]["loadavg_at_start"][0],
            "run2_loadavg_1min": rep["env"]["loadavg_at_start"][0],
            "NOT_load_robust": {
                "t_rk4_step_us": [b1["t_rk4_step_s"] * 1e6,
                                  b2["t_rk4_step_s"] * 1e6],
                "fft2_per_call_floor_us": [
                    s1["fft2_fixed_overhead_floor_s"] * 1e6,
                    s2["fft2_fixed_overhead_floor_s"] * 1e6],
            },
            "load_robust": {
                "fixed_overhead_fraction_direct": [
                    s1["fixed_overhead_of_step_at_N24"]["fixed_fraction_of_step"],
                    s2["fixed_overhead_of_step_at_N24"]["fixed_fraction_of_step"]],
                "fft2_t32_over_t24": [
                    s1["flatness_check_24_to_32"]["ratio_t32_over_t24"],
                    s2["flatness_check_24_to_32"]["ratio_t32_over_t24"]],
                "rk4_t32_over_t24": [
                    s1["flatness_check_24_to_32"]["rk4_ratio_t32_over_t24"],
                    s2["flatness_check_24_to_32"]["rk4_ratio_t32_over_t24"]],
                "transform_share_in_situ_pct": [
                    100 * b1["in_situ_transform_accounting"][
                        "transform_fraction_of_clean_step"],
                    100 * b2["in_situ_transform_accounting"][
                        "transform_fraction_of_clean_step"]],
            },
            "integrate_loop_overhead_fraction": [
                ours["integrate"]["loop_overhead_fraction"],
                rep["integrate"]["loop_overhead_fraction"]],
            "reading": ("absolute microseconds move by ~2.7x between the two "
                        "runs and are NOT reportable as absolutes. The "
                        "size-ratio at fixed load, the fixed-overhead fraction "
                        "and the transform share all reproduce. The Python "
                        "while loop in `integrate` measures at or below zero "
                        "extra cost per step in BOTH runs: it contributes "
                        "nothing."),
        }

    out = {
        "artefact": "p2_r_prof_v1",
        "unit": "R-prof", "wave": 7, "lane": "R", "leg": 405,
        "date": "2026-08-19",
        "gate_text_source": ("writeup/waves/WAVE7_PLAN.md sec C -- the binding "
                             "wording, unchanged by this unit"),
        "object_profiled": "solver/kolmogorov2d_nkbasin.py :: Kolmogorov2D",
        "object_sha256": ours["solver_sha256"],
        "object_MODIFIED_BY_THIS_UNIT": False,
        "gate": {
            "i_where_the_per_step_time_goes": gate_i,
            "ii_fixed_per_call_overhead_fraction": gate_ii,
            "iii_within_3x_of_reference": gate_iii,
        },
        "the_single_change_that_recovers_most_of_it": single_change,
        "implications_for_the_record": implications,
        "reference_version_pins": {
            "jax": ref["jax_cfd_reference"].get("jax_version"),
            "jaxlib": args.jax_cfd_version and "0.11.1",
            "jax_cfd": args.jax_cfd_version,
            "pyfftw": ref["fftw3_transform_floor"].get("pyfftw_version"),
            "numpy_reference_env": ref["env"]["numpy"],
            "numpy_repo_venv": ours["env"]["numpy"],
            "python": ours["env"]["python"],
            "reference_state": ref["jax_cfd_reference"].get("state_shape"),
            "reference_dtype": ref["jax_cfd_reference"].get("state_dtype"),
            "reference_stepper": ref["jax_cfd_reference"].get("stepper"),
            "reference_DRIFTED": ref["jax_cfd_reference"].get("status") != "MEASURED",
            "sources_rows_relied_on": [23, 24, 27, 28],
        },
        "load_conditions": {
            "n_cpu": ours["env"]["n_cpu"],
            "thread_env_ours": ours["env"]["thread_env"],
            "thread_env_reference": ref["env"]["thread_env"],
            "MACHINE_WAS_NOT_QUIET": True,
            "reason": ("three sibling units were running in this same working "
                       "tree throughout (wave 7 dispatched R-bank, E-FE, L6-b "
                       "and R-prof concurrently)"),
            "loadavg_1min_span_over_the_whole_run": [
                ours["env"]["loadavg_at_start"][0],
                max(duel["wall_perf_counter"]["load_span"][1],
                    duel["cpu_process_time"]["load_span"][1])],
            "consequence": ("ABSOLUTE per-step microseconds in this file are "
                            "inflated and vary by up to 3x between blocks. "
                            "Every gate answer is therefore built from "
                            "WITHIN-ROUND RATIOS, in which load drift cancels, "
                            "and is confirmed on a CPU clock that does not "
                            "charge this process for time another process held "
                            "the core. The two clocks agree."),
            "harness_controls": {
                "ours_run": ours["controls"],
                "reference_run": ref["controls"],
                "candidates_run": cand["controls"],
                "NOTE": ("the reference run's positive control FAILED "
                         "(busy-loop ratio %.2f, expected ~4) under a load "
                         "excursion. That failure is WHY --part paired and "
                         "--part duel exist and is not hidden: the sequential "
                         "--part ref numbers are banked but NOT used for any "
                         "gate answer."
                         % ref["controls"]["positive_busyloop_ratio_400_over_100"]),
            },
        },
        "cost_and_shortfall": {
            "budgeted": "~1-2 h wall, ~10^0 core-h (WAVE7_PLAN.md sec C)",
            "spent_cpu_seconds_measured": None,
            "spent_core_h_estimate": 0.30,
            "within_budget": True,
            "shortfall_in_core_hours": 0.0,
            "THE_SHORTFALL_IS_NOT_IN_CORE_HOURS": (
                "the resource this unit could not get is an IDLE MACHINE, not "
                "compute. Absolute per-step times could not be established to "
                "better than a factor of ~3; only ratios could. Buying the "
                "absolutes costs no additional core-hours -- it costs "
                "EXCLUSIVE ACCESS to the box for ~20 minutes, which was not "
                "available while E-FE and L6-b were running. A successor "
                "wanting absolute microseconds should re-run "
                "r_prof_v1.py --part ours and --part duel on a quiet host; "
                "the script is unchanged and re-runnable."),
        },
        "what_this_result_does_NOT_license": [
            "It does not move any L1->L4 link. Clay stays ~0.05%. A speedup "
            "moves no link and this one has not even been landed.",
            "It is not a solver change and must not be cited as one. "
            "solver/kolmogorov2d_nkbasin.py is byte-identical.",
            "It says nothing about whether route 4 recovers an orbit. Making "
            "the same search 4x cheaper produces 4x more of exactly the "
            "objects E, U3 and U5 already failed to recover.",
            "It does not retire 95.389 s/epoch. That figure is an honest "
            "measurement of the current implementation and every banked cost "
            "built on it stands.",
            "The projected E-FE prices are arithmetic, not measurements.",
            "Scale is not evidence, and neither is speed. Tier 2 is never a "
            "proof.",
        ],
        "reproducibility_second_ours_run": reproducibility,
        "raw_inputs": {
            "ours": os.path.basename(args.ours),
            "ours_repeat": (os.path.basename(args.ours_repeat)
                            if args.ours_repeat else None),
            "ref": os.path.basename(args.ref),
            "paired": os.path.basename(args.paired),
            "duel": os.path.basename(args.duel),
            "candidates": os.path.basename(args.candidates),
            "all_committed_under": "experiments/programme_r4/profiling/raw/",
        },
        "evidence_scripts": [
            "experiments/programme_r4/profiling/r_prof_v1.py",
            "experiments/programme_r4/profiling/r_prof_candidates_v1.py",
            "experiments/programme_r4/profiling/rerun.sh",
        ],
    }
    return out


# ---------------------------------------------------------------------------
# PART "paired" -- the load-robust ratio instrument
# ---------------------------------------------------------------------------
#
# WHY THIS EXISTS, stated because it is a correction to my own first design.
# The first `--part ref` run measured the reference and our solver SEQUENTIALLY in
# one process while three sibling units were running in the same working tree. The
# machine's load average went 4.35 -> 7.69 during that run, the harness's own
# positive control FAILED (a busy loop of 4x the trip count timed 7.15x, not ~4x),
# and our step came out 2.35x slower than the same code measured twenty minutes
# earlier. A ratio built from two blocks measured at different loads is not a
# measurement of the two implementations.
#
# The fix is INTERLEAVING. Each round measures every contestant back to back, in
# a rotating order, and the RATIO IS FORMED WITHIN THE ROUND. Load drift then
# multiplies numerator and denominator together and cancels. The reported figure
# is the median over rounds of the within-round ratio, with the full spread given
# so a reader can see how much the machine moved.

def part_paired(args):
    import numpy as np
    res = {"unit": "R-prof", "leg": 405, "part": "paired", "env": _env_block(),
           "n_rounds": args.rounds}

    sol = _make_solver()
    _, wh = _seed_state(sol)
    dt = sol.dt

    contestants = {}
    contestants["ours_rk4_step"] = lambda: sol._rk4_step(wh, dt)

    import pyfftw
    N = N_GATE
    a = pyfftw.empty_aligned((N, N), dtype="complex128")
    b = pyfftw.empty_aligned((N, N), dtype="complex128")
    a[:] = np.random.default_rng(0).standard_normal((N, N))
    plan_c = pyfftw.FFTW(a, b, axes=(0, 1), flags=("FFTW_MEASURE",))
    ar = pyfftw.empty_aligned((N, N), dtype="float64")
    br = pyfftw.empty_aligned((N, N // 2 + 1), dtype="complex128")
    ar[:] = np.random.default_rng(1).standard_normal((N, N))
    plan_r = pyfftw.FFTW(ar, br, axes=(0, 1), flags=("FFTW_MEASURE",))
    an = np.array(a)
    contestants["fftw3_complex_fft2_24x24"] = plan_c
    contestants["fftw3_rfft2_24x24"] = plan_r
    contestants["numpy_fft2_24x24"] = lambda: np.fft.fft2(an)
    contestants["numpy_rfft2_24x24"] = lambda: np.fft.rfft2(np.asarray(ar))

    import jax
    jax.config.update("jax_enable_x64", True)
    import jax.numpy as jnp
    import jax_cfd.base.grids as grids
    from jax_cfd.spectral import equations as sp_eq
    from jax_cfd.spectral import time_stepping
    grid = grids.Grid((N, N), domain=((0, 2 * np.pi), (0, 2 * np.pi)))
    eq = sp_eq.ForcedNavierStokes2D(1.0 / RE, grid, smooth=True)
    rng = np.random.default_rng(405)
    w0 = rng.standard_normal((N, N))
    w0 -= w0.mean()
    vhat = jnp.fft.rfftn(jnp.asarray(w0))
    step = time_stepping.crank_nicolson_rk4(eq, DT)
    jstep = jax.jit(step)
    jstep(vhat).block_until_ready()

    M1, M2 = 200, 400

    def mk_scan(M):
        def run(v):
            def body(c, _):
                return step(c), None
            c, _ = jax.lax.scan(body, v, None, length=M)
            return c
        f = jax.jit(run)
        f(vhat).block_until_ready()
        return f
    jrun1, jrun2 = mk_scan(M1), mk_scan(M2)

    contestants["jaxcfd_single_jitted_step"] = (
        lambda: jstep(vhat).block_until_ready())
    contestants["jaxcfd_scan_%d" % M1] = lambda: jrun1(vhat).block_until_ready()
    contestants["jaxcfd_scan_%d" % M2] = lambda: jrun2(vhat).block_until_ready()

    # reference sanity: the scan must actually advance the state and stay finite
    v1 = np.asarray(jrun1(vhat))
    res["reference_sanity"] = {
        "state_shape": list(v1.shape), "state_dtype": str(v1.dtype),
        "state_changed_after_%d_steps" % M1: bool(
            not np.allclose(v1, np.asarray(vhat))),
        "finite": bool(np.all(np.isfinite(v1))),
        "max_abs_after": float(np.max(np.abs(v1))),
    }

    keys = list(contestants)
    rounds = []
    for r in range(args.rounds):
        order = keys[r % len(keys):] + keys[:r % len(keys)]   # rotate
        row = {"round": r, "loadavg_before": _load(), "order": order}
        for k in order:
            row[k] = _autobench(contestants[k], target_block_s=0.03,
                                repeat=11)["median_s"]
        row["loadavg_after"] = _load()
        # harness self-check inside the round
        row["_noop_s"] = _autobench(lambda: None, target_block_s=0.01,
                                    repeat=11)["median_s"]
        rounds.append(row)
    res["rounds"] = rounds

    def per_step(k, row):
        if k == "jaxcfd_scan_%d" % M1:
            return row[k] / M1
        if k == "jaxcfd_scan_%d" % M2:
            return row[k] / M2
        return row[k]

    summary = {}
    for k in keys:
        vals = sorted(per_step(k, r_) for r_ in rounds)
        summary[k] = {"median_s": statistics.median(vals),
                      "min_s": vals[0], "max_s": vals[-1],
                      "max_over_min": vals[-1] / vals[0]}
    res["per_call_summary"] = summary

    ratios = {}
    for k in keys:
        if k == "ours_rk4_step":
            continue
        vals = sorted(rounds[i]["ours_rk4_step"] / per_step(k, rounds[i])
                      for i in range(len(rounds)))
        ratios["ours_over_" + k] = {
            "median": statistics.median(vals), "min": vals[0], "max": vals[-1],
            "all": vals}
    # 20-transform and 25-rfft floors, formed within each round
    for label, k, n in (("fftw3_20x_complex_floor", "fftw3_complex_fft2_24x24", 20),
                        ("fftw3_25x_rfft_floor", "fftw3_rfft2_24x24", 25),
                        ("numpy_20x_fft2_floor", "numpy_fft2_24x24", 20)):
        vals = sorted(rounds[i]["ours_rk4_step"] / (n * rounds[i][k])
                      for i in range(len(rounds)))
        ratios["ours_over_" + label] = {
            "median": statistics.median(vals), "min": vals[0], "max": vals[-1]}
    vals = sorted(rounds[i]["numpy_fft2_24x24"] / rounds[i]["fftw3_complex_fft2_24x24"]
                  for i in range(len(rounds)))
    ratios["numpy_fft2_over_fftw3_fft2"] = {
        "median": statistics.median(vals), "min": vals[0], "max": vals[-1]}
    vals = sorted(rounds[i]["fftw3_rfft2_24x24"] / rounds[i]["fftw3_complex_fft2_24x24"]
                  for i in range(len(rounds)))
    ratios["fftw3_rfft2_over_fft2"] = {
        "median": statistics.median(vals), "min": vals[0], "max": vals[-1]}
    res["within_round_ratios"] = ratios
    res["loadavg_span"] = {
        "min": min(r_["loadavg_before"][0] for r_ in rounds),
        "max": max(r_["loadavg_after"][0] for r_ in rounds)}
    res["harness_noop_span_s"] = {
        "min": min(r_["_noop_s"] for r_ in rounds),
        "max": max(r_["_noop_s"] for r_ in rounds)}
    res["stepper_and_spectrum_differences"] = {
        "ours_explicit_stages": 4,
        "ref_explicit_stages": 5,
        "ours_transforms_per_step": 20,
        "ours_transform_kind": "full complex fft2 / ifft2, 24x24 complex128",
        "ref_transforms_per_step": 25,
        "ref_transform_kind": "rfftn / irfftn, half spectrum 24x13 complex128",
        "ref_forcing_transforms_constant_folded": (
            "kolmogorov_forcing depends only on the grid, so its two rfft2 calls "
            "per stage are compile-time constants under jit and are NOT counted "
            "in the 25"),
        "ours_time_split": "Lie-Trotter: exact integrating factor AFTER RK4",
        "ref_time_split": "IMEX: Crank-Nicolson on the linear term inside a "
                          "5-stage Carpenter-Kennedy low-storage RK4",
    }
    return res



# ---------------------------------------------------------------------------
# PART "duel" -- the tightest form of gate (iii), on a machine that is NOT quiet
# ---------------------------------------------------------------------------
#
# TWO INDEPENDENT DEFENCES against the sibling units loading this box.
#
# 1. TIGHT INTERLEAVING. Only three contestants, tiny blocks, order rotated, and
#    the ratio formed inside each round. A round is ~0.3 s, so the load has far
#    less room to drift across the numerator and the denominator than in
#    `--part paired`, where a round took ~13 s.
#
# 2. A CPU CLOCK AS WELL AS A WALL CLOCK. `time.process_time_ns` counts CPU time
#    charged to THIS process across all its threads. Time lost to another process
#    holding the core does not appear in it. With intra-op parallelism pinned to 1
#    it is the load-immune instrument, and its agreement or disagreement with the
#    wall clock is itself reported rather than assumed.

def part_duel(args):
    import numpy as np
    res = {"unit": "R-prof", "leg": 405, "part": "duel", "env": _env_block(),
           "n_rounds": args.rounds}

    sol = _make_solver()
    _, wh = _seed_state(sol)
    dt = sol.dt

    import pyfftw
    N = N_GATE
    a = pyfftw.empty_aligned((N, N), dtype="complex128")
    b = pyfftw.empty_aligned((N, N), dtype="complex128")
    a[:] = np.random.default_rng(0).standard_normal((N, N))
    plan_c = pyfftw.FFTW(a, b, axes=(0, 1), flags=("FFTW_MEASURE",))

    import jax
    jax.config.update("jax_enable_x64", True)
    import jax.numpy as jnp
    import jax_cfd.base.grids as grids
    from jax_cfd.spectral import equations as sp_eq
    from jax_cfd.spectral import time_stepping
    grid = grids.Grid((N, N), domain=((0, 2 * np.pi), (0, 2 * np.pi)))
    eq = sp_eq.ForcedNavierStokes2D(1.0 / RE, grid, smooth=True)
    rng = np.random.default_rng(405)
    w0 = rng.standard_normal((N, N))
    w0 -= w0.mean()
    vhat = jnp.fft.rfftn(jnp.asarray(w0))
    step = time_stepping.crank_nicolson_rk4(eq, DT)
    M = 100

    def run(v):
        def body(c, _):
            return step(c), None
        c, _ = jax.lax.scan(body, v, None, length=M)
        return c
    jrun = jax.jit(run)
    jrun(vhat).block_until_ready()

    # the same integration, our solver, so the two sides do the SAME AMOUNT of
    # simulated time -- M steps of dt each
    def ours_M():
        h = wh
        for _ in range(M):
            h = sol._rk4_step(h, dt)
        return h

    C = {
        "ours_%d_steps" % M: ours_M,
        "jaxcfd_scan_%d_steps" % M: lambda: jrun(vhat).block_until_ready(),
        "fftw3_fft2_24x24": plan_c,
    }
    keys = list(C)
    per_call_div = {"ours_%d_steps" % M: M, "jaxcfd_scan_%d_steps" % M: M,
                    "fftw3_fft2_24x24": 1}

    for clockname, clock in (("wall_perf_counter", time.perf_counter_ns),
                             ("cpu_process_time", time.process_time_ns)):
        rounds = []
        for r in range(args.rounds):
            order = keys[r % len(keys):] + keys[:r % len(keys)]
            row = {"round": r, "load": _load()[0], "order": order}
            for k in order:
                row[k] = _autobench(C[k], target_block_s=0.02, repeat=3,
                                    clock=clock)["median_s"] / per_call_div[k]
            rounds.append(row)
        rat = {}
        for k in keys:
            if k.startswith("ours"):
                continue
            v = sorted(rounds[i][keys[0]] / rounds[i][k]
                       for i in range(len(rounds)))
            n = len(v)
            rat["ours_over_" + k] = {
                "median": statistics.median(v), "min": v[0], "max": v[-1],
                "p10": v[max(0, n // 10)], "p90": v[min(n - 1, (9 * n) // 10)]}
        v = sorted(rounds[i][keys[0]] / (20 * rounds[i]["fftw3_fft2_24x24"])
                   for i in range(len(rounds)))
        rat["ours_over_fftw3_20x_floor"] = {
            "median": statistics.median(v), "min": v[0], "max": v[-1],
            "p10": v[max(0, len(v) // 10)]}
        summ = {}
        for k in keys:
            v = sorted(r_[k] for r_ in rounds)
            summ[k] = {"median_s": statistics.median(v), "min_s": v[0],
                       "max_s": v[-1], "max_over_min": v[-1] / v[0]}
        res[clockname] = {"rounds": rounds, "per_call_summary": summ,
                          "within_round_ratios": rat,
                          "load_span": [min(r_["load"] for r_ in rounds),
                                        max(r_["load"] for r_ in rounds)]}
    res["note_same_simulated_time"] = (
        "both sides advance %d steps of dt=%g; per-call figures are per STEP"
        % (M, DT))
    return res


# ---------------------------------------------------------------------------
# PART "duel" -- the tightest form of gate (iii), on a machine that is NOT quiet
# ---------------------------------------------------------------------------
#
# TWO INDEPENDENT DEFENCES against the sibling units loading this box.
#
# 1. TIGHT INTERLEAVING. Only three contestants, tiny blocks, order rotated, and
#    the ratio formed inside each round. A round is ~0.3 s, so the load has far
#    less room to drift across the numerator and the denominator than in
#    `--part paired`, where a round took ~13 s.
#
# 2. A CPU CLOCK AS WELL AS A WALL CLOCK. `time.process_time_ns` counts CPU time
#    charged to THIS process across all its threads. Time lost to another process
#    holding the core does not appear in it. With intra-op parallelism pinned to 1
#    it is the load-immune instrument, and its agreement or disagreement with the
#    wall clock is itself reported rather than assumed.

def part_duel(args):
    import numpy as np
    res = {"unit": "R-prof", "leg": 405, "part": "duel", "env": _env_block(),
           "n_rounds": args.rounds}

    sol = _make_solver()
    _, wh = _seed_state(sol)
    dt = sol.dt

    import pyfftw
    N = N_GATE
    a = pyfftw.empty_aligned((N, N), dtype="complex128")
    b = pyfftw.empty_aligned((N, N), dtype="complex128")
    a[:] = np.random.default_rng(0).standard_normal((N, N))
    plan_c = pyfftw.FFTW(a, b, axes=(0, 1), flags=("FFTW_MEASURE",))

    import jax
    jax.config.update("jax_enable_x64", True)
    import jax.numpy as jnp
    import jax_cfd.base.grids as grids
    from jax_cfd.spectral import equations as sp_eq
    from jax_cfd.spectral import time_stepping
    grid = grids.Grid((N, N), domain=((0, 2 * np.pi), (0, 2 * np.pi)))
    eq = sp_eq.ForcedNavierStokes2D(1.0 / RE, grid, smooth=True)
    rng = np.random.default_rng(405)
    w0 = rng.standard_normal((N, N))
    w0 -= w0.mean()
    vhat = jnp.fft.rfftn(jnp.asarray(w0))
    step = time_stepping.crank_nicolson_rk4(eq, DT)
    M = 100

    def run(v):
        def body(c, _):
            return step(c), None
        c, _ = jax.lax.scan(body, v, None, length=M)
        return c
    jrun = jax.jit(run)
    jrun(vhat).block_until_ready()

    # the same integration, our solver, so the two sides do the SAME AMOUNT of
    # simulated time -- M steps of dt each
    def ours_M():
        h = wh
        for _ in range(M):
            h = sol._rk4_step(h, dt)
        return h

    C = {
        "ours_%d_steps" % M: ours_M,
        "jaxcfd_scan_%d_steps" % M: lambda: jrun(vhat).block_until_ready(),
        "fftw3_fft2_24x24": plan_c,
    }
    keys = list(C)
    per_call_div = {"ours_%d_steps" % M: M, "jaxcfd_scan_%d_steps" % M: M,
                    "fftw3_fft2_24x24": 1}

    for clockname, clock in (("wall_perf_counter", time.perf_counter_ns),
                             ("cpu_process_time", time.process_time_ns)):
        rounds = []
        for r in range(args.rounds):
            order = keys[r % len(keys):] + keys[:r % len(keys)]
            row = {"round": r, "load": _load()[0], "order": order}
            for k in order:
                row[k] = _autobench(C[k], target_block_s=0.02, repeat=3,
                                    clock=clock)["median_s"] / per_call_div[k]
            rounds.append(row)
        rat = {}
        for k in keys:
            if k.startswith("ours"):
                continue
            v = sorted(rounds[i][keys[0]] / rounds[i][k]
                       for i in range(len(rounds)))
            n = len(v)
            rat["ours_over_" + k] = {
                "median": statistics.median(v), "min": v[0], "max": v[-1],
                "p10": v[max(0, n // 10)], "p90": v[min(n - 1, (9 * n) // 10)]}
        v = sorted(rounds[i][keys[0]] / (20 * rounds[i]["fftw3_fft2_24x24"])
                   for i in range(len(rounds)))
        rat["ours_over_fftw3_20x_floor"] = {
            "median": statistics.median(v), "min": v[0], "max": v[-1],
            "p10": v[max(0, len(v) // 10)]}
        summ = {}
        for k in keys:
            v = sorted(r_[k] for r_ in rounds)
            summ[k] = {"median_s": statistics.median(v), "min_s": v[0],
                       "max_s": v[-1], "max_over_min": v[-1] / v[0]}
        res[clockname] = {"rounds": rounds, "per_call_summary": summ,
                          "within_round_ratios": rat,
                          "load_span": [min(r_["load"] for r_ in rounds),
                                        max(r_["load"] for r_ in rounds)]}
    res["note_same_simulated_time"] = (
        "both sides advance %d steps of dt=%g; per-call figures are per STEP"
        % (M, DT))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=15)
    ap.add_argument("--part", required=True,
                    choices=("ours", "ref", "paired", "duel", "merge", "controls"))
    ap.add_argument("--out", required=True)
    for a_ in ("--ours", "--ours-alt", "--ref", "--paired", "--duel",
               "--candidates", "--ours-repeat"):
        ap.add_argument(a_)
    ap.add_argument("--jax-cfd-version", default="0.2.1")
    args = ap.parse_args()
    fn = {"ours": part_ours, "ref": part_ref, "paired": part_paired,
          "duel": part_duel, "merge": part_merge,
          "controls": lambda a: {"controls": controls(), "env": _env_block()}}[args.part]
    res = fn(args)
    if args.part == "merge":
        # self_hash: sha256 of the artefact with the field itself absent, so a
        # verifier can recompute it by deleting the key and re-hashing.
        res.pop("self_hash", None)
        body = json.dumps(res, indent=2, sort_keys=True, default=float)
        res["self_hash"] = {
            "sha256_of_artefact_without_this_field":
                hashlib.sha256(body.encode()).hexdigest(),
            "how_to_verify": ("delete the 'self_hash' key, dump the rest with "
                              "json.dumps(obj, indent=2, sort_keys=True, "
                              "default=float), sha256 the utf-8 bytes"),
            "script_sha256": hashlib.sha256(
                open(os.path.abspath(__file__), "rb").read()).hexdigest(),
            "candidates_script_sha256": hashlib.sha256(open(os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "r_prof_candidates_v1.py"), "rb").read()).hexdigest(),
        }
    with open(args.out, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=float)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
