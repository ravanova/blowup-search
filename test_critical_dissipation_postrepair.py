"""Leg 170 (Route-CDB) -- leg 121's battery, BANKED as a permanent regression suite.

Run:  .venv/bin/python test_critical_dissipation_postrepair.py       (~90 s)

WHAT THIS FILE IS FOR, AND WHY IT IS NOT test_critical_dissipation_adversarial.py
---------------------------------------------------------------------------------
`test_critical_dissipation_adversarial.py` was rewritten inside leg 154's own repair
commit (`87d6904`, +206/-48 lines), converting leg 121's characterization pins into
soundness pins.  That is a legitimate pin and it is not duplicated here.  What it cannot
be is INDEPENDENT of the repair: the same leg wrote the guard, the driver that graded the
guard, and the test that pins the grade.

This file is the independent one.  Every non-integer case below is reconstructed from
leg 121's OWN banked record (`writeup/data/p2_route_cda_v1_adversarial.json`), never from
leg 154's `A_clause_a_refusals`, and every refusal is asserted PER CASE and PER ENTRY
POINT rather than as an aggregate -- because leg 147 found a landed, merged,
ledger-blessed repair whose "17 of 21 now reject" hid one surviving case that returned no
signal of any kind.

`test_2` is the negative control that keeps this file honest (lesson 90): the SAME
harness, bound to the pre-repair module read out of git at `9dba93f`, must still report
every one of those cases SILENTLY TRUNCATED.  If it ever stops doing so, the pre-repair
module is not loading, the differential is a module compared with itself, and every other
test here is vacuous.

`test_3` is the other direction: leg 121's sub-integer cases were ALREADY refused before
the repair, by `lambda_power`'s `p < 1` check.  A case the old code already refused is not
evidence for the new guard, so they are counted separately and never folded into the
headline -- and they must stay `ValueError` for leg 121's own `except ValueError` control.

`test_7` pins the KNOWN GAPS as characterizations, not soundness claims: they are
measured, banked and deliberately NOT repaired under leg 170's authority (its gate forbids
patching on both branches).  A future repair must invert them consciously.

READ-ONLY.  `solver/critical_dissipation.py` is not edited by leg 170 under either branch.
Full measurement: `experiments/p2_route_cdb_v1_postrepair.py` /
`writeup/data/p2_route_cdb_v1_postrepair.json`.
"""

import json
import os
import sys
import warnings

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from experiments.p2_route_cdb_v1_postrepair import (   # noqa: E402
    LEG121_JSON, PRE_REPAIR_SHA, _entry_points, _probe, compare,
    leg121_noninteger_cases, load_pre_repair, r1_finding_legs_driver_still_runs,
    r4_escape_hatch_reproduces_leg121)

import solver.critical_dissipation as CD               # noqa: E402

PASS, FAIL = [], []

_rng = np.random.default_rng(20250806)
B_SEED = _rng.standard_normal(200) * 0.3
B_SEED[0] = -1.0


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   {detail}")


# ---------------------------------------------------------------------------
def test_1_every_noninteger_case_refused_at_every_entry_point():
    print("\n[1] clause (a): leg 121's non-integer cases x every public entry point")
    new, _already = leg121_noninteger_cases()
    eps = _entry_points(CD, B_SEED)
    cells, refused, domain, silent = 0, 0, 0, []
    for c in new:
        for name, fn in eps.items():
            r = _probe(fn, c["p"])
            cells += 1
            refused += int(r["refused"])
            domain += int(r["is_domain_error"])
            if not r["refused"] and r["n_warnings"] == 0:
                silent.append((c["p"], name))
    print(f"      {len(new)} cases x {len(eps)} entry points = {cells} cells "
          f"({', '.join(sorted(eps))})")
    check("0 cells silently accept a non-integer exponent", not silent,
          f"{len(silent)} silent" + (f": {silent[:4]}" if silent else ""))
    check("every case x entry-point cell refuses", refused == cells,
          f"{refused}/{cells}")
    check("every refusal is the NEW guard, not the pre-existing p<1 ValueError",
          domain == cells, f"{domain}/{cells} CriticalDissipationDomainError")
    check("every refusal is still a ValueError (leg 121's own control catches it)",
          all(_probe(fn, c["p"])["is_ValueError"] for c in new for fn in eps.values()))


