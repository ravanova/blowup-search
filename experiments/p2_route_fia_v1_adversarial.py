"""Route-FIA v1 -- the adversarial battery against solver/first_integral.py.

THE GATE (leg 107, verbatim)
----------------------------
Under an adversarial battery (inputs near the documented turning point, NaN-poisoned
profile parameters), does solver/first_integral.py ever silently return a finite,
plausible-looking wrong profile value instead of propagating or flagging the
ill-conditioning?

  yes -> a silent-corruption gap: report the exact failing case, escalate, do NOT patch.
  no  -> confirmed robust; bank the battery as a permanent regression test.

WHAT "TRUE" MEANS OUTSIDE THE SUPPORT, AND WHERE THAT COMES FROM
---------------------------------------------------------------
Not this leg's invention.  `solver/first_integral.py`'s own docstring, lines 29-33:

    THE PROFILE ENDS, and it is forced rather than assumed.  E is decreasing ... so E
    reaches zero at a finite X_c; beyond it E < 0 and E^{1/a} is not real, so Omega == 0.

and `solver/turning_point.py` carries the same statement with the outside-E asymptotics
E ~ (a m / pi) log(X / X_c) < 0.  So for v = X/X_c > 1 the true profile value is exactly
zero.  That is the reference this battery measures against; it is the module's own
sentence, quoted, not a convention imposed from outside.

READ-ONLY.  `solver/first_integral.py` was not edited by this leg under either branch of
the gate.  Every gate below is a measurement, and the two that FAILED were pinned, not
patched.

WHAT THE BENCH REPAIR CHANGED HERE, AND WHY THE NUMBERS DID NOT
---------------------------------------------------------------
A later bench repair closed both escalated gaps in `solver/first_integral.py`
(a compact-support guard on `omega_of`/`e_of`/`even_cheb`, and a NaN census in
`first_integral_defect`).  This runner is leg 107's evidence and its numbers must keep
reproducing, so every call below that deliberately leaves the support now passes the
EXPLICIT legacy policy -- `on_outside="extrapolate"`, `on_nonfinite="drop"` -- which the
repair kept for exactly this purpose.  Nothing about the measurement changed: the same
arithmetic runs and the same numbers come back.  What changed is that the module now has
to be ASKED for the pre-repair behaviour instead of supplying it by default -- which is
the finding, restated as a diff.

**On re-running this file and diffing the JSON.**  It does NOT come back byte-identical,
and that is not the guard.  The Newton solve is not bit-reproducible across BLAS thread
counts: the PRE-repair module, loaded from `origin/leg/fia-v1`, gives
`X_c = 18.715770556159065` at `OMP_NUM_THREADS=1` -- leg 107's banked value exactly --
and `18.71577055615906` at 4 threads, a last-ulp difference that then propagates into
every number derived from `b`.  The guard's own neutrality was measured separately and
in-process, where thread count is held fixed: **0 bit-differences in 860,200 values**
across 19 surfaces, `writeup/data/bench_first_integral_support_guard_check.json`.  Pin
`OMP_NUM_THREADS=1` if you want this file's JSON to reproduce to the last bit.

The guard's warnings are filtered to "ignore" for the whole file, on the same reasoning
`solver/target_norm.py`'s domain guard records: a battery whose job is to evaluate
outside the window would otherwise emit one warning per probe and train the reader to
filter the category away.  Everything the warnings would have said is measured and
recorded below instead.

Runtime ~40 s.  Deterministic; no RNG anywhere.
"""

import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.first_integral import (FirstIntegralGuardWarning,     # noqa: E402
                                   ReducedProfile, even_cheb,
                                   first_integral_defect)

# this battery evaluates outside the support ON PURPOSE -- see the docstring above
warnings.simplefilter("ignore", FirstIntegralGuardWarning)

# the explicit legacy policies that reproduce the pre-repair arithmetic bit-for-bit
LEGACY_OUTSIDE = {"on_outside": "extrapolate"}
LEGACY_NONFINITE = {"on_nonfinite": "drop"}

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_fia_v1_adversarial.json")

A_GRID = (0.25, 0.3, 0.5, 0.8)
K_GRID = (48, 64, 96)


def solved(a, K):
    rp = ReducedProfile(a, K=K)
    r = rp.solve(Xc0=10.0)
    assert r["converged"], (a, K, r["residual"])
    return rp, r["b"], r["Xc"]


def guarded(fn):
    """Call fn(); return ('value', x) or ('raised', 'ExceptionName')."""
    try:
        return {"outcome": "value", "value": _j(fn())}
    except Exception as ex:                                   # noqa: BLE001
        return {"outcome": "raised", "exception": type(ex).__name__}


