"""ROUTE-CDB v1 -- POST-REPAIR REGRESSION CHECK on solver/critical_dissipation.py.

Leg 170.  Closes the loop on leg 154 (Route-CDR), which repaired the silent exponent
truncation leg 121 (Route-CDA) found.  THIS LEG EDITS NOTHING.  Both branches of its
gate forbid patching; the deliverable is the measurement and the banked suite.

GATE (DIRECTION.md sec 170, verbatim):
  Post-repair, does solver/critical_dissipation.py (a) reject or visibly flag every
  non-integer `p (2s)` case in leg 121's battery, and (b) reproduce every
  previously-validated integer-`p` result bit-identically?
    yes -> Repair confirmed solid and non-regressive.  Bank leg 121's battery as a
           permanent regression suite.
    no  -> An incomplete fix or a repair regression.  Report the exact case and
           magnitudes; escalate as a priority finding, do not patch under this leg's
           own authority.

NOT A PHYSICS MEASUREMENT.  alpha_1 = 0 at a=0 (ALS eq 61), sigma = 3 at a = 1/2 (Xu
arXiv:2607.19762 sec 6.1 + Table 1 + Fig 3) and the searched-not-found alpha_1 =
+0.133683 (leg 64) are NOT contested, re-derived or re-aimed here.  They appear only as
fixed points a differential must not move.  The standing "no more gCLM measurement legs"
ban does not bind a measurement of CODE.  BANKED NUMBERS AT RISK: 0.

WHERE THE BATTERY COMES FROM (novelty pass, writeup/novelty/leg_170.md).  The two
failure shapes legs 147/NKB and 131/HNB found on other modules are declared there BEFORE
this ran, and they are what R1 and R2 hunt:
  (i)  an aggregate count hides a non-uniform case -- so leg 154's banked
       "15/15 refused (was 0/15)" is NOT accepted as a count.  Every refusal is
       re-measured per case AND per entry point, recording whether the refusal is the
       NEW guard or the PRE-EXISTING `p < 1` ValueError that would have refused anyway.
  (ii) the repair lands a guard the finding leg's own battery cannot run past.

INDEPENDENCE IS CONSTRUCTED, NOT ASSERTED.  The non-integer case list is rebuilt from
leg 121's OWN banked JSON (writeup/data/p2_route_cda_v1_adversarial.json), never from
leg 154's A_clause_a_refusals; clause (b) runs over an independently chosen grid.  If
the totals agree, that is two constructions of one number, not one number copied twice.

Deterministic, NOT logged.  Writes writeup/data/p2_route_cdb_v1_postrepair.json.
"""

import hashlib
import json
import subprocess
import sys
import tempfile
import shutil
import time
import types
import warnings
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from solver import critical_dissipation as POST          # noqa: E402  the landed module

# The module's CREATING commit, and a stable ancestor of main.  Leg 130's correction
# d871675: never pin the differential to a hash a rebase will rewrite.
PRE_REPAIR_SHA = "9dba93f"
MODULE_PATH = "solver/critical_dissipation.py"
LEG121_JSON = REPO / "writeup/data/p2_route_cda_v1_adversarial.json"
LEG121_DRIVER = REPO / "experiments/p2_route_cda_v1_adversarial.py"


# --------------------------------------------------------------------------
# the pre-repair module, read out of git and exec'd in THIS interpreter
# --------------------------------------------------------------------------
def load_pre_repair():
    """numpy/BLAS are shared with the post-repair module, so any difference is the
    repair rather than the environment.  Inherited verbatim from legs 129/130/150/151/
    152/154."""
    src = subprocess.run(["git", "show", f"{PRE_REPAIR_SHA}:{MODULE_PATH}"],
                         cwd=str(REPO), capture_output=True, text=True, check=True).stdout
    name = "critical_dissipation_pre_repair"
    mod = types.ModuleType(name)
    mod.__file__ = f"<git:{PRE_REPAIR_SHA}:{MODULE_PATH}>"
    sys.modules[name] = mod
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, src


def _sha16(s):
    return hashlib.sha256(s.encode() if isinstance(s, str) else s).hexdigest()[:16]


# --------------------------------------------------------------------------
# leaf-by-leaf bitwise comparison.  == on float64, NOT np.allclose.
# --------------------------------------------------------------------------
def _leaves(x, path, out):
    if isinstance(x, dict):
        for k in sorted(x, key=str):
            _leaves(x[k], f"{path}.{k}", out)
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            _leaves(v, f"{path}[{i}]", out)
    elif isinstance(x, np.ndarray):
        flat = x.ravel()
        for i, v in enumerate(flat):
            out.append((f"{path}[{i}]", complex(v) if np.iscomplexobj(x) else float(v)))
    elif isinstance(x, (bool, np.bool_)):
        out.append((path, bool(x)))
    elif isinstance(x, (int, np.integer)):
        out.append((path, int(x)))
    elif isinstance(x, (float, np.floating)):
        out.append((path, float(x)))
    elif isinstance(x, (complex, np.complexfloating)):
        out.append((path, complex(x)))
    elif isinstance(x, str) or x is None:
        out.append((path, x))
    else:
        out.append((path, repr(x)))


def _identical(u, v):
    """NaN == NaN counts as identical; everything else is bitwise ==."""
    if isinstance(u, float) and isinstance(v, float):
        if np.isnan(u) and np.isnan(v):
            return True
        return u == v
    if isinstance(u, complex) and isinstance(v, complex):
        a = (np.isnan(u.real) and np.isnan(v.real)) or u.real == v.real
        b = (np.isnan(u.imag) and np.isnan(v.imag)) or u.imag == v.imag
        return bool(a and b)
    return type(u) is type(v) and u == v


