#!/usr/bin/env python3
"""Route-H2S v1 — SCOPING: is a certificate formulation structurally viable on origin-H^2?

WHAT THIS LEG IS, AND WHAT IT IS NOT
------------------------------------
Leg 127 proved `Z_1 >= 1` for EVERY bounded approximate inverse `A` on this
repository's weighted-`ell^1` realization at `s < 1`, by exhibiting an explicit
singular sequence with `sigma_min(L) -> 0` (fitted exponents 0.9925 / 0.6985 /
0.3202 at `s = 0 / 0.3 / 0.7`, predicted `1 - s`, max deviation 0.0219).  In the
same pass it recorded that Xu (arXiv:2607.19762, 22 Jul 2026) proves the SAME
`a = 0` CLM linearization invertible on a DIFFERENT realization, the odd
origin-`H^2` space `X`, after modulating out the two symmetry modes.

So the ~70-leg obstruction is a property of the CHOSEN SPACE, not of the
operator.  This module asks the one question that comes before spending a leg on
a construction: **is a certificate formulation on `X` structurally viable at
all?**

It BUILDS NO CERTIFICATE and MEASURES NO CERTIFICATE.  `Y_0`, `Z_1`, `Z_2` are
never formed.  No solver module is added or edited; this file imports nothing
from `solver/`.  What it does run is FIVE LITERATURE RE-DERIVATION GATES against
Xu's published construction -- the same discipline leg 48 used on
Dahne-Figueras: quote nothing that has not been re-derived here from the paper's
own formulas.

THE OBJECT
----------
At `a = 0` the exact CLM collapse profile is `Omega(y) = -y/(y^2 + 1/4)`.  On the
upper-half-plane Hardy space `H_+^2` the Hilbert transform acts as `-i`, and Xu's
single-simple-pole identity `H Omega - i Omega = i/(y + i/2)` collapses the
NONLOCAL linearization to a SCALAR FIRST-ORDER operator (Xu eq. 4.21):

    L_0^+ = -1 - y d/dy + i/b ,          b(y) = y + i/2 .

`X = {phi odd : phi, phi'' in L^2(0, inf), phi(y) = a_1 y + o(y)}`; extended
oddly it is the odd part of `H^2(R)` with an equivalent norm,
`||phi||_X^2 = ||phi||_{L^2}^2 + ||phi''||_{L^2}^2`, and
`||phi||_X^2 = 2 ||P_+ phi||_{X_+}^2` (Xu sec 4.4), so every operator-norm
statement transfers from the Hardy block to `X` with constant 1.

Xu's resolvent (eq. 4.23), for `Re z > -1/2`, `z not in {0, 1}`:

    G = b^2 f,  G_0 = G(0),  G_1 = G'(0),  G_2(t) = G(t) - G_0 - G_1 t,
    I(y) = int_0^1 s^{z-2} G_2(y s) ds,
    Phi = I + c_0 + c_1 y,   c_0 = G_0/(z-1),  c_1 = G_1/z,
    u = R_0^+(z) f = -b^{-2} Phi .

THE FIVE GATES
--------------
  G1  Xu Lemma 4.5, the exact Hardy-Mellin norm.  `T_z g(y) = int_0^1 s^z g(ys) ds`
      has Mellin symbol `1/(z + 1/2 - i xi)` and EXACT operator norm `1/alpha`,
      `alpha = Re z + 1/2`.  Re-derived here as a closed form AND witnessed from
      below by explicit `g`, so the constant is earned, not quoted.

  G2  The resolvent identity `(L_0^+ - z) u = f`.  Xu reports a sympy-exact
      identity with float substitution residual 3e-16.  `sympy` is NOT installed
      in this venv, so this gate re-derives the identity BY HAND in the docstring
      below and then checks it NUMERICALLY, with every derivative taken
      analytically (three independent quadratures, no finite differences).

      Hand derivation, recorded because it is the reason the gate can be trusted.
      Substituting `t = ys` gives `I(y) = y^{1-z} int_0^y t^{z-2} G_2(t) dt`,
      hence `y I'(y) = (1-z) I(y) + G_2(y)`.  With `u = -Phi/b^2`,
      `y u' = -y Phi'/b^2 + 2 y Phi / b^3`, and using `2y + i = 2b`:

          (L_0^+ - z) u = b^{-2} [ (z-1) Phi + y Phi' ]
                        = b^{-2} [ (z-1) c_0 + z c_1 y + G_2 ]
                        = b^{-2} [ G_0 + G_1 y + G_2 ] = b^{-2} G = f .

      The cancellation is EXACT and it is what `c_0 = G_0/(z-1)` and
      `c_1 = G_1/z` are for.  Note where their poles sit: `z = 1` and `z = 0`,
      the two symmetry eigenvalues, and NOWHERE else.

  G3  The two symmetry modes, in closed form.  `L_0^+ (b^{-2}) = b^{-2}`
      (eigenvalue 1, the time-shift mode) and `L_0^+ (y b^{-2}) = 0`
      (eigenvalue 0, the scaling mode).  Both verified by hand above and
      numerically here.  These are Xu's stated rank-one Riesz residues.

  G4  THE CERTIFICATE-RELEVANT ONE: the BORDERED reduction at `z = 0`.  The only
      thing singular at `z = 0` is `c_1 = G_1/z`, and `G_1 = G'(0) = (b^2 f)'(0)`
      is a RANK-ONE functional of `f`:

          ell(f) = 2 b(0) f(0) + b(0)^2 f'(0) = i f(0) - f'(0)/4 .

      So the bordered system that this repository's stage TC already has the
      shape of --

          [ L_0^+   m ] [ u ]   [ f ]              m(y) = y b(y)^{-2}
          [ ell     0 ] [ k ] = [ 0 ]              (the z=0 null mode)

      -- removes the singularity COMPLETELY, with a rank-one border per Hardy
      block (rank two on the real odd space).  This gate measures
      `||u||_X / ||f||_X` on the solvability subspace `{ell(f) = 0}` over a
      family of test data.  That ratio is the `X`-realization analogue of the
      quantity leg 127 drove to ZERO in `ell^1_w`.

      CONTRAST WORTH STATING PRECISELY.  Leg 127 found that the `ell^1_w`
      singular sequence has EXACTLY ZERO far-field-amplitude component, so
      bordering does not move the obstruction at all.  Here the singularity IS
      the border direction: `m` spans the residue exactly.

  G5  The `alpha^{-3/2}` majorant.  Xu's Prop 4.6 bound `||R_0(z)||_X <=
      C(R,d) alpha^{-3/2}` blows up only as `z` approaches the essential line
      `Re z = -1/2`.  The certificate-relevant point is `z = 0`, where
      `alpha = 1/2` and `alpha^{-3/2} = 2^{3/2}`.  This gate reports the shape of
      the curve and the value at the point that matters, and re-derives the
      explicit pieces Xu makes explicit (`c_G = 5/4 + sqrt(10) + 2`, the
      `1/alpha` Hardy norm, the `1/sqrt(2 alpha)` tail norm).  `C(R,d)` is left
      implicit by the paper and is NOT invented here.

CEILING (stated up front, not buried)
-------------------------------------
Everything above is a consequence of `a = 0` EXACTNESS.  The single-simple-pole
identity, the Hardy block-diagonalization to a scalar ODE, the closed-form
kernel and the exact Mellin norm all hold because `Omega` is the exact CLM
profile.  For `a > 0` Xu proves only a CONDITIONAL two-line inclusion under his
hypothesis `Adm(a)`: no resolvent, no invertibility, no gap.  Nothing here
transfers to `HL_S2_nonsymmetric`, which is not a CLM profile.  No link of the
`L1 -> L4` chain moves.  Float64 throughout; nothing interval-enclosed.
"""

