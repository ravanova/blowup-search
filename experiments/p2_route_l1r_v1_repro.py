#!/usr/bin/env python3
"""Route-L1R (leg 110) -- the L1 death-certificate reproduction audit.

`L1 is dead in both realizations` is the most load-bearing negative in this repository:
it gates the plan of record's sequence, it is the stated lift condition on stage V's ban,
and it is the framing premise of NG.  Leg 60/PQ proved that this project's banked negatives
can partially fail reproduction from their own stored data (3 of 114 quoted numbers).  This
leg runs that same discipline against the two L1 death records.

WHAT THIS SCRIPT DOES NOT DO
----------------------------
It imports no solver module, opens no scenario, and re-runs no measurement.  It reads four
already-banked curated JSONs and nothing else:

    writeup/data/p2_route_l1_v2_spectral.json     leg 51 -- the coefficient-basis death
    writeup/data/p2_route_l1_v1_interval.json     leg 46 -- step one, for the cross-quotes
    writeup/data/p2_route_tn_v1_consistency.json  leg 56 -- the collocation-basis death
    writeup/data/p2_route_mm_v1_shape.json        leg 54 -- the lane-closing headline
    writeup/data/leg_54_verify_headline.json      VER-A  -- the verifier's own record

THE TOLERANCE RULE, FIXED BEFORE THE COMPARISON (inherited verbatim from leg 60)
--------------------------------------------------------------------------------
Every quoted value is passed in as *the string that appears in the document*, and the
tolerance is derived from that string: HALF A UNIT IN ITS OWN LAST PRINTED DIGIT.  A
document that writes `1.28` claims three significant figures, so the check accepts exactly
what rounds to `1.28`.  There is no global relative tolerance anywhere in this file, which
is what stops the check from being tuned until it passes.

Rows are of two kinds, declared per row and never re-labelled after seeing the result:

  STRICT  one printed number against one stored quantity.  These decide the gate.
  RANGE   one printed number asserted to hold across a SET of stored values ("flat at X
          across the whole range", "floors at ~X").  Reported with magnitudes alongside,
          because a range claim failing at one end is a different defect from a wrong
          number, and lesson 75 says not to merge them.

Wherever a stored field is itself a derived quantity (a divergence exponent, a per-mode
growth factor, an order per doubling, a ratio, an extrapolated n), this script RE-DERIVES
it from the underlying ladder rather than reading the field, and then checks the re-derived
value against the stored field as its own separate row -- so the load-bearing numbers are
genuinely reproduced, not transcribed twice.

Usage:  python experiments/p2_route_l1r_v1_repro.py
Writes: writeup/data/p2_route_l1r_v1_repro.json
"""

from __future__ import annotations

import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data")
OUT = os.path.join(DATA, "p2_route_l1r_v1_repro.json")


# --------------------------------------------------------------------------------------
# the tolerance rule
# --------------------------------------------------------------------------------------

_NUM = re.compile(r"^\s*[~≈xX×+]*\s*(-?)(\d+)(?:\.(\d+))?(?:[eE]([+-]?\d+))?\s*$")


def parse_quoted(text: str):
    """Return (value, half_ulp) for the string exactly as the document prints it.

    The half-ulp is half a unit in the LAST PRINTED DIGIT of the mantissa, scaled by the
    printed exponent.  Thousands separators are stripped; a leading tilde, `x` or `×` is
    a multiplier/approximation marker, not part of the number.
    """
    cleaned = text.replace(",", "").replace("−", "-").replace(" ", "")
    m = _NUM.match(cleaned)
    if not m:
        raise ValueError("cannot parse quoted string %r" % text)
    sign, whole, frac, exp = m.group(1), m.group(2), m.group(3) or "", m.group(4)
    exp = int(exp) if exp is not None else 0
    value = float("%s%s.%s0e%d" % (sign, whole, frac, exp))
    half_ulp = 0.5 * (10.0 ** (-len(frac))) * (10.0 ** exp)
    return value, half_ulp


class Ledger:
    def __init__(self):
        self.rows = []

    def add(self, doc, section, label, quoted, reproduced, kind="STRICT", note=""):
        qval, half_ulp = parse_quoted(quoted)
        delta = abs(reproduced - qval)
        half_ulps = delta / half_ulp if half_ulp > 0 else float("inf")
        ok = delta <= half_ulp * (1.0 + 1e-12)
        self.rows.append(
            {
                "doc": doc,
                "section": section,
                "label": label,
                "kind": kind,
                "quoted": quoted,
                "quoted_value": qval,
                "reproduced": reproduced,
                "abs_delta": delta,
                "rel_delta": delta / abs(qval) if qval != 0 else (0.0 if delta == 0 else float("inf")),
                "half_ulp": half_ulp,
                "half_ulps_out": half_ulps,
                "pass": bool(ok),
                "note": note,
            }
        )
        return ok

    def counts(self, kind=None):
        rows = [r for r in self.rows if kind is None or r["kind"] == kind]
        return len(rows), sum(1 for r in rows if r["pass"])


