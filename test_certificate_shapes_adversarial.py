"""Adversarial gates for `solver/certificate_shapes.py` (leg 146, Route-CSA).

`test_certificate_shapes.py` validates the module on WELL-FORMED input: 25 gates from
legs 57 and 62, every one of which feeds the shipped ledgers or a legal parameter and
checks the answer. This file validates the other half -- what the module does with a
malformed shape descriptor, a boundary class parameter, a degenerate (emptied)
enumeration, and a NaN-poisoned matrix -- and banks leg 146's battery so the answers
cannot silently regress.

The gate leg 146 answered, verbatim from `DIRECTION.md` §146:

  "Under adversarial input (malformed shape descriptors, boundary class parameters,
   degenerate splits) does `certificate_shapes.py` ever silently return a wrong or
   incomplete enumeration, and does its enumerated set match what legs 54/58/126 each
   read from it?"

Answered **YES on the first clause** (7 independent silent-corruption sites) and
**cleanly on the second** (the enumeration question relocates, and the completeness
cross-check that survives the relocation passes 7/7). Leg 146 had no patch authority
under its own gate and did not patch: `solver/certificate_shapes.py` is byte-identical
to what it inherited.

READ THIS BEFORE "FIXING" A FAILURE IN GATES 1-7
------------------------------------------------
Gates 1-7 are CHARACTERIZATION gates. They assert that a defect is OPEN -- they pin the
wrong answer, with its magnitude. **If one of them fails, that is very likely GOOD NEWS:
someone has repaired the module.** The correct response is to read
`experiments/journal/leg_146.md`, confirm the fix, and CONVERT the gate to a soundness
gate asserting the repaired property -- keeping leg 146's pre-repair magnitude printed
next to the repaired one, exactly as `test_first_integral_adversarial.py` does for leg
107. It must NOT be "fixed" by loosening an assertion or deleting the gate.

Gate 8 is a SOUNDNESS gate from the start and must keep passing unconditionally.

THE SEVEN SITES, AS MAGNITUDES
------------------------------
  | gate | site | leg 146 measured |
  |---|---|---|
  | 1 | `is_counterexample` has no schema check | 3 of 7 malformed descriptors silently reclassify a genuine counterexample as not-one |
  | 2 | `real_ledger` rests on one optional key | deleting `is_fictitious` flips Route-XS's gate NO -> YES, citing a row with `arxiv: None` |
  | 3 | the two location guards differ | 2 quote-mutations missed by `unlocated_rows`, the same one caught by `cp_unlocated_rows` |
  | 4 | `cadiot_covers` reasons from absence | an empty scope answers "yes" -- Cadiot covers our operator, on 0 clauses |
  | 5 | `bdl_admissible` drops a modulus | 4 of 13 swept `mu` misclassified; worst reported-admissible `delta` = -500.0 |
  | 6 | `max(0.0, nan)` returns 0.0 | `s_required` 255.0 -> 0.0, i.e. "Lemma 3.2 needs no shift"; 4 of 5 poisons |
  | 7 | `m_divergence` lacks its sibling's guard | one NaN rung inverts the `K`-exponent -0.8089 -> +0.2659 |

Every number here is read from `writeup/data/p2_route_csa_v1_adversarial.json`, produced
by `experiments/p2_route_csa_v1_adversarial.py`. This file re-derives them rather than
reading the JSON, so the two are independent.

Runtime ~25 s (gate 7 runs `classify_operator` twice). Deterministic; no RNG.
"""

import copy
import sys

import numpy as np

import solver.certificate_shapes as cs
from solver.certificate_shapes import (
    BLOCK_DIAGONAL,
    CADIOT_SCOPE,
    SHAPE_LEDGER,
    SHIFT,
    bdl_admissible,
    bdl_delta,
    cadiot_covers,
    cadiot_shift_requirement,
    cp_unlocated_rows,
    decay_exponent,
    gate_answer,
    is_counterexample,
    real_ledger,
    shift_requirement_ladder,
    unlocated_rows,
)
from solver.spectral_certificate import tail_block

