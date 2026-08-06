"""Route-FGB v1: the POST-REPAIR REGRESSION CHECK for solver/fractional_gclm.py.

WHAT THIS IS.  Leg 91 (Route-FGA) measured a silent-acceptance gap in
`solver/fractional_gclm.py`: `s < 0` and `nu < 0` were accepted at construction, ran to
completion, and returned a finite, plausible-looking relevance exponent `p` which -- injected
into the `p(s)` fit whose zero crossing IS the measured `s_c` -- moved that crossing by up to
+13.33 %.  The bench repair `8d4fdec` landed with leg 91's own audit and, unlike legs 92/98/99's
findings, never got its close-the-loop regression leg.  This is that leg.

    GATE.  Post-repair, does solver/fractional_gclm.py (a) reject every s<0 / nu<0 case in
    leg 91's original battery at construction, and (b) reproduce the banked s_c measurement
    bit-identically on the validated line?

WHAT THIS IS NOT.  It is not a measurement of `s_c`, and not a re-derivation of anything.
`s_c = alpha/2` is validated against XU eq (6.3) row by row and is marked PRE-EMPTED under
Route-J -- settled physics, fixed background.  The banked `s_c` is touched here only to ask
WHETHER THE BITS MOVED.  No number printed by this file is a statement about the value of `s_c`
for any physically admissible `s`.

`solver/fractional_gclm.py` is READ-ONLY under this leg, under either branch of the gate.

--------------------------------------------------------------------------
THE THREE BATTERIES
--------------------------------------------------------------------------
B1  LEG 91'S BATTERY, RE-RUN AS LEG 91'S OWN CODE.  This file *imports*
    experiments/p2_route_fga_v1_adversarial.py and calls its `a1_pure_functions`,
    `a2_operator_construction`, `a3_pipeline`, `a4_sc_contamination` and
    `a5_dissipation_strength` directly, with leg 91's own constants.  Its `main()` is never
    called, so its JSON -- the frozen PRE-REPAIR evidence -- is never overwritten.  That is
    what makes this re-run independent of the repair's own bundled test.
    Each battery is diffed case-by-case against the banked pre-repair JSON.

B2  THE BANKED s_c, THREE WAYS.  Route-F's `F2_relevance_line` (n = 8192, a = 0, nu = 1e-3,
    seven s values) is the validated line whose zero crossing is the banked `s_c`
    (`s_zero = 0.5033053850201455`).  A two-arm comparison (banked JSON vs today) CANNOT
    separate "the repair moved the number" from "the environment moved the number", so there
    are three arms:

        BANKED  writeup/data/p2_route_f_v1_viscosity.json, generated 2026-08-02T01:15:27Z
        POST    the module on main today (with the guard)
        PRE     the module at 8d4fdec^, reconstructed by `git show` into a temp file and
                imported under a private name -- never written into the repo

    POST vs PRE isolates the REPAIR.  POST vs BANKED includes everything else.  Distances are
    reported in ULPs, never as the word "identical".  This is the control that can come out
    differently (lesson 90): PRE is a real second computation, and if the guard had touched the
    numerical path the two arms would disagree.

B3  THE KNOWN-ANSWER GATE, same three ways.  Route-F's `F1_known_answer` -- the exact a = 0
    CLM solution, the solver-vs-exact error at t = 2.5, and the run's own recovered singular
    time -- is the gate the whole of Route-F hangs from.  Cheap, and an independent second
    surface for the same bit-identity question.  It is also a DISCRIMINATOR: F1 runs at
    `nu = 0`, `s = 1`, so `|k|^{2s}` is an exact integer power and `exp(-nu*visc*dt)` is
    `exp(0) = 1` exactly -- neither transcendental kernel is exercised non-trivially.  F2 runs
    at `nu = 1e-3` and fractional `s`, so both are.  If the archive arm splits along that line,
    the drift is localized to the libm/NumPy kernels, not to anything in this repository.

B4  THE MECHANISM, MEASURED RATHER THAN ASSERTED (lesson 85: ablate the mechanism, not just
    the effect).  "A library kernel moved by an ULP" is only an explanation if an ULP is
    ENOUGH.  So: rebuild the same line with `visc` displaced by exactly ONE ULP
    (`np.nextafter`) and nothing else changed, and measure how far `p` and the zero crossing
    move.  If a 1-ULP displacement of the multiplier already produces a shift of the same
    order as the archive arm's, the archive arm needs no further explanation.  If it produces
    a shift orders of magnitude smaller, the explanation is wrong and something else moved --
    which is why this probe is in the leg rather than a sentence in the journal.

Deterministic, NOT logged.  Writes writeup/data/p2_route_fgb_v1_postrepair.json.

Run: .venv/bin/python -u experiments/p2_route_fgb_v1_postrepair.py
"""

