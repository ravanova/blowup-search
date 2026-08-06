"""Route-VNA v1 -- the adversarial battery against solver/viscous_novelty.py.

THE GATE (leg 143, verbatim)
-----------------------------
Under adversarial and degenerate inputs, does `viscous_novelty.py` ever silently return a
wrong value rather than reject or visibly propagate the defect?

  yes -> Name the exact mechanism and magnitude; escalate for a repair leg if
         claim-adjacent, do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         capabilities.py.

WHAT THIS MODULE IS, AND WHAT A DEFECT HERE WOULD COST
-------------------------------------------------------
`solver/viscous_novelty.py` is NOT a certificate module -- it has no Y_0/Z_0/Z_1/Z_2 and no
`closes=True` verdict, so the fabrication-rejection class of legs 79/98/116/140 cannot occur
here and is not looked for (see `writeup/novelty/leg_143.md`).  It is the executable form of
**stage V's novelty gate**: `novelty_verdict()` returns the "YES, stage V is pre-empted"
answer that `plan_of_record.py` records as CLOSED BY ITS OWN GATE at leg 48, and the
reproduction functions underwrite `capabilities.py`'s recorded agreement magnitudes with
Dahne-Figueras arXiv:2410.05480.

WHAT "TRUE" MEANS HERE, AND WHERE IT COMES FROM
------------------------------------------------
Not this leg's invention.  Every reference below is the module's OWN documented contract:

  * `branch_in_kappa`'s docstring: "The sweep STOPS when Newton stops converging or when
    eps leaves [0, 1): past the branch's end the map has other zeros (with negative eps,
    i.e. anti-dissipation) and a continuation that does not check will happily report them
    as branch points."  So eps outside [0,1) is, by the module's own sentence, not a branch
    point.  G1 measures what happens in the one continuation consumer that does not check.

  * `integrate_from_zero`'s docstring: "the initial-value problem Q(0) = mu, Q'(0) = 0,
    integrated to xi1".  So a return that never advanced past the xi = 1e-8 series start is
    wrong by its own contract.  G2 measures it against the honestly-integrated value.

  * `compare_to_published_branch`'s docstring: "our sweep is monotone in kappa, so a plain
    interpolation is well-defined".  G3 measures what the same code returns when that
    stated precondition does not hold.

  * The `PRECEDENTS` ledger documents exactly three verdict values -- PRE_EMPTS, ADJACENT,
    EXCLUSION.  G4 measures whether anything enforces that vocabulary.

READ-ONLY.  `solver/viscous_novelty.py` is NOT edited by this leg under either branch of the
gate.  Every gate below is a measurement, and the ones that FAIL are pinned, not patched.

LESSON 90.  Every "no guard here" claim sits beside G5 -- the guards in this same module
that DO fire, and that could have come out the other way.

LATENCY IS PART OF THE FINDING (legs 79/116).  G6 runs the real, banked DF Case I j=1
reproduction end to end and reports whether any number recorded in `capabilities.py` is
actually exposed by G1-G4.

Runtime ~270 s, dominated by G6's full 66-record branch continuation and its margin ladder.
Deterministic; no RNG anywhere.
"""

import json
import math
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import viscous_novelty as V                            # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_vna_v1_adversarial.json")

# DF Case I, branch j = 1 -- the module's own transcribed row (DF_TABLE1[0]).
D, SIGMA, XI1 = 1, 2.3, 10.0
MU, KAPPA = V.DF_TABLE1[0][1], V.DF_TABLE1[0][2]


def _j(x):
    """JSON-safe: NaN/inf become strings so the record is unambiguous."""
    if isinstance(x, (bool, str)) or x is None:
        return x
    x = float(x)
    if math.isnan(x):
        return "nan"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


