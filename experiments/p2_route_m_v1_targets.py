"""Route-M v1: TARGET SELECTION. "Certify WHAT, that isn't already done?"

The port has been aimed at Chen-Hou's 2D Boussinesq profile for twenty legs.  That
object was certified by its authors.  This leg asks the question nobody asked -- which
objects with numerically convincing blow-up are still UNCERTIFIED, and which of those
are within interval-arithmetic reach -- and answers it in code rather than in prose.

  M1  THE LEDGER.  Six candidate objects, three questions each (already certified? /
      within reach? / what would it contribute?), sourced to primary literature, ranked
      by contribution.  From solver/target_selection.py; cheap.
  M2  THE FEASIBILITY ALGEBRA, gated against a completed certificate.  The radii
      polynomial's Y_0 BUDGET is what makes "reachable" a measurement.  Validated on
      Cadiot-Lessard-Nave's published Kawahara constants, then used to audit the scalar
      Newton-Kantorovich closure asserted by the 3D Navier-Stokes preprint -- in both
      the printed form and the form Kantorovich's theorem requires.
  M3  REACHABILITY, MEASURED, on the top-ranked object.  A grid-refinement ladder for
      the non-symmetric Hou-Luo profile with the dissipation taken to zero WITH the
      grid.  The question is not the endpoint, it is the DIRECTION (banked lesson 72),
      and the comparison is against Route-K's committed 2D ladder, where the same
      measurement went the other way.
  M4  THE CONTRAST, read out of committed JSON rather than recomputed: Route-G's 2D
      resolution ladder, 2x finer and 16x worse, on the object the port is aimed at.

Deterministic.  M1/M2/M4 are seconds; M3 is the cost (~1 h at the default ladder).
Writes writeup/data/p2_route_m_v1_targets.json.

Run: .venv/bin/python -u experiments/p2_route_m_v1_targets.py
     .venv/bin/python -u experiments/p2_route_m_v1_targets.py --quick   (n ladder 201/401)
"""

import argparse
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.hl_rescaled import RescaledHLScenario2, scenario2_ic     # noqa: E402
from solver.target_selection import (                                # noqa: E402
    CERTIFICATION_RECORD, TARGET_LEDGER, cln_kawahara_check, gate_verdict,
    ledger_counts, ns_preprint_closure_audit, radii_polynomial, rank_table,
    uncertified_targets, y0_budget,
)

OUT = ROOT / "writeup" / "data" / "p2_route_m_v1_targets.json"
ROUTE_K = ROOT / "writeup" / "data" / "p2_route_k_v1_port.json"

CHL_RATIO = -2.5114          # [CHL] Fig 4.2, the normalization-INDEPENDENT constant
CHL_TRIPLE = (1.0636, -0.4235, 0.0765)
TAU_END = 42.0               # matched across the ladder; section 8's run reached ~42
NU_REF, N_REF = 0.02, 801    # section 8's dissipation, at section 8's resolution