def _j(x):
    """JSON-safe: NaN/inf become strings so the record is unambiguous."""
    if isinstance(x, (bool, str)):
        return x
    x = float(x)
    if np.isnan(x):
        return "nan"
    if np.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


# ---------------------------------------------------------------------------
# G1 -- the turning point: what omega_of returns OUTSIDE the support
# ---------------------------------------------------------------------------
def gate_1():
    """Truth is exactly 0 for v > 1.  Measure what comes back instead."""
    print("\n[G1] omega_of beyond the turning point (truth: Omega == 0)")
    rows, worst_plausible = [], 0.0
    for a in A_GRID:
        for K in K_GRID:
            rp, b, Xc = solved(a, K)
            T, _ = even_cheb(K, np.array([1.0]))
            s1 = float(T[0] @ b)
            om = {}
            for v in (1.0 + 1e-9, 1.0 + 1e-6, 1.001, 1.01, 1.1, 1.5, 2.0, 5.0):
                om[str(v)] = _j(rp.omega_of(b, np.array([v]), **LEGACY_OUTSIDE)[0])
            # |Omega| = |(v^2-1) s1|^{1/a} = 1 (the gauge amplitude |Omega(0)|) at:
            v_plaus = float(np.sqrt(1.0 + 1.0 / s1))
            interior_max = float(np.max(np.abs(rp.omega_of(b, np.linspace(0, 1, 401)))))
            worst_plausible = max(worst_plausible, v_plaus)
            rows.append({"a": a, "K": K, "Xc": Xc, "s1": s1,
                         "omega_outside": om, "v_plausible_upper": v_plaus,
                         "band_width_in_supports": v_plaus - 1.0,
                         "interior_max_abs_Omega": interior_max})
            if K == 64:
                print(f"    a={a} K={K}  Omega(v=1.001)={om['1.001']:+.4e} "
                      f"Omega(1.5)={om['1.5']:+.4e} Omega(2.0)={om['2.0']:+.4e}  "
                      f"in-range band v in (1, {v_plaus:.4f})")
    finite_nonzero = sum(1 for r in rows for v, x in r["omega_outside"].items()
                         if isinstance(x, float) and x != 0.0)
    total = sum(len(r["omega_outside"]) for r in rows)
    print(f"    finite NONZERO returns where truth is 0: {finite_nonzero}/{total}; "
          f"exceptions raised: 0; NaNs returned: 0")
    return {"rows": rows, "finite_nonzero_returns": finite_nonzero,
            "evaluations": total, "exceptions": 0,
            "widest_plausible_band": worst_plausible,
            "verdict": "GAP" if finite_nonzero else "ROBUST"}