def guarded(fn):
    """Call fn(); return {'outcome': 'value'|'raised', ...} plus any warnings raised."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            val = fn()
            out = {"outcome": "value", "value": val}
        except Exception as ex:                                    # noqa: BLE001
            out = {"outcome": "raised", "exception": type(ex).__name__, "message": str(ex)}
    out["warnings"] = sorted({str(x.message)[:90] for x in w})
    return out


# ---------------------------------------------------------------------------
# G1 -- the anti-dissipation guard, present in branch_in_kappa, absent in margin_law
# ---------------------------------------------------------------------------
def g1_antidissipation_guard():
    """margin_law calls solve_at_kappa directly and filters ONLY on hist[-1].

    `branch_in_kappa` filters on BOTH the residual and `-1e-6 <= eps < 1.0`, and its
    docstring says why.  `margin_law` re-solves at kappa* +/- offset with its own seeds and
    applies no eps test, so an offset that walks off the physical branch returns rows on the
    anti-dissipative continuation -- and those rows are fitted into the divergence exponent
    the function exists to report."""
    # a deliberately impoverished seed record set: legal in shape, far from the fold.
    seed_branch = [{"kappa": 0.85, "mu": MU, "eps": 0.0, "defect": 0.0, "converged": True},
                   {"kappa": 0.80, "mu": MU, "eps": 0.02, "defect": 0.0, "converged": True}]
    fold = {"eps_star": 0.06, "kappa_star": 0.5546}
    res = V.margin_law(seed_branch, fold, D, SIGMA, XI1, offsets=(0.08, 0.04))
    rows = []
    for r in res["rows"]:
        admissible = bool(-1e-6 <= r["eps"] < 1.0)
        rows.append({"kappa": _j(r["kappa"]), "offset": _j(r["offset"]),
                     "eps": _j(r["eps"]), "mu": _j(r["mu"]),
                     "Jinv_norm": _j(r["Jinv_norm"]), "cond": _j(r["cond"]),
                     "eps_admissible_by_branch_in_kappa_guard": admissible})
    rejected = [r for r in rows if not r["eps_admissible_by_branch_in_kappa_guard"]]
    return {
        "what": "margin_law accepts rows branch_in_kappa's own documented guard rejects",
        "module_sentence_relied_on": (
            "branch_in_kappa docstring: 'the map has other zeros (with negative eps, i.e. "
            "anti-dissipation) and a continuation that does not check will happily report "
            "them as branch points'"),
        "rows": rows,
        "n_rows_returned": len(rows),
        "n_rows_with_inadmissible_eps": len(rejected),
        "most_negative_eps": _j(min([r["eps"] for r in rows], default=float("nan"))),
        "slope_reported": _j(res.get("slope")),
        "slope_expected_by_module": _j(res.get("expected_slope")),
        "slope_misreport_factor": _j(abs(res["slope"] / res["expected_slope"])
                                     if res.get("slope") else float("nan")),
        "exception_raised": False,
        "silently_returned_wrong_value": bool(rejected),
    }


# ---------------------------------------------------------------------------
# G2 -- integrate_from_zero returns the initial condition for xi1 <= the series start
# ---------------------------------------------------------------------------
def g2_xi1_passthrough():
    """The loop is `while xi < xi1` from xi = 1e-8, so any xi1 <= 1e-8 -- including 0 and
    every negative value -- exits immediately and returns Q(1e-8) ~ mu, with n_steps = 0
    and no warning.  `match_defect` discards n_steps (the one available signal)."""
    Qref, dQref, nref = V.integrate_from_zero(MU, KAPPA, 0.0, D, SIGMA, 1.0)
    rows = []
    for xi1 in (1e-8, 0.0, -1.0, -1e6):
        Q, dQ, n = V.integrate_from_zero(MU, KAPPA, 0.0, D, SIGMA, xi1)
        rows.append({"xi1": _j(xi1), "Q_real": _j(Q.real), "Q_imag": _j(Q.imag),
                     "n_steps": n, "equals_initial_condition_mu": bool(abs(Q - MU) < 1e-15),
                     "abs_error_vs_honest_xi1_1": _j(abs(Q - Qref))})
    md = guarded(lambda: V.match_defect(MU, KAPPA, 0.0, D, SIGMA, 1e-9))
    if md["outcome"] == "value":
        defect, gamma, scale = md["value"]
        md_summary = {"outcome": "value", "abs_defect": _j(abs(defect)),
                      "scale": _j(scale), "relative": _j(abs(defect) / scale)}
    else:
        md_summary = md
    return {
        "what": "integrate_from_zero returns Q(origin) for any xi1 <= 1e-8, n_steps = 0",
        "module_sentence_relied_on": (
            "integrate_from_zero docstring: 'the initial-value problem Q(0) = mu, "
            "Q'(0) = 0, integrated to xi1'"),
        "honest_reference_xi1_1.0": {"Q_real": _j(Qref.real), "Q_imag": _j(Qref.imag),
                                     "n_steps": nref},
        "rows": rows,
        "match_defect_at_xi1_1e-9": md_summary,
        "exception_raised": False,
        "silently_returned_wrong_value": all(r["equals_initial_condition_mu"] for r in rows),
    }


# ---------------------------------------------------------------------------
# G3 -- compare_to_published_branch on a record list that ties in kappa
# ---------------------------------------------------------------------------
def g3_interp_tie():
    """`np.interp` requires strictly increasing x.  The module sorts (so ORDER is handled)
    but a TIE in kappa is not, and the tie's partner value is what gets returned."""
    clean = [{"kappa": k, "eps": e, "mu": 1.0, "defect": 0.0, "converged": True}
             for k, e in [(0.85, 0.001), (0.80, 0.020), (0.75, 0.036), (0.70, 0.047),
                          (0.65, 0.055), (0.60, 0.059), (0.55, 0.0606)]]
    base = V.compare_to_published_branch(clean)
    poisoned = clean + [{"kappa": 0.80, "eps": 0.99, "mu": 1.0, "defect": 0.0,
                         "converged": True}]
    hit = V.compare_to_published_branch(poisoned)
    worst = max(hit["rows"], key=lambda r: abs(r["diff"]))
    return {
        "what": "a duplicated kappa silently changes the published-agreement headline",
        "module_sentence_relied_on": (
            "compare_to_published_branch docstring: 'our sweep is monotone in kappa, so a "
            "plain interpolation is well-defined'"),
        "clean_max_abs_diff": _j(base["max_abs_diff"]),
        "clean_rms_diff": _j(base["rms_diff"]),
        "poisoned_max_abs_diff": _j(hit["max_abs_diff"]),
        "poisoned_rms_diff": _j(hit["rms_diff"]),
        "inflation_factor": _j(hit["max_abs_diff"] / base["max_abs_diff"]),
        "worst_row": {k: _j(v) for k, v in worst.items()},
        "exception_raised": False,
        "silently_returned_wrong_value": hit["max_abs_diff"] > 10 * base["max_abs_diff"],
    }