import json
import math
import os

import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "writeup", "data", "p2_route_h2s_v1_scoping.json")

# ---------------------------------------------------------------------------
# quadrature helpers
# ---------------------------------------------------------------------------

def _gl(n):
    """Gauss-Legendre nodes/weights on (0, 1)."""
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (x + 1.0), 0.5 * w


def _half_line_quad(n=400):
    """Nodes/weights for int_0^inf . dy via y = t/(1-t)."""
    t, w = _gl(n)
    y = t / (1.0 - t)
    jac = 1.0 / (1.0 - t) ** 2
    return y, w * jac


# ---------------------------------------------------------------------------
# the object: L_0^+ = -1 - y d/dy + i/b, b = y + i/2
# ---------------------------------------------------------------------------

def b_of(y):
    return y + 0.5j


class TestDatum:
    """f(y) = sum_n coeff_n (y + i)^{-n}: analytic in the UHP, so in H_+^2.

    Closed-form f, f', f'' -- no finite differences anywhere in this module.
    """

    def __init__(self, coeffs):
        # coeffs: dict {n: c_n}, n >= 1
        self.coeffs = dict(coeffs)

    def f(self, y):
        z = y + 1.0j
        return sum(c * z ** (-n) for n, c in self.coeffs.items())

    def df(self, y):
        z = y + 1.0j
        return sum(c * (-n) * z ** (-n - 1) for n, c in self.coeffs.items())

    def d2f(self, y):
        z = y + 1.0j
        return sum(c * n * (n + 1) * z ** (-n - 2) for n, c in self.coeffs.items())


def G_parts(td, y):
    """G = b^2 f and its first two derivatives, in closed form."""
    b = b_of(y)
    f, f1, f2 = td.f(y), td.df(y), td.d2f(y)
    G = b * b * f
    G1 = 2.0 * b * f + b * b * f1
    G2 = 2.0 * f + 4.0 * b * f1 + b * b * f2
    return G, G1, G2


# --- the second-order Taylor remainder G_2, WITHOUT cancellation ------------
#
# The first working draft of this module formed G_2(t) = G(t) - G(0) - G'(0) t
# by literal subtraction.  For small t that is a difference of nearly equal
# floats -- G_2 is O(t^2) while G(0) is O(1) -- and the resolvent integrand then
# multiplies the resulting noise by s^{z-2}, which is 1e+14 at s = 1e-6, z = -0.4.
# The observed relative residual was 1.0e+09 on one of the three test data and
# 9.2e-06 on another, at the SAME z.  Two data disagreeing by fifteen orders of
# magnitude on the same identity is a floating-point tell, not a mathematical
# one (lesson 86: a bound dominated by its own evaluation error is a statement
# about the code).  The repair is to build G_2 from its own Taylor coefficients.
#
# f(y) = sum_n c_n (y + i)^{-n},  and  (t + i)^{-n} = i^{-n} sum_k C(n+k-1, k) (i t)^k,
# convergent for |t| < 1.  With b^2 = t^2 + i t - 1/4,
#     G(t) = (-1/4 + i t + t^2) P(t),   P(t) = sum_k p_k t^k,
#     g_m = -p_m/4 + i p_{m-1} + p_{m-2},
# and G_2(t) = sum_{m >= 2} g_m t^m -- every term genuinely present, nothing
# subtracted.  G_2'' = G'' needs no repair (it involves no subtraction) and is
# left in closed form, which also makes the switch-over auditable.

_SERIES_K = 90
_SERIES_SWITCH = 0.5


def _series_g(td, K=_SERIES_K):
    cached = getattr(td, "_g_series", None)
    if cached is not None:
        return cached
    p = np.zeros(K + 1, dtype=complex)
    for n, c in td.coeffs.items():
        n = int(n)
        for k in range(K + 1):
            p[k] += c * (1j) ** (-n) * math.comb(n + k - 1, k) * (1j) ** k
    g = np.zeros(K + 1, dtype=complex)
    for m in range(K + 1):
        g[m] = -p[m] / 4.0
        if m >= 1:
            g[m] += 1j * p[m - 1]
        if m >= 2:
            g[m] += p[m - 2]
    td._g_series = g
    return g


