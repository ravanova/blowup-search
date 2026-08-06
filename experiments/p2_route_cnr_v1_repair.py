"""Leg 150, Route-CNR: the repair of solver/collocation_newton.py, and its no-op proof.

WHAT THIS RUNNER IS.  Leg 114 (Route-CNA) audited this module and its gate answered YES:
8 silent corruptions in 61 gate-scoped cases, three mechanisms (M1 the convergence flag is
blind to the row it drops; M2 the one-gauge system has a spurious constant root reported
converged; M3 `critical_radius` has no magnitude test on the sign change).  Leg 114's
territory forbade the patch under either gate branch.  This leg lands it.

The ENTIRE licence for the repair is a measured no-op guarantee on clean input, so the
runner's centre of gravity is arm B, not arm A:

  ARM A  the 8 failing cases: pre-repair verdict vs post-repair verdict.
  ARM B  ZERO REGRESSION, measured as a BITWISE differential.  The pre-repair module is read
         out of git at d4a6387 -- the module's OWN creating commit and a stable ancestor of
         main, chosen per leg 130's d871675 lesson (its first draft pinned a hash the rebase
         rewrote, so the runner stopped resolving the moment the branch landed) -- imported
         under a substituted module name, and run in the SAME PROCESS as the repaired module.
         Every returned float is compared with `==` on float64, never `allclose`.
  ARM C  the two margins the M3 threshold sits between, both measured, neither assumed.
  ARM D  blast radius: the consumers, and what gate clause (b) can and cannot be checked on.

Repo convention: self-running script, no pytest.
  Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_cnr_v1_repair.py

Emits: writeup/data/p2_route_cnr_v1_repair.json
Findings: writeup/novelty/leg_150.md, experiments/journal/leg_150.md
Battery it must invert: test_collocation_newton_adversarial.py (leg 114, 7 KNOWN GAP pins)
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import collocation_newton as POST                          # noqa: E402

PRE_REF = "d4a6387"          # the module's creating commit; stable ancestor of main
C = 0.5
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_cnr_v1_repair.json")


# ---------------------------------------------------------------------------
# the pre-repair module, read out of git, imported in THIS process
# ---------------------------------------------------------------------------


def load_prerepair(ref=PRE_REF):
    src = subprocess.check_output(["git", "show", f"{ref}:solver/collocation_newton.py"])
    sha = hashlib.sha256(src).hexdigest()
    d = tempfile.mkdtemp(prefix="cnr_prerepair_")
    path = os.path.join(d, "collocation_newton_prerepair.py")
    with open(path, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("collocation_newton_prerepair", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod, sha, len(src.splitlines())


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def hexf(x):
    """Exact float64 identity, so 'identical' means identical and not 'close'."""
    return float(x).hex()


def sha_arr(a):
    return hashlib.sha256(np.asarray(a, float).tobytes()).hexdigest()


def clean_cases():
    """Every clean/valid input shape this module is actually called on.

    a in {0 .. 0.5} is the production range (experiments/p2_route_d_v12_defect.py calls
    newton_gauged at five sites over exactly that range); the lambda-starts are the basin
    leg 114 measured as landing on the TRUE anchor; the test_4 start is the perturbed clean
    start test_collocation_newton.py gate 4 uses.
    """
    out = []
    for J, mi in ((40, 60), (60, 60), (80, 60)):
        for a in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
            out.append(dict(tag=f"a{a}_J{J}", J=J, a=a, c=C, om0=None, max_iter=mi))
    for J, mi in ((120, 25),):
        for a in (0.0, 0.3, 0.5):
            out.append(dict(tag=f"a{a}_J{J}", J=J, a=a, c=C, om0=None, max_iter=mi))
    for cc in (0.1, 0.3, 0.5, 0.8, 1.0):
        out.append(dict(tag=f"c{cc}_J60", J=60, a=0.0, c=cc, om0=None, max_iter=60))
    for lam in (0.3, 0.5, 0.8, 1.0, 1.2, 2.0, 5.0):
        out.append(dict(tag=f"lam{lam}_J60", J=60, a=0.0, c=C, om0=("lam", lam),
                        max_iter=200))
    out.append(dict(tag="test4_start_J60", J=60, a=0.0, c=C, om0=("test4", None),
                    max_iter=60))
    for drop in (1, 7, 30):
        out.append(dict(tag=f"drop{drop}_J60", J=60, a=0.0, c=C, om0=None, max_iter=60,
                        drop=drop))
    return out


def build_om0(col, spec):
    if spec is None:
        return None
    kind, v = spec
    if kind == "lam":
        return v * col.anchor()
    if kind == "test4":
        return col.anchor() * 1.2 + 0.02 * np.cos(col.theta)
    raise ValueError(kind)


FLOAT_KEYS = ("c", "kept_sup", "dropped_defect", "relres")
INT_KEYS = ("drop", "iterations")


# ---------------------------------------------------------------------------
# ARM B -- zero regression, bitwise
# ---------------------------------------------------------------------------


def arm_b(PRE):
    rows, n_ident, n_moved = [], 0, 0
    n_float_cmp = 0
    for case in clean_cases():
        J, a = case["J"], case["a"]
        kw = dict(c=case["c"], max_iter=case["max_iter"])
        if "drop" in case:
            kw["drop"] = case["drop"]
        cpre = PRE.ACollocation(J, a=a)
        cpost = POST.ACollocation(J, a=a)
        rpre = cpre.newton_gauged(om0=build_om0(cpre, case["om0"]), **kw)
        rpost = cpost.newton_gauged(om0=build_om0(cpost, case["om0"]), **kw)

        same_om = sha_arr(rpre["Omega"]) == sha_arr(rpost["Omega"])
        n_float_cmp += len(rpre["Omega"])
        diffs = []
        for k in FLOAT_KEYS:
            n_float_cmp += 1
            pa, pb = rpre[k], rpost[k]
            eq = (hexf(pa) == hexf(pb)) or (np.isnan(pa) and np.isnan(pb))
            if not eq:
                diffs.append({"key": k, "pre": hexf(pa), "post": hexf(pb)})
        for k in INT_KEYS:
            if int(rpre[k]) != int(rpost[k]):
                diffs.append({"key": k, "pre": int(rpre[k]), "post": int(rpost[k])})
        hist_same = ([hexf(x) for x in rpre["history"]]
                     == [hexf(x) for x in rpost["history"]])
        n_float_cmp += len(rpre["history"])
        conv_moved = bool(rpre["converged"]) != bool(rpost["converged"])

        ok = same_om and hist_same and not diffs and not conv_moved
        n_ident += int(ok)
        n_moved += int(not ok)
        rows.append({"tag": case["tag"], "J": J, "a": a, "c": case["c"],
                     "Omega_bitwise_identical": bool(same_om),
                     "history_bitwise_identical": bool(hist_same),
                     "float_key_diffs": diffs,
                     "converged_pre": bool(rpre["converged"]),
                     "converged_post": bool(rpost["converged"]),
                     "converged_moved": conv_moved,
                     "relres": hexf(rpost["relres"]),
                     "dropped_defect": hexf(rpost["dropped_defect"]),
                     "identical": bool(ok)})

    # critical_radius on REAL fields, both grids the consumers use
    cr_rows, cr_ident = [], 0
    for a in (0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5):
        cpre = PRE.ACollocation(60, a=a)
        cpost = POST.ACollocation(60, a=a)
        spre = cpre.newton_gauged(c=C, max_iter=60)
        Epre = PRE.effective_speed(cpre.X, cpre.V @ spre["Omega"], C, a)
        Epost = POST.effective_speed(cpost.X, cpost.V @ spre["Omega"], C, a)
        assert sha_arr(Epre) == sha_arr(Epost), "effective_speed must not move"
        vpre = PRE.critical_radius(cpre.X, Epre)
        vpost = POST.critical_radius(cpost.X, Epost)
        same = hexf(vpre) == hexf(vpost) or (np.isinf(vpre) and np.isinf(vpost))
        n_float_cmp += 1
        cr_ident += int(same)
        # and the exponent that consumes it
        ppre = PRE.zero_order(cpre.X, spre["Omega"], vpre)
        ppost = POST.zero_order(cpost.X, spre["Omega"], vpost)
        p_same = ((hexf(ppre[0]) == hexf(ppost[0])
                   or (np.isnan(ppre[0]) and np.isnan(ppost[0]))) and ppre[1] == ppost[1])
        n_float_cmp += 1
        cr_rows.append({"a": a, "Xc_pre": repr(vpre), "Xc_post": repr(vpost),
                        "identical": bool(same), "zero_order_identical": bool(p_same),
                        "zero_order_post": [repr(ppost[0]), int(ppost[1])]})

    # a log grid, the shape solver/turning_point.py builds
    Xlog = np.exp(np.linspace(np.log(1e-3), np.log(1e4), 2000))
    for a in (0.2, 0.3, 0.5):
        cpost = POST.ACollocation(60, a=a)
        s = cpost.newton_gauged(c=C, max_iter=60)
        A = cpost.to_coef @ s["Omega"]
        th = 2.0 * np.arctan(Xlog)
        U = POST.velocity_integrals(th, cpost.J) @ A
        E = POST.effective_speed(Xlog, U, C, a)
        vpre, vpost = PRE.critical_radius(Xlog, E), POST.critical_radius(Xlog, E)
        same = hexf(vpre) == hexf(vpost) or (np.isinf(vpre) and np.isinf(vpost))
        n_float_cmp += 1
        cr_ident += int(same)
        cr_rows.append({"a": a, "grid": "log2000", "Xc_pre": repr(vpre),
                        "Xc_post": repr(vpost), "identical": bool(same),
                        "zero_order_identical": None})

    # the untouched kernels, sampled
    kern = {}
    th = POST.refined_theta(60, 8)
    kern["refined_theta"] = sha_arr(th) == sha_arr(PRE.refined_theta(60, 8))
    kern["velocity_integrals"] = (sha_arr(POST.velocity_integrals(th, 60))
                                  == sha_arr(PRE.velocity_integrals(th, 60)))
    cp, cq = POST.ACollocation(60, a=0.3), PRE.ACollocation(60, a=0.3)
    om = cp.anchor()
    kern["weighted_defect"] = (hexf(POST.weighted_defect(cp, om, C, 1.0)[0])
                               == hexf(PRE.weighted_defect(cq, om, C, 1.0)[0]))
    kern["interpolant_residual"] = (sha_arr(cp.interpolant_residual(om, C, th)[0])
                                    == sha_arr(cq.interpolant_residual(om, C, th)[0]))
    kern["newton_two_gauge"] = (sha_arr(cp.newton(c0=C, max_iter=40)["Omega"])
                                == sha_arr(cq.newton(c0=C, max_iter=40)["Omega"]))
    n_float_cmp += 5

    return {"cases": rows, "n_identical": n_ident, "n_moved": n_moved,
            "critical_radius_real_fields": cr_rows,
            "critical_radius_identical": cr_ident,
            "critical_radius_total": len(cr_rows),
            "untouched_kernels_identical": kern,
            "float64_comparisons": int(n_float_cmp)}


# ---------------------------------------------------------------------------
# ARM A -- the 8 failing cases
# ---------------------------------------------------------------------------


def arm_a(PRE):
    rows = []
    cpre, cpost = PRE.ACollocation(60, a=0.0), POST.ACollocation(60, a=0.0)
    anc = cpost.anchor()

    solve_cases = [
        ("M1 third root, om0=0.1*anchor", ("lam", 0.1), C),
        ("M2 constant, om0=zeros", ("zeros", None), C),
        ("M2 constant, om0=ones", ("ones", None), C),
        ("M2 constant, om0=1e-8*anchor", ("lam", 1e-8), C),
        ("M2 constant, om0=0.01*anchor", ("lam", 0.01), C),
        ("relres has no referent, c=0", (None, None), 0.0),
    ]
    for name, spec, cc in solve_cases:
        def mk(col):
            if spec[0] == "lam":
                return spec[1] * col.anchor()
            if spec[0] == "zeros":
                return np.zeros(col.J)
            if spec[0] == "ones":
                return np.ones(col.J)
            return None
        rpre = cpre.newton_gauged(om0=mk(cpre), c=cc, max_iter=200)
        rpost = cpost.newton_gauged(om0=mk(cpost), c=cc, max_iter=200)
        rows.append({"case": name,
                     "converged_pre": bool(rpre["converged"]),
                     "converged_post": bool(rpost["converged"]),
                     "reason_post": rpost.get("reason"),
                     "kept_sup": hexf(rpost["kept_sup"]),
                     "dropped_defect_pre": float(rpre["dropped_defect"]),
                     "relres_pre": float(rpre["relres"]),
                     "relres_post": repr(rpost["relres"]),
                     "relres_has_referent": bool(rpost["relres_has_referent"]),
                     "fixed": bool(rpre["converged"] and not rpost["converged"])})

    # M3
    Xg = np.linspace(0.01, 40.0, 800)
    for eps in (1e-16, 1e-12, 1e-8, 1e-3):
        Ep = 0.5 + 0.0 * Xg
        Ep[300] = -eps
        vpre, vpost = PRE.critical_radius(Xg, Ep), POST.critical_radius(Xg, Ep)
        ppre = PRE.zero_order(Xg, -1.0 / (1.0 + Xg ** 2), vpre)
        ppost = POST.zero_order(Xg, -1.0 / (1.0 + Xg ** 2), vpost)
        rows.append({"case": f"M3 one-point dip, eps={eps:g}",
                     "Xc_pre": repr(vpre), "Xc_post": repr(vpost),
                     "zero_order_pre": [repr(ppre[0]), int(ppre[1])],
                     "zero_order_post": [repr(ppost[0]), int(ppost[1])],
                     "fixed": bool(np.isfinite(vpre) and not np.isfinite(vpost))})

    # the structural gaps
    struct = {}
    try:
        cpre.newton_gauged(c=C, max_iter=0)
        struct["max_iter_0_pre"] = "returned"
    except IndexError:
        struct["max_iter_0_pre"] = "IndexError"
    r0 = cpost.newton_gauged(c=C, max_iter=0)
    struct["max_iter_0_post"] = {"converged": bool(r0["converged"]),
                                 "iterations": int(r0["iterations"]),
                                 "reason": r0.get("reason")}

    bad = cpost.anchor().copy()
    bad[7] = np.nan
    rpost = cpost.newton(om0=bad, c0=C, max_iter=20)
    need = {"relres", "residual_rms", "iterations", "nodal_sup"}
    struct["singular_dict_missing_post"] = sorted(need - set(rpost.keys()))
    rpre2 = cpre.newton(om0=bad, c0=C, max_iter=20)
    struct["singular_dict_missing_pre"] = sorted(need - set(rpre2.keys()))
    try:
        PRE.continuation([float("nan")], J=40, max_iter=20)
        struct["continuation_nan_pre"] = "returned"
    except KeyError as exc:
        struct["continuation_nan_pre"] = f"KeyError({exc})"
    try:
        got = POST.continuation([float("nan")], J=40, max_iter=20)
        struct["continuation_nan_post"] = {"rows": len(got),
                                           "converged": bool(got[0]["converged"]),
                                           "relres": repr(got[0]["relres"])}
    except KeyError as exc:
        struct["continuation_nan_post"] = f"KeyError({exc})"

    return {"cases": rows, "structural": struct,
            "n_fixed": sum(1 for r in rows if r.get("fixed"))}


# ---------------------------------------------------------------------------
# ARM C -- the two margins the M3 threshold sits between
# ---------------------------------------------------------------------------


def arm_c():
    thresh = 1e-2
    real = []
    for a in (0.15, 0.2, 0.25, 0.3, 0.4, 0.5):
        col = POST.ACollocation(60, a=a)
        s = col.newton_gauged(c=C, max_iter=60)
        E = POST.effective_speed(col.X, col.V @ s["Omega"], C, a)
        X = np.asarray(col.X, float)
        o = np.argsort(X)
        X, Es = X[o], E[o]
        m = X > 0
        Es = Es[m]
        sg = np.where(np.diff(np.sign(Es)) != 0)[0]
        if sg.size == 0:
            continue
        i = int(sg[0])
        tail = Es[i + 1:]
        back = np.where(np.sign(tail) != np.sign(tail[0]))[0]
        run = tail[:int(back[0])] if back.size else tail
        depth = float(np.max(np.abs(run)) / np.max(np.abs(Es)))
        real.append({"a": a, "run_length": int(run.size), "rel_depth": depth,
                     "Xc": repr(POST.critical_radius(col.X, E))})
    Xg = np.linspace(0.01, 40.0, 800)
    adv = []
    for eps in (1e-16, 1e-12, 1e-8, 1e-3):
        Ep = 0.5 + 0.0 * Xg
        Ep[300] = -eps
        adv.append({"eps": eps, "run_length": 1, "rel_depth": float(eps / 0.5)})
    worst_real = min(r["rel_depth"] for r in real)
    worst_adv = max(r["rel_depth"] for r in adv)
    return {"min_rel_depth_threshold": thresh,
            "real_fields": real, "adversaries": adv,
            "worst_real_rel_depth": worst_real,
            "worst_adversary_rel_depth": worst_adv,
            "accept_side_margin": worst_real / thresh,
            "reject_side_margin": thresh / worst_adv,
            "run_length_predicate_is_dead": bool(
                min(r["run_length"] for r in real) <= 1)}


# ---------------------------------------------------------------------------
# ARM D -- blast radius / gate clause (b) bookkeeping
# ---------------------------------------------------------------------------


def arm_d():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    leg110 = os.path.join(root, "experiments", "p2_route_l1r_v1_repro.py")
    cap = open(os.path.join(root, "capabilities.py")).read()
    return {
        "leg110_repro_runner_present": os.path.exists(leg110),
        "leg110_note": ("DIRECTION.md sec 110 is ASSIGNED, not landed: no "
                        "experiments/p2_route_l1r_v1_repro.py, no writeup/novelty/leg_110.md "
                        "and no experiments/journal/leg_110.md exist on main, so gate clause "
                        "(b)'s reference to 'leg 110's death-certificate reproduction' has no "
                        "artifact to check.  Leg 110's own declared territory says 'No solver "
                        "module' -- it reads banked JSON only -- so this patch provably cannot "
                        "reach it."),
        "capabilities_validated_line": ("matches the dense Newton solve on shared problems, "
                                        "and reports the defect the certificate sees"),
        "capabilities_line_present": ("matches the dense Newton solve on shared problems"
                                      in cap),
        "consumers": ["solver/turning_point.py", "experiments/p2_route_d_v12_defect.py",
                      "experiments/p2_route_d_v13_turning.py",
                      "experiments/p2_route_d_v14_first_integral.py",
                      "test_collocation_newton.py", "test_turning_point.py",
                      "test_first_integral.py",
                      "experiments/bench_first_integral_support_guard_check.py"],
    }


def main():
    np.seterr(all="ignore")
    warnings.filterwarnings("ignore")
    PRE, sha, nlines = load_prerepair()
    print(f"pre-repair module: {PRE_REF}:solver/collocation_newton.py "
          f"sha256={sha[:16]} lines={nlines}")

    B = arm_b(PRE)
    print(f"ARM B  zero regression: {B['n_identical']}/{B['n_identical']+B['n_moved']} "
          f"clean cases bitwise identical, {B['n_moved']} moved; "
          f"critical_radius {B['critical_radius_identical']}/{B['critical_radius_total']} "
          f"identical on real fields; {B['float64_comparisons']} float64 comparisons")
    for k, v in B["untouched_kernels_identical"].items():
        print(f"       kernel {k}: {'identical' if v else 'MOVED'}")
    for r in B["cases"]:
        if not r["identical"]:
            print(f"       MOVED: {r}")

    A = arm_a(PRE)
    print(f"ARM A  {A['n_fixed']}/{len(A['cases'])} of leg 114's failing cases now "
          f"reject or report accurately")
    for r in A["cases"]:
        print(f"       {r['case']}: fixed={r.get('fixed')}")
    print(f"       structural: {json.dumps(A['structural'], default=str)[:400]}")

    Cc = arm_c()
    print(f"ARM C  M3 threshold {Cc['min_rel_depth_threshold']:g}: worst real rel-depth "
          f"{Cc['worst_real_rel_depth']:.4e} ({Cc['accept_side_margin']:.1f}x above), "
          f"worst adversary {Cc['worst_adversary_rel_depth']:.4e} "
          f"({Cc['reject_side_margin']:.1f}x below); run-length predicate dead: "
          f"{Cc['run_length_predicate_is_dead']}")

    D = arm_d()
    print(f"ARM D  leg 110 repro runner present: {D['leg110_repro_runner_present']}; "
          f"capabilities validated line present: {D['capabilities_line_present']}")

    gate_b = (B["n_moved"] == 0
              and B["critical_radius_identical"] == B["critical_radius_total"]
              and all(B["untouched_kernels_identical"].values()))
    gate_a = A["n_fixed"] == len(A["cases"])
    payload = {
        "leg": 150, "route": "ROUTE-CNR",
        "pre_repair_ref": PRE_REF, "pre_repair_sha256": sha,
        "arm_A_failing_cases": A, "arm_B_zero_regression": B,
        "arm_C_m3_margins": Cc, "arm_D_blast_radius": D,
        "gate_clause_a_all_fixed": bool(gate_a),
        "gate_clause_b_zero_movement": bool(gate_b),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, default=str)
    print(f"\nGATE (a) all failing cases fixed: {gate_a}")
    print(f"GATE (b) zero clean-input movement: {gate_b}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