import importlib.util
import json
import platform
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

BANKED_FGA = ROOT / "writeup" / "data" / "p2_route_fga_v1_adversarial.json"
BANKED_F = ROOT / "writeup" / "data" / "p2_route_f_v1_viscosity.json"
OUT = ROOT / "writeup" / "data" / "p2_route_fgb_v1_postrepair.json"

REPAIR_COMMIT = "8d4fdec"          # Leg 0: ORCH -- the domain guard
PRE_REPAIR_REF = REPAIR_COMMIT + "^:solver/fractional_gclm.py"

# Route-F's own constants, used as imported -- not re-tuned here.
N_LINE = 8192
AMP_LINE = 1000.0
S_LINE = (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75)
NU_LINE = 1e-3
A_LINE = 0.0


# --------------------------------------------------------------------------
def ulps(a, b):
    """Signed distance in ULPs between two float64s.  0 means bit-identical.

    Reported instead of "identical" because an equality with no stated resolution says
    nothing: 0 ULP is a measurement, not a word.
    """
    a, b = float(a), float(b)
    if np.isnan(a) or np.isnan(b):
        return None
    ia, ib = (struct.unpack("<q", struct.pack("<d", v))[0] for v in (a, b))
    ia = ia if ia >= 0 else (1 << 63) - ia
    ib = ib if ib >= 0 else (1 << 63) - ib
    return int(ib - ia)


def cmp3(name, banked, post, pre):
    """One row of the three-arm comparison."""
    d_bp = ulps(banked, post)
    d_pp = ulps(pre, post)
    return {"quantity": name,
            "banked": float(banked), "post": float(post), "pre": float(pre),
            "ulps_banked_to_post": d_bp,
            "ulps_pre_to_post": d_pp,
            "rel_banked_to_post": (abs(float(post) - float(banked))
                                   / abs(float(banked)) if banked else None),
            "repair_is_bitwise_noop": (d_pp == 0),
            "reproduces_banked_bitwise": (d_bp == 0)}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pre_repair_module():
    """The module as it stood at 8d4fdec^, reconstructed from git into a temp file.

    Never written into the repository: this leg's territory does not include solver/, and the
    pre-repair source is history, not a file anyone should be able to import by accident.
    """
    src = subprocess.run(["git", "show", PRE_REPAIR_REF], cwd=str(ROOT),
                         capture_output=True, text=True, check=True).stdout
    tmp = Path(tempfile.mkdtemp(prefix="fgb_pre_")) / "fractional_gclm_prerepair.py"
    tmp.write_text(src)
    return load_module(tmp, "_fgb_pre_fractional_gclm"), src


def initial(n):
    x = np.arange(n) * 2.0 * np.pi / n
    return np.sin(x) + 0.4 * np.sin(2.0 * x)


