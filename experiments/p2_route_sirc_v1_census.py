"""Leg 237 -- Route-SIRC: census of the scale-invariant-residual defect CLASS in solver/.

THE DEFECT CLASS, as leg 202 (Route-PNA) mechanism M2 established it on
`solver/profile_newton.py`:

    A Newton/relaxation solver whose equation carries an exact SCALING degeneracy
    is pinned to one member of the family only by GAUGE rows.  If the module's
    `converged` (or `closes`) verdict is computed from a SCALE-INVARIANT quantity
    ALONE -- a relative residual, a normalised error, a ratio-based tolerance --
    and never consults the gauge rows or any absolute-scale companion, then the
    verdict takes exactly the same value on the physical branch member and on an
    escaped member whose reported output (the wave speed, the amplitude) is wrong
    by orders of magnitude.  No returned field can distinguish them.  Leg 202
    measured `relres` spread 1.6e-11 across lambda = 1, 2, 10 while `c` ran
    0.5 -> 5.0, and reached `c = -306421` against a true 0.49797 at DEFAULT
    parameters.

THE GATE (pre-committed, verbatim, both branches):

    "Does any OTHER solver/ module (besides profile_newton.py, already confirmed
    affected) use a scale-invariant residual/ratio as its SOLE convergence or
    closure test, without an absolute-scale companion check?"

METHOD.  Every convergence/closure verdict site in solver/ is enumerated and
classified by READING the expression that produces the boolean, not by the
presence of a ratio anywhere in the file.  A site is a HIT only if all three
hold:

    (C1) the boolean verdict is a function of a scale-invariant quantity only;
    (C2) no absolute-scale companion (an absolute residual/sup test, a gauge-row
         test, a range check on the output) enters the SAME boolean;
    (C3) the module's equation actually ADMITS a scaling degeneracy, so an
         escaped member exists to be confused with the physical one -- verified
         by construction, not by inspection.

Probe groups, frozen before the numerics were run:

    G1  the algebraic scale-invariance of the candidate's verdict quantity,
        measured across lambda (the leg-202 M2 measurement, re-run here).
    G2  the escaped-member construction: a start that lands off the physical
        branch and is still reported converged, with the magnitude of the error
        in the reported output.
    G3  the CONTROL: the sibling verdict in the same module that DOES carry an
        absolute companion, run on the same input, to show the companion is what
        does the work.
    G4  the full census table: every solver/ module, its verdict sites, and the
        C1/C2/C3 classification with the reason.

Run: .venv/bin/python experiments/p2_route_sirc_v1_census.py
"""

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from solver.collocation_newton import ACollocation, continuation   # noqa: E402
from solver import profile_newton                                  # noqa: E402

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_sirc_v1_census.json")


# ---------------------------------------------------------------------------
# G1 -- is the candidate's verdict quantity exactly scale-invariant?
# ---------------------------------------------------------------------------

def _rel_of(col, om, c):
    """ACollocation.newton's verdict quantity, recomputed from outside the module.

    This is the module's own line, transcribed:
        R   = residual_a(om, c)
        src = om * (H @ om)
        rel = rms(R) / rms(src)
    `converged` is `bool(rel < 1e-9)` and NOTHING else.
    """
    R = col.residual_a(om, c)
    src = om * (col.H @ om)
    rms = float(np.sqrt(np.mean(R ** 2)))
    den = float(np.sqrt(np.mean(src ** 2)))
    return rms / den if den > 0 else float("inf"), rms, den


def g1_scale_invariance(J=200, a=0.0, lambdas=(1.0, 2.0, 10.0, 1e3, 1e-3)):
    """R -> lam^2 R and src -> lam^2 src under (Omega, c) -> (lam Omega, lam c),
    so rel is invariant EXACTLY, not approximately.  Measured, not argued."""
    col = ACollocation(J, a=a)
    r = col.newton(max_iter=60)
    om, c = r["Omega"], r["c"]
    rows = []
    for lam in lambdas:
        rel, rms, den = _rel_of(col, lam * om, lam * c)
        rows.append({"lambda": float(lam), "rel": rel,
                     "residual_rms": rms, "source_rms": den,
                     "c": float(lam * c),
                     "Omega_at_theta0": float(col.to_coef.sum(axis=0) @ (lam * om))})
    base = rows[0]["rel"]
    spread = max(abs(x["rel"] - base) for x in rows)
    c_span = max(abs(x["c"]) for x in rows) / max(min(abs(x["c"]) for x in rows), 1e-300)
    return {"J": J, "a": a, "rows": rows,
            "rel_spread_absolute": float(spread),
            "rel_spread_relative": float(spread / base) if base else float("inf"),
            "c_dynamic_range": float(c_span),
            "residual_rms_dynamic_range": float(
                max(x["residual_rms"] for x in rows)
                / max(min(x["residual_rms"] for x in rows), 1e-300)),
            "reading": ("rel is constant to the quoted spread while c and the "
                        "absolute residual both move over the quoted range: the "
                        "verdict quantity cannot see the scaling direction.")}