def test_2_negative_control_pre_repair_module_still_truncates():
    print(f"\n[2] NEGATIVE CONTROL (lesson 90): pre-repair module at git {PRE_REPAIR_SHA}")
    PRE, _src = load_pre_repair()
    new, _already = leg121_noninteger_cases()
    eps = _entry_points(PRE, B_SEED)
    truncated = 0
    for c in new:
        r = _probe(eps["lambda_power"], c["p"])
        if not r["refused"] and r["n_warnings"] == 0:
            truncated += 1
    check("the pre-repair module SILENTLY truncates every one of the same cases",
          truncated == len(new), f"{truncated}/{len(new)} silent pre-repair")
    check("the two modules are distinguishable objects (else the differential is a "
          "tautology)", PRE is not CD and not hasattr(PRE, "_validated_p"))
    # leg 121's headline, end to end, off the pre-repair module
    rows = PRE.mu_branch(0.0, 1.9, [0.0, 0.05, 0.1], K=64)
    sl = PRE.alpha_slope(rows)
    banked = [r for r in json.loads(LEG121_JSON.read_text())
              ["C2_flow_identity_under_truncation"]["rows"] if r["p_requested"] == 1.9][0]
    check("pre-repair reproduces leg 121's banked residual/alpha/alpha_1 bit-identically",
          rows[-1]["residual"] == banked["residual_fake"]
          and rows[-1]["alpha"] == banked["alpha_fake"]
          and sl["alpha_1"] == banked["alpha_1_fake"],
          f"residual {rows[-1]['residual']!r}, alpha_1 {sl['alpha_1']!r}")


def test_3_already_refused_cases_are_counted_separately():
    print("\n[3] the cases the OLD p<1 check already refused (NOT evidence for the guard)")
    new, already = leg121_noninteger_cases()
    PRE, _src = load_pre_repair()
    for c in already:
        pre_r = _probe(_entry_points(PRE, B_SEED)["lambda_power"], c["p"])
        post_r = _probe(_entry_points(CD, B_SEED)["lambda_power"], c["p"])
        check(f"p = {c['p']} refused BEFORE and AFTER, both ValueError",
              pre_r["refused"] and post_r["refused"]
              and pre_r["is_ValueError"] and post_r["is_ValueError"],
              f"{pre_r['exc_class']} -> {post_r['exc_class']}")
    check("the headline count excludes them", len(already) > 0
          and all(c["p"] not in [n["p"] for n in new] for c in already),
          f"{len(new)} new-guard cases, {len(already)} pre-existing refusals")


def test_4_non_finite_p_is_a_ValueError_not_an_OverflowError():
    print("\n[4] leg 121's prescribed predicate's blind spot stays closed")
    PRE, _src = load_pre_repair()
    for p in (float("inf"), float("-inf"), float("nan")):
        post = _probe(_entry_points(CD, B_SEED)["lambda_power"], p)
        pre = _probe(_entry_points(PRE, B_SEED)["lambda_power"], p)
        check(f"p = {p!r} refused as a ValueError (was {pre['exc_class']})",
              post["refused"] and post["is_ValueError"] and post["is_domain_error"],
              f"{pre['exc_class']} -> {post['exc_class']}")
    check("np.floor(inf) == inf, so an integrality-only predicate is BLIND to it "
          "(why the finiteness clause runs first)", np.floor(np.inf) == np.inf)


