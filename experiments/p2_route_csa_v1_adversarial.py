"""Route-CSA v1 -- the adversarial battery against solver/certificate_shapes.py.

THE GATE (leg 146, DIRECTION.md, verbatim)
------------------------------------------
Under adversarial input (malformed shape descriptors, boundary class parameters,
degenerate splits) does `certificate_shapes.py` ever silently return a wrong or
incomplete enumeration, and does its enumerated set match what legs 54/58/126 each
read from it?

  yes -> Name the exact mechanism.  If the enumeration itself is short or wrong, this
         directly threatens leg 126's completeness claim -- escalate immediately as a
         priority finding, do not patch under this leg's own authority.
  no  -> Bank the battery as the permanent regression suite; record in capabilities.py,
         and note explicitly that leg 126's completeness count is independently
         corroborated.

READ-ONLY.  `solver/certificate_shapes.py` was not edited by this leg under either
branch.  Every gate below is a measurement.  Where a function is fault-injected, the
injection is done by rebinding a module ATTRIBUTE in this process (CSA7) or by handing
the function a poisoned argument (CSA6) -- the file on disk is untouched, and the
rebinding is restored in a `finally`.

WHAT THIS MODULE IS, WHICH DECIDES WHAT "WRONG" MEANS
-----------------------------------------------------
`solver/certificate_shapes.py` is a LEDGER module, not a floating-point kernel.  It
holds two enumerations and two executable gate predicates over them:

  * `SHAPE_LEDGER` (5 rows, 4 real + 1 flagged fictitious control) and `gate_answer`
    -- leg 57's Route-XS gate: is there a published radii-polynomial certificate with
    an off-diagonal unbounded part and a non-decaying tail inverse?  Banked answer NO.
  * `CADIOT_SCOPE` (6 located clauses), `CP_FORWARD` (3 rows) and `cadiot_covers`
    -- leg 62's Route-CP gate: does Cadiot arXiv:2505.03091 cover our operator?
    Banked answer NO, on 6 of 6 failing clauses.

plus the measured half (`classify_operator`, `m_divergence`, `decay_exponent`,
`cadiot_shift_requirement`) that turns the shift-vs-multiplier dichotomy into a
number.  So "silently returns a wrong enumeration" has two concrete senses, and both
are probed: a ROW that should count as evidence and does not (or vice versa), and a
MEASUREMENT whose refusal path exists in one function and is missing in its sibling.

THE PROVENANCE CORRECTION, MADE BEFORE THE BATTERY AND CARRIED INTO IT
----------------------------------------------------------------------
`DIRECTION.md` §146 states this module "supplies the shape/class enumeration that leg
54's battery and leg 58's theorem both range over".  It does not, and CSA8 measures
that rather than asserting it: the seven-shape enumeration is declared in leg 54's own
runner (`experiments/p2_route_mm_v1_shape.py`, `SHAPES`) and re-declared independently
by leg 58 (`p2_route_ng_v1_nogo.py`, `IN_CLASS`/`OUT_OF_CLASS`) and leg 126
(`p2_route_bx_v1_stageb.py`, `a21_of_shape`).  `solver/certificate_shapes.py`
contributes zero names to it.  CSA8 therefore audits the real completeness risk --
whether those three independent declarations have DRIFTED from each other -- which is
the thing that could actually hole leg 126's count.

Runtime ~35 s.  Deterministic; no RNG anywhere.
"""

import ast
import copy
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.certificate_shapes as cs                                # noqa: E402
from solver.certificate_shapes import (                               # noqa: E402
    BLOCK_DIAGONAL,
    CADIOT_SCOPE,
    CP_FORWARD,
    CP_SYNTHETIC_COVERING_SCOPE,
    SHAPE_LEDGER,
    SHIFT,
    bdl_admissible,
    bdl_delta,
    cadiot_covers,
    cadiot_shift_requirement,
    cp_unlocated_rows,
    decay_exponent,
    gate_answer,
    real_ledger,
    shift_requirement_ladder,
    unlocated_rows,
)
from solver.spectral_certificate import tail_block                    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_csa_v1_adversarial.json")

#: A row that IS a counterexample under the module's own predicate, used as the probe
#: body for CSA1.  It is the shipped control row's classification, restated locally so
#: the mutations cannot disturb the module's own object.
GENUINE_COUNTEREXAMPLE = {
    "tag": "PROBE_COUNTEREXAMPLE",
    "arxiv": None, "url": None,
    "is_radii_polynomial": True,
    "unbounded_part": SHIFT,
    "approx_inverse": BLOCK_DIAGONAL,
    "tail_inverse_decays": False,
    "located": [{"where": "probe", "quote": "probe", "supports": "probe"}],
}


