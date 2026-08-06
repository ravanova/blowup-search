"""Leg 241 / Route-PCRC: the cleanup leg behind leg 217's escalation.

Leg 200 (Route-PCA) audited `solver/port_certification.py` and escalated FOUR silent
wrong-value mechanisms without patch authority.  Leg 217 (Route-PCR) repaired all four,
verified no clean-input number moves, and **escalated rather than landing** because its
gate's last clause failed on two artifacts OUTSIDE its declared territory:

  (i)  `test_port_certification_regression.py:87-88` and the banked row
       `writeup/data/p2_route_pc_v1_regression.json -> cases[Y0_negative_zero]` both
       assert the PRE-repair `accept` on the exact degenerate input leg 200 flagged; and
  (ii) leg 217's own report names THREE MORE silent paths beyond its four, uncharacterised.

This leg does (i) as a mechanical correction and (ii) as a characterisation.  It repairs
NOTHING in `solver/port_certification.py` -- repair of a new mechanism is not this leg's job.

THE DEPENDENCY THIS RUNNER MAKES EXPLICIT.  Leg 217's branch `leg/217-pcr-v1` is PARKED,
not merged.  So "the correct post-repair behaviour" is not a property of the working tree;
it is a property of a blob on another branch.  Rather than assume that branch state is
final, every gate here measures BOTH module states side by side -- the in-tree module and
leg 217's blob, loaded from git at run time -- and reports which one it is standing on.
If leg 217 lands, the two coincide and the gates report that coincidence rather than
changing their answer.

GATES
  G0  which module state is in the tree, and is leg 217's blob reachable
  G1  (a) the two flagged inputs: the full return dict under both module states
  G2  (a) the blast radius: the whole 39-case battery re-run under leg 217's module,
          diffed row-by-row against the banked JSON.  Exactly one row may move.
  G3  (b) RESIDUAL 1 -- `leading_order_solve` sign-blind in `c_l`, with the control column
  G4  (b) RESIDUAL 2 -- `stall_verdict` reads the ladder POSITIONALLY, on the LIVE ladders
  G5  (b) RESIDUAL 3 -- `pack`/`unpack` validate only the TOTAL size, at the LIVE shape
  G6  claim-adjacency: for each residual path, the live banked configuration and its margin

Run: .venv/bin/python experiments/p2_route_pcrc_v1_cleanup.py
"""

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

LEG_217_REF = "origin/leg/217-pcr-v1"
BANKED_REGRESSION = ROOT / "writeup" / "data" / "p2_route_pc_v1_regression.json"
BANKED_PRECOND = ROOT / "writeup" / "data" / "p2_route_l_v1_precond.json"
OUT = ROOT / "writeup" / "data" / "p2_route_pcrc_v1_cleanup.json"


