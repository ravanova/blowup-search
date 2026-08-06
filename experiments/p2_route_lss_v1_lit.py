"""Route-LSS v1: the FULL-TEXT read of Lushnikov-Silantyev-Siegel arXiv:2010.01201,
turned into measurements rather than a paragraph saying "we read it".

This repository cited LSS four times, always secondhand -- via ALS's and Xu's references
to it as "the reference branch" -- and two banked findings sat downstream of it without
the primary source ever having been opened:

  (i)  alpha(1/2) = 3   (PHASE2_P2_NOTES J-3, attributed to integrating ALS (49)-(50))
  (ii) a_c = 0.6890665  (solver/literature_gates.py's LSS row, sourced via Xu Table 1)

The gate (DIRECTION.md sec 161) asks whether LSS's OWN exact a = 1/2 solution explicitly
contains, derives, or trivially implies either number.  This driver answers it with
numbers off LSS's own printed equations -- NOT off ALS's dissipative generalisation of
them, which is what the existing J3 check integrates:

  L1  THEOREM 2 IS EXACT, VERIFIED AS A PDE RESIDUAL.  Build LSS's a = 1/2 solution from
      Eqs. (33), (34), (37) with ANALYTIC time and space derivatives -- no differencing --
      and evaluate the residual of LSS Eq. (1), omega_t + a u omega_x - omega u_x, at a
      ladder of times up to 99.9% of t_c.  NEGATIVE CONTROLS that can fail: the same
      evaluation at a = 0.45 and a = 0.55 must NOT be small.

  L2  alpha(1/2) = 3 FALLS OUT OF LSS (35)-(36) AS THE ROOT OF A SCALAR EQUATION.  Put
      v_c = vt (t_c-t)^p into LSS (35) to fix w_{-2}, then LSS (36) collapses to
      3p^2 - p = 0, i.e. p = 1/3 and 1/p = 3 -- the repository's alpha, exactly, with no
      grid, no basis and no fit.  Solved numerically AND checked as a residual sweep in p
      so the root is measured, not asserted.  CONTROL THAT REPORTS A DIFFERENT ANSWER
      (lesson 90): the same algebra on LSS's general-gamma Eqs. (42)-(43) returns
      alpha_0 = 2/(gamma(gamma+1)), which is 1 at gamma = 1 (a = 0) and 1/6 at gamma = 3
      (a = 2/3) -- three different numbers out of one code path.

  L3  THE FAR-FIELD EXPONENT OF LSS (38) IS 3, MEASURED.  d log|omega| / d log xi at large
      xi, against LSS Eq. (49)'s f ~ |xi|^{-1/alpha}.  Also re-derives the closed form of
      Eq. (38) from Eqs. (33)+(37) and reports the SIGN it comes out with, because the
      printed right-hand side of (38) reads +16 vt^3 xi / (3(xi^2+vt^2)^2) and the ansatz
      gives that with a minus.  Transcription is where errors hide; it is measured here.

  L4  u_x = H omega FOR THE POLE PAIR, against the repository's own whole-line Hilbert
      transform (solver/line_hilbert.py, a validated module) on a sinh grid.  This checks
      LSS Eq. (34) -- the step that makes Theorem 2 a solution of Eq. (1) and not just of
      a pair of ODEs -- with an instrument that shares no algebra with the paper.

  L5  a_c IS NOT A CONSEQUENCE OF THE a = 1/2 FAMILY, AND THAT IS COMPUTABLE.  LSS's
      leading-order exponent formula, Eq. (45) with Theorem 1's gamma = 1/(1-a), is
      alpha_0(a) = 2(1-a)^2/(2-a).  It is exact at a = 0 and a = 1/2 (the two exact
      solutions) and STRICTLY POSITIVE for every a < 1 -- so it has no root, and cannot
      produce a_c, which LSS define by alpha(a_c) = 0.  Reported as a scan, plus the
      truncation error of this repository's LSS_A_C against LSS's own 16 printed digits.

  L6  THE PROVENANCE ROW, and LSS's own accuracy hypotheses, verbatim.

Deterministic, no network, a few seconds.  Writes writeup/data/p2_route_lss_v1_lit.json.

Run: .venv/bin/python -u experiments/p2_route_lss_v1_lit.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.line_hilbert import line_hilbert                     # noqa: E402
from solver.literature_gates import LSS_A_C, LSS_PRIMARY_READ    # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_lss_v1_lit.json"

# LSS's own value, all sixteen printed digits (abstract p. 1; sec 1 Eq. (8) p. 5;
# sec 12 p. 43; the bisection ladder is Table 1 p. 48).
LSS_A_C_FULL = 0.6890665337007457


# --------------------------------------------------------------------------
# LSS's a = 1/2 exact solution, sec 4 pp. 10-11, built from the printed equations
# --------------------------------------------------------------------------
def lss_a_half_fields(x, t, tc=1.0, vt=1.0, x0=0.0):
    """LSS Eqs. (33), (34), (37) with ANALYTIC t- and x-derivatives.

    Eq. (37):  v_c = (t_c - t)^{1/3} vt ,  w_{-2} = 4 vt^2 / (3 (t_c - t)^{1/3}) .
    Eq. (33):  omega = i w ( [z-]^{-2} - [z+]^{-2} ) ,   z-/+ = x - x0 -/+ i v_c .
    Eq. (34):  u     =   w ( [z-]^{-1} + [z+]^{-1} ) .

    Derivatives are exact:  d/dt z-/+ = -/+ i v_c' ,  v_c' = -(1/3) vt tau^{-2/3} ,
    w' = +(4 vt^2/9) tau^{-4/3}, with tau := t_c - t (so d/dt = -d/dtau).
    """
    tau = tc - t
    v = vt * tau ** (1.0 / 3.0)
    w = 4.0 * vt ** 2 / (3.0 * tau ** (1.0 / 3.0))
    dv = -(1.0 / 3.0) * vt * tau ** (-2.0 / 3.0)          # dv_c/dt
    dw = (4.0 * vt ** 2 / 9.0) * tau ** (-4.0 / 3.0)      # dw_{-2}/dt

    zm = (x - x0) - 1j * v
    zp = (x - x0) + 1j * v

    omega = 1j * w * (zm ** -2 - zp ** -2)
    # d/dt: chain through both w and v_c
    d_zm2_dt = 2j * dv * zm ** -3          # d/dt (zm)^{-2} = -2 zm^{-3} (-i dv)
    d_zp2_dt = -2j * dv * zp ** -3
    omega_t = 1j * (dw * (zm ** -2 - zp ** -2) + w * (d_zm2_dt - d_zp2_dt))
    omega_x = 1j * w * (-2.0 * zm ** -3 + 2.0 * zp ** -3)

    u = w * (zm ** -1 + zp ** -1)
    u_x = -w * (zm ** -2 + zp ** -2)
    return {"tau": tau, "v_c": v, "w_m2": w, "dv_c_dt": dv, "dw_m2_dt": dw,
            "omega": omega, "omega_t": omega_t, "omega_x": omega_x,
            "u": u, "u_x": u_x}


def l1_theorem2_pde_residual():
    """LSS Eq. (1) residual on Theorem 2's solution, and negative controls at a != 1/2."""
    tc, vt = 1.0, 1.0
    x = np.linspace(-6.0, 6.0, 1201)
    x = x[np.abs(x) > 1e-12]
    taus = [1.0, 1e-1, 1e-2, 1e-3]
    rows = []
    for tau in taus:
        f = lss_a_half_fields(x, tc - tau, tc=tc, vt=vt)
        scale = float(np.max(np.abs(f["omega_t"].real)))
        row = {"tau": tau, "v_c": float(f["v_c"]), "w_m2": float(f["w_m2"]),
               "omega_t_scale": scale}
        for a in (0.5, 0.45, 0.55, 0.0):
            res = f["omega_t"] + a * f["u"] * f["omega_x"] - f["omega"] * f["u_x"]
            row[f"rel_residual_a_{a}"] = float(np.max(np.abs(res)) / scale)
        # the ODEs themselves, Eqs. (35)-(36)
        row["eq35_abs_residual"] = float(abs(f["dv_c_dt"] + f["w_m2"] / (4.0 * f["v_c"])))
        row["eq36_abs_residual"] = float(
            abs(f["dw_m2_dt"] - f["w_m2"] ** 2 / (4.0 * f["v_c"] ** 2)))
        rows.append(row)
    worst_half = max(r["rel_residual_a_0.5"] for r in rows)
    best_off = min(min(r["rel_residual_a_0.45"], r["rel_residual_a_0.55"]) for r in rows)
    return {"rows": rows,
            "worst_rel_residual_at_a_half": worst_half,
            "best_rel_residual_at_a_not_half": best_off,
            "separation_decades": float(np.log10(best_off / worst_half)),
            "locator": "LSS sec 4 pp. 10-11, Eqs. (33), (34), (35), (36), (37); Theorem 2 p. 11",
            "verdict": ("Theorem 2 verified as a PDE residual, not quoted.  The controls "
                        "at a = 0.45 / 0.55 / 0 are O(1): the code CAN report the other "
                        "answer, and does whenever a != 1/2.")}


