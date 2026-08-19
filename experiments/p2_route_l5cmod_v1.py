#!/usr/bin/env python3
"""Leg 413 / unit `L5-cmod` -- does `c_mod` SATURATE, or is it LOGARITHMICALLY DIVERGENT?

WHAT THIS IS.  An EXTENSION of `L5`'s (leg 400) cutoff-radius sweep on its one load-bearing row
`alpha = 1 | kappa = a_physical_frozen | DSS`, from `rho ~ 1.26e3` out to `rho ~ 1.26e8`, in `L5`'s
own norm `||curl F||_{L1_t L3/2_x}`, with `L5`'s own apparatus and `L5`'s own driver constants.
Pre-registered in `experiments/journal/leg_413.md` SS0-SS6, committed BEFORE this file existed.

WHY.  `CORRECTIONS.md` SS53 flags `L5`'s banked reading -- *"the error PER UNIT SIMILARITY TIME
saturates at c_mod = 869.288, measured rho-exponent 0.000109 over rho0 in [10,1000]"* -- on the
ground that **a logarithmic divergence is exactly the exponent-zero case**: a power-law fit cannot
tell `const` from `const + c log rho`, both give exponent ~ 0.  `L5`'s sweep stops three decades
short of where the sister functional's sweep (`L-JVER`, leg 409) flattens to a NONZERO floor, and
`L5`'s own last two increments are POSITIVE.

THE GATE (verbatim, SS0 of the journal):
    Is the per-decade increment in `c_mod` approaching a NONZERO CONSTANT -- YES or NO?

`L5`'s CODE AND ARTEFACT ARE READ, NEVER MODIFIED.  This file imports
`experiments/p2_route_l5_v1.py` as a module and `experiments/p2_route_l5_v1_driver.py` for its
constants, disables `L5.checkpoint` as a hard interlock so `L5`'s artefact can not be written even
by accident, and hashes `L5`'s four files before and after the run.

CEILING (journal SS1, written before any number existed).  Tier 2.  float64.  No `L1->L4` link
moves either way.  Clay stays ~0.05%.  Says NOTHING about whether a blow-up profile exists.  `c_mod`
is a property of leg 381's SYNTHETIC realization either way -- route 4 has no banked profile.  The
ansatz-class EXPONENT `1 - alpha = 0` is untouched by this unit.  Common-mode blindness with `L5`
is INHERITED and NOT repaired (`CORRECTIONS.md` SS45): there is no second implementation of
`R_loc`.

Run:    OMP_NUM_THREADS=1 .venv/bin/python experiments/p2_route_l5cmod_v1.py
Writes: writeup/data/p2_route_l5cmod_v1.json   (checkpointed after every stage)
"""

import hashlib
import importlib.util
import json
import math
import os
import resource
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_l5cmod_v1.json"
L5_SRC = ROOT / "experiments" / "p2_route_l5_v1.py"
L5_DRV = ROOT / "experiments" / "p2_route_l5_v1_driver.py"
L5_EVD = ROOT / "experiments" / "p2_route_l5_v1_evidence.py"
L5_JSON = ROOT / "writeup" / "data" / "p2_route_l5_finite_energy_v1.json"

LOAD_BEARING_ROW = "alpha=1|kappa=a_physical_frozen|DSS"


# ---------------------------------------------------------------------------------------------
# 0.  Load `L5` -- READ ONLY, with a hard interlock against writing its artefact
# ---------------------------------------------------------------------------------------------

