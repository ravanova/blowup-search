"""Route-RSR v1 -- the REPAIR of `solver/rescaled_spectrum.py`'s convergence filter,
plus the explicit re-confirmation of every Route-E / Route-G banked row.

Leg 225.  Repairs leg 203's finding R1: `converged_spectrum` had no guard on
`K_fine` vs `K_coarse`, so at `K_fine == K_coarse` the filter compared a spectrum
with ITSELF, every match distance was identically 0.0, and the whole discretized
continuum was certified as "the grid-independent part of the spectrum" -- n_kept
2 -> K (24x at K = 48), including a spurious +-40.4623i pair.

THE INSTRUMENT.  Both module versions are loaded into the SAME process:

  * `RS_pre`  -- the pre-repair source, read out of git at the merge base, so the
                 comparison is against the code as it actually stood, not against
                 a remembered number.
  * `RS_post` -- the working tree, repaired.

Every comparison is `==` on raw float64 (with an explicit NaN clause), not
`allclose`.  Same process means same BLAS, same threading, same libm -- so a
moved bit is a statement about the repair and not about the machine.  Comparison
against the BANKED JSON is reported separately and labelled as such, because the
bank was produced on another run and cross-run drift is a different quantity from
pre-vs-post drift.

THE GATE (pre-committed, DIRECTION.md leg 225, verbatim):

  Does fixing the `K_fine==K_coarse` degenerate comparison (per leg 203's own
  identified mechanism) cause every one of leg 203's adversarial cases to now
  correctly reject false convergence, AND does an explicit, fresh re-run of the
  5/7 Route-E and 7/7 Route-G banked rows confirm (a) their own independently-
  banked residuals are unchanged, and (b) their `converged=False` flag from the
  module's separate conservative check still holds post-repair (i.e. the repair
  doesn't silently relabel them `converged=True` for the wrong reason either)?

Batteries:
  B1  leg 203's S3 adversarial cases, pre vs post
  B2  R1's reachability path (R5: non-integer K floor-truncated into equality)
  B3  clean-input bit-identity on `converged_spectrum` -- the repair's licence
  B4  `on_no_refinement="allow"` reproduces the pre-repair path bit-for-bit
  B5  Route-E E5_sweep re-confirmation, all 7 rows, pre vs post vs banked
  B6  Route-G g4_cross_model re-confirmation, all 7 rows, pre vs post vs banked
  B7  the census of what this repair does NOT cover, measured not asserted

Run: .venv/bin/python experiments/p2_route_rsr_v1_repair.py [--quick]
"""

import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
import types
import warnings

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_rsr_v1_repair.json")
MODULE_PATH = "solver/rescaled_spectrum.py"

# The commit the repair is differenced against: this leg's merge base with main.
PRE_REPAIR_REF = "4f6cf4b1333974614255929be30f188c23abec39"


# --------------------------------------------------------------------------
# loading both module versions into one process
# --------------------------------------------------------------------------
def load_pre_repair(ref=PRE_REPAIR_REF, path=MODULE_PATH):
    """Exec the pre-repair source out of git as a private module object.

    `solver/rescaled_spectrum.py` imports only numpy (and, post-repair,
    warnings), so it can be exec'd standalone with no package plumbing.
    """
    src = subprocess.check_output(["git", "show", "%s:%s" % (ref, path)],
                                  cwd=ROOT).decode("utf-8")
    mod = types.ModuleType("rescaled_spectrum_pre")
    mod.__file__ = "<git:%s:%s>" % (ref[:7], path)
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, src


def load_post_repair(path=MODULE_PATH):
    full = os.path.join(ROOT, path)
    spec = importlib.util.spec_from_file_location("rescaled_spectrum_post", full)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(full) as fh:
        return mod, fh.read()


# --------------------------------------------------------------------------
# bit-level comparison
# --------------------------------------------------------------------------
def bits(x):
    """Raw float64 bit pattern, so NaN payloads and -0.0/+0.0 are distinguished."""
    return np.asarray(x, dtype=np.float64).view(np.uint64)


def same_bits(a, b):
    """True iff a and b are bit-identical as float64 arrays (NaN == NaN here)."""
    a = np.asarray(a)
    b = np.asarray(b)
    if a.shape != b.shape:
        return False
    if a.size == 0:
        return True
    if np.iscomplexobj(a) or np.iscomplexobj(b):
        a = np.asarray(a, dtype=np.complex128)
        b = np.asarray(b, dtype=np.complex128)
        return (np.array_equal(bits(a.real), bits(b.real))
                and np.array_equal(bits(a.imag), bits(b.imag)))
    return np.array_equal(bits(a), bits(b))


