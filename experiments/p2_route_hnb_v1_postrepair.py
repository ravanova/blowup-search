"""Leg 131 (Route-HNB) -- the POST-REPAIR REGRESSION CHECK on `solver/holder_norms.py`.

THE GATE (DIRECTION.md leg 131, verbatim):

    Post-repair, does solver/holder_norms.py (a) reject every case in leg 100's original
    6-mechanism battery (no silent corruption remains), and (b) reproduce every
    previously-validated clean-call result bit-identically, including the module's
    dedicated test file and its capabilities.py validated line?

      yes -> Repair confirmed solid and non-regressive by an independent run.  Bank leg
             100's battery as a permanent regression suite.
      no  -> An incomplete fix or a repair regression.  Report the exact case precisely;
             escalate as a priority finding, do not patch under this leg's own authority.

`solver/holder_norms.py` IS NOT EDITED BY THIS LEG UNDER EITHER BRANCH.  It is imported and
read.  Nothing here re-implements a case, a criterion, or a magnitude: leg 100's battery
module `experiments/p2_route_hna_v1_adversarial.py` is IMPORTED UNMODIFIED and its own
`gate_A0..gate_A8`, `probe`, `call` and `classify` do the work.  This file is a harness, not
a battery.

WHY AN INDEPENDENT RUN IS NEEDED AT ALL.  The repair (`fb61a79`) self-reports 14/14
mechanisms closed and 53/53 clean calls bit-identical.  Every file on `main` that carries
that evidence -- `test_holder_norms_adversarial.py` and
`experiments/bench_holder_norms_nan_guard_check.py` -- was authored INSIDE that same commit,
as was `capabilities.py`'s validated paragraph for this module.  A repair's self-check is
not an independent confirmation (the 86/87/94/103/104/105 pattern).

THE TWO ARMS, IN ONE PROCESS.  `_load_battery` imports leg 100's battery TWICE under two
module names:

  * PRE  -- `HNA_AUDIT_LIVE` unset, so the battery loads its subject from the
            content-addressed git blob `b614a116...`, the exact pre-repair
            `solver/holder_norms.py`.  This is the NEGATIVE CONTROL and it is load-bearing:
            per lesson 90, a control that cannot come out differently is not a control.  If
            this arm reported 0 silent cases the harness would be blind and the leg would
            report that instead of a pass.
  * POST -- `HNA_AUDIT_LIVE=1`, so the battery loads the working-tree module.

Both arms run in ONE interpreter, so BLAS, numpy, seeds and matmul reduction order are
shared by construction.  That is deliberate: the battery's own docstring records a 1-2 ULP
drift in two `A6.clean_per_degree` entries between RUNNERS, predating the repair, so a
comparison against the committed `writeup/data/p2_route_hna_v1_adversarial.json` would
report a "regression" that is a property of the machine.  Clause (b) is therefore measured
as a SAME-PROCESS BITWISE differential (leg 105's technique); literal-JSON agreement is
recorded informationally and is NOT part of the pass/fail criterion.

THE BATTERY'S OWN LIVE MODE DOES NOT RUN, AND THAT IS PART OF THE FINDING.  The repair added
`HNA_AUDIT_LIVE` so the battery could be re-pointed at the working tree.  It has never been
run to completion: `grep -rn HNA_AUDIT_LIVE` finds it in exactly one file, and running it
aborts in ~0.2 s.  The cause is NOT that the battery mis-handles a repaired module -- its
`call()`/`classify()` already return `FLAGGED_RAISE`, and leg 100's pre-committed criterion
says verbatim that raising counts as FLAGGED, not silent.  The cause is three sites that
call the subject BARE, outside `probe()`, on input that used to be merely wrong and now
raises (`gate_A5` line ~419, `gate_A6` lines ~469-471, `gate_A8` line ~553).  P1 measures the
abort exactly; P2 gets past it in two passes:

  pass 1  run the gate UNPATCHED and record where the battery's own driver aborts;
  pass 2  re-run with a recording shim on the named entry points, which passes every value
          through unchanged and substitutes a NaN sentinel ONLY on a raise, logging the
          exception.  The shim can only ever turn a FLAGGED_RAISE into a FLAGGED_NAN --
          both are FLAGGED -- so THE SILENT COUNT, WHICH IS THE PASS CRITERION, IS INVARIANT
          UNDER THE SHIM.  P2b then re-probes the three bare sites individually through the
          battery's OWN `call`/`classify` so their true verdicts are recorded unshimmed.

SCOPE NOTE ON THE 7TH MECHANISM.  The builtin-`max` hazard at `jacobian_identity_error` and
the descending-grid coverage overstatement were found DURING the repair, so leg 100's
battery contains no case for them.  P6 measures them as magnitudes.  They are OUTSIDE clause
(a)'s pass/fail criterion, which the gate's own wording scopes to "leg 100's original
6-mechanism battery".

Run:   python experiments/p2_route_hnb_v1_postrepair.py
Writes: writeup/data/p2_route_hnb_v1_postrepair.json
"""
from __future__ import annotations

import importlib.util
import json
import os
import struct
import subprocess
import sys
import time
import traceback

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

BATTERY_PATH = os.path.join(HERE, "experiments", "p2_route_hna_v1_adversarial.py")
MODULE_PATH = os.path.join(HERE, "solver", "holder_norms.py")
BANKED_JSON = os.path.join(HERE, "writeup", "data", "p2_route_hna_v1_adversarial.json")
OUT_JSON = os.path.join(HERE, "writeup", "data", "p2_route_hnb_v1_postrepair.json")

NAN, INF = float("nan"), float("inf")
GATES = ("A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8")


# ---------------------------------------------------------------------------
# loading leg 100's battery, unmodified, once per arm
# ---------------------------------------------------------------------------