# --------------------------------------------------------------------------------------
# re-derivation helpers -- these recompute, they do not read the stored derived field
# --------------------------------------------------------------------------------------


def loglog_slope(xs, ys):
    """Least-squares slope of log(y) against log(x): the divergence exponent."""
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    den = sum((a - mx) ** 2 for a in lx)
    return num / den


def per_mode_growth(ms, norms):
    """Growth factor per neglected mode, from the two ends of the ladder."""
    return (norms[-1] / norms[0]) ** (1.0 / (ms[-1] - ms[0]))


def order_per_doubling(a, b):
    """Convergence order from consecutive rungs at a 2x refinement."""
    return math.log(a / b) / math.log(2.0)


def n_required(n0, defect, target, order):
    """Refinement needed to bring `defect` down to `target` at the measured `order`."""
    return n0 * (defect / target) ** (1.0 / order)


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


# --------------------------------------------------------------------------------------
# ARM A -- the coefficient-basis death (leg 51's measurements; the lane closed at leg 54)
# --------------------------------------------------------------------------------------


def arm_a(led, spectral, interval):
    T = "TECHNICAL_P2_ROUTEL1_V2.md"
    B = "BLOG_P2_ROUTEL1_V2.md"
    N = "PHASE2_P2_NOTES.md §40"

    s1 = spectral["S1_exactness"]
    s2 = spectral["S2_exact_residual"]
    s3 = spectral["S3_terms"]
    s4 = spectral["S4_control"]
    s5 = spectral["S5_exact_check"]
    s6 = spectral["S6_window"]

    # --- §2 the exactness audit -------------------------------------------------------
    worst_identity = max(
        max(r["defect_cos"], r["defect_sin"]) for r in s1["identity"]
    )
    led.add(T, "2", "w^k vs cos+i sin, worst defect over k=1,2,3,5,9", "3.5e-15", worst_identity)
    led.add(T, "2", "velocity closed-form defect c_k = (-1)^k k", "0.0",
            s1["velocity_defect_vs_closed_form"])
    # the closed form itself, re-derived rather than trusted:
    ck_defect = max(
        abs(c - ((-1) ** k) * k) for k, c in enumerate(s1["velocity_constants"], start=1)
    )
    led.add(T, "2", "max |c_k - (-1)^k k| over the stored constants", "0.0", ck_defect)

    ladder = s1["numeric_ladder"]
    slope = loglog_slope([r["n"] for r in ladder], [r["max_defect"] for r in ladder])
    led.add(T, "2", "line_hilbert.py cross-check convergence exponent (re-fit)", "-1.00", slope)
    led.add(T, "2", "  same, re-fit vs stored numeric_convergence_exponent", "-1.0022246810",
            s1["numeric_convergence_exponent"],
            note="re-fit %.10f" % slope)

    # --- §3 the anchor's residual -----------------------------------------------------
    led.add(T, "3", "modes in the residual of the 8-mode profile", "18", float(s2["modes"]))
    led.add(T, "3", "max |residual| in rational arithmetic", "0.0", s2["max_abs"])
    led.add(T, "3", "negative control: modes made nonzero by perturbing b_4", "5",
            float(s2["perturbed_nonzero_modes"]))

    # --- §4 the four terms at K = 256 -------------------------------------------------
    fb = {(r["K"], r["class"], r["param"]): r for r in s3["finite_block"]}
    for cls, par, z1, z2, rmax in (
        ("flat", 0.0, "1.18e-08", "9.80e+03", "1.02e-04"),
        ("algebraic", 1.0, "1.44e-10", "79.5", "1.26e-02"),
        ("geometric", 1.1, "1.19e-05", "1.50e+08", "6.65e-09"),
    ):
        row = fb[(256, cls, par)]
        tag = "%s %s" % (cls, par)
        led.add(T, "4", "K=256 %s Z1(finite)" % tag, z1, row["Z1_finite"])
        led.add(T, "4", "K=256 %s Z2" % tag, z2, row["Z2"])
        led.add(T, "4", "K=256 %s r_max" % tag, rmax, row["r_max"])
        led.add(T, "4", "K=256 %s Y0" % tag, "0", row["Y0"])

    # --- §4 the tail table, and the exponents re-fitted from the ladders --------------
    tail = {(r["class"], r["param"]): r for r in s3["tail"]}
    tail_quotes = [
        ("flat", 0.0, "1.02", "16.3", "1.28", "1.0029"),
        ("algebraic", 0.394, "0.876", "7.66", "1.00", "1.0023"),
        ("algebraic", 1.0, "0.706", "2.87", "0.64", "1.0015"),
        ("geometric", 1.05, "2.51", "5.75e+18", None, "1.045"),
        ("geometric", 1.2, "2.74e+03", "3.60e+77", None, "1.195"),
    ]
    for cls, par, at128, at1088, expo, pm in tail_quotes:
        row = tail[(cls, par)]
        tag = "%s %s" % (cls, par)
        led.add(T, "4", "tail norm %s at M=128" % tag, at128, row["norm"][0])
        led.add(T, "4", "tail norm %s at M=1088" % tag, at1088, row["norm"][-1])
        redone_pm = per_mode_growth(row["M"], row["norm"])
        led.add(T, "4", "per-mode growth %s (re-derived from the ladder)" % tag, pm, redone_pm)
        if expo is not None:
            redone = loglog_slope(row["M"], row["norm"])
            led.add(T, "4", "divergence exponent %s (re-fit log-log)" % tag, expo, redone)
            led.add(T, "4", "  same, re-fit vs stored divergence_exponent %s" % tag,
                    "%.12f" % row["divergence_exponent"], redone)

    # "The geometric growth factor IS nu, to three digits, in both cases" -- the claim,
    # checked at the precision the claim itself names.  The measured growth is compared to
    # nu printed to three digits, so the tolerance is half a unit in that third digit.
    for par in (1.05, 1.2):
        row = tail[("geometric", par)]
        g = per_mode_growth(row["M"], row["norm"])
        led.add(T, "4", "per-mode growth vs nu=%s, under 'the growth factor IS nu, to "
                        "three digits'" % par,
                "%.3f" % par, g,
                note=("three significant figures: growth %.3g vs nu %.3g; three decimal "
                      "places: growth %.3f vs nu %.3f; growth is %.3f%% BELOW nu"
                      % (g, par, g, par, 100.0 * (par - g) / par)))

    # --- §5 the structural fact -------------------------------------------------------
    led.add(T, "5", "max |diag(T_tail)|", "0.0", s3["tail_diagonal_max_abs"])
    led.add(T, "5", "homogeneous-mode decay exponent h_m ~ m^e", "-2.007",
            s3["homogeneous_mode_exponent"])
    led.add(B, "-", "same decay exponent, as the blog prints it", "-2.007",
            s3["homogeneous_mode_exponent"])

    # --- §6 the sawtooth --------------------------------------------------------------
    saw_defect = max(
        abs(c - 1.0 / m) for m, c in enumerate(s3["sawtooth_first_coefficients"], start=1)
    )
    led.add(T, "6", "sawtooth coefficients are exactly 1/m (max defect)", "0.0", saw_defect)

    # --- §7 the positive control ------------------------------------------------------
    ctl = {(r["mu"], r["class"], r["param"]): r for r in s4["tail"]}
    for mu, cls, par, expo in (
        (0.0, "flat", 0.0, "1.28"),
        (0.1, "flat", 0.0, "0.000"),
        (0.5, "flat", 0.0, "0.000"),
        (0.0, "algebraic", 1.0, "0.64"),
        (0.1, "algebraic", 1.0, "0.000"),
        (0.5, "algebraic", 1.0, "0.000"),
        (0.5, "geometric", 1.2, "0.000"),
    ):
        row = ctl[(mu, cls, par)]
        led.add(T, "7", "control mu=%s %s %s divergence exponent (re-fit)" % (mu, cls, par),
                expo, loglog_slope(row["M"], row["norm"]))
    for mu, expo in ((0.0, "1.195"), (0.1, "1.081")):
        row = ctl[(mu, "geometric", 1.2)]
        led.add(T, "7", "control mu=%s geometric 1.2 per-mode growth (re-derived)" % mu,
                expo, per_mode_growth(row["M"], row["norm"]))
    mins = s4["min_mu_that_saturates"]
    led.add(T, "7", "min mu that saturates: flat", "0.1", mins["flat_0.0"])
    led.add(T, "7", "min mu that saturates: algebraic s=1", "0.1", mins["algebraic_1.0"])
    led.add(T, "7", "min mu that saturates: geometric nu=1.2", "0.5", mins["geometric_1.2"])
    led.add(T, "7", "geometric needs N times more dissipation", "5",
            mins["geometric_1.2"] / mins["flat_0.0"])

    # --- §8 float against exact -------------------------------------------------------
    rows5 = {r["K"]: r for r in s5["rows"]}
    worst = max(r["rel_gap"] for r in s5["rows"])
    led.add(T, "8", "max relative gap exact vs float (re-derived as the max over rows)",
            "8.8e-15", worst)
    led.add(T, "8", "  same, re-derived vs stored max_rel_gap", "%.12e" % s5["max_rel_gap"], worst)
    led.add(T, "8", "exact weighted inverse norm at K=96", "62.0005", rows5[96]["exact"])
    led.add(T, "8", "exact weighted inverse norm at K=128", "609.17", rows5[128]["exact"])

    # --- §9 the window ----------------------------------------------------------------
    curve = {round(r["s"], 3): r for r in s6["curve"]}
    for s_val, quoted in ((0.0, "1.28"), (0.394, "1.00"), (1.0, "0.64"), (2.0, "1.27")):
        row = curve[s_val]
        redone = loglog_slope(spectral["S3_terms"]["tail"][0]["M"], row["norm"])
        led.add(T, "9", "divergence exponent at s=%s (re-fit log-log)" % s_val, quoted, redone)
        led.add(N, "L1v2-4", "same exponent at s=%s as the notes print it" % s_val, quoted, redone)

    # the U-curve minimum, re-derived by argmin rather than read
    best_s, best_row = min(curve.items(), key=lambda kv: kv[1]["divergence_exponent"])
    best_refit = loglog_slope(spectral["S3_terms"]["tail"][0]["M"], best_row["norm"])
    led.add(T, "9", "argmin of the U-curve", "1.00", best_s)
    led.add(N, "L1v2-4", "divergence-curve minimum (re-fit at the argmin)", "+0.639", best_refit)
    led.add(N, "L1v2-4", "  same, re-fit vs stored best_divergence_exponent",
            "%.12f" % s6["window"]["best_divergence_exponent"], best_refit)

    win = s6["window"]
    led.add(T, "9", "target far-field exponent alpha", "0.394", win["alpha"])
    led.add(T, "9", "object-side ceiling s_max", "0.394", win["s_max_object"])
    led.add(T, "9", "operator-side optimum s", "1.00", win["s_operator"])
    gap_rederived = win["s_operator"] - win["s_max_object"]
    led.add(T, "9", "window gap in exponent units (re-derived s_op - s_obj)", "0.606", gap_rederived)
    led.add(B, "-", "same gap as the blog prints it", "0.606", gap_rederived)
    led.add(N, "L1v2-4", "same gap as the notes print it", "0.606", gap_rederived)
    led.add(T, "9", "exponent at the object's own boundary", "1.00",
            win["divergence_at_object_boundary"])
    led.add(N, "L1v2-4", "target coefficient exponent k^-1-alpha", "-1.394",
            win["coefficient_exponent_of_target"])

    # --- §1 the cross-quoted leg-46 numbers -------------------------------------------
    n201 = [r for r in interval["L1_2_ladder"] if r["n"] == 201][0]
    led.add(T, "1", "grid certificate Y0 at the anchor (leg 46, n=201)", "5.17e-12",
            n201["interval"]["Y0"])

    # --- BLOG-only numbers ------------------------------------------------------------
    g12 = tail[("geometric", 1.2)]
    led.add(B, "-", "geometric nu=1.2 constant at 128 modes", "2.7e+03", g12["norm"][0])
    led.add(B, "-", "geometric nu=1.2 constant at 1088 modes", "3.6e+77", g12["norm"][-1])
    led.add(B, "-", "best-case algebraic growth M^0.64", "0.64",
            loglog_slope(g12["M"], tail[("algebraic", 1.0)]["norm"]))

    # --- RANGE rows: printed numbers asserted to hold across a SET --------------------
    # "Every weight class saturates immediately ... the divergence exponent drops to 0.000
    #  and stays there" (BLOG).  Checked against every class at mu = 0.1.
    for cls, par in (("flat", 0.0), ("algebraic", 1.0), ("geometric", 1.2)):
        row = ctl[(0.1, cls, par)]
        led.add(B, "control", "mu=0.1 %s %s exponent, under 'every class drops to 0.000'"
                % (cls, par), "0.000", loglog_slope(row["M"], row["norm"]), kind="RANGE")
    # "Agreement: 15 digits" (BLOG) for a max relative gap of 8.77e-15
    led.add(B, "-", "exact-vs-float agreement in digits (-log10 of the max rel gap)",
            "15", -math.log10(worst), kind="RANGE")
    # "defect 0.0, k = 1..16" (TECHNICAL §2) -- the stored ladder's length
    led.add(T, "2", "number of velocity constants stored, under 'k = 1..16'", "16",
            float(len(s1["velocity_constants"])), kind="RANGE")