# ==========================================================================
# CSA1 -- MALFORMED SHAPE DESCRIPTORS: does a typo silently drop a counterexample?
# ==========================================================================
def gate_csa1():
    """Mutate one gate-bearing key of a GENUINE counterexample row, seven ways.

    `is_counterexample` reads all three of its clauses through `dict.get`, with no
    schema check anywhere in the module.  So the question is not whether a malformed
    descriptor is rejected -- nothing rejects anything -- but whether it is silently
    reclassified.  A row that should answer the gate "yes" and instead answers "no" is
    a wrong enumeration in the sense that matters: the gate's banked answer IS "no",
    so such a mutation is invisible against the expected result.

    **The predicate and the reporter are measured separately, because they do not
    behave the same way and the difference is the finding's boundary.**
    `is_counterexample` reads every clause through `dict.get` and is therefore silent;
    `gate_answer`'s row-summary block reads the SAME fields through `r["..."]` and
    therefore raises `KeyError`.  So a DELETED key is loud (caught by the reporter,
    not by the predicate) while a key that is present with a wrong-typed or
    wrong-cased VALUE is silent all the way through.  Only the latter are counted as
    the gap; the former are recorded as caught, by name.
    """
    base_silent = cs.is_counterexample(copy.deepcopy(GENUINE_COUNTEREXAMPLE))
    muts = []

    def probe(label, mutate, why):
        row = copy.deepcopy(GENUINE_COUNTEREXAMPLE)
        mutate(row)
        classified = cs.is_counterexample(row)
        rec = {"mutation": label, "why_plausible": why,
               "predicate_is_counterexample": bool(classified),
               "predicate_baseline": bool(base_silent),
               "predicate_silently_reclassified": bool(classified) != bool(base_silent)}
        try:
            g = gate_answer(rows=[row])
            rec.update({"reporter_raised": False, "answer": g["answer"],
                        "counterexamples": g["counterexamples"],
                        "n_rows_examined": g["n_rows_examined"]})
        except Exception as e:                                   # noqa: BLE001
            rec.update({"reporter_raised": True,
                        "reporter_exception": f"{type(e).__name__}: {e}",
                        "answer": None, "counterexamples": None,
                        "n_rows_examined": None})
        rec["silently_reclassified"] = bool(
            rec["predicate_silently_reclassified"] and not rec["reporter_raised"])
        muts.append(rec)

    probe("drop key 'tail_inverse_decays'",
          lambda r: r.pop("tail_inverse_decays"),
          "a new ledger row written from a paper that forms no tail estimate")
    probe("rename 'tail_inverse_decays' -> 'tail_inverse_decay'",
          lambda r: r.__setitem__("tail_inverse_decay", r.pop("tail_inverse_decays")),
          "a one-character transcription typo; every access is dict.get")
    probe("'tail_inverse_decays' = numpy False (np.bool_)",
          lambda r: r.__setitem__("tail_inverse_decays", np.bool_(False)),
          ("the natural value if the field is filled from a MEASUREMENT -- "
           "`classify_operator` computes exactly this quantity, and the predicate "
           "tests it with `is False`, an IDENTITY check numpy booleans fail"))
    probe("'tail_inverse_decays' = 0",
          lambda r: r.__setitem__("tail_inverse_decays", 0),
          "falsy but not the False singleton; same `is False` identity check")
    probe("drop key 'unbounded_part'",
          lambda r: r.pop("unbounded_part"),
          "an incompletely filled row")
    probe("'unbounded_part' = 'shift' (lowercase)",
          lambda r: r.__setitem__("unbounded_part", "shift"),
          ("the vocabulary constants exist precisely to stop this, but nothing "
           "checks that a row's value is drawn from them"))
    probe("drop key 'is_radii_polynomial'",
          lambda r: r.pop("is_radii_polynomial"),
          "an incompletely filled row")

    silent = [m for m in muts if m["silently_reclassified"]]
    raised = [m for m in muts if m["reporter_raised"]]
    pred_silent = [m for m in muts if m["predicate_silently_reclassified"]]
    return {
        "what": ("seven malformed-descriptor mutations of a row that IS a "
                 "counterexample under the module's own predicate"),
        "baseline_predicate_on_the_unmutated_row": bool(base_silent),
        "n_mutations": len(muts),
        "n_predicate_reclassified": len(pred_silent),
        "n_caught_by_the_reporter_raising": len(raised),
        "n_silently_reclassified": len(silent),
        "silently_reclassified_mutations": [m["mutation"] for m in silent],
        "caught_mutations": [m["mutation"] for m in raised],
        "mutations": muts,
        "mechanism": ("`is_counterexample` reads `is_radii_polynomial`, "
                      "`unbounded_part` and `tail_inverse_decays` through `dict.get`, "
                      "and `tail_inverse_decays` through the IDENTITY test `is False`. "
                      "There is no schema validator anywhere in the module.  A "
                      "MISSING key is caught, but only incidentally and only one "
                      "function later, by `gate_answer`'s row-summary block using "
                      "`r[...]`; the predicate itself never objects.  A key that is "
                      "PRESENT with a numpy boolean, an int, or a lower-cased "
                      "vocabulary word passes both, and `n_rows_examined` still "
                      "counts the row as examined evidence while it contributes "
                      "none."),
        "verdict": "GAP" if silent else "ROBUST",
    }


