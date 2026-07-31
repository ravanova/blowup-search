"""P2 Route-D v12 -- Y_0 in the basis the bounds live in, and what it found there.

v11 killed the ~1e-2 residual floor with a Newton solve on the sinh-rho grid and
handed over one instruction: carry the profile into the theta-collocation basis
where every Route-D bound lives, and measure Y_0 THERE, because the two
discretizations are different objects.  This leg does that.  The carry-over is a
build (the a-transport term in the compactified basis, with the velocity's exact
integrals I_k) and the measurement is the point -- but the measurement turned up
a structural fact about the a > 0 profile that eleven legs of far-field analysis
had no way to see, so most of what is below is about that.

NOT a logged Tier-1/2 experiment: deterministic Newton + deterministic sweeps, no
GA, no seeds.  Run:

    .venv/bin/python -u experiments/p2_route_d_v12_defect.py
    -> writeup/data/p2_route_d_v12_defect.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v12_evidence.py   (fig30)

SIX measurements: T1 the carry-over and its control; T2 the defect the
certificate actually sees; T3 the critical radius (the mechanism); T4 the
convergence rate and the J it would take; T5 what the profile does to ||A||;
T6 the survival boundary re-read, with a control.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.collocation_newton import (ACollocation, critical_radius,       # noqa: E402
                                       effective_speed, refined_theta,
                                       zero_order)
from solver.decay_collocation import sup_op_norm                            # noqa: E402
from solver.holder_norms import HolderNorm                                  # noqa: E402
from solver.profile_newton import TwoScaleNewton                            # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v12_defect.json"

ALPHA, GAMMA = 1.4, 0.15         # the operating point, unchanged since v7 V4
Y0_MAX = 2.45e-4                 # v10's conditional budget at (1.4, 0.15)
A_NORM_UB = 20.94                # v10 W2: upper bound on ||A|| at the same point
C_FIXED = 0.5                    # the gauge that makes the certificate's system square


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def codomain_norm(theta, R, alpha=ALPHA, gamma=GAMMA):
    """||R||_Y = sup w^{alpha+1}|R| + [R]_{gamma, weight alpha+1-gamma}.

    The codomain of the Route-D pair (v5 U-series, weight fixed by v8 X0): one
    more power of decay than the domain, and a Holder seminorm whose weight is
    alpha+1-gamma.  HolderNorm's convention is (sup weight, seminorm weight)
    = (a, a-g), so passing a = alpha+1 gives exactly that.
    """
    X = np.tan(0.5 * np.asarray(theta, float))
    hn = HolderNorm(theta, X, alpha + 1.0, gamma)
    return hn.sup_part(R), hn.seminorm(R), hn(R)


def profile_and_defect(J, a, refine=4, c=C_FIXED):
    """Newton in the certificate's gauged system, then the defect of the interpolant."""
    col = ACollocation(J, a=a)
    r = col.newton_gauged(c=c)
    th = refined_theta(J, refine)
    R, _ = col.interpolant_residual(r["Omega"], c, th)
    sup, semi, tot = codomain_norm(th, R)
    X = np.tan(0.5 * th)
    i = int(np.argmax((1.0 + X ** 2) ** (0.5 * (ALPHA + 1.0)) * np.abs(R)))
    return col, r, {"sup_part": sup, "seminorm_part": semi, "norm": tot,
                    "argmax_X": float(X[i]),
                    "raw_sup": float(np.max(np.abs(R)))}


def structure(col, om, c, a):
    """(X_c, X_c/c, fitted zero order) from a profile on any grid."""
    E = effective_speed(col.X, col.V @ om, c, a)
    Xc = critical_radius(col.X, E)
    p, npts = zero_order(col.X, om, Xc)
    return {"Xc": Xc, "Xc_over_c": Xc / c, "zero_order": p, "fit_points": npts}


# ---------------------------------------------------------------------------
# T0 -- the profiles themselves (so the figure rebuilds without a re-run)
# ---------------------------------------------------------------------------


def t0_profiles(J=800, a_values=(0.0, 0.1, 0.2, 0.3, 0.5), keep=400):
    out = []
    for a in a_values:
        col = ACollocation(J, a=a)
        r = col.newton_gauged(c=C_FIXED)
        om = r["Omega"]
        E = effective_speed(col.X, col.V @ om, C_FIXED, a)
        Xc = critical_radius(col.X, E)
        m = col.X <= 3e3
        idx = np.unique(np.linspace(0, int(m.sum()) - 1, keep).astype(int))
        out.append({"a": a, "Xc": Xc,
                    "X": [float(x) for x in col.X[m][idx]],
                    "Omega": [float(x) for x in om[m][idx]],
                    "E": [float(x) for x in E[m][idx]]})
    return {"J": J, "c": C_FIXED, "profiles": out}