# --------------------------------------------------------------------------------------
# ARM B -- the collocation-basis death (leg 56)
# --------------------------------------------------------------------------------------


def arm_b(led, tn):
    T = "TECHNICAL_P2_ROUTETN_V1.md"
    B = "BLOG_P2_ROUTETN_V1.md"
    N = "PHASE2_P2_NOTES.md Route-TN v1"

    rungs = {r["certificate"]["n"]: r for r in tn["rungs"]}
    r801 = rungs[801]
    cert801 = r801["certificate"]
    v = tn["verdict"]
    ref = tn["leg46_reference_as_stored"]
    rates = tn["rates"]
    attr = tn["H_attribution"]

    # --- §3 the endpoint-zeroing evidence table ---------------------------------------
    chk = tn["validation"]["H_is_endpoint_zeroed_check"]
    led.add(T, "3", "node-1 abscissa at n=201", "-687.943", chk["X"])
    led.add(T, "3", "H_disc f", "-1.8584719686e-03", chk["H_disc"])
    led.add(T, "3", "H(Pi0_n f) by PV quadrature", "-1.8584719686e-03",
            chk["H_of_endpoint_zeroed_interpolant_quadrature"])
    led.add(T, "3", "|H_disc - H(Pi0_n f)|", "2.61e-15", chk["abs_diff_H_disc_vs_endpoint_zeroed"])
    led.add(T, "3", "H(Pi_n f) by PV quadrature", "-1.4880639571e-03",
            chk["H_of_full_interpolant_quadrature"])
    led.add(T, "3", "|H_disc - H(Pi_n f)|", "3.704e-04", chk["abs_diff_H_disc_vs_full"])
    led.add(T, "3", "full-interpolant matrix vs quadrature", "4.34e-19",
            chk["abs_diff_full_matrix_vs_quadrature"])
    led.add(T, "3", "H_M f, the reference", "-1.4885580e-03", chk["H_M_reference"])
    led.add(B, "-", "same agreement as the blog prints it", "2.6e-15",
            chk["abs_diff_H_disc_vs_endpoint_zeroed"])
    led.add(B, "-", "same difference as the blog prints it", "3.7e-04",
            chk["abs_diff_H_disc_vs_full"])

    # --- §4 node bookkeeping ----------------------------------------------------------
    led.add(T, "4", "interior nodes at n=801", "799", float(r801["defects"]["odd"]["interior_nodes"]))
    led.add(T, "4", "excluded endpoint nodes", "2", float(r801["defects"]["odd"]["excluded_nodes"]))
    led.add(T, "7", "X_max, frozen at every rung", "745.239", cert801["X_max"])
    led.add(T, "7", "weight exponent p = P_STAR", "0.39", cert801["p_star"])

    # --- §5 the rigorous evaluation primitives ----------------------------------------
    led.add(T, "5", "ilog max enclosure width", "3.55e-14", tn["validation"]["ilog_max_width"])
    led.add(T, "5", "iatan_small max enclosure width", "1.48e-14",
            tn["validation"]["iatan_max_width"])

    # --- §6 the comparison quantity, RE-DERIVED (lesson 85, and the leg's own claim) ---
    led.add(T, "6", "leg 46/50 budget at n=801, as stored", "3.554656e-10", ref["budget"])
    led.add(T, "6", "leg 46/50 ||A||_w at n=801, as stored", "15417.7", ref["A_norm"])
    tau_rederived = cert801["budget"] / cert801["A_norm"]
    led.add(T, "6", "tau = budget / ||A||_w  (RE-DERIVED, not read)", "2.306e-14", tau_rederived)
    led.add(T, "7", "  same tau at the ladder's precision", "2.3056e-14", tau_rederived)
    led.add(T, "6", "  re-derived tau vs stored tau_admissible_defect",
            "%.12e" % cert801["tau_admissible_defect"], tau_rederived)
    led.add(T, "6", "Y0 as this leg re-derives it at n=801", "9.97e-12", cert801["Y0"])
    led.add(T, "6", "Y0 as leg 46 stored it at n=801", "7.35e-12", ref["Y0"])
    led.add(B, "-", "budget as the blog prints it", "3.5547e-10", ref["budget"])
    led.add(B, "-", "||A||_w as the blog prints it", "1.5418e+04", ref["A_norm"])
    led.add(B, "-", "Z2 at n=801", "1.4e+09", cert801["Z2"])

    # --- §7 the ladder ----------------------------------------------------------------
    quotes = {
        201: ("1.1220e-04", "4.7287e-03", "1.9042e-02", "2.3008e-13"),
        401: ("6.8724e-06", "4.7131e-03", "2.2582e-02", "3.1728e-14"),
        801: ("4.2738e-07", "4.7041e-03", "2.6260e-02", "2.3056e-14"),
    }
    for n, (qd, qh, qt, qtau) in quotes.items():
        od = rungs[n]["defects"]["odd"]
        led.add(T, "7", "n=%d D defect" % n, qd, od["defect_D_abs"])
        led.add(T, "7", "n=%d H defect" % n, qh, od["defect_H_abs"])
        led.add(T, "7", "n=%d far-field truncation" % n, qt, od["truncation_H_abs"])
        led.add(T, "7", "n=%d tau (re-derived from that rung)" % n, qtau,
                rungs[n]["certificate"]["budget"] / rungs[n]["certificate"]["A_norm"])

    # orders, re-derived from consecutive rungs rather than read
    dD = rates["defect_D_odd"]
    dH = rates["defect_H_odd"]
    tr = rates["truncation_odd"]
    led.add(T, "7", "D order 201->401 (re-derived)", "4.03", order_per_doubling(dD[0], dD[1]))
    led.add(T, "7", "D order 401->801 (re-derived)", "4.01", order_per_doubling(dD[1], dD[2]))
    led.add(T, "7", "H order 201->401 (re-derived)", "0.00", order_per_doubling(dH[0], dH[1]))
    led.add(T, "7", "H order 401->801 (re-derived)", "0.00", order_per_doubling(dH[1], dH[2]))
    led.add(B, "-", "truncation order 401->801 (re-derived)", "-0.22",
            order_per_doubling(tr[1], tr[2]))
    led.add(T, "7", "  D order re-derived vs stored rate field",
            "%.12f" % rates["defect_D_odd_rate"][1]["order"], order_per_doubling(dD[1], dD[2]))

    # the headline ratios, re-derived as defect / tau
    led.add(T, "7", "D defect over tau at n=801 (RE-DERIVED)", "1.854e+07",
            r801["defects"]["odd"]["defect_D_abs"] / tau_rederived)
    led.add(T, "7", "H defect over tau at n=801 (RE-DERIVED)", "2.040e+11",
            r801["defects"]["odd"]["defect_H_abs"] / tau_rederived)
    led.add(T, "7", "far-field truncation over tau at n=801 (RE-DERIVED)", "1.139e+12",
            r801["defects"]["odd"]["truncation_H_abs"] / tau_rederived)
    led.add(T, "11", "gate answer magnitude: H exceeds tau by", "2.04e+11",
            r801["defects"]["odd"]["defect_H_abs"] / tau_rederived)
    led.add(T, "11", "gate answer magnitude: D exceeds tau by", "1.85e+07",
            r801["defects"]["odd"]["defect_D_abs"] / tau_rederived)
    led.add(N, "-", "notes: derivative excess", "1.85e7",
            r801["defects"]["odd"]["defect_D_abs"] / tau_rederived)
    led.add(N, "-", "notes: Hilbert excess", "2.04e11",
            r801["defects"]["odd"]["defect_H_abs"] / tau_rederived)
    led.add(T, "11", "gate answer magnitude: H defect at n=801", "4.704e-03", v["defect_H_at_801"])
    led.add(T, "11", "gate answer magnitude: D defect at n=801", "4.274e-07", v["defect_D_at_801"])

    # H does not converge: the total factor over a 4x refinement, re-derived
    led.add(T, "7", "H total factor over the 4x refinement (re-derived)", "1.0052", dH[0] / dH[2])
    led.add(B, "-", "same factor as the blog prints it", "1.005", dH[0] / dH[2])

    # the extrapolations, re-derived from the measured orders
    nreq_D = n_required(801, r801["defects"]["odd"]["defect_D_abs"], tau_rederived,
                        rates["defect_D_odd_rate"][1]["order"])
    led.add(T, "7", "n required, derivative side (RE-DERIVED at measured order)", "52163", nreq_D)
    led.add(T, "7", "  same, re-derived vs stored n_required",
            "%.6f" % tn["D_only_extrapolation"]["n_required"], nreq_D)
    led.add(T, "7", "N = 2n+3 at that n", "104329", 2 * 52163 + 3)
    led.add(B, "-", "n required, as the blog rounds it", "52000", round(nreq_D, -3))

    # --- §7.1 the attribution ----------------------------------------------------------
    ez = attr["defect_H_endpoint_zeroing"]
    ip = attr["defect_H_interpolation"]
    for i, n in enumerate((201, 401, 801)):
        led.add(T, "7.1", "n=%d endpoint-zeroing term" % n,
                ["4.7351e-03", "4.7148e-03", "4.7046e-03"][i], ez[i])
        led.add(T, "7.1", "n=%d true-interpolation term" % n,
                ["6.3159e-06", "1.7022e-06", "4.4181e-07"][i], ip[i])
    led.add(T, "7.1", "endpoint-zeroing order 401->801 (re-derived)", "0.00",
            order_per_doubling(ez[1], ez[2]))
    led.add(T, "7.1", "endpoint-zeroing order 201->401 (re-derived)", "0.01",
            order_per_doubling(ez[0], ez[1]))
    led.add(T, "7.1", "interpolation order 201->401 (re-derived)", "1.89",
            order_per_doubling(ip[0], ip[1]))
    led.add(T, "7.1", "interpolation order 401->801 (re-derived)", "1.95",
            order_per_doubling(ip[1], ip[2]))
    share = ez[2] / attr["defect_H_total"][2]
    led.add(T, "7.1", "endpoint-zeroing share at n=801 (RE-DERIVED)", "1.00009", share)
    nreq_I = n_required(801, ip[2], tau_rederived, order_per_doubling(ip[1], ip[2]))
    led.add(T, "7.1", "n required, interpolation only (RE-DERIVED)", "4.43e+06", nreq_I)
    led.add(T, "7.1", "  same, re-derived vs stored n_required_interpolation_only",
            "%.6f" % attr["n_required_interpolation_only"], nreq_I)

    # --- §7 the scale curve ------------------------------------------------------------
    sc = {r["a"]: r for r in tn["scale_curve"]}
    led.add(T, "7", "scale curve a=0.125 D defect", "1.804e-03", sc[0.125]["defect_D_abs"])
    led.add(T, "7", "scale curve a=0.25 D defect", "2.752e-05", sc[0.25]["defect_D_abs"])
    led.add(T, "7", "scale curve a=0.5 D defect", "4.274e-07", sc[0.5]["defect_D_abs"])
    for a in (1.0, 2.0, 8.0, 32.0):
        led.add(T, "7", "scale curve a=%s D defect, under 'floors at ~7.13e-08'" % a,
                "7.13e-08", sc[a]["defect_D_abs"], kind="RANGE")
        led.add(T, "7", "scale curve a=%s H defect, under 'flat at 4.704e-03'" % a,
                "4.704e-03", sc[a]["defect_H_abs"], kind="RANGE")
    for a in (0.125, 0.25, 0.5):
        led.add(T, "7", "scale curve a=%s H defect, under 'flat at 4.704e-03'" % a,
                "4.704e-03", sc[a]["defect_H_abs"], kind="RANGE")

    # --- §8 the mechanism ablation -----------------------------------------------------
    ab = {r["n"]: r for r in tn["mechanism_ablation"]}
    led.add(T, "8", "predicted collapse M/a", "1490.5", ab[801]["predicted_collapse_M_over_a"])
    led.add(B, "-", "predicted collapse, as the blog rounds it", "1490",
            round(ab[801]["predicted_collapse_M_over_a"]))
    for n, qc, qd in ((201, "1421", "1.12"), (401, "1516", "1.11"), (801, "1503", "1.11")):
        led.add(T, "8", "n=%d H collapse odd/even (RE-DERIVED)" % n, qc,
                ab[n]["defect_H_odd"] / ab[n]["defect_H_even"])
        led.add(T, "8", "n=%d D change odd/even (RE-DERIVED)" % n, qd,
                ab[n]["defect_D_odd"] / ab[n]["defect_D_even"])
    led.add(T, "8", "even-family H defect at n=201", "3.33e-06", ab[201]["defect_H_even"])
    led.add(T, "8", "even-family H defect at n=801", "3.13e-06", ab[801]["defect_H_even"])
    led.add(B, "-", "even-family H defect at n=801, blog precision", "3.130e-06",
            ab[801]["defect_H_even"])
    led.add(B, "-", "even-family D defect at n=801, blog precision", "3.866e-07",
            ab[801]["defect_D_even"])
    collapse_vs_pred = abs(
        ab[801]["defect_H_collapse"] / ab[801]["predicted_collapse_M_over_a"] - 1.0
    )
    led.add(T, "8", "|collapse/prediction - 1| at n=801, under 'to within 1%'", "0.01",
            collapse_vs_pred, kind="RANGE")

    # --- §9 the widths (discipline 86) -------------------------------------------------
    led.add(T, "9", "enclosure width/value, D at n=801", "6.34e-08",
            r801["defects"]["odd"]["width_frac_D"])
    led.add(T, "9", "enclosure width/value, H at n=801", "1.15e-13",
            r801["defects"]["odd"]["width_frac_H"])
    led.add(T, "9", "worst quadrature disagreement", "4.44e-15",
            tn["validation"]["quadrature_worst_abs_disagreement"])
    led.add(T, "9", "quadrature cross-check cases", "12",
            float(tn["validation"]["quadrature_cases"]))