COUNTEREXAMPLE = {
    "tag": "PROBE", "arxiv": None, "url": None,
    "is_radii_polynomial": True, "unbounded_part": SHIFT,
    "approx_inverse": BLOCK_DIAGONAL, "tail_inverse_decays": False,
    "located": [{"where": "probe", "quote": "probe", "supports": "probe"}],
}


def test_0_the_banked_answers_still_hold():
    """The anchor. Both shipped gates must still answer what legs 57 and 62 banked.

    Without this, every characterization gate below could be passing because the
    module had been gutted rather than because the defects are where leg 146 found
    them.
    """
    xs = gate_answer()
    cp = cadiot_covers()
    print(f"    Route-XS gate: {xs['answer']!r} over {xs['n_rows_examined']} real rows")
    print(f"    Route-CP gate: {cp['answer']!r}, "
          f"{cp['n_clauses_failing']}/{len(cp['clauses_examined'])} clauses fail")
    assert xs["answer"] == "no", xs["answer"]
    assert xs["n_rows_examined"] == 4, xs["n_rows_examined"]
    assert xs["counterexamples"] == [], xs["counterexamples"]
    assert cp["answer"] == "no", cp["answer"]
    assert cp["n_clauses_failing"] == 6, cp["n_clauses_failing"]
    assert len(SHAPE_LEDGER) == 5 and len(real_ledger()) == 4
    assert unlocated_rows() == [], unlocated_rows()
    assert cp_unlocated_rows() == [], cp_unlocated_rows()
    # and the control can still answer the other way (lesson 90, legs 57/62's own)
    assert gate_answer(SHAPE_LEDGER)["answer"] == "yes"
    print("[ok] leg 57's NO over 4 rows and leg 62's NO over 6/6 clauses both hold, "
          "and both gates can still answer yes on their controls")


def test_1_malformed_descriptors_silently_reclassify():
    """CHARACTERIZATION. `is_counterexample` reads every clause through `dict.get`.

    A key that is PRESENT with a wrong-typed or wrong-cased value passes both the
    predicate and `gate_answer`'s reporter. A key that is MISSING is caught, but only
    incidentally, by the reporter's `r[...]` -- never by the predicate.
    """
    assert is_counterexample(COUNTEREXAMPLE) is True

    silent, caught = [], []
    for label, mutate in [
            ("np.bool_(False)",
             lambda r: r.__setitem__("tail_inverse_decays", np.bool_(False))),
            ("int 0",
             lambda r: r.__setitem__("tail_inverse_decays", 0)),
            ("'shift' lowercase",
             lambda r: r.__setitem__("unbounded_part", "shift")),
            ("drop tail_inverse_decays",
             lambda r: r.pop("tail_inverse_decays")),
            ("drop unbounded_part",
             lambda r: r.pop("unbounded_part")),
            ("drop is_radii_polynomial",
             lambda r: r.pop("is_radii_polynomial")),
            ("rename tail_inverse_decays",
             lambda r: r.__setitem__("tail_inverse_decay",
                                     r.pop("tail_inverse_decays")))]:
        row = copy.deepcopy(COUNTEREXAMPLE)
        mutate(row)
        reclassified = is_counterexample(row) is not True
        try:
            gate_answer(rows=[row])
            raised = False
        except Exception:                                        # noqa: BLE001
            raised = True
        (silent if (reclassified and not raised) else caught).append(label)

    print(f"    silently reclassified: {len(silent)}/7 -> {silent}")
    print(f"    caught (reporter raised): {len(caught)}/7 -> {caught}")
    assert len(silent) == 3, silent
    assert set(silent) == {"np.bool_(False)", "int 0", "'shift' lowercase"}, silent
    # the numpy case is the one that matters: `classify_operator` COMPUTES this field
    assert np.bool_(False) is not False
    print("[ok] pinned: 3 of 7 malformed descriptors silently turn a genuine "
          "counterexample into a non-counterexample; the `is False` identity test "
          "rejects the very numpy boolean `classify_operator` produces")


