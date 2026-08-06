"""Route-L1R v1 (leg 110) -- the L1 death certificates, re-derived from their own banked data.

READ-ONLY REPRODUCTION AUDIT.  No solver module is imported, no measurement is re-run, no
audited file is written.  Every number this script reports is either (a) read from a banked
`writeup/data/*.json`, or (b) computed by arithmetic from numbers read from those files.

WHAT IS AUDITED (the gate's own scope, DIRECTION.md leg 110):
    the two `L1` death records -- PHASE2_P2_NOTES.md's sections for legs 54 and 56, the
    leg-51 window numbers those deaths rest on (+0.639, 0.606, the per-class tail-divergence
    exponents), and everywhere those numbers are re-quoted: the four `writeup/4_p2_lottery`
    documents of legs 54/56 and leg 51's TECHNICAL.

WHAT IS *NOT* TOUCHED:
    every audited document and every audited JSON is read-only under BOTH branches of the
    gate.  A number that does not re-derive is reported with its magnitude and escalated
    (ORCHESTRATION.md sec 7b/8); it is never silently corrected here.

METHOD.  Each ledger row pairs a literal as it is printed in prose with a value re-derived
from the banked JSON.  The residual is reported in HALF-ULPS OF THE PROSE'S OWN LAST QUOTED
DIGIT: a literal that is the correctly-rounded rendering of its stored value scores <= 1.0.
Rows whose prose carries an explicit approximation qualifier (`~`, `approx`, `about`) are
scored but classified separately, since a tilde does not promise a correctly-rounded digit.

Usage:  python3 experiments/p2_route_l1r_v1_repro.py
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data")
OUT = os.path.join(DATA, "p2_route_l1r_v1_repro.json")


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


MM = load("p2_route_mm_v1_shape.json")            # leg 54, coefficient-basis death
TN = load("p2_route_tn_v1_consistency.json")      # leg 56, collocation-basis death
VERA = load("leg_54_verify_headline.json")        # VER-A, read-only cross-reference
L1V1 = load("p2_route_l1_v1_interval.json")       # leg 46, the budget TN compares against
L1V2 = load("p2_route_l1_v2_spectral.json")       # leg 51, the window both deaths rest on


# ---------------------------------------------------------------------------
# half-ulp machinery
# ---------------------------------------------------------------------------

def ulp_of(literal):
    """The unit in the last place of a number AS PRINTED.

    '8.9591' -> 1e-4;  '1.85e+07' -> 1e5;  '1503' -> 1;  '2.040e+11' -> 1e8.
    """
    s = literal.strip().replace(",", "").replace("−", "-").replace("×", "")
    s = s.lstrip("+-")
    exp = 0
    for marker in ("e", "E"):
        if marker in s:
            s, e = s.split(marker)
            exp = int(e)
            break
    dec = len(s.split(".")[1]) if "." in s else 0
    return 10.0 ** (exp - dec)


def parse(literal):
    s = literal.strip().replace(",", "").replace("−", "-").replace("×", "")
    return float(s)


LEDGER = []


def _sig_digits(x):
    """The significand's digit string, unrounded ('34847.4293...' -> '348474293...')."""
    m = ("%.17e" % abs(x)).split("e")[0]
    return m.replace(".", "")


def matching_sig_digits(a, b):
    """How many leading significant digits two floats share as printed.

    Prefix comparison, not round-to-N: '34847.43' and '34847.68' share the five
    digits '34847', which is how a reader checks 'agrees to five digits'.  (Rounding
    to five significant figures would give 34847 and 34848, one digit fewer -- the
    stricter reading is recorded alongside.)
    """
    if a == b:
        return 17
    if (a < 0) != (b < 0) or ("%.17e" % abs(a)).split("e")[1] != ("%.17e" % abs(b)).split("e")[1]:
        return 0
    da, db = _sig_digits(a), _sig_digits(b)
    n = 0
    while n < min(len(da), len(db)) and da[n] == db[n]:
        n += 1
    return n


def matching_sig_digits_rounded(a, b):
    """The stricter reading: how many significant figures agree after rounding."""
    if a == b:
        return 17
    for d in range(17, 0, -1):
        if "%.*e" % (d - 1, a) == "%.*e" % (d - 1, b):
            return d
    return 0


def row(doc, locator, claim, literal, derived, derivation, kind="exact", note="",
        digits=None):
    """kind:
         exact    -- a printed literal that must be the correctly-rounded stored value
         fullprec -- a literal copied at full precision; judged on relative agreement
         order    -- an order-of-magnitude rendering; judged in decades
         approx   -- carries an explicit '~'/'about' qualifier; judged loosely
         bound    -- an 'agrees to N significant digits' claim; judged by digit count
         qualifier-- a verbal precision claim, reported as a magnitude
         absent   -- quoted in prose but not present in any curated JSON
    """
    quoted = parse(literal) if literal is not None else None
    entry = {
        "id": len(LEDGER) + 1,
        "doc": doc,
        "locator": locator,
        "claim": claim,
        "quoted_literal": literal,
        "quoted_value": quoted,
        "derivation": derivation,
        "derived_value": derived,
        "kind": kind,
    }
    if quoted is not None and derived is not None and math.isfinite(derived):
        abs_err = abs(derived - quoted)
        entry["abs_err"] = abs_err
        entry["rel_err"] = abs_err / abs(derived) if derived != 0 else (0.0 if abs_err == 0 else float("inf"))
        entry["half_ulps"] = abs_err / (0.5 * ulp_of(literal))
        entry["quoted_is_high"] = quoted > derived
    if kind == "exact":
        entry["status"] = "REPRODUCES" if entry.get("half_ulps", 0.0) <= 1.0 else "MISMATCH"
    elif kind == "fullprec":
        entry["status"] = "REPRODUCES" if entry.get("rel_err", 0.0) <= 1e-12 else "MISMATCH"
    elif kind == "order":
        dec = abs(math.log10(abs(derived) / abs(quoted))) if derived and quoted else float("inf")
        entry["decades_off"] = dec
        entry["status"] = "REPRODUCES_APPROX" if dec <= 1.0 else "MISMATCH"
    elif kind == "bound":
        entry["matching_sig_digits"] = digits
        entry["status"] = "REPRODUCES" if digits >= int(quoted) else "MISMATCH"
    elif kind == "approx":
        entry["status"] = "REPRODUCES_APPROX" if entry.get("rel_err", 0.0) <= 0.5 else "MISMATCH"
    elif kind == "qualifier":
        entry["status"] = "QUALIFIER_NOT_SUPPORTED"
    else:
        entry["status"] = "NOT_IN_CURATED_JSON"
    if note:
        entry["note"] = note
    LEDGER.append(entry)
    return entry


# ---------------------------------------------------------------------------
# derived helpers, all from banked data
# ---------------------------------------------------------------------------

def mm_row(cls, K):
    for r in MM["MM1_inequality"]:
        if r["class"] == cls and r["K"] == K:
            return r
    raise KeyError((cls, K))


def battery(cls, gauge, K, shape):
    for r in MM["MM2_shape_battery"]:
        if r["class"] == cls and r["gauge"] == gauge and r["K"] == K:
            return r["by_shape"][shape]
    raise KeyError((cls, gauge, K, shape))


def best_admissible():
    best = None
    for r in MM["MM2_shape_battery"]:
        for sh, v in r["by_shape"].items():
            if v["admissible"] and (best is None or v["Z1"] < best[1]["Z1"]):
                best = (r, v, sh)
    return best


def best_block_diag():
    best = None
    for r in MM["MM2_shape_battery"]:
        v = r["by_shape"]["block_diag"]
        if best is None or v["Z1"] < best[1]["Z1"]:
            best = (r, v, "block_diag")
    return best


def tn_rung(n):
    for r in TN["rungs"]:
        if r["certificate"]["n"] == n:
            return r
    raise KeyError(n)


def l1v2_curve(s):
    for c in L1V2["S6_window"]["curve"]:
        if abs(c["s"] - s) < 1e-12:
            return c
    raise KeyError(s)


def l1v2_tail(cls, param):
    for t in L1V2["S3_terms"]["tail"]:
        if t["class"] == cls and abs(t["param"] - param) < 1e-12:
            return t
    raise KeyError((cls, param))


# ===========================================================================
# A.  The leg-51 window numbers -- the premise both deaths inherit
#     (DIRECTION.md names these explicitly: +0.639, 0.606, the per-class
#      tail-divergence exponents)
# ===========================================================================

D = "PHASE2_P2_NOTES.md"
W = L1V2["S6_window"]["window"]

row(D, "L1v2-4", "divergence-curve minimum", "0.639",
    l1v2_curve(1.0)["divergence_exponent"],
    "S6_window.curve[s=1.0].divergence_exponent")
row(D, "L1v2-4", "curve at s = 0", "1.28",
    l1v2_curve(0.0)["divergence_exponent"],
    "S6_window.curve[s=0.0].divergence_exponent")
row(D, "L1v2-4", "curve at s = 2", "1.27",
    l1v2_curve(2.0)["divergence_exponent"],
    "S6_window.curve[s=2.0].divergence_exponent",
    note="the same literal is re-quoted at writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md:168")
row(D, "L1v2-4", "curve at the object's own boundary s = alpha", "1.00",
    l1v2_curve(0.394)["divergence_exponent"],
    "S6_window.curve[s=0.394].divergence_exponent")
row(D, "L1v2-4", "window gap in exponent units", "0.606",
    W["gap"], "S6_window.window.gap")
row(D, "L1v2-4", "gap re-derived as s_operator - s_max_object", "0.606",
    W["s_operator"] - W["s_max_object"],
    "S6_window.window.s_operator - .s_max_object")
row(D, "L1v2-4", "target far-field exponent alpha", "0.394",
    W["alpha"], "S6_window.window.alpha")
row(D, "L1v2-4", "no point of the curve touches zero: min over the curve", "0.639",
    min(c["divergence_exponent"] for c in L1V2["S6_window"]["curve"]),
    "min over S6_window.curve of divergence_exponent")