# ---------------------------------------------------------------------------
# T1 -- the carry-over, and the control that makes it readable
# ---------------------------------------------------------------------------


def t1_carry_over(J=400):
    col = ACollocation(J, a=0.0)
    ex = col.anchor()
    th = refined_theta(J, 4)
    R0, _ = col.interpolant_residual(ex, 0.5, th)
    sup0, semi0, tot0 = codomain_norm(th, R0)

    rows = []
    for a in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        _, r, d = profile_and_defect(J, a)
        rows.append({"a": a, "kept_sup": r["kept_sup"],
                     "dropped_defect": r["dropped_defect"],
                     "relres": r["relres"], "iterations": r["iterations"],
                     "raw_offnode_sup": d["raw_sup"]})
    return {"J": J,
            "control_exact_anchor": {"raw_sup": float(np.max(np.abs(R0))),
                                     "sup_part": sup0, "seminorm_part": semi0,
                                     "norm": tot0},
            "rows": rows}


# ---------------------------------------------------------------------------
# T2 -- the defect the certificate actually sees
# ---------------------------------------------------------------------------


def t2_defect(J=400):
    rows = []
    for a in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
        _, r, d = profile_and_defect(J, a)
        y0 = A_NORM_UB * d["norm"]
        rows.append({"a": a, "sup_part": d["sup_part"],
                     "seminorm_part": d["seminorm_part"], "F_norm": d["norm"],
                     "argmax_X": d["argmax_X"], "Y0_upper": y0,
                     "over_budget": y0 / Y0_MAX})
    return {"J": J, "alpha": ALPHA, "gamma": GAMMA, "Y0_max": Y0_MAX,
            "A_norm_upper": A_NORM_UB, "rows": rows}


# ---------------------------------------------------------------------------
# T3 -- the mechanism, in two independent discretizations
# ---------------------------------------------------------------------------


def t3_structure():
    theta_rows, rho_rows = [], []
    for a in (0.1, 0.2, 0.3, 0.4, 0.5):
        for J in (400, 800):
            col = ACollocation(J, a=a)
            r = col.newton_gauged(c=C_FIXED)
            s = structure(col, r["Omega"], C_FIXED, a)
            s.update({"a": a, "J": J, "predicted_zero_order": 1.0 / a})
            theta_rows.append(s)
        # n = 1601 costs an SVD per Newton step on a 1603 x 1602 system, so the
        # refinement check is run where the zero is hardest to resolve rather
        # than at every a; n = 801 covers the whole sweep.
        for n in ((801, 1601) if a in (0.3, 0.5) else (801,)):
            nw = TwoScaleNewton(a=a, n=n)
            sol = nw.solve()
            E = effective_speed(nw.fam.X, nw.VH @ sol["Omega"], sol["c"], a)
            Xc = critical_radius(nw.fam.X, E)
            p, npts = zero_order(nw.fam.X, sol["Omega"], Xc)
            rho_rows.append({"a": a, "n": n, "c": sol["c"], "Xc": Xc,
                             "Xc_over_c": Xc / sol["c"], "zero_order": p,
                             "fit_points": npts, "relres": sol["relres"],
                             "predicted_zero_order": 1.0 / a})
    # the cross-build agreement, at the finest grid of each
    cross = []
    for a in (0.1, 0.2, 0.3, 0.4, 0.5):
        t = [x for x in theta_rows if x["a"] == a and x["J"] == 800][0]
        rr = sorted([x for x in rho_rows if x["a"] == a],
                    key=lambda x: -x["n"])[0]
        cross.append({"a": a, "theta": t["Xc_over_c"], "rho": rr["Xc_over_c"],
                      "rel_gap": abs(t["Xc_over_c"] - rr["Xc_over_c"])
                                 / rr["Xc_over_c"]})
    return {"theta_collocation": theta_rows, "sinh_rho": rho_rows,
            "cross_build": cross}


# ---------------------------------------------------------------------------
# T4 -- the rate, and the grid it would take
# ---------------------------------------------------------------------------


