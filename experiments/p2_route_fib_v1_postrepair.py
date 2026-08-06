"""Route-FIB v1 -- the INDEPENDENT post-repair regression check on solver/first_integral.py.

THE GATE (leg 135, verbatim from DIRECTION.md)
----------------------------------------------
Post-repair, does solver/first_integral.py (a) reject every fabricated value in leg 107's
original battery in an independent re-run, and (b) reproduce the previously-validated
clean results bit-identically, including the long-running gate-4 test?

  yes -> Repair confirmed solid and non-regressive.  Bank leg 107's battery as a
         permanent regression suite.
  no  -> An incomplete fix or a repair regression.  Report the exact case precisely;
         escalate as a priority finding, do not patch under this leg's own authority.

READ-ONLY.  `solver/first_integral.py` is not edited by this leg under either branch.
So is every file belonging to leg 107 or to the bench repair: leg 107's runner and JSON,
the bench check and its JSON, and `test_first_integral_adversarial.py` are READ, and in
one case read OUT OF GIT, but never written.

WHY THE BATTERY IS READ OUT OF GIT AND NOT IMPORTED FROM `main`
---------------------------------------------------------------
The bench repair edited leg 107's own runner in place (61 lines), threading the explicit
legacy policies `on_outside="extrapolate"` / `on_nonfinite="drop"` through every call
that leaves the support, plus a module-level `simplefilter("ignore")`.  That is a
defensible choice -- it keeps leg 107's escalated numbers reproducing -- but it means the
file now on `main` asks the REPAIRED module for the PRE-repair arithmetic, so running it
cannot distinguish a repaired module from an unrepaired one.  It would "pass" identically
had the repair never landed (lesson 90: a control that cannot come out differently).

So "leg 107's original battery" here means literally leg 107's file, read from
`git show 5e03e13:experiments/p2_route_fia_v1_adversarial.py`, executed unmodified, with
every call going through the module's DEFAULT policy path -- which is the path every
caller in the repo actually takes.  It is bound to a module by substituting
`sys.modules["solver.first_integral"]`, so the SAME battery source runs against both the
pre-repair and the post-repair module in the same process.  Part A's negative control is
that substitution pointed at the pre-repair module: it must reproduce leg 107's escalated
counts exactly, or this harness is not measuring what it claims to.

WHY "BIT-FOR-BIT" IS MEASURED IN-PROCESS AND NEVER AGAINST A BANKED JSON
------------------------------------------------------------------------
Pre-registered in `writeup/novelty/leg_135.md` §3(i), before any number here was seen.
Leg 107's runner already documents that the PRE-repair module gives
X_c = 18.715770556159065 at OMP_NUM_THREADS=1 and 18.71577055615906 at 4 threads -- a
last-ULP Newton difference that propagates into everything derived from b.  A JSON diff
therefore measures the BLAS thread count, not the repair.  Every bit-comparison below
loads both modules into ONE interpreter and runs them back to back.

Runtime ~4 min at OMP_NUM_THREADS=1.  Deterministic; no RNG anywhere.
"""

import importlib.util
import json
import os
import subprocess
import sys
import time
import warnings

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_fib_v1_postrepair.json")

# the two commits this leg pivots on
REPAIR = "9c08287"          # bench: the compact-support guard + NaN census
PRE = "9c08287^"            # 95db2a1 -- the module leg 107 audited, byte-identical
LEG107 = "5e03e13"          # leg 107's landing commit; its runner BEFORE the repair edit

# Part B's grids are chosen to be DISJOINT from the bench check's own
# (A_GRID = 0.25/0.3/0.5/0.8, K_GRID = 48/64/96), so this is not the same measurement.
A_MINE = (0.2, 0.35, 0.45, 0.6, 0.75)
K_MINE = (32, 56)


# ---------------------------------------------------------------------------
# module / source loading
# ---------------------------------------------------------------------------
def git_show(spec):
    return subprocess.check_output(["git", "show", spec], cwd=ROOT).decode()


def load_module_from_source(src, name):
    """Import a .py source string as a fresh module object, without touching disk state."""
    path = os.path.join(ROOT, "writeup", "data", f".__fib_tmp_{name}.py")
    with open(path, "w") as f:
        f.write(src)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod
    finally:
        os.remove(path)