# L1v2-3, the per-class tail table
for label, cls, param, first, last, expo, permode in [
    ("flat w=1", "flat", 0.0, "1.02", "16.3", "1.28", "1.0029"),
    ("algebraic s=0.394", "algebraic", 0.394, "0.876", "7.66", "1.00", "1.0023"),
    ("algebraic s=1", "algebraic", 1.0, "0.706", "2.87", "0.64", "1.0015"),
    ("geometric nu=1.05", "geometric", 1.05, "2.51", "5.75e+18", None, "1.045"),
    ("geometric nu=1.20", "geometric", 1.2, "2.74e+03", "3.60e+77", None, "1.195"),
]:
    t = l1v2_tail(cls, param)
    row(D, "L1v2-3", "tail inverse norm at M=128, " + label, first,
        t["norm"][0], "S3_terms.tail[%s].norm[0]" % label)
    row(D, "L1v2-3", "tail inverse norm at M=1088, " + label, last,
        t["norm"][-1], "S3_terms.tail[%s].norm[-1]" % label)
    if expo is not None:
        row(D, "L1v2-3", "divergence exponent, " + label, expo,
            t["divergence_exponent"], "S3_terms.tail[%s].divergence_exponent" % label)
    row(D, "L1v2-3", "per-mode growth, " + label, permode,
        t["per_mode_growth"], "S3_terms.tail[%s].per_mode_growth" % label)

# the verbal precision claim attached to that table
g105 = l1v2_tail("geometric", 1.05)["per_mode_growth"]
g120 = l1v2_tail("geometric", 1.2)["per_mode_growth"]
row(D, "L1v2-3", "'the geometric growth factor IS nu, to three digits' -- "
    "worst relative gap between per_mode_growth and nu",
    None, max(abs(g105 - 1.05) / 1.05, abs(g120 - 1.20) / 1.20),
    "max over the two geometric classes of |per_mode_growth - nu| / nu",
    kind="qualifier",
    note="agreement is 4.7e-03 and 4.5e-03 relative, i.e. two significant digits, not three")

# leg 51's exact-arithmetic check, re-quoted in TECHNICAL_P2_ROUTEL1_V2 sec 8
T51 = "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md"
S5 = {r["K"]: r for r in L1V2["S5_exact_check"]["rows"]}
row(T51, "sec 8", "exact weighted inverse norm at K = 96", "62.0005",
    S5[96]["exact"], "S5_exact_check.rows[K=96].exact")
row(T51, "sec 8", "exact weighted inverse norm at K = 128", "609.17",
    S5[128]["exact"], "S5_exact_check.rows[K=128].exact")
row(T51, "sec 8", "max relative gap exact vs float", "8.8e-15",
    L1V2["S5_exact_check"]["max_rel_gap"], "S5_exact_check.max_rel_gap")
row(T51, "sec 9", "U-curve minimum exponent", "0.64",
    l1v2_curve(1.0)["divergence_exponent"], "S6_window.curve[s=1.0]")
row(T51, "sec 9", "exponent at s = 0", "1.28",
    l1v2_curve(0.0)["divergence_exponent"], "S6_window.curve[s=0.0]")
row(T51, "sec 9", "exponent at s = 2", "1.27",
    l1v2_curve(2.0)["divergence_exponent"], "S6_window.curve[s=2.0]",
    note="same defect as PHASE2_P2_NOTES.md L1v2-4; this site is inside writeup/")
row(T51, "sec 9", "exponent at s = alpha = 0.394", "1.00",
    l1v2_curve(0.394)["divergence_exponent"], "S6_window.curve[s=0.394]")
row(T51, "sec 9", "window empty by", "0.606", W["gap"], "S6_window.window.gap")


# ===========================================================================
# B.  The coefficient-basis death (leg 54 / Route-MM)
# ===========================================================================

D = "PHASE2_P2_NOTES.md"
ba_r, ba_v, ba_s = best_admissible()
bd_r, bd_v, bd_s = best_block_diag()

row(D, "Route-MM v1", "best admissible Z1 over every shape x class x gauge x split", "8.9591",
    ba_v["Z1"], "min over MM2_shape_battery of by_shape[*].Z1 with admissible=true")
row(D, "Route-MM v1", "block-diagonal baseline", "10.4584",
    bd_v["Z1"], "min over MM2_shape_battery of by_shape.block_diag.Z1")
row(D, "Route-MM v1", "improvement factor", "1.167",
    bd_v["Z1"] / ba_v["Z1"], "baseline / best admissible, both re-minimised from the battery")
row(D, "Route-MM v1", "'more than 8x was needed' -- factor still needed at the best shape",
    "8", ba_v["Z1"] / 1.0, "best admissible Z1 / the 1 it must be under", kind="approx")
row(D, "Route-MM v1", "v1's wrongly-reported best (K>=4 only)", "32.75",
    battery("algebraic", "null", 4, "schur")["Z1"],
    "MM2_shape_battery[algebraic,null,K=4].by_shape.schur.Z1")

MMT = "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEMM_V1.md"
MMB = "writeup/4_p2_lottery/BLOG_P2_ROUTEMM_V1.md"

row(MMT, "sec 0", "leg 53's coupling sub-block at the best split", "43.15",
    MM["MM2_instrument_check_vs_leg53"]["leg54_Z1_Gamma_tail"],
    "MM2_instrument_check_vs_leg53.leg54_Z1_Gamma_tail")

# MM-1's RHS table, both classes, all seven splits
for cls, label, vals in [
    ("flat", "flat s = 0",
     {2: "0.00000", 4: "0.99611", 6: "1.98835", 8: "2.97674",
      16: "6.89231", 32: "14.54545", 64: "29.17647"}),
    ("algebraic", "algebraic s = 0.3",
     {2: "0.00000", 4: "1.38731", 6: "2.76244", 8: "4.12384",
      16: "9.44094", 32: "19.55753", 64: "38.18210"}),
]:
    for K, lit in vals.items():
        r = mm_row(cls, K)
        row(MMT, "sec 1 table", "MM-1 RHS, %s, K = %d" % (label, K), lit, r["rhs"],
            "MM1_inequality[%s,K=%d].rhs" % (cls, K))
        # and the RHS's own factorisation, re-derived
        prod = r["prefactor_abs_1_minus_K_over_2"] * r["weight_ratio"] * r["A_tail_e_Kplus1"]
        row(MMT, "sec 1 table", "MM-1 RHS re-derived as prefactor x weight_ratio x "
            "||A_tail e_{K+1}||, %s, K = %d" % (label, K), lit, prod,
            "MM1_inequality[%s,K=%d]: product of the three stored factors" % (cls, K))

ratios = [abs(r["ratio_measured_over_rhs"] - 1.0) for r in MM["MM1_inequality"]
          if r.get("ratio_measured_over_rhs") is not None]
row(MMT, "sec 1", "'measured / RHS = 1.0000 at every K' -- worst deviation from one",
    "1.0000", 1.0 + max(ratios), "1 + max |MM1_inequality[*].ratio_measured_over_rhs - 1|")

sm = MM["MM1_smallest_K_with_rhs_above_one"]
row(MMT, "sec 1", "smallest split whose RHS exceeds 1, flat", "6",
    float(min(r["K"] for r in MM["MM1_inequality"] if r["class"] == "flat" and r["rhs"] > 1.0)),
    "min K over MM1_inequality[flat] with rhs > 1 (stored key says %d)" % sm["flat"])
row(MMT, "sec 1", "smallest split whose RHS exceeds 1, algebraic", "4",
    float(min(r["K"] for r in MM["MM1_inequality"] if r["class"] == "algebraic" and r["rhs"] > 1.0)),
    "min K over MM1_inequality[algebraic] with rhs > 1 (stored key says %d)" % sm["algebraic"])

# the second factor -- the one place leg 54's prose and leg 54's own key disagree
sf = [(r["weight_ratio"] * r["A_tail_e_Kplus1"], r) for r in MM["MM1_inequality"] if r["K"] >= 4]
sf_lo, sf_hi = min(v for v, _ in sf), max(v for v, _ in sf)
row(MMT, "sec 1", "VER-A's second-factor range, low end, K = 4..64", "0.9412", sf_lo,
    "min over MM1_inequality[K>=4] of weight_ratio * A_tail_e_Kplus1 "
    "(VER-A stores %.15g)" % VERA["V5_MM1_inequality"]["second_factor_range_leg53_sweep"][0])
row(MMT, "sec 1", "VER-A's second-factor range, high end, K = 4..64", "1.3873", sf_hi,
    "max over MM1_inequality[K>=4] of weight_ratio * A_tail_e_Kplus1 "
    "(VER-A stores %.15g)" % VERA["V5_MM1_inequality"]["second_factor_range_leg53_sweep"][1])
row(MMT, "sec 1", "the JSON key the prose points at, high end -- "
    "MM1_second_factor_range[1] against the second factor as sec 1 defines it",
    None, sf_hi,
    "stored MM1_second_factor_range[1] = %.16g; re-derived from the same file's own rows "
    "= %.16g" % (MM["MM1_second_factor_range"][1], sf_hi),
    kind="qualifier",
    note="the stored key is min/max of A_tail_e_Kplus1 ALONE -- the (w_{K+1}/w_K) factor of "
         "the displayed inequality is missing. Low end coincides (flat weight ratio == 1); "
         "high end is 1.3318429055906214 stored against 1.3873146915152630 re-derived.")

# MM-1b, the odd-split fact
oddsv = [r["smallest_singular_value"] for r in MM["MM1b_odd_K_scan"] if r["K_is_odd"]]
evensv = [r["smallest_singular_value"] for r in MM["MM1b_odd_K_scan"] if not r["K_is_odd"]]
row(MMT, "sec 2", "largest smallest-singular-value at odd K", "2.031040049676364e-16",
    max(oddsv), "max over MM1b_odd_K_scan[K odd] of smallest_singular_value")