def test_2_one_optional_key_admits_a_fictitious_row_as_evidence():
    """CHARACTERIZATION. `real_ledger` filters on `r.get("is_fictitious", False)`."""
    poisoned = copy.deepcopy(SHAPE_LEDGER)
    ctrl = [r for r in poisoned if r["tag"] == "SYNTHETIC_CONTROL"][0]
    assert ctrl["counterexample"] is True          # the parallel field, read by nobody
    ctrl.pop("is_fictitious")
    rows = [r for r in poisoned if not r.get("is_fictitious", False)]
    g = gate_answer(rows=rows)
    bad = unlocated_rows(rows=rows)

    print(f"    real rows 4 -> {len(rows)}; gate 'no' -> {g['answer']!r} "
          f"citing {g['counterexamples']}")
    print(f"    unlocated_rows on the citation-free row: {len(bad)} flagged")
    print(f"    that row's where = {ctrl['located'][0]['where']!r}, "
          f"arxiv={ctrl['arxiv']!r}")
    assert len(rows) == 5
    assert g["answer"] == "yes", g["answer"]
    assert g["counterexamples"] == ["SYNTHETIC_CONTROL"]
    assert len(bad) == 0, bad          # the standing guard does NOT catch it
    # the redundancy that could have caught it is dead code
    assert not any("counterexample" in (getattr(cs, n).__doc__ or "")
                   and n == "real_ledger" for n in ("real_ledger",))
    print("[ok] pinned: deleting one optional key flips Route-XS's gate NO -> YES on a "
          "row with arxiv=None and url=None, and the standing location guard reports "
          "it clean")


def test_3_the_two_location_guards_are_not_the_same_guard():
    """CHARACTERIZATION. `cp_unlocated_rows` checks `quote`; `unlocated_rows` does not."""
    missed = []
    for label, mutate in [("quote := ''",
                           lambda r: r["located"][0].__setitem__("quote", "")),
                          ("quote deleted",
                           lambda r: r["located"][0].pop("quote")),
                          ("where := '(none)'",
                           lambda r: r["located"][0].__setitem__("where", "(none)")),
                          ("where := 'p. 3'",
                           lambda r: r["located"][0].__setitem__("where", "p. 3"))]:
        rows = copy.deepcopy(real_ledger())
        mutate(rows[0])
        if not unlocated_rows(rows=rows):
            missed.append(label)

    scope = copy.deepcopy(CADIOT_SCOPE)
    scope[0]["quote"] = ""
    saved = cs.CADIOT_SCOPE
    try:
        cs.CADIOT_SCOPE = scope
        cp_caught = len(cp_unlocated_rows()) > 0
    finally:
        cs.CADIOT_SCOPE = saved

    # and the converse: a legitimate section title containing the word
    rows = copy.deepcopy(real_ledger())
    rows[0]["located"][0]["where"] = "section 2 (the abstract setting), Lemma 2.4"
    false_positive = len(unlocated_rows(rows=rows)) > 0

    print(f"    unlocated_rows missed: {len(missed)}/4 -> {missed}")
    print(f"    cp_unlocated_rows caught the identical quote mutation: {cp_caught}")
    print(f"    false positive on a legitimate 'abstract setting' title: "
          f"{false_positive}")
    assert missed == ["quote := ''", "quote deleted", "where := '(none)'",
                      "where := 'p. 3'"], missed
    assert cp_caught is True
    assert false_positive is True
    print("[ok] pinned: the guard the module docstring calls 'the standing guard' "
          "misses all four, including the two its own sibling catches, and fires on a "
          "legitimate section title")