def counted(fn, *args, **kw):
    """Run fn, returning (result, number of warnings raised, category names)."""
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        val = fn(*args, **kw)
    return val, len(rec), sorted({type(w.message).__name__ for w in rec})


def bitdiff(x, y):
    """Bit-level comparison of two float arrays: NaN==NaN, -0.0 != +0.0."""
    xa = np.ascontiguousarray(np.atleast_1d(np.asarray(x, float)).ravel())
    ya = np.ascontiguousarray(np.atleast_1d(np.asarray(y, float)).ravel())
    if xa.shape != ya.shape:
        return {"n": int(xa.size), "n_bit_differences": int(max(xa.size, ya.size)),
                "shape_mismatch": [list(xa.shape), list(ya.shape)]}
    nb = int(np.count_nonzero(xa.view(np.uint64) != ya.view(np.uint64)))
    with np.errstate(invalid="ignore"):
        d = np.abs(xa - ya)
        mx = float(np.nanmax(d)) if d.size else 0.0
    return {"n": int(xa.size), "n_bit_differences": nb, "max_abs_diff": jsafe(mx)}


def jsafe(x):
    if isinstance(x, (bool, str, type(None))):
        return x
    x = float(x)
    if np.isnan(x):
        return "nan"
    if np.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


# ---------------------------------------------------------------------------
# PART A -- leg 107's ORIGINAL battery, re-run independently against both modules
# ---------------------------------------------------------------------------
def run_original_battery(fi_module, tag):
    """Execute leg 107's file (out of git at 5e03e13) bound to `fi_module`.

    main() is deliberately NOT called: it writes leg 107's JSON, which is leg 107's
    territory.  The nine gate functions are called directly, exactly as main() does.
    """
    src = git_show(f"{LEG107}:experiments/p2_route_fia_v1_adversarial.py")
    saved = sys.modules.get("solver.first_integral")
    sys.modules["solver.first_integral"] = fi_module
    try:
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always")
            bat = load_module_from_source(src, f"fia_original_{tag}")
            gates, t0 = {}, time.time()
            for name, fn in bat.GATES:
                # A gate may CRASH against the repaired module, and that is a datum, not
                # an error to route around: leg 107's G4 aggregates with
                # `max(r["n_nan"] for r in ladder if not r["flagged"])`, which has an
                # EMPTY argument once nothing is absorbed.  The battery cannot represent
                # its own repaired outcome.  Recorded verbatim; the ladder it could not
                # summarise is re-derived independently in nan_ladder_ab() below.
                try:
                    gates[name] = fn()
                except Exception as ex:                        # noqa: BLE001
                    gates[name] = {"crashed": True,
                                   "exception": type(ex).__name__, "message": str(ex)}
                    print(f"    !! {name} raised {type(ex).__name__}: {ex}")
            dt = time.time() - t0
        cats = {}
        for w in rec:
            cats[type(w.message).__name__] = cats.get(type(w.message).__name__, 0) + 1
    finally:
        if saved is not None:
            sys.modules["solver.first_integral"] = saved
        else:
            sys.modules.pop("solver.first_integral", None)
        sys.modules.pop(f"fia_original_{tag}", None)
    g1, g4 = gates["G1_turning_point_continuation"], gates["G4_nan_poisoned_defect"]
    crashed = sorted(k for k, v in gates.items() if isinstance(v, dict)
                     and v.get("crashed"))
    return {"gates": gates, "runtime_s": round(dt, 1), "warnings_by_category": cats,
            "gates_that_crashed": crashed,
            "headline": {
                "fabricated_out_of_support_values": g1["finite_nonzero_returns"],
                "out_of_support_evaluations": g1["evaluations"],
                "nan_points_absorbed_of_400": g4.get("max_nan_absorbed_of_400"),
                "absorbed_ladder_rungs": g4.get("absorbed_cases"),
                "clean_defect": g4.get("clean_defect"),
                "G1_verdict": g1["verdict"], "G4_verdict": g4.get("verdict"),
                "G4_crashed": bool(g4.get("crashed", False))}}