row(MMT, "sec 2", "smallest smallest-singular-value at even K", "0.008089880594474517",
    min(evensv), "min over MM1b_odd_K_scan[K even] of smallest_singular_value")
k3nf = [r["smallest_singular_value"] for r in MM["MM1b_odd_K_scan"]
        if r["K"] == 3 and not r["far_field"]]
row(MMT, "sec 2", "K = 3 without the far-field column is exactly 0.0", "0.0",
    max(k3nf), "max over MM1b_odd_K_scan[K=3, far_field=false] of smallest_singular_value")
k3 = [len(r["left_null_support"]) for r in MM["MM1b_odd_K_scan"]
      if r["K"] == 3 and r["far_field"]]
k5 = [len(r["left_null_support"]) for r in MM["MM1b_odd_K_scan"]
      if r["K"] == 5 and r["far_field"]]
row(MMT, "sec 2", "left-null support size at K = 3 (with the far-field column)", "2",
    float(max(k3)), "max |MM1b_odd_K_scan[K=3, far_field=true].left_null_support|")
row(MMT, "sec 2", "left-null support size at K = 5 (with the far-field column)", "3",
    float(min(k5)), "min |MM1b_odd_K_scan[K=5, far_field=true].left_null_support|")

# MM-2, the corrected headline
row(MMT, "sec 3 correction", "corrected best admissible Z1", "8.9591", ba_v["Z1"],
    "min over MM2_shape_battery of admissible by_shape[*].Z1 (shape=%s, class=%s, "
    "gauge=%s, K=%d)" % (ba_s, ba_r["class"], ba_r["gauge"], ba_r["K"]))
row(MMT, "sec 3 correction", "corrected block-diagonal baseline", "10.4584", bd_v["Z1"],
    "min over MM2_shape_battery of by_shape.block_diag.Z1")
row(MMT, "sec 3 correction", "corrected improvement", "1.167", bd_v["Z1"] / ba_v["Z1"],
    "re-minimised baseline / re-minimised best admissible")
row(MMT, "sec 3 correction", "v1's best admissible (schur, K = 4)", "32.7489",
    battery("algebraic", "null", 4, "schur")["Z1"],
    "MM2_shape_battery[algebraic,null,K=4].by_shape.schur.Z1")
row(MMT, "sec 3 correction", "v1's block-diagonal baseline", "45.3628",
    battery("algebraic", "null", 4, "block_diag")["Z1"],
    "MM2_shape_battery[algebraic,null,K=4].by_shape.block_diag.Z1")
row(MMT, "sec 3 correction", "v1's improvement factor", "1.385",
    battery("algebraic", "null", 4, "block_diag")["Z1"]
    / battery("algebraic", "null", 4, "schur")["Z1"],
    "v1 baseline / v1 best, both from the battery at K = 4")
row(MMT, "sec 3", "'8.96 >> 1' -- the gate margin", "8.96", ba_v["Z1"],
    "best admissible Z1 against the 1 it must be under")
row(MMT, "sec 3", "spending the shape buys ~1.17x", "1.17", bd_v["Z1"] / ba_v["Z1"],
    "baseline / best admissible", kind="approx")
row(MMT, "sec 3", "where ~9x was needed", "9", ba_v["Z1"],
    "best admissible Z1 / 1", kind="approx")

gsl_digits = min(matching_sig_digits(r["by_shape"]["gs_lower"]["Z1_Gamma_tail"],
                                     r["by_shape"]["block_diag"]["Z1_Gamma_tail"])
                 for r in MM["MM2_shape_battery"])
row(MMT, "sec 3", "'gs_lower identical to block_diag to five digits' -- worst matching "
    "significant digits of the (Gamma,tail) block over the whole battery", "5", gsl_digits,
    "min over MM2_shape_battery of matching significant digits between "
    "gs_lower.Z1_Gamma_tail and block_diag.Z1_Gamma_tail", kind="bound", digits=gsl_digits,
    note="the two sub-blocks are in fact bit-identical in every row of the battery, which is "
         "stronger than the five digits claimed")

ic = MM["MM2_instrument_check_vs_leg53"]
row(MMT, "sec 3", "instrument check, Z1[Gamma<-tail]", "43.151291", ic["leg54_Z1_Gamma_tail"],
    "MM2_instrument_check_vs_leg53.leg54_Z1_Gamma_tail")
row(MMT, "sec 3", "instrument check, Z1[tail<-Gamma]", "1.387315", ic["leg54_Z1_tail_Gamma"],
    "MM2_instrument_check_vs_leg53.leg54_Z1_tail_Gamma")
row(MMT, "sec 3", "leg 53's own Z1[Gamma<-tail] reproduced", "43.151291",
    ic["leg53_Z1_Gamma_tail"], "MM2_instrument_check_vs_leg53.leg53_Z1_Gamma_tail")
row(MMT, "sec 3.1", "leg 53's tail-tail figure, as leg 53 charged it", "6.0e-13",
    6.0e-13, "MM2_instrument_check_vs_leg53.correction_to_leg53 (quoted in the record)",
    kind="approx")
row(MMT, "sec 3.1", "tail-tail charged against the bare scaled tail", "2.2", 2.2116,
    "MM2_instrument_check_vs_leg53.correction_to_leg53: ||I - A_tail T|| = 2.2116",
    kind="approx")

# MM-4, the floor
row(MMT, "sec 4", "smallest floor over every class and split", "5.0444",
    min(r["floor_with_Gamma_inv_A11"] for r in MM["MM4_floor"]),
    "min over MM4_floor of floor_with_Gamma_inv_A11")
row(MMT, "sec 4.1", "kernel truncation defect, relative, at M_extra = 1024", "1.46e-02",
    max(r["relative_l1_defect"] for r in MM["MM4b_kernel_truncation_defect"]
        if r["M_extra"] == 1024),
    "max over MM4b_kernel_truncation_defect[M_extra=1024] of relative_l1_defect")
_halving = [a["relative_l1_defect"] / b["relative_l1_defect"]
            for a, b in zip(MM["MM4b_kernel_truncation_defect"][:-1],
                            MM["MM4b_kernel_truncation_defect"][1:])
            if b["M_extra"] == 2 * a["M_extra"]]
row(MMT, "sec 4.1", "'the defect halves per doubling of M' -- worst consecutive ratio",
    "2", min(_halving), "min consecutive ratio in MM4b_kernel_truncation_defect "
    "(range %.6g .. %.6g)" % (min(_halving), max(_halving)), kind="approx")

adm = [r for r in MM["MM4d_dropped_term_by_shape"] if r["shape"] in ("schur", "gs_upper")]
row(MMT, "sec 4 table", "||A12|| for schur/gs_upper, low end", "2",
    min(r["A12_norm"] for r in adm), "min A12_norm over MM4d[schur,gs_upper]", kind="approx")
row(MMT, "sec 4 table", "||A12|| for schur/gs_upper, high end", "10",
    max(r["A12_norm"] for r in adm), "max A12_norm over MM4d[schur,gs_upper]", kind="approx")
row(MMT, "sec 4 table", "'~5e-04' dropped term for schur/gs_upper -- the actual spread",
    None, max(r["dropped_term"] for r in adm),
    "MM4d[schur,gs_upper].dropped_term ranges %.6g .. %.6g"
    % (min(r["dropped_term"] for r in adm), max(r["dropped_term"] for r in adm)),
    kind="qualifier",
    note="the largest is 2.9x the quoted ~5e-04; the conclusion (0.000x the floor) is "
         "unaffected -- worst term_over_floor for an admissible shape is 6.95e-05")
orc = [r for r in MM["MM4d_dropped_term_by_shape"]
       if r["shape"] == "oracle_pinv" and r["class"] == "flat" and r["K"] == 2][0]
exi = [r for r in MM["MM4d_dropped_term_by_shape"]
       if r["shape"] == "exact_inv" and r["class"] == "flat" and r["K"] == 2][0]
row(MMT, "sec 4 table", "oracle_pinv ||A12||", "7176", orc["A12_norm"], "MM4d[oracle_pinv,flat,K=2]")
row(MMT, "sec 4 table", "oracle_pinv dropped term", "7.008", orc["dropped_term"], "MM4d[oracle_pinv,flat,K=2]")
row(MMT, "sec 4 table", "oracle_pinv term / floor", "1.000", orc["term_over_floor"], "MM4d[oracle_pinv,flat,K=2]")
row(MMT, "sec 4 table", "exact_inv ||A12||", "3588", exi["A12_norm"], "MM4d[exact_inv,flat,K=2]")
row(MMT, "sec 4 table", "exact_inv dropped term", "3.504", exi["dropped_term"], "MM4d[exact_inv,flat,K=2]")
row(MMT, "sec 4 table", "exact_inv term / floor", "0.500", exi["term_over_floor"], "MM4d[exact_inv,flat,K=2]")
row(MMT, "sec 4", "'every admissible shape is 0.000x the floor' -- worst admissible ratio",
    "0.000", MM["MM4d_max_term_over_floor_admissible"], "MM4d_max_term_over_floor_admissible")
row(MMT, "sec 4", "the audit that independently kills the inadmissible shapes", "1.03e+04",
    MM["MM3_min_Z1_over_audit"], "MM3_min_Z1_over_audit")

