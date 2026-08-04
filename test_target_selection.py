"""Gates for solver/target_selection.py -- Route-M's target ledger.

A ledger's failure mode is not a wrong number, it is DRIFT: an entry whose verdict no
longer matches its evidence, a rank that no longer matches the criterion, a "reachable"
that nobody re-derived.  These gates are the drift detector, in the same spirit as
test_plan_of_record.py -- and for the same reason, which is that this project's
characteristic failure is drift, not error.

Run: .venv/bin/python test_target_selection.py
"""

import numpy as np

from solver.target_selection import (
    CERTIFICATION_RECORD, CERTIFIED_REFERENCE, ROUTE_M_SOURCES, TARGET_LEDGER,
    certified_objects, cln_kawahara_check, cost_ratio_vs_certified, gate_verdict,
    ledger_counts, ns_preprint_closure_audit, radii_polynomial, rank_table,
    uncertified_targets, unknowns, y0_budget,
)

VALID_VERDICTS = {"NO", "YES_CAP", "YES_ANALYTIC", "CLAIMED_UNUSABLE"}
VALID_PROOF_KINDS = {"CAP", "ANALYTIC", "CAP+ANALYTIC", "NONE"}


def test_ledger_answers_all_three_questions():
    """Every candidate answers Q1/Q2/Q3 and cites a source. No silent blanks."""
    for t in TARGET_LEDGER:
        for k in ("rank", "id", "object", "source", "certified", "q1", "q2", "q3",
                  "our_machinery"):
            assert k in t and t[k] not in (None, "", {}), f"{t.get('id')}: missing {k}"
        assert t["certified"] in VALID_VERDICTS, f"{t['id']}: bad verdict {t['certified']}"
        for k in ("dim", "n_fields", "n_modulation", "nonlocal"):
            assert k in t["q2"], f"{t['id']}: q2 missing {k}"
        assert len(t["q3"]) > 60, f"{t['id']}: Q3 is too short to be an answer"
    ranks = sorted(t["rank"] for t in TARGET_LEDGER)
    assert ranks == list(range(1, len(TARGET_LEDGER) + 1)), f"ranks not contiguous: {ranks}"
    ids = [t["id"] for t in TARGET_LEDGER]
    assert len(set(ids)) == len(ids), "duplicate ledger ids"
    print(f"    {len(TARGET_LEDGER)} candidates, three questions each, ranks 1..{len(ranks)}")
    print("[ok] the ledger answers all three questions for every candidate")


def test_certification_record_is_consistent_with_the_ledger():
    """A ledger entry marked certified must point at a proof in the record, and vice versa.

    This is the gate that would have caught the leg's own headline had it existed
    earlier: the object the port is aimed at is in CERTIFICATION_RECORD with
    proof_kind = CAP, and no ledger entry may call it uncertified.
    """
    for c in CERTIFICATION_RECORD:
        assert c["proof_kind"] in VALID_PROOF_KINDS, f"{c['object']}: {c['proof_kind']}"
        assert c["source"] and c["note"]
    certified_names = " || ".join(c["object"] for c in certified_objects())
    for t in TARGET_LEDGER:
        if t["certified"].startswith("YES"):
            key = t["object"].split(",")[0].strip()
            assert key.lower() in certified_names.lower(), \
                f"{t['id']} claims certified but is not in CERTIFICATION_RECORD"
    n_proved = len(certified_objects())
    assert n_proved >= 6, "the exclusion list lost entries"
    counts = ledger_counts()
    assert counts.get("YES_CAP", 0) >= 1, "the certified reference vanished from the ledger"
    print(f"    {n_proved} proved objects on the exclusion list; ledger counts {counts}")
    print("[ok] certification record and ledger agree")


