"""Route-NLH (leg 331) -- does Breden-Chu's machinery hold a NONLOCAL operator?

THE GATE (pre-committed, DIRECTION.md cycle-7b, and writeup/novelty/leg_331.md sec 5)

    Does bc_weighted_sobolev.py's machinery, pointed at a named nonlocal operator on its
    own weighted space, produce finite, closing bounds of the same kind it produces for
    the local operators it was built on -- magnitudes, not booleans, realization named?

THE OBJECT: ONE LETTER CHANGED
-----------------------------------------------------------------------------
Breden-Chu eq. (54) is      L u - u/4 + u^2 d_x u = 0     (Neumann at 0, even sector)
this leg's object is        L u - u/4 + u^2 Lam^{2a} u = 0,   Lam^{2a} = (-Delta)^a

with a = 1/2 giving Lam = H d_x, the HILBERT-TRANSFORM realization the gate names first.
The local original is therefore the CONTROL, and it runs through the IDENTICAL code path
with nonlocality as the single varied ingredient (lesson 90: the control can come out
differently, and does -- see the M1 table).

THE PRIMITIVE, AND WHY IT NEEDS NO NEW SPECIAL-FUNCTION CODE
-----------------------------------------------------------------------------
psi_m(x) = L_m^{(-1/2)}(x^2/4) e^{-x^2/4} / Zeta_m = kappa_m H_{2m}(x/2) e^{-x^2/4},
using L_m^{(-1/2)}(s^2) = (-1)^m H_{2m}(s)/(2^{2m} m!).  The Fourier transform of
H_n(x/2)e^{-x^2/4} is obtained from the generating function e^{2zt-t^2} in one line:

    Int e^{2(x/2)t - t^2} e^{-x^2/4} e^{-i xi x} dx = 2 sqrt(pi) e^{-xi^2} e^{-2 i t xi}

and matching powers of t gives a MONOMIAL, not a Hermite polynomial:

    FT[ H_n(x/2) e^{-x^2/4} ](xi)  =  2 sqrt(pi) (-i)^n (2 xi)^n e^{-xi^2}.

(The tempting identity FT[H_n e^{-y^2}] ~ H_n is FALSE: H_n(y)e^{-y^2} is not a Hermite
FUNCTION -- those carry e^{-y^2/2}.  Using it makes m = 0 come out exactly right and every
m >= 1 come out ~100% wrong, which is precisely what the a = 0 known-answer gate below
caught before a single nonlocal number was quoted.)

Hence the exact representation this module is built on:

    Lam^{2a} psi_m (x)  =  ( 2 / (sqrt(pi) m! Zeta_m) )  Int_0^inf  xi^{2m+2a} e^{-xi^2} cos(xi x) dxi

a pure monomial-times-Gaussian cosine integral, evaluated in LOGS so that the prefactor
1/(m! Zeta_m) (~e^{-187} at m = 60) and the integrand peak (~e^{+186} at m = 60) are never
formed separately.  Nothing about the basis is rebuilt.

THE TAIL THIS FORCES.  The symbol is |xi|^{2a} xi^{2m} e^{-xi^2}: the only non-smoothness
at xi = 0 is |xi|^{2a}, and it is multiplied by a factor vanishing to order 2m, so

    Lam^{2a} psi_m (x)  ~  C_m  x^{-(1 + 2a + 2m)}     as x -> infinity,

ALGEBRAIC for every m and every a > 0, against a local control d_x psi_m that decays like
e^{-x^2/4}.  That contrast is what M1 measures.

TWO KNOWN-ANSWER GATES ON THAT PRIMITIVE (lesson 84 -- a probe has a WINDOW)
    a = 0   ->  Lam^0 psi_m must equal psi_m       (self-duality of the transform)
    a = 1   ->  Lam^2 psi_m must equal -d_xx psi_m (computed from L psi_m = lam_m psi_m,
                i.e. -psi_m'' = lam_m psi_m + (x/2) psi_m')
Both are checked before any nonlocal number is quoted.  A third, independent instrument
-- solver/line_hilbert.py, validated on the CLM known-answer pair -- cross-checks a = 1/2.

HOW EACH BREDEN-CHU BOUND IS GRADED (the honest ceiling, stated before the numbers)
-----------------------------------------------------------------------------
  DERIVATION-FREE  the published formula is a COMPUTATION on the operator (a norm, a
                   projection, a matrix inverse).  Substituting Lam for d_x changes what
                   is computed, not why the formula is valid.  Y, Zbar11, Zbar21 are here.
  TRANSCRIBED      the published formula's DERIVATION used locality (a pointwise product
                   rule, an integration by parts, or a half-power bound ||d_x L^{-1}||
                   <= lam_{n+1}^{-1/2}).  Substituting Lam gives a number, but this leg
                   has NOT re-derived the inequality behind it.  Zbar12, Zbar22, Z2, Z3
                   are here, and every statement resting on them says so.

ARITHMETIC MODEL.  float64 throughout, with decimal.Decimal used only where a stability
check demands it.  NOT interval arithmetic.  Nothing here is a rigorous enclosure and
nothing here may be cited as one.  This inherits leg 256's ceiling verbatim.
"""

import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import bc_weighted_sobolev as bc          # noqa: E402
from solver import line_hilbert                        # noqa: E402