def test_5_escape_hatch_reproduces_leg121_end_to_end():
    print("\n[5] leg 135's rule: the record that authorised the repair stays runnable")
    PRE, _src = load_pre_repair()
    r4 = r4_escape_hatch_reproduces_leg121(PRE)
    # The comparison that can SEE the repair: same interpreter, same NumPy/BLAS.
    check("the hatch reproduces the PRE-REPAIR module's (residual, alpha, alpha_1) triple "
          "bit-identically, in process, on every one of leg 121's C2 rows",
          r4["n_rows_hatch_matches_pre_repair_in_process"] == r4["n_rows"],
          f"{r4['n_rows_hatch_matches_pre_repair_in_process']}/{r4['n_rows']} rows")
    # The banked JSON is a DRIFTED reference, and this is the check that proves it is
    # drift rather than the repair: the pre-repair module misses its own banked value too.
    check("KNOWN GAP: leg 121's banked JSON no longer reproduces bitwise on today's "
          "NumPy/BLAS -- the PRE-REPAIR module misses it by the same amount, so it is "
          "environmental drift and not the repair",
          r4["n_rows_PRE_REPAIR_matches_banked_json"] == r4["n_rows_hatch_matches_banked_json"],
          f"pre-repair {r4['n_rows_PRE_REPAIR_matches_banked_json']}/{r4['n_rows']} vs "
          f"hatch {r4['n_rows_hatch_matches_banked_json']}/{r4['n_rows']}, worst "
          f"{r4['worst_ulp_pre_repair_vs_banked']} ULP")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        CD.lambda_power(8, 1.9, on_noninteger="truncate")
    check("the hatch warns, names the substitution, and is a RuntimeWarning",
          len(w) == 1 and issubclass(w[0].category, RuntimeWarning)
          and "truncating to 1" in str(w[0].message))
    check("the hatch is NOT the default -- the same call without it raises",
          _probe(lambda p: CD.lambda_power(8, p), 1.9)["is_domain_error"])


def test_6_integer_p_results_are_bit_identical():
    print("\n[6] clause (b): integer-p differential against the pre-repair module")
    PRE, _src = load_pre_repair()
    results = []

    def q(name, fn):
        results.append(compare(name, fn(PRE), fn(CD)))

    q("lambda_block", lambda m: {str(n): m.lambda_block(n) for n in (1, 2, 5, 17, 33)})
    q("lambda_power", lambda m: {f"K{K}p{p}": list(m.lambda_power(K, p))
                                 for K in (4, 9, 23, 48) for p in (1, 2, 3, 5)})
    q("integral_float_types",
      lambda m: {f"{p!r}": list(m.lambda_power(9, p))
                 for p in (3, 3.0, np.float64(3.0), np.int64(3), True)})
    q("lambda_truncation", lambda m: {f"K{K}p{p}": m.lambda_truncation(B_SEED[:K], K, p)
                                      for K in (9, 23) for p in (1, 2, 3)})
    q("exact_a0_family", lambda m: {str(mu): list(m.exact_a0_family(mu, np.linspace(-7, 7, 81)))
                                    for mu in (0.0, 0.13, 0.5)})
    q("exact_a0_residual",
      lambda m: {f"{nu}": m.exact_a0_residual(np.linspace(-4, 4, 61), 0.0, nu, 0.5)
                 for nu in (0.01, 0.5)})
    q("amplitude_eigenvalue", lambda m: m.amplitude_eigenvalue(np.linspace(0, 2, 21)))
    q("CRITICAL_POINTS", lambda m: [dict(x) for x in m.CRITICAL_POINTS])

    def flow(m):
        out = {}
        for a in (0.0, 0.17):
            for K in (23, 48):
                for p in (1, 3):
                    for mu in (0.0, 0.09):
                        f = m.CriticalDissipativeFlow(a, mu=mu, p=p, K=K)
                        b = B_SEED[:K]
                        out[f"{a}|{K}|{p}|{mu}"] = {
                            "p": f.p, "s": f.s, "Lp": f.Lp, "Lam": f.Lam,
                            "lam_dx0": f.lam_dx0, "c_omega": f.c_omega(b),
                            "residual": f.residual(b), "jacobian": f.jacobian(b),
                            "alpha": f.alpha(b), "generator": f.generator(b)}
        return out
    q("CriticalDissipativeFlow_surface", flow)

    def branch(m):
        rows = m.mu_branch(0.0, 1, [0.0, 0.05, 0.1], K=64)
        sl = m.alpha_slope(rows)
        return {"rows": [{k: v for k, v in r.items() if k != "b"} for r in rows],
                "b": rows[-1]["b"], "slope": sl,
                "verdict": m.marginal_verdict(sl["alpha_1"])}
    q("mu_branch_alpha_slope", branch)

    n = sum(r["n"] for r in results)
    nm = sum(r["n_moved"] for r in results)
    print(f"      {n} leaves over {len(results)} named quantities")
    check("0 integer-p leaves moved (== on float64, NOT allclose; NaN==NaN identical)",
          nm == 0, f"{n - nm}/{n} bit-identical, {nm} moved")
    for r in results:
        if r["n_moved"]:
            print(f"        MOVED in {r['quantity']}: {r['moved'][:3]}")
    check("the differential actually compared something", n > 100_000, f"{n} leaves")