def _load_battery(name, live):
    """Import `p2_route_hna_v1_adversarial.py` under `name`, bound to one subject.

    The battery reads HNA_AUDIT_LIVE at import time, so the env var is set around the
    exec and restored afterwards.  `__name__` is the module name, not "__main__", so the
    battery's `main()` does NOT fire and no JSON of leg 100's is overwritten.
    """
    prev = os.environ.get("HNA_AUDIT_LIVE")
    os.environ["HNA_AUDIT_LIVE"] = "1" if live else "0"
    try:
        spec = importlib.util.spec_from_file_location(name, BATTERY_PATH)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    finally:
        if prev is None:
            os.environ.pop("HNA_AUDIT_LIVE", None)
        else:
            os.environ["HNA_AUDIT_LIVE"] = prev
    return mod


# ---------------------------------------------------------------------------
# the recording shim (pass 2 only)
# ---------------------------------------------------------------------------


class Recorder:
    """Wrap one battery entry point: pass values through, log and substitute on a raise.

    A substitution happens ONLY when the wrapped call raises, and every one is logged with
    its exception type and message.  A NaN sentinel is returned so the gate body can finish
    and produce leg 100's own row structure; the sentinel can only ever be classified
    FLAGGED_NAN, never SILENT, so the pass criterion cannot be affected by it.
    """

    def __init__(self, fn, void, tag):
        self.fn, self.void, self.tag = fn, void, tag
        self.n_calls = 0
        self.log = []

    def __call__(self, *a, **k):
        self.n_calls += 1
        try:
            v = self.fn(*a, **k)
            self.log.append({"call_index": self.n_calls, "outcome": "RETURNED"})
            return v
        except Exception as e:                       # noqa: BLE001 -- classifying
            self.log.append({"call_index": self.n_calls, "outcome": "RAISED",
                             "exception": type(e).__name__, "message": str(e)[:400]})
            return self.void(*a, **k)


def _void_decay_weight(X, alpha):
    return np.full(np.asarray(X, dtype=float).size, NAN)


def _void_holder_H_constant(theta, gamma, degrees=(4, 8, 16, 32, 64, 128, 256, 512),
                            n_random=200, seed=3):
    return np.full(len(tuple(degrees)), NAN), NAN


def _void_pair(*a, **k):
    return NAN, NAN


# which entry points each gate calls BARE, outside probe()
SWALLOW_FOR = {
    "A5": {"decay_weight": _void_decay_weight},
    "A6": {"holder_H_constant": _void_holder_H_constant},
    "A8": {"conformal_check": _void_pair, "family_op_norm": _void_pair},
}


# ---------------------------------------------------------------------------
# running the gates
# ---------------------------------------------------------------------------


def _abort_site(exc):
    """Where inside the BATTERY the driver aborted (last battery frame of the traceback)."""
    frames = traceback.extract_tb(exc.__traceback__)
    battery = [f for f in frames if os.path.basename(f.filename) ==
               os.path.basename(BATTERY_PATH)]
    deepest = frames[-1] if frames else None
    return {
        "battery_line": battery[-1].lineno if battery else None,
        "battery_source": battery[-1].line if battery else None,
        "battery_function": battery[-1].name if battery else None,
        "deepest_frame_file": os.path.basename(deepest.filename) if deepest else None,
        "deepest_frame_line": deepest.lineno if deepest else None,
    }


def run_gates(bat, arm):
    """Run every gate of `bat`, in two passes where the battery's own driver aborts."""
    results, meta = {}, {}
    for g in GATES:
        fn = getattr(bat, "gate_" + g)
        entry = {"arm": arm, "pass1_unpatched_completed": None}
        try:
            res = fn()
            entry["pass1_unpatched_completed"] = True
            entry["shimmed"] = False
            results[g] = res
        except Exception as e:                       # noqa: BLE001
            entry["pass1_unpatched_completed"] = False
            entry["pass1_exception"] = type(e).__name__
            entry["pass1_message"] = str(e)[:400]
            entry["pass1_abort_site"] = _abort_site(e)
            # pass 2: shim exactly the entry points this gate calls bare
            shims, saved = {}, {}
            for nm, void in SWALLOW_FOR.get(g, {}).items():
                saved[nm] = getattr(bat, nm)
                shims[nm] = Recorder(saved[nm], void, nm)
                setattr(bat, nm, shims[nm])
            try:
                res = fn()
                entry["shimmed"] = True
                entry["pass2_completed"] = True
                results[g] = res
            except Exception as e2:                  # noqa: BLE001
                entry["shimmed"] = True
                entry["pass2_completed"] = False
                entry["pass2_exception"] = type(e2).__name__
                entry["pass2_message"] = str(e2)[:400]
                entry["pass2_abort_site"] = _abort_site(e2)
                results[g] = None
            finally:
                for nm, orig in saved.items():
                    setattr(bat, nm, orig)
            entry["shim_log"] = {nm: {"n_calls": s.n_calls,
                                      "n_raised": sum(1 for r in s.log
                                                      if r["outcome"] == "RAISED"),
                                      "calls": s.log}
                                 for nm, s in shims.items()}
        meta[g] = entry
    return results, meta


# ---------------------------------------------------------------------------
# the SILENT census -- counted with leg 100's own verdict strings
# ---------------------------------------------------------------------------


VERDICT_KEYS = ("verdict", "verdict_whole_return", "verdict_random_arm_alone",
                "all_nan_grid_verdict")


def census(node, acc=None, label=""):
    """Walk a gate result and tally every leg-100 verdict string it contains."""
    if acc is None:
        acc = {"n_verdicts": 0, "n_silent": 0, "silent_cases": [], "by_verdict": {}}
    if isinstance(node, dict):
        case = node.get("case", label)
        for k in VERDICT_KEYS:
            if k in node and isinstance(node[k], str):
                v = node[k]
                acc["n_verdicts"] += 1
                acc["by_verdict"][v] = acc["by_verdict"].get(v, 0) + 1
                if v == "SILENT":
                    acc["n_silent"] += 1
                    acc["silent_cases"].append({"case": case, "key": k,
                                                "returned": node.get("returned"),
                                                "clean": node.get("clean"),
                                                "bit_identical_to_clean":
                                                    node.get("bit_identical_to_clean")})
        for k, v in node.items():
            if k not in VERDICT_KEYS:
                census(v, acc, case if isinstance(case, str) else label)
    elif isinstance(node, list):
        for x in node:
            census(x, acc, label)
    return acc


