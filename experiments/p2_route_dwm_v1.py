#!/usr/bin/env python3
"""Leg 305 (Route-DWM) -- per-constant width ledger of BCG's own r-dominance argument.

    .venv/bin/python experiments/p2_route_dwm_v1.py

THE QUESTION.  Leg 266 (verified and corrected by leg 300, propagated by leg 319) fixed the
certificate obligation at the stability step with F_dis RETAINED, r OUTSIDE the dominance
window (1.1666667, 1.1909830) -- 6.854x narrower than the target window (1, 7/6], closed form
(7 + 3 sqrt 5)/2.  Nobody knew whether that width is SHARP for BCG's argument or an artifact of
one generous intermediate constant.  This runner re-derives the window tracking every
intermediate constant and measures which constant costs the most width.

    Source: Buckmaster, Cao-Labora, Gomez-Serrano, arXiv:2208.09445,
    "Smooth imploding solutions for 3D compressible fluids", Forum of Math. Pi 13 e6 (2025).
    e-print tarball md5 45ea63c45a1a199ecfb4dc4a15431600 (the tarball leg 266 banked),
    file RadialImplosion31_FinalArxiv.tex.  Every `l.NNN` below is a line in that file.

INDEPENDENCE OF THE CODE PATH (pre-registered, journal Part I sec 3).  Leg 240 already banked
these endpoints; leg 300 re-derived the ratio.  A reproduction through the same formula is not
a reproduction, so BOTH endpoints are re-derived here from DIFFERENT displayed equations than
either leg used:

  * upper endpoint: legs 240 and 300 both evaluated BCG's CLOSED FORM \\eqref{eq:rstar}
    (l.352-358) directly.  This runner instead ROOT-SOLVES the upstream Jacobian quantity
        D_{Z,1}(r,g) = -4 + (1+g)(r-1)/(g-1) + R_2(r,g) = 0
    from \\eqref{eq:k_asquotientDZ1} (l.600) -- the quantity whose vanishing is what CAUSES
    k -> infinity (Lemma \\ref{lemma:k}, l.579-583, and its proof at l.605).  R_2 is transcribed
    from \\eqref{eq:def_R2} (l.547-551), R_1 from \\eqref{eq:R1} (l.526-528).
  * lower endpoint: leg 240 used CGSS (1.8).  This runner reads the exponent straight off BCG's
    own displayed PDE \\eqref{eq:main} (l.483), e^{(2 - r + (1/alpha)(1-r)) s}, whose sign
    condition is \\eqref{eq:delta:dis} (l.489-491), and SOLVES for the root rather than quoting
    \\eqref{eq:r:restriction}'s 2g/(g+1).
  * arithmetic: 60-decimal-digit `decimal` throughout (leg 300's house pattern).  IEEE double
    appears ONLY as a deliberately contrasted control -- see the trap below.

\\eqref{eq:rstar} is evaluated in exactly one place -- CHECK T4 -- purely as the cross-check
that the root-solve reproduces it.  Nothing else in this file consumes it.

THE r=1 CONDITIONING TRAP, EXPECTED AND PRE-REGISTERED (tolerance T5).  BCG state at l.603
that R_2 = 0 at r = 1, hence k(1) = 1.  The radicand is a sum of terms of magnitude up to
24.528 cancelling to EXACTLY zero there, so in IEEE double it evaluates to rounding dust and
the square root costs half the digits.  Leg 302 measured |k(1) - 1| = 1.29e-07 against a 1e-9
tolerance and proved by a 60-digit path that the TRANSCRIPTION was correct and the ARITHMETIC
was not.  This runner reproduces both sides on purpose: the float evaluation is EXPECTED TO
FAIL and the 60-digit evaluation is REQUIRED to pass.  A conditioning artifact reported as a
sharpness finding would be a serious error, so the float number is emitted under the key
`conditioning_trap`, decides nothing, and is labelled as diagnostic everywhere it appears.

RUNTIME.  Assessed before running (standing rule).  The first draft used linear scans and
would have taken hours; every scan was replaced by an expanding geometric bracket plus
bisection, and the two endpoints are recomputed only when the perturbed constant can actually
move them.  Estimate after that change: under two minutes.  Achieved runtime is printed and
banked in the JSON as `runtime_s`.

NO SOLVER IMPORT, NO NETWORK, NO CERTIFICATE, STDLIB + NOTHING ELSE.  capabilities.py was
grepped (666 lines; zero hits on bcg/2208.09445/implos/compressible/r_star/dominance) and is
not imported.  This is closed-form algebra on a published argument.  Measuring the shape of an
obligation is NOT discharging it: Walls 1 and 2 stand, and the object is 3D COMPRESSIBLE
Navier-Stokes at gamma = 7/5, which is NOT the incompressible system the Clay problem asks
about.  Clay odds ~0.05%, unchanged.
"""

import json
import math
import os
import time
from decimal import Decimal, getcontext, InvalidOperation, localcontext

getcontext().prec = 60

D = Decimal
GAMMA_BCG = D(7) / D(5)
EPS_SENS = D("1e-5")
EPS_SENS_2 = D("1e-6")
TINY = D("1e-40")

TOL = {"T1_endpoints_vs_leg240": D("5e-8"),
       "T2_gamma_ceiling_vs_leg240": D("5e-13"),
       "T3_closed_forms": D("1e-40"),
       "T4_rootsolve_vs_closed_form": D("1e-40"),
       "T5_k_of_1_highprec": D("1e-40"),
       "T5_k_of_1_float_expected_to_fail_at": 1e-9,
       "T6_elasticity_linearity_rel": D("1e-4")}

