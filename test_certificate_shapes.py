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

# Route-CP (leg 62) -- Cadiot arXiv:2505.03091's scope, gates 16-25
from solver.certificate_shapes import (
    CADIOT_SCOPE,
    CP_A1_GROWTH,
    CP_A1_LMIN,
    CP_CLASS,
    CP_FORWARD,
    CP_L31,
    CP_L32,
    CP_NOT_OBTAINED,
    CP_SYNTHETIC_COVERING_SCOPE,
    CP_SYSTEMS,
    cadiot_covers,
    cadiot_ratio_ladder,
    cadiot_shift_requirement,
    cadiot_symbol_admissibility,
    cadiot_vs_bdl_thresholds,
    cadiot_whitham_matrix,
    cp_unlocated_rows,
    our_operator_gershgorin,
    shift_requirement_ladder,
)
from solver.spectral_certificate import tail_block

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


# --------------------------------------------------------------------------
# ROUTE-CP (leg 62): CADIOT'S SCOPE
#
# Gates 16-19 guard the BOOKKEEPING (located clauses, a gate that answers both ways);
# gates 20-24 guard the MEASUREMENT (the paper's own constants re-derived, the mechanism
# checked as an identity rather than assumed, and the two published thresholds kept
# apart from the operator's own hinge).
# --------------------------------------------------------------------------
def test_16_every_cadiot_clause_is_traced_to_a_located_full_text_statement():
    """Same guard as gate 1, for Route-CP's clauses. Never an abstract."""
    assert cp_unlocated_rows() == [], cp_unlocated_rows()
    for c in CADIOT_SCOPE:
        assert c["where"] and c["quote"] and c["supports"], c["clause"]
        assert "abstract" not in c["where"].lower(), c["clause"]
    for f in CP_FORWARD:
        assert f["url"].startswith("https://arxiv.org/abs/"), f["tag"]
    assert "NOT OBTAINED" in CP_NOT_OBTAINED["status"]
    print(f"  {len(CADIOT_SCOPE)} clauses + {len(CP_FORWARD)} forward rows, all located; "
          f"Farid-Lancaster recorded NOT OBTAINED rather than glossed")


def test_17_the_cadiot_gate_answers_no_on_the_located_clauses():
    """Route-CP's gate, in DIRECTION.md's wording, answered off the ledger."""
    g = cadiot_covers()
    assert g["answer"] == "no", g
    assert g["n_clauses_failing"] == len(CADIOT_SCOPE), g
    assert g["forward_citations_relaxing_the_hypothesis"] == [], g
    assert set(g["clauses_that_fail_for_our_operator"]) == {
        CP_CLASS, CP_A1_LMIN, CP_A1_GROWTH, CP_L31, CP_L32, CP_SYSTEMS}
    print(f"  gate answers '{g['answer']}': {g['n_clauses_failing']} of "
          f"{len(g['clauses_examined'])} located clauses fail for our operator")


def test_18_the_cadiot_gate_can_answer_yes_lesson_90():
    """A gate that cannot come out the other way is not a gate. Both disjuncts live."""
    g = cadiot_covers(scope=CP_SYNTHETIC_COVERING_SCOPE)
    assert g["answer"] == "yes", g
    assert g["n_clauses_failing"] == 0, g

    relaxed = [dict(f) for f in CP_FORWARD]
    relaxed[0]["relaxes_the_hypothesis"] = True
    g2 = cadiot_covers(forward=relaxed)
    assert g2["answer"] == "yes", g2
    assert g2["forward_citations_relaxing_the_hypothesis"] == ["BCF"], g2
    print("  flips to yes two independent ways: a covering scope, and a forward "
          "citation that relaxes the hypothesis")


def test_19_the_control_scope_is_never_counted_as_evidence():
    """The fictitious clauses are not in the real scope ledger."""
    real = {c["clause"] for c in CADIOT_SCOPE}
    for c in CP_SYNTHETIC_COVERING_SCOPE:
        assert c["where"].startswith("(none"), c
    assert cadiot_covers()["answer"] == "no"
    assert len(real) == len(CADIOT_SCOPE), "duplicate clause ids"
    print(f"  {len(real)} distinct real clauses; the control cites nothing and is "
          f"passed explicitly or not at all")