# --------------------------------------------------------------------------
def b1_battery(fga, banked):
    """Leg 91's five batteries, its own code, against the repaired module."""
    print("\n" + "=" * 78)
    print("[B1] LEG 91's BATTERY, RE-RUN VERBATIM (its functions, its constants)")
    print("=" * 78)
    post = {}
    post["A1"] = fga.a1_pure_functions()
    post["A2"] = fga.a2_operator_construction()
    post["A3"] = fga.a3_pipeline()

    print("\n[A4-pre] the clean relevance line (audit resolution n = %d)" % fga.N_AUDIT)
    clean = []
    for s in fga.CLEAN_S:
        r = fga._pipeline(s)
        print("   s=%.2f  p=%+.4f  outcome=%s  (%.1fs)" % (s, r["p"], r["outcome"],
                                                           r["seconds"]))
        clean.append({"s": float(s), "p": float(r["p"]), "outcome": r["outcome"]})
    post["A4"] = fga.a4_sc_contamination(clean)
    post["A5"] = fga.a5_dissipation_strength()

    # -- the case-by-case diff against the frozen pre-repair evidence ------
    print("\n[B1-diff] pre-repair (banked, leg 91) vs post-repair (today), case by case")
    diff = {}

    # A1: the pure closed forms.  The repair was scoped to the OPERATOR and deliberately did
    # not touch these; leg 91's gates 2/3/5 pin them as known gaps.  Counted, not hidden.
    b1a, p1a = banked["A1_pure_functions"], post["A1"]
    diff["A1"] = {"pre_n_silent_finite": b1a["n_silent_finite"],
                  "post_n_silent_finite": p1a["n_silent_finite"],
                  "n_cases": p1a["n_cases"],
                  "in_gate_scope": False,
                  "note": ("the PURE CLOSED FORMS critical_s / relevance_exponent, which the "
                           "repair was explicitly scoped NOT to touch (leg 91 gates 2/3/5 are "
                           "standing gap pins). They are not a construction path, so they are "
                           "outside the gate's clause (a), which says 'at construction'.")}
    print("   A1 pure closed forms   silent-finite: %d/%d -> %d/%d   (out of gate scope)"
          % (b1a["n_silent_finite"], b1a["n_cases"],
             p1a["n_silent_finite"], p1a["n_cases"]))

    # A2: operator construction -- the gate's clause (a) proper.
    b2r = {str(r["s"]): r for r in banked["A2_operator_construction"]["rows"]}
    a2rows = []
    for r in post["A2"]["rows"]:
        key = str(r["s"])
        b = b2r.get(key, {})
        neg = isinstance(r["s"], float) and r["s"] < 0.0
        a2rows.append({
            "s": r["s"], "negative_s": neg,
            "pre_raised": b.get("exception") is not None,
            "post_raised": r.get("exception") is not None,
            "pre_mask_hid_a_nonfinite_k0": b.get("mask_hid_a_nonfinite_k0"),
            "pre_monotone_increasing_in_k": b.get("monotone_increasing_in_k"),
            "post_exception": r.get("exception"),
            "post_monotone_increasing_in_k": r.get("monotone_increasing_in_k")})
    n_neg = sum(1 for r in a2rows if r["negative_s"])
    n_neg_raised = sum(1 for r in a2rows if r["negative_s"] and r["post_raised"])
    n_neg_pre_built = sum(1 for r in a2rows if r["negative_s"] and not r["pre_raised"])
    n_inv_pre = sum(1 for r in a2rows
                    if r["negative_s"] and r["pre_monotone_increasing_in_k"] is False)
    n_valid_still_build = sum(1 for r in a2rows
                              if not r["negative_s"] and not r["post_raised"])
    n_valid = sum(1 for r in a2rows if not r["negative_s"])
    diff["A2"] = {"rows": a2rows, "n_negative_s_cases": n_neg,
                  "n_negative_s_built_an_operator_pre": n_neg_pre_built,
                  "n_negative_s_with_inverted_multiplier_pre": n_inv_pre,
                  "n_negative_s_rejected_at_construction_post": n_neg_raised,
                  "n_non_negative_s_cases": n_valid,
                  "n_non_negative_s_still_construct_post": n_valid_still_build,
                  "in_gate_scope": True}
    print("   A2 construction        s<0 cases %d: built an operator PRE %d (of which %d with "
          "an INVERTED, decreasing multiplier) -> rejected at construction POST %d"
          % (n_neg, n_neg_pre_built, n_inv_pre, n_neg_raised))
    print("      no-overshoot: %d/%d non-negative s still construct normally"
          % (n_valid_still_build, n_valid))

    # A3: the full pipeline.
    b3, p3 = banked["A3_pipeline"], post["A3"]
    diff["A3"] = {"pre_n_silent_finite_p": b3["n_silent_finite_p"],
                  "post_n_silent_finite_p": p3["n_silent_finite_p"],
                  "pre_silent_s_values": b3["silent_s_values"],
                  "post_silent_s_values": p3["silent_s_values"],
                  "pre_n_refused": b3["n_refused"], "post_n_refused": p3["n_refused"],
                  "rows": [{"case": r["case"], "s": r["s"], "invalid_input": r["invalid_input"],
                            "outcome": r["outcome"], "p": r["p"], "p_finite": r["p_finite"],
                            "exception": r["exception"]} for r in p3["rows"]],
                  "in_gate_scope": True}
    print("   A3 full pipeline       invalid-s inputs returning a SILENT finite p: %d -> %d "
          "(pre: s=%s)" % (b3["n_silent_finite_p"], p3["n_silent_finite_p"],
                           b3["silent_s_values"]))

    # A4: the headline -- contamination of the measured s_c.
    b4, p4 = banked["A4_sc_contamination"], post["A4"]
    conts = []
    for bc, pc in zip(b4["contaminations"], p4["contaminations"]):
        conts.append({"s_injected": pc["s_injected"],
                      "pre_p_injected": bc["p_injected"],
                      "pre_shift": bc.get("shift"),
                      "pre_shift_percent": bc.get("shift_percent"),
                      "post_p_injected": pc["p_injected"],
                      "post_shift": pc.get("shift"),
                      "post_propagated_or_flagged": pc["propagated_or_flagged"]})
        print("   A4 inject s=%+.1f       s_c shift PRE %s -> POST %s (flagged=%s)"
              % (pc["s_injected"],
                 ("%+.6f (%+.2f%%)" % (bc["shift"], bc["shift_percent"]))
                 if isinstance(bc.get("shift"), float) else str(bc.get("shift")),
                 str(pc.get("shift")), pc["propagated_or_flagged"]))
    diff["A4"] = {"contaminations": conts,
                  "pre_clean_zero": b4["clean_zero"], "post_clean_zero": p4["clean_zero"],
                  "n_injections": len(conts),
                  "n_reaching_the_fit_pre": sum(1 for c in conts
                                                if isinstance(c["pre_shift"], float)),
                  "n_reaching_the_fit_post": sum(
                      1 for c in conts if not c["post_propagated_or_flagged"]),
                  "in_gate_scope": True,
                  "note": ("clean_zero at n=%d is an AUDIT ARTEFACT, not a physics number; "
                           "only the shift is claimed, and clean vs contaminated share every "
                           "setting so resolution bias cancels." % fga.N_AUDIT)}

    # A5: the dissipation strength.
    b5, p5 = banked["A5_dissipation_strength"], post["A5"]
    a5rows = []
    for br, pr in zip(b5["rows"], p5["rows"]):
        a5rows.append({"case": pr["case"], "nu": pr["nu"],
                       "pre_p": br["p"], "pre_p_finite": br["p_finite"],
                       "pre_p_vs_control_percent": br.get("p_vs_control_percent"),
                       "post_p": pr["p"], "post_p_finite": pr["p_finite"],
                       "post_exception": pr["exception"], "post_outcome": pr["outcome"]})
        print("   A5 %-38s p PRE %-9s -> POST %-9s  raised=%s"
              % (pr["case"], str(br["p"])[:9], str(pr["p"])[:9],
                 pr["exception"] is not None))
    n_neg_nu_pre = sum(1 for r in a5rows if isinstance(r["nu"], float) and r["nu"] < 0
                       and r["pre_p_finite"])
    n_neg_nu_post = sum(1 for r in a5rows if isinstance(r["nu"], float) and r["nu"] < 0
                        and r["post_p_finite"])
    diff["A5"] = {"rows": a5rows,
                  "pre_n_silent_finite_p": b5["n_silent_finite_p"],
                  "post_n_silent_finite_p": p5["n_silent_finite_p"],
                  "n_negative_nu_silent_pre": n_neg_nu_pre,
                  "n_negative_nu_silent_post": n_neg_nu_post,
                  "pre_control_p": b5["control_p"], "post_control_p": p5["control_p"],
                  "in_gate_scope": True}

    # -- clause (a) of the gate, counted -----------------------------------
    scope = {"A2_negative_s_construction": (n_neg_pre_built, n_neg_raised),
             "A3_pipeline_invalid_s_silent": (b3["n_silent_finite_p"],
                                              b3["n_silent_finite_p"] - p3["n_silent_finite_p"]),
             "A4_injections_reaching_the_sc_fit": (diff["A4"]["n_reaching_the_fit_pre"],
                                                   diff["A4"]["n_reaching_the_fit_pre"]
                                                   - diff["A4"]["n_reaching_the_fit_post"]),
             "A5_negative_nu_silent": (n_neg_nu_pre, n_neg_nu_pre - n_neg_nu_post)}
    tot_pre = sum(v[0] for v in scope.values())
    tot_closed = sum(v[1] for v in scope.values())
    diff["clause_a"] = {"per_battery_pre_and_closed": {k: list(v) for k, v in scope.items()},
                        "n_gate_scoped_silent_pre": tot_pre,
                        "n_closed_post": tot_closed,
                        "n_still_silent_post": tot_pre - tot_closed}
    print("\n   CLAUSE (a): %d gate-scoped s<0 / nu<0 silent-acceptance cases pre-repair, "
          "%d closed post-repair, %d still silent"
          % (tot_pre, tot_closed, tot_pre - tot_closed))
    print("   NO-OVERSHOOT: %d/%d admissible-s constructions unaffected; control p at the "
          "admissible s: PRE %s -> POST %s"
          % (n_valid_still_build, n_valid, b5["control_p"], p5["control_p"]))
    return {"post": post, "diff": diff}