# Leg 240's and leg 300's banked answers.  REFERENCE ONLY -- reproduced here, never re-claimed.
KNOWN = {"K1_lower_endpoint": D("1.1666667"), "K2_upper_endpoint": D("1.1909830"),
         "K3_width": D("2.43e-02"), "K4_delta_dis_max": D("0.1458980"),
         "K5_gamma_ceiling": D("2.154700538379"), "K6_grid_max_dev": D("1.78e-15"),
         "K7_width_ratio": D("6.854")}


def sqrtD(x):
    """Square root in 60-digit decimal.

    A radicand that is negative only at the rounding level is clamped to zero: BOTH radicands
    in this file vanish EXACTLY at points we evaluate at (R_2 at r = 1, BCG l.603; R_1 at
    r = r*), so a 1e-58 negative there is the last digit of a closed form, not a domain error.
    Anything more negative than that still raises -- the clamp is a rounding guard, not a
    silencer, and `self_test` exercises the raising path via the deliberately-wrong-a1 control."""
    if x < 0:
        if -x < D("1e-45"):
            return D(0)
        raise InvalidOperation("negative radicand")
    return x.sqrt()


def bisect(f, a, b, iters=250):
    """Sign-change bisection.  f(a) and f(b) must straddle (or f(b) may be exactly 0)."""
    fa = f(a)
    for _ in range(iters):
        m = (a + b) / 2
        fm = f(m)
        if (fa <= 0) == (fm <= 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def bracket_root(f, x0, direction=D(1), lo_frac=D("1e-6"), max_span=D(200)):
    """Expanding geometric bracket for a sign change starting at x0."""
    f0 = f(x0)
    step = lo_frac
    while step < max_span:
        x1 = x0 + direction * step
        try:
            f1 = f(x1)
        except (InvalidOperation, ZeroDivisionError):
            return None
        if (f0 <= 0) != (f1 <= 0):
            return (x0, x1) if direction > 0 else (x1, x0)
        step *= 2
    return None


# ======================================================================================
# 1.  BCG's algebra, transcribed once, every coefficient exposed as a named argument.
#     Exposing them is what makes a per-constant ledger possible; nothing is inline.
# ======================================================================================

def R1_radicand(r, g):
    """The radicand of BCG \\eqref{eq:R1}, l.526-528, unrooted so its sign is inspectable."""
    return g**2 * (r - 3)**2 - 2*g*(3*r*r - 6*r + 7) + (9*r*r - 14*r + 9)


def R1(r, g):
    return sqrtD(R1_radicand(r, g))


def R1_roots(g):
    """R_1's radicand is a quadratic in r.  Both roots, in closed form."""
    A = g*g - 6*g + 9
    B = -6*g*g + 12*g - 14
    C = 9*g*g - 14*g + 9
    disc = B*B - 4*A*C
    s = sqrtD(disc)
    return sorted([(-B - s)/(2*A), (-B + s)/(2*A)])


def R2_radicand(r, g, a2=None, a1=None, a0=None, aR1=None):
    """The bracket of BCG \\eqref{eq:def_R2}, l.548-550, with its four groups named:
         a2  coefficient of r^2    -(3g-5)((g-5)g+2)                      [ledger C8]
         a1  coefficient of r       (g(g(18g-52)+50)-8)                   [ledger C9]
         a0  constant               g((76-27g)g-71) + 18                  [ledger C10]
         aR1 the R_1-coupled group  R_1 * (9(g-2)g + ((2-3g)g+5) r + 5)   [ledger C11]
    """
    a2 = -(3*g - 5) * ((g - 5)*g + 2) if a2 is None else a2
    a1 = (g*(g*(18*g - 52) + 50) - 8) if a1 is None else a1
    a0 = (g*((76 - 27*g)*g - 71) + 18) if a0 is None else a0
    if aR1 is None:
        aR1 = R1(r, g) * (9*(g - 2)*g + ((2 - 3*g)*g + 5)*r + 5)
    elif callable(aR1):          # the C11 ledger row perturbs the whole r-dependent group
        aR1 = aR1(r)
    return a2*r*r + a1*r + a0 + aR1


def R2(r, g, scale=None, **kw):
    """BCG \\eqref{eq:def_R2}: R_2 = (1/(g-1)) * ( bracket )^{1/2}.  `scale` is ledger C7."""
    scale = D(1) if scale is None else scale
    return scale * sqrtD(R2_radicand(r, g, **kw)) / (g - 1)


def D_Z1(r, g, c4=None, c_lin=None, **kw):
    """BCG \\eqref{eq:k_asquotientDZ1} denominator, l.600:
         D_{Z,1} = c4 + c_lin*(r-1) + R_2,   BCG's c4 = -4 [C5], c_lin = (1+g)/(g-1) [C6].
       Lemma \\ref{lemma:aux_DZ1_cancellation}, cited at l.605: D_{Z,1} = 0 exactly at r = r*."""
    c4 = D(-4) if c4 is None else c4
    c_lin = (1 + g)/(g - 1) if c_lin is None else c_lin
    return c4 + c_lin*(r - 1) + R2(r, g, **kw)


def k_of_r(r, g):
    """BCG \\eqref{eq:k_asquotientDZ1}, l.600:  k(r) = check-D_{Z,1} / D_{Z,1}."""
    base = D(-4) + (1 + g)/(g - 1)*(r - 1)
    r2 = R2(r, g)
    return (base - r2) / (base + r2)


def k_of_r_float(r, g):
    """The SAME formula in IEEE double.  Diagnostic only -- this is the trap, not a result."""
    gf, rf = float(g), float(r)
    r1 = math.sqrt(gf**2*(rf-3)**2 - 2*gf*(3*rf*rf-6*rf+7) + (9*rf*rf-14*rf+9))
    br = (-(3*gf-5)*((gf-5)*gf+2)*rf*rf + (gf*(gf*(18*gf-52)+50)-8)*rf
          + gf*((76-27*gf)*gf-71) + 18 + r1*(9*(gf-2)*gf + ((2-3*gf)*gf+5)*rf + 5))
    r2 = math.sqrt(br) / (gf - 1.0) if br >= 0 else float("nan")
    base = -4.0 + (1.0+gf)/(gf-1.0)*(rf-1.0)
    return (base - r2) / (base + r2)


# --------------------------------------------------------------------------------------
# 2.  The two endpoints, each solved as a ROOT of a named condition.
# --------------------------------------------------------------------------------------

def dis_exponent(r, g, c_lap=None, c_r=None, c_dens=None, alpha=None):
    """Exponent of BCG's dissipative-forcing prefactor, read off \\eqref{eq:main} l.483:
         e^{(2 - r + (1/alpha)(1-r)) s}   ->   c_lap - c_r*r + c_dens*(1-r)/alpha
       with alpha = (g-1)/2.  delta_dis := -(this); sign condition \\eqref{eq:delta:dis}
       l.489-491.  Ledger constants C1-C4."""
    c_lap = D(2) if c_lap is None else c_lap
    c_r = D(1) if c_r is None else c_r
    c_dens = D(1) if c_dens is None else c_dens
    alpha = (g - 1)/2 if alpha is None else alpha
    return c_lap - c_r*r + c_dens*(1 - r)/alpha


def delta_dis(r, g, **kw):
    return -dis_exponent(r, g, **kw)


def lower_endpoint(g, **kw):
    """Root of dis_exponent = 0.  Solved, not quoted.  T3 checks it against 2g/(g+1)."""
    f = lambda r: dis_exponent(r, g, **kw)
    # Search from well BELOW r = 1.  Unperturbed the root is 7/6 > 1, but the ledger perturbs
    # c_lap / c_r / alpha, and for those the root leaves (1, r*) through the LEFT end.  Starting
    # the bracket at 1+TINY made those families look "unreachable" when in fact the dissipative
    # condition had simply become vacuous on r > 1 -- which is the width-closing regime we are
    # trying to measure.  `window` clamps to max(lo, 1); BCG require r > 1 independently.
    br = bracket_root(f, D("0.01"))
    if br is None:
        raise RuntimeError("no root of the dissipative exponent")
    return bisect(f, br[0], br[1])


def realness_edge(g, **kw):
    """Largest r > 1 for which BOTH radicands stay non-negative, i.e. for which P_s exists as a
    real point and R_2 is real.  This bounds the search domain for r* WITHOUT using
    \\eqref{eq:rstar}.  R_1's edge is closed-form (a quadratic); R_2's is bisected if it bites
    first."""
    roots = [x for x in R1_roots(g) if x > 1]
    edge = min(roots) if roots else D(5)
    f = lambda r: R2_radicand(r, g, **kw)
    if f(edge - TINY) >= 0:
        return edge, "R1"
    br = bracket_root(f, D(1) + D("1e-9"))
    if br is None:
        return edge, "R1"
    return bisect(f, br[0], br[1]), "R2"


def upper_endpoint(g, **kw):
    """Root of D_{Z,1} = 0 in r > 1.

    D_{Z,1}(1) = -4 + 0 + R_2(1) = -4 (R_2(1) = 0, BCG l.603), so it starts strictly negative.
    Search on [1, realness_edge].  If D_{Z,1} has not reached 0 by the edge, the edge itself IS
    the endpoint -- and WHICH of the two happens is measured, not assumed (see
    `structural_findings` in the JSON)."""
    edge, which = realness_edge(g, **{k: v for k, v in kw.items() if k in
                                      ("a2", "a1", "a0", "aR1")})
    f = lambda r: D_Z1(r, g, **kw)
    # DIAGNOSED BUG (leg 305, fixed here): testing the sign of D_{Z,1} AT the realness edge
    # samples the noise floor.  D_{Z,1} vanishes at the edge to ~1e-30 (measured: -1.6E-30 at
    # gamma = 7/5, +2.0E-58 at the gamma-ceiling) because R_1 -> 0 there like a square root, so
    # the sign of f(edge) is arithmetic dust and flips with gamma at the 1e-11 level.  That dust
    # injected a jump discontinuity of +0.0068 into r*(gamma) and trapped the T2 gamma-ceiling
    # bisection at 2.15470053845 instead of 1 + 2/sqrt(3).  Back off from the degenerate point by
    # a fixed relative amount: the square-root behaviour turns a 1e-25 backoff in r into a ~1e-14
    # signal in D_{Z,1}, eleven orders above the dust, while staying far inside every tolerance.
    edge_safe = edge - (edge - 1)*D("1e-25")
    if f(edge_safe) > 0:
        # D_{Z,1} genuinely crosses zero strictly INSIDE the domain: BCG's gamma >= 5/3 branch.
        return bisect(f, D(1) + TINY, edge_safe)
    # D_{Z,1} reaches zero only AT the realness edge: BCG's 1 < gamma < 5/3 branch, where r* is
    # the P_s/P_sbar saddle-node (the R_1 discriminant root), not a D_{Z,1} root interior to the
    # domain.  Which branch holds is MEASURED here, not read off eq:rstar.
    return edge


def r_star_closed_form(g):
    """BCG \\eqref{eq:rstar} l.352-358.  Used in CHECK T4 ONLY, as the cross-check target."""
    if g < D(5)/3:
        return 1 + 2/(1 + sqrtD(2/(g - 1)))**2
    return (3*g - 1)/(2 + sqrtD(D(3))*(g - 1))


def window(g, lower_kw=None, upper_kw=None, lo=None, hi=None):
    lo = lower_endpoint(g, **(lower_kw or {})) if lo is None else lo
    hi = upper_endpoint(g, **(upper_kw or {})) if hi is None else hi
    # BCG's admissible set is r > 1 regardless of delta_dis, so a dissipative threshold that has
    # dropped below 1 does not widen the window past (1, r*).  Clamping here is the physics, and
    # it is what makes the width bounded above by r* - 1 = 0.190983 at gamma = 7/5.
    lo_eff = lo if lo > 1 else D(1)
    return lo, hi, hi - lo_eff


# ======================================================================================
# 3.  CHECKS T1-T6.  T1-T4 failing => gate NO => escalate (pre-registered rule).
# ======================================================================================

def run_checks():
    g = GAMMA_BCG
    out, v = {}, {}

    lo, hi, w = window(g)
    ratio = (lo - 1)/w
    out.update({"lower_endpoint": str(lo), "upper_endpoint": str(hi), "width": str(w),
                "target_window_width": str(lo - 1), "width_ratio": str(ratio)})

    d1, d2 = abs(lo - KNOWN["K1_lower_endpoint"]), abs(hi - KNOWN["K2_upper_endpoint"])
    out["T1_dev_lower"], out["T1_dev_upper"] = str(d1), str(d2)
    v["T1"] = bool(d1 <= TOL["T1_endpoints_vs_leg240"] and d2 <= TOL["T1_endpoints_vs_leg240"])

    f = lambda x: upper_endpoint(x) - lower_endpoint(x)
    ceiling = bisect(f, D("1.7"), D("3.0"))
    out["gamma_ceiling"] = str(ceiling)
    out["gamma_ceiling_closed_form"] = str(1 + 2/sqrtD(D(3)))
    dC = abs(ceiling - KNOWN["K5_gamma_ceiling"])
    out["T2_dev"] = str(dC)
    v["T2"] = bool(dC <= TOL["T2_gamma_ceiling_vs_leg240"])

    cf = {"r_star_=(7-sqrt5)/4": (hi, (7 - sqrtD(D(5)))/4),
          "r_dis_=7/6": (lo, D(7)/6),
          "ratio_=(7+3sqrt5)/2": (ratio, (7 + 3*sqrtD(D(5)))/2),
          "width_=(7-3sqrt5)/12": (w, (7 - 3*sqrtD(D(5)))/12)}
    out["T3"] = {k: {"solved": str(a), "closed_form": str(b), "dev": str(abs(a - b))}
                 for k, (a, b) in cf.items()}
    v["T3"] = all(abs(a - b) <= TOL["T3_closed_forms"] for a, b in cf.values())

    worst, worst_g, n = D(0), None, 0
    for i in range(1, 40):
        gi = D("1.05") + i*D("0.05")
        if gi >= D(5)/3:
            continue
        n += 1
        d = abs(upper_endpoint(gi) - r_star_closed_form(gi))
        if d > worst:
            worst, worst_g = d, gi
    out["T4_max_dev"], out["T4_worst_gamma"], out["T4_n_gammas"] = str(worst), str(worst_g), n
    v["T4"] = bool(worst <= TOL["T4_rootsolve_vs_closed_form"])

    # ---- T5: the conditioning trap.  Float EXPECTED to fail; 60 digits REQUIRED to pass.
    k1_hi = k_of_r(D(1), g)   # BCG l.603 asserts R_2 = 0 AT r = 1 exactly.  Probing at
    # 1 + 1e-45 instead measured MY OFFSET, not BCG: the radicand vanishes linearly, so the
    # square root halves the exponent and returns 1.095e-22 of my own perturbation.  The honest
    # test of l.603 is at r = 1 itself, where the 60-digit radicand is 0.000 exactly.
    k1_fl = k_of_r_float(1.0, g)
    dev_hi, dev_fl = abs(k1_hi - 1), abs(k1_fl - 1.0)
    with localcontext() as ctx:
        ctx.prec = 60
        rad_hi = R2_radicand(D(1), g)
    gf = float(g)
    r1f = math.sqrt(gf**2*4 - 2*gf*4 + 4)
    rad_fl = (-(3*gf-5)*((gf-5)*gf+2) + (gf*(gf*(18*gf-52)+50)-8) + gf*((76-27*gf)*gf-71)
              + 18 + r1f*(9*(gf-2)*gf + ((2-3*gf)*gf+5) + 5))
    out["conditioning_trap"] = {
        "k_of_1_highprec_dev": str(dev_hi), "k_of_1_float_dev": repr(dev_fl),
        "R2_radicand_at_r1_highprec": str(rad_hi), "R2_radicand_at_r1_float": repr(rad_fl),
        "largest_term_magnitude_in_radicand": str(abs(g*((76 - 27*g)*g - 71))),
        "float_fails_1e-9": bool(dev_fl > TOL["T5_k_of_1_float_expected_to_fail_at"]),
        "highprec_passes_1e-40": bool(dev_hi <= TOL["T5_k_of_1_highprec"]),
        "leg302_measured": "1.29e-07",
        "note": ("BCG l.603: R_2 = 0 at r = 1 exactly.  The float number is DIAGNOSTIC ONLY, "
                 "decides nothing, and is a property of IEEE double, not of BCG's argument.")}
    v["T5_highprec"] = bool(dev_hi <= TOL["T5_k_of_1_highprec"])
    v["T5_float_fails_as_predicted"] = bool(dev_fl > TOL["T5_k_of_1_float_expected_to_fail_at"])

    out["delta_dis_max_over_window"] = str(delta_dis(hi, g))
    out["K3_width_agrees_at_3sf"] = bool(abs(w - KNOWN["K3_width"]) < D("5e-5"))
    out["K4_delta_dis_max_dev"] = str(abs(delta_dis(hi, g) - KNOWN["K4_delta_dis_max"]))
    return out, v, lo, hi, w


# ======================================================================================
# 4.  THE LEDGER.  Eleven constants, each a named symbol in a displayed BCG equation.
# ======================================================================================

LEDGER_SPEC = [
    ("C1_c_lap",   "lower", "c_lap",  lambda g: D(2),
     "eq:main l.483", "the Laplacian's own scaling weight (two spatial derivatives)"),
    ("C2_c_r",     "lower", "c_r",    lambda g: D(1),
     "eq:main l.483", "coefficient of r in the prefactor exponent"),
    ("C3_c_dens",  "lower", "c_dens", lambda g: D(1),
     "eq:main l.483", "multiplier on (1/alpha)(1-r): power of S^{1/alpha} dividing the Laplacian"),
    ("C4_alpha",   "lower", "alpha",  lambda g: (g - 1)/2,
     "eq:main l.483 (alpha = (gamma-1)/2)", "the ideal-gas exponent"),
    ("C5_c4",      "upper", "c4",     lambda g: D(-4),
     "eq:k_asquotientDZ1 l.600", "the constant -4 in D_{Z,1}"),
    ("C6_c_lin",   "upper", "c_lin",  lambda g: (1 + g)/(g - 1),
     "eq:k_asquotientDZ1 l.600", "the linear-in-r coefficient (1+gamma)/(gamma-1) in D_{Z,1}"),
    ("C7_R2scale", "upper", "scale",  lambda g: D(1),
     "eq:def_R2 l.547-551", "overall scale of R_2"),
    ("C8_a2",      "upper", "a2",     lambda g: -(3*g - 5)*((g - 5)*g + 2),
     "eq:def_R2 l.548", "radicand r^2 coefficient"),
    ("C9_a1",      "upper", "a1",     lambda g: (g*(g*(18*g - 52) + 50) - 8),
     "eq:def_R2 l.548-549", "radicand r coefficient"),
    ("C10_a0",     "upper", "a0",     lambda g: (g*((76 - 27*g)*g - 71) + 18),
     "eq:def_R2 l.548,550", "radicand constant term"),
    ("C11_aR1",    "upper", "aR1",    None,
     "eq:def_R2 l.550", "the R_1-coupled group R_1*(9(g-2)g + ((2-3g)g+5)r + 5)"),
]

# Every constant's class, argued term by term in the TECHNICAL prose and recorded here.
CONST_CLASS = {n: "EXACT_IDENTITY" for n, *_ in LEDGER_SPEC}


def width_with(g, name, kind, arg, valf, factor, lo0, hi0):
    """Recompute the window with exactly ONE constant multiplied by `factor`.

    Only the endpoint the constant can actually move is recomputed -- the other is passed in.
    That is the single change that took this runner from hours to seconds."""
    if kind == "lower":
        return window(g, lower_kw={arg: valf(g)*factor}, hi=hi0)[2]
    if name == "C11_aR1":
        grp = lambda r: (R1(r, g)*(9*(g - 2)*g + ((2 - 3*g)*g + 5)*r + 5))*factor
        return window(g, upper_kw={"aR1": grp}, lo=lo0)[2]
    return window(g, upper_kw={arg: valf(g)*factor}, lo=lo0)[2]


def _wrap_aR1(kw, g):
    """R2_radicand/D_Z1 accept aR1 either as a value or as a callable of r."""
    return kw


def move_to_close(g, name, kind, arg, valf, target_w, lo0, hi0):
    """Smallest |relative move| in this constant that widens the window to target_w.

    Expanding geometric bracket then bisection -- no linear scan.  Returns None
    ('unreachable') if the one-parameter family never attains target_w, which is itself a
    finding and not a failure."""
    def W(factor):
        try:
            return width_with(g, name, kind, arg, valf, factor, lo0, hi0)
        except (InvalidOperation, ZeroDivisionError, RuntimeError, ValueError):
            return None

    best = None
    for sign in (D(1), D(-1)):
        step, prev_f, hit = D("1e-4"), D(1), None
        while step < D(200):
            f = 1 + sign*step
            if f <= 0:
                # DIAGNOSED BUG (leg 305, fixed here): for a DOWNWARD move the additive
                # geometric bracket 1 - step marches straight through zero and used to give up,
                # reporting C4_alpha "unreachable" when its true move is finite.  Once the
                # additive ladder would go non-positive, switch to a MULTIPLICATIVE ladder that
                # approaches zero from above and can never overshoot the domain.
                f = prev_f / 2
                if f < D("1e-12"):
                    break
                val = W(f)
                if val is not None and val >= target_w:
                    hit = (prev_f, f)
                    break
                if val is None:
                    break
                prev_f = f
                continue
            val = W(f)
            if val is None:
                # DIAGNOSED BUG (leg 305, fixed here): the geometric bracket doubles straight
                # out of the constant's valid domain and used to give up, reporting "unreachable"
                # for C1/C2/C4 whose true moves are finite.  Instead, bisect IN to the validity
                # edge and ask whether target_w is attained before it.
                a, b = prev_f, f            # a valid, b invalid
                for _ in range(200):
                    m = (a + b)/2
                    if W(m) is None:
                        b = m
                    else:
                        a = m
                va = W(a)
                if va is not None and va >= target_w:
                    hit = (prev_f, a)
                break
            if val >= target_w:
                hit = (prev_f, f)
                break
            prev_f, step = f, step*2
        if hit is None:
            continue
        a, b = (hit[0], hit[1]) if sign > 0 else (hit[1], hit[0])
        for _ in range(120):
            m = (a + b)/2
            val = W(m)
            if val is None:
                break
            if (val >= target_w) == (sign > 0):
                b = m
            else:
                a = m
        rel = (a + b)/2 - 1
        if best is None or abs(rel) < abs(best):
            best = rel
    return best


def build_ledger(g, lo0, hi0, w0):
    target_w = lo0 - 1
    rows = []
    for name, kind, arg, valf, loc, meaning in LEDGER_SPEC:
        vf = valf if valf is not None else (lambda gg: D(1))
        wp = width_with(g, name, kind, arg, vf, 1 + EPS_SENS, lo0, hi0)
        wm = width_with(g, name, kind, arg, vf, 1 - EPS_SENS, lo0, hi0)
        m1 = (wp - wm)/(2*EPS_SENS)
        wp2 = width_with(g, name, kind, arg, vf, 1 + EPS_SENS_2, lo0, hi0)
        wm2 = width_with(g, name, kind, arg, vf, 1 - EPS_SENS_2, lo0, hi0)
        m1b = (wp2 - wm2)/(2*EPS_SENS_2)
        lin = abs(m1 - m1b)/abs(m1) if m1 != 0 else abs(m1 - m1b)
        m2 = width_with(g, name, kind, arg, vf, D("1.01"), lo0, hi0) - w0
        m3 = move_to_close(g, name, kind, arg, vf, target_w, lo0, hi0)

        # ONE-SIDED derivatives and the cusp diagnosis.  The central difference above is
        # meaningless for every constant living in D_{Z,1}/R_2, because at gamma = 7/5 the upper
        # endpoint is PINNED to the R_1 discriminant root (the P_s / bar-P_s saddle-node): those
        # constants can only LOWER r*, never raise it, so r* sits at a maximum of each of those
        # one-parameter families and the two sides are not comparable.  MEASURED consequence
        # (scaling_exponent_dn / _up below, ~2.00 for every capped row): because D_{Z,1} meets
        # zero at the edge with a VERTICAL tangent (R_1 ~ sqrt(edge - r)), an O(eps) perturbation
        # of any D_{Z,1}/R_2 constant moves the endpoint only by O(eps^2).  So the central
        # difference is itself O(eps), and halving eps halves it: the T6 relative deviation is
        # then exactly 0.9, which is what is measured (0.8991-0.8999) for all seven capped rows.
        # T6 fails on those rows because BCG's constants sit at a STATIONARY MAXIMUM of r*, not
        # because the arithmetic is wrong -- T6b, the same test on the uncapped rows, passes at
        # ~9e-15.  Diagnosed before believed, per leg 302's lesson.
        d_up, d_dn = wp - w0, wm - w0
        d_up2, d_dn2 = wp2 - w0, wm2 - w0
        capped = (d_up <= 0) and (d_dn <= 0)

        def _exponent(da, db):
            if da == 0 or db == 0:
                return None
            ra, rb = abs(da), abs(db)
            return D(str(math.log(float(ra)/float(rb)) / math.log(float(EPS_SENS/EPS_SENS_2))))

        p_up, p_dn = _exponent(d_up, d_up2), _exponent(d_dn, d_dn2)
        rows.append({"constant": name, "locator": loc, "meaning": meaning,
                     "bcg_value": (str(valf(g)) if valf else "r-dependent group"),
                     "M1_dW_dlnc": str(m1), "M1_linearity_rel_dev": str(lin),
                     "M1_one_sided_up": str(d_up/EPS_SENS),
                     "M1_one_sided_dn": str(-d_dn/EPS_SENS),
                     "capped_r_star_at_a_maximum": bool(capped),
                     "scaling_exponent_up": (str(p_up) if p_up is not None else "flat"),
                     "scaling_exponent_dn": (str(p_dn) if p_dn is not None else "flat"),
                     "M2_width_credit_1pct": str(m2),
                     "M2_pct_of_window_per_1pct": str(m2/w0*100),
                     "M3_move_to_close": (str(m3) if m3 is not None else "unreachable"),
                     "M3_move_to_close_pct": (str(m3*100) if m3 is not None else "unreachable"),
                     "M4_class": CONST_CLASS[name]})
    return rows, target_w


# ======================================================================================
# 5.  The DISCRETE sub-ledger: BCG's admissible speeds are not an interval.
# ======================================================================================

def discrete_ledger(g, lo, hi):
    """Lemma \\ref{lemma:k} (l.583): k : [1, r*) -> [1, +inf) is a bijection, and BCG's profiles
    live at r_n := k^{-1}(n) for odd n >= 3 (l.367-369).  So the width deficit has a COUNTING
    form: how many admissible speeds does the dominance condition cost?"""
    k_thr = k_of_r(lo, g)
    n_lost = int(k_thr)
    odd_lost = [n for n in range(3, n_lost + 1, 2)]
    first_ok = next(n for n in range(3, n_lost + 40, 2) if D(n) > k_thr)
    r_n = {}
    for n in odd_lost + [first_ok]:
        fn = lambda r: k_of_r(r, g) - n
        r_n[str(n)] = str(bisect(fn, D(1) + D("1e-30"), hi - D("1e-30")))
    return {"k_at_dominance_threshold": str(k_thr), "n_lost_floor": n_lost,
            "odd_speeds_lost": odd_lost, "n_odd_speeds_lost": len(odd_lost),
            "first_admissible_odd_speed_for_NS": first_ok, "r_n_values": r_n,
            "note": ("BCG use odd n >= 3 (l.367-369).  Every r_n at or below the dominance "
                     "threshold is a profile the EULER theorem has and the NAVIER-STOKES "
                     "theorem cannot use.")}


# ======================================================================================
# 6.  Controls that can come out differently (lesson 90).
# ======================================================================================

def self_test(g, hi):
    t = {}
    t["R1_at_r1_equals_2(g-1)"] = bool(abs(R1(D(1), g) - 2*(g - 1)) < D("1e-50"))
    t["R2_at_r1_is_zero"] = bool(abs(R2_radicand(D(1), g)) < D("1e-50"))
    bad = abs(upper_endpoint(g, a1=(g*(g*(18*g - 52) + 50) - 8)*D("1.001"))
              - r_star_closed_form(g))
    t["deliberately_wrong_a1_breaks_T4"] = bool(bad > TOL["T4_rootsolve_vs_closed_form"])
    t["deliberately_wrong_a1_dev"] = str(bad)
    lo = lower_endpoint(g)
    xs = [lo + (hi - lo)*D(i)/20 for i in range(1, 20)]
    ks = [k_of_r(x, g) for x in xs]
    t["k_strictly_increasing_on_window"] = all(ks[i] < ks[i+1] for i in range(len(ks)-1))
    t["k_at_r1_is_1"] = bool(abs(k_of_r(D(1), g) - 1) < D("1e-40"))
    return t


def main():
    t0 = time.time()
    g = GAMMA_BCG
    checks, verdicts, lo, hi, w0 = run_checks()
    rows, target_w = build_ledger(g, lo, hi, w0)
    disc = discrete_ledger(g, lo, hi)
    tests = self_test(g, hi)

    finite = [r for r in rows if r["M3_move_to_close"] != "unreachable"]
    costliest = min(finite, key=lambda r: abs(D(r["M3_move_to_close"]))) if finite else None
    # T6 verbatim as pre-registered.  It is NOT restricted after the fact and NOT a gate trigger.
    verdicts["T6"] = all(D(r["M1_linearity_rel_dev"]) <= TOL["T6_elasticity_linearity_rel"]
                         for r in rows)
    # T6b is an ADDITIONAL check, declared as additional: the same linearity test restricted to
    # the constants whose family is not pinned at the saddle-node.  T6 failing while T6b passes
    # is the signature of a square-root cusp rather than of broken arithmetic.
    uncapped = [r for r in rows if not r["capped_r_star_at_a_maximum"]]
    verdicts["T6b_uncapped_only"] = bool(uncapped) and all(
        D(r["M1_linearity_rel_dev"]) <= TOL["T6_elasticity_linearity_rel"] for r in uncapped)

    reproduced = all(verdicts[k] for k in ("T1", "T2", "T3", "T4"))
    gate = "YES" if (reproduced and costliest is not None) else "NO"

    slack = any(r["M4_class"] == "ESTIMATE" and r["M3_move_to_close"] != "unreachable"
                and D("0.5") <= abs(D(r["M3_move_to_close"])) <= D(2) for r in rows)
    verdict_sharp = "SLACK" if slack else "SHARP_FOR_BCG_ARGUMENT_AS_STATED"

    edge, which = realness_edge(g)
    payload = {
        "leg": 305, "route": "DWM", "date": "2026-08-11", "figure": "fig82",
        "source": {"arxiv": "arXiv:2208.09445",
                   "eprint_tar_md5": "45ea63c45a1a199ecfb4dc4a15431600",
                   "tex": "RadialImplosion31_FinalArxiv.tex",
                   "journal": "Forum of Mathematics Pi 13 e6 (2025)"},
        "gate_wording": ("Does the re-derivation reproduce the window endpoints and yield a "
                         "per-constant width ledger naming the costliest constant?"),
        "gate": gate,
        "gamma": str(g), "precision_decimal_digits": getcontext().prec,
        "known_answers_reference_only_not_this_legs_claims":
            {k: str(v) for k, v in KNOWN.items()},
        "checks": checks, "verdicts": verdicts,
        "tolerances": {k: str(v) for k, v in TOL.items()},
        "ledger": rows,
        "costliest_constant": costliest,
        "sharp_or_slack": verdict_sharp,
        # The counterfactual, banked so that no downstream prose or figure ever retypes it.
        # c_lap is the Laplacian's own scaling weight = 2 spatial derivatives.  Moving it is not
        # a sharper estimate: it is a DIFFERENT operator.  c_lap = 2s corresponds to nu(-Lap)^s.
        "counterfactual": ({
            "c_lap_before": "2",
            "c_lap_after": str(D(2)*(1 + D(costliest["M3_move_to_close"]))),
            "fractional_order_s": str(D(2)*(1 + D(costliest["M3_move_to_close"]))/2),
            "lower_endpoint_after": str(lower_endpoint(
                g, c_lap=D(2)*(1 + D(costliest["M3_move_to_close"])))),
            "closed_form_c_lap_star": str((9 - 3*sqrtD(D(5)))/2),
            "closed_form_s_star": str((9 - 3*sqrtD(D(5)))/4),
            "meaning": ("closing the 6.854x deficit requires replacing nu*Laplacian with the "
                        "HYPODISSIPATION nu(-Laplacian)^s, s < 1.  That is a different PDE, not "
                        "a sharper proof of the same one."),
        } if costliest and costliest["constant"] == "C1_c_lap" else {}),
        "discrete_ledger": disc,
        "self_test": tests,
        "structural_findings": {
            "realness_edge": str(edge), "realness_edge_set_by": which,
            "R1_radicand_at_r_star": str(R1_radicand(hi, g)),
            "r_star_is_a_root_of_R1_radicand": bool(abs(R1_radicand(hi, g)) < D("1e-50")),
            "R1_radicand_roots_at_gamma_7_5": [str(x) for x in R1_roots(g)],
            "D_Z1_at_realness_edge": str(D_Z1(edge, g)),
            "interpretation": (
                "r* is exactly the smaller root of BCG's R_1 radicand, i.e. exactly where the "
                "two stationary points P_s and bar-P_s of \\eqref{eq:Ps}/\\eqref{eq:Psbar} "
                "MERGE.  The upper endpoint is a saddle-node bifurcation of BCG's phase "
                "portrait, not an estimate -- which is why no constant in D_{Z,1} or R_2 can "
                "move it."),
            "closed_form_c_lap_that_would_close_the_deficit": str((9 - 3*sqrtD(D(5)))/2),
            "equivalent_fractional_dissipation_order_s": str((9 - 3*sqrtD(D(5)))/4),
            "meaning": ("c_lap = 2 counts the derivatives of the Laplacian.  Closing the "
                        "deficit by moving it means replacing nu*Delta with the hypodissipation "
                        "nu*(-Delta)^s at s = (9-3sqrt5)/4 -- a different PDE, not a sharper "
                        "proof of the same one."),
        },
        "walls": {
            "wall1_wall2": ("stand; measuring the shape of an obligation is not discharging it"),
            "system": ("3D COMPRESSIBLE Navier-Stokes (BCG, gamma = 7/5) -- NOT the "
                       "incompressible system the Clay problem asks about"),
            "clay_odds": "~0.05%, unchanged",
            "chain": "no link of the L1->L4 chain moved"},
        "runtime_s": None}
    payload["runtime_s"] = round(time.time() - t0, 2)

    dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "writeup", "data", "p2_route_dwm_v1.json")
    with open(dest, "w") as fh:
        json.dump(payload, fh, indent=2)

    p = lambda x, n=10: str(+D(x).quantize(D(1).scaleb(-n))) if x is not None else "-"
    print("=" * 92)
    print("LEG 305 -- ROUTE-DWM: per-constant width ledger of BCG's r-dominance argument")
    print("=" * 92)
    print("window           (%s, %s)" % (p(lo, 10), p(hi, 10)))
    print("width            %s      target (1,7/6] width %s" % (p(w0, 10), p(target_w, 10)))
    print("ratio            %s   vs leg 300's closed form (7+3sqrt5)/2" % p(checks["width_ratio"], 10))
    print("-" * 92)
    for k in ("T1", "T2", "T3", "T4", "T5_highprec", "T5_float_fails_as_predicted", "T6", "T6b_uncapped_only"):
        print("  %-32s %s" % (k, verdicts[k]))
    ct = checks["conditioning_trap"]
    print("  conditioning trap  float |k(1)-1| = %s   (leg 302: %s)"
          % (ct["k_of_1_float_dev"], ct["leg302_measured"]))
    print("                     60-digit |k(1)-1| = %s" % ct["k_of_1_highprec_dev"])
    print("-" * 92)
    print("%-12s %-13s %-13s %-11s %-16s %s"
          % ("constant", "BCG value", "dW/dlnc", "%win per 1%", "move_to_close", "class"))
    for r in rows:
        try:
            val = p(r["bcg_value"], 4)
        except Exception:
            val = "grp(r)"
        m3 = r["M3_move_to_close_pct"]
        m3s = "unreachable" if m3 == "unreachable" else p(m3, 2) + "%"
        print("%-12s %-13s %-13s %-11s %-16s %s"
              % (r["constant"], val, p(r["M1_dW_dlnc"], 6),
                 p(r["M2_pct_of_window_per_1pct"], 3), m3s, r["M4_class"]))
    print("-" * 92)
    print("COSTLIEST CONSTANT : %s  (%s)"
          % (costliest["constant"] if costliest else "none",
             costliest["meaning"] if costliest else ""))
    print("SHARP OR SLACK     : %s" % verdict_sharp)
    print("r* structural      : R_1 radicand at r* = %s  -> saddle-node of P_s / bar-P_s"
          % payload["structural_findings"]["R1_radicand_at_r_star"])
    print("discrete ledger    : k(threshold) = %s -> %d speeds lost, %d odd (%s); NS starts n=%d"
          % (p(disc["k_at_dominance_threshold"], 6), disc["n_lost_floor"],
             disc["n_odd_speeds_lost"], disc["odd_speeds_lost"],
             disc["first_admissible_odd_speed_for_NS"]))
    print("self-test          : %s" % tests)
    print("GATE: %s    runtime %.2f s" % (gate, payload["runtime_s"]))
    print("Walls 1 and 2 stand. 3D COMPRESSIBLE NS, not Clay's incompressible system. "
          "Clay ~0.05%, unchanged.")
    return payload


if __name__ == "__main__":
    main()