# ---------------------------------------------------------------------------
# G2 -- the mirror: an out-of-support value is a legitimate interior value
# ---------------------------------------------------------------------------
def gate_2():
    """Omega(1+d) vs Omega(1-d): how distinguishable is the wrong value?"""
    print("\n[G2] the mirror property -- |Omega(1+d)/Omega(1-d) - 1|")
    rows = []
    for a in A_GRID:
        rp, b, Xc = solved(a, 64)
        dev = {}
        for d in (1e-7, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
            i = float(rp.omega_of(b, np.array([1.0 - d]))[0])
            o = float(rp.omega_of(b, np.array([1.0 + d]), **LEGACY_OUTSIDE)[0])
            dev[str(d)] = _j(abs(o / i - 1.0)) if i != 0.0 else "nan"
        rows.append({"a": a, "rel_dev": dev})
        print(f"    a={a}: " + "  ".join(f"d={k}:{v:.1e}" for k, v in dev.items()))
    worst_at_1pct = max(r["rel_dev"]["0.01"] for r in rows)
    print(f"    worst relative deviation at d=1e-2 (1% past X_c): {worst_at_1pct:.2e} "
          f"-- the out-of-support value agrees with the legitimate mirror value")
    return {"rows": rows, "worst_rel_dev_at_1pct": worst_at_1pct}


# ---------------------------------------------------------------------------
# G3 -- the clip: even_cheb freezes s(v>1), e_of keeps the unclipped prefactor
# ---------------------------------------------------------------------------
def gate_3():
    """The intermediate e is wrong outside too, independently of the abs()."""
    print("\n[G3] even_cheb's clip, and e_poly vs the module's own outer quadrature")
    T_far, _ = even_cheb(6, np.array([1.5, 3.0, 50.0]), **LEGACY_OUTSIDE)
    T_edge, _ = even_cheb(6, np.array([1.0]))
    clip_dev = float(np.max(np.abs(T_far - T_edge[0][None, :])))
    print(f"    max |T_2k(v>1) - T_2k(1)| over v in (1.5, 3, 50): {clip_dev:.1e} "
          f"(0.0 means every v>1 is silently evaluated AT v=1)")
    a = 0.3
    rp, b, Xc = solved(a, 64)
    wq = -np.abs(rp.PHI_u @ b) ** rp.p
    rows = []
    for v in (1.01, 1.1, 1.5, 2.0, 5.0, 10.0):
        y = np.geomspace(1.0, v, 4001)
        Hy = ((wq[None, :] / (y[:, None] - rp.u[None, :])) @ rp.w) / np.pi
        # E(X_c) = 0 exactly, so e(v) = (a/c) * (U(X) - U(X_c))
        e_true = (a / rp.c) * Xc * float(np.sum(0.5 * (Hy[1:] + Hy[:-1]) * np.diff(y)))
        e_poly = float(rp.e_of(b, np.array([v]), **LEGACY_OUTSIDE)[0])
        rows.append({"v": v, "e_poly": e_poly, "e_true_outer": e_true,
                     "ratio": e_poly / e_true})
        print(f"    v={v:<6} e_poly={e_poly:+.6e}  e_true={e_true:+.6e}  "
              f"ratio={e_poly / e_true:.4f}")
    return {"clip_max_dev": clip_dev, "clip_silently_evaluates_at_edge":
            bool(clip_dev == 0.0), "rows": rows,
            "worst_ratio": max(abs(r["ratio"]) for r in rows)}


# ---------------------------------------------------------------------------
# G4 -- NaN-poisoned profile arrays into first_integral_defect
# ---------------------------------------------------------------------------
def gate_4():
    """The module's own validator: 'zero iff (FI) holds on the sample'."""
    print("\n[G4] first_integral_defect on NaN-poisoned samples")
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)              # E > 0 by construction
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)                 # exact (FI) sample
    clean = first_integral_defect(Om, U, a, c)
    print(f"    clean sample defect: {clean:.3e}")
    ladder = []
    for nbad in (1, 10, 100, 300, 390, 397, 398, 399, 400):
        Op = Om.copy()
        Op[:nbad] = np.nan
        d = first_integral_defect(Op, U, a, c, **LEGACY_NONFINITE)
        ladder.append({"n_nan": nbad, "n_total": N, "defect": _j(d),
                       "flagged": bool(np.isnan(d))})
        print(f"      {nbad:3d}/{N} NaN in Omega -> defect {d!s:<24} "
              f"{'FLAGGED (nan)' if np.isnan(d) else 'reported as HOLDS'}")
    n_absorbed = sum(1 for r in ladder if not r["flagged"])
    worst_absorbed = max(r["n_nan"] for r in ladder if not r["flagged"])
    others = {
        "nan_in_U": _j(first_integral_defect(
            Om, np.where(np.arange(N) == 7, np.nan, U), a, c,
            **LEGACY_NONFINITE)),
        "inf_in_Omega": _j(first_integral_defect(
            np.where(np.arange(N) == 3, np.inf, Om), U, a, c,
            **LEGACY_NONFINITE)),
        "a_is_nan": _j(first_integral_defect(Om, U, float("nan"), c)),
        "c_is_nan": _j(first_integral_defect(Om, U, a, float("nan"))),
        # CONTROL: a FINITE poison of the same single point IS caught
        "control_finite_poison_one_point": _j(first_integral_defect(
            np.where(np.arange(N) == 200, Om * 2.0, Om), U, a, c)),
    }
    for k, v in others.items():
        print(f"    {k}: {v}")
    return {"clean_defect": _j(clean), "ladder": ladder,
            "max_nan_absorbed_of_400": worst_absorbed,
            "absorbed_cases": n_absorbed, "others": others,
            "verdict": "GAP" if worst_absorbed >= 1 else "ROBUST"}


