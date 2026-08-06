"""Leg 154 — Route-CDR: the repair of solver/critical_dissipation.py, and its licence.

Leg 121 (Route-CDA) landed gate YES: the module silently truncated a non-integer `p`
(= 2s) to a different, LOWER integer exponent and returned results BIT-IDENTICAL to an
honest run of that different input, at machine precision.  It escalated rather than
patched.  This leg is the patch.

THE GATE (DIRECTION.md leg 154, verbatim):

  Post-repair: (a) does critical_dissipation.py reject or visibly flag every non-integer
  p (2s) case in leg 121's battery rather than silently truncating, with the PIN
  inverted, and (b) is the module bit-identical on every previously-passing integer-p
  case, including any capabilities.py validated line?

Clause (b) IS THE ENTIRE LICENCE.  If any clean-input result moves at all, this leg
stops and escalates; it does not iterate the repair under its own authority.  So (b) is
measured, not argued: the pre-repair module is read out of git at 9dba93f (the module's
only commit, hence a stable ancestor of main — leg 130's d871675 correction), imported
into THIS SAME PROCESS under a distinct name, and compared leaf by leaf with `==` on
float64 — not `np.allclose` — with NaN == NaN counted as identical.

Behind a LESSON-90 CONTROL: if the two module objects are not actually distinguishable,
the whole run is void.  Leg 129 shipped a differential whose control read 0/33 because
its own `sys.path.insert` had made both sides the same module.  That control is an
assert here, not a comment.

SECTIONS
  N1  the novelty pass's own claim, made executable: leg 121's PRESCRIBED predicate
  A   CLAUSE (a): every non-integer p in leg 121's battery, refused
  B   CLAUSE (b): the bitwise differential
  C   the escape hatch reproduces leg 121's measurement bit-identically (lesson, leg 135)
  D   the guard fires on 0 shipped configurations
  E   controls that must still pass, and the residues declared not-patched
"""

import hashlib
import json
import subprocess
import sys
import types
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import solver.critical_dissipation as NEW          # noqa: E402  the repaired module

PRE_REPAIR_SHA = "9dba93f"
OUT = ROOT / "writeup" / "data" / "p2_route_cdr_v1_repair.json"