# ---------------------------------------------------------------------------
# G2 -- the escaped member, reported converged
# ---------------------------------------------------------------------------

def g2_escaped_member(J=200, a=0.0, epsilons=(1e-6, 1e-8, 1e-10)):
    """THE BLINDNESS, EXHIBITED WITHOUT ITERATING.

    (Omega*, c*) is the module's own converged solution.  (lam Omega*, lam c*)
    is an EXACT zero of the J residual rows for every lam, because R is
    homogeneous of degree 2.  It violates both gauges by O(lam) and its reported
    wave speed is lam times the true one.  Feed each to the module's OWN verdict
    expression and record what it says.

    ACollocation.newton's gauges are Omega(theta=0) = -1 and Omega(node nearest
    X=1) = -1/2.  Both are rows of F; NEITHER is consulted by `converged`.
    """
    col = ACollocation(J, a=a)
    g0 = col.to_coef.sum(axis=0)
    i1 = int(np.argmin(np.abs(col.X - 1.0)))
    ref = col.newton(max_iter=60)
    rows = []
    for lam in (1.0, 2.0, 10.0, 1e3):
        om, c = lam * ref["Omega"], lam * ref["c"]
        rel, rms, den = _rel_of(col, om, c)
        gauge0 = float(g0 @ om + 1.0)
        gauge1 = float(om[i1] + 0.5)
        rows.append({
            "lambda": float(lam),
            "verdict_converged": bool(rel < 1e-9),
            "rel": rel,
            "residual_rms": rms,
            "c": float(c),
            "c_reference": float(ref["c"]),
            "c_relative_error": float(abs(c - ref["c"])
                                      / max(abs(ref["c"]), 1e-300)),
            "gauge0_defect": gauge0,
            "gauge1_defect": gauge1,
            "gauge_defect_sup": float(max(abs(gauge0), abs(gauge1))),
        })
    bad = [x for x in rows if x["verdict_converged"] and x["gauge_defect_sup"] > 1e-8]
    return {"J": J, "a": a,
            "reference": {"c": float(ref["c"]), "relres": float(ref["relres"]),
                          "converged": bool(ref["converged"])},
            "rows": rows,
            "n_verdict_true_with_broken_gauge": len(bad),
            "worst_c_relative_error": float(max(x["c_relative_error"] for x in rows)),
            "worst_gauge_defect": float(max(x["gauge_defect_sup"] for x in rows)),
            "reading": ("the verdict expression returns True on every member, "
                        "including one whose gauges are off by the quoted defect "
                        "and whose reported c is wrong by the quoted factor. This "
                        "establishes C1 and C2. Whether the ITERATION can LAND "
                        "there is a separate question -- see G5.")}


# ---------------------------------------------------------------------------
# G5 -- REACHABILITY: can the module's own iteration actually land off-branch?
# ---------------------------------------------------------------------------

