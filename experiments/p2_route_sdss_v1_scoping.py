#!/usr/bin/env python3
"""Leg 313 / Route-SDSS -- does leg 260's substantive obstruction survive SEEDING?

PAPER SCOPING ONLY. No solver is built, run, read into, or edited; no search is run.
Everything here is quadrature and arithmetic about closed forms, which is exactly the
scope leg 260's own scoping runner operated in.

The leg asks ONE question: leg 260 killed the DSS lane's expensive entrance with a
SUBSTANTIVE (not price-shaped) obstruction, verbatim -- "Entry B's defining adjective
UNSEEDED is incompatible with its object's only function space".  Does that obstruction
survive when the search is SEEDED from a known numerical DSS candidate rather than
trawled?  The ban's own lift clause names three questions (a) function space,
(b) object, (c) price; they are answered in the same pass.

What is measured here:

  S1  The ban text itself, machine-read from plan_of_record.BANNED at run time (never
      trusted to a transcribed sentence).  Entry B's own object clause is checked for
      the words that scope it.

  S2  The Type-I profile's norm, |U(y)| <= C/(1+|y|) on R^3 (Chae-Wolf arXiv:1610.09464
      Thm 1.1, carried from leg 253 via leg 260), in three spaces:
        - unweighted L^2(dy)                 -- leg 260's divergent row, REPRODUCED as a
                                                positive control against a banked number
        - weighted   L^2((1+|y|)^{-s} dy)    -- leg 260's OWN answer (a) space
        - the algebraically compactified variable X = |y|/(1+|y|), which is the
          discretisation the only DEMONSTRATED seeded method actually uses
          (Hou arXiv:2405.10916: "the computation is performed in a transformed domain
          on a uniform mesh, which maps back to a highly adaptive physical mesh")

  S3  The far-field log-periodic block under that same compactification.  In the
      physical variable it is r^{-1+i*kappa}; in X it is (1-X)^{1-i*kappa} -- which is
      EXACTLY the X^{1-i*y} limited-regularity form that clause (a) requires this leg to
      carry from PHASE2_P2_NOTES sec 26 / Route-E sec 4.1, at the opposite end of the
      domain.  Its Chebyshev coefficient decay and cost-to-tolerance are measured, with
      a smooth positive control and a kappa = 0 control that CAN come out differently
      (lesson 90).

  S4  The price (c), re-read from the live tree rather than cited from leg 260.

Runtime: a few seconds.  No estimate step was needed and no long run arose.
"""
from __future__ import annotations

import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import plan_of_record as por          # noqa: E402  (ban text, read not written)
import capabilities as caps           # noqa: E402  (the standing grep-first ban)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_sdss_v1.json")

selftests: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    selftests.append({"name": name, "pass": bool(ok), "detail": detail})


