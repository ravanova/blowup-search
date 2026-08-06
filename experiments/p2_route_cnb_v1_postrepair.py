"""Leg 166, Route-CNB: the INDEPENDENT post-repair regression check of
solver/collocation_newton.py -- closing the loop on leg 150.

Leg 114 (Route-CNA) found 8 silent corruptions in 61 adversarial cases, three
mechanisms.  Leg 150 (Route-CNR) repaired all three and reported its own repair
sound.  Nobody independent has re-run it.  That matters more than usual here,
because leg 150 wrote the patch AND its own 7 pin inversions in the SAME commit
(446805b) -- the battery that certifies the repair was edited by the repair's
author.  This leg re-derives the verdict from leg 114's BANKED RECORD instead.

WHAT THIS RUNNER DOES NOT DO: it does not import, call, or replay
experiments/p2_route_cnr_v1_repair.py.  Every case here is built either from
writeup/data/p2_route_cna_v1_adversarial.json (leg 114's own JSON, the adversary
as RECORDED rather than as re-understood by the repair) or from this leg's own
grid, which is deliberately wider than and offset from leg 150's 40 cases.

ARMS
  A  leg 114's 8 SILENT_WRONG cases, parameters read out of leg 114's JSON,
     re-run against the module on disk.  Gate clause (a).
  B  bitwise differential against the PRE-REPAIR module read out of git at
     d4a6387, on this leg's own wider grid.  == on float64, never allclose;
     Omega compared by sha256 of raw bytes, scalars by hex float.  Gate clause (b).
  C  the banked batteries and the module's own gates, run as subprocesses:
     test_collocation_newton.py (the capabilities.py-registered test, line 350-353),
     test_collocation_newton_adversarial.py (leg 114's battery with leg 150's
     inversions), test_turning_point.py, test_turning_point_adversarial.py.
  D  consumer-level end-to-end: solver/turning_point.py's three critical_radius
     sites and experiments/p2_route_d_v12_defect.py's newton_gauged call shape,
     pre vs post, bitwise.  Leg 150 argued this blast radius; this leg runs it.
  E  BEYOND THE GATE -- residual-gap probes on the repaired guards.  Reported as
     magnitudes with a reachability measurement, in leg 114's own discipline
     (latent vs live), NOT as a gate answer.

Nothing here is rigorous and nothing is interval-enclosed.  solver/ is READ-ONLY
under either gate branch: this leg edits no solver module.
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from solver import collocation_newton as POST                            # noqa: E402

PRE_REF = "d4a6387"       # the module's creating commit; stable ancestor of main
CNA_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_cna_v1_adversarial.json")
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_cnb_v1_postrepair.json")

np.seterr(all="ignore")


def log(msg):
    print(f"[cnb] {msg}", flush=True)


# ---------------------------------------------------------------------------
# the pre-repair module, read out of git, imported in THIS process
# ---------------------------------------------------------------------------


def load_prerepair(ref=PRE_REF):
    src = subprocess.check_output(
        ["git", "show", f"{ref}:solver/collocation_newton.py"], cwd=ROOT)
    sha = hashlib.sha256(src).hexdigest()
    d = tempfile.mkdtemp(prefix="cnb_prerepair_")
    path = os.path.join(d, "collocation_newton_cnb_pre.py")
    with open(path, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("collocation_newton_cnb_pre", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod, sha, len(src.splitlines())


def hexf(x):
    """Exact float64 identity: 'identical' means identical, not 'close'."""
    x = float(x)
    if x != x:
        return "nan"
    return x.hex()


def arr_sha(a):
    return hashlib.sha256(np.ascontiguousarray(np.asarray(a, float)).tobytes()).hexdigest()[:16]


def same_scalar(u, v):
    """Bit equality with nan==nan and inf==inf treated as identity."""
    u, v = float(u), float(v)
    if u != u and v != v:
        return True
    return u == v


# ---------------------------------------------------------------------------
# ARM A -- leg 114's 8 SILENT_WRONG cases, from leg 114's OWN banked JSON
# ---------------------------------------------------------------------------


def arm_A(cna):
    """Re-run the 8 recorded SILENT_WRONG cases.  Gate clause (a)."""
    J = int(cna["grid_J"])
    c = float(cna["speed_c"])
    alpha = float(cna["alpha_decay_class"])
    recorded = {x["case"]: x for x in cna["cases"] if x["verdict"] == "SILENT_WRONG"}
    col = POST.ACollocation(J, a=0.0)
    anchor = col.anchor()
    out = []

    def score(case, fixed, how, mags, recorded_mags):
        out.append({"case": case, "leg114_verdict": "SILENT_WRONG",
                    "leg166_fixed": bool(fixed), "how": how,
                    "leg166_magnitudes": mags,
                    "leg114_recorded_magnitudes": recorded_mags})

    # --- M2, three starts that returned the spurious constant -----------------
    for case, om0 in (("om0_zeros", np.zeros(J)),
                      ("om0_ones", np.ones(J)),
                      ("om0_1e-8_times_anchor", 1e-8 * anchor)):
        r = col.newton_gauged(c=c, om0=om0)
        nrm = POST.__dict__.get("norm_domain")
        mags = {"converged": bool(r["converged"]),
                "converged_kept_rows": bool(r["converged_kept_rows"]),
                "kept_sup": r["kept_sup"], "dropped_defect": r["dropped_defect"],
                "relres": r["relres"], "reason": r["reason"],
                "sup_dev_from_minus_one": float(np.max(np.abs(r["Omega"] + 1.0)))}
        score(case, not r["converged"],
              "converged=False; the FULL-residual relres clause rejects it",
              mags, recorded[case]["magnitudes"])

    # --- M1, the third spurious root ------------------------------------------
    case = "om0_0.1_times_anchor"
    r = col.newton_gauged(c=c, om0=0.1 * anchor)
    score(case, not r["converged"],
          "converged=False; relres over ALL J rows exceeds relres_tol",
          {"converged": bool(r["converged"]),
           "converged_kept_rows": bool(r["converged_kept_rows"]),
           "kept_sup": r["kept_sup"], "dropped_defect": r["dropped_defect"],
           "relres": r["relres"], "reason": r["reason"]},
          recorded[case]["magnitudes"])

    # --- the structural fact: Omega = -1 is still an exact root of the system --
    # Leg 114's 5th SILENT_WRONG is not a call, it is the STATEMENT that the
    # one-gauge system has a second root.  That is a property of the equation and
    # a repair cannot delete it -- so the check is that the module no longer
    # BLESSES it, not that the root stopped existing.  Reported both ways.
    case = "constant_profile_is_an_exact_root"
    const = -np.ones(J)
    g0 = col.to_coef.sum(axis=0)
    sup_res = float(np.max(np.abs(col.residual_a(const, c))))
    gauge = float(g0 @ const + 1.0)
    r = col.newton_gauged(c=c, om0=const)
    score(case, not r["converged"],
          "the root still EXISTS (an equation property no patch can remove) but "
          "the module no longer returns it converged: relres rejects it",
          {"sup_residual_at_constant": sup_res, "gauge_row_at_constant": gauge,
           "converged_when_started_there": bool(r["converged"]),
           "converged_kept_rows": bool(r["converged_kept_rows"]),
           "relres": r["relres"], "reason": r["reason"]},
          recorded[case]["magnitudes"])

    # --- M3, the three critical_radius corruptions ---------------------------
    # VERBATIM from experiments/p2_route_cna_v1_adversarial.py lines 285-306:
    # the grid is Xg = np.linspace(0.01, 40.0, 800), the dip is E[300] = -eps on a
    # 0.5 field, and the sign noise is (-1.0)**arange(Xg.size).  Reconstructed from
    # leg 114's source, not from a paraphrase of it.
    Xg = np.linspace(0.01, 40.0, 800)

    case = "single_roundoff_scale_dip"
    depths_post, depths_pre = {}, {}
    for eps in (1e-16, 1e-12, 1e-8, 1e-3):
        E = np.full(Xg.size, 0.5)
        E[300] = -eps
        depths_post[f"dip_{eps:.0e}"] = POST.critical_radius(Xg, E)
        depths_pre[f"dip_{eps:.0e}"] = POST.critical_radius(Xg, E, min_rel_depth=0.0)
    rec = recorded[case]["magnitudes"]
    reproduces = all(same_scalar(depths_pre[k], rec[k]) for k in depths_pre)
    score(case, all(not np.isfinite(v) for v in depths_post.values()),
          "inf at all four dip depths, which is the truth; min_rel_depth=0.0 "
          "reproduces leg 114's four recorded values BIT-IDENTICALLY, so the "
          "measurement survives its own repair",
          {"Xc_post": depths_post, "Xc_at_min_rel_depth_0": depths_pre,
           "true_answer": "inf",
           "min_rel_depth_0_reproduces_leg114_record_bitwise": bool(reproduces)},
          rec)

    case = "pure_sign_noise"
    E = (-1.0) ** np.arange(Xg.size)          # leg 114's construction, verbatim
    xc_post = POST.critical_radius(Xg, E)
    xc_pre = POST.critical_radius(Xg, E, min_rel_depth=0.0)
    rec = recorded[case]["magnitudes"]
    # WHY it survives: the landed predicate is RELATIVE depth, and this field has no
    # scale -- every constant-sign run is one node long with |E| = 1 = max|E|, so the
    # excursion ratio on BOTH sides is exactly 1.0, the largest value the test can
    # ever see.  A relative test cannot reject a field whose noise IS its own maximum.
    ladder = {f"min_rel_depth={d}": POST.critical_radius(Xg, E, min_rel_depth=d)
              for d in (0.0, 1e-2, 0.1, 0.5, 0.9, 0.999, 1.0, 1.5)}
    score(case, not np.isfinite(xc_post),
          "NOT FIXED. Returns leg 114's recorded value bit-identically. The landed "
          "predicate is a RELATIVE depth and this field has no scale: both sides' "
          "excursion ratio is exactly 1.0, the maximum the test can see.",
          {"Xc_post": xc_post, "Xc_at_min_rel_depth_0": xc_pre,
           "true_answer": "undefined",
           "identical_to_leg114_record": bool(same_scalar(xc_post, rec["Xc"])),
           "identical_to_prerepair": bool(same_scalar(xc_post, xc_pre)),
           "excursion_ratio_each_side": 1.0,
           "threshold_ladder": ladder},
          rec)

    case = "chain_bogus_radius_into_zero_order"
    E = np.full(Xg.size, 0.5)
    E[300] = -1e-16
    xc = POST.critical_radius(Xg, E)
    om = col.anchor()
    p, npts = POST.zero_order(Xg, np.interp(Xg, col.X, om), xc)
    score(case, (not np.isfinite(p)) and npts == 0,
          "the bogus radius is gone, so zero_order returns (nan, 0) -- exactly "
          "what the true inf gives",
          {"Xc": xc, "p": p, "points": int(npts),
           "truth": {"p": "nan", "points": 0}},
          recorded[case]["magnitudes"])

    n_fixed = sum(1 for x in out if x["leg166_fixed"])
    return {"n_cases": len(out), "n_fixed": n_fixed,
            "n_recorded_silent_wrong": len(recorded),
            "grid_J": J, "speed_c": c, "alpha_decay_class": alpha,
            "cases": out}


# ---------------------------------------------------------------------------
# ARM B -- bitwise differential vs the pre-repair module, on THIS leg's grid
# ---------------------------------------------------------------------------


def arm_B(PRE):
    """Every previously-valid call, pre vs post, compared by == on float64.

    Deliberately NOT leg 150's 40 cases: a wider a-ladder (11 values, including
    the four leg 150 did not use), J in {40,60,80,100,120,160}, a c-ladder at
    finer spacing, every `drop` value on a small grid, and the lambda-anchor
    basin at 12 points.
    """
    cmp_count = 0
    rows = []

    def cmp_solve(tag, J, a, c, om0=None, drop=0, **kw):
        nonlocal cmp_count
        cp = PRE.ACollocation(J, a=a)
        cq = POST.ACollocation(J, a=a)
        rp = cp.newton_gauged(c=c, om0=om0, drop=drop, **kw)
        rq = cq.newton_gauged(c=c, om0=om0, drop=drop, **kw)
        fields = {}
        ok = True
        # Omega: sha256 of the raw float64 bytes
        sp, sq = arr_sha(rp["Omega"]), arr_sha(rq["Omega"])
        fields["Omega_sha"] = {"pre": sp, "post": sq}
        cmp_count += int(np.asarray(rp["Omega"]).size)
        ok &= (sp == sq)
        # the full Newton history
        hp, hq = list(rp["history"]), list(rq["history"])
        cmp_count += len(hp)
        ok &= (len(hp) == len(hq) and all(same_scalar(u, v) for u, v in zip(hp, hq)))
        fields["history_len"] = {"pre": len(hp), "post": len(hq)}
        for k in ("c", "kept_sup", "dropped_defect", "relres"):
            cmp_count += 1
            same = same_scalar(rp[k], rq[k])
            ok &= same
            fields[k] = {"pre": hexf(rp[k]), "post": hexf(rq[k]), "identical": same}
        rows.append({"case": tag, "J": J, "a": a, "c": c, "drop": drop,
                     "identical": bool(ok),
                     "converged_pre": bool(rp["converged"]),
                     "converged_post": bool(rq["converged"]),
                     "converged_kept_rows_post": bool(rq["converged_kept_rows"]),
                     "fields": fields})

    # the production a-range, at more a and more J than leg 150 used
    for J in (40, 60, 80, 100, 120, 160):
        for a in (0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5):
            cmp_solve(f"clean_J{J}_a{a}", J, a, 0.5)
    # the c-ladder
    for c in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5):
        cmp_solve(f"c{c}", 60, 0.3, c)
    # every drop value on a small grid
    for drop in range(0, 40, 4):
        cmp_solve(f"drop{drop}", 40, 0.2, 0.5, drop=drop)
    # the lambda-anchor basin, in the range that lands on the TRUE anchor
    ca = POST.ACollocation(60, a=0.0)
    anc = ca.anchor()
    for lam in (0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.3, 1.6, 2.0, 2.5, 3.5, 5.0):
        cmp_solve(f"lambda{lam}", 60, 0.0, 0.5, om0=lam * anc)

    # --- the two-gauge sibling `newton`, untouched by the repair --------------
    newton_rows = []
    for J in (40, 60, 80):
        for a in (0.0, 0.2, 0.4):
            rp = PRE.ACollocation(J, a=a).newton()
            rq = POST.ACollocation(J, a=a).newton()
            ok = (arr_sha(rp["Omega"]) == arr_sha(rq["Omega"])
                  and all(same_scalar(rp[k], rq[k])
                          for k in ("c", "residual_rms", "relres", "nodal_sup")))
            cmp_count += int(np.asarray(rp["Omega"]).size) + 4
            newton_rows.append({"case": f"newton_J{J}_a{a}", "identical": bool(ok),
                                "relres": hexf(rq["relres"]),
                                "nodal_sup": hexf(rq["nodal_sup"])})

    # --- critical_radius on REAL E fields, both consumer grids ---------------
    cr_rows = []
    for a in (0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5):
        cq = POST.ACollocation(60, a=a)
        r = cq.newton_gauged(c=0.5)
        om = r["Omega"]
        E = POST.effective_speed(cq.X, cq.V @ om, r["c"], a)
        xp = PRE.critical_radius(cq.X, E)
        xq = POST.critical_radius(cq.X, E)
        pp = PRE.zero_order(cq.X, om, xp)
        pq = POST.zero_order(cq.X, om, xq)
        cmp_count += 3
        cr_rows.append({"case": f"real_E_grid_a{a}", "a": a,
                        "n_nonfinite_E": int((~np.isfinite(E)).sum()),
                        "Xc_pre": hexf(xp), "Xc_post": hexf(xq),
                        "identical": bool(same_scalar(xp, xq)
                                          and same_scalar(pp[0], pq[0])
                                          and pp[1] == pq[1]),
                        "p_post": hexf(pq[0]), "points_post": int(pq[1])})

    # --- the untouched kernels ------------------------------------------------
    ker_rows = []
    cq, cp = POST.ACollocation(60, a=0.3), PRE.ACollocation(60, a=0.3)
    r = cq.newton_gauged(c=0.5)
    om = r["Omega"]
    th = POST.refined_theta(60, 8)
    checks = {
        "velocity_integrals": (PRE.velocity_integrals(th, 60), POST.velocity_integrals(th, 60)),
        "refined_theta": (PRE.refined_theta(60, 8), POST.refined_theta(60, 8)),
        "interpolant_residual": (cp.interpolant_residual(om, 0.5, th)[0],
                                 cq.interpolant_residual(om, 0.5, th)[0]),
        "weighted_defect": (np.array(PRE.weighted_defect(cp, om, 0.5, 2.0)[:2]),
                            np.array(POST.weighted_defect(cq, om, 0.5, 2.0)[:2])),
        "effective_speed": (PRE.effective_speed(cq.X, cq.V @ om, 0.5, 0.3),
                            POST.effective_speed(cq.X, cq.V @ om, 0.5, 0.3)),
        "eval_matrices": (np.concatenate([m.ravel() for m in PRE.eval_matrices(th, 60)]),
                          np.concatenate([m.ravel() for m in POST.eval_matrices(th, 60)])),
    }
    for name, (u, v) in checks.items():
        cmp_count += int(np.asarray(u).size)
        ker_rows.append({"kernel": name, "identical": bool(arr_sha(u) == arr_sha(v)),
                         "n_floats": int(np.asarray(u).size)})

    n_ident = sum(1 for r in rows if r["identical"])
    n_moved_converged = sum(1 for r in rows
                            if r["converged_pre"] != r["converged_post"])
    return {"n_solve_cases": len(rows), "n_identical": n_ident,
            "n_converged_flag_moved_on_clean": n_moved_converged,
            "n_float64_comparisons": cmp_count,
            "prerepair_ref": PRE_REF,
            "solves": rows,
            "two_gauge_newton": {"n": len(newton_rows),
                                 "n_identical": sum(1 for r in newton_rows if r["identical"]),
                                 "rows": newton_rows},
            "critical_radius_real_fields": {
                "n": len(cr_rows),
                "n_identical": sum(1 for r in cr_rows if r["identical"]),
                "rows": cr_rows},
            "untouched_kernels": {"n": len(ker_rows),
                                  "n_identical": sum(1 for r in ker_rows if r["identical"]),
                                  "rows": ker_rows}}


# ---------------------------------------------------------------------------
# ARM C -- the banked batteries and the module's own gates
# ---------------------------------------------------------------------------


def arm_C():
    out = []
    for name in ("test_collocation_newton.py",
                 "test_collocation_newton_adversarial.py",
                 "test_turning_point.py",
                 "test_turning_point_adversarial.py",
                 "test_first_integral.py"):
        p = os.path.join(ROOT, name)
        if not os.path.exists(p):
            out.append({"file": name, "status": "ABSENT"})
            continue
        r = subprocess.run([sys.executable, p], cwd=ROOT,
                           capture_output=True, text=True, timeout=1800)
        tail = (r.stdout or "").strip().splitlines()
        out.append({"file": name, "returncode": r.returncode,
                    "status": "PASS" if r.returncode == 0 else "FAIL",
                    "last_lines": tail[-4:] if tail else [],
                    "stderr_tail": (r.stderr or "").strip().splitlines()[-3:]})
    return {"n": len(out), "n_pass": sum(1 for x in out if x.get("status") == "PASS"),
            "runs": out}


# ---------------------------------------------------------------------------
# ARM D -- the consumers, end to end, pre vs post
# ---------------------------------------------------------------------------


def arm_D(PRE):
    """solver/turning_point.py's three critical_radius sites, and the production
    newton_gauged call shape, run pre and post and compared bitwise."""
    import solver.turning_point as TP
    rows = []
    for a in (0.1, 0.2, 0.3, 0.4, 0.5):
        # the exact expression turning_point.py uses at lines 100 / 126 / 187
        cq = POST.ACollocation(60, a=a)
        rq = cq.newton_gauged(c=0.5)
        om, c = rq["Omega"], rq["c"]
        E = POST.effective_speed(cq.X, cq.V @ om, c, a)
        xq = POST.critical_radius(cq.X, E)
        cp = PRE.ACollocation(60, a=a)
        rp = cp.newton_gauged(c=0.5)
        Ep = PRE.effective_speed(cp.X, cp.V @ om, c, a)
        xp = PRE.critical_radius(cp.X, Ep)
        rows.append({"site": "turning_point.critical_radius(col.X, ...)", "a": a,
                     "Xc_pre": hexf(xp), "Xc_post": hexf(xq),
                     "identical": bool(same_scalar(xp, xq)),
                     "converged_post": bool(rq["converged"]),
                     "relres_post": rq["relres"]})
    # the production call shape of experiments/p2_route_d_v12_defect.py:
    # newton_gauged(c=...) with om0=None, then the certificate-visible defect
    prod = []
    for a in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        cq = POST.ACollocation(60, a=a)
        rq = cq.newton_gauged(c=0.5)
        cp = PRE.ACollocation(60, a=a)
        rp = cp.newton_gauged(c=0.5)
        wq = POST.weighted_defect(cq, rq["Omega"], rq["c"], 2.0)
        wp = PRE.weighted_defect(cp, rp["Omega"], rp["c"], 2.0)
        prod.append({"a": a,
                     "converged_pre": bool(rp["converged"]),
                     "converged_post": bool(rq["converged"]),
                     "Omega_identical": bool(arr_sha(rp["Omega"]) == arr_sha(rq["Omega"])),
                     "dropped_defect": hexf(rq["dropped_defect"]),
                     "relres": hexf(rq["relres"]),
                     "weighted_defect_pre": hexf(wp[0]),
                     "weighted_defect_post": hexf(wq[0]),
                     "weighted_defect_identical": bool(same_scalar(wp[0], wq[0]))})
    # turning_point's own top-level entry points, if they run
    tp_calls = []
    for fn in ("homogeneous_far_field",):
        if hasattr(TP, fn):
            tp_calls.append({"fn": fn, "present": True})
    n_ok = sum(1 for r in rows if r["identical"])
    n_prod = sum(1 for r in prod if r["Omega_identical"] and r["weighted_defect_identical"])
    return {"critical_radius_sites": {"n": len(rows), "n_identical": n_ok, "rows": rows},
            "production_defect_path": {"n": len(prod), "n_identical": n_prod,
                                       "n_converged_post": sum(1 for r in prod if r["converged_post"]),
                                       "rows": prod},
            "turning_point_entry_points": tp_calls}


# ---------------------------------------------------------------------------
# ARM E -- residual-gap probes (BEYOND the gate; reported, not scored)
# ---------------------------------------------------------------------------


def arm_E(PRE):
    """Does the repaired magnitude guard have a bypass, and is it reachable?

    critical_radius computes `thresh = min_rel_depth * max|E|` and applies the
    magnitude test only `if thresh > 0.0`; and _run_extent returns None -- "this
    leg cannot judge the magnitude here" -- for any constant-sign run containing
    a non-finite value, which the caller treats as ACCEPT.  Both routes mean a
    single non-finite entry in E turns the guard off.
    """
    col = POST.ACollocation(60, a=0.0)
    X = col.X
    probes = []

    def dip_field(poison=None, pi=3):
        E = np.full(X.size, 0.5)
        E[X.size // 2] = -1e-16          # leg 114's M3 adversary, verbatim
        if poison is not None:
            E[pi] = poison
        return E

    base = dip_field()
    xc_clean = POST.critical_radius(X, base)
    xc_pre = PRE.critical_radius(X, base)
    for label, poison in (("no_poison", None), ("one_nan", np.nan),
                          ("one_posinf", np.inf), ("one_neginf", -np.inf)):
        E = dip_field(poison)
        xq = POST.critical_radius(X, E)
        xp = PRE.critical_radius(X, E)
        thresh = float(1e-2 * np.max(np.abs(E)))
        probes.append({
            "field": f"leg114_M3_adversary_plus_{label}",
            "thresh_computed_by_the_guard": hexf(thresh),
            "guard_active": bool(thresh > 0.0),
            "Xc_post": hexf(xq), "Xc_pre": hexf(xp),
            "post_equals_pre": bool(same_scalar(xq, xp)),
            "true_answer": "inf",
            "guard_bypassed": bool(np.isfinite(xq) and same_scalar(xq, xp))})

    # reachability: does a REAL E field ever carry a non-finite entry?
    reach = []
    for a in (0.2, 0.3, 0.5):
        cq = POST.ACollocation(60, a=a)
        r = cq.newton_gauged(c=0.5)
        om = r["Omega"]
        A = cq.to_coef @ om
        Egrid = POST.effective_speed(cq.X, cq.V @ om, r["c"], a)
        reach.append({"a": a, "grid": "collocation col.X",
                      "n_nonfinite": int((~np.isfinite(Egrid)).sum()),
                      "max_abs_E": hexf(np.max(np.abs(Egrid))),
                      "X_max": hexf(np.max(cq.X))})
        for Xmax in (1e6, 1e8, 1e10, 1e12, 1e14, 1e16):
            Xl = np.exp(np.linspace(np.log(1e-3), np.log(Xmax), 2000))
            th = 2.0 * np.arctan(Xl)
            _, _, Im = POST.eval_matrices(th, cq.J)
            El = POST.effective_speed(Xl, Im @ A, r["c"], a)
            nf = int((~np.isfinite(El)).sum())
            reach.append({"a": a, "grid": f"log grid to X={Xmax:.0e}",
                          "n_nonfinite": nf,
                          "max_abs_E": hexf(np.max(np.abs(El))),
                          "guard_active": bool(np.isfinite(np.max(np.abs(El)))
                                               and float(1e-2 * np.max(np.abs(El))) > 0.0)})
    return {"probes": probes,
            "n_bypassed": sum(1 for p in probes if p["guard_bypassed"]),
            "Xc_clean_adversary_post": hexf(xc_clean),
            "Xc_clean_adversary_pre": hexf(xc_pre),
            "reachability": reach,
            "consumer_default_X_max": 1e8,
            "note": ("turning_point.py feeds critical_radius ONLY col.X (0 non-finite "
                     "at every a measured) and its log grid defaults to X_max=1e8, "
                     "below the onset of non-finite E. The bypass is LATENT, not live "
                     "-- the same status leg 114 measured for M3 itself.")}


# ---------------------------------------------------------------------------
# ARM F -- can the LANDED PREDICATE CLASS be tuned to cover the surviving case?
# ---------------------------------------------------------------------------


def arm_F():
    """Is `pure_sign_noise` a mis-tuned threshold or a predicate that cannot cover it?

    This is the control lesson 90 demands -- one that CAN report the other answer.
    If some `min_rel_depth` rejects the sign-noise field while leaving every real
    crossing intact, the gap is a tuning bug and the finding is small.  If the two
    requirements are disjoint over the whole parameter range, the predicate CLASS is
    the ceiling and no threshold repairs it.
    """
    Xg = np.linspace(0.01, 40.0, 800)
    Enoise = (-1.0) ** np.arange(Xg.size)

    real = []
    for a in (0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5):
        col = POST.ACollocation(60, a=a)
        r = col.newton_gauged(c=0.5)
        E = POST.effective_speed(col.X, col.V @ r["Omega"], r["c"], a)
        if np.isfinite(POST.critical_radius(col.X, E)):
            real.append((a, col.X, E))

    ladder = []
    for d in (0.0, 1e-3, 1e-2, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999,
              1.0, 1.0000001, 1.1, 1.5, 2.0):
        noise_rejected = not np.isfinite(POST.critical_radius(Xg, Enoise, min_rel_depth=d))
        surviving = sum(1 for _, X, E in real
                        if np.isfinite(POST.critical_radius(X, E, min_rel_depth=d)))
        ladder.append({"min_rel_depth": d,
                       "sign_noise_rejected": bool(noise_rejected),
                       "real_crossings_surviving": int(surviving),
                       "real_crossings_total": len(real),
                       "BOTH": bool(noise_rejected and surviving == len(real))})

    works = [x for x in ladder if x["BOTH"]]
    return {"n_real_crossing_fields": len(real),
            "ladder": ladder,
            "n_thresholds_that_do_both": len(works),
            "verdict": ("NO admissible min_rel_depth separates them: every value that "
                        "rejects the sign-noise field (d > 1.0) also rejects EVERY real "
                        "crossing, because a relative-depth test is scale-invariant and "
                        "this field's excursion ratio is exactly 1.0 on both sides. The "
                        "predicate CLASS is the ceiling, not the threshold."
                        if not works else
                        "a threshold exists that does both -- the gap is tuning, not class")}


# ---------------------------------------------------------------------------
# ARM G -- which of leg 114's 8 did leg 150's own arm A actually cover?
# ---------------------------------------------------------------------------


def arm_G(cna):
    """Read leg 150's banked arm A and map its cases onto leg 114's 8.

    Leg 150 reported '10/10 gate-scoped failing cases fixed'.  This arm asks a
    different question -- 10 out of WHICH 10 -- by reading its own JSON.
    """
    path = os.path.join(ROOT, "writeup", "data", "p2_route_cnr_v1_repair.json")
    if not os.path.exists(path):
        return {"status": "leg 150 JSON absent"}
    with open(path) as fh:
        cnr = json.load(fh)
    names = [c if isinstance(c, str) else c.get("case")
             for c in cnr["arm_A_failing_cases"]["cases"]]
    # leg 150's case labels -> leg 114's case names
    mapping = {
        "om0_zeros": "M2 constant, om0=zeros",
        "om0_ones": "M2 constant, om0=ones",
        "om0_1e-8_times_anchor": "M2 constant, om0=1e-8*anchor",
        "om0_0.1_times_anchor": "M1 third root, om0=0.1*anchor",
        "single_roundoff_scale_dip": "M3 one-point dip, eps=1e-16",
        "constant_profile_is_an_exact_root": None,
        "pure_sign_noise": None,
        "chain_bogus_radius_into_zero_order": None,
    }
    leg114_cases = [c["case"] for c in cna["cases"] if c["verdict"] == "SILENT_WRONG"]
    covered, uncovered = [], []
    for c in leg114_cases:
        tgt = mapping.get(c)
        if tgt is not None and tgt in names:
            covered.append(c)
        else:
            uncovered.append(c)
    return {"leg150_reported_n_fixed": cnr["arm_A_failing_cases"]["n_fixed"],
            "leg150_arm_A_case_labels": names,
            "leg114_silent_wrong_cases": leg114_cases,
            "n_of_leg114_8_covered_by_leg150": len(covered),
            "covered": covered,
            "n_uncovered": len(uncovered),
            "uncovered": uncovered,
            "note": ("Leg 150's 10 cases are 5 of leg 114's 8 (the M3 one-point dip "
                     "appears 4 times, at 4 dip depths, as 4 of the 10) plus 2 cases "
                     "leg 150 introduced itself (om0=0.01*anchor, and the c=0 "
                     "no-referent case). Three of leg 114's 8 were never re-run by the "
                     "repair leg. This leg re-runs all 8.")}


# ---------------------------------------------------------------------------


def main():
    with open(CNA_JSON) as fh:
        cna = json.load(fh)
    PRE, pre_sha, pre_lines = load_prerepair()
    post_src = open(os.path.join(ROOT, "solver", "collocation_newton.py"), "rb").read()

    log("arm A: leg 114's 8 failing cases")
    A = arm_A(cna)
    log(f"arm A done: {A['n_fixed']}/{A['n_cases']} fixed")
    log("arm B: bitwise differential vs d4a6387")
    B = arm_B(PRE)
    log(f"arm B done: {B['n_identical']}/{B['n_solve_cases']} identical")
    log("arm C: banked batteries (subprocesses)")
    C = arm_C()
    log(f"arm C done: {C['n_pass']}/{C['n']} pass")
    log("arm D: consumers")
    D = arm_D(PRE)
    log("arm D done")
    log("arm E: residual-gap probes")
    E = arm_E(PRE)
    log("arm E done")
    log("arm F: predicate-class control")
    F = arm_F()
    log("arm F done")
    log("arm G: leg 150 coverage audit")
    G = arm_G(cna)
    log("arm G done")

    clause_a = (A["n_fixed"] == A["n_cases"] == 8)
    clause_b = (B["n_identical"] == B["n_solve_cases"]
                and B["n_converged_flag_moved_on_clean"] == 0
                and B["two_gauge_newton"]["n_identical"] == B["two_gauge_newton"]["n"]
                and B["critical_radius_real_fields"]["n_identical"]
                == B["critical_radius_real_fields"]["n"]
                and B["untouched_kernels"]["n_identical"] == B["untouched_kernels"]["n"]
                and C["n_pass"] == C["n"]
                and D["critical_radius_sites"]["n_identical"] == D["critical_radius_sites"]["n"]
                and D["production_defect_path"]["n_identical"] == D["production_defect_path"]["n"])

    doc = {
        "leg": 166, "route": "ROUTE-CNB",
        "module": "solver/collocation_newton.py",
        "module_sha256_post": hashlib.sha256(post_src).hexdigest()[:16],
        "module_lines_post": len(post_src.splitlines()),
        "module_sha256_pre": pre_sha[:16], "module_lines_pre": pre_lines,
        "prerepair_ref": PRE_REF,
        "gate": ("Post-repair, does solver/collocation_newton.py (a) reject or correctly "
                 "flag every one of leg 114's original 8 failing cases in an independent "
                 "re-run, and (b) reproduce leg 110's death-certificate reproduction and "
                 "every other previously-validated result bit-identically?"),
        "clause_a_answer": "YES" if clause_a else "NO",
        "clause_b_answer": "YES" if clause_b else "NO",
        "gate_answer": "YES" if (clause_a and clause_b) else "NO",
        "clause_b_leg110_referent": {
            "status": "DOES NOT EXIST",
            "evidence": ["DIRECTION.md section 110 still reads ASSIGNED",
                         "experiments/journal/leg_110.md absent",
                         "writeup/novelty/leg_110.md absent",
                         "experiments/p2_route_l1r_v1_repro.py absent",
                         "writeup/data/p2_route_l1r_v1_repro.json absent"],
            "note": ("Reported as a non-existent referent rather than scored, per "
                     "standing lesson 73. Independently re-verified at this leg's own "
                     "merge base; leg 150 section 5 found the same. The checkable form "
                     "of the clause -- bit-identity against the pre-repair module and "
                     "the capabilities.py-registered test -- is run in arms B, C, D.")},
        "arm_A_leg114_failing_cases": A,
        "arm_B_bitwise_differential": B,
        "arm_C_banked_batteries": C,
        "arm_D_consumers": D,
        "arm_E_residual_gap_probes_BEYOND_GATE": E,
        "arm_F_predicate_class_control": F,
        "arm_G_leg150_arm_A_coverage_audit": G,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, default=float)

    print(f"ARM A  leg 114's failing cases : {A['n_fixed']}/{A['n_cases']} fixed")
    print(f"ARM B  bitwise differential    : {B['n_identical']}/{B['n_solve_cases']} solves "
          f"identical, {B['n_float64_comparisons']} float64 comparisons, "
          f"{B['n_converged_flag_moved_on_clean']} converged flags moved on clean input")
    print(f"       two-gauge newton        : {B['two_gauge_newton']['n_identical']}/"
          f"{B['two_gauge_newton']['n']}")
    print(f"       critical_radius real E  : {B['critical_radius_real_fields']['n_identical']}/"
          f"{B['critical_radius_real_fields']['n']}")
    print(f"       untouched kernels       : {B['untouched_kernels']['n_identical']}/"
          f"{B['untouched_kernels']['n']}")
    print(f"ARM C  banked batteries        : {C['n_pass']}/{C['n']} pass")
    print(f"ARM D  consumer sites          : "
          f"{D['critical_radius_sites']['n_identical']}/{D['critical_radius_sites']['n']} "
          f"critical_radius, "
          f"{D['production_defect_path']['n_identical']}/{D['production_defect_path']['n']} "
          f"production defect path")
    print(f"ARM E  guard bypass probes     : {E['n_bypassed']}/{len(E['probes'])} bypassed "
          f"(BEYOND the gate; latent, see JSON)")
    print(f"ARM F  predicate-class control : {F['n_thresholds_that_do_both']}/"
          f"{len(F['ladder'])} thresholds reject the sign noise AND keep all "
          f"{F['n_real_crossing_fields']} real crossings")
    print(f"ARM G  leg 150 arm A coverage  : {G['n_of_leg114_8_covered_by_leg150']}/8 of "
          f"leg 114's SILENT_WRONG cases; uncovered = {G['uncovered']}")
    for x in A["cases"]:
        if not x["leg166_fixed"]:
            print(f"       NOT FIXED -> {x['case']}: {x['how']}")
    print(f"\nCLAUSE (a) {doc['clause_a_answer']}   CLAUSE (b) {doc['clause_b_answer']}   "
          f"GATE {doc['gate_answer']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
