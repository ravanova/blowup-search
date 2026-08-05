"""Gates for solver/certificate_shapes.py -- Route-XS v1 (leg 57), the shape dichotomy.

No pytest: `requirements.txt` is numpy + matplotlib, and the repo's convention is plain
asserts with a __main__ runner.  Run it with `.venv/bin/python test_certificate_shapes.py`.

The gates are in two groups and the split is the point.

  LEDGER (1-8)    guard the BOOKKEEPING: every classification traced to a located
                  FULL-TEXT statement, no row citing an abstract, and -- the one that
                  matters most -- a gate predicate that can answer BOTH ways (lesson 90).
  OPERATOR (9-14) guard the MEASUREMENT: the labels in the ledger are the labels the
                  measurement returns when the corresponding operator is fed to it, and
                  every verdict is asserted with its MAGNITUDE, never as a bare boolean.

Gate 14 is a hypothesis this leg posed, checked, and killed.  It is kept as a test so
the dead hypothesis cannot quietly come back.
"""

import numpy as np

from solver.certificate_shapes import (
    BLOCK_DIAGONAL,
    FINITE_JACOBIAN,
    MULTIPLIER,
    NO_APPROXIMATE_INVERSE,
    NO_UNBOUNDED_PART,
    NOT_BLOCK_DIAGONAL,
    SHAPE_LEDGER,
    SHIFT,
    TRIDIAGONAL_DOMINANT,
    bdl_admissible,
    bdl_delta,
    classify_operator,
    decay_exponent,
    gate_answer,
    is_counterexample,
    m_divergence,
    real_ledger,
    tail_inverse_ladder,
    unlocated_rows,
)

SHAPES = {MULTIPLIER, TRIDIAGONAL_DOMINANT, SHIFT, NO_UNBOUNDED_PART}
INVERSES = {BLOCK_DIAGONAL, NOT_BLOCK_DIAGONAL, FINITE_JACOBIAN, NO_APPROXIMATE_INVERSE}


def _row(tag):
    return next(r for r in real_ledger() if r["tag"] == tag)


# --------------------------------------------------------------------------
# LEDGER
# --------------------------------------------------------------------------
def test_1_every_row_is_traced_to_a_located_full_text_statement():
    """The leg's deliverable clause. Leg 53 lost a claim by reading BDL's ABSTRACT.

    If this ever fails, the row it names is inadmissible evidence and any prose quoting
    it must be withdrawn -- that is the whole reason it is a test and not a habit.
    """
    bad = unlocated_rows()
    assert bad == [], f"rows not traced to a located statement: {bad}"
    for row in real_ledger():
        assert row["located"], row["tag"]
        for d in row["located"]:
            assert d["where"], row["tag"]
            assert "abstract" not in d["where"].lower(), (row["tag"], d["where"])
            assert d["quote"] and d["supports"], row["tag"]
    print(f"  {len(real_ledger())} rows, "
          f"{sum(len(r['located']) for r in real_ledger())} located statements, "
          f"0 citing an abstract")


def test_2_every_row_has_a_resolvable_link():
    """Links, not counts (the standing rule this project keeps re-learning)."""
    for row in real_ledger():
        assert row["url"] and row["url"].startswith("https://arxiv.org/abs/"), row["tag"]
        assert row["arxiv"], row["tag"]
    print("  " + ", ".join(f"{r['tag']}={r['url']}" for r in real_ledger()))


def test_3_vocabulary_is_closed():
    """Free text in a classification field is how a ledger stops being executable."""
    for row in SHAPE_LEDGER:
        assert row["unbounded_part"] in SHAPES, row["tag"]
        assert row["approx_inverse"] in INVERSES, row["tag"]
        assert row["tail_inverse_decays"] in (True, False, None), row["tag"]
    print(f"  {len(SHAPE_LEDGER)} rows, all fields in the closed vocabulary")


def test_4_gate_answers_no_on_the_published_record():
    g = gate_answer()
    assert g["answer"] == "no", g
    assert g["counterexamples"] == []
    assert g["n_rows_examined"] == 4
    print(f"  gate = {g['answer']!r} over {g['n_rows_examined']} published rows")