def nan_ladder_ab(mod_pre, mod_post):
    """Leg 107's G4 ladder, re-derived on both modules under the DEFAULT policy.

    Identical construction to leg 107's gate_4 (a = 0.3, c = 0.5, N = 400,
    X = linspace(0.01, 3, 400), E = c exp(-X^2/4), U = (E - c)/a,
    Omega = -(E/c)^{1/a}), transcribed here for one reason only: leg 107's own
    aggregator raises ValueError once no rung is absorbed, so the ladder has to be read
    off outside it.  The per-rung numbers are the battery's; only the summary is mine.
    """
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)
    rows = []
    for nbad in (1, 10, 100, 300, 390, 397, 398, 399, 400):
        Op = Om.copy()
        Op[:nbad] = np.nan
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always")
            dp = mod_pre.first_integral_defect(Op, U, a, c)
            dq = mod_post.first_integral_defect(Op, U, a, c)
        rows.append({"n_nan": nbad, "n_total": N,
                     "pre_defect": jsafe(dp), "pre_flagged": bool(np.isnan(dp)),
                     "post_defect": jsafe(dq), "post_flagged": bool(np.isnan(dq)),
                     "post_warnings": len(rec)})
    pre_absorbed = [r["n_nan"] for r in rows if not r["pre_flagged"]]
    post_absorbed = [r["n_nan"] for r in rows if not r["post_flagged"]]
    return {"rows": rows,
            "pre_absorbed_rungs": len(pre_absorbed),
            "pre_max_nan_absorbed": max(pre_absorbed) if pre_absorbed else 0,
            "post_absorbed_rungs": len(post_absorbed),
            "post_max_nan_absorbed": max(post_absorbed) if post_absorbed else 0}


def part_a(mod_pre, mod_post):
    print("\n" + "=" * 74)
    print("[A] leg 107's ORIGINAL battery (git 5e03e13), DEFAULT policies, both modules")
    print("=" * 74)
    print("  A0 negative control -- bound to the PRE-repair module "
          f"({PRE}).  Must reproduce leg 107's escalated numbers.", flush=True)
    pre = run_original_battery(mod_pre, "pre")
    hp = pre["headline"]
    print(f"      fabricated out-of-support values: {hp['fabricated_out_of_support_values']}"
          f"/{hp['out_of_support_evaluations']};  NaN points absorbed of 400: "
          f"{hp['nan_points_absorbed_of_400']};  warnings: {pre['warnings_by_category']}")
    print("\n  A1 the check -- the SAME battery source bound to the CURRENT module.",
          flush=True)
    post = run_original_battery(mod_post, "post")
    hq = post["headline"]
    print(f"      fabricated out-of-support values: {hq['fabricated_out_of_support_values']}"
          f"/{hq['out_of_support_evaluations']};  NaN points absorbed of 400: "
          f"{hq['nan_points_absorbed_of_400']};  warnings: {post['warnings_by_category']}")

    # the exact out-of-support values, case by case, pre vs post
    rows = []
    for rp_, rq_ in zip(pre["gates"]["G1_turning_point_continuation"]["rows"],
                        post["gates"]["G1_turning_point_continuation"]["rows"]):
        for v in rp_["omega_outside"]:
            rows.append({"a": rp_["a"], "K": rp_["K"], "v": float(v),
                         "pre": rp_["omega_outside"][v], "post": rq_["omega_outside"][v]})
    fabricated = [r for r in rows if isinstance(r["pre"], float) and r["pre"] != 0.0]
    now_exact_zero = [r for r in fabricated
                      if isinstance(r["post"], float) and r["post"] == 0.0
                      and not np.signbit(r["post"])]
    worst = max(fabricated, key=lambda r: abs(r["pre"])) if fabricated else None
    print(f"\n      of {len(fabricated)} pre-repair fabricated values, "
          f"{len(now_exact_zero)} are now EXACTLY +0.0")
    if worst:
        print(f"      largest fabricated value: |Omega| = {abs(worst['pre']):.6f} at "
              f"a={worst['a']} K={worst['K']} v={worst['v']} (gauge amplitude 1) "
              f"-> now {worst['post']!r}")

    # the NaN ladder, rung by rung, re-derived (leg 107's aggregator cannot summarise it)
    print("\n      the NaN ladder, DEFAULT policy, both modules "
          "(re-derived -- see nan_ladder_ab):")
    lad = nan_ladder_ab(mod_pre, mod_post)
    for r in lad["rows"]:
        print(f"      {r['n_nan']:3d}/400 NaN: pre {str(r['pre_defect']):<24}"
              f"{'FLAGGED' if r['pre_flagged'] else 'reported as HOLDS'}"
              f"   |  post {str(r['post_defect']):<8}"
              f"{'FLAGGED' if r['post_flagged'] else 'reported as HOLDS'}")
    print(f"      absorbed rungs: pre {lad['pre_absorbed_rungs']}/9 "
          f"(worst {lad['pre_max_nan_absorbed']}/400 NaN still certified) -> "
          f"post {lad['post_absorbed_rungs']}/9")

    ok = (pre["headline"]["fabricated_out_of_support_values"] == 96
          and post["headline"]["fabricated_out_of_support_values"] == 0
          and len(now_exact_zero) == len(fabricated) == 96
          and lad["pre_absorbed_rungs"] >= 1
          and lad["post_absorbed_rungs"] == 0)
    return {"pre_repair_control": pre, "post_repair": post,
            "out_of_support_cases": rows,
            "n_fabricated_pre": len(fabricated),
            "n_now_exactly_positive_zero": len(now_exact_zero),
            "largest_fabricated": worst,
            "nan_ladder": lad,
            "leg_107_aggregator_crashes_on_repaired_module":
                post["gates_that_crashed"],
            "clause_a_holds": bool(ok)}