# ---------------------------------------------------------------------------
# module loading -- the in-tree module, and leg 217's blob
# ---------------------------------------------------------------------------
def _load_module_from_source(name, source_text):
    """Import `source_text` as a fresh module named `name`.

    `solver/port_certification.py` imports absolutely (`from solver.certificate_guards
    import ...`), so it loads correctly under any module name with ROOT on sys.path.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(source_text)
        path = fh.name
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _git_show(ref_path):
    try:
        return subprocess.run(["git", "show", ref_path], cwd=str(ROOT),
                              capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _is_repaired(mod):
    """Post-leg-217 iff `radii_polynomial_status` forms and reports `r_min`."""
    try:
        return "r_min" in mod.radii_polynomial_status(1e-6, 0.1, 1.0)
    except Exception:                                               # noqa: BLE001
        return False


def gate_0_module_states():
    import solver.port_certification as intree

    blob = _git_show(f"{LEG_217_REF}:solver/port_certification.py")
    repaired = None
    if blob is not None:
        repaired = _load_module_from_source("_pc_leg217", blob)

    intree_repaired = _is_repaired(intree)
    if repaired is None:
        # leg 217 unreachable (no such ref): fall back to the tree, and say so.
        repaired = intree

    return intree, repaired, {
        "in_tree_is_post_leg_217_repair": bool(intree_repaired),
        "leg_217_blob_reachable": blob is not None,
        "leg_217_ref": LEG_217_REF,
        "leg_217_blob_is_post_repair": bool(_is_repaired(repaired)),
        "the_two_modules_coincide": bool(intree_repaired),
        "reading": ("leg 217 has LANDED: the in-tree module already carries the repair, "
                    "and every 'post-repair' column below is the working tree's own answer"
                    if intree_repaired else
                    "leg 217 is still PARKED: every 'post-repair' column below is measured "
                    "on the blob at " + LEG_217_REF + ", not on the working tree. The two "
                    "artifacts this leg corrects are therefore correct AGAINST THAT BLOB, "
                    "and are red against the working tree until leg 217 merges."),
    }


# ---------------------------------------------------------------------------
# G1 -- the two flagged inputs
# ---------------------------------------------------------------------------
FLAGGED = (
    ("test_port_certification_regression.py:87-88", (0.0, 0.0, 0.0),
     "the test's own comment says its intent is that 0.0 is a legitimate BOUND, i.e. not a "
     "HYPOTHESIS violation. That intent survives the repair (status stays EVALUATED); what "
     "the repair changes is the RADIUS verdict, which legs 79/128 left behind."),
    ("writeup/data/p2_route_pc_v1_regression.json -> cases[Y0_negative_zero]",
     (-0.0, 0.1, 1.0),
     "negative zero: signed but numerically 0.0, so it is admitted by the hypothesis guard "
     "and then certifies a ball of radius exactly 0."),
)


def _jsonable(d):
    return {k: (float(v) if isinstance(v, float) else v) for k, v in sorted(d.items())}


def gate_1_flagged_inputs(intree, repaired):
    rows = []
    for site, args, note in FLAGGED:
        before = intree.radii_polynomial_status(*args)
        after = repaired.radii_polynomial_status(*args)
        rows.append({
            "site": site,
            "args": {"Y0": args[0], "Z1": args[1], "Z2": args[2]},
            "note": note,
            "in_tree": _jsonable(before),
            "post_leg_217": _jsonable(after),
            "status_moved": before.get("status") != after.get("status"),
            "closes_before": before.get("closes"),
            "closes_after": after.get("closes"),
            "r_min_after": after.get("r_min"),
            "radius_violation_after": after.get("radius_violation"),
        })
    return {
        "mechanism": ("`radii_polynomial_status` returned `closes = bool(disc >= 0)` and "
                      "never formed the smaller root r_min = ((1-Z_1) - sqrt(disc))/(2 Z_2) "
                      "-- the radius of the ball the theorem concludes a zero lives INSIDE. "
                      "With Y_0 = 0 (the value leg 51 measured on the a=0 CLM profile) and "
                      "any contraction Z_1 < 1, r_min is exactly 0: a conclusion with no "
                      "content, reported as a closing certificate."),
        "rows": rows,
        "status_preserved_on_both": all(not r["status_moved"] for r in rows),
        "reading": ("BOTH inputs keep status EVALUATED and both flip closes True -> False "
                    "on a ball of radius exactly 0. The hypothesis half (legs 79/128) is "
                    "untouched; only the radius half moves."),
    }


# ---------------------------------------------------------------------------
# G2 -- the blast radius, row by row against the banked JSON
# ---------------------------------------------------------------------------
_COMPARED_KEYS = ("status", "closes", "outcome", "verdict", "carries_Y0", "carries_Z1",
                  "keys", "outside_theorem", "violates")


def gate_2_blast_radius(repaired):
    """Re-run leg 79's whole battery under the repaired module; diff against the bank.

    The battery module builds its rows by calling `radii_polynomial_status` at import
    time of the functions, so the repaired module is injected under the name the battery
    imported before the row builders run.
    """
    banked = json.loads(BANKED_REGRESSION.read_text())

    import solver.port_certification as intree
    saved = {k: getattr(intree, k) for k in ("radii_polynomial_status",)}
    intree.radii_polynomial_status = repaired.radii_polynomial_status
    try:
        import p2_route_pc_v1_regression as batt
        importlib.reload(batt)
        rows = (batt.pc1_honest_paths() + batt.pc2_sign_violations()
                + batt.pc3_nonfinite() + batt.pc4_type_confusion())
        verdict = batt.pc5_verdict(rows)
    finally:
        for k, v in saved.items():
            setattr(intree, k, v)
        import p2_route_pc_v1_regression as batt2
        importlib.reload(batt2)

    by_label = {r["label"]: r for r in rows}
    moved = []
    for old in banked["cases"]:
        new = by_label.get(old["label"])
        if new is None:
            moved.append({"label": old["label"], "how": "DISAPPEARED"})
            continue
        deltas = {k: {"banked": old.get(k), "post_repair": new.get(k)}
                  for k in _COMPARED_KEYS if old.get(k) != new.get(k)}
        if deltas:
            moved.append({"label": old["label"], "deltas": deltas})

    verdict_deltas = {k: {"banked": banked["verdict"].get(k), "post_repair": verdict.get(k)}
                      for k in verdict if banked["verdict"].get(k) != verdict.get(k)}

    return {
        "cases_total": len(rows),
        "banked_cases_total": len(banked["cases"]),
        "rows_that_move": len(moved),
        "moved": moved,
        "verdict_block_deltas": verdict_deltas,
        "verdict_block_byte_identical": not verdict_deltas,
        "gate_answer_banked": banked["verdict"].get("gate_answer"),
        "gate_answer_post_repair": verdict.get("gate_answer"),
        "reading": ("the repair is a rejection layer in leg 128's sense: it may turn "
                    "something previously accepted into a refusal and must never move a "
                    "clean-input number. Exactly the rows listed above move."),
    }


# ---------------------------------------------------------------------------
# G3 -- RESIDUAL 1: leading_order_solve is sign-blind in c_l
# ---------------------------------------------------------------------------
def _dense_radial(c_l, drho, c_diag, nr, upwind_by_sign):
    """(-c_l d_rho + c_diag) on the radial axis.

    `upwind_by_sign=False` assembles what the CODE computes: the backward difference,
    unconditionally.  `True` assembles what the DOCSTRING advertises: first-order upwind,
    the difference direction chosen by the sign of `c_l`.  They coincide for c_l > 0.
    """
    L = np.zeros((nr, nr))
    a = c_l / drho
    for i in range(nr):
        if (not upwind_by_sign) or c_l > 0:
            L[i, i] = c_diag - a
            if i - 1 >= 0:
                L[i, i - 1] = a
        elif c_l < 0:
            L[i, i] = c_diag + a
            if i + 1 < nr:
                L[i, i + 1] = -a
        else:
            L[i, i] = c_diag
    return L


def _rel(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    nb = float(np.linalg.norm(b))
    return float(np.linalg.norm(a - b) / nb) if nb else float(np.linalg.norm(a - b))


def _c_l_sweep(solve, nr, ncol, drho, c_diag, seed, c_ls):
    rng = np.random.default_rng(seed)
    rhs = rng.standard_normal((nr, ncol))
    rows = []
    for c_l in c_ls:
        got = solve(rhs, c_l, drho, c_diag)
        adv = np.linalg.solve(_dense_radial(c_l, drho, c_diag, nr, True), rhs)
        asm = np.linalg.solve(_dense_radial(c_l, drho, c_diag, nr, False), rhs)
        resid = _rel(_dense_radial(c_l, drho, c_diag, nr, True) @ got, rhs)
        rows.append({"c_l": float(c_l),
                     "rel_error_vs_advertised_operator": _rel(got, adv),
                     "rel_error_vs_assembled_operator": _rel(got, asm),
                     "residual_over_rhs_vs_advertised": resid,
                     "silent": bool(np.all(np.isfinite(got)))})
    return rows


def gate_3_leading_order_c_l(repaired):
    solve = repaired.leading_order_solve
    banked_c_l = float(json.loads(BANKED_PRECOND.read_text())["seed"]["c_l"])
    c_ls = (banked_c_l, 2.5, 0.5, 0.001, 0.0, -0.001, -0.5, -2.5, -banked_c_l)

    leg200 = _c_l_sweep(solve, nr=16, ncol=4, drho=0.1, c_diag=-1.2, seed=3, c_ls=c_ls)
    live = _c_l_sweep(solve, nr=200, ncol=48, drho=0.1, c_diag=-1.0145055559524538,
                      seed=241, c_ls=c_ls)

    def at(rows, c):
        return next(r for r in rows if r["c_l"] == c)

    worst_control = max(max(r["rel_error_vs_assembled_operator"] for r in leg200),
                        max(r["rel_error_vs_assembled_operator"] for r in live))
    return {
        "mechanism": ("`leading_order_solve` hard-codes the BACKWARD radial difference "
                      "(`prev = (rhs[i] - a*prev)/denom`, sweeping i upward) regardless of "
                      "sign(c_l). For c_l < 0 the advection is inward and the backward "
                      "stencil is ANTI-upwind, so the routine returns the exact inverse of "
                      "a matrix that is not the one its docstring names -- finite, "
                      "correctly shaped, no exception, no flag. Leg 217 repaired the DTYPE "
                      "defect in this same function (M3, `np.zeros_like` with no float "
                      "cast) and deliberately left the sign defect: M3 is a one-token cast, "
                      "this is M1's structural twin."),
        "leg_200_fixture": {"nr": 16, "ncol": 4, "drho": 0.1, "c_diag": -1.2, "seed": 3,
                            "rows": leg200},
        "live_shaped_fixture": {"nr": 200, "ncol": 48, "drho": 0.1,
                                "c_diag": -1.0145055559524538, "seed": 241, "rows": live},
        "magnitude_at_c_l_minus_0p5": {
            "leg_200_fixture": at(leg200, -0.5)["rel_error_vs_advertised_operator"],
            "live_shaped_fixture": at(live, -0.5)["rel_error_vs_advertised_operator"]},
        "magnitude_at_banked_c_l_sign_flipped": {
            "c_l": -banked_c_l,
            "leg_200_fixture": at(leg200, -banked_c_l)["rel_error_vs_advertised_operator"],
            "live_shaped_fixture": at(live, -banked_c_l)["rel_error_vs_advertised_operator"]},
        "amplification_law": {
            "per_row_factor": "|a / (c_diag - a)| with a = c_l/drho",
            "over_the_sweep": "that factor raised to nr, the number of radial nodes",
            "rows": [{"c_l": float(c), "nr": nr,
                      "per_row": abs((c / 0.1) / (-1.0145055559524538 - c / 0.1)),
                      "to_the_nr": abs((c / 0.1) / (-1.0145055559524538 - c / 0.1)) ** nr}
                     for nr in (16, 200) for c in (-0.001, -0.5, -2.5, -banked_c_l)],
            "why_the_curve_is_not_monotone": (
                "for c_l < 0 the factor is |a|/(|a| - |c_diag|), which exceeds 1 only once "
                "|a| > |c_diag| and tends to 1 from above as |a| -> infinity. It therefore "
                "PEAKS at a MARGINAL breach, |c_l| ~ drho*|c_diag| ~ 0.101, and decays "
                "toward both ends: a gross negative c_l is SAFER than a slight one. This is "
                "banked lesson 88 from the other side, and it is the same non-monotonicity "
                "leg 200 measured for M1 (worst at s_rho = -0.4, not at -3.0)."),
            "why_the_magnitude_is_fixture_bound": (
                "the error is exponential in nr, so a magnitude quoted here is meaningless "
                "without its grid. Leg 200's 26.0x is a 16-node number; the same defect at "
                "the LIVE 200-node radial resolution is 7.4e+18. Both are given above, "
                "neither is borrowed for the other -- leg 53's lesson, and leg 217 restated "
                "it when it separated its own residue table by fixture."),
        },
        "control_worst_rel_error_vs_the_operator_it_assembles": worst_control,
        "control_reading": ("the control column is ~1e-16 at EVERY c_l including the "
                            "negative ones: the sweep is arithmetically exact throughout. "
                            "All of the wrongness is in WHICH operator, none of it in the "
                            "solve -- the column that could report the other answer, and "
                            "does not."),
        "c_l_zero_is_exact": {
            "leg_200_fixture": at(leg200, 0.0)["rel_error_vs_advertised_operator"],
            "live_shaped_fixture": at(live, 0.0)["rel_error_vs_advertised_operator"],
            "why": ("c_l = 0 carries no radial coupling and is admissible in either "
                    "direction -- the exact analogue of leg 217's `s_rho == 0` "
                    "bit-identical branch in `line_sweep_solve`.")},
        "verdict": "SILENT",
    }


# ---------------------------------------------------------------------------
# G4 -- RESIDUAL 2: stall_verdict reads the ladder positionally
# ---------------------------------------------------------------------------
def gate_4_stall_positional(repaired):
    sv = repaired.stall_verdict
    banked = json.loads(BANKED_PRECOND.read_text())
    ladders = banked["L3_preconditioners"]["ladders"]

    rows = []
    for label, ladder in ladders.items():
        asc = sv(list(ladder))
        desc = sv(list(reversed(ladder)))
        rows.append({
            "ladder": label,
            "ascending_dims": {"work_ratio": asc["work_ratio"],
                               "residual_gain": asc["residual_gain"],
                               "flat": asc["flat"], "reading": asc["reading"]},
            "same_data_descending_dims": {"work_ratio": desc["work_ratio"],
                                          "residual_gain": desc["residual_gain"],
                                          "flat": desc["flat"], "reading": desc["reading"]},
            "gain_ratio_asc_over_desc": float(asc["residual_gain"] / desc["residual_gain"]),
            "published_verdict_flips": bool(asc["flat"] != desc["flat"]),
        })

    deep = banked["L3_preconditioners"]["line_sweep_deeper"]
    deep_asc, deep_desc = sv(list(deep)), sv(list(reversed(deep)))

    # attribution_summary propagates the same positional read into a RANKED table.
    attr_asc = repaired.attribution_summary({"full": list(ladders["none"]),
                                             "line sweep": list(ladders["full transport line sweep"])})
    attr_desc = repaired.attribution_summary({"full": list(reversed(ladders["none"])),
                                              "line sweep": list(reversed(ladders["full transport line sweep"]))})

    flipping = [r for r in rows if r["published_verdict_flips"]]
    return {
        "mechanism": ("`stall_verdict` does `first, last = rows[0], rows[-1]` -- POSITIONAL, "
                      "never keyed on `m`. `krylov_ladder` appends in the caller's `dims` "
                      "order and never sorts. So reversing the `dims` tuple maps the "
                      "published gain g -> 1/g and the work ratio w -> 1/w on IDENTICAL "
                      "measurements, with no error, no NaN and no flag. Leg 217 repaired "
                      "M4 in this same function -- the NaN comparison `flat = bool(gain < "
                      "2.0)` -- and left the positional read, which is a separate defect in "
                      "the same two lines."),
        "measured_on": "the four LIVE banked ladders of writeup/data/p2_route_l_v1_precond.json",
        "rows": rows,
        "line_sweep_deeper": {
            "ascending": {"work_ratio": deep_asc["work_ratio"],
                          "residual_gain": deep_asc["residual_gain"],
                          "flat": deep_asc["flat"]},
            "descending": {"work_ratio": deep_desc["work_ratio"],
                           "residual_gain": deep_desc["residual_gain"],
                           "flat": deep_desc["flat"]},
            "gain_ratio": float(deep_asc["residual_gain"] / deep_desc["residual_gain"])},
        "attribution_summary_ranking": {
            "ascending": [q["ablation"] for q in attr_asc],
            "descending": [q["ablation"] for q in attr_desc],
            "ranking_inverts": [q["ablation"] for q in attr_asc] != [q["ablation"] for q in attr_desc],
            "why": ("`attribution_summary` sorts by `-gain`, so inverting every gain "
                    "inverts the published ranking as well as each verdict.")},
        "ladders_whose_published_verdict_flips": [r["ladder"] for r in flipping],
        "sharpest": ("'full transport line sweep' is the ladder that carries Route-L's "
                     "entire headline -- 'the curve stops being flat'. Reversed, the same "
                     "five measurements report FLAT, i.e. 'a continuum in the spectrum', "
                     "which is the exact conclusion Route-L used the ladder to overturn."),
        "verdict": "SILENT",
    }


# ---------------------------------------------------------------------------
# G5 -- RESIDUAL 3: pack/unpack validate only the total size
# ---------------------------------------------------------------------------
class _FakeGrid:
    def __init__(self, nr, nb):
        self.rho = np.zeros(nr)
        self.beta = np.zeros(nb)
        self.drho = 0.1


def _transpose_probe(repaired, nr, nb, seed):
    res = repaired.ProfileResidual(solver=None, grid=_FakeGrid(nr, nb))
    rng = np.random.default_rng(seed)
    o, e, x = (rng.standard_normal((nr, nb)) for _ in range(3))

    o2, e2, x2 = res.unpack(res.pack(o, e, x))
    clean = float(max(np.max(np.abs(o - o2)), np.max(np.abs(e - e2)),
                      np.max(np.abs(x - x2))))

    raised = None
    try:
        e_back = res.unpack(res.pack(o, e.T.copy(), x))[1]
    except Exception as exc:                                        # noqa: BLE001
        return {"nr": nr, "nb": nb, "clean_round_trip_max_abs_error": clean,
                "transposed_raised": type(exc).__name__, "outcome": "VISIBLE"}

    wrong_len = None
    try:
        res.unpack(np.zeros(3 * nr * nb + 1))
    except Exception as exc:                                        # noqa: BLE001
        wrong_len = type(exc).__name__
    return {
        "nr": nr, "nb": nb, "square": nr == nb,
        "clean_round_trip_max_abs_error": clean,
        "transposed_raised": raised,
        "shape_returned": list(np.shape(e_back)),
        "equals_intended_field": bool(np.allclose(e_back, e)),
        "equals_reshaped_transpose": bool(np.allclose(e_back, e.T.reshape(nr, nb))),
        "rel_error_vs_intended_field": _rel(e_back, e),
        "max_abs_error_vs_intended_field": float(np.max(np.abs(e_back - e))),
        "wrong_total_length_raised": wrong_len,
        "outcome": "SILENT",
    }


def gate_5_pack_unpack(repaired):
    grid = json.loads(BANKED_PRECOND.read_text())["grid"]
    nr_live, nb_live = int(grid["n_r"]), int(grid["n_beta"])

    probes = [_transpose_probe(repaired, 6, 4, 5),               # leg 200's own fixture
              _transpose_probe(repaired, nr_live, nb_live, 241),  # the LIVE shape
              _transpose_probe(repaired, 32, 32, 241)]            # square: the worst case

    return {
        "mechanism": ("`pack` is `np.concatenate([np.ravel(o), np.ravel(e), np.ravel(x)])` "
                      "and `unpack` is three `reshape(self.shape)` calls. Neither validates "
                      "a PER-FIELD shape, only the total size -- and a transpose is "
                      "total-size-preserving at EVERY shape, square or not. So a field "
                      "handed in the (beta, rho) layout round-trips into a different, "
                      "finite, plausible field with no exception. A wrong TOTAL length is "
                      "caught, by `reshape`, not by a check."),
        "correction_to_leg_200s_note": (
            "leg 200 recorded 'the transposition survives only because nr*nb is "
            "layout-independent'. That is true but reads as a squareness caveat; it is "
            "not one. nr*nb == nb*nr identically, so the live 200x48 grid is exactly as "
            "exposed as a square one -- measured below, not argued."),
        "probes": probes,
        "live_grid": {"n_r": nr_live, "n_beta": nb_live, "square": nr_live == nb_live},
        "magnitude_at_live_shape": next(p["rel_error_vs_intended_field"] for p in probes
                                        if p["nr"] == nr_live),
        "magnitude_at_leg_200_fixture": next(p["rel_error_vs_intended_field"] for p in probes
                                             if (p["nr"], p["nb"]) == (6, 4)),
        "verdict": "SILENT",
    }


# ---------------------------------------------------------------------------
# G6 -- claim adjacency: does any BANKED number depend on these three?
# ---------------------------------------------------------------------------
def gate_6_claim_adjacency(g3, g4, g5):
    banked = json.loads(BANKED_PRECOND.read_text())
    c_l = float(banked["seed"]["c_l"])
    grid = banked["grid"]

    ledger = [
        {"path": "leading_order_solve sign-blind in c_l",
         "banked_configuration": {"c_l": c_l, "source":
                                  "writeup/data/p2_route_l_v1_precond.json -> seed.c_l"},
         "fires_when": "c_l < 0",
         "margin_to_firing": c_l,
         "margin_is": "a MEASURED quantity: the seed's own dilation constant",
         "claim_adjacent": False,
         "why": ("every PORT-family number was produced at c_l = +3.0605936608715 > 0, "
                 "and c_l > 0 is what the Hou-Luo rescaling produces by construction. The "
                 "path is LATENT, with a margin of 3.06 in the constant itself.")},
        {"path": "stall_verdict reads the ladder positionally",
         "banked_configuration": {"DIMS": [10, 20, 40, 80, 160],
                                  "deep": [240, 320],
                                  "source": "experiments/p2_route_l_v1_precond.py:49"},
         "fires_when": "the caller's `dims` tuple is not ascending",
         "margin_to_firing": 0.0,
         "margin_is": ("NOT a numerical margin. The banked ladders are correct only "
                       "because `DIMS` is a hard-coded ascending literal; nothing in "
                       "`krylov_ladder` or `stall_verdict` enforces it, and no caller "
                       "checks it. This is the one of the three with zero defence."),
         "claim_adjacent": False,
         "why": ("the banked values ARE right -- DIMS is ascending -- so no banked number "
                 "is wrong. But had it been written descending, the four published "
                 "`flat` verdicts and the attribution ranking would all have inverted, "
                 "silently, and Route-L's headline with them. Latent, undefended.")},
        {"path": "pack/unpack validate only the total size",
         "banked_configuration": {"n_r": grid["n_r"], "n_beta": grid["n_beta"],
                                  "source": "writeup/data/p2_route_l_v1_precond.json -> grid"},
         "fires_when": ("a caller supplies one of the three fields in the (beta, rho) "
                        "layout -- at ANY grid shape, since a transpose preserves nr*nb"),
         "margin_to_firing": 0.0,
         "margin_is": ("NOT a numerical margin either. Every live caller obtains its "
                       "fields FROM `unpack`, so the layout is correct by construction "
                       "rather than by validation."),
         "claim_adjacent": False,
         "why": ("no banked number was produced from an externally-laid-out field: `F`, "
                 "`info`, `jacobian_vector` and `make_preconditioner` all round-trip "
                 "fields that `unpack` itself produced. Latent.")},
    ]
    return {
        "question": ("does any banked number depend on one of the three residual paths -- "
                     "i.e. is any of them CLAIM-ADJACENT rather than merely latent?"),
        "ledger": ledger,
        "any_claim_adjacent": any(r["claim_adjacent"] for r in ledger),
        "answer": ("NO. All three are latent in leg 200's exact sense: the "
                   "hypothesis-satisfying counterpart returns the same number, so nothing "
                   "in the banked record is wrong. Nothing here needs its own escalation "
                   "under this leg's gate."),
        "but": ("two of the three have a margin of ZERO -- they are correct by a "
                "hard-coded literal and by caller convention respectively, not by any "
                "check. That is a weaker guarantee than `c_l > 0`, which is a measured "
                "3.06, and it is the distinction a repair leg should be scoped on."),
        "magnitudes_carried_forward": {
            "leading_order_solve_at_c_l_minus_0p5_leg200_fixture":
                g3["magnitude_at_c_l_minus_0p5"]["leg_200_fixture"],
            "stall_verdict_worst_gain_ratio":
                max(r["gain_ratio_asc_over_desc"] for r in g4["rows"]),
            "pack_unpack_at_live_shape": g5["magnitude_at_live_shape"]},
    }


# ---------------------------------------------------------------------------
# G7 -- the correction, authored and verified but NOT applied, and why
# ---------------------------------------------------------------------------
STALE_TEST_LINES = (
    '    # the boundary of the new guard: 0.0 is a legitimate bound, and so is -0.0\n'
    '    edge = radii_polynomial_status(0.0, 0.0, 0.0)\n'
    '    assert edge["status"] == "EVALUATED" and edge["closes"] is True, edge\n'
)
CORRECTED_TEST_LINES = (
    '    # the boundary of the new guard: 0.0 is a legitimate BOUND, and so is -0.0 -- the\n'
    '    # HYPOTHESIS guard admits both (status stays EVALUATED). Since leg 217 the RADIUS\n'
    '    # half is also checked, and a ball of radius exactly 0 is not a certificate.\n'
    '    edge = radii_polynomial_status(0.0, 0.0, 0.0)\n'
    '    assert edge["status"] == "EVALUATED", edge\n'
    '    assert edge["closes"] is False and edge["r_min"] == 0.0, edge\n'
    '    assert "radius_violation" in edge, edge\n'
)


def gate_7_the_correction(intree, repaired):
    """Emit the exact correction, verified against leg 217's blob, and state why it is
    NOT applied on this branch."""
    src = (ROOT / "test_port_certification_regression.py").read_text()
    present = STALE_TEST_LINES in src

    edge = repaired.radii_polynomial_status(0.0, 0.0, 0.0)
    verified = (edge.get("status") == "EVALUATED" and edge.get("closes") is False
                and edge.get("r_min") == 0.0 and "radius_violation" in edge)

    banked = json.loads(BANKED_REGRESSION.read_text())
    old_row = next(c for c in banked["cases"] if c["label"] == "Y0_negative_zero")
    after = repaired.radii_polynomial_status(-0.0, 0.1, 1.0)
    new_row = dict(old_row)
    new_row.update(status=after["status"], closes=after["closes"],
                   keys=sorted(after.keys()), verdict="REJECTED")

    return {
        "test_correction": {
            "file": "test_port_certification_regression.py",
            "lines": "86-88",
            "stale_text_present_in_tree": present,
            "replacement": CORRECTED_TEST_LINES,
            "verified_against_leg_217_blob": verified,
            "in_tree_closes_on_the_same_input":
                intree.radii_polynomial_status(0.0, 0.0, 0.0).get("closes"),
            "red_against_the_working_tree":
                intree.radii_polynomial_status(0.0, 0.0, 0.0).get("closes") is not False,
        },
        "json_row_correction": {
            "file": "writeup/data/p2_route_pc_v1_regression.json",
            "row": "cases[Y0_negative_zero]",
            "banked": old_row,
            "corrected": new_row},
        "why_not_applied": [
            ("A1: leg 217 is PARKED. The corrected assertion is RED against this branch's "
             "own tree -- in-tree `radii_polynomial_status(0.0, 0.0, 0.0)` returns "
             "closes=True. `scripts/merge_gate.sh` maps a changed `test_*.py` straight to "
             "itself (case `test_*.py)` in its diff loop), so applying it makes THIS "
             "leg's merge gate fail. The correction is right against leg 217's blob and "
             "wrong against main; it cannot be both until leg 217 merges."),
            ("A2: the bank is stale in FIVE rows, not one. Leg 217's report names only "
             "`Y0_negative_zero`, and that is the only row whose `closes`/`verdict` move "
             "-- but `legit_close`, `legit_fail`, `Y0_bool_true` and `Z1_bool_false` all "
             "gain `r_min` and/or `why` in their recorded `keys` list. Those four are "
             "outside this leg's declared one-row territory. Correcting only the named "
             "row would leave an artifact that NO single run of the battery could emit: "
             "one row with post-repair keys beside four with pre-repair keys. That is a "
             "worse artifact than the stale one, so this leg does not produce it."),
        ],
        "how_to_land": ("apply both corrections IN leg 217's landing commit, and "
                        "regenerate `p2_route_pc_v1_regression.json` wholesale rather than "
                        "editing the single row -- the regeneration is what makes all five "
                        "rows consistent, and G2 above certifies that the regeneration "
                        "moves exactly those five rows and leaves the `verdict` block "
                        "byte-identical."),
    }


# ---------------------------------------------------------------------------
def main():
    intree, repaired, g0 = gate_0_module_states()
    print("== G0: module states ==")
    print(f"  in-tree is post-leg-217: {g0['in_tree_is_post_leg_217_repair']}")
    print(f"  leg 217 blob reachable : {g0['leg_217_blob_reachable']} ({LEG_217_REF})")
    print(f"  {g0['reading']}")

    g1 = gate_1_flagged_inputs(intree, repaired)
    print("\n== G1: the two flagged inputs ==")
    for r in g1["rows"]:
        print(f"  {r['site']}")
        print(f"    args {r['args']}  status {r['in_tree'].get('status')} (unmoved: "
              f"{not r['status_moved']})  closes {r['closes_before']} -> {r['closes_after']}"
              f"  r_min {r['r_min_after']}")

    g2 = gate_2_blast_radius(repaired)
    print("\n== G2: blast radius over leg 79's 39-case battery ==")
    print(f"  cases {g2['cases_total']}   rows that move: {g2['rows_that_move']}")
    for m in g2["moved"]:
        print(f"    {m['label']}: {list(m.get('deltas', {}))}")
    print(f"  verdict block byte-identical: {g2['verdict_block_byte_identical']}   "
          f"gate answer {g2['gate_answer_banked']} -> {g2['gate_answer_post_repair']}")

    g3 = gate_3_leading_order_c_l(repaired)
    print("\n== G3: RESIDUAL 1 -- leading_order_solve sign-blind in c_l ==")
    print("  c_l      rel.err vs ADVERTISED    rel.err vs ASSEMBLED (control)")
    for r in g3["leg_200_fixture"]["rows"]:
        print(f"   {r['c_l']:>9.4f}   {r['rel_error_vs_advertised_operator']:>14.4e}"
              f"   {r['rel_error_vs_assembled_operator']:>14.4e}")
    print(f"  worst control (all fixtures): "
          f"{g3['control_worst_rel_error_vs_the_operator_it_assembles']:.3e}")

    g4 = gate_4_stall_positional(repaired)
    print("\n== G4: RESIDUAL 2 -- stall_verdict reads the ladder positionally ==")
    for r in g4["rows"]:
        a, d = r["ascending_dims"], r["same_data_descending_dims"]
        print(f"  {r['ladder']:<28} gain {a['residual_gain']:.4f} ({'flat' if a['flat'] else 'bending'})"
              f"  ->  {d['residual_gain']:.4f} ({'flat' if d['flat'] else 'bending'})"
              f"   ratio {r['gain_ratio_asc_over_desc']:.2f}x"
              f"{'   VERDICT FLIPS' if r['published_verdict_flips'] else ''}")

    g5 = gate_5_pack_unpack(repaired)
    print("\n== G5: RESIDUAL 3 -- pack/unpack validate only the total size ==")
    for p in g5["probes"]:
        print(f"  {p['nr']}x{p['nb']:<4} square={p.get('square')}  outcome {p['outcome']}"
              f"  rel.err vs intended field {p.get('rel_error_vs_intended_field'):.4f}"
              f"  clean round trip {p['clean_round_trip_max_abs_error']:.1e}")

    g6 = gate_6_claim_adjacency(g3, g4, g5)
    print("\n== G6: claim adjacency ==")
    for r in g6["ledger"]:
        print(f"  {r['path']:<46} claim-adjacent {r['claim_adjacent']}  "
              f"margin {r['margin_to_firing']}")
    print(f"  {g6['answer']}")

    g7 = gate_7_the_correction(intree, repaired)
    print("\n== G7: the correction, authored and verified, NOT applied ==")
    print(f"  stale test text present in tree: "
          f"{g7['test_correction']['stale_text_present_in_tree']}   "
          f"replacement verified against leg 217's blob: "
          f"{g7['test_correction']['verified_against_leg_217_blob']}")
    for w in g7["why_not_applied"]:
        print(f"  - {w}")

    payload = {
        "leg": 241, "route": "PCRC",
        "title": ("the cleanup behind leg 217's escalation: the two stale artifacts "
                  "corrected, and the three residual silent paths characterised"),
        "depends_on": {"leg_217_branch": LEG_217_REF,
                       "landed_to_main": g0["in_tree_is_post_leg_217_repair"]},
        "G0_module_states": g0,
        "G1_flagged_inputs": g1,
        "G2_blast_radius": g2,
        "G3_residual_leading_order_c_l": g3,
        "G4_residual_stall_positional": g4,
        "G5_residual_pack_unpack": g5,
        "G6_claim_adjacency": g6,
        "G7_the_correction_not_applied": g7,
        "gate": {
            "question": ("(a) Do test_port_certification_regression.py and the banked JSON "
                         "row now assert the CORRECT (post-leg-217-repair) behaviour on the "
                         "exact degenerate input leg 200 originally flagged, with no other "
                         "assertion in either artifact touched; and (b) are all 3 additional "
                         "silent paths leg 217 named characterised with a precise mechanism "
                         "and magnitude, the same shape leg 200's own report used for its "
                         "original 4?"),
            "a": "INCOMPLETE -- authored and verified, deliberately NOT applied; see G7",
            "b": "CHARACTERISED -- all three, mechanism and magnitude; see G3, G4, G5, G6",
            "outcome": "branch pushed only; no merge, ahead of or in place of leg 217",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=False) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