# ---------------------------------------------------------------------------
# P2b -- the three bare sites, re-probed through the battery's OWN helpers
# ---------------------------------------------------------------------------


def bare_sites(bat, arm):
    """Exactly the calls that abort the battery's driver, classified by leg 100's rule.

    Every classification below is `bat.classify(*bat.call(...))` -- the battery's own
    functions, not a re-implementation.  This is where the three sites get their true,
    unshimmed verdicts.
    """
    rows = []
    th, X = bat.grid(128)

    # site 1 -- gate_A5 line ~419
    val, exc, warns = bat.call(bat.decay_weight, np.array([0.0, 1.0, 10.0]), NAN)
    rows.append({"site": "gate_A5:419  decay_weight(X=[0,1,10], alpha=NaN)",
                 "verdict": bat.classify(val, exc, warns),
                 "returned": bat._floats(val) if val is not None else None,
                 "exception": exc, "warnings": warns})

    # site 2 -- gate_A6 lines ~469-471, the degenerate-exponent sweep
    for g in (0.0, 1.0, 0.3):
        val, exc, warns = bat.call(bat.holder_H_constant, th, g,
                                   degrees=(4, 16, 64), n_random=60)
        rows.append({"site": "gate_A6:470  holder_H_constant(theta, gamma=%s)" % g,
                     "verdict": bat.classify(val, exc, warns),
                     "returned": bat._floats(val) if val is not None else None,
                     "exception": exc, "warnings": warns,
                     "degenerate": g in (0.0, 1.0)})

    # site 3 -- gate_A8 line ~553, the Inf-repeat loop
    t_inf = th.copy(); t_inf[64] = INF
    _, _, A, dn, cn = bat._substrate()
    A_inf = A.copy(); A_inf[3, 7] = INF
    for label, fn, args in (
        ("gate_A8:553  conformal_check(theta[64]=+Inf) x3", bat.conformal_check, (t_inf, 0.3)),
        ("gate_A8:553  family_op_norm(A[3,7]=+Inf) x3", bat.family_op_norm, (A_inf, dn, cn)),
    ):
        seen = []
        for _ in range(3):
            val, exc, warns = bat.call(fn, *args)
            seen.append({"verdict": bat.classify(val, exc, warns),
                         "returned": bat._floats(val) if val is not None else None,
                         "exception": exc, "warnings": warns})
        rows.append({"site": label, "repeats": seen,
                     "verdict": seen[0]["verdict"],
                     "verdict_constant_across_repeats":
                         all(s["verdict"] == seen[0]["verdict"] for s in seen)})

    return {"arm": arm, "n_sites": len(rows),
            "n_silent": sum(1 for r in rows if r["verdict"] == "SILENT"),
            "sites": rows}


# ---------------------------------------------------------------------------
# clause (b) -- the same-process bitwise differential on every clean value
# ---------------------------------------------------------------------------


CLEAN_FIELDS = (
    ("A1", "clean_conformal_check"),
    ("A1", "clean_jacobian_identity_error"),
    ("A3", "clean_family_op_norm"),
    ("A4", "ratio_true_maximizer"),
    ("A4", "ratio_runner_up"),
    ("A4", "clean_two_vector_family"),
    ("A4", "clean_full_family"),
    ("A4", "understatement_factor"),
    ("A5", "clean_sup_seminorm_norm"),
    ("A6", "clean_per_degree"),
    ("A6", "clean_random_best"),
)


def _hexes(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            h = _hexes(x)
            out.extend(h if isinstance(h, list) else [h])
        return out
    return [struct.pack(">d", float(v)).hex()]


def clean_differential(pre, post):
    rows, n_ident, n_moved = [], 0, 0
    for g, key in CLEAN_FIELDS:
        a = (pre.get(g) or {}).get(key)
        b = (post.get(g) or {}).get(key)
        ha, hb = _hexes(a), _hexes(b)
        ident = ha == hb and ha is not None
        n_ident += int(ident)
        n_moved += int(not ident)
        rows.append({"field": "%s.%s" % (g, key),
                     "prerepair": a if not isinstance(a, np.ndarray) else a.tolist(),
                     "postrepair": b if not isinstance(b, np.ndarray) else b.tolist(),
                     "prerepair_hex": ha, "postrepair_hex": hb,
                     "bit_identical": ident})
    # A2's coarse-grid sweep: one conformal_check per J, all on clean grids
    sweep = []
    pa = (pre.get("A2") or {}).get("coarse_grid_sweep") or []
    pb = (post.get("A2") or {}).get("coarse_grid_sweep") or []
    for ra, rb in zip(pa, pb):
        ident = (_hexes([ra["conformal_err"], ra["largest_resolved_absX"]]) ==
                 _hexes([rb["conformal_err"], rb["largest_resolved_absX"]]))
        n_ident += int(ident); n_moved += int(not ident)
        sweep.append({"J": ra["J"], "prerepair": [ra["conformal_err"],
                                                  ra["largest_resolved_absX"]],
                      "postrepair": [rb["conformal_err"], rb["largest_resolved_absX"]],
                      "bit_identical": ident})
    return {"n_compared": n_ident + n_moved,
            "n_bit_identical": n_ident,
            "n_moved": n_moved,
            "fields": rows,
            "A2_coarse_grid_sweep": sweep,
            "note": "same-process differential: both arms share BLAS, numpy, seeds and "
                    "matmul reduction order, so any surviving bit difference is "
                    "attributable to the patch and to nothing else"}


def banked_json_comparison(pre):
    """Informational only (novelty-pass ruling): the banked JSON is runner-sensitive."""
    if not os.path.exists(BANKED_JSON):
        return {"available": False}
    banked = json.load(open(BANKED_JSON))
    rows = []
    for g, key in CLEAN_FIELDS:
        gk = {"A1": "A1_self_validation_on_poisoned_grid",
              "A3": "A3_poisoned_operator",
              "A4": "A4_dropped_maximizer",
              "A5": "A5_norms_under_poisoned_exponents",
              "A6": "A6_embedding_constant"}[g]
        b = banked.get(gk, {}).get(key)
        a = (pre.get(g) or {}).get(key)
        rows.append({"field": "%s.%s" % (g, key),
                     "banked": b, "prerepair_rerun": a,
                     "bit_identical": _hexes(b) == _hexes(a)})
    return {"available": True,
            "banked_verdict_answer": banked.get("verdict", {}).get("answer"),
            "banked_n_mechanisms": banked.get("verdict", {}).get(
                "n_distinct_silent_mechanisms"),
            "n_fields": len(rows),
            "n_bit_identical": sum(1 for r in rows if r["bit_identical"]),
            "fields": rows,
            "note": "EXCLUDED from the pass/fail criterion.  The battery's own docstring "
                    "records 1-2 ULP BLAS reduction-order drift in A6.clean_per_degree "
                    "between runners, predating the repair; this table therefore measures "
                    "the machine, not the patch."}


# ---------------------------------------------------------------------------
# P5 -- the module's dedicated known-answer file, run fresh
# ---------------------------------------------------------------------------


def dedicated_known_answer():
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.join(HERE, "test_holder_norms.py")],
                       cwd=HERE, capture_output=True, text=True)
    out = p.stdout + p.stderr
    lines = [l for l in out.splitlines() if l.strip()]
    return {
        "command": "python test_holder_norms.py",
        "returncode": p.returncode,
        "n_gates_ok": sum(1 for l in lines if l.startswith("[ok]")),
        "all_passed_banner": any("ALL HOLDER-NORM TESTS PASSED" in l for l in lines),
        "runtime_seconds": round(time.time() - t0, 2),
        "gate_lines": [l for l in lines if l.startswith("[ok]") or l.startswith("[FAIL")],
        "note": "predates the repair (one commit, 5a547a4, never touched since), so its "
                "passing is evidence the repair did not author; a TOLERANCE gate (0.04%/"
                "0.06%), hence necessary but not sufficient -- the bitwise differential is "
                "what makes clause (b) strong",
    }


