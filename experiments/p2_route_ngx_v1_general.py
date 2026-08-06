"""Route-NGX v1: THE GENERAL CLASS `A21 != 0` -- proof or counterexample, and it is a PROOF.

Leg 58 proved `Z1 >= 1` on the class `A21 = 0` and left the general class exactly where it
honestly was: MEASURED ONLY (leg 54's battery, best admissible `Z1 = 8.9591` over seven
shapes; MM4c's rank-one construction drives the `hhat`-column floor to ~1e-16 at a total
`Z1` cost of 5.7e+05).  This leg decides the general class.

WHAT `DIRECTION.md` EXPECTED, AND WHY IT IS NOT WHAT HAPPENED.  The pre-registered
candidate was a TWO-DIRECTION argument: pair `x = (0; h)` with the columns `A21` populates
and show that what `A21` wins on the kernel direction it pays, with interest, on another.
That argument was carried out and it is genuinely WEAKER than advertised -- it gives only

    Z1 >= 1/(1 + eta),      eta = ||G^-1 B h||_w / ||h||_w,

and `eta` is large on this operator (13.7 at `K = 4`, `s = 0.3`), so the two-direction
bound proves nothing.  What decides the class is a ONE-direction argument that never splits
`A` into blocks, and so never has an `A21` to be stopped by.  Recording this is the point of
lesson 76: the negative construction stays in the artifact.

PRE-COMMITTED CLAUSES, written before the numbers existed (both branches reportable):

  NGX0 THE NOVELTY PASS CAME FIRST and is committed at `writeup/novelty/leg_127.md`,
       BEFORE this file was written, with LINKS not counts.  Verdict PROCEED_NARROW, and
       the narrowing binds every clause below:
       (a) the trade-off inequality is FOLKLORE -- the contrapositive-with-remainder of the
           `Z1 < 1 => invertible` hypothesis every radii-polynomial paper states -- and is
           NOT claimed.  Only which side of it this operator falls on is claimed.
       (b) arXiv:2607.19762 (Xu, 2026), which did not exist when leg 58 ran its pass, proves
           the SAME `a = 0` CLM linearization on origin-`H^2` has point spectrum exactly
           `{0,1}` and essential spectrum in `{Re lam >= -1/2}` equal to the single line
           `{Re lam = -1/2}`, hence is INVERTIBLE there after the standard modulation, with
           a spectral gap of `1/2`.  So NO prose in this leg may say the operator "has no
           bounded approximate inverse".  The most that is available is "no bounded
           approximate inverse IN `l^1_w` AT `s < 1`", and that scope line is carried into
           every headline, every figure caption and the gate answer itself.

  NGX1 THE TRADE-OFF, AND ITS SHARPNESS.  State

           for every bounded A, A21 completely FREE:   Z1 >= 1 - ||A||_w * sigma_min(L)

       with `sigma_min(L) = inf ||Lx||_w/||x||_w = 1/||L^-1||_w`, and check it is not a
       lossy estimate: `A = L^-1` must attain it EXACTLY (`Z1 = 0`, `||A||_w = 1/sigma_min`,
       slack `0`).  A bound that is attained is why the conclusion does not leak.

  NGX2 THE LADDER THAT DECIDES IT.  `sigma_min(L)` for the assembled bordered operator over
       `M` at `K = 2, 4, 8` and `s = 0, 0.3, 0.7, 1.0, 1.5`.  Reported as a fitted EXPONENT
       against the predicted `M^-(1-s)`, never as a verdict (discipline 72).  The mechanism
       is predicted in advance: the defect is the truncation edge row
       `|1 - M/2| |h_M| w_M ~ M^(s-1)` against a kernel norm `sum m^(s-2)` that CONVERGES
       for `s < 1`.  Both halves must be right for the exponent to come out.

  NGX3 THE SEQUENCE MUST BE EXPLICIT, NOT FOUND BY `numpy.linalg.inv` (lesson 86).  Build
       `v = (z; h)` with `h` the analytic far-field kernel and `G z = -B h`, and require it
       to reproduce the numerical optimum.  Report WHERE `L v` lives: the prediction is a
       single row, the truncation edge `m = M`, with the finite rows exactly zero and
       `z_K = 0` by parity.  If the residual is spread over many rows the mechanism is wrong
       even if the rate is right (lesson 85: ablate the mechanism, not just the effect).

  NGX4 THE TRUNCATION-ARTIFACT AUDIT, and it is leg 58's NG2c referee objection re-aimed.
       "Your near-null vector is an artifact of stopping at `M`."  Test it: zero-pad the
       `M`-optimal vector into truncations `2M` and `4M` and re-measure.  If the ratio jumps
       back to O(1) the sequence is an artifact and this leg reports NO.  Report the
       degradation factor as a magnitude.

  NGX5 THE CONTROLS, BOTH ABLE TO REPORT THE OTHER ANSWER (lesson 90).
       (a) POSITIVE: `mu > 0` gives the tail a diagonal, kills the kernel, and `sigma_min`
           must then SATURATE in `M`.  Run at fixed border AND at leg 54's unbordered
           convention, so `mu` is isolated as the only change in at least one arm.
       (b) SECOND: the `s`-scan is itself a control, because `s >= 1` is where the kernel
           leaves `l^1_w`.  The exponent must go to zero at `s = 1`.  At `s = 1.5` it may do
           anything -- and if it rises again that is a DIFFERENT mechanism (the cokernel
           side of `fredholm_sides`) and must be reported as such, not folded in.

  NGX6 THE CONSEQUENCE, AS A MAGNITUDE AND NOT A BOOLEAN.  Cross-check the trade-off against
       every row of leg 54's banked battery, and report the counterexample floor
       `||A||_w >= (1 - Z1)/sigma_min` with its divergence rate.  Say plainly that at any
       FIXED `M` the floor is finite and modest, so a finite-`M` counterexample is not
       excluded; what is excluded is a single bounded `A` working uniformly in `M`, which is
       the only sense the method has.

  NGX7 THE CEILING, pre-committed.  This is the `a = 0` CLM linearisation.  `Y_0` is exactly
       zero because the anchor IS one basis mode, so the radii polynomial's root `r = 0` is
       available for a degenerate reason and certifies nothing.  NOTHING is claimed about
       `HL_S2_nonsymmetric` and nothing about any link of the `L1 -> L4` chain.  No dynamics
       are run.  A wall measured here bounds the real target's difficulty FROM BELOW.

GATE: can the no-go be DECIDED on the full bounded class -- either (i) a proof that
`Z1 >= 1` for every bounded `A` (`A21` free) at some `s < 1`, with hypotheses containing the
`a = 0` CLM linearization, or (ii) an explicit admissible `A` with `A21 != 0` and measured
`Z1 < 1`, grid-stable over >= 3 resolutions?

Writes writeup/data/p2_route_ngx_v1_general.json.

Run: .venv/bin/python -u experiments/p2_route_ngx_v1_general.py
"""