# ---------------------------------------------------------------------------
# G4 -- the ledger's verdict vocabulary is unenforced
# ---------------------------------------------------------------------------
def g4_verdict_vocabulary():
    """`novelty_verdict` selects on the exact string "PRE_EMPTS".  Nothing validates that a
    ledger entry's verdict is one of the three documented values, so a one-character typo
    flips the stage-V gate answer with no error."""
    saved = V.PRECEDENTS
    try:
        baseline = V.novelty_verdict()[0]
        V.PRECEDENTS = [dict(p) for p in saved]
        V.PRECEDENTS[0]["verdict"] = "PRE-EMPTS"          # hyphen, not underscore
        typo = V.novelty_verdict()[0]
        V.PRECEDENTS = [dict(p) for p in saved]
        del V.PRECEDENTS[0]["verdict"]
        missing = guarded(lambda: V.novelty_verdict()[0])
    finally:
        V.PRECEDENTS = saved
    return {
        "what": "one character in a ledger verdict flips stage V's gate answer",
        "documented_vocabulary": ["PRE_EMPTS", "ADJACENT", "EXCLUSION"],
        "baseline_gate_answer": baseline,
        "typo_gate_answer": typo,
        "gate_answer_flipped": bool(baseline != typo),
        "missing_key_behaviour": missing,
        "restored_gate_answer": V.novelty_verdict()[0],
        "exception_raised": False,
        "silently_returned_wrong_value": bool(baseline != typo),
    }