# ==========================================================================
# the pre-repair module, read out of git and imported into THIS process
# ==========================================================================
def load_pre_repair():
    """`git show <sha>:solver/critical_dissipation.py`, executed as a fresh module.

    Deliberately NOT a subprocess: same interpreter, same numpy, same BLAS, so any
    difference the differential reports is the repair and not the environment.  The
    module is registered under a name that cannot collide with the real one.
    """
    src = subprocess.run(
        ["git", "show", f"{PRE_REPAIR_SHA}:solver/critical_dissipation.py"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType("_critical_dissipation_pre_repair")
    mod.__file__ = f"<git:{PRE_REPAIR_SHA}:solver/critical_dissipation.py>"
    sys.modules[mod.__name__] = mod
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, src


# ==========================================================================
# leaf comparison: exact, not approximate
# ==========================================================================
def leaves(obj, prefix=""):
    """Flatten to (name, float) leaves.  Arrays go entry by entry."""
    out = []
    if isinstance(obj, dict):
        for k in sorted(obj.keys(), key=str):
            out += leaves(obj[k], f"{prefix}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            out += leaves(v, f"{prefix}[{i}]")
    elif isinstance(obj, np.ndarray):
        flat = obj.ravel()
        if np.iscomplexobj(flat):
            for i, v in enumerate(flat):
                out.append((f"{prefix}[{i}].re", float(v.real)))
                out.append((f"{prefix}[{i}].im", float(v.imag)))
        else:
            for i, v in enumerate(flat):
                out.append((f"{prefix}[{i}]", float(v)))
    elif isinstance(obj, (bool, np.bool_)):
        out.append((prefix, float(obj)))
    elif isinstance(obj, (int, float, np.integer, np.floating)):
        out.append((prefix, float(obj)))
    elif isinstance(obj, complex):
        out.append((prefix + ".re", float(obj.real)))
        out.append((prefix + ".im", float(obj.imag)))
    elif isinstance(obj, str) or obj is None:
        out.append((prefix, obj))
    return out


def identical(x, y):
    """Bitwise-exact equality on float64, with NaN == NaN counted identical.

    `==`, not `np.allclose`.  The licence is "nothing moved", not "nothing moved much";
    a tolerance would let the repair spend a budget it was never granted.
    """
    if isinstance(x, str) or isinstance(y, str) or x is None or y is None:
        return x == y
    if np.isnan(x) and np.isnan(y):
        return True
    return x == y


def digest(vals):
    h = hashlib.sha256()
    for v in vals:
        h.update(np.float64(v).tobytes() if not isinstance(v, str) else v.encode())
    return h.hexdigest()[:16]


# ==========================================================================
# the clean-input surface: everything reachable with an INTEGER p
# ==========================================================================
def clean_surface(M, label):
    """Every quantity the module produces on well-formed, integer-p input.

    Chosen to cover the whole call graph the repair could conceivably have disturbed:
    the raw operator blocks, the flow's assembled matrices, its exact Jacobian, the
    Newton continuation in mu that IS the module's product, the alpha_1 extraction, the
    closed-form a=0 family, and the pure functions.
    """
    R = {}

    # --- the raw operator ------------------------------------------------
    for n in (2, 3, 8, 16, 33, 64, 96):
        R[f"lambda_block_n{n}"] = M.lambda_block(n)
    for K in (8, 16, 48, 64, 96, 144):
        for p in (1, 2, 3, 4, 5, 7):
            keep, drop = M.lambda_power(K, p)
            R[f"lambda_power_keep_K{K}_p{p}"] = keep
            R[f"lambda_power_drop_K{K}_p{p}"] = drop
    R["LAMBDA_SIN1"] = M.LAMBDA_SIN1
    R["CRITICAL_POINTS"] = [dict(d) for d in M.CRITICAL_POINTS]

    # p as an exactly-integral FLOAT and as np.float64 -- the inputs the guard must
    # keep accepting (leg 121's C4 pins them), exercised on the real path.
    for p in (1.0, 3.0, np.float64(3.0), np.int64(3), True):
        keep, drop = M.lambda_power(32, p)
        R[f"lambda_power_keep_K32_p{p!r}"] = keep
        R[f"lambda_power_drop_K32_p{p!r}"] = drop

    # --- the flow's assembled matrices, gauge, residual, exact Jacobian --
    rng = np.random.default_rng(20260806)
    for (a, p, K) in [(0.0, 1, 48), (0.0, 1, 96), (0.5, 3, 48), (0.5, 3, 96),
                      (0.5821792673, 5, 64), (0.25, 1, 32), (1.0, 2, 32)]:
        for mu in (0.0, 0.05, 0.2, 1.0):
            f = M.CriticalDissipativeFlow(a, mu=mu, p=p, K=K)
            tag = f"flow_a{a}_p{p}_K{K}_mu{mu}"
            R[tag + "_Lp"] = f.Lp
            R[tag + "_Lam"] = f.Lam
            R[tag + "_lam_dx0"] = f.lam_dx0
            R[tag + "_s"] = f.s
            R[tag + "_p"] = f.p
            b = rng.standard_normal(K) / np.arange(1, K + 1) ** 2
            R[tag + "_c_omega"] = f.c_omega(b)
            R[tag + "_dc_omega"] = f._dc_omega(b)
            R[tag + "_residual"] = f.residual(b)
            R[tag + "_jacobian"] = f.jacobian(b)
            R[tag + "_alpha"] = f.alpha(b)
            R[tag + "_mu_growth"] = f.mu_growth(b)
            R[tag + "_lambda_trunc"] = M.lambda_truncation(b, K, p)

    # --- the module's actual product: the mu-branch and alpha_1 ----------
    for (a, p, K) in [(0.0, 1, 48), (0.5, 3, 48), (0.5, 3, 64)]:
        rows = M.mu_branch(a, p, [0.0, 0.05, 0.1, 0.15, 0.2], K=K, da=0.05)
        for r in rows:
            tag = f"branch_a{a}_p{p}_K{K}_mu{r['mu']}"
            for key in ("residual", "alpha", "mu_growth", "gauge",
                        "omega_x0", "tail", "lambda_truncation"):
                R[tag + "_" + key] = r[key]
            R[tag + "_b"] = r["b"]
        sl = M.alpha_slope(rows)
        for key in ("alpha_0", "alpha_1", "alpha_2", "alpha_1_chord",
                    "secant_spread", "mu", "secants"):
            R[f"slope_a{a}_p{p}_K{K}_{key}"] = sl[key]
        R[f"verdict_a{a}_p{p}_K{K}"] = M.marginal_verdict(sl["alpha_1"])

    # --- the pure functions ----------------------------------------------
    for a1 in (0.0, 1e-12, 0.133683, 1.4675439450790417, 3.5251293668, -0.5, 1e6):
        R[f"verdict_{a1}"] = M.marginal_verdict(a1)
        for mu0, tgt in [(1.0, 1e-3), (0.5, 1e-6), (0.2, 0.1)]:
            R[f"decay_{a1}_{mu0}_{tgt}"] = M.mu_decay_time(a1, mu0, tgt)
    R["amplitude_eigenvalue"] = M.amplitude_eigenvalue(
        np.linspace(0.0, 4.0, 401))

    X = np.concatenate([np.linspace(-40, 40, 1601), [0.0]])
    for mu in (0.0, 0.05, 0.25, 1.0, 3.0):
        om, mu0, lam = M.exact_a0_family(mu, X)
        R[f"exact_family_mu{mu}_om"] = om
        R[f"exact_family_mu{mu}_mu0"] = mu0
        R[f"exact_family_mu{mu}_lam"] = lam
    x = np.linspace(-12, 12, 801)
    for (t, nu, m0) in [(0.0, 1e-2, 0.3), (0.5, 1e-3, 1.0), (0.9, 1.0, 2.0)]:
        q = M.exact_a0_spacetime(x, t, nu, m0)
        for k in ("omega", "H_omega", "lambda_omega", "omega_t", "z"):
            R[f"exact_st_t{t}_nu{nu}_m{m0}_{k}"] = q[k]
        R[f"exact_res_t{t}_nu{nu}_m{m0}"] = M.exact_a0_residual(x, t, nu, m0)

    print(f"  [{label}] clean surface built: {len(R)} named quantities")
    return R


# ==========================================================================
# N1 — the novelty pass's claim, executable
# ==========================================================================
def section_N1():
    """Leg 121's PRESCRIBED predicate, run.  The novelty pass says it is insufficient;
    this makes that a measurement rather than a recollection."""
    def prescribed(p):
        if float(p) != round(float(p)):
            raise ValueError("non-integral p")
        return int(p)

    rows = []
    for c in [1, 3, 5, 1.0, 3.0, np.float64(3.0), np.int64(3), True, "3",
              1.9, 2.9999999, "3.5", float("nan"), float("inf"), float("-inf"),
              1e300, 2.0 ** 53 + 1.0, None, 1 + 0j]:
        rec = {"input": repr(c)}
        try:
            r = prescribed(c)
            rec["prescribed"] = "accepted"
            rec["prescribed_p"] = str(r) if abs(r) < 10 ** 12 else f"<{len(str(r))}-digit int>"
            rec["prescribed_exc"] = None
        except Exception as e:
            rec["prescribed"] = "raised"
            rec["prescribed_p"] = None
            rec["prescribed_exc"] = type(e).__name__
        try:
            r = NEW._validated_p(c)
            rec["adopted"] = "accepted"
            rec["adopted_p"] = str(r) if abs(r) < 10 ** 12 else f"<{len(str(r))}-digit int>"
            rec["adopted_exc"] = None
        except Exception as e:
            rec["adopted"] = "raised"
            rec["adopted_p"] = None
            rec["adopted_exc"] = type(e).__name__
        rec["differs"] = (rec["prescribed"], rec["prescribed_exc"]) != \
                         (rec["adopted"], rec["adopted_exc"])
        rows.append(rec)

    inf_row = [r for r in rows if r["input"] == "inf"][0]
    # the headline of the novelty pass, asserted
    assert inf_row["prescribed_exc"] == "OverflowError", inf_row
    assert inf_row["adopted_exc"] == "CriticalDissipationDomainError", inf_row
    # and the mechanism: floor(inf) == inf, so an integrality-only test is BLIND to inf
    floor_blind = bool(np.floor(np.inf) == np.inf)
    assert floor_blind

    print(f"  N1: {sum(r['differs'] for r in rows)}/{len(rows)} inputs where leg 121's "
          f"prescribed predicate and the adopted one disagree")
    return {"rows": rows,
            "n_disagree": int(sum(r["differs"] for r in rows)),
            "floor_of_inf_equals_inf": floor_blind,
            "prescribed_raises_OverflowError_on_inf": True,
            "note": ("np.floor(inf) == inf is True, so an integrality-only predicate does "
                     "not merely mis-handle infinity, it ADMITS it. The isfinite clause is "
                     "measured necessary, not defensive decoration. SEI CERT FLP04-C.")}


# ==========================================================================
# A — CLAUSE (a): every non-integer p from leg 121's battery, refused
# ==========================================================================
def section_A(PRE):
    """Leg 121's own C1/C2/C3/C4 inputs, replayed against the repaired module.

    Every case is run against BOTH modules, so each row carries the pre-repair
    behaviour it is being contrasted with rather than quoting leg 121's JSON.
    """
    C1 = []
    for p in [1.9, 1.0000001, 2.9999999, 2.9, 3.9]:      # leg 121 C1's five
        rec = {"p_requested": p}
        keep_old, _ = PRE.lambda_power(64, p)
        rec["pre_repair"] = "accepted"
        rec["pre_repair_p_used"] = int(p)
        try:
            NEW.lambda_power(64, p)
            rec["post_repair"] = "ACCEPTED -- CLAUSE (a) FAILS"
            rec["post_repair_exc"] = None
        except NEW.CriticalDissipationDomainError as e:
            rec["post_repair"] = "refused"
            rec["post_repair_exc"] = "CriticalDissipationDomainError"
            rec["post_repair_msg_names_both"] = (str(int(p)) in str(e)
                                                 and repr(p) in str(e))
        rec["is_ValueError"] = issubclass(NEW.CriticalDissipationDomainError, ValueError)
        C1.append(rec)

    # C2 -- THE HEADLINE. leg 121's nine, full pipeline.
    C2 = []
    for p_req in [1.1, 1.5, 1.9, 2.1, 2.5, 2.9, 3.1, 3.5, 3.9]:
        p_true = int(p_req)
        rec = {"p_requested": p_req, "p_pre_repair_built": p_true,
               "s_requested": 0.5 * p_req, "s_pre_repair_built": 0.5 * p_true}
        f_old = PRE.CriticalDissipativeFlow(0.0, mu=0.1, p=p_req, K=64)
        rec["pre_repair_p_attr"] = int(f_old.p)
        rec["pre_repair_s_attr"] = float(f_old.s)
        try:
            NEW.CriticalDissipativeFlow(0.0, mu=0.1, p=p_req, K=64)
            rec["post_repair"] = "ACCEPTED -- CLAUSE (a) FAILS"
            rec["post_repair_exc"] = None
        except NEW.CriticalDissipationDomainError:
            rec["post_repair"] = "refused"
            rec["post_repair_exc"] = "CriticalDissipationDomainError"
        C2.append(rec)

    # C3 -- the realistic float near-miss: p computed, not typed.
    p_near = 2.0 * (2.5 - 1e-12)
    C3 = {"expression": "2.0 * (2.5 - 1e-12)", "value": p_near,
          "pre_repair_p_used": int(p_near), "intended_p": 5,
          "units_lost": 5 - int(p_near)}
    try:
        NEW.lambda_power(32, p_near)
        C3["post_repair"] = "ACCEPTED -- CLAUSE (a) FAILS"
    except NEW.CriticalDissipationDomainError:
        C3["post_repair"] = "refused"
    # the two constructions leg 121 recorded as NOT triggering it must still be accepted
    C3["non_triggering_still_accepted"] = []
    for expr, val in [("2.0 * (5 * 0.1 * 5)", 2.0 * (5 * 0.1 * 5)),
                      ("2.0 * sum of five 0.5s", 2.0 * sum([0.5] * 5))]:
        ok = True
        try:
            NEW.lambda_power(16, val)
        except Exception:
            ok = False
        C3["non_triggering_still_accepted"].append(
            {"expr": expr, "value": val, "is_exactly_integral": float(val).is_integer(),
             "accepted": ok})

    # C4 -- the type-coercion asymmetry, in BOTH directions.
    C4 = []
    for c in [3.5, "3.5", "3.0", "3", 3.0, np.float64(3.0), np.int64(3), 3]:
        rec = {"input": repr(c), "type": type(c).__name__}
        for name, M in (("pre_repair", PRE), ("post_repair", NEW)):
            try:
                M.lambda_power(16, c)
                rec[name] = "accepted"
                rec[name + "_exc"] = None
            except Exception as e:
                rec[name] = "refused"
                rec[name + "_exc"] = type(e).__name__
        rec["unchanged"] = rec["pre_repair"] == rec["post_repair"]
        C4.append(rec)

    # non-finite p: the novelty pass's own addition to leg 121's battery
    NF = []
    for c in [float("nan"), float("inf"), float("-inf")]:
        rec = {"input": repr(c)}
        for name, M in (("pre_repair", PRE), ("post_repair", NEW)):
            try:
                M.lambda_power(16, c)
                rec[name + "_exc"] = None
            except Exception as e:
                rec[name + "_exc"] = type(e).__name__
        NF.append(rec)

    n_refused = sum(r["post_repair"] == "refused" for r in C1) + \
        sum(r["post_repair"] == "refused" for r in C2) + \
        (1 if C3["post_repair"] == "refused" else 0)
    n_total = len(C1) + len(C2) + 1
    print(f"  A: clause (a) -- {n_refused}/{n_total} non-integer p cases from leg 121's "
          f"battery now REFUSED (was 0/{n_total})")
    print(f"     C4 type-coercion: {sum(r['unchanged'] for r in C4)}/{len(C4)} "
          f"unchanged, and the one that moves is p=3.5 (float), by design")
    return {"C1": C1, "C2": C2, "C3": C3, "C4": C4, "non_finite": NF,
            "n_refused": n_refused, "n_total": n_total,
            "n_refused_pre_repair": 0}


# ==========================================================================
# B — CLAUSE (b): the bitwise differential.  THE LICENCE.
# ==========================================================================
def section_B(PRE, PRE_SRC):
    # ---- LESSON-90 CONTROL, first, as an assert ------------------------
    # If the two module objects are not distinguishable, every "identical" below is a
    # tautology of the code and the run is void (leg 129 shipped exactly that bug).
    ctrl = {
        "modules_are_distinct_objects": PRE is not NEW,
        "pre_repair_has_guard": hasattr(PRE, "_validated_p"),
        "post_repair_has_guard": hasattr(NEW, "_validated_p"),
        "pre_repair_file": PRE.__file__,
        "post_repair_file": NEW.__file__,
        "pre_repair_src_sha256": hashlib.sha256(PRE_SRC.encode()).hexdigest()[:16],
        "post_repair_src_sha256": hashlib.sha256(
            (ROOT / "solver" / "critical_dissipation.py").read_text().encode()
        ).hexdigest()[:16],
    }
    # the differential is only meaningful if the two sides genuinely differ
    assert ctrl["modules_are_distinct_objects"]
    assert not ctrl["pre_repair_has_guard"], \
        "VOID: the 'pre-repair' module already has the guard -- both sides are the repair"
    assert ctrl["post_repair_has_guard"]
    assert ctrl["pre_repair_src_sha256"] != ctrl["post_repair_src_sha256"]
    # and the control must be able to report the other answer: on the ONE input the
    # repair is about, the two modules MUST disagree.
    pre_ok = True
    try:
        PRE.lambda_power(16, 1.9)
    except Exception:
        pre_ok = False
    post_ok = True
    try:
        NEW.lambda_power(16, 1.9)
    except Exception:
        post_ok = False
    ctrl["pre_accepts_p_1p9"] = pre_ok
    ctrl["post_accepts_p_1p9"] = post_ok
    assert pre_ok and not post_ok, "VOID: the two modules are not behaviourally distinct"
    print(f"  B: lesson-90 control PASSES -- the two modules are distinguishable "
          f"(pre accepts p=1.9, post refuses)")

    # ---- the differential ----------------------------------------------
    old = clean_surface(PRE, "pre-repair")
    new = clean_surface(NEW, "post-repair")
    assert set(old) == set(new), "surface keys differ between the two modules"

    n_leaf = 0
    moved = []
    per_key = {}
    for k in sorted(old):
        lo, ln = leaves(old[k], k), leaves(new[k], k)
        if len(lo) != len(ln):
            moved.append({"leaf": k, "reason": "shape", "old": len(lo), "new": len(ln)})
            continue
        bad = 0
        for (n1, v1), (n2, v2) in zip(lo, ln):
            n_leaf += 1
            if not identical(v1, v2):
                bad += 1
                if len(moved) < 50:
                    moved.append({"leaf": n1, "old": repr(v1), "new": repr(v2)})
        per_key[k] = {"n": len(lo), "n_moved": bad}

    all_old = [v for k in sorted(old) for _, v in leaves(old[k], k)]
    all_new = [v for k in sorted(new) for _, v in leaves(new[k], k)]

    print(f"  B: clause (b) -- {n_leaf - len(moved)}/{n_leaf} clean-input leaves "
          f"BIT-IDENTICAL, {len(moved)} moved")
    return {"n_leaves": n_leaf, "n_moved": len(moved), "moved": moved[:50],
            "n_named_quantities": len(old),
            "digest_pre_repair": digest(all_old), "digest_post_repair": digest(all_new),
            "lesson90_control": ctrl,
            "per_quantity": {k: v for k, v in per_key.items() if v["n_moved"]} or
                            "every named quantity 0/0 moved",
            "method": ("== on float64, NaN==NaN counted identical; NOT np.allclose. The "
                       "pre-repair module is read out of git at 9dba93f and exec'd in "
                       "THIS interpreter, so numpy/BLAS are shared and any difference is "
                       "the repair.")}


# ==========================================================================
# C — the escape hatch keeps leg 121's measurement runnable (lesson, leg 135)
# ==========================================================================
def section_C(PRE):
    """A repair that makes the escalating leg's battery unrunnable destroys the record
    that authorised it.  So on_noninteger='truncate' must reproduce leg 121's numbers
    BIT-IDENTICALLY, behind a warning."""
    rows = []
    for p_req, p_true in [(1.9, 1), (2.9, 2), (3.9, 3)]:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            f_new = NEW.CriticalDissipativeFlow(0.0, mu=0.1, p=p_req, K=64,
                                                on_noninteger="truncate")
            n_warn = len(w)
            wtype = type(w[0].message).__name__ if w else None
            wmsg = str(w[0].message) if w else None
        f_old = PRE.CriticalDissipativeFlow(0.0, mu=0.1, p=p_req, K=64)
        b = np.zeros(64); b[0] = -1.0
        rec = {"p_requested": p_req, "p_built": int(f_new.p),
               "n_warnings": n_warn, "warning_type": wtype,
               "warning_names_the_substitution": bool(
                   wmsg and str(p_true) in wmsg and repr(p_req) in wmsg),
               "warning": wmsg}
        pairs = {"s": (f_old.s, f_new.s),
                 "alpha": (f_old.alpha(b), f_new.alpha(b)),
                 "c_omega": (f_old.c_omega(b), f_new.c_omega(b))}
        for nm, (a_, b_) in pairs.items():
            rec[nm + "_pre"] = float(a_)
            rec[nm + "_post"] = float(b_)
            rec[nm + "_bit_identical"] = identical(float(a_), float(b_))
        arrs = {"Lp": (f_old.Lp, f_new.Lp), "Lam": (f_old.Lam, f_new.Lam),
                "residual": (f_old.residual(b), f_new.residual(b)),
                "jacobian": (f_old.jacobian(b), f_new.jacobian(b))}
        rec["arrays_bit_identical"] = all(
            np.array_equal(x, y, equal_nan=True) for x, y in arrs.values())
        rec["n_array_entries"] = int(sum(np.size(x) for x, _ in arrs.values()))
        rows.append(rec)
    n_ok = sum(r["arrays_bit_identical"] and r["alpha_bit_identical"] for r in rows)
    print(f"  C: escape hatch -- {n_ok}/{len(rows)} truncate-mode runs reproduce the "
          f"pre-repair module bit-identically, each behind exactly one RuntimeWarning")
    return {"rows": rows, "n_bit_identical": n_ok, "n_total": len(rows)}


# ==========================================================================
# D — how often does the guard fire on things this repository actually runs?
# ==========================================================================
def section_D():
    """The guard's cost, measured rather than asserted: it must fire on NOTHING that
    ships.  Every p that appears in the repository's own call graph is exercised."""
    shipped = []
    for d in NEW.CRITICAL_POINTS:
        shipped.append(("CRITICAL_POINTS " + d["label"], d["p"]))
    for p in (1, 2, 3, 4, 5, 7):
        shipped.append((f"literal {p}", p))
    for p in (1.0, 3.0, np.float64(3.0), np.int64(3), True):
        shipped.append((f"integral non-int type {p!r}", p))
    fired = []
    for label, p in shipped:
        try:
            NEW._validated_p(p)
        except Exception as e:
            fired.append({"case": label, "exc": type(e).__name__})
    print(f"  D: the guard fires on {len(fired)}/{len(shipped)} shipped configurations")
    return {"n_shipped": len(shipped), "n_fired": len(fired), "fired": fired,
            "cases": [c for c, _ in shipped]}


# ==========================================================================
# E — controls that must still pass, and the residues NOT patched
# ==========================================================================
def section_E(PRE):
    # leg 121's sub-integer CONTROL: still a ValueError, in both modules
    ctrl = []
    for p in (0.5, 0.999, -0.5, -3, 0):
        rec = {"p": p}
        for name, M in (("pre_repair", PRE), ("post_repair", NEW)):
            try:
                M.lambda_power(16, p)
                rec[name] = "accepted -- CONTROL BROKEN"
            except ValueError as e:
                rec[name] = "ValueError"
                rec[name + "_class"] = type(e).__name__
            except Exception as e:
                rec[name] = f"WRONG TYPE: {type(e).__name__}"
        rec["both_ValueError"] = rec["pre_repair"] == rec["post_repair"] == "ValueError"
        ctrl.append(rec)

    # the residues, MEASURED and declared not-patched
    res = {}
    huge = 1e300
    res["p_1e300"] = {
        "accepted_by_guard": True, "n_digits_of_int": len(str(int(huge))),
        "disposition": "DECLARED RESIDUE, NOT PATCHED",
        "reason": ("finite and integral, so the guard admits it; the resulting "
                   "lambda_power loop is a resource exhaustion (unbounded matmul chain, "
                   "eventual MemoryError) -- LOUD, not a silent substitution of a "
                   "different exponent, which is the only thing this repair is licensed "
                   "to close. A cap would be an arbitrary threshold with no measurement "
                   "behind it.")}
    try:
        NEW._validated_p(huge)
        res["p_1e300"]["confirmed_accepted"] = True
    except Exception:
        res["p_1e300"]["confirmed_accepted"] = False

    # the identical defect one level up, OUTSIDE this leg's territory
    mf = (ROOT / "solver" / "marginal_flow.py").read_text().splitlines()
    hits = [{"line": i + 1, "text": ln.strip()}
            for i, ln in enumerate(mf) if "int(p)" in ln]
    res["marginal_flow_int_p"] = {
        "hits": hits, "n": len(hits),
        "disposition": "DECLARED RESIDUE, OUT OF TERRITORY",
        "reason": ("solver/marginal_flow.py carries the IDENTICAL int(p) truncation one "
                   "level up, so a non-integer p handed to AugmentedFlow is truncated "
                   "there BEFORE it reaches this repair's guard. Editing it would fail "
                   "the merge gate's territory check. Declared in the novelty pass, "
                   "BEFORE construction, so it is not discovered later as a surprise.")}
    # measured, not asserted: does the residue actually bite?
    import solver.marginal_flow as MF
    af = MF.AugmentedFlow(0.0, p=1.9, K=16) if _accepts(MF) else None
    res["marginal_flow_int_p"]["AugmentedFlow_p1p9_still_truncates"] = (
        int(af.p) if af is not None else "raised")
    res["marginal_flow_int_p"]["AugmentedFlow_p_built"] = (
        int(af.p) if af is not None else None)

    res["unguarded_by_design"] = {
        "mu_lt_0": "leg 121 C5 -- not the gate's subject, still open",
        "mu_decay_time_domain": "leg 121 C6 -- not the gate's subject, still open",
        "marginal_verdict_nonfinite": "leg 121 C7 -- not the gate's subject, still open",
        "amplitude_eigenvalue_mu_lt_0": "leg 121 C8 -- not the gate's subject, still open",
        "note": ("The gate licenses the exponent-truncation repair and nothing else. "
                 "Each of these is documented in the module docstring as a live "
                 "escalation rather than silently left.")}

    print(f"  E: {sum(r['both_ValueError'] for r in ctrl)}/{len(ctrl)} sub-integer "
          f"CONTROLs still raise ValueError in BOTH modules; "
          f"{len(hits)} out-of-territory int(p) sites declared")
    return {"sub_integer_controls": ctrl, "residues": res}


def _accepts(MF):
    try:
        MF.AugmentedFlow(0.0, p=1.9, K=16)
        return True
    except Exception:
        return False


# ==========================================================================
def main():
    print("Leg 154 — Route-CDR: the repair of solver/critical_dissipation.py")
    print(f"  pre-repair pin: {PRE_REPAIR_SHA} (the module's only commit)")
    PRE, PRE_SRC = load_pre_repair()

    out = {
        "leg": 154, "route": "CDR",
        "title": "repair of critical_dissipation.py's silent exponent truncation",
        "pre_repair_sha": PRE_REPAIR_SHA,
        "gate_verbatim": (
            "Post-repair: (a) does critical_dissipation.py reject or visibly flag every "
            "non-integer p (2s) case in leg 121's battery rather than silently "
            "truncating, with the PIN inverted, and (b) is the module bit-identical on "
            "every previously-passing integer-p case, including any capabilities.py "
            "validated line?"),
        "not_a_physics_measurement": (
            "No gCLM physics is measured or contested here. alpha_1 = 0 at a=0, "
            "sigma=3 at a=1/2 and alpha_1 = +0.133683 stand exactly as banked in "
            "capabilities.py. Every alpha value below appears ONLY as a bit-pattern "
            "required to be UNCHANGED between two versions of the same code -- the "
            "opposite of a measurement claim."),
    }
    out["N1_prescribed_predicate"] = section_N1()
    out["A_clause_a_refusals"] = section_A(PRE)
    out["B_clause_b_differential"] = section_B(PRE, PRE_SRC)
    out["C_escape_hatch"] = section_C(PRE)
    out["D_guard_firing_rate"] = section_D()
    out["E_controls_and_residues"] = section_E(PRE)

    a, b = out["A_clause_a_refusals"], out["B_clause_b_differential"]
    out["gate_answer"] = {
        "clause_a": "YES" if a["n_refused"] == a["n_total"] else "NO",
        "clause_a_detail": f"{a['n_refused']}/{a['n_total']} refused "
                           f"(was {a['n_refused_pre_repair']}/{a['n_total']})",
        "clause_b": "YES" if b["n_moved"] == 0 else "NO",
        "clause_b_detail": f"{b['n_leaves'] - b['n_moved']}/{b['n_leaves']} "
                           f"clean-input leaves bit-identical, {b['n_moved']} moved",
    }
    out["gate_answer"]["overall"] = (
        "YES" if out["gate_answer"]["clause_a"] == "YES"
        and out["gate_answer"]["clause_b"] == "YES" else "NO")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, default=str))
    print(f"\nGATE: clause (a) {out['gate_answer']['clause_a']} "
          f"({out['gate_answer']['clause_a_detail']}); "
          f"clause (b) {out['gate_answer']['clause_b']} "
          f"({out['gate_answer']['clause_b_detail']})")
    print(f"wrote {OUT}")
    return out


if __name__ == "__main__":
    main()