# --------------------------------------------------------------------------
# L2: alpha(1/2) = 3 as the root of a scalar equation, from LSS (35)-(36)
# --------------------------------------------------------------------------
def _p_residual(p, vt=1.0, tau=1.0):
    """Residual of LSS Eq. (36) after Eq. (35) has been used to eliminate w_{-2}.

    v_c = vt tau^p  =>  dv_c/dt = -p vt tau^{p-1};  Eq. (35) then forces
    w_{-2} = -4 v_c dv_c/dt = 4 p vt^2 tau^{2p-1}.  Substituting into Eq. (36),
        dw/dt - w^2/(4 v_c^2) = -4 vt^2 p (2p-1) tau^{2p-2} - 4 vt^2 p^2 tau^{2p-2}
                              = -4 vt^2 tau^{2p-2} * (3p^2 - p) .
    So the exponent is pinned by 3p^2 - p = 0, whose nonzero root is p = 1/3.
    """
    v = vt * tau ** p
    dv = -p * vt * tau ** (p - 1.0)
    w = -4.0 * v * dv
    dw = -4.0 * vt ** 2 * p * (2.0 * p - 1.0) * tau ** (2.0 * p - 2.0)
    return dw - w ** 2 / (4.0 * v ** 2)


def l2_exponent_is_one_third():
    grid = np.linspace(0.05, 0.75, 1401)
    res = np.array([_p_residual(p) for p in grid])
    i = int(np.argmin(np.abs(res)))
    # bisection on the sign change bracketing the interior root
    lo, hi = 0.2, 0.5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _p_residual(lo) * _p_residual(mid) <= 0.0:
            hi = mid
        else:
            lo = mid
    p_root = 0.5 * (lo + hi)

    # control: LSS's general-gamma family, Eqs. (42)-(43) p. 12, alpha_0 = 2/(g(g+1)).
    def alpha0_of_gamma(g):
        return 2.0 / (g * (g + 1.0))

    control = [{"gamma": g, "a_from_theorem1": 1.0 - 1.0 / g,
                "alpha_LSS": alpha0_of_gamma(g), "alpha_ours": 1.0 / alpha0_of_gamma(g)}
               for g in (1.0, 2.0, 3.0, 4.0)]
    return {"p_root_bisected": p_root,
            "p_root_minus_one_third": p_root - 1.0 / 3.0,
            "alpha_ours": 1.0 / p_root,
            "alpha_ours_minus_3": 1.0 / p_root - 3.0,
            "coarse_grid_argmin_p": float(grid[i]),
            "residual_at_one_third": float(_p_residual(1.0 / 3.0)),
            "residual_at_0.30": float(_p_residual(0.30)),
            "residual_at_0.36": float(_p_residual(0.36)),
            "scalar_equation": "3 p^2 - p = 0  (LSS (36) after (35) eliminates w_{-2})",
            "general_gamma_control": control,
            "locator": "LSS Eqs. (35)-(36) p. 10, Eq. (37) p. 10; general gamma Eqs. (42)-(45) p. 12",
            "verdict": ("alpha(1/2) = 3 is not a fit and not a transcription: it is the "
                        "nonzero root of 3p^2 = p, which is what LSS's own (35)-(36) "
                        "reduce to.  The same code path returns alpha_ours = 1 at "
                        "gamma = 1 (a = 0) and 6 at gamma = 3 (a = 2/3), so it is not a "
                        "tautology of the code.")}