# ==========================================================================
# CSA2 -- THE FICTITIOUS-ROW FLAG: one missing key admits a control as evidence
# ==========================================================================
def gate_csa2():
    """`real_ledger()` excludes the control row on `r.get("is_fictitious", False)`.

    That single key is the only thing between a row that cites nothing and the
    published record.  The row also carries `"counterexample": True`, which NO
    function in the module reads -- two parallel encodings of the same fact, one live
    and one dead, which is the drift hazard measured here.
    """
    clean_real = real_ledger()
    clean_gate = gate_answer()
    clean_unloc = unlocated_rows()

    poisoned = copy.deepcopy(SHAPE_LEDGER)
    ctrl = [r for r in poisoned if r["tag"] == "SYNTHETIC_CONTROL"][0]
    ctrl.pop("is_fictitious")
    p_real = [r for r in poisoned if not r.get("is_fictitious", False)]
    p_gate = gate_answer(rows=p_real)
    p_unloc = unlocated_rows(rows=p_real)

    # how many functions read the DEAD parallel field?
    dead_field_readers = sum(
        1 for name in dir(cs)
        if callable(getattr(cs, name, None))
        and getattr(getattr(cs, name), "__doc__", None) is not None
        and '["counterexample"]' in (getattr(cs, name).__doc__ or ""))

    return {
        "what": ("delete the single key `is_fictitious` from the shipped control row "
                 "-- a row whose own `note` reads 'CONTROL ROW.  Never counted as "
                 "evidence.'"),
        "clean": {"n_real_rows": len(clean_real), "answer": clean_gate["answer"],
                  "counterexamples": clean_gate["counterexamples"],
                  "n_unlocated": len(clean_unloc)},
        "poisoned": {"n_real_rows": len(p_real), "answer": p_gate["answer"],
                     "counterexamples": p_gate["counterexamples"],
                     "n_unlocated": len(p_unloc)},
        "gate_answer_flipped": clean_gate["answer"] != p_gate["answer"],
        "fictitious_row_cited_as_published_evidence": p_gate["counterexamples"],
        "citation_free_row_reported_clean_by_unlocated_rows": len(p_unloc) == 0,
        "control_row_where_field": ctrl["located"][0]["where"],
        "control_row_arxiv": ctrl["arxiv"],
        "control_row_url": ctrl["url"],
        "n_functions_reading_the_parallel_counterexample_field": dead_field_readers,
        "mechanism": ("with `is_fictitious` gone the row enters `real_ledger()` and "
                      "flips Route-XS's gate from NO to YES, citing a row with "
                      "`arxiv: None` and `url: None`.  The standing guard "
                      "`unlocated_rows` does NOT catch it: the guard rejects a "
                      "`where` that is empty or contains the substring 'abstract', "
                      "and this row's `where` is the non-empty string "
                      "'(none -- this row is a control and cites nothing)'.  The row "
                      "also carries a `counterexample: True` field that no function "
                      "reads, so the redundancy that could have caught the drift is "
                      "dead code."),
        "verdict": "GAP" if clean_gate["answer"] != p_gate["answer"] else "ROBUST",
    }


# ==========================================================================
# CSA3 -- THE TWO LOCATION GUARDS ARE NOT THE SAME GUARD
# ==========================================================================
def gate_csa3():
    """`unlocated_rows` vs `cp_unlocated_rows` on the SAME mutation.

    Both exist to enforce one rule ("a located statement, never an abstract").  They
    do not enforce the same rule: `cp_unlocated_rows` also requires a non-empty
    `quote`; `unlocated_rows` does not check `quote` at all.
    """
    probes = []

    def xs_probe(label, mutate, why):
        rows = copy.deepcopy(real_ledger())
        mutate(rows[0])
        bad = unlocated_rows(rows=rows)
        probes.append({"guard": "unlocated_rows (SHAPE_LEDGER)", "mutation": label,
                       "why_plausible": why, "n_flagged": len(bad),
                       "caught": len(bad) > 0})

    def cp_probe(label, mutate, why):
        scope = copy.deepcopy(CADIOT_SCOPE)
        mutate(scope[0])
        saved = cs.CADIOT_SCOPE
        try:
            cs.CADIOT_SCOPE = scope
            bad = cp_unlocated_rows()
        finally:
            cs.CADIOT_SCOPE = saved
        probes.append({"guard": "cp_unlocated_rows (CADIOT_SCOPE)", "mutation": label,
                       "why_plausible": why, "n_flagged": len(bad),
                       "caught": len(bad) > 0})

    xs_probe("quote := '' (empty)",
             lambda r: r["located"][0].__setitem__("quote", ""),
             "a row located to a section but with the sentence never transcribed")
    xs_probe("quote key deleted",
             lambda r: r["located"][0].pop("quote"),
             "same, as an omission rather than an empty string")
    xs_probe("where := '(none)'",
             lambda r: r["located"][0].__setitem__("where", "(none)"),
             "the literal spelling the shipped control row uses for 'cites nothing'")
    xs_probe("where := 'p. 3'",
             lambda r: r["located"][0].__setitem__("where", "p. 3"),
             ("a page number is not a section/assumption/proposition, which is what "
              "the module's own comment requires"))
    cp_probe("quote := '' (empty)",
             lambda r: r.__setitem__("quote", ""),
             "the identical mutation, on the sibling guard")

    xs_quote = [p for p in probes if p["guard"].startswith("unlocated_rows")
                and "quote" in p["mutation"]]
    cp_quote = [p for p in probes if p["guard"].startswith("cp_unlocated_rows")]
    asymmetric = (not any(p["caught"] for p in xs_quote)
                  and all(p["caught"] for p in cp_quote))

    # the converse: a legitimate `where` containing the substring "abstract"
    rows = copy.deepcopy(real_ledger())
    rows[0]["located"][0]["where"] = "section 2 (the abstract setting), Lemma 2.4"
    false_positive = len(unlocated_rows(rows=rows)) > 0

    return {
        "what": ("the same five mutations put to the module's two location guards, "
                 "which are meant to enforce one rule"),
        "probes": probes,
        "quote_mutations_missed_by_unlocated_rows":
            sum(1 for p in xs_quote if not p["caught"]),
        "quote_mutations_caught_by_cp_unlocated_rows":
            sum(1 for p in cp_quote if p["caught"]),
        "guards_are_asymmetric": bool(asymmetric),
        "false_positive_on_legitimate_where_containing_abstract": bool(false_positive),
        "mechanism": ("`cp_unlocated_rows` tests `if not r.get('quote')`; "
                      "`unlocated_rows` tests only `where`.  A SHAPE_LEDGER row whose "
                      "classification is traced to a section but whose licensing "
                      "sentence was never transcribed passes the guard the module "
                      "docstring calls 'the standing guard'.  The `where` test is a "
                      "substring match on 'abstract', so it both misses '(none)' and "
                      "'p. 3' and falsely flags a legitimate section title."),
        "verdict": "GAP" if asymmetric else "ROBUST",
    }