# ---------------------------------------------------------------------------
# S1 -- the ban text, machine-read.  Never transcribed.
# ---------------------------------------------------------------------------
def s1_ban_text() -> dict:
    bans = [b for b in por.BANNED]
    txts = []
    for b in bans:
        # BANNED entries are (what, lifted_by) pairs or objects; normalise to text.
        if isinstance(b, (list, tuple)):
            txts.append((str(b[0]), str(b[1]) if len(b) > 1 else ""))
        else:
            txts.append((str(getattr(b, "what", b)), str(getattr(b, "lifted_by", ""))))

    dss = [(w, l) for (w, l) in txts if "DSS" in w]
    entry_a = [(w, l) for (w, l) in dss if "CHEAP-ENTRANCE" in w]
    entry_b = [(w, l) for (w, l) in dss if "EXPENSIVE" in w]

    check("S1.1 two DSS entries", len(dss) == 2, f"found {len(dss)}")
    check("S1.2 entry A present", len(entry_a) == 1, "CHEAP-ENTRANCE")
    check("S1.3 entry B present", len(entry_b) == 1, "EXPENSIVE entrance")

    aw, al = entry_a[0]
    bw, bl = entry_b[0]

    # Entry A is scoped to bifurcation off a fixed point.
    a_bifurcation = "BIFURCATION OFF A FIXED POINT" in aw
    check("S1.4 entry A scoped to bifurcation-off-a-fixed-point", a_bifurcation, aw[:80])

    # Entry B's OBJECT clause -- the words that scope it.
    b_global = "GLOBAL periodic-orbit search" in bw
    b_noseed = "no fixed point nearby to seed it" in bw
    check("S1.5 entry B object clause says GLOBAL", b_global, "GLOBAL periodic-orbit search")
    check("S1.6 entry B object clause says 'no fixed point nearby to seed it'", b_noseed,
          "the seeding scope is in the ban's own object text")

    # The three lift questions.
    q_space = "FUNCTION SPACE" in bl
    q_object = "OBJECT" in bl
    q_price = "PRICE in leg-hours" in bl
    check("S1.7 lift clause names (a) FUNCTION SPACE", q_space, "")
    check("S1.8 lift clause names (b) OBJECT", q_object, "")
    check("S1.9 lift clause names (c) PRICE in leg-hours", q_price, "")

    # Clause (a)'s recorded difficulty and clause (b)'s recorded scope, verbatim markers.
    a_diff = "X^{1-iy}" in bl and "LIMITED REGULARITY" in bl
    b_scope = "gCLM" in bl and "NS" in bl
    check("S1.10 clause (a) carries the X^{1-iy} limited-regularity difficulty", a_diff, "")
    check("S1.11 clause (b) contrasts gCLM with NS", b_scope, "")
    mu_absent = "max Re = -1e-13" in bl and "mu=0.05" in bl
    check("S1.12 clause (a) carries the viscous-band-absent magnitude", mu_absent,
          "max Re = -1e-13 at mu=0.05")

    # Does EITHER entry name a search seeded from a known numerical candidate?
    seeded_named = any(("seeded from" in w.lower()) or ("numerical candidate" in w.lower())
                       for (w, _) in dss)
    check("S1.13 neither DSS entry names a seeded-from-a-numerical-candidate search",
          not seeded_named, "reported, not acted on -- this leg does not lift bans")

    return {
        "n_dss_entries": len(dss),
        "entry_A_scoped_to_bifurcation_off_fixed_point": bool(a_bifurcation),
        "entry_B_object_says_GLOBAL": bool(b_global),
        "entry_B_object_says_no_fixed_point_nearby_to_seed_it": bool(b_noseed),
        "entry_B_object_clause_verbatim":
            "a GLOBAL periodic-orbit search of a rescaled flow with no fixed point "
            "nearby to seed it",
        "lift_clause_names_a_function_space": bool(q_space),
        "lift_clause_names_b_object": bool(q_object),
        "lift_clause_names_c_price": bool(q_price),
        "clause_a_carries_X_1_minus_iy_difficulty": bool(a_diff),
        "clause_a_viscous_band_absent_max_Re": -1e-13,
        "clause_a_viscous_band_absent_mu": 0.05,
        "either_entry_names_a_seeded_search": bool(seeded_named),
    }


# ---------------------------------------------------------------------------
# S2 -- the Type-I profile's norm in three spaces.
# ---------------------------------------------------------------------------
def shell_ratio(integrand, R, n=400001):
    """(int_R^{2R} f) / (int_{R/2}^{R} f), by Simpson.  >1 diverges, <1 converges."""
    def q(a, b):
        x = np.linspace(a, b, n)
        return np.trapezoid(integrand(x), x) if hasattr(np, "trapezoid") \
            else np.trapz(integrand(x), x)
    return q(R, 2.0 * R) / q(0.5 * R, R)