# --------------------------------------------------------------------------------------
# ARM C -- the lane-closing headline (leg 54), and the verifier's own record
# --------------------------------------------------------------------------------------


def arm_c(led, mm, ver):
    N = "PHASE2_P2_NOTES.md Route-MM v1"
    C = "CONTINUATION_PROMPT.md"

    best = mm["MM2_best_admissible"]
    base = mm["MM2_block_diagonal_baseline"]
    led.add(N, "-", "best admissible Z1 over every shape/class/gauge/split", "8.9591", best["Z1"])
    led.add(N, "-", "block-diagonal baseline Z1", "10.4584", base["Z1"])
    improvement = base["Z1"] / best["Z1"]
    led.add(N, "-", "improvement factor (RE-DERIVED baseline/best)", "1.167", improvement)
    led.add(N, "-", "  re-derived vs stored MM2_improvement_over_block_diagonal",
            "%.12f" % mm["MM2_improvement_over_block_diagonal"], improvement)
    led.add(N, "-", "K at the best admissible point", "2", float(best["K"]))
    led.add(N, "-", "weight param at the best admissible point", "0.3", best["param"])
    led.add(C, "-", "the floor as the continuation prompt quotes it", "8.9591", best["Z1"])
    led.add(N, "-", "MM-1 restriction: smallest K with rhs>1, flat", "6",
            float(mm["MM1_smallest_K_with_rhs_above_one"]["flat"]))
    led.add(N, "-", "MM-1 restriction: smallest K with rhs>1, algebraic", "4",
            float(mm["MM1_smallest_K_with_rhs_above_one"]["algebraic"]))
    led.add(N, "-", "MM-1 max deviation of the ratio from one", "1.9e-15",
            mm["MM1_max_ratio_deviation_from_one"])

    # the "more than 8x was needed" claim, re-derived: to reach Z1 < 1 from the best point
    led.add(N, "-", "further improvement needed from the best point (RE-DERIVED)", "8.9591",
            best["Z1"] / 1.0)

    # VER-A's own re-measurement of leg 53's headline, which leg 54 built on
    led.add("leg_54_verify_headline.json", "V2", "leg 53's Z1[Gamma<-tail] min over its sweep",
            "0.9961", ver["V2_tail_from_gamma"]["min_leg53_sweep"]["Z1_tail_Gamma"])
    led.add(N, "-", "leg 54 reproduces leg 53's Z1[Gamma->tail] bit-for-bit",
            "43.15129110858924", mm["MM2_instrument_check_vs_leg53"]["leg54_Z1_Gamma_tail"])
    led.add(N, "-", "  and leg 53's own stored value", "43.15129110858924",
            mm["MM2_instrument_check_vs_leg53"]["leg53_Z1_Gamma_tail"])