def test_5_gate_can_answer_yes_lesson_90():
    """A control that cannot come out differently is not a control.

    Admit the fictitious row and the SAME predicate must flip.  Without this, the "no"
    in gate 4 is a property of the code rather than of the literature -- which is
    exactly the failure leg 53 shipped and VERIFIER caught.
    """
    g = gate_answer(SHAPE_LEDGER)
    assert g["answer"] == "yes", g
    assert g["counterexamples"] == ["SYNTHETIC_CONTROL"]
    print("  admitting the fictitious row flips the gate to 'yes' -- the gate is live")


def test_6_the_control_row_is_excluded_from_evidence():
    assert all(not r.get("is_fictitious") for r in real_ledger())
    assert len(SHAPE_LEDGER) == len(real_ledger()) + 1
    print("  control row present in SHAPE_LEDGER, absent from real_ledger()")


def test_7_the_near_misses_are_near_misses_for_DIFFERENT_reasons():
    """Each clause of the gate does work; knock one out and a real paper becomes a
    spurious counterexample.  That the two near-misses fail different clauses is the
    substance of the classification, not a bookkeeping detail."""
    ch = _row("CH")
    assert not is_counterexample(ch)
    assert ch["unbounded_part"] == SHIFT and ch["is_radii_polynomial"] is False

    bdl = _row("BDL")
    assert not is_counterexample(bdl)
    assert bdl["is_radii_polynomial"] and bdl["unbounded_part"] != SHIFT

    # and the two failures are on different clauses
    assert (ch["is_radii_polynomial"], ch["unbounded_part"] == SHIFT) == (False, True)
    assert (bdl["is_radii_polynomial"], bdl["unbounded_part"] == SHIFT) == (True, False)
    print("  CH fails the radii-polynomial clause; BDL fails the shift clause")


def test_8_the_three_papers_are_classified_as_the_prose_says():
    """CH is the row most likely to be misread, so it is pinned here.

    Chen-Hou certify a transport operator.  Drop the gate's `is_radii_polynomial`
    clause and they read as a REFUTATION of the dichotomy; keep it and they are the
    strongest CONFIRMATION in the corpus, because they certify the shift by abandoning
    the tail estimate rather than by repairing it.
    """
    ch = _row("CH")
    assert ch["approx_inverse"] == NO_APPROXIMATE_INVERSE
    assert ch["tail_inverse_decays"] is None      # not False: there IS no tail inverse
    assert any("2.7" in d["where"] for d in ch["located"])

    bdl = _row("BDL")
    assert bdl["approx_inverse"] == NOT_BLOCK_DIAGONAL
    assert bdl["unbounded_part"] == TRIDIAGONAL_DOMINANT
    assert bdl["tail_inverse_decays"] is True
    assert any("Proposition 2.3" in d["where"] for d in bdl["located"])

    cln = _row("CLN")
    assert cln["unbounded_part"] == MULTIPLIER
    assert cln["approx_inverse"] == BLOCK_DIAGONAL
    assert any("Assumption 2.1" in d["where"] for d in cln["located"])

    df = _row("DF")
    assert df["unbounded_part"] == NO_UNBOUNDED_PART
    assert df["approx_inverse"] == FINITE_JACOBIAN
    print("  CLN=multiplier/block-diag, BDL=tridiag-dominant/NOT-block-diag, "
          "CH=shift/no-inverse, DF=finite-dim")


# --------------------------------------------------------------------------
# OPERATOR -- the labels above, MEASURED
# --------------------------------------------------------------------------
def test_9_bdl_ratio_is_infinite_at_zero_diagonal():
    """delta = 1/(2 mu).  A zero diagonal is not a small ratio; it is no ratio."""
    assert bdl_delta(0.0) == float("inf")
    assert not bdl_admissible(0.0)
    assert abs(bdl_delta(1.0) - 0.5) < 1e-12
    assert bdl_admissible(2.0) and abs(bdl_delta(2.0) - 0.25) < 1e-12
    print("  delta(0)=inf, delta(1)=0.5 (BDL's boundary), delta(2)=0.25 (admissible)")