def test_unknown_count_is_exact_arithmetic():
    """No fudge factors: unknowns = fields * n^dim + modulation, and the ratio follows."""
    assert unknowns(1, 2, 600, 3) == 2 * 600 + 3
    assert unknowns(2, 3, 600, 2) == 3 * 600 ** 2 + 2
    assert unknowns(3, 3, 600, 2) == 3 * 600 ** 3 + 2
    r = cost_ratio_vs_certified(CERTIFIED_REFERENCE["dim"], CERTIFIED_REFERENCE["n_fields"],
                                600, CERTIFIED_REFERENCE["n_modulation"])
    assert abs(r["ratio"] - 1.0) < 1e-15, "the reference object is not its own unit"
    one_d = cost_ratio_vs_certified(1, 2, 600, 3)["ratio"]
    three_d = cost_ratio_vs_certified(3, 3, 600, 2)["ratio"]
    assert one_d < 1.0 < three_d
    print(f"    ratio(1D,2 fields) = {one_d:.3e}   ratio(3D,3 fields) = {three_d:.3e}")
    print("[ok] unknown counts are exact and the reference object is the unit")


def test_y0_budget_is_the_exact_feasibility_boundary():
    """(1-Z1)^2/(2 Z2) is not a heuristic: it is where the radii polynomial loses its root.

    Checked by BRACKETING the boundary rather than evaluating at it -- a strict
    inequality tested at its own boundary is a coin flip in floating point.
    """
    for Z1, Z2 in ((0.0, 1.0), (0.3, 1e3), (0.75, 1e5), (0.9, 1e-2)):
        B = y0_budget(Z1, Z2)
        assert radii_polynomial(B * (1.0 - 1e-9), Z1, Z2)["feasible"], \
            f"infeasible just inside the budget at Z1={Z1}, Z2={Z2}"
        assert not radii_polynomial(B * (1.0 + 1e-9), Z1, Z2)["feasible"], \
            f"feasible just outside the budget at Z1={Z1}, Z2={Z2}"
        rp = radii_polynomial(0.5 * B, Z1, Z2)
        assert rp["r_min"] < rp["r_max"], "empty admissible interval inside the budget"
        assert rp["Z1"] + Z2 * rp["r_min"] < 1.0, "the second NK condition is violated"
    assert not radii_polynomial(1e-30, 1.0, 1.0)["feasible"], "Z1 >= 1 must refuse"
    print("[ok] Y0 budget brackets the radii polynomial's root exactly, on four (Z1,Z2)")


def test_reproduces_published_kawahara_radius():
    """[CLN] Theorem 6.6: our algebra returns their r0 from their Y0. A known answer."""
    k = cln_kawahara_check()
    assert k["rel_err_vs_published_r0"] < 1e-3, k
    assert 0.0 < k["Z1_implied"] < 0.05, f"implied Z1 out of range: {k['Z1_implied']}"
    print(f"    published r0 = {k['r0_published']:.3e}, ours "
          f"{k['r_from_our_algebra']:.3e}, rel err {k['rel_err_vs_published_r0']:.1e}, "
          f"implied Z1 = {k['Z1_implied']:.2e}")
    print("[ok] the feasibility algebra reproduces a COMPLETED certificate's radius")


def test_ns_preprint_audit_reports_magnitudes_not_a_boolean():
    """Both closure forms are computed, and the audit does NOT rest on the arithmetic.

    The point of the gate is the discipline: the manuscript's scalar closure holds in
    the printed form AND in the corrected Kantorovich form, so the audit must say so.
    An audit that reported 'fails' here would be reporting the wrong thing, and the
    reasons the object is not certified have to stand without it (lesson 76 -- keep the
    negative construction in the artifact).
    """
    a = ns_preprint_closure_audit()
    assert a["closure_as_printed_2dMK"] < 1.0
    assert a["closure_corrected_2M2Kdelta"] < 1.0
    assert a["both_close"] is True
    assert a["closure_corrected_2M2Kdelta"] > a["closure_as_printed_2dMK"], \
        "the corrected form must be the LARGER one -- it carries an extra factor M"
    ratio = a["closure_corrected_2M2Kdelta"] / a["closure_as_printed_2dMK"]
    assert abs(ratio - a["M"]) / a["M"] < 1e-9, "the two forms differ by exactly M"
    assert a["K_rel_err"] < 1e-3, "their K does not match their own factor product"
    print(f"    printed 2dMK = {a['closure_as_printed_2dMK']:.3e}; corrected 2M^2Kd = "
          f"{a['closure_corrected_2M2Kdelta']:.3e} (ratio = M = {a['M']}); "
          f"their K from their parts, rel err {a['K_rel_err']:.1e}")
    print("[ok] NS-preprint closure audited in both forms; both close, and it is recorded")