def s2_spaces() -> dict:
    R = 1.0e4          # deep in the asymptotic regime -- leg 260's own hard-won lesson

    # (i-control) REPRODUCE leg 260's banked p=2 row EXACTLY.  Leg 260's table is
    # computed on the PURE POWER |U| = r^{-1} (its closed form is 2^{3-p}); this leg's
    # rows below use the faithful Type-I envelope |U| = (1+r)^{-1}, which differs from
    # the pure power by an O(1/R) shell correction.  The two are separated here on
    # purpose: the control must reproduce the BANKED number on the BANKED integrand.
    f_pure = lambda r: (r ** 2) * r ** (-2.0)
    ratio_pure = shell_ratio(f_pure, R)
    check("S2.1 positive control: on leg 260's OWN integrand (pure power |U|=r^{-1}) "
          "the shell ratio reproduces its banked divergent p=2 row 2.000035 to <1e-4",
          abs(ratio_pure - 2.000035) < 1e-4,
          f"measured {ratio_pure:.6f} vs banked 2.000035")

    # (i) unweighted L^2(dy) on the faithful envelope: r^2 (1+r)^{-2} -> 1.  Ratio -> 2.
    f_L2 = lambda r: (r ** 2) / (1.0 + r) ** 2
    ratio_L2 = shell_ratio(f_L2, R)
    # Exact finite-R value for THIS integrand: int (1 - 2/r + O(r^-2)) dr.
    exact_L2 = (R - 2.0 * np.log(2.0)) / (0.5 * R - 2.0 * np.log(2.0))
    check("S2.1b the faithful (1+r)^{-1} envelope also diverges, and matches its own "
          "exact finite-R value (not leg 260's pure-power one) to <1e-5 relative",
          abs(ratio_L2 - exact_L2) / exact_L2 < 1e-5,
          f"measured {ratio_L2:.6f}, exact-for-this-integrand {exact_L2:.6f}, "
          f"leg 260's pure-power row 2.000035 -- the 1.2e-4 gap is the envelope, "
          f"not an error")

    # (ii) weighted L^2(rho), rho = (1+r)^{-s}: integrand r^2 (1+r)^{-2-s} ~ r^{-s}.
    s_grid = [0.0, 0.5, 0.9, 1.0, 1.1, 1.5, 2.0, 3.0]
    weighted = {}
    for s in s_grid:
        f = lambda r, s=s: (r ** 2) * (1.0 + r) ** (-2.0 - s)
        ratio = shell_ratio(f, R)
        closed = 2.0 ** (1.0 - s)            # exact ASYMPTOTIC ratio for r^{-s}
        weighted[f"s={s}"] = {
            "shell_ratio": float(ratio),
            "closed_form_2^(1-s)": float(closed),
            "rel_err_vs_closed_form": float(abs(ratio - closed) / closed),
            "finite": bool(ratio < 1.0),
        }
    # The residual is the same O((2+s)ln2 / R) envelope correction as in S2.1b, so the
    # tolerance is set at 1e-3 and the SHAPE (monotone in s, crossing at 1) is what is
    # tested -- reporting the magnitude, not a boolean.
    check("S2.2 weighted ratios match the closed form 2^(1-s) to <1e-3 relative on "
          "every row, with the residual explained by the same envelope correction",
          all(v["rel_err_vs_closed_form"] < 1e-3 for v in weighted.values()),
          "max rel err "
          f"{max(v['rel_err_vs_closed_form'] for v in weighted.values()):.2e} "
          f"(envelope correction ~ (2+s)ln2/R = {5.0 * np.log(2.0) / R:.2e} at s=3)")
    check("S2.3 the weighted crossing is at s = 1 (bracketed, and the crossing row is "
          "within the envelope correction of 1)",
          abs(weighted["s=1.0"]["shell_ratio"] - 1.0) < 1e-3
          and weighted["s=0.9"]["shell_ratio"] > 1.0
          and weighted["s=1.1"]["shell_ratio"] < 1.0,
          f"s=0.9 -> {weighted['s=0.9']['shell_ratio']:.6f}, "
          f"s=1.0 -> {weighted['s=1.0']['shell_ratio']:.6f}, "
          f"s=1.1 -> {weighted['s=1.1']['shell_ratio']:.6f}")

    # (iii) the compactified variable X = r/(1+r), i.e. r = X/(1-X), 1+r = 1/(1-X).
    # The Type-I profile |U| ~ 1/(1+r) becomes EXACTLY (1-X): a LINEAR ZERO at X = 1.
    Xg = np.linspace(0.0, 1.0, 2000001)[:-1]
    U_of_X = 1.0 - Xg
    norm_flat = float(np.sqrt(np.trapezoid(U_of_X ** 2, Xg) if hasattr(np, "trapezoid")
                              else np.trapz(U_of_X ** 2, Xg)))
    exact_flat = float(np.sqrt(1.0 / 3.0))
    check("S2.4 compactified profile is the exact linear zero (1-X); its L^2(dX) norm "
          "is finite and equals sqrt(1/3)",
          abs(norm_flat - exact_flat) < 1e-6,
          f"measured {norm_flat:.9f} vs exact {exact_flat:.9f}")

    # The SAME object, three verdicts.  That is the whole of S2.
    return {
        "profile": "|U(y)| <= C/(1+|y|)  (Type I; Chae-Wolf arXiv:1610.09464 Thm 1.1)",
        "shell_start_R": R,
        "unweighted_L2_shell_ratio": float(ratio_L2),
        "unweighted_L2_finite": bool(ratio_L2 < 1.0),
        "leg260_banked_p2_row": 2.000035,
        "weighted_L2_rows": weighted,
        "weighted_crossing_s": 1.0,
        "compactified_map": "X = |y|/(1+|y|)",
        "compactified_profile_closed_form": "(1 - X)  [an exact linear zero at X=1]",
        "compactified_L2_dX_norm": norm_flat,
        "compactified_L2_dX_norm_exact": exact_flat,
        "compactified_finite": True,
    }


