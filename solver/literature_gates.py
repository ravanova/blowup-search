"""ROUTE J v1: the PRIMARY-SOURCE pass -- published results as executable gates.

--------------------------------------------------------------------------
WHY THIS MODULE EXISTS
--------------------------------------------------------------------------
For six legs the literature check was blocked on network egress, and five passes of
`LITERATURE_CHECK.md` were written anyway -- all of them SEARCH-LEVEL, none of them
against a primary source.  Egress opened.  The papers are now read, and this module is
what a read paper should leave behind: not a paragraph saying "we checked", but CODE
that re-derives the published number from the published equations and compares it to
ours, so the check survives the session that made it.

The discipline is the project's own (banked lesson 3, "build the same object twice"),
turned outward.  A literature claim we cannot re-run is exactly as durable as a rendered
figure we looked at once -- which is to say, not (lesson from Route-I: LOOKING AT AN
ARTIFACT IS NOT VERIFICATION).

--------------------------------------------------------------------------
THE FOUR SOURCES THAT DO THE WORK, AND WHAT EACH ONE SETTLES
--------------------------------------------------------------------------
**[ALS] arXiv:2207.07548** -- Ambrose, Lushnikov, Siegel, Silantyev, *Global existence
and singularity formation for the generalized Constantin-Lax-Majda equation with
dissipation: the real line vs. periodic domains*, Nonlinearity (2022).

  Their equation is ours with sigma = 2s:  omega_t + a u omega_x = omega H(omega)
  - nu Lambda^sigma omega, and their similarity convention is

      omega = tau^{-beta} f(x/tau^{alpha_ALS}),   tau = t_c - t,

  so **alpha_ALS is our beta (the LENGTH exponent), and our alpha is 1/alpha_ALS.**
  Getting that dictionary wrong is the only way to misread this paper, and every
  comparison below states which side it is on.

  * §5.1 gives Schochet's a = 0, sigma = 2 solution WITH A CORRECTION to the 1986
    constant, and reads it as self-similar with **alpha_ALS = 1, beta = 2**.
  * §5.3, eqs (57)-(58), gives the a = 0, sigma = 1 pole solution.  **This is
    Route-H's closed form (E), exactly** -- see `route_h_E_as_als`.
  * §5.2, eqs (49)-(50), gives the a = 1/2, sigma = 1 system whose collapse has
    **alpha_ALS = 1/3**, i.e. our **alpha(1/2) = 3, EXACTLY** -- see `a_half_branch`.
  * §8 explicitly leaves the critical-sigma question OPEN ("whether sigma = 1 is the
    optimal lower bound ... left for future work").  **The s_c formula is NOT here.**

**[XU] arXiv:2607.19762** -- Xu, *The spectral picture of self-similar collapse in the
Constantin-Lax-Majda equation* (22 Jul 2026).  This is the one that pre-empts us.

  * §6.1 eq (6.3) records **s*(a) = 1/c_l(a)**, "the scaling-critical dissipation
    exponent", from exactly our argument (dissipation enters the rescaled equation with
    coefficient e^{-gamma tau}, gamma = 1 - s c_l).  In our gauge that is **s_c = alpha/2
    -- Route-F v1's headline, posted eleven days before our leg.**
  * Theorem 2: the full point spectrum of the CLM linearization on the odd
    origin-H^2 realization is **exactly {0, 1}**, the symmetry modes, rigorously, in our
    own normalization Omega = -y/(y^2 + 1/4).  **That is Route-E v1's negative.**
  * **Proposition 2, the realization dichotomy** -- the one to actually carry forward.
    The essential-spectrum SMEAR that grids WITHOUT AN ORIGIN CONDITION place inside the
    strip is the faithful spectrum of the MAXIMAL L^2 realization; imposing the single
    second-derivative condition at the origin removes the whole family.  Route-E measured
    a continuum; Route-I counted 141 unstable directions out of 144.  **Both are
    realization-dependent, and our discretization is the loose realization.**
  * Table 1 is the branch c_l(a).  `XU_TABLE1` below is it, transcribed.

**[CH] arXiv:2210.07191** -- Chen & Hou, *Stable nearly self-similar blowup of the 2D
Boussinesq and 3D Euler equations with smooth data I*.  Pins Route-G's anchor:
`c_l/c_omega ~= -2.9205600`, i.e. **beta = 2.92056**, quoted there as close to Hou-Luo.

**[HTW] arXiv:2209.08232** -- Huang, Tong, Wei, *On self-similar finite-time blowups of
the De Gregorio model on the real line*.  Proposition 2.3: any H^1 solution of the
profile equation with c_omega/c_l > 0 **must be compactly supported**.  Note the scope:
this is **De Gregorio, a = 1**, where non-degeneracy forces c_l = c_omega.  Route-D
v12/v13's finite support is the same phenomenon in a regime this proposition does not
cover, and the a-dependence (X_c the zero of c + aU, algebraic order 1/a) is not here.

--------------------------------------------------------------------------
WHAT IS ACTUALLY VERIFIED HERE, AND WHAT IS MERELY TRANSCRIBED
--------------------------------------------------------------------------
Transcription is a place errors hide, so the two are kept apart in the code and in the
JSON.  **VERIFIED** means this module re-derives the number from the published equations
and it agrees:

  J1  Schochet's constant.  `schochet_pde_residual` evaluates the residual of the
      complex Burgers equation (36) on the exact pole ansatz (37)-(41) with ANALYTIC
      derivatives -- no differencing.  ALS's corrected K_pm = 24(3 +- sqrt 6) returns
      ~1e-16; Schochet's original 12(6 +- sqrt 6) returns ~1e-2.  **We independently
      confirm a published correction to a 1986 CPAM paper.**
  J2  Route-H's (E) against ALS (57)-(58), pointwise, under an explicit parameter map.
  J3  alpha(1/2) = 3 by integrating ALS (49)-(50) -- a system that shares no grid, no
      basis and no code with our compactified Newton solve.
  J4  the SUPERCRITICAL balance, which nothing in this project had: above s_c the
      self-similar exponents are set by dissipation-vs-stretching, beta = sigma *
      alpha_ALS, and the TIME DERIVATIVE IS SUBDOMINANT.  Schochet is the witness
      (sigma = 2, alpha_ALS = 1, beta = 2), and the mechanism is a **double pole whose
      residue B = -12 i nu is proportional to nu and vanishes inviscidly.**

**TRANSCRIBED, not verified:** `XU_TABLE1`, `CHEN_HOU_*`, and every scope note.  Those
are read off a PDF by a human-equivalent process and are exactly as good as that.

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* Not rigorous.  Float64, no intervals.  A residual of 1e-16 says the constant satisfies
  the equation to rounding, not that the solution exists in any theorem's sense.
* Not a full reading.  Tier 2 and Tier 3 of `Papers/MANIFEST.md` are fetched and
  extracted but only Tier 1 is read closely; `LITERATURE_CHECK.md` sixth pass says which.
* **Not a survival claim for anything.**  Where a paper pre-empts us this module records
  the pre-emption; it does not look for a way to keep the claim.
"""

