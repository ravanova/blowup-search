"""Route-DCR, leg 151 -- the REPAIR runner for solver/decay_collocation.py.

Leg 115 (Route-DCA) measured three silent-corruption gaps in the nodal spectral core under
the collocation lane and escalated: its gate's yes-branch reports, it does not patch.  Leg
151 lands the guards.  This runner is the evidence, and it answers the gate's two clauses
separately and with magnitudes:

  (a) do all 3 of leg 115's failing cases now reject or visibly flag the degenerate/poisoned
      input, with every PIN inverted?
  (b) is the module BIT-IDENTICAL on every previously-passing case, including the
      capabilities.py validated line?

Clause (b) is the one that can only be answered by a differential, so it is run as one, on
leg 130 / Route-HPR's template (`experiments/p2_route_hpr_v1_repair.py`): the PRE-REPAIR
module is read out of git, imported into THIS SAME PROCESS under a private name, and called
side by side with the repaired module on every shipped configuration.  Comparison is `==` on
raw float64 and `sha256` on raw array bytes -- never `allclose`.

LESSON 90 (a control that cannot come out differently is not a control).  A no-op
differential that accidentally compares a module against ITSELF reports 0/0 movement and is a
tautology of the code -- exactly the trap leg 129 fell into and caught.  Two executable
controls guard against it here, and the run is VOID (SystemExit) if either fails:

  CONTROL 1 (identity):   the pre-repair module must be a genuinely DIFFERENT object with a
                          different source length and no DecayCollocationDomainError symbol.
  CONTROL 2 (must move):  the pre-repair module must REPRODUCE leg 115's banked headline
                          1.681792830507429 at J = 1 for all five drop values and all nine c
                          values, while the repaired module raises on every one of them.
                          If the "moved" count is zero, the harness is dead, not the defect.
  CONTROL 3 (wrong predicate): leg 115's own PRESCRIBED predicate ("rows is empty") is
                          evaluated on the same five drop values and must catch strictly
                          FEWER than the landed shape invariant does.  This is the arm that
                          justifies the repair's departure from the finding leg's text.

Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_dcr_v1_repair.py
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import decay_collocation as DC                              # noqa: E402
from solver.decay_collocation import (                                  # noqa: E402
    C_ANCHOR, Collocation, DecayCollocationDomainError, gauged_jacobian,
    graded_inverse_norm, grid, sup_op_norm, transforms,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dcr_v1_repair.json")

# The module's OWN creating commit -- Route-D v4 -- and its only commit before this repair.
# Deliberately NOT "the commit before mine": a leg's own hashes are rewritten by the rebase
# onto main, so a self-referential pin stops resolving the moment the branch lands.  This is
# leg 130's lesson, landed as its follow-up commit d871675.
PRE_REPAIR_REF = "a595dcb"

# Leg 115's banked headline, from writeup/data/p2_route_dca_v1_adversarial.json.
LEG115_J1_VALUE = 1.681792830507429
LEG115_DROPS = (0, 1, -1, 5, 100)
LEG115_CS = (0.0, 0.5, 1.0, 100.0, -50.0, 1e6,
             float("nan"), float("inf"), -float("inf"))

# The shipped configuration space, read from the call sites rather than invented:
#   experiments/p2_route_d_v4_graded.py  J_LADDER = [125, 250, 500, 1000, 2000]
#   experiments/p2_route_d_v6_bounds.py  J_LADDER = [125, 250, 500, 1000, 1600]
#   experiments/p2_route_d_v5_holder.py  J_LADDER = [250, 500, 1000]
#   test_decay_collocation.py            J in {8, 16, 32, 64, 128, 150, 300, 400, 600, 1200}
# The inverse-bearing arm is capped (INV_JS) because it costs O(J^3); the cheap arm covers
# the full ladder including J = 2000.
CHEAP_JS = (8, 16, 32, 64, 125, 128, 150, 250, 300, 400, 500, 600, 1000, 1200, 1600, 2000)
INV_JS = (8, 16, 32, 64, 125, 250, 500, 1000)
ALPHAS = (0.0, 0.5, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0)
GAUGES = ("origin", "a0")


def sha(a):
    """sha256 of the raw bytes of a float64 array -- bitwise, not tolerance-based."""
    return hashlib.sha256(np.ascontiguousarray(a, dtype=float).tobytes()).hexdigest()


# ---------------------------------------------------------------------------
# the pre-repair module, loaded from git into this same process
# ---------------------------------------------------------------------------


def load_pre_repair():
    """Import the module as it stood before the guards, under a private name."""
    src = subprocess.run(["git", "show", "%s:solver/decay_collocation.py" % PRE_REPAIR_REF],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    fd, path = tempfile.mkstemp(suffix="_pre_decay_collocation.py")
    with os.fdopen(fd, "w") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("_pre_decay_collocation", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, len(src.splitlines())


# ---------------------------------------------------------------------------
# CONTROL 1 -- the two modules are genuinely different objects
# ---------------------------------------------------------------------------


def control_identity(pre, pre_lines):
    post_lines = len(open(os.path.join(ROOT, "solver", "decay_collocation.py")).read()
                     .splitlines())
    out = {
        "pre_repair_ref": PRE_REPAIR_REF,
        "pre_repair_lines": pre_lines,
        "post_repair_lines": post_lines,
        "distinct_module_objects": pre is not DC,
        "pre_has_guard_symbol": hasattr(pre, "DecayCollocationDomainError"),
        "post_has_guard_symbol": hasattr(DC, "DecayCollocationDomainError"),
        "pre_raise_count": subprocess.run(
            ["git", "show", "%s:solver/decay_collocation.py" % PRE_REPAIR_REF],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.count("raise "),
    }
    out["ok"] = (out["distinct_module_objects"] and not out["pre_has_guard_symbol"]
                 and out["post_has_guard_symbol"] and out["pre_raise_count"] == 0
                 and post_lines > pre_lines)
    return out


# ---------------------------------------------------------------------------
# (a) the three findings: does the guard fire, and did the defect exist?
# ---------------------------------------------------------------------------


def clause_a_g1(pre):
    """G1: J = 1. Pre-repair reproduces leg 115's constant; post-repair raises on all."""
    rows = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            pre_col = pre.Collocation(1)
            post_col = Collocation(1)
            for drop in LEG115_DROPS:
                for gauge in GAUGES:
                    v_pre = pre.graded_inverse_norm(pre_col, 1.5, gauge=gauge, drop=drop)[0]
                    try:
                        v_post = graded_inverse_norm(post_col, 1.5, gauge=gauge, drop=drop)[0]
                        post_raised, post_val = False, v_post
                    except DecayCollocationDomainError:
                        post_raised, post_val = True, None
                    rows.append({"kind": "drop", "drop": drop, "gauge": gauge,
                                 "pre_value": v_pre,
                                 "pre_equals_leg115_headline": v_pre == LEG115_J1_VALUE,
                                 "post_raised": post_raised, "post_value": post_val})
            for c in LEG115_CS:
                v_pre = pre.graded_inverse_norm(pre_col, 1.5, c=c)[0]
                try:
                    v_post = graded_inverse_norm(post_col, 1.5, c=c)[0]
                    post_raised, post_val = False, v_post
                except DecayCollocationDomainError:
                    post_raised, post_val = True, None
                rows.append({"kind": "c", "c": repr(c), "pre_value": v_pre,
                             "pre_equals_leg115_headline": v_pre == LEG115_J1_VALUE,
                             "post_raised": post_raised, "post_value": post_val})
    n = len(rows)
    return {"n_cases": n,
            "pre_reproduces_leg115_headline": sum(r["pre_equals_leg115_headline"] for r in rows),
            "pre_n_distinct_values": len(set(r["pre_value"] for r in rows)),
            "post_n_raised": sum(r["post_raised"] for r in rows),
            "leg115_headline": LEG115_J1_VALUE,
            "rows": rows}