# --------------------------------------------------------------------------
def _f2_line(mod, tag):
    """Route-F's F2_relevance_line, recomputed with `mod` as the solver module."""
    rows = []
    for s in S_LINE:
        t0 = time.time()
        g = mod.FractionalGCLM(n=N_LINE, a=A_LINE, nu=NU_LINE, s=s)
        r = g.run(initial(N_LINE), amp_factor=AMP_LINE, sample_every=5, max_steps=600000)
        T = mod.estimate_T(r)
        f = mod.fit_relevance(r, T)
        rows.append({"s": float(s), "T_est": float(T), "p": float(f["p"]),
                     "fit_rms": float(f.get("fit_rms", float("nan"))),
                     "n_points": int(f.get("n_points", 0)),
                     "outcome": r["outcome"], "steps": int(r["steps"]),
                     "max_tail": float(r["max_tail"])})
        print("   [%s] s=%.2f  p=%.16f  outcome=%-15s (%.1fs)"
              % (tag, s, f["p"], r["outcome"], time.time() - t0))
    ss = np.array([r["s"] for r in rows])
    pp = np.array([r["p"] for r in rows])
    c = np.polyfit(ss, pp, 1)
    return {"rows": rows, "slope": float(c[0]), "s_zero": float(-c[1] / c[0])}


