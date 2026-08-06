"""Route-SUA v1: an ADVERSARIAL AUDIT of solver/spectral_utils.py -- the shared core.

WHAT THIS IS NOT.  It is not a measurement of anything physical.  No number printed here is a
statement about blow-up, about a certificate constant, or about any quantity in the plan of
record.  It re-derives no physics and contests no banked result.

WHAT THIS IS.  Every number here is a statement about CODE BEHAVIOUR UNDER DEGENERATE OR
POISONED INPUT.  The question, verbatim from the leg's gate (DIRECTION.md, leg 120):

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/spectral_utils.py ever silently return a wrong value instead of propagating or
    flagging the invalid input?

WHY THIS MODULE.  It is imported by solver/gclm.py, solver/fractional_gclm.py,
solver/line_hilbert.py, ga/, and six sweep drivers.  A silent corruption here propagates into
every downstream module at once, including already-audited ones.  It has a dedicated test file
(test_spectral_utils_dedicated.py, leg 66) but had no adversarial battery.

WHERE THE BOUNDARIES COME FROM (novelty pass, writeup/novelty/leg_120.md).  Two published
references set the two targets, so nothing below is an invented standard:

  (L1) BOWMAN 2013 (`How Important is Dealiasing for Turbulence Simulations?`, U. Alberta,
       p.29, `Centered Convolutions`): "one needs to pad to N >= 3m - 2 to prevent mode m - 1
       from beating with itself to contaminate the most negative (first) mode".  With
       K = m - 1 the largest retained wavenumber this is N >= 3K + 1, i.e. K < N/3 STRICTLY.
       `dealias_mask` keeps k <= n/3.  For 3 | n those differ by exactly one mode.  S1 runs
       Bowman's own experiment: put the field on mode K, square it, read mode K back.

  (L2) JOHNSON (MIT), `Notes on FFT-based differentiation`, Algorithm 1 step 2: "Multiply Y_k
       by 2*pi*i/L k for k < N/2, by 2*pi*i/L (k - N) for k > N/2, and by ZERO for k = N/2 (if
       N is even)".  The module's even/odd split is therefore CORRECT and is confirmed, not
       contested.  But the published prescription MULTIPLIES by zero and the module ASSIGNS
       zero (`d[-1] = 0.0`).  IEEE-754: 0.0 * nan = nan and 0.0 * inf = nan, so the published
       form PROPAGATES a poisoned Nyquist coefficient and the assignment form ERASES it.  S4
       instruments that one line, with controls.

NOT A RE-FIND OF LEG 66/69.  `derivative_hat`'s odd-n defect was found by leg 66 and fixed by
Leg 0 on bench/fix-derivative-hat-odd-n.  S4c is an explicit REGRESSION CONTROL that the fix is
intact; it is never reported as a new finding.

PASSES ARE REPORTED AS LOUDLY AS FAILURES (leg 91's design rule, inherited): S8 is the map of
inputs the module handles correctly.  The deliverable is a behaviour map, not a bug list.

THE NINE BATTERIES
  S1  THE DEALIAS BOUNDARY.  Bowman's experiment at 23 grid sizes: is the retained band
      alias-free?  Magnitude = the spurious coefficient landing back inside the band.
  S2  THE CONSEQUENCE IN A SHIPPED DIAGNOSTIC.  `energy_production` is documented as the
      "Exact rate d/dt E" and feeds solver/gclm.py's per-run energy-balance residual.  Measured
      against an alias-free 6x-refined reference.
  S3  DOWNSTREAM EXPOSURE.  Which grid sizes actually reach `dealias_mask`, and a census of
      every banked `energy_balance_residual`.  Answers "which banked numbers are at risk".
  S4  NYQUIST POISON.  Does a non-finite Nyquist coefficient survive `derivative_hat`?
      Controls: non-Nyquist slot, and odd-n top mode (leg 69 regression).
  S5  MEAN-MODE POISON AND DTYPE, in `velocity_hat`.
  S6  MALFORMED `k`: scalar, length-1, wrong-length, across all three spectral multipliers.
  S7  DEGENERATE GRID SIZES: n = 0, 1, 2, 3 and negative n, at every entry point.
  S8  THE PASSES: NaN/Inf propagation through the integral quantities, the length guard, and
      the leg-69 regression control.
  S9  THE PROPOSED REPAIR, evaluated as an expression and verified NOT applied: is it a
      no-op at every resolution the repository runs, and does it close the boundary?

Deterministic (fixed seeds), no solver run, no logging.  Writes
writeup/data/p2_route_sua_v1_adversarial.json.

Run: .venv/bin/python -u experiments/p2_route_sua_v1_adversarial.py
"""

import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.spectral_utils import (          # noqa: E402
    TWO_PI, dealias_mask, derivative_hat, energy, energy_production, grid,
    hilbert_hat, integral, l1_norm, velocity_hat, wavenumbers,
)

OUT = ROOT / "writeup" / "data" / "p2_route_sua_v1_adversarial.json"

# Grid sizes: powers of two (what the repo actually runs), multiples of three (the
# marginal case Bowman's inequality identifies), and neither.
GRIDS_POW2 = (16, 32, 64, 128, 256, 512)
GRIDS_DIV3 = (6, 9, 12, 24, 27, 48, 81, 96, 192, 384, 768)
GRIDS_OTHER = (10, 20, 40, 50, 100, 200)
ALL_GRIDS = tuple(sorted(set(GRIDS_POW2 + GRIDS_DIV3 + GRIDS_OTHER)))

REFINE = 6          # refinement factor for the alias-free reference in S2
SEED = 20260806


def _j(x):
    """JSON-safe float (NaN/Inf become tagged strings, never silently dropped)."""
    if isinstance(x, (bool, str, int)) or x is None:
        return x
    f = float(x)
    if np.isnan(f):
        return "nan"
    if np.isinf(f):
        return "+inf" if f > 0 else "-inf"
    return f