def _predicate_leg115_prescribed(J, drop):
    """Leg 115's journal, verbatim: raise "when `rows` is empty (i.e. J <= 1)"."""
    return len([j for j in range(J) if j != drop]) == 0


def _predicate_landed(J, drop):
    """The shape invariant that actually landed: len(rows) == J - 1 >= 1."""
    if not (isinstance(drop, int) and 0 <= drop < J):
        return True
    return not (len([j for j in range(J) if j != drop]) == J - 1 and J - 1 >= 1)


def clause_a_g1_wrong_predicate():
    """CONTROL 3: leg 115's PRESCRIBED predicate vs the landed one.

    LESSON 90 applies to this control directly: if it only ever evaluated the two predicates
    at J = 1, the landed one would be constantly True and the comparison would be a tautology
    of how it was written.  So the domain spans BOTH regimes -- the degenerate J = 1 cases
    leg 115 pinned AND ordinary shipped grids where the landed predicate must come out FALSE
    (i.e. must NOT refuse).  A control that only ever fires is not a control; the assertion
    below requires the landed predicate to be False somewhere.
    """
    rows = []
    for J, drop in ([(1, d) for d in LEG115_DROPS]
                    + [(J, d) for J in (2, 8, 64, 1000) for d in (0, 1, J // 2, J - 1)]
                    + [(J, d) for J in (8, 64) for d in (-1, 100000)]):
        rows.append({"J": J, "drop": drop,
                     "len_rows": len([j for j in range(J) if j != drop]),
                     "is_leg115_pinned_case": J == 1 and drop in LEG115_DROPS,
                     "caught_by_leg115_prescribed_predicate":
                         bool(_predicate_leg115_prescribed(J, drop)),
                     "caught_by_landed_shape_invariant": bool(_predicate_landed(J, drop))})
    pinned = [r for r in rows if r["is_leg115_pinned_case"]]
    n_pre = sum(r["caught_by_leg115_prescribed_predicate"] for r in pinned)
    n_landed = sum(r["caught_by_landed_shape_invariant"] for r in pinned)
    n_landed_false = sum(not r["caught_by_landed_shape_invariant"] for r in rows)
    return {"n_rows_total": len(rows),
            "n_leg115_pinned_cases": len(pinned),
            "n_caught_by_leg115_prescribed_predicate": n_pre,
            "n_caught_by_landed_shape_invariant": n_landed,
            "prescribed_predicate_is_strictly_weaker": n_pre < n_landed,
            "n_leg115_pins_the_prescription_would_have_missed": n_landed - n_pre,
            "landed_predicate_is_FALSE_somewhere": n_landed_false > 0,
            "n_rows_landed_predicate_does_not_refuse": n_landed_false,
            "rows": rows}


def clause_a_g2(pre):
    """G2: the 1-D shape ambiguity. Pre-repair returns 12.0; post-repair raises."""
    A_flat = np.array([10.0, 1.0, 1.0])
    w_dom, w_cod = np.array([1.0, 1.0, 1.0]), np.array([1.0])
    v_pre = pre.sup_op_norm(A_flat, w_dom, w_cod)
    v_pre_col = pre.sup_op_norm(A_flat.reshape(3, 1), w_dom, w_cod)
    try:
        v_post = sup_op_norm(A_flat, w_dom, w_cod)
        post_raised = False
    except DecayCollocationDomainError:
        v_post, post_raised = None, True
    v_post_col = sup_op_norm(A_flat.reshape(3, 1), w_dom, w_cod)
    rng = np.random.default_rng(20260806)
    n_cases, n_pre_mismatch, n_post_raised = 30, 0, 0
    for _ in range(n_cases):
        n = int(rng.integers(2, 7))
        a = rng.uniform(0.1, 20.0, size=n)
        wd, wc = np.ones(n), np.ones(1)
        if pre.sup_op_norm(a, wd, wc) != pre.sup_op_norm(a.reshape(n, 1), wd, wc):
            n_pre_mismatch += 1
        try:
            sup_op_norm(a, wd, wc)
        except DecayCollocationDomainError:
            n_post_raised += 1
    return {"worked_case_pre_flat": v_pre, "worked_case_pre_column": v_pre_col,
            "worked_case_post_raised": post_raised,
            "worked_case_post_column": v_post_col,
            "column_reading_unchanged_by_repair": v_pre_col == v_post_col,
            "battery_n_cases": n_cases,
            "battery_pre_n_mismatch": n_pre_mismatch,
            "battery_post_n_raised": n_post_raised}


def clause_a_g3(pre):
    """G3: a non-real alpha. Pre-repair silently diverges; post-repair raises."""
    pre_col, post_col = pre.Collocation(16), Collocation(16)
    om = post_col.anchor()
    alphas = [1.5 + 0.1j, 1.5 + 1.0j, 0.0 + 1.0j, -1.0 + 2.0j, 1.0 + 0.0j, 1.5 + 1e-10j]
    n_pre_diverged = n_post_raised = 0
    rows = []
    for a in alphas:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            v_pre = pre_col.norm_domain(om, a)
        v_pre_real = pre_col.norm_domain(om, a.real)
        diverged = (v_pre != v_pre_real)
        n_pre_diverged += int(diverged)
        try:
            post_col.norm_domain(om, a)
            raised = False
        except DecayCollocationDomainError:
            raised = True
        n_post_raised += int(raised)
        rows.append({"alpha": repr(a), "pre_value": v_pre, "pre_real_part_value": v_pre_real,
                     "pre_silently_diverged": diverged, "post_raised": raised})
    # the end-to-end path leg 115 flagged
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        e2e_pre = pre.graded_inverse_norm(pre.Collocation(16), 1.5 + 0.3j)[0]
    try:
        graded_inverse_norm(post_col, 1.5 + 0.3j)
        e2e_post_raised = False
    except DecayCollocationDomainError:
        e2e_post_raised = True
    return {"n_cases": len(alphas), "pre_n_silently_diverging": n_pre_diverged,
            "post_n_raised": n_post_raised,
            "end_to_end_pre_value": e2e_pre, "end_to_end_post_raised": e2e_post_raised,
            "rows": rows}


# ---------------------------------------------------------------------------
# (b) zero movement: the bitwise differential over every shipped configuration
# ---------------------------------------------------------------------------


def bitwise_differential(pre):
    """Every shipped configuration, pre vs post, compared bitwise.

    Two arms.  The CHEAP arm covers the full J ladder including J = 2000 over every grid,
    transform, operator and weight quantity.  The INVERSE arm is capped at J = 1000 because
    `graded_inverse_norm` costs O(J^3), and covers the gauge/drop/alpha product on top.
    """
    n = n_ident = 0
    movers = []

    def cmp(tag, a, b):
        nonlocal n, n_ident
        n += 1
        ha, hb = sha(a), sha(b)
        if ha == hb:
            n_ident += 1
        else:
            movers.append({"quantity": tag, "pre_sha256": ha, "post_sha256": hb})

    # --- cheap arm: grid, transforms, operators, weights, norms ---------
    for J in CHEAP_JS:
        th_pre, X_pre = pre.grid(J)
        th_post, X_post = grid(J)
        cmp("grid.theta[J=%d]" % J, th_pre, th_post)
        cmp("grid.X[J=%d]" % J, X_pre, X_post)
        tc_pre, ce_pre, se_pre = pre.transforms(J)
        tc_post, ce_post, se_post = transforms(J)
        cmp("transforms.to_coef[J=%d]" % J, tc_pre, tc_post)
        cmp("transforms.cos_eval[J=%d]" % J, ce_pre, ce_post)
        cmp("transforms.sin_eval[J=%d]" % J, se_pre, se_post)
        cpre, cpost = pre.Collocation(J), Collocation(J)
        cmp("Collocation.H[J=%d]" % J, cpre.H, cpost.H)
        cmp("Collocation.D[J=%d]" % J, cpre.D, cpost.D)
        cmp("Collocation.transport[J=%d]" % J, cpre.transport, cpost.transport)
        om_pre, om_post = cpre.anchor(), cpost.anchor()
        cmp("anchor[J=%d]" % J, om_pre, om_post)
        for c in (0.0, C_ANCHOR, 1.0, -0.25):
            cmp("residual[J=%d,c=%s]" % (J, c), cpre.residual(om_pre, c),
                cpost.residual(om_post, c))
            cmp("dc_column[J=%d,c=%s]" % (J, c), cpre.dc_column(om_pre),
                cpost.dc_column(om_post))
        cmp("jacobian_matrix[J=%d]" % J, cpre.jacobian_matrix(om_pre, C_ANCHOR),
            cpost.jacobian_matrix(om_post, C_ANCHOR))
        cmp("quadratic[J=%d]" % J, cpre.quadratic(om_pre), cpost.quadratic(om_post))
        for alpha in ALPHAS:
            cmp("w_domain[J=%d,a=%s]" % (J, alpha), cpre.w_domain(alpha),
                cpost.w_domain(alpha))
            cmp("w_codomain[J=%d,a=%s]" % (J, alpha), cpre.w_codomain(alpha),
                cpost.w_codomain(alpha))
            cmp("norm_domain[J=%d,a=%s]" % (J, alpha),
                np.array([cpre.norm_domain(om_pre, alpha)]),
                np.array([cpost.norm_domain(om_post, alpha)]))
            cmp("norm_codomain[J=%d,a=%s]" % (J, alpha),
                np.array([cpre.norm_codomain(om_pre, alpha)]),
                np.array([cpost.norm_codomain(om_post, alpha)]))
        # the capabilities.py validated line: manufactured solutions on the graded grid.
        # ||f_alpha||_X == 1 exactly, the identity test_decay_collocation.py gate 6 asserts.
        for alpha in (1.2, 1.5, 1.8):
            f_pre = (1.0 + cpre.X ** 2) ** (-0.5 * alpha)
            f_post = (1.0 + cpost.X ** 2) ** (-0.5 * alpha)
            cmp("manufactured_solution[J=%d,a=%s]" % (J, alpha), f_pre, f_post)
            cmp("manufactured_norm[J=%d,a=%s]" % (J, alpha),
                np.array([cpre.norm_domain(f_pre, alpha)]),
                np.array([cpost.norm_domain(f_post, alpha)]))

    # --- inverse arm: the gauged system and the graded inverse norm -----
    for J in INV_JS:
        cpre, cpost = pre.Collocation(J), Collocation(J)
        om_pre, om_post = cpre.anchor(), cpost.anchor()
        for gauge in GAUGES:
            for drop in (0, 1, 2, J // 4, J // 2, J - 1):     # the shipped drop sweep, v4 w5
                M_pre, r_pre = pre.gauged_jacobian(cpre, om_pre, C_ANCHOR,
                                                   gauge=gauge, drop=drop)
                M_post, r_post = gauged_jacobian(cpost, om_post, C_ANCHOR,
                                                 gauge=gauge, drop=drop)
                cmp("gauged_jacobian.M[J=%d,%s,drop=%d]" % (J, gauge, drop), M_pre, M_post)
                cmp("gauged_jacobian.rows[J=%d,%s,drop=%d]" % (J, gauge, drop),
                    np.array(r_pre, dtype=float), np.array(r_post, dtype=float))
            for alpha in ALPHAS:
                v_pre, A_pre, Mi_pre = pre.graded_inverse_norm(cpre, alpha, gauge=gauge)
                v_post, A_post, Mi_post = graded_inverse_norm(cpost, alpha, gauge=gauge)
                cmp("graded_inverse_norm.value[J=%d,%s,a=%s]" % (J, gauge, alpha),
                    np.array([v_pre]), np.array([v_post]))
                cmp("graded_inverse_norm.A[J=%d,%s,a=%s]" % (J, gauge, alpha), A_pre, A_post)
                cmp("graded_inverse_norm.M[J=%d,%s,a=%s]" % (J, gauge, alpha),
                    Mi_pre, Mi_post)
        # sup_op_norm itself, on the only shape any in-repo caller ever passes
        A = np.linalg.inv(gauged_jacobian(cpost, om_post, C_ANCHOR)[0])
        for alpha in ALPHAS:
            wd, wc = cpost.w_domain(alpha), cpost.w_codomain(alpha)
            cmp("sup_op_norm[J=%d,a=%s]" % (J, alpha),
                np.array([pre.sup_op_norm(A, wd, wc)]),
                np.array([sup_op_norm(A, wd, wc)]))

    return {"n_quantities": n, "n_bit_identical": n_ident,
            "n_moved": n - n_ident, "movers": movers,
            "cheap_J_ladder": list(CHEAP_JS), "inverse_J_ladder": list(INV_JS),
            "alphas": list(ALPHAS), "gauges": list(GAUGES)}


def subclass_arm(pre):
    """The ACollocation subclass (solver/collocation_newton.py) inherits from Collocation.

    That file is OUTSIDE this leg's territory and is not edited, but the coupling is real, so
    it is MEASURED rather than reasoned about: every in-repo ACollocation call site passes
    J >= 8 in range, so the guards must fire on none of them and every value must be
    bit-identical.  The subclass is imported from the CURRENT tree in both arms -- only its
    inherited base differs -- so this arm isolates exactly the inheritance path.
    """
    from solver.collocation_newton import ACollocation                  # noqa: E402
    n = n_ident = 0
    movers = []
    n_guard_fired = 0

    def cmp(tag, a, b):
        nonlocal n, n_ident
        n += 1
        if sha(a) == sha(b):
            n_ident += 1
        else:
            movers.append({"quantity": tag, "pre_sha256": sha(a), "post_sha256": sha(b)})

    for J in (8, 16, 120, 200, 240):
        base_pre = pre.Collocation(J)
        for a in (0.0, 0.15, 0.35, 0.5):
            try:
                col = ACollocation(J, a=a)
            except DecayCollocationDomainError:
                n_guard_fired += 1
                continue
            om = col.anchor()
            # every quantity ACollocation INHERITS from Collocation, against the pre-repair
            # base -- this is exactly the inheritance path and nothing else
            cmp("ACollocation.X[J=%d,a=%s]" % (J, a), base_pre.X, col.X)
            cmp("ACollocation.H[J=%d,a=%s]" % (J, a), base_pre.H, col.H)
            cmp("ACollocation.transport[J=%d,a=%s]" % (J, a), base_pre.transport,
                col.transport)
            cmp("ACollocation.anchor[J=%d,a=%s]" % (J, a), base_pre.anchor(), om)
            for alpha in (1.0, 1.5, 2.0):
                cmp("ACollocation.w_domain[J=%d,a=%s,al=%s]" % (J, a, alpha),
                    base_pre.w_domain(alpha), col.w_domain(alpha))
                cmp("ACollocation.norm_domain[J=%d,a=%s,al=%s]" % (J, a, alpha),
                    np.array([base_pre.norm_domain(base_pre.anchor(), alpha)]),
                    np.array([col.norm_domain(om, alpha)]))
            # and the subclass's OWN residual, which must stay finite and unaffected
            cmp("ACollocation.residual_inherited_part[J=%d,a=%s]" % (J, a),
                base_pre.residual(base_pre.anchor(), C_ANCHOR),
                col.residual(om, C_ANCHOR))
    return {"n_quantities": n, "n_bit_identical": n_ident, "n_moved": n - n_ident,
            "n_guard_fired_on_ACollocation_call_sites": n_guard_fired,
            "movers": movers,
            "note": "ACollocation call sites all pass J >= 8 in range; guards fire on 0. "
                    "solver/collocation_newton.py is NOT edited by this leg."}


def guard_firing_census():
    """How many SHIPPED configurations does each guard refuse? Must be zero on all three."""
    fired = {"J_clause": 0, "drop_clause": 0, "alpha_clause": 0, "shape_clause": 0}
    checked = 0
    for J in CHEAP_JS:
        col = Collocation(J)
        for drop in (0, 1, 2, J // 4, J // 2, J - 1):
            for gauge in GAUGES:
                checked += 1
                try:
                    gauged_jacobian(col, col.anchor(), C_ANCHOR, gauge=gauge, drop=drop)
                except DecayCollocationDomainError as e:
                    fired["J_clause" if "J >= 2" in str(e) else "drop_clause"] += 1
        for alpha in ALPHAS:
            checked += 1
            try:
                col.w_domain(alpha), col.w_codomain(alpha)
            except DecayCollocationDomainError:
                fired["alpha_clause"] += 1
    return {"n_shipped_configurations_checked": checked, "n_refused": fired,
            "total_refused": sum(fired.values())}


# ---------------------------------------------------------------------------


def main():
    pre, pre_lines = load_pre_repair()

    c1 = control_identity(pre, pre_lines)
    if not c1["ok"]:
        raise SystemExit("CONTROL 1 FAILED (identity): %r -- the differential would be a "
                         "tautology of the code (lesson 90). Run VOID." % (c1,))

    g1 = clause_a_g1(pre)
    if g1["pre_reproduces_leg115_headline"] != g1["n_cases"] or g1["pre_n_distinct_values"] != 1:
        raise SystemExit("CONTROL 2 FAILED (must move): the pre-repair module did not "
                         "reproduce leg 115's banked collapse (%d/%d at %d distinct values). "
                         "The harness is dead, not the defect. Run VOID."
                         % (g1["pre_reproduces_leg115_headline"], g1["n_cases"],
                            g1["pre_n_distinct_values"]))
    if g1["post_n_raised"] != g1["n_cases"]:
        raise SystemExit("CLAUSE (a) FAILED on G1: %d of %d cases still return a value."
                         % (g1["n_cases"] - g1["post_n_raised"], g1["n_cases"]))

    wp = clause_a_g1_wrong_predicate()
    if not wp["prescribed_predicate_is_strictly_weaker"]:
        raise SystemExit("CONTROL 3 FAILED: leg 115's prescribed predicate was expected to "
                         "be strictly weaker than the landed one; measured %r. Run VOID." % (wp,))
    if not wp["landed_predicate_is_FALSE_somewhere"]:
        raise SystemExit("CONTROL 3 FAILED (lesson 90): the landed predicate refused EVERY "
                         "row it was evaluated on, so this comparison could not have come "
                         "out differently. Run VOID.")

    g2, g3 = clause_a_g2(pre), clause_a_g3(pre)
    diff = bitwise_differential(pre)
    sub = subclass_arm(pre)
    census = guard_firing_census()

    clause_a = (g1["post_n_raised"] == g1["n_cases"]
                and g2["worked_case_post_raised"]
                and g2["battery_post_n_raised"] == g2["battery_n_cases"]
                and g3["post_n_raised"] == g3["n_cases"]
                and g3["end_to_end_post_raised"])
    clause_b = (diff["n_moved"] == 0 and sub["n_moved"] == 0
                and census["total_refused"] == 0)

    out = {
        "leg": 151, "route": "ROUTE-DCR",
        "module": "solver/decay_collocation.py",
        "repairs_finding_of_leg": 115,
        "pre_repair_ref": PRE_REPAIR_REF,
        "control_1_identity": c1,
        "control_3_prescribed_vs_landed_predicate": wp,
        "clause_a_g1_grid_collapse": g1,
        "clause_a_g2_shape_ambiguity": g2,
        "clause_a_g3_nonreal_alpha": g3,
        "clause_b_bitwise_differential": diff,
        "clause_b_subclass_arm": sub,
        "clause_b_guard_firing_census": census,
        "GATE_clause_a_all_three_findings_now_refused": bool(clause_a),
        "GATE_clause_b_bit_identical_on_every_clean_case": bool(clause_b),
        "GATE": "YES" if (clause_a and clause_b) else "NO",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print("CONTROL 1 identity        : pre %d lines (%d raises) vs post %d lines, distinct=%s"
          % (c1["pre_repair_lines"], c1["pre_raise_count"], c1["post_repair_lines"],
             c1["distinct_module_objects"]))
    print("CONTROL 2 must-move       : pre-repair reproduces leg 115's %r on %d/%d cases at "
          "%d distinct value(s); post-repair raises on %d/%d"
          % (LEG115_J1_VALUE, g1["pre_reproduces_leg115_headline"], g1["n_cases"],
             g1["pre_n_distinct_values"], g1["post_n_raised"], g1["n_cases"]))
    print("CONTROL 3 wrong-predicate : leg 115's prescribed 'rows is empty' catches %d/%d of "
          "its own pinned drop cases; the landed shape invariant catches %d/%d (%d would "
          "have been missed). Landed predicate does NOT refuse on %d of %d rows overall, so "
          "the comparison could come out differently."
          % (wp["n_caught_by_leg115_prescribed_predicate"], wp["n_leg115_pinned_cases"],
             wp["n_caught_by_landed_shape_invariant"], wp["n_leg115_pinned_cases"],
             wp["n_leg115_pins_the_prescription_would_have_missed"],
             wp["n_rows_landed_predicate_does_not_refuse"], wp["n_rows_total"]))
    print("(a) G1 grid collapse      : %d/%d refused" % (g1["post_n_raised"], g1["n_cases"]))
    print("(a) G2 shape ambiguity    : worked case %r -> refused; battery %d/%d refused "
          "(pre: %d/%d mismatched); column reading unchanged at %r"
          % (g2["worked_case_pre_flat"], g2["battery_post_n_raised"], g2["battery_n_cases"],
             g2["battery_pre_n_mismatch"], g2["battery_n_cases"], g2["worked_case_post_column"]))
    print("(a) G3 non-real alpha     : %d/%d refused (pre: %d/%d silently diverged); "
          "end-to-end pre %r -> refused=%s"
          % (g3["post_n_raised"], g3["n_cases"], g3["pre_n_silently_diverging"], g3["n_cases"],
             g3["end_to_end_pre_value"], g3["end_to_end_post_raised"]))
    print("(b) bitwise differential  : %d/%d quantities BIT-IDENTICAL, %d moved"
          % (diff["n_bit_identical"], diff["n_quantities"], diff["n_moved"]))
    print("(b) ACollocation subclass : %d/%d bit-identical, %d moved"
          % (sub["n_bit_identical"], sub["n_quantities"], sub["n_moved"]))
    print("(b) guard firing census   : %d shipped configurations checked, %d refused %r"
          % (census["n_shipped_configurations_checked"], census["total_refused"],
             census["n_refused"]))
    print("\nGATE clause (a) %s ; clause (b) %s  ->  %s"
          % (clause_a, clause_b, out["GATE"]))
    print("written: %s" % OUT)


if __name__ == "__main__":
    main()