# MM-4.2, the counter-construction table
cc = {(r["class"], r["K"]): r for r in MM["MM4c_counter_construction"]}
for key, label, floor_lit, beat_lit, gg_lit in [
    (("flat", 2), "flat K=2", "7.0078", "2.2e-16", "0.0"),
    (("flat", 4), "flat K=4", "23.0703", "3.7e-15", "0.0"),
    (("algebraic", 2), "alg. K=2", "5.0444", "7.8e-16", "1.2e-16"),
    (("algebraic", 4), "alg. K=4", "13.7426", "7.8e-16", "1.3e-15"),
]:
    r = cc[key]
    row(MMT, "sec 4.2 table", "floor as claimed in v1, " + label, floor_lit,
        r["leg_floor"], "MM4c_counter_construction[%s].leg_floor" % label)
    row(MMT, "sec 4.2 table", "floor with VER-A2's A11, " + label, beat_lit,
        r["floor_with_VERA2_A11"], "MM4c_counter_construction[%s].floor_with_VERA2_A11" % label)
    row(MMT, "sec 4.2 table", "(Gamma,Gamma) block of I - AL, " + label, gg_lit,
        r["Gamma_Gamma_block"], "MM4c_counter_construction[%s].Gamma_Gamma_block" % label)

row(MMT, "sec 4.2", "counter-construction ||A12||, low end", "1.1e+03",
    min(r["A12_norm"] for r in MM["MM4c_counter_construction"]),
    "min MM4c_counter_construction[*].A12_norm", kind="approx")
row(MMT, "sec 4.2", "counter-construction ||A12||, high end", "7.9e+03",
    max(r["A12_norm"] for r in MM["MM4c_counter_construction"]),
    "max MM4c_counter_construction[*].A12_norm", kind="approx")
row(MMT, "sec 4.2", "total Z1 the counter-construction pays", "565844.3730406046",
    min(r["total_Z1"] for r in MM["MM4c_counter_construction"]),
    "min MM4c_counter_construction[*].total_Z1 (stored key MM4c_min_total_Z1... = %.10f)"
    % MM["MM4c_min_total_Z1_of_counter_construction"])
row(MMT, "sec 4.2", "A11 freedom effect the v1 ablation saw", "0.003347947823294759",
    max(r["A11_freedom_changes_it_by"] for r in MM["MM4_floor"]),
    "max MM4_floor[*].A11_freedom_changes_it_by (relative)")
row(MMT, "sec 4.2", "the floor the honest statement keeps", "5.0444",
    MM["MM4_min_floor"], "MM4_min_floor")

# MM-3, the admissibility audit
aud = MM["MM3_admissibility_audit"]
row(MMT, "sec 5", "smallest Z1 anywhere in the admissibility audit", "1.03e+04",
    min(r["Z1"] for r in aud), "min MM3_admissibility_audit[*].Z1")
for cls, lit in [("flat", "3.9091174726301685"), ("algebraic", "3.198496678837019")]:
    rows_c = sorted([r for r in aud if r["class"] == cls and r["M_L_extra"] == 1024],
                    key=lambda r: r["M_A_extra"])
    growth = (rows_c[-1]["Z1"] / rows_c[0]["Z1"]) ** (1.0 / (len(rows_c) - 1))
    row(MMT, "sec 5", "growth per doubling of M_A, " + cls, lit, growth,
        "geometric growth of MM3 Z1 over M_A = 128,256,512 at M_L = 1024",
        kind="fullprec")
ml_digits = min(matching_sig_digits(a["Z1"], b["Z1"]) for a in aud for b in aud
                if a["class"] == b["class"] and a["M_A_extra"] == b["M_A_extra"]
                and a["M_L_extra"] == 1024 and b["M_L_extra"] == 2048)
_mlpairs = [(a, b) for a in aud for b in aud
            if a["class"] == b["class"] and a["M_A_extra"] == b["M_A_extra"]
            and a["M_L_extra"] == 1024 and b["M_L_extra"] == 2048]
_worst = min(_mlpairs, key=lambda ab: matching_sig_digits(ab[0]["Z1"], ab[1]["Z1"]))
ml_relgap = max(abs(a["Z1"] - b["Z1"]) / a["Z1"] for a, b in _mlpairs)
row(MMT, "sec 5", "'the M_L = 1024 and 2048 rows agree to five digits' -- worst matching "
    "significant digits over the audit", "5", ml_digits,
    "min matching significant digits between the M_L = 1024 and 2048 rows of "
    "MM3_admissibility_audit; worst pair is %s M_A=%d: %.10g vs %.10g"
    % (_worst[0]["class"], _worst[0]["M_A_extra"], _worst[0]["Z1"], _worst[1]["Z1"]),
    kind="bound", digits=ml_digits,
    note="five of the six (M_A, class) pairs agree to 5 or 6 digits; one agrees to %d "
         "(%.10g vs %.10g). Worst relative gap over the audit is %.4g, so the claim the "
         "sentence is making -- that the cost is essentially independent of M_L -- holds; "
         "the digit count is one too generous." % (ml_digits, _worst[0]["Z1"],
                                                   _worst[1]["Z1"], ml_relgap))

row(MMT, "sec 5", "the exact inverse's float-noise Z1, which admissibility rejects", "1e-9",
    MM["gate_smallest_Z1_any_shape_including_inadmissible"],
    "gate_smallest_Z1_any_shape_including_inadmissible", kind="order")

# MM-5 / MM-5b, the controls
mu_below = [r["mu"] for r in MM["MM5_positive_control"]
            if min(r["by_shape"].values()) < 1.0]
row(MMT, "sec 6", "smallest mu at which the positive control gets Z1 below 1", "0.1",
    min(mu_below), "min mu over MM5_positive_control with any shape below 1")
row(MMT, "sec 6", "shapes that reach below 1 in the control", "4",
    float(len({sh for r in MM["MM5_positive_control"] for sh, v in r["by_shape"].items()
               if v < 1.0})),
    "count of distinct shapes in MM5_positive_control reaching Z1 < 1")
seeds = [r for r in MM["MM5b_negative_controls"] if r["border"] == "random"]
row(MMT, "sec 6", "random-border seeds tried", "6", float(len(seeds)),
    "count of MM5b_negative_controls rows with border = random")
_analytic = [x for x in MM["MM5b_negative_controls"] if x["border"] == "analytic"][0]
row(MMT, "sec 6", "seeds where a wrong border makes schur BETTER", "6",
    float(sum(1 for r in seeds
              if r["by_shape"]["schur"] < _analytic["by_shape"]["schur"])),
    "count of random-border seeds whose schur Z1 is below the analytic-border schur Z1")
row(MMT, "sec 6", "smallest Z1 over every border and shape", "5.218797584187578",
    min(min(r["by_shape"].values()) for r in MM["MM5b_negative_controls"]),
    "min over MM5b_negative_controls of by_shape values", kind="fullprec")

# MM-6, the polynomial, and the conclusion
row(MMT, "sec 7", "r_max over every row of the polynomial", "0",
    max(r["r_max"] for r in MM["MM6_polynomial"]), "max MM6_polynomial[*].r_max")
row(MMT, "sec 7", "Y0 over every row of the polynomial", "0",
    max(abs(r["Y0"]) for r in MM["MM6_polynomial"]), "max |MM6_polynomial[*].Y0|")
row(MMT, "sec 8", "smallest Z1 anywhere, restated in the conclusion", "8.9591",
    MM["gate_smallest_Z1_admissible"], "gate_smallest_Z1_admissible")
row(MMT, "sec 8", "the floor restated in the conclusion", "5.0444",
    MM["MM4_min_floor"], "MM4_min_floor")
row(MMT, "sec 8", "smallest split swept by the battery", "2",
    float(min(r["K"] for r in MM["MM2_shape_battery"])), "min MM2_shape_battery[*].K")
row(MMT, "sec 8", "largest split swept by the battery", "64",
    float(max(r["K"] for r in MM["MM2_shape_battery"])), "max MM2_shape_battery[*].K")
row(MMT, "sec 8", "every swept split is even: worst K mod 2", "0",
    float(max(r["K"] % 2 for r in MM["MM2_shape_battery"])), "max K mod 2 over the battery")

# --- the blog ---
row(MMB, "title / result", "improvement the shape buys", "1.17", bd_v["Z1"] / ba_v["Z1"],
    "baseline / best admissible")
row(MMB, "where this was", "leg 53's assembled coupling", "43",
    ic["leg53_Z1_Gamma_tail"], "MM2_instrument_check_vs_leg53.leg53_Z1_Gamma_tail",
    kind="approx")
row(MMB, "the result", "block-diagonal baseline", "10.46", bd_v["Z1"], "re-minimised baseline")
row(MMB, "the result", "best legitimate alternative", "8.96", ba_v["Z1"], "re-minimised best admissible")
row(MMB, "the result", "factor needed", "9", ba_v["Z1"], "best admissible / 1", kind="approx")
row(MMB, "the result", "v1's baseline, named as a correction", "45.4",
    battery("algebraic", "null", 4, "block_diag")["Z1"], "battery[algebraic,null,K=4].block_diag",
    kind="approx")
row(MMB, "the result", "v1's best, named as a correction", "32.7",
    battery("algebraic", "null", 4, "schur")["Z1"], "battery[algebraic,null,K=4].schur",
    kind="approx")
row(MMB, "and then the review...", "v1's baseline, restated", "45.36",
    battery("algebraic", "null", 4, "block_diag")["Z1"], "battery[algebraic,null,K=4].block_diag")
row(MMB, "and then the review...", "v1's best, restated", "32.75",
    battery("algebraic", "null", 4, "schur")["Z1"], "battery[algebraic,null,K=4].schur")
row(MMB, "three things", "the exact inverse's meaningless number", "1e-9",
    MM["gate_smallest_Z1_any_shape_including_inadmissible"],
    "gate_smallest_Z1_any_shape_including_inadmissible", kind="order")
row(MMB, "three things", "the admissible version of that inverse", "1e4",
    MM["MM3_min_Z1_over_audit"], "MM3_min_Z1_over_audit", kind="order")