OUT_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "writeup", "data", "p2_route_nlh_v1.json")


# ===========================================================================
# 0.  Gauss-Legendre panels (no scipy) -- the one general-purpose integrator
# ===========================================================================

def _gauss_legendre_nodes(k):
    """k-point Gauss-Legendre nodes/weights on [-1,1] via the Golub-Welsch matrix."""
    i = np.arange(1, k, dtype=float)
    b = i / np.sqrt(4.0 * i * i - 1.0)
    J = np.diag(b, -1) + np.diag(b, 1)
    x, V = np.linalg.eigh(J)
    return x, 2.0 * V[0, :] ** 2


def panel_rule(a, b, n_panel, k=12):
    """Composite k-point Gauss-Legendre rule on [a,b] with n_panel equal panels."""
    gx, gw = _gauss_legendre_nodes(k)
    edges = np.linspace(a, b, n_panel + 1)
    lo, hi = edges[:-1, None], edges[1:, None]
    half = 0.5 * (hi - lo)
    nodes = (0.5 * (lo + hi) + half * gx[None, :]).ravel()
    weights = (half * gw[None, :]).ravel()
    return nodes, weights


# ===========================================================================
# 1.  THE NONLOCAL PRIMITIVE:  Lam^{2a} psi_m, exactly, on the existing basis
# ===========================================================================

class FractionalBasisImages:
    """Lam^{2a} psi_m evaluated at arbitrary x, for m = 0..n, by the cosine integral.

        Lam^{2a} psi_m (x) = (2/(sqrt(pi) m! Zeta_m)) Int_0^inf xi^{2m+2a} e^{-xi^2} cos(xi x) dxi

    The xi-grid must resolve cos(xi * x_max), so its panel count is driven by x_max; the
    integrand's own support is set by xi^{2m+2a}e^{-xi^2}, which peaks at sqrt(m+a).
    """

    def __init__(self, n, alpha, x_max, panels_per_unit=None, k=12, xi_max=None):
        self.n, self.alpha, self.x_max = n, float(alpha), float(x_max)
        if xi_max is None:
            # integrand xi^{2m+2a} e^{-xi^2} peaks at sqrt(m+a) and dies well before this
            xi_max = math.sqrt(n + 1.0) + 9.0
        self.xi_max = xi_max
        if panels_per_unit is None:
            # >= 8 panels per oscillation of cos(xi x_max) at the worst x
            panels_per_unit = max(6.0, 4.0 * self.x_max / math.pi)
        n_panel = int(math.ceil(panels_per_unit * xi_max))
        self.n_panel, self.k = n_panel, k
        xi, w = panel_rule(0.0, xi_max, n_panel, k)
        self.xi, self.w = xi, w
        m = np.arange(n + 1, dtype=float)
        lg = np.vectorize(math.lgamma, otypes=[float])
        # log( 2 / (sqrt(pi) m! Zeta_m) )
        log_pref = math.log(2.0) - 0.5 * math.log(math.pi) - lg(m + 1.0) - bc.log_zeta(n)
        log_xi = np.log(xi)
        # amp[q, m] = w_q exp( log_pref_m + (2m+2a) log xi_q - xi_q^2 ), formed in logs
        expo = (log_pref[None, :] + np.outer(log_xi, 2.0 * m + 2.0 * self.alpha)
                - (xi * xi)[:, None])
        self.amp = w[:, None] * np.exp(expo)
        self.log_amp_peak = float(np.max(expo))

    def at(self, x, block=4096):
        """(len(x), n+1) array of Lam^{2a} psi_m(x). Blocked to bound memory."""
        x = np.asarray(x, dtype=float)
        out = np.empty((x.size, self.n + 1))
        for s in range(0, x.size, block):
            xb = x[s:s + block]
            C = np.cos(np.outer(xb, self.xi))                   # (b, Q)
            out[s:s + block, :] = C @ self.amp
        return out

    def apply(self, a, x, block=8192):
        """Lam^{2a} (sum_m a_m psi_m)(x), contracting in xi FIRST.

        Identical to `self.at(x) @ a` but costs O(len(x) * Q) instead of
        O(len(x) * Q * n): the a-contraction is done on the amplitudes, where it is
        exact and free, so a fine reference x-grid is affordable at large n.
        """
        v = self.amp @ np.asarray(a, dtype=float)               # (Q,)
        x = np.asarray(x, dtype=float)
        out = np.empty(x.size)
        for s in range(0, x.size, block):
            out[s:s + block] = np.cos(np.outer(x[s:s + block], self.xi)) @ v
        return out


# -- the two known-answer gates on that primitive ---------------------------

def gate_alpha_zero(n=12, x_max=14.0):
    """Lam^0 psi_m must reproduce psi_m exactly.  Returns the max relative defect."""
    x = np.linspace(0.05, x_max, 400)
    got = FractionalBasisImages(n, 0.0, x_max).at(x)
    want, _ = bc.psi_values(n, x)
    scale = np.max(np.abs(want), axis=0)
    return {"n": n, "x_max": x_max,
            "max_abs_defect": float(np.max(np.abs(got - want))),
            "max_rel_defect": float(np.max(np.abs(got - want) / scale[None, :]))}