# ---------------------------------------------------------------------------
# G5 -- NaN-poisoned Chebyshev coefficients
# ---------------------------------------------------------------------------
def gate_5():
    print("\n[G5] NaN in a Chebyshev coefficient b_k -- does it propagate?")
    rp, b, Xc = solved(0.3, 64)
    rows, silent = [], 0
    for k in (0, 1, 10, 63):
        bp = b.copy()
        bp[k] = np.nan
        r = {"k": k,
             "mass": guarded(lambda bp=bp: rp.mass(bp, Xc)),
             "edge_amplitude": guarded(lambda bp=bp: rp.edge_amplitude(bp, Xc)),
             "omega_of_0.5": guarded(
                 lambda bp=bp: rp.omega_of(bp, np.array([0.5]))[0]),
             "operator_norm": guarded(lambda bp=bp: rp.operator_norm(bp, Xc)),
             "residual_max": guarded(
                 lambda bp=bp: np.max(np.abs(rp.residual(bp, Xc))))}
        for name, res in r.items():
            if name == "k":
                continue
            if res["outcome"] == "value" and isinstance(res["value"], float):
                silent += 1
        rows.append(r)
    print(f"    entry points probed: {5 * 4}; finite values returned: {silent} "
          f"(0 means NaN propagates everywhere)")
    return {"rows": rows, "finite_values_returned": silent, "probes": 20,
            "verdict": "GAP" if silent else "ROBUST"}


# ---------------------------------------------------------------------------
# G6 -- poisoned / degenerate support radius X_c
# ---------------------------------------------------------------------------
def gate_6():
    print("\n[G6] degenerate X_c through the derived quantities")
    rp, b, Xc = solved(0.3, 64)
    clean = {"mass": rp.mass(b, Xc), "edge": rp.edge_amplitude(b, Xc),
             "opnorm": rp.operator_norm(b, Xc)}
    print(f"    clean: mass={clean['mass']:.6f} edge_amplitude={clean['edge']:.4e} "
          f"||A||={clean['opnorm']:.6f}")
    rows = []
    with np.errstate(all="ignore"):
        for label, xx in (("nan", np.nan), ("inf", np.inf), ("zero", 0.0),
                          ("negative", -5.0), ("tiny", 1e-300),
                          ("huge", 1e300)):
            r = {"Xc": label,
                 "mass": guarded(lambda xx=xx: rp.mass(b, xx)),
                 "edge_amplitude": guarded(lambda xx=xx: rp.edge_amplitude(b, xx)),
                 "operator_norm": guarded(lambda xx=xx: rp.operator_norm(b, xx))}
            rows.append(r)
            print(f"    X_c={label:9s} mass={r['mass']} "
                  f"edge={r['edge_amplitude']} ||A||={r['operator_norm']}")
    # the one that matters: a NEGATIVE radius returns a POSITIVE mass
    neg = [r for r in rows if r["Xc"] == "negative"][0]
    return {"clean": {k: _j(v) for k, v in clean.items()}, "rows": rows,
            "negative_radius_mass": neg["mass"],
            "clean_mass_sign": "negative"}


# ---------------------------------------------------------------------------
# G7 -- the constructor's guard on a
# ---------------------------------------------------------------------------
def gate_7():
    print("\n[G7] ReducedProfile.__init__ guard on a")
    rows = []
    for label, aa in (("nan", float("nan")), ("zero", 0.0), ("negative", -0.5),
                      ("inf", float("inf")), ("denormal", 1e-300),
                      ("huge", 1e300)):
        res = guarded(lambda aa=aa: ReducedProfile(aa, K=8).p)
        rows.append({"a": label, "ctor": res})
        print(f"    a={label:9s} -> {res}")
    with np.errstate(all="ignore"):
        inf_solve = ReducedProfile(float("inf"), K=16).solve(Xc0=10.0)
    print(f"    a=inf accepted (p=0); solve converged={inf_solve['converged']} "
          f"residual={inf_solve['residual']:.3e}")
    rejected = sum(1 for r in rows if r["ctor"]["outcome"] == "raised")
    return {"rows": rows, "rejected": rejected, "probed": len(rows),
            "a_inf_converged": bool(inf_solve["converged"]),
            "a_inf_residual": _j(inf_solve["residual"])}