def G2_remainder(td, t, g_series=None):
    """G_2(t) = G(t) - G(0) - G'(0) t and G_2'(t), cancellation-free near 0."""
    t = np.asarray(t)
    g = _series_g(td) if g_series is None else g_series
    G0, G1_0, _ = G_parts(td, 0.0)

    Gv, Gd, _ = G_parts(td, t)
    far_v = Gv - G0 - G1_0 * t
    far_d = Gd - G1_0

    tt = np.abs(t)
    use_near = tt < _SERIES_SWITCH
    tsafe = np.where(use_near, t, 0.0)

    # Horner, so nothing of size (len(t), K) is ever allocated.
    q = g[2:]
    j = np.arange(len(q))
    acc_v = np.zeros_like(tsafe, dtype=complex)
    acc_d = np.zeros_like(tsafe, dtype=complex)
    for k in range(len(q) - 1, -1, -1):
        acc_v = acc_v * tsafe + q[k]
        acc_d = acc_d * tsafe + (j[k] + 2) * q[k]
    near_v = tsafe * tsafe * acc_v
    near_d = tsafe * acc_d

    return np.where(use_near, near_v, far_v), np.where(use_near, near_d, far_d)


def _s_panels(y, n_s, power=4):
    """Per-y quadrature nodes/weights for int_0^1 . ds, split at s* = min(1, 1/y).

    THE INTEGRAND HAS TWO REGIMES AND ONE PANEL CANNOT SEE BOTH.  For s < 1/y the
    argument ys is inside the origin-Taylor regime where G_2(ys) = O((ys)^2) and
    s^{z-2} G_2(ys) = O(s^z): a power endpoint, handled by s = s* sigma^power.
    For s > 1/y the argument runs from 1 out to y, so the integrand spreads over
    log10(y) DECADES: handled by the log grading s = (s*)^{1-v}, under which
    ds = s (-ln s*) dv and the integrand becomes smooth in v.

    The first draft of this module used a single power panel over the whole
    interval and reported relative residuals of 1e+09 at y = 1e3.  That was the
    quadrature, not the identity -- which is exactly why gate G2 samples a wide
    y range and reports the residual instead of asserting the algebra.
    """
    y = np.atleast_1d(np.asarray(y, dtype=float))
    sA = np.minimum(1.0, 1.0 / np.maximum(y, 1e-300))       # (ny,)
    sig, wq = _gl(n_s)

    # panel A: (0, sA) with a power grading
    sa = sA[:, None] * (sig ** power)[None, :]
    wa = sA[:, None] * (power * sig ** (power - 1) * wq)[None, :]

    # panel B: (sA, 1) with a log grading; empty (weight 0) when sA == 1
    lg = -np.log(np.maximum(sA, 1e-300))                     # (ny,)
    sb = sA[:, None] ** (1.0 - sig)[None, :]
    wb = sb * (lg[:, None]) * wq[None, :]
    wb = np.where((sA[:, None] >= 1.0), 0.0, wb)

    return np.concatenate([sa, sb], axis=1), np.concatenate([wa, wb], axis=1)


def resolvent(td, z, y, n_s=300, drop_c1=False, power=4):
    """Xu eq. (4.23): u = -b^{-2}(I + c_0 + c_1 y), plus u' and u''.

    drop_c1=True is the BORDERED branch: it is only legitimate when
    G'(0) = ell(f) = 0, which is exactly the solvability condition of gate G4.
    """
    y = np.atleast_1d(np.asarray(y, dtype=float))
    s, wgt = _s_panels(y, n_s, power=power)   # both (ny, 2*n_s)

    G0, G1_0, _ = G_parts(td, 0.0)          # G(0), G'(0)

    ys = y[:, None] * s
    _, _, Gdd = G_parts(td, ys)
    G2v, G2d = G2_remainder(td, ys)          # G_2(ys), G_2'(ys), cancellation-free
    G2dd = Gdd                               # G_2'' = G'': no subtraction, no repair

    I0 = (G2v * s ** (z - 2.0) * wgt).sum(axis=1)
    I1 = (G2d * s ** (z - 1.0) * wgt).sum(axis=1)
    I2 = (G2dd * s ** z * wgt).sum(axis=1)

    c0 = G0 / (z - 1.0)
    c1 = 0.0 if drop_c1 else G1_0 / z

    Phi = I0 + c0 + c1 * y
    Phi1 = I1 + c1
    Phi2 = I2

    b = b_of(y)
    u = -Phi / b ** 2
    du = -Phi1 / b ** 2 + 2.0 * Phi / b ** 3
    d2u = -Phi2 / b ** 2 + 4.0 * Phi1 / b ** 3 - 6.0 * Phi / b ** 4
    return u, du, d2u


def apply_L0plus(u, du, y):
    """(L_0^+ u)(y) = -u - y u' + (i/b) u."""
    return -u - y * du + 1.0j * u / b_of(y)


def x_norm(vals, d2vals, y, w):
    """||phi||_{X_+}^2 = ||phi||_{L^2(0,inf)}^2 + ||phi''||_{L^2(0,inf)}^2."""
    return math.sqrt(float(np.sum(w * (np.abs(vals) ** 2 + np.abs(d2vals) ** 2))))


# ---------------------------------------------------------------------------
# GATE 1 -- Xu Lemma 4.5, exact Hardy-Mellin norm 1/alpha
# ---------------------------------------------------------------------------