def t4_rate(a_values=(0.2, 0.3, 0.4), Js=(100, 200, 400, 800, 1600)):
    out = []
    for a in a_values:
        rows = []
        for J in Js:
            col, r, d = profile_and_defect(J, a)
            Xc = critical_radius(col.X, effective_speed(col.X, col.V @ r["Omega"],
                                                        C_FIXED, a))
            near = int(np.sum((col.X > 0.5 * Xc) & (col.X < 1.5 * Xc)))
            rows.append({"J": J, "F_norm": d["norm"], "sup_part": d["sup_part"],
                         "dropped_defect": r["dropped_defect"],
                         "nodes_near_Xc": near, "Xc": Xc})
        lj = np.log([x["J"] for x in rows])
        ly = np.log([x["F_norm"] for x in rows])
        slope = float(np.polyfit(lj, ly, 1)[0])
        # J at which A_NORM_UB * ||F|| would drop under the budget
        y = [A_NORM_UB * x["F_norm"] for x in rows]
        need = float(np.exp((np.log(Y0_MAX) - np.log(y[-1])) / slope + lj[-1])) \
            if slope < 0 else float("inf")
        out.append({"a": a, "rows": rows, "log_slope": slope,
                    "predicted_rate": -(1.0 / a + 1.0),
                    "J_needed_for_budget": need})
    return out


# ---------------------------------------------------------------------------
# T5 -- what the real profile does to the operator the bounds are about
# ---------------------------------------------------------------------------


def t5_operator(J=400, alphas=(1.2, 1.4, 1.6, 1.8)):
    """Sup-to-sup graded inverse norm at the a>0 profile vs at the a=0 anchor.

    Exactly v4's W1/W2 measurement (an EXACT induced norm between discrete sup
    norms -- not a Holder ball, so v6's B1 trap does not apply), but linearized
    at the profile the certificate would actually use.
    """
    rows = []
    for a in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        col = ACollocation(J, a=a)
        r = col.newton_gauged(c=C_FIXED)
        om = r["Omega"]
        g0 = col.to_coef.sum(axis=0)
        keep = [j for j in range(J) if j != 0]
        M = np.empty((J, J))
        M[0, :] = g0
        M[1:, :] = col.jacobian_a(om, C_FIXED)[keep, :]
        A = np.linalg.inv(M)
        vals = {}
        for al in alphas:
            w_dom = (1.0 + col.X ** 2) ** (0.5 * al)
            w_cod = np.empty(J)
            w_cod[0] = 1.0
            w_cod[1:] = ((1.0 + col.X ** 2) ** (0.5 * (al + 1.0)))[keep]
            vals["%.1f" % al] = sup_op_norm(A, w_dom, w_cod)
        rows.append({"a": a, "cond": float(np.linalg.cond(M)), "norms": vals})

    # THE QUESTION THE SINGLE-J ROW CANNOT ANSWER.  A large ||A|| could be a
    # large operator or a grid artifact; only the J-ladder tells them apart, and
    # the linearization at a profile with a zero of order 1/a at X_c has a
    # homogeneous solution ~ (X_c - X)^{-1/a}, which is not in any sup norm.  If
    # that is what the number is seeing, it must GROW with J.
    ladder = []
    for a in (0.0, 0.2, 0.3):
        for Jl in (200, 400, 800):
            col = ACollocation(Jl, a=a)
            r = col.newton_gauged(c=C_FIXED)
            g0 = col.to_coef.sum(axis=0)
            keep = [j for j in range(Jl) if j != 0]
            M = np.empty((Jl, Jl))
            M[0, :] = g0
            M[1:, :] = col.jacobian_a(r["Omega"], C_FIXED)[keep, :]
            A = np.linalg.inv(M)
            w_dom = (1.0 + col.X ** 2) ** (0.5 * ALPHA)
            w_cod = np.empty(Jl)
            w_cod[0] = 1.0
            w_cod[1:] = ((1.0 + col.X ** 2) ** (0.5 * (ALPHA + 1.0)))[keep]
            ladder.append({"a": a, "J": Jl, "norm": sup_op_norm(A, w_dom, w_cod)})
    for a in (0.0, 0.2, 0.3):
        rows_a = [x for x in ladder if x["a"] == a]
        lj = np.log([x["J"] for x in rows_a])
        ln = np.log([x["norm"] for x in rows_a])
        for x in rows_a:
            x["log_slope"] = float(np.polyfit(lj, ln, 1)[0])
    return {"J": J, "alpha_ladder": ALPHA, "rows": rows, "ladder": ladder}


# ---------------------------------------------------------------------------
# T6 -- the survival boundary, re-read; and the control the hypothesis needs
# ---------------------------------------------------------------------------