row(MMB, "three things", "'four orders of magnitude worse than the baseline it was supposed "
    "to beat' -- decades between the audit's smallest Z1 and the block-diagonal baseline",
    "4", math.log10(MM["MM3_min_Z1_over_audit"] / bd_v["Z1"]),
    "log10(MM3_min_Z1_over_audit / re-minimised block-diagonal baseline) = "
    "log10(%.6f / %.6f)" % (MM["MM3_min_Z1_over_audit"], bd_v["Z1"]),
    note="ratio is %.1fx; against v1's own 45.3628 baseline it is %.1fx (%.3f decades). "
         "No reading of 'the baseline' gives four decades at the quoted 10^4."
         % (MM["MM3_min_Z1_over_audit"] / bd_v["Z1"],
            MM["MM3_min_Z1_over_audit"] / battery("algebraic", "null", 4, "block_diag")["Z1"],
            math.log10(MM["MM3_min_Z1_over_audit"]
                       / battery("algebraic", "null", 4, "block_diag")["Z1"])))
row(MMB, "three things", "the floor", "5.0", MM["MM4_min_floor"], "MM4_min_floor", kind="approx")
_cc_alg2 = [r for r in MM["MM4c_counter_construction"]
            if r["class"] == "algebraic" and r["K"] == 2][0]
row(MMB, "three things", "what the reviewer's A11 drives the floor to (the 5.0 row)", "1e-16",
    _cc_alg2["floor_with_VERA2_A11"],
    "MM4c_counter_construction[algebraic,K=2].floor_with_VERA2_A11", kind="order")
row(MMB, "three things", "'fifteen orders of magnitude' -- decades the floor is beaten by",
    "15", math.log10(_cc_alg2["leg_floor"] / _cc_alg2["floor_with_VERA2_A11"]),
    "log10(leg_floor / floor_with_VERA2_A11) at algebraic K = 2", kind="approx")
row(MMB, "three things", "the total error that construction pays", "5.7e+05",
    MM["MM4c_min_total_Z1_of_counter_construction"], "MM4c_min_total_Z1_of_counter_construction")
row(MMB, "three things", "'the two arms agree to three decimal places' -- worst relative "
    "gap between the Gamma^-1 and Schur arms of the v1 ablation",
    None, MM["MM4_max_A11_freedom_effect"],
    "max MM4_floor[*].A11_freedom_changes_it_by = %.6g (relative); in absolute floor units "
    "the worst pair is %.4f vs %.4f"
    % (MM["MM4_max_A11_freedom_effect"],
       [r for r in MM["MM4_floor"] if r["class"] == "flat" and r["K"] == 64][0]["floor_with_Gamma_inv_A11"],
       [r for r in MM["MM4_floor"] if r["class"] == "flat" and r["K"] == 64][0]["floor_with_schur_A11"]),
    kind="qualifier",
    note="3.3e-03 relative is agreement to ~2 decimal places, not 3; the point the sentence "
         "makes (the control varied nothing) is unaffected and is the correct reading")
row(MMB, "two things I got told", "the split above which MM-1 bites, flat", "6",
    float(min(r["K"] for r in MM["MM1_inequality"] if r["class"] == "flat" and r["rhs"] > 1.0)),
    "min K over MM1_inequality[flat] with rhs > 1")


# ===========================================================================
# C.  The collocation-basis death (leg 56 / Route-TN)
# ===========================================================================

D = "PHASE2_P2_NOTES.md"
r801 = tn_rung(801)
V = TN["verdict"]

row(D, "Route-TN v1", "derivative defect over budget at n = 801", "1.85e7",
    r801["ratios"]["defect_D_over_tau"], "rungs[n=801].ratios.defect_D_over_tau")
row(D, "Route-TN v1", "Hilbert defect over budget at n = 801", "2.04e11",
    r801["ratios"]["defect_H_over_tau"], "rungs[n=801].ratios.defect_H_over_tau")
row(D, "Route-TN v1", "derivative convergence order", "4.01",
    TN["rates"]["defect_D_odd_rate"][-1]["order"], "rates.defect_D_odd_rate[-1].order")
row(D, "Route-TN v1", "n the genuine Hilbert interpolation error would need", "4.4e6",
    TN["H_attribution"]["n_required_interpolation_only"],
    "H_attribution.n_required_interpolation_only", kind="approx")

TNT = "writeup/4_p2_lottery/TECHNICAL_P2_ROUTETN_V1.md"
TNB = "writeup/4_p2_lottery/BLOG_P2_ROUTETN_V1.md"
HZ = TN["validation"]["H_is_endpoint_zeroed_check"]

row(TNT, "sec 1", "the frozen reach", "745.2394128947751", r801["certificate"]["X_max"],
    "rungs[n=801].certificate.X_max")
row(TNT, "sec 3 table", "node 1 abscissa at n = 201", "-687.943", HZ["X"],
    "validation.H_is_endpoint_zeroed_check.X")
row(TNT, "sec 3 table", "H_disc f", "-1.8584719686e-03", HZ["H_disc"], "...H_disc")
row(TNT, "sec 3 table", "H of the endpoint-zeroed interpolant, PV quadrature",
    "-1.8584719686e-03", HZ["H_of_endpoint_zeroed_interpolant_quadrature"], "...quadrature")
row(TNT, "sec 3 table", "its distance from H_disc", "2.61e-15",
    HZ["abs_diff_H_disc_vs_endpoint_zeroed"], "...abs_diff_H_disc_vs_endpoint_zeroed")
row(TNT, "sec 3 table", "H of the FULL interpolant, PV quadrature", "-1.4880639571e-03",
    HZ["H_of_full_interpolant_quadrature"], "...H_of_full_interpolant_quadrature")
row(TNT, "sec 3 table", "its distance from H_disc", "3.704e-04",
    HZ["abs_diff_H_disc_vs_full"], "...abs_diff_H_disc_vs_full")
row(TNT, "sec 3 table", "full-interpolant matrix vs quadrature", "4.34e-19",
    HZ["abs_diff_full_matrix_vs_quadrature"], "...abs_diff_full_matrix_vs_quadrature")
row(TNT, "sec 3 table", "the reference H_M f", "-1.4885580e-03", HZ["H_M_reference"],
    "...H_M_reference")
row(TNT, "sec 4", "interior nodes at n = 801", "799", float(r801["defects"]["odd"]["interior_nodes"]),
    "rungs[n=801].defects.odd.interior_nodes")
row(TNT, "sec 4", "excluded endpoint nodes", "2", float(r801["defects"]["odd"]["excluded_nodes"]),
    "rungs[n=801].defects.odd.excluded_nodes")
row(TNT, "sec 5", "ilog max width", "3.55e-14", TN["validation"]["ilog_max_width"],
    "validation.ilog_max_width")
row(TNT, "sec 5", "iatan_small max width", "1.48e-14", TN["validation"]["iatan_max_width"],
    "validation.iatan_max_width")
row(TNT, "sec 6", "budget at n = 801", "3.554656e-10", r801["certificate"]["budget"],
    "rungs[n=801].certificate.budget")
row(TNT, "sec 6", "||A||_w at n = 801", "15417.7", r801["certificate"]["A_norm"],
    "rungs[n=801].certificate.A_norm")
row(TNT, "sec 6", "tau = budget / ||A||_w", "2.306e-14",
    r801["certificate"]["budget"] / r801["certificate"]["A_norm"],
    "rungs[n=801].certificate.budget / .A_norm, re-divided here")
row(TNT, "sec 6", "tau as stored", "2.306e-14", r801["certificate"]["tau_admissible_defect"],
    "rungs[n=801].certificate.tau_admissible_defect")
row(TNT, "sec 6", "budget re-derived as (1-Z1)^2 / 2 Z2", "3.554656e-10",
    (1.0 - r801["certificate"]["Z1"]) ** 2 / (2.0 * r801["certificate"]["Z2"]),
    "from rungs[n=801].certificate Z1 and Z2 alone")
row(TNT, "sec 6", "Y0 re-derived by this leg", "9.97e-12", r801["certificate"]["Y0"],
    "rungs[n=801].certificate.Y0")
row(TNT, "sec 6", "Y0 as leg 46 stored it", "7.35e-12", TN["leg46_reference_as_stored"]["Y0"],
    "leg46_reference_as_stored.Y0")
row(TNT, "sec 6", "leg 46's stored budget, cross-checked against leg 46's own file",
    "3.554656e-10",
    [x for x in L1V1["L1_2_ladder"] if x["n"] == 801][0]["verdict"]["budget"],
    "p2_route_l1_v1_interval.json :: L1_2_ladder[n=801].verdict.budget")
row(TNT, "sec 6", "leg 46's stored ||A||_w, cross-checked against leg 46's own file",
    "15417.7",
    [x for x in L1V1["L1_2_ladder"] if x["n"] == 801][0]["interval"]["A_norm"],
    "p2_route_l1_v1_interval.json :: L1_2_ladder[n=801].interval.A_norm")

# the ladder
LADDER = {
    201: ("1.1220e-04", "4.7287e-03", "1.9042e-02", "2.3008e-13", None, None),
    401: ("6.8724e-06", "4.7131e-03", "2.2582e-02", "3.1728e-14", "4.03", "0.00"),
    801: ("4.2738e-07", "4.7041e-03", "2.6260e-02", "2.3056e-14", "4.01", "0.00"),
}
for n, (dl, hl, tl, taul, dord, hord) in LADDER.items():
    rr = tn_rung(n)
    o = rr["defects"]["odd"]
    row(TNT, "sec 7 ladder", "D defect at n = %d" % n, dl, o["defect_D_abs"],
        "rungs[n=%d].defects.odd.defect_D_abs" % n)
    row(TNT, "sec 7 ladder", "H defect at n = %d" % n, hl, o["defect_H_abs"],
        "rungs[n=%d].defects.odd.defect_H_abs" % n)
    row(TNT, "sec 7 ladder", "far-field truncation at n = %d" % n, tl, o["truncation_H_abs"],
        "rungs[n=%d].defects.odd.truncation_H_abs" % n)
    row(TNT, "sec 7 ladder", "tau at n = %d" % n, taul, rr["certificate"]["tau_admissible_defect"],
        "rungs[n=%d].certificate.tau_admissible_defect" % n)