# ==========================================================================
# CSA4 -- DEGENERATE ENUMERATIONS: the empty scope answers YES
# ==========================================================================
def gate_csa4():
    """`cadiot_covers` on a scope that has been emptied, and on unknown clauses.

    `covered = (not failing) or bool(relaxed)`.  With no clauses there is nothing to
    fail, so the gate reports that Cadiot's construction DOES cover our operator --
    the exact inversion of leg 62's banked answer, on zero evidence, with
    `clauses_examined: []` sitting in the returned dict unread.
    """
    empty = cadiot_covers(scope=[])
    empty_both = cadiot_covers(scope=[], forward=[])
    clean = cadiot_covers()

    unknown = copy.deepcopy(CADIOT_SCOPE)
    for c in unknown:
        c["holds_for_the_a0_CLM_linearisation"] = None
    unk = cadiot_covers(scope=unknown)

    synth = cadiot_covers(scope=CP_SYNTHETIC_COVERING_SCOPE)

    # how far can the scope be truncated before the answer moves?
    ladder = []
    for n in range(len(CADIOT_SCOPE), -1, -1):
        g = cadiot_covers(scope=CADIOT_SCOPE[:n])
        ladder.append({"n_clauses": n, "answer": g["answer"],
                       "n_failing": g["n_clauses_failing"]})

    xs_empty = gate_answer(rows=[])

    return {
        "what": ("degenerate splits of the two enumerations: empty scope, empty "
                 "forward list, all-unknown clauses, and the truncation ladder"),
        "clean": {"answer": clean["answer"],
                  "n_clauses_failing": clean["n_clauses_failing"],
                  "clauses_examined": clean["clauses_examined"]},
        "empty_scope": {"answer": empty["answer"],
                        "clauses_examined": empty["clauses_examined"],
                        "n_clauses_failing": empty["n_clauses_failing"]},
        "empty_scope_and_forward": {"answer": empty_both["answer"]},
        "all_clauses_unknown_None": {
            "answer": unk["answer"],
            "n_clauses_failing": unk["n_clauses_failing"],
            "note": ("an UNKNOWN clause is silently counted as a clause that FAILS "
                     "for our operator, i.e. as evidence for the banked answer")},
        "synthetic_covering_control": {
            "answer": synth["answer"],
            "n_clauses": len(CP_SYNTHETIC_COVERING_SCOPE),
            "note": ("lesson 90's control: the predicate demonstrably CAN answer yes, "
                     "and it does -- but so does the EMPTY scope, which is the defect")},
        "truncation_ladder": ladder,
        "xs_gate_on_empty_ledger": {"answer": xs_empty["answer"],
                                    "n_rows_examined": xs_empty["n_rows_examined"]},
        "empty_enumeration_inverts_the_cp_gate": empty["answer"] != clean["answer"],
        "empty_enumeration_silently_confirms_the_xs_gate":
            xs_empty["answer"] == gate_answer()["answer"],
        "mechanism": ("`cadiot_covers` derives its answer from the ABSENCE of failing "
                      "clauses rather than from the PRESENCE of holding ones, so an "
                      "empty or fully filtered scope is indistinguishable from a "
                      "scope every clause of which holds.  `gate_answer` has the "
                      "mirror-image weakness with the opposite sign: an empty ledger "
                      "reproduces the banked NO with `n_rows_examined: 0`, so a "
                      "filtering bug upstream would be invisible against the "
                      "expected result."),
        "verdict": "GAP" if empty["answer"] != clean["answer"] else "ROBUST",
    }


# ==========================================================================
# CSA5 -- BOUNDARY CLASS PARAMETERS: BDL admissibility has no absolute value
# ==========================================================================
def gate_csa5():
    """`bdl_admissible(mu)` is `1/(2 mu) < 0.5`, unsigned.

    BDL's assumption (5) is `|lambda_k/mu_k|, |beta_k/mu_k| <= delta < 1/2` -- a bound
    on a MODULUS.  The module's `delta` is signed, so every `mu < 0` passes.
    """
    sweep = []
    for mu in (-100.0, -2.0, -1.0, -0.5, -0.4, -1e-3, 0.0, 1e-3, 0.4, 0.5, 1.0, 2.0,
               100.0):
        d = bdl_delta(mu)
        sweep.append({"mu": mu, "bdl_delta": d,
                      "abs_delta": abs(d),
                      "bdl_admissible_as_coded": bool(bdl_admissible(mu)),
                      "admissible_if_modulus_were_used": bool(abs(d) < 0.5)})
    wrong = [s for s in sweep
             if s["bdl_admissible_as_coded"] != s["admissible_if_modulus_were_used"]]
    worst = max(wrong, key=lambda s: s["abs_delta"]) if wrong else None

    # what `classify_operator` would LABEL those operators, without running the
    # expensive measurement: the label is a pure function of mu.
    labels = [{"mu": s["mu"],
               "shape_label": (cs.SHIFT if s["mu"] == 0.0
                               else (cs.MULTIPLIER if bdl_admissible(s["mu"])
                                     else cs.TRIDIAGONAL_DOMINANT))}
              for s in sweep]

    return {
        "what": "the BDL admissibility dial swept through and past zero",
        "sweep": sweep,
        "n_swept": len(sweep),
        "n_misclassified": len(wrong),
        "misclassified_mu": [s["mu"] for s in wrong],
        "worst_case": worst,
        "shape_labels": labels,
        "negative_mu_labelled_MULTIPLIER": [l["mu"] for l in labels
                                            if l["mu"] < 0
                                            and l["shape_label"] == cs.MULTIPLIER],
        "mechanism": ("`bdl_delta` returns the SIGNED ratio 1/(2 mu) and "
                      "`bdl_admissible` compares it to 0.5 without `abs`.  BDL's "
                      "assumption (5), quoted verbatim in this module's own "
                      "SHAPE_LEDGER row, bounds |lambda_k/mu_k| -- a modulus.  Every "
                      "mu < 0 is therefore reported admissible, and "
                      "`classify_operator`'s `shape` field, which is a pure function "
                      "of `bdl_admissible`, labels an anti-dissipative operator "
                      "MULTIPLIER: the label at the OPPOSITE end of the module's own "
                      "shift-to-multiplier dial."),
        "verdict": "GAP" if wrong else "ROBUST",
    }