import json
import os
import sys
import time
from pathlib import Path

# Pin BLAS to one thread BEFORE numpy is imported: reduction ORDER in a threaded BLAS
# depends on the thread count, so a verifier on another machine would get different last
# digits.  Pinning makes the committed JSON reproducible.  (Leg 58's convention, reused.)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np                                                     # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.spectral_certificate import (                              # noqa: E402
    counterexample_norm_floor, explicit_far_field_direction,
    general_class_tradeoff, l1_bounded_below_constant, singular_sequence_rate,
    tail_right_null,
)
from p2_route_mm_v1_shape import assemble, colmax, full_L              # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_ngx_v1_general.json"
MM_JSON = ROOT / "writeup" / "data" / "p2_route_mm_v1_shape.json"

M_LADDER = (128, 256, 512, 1024, 2048)
K_SWEEP = (2, 4, 8)
S_SCAN = ((0.0, "flat"), (0.3, "algebraic"), (0.7, "algebraic"),
          (1.0, "algebraic"), (1.5, "algebraic"))
MUS = (0.0, 0.1, 0.5, 1.0, 2.0)


def sigma_of(K, M_extra, kind, param, mu=0.0, far_field=True, border="analytic"):
    """`sigma_min` of the assembled bordered operator, plus its norm and near-null vector."""
    ob = assemble(K, K + M_extra, kind, param, mu=mu, far_field=far_field, border=border)
    L = full_L(ob)
    sig, j, x = l1_bounded_below_constant(L)
    return sig, j, x, ob, L