def file_sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def load_l5(tag):
    """A FRESH module instance of L5's core.  `checkpoint` is replaced by a raising interlock."""
    spec = importlib.util.spec_from_file_location("l5core_%s" % tag, L5_SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    def _forbidden(*a, **k):
        raise RuntimeError("leg 413 INTERLOCK: L5's artefact is READ, NEVER MODIFIED")

    mod.checkpoint = _forbidden
    return mod


def load_l5_driver_constants():
    """The row's constants, taken from `L5`'s DRIVER file itself -- not from memory, not from prose."""
    spec = importlib.util.spec_from_file_location("l5drv", L5_DRV)
    drv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(drv)          # module-level only; `main()` is under a __main__ guard
    drv.L5.checkpoint = lambda *a, **k: (_ for _ in ()).throw(
        RuntimeError("leg 413 INTERLOCK: L5's artefact is READ, NEVER MODIFIED"))
    return dict(RES=dict(drv.RES), RES_HI=dict(drv.RES_HI), N_S=drv.N_S,
                RHOS=list(drv.RHOS), KAPPA=drv.KAPPAS["kappa=a_physical_frozen"],
                ALPHA=drv.ALPHAS[0])


# ---------------------------------------------------------------------------------------------
# 1.  PLANTED PROFILES -- controls only.  Injected by rebinding `psi_derivs` on a SEPARATE module
#     instance, so the pristine instance used for the gate is untouched.
# ---------------------------------------------------------------------------------------------

def psi_pure_power(r, alpha, order=4):
    """psi = r^{2-alpha} EXACTLY -- the scale-invariant limit of L5's (1+r^2)^{(2-alpha)/2}."""
    p = 2.0 - alpha
    out, coef = [], 1.0
    for k in range(order + 1):
        out.append(coef * r ** (p - k))
        coef *= (p - k)
    return out


def _log_factor_derivs(r, beta, order=4):
    """derivatives of 1 + beta * u, u = 0.5 ln(1+r^2)  (u', u'', u''', u'''' verified vs mpmath 40dps)."""
    b = 1.0 + r * r
    d = [1.0 + beta * 0.5 * np.log(b),
         beta * (r / b),
         beta * ((1.0 - r * r) / b ** 2),
         beta * (2.0 * r * (r * r - 3.0) / b ** 3),
         beta * (-6.0 * (r ** 4 - 6.0 * r * r + 1.0) / b ** 4)]
    return d[:order + 1]


def make_psi_log(mod, beta):
    """psi -> psi_alpha * (1 + beta * 0.5 ln(1+r^2)): an EXACTLY logarithmic planted divergence."""
    base = mod.psi_derivs

    def psi(r, alpha, order=4):
        return mod.leibniz(base(r, alpha, order), _log_factor_derivs(r, beta, order), order)
    return psi


# ---------------------------------------------------------------------------------------------
# 2.  One row of the ladder, through L5's own `period_average`
# ---------------------------------------------------------------------------------------------

def row(mod, rho0, alpha, kappa, n_s, res, per_term=True, **kw):
    t0 = time.time()
    v = mod.period_average(alpha, rho0, kappa, mode="DSS", n_s=n_s, per_term=per_term, **res, **kw)
    v["rho0"] = float(rho0)
    v["seconds"] = round(time.time() - t0, 2)
    return v


def ladder(mod, rho0s, alpha, kappa, n_s, res, label="", per_term=True, **kw):
    rows = []
    for rho0 in rho0s:
        v = row(mod, rho0, alpha, kappa, n_s, res, per_term=per_term, **kw)
        rows.append(v)
        print("   %-18s rho0=%-10g rho=%-12.6g curl_L32=%.10f L3=%.8f (%.1fs)"
              % (label, rho0, v["rho"], v["curl_L32"], v["L3"], v["seconds"]), flush=True)
    return rows


def increments(rows, key="curl_L32"):
    """increment in `key` PER DECADE of the banked `rho` field, band by band."""
    out = []
    for a, b in zip(rows[:-1], rows[1:]):
        dec = math.log10(b["rho"] / a["rho"])
        out.append({"rho_lo": a["rho"], "rho_hi": b["rho"], "decades": dec,
                    "value_lo": a[key], "value_hi": b[key],
                    "delta": b[key] - a[key], "per_decade": (b[key] - a[key]) / dec})
    return out


def last3_verdict(incs, noise_floor):
    """The SS0.2 decision rule, fixed before any number existed."""
    tail = [i["per_decade"] for i in incs[-3:]]
    mean = float(np.mean(tail))
    spread = float(max(tail) - min(tail))
    rel_spread = abs(spread / mean) if mean != 0 else float("inf")
    shrinking = all(abs(tail[k + 1]) < abs(tail[k]) for k in range(len(tail) - 1))
    above_noise = abs(mean) > 10.0 * noise_floor
    if rel_spread < 0.01 and above_noise:
        verdict = "YES"
    elif shrinking and abs(tail[-1]) <= noise_floor:
        verdict = "NO"
    else:
        verdict = "UNDER-RESOURCED"
    return {"last3_per_decade": tail, "mean": mean, "rel_spread_of_last3": rel_spread,
            "monotonically_shrinking": shrinking, "noise_floor_used": noise_floor,
            "terminal_over_noise_floor": abs(tail[-1]) / noise_floor if noise_floor else None,
            "mean_over_noise_floor": abs(mean) / noise_floor if noise_floor else None,
            "verdict_by_precommitted_rule": verdict}


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


def checkpoint(doc, note):
    doc["_checkpoint"] = note
    doc["_checkpoint_time"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    OUT.write_text(json.dumps(doc, indent=1))
    print("  [checkpoint] %s -> %s" % (note, OUT.name), flush=True)


# ---------------------------------------------------------------------------------------------
# 3.  THE RUN
# ---------------------------------------------------------------------------------------------

# the gate ladder: L5's own [10,30,100,300,1000] continued by the SAME x3, x10/3 alternation
GATE_RHO0S = [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 1e4, 3e4, 1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8]
CTRL_RHO0S = [1e3, 1e4, 1e5, 1e6, 1e7, 1e8]
BETA_LOG = 0.05
DELTA_ALPHA = 0.001


def main():
    t_start = time.time()
    K = load_l5_driver_constants()
    RES, RES_HI, N_S, KAPPA, ALPHA = K["RES"], K["RES_HI"], K["N_S"], K["KAPPA"], K["ALPHA"]
    L5 = load_l5("gate")

    doc = {
        "leg": 413, "unit": "L5-cmod", "lane": "L", "wave": 9,
        "route": "L5-CMOD-CUTOFF-EXTENSION",
        "what": ("extend L5's cutoff-radius sweep on its load-bearing row "
                 "alpha=1|kappa=a_physical_frozen|DSS from rho~1.26e3 out to rho~1.26e8, same "
                 "apparatus, same norm ||curl F||_{L1_t L3/2_x}, same ansatz, and report the "
                 "increment in c_mod PER DECADE of rho for every band"),
        "gate_question": ("Is the per-decade increment in c_mod approaching a NONZERO CONSTANT "
                          "-- YES or NO?"),
        "preregistration": "experiments/journal/leg_413.md SS0-SS6, committed before this file existed",
        "precommitted_decision_rule": (
            "journal SS0.2: YES iff the last three consecutive per-decade increments agree to "
            "within 1% of their mean AND that mean exceeds 10x the MEASURED arithmetic-noise floor; "
            "NO iff the last three shrink monotonically in magnitude and the terminal one is at or "
            "below that floor; anything else UNDER-RESOURCED, never NO"),
        "ceiling": ("TIER 2. float64. Extension of L5's OWN apparatus on a SYNTHETIC exactly-DSS "
                    "realization (leg 381). No link of the L1->L4 chain moves either way. Clay "
                    "stays ~0.05%. Says NOTHING about whether a blow-up profile exists. c_mod is a "
                    "property of leg 381's realization either way. The ansatz-class exponent "
                    "1-alpha=0 is untouched. Common-mode blindness with L5 is INHERITED and NOT "
                    "repaired: no second implementation of R_loc exists (CORRECTIONS.md SS45)."),
        "row_constants_read_from_L5_driver": {
            "file": "experiments/p2_route_l5_v1_driver.py", "RES": RES, "RES_HI": RES_HI,
            "N_S": N_S, "kappa": KAPPA, "alpha": ALPHA, "L5_RHOS": K["RHOS"],
            "row": LOAD_BEARING_ROW, "fd_rel": 1e-4, "kind": "C4", "amp": 1.0, "a_mod": 0.5},
        "L5_files_read_never_modified": {
            "before": {p.name: file_sha(p) for p in (L5_SRC, L5_DRV, L5_EVD, L5_JSON)}},
        "controls": {}, "gate": {},
    }
    checkpoint(doc, "opened")

    banked = json.loads(L5_JSON.read_text())["sweep"][LOAD_BEARING_ROW]

    # ---- X1: reproduce L5's banked rows from L5's own code -----------------------------------
    print("X1  reproduce L5's banked rho0 in [10,1000] rows from L5's OWN code "
          "(recompute-from-primary)...", flush=True)
    rep = ladder(L5, K["RHOS"], ALPHA, KAPPA, N_S, RES, label="X1-reproduce")
    keys = ("rho", "L3", "curl_L32", "T1_L3", "T2_L3", "T3_L3", "T4_L3", "T5_L3", "T12_L3", "T123_L3")
    worst, worst_key, ident = 0.0, None, 0
    per_field = []
    for mine, bank in zip(rep, banked["rows"]):
        for k in keys:
            rel = abs(mine[k] - bank[k]) / max(abs(bank[k]), 1e-300)
            if mine[k] == bank[k]:
                ident += 1
            per_field.append({"rho0": mine["rho0"], "field": k, "mine": mine[k],
                              "banked": bank[k], "rel": rel, "bit_identical": mine[k] == bank[k]})
            if rel > worst:
                worst, worst_key = rel, "rho0=%g %s" % (mine["rho0"], k)
    doc["controls"]["X1_reproduce_L5_banked_rows"] = {
        "class": "recompute-from-primary",
        "what": ("call L5.period_average with L5's own driver constants at L5's own rho0 ladder and "
                 "compare 10 fields per row against the banked artefact"),
        "n_fields_compared": len(per_field), "n_bit_identical": ident,
        "max_rel_diff": worst, "worst_field": worst_key,
        "threshold": 1e-12, "passed": worst < 1e-12,
        "rows_recomputed": rep, "field_by_field": per_field}
    print("X1  max rel = %.3e over %d fields, %d bit-identical -> %s"
          % (worst, len(per_field), ident, "PASS" if worst < 1e-12 else "FAIL"), flush=True)
    checkpoint(doc, "X1")
    if not worst < 1e-12:
        doc["gate"] = {"answer": "STOPPED", "why": "X1 failed: this is not L5's object"}
        checkpoint(doc, "STOPPED at X1")
        return

    # ---- THE GATE LADDER ---------------------------------------------------------------------
    print("GATE  ladder rho0 = 10 ... 1e8 on %s ..." % LOAD_BEARING_ROW, flush=True)
    grows = rep + ladder(L5, GATE_RHO0S[len(K["RHOS"]):], ALPHA, KAPPA, N_S, RES, label="GATE")
    doc["gate"]["rows"] = grows
    doc["gate"]["increments_per_decade_curl_L32"] = increments(grows, "curl_L32")
    doc["gate"]["increments_per_decade_L3"] = increments(grows, "L3")
    checkpoint(doc, "gate ladder")

    # ---- X4: exact scale invariance = the MEASURED noise floor --------------------------------
    print("X4  planted EXACT scale invariance (psi = r^{2-alpha}) -> measures the noise floor "
          "(recompute-from-primary)...", flush=True)
    Lp = load_l5("purepower")
    Lp.psi_derivs = psi_pure_power
    prows = ladder(Lp, GATE_RHO0S[4:], ALPHA, KAPPA, N_S, RES, label="X4-purepower")
    pinc = increments(prows, "curl_L32")
    vals = [r["curl_L32"] for r in prows]
    spread = (max(vals) - min(vals))
    noise = max(abs(i["per_decade"]) for i in pinc)
    doc["controls"]["X4_exact_scale_invariance_noise_floor"] = {
        "class": "recompute-from-primary",
        "what": ("psi replaced by the pure power r^{2-alpha}, which makes the whole construction "
                 "EXACTLY scale-invariant in rho at alpha=1, so any residual rho-dependence is "
                 "arithmetic noise of the instrument and nothing else"),
        "rows": prows, "increments_per_decade": pinc,
        "absolute_spread_over_5_decades": spread,
        "relative_spread": spread / float(np.mean(vals)),
        "noise_floor_per_decade": noise,
        "passed": spread / float(np.mean(vals)) < 1e-9}
    print("X4  spread %.3e (rel %.3e) over 5 decades; NOISE FLOOR %.3e per decade"
          % (spread, spread / float(np.mean(vals)), noise), flush=True)
    checkpoint(doc, "X4")

    # ---- X2: planted EXACT logarithm -- the instrument MUST answer YES ------------------------
    print("X2  planted EXACT log divergence beta=%g -- instrument MUST answer YES "
          "(recompute-from-primary)..." % BETA_LOG, flush=True)
    Ll = load_l5("logdefect")
    Ll.psi_derivs = make_psi_log(Ll, BETA_LOG)
    lrows = ladder(Ll, CTRL_RHO0S, ALPHA, KAPPA, N_S, RES, label="X2-logdefect")
    linc = increments(lrows, "curl_L32")
    lver = last3_verdict(linc, noise)
    predicted = lrows[-1]["curl_L32"] * BETA_LOG * math.log(10.0) / (1.0 + BETA_LOG * math.log(lrows[-1]["rho"]))
    doc["controls"]["X2_planted_log_divergence_must_say_YES"] = {
        "class": "recompute-from-primary",
        "what": ("psi -> psi_alpha * (1 + beta*0.5*ln(1+r^2)); at alpha=1 the scale-invariant size "
                 "becomes proportional to (1 + beta ln rho), i.e. an EXACTLY CONSTANT per-decade "
                 "increment. A gate whose null is NO is worthless without a control that MUST "
                 "return YES."),
        "beta": BETA_LOG, "rows": lrows, "increments_per_decade": linc,
        "verdict": lver, "roughly_predicted_per_decade": predicted,
        "fired_as_planted": lver["verdict_by_precommitted_rule"] == "YES",
        "passed": lver["verdict_by_precommitted_rule"] == "YES"}
    print("X2  last3 = %s -> %s (planted: YES)"
          % (["%.4g" % v for v in lver["last3_per_decade"]],
             lver["verdict_by_precommitted_rule"]), flush=True)
    checkpoint(doc, "X2")

    # ---- X3: planted power laws, BOTH SIGNS ---------------------------------------------------
    doc["controls"]["X3_planted_power_law_sign"] = {"class": "recompute-from-primary", "cases": {}}
    for sgn, a in ((+1, ALPHA - DELTA_ALPHA), (-1, ALPHA + DELTA_ALPHA)):
        print("X3  planted power law alpha=%.6g (expect sign %+d) ..." % (a, sgn), flush=True)
        rws = ladder(L5, CTRL_RHO0S, a, KAPPA, N_S, RES, label="X3-alpha=%.4g" % a)
        inc = increments(rws, "curl_L32")
        tail = [i["per_decade"] for i in inc[-3:]]
        pred = rws[-1]["curl_L32"] * DELTA_ALPHA * math.log(10.0)
        ok = all((v > 0) == (sgn > 0) for v in tail) and abs(abs(np.mean(tail)) / pred - 1.0) < 0.25
        doc["controls"]["X3_planted_power_law_sign"]["cases"]["alpha=%.6g" % a] = {
            "expected_sign": sgn, "rows": rws, "increments_per_decade": inc,
            "last3_per_decade": tail, "predicted_magnitude_per_decade": pred,
            "fired_as_planted": bool(ok), "passed": bool(ok)}
        print("X3  last3 = %s ; predicted magnitude %.4g -> %s"
              % (["%.4g" % v for v in tail], pred, "PASS" if ok else "DID NOT FIRE"), flush=True)
        checkpoint(doc, "X3 alpha=%.6g" % a)

    # ---- X5: quadrature / n_s / FD self-convergence at the LARGEST rho -------------------------
    print("X5  self-convergence at the largest rho (rho0=1e8) ...", flush=True)
    base = grows[-1]
    variants = {"RES_baseline_n_s_6_fd_1e-4": dict(res=RES, n_s=N_S, kw={}),
                "RES_HI_n_s_6_fd_1e-4": dict(res=RES_HI, n_s=N_S, kw={}),
                "RES_n_s_12_fd_1e-4": dict(res=RES, n_s=2 * N_S, kw={}),
                "RES_n_s_6_fd_1e-3": dict(res=RES, n_s=N_S, kw={"fd_rel": 1e-3}),
                "RES_n_s_6_fd_1e-5": dict(res=RES, n_s=N_S, kw={"fd_rel": 1e-5})}
    x5 = {}
    for name, cfg in variants.items():
        if name.startswith("RES_baseline"):
            v = base
        else:
            v = row(L5, 1e8, ALPHA, KAPPA, cfg["n_s"], cfg["res"], **cfg["kw"])
        x5[name] = {"curl_L32": v["curl_L32"], "L3": v["L3"], "rho": v["rho"],
                    "seconds": v.get("seconds")}
        print("   %-28s curl_L32 = %.10f" % (name, v["curl_L32"]), flush=True)
    ref = x5["RES_baseline_n_s_6_fd_1e-4"]["curl_L32"]
    devs = {k: abs(v["curl_L32"] - ref) for k, v in x5.items() if not k.startswith("RES_baseline")}
    res_floor = max(devs.values())
    gate_incs = [abs(i["per_decade"]) for i in doc["gate"]["increments_per_decade_curl_L32"][-3:]]
    doc["controls"]["X5_self_convergence_at_largest_rho"] = {
        "class": "recompute-from-primary",
        "what": ("at rho0=1e8: angular+radial order RES vs RES_HI, n_s 6 vs 12, and the curl's "
                 "finite-difference step fd_rel over 1e-3/1e-4/1e-5"),
        "variants": x5, "absolute_deviations_from_baseline": devs,
        "resolution_floor_absolute": res_floor,
        "gate_last3_increments_abs": gate_incs,
        "note": ("this is an ABSOLUTE spread in c_mod, not a per-decade rate; it bounds how much of "
                 "any measured per-decade increment could be discretisation rather than the object")}
    print("X5  resolution floor (absolute) = %.3e ; gate's last-3 per-decade = %s"
          % (res_floor, ["%.3e" % g for g in gate_incs]), flush=True)
    checkpoint(doc, "X5")

    # ---- X6: the overlap.  DISCLOSED as subsumed, not re-run to inflate a tally ---------------
    doc["controls"]["X6_overlap"] = {
        "class": "recompute-from-primary",
        "what": ("journal SS4(f) asked that the extension code reproduce the banked rho0=1000 row "
                 "through MY driver path as well as through L5's"),
        "DISCLOSURE": ("this control is SUBSUMED BY X1 BY CONSTRUCTION and is not an independent "
                       "check: the gate ladder's first five rows ARE the X1 rows, reused rather "
                       "than recomputed, so there is only one code path and X6 cannot fail unless "
                       "X1 fails. It is reported as one check, not two, and it is NOT counted "
                       "separately in the tally."),
        "counted_in_tally": False,
        "gate_row_rho0_1000_curl_L32": grows[4]["curl_L32"],
        "banked_row_rho0_1000_curl_L32": banked["rows"][4]["curl_L32"],
        "bit_identical": grows[4]["curl_L32"] == banked["rows"][4]["curl_L32"]}

    # ---- X7: how far float64 can still SEE the object, stated not hidden ----------------------
    print("X7  float64 saturation reach of psi = (1+r^2)^{1/2} ...", flush=True)
    sat = []
    for v in grows:
        rr = 1.5 * v["rho"]                     # annulus midpoint-ish
        resolved = bool((1.0 + rr * rr) != (rr * rr))
        sat.append({"rho": v["rho"], "r_probe": rr, "relative_size_of_the_1": 1.0 / (rr * rr),
                    "resolved_in_float64": resolved})
    last_resolved = max([s["rho"] for s in sat if s["resolved_in_float64"]], default=None)
    doc["controls"]["X7_float64_saturation_reach"] = {
        "class": "recompute-from-primary",
        "what": ("psi_alpha = (1+r^2)^{(2-alpha)/2} differs from the exactly scale-invariant pure "
                 "power r^{2-alpha} by a RELATIVE O(r^-2). Beyond r^2 ~ 1/eps the `1` is below "
                 "float64 resolution and the code is computing the pure power EXACTLY, so the "
                 "terminal bands of the ladder cannot resolve the correction even in principle."),
        "eps": float(np.finfo(float).eps), "per_row": sat,
        "largest_rho_where_the_correction_is_still_resolved": last_resolved,
        "consequence": ("the gate must not rest on the float-saturated bands alone; X8 discriminates "
                        "the two models on the WELL-RESOLVED decades, and X4 measures what the "
                        "saturated bands are worth")}
    print("X7  correction still resolved up to rho = %.4g" % (last_resolved or float("nan")),
          flush=True)

    # ---- X8: model discrimination on the WELL-RESOLVED decades --------------------------------
    fitrows = [v for v in grows if v["rho"] <= 1.3e6]
    x = np.array([v["rho"] for v in fitrows])
    y = np.array([v["curl_L32"] for v in fitrows])
    fits = {}
    for name, basis in (("A + B*rho^-2", x ** -2.0), ("A + B*log10(rho)", np.log10(x))):
        A = np.vstack([np.ones_like(x), basis]).T
        sol, *_ = np.linalg.lstsq(A, y, rcond=None)
        r = y - A @ sol
        fits[name] = {"A": float(sol[0]), "B": float(sol[1]),
                      "max_abs_residual": float(np.max(np.abs(r))),
                      "rms_residual": float(np.sqrt(np.mean(r ** 2)))}
    ratio = (fits["A + B*log10(rho)"]["rms_residual"]
             / max(fits["A + B*rho^-2"]["rms_residual"], 1e-300))
    doc["controls"]["X8_model_discrimination"] = {
        "class": "recompute-from-primary",
        "what": ("two-parameter least squares of c_mod(rho) over the decades where the correction "
                 "is still resolved in float64: SATURATING (A + B rho^-2, the analytic prior of "
                 "journal SS3) against LOG-DIVERGENT (A + B log10 rho, SS53's hypothesis). Same "
                 "data, same number of parameters."),
        "rows_used": [{"rho": v["rho"], "curl_L32": v["curl_L32"]} for v in fitrows],
        "fits": fits, "rms_ratio_log_over_power": ratio,
        "reading": ("a ratio >> 1 means the saturating model fits the SAME data far better with the "
                    "SAME number of parameters; a ratio ~ 1 or < 1 means the two are not separable "
                    "at this reach and the gate is UNDER-RESOURCED")}
    print("X8  rms residual: A+B rho^-2 = %.3e ; A+B log10 rho = %.3e ; ratio %.4g"
          % (fits["A + B*rho^-2"]["rms_residual"], fits["A + B*log10(rho)"]["rms_residual"], ratio),
          flush=True)
    checkpoint(doc, "X6/X7/X8")

    # ---- THE GATE SPEAKS ----------------------------------------------------------------------
    incs = doc["gate"]["increments_per_decade_curl_L32"]
    verdict = last3_verdict(incs, noise)
    banked_cmod = json.loads(L5_JSON.read_text())["gate"]["c_mod_per_unit_s"]
    signs = [i["per_decade"] > 0 for i in incs]
    doc["gate"].update({
        "c_mod_banked_by_L5": banked_cmod,
        "c_mod_at_largest_rho": grows[-1]["curl_L32"],
        "largest_rho_reached": grows[-1]["rho"],
        "largest_rho0_reached": grows[-1]["rho0"],
        "total_change_from_L5s_last_rho": grows[-1]["curl_L32"] - banked_cmod,
        "relative_change_from_L5s_last_rho": (grows[-1]["curl_L32"] - banked_cmod) / banked_cmod,
        "decades_added": math.log10(grows[-1]["rho"] / grows[4]["rho"]),
        "all_increments_positive": all(signs),
        "negative_increment_bands": [i for i, s in zip(incs, signs) if not s],
        "verdict_detail": verdict,
        "answer": verdict["verdict_by_precommitted_rule"]})
    doc["L5_files_read_never_modified"]["after"] = {
        p.name: file_sha(p) for p in (L5_SRC, L5_DRV, L5_EVD, L5_JSON)}
    doc["L5_files_read_never_modified"]["unchanged"] = (
        doc["L5_files_read_never_modified"]["before"] ==
        doc["L5_files_read_never_modified"]["after"])
    ru = resource.getrusage(resource.RUSAGE_SELF)
    doc["cost_own_footprint"] = {
        "wall_seconds": round(time.time() - t_start, 1),
        "cpu_seconds_user": round(ru.ru_utime, 1), "cpu_seconds_sys": round(ru.ru_stime, 1),
        "max_rss_mb": round(ru.ru_maxrss / 1024.0, 1),
        "processes": 1, "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS", "unset"),
        "note": "CORRECTIONS.md SS40: this is the unit's OWN footprint, not the ambient load"}
    doc["chain"] = {"links_moved": [],
                    "statement": ("NO link of the L1->L4 chain moved. Tier-2 float64 extension of a "
                                  "Tier-2 float64 sweep on a synthetic realization. Clay ~0.05%. "
                                  "Scale is not evidence.")}
    doc["self_hash"] = sha({k: v for k, v in doc.items() if not k.startswith("_")})
    checkpoint(doc, "SEALED")
    print("\nGATE ANSWER: %s" % doc["gate"]["answer"], flush=True)
    print("  last-3 per-decade increments: %s" % verdict["last3_per_decade"], flush=True)
    print("  measured noise floor per decade: %.3e" % noise, flush=True)
    print("  L5 files unchanged: %s" % doc["L5_files_read_never_modified"]["unchanged"], flush=True)


if __name__ == "__main__":
    main()
