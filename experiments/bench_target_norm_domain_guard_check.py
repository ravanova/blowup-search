"""BENCH REPAIR CHECK -- does the domain guard change any number leg 55 banked?

Not a leg.  This is the verification half of the bench repair that added a domain guard to
`solver/target_norm.py` after leg 84 (Route-TNA) measured the module returning
untrustworthy exponents in silence.  It answers exactly two questions, and it edits
nothing that belongs to leg 55:

  A. **ZERO REGRESSION.**  For a battery of in-window and out-of-window calls, is every
     number the patched module returns bit-identical to the number the pre-patch module
     returned?  The pre-patch module is loaded straight out of git
     (`git show <BASE>:solver/target_norm.py`) and imported alongside the patched one, so
     this is a real A/B and not a re-reading of the same code.  The guard is supposed to
     add fields and a warning and to compute NOTHING.

  B. **IS LEG 55'S BANKED FINDING CONTAMINATED?**  Leg 55 banked `HL_S2_nonsymmetric`
     having finite l^1_w norm at `s = 0` (margin +0.394) and `s = 0.3` (margin +0.094).
     That finding is cited by other legs, so the question the orchestrator needs answered
     is whether those two margins were computed from the 14 contaminated theta-samples.
     This re-runs leg 55's OWN `nb5_norms` path -- its own `solve_target` and `_measure`,
     imported from `experiments/p2_route_nb_v1_targetnorm.py`, not reimplemented -- with
     the guard active, at leg 55's headline domain `rho_max = 12` AND at the shipped
     `rho_max = 8`, and prints `domain_valid` next to every margin.

The counterfactual matters as much as the replication: if the two domains give the same
verdict, the finding is safe *and* we know by how much it was safe.
"""

import json
import os
import subprocess
import sys
import types
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from solver import target_norm as patched                                 # noqa: E402
from solver.hl_rescaled import sinh_grid_origin                           # noqa: E402
from solver.target_norm import TargetNormDomainWarning                    # noqa: E402
from p2_route_nb_v1_targetnorm import (                                   # noqa: E402
    BAND, S_VALUES, _measure, solve_target,
)

OUT = os.path.join(ROOT, "writeup", "data", "bench_target_norm_domain_guard_check.json")

# the commit the repair is based on -- leg 84's tip, i.e. the module BEFORE the guard
BASE = os.environ.get("BENCH_BASE_REF", "origin/leg/tna-v1")

# leg 55's two banked margins, transcribed from writeup/data/p2_route_nb_v1_targetnorm.json
# (NB5_norms.classes[*].verdict.margin_in_exponent_units).  Read, never written.
LEG55_BANKED = {0.0: 0.39374453128859876, 0.3: 0.09374453128859872}
LEG55_BANKED_P = 1.3937445312885988
LEG55_HEADLINE_RHO_MAX = 12.0        # nb5_norms(n=801, rho_max=12.0)
LEG55_SHIPPED_RHO_MAX = 8.0          # the domain where the 14 samples fall outside


