"""Route-CNRV: the INDEPENDENT post-repair verification of leg 248's repair to
`solver/collocation_newton.py`.

Leg 237 (Route-SIRC) censused `solver/` for leg 202's defect class -- a boolean
convergence verdict computed from a quantity exactly invariant under the
equation's own scaling degeneracy -- and found one further instance, in
`ACollocation.newton` (and, through it, `continuation`).  Leg 248 repaired it by
ANDing an absolute, AFFINE gauge defect into the verdict.

Leg 248 wrote the patch and its own "independent" reachability re-run IN THE SAME
COMMIT.  That is exactly the situation the post-repair discipline (the 228/231-234
family, and leg 166 one repair earlier on this same module) exists to re-check
with numbers nobody who wrote the patch produced.  THIS RUNNER READS
`solver/collocation_newton.py` AND EDITS NOTHING IN IT.

THE GATE (pre-committed, DIRECTION.md 12399-12404, verbatim, both branches)
--------------------------------------------------------------------------
"Does an independent re-run confirm (a) all 41 of leg 237's reachability-battery
cases now correctly reject/flag, (b) the 2 cases reproducing leg 202's banked
numbers remain correctly flagged as genuine (no overcorrection), and (c) no
collocation_newton.py-dependent banked value moved (robustness sweep over
dependents)?"
  yes -> Bank, closing 237's finding on independently-confirmed footing.
  no  -> Name the failing case precisely; the confirmed-gap rework rule applies.

Read as it must be read (leg 248 stated this reading and it is adopted, not
re-derived): leg 237 measured 0 escapes among its 41, so "correctly" in clause
(a) means CORRECT VERDICT, not "all False".  The 17 that converge sit on the
gauged member to machine precision and a correct repair must STILL call them
converged; the 24 that do not converge must stay unconverged.  Suppressing the 17
is the overcorrection clause (b) guards against.

WHAT MAKES THIS INDEPENDENT RATHER THAN A RE-READING (four things)
------------------------------------------------------------------
 1. Section A rebuilds leg 237's 41-case trial space FROM ITS DOCSTRING, in this
    file, and recomputes the CORRECT verdict for every case FROM THE RETURNED
    (Omega, c) ALONE -- this leg's own `relres`, this leg's own `gauge_defect`
    from the formula in the module's docstring -- then compares that against what
    the module REPORTED.  A bug in how the module computes-and-returns
    `gauge_defect` (as opposed to a bug in the gate consuming it) is invisible to
    any check that reads the field.  Section A' additionally calls leg 237's OWN
    `g5_reachability`, unmodified, as a replication cross-check.
 2. Section B re-derives leg 202's calibration pair from `solver/profile_newton.py`
    directly -- not from leg 202's JSON, not from leg 248's, not through leg 237's
    `g3b` wrapper.
 3. Section C is gate clause (c), which is NEW relative to leg 248's own gate
    (clauses (a) and (b) only).  It compares the post-repair module against the
    genuine PRE-REPAIR SOURCE read out of git at `1ea4ecd` -- a differential that
    can come out non-zero -- rather than against `gauge_tol=inf`, which is the
    module's own self-description of what pre-repair meant.
 4. Every control here is one that can come out differently (lesson 90), and
    section G is the comparator's own self-test: the float-move detector is shown
    firing on a deliberately moved float, so "0 floats moved" is a measurement and
    not a property of the comparison code.

MAGNITUDES, NOT BOOLEANS (standing discipline).  Every clause is banked with the
separation that decides it, in the units it is decided in.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous: this
is a regression verification of a solver-hygiene repair, not a bound.

RUN IT WITH BLAS PINNED -- leg 166 measured a ~100x wall-clock difference from
thread oversubscription on exactly this module's dense solves:
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        .venv/bin/python experiments/p2_route_cnrv_v1_postrepair.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if os.path.join(ROOT, "experiments") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "experiments"))

from solver.collocation_newton import (ACollocation, continuation,    # noqa: E402
                                       critical_radius, effective_speed)
from solver import profile_newton                                     # noqa: E402

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_cnrv_v1_postrepair.json")

# leg 237's own escape predicate, adopted by leg 248 as `gauge_tol`'s default.
GAUGE_TOL = 1e-8
# `gauge_tol=inf` is the module's documented pre-repair reproduction path.
PRE_TOL = float("inf")
# the last commit before leg 248 touched the module -- the GENUINE pre-repair source
PRE_REPAIR_REV = "1ea4ecd"

# leg 202's banked numbers, transcribed from leg 248's gate clause (b) wording
LEG202_BANKED_C = {1e-8: -6127.94, 1e-10: -306421.26}


# ---------------------------------------------------------------------------
# this leg's own re-derivation of the two quantities the verdict is made of
# ---------------------------------------------------------------------------

def independent_gauge_defect(col, om):
    """max(|Omega(theta=0) + 1|, |Omega(node nearest X=1) + 1/2|).

    Transcribed from the formula in `ACollocation.newton`'s own docstring and
    evaluated HERE, from the returned Omega, with no reference to the module's
    internal bookkeeping or its returned `gauge_defect` field.
    """
    g0 = col.to_coef.sum(axis=0)
    i1 = int(np.argmin(np.abs(col.X - 1.0)))
    om = np.asarray(om, float)
    return float(max(abs(float(g0 @ om) + 1.0), abs(float(om[i1]) + 0.5)))


def independent_relres(col, om, c):
    """rms(R) / rms(Omega H(Omega)), recomputed here from (Omega, c)."""
    om = np.asarray(om, float)
    R = col.residual_a(om, float(c))
    src = om * (col.H @ om)
    den = float(np.sqrt(np.mean(src ** 2)))
    if not np.any(src):
        return float("inf")
    return float(float(np.sqrt(np.mean(R ** 2))) / den)


def correct_verdict(relres, gauge_defect, gauge_tol=GAUGE_TOL):
    """What `converged` OUGHT to be: the relative test AND the absolute one.

    Both halves are stated here rather than imported, so this is an independent
    statement of the specification and not a re-execution of the module's code.
    """
    return bool(relres < 1e-9 and gauge_defect <= gauge_tol)


# ---------------------------------------------------------------------------
# A -- clause (a): leg 237's 41-case trial space, rebuilt here from its docstring
# ---------------------------------------------------------------------------

def battery_cases(col, ref_om, ref_c, seeds=20, seed=0):
    """Leg 237's trial space A..E, re-derived from `g5_reachability`'s docstring.

    Yields (route, label, kwargs-for-newton).  Route F (the a-ladder through
    `continuation`) is measured separately in section E because it is a different
    entry point, exactly as leg 237 treated it.
    """
    out = []
    for lam in (0.01, 0.1, 1.5, 2.0, 5.0, 10.0, 100.0, 1000.0):
        out.append(("A_lambda_start", f"lam={lam:g}",
                    dict(om0=lam * col.anchor(), c0=lam * 0.5, max_iter=60)))
    for eps in (1e-6, 1e-8, 1e-10):
        out.append(("B_small_amplitude", f"eps={eps:g}",
                    dict(om0=eps * col.anchor(), c0=0.5, max_iter=60)))
    for mu in (1.2, 2.0, 5.0):
        om0 = np.interp(col.X / mu, col.X, ref_om)
        out.append(("C_dilation", f"mu={mu:g}",
                    dict(om0=om0, c0=mu * ref_c, max_iter=60)))
    rng = np.random.default_rng(seed)
    for s in range(int(seeds)):
        om0 = rng.normal(size=col.J) * float(rng.choice([0.1, 1.0, 10.0]))
        c0 = float(rng.normal() * rng.choice([1.0, 10.0, 100.0]))
        out.append(("D_random", f"seed={s}", dict(om0=om0, c0=c0, max_iter=60)))
    for mi in (1, 2, 3, 5, 10, 20, 60):
        out.append(("E_budget", f"max_iter={mi}",
                    dict(om0=10.0 * col.anchor(), c0=5.0, max_iter=mi)))
    return out


def section_A(J=200, seeds=20, seed=0):
    col = ACollocation(J, a=0.0)
    ref = col.newton(max_iter=60)
    ref_c, ref_om = float(ref["c"]), ref["Omega"]

    rows = []
    for route, label, kw in battery_cases(col, ref_om, ref_c, seeds, seed):
        post = col.newton(gauge_tol=GAUGE_TOL, **kw)
        pre = col.newton(gauge_tol=PRE_TOL, **kw)
        om = post["Omega"]
        gd_mine = independent_gauge_defect(col, om)
        rr_mine = independent_relres(col, om, post["c"])
        want = correct_verdict(rr_mine, gd_mine)
        coff = float(abs(float(post["c"]) - ref_c) / max(abs(ref_c), 1e-300))
        rows.append({
            "route": route, "case": label,
            # what the module REPORTS
            "module_converged": bool(post["converged"]),
            "module_converged_relres_only": bool(post["converged_relres_only"]),
            "module_gauge_ok": bool(post["gauge_ok"]),
            "module_gauge_defect": float(post["gauge_defect"]),
            "module_relres": float(post["relres"]),
            "c": float(post["c"]),
            # what THIS LEG computes, from (Omega, c) alone
            "independent_gauge_defect": gd_mine,
            "independent_relres": rr_mine,
            "independent_correct_verdict": want,
            # the three comparisons that make this a check and not a reading
            "verdict_matches": bool(bool(post["converged"]) == want),
            "gauge_defect_field_bit_identical": bool(
                float(post["gauge_defect"]) == gd_mine),
            "gauge_defect_field_rel_error": float(
                abs(float(post["gauge_defect"]) - gd_mine)
                / max(abs(gd_mine), 1e-300)),
            "relres_field_rel_error": float(
                abs(float(post["relres"]) - rr_mine) / max(abs(rr_mine), 1e-300)),
            # the pre-repair verdict, from the module's own reproduction path
            "pre_repair_converged": bool(pre["converged"]),
            "verdict_changed_by_repair": bool(
                bool(pre["converged"]) != bool(post["converged"])),
            "c_relative_error": coff,
            # leg 237's escape predicate, unchanged
            "escaped": bool(post["converged"] and (gd_mine > 1e-8 or coff > 1e-6)),
        })

    conv = [r for r in rows if r["module_converged"]]
    unconv = [r for r in rows if not r["module_converged"]]
    return {
        "J": J, "seeds": seeds, "seed": seed,
        "reference_c": ref_c,
        "n_cases": len(rows),
        "n_converged": len(conv),
        "n_unconverged": len(unconv),
        "n_escaped": int(sum(1 for r in rows if r["escaped"])),
        "n_verdict_mismatches": int(sum(1 for r in rows if not r["verdict_matches"])),
        "mismatched_cases": [r["case"] for r in rows if not r["verdict_matches"]],
        "n_gauge_defect_field_bit_identical": int(
            sum(1 for r in rows if r["gauge_defect_field_bit_identical"])),
        "worst_gauge_defect_field_rel_error": float(
            max(r["gauge_defect_field_rel_error"] for r in rows)),
        "worst_relres_field_rel_error": float(
            max(r["relres_field_rel_error"] for r in rows)),
        "n_verdicts_changed_by_repair": int(
            sum(1 for r in rows if r["verdict_changed_by_repair"])),
        "worst_gauge_defect_among_converged": float(
            max([r["independent_gauge_defect"] for r in conv] or [0.0])),
        "worst_c_relative_error_among_converged": float(
            max([r["c_relative_error"] for r in conv] or [0.0])),
        "best_gauge_defect_among_unconverged": float(
            min([r["independent_gauge_defect"] for r in unconv] or [float("inf")])),
        "rows": rows,
        "reading": ("clause (a) is CORRECT VERDICT, not all-False: the converged "
                    "members must survive and the unconverged must stay rejected, "
                    "with the verdict recomputed here from (Omega, c) alone."),
    }


def section_A_prime(J=200, seeds=20, seed=0):
    """Replication cross-check: leg 237's OWN g5_reachability, imported unmodified."""
    try:
        import p2_route_sirc_v1_census as census
    except Exception as exc:                                    # pragma: no cover
        return {"available": False, "reason": repr(exc)}
    g = census.g5_reachability(J=J, seeds=seeds, seed=seed)
    return {
        "available": True,
        "n_cases": int(g["n_cases"]),
        "n_converged": int(g["n_converged"]),
        "n_escaped": int(g["n_escaped"]),
        "reference_c": float(g["reference_c"]),
        "worst_gauge_defect_among_converged": float(
            g["worst_gauge_defect_among_converged"]),
        "worst_c_relative_error_among_converged": float(
            g["worst_c_relative_error_among_converged"]),
        "n_ladder_converged_off_anchor": int(g["n_ladder_converged_off_anchor"]),
        "rows": [{"route": r["route"], "case": r["case"],
                  "converged": bool(r["converged"]),
                  "gauge_defect_sup": float(r["gauge_defect_sup"]),
                  "escaped": bool(r["escaped"])} for r in g["rows"]],
    }