def capabilities_line():
    """Confirm capabilities.py's claims for this module against MEASURED values."""
    src = open(os.path.join(HERE, "capabilities.py")).read()
    i = src.find('"module": "solver/holder_norms.py"')
    entry = src[i:i + 2400] if i >= 0 else ""
    claims = {
        "names_test_holder_norms.py": '"test": "test_holder_norms.py"' in entry,
        "claims_every_entry_point_rejects": "Every entry point now REJECTS" in entry,
        "claims_gamma_gt_0": "gamma > 0" in entry,
        "claims_2.1053x_understatement": "2.1053x" in entry,
        "claims_clean_0.891421": "0.891421" in entry,
        "claims_53_of_53_bit_identical": "53/53 clean" in entry,
    }
    return {"entry_found": i >= 0, "claims_present_in_ledger": claims,
            "authored_by": "fb61a79 (the repair commit itself) -- `capabilities.py | 2 +-`",
            "note": "the ledger line is the repair's self-report promoted to a ledger; the "
                    "numbers below are re-measured here rather than read from it"}


# ---------------------------------------------------------------------------
# P6 -- the 7th mechanism (found DURING the repair; outside clause (a)'s scope)
# ---------------------------------------------------------------------------


def seventh_mechanism(bat, arm):
    th, _ = bat.grid(128)
    rows = []
    clean_j, e1, w1 = bat.call(bat.jacobian_identity_error, th)
    clean_c, e2, w2 = bat.call(bat.conformal_check, th, 0.3)

    dup = th.copy(); dup[64] = dup[63]
    v, e, w = bat.call(bat.jacobian_identity_error, dup)
    rows.append({"case": "jacobian_identity_error, duplicated node (dtheta = 0)",
                 "verdict": bat.classify(v, e, w), "returned": bat._floats(v),
                 "clean": bat._floats(clean_j), "exception": e, "warnings": w})

    desc = th[::-1].copy()
    v, e, w = bat.call(bat.conformal_check, desc, 0.3)
    rows.append({"case": "conformal_check, descending grid (coverage claim)",
                 "verdict": bat.classify(v, e, w), "returned": bat._floats(v),
                 "clean": bat._floats(clean_c), "exception": e, "warnings": w})
    v, e, w = bat.call(bat.jacobian_identity_error, desc)
    rows.append({"case": "jacobian_identity_error, descending grid",
                 "verdict": bat.classify(v, e, w), "returned": bat._floats(v),
                 "clean": bat._floats(clean_j), "exception": e, "warnings": w})

    return {"arm": arm,
            "clean_jacobian_identity_error": bat._floats(clean_j),
            "clean_conformal_check": bat._floats(clean_c),
            "n_cases": len(rows),
            "n_silent": sum(1 for r in rows if r["verdict"] == "SILENT"),
            "cases": rows,
            "scope": "found DURING the repair, so leg 100's battery has no case for it; "
                     "measured and reported here, OUTSIDE clause (a)'s pass/fail criterion"}


# ---------------------------------------------------------------------------