def test_7_known_gaps_pinned_as_characterizations_not_soundness():
    print("\n[7] KNOWN GAPS -- measured, banked, deliberately NOT repaired by leg 170")

    r1 = r1_finding_legs_driver_still_runs()
    check("KNOWN GAP: leg 121's OWN driver still aborts against the repaired module "
          f"({r1['n_sections_completed']}/{r1['n_sections_total']} sections)",
          not r1["completed"] and r1["n_sections_completed"] < r1["n_sections_total"],
          f"aborts in {r1['abort_in_section']}, rc={r1['returncode']}")

    f = CD.CriticalDissipativeFlow(0.0, mu=-0.5, p=1, K=16)
    check("KNOWN GAP (leg 121 C5): mu < 0 still accepted unguarded", f.mu == -0.5)
    check("KNOWN GAP (leg 121 C6): mu_decay_time takes a negative target silently",
          np.isfinite(CD.mu_decay_time(1.0, 0.1, -1.0)))
    check("KNOWN GAP (leg 121 C7): marginal_verdict on NaN returns a sentence",
          isinstance(CD.marginal_verdict(float("nan")), str))
    check("KNOWN GAP (leg 121 C8): amplitude_eigenvalue(mu<0) unguarded",
          np.isnan(CD.amplitude_eigenvalue(-1.0)) or np.isreal(CD.amplitude_eigenvalue(-1.0)))
    check("KNOWN GAP (leg 154's declared residue): p = 1e300 is finite and integral, "
          "so the guard admits it", CD._validated_p(1e300) > 0)

    try:
        from solver.marginal_flow import AugmentedFlow
        g = AugmentedFlow(0.0, p=1.9)
        reached = False
        built = int(getattr(g, "p", -1))
    except ValueError:
        reached, built = True, None
    check("KNOWN GAP (leg 154's declared residue, out of territory): the IDENTICAL "
          "int(p) one level up truncates before the guard is reached",
          not reached, f"AugmentedFlow(0.0, p=1.9) builds p = {built}")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 74)
    print("leg 170 (Route-CDB) -- leg 121's battery as a permanent regression suite")
    print("=" * 74)
    print(f"case list source: {LEG121_JSON.name} (leg 121's OWN record)")
    print(f"negative control module: git {PRE_REPAIR_SHA}:solver/critical_dissipation.py")
    test_1_every_noninteger_case_refused_at_every_entry_point()
    test_2_negative_control_pre_repair_module_still_truncates()
    test_3_already_refused_cases_are_counted_separately()
    test_4_non_finite_p_is_a_ValueError_not_an_OverflowError()
    test_5_escape_hatch_reproduces_leg121_end_to_end()
    test_6_integer_p_results_are_bit_identical()
    test_7_known_gaps_pinned_as_characterizations_not_soundness()
    print("\n" + "=" * 74)
    print(f"{len(PASS)}/{len(PASS) + len(FAIL)} passed")
    if FAIL:
        for x in FAIL:
            print(f"  FAILED: {x}")
        sys.exit(1)