def test_20_cadiots_own_constants_are_RE_DERIVED_not_quoted():
    """The paper states l_min in words for three of its four examples. Reproduce them.

    Whitham: 'notice that l(xi) >= l(0) = 1 - c = 0.2 for all xi in R'.
    Swift-Hohenberg: |l| = (1 - |2 pi xi|^2)^2 + mu >= mu, with mu = 0.28 and 0.32.
    """
    for name in ("SH_square", "SH_hexagonal", "Whitham"):
        a = cadiot_symbol_admissibility(name)
        stated = a["author_states"]["l_min"]
        assert abs(a["l_min"] - stated) < 1e-6, (name, a["l_min"], stated)
        assert a["growth_exponent"] > 0.4, (name, a["growth_exponent"])
        print(f"  {name:14s} l_min measured {a['l_min']:.6f} vs stated {stated} "
              f"(|diff| {abs(a['l_min'] - stated):.2e}), growth "
              f"{a['growth_exponent']:+.4f}")


def test_21_cadiots_ONE_systems_example_has_a_BOUNDED_off_diagonal():
    """Section 5.3 eq. (44): the off-diagonal is the constant lam1 lam2 - 1 = 1/9.

    This is the only place an off-diagonal entry appears anywhere in the paper, so if
    the framework reached an off-diagonal UNBOUNDED part it would have to be here.
    """
    a = cadiot_symbol_admissibility("GrayScott")
    assert a["is_matrix_symbol"]
    assert abs(a["offdiag_entry"] - 1.0 / 9.0) < 1e-12, a["offdiag_entry"]
    assert a["l_min"] > 0.99, a["l_min"]
    assert abs(a["growth_exponent"] - 2.0) < 1e-3, a["growth_exponent"]
    assert a["offdiag_over_diag_exponent"] < -1.9, a["offdiag_over_diag_exponent"]
    assert a["offdiag_over_diag_at_xi_max"] < 1e-8, a["offdiag_over_diag_at_xi_max"]
    print(f"  Gray-Scott offdiag = {a['offdiag_entry']:.6f} (constant), diagonal grows "
          f"{a['growth_exponent']:+.4f}; ratio exponent "
          f"{a['offdiag_over_diag_exponent']:+.4f}, "
          f"{a['offdiag_over_diag_at_xi_max']:.2e} at |xi| = {a['xi_max']:.0e}")


def test_22_lemma_3_2s_shift_SATURATES_for_cadiot_and_DIVERGES_for_us():
    """The load-bearing comparison, as two ladders and their exponents.

    Cadiot's own Whitham operator: one finite s serves every truncation.  Ours at
    mu = 0: the required |s| grows linearly with the truncation, so no s survives the
    limit and Lemma 3.2 cannot be entered at all.
    """
    lad_c = shift_requirement_ladder(cadiot_whitham_matrix, (128, 256, 512, 1024))
    assert lad_c["saturates"], lad_c
    assert abs(lad_c["exponent"]) < 1e-6, lad_c
    assert abs(lad_c["ratio_last_over_first"] - 1.0) < 1e-9, lad_c

    lad_o = shift_requirement_ladder(lambda M: tail_block(8, M, mu=0.0),
                                     (128, 256, 512, 1024, 2048))
    assert not lad_o["saturates"], lad_o
    assert lad_o["exponent"] > 0.95, lad_o
    assert lad_o["s_required"][-1] > 500.0, lad_o
    print(f"  Cadiot/Whitham |s| = {lad_c['s_required'][0]:.5f} at every N "
          f"(exponent {lad_c['exponent']:+.1e}); ours {lad_o['s_required'][0]:.0f} -> "
          f"{lad_o['s_required'][-1]:.0f} over M = 128..2048 "
          f"(exponent {lad_o['exponent']:+.4f})")


def test_23_the_control_MOVES_when_the_operator_moves_lesson_90():
    """Four identical numbers should read as a bug unless something makes them move.

    The saturating |s| above is identical across N.  That is saturation, not a tautology
    of the code -- and the proof is that it moves when the convolution's l^1 norm moves,
    while the ratio's EXPONENT does not (the numerator is exactly 2||V||_1 in the
    interior, so the exponent belongs to Cadiot's SYMBOL alone).
    """
    levels, exps = [], []
    for l1 in (0.05, 0.35, 2.0, 10.0):
        A = cadiot_whitham_matrix(512, kernel_l1=l1)
        levels.append(cadiot_shift_requirement(A))
        exps.append(cadiot_ratio_ladder(A, np.abs(np.arange(-512, 513)),
                                        hi_trim=8)["exponent"])
    assert levels[0] == 0.0 and levels[-1] > 9.0, levels
    assert levels[1] < levels[2] < levels[3], levels
    assert max(exps) - min(exps) < 1e-9, exps
    assert exps[0] < -0.5, exps
    # and the binding row is the one Assumption 1 is about: |s| = sqrt((r/2)^2 - l_min^2)
    predicted = float(np.sqrt((2 * 0.35 / 2.0) ** 2 - 0.2 ** 2))
    assert abs(levels[1] - predicted) < 1e-6, (levels[1], predicted)
    print(f"  |s| moves 0.0 -> {levels[-1]:.3f} with ||V||_1 while the exponent is "
          f"fixed at {exps[0]:+.6f}; and |s| = sqrt((r/2)^2 - l_min^2) = "
          f"{predicted:.5f} EXACTLY, i.e. the binding row is the one Assumption 1's "
          f"l_min = 0.2 is about")