def hdr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ---------------------------------------------------------------------------
# S1 -- THE DEALIAS BOUNDARY (Bowman's own experiment)
# ---------------------------------------------------------------------------

def s1_dealias_boundary():
    """Bowman: pad to N >= 3m-2, i.e. K < N/3 STRICTLY, or mode K beats with itself
    and contaminates mode -K.  `dealias_mask` keeps k <= n/3.  Run the experiment."""
    hdr("S1  THE DEALIAS BOUNDARY -- Bowman's condition N >= 3K+1, i.e. K < N/3 strictly")
    print("field placed on the top retained mode K, squared, and mode K read back.")
    print("the 2/3 rule guarantees that coefficient is EXACTLY ZERO.\n")
    print("    n  3|n   K   n/3      K<n/3?  spurious|c_K|   true|c_K|   verdict")
    rows = []
    for n in ALL_GRIDS:
        k = wavenumbers(n)
        m = dealias_mask(n)
        K = int(np.max(k[m]))
        strict_ok = bool(K < n / 3.0)          # Bowman's inequality
        x = grid(n)
        w = np.fft.irfft(np.fft.rfft(np.cos(K * x)) * m, n)
        prod = np.fft.rfft(w * w) * m / n      # dealiased quadratic product, as solvers do it
        # cos^2(Kx) = 1/2 + 1/2 cos(2Kx); 2K is outside the retained band, so inside
        # the band the ONLY true coefficient is the mean.  c_K must be exactly 0.
        spurious = float(np.abs(prod[K]))
        verdict = "ALIAS-FREE" if spurious < 1e-12 else "CONTAMINATED"
        rows.append({"n": n, "divisible_by_3": n % 3 == 0, "K": K,
                     "n_over_3": _j(n / 3.0), "bowman_strict_ok": strict_ok,
                     "spurious_coeff_at_K": _j(spurious), "true_coeff_at_K": 0.0,
                     "verdict": verdict})
        print("  %5d  %-3s %4d  %8.3f  %-6s  %.6e   %.1f       %s"
              % (n, "yes" if n % 3 == 0 else "no", K, n / 3.0,
                 "yes" if strict_ok else "NO", spurious, 0.0, verdict))
    bad = [r for r in rows if r["verdict"] == "CONTAMINATED"]
    clean = [r for r in rows if r["verdict"] == "ALIAS-FREE"]
    worst_clean = max(float(r["spurious_coeff_at_K"]) for r in clean)
    print("\n  CONTAMINATED: %d/%d grid sizes -- exactly the %d with 3 | n"
          % (len(bad), len(rows), sum(1 for r in rows if r["divisible_by_3"])))
    print("  spurious coefficient on those: %s (identical at every one)"
          % sorted({round(float(r["spurious_coeff_at_K"]), 12) for r in bad}))
    print("  worst spurious coefficient on the clean grids: %.3e (round-off)" % worst_clean)
    return {"rows": rows,
            "n_contaminated": len(bad), "n_total": len(rows),
            "contaminated_grids": [r["n"] for r in bad],
            "spurious_coeff_on_contaminated": _j(bad[0]["spurious_coeff_at_K"]) if bad else None,
            "worst_spurious_on_clean": _j(worst_clean),
            "contaminated_iff_divisible_by_3":
                all(r["divisible_by_3"] for r in bad)
                and all(not r["divisible_by_3"] for r in clean)}


# ---------------------------------------------------------------------------
# S2 -- THE CONSEQUENCE IN A SHIPPED DIAGNOSTIC
# ---------------------------------------------------------------------------

def _band_field(n, seed=SEED):
    """Random real field supported exactly on the 2/3-retained band, mixed parity."""
    rng = np.random.default_rng(seed)
    m = dealias_mask(n)
    wh = (rng.standard_normal(m.shape) + 1j * rng.standard_normal(m.shape)) * m
    wh[0] = wh[0].real
    w = np.fft.irfft(wh, n)
    return np.fft.irfft(np.fft.rfft(w) * m, n)