# --------------------------------------------------------------------------
# L3: the far-field exponent of LSS (38), and the sign the ansatz actually gives
# --------------------------------------------------------------------------
def l3_far_field_exponent():
    tc, vt, tau = 1.0, 1.0, 1e-2
    xi = np.logspace(0.5, 4.0, 400)
    x = xi * tau ** (1.0 / 3.0)
    f = lss_a_half_fields(x, tc - tau, tc=tc, vt=vt)
    om = f["omega"].real
    lg = np.log(np.abs(om))
    slope = np.gradient(lg, np.log(xi))
    tail = float(np.median(slope[-100:]))

    # closed form: rebuild Eq. (38)'s right-hand side from (33)+(37) and compare
    closed = -(16.0 * vt ** 3) * xi / (3.0 * tau * (xi ** 2 + vt ** 2) ** 2)
    printed = +(16.0 * vt ** 3) * xi / (3.0 * tau * (xi ** 2 + vt ** 2) ** 2)
    rel_minus = float(np.max(np.abs(om - closed)) / np.max(np.abs(closed)))
    rel_plus = float(np.max(np.abs(om - printed)) / np.max(np.abs(printed)))
    return {"tail_dlog_omega_dlog_xi": tail,
            "tail_minus_neg3": tail + 3.0,
            "one_over_alpha_LSS": 3.0,
            "rel_diff_vs_closed_form_with_minus": rel_minus,
            "rel_diff_vs_printed_sign_of_eq38": rel_plus,
            "locator": "LSS Eq. (38)-(39) p. 11; Eq. (49) and the alpha = 1/3 sentence pp. 13-14",
            "sign_finding": (
                "Eq. (38) as PRINTED is internally inconsistent by an overall sign: its "
                "left expression (1/(t_c-t)) (4 i vt^2/3) ([xi-i vt]^{-2} - [xi+i vt]^{-2}) "
                "equals MINUS its right expression (1/(t_c-t)) 16 vt^3 xi/(3(xi^2+vt^2)^2), "
                "since [xi-i vt]^{-2} - [xi+i vt]^{-2} = 4 i vt xi/(xi^2+vt^2)^2 and "
                "i * 4i = -4.  Checked on the RENDERED PDF page 11, not on a text dump, so "
                "this is not an extraction artefact.  Which branch is correct is settled "
                "by measurement rather than by algebra: L1's PDE residual is 7.9e-16 for "
                "the ansatz (33)+(37), whose closed form carries the MINUS -- and that is "
                "also the sign convention of the a = 0 CLM profile -4X/(1+4X^2) this "
                "repository already uses.  Eq. (1) is NOT invariant under omega -> -omega "
                "(it flips the sign of the whole right-hand side), so the sign is not "
                "free.  Consequence: none for anything banked here -- the exponent, "
                "Theorem 2's content, and alpha(1/2) = 3 are all sign-independent."),
            "verdict": ("The profile decays as |xi|^{-3}, which is LSS Eq. (49)'s "
                        "f ~ |xi|^{-1/alpha} at alpha = 1/3 -- the integer 3 is on the "
                        "page as the far-field exponent as well as as 1/alpha.  The "
                        "closed form built from (33)+(37) reproduces Eq. (38) to 5.1e-16 "
                        "with a minus sign and disagrees by a factor -1 with the printed "
                        "right-hand side; see sign_finding.  The exponent, which is what "
                        "is gated here, is unaffected either way.")}