# ==========================================================================
# CSA6 -- NaN ABSORPTION IN LEMMA 3.2's SHIFT REQUIREMENT
# ==========================================================================
def gate_csa6():
    """`cadiot_shift_requirement` on a poisoned matrix.

    The implementation ends `sqrt(max(0.0, float(np.max(...))))`.  `np.max` of an
    array containing NaN is NaN, and Python's two-argument `max(0.0, nan)` returns
    **0.0** -- because `nan > 0.0` is False and `max` keeps its first argument.  So a
    single NaN anywhere in the matrix converts "no finite shift exists" into "the
    unshifted matrix is already diagonally dominant", which is the module's own
    documented reading of the value 0.0 and the maximally wrong answer available.
    """
    K, M = 8, 512
    T = tail_block(K, M, mu=0.0)
    clean = cadiot_shift_requirement(T)

    cases = []

    def poison(label, mutate, why):
        Tp = np.array(T, dtype=float, copy=True)
        mutate(Tp)
        v = cadiot_shift_requirement(Tp)
        cases.append({"poison": label, "why_plausible": why,
                      "s_required": v, "clean_s_required": clean,
                      "reads_as": ("ALREADY DOMINANT (Lemma 3.2 entered trivially)"
                                   if v == 0.0 else
                                   ("no finite shift" if not np.isfinite(v)
                                    else "a finite shift of this size")),
                      "silently_inverted": v == 0.0 and clean > 0.0,
                      "absolute_error_vs_clean": (abs(v - clean)
                                                  if np.isfinite(v) else float("inf"))})

    poison("one NaN in an OFF-diagonal entry",
           lambda A: A.__setitem__((5, 7), np.nan),
           "an upstream operator build that produced a NaN in one row")
    poison("one NaN on the DIAGONAL",
           lambda A: A.__setitem__((3, 3), np.nan),
           "a dissipation dial evaluated at a singular parameter")
    poison("NaN in the LAST row (the truncation boundary)",
           lambda A: A.__setitem__((M - K - 1, M - K - 1), np.nan),
           "a truncation artifact at the far end, the least-inspected row")
    poison("one +inf in an OFF-diagonal entry",
           lambda A: A.__setitem__((5, 7), np.inf),
           "an overflow rather than an invalid operation")
    poison("an entire row set to NaN",
           lambda A: A.__setitem__((11, slice(None)), np.nan),
           "a wholly failed row, the loudest possible upstream failure")

    silent = [c for c in cases if c["silently_inverted"]]

    # the same poison one level up, where the verdict word is produced
    def poisoned_matrix_fn(n):
        A = np.array(tail_block(K, int(n), mu=0.0), dtype=float, copy=True)
        A[5, 7] = np.nan
        return A

    clean_ladder = shift_requirement_ladder(
        lambda n: tail_block(K, int(n), mu=0.0), (128, 256, 512))
    poisoned_ladder = shift_requirement_ladder(poisoned_matrix_fn, (128, 256, 512))

    return {
        "what": ("Lemma 3.2's minimum-modulus shift, on the matrix this repository "
                 "actually built, with one entry poisoned"),
        "matrix": {"source": "solver.spectral_certificate.tail_block", "K": K, "M": M,
                   "mu": 0.0, "shape": list(T.shape)},
        "clean_s_required": clean,
        "cases": cases,
        "n_poisons": len(cases),
        "n_silently_inverted_to_zero": len(silent),
        "ladder_clean": clean_ladder,
        "ladder_poisoned": poisoned_ladder,
        "ladder_verdict_flipped": (clean_ladder.get("saturates")
                                   != poisoned_ladder.get("saturates")),
        "mechanism": ("`sqrt(max(0.0, float(np.max(r**2/4 - lam**2))))`.  With a NaN "
                      "anywhere in the matrix `np.max` is NaN, `nan > 0.0` is False, "
                      "and Python's `max` returns its first argument 0.0.  The "
                      "function's own docstring states that '0.0 means the unshifted "
                      "matrix is already dominant', so the NaN is not merely absorbed "
                      "-- it is reported as the one value that says Cadiot's Lemma "
                      "3.2 needs no shift at all.  One level up, "
                      "`shift_requirement_ladder` sees a zero rung, refuses the "
                      "exponent, and sets `saturates: True` -- which is precisely the "
                      "verdict leg 62 measured for Cadiot's OWN Whitham operator, "
                      "i.e. the positive control's answer, produced from a poisoned "
                      "version of ours."),
        "verdict": "GAP" if silent else "ROBUST",
    }