# ---------------------------------------------------------------------------
# G5 -- LESSON 90: the guards in this module that DO fire
# ---------------------------------------------------------------------------
def g5_positive_controls():
    """Every "no guard here" claim above must sit beside a "guard here, and it fired" case
    from the same module.  These are those cases, and each could report the other answer."""
    controls = {
        "kappa_zero_asymptotic_coefficients":
            guarded(lambda: V.asymptotic_coefficients(1.0, 0.0, 0.0, D, SIGMA)[0].real),
        "dimension_zero_integrate_from_zero":
            guarded(lambda: V.integrate_from_zero(MU, KAPPA, 0.0, 0, SIGMA, 1.0)[2]),
        "steps_per_osc_zero":
            guarded(lambda: V.integrate_from_zero(MU, KAPPA, 0.0, D, SIGMA, 1.0,
                                                  steps_per_osc=0)[2]),
        "margin_law_nan_seed_row":
            guarded(lambda: V.margin_law(
                [{"kappa": 0.5546, "mu": float("nan"), "eps": 0.06, "defect": 0.0,
                  "converged": True}],
                {"eps_star": 0.06, "kappa_star": 0.5546}, D, SIGMA, XI1,
                offsets=(0.02, 0.01))["slope"]),
    }
    nan_branch = V.branch_in_kappa(float("nan"), 0.85, 0.83, D, SIGMA, XI1, dkappa=0.01)
    controls["branch_in_kappa_nan_seed"] = {
        "outcome": "value",
        "n_records": len(nan_branch),
        "n_converged": int(sum(r["converged"] for r in nan_branch)),
        "rejected_all": bool(not any(r["converged"] for r in nan_branch)),
        "warnings": [],
    }
    # fold_of on degenerate parabolas -- tested, and it behaves
    degenerate = {}
    for name, kv in {"collinear": [(0.50, 0.010), (0.51, 0.020), (0.52, 0.030), (0.53, 0.020)],
                     "tiny_curvature": [(0.50, 0.0100000), (0.51, 0.0100001),
                                        (0.52, 0.0100000)]}.items():
        b = [{"kappa": k, "eps": e, "mu": 1.0, "defect": 0.0, "converged": True}
             for k, e in kv]
        f = V.fold_of(b)
        lo, hi = min(k for k, _ in kv), max(k for k, _ in kv)
        degenerate[name] = {"kappa_star": _j(f.get("kappa_star")),
                            "eps_star": _j(f.get("eps_star")),
                            "interior": f.get("interior"),
                            "vertex_inside_bracket": bool(lo <= f["kappa_star"] <= hi)}
    flat = [{"kappa": 0.5 + 0.01 * i, "eps": 0.05, "mu": 1.0, "defect": 0.0,
             "converged": True} for i in range(5)]
    degenerate["flat_eps_endpoint_maximum"] = {
        "interior": V.fold_of(flat)["interior"],
        "honestly_flagged_non_interior": V.fold_of(flat)["interior"] is False}
    n_fire = sum(1 for c in controls.values() if c["outcome"] == "raised"
                 or c.get("rejected_all"))
    return {"what": "guards in the same module that fire, and could have come out otherwise",
            "controls": controls, "n_controls": len(controls), "n_that_fired": n_fire,
            "fold_of_degenerate_inputs": degenerate}


# ---------------------------------------------------------------------------
# G6 -- LATENCY: is anything banked in capabilities.py actually exposed?
# ---------------------------------------------------------------------------
def g6_latency_real_pipeline():
    """The real DF Case I j=1 reproduction, end to end, on the module's own transcribed
    row.  If this is clean, G1-G4 are latent: real defects, but not reached by the banked
    computation.  That distinction is the whole difference between 'escalate a repair' and
    'the recorded numbers are wrong'."""
    t0 = time.time()
    branch = V.branch_in_kappa(MU, KAPPA, 0.20, D, SIGMA, XI1, dkappa=0.01)
    rec = [r for r in branch if r["converged"]]
    fold = V.fold_of(branch)
    cmp_ = V.compare_to_published_branch(branch)
    ml = V.margin_law(branch, fold, D, SIGMA, XI1)
    inadmissible = [r for r in ml["rows"] if not (-1e-6 <= r["eps"] < 1.0)]
    pub = V.DF_FIG1A_BRANCH1_FOLD
    return {
        "what": "the banked reproduction, run under the same conditions capabilities.py cites",
        "runtime_s": _j(time.time() - t0),
        "branch": {"n_records": len(branch), "n_converged": len(rec),
                   "all_converged": bool(len(rec) == len(branch)),
                   "eps_min": _j(min(r["eps"] for r in rec)),
                   "eps_max": _j(max(r["eps"] for r in rec)),
                   "all_eps_admissible": bool(all(-1e-6 <= r["eps"] < 1.0 for r in rec))},
        "fold": {"eps_star": _j(fold["eps_star"]), "kappa_star": _j(fold["kappa_star"]),
                 "interior": fold["interior"],
                 "published_eps_star": _j(pub["eps_star"]),
                 "abs_diff_eps_star": _j(abs(fold["eps_star"] - pub["eps_star"])),
                 "abs_diff_kappa_star": _j(abs(fold["kappa_star"] - pub["kappa_star"]))},
        "compare_to_published": {"n": cmp_["n"], "max_abs_diff": _j(cmp_["max_abs_diff"]),
                                 "rms_diff": _j(cmp_["rms_diff"])},
        "margin_law": {"n_rows": len(ml["rows"]), "slope": _j(ml["slope"]),
                       "expected_slope": _j(ml["expected_slope"]),
                       "n_rows_with_inadmissible_eps": len(inadmissible)},
        "any_banked_number_exposed": bool(inadmissible) or len(rec) != len(branch),
    }


