#!/usr/bin/env python3
"""Leg 390, Route-DTOR: pricing Fefferman statement (D) (breakdown on R^3/Z^3).

WHAT THIS RUNNER IS
-------------------------------------------------------------------------------
`CLAY_OBLIGATIONS.md` prices a Tier-2 DSS candidate against Fefferman's breakdown
statement **(C)** (breakdown on R^3), whose acceptance conditions include **(7)**,
bounded energy. Leg 381 named -- without authorising -- statement **(D)**
(breakdown on R^3/Z^3), whose acceptance conditions are **(10)** periodicity and
**(11)** smoothness, with no decay and no bounded-energy condition. §4 and §5 of
the ledger are precisely the obligations that bounded energy and decay generate,
so (D) would make §4 vacuous by construction.

This runner re-derives the ledger under (D) and PUTS NUMBERS ON THE PRICE:

  check_A  the acceptance-condition diff, machine-read from the landed leg-381
           record (verbatim strings, never retyped here)
  check_B  the rigidity that decides the shape of the whole question: an exactly
           lambda-DSS field cannot be Z^3-periodic and non-constant -- measured
           as a Fourier-band annihilation count, not asserted
  check_C  THE HEART: the periodization bill for the R^3-anchored profile, as an
           exponent threshold in the SAME currency as leg 381's cutoff bill
  check_D  the cut-then-periodize route: leg 381's cutoff bill inherited verbatim
           by machine read, plus the image-interaction magnitudes it adds
  check_E  §2's four screen rows, machine-read against their named landed records
           under a pre-registered domain-marker rule
  check_F  the §1-§5 disposition table, assembled from A-E

WHAT THIS RUNNER IS NOT
-------------------------------------------------------------------------------
It is not a retarget, not a recommendation, and not build authority. **THE
RETARGET DECISION IS THE USER'S AND THIS LEG MAKES NONE.** It prices an option.
It edits no obligations file (it hashes `CLAY_OBLIGATIONS.md` on read to record
that it only read it), no solver module, and adds no `capabilities.py` row
because it adds no solver module. CEILING: **TIER 2**. §6's two no-method
obligations stay OPEN. No link of the `L1 -> L4` chain moves. Clay stays ~0.05%.

NO GREEN WITHOUT A DEMONSTRATED RED PATH: every check that can report agreement
carries a planted violation in the same artifact, under a `can_fail_*` key, and
the planted violation is shown FIRING.

    .venv/bin/python experiments/p2_route_dtor_v1.py
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data"
CLOC = DATA / "p2_route_cloc_v1.json"        # leg 381, the (D)/(C) verbatim source
PVLX = DATA / "p2_route_pvlx_v1.json"        # leg 330, Chae-Wolf / Pineau-Vicol
CTRX = DATA / "p2_route_ctrx_v1.json"        # leg 326, Chae-Tsai
MRYX = DATA / "p2_route_mryx_v1.json"        # leg 368, Morrey (Jiu-Wang-Wei)
POCP = DATA / "p2_route_pocp_v1.json"        # leg 348, §1's certification-route census
SCREEN = ROOT / "solver" / "dssp_screen.py"  # the executable §2 screen (legs 357/362/370)
OBLIG = ROOT / "CLAY_OBLIGATIONS.md"         # READ ONLY, hashed to prove it
OUT = DATA / "p2_route_dtor_v1.json"


def _load(p: Path):
    return json.loads(p.read_text())


# =============================================================================
# check_A -- the acceptance-condition diff, machine-read
# =============================================================================

_CITE = re.compile(r"\((\d+)\)")


def parse_statement(text: str) -> dict:
    """Split a Fefferman breakdown statement into its DATA conditions (the ones
    the initial datum and forcing must satisfy) and its SOLUTION conditions (the
    ones a solution would have to satisfy, and whose non-existence is asserted).

    Both statements have the identical shape

        ... satisfying (a), (b), for which there exist no solutions (p, u) of
        (c), (d), ..., on ... x [0, infinity).

    so the split point is the phrase 'for which there exist no solutions'. The
    condition numbers are then read off by regex. Nothing is retyped.
    """
    lo = text.lower()
    key = "for which there exist no solutions"
    i = lo.find(key)
    if i < 0:
        raise ValueError("statement does not have the expected shape")
    head, tail = text[:i], text[i:]
    j = head.lower().rfind("satisfying")
    if j < 0:
        raise ValueError("no 'satisfying' clause")
    data = sorted(int(m) for m in _CITE.findall(head[j:]))
    solution = sorted(int(m) for m in _CITE.findall(tail))
    return {"data_conditions": data, "solution_conditions": solution}


def check_A() -> dict:
    d = _load(CLOC)["check_D_clay_primary_text"]
    vb = d["verbatim_conditions"]
    C, D = parse_statement(vb["(C)"]), parse_statement(vb["(D)"])

    BOUNDED_ENERGY = 7
    # (7) is the bounded-energy condition: confirm from its OWN banked text.
    seven_is_bounded_energy = "bounded energy" in vb["(7)"].lower()
    # (6) and (11) are the smoothness conditions: confirm they are the same text.
    six_eleven_identical = vb["(6)"].strip() == vb["(11)"].strip()
    # (10) is the periodicity condition: confirm from its own banked text.
    ten_is_periodicity = "u(x, t) = u(x + e" in vb["(10)"]

    dropped = sorted(set(C["solution_conditions"]) - set(D["solution_conditions"]))
    added = sorted(set(D["solution_conditions"]) - set(C["solution_conditions"]))

    banked = set(vb)
    missing_data_conditions = [c for c in ("(8)", "(9)") if c not in banked]

    out = {
        "source_record": "writeup/data/p2_route_cloc_v1.json (leg 381, 7aecf78)",
        "source_of_the_verbatim_text": d["source"],
        "statement_C": C,
        "statement_D": D,
        "seven_is_bounded_energy_confirmed_from_its_own_text": bool(seven_is_bounded_energy),
        "ten_is_periodicity_confirmed_from_its_own_text": bool(ten_is_periodicity),
        "six_and_eleven_are_the_same_text": bool(six_eleven_identical),
        "solution_conditions_dropped_going_C_to_D": dropped,
        "solution_conditions_added_going_C_to_D": added,
        "bounded_energy_in_C": BOUNDED_ENERGY in C["solution_conditions"],
        "bounded_energy_in_D": BOUNDED_ENERGY in D["solution_conditions"],
        "acceptance_diff_in_one_line": (
            "exactly one condition is dropped and exactly one is added: (7) bounded energy "
            "OUT, (10) periodicity IN; (6) and (11) are the same smoothness condition under "
            "two numbers. §4's premise is therefore ABSENT from (D)'s own text."
        ),
        "data_conditions_of_D_are_not_in_this_repository": missing_data_conditions,
        "gap_note": (
            "(8) and (9) -- (D)'s DATA conditions -- were never banked verbatim by leg 381 and "
            "no outreach is permitted to this leg, so they are treated as UNREAD-IN-REPOSITORY. "
            "Nothing below is priced from them. Routed to integration as a correction to be "
            "banked by a leg with outreach; this leg edits no obligations file."
        ),
        "can_fail_planted_seven_back_into_D": None,
    }

    # PLANTED VIOLATION: put (7) back into (D)'s solution list and show the
    # parser reports the bounded-energy premise PRESENT. A green that cannot go
    # red is not evidence.
    mutated = vb["(D)"].replace("(1), (2), (3), (10), (11)", "(1), (2), (3), (7), (10), (11)")
    Dm = parse_statement(mutated)
    out["can_fail_planted_seven_back_into_D"] = {
        "what_was_planted": "the string '(7),' inserted into (D)'s solution-condition list",
        "parser_reports_bounded_energy_in_D": BOUNDED_ENERGY in Dm["solution_conditions"],
        "fired": bool(
            (BOUNDED_ENERGY in Dm["solution_conditions"])
            != (BOUNDED_ENERGY in D["solution_conditions"])
        ),
    }
    return out


# =============================================================================
# check_B -- an exactly lambda-DSS field cannot be periodic and non-constant
# =============================================================================

def dss_periodic_survivors(lam: float, M: int, n_steps: int, tol: float = 1e-12):
    """A field that is L-periodic AND exactly lambda-DSS is also L/lambda-periodic
    (apply the DSS relation and read off the period of x -> u(lambda x)). In
    Fourier variables on the L-torus a mode has index m in Z^3; L/lambda^n
    periodicity requires m_j / lambda^n in Z for every j.

    Returns, for each n, how many nonzero modes of the band |m|_inf <= M survive.
    """
    m = np.arange(-M, M + 1)
    rows = []
    for n in range(1, n_steps + 1):
        q = m / lam ** n
        ok1d = np.abs(q - np.round(q)) < tol            # per-coordinate survivors
        n_ok = int(ok1d.sum())
        # a 3D mode survives iff every coordinate survives; the nonzero count is
        # (#survivors)^3 - 1 (the zero mode always survives and is the constant)
        rows.append({
            "n_dss_steps": n,
            "implied_period_over_L": float(lam ** (-n)),
            "surviving_1d_indices": sorted(int(v) for v in m[ok1d]),
            "surviving_nonzero_3d_modes": int(n_ok ** 3 - 1),
        })
    return rows


def check_B() -> dict:
    lam_banked = _load(CLOC)["check_A_field_is_what_it_claims"]["lambda"]   # 1.7
    lam_pv = _load(PVLX)["magnitudes_of_near_1"][0]["value_lambda_ceiling"]  # e^{1/2}
    M = 64

    cases = {}
    for name, lam in [("lambda_banked_1.7_rational_17_over_10", lam_banked),
                      ("lambda_PV_ceiling_e_to_the_half_irrational", lam_pv)]:
        rows = dss_periodic_survivors(lam, M, n_steps=3)
        n_star = next((r["n_dss_steps"] for r in rows
                       if r["surviving_nonzero_3d_modes"] == 0), None)
        # quantitative margin of the ONE-STEP constraint: how far the worst
        # surviving-candidate mode is from satisfying it
        m = np.arange(1, M + 1)
        q = m / lam
        margin = float(np.min(np.abs(np.exp(2j * np.pi * q) - 1.0)))
        cases[name] = {
            "lambda": float(lam),
            "band_M": M,
            "rows": rows,
            "n_steps_to_annihilate_the_band": n_star,
            "one_step_worst_case_margin_min_over_modes_of_abs_exp_minus_1": margin,
        }

    # how the one-step margin degrades with band width, for the irrational case:
    # dist(m/lambda, Z) is equidistributed, so the minimum over |m| <= M falls
    # like M^{-1}. Measured, with its fitted exponent.
    Ms = np.array([8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    mins = []
    for MM in Ms:
        m = np.arange(1, MM + 1)
        mins.append(float(np.min(np.abs(np.exp(2j * np.pi * m / lam_pv) - 1.0))))
    mins = np.array(mins)
    slope = float(np.polyfit(np.log(Ms), np.log(mins), 1)[0])

    # can_fail: lambda = 1 is no dilation at all -- the annihilation must NOT happen
    control = dss_periodic_survivors(1.0, M, n_steps=3)
    control_n_star = next((r["n_dss_steps"] for r in control
                           if r["surviving_nonzero_3d_modes"] == 0), None)

    return {
        "statement": (
            "If u(.,t) is L-periodic for every t and u is exactly lambda-DSS with lambda > 1, "
            "then u(.,t) is L/lambda^n-periodic for every n, hence (letting n -> infinity) "
            "constant in x. A NON-CONSTANT exactly-DSS field on T^3 does not exist."
        ),
        "why_it_decides_the_shape_of_this_leg": (
            "(D) cannot be targeted by a NATIVE torus DSS object. It can only be targeted by "
            "periodizing/localising an R^3-anchored one, which is why the price below is a "
            "periodization price and not a relabelling."
        ),
        "cases": cases,
        "one_step_margin_decay_with_band_width": {
            "band_widths_M": [int(v) for v in Ms],
            "worst_case_margins": [float(v) for v in mins],
            "fitted_exponent_in_M": slope,
            "predicted_exponent": -1.0,
            "abs_error": abs(slope + 1.0),
            "reading": (
                "the incompatibility is EXACT for every lambda > 1, but its quantitative margin "
                "is not uniform: it decays like M^{-1} in the resolved band, so a field that is "
                "DSS only to a tolerance can be periodic to that tolerance provided its content "
                "above wavenumber ~ 1/tolerance is negligible. That is a statement about "
                "APPROXIMATE objects and it does not soften the exact one."
            ),
        },
        "can_fail_lambda_equals_one_control": {
            "what_was_planted": "lambda = 1, i.e. no dilation at all",
            "n_steps_to_annihilate_the_band": control_n_star,
            "surviving_nonzero_3d_modes_at_n_1": control[0]["surviving_nonzero_3d_modes"],
            "fired": bool(control_n_star is None and control[0]["surviving_nonzero_3d_modes"] > 0),
        },
    }


# =============================================================================
# check_C -- THE HEART: the periodization bill, as an exponent threshold
# =============================================================================

_R_CACHE = {"N": None, "r": None}


def _lattice_radii(N: int = 96) -> np.ndarray:
    """Sorted |k|_2 for every nonzero k in Z^3 with |k|_inf <= N."""
    if _R_CACHE["N"] == N:
        return _R_CACHE["r"]
    g = np.arange(-N, N + 1)
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    r = np.sqrt(KX.astype(np.float32) ** 2 + KY ** 2 + KZ ** 2).ravel()
    r = np.sort(r[r > 0].astype(np.float64))
    _R_CACHE["N"], _R_CACHE["r"] = N, r
    return r


def image_sum_partial(alpha: float, R: float, L: float = 1.0) -> float:
    """S(R) = sum over 0 < |k|_2 <= R, k in Z^3, of (L|k|_2)^{-alpha}.

    This is the size of the image contribution to u_per(x) = sum_k u(x + Lk) at
    the cell centre for a profile with |u(y)| ~ (1+|y|)^{-alpha}: each image sits
    at distance ~ L|k| and contributes ~ (L|k|)^{-alpha}. Spherical truncation,
    so the asymptotic S(R) ~ 4 pi R^{3-alpha}/(3-alpha) has no shape correction.
    """
    r = _lattice_radii()
    i = int(np.searchsorted(r, R, side="right"))
    return float(np.sum((L * r[:i]) ** (-alpha)))


def _increment_exponent(alpha: float, radii=(12.0, 24.0, 48.0, 96.0)) -> float:
    """Fitted exponent of the SHELL INCREMENT S(2R) - S(R) ~ R^{3-alpha}.

    The increment, not the partial sum, is the right diagnostic: a partial sum
    of positive terms is monotone whatever alpha is, so its log-log slope cannot
    detect convergence. The increment's exponent changes sign exactly at the
    convergence threshold.
    """
    S = [image_sum_partial(alpha, R) for R in radii]
    d = [S[i + 1] - S[i] for i in range(len(S) - 1)]
    return float(np.polyfit(np.log(radii[:len(d)]), np.log(d), 1)[0])


def check_C() -> dict:
    cloc = _load(CLOC)
    b3 = cloc["check_B3_Lp_thresholds"]
    alpha_available = float(b3["banked_type_I_alpha"])        # 1.0, Chae-Wolf Type-I
    alpha_L2 = float(b3["L2_threshold_alpha"])                # 1.5, §4's requirement
    deficit_sec4 = float(b3["deficit_to_L2_in_exponent"])     # 0.5
    ratio_sec4 = float(b3["required_over_available_exponent_ratio"])  # 1.5

    radii = (12.0, 24.0, 48.0, 96.0)
    alphas = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    rows = []
    for a in alphas:
        S = [image_sum_partial(a, R) for R in radii]
        d = [S[i + 1] - S[i] for i in range(len(S) - 1)]
        slope = _increment_exponent(a, radii)
        pred = 3.0 - a
        rows.append({
            "alpha": a,
            "partial_sums_by_R": {str(R): float(s) for R, s in zip(radii, S)},
            "shell_increments": [float(v) for v in d],
            "measured_increment_exponent_in_R": slope,
            "predicted_increment_exponent_3_minus_alpha": pred,
            "abs_error": abs(slope - pred),
            "converges": bool(pred < 0.0),
        })

    # the alpha = 3 boundary case is logarithmic: constant increment per DOUBLING
    # of R, reported in leg 381's own idiom (it priced the L^3 tail the same way).
    doubl = [12.0, 24.0, 48.0, 96.0]
    S3 = [image_sum_partial(3.0, R) for R in doubl]
    incr = [S3[i + 1] - S3[i] for i in range(len(S3) - 1)]
    incr_spread = float(max(incr) - min(incr))

    # the torus size L is a PREFACTOR only: S(R, alpha, L) = L^{-alpha} S(R, alpha, 1).
    Ls = [1.0, 3.0, 10.0, 30.0]
    SL = [image_sum_partial(1.0, 24.0, L) for L in Ls]
    L_slope = float(np.polyfit(np.log(Ls), np.log(SL), 1)[0])

    # locate the convergence threshold from the MEASURED increment exponents, by
    # bisection -- the exponent changes sign exactly at the threshold.
    lo, hi = 2.0, 4.0
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        if _increment_exponent(mid, radii) > 0:
            lo = mid
        else:
            hi = mid
    alpha_crit = 0.5 * (lo + hi)

    deficit_per = alpha_crit - alpha_available
    ratio_per = alpha_crit / alpha_available

    # can_fail: assert against a DELIBERATELY WRONG prediction and show it fires
    a_test = 1.0
    slope_test = _increment_exponent(a_test, radii)
    wrong_pred = (3.0 - a_test) + 0.25
    TOL = 0.02

    return {
        "what_is_being_priced": (
            "the direct periodization u_per(x) = sum_{k in Z^3} u(x + Lk) of the R^3-anchored "
            "profile onto a torus of side L. This is the cheapest conceivable way to put the "
            "existing object on T^3: no cutoff, no modification, just wrap it."
        ),
        "rows": rows,
        "alpha_3_is_the_logarithmic_boundary": {
            "R_ladder": doubl,
            "partial_sums": [float(v) for v in S3],
            "increment_per_doubling_of_R": [float(v) for v in incr],
            "increment_spread": incr_spread,
            "reading": "constant increment per doubling of the image window, i.e. logarithmic "
                       "divergence -- the same signature leg 381 measured for the critical L^3 "
                       "tail (326.875 per decade, spread 7.4e-10).",
        },
        "torus_size_is_a_prefactor_not_a_cure": {
            "L_ladder": Ls,
            "S_at_alpha_1_R_24": [float(v) for v in SL],
            "measured_L_exponent": L_slope,
            "predicted_L_exponent": -1.0,
            "abs_error": abs(L_slope + 1.0),
            "reading": "S_N(alpha, L) = L^{-alpha} S_N(alpha, 1): enlarging the torus buys a "
                       "constant prefactor and does not change the N-divergence. No torus size "
                       "makes the image sum converge at alpha <= 3.",
        },
        "convergence_threshold_located_by_bisection_on_measured_exponents": alpha_crit,
        "THE_BILL": {
            "alpha_required_for_periodization_to_converge": alpha_crit,
            "alpha_required_by_section_4_bounded_energy_L2": alpha_L2,
            "alpha_available_a_priori_Type_I_Chae_Wolf": alpha_available,
            "deficit_periodization": deficit_per,
            "deficit_section_4": deficit_sec4,
            "ratio_periodization_required_over_available": ratio_per,
            "ratio_section_4_required_over_available": ratio_sec4,
            "REPURCHASE_FACTOR_IN_DEFICIT": deficit_per / deficit_sec4,
            "REPURCHASE_FACTOR_IN_RATIO": ratio_per / ratio_sec4,
            "currency_note": (
                "both bills are quoted in the SAME currency -- the far-field decay exponent "
                "alpha of the profile -- so they are directly comparable. §4's numbers are "
                "machine-read from writeup/data/p2_route_cloc_v1.json check_B3, not retyped."
            ),
        },
        "can_fail_wrong_prediction_planted": {
            "what_was_planted": f"predicted exponent {wrong_pred} instead of {3.0 - a_test} at alpha = {a_test}",
            "measured": slope_test,
            "abs_error_against_planted_prediction": abs(slope_test - wrong_pred),
            "tolerance": TOL,
            "fired": bool(abs(slope_test - wrong_pred) > TOL
                          and abs(slope_test - (3.0 - a_test)) < TOL),
        },
    }


# =============================================================================
# check_D -- the cut-then-periodize route, and what it inherits
# =============================================================================

def _cut_field(x, y, z, rho=1.0):
    """A smooth, compactly supported, EXACTLY divergence-free velocity field.

    u = curl(psi e_z) = (d psi/dy, -d psi/dx, 0) with psi = F(s) x y,
    F(s) = exp(-2/(1-s)) for s = |x|^2/rho^2 < 1 and 0 otherwise. Being a curl,
    div u = 0 identically; F is C^infinity and vanishes to infinite order at
    |x| = rho, so u is smooth and supported in the closed ball of radius rho.

    Returns (u_x, u_y): the third component is identically zero.
    """
    s = (x * x + y * y + z * z) / (rho * rho)
    inside = s < 1.0
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        one_minus = np.where(inside, 1.0 - s, 1.0)
        F = np.where(inside, np.exp(-2.0 / one_minus), 0.0)
        dF = np.where(inside, -2.0 / (one_minus * one_minus) * F, 0.0)
    ux = dF * (2.0 * y / rho ** 2) * x * y + F * x
    uy = -(dF * (2.0 * x / rho ** 2) * x * y + F * y)
    return ux, uy


def _cut_field_mag(x, y, z, rho=1.0):
    ux, uy = _cut_field(x, y, z, rho)
    return np.sqrt(ux * ux + uy * uy)


def check_D() -> dict:
    cloc = _load(CLOC)
    bill = cloc["check_C_cutoff_magnitudes"]["by_alpha"]["alpha=1.0"]["measured_rho_exponents"]
    l3 = cloc["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"]

    inherited = {
        "nonlinear_residual_L2_rho_exponent": bill["nonlinear_residual_L2"],
        "viscous_residual_L2_rho_exponent": bill["viscous_residual_L2"],
        "divergence_defect_L2_rho_exponent": bill["divergence_defect_L2"],
        "pressure_perturbation_at_origin_rho_exponent": bill["pressure_perturbation_at_origin"],
        "critical_L3_tail_increment_per_decade": l3["increment_per_decade"][0],
        "critical_L3_tail_increment_spread": l3["increment_per_decade_spread"],
        "machine_read_from": "writeup/data/p2_route_cloc_v1.json (leg 381)",
        "reading": (
            "UNCHANGED BY (D), every number. If the object is cut off before it is wrapped -- "
            "and check_B says it must be, since a non-constant exactly-DSS torus field does not "
            "exist -- then leg 381's entire cutoff bill is paid in full, including the critical "
            "L^3 tail that never gets small. What (D) deletes is the ACCEPTANCE TEST (7), not "
            "the cutoff analysis that §4 transferred to §5."
        ),
    }

    # -- image overlap of a COMPACTLY SUPPORTED cut field --------------------
    rho = 1.0
    n = 41
    g = np.linspace(-rho, rho, n)
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
    # the field is a curl, so div u = 0 identically; measured by 4th-order FD so
    # this is a measurement and not an assertion about the construction
    div_ladder = []
    for nn in (41, 81, 161, 321):
        gg = np.linspace(-rho, rho, nn)
        hh = gg[1] - gg[0]
        XX, YY, ZZ = np.meshgrid(gg, gg, gg, indexing="ij")
        uxx, uyy = _cut_field(XX, YY, ZZ, rho)
        dv = ((np.roll(uxx, -1, 0) - np.roll(uxx, 1, 0)) / (2 * hh)
              + (np.roll(uyy, -1, 1) - np.roll(uyy, 1, 1)) / (2 * hh))
        interior = (slice(2, -2),) * 3
        div_ladder.append({
            "n_per_axis": nn, "h": float(hh),
            "max_abs_divergence_fd2": float(np.max(np.abs(dv[interior]))),
            "field_sup": float(np.max(np.sqrt(uxx ** 2 + uyy ** 2))),
        })
    ratios = [div_ladder[i]["max_abs_divergence_fd2"] / div_ladder[i + 1]["max_abs_divergence_fd2"]
              for i in range(len(div_ladder) - 1)]
    div_max = div_ladder[-1]["max_abs_divergence_fd2"]
    field_max = div_ladder[-1]["field_sup"]

    overlap = []
    for L in (3.0, 2.5, 2.0001, 1.5, 1.0):
        acc = np.zeros_like(X)
        for kx in (-1, 0, 1):
            for ky in (-1, 0, 1):
                for kz in (-1, 0, 1):
                    if (kx, ky, kz) == (0, 0, 0):
                        continue
                    acc += _cut_field_mag(X + L * kx, Y + L * ky, Z + L * kz, rho)
        overlap.append({
            "L_over_rho": L / rho,
            "sup_image_velocity_contamination_in_the_cell": float(np.max(acc)),
            "relative_to_the_cell_field_sup": float(np.max(acc) / field_max),
            "images_disjoint_predicted": bool(L > 2.0 * rho),
        })

    # -- leading-multipole image PRESSURE interaction on the cubic lattice ---
    # A compactly supported field's far pressure field from an image at Lk is
    #   p_k(0) ~ T_ij(k) M_ij,  T_ij(k) = (3 k_i k_j/|k|^2 - delta_ij)/(4 pi L^3 |k|^3)
    # with M_ij = integral u_i u_j (a fixed tensor once the cutoff is chosen).
    # The MAGNITUDE sum over the lattice is log-divergent (|k|^{-3}); the SIGNED
    # sum is not, because a cubic shell cancels it.
    def shell_tensor_sum(N):
        g = np.arange(-N, N + 1)
        KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
        r2 = (KX ** 2 + KY ** 2 + KZ ** 2).astype(float)
        sel = (r2 > 0) & (np.maximum(np.maximum(np.abs(KX), np.abs(KY)), np.abs(KZ)) == N)
        kx, ky, kz, rr = KX[sel].astype(float), KY[sel].astype(float), KZ[sel].astype(float), r2[sel]
        r = np.sqrt(rr)
        T = np.zeros((3, 3))
        comps = [kx, ky, kz]
        for i in range(3):
            for j in range(3):
                T[i, j] = np.sum((3 * comps[i] * comps[j] / rr - (1.0 if i == j else 0.0))
                                 / (4 * np.pi * r ** 3))
        mag = float(np.sum(1.0 / (4 * np.pi * r ** 3)))
        return T, mag

    shells, cum = [], np.zeros((3, 3))
    mag_cum = 0.0
    for N in range(1, 33):
        T, mag = shell_tensor_sum(N)
        cum = cum + T
        mag_cum += mag
        shells.append({
            "shell_N": N,
            "shell_signed_tensor_max_abs": float(np.max(np.abs(T))),
            "cumulative_signed_tensor_max_abs": float(np.max(np.abs(cum))),
            "cumulative_magnitude_sum": mag_cum,
        })
    mags = np.array([s["cumulative_magnitude_sum"] for s in shells])
    # magnitude sum grows like log N: increment per DOUBLING tends to log 2,
    # because sum_{|k|<=N} 1/(4 pi |k|^3) ~ (4 pi/4 pi) log N = log N
    idx = [1, 3, 7, 15, 31]       # N = 2, 4, 8, 16, 32
    mag_incr = [float(mags[idx[i + 1]] - mags[idx[i]]) for i in range(len(idx) - 1)]
    mag_incr_predicted = float(np.log(2.0))

    # can_fail for the cancellation: break the cubic symmetry by summing a
    # HALF-lattice (k_x > 0 only) and show the signed sum stops cancelling.
    def half_lattice_signed(N):
        g = np.arange(-N, N + 1)
        KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
        r2 = (KX ** 2 + KY ** 2 + KZ ** 2).astype(float)
        sel = (r2 > 0) & (KX > 0)
        kx, rr = KX[sel].astype(float), r2[sel]
        r = np.sqrt(rr)
        return float(np.sum((3 * kx * kx / rr - 1.0) / (4 * np.pi * r ** 3)))

    return {
        "route": "cut off at radius rho first, then periodize on a torus of side L > 2 rho",
        "inherited_cutoff_bill_from_leg_381": inherited,
        "image_overlap_of_the_cut_field": {
            "field": "u = curl(psi e_z), psi = exp(-2/(1-|x|^2/rho^2)) x y, supported in |x| <= rho",
            "divergence_refinement_ladder": div_ladder,
            "divergence_error_ratios_per_halving": [float(v) for v in ratios],
            "divergence_reading": "the residual falls by ~4 per halving of h, i.e. it is second-"
                                  "order TRUNCATION error of the difference stencil and not a "
                                  "non-solenoidal field: u is a curl and div u = 0 identically",
            "measured_max_abs_divergence_fd2_finest": div_max,
            "field_sup": field_max,
            "rows": overlap,
            "reading": "with L > 2 rho the images have disjoint support and the DIRECT image "
                       "contamination of the cell is exactly zero. The cut-then-wrap route pays "
                       "no direct image term at all -- this is a CREDIT on (D)'s side.",
        },
        "image_pressure_interaction_leading_multipole": {
            "model": "p_image(0) ~ sum_{k != 0} T_ij(Lk) M_ij, T_ij = (3 k_i k_j/|k|^2 - d_ij)"
                     "/(4 pi L^3 |k|^3); leading multipole of the nonlocal pressure only, not "
                     "the full field",
            "shells": shells,
            "cumulative_signed_tensor_max_abs_at_N_32": float(np.max(np.abs(cum))),
            "cumulative_magnitude_sum_at_N_32": float(mags[-1]),
            "magnitude_increment_per_doubling_of_N": mag_incr,
            "magnitude_increment_per_doubling_predicted_log2": mag_incr_predicted,
            "magnitude_increment_relative_error_at_top_rung":
                abs(mag_incr[-1] - mag_incr_predicted) / mag_incr_predicted,
            "reading": (
                "the MAGNITUDE sum is logarithmically divergent (constant increment per doubling "
                "-- the third appearance of that signature in this ledger), but the SIGNED sum "
                "cancels shell by shell on the cubic lattice to machine precision. The pressure "
                "non-locality is therefore NOT the obstruction on T^3 either -- which is the same "
                "verdict leg 381 reached on R^3, by a different mechanism. CREDIT on (D)'s side."
            ),
            "can_fail_cubic_symmetry_broken": {
                "what_was_planted": "sum over the half-lattice k_x > 0 only, destroying the "
                                    "cubic symmetry that does the cancelling",
                "signed_sum_N_8": half_lattice_signed(8),
                "signed_sum_N_16": half_lattice_signed(16),
                "fired": bool(abs(half_lattice_signed(16)) > 1e-3),
            },
        },
    }


# =============================================================================
# check_E -- §2's four screen rows, machine-read under a pre-registered rule
# =============================================================================

# Pre-registered domain markers (journal §0 rule 2): whole-space structure that
# T^3 does not carry.
R3_MARKERS = [
    r"R\^3", r"R\^n", r"\bR3\b", r"L\^3\(R\^3\)", r"L\^q\(R\^3", r"M\(dot\)q",
    r"sup_\{?R>0\}?", r"Morrey", r"\(1\+\|y\|\)", r"decay", r"infinity",
]
# ansatz markers: the object class the theorem constrains is defined by the
# dilation action, which does not act on T^3 (check_B)
ANSATZ_MARKERS = [r"self-similar", r"self similar", r"discretely self", r"DSS",
                  r"rescaled", r"1\.6", r"lambda"]


def _scan(text: str, markers) -> list:
    hits = []
    for m in markers:
        if re.search(m, text, flags=re.IGNORECASE):
            hits.append(m)
    return hits


def _verdict(hyp: str, ansatz_bound_text: str) -> dict:
    r3 = _scan(hyp, R3_MARKERS)
    an = _scan(ansatz_bound_text, ANSATZ_MARKERS)
    marker_verdict = "R3-ONLY" if r3 else "CARRIES-TO-T3"
    ansatz_verdict = "R3-ONLY" if an else "CARRIES-TO-T3"
    combined = "R3-ONLY" if (r3 or an) else "CARRIES-TO-T3"
    return {
        "r3_markers_hit": r3,
        "ansatz_markers_hit": an,
        "marker_verdict": marker_verdict,
        "ansatz_class_verdict": ansatz_verdict,
        "combined_verdict": combined,
    }


def check_E() -> dict:
    rows = []

    # -- row 1: NRS 1996 / Tsai. Its landed record is the executable screen
    # itself: the quotation lives in solver/dssp_screen.py's ledger_nrs_tsai.
    src = SCREEN.read_text()
    m = re.search(r'"The "\s*\n?\s*"(main result of \[NRS\][^"]*)"', src)
    quote = None
    if m is None:
        # concatenated string literals: reassemble the neighbourhood verbatim
        i = src.find("main result of [NRS]")
        seg = src[i - 200: i + 400]
        quote = " ".join(re.findall(r'"([^"]*)"', seg))
    else:
        quote = m.group(1)
    rows.append({
        "row": "NRS 1996 / Tsai (T1/T2)",
        "landed_record": "solver/dssp_screen.py (legs 357/362/370), ledger_nrs_tsai()",
        "field_read": "the verbatim NRS quotation carried in the module source",
        "hypothesis_text_machine_read": quote,
        "ledger_text_in_obligations": "bind exactly-backward-self-similar profiles only; DSS at "
                                      "lambda >> 1 is outside the hypothesis (legs 253, 341)",
        **_verdict(quote, "exactly-backward-self-similar profiles; DSS"),
    })

    # -- row 2: Chae-Wolf / Pineau-Vicol, leg 330
    pv = _load(PVLX)
    clauses = {c["id"]: c for c in pv["clause_by_clause"]}
    deciding = next(c for c in pv["clause_by_clause"] if "DECIDING" in c["verdict"].upper())
    ceiling = pv["magnitudes_of_near_1"][0]["value_lambda_ceiling"]
    hyp_pv = clauses["H1"]["hypothesis_quote"] + " | " + clauses["H2"]["hypothesis_quote"]
    rows.append({
        "row": "Chae-Wolf / Pineau-Vicol",
        "landed_record": "writeup/data/p2_route_pvlx_v1.json (leg 330, 5496bbc)",
        "field_read": "clause_by_clause[H1,H2,H5] and magnitudes_of_near_1[M1].value_lambda_ceiling",
        "hypothesis_text_machine_read": hyp_pv,
        "deciding_clause_id": deciding["id"],
        "deciding_clause_quote": deciding["hypothesis_quote"],
        "lambda_ceiling_machine_read": ceiling,
        **_verdict(hyp_pv, clauses["H3"]["hypothesis_quote"]),
    })

    # -- row 3: Chae-Tsai, leg 326
    ct = _load(CTRX)
    ledger = ct["gate"]["clause_ledger"]
    decisive = next(k for k, v in ledger.items()
                    if isinstance(v, dict) and v.get("decisive") is True)
    hyp_ct = ct["theorem_read"]["equation_1_6_verbatim"] + " | " + ct["theorem_read"]["equation_1_6_is"]
    rows.append({
        "row": "Chae-Tsai",
        "landed_record": "writeup/data/p2_route_ctrx_v1.json (leg 326, c541cdb)",
        "field_read": f"gate.clause_ledger.{decisive}.verdict and theorem_read.equation_1_6_*",
        "hypothesis_text_machine_read": hyp_ct,
        "decisive_clause": decisive,
        "decisive_clause_verdict": ledger[decisive]["verdict"],
        "gate_branch": ct["gate"]["branch"],
        **_verdict(hyp_ct, ct["theorem_read"]["label"] + " time periodic solution of (1.6) "
                   + ct["theorem_read"]["equation_1_6_is"]),
    })

    # -- row 4: Morrey (Jiu-Wang-Wei), legs 368/370
    mr = _load(MRYX)
    th = mr["paper_theorems_read_at_primary_text"]
    hyp_mr = th["theorem_1_2"] + " | " + th["morrey_norm_definition"]
    rows.append({
        "row": "Morrey (Jiu-Wang-Wei arXiv:2006.15776)",
        "landed_record": "writeup/data/p2_route_mryx_v1.json (leg 368) + "
                         "writeup/data/p2_route_b7m_v1.json (leg 370 screen extension)",
        "field_read": "paper_theorems_read_at_primary_text.theorem_1_2 and .morrey_norm_definition",
        "hypothesis_text_machine_read": hyp_mr,
        "classification_verdict": mr["classification"]["verdict"],
        "classification_scope": mr["classification"]["scope"],
        **_verdict(hyp_mr, mr["classification"]["scope"]),
    })

    n_r3 = sum(1 for r in rows if r["combined_verdict"] == "R3-ONLY")
    n_carry = len(rows) - n_r3

    # can_fail: a planted control row whose hypothesis has NO whole-space marker
    # and NO ansatz marker must come out CARRIES-TO-T3. Without this the rule
    # could be one that returns R3-ONLY for everything.
    control_pos = _verdict("a smooth solution of the heat equation with bounded gradient",
                           "no ansatz assumed")
    control_neg = _verdict("a weak solution in L^3(R^3)", "backward self-similar")

    return {
        "rule_applied": (
            "PRE-REGISTERED (journal §0 rule 2): a row is R3-ONLY if the hypothesis text in its "
            "landed record invokes whole-space structure T^3 does not carry, OR if the object "
            "class it constrains is defined by the dilation action check_B shows does not act "
            "on T^3. Both sub-verdicts are reported separately and never netted into one word."
        ),
        "markers_r3": R3_MARKERS,
        "markers_ansatz": ANSATZ_MARKERS,
        "rows": rows,
        "tally": {
            "rows_total": len(rows),
            "R3_ONLY": n_r3,
            "CARRIES_TO_T3": n_carry,
            "clearances_that_carry_to_T3": n_carry,
        },
        "what_the_tally_means": (
            "§2 is described in CLAY_OBLIGATIONS.md as 'LARGELY DISCHARGED, and this is the "
            "programme's strongest position'. Under (D) that position does not transfer: the "
            "screen's clearances were secured against R^3 hypotheses about an R^3 object. A "
            "torus screen would have to be rebuilt against the PERIODIC rigidity literature, "
            "which this repository has never searched. This is the known cost side and it is "
            "reported as a count, not as a word."
        ),
        "can_fail_planted_control_rows": {
            "positive_control_no_markers_expected_CARRIES": control_pos["combined_verdict"],
            "negative_control_full_markers_expected_R3_ONLY": control_neg["combined_verdict"],
            "fired": bool(control_pos["combined_verdict"] == "CARRIES-TO-T3"
                          and control_neg["combined_verdict"] == "R3-ONLY"),
        },
    }


# =============================================================================
# check_F -- the §1-§5 disposition table
# =============================================================================

def obligations_sections() -> dict:
    """Read CLAY_OBLIGATIONS.md (READ ONLY) and split out §1..§5."""
    text = OBLIG.read_text()
    parts = re.split(r"\n## ", text)
    out = {}
    for p in parts:
        m = re.match(r"§(\d) — ", p)
        if m:
            out[f"section_{m.group(1)}"] = p
    return out, hashlib.sha256(text.encode()).hexdigest()


def check_F(A, B, C, D, E) -> dict:
    secs, sha = obligations_sections()
    pocp = _load(POCP)
    census = pocp["domain_census"]

    bill = C["THE_BILL"]
    table = [
        {
            "section": "§1 — the profile exists (rigorous enclosure)",
            "disposition": "UNCHANGED",
            "magnitude_or_pointer": {
                "why_unchanged": "the enclosure problem is a statement about a profile equation "
                                 "and its linearisation; (D) changes the ACCEPTANCE conditions of "
                                 "the assembled solution, not the enclosure.",
                "credit_on_D_side": "leg 348's obstruction for §1 is that every located "
                                    "periodic-orbit certification instance closes its tail "
                                    "estimate against a COMPACT domain. A torus IS that domain.",
                "located_instances_compact_or_periodic": len(census["compact_or_periodic_domain"]),
                "located_instances_unbounded_with_algebraic_decay": len(
                    census["unbounded_domain_with_algebraic_decay"]),
                "located_instances_unbounded_periodic_orbit_any_weight": len(
                    census["unbounded_domain_periodic_orbit_any_weight"]),
                "record": "writeup/data/p2_route_pocp_v1.json (leg 348), domain_census",
                "the_catch_stated_plainly": "that credit is only collectable by an object that "
                                            "LIVES on the torus, and check_B measures that a "
                                            "non-constant exactly-DSS torus field does not exist. "
                                            "The credit and the obstruction are about different "
                                            "objects and this leg does not net them.",
            },
        },
        {
            "section": "§2 — the profile is admissible (rigidity screen)",
            "disposition": "TRANSFERRED",
            "magnitude_or_pointer": {
                "rows_total": E["tally"]["rows_total"],
                "rows_that_carry_to_T3_as_clearances": E["tally"]["CARRIES_TO_T3"],
                "rows_R3_only": E["tally"]["R3_ONLY"],
                "transferred_to": "a torus rigidity screen against the periodic literature, "
                                  "which this repository has never searched (novelty pass §1)",
                "record": "per-row landed records listed in check_E.rows[*].landed_record",
            },
        },
        {
            "section": "§3 — the profile generates a genuine NS solution",
            "disposition": "TRANSFERRED",
            "magnitude_or_pointer": {
                "what_transfers": "the Biot-Savart / pressure reconstruction must be redone with "
                                  "the PERIODIC Green's function; leg 351's closed-form R^3 swirl "
                                  "potential is not the torus one.",
                "image_pressure_magnitude_sum_is_log_divergent_increment_per_doubling":
                    D["image_pressure_interaction_leading_multipole"]
                     ["magnitude_increment_per_doubling_of_N"],
                "but_signed_sum_cancels_cumulative_max_abs_at_N_32":
                    D["image_pressure_interaction_leading_multipole"]
                     ["cumulative_signed_tensor_max_abs_at_N_32"],
                "direct_image_contamination_when_L_exceeds_2rho":
                    D["image_overlap_of_the_cut_field"]["rows"][0][
                        "sup_image_velocity_contamination_in_the_cell"],
                "reading": "the periodization terms §3 must absorb are measured SMALL or exactly "
                           "zero at leading multipole order. §3 is the cheap transfer.",
            },
        },
        {
            "section": "§4 — finite energy and the localisation problem",
            "disposition": "VACATED-AS-AN-ACCEPTANCE-TEST, TRANSFERRED-AS-WORK",
            "magnitude_or_pointer": {
                "vacated_part": "condition (7) does not appear in (D)'s own text -- machine-read, "
                                "check_A: exactly one condition dropped going (C) -> (D), and it "
                                "is (7) bounded energy.",
                "transferred_part_route_1_wrap_the_uncut_profile": {
                    "alpha_required": bill["alpha_required_for_periodization_to_converge"],
                    "alpha_required_by_section_4": bill["alpha_required_by_section_4_bounded_energy_L2"],
                    "alpha_available": bill["alpha_available_a_priori_Type_I_Chae_Wolf"],
                    "deficit_periodization": bill["deficit_periodization"],
                    "deficit_section_4": bill["deficit_section_4"],
                    "REPURCHASE_FACTOR_IN_DEFICIT": bill["REPURCHASE_FACTOR_IN_DEFICIT"],
                },
                "transferred_part_route_2_cut_then_wrap": {
                    "inherits": "leg 381's cutoff bill in full and unchanged",
                    "critical_L3_tail_increment_per_decade":
                        D["inherited_cutoff_bill_from_leg_381"]["critical_L3_tail_increment_per_decade"],
                    "note": "the cutoff analysis §4 transferred to §5 is performed IDENTICALLY "
                            "under (D); only the final acceptance test changes.",
                },
                "why_a_route_must_be_chosen": "check_B: a non-constant exactly-DSS field on T^3 "
                                              "does not exist, so route 1 is not available to an "
                                              "exactly-DSS object at all -- it is priced here "
                                              "because it is the cheapest conceivable wrap and "
                                              "the number is what makes the comparison legible.",
            },
        },
        {
            "section": "§5 — stability / persistence under localisation",
            "disposition": "UNCHANGED",
            "magnitude_or_pointer": {
                "why_unchanged": "leg 314's residual obligation is a high-frequency resolvent "
                                 "bound on |Im mu| -> infinity -- a statement about the "
                                 "linearisation's spectrum at large frequency, not about the "
                                 "ambient domain.",
                "r3_markers_in_section_5_text": _scan(secs["section_5"], [r"R\^3", r"R\^n"]),
                "record": "CLAY_OBLIGATIONS.md §5 (read, never edited), sha256 below",
                "note": "under route 2 the perturbation §5 must survive is the SAME cutoff "
                        "perturbation, so §5's content is untouched; under route 1 it would be a "
                        "periodization perturbation instead, but route 1 has no object.",
            },
        },
    ]

    dispositions = [t["disposition"] for t in table]
    every_named = all(
        d.startswith("VACATED") or d == "UNCHANGED" or d.startswith("TRANSFERRED")
        for d in dispositions)
    transferred_priced = all(
        isinstance(t["magnitude_or_pointer"], dict) and len(t["magnitude_or_pointer"]) > 0
        for t in table if t["disposition"].startswith("TRANSFERRED")
        or t["disposition"].startswith("VACATED"))

    return {
        "obligations_file_sha256_READ_ONLY": sha,
        "table": table,
        "gate_clause_1_every_section_named_or_priced": bool(every_named and transferred_priced),
        "section_6_status": {
            "item_1_certified_far_field_decay_and_admissible_cutoff": "OPEN",
            "item_2_persistence_stability_under_localisation": "OPEN",
            "unchanged_by_this_leg": True,
            "note": "and §6 item 1 is if anything MORE load-bearing under (D): the certified "
                    "far-field exponent alpha is the currency of the periodization bill too.",
        },
    }


# =============================================================================

def main() -> int:
    A = check_A()
    B = check_B()
    C = check_C()
    D = check_D()
    E = check_E()
    F = check_F(A, B, C, D, E)

    gate_1 = F["gate_clause_1_every_section_named_or_priced"]
    gate_2 = all(("combined_verdict" in r and r.get("landed_record")) for r in E["rows"]) \
        and E["tally"]["rows_total"] == 4
    answer = "yes" if (gate_1 and gate_2) else "no"

    bill = C["THE_BILL"]
    out = {
        "leg": 390,
        "route": "DTOR",
        "title": "Does Fefferman statement (D) (breakdown on R^3/Z^3) delete "
                 "CLAY_OBLIGATIONS §4, or re-price it?",
        "kind": "scoping / arithmetic. Reading and arithmetic; no outreach; edits no "
                "obligations file, no solver module, no capabilities row.",
        "ceiling": "TIER 2 in both gate branches. §6's two no-method obligations stay OPEN. "
                   "No link of the L1 -> L4 chain moved. Clay stays ~0.05%.",
        "THE_RETARGET_DECISION_IS_THE_USERS_AND_THIS_LEG_MAKES_NONE": True,
        "no_recommendation_is_written_anywhere_in_this_artifact": True,
        "novelty_log": "writeup/novelty/leg_390.md (committed before the runner existed)",
        "journal": "experiments/journal/leg_390.md (gate pre-committed, immutable)",
        "figure": "fig106 (allocated at dispatch; rebuilt by "
                  "experiments/p2_route_dtor_v1_evidence.py from this JSON alone)",
        "check_A_acceptance_condition_diff": A,
        "check_B_dss_and_periodicity_are_incompatible": B,
        "check_C_periodization_bill": C,
        "check_D_cut_then_periodize": D,
        "check_E_section_2_four_rows": E,
        "check_F_section_1_to_5_disposition": F,
        "gate": {
            "question": "Does the (D)-variant ledger re-derive with every §1-§5 obligation either "
                        "named-as-vacated or priced-as-transferred, AND does the §2 enumeration "
                        "close with each row's R^3-only / carries-to-T^3 verdict tied to its "
                        "landed record?",
            "clause_1_ledger_rederives": gate_1,
            "clause_2_section_2_enumeration_closes": gate_2,
            "answer": answer,
            "yes_branch_deliverable": {
                "is_section_4_deletion_repurchased_by_periodization": (
                    "The DELETION IS REAL AND THE WORK IS NOT DELETED. (7) is absent from (D)'s "
                    "own text, so bounded energy stops being an acceptance test. But the object "
                    "is R^3-anchored and cannot be made exactly DSS on T^3 at all, so it must "
                    "still be localised -- and leg 381's cutoff bill is then paid in full and "
                    "unchanged, critical L^3 tail included. Priced as a magnitude: wrapping the "
                    "UNCUT profile needs alpha > "
                    f"{bill['alpha_required_for_periodization_to_converge']:.4f} against §4's "
                    f"alpha > {bill['alpha_required_by_section_4_bounded_energy_L2']} on the same "
                    f"a-priori alpha = {bill['alpha_available_a_priori_Type_I_Chae_Wolf']}: "
                    f"deficit {bill['deficit_periodization']:.4f} against "
                    f"{bill['deficit_section_4']}, a repurchase factor of "
                    f"{bill['REPURCHASE_FACTOR_IN_DEFICIT']:.4f} in deficit and "
                    f"{bill['REPURCHASE_FACTOR_IN_RATIO']:.4f} in ratio."
                ),
                "which_section_2_rows_re_open": (
                    f"{E['tally']['R3_ONLY']} of {E['tally']['rows_total']} rows are R^3-only, so "
                    f"{E['tally']['CARRIES_TO_T3']} clearances carry to T^3. §2's screen re-opens "
                    "in full and would have to be rebuilt against a periodic rigidity literature "
                    "this repository has never searched."
                ),
                "the_other_direction_reported_at_the_same_strength": (
                    "§1's named obstruction (leg 348) is that "
                    f"{len(_load(POCP)['domain_census']['compact_or_periodic_domain'])} of the "
                    "located periodic-orbit certification instances close against a COMPACT "
                    "domain and "
                    f"{len(_load(POCP)['domain_census']['unbounded_domain_periodic_orbit_any_weight'])}"
                    " against an unbounded one. A torus target sits on the right side of that "
                    "census. This leg reports it and nets it against nothing."
                ),
            },
            "clay_movement": "none. Clay stays ~0.05%.",
        },
        "can_fail_summary": {
            "check_A_planted_seven_back_into_D": A["can_fail_planted_seven_back_into_D"]["fired"],
            "check_B_lambda_equals_one_control": B["can_fail_lambda_equals_one_control"]["fired"],
            "check_C_wrong_prediction_planted": C["can_fail_wrong_prediction_planted"]["fired"],
            "check_D_cubic_symmetry_broken": D["image_pressure_interaction_leading_multipole"][
                "can_fail_cubic_symmetry_broken"]["fired"],
            "check_E_planted_control_rows": E["can_fail_planted_control_rows"]["fired"],
        },
        "corrections_routed_to_integration_verbatim_not_applied_here": [
            "CLAY_OBLIGATIONS.md's (D) paragraph says (D) 'carries no decay condition and no "
            "bounded-energy condition'. Machine-read against (D)'s own banked text, the precise "
            "statement is narrower and should be recorded as such: (D)'s SOLUTION conditions are "
            "(1),(2),(3),(10),(11) and contain no (7); its DATA conditions are (8),(9), whose "
            "verbatim text is NOT in this repository, so no claim about what they do or do not "
            "require is supportable here.",
            "writeup/data/p2_route_cloc_v1.json check_D_clay_primary_text.verbatim_conditions "
            "banks (4),(5),(6),(7),(10),(11),(A),(C),(D) but not (8),(9). A leg with outreach "
            "should close that gap.",
            "CLAY_OBLIGATIONS.md §2 calls the screen 'the programme's strongest position'. That "
            "is true of the R^3 target and, per check_E, of no torus target: the sentence is "
            "correct as written and would need a scope word if (D) were ever adopted.",
        ],
    }

    OUT.write_text(json.dumps(out, indent=1))
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"GATE: {answer}")
    print(f"  periodization threshold alpha > {bill['alpha_required_for_periodization_to_converge']:.6f}"
          f"  vs §4's alpha > {bill['alpha_required_by_section_4_bounded_energy_L2']}"
          f"  on available alpha = {bill['alpha_available_a_priori_Type_I_Chae_Wolf']}")
    print(f"  repurchase factor in deficit: {bill['REPURCHASE_FACTOR_IN_DEFICIT']:.6f}")
    print(f"  §2 rows: {E['tally']['R3_ONLY']} R^3-only, {E['tally']['CARRIES_TO_T3']} carry to T^3")
    print(f"  can_fail all fired: {all(out['can_fail_summary'].values())}")
    print("  THE RETARGET DECISION IS THE USER'S AND THIS LEG MAKES NONE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