# --------------------------------------------------------------------------
# M3 -- the reachability ladder
# --------------------------------------------------------------------------
def relax_to_tau(n, nu, tau_end, c=0.35, rho_max=7.0, x0=0.30, record=64):
    """Relax CHL (4.1)/(4.2) at resolution n to a FIXED rescaled time tau_end.

    Fixed tau rather than fixed step count, because the step is CFL-limited and shrinks
    with the grid: comparing at equal steps would compare different amounts of elapsed
    dynamics and the ladder would measure the clock, not the operator.

    `nu` is the subgrid dissipation, and on this ladder it is taken to zero WITH the
    grid (nu ~ drho).  A ladder at fixed nu measures the dissipation's floor; the
    certificate has to live at nu = 0, so the floor has to be shown moving.
    """
    s2 = RescaledHLScenario2(n=n, c=c, rho_max=rho_max, nu=nu)
    Om, V = scenario2_ic(s2.X, x0=x0)
    dt = 0.3 * s2.drho / max(s2.max_speed_rho(Om, V), 1e-6)
    tau, step = 0.0, 0
    hist = {"tau": [], "res": [], "ratio": [], "c_l": [], "c_omega": [], "c_r": []}
    res = np.inf
    c_l = c_omega = c_r = np.nan
    t0 = time.time()
    while tau < tau_end:
        Om, V, c_l, c_omega, c_r, res = s2.step(Om, V, dt)
        tau += dt
        step += 1
        if step % record == 0:
            hist["tau"].append(tau); hist["res"].append(res)
            hist["ratio"].append(c_l / c_omega if c_omega != 0 else np.nan)
            hist["c_l"].append(c_l); hist["c_omega"].append(c_omega)
            hist["c_r"].append(c_r)
        if not np.isfinite(res) or res > 1e8:
            break
    X, Om_f = s2.X, Om
    peak = int(np.argmax(Om_f))
    return {
        "n": int(n), "nu": float(nu), "drho": float(s2.drho), "dt": float(dt),
        "steps": int(step), "tau": float(tau), "wall_s": float(time.time() - t0),
        "residual": float(res), "c_l": float(c_l), "c_omega": float(c_omega),
        "c_r": float(c_r),
        "ratio": float(c_l / c_omega) if c_omega else float("nan"),
        "ratio_err_vs_CHL": float(abs(c_l / c_omega - CHL_RATIO) / abs(CHL_RATIO))
        if c_omega else float("nan"),
        "min_Omega": float(np.min(Om_f)), "min_V": float(np.min(V)),
        "X_peak": float(X[peak]), "Omega_peak": float(Om_f[peak]),
        "blewup": bool(not np.isfinite(res) or res > 1e8),
        "hist": {k: [float(x) for x in v] for k, v in hist.items()},
        "tau_direction": tau_direction(hist),
        # the profile, thinned, so the figure can be rebuilt from committed data
        "X_sample": [float(x) for x in X[::max(1, n // 400)]],
        "Omega_sample": [float(x) for x in Om_f[::max(1, n // 400)]],
        "V_sample": [float(x) for x in V[::max(1, n // 400)]],
    }


def tau_direction(hist, tail_frac=1.0 / 3.0):
    """Is the residual still FALLING in rescaled time, or has it floored / turned up?

    Route-K's 2D object LIMIT-CYCLES: its sup residual falls 38x and then climbs 9x, and
    every previous run had stopped at the bottom of the cycle and called it converged
    (banked lesson 71 -- read the residual column's DIRECTION).  This is that same
    instrument, applied to the 1D candidate before it is named as a target, so the
    naming cannot rest on a run that happened to stop at a good moment.

    Returns the tail slope d log(res)/d tau, the ratio of the FINAL residual to the
    MINIMUM ever attained (the limit-cycle detector: >> 1 means the run walked back up),
    and where in tau that minimum sat.
    """
    tau = np.asarray(hist["tau"], float)
    res = np.asarray(hist["res"], float)
    ok = np.isfinite(res) & (res > 0)
    tau, res = tau[ok], res[ok]
    if tau.size < 8:
        return {"refused": True, "reason": "fewer than 8 recorded rungs in tau"}
    i0 = int((1.0 - tail_frac) * (tau.size - 1))
    slope = float(np.polyfit(tau[i0:], np.log(res[i0:]), 1)[0])
    imin = int(np.argmin(res))
    return {"refused": False, "tail_slope_dlogres_dtau": slope,
            "final_over_min": float(res[-1] / res[imin]),
            "tau_at_min": float(tau[imin]), "tau_end": float(tau[-1]),
            "min_res": float(res[imin]), "final_res": float(res[-1]),
            "monotone_tail": bool(slope < 0.0),
            "limit_cycles": bool(res[-1] / res[imin] > 2.0)}


def ladder_direction(rungs, key="residual"):
    """The SHAPE of the ladder, not its endpoint (banked lesson 72).

    Returns the per-rung ratios and a classifier.  FALLING means each refinement
    strictly improves the quantity -- the only reading under which a fixed point that
    interval arithmetic could enclose is plausibly there.
    """
    v = [r[key] for r in rungs]
    ratios = [v[i + 1] / v[i] for i in range(len(v) - 1)]
    if any(not np.isfinite(x) for x in v):
        cls = "DIVERGED"
    elif all(x < 0.9 for x in ratios):
        cls = "FALLING"
    elif all(x > 1.1 for x in ratios):
        cls = "GROWING"
    else:
        cls = "FLAT_OR_MIXED"
    return {"values": v, "step_ratios": ratios, "net_ratio": v[-1] / v[0],
            "classification": cls}


def _rung(job):
    """Pool worker: one (n, nu, tau_end) rung of the M3 ladder."""
    n, nu, tau_end = job
    return relax_to_tau(n, nu, tau_end)


def _jsonable(o):
    """numpy scalars are not JSON-serializable and silently reach the payload."""
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    raise TypeError(f"not JSON serializable: {type(o)}")


def route_k_2d_contrast():
    """Route-K's committed 2D ladder, READ not recomputed -- the object the port is on."""
    if not ROUTE_K.exists():
        return {"available": False}
    d = json.loads(ROUTE_K.read_text())["K1_K2_no_fixed_point"]
    lad = d["route_g_resolution_ladder"]
    return {"available": True, "ladder": lad,
            "grows_under_refinement": bool(d["route_g_residual_grows_under_refinement"]),
            "net_ratio": lad[-1]["residual"] / lad[0]["residual"],
            "n_r": [r["n_r"] for r in lad],
            "c_omega_spread": d["route_g_c_omega_spread_over_that_ladder"]}


# --------------------------------------------------------------------------
# the pre-committed predicate
# --------------------------------------------------------------------------
def evaluate(payload):
    """Route-M's gate, both branches, committed before the run.

    M-A  the ledger contains at least one UNCERTIFIED object whose unknown count is at
         or below the object that WAS certified.  (If this fails, the leg's answer is
         'no target exists', and the plan says STOP and report.)
    M-B  the feasibility algebra reproduces a published certificate's radius.
    M-C  the 3D Navier-Stokes preprint's scalar closure is checked, both forms, and the
         result is RECORDED whichever way it comes out.
    M-D  the top-ranked object's residual ladder FALLS under refinement with the
         dissipation going to zero -- the measured half of "within reach".
    M-E  and it stays the RIGHT object while doing so: the normalization-independent
         contraction ratio stays within 5% of CHL's -2.5114 on every rung.
    M-F  the contrast is real: the 2D object's committed ladder goes the OTHER way.
    """
    C = {}
    g = payload["M1_ledger"]["gate"]
    C["M-A_uncertified_reachable_target_exists"] = (
        g["gate"] == "YES" and g["named_target"] is not None)
    C["M-B_algebra_reproduces_published_radius"] = (
        payload["M2_feasibility"]["cln_kawahara"]["rel_err_vs_published_r0"] < 1e-2)
    a = payload["M2_feasibility"]["ns_preprint_audit"]
    C["M-C_ns_closure_audited_both_forms"] = (
        "closure_as_printed_2dMK" in a and "closure_corrected_2M2Kdelta" in a)
    lad = payload["M3_reachability"]["residual_ladder"]
    C["M-D_residual_falls_under_refinement"] = lad["classification"] == "FALLING"
    C["M-E_ratio_holds_across_the_ladder"] = all(
        r["ratio_err_vs_CHL"] < 0.05 for r in payload["M3_reachability"]["rungs"])
    k = payload["M4_contrast_2d"]
    C["M-F_2d_object_goes_the_other_way"] = bool(
        k.get("available") and k["grows_under_refinement"])
    C["M-G_candidate_does_not_limit_cycle_in_tau"] = all(
        (not r["tau_direction"].get("refused"))
        and (not r["tau_direction"]["limit_cycles"])
        for r in payload["M3_reachability"]["rungs"])
    return C


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="short ladder (201/401) for a smoke run, not for the record")
    ap.add_argument("--tau", type=float, default=TAU_END)
    args = ap.parse_args()

    ns = (201, 401) if args.quick else (401, 801, 1601)
    tau_end = 8.0 if args.quick else args.tau

    print("ROUTE-M v1: target selection -- 'certify WHAT, that isn't already done?'",
          flush=True)

    # ---- M1 -------------------------------------------------------------
    print("\n[M1] the ledger", flush=True)
    m1 = {"counts": ledger_counts(), "rank_table": rank_table(),
          "gate": gate_verdict(),
          "uncertified": [{"rank": t["rank"], "id": t["id"], "object": t["object"],
                           "source": t["source"], "q3": t["q3"]}
                          for t in uncertified_targets()],
          "certified_objects": [{"object": c["object"], "proof_kind": c["proof_kind"],
                                 "source": c["source"]}
                                for c in CERTIFICATION_RECORD],
          "ledger": [{k: v for k, v in t.items() if k != "q2"} | {"q2": t["q2"]}
                     for t in TARGET_LEDGER]}
    for r in m1["rank_table"]:
        print(f"    rank {r['rank']}  {r['id']:32s} {r['certified']:18s} "
              f"dim={r['dim']} fields={r['n_fields']} mod={r['n_modulation']}  "
              f"unknowns={r['unknowns']:>10d}  ratio={r['ratio']:.3e}", flush=True)
    print(f"    GATE: {m1['gate']['gate']}  -> {m1['gate']['named_target']}", flush=True)

    # ---- M2 -------------------------------------------------------------
    print("\n[M2] the feasibility algebra", flush=True)
    cln = cln_kawahara_check()
    ns_audit = ns_preprint_closure_audit()
    # the budget curve: what residual a certificate tolerates, as Z1 and Z2 vary
    budget = [{"Z1": z1, "Z2": z2, "Y0_budget": y0_budget(z1, z2)}
              for z1 in (0.0, 0.25, 0.5, 0.75, 0.9)
              for z2 in (1e0, 1e2, 1e4)]
    m2 = {"cln_kawahara": cln, "ns_preprint_audit": ns_audit, "budget_grid": budget,
          "worked_example": radii_polynomial(1e-8, 0.3, 1e3)}
    print(f"    CLN Kawahara: published r0={cln['r0_published']:.3e}, ours "
          f"{cln['r_from_our_algebra']:.3e}, rel err {cln['rel_err_vs_published_r0']:.1e}",
          flush=True)
    print(f"    NS preprint closure: printed 2*d*M*K = "
          f"{ns_audit['closure_as_printed_2dMK']:.3e}; corrected 2*M^2*K*d = "
          f"{ns_audit['closure_corrected_2M2Kdelta']:.3e}; both close = "
          f"{ns_audit['both_close']}", flush=True)

    # ---- M3 -------------------------------------------------------------
    print(f"\n[M3] reachability of {m1['gate']['named_target']}: refinement ladder to "
          f"tau={tau_end}, nu -> 0 with the grid", flush=True)
    jobs = [(n, NU_REF * ((N_REF - 1) / (n - 1)), tau_end) for n in ns]   # nu ~ drho
    print(f"    rungs {[j[0] for j in jobs]}, nu {[round(j[1], 4) for j in jobs]}, "
          f"run in parallel", flush=True)
    with mp.Pool(len(jobs)) as pool:
        rungs = pool.map(_rung, jobs)
    for r in rungs:
        td = r["tau_direction"]
        print(f"    n={r['n']:5d} steps={r['steps']:6d} tau={r['tau']:.2f} "
              f"res={r['residual']:.4e} ratio={r['ratio']:+.4f} "
              f"(CHL {CHL_RATIO}, err {100*r['ratio_err_vs_CHL']:.2f}%) "
              f"X*={r['X_peak']:.3f} minOm={r['min_Omega']:.2e} "
              f"[{r['wall_s']:.0f}s]", flush=True)
        if not td.get("refused"):
            print(f"          tau-direction: slope={td['tail_slope_dlogres_dtau']:+.4f}/tau"
                  f"  final/min={td['final_over_min']:.3f}"
                  f"  min at tau={td['tau_at_min']:.1f}"
                  f"  limit_cycles={td['limit_cycles']}", flush=True)
    m3 = {"tau_end": tau_end, "nu_law": "nu = 0.02 * (800/(n-1))", "rungs": rungs,
          "residual_ladder": ladder_direction(rungs, "residual"),
          "ratio_ladder": ladder_direction(rungs, "ratio"),
          "chl_ratio": CHL_RATIO, "chl_triple": list(CHL_TRIPLE)}
    print(f"    residual ladder: {m3['residual_ladder']['classification']} "
          f"(net {m3['residual_ladder']['net_ratio']:.3f}, per-rung "
          f"{[round(x,3) for x in m3['residual_ladder']['step_ratios']]})", flush=True)

    # ---- M4 -------------------------------------------------------------
    print("\n[M4] the contrast -- the 2D object the port is aimed at", flush=True)
    m4 = route_k_2d_contrast()
    if m4.get("available"):
        vals = ", ".join(f"{r['residual']:.3e}" for r in m4["ladder"])
        print(f"    Route-G/K committed ladder n_r={m4['n_r']}: [{vals}] "
              f"-> net {m4['net_ratio']:.1f}x WORSE", flush=True)

    payload = {"route": "M", "version": 1,
               "question": "certify WHAT, that isn't already done?",
               "M1_ledger": m1, "M2_feasibility": m2, "M3_reachability": m3,
               "M4_contrast_2d": m4}
    payload["predicate_checks"] = evaluate(payload)
    OUT.write_text(json.dumps(payload, default=_jsonable))

    print("\n--- PRE-COMMITTED PREDICATE ---")
    for k, v in payload["predicate_checks"].items():
        print(f"    {'PASS' if v else 'FAIL'}  {k}")
    npass = sum(payload["predicate_checks"].values())
    print(f"\n{npass}/{len(payload['predicate_checks'])} clauses hold")
    print(f"wrote {OUT}")