# ---------------------------------------------------------------------------
# G7 -- the integrator's only termination lever, measured not executed to failure
# ---------------------------------------------------------------------------
def g7_step_cap_termination():
    """h = min(hmax, period_step, xi1 - xi).  For hmax <= 0 the step is <= 0 and xi never
    advances -- the loop cannot terminate.  Demonstrated by evaluating the loop's own first
    step rather than by running it, so this battery always terminates."""
    rows = []
    for hmax in (1e-2, 1e-3, 1e-4):
        t0 = time.time()
        _, _, n = V.integrate_from_zero(MU, KAPPA, 0.0, D, SIGMA, 1.0, hmax=hmax)
        rows.append({"hmax": _j(hmax), "n_steps": n, "seconds": _j(time.time() - t0)})
    xi = 1e-8
    first = {}
    for hmax in (0.0, -1e-3):
        period_step = 2.0 * np.pi / max(KAPPA * xi, 1e-12) * (40.0 / 200)
        h = min(hmax, period_step, 1.0 - xi)
        first[str(hmax)] = {"h": _j(h), "xi_advances": bool(xi + h > xi)}
    return {"what": "step count scales as 1/hmax; hmax <= 0 cannot terminate",
            "rows": rows, "first_step_at_nonpositive_hmax": first,
            "terminates_for_nonpositive_hmax": False,
            "kind": "non-termination, NOT a silent wrong value"}


def main():
    t0 = time.time()
    gates = {}
    gates["G1_antidissipation_guard_missing_in_margin_law"] = g1_antidissipation_guard()
    gates["G2_integrate_from_zero_xi1_passthrough"] = g2_xi1_passthrough()
    gates["G3_compare_to_published_branch_interp_tie"] = g3_interp_tie()
    gates["G4_ledger_verdict_vocabulary_unenforced"] = g4_verdict_vocabulary()
    gates["G5_positive_controls"] = g5_positive_controls()
    gates["G6_latency_real_pipeline"] = g6_latency_real_pipeline()
    gates["G7_step_cap_termination"] = g7_step_cap_termination()

    silent = [k for k, v in gates.items() if v.get("silently_returned_wrong_value")]
    doc = {
        "leg": 143,
        "route": "ROUTE-VNA",
        "module_under_audit": "solver/viscous_novelty.py",
        "module_edited_by_this_leg": False,
        "gate": ("Under adversarial and degenerate inputs, does viscous_novelty.py ever "
                 "silently return a wrong value rather than reject or visibly propagate "
                 "the defect?"),
        "gate_answer": "YES" if silent else "NO",
        "silent_corruption_sites": silent,
        "n_silent_corruption_sites": len(silent),
        "banked_numbers_exposed": gates["G6_latency_real_pipeline"]["any_banked_number_exposed"],
        "disposition": ("ESCALATED, NOT PATCHED -- the gate's yes-branch withholds patch "
                        "authority from this leg" if silent else "battery banked"),
        "gates": gates,
        "runtime_s": _j(time.time() - t0),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print(f"gate answer: {doc['gate_answer']}  "
          f"silent-corruption sites: {len(silent)}  "
          f"banked numbers exposed: {doc['banked_numbers_exposed']}")
    for k in silent:
        print(f"  - {k}")
    print(f"wrote {OUT} in {doc['runtime_s']:.1f}s")


if __name__ == "__main__":
    main()