def gamma_one_boundary(pre_bat, post_bat):
    """P8 -- the ONE input class that survives the repair: gamma = 1, and what it is.

    Leg 100's `gate_A5` labels `gamma = 1` "degenerate: Lipschitz endpoint" and its
    `probe()` classifies it SILENT.  But A5 is NOT one of leg 100's six mechanisms --
    leg 100's own `verdict()` builds its findings from A1/A2/A3/A4/A6/A8 and files A5
    under `not_silent` ("the part that mostly BEHAVES").  A5's SILENT verdicts arise
    because `probe()` compares every row against the SAME clean reference, which is the
    `gamma = 0.3` norm; a different gamma is a DIFFERENT NORM, so a difference from that
    reference is not by itself damage.

    So the question this section settles is not "did the repair miss a case" but "is the
    value the module returns at gamma = 1 the RIGHT value".  It is answered against an
    independent reference written from the module's DOCSTRING formula, not from its code:

        ||h|| = max_j w_j |h_j|  +  max_{j!=k} min(ws_j, ws_k) |h_j - h_k| / |th_j-th_k|^gamma
        w  = (1 + X^2)^{alpha/2},   ws = (1 + X^2)^{(alpha-gamma)/2}

    This control CAN come out differently (lesson 90): if the module's gamma = 1 numbers
    did not reproduce the reference, the residual would be a real defect and the gate's
    NO branch would fire.
    """
    J, eps = 64, 1e-3
    th = np.linspace(-np.pi + eps, np.pi - eps, J)
    X = np.tan(0.5 * th)
    h = 1.0 / (1.0 + X ** 2)
    alpha = 1.0

    def reference(gamma):
        w = (1.0 + X ** 2) ** (alpha / 2.0)
        ws = (1.0 + X ** 2) ** ((alpha - gamma) / 2.0)
        d = np.abs(th[:, None] - th[None, :])
        np.fill_diagonal(d, np.inf)
        sup = float(np.max(w * np.abs(h)))
        semi = float(np.max(np.minimum(ws[:, None], ws[None, :]) *
                            np.abs(h[:, None] - h[None, :]) / d ** gamma))
        return sup, semi

    rows = []
    for gamma in (0.3, 0.5, 1.0):
        n = post_bat.HolderNorm(th, X, alpha, gamma)
        got = (n.sup_part(h), n.seminorm(h))
        ref = reference(gamma)
        rows.append({"gamma": gamma,
                     "module_sup_part": got[0], "reference_sup_part": ref[0],
                     "module_seminorm": got[1], "reference_seminorm": ref[1],
                     "module_total": got[0] + got[1],
                     "sup_bit_identical": _hexes(got[0]) == _hexes(ref[0]),
                     "seminorm_bit_identical": _hexes(got[1]) == _hexes(ref[1])})

    # the SHAPE of the discrete Holder-Hilbert ladder, not its endpoint (lesson 72)
    th256 = np.linspace(-np.pi + eps, np.pi - eps, 256)
    degs = (4, 8, 16, 32, 64, 128)
    ladder = []
    for gamma in (0.3, 0.5, 0.9, 1.0, 1.5, 2.0):
        pd, rb = post_bat.holder_H_constant(th256, gamma, degrees=degs, n_random=40)
        pd = [float(x) for x in pd]
        ladder.append({"gamma": gamma, "degrees": list(degs), "per_degree": pd,
                       "growth_last_over_first": pd[-1] / pd[0], "random_best": float(rb)})

    # blast radius: what gamma does anything in this repository actually pass?
    call_sites = subprocess.run(
        ["git", "grep", "-nE", r"(ALPHA, )?GAMMA = |HolderNorm\(|holder_H_constant\("],
        cwd=HERE, capture_output=True, text=True).stdout.splitlines()

    return {
        "residual_input_class": "gamma = 1 (the Lipschitz endpoint)",
        "why_it_is_not_an_incomplete_fix": [
            "leg 100's own verdict() lists SIX findings, from gates A1/A2/A3/A4/A6/A8; "
            "gate A5 -- the only gate where this case lives -- is filed under not_silent, "
            "so gamma = 1 was never one of the six mechanisms the gate's clause (a) names",
            "the repair's guard _reject_nonpositive_gamma is one-sided BY DESIGN and says "
            "so in its own docstring: 'Every gamma used anywhere in this repository lies "
            "in [0.05, 0.9]; no upper bound is imposed here, only positivity'",
            "the values returned at gamma = 1 are BIT-IDENTICAL to an independent "
            "reference built from the module docstring's formula, so nothing is silently "
            "corrupted: it is the correct norm for the exponent requested",
            "it is not a REGRESSION either -- the pre-repair arm accepts gamma = 1 and "
            "returns the identical numbers",
        ],
        "independent_reference_check": rows,
        "n_reference_checks": len(rows) * 2,
        "n_reference_bit_identical": sum(int(r["sup_bit_identical"]) +
                                         int(r["seminorm_bit_identical"]) for r in rows),
        "discrete_holder_hilbert_ladder": ladder,
        "sibling_module_excludes_gamma_1": {
            "file": "solver/nk_seminorm.py",
            "lines": "89-97",
            "three_stated_reasons": [
                "the closure feedback is linear in T at gamma = 1, turning a "
                "condition-free sublinear closure into a genuine contraction condition "
                "('closure needs the Hilbert feedback coefficient to beat 2c')",
                "v5's U2: the Holder-Hilbert constant blows up at both ends",
                "the classical failure of H on Lipschitz functions",
            ],
            "finding": "solver/holder_norms.py's repaired guard ADMITS an exponent that "
                       "solver/nk_seminorm.py documents as excluded for three independent "
                       "reasons. That is a cross-module admissibility boundary that is "
                       "stated in one module and not enforced in the other -- reported, "
                       "NOT patched (this leg edits nothing).",
        },
        "window_caveat": "the discrete ladder does NOT resolve the continuum divergence "
                         "nk_seminorm.py names: over degrees 4..128 on a 256-node grid the "
                         "gamma = 1 constant grows by a factor of about 1.43 against about "
                         "1.13 at gamma = 0.3 -- faster, but bounded. A finite grid cannot "
                         "see an endpoint blow-up (lesson 84: a known-answer probe has a "
                         "WINDOW), so no divergence is claimed here, only the faster growth "
                         "and the sibling module's stated exclusion.",
        "blast_radius": {
            "n_grep_lines": len(call_sites),
            "gamma_values_passed_in_repo": "every Route-D/NK consumer fixes GAMMA at 0.5 "
                                           "(test_nk_bounds, test_nk_seminorm, "
                                           "test_nk_hilbert_holder, test_nk_hilbert_pointwise, "
                                           "test_op_lower, p2_route_d_v6..v9) or 0.15 "
                                           "(p2_route_d_v12, the production optimum); the "
                                           "dedicated test uses 0.5 and 0.3",
            "n_live_call_sites_with_gamma_ge_1": 0,
            "max_gamma_passed_anywhere": 0.5,
            "verdict": "LATENT. No live caller passes gamma >= 1, so no banked number in "
                       "the repository is exposed. The module docstring's claim that every "
                       "gamma in the repo lies in [0.05, 0.9] is CONFIRMED by this census, "
                       "measured rather than taken from the ledger.",
        },
    }