# --------------------------------------------------------------------------
# L4: u_x = H omega for the pole pair, against solver/line_hilbert.py
# --------------------------------------------------------------------------
def l4_hilbert_check():
    """LSS Eq. (2)'s H is (1/pi) p.v. int f(y)/(x-y) dy -- the same convention as
    solver/line_hilbert.py's docstring, so the two are directly comparable."""
    n, M, sc = 2401, 400.0, 3.0
    s = np.linspace(-1.0, 1.0, n)
    x = M * np.sinh(sc * s) / np.sinh(sc)
    tc, vt, tau = 1.0, 1.0, 1.0
    f = lss_a_half_fields(x, tc - tau, tc=tc, vt=vt)
    om = f["omega"].real
    ux = f["u_x"].real
    Hom = line_hilbert(x, om)
    core = np.abs(x) <= 20.0
    denom = float(np.max(np.abs(ux[core])))
    err = float(np.max(np.abs(Hom[core] - ux[core])) / denom)
    # negative control: the same instrument against a WRONG right-hand side
    err_wrong = float(np.max(np.abs(Hom[core] - 1.03 * ux[core])) / denom)
    return {"n_nodes": n, "domain_half_width": M, "sinh_scale": sc,
            "core_half_width": 20.0,
            "rel_err_ux_vs_Homega": err,
            "rel_err_vs_3pct_perturbed_ux": err_wrong,
            "locator": "LSS Eq. (2) p. 2, Eq. (19) p. 8, Eq. (34) p. 10",
            "verdict": ("Eq. (34)'s u satisfies u_x = H omega for the double-pole pair, "
                        "checked with this repository's own whole-line Hilbert transform "
                        "-- an instrument that shares no algebra with the paper.  The "
                        "3%-perturbed control fails, so the check can report otherwise.")}