# ---------------------------------------------------------------------------
# S3 -- the log-periodic block under the same compactification.
# ---------------------------------------------------------------------------
def cheb_coeffs(fn, N):
    """Chebyshev coefficients of fn on [0,1] at N+1 Chebyshev-Lobatto points."""
    k = np.arange(N + 1)
    t = np.cos(np.pi * k / N)                 # [-1,1]
    X = 0.5 * (t + 1.0)                       # [0,1]
    v = fn(X)
    # DCT-I via FFT of the mirrored sequence.
    ext = np.concatenate([v, v[-2:0:-1]])
    c = np.real(np.fft.fft(np.real(ext))) + 1j * np.real(np.fft.fft(np.imag(ext)))
    c = c[:N + 1] / N
    c[0] /= 2.0
    c[N] /= 2.0
    return np.abs(c)


def tail_truncation_error(absc):
    """sum_{n>m} |a_n| for every m -- a rigorous-in-form truncation bound."""
    return np.cumsum(absc[::-1])[::-1]


def s3_regularity() -> dict:
    N = 1 << 20        # 1,048,576 modes.  Chosen by the resolution study below:
                       # at N = 2^14 the kappa = 20 row moved 29.8% under an 8x
                       # refinement, i.e. it was measuring the ARRAY, not the object.
    results = {}

    # POSITIVE CONTROL: a smooth (entire) function must show geometric decay.
    # NOTE, and this is a lesson-90 repair kept in the artifact: the first draft used
    # exp(-8(X-1/2)^2), which is EVEN about the midpoint, so all its ODD Chebyshev
    # coefficients vanish identically and the "first coefficient below tol" test
    # reported n = 1 for a symmetry reason having nothing to do with smoothness -- a
    # control that could not come out differently.  Replaced with an ASYMMETRIC entire
    # function, and the criterion strengthened from "the first coefficient below tol"
    # to "the last index at or above tol", which no symmetry can fake.
    def tail_index(absc, tol):
        idx = np.nonzero(absc >= tol)[0]
        return int(idx[-1]) + 1 if idx.size else 0

    ctrl_a = cheb_coeffs(lambda X: np.exp(-8.0 * (X - 0.5) ** 2) + 0j, N)
    odd_vanish = float(np.max(ctrl_a[1:200:2]))
    ctrl = cheb_coeffs(lambda X: np.exp(2.3 * X) * np.sin(3.0 * X + 0.7) + 0j, N)
    n_ctrl = tail_index(ctrl, 1e-13)
    check("S3.1 positive control: an ASYMMETRIC entire function has every coefficient "
          "below 1e-13 past a few dozen modes (geometric decay -- the instrument CAN "
          "report spectral accuracy)",
          0 < n_ctrl < 200, f"last index >= 1e-13 is n = {n_ctrl}")
    check("S3.1b the discarded symmetric control is retained and shown to be degenerate: "
          "its odd coefficients vanish for a SYMMETRY reason, not a smoothness one",
          odd_vanish < 1e-15,
          f"max odd |a_n| of exp(-8(X-1/2)^2) over n<200 is {odd_vanish:.3e} -- this is "
          f"why it was not usable as the control")

    # kappa = 0 CONTROL that can come out differently (lesson 90): (1-X)^1 is a
    # POLYNOMIAL, so its coefficients must terminate.  If this did not terminate the
    # measurement below would be an artifact of the transform, not of the object.
    k0 = cheb_coeffs(lambda X: (1.0 - X) + 0j, N)
    terminates = bool(np.max(k0[3:]) < 1e-12)
    check("S3.2 kappa=0 control terminates (the exponent 1-i*kappa is a polynomial at "
          "kappa=0, so the defect must vanish there -- and it does)",
          terminates, f"max|a_n| for n>=3 is {np.max(k0[3:]):.3e}")

    kappas = [0.0, 1.0, 2.0, 5.0, 10.0, 20.0]
    for kap in kappas:
        f = lambda X, kap=kap: np.exp((1.0 - 1j * kap) * np.log(np.maximum(1.0 - X, 1e-300)))
        a = cheb_coeffs(f, N)
        tail = tail_truncation_error(a)
        scale = float(tail[0]) if tail[0] > 0 else 1.0
        rel = tail / scale
        # fitted algebraic rate over the resolved decade 64..1024
        lo, hi = 64, 1024
        n = np.arange(N + 1)
        m = (n >= lo) & (n <= hi) & (a > 0)
        p = float(-np.polyfit(np.log(n[m]), np.log(a[m]), 1)[0]) if m.sum() > 10 else float("nan")
        # modes needed for 1e-6 / 1e-8 relative truncation error
        def n_for(eps):
            idx = np.argmax(rel < eps)
            return int(idx) if rel[idx] < eps else -1
        results[f"kappa={kap}"] = {
            "fitted_algebraic_rate_p": p,
            "modes_for_rel_trunc_1e-6": n_for(1e-6),
            "modes_for_rel_trunc_1e-8": n_for(1e-8),
            "rel_trunc_at_n=32": float(rel[32]),
            "rel_trunc_at_n=256": float(rel[256]),
        }

    # RESOLUTION STUDY.  The truncation tails are computed from a finite coefficient
    # array, so a reported "modes for 1e-8" that sits near N is measuring the ARRAY, not
    # the object (this leg's first draft quoted a 1e-8 column that saturated at
    # n = 16332 with N = 16384 -- discarded, and the reason kept here).  The 1e-6 column
    # is re-measured at 8x the resolution and required to be stable.
    N2 = 1 << 17   # the COARSE level, compared against the N = 2^20 primary
    stability = {}
    for kap in kappas:
        if kap == 0.0:
            continue
        f = lambda X, kap=kap: np.exp((1.0 - 1j * kap) * np.log(np.maximum(1.0 - X, 1e-300)))
        a2 = cheb_coeffs(f, N2)
        rel2 = tail_truncation_error(a2) / float(tail_truncation_error(a2)[0])
        idx = np.argmax(rel2 < 1e-6)
        n2 = int(idx) if rel2[idx] < 1e-6 else -1
        n1 = results[f"kappa={kap}"]["modes_for_rel_trunc_1e-6"]
        stability[f"kappa={kap}"] = {
            "modes_at_N_131072": n2, "modes_at_N_1048576": n1,
            "rel_change": abs(n2 - n1) / float(n1) if n1 > 0 else float("nan"),
        }
        results[f"kappa={kap}"]["modes_for_rel_trunc_1e-6_at_coarse_level"] = n2
        # The 1e-8 column saturated against N and is NOT reported as a resolved number.
        results[f"kappa={kap}"]["modes_for_rel_trunc_1e-8"] = (
            "NOT QUOTED -- at N = 2^14 this column saturated against the array "
            "(n = 16332 of N = 16384); it is a statement about the array, not the object")
    check("S3.7 resolution study: at the chosen N = 2^20 the 1e-6 mode counts are "
          "stable to <5% against the 8x-coarser N = 2^17 level, so they measure the "
          "OBJECT and not the array (they were NOT at N = 2^14 -- see the docstring)",
          all(v["rel_change"] < 0.05 for v in stability.values()),
          "; ".join(f"{k}: {v['modes_at_N_131072']}->{v['modes_at_N_1048576']} "
                    f"({100 * v['rel_change']:.1f}%)" for k, v in stability.items()))

    nonzero = [v for k, v in results.items() if k != "kappa=0.0"]
    rates = [v["fitted_algebraic_rate_p"] for v in nonzero]
    check("S3.3 every kappa != 0 decays ALGEBRAICALLY, fitted rate in (2, 4) -- not "
          "geometrically, unlike the smooth control",
          all(2.0 < r < 4.0 for r in rates),
          "rates " + ", ".join(f"{r:.3f}" for r in rates))
    n6 = [v["modes_for_rel_trunc_1e-6"] for v in nonzero]
    check("S3.4 the cost to 1e-6 is monotone increasing in kappa (the defect gets "
          "WORSE as the log-periodic frequency rises)",
          all(x > 0 for x in n6) and all(b >= a for a, b in zip(n6, n6[1:])),
          "modes " + ", ".join(str(x) for x in n6))
    # A REAL comparison, at the SAME tolerance on the SAME instrument.  The first draft
    # of this check was `min(n6) >= 10 * 1`, which is a tautology -- lesson 90 again,
    # caught by this leg's own review and repaired rather than deleted.
    ctrl_tail = tail_truncation_error(ctrl)
    ctrl_rel = ctrl_tail / float(ctrl_tail[0])
    n_ctrl_6 = int(np.argmax(ctrl_rel < 1e-6))
    sep = min(n6) / float(max(n_ctrl_6, 1))
    check("S3.5 at the SAME 1e-6 tolerance on the SAME instrument, the smooth control "
          "is >= 10x cheaper than the cheapest kappa != 0 case",
          sep >= 10.0,
          f"control needs n={n_ctrl_6} for 1e-6; cheapest kappa!=0 needs n={min(n6)}, "
          f"worst n={max(n6)} -- separation {sep:.1f}x")

    # How the cost scales in the log-periodic frequency.  Fitted on the MEASURED rows
    # only (kappa = 1..20); anything beyond is labelled an extrapolation and is NOT an
    # NS number -- clause (b) forbids importing gCLM's frequency into NS, and the
    # extrapolation below is reported precisely to show what such an import would cost
    # if it were legitimate, which it is not.
    ks = np.array([k for k in kappas if k > 0.0])
    ns = np.array([results[f"kappa={k}"]["modes_for_rel_trunc_1e-6"] for k in ks],
                  dtype=float)
    q, logC = np.polyfit(np.log(ks), np.log(ns), 1)
    fit_pred = np.exp(logC) * ks ** q
    fit_relerr = float(np.max(np.abs(fit_pred - ns) / ns))
    check("S3.6 the cost-to-1e-6 follows a clean power law in kappa across the measured "
          "rows (max rel residual < 0.15) -- a SHAPE, not an endpoint (lesson 72)",
          fit_relerr < 0.15,
          f"n(kappa) ~ {np.exp(logC):.0f} * kappa^{q:.3f}, max rel residual "
          f"{fit_relerr:.3f}")
    kappa_gclm = 430.35
    extrap = float(np.exp(logC) * kappa_gclm ** q)

    return {
        "cost_scaling_exponent_q": float(q),
        "cost_scaling_prefactor_C": float(np.exp(logC)),
        "cost_scaling_max_rel_residual": fit_relerr,
        "EXTRAPOLATION_ONLY_modes_at_gclm_leading_kappa": extrap,
        "EXTRAPOLATION_CAVEAT": (
            "430.35 is Route-I's leading |Im| in gCLM. Clause (b) of the ban's own lift "
            "condition states the gCLM reasons do NOT transfer to NS ('Nothing about NS. "
            "gCLM's scaling structure is not NS's'). This row is reported to show the "
            "cost of an import that is NOT licensed, and must not be quoted as an NS "
            "resolution requirement. The NS log-periodic frequency is UNKNOWN -- it is "
            "an output of the very search being scoped."),
        "physical_far_field_block": "r^{-1+i*kappa}",
        "compactified_far_field_block": "(1-X)^{1-i*kappa}",
        "identical_in_form_to_clause_a_difficulty": "X^{1-iy} (Route-E sec 4.1 / sec 26)",
        "N_modes_used": N,
        "positive_control_smooth_modes_to_1e-13": n_ctrl,
        "positive_control_smooth_modes_to_1e-6": n_ctrl_6,
        "kappa0_control_terminates": terminates,
        "rows": results,
        "resolution_study_1e-6_stability": stability,
        "route_I_leading_abs_imag": 430.35,
    }