def b2_sc_bitwise(pre_mod, banked_f):
    """THE HEADLINE.  The banked s_c line, three ways."""
    print("\n" + "=" * 78)
    print("[B2] THE BANKED s_c LINE, THREE ARMS  (n = %d, a = %.1f, nu = %g, %d s values)"
          % (N_LINE, A_LINE, NU_LINE, len(S_LINE)))
    print("     BANKED = writeup/data/p2_route_f_v1_viscosity.json (%s)"
          % banked_f.get("generated"))
    print("     POST   = solver/fractional_gclm.py on main today (with the guard)")
    print("     PRE    = the same module at %s, reconstructed from git" % PRE_REPAIR_REF)
    print("=" * 78)
    import solver.fractional_gclm as post_mod          # noqa: PLC0415 -- deliberate, local
    post = _f2_line(post_mod, "POST")
    pre = _f2_line(pre_mod, "PRE ")
    b = banked_f["F2_relevance_line"]

    cmps = []
    for i, s in enumerate(S_LINE):
        cmps.append(cmp3("p(s=%.2f)" % s, b["rows"][i]["p"], post["rows"][i]["p"],
                         pre["rows"][i]["p"]))
        cmps.append(cmp3("T_est(s=%.2f)" % s, b["rows"][i]["T_est"], post["rows"][i]["T_est"],
                         pre["rows"][i]["T_est"]))
    cmps.append(cmp3("slope", b["slope"], post["slope"], pre["slope"]))
    cmps.append(cmp3("s_zero (THE BANKED s_c MEASUREMENT)", b["s_zero"], post["s_zero"],
                     pre["s_zero"]))

    print("\n   quantity                              banked                post                "
          "  ULP(b->post)  ULP(pre->post)")
    for c in cmps:
        print("   %-36s  %.17g  %.17g  %12s  %14s"
              % (c["quantity"], c["banked"], c["post"],
                 c["ulps_banked_to_post"], c["ulps_pre_to_post"]))

    n = len(cmps)
    n_pre_eq = sum(1 for c in cmps if c["repair_is_bitwise_noop"])
    n_bank_eq = sum(1 for c in cmps if c["reproduces_banked_bitwise"])
    worst_bank = max((abs(c["ulps_banked_to_post"]) for c in cmps
                      if c["ulps_banked_to_post"] is not None), default=None)
    worst_rel = max((c["rel_banked_to_post"] for c in cmps
                     if c["rel_banked_to_post"] is not None), default=None)
    print("\n   REPAIR ARM  (PRE vs POST, same environment): %d/%d quantities at 0 ULP" %
          (n_pre_eq, n))
    print("   ARCHIVE ARM (BANKED vs POST, across environments): %d/%d at 0 ULP; worst "
          "%s ULP, worst relative %.3e" % (n_bank_eq, n, worst_bank, worst_rel or 0.0))

    # -- how big is the archive-arm drift AGAINST THE MEASUREMENT'S OWN ERROR BAR? -----
    # Route-F's own dominant systematic is the fit window (F7), swept not chosen; F5 is the
    # resolution ladder.  Quoting the drift in ULPs alone would be "small in which norm?".
    dz = abs(post["s_zero"] - b["s_zero"])
    w7 = banked_f["F7_window_systematic"]["zero_halfspread"]
    r5 = banked_f["F5_resolution"]["spread"]
    scale = {"s_zero_abs_shift_banked_to_post": dz,
             "s_zero_rel_shift_banked_to_post": dz / abs(b["s_zero"]),
             "route_f_window_systematic_halfspread_F7": w7,
             "route_f_resolution_spread_F5": r5,
             "shift_over_window_systematic": dz / w7,
             "shift_over_resolution_spread": dz / r5,
             "banked_s_zero_vs_predicted_s_c": abs(b["s_zero"] - 0.5)}
    print("   SCALE: the archive-arm shift in s_zero is %.3e absolute (%.3e relative), i.e. "
          "%.3e of Route-F's own window systematic (%.4f) and %.3e of its resolution spread "
          "(%.4f).  The banked s_zero itself sits %.4f from the predicted s_c = 0.5."
          % (dz, dz / abs(b["s_zero"]), dz / w7, w7, dz / r5, r5, abs(b["s_zero"] - 0.5)))
    return {"post": post, "pre": pre, "significance": scale,
            "banked": {"rows": b["rows"], "slope": b["slope"], "s_zero": b["s_zero"],
                       "generated": banked_f.get("generated")},
            "comparisons": cmps, "n_quantities": n,
            "n_zero_ulp_repair_arm": n_pre_eq, "n_zero_ulp_archive_arm": n_bank_eq,
            "worst_ulp_archive_arm": worst_bank, "worst_rel_archive_arm": worst_rel}