def test_4_a_degenerate_enumeration_inverts_the_cp_gate():
    """CHARACTERIZATION. `covered = (not failing) or bool(relaxed)`."""
    clean = cadiot_covers()
    empty = cadiot_covers(scope=[])
    unknown = copy.deepcopy(CADIOT_SCOPE)
    for c in unknown:
        c["holds_for_the_a0_CLM_linearisation"] = None
    unk = cadiot_covers(scope=unknown)
    xs_empty = gate_answer(rows=[])

    print(f"    clean scope (6 clauses): {clean['answer']!r}")
    print(f"    EMPTY scope (0 clauses): {empty['answer']!r}, "
          f"clauses_examined={empty['clauses_examined']}")
    print(f"    all-None clauses: {unk['answer']!r}, "
          f"{unk['n_clauses_failing']} counted as failing")
    print(f"    XS gate on an empty ledger: {xs_empty['answer']!r} over "
          f"{xs_empty['n_rows_examined']} rows")
    assert clean["answer"] == "no"
    assert empty["answer"] == "yes", empty["answer"]
    assert empty["clauses_examined"] == []
    assert empty["n_clauses_failing"] == 0
    assert unk["n_clauses_failing"] == 6      # UNKNOWN silently counted as FAILING
    assert xs_empty["answer"] == "no" and xs_empty["n_rows_examined"] == 0
    print("[ok] pinned: an emptied scope reports that Cadiot's construction COVERS our "
          "operator, inverting leg 62's answer on zero evidence; and the sibling gate "
          "reproduces its banked NO on zero rows, where a filtering bug would be "
          "invisible")


def test_5_bdl_admissibility_drops_a_modulus():
    """CHARACTERIZATION. BDL assumption (5) bounds |lambda_k/mu_k|; the code does not."""
    wrong = []
    for mu in (-100.0, -2.0, -1.0, -0.5, -0.4, -1e-3, 0.0, 1e-3, 0.4, 0.5, 1.0, 2.0,
               100.0):
        d = bdl_delta(mu)
        if bool(bdl_admissible(mu)) != bool(abs(d) < 0.5):
            wrong.append((mu, d))
    worst = min(wrong, key=lambda t: t[1])

    print(f"    misclassified: {len(wrong)}/13 -> {[m for m, _ in wrong]}")
    print(f"    worst: mu={worst[0]}, bdl_delta={worst[1]} reported ADMISSIBLE "
          f"(|delta|={abs(worst[1])} vs threshold 0.5)")
    assert len(wrong) == 4, wrong
    assert all(mu < 0 for mu, _ in wrong), wrong
    assert bdl_admissible(-0.4) is True and abs(bdl_delta(-0.4)) == 1.25
    # and the shape LABEL follows the broken predicate to the far end of the dial
    label = cs.MULTIPLIER if bdl_admissible(-1.0) else cs.TRIDIAGONAL_DOMINANT
    print(f"    classify_operator would label mu=-1.0 as {label}")
    assert label == cs.MULTIPLIER
    print("[ok] pinned: every mu < 0 passes BDL assumption (5) because delta is signed, "
          "and an anti-dissipative operator is labelled MULTIPLIER -- the word at the "
          "opposite end of this module's own shift-to-multiplier dial")


