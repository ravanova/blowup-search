"""PROG-R4 / `R-prof` (leg 405) -- PRICING THE SINGLE CHANGE. NOT A SOLVER REWRITE.

The gate's `NO` branch asks for "the FACTOR and the SINGLE change that recovers most
of it", and forbids rewriting the solver in this unit -- a stepper change invalidates
every banked comparison in the programme, which is exactly the `R4` problem.

So this file builds PROTOTYPES OUTSIDE THE SOLVER. It does not import-and-patch
`Kolmogorov2D`; it constructs standalone step functions with the SAME arithmetic and
the SAME scheme, checks each one against `Kolmogorov2D._rk4_step` to machine
precision on the same input, and times it in interleaved rounds against the original.

WHAT IT IS ALLOWED TO CONCLUDE: how much of the measured factor each candidate
recovers, at N=24, on this machine, on this input. NOTHING ELSE. A landed change
needs its own unit, its own equivalence check across the whole campaign, and a
statement about every banked orbit -- none of which is done here.

Candidates, all of them the SAME numerical scheme (classical RK4 on the non-stiff
part + the exact integrating factor applied after the step, 2/3-rule dealiasing):

  V0  baseline          -- `Kolmogorov2D._rk4_step` exactly as it stands
  V1  batched numpy     -- the four inverse transforms of a stage issued as ONE
                           `np.fft.ifft2(stack, axes=(1,2))` on a (4,N,N) array.
                           5 transform CALLS per stage become 2. No new dependency.
  V2  planned FFTW3     -- the same five transforms, but through pre-planned
                           `pyfftw.FFTW` objects on aligned buffers (row 24).
  V3  V1 + V2           -- batched AND planned: 2 planned calls per stage.

`--part duel` in `r_prof_v1.py` established the factor; this file establishes which
change recovers it.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import numpy as np                                                # noqa: E402
from r_prof_v1 import (DT, N_GATE, RE, _autobench, _load, _env_block,  # noqa: E402
                       _make_solver, _seed_state, controls)


# ---------------------------------------------------------------------------
# V1 -- batched numpy transforms
# ---------------------------------------------------------------------------

class V1Batched:
    def __init__(self, sol):
        self.s = sol
        N = sol.N
        self.stack = np.empty((4, N, N), dtype=np.complex128)

    def rhs(self, w_hat):
        s = self.s
        st = self.stack
        st[0] = 1j * s.KY * w_hat * s.inv_Ksq          # u_hat
        st[1] = -1j * s.KX * w_hat * s.inv_Ksq         # v_hat
        st[2] = 1j * s.KX * w_hat                      # d(omega)/dx spectral
        st[3] = 1j * s.KY * w_hat                      # d(omega)/dy spectral
        p = np.fft.ifft2(st, axes=(1, 2)).real
        adv_hat = np.fft.fft2(p[0] * p[2] + p[1] * p[3]) * s.mask
        return -adv_hat + s.forcing_hat

    def step(self, w_hat, dt):
        s = self.s
        decay = s.decay if dt == s.dt else np.exp(-s.Ksq / s.Re * dt)
        k1 = self.rhs(w_hat)
        k2 = self.rhs(w_hat + 0.5 * dt * k1)
        k3 = self.rhs(w_hat + 0.5 * dt * k2)
        k4 = self.rhs(w_hat + dt * k3)
        return (w_hat + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)) * decay


# ---------------------------------------------------------------------------
# V2 -- planned FFTW3 transforms, one plan per call site
# ---------------------------------------------------------------------------

class V2Fftw:
    def __init__(self, sol, flags=("FFTW_MEASURE",)):
        import pyfftw
        self.s = sol
        N = sol.N
        self.bi_in = pyfftw.empty_aligned((N, N), dtype="complex128")
        self.bi_out = pyfftw.empty_aligned((N, N), dtype="complex128")
        self.p_inv = pyfftw.FFTW(self.bi_in, self.bi_out, axes=(0, 1),
                                 direction="FFTW_BACKWARD", flags=flags)
        self.bf_in = pyfftw.empty_aligned((N, N), dtype="complex128")
        self.bf_out = pyfftw.empty_aligned((N, N), dtype="complex128")
        self.p_fwd = pyfftw.FFTW(self.bf_in, self.bf_out, axes=(0, 1),
                                 direction="FFTW_FORWARD", flags=flags)

    def _inv_real(self, arr):
        self.bi_in[:] = arr
        self.p_inv()
        return self.bi_out.real.copy()

    def rhs(self, w_hat):
        s = self.s
        u = self._inv_real(1j * s.KY * w_hat * s.inv_Ksq)
        v = self._inv_real(-1j * s.KX * w_hat * s.inv_Ksq)
        wx = self._inv_real(1j * s.KX * w_hat)
        wy = self._inv_real(1j * s.KY * w_hat)
        self.bf_in[:] = u * wx + v * wy
        self.p_fwd()
        return -(self.bf_out * s.mask) + s.forcing_hat

    def step(self, w_hat, dt):
        s = self.s
        decay = s.decay if dt == s.dt else np.exp(-s.Ksq / s.Re * dt)
        k1 = self.rhs(w_hat)
        k2 = self.rhs(w_hat + 0.5 * dt * k1)
        k3 = self.rhs(w_hat + 0.5 * dt * k2)
        k4 = self.rhs(w_hat + dt * k3)
        return (w_hat + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)) * decay


# ---------------------------------------------------------------------------
# V3 -- batched AND planned
# ---------------------------------------------------------------------------

class V3Both:
    def __init__(self, sol, flags=("FFTW_MEASURE",)):
        import pyfftw
        self.s = sol
        N = sol.N
        self.st_in = pyfftw.empty_aligned((4, N, N), dtype="complex128")
        self.st_out = pyfftw.empty_aligned((4, N, N), dtype="complex128")
        self.p_inv = pyfftw.FFTW(self.st_in, self.st_out, axes=(1, 2),
                                 direction="FFTW_BACKWARD", flags=flags)
        self.bf_in = pyfftw.empty_aligned((N, N), dtype="complex128")
        self.bf_out = pyfftw.empty_aligned((N, N), dtype="complex128")
        self.p_fwd = pyfftw.FFTW(self.bf_in, self.bf_out, axes=(0, 1),
                                 direction="FFTW_FORWARD", flags=flags)

    def rhs(self, w_hat):
        s = self.s
        st = self.st_in
        st[0] = 1j * s.KY * w_hat * s.inv_Ksq
        st[1] = -1j * s.KX * w_hat * s.inv_Ksq
        st[2] = 1j * s.KX * w_hat
        st[3] = 1j * s.KY * w_hat
        self.p_inv()
        p = self.st_out.real
        self.bf_in[:] = p[0] * p[2] + p[1] * p[3]
        self.p_fwd()
        return -(self.bf_out * s.mask) + s.forcing_hat

    def step(self, w_hat, dt):
        s = self.s
        decay = s.decay if dt == s.dt else np.exp(-s.Ksq / s.Re * dt)
        k1 = self.rhs(w_hat)
        k2 = self.rhs(w_hat + 0.5 * dt * k1)
        k3 = self.rhs(w_hat + 0.5 * dt * k2)
        k4 = self.rhs(w_hat + dt * k3)
        return (w_hat + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)) * decay


# ---------------------------------------------------------------------------

def equivalence(sol, variants, w_hat, n_steps=200):
    """A candidate that is faster and WRONG is worth nothing. Each variant is
    checked (a) on a single step and (b) after 200 steps, against the solver's
    own output, in relative sup norm."""
    out = {}
    ref1 = sol._rk4_step(w_hat, sol.dt)
    h = w_hat.copy()
    for _ in range(n_steps):
        h = sol._rk4_step(h, sol.dt)
    refN = h
    for name, v in variants.items():
        a = v.step(w_hat, sol.dt)
        h = w_hat.copy()
        for _ in range(n_steps):
            h = v.step(h, sol.dt)
        out[name] = {
            "rel_sup_err_1_step": float(np.max(np.abs(a - ref1))
                                        / max(np.max(np.abs(ref1)), 1e-300)),
            "rel_sup_err_%d_steps" % n_steps: float(
                np.max(np.abs(h - refN)) / max(np.max(np.abs(refN)), 1e-300)),
            "bitwise_identical_1_step": bool(np.array_equal(a, ref1)),
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=40)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sol = _make_solver()
    _, wh = _seed_state(sol)
    dt = sol.dt

    variants = {"V1_batched_numpy": V1Batched(sol)}
    fftw_ok = True
    try:
        variants["V2_planned_fftw3"] = V2Fftw(sol)
        variants["V3_batched_and_planned"] = V3Both(sol)
    except Exception as exc:                                    # pragma: no cover
        fftw_ok = False
        fftw_err = repr(exc)

    res = {"unit": "R-prof", "leg": 405, "part": "candidates",
           "env": _env_block(), "controls": controls(),
           "fftw_available": fftw_ok,
           "N": N_GATE, "Re": RE, "dt": DT,
           "what_this_is_not": (
               "NOT a solver change. Prototypes built beside the solver and "
               "priced. Landing any of them is a separate unit with its own "
               "equivalence check over every banked orbit.")}
    if not fftw_ok:
        res["fftw_error"] = fftw_err
    res["equivalence_vs_Kolmogorov2D_rk4_step"] = equivalence(sol, variants, wh)

    C = {"V0_baseline_solver": lambda: sol._rk4_step(wh, dt)}
    for name, v in variants.items():
        C[name] = (lambda vv: (lambda: vv.step(wh, dt)))(v)
    keys = list(C)

    for clockname, clock in (("wall_perf_counter", time.perf_counter_ns),
                             ("cpu_process_time", time.process_time_ns)):
        rounds = []
        for r in range(args.rounds):
            order = keys[r % len(keys):] + keys[:r % len(keys)]
            row = {"round": r, "load": _load()[0]}
            for k in order:
                row[k] = _autobench(C[k], target_block_s=0.02, repeat=3,
                                    clock=clock)["median_s"]
            rounds.append(row)
        summ, spd = {}, {}
        for k in keys:
            vals = sorted(r_[k] for r_ in rounds)
            summ[k] = {"median_s": statistics.median(vals), "min_s": vals[0],
                       "max_s": vals[-1]}
            if k != "V0_baseline_solver":
                sp = sorted(r_["V0_baseline_solver"] / r_[k] for r_ in rounds)
                spd["speedup_" + k] = {
                    "median": statistics.median(sp), "min": sp[0], "max": sp[-1],
                    "p10": sp[max(0, len(sp) // 10)]}
        res[clockname] = {"per_call_summary": summ,
                          "within_round_speedups": spd,
                          "load_span": [min(r_["load"] for r_ in rounds),
                                        max(r_["load"] for r_ in rounds)],
                          "rounds": rounds}
    with open(args.out, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=float)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