def compare_A_to_A_prime(A, Ap):
    """Row-for-row, leg 237's function against this leg's re-derived battery."""
    if not Ap.get("available"):
        return {"available": False}
    mine = {(r["route"], r["case"]): r for r in A["rows"]}
    theirs = {(r["route"], r["case"]): r for r in Ap["rows"]}
    keys = sorted(set(mine) | set(theirs))
    mism = []
    for k in keys:
        if k not in mine or k not in theirs:
            mism.append({"case": list(k), "why": "case present in only one battery"})
            continue
        a, b = mine[k], theirs[k]
        if bool(a["module_converged"]) != bool(b["converged"]):
            mism.append({"case": list(k), "why": "verdict",
                         "mine": a["module_converged"], "theirs": b["converged"]})
        elif a["independent_gauge_defect"] != b["gauge_defect_sup"]:
            mism.append({"case": list(k), "why": "gauge defect",
                         "mine": a["independent_gauge_defect"],
                         "theirs": b["gauge_defect_sup"]})
    return {"available": True, "n_keys": len(keys), "n_mismatches": len(mism),
            "mismatches": mism,
            "reading": ("this leg's re-derived trial space and leg 237's own "
                        "function are the same 41 cases producing the same "
                        "verdicts and the same gauge defects, bitwise.")}


