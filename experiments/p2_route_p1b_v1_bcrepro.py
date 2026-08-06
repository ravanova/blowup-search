"""Route-P1B v1 (leg 256): Breden-Chu's Theorem 42, reproduced end to end, on their ground.

WHAT THIS RUNS, AND WHY IT IS THE CHEAPEST POSSIBLE PHASE-1 KILL TEST
-----------------------------------------------------------------------------
Before any Phase-1 construction is posable, one question has to be answered: can this
repository drive Breden-Chu's machinery AT ALL, on a result they already published?
This is leg 61's Kawahara shape (`experiments/p2_route_ka_v1_kawahara.py`) applied to
the Grade-A technique of leg 174's empty occupancy cell.

The result reproduced -- chosen and stated in `writeup/novelty/leg_256.md` BEFORE this
file existed -- is **Theorem 42** of arXiv:2404.04054v2, the generalised viscous
Burgers self-similar profile.  It is the paper's ONLY result with a genuine first-order
term f(x, u, grad u), and the one Remark 40 ("terms like (u.grad)u could in principle
also be handled in dimension d in {2,3}") is attached to.

  L u - u/4 + u^2 d_x u = 0,   x >= 0,   L = -d_xx - (x/2)d_x,   Neumann at 0

  their published constants at n = 1500:
     Y = 0.00075636391   Z1 = 0.065135932   Z2 = 343.3917   Z3 = 556.478
     deltabar = 0.00271646316,   enclosure ||u* - ubar||_{H^2(mu)} <= 1e-3

BAN DISCIPLINE
-----------------------------------------------------------------------------
Everything here lives in Breden-Chu's own weighted-Sobolev setting: a HILBERT norm
||L.||_{L^2(mu)}, the half-Hermite/Laguerre basis, Poincare tail control on an
UNBOUNDED domain.  None of the three realizations `plan_of_record.py` names dead
(ell^1_w coefficients, collocation, origin-H^2) is touched.  This leg does NOT lift
the ban and NO Phase-1 construction runs under its authority.  See
`solver/bc_weighted_sobolev.py`'s header and `writeup/novelty/leg_256.md` section 1.

ARITHMETIC, DECLARED BEFORE THE NUMBERS (standing discipline 75)
-----------------------------------------------------------------------------
Breden-Chu prove Theorem 42 in interval arithmetic over 16384-bit BigFloat.  This
environment has numpy only.  **Everything below is float64: this reproduces their
certificate's CONSTANTS, not their proof.**  Nothing here is a rigorous enclosure.
The reproduction's own resolution is MEASURED, not assumed, by three gates whose
magnitudes are reported first, before any constant is quoted:
  * their own two exact rational quadrature identities (669/31250 and -29/324),
  * <psi_a, psi_b> = delta_ab across ALL modes a,b <= n,
  * sum_i w_i = Gamma(alpha+1) for each Gauss-Laguerre rule.

WHAT MAKES THIS INDEPENDENT RATHER THAN A RE-RUN OF THEIR NOTEBOOK
-----------------------------------------------------------------------------
Their `ubar` is never used to produce the headline numbers.  The approximate solution
is found from scratch: eq. (54) is shot as an ODE, the admissible amplitude u(0) is
bisected out of the two-sided far-field behaviour, the profile is projected onto the
basis, and Newton is run up a continuation ladder in n.  Their stored `ubar` enters
ONLY as an ablation (section 6), whose entire purpose is to separate "our ubar differs
from theirs" from "our bounds differ from theirs".

THE ABLATIONS EXIST TO KILL EXPLANATIONS, NOT TO DECORATE
-----------------------------------------------------------------------------
  * bounds on THEIR ubar vs on OURS -- localises any gap to the solution or to the
    bound formulas;
  * their loose analytic sup bounds vs the sharp measured sup -- Z2 and Z3 are built
    from ||psi_m||_inf bounds their own Remark 41 states more sharply than their code
    uses, and this measures what that costs;
  * a resolution ladder in n -- says whether a constant is resolution-set or not;
  * a displaced ubar -- an over-optimistic certificate is one that does not notice.
"""