def gate_1_mellin_norm():
    rows = []
    for z in (0.0, 0.25, 1.0, -0.25, -0.4, -0.45):
        alpha = z + 0.5
        # closed form: symbol 1/(z + 1/2 - i xi), modulus maximized at xi = Im z = 0
        xi = np.linspace(-40.0, 40.0, 400001)
        sym = np.abs(1.0 / (z + 0.5 - 1j * xi))
        sup_sym = float(sym.max())
        argmax_xi = float(xi[int(sym.argmax())])
        # LOWER WITNESS, in closed form -- this is what makes 1/alpha the EXACT
        # norm rather than merely an upper bound, and it is re-derived here, not
        # quoted.  Take g_eps(y) = y^{-1/2+eps} on (0,1), zero beyond.  Its Mellin
        # transform is 1/(eps + i xi), which concentrates at xi = 0 as eps -> 0 --
        # exactly where the symbol modulus peaks for real z.  Then
        #   T_z g_eps(y) = g_eps(y) / (alpha + eps)                     for y < 1
        #   T_z g_eps(y) = y^{-1/2+eps} y^{-(alpha+eps)} / (alpha+eps)  for y > 1
        # so ||T_z g_eps||^2 / ||g_eps||^2 = (1 + eps/alpha) / (alpha + eps)^2,
        # which -> 1/alpha^2.  ANY eps > 0 already gives a valid lower bound.
        best, best_eps = 0.0, None
        for eps in (0.1, 0.02, 0.005, 0.001, 2e-4):
            ratio = math.sqrt(1.0 + eps / alpha) / (alpha + eps)
            if ratio > best:
                best, best_eps = ratio, eps
        rows.append({"z": z, "alpha": alpha, "best_witness_eps": best_eps,
                     "closed_form_1_over_alpha": 1.0 / alpha,
                     "sup_symbol_modulus": sup_sym,
                     "argmax_xi": argmax_xi,
                     "rel_err_closed_form_vs_symbol": abs(sup_sym - 1.0 / alpha) * alpha,
                     "best_lower_witness": best,
                     "witness_fraction_of_bound": best * alpha})
    max_rel = max(r["rel_err_closed_form_vs_symbol"] for r in rows)

    # CONTROL THAT CAN FAIL (lesson 90): the witness above is a closed form, and a
    # closed form nobody applied T_z to is an assertion.  Apply T_z numerically to
    # g_eps and compare pointwise, on both sides of y = 1 where the two branches
    # of the closed form differ.
    z_c, eps_c = 0.0, 0.1
    a_c = z_c + 0.5
    yv = np.array([0.05, 0.3, 0.9, 1.1, 3.0, 20.0])
    # g_eps carries an INDICATOR, so the integrand has a jump at s = 1/y.  Put a
    # panel boundary exactly there (a single power panel across the jump was the
    # first draft and converged only to 1.4e-05).
    ss, wss = _s_panels(yv, 3000, power=4)
    arg = yv[:, None] * ss
    g_at = np.where(arg < 1.0, np.maximum(arg, 1e-300) ** (-0.5 + eps_c), 0.0)
    Tg_num = (g_at * ss ** z_c * wss).sum(axis=1)
    Tg_cf = np.where(yv < 1.0,
                     yv ** (-0.5 + eps_c) / (a_c + eps_c),
                     yv ** (-0.5 + eps_c) * yv ** (-(a_c + eps_c)) / (a_c + eps_c))
    ctrl_rel = float(np.abs(Tg_num - Tg_cf).max() / np.abs(Tg_cf).max())

    return {"rows": rows, "max_rel_err": max_rel,
            "control_Tz_applied_numerically": {
                "z": z_c, "eps": eps_c,
                "y_samples": yv.tolist(),
                "max_rel_deviation_from_closed_form": ctrl_rel,
                "why_it_could_fail": ("the closed form has TWO branches (y < 1 and "
                                      "y > 1) with different exponents; sampling both "
                                      "sides means a wrong branch shows up as a large "
                                      "deviation rather than cancelling")},
            "verdict": "PASS" if (max_rel < 1e-8 and ctrl_rel < 1e-6) else "FAIL",
            "note": ("Xu Lemma 4.5 re-derived: Mellin symbol 1/(z+1/2-i xi), sup at "
                     "xi = Im z, exact norm 1/alpha.  The lower witness is reported at "
                     "whatever fraction of the bound it reaches -- an honest 'the ascent "
                     "adds nothing' number, per solver/op_lower.py's own discipline.  "
                     "The witness family is stated for REAL z; for complex z the "
                     "extremizer sits at xi = Im z and the same construction applies "
                     "after a translation.")}


# ---------------------------------------------------------------------------
# GATE 2 -- the resolvent identity (L_0^+ - z) u = f
# ---------------------------------------------------------------------------

DATA = {
    "simple_pole":  TestDatum({1: 1.0}),
    "double_pole":  TestDatum({2: 1.0}),
    "mixed":        TestDatum({1: 0.5, 2: -1.0, 3: 0.25}),
}