# ---------------------------------------------------------------------------
# S4 -- the price, re-read from the live tree.
# ---------------------------------------------------------------------------
def s4_price(s3: dict) -> dict:
    n_modules = len(caps.CAPABILITIES)
    leg = 313
    rate = leg / n_modules
    must_build = 5
    floor = must_build * rate

    check("S4.1 capabilities.py index read live, not hardcoded",
          n_modules > 0, f"{n_modules} indexed modules")
    check("S4.2 leg 260's own prediction is CHECKED and is REFUTED in direction: it "
          "said the floor would FALL as modules land; 53 legs later the module count "
          "is unchanged, so the floor ROSE",
          n_modules == 48 and floor > 27.0,
          f"260: 48 modules / 260 legs -> 5.42 -> floor 27. "
          f"313: {n_modules} modules / {leg} legs -> {rate:.2f} -> floor {floor:.1f}")

    # Resolution demand implied by S3, in the radial/compactified direction.
    worst = max(v["modes_for_rel_trunc_1e-6"] for k, v in s3["rows"].items()
                if k != "kappa=0.0")
    # Compared at the SAME tolerance (1e-6) on the same instrument -- not against the
    # control's 1e-13 point, which would flatter the penalty.
    smooth_equiv = max(int(s3["positive_control_smooth_modes_to_1e-6"]), 1)
    penalty = worst / float(smooth_equiv)

    dof_smooth = 128 ** 3 * 2
    dof_far = (128 ** 2) * worst * 2
    dof_ratio = dof_far / dof_smooth

    phase1_dof = 2 * 10000
    phase1_hours = 14.0

    check("S4.3 the far-field resolution penalty is a real multiplier, not a rounding",
          penalty > 1.0, f"{penalty:.2f}x modes vs the smooth control")

    return {
        "capabilities_indexed_modules": n_modules,
        "leg_number": leg,
        "legs_per_delivered_module": rate,
        "modules_that_must_be_built": must_build,
        "build_floor_legs": floor,
        "leg260_rate": 260 / 48,
        "leg260_floor_legs": 27,
        "floor_moved_direction": "UP",
        "far_field_modes_to_1e-6_worst_kappa": worst,
        "smooth_control_modes": smooth_equiv,
        "radial_resolution_penalty": penalty,
        "dof_uniform_128cubed_x2": dof_smooth,
        "dof_with_measured_far_field_radial": dof_far,
        "dof_ratio_vs_uniform": dof_ratio,
        "phase1_viscous_rung_dof": phase1_dof,
        "phase1_viscous_rung_hours_single_cpu": phase1_hours,
        "dof_ratio_vs_phase1": dof_far / phase1_dof,
    }