def gate_alpha_one(n=12, x_max=14.0):
    """Lam^2 psi_m must equal -d_xx psi_m = lam_m psi_m + (x/2) d_x psi_m."""
    x = np.linspace(0.05, x_max, 400)
    got = FractionalBasisImages(n, 1.0, x_max).at(x)
    P, D = bc.psi_values(n, x)
    want = bc.eigenvalues(n)[None, :] * P + (x[:, None] / 2.0) * D
    scale = np.max(np.abs(want), axis=0)
    return {"n": n, "x_max": x_max,
            "max_abs_defect": float(np.max(np.abs(got - want))),
            "max_rel_defect": float(np.max(np.abs(got - want) / scale[None, :]))}


def gate_line_hilbert_cross_check(n=6, x_max=10.0, grid=2401, span=60.0):
    """Independent instrument: Lam psi_m = H(d_x psi_m) via solver/line_hilbert.py.

    line_hilbert is validated on the CLM known-answer pair; it is a spline-analytic
    whole-line transform on a truncated domain, so it carries its own truncation error.
    Agreement to a few digits is what this cross-check can deliver, and that is enough
    to rule out a wrong constant or a wrong sign in the cosine-integral route.
    """
    xs = np.linspace(-span, span, grid)
    _, D = bc.psi_values(n, xs)
    x_eval = np.linspace(0.5, x_max, 40)
    mine = FractionalBasisImages(n, 0.5, span).at(x_eval)
    rows = []
    for m in range(n + 1):
        Hd = line_hilbert.line_hilbert(xs, D[:, m])
        ref = np.interp(x_eval, xs, Hd)
        denom = max(float(np.max(np.abs(ref))), 1e-300)
        rows.append({"m": m,
                     "max_abs_diff": float(np.max(np.abs(mine[:, m] - ref))),
                     "rel_to_peak": float(np.max(np.abs(mine[:, m] - ref)) / denom)})
    return {"n": n, "span": span, "grid": grid, "per_mode": rows,
            "worst_rel_to_peak": max(r["rel_to_peak"] for r in rows)}


# ===========================================================================
# 2.  M1 -- DOES THE NONLOCAL IMAGE STAY IN THE SPACE?
# ===========================================================================

def m1_truncated_weighted_norms(n_modes, alpha, radii, panels=900, k=12):
    """||Op psi_m||^2 over |x| < R in L^2(mu), mu = e^{x^2/4}, for a ladder of R.

    Nonlocal Op = Lam^{2a}; local CONTROL Op = d_x, on the SAME integrator, and the
    control's own exact value is known (||d_x psi_m||^2_{L^2(mu)} is finite), so the
    control can and does come out differently.
    """
    Rmax = float(max(radii))
    img = FractionalBasisImages(n_modes, alpha, Rmax)
    out = {"alpha": alpha, "radii": [float(r) for r in radii], "modes": {}}
    for m in range(n_modes + 1):
        nl, loc = [], []
        for R in radii:
            x, w = panel_rule(0.0, float(R), panels, k)
            wt = np.exp(x * x / 4.0)
            f = img.at(x)[:, m]
            _, D = bc.psi_values(n_modes, x)
            nl.append(float(2.0 * np.sum(w * wt * f * f)))
            loc.append(float(2.0 * np.sum(w * wt * D[:, m] ** 2)))
        out["modes"][str(m)] = {"nonlocal_sq": nl, "local_control_sq": loc}
    return out


def m1_tail_exponent(alpha, m=0, xs=(20.0, 30.0, 40.0, 60.0)):
    """The measured algebraic decay exponent of Lam^{2a} psi_m at large x.

    The Fourier symbol |xi|^{2a} xi^{2m} e^{-xi^2} is non-smooth at 0 only through
    |xi|^{2a}, multiplied by a factor vanishing to order 2m, which forces an ALGEBRAIC
    tail x^{-(1+2a+2m)}; the local control d_x psi_m decays like e^{-x^2/4}.
    Reported as a fitted exponent against the predicted 1+2a+2m.
    """
    xs = np.array(xs, dtype=float)
    img = FractionalBasisImages(max(m, 2), alpha, float(xs[-1]))
    f = np.abs(img.at(xs)[:, m])
    p = np.polyfit(np.log(xs), np.log(f), 1)
    _, D = bc.psi_values(max(m, 2), xs)
    return {"alpha": alpha, "m": m, "x": xs.tolist(),
            "abs_nonlocal": f.tolist(),
            "abs_local_control": np.abs(D[:, m]).tolist(),
            "fitted_exponent": float(-p[0]),
            "predicted_exponent": 1.0 + 2.0 * alpha + 2.0 * m}


# ===========================================================================
# 3.  THE NONLOCAL PROBLEM ON BREDEN-CHU'S OWN QUADRATURE
# ===========================================================================

def nonlocal_columns(n, alpha, rules, block=256):
    """The Lam^{2a}psi_m columns at each rule's nodes, on the rule's OWN weight share.

    V[i,m] = psi_m(x_i) e^{log_share_i}; this returns the same object with psi replaced
    by Lam^{2a}psi, so every Breden-Chu formula downstream is theirs with one
    substitution.  Computed once per (n, alpha) and reused across the homotopy.
    """
    LV = {}
    for key in ("four", "six"):
        r = rules[key]
        log_share = (r.log_w - (r.alpha + 1.0) * math.log(r.c)) / r.K
        img = FractionalBasisImages(n, alpha, float(np.max(r.x)))
        LV[key] = img.at(r.x, block=block) * np.exp(log_share)[:, None]
    return LV