def g5_reachability(J=200, seeds=20, seed=0):
    """The question leg 202 got wrong once and corrected in its own artifact.

    Leg 202's journal records an intermediate reading that gauge blindness was
    "structural but UNREACHABLE at the default budget", and says plainly that
    the reading was wrong because the small-amplitude route reached it.  This
    leg asks the same question of ACollocation.newton and must report the answer
    it gets, not the answer the analogy predicts.

    Trial space, named in full per lesson 91 -- the negative below holds in
    EXACTLY this set and is claimed nowhere wider:
        A  lambda-scaled starts, om0 = lam * anchor, c0 = lam * 0.5,
           lam in {0.01, 0.1, 1.5, 2, 5, 10, 100, 1000}
        B  small-amplitude starts, om0 = eps * anchor, c0 = 0.5,
           eps in {1e-6, 1e-8, 1e-10}          (leg 202's M2 route)
        C  dilated starts, om0 = Omega*(X/mu), c0 = mu c*, mu in {1.2, 2, 5}
        D  random starts, om0 ~ N(0,1) * s, s in {0.1, 1, 10},
           c0 ~ N(0,1) * {1,10,100}, `seeds` draws from numpy default_rng(seed)
        E  iteration-budget truncation, max_iter in {1, 2, 3, 5, 10, 20, 60}
        F  the a-ladder through `continuation`, a = 0 .. 1.5 step 0.3, J = 60
           (leg 202's M1 rescue-clause route)
    all at a = 0 unless stated, on the module's default grid.
    """
    col = ACollocation(J, a=0.0)
    g0 = col.to_coef.sum(axis=0)
    i1 = int(np.argmin(np.abs(col.X - 1.0)))
    ref = col.newton(max_iter=60)
    cref = float(ref["c"])

    def record(route, label, r):
        om = r["Omega"]
        gd = float(max(abs(g0 @ om + 1.0), abs(om[i1] + 0.5)))
        coff = float(abs(r["c"] - cref) / max(abs(cref), 1e-300))
        return {"route": route, "case": label,
                "converged": bool(r["converged"]),
                "relres": float(r["relres"]), "c": float(r["c"]),
                "c_relative_error": coff, "gauge_defect_sup": gd,
                # an ESCAPE is a converged=True that is off the gauged member
                "escaped": bool(r["converged"] and (gd > 1e-8 or coff > 1e-6))}

    rows = []
    for lam in (0.01, 0.1, 1.5, 2.0, 5.0, 10.0, 100.0, 1000.0):
        rows.append(record("A_lambda_start", f"lam={lam:g}",
                           col.newton(om0=lam * col.anchor(), c0=lam * 0.5,
                                      max_iter=60)))
    for eps in (1e-6, 1e-8, 1e-10):
        rows.append(record("B_small_amplitude", f"eps={eps:g}",
                           col.newton(om0=eps * col.anchor(), c0=0.5, max_iter=60)))
    for mu in (1.2, 2.0, 5.0):
        om0 = np.interp(col.X / mu, col.X, ref["Omega"])
        rows.append(record("C_dilation", f"mu={mu:g}",
                           col.newton(om0=om0, c0=mu * cref, max_iter=60)))
    rng = np.random.default_rng(seed)
    for s in range(int(seeds)):
        om0 = rng.normal(size=col.J) * float(rng.choice([0.1, 1.0, 10.0]))
        c0 = float(rng.normal() * rng.choice([1.0, 10.0, 100.0]))
        rows.append(record("D_random", f"seed={s}",
                           col.newton(om0=om0, c0=c0, max_iter=60)))
    for mi in (1, 2, 3, 5, 10, 20, 60):
        rows.append(record("E_budget", f"max_iter={mi}",
                           col.newton(om0=10.0 * col.anchor(), c0=5.0, max_iter=mi)))

    ladder = []
    for o in continuation(np.arange(0.0, 1.51, 0.3), J=60, max_iter=60):
        om = o["Omega"]
        h = len(om) // 2
        ladder.append({"a": float(o["a"]), "converged": bool(o["converged"]),
                       "relres": float(o["relres"]), "c": float(o["c"]),
                       "far_field_fraction": float(
                           np.max(np.abs(om[h:])) / max(np.max(np.abs(om)), 1e-300))})

    n_conv = sum(1 for x in rows if x["converged"])
    n_esc = sum(1 for x in rows if x["escaped"])
    return {"J": J, "reference_c": cref, "rows": rows,
            "continuation_ladder_J60": ladder,
            "n_cases": len(rows), "n_converged": n_conv, "n_escaped": n_esc,
            "n_ladder_converged_off_anchor": int(sum(
                1 for x in ladder if x["converged"] and x["a"] > 0.0)),
            "worst_gauge_defect_among_converged": float(max(
                [x["gauge_defect_sup"] for x in rows if x["converged"]] or [0.0])),
            "worst_c_relative_error_among_converged": float(max(
                [x["c_relative_error"] for x in rows if x["converged"]] or [0.0])),
            "reading": ("if n_escaped is 0 the defect is LATENT in this module: "
                        "the verdict cannot see the scaling direction, but the "
                        "two gauge rows in the overdetermined Gauss-Newton pull "
                        "every start in this trial space back to the gauged "
                        "member, so no caller is currently handed a wrong number. "
                        "Latent is not absent -- the guard is the ITERATION's "
                        "behaviour, not the TEST, and nothing in the module "
                        "enforces it.")}


# ---------------------------------------------------------------------------
# G3 -- the control: the sibling verdict that HAS an absolute companion
# ---------------------------------------------------------------------------