def main() -> int:
    s1 = s1_ban_text()
    s2 = s2_spaces()
    s3 = s3_regularity()
    s4 = s4_price(s3)

    n_pass = sum(1 for t in selftests if t["pass"])
    payload = {
        "leg": 313,
        "route": "SDSS",
        "question": ("Does leg 260's substantive obstruction -- 'Entry B's defining "
                     "adjective UNSEEDED is incompatible with its object's only "
                     "function space' -- survive when the search is SEEDED?"),
        "gate_pre_committed": ("Does leg 260's substantive obstruction survive seeding, "
                               "with the (a)/(b)/(c) triple answered either way?"),
        "gate_answer": "NO",
        "scope": ("paper scoping only; no construction, no search run, no solver built, "
                  "run, read into or edited"),
        "s1_ban_text": s1,
        "s2_function_space": s2,
        "s3_regularity_of_the_far_field_block": s3,
        "s4_price": s4,
        "named_mechanism": (
            "THE LOG-PERIODIC BLOCK'S REGULARITY DEFECT IS AN INVARIANT OF THE "
            "ENTRANCE, NOT A PROPERTY OF THE DOMAIN'S FAR END. The compactification "
            "X = |y|/(1+|y|) that makes the Type-I profile's norm FINITE carries the "
            "far-field block r^{-1+i*kappa} to (1-X)^{1-i*kappa} -- the identical "
            "functional form to clause (a)'s recorded gCLM difficulty X^{1-iy}, at the "
            "opposite end of the domain. Seeding dissolves all four of leg 260's "
            "sec 3.4 reasons; it does not dissolve this, because this is not a "
            "statement about the seed."),
        "walls": {
            "clay_odds": "~0.05%, unchanged",
            "links_of_L1_to_L4_moved": 0,
            "wall_1": "no claim of movement; this leg answers a scoping question",
            "wall_2": ("the screened object is non-axisymmetric 3D with no symmetry "
                       "reduction -- squarely on the far side of Wall 2"),
        },
        "selftests": selftests,
        "selftests_passed": f"{n_pass}/{len(selftests)}",
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)

    for t in selftests:
        print(("PASS " if t["pass"] else "FAIL ") + t["name"] + " :: " + t["detail"])
    print(f"\n{n_pass}/{len(selftests)} self-tests pass -> {OUT}")
    return 0 if n_pass == len(selftests) else 1


if __name__ == "__main__":
    sys.exit(main())