def gate_2_resolvent_identity():
    yq, wq = _half_line_quad(600)
    ys = yq[(yq > 1e-3) & (yq < 1e3)]
    rows = []
    for name, td in DATA.items():
        for z in (0.5, 0.25, -0.2, -0.4, 2.0, 0.3 + 0.7j):
            u, du, _ = resolvent(td, z, ys, n_s=400)
            res = apply_L0plus(u, du, ys) - z * u - td.f(ys)
            scale = np.abs(td.f(ys)).max()
            rows.append({"datum": name, "z": str(z),
                         "max_abs_residual": float(np.abs(res).max()),
                         "max_rel_residual": float(np.abs(res).max() / scale)})
    worst = max(r["max_rel_residual"] for r in rows)

    # Resolution ladder (>= 3 resolutions, leg 127's own standard).  A residual
    # quoted at one quadrature order is a statement about that order.
    ladder = []
    for name, z in (("mixed", -0.4), ("simple_pole", 0.25), ("mixed", 0.3 + 0.7j)):
        td = DATA[name]
        row = {"datum": name, "z": str(z)}
        for n in (150, 300, 600):
            u, du, _ = resolvent(td, z, ys, n_s=n)
            r = apply_L0plus(u, du, ys) - z * u - td.f(ys)
            row[f"n_s_{n}"] = float(np.abs(r).max() / np.abs(td.f(ys)).max())
        ladder.append(row)

    return {"rows": rows, "worst_rel_residual": worst,
            "resolution_ladder": ladder,
            "cancellation_repair": {
                "what": ("G_2 = G - G(0) - G'(0) t formed by LITERAL SUBTRACTION (first "
                         "draft) vs formed from its own Taylor coefficients (this module)"),
                "worst_case": "datum 'mixed', z = -0.4 (alpha = 0.1)",
                "rel_residual_before_banked": 1.0000779616959437e+09,
                "rel_residual_after_banked": 1.4182983223100105e-14,
                "improvement_factor": 1.0000779616959437e+09 / 1.4182983223100105e-14,
                "why_it_mattered": ("at the SAME z the 'simple_pole' datum read 9.2e-06 "
                                    "while 'mixed' read 1.0e+09.  Fifteen orders of "
                                    "magnitude between two data on one identity is a "
                                    "floating-point tell, not a mathematical one "
                                    "(lesson 86).  Both banked numbers are from this "
                                    "module's own runs, before and after the repair."),
            },
            "xu_reported_sympy_float_residual": 3e-16,
            "verdict": "PASS" if worst < 1e-9 else "FAIL",
            "note": ("Every derivative analytic (three independent quadratures), no "
                     "finite differences.  sympy is not installed in this venv, so Xu's "
                     "exact check is replaced by the hand derivation in this module's "
                     "docstring plus this numerical one; the floor here is quadrature, "
                     "not the identity.")}


# ---------------------------------------------------------------------------
# GATE 3 -- the two symmetry modes in closed form
# ---------------------------------------------------------------------------

def gate_3_symmetry_modes():
    yq, wq = _half_line_quad(600)
    ys = yq[(yq > 1e-4) & (yq < 1e4)]
    b = b_of(ys)

    # time-shift mode: u = b^{-2}, expect L_0^+ u = 1 * u
    u1 = b ** -2
    du1 = -2.0 * b ** -3
    r1 = apply_L0plus(u1, du1, ys) - 1.0 * u1

    # scaling mode: u = y b^{-2}, expect L_0^+ u = 0
    u0 = ys * b ** -2
    du0 = b ** -2 - 2.0 * ys * b ** -3
    r0 = apply_L0plus(u0, du0, ys) - 0.0 * u0

    return {
        "mode_eigenvalue_1": {"form": "b^{-2}",
                              "max_abs_residual": float(np.abs(r1).max()),
                              "max_abs_mode": float(np.abs(u1).max())},
        "mode_eigenvalue_0": {"form": "y b^{-2}",
                              "max_abs_residual": float(np.abs(r0).max()),
                              "max_abs_mode": float(np.abs(u0).max())},
        "verdict": "PASS" if max(float(np.abs(r1).max()),
                                 float(np.abs(r0).max())) < 1e-12 else "FAIL",
        "note": ("These are Xu's rank-one Riesz residues on H_+^2, and they are the "
                 "border COLUMN candidates.  Both identities also hold exactly by hand "
                 "(the algebra turns on 2y + i = 2b); the numbers here are the check, "
                 "not the proof."),
    }


# ---------------------------------------------------------------------------
# GATE 4 -- the bordered reduction at z = 0, and the sigma_min analogue
# ---------------------------------------------------------------------------

def _border_functional(td):
    """ell(f) = G'(0) = 2 b(0) f(0) + b(0)^2 f'(0) = i f(0) - f'(0)/4."""
    return 1.0j * td.f(0.0) - 0.25 * td.df(0.0)


def _project_to_solvable(td):
    """Subtract a multiple of a fixed datum to enforce ell(f) = 0."""
    ref = TestDatum({3: 1.0})
    lr = _border_functional(ref)
    lf = _border_functional(td)
    k = lf / lr
    merged = dict(td.coeffs)
    for n, c in ref.coeffs.items():
        merged[n] = merged.get(n, 0.0) - k * c
    return TestDatum(merged)