def ulps_apart(x, y):
    """Signed distance in ULPs between two float64 scalars (for reporting drift)."""
    if not (math.isfinite(x) and math.isfinite(y)):
        return None
    ax = int(np.float64(x).view(np.int64))
    ay = int(np.float64(y).view(np.int64))
    if ax < 0:
        ax = -(ax & 0x7FFFFFFFFFFFFFFF)
    if ay < 0:
        ay = -(ay & 0x7FFFFFFFFFFFFFFF)
    return ay - ax


def rel_diff(x, y):
    if x == y:
        return 0.0
    if not (math.isfinite(x) and math.isfinite(y)):
        return float("nan")
    d = abs(y - x)
    s = max(abs(x), abs(y))
    return d / s if s else d


def jc(z):
    """JSON-safe complex list."""
    return [[float(np.real(v)), float(np.imag(v))] for v in np.atleast_1d(z)]


def call_outcome(fn, *args, **kw):
    """Run fn, capturing either its return or the exception it raised."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            val = fn(*args, **kw)
            exc = None
        except Exception as ex:  # noqa: BLE001
            val = None
            exc = {"type": type(ex).__name__, "message": str(ex)[:400]}
    return {"value": val, "exception": exc,
            "warnings": [str(w.message)[:300] for w in caught]}


def summarize_cs(res):
    """The reportable content of a converged_spectrum result dict."""
    if res is None:
        return None
    kept = np.asarray(res["kept"])
    return {
        "n_total": int(res["n_total"]),
        "n_kept": int(res["n_kept"]),
        "max_match_distance": (float(np.max(res["dist"]))
                               if np.asarray(res["dist"]).size else None),
        "max_abs_imag_kept": (float(np.max(np.abs(np.imag(kept))))
                              if kept.size else 0.0),
        "residual_coarse": float(res["residual_coarse"]),
        "residual_fine": float(res["residual_fine"]),
        "c_omega_coarse": float(res["c_omega_coarse"]),
        "c_omega_fine": float(res["c_omega_fine"]),
        "kept_head": jc(kept[:6]) if kept.size else [],
    }


# ==========================================================================
# B1 -- leg 203's S3 adversarial cases, pre vs post
# ==========================================================================
S3_CASES = [
    (24, 36, "genuine refinement"),
    (24, 24, "DEGENERATE: self-comparison"),
    (24, 12, "coarser 'refinement'"),
    (32, 48, "genuine refinement"),
    (32, 32, "DEGENERATE: self-comparison"),
    (48, 72, "genuine refinement"),
    (48, 48, "DEGENERATE: self-comparison"),
]


def b1_adversarial(RS_pre, RS_post, a=0.0):
    print("\n[B1] leg 203's S3 adversarial cases, pre vs post")
    rows = []
    for Kc, Kf, label in S3_CASES:
        pre = call_outcome(RS_pre.converged_spectrum, a, K_coarse=Kc, K_fine=Kf,
                           tol=1e-3)
        post = call_outcome(RS_post.converged_spectrum, a, K_coarse=Kc, K_fine=Kf,
                            tol=1e-3)
        degenerate = Kf <= Kc
        row = {
            "K_coarse": Kc, "K_fine": Kf, "label": label,
            "refinement_happened": Kf > Kc,
            "equal_K": Kf == Kc,
            "pre": {"summary": summarize_cs(pre["value"]),
                    "exception": pre["exception"]},
            "post": {"summary": summarize_cs(post["value"]),
                     "exception": post["exception"]},
        }
        # The gate's question, per case: did false convergence get rejected?
        if degenerate:
            row["pre_certified_n_kept"] = (int(pre["value"]["n_kept"])
                                           if pre["value"] is not None else None)
            row["post_rejects"] = post["exception"] is not None
            row["post_exception_type"] = (post["exception"]["type"]
                                          if post["exception"] else None)
            row["inflation_factor_pre"] = (
                float(pre["value"]["n_kept"]) / 2.0
                if pre["value"] is not None else None)
        else:
            row["bit_identical"] = (
                pre["value"] is not None and post["value"] is not None
                and same_bits(pre["value"]["kept"], post["value"]["kept"])
                and same_bits(pre["value"]["dist"], post["value"]["dist"])
                and same_bits(pre["value"]["ev_coarse"], post["value"]["ev_coarse"])
                and same_bits(pre["value"]["ev_fine"], post["value"]["ev_fine"])
                and same_bits(pre["value"]["residual_coarse"],
                              post["value"]["residual_coarse"])
                and same_bits(pre["value"]["residual_fine"],
                              post["value"]["residual_fine"])
                and int(pre["value"]["n_kept"]) == int(post["value"]["n_kept"]))
        rows.append(row)
        if degenerate:
            print("   K=%d/%d %-28s pre n_kept=%s  post=%s"
                  % (Kc, Kf, label, row["pre_certified_n_kept"],
                     row["post_exception_type"] or "NO REJECTION"))
        else:
            print("   K=%d/%d %-28s n_kept=%d  bit-identical=%s"
                  % (Kc, Kf, label, post["value"]["n_kept"], row["bit_identical"]))

    degen = [r for r in rows if not r["refinement_happened"]]
    clean = [r for r in rows if r["refinement_happened"]]
    return {
        "rows": rows,
        "n_degenerate_cases": len(degen),
        "n_degenerate_rejected_post": sum(1 for r in degen if r["post_rejects"]),
        "n_clean_cases": len(clean),
        "n_clean_bit_identical": sum(1 for r in clean if r["bit_identical"]),
        "pre_n_kept_on_equal_K": [r["pre_certified_n_kept"] for r in degen
                                  if r["equal_K"]],
        "worst_pre_inflation": max((r["inflation_factor_pre"] or 0.0)
                                   for r in degen),
        "worst_spurious_imag_pre": max(
            (r["pre"]["summary"]["max_abs_imag_kept"] for r in degen
             if r["pre"]["summary"]), default=None),
    }


# ==========================================================================
# B2 -- R1's reachability path: non-integer K floor-truncated into equality
# ==========================================================================
def b2_reachability(RS_pre, RS_post, a=0.0):
    print("\n[B2] R5 reachability: non-integer K_fine truncating into equality")
    rows = []
    for Kc, Kf in [(24, 24.9), (24, 24.0), (32, 32.5)]:
        pre = call_outcome(RS_pre.converged_spectrum, a, K_coarse=Kc, K_fine=Kf,
                           tol=1e-3)
        post = call_outcome(RS_post.converged_spectrum, a, K_coarse=Kc, K_fine=Kf,
                            tol=1e-3)
        rows.append({
            "K_coarse": Kc, "K_fine": Kf,
            "K_fine_truncates_to": int(Kf),
            "pre_n_kept": (int(pre["value"]["n_kept"])
                           if pre["value"] is not None else None),
            "pre_exception": pre["exception"],
            "post_exception": post["exception"],
            "post_rejects": post["exception"] is not None,
        })
        print("   K=%s/%s -> int %d   pre n_kept=%s   post=%s"
              % (Kc, Kf, int(Kf), rows[-1]["pre_n_kept"],
                 (post["exception"] or {}).get("type", "NO REJECTION")))
    return {"rows": rows,
            "n_rejected_post": sum(1 for r in rows if r["post_rejects"]),
            "n_cases": len(rows)}


# ==========================================================================
# B3 -- clean-input bit-identity: the repair's licence
# ==========================================================================
def b3_clean_identity(RS_pre, RS_post, quick):
    print("\n[B3] clean-input bit-identity on converged_spectrum (the licence)")
    cases = [(0.0, 24, 36), (0.0, 32, 48), (0.0, 48, 72)]
    if not quick:
        # the one literal converged_spectrum call site in the repository
        cases.append((0.0, 96, 144))
    rows = []
    leaves_total = leaves_same = 0
    for a, Kc, Kf in cases:
        t0 = time.time()
        rp = RS_pre.converged_spectrum(a, K_coarse=Kc, K_fine=Kf, tol=1e-3)
        rq = RS_post.converged_spectrum(a, K_coarse=Kc, K_fine=Kf, tol=1e-3)
        fields = {}
        for key in ("kept", "dist", "ev_coarse", "ev_fine", "residual_coarse",
                    "residual_fine", "c_omega_coarse", "c_omega_fine"):
            ok = same_bits(rp[key], rq[key])
            n = int(np.asarray(rp[key]).size)
            fields[key] = {"leaves": n, "bit_identical": bool(ok)}
            leaves_total += n
            leaves_same += n if ok else 0
        rows.append({"a": a, "K_coarse": Kc, "K_fine": Kf,
                     "n_kept_pre": int(rp["n_kept"]),
                     "n_kept_post": int(rq["n_kept"]),
                     "fields": fields,
                     "all_bit_identical": all(f["bit_identical"]
                                              for f in fields.values()),
                     "seconds": time.time() - t0})
        print("   a=%.2f K=%d/%d  n_kept %d -> %d  all-bit-identical=%s (%.1fs)"
              % (a, Kc, Kf, rp["n_kept"], rq["n_kept"],
                 rows[-1]["all_bit_identical"], rows[-1]["seconds"]))
    return {"rows": rows, "leaves_compared": leaves_total,
            "leaves_bit_identical": leaves_same,
            "leaves_moved": leaves_total - leaves_same}


# ==========================================================================
# B4 -- the escape hatch reproduces the pre-repair path bit-for-bit
# ==========================================================================
def b4_escape_hatch(RS_pre, RS_post, a=0.0):
    print("\n[B4] on_no_refinement='allow' reproduces the pre-repair path")
    rows = []
    for Kc, Kf in [(24, 24), (32, 32), (48, 48), (24, 12)]:
        pre = RS_pre.converged_spectrum(a, K_coarse=Kc, K_fine=Kf, tol=1e-3)
        got = call_outcome(RS_post.converged_spectrum, a, K_coarse=Kc, K_fine=Kf,
                           tol=1e-3, on_no_refinement="allow")
        post = got["value"]
        ok = (post is not None
              and same_bits(pre["kept"], post["kept"])
              and same_bits(pre["dist"], post["dist"])
              and same_bits(pre["ev_coarse"], post["ev_coarse"])
              and same_bits(pre["ev_fine"], post["ev_fine"])
              and int(pre["n_kept"]) == int(post["n_kept"]))
        rows.append({"K_coarse": Kc, "K_fine": Kf,
                     "n_kept_pre": int(pre["n_kept"]),
                     "n_kept_allow": int(post["n_kept"]) if post else None,
                     "bit_identical": bool(ok),
                     "warned": len(got["warnings"]) > 0,
                     "warning": got["warnings"][0] if got["warnings"] else None})
        print("   K=%d/%d  n_kept %d -> %s  bit-identical=%s  warned=%s"
              % (Kc, Kf, pre["n_kept"], rows[-1]["n_kept_allow"], ok,
                 rows[-1]["warned"]))
    bad = call_outcome(RS_post.converged_spectrum, a, K_coarse=24, K_fine=24,
                       on_no_refinement="nonsense")
    return {"rows": rows,
            "n_bit_identical": sum(1 for r in rows if r["bit_identical"]),
            "n_warned": sum(1 for r in rows if r["warned"]),
            "n_cases": len(rows),
            "bad_option_rejected": bad["exception"] is not None,
            "bad_option_exception": bad["exception"]}


# ==========================================================================
# B5 -- Route-E E5_sweep re-confirmation
# ==========================================================================
E5_TOLS = (1e-4, 1e-3, 1e-2, 1e-1)


def e5_row(RS, a, K_coarse, K_fine, da=0.02):
    """Reproduce experiments/p2_route_e_v1_spectrum.py:e5_sweep for ONE a.

    Deliberately re-implemented against the same module entry points that file
    uses (spectrum + match_filter, lines 164-171) rather than converged_spectrum
    -- because that is what Route-E actually calls, and the point of this
    battery is to re-run what was banked, not something that resembles it.
    """
    ev_c, _, out_c = RS.spectrum(a, K_coarse, da=da)
    ev_f, _, out_f = RS.spectrum(a, K_fine, da=da)
    counts = {}
    for t in E5_TOLS:
        kept, _ = RS.match_filter(ev_c, ev_f, t)
        counts["%g" % t] = int(kept.size)
    kept_ref, dist_ref = RS.match_filter(ev_c, ev_f, 1e-2)
    return {
        "a": float(a),
        "counts": counts,
        "kept_ref": kept_ref,
        "n_unstable_converged": int(np.sum(np.real(kept_ref) > 1e-3)),
        "residual_coarse": out_c["residual"],
        "residual_fine": out_f["residual"],
        "converged_coarse": bool(out_c["converged"]),
        "converged_fine": bool(out_f["converged"]),
        "c_omega": out_f["c_omega"],
        "max_re_all_coarse": float(np.max(ev_c.real)),
    }


def b5_route_e(RS_pre, RS_post, banked, quick):
    print("\n[B5] Route-E E5_sweep re-confirmation, all 7 rows, pre vs post vs banked")
    bank = {round(r["a"], 6): r for r in banked["E5_sweep"]}
    a_values = sorted(bank)
    if quick:
        a_values = a_values[:2]
    rows = []
    for a in a_values:
        t0 = time.time()
        pre = e5_row(RS_pre, a, 96, 144)
        post = e5_row(RS_post, a, 96, 144)
        b = bank[a]
        r = {
            "a": a,
            "seconds": time.time() - t0,
            "banked_residual_coarse": b["residual_coarse"],
            "banked_residual_fine": b["residual_fine"],
            "banked_counts": b["counts"],
            "banked_n_unstable_converged": b["n_unstable_converged"],
            # --- the gate's clause (a): residuals ---
            "residual_coarse_pre": pre["residual_coarse"],
            "residual_coarse_post": post["residual_coarse"],
            "residual_fine_pre": pre["residual_fine"],
            "residual_fine_post": post["residual_fine"],
            "residual_coarse_bit_identical_pre_post":
                bool(same_bits(pre["residual_coarse"], post["residual_coarse"])),
            "residual_fine_bit_identical_pre_post":
                bool(same_bits(pre["residual_fine"], post["residual_fine"])),
            "residual_coarse_rel_diff_vs_banked":
                rel_diff(b["residual_coarse"], post["residual_coarse"]),
            "residual_fine_rel_diff_vs_banked":
                rel_diff(b["residual_fine"], post["residual_fine"]),
            "residual_coarse_ulps_vs_banked":
                ulps_apart(b["residual_coarse"], post["residual_coarse"]),
            "residual_fine_ulps_vs_banked":
                ulps_apart(b["residual_fine"], post["residual_fine"]),
            # --- the gate's clause (b): the converged flag ---
            "above_1e-8_banked": bool(max(b["residual_coarse"],
                                          b["residual_fine"]) > 1e-8),
            "converged_coarse_pre": pre["converged_coarse"],
            "converged_coarse_post": post["converged_coarse"],
            "converged_fine_pre": pre["converged_fine"],
            "converged_fine_post": post["converged_fine"],
            "flag_flipped_pre_to_post":
                bool(pre["converged_coarse"] != post["converged_coarse"]
                     or pre["converged_fine"] != post["converged_fine"]),
            # --- everything else Route-E banked ---
            "counts_pre": pre["counts"],
            "counts_post": post["counts"],
            "counts_match_banked": bool(post["counts"] == b["counts"]),
            "counts_bit_identical_pre_post": bool(pre["counts"] == post["counts"]),
            "n_unstable_pre": pre["n_unstable_converged"],
            "n_unstable_post": post["n_unstable_converged"],
            "n_unstable_matches_banked":
                bool(post["n_unstable_converged"] == b["n_unstable_converged"]),
            "kept_ref_bit_identical_pre_post":
                bool(same_bits(pre["kept_ref"], post["kept_ref"])),
            "kept_ref_post": jc(post["kept_ref"][:6]),
            "c_omega_pre": pre["c_omega"], "c_omega_post": post["c_omega"],
            "c_omega_bit_identical_pre_post":
                bool(same_bits(pre["c_omega"], post["c_omega"])),
        }
        rows.append(r)
        print("   a=%.2f  res_c %.6e (banked %.6e, %d ulp)  conv_c %s->%s  "
              "counts %s  (%.0fs)"
              % (a, r["residual_coarse_post"], r["banked_residual_coarse"],
                 r["residual_coarse_ulps_vs_banked"] or 0,
                 r["converged_coarse_pre"], r["converged_coarse_post"],
                 [r["counts_post"]["%g" % t] for t in E5_TOLS], r["seconds"]))
        sys.stdout.flush()

    above = [r for r in rows if r["above_1e-8_banked"]]
    return {
        "rows": rows,
        "n_rows": len(rows),
        "n_rows_above_1e8_threshold": len(above),
        "n_residuals_bit_identical_pre_post": sum(
            1 for r in rows if r["residual_coarse_bit_identical_pre_post"]
            and r["residual_fine_bit_identical_pre_post"]),
        "n_flag_flips_pre_to_post": sum(1 for r in rows
                                        if r["flag_flipped_pre_to_post"]),
        "n_counts_match_banked": sum(1 for r in rows if r["counts_match_banked"]),
        "n_unstable_total_post": sum(r["n_unstable_post"] for r in rows),
        "worst_residual_rel_diff_vs_banked": max(
            max(r["residual_coarse_rel_diff_vs_banked"],
                r["residual_fine_rel_diff_vs_banked"]) for r in rows),
        "worst_residual_ulps_vs_banked": max(
            abs(r["residual_coarse_ulps_vs_banked"] or 0) for r in rows),
        "all_still_converged_false_where_expected": all(
            (not r["converged_coarse_post"]) for r in above),
    }


# ==========================================================================
# B6 -- Route-G g4_cross_model re-confirmation
# ==========================================================================
def b6_route_g(RS_pre, RS_post, banked, quick):
    print("\n[B6] Route-G g4_cross_model re-confirmation, all 7 rows, "
          "pre vs post vs banked")
    bank = banked["g4_cross_model"]["negative_a"]
    jobs = [(r["K"], r["a"], r) for r in bank]
    if quick:
        jobs = [j for j in jobs if j[0] == 96 and j[1] == -1.0]
    rows = []
    for K, a, b in jobs:
        t0 = time.time()
        # exactly experiments/p2_route_g_v1_collapse.py:383
        flow_pre, res_pre = RS_pre.continuation(a, K=K, da=-0.02, max_iter=300)
        alpha_pre = float(-flow_pre.c_omega(res_pre["b"]))
        flow_post, res_post = RS_post.continuation(a, K=K, da=-0.02, max_iter=300)
        alpha_post = float(-flow_post.c_omega(res_post["b"]))
        r = {
            "K": K, "a": a, "seconds": time.time() - t0,
            "banked_residual": b["residual"],
            "banked_alpha": b["alpha"], "banked_beta": b["beta"],
            "banked_converged": b["converged"],
            "residual_pre": res_pre["residual"],
            "residual_post": res_post["residual"],
            "residual_bit_identical_pre_post":
                bool(same_bits(res_pre["residual"], res_post["residual"])),
            "residual_rel_diff_vs_banked":
                rel_diff(b["residual"], res_post["residual"]),
            "residual_ulps_vs_banked":
                ulps_apart(b["residual"], res_post["residual"]),
            "converged_pre": bool(res_pre["converged"]),
            "converged_post": bool(res_post["converged"]),
            "flag_flipped_pre_to_post":
                bool(res_pre["converged"] != res_post["converged"]),
            "flag_matches_banked": bool(bool(res_post["converged"])
                                        == b["converged"]),
            "alpha_pre": alpha_pre, "alpha_post": alpha_post,
            "alpha_bit_identical_pre_post": bool(same_bits(alpha_pre, alpha_post)),
            "alpha_rel_diff_vs_banked": rel_diff(b["alpha"], alpha_post),
            "alpha_ulps_vs_banked": ulps_apart(b["alpha"], alpha_post),
            "beta_post": 1.0 / alpha_post,
            "beta_rel_diff_vs_banked": rel_diff(b["beta"], 1.0 / alpha_post),
            "b_bit_identical_pre_post": bool(same_bits(res_pre["b"],
                                                       res_post["b"])),
        }
        rows.append(r)
        print("   K=%3d a=%+.2f  res %.6e (banked %.6e, %s ulp)  conv %s->%s "
              "(banked %s)  alpha %.10f (banked %.10f)  (%.0fs)"
              % (K, a, r["residual_post"], r["banked_residual"],
                 r["residual_ulps_vs_banked"], r["converged_pre"],
                 r["converged_post"], r["banked_converged"], r["alpha_post"],
                 r["banked_alpha"], r["seconds"]))
        sys.stdout.flush()
    return {
        "rows": rows,
        "n_rows": len(rows),
        "n_residual_bit_identical_pre_post": sum(
            1 for r in rows if r["residual_bit_identical_pre_post"]),
        "n_alpha_bit_identical_pre_post": sum(
            1 for r in rows if r["alpha_bit_identical_pre_post"]),
        "n_flag_flips_pre_to_post": sum(1 for r in rows
                                        if r["flag_flipped_pre_to_post"]),
        "n_flag_matches_banked": sum(1 for r in rows if r["flag_matches_banked"]),
        "n_converged_false_post": sum(1 for r in rows
                                      if not r["converged_post"]),
        "worst_residual_rel_diff_vs_banked": max(
            r["residual_rel_diff_vs_banked"] for r in rows),
        "worst_alpha_rel_diff_vs_banked": max(
            r["alpha_rel_diff_vs_banked"] for r in rows),
        "worst_residual_ulps_vs_banked": max(
            abs(r["residual_ulps_vs_banked"] or 0) for r in rows),
        "worst_alpha_ulps_vs_banked": max(
            abs(r["alpha_ulps_vs_banked"] or 0) for r in rows),
    }


# ==========================================================================
# B7 -- what this repair does NOT cover, measured rather than asserted
# ==========================================================================
def b7_uncovered(RS_post):
    print("\n[B7] the census of what this repair does NOT cover")
    out = {}

    # (i) planted_eigenvalue_control -- same (K_coarse, K_fine) pair, same filter,
    #     same file, NOT named by leg 203's R1 and therefore NOT repaired.
    c_eq = RS_post.planted_eigenvalue_control(a=0.0, K_coarse=24, K_fine=24,
                                              strength=6.0)
    c_ref = RS_post.planted_eigenvalue_control(a=0.0, K_coarse=24, K_fine=36,
                                               strength=6.0)
    out["planted_eigenvalue_control"] = {
        "file": "solver/rescaled_spectrum.py",
        "guarded_by_leg_225": False,
        "n_planted_equal_K": int(np.asarray(c_eq["planted"]).size),
        "n_plain_equal_K": int(np.asarray(c_eq["plain"]).size),
        "n_planted_refined": int(np.asarray(c_ref["planted"]).size),
        "n_plain_refined": int(np.asarray(c_ref["plain"]).size),
    }
    p = out["planted_eigenvalue_control"]
    p["inflation_factor_equal_K"] = (
        float(p["n_planted_equal_K"]) / max(1, p["n_planted_refined"]))
    print("   planted_eigenvalue_control  K=24/24 keeps %d planted (K=24/36 keeps "
          "%d) -- UNGUARDED, %.1fx"
          % (p["n_planted_equal_K"], p["n_planted_refined"],
             p["inflation_factor_equal_K"]))

    # (ii) converged_dissipative_spectrum -- a re-implementation of this filter in
    #      a DIFFERENT file, outside leg 225's declared territory.
    try:
        from solver.critical_dissipation import converged_dissipative_spectrum
        d_eq = converged_dissipative_spectrum(0.0, 1, 0.5, K_coarse=24, K_fine=24,
                                              tol=1e-3)
        d_ref = converged_dissipative_spectrum(0.0, 1, 0.5, K_coarse=24, K_fine=36,
                                               tol=1e-3)
        out["converged_dissipative_spectrum"] = {
            "file": "solver/critical_dissipation.py",
            "in_leg_225_territory": False,
            "guarded_by_leg_225": False,
            "n_kept_equal_K": int(d_eq["n_kept"]),
            "n_total_equal_K": int(d_eq["n_total"]),
            "n_kept_refined": int(d_ref["n_kept"]),
            "inflation_factor_equal_K": (float(d_eq["n_kept"])
                                         / max(1, int(d_ref["n_kept"]))),
        }
        d = out["converged_dissipative_spectrum"]
        print("   converged_dissipative_spectrum  K=24/24 keeps %d of %d "
              "(K=24/36 keeps %d) -- UNGUARDED, %.1fx, OUT OF TERRITORY"
              % (d["n_kept_equal_K"], d["n_total_equal_K"], d["n_kept_refined"],
                 d["inflation_factor_equal_K"]))
    except Exception as ex:  # noqa: BLE001
        out["converged_dissipative_spectrum"] = {
            "error": "%s: %s" % (type(ex).__name__, str(ex)[:200])}

    out["leg_203_mechanisms_not_addressed"] = [
        "R2 spectrum/converged_spectrum discard newton's converged flag",
        "R3 continuation silently skips on a sign-mismatched da",
        "R4 continuum_defect carries no admissibility content",
        "R6 filter's kept-count blind to a planted wrong profile",
        "R7 match_filter(tol=nan) keeps 0 silently",
        "R8 planted control's docstring criterion is wrong (prose only)",
    ]
    out["leg_203_mechanisms_addressed"] = [
        "R1 converged_spectrum has no guard on K_fine vs K_coarse",
        "R5 non-integer K floor-truncation, ONLY on its R1 reachability path "
        "(converged_spectrum now truncates before comparing, so a non-integer "
        "K_fine that collapses onto K_coarse is rejected)",
    ]
    return out


# ==========================================================================
# the call-site census -- which banked rows actually route through the repair
# ==========================================================================
def call_site_census():
    """grep, not assumption: who literally calls `converged_spectrum`?"""
    try:
        hits = subprocess.check_output(
            ["git", "grep", "-n", "converged_spectrum", "--", "*.py"],
            cwd=ROOT).decode("utf-8").splitlines()
    except subprocess.CalledProcessError:
        hits = []
    calls = [h for h in hits
             if "converged_spectrum(" in h
             and "def converged_spectrum" not in h
             and "converged_dissipative_spectrum" not in h]
    return {
        "grep_all_mentions": hits,
        "literal_call_sites": calls,
        "n_literal_call_sites": len(calls),
        "route_e_e5_actually_calls": "spectrum() x2 + match_filter() directly "
                                     "(experiments/p2_route_e_v1_spectrum.py:164-171)",
        "route_g_g4_actually_calls": "continuation() only "
                                     "(experiments/p2_route_g_v1_collapse.py:383)",
        "route_h_h5_actually_calls": "converged_dissipative_spectrum() "
                                     "(solver/critical_dissipation.py:576), a "
                                     "SEPARATE re-implementation of the filter",
    }


# ==========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="short Route-E/Route-G subsets, for smoke-testing only")
    args = ap.parse_args()

    t_start = time.time()
    print("ROUTE-RSR v1 -- repair of solver/rescaled_spectrum.py (leg 225), "
          "closing leg 203's R1")
    print("  pre-repair source: git %s:%s" % (PRE_REPAIR_REF[:7], MODULE_PATH))

    RS_pre, src_pre = load_pre_repair()
    RS_post, src_post = load_post_repair()
    print("  pre-repair module loaded: %d chars, converged_spectrum guarded=%s"
          % (len(src_pre), "on_no_refinement" in src_pre))
    print("  post-repair module loaded: %d chars, converged_spectrum guarded=%s"
          % (len(src_post), "on_no_refinement" in src_post))

    with open(os.path.join(ROOT, "writeup", "data",
                           "p2_route_e_v1_spectrum.json")) as fh:
        banked_e = json.load(fh)
    with open(os.path.join(ROOT, "writeup", "data",
                           "p2_route_g_v1_collapse.json")) as fh:
        banked_g = json.load(fh)

    res = {
        "leg": 225,
        "route": "RSR",
        "title": "repair of rescaled_spectrum.converged_spectrum's degenerate "
                 "K_fine==K_coarse comparison (leg 203 R1), with an explicit "
                 "re-confirmation of every Route-E and Route-G banked row",
        "module_repaired": MODULE_PATH,
        "pre_repair_ref": PRE_REPAIR_REF,
        "repairs_finding": "leg 203 R1 (+ R5 on its R1 reachability path only)",
        "quick": bool(args.quick),
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "call_site_census": call_site_census(),
    }

    res["B1_adversarial"] = b1_adversarial(RS_pre, RS_post)
    res["B2_reachability"] = b2_reachability(RS_pre, RS_post)
    res["B3_clean_identity"] = b3_clean_identity(RS_pre, RS_post, args.quick)
    res["B4_escape_hatch"] = b4_escape_hatch(RS_pre, RS_post)
    res["B5_route_e"] = b5_route_e(RS_pre, RS_post, banked_e, args.quick)
    res["B6_route_g"] = b6_route_g(RS_pre, RS_post, banked_g, args.quick)
    res["B7_uncovered"] = b7_uncovered(RS_post)

    b1, b2, b3, b4, b5, b6 = (res["B1_adversarial"], res["B2_reachability"],
                              res["B3_clean_identity"], res["B4_escape_hatch"],
                              res["B5_route_e"], res["B6_route_g"])

    clause_repair = (
        b1["n_degenerate_rejected_post"] == b1["n_degenerate_cases"]
        and b1["n_clean_bit_identical"] == b1["n_clean_cases"]
        and b2["n_rejected_post"] == b2["n_cases"]
        and b3["leaves_moved"] == 0
        and b4["n_bit_identical"] == b4["n_cases"])
    clause_reconf_residuals = (
        b5["n_residuals_bit_identical_pre_post"] == b5["n_rows"]
        and b6["n_residual_bit_identical_pre_post"] == b6["n_rows"]
        and b6["n_alpha_bit_identical_pre_post"] == b6["n_rows"])
    clause_reconf_flags = (
        b5["n_flag_flips_pre_to_post"] == 0
        and b6["n_flag_flips_pre_to_post"] == 0
        and b6["n_flag_matches_banked"] == b6["n_rows"]
        and b5["all_still_converged_false_where_expected"])

    res["gate"] = {
        "question": (
            "Does fixing the K_fine==K_coarse degenerate comparison (per leg "
            "203's own identified mechanism) cause every one of leg 203's "
            "adversarial cases to now correctly reject false convergence, AND "
            "does an explicit, fresh re-run of the 5/7 Route-E and 7/7 Route-G "
            "banked rows confirm (a) their own independently-banked residuals "
            "are unchanged, and (b) their converged=False flag from the "
            "module's separate conservative check still holds post-repair "
            "(i.e. the repair doesn't silently relabel them converged=True for "
            "the wrong reason either)?"),
        "clause_repair_complete": bool(clause_repair),
        "clause_reconfirmation_residuals_unchanged": bool(clause_reconf_residuals),
        "clause_reconfirmation_flags_hold": bool(clause_reconf_flags),
        "answer": ("YES" if (clause_repair and clause_reconf_residuals
                             and clause_reconf_flags) else "NO"),
        "priority_finding_route_e_g_moved": bool(
            not (clause_reconf_residuals and clause_reconf_flags)),
    }
    res["wall_clock_seconds"] = time.time() - t_start

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(res, fh, indent=1, default=float)

    print("\n" + "=" * 74)
    print("GATE: %s" % res["gate"]["answer"])
    print("  repair complete .................. %s  (%d/%d degenerate rejected, "
          "%d/%d clean bit-identical, %d leaves moved)"
          % (clause_repair, b1["n_degenerate_rejected_post"],
             b1["n_degenerate_cases"], b1["n_clean_bit_identical"],
             b1["n_clean_cases"], b3["leaves_moved"]))
    print("  Route-E/G residuals unchanged .... %s  (E %d/%d, G %d/%d bit-identical)"
          % (clause_reconf_residuals, b5["n_residuals_bit_identical_pre_post"],
             b5["n_rows"], b6["n_residual_bit_identical_pre_post"], b6["n_rows"]))
    print("  Route-E/G flags still hold ....... %s  (%d flag flips total)"
          % (clause_reconf_flags, b5["n_flag_flips_pre_to_post"]
             + b6["n_flag_flips_pre_to_post"]))
    if res["gate"]["priority_finding_route_e_g_moved"]:
        print("\n  *** PRIORITY FINDING: a Route-E/Route-G banked row MOVED. ***")
    print("  wrote %s  (%.0fs)" % (OUT_JSON, res["wall_clock_seconds"]))
    print("=" * 74)


if __name__ == "__main__":
    main()