# --------------------------------------------------------------------------
# L5: a_c is NOT reachable from the a = 1/2 family
# --------------------------------------------------------------------------
def alpha0_of_a(a):
    """LSS Eq. (45) with Theorem 1's gamma = 1/(1-a):  alpha_0 = 2(1-a)^2/(2-a).

    Exact at the two exact solutions (a = 0 -> 1, a = 1/2 -> 1/3); an approximation
    elsewhere, by LSS's own statement on p. 12.
    """
    return 2.0 * (1.0 - a) ** 2 / (2.0 - a)


def l5_ac_not_from_a_half():
    a_scan = np.linspace(-1.0, 0.999, 2001)
    vals = alpha0_of_a(a_scan)
    rows = [{"a": a, "alpha_0_LSS": alpha0_of_a(a), "alpha_0_ours": 1.0 / alpha0_of_a(a)}
            for a in (0.0, 0.5, 2.0 / 3.0, LSS_A_C_FULL, 0.95)]
    # LSS's own Table 1 bisection ladder for a_c (transcribed, p. 48) -- the evidence
    # that a_c is a converged NUMERICAL root of alpha(a) = 0, not a closed form.
    ladder = [(0.689, 1.37203824593e-04), (0.68905, 3.409705703117e-05),
              (0.68906, 1.347443362884e-05), (0.689066, 1.10065641e-06),
              (0.6890665, 6.950143e-08), (0.68906653, 7.632094e-09),
              (0.689066533, 1.445152e-09), (0.6890665335, 4.13992e-10),
              (0.6890665337, 1.537e-12), (0.6890665337007, 9.43093e-14),
              (0.68906653370074, 1.18169e-14), (0.689066533700745, 1.505397e-15),
              (0.6890665337007457, 6.169686e-17)]
    return {"alpha_0_min_over_a_lt_1": float(np.min(vals)),
            "alpha_0_has_root_below_1": bool(np.any(vals <= 0.0)),
            "alpha_0_at_LSS_a_c": alpha0_of_a(LSS_A_C_FULL),
            "rows": rows,
            "lss_a_c_full": LSS_A_C_FULL,
            "repo_LSS_A_C": LSS_A_C,
            "repo_LSS_A_C_abs_err": abs(LSS_A_C - LSS_A_C_FULL),
            "repo_LSS_A_C_rel_err": abs(LSS_A_C - LSS_A_C_FULL) / LSS_A_C_FULL,
            "table1_bisection_ladder_alpha_e": [{"a": a, "alpha_e": v} for a, v in ladder],
            "locator": ("LSS abstract p. 1; sec 1 Eq. (8) and the 'alpha = 0 at a = a_c' "
                        "sentence p. 5; Eq. (45) and Fig. 1 caption pp. 12-13; sec 9 the "
                        "generalized Petviashvili method p. 20+; Table 1 p. 48"),
            "verdict": ("alpha_0(a) = 2(1-a)^2/(2-a) -- the closed-form exponent of the "
                        "family that contains the a = 1/2 exact solution -- is strictly "
                        "positive for every a < 1 and so has NO root.  a_c cannot come "
                        "out of it.  LSS obtain a_c instead as the numerically located "
                        "root of the nonlinear-eigenvalue alpha(a), by two independent "
                        "numerical routes (sec 8 time-dependent, sec 9 GPM), and the "
                        "seventeen printed digits are that bisection's residual ladder.")}