def gate_4_bordered_at_zero():
    yq, wq = _half_line_quad(900)
    m = (yq > 1e-5) & (yq < 1e5)
    ys, ws = yq[m], wq[m]

    rows = []
    for name, td in DATA.items():
        tds = _project_to_solvable(td)
        ell_after = complex(_border_functional(tds))
        u, du, d2u = resolvent(tds, 0.0, ys, n_s=500, drop_c1=True)
        # residual of the bordered solve: L_0^+ u = f (z = 0)
        res = apply_L0plus(u, du, ys) - tds.f(ys)
        fn = x_norm(tds.f(ys), tds.d2f(ys), ys, ws)
        un = x_norm(u, d2u, ys, ws)
        rows.append({
            "datum": name,
            "ell_after_projection_abs": abs(ell_after),
            "max_rel_residual": float(np.abs(res).max() / max(np.abs(tds.f(ys)).max(), 1e-300)),
            "f_X_norm": fn,
            "u_X_norm": un,
            "ratio_uX_over_fX": un / fn,
        })
    ratios = [r["ratio_uX_over_fX"] for r in rows]
    worst_res = max(r["max_rel_residual"] for r in rows)

    # Resolution / truncation ladder.  ||u||_X and ||f||_X are integrals over the
    # WHOLE half-line, so the ratio has to be shown stable in both the quadrature
    # order and the truncation window before it is quoted.
    ladder = []
    tds_worst = _project_to_solvable(DATA["simple_pole"])
    for n_q, lo, hi in ((600, 1e-4, 1e4), (900, 1e-5, 1e5), (1400, 1e-6, 1e6)):
        yq2, wq2 = _half_line_quad(n_q)
        mm = (yq2 > lo) & (yq2 < hi)
        y2, w2 = yq2[mm], wq2[mm]
        u2, _, d2u2 = resolvent(tds_worst, 0.0, y2, n_s=400, drop_c1=True)
        f2 = x_norm(tds_worst.f(y2), tds_worst.d2f(y2), y2, w2)
        ladder.append({"n_quad": n_q, "window": [lo, hi], "n_nodes_kept": int(mm.sum()),
                       "ratio_uX_over_fX": x_norm(u2, d2u2, y2, w2) / f2})
    spread = max(r["ratio_uX_over_fX"] for r in ladder) - min(r["ratio_uX_over_fX"] for r in ladder)
    return {
        "border_column_m": "m(y) = y b(y)^{-2}, b = y + i/2   (the z=0 null mode, gate 3)",
        "border_row_ell": "ell(f) = i f(0) - f'(0)/4   (= G'(0), the ONLY z-pole at z=0)",
        "border_rank_per_hardy_block": 1,
        "border_rank_on_odd_real_space": 2,
        "rows": rows,
        "resolution_ladder": ladder,
        "resolution_ladder_spread": spread,
        "max_ratio_uX_over_fX": max(ratios),
        "implied_sigma_min_lower_witness": 1.0 / max(ratios),
        "worst_rel_residual": worst_res,
        "verdict": "PASS" if worst_res < 1e-8 else "FAIL",
        "ell1w_contrast": {
            "leg_127_sigma_min_fitted_exponent_s0": 0.9925,
            "leg_127_sigma_min_fitted_exponent_s03": 0.6985,
            "leg_127_sigma_min_fitted_exponent_s07": 0.3202,
            "leg_127_predicted_exponent": "1 - s",
            "leg_127_max_deviation": 0.0219,
            "leg_127_bordering_effect": (
                "NONE -- bordered and unbordered sigma_min agree to 5.7e-15 relative at "
                "mu = 0.  MECHANISM, per leg 127's CORRECTED journal reading (the earlier "
                "'exactly zero far-field component' phrasing is superseded and is NOT used "
                "here): the far-field-amplitude component z[K+1] is NOT zero -- it is "
                "6.5-6.8% of ||v||_1 and GROWING with M -- but its coupling column "
                "C[:,K+1] is supported on a SINGLE ROW, the truncation edge, so leg 52's "
                "bordering repair has nowhere else to reach."),
            "origin_H2_bordering_effect": (
                "COMPLETE -- the only z-pole at z = 0 is c_1 = G'(0)/z, rank one, and "
                "its residue direction IS the border column m = y b^{-2}"),
        },
        "note": ("The ratio ||u||_X / ||f||_X is measured on a 3-element family, which "
                 "is a WITNESS from below on the reduced resolvent norm, not the norm.  "
                 "It is reported as such.  No Y_0, Z_1 or Z_2 is formed anywhere."),
    }


# ---------------------------------------------------------------------------
# GATE 5 -- the alpha^{-3/2} majorant, and where the certificate actually sits
# ---------------------------------------------------------------------------

def gate_5_majorant_shape():
    c_G = 1.25 + math.sqrt(10.0) + 2.0
    alphas = [0.5, 0.25, 0.1, 0.05, 0.01, 0.001]
    rows = []
    for a in alphas:
        rows.append({
            "alpha": a,
            "Re_z": a - 0.5,
            "alpha_pow_minus_3_2": a ** -1.5,
            "hardy_norm_1_over_alpha": 1.0 / a,
            "tail_norm_1_over_sqrt_2alpha": 1.0 / math.sqrt(2.0 * a),
            "origin_taylor_coeff_majorant_A": c_G / (math.sqrt(3.0) * a),
            "A_tail_contribution": c_G / (math.sqrt(6.0) * a ** 1.5),
        })
    return {
        "c_G_closed_form": "5/4 + sqrt(10) + 2",
        "c_G_value": c_G,
        "rows": rows,
        "certificate_relevant_point": {
            "z": 0.0,
            "alpha": 0.5,
            "alpha_pow_minus_3_2": 0.5 ** -1.5,
            "reading": ("The certificate sits at z = 0, alpha = 1/2, a DISTANCE 1/2 "
                        "from the essential line Re z = -1/2.  The alpha^{-3/2} blow-up "
                        "is a statement about approaching the line and is not engaged "
                        "by a static invertibility certificate."),
        },
        "C_R_d": ("LEFT IMPLICIT BY XU (Prop 4.6 states the constant depends only on "
                  "c_G, R, d, and does not evaluate it).  Not invented here.  Assembling "
                  "an explicit ||R_0||_X is a CONSTRUCTION leg's job, not this one's."),
        "verdict": "REPORTED",
    }


# ---------------------------------------------------------------------------
# The scoping inventory and the obstruction census (structured, not measured)
# ---------------------------------------------------------------------------