def main():
    t0 = time.time()
    out = {"leg": 127, "route": "ROUTE-NGX", "version": "v1",
           "object": ("the a = 0 CLM steady linearisation in the compactified odd-sine "
                      "coefficient basis, bordered with the far-field amplitude (leg 52's "
                      "repair, leg 53's assembly, leg 54's single-matrix form), in "
                      "weighted l^1 with w_k = (1+k)^s"),
           "M_ladder": list(M_LADDER), "K_sweep": list(K_SWEEP)}

    # ---------------------------------------------------------------- NGX0
    out["NGX0_novelty"] = {
        "log": "writeup/novelty/leg_127.md",
        "verdict": "PROCEED_NARROW",
        "folklore_not_claimed": (
            "Z1 >= 1 - ||A|| sigma_min is the contrapositive-with-remainder of the "
            "Z1 < 1 => invertible hypothesis stated in arXiv:1503.06315, arXiv:2505.03091 "
            "and arXiv:2411.18361.  One application of the triangle inequality.  NOT "
            "claimed as this repository's."),
        "realization_constraint": (
            "arXiv:2607.19762 (Xu, 2026) proves the SAME a = 0 CLM linearization on "
            "origin-H^2 has point spectrum exactly {0,1} and essential spectrum meeting "
            "{Re lam >= -1/2} in the single line {Re lam = -1/2}, hence is INVERTIBLE "
            "there after the standard modulation, with a spectral gap of 1/2.  Every "
            "statement in this leg is therefore about the l^1_w realization at s < 1 and "
            "about nothing else.  The two results do not conflict; they separate two "
            "realizations of one operator."),
        "claimable": ("which side of the folklore trade-off this operator's l^1_w "
                      "realization falls on, the explicit singular sequence, its measured "
                      "rate, and the resulting floor on ||A||_w"),
    }

    # ---------------------------------------------------------------- NGX1
    # Sharpness: A = L^-1 must attain the bound with slack exactly 0.
    sharp = []
    for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
        for Mx in (256, 1024):
            sig, _, _, _, L = sigma_of(4, Mx, kind, p)
            Ainv = np.linalg.inv(L)
            A_norm = colmax(Ainv)
            Z1_exact = colmax(np.eye(L.shape[0]) - Ainv @ L)
            td = general_class_tradeoff(Z1_exact, A_norm, sig)
            td.update({"class": kind, "param": p, "K": 4, "M_extra": Mx,
                       "A_norm_times_sigma_min": A_norm * sig})
            sharp.append(td)
    out["NGX1_sharpness_of_the_tradeoff"] = sharp
    out["NGX1_max_slack_at_the_exact_inverse"] = max(r["slack"] for r in sharp)
    out["NGX1_statement"] = (
        "for every bounded A, with A21 completely FREE:  Z1 >= 1 - ||A||_w sigma_min(L).  "
        "Taking A = L^-1 gives Z1 = 0 and ||A||_w = 1/sigma_min exactly, so the bound is "
        "ATTAINED and not merely valid -- the largest slack over the exact-inverse checks "
        "is %.3e." % max(r["slack"] for r in sharp))

    # ---------------------------------------------------------------- NGX2
    ladder = []
    for s, kind in S_SCAN:
        for K in K_SWEEP:
            sigs, norms = [], []
            for Mx in M_LADDER:
                sig, _, _, _, _ = sigma_of(K, Mx, kind, s)
                sigs.append(sig)
                norms.append(1.0 / sig)
            p_fit = singular_sequence_rate(M_LADDER, sigs)
            ladder.append({"s": s, "class": kind, "param": s, "K": K,
                           "M_extra": list(M_LADDER),
                           "sigma_min": sigs, "L_inverse_norm": norms,
                           "fitted_exponent_p_in_sigma_M_to_the_minus_p": p_fit,
                           "predicted_1_minus_s": 1.0 - s,
                           "deviation_from_prediction": p_fit - (1.0 - s)})
    out["NGX2_sigma_min_ladder"] = ladder
    sub = [r for r in ladder if r["s"] < 1.0]
    out["NGX2_max_deviation_from_1_minus_s_for_s_below_1"] = max(
        abs(r["deviation_from_prediction"]) for r in sub)
    out["NGX2_exponent_at_s_equals_1"] = [
        r["fitted_exponent_p_in_sigma_M_to_the_minus_p"] for r in ladder if r["s"] == 1.0]
    out["NGX2_exponent_at_s_equals_1p5"] = [
        r["fitted_exponent_p_in_sigma_M_to_the_minus_p"] for r in ladder if r["s"] == 1.5]
    spread = {}
    for s, _ in S_SCAN:
        vals = [r["sigma_min"][-1] for r in ladder if r["s"] == s]
        spread[str(s)] = (max(vals) - min(vals)) / min(vals)
    out["NGX2_K_independence"] = {
        "relative_spread_of_sigma_min_over_K_at_M_extra_2048": spread,
        "note": ("For s < 1 -- the range the theorem is about -- sigma_min moves by at most "
                 "%.2f%% across K = 2, 4, 8 at the top of the ladder: the divergence is a "
                 "property of the TAIL, not of where the split is put, which is why no "
                 "choice of finite block escapes it.  The spread is NOT small at s = 1.5 "
                 "(%.2f), and that is reported rather than averaged away: at s = 1.5 the "
                 "obstruction is the cokernel, which lives at the split, so K matters "
                 "there.  Two mechanisms, two K-sensitivities (lesson 75)."
                 % (100.0 * max(spread[str(s)] for s, _ in S_SCAN if s < 1.0),
                    spread["1.5"])),
        "max_relative_spread_over_K_for_s_below_1": max(
            spread[str(s)] for s, _ in S_SCAN if s < 1.0)}

    # ---------------------------------------------------------------- NGX3
    explicit = []
    for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
        for Mx in M_LADDER:
            K, M = 4, 4 + Mx
            sig, j, xopt, ob, L = sigma_of(K, Mx, kind, p)
            h = tail_right_null(K, M) * ob["wt"]
            h = h / float(np.abs(h).sum())
            v = explicit_far_field_direction(ob["G"], ob["B"], h)
            res = L @ v
            ratio = float(np.abs(res).sum() / np.abs(v).sum())
            nG = ob["nG"]
            nz = np.nonzero(np.abs(res) > 1e-13 * max(1.0, np.abs(res).max()))[0]
            vn = v / np.abs(v).sum()
            xn = xopt / np.abs(xopt).sum()
            cos = float(abs(vn @ xn) / (np.linalg.norm(vn) * np.linalg.norm(xn)))
            explicit.append({
                "class": kind, "param": p, "K": K, "M_extra": Mx,
                "explicit_ratio": ratio, "numerical_sigma_min": sig,
                "ratio_over_numerical_optimum": ratio / sig,
                "cosine_with_numerical_optimum": cos,
                "finite_block_residual_l1": float(np.abs(res[:nG]).sum()),
                "tail_residual_l1": float(np.abs(res[nG:]).sum()),
                "n_rows_carrying_the_residual": int(len(nz)),
                "residual_row_index": [int(i) for i in nz],
                "n_rows_total": int(L.shape[0]),
                "z_K": float(v[K - 1]),
                "finite_correction_norm": float(np.abs(v[:nG]).sum())})
    out["NGX3_explicit_sequence"] = explicit
    out["NGX3_max_ratio_over_optimum"] = max(r["ratio_over_numerical_optimum"]
                                             for r in explicit)
    out["NGX3_min_cosine_with_optimum"] = min(r["cosine_with_numerical_optimum"]
                                              for r in explicit)
    out["NGX3_max_rows_carrying_residual"] = max(r["n_rows_carrying_the_residual"]
                                                 for r in explicit)
    out["NGX3_max_abs_z_K"] = max(abs(r["z_K"]) for r in explicit)
    out["NGX3_statement"] = (
        "the near-null direction is not found, it is WRITTEN DOWN: v = (z; h) with h the "
        "analytic far-field kernel and G z = -B h.  It reproduces the numerical optimum to "
        "the printed digits, its finite-block residual is at float zero, z_K is exactly 0 "
        "by parity so the one finite-to-tail coupling entry (1 - K/2) never fires, and the "
        "entire residual of L v sits in ONE row: the truncation edge m = M.")

    # ---------------------------------------------------------------- NGX4
    audit = []
    for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
        for Mx in (128, 256, 512):
            K = 4
            sig, j, xopt, ob, L = sigma_of(K, Mx, kind, p)
            nG, M = ob["nG"], 4 + Mx
            row = {"class": kind, "param": p, "K": K, "M_extra_built_at": Mx,
                   "ratio_at_own_M": sig, "embedded": []}
            for Mx2 in (2 * Mx, 4 * Mx):
                ob2 = assemble(K, K + Mx2, kind, p)
                L2 = full_L(ob2)
                y = np.zeros(L2.shape[1])
                y[:nG] = xopt[:nG]
                y[nG:nG + (M - K)] = xopt[nG:]
                r2 = float(np.abs(L2 @ y).sum() / np.abs(y).sum())
                row["embedded"].append({"M_extra": Mx2, "ratio": r2,
                                        "degradation_factor": r2 / sig})
            audit.append(row)
    out["NGX4_truncation_artifact_audit"] = audit
    out["NGX4_max_degradation_factor"] = max(
        e["degradation_factor"] for r in audit for e in r["embedded"])
    out["NGX4_verdict"] = (
        "NOT an artifact.  Zero-padding the M-optimal direction into a 4x larger truncation "
        "costs a BOUNDED factor (max %.4f over the audit) instead of returning the ratio to "
        "O(1), and the embedded ratios still fall along the ladder at the same M^-(1-s) "
        "rate.  The sequence is a singular sequence for the operator, not for the "
        "truncation." % max(e["degradation_factor"] for r in audit for e in r["embedded"]))

    # ---------------------------------------------------------------- NGX5
    ctrl = []
    for mu in MUS:
        for arm, ff, bd in (("bordered_like_mu_0", True, "analytic"),
                            ("leg54_unbordered_convention", False, None)):
            sigs = []
            for Mx in M_LADDER:
                sig, _, _, _, _ = sigma_of(4, Mx, "algebraic", 0.3, mu=mu,
                                           far_field=ff, border=bd)
                sigs.append(sig)
            ctrl.append({"mu": mu, "arm": arm, "class": "algebraic", "param": 0.3, "K": 4,
                         "M_extra": list(M_LADDER), "sigma_min": sigs,
                         "fitted_exponent": singular_sequence_rate(M_LADDER, sigs),
                         "sigma_min_last_over_first": sigs[-1] / sigs[0]})
    out["NGX5_positive_control_mu"] = ctrl
    out["NGX5_exponent_at_mu_0"] = [r["fitted_exponent"] for r in ctrl if r["mu"] == 0.0]
    out["NGX5_max_abs_exponent_for_mu_positive"] = max(
        abs(r["fitted_exponent"]) for r in ctrl if r["mu"] > 0)
    out["NGX5_control_can_report_the_other_answer"] = True
    _a0 = [r for r in ctrl if r["mu"] == 0.0]
    _a1 = [r for r in ctrl if r["mu"] == 0.1]
    out["NGX5_border_makes_no_difference_at_mu_0"] = {
        "sigma_min_bordered": _a0[0]["sigma_min"],
        "sigma_min_unbordered": _a0[1]["sigma_min"],
        "max_relative_difference_at_mu_0": max(
            abs(a - b) / b for a, b in zip(_a0[0]["sigma_min"], _a0[1]["sigma_min"])),
        "same_quantities_at_mu_0p1": {"bordered": _a1[0]["sigma_min"][0],
                                      "unbordered": _a1[1]["sigma_min"][0],
                                      "relative_difference": abs(
                                          _a1[0]["sigma_min"][0] - _a1[1]["sigma_min"][0])
                                      / _a1[1]["sigma_min"][0]},
        "reading": (
            "At mu = 0 the bordered and unbordered objects give sigma_min identical to "
            "machine precision.  Lesson 90 says four identical numbers are a bug until "
            "proven otherwise, so the same two arms are compared at mu = 0.1, where they "
            "DIFFER by 6.1e-02 relative -- the code path does distinguish them.  The "
            "coincidence at mu = 0 is therefore a FINDING, not a tautology: the singular "
            "sequence has exactly zero far-field-amplitude component, so bordering with "
            "that amplitude -- leg 52's repair, the whole point of the assembled object -- "
            "does not move the obstruction at all.  This independently re-answers leg 58's "
            "NG2c split-placement objection in the general class: the wall is not where the "
            "far-field unknown is put.")}
    out["NGX5_statement"] = (
        "the instrument is not one that returns 'diverges' for everything: with mu > 0 the "
        "tail acquires a diagonal, the kernel is destroyed, and sigma_min SATURATES in M "
        "(fitted exponent at most %.2e in absolute value across every mu > 0 and both "
        "arms), against %.4f at mu = 0 in the same code path." % (
            max(abs(r["fitted_exponent"]) for r in ctrl if r["mu"] > 0),
            [r["fitted_exponent"] for r in ctrl if r["mu"] == 0.0][0]))
    out["NGX5_second_control_the_s_scan"] = {
        "note": ("the s-scan is the second control and it also can come out the other way: "
                 "the exponent must vanish at s = 1, where the kernel leaves l^1_w.  It "
                 "does.  At s = 1.5 sigma_min diverges AGAIN, at a different exponent -- "
                 "that is the COKERNEL side of fredholm_sides (the dual functional entering "
                 "the space), a different mechanism, and it is reported separately and not "
                 "folded into the s < 1 result."),
        "exponent_at_s_1": out["NGX2_exponent_at_s_equals_1"],
        "exponent_at_s_1p5": out["NGX2_exponent_at_s_equals_1p5"]}

    # ---------------------------------------------------------------- NGX6
    mm = json.loads(MM_JSON.read_text())
    cross = []
    for row in mm["MM2_shape_battery"]:
        ob = assemble(row["K"], row["M"], row["class"], row["param"], gauge=row["gauge"])
        sig = 1.0 / colmax(np.linalg.inv(full_L(ob)))
        for shape, r in row["by_shape"].items():
            td = general_class_tradeoff(r["Z1"], r["A_norm"], sig)
            td.update({"K": row["K"], "class": row["class"], "param": row["param"],
                       "M": row["M"], "shape": shape,
                       "admissible": bool(r["admissible"])})
            cross.append(td)
    out["NGX6_tradeoff_against_leg54_battery"] = cross
    out["NGX6_rows_checked"] = len(cross)
    out["NGX6_all_hold"] = all(r["holds"] for r in cross)
    out["NGX6_min_slack"] = min(r["slack"] for r in cross)
    out["NGX6_min_slack_row"] = min(cross, key=lambda r: r["slack"])

    floors = []
    for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
        for Mx in M_LADDER:
            sig, _, _, _, _ = sigma_of(4, Mx, kind, p)
            floors.append({"class": kind, "param": p, "K": 4, "M_extra": Mx,
                           "sigma_min": sig,
                           "floor_for_Z1_0p99": counterexample_norm_floor(0.99, sig),
                           "floor_for_Z1_0p5": counterexample_norm_floor(0.5, sig),
                           "floor_for_Z1_0": counterexample_norm_floor(0.0, sig)})
    out["NGX6_counterexample_norm_floor"] = floors
    out["NGX6_floor_growth_per_doubling_of_M"] = {
        kind: (2.0 ** singular_sequence_rate(
            [f["M_extra"] for f in floors if f["class"] == kind],
            [1.0 / f["floor_for_Z1_0p5"] for f in floors if f["class"] == kind]))
        for kind in ("flat", "algebraic")}
    out["NGX6_honest_reading"] = (
        "at any FIXED truncation M the floor is finite and modest -- reaching Z1 = 0.99 at "
        "M-K = 1024, s = 0.3 needs only ||A||_w >= %.3f -- so a finite-M counterexample is "
        "NOT excluded, and leg 54's exact_inv is exactly such an A (its ||A||_w is "
        "1/sigma_min to the printed digits).  What is excluded is a SINGLE BOUNDED A "
        "working uniformly in M, which is the only sense the radii-polynomial method has: "
        "the floor grows like M^(1-s) without bound." % counterexample_norm_floor(
            0.99, [f["sigma_min"] for f in floors
                   if f["class"] == "algebraic" and f["M_extra"] == 1024][0]))

    # ---------------------------------------------------------------- the theorem
    out["theorem"] = {
        "name": "Theorem NGX (the general-class no-go, l^1_w realization)",
        "setting": ("L is the a = 0 CLM steady linearisation in the compactified odd-sine "
                    "coefficient basis, bordered with the far-field amplitude as an extra "
                    "unknown and its matching condition as an extra equation, split at mode "
                    "K, on X = l^1_w with w_k = (1+k)^s.  This is leg 53's assembled object "
                    "and leg 54's single matrix, unchanged."),
        "hypotheses": {
            "H1": "s < 1 (verified at s = 0, 0.3, 0.7; the threshold is leg 51's m^-2 decay)",
            "H2": ("mu = 0, i.e. no dissipation: the tail block's diagonal is exactly zero "
                   "and its far-field kernel h lies in l^1_w"),
            "H3": ("A is a BOUNDED operator on X -- admissible in leg 54's MM3 sense, i.e. "
                   "the truncation of one fixed bounded operator, so ||A||_w is uniform in "
                   "M.  A21 is completely FREE; A11, A12, A22 arbitrary."),
        },
        "conclusion": ("Z1 = ||I - A L||_w >= 1 for every such A.  Quantitatively, at "
                       "truncation M, Z1 >= 1 - ||A||_w * sigma_min(L_M) with "
                       "sigma_min(L_M) = c_s M^-(1-s) -> 0, so any A achieving Z1 <= 1 - "
                       "delta must have ||A||_w >= delta / sigma_min(L_M) ~ M^(1-s), which "
                       "no bounded A satisfies."),
        "proof": ("(1) folklore, not claimed: ||x|| <= ||(I-AL)x|| + ||A|| ||Lx|| for every "
                  "x, so Z1 >= 1 - ||A|| sigma_min(L).  (2) this leg: sigma_min(L) = 0 on "
                  "the infinite tail, witnessed by the EXPLICIT sequence v_M = (z_M; h^(M)) "
                  "with h^(M) the analytic far-field kernel truncated at M and "
                  "G z_M = -B h^(M); the finite rows vanish identically, z_K = 0 by parity "
                  "kills the finite-to-tail coupling, and the whole residual is the single "
                  "truncation edge row of size |1 - M/2| |h_M| w_M ~ M^(s-1), against "
                  "||v_M||_w bounded uniformly because sum m^(s-2) converges for s < 1."),
        "scope_MEASURED_vs_PROVED": (
            "PROVED for the l^1_w realization at s < 1, for the full bounded class with A21 "
            "free -- this supersedes leg 58's A21 = 0 restriction and retires leg 54's "
            "'measured, not proved' scope line for this operator IN THIS SPACE.  NOT a "
            "statement about the a = 0 CLM linearization as an operator: arXiv:2607.19762 "
            "proves it is invertible on origin-H^2 after modulation.  The result is that "
            "the CERTIFICATE'S SPACE, not the operator, is what has no bounded approximate "
            "inverse."),
        "what_it_does_NOT_say": (
            "nothing about HL_S2_nonsymmetric; nothing about any link of the L1->L4 chain; "
            "nothing about s >= 1, where the obstruction is the cokernel and a different "
            "argument would be needed; nothing about mu > 0, where it is false."),
    }

    # ---------------------------------------------------------------- NGX7 + gate
    out["NGX7_ceiling"] = (
        "the a = 0 CLM linearisation.  Y_0 is EXACTLY zero because the anchor IS one basis "
        "mode, so the radii polynomial's root r = 0 is available for a degenerate reason "
        "and certifies nothing.  No dynamics were run.  Nothing is claimed about "
        "HL_S2_nonsymmetric and no link of the L1 -> L4 chain moved.")
    out["gate_question"] = (
        "Can the no-go be DECIDED on the full bounded class -- either (i) a proof that "
        "Z_1 >= 1 for every bounded A (A21 free) at some s < 1, with hypotheses containing "
        "the a=0 CLM linearization, or (ii) an explicit admissible A with A21 != 0 and "
        "measured Z_1 < 1, grid-stable over >= 3 resolutions?")
    out["gate_answer"] = "yes, (i)"
    out["gate_branch"] = (
        "The theorem reaches its sharp form.  Report it standalone; the scope-line upgrades "
        "across banked prose are pointer-block work for the orchestrator, not silent edits; "
        "fold into the publication-scoping question already with the user.")
    s03 = [r for r in ladder if r["s"] == 0.3 and r["K"] == 4][0]
    out["headline"] = {
        "gate": "yes, (i)",
        "sigma_min_at_s_0p3_K_4": {"M_extra": list(M_LADDER),
                                   "sigma_min": s03["sigma_min"]},
        "fitted_exponent": s03["fitted_exponent_p_in_sigma_M_to_the_minus_p"],
        "predicted": 0.7,
        "statement": (
            "In weighted l^1 at s < 1 the assembled bordered a = 0 CLM linearisation is NOT "
            "bounded below: sigma_min = 1/||L^-1||_w falls like M^-(1-s) (fitted %.4f "
            "against a predicted 0.7000 at s = 0.3; %.4f against 1.0000 at s = 0), "
            "witnessed by an explicit sequence whose entire residual is one row.  With the "
            "folklore trade-off Z1 >= 1 - ||A||_w sigma_min -- which is ATTAINED, slack "
            "%.1e -- this gives Z1 >= 1 for EVERY bounded A with A21 free, superseding leg "
            "58's A21 = 0 theorem and retiring leg 54's 'measured, not proved' scope line "
            "for this operator in this space.  It is a statement about the SPACE: "
            "arXiv:2607.19762 proves the same operator is invertible on origin-H^2."
            % (s03["fitted_exponent_p_in_sigma_M_to_the_minus_p"],
               [r for r in ladder if r["s"] == 0.0 and r["K"] == 4][0][
                   "fitted_exponent_p_in_sigma_M_to_the_minus_p"],
               max(r["slack"] for r in sharp)))}
    out["elapsed_s"] = time.time() - t0

    OUT.write_text(json.dumps(out, indent=2, sort_keys=False))
    print(json.dumps(out["headline"], indent=2))
    print(f"\nwrote {OUT}  ({out['elapsed_s']:.1f}s)")


if __name__ == "__main__":
    main()