def load_prepatch():
    """Import the PRE-guard solver/target_norm.py out of git as a separate module."""
    src = subprocess.run(["git", "show", f"{BASE}:solver/target_norm.py"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType("target_norm_prepatch")
    mod.__file__ = f"<{BASE}:solver/target_norm.py>"
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, src


# --------------------------------------------------------------------------
# A -- zero regression, A/B against the module as it stood before the guard
# --------------------------------------------------------------------------
def part_a(old):
    """Every returned NUMBER must be bit-identical; only new KEYS may appear."""
    alpha, tail, M, band = 0.4, -0.4, 16384, BAND
    _, X745 = sinh_grid_origin(801, rho_max=8.0)
    _, XBIG = sinh_grid_origin(801, rho_max=12.0)
    cases = []
    for label, X, ff, te in (
            ("in-window   rho_max=12, power", XBIG, "power", tail),
            ("out-of-window rho_max=8, power", X745, "power", tail),
            ("out-of-window rho_max=8, clamp", X745, "clamp", None),
            ("out-of-window rho_max=8, zero", X745, "zero", None),
    ):
        f_new = patched.calibration_family(X, alpha)
        f_old = old.calibration_family(X, alpha)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", TargetNormDomainWarning)
            sp_n = patched.spectrum(X, f_new, M=M, far_field=ff, tail_exponent=te)
            fit_n = patched.fit_exponent(sp_n["k"], sp_n["hk"], *band,
                                         n_outside_grid=sp_n["n_outside_grid"])
            ps_n = patched.weighted_partial_sums(sp_n["k"], sp_n["hk"], 0.3, [512, 4096],
                                                 n_outside_grid=sp_n["n_outside_grid"])
            at_n = patched.analytic_tail(fit_n["p"], fit_n["C"], 4096, 0.3,
                                         n_outside_grid=sp_n["n_outside_grid"])
            nv_n = patched.norm_verdict(fit_n["p"], 0.3,
                                        n_outside_grid=sp_n["n_outside_grid"])
        sp_o = old.spectrum(X, f_old, M=M, far_field=ff, tail_exponent=te)
        fit_o = old.fit_exponent(sp_o["k"], sp_o["hk"], *band)
        ps_o = old.weighted_partial_sums(sp_o["k"], sp_o["hk"], 0.3, [512, 4096])
        at_o = old.analytic_tail(fit_o["p"], fit_o["C"], 4096, 0.3)
        nv_o = old.norm_verdict(fit_o["p"], 0.3)

        # every key the OLD module returned must still be present and bit-identical
        def cmp(a, b):
            bad = []
            for key, vo in b.items():
                vn = a.get(key, "<MISSING>")
                same = (np.array_equal(vn, vo) if isinstance(vo, np.ndarray)
                        else (vn is vo or vn == vo
                              or (isinstance(vo, float) and isinstance(vn, float)
                                  and np.isnan(vo) and np.isnan(vn))))
                if not same:
                    bad.append((key, vo, vn))
            return bad

        diffs = (cmp(sp_n, sp_o) + cmp(fit_n, fit_o) + cmp(at_n, at_o) + cmp(nv_n, nv_o)
                 + [d for i in range(2) for d in cmp(ps_n[i], ps_o[i])])
        cases.append({
            "case": label, "far_field": ff,
            "n_outside_grid": int(sp_n["n_outside_grid"]),
            "domain_valid": sp_n["domain_valid"],
            "p_prepatch": float(fit_o["p"]), "p_patched": float(fit_n["p"]),
            "p_bit_identical": bool(float(fit_o["p"]) == float(fit_n["p"])),
            "margin_prepatch": float(nv_o["margin_in_exponent_units"]),
            "margin_patched": float(nv_n["margin_in_exponent_units"]),
            "n_value_differences": len(diffs),
            "differences": [[k, repr(a), repr(b)] for k, a, b in diffs],
            "new_keys_spectrum": sorted(set(sp_n) - set(sp_o)),
            "new_keys_fit_exponent": sorted(set(fit_n) - set(fit_o)),
        })
    return {"what": ("A/B of the patched module against the pre-guard module loaded from "
                     f"git {BASE}; every value the old module returned must be "
                     "bit-identical, only new keys may appear"),
            "cases": cases,
            "n_cases": len(cases),
            "n_cases_with_any_value_difference": sum(
                1 for c in cases if c["n_value_differences"]),
            "all_bit_identical": all(not c["n_value_differences"] for c in cases)}


# --------------------------------------------------------------------------
# B -- leg 55's own measurement, re-run with the guard on
# --------------------------------------------------------------------------
def rerun_leg55(rho_max, n=801):
    """Leg 55's nb5_norms path verbatim -- its solve, its _measure, its S_VALUES."""
    warned = []
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        s = solve_target(n, rho_max=rho_max)
        sp, fit = _measure(s["b"].X, s["Omega"], s["c_omega"] / s["c_l"])
        k, hk = sp["k"], sp["hk"]
        p, C = fit["p"], fit["C"]
        n_out = int(sp["n_outside_grid"])
        classes = []
        for sv in S_VALUES:
            ps = patched.weighted_partial_sums(k, hk, sv, [16, 64, 256, 1024, 4096],
                                               n_outside_grid=n_out)
            tail = patched.analytic_tail(p, C, 4096, sv, n_outside_grid=n_out)
            v = patched.norm_verdict(p, sv, alpha=s["alpha"], n_outside_grid=n_out)
            classes.append({"s": float(sv), "verdict": v, "analytic_tail": tail,
                            "S_N_at_4096": ps[-1]["S_N"],
                            "norm_upper_bound": (None if not tail["finite"]
                                                 else float(ps[-1]["S_N"]
                                                            + tail["bound"]))})
        warned = [str(x.message) for x in w
                  if issubclass(x.category, TargetNormDomainWarning)]
    return {"rho_max": float(rho_max), "n": int(n),
            "X_max": float(np.abs(s["b"].X).max()),
            "alpha": float(s["alpha"]), "p": float(p), "C": float(C),
            "converged": bool(s["converged"]), "residual": float(s["residual"]),
            "n_theta_points_outside_grid": n_out,
            "domain_valid": sp["domain_valid"],
            "n_domain_warnings_raised": len(warned),
            "first_warning": warned[0] if warned else None,
            "classes": classes}


def part_b():
    head = rerun_leg55(LEG55_HEADLINE_RHO_MAX)
    ship = rerun_leg55(LEG55_SHIPPED_RHO_MAX)
    rows = []
    for sv in (0.0, 0.3):
        ch = next(c for c in head["classes"] if c["s"] == sv)
        cs = next(c for c in ship["classes"] if c["s"] == sv)
        banked = LEG55_BANKED[sv]
        got = float(ch["verdict"]["margin_in_exponent_units"])
        rows.append({
            "s": sv,
            "leg55_banked_margin": banked,
            "rerun_margin_at_leg55_headline_domain": got,
            "abs_difference_vs_banked": abs(got - banked),
            "reproduces_banked_margin": bool(abs(got - banked) < 1e-12),
            "headline_domain_valid": ch["verdict"]["domain_valid"],
            "headline_finite": bool(ch["verdict"]["finite"]),
            "counterfactual_margin_at_shipped_745_domain": float(
                cs["verdict"]["margin_in_exponent_units"]),
            "counterfactual_domain_valid": cs["verdict"]["domain_valid"],
            "counterfactual_finite": bool(cs["verdict"]["finite"]),
            "margin_cost_of_the_contaminated_domain": float(
                got - cs["verdict"]["margin_in_exponent_units"]),
            "verdict_would_have_flipped": bool(
                ch["verdict"]["finite"] != cs["verdict"]["finite"]),
        })
    return {
        "what": ("leg 55's nb5_norms re-run with the guard active, at its own headline "
                 "domain (rho_max = 12) and, as a counterfactual, at the shipped "
                 "rho_max = 8 domain where 14 theta-samples fall outside the data"),
        "leg55_headline_run": head,
        "shipped_domain_counterfactual": ship,
        "margins": rows,
        "leg55_headline_is_clean": bool(head["n_theta_points_outside_grid"] == 0
                                        and head["domain_valid"] is True),
        "leg55_banked_p": LEG55_BANKED_P,
        "rerun_p_at_headline": head["p"],
        "p_reproduces": bool(abs(head["p"] - LEG55_BANKED_P) < 1e-12),
        "any_banked_margin_changed": bool(
            any(not r["reproduces_banked_margin"] for r in rows)),
        "any_verdict_would_have_flipped": bool(
            any(r["verdict_would_have_flipped"] for r in rows)),
    }


def main():
    old, _src = load_prepatch()
    pay = {"what": "bench repair check: solver/target_norm.py domain guard",
           "not_a_leg": True, "base_ref_for_prepatch_module": BASE,
           "A_zero_regression": part_a(old)}
    print("A: zero-regression A/B done.", flush=True)
    pay["B_leg55_contamination_check"] = part_b()
    a, b = pay["A_zero_regression"], pay["B_leg55_contamination_check"]
    pay["headline"] = {
        "guard_changes_no_number": a["all_bit_identical"],
        "leg55_headline_domain_had_zero_samples_outside":
            b["leg55_headline_is_clean"],
        "leg55_banked_margins_reproduce_exactly": not b["any_banked_margin_changed"],
        "leg55_needs_a_rework_leg": bool(b["any_banked_margin_changed"]
                                         or not b["leg55_headline_is_clean"]),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(pay, fh, indent=2, default=float)
    print(json.dumps(pay["headline"], indent=2))
    print(json.dumps(b["margins"], indent=2))
    print(f"\nwrote {OUT}")
    return pay


if __name__ == "__main__":
    main()