def g3_control_gauged(J=200, a=0.0, epsilons=(1e-6, 1e-8, 1e-10)):
    """`newton_gauged` in the SAME module answers
        converged = converged_kept AND full_ok
    with converged_kept = (kept_sup < 1e-11), an ABSOLUTE sup test on the gauged
    system's own residual rows (leg 150's repair).  Same class of input; if the
    companion is what does the work, this one must not report converged."""
    col = ACollocation(J, a=a)
    rows = []
    for eps in epsilons:
        r = col.newton_gauged(c=0.5, om0=eps * col.anchor(), max_iter=60)
        rows.append({"eps": float(eps),
                     "converged": bool(r["converged"]),
                     "converged_kept_rows": bool(r["converged_kept_rows"]),
                     "kept_sup": float(r["kept_sup"]),
                     "relres": float(r["relres"]),
                     "relres_has_referent": bool(r["relres_has_referent"]),
                     "reason": r["reason"]})
    return {"J": J, "a": a, "rows": rows,
            "n_converged": int(sum(1 for x in rows if x["converged"])),
            "reading": ("the absolute companion (kept_sup < 1e-11) is the field "
                        "that separates the cases; the relative one does not.")}


# ---------------------------------------------------------------------------
# G3b -- the same probe against the KNOWN affected module, as calibration
# ---------------------------------------------------------------------------

def g3b_profile_newton_calibration(n=201, epsilons=(1e-8, 1e-10)):
    """Re-run leg 202's M2 on profile_newton so the census carries the known
    positive alongside the new one, at this leg's own resolution."""
    try:
        pr = profile_newton.TwoScaleNewton(a=0.0, n=n)
        ref = pr.solve()
        rows = []
        for eps in epsilons:
            r = pr.solve(om0=eps * pr.anchor())
            om = r["Omega"]
            rows.append({
                "eps": float(eps), "converged": bool(r["converged"]),
                "relres": float(r["relres"]), "c": float(r["c"]),
                "c_reference": float(ref["c"]),
                "c_relative_error": float(abs(r["c"] - ref["c"])
                                          / max(abs(ref["c"]), 1e-300)),
                "gauge_defect_sup": float(max(abs(om[pr.i0] + 1.0),
                                              abs(om[pr.i1] + 0.5))),
                "escaped": bool(r["converged"]
                                and abs(om[pr.i0] + 1.0) > 1e-8)})
        return {"available": True, "n": n, "rows": rows,
                "reference_c": float(ref["c"]),
                "n_escaped": int(sum(1 for x in rows if x["escaped"])),
                "reading": ("the KNOWN positive, re-run here at this leg's own "
                            "resolution: on profile_newton the same class of "
                            "start DOES reach an escaped member reported "
                            "converged. That is the contrast that makes "
                            "collocation_newton's grade LATENT rather than "
                            "materially exposed.")}
    except Exception as exc:
        return {"available": False, "reason": repr(exc)}


# ---------------------------------------------------------------------------
# G4 -- the census table
# ---------------------------------------------------------------------------
#
# Every entry was produced by reading the expression that yields the boolean.
# `verdict_expression` is transcribed from the source at the cited line.