import numpy as np

# --------------------------------------------------------------------------
# provenance
# --------------------------------------------------------------------------
PRIMARY_SOURCES = {
    "2207.07548": {
        "tag": "ALS",
        "authors": "Ambrose, Lushnikov, Siegel, Silantyev",
        "title": ("Global existence and singularity formation for the generalized "
                  "Constantin-Lax-Majda equation with dissipation: "
                  "the real line vs. periodic domains"),
        "venue": "Nonlinearity (arXiv v1, 15 Jul 2022)",
        "read": "full text; sections 1, 5, 7.3, 8 closely",
        "gates": ["Route-H closed form (E)", "alpha(1/2) = 3",
                  "the supercritical balance", "Route-F s_c (NEGATIVE: not here)"],
    },
    "2607.19762": {
        "tag": "XU",
        "authors": "Xu",
        "title": ("The spectral picture of self-similar collapse in the "
                  "Constantin-Lax-Majda equation"),
        "venue": "arXiv, 22 Jul 2026",
        "read": "full text; abstract, sections 2, 3, 6, 7 closely",
        "gates": ["Route-F s_c = alpha/2 (PRE-EMPTS)", "Route-E point spectrum",
                  "Route-E/I essential spectrum (RE-CLASSIFIES)", "alpha(a) branch, a_c"],
    },
    "2210.07191": {
        "tag": "CH",
        "authors": "Chen, Hou",
        "title": ("Stable nearly self-similar blowup of the 2D Boussinesq and "
                  "3D Euler equations with smooth data I: Analysis"),
        "venue": "arXiv v3, 9 May 2023",
        "read": "abstract, section 1, the profile section around eq. for c_l/c_omega",
        "gates": ["Route-G beta anchor", "the L1->L2 port's formulation"],
    },
    "2209.08232": {
        "tag": "HTW",
        "authors": "Huang, Tong, Wei",
        "title": "On self-similar finite-time blowups of the De Gregorio model on the real line",
        "venue": "arXiv, 17 Sep 2022",
        "read": "sections 1, 2 closely",
        "gates": ["Route-D v12/v13 finite support (PARTIAL, scope differs)"],
    },
}