def compare(name, a, b):
    la, lb = [], []
    _leaves(a, name, la)
    _leaves(b, name, lb)
    if len(la) != len(lb):
        return {"quantity": name, "n": max(len(la), len(lb)), "n_moved": max(len(la), len(lb)),
                "moved": [{"path": name, "why": f"leaf count {len(la)} != {len(lb)}"}]}
    moved = []
    for (pa, va), (pb, vb) in zip(la, lb):
        if not _identical(va, vb):
            moved.append({"path": pa, "pre": repr(va), "post": repr(vb)})
    return {"quantity": name, "n": len(la), "n_moved": len(moved), "moved": moved[:8]}


# --------------------------------------------------------------------------
# R0 -- the lesson-90 control.  If this does not fire, the whole run is void.
# --------------------------------------------------------------------------
def r0_control(PRE, pre_src):
    """A control that cannot come out differently is not a control (lesson 90).

    What would have to change in the code for this to report the other answer: the
    pre-repair side must ACCEPT p = 1.9 and the post-repair side must REFUSE it.  If
    both refuse, the pre-repair module did not load and every bit-identity below is a
    tautology of a single module compared with itself.
    """
    def accepts(mod):
        try:
            mod.lambda_power(8, 1.9)
            return True, None
        except Exception as e:                                    # noqa: BLE001
            return False, type(e).__name__

    pre_ok, pre_exc = accepts(PRE)
    post_ok, post_exc = accepts(POST)

    # leg 121's banked C2 headline, end to end, through the PRE-repair module
    rows = PRE.mu_branch(0.0, 1.9, [0.0, 0.05, 0.1], K=64)
    sl = PRE.alpha_slope(rows)
    banked = json.loads(LEG121_JSON.read_text())["C2_flow_identity_under_truncation"]
    b0 = [r for r in banked["rows"] if r["p_requested"] == 1.9][0]

    return {
        "pre_repair_ref": f"git:{PRE_REPAIR_SHA}:{MODULE_PATH}",
        "pre_repair_src_sha256_16": _sha16(pre_src),
        "post_repair_src_sha256_16": _sha16((REPO / MODULE_PATH).read_text()),
        "modules_are_distinct_objects": PRE is not POST,
        "pre_has_guard": hasattr(PRE, "_validated_p"),
        "post_has_guard": hasattr(POST, "_validated_p"),
        "pre_accepts_p_1p9": pre_ok, "pre_exception": pre_exc,
        "post_accepts_p_1p9": post_ok, "post_exception": post_exc,
        "control_fires": bool(pre_ok and not post_ok),
        # Does leg 121's OWN module, on leg 121's OWN code path, still reproduce leg 121's
        # OWN banked numbers today?  If not, the banked JSON is a drifted reference and
        # every "vs banked" comparison in this leg has to be read in ULP, not in booleans.
        "leg121_C2_reproduced_from_pre_repair": {
            "residual_pre": rows[-1]["residual"], "residual_banked": b0["residual_fake"],
            "residual_bit_identical": rows[-1]["residual"] == b0["residual_fake"],
            "residual_ulp": _ulps(rows[-1]["residual"], b0["residual_fake"]),
            "alpha_pre": rows[-1]["alpha"], "alpha_banked": b0["alpha_fake"],
            "alpha_bit_identical": rows[-1]["alpha"] == b0["alpha_fake"],
            "alpha_ulp": _ulps(rows[-1]["alpha"], b0["alpha_fake"]),
            "alpha_1_pre": sl["alpha_1"], "alpha_1_banked": b0["alpha_1_fake"],
            "alpha_1_bit_identical": sl["alpha_1"] == b0["alpha_1_fake"],
            "alpha_1_ulp": _ulps(sl["alpha_1"], b0["alpha_1_fake"]),
            "note": ("If these are NOT bit-identical, the pre-repair module does not "
                     "reproduce its own banked value on today's NumPy/BLAS. That is "
                     "environmental drift, it is measured here in ULP, and it means the "
                     "banked JSON cannot serve as a bitwise reference for ANY leg. It does "
                     "NOT touch clause (b), which compares pre against post in ONE process "
                     "so the environment cancels exactly."),
        },
    }