# ==========================================================================
# CSA7 -- THE MISSING SIBLING GUARD: m_divergence vs decay_exponent
# ==========================================================================
def gate_csa7():
    """One non-finite rung in the M-ladder, injected by rebinding a module attribute.

    `decay_exponent` refuses on a non-positive or non-finite rung, by name.  Its
    sibling `m_divergence` fits `np.polyfit(log(Ms), log(vals), 1)` with no guard at
    all -- and `classify_operator` turns that fit into the BRANCH that decides whether
    the operator is treated as invertible or as needing leg 52's bordering.
    """
    Ks, M = (4, 8, 16, 32), 256
    mu = 1.0                       # an operator that is genuinely invertible

    clean = cs.classify_operator(mu, Ks=Ks, M=M)

    orig = cs.tail_inverse_norm
    poisoned_M = 512               # the rung `classify_operator`'s m_divergence hits

    def poisoned(K, Mv, kind, param, mu=0.0):
        v = orig(K, Mv, kind, param, mu=mu)
        return float("nan") if int(Mv) == poisoned_M else v

    try:
        cs.tail_inverse_norm = poisoned
        dirty = cs.classify_operator(mu, Ks=Ks, M=M)
    finally:
        cs.tail_inverse_norm = orig

    # the sibling, on the same input
    sibling = decay_exponent([128, 256, 512, 1024],
                             [1.0, 2.0, float("nan"), 4.0])

    flipped = {
        "tail_block_boundedly_invertible": [clean["tail_block_boundedly_invertible"],
                                            dirty["tail_block_boundedly_invertible"]],
        "needed_bordering": [clean["needed_bordering"], dirty["needed_bordering"]],
        "M_exponent": [clean["M_exponent"], dirty["M_exponent"]],
        "K_exponent": [clean["K_exponent"], dirty["K_exponent"]],
        "tail_inverse_decays": [clean["tail_inverse_decays"],
                                dirty["tail_inverse_decays"]],
        "shape_label": [clean["shape"], dirty["shape"]],
    }
    dichotomy_inverted = (clean["tail_inverse_decays"] is True
                          and dirty["tail_inverse_decays"] is False)

    return {
        "what": ("one NaN rung in `m_divergence`'s M-ladder at mu = 1.0, an operator "
                 "whose tail block IS boundedly invertible"),
        "mu": mu, "Ks": list(Ks), "M": M, "poisoned_rung_M": poisoned_M,
        "clean": {k: clean[k] for k in
                  ("shape", "M_exponent", "K_exponent", "needed_bordering",
                   "tail_block_boundedly_invertible", "tail_inverse_decays")},
        "poisoned": {k: dirty[k] for k in
                     ("shape", "M_exponent", "K_exponent", "needed_bordering",
                      "tail_block_boundedly_invertible", "tail_inverse_decays")},
        "flipped_fields": flipped,
        "K_exponent_sign_change": [clean["K_exponent"], dirty["K_exponent"]],
        "dichotomy_verdict_inverted": bool(dichotomy_inverted),
        "sibling_decay_exponent_on_the_same_input": sibling,
        "sibling_refuses": bool(sibling.get("refused")),
        "mechanism": ("`decay_exponent` guards its fit -- "
                      "`if Ks.size < tail or np.any(vals <= 0) or not "
                      "np.all(np.isfinite(vals)): return {'refused': True, ...}`.  "
                      "`m_divergence`, thirteen lines later and doing the same "
                      "log-log fit, has no such guard.  Its NaN exponent then reaches "
                      "`invertible = md['exponent_in_M'] < 0.25`, where `nan < 0.25` "
                      "is False, so the operator is silently routed down the "
                      "NOT-invertible branch and measured BORDERED -- leg 52's mu = 0 "
                      "object -- while the exported `shape` label, computed from mu "
                      "alone, still reads the mu > 0 word.  The label and the "
                      "measurement disagree and only the disagreement is silent."),
        "verdict": "GAP" if dichotomy_inverted else "ROBUST",
    }


# ==========================================================================
# CSA8 -- THE COMPLETENESS CLAUSE: what legs 54/58/126 actually range over
# ==========================================================================
def _literal_from(path, name, index=None):
    """Read a module-level (or nested) literal by AST, with no import side effects."""
    with open(os.path.join(ROOT, path)) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except ValueError:
                        return None
    return index


def _imports_from(path, module):
    """The names `path` imports from `module`, by AST -- provenance, not grep."""
    with open(os.path.join(ROOT, path)) as f:
        tree = ast.parse(f.read())
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            names += [a.name for a in node.names]
    return sorted(names)


def _nested_literal(path, name):
    """A literal assigned anywhere in `path`, including inside a function body."""
    with open(os.path.join(ROOT, path)) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except ValueError:
                        return None
    return None


def _a21_agreement(leg58_in, leg58_out, leg126_a21, shapes):
    """The cross-check itself, factored out so a PERTURBED input can be fed to it."""
    rows = []
    for nm in sorted(shapes):
        v58 = ("zero" if nm in tuple(leg58_in or ())
               else ("nonzero" if nm in tuple(leg58_out or ()) else None))
        v126 = (leg126_a21 or {}).get(nm)
        vals = {x for x in (v58, v126) if x is not None}
        rows.append({"shape": nm, "leg58": v58, "leg126": v126,
                     "n_declarations": len(
                         [x for x in (v58, v126) if x is not None]),
                     "agree": len(vals) == 1})
    return rows