# ---------------------------------------------------------------------------
# PART B -- in-support bit-for-bit A/B, on grids the bench check did not use
# ---------------------------------------------------------------------------
def part_b(mod_pre, mod_post):
    print("\n" + "=" * 74)
    print("[B] in-support surfaces, same process, bit-for-bit (grids disjoint from the "
          "bench's)")
    print("=" * 74, flush=True)
    SHAPE = np.linspace(0.0, 1.0, 401)          # hits v = 1 EXACTLY -- the support EDGE
    CHEB = 0.5 * (1.0 - np.cos(np.pi * (np.arange(997) + 0.5) / 997))
    rows = []
    for a in A_MINE:
        for K in K_MINE:
            rpo = mod_pre.ReducedProfile(a, K=K)
            rpn = mod_post.ReducedProfile(a, K=K)
            with warnings.catch_warnings(record=True) as rec:
                warnings.simplefilter("always")
                ro = rpo.solve(Xc0=10.0)
                rn = rpn.solve(Xc0=10.0)
                assert ro["converged"] and rn["converged"], (a, K)
                bo, Xo = ro["b"], ro["Xc"]
                bn, Xn = rn["b"], rn["Xc"]
                To, dTo = mod_pre.even_cheb(K, CHEB)
                Tn, dTn = mod_post.even_cheb(K, CHEB)
                surf = {
                    "solve.b": bitdiff(bo, bn),
                    "solve.Xc": bitdiff([Xo], [Xn]),
                    "solve.residual": bitdiff([ro["residual"]], [rn["residual"]]),
                    "omega_of(graded nodes u)":
                        bitdiff(rpo.omega_of(bo, rpo.u), rpn.omega_of(bn, rpn.u)),
                    "omega_of(linspace(0,1,401))  [edge v=1 included]":
                        bitdiff(rpo.omega_of(bo, SHAPE), rpn.omega_of(bn, SHAPE)),
                    "e_of(linspace(0,1,401))":
                        bitdiff(rpo.e_of(bo, SHAPE), rpn.e_of(bn, SHAPE)),
                    "even_cheb T (997 Chebyshev pts)": bitdiff(To, Tn),
                    "even_cheb dT (997 Chebyshev pts)": bitdiff(dTo, dTn),
                    "residual(b, Xc)":
                        bitdiff(rpo.residual(bo, Xo), rpn.residual(bn, Xn)),
                    "jacobian(b, Xc)":
                        bitdiff(rpo.jacobian(bo, Xo), rpn.jacobian(bn, Xn)),
                    "mass": bitdiff([rpo.mass(bo, Xo)], [rpn.mass(bn, Xn)]),
                    "edge_amplitude": bitdiff([rpo.edge_amplitude(bo, Xo)],
                                              [rpn.edge_amplitude(bn, Xn)]),
                    "operator_norm": bitdiff([rpo.operator_norm(bo, Xo)],
                                             [rpn.operator_norm(bn, Xn)]),
                    "predicted_radius": bitdiff([rpo.predicted_radius(bo, Xo)],
                                                [rpn.predicted_radius(bn, Xn)]),
                    "outer_velocity": bitdiff(rpo.outer_velocity(bo, Xo),
                                              rpn.outer_velocity(bn, Xn)),
                }
            nv = sum(s["n"] for s in surf.values())
            nd = sum(s["n_bit_differences"] for s in surf.values())
            rows.append({"a": a, "K": K, "Xc": Xo, "n_surfaces": len(surf),
                         "n_values": nv, "n_bit_differences": nd,
                         "n_warnings_raised": len(rec),
                         "warning_categories": sorted({type(w.message).__name__
                                                       for w in rec}),
                         "surfaces": surf})
            print(f"    a={a:<5} K={K:<3} {nv:>7} values over {len(surf)} surfaces: "
                  f"{nd} bit-differences, {len(rec)} spurious warnings "
                  f"(X_c={Xo:.12f})", flush=True)
    tv = sum(r["n_values"] for r in rows)
    td = sum(r["n_bit_differences"] for r in rows)
    tw = sum(r["n_warnings_raised"] for r in rows)
    print(f"    TOTAL: {tv} in-support values, {td} bit-differences, "
          f"{tw} spurious warnings")

    # a clean first_integral_defect sample, both modules, default policy
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)
    do = mod_pre.first_integral_defect(Om, U, a, c)
    dn, nw, cats = counted(mod_post.first_integral_defect, Om, U, a, c)
    dbits = bitdiff([do], [dn])
    print(f"    clean first_integral_defect (400 finite pts): pre {do:.6e}  "
          f"post {dn:.6e}  -> {dbits['n_bit_differences']} bit-differences, "
          f"{nw} warnings")
    return {"rows": rows, "n_values_compared": tv, "n_bit_differences": td,
            "n_spurious_warnings": tw, "n_a_values": len(A_MINE),
            "n_K_values": len(K_MINE),
            "clean_defect": {"pre": jsafe(do), "post": jsafe(dn),
                             "n_bit_differences": dbits["n_bit_differences"],
                             "warnings": nw},
            "clause_b_in_support_holds": bool(td == 0 and tw == 0
                                              and dbits["n_bit_differences"] == 0)}