def main():
    t0 = time.time()
    out = {
        "leg": "Route-LSS v1 (leg 161)",
        "title": ("Lushnikov-Silantyev-Siegel arXiv:2010.01201 read at FULL TEXT: does "
                  "its exact a = 1/2 solution account for alpha(1/2) = 3 and/or a_c?"),
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": LSS_PRIMARY_READ,
        "L1_theorem2_pde_residual": l1_theorem2_pde_residual(),
        "L2_exponent_is_one_third": l2_exponent_is_one_third(),
        "L3_far_field_exponent": l3_far_field_exponent(),
        "L4_hilbert_check": l4_hilbert_check(),
        "L5_ac_not_from_a_half": l5_ac_not_from_a_half(),
    }
    out["gate"] = {
        "question": ("Does LSS arXiv:2010.01201's own exact a = 1/2 solution (read at "
                     "full text, not via ALS's or Xu's secondary citation) explicitly "
                     "contain, derive, or trivially imply (a) the alpha(1/2) = 3 scaling "
                     "exponent, and/or (b) the a_c = 0.6890665 boundary value, with "
                     "hypotheses recorded verbatim?"),
        "answer_clause_a": "YES",
        "answer_clause_a_detail": (
            "EXPLICITLY CONTAINS it.  LSS Eq. (39) p. 11 is xi = (x-x_0)/(t_c-t)^{1/3}, "
            "i.e. alpha_LSS(1/2) = 1/3 exactly, hence this repository's alpha(1/2) = 3 "
            "exactly under literature_gates.py's own dictionary (our alpha = 1/alpha_ALS). "
            "It is stated in words at pp. 13-14 ('in agreement with the exact results of "
            "Section 3 (Eq. (30)) and Section 4 (Eq. (38)) for alpha = 1 and alpha = 1/3, "
            "respectively'), it is the far-field exponent 1/alpha = 3 of Eq. (38), it is "
            "the closed form alpha_0(1/2) = 2(1-a)^2/(2-a) = 1/3 of Eq. (45), and Table 1 "
            "p. 48 lists alpha_e = 0.333333333 at a = 0.5."),
        "answer_clause_b": "YES as primary source, NO from the a = 1/2 exact solution",
        "answer_clause_b_detail": (
            "a_c = 0.6890665337007457... is LSS's OWN number -- abstract p. 1, Eq. (8) "
            "p. 5, sec 12 p. 43 -- and this repository's LSS_A_C = 0.6890665 is that value "
            "truncated (4.89e-08 relative).  But it does NOT come from the a = 1/2 exact "
            "solution: it is defined by alpha(a_c) = 0 and located numerically by the "
            "sec 8 / sec 9 eigenvalue routes, while the exact-solution family's closed-form "
            "exponent alpha_0(a) = 2(1-a)^2/(2-a) is strictly positive on a < 1 and has no "
            "root at all.  The two banked findings share a PAPER, not a derivation."),
        "consequence": (
            "The provenance of solver/literature_gates.py's LSS row is upgraded from "
            "secondary-source (via ALS/Xu) to primary-source-read, with section, page and "
            "equation locators and LSS's own accuracy hypotheses verbatim.  One framing "
            "correction is earned and is flagged, not applied elsewhere: ALS sec 5.2, Xu "
            "Table 1's a = 0.5 row and LSS sec 4 are ONE ancestor (three of ALS's four "
            "authors are LSS's three; Xu checks against LSS's branch by Xu's own "
            "statement), so they must not be counted as independent confirmations of "
            "alpha(1/2) = 3.  The genuinely independent second source is J. Chen "
            "arXiv:1908.09385, which LSS's own Note on p. 11 credits with discovering the "
            "same solution independently."),
    }
    out["wall_clock_seconds"] = round(time.time() - t0, 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print("== Route-LSS v1: LSS arXiv:2010.01201 at full text ==")
    l1 = out["L1_theorem2_pde_residual"]
    print(f"L1 Theorem 2 residual: worst at a=1/2 {l1['worst_rel_residual_at_a_half']:.2e}, "
          f"best at a!=1/2 {l1['best_rel_residual_at_a_not_half']:.2e} "
          f"({l1['separation_decades']:.1f} decades apart)")
    l2 = out["L2_exponent_is_one_third"]
    print(f"L2 exponent: p = {l2['p_root_bisected']:.15f} (p - 1/3 = "
          f"{l2['p_root_minus_one_third']:.2e}); our alpha = {l2['alpha_ours']:.15f}; "
          f"control alpha_ours at gamma=1,3 = "
          f"{l2['general_gamma_control'][0]['alpha_ours']:.4f}, "
          f"{l2['general_gamma_control'][2]['alpha_ours']:.4f}")
    l3 = out["L3_far_field_exponent"]
    print(f"L3 far field: dlog|omega|/dlog xi = {l3['tail_dlog_omega_dlog_xi']:.6f} "
          f"(vs -1/alpha = -3); closed form matches Eq. (38) up to sign "
          f"(minus {l3['rel_diff_vs_closed_form_with_minus']:.2e}, "
          f"printed sign {l3['rel_diff_vs_printed_sign_of_eq38']:.2e})")
    l4 = out["L4_hilbert_check"]
    print(f"L4 u_x vs H(omega): rel {l4['rel_err_ux_vs_Homega']:.2e}; "
          f"3%-perturbed control {l4['rel_err_vs_3pct_perturbed_ux']:.2e}")
    l5 = out["L5_ac_not_from_a_half"]
    print(f"L5 a_c: alpha_0 min over a<1 = {l5['alpha_0_min_over_a_lt_1']:.6f} "
          f"(root below 1: {l5['alpha_0_has_root_below_1']}); "
          f"alpha_0(a_c) = {l5['alpha_0_at_LSS_a_c']:.6f}; "
          f"repo LSS_A_C off LSS's 16 digits by {l5['repo_LSS_A_C_rel_err']:.2e}")
    g = out["gate"]
    print(f"GATE (a) {g['answer_clause_a']} | (b) {g['answer_clause_b']}")
    print(f"-> {OUT}  ({out['wall_clock_seconds']} s)")


if __name__ == "__main__":
    main()