# --------------------------------------------------------------------------
# the exponent dictionary -- get this wrong and every comparison below inverts
# --------------------------------------------------------------------------
#   ALS / XU:   omega ~ tau^{-beta} f(x / tau^{c_l}),  c_l == alpha_ALS
#   ours:       omega ~ tau^{-1},   L ~ tau^{beta_ours},   alpha_ours := 1 / beta_ours
#   hence       alpha_ours == 1 / c_l ,  and with sigma = 2 s,
#               s_c(ours) = alpha_ours / 2 == s*(XU) / 2 .
def ours_alpha_from_cl(c_l):
    """Their focusing exponent c_l -> our far-field/decay exponent alpha."""
    return 1.0 / float(c_l)


def xu_s_star(c_l):
    """[XU] eq (6.3): s*(a) = 1/c_l(a), in THEIR Lambda^s convention."""
    return 1.0 / float(c_l)


def ours_s_c(alpha):
    """Route-F's s_c = alpha/2, in OUR (-Delta)^s convention.  s_c = s*/2."""
    return 0.5 * float(alpha)


# --------------------------------------------------------------------------
# [ALS] section 5.1 -- Schochet, a = 0, sigma = 2 (the SUPERCRITICAL witness)
# --------------------------------------------------------------------------
def schochet_K(sign=+1, corrected=True):
    """K_pm.  ALS: 24(3 +- sqrt 6).  Schochet 1986 as printed: 12(6 +- sqrt 6).

    ALS say in §5.1 that they are correcting the 1986 value.  `schochet_pde_residual`
    is how we find out which one solves the equation, rather than which one is in print.
    """
    r = np.sqrt(6.0)
    return (24.0 * (3.0 + sign * r)) if corrected else (12.0 * (6.0 + sign * r))


def schochet_omega_plus(x, t, x10, x20, nu, K):
    """ALS (37)-(41): omega_+ and its EXACT t- and xx-derivatives.

    Returns (omega_+, d_t omega_+, d_xx omega_+).  Everything is differentiated in
    closed form -- there is no finite differencing anywhere, so the residual below
    tests the SOLUTION and not a discretization of it (same discipline as Route-H's
    `exact_a0_residual`).
    """
    x = np.asarray(x, complex)
    d0 = complex(x10) - complex(x20)
    s0 = complex(x10) + complex(x20)
    d = np.sqrt(d0 ** 2 - (5.0 / 3.0) * K * nu * t + 0j)      # (43) via (40),(41)
    dd = -(5.0 / 6.0) * K * nu / d                            # d/dt of d
    x1, x2 = 0.5 * (s0 + d), 0.5 * (s0 - d)
    A = -K * nu * 1j / d                                      # (38)
    Ad = K * nu * 1j * dd / d ** 2
    B = -12.0 * nu * 1j                                       # (39): B = D, C = -A
    w = wt = wxx = 0.0
    for Aq, Aqd, xq, xqd in ((A, Ad, x1, 0.5 * dd), (-A, -Ad, x2, -0.5 * dd)):
        u = x - xq
        w += Aq / u + B / u ** 2
        wt += Aqd / u + Aq * xqd / u ** 2 + 2.0 * B * xqd / u ** 3
        wxx += 2.0 * Aq / u ** 3 + 6.0 * B / u ** 4
    return 0.5 * w, 0.5 * wt, 0.5 * wxx


def schochet_pde_residual(K, nu=1.0, t=0.01, x10=-1j, x20=-2j, pts=None):
    """Relative residual of ALS (36):  omega_+t + i omega_+^2 - nu omega_+xx = 0.

    Evaluated at complex points off the poles.  Reported as a MAGNITUDE relative to
    |omega_+^2| -- never as a boolean (banked lesson 58).
    """
    if pts is None:
        pts = np.array([0.3 + 0.5j, -0.7 + 1.2j, 1.9 + 0.2j, 0.05 + 3.0j])
    w, wt, wxx = schochet_omega_plus(pts, t, x10, x20, nu, K)
    r = wt + 1j * w ** 2 - nu * wxx
    return float(np.max(np.abs(r)) / (np.max(np.abs(w ** 2)) + 1e-300))


def schochet_blowup_time(x10, x20, nu, K):
    """ALS (44): t_c = -(12/5) x1(0) x2(0) / (K nu), for poles on the -i axis."""
    return float(np.real(-(12.0 / 5.0) * complex(x10) * complex(x20) / (K * nu)))