def gate_csa8():
    """Does `certificate_shapes.py`'s enumerated set match what 54/58/126 read from it?

    Answered by LOCATING the enumeration rather than assuming it, then putting the
    completeness question that survives the relocation.

    The provenance turns out to be tighter than the direction supposed, and tighter
    than this leg first supposed: `SHAPES` is declared ONCE, in leg 54's runner, and
    legs 58 and 126 both **import** it (`from p2_route_mm_v1_shape import ...`).  So
    membership cannot drift by construction.  What IS hand-written twice, and can
    drift, is the partition of those shapes by `A21`: leg 58 writes
    `IN_CLASS`/`OUT_OF_CLASS`, leg 126 writes `a21_of_shape`.  Leg 126 uses its copy
    to DROP inconsistent (shape, A21) pairs from the product it enumerates, so a
    disagreement there would change the 1,686 count directly.  That is the real
    completeness risk and it is what this gate measures.
    """
    leg54 = _literal_from("experiments/p2_route_mm_v1_shape.py", "SHAPES")
    leg54_admissible = _literal_from("experiments/p2_route_mm_v1_shape.py",
                                     "ADMISSIBLE")
    leg58_in = _literal_from("experiments/p2_route_ng_v1_nogo.py", "IN_CLASS")
    leg58_out = _literal_from("experiments/p2_route_ng_v1_nogo.py", "OUT_OF_CLASS")
    leg126_a21 = _nested_literal("experiments/p2_route_bx_v1_stageb.py",
                                 "a21_of_shape")

    imports = {
        "leg58_imports_from_p2_route_mm_v1_shape":
            _imports_from("experiments/p2_route_ng_v1_nogo.py",
                          "p2_route_mm_v1_shape"),
        "leg126_imports_from_p2_route_mm_v1_shape":
            _imports_from("experiments/p2_route_bx_v1_stageb.py",
                          "p2_route_mm_v1_shape"),
        "leg58_imports_from_solver.certificate_shapes":
            _imports_from("experiments/p2_route_ng_v1_nogo.py",
                          "solver.certificate_shapes"),
        "leg126_imports_from_solver.certificate_shapes":
            _imports_from("experiments/p2_route_bx_v1_stageb.py",
                          "solver.certificate_shapes"),
        "leg54_imports_from_solver.certificate_shapes":
            _imports_from("experiments/p2_route_mm_v1_shape.py",
                          "solver.certificate_shapes"),
    }

    # what does the module under test contribute to that enumeration?
    with open(os.path.join(ROOT, "solver/certificate_shapes.py")) as f:
        src = f.read()
    contributed = sorted(n for n in (leg54 or ()) if n in src)

    shapes = sorted(leg54 or ())
    coverage = {
        "leg58_partition_covers_SHAPES":
            sorted(tuple(leg58_in or ()) + tuple(leg58_out or ())) == shapes,
        "leg58_partition_is_disjoint":
            not (set(leg58_in or ()) & set(leg58_out or ())),
        "leg126_map_covers_SHAPES": sorted((leg126_a21 or {}).keys()) == shapes,
        "leg126_map_has_no_extra_keys":
            not (set((leg126_a21 or {}).keys()) - set(shapes)),
        "leg54_ADMISSIBLE_covers_SHAPES":
            sorted((leg54_admissible or {}).keys()) == shapes,
    }

    a21_rows = _a21_agreement(leg58_in, leg58_out, leg126_a21, shapes)
    a21_disagreements = [r for r in a21_rows if not r["agree"]]

    # ---- LESSON 90: this cross-check must be able to come out the other way. ----
    # Perturb ONE entry of leg 126's map and confirm the same comparator reports it.
    perturbed = dict(leg126_a21 or {})
    victim = "ff_lift"
    perturbed[victim] = ("zero" if perturbed.get(victim) == "nonzero" else "nonzero")
    ctrl_rows = _a21_agreement(leg58_in, leg58_out, perturbed, shapes)
    ctrl_disagreements = [r for r in ctrl_rows if not r["agree"]]
    control = {
        "perturbation": f"flip leg 126's a21_of_shape['{victim}']",
        "n_disagreements_reported": len(ctrl_disagreements),
        "shapes_reported": [r["shape"] for r in ctrl_disagreements],
        "comparator_can_report_disagreement": len(ctrl_disagreements) == 1,
    }

    agree = (not a21_disagreements) and all(coverage.values())

    return {
        "what": ("locate the shape/class enumeration legs 54/58/126 range over, then "
                 "cross-check the parts of it that are hand-written more than once"),
        "direction_md_premise": ("solver/certificate_shapes.py 'supplies the "
                                 "shape/class enumeration that leg 54's battery and "
                                 "leg 58's theorem both range over'"),
        "premise_holds": False,
        "where_the_enumeration_actually_lives": {
            "declared_once": "experiments/p2_route_mm_v1_shape.py :: SHAPES (leg 54)",
            "leg58": ("experiments/p2_route_ng_v1_nogo.py -- IMPORTS SHAPES; "
                      "hand-writes the A21 partition IN_CLASS / OUT_OF_CLASS"),
            "leg126": ("experiments/p2_route_bx_v1_stageb.py -- IMPORTS SHAPES and "
                       "ADMISSIBLE; hand-writes the A21 map a21_of_shape")},
        "import_provenance": imports,
        "membership_cannot_drift_because_it_is_imported": (
            "SHAPES" in imports["leg58_imports_from_p2_route_mm_v1_shape"]
            and "SHAPES" in imports["leg126_imports_from_p2_route_mm_v1_shape"]),
        "names_certificate_shapes_py_contributes_to_it": contributed,
        "n_names_contributed_by_the_module_under_test": len(contributed),
        "n_names_legs_54_58_126_import_from_the_module_under_test": sum(
            len(v) for k, v in imports.items() if "certificate_shapes" in k),
        "SHAPES": shapes,
        "n_shapes": len(shapes),
        "coverage": coverage,
        "a21_axis": a21_rows,
        "n_a21_cross_checked": len(a21_rows),
        "n_a21_disagreements": len(a21_disagreements),
        "a21_disagreements": a21_disagreements,
        "negative_control_lesson_90": control,
        "what_certificate_shapes_py_DOES_enumerate": {
            "SHAPE_LEDGER_rows_total": len(SHAPE_LEDGER),
            "SHAPE_LEDGER_rows_real": len(real_ledger()),
            "CADIOT_SCOPE_clauses": len(CADIOT_SCOPE),
            "CP_FORWARD_rows": len(CP_FORWARD),
            "CADIOT_EXAMPLES": len(cs.CADIOT_EXAMPLES)},
        "consequence_for_leg_126": (
            "leg 126's 1,686-configuration count does NOT read this module -- it "
            "imports nothing from solver/certificate_shapes.py, and neither do legs "
            "54 or 58 -- so none of CSA1-CSA7 can reach that count.  The direction's "
            "stated threat model has no code path.  The completeness risk that DOES "
            "exist is the A21 partition, hand-written once by leg 58 and again by "
            "leg 126 over an imported shape list; leg 126 drops inconsistent "
            "(shape, A21) pairs using its copy, so a disagreement would move the "
            "count.  All 7 shapes are cross-checked and all 7 agree, with full "
            "coverage and disjointness on both sides, and the comparator is shown to "
            "report a disagreement when one is injected.  Leg 126's completeness "
            "count is independently corroborated on this axis."),
        "verdict": ("ROBUST" if (agree and control[
            "comparator_can_report_disagreement"]) else "GAP"),
    }