class NonlocalSelfSimilar:
    """L u - u/4 + u^2 W_t u = 0 with W_t = (1-t) d_x + t Lam^{2a}, in Breden-Chu's basis.

    t is the HOMOTOPY IN NONLOCALITY.  t = 0 is Breden-Chu eq. (54) exactly, so this
    class must reproduce `bc.bounds` at t = 0 -- a regression control that can come out
    differently, and is checked.  t = 1 is the fully nonlocal object.
    """

    def __init__(self, n, alpha, rules=None, t=1.0, LV=None):
        self.n, self.alpha, self.t = n, float(alpha), float(t)
        self.rules = rules if rules is not None else bc.make_rules(n)
        self.lam = bc.eigenvalues(n)
        self.LV = LV if LV is not None else nonlocal_columns(n, self.alpha, self.rules)
        self.W = {k: (1.0 - self.t) * self.rules[k].DV + self.t * self.LV[k]
                  for k in ("four", "six")}

    def nonlinear_coeffs(self, a):
        V4, LV4 = self.rules["four"].V, self.W["four"]
        u, lu = V4 @ a, LV4 @ a
        return V4.T @ (u * u * lu)

    def F(self, a):
        return a + (-a / 4.0 + self.nonlinear_coeffs(a)) / self.lam

    def DF(self, a):
        V4, LV4 = self.rules["four"].V, self.W["four"]
        u, lu = V4 @ a, LV4 @ a
        G = V4.T @ ((u * lu)[:, None] * V4)
        DG = V4.T @ ((u * u)[:, None] * LV4)
        M = np.eye(self.n + 1) - np.diag(1.0 / (4.0 * self.lam))
        M += (2.0 * G + DG) / self.lam[:, None]
        return M, G, DG

    def newton(self, a0, tol=1e-13, max_iter=60):
        a = np.array(a0, dtype=float)
        hist = []
        for _ in range(max_iter):
            r = self.F(a)
            rn = float(np.linalg.norm(self.lam * r))
            hist.append(rn)
            if rn < tol or not np.isfinite(rn):
                break
            M, _, _ = self.DF(a)
            try:
                a = a - np.linalg.solve(M, r)
            except np.linalg.LinAlgError:
                break
        return a, hist


# -- M3: is the machinery's own quadrature still exact? ---------------------

def m3_quadrature_exactness(problem, a, panels=4000, k=16, R=48.0):
    """Breden-Chu's K-product rules are EXACT for products of psi and d_xpsi (polynomial
    times Gaussian).  Lam^{2a}psi is not in that class.  Measure the induced error, on
    the very quantity their tail bounds are a difference of.

    Reference: a refined direct Gauss-Legendre integral in x of the same integrand.
    """
    V4, LV4 = problem.rules["four"].V, problem.W["four"]
    V6 = problem.rules["six"].V
    LV6 = problem.W["six"]
    u6, lu6 = V6 @ a, LV6 @ a
    rule_full_sq = float(np.sum(u6 ** 4 * lu6 ** 2))          # ||ubar^2 Lam ubar||^2 by rule

    x, w = panel_rule(0.0, R, panels, k)
    wt = np.exp(x * x / 4.0)
    P, D = bc.psi_values(problem.n, x)
    img = FractionalBasisImages(problem.n, problem.alpha, R)
    u = P @ a
    du = D @ a
    # the reference carries the SAME homotopy mixture as the rule it is judging, so at
    # t = 0 this comparison reduces to the local one and MUST read ~0: M3 contains its
    # own control, and the ramp in t is the measurement.
    lu = (1.0 - problem.t) * du + problem.t * img.apply(a, x)
    # NO factor 2 for evenness: Breden-Chu's product rules are half-line rules.  That
    # convention was not assumed, it was MEASURED by the local control below, which
    # came out at exactly 0.5 with a factor 2 present and ~0 without it.
    ref_full_sq = float(np.sum(w * wt * (u * u * lu) ** 2))

    proj = problem.nonlinear_coeffs(a)
    proj_sq = float(np.dot(proj, proj))

    # the SAME diagnostic for the LOCAL control, where the rule IS exact
    DV6 = problem.rules["six"].DV
    du6 = DV6 @ a
    loc_rule_sq = float(np.sum(u6 ** 4 * du6 ** 2))
    loc_ref_sq = float(np.sum(w * wt * (u * u * du) ** 2))

    return {
        "t": problem.t, "R_reference": R, "panels": panels, "k": k,
        "nonlocal_rule_full_sq": rule_full_sq,
        "nonlocal_reference_full_sq": ref_full_sq,
        "nonlocal_rel_error": abs(rule_full_sq / ref_full_sq - 1.0) if ref_full_sq else float("nan"),
        "local_control_rule_full_sq": loc_rule_sq,
        "local_control_reference_full_sq": loc_ref_sq,
        "local_control_rel_error": abs(loc_rule_sq / loc_ref_sq - 1.0) if loc_ref_sq else float("nan"),
        "projected_sq": proj_sq,
        "tail_sq_by_rule": rule_full_sq - proj_sq,
        "tail_sq_by_reference": ref_full_sq - proj_sq,
        "tail_sq_by_rule_is_negative": bool(rule_full_sq - proj_sq < 0.0),
        "cancellation_ratio_full_over_tail": (
            abs(ref_full_sq / (ref_full_sq - proj_sq))
            if abs(ref_full_sq - proj_sq) > 0 else float("inf")),
    }