def t6_boundary(n=801):
    """X_c(a) from the rho-grid (which resolves the zero), plus an integer-p control.

    Two readings of a* are on the table.  (i) GEOMETRIC: X_c(a) descends toward
    the core, and when the support radius reaches the anchor's own width there is
    no two-scale structure left.  (ii) ARITHMETIC: the zero order is 1/a, which
    passes through the integer 2 exactly at a = 1/2, and H of (X_c-X)^p_+ grows a
    log at integer p.  They predict different things at a = 1/3 (p = 3, also an
    integer, but X_c still far outside the core), so sweeping through 1/3 is the
    control that separates them.
    """
    rows = []
    for a in (0.25, 0.30, 1.0 / 3.0, 0.35, 0.40, 0.45, 0.48, 0.50, 0.52, 0.55,
              0.60, 0.70):
        nw = TwoScaleNewton(a=a, n=n)
        sol = nw.solve()
        E = effective_speed(nw.fam.X, nw.VH @ sol["Omega"], sol["c"], a)
        Xc = critical_radius(nw.fam.X, E)
        p, _ = zero_order(nw.fam.X, sol["Omega"], Xc)
        # half-width of the core: where |Omega| falls to half its value at X=0
        X, om = nw.fam.X, np.abs(sol["Omega"])
        m = X > 0
        half = float(np.interp(0.5 * om[nw.fam.i0], om[m][::-1], X[m][::-1]))
        rows.append({"a": a, "c": sol["c"], "relres": sol["relres"], "Xc": Xc,
                     "zero_order": p, "predicted_zero_order": 1.0 / a,
                     "half_width": half, "ratio_Xc_over_halfwidth": Xc / half})
    return {"n": n, "rows": rows}


# ---------------------------------------------------------------------------


def main():
    data = {"meta": {"leg": "P2 Route-D v12", "alpha": ALPHA, "gamma": GAMMA,
                     "Y0_max_from_v10": Y0_MAX, "A_norm_upper_v10": A_NORM_UB,
                     "c_fixed": C_FIXED}}
    print("T0 profiles ...", flush=True)
    data["t0_profiles"] = t0_profiles()
    print("T1 carry-over ...", flush=True)
    data["t1_carry_over"] = t1_carry_over()
    print("T2 defect ...", flush=True)
    data["t2_defect"] = t2_defect()
    print("T3 structure ...", flush=True)
    data["t3_structure"] = t3_structure()
    print("T4 rate ...", flush=True)
    data["t4_rate"] = t4_rate()
    print("T5 operator ...", flush=True)
    data["t5_operator"] = t5_operator()
    print("T6 boundary ...", flush=True)
    data["t6_boundary"] = t6_boundary()
    data["t7_ledger"] = {
        "changed": "Y0 measured in the certificate's own basis for the first "
                   "time; the a>0 profile is NOT in the decay class the space "
                   "was built for (compact support at X_c, zero of order 1/a)",
        "still_open": ["Z1 core<->far coupling", "Z1 core discretization",
                       "discrete<->continuum transfer",
                       "the space itself: the codomain class assumed a tail the "
                       "object does not have"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    t1, t2 = data["t1_carry_over"], data["t2_defect"]
    print("\nP2 ROUTE-D v12 -- the defect in the bounds' own basis\n" + "=" * 62)
    print("  T1  control (exact anchor, a=0): off-node sup %.1e, codomain norm "
          "%.1e" % (t1["control_exact_anchor"]["raw_sup"],
                    t1["control_exact_anchor"]["norm"]))
    for r in t1["rows"]:
        print("      a=%.2f  rows Newton enforces %.1e | row it displaced %.1e"
              % (r["a"], r["kept_sup"], r["dropped_defect"]))
    print("  T2  ||F||_Y and Y0 <= ||A|| ||F||_Y against the budget %.2e:" % Y0_MAX)
    for r in t2["rows"]:
        print("      a=%.2f  sup %.2e + semi %.2e = %.2e -> Y0 <= %.2e (%.0fx "
              "budget)" % (r["a"], r["sup_part"], r["seminorm_part"],
                           r["F_norm"], r["Y0_upper"], r["over_budget"]))
    print("  T3  X_c/c, two builds:")
    for r in data["t3_structure"]["cross_build"]:
        print("      a=%.2f  theta %.3f vs rho %.3f  (%.2f%%)"
              % (r["a"], r["theta"], r["rho"], 100 * r["rel_gap"]))
    print("  T4  defect vs J: slope %s (predicted %s)"
          % (["%.2f" % x["log_slope"] for x in data["t4_rate"]],
             ["%.2f" % x["predicted_rate"] for x in data["t4_rate"]]))
    print("  T6  X_c / core half-width across a:")
    for r in data["t6_boundary"]["rows"]:
        print("      a=%.3f  X_c=%7.3f  p=%.2f (1/a=%.2f)  X_c/halfwidth=%.2f"
              % (r["a"], r["Xc"], r["zero_order"], r["predicted_zero_order"],
                 r["ratio_Xc_over_halfwidth"]))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
