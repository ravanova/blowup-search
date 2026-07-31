"""Scope of the Route-D bound programme in `a`: where the advection term lives.

Eleven Route-D legs built a space, priced it, and bounded constants in it.  Every
one of them worked at the exact `a = 0` anchor, because that is where the
known-answer gate lives -- and `a = 0` is precisely the value at which the
advection term `-a U Omega_X` is ABSENT.  Nobody checked whether the space those
legs chose can carry that term at all.  It cannot, and this module is the check.

--------------------------------------------------------------------------
(1) THE VELOCITY IS LOGARITHMICALLY DIVERGENT
--------------------------------------------------------------------------
The rescaled velocity is `U(X) = int_0^X H(Omega) dX'`.  v3 (S6) established the
far-field law `H(Omega)(X) -> (int Omega) / (pi X)`, so integrating it,

    U(X)  ->  (M / pi) log X ,      M := int Omega dX .                     (U)

There is no cancellation available: `M != 0` for every profile in this family --
the a = 0 anchor itself has `int -1/(1+X^2) = -pi`, so `M/pi -> -1`.  Measured
against `velocity_log_rate`, the fitted slope matches `M/pi` to four significant
figures at a = 0, 0.3 and 0.5.

--------------------------------------------------------------------------
(2) WHAT THAT DOES TO THE OPERATOR (the part that matters)
--------------------------------------------------------------------------
The linearization of the two-scale residual carries the advection term as

    dR2/dOmega . h  ->  - a [ (V H h) Omega_X  +  U h_X ] ,

and the two pieces behave completely differently in the decay-graded codomain
`||g||_Y = sup (1+X^2)^{(alpha+1)/2} |g|` that v3-v11 use:

  * `(V H h) Omega_X` ~ (log X) * X^{-3}, so weighted it is `X^{alpha-2} log X`
    -- DECAYS for alpha < 2, which is the whole working range.  Harmless.
  * `U h_X` ~ (log X) * X^{-alpha-1}, so weighted it is `(a |M| alpha / pi) log X`
    -- DIVERGES.  For every `a != 0`.

So **`DF` does not map the domain class into the codomain class for any a != 0**,
and neither does the residual: `Y0` is infinite in that norm too.  The eleven-leg
bound programme is `a = 0`-only.  `advection_split` measures both pieces and fits
their log rates; at a = 0 both are identically zero.

--------------------------------------------------------------------------
(3) THE FIX IS A GRADING, AND IT IS ALREADY IN THE PROJECT
--------------------------------------------------------------------------
The two-scale (traveling-wave) residual balances `Omega H(Omega)` against
`c Omega_X`, whose far field is `X^{-alpha-1}`; that is why its codomain carries
`alpha + 1`.  The ONE-scale (self-similar) residual of PHASE2_P2_NOTES section 9,

    R = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X ,

balances against `c_l X Omega_X ~ X^{-alpha}` instead, so its natural codomain
grading is `alpha` -- one power WEAKER.  One power is exactly what the log needs:
`X^{alpha} * (log X) X^{-alpha-1} = (log X)/X -> 0`.  `grading_comparison`
measures both on the same profile; the two-scale column grows and the one-scale
column falls to zero.  The constructive reading of this module is therefore not
"a != 0 is out of reach" but "**a != 0 needs the one-scale formulation**", which
this project already has a validated solver for.

--------------------------------------------------------------------------
(4) A STRUCTURAL FEATURE FOUND ON THE WAY
--------------------------------------------------------------------------
Because `U` is log-divergent and negative, the EFFECTIVE traveling-wave speed

    c_eff(X) = c + a U(X)

changes sign at a finite, grid-independent `X*(a)` (`stagnation_point`): the far
field of an `a != 0` "traveling wave" moves opposite to its core.  This is a
property of the ansatz, not of the discretization -- `X*` is stable to 1% under
refinement of both `n` and the domain radius.

--------------------------------------------------------------------------
(5) WHAT THE CROSSING TURNED OUT TO BE
--------------------------------------------------------------------------
`stagnation_point` was written here as "the effective speed reverses" -- a
property of the ansatz.  A parallel line of work (solver/finite_support.py) reads
the same crossing as something sharper and better: it is the EDGE OF SUPPORT of
the a > 0 profile, `X_c`, beyond which the profile is identically zero with an
algebraic zero of order 1/a.  That reading is the one to carry forward, and it
retro-explains a measurement in this module's own test file: for a != 0 the
Newton profile collapses to ~1e-9 by X ~ 10 while `X* = 7.16` at a = 0.3, and the
"tail" beyond it does not converge under refinement -- its sign flips between
grids.  There is no tail.  There is numerical dust past the end of the profile.
The gates here are written to depend only on the reproducible half of the
measurement (test gate 2), so they stand either way.

Plain float64 throughout.  Nothing here is interval-enclosed and nothing is
rigorous; this is a scoping measurement about which space the later, rigorous
work has to be done in.
"""

import numpy as np


def _trapz(y, x):
    return float(np.trapezoid(y, x)) if hasattr(np, "trapezoid") else float(
        np.trapz(y, x))                                            # noqa: NPY201


def profile_mass(om, X):
    """M = int Omega dX -- the constant in the far-field law (U)."""
    return _trapz(np.asarray(om, dtype=float), np.asarray(X, dtype=float))