def test_24_the_two_published_thresholds_are_not_the_operators_hinge():
    """Three numbers on one dial, kept apart on purpose.

    Cadiot's Lemma 3.2 admits this family for mu >= 1/2; BDL's assumption (5) only for
    mu > 1; and leg 57 measured the OPERATOR's own hinge at mu = 0 exactly.  Conflating
    them is how a hypothesis of a construction gets read as a property of an operator.
    """
    t = cadiot_vs_bdl_thresholds()
    assert t["factor_between_them"] == 2.0, t
    assert t["both_vacuous_at"] == 0.0 and t["leg_57_operator_hinge"] == 0.0

    # measured, not asserted: the identity r_k = k - 1 that produces the 1/2
    for mu in (0.25, 0.45, 1.0):
        g = our_operator_gershgorin(K=8, M=512, mu=mu)
        assert g["row_sum_identity_max_err_vs_k_minus_1"] < 1e-10, g
    below = shift_requirement_ladder(lambda M: tail_block(8, M, mu=0.45),
                                     (256, 512, 1024))
    at = shift_requirement_ladder(lambda M: tail_block(8, M, mu=0.5), (256, 512, 1024))
    assert not below["saturates"] and below["exponent"] > 0.95, below
    assert at["saturates"] and max(at["s_required"]) == 0.0, at
    assert our_operator_gershgorin(K=8, M=512, mu=0.0)["s_required"] > 250.0
    print(f"  mu = 0.45 diverges (exponent {below['exponent']:+.4f}), mu = 0.50 needs "
          f"|s| = 0 exactly; BDL needs mu > 1, factor "
          f"{t['factor_between_them']:.0f}; the operator's own hinge is mu = 0")


def test_25_the_ratio_ladder_refuses_at_an_exactly_zero_diagonal():
    """When a quantity has no referent, say so instead of bounding it (discipline 73)."""
    lad = cadiot_ratio_ladder(tail_block(8, 256, mu=0.0), np.arange(9, 257))
    assert lad["refused"] and lad["exponent"] is None, lad
    assert lad["n_infinite_rows"] == 248, lad
    ok = cadiot_ratio_ladder(tail_block(8, 256, mu=1.0), np.arange(9, 257), hi_trim=1)
    assert not ok["refused"] and abs(ok["exponent"]) < 0.01, ok
    # and the flatness is mu-INDEPENDENT: the level moves, the exponent does not, because
    # r_k = k - 1 exactly and the diagonal is mu*k (lesson 90 -- checked, not assumed).
    exps, levels = [], []
    for mu in (0.25, 0.5, 1.0, 2.0):
        lad = cadiot_ratio_ladder(tail_block(8, 512, mu=mu), np.arange(9, 513), hi_trim=1)
        exps.append(lad["exponent"])
        levels.append(lad["ratio_at_window_top"])
    assert max(exps) - min(exps) < 1e-9, exps
    assert levels[0] > 3.9 and levels[-1] < 0.51, levels
    print(f"  and the exponent is mu-independent ({exps[0]:+.4f} at every mu, spread "
          f"{max(exps) - min(exps):.1e}) while the LEVEL moves "
          f"{levels[0]:.3f} -> {levels[-1]:.3f}")
    print(f"  mu = 0: {lad['n_infinite_rows']} rows with an exactly zero diagonal, "
          f"exponent REFUSED; mu = 1: exponent {ok['exponent']:+.4f} (flat, not "
          f"decaying)")


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
               test_16_every_cadiot_clause_is_traced_to_a_located_full_text_statement,
               test_17_the_cadiot_gate_answers_no_on_the_located_clauses,
               test_18_the_cadiot_gate_can_answer_yes_lesson_90,
               test_19_the_control_scope_is_never_counted_as_evidence,
               test_20_cadiots_own_constants_are_RE_DERIVED_not_quoted,
               test_21_cadiots_ONE_systems_example_has_a_BOUNDED_off_diagonal,
               test_22_lemma_3_2s_shift_SATURATES_for_cadiot_and_DIVERGES_for_us,
               test_23_the_control_MOVES_when_the_operator_moves_lesson_90,
               test_24_the_two_published_thresholds_are_not_the_operators_hinge,
               test_25_the_ratio_ladder_refuses_at_an_exactly_zero_diagonal):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