# ---------------------------------------------------------------------------
# PART C -- the downstream surface the repair's own driver never ran
# ---------------------------------------------------------------------------
def part_c(mod_pre, mod_post):
    """solver/reduced_certificate.py consumes even_cheb/e_of/graded_grid at 5 sites.

    Registered as a falsifiable prediction in writeup/novelty/leg_135.md §3(ii) BEFORE
    it was run: even_cheb and e_of had their DEFAULT changed to return NaN outside the
    support, so any call site handed |v| > 1 turns a finite certificate number into NaN.
    The bench check's A/B enumerates only the p2_route_d_v14 call sites.
    """
    print("\n" + "=" * 74)
    print("[C] the downstream consumer: solver/reduced_certificate.py (NOT in the "
          "bench A/B)")
    print("=" * 74, flush=True)
    rc_src = open(os.path.join(ROOT, "solver", "reduced_certificate.py")).read()

    # (C1) instrument the CURRENT module: what |v| do the five call sites actually see?
    seen = {"even_cheb": [], "e_of": []}
    real_even, real_e_of = mod_post.even_cheb, mod_post.ReducedProfile.e_of

    def spy_even_cheb(K, v, *a_, **k_):
        seen["even_cheb"].append(float(np.max(np.abs(np.asarray(v, float)))))
        return real_even(K, v, *a_, **k_)

    def spy_e_of(self, b, v=None, *a_, **k_):
        vv = self.u if v is None else np.asarray(v, float)
        seen["e_of"].append(float(np.max(np.abs(vv))))
        return real_e_of(self, b, v, *a_, **k_)

    def load_rc(fi_mod, name):
        saved = sys.modules.get("solver.first_integral")
        sys.modules["solver.first_integral"] = fi_mod
        try:
            return load_module_from_source(rc_src, name)
        finally:
            if saved is not None:
                sys.modules["solver.first_integral"] = saved
            else:
                sys.modules.pop("solver.first_integral", None)

    mod_post.even_cheb, mod_post.ReducedProfile.e_of = spy_even_cheb, spy_e_of
    try:
        rc_new = load_rc(mod_post, "rc_post")
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always")
            reh_new = [rc_new.rehearsal(a, K=48) for a in (0.3, 0.5)]
        warn_new = len(rec)
    finally:
        mod_post.even_cheb, mod_post.ReducedProfile.e_of = real_even, real_e_of
    max_v = {k: (max(v) if v else None) for k, v in seen.items()}
    ncalls = {k: len(v) for k, v in seen.items()}
    print(f"    call sites exercised: even_cheb x{ncalls['even_cheb']}, "
          f"e_of x{ncalls['e_of']}")
    print(f"    largest |v| ever presented: even_cheb {max_v['even_cheb']!r}, "
          f"e_of {max_v['e_of']!r}   (the guard fires at |v| > 1 + 4eps)")
    print(f"    guard warnings raised inside reduced_certificate: {warn_new}")

    # (C2) the A/B itself: same rehearsal, pre-repair first_integral underneath
    rc_old = load_rc(mod_pre, "rc_pre")
    reh_old = [rc_old.rehearsal(a, K=48) for a in (0.3, 0.5)]
    fields = ("Xc_over_c", "newton_residual", "Y0_interpolant_defect", "Z0", "opnorm")
    rows, nd_tot, nv_tot = [], 0, 0
    for ro, rn in zip(reh_old, reh_new):
        per = {f: bitdiff([ro[f]], [rn[f]]) for f in fields}
        per["N2_sup_by_cutoff"] = bitdiff(ro["N2_sup_by_cutoff"],
                                          rn["N2_sup_by_cutoff"])
        nd = sum(p["n_bit_differences"] for p in per.values())
        nv = sum(p["n"] for p in per.values())
        nd_tot += nd
        nv_tot += nv
        rows.append({"a": ro["a"], "K": ro["K"],
                     "Y0_pre": jsafe(ro["Y0_interpolant_defect"]),
                     "Y0_post": jsafe(rn["Y0_interpolant_defect"]),
                     "Z0_pre": jsafe(ro["Z0"]), "Z0_post": jsafe(rn["Z0"]),
                     "opnorm_pre": jsafe(ro["opnorm"]),
                     "opnorm_post": jsafe(rn["opnorm"]),
                     "N2_finite_pre": ro["N2_finite"],
                     "N2_finite_post": rn["N2_finite"],
                     "n_values": nv, "n_bit_differences": nd, "fields": per})
        print(f"    rehearsal(a={ro['a']}, K=48): Y_0 {ro['Y0_interpolant_defect']:.6e} "
              f"-> {rn['Y0_interpolant_defect']:.6e}, ||A|| {ro['opnorm']:.9f} -> "
              f"{rn['opnorm']:.9f}, {nd}/{nv} bit-differences")
    return {"call_sites": {"n_calls": ncalls, "max_abs_v_presented": max_v,
                           "guard_warnings_raised": warn_new,
                           "prediction_from_novelty_pass":
                               "any |v| > 1 at these sites silently becomes NaN "
                               "post-repair; measured either way",
                           "any_site_outside_support":
                               bool(any(m is not None and m > 1.0
                                        for m in max_v.values()))},
            "rehearsal_ab": rows, "n_values_compared": nv_tot,
            "n_bit_differences": nd_tot,
            "clause_b_downstream_holds": bool(nd_tot == 0 and warn_new == 0)}