import json
import math
import os
import subprocess
import sys
import tempfile
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import bc_weighted_sobolev as bc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_p1b_v1_bcrepro.json")

PUB = bc.BC_THEOREM_42
N_HEADLINE = 1500
LADDER = (100, 200, 400, 800, 1500)

# Their `ubar`, at the commit pinned in writeup/novelty/leg_256.md.  Used for the
# ablation ONLY -- never for the headline numbers.
UBAR_URL = ("https://raw.githubusercontent.com/Huggzz/Hermite-Laguerre_proofs/"
            + PUB["code_commit"] + "/Burger/ubar")


def decades(x, y):
    """log10(x/y) -- the magnitude this repository reports instead of a boolean."""
    if x <= 0 or y <= 0 or not np.isfinite(x) or not np.isfinite(y):
        return None
    return float(np.log10(x / y))


def fetch_their_ubar(n):
    """Their stored coefficients, or None if egress is blocked.

    Julia `Serialization` of a Vector{Float64}: a 16-byte header then 1501 little-endian
    doubles (verified against the file length, 12024 = 16 + 1501*8).  Read defensively --
    if anything about the layout is not exactly that, return None rather than guess.
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".ubar", delete=False) as fh:
            path = fh.name
        rc = subprocess.run(["curl", "-sSL", "--max-time", "60", "-o", path, UBAR_URL],
                            capture_output=True)
        if rc.returncode != 0:
            return None, "curl failed: " + rc.stderr.decode()[:200]
        raw = open(path, "rb").read()
        os.unlink(path)
        if len(raw) != 16 + 1501 * 8:
            return None, "unexpected length %d" % len(raw)
        a = np.frombuffer(raw, dtype="<f8", count=1501, offset=16).copy()
        if not np.all(np.isfinite(a)) or abs(a[0] - 1.5850701039153166) > 1e-12:
            return None, "leading coefficient does not match the pinned file"
        return a[:n + 1], None
    except Exception as exc:                                   # pragma: no cover
        return None, repr(exc)


def _y_threshold(Z1, Z2, Z3, mult):
    """The largest Y for which delta = mult*Y/(1-Z1) satisfies P(delta) < 0.

    Substituting delta = kY with k = mult/(1-Z1) into Corollary 21's P gives
    P = Y[(Z3/6)k^3 Y^2 + (Z2/2)k^2 Y - (mult - 1)], so the multiplier validates
    exactly below the positive root of that quadratic.
    """
    k = mult / (1.0 - Z1)
    r = np.roots([Z3 / 6.0 * k ** 3, Z2 / 2.0 * k ** 2, -(mult - 1.0)])
    pos = [x.real for x in r if abs(x.imag) < 1e-14 and x.real > 0]
    return float(min(pos)) if pos else None


def _worst_ratio_key(ratios):
    """Which comparison sits furthest from 1, in either direction."""
    usable = {k: v for k, v in ratios.items() if v and v > 0 and np.isfinite(v)}
    if not usable:
        return None
    return max(usable, key=lambda k: abs(math.log(usable[k])))


def constants_row(b, verdict):
    """One comparison row: our constant, theirs, the ratio, in magnitudes."""
    row = {}
    for key, pub_key in (("Y", "Y_published"), ("Z1", "Z1_published"),
                         ("Z2", "Z2_published"), ("Z3", "Z3_published")):
        ours, theirs = b[key], PUB[pub_key]
        row[key] = {"ours": ours, "theirs": theirs,
                    "ratio_ours_over_theirs": ours / theirs,
                    "decades": decades(ours, theirs)}
    db = verdict.get("delta_bar")
    row["delta_bar"] = {"ours": db, "theirs": PUB["deltabar_published"],
                        "ratio_ours_over_theirs": (db / PUB["deltabar_published"]
                                                   if db and np.isfinite(db) else None)}
    for key, pub_key in (("op_norm_LAL", "op_norm_LAL_implied"),
                         ("sup_combination", "sup_combination_implied")):
        row[key] = {"ours": b[key], "theirs_implied": PUB[pub_key],
                    "ratio_ours_over_theirs": b[key] / PUB[pub_key]}
    return row


def main():
    out = {"published": dict(PUB)}
    t_all = time.time()

    # =====================================================================
    # 0.  THE ARITHMETIC'S OWN RESOLUTION -- reported BEFORE any constant
    # =====================================================================
    print("ROUTE-P1B v1 -- Breden-Chu Theorem 42, reproduced")
    print("  arithmetic: float64 (theirs: interval over 16384-bit BigFloat)")
    print("  -- quadrature gates first, before any constant is quoted --")
    sys.stdout.flush()

    t = time.time()
    rules = bc.make_rules(N_HEADLINE)
    build_s = time.time() - t
    gates = {
        "n": N_HEADLINE,
        "build_seconds": build_s,
        "weight_normalisation": {k: bc.check_weight_normalisation(rules[k])
                                 for k in ("six", "four", "two")},
        "exact_rational_identities": bc.check_quadrature_identities(rules),
        "orthonormality_all_modes": bc.check_orthonormality(rules),
        "what_these_license": (
            "the largest of these is the reproduction's RESOLUTION: a float64 "
            "reproduction of a BigFloat interval proof can be trusted to about this "
            "relative size and no further.  Every ratio reported below must be read "
            "against it."),
    }
    out["quadrature_gates"] = gates
    res = max(gates["exact_rational_identities"]["six_product_rel_err"],
              gates["exact_rational_identities"]["four_product_rel_err"],
              gates["orthonormality_all_modes"]["max_abs_offdiag_and_diag_defect"])
    out["reproduction_resolution"] = res
    print(f"  quadrature build {build_s:.1f}s")
    print(f"  exact identity 669/31250 : rel err "
          f"{gates['exact_rational_identities']['six_product_rel_err']:.3e}")
    print(f"  exact identity -29/324   : rel err "
          f"{gates['exact_rational_identities']['four_product_rel_err']:.3e}")
    print(f"  <psi_a,psi_b>=delta_ab   : max defect "
          f"{gates['orthonormality_all_modes']['max_abs_offdiag_and_diag_defect']:.3e}")
    print(f"  => reproduction resolution {res:.2e} relative")
    sys.stdout.flush()

    # =====================================================================
    # 1.  AN INDEPENDENT APPROXIMATE SOLUTION -- their ubar is not used here
    # =====================================================================
    t = time.time()
    a0 = bc.find_amplitude()
    xs, us = bc.shoot_profile(a0, x_max=12.0, h=1e-4)
    shoot_s = time.time() - t
    out["independent_amplitude"] = {
        "u0_by_shooting": a0,
        "seconds": shoot_s,
        "method": ("RK4 on u'' + (x/2)u' + u/4 - u^2 u' = 0, u'(0)=0, bisecting u(0) on "
                   "the sign change of u(9); the generic ODE solution decays only like "
                   "x^{-1/2} and is not in H^2(mu), the admissible one like e^{-x^2/4}"),
        "u_at_4": float(us[int(4.0 / 1e-4)]),
        "u_at_9": float(us[int(9.0 / 1e-4)]),
    }
    print(f"  independent u(0) = {a0:.12f}   (shooting, {shoot_s:.1f}s)")
    sys.stdout.flush()

    # =====================================================================
    # 2.  THE CONTINUATION LADDER -- also the resolution sweep
    # =====================================================================
    seed = bc.project_profile(xs, us, LADDER[0])
    ladder = []
    a = None
    for n in LADDER:
        t = time.time()
        rl = rules if n == N_HEADLINE else bc.make_rules(n)
        pr = bc.BurgersSelfSimilar(n, rl)
        if a is None:
            start = seed
        else:
            start = np.zeros(n + 1)
            start[:len(a)] = a                       # prolong by zero-padding
        a, hist = pr.newton(start)
        b = bc.bounds(pr, a)
        v = bc.radii_verdict(b["Y"], b["Z1"], b["Z2"], b["Z3"])
        ladder.append({
            "n": n, "seconds": time.time() - t,
            "newton_residual_history": [float(h) for h in hist],
            "final_residual_H2": float(hist[-1]),
            "bounds": {k: b[k] for k in
                       ("Y", "Z1", "Z2", "Z3", "Zbar11", "Zbar12", "Zbar21", "Zbar22",
                        "op_norm_LAL", "sup_ubar", "sup_dubar", "sup_combination",
                        "ubar_at_zero", "S_n", "Y_finite_part", "Y_tail_part",
                        "nonlinearity_norm")},
            "verdict": v,
            "coefficient_tail": float(abs(a[-1])),
        })
        print(f"  n={n:5d}  newton->{hist[-1]:.2e}  Y={b['Y']:.5e}  Z1={b['Z1']:.5e}  "
              f"Z2={b['Z2']:.4f}  Z3={b['Z3']:.4f}  closes={v['closes']}  "
              f"({ladder[-1]['seconds']:.0f}s)")
        sys.stdout.flush()
        if n != N_HEADLINE:
            del rl, pr
    out["ladder"] = ladder

    n = N_HEADLINE
    pr = bc.BurgersSelfSimilar(n, rules)
    a_ours = a
    b_ours = bc.bounds(pr, a_ours)
    v_ours = bc.radii_verdict(b_ours["Y"], b_ours["Z1"], b_ours["Z2"], b_ours["Z3"])
    out["headline"] = {"n": n, "bounds": b_ours, "verdict": v_ours,
                       "comparison": constants_row(b_ours, v_ours)}

    # =====================================================================
    # 3.  THE TWO READINGS, exactly as pre-committed in writeup/novelty/leg_256.md
    # =====================================================================
    enc = PUB["enclosure_published"]
    P_at_enc = bc.radii_polynomial(b_ours["Y"], b_ours["Z1"], b_ours["Z2"],
                                   b_ours["Z3"], enc)
    dmin, dbar = v_ours.get("delta_min"), v_ours.get("delta_bar")
    reading_a = bool(v_ours["closes"] and np.isfinite(dmin)
                     and dmin < enc < dbar)
    ratios = {k: out["headline"]["comparison"][k]["ratio_ours_over_theirs"]
              for k in ("Y", "Z1", "Z2", "Z3")}
    ratios["delta_bar"] = out["headline"]["comparison"]["delta_bar"][
        "ratio_ours_over_theirs"]
    within2 = {k: (r is not None and 0.5 <= r <= 2.0) for k, r in ratios.items()}
    reading_b = all(within2.values())
    out["gate"] = {
        "reading_A_their_enclosure_is_a_certified_radius_of_our_polynomial": reading_a,
        "our_certified_interval": [dmin, dbar],
        "their_published_enclosure": enc,
        "our_P_at_their_enclosure": float(P_at_enc),
        "their_enclosure_over_our_delta_min": (enc / dmin if dmin and
                                               np.isfinite(dmin) else None),
        "our_delta_bar_over_their_enclosure": (dbar / enc if dbar and
                                               np.isfinite(dbar) else None),
        "reading_B_all_constants_within_2x": reading_b,
        "reading_B_ratios_ours_over_theirs": ratios,
        "reading_B_within_2x": within2,
        "worst_ratio_key": _worst_ratio_key(ratios),
        "precommitted_in": "writeup/novelty/leg_256.md section 6",
    }

    # =====================================================================
    # 4.  THEIR PUBLISHED CONSTANTS, AUDITED ON THEIR OWN TERMS
    #     (pre-registered in writeup/novelty/leg_256.md section 8)
    # =====================================================================
    pY, pZ1 = PUB["Y_published"], PUB["Z1_published"]
    pZ2, pZ3 = PUB["Z2_published"], PUB["Z3_published"]
    pv = bc.radii_verdict(pY, pZ1, pZ2, pZ3)
    their_dlo = pY / (1.0 - pZ1) * 1.17163            # their proof.ipynb cell 35
    needed = pv["delta_min"] / (pY / (1.0 - pZ1))
    out["their_constants_audit"] = {
        "delta_bar_recomputed": pv["delta_bar"],
        "delta_bar_published": PUB["deltabar_published"],
        "delta_bar_rel_err": abs(pv["delta_bar"] / PUB["deltabar_published"] - 1.0),
        "Q_at_delta_bar": float(-1.0 + pZ1 + pZ2 * pv["delta_bar"]
                                + pZ3 / 2.0 * pv["delta_bar"] ** 2),
        "delta_min_of_their_polynomial": pv["delta_min"],
        "P_at_their_published_enclosure_1e-3": float(
            bc.radii_polynomial(pY, pZ1, pZ2, pZ3, 1e-3)),
        "their_enclosure_over_their_delta_min": 1e-3 / pv["delta_min"],
        "their_delta_bar_over_their_enclosure": pv["delta_bar"] / 1e-3,
        "theorem_42_carried_by_its_own_printed_constants": bool(
            bc.radii_polynomial(pY, pZ1, pZ2, pZ3, 1e-3) < 0
            and pv["delta_min"] < 1e-3 < pv["delta_bar"]),
        "notebook_delta_lo_multiplier": 1.17163,
        "notebook_delta_lo": their_dlo,
        "P_at_notebook_delta_lo": float(
            bc.radii_polynomial(pY, pZ1, pZ2, pZ3, their_dlo)),
        "multiplier_actually_needed": needed,
        "multiplier_shortfall_factor": needed / 1.17163,
        # With delta = k Y, k = 1.17163/(1-Z1), P(delta) = Y[(Z3/6)k^3 Y^2
        # + (Z2/2)k^2 Y - 0.17163], so their multiplier validates iff Y is below the
        # positive root of that quadratic.  Solved here rather than quoted, so the
        # claim "print-rounding does not explain it" is checkable.
        "Y_at_which_their_multiplier_would_validate": _y_threshold(
            pZ1, pZ2, pZ3, 1.17163),
        "verdict": (
            "NOT a challenge to Theorem 42, and pre-registered as such in "
            "writeup/novelty/leg_256.md section 8 BEFORE this ran.  Theorem 42 claims "
            "||u*-ubar|| <= 1e-3, and 1e-3 lies strictly inside the certified interval "
            "of their own printed constants.  What is stale is the multiplier in the "
            "RELEASED NOTEBOOK's delta_lo, not anything in the paper."),
    }

    # =====================================================================
    # 5.  ABLATION: their loose analytic sup bounds vs the sharp measured sup
    # =====================================================================
    t = time.time()
    sup_sharp, dsup_sharp = bc.sharp_sup_psi(n)
    sup_bc, dsup_bc = bc.sup_psi_bounds(n)
    b_sharp = bc.bounds(pr, a_ours, sup_psi=sup_sharp, sup_dpsi=dsup_sharp)
    v_sharp = bc.radii_verdict(b_sharp["Y"], b_sharp["Z1"], b_sharp["Z2"],
                               b_sharp["Z3"])
    out["ablation_sup_bounds"] = {
        "seconds": time.time() - t,
        "their_bound_over_sharp_max_ratio_psi": float(np.max(sup_bc / sup_sharp)),
        "their_bound_over_sharp_max_ratio_dpsi": float(np.max(dsup_bc / dsup_sharp)),
        "remark_41_bound_pi_minus_quarter": math.pi ** -0.25,
        "sharp_max_sup_psi": float(np.max(sup_sharp)),
        "their_code_max_sup_psi": float(np.max(sup_bc)),
        "sup_ubar_theirs_formula": b_ours["sup_ubar"],
        "sup_ubar_sharp": b_sharp["sup_ubar"],
        "Z2_with_their_sup": b_ours["Z2"], "Z2_with_sharp_sup": b_sharp["Z2"],
        "Z2_ratio": b_sharp["Z2"] / b_ours["Z2"],
        "Z1_with_sharp_sup": b_sharp["Z1"],
        "delta_bar_with_sharp_sup": v_sharp["delta_bar"],
        "delta_min_with_sharp_sup": v_sharp["delta_min"],
        "what_it_tests": (
            "their Z2/Z3 are built from an analytic ||psi_m||_inf bound their own "
            "Remark 41 states more sharply (pi^{-1/4}) than their code uses.  This "
            "measures the cost, and shows whether any gap between our constants and "
            "theirs could be hiding there."),
    }

    # =====================================================================
    # 5b. ABLATION: WHICH sup-bound family reproduces their published Z1, Z2?
    #
    # Z1 and Z2 are the only Theorem-42 constants that depend on how ||psi_m||_inf and
    # ||d_x psi_m||_inf are bounded -- and the paper and its released code do not agree
    # on that.  Everything else (Y, Z3, ||L A L^{-1}||, ubar itself) is sup-independent.
    # So if exactly Z1 and Z2 differ from the published values, this is where it lives,
    # and this ablation says so with numbers instead of adjectives.
    # =====================================================================
    t = time.time()
    fams = bc.sup_bound_families(n)
    prov = {}
    for name, (sp, dsp) in fams.items():
        r = bc.recombine_with_sups(b_ours, a_ours, sp, dsp, n)
        rv = bc.radii_verdict(r["Y"], r["Z1"], r["Z2"], r["Z3"])
        prov[name] = {
            **r,
            "Z1_over_published": r["Z1"] / PUB["Z1_published"],
            "Z2_over_published": r["Z2"] / PUB["Z2_published"],
            "combination_over_published_implied":
                r["sup_combination"] / PUB["sup_combination_implied"],
            "delta_min": rv.get("delta_min"), "delta_bar": rv.get("delta_bar"),
            "closes": rv["closes"],
        }
        print(f"  sup family {name:24s} Z1/pub {prov[name]['Z1_over_published']:.4f}  "
              f"Z2/pub {prov[name]['Z2_over_published']:.4f}")
    sys.stdout.flush()
    out["ablation_sup_provenance"] = {
        "seconds": time.time() - t,
        "families": prov,
        "headline_family": "code_cells_16_17",
        "what_it_tests": (
            "Z1 and Z2 are the ONLY Theorem-42 constants that depend on the L^infty "
            "bounds for psi_m and d_xpsi_m.  arXiv:2404.04054v2 contains more than one "
            "such bound -- Remark 41's (sharp), proof.ipynb cells 16/17's (loose), and "
            "an alternative d_xpsi bound sitting commented out in cell 15.  This table "
            "says which family each published constant is consistent with, instead of "
            "attributing the gap by argument."),
    }

    # =====================================================================
    # 6.  ABLATION: the SAME bounds on THEIR ubar -- solution vs bounds
    # =====================================================================
    their_a, err = fetch_their_ubar(n)
    if their_a is None:
        out["ablation_their_ubar"] = {"available": False, "why": err}
        print(f"  ablation on their ubar SKIPPED: {err}")
    else:
        t = time.time()
        b_theirs = bc.bounds(pr, their_a)
        v_theirs = bc.radii_verdict(b_theirs["Y"], b_theirs["Z1"], b_theirs["Z2"],
                                    b_theirs["Z3"])
        d = a_ours - their_a
        out["ablation_their_ubar"] = {
            "available": True, "seconds": time.time() - t,
            "source": UBAR_URL,
            "coefficient_difference_H2_norm": float(
                np.linalg.norm(bc.eigenvalues(n) * d)),
            "coefficient_difference_l2": float(np.linalg.norm(d)),
            "coefficient_difference_max_abs": float(np.max(np.abs(d))),
            "our_ubar_at_zero": b_ours["ubar_at_zero"],
            "their_ubar_at_zero": b_theirs["ubar_at_zero"],
            "our_newton_residual_on_their_ubar_H2": float(
                np.linalg.norm(bc.eigenvalues(n) * pr.F(their_a))),
            "our_newton_residual_on_our_ubar_H2": float(
                np.linalg.norm(bc.eigenvalues(n) * pr.F(a_ours))),
            "bounds": {k: b_theirs[k] for k in ("Y", "Z1", "Z2", "Z3", "op_norm_LAL",
                                                "sup_ubar", "sup_dubar",
                                                "sup_combination")},
            "verdict": v_theirs,
            "comparison": constants_row(b_theirs, v_theirs),
            "what_it_tests": (
                "separates 'our ubar differs from theirs' from 'our bound formulas "
                "differ from theirs'.  If the constants computed on THEIR ubar land on "
                "their published values but ours do not, the gap is in the solution; if "
                "both land the same distance away, the gap is in the bounds."),
        }
        print(f"  ablation on THEIR ubar: Y={b_theirs['Y']:.5e} Z1={b_theirs['Z1']:.5e} "
              f"Z2={b_theirs['Z2']:.4f} Z3={b_theirs['Z3']:.4f}")
        sys.stdout.flush()

    # =====================================================================
    # 7.  Does the certificate NOTICE a displaced ubar?
    # =====================================================================
    rng = np.random.default_rng(2560)
    poison = []
    for scale in (1e-10, 1e-6, 1e-3):
        bad = a_ours.copy()
        bad[:20] = bad[:20] + scale * rng.standard_normal(20)
        bb = bc.bounds(pr, bad)
        vv = bc.radii_verdict(bb["Y"], bb["Z1"], bb["Z2"], bb["Z3"])
        poison.append({"scale": scale, "Y": bb["Y"], "Z1": bb["Z1"],
                       "closes": vv["closes"], "delta_min": vv.get("delta_min"),
                       "Y_over_ours": bb["Y"] / b_ours["Y"],
                       # Y's finite part is the half that tracks the ITERATE; the other
                       # half is the truncation tail, which a small displacement cannot
                       # move.  Reporting only the total would hide that.
                       "Y_finite_part": bb["Y_finite_part"],
                       "Y_finite_part_over_ours":
                           bb["Y_finite_part"] / b_ours["Y_finite_part"],
                       "Y_tail_part": bb["Y_tail_part"]})
        print(f"  poison {scale:.0e} -> Y {bb['Y']:.4e} ({bb['Y']/b_ours['Y']:.2f}x), "
              f"finite part {bb['Y_finite_part']:.3e} "
              f"({bb['Y_finite_part']/b_ours['Y_finite_part']:.2e}x), "
              f"closes {vv['closes']}")
        sys.stdout.flush()
    out["poisoning"] = poison

    out["total_seconds"] = time.time() - t_all
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=float)

    # -- console summary, magnitudes only -----------------------------------
    print("")
    print("  ---- THE GATE ----")
    print(f"  our certified interval : [{dmin:.6e}, {dbar:.6e}]")
    print(f"  their published enclosure 1e-3, our P(1e-3) = {P_at_enc:.4e}")
    print(f"  READING A (their 1e-3 is a certified radius of OUR polynomial): "
          f"{reading_a}")
    print(f"  READING B (all constants within 2x): {reading_b}")
    for k in ("Y", "Z1", "Z2", "Z3", "delta_bar"):
        r = ratios[k]
        print(f"     {k:10s} ours/theirs = {r:.4f}" if r else f"     {k:10s} n/a")
    print(f"  wrote {OUT}   ({out['total_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
