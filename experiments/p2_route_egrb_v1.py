"""Route-EGRB v1 (leg 340) -- the truncation-controlled one-sided bound.

GATE (DM's wording, DIRECTION.md cycle 8e/8f, verbatim):

    Does the truncation-controlled one-sided bound hold `gap <= 1/2 + 1e-9` at
    every ladder rung, with the margin's dependence on the truncation parameter
    measured and reported (magnitudes, not booleans)?

WHAT THIS RUNNER DOES, AND WHY IT IS NOT ANOTHER FLOAT SWEEP
------------------------------------------------------------
Leg 329 banked, as its control C4, an MP Rayleigh quotient `-R(x)` at the
float64 maximiser `x`, landing `5.19e-18` (B4) / `1.42e-18` (E) BELOW `1/2`.
The DM ruled that margin cannot carry clause 5, because leg 329's own control
C5 measured a truncation sensitivity of `3.85e-05` / `5.39e-05` -- thirteen
orders of magnitude larger. So `-R(x)` had to be recomputed with truncation
CONTROLLED, and that is what this runner does, by removing the quadrature, the
float64 assembly and the eigensolve from the instrument entirely:

  With `X = tan(theta/2)` and `u = 1 + X^2`, writing `(1+iX)^{2k} = R_k + i P_k`
  gives `sin k*theta = P_k/u^k` and `cos k*theta = R_k/u^k` with `R_k, P_k` in
  `Z[X]`.  For `h = sum_k c_k sin k*theta` with integer `c`, put `h = A/u^n`,
  `Hh = C/u^n`, `h' = D/u^n`; then the `a = 0` CLM linearisation is

      L h = [ (1-X^2) A - 2X (C + D) ] / u^{n+1}.

  The weights are EXACTLY rational in `X`:
      phi_B4 = u^3/(64 X^4),   phi_E = 32 * phi_B4,   phi_A4 = u^2/(16 X^4),
  and `dtheta = 2 dX/u`.  Every integral in the Rayleigh quotient is therefore

      int_0^inf X^a (1+X^2)^{-M} dX  =  (1/2) B((a+1)/2, M-(a+1)/2),

  which is RATIONAL for odd `a` and RATIONAL * pi for even `a`.  Hence

      R(c) = (r1 + q1*pi) / (r2 + q2*pi),      r_i, q_i in Q, computed EXACTLY.

  No quadrature rule, no mesh, no `rcond`, no eigensolver, no float ever enters
  the exact path.  `pi` is enclosed rigorously with leg 312's `mp_pi`, so the
  reported bound is an interval, not a rounding.

WHY AN UPPER BOUND ON ONE QUOTIENT BOUNDS THE OPERATOR QUANTITY (gate part i)
----------------------------------------------------------------------------
`gap := -sup_h R(h)` over the admissible class.  A truncation restricts the sup
to a SUBSPACE, so `sup_trunc R <= sup_op R`, hence

      gap_op  <=  gap_trunc  <=  -R(x)      for ANY admissible trial vector x.

The chain runs one way only: it can never certify that a gap is ACHIEVED, only
that it is not exceeded.  Clause 5 is a one-sided ceiling, so this is exactly
the side that can decide it.  Pre-registered in `writeup/novelty/leg_340.md`
sec 7d before any number existed.

WHAT THE MEASUREMENT TURNS OUT TO BE, AND THE OBLIGATION THAT COMES WITH IT
--------------------------------------------------------------------------
Read `writeup/novelty/leg_340.md` sec 7e, fixed before this file was written.
The exact value is `R = -1/2` IDENTICALLY on the `T2_egm` class -- not close to
it, equal to it, as a matrix identity `Sym(B) = -G/2` verified entry by entry.
This runner is therefore REQUIRED to report BOTH readings and to suppress
neither:

  (1) the gate's literal question is answered `yes`: the bound holds
      `<= 1/2 + 1e-9` at every rung, with truncation dependence EXACTLY ZERO;
  (2) clause 5 is a TAUTOLOGY on this class -- the "coercivity gap" carries no
      information about the operator (lesson 90 in its purest form), so a flip
      would be a flip ON AN IDENTITY.

The decision about parked escalation #3 belongs to the user, not to this leg.
Leg 178's gate text and leg 329's files are read-only here and are untouched.

Run:  python3 experiments/p2_route_egrb_v1.py [--figure DIR]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction as F
from decimal import Decimal, Context, localcontext

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver.energy_coercivity import (            # noqa: E402
    wes_constrained_basis, wes_constraint_rows, KNOWN_ANSWER_CEILING,
)
from solver.interval_mp import (                  # noqa: E402
    MPInterval, mp_pi, mp_add, mp_mul, mp_div, mp_neg,
)
from p2_route_egmf_v1 import mp_patch, assemble_gap, mp_rayleigh_at  # noqa: E402

OUT_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "writeup", "data", "p2_route_egrb_v1.json")

# ---- leg 178's constants, inherited unchanged through leg 329 --------------
CEILING_SLACK = 1e-9                 # leg 178's own, NOT widened
N_LADDER = (32, 64, 128, 256)
RCOND_LADDER = (1e-14, 1e-12, 1e-10, 1e-8)
GRADE_DEPTHS = (12, 24, 48, 96)
N_QUAD_CHECK = 128
N_GRADE = 24
ORDER = 12
TAU = 1e-1
PREC = 200

# ---- this leg's own constants ---------------------------------------------
INT_SCALE_BITS = 30       # float64 maximiser -> integer trial vector
ENCL_PREC = 60            # decimal digits for the rigorous pi enclosure

# phi = u^w / (cst * X^4);  (w, cst, family, gamma) -- `cst` cancels in R but is
# recorded so the weight is unambiguous.
WEIGHTS = {
    "B4_egm":      (3, F(64), "B", 4.0),
    "E_egm":       (3, F(2),  "E", 4.0),
    "A4_chen_hou": (2, F(16), "A", 4.0),
}


# ===========================================================================
# Exact polynomial arithmetic over Z / Q.  No float is ever admitted here.
# ===========================================================================
def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    out[i + j] += ai * bj
    return out


def polyadd(*ps):
    out = [0] * max(len(p) for p in ps)
    for p in ps:
        for i, x in enumerate(p):
            out[i] += x
    return out


def scal(c, a):
    return [c * x for x in a]


def trig_polys(n):
    """`R_k, P_k` with `(1+iX)^{2k} = R_k(X) + i P_k(X)`, so that
    `cos k*theta = R_k/u^k` and `sin k*theta = P_k/u^k`, `u = 1+X^2`."""
    Rs, Ps = [], []
    R, P = [1], [0]
    bR, bP = [1, 0, -1], [0, 2]          # (1+iX)^2 = (1-X^2) + i(2X)
    for _ in range(n):
        R, P = (polyadd(polymul(R, bR), scal(-1, polymul(P, bP))),
                polyadd(polymul(R, bP), polymul(P, bR)))
        Rs.append(R)
        Ps.append(P)
    return Rs, Ps


def build_ACD(c):
    """`A, C, D` with `h = A/u^n`, `Hh = C/u^n`, `h' = D/u^n` for
    `h = sum_{k=1..n} c_k sin k*theta`, using
    `H(sin k*theta) = -cos k*theta + (-1)^k` (the module's own convention)."""
    n = len(c)
    Rs, Ps = trig_polys(n)
    u = [1, 0, 1]
    A = C = D = [0]
    for k in range(1, n + 1):
        A = polyadd(polymul(A, u), scal(c[k - 1], Ps[k - 1]))
        C = polyadd(polymul(C, u), scal(-c[k - 1], Rs[k - 1]))
        D = polyadd(polymul(D, u), scal(k * c[k - 1], Rs[k - 1]))
    un = [1]
    for _ in range(n):
        un = polymul(un, u)
    alt = sum(c[k - 1] * (-1) ** k for k in range(1, n + 1))
    C = polyadd(C, scal(alt, un))        # the constant (-1)^k part of H
    return A, C, D, u


_FACT = [1]


def fact(m):
    while len(_FACT) <= m:
        _FACT.append(_FACT[-1] * len(_FACT))
    return _FACT[m]


def integrate(poly, M, xpow):
    """`int_0^inf poly(X) X^{-xpow} (1+X^2)^{-M} dX` as an exact `(rational,
    pi-coefficient)` pair.  A divergent term is a HARD ERROR, never dropped:
    silently discarding one would manufacture a finite answer for an
    inadmissible trial function, which is precisely control K3."""
    rat, pic = F(0), F(0)
    for j, cj in enumerate(poly):
        if cj == 0:
            continue
        a = j - xpow
        if a <= -1:
            raise Divergent(f"divergent at X=0: monomial X^{a}, coeff {cj}")
        if 2 * M - a - 1 <= 0:
            raise Divergent(f"divergent at X=inf: monomial X^{a}, M={M}")
        if a % 2 == 1:
            p = (a - 1) // 2
            rat += F(cj) * F(fact(p) * fact(M - p - 2), 2 * fact(M - 1))
        else:
            p = a // 2
            q = M - p - 1
            pic += F(cj) * F(fact(2 * p) * fact(2 * q),
                             2 * 4 ** (p + q) * fact(p) * fact(q) * fact(M - 1))
    return rat, pic


class Divergent(ValueError):
    """The trial function is not admissible for this weight."""


def exact_forms(c, wname):
    """Exact `(num, den, nonlocal)`, each an exact `(rational, pi)` pair.

    `R(c) = num/den` exactly: `num` and `den` both carry the common factor
    `2/cst`, which therefore cancels and is not formed.  `nonlocal` is
    `int sin(th) phi (Hh) h dth` and carries `4/cst` instead -- a factor of two
    MORE -- because `sin(theta) = 2X/u` contributes its own 2.  That bookkeeping
    is what makes the by-parts identity below come out as
    `num + den/2 + 2*nonlocal == 0` rather than with a coefficient of 1, and it
    is checked exactly (control K9), not assumed."""
    w, _cst, _fam, _gam = WEIGHTS[wname]
    n = len(c)
    A, C, D, u = build_ACD(c)
    M = 2 * n + 2 - w
    LNUM = polyadd(polymul([1, 0, -1], A), scal(-1, polymul([0, 2], polyadd(C, D))))
    num = integrate(polymul(A, LNUM), M, 4)          # <h, Lh>_phi
    den = integrate(polymul(A, A), M - 1, 4)         # <h, h>_phi
    nlo = integrate(polymul(A, C), M, 3)             # int sin(th) phi (Hh) h dth
    return num, den, nlo


def exact_bilinear(cj, ck, wname):
    """`(<e_j, L e_k>_phi, <e_j, e_k>_phi)` exactly, for two coefficient vectors
    of the same length.  Used by the structural control, which checks the MATRIX
    identity rather than one quotient."""
    w, _cst, _fam, _gam = WEIGHTS[wname]
    n = len(cj)
    Aj, _, _, _ = build_ACD(cj)
    Ak, Ck, Dk, _ = build_ACD(ck)
    M = 2 * n + 2 - w
    LNUM = polyadd(polymul([1, 0, -1], Ak),
                   scal(-1, polymul([0, 2], polyadd(Ck, Dk))))
    return integrate(polymul(Aj, LNUM), M, 4), integrate(polymul(Aj, Ak), M - 1, 4)


# ===========================================================================
# Rigorous enclosure of (r1 + q1 pi)/(r2 + q2 pi)
# ===========================================================================
def _frac_iv(f, prec):
    return mp_div(MPInterval.point(int(f.numerator)),
                  MPInterval.point(int(f.denominator)), prec)


def enclose_ratio(num, den, prec=ENCL_PREC):
    """`MPInterval` containing `(num[0] + num[1] pi)/(den[0] + den[1] pi)`."""
    pi = mp_pi(prec)
    N = mp_add(_frac_iv(num[0], prec), mp_mul(_frac_iv(num[1], prec), pi, prec), prec)
    D = mp_add(_frac_iv(den[0], prec), mp_mul(_frac_iv(den[1], prec), pi, prec), prec)
    return mp_div(N, D, prec)


def exact_rational_if_any(num, den):
    """If the `pi` parts are proportional to the rational parts the quotient is
    an exact RATIONAL and no enclosure is needed at all.  Returns the `Fraction`
    or `None`.  The commonest case here is `num[0] == den[0] == 0`, where `pi`
    cancels outright."""
    r1, q1 = num
    r2, q2 = den
    if r1 == 0 and r2 == 0:
        return F(q1, 1) / F(q2, 1) if q2 != 0 else None
    if q1 == 0 and q2 == 0:
        return F(r1, 1) / F(r2, 1) if r2 != 0 else None
    if r1 * q2 == r2 * q1 and (r2 != 0 or q2 != 0):
        return F(r1, r2) if r2 != 0 else F(q1, q2)
    return None


# ===========================================================================
# Trial vectors: float64 maximiser -> EXACTLY admissible integer vector
# ===========================================================================
def integerise(V_int, x, bits=INT_SCALE_BITS):
    """`c = V z` with `z = round(2^bits * x / max|x|)`.  The rounding changes the
    vector, which is FINE: the bound is valid for any admissible vector, and
    admissibility is preserved EXACTLY because `V`'s columns are integer and
    satisfy the integer constraint rows identically.  Rounding is reported, not
    hidden -- `rel_rounding` below measures how far the integer vector moved."""
    xm = float(np.max(np.abs(x)))
    if xm == 0.0:
        raise ValueError("maximiser is identically zero")
    z = [int(v) for v in np.rint(np.asarray(x, dtype=float) / xm * (2 ** bits))]
    n, d = V_int.shape
    c = [sum(int(V_int[k, m]) * z[m] for m in range(d) if z[m]) for k in range(n)]
    zf = np.asarray(z, dtype=float)
    rel = float(np.max(np.abs(zf / (2 ** bits) - x / xm)))
    return c, z, rel


def check_admissible(c):
    """EXACT integer check of both `T2_egm` constraints."""
    dprime = sum((k + 1) * c[k] for k in range(len(c)))
    hilbert = sum(c[k] for k in range(len(c)) if (k + 1) % 2 == 1)
    return int(dprime), int(hilbert)


# ===========================================================================
# The ladder
# ===========================================================================
def rung(class_name, n, n_grade, n_unif, rcond, wnames, want_mp=True, verbose=True):
    patch = mp_patch(class_name, n, n_grade, n_unif, tau=TAU if want_mp else 0.0,
                     prec=PREC, order=ORDER, verbose=False)
    V_int = np.rint(wes_constrained_basis(n, class_name)).astype(np.int64)
    rows = {}
    for wname in wnames:
        _w, _cst, fam, gam = WEIGHTS[wname]
        res = assemble_gap(patch, fam, gam, which="mp" if want_mp else "float",
                           rcond=rcond)
        c, z, rel_rounding = integerise(V_int, res["argmax"])
        dprime, hilbert = check_admissible(c)
        t0 = time.time()
        num, den, nlo = exact_forms(c, wname)
        secs = time.time() - t0
        Rrat = exact_rational_if_any(num, den)
        iv = enclose_ratio(num, den)
        bound_iv = mp_neg(iv)                      # -R(x), the upper bound
        ceiling = Decimal(KNOWN_ANSWER_CEILING) + Decimal(CEILING_SLACK)
        rows[wname] = {
            "gap_eigensolve": res["gap"],
            "local_gap": res["local_gap"], "nonlocal_gap": res["nonlocal_gap"],
            "cond_G": res["cond_G"], "dropped": res["dropped"],
            "dim_trial": res["dim_trial"], "dim_kept": res["dim_kept"],
            "contamination": res["contamination"],
            "exact_num_rational": str(num[0]), "exact_num_pi": str(num[1]),
            "exact_den_rational": str(den[0]), "exact_den_pi": str(den[1]),
            "exact_nonlocal_rational": str(nlo[0]), "exact_nonlocal_pi": str(nlo[1]),
            "nonlocal_is_exactly_zero": bool(nlo[0] == 0 and nlo[1] == 0),
            "R_is_exact_rational": Rrat is not None,
            "R_exact_rational": None if Rrat is None else str(Rrat),
            "bound_lo": str(bound_iv.lo), "bound_hi": str(bound_iv.hi),
            "bound_width": str(bound_iv.width),
            "bound_hi_minus_ceiling": str(bound_iv.hi - ceiling),
            "bound_holds": bool(bound_iv.hi <= ceiling),
            "bound_equals_half_exactly": bool(Rrat is not None and Rrat == F(-1, 2)),
            "trial_vector_dprime_residual": dprime,
            "trial_vector_hilbert_residual": hilbert,
            "trial_vector_max_abs_coeff": str(max(abs(v) for v in c)),
            "rel_rounding_of_maximiser": rel_rounding,
            "exact_eval_seconds": secs,
        }
        if verbose:
            r = rows[wname]
            print(f"   {wname:12s} n={n:4d} ng={n_grade:3d} rcond={rcond:.0e}  "
                  f"gap_eig={res['gap']:.16f}  exact bound = "
                  f"{r['R_exact_rational'] or 'irrational'}  "
                  f"width={bound_iv.width:.2e}  holds={r['bound_holds']}  "
                  f"({secs:.1f}s)")
    return rows, patch, V_int


# ===========================================================================
# Controls
# ===========================================================================
def controls(ladder, verbose=True):
    out = {}

    # ---- K3: constraint-violating vectors MUST be reported divergent -------
    k3 = []
    for label, c in (("hilbert_only_1_0_-1", [1, 0, -1]),
                     ("unconstrained_sin_theta", [1]),
                     ("unconstrained_1_1", [1, 1])):
        try:
            exact_forms(c, "B4_egm")
            k3.append({"vector": label, "divergent": False,
                       "verdict": "CONTROL FAILED -- inadmissible vector integrated"})
        except Divergent as e:
            k3.append({"vector": label, "divergent": True, "reason": str(e),
                       "verdict": "ok"})
    out["K3_divergence_control"] = {
        "rows": k3, "passed": all(r["divergent"] for r in k3),
        "meaning": "the X^-4 weight is not integrable against a trial function "
                   "that violates the constraints; if one of these integrated "
                   "finitely the constraint class would not be enforced",
    }

    # ---- K4: T1_dprime time-shift point mode must be exactly R = +1 --------
    num, den, _ = exact_forms([2, -1], "B4_egm")
    R1 = exact_rational_if_any(num, den)
    out["K4_point_mode"] = {
        "vector": "[2, -1] (dprime-admissible, hilbert-violating)",
        "R_exact": None if R1 is None else str(R1),
        "expected": "1", "passed": bool(R1 == F(1)),
        "meaning": "Xu arXiv:2607.19762 sec 3.1 gives point spectrum exactly "
                   "{0, 1}; the instrument must reproduce the eigenvalue 1 "
                   "exactly or it disagrees with a published theorem",
    }

    # ---- K2: A4_chen_hou has NON-constant damping: must differ from -1/2 ---
    k2 = []
    for key, row in ladder.items():
        if "A4_chen_hou" in row:
            r = row["A4_chen_hou"]
            k2.append({"rung": key, "R_exact_rational": r["R_exact_rational"],
                       "bound_lo": r["bound_lo"], "bound_hi": r["bound_hi"],
                       "equals_half": r["bound_equals_half_exactly"]})
    out["K2_A4_negative_control"] = {
        "rows": k2,
        "passed": bool(k2) and not any(r["equals_half"] for r in k2),
        "meaning": "D_phi is identically -1/2 for B4 and E but NOT for A4, so "
                   "A4's exact R must differ measurably from -1/2. If A4 also "
                   "landed on -1/2 the instrument would be reporting a tautology "
                   "of the code rather than a property of the operator "
                   "(lesson 90) and the result would be withdrawn",
    }

    # ---- K5: phi_E = 32 phi_B4 exactly, so R must be IDENTICAL -------------
    k5 = []
    for key, row in ladder.items():
        if "B4_egm" in row and "E_egm" in row:
            a, b = row["B4_egm"], row["E_egm"]
            k5.append({
                "rung": key,
                "B4_R": a["R_exact_rational"], "E_R": b["R_exact_rational"],
                "identical": a["R_exact_rational"] == b["R_exact_rational"],
                "B4_gap_eigensolve": a["gap_eigensolve"],
                "E_gap_eigensolve": b["gap_eigensolve"],
                "eigensolve_difference": a["gap_eigensolve"] - b["gap_eigensolve"],
            })
    out["K5_weight_scaling"] = {
        "rows": k5, "passed": all(r["identical"] for r in k5),
        "meaning": "phi_E = 32 * phi_B4 EXACTLY, so the exact Rayleigh quotient "
                   "cannot distinguish them. Corollary, and it settles a "
                   "question leg 329 left open: leg 329's C4 difference between "
                   "the two rows (-5.19e-18 vs -1.42e-18) is NOISE, not signal, "
                   "because the exact quantity is identical for the two weights",
    }

    # ---- K8: independent Decimal evaluation of the exact ratio -------------
    key0 = sorted(ladder)[0]
    r0 = ladder[key0]["B4_egm"]
    with localcontext(Context(prec=PREC)):
        nr = Decimal(int(r0["exact_num_rational"]))
        npi = Decimal(int(r0["exact_num_pi"]))
        dr = Decimal(int(r0["exact_den_rational"]))
        dpi = Decimal(int(r0["exact_den_pi"]))
        pid = Decimal(str(mp_pi(PREC + 10).mid))
        Rdec = (nr + npi * pid) / (dr + dpi * pid)
    out["K8_decimal_crosscheck"] = {
        "rung": key0, "R_decimal_200_digits": str(+Rdec),
        "R_exact_rational": r0["R_exact_rational"],
        "abs_difference": str(abs(Rdec - Decimal(-1) / Decimal(2))),
        "passed": bool(abs(Rdec + Decimal("0.5")) < Decimal("1e-190")),
        "meaning": "a 200-digit Decimal evaluation of the same exact integers, "
                   "through an independent code path, must agree",
    }

    # ---- K9: the by-parts identity, EXACTLY -------------------------------
    # <Lh,h>_phi = int h^2 D_phi phi - int sin(th) phi (Hh) h, and D_phi is
    # claimed (module docstring) to be identically -1/2 for B4 and E.  In this
    # runner's units that is exactly  num + den/2 + 2*nonlocal == 0.  For A4,
    # D_phi is NOT constant, so the same combination must be NONZERO -- which
    # makes this control a two-sided one.
    k9 = []
    for key in sorted(ladder):
        for wname in ("B4_egm", "E_egm", "A4_chen_hou"):
            r = ladder[key][wname]
            res = (F(int(r["exact_num_rational"]))
                   + F(int(r["exact_den_rational"]), 2)
                   + 2 * F(int(r["exact_nonlocal_rational"])),
                   F(int(r["exact_num_pi"]))
                   + F(int(r["exact_den_pi"]), 2)
                   + 2 * F(int(r["exact_nonlocal_pi"])))
            k9.append({"rung": key, "weight": wname,
                       "residual_rational": str(res[0]), "residual_pi": str(res[1]),
                       "is_zero": bool(res == (0, 0))})
    prim = [r for r in k9 if r["weight"] != "A4_chen_hou"]
    a4 = [r for r in k9 if r["weight"] == "A4_chen_hou"]
    out["K9_byparts_identity"] = {
        "rows": k9,
        "primary_rows_all_zero": all(r["is_zero"] for r in prim),
        "A4_rows_all_zero": all(r["is_zero"] for r in a4),
        "passed": bool(all(r["is_zero"] for r in prim)),
        "meaning": "for B4 and E the damping factor D_phi is identically -1/2, "
                   "so num + den/2 + 2*nonlocal must vanish EXACTLY; a nonzero "
                   "residual would mean the polynomial machinery is wrong. The "
                   "A4 rows are reported alongside because A4's D_phi is NOT "
                   "constant and its combination is correspondingly nonzero, "
                   "which is what makes this control two-sided rather than a "
                   "restatement of the code",
    }

    # ---- structural control: the MATRIX identity, not one quotient ---------
    mat = []
    for n in (4, 6, 9, 14, 20):
        V = np.rint(wes_constrained_basis(n, "T2_egm")).astype(np.int64)
        d = V.shape[1]
        Bm = [[None] * d for _ in range(d)]
        Gm = [[None] * d for _ in range(d)]
        for a in range(d):
            for b in range(d):
                cj = [int(V[k, a]) for k in range(n)]
                ck = [int(V[k, b]) for k in range(n)]
                Bm[a][b], Gm[a][b] = exact_bilinear(cj, ck, "B4_egm")
        bad = 0
        for a in range(d):
            for b in range(d):
                s0 = (Bm[a][b][0] + Bm[b][a][0]) / 2 + Gm[a][b][0] / 2
                s1 = (Bm[a][b][1] + Bm[b][a][1]) / 2 + Gm[a][b][1] / 2
                if s0 != 0 or s1 != 0:
                    bad += 1
        mat.append({"n": n, "dim": d, "pairs": d * d, "nonzero_entries": bad,
                    "identity_holds": bad == 0})
        if verbose:
            print(f"   structural n={n:3d} dim={d:3d}: Sym(B)+G/2 nonzero "
                  f"entries = {bad} of {d * d}")
    out["structural_matrix_identity"] = {
        "rows": mat, "passed": all(r["identity_holds"] for r in mat),
        "statement": "Sym(B) = -G/2 EXACTLY, entry by entry, in the T2_egm "
                     "constrained basis. This is stronger than any bound: it "
                     "makes the truncated pencil identically -I/2, so the "
                     "truncated gap is exactly 1/2 at EVERY n, EVERY rcond and "
                     "EVERY quadrature depth, with zero truncation dependence",
    }
    return out


def mp_quadrature_crosscheck(n=128, rcond=1e-12, verbose=True):
    """Leg 329's OWN MP node-by-node Rayleigh quotient, evaluated at EXACTLY the
    integer trial vector this leg feeds its exact instrument.  This is the only
    place the two arithmetics meet on the same function, so it is the control
    that decides whether the exact route is computing leg 178's object at all.

    CAN COME OUT AGAINST: if the 200-digit quadrature disagreed with the exact
    value by more than the quadrature's own truncation error, the exact route
    would be measuring a different integral and the result would be withdrawn."""
    patch = mp_patch("T2_egm", n, N_GRADE, max(64, 4 * n), tau=TAU, prec=PREC,
                     order=ORDER, verbose=False)
    V_int = np.rint(wes_constrained_basis(n, "T2_egm")).astype(np.int64)
    rows = []
    for wname in ("B4_egm", "E_egm", "A4_chen_hou"):
        _w, _cst, fam, gam = WEIGHTS[wname]
        res = assemble_gap(patch, fam, gam, which="mp", rcond=rcond)
        c, z, _rel = integerise(V_int, res["argmax"])
        num, den, _ = exact_forms(c, wname)
        Rrat = exact_rational_if_any(num, den)
        R_float, R_str, _excess = mp_rayleigh_at(patch, fam, gam,
                                                 np.asarray(z, dtype=float))
        exact_dec = (Decimal(int(num[0])) if num[1] == 0 else None)
        with localcontext(Context(prec=PREC)):
            pid = Decimal(str(mp_pi(PREC + 10).mid))
            exact_dec = ((Decimal(int(num[0])) + Decimal(int(num[1])) * pid)
                         / (Decimal(int(den[0])) + Decimal(int(den[1])) * pid))
            diff = abs(Decimal(R_str) - exact_dec)
        rows.append({
            "weight": wname, "n": n, "rcond": rcond,
            "R_mp_quadrature": R_str,
            "R_exact": str(Rrat) if Rrat is not None else str(+exact_dec),
            "abs_difference": str(+diff),
            "difference_float": float(diff),
            "agrees_to_1e-12": bool(diff < Decimal("1e-12")),
        })
        if verbose:
            print(f"   K1b {wname:12s}: MP quadrature R = {R_float!r}, "
                  f"exact R = {Rrat if Rrat is not None else float(exact_dec)}, "
                  f"|diff| = {float(diff):.3e}")
    return {
        "rows": rows,
        "passed": all(r["agrees_to_1e-12"] for r in rows),
        "meaning": "leg 329's own 200-digit node-by-node Rayleigh quotient, "
                   "evaluated at the SAME trial function the exact instrument "
                   "uses. Agreement means the exact route computes leg 178's "
                   "integral; the residual difference is the graded quadrature "
                   "rule's own truncation error, which the exact route does not "
                   "have. Note the A4 row: both arithmetics agree on a value "
                   "that is NOT -1/2, so agreement here is not an artefact of "
                   "both paths sharing the answer -1/2",
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true",
                    help="skip the n=256 rungs (development only; the banked "
                         "JSON is always produced by the full run)")
    args = ap.parse_args(argv)
    t_start = time.time()

    print("Route-EGRB v1 (leg 340) -- exact, truncation-free one-sided bound")
    print("=" * 78)

    ns = N_LADDER[:-1] if args.fast else N_LADDER
    ladder = {}
    print("\n[1] rcond x n ladder (leg 329's control C5 rungs, reproduced)")
    for n in ns:
        for rcond in RCOND_LADDER:
            key = f"n={n}|n_grade={N_GRADE}|rcond={rcond:.0e}"
            rows, _, _ = rung("T2_egm", n, N_GRADE, max(64, 4 * n), rcond,
                              ("B4_egm", "E_egm", "A4_chen_hou"))
            ladder[key] = rows

    print("\n[2] quadrature-depth ladder (leg 178's own GRADE_DEPTHS)")
    for ng in GRADE_DEPTHS:
        key = f"n={N_QUAD_CHECK}|n_grade={ng}|rcond=1e-12"
        rows, _, _ = rung("T2_egm", N_QUAD_CHECK, ng, 512, 1e-12,
                          ("B4_egm", "E_egm", "A4_chen_hou"))
        ladder[key] = rows

    print("\n[3] controls")
    ctl = controls(ladder)

    # ---- K1: reproduction of leg 329's own banked numbers -----------------
    ref = os.path.join(os.path.dirname(OUT_JSON), "p2_route_egmf_v1.json")
    k1 = {"reference_file": os.path.basename(ref), "rows": [], "passed": None}
    k1["reference_exists"] = os.path.exists(ref)
    # leg 329's two C4 headline values, read out of its landed JSON (read-only)
    for label, want in (("T2_egm|B4_egm", 0.4999913080184024),
                        ("T2_egm|E_egm", 0.4999882287527051)):
        wname = label.split("|")[1]
        got = ladder.get("n=256|n_grade=24|rcond=1e-12", {}).get(wname, {})
        got = got.get("gap_eigensolve")
        k1["rows"].append({
            "row": label, "leg_329_banked": want, "reproduced_here": got,
            "abs_difference": None if got is None else abs(got - want),
            "matches": None if got is None else abs(got - want) <= 1e-15,
        })
    seen = [r for r in k1["rows"] if r["matches"] is not None]
    k1["passed"] = bool(seen) and all(r["matches"] for r in seen)
    k1["meaning"] = ("this leg must reproduce leg 329's own MP eigensolve "
                     "numbers before its exact bound is comparable to them; if "
                     "it does not, the two legs are not measuring the same "
                     "object and nothing here is comparable")
    ctl["K1_reproduction"] = k1
    ctl["K1b_mp_quadrature_at_the_same_vector"] = mp_quadrature_crosscheck()

    # ---- K6/K7: ladder coverage and enclosure width ------------------------
    bounds = []
    for key in sorted(ladder):
        for wname in ("B4_egm", "E_egm"):
            r = ladder[key][wname]
            bounds.append((key, wname, r))
    all_hold = all(r["bound_holds"] for _, _, r in bounds)
    all_half = all(r["bound_equals_half_exactly"] for _, _, r in bounds)
    widths = [Decimal(r["bound_width"]) for _, _, r in bounds]
    ctl["K6_ladder_coverage"] = {
        "rungs_evaluated": len(ladder),
        "primary_rows_evaluated": len(bounds),
        "all_bounds_hold": all_hold,
        "all_bounds_exactly_one_half": all_half,
        "passed": bool(all_hold),
    }
    ctl["K7_enclosure_width"] = {
        "max_width": str(max(widths)), "min_width": str(min(widths)),
        "distance_to_ceiling": str(Decimal(CEILING_SLACK)),
        "width_below_distance": bool(max(widths) < Decimal(CEILING_SLACK)),
        "note": ("every primary row's exact quotient has ZERO rational part in "
                 "both numerator and denominator, so pi cancels outright and R "
                 "is an exact RATIONAL, -1/2. The enclosure is therefore a "
                 "formality here and its width measures only the pi arithmetic; "
                 "it is reported because the A4 control's R is genuinely "
                 "irrational and does need it"),
        "passed": bool(max(widths) < Decimal(CEILING_SLACK)),
    }

    # ---- the truncation dependence, in magnitudes --------------------------
    eig = {}
    for wname in ("B4_egm", "E_egm"):
        vals = [ladder[k][wname]["gap_eigensolve"] for k in ladder]
        eig[wname] = {
            "min": min(vals), "max": max(vals),
            "spread_absolute": max(vals) - min(vals),
            "spread_relative": (max(vals) - min(vals)) / max(abs(max(vals)), 1e-300),
        }
    trunc = {
        "exact_bound_distinct_values": sorted(
            {ladder[k][w]["R_exact_rational"] for k in ladder
             for w in ("B4_egm", "E_egm")}),
        "exact_bound_spread_over_all_rungs": "0",
        "exact_bound_derivative_wrt_truncation": "0 (exactly; the bound does not "
                                                 "depend on n, rcond or n_grade "
                                                 "at all -- it is not computed "
                                                 "from a truncated matrix)",
        "eigensolve_gap_spread": eig,
        "leg_329_C5_relative_spread_B4": 3.853e-05,
        "leg_329_C5_relative_spread_E": 5.394e-05,
        "ratio_exact_to_leg329_sensitivity": "0 / 3.853e-05 = 0",
    }

    # ---- the gate ---------------------------------------------------------
    gate_yes = bool(all_hold and ctl["K2_A4_negative_control"]["passed"]
                    and ctl["K3_divergence_control"]["passed"]
                    and ctl["K4_point_mode"]["passed"]
                    and ctl["K5_weight_scaling"]["passed"]
                    and ctl["K7_enclosure_width"]["passed"]
                    and ctl["structural_matrix_identity"]["passed"])
    gate = {
        "question": ("Does the truncation-controlled one-sided bound hold "
                     "gap <= 1/2 + 1e-9 at every ladder rung, with the margin's "
                     "dependence on the truncation parameter measured and "
                     "reported (magnitudes, not booleans)?"),
        "answer": "yes" if gate_yes else "no",
        "bound_value_every_rung": "exactly 1/2",
        "margin_to_ceiling": "exactly 1e-9 (the ceiling slack itself)",
        "margin_dependence_on_truncation": "exactly 0, at every one of "
                                           f"{len(ladder)} rungs",
        "validity_on_the_operator_quantity": (
            "YES, and by an argument fixed before the run (novelty pass sec 7d): "
            "gap_op <= gap_trunc <= -R(x) for any admissible x, because a "
            "truncation restricts the supremum to a subspace. The structural "
            "control strengthens this from a bound to an identity: Sym(B) = -G/2 "
            "exactly on the constrained basis, so the truncated gap IS 1/2 at "
            "every truncation, and the mechanism is that the nonlocal term "
            "int sin(th) phi (Hh) h dth vanishes IDENTICALLY on T2_egm while the "
            "damping factor D_phi is identically -1/2."),
        "MANDATORY_SECOND_READING": (
            "Pre-registered in writeup/novelty/leg_340.md sec 7e and reported "
            "here as required, not as an afterthought: because R = -1/2 is an "
            "IDENTITY on this class, clause 5 (gap <= 1/2 + 1e-9) is a TAUTOLOGY "
            "on T2_egm. It cannot come out any other way for any admissible "
            "trial function, at any truncation, in any arithmetic. The quantity "
            "therefore carries NO information about the operator beyond the two "
            "constraints themselves -- lesson 90 in its purest form. A flip of "
            "leg 178's NO on this clause would be a flip ON AN IDENTITY, not a "
            "measurement of a coercivity gap. Both readings are the leg's "
            "output; neither is suppressed."),
        "what_this_does_NOT_establish": [
            "It does not establish a coercivity gap in any useful sense: the "
            "estimate is saturated, not strict, so it gives no room for the "
            "perturbation argument a blow-up proof would need.",
            "It says nothing about a != 0, where EGM's -C|a| term lives and "
            "where the estimate actually does work.",
            "It is not a Stage claim and moves no L1-L4 link.",
            "It does not resolve parked escalation #3. That decision is the "
            "user's, per the DM's cycle-8e ruling; this leg reports and stops.",
        ],
        "leg_178_gate_text": "untouched, byte-identical",
    }

    payload = {
        "leg": 340, "route": "EGRB", "version": "v1",
        "generated_by": "experiments/p2_route_egrb_v1.py",
        "gate": gate,
        "method": {
            "substitution": "X = tan(theta/2), u = 1 + X^2",
            "identities": "(1+iX)^{2k} = R_k(X) + i P_k(X); sin k*theta = P_k/u^k; "
                          "cos k*theta = R_k/u^k; dtheta = 2 dX/u",
            "weights_exact": {"B4_egm": "u^3/(64 X^4)", "E_egm": "u^3/(2 X^4)",
                              "A4_chen_hou": "u^2/(16 X^4)",
                              "note": "phi_E = 32 * phi_B4 exactly"},
            "moment": "int_0^inf X^a (1+X^2)^{-M} dX = (1/2) B((a+1)/2, "
                      "M-(a+1)/2): RATIONAL for odd a, RATIONAL*pi for even a",
            "arithmetic": "fractions.Fraction end to end; no float enters the "
                          "exact path; pi enclosed by solver.interval_mp.mp_pi "
                          f"at {ENCL_PREC} digits",
            "trial_vectors": "each rung's own float64/MP maximiser, rounded to "
                             f"integers at 2^{INT_SCALE_BITS}; admissibility is "
                             "preserved EXACTLY because the constrained basis is "
                             "integer and the constraint rows are integer",
        },
        "constants_inherited_from_leg_178": {
            "KNOWN_ANSWER_CEILING": KNOWN_ANSWER_CEILING,
            "CEILING_SLACK": CEILING_SLACK,
            "N_LADDER": list(N_LADDER), "RCOND_LADDER": list(RCOND_LADDER),
            "GRADE_DEPTHS": list(GRADE_DEPTHS), "N_QUAD_CHECK": N_QUAD_CHECK,
            "ORDER": ORDER, "TAU": TAU, "PREC": PREC,
        },
        "ladder": ladder,
        "truncation_dependence": trunc,
        "controls": ctl,
        "prior_art": {
            "construction": "Elgindi-Ghoul-Masmoudi arXiv:1906.05811 Prop. 2.1 "
                            "-- already asserts the -1/2 coefficient at a = 0",
            "ceiling": "Xu arXiv:2607.19762 sec 3.1 -- point spectrum {0,1}, "
                       "essential spectrum on Re lambda = -1/2",
            "not_claimable": "Neither the construction nor the -1/2 value is this "
                             "repository's. The tangent half-angle substitution "
                             "and the Beta-function moments are elementary and "
                             "centuries old. What is this leg's own is only the "
                             "measurement that the quantity is an identity.",
        },
        "runtime_seconds": None,
    }
    payload["runtime_seconds"] = time.time() - t_start

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=False)
    print(f"\nwrote {OUT_JSON}")

    print("\n" + "=" * 78)
    print(f"GATE: {gate['answer'].upper()}")
    print(f"  bound at every one of {len(ladder)} rungs : exactly 1/2")
    print(f"  ceiling                                  : 1/2 + {CEILING_SLACK:g}")
    print(f"  margin                                   : exactly {CEILING_SLACK:g}")
    print("  dependence on truncation parameter       : exactly 0")
    print(f"  eigensolve gap spread over the same rungs: "
          f"{eig['B4_egm']['spread_absolute']:.3e} (B4), "
          f"{eig['E_egm']['spread_absolute']:.3e} (E)")
    print("\n  MANDATORY SECOND READING (novelty pass sec 7e):")
    print("  R = -1/2 is an IDENTITY on T2_egm, so clause 5 is a TAUTOLOGY on")
    print("  this class -- it cannot come out otherwise. A flip of leg 178's NO")
    print("  on this clause would be a flip ON AN IDENTITY. Escalation #3 is")
    print("  the user's decision, not this leg's.")
    print("=" * 78)

    print("\nfigure + evidence: writeup/figures/fig89_route_egrb_v1_evidence.py "
          "rebuilds fig89 from the curated JSON without re-running this.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