def schochet_similarity_profile(xi, x10, x20, nu, K):
    """ALS (45): the asymptotic profile, omega ~= -24 v~ xi / (xi^2 + v~^2)^2 / tau^2.

    Returns (profile_values, v_tilde).  Note the exponents this carries: **beta = 2**
    (the prefactor is tau^{-2}) with **alpha_ALS = 1** (xi = x/tau).
    """
    v = -5.0j / 12.0 * K * nu / (complex(x10) + complex(x20))
    xi = np.asarray(xi, float)
    return -24.0 * np.real(v) * xi / (xi ** 2 + np.real(v) ** 2) ** 2, float(np.real(v))


def rescaled_collapse(x10, x20, nu, K, taus, xi_max=6.0, n=801):
    """omega(x,t) * tau^beta on the similarity grid xi = x/tau, for a ladder of tau.

    The point of this function is that beta is an INPUT, not an output: run it at
    beta = 2 and the curves collapse, run it at beta = 1 and they do not.  That is how
    the supercritical exponent gets MEASURED rather than quoted.
    """
    tc = schochet_blowup_time(x10, x20, nu, K)
    xi = np.linspace(-xi_max, xi_max, n)
    out = {}
    for tau in taus:
        x = xi * tau
        w, _, _ = schochet_omega_plus(x, tc - tau, x10, x20, nu, K)
        out[float(tau)] = 2.0 * np.real(w)        # omega = 2 Re omega_+
    return xi, out, tc


def collapse_spread(xi, curves, beta):
    """Max spread across the tau-ladder of tau^beta * omega, relative to the profile.

    The refusal predicate for "did it collapse?": a MAGNITUDE, so beta = 1 and beta = 2
    can be compared on the same axis instead of one of them being declared correct.
    """
    taus = sorted(curves)
    stack = np.array([curves[t] * t ** beta for t in taus])
    scale = float(np.max(np.abs(stack))) + 1e-300
    return float(np.max(np.max(stack, axis=0) - np.min(stack, axis=0)) / scale)


SUPERCRITICAL_BALANCE = """\
omega ~ tau^-beta f(x tau^-alpha_ALS) in omega_t + ... = omega H omega - nu Lambda^sigma omega:
    omega_t              ~ tau^{-beta - 1}
    omega H omega        ~ tau^{-2 beta}
    nu Lambda^sigma omega ~ tau^{-beta - sigma alpha_ALS}
SUBcritical (sigma < 1/alpha_ALS): omega_t balances stretching  =>  beta = 1, dissipation
    is a lower-order correction.  This is the regime Routes E/F/G/H/I all live in.
SUPERcritical (sigma > 1/alpha_ALS): DISSIPATION balances stretching  =>  beta = sigma
    alpha_ALS, and **omega_t is subdominant** (tau^{-beta-1} vs tau^{-2 beta}, beta > 1).
Schochet is the witness: sigma = 2, alpha_ALS = 1  =>  beta = 2, matching ALS (45).
The mechanism is the DOUBLE POLE with residue B = -12 i nu: it is proportional to nu, so
it is absent inviscidly, and it is what carries the tau^{-2}."""


def supercritical_beta(sigma, alpha_als):
    """beta = sigma * alpha_ALS, the dissipation-vs-stretching balance."""
    return float(sigma) * float(alpha_als)


# --------------------------------------------------------------------------
# [ALS] section 5.3 -- a = 0, sigma = 1: this IS Route-H's (E)
# --------------------------------------------------------------------------
def als_a0_sigma1(x, t, w_m1_0, vc0, nu):
    """ALS (57)-(58).  omega_{-1} is CONSTANT in t; v_c(t) = (omega_{-1}(0) + nu) t + v_c(0)."""
    x = np.asarray(x, float)
    w0 = complex(w_m1_0)
    vc = (w0 + nu) * t + complex(vc0)
    return np.real(w0 / (x - 1j * vc) + np.conj(w0) / (x + 1j * np.conj(vc)))


def als_a0_sigma1_tc(w_m1_0, vc0, nu):
    """ALS (59): t_c = -Re[v_c(0)] / (Re[omega_{-1}(0)] + nu).  Blow-up iff Re w < -nu."""
    den = np.real(complex(w_m1_0)) + nu
    return float("inf") if den >= 0 else float(-np.real(complex(vc0)) / den)