def test_gate_is_decisive_and_names_a_live_target():
    """Route-M's gate returns YES/NO and, on YES, names an entry that is really uncertified."""
    g = gate_verdict()
    assert g["gate"] in ("YES", "NO")
    if g["gate"] == "YES":
        named = g["named_target"]
        entry = next(t for t in TARGET_LEDGER if t["id"] == named)
        assert entry["certified"] == "NO", "named target is certified"
        assert entry["rank"] == min(t["rank"] for t in uncertified_targets()), \
            "named target is not the top-ranked uncertified one"
        row = next(r for r in rank_table() if r["id"] == named)
        assert row["ratio"] <= 1.0, "named target costs more than the certified object"
        print(f"    GATE {g['gate']} -> {named} (rank {entry['rank']}, "
              f"cost ratio {row['ratio']:.3e} of the certified object)")
    else:
        print("    GATE NO -- the plan says STOP and report")
    print("[ok] the gate is decisive and internally consistent")


def test_ranking_is_by_contribution_not_by_cost():
    """The declared criterion is Q3 first, Q2 last. If cost drove the ranking, say so.

    The cheapest uncertified object (a single scalar field) is NOT rank 1, and that is
    the whole point of the ordering: an object that reproduces a published theorem is
    worth nothing however cheap it is.  This gate fails if someone later re-sorts the
    ledger by cost without changing the stated criterion.
    """
    rows = {r["id"]: r for r in rank_table()}
    unc = sorted(uncertified_targets(), key=lambda t: t["rank"])
    costs = [rows[t["id"]]["ratio"] for t in unc]
    assert costs != sorted(costs), \
        "the uncertified ranking is in cost order -- criterion and ledger have drifted"
    cheapest = min(unc, key=lambda t: rows[t["id"]]["ratio"])
    assert cheapest["rank"] != 1, "the cheapest object took rank 1"
    print(f"    uncertified ranks {[t['rank'] for t in unc]} carry costs "
          f"{[f'{c:.1e}' for c in costs]} -- not sorted by cost")
    print("[ok] ranking follows the stated criterion (contribution first)")


def test_every_source_read_is_declared():
    """Each ledger source appears in ROUTE_M_SOURCES or in Route-J's four. No orphans."""
    from solver.literature_gates import PRIMARY_SOURCES
    known = set(ROUTE_M_SOURCES) | set(PRIMARY_SOURCES)
    for t in TARGET_LEDGER:
        ids = [w.strip(" ,;()") for w in t["source"].replace("arXiv:", " ").split()]
        arxiv = [w for w in ids if w[:4].isdigit() and "." in w]
        assert arxiv, f"{t['id']}: no arXiv id in its source string"
        for a in arxiv:
            assert a in known, f"{t['id']}: cites {a}, which no source block declares"
    for k, v in ROUTE_M_SOURCES.items():
        for f in ("tag", "authors", "title", "venue", "read", "gates"):
            assert v.get(f), f"{k}: source block missing {f}"
    print(f"    {len(ROUTE_M_SOURCES)} new source blocks; every ledger citation resolves")
    print("[ok] every source the ledger cites is declared with what was read of it")


if __name__ == "__main__":
    test_ledger_answers_all_three_questions()
    test_certification_record_is_consistent_with_the_ledger()
    test_unknown_count_is_exact_arithmetic()
    test_y0_budget_is_the_exact_feasibility_boundary()
    test_reproduces_published_kawahara_radius()
    test_ns_preprint_audit_reports_magnitudes_not_a_boolean()
    test_gate_is_decisive_and_names_a_live_target()
    test_ranking_is_by_contribution_not_by_cost()
    test_every_source_read_is_declared()
    print("\nALL TARGET-SELECTION TESTS PASSED")