def test_10_shift_tail_block_is_not_boundedly_invertible():
    """XS2. At mu = 0 the UNBORDERED tail inverse grows LINEARLY in M -- no limit.

    This is the fact that forced leg 52 to border.  Asserted as an EXPONENT, not as an
    overflow: the number is finite at every M and the divergence is only visible as a
    ladder (lesson 72, report the shape of a ladder not its endpoint).
    """
    md = m_divergence(0.0, K=8, bordered=False)
    assert md["exponent_in_M"] > 0.9, md
    assert md["vals"][-1] > 10 * md["vals"][0], md
    print(f"  unbordered, mu=0: M-exponent = {md['exponent_in_M']:+.3f} "
          f"({md['vals'][0]:.3g} -> {md['vals'][-1]:.3g})")


def test_11_bordering_makes_it_exist_but_not_decay():
    """XS3, and it is the sharp form of "a constant, not 1/K".

    Bordered at mu = 0 the inverse SATURATES in M (so it exists -- leg 52's repair
    works) but GROWS in K (so the tail estimate has nothing to close with -- leg 53's
    failure).  Both halves, both as magnitudes, in one gate.
    """
    md = m_divergence(0.0, K=8, bordered=True)
    assert abs(md["exponent_in_M"]) < 0.1, md          # exists: flat in M
    Ks, vals = tail_inverse_ladder(0.0, bordered=True)
    de = decay_exponent(Ks, vals)
    assert not de["refused"], de
    assert de["exponent"] > 0.3, de                    # GROWS in K
    assert abs(vals[0] - 2.191) < 0.02, vals           # the repo's standing 2.19
    assert vals[-1] > 4 * vals[0], vals
    print(f"  bordered, mu=0: flat in M ({md['exponent_in_M']:+.3f}), "
          f"GROWS in K ({de['exponent']:+.3f}); {vals[0]:.4g} -> {vals[-1]:.4g}")


def test_12_a_nonzero_diagonal_restores_decay():
    """The positive control -- and it demonstrably reports the other answer at mu = 0."""
    for mu in (0.25, 1.0, 2.0):
        c = classify_operator(mu)
        assert c["tail_block_boundedly_invertible"], c
        assert not c["needed_bordering"], c
        assert c["tail_inverse_decays"] is True, c
        assert c["K_exponent"] < -0.8, c
        print(f"  mu={mu:<5} invertible, K-exponent = {c['K_exponent']:+.3f}, decays")


def test_13_the_shift_is_the_only_case_that_fails():
    c = classify_operator(0.0)
    assert c["shape"] == SHIFT
    assert c["needed_bordering"]
    assert c["tail_inverse_decays"] is False
    assert c["K_exponent"] > 0
    print(f"  mu=0.0   SHIFT, needs bordering, K-exponent = {c['K_exponent']:+.3f}, "
          "does NOT decay")


def test_14_bdl_threshold_is_NOT_where_the_behaviour_changes():
    """A hypothesis this leg posed, checked, and KILLED -- kept so it cannot come back.

    BDL's assumption (5) is delta < 1/2, which for our operator reads mu > 1.  If that
    were the hinge, mu = 0.25 (delta = 2, far OUTSIDE BDL's admissible set) would have
    to behave like mu = 0.  It does not: it is boundedly invertible and its tail inverse
    decays at -0.85.  delta < 1/2 is what BDL's LU CONSTRUCTION needs; it is not where
    the operator changes character.  The hinge is zero-vs-nonzero diagonal.
    """
    assert not bdl_admissible(0.25)
    c = classify_operator(0.25)
    assert c["tail_block_boundedly_invertible"], c
    assert c["tail_inverse_decays"] is True, c
    assert c["K_exponent"] < -0.8, c
    print(f"  mu=0.25 is OUTSIDE BDL (delta={bdl_delta(0.25):.3g}) and still decays "
          f"({c['K_exponent']:+.3f}) -- the hypothesis is dead")