def velocity(fam, om):
    """U(X) = int_0^X H(Omega) dX', from the family's cached operators."""
    return fam.Vmat @ (fam.Hmat @ om)


def _log_fit(X, y, lo, hi):
    """Least-squares slope of y against log X on the window [lo, hi]."""
    X = np.asarray(X, dtype=float)
    sel = (X > lo) & (X < hi)
    if sel.sum() < 8:
        return float("nan")
    return float(np.polyfit(np.log(X[sel]), np.asarray(y, dtype=float)[sel], 1)[0])


def velocity_log_rate(fam, om, lo=10.0, hi=1e3):
    """Fitted `dU/d log X` against the predicted mass rate.

    `dU/dX = H(Omega)` exactly, so `dU/d log X = X H(Omega)(X)` is an IDENTITY;
    the CONTENT of (U) is that this tends to `M / pi`.  The predictor to compare
    against is therefore the mass accumulated over the FIT WINDOW, not over the
    whole truncated domain: on the sinh grid the outermost decade is coarse (the
    same far-field under-resolution v11 found), and at a = 0.5 it moves the
    full-domain mass by 15% while the windowed mass and the fitted slope agree to
    0.3%.  Both are returned so the discrepancy is visible rather than hidden.
    """
    X = np.asarray(fam.X, dtype=float)
    U = velocity(fam, om)
    sel = np.abs(X) <= hi
    M_window = _trapz(np.asarray(om, dtype=float)[sel], X[sel])
    M_full = profile_mass(om, X)
    return {"measured": _log_fit(X, U, lo, hi),
            "predicted": float(M_window / np.pi),
            "predicted_full_domain": float(M_full / np.pi),
            "mass_window": float(M_window), "mass": float(M_full),
            "window": [float(lo), float(hi)]}


# ---------------------------------------------------------------------------
# the operator split
# ---------------------------------------------------------------------------

GRADINGS = {
    # exponent of (1+X^2)^{./2} in the codomain norm, given the domain grading
    "two_scale": lambda alpha: alpha + 1.0,   # balances c Omega_X ~ X^{-alpha-1}
    "one_scale": lambda alpha: alpha,         # balances c_l X Omega_X ~ X^{-alpha}
}


def advection_split(fam, om, a, alpha, D, grading="two_scale", h=None,
                    lo=10.0, hi=1e4):
    """The two advection pieces of DF, weighted, with their fitted log rates.

    `D` is the family's d/dX matrix (solver.profile_newton.derivative_matrix --
    note it ALREADY divides by X_rho, so do not divide again).  `h` defaults to
    the natural domain-class element f_alpha = (1+X^2)^{-alpha/2}.

    Returns the weighted profiles and slopes for
        transport piece   a * U * h_X          (the one that diverges)
        stretch piece     a * (V H h) * Omega_X (the one that does not)
    """
    X = fam.X
    h = (1.0 + X ** 2) ** (-0.5 * alpha) if h is None else np.asarray(h, float)
    w = (1.0 + X ** 2) ** (0.5 * GRADINGS[grading](alpha))
    U = velocity(fam, om)
    hX = D @ h
    omX = D @ np.asarray(om, dtype=float)
    VHh = fam.Vmat @ (fam.Hmat @ h)

    t_transport = a * np.abs(U * hX) * w
    t_stretch = a * np.abs(VHh * omX) * w
    M = profile_mass(om, X)
    return {
        "grading": grading,
        "weight_exponent": float(GRADINGS[grading](alpha)),
        "transport": t_transport, "stretch": t_stretch, "X": X,
        "transport_log_rate": _log_fit(X, t_transport, lo, hi),
        "stretch_log_rate": _log_fit(X, t_stretch, lo, hi),
        # (U) + h_X ~ -alpha X^{-alpha-1} + w ~ X^{alpha+1} give the rate below
        "transport_predicted_rate": float(a * abs(M) * alpha / np.pi)
        if grading == "two_scale" else 0.0,
        "transport_at": {float(q): float(np.interp(q, X, t_transport))
                         for q in (1e1, 1e2, 1e3, 1e4)},
        "stretch_at": {float(q): float(np.interp(q, X, t_stretch))
                       for q in (1e1, 1e2, 1e3, 1e4)},
    }


def grading_comparison(fam, om, a, alpha, D, lo=10.0, hi=1e4):
    """`advection_split` under both gradings -- the negative and its fix, side by side."""
    return {g: advection_split(fam, om, a, alpha, D, grading=g, lo=lo, hi=hi)
            for g in ("two_scale", "one_scale")}


# ---------------------------------------------------------------------------
# the stagnation point
# ---------------------------------------------------------------------------


def stagnation_point(fam, om, c, a):
    """Smallest X > 0 where the effective speed c + a U(X) changes sign.

    Returns None when there is no crossing (a = 0, where c_eff == c > 0).
    Linear interpolation between the bracketing nodes; the value is stable to ~1%
    under refinement of n and of the domain radius (test gate 4).
    """
    X, U = fam.X, velocity(fam, om)
    pos = X > 0
    Xp, eff = X[pos], (c + a * velocity(fam, om)[pos])
    s = np.sign(eff)
    idx = np.where(np.diff(s) != 0)[0]
    if idx.size == 0:
        return None
    i = int(idx[0])
    x0, x1, f0, f1 = Xp[i], Xp[i + 1], eff[i], eff[i + 1]
    return float(x0 - f0 * (x1 - x0) / (f1 - f0))