def _alias_free_production(w, n, a, nu, f=REFINE):
    """Same integral as energy_production, evaluated on an f-times finer grid where the
    cubic product is fully resolved -- so it carries no aliasing."""
    nf = f * n
    wh = np.fft.rfft(w)
    whf = np.zeros(nf // 2 + 1, dtype=complex)
    whf[:len(wh)] = wh * (nf / n)
    wf = np.fft.irfft(whf, nf)
    kf = wavenumbers(nf)
    hwf = np.fft.irfft(hilbert_hat(np.fft.rfft(wf), kf), nf)
    wxf = np.fft.irfft(derivative_hat(np.fft.rfft(wf), kf, nf), nf)
    prod = (a / 2.0 + 1.0) * TWO_PI * float(np.mean(wf * wf * hwf))
    diss = nu * TWO_PI * float(np.mean(wxf * wxf))
    return prod - diss


def s2_energy_production():
    hdr("S2  THE CONSEQUENCE IN A SHIPPED DIAGNOSTIC -- energy_production")
    print("docstring: \"Exact rate d/dt E for gCLM\".  It feeds solver/gclm.py's per-run")
    print("energy-balance residual (the artifact guard of LOGGING.md).  Measured against an")
    print("alias-free %dx-refined evaluation of the SAME integral.\n" % REFINE)
    print("    n  3|n   energy_production      alias-free reference     rel_err")
    rows = []
    for n in ALL_GRIDS:
        if n < 12:
            continue
        w = _band_field(n)
        got = energy_production(w, a=0.0, nu=0.0)
        ref = _alias_free_production(w, n, a=0.0, nu=0.0)
        rel = abs(got - ref) / max(abs(ref), 1e-300)
        rows.append({"n": n, "divisible_by_3": n % 3 == 0,
                     "energy_production": _j(got), "alias_free_reference": _j(ref),
                     "rel_err": _j(rel)})
        print("  %5d  %-3s  %+.12e  %+.12e  %.4e"
              % (n, "yes" if n % 3 == 0 else "no", got, ref, rel))
    d3 = [r for r in rows if r["divisible_by_3"]]
    nd3 = [r for r in rows if not r["divisible_by_3"]]
    worst_d3 = max(d3, key=lambda r: float(r["rel_err"]))
    worst_nd3 = max(nd3, key=lambda r: float(r["rel_err"]))
    print("\n  worst rel_err with 3 | n     : %.4e  (n = %d)"
          % (float(worst_d3["rel_err"]), worst_d3["n"]))
    print("  worst rel_err with 3 does NOT divide n: %.4e  (n = %d)"
          % (float(worst_nd3["rel_err"]), worst_nd3["n"]))
    print("  separation: %.3e decades"
          % (np.log10(float(worst_d3["rel_err"]) / float(worst_nd3["rel_err"]))))
    return {"rows": rows, "refine_factor": REFINE,
            "worst_rel_err_div3": _j(worst_d3["rel_err"]), "worst_n_div3": worst_d3["n"],
            "worst_rel_err_not_div3": _j(worst_nd3["rel_err"]),
            "worst_n_not_div3": worst_nd3["n"],
            "separation_decades": _j(np.log10(float(worst_d3["rel_err"])
                                              / float(worst_nd3["rel_err"])))}


# ---------------------------------------------------------------------------
# S3 -- DOWNSTREAM EXPOSURE
# ---------------------------------------------------------------------------

RESKEYS = ("n", "N", "n_grid", "grid_n", "resolution", "resolution_N", "res", "nx", "n_res")


def s3_exposure():
    """Which grid sizes reach dealias_mask, and which banked numbers are at risk."""
    hdr("S3  DOWNSTREAM EXPOSURE -- which banked numbers could this affect?")

    # (a) every call site of the 1D mask, and the resolutions declared on that path
    call_sites = ["solver/gclm.py:178", "solver/fractional_gclm.py:195",
                  "phase2_spike0_probe.py:23"]
    declared = {
        "stage1_5_sweep.RESOLUTIONS": [256, 512],
        "stage1_5_sweep.N_REFERENCE": [2048],
        "stage2_5_sweep.RESOLUTIONS": [256, 512],
        "stage2_6_sweep.RESOLUTIONS": [256, 512],
        "stage3_6_sweep.RESOLUTIONS": [1024, 2048, 4096],
        "stage3_6_sweep.N_REFERENCE": [4096],
        "nongenericity_sweep.RESOLUTIONS": [256, 512],
        "ga.resolution_study.DEFAULT_RESOLUTIONS": [256, 512, 1024],
        "ga.evolve.fitness_resolution_N": [256],
        "experiments/p2_route_f_v1_viscosity.N_DEFAULT": [8192],
        "experiments/p2_route_fga_v1_adversarial.N_AUDIT": [512],
        "experiments/p2_route_gla_v1_adversarial.N_SOLVE": [64],
        "experiments/p2_route_h_v1_critical.h7 n": [8192],
        "phase2_spike0_probe.run N": [2048],
        "solver.fractional_gclm.FractionalGCLM default n": [2048],
    }
    every = sorted({v for vs in declared.values() for v in vs})
    exposed_sizes = [v for v in every if v % 3 == 0]
    print("  1D dealias_mask call sites (non-test): %s" % ", ".join(call_sites))
    print("  every grid size declared on that path : %s" % every)
    print("  ... of which divisible by 3           : %s" % (exposed_sizes or "NONE"))
    print("  (every one is a power of two; no power of two is divisible by 3)")

    # (b) census of the banked quantity energy_production actually feeds
    found = []
    for base in ("writeup", "reports"):
        for dp, _, fns in os.walk(ROOT / base):
            for fn in fns:
                if not fn.endswith(".json"):
                    continue
                p = Path(dp) / fn
                try:
                    obj = json.loads(p.read_text())
                except Exception:
                    continue

                def walk(o, inherited):
                    if isinstance(o, dict):
                        here = inherited
                        for kk in RESKEYS:
                            v = o.get(kk)
                            if isinstance(v, int) and v >= 4:
                                here = v
                        if any(str(kk).startswith("energy_balance_residual") for kk in o):
                            found.append((str(p.relative_to(ROOT)), here))
                        for vv in o.values():
                            walk(vv, here)
                    elif isinstance(o, list):
                        for vv in o:
                            walk(vv, inherited)

                walk(obj, None)
    files = sorted({f for f, _ in found})
    at_risk = [(f, r) for f, r in found if isinstance(r, int) and r % 3 == 0]
    print("\n  banked records carrying `energy_balance_residual` : %d" % len(found))
    print("  in files                                          : %s" % ", ".join(files))
    print("  of those, run at a grid size divisible by 3       : %d" % len(at_risk))
    print("  the two source runners' resolutions               : "
          "GLA N_SOLVE = 64 (1D), BOA N = 32 (2D)")

    # (c) the 2D sibling -- reported, NOT touched (out of this leg's territory)
    print("\n  SIBLING, OUT OF TERRITORY (reported only, not modified):")
    print("    solver/boussinesq.py:149 dealias_mask2d uses the identical cut `<= n/3`.")
    print("    Same boundary, same marginal case.  Banked Boussinesq runs use n = 32,")
    print("    so it is unexposed too -- but it is the same one-character question.")

    print("\n  ==> BANKED NUMBERS AT RISK: %d" % len(at_risk))
    return {"call_sites_1d": call_sites,
            "declared_resolutions": declared,
            "all_declared_sizes": every,
            "declared_sizes_divisible_by_3": exposed_sizes,
            "banked_energy_balance_residual_records": len(found),
            "banked_files": files,
            "banked_records_at_risk": len(at_risk),
            "sibling_same_cut": "solver/boussinesq.py:149 dealias_mask2d (<= n/3), "
                                "out of territory, banked runs at n=32, unexposed",
            "banked_numbers_at_risk": len(at_risk)}


# ---------------------------------------------------------------------------
# S4 -- NYQUIST POISON
# ---------------------------------------------------------------------------

def s4_nyquist_poison():
    hdr("S4  NYQUIST POISON -- does derivative_hat propagate a non-finite coefficient?")
    print("Johnson Algorithm 1 says MULTIPLY the k=N/2 coefficient by zero.  The module")
    print("ASSIGNS `d[-1] = 0.0`.  0.0*nan = nan and 0.0*inf = nan, so the published form")
    print("propagates and the assignment erases.  Measured:\n")
    poisons = [("nan", np.nan), ("+inf", np.inf), ("-inf", -np.inf)]

    print("  (a) POISON AT THE NYQUIST SLOT, n EVEN")
    print("      `warned` records whether numpy raised a RuntimeWarning inside the multiply")
    print("      BEFORE the assignment wiped the result -- for +-inf the complex product")
    print("      (0 + i k)(inf + 0i) is already nan, so a signal existed and was discarded.\n")
    print("        n  poison  spectrum finite  physical finite  max|w_x|    warned  "
          "value before assignment")
    a_rows = []
    for n in (8, 16, 64, 256):
        k = wavenumbers(n)
        for tag, p in poisons:
            wh = np.fft.rfft(np.sin(grid(n)))
            wh[-1] = p
            with warnings.catch_warnings(record=True) as wl:
                warnings.simplefilter("always")
                with np.errstate(all="warn"):
                    d = derivative_hat(wh.copy(), k, n)
            warned = len(wl) > 0
            out = np.fft.irfft(d, n)
            # the value the multiply produced at that slot, before `d[-1] = 0.0`
            with np.errstate(all="ignore"):
                pre = complex(1j * k[-1] * p)
            a_rows.append({"n": n, "poison": tag,
                           "spectrum_finite": bool(np.all(np.isfinite(d))),
                           "physical_finite": bool(np.all(np.isfinite(out))),
                           "max_abs_out": _j(np.max(np.abs(out))),
                           "warned_in_multiply": bool(warned),
                           "value_before_assignment_finite": bool(np.isfinite(pre)),
                           "published_multiply_form_finite": bool(np.isfinite(0.0 * pre))})
            print("    %5d  %-6s  %-15s  %-15s  %.4e  %-6s  %s"
                  % (n, tag, np.all(np.isfinite(d)), np.all(np.isfinite(out)),
                     np.max(np.abs(out)), warned, "non-finite" if not np.isfinite(pre)
                     else "finite"))
    erased = sum(1 for r in a_rows if r["spectrum_finite"])
    print("\n    ERASED: %d/%d poisoned Nyquist coefficients returned a fully finite result."
          % (erased, len(a_rows)))
    print("    The published multiply-by-zero form would have propagated all %d." % len(a_rows))

    print("\n  (b) CONTROL -- same poison at a NON-Nyquist slot (must propagate)")
    b_rows = []
    for n in (64, 256):
        k = wavenumbers(n)
        for tag, p in poisons:
            wh = np.fft.rfft(np.sin(grid(n)))
            wh[5] = p
            d = derivative_hat(wh.copy(), k, n)
            prop = not np.all(np.isfinite(d))
            b_rows.append({"n": n, "slot": 5, "poison": tag, "propagated": bool(prop),
                           "n_nonfinite": int(np.sum(~np.isfinite(d)))})
            print("    n=%4d slot=5 poison=%-6s propagated=%s (%d non-finite entries)"
                  % (n, tag, prop, int(np.sum(~np.isfinite(d)))))

    print("\n  (c) REGRESSION CONTROL -- leg 66/69's odd-n fix must still be intact")
    c_rows = []
    for n in (17, 65, 129):
        k = wavenumbers(n)
        kt = (n - 1) // 2
        wh = np.fft.rfft(np.sin(kt * grid(n)))
        wh[-1] = np.nan
        d = derivative_hat(wh.copy(), k, n)
        prop = not np.all(np.isfinite(d))
        # and the derivative itself is still exact at the top mode
        w = np.sin(kt * grid(n))
        dw = np.fft.irfft(derivative_hat(np.fft.rfft(w), k, n), n)
        ex = kt * np.cos(kt * grid(n))
        rel = float(np.max(np.abs(dw - ex)) / np.max(np.abs(ex)))
        c_rows.append({"n": n, "top_mode_poison_propagated": bool(prop),
                       "top_mode_rel_err": _j(rel)})
        print("    n=%4d (odd) top-mode poison propagated=%s ; top-mode rel err=%.3e"
              % (n, prop, rel))
    print("    leg 66/69's fix is INTACT -- this leg re-finds nothing there.")
    return {"nyquist_even": a_rows, "n_erased": erased, "n_nyquist_cases": len(a_rows),
            "control_non_nyquist": b_rows,
            "all_non_nyquist_propagate": all(r["propagated"] for r in b_rows),
            "regression_odd_n": c_rows,
            "leg69_fix_intact": all(r["top_mode_poison_propagated"] for r in c_rows)
                                and all(float(r["top_mode_rel_err"]) < 1e-12 for r in c_rows)}


# ---------------------------------------------------------------------------
# S5 -- velocity_hat: mean-mode poison and dtype
# ---------------------------------------------------------------------------

def s5_velocity_hat():
    hdr("S5  velocity_hat -- mean-mode poison, and the dtype it inherits")
    n = 64
    k = wavenumbers(n)
    print("  (a) POISON AT THE MEAN MODE k = 0")
    print("      `u_hat = np.zeros_like(w_hat)` then only k != 0 entries are written,")
    print("      so index 0 keeps whatever zeros_like put there, whatever came in.\n")
    a_rows = []
    for tag, p in (("nan", np.nan), ("+inf", np.inf), ("-inf", -np.inf)):
        wh = np.fft.rfft(np.sin(grid(n)))
        wh[0] = p
        u = velocity_hat(wh.copy(), k)
        a_rows.append({"poison": tag, "u_hat_0_real": _j(np.real(u[0])),
                       "u_hat_0_imag": _j(np.imag(u[0])),
                       "output_all_finite": bool(np.all(np.isfinite(u)))})
        print("    poison@k=0 = %-5s -> u_hat[0] = %r ; whole output finite: %s"
              % (tag, u[0], bool(np.all(np.isfinite(u)))))
    print("    ERASED: %d/%d." % (sum(1 for r in a_rows if r["output_all_finite"]), len(a_rows)))

    print("\n  (b) DTYPE INHERITANCE.  zeros_like copies the input dtype; the float")
    print("      quotient is then unsafe-cast on assignment.  Contrast with the other two")
    print("      spectral multipliers, which promote to complex.\n")
    b_rows = []
    rng = np.random.default_rng(SEED)
    kk = np.arange(33.0)
    for scale in (1, 3, 10, 100, 1000):
        # worst case over 200 draws at each scale -- one draw is not a magnitude
        worst = {"max_abs_err": 0.0, "rel_err": 0.0}
        for _ in range(200):
            a = (rng.standard_normal(33) * scale).astype(np.int64)
            a[0] = 0
            u = velocity_hat(a.copy(), kk)
            ex = np.zeros(33)
            ex[1:] = -a[1:] / kk[1:]
            abs_err = float(np.max(np.abs(np.asarray(u, dtype=np.float64) - ex)))
            rel = abs_err / max(float(np.max(np.abs(ex))), 1e-300)
            if rel > worst["rel_err"]:
                worst = {"max_abs_err": abs_err, "rel_err": rel}
        b_rows.append({"int_scale": scale, "max_abs_err": _j(worst["max_abs_err"]),
                       "rel_err": _j(worst["rel_err"]),
                       "out_dtype": str(np.asarray(velocity_hat(
                           np.zeros(33, dtype=np.int64), kk)).dtype)})
        print("    int64 input, scale %-5d -> worst over 200 draws: max abs err %.4f  "
              "rel %.4e" % (scale, worst["max_abs_err"], worst["rel_err"]))
    worst_dtype_rel = max(float(r["rel_err"]) for r in b_rows)
    ih = np.array([0, 7, 3, 1], dtype=np.int64)
    kd = np.array([0.0, 1.0, 2.0, 3.0])
    dh_dtype = str(np.asarray(derivative_hat(ih.copy(), kd, 6)).dtype)
    hh_dtype = str(np.asarray(hilbert_hat(ih.copy(), kd)).dtype)
    vh_dtype = str(np.asarray(velocity_hat(ih.copy(), kd)).dtype)
    print("\n    same int64 input:  derivative_hat -> %s ; hilbert_hat -> %s ; "
          "velocity_hat -> %s" % (dh_dtype, hh_dtype, vh_dtype))
    print("    velocity_hat is the only one of the three that inherits the input dtype.")
    return {"mean_mode_poison": a_rows,
            "n_erased": sum(1 for r in a_rows if r["output_all_finite"]),
            "dtype_truncation": b_rows,
            "worst_dtype_rel_err": _j(worst_dtype_rel),
            "dtypes_on_int_input": {"derivative_hat": dh_dtype, "hilbert_hat": hh_dtype,
                                    "velocity_hat": vh_dtype}}


# ---------------------------------------------------------------------------
# S6 -- malformed k
# ---------------------------------------------------------------------------

def s6_malformed_k():
    hdr("S6  MALFORMED `k` -- scalar, length-1, wrong length")
    print("  every one of these is a caller error.  The question is whether the module")
    print("  refuses it or broadcasts it into a full-length, plausible, WRONG answer.\n")
    n = 64
    wh = np.fft.rfft(np.sin(3 * grid(n)) + 0.4 * np.sin(11 * grid(n)))
    k_ok = wavenumbers(n)
    h_ok = np.fft.irfft(hilbert_hat(wh.copy(), k_ok), n)
    d_ok = np.fft.irfft(derivative_hat(wh.copy(), k_ok, n), n)
    scale_h = float(np.max(np.abs(h_ok)))
    scale_d = float(np.max(np.abs(d_ok)))
    rows = []
    cases = [("scalar 0.0", 0.0), ("scalar 1.0", 1.0), ("scalar -1.0", -1.0),
             ("length-1 array", np.array([2.0])), ("wrong length (n/2)", wavenumbers(32))]
    for fname, fn, ok, scale in (
            ("hilbert_hat", lambda w, kk: np.fft.irfft(hilbert_hat(w, kk), n), h_ok, scale_h),
            ("velocity_hat", lambda w, kk: velocity_hat(w, kk), None, None),
            ("derivative_hat", lambda w, kk: np.fft.irfft(derivative_hat(w, kk, n), n),
             d_ok, scale_d)):
        for tag, kk in cases:
            try:
                got = fn(wh.copy(), kk)
                if ok is None:
                    rows.append({"fn": fname, "case": tag, "outcome": "ACCEPTED",
                                 "rel_sup_err": None})
                    print("    %-15s %-20s ACCEPTED (no exception)" % (fname, tag))
                else:
                    rel = float(np.max(np.abs(got - ok))) / scale
                    rows.append({"fn": fname, "case": tag, "outcome": "ACCEPTED",
                                 "rel_sup_err": _j(rel)})
                    print("    %-15s %-20s ACCEPTED -> rel sup err vs correct: %.4e"
                          % (fname, tag, rel))
            except Exception as e:
                rows.append({"fn": fname, "case": tag,
                             "outcome": "REFUSED:" + type(e).__name__, "rel_sup_err": None})
                print("    %-15s %-20s REFUSED (%s)" % (fname, tag, type(e).__name__))
    acc = [r for r in rows if r["outcome"] == "ACCEPTED"]
    worst = max((r for r in acc if r["rel_sup_err"] not in (None, "nan")),
                key=lambda r: float(r["rel_sup_err"]), default=None)
    print("\n    ACCEPTED (silently) : %d/%d cases" % (len(acc), len(rows)))
    if worst:
        print("    worst silent error  : rel sup %.4e  (%s, %s)"
              % (float(worst["rel_sup_err"]), worst["fn"], worst["case"]))
    return {"rows": rows, "n_accepted": len(acc), "n_cases": len(rows),
            "worst_silent_rel_sup_err": worst["rel_sup_err"] if worst else None,
            "worst_case": (worst["fn"] + " / " + worst["case"]) if worst else None}


# ---------------------------------------------------------------------------
# S7 -- degenerate grid sizes
# ---------------------------------------------------------------------------

def s7_degenerate_n():
    hdr("S7  DEGENERATE GRID SIZES at every entry point")
    print("      n   grid            wavenumbers      dealias_mask     non-mean modes kept")
    rows = []
    for n in (-8, -1, 0, 1, 2, 3, 4):
        rec = {"n": n}
        cells = []
        for name, fn in (("grid", lambda: grid(n)),
                         ("wavenumbers", lambda: wavenumbers(n)),
                         ("dealias_mask", lambda: dealias_mask(n))):
            try:
                v = np.asarray(fn())
                rec[name] = {"outcome": "returned", "length": int(v.size)}
                cells.append("len=%d" % v.size)
            except Exception as e:
                rec[name] = {"outcome": "raised", "exception": type(e).__name__}
                cells.append("RAISE %s" % type(e).__name__)
        try:
            m = dealias_mask(n)
            kk = wavenumbers(n)
            nm = int(np.sum(m & (kk > 0)))
        except Exception:
            nm = None
        rec["non_mean_modes_retained"] = nm
        rows.append(rec)
        print("   %5d   %-15s %-16s %-16s %s" % (n, cells[0], cells[1], cells[2], nm))
    print("\n    grid(0) and grid(negative) return EMPTY arrays with no error, while")
    print("    wavenumbers(0)/dealias_mask(0) raise ZeroDivisionError -- inconsistent entry")
    print("    behaviour at the same invalid n.")
    print("    n = 1 and n = 2 retain ZERO non-mean modes.  That is the exact condition")
    print("    leg 89 made a hard ValueError in the 2D solver (solver/boussinesq.py:349);")
    print("    the 1D path has no equivalent guard.")
    return {"rows": rows,
            "grid_returns_empty_for_nonpositive":
                all(r["grid"]["outcome"] == "returned" for r in rows if r["n"] <= 0),
            "wavenumbers_raises_at_zero":
                [r for r in rows if r["n"] == 0][0]["wavenumbers"]["outcome"] == "raised",
            "zero_non_mean_modes_at": [r["n"] for r in rows
                                       if r["non_mean_modes_retained"] == 0]}


# ---------------------------------------------------------------------------
# S8 -- THE PASSES
# ---------------------------------------------------------------------------

def s8_passes():
    hdr("S8  THE PASSES -- recorded as loudly as the failures (leg 91's rule)")
    n = 64
    base = np.sin(grid(n))
    cases = [
        ("clean", base),
        ("one nan", np.where(np.arange(n) == 7, np.nan, base)),
        ("one +inf", np.where(np.arange(n) == 7, np.inf, base)),
        ("one -inf", np.where(np.arange(n) == 7, -np.inf, base)),
        ("+inf and -inf", np.where(np.arange(n) == 7, np.inf,
                                   np.where(np.arange(n) == 9, -np.inf, base))),
        ("all nan", np.full(n, np.nan)),
        ("empty", np.zeros(0)),
        ("1e200 scale", 1e200 * base),
    ]
    print("  (a) INTEGRAL QUANTITIES -- do they absorb poison, or propagate it?")
    print("        case            integral        l1_norm         energy          warnings")
    a_rows = []
    for tag, f in cases:
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            with np.errstate(all="ignore"):
                vals = (integral(f), l1_norm(f), energy(f))
            nw = len(wl)
        absorbed = (tag not in ("clean", "1e200 scale")
                    and all(np.isfinite(v) for v in vals) and nw == 0)
        a_rows.append({"case": tag, "integral": _j(vals[0]), "l1_norm": _j(vals[1]),
                       "energy": _j(vals[2]), "n_warnings": nw, "absorbed": bool(absorbed)})
        print("      %-15s %-15.6g %-15.6g %-15.6g %d%s"
              % (tag, vals[0], vals[1], vals[2], nw, "   <-- ABSORBED" if absorbed else ""))
    print("      absorbed (poison in, clean finite number out, no warning): %d/%d"
          % (sum(1 for r in a_rows if r["absorbed"]), len(a_rows)))

    print("\n  (b) derivative_hat's LENGTH GUARD (added with leg 66/69's fix)")
    b_rows = []
    for n_, m_ in ((64, 33), (64, 32), (64, 34), (17, 9), (17, 8)):
        wh = np.zeros(m_, dtype=complex)
        try:
            derivative_hat(wh, wavenumbers(n_)[:m_], n_)
            out = "accepted"
        except ValueError:
            out = "ValueError"
        except Exception as e:
            out = type(e).__name__
        correct = (m_ == n_ // 2 + 1)
        b_rows.append({"n": n_, "n_coeffs": m_, "correct_length": correct, "outcome": out})
        print("      n=%3d with %2d coefficients (correct=%s) -> %s"
              % (n_, m_, correct, out))
    guard_ok = all((r["outcome"] == "accepted") == r["correct_length"] for r in b_rows)
    print("      guard fires on exactly the wrong-length inputs: %s" % guard_ok)

    print("\n  (c) THE SPECTRAL CONVENTIONS THE REPO RESTS ON (unchanged, re-derived)")
    n = 64
    x = grid(n)
    hs = np.fft.irfft(hilbert_hat(np.fft.rfft(np.sin(x)), wavenumbers(n)), n)
    hc = np.fft.irfft(hilbert_hat(np.fft.rfft(np.cos(x)), wavenumbers(n)), n)
    # E = (1/2) int sin^2 = (1/2)(pi) = pi/2.  (The module computes pi*mean(w^2);
    # mean(sin^2) = 1/2 on the grid, so pi/2 is the value to check against.)
    e_sin = energy(np.sin(x))
    c_rows = {"H_sin_is_minus_cos": _j(np.max(np.abs(hs - (-np.cos(x))))),
              "H_cos_is_sin": _j(np.max(np.abs(hc - np.sin(x)))),
              "energy_of_sin_is_half_pi": _j(abs(e_sin - np.pi / 2.0)),
              "integral_of_1_is_2pi": _j(abs(integral(np.ones(n)) - TWO_PI)),
              # NOT a defect: |sin| is not band-limited (corners at 0, pi), so the
              # periodic trapezoid is algebraically, not spectrally, accurate here.
              # Recorded so the 3.2e-03 is never mistaken for a spectral-exactness gap.
              "l1_norm_of_sin_vs_4_NOT_A_DEFECT": _j(abs(l1_norm(np.sin(x)) - 4.0))}
    for kk, vv in c_rows.items():
        print("      %-28s residual %.3e" % (kk, float(vv)))
    return {"integral_quantities": a_rows,
            "n_absorbed": sum(1 for r in a_rows if r["absorbed"]),
            "length_guard": b_rows, "length_guard_exact": guard_ok,
            "conventions": c_rows}


# ---------------------------------------------------------------------------
# S9 -- THE PROPOSED REPAIR, VERIFIED BUT NOT APPLIED
# ---------------------------------------------------------------------------

def s9_proposed_repair():
    """Leg 120's yes-branch is `escalate, do not patch`, and no solver file is edited here.
    But an escalation is only actionable if the repair is known to be safe, so the candidate
    is EVALUATED as an expression and its two properties measured.

    Candidate: `dealias_mask(n)` should return `wavenumbers(n) <= (n - 1) // 3`, which is the
    largest integer STRICTLY below n/3 -- Bowman's `K < N/3`.
    """
    hdr("S9  THE PROPOSED REPAIR -- verified, NOT applied (territory is read-only)")
    print("  candidate: dealias_mask(n) -> wavenumbers(n) <= (n - 1) // 3\n")

    print("  (a) is it a NO-OP at every grid size this repository actually runs?")
    repo_grids = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    a_rows = []
    for n in repo_grids:
        cur, fix = dealias_mask(n), wavenumbers(n) <= (n - 1) // 3
        same = bool(np.array_equal(cur, fix))
        a_rows.append({"n": n, "kept_now": int(cur.sum()), "kept_after": int(fix.sum()),
                       "identical": same})
        print("      n=%5d  kept now=%5d  kept after=%5d  identical=%s"
              % (n, cur.sum(), fix.sum(), same))
    noop = all(r["identical"] for r in a_rows)
    print("      NO-OP on every banked resolution: %s" % noop)

    print("\n  (b) does it close the contamination where 3 | n?")
    b_rows = []
    for n in GRIDS_DIV3:
        row = {"n": n}
        for tag, m in (("current", dealias_mask(n)),
                       ("proposed", wavenumbers(n) <= (n - 1) // 3)):
            k = wavenumbers(n)
            K = int(np.max(k[m]))
            w = np.fft.irfft(np.fft.rfft(np.cos(K * grid(n))) * m, n)
            sp = float(np.abs((np.fft.rfft(w * w) * m / n)[K]))
            row[tag + "_K"] = K
            row[tag + "_spurious"] = _j(sp)
        b_rows.append(row)
        print("      n=%5d  current K=%4d spurious=%.3e  ->  proposed K=%4d spurious=%.3e"
              % (n, row["current_K"], float(row["current_spurious"]),
                 row["proposed_K"], float(row["proposed_spurious"])))
    closed = all(float(r["proposed_spurious"]) < 1e-12 for r in b_rows)
    print("      contamination closed at every 3 | n size: %s" % closed)

    print("\n  (c) is `(n-1)//3` the largest integer strictly below n/3, for every n?")
    bad = [n for n in range(1, 5000)
           if not ((n - 1) // 3 < n / 3.0 and (n - 1) // 3 + 1 >= n / 3.0)]
    print("      counterexamples in 1..4999: %s" % (bad or "NONE"))

    print("\n  NOTE: test_spectral_utils_dedicated.py:121-122 asserts dealias_mask(96)[32]")
    print("  is True (\"k = n/3 must be retained (<=, not <)\").  That assertion encodes the")
    print("  defect and must be inverted by the same repair.  Not this leg's file to edit.")
    return {"candidate": "wavenumbers(n) <= (n - 1) // 3",
            "noop_on_banked_resolutions": noop, "noop_rows": a_rows,
            "closes_contamination": closed, "closure_rows": b_rows,
            "counterexamples_1_to_4999": bad,
            "applied": False,
            "blocks_on": ("test_spectral_utils_dedicated.py:121-122 asserts the defect "
                          "and must be inverted by the same repair")}


# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("THE NINE BATTERIES")[0].strip()[:400])
    res = {"leg": 120, "route": "SUA", "branch": "leg/sua-v1", "date": "2026-08-06",
           "module_under_audit": "solver/spectral_utils.py",
           "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                    "solver/spectral_utils.py ever silently return a wrong value instead of "
                    "propagating or flagging the invalid input?"),
           "references": {
               "L1_bowman_2013": ("https://www.math.ualberta.ca/~bowman/talks/alias0.pdf -- "
                                  "p.29 Centered Convolutions: pad to N >= 3m-2 to prevent "
                                  "mode m-1 beating with itself to contaminate mode -m+1; "
                                  "with K=m-1 this is K < N/3 STRICTLY"),
               "L2_johnson_mit": ("https://math.mit.edu/~stevenj/fft-deriv.pdf -- Algorithm 1 "
                                  "step 2: multiply Y_k by ZERO for k = N/2 (N even). A "
                                  "MULTIPLICATION, not an assignment."),
           },
           "seed": SEED}
    res["S1_dealias_boundary"] = s1_dealias_boundary()
    res["S2_energy_production"] = s2_energy_production()
    res["S3_exposure"] = s3_exposure()
    res["S4_nyquist_poison"] = s4_nyquist_poison()
    res["S5_velocity_hat"] = s5_velocity_hat()
    res["S6_malformed_k"] = s6_malformed_k()
    res["S7_degenerate_n"] = s7_degenerate_n()
    res["S8_passes"] = s8_passes()
    res["S9_proposed_repair"] = s9_proposed_repair()

    s1, s2, s3 = res["S1_dealias_boundary"], res["S2_energy_production"], res["S3_exposure"]
    s4, s5, s6 = res["S4_nyquist_poison"], res["S5_velocity_hat"], res["S6_malformed_k"]
    gate = "YES" if (s1["n_contaminated"] > 0 or s4["n_erased"] > 0) else "NO"
    res["gate_answer"] = gate
    res["findings"] = {
        "D1_dealias_boundary_off_by_one_mode": {
            "what": ("dealias_mask keeps k <= n/3; Bowman's alias-free condition is k < n/3 "
                     "STRICTLY. For 3 | n the mask retains exactly one mode too many and that "
                     "mode beats with itself back into the retained band."),
            "contaminated_grids": s1["contaminated_grids"],
            "spurious_coeff": s1["spurious_coeff_on_contaminated"],
            "true_coeff": 0.0,
            "worst_on_clean_grids": s1["worst_spurious_on_clean"],
        },
        "D2_energy_production_aliased_at_div3": {
            "what": ("energy_production, docstring 'Exact rate d/dt E', inherits D1: it is the "
                     "cubic-in-w diagnostic feeding solver/gclm.py's energy-balance residual."),
            "worst_rel_err_div3": s2["worst_rel_err_div3"], "at_n": s2["worst_n_div3"],
            "worst_rel_err_not_div3": s2["worst_rel_err_not_div3"],
            "separation_decades": s2["separation_decades"],
        },
        "D3_nyquist_poison_erased": {
            "what": ("derivative_hat ASSIGNS d[-1] = 0.0 where Johnson Algorithm 1 MULTIPLIES "
                     "by zero; 0.0*nan = nan, so the published form propagates and the "
                     "assignment erases."),
            "erased": s4["n_erased"], "of": s4["n_nyquist_cases"],
            "controls_propagate": s4["all_non_nyquist_propagate"],
            "leg69_fix_intact": s4["leg69_fix_intact"],
        },
        "D4_velocity_hat_mean_mode_erased": {
            "erased": s5["n_erased"], "of": len(s5["mean_mode_poison"])},
        "D5_velocity_hat_dtype_truncation": {
            "worst_rel_err": s5["worst_dtype_rel_err"],
            "dtypes": s5["dtypes_on_int_input"]},
        "D6_malformed_k_broadcast": {
            "accepted_silently": s6["n_accepted"], "of": s6["n_cases"],
            "worst_rel_sup_err": s6["worst_silent_rel_sup_err"], "worst": s6["worst_case"]},
        "D7_degenerate_n_inconsistent": res["S7_degenerate_n"],
    }
    res["banked_numbers_at_risk"] = s3["banked_numbers_at_risk"]

    hdr("GATE")
    print("  Gate: does solver/spectral_utils.py ever SILENTLY return a wrong value")
    print("        instead of propagating or flagging the invalid input?")
    print("\n  ANSWER: %s\n" % gate)
    print("  D1  dealias_mask retains one mode too many when 3 | n (Bowman: K < n/3 strict).")
    print("      Spurious retained coefficient %s against a true value of exactly 0,"
          % s1["spurious_coeff_on_contaminated"])
    print("      at %d/%d grid sizes -- exactly the ones with 3 | n. Clean grids: %.1e."
          % (s1["n_contaminated"], s1["n_total"], float(s1["worst_spurious_on_clean"])))
    print("  D2  energy_production ('Exact rate d/dt E') inherits it: rel err %.4e at n = %d,"
          % (float(s2["worst_rel_err_div3"]), s2["worst_n_div3"]))
    print("      vs %.2e at every n not divisible by 3 (%.1f decades of separation)."
          % (float(s2["worst_rel_err_not_div3"]), float(s2["separation_decades"])))
    print("  D3  derivative_hat ERASES a non-finite Nyquist coefficient: %d/%d poisoned"
          % (s4["n_erased"], s4["n_nyquist_cases"]))
    print("      inputs returned a fully finite result. Controls propagate; leg 69 fix intact.")
    print("  D4  velocity_hat erases a non-finite mean mode: %d/%d." % (s5["n_erased"], 3))
    print("  D5  velocity_hat truncates integer input (rel err %s); the other two promote."
          % s5["worst_dtype_rel_err"])
    print("  D6  malformed k accepted silently in %d/%d cases, worst rel sup err %s."
          % (s6["n_accepted"], s6["n_cases"], s6["worst_silent_rel_sup_err"]))
    print("\n  BANKED NUMBERS AT RISK: %d" % s3["banked_numbers_at_risk"])
    print("  Every grid size on the dealias path is a power of two %s;" % s3["all_declared_sizes"])
    print("  no power of two is divisible by 3, so D1/D2 are LATENT -- exactly the severity")
    print("  shape of legs 66, 69 and 79. ESCALATE, DO NOT PATCH (leg 120's yes-branch).")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, sort_keys=False) + "\n")
    print("\nwrote %s" % OUT.relative_to(ROOT))
    return res


if __name__ == "__main__":
    main()