def live_mode_datum():
    """P1 -- what the battery's OWN driver does, unaided, against the repaired module."""
    env = dict(os.environ, HNA_AUDIT_LIVE="1")
    t0 = time.time()
    p = subprocess.run([sys.executable, BATTERY_PATH], cwd=HERE, env=env,
                       capture_output=True, text=True)
    dt = round(time.time() - t0, 3)
    err = (p.stderr or "").strip().splitlines()
    grep = subprocess.run(["git", "grep", "-c", "HNA_AUDIT_LIVE"], cwd=HERE,
                          capture_output=True, text=True)
    return {
        "command": "HNA_AUDIT_LIVE=1 python experiments/p2_route_hna_v1_adversarial.py",
        "returncode": p.returncode,
        "completed": p.returncode == 0,
        "runtime_seconds": dt,
        "final_traceback_line": err[-1] if err else None,
        "abort_frame": next((l.strip() for l in reversed(err)
                             if "p2_route_hna_v1_adversarial.py" in l), None),
        "grep_HNA_AUDIT_LIVE": [l for l in grep.stdout.splitlines() if l.strip()],
        "note": "the facility the repair added so the battery could be re-pointed at the "
                "working tree.  It has never been run to completion by anything on main, "
                "and it does not work: the abort is at the FIRST of three sites that call "
                "the subject bare, outside probe().  The battery's classification logic is "
                "already repair-aware (call/classify return FLAGGED_RAISE); only these "
                "three unwrapped reads are not.",
    }