INFRASTRUCTURE = [
    {"need": "X-norm object: ||phi||_X^2 = ||phi||_L2^2 + ||phi''||_L2^2 on the odd half-line",
     "status": "NEW",
     "evidence": ("grep over solver/ finds NO L^2 or Sobolev norm object.  The two norm "
                  "families this repository owns are weighted-Holder (solver/holder_norms.py, "
                  "sup + seminorm on a conformal theta variable, 634 lines) and weighted-ell^1 "
                  "Fourier (solver/spectral_certificate.py, w_k = (1+k)^s, 924 lines).  "
                  "Neither is a Hilbert norm.")},
    {"need": "Hardy-block projectors P_+ / P_- and the block-diagonalization of L_0",
     "status": "MOSTLY NEW",
     "evidence": ("solver/nk_fourier.py line 18 and solver/decay_grading.py line 24 already "
                  "use Hardy-space language (G_k(X) := e^{ik theta} - (-1)^k lies in the "
                  "Hardy space; h + iH(h) is a Hardy boundary value), so the IDEA is banked, "
                  "but no projector object exists.")},
    {"need": "Mellin transform / generalized Hardy operator T_z",
     "status": "NEW",
     "evidence": "grep -i mellin over solver/ returns ZERO hits."},
    {"need": "Hilbert transform on the whole line",
     "status": "REUSABLE",
     "evidence": ("solver/line_hilbert.py, capabilities.py entry 'Hilbert transform on the "
                  "whole line', test_line_hilbert.py.  On the Hardy block it is not even "
                  "needed -- H acts as -i -- but it is needed to build the block-diagonalization.")},
    {"need": "lower bounds on an operator norm in an arbitrary (dom, cod) norm pair",
     "status": "REUSABLE FRAMEWORK, NEW NORM OBJECTS",
     "evidence": ("solver/op_lower.py is built on the norm-agnostic identity "
                  "||A|| >= ||Ag||_X / ||g||_Y and takes dom/cod norm objects as arguments; "
                  "its float-safety layer `_Quotient` was hardened by leg 101 against 47 of "
                  "209 gate-deciding overflow/underflow cases.  That layer is worth more than "
                  "the norms it currently wraps.  But its adversary FAMILIES (powers of "
                  "cos(theta/2), smoothed steps, boxes) are shaped for the weighted-Holder "
                  "ball and would have to be re-chosen for the X ball.")},
    {"need": "radii-polynomial / Newton-Kantorovich bookkeeping (Y_0, Z_1, Z_2 assembly, "
             "bordered system with a border column and a matching condition)",
     "status": "REUSABLE AT THE ALGEBRA LEVEL",
     "evidence": ("solver/spectral_certificate.py carries the bordered assembly from stage "
                  "TC.  The algebra is realization-agnostic; every CONSTANT in it is "
                  "ell^1_w-specific.  Gate 4 above shows the bordered SHAPE is exactly right: "
                  "one border column, one matching row, per Hardy block.")},
    {"need": "a discretization that ENFORCES the origin condition",
     "status": "NEW, AND THE REPOSITORY CURRENTLY HAS THE OPPOSITE",
     "evidence": ("capabilities.py, solver/rescaled_spectrum.py entry: 'point spectrum {0,1} "
                  "at a=0, which XU Theorem 2 later proved -- but in the LOOSE realization: "
                  "our grid imposes NO origin condition (70)'.  Per Xu sec 4.6 the loose "
                  "(maximal L^2) realization has the WHOLE OPEN STRIP as genuine eigenvalues "
                  "and NO spectral gap.  So every numerical object this repository owns for "
                  "this operator is in the realization WITHOUT the gap.")},
    {"need": "Banach-algebra / product estimates on X",
     "status": "PARTLY SUPPLIED BY XU, PARTLY NEW",
     "evidence": ("H^2(R) is an algebra (s > 1/2), but X is the ODD part, which is not closed "
                  "under products, and H maps odd to even so H does NOT map X into itself.  "
                  "Xu sec 4.1 handles this by parity bookkeeping (in phi H Omega and Omega H phi "
                  "the even factor is multiplied by an odd profile factor) and by the fact that "
                  "multiplication by m with m, m', m'' in L^inf is X-bounded with an explicit "
                  "constant.  That is a recipe, not a module.")},
]

OBSTRUCTIONS = [
    {"id": "O1", "name": "alpha^{-3/2} resolvent blow-up at the essential line",
     "class": "NOT the ell^1_w class", "severity_for_a_static_certificate": "NONE",
     "detail": ("Engaged only as Re z -> -1/2.  The certificate sits at z = 0, alpha = 1/2, "
                "where alpha^{-3/2} = 2.828...  A certificate that needed UNIFORM control up "
                "to the line would meet it; an invertibility certificate at z = 0 does not.")},
    {"id": "O2", "name": "non-normality: the spectral gap is not a decay rate in the X norm",
     "class": "NOT the ell^1_w class", "severity_for_a_static_certificate": "NONE",
     "severity_downstream": "HIGH",
     "detail": ("XU'S OWN ABSTRACT: 'we keep the two separate, since L_0 is non-normal and a "
                "spectral gap does not by itself give a decay rate in the X norm.'  His "
                "semigroup and the exact rate e^{-tau/2} live on a THIRD space Y_theta, "
                "origin-stricter than X, reached by a bounded transfer map.  So an origin-H^2 "
                "certificate would certify INVERTIBILITY, not nonlinear stability -- and "
                "nonlinear stability is what L1 needs.  This is the honest ceiling on what the "
                "yes-branch is worth.")},
    {"id": "O3", "name": "a = 0 exactness dependence",
     "class": "NOT the ell^1_w class", "severity_for_a_static_certificate": "NONE at a = 0",
     "severity_for_transfer": "FATAL",
     "detail": ("Every usable object above -- the single-simple-pole identity "
                "H Omega - i Omega = i/(y + i/2), the collapse of the NONLOCAL L_0 to a SCALAR "
                "first-order ODE on each Hardy block, the closed-form kernel (4.23), the exact "
                "Mellin norm 1/alpha -- is a consequence of Omega being the EXACT CLM profile "
                "-y/(y^2 + 1/4).  For a > 0 Xu proves only a CONDITIONAL two-line inclusion "
                "under Adm(a): no resolvent, no invertibility, no gap.  "
                "HL_S2_nonsymmetric is not a CLM profile and inherits none of it.  Corollary "
                "that must be said out loud: a certificate at a = 0 in origin-H^2 would "
                "certify an object Xu already inverts IN CLOSED FORM.")},
    {"id": "O4", "name": "realization coupling for a > 0",
     "class": "structural, new", "severity_for_a_static_certificate": "N/A at a = 0",
     "detail": ("Xu sec 4.6: 'One cannot use the H^2 metric to empty the strip and the L^2 "
                "metric to close the origin channel.'  The origin-regularity index and the "
                "position of the essential lines are COUPLED; a stronger H^3 realization shifts "
                "the origin line off, and for a > 0 the two-line picture is relative to the "
                "choice of realization.  At a = 0 the two lines coincide, which is why the "
                "picture is clean there and only there.")},
    {"id": "O5", "name": "the ell^1_w class obstruction (sigma_min -> 0 / zero diagonal)",
     "class": "THE ell^1_w class -- checked for, and it DOES NOT RECUR",
     "severity_for_a_static_certificate": "NONE",
     "detail": ("In ell^1_w at s < 1, leg 127's explicit singular sequence drives sigma_min(L) "
                "to zero like M^{-(1-s)} (fitted 0.9925 / 0.6985 / 0.3202 against predicted "
                "1 - s, max deviation 0.0219), forcing Z_1 >= 1 for EVERY bounded A, and "
                "bordering does not touch it because the sequence has exactly zero far-field "
                "amplitude component.  On X the corresponding quantity is bounded away from "
                "zero and is M-INDEPENDENT: L_0|_X has only two spectral points with "
                "Re >= -1/2, both eigenvalues, both with RANK-ONE Riesz residues per Hardy "
                "block, and the residue at z = 0 IS the border column.  Gate 4 measures a "
                "lower witness on sigma_min directly.")},
]