CENSUS = [
    # ---- THE HIT -----------------------------------------------------------
    {"module": "solver/collocation_newton.py",
     "function": "ACollocation.newton",
     "line": 359,
     "verdict_expression": 'converged = bool(rel < 1e-9), '
                           'rel = rms(residual_a(om, c)) / rms(om * (H @ om))',
     "scale_invariant": True,
     "absolute_companion": False,
     "scaling_degeneracy": True,
     "hit": True,
     "reason": ("R = Omega H(Omega) - c Omega_X - a U Omega_X scales as lam^2 and "
                "the denominator Omega H(Omega) scales as lam^2, so rel is EXACTLY "
                "invariant under the module's own documented degeneracy "
                "(Omega, c) -> (lam Omega, lam c). The two gauge rows that pin the "
                "member are rows J and J+1 of F; `converged` is computed from R "
                "alone and never consults them. Same shape as leg 202 M2.")},
    {"module": "solver/collocation_newton.py",
     "function": "continuation",
     "line": 366,
     "verdict_expression": 'r["relres"] > 1e-10 -> retry; '
                           'accept alt if alt["relres"] < r["relres"]; '
                           'reseed if r["relres"] < 1e-10',
     "scale_invariant": True,
     "absolute_companion": False,
     "scaling_degeneracy": True,
     "hit": True,
     "reason": ("transitive: every branch decision -- retry, accept-the-retry, and "
                "RESEED THE REMAINDER OF THE LADDER -- is a comparison of the same "
                "scale-invariant relres, and the escaped member scores at machine "
                "zero on it. This is leg 202 M1's rescue-clause shape driven by "
                "leg 202 M2's blind quantity.")},

    # ---- the near misses, and why they are not hits -------------------------
    {"module": "solver/collocation_newton.py",
     "function": "ACollocation.newton_gauged",
     "line": 285,
     "verdict_expression": "converged = bool(converged_kept and full_ok); "
                           "converged_kept = kept_last < 1e-11 (ABSOLUTE sup); "
                           "full_ok = has_referent and relres < relres_tol",
     "scale_invariant": False,
     "absolute_companion": True,
     "scaling_degeneracy": True,
     "hit": False,
     "reason": ("the relative half is ANDed with an absolute sup test on the "
                "gauged rows, and has_referent refuses to fabricate a denominator "
                "from an identically-zero source scale (leg 150's repair). The "
                "absolute companion is present and load-bearing -- G3 measures it.")},
    {"module": "solver/gclm_rescaled.py",
     "function": "run",
     "line": 191,
     "verdict_expression": "converged = res < tol_eff, "
                           "tol_eff = tol * max(|f(0)|/4, GAUGE_TOL_FLOOR)",
     "scale_invariant": True,
     "absolute_companion": True,
     "scaling_degeneracy": True,
     "hit": False,
     "reason": ("scale-invariant BY DESIGN (leg 85's Route-GRA repair) and the "
                "absolute scale is carried explicitly: the gauge is READ FROM THE "
                "DATA at f(0), returned as `gauge` and `tol_effective`, and floored "
                "so poisoned data cannot pass. Decisive difference from the defect "
                "class: the module's CLAIM quantity is the rate c_omega, which is "
                "itself invariant under the same lambda family, so an escaped "
                "member does not carry a wrong reported number -- there is nothing "
                "for the blindness to hide.")},
    {"module": "solver/marginal_flow.py",
     "function": "run (record verdict)",
     "line": 355,
     "verdict_expression": "converged = finite and no diverged_at_tau and "
                           "worst_res < NEWTON_STAGNATION and "
                           "state_growth < STATE_GROWTH (1e5)",
     "scale_invariant": False,
     "absolute_companion": True,
     "scaling_degeneracy": False,
     "hit": False,
     "reason": ("worst_res is a residual-over-floor RATIO, but it is ANDed with an "
                "absolute finiteness test and an absolute state-growth cap whose "
                "calibration is written out at the site (246x headroom above the "
                "largest legitimate trajectory, 141x below the nearest true "
                "positive).")},
    {"module": "solver/nk_seminorm.py",
     "function": "operator_norm_fixed_point",
     "line": 242,
     "verdict_expression": "closes = False if nxt > T_cap (ABSOLUTE cap); "
                           "loop stop |nxt - T| <= tol * max(1.0, T)",
     "scale_invariant": False,
     "absolute_companion": True,
     "scaling_degeneracy": False,
     "hit": False,
     "reason": ("the relative-with-floor expression is the loop's STOP, not the "
                "verdict; `closes` is decided by the absolute cap T_cap. The "
                "max(1.0, T) floor also makes the stop absolute for T < 1.")},
    {"module": "solver/interval_certificate.py",
     "function": "KawaharaProblem.newton",
     "line": 1034,
     "verdict_expression": "loop stop max|step| < tol * max(1.0, max|a|); "
                           "returns (a, hist) with NO boolean",
     "scale_invariant": False,
     "absolute_companion": True,
     "scaling_degeneracy": False,
     "hit": False,
     "reason": ("no convergence boolean is returned at all -- the caller gets the "
                "residual ladder as a magnitude. The closure verdict is `closes` "
                "from the radii polynomial, whose Y_0 is a NORM (dimensional), so "
                "that test is not scale-invariant.")},
    {"module": "solver/port_certification.py",
     "function": "gmres",
     "line": 148,
     "verdict_expression": "loop stop `rel < tol`; returns "
                           "(x, relative_residual, krylov_dim) with NO boolean",
     "scale_invariant": True,
     "absolute_companion": True,
     "scaling_degeneracy": False,
     "hit": False,
     "reason": ("the module's own docstring at line 121 pre-empts this exact "
                "defect: 'Reported as a MAGNITUDE (the relative residual), never "
                "as converged/not (lesson 58)'. A scale-invariant quantity that is "
                "never turned into a boolean cannot be a sole convergence TEST. "
                "Banked as the explicit anti-instance.")},
    {"module": "solver/spectral_certificate.py",
     "function": "tail_norm_ladder",
     "line": 611,
     "verdict_expression": 'verdict from r = last increment ratio: '
                           '"converges" if r < 0.95, "log_divergent" if r < 1.05, '
                           'else "power_divergent"',
     "scale_invariant": True,
     "absolute_companion": False,
     "scaling_degeneracy": False,
     "hit": False,
     "reason": ("scale-invariant and sole, but C3 FAILS: the property under test "
                "is membership of h in l^1_w, which is itself exactly invariant "
                "under h -> lam h. Every member of the family has the same true "
                "answer, so there is no escaped member whose reported number is "
                "wrong. This is the one site that satisfies C1 and C2 and is still "
                "not the defect -- which is why C3 is in the classification.")},
    {"module": "solver/dissipative_profile.py",
     "function": "newton / solve_for_a",
     "line": 333,
     "verdict_expression": "loop stop nrm < tol (ABSOLUTE rms); returns "
                           "residual_rms as a magnitude, NO boolean",
     "scale_invariant": False,
     "absolute_companion": True,
     "scaling_degeneracy": True,
     "hit": False,
     "reason": ("the module has BOTH degeneracies (amplitude and dilation) and "
                "pins them with c_omega and an explicit `scale_gauge`, which is "
                "returned. The stop is an absolute rms and no boolean is "
                "manufactured from it.")},

    # ---- absolute-test verdicts: swept, classified, no ratio anywhere -------
    {"module": "solver/hl_rescaled.py", "function": "RescaledHL.run / "
     "RescaledHLDynamic.run", "line": "545, 700",
     "verdict_expression": "converged = bool(res < tol), res = sup|L0| (ABSOLUTE)",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": True, "hit": False,
     "reason": ("absolute sup of the steady operator, plus an amplitude "
                "renormalisation gauge applied every step (normalize_amp) and an "
                "absolute divergence cut res > 1e8.")},
    {"module": "solver/boussinesq_rescaled.py", "function": "run", "line": 278,
     "verdict_expression": "converged = res < tol (ABSOLUTE) with an explicit "
                           "renorm to a fixed odd-slope target",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": True, "hit": False,
     "reason": ("the renorm block rescales to wx0_target/ex0_target every step, "
                "which is the absolute-scale companion made structural.")},
    {"module": "solver/bordered_hl.py", "function": "BorderedHL.newton", "line": 253,
     "verdict_expression": "converged = bool(res[-1] < tol and isfinite(res[-1])), "
                           "res = |F(z)|_inf over ALL rows INCLUDING the border",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": False, "hit": False,
     "reason": "absolute sup over the full bordered system, gauge rows included."},
    {"module": "solver/weight_search.py", "function": "WeightedProblem.newton",
     "line": 372,
     "verdict_expression": "converged = bool(ladder[-1] < tol), ladder = |F|_inf; "
                           "tol raised to residual_floor(z) when auto",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": False, "hit": False,
     "reason": ("absolute sup, and the auto floor is an absolute arithmetic-floor "
                "estimate; stalled_at_floor is reported separately.")},
    {"module": "solver/first_integral.py", "function": "newton", "line": 613,
     "verdict_expression": "converged = bool(res < 1e-10), res = sup|residual| "
                           "(ABSOLUTE)",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": False, "hit": False,
     "reason": "absolute sup; the amplitude gauge Omega(0) = -1 is imposed exactly."},
    {"module": "solver/finite_support.py", "function": "solve", "line": 324,
     "verdict_expression": "converged = bool(hist[-1] < 1e-8), hist = sup|F| "
                           "(ABSOLUTE)",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": False, "hit": False,
     "reason": "absolute sup over the system including the free-boundary row."},
    {"module": "solver/rescaled_spectrum.py", "function": "newton", "line": 284,
     "verdict_expression": "converged = bool(res < 1e-8), res = sup|R| (ABSOLUTE); "
                           "gauge returned as its own field",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": True, "hit": False,
     "reason": ("absolute sup, and the normalisation gauge k.b + 1 is returned as "
                "`gauge` so the caller can see the member.")},
    {"module": "solver/viscous_novelty.py", "function": "branch sweep", "line": 607,
     "verdict_expression": "ok = hist[-1] < tol AND -1e-6 <= eps_n < 1.0 AND "
                           "|eps_n - eps| < 0.05 AND |mu_n - mu| < 0.5",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": False, "hit": False,
     "reason": "absolute defect plus three absolute range/continuity checks."},
    {"module": "solver/reduced_certificate.py", "function": "build", "line": 229,
     "verdict_expression": "delegates: `if not r['converged']` from the profile "
                           "solver it is handed",
     "scale_invariant": False, "absolute_companion": None,
     "scaling_degeneracy": False, "hit": False,
     "reason": ("no verdict of its own; inherits whatever its input solver "
                "reports. Recorded so the census has no silent gap.")},
    {"module": "solver/nk_bounds.py, solver/nk_fourier.py, "
               "solver/interval_certificate.py",
     "function": "radii-polynomial `closes`", "line": "538, 315, 501",
     "verdict_expression": "closes = (1 - Z1 > 0) and (Z2 > 0) and (disc >= 0) "
                           "and r_min < r_max",
     "scale_invariant": False, "absolute_companion": True,
     "scaling_degeneracy": False, "hit": False,
     "reason": ("Z1 is dimensionless but Y_0 is a NORM of the defect and carries "
                "the absolute scale into the discriminant, so the test is not "
                "scale-invariant. certificate_guards.py additionally refuses "
                "hypothesis-violating inputs rather than laundering them.")},
]