# ---------------------------------------------------------------------------
# B -- clause (b): leg 202's calibration pair, re-derived from profile_newton
# ---------------------------------------------------------------------------

def section_B(n=201, epsilons=(1e-8, 1e-10)):
    """The 2 cases that reproduce leg 202's banked numbers, from source.

    This is the live control that the escape detector still FIRES: the pair is on
    a DIFFERENT module (`solver/profile_newton.py`), untouched by leg 248's
    repair, and it must still be flagged as genuine escapes.  If a
    post-repair harness reported these as clean, the harness -- not the module --
    would have been overcorrected.
    """
    pr = profile_newton.TwoScaleNewton(a=0.0, n=n)
    ref = pr.solve()
    ref_c = float(ref["c"])
    rows = []
    for eps in epsilons:
        r = pr.solve(om0=eps * pr.anchor())
        om = r["Omega"]
        gd = float(max(abs(float(om[pr.i0]) + 1.0), abs(float(om[pr.i1]) + 0.5)))
        coff = float(abs(float(r["c"]) - ref_c) / max(abs(ref_c), 1e-300))
        banked = LEG202_BANKED_C.get(eps)
        rows.append({
            "eps": float(eps),
            "converged": bool(r["converged"]),
            "relres": float(r["relres"]),
            "c": float(r["c"]),
            "c_reference": ref_c,
            "c_relative_error": coff,
            "gauge_defect_sup": gd,
            "escaped": bool(r["converged"] and abs(float(om[pr.i0]) + 1.0) > 1e-8),
            "leg202_banked_c": banked,
            "agreement_with_banked_c": (
                None if banked is None else
                float(abs(float(r["c"]) - banked) / max(abs(banked), 1e-300))),
        })
    return {
        "module": "solver/profile_newton.py (NOT the repaired module)",
        "n": n, "rows": rows, "reference_c": ref_c,
        "n_cases": len(rows),
        "n_escaped": int(sum(1 for r in rows if r["escaped"])),
        "n_still_flagged": int(sum(1 for r in rows if r["escaped"])),
        "worst_agreement_with_banked_c": float(max(
            r["agreement_with_banked_c"] for r in rows
            if r["agreement_with_banked_c"] is not None)),
        "reading": ("re-derived from profile_newton.TwoScaleNewton directly -- "
                    "not read from leg 202's, leg 237's or leg 248's JSON."),
    }