def test_15_decay_exponent_refuses_rather_than_returning_a_number():
    """Refusal predicates, because a fit through a bad rung is worse than no fit."""
    assert decay_exponent([4, 8], [1.0, 2.0])["refused"]
    assert decay_exponent([4, 8, 16, 32], [1.0, 2.0, 0.0, 3.0])["refused"]
    assert decay_exponent([4, 8, 16, 32], [1.0, 2.0, np.inf, 3.0])["refused"]
    assert decay_exponent([4, 8, 16, 32], [1.0, 2.0, -1.0, 3.0])["refused"]
    print("  refuses on: too few rungs, a zero rung, an inf rung, a negative rung")


# ==========================================================================
# ROUTE-CP v1 (leg 62): the Cadiot pre-emption, settled from the full text
# ==========================================================================
# Gates 16-22 guard the CP ledger.  Same two groups as above: 16-20 guard the
# bookkeeping (located statements, disclosed reading depth, a gate that refuses what it
# has not read), 21-22 guard the measurement (the diagonal weight that repairs BRT's
# radii, measured against a shift and against BRT's own operator).
def test_16_cp_rows_are_traced_and_disclose_their_reading_depth():
    from solver.certificate_shapes import CP_LEDGER, cp_unlocated_rows
    bad = cp_unlocated_rows()
    assert bad == [], f"CP rows not traced, or hiding a second-hand reading: {bad}"
    for row in CP_LEDGER:
        assert row["located"], row["tag"]
        for d in row["located"]:
            assert d["where"] and "abstract" not in d["where"].lower(), (row["tag"], d)
            assert d["quote"] and d["supports"], row["tag"]
    n_loc = sum(len(r["located"]) for r in CP_LEDGER)
    print(f"  {len(CP_LEDGER)} rows, {n_loc} located statements, none from an abstract")


def test_17_the_gate_answers_no_and_names_what_it_refused():
    from solver.certificate_shapes import cp_gate_answer
    g = cp_gate_answer()
    assert g["answer"] == "no", g
    assert g["covering_rows"] == [] and g["contradicting_rows"] == []
    # FL91 is paywalled and read only second-hand.  It must be REFUSED, not counted.
    assert g["refused_not_full_text"] == ["FL91"], g["refused_not_full_text"]
    assert g["n_full_text"] == 3, g["n_full_text"]
    print(f"  gate=no over {g['n_full_text']} full-text rows; "
          f"refused (not full text): {g['refused_not_full_text']}")


def test_18_the_gate_can_answer_yes_lesson_90():
    """A gate that cannot come out the other way is not a gate."""
    from solver.certificate_shapes import FULL_TEXT, cp_gate_answer, cp_literature_rows
    synthetic = dict(cp_literature_rows()[0])
    synthetic["tag"] = "SYNTHETIC_CP_CONTROL"
    synthetic["read_at"] = FULL_TEXT
    synthetic["covers_offdiag_unbounded"] = True
    synthetic["rho"] = 3.0
    g = cp_gate_answer(cp_literature_rows() + [synthetic])
    assert g["answer"] == "yes", g
    assert g["covering_rows"] == ["SYNTHETIC_CP_CONTROL"], g["covering_rows"]
    print("  admitting a fictitious covering row flips the answer to yes")


def test_19_the_dominance_ratio_separates_every_source_from_our_object():
    from solver.certificate_shapes import (cp_gate_answer, dominance_ratio_admits,
                                           our_cp_row)
    g = cp_gate_answer()
    for r in g["rows"]:
        if r["rho"] is None:
            assert dominance_ratio_admits(r["rho"]) is None, r["tag"]
            continue
        assert r["rho"] < 1.0, (r["tag"], r["rho"])
        assert r["rho_admits_tail_estimate"] is True, r["tag"]
    ours = our_cp_row()
    assert ours["rho"] == float("inf")
    assert dominance_ratio_admits(ours["rho"]) is False
    # magnitudes, never a bare boolean: the gap is not marginal
    assert ours["offdiag_growth"] - ours["diag_growth"]["a0_clm"] == 1.0
    print(f"  every located source rho < 1; ours rho = {ours['rho']}, "
          f"gamma_R - gamma_D = "
          f"{ours['offdiag_growth'] - ours['diag_growth']['a0_clm']:+.1f}")