MODULES_WITH_NO_VERDICT = [
    "advection_scope", "boussinesq", "boussinesq_velocity", "certificate_guards",
    "certificate_shapes", "chen_inviscid_certificate", "critical_dissipation",
    "decay_collocation", "decay_grading", "energy_coercivity", "fractional_boussinesq",
    "fractional_gclm", "ga_search", "gclm", "gclm_family", "hilbert_holder",
    "hilbert_pointwise", "holder_norms", "interval", "line_hilbert",
    "literature_gates", "op_lower", "origin_h2_certificate", "spectral_utils",
    "target_norm", "target_selection", "turning_point",
]


# ---------------------------------------------------------------------------
# G6 -- claim adjacency: does a BANKED number depend on the hit?
# ---------------------------------------------------------------------------

def g6_claim_adjacency():
    """Enumerate every call site of the two hit functions outside solver/.

    The escalation rule turns on this: a claim-adjacent hit is parked and
    escalated, a non-claim-adjacent one lands as a characterized finding.  So
    the answer is measured from the tree, not asserted.

    `.newton(` is ambiguous across modules (several classes define one), so a
    site counts only if the receiver is an ACollocation, which is established by
    the file also importing ACollocation from this module.
    """
    import re
    import subprocess

    def grep(pat):
        try:
            out = subprocess.run(["git", "grep", "-n", pat], cwd=ROOT,
                                 capture_output=True, text=True).stdout
        except Exception:
            return []
        return [l for l in out.splitlines() if l.strip()]

    importers = sorted({l.split(":")[0] for l in grep("ACollocation")
                        if not l.split(":")[0].startswith("solver/")})
    newton_sites, cont_sites = [], []
    for line in grep(r"\.newton("):
        path = line.split(":")[0]
        if path.startswith("solver/") or path not in importers:
            continue
        newton_sites.append(line.strip())
    for line in grep(r"continuation("):
        path = line.split(":")[0]
        if path.startswith("solver/") or path not in importers:
            continue
        if re.search(r"\bcontinuation\s*\(", line):
            cont_sites.append(line.strip())

    def kind(path):
        if path.startswith("test_"):
            return "test"
        if "adversarial" in path or "postrepair" in path or "_repair" in path:
            return "audit/repair runner"
        if path.startswith("experiments/"):
            return "experiment runner"
        return "other"

    sites = [{"site": s, "file": s.split(":")[0],
              "kind": kind(s.split(":")[0])}
             for s in newton_sites + cont_sites]
    banked = [s for s in sites
              if s["kind"] in ("experiment runner",)]
    return {
        "question": "does a banked number depend on the hit function?",
        "method": ("git grep every call site of ACollocation.newton and of "
                   "collocation_newton.continuation outside solver/, keeping "
                   "only files that import ACollocation from this module"),
        "files_importing_ACollocation_outside_solver": importers,
        "call_sites": sites,
        "n_call_sites": len(sites),
        "n_in_audit_or_test_files": int(sum(
            1 for s in sites if s["kind"] in ("test", "audit/repair runner"))),
        "n_in_claim_bearing_experiment_runners": len(banked),
        "claim_bearing_sites": banked,
        "verdict": ("NOT_CLAIM_ADJACENT" if not banked else "CLAIM_ADJACENT"),
        "note": ("Route-D's real consumers -- test_collocation_newton.py, "
                 "experiments/p2_route_d_v12_defect.py, p2_route_d_v13_turning.py "
                 "-- call `newton_gauged`, the sibling that carries leg 150's "
                 "absolute companion, NOT the hit. That is why the grade is what "
                 "it is, and it is the single most load-bearing fact in this leg."),
    }