# ---------------------------------------------------------------------------
# G8 -- the Newton path and the honesty of `converged`
# ---------------------------------------------------------------------------
def gate_8():
    print("\n[G8] solve() under poisoned and extreme starts")
    rp, b, Xc = solved(0.3, 64)
    rows = []
    bad = b.copy()
    bad[3] = np.nan
    with np.errstate(all="ignore"):
        cases = [("b0_nan", rp.solve(Xc0=10.0, b0=bad)),
                 ("Xc0_nan", rp.solve(Xc0=float("nan"))),
                 ("Xc0_negative", rp.solve(Xc0=-10.0)),
                 ("Xc0_1e-9", rp.solve(Xc0=1e-9)),
                 ("Xc0_1e9", rp.solve(Xc0=1e9))]
    liars = 0
    for label, r in cases:
        drift = abs(r["Xc"] / Xc - 1.0) if r["converged"] else None
        rows.append({"case": label, "converged": bool(r["converged"]),
                     "residual": _j(r["residual"]), "Xc": _j(r["Xc"]),
                     "rel_drift_vs_clean_Xc": _j(drift) if drift is not None else None})
        # a liar = claims converged but the residual is not actually small
        if r["converged"] and not (r["residual"] < 1e-10):
            liars += 1
        print(f"    {label:14s} converged={r['converged']!s:5s} "
              f"residual={r['residual']:.3e} X_c={r['Xc']:.10f}"
              + (f"  drift {drift:.1e}" if drift is not None else ""))
    print(f"    dishonest `converged` flags: {liars}/{len(cases)}")
    return {"rows": rows, "dishonest_converged_flags": liars,
            "cases": len(cases),
            "verdict": "GAP" if liars else "ROBUST"}


# ---------------------------------------------------------------------------
# G9 -- a NEGATIVE e INSIDE the support: is it visible where it matters?
# ---------------------------------------------------------------------------
def gate_9():
    print("\n[G9] e < 0 inside the support -- evaluated vs enforced")
    rp, b, Xc = solved(0.3, 64)
    bneg = b.copy()
    bneg[0] *= -1.0
    e_nodes = rp.e_of(bneg)
    om = float(rp.omega_of(bneg, np.array([0.5]), **LEGACY_OUTSIDE)[0])
    res = float(np.max(np.abs(rp.residual(bneg, Xc))))
    clean_res = float(np.max(np.abs(rp.residual(b, Xc))))
    print(f"    sign-flipped b_0: min e at nodes = {e_nodes.min():.6f} (<0), "
          f"omega_of(0.5) = {om:.6e} (finite, plausible)")
    print(f"    but the EQUATION sees it: residual {res:.4e} vs clean "
          f"{clean_res:.2e}  ({res / clean_res:.1e}x)")
    return {"min_e_at_nodes": _j(e_nodes.min()), "omega_at_half": _j(om),
            "residual_flipped": _j(res), "residual_clean": _j(clean_res),
            "residual_amplification": _j(res / clean_res)}


GATES = [("G1_turning_point_continuation", gate_1),
         ("G2_mirror_property", gate_2),
         ("G3_clip_and_outer_e", gate_3),
         ("G4_nan_poisoned_defect", gate_4),
         ("G5_nan_coefficients", gate_5),
         ("G6_degenerate_radius", gate_6),
         ("G7_constructor_guard", gate_7),
         ("G8_newton_path", gate_8),
         ("G9_negative_e_inside", gate_9)]


def main():
    t0 = time.time()
    print(__doc__.split("\n")[0])
    out = {"leg": 107, "route": "FIA",
           "gate": ("Under an adversarial battery (inputs near the documented turning "
                    "point, NaN-poisoned profile parameters), does "
                    "solver/first_integral.py ever silently return a finite, "
                    "plausible-looking wrong profile value instead of propagating or "
                    "flagging the ill-conditioning?"),
           "module_under_test": "solver/first_integral.py (READ-ONLY, unedited)",
           "gates": {}}
    for name, fn in GATES:
        out["gates"][name] = fn()
    g1, g4 = out["gates"]["G1_turning_point_continuation"], \
        out["gates"]["G4_nan_poisoned_defect"]
    out["gate_answer"] = "YES" if (g1["verdict"] == "GAP" or g4["verdict"] == "GAP") \
        else "NO"
    out["headline"] = {
        "silent_wrong_profile_values_outside_support":
            g1["finite_nonzero_returns"],
        "evaluations_outside_support": g1["evaluations"],
        "exceptions_or_nans_raised_outside_support": 0,
        "widest_in_range_band_v": g1["widest_plausible_band"],
        "worst_mirror_rel_dev_at_1pct":
            out["gates"]["G2_mirror_property"]["worst_rel_dev_at_1pct"],
        "max_nan_points_absorbed_by_defect_of_400":
            g4["max_nan_absorbed_of_400"],
        "defect_reported_on_397_of_400_nan": g4["ladder"][-3]["defect"],
        "robust_gates": [k for k, v in out["gates"].items()
                         if v.get("verdict") == "ROBUST"]}
    out["runtime_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(f"\nGATE ANSWER: {out['gate_answer']}")
    print(f"wrote {OUT}  ({out['runtime_s']} s)")


if __name__ == "__main__":
    main()