# ---------------------------------------------------------------------------
# PART D -- the module's own 7 gates on current main, gate 4 included
# ---------------------------------------------------------------------------
def part_d():
    print("\n" + "=" * 74)
    print("[D] test_first_integral.py -- all 7 gates on current main (gate 4 is the "
          "long one)")
    print("=" * 74, flush=True)
    env = dict(os.environ, OMP_NUM_THREADS="1")
    t0 = time.time()
    p = subprocess.run([sys.executable, "-u", os.path.join(ROOT, "test_first_integral.py")],
                       cwd=ROOT, env=env, capture_output=True, text=True, timeout=7200)
    dt = time.time() - t0
    out = p.stdout + p.stderr
    n_pass = out.count("[PASS]")
    n_fail = out.count("[FAIL]")
    gate4 = [ln.strip() for ln in out.splitlines()
             if "vanishing no slower" in ln or "falls x" in ln]
    print(out[-1500:])
    print(f"    -> {n_pass} PASS, {n_fail} FAIL, exit {p.returncode}, {dt:.0f} s")
    return {"n_pass": n_pass, "n_fail": n_fail, "exit_code": p.returncode,
            "runtime_s": round(dt, 1), "gate_4_lines": gate4,
            "tail": out[-2000:],
            "clause_b_gates_hold": bool(p.returncode == 0 and n_fail == 0
                                        and n_pass >= 7)}


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    print(__doc__.split("\n")[0])
    print(f"repair {REPAIR}   pre-repair {PRE}   leg-107 runner {LEG107}")
    mod_pre = load_module_from_source(git_show(f"{PRE}:solver/first_integral.py"),
                                      "first_integral_prerepair")
    import solver.first_integral as mod_post          # noqa: E402
    print(f"    pre-repair module: {len(git_show(f'{PRE}:solver/first_integral.py'))} "
          f"chars; post-repair module: {os.path.getsize(mod_post.__file__)} bytes")
    assert not hasattr(mod_pre, "FirstIntegralGuardWarning"), \
        "the 'pre-repair' module has the guard -- wrong commit"
    assert hasattr(mod_post, "FirstIntegralGuardWarning"), \
        "the current module has no guard -- is the repair merged?"

    A = part_a(mod_pre, mod_post)
    B = part_b(mod_pre, mod_post)
    C = part_c(mod_pre, mod_post)
    D = part_d()

    clause_a = A["clause_a_holds"]
    clause_b = (B["clause_b_in_support_holds"] and C["clause_b_downstream_holds"]
                and D["clause_b_gates_hold"])
    out = {
        "leg": 135, "route": "FIB",
        "gate": ("Post-repair, does solver/first_integral.py (a) reject every fabricated "
                 "value in leg 107's original battery in an independent re-run, and (b) "
                 "reproduce the previously-validated clean results bit-identically, "
                 "including the long-running gate-4 test?"),
        "module_under_test": "solver/first_integral.py (READ-ONLY, unedited by leg 135)",
        "commits": {"repair": REPAIR, "pre_repair": PRE, "leg_107_runner": LEG107},
        "A_original_battery": A,
        "B_in_support_bitwise": B,
        "C_downstream_reduced_certificate": C,
        "D_module_own_gates": D,
        "clause_a_fabricated_values_rejected": clause_a,
        "clause_b_clean_results_bit_identical": clause_b,
        "gate_answer": "YES" if (clause_a and clause_b) else "NO",
        "headline": {
            "fabricated_values_pre_repair": A["n_fabricated_pre"],
            "fabricated_values_post_repair":
                A["post_repair"]["headline"]["fabricated_out_of_support_values"],
            "now_exactly_positive_zero": A["n_now_exactly_positive_zero"],
            "largest_fabricated_value_pre": (abs(A["largest_fabricated"]["pre"])
                                             if A["largest_fabricated"] else None),
            "nan_absorbed_of_400_pre": A["nan_ladder"]["pre_max_nan_absorbed"],
            "nan_absorbed_ladder_rungs_pre": A["nan_ladder"]["pre_absorbed_rungs"],
            "nan_absorbed_ladder_rungs_post": A["nan_ladder"]["post_absorbed_rungs"],
            "in_support_values_compared": B["n_values_compared"],
            "in_support_bit_differences": B["n_bit_differences"],
            "in_support_spurious_warnings": B["n_spurious_warnings"],
            "downstream_values_compared": C["n_values_compared"],
            "downstream_bit_differences": C["n_bit_differences"],
            "module_gates_pass": D["n_pass"], "module_gates_fail": D["n_fail"],
            "module_gates_runtime_s": D["runtime_s"]},
    }
    out["runtime_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True, default=str)
    print("\n" + "=" * 74)
    print(f"CLAUSE (a) fabricated values rejected : {clause_a}")
    print(f"CLAUSE (b) clean results bit-identical: {clause_b}")
    print(f"GATE ANSWER: {out['gate_answer']}")
    print(f"wrote {OUT}  ({out['runtime_s']} s)")


if __name__ == "__main__":
    main()