def route_h_E_as_als(mu0, nu, T):
    """THE PARAMETER MAP.  Route-H's (E) is ALS (57)-(58) with these constants.

    Route-H wrote, for kappa = nu/mu_0,
        omega(x,t) = -2 (1 + mu_0) kappa x / (kappa^2 (T-t)^2 + x^2) .
    Splitting into partial fractions gives a c.c. pair of SIMPLE poles at
    x = +- i kappa (T-t), i.e. exactly (57) with

        omega_{-1}(0) = -(1 + mu_0) kappa   (real, < -nu, so ALS's blow-up branch)
        v_c(0)        = kappa T .

    And ALS's evolution law is then an identity rather than an assumption:
        dv_c/dt = omega_{-1}(0) + nu = -(1+mu_0) nu/mu_0 + nu = -nu/mu_0 = -kappa ,
    which is what (E) has; and (59) returns t_c = -kappa T / (-kappa) = T.
    """
    kappa = float(nu) / float(mu0)
    return {"w_m1_0": -(1.0 + float(mu0)) * kappa, "vc0": kappa * float(T),
            "kappa": kappa,
            "dvc_dt_from_als": -(1.0 + float(mu0)) * kappa + float(nu),
            "dvc_dt_from_E": -kappa}


# --------------------------------------------------------------------------
# [ALS] section 5.2 -- a = 1/2, sigma = 1: alpha(1/2) = 3, EXACTLY
# --------------------------------------------------------------------------
def _a_half_rhs(u, y, nu):
    """ALS (49)-(50) reparametrised by u = log v_c, which is what makes v_c -> 0 stable.

        dv_c/dt = nu - Omega/4 ,   dOmega/dt = (Omega/v_c)(Omega/2 - 1),  Omega = w_{-2}/v_c
      =>  dOmega/du = Omega (Omega/2 - 1) / (nu - Omega/4)
          dtau/du   = v_c / (Omega/4 - nu) ,    tau := t_c - t .

    Integrating in t instead is what the first attempt did, and it dies: dt underflows
    against an O(1) elapsed time long before v_c reaches the asymptotic regime, and the
    exponent comes back NaN.  The variable, not the time (banked lesson 57's cousin).
    """
    Om, _ = y
    return np.array([Om * (0.5 * Om - 1.0) / (nu - 0.25 * Om),
                     np.exp(u) / (0.25 * Om - nu)])


def a_half_branch(Om0=10.0, nu=1.0, u0=0.0, u1=-34.0, n=200_000):
    """Integrate ALS (49)-(50) into the collapse and MEASURE c_l = d log v_c/d log tau.

    Om0 must exceed 4 for v_c to be decreasing (ALS: blow-up needs Omega(0) > 2, and
    v_c turns around at Omega = 4).  Returns the full trajectory plus the ladder of
    local exponents, with `tau_floor_rung` marking where tau stops being resolvable
    against the accumulated quadrature -- those rungs are REFUSED, not averaged in.
    """
    h = (u1 - u0) / n
    y = np.array([float(Om0), 0.0])
    U = np.empty(n + 1)
    Y = np.empty((n + 1, 2))
    U[0], Y[0] = u0, y
    u = u0
    for i in range(n):
        k1 = _a_half_rhs(u, y, nu)
        k2 = _a_half_rhs(u + 0.5 * h, y + 0.5 * h * k1, nu)
        k3 = _a_half_rhs(u + 0.5 * h, y + 0.5 * h * k2, nu)
        k4 = _a_half_rhs(u + h, y + h * k3, nu)
        y = y + h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        u += h
        U[i + 1], Y[i + 1] = u, y
    Om, S = Y[:, 0], Y[:, 1]
    tau = S - S[-1]                       # t_c - t, ->0 at the end of the run
    ok = tau > 0
    c_l = np.full_like(U, np.nan)
    c_l[ok] = np.gradient(U[ok], np.log(tau[ok]))
    # THE REFUSAL PREDICATE, and the first version of it was WRONG.  tau > floor lets
    # through rungs where tau itself is still representable but its INCREMENT is not --
    # and the local exponent is a difference quotient, so what has to survive is
    # d tau, not tau.  With tau > 1e3 eps max|S| the ladder read c_l = 0.222 at the
    # deepest "resolved" rung and 0.33333 in the middle: a turnover that the loose gate
    # did not catch and that no threshold on tau can catch, because tau is fine there.
    # Gate the QUANTITY THE MEASUREMENT DIVIDES BY (banked lesson 57, one level down).
    eps_S = np.finfo(float).eps * float(np.max(np.abs(S)))
    dtau = np.full_like(tau, np.inf)
    dtau[1:-1] = np.abs(tau[2:] - tau[:-2])
    resolved = ok & (dtau > 1e3 * eps_S)
    return {"u": U, "log_vc": U, "Omega": Om, "tau": tau, "dtau": dtau,
            "c_l_local": c_l, "resolved": resolved,
            "dtau_floor": float(1e3 * eps_S), "eps_S": float(eps_S)}