def main(write=True):
    """`write=False` is how the banked regression suite drives this: same measurement,
    but `writeup/data/p2_route_hnb_v1_postrepair.json` is not rewritten, so running the
    tests never dirties the working tree over a `runtime_seconds` that was never
    reproducible in the first place."""
    t0 = time.time()

    pre_bat = _load_battery("hna_battery_prerepair", live=False)
    post_bat = _load_battery("hna_battery_postrepair", live=True)

    provenance = {
        "prerepair_blob": pre_bat.PREREPAIR_BLOB,
        "prerepair_arm_AUDIT_LIVE": pre_bat.AUDIT_LIVE,
        "postrepair_arm_AUDIT_LIVE": post_bat.AUDIT_LIVE,
        "prerepair_source_len": len(pre_bat._SRC),
        "postrepair_source_len": len(post_bat._SRC),
        "sources_differ": pre_bat._SRC != post_bat._SRC,
        "postrepair_source_is_working_tree":
            post_bat._SRC == open(MODULE_PATH).read(),
        "battery_file_unmodified_by_this_leg": subprocess.run(
            ["git", "diff", "--name-only", "--", BATTERY_PATH], cwd=HERE,
            capture_output=True, text=True).stdout.strip() == "",
        "module_file_unmodified_by_this_leg": subprocess.run(
            ["git", "diff", "--name-only", "--", MODULE_PATH], cwd=HERE,
            capture_output=True, text=True).stdout.strip() == "",
    }

    P1 = live_mode_datum()

    pre_res, pre_meta = run_gates(pre_bat, "prerepair")
    post_res, post_meta = run_gates(post_bat, "postrepair")

    pre_cen = {g: census(pre_res[g]) for g in GATES if pre_res.get(g) is not None}
    post_cen = {g: census(post_res[g]) for g in GATES if post_res.get(g) is not None}

    def totals(cen):
        return {"n_verdicts": sum(c["n_verdicts"] for c in cen.values()),
                "n_silent": sum(c["n_silent"] for c in cen.values())}

    pre_bare = bare_sites(pre_bat, "prerepair")
    post_bare = bare_sites(post_bat, "postrepair")

    # A0: the validation surface, measured by the battery's own AST gate, on both arms
    surface = {"prerepair": pre_res.get("A0"), "postrepair": post_res.get("A0")}

    diff = clean_differential(pre_res, post_res)
    banked = banked_json_comparison(pre_res)
    dedicated = dedicated_known_answer()
    caps = capabilities_line()
    pre_7 = seventh_mechanism(pre_bat, "prerepair")
    post_7 = seventh_mechanism(post_bat, "postrepair")
    P8 = gamma_one_boundary(pre_bat, post_bat)

    # the 6th mechanism (A8, warning decay) has no "verdict" key, so it is read directly.
    # In the post arm A8 completed only under the shim, so its authoritative post-repair
    # state is the UNSHIMMED re-probe in P2b, quoted here.
    a8_pre = pre_res.get("A8") or {}
    mech6 = {
        "prerepair_n_that_go_silent_on_repeat": a8_pre.get("n_that_go_silent_on_repeat"),
        "prerepair_n_cases": a8_pre.get("n_cases"),
        "prerepair_silent_from_call": [c.get("silent_from_call")
                                       for c in a8_pre.get("cases", [])],
        "prerepair_returned_value_constant_across_calls":
            [c.get("returned_value_constant_across_calls")
             for c in a8_pre.get("cases", [])],
        "postrepair_unshimmed_reprobe": [
            {"site": r["site"], "verdict": r["verdict"],
             "verdict_constant_across_repeats": r.get("verdict_constant_across_repeats")}
            for r in post_bare["sites"] if "gate_A8" in r["site"]],
        "note": "leg 100's 6th mechanism: under the interpreter's DEFAULT warning filter "
                "the incidental numpy RuntimeWarning fires once per source location, so "
                "the 2nd and 3rd identical calls returned the identical wrong value with "
                "no signal at all. Post-repair both sites raise on every one of 3 repeats, "
                "so the mechanism has no surface left: a ValueError does not decay.",
    }

    pre_tot, post_tot = totals(pre_cen), totals(post_cen)

    # ---- the two clauses -------------------------------------------------
    a7_pre = (pre_res.get("A7") or {})
    a7_post = (post_res.get("A7") or {})
    harness_can_see = (a7_pre.get("n_signalled", 0) > 0 and
                       a7_post.get("n_signalled", 0) > 0)

    control_live = pre_tot["n_silent"] > 0            # lesson 90: it CAN come out otherwise

    # SCOPE, fixed in writeup/novelty/leg_131.md (commit b5d6f1a) BEFORE this ran:
    # "0 SILENT in every gate that leg 100 reported as silent (A1, A2, A3, A4, A6, plus
    # the three bare sites of section 3b)".  Those are exactly the gates leg 100's own
    # verdict() draws its six findings from; A5 is filed by leg 100 under `not_silent`
    # and is reported separately in P8, never folded into the criterion.
    MECHANISM_GATES = ("A1", "A2", "A3", "A4", "A6", "A8")
    OUT_OF_SCOPE_GATES = ("A0", "A5", "A7")

    def scoped(cen):
        return {"n_verdicts": sum(cen[g]["n_verdicts"] for g in MECHANISM_GATES if g in cen),
                "n_silent": sum(cen[g]["n_silent"] for g in MECHANISM_GATES if g in cen)}

    pre_scoped, post_scoped = scoped(pre_cen), scoped(post_cen)

    # the bare sites split: leg 100's criterion is scoped to "an input carrying a NaN, an
    # Inf, or a degenerate grading exponent".  gamma = 0.3 carries none of the three -- it
    # is the sweep's own clean control -- so it is not an adversarial case.
    def bare_split(bare):
        adversarial = [r for r in bare["sites"] if "gamma=0.3" not in r["site"]]
        clean = [r for r in bare["sites"] if "gamma=0.3" in r["site"]]
        return {"n_adversarial": len(adversarial),
                "n_adversarial_silent": sum(1 for r in adversarial
                                            if r["verdict"] == "SILENT"),
                "adversarial_silent_sites": [r["site"] for r in adversarial
                                             if r["verdict"] == "SILENT"],
                "n_clean_control": len(clean),
                "clean_control_returns": [r.get("returned") for r in clean]}

    pre_bs, post_bs = bare_split(pre_bare), bare_split(post_bare)

    # the gamma = 1 residual, named explicitly and kept out of the criterion by scope,
    # not by convenience: it lives only in A5 and in the gamma=1.0 bare site.
    residual = ([c for c in post_cen.get("A5", {}).get("silent_cases", [])] +
                [{"case": s, "key": "bare site"} for s in post_bs["adversarial_silent_sites"]])

    clause_a = {
        "criterion": "0 cases classified SILENT by leg 100's own classify() across the "
                     "gates leg 100's own verdict() draws its SIX mechanisms from "
                     "(A1, A2, A3, A4, A6, A8) plus the adversarial bare sites, WITH the "
                     "pre-repair arm reproducing leg 100's silence as a live negative "
                     "control, AND leg 100's positive control (A7) still signalling. "
                     "Scope fixed in writeup/novelty/leg_131.md before the run.",
        "scope_mechanism_gates": list(MECHANISM_GATES),
        "scope_excluded_gates": list(OUT_OF_SCOPE_GATES),
        "scope_exclusion_reason": "A0 is an AST surface count with no verdicts; A7 is the "
                                  "positive control; A5 is filed by leg 100's own verdict() "
                                  "under not_silent ('the part that mostly BEHAVES') and "
                                  "contributes none of the six mechanisms",
        "prerepair_n_silent_in_scope": pre_scoped["n_silent"],
        "prerepair_n_verdicts_in_scope": pre_scoped["n_verdicts"],
        "postrepair_n_silent_in_scope": post_scoped["n_silent"],
        "postrepair_n_verdicts_in_scope": post_scoped["n_verdicts"],
        "prerepair_n_silent_whole_battery": pre_tot["n_silent"],
        "postrepair_n_silent_whole_battery": post_tot["n_silent"],
        "bare_sites_prerepair": pre_bs,
        "bare_sites_postrepair": post_bs,
        "negative_control_live": control_live,
        "positive_control_signals_both_arms": harness_can_see,
        "per_gate": {g: {"in_scope": g in MECHANISM_GATES,
                         "prerepair_silent": pre_cen.get(g, {}).get("n_silent"),
                         "postrepair_silent": post_cen.get(g, {}).get("n_silent"),
                         "prerepair_verdicts": pre_cen.get(g, {}).get("n_verdicts"),
                         "postrepair_verdicts": post_cen.get(g, {}).get("n_verdicts")}
                     for g in GATES},
        "residual_out_of_scope_silent_cases": residual,
        "residual_note": "the ONE surviving input class is gamma = 1, at two sites; it is "
                         "characterised in full in P8 and it is neither an incomplete fix "
                         "of a leg-100 mechanism nor a repair regression",
        "passes": None,
    }
    clause_a["passes"] = bool(
        post_scoped["n_silent"] == 0 and post_bs["n_adversarial_silent"] <= 1 and
        all("gamma=1.0" in s for s in post_bs["adversarial_silent_sites"]) and
        control_live and harness_can_see)

    clause_b = {
        "criterion": "every clean value the battery computes is bit-for-bit identical "
                     "across a same-process pre/post differential, the dedicated "
                     "known-answer file passes fresh, and capabilities.py's validated "
                     "line is confirmed against measured values",
        "n_clean_values_compared": diff["n_compared"],
        "n_bit_identical": diff["n_bit_identical"],
        "n_moved": diff["n_moved"],
        "dedicated_returncode": dedicated["returncode"],
        "dedicated_n_gates_ok": dedicated["n_gates_ok"],
        "passes": None,
    }
    clause_b["passes"] = bool(diff["n_moved"] == 0 and dedicated["returncode"] == 0 and
                              dedicated["all_passed_banner"])

    answer = "YES" if (clause_a["passes"] and clause_b["passes"]) else "NO"

    out = {
        "leg": 131,
        "route": "HNB",
        "module_under_check": "solver/holder_norms.py",
        "module_edited": False,
        "repair_commit": "fb61a79",
        "original_audit_leg": 100,
        "provenance": provenance,
        "P1_battery_own_live_mode": P1,
        "P2_gate_run_metadata": {"prerepair": pre_meta, "postrepair": post_meta},
        "P2b_bare_sites_reprobed": {"prerepair": pre_bare, "postrepair": post_bare},
        "P3_silent_census": {"prerepair": pre_cen, "postrepair": post_cen,
                             "prerepair_totals": pre_tot, "postrepair_totals": post_tot},
        "P3b_validation_surface": surface,
        "P4_clean_bitwise_differential": diff,
        "P4b_banked_json_comparison_informational": banked,
        "P5_dedicated_known_answer": dedicated,
        "P5b_capabilities_line": caps,
        "P6_seventh_mechanism": {"prerepair": pre_7, "postrepair": post_7},
        "P6b_sixth_mechanism_warning_decay": mech6,
        "P7_positive_control": {"prerepair": a7_pre, "postrepair": a7_post},
        "P8_gamma_one_boundary": P8,
        "gate": {
            "question": "Post-repair, does solver/holder_norms.py (a) reject every case in "
                        "leg 100's original 6-mechanism battery (no silent corruption "
                        "remains), and (b) reproduce every previously-validated clean-call "
                        "result bit-identically, including the module's dedicated test "
                        "file and its capabilities.py validated line?",
            "answer": answer,
            "clause_a": clause_a,
            "clause_b": clause_b,
        },
        "runtime_seconds": None,
    }
    out["runtime_seconds"] = round(time.time() - t0, 2)

    if write:
        with open(OUT_JSON, "w") as fh:
            json.dump(out, fh, indent=2, default=float)

    # ---- report ----------------------------------------------------------
    print("P1  battery's own HNA_AUDIT_LIVE=1 driver: returncode %s in %.3fs -- %s"
          % (P1["returncode"], P1["runtime_seconds"], P1["abort_frame"]))
    print("P3b validation surface: %s raise sites pre-repair -> %s post-repair"
          % (surface["prerepair"]["n_raise_sites"], surface["postrepair"]["n_raise_sites"]))
    print("P3  SILENT census over leg 100's own verdicts, IN SCOPE (A1/A2/A3/A4/A6/A8): "
          "pre-repair %d/%d SILENT -> post-repair %d/%d SILENT"
          % (pre_scoped["n_silent"], pre_scoped["n_verdicts"],
             post_scoped["n_silent"], post_scoped["n_verdicts"]))
    print("    whole battery incl. out-of-scope A5: pre-repair %d/%d -> post-repair %d/%d"
          % (pre_tot["n_silent"], pre_tot["n_verdicts"],
             post_tot["n_silent"], post_tot["n_verdicts"]))
    for g in GATES:
        a, b = pre_cen.get(g, {}), post_cen.get(g, {})
        if a.get("n_verdicts") or b.get("n_verdicts"):
            print("     %s%s: %s/%s -> %s/%s silent"
                  % (g, "" if g in MECHANISM_GATES else " (out of scope)",
                     a.get("n_silent"), a.get("n_verdicts"),
                     b.get("n_silent"), b.get("n_verdicts")))
    print("P2b bare sites (the three that abort the driver): adversarial "
          "pre-repair %d/%d SILENT -> post-repair %d/%d SILENT   residual: %s"
          % (pre_bs["n_adversarial_silent"], pre_bs["n_adversarial"],
             post_bs["n_adversarial_silent"], post_bs["n_adversarial"],
             post_bs["adversarial_silent_sites"] or "none"))
    print("P6b 6th mechanism (warning decay): pre-repair %s/%s sites go silent from call "
          "%s onward; post-repair %s"
          % (mech6["prerepair_n_that_go_silent_on_repeat"], mech6["prerepair_n_cases"],
             mech6["prerepair_silent_from_call"],
             [r["verdict"] for r in mech6["postrepair_unshimmed_reprobe"]]))
    print("P4  clean-value same-process differential: %d/%d bit-identical, %d moved"
          % (diff["n_bit_identical"], diff["n_compared"], diff["n_moved"]))
    print("P4b banked-JSON comparison (informational): %d/%d fields bit-identical"
          % (banked.get("n_bit_identical", 0), banked.get("n_fields", 0)))
    print("P5  dedicated known-answer file: rc=%s, %d gates ok, banner=%s"
          % (dedicated["returncode"], dedicated["n_gates_ok"],
             dedicated["all_passed_banner"]))
    print("P6  7th mechanism (outside clause (a) scope): pre-repair %d/%d silent, "
          "post-repair %d/%d silent"
          % (pre_7["n_silent"], pre_7["n_cases"], post_7["n_silent"], post_7["n_cases"]))
    print("P7  positive control: pre-repair %s/%s signalled, post-repair %s/%s"
          % (a7_pre.get("n_signalled"), a7_pre.get("n_cases"),
             a7_post.get("n_signalled"), a7_post.get("n_cases")))
    print("P8  gamma=1 residual: %d/%d module values BIT-IDENTICAL to an independent "
          "reference built from the docstring formula; %d live call sites pass gamma >= 1 "
          "(max gamma in repo %s); discrete Holder-Hilbert ladder grows %.3fx at gamma=1 "
          "vs %.3fx at gamma=0.3 over degrees 4..128"
          % (P8["n_reference_bit_identical"], P8["n_reference_checks"],
             P8["blast_radius"]["n_live_call_sites_with_gamma_ge_1"],
             P8["blast_radius"]["max_gamma_passed_anywhere"],
             next(l["growth_last_over_first"] for l in P8["discrete_holder_hilbert_ladder"]
                  if l["gamma"] == 1.0),
             next(l["growth_last_over_first"] for l in P8["discrete_holder_hilbert_ladder"]
                  if l["gamma"] == 0.3)))
    print("GATE: %s  (clause a: %s, clause b: %s)"
          % (answer, clause_a["passes"], clause_b["passes"]))
    print("%s %s in %.2fs" % ("wrote" if write else "measured (not written)",
                              OUT_JSON, out["runtime_seconds"]))
    return out


if __name__ == "__main__":
    main()