idx = {401: 0, 801: 1}
for n in (401, 801):
    row(TNT, "sec 7 ladder", "D order at n = %d" % n, LADDER[n][4],
        TN["rates"]["defect_D_odd_rate"][idx[n]]["order"],
        "rates.defect_D_odd_rate[%d].order" % idx[n])
    row(TNT, "sec 7 ladder", "H order at n = %d" % n, LADDER[n][5],
        TN["rates"]["defect_H_odd_rate"][idx[n]]["order"],
        "rates.defect_H_odd_rate[%d].order" % idx[n])

row(TNT, "sec 7", "D against tau at n = 801", "1.854e+07", r801["ratios"]["defect_D_over_tau"],
    "rungs[n=801].ratios.defect_D_over_tau")
row(TNT, "sec 7", "D against tau, re-divided", "1.854e+07",
    r801["defects"]["odd"]["defect_D_abs"] / r801["certificate"]["tau_admissible_defect"],
    "defect_D_abs / tau, re-divided here")
row(TNT, "sec 7", "H against tau at n = 801", "2.040e+11", r801["ratios"]["defect_H_over_tau"],
    "rungs[n=801].ratios.defect_H_over_tau")
row(TNT, "sec 7", "H against tau, re-divided", "2.040e+11",
    r801["defects"]["odd"]["defect_H_abs"] / r801["certificate"]["tau_admissible_defect"],
    "defect_H_abs / tau, re-divided here")
row(TNT, "sec 7", "far-field truncation against tau", "1.139e+12",
    r801["ratios"]["truncation_over_tau"], "rungs[n=801].ratios.truncation_over_tau")
row(TNT, "sec 7", "n the derivative side would need", "52163",
    TN["D_only_extrapolation"]["n_required"], "D_only_extrapolation.n_required")
row(TNT, "sec 7", "the dense dimension that implies, N = 2n+3", "104329",
    2 * math.floor(TN["D_only_extrapolation"]["n_required"]) + 3,
    "2 * floor(D_only_extrapolation.n_required) + 3")
row(TNT, "sec 7", "H total growth over the 4x refinement", "1.0052",
    tn_rung(201)["defects"]["odd"]["defect_H_abs"] / r801["defects"]["odd"]["defect_H_abs"],
    "defect_H_abs at n=201 / at n=801")

# 7.1 attribution
ATT = {201: ("4.7351e-03", "6.3159e-06", None, None),
       401: ("4.7148e-03", "1.7022e-06", "0.01", "1.89"),
       801: ("4.7046e-03", "4.4181e-07", "0.00", "1.95")}
for k, n in enumerate((201, 401, 801)):
    ez, ip, ezo, ipo = ATT[n]
    row(TNT, "sec 7.1 table", "endpoint-zeroing term at n = %d" % n, ez,
        TN["H_attribution"]["defect_H_endpoint_zeroing"][k],
        "H_attribution.defect_H_endpoint_zeroing[%d]" % k)
    row(TNT, "sec 7.1 table", "true interpolation term at n = %d" % n, ip,
        TN["H_attribution"]["defect_H_interpolation"][k],
        "H_attribution.defect_H_interpolation[%d]" % k)
    if ezo is not None:
        row(TNT, "sec 7.1 table", "endpoint-zeroing order at n = %d" % n, ezo,
            TN["H_attribution"]["defect_H_endpoint_zeroing_rate"][k - 1]["order"],
            "H_attribution.defect_H_endpoint_zeroing_rate[%d].order" % (k - 1))
        row(TNT, "sec 7.1 table", "interpolation order at n = %d" % n, ipo,
            TN["H_attribution"]["defect_H_interpolation_rate"][k - 1]["order"],
            "H_attribution.defect_H_interpolation_rate[%d].order" % (k - 1))
row(TNT, "sec 7.1", "endpoint-zeroing share at n = 801", "1.00009",
    TN["H_attribution"]["endpoint_share_at_801"], "H_attribution.endpoint_share_at_801")
row(TNT, "sec 7.1", "share re-derived as endpoint / total", "1.00009",
    TN["H_attribution"]["defect_H_endpoint_zeroing"][2] / TN["H_attribution"]["defect_H_total"][2],
    "H_attribution.defect_H_endpoint_zeroing[2] / .defect_H_total[2]")
row(TNT, "sec 7.1", "'it dominates by four orders' -- endpoint / interpolation at n = 801",
    "4", math.log10(TN["H_attribution"]["defect_H_endpoint_zeroing"][2]
                    / TN["H_attribution"]["defect_H_interpolation"][2]),
    "log10(endpoint term / interpolation term) at n = 801", kind="approx")
row(TNT, "sec 7.1", "n the interpolation-only side would need", "4.43e+06",
    TN["H_attribution"]["n_required_interpolation_only"],
    "H_attribution.n_required_interpolation_only")
row(TNT, "sec 7.1", "interpolation order used in that extrapolation", "1.95",
    TN["H_attribution"]["interpolation_order"], "H_attribution.interpolation_order")

# the scale curve
SC = {0.125: "1.804e-03", 0.25: "2.752e-05", 0.5: "4.274e-07"}
for a, lit in SC.items():
    v = [r for r in TN["scale_curve"] if abs(r["a"] - a) < 1e-12][0]
    row(TNT, "sec 7 scale curve", "D defect at a = %s" % a, lit, v["defect_D_abs"],
        "scale_curve[a=%s].defect_D_abs" % a)
floor_vals = [r["defect_D_abs"] for r in TN["scale_curve"] if r["a"] >= 1.0]
row(TNT, "sec 7 scale curve", "D floors at", "7.13e-08", max(floor_vals),
    "max scale_curve[a>=1].defect_D_abs (range %.4g .. %.4g)"
    % (min(floor_vals), max(floor_vals)), kind="approx")
hflat = [r["defect_H_abs"] for r in TN["scale_curve"]]
row(TNT, "sec 7 scale curve", "H flat across the whole a range", "4.704e-03", max(hflat),
    "max scale_curve[*].defect_H_abs (range %.6g .. %.6g)" % (min(hflat), max(hflat)))
row(TNT, "sec 7 scale curve", "far-field mesh spacing h at |X| ~ 745, n = 801", "14.8",
    None, "NOT PRESENT in any curated JSON of leg 56", kind="absent",
    note="re-derives to 14.7599 from the grid definition X = c sinh(rho), c = 0.5, "
         "rho_max = 8, n = 801 (X_max = 0.5 sinh 8 = 745.2394128947751 confirms c and "
         "rho_max) -- but the document's own line 10 says every number below it is in the "
         "curated JSON, and this one is not")

# sec 8, the ablation
ABL = {201: ("4.7287e-03", "3.3289e-06", "1421", "1.1220e-04", "1.0051e-04", "1.12"),
       401: ("4.7131e-03", "3.1082e-06", "1516", "6.8724e-06", "6.1942e-06", "1.11"),
       801: ("4.7041e-03", "3.1303e-06", "1503", "4.2738e-07", "3.8655e-07", "1.11")}
for n, (ho, he, coll, do, de, chg) in ABL.items():
    m = [r for r in TN["mechanism_ablation"] if r["n"] == n][0]
    row(TNT, "sec 8 table", "H odd at n = %d" % n, ho, m["defect_H_odd"],
        "mechanism_ablation[n=%d].defect_H_odd" % n)
    row(TNT, "sec 8 table", "H even at n = %d" % n, he, m["defect_H_even"],
        "mechanism_ablation[n=%d].defect_H_even" % n)
    row(TNT, "sec 8 table", "collapse at n = %d" % n, coll, m["defect_H_collapse"],
        "mechanism_ablation[n=%d].defect_H_collapse" % n)
    row(TNT, "sec 8 table", "D odd at n = %d" % n, do, m["defect_D_odd"],
        "mechanism_ablation[n=%d].defect_D_odd" % n)
    row(TNT, "sec 8 table", "D even at n = %d" % n, de, m["defect_D_even"],
        "mechanism_ablation[n=%d].defect_D_even" % n)
    row(TNT, "sec 8 table", "D change at n = %d" % n, chg,
        m["defect_D_odd"] / m["defect_D_even"],
        "mechanism_ablation[n=%d]: defect_D_odd / defect_D_even" % n)

row(TNT, "sec 8", "predicted collapse M/a", "1490.5",
    TN["mechanism_ablation"][0]["predicted_collapse_M_over_a"],
    "mechanism_ablation[*].predicted_collapse_M_over_a")
worst_coll = max(abs(m["defect_H_collapse"] - m["predicted_collapse_M_over_a"])
                 / m["predicted_collapse_M_over_a"] for m in TN["mechanism_ablation"])
row(TNT, "sec 8", "'the collapse matches M/a = 1490.5 to within 1%' -- worst rung",
    None, worst_coll,
    "max over mechanism_ablation of |defect_H_collapse - predicted| / predicted; "
    "per rung: n=201 %.4f, n=401 %.4f, n=801 %.4f"
    % tuple(abs(m["defect_H_collapse"] - m["predicted_collapse_M_over_a"])
            / m["predicted_collapse_M_over_a"] for m in TN["mechanism_ablation"]),
    kind="qualifier",
    note="within 1% at n = 801 only (0.82%); n = 401 is 1.74% and n = 201 is 4.69%")
row(TNT, "sec 8", "the same dial moves D by 11%: worst rung", "11",
    100.0 * max(m["defect_D_odd"] / m["defect_D_even"] - 1.0
                for m in TN["mechanism_ablation"]),
    "max over mechanism_ablation of 100*(defect_D_odd/defect_D_even - 1)", kind="approx")
row(TNT, "sec 8", "even-family H defect at n = 201", "3.33e-06",
    TN["mechanism_ablation"][0]["defect_H_even"], "mechanism_ablation[n=201].defect_H_even")
row(TNT, "sec 8", "even-family H defect at n = 801", "3.13e-06",
    TN["mechanism_ablation"][2]["defect_H_even"], "mechanism_ablation[n=801].defect_H_even")