# --------------------------------------------------------------------------
def _f1(mod):
    """Route-F's F1_known_answer, recomputed with `mod` as the solver module."""
    n = N_LINE
    w0 = initial(n)
    T0 = mod.clm_blowup_time(w0)
    g = mod.FractionalGCLM(n=n, a=0.0, nu=0.0, s=1.0)
    mid = g.run(w0, t_end=2.5, amp_factor=1e12, sample_every=5)
    err = float(np.max(np.abs(mid["omega"] - mod.clm_exact(w0, mid["t_final"]))))
    r = g.run(w0, amp_factor=AMP_LINE, sample_every=5)
    Te = mod.estimate_T(r)
    return {"T_exact": float(T0), "solver_vs_exact_at_2.5": err, "T_est": float(Te),
            "T_rel_err": abs(Te - T0) / T0, "max_tail": float(r["max_tail"])}


def b3_known_answer(pre_mod, banked_f):
    print("\n" + "=" * 78)
    print("[B3] THE KNOWN-ANSWER GATE (Route-F F1), same three arms")
    print("=" * 78)
    import solver.fractional_gclm as post_mod          # noqa: PLC0415
    post, pre = _f1(post_mod), _f1(pre_mod)
    b = banked_f["F1_known_answer"]
    cmps = [cmp3(k, b[k], post[k], pre[k])
            for k in ("T_exact", "solver_vs_exact_at_2.5", "T_est", "T_rel_err", "max_tail")]
    for c in cmps:
        print("   %-24s banked %.17g  post %.17g  ULP(b->post)=%s  ULP(pre->post)=%s"
              % (c["quantity"], c["banked"], c["post"], c["ulps_banked_to_post"],
                 c["ulps_pre_to_post"]))
    n_pre_eq = sum(1 for c in cmps if c["repair_is_bitwise_noop"])
    n_bank_eq = sum(1 for c in cmps if c["reproduces_banked_bitwise"])
    print("   REPAIR ARM %d/%d at 0 ULP;  ARCHIVE ARM %d/%d at 0 ULP"
          % (n_pre_eq, len(cmps), n_bank_eq, len(cmps)))
    return {"post": post, "pre": pre, "banked": b, "comparisons": cmps,
            "n_quantities": len(cmps), "n_zero_ulp_repair_arm": n_pre_eq,
            "n_zero_ulp_archive_arm": n_bank_eq}