def section_B_overcorrection(Js=(60, 100, 160, 200, 240)):
    """The other half of clause (b): a clean solve must NOT be rejected.

    An overcorrected repair is one that suppresses genuine convergence.  Measured
    as a MARGIN, not a boolean: how far below `gauge_tol` the clean solves sit.
    """
    rows = []
    for J in Js:
        for a in (0.0, 0.15, 0.3, 0.5):
            col = ACollocation(J, a=float(a))
            r = col.newton(max_iter=60)
            gd = independent_gauge_defect(col, r["Omega"])
            rows.append({
                "J": int(J), "a": float(a),
                "converged": bool(r["converged"]),
                "converged_relres_only": bool(r["converged_relres_only"]),
                "gauge_defect": gd,
                "relres": float(r["relres"]),
                "margin_decades_below_tol": (
                    float(np.log10(GAUGE_TOL / gd)) if gd > 0 else float("inf")),
                "suppressed_by_repair": bool(
                    r["converged_relres_only"] and not r["converged"]),
            })
    ok = [r for r in rows if r["converged_relres_only"]]
    return {
        "n_cases": len(rows),
        "n_relres_clean": len(ok),
        "n_suppressed_by_repair": int(sum(1 for r in rows if r["suppressed_by_repair"])),
        "worst_gauge_defect_on_clean_solve": float(
            max([r["gauge_defect"] for r in ok] or [0.0])),
        "min_margin_decades_below_tol": float(
            min([r["margin_decades_below_tol"] for r in ok] or [float("inf")])),
        "rows": rows,
        "reading": ("no clean solve is suppressed, and the margin says by how "
                    "much -- a boolean here would hide how close the repair came."),
    }


# ---------------------------------------------------------------------------
# C -- clause (c): the dependent sweep against the GENUINE pre-repair source
# ---------------------------------------------------------------------------