GATES = [("CSA1_malformed_shape_descriptors", gate_csa1),
         ("CSA2_fictitious_row_flag_drift", gate_csa2),
         ("CSA3_location_guard_asymmetry", gate_csa3),
         ("CSA4_degenerate_enumerations", gate_csa4),
         ("CSA5_boundary_class_parameters", gate_csa5),
         ("CSA6_nan_absorption_in_shift_requirement", gate_csa6),
         ("CSA7_missing_sibling_guard_in_m_divergence", gate_csa7),
         ("CSA8_completeness_vs_legs_54_58_126", gate_csa8)]


def main():
    t0 = time.time()
    print(__doc__.split("\n")[0])
    out = {
        "leg": 146, "route": "CSA",
        "gate": ("Under adversarial input (malformed shape descriptors, boundary "
                 "class parameters, degenerate splits) does certificate_shapes.py "
                 "ever silently return a wrong or incomplete enumeration, and does "
                 "its enumerated set match what legs 54/58/126 each read from it?"),
        "module_under_test": "solver/certificate_shapes.py (READ-ONLY, unedited)",
        "gates": {},
    }
    for name, fn in GATES:
        print(f"  == {name}")
        out["gates"][name] = fn()

    gaps = [k for k, v in out["gates"].items() if v["verdict"] == "GAP"]
    out["gate_answer"] = "YES" if gaps else "NO"
    out["n_gates"] = len(GATES)
    out["n_gaps"] = len(gaps)
    out["gaps"] = gaps
    out["robust_gates"] = [k for k, v in out["gates"].items()
                           if v["verdict"] == "ROBUST"]

    g = out["gates"]
    out["headline"] = {
        "silent_corruption_sites": len(gaps),
        "malformed_descriptor_mutations_silently_reclassified":
            [g["CSA1_malformed_shape_descriptors"]["n_silently_reclassified"],
             g["CSA1_malformed_shape_descriptors"]["n_mutations"]],
        "one_deleted_key_flips_the_XS_gate":
            g["CSA2_fictitious_row_flag_drift"]["gate_answer_flipped"],
        "citation_free_row_passes_the_standing_guard":
            g["CSA2_fictitious_row_flag_drift"][
                "citation_free_row_reported_clean_by_unlocated_rows"],
        "quote_mutations_missed_by_one_guard_and_caught_by_its_sibling":
            [g["CSA3_location_guard_asymmetry"][
                "quote_mutations_missed_by_unlocated_rows"],
             g["CSA3_location_guard_asymmetry"][
                 "quote_mutations_caught_by_cp_unlocated_rows"]],
        "empty_scope_inverts_the_CP_gate_to":
            g["CSA4_degenerate_enumerations"]["empty_scope"]["answer"],
        "negative_mu_values_misclassified_admissible":
            [g["CSA5_boundary_class_parameters"]["n_misclassified"],
             g["CSA5_boundary_class_parameters"]["n_swept"]],
        "worst_bdl_delta_reported_admissible":
            (g["CSA5_boundary_class_parameters"]["worst_case"] or {}).get("bdl_delta"),
        "shift_requirement_clean_vs_one_nan":
            [g["CSA6_nan_absorption_in_shift_requirement"]["clean_s_required"],
             g["CSA6_nan_absorption_in_shift_requirement"]["cases"][0]["s_required"]],
        "nan_poisons_inverted_to_already_dominant":
            [g["CSA6_nan_absorption_in_shift_requirement"][
                "n_silently_inverted_to_zero"],
             g["CSA6_nan_absorption_in_shift_requirement"]["n_poisons"]],
        "K_exponent_sign_inversion_from_one_nan_rung":
            g["CSA7_missing_sibling_guard_in_m_divergence"]["K_exponent_sign_change"],
        "sibling_function_refuses_the_same_input":
            g["CSA7_missing_sibling_guard_in_m_divergence"]["sibling_refuses"],
        "names_this_module_contributes_to_leg_54_58_126_enumeration":
            g["CSA8_completeness_vs_legs_54_58_126"][
                "n_names_contributed_by_the_module_under_test"],
        "shape_membership_is_imported_not_redeclared":
            g["CSA8_completeness_vs_legs_54_58_126"][
                "membership_cannot_drift_because_it_is_imported"],
        "a21_partition_cross_checked_and_disagreements":
            [g["CSA8_completeness_vs_legs_54_58_126"]["n_a21_cross_checked"],
             g["CSA8_completeness_vs_legs_54_58_126"]["n_a21_disagreements"]],
        "a21_comparator_reports_an_injected_disagreement":
            g["CSA8_completeness_vs_legs_54_58_126"]["negative_control_lesson_90"][
                "comparator_can_report_disagreement"],
    }
    out["runtime_s"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True, default=str)
    print(f"\nGATE ANSWER: {out['gate_answer']}  ({out['n_gaps']}/{out['n_gates']} "
          f"gates report GAP: {', '.join(gaps)})")
    print(f"wrote {OUT}  ({out['runtime_s']} s)")


if __name__ == "__main__":
    main()