# --------------------------------------------------------------------------
# R1 -- does leg 121's OWN driver still run?  (failure shape (ii))
# --------------------------------------------------------------------------
def r1_finding_legs_driver_still_runs():
    """Leg 147 found leg 116's battery aborting in 0.9 s against the repaired module,
    and nobody noticed.  Leg 131 found the same shape.  Leg 154 anticipated it and built
    the `on_noninteger="truncate"` hatch per leg 135's rule -- but leg 121's BANKED
    driver predates the hatch and does not pass it.

    Run it UNMODIFIED, from a scratch copy at the same directory depth, so its own
    `parents[1] / "writeup/data/..."` write lands outside the repository and no file
    outside this leg's territory is touched.
    """
    tmp = Path(tempfile.mkdtemp(prefix="cdb170_"))
    try:
        (tmp / "experiments").mkdir()
        (tmp / "writeup" / "data").mkdir(parents=True)
        shutil.copy2(LEG121_DRIVER, tmp / "experiments" / LEG121_DRIVER.name)
        t0 = time.time()
        proc = subprocess.run([sys.executable, f"experiments/{LEG121_DRIVER.name}"],
                              cwd=str(tmp), capture_output=True, text=True,
                              env={"PYTHONPATH": str(REPO), "PATH": "/usr/bin:/bin",
                                   "HOME": str(tmp)}, timeout=1800)
        dt = time.time() - t0
        out = proc.stdout + proc.stderr
        # the driver's nine sections, in the order its main() runs them
        sections = ["C1_lambda_power_truncation", "C2_flow_identity_under_truncation",
                    "C3_realistic_float_near_miss", "C4_type_coercion_asymmetry",
                    "C5_negative_mu", "C6_mu_decay_time_domain",
                    "C7_marginal_verdict_nan", "C8_amplitude_eigenvalue_sign",
                    "C9_positive_controls"]
        wrote = tmp / "writeup/data/p2_route_cda_v1_adversarial.json"
        produced = json.loads(wrote.read_text()) if wrote.exists() else None
        done = [s for s in sections if produced is not None and s in produced]
        # the three sections that carry the bit-identity evidence which AUTHORISED the repair
        evidence = ["C1_lambda_power_truncation", "C2_flow_identity_under_truncation",
                    "C3_realistic_float_near_miss"]
        return {
            "driver": str(LEG121_DRIVER.relative_to(REPO)),
            "ran_unmodified": True, "returncode": proc.returncode, "seconds": round(dt, 2),
            "completed": proc.returncode == 0,
            "wrote_json": produced is not None,
            "n_sections_total": len(sections),
            "n_sections_completed": len(done),
            "sections_completed": done,
            "n_evidence_sections_total": len(evidence),
            "n_evidence_sections_completed": len([s for s in evidence if s in done]),
            "abort_exception": ([ln for ln in out.splitlines()
                                 if "Error:" in ln or "Error " in ln] or [None])[-1],
            "abort_in_section": (sections[len(done)] if produced is not None
                                 and len(done) < len(sections) else None),
            "tail": out.strip().splitlines()[-1][:300] if out.strip() else None,
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------
# leg 121's non-integer battery, REBUILT FROM LEG 121's OWN JSON
# --------------------------------------------------------------------------
def leg121_noninteger_cases():
    """Every non-integral float `p` leg 121 measured, taken from ITS OWN banked record.

    C1's `p = -0.5` and `p = 0.5` are non-integral but were ALREADY refused pre-repair
    by `lambda_power`'s `p < 1` check, so they are carried separately: a case the old
    code already refused is not evidence for the new guard (failure shape (i)).
    """
    d = json.loads(LEG121_JSON.read_text())
    new, already = [], []
    for r in d["C1_lambda_power_truncation"]["rows"]:
        p = r["p_requested"]
        if float(p) == np.floor(float(p)):
            continue
        (new if r["silently_truncated"] else already).append(
            {"p": float(p), "src": "C1", "case": r["case"],
             "pre_repair_accepted": bool(r["accepted"]),
             "pre_repair_built": r["p_actually_used"],
             "pre_repair_exception": r["exception"]})
    seen = {c["p"] for c in new} | {c["p"] for c in already}
    for r in d["C2_flow_identity_under_truncation"]["rows"]:
        p = float(r["p_requested"])
        new.append({"p": p, "src": "C2", "case": f"p = {p} (full pipeline, p_true={r['p_true']})",
                    "pre_repair_accepted": True, "pre_repair_built": r["p_actually_built"],
                    "pre_repair_exception": None})
        seen.add(p)
    for r in d["C3_realistic_float_near_miss"]["cases"]:
        p = float(r["p_computed"])
        if p != np.floor(p):
            new.append({"p": p, "src": "C3", "case": r["case"],
                        "pre_repair_accepted": True,
                        "pre_repair_built": r["p_actually_used_by_int_cast"],
                        "pre_repair_exception": None})
            seen.add(p)
    for r in d["C4_type_coercion_asymmetry"]["rows"]:
        if r["type"] == "float" and r["accepted"]:
            p = float(r["p_repr"])
            if p != np.floor(p):
                new.append({"p": p, "src": "C4", "case": r["case"],
                            "pre_repair_accepted": True, "pre_repair_built": r["p_built"],
                            "pre_repair_exception": None})
    return new, already


# --------------------------------------------------------------------------
# R2 -- clause (a), PER CASE and PER ENTRY POINT  (failure shape (i))
# --------------------------------------------------------------------------
def _entry_points(mod, b_seed):
    """Every public entry point of the module that takes `p`.

    `b0` is passed wherever the signature allows it so the probe measures the GUARD and
    not the cost of a continuation: if the guard fires, it fires before any solve.
    """
    K = 16
    return {
        "lambda_power": lambda p: mod.lambda_power(K, p),
        "lambda_truncation": lambda p: mod.lambda_truncation(b_seed[:K], K, p),
        "CriticalDissipativeFlow.__init__": lambda p: mod.CriticalDissipativeFlow(
            0.0, mu=0.1, p=p, K=K),
        "mu_branch": lambda p: mod.mu_branch(0.0, p, [0.05], K=K, b0=b_seed[:K]),
        "dissipative_spectrum": lambda p: mod.dissipative_spectrum(
            0.0, p, 0.05, K, b0=b_seed[:K]),
        "converged_dissipative_spectrum": lambda p: mod.converged_dissipative_spectrum(
            0.0, p, 0.05, K_coarse=K, K_fine=K + 8, b0=b_seed[:K]),
    }


def _probe(fn, p):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            fn(p)
            return {"refused": False, "exception": None, "exc_class": None,
                    "is_ValueError": False, "is_domain_error": False,
                    "n_warnings": len(w),
                    "warnings": [str(x.message)[:200] for x in w]}
        except Exception as e:                                    # noqa: BLE001
            return {"refused": True, "exception": f"{type(e).__name__}: {e}"[:400],
                    "exc_class": type(e).__name__,
                    "is_ValueError": isinstance(e, ValueError),
                    "is_domain_error":
                        type(e).__name__ == "CriticalDissipationDomainError",
                    "n_warnings": len(w),
                    "warnings": [str(x.message)[:200] for x in w]}


def r2_clause_a(PRE, b_seed):
    new, already = leg121_noninteger_cases()
    eps = _entry_points(POST, b_seed)
    pre_eps = _entry_points(PRE, b_seed)

    rows, n_cell, n_refused, n_domain, n_valueerror, silent = [], 0, 0, 0, 0, []
    for c in new:
        per = {}
        for name, fn in eps.items():
            r = _probe(fn, c["p"])
            per[name] = r
            n_cell += 1
            n_refused += int(r["refused"])
            n_domain += int(r["is_domain_error"])
            n_valueerror += int(r["is_ValueError"])
            if not r["refused"] and r["n_warnings"] == 0:
                silent.append({"p": c["p"], "entry_point": name, "src": c["src"]})
        # does the refusal message NAME the substitution it prevented?
        msg = per["lambda_power"]["exception"] or ""
        rows.append({
            **c,
            "refused_at_all_entry_points": all(v["refused"] for v in per.values()),
            "n_entry_points_refusing": sum(v["refused"] for v in per.values()),
            "n_entry_points": len(eps),
            "all_ValueError": all(v["is_ValueError"] for v in per.values()),
            "all_CriticalDissipationDomainError":
                all(v["is_domain_error"] for v in per.values()),
            "message_names_requested_p": repr(c["p"]) in msg,
            "message_names_would_be_built_p":
                f"p = {int(c['p'])}" in msg or f"build p = {int(c['p'])}" in msg,
            "per_entry_point": per,
        })

    # the separation failure shape (i) demands: cases the OLD code already refused
    already_rows = []
    for c in already:
        pre_r = _probe(pre_eps["lambda_power"], c["p"])
        post_r = _probe(eps["lambda_power"], c["p"])
        already_rows.append({
            **c,
            "pre_repair_refused": pre_r["refused"], "pre_repair_class": pre_r["exc_class"],
            "post_repair_refused": post_r["refused"], "post_repair_class": post_r["exc_class"],
            "both_ValueError": pre_r["is_ValueError"] and post_r["is_ValueError"],
            "refusal_reason_changed": pre_r["exc_class"] != post_r["exc_class"],
            "pre_message": pre_r["exception"], "post_message": post_r["exception"],
        })

    # non-finite p: leg 154's adopted first clause, and leg 121's prescribed predicate's blind spot
    nonfinite = []
    for p in [float("inf"), float("-inf"), float("nan")]:
        r = _probe(eps["lambda_power"], p)
        pr = _probe(pre_eps["lambda_power"], p)
        nonfinite.append({"p": repr(p), "post_refused": r["refused"],
                          "post_class": r["exc_class"], "post_is_ValueError": r["is_ValueError"],
                          "pre_class": pr["exc_class"],
                          "pre_was_ValueError": pr["is_ValueError"]})

    # the entry point that routes through dissipative_spectrum without a b0 -- measured once
    planted = _probe(lambda p: POST.planted_dissipative_control(
        a=0.0, p=p, mu=0.05, K_coarse=16, K_fine=24), 1.9)

    return {
        "case_list_source": "writeup/data/p2_route_cda_v1_adversarial.json (leg 121's OWN "
                            "record), NOT leg 154's A_clause_a_refusals",
        "n_cases_new_guard": len(new),
        "n_cases_already_refused_pre_repair": len(already),
        "n_entry_points": len(eps),
        "entry_points": sorted(eps),
        "n_case_entrypoint_cells": n_cell,
        "n_cells_refused": n_refused,
        "n_cells_CriticalDissipationDomainError": n_domain,
        "n_cells_ValueError": n_valueerror,
        "n_cells_silently_accepted": len(silent),
        "silently_accepted": silent,
        "n_cases_refused_at_every_entry_point":
            sum(r["refused_at_all_entry_points"] for r in rows),
        "rows": rows,
        "already_refused_pre_repair": already_rows,
        "non_finite": nonfinite,
        "planted_dissipative_control_p1p9": planted,
    }


# --------------------------------------------------------------------------
# R3 -- clause (b), an INDEPENDENTLY CONSTRUCTED integer-p differential
# --------------------------------------------------------------------------
def r3_clause_b(PRE, b_seed):
    """Bitwise A/B over integer-`p` configurations.  == on float64, NOT np.allclose.

    The grid is chosen independently of leg 154's (whose shipped-config census was 14
    named cases and whose differential this leg never read as a case list): off-lattice
    `a` values, non-round `K`, irregular mu ladders, and the whole free-function surface.
    """
    results = []

    def q(name, fn):
        try:
            a = fn(PRE)
        except Exception as e:                                    # noqa: BLE001
            a = {"__exception__": f"{type(e).__name__}: {e}"}
        try:
            b = fn(POST)
        except Exception as e:                                    # noqa: BLE001
            b = {"__exception__": f"{type(e).__name__}: {e}"}
        results.append(compare(name, a, b))

    q("LAMBDA_SIN1", lambda m: m.LAMBDA_SIN1)
    q("CRITICAL_POINTS", lambda m: [dict(d) for d in m.CRITICAL_POINTS])
    q("lambda_block", lambda m: {str(n): m.lambda_block(n) for n in (1, 2, 5, 17, 33, 57, 96)})
    q("lambda_power", lambda m: {f"K{K}p{p}": list(m.lambda_power(K, p))
                                 for K in (4, 9, 23, 57, 96) for p in (1, 2, 3, 4, 5)})
    q("lambda_power_integral_float_types",
      lambda m: {f"{K}:{p!r}": list(m.lambda_power(K, p))
                 for K in (7, 31) for p in (3, 3.0, np.float64(3.0), np.int64(3), True)})
    q("lambda_truncation", lambda m: {f"K{K}p{p}": m.lambda_truncation(b_seed[:K], K, p)
                                      for K in (9, 23, 57) for p in (1, 2, 3, 5)})
    q("_ladder_to", lambda m: {str(x): m._ladder_to(x) for x in (0.0, 0.05, 0.1, 0.37, 1.0)})
    q("amplitude_eigenvalue",
      lambda m: m.amplitude_eigenvalue(np.linspace(0.0, 2.0, 41)))
    q("marginal_verdict", lambda m: {f"{x:g}": m.marginal_verdict(x)
                                     for x in (-1.0, -1e-12, 0.0, 1e-12, 1e-9, 0.133683, 3.0)})
    q("mu_decay_time", lambda m: {f"{a1:g}|{m0:g}|{t:g}": m.mu_decay_time(a1, m0, t)
                                  for a1 in (0.133683, 1.0, 1.4675) for m0 in (0.1, 1.0)
                                  for t in (1e-3, 1e-6)})
    q("exact_a0_family", lambda m: {str(mu): list(m.exact_a0_family(mu, np.linspace(-7, 7, 101)))
                                    for mu in (0.0, 0.05, 0.13, 0.5, 2.0)})
    q("exact_a0_spacetime",
      lambda m: {f"{t}|{nu}|{mu0}": m.exact_a0_spacetime(np.linspace(-4, 4, 61), t, nu, mu0)
                 for t in (0.0, 0.37) for nu in (0.01, 0.5) for mu0 in (0.1, 1.0)})
    q("exact_a0_residual",
      lambda m: {f"{t}|{nu}|{mu0}": m.exact_a0_residual(np.linspace(-4, 4, 61), t, nu, mu0)
                 for t in (0.0, 0.37) for nu in (0.01, 0.5) for mu0 in (0.1, 1.0)})

    # the class surface, on off-lattice a and non-round K
    def flow_surface(m):
        out = {}
        for a in (0.0, 0.17, 0.5):
            for K in (23, 57):
                for p in (1, 3):
                    for mu in (0.0, 0.09):
                        f = m.CriticalDissipativeFlow(a, mu=mu, p=p, K=K)
                        b = b_seed[:K]
                        out[f"a{a}K{K}p{p}mu{mu}"] = {
                            "p": f.p, "s": f.s, "mu": f.mu,
                            "Lp": f.Lp, "Lam": f.Lam, "lam_dx0": f.lam_dx0,
                            "c_omega": f.c_omega(b), "_dc_omega": f._dc_omega(b),
                            "residual": f.residual(b), "jacobian": f.jacobian(b),
                            "alpha": f.alpha(b), "mu_growth": f.mu_growth(b),
                            "generator": f.generator(b),
                        }
        return out
    q("CriticalDissipativeFlow_surface", flow_surface)

    # the physics path: continuation seed -> mu branch -> alpha_slope -> verdict.
    # These are the quantities capabilities.py's validated line is quoted from.
    def branch(m):
        out = {}
        for a, p, K, mus in [(0.0, 1, 64, [0.0, 0.05, 0.1]),
                             (0.0, 1, 96, [0.0, 0.03, 0.07, 0.13]),
                             (0.5, 3, 96, [0.0, 0.05, 0.1, 0.15, 0.2])]:
            rows = m.mu_branch(a, p, mus, K=K)
            sl = m.alpha_slope(rows)
            out[f"a{a}p{p}K{K}"] = {
                "rows": [{k: v for k, v in r.items() if k != "b"} for r in rows],
                "b_last": rows[-1]["b"],
                "alpha_slope": sl,
                "verdict": m.marginal_verdict(sl["alpha_1"]),
                "decay_time": m.mu_decay_time(sl["alpha_1"], 0.1, 1e-3),
            }
        return out
    q("mu_branch_alpha_slope_verdict", branch)

    q("inviscid_seed", lambda m: {f"a{a}K{K}": m.inviscid_seed(a, K=K)[0]
                                  for a in (0.0, 0.17, 0.5) for K in (48,)})
    q("converged_dissipative_spectrum",
      lambda m: {k: v for k, v in m.converged_dissipative_spectrum(
          0.0, 1, 0.1, K_coarse=48, K_fine=72).items()})
    q("planted_dissipative_control",
      lambda m: {k: v for k, v in m.planted_dissipative_control(
          a=0.0, p=1, mu=0.1, K_coarse=48, K_fine=72).items()})

    n = sum(r["n"] for r in results)
    nm = sum(r["n_moved"] for r in results)
    dig_pre = _sha16(json.dumps([r["quantity"] for r in results], sort_keys=True))
    return {
        "method": ("== on float64, NaN==NaN counted identical; NOT np.allclose. The "
                   "pre-repair module is read out of git at 9dba93f and exec'd in THIS "
                   "interpreter, so numpy/BLAS are shared and any difference is the repair."),
        "grid_is_independent_of_leg_154": True,
        "n_named_quantities": len(results),
        "n_leaves": n, "n_moved": nm,
        "quantity_index_digest": dig_pre,
        "per_quantity": [{"quantity": r["quantity"], "n": r["n"], "n_moved": r["n_moved"]}
                         for r in results],
        "moved": [m for r in results for m in r["moved"]][:40],
    }


# --------------------------------------------------------------------------
# R4 -- the escape hatch, END TO END against leg 121's banked numbers (lesson, leg 135)
# --------------------------------------------------------------------------
def _ulps(a, b):
    """Distance in representable float64 steps.  A drift of a few ULP at 1e-15 is an
    environment, not a regression -- but it has to be MEASURED to be called that."""
    if a == b:
        return 0
    if not (np.isfinite(a) and np.isfinite(b)):
        return None
    ia = np.abs(np.array([a], dtype=np.float64).view(np.int64)[0])
    ib = np.abs(np.array([b], dtype=np.float64).view(np.int64)[0])
    return int(abs(ia - ib))


def r4_escape_hatch_reproduces_leg121(PRE):
    """Leg 135's rule: a repair that makes the escalating leg's battery unrunnable
    destroys the record that authorised it.

    Leg 154 checked the hatch at CONSTRUCTION level only -- its banked rows carry
    `alpha_pre = 0.8` off a synthetic `b`, not a Newton solve.  Leg 121's actual
    evidence is the END-TO-END triple (Newton residual, alpha, alpha_1).

    TWO COMPARISONS, AND THE DISTINCTION IS THE WHOLE POINT (leg 147's method):

      * IN-PROCESS, hatch vs the pre-repair module at 9dba93f, both running NOW on the
        same NumPy/BLAS.  This is the comparison that can see the repair, and it is the
        one that answers leg 135's rule.
      * AGAINST LEG 121'S BANKED JSON, written months ago on a different environment.
        A difference here is drift unless the PRE-REPAIR module reproduces the banked
        value, which is exactly what makes it separable -- so the pre-repair side is run
        through the identical harness and reported alongside.

    Both use the module's OWN `mu_branch`, i.e. leg 121's own code path, not a
    re-implementation of it.
    """
    banked = json.loads(LEG121_JSON.read_text())["C2_flow_identity_under_truncation"]
    mus, K = banked["mus"], banked["K"]

    def run(mod, p_req, hatch):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            kw = {"on_noninteger": "truncate"} if hatch else {}
            if hatch:
                # mu_branch has no on_noninteger parameter, so drive the flow directly
                # along exactly the path mu_branch takes.
                b = mod.inviscid_seed(0.0, K=K)[0]
                recs = []
                for mu in mus:
                    f = mod.CriticalDissipativeFlow(0.0, mu=float(mu), p=p_req, K=K, **kw)
                    out = f.newton(b0=b)
                    b = out["b"]
                    recs.append({"mu": float(mu), "alpha": f.alpha(b),
                                 "residual": float(out["residual"])})
            else:
                recs = [{"mu": r["mu"], "alpha": r["alpha"], "residual": r["residual"]}
                        for r in mod.mu_branch(0.0, p_req, mus, K=K)]
            sl = mod.alpha_slope(recs)
        return recs[-1]["residual"], recs[-1]["alpha"], sl["alpha_1"], w

    rows = []
    for b in banked["rows"]:
        p_req = float(b["p_requested"])
        r_post, a_post, a1_post, w = run(POST, p_req, hatch=True)
        r_pre, a_pre, a1_pre, _ = run(PRE, p_req, hatch=False)
        bank = (b["residual_fake"], b["alpha_fake"], b["alpha_1_fake"])
        rows.append({
            "p_requested": p_req, "p_true": b["p_true"],
            "p_built": POST._validated_p(p_req, "truncate"),
            "n_warnings": len(w),
            "warning_types": sorted({type(x.message).__name__ for x in w}),
            "warning_names_substitution": any("truncating to" in str(x.message) for x in w),
            # (1) the comparison that can see the repair
            "residual_hatch": r_post, "residual_pre_repair": r_pre,
            "alpha_hatch": a_post, "alpha_pre_repair": a_pre,
            "alpha_1_hatch": a1_post, "alpha_1_pre_repair": a1_pre,
            "hatch_matches_pre_repair_in_process":
                (r_post == r_pre) and (a_post == a_pre) and (a1_post == a1_pre),
            # (2) the comparison against a months-old banked number
            "residual_banked": bank[0], "alpha_banked": bank[1], "alpha_1_banked": bank[2],
            "hatch_matches_banked":
                (r_post == bank[0]) and (a_post == bank[1]) and (a1_post == bank[2]),
            "PRE_REPAIR_matches_banked":
                (r_pre == bank[0]) and (a_pre == bank[1]) and (a1_pre == bank[2]),
            "ulp_pre_repair_vs_banked": {
                "residual": _ulps(r_pre, bank[0]), "alpha": _ulps(a_pre, bank[1]),
                "alpha_1": _ulps(a1_pre, bank[2])},
        })

    # is the warning visible to a DEFAULT-configured interpreter, or swallowed?
    code = ("import sys; sys.path.insert(0,%r)\n"
            "from solver.critical_dissipation import lambda_power\n"
            "lambda_power(8, 1.9, on_noninteger='truncate')\n" % str(REPO))
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    n_in_proc = sum(r["hatch_matches_pre_repair_in_process"] for r in rows)
    n_banked = sum(r["hatch_matches_banked"] for r in rows)
    n_pre_banked = sum(r["PRE_REPAIR_matches_banked"] for r in rows)
    worst_ulp = max([u for r in rows for u in r["ulp_pre_repair_vs_banked"].values()
                     if u is not None] or [0])
    return {
        "n_rows": len(rows),
        "n_rows_hatch_matches_pre_repair_in_process": n_in_proc,
        "n_rows_hatch_matches_banked_json": n_banked,
        "n_rows_PRE_REPAIR_matches_banked_json": n_pre_banked,
        "worst_ulp_pre_repair_vs_banked": worst_ulp,
        "interpretation": (
            "The in-process count is the one that can see the repair: it compares the "
            "hatch against the pre-repair module at 9dba93f running on the SAME NumPy/BLAS "
            "in the SAME interpreter. The banked-JSON count is a comparison against numbers "
            "written months ago; it is only interpretable alongside "
            "n_rows_PRE_REPAIR_matches_banked_json, because if the PRE-REPAIR module does "
            "not reproduce its own banked value either, the difference is environmental "
            "drift and not the repair (leg 147 found the same and measured it in ULP)."),
        "warning_reaches_default_interpreter": "RuntimeWarning" in proc.stderr,
        "default_interpreter_stderr": proc.stderr.strip().splitlines()[:2],
        "leg154_checked_end_to_end": False,
        "leg154_hatch_check_scope": ("construction level only -- its banked rows carry "
                                     "alpha_pre = 0.8 off a synthetic b, not a Newton solve "
                                     "(writeup/data/p2_route_cdr_v1_repair.json, C_escape_hatch)"),
        "rows": rows,
    }


# --------------------------------------------------------------------------
# R5 -- residues re-confirmed, NOT re-litigated (all declared in the novelty pass)
# --------------------------------------------------------------------------
def r5_residues(b_seed):
    out = {}

    # p = 1e300: finite and integral, so the guard admits it.  _validated_p ONLY --
    # calling lambda_power with it is the resource exhaustion leg 154 described.
    try:
        out["p_1e300"] = {"accepted_by_guard": POST._validated_p(1e300) is not None,
                          "n_digits": len(str(int(1e300))),
                          "disposition": "leg 154 DECLARED RESIDUE, not patched; re-confirmed"}
    except Exception as e:                                        # noqa: BLE001
        out["p_1e300"] = {"accepted_by_guard": False, "exception": type(e).__name__}

    # C5-C8: declared unguarded in the module's own docstring.  NOT clause (a)'s subject.
    c = {}
    f = POST.CriticalDissipativeFlow(0.0, mu=-0.5, p=1, K=16)
    c["C5_negative_mu"] = {"accepted": True, "mu": f.mu,
                           "alpha": f.alpha(b_seed[:16]), "guarded": False}
    c["C6_mu_decay_time"] = {"negative_target": POST.mu_decay_time(1.0, 0.1, -1.0),
                             "target_above_mu0": POST.mu_decay_time(1.0, 0.1, 10.0),
                             "guarded": False}
    c["C7_marginal_verdict_nan"] = {"verdict": POST.marginal_verdict(float("nan")),
                                    "guarded": False}
    c["C8_amplitude_eigenvalue"] = {"mu_neg_1": float(POST.amplitude_eigenvalue(-1.0)),
                                    "guarded": False}
    out["C5_C8_still_unguarded"] = c
    out["C5_C8_note"] = ("Declared unguarded in the module docstring and in this leg's novelty "
                         "pass BEFORE measuring. Leg 154 was licensed for the exponent defect "
                         "and nothing else, so these are NOT clause (a) failures. Escalation "
                         "column, unchanged.")

    # the one-level-up residue: BEHAVIOURAL probe at the public entry point only.
    # solver/marginal_flow.py is outside this leg's read territory; not a line of it is read.
    try:
        from solver.marginal_flow import AugmentedFlow
        g = AugmentedFlow(0.0, p=1.9)
        out["one_level_up"] = {
            "entry_point": "solver.marginal_flow.AugmentedFlow(0.0, p=1.9)",
            "refused": False, "p_built": int(getattr(g, "p", -1)),
            "reaches_the_guard": False,
            "note": ("BEHAVIOURAL probe only -- no line of solver/marginal_flow.py is read or "
                     "edited; it is outside this leg's declared territory. Leg 154 declared "
                     "and measured this residue before its own patch (5 int(p) sites)."),
        }
    except Exception as e:                                        # noqa: BLE001
        out["one_level_up"] = {"entry_point": "solver.marginal_flow.AugmentedFlow(0.0, p=1.9)",
                               "refused": True, "exception": f"{type(e).__name__}: {e}"[:200],
                               "reaches_the_guard": True}
    return out


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("ROUTE-CDB v1 -- post-repair regression check on solver/critical_dissipation.py")
    print("Leg 170. EDITS NOTHING. Not a gCLM physics measurement; code behaviour only.\n")

    PRE, pre_src = load_pre_repair()
    rng = np.random.default_rng(20250806)
    b_seed = rng.standard_normal(200) * 0.3
    b_seed[0] = -1.0

    d = {"leg": 170, "route": "CDB",
         "title": "post-repair regression check of critical_dissipation.py's exponent guard",
         "closes_the_loop_on": {"finding_leg": 121, "repair_leg": 154},
         "pre_repair_sha": PRE_REPAIR_SHA,
         "gate_verbatim": (
             "Post-repair, does solver/critical_dissipation.py (a) reject or visibly flag "
             "every non-integer p (2s) case in leg 121's battery, and (b) reproduce every "
             "previously-validated integer-p result bit-identically?"),
         "not_a_physics_measurement": (
             "alpha_1 = 0 at a=0 (ALS eq 61), sigma=3 at a=1/2 (Xu arXiv:2607.19762 sec 6.1 "
             "+ Table 1 + Fig 3) and alpha_1 = +0.133683 (searched-not-found, leg 64) are "
             "NOT contested or re-derived. They appear only as fixed points a differential "
             "must not move. BANKED NUMBERS AT RISK: 0."),
         "edits": "none, under either branch of the gate"}

    print("[R0] lesson-90 control: pre-repair must ACCEPT p=1.9, post-repair must REFUSE")
    d["R0_control"] = r0_control(PRE, pre_src)
    r0 = d["R0_control"]
    print(f"   pre accepts p=1.9: {r0['pre_accepts_p_1p9']}   "
          f"post accepts: {r0['post_accepts_p_1p9']}   FIRES={r0['control_fires']}")
    if not r0["control_fires"]:
        print("   CONTROL DID NOT FIRE -- run is VOID")

    print("\n[R1] does leg 121's OWN driver still run against the repaired module?")
    d["R1_finding_legs_driver"] = r1_finding_legs_driver_still_runs()
    r1 = d["R1_finding_legs_driver"]
    print(f"   completed={r1['completed']}  sections {r1['n_sections_completed']}"
          f"/{r1['n_sections_total']}  aborts in {r1['abort_in_section']}  "
          f"({r1['seconds']}s)")

    print("\n[R2] clause (a): every non-integer case x every entry point")
    d["R2_clause_a"] = r2_clause_a(PRE, b_seed)
    r2 = d["R2_clause_a"]
    print(f"   {r2['n_cases_new_guard']} cases x {r2['n_entry_points']} entry points = "
          f"{r2['n_case_entrypoint_cells']} cells; refused {r2['n_cells_refused']}, "
          f"of which {r2['n_cells_CriticalDissipationDomainError']} by the NEW guard; "
          f"silently accepted {r2['n_cells_silently_accepted']}")
    print(f"   + {r2['n_cases_already_refused_pre_repair']} cases the OLD p<1 check "
          f"already refused (not evidence for the new guard)")

    print("\n[R3] clause (b): bitwise differential on integer p, independent grid")
    d["R3_clause_b"] = r3_clause_b(PRE, b_seed)
    r3 = d["R3_clause_b"]
    print(f"   {r3['n_leaves']} leaves over {r3['n_named_quantities']} named quantities, "
          f"{r3['n_moved']} moved")

    print("\n[R4] the escape hatch, END TO END against leg 121's banked triple")
    d["R4_escape_hatch"] = r4_escape_hatch_reproduces_leg121(PRE)
    r4 = d["R4_escape_hatch"]
    print(f"   hatch == pre-repair IN PROCESS: "
          f"{r4['n_rows_hatch_matches_pre_repair_in_process']}/{r4['n_rows']} rows; "
          f"vs leg 121's banked JSON: {r4['n_rows_hatch_matches_banked_json']}/{r4['n_rows']} "
          f"(pre-repair itself {r4['n_rows_PRE_REPAIR_matches_banked_json']}/{r4['n_rows']}, "
          f"worst {r4['worst_ulp_pre_repair_vs_banked']} ULP -- drift, not repair)")
    print(f"   warning reaches a default interpreter: "
          f"{r4['warning_reaches_default_interpreter']}")

    print("\n[R5] residues, re-confirmed and not re-litigated")
    d["R5_residues"] = r5_residues(b_seed)

    # ---------------- the gate ----------------
    clause_a = (r2["n_cells_silently_accepted"] == 0
                and r2["n_cells_refused"] == r2["n_case_entrypoint_cells"])
    clause_b = (r3["n_moved"] == 0)
    d["gate_answer"] = {
        "clause_a": "YES" if clause_a else "NO",
        "clause_a_detail": (
            f"{r2['n_cells_refused']}/{r2['n_case_entrypoint_cells']} case x entry-point "
            f"cells refused ({r2['n_cases_new_guard']} of leg 121's non-integer cases x "
            f"{r2['n_entry_points']} public entry points), "
            f"{r2['n_cells_CriticalDissipationDomainError']} of them by the NEW guard, "
            f"{r2['n_cells_silently_accepted']} silently accepted"),
        "clause_b": "YES" if clause_b else "NO",
        "clause_b_detail": (f"{r3['n_leaves'] - r3['n_moved']}/{r3['n_leaves']} leaves "
                            f"bit-identical over {r3['n_named_quantities']} named "
                            f"quantities, {r3['n_moved']} moved"),
        "overall": "YES" if (clause_a and clause_b) else "NO",
        "control_fires": r0["control_fires"],
        "escalations_not_gate_failures": {
            "leg121_driver_unrunnable": not r1["completed"],
            "n_sections_of_leg121_battery_lost":
                r1["n_sections_total"] - r1["n_sections_completed"],
            "one_level_up_unguarded": not d["R5_residues"]["one_level_up"]["reaches_the_guard"],
            "C5_C8_still_unguarded": True,
            "p_1e300_accepted": d["R5_residues"]["p_1e300"].get("accepted_by_guard"),
        },
    }
    d["seconds"] = round(time.time() - t0, 1)

    print("\n" + "=" * 74)
    print(f"GATE (a) {d['gate_answer']['clause_a']}: {d['gate_answer']['clause_a_detail']}")
    print(f"GATE (b) {d['gate_answer']['clause_b']}: {d['gate_answer']['clause_b_detail']}")
    print(f"OVERALL: {d['gate_answer']['overall']}   ({d['seconds']}s)")

    out = REPO / "writeup/data/p2_route_cdb_v1_postrepair.json"
    out.write_text(json.dumps(d, indent=2, default=str))
    print(f"wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