def test_20_an_unread_source_can_never_silently_answer_a_gate():
    from solver.certificate_shapes import SECOND_HAND, cp_literature_rows
    fl = [r for r in cp_literature_rows() if r["tag"] == "FL91"][0]
    assert fl["read_at"] == SECOND_HAND
    assert fl["rho"] is None, "an unread source must not carry a numeric rho"
    assert fl["arxiv"] is None and "paywalled" in fl["fetch"]
    print("  FL91 carries rho=None and is flagged SECOND_HAND with its reason")


def test_21_a_diagonal_weight_cannot_damp_a_nearest_neighbour_shift():
    """BRT's repair (Definition 2.8), applied to a shift, measured -- not asserted.

    This is WHY legs 51-53 measured "the coupling entry is K/2 for EVERY s".
    """
    from solver.certificate_shapes import shift_damping_ladder
    lad = shift_damping_ladder()
    for r in lad:
        # a repair would need the ratio -> 0.  It goes to 1, from below, for every p.
        assert r["ratio_at_largest_index"] > 0.999, (r["p"], r["ratio_at_largest_index"])
        assert r["distance_from_one_at_largest_index"] < 1e-3, r["p"]
        # and it is MONOTONE toward 1 in the index -- the damping gets worse, not better
        assert r["ratio"][-1] > r["ratio"][0] or r["p"] == 0.0, r["p"]
    worst = max(x["distance_from_one_at_largest_index"] for x in lad)
    print(f"  p in {[x['p'] for x in lad]}: at index 8192 the weight damps a "
          f"nearest-neighbour coupling by at most {worst:.2e}")


def test_22_the_same_weight_reproduces_BRTs_published_exponent_on_THEIR_operator():
    """The contrast that makes gate 21 a finding rather than an isolated fact.

    BRT eq. (2.8): the weighted row sum of their bounded, spread off-diagonal grows like
    `i^{p-q1}`.  Measured here and compared to their prediction.
    """
    from solver.certificate_shapes import spread_damping_ladder
    for p, q1 in ((1.7, 1.0), (1.2, 1.0), (2.5, 1.0)):
        d = spread_damping_ladder(p, q1)
        err = abs(d["measured_growth_exponent_in_i"]
                  - d["brt_predicted_exponent_p_minus_q1"])
        assert err < 5e-3, (p, q1, d["measured_growth_exponent_in_i"], err)
        print(f"  p={p}, q1={q1}: measured exponent "
              f"{d['measured_growth_exponent_in_i']:+.4f} vs BRT's p-q1 = "
              f"{d['brt_predicted_exponent_p_minus_q1']:+.4f}  (|err| {err:.1e})")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_every_row_is_traced_to_a_located_full_text_statement,
               test_2_every_row_has_a_resolvable_link,
               test_3_vocabulary_is_closed,
               test_4_gate_answers_no_on_the_published_record,
               test_5_gate_can_answer_yes_lesson_90,
               test_6_the_control_row_is_excluded_from_evidence,
               test_7_the_near_misses_are_near_misses_for_DIFFERENT_reasons,
               test_8_the_three_papers_are_classified_as_the_prose_says,
               test_9_bdl_ratio_is_infinite_at_zero_diagonal,
               test_10_shift_tail_block_is_not_boundedly_invertible,
               test_11_bordering_makes_it_exist_but_not_decay,
               test_12_a_nonzero_diagonal_restores_decay,
               test_13_the_shift_is_the_only_case_that_fails,
               test_14_bdl_threshold_is_NOT_where_the_behaviour_changes,
               test_15_decay_exponent_refuses_rather_than_returning_a_number,
               test_16_cp_rows_are_traced_and_disclose_their_reading_depth,
               test_17_the_gate_answers_no_and_names_what_it_refused,
               test_18_the_gate_can_answer_yes_lesson_90,
               test_19_the_dominance_ratio_separates_every_source_from_our_object,
               test_20_an_unread_source_can_never_silently_answer_a_gate,
               test_21_a_diagonal_weight_cannot_damp_a_nearest_neighbour_shift,
               test_22_the_same_weight_reproduces_BRTs_published_exponent_on_THEIR_operator):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