def test_6_one_nan_reports_lemma_3_2_as_needing_no_shift():
    """CHARACTERIZATION. `sqrt(max(0.0, nan))` is 0.0, and 0.0 means 'already dominant'."""
    K, M = 8, 512
    T = tail_block(K, M, mu=0.0)
    clean = cadiot_shift_requirement(T)
    assert max(0.0, float("nan")) == 0.0      # the exact language mechanism

    zeros, others = [], []
    for label, ij, val in [("off-diagonal NaN", (5, 7), np.nan),
                           ("diagonal NaN", (3, 3), np.nan),
                           ("last-row NaN", (M - K - 1, M - K - 1), np.nan),
                           ("off-diagonal +inf", (5, 7), np.inf)]:
        Tp = np.array(T, dtype=float, copy=True)
        Tp[ij] = val
        v = cadiot_shift_requirement(Tp)
        (zeros if v == 0.0 else others).append((label, v))
    Tp = np.array(T, dtype=float, copy=True)
    Tp[11, :] = np.nan
    row_nan = cadiot_shift_requirement(Tp)
    if row_nan == 0.0:
        zeros.append(("whole row NaN", row_nan))

    print(f"    clean s_required = {clean}  (grows linearly in M: no finite shift)")
    print(f"    inverted to 0.0 = 'already diagonally dominant': {len(zeros)}/5 "
          f"-> {[l for l, _ in zeros]}")
    print(f"    not inverted: {others}")
    assert clean == 255.0, clean
    assert len(zeros) == 4, zeros
    assert others == [("off-diagonal +inf", float("inf"))], others

    # one level up, the verdict WORD flips to the positive control's answer
    ladder_clean = shift_requirement_ladder(
        lambda n: tail_block(K, int(n), mu=0.0), (128, 256, 512))

    def poisoned(n):
        A = np.array(tail_block(K, int(n), mu=0.0), dtype=float, copy=True)
        A[5, 7] = np.nan
        return A

    ladder_bad = shift_requirement_ladder(poisoned, (128, 256, 512))
    print(f"    ladder clean: saturates={ladder_clean.get('saturates')}, "
          f"exponent={ladder_clean.get('exponent')}")
    print(f"    ladder poisoned: saturates={ladder_bad.get('saturates')}, "
          f"refused={ladder_bad.get('refused') is not None}")
    assert ladder_clean.get("saturates") is False
    assert ladder_bad.get("saturates") is True
    print("[ok] pinned: one NaN turns 'no finite shift exists' (255.0) into 'the "
          "unshifted matrix is already dominant' (0.0), and the ladder then reports "
          "SATURATES -- the verdict leg 62 measured for Cadiot's own Whitham operator")


def test_7_a_missing_sibling_guard_inverts_the_dichotomy():
    """CHARACTERIZATION. `decay_exponent` guards its fit; `m_divergence` does not."""
    sibling = decay_exponent([128, 256, 512, 1024], [1.0, 2.0, float("nan"), 4.0])
    assert sibling["refused"] is True, sibling
    print(f"    decay_exponent on a NaN rung: refused -- {sibling['reason']!r}")

    Ks, M, mu = (4, 8, 16, 32), 256, 1.0
    clean = cs.classify_operator(mu, Ks=Ks, M=M)
    orig = cs.tail_inverse_norm

    def poisoned(K, Mv, kind, param, mu=0.0):
        v = orig(K, Mv, kind, param, mu=mu)
        return float("nan") if int(Mv) == 512 else v

    try:
        cs.tail_inverse_norm = poisoned
        dirty = cs.classify_operator(mu, Ks=Ks, M=M)
    finally:
        cs.tail_inverse_norm = orig

    print(f"    mu=1 clean:    invertible={clean['tail_block_boundedly_invertible']}, "
          f"M_exp={clean['M_exponent']:+.3e}, K_exp={clean['K_exponent']:+.4f}, "
          f"decays={clean['tail_inverse_decays']}")
    print(f"    mu=1 poisoned: invertible={dirty['tail_block_boundedly_invertible']}, "
          f"M_exp={dirty['M_exponent']}, K_exp={dirty['K_exponent']:+.4f}, "
          f"decays={dirty['tail_inverse_decays']}")
    assert clean["tail_block_boundedly_invertible"] is True
    assert clean["tail_inverse_decays"] is True and clean["K_exponent"] < 0.0
    assert np.isnan(dirty["M_exponent"])
    assert dirty["tail_block_boundedly_invertible"] is False
    assert dirty["needed_bordering"] is True
    assert dirty["tail_inverse_decays"] is False and dirty["K_exponent"] > 0.0
    # the exported label still reads the mu > 0 word, so label and measurement disagree
    assert clean["shape"] == dirty["shape"] == cs.TRIDIAGONAL_DOMINANT
    print(f"    K-exponent sign inverted: {clean['K_exponent']:+.4f} -> "
          f"{dirty['K_exponent']:+.4f}, while `shape` still reads "
          f"{dirty['shape']}")
    print("[ok] pinned: one NaN rung routes an invertible operator down leg 52's "
          "bordering branch and inverts the sign of the module's headline dichotomy, "
          "on the exact input its sibling function refuses by name")