def a_half_verdict(br, frac=0.9):
    """The measured c_l at the deepest RESOLVED rung, against the exact 1/3.

    `frac` selects how far down the resolved ladder to read; the refusal is on
    `resolved`, so a rung that has fallen through the tau floor can never be quoted.
    """
    idx = np.flatnonzero(br["resolved"])
    if idx.size < 10:
        return {"refused": True, "reason": "fewer than 10 resolved rungs"}
    i = idx[int(frac * (idx.size - 1))]
    cl = float(br["c_l_local"][i])
    # Omega ~ v_c^{-2} is the independent structural check on the same trajectory
    j0, j1 = idx[int(0.4 * idx.size)], idx[int(0.85 * idx.size)]
    slope = float((np.log(br["Omega"][j1]) - np.log(br["Omega"][j0]))
                  / (br["log_vc"][j1] - br["log_vc"][j0]))
    return {"refused": False, "c_l": cl, "c_l_exact": 1.0 / 3.0,
            "c_l_rel_err": abs(cl - 1.0 / 3.0) * 3.0,
            "alpha_ours": ours_alpha_from_cl(cl), "alpha_exact": 3.0,
            "v_c_at_read": float(np.exp(br["log_vc"][i])),
            "tau_at_read": float(br["tau"][i]),
            "dtau_at_read": float(br["dtau"][i]),
            "dlogOmega_dlogvc": slope, "dlogOmega_dlogvc_exact": -2.0,
            "n_resolved": int(idx.size), "n_total": int(br["u"].size)}


# --------------------------------------------------------------------------
# [XU] Table 1 -- TRANSCRIBED, not verified
# --------------------------------------------------------------------------
# a, c_l(a), s*(a) = 1/c_l.  Rows at a = 0.1, 0.3, 0.5, 0.65 are XU's own degree-6
# interpolations of a Delta a = 0.04 Newton branch; the rest are Newton solves.  XU's
# own accuracy statement: two-grid difference <~ 5e-4, a = 0 profile accuracy ~3e-4,
# "agrees with the high-precision branch of [LSS] to about two or three significant
# figures at nonzero a".  Compare at THAT level, not at ours.
XU_TABLE1 = [
    (0.00, 1.0000, 1.000),
    (0.10, 0.8730, 1.145),
    (0.20, 0.7474, 1.338),
    (0.30, 0.6178, 1.619),
    (0.40, 0.4809, 2.079),
    (0.50, 0.3333, 3.000),
    (0.60, 0.1691, 5.914),
    (0.65, 0.0775, 12.90),
]
# [LSS] = Lushnikov, Silantyev, Siegel, cited by both ALS and XU as the reference branch.
LSS_A_C = 0.6890665          # the published critical advection
XU_A_C_RECOMPUTED = 0.6888   # XU's own recompute; they quote 0.04% agreement
XU_S2_BOUNDARY = 0.39        # where s* crosses the ordinary Laplacian s = 2 (c_l = 1/2)

CHEN_HOU_CL_OVER_COMEGA = -2.9205600   # [CH], "very close to the one reported by Hou-Luo"
CHEN_HOU_BETA = 2.9205600              # Route-G's anchor, same number


def compare_branch(ours_rows):
    """Our (a, alpha) against XU's s*(a) = 1/c_l(a).  Returns per-row magnitudes.

    `ours_rows` is a list of dicts with keys 'a' and 'alpha' -- i.e. Route-F's F6_sc_map
    straight out of the committed JSON, so this comparison cannot drift from the data.
    """
    table = {round(a, 3): (cl, ss) for a, cl, ss in XU_TABLE1}
    rows = []
    for r in ours_rows:
        a = round(float(r["a"]), 3)
        if a not in table:
            continue
        cl, ss = table[a]
        ours = float(r["alpha"])
        rows.append({"a": a, "alpha_ours": ours, "s_star_xu": ss, "c_l_xu": cl,
                     "abs_diff": abs(ours - ss),
                     "rel_diff": abs(ours - ss) / ss,
                     "s_c_ours": ours_s_c(ours), "s_c_from_xu": 0.5 * ss})
    return rows