def main():
    g1 = g1_scale_invariance()
    g2 = g2_escaped_member()
    g3 = g3_control_gauged()
    g3b = g3b_profile_newton_calibration()
    g5 = g5_reachability()

    hits = [c for c in CENSUS if c["hit"]]
    gate = "YES" if hits else "NO"
    exposure = ("MATERIALLY_EXPOSED" if g5["n_escaped"] > 0 else "LATENT")

    n_solver_files = len([f for f in os.listdir(os.path.join(ROOT, "solver"))
                          if f.endswith(".py") and f != "__init__.py"])

    out = {
        "leg": 237,
        "route": "SIRC",
        "gate": ("Does any OTHER solver/ module (besides profile_newton.py, "
                 "already confirmed affected) use a scale-invariant "
                 "residual/ratio as its SOLE convergence or closure test, "
                 "without an absolute-scale companion check?"),
        "answer": gate,
        "exposure_grade": exposure,
        "answer_long": (
            f"{gate} -- solver/collocation_newton.py::ACollocation.newton (and "
            "`continuation`, transitively) computes `converged` from "
            "rel = rms(R)/rms(Omega H(Omega)) ALONE, which is exactly invariant "
            "under the module's own documented degeneracy (Omega, c) -> "
            "(lam Omega, lam c), and never consults either gauge row. "
            f"Graded {exposure}: across the six-route trial space named in G5 "
            "(lambda-scaled, small-amplitude, dilated, random, budget-truncated "
            "starts, and the a-ladder through `continuation`) the iteration "
            "returns to the gauged member in every case, so no caller is "
            "currently handed a wrong number. The negative is claimed in THAT "
            "trial space and nowhere wider (lesson 91)."),
        "criteria": {
            "C1": "the boolean verdict is a function of a scale-invariant quantity only",
            "C2": "no absolute-scale companion enters the SAME boolean",
            "C3": "the equation admits a scaling degeneracy, so an escaped member exists",
        },
        "coverage": {
            "solver_py_files": n_solver_files,
            "modules_with_a_convergence_or_closure_verdict":
                len({c["module"] for c in CENSUS}),
            "verdict_sites_classified": len(CENSUS),
            "modules_with_no_verdict_site": len(MODULES_WITH_NO_VERDICT),
            "modules_with_no_verdict_site_list": MODULES_WITH_NO_VERDICT,
        },
        "hits": [{"module": h["module"], "function": h["function"],
                  "line": h["line"], "reason": h["reason"]} for h in hits],
        "census": CENSUS,
        "G1_scale_invariance": g1,
        "G2_escaped_member": g2,
        "G3_control_absolute_companion": g3,
        "G3b_profile_newton_calibration": g3b,
        "G5_reachability": g5,
        "claim_adjacency": g6_claim_adjacency(),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=False)

    print(f"GATE: {gate}   hits: {len(hits)}")
    for h in hits:
        print(f"  HIT  {h['module']}::{h['function']}  line {h['line']}")
    print(f"G1  rel spread across lambda in "
          f"{[r['lambda'] for r in g1['rows']]}: {g1['rel_spread_absolute']:.3e} "
          f"absolute, while c spans {g1['c_dynamic_range']:.3e}x and the absolute "
          f"residual spans {g1['residual_rms_dynamic_range']:.3e}x")
    print(f"G2  verdict=True on a broken-gauge member: "
          f"{g2['n_verdict_true_with_broken_gauge']}/{len(g2['rows'])}; "
          f"worst c relative error {g2['worst_c_relative_error']:.3e}, "
          f"worst gauge defect {g2['worst_gauge_defect']:.3e}")
    for r in g2["rows"]:
        print(f"    lam={r['lambda']:.0e}  verdict={r['verdict_converged']}  "
              f"rel={r['rel']:.3e}  c={r['c']:+.6e}  "
              f"(ref {r['c_reference']:+.6e})  gauge defect {r['gauge_defect_sup']:.3e}")
    print(f"G3  control newton_gauged converged on "
          f"{g3['n_converged']}/{len(g3['rows'])} of the same inputs")
    for r in g3["rows"]:
        print(f"    eps={r['eps']:.0e}  converged={r['converged']}  "
              f"kept_sup={r['kept_sup']:.3e}  reason={r['reason']}")
    print(f"G5  reachability: {g5['n_escaped']} escapes in {g5['n_cases']} cases "
          f"({g5['n_converged']} converged); worst gauge defect among converged "
          f"{g5['worst_gauge_defect_among_converged']:.3e}, worst c rel error "
          f"{g5['worst_c_relative_error_among_converged']:.3e}")
    print(f"    a-ladder (J=60): "
          f"{g5['n_ladder_converged_off_anchor']} converged at a > 0 of "
          f"{len(g5['continuation_ladder_J60']) - 1}")
    print(f"EXPOSURE: {exposure}")
    print(f"wrote {OUT}")
    return out


if __name__ == "__main__":
    main()