def load_pre_repair_module(rev=PRE_REPAIR_REV):
    """Import `solver/collocation_newton.py` as it stood BEFORE leg 248's repair.

    Read out of git, written to a temp file, imported under its own name.  This is
    what makes section C a differential that can come out non-zero: comparing the
    post-repair module against `gauge_tol=inf` would only re-execute the module's
    own claim about what pre-repair meant.
    """
    src = subprocess.run(
        ["git", "-C", ROOT, "show", f"{rev}:solver/collocation_newton.py"],
        capture_output=True, text=True, check=True).stdout
    d = tempfile.mkdtemp(prefix="cnrv_pre_")
    path = os.path.join(d, "collocation_newton_pre.py")
    with open(path, "w") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("collocation_newton_pre", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["collocation_newton_pre"] = mod
    spec.loader.exec_module(mod)
    return mod, src


def _float_fields(d):
    """Every float-valued field of a newton() return, by name."""
    out = {}
    for k, v in d.items():
        if k == "Omega":
            continue
        if isinstance(v, (float, int)) and not isinstance(v, bool):
            out[k] = float(v)
    return out


def compare_floats(pre, post, tag, moved):
    """Bitwise comparison of every float both dicts carry.  Appends to `moved`."""
    n = 0
    a, b = _float_fields(pre), _float_fields(post)
    for k in sorted(set(a) & set(b)):
        n += 1
        x, y = a[k], b[k]
        same = (x == y) or (np.isnan(x) and np.isnan(y))
        if not same:
            moved.append({"where": tag, "field": k, "pre": x, "post": y,
                          "rel": float(abs(y - x) / max(abs(x), 1e-300))})
    # Omega, elementwise
    if "Omega" in pre and "Omega" in post:
        p, q = np.asarray(pre["Omega"], float), np.asarray(post["Omega"], float)
        n += p.size
        if p.shape != q.shape or not np.array_equal(p, q):
            moved.append({"where": tag, "field": "Omega",
                          "pre": "array", "post": "array",
                          "rel": float(np.max(np.abs(q - p)) if p.shape == q.shape
                                       else float("inf"))})
    return n


def section_C(Js=(40, 60, 80, 100, 120, 160, 200), a_values=(0.0, 0.15, 0.3, 0.5),
              c0_ladder=(0.25, 0.5, 1.0)):
    """Every direct `.newton()`/`continuation()` caller's computation, pre vs post.

    Leg 248 touched exactly two entry points: `ACollocation.newton`'s verdict and
    `continuation`'s three branch decisions.  `newton_gauged` and
    `critical_radius` are untouched (checked here byte-for-byte, not assumed).
    """
    pre_mod, pre_src = load_pre_repair_module()
    post_src = open(os.path.join(ROOT, "solver", "collocation_newton.py")).read()

    def _slice(src, name):
        """The source text of a top-level def/method, for byte-identity checks."""
        lines = src.splitlines()
        start = None
        for i, ln in enumerate(lines):
            if ln.strip().startswith(f"def {name}("):
                start = i
                indent = len(ln) - len(ln.lstrip())
                break
        if start is None:
            return None
        out = [lines[start]]
        for ln in lines[start + 1:]:
            if ln.strip() and (len(ln) - len(ln.lstrip())) <= indent:
                break
            out.append(ln)
        return "\n".join(out)

    untouched = {}
    for name in ("newton_gauged", "critical_radius", "zero_order",
                 "weighted_defect", "residual_a", "jacobian_a",
                 "interpolant_residual", "velocity_integrals", "effective_speed"):
        a, b = _slice(pre_src, name), _slice(post_src, name)
        untouched[name] = {"present_both": bool(a is not None and b is not None),
                           "byte_identical": bool(a is not None and a == b)}

    moved, n_compared = [], 0
    rows = []

    # --- direct .newton() consumers, over the grid/parameter space the
    #     dependents actually use
    for J in Js:
        for a in a_values:
            col_pre = pre_mod.ACollocation(J, a=float(a))
            col_post = ACollocation(J, a=float(a))
            for c0 in c0_ladder:
                rp = col_pre.newton(c0=float(c0), max_iter=60)
                rq = col_post.newton(c0=float(c0), max_iter=60)
                tag = f"newton(J={J},a={a},c0={c0})"
                n_compared += compare_floats(rp, rq, tag, moved)
                rows.append({"where": tag,
                             "pre_converged": bool(rp["converged"]),
                             "post_converged": bool(rq["converged"]),
                             "verdict_changed": bool(
                                 bool(rp["converged"]) != bool(rq["converged"])),
                             "post_gauge_defect": float(rq["gauge_defect"]),
                             "relres": float(rq["relres"])})

    # --- `continuation` ladders, the second touched entry point
    ladders = []
    for J, avals in ((60, np.arange(0.0, 1.51, 0.3)), (200, np.arange(0.0, 0.51, 0.1))):
        lp = pre_mod.continuation(avals, J=J, max_iter=60)
        lq = continuation(avals, J=J, max_iter=60)
        for i, (p, q) in enumerate(zip(lp, lq)):
            tag = f"continuation(J={J})[{i}]"
            n_compared += compare_floats(p, q, tag, moved)
            ladders.append({"where": tag, "a": float(q["a"]),
                            "pre_converged": bool(p["converged"]),
                            "post_converged": bool(q["converged"]),
                            "verdict_changed": bool(
                                bool(p["converged"]) != bool(q["converged"])),
                            "c": float(q["c"]),
                            "gauge_defect": float(q["gauge_defect"])})

    # --- `newton_gauged`, the sibling the repair must not have touched
    for J in (60, 120, 200):
        for drop in (0, 1, J // 2):
            cp = pre_mod.ACollocation(J, a=0.0)
            cq = ACollocation(J, a=0.0)
            rp = cp.newton_gauged(drop=int(drop), max_iter=60)
            rq = cq.newton_gauged(drop=int(drop), max_iter=60)
            n_compared += compare_floats(rp, rq, f"newton_gauged(J={J},drop={drop})",
                                         moved)

    # --- `critical_radius`, leg 166's / leg 0-BENCH's territory, also untouched
    for J in (200, 400):
        cq = ACollocation(J, a=0.3)
        r = cq.newton(max_iter=60)
        U = (cq.V @ r["Omega"])
        E = pre_mod.effective_speed(cq.X, U, r["c"], 0.3)
        xp = pre_mod.critical_radius(cq.X, E)
        xq = critical_radius(cq.X, E)
        n_compared += 1
        if not (xp == xq or (np.isnan(xp) and np.isnan(xq))):
            moved.append({"where": f"critical_radius(J={J})", "field": "Xc",
                          "pre": float(xp), "post": float(xq), "rel": float("inf")})

    return {
        "pre_repair_rev": PRE_REPAIR_REV,
        "n_float_comparisons": int(n_compared),
        "n_floats_moved": len(moved),
        "moved": moved,
        "n_verdicts_changed_newton": int(sum(1 for r in rows if r["verdict_changed"])),
        "n_verdicts_changed_continuation": int(
            sum(1 for r in ladders if r["verdict_changed"])),
        "untouched_functions": untouched,
        "n_untouched_byte_identical": int(
            sum(1 for v in untouched.values() if v["byte_identical"])),
        "n_untouched_checked": len(untouched),
        "newton_rows": rows,
        "continuation_rows": ladders,
        "reading": ("gate clause (c): the differential is against the genuine "
                    "pre-repair SOURCE at " + PRE_REPAIR_REV + ", not against the "
                    "post-repair module's own gauge_tol=inf self-description."),
    }


def section_C_tests():
    """The registered and adversarial suites of every dependent, run as processes."""
    files = [
        "test_collocation_newton.py",
        "test_collocation_newton_adversarial.py",
        "test_collocation_newton_postrepair.py",
        "test_turning_point.py",
        "test_turning_point_adversarial.py",
        "test_first_integral.py",
    ]
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    rows = []
    for f in files:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            rows.append({"file": f, "present": False})
            continue
        r = subprocess.run([sys.executable, p], cwd=ROOT, env=env,
                           capture_output=True, text=True)
        tail = (r.stdout or "").strip().splitlines()
        rows.append({"file": f, "present": True, "returncode": int(r.returncode),
                     "passed": bool(r.returncode == 0),
                     "last_line": tail[-1] if tail else "",
                     "stderr_tail": (r.stderr or "").strip().splitlines()[-1:]})
    return {"n_files": len(rows),
            "n_present": int(sum(1 for r in rows if r.get("present"))),
            "n_passed": int(sum(1 for r in rows if r.get("passed"))),
            "n_failed": int(sum(1 for r in rows
                                if r.get("present") and not r.get("passed"))),
            "failing_files": [r["file"] for r in rows
                              if r.get("present") and not r.get("passed")],
            "rows": rows}


# ---------------------------------------------------------------------------
# D -- the mechanism, re-measured: does the repair actually BITE?
# ---------------------------------------------------------------------------

def section_D(J=200, lams=(0.5, 1.0, 2.0, 5.0, 10.0, 100.0, 1000.0)):
    """(lam Omega*, lam c*) is an exact zero of all J residual rows for every lam.

    `relres` is a ratio of two degree-2 quantities and is therefore EXACTLY
    invariant along that family; the gauge defect is affine and is not.  This
    section re-measures both spreads and the pre/post verdicts, feeding the family
    through the module's own entry point at `max_iter=0` -- no transcription.

    THIS IS THE CONTROL THAT CAN COME OUT DIFFERENTLY (lesson 90): if the repair
    were inert, `n_true_with_broken_gauge_after` would equal the `before` count.
    """
    col = ACollocation(J, a=0.0)
    star = col.newton(max_iter=60)
    om_star, c_star = star["Omega"], float(star["c"])
    rows = []
    for lam in lams:
        om0, c0 = float(lam) * om_star, float(lam) * c_star
        pre = col.newton(om0=om0, c0=c0, max_iter=0, gauge_tol=PRE_TOL)
        post = col.newton(om0=om0, c0=c0, max_iter=0, gauge_tol=GAUGE_TOL)
        gd = independent_gauge_defect(col, post["Omega"])
        rows.append({
            "lam": float(lam),
            "relres": float(post["relres"]),
            "residual_rms": float(post["residual_rms"]),
            "c": float(post["c"]),
            "gauge_defect": gd,
            "gauge_defect_over_abs_lam_minus_1": (
                float(gd / abs(lam - 1.0)) if lam != 1.0 else None),
            "pre_repair_converged": bool(pre["converged"]),
            "post_repair_converged": bool(post["converged"]),
            "verdict_changed": bool(bool(pre["converged"]) != bool(post["converged"])),
        })
    rr = [r["relres"] for r in rows]
    rms = [r["residual_rms"] for r in rows]
    cs = [abs(r["c"]) for r in rows]
    off = [r for r in rows if r["gauge_defect"] > GAUGE_TOL]
    return {
        "J": J, "rows": rows,
        "relres_spread_absolute": float(max(rr) - min(rr)),
        "relres_dynamic_range": float(max(rr) / max(min(rr), 1e-300)),
        "residual_rms_dynamic_range": float(max(rms) / max(min(rms), 1e-300)),
        "c_dynamic_range": float(max(cs) / max(min(cs), 1e-300)),
        "n_off_gauge_members": len(off),
        "n_true_with_broken_gauge_before": int(
            sum(1 for r in off if r["pre_repair_converged"])),
        "n_true_with_broken_gauge_after": int(
            sum(1 for r in off if r["post_repair_converged"])),
        "smallest_off_gauge_defect": float(
            min([r["gauge_defect"] for r in off] or [float("inf")])),
        "reading": ("relres is flat to the quoted absolute spread across a "
                    "dynamic range of c and of absolute residual that is many "
                    "decades wide -- the exact degeneracy the repair's affine "
                    "companion was added to see."),
    }


# ---------------------------------------------------------------------------
# E -- how load-bearing is the threshold?  (independent re-derivation)
# ---------------------------------------------------------------------------

def section_E(J=200, tols=(1e-14, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 0.5)):
    """Both gate clauses, re-evaluated at eight `gauge_tol` values.

    If the answer is the same across many decades, the threshold is not what the
    result rests on.  Measured as the WIDTH of the indifference band, in decades.
    """
    col = ACollocation(J, a=0.0)
    ref = col.newton(max_iter=60)
    ref_c, ref_om = float(ref["c"]), ref["Omega"]
    cases = battery_cases(col, ref_om, ref_c)
    star_c, star_om = ref_c, ref_om

    rows = []
    for tol in tols:
        n_ok = 0
        for route, label, kw in cases:
            r = col.newton(gauge_tol=float(tol), **kw)
            gd = independent_gauge_defect(col, r["Omega"])
            rr = independent_relres(col, r["Omega"], r["c"])
            if bool(r["converged"]) == correct_verdict(rr, gd, float(tol)):
                n_ok += 1
        # clause (a) as a function of tol, and does the repair still bite?
        bite_before, bite_after = 0, 0
        for lam in (2.0, 5.0, 10.0, 1000.0):
            pre = col.newton(om0=lam * star_om, c0=lam * star_c,
                             max_iter=0, gauge_tol=PRE_TOL)
            post = col.newton(om0=lam * star_om, c0=lam * star_c,
                              max_iter=0, gauge_tol=float(tol))
            bite_before += int(bool(pre["converged"]))
            bite_after += int(bool(post["converged"]))
        rows.append({"gauge_tol": float(tol),
                     "n_battery_correct": int(n_ok),
                     "n_battery": len(cases),
                     "clause_a_holds": bool(n_ok == len(cases)),
                     "n_off_gauge_accepted_before": bite_before,
                     "n_off_gauge_accepted_after": bite_after,
                     "repair_bites": bool(bite_after < bite_before)})
    good = [r["gauge_tol"] for r in rows if r["clause_a_holds"] and r["repair_bites"]]
    return {"J": J, "rows": rows,
            "n_tolerances": len(rows),
            "n_tolerances_where_both_hold": len(good),
            "indifference_band": [float(min(good)), float(max(good))] if good else None,
            "n_decades_of_indifference": (
                float(np.log10(max(good) / min(good))) if good else 0.0),
            "reading": ("the choice of gauge_tol inside the indifference band is "
                        "not load-bearing; the band's width says how much room "
                        "there was.")}


# ---------------------------------------------------------------------------
# G -- the comparator's own self-test (lesson 90)
# ---------------------------------------------------------------------------

def section_G():
    """"0 floats moved" must be a measurement, not a property of the comparator.

    Feed the float-move detector a pair that DOES differ, in each of the three
    shapes it handles (scalar field, nan field, Omega array), and require it to
    fire.  A detector that cannot report the other answer is not a check.
    """
    checks = []

    moved = []
    compare_floats({"c": 1.0, "Omega": np.zeros(3)},
                   {"c": 1.0 + 2.0 ** -52, "Omega": np.zeros(3)}, "selftest_scalar",
                   moved)
    checks.append({"shape": "scalar field, 1 ulp apart",
                   "detector_fired": bool(len(moved) == 1),
                   "reported_rel": float(moved[0]["rel"]) if moved else None})

    moved = []
    compare_floats({"c": 1.0, "Omega": np.zeros(3)},
                   {"c": 1.0, "Omega": np.array([0.0, 1e-300, 0.0])},
                   "selftest_omega", moved)
    checks.append({"shape": "Omega array, one entry at 1e-300",
                   "detector_fired": bool(len(moved) == 1),
                   "reported_rel": float(moved[0]["rel"]) if moved else None})

    moved = []
    compare_floats({"c": float("nan"), "Omega": np.zeros(3)},
                   {"c": float("nan"), "Omega": np.zeros(3)}, "selftest_nan", moved)
    checks.append({"shape": "nan vs nan (must NOT fire)",
                   "detector_fired": bool(len(moved) != 0),
                   "expected_fire": False, "reported_rel": None})

    # and the verdict comparator: a deliberately wrong specification must mismatch
    col = ACollocation(60, a=0.0)
    r = col.newton(max_iter=60)
    gd = independent_gauge_defect(col, r["Omega"])
    rr = independent_relres(col, r["Omega"], r["c"])
    checks.append({
        "shape": "verdict comparator against an absurd gauge_tol=0.0",
        "detector_fired": bool(bool(r["converged"]) != correct_verdict(rr, gd, 0.0)),
        "expected_fire": True,
        "reported_rel": None,
        "note": ("a clean solve has gauge_defect > 0, so the specification at "
                 "gauge_tol = 0 says REJECT while the module says accept -- the "
                 "comparator must notice"),
    })

    want_fire = [c for c in checks if c.get("expected_fire", True)]
    return {"checks": checks,
            "n_checks": len(checks),
            "n_behaved_as_specified": int(
                sum(1 for c in checks
                    if c["detector_fired"] == c.get("expected_fire", True))),
            "reading": ("every zero this runner reports is a zero the detector "
                        "was capable of reporting as non-zero.")}


# ---------------------------------------------------------------------------
# assembly
# ---------------------------------------------------------------------------

def main():
    res = {
        "leg": 286, "route": "CNRV",
        "subject": ("independent post-repair verification of leg 248's repair to "
                    "solver/collocation_newton.py (ACollocation.newton's verdict "
                    "and continuation's three branch decisions)"),
        "module_under_test": "solver/collocation_newton.py (read-only)",
        "pre_repair_rev": PRE_REPAIR_REV,
        "gate": ("Does an independent re-run confirm (a) all 41 of leg 237's "
                 "reachability-battery cases now correctly reject/flag, (b) the 2 "
                 "cases reproducing leg 202's banked numbers remain correctly "
                 "flagged as genuine (no overcorrection), and (c) no "
                 "collocation_newton.py-dependent banked value moved (robustness "
                 "sweep over dependents)?"),
    }

    print("[run] A  -- clause (a): the 41-case battery, verdicts recomputed here",
          flush=True)
    res["A_battery_41"] = section_A()
    print("[run] A' -- replication through leg 237's own g5_reachability", flush=True)
    res["A_prime_leg237_replication"] = section_A_prime()
    res["A_vs_A_prime"] = compare_A_to_A_prime(res["A_battery_41"],
                                               res["A_prime_leg237_replication"])
    print("[run] B  -- clause (b): leg 202's pair, from profile_newton directly",
          flush=True)
    res["B_leg202_calibration"] = section_B()
    res["B_overcorrection_check"] = section_B_overcorrection()
    print("[run] C  -- clause (c): dependent sweep vs the pre-repair source",
          flush=True)
    res["C_dependent_sweep"] = section_C()
    print("[run] C' -- dependents' own test suites", flush=True)
    res["C_dependent_tests"] = section_C_tests()
    print("[run] D  -- does the repair bite?  the scaling family", flush=True)
    res["D_repair_bites"] = section_D()
    print("[run] E  -- threshold indifference band", flush=True)
    res["E_threshold_sensitivity"] = section_E()
    print("[run] G  -- the comparator's own self-test", flush=True)
    res["G_comparator_selftest"] = section_G()

    A = res["A_battery_41"]
    B = res["B_leg202_calibration"]
    Bo = res["B_overcorrection_check"]
    C = res["C_dependent_sweep"]
    Ct = res["C_dependent_tests"]

    clause_a = bool(A["n_verdict_mismatches"] == 0 and A["n_cases"] == 41)
    clause_b = bool(B["n_still_flagged"] == 2 and Bo["n_suppressed_by_repair"] == 0)
    clause_c = bool(C["n_floats_moved"] == 0 and Ct["n_failed"] == 0)

    res["gate_clause_a_all_41_correct"] = {
        "answer": clause_a,
        "n_cases": A["n_cases"],
        "n_correct": A["n_cases"] - A["n_verdict_mismatches"],
        "failing_cases": A["mismatched_cases"],
        "n_converged": A["n_converged"],
        "worst_gauge_defect_among_converged": A["worst_gauge_defect_among_converged"],
        "best_gauge_defect_among_unconverged": A["best_gauge_defect_among_unconverged"],
    }
    res["gate_clause_b_leg202_pair_still_flagged"] = {
        "answer": clause_b,
        "n_still_flagged": B["n_still_flagged"],
        "worst_agreement_with_banked_c": B["worst_agreement_with_banked_c"],
        "n_clean_solves_suppressed": Bo["n_suppressed_by_repair"],
        "min_margin_decades_below_tol": Bo["min_margin_decades_below_tol"],
    }
    res["gate_clause_c_no_dependent_moved"] = {
        "answer": clause_c,
        "n_float_comparisons": C["n_float_comparisons"],
        "n_floats_moved": C["n_floats_moved"],
        "n_dependent_suites_run": Ct["n_present"],
        "n_dependent_suites_failed": Ct["n_failed"],
        "failing_files": Ct["failing_files"],
    }
    res["gate_answer"] = "YES" if (clause_a and clause_b and clause_c) else "NO"
    res["clay_odds"] = ("~0.05%, unmoved: this is a regression verification of a "
                        "solver-hygiene repair on a latent defect in a module with "
                        "no claim-bearing call site. No link of the L1->L4 chain "
                        "is touched.")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1, default=float, sort_keys=False)
    print("\nwrote", OUT)
    print("GATE:", res["gate_answer"],
          "| (a)", clause_a, "(b)", clause_b, "(c)", clause_c)
    return res


if __name__ == "__main__":
    main()