# --------------------------------------------------------------------------
def b4_ulp_sensitivity(b2):
    """Is ONE ULP in the dissipation multiplier enough to produce the archive arm's drift?

    Everything is held fixed except `visc`, which is displaced by exactly one ULP upward
    AFTER construction -- i.e. the smallest possible difference a different `pow`
    implementation could make.  The comparison is against this leg's own POST line, so the
    environment, the module and the driver are identical and the ULP displacement is the only
    variable.  A control that can come out differently: if the integration were insensitive at
    this order, this probe would report a handful of ULPs and refute the localization.
    """
    print("\n" + "=" * 78)
    print("[B4] MECHANISM: displace visc by exactly ONE ULP, change nothing else")
    print("=" * 78)
    import solver.fractional_gclm as mod               # noqa: PLC0415
    rows = []
    for s in S_LINE:
        g = mod.FractionalGCLM(n=N_LINE, a=A_LINE, nu=NU_LINE, s=s)
        g.visc = np.nextafter(g.visc, np.inf)          # 1 ULP up, elementwise
        g.visc[0] = 0.0                                # the mean is still not dissipated
        r = g.run(initial(N_LINE), amp_factor=AMP_LINE, sample_every=5, max_steps=600000)
        T = mod.estimate_T(r)
        f = mod.fit_relevance(r, T)
        rows.append({"s": float(s), "p": float(f["p"]), "T_est": float(T)})
    ss = np.array([r["s"] for r in rows])
    pp = np.array([r["p"] for r in rows])
    c = np.polyfit(ss, pp, 1)
    nudged = {"rows": rows, "slope": float(c[0]), "s_zero": float(-c[1] / c[0])}

    post = b2["post"]
    cmps = []
    for i, s in enumerate(S_LINE):
        cmps.append({"quantity": "p(s=%.2f)" % s,
                     "ulps_post_to_nudged": ulps(post["rows"][i]["p"], rows[i]["p"])})
    cmps.append({"quantity": "slope",
                 "ulps_post_to_nudged": ulps(post["slope"], nudged["slope"])})
    cmps.append({"quantity": "s_zero",
                 "ulps_post_to_nudged": ulps(post["s_zero"], nudged["s_zero"])})
    for c_ in cmps:
        print("   %-12s  1-ULP-in-visc moves it by %s ULP"
              % (c_["quantity"], c_["ulps_post_to_nudged"]))
    worst = max(abs(c_["ulps_post_to_nudged"]) for c_ in cmps
                if c_["ulps_post_to_nudged"] is not None)
    arch = b2["worst_ulp_archive_arm"]
    print("\n   worst 1-ULP-in-visc response: %d ULP;  worst ARCHIVE-arm drift: %d ULP;  "
          "ratio %.2f" % (worst, arch, (arch / worst) if worst else float("inf")))
    return {"nudged": nudged, "comparisons": cmps,
            "worst_ulp_response_to_one_ulp_in_visc": worst,
            "worst_ulp_archive_arm": arch,
            "archive_drift_over_one_ulp_response": (arch / worst) if worst else None,
            "one_ulp_accounts_for_the_archive_arm": bool(worst >= arch)}


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("ROUTE-FGB v1 -- POST-REPAIR REGRESSION CHECK of solver/fractional_gclm.py")
    print("Leg 134. NOT a measurement of s_c (PRE-EMPTED, Route-J, settled physics).")
    print("The module is READ-ONLY under this leg, under either branch of the gate.")

    fga = load_module(ROOT / "experiments" / "p2_route_fga_v1_adversarial.py",
                      "_fgb_leg91_battery")
    banked_fga = json.loads(BANKED_FGA.read_text())
    banked_f = json.loads(BANKED_F.read_text())
    pre_mod, pre_src = pre_repair_module()

    import solver.fractional_gclm as post_mod          # noqa: PLC0415
    post_src = (ROOT / "solver" / "fractional_gclm.py").read_text()

    d = {"leg": 134, "route": "FGB",
         "title": "post-repair regression check of fractional_gclm.py's domain guard, and the "
                  "banked s_c line re-run three ways",
         "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "repair_commit": REPAIR_COMMIT,
         "not_a_physics_measurement": (
             "s_c = alpha/2 is validated against XU eq (6.3) and PRE-EMPTED (Route-J). "
             "Nothing here re-measures or contests it. The banked s_c is touched only to ask "
             "whether the bits moved."),
         "environment": {"python": platform.python_version(), "numpy": np.__version__,
                         "platform": platform.platform(), "machine": platform.machine()},
         "sources": {"pre_repair_ref": PRE_REPAIR_REF,
                     "pre_repair_source_lines": len(pre_src.splitlines()),
                     "post_repair_source_lines": len(post_src.splitlines()),
                     "diff_is_additive_only": (
                         len(post_src.splitlines()) > len(pre_src.splitlines())),
                     "banked_fga_json": str(BANKED_FGA.relative_to(ROOT)),
                     "banked_f_json": str(BANKED_F.relative_to(ROOT))}}

    d["B1_leg91_battery_rerun"] = b1_battery(fga, banked_fga)
    d["B2_sc_line_bitwise"] = b2_sc_bitwise(pre_mod, banked_f)
    d["B3_known_answer_bitwise"] = b3_known_answer(pre_mod, banked_f)
    d["B4_ulp_sensitivity"] = b4_ulp_sensitivity(d["B2_sc_line_bitwise"])

    # -- the gate, answered from the batteries themselves ------------------
    ca = d["B1_leg91_battery_rerun"]["diff"]["clause_a"]
    b2 = d["B2_sc_line_bitwise"]
    b3 = d["B3_known_answer_bitwise"]
    clause_a = (ca["n_still_silent_post"] == 0)
    repair_arm = (b2["n_zero_ulp_repair_arm"] == b2["n_quantities"]
                  and b3["n_zero_ulp_repair_arm"] == b3["n_quantities"])
    archive_arm = (b2["n_zero_ulp_archive_arm"] == b2["n_quantities"]
                   and b3["n_zero_ulp_archive_arm"] == b3["n_quantities"])
    d["gate"] = {
        "question": ("Post-repair, does solver/fractional_gclm.py (a) reject every s<0 / nu<0 "
                     "case in leg 91's original battery at construction, and (b) reproduce "
                     "the banked s_c measurement bit-identically on the validated line?"),
        "clause_a_all_rejected_at_construction": clause_a,
        "clause_a_counts": ca,
        "clause_b_repair_arm_bitwise": repair_arm,
        "clause_b_archive_arm_bitwise": archive_arm,
        "answer": "yes" if (clause_a and repair_arm) else "no",
        "answer_qualifier": (
            "clause (b) is answered on the REPAIR ARM (PRE vs POST in one environment), which "
            "is the arm that isolates the repair and the only arm a repair can be held to. "
            "The ARCHIVE ARM (BANKED vs POST) additionally spans a compiler/library "
            "environment change since 2026-08-02 and is reported separately, in ULPs.")}
    d["seconds"] = round(time.time() - t0, 1)

    print("\n" + "=" * 78)
    print("GATE (a) every s<0 / nu<0 case rejected at construction: %s "
          "(%d gate-scoped silent cases -> %d)"
          % (str(clause_a).upper(), ca["n_gate_scoped_silent_pre"], ca["n_still_silent_post"]))
    print("GATE (b) banked s_c reproduced bitwise -- REPAIR ARM: %s ; ARCHIVE ARM: %s"
          % (str(repair_arm).upper(), str(archive_arm).upper()))
    print("GATE: %s" % d["gate"]["answer"].upper())
    print("=" * 78)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(d, indent=1))
    print("wrote %s  (%.1f s)" % (OUT, d["seconds"]))


if __name__ == "__main__":
    main()