# -- M4: the sup-norm route -------------------------------------------------

def m4_sup_norms(n, alpha, x_max=40.0, n_x=6000):
    """sup|Lam^{2a} psi_m| and its growth in m, against sup|d_x psi_m| and Remark 41.

    What Zbar22/Z2/Z3 need is the convergence of sum_m sup^2 / lam_m^2; the growth
    exponent decides it, so the exponent is what is reported.
    """
    x = np.linspace(0.0, x_max, n_x)
    img = FractionalBasisImages(n, alpha, x_max)
    L = np.abs(img.at(x))
    sup_nl = np.max(L, axis=0)
    meas_sup, meas_dsup = bc.sharp_sup_psi(n)
    lam = bc.eigenvalues(n)
    m = np.arange(n + 1)
    fit = np.polyfit(np.log(m[2:] + 1.0), np.log(sup_nl[2:]), 1)
    return {
        "alpha": alpha, "n": n, "x_max": x_max,
        "sup_nonlocal": sup_nl.tolist(),
        "sup_local_control_dpsi": meas_dsup.tolist(),
        "sup_psi_measured": meas_sup.tolist(),
        "growth_exponent_fitted": float(fit[0]),
        "series_sum_sup_sq_over_lam_sq_nonlocal": float(np.sum(sup_nl ** 2 / lam ** 2)),
        "series_sum_sup_sq_over_lam_sq_local": float(np.sum(meas_dsup ** 2 / lam ** 2)),
        "series_partial_tail_last_decade_nonlocal": float(
            np.sum((sup_nl ** 2 / lam ** 2)[max(1, n // 2):])),
    }


# -- M5: the bounds themselves ---------------------------------------------

def m5_bounds(problem, a, sup_psi=None, sup_dpsi=None):
    """Breden-Chu section 6's bounds with Lam^{2a} in place of d_x.

    Grading (stated in every consumer of this dict):
      DERIVATION-FREE : Y, Zbar11, Zbar21
      TRANSCRIBED     : Zbar12, Zbar22, Z2, Z3  (their derivations used locality)
    """
    n = problem.n
    lam = problem.lam
    lam_next = bc.lambda_next(n)
    V4, LV4 = problem.rules["four"].V, problem.W["four"]
    V6, LV6 = problem.rules["six"].V, problem.W["six"]
    if sup_psi is None or sup_dpsi is None:
        sup_psi, sup_dpsi = bc.sup_psi_bounds(n)

    u4, lu4 = V4 @ a, LV4 @ a
    u6, lu6 = V6 @ a, LV6 @ a

    PF = problem.F(a)
    M, G, DG = problem.DF(a)
    An = np.linalg.inv(M)

    proj_nl = V4.T @ (u4 * u4 * lu4)
    full_nl_sq = float(np.sum(u6 ** 4 * lu6 ** 2))
    proj_nl_sq = float(np.dot(proj_nl, proj_nl))
    tail_sq = full_nl_sq - proj_nl_sq
    finite_sq = float(np.sum((lam * (An @ PF)) ** 2))
    Y = math.sqrt(max(finite_sq + tail_sq, 0.0))

    Z11 = bc.op_norm(lam[:, None] * (np.eye(n + 1) - An @ M) / lam[None, :])

    col = (u6 * lu6)[:, None] * V6
    int_full = np.sum(col * col, axis=0)
    dcol = (u6 * u6)[:, None] * LV6
    dint_full = np.sum(dcol * dcol, axis=0)
    w = (2.0 * np.sqrt(np.maximum(int_full - np.sum(G * G, axis=0), 0.0))
         + np.sqrt(np.maximum(dint_full - np.sum(DG * DG, axis=0), 0.0)))
    Z21 = float(np.linalg.norm(w / lam))

    S_n = bc.tail_constant_S(n)
    psi0 = bc.psi_at_zero(n)
    u0 = float(np.dot(a, psi0))
    dcol2 = (u6 * u6)[:, None] * (LV6 + V6)
    dint2 = np.sum(dcol2 * dcol2, axis=0)
    DG2 = V4.T @ ((u4 * u4)[:, None] * (V4 + LV4))
    wt = (u0 * u0 * math.sqrt(S_n) * psi0
          + np.sqrt(np.maximum(dint2 - np.sum(DG2 * DG2, axis=0), 0.0)) / lam_next)
    Z12 = float(np.linalg.norm(np.abs(lam[:, None] * An / lam[None, :]) @ wt))

    sup_u = float(np.dot(np.abs(a), sup_psi))
    sup_du = float(np.dot(np.abs(a), sup_dpsi))
    Z22 = (0.25 + 2.0 * sup_u * sup_du) / lam_next + sup_u ** 2 / math.sqrt(lam_next)

    B = np.array([[Z11, Z12], [Z21, Z22]])
    Z1 = float(np.linalg.norm(B, 2))
    op_n = max(bc.op_norm(lam[:, None] * An / lam[None, :]), 1.0)
    Z2 = 2.0 ** 3.75 * op_n * (math.sqrt(2.0) * sup_u + sup_du)
    Z3 = 96.0 * op_n

    return {
        "n": n, "alpha": problem.alpha,
        "Y": Y, "Z1": Z1, "Z2": Z2, "Z3": Z3,
        "Zbar11": Z11, "Zbar12": Z12, "Zbar21": Z21, "Zbar22": Z22,
        "op_norm_LAL": op_n,
        "Y_finite_part": math.sqrt(max(finite_sq, 0.0)),
        "Y_tail_part_signed": tail_sq,
        "Y_tail_part": math.sqrt(max(tail_sq, 0.0)),
        "tail_sq_negative": bool(tail_sq < 0.0),
        "nonlinearity_norm_sq_by_rule": full_nl_sq,
        "PF_H2_norm": float(np.linalg.norm(lam * PF)),
        "sup_ubar": sup_u, "sup_dubar": sup_du, "ubar_at_zero": u0,
        "grading": {"derivation_free": ["Y", "Zbar11", "Zbar21"],
                    "transcribed": ["Zbar12", "Zbar22", "Z2", "Z3"]},
    }


# ===========================================================================
# 4.  THE RUN
# ===========================================================================

TS = tuple(round(0.1 * i, 3) for i in range(11))
M3_AT = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)


def bc_seed(n, coarse=None, coarse_n=None):
    """Leg 256's seed recipe, EXACTLY: shoot to x_max=12.0 at h=1e-4 and project.

    Leg 256's ladder starts at n = 100 and prolongs by zero-padding; seeding a Newton
    below that n put the iterate outside the basin (measured: residual 1.7e3).  When a
    coarser converged coefficient vector is supplied it is zero-padded instead.
    """
    if coarse is not None:
        out = np.zeros(n + 1)
        out[:coarse_n + 1] = coarse
        return out
    a0_amp = bc.find_amplitude()
    xs, us = bc.shoot_profile(a0_amp, x_max=12.0, h=1e-4)
    return bc.project_profile(xs, us, n)


def homotopy(n, alpha, rules, seed, ts=TS, m3_at=M3_AT, sup_psi=None, sup_dpsi=None):
    """Continue from t=0 (Breden-Chu eq. 54, exactly) to t=1 (fully nonlocal).

    Newton at each t starts from the previous t's solution, so the ladder in t is the
    measurement: WHERE it stops closing, and by which bound, not merely whether t=1 does.
    """
    LV = nonlocal_columns(n, alpha, rules)
    steps, a = [], np.array(seed, dtype=float)
    lam = bc.eigenvalues(n)
    a_local = None
    ctx = {"LV": LV, "a_last_good": None, "t_last_good": None}
    for t in ts:
        prob = NonlocalSelfSimilar(n, alpha, rules, t=t, LV=LV)
        a, hist = prob.newton(a)
        conv = bool(np.isfinite(hist[-1]) and hist[-1] < 1e-9)
        if not conv:
            a = np.array(seed, dtype=float)          # do not carry a diverged iterate
        if t == 0.0:
            a_local = a.copy()
        b = m5_bounds(prob, a, sup_psi, sup_dpsi)
        v = bc.radii_verdict(b["Y"], b["Z1"], b["Z2"], b["Z3"])
        # u == 0 solves the equation for EVERY t, and its radii polynomial closes with
        # Y ~ 1e-29.  That is lesson 90: a verdict that cannot come out differently.
        # Flagged here so no consumer can read it as a certification.
        trivial = bool(b["sup_ubar"] < 1e-8)
        step = {"t": t, "newton_residual_H2": hist[-1], "newton_iters": len(hist),
                "newton_converged": conv, "bounds": b, "radii": v,
                "collapsed_to_trivial_solution": trivial,
                "verdict_is_meaningful": bool(conv and not trivial),
                "profile_distance_from_t0_H2": (
                    float(np.linalg.norm(lam * (a - a_local))) if a_local is not None
                    else float("nan"))}
        if conv and not trivial:
            ctx["a_last_good"], ctx["t_last_good"] = a.copy(), t
        if t in m3_at and conv and not trivial:
            step["M3_quadrature"] = m3_quadrature_exactness(prob, a)
        steps.append(step)
        print("   n=%3d a=%.2f t=%.3f  res=%.2e sup=%.4g Y=%.4e Z1=%.5g Z2=%.4g "
              "Z3=%.4g closes=%s tailneg=%s trivial=%s"
              % (n, alpha, t, hist[-1], b["sup_ubar"], b["Y"], b["Z1"], b["Z2"],
                 b["Z3"], v["closes"], b["tail_sq_negative"], trivial))
        sys.stdout.flush()
    return steps, ctx


def locate_z1_crossing(n, alpha, rules, steps, ctx, iters=14,
                       sup_psi=None, sup_dpsi=None):
    """The t at which Zbar/Z1 leaves Breden-Chu's admissible region Z1 < 1.

    This, not the fold, is the GATE quantity: the radii polynomial has no positive root
    at all once Z1 >= 1, whatever Y does.  Reported as the fraction of nonlocality the
    machinery's own contraction constant tolerates.
    """
    alive = [s for s in steps if s["verdict_is_meaningful"]]
    if not alive:
        return {"crossed": None, "note": "no meaningful step"}
    if all(s["bounds"]["Z1"] >= 1.0 for s in alive):
        return {"crossed": True, "t_star": 0.0,
                "note": "Z1 >= 1 already at t = 0; the LOCAL control is not admissible "
                        "at this n, so the crossing carries no nonlocal information"}
    below = [s for s in alive if s["bounds"]["Z1"] < 1.0]
    above = [s for s in alive if s["bounds"]["Z1"] >= 1.0]
    t_lo = max(s["t"] for s in below)
    if not above:
        return {"crossed": False, "t_last_below": t_lo,
                "Z1_max_on_grid": max(s["bounds"]["Z1"] for s in alive),
                "note": "Z1 < 1 wherever the branch was tracked"}
    t_hi = min(s["t"] for s in above if s["t"] > t_lo)
    LV, a = ctx["LV"], ctx["a_last_good"]
    a_lo = a
    trail = []
    for _ in range(iters):
        t_mid = 0.5 * (t_lo + t_hi)
        prob = NonlocalSelfSimilar(n, alpha, rules, t=t_mid, LV=LV)
        a_mid, hist = prob.newton(a_lo)
        b = m5_bounds(prob, a_mid, sup_psi, sup_dpsi)
        ok = bool(np.isfinite(hist[-1]) and hist[-1] < 1e-9 and b["sup_ubar"] > 1e-8)
        trail.append({"t": t_mid, "Z1": b["Z1"], "Y": b["Y"], "sup_ubar": b["sup_ubar"],
                      "meaningful": ok})
        if ok and b["Z1"] < 1.0:
            t_lo, a_lo = t_mid, a_mid
        else:
            t_hi = t_mid
    return {"crossed": True, "t_star": 0.5 * (t_lo + t_hi),
            "t_last_below": t_lo, "t_first_at_or_above": t_hi,
            "bracket_width": t_hi - t_lo, "bisection_trail": trail,
            "Z1_at_t0": steps[0]["bounds"]["Z1"],
            "nonlocal_fraction_tolerated": 0.5 * (t_lo + t_hi)}


def locate_fold(n, alpha, rules, steps, ctx, iters=12, sup_psi=None, sup_dpsi=None):
    """Bisect the last t whose Newton keeps a NONTRIVIAL profile.

    The continuation loses the branch between two grid t's; this reports where, and the
    sup-norm it has reached there, so the loss is a magnitude and not a bracket.  u == 0
    is a solution at every t, so 'lost' means 'the nontrivial branch was not found from
    the previous solution', which is a statement about the branch AND the solver.
    """
    good = [s for s in steps if s["verdict_is_meaningful"]]
    bad = [s for s in steps if not s["verdict_is_meaningful"]]
    if not bad or not good:
        return {"branch_lost": False, "note": "no loss on the t-grid"}
    t_lo = max(s["t"] for s in good)
    t_hi = min((s["t"] for s in bad if s["t"] > t_lo), default=None)
    if t_hi is None:
        return {"branch_lost": False, "note": "all losses precede the last good t"}
    LV = ctx["LV"]
    a_lo = ctx["a_last_good"]
    if a_lo is None:
        return {"branch_lost": True, "note": "no good step to continue from"}
    t_lo = ctx["t_last_good"]
    t_hi = min((s["t"] for s in steps
                if not s["verdict_is_meaningful"] and s["t"] > t_lo), default=None)
    if t_hi is None:
        return {"branch_lost": False, "note": "all losses precede the last good t"}
    trail = []
    for _ in range(iters):
        t_mid = 0.5 * (t_lo + t_hi)
        prob = NonlocalSelfSimilar(n, alpha, rules, t=t_mid, LV=LV)
        a_mid, hist = prob.newton(a_lo)
        b = m5_bounds(prob, a_mid, sup_psi, sup_dpsi)
        ok = bool(np.isfinite(hist[-1]) and hist[-1] < 1e-9 and b["sup_ubar"] > 1e-8)
        trail.append({"t": t_mid, "kept_branch": ok, "sup_ubar": b["sup_ubar"],
                      "Z1": b["Z1"], "Y": b["Y"], "residual": hist[-1]})
        if ok:
            t_lo, a_lo = t_mid, a_mid
        else:
            t_hi = t_mid
    last = trail[-1]
    return {"branch_lost": True, "t_last_kept": t_lo, "t_first_lost": t_hi,
            "bracket_width": t_hi - t_lo, "bisection_trail": trail,
            "sup_ubar_at_last_kept": max(
                (s["sup_ubar"] for s in trail if s["kept_branch"]), default=last["sup_ubar"]),
            "Z1_at_last_kept": max(
                (s["Z1"] for s in trail if s["kept_branch"]), default=last["Z1"])}


def run(ns=(100, 200), alphas=(0.25, 0.5, 0.75), headline_n=200, headline_alpha=0.5):
    t0 = time.time()
    res = {
        "leg": 331, "route": "NLH",
        "gate_question": ("Does bc_weighted_sobolev.py's machinery, pointed at a named "
                          "nonlocal operator on its own weighted space, produce finite, "
                          "closing bounds of the same kind it produces for the local "
                          "operators it was built on?"),
        "realization": ("even half-Hermite/Laguerre basis psi_m = L_m^{(-1/2)}(x^2/4)"
                        "e^{-x^2/4}/Zeta_m; H^2(mu), mu = e^{|x|^2/4}/Z; d = 1; even "
                        "(Neumann) sector; nonlocal operator Lam^{2a} = (-Delta)^a, "
                        "a = 1/2 being H d_x; float64, NOT interval arithmetic"),
        "arithmetic_ceiling": ("float64. Reproduces CONSTANTS, not a proof. Nothing here "
                               "is a rigorous enclosure or may be cited as one."),
        "headline_n": headline_n, "headline_alpha": headline_alpha,
    }

    # -- instrument gates first ------------------------------------------
    res["instrument_gates"] = {
        "alpha_zero_identity": gate_alpha_zero(),
        "alpha_one_laplacian": gate_alpha_one(),
        "line_hilbert_cross_check": gate_line_hilbert_cross_check(),
    }
    print("gate a=0  max rel defect %.3e"
          % res["instrument_gates"]["alpha_zero_identity"]["max_rel_defect"])
    print("gate a=1  max rel defect %.3e"
          % res["instrument_gates"]["alpha_one_laplacian"]["max_rel_defect"])
    print("line_hilbert worst rel  %.3e"
          % res["instrument_gates"]["line_hilbert_cross_check"]["worst_rel_to_peak"])

    # -- M1 ---------------------------------------------------------------
    res["M1_image_in_space"] = m1_truncated_weighted_norms(
        4, headline_alpha, radii=(4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0))
    res["M1_tail_exponents"] = [m1_tail_exponent(a, m=0) for a in alphas]
    print("M1 done  %.1fs" % (time.time() - t0))

    # -- the local control problem, for side-by-side ----------------------
    res["by_n"] = {}
    coarse, coarse_n = None, None
    for n in ns:
        rules = bc.make_rules(n)
        sup_psi, sup_dpsi = bc.sup_psi_bounds(n)
        loc = bc.BurgersSelfSimilar(n, rules)
        seed = bc_seed(n, coarse, coarse_n)
        a_loc, hist_loc = loc.newton(seed)
        coarse, coarse_n = a_loc, n
        loc_bounds = bc.bounds(loc, a_loc)
        loc_verdict = bc.radii_verdict(loc_bounds["Y"], loc_bounds["Z1"],
                                       loc_bounds["Z2"], loc_bounds["Z3"])
        print("n=%3d LOCAL CONTROL res=%.2e Y=%.4e Z1=%.5g closes=%s  (%.1fs)"
              % (n, hist_loc[-1], loc_bounds["Y"], loc_bounds["Z1"],
                 loc_verdict["closes"], time.time() - t0))
        sys.stdout.flush()

        entry = {"n": n,
                 "local_control": {"newton_residual_H2": hist_loc[-1],
                                   "newton_iters": len(hist_loc),
                                   "bounds": loc_bounds, "radii": loc_verdict},
                 "homotopy": {}}

        for alpha in alphas:
            steps, ctx = homotopy(n, alpha, rules, a_loc,
                                  sup_psi=sup_psi, sup_dpsi=sup_dpsi)
            fold = locate_fold(n, alpha, rules, steps, ctx,
                               sup_psi=sup_psi, sup_dpsi=sup_dpsi)
            cross = locate_z1_crossing(n, alpha, rules, steps, ctx,
                                       sup_psi=sup_psi, sup_dpsi=sup_dpsi)
            print("   -> Z1<1 crossing: %s" % {k: v for k, v in cross.items()
                                               if k != "bisection_trail"})
            print("   -> fold: %s" % {k: v for k, v in fold.items()
                                      if k != "bisection_trail"})
            sys.stdout.flush()
            # -- the t = 0 REGRESSION CONTROL: must reproduce bc.bounds exactly
            b0 = steps[0]["bounds"]
            keys = ("Y", "Z1", "Z2", "Z3", "Zbar11", "Zbar12", "Zbar21", "Zbar22")
            rel = {k: (abs(b0[k] - loc_bounds[k]) / abs(loc_bounds[k])
                       if loc_bounds.get(k) else float("nan")) for k in keys
                   if k in loc_bounds}
            entry["homotopy"][str(alpha)] = {
                "steps": steps, "fold": fold, "Z1_crossing": cross,
                "t0_regression_control": {
                    "max_rel_diff_vs_bc_bounds": max(
                        v for v in rel.values() if math.isfinite(v)),
                    "per_bound_rel_diff": rel,
                    "note": ("t=0 sets W = d_x identically, so this compares the leg's "
                             "own bound code against solver/bc_weighted_sobolev.py's "
                             "bounds() on the same coefficients; it CAN come out "
                             "differently (lesson 90) and is what licenses t>0.")},
            }
        res["by_n"][str(n)] = entry
        print("n=%d done  %.1fs" % (n, time.time() - t0))
        sys.stdout.flush()

    # -- M4 ---------------------------------------------------------------
    res["M4_sup_norms"] = {str(a): m4_sup_norms(60, a) for a in alphas}
    res["runtime_s"] = time.time() - t0
    print("total %.1fs" % res["runtime_s"])
    return res


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote", OUT_JSON)