# --------------------------------------------------------------------------
# the ledger -- every standing novelty claim, and what the primary source did to it
# --------------------------------------------------------------------------
# verdict: PRE-EMPTED | CONFIRMED_AND_PRE-EMPTED | PARTIAL | SURVIVES | OPEN | UNSEARCHED
CLAIM_LEDGER = [
    {
        "claim": "s_c = alpha/2, the critical dissipation exponent is half the far-field decay exponent",
        "leg": "Route-F v1 (§27)", "source": "2607.19762 §6.1 eq (6.3)",
        "verdict": "PRE-EMPTED",
        "note": ("XU records s*(a) = 1/c_l(a) from the same rescaling argument, with the "
                 "same caveat that it is a formal relevance threshold and not a "
                 "blow-up/regularity threshold.  Posted 22 Jul 2026, eleven days before "
                 "Route-F v1.  Our F6 map agrees with their Table 1 row by row."),
        "survives": ("F3's cross-check -- alpha from a steady compactified solve against "
                     "dp/ds from time-dependent periodic simulation, no shared grid, basis "
                     "or fitted constant.  XU state the only quantitative validation of "
                     "their branch is the a_c endpoint, so an independent dynamical check "
                     "of the FORMULA is a thing they do not have.  That is a validation, "
                     "not a new result."),
    },
    {
        "claim": "the CLM linearization's isolated eigenvalues are only the symmetry modes",
        "leg": "Route-E v1 (§26)", "source": "2607.19762 Theorem 2",
        "verdict": "CONFIRMED_AND_PRE-EMPTED",
        "note": ("Point spectrum exactly {0,1} on the odd origin-H^2 realization, proved, "
                 "no embedded eigenvalues, in our own normalization Omega = -y/(y^2+1/4). "
                 "Our dense solve found the same thing at two points."),
        "survives": "nothing of the claim; the negative stands and is not ours.",
    },
    {
        "claim": "the non-symmetry spectrum is a CONTINUUM, so there is no eigenvalue to move (no Hopf)",
        "leg": "Route-E v1 (§26), inherited by Route-I (§30)",
        "source": "2607.19762 Proposition 2 (realization dichotomy)",
        "verdict": "PRE-EMPTED_AND_RE-CLASSIFIED",
        "note": ("The continuum we measured is the faithful spectrum of the MAXIMAL L^2 "
                 "realization; the origin-H^2 realization has none of it.  So 'continuous "
                 "spectrum' is not a property of the operator, it is a property of the "
                 "realization our discretization implements -- one WITHOUT an origin "
                 "condition, which is the loose one.  **This is the item with the largest "
                 "forward consequence: Route-I's 141-of-144 unstable directions are "
                 "counted in that same loose realization.**"),
        "survives": ("the DSS conclusion, for a different and better reason: in the tight "
                     "realization there is no continuum AND no complex pair, so there is "
                     "still nothing to bifurcate.  The lane stays shut either way."),
    },
    {
        "claim": "alpha(1/2) = 3 (twelve digits), and the odd-integer-alpha resonances",
        "leg": "Route-E v1 (§26)", "source": "2207.07548 §5.2 + XU Table 1",
        "verdict": "CONFIRMED_AND_PRE-EMPTED",
        "note": ("c_l(1/2) = 1/3 is EXACT, from the a = 1/2 pole-dynamics solution.  "
                 "Verified here by integrating ALS (49)-(50).  **And this answers Route-E's "
                 "own open question** -- why alpha = 3 is a round rational and alpha = 5 is "
                 "not: exact pole-dynamics solutions exist at a = 0 and a = 1/2 AND NOWHERE "
                 "ELSE (ALS §1, citing Lushnikov et al).  a = 0.5821792673 has no exact "
                 "solution behind it, so there is no reason for alpha = 5 to be special "
                 "beyond Lambda^5 being a finite matrix -- which is OUR instrument, not the "
                 "problem's structure."),
        "survives": "the resonance framing as an instrument note; nothing as a result.",
    },
    {
        "claim": "the alpha(a) branch and its endpoint a_c ~ 0.694",
        "leg": "Route-E v1 (§26)", "source": "XU Table 1; LSS a_c = 0.6890665",
        "verdict": "PRE-EMPTED",
        "note": ("The branch is LSS's, published.  Our a_c is 0.7% off the published value; "
                 "XU's recompute is 0.04% off.  We are the least accurate of the three and "
                 "should quote theirs."),
        "survives": "nothing.",
    },
    {
        "claim": "the closed-form viscous CLM blow-up (E) at a = 0, s = 1/2",
        "leg": "Route-H v1 (§29)", "source": "2207.07548 §5.3 eqs (57)-(58)",
        "verdict": "PRE-EMPTED",
        "note": ("Identical, pointwise, under an explicit parameter map -- verified here to "
                 "machine precision, including that ALS's t_c formula returns our T.  "
                 "Route-H already declined to claim it; that was the right call and it is "
                 "now settled rather than suspected."),
        "survives": ("its USE as a known-answer gate, which is what Route-H built it for, "
                     "and which is strictly better now that it has a citation."),
    },
    {
        "claim": "alpha_1 = 0 at a = 0: a LINE of viscous self-similar blow-ups",
        "leg": "Route-H v1 (§29)", "source": "2207.07548 §5.3 eq (61)",
        "verdict": "CONFIRMED_AND_PRE-EMPTED",
        "note": ("ALS's self-similar form (61) carries nu INSIDE the profile with the "
                 "exponents fixed at alpha_ALS = beta = 1, which is a one-parameter family "
                 "of viscous self-similar blow-ups -- our alpha_1 = 0, exactly."),
        "survives": "nothing at a = 0.  alpha_1 = +0.133683 at a = 1/2 is a different point.",
    },
    {
        "claim": "alpha_1 = +0.133683 at a = 1/2 (the marginal invariant at s = s_c = 3/2)",
        "leg": "Route-H v1 (§29)", "source": "not found in Tier 1",
        "verdict": "UNSEARCHED_AT_PRIMARY_SOURCE",
        "note": ("ALS do a = 1/2 at sigma = 0 and 1; criticality at a = 1/2 is sigma = 3, "
                 "which is not in ALS and not in XU (who stop at recording s* itself).  So "
                 "the MARGINAL case at a = 1/2 is not pre-empted by either.  It is also not "
                 "searched beyond Tier 1, and the honest label is unsearched, not novel."),
        "survives": "provisionally, pending Tier 2/3.",
    },
    {
        "claim": "finite support of the a > 0 profiles, X_c the zero of c + aU, order 1/a",
        "leg": "Route-D v12/v13", "source": "2209.08232 Proposition 2.3",
        "verdict": "PARTIAL",
        "note": ("HTW prove compact support for the DE GREGORIO model (a = 1), where "
                 "non-degeneracy forces c_l = c_omega, via the same mechanism (the profile "
                 "is proportional to u + c_omega x, and the support ends where that "
                 "vanishes).  The phenomenon and the mechanism are published.  What is not "
                 "there is the a-dependence: X_c as the zero of c + aU across a in (0, 1/2), "
                 "and the algebraic order 1/a of that zero."),
        "survives": ("the a-dependence, and the consequence we actually used it for -- that "
                     "a compactly supported profile in a GLOBAL spectral basis puts its "
                     "worst error where the codomain weight is largest.  That is a "
                     "certification-space statement, not a PDE one."),
    },
    {
        "claim": "beta = 2.92 as the 2D Boussinesq / Hou-Luo self-similar anchor",
        "leg": "Route-G v1 (§28)", "source": "2210.07191",
        "verdict": "CONFIRMED (never claimed as ours)",
        "note": "c_l/c_omega ~= -2.9205600, matching our anchor to the digits we quote.",
        "survives": "n/a -- this was always cited.",
    },
    {
        "claim": "the SUPERCRITICAL exponents: what happens for s > s_c",
        "leg": "none -- Routes F/H/I all stop at criticality",
        "source": "2207.07548 §5.1 (Schochet, corrected)",
        "verdict": "OPEN_QUESTION_ANSWERED_BY_THE_LITERATURE",
        "note": ("This is the one place reading the papers ADDED something instead of "
                 "removing it.  Above s_c the self-similar balance is dissipation against "
                 "stretching, beta = sigma alpha_ALS with omega_t SUBDOMINANT, and the "
                 "mechanism is a double pole whose residue is proportional to nu.  "
                 "Route-F's 'the scaling says which term dominates' had no second half; "
                 "this is the second half, in the one case where it is exactly solvable."),
        "survives": "n/a -- an inbound result, not a claim of ours.",
    },
    {
        "claim": "the discrete-ball trap, the weighted-l1 no-go, the elasticity discipline",
        "leg": "Route-D v3/v6", "source": "2302.12877 (Tier 2, fetched, NOT read closely)",
        "verdict": "UNSEARCHED_AT_PRIMARY_SOURCE",
        "note": ("Still the only claims with a real chance of being new, and still checked "
                 "only by search.  Tier 2 is fetched and extracted; reading it is the next "
                 "literature spend, and it is now cheap."),
        "survives": "provisionally.",
    },
]


def ledger_counts():
    """How the ledger comes out, as counts -- the headline number of this leg."""
    out = {}
    for c in CLAIM_LEDGER:
        out[c["verdict"]] = out.get(c["verdict"], 0) + 1
    return out