# --------------------------------------------------------------------------------------


def main():
    spectral = load("p2_route_l1_v2_spectral.json")
    interval = load("p2_route_l1_v1_interval.json")
    tn = load("p2_route_tn_v1_consistency.json")
    mm = load("p2_route_mm_v1_shape.json")
    ver = load("leg_54_verify_headline.json")

    led = Ledger()
    arm_a(led, spectral, interval)
    n_a = len(led.rows)
    arm_b(led, tn)
    n_b = len(led.rows) - n_a
    arm_c(led, mm, ver)
    n_c = len(led.rows) - n_a - n_b

    strict_total, strict_pass = led.counts("STRICT")
    range_total, range_pass = led.counts("RANGE")
    total, passed = led.counts()

    width = max(len(r["label"]) for r in led.rows)
    print("=" * 100)
    print("ROUTE-L1R -- the L1 death-certificate reproduction audit (leg 110)")
    print("tolerance: half a unit in the last printed digit of the quoted string. No global rtol.")
    print("=" * 100)
    cur = None
    for r in led.rows:
        key = (r["doc"], r["kind"])
        if key != cur:
            cur = key
            print("\n--- %s   [%s rows]" % (r["doc"], r["kind"]))
        flag = "PASS" if r["pass"] else "FAIL"
        print("  %s  %-*s  quoted %-22s reproduced %-24s  %7.2f half-ulps"
              % (flag, width, r["label"], r["quoted"], "%.12g" % r["reproduced"],
                 r["half_ulps_out"]))

    print("\n" + "=" * 100)
    print("ARM A (coefficient basis, leg 51/54 lane): %d rows" % n_a)
    print("ARM B (collocation basis, leg 56):         %d rows" % n_b)
    print("ARM C (lane-closing headline, leg 54):     %d rows" % n_c)
    print("STRICT rows: %d / %d reproduce" % (strict_pass, strict_total))
    print("RANGE  rows: %d / %d reproduce" % (range_pass, range_total))
    print("TOTAL:       %d / %d" % (passed, total))
    fails = [r for r in led.rows if not r["pass"]]
    if fails:
        print("\nDISCREPANCIES:")
        for r in fails:
            print("  [%s] %s :: %s\n      %s"
                  % (r["kind"], r["doc"], r["section"], r["label"]))
            print("      quoted %s   reproduced %.12g   abs %.6g   rel %.6g   %.2f half-ulps"
                  % (r["quoted"], r["reproduced"], r["abs_delta"], r["rel_delta"],
                     r["half_ulps_out"]))
    gate = "yes" if strict_pass == strict_total else "no"
    print("\nGATE (verbatim): does every quoted headline number in the two L1 death records")
    print("reproduce exactly from the banked JSON data alone?  ->  %s" % gate.upper())

    out = {
        "route": "L1R",
        "version": "v1",
        "leg": 110,
        "question": ("Does every quoted headline number in the two L1 death records "
                     "(coefficient basis, leg 51/54; collocation basis, leg 56) reproduce "
                     "exactly from the banked writeup/data JSONs alone?"),
        "method": {
            "recomputes_nothing": True,
            "solver_modules_imported": [],
            "sources_read_only": [
                "writeup/data/p2_route_l1_v2_spectral.json",
                "writeup/data/p2_route_l1_v1_interval.json",
                "writeup/data/p2_route_tn_v1_consistency.json",
                "writeup/data/p2_route_mm_v1_shape.json",
                "writeup/data/leg_54_verify_headline.json",
            ],
            "tolerance_rule": ("half a unit in the last printed digit of the string the "
                               "document prints; no global relative tolerance anywhere"),
            "row_kinds": {
                "STRICT": "one printed number against one stored quantity; decides the gate",
                "RANGE": ("one printed number asserted to hold across a SET of stored "
                          "values; reported separately, does not decide the gate"),
            },
            "derived_fields_refit_not_read": [
                "divergence exponents (log-log least squares over the M ladder)",
                "per-mode growth factors (from the ladder endpoints)",
                "convergence orders (log2 of consecutive-rung factors)",
                "tau = budget / ||A||_w",
                "defect / tau ratios",
                "endpoint-zeroing share",
                "extrapolated n at the measured order",
                "MM improvement = baseline / best",
            ],
        },
        "counts": {
            "arm_a_coefficient_basis": n_a,
            "arm_b_collocation_basis": n_b,
            "arm_c_lane_closing_headline": n_c,
            "strict_total": strict_total,
            "strict_pass": strict_pass,
            "range_total": range_total,
            "range_pass": range_pass,
            "total": total,
            "pass": passed,
        },
        "rows": led.rows,
        "discrepancies": fails,
        "gate": {
            "question": ("does every quoted headline number in the two L1 death records "
                         "reproduce exactly from the banked JSON data alone?"),
            "answer": gate,
            "decided_on": "STRICT rows only",
        },
        "ceiling": ("This audits the DOCUMENTS against the DATA. It does not re-measure "
                    "anything, and a reproduction result -- either way -- lifts no ban, "
                    "revives no lane, and changes no conclusion. A discrepancy found here "
                    "is a defect in a sentence, not evidence about L1."),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