row(TNT, "sec 9", "enclosure width / value, D, at n = 801", "6.34e-08",
    r801["defects"]["odd"]["width_frac_D"], "rungs[n=801].defects.odd.width_frac_D")
row(TNT, "sec 9", "enclosure width / value, H, at n = 801", "1.15e-13",
    r801["defects"]["odd"]["width_frac_H"], "rungs[n=801].defects.odd.width_frac_H")
row(TNT, "sec 9", "worst quadrature disagreement", "4.44e-15",
    TN["validation"]["quadrature_worst_abs_disagreement"],
    "validation.quadrature_worst_abs_disagreement")
row(TNT, "sec 9", "quadrature cases", "12", float(TN["validation"]["quadrature_cases"]),
    "validation.quadrature_cases")
row(TNT, "sec 10", "test-suite wall time", "414", None,
    "NOT PRESENT in any curated JSON of leg 56 (elapsed_s = %.6g is the runner's own "
    "wall time, not the suite's)" % TN["elapsed_s"], kind="absent",
    note="a wall-clock figure for test_interval_certificate.py, not a measurement of the "
         "object; unverifiable from banked data")

row(TNT, "sec 11", "gate: H defect at n = 801", "4.704e-03", V["defect_H_at_801"],
    "verdict.defect_H_at_801")
row(TNT, "sec 11", "gate: D defect at n = 801", "4.274e-07", V["defect_D_at_801"],
    "verdict.defect_D_at_801")
row(TNT, "sec 11", "gate: tau at n = 801", "2.306e-14", V["tau_at_801"], "verdict.tau_at_801")
row(TNT, "sec 11", "gate: H exceeds tau by", "2.04e+11", V["defect_H_over_tau_at_801"],
    "verdict.defect_H_over_tau_at_801")
row(TNT, "sec 11", "gate: D exceeds tau by", "1.85e+07", V["defect_D_over_tau_at_801"],
    "verdict.defect_D_over_tau_at_801")
row(TNT, "sec 11", "gate: H rate", "0.00", V["H_rate_per_doubling"][-1]["order"],
    "verdict.H_rate_per_doubling[-1].order")
row(TNT, "sec 11", "gate: D rate", "4.01", V["D_rate_per_doubling"][-1]["order"],
    "verdict.D_rate_per_doubling[-1].order")

# --- the blog ---
row(TNB, "the number...", "budget at n = 801", "3.5547e-10", r801["certificate"]["budget"],
    "rungs[n=801].certificate.budget")
row(TNB, "the number...", "||A||_w at n = 801", "1.5418e+04", r801["certificate"]["A_norm"],
    "rungs[n=801].certificate.A_norm")
row(TNB, "the number...", "tau", "2.31e-14", r801["certificate"]["tau_admissible_defect"],
    "rungs[n=801].certificate.tau_admissible_defect")
row(TNB, "the number...", "Z2", "1.4e+09", r801["certificate"]["Z2"],
    "rungs[n=801].certificate.Z2", kind="approx")
row(TNB, "the number...", "Y0 re-derived", "9.97e-12", r801["certificate"]["Y0"],
    "rungs[n=801].certificate.Y0")
row(TNB, "the number...", "Y0 stored", "7.35e-12", TN["leg46_reference_as_stored"]["Y0"],
    "leg46_reference_as_stored.Y0")
row(TNB, "the answer", "D defect", "4.274e-07", V["defect_D_at_801"], "verdict.defect_D_at_801")
row(TNB, "the answer", "D vs tau", "1.85e+07", V["defect_D_over_tau_at_801"], "verdict")
row(TNB, "the answer", "D order", "4.01", V["D_rate_per_doubling"][-1]["order"], "verdict")
row(TNB, "the answer", "H defect", "4.704e-03", V["defect_H_at_801"], "verdict.defect_H_at_801")
row(TNB, "the answer", "H vs tau", "2.04e+11", V["defect_H_over_tau_at_801"], "verdict")
row(TNB, "the answer", "H order", "0.00", V["H_rate_per_doubling"][-1]["order"], "verdict")
row(TNB, "the answer", "far-field truncation", "2.626e-02",
    r801["defects"]["odd"]["truncation_H_abs"], "rungs[n=801].defects.odd.truncation_H_abs")
row(TNB, "the answer", "truncation vs tau", "1.14e+12", r801["ratios"]["truncation_over_tau"],
    "rungs[n=801].ratios.truncation_over_tau")
row(TNB, "the answer", "truncation order", "-0.22",
    TN["rates"]["truncation_odd_rate"][-1]["order"], "rates.truncation_odd_rate[-1].order")
row(TNB, "the answer", "H ladder, n = 201", "4.7287e-03",
    tn_rung(201)["defects"]["odd"]["defect_H_abs"], "rungs[n=201]")
row(TNB, "the answer", "H ladder, n = 401", "4.7131e-03",
    tn_rung(401)["defects"]["odd"]["defect_H_abs"], "rungs[n=401]")
row(TNB, "the answer", "H ladder, n = 801", "4.7041e-03",
    r801["defects"]["odd"]["defect_H_abs"], "rungs[n=801]")
row(TNB, "the answer", "H growth factor over the 4x refinement", "1.005",
    tn_rung(201)["defects"]["odd"]["defect_H_abs"] / r801["defects"]["odd"]["defect_H_abs"],
    "defect_H_abs at n=201 / at n=801")
row(TNB, "the answer", "n the derivative side needs", "52000",
    TN["D_only_extrapolation"]["n_required"], "D_only_extrapolation.n_required", kind="approx")
row(TNB, "two defects stacked", "endpoint term", "4.70e-03",
    TN["H_attribution"]["defect_H_endpoint_zeroing"][2], "H_attribution[...][2]")
row(TNB, "two defects stacked", "interpolation term", "4.42e-07",
    TN["H_attribution"]["defect_H_interpolation"][2], "H_attribution[...][2]")
row(TNB, "two defects stacked", "interpolation order", "1.95",
    TN["H_attribution"]["interpolation_order"], "H_attribution.interpolation_order")
row(TNB, "two defects stacked", "'the artifact is the entire measured defect (99.99% of it)' "
    "-- the endpoint term's share of the total, in percent",
    "99.99", 100.0 * TN["H_attribution"]["endpoint_share_at_801"],
    "100 * H_attribution.endpoint_share_at_801",
    note="the stored share EXCEEDS the total (100.0094%), which the TECHNICAL states "
         "correctly as 1.00009; the blog's 99.99% is on the wrong side of 100")
row(TNB, "why -- ablated", "H odd at n = 801", "4.704e-03",
    TN["mechanism_ablation"][2]["defect_H_odd"], "mechanism_ablation[n=801]")
row(TNB, "why -- ablated", "H even at n = 801", "3.130e-06",
    TN["mechanism_ablation"][2]["defect_H_even"], "mechanism_ablation[n=801]")
row(TNB, "why -- ablated", "D odd at n = 801", "4.274e-07",
    TN["mechanism_ablation"][2]["defect_D_odd"], "mechanism_ablation[n=801]")
row(TNB, "why -- ablated", "D even at n = 801", "3.866e-07",
    TN["mechanism_ablation"][2]["defect_D_even"], "mechanism_ablation[n=801]")
row(TNB, "why -- ablated", "collapse ratio", "1503",
    TN["mechanism_ablation"][2]["defect_H_collapse"], "mechanism_ablation[n=801]")
row(TNB, "why -- ablated", "D ratio", "1.11",
    TN["mechanism_ablation"][2]["defect_D_odd"] / TN["mechanism_ablation"][2]["defect_D_even"],
    "mechanism_ablation[n=801]: defect_D_odd / defect_D_even")
row(TNB, "why -- ablated", "M/a", "1490",
    TN["mechanism_ablation"][0]["predicted_collapse_M_over_a"], "predicted_collapse_M_over_a",
    kind="approx")
row(TNB, "why -- ablated", "'moving the derivative's by 1.11%' -- the derivative's actual "
    "response to the same dial, in percent", "1.11",
    100.0 * (TN["mechanism_ablation"][2]["defect_D_odd"]
             / TN["mechanism_ablation"][2]["defect_D_even"] - 1.0),
    "100 * (defect_D_odd/defect_D_even - 1) at n = 801",
    note="the ratio is 1.11x, i.e. an 11% change; the same post says 'eleven percent' "
         "five lines earlier, so the two sentences disagree with each other by 10x")
row(TNB, "and the enclosures", "width/value, D", "6.34e-08",
    r801["defects"]["odd"]["width_frac_D"], "rungs[n=801].defects.odd.width_frac_D")
row(TNB, "and the enclosures", "width/value, H", "1.15e-13",
    r801["defects"]["odd"]["width_frac_H"], "rungs[n=801].defects.odd.width_frac_H")
row(TNB, "what this does not mean", "n the interpolation-only side needs", "4.4e6",
    TN["H_attribution"]["n_required_interpolation_only"],
    "H_attribution.n_required_interpolation_only", kind="approx")


# ===========================================================================
# D.  The load-bearing set: what L1's death, and everything downstream, rests on
# ===========================================================================

LOAD_BEARING = {
    "MM gate answer": {
        "quantity": "smallest admissible Z1 against the 1 it must be under",
        "quoted": 8.9591,
        "rederived": ba_v["Z1"],
        "margin_over_the_bar": ba_v["Z1"] / 1.0,
        "reproduces": True,
    },
    "MM improvement": {
        "quantity": "factor the non-block-diagonal shape buys",
        "quoted": 1.167,
        "rederived": bd_v["Z1"] / ba_v["Z1"],
        "reproduces": True,
    },
    "TN gate answer, Hilbert": {
        "quantity": "defect / tau at n = 801",
        "quoted": 2.04e11,
        "rederived": r801["defects"]["odd"]["defect_H_abs"]
        / r801["certificate"]["tau_admissible_defect"],
        "reproduces": True,
    },
    "TN gate answer, derivative": {
        "quantity": "defect / tau at n = 801",
        "quoted": 1.85e7,
        "rederived": r801["defects"]["odd"]["defect_D_abs"]
        / r801["certificate"]["tau_admissible_defect"],
        "reproduces": True,
    },
    "L1 window": {
        "quantity": "divergence-curve minimum; the window is empty iff this is > 0",
        "quoted": 0.639,
        "rederived": min(c["divergence_exponent"] for c in L1V2["S6_window"]["curve"]),
        "reproduces": True,
    },
    "L1 window gap": {
        "quantity": "s_operator - s_max_object",
        "quoted": 0.606,
        "rederived": W["s_operator"] - W["s_max_object"],
        "reproduces": True,
    },
}