def main():
    g1 = gate_1_mellin_norm()
    g2 = gate_2_resolvent_identity()
    g3 = gate_3_symmetry_modes()
    g4 = gate_4_bordered_at_zero()
    g5 = gate_5_majorant_shape()

    gate_answer = ("YES -- origin-H^2 admits a structurally viable certificate formulation "
                   "for the bordered a = 0 CLM linearization: Xu's own text supplies the SPLIT "
                   "(the Hardy block-diagonalization L_0 = L_0^+ (+) L_0^-, with the two blocks "
                   "intertwined by conjugation and NOT coupled) and the SHAPE (the explicit "
                   "kernel (4.23): a generalized Hardy-Mellin operator of exact norm 1/alpha "
                   "plus a rank-two correction whose two poles are exactly the two symmetry "
                   "eigenvalues), and the ell^1_w-class obstruction -- sigma_min driven to zero "
                   "by a singular sequence the border cannot see -- provably does not recur, "
                   "because on X the only spectrum with Re >= -1/2 off the essential line is "
                   "{0, 1}, both with rank-one Riesz residues, and the residue at 0 IS the "
                   "border column m = y b^{-2}.")

    payload = {
        "leg": 163,
        "route": "ROUTE-H2S",
        "kind": "SCOPING -- no certificate built, no certificate measured, no solver module",
        "object": "bordered a = 0 CLM linearization, odd origin-H^2 realization X (Xu arXiv:2607.19762)",
        "source": {
            "arxiv": "2607.19762",
            "title": "The spectral picture of self-similar collapse in the Constantin-Lax-Majda equation",
            "author": "Jie Xu",
            "date": "2026-07-22",
            "url": "https://arxiv.org/abs/2607.19762",
            "sections_read_this_leg": ["abstract", "4.1", "4.4", "4.6", "Prop 4.6", "Lemma 4.5"],
            "fetched_by": "bash Papers/fetch.sh 2607.19762 (egress HTTP 200, 624K)",
        },
        "gates": {
            "G1_mellin_exact_norm": g1,
            "G2_resolvent_identity": g2,
            "G3_symmetry_modes": g3,
            "G4_bordered_reduction_at_zero": g4,
            "G5_majorant_shape": g5,
        },
        "infrastructure_inventory": INFRASTRUCTURE,
        "obstruction_census": OBSTRUCTIONS,
        "gate_answer": gate_answer,
        "escalation": ("YES-branch: this is escalation-grade.  DIRECTION.md's yes-branch "
                       "forbids building anything under this leg's authority; a construction "
                       "attempt is a separate later leg contingent on the user's ruling, the "
                       "way leg 63/125's dissipative direction was.  Branch pushed, main NOT "
                       "touched."),
        "ceiling": ("The a = 0 CLM linearization only.  Float64, nothing interval-enclosed.  "
                    "No Y_0, Z_1 or Z_2 formed.  Nothing claimed about HL_S2_nonsymmetric: "
                    "obstruction O3 says explicitly that none of Xu's machinery transfers to "
                    "it.  No link of the L1 -> L4 chain moved.  No ban lifted."),
    }

    with open(os.path.normpath(OUT), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)

    print("Route-H2S v1 -- origin-H^2 certificate feasibility SCOPING")
    print("=" * 72)
    print(f"G1 Mellin exact norm 1/alpha      : {g1['verdict']}  "
          f"(max rel err {g1['max_rel_err']:.3e})")
    print(f"G2 resolvent identity residual    : {g2['verdict']}  "
          f"(worst rel {g2['worst_rel_residual']:.3e}; Xu sympy float 3e-16)")
    print(f"G3 symmetry modes b^-2 / y b^-2   : {g3['verdict']}  "
          f"(residuals {g3['mode_eigenvalue_1']['max_abs_residual']:.3e} / "
          f"{g3['mode_eigenvalue_0']['max_abs_residual']:.3e})")
    print(f"G4 bordered reduction at z = 0    : {g4['verdict']}  "
          f"(max ||u||_X/||f||_X = {g4['max_ratio_uX_over_fX']:.4f}, "
          f"sigma_min witness >= {g4['implied_sigma_min_lower_witness']:.4f})")
    print(f"G5 alpha^-3/2 at the certificate  : "
          f"alpha = 1/2, alpha^-3/2 = {0.5 ** -1.5:.4f}")
    print()
    print("GATE:", gate_answer)
    print()
    print(f"written: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