def test_8_the_enumeration_legs_54_58_126_range_over_is_complete():
    """SOUNDNESS -- must keep passing. The gate's second clause.

    `DIRECTION.md` §146 supposed this module supplies that enumeration. It does not:
    `SHAPES` is declared once in leg 54's runner and IMPORTED by legs 58 and 126, and
    nothing imports anything from `solver/certificate_shapes.py`. What is hand-written
    twice is the A21 partition, and leg 126 uses its copy to drop inconsistent
    (shape, A21) pairs -- so a disagreement there would move its 1,686 count.
    """
    sys.path.insert(0, "experiments")
    import ast
    import os

    def lit(path, name):
        with open(path) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id == name:
                        return ast.literal_eval(node.value)
        return None

    def imports(path, module):
        with open(path) as f:
            tree = ast.parse(f.read())
        out = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == module:
                out += [a.name for a in node.names]
        return sorted(out)

    mm = os.path.join("experiments", "p2_route_mm_v1_shape.py")
    ng = os.path.join("experiments", "p2_route_ng_v1_nogo.py")
    bx = os.path.join("experiments", "p2_route_bx_v1_stageb.py")

    shapes = sorted(lit(mm, "SHAPES"))
    in_cls, out_cls = lit(ng, "IN_CLASS"), lit(ng, "OUT_OF_CLASS")
    a21 = lit(bx, "a21_of_shape")

    n_from_module = sum(len(imports(p, "solver.certificate_shapes"))
                        for p in (mm, ng, bx))
    print(f"    SHAPES ({len(shapes)}): {shapes}")
    print(f"    leg 58 imports from leg 54: {imports(ng, 'p2_route_mm_v1_shape')}")
    print(f"    leg 126 imports from leg 54: {imports(bx, 'p2_route_mm_v1_shape')}")
    print(f"    names legs 54/58/126 import from solver/certificate_shapes.py: "
          f"{n_from_module}")
    assert len(shapes) == 7
    assert "SHAPES" in imports(ng, "p2_route_mm_v1_shape")
    assert "SHAPES" in imports(bx, "p2_route_mm_v1_shape")
    assert n_from_module == 0, n_from_module

    assert sorted(tuple(in_cls) + tuple(out_cls)) == shapes
    assert not (set(in_cls) & set(out_cls))
    assert sorted(a21.keys()) == shapes

    def cross(map126):
        return [nm for nm in shapes
                if ("zero" if nm in in_cls else "nonzero") != map126.get(nm)]

    disagree = cross(a21)
    print(f"    A21 partition cross-checked over {len(shapes)} shapes: "
          f"{len(disagree)} disagreements")
    assert disagree == [], disagree

    # LESSON 90: the comparator must be able to come out the other way.
    perturbed = dict(a21)
    perturbed["ff_lift"] = "zero"
    ctrl = cross(perturbed)
    print(f"    negative control (flip a21_of_shape['ff_lift']): reports {ctrl}")
    assert ctrl == ["ff_lift"], ctrl
    print("[ok] the enumeration is declared once and imported twice, this module "
          "contributes 0 names to it, the twice-written A21 partition agrees 7/7, and "
          "the comparator reports an injected disagreement -- leg 126's completeness "
          "count is independently corroborated on this axis")


if __name__ == "__main__":
    test_0_the_banked_answers_still_hold()
    test_1_malformed_descriptors_silently_reclassify()
    test_2_one_optional_key_admits_a_fictitious_row_as_evidence()
    test_3_the_two_location_guards_are_not_the_same_guard()
    test_4_a_degenerate_enumeration_inverts_the_cp_gate()
    test_5_bdl_admissibility_drops_a_modulus()
    test_6_one_nan_reports_lemma_3_2_as_needing_no_shift()
    test_7_a_missing_sibling_guard_inverts_the_dichotomy()
    test_8_the_enumeration_legs_54_58_126_range_over_is_complete()
    print("\nAll leg-146 adversarial gates passed: 1 anchor + 7 CHARACTERIZATION gates "
          "pinning open silent-corruption sites + 1 SOUNDNESS gate. A failure in gates "
          "1-7 most likely means the module was repaired -- see the header and "
          "experiments/journal/leg_146.md before changing anything.")