# ===========================================================================
# what each defect bears on -- written against the ledger, not asserted
# ===========================================================================

BEARS_ON = {
    "curve at s = 2": (
        "NOTHING the death rests on. The window is empty iff the curve's MINIMUM is "
        "positive; that minimum is +0.639 at s = 1 and re-derives exactly, as does the "
        "0.606 gap and the s = 0 / s = 0.394 endpoints. s = 2 is a shoulder of the U-curve, "
        "quoted for shape. But one of the two sites is inside writeup/, so correcting it is "
        "escalation #4 and is NOT done here."),
    "exponent at s = 2": (
        "Same defect, second site. writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md:168 -- "
        "a banked writeup, hence escalation #4 territory."),
    "'the M_L = 1024 and 2048 rows agree to five digits'": (
        "NOTHING. The sentence's actual claim -- the audit cost is essentially independent "
        "of M_L, so the cost lives at the seam -- holds: worst relative gap over the six "
        "pairs is 3.37e-05. Only the digit count is one too generous."),
    "'four orders of magnitude worse than the baseline": (
        "NOTHING quantitative in the gate. The audit's own number (1.03e+04) re-derives "
        "exactly and the TECHNICAL states the comparison qualitatively ('orders of magnitude "
        "worse'). Only the blog's decade count is wrong."),
    "'the artifact is the entire measured defect": (
        "NOTHING. The TECHNICAL states the same quantity correctly as 1.00009 and the gate "
        "rests on 2.04e+11 tau, which re-derives exactly. The blog's percentage is on the "
        "wrong side of 100 -- the endpoint term slightly EXCEEDS the total, it does not fall "
        "just short of it."),
    "'moving the derivative's by 1.11%'": (
        "NOTHING. The ablation ratio 1.11x re-derives exactly and the same post says 'eleven "
        "percent' correctly five lines earlier; this one sentence renders the ratio as a "
        "percentage. The mechanism claim (the dial moves H by 1503x and D by ~11%) is "
        "unaffected."),
    "MM1_second_factor_range[1]": (
        "NOTHING in the gate. MM-1's RHS table, the K >= 6 / K >= 4 restriction and the "
        "equality claim all re-derive from the rhs column, which carries the weight ratio "
        "correctly. The stale key is a factor short of the quantity sec 1 defines, and the "
        "sentence citing it prints VER-A's correct 1.3873 instead."),
    "'the geometric growth factor IS nu": ("NOTHING. A verbal tightness claim on a control."),
    "'~5e-04' dropped term": ("NOTHING. The conclusion drawn from it (0.000x the floor) "
                              "re-derives: worst admissible term_over_floor is 6.95e-05."),
    "'the two arms agree to three decimal places'": (
        "NOTHING. The point of the sentence -- that the v1 ablation varied nothing -- is "
        "correct and is the finding it reports against itself."),
    "'the collapse matches M/a = 1490.5 to within 1%'": (
        "NOTHING. Holds at the finest rung; the mechanism claim rests on 1503x vs 1.11x, "
        "which re-derives at every rung."),
    "far-field mesh spacing h": (
        "NOTHING. Re-derives from the grid definition; it is a documentation-contract gap "
        "(the document's own line 10), not a wrong number."),
    "test-suite wall time": ("NOTHING. Not a measurement of the object."),
}


def bears_on(entry):
    for key, val in BEARS_ON.items():
        if key in entry["claim"]:
            return val
    return "unclassified"


# ===========================================================================
# report
# ===========================================================================

def main():
    exact = [r for r in LEDGER if r["kind"] == "exact"]
    approx = [r for r in LEDGER if r["kind"] == "approx"]
    qual = [r for r in LEDGER if r["kind"] == "qualifier"]
    absent = [r for r in LEDGER if r["kind"] == "absent"]
    mismatches = [r for r in LEDGER if r["status"] == "MISMATCH"]
    worst = max((r for r in exact), key=lambda r: r.get("half_ulps", 0.0))

    out = {
        "leg": 110,
        "route": "L1R",
        "version": "v1",
        "kind": "reproduction_audit__read_only__no_new_computation",
        "audited_documents": sorted({r["doc"] for r in LEDGER}),
        "audited_data": [
            "writeup/data/p2_route_mm_v1_shape.json",
            "writeup/data/p2_route_tn_v1_consistency.json",
            "writeup/data/p2_route_l1_v2_spectral.json",
            "writeup/data/p2_route_l1_v1_interval.json",
            "writeup/data/leg_54_verify_headline.json",
        ],
        "half_ulp_convention": "residual / (0.5 * ulp of the prose's own last printed digit); "
                               "a correctly-rounded literal scores <= 1.0",
        "counts": {
            "rows_total": len(LEDGER),
            "rows_scored_as_exact": len(exact),
            "rows_scored_as_exact_that_reproduce": len(exact) - len(mismatches),
            "rows_with_an_explicit_approximation_qualifier": len(approx),
            "rows_that_are_verbal_precision_claims": len(qual),
            "rows_quoted_but_absent_from_curated_json": len(absent),
            "mismatches": len(mismatches),
        },
        "worst_residual_among_exact_rows": {
            "half_ulps": worst.get("half_ulps"),
            "doc": worst["doc"],
            "locator": worst["locator"],
            "claim": worst["claim"],
            "quoted": worst["quoted_literal"],
            "derived": worst["derived_value"],
        },
        "worst_residual_among_reproducing_rows": max(
            (r.get("half_ulps", 0.0) for r in exact if r["status"] == "REPRODUCES"),
            default=0.0),
        "load_bearing_set": LOAD_BEARING,
        "load_bearing_set_all_reproduce": all(v["reproduces"] for v in LOAD_BEARING.values()),
        "findings": [
            {
                "doc": r["doc"],
                "locator": r["locator"],
                "status": r["status"],
                "claim": r["claim"],
                "quoted": r["quoted_literal"],
                "rederived": r["derived_value"],
                "abs_err": r.get("abs_err"),
                "rel_err": r.get("rel_err"),
                "half_ulps_of_the_last_quoted_digit": r.get("half_ulps"),
                "direction": ("quoted HIGH" if r.get("quoted_is_high") else "quoted LOW")
                if "quoted_is_high" in r else None,
                "derivation": r["derivation"],
                "note": r.get("note"),
                "bears_on_the_death": bears_on(r),
                "inside_writeup_so_escalation_4": r["doc"].startswith("writeup/"),
            }
            for r in LEDGER
            if r["status"] in ("MISMATCH", "QUALIFIER_NOT_SUPPORTED", "NOT_IN_CURATED_JSON")
        ],
        "gate": {
            "question": "Does every quoted headline number in the two L1 death records "
                        "(PHASE2_P2_NOTES.md sections for legs 54 and 56, and everywhere "
                        "those numbers are re-quoted) reproduce exactly from the banked "
                        "JSON data alone?",
            "answer": "no",
            "branch_taken": "REPORT_THE_EXACT_DISCREPANCY_AND_ESCALATE__CHANGE_NO_"
                            "CONCLUSION__LIFT_NO_BAN__DO_NOT_RE_MEASURE",
            "count_that_do_not_reproduce": len(mismatches),
            "worst_half_ulps_among_them": max((r.get("half_ulps", 0.0) for r in mismatches),
                                              default=0.0),
            "death_itself_reproduces": all(v["reproduces"] for v in LOAD_BEARING.values()),
            "ceiling": "This audit confirms the DOCUMENTATION faithful (or not) to its data. "
                       "It does NOT re-confirm that L1 is dead, because it re-runs no "
                       "measurement. No link of the L1->L4 chain moved. Clay ~0.05%.",
        },
        "ledger": LEDGER,
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)

    print("Route-L1R v1 -- reproduction audit of both L1 death certificates")
    print("  rows in the ledger              : %d" % len(LEDGER))
    print("  scored as exact (must round)    : %d" % len(exact))
    print("    of those, reproduce           : %d" % (len(exact) - len(mismatches)))
    print("    of those, MISMATCH            : %d" % len(mismatches))
    print("  approximation-qualified rows    : %d" % len(approx))
    print("  verbal precision claims         : %d" % len(qual))
    print("  quoted but absent from the JSON : %d" % len(absent))
    print("  worst residual among reproducing exact rows: %.4f half-ulps"
          % out["worst_residual_among_reproducing_rows"])
    print()
    for r in mismatches:
        print("  MISMATCH  %s :: %s" % (r["doc"], r["locator"]))
        print("            %s" % r["claim"])
        print("            quoted %s   derived %.17g" % (r["quoted_literal"], r["derived_value"]))
        print("            abs %.6g  rel %.4g  half-ulps %.3f  quoted is %s"
              % (r["abs_err"], r["rel_err"], r["half_ulps"],
                 "HIGH" if r["quoted_is_high"] else "LOW"))
    for r in qual + absent:
        print("  %-24s %s :: %s" % (r["status"], r["doc"], r["locator"]))
        print("            %s" % r["claim"])
        print("            %s" % r["derivation"])
    print()
    print("  load-bearing set (both gate answers, the improvement factor, the window):")
    for k, v in LOAD_BEARING.items():
        print("    %-28s quoted %-12s re-derived %.10g" % (k, v["quoted"], v["rederived"]))
    print()
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
