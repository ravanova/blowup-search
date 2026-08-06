"""ROUTE V v0: the pre-committed NOVELTY GATE for stage V -- and the re-derivation that
settles it.

--------------------------------------------------------------------------
WHY THIS MODULE EXISTS
--------------------------------------------------------------------------
`plan_of_record.py` puts stage `V` (viscous survival: "does a blow-up certificate's
margin survive dissipation?") behind a gate that is a BAN, not a suggestion:

    FIRST: has anyone already done certification-under-dissipation for a self-similar
    blow-up profile?   yes -> report it, fall back to C-PILOT, do NOT spend the leg.

Leg 42 deleted seven of twelve standing novelty claims, and stage V was flagged as a
speculation of exactly that kind when it was proposed.  So the gate is asked before any
measurement is built -- and asked the way Route-J asks literature questions (§31): not
with a paragraph saying "we checked", but with CODE that re-derives the published result
from the published equations, so the check survives the session that made it.

--------------------------------------------------------------------------
THE ANSWER IS YES, AND THE PRE-EMPTING PAPER IS DAHNE-FIGUERAS
--------------------------------------------------------------------------
**[DF] arXiv:2410.05480** -- Dahne & Figueras, *Self-Similar Singular Solutions to the
Nonlinear Schroedinger and the Complex Ginzburg-Landau Equations* (Oct 2024, v2 Dec 2024).

Their equation is

    i u_t + (1 - i eps) Laplacian u + (1 + i delta) |u|^{2 sigma} u = 0            (CGL)

on R^d.  **eps is a dissipation dial**: eps = delta = 0 is the focusing NLS (conservative);
eps > 0 is the complex Ginzburg-Landau equation, in which the Laplacian acquires a
dissipative real part.  Their Zakharov ansatz

    u(x,t) = (2 kappa (T-t))^{-(1/sigma + i omega/kappa)/2} Q( |x| / sqrt(2 kappa (T-t)) )

reduces blow-up to the singular ODE (their (3))

    (1 - i eps)(Q'' + (d-1)/xi Q') + i kappa xi Q' + i (kappa/sigma) Q - omega Q
        + (1 + i delta) |Q|^{2 sigma} Q = 0,   Q'(0) = 0,  Q ~ xi^{-1/sigma - i omega/kappa}.

**What they prove is exactly the shape of stage V's question.**  Theorem 4.1: in Case I
(d = 1, sigma = 2.3) there are at least EIGHT continuous curves of self-similar singular
solutions parameterised by s in [0,1], each starting at an NLS solution (eps = 0) and
followed as eps grows -- *verified along the whole branch*, in interval arithmetic, by a
rigorous shooting method.  Theorem 4.4 does Case II (d = 3, sigma = 1) and verifies only
PARTS of the branches (their Fig. 2b: solid = verified, dotted = numerics only).

So "switch dissipation on and ask whether the certificate still closes, and where it
stops closing" is a published, rigorous, computer-assisted result from 2024 -- with
interval arithmetic this project does not have, on branches this project has not
computed.  **Stage V as posed is pre-empted.  Gate answer: YES.**

**And their answer has a SHAPE, which is the part worth carrying forward.**  The
certificate does not die when the dissipation is switched on.  It dies at a FOLD: each
branch turns around at a largest eps, the linearisation is singular there, and rigorous
branch verification has to stop at or before it.  `branch_in_kappa` below reproduces that
fold on Case I, branch j = 1, from the published equations.

--------------------------------------------------------------------------
THE SECOND PRECEDENT, AND THE ONE HOLE THAT IS LEFT
--------------------------------------------------------------------------
**[BC] arXiv:2404.04054** -- constructive (computer-assisted, Newton-Kantorovich in a
weighted Sobolev space) proofs of self-similar profiles for semilinear parabolic PDEs:
nonlinear heat, nonlinear Schroedinger, and a generalised VISCOUS Burgers equation.  The
dissipative term sits inside the certified profile equation.  Certification of a
self-similar profile of a dissipative equation is therefore not merely possible; it is
routine enough to be a methods paper.

**The hole:** neither paper does it for a FLUID transport model -- an inviscid blow-up of
Euler/Boussinesq/CLM type perturbed by viscosity.  Four arXiv queries for that
combination return nothing (`SEARCH_LOG`).  That hole is real, and it is NOT what stage V
asked for: stage V asked whether certification-under-dissipation can be done and what the
margin does, and the answer to both is published.  Narrowing the claim to "nobody has
done it for OUR model" is the move leg 42 deleted seven claims for.

--------------------------------------------------------------------------
WHAT IS VERIFIED HERE, AND WHAT IS ONLY TRANSCRIBED
--------------------------------------------------------------------------
Transcription is where errors hide (Route-J's rule), so the two are kept apart:

  TRANSCRIBED -- `DF_TABLE1`, `DF_TABLE2`: the published enclosures of (mu, gamma, kappa)
      for the NLS zeros, read off DF Tables 1 and 2.  Only mu and kappa are used as
      gates; **gamma is parameterisation-dependent** (DF parameterise the solution
      manifold at infinity in their §7; the module's `gamma` is the coefficient of the
      leading algebraic term in ITS OWN expansion, and the two need not agree).

  VERIFIED -- `shoot_newton` integrates their ODE from the origin with an independent
      RK4 and matches it to a three-term far-field expansion derived here, and returns
      (mu, kappa).  For both published cases it lands on the published enclosure:
      Case I j=1 to 2.4e-08 / 1.4e-07, Case II j=1 to 2.3e-08 / 2.5e-08.

  VERIFIED -- `branch_in_kappa` continues Case I branch j=1 in the DISSIPATION dial and
      returns the fold: eps* = 0.0606 at kappa ~ 0.55, inside the eps-range DF plot
      (their Figs. 1a/2a run to 0.06).  The margin proxy ||J^{-1}|| grows into it.

NORMS AND SCALES ARE NAMED (standing discipline).  The matching defect is
||Q_0'(xi_1) - Q_inf'(xi_1)||_C -- an ABSOLUTE complex modulus, whose scale is set by
|Q'(xi_1)| itself (1.3e-03 in Case II), so the relative defect at the published zero is
3.7e-07 rather than "small".  `match_defect` returns both.
"""

import numpy as np

# --------------------------------------------------------------------------
# THE LEDGER -- the gate's evidence, machine-readable
# --------------------------------------------------------------------------
# verdict:
#   PRE_EMPTS -- does certification-under-dissipation for a self-similar blow-up profile.
#   ADJACENT  -- certifies self-similar profiles of a dissipative equation, but with no
#                dissipation dial followed.
#   EXCLUSION -- studies dissipation without a certificate, or a certificate without
#                dissipation; does not answer the gate.
PRECEDENTS = [
    {
        "id": "arXiv:2410.05480",
        "who": "Dahne, Figueras",
        "what": "Self-similar singular solutions to NLS and the complex Ginzburg-Landau "
                "equation: rigorous shooting, interval arithmetic, branches followed in "
                "the dissipation parameter eps from the NLS limit.",
        "dial": "eps in (1 - i eps) Laplacian: 0 = NLS (conservative), >0 = CGL "
                "(dissipative)",
        "rigor": "computer-assisted proof, interval arithmetic (Arb), whole-branch "
                 "verification in Case I; partial in Case II",
        "verdict": "PRE_EMPTS",
        "gate": "cgl_branch_reproduction",
    },
    {
        "id": "arXiv:2404.04054",
        "who": "constructive-proofs group (semilinear PDEs on H^2(e^{|x|^2/4}))",
        "what": "Newton-Kantorovich computer-assisted existence proofs for self-similar "
                "profiles of parabolic PDEs -- nonlinear heat, NLS, generalised VISCOUS "
                "Burgers -- in a weighted Sobolev space.",
        "dial": "none followed; dissipation is present in the certified equation",
        "rigor": "computer-assisted proof, Newton-Kantorovich",
        "verdict": "ADJACENT",
        "gate": None,
    },
    {
        "id": "arXiv:2207.07548",
        "who": "Ambrose, Lushnikov, Siegel, Silantyev",
        "what": "gCLM WITH dissipation: global existence vs singularity formation, line "
                "vs circle. Analysis and numerics; no certificate of a profile.",
        "dial": "nu Lambda^sigma, sigma varied",
        "rigor": "analysis + numerics, no computer-assisted certificate",
        "verdict": "EXCLUSION",
        "gate": None,
    },
    {
        "id": "arXiv:1908.09385",
        "who": "J. Chen",
        "what": "Singularity formation and global well-posedness for gCLM WITH "
                "dissipation. Checked in leg 45: analytic throughout, no computer "
                "assistance.",
        "dial": "dissipation exponent",
        "rigor": "analytic",
        "verdict": "EXCLUSION",
        "gate": None,
    },
    {
        "id": "arXiv:2210.07191 + Part II (2305.05660)",
        "who": "Chen, Hou",
        "what": "2D Boussinesq / 3D Euler with boundary: certified self-similar blow-up. "
                "INVISCID -- the certificate has no dissipation dial.",
        "dial": "none",
        "rigor": "computer-assisted proof, interval arithmetic",
        "verdict": "EXCLUSION",
        "gate": None,
    },
    {
        "id": "arXiv:2509.14185",
        "who": "Wang, Lai, Gomez-Serrano, Buckmaster et al.",
        "what": "Unstable self-similar singularities for IPM and 3D Euler with boundary "
                "at near-machine precision, stated as CAP-ready. Inviscid.",
        "dial": "none",
        "rigor": "numerics at CAP-ready precision; no certificate claimed",
        "verdict": "EXCLUSION",
        "gate": None,
    },
    # Appended by leg 197 (Route-VNL), append-only: this row was FOUND and characterized at
    # primary-source depth by leg 174 (Route-VBS, writeup/data/p2_route_vbs_v1_scoping.json,
    # ledger key "BCG-NS") but never reached this shared ledger -- leg 174's own audit
    # recorded `arXiv_2208.09445_in_viscous_novelty_PRECEDENTS: false`, and none of the 12
    # SEARCH_LOG queries above mentions compressible/implosion/imploding, so stage V's gate
    # could not have reached it.  The `what`/`dial`/`rigor` text below is leg 174's Grade-B
    # characterization, transcribed; `experiments/p2_route_vnl_v1_ledger.py` checks the
    # transcription against leg 174's JSON rather than trusting this comment.
    {
        "id": "arXiv:2208.09445",
        "who": "Buckmaster, Cao-Labora, Gomez-Serrano",
        "what": "Smooth imploding solutions for 3D compressible fluids (Forum of Math Pi 13 "
                "(2025) e6, doi 10.1017/fmp.2024.12). Theorem 1.3 is finite-time singularity "
                "formation for the 3D isentropic compressible NAVIER-STOKES equations from "
                "smooth, finite-energy data with density constant at infinity -- a genuine "
                "viscous fluid equation. GRADE B, not A (leg 174's distinction): the object "
                "the interval arithmetic encloses is the self-similar profile solving system "
                "(1.5), the ODE reduction of the INVISCID compressible Euler system (1.3); "
                "Navier-Stokes is reached from it by the analytic stability argument of "
                "sections 7-8. The viscous term is DOMINATED, not enclosed -- section 7: "
                "'in the Navier-Stokes case we need to restrict the parameter r to a regime "
                "where the self-similar profile dominates the dissipation', i.e. dissipation "
                "becomes an exponentially decaying forcing in self-similar time rather than "
                "sitting at the leading scaling order as eps does in DF-CGL.",
        "dial": "none followed; the dissipation (Lame viscosities mu_1 > 0, 2 mu_1 + mu_2 > 0) "
                "is OUTSIDE the certified object -- it is dominated by the choice of "
                "self-similar exponent r, not enclosed",
        "rigor": "computer-assisted proof, interval arithmetic, essential and non-removable: "
                 "the first 10000 Taylor coefficient pairs (W_j, Z_j) at r = r*, with rigorous "
                 "error bounds, ~14 hours on a single CPU (section 1.3); Lemmas A.27/A.28 and "
                 "Appendix B 'Implementation details of the computer-assisted part'. Remove "
                 "the computer and the theorem does not stand as published.",
        "verdict": "EXCLUSION",
        "gate": None,
        # leg-197 provenance fields; the seven fields above are the schema the gate reads.
        "grade": "B",
        "banked_by": "leg 174 (Route-VBS), ledger key BCG-NS",
        "why_exclusion_not_pre_empts": "this module's vocabulary grades the CERTIFIED object: "
            "PRE_EMPTS requires certification-under-dissipation of the profile itself. BCG's "
            "certified equation carries no dissipative term, so it lands with the other "
            "inviscid-certificate rows (Chen-Hou), exactly as leg 113 filed it "
            "(clause_2_inviscid: True). It is nonetheless the strongest fluid-adjacent "
            "occupant of the rung, and its absence here is what made the rung look empty.",
    },
]

# the arXiv queries that produced the ledger, kept so the check can be re-run and so a
# later leg can see what was NOT asked (leg 42's failure mode was an unrecorded search).
SEARCH_LOG = [
    ('abs:"computer-assisted" AND abs:"self-similar" AND abs:blowup', 2),
    ('abs:"self-similar" AND abs:blowup AND abs:"fractional dissipation"', 1),
    ('abs:"Ginzburg-Landau" AND abs:"self-similar" AND abs:"computer-assisted"', 1),
    ('abs:"nonlinear heat equation" AND abs:"self-similar" AND abs:"computer-assisted"', 1),
    ('abs:"branches" AND abs:"self-similar" AND abs:"Ginzburg-Landau"', 1),
    ('abs:"self-similar" AND abs:blowup AND abs:"interval arithmetic"', 0),
    ('abs:"self-similar" AND abs:"blow-up" AND abs:"validated numerics"', 0),
    ('abs:"Boussinesq" AND abs:blowup AND abs:viscosity AND abs:"computer-assisted"', 0),
    ('abs:"self-similar" AND abs:blowup AND abs:"computer-assisted proof" AND abs:viscosity', 0),
    ('abs:"blowup" AND abs:"viscous" AND abs:"rigorous" AND abs:"continuation"', 0),
    ('abs:"hypodissipative" AND abs:"Navier-Stokes" AND abs:blowup', 1),
    ('abs:"self-similar" AND abs:"Navier-Stokes" AND abs:"computer-assisted"', 3),
]


def novelty_verdict():
    """The gate, computed from the ledger rather than remembered.

    Returns (answer, entries) with answer in {"YES", "NO"}: YES means stage V as posed
    is pre-empted and the plan's fallback (C-PILOT) applies."""
    pre = [p for p in PRECEDENTS if p["verdict"] == "PRE_EMPTS"]
    return ("YES" if pre else "NO"), pre


# --------------------------------------------------------------------------
# TRANSCRIBED: Dahne-Figueras Tables 1 and 2 (eps = 0, i.e. the NLS end of the dial)
# --------------------------------------------------------------------------
# (j, mu, kappa, xi_1) -- gamma is deliberately NOT transcribed as a gate; see docstring.
DF_TABLE1 = [           # Case I: d = 1, sigma = 2.3
    (1, 1.23203754902, 0.85310897700, 10.0),
    (2, 0.78307776500, 0.49322332400, 15.0),
    (3, 1.12384441100, 0.34675442900, 20.0),
    (4, 0.88388273000, 0.26676158000, 25.0),
]
DF_TABLE2 = [           # Case II: d = 3, sigma = 1
    (1, 1.885656965028834, 0.9173561185914533, 60.0),
]
DF_EPS_RANGE = {"case_I": 0.06, "case_II": 0.25}   # x-ranges of their Figs. 1 and 2

# TRANSCRIBED from DF Fig. 1a by reading the PDF's vector path data (`read_df_figure`):
# their own branch j = 1, sampled at a few kappa, plus its turning point.  Kept here so
# the gate still runs when Papers/ is empty -- Papers/ is gitignored and is destroyed
# whenever the container is rebuilt, which is exactly how five literature passes stayed
# search-level (Papers/MANIFEST.md).
DF_FIG1A_BRANCH1_FOLD = {"eps_star": 0.0606361, "kappa_star": 0.554644}
DF_FIG1A_BRANCH1_SAMPLES = [       # (kappa, eps) read off their curve, both sides
    (0.850127, 0.0012534),
    (0.800313, 0.0203187),
    (0.750232, 0.0357083),
    (0.700264, 0.0472553),
    (0.650150, 0.0551074),
    (0.600007, 0.0594489),
    (0.554644, 0.0606361),         # the fold
    (0.500204, 0.0591207),
    (0.449699, 0.0554317),
    (0.400386, 0.0503250),
    (0.350238, 0.0442117),
    (0.300151, 0.0377022),
    (0.250048, 0.0311467),
    (0.209734, 0.0259555),
]
# the calibration's own known-answer check: the eight curves of Fig. 1a start (at eps=0)
# on the eight kappa of Table 1, which is transcribed from a different page.  Agreement
# is 1.03e-05 or better on all four of Table 1's rows used here -- i.e. the width of a
# plotted line, which is the accuracy a figure can carry.
DF_FIG1A_CALIBRATION_RESIDUAL = 1.1e-05


def read_df_figure(pdf_path, page, xobject, eps_per_tick=0.01, kappa_per_tick=0.2,
                   kappa_first_tick=0.2, min_points=15):
    """DF's published branch figure, read as DATA from the PDF's vector paths.

    Their Figs. 1 and 2 are pgf vector graphics, not raster images, so the branch curves
    are literal polylines in the content stream and the axis ticks are two-point
    segments.  Calibrating on the ticks turns the figure into (eps, kappa) pairs -- which
    is the difference between "our fold is consistent with their plotted range" and "our
    fold agrees with theirs to 1e-07".

    THE CALIBRATION CHECKS ITSELF: the left endpoint of each extracted curve must land on
    the corresponding kappa of Table 1, which is transcribed from a different part of the
    paper.  Two independent readings of the same object (banked lesson 3).

    Returns (curves, calibration) with curves a list of (eps, kappa) arrays, longest
    first, or None if the PDF is not present -- Papers/ is gitignored."""
    import os
    import re
    if not os.path.exists(pdf_path):
        return None
    from pypdf import PdfReader
    stream = (PdfReader(pdf_path).pages[page]["/Resources"]["/XObject"][xobject]
              .get_object().get_data().decode("latin1"))
    paths, cur = [], []
    for line in stream.split("\n"):
        line = line.strip()
        m = re.fullmatch(r"([-\d.]+) ([-\d.]+) ([ml])", line)
        if m:
            x, y, op = float(m.group(1)), float(m.group(2)), m.group(3)
            if op == "m":
                if len(cur) > 1:
                    paths.append(np.array(cur))
                cur = [(x, y)]
            else:
                cur.append((x, y))
        elif line in ("S", "f", "h", "n") and len(cur) > 1:
            paths.append(np.array(cur))
            cur = []
    if len(cur) > 1:
        paths.append(np.array(cur))
    two = [p for p in paths if len(p) == 2]
    span = [np.abs(p[1] - p[0]) for p in two]
    xt = sorted(float(p[0][0]) for p, s in zip(two, span) if s[0] < 1e-6 and 1 < s[1] < 6)
    yt = sorted(float(p[0][1]) for p, s in zip(two, span) if s[1] < 1e-6 and 1 < s[0] < 6)
    if len(xt) < 2 or len(yt) < 2:
        return None
    x_per = float(np.mean(np.diff(xt))) / eps_per_tick
    y_per = float(np.mean(np.diff(yt))) / kappa_per_tick
    curves = []
    for p in sorted((q for q in paths if len(q) >= min_points), key=len, reverse=True):
        curves.append((np.asarray((p[:, 0] - xt[0]) / x_per, dtype=float),
                       np.asarray(kappa_first_tick + (p[:, 1] - yt[0]) / y_per,
                                  dtype=float)))
    return curves, {"x_tick0": xt[0], "x_per_unit": x_per, "y_tick0": yt[0],
                    "y_per_unit": y_per, "n_x_ticks": len(xt), "n_y_ticks": len(yt)}


# --------------------------------------------------------------------------
# VERIFIED: the profile ODE, integrated from the origin
# --------------------------------------------------------------------------
def _second_derivative(xi, Q, dQ, kappa, eps, d, sigma, omega, delta=0.0):
    """Q'' from DF (3), solved for the highest derivative."""
    fac = 1.0 - 1j * eps
    reg = 0.0 if xi == 0.0 else (d - 1) / xi * dQ
    return (-fac * reg - 1j * kappa * xi * dQ - 1j * (kappa / sigma) * Q + omega * Q
            - (1.0 + 1j * delta) * (abs(Q) ** (2 * sigma)) * Q) / fac


def integrate_from_zero(mu, kappa, eps, d, sigma, xi1, omega=1.0, delta=0.0,
                        steps_per_osc=200, hmax=0.01):
    """Q_0 of DF (5): the initial-value problem Q(0) = mu, Q'(0) = 0, integrated to xi1.

    RK4 with a PHASE-RESOLVING step.  The far field of this ODE oscillates like
    exp(i kappa xi^2 / 2), whose local wavenumber is kappa*xi and therefore grows without
    bound; a fixed step silently under-resolves the outer part of the interval.  The step
    is capped at both a fixed hmax and a fraction of the local period, and
    `resolution_ladder` below halves both and reports the change rather than asserting
    convergence."""
    fac = 1.0 - 1j * eps
    # the origin: Q'(0) = 0 makes (d-1)/xi Q' -> (d-1) Q''(0), so the singular term is
    # removable and Q''(0) follows from the equation (this is the d-fold factor below).
    dd0 = (omega * mu - 1j * (kappa / sigma) * mu
           - (1.0 + 1j * delta) * (abs(mu) ** (2 * sigma)) * mu) / (fac * d)
    xi = 1e-8
    Q = mu + 0.5 * dd0 * xi ** 2
    dQ = dd0 * xi
    n_steps = 0
    # a damped-Newton line search evaluates the map at states that overflow; those trials
    # are supposed to be rejected on their norm, not to raise.
    err = np.errstate(over="ignore", invalid="ignore", divide="ignore")
    err.__enter__()
    while xi < xi1:
        period_step = 2.0 * np.pi / max(kappa * xi, 1e-12) * (40.0 / steps_per_osc)
        h = min(hmax, period_step, xi1 - xi)
        y = np.array([Q, dQ])

        def f(x, yv):
            return np.array([yv[1], _second_derivative(x, yv[0], yv[1], kappa, eps,
                                                       d, sigma, omega, delta)])
        k1 = f(xi, y)
        k2 = f(xi + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(xi + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(xi + h, y + h * k3)
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        Q, dQ = y
        xi += h
        n_steps += 1
    err.__exit__(None, None, None)
    return complex(Q), complex(dQ), n_steps


# --------------------------------------------------------------------------
# VERIFIED: the far field, three terms, derived here rather than transcribed
# --------------------------------------------------------------------------
def asymptotic_coefficients(gamma, kappa, eps, d, sigma, omega=1.0, delta=0.0):
    """(p, a1, a2) for  Q_inf = gamma xi^p (1 + a1 xi^-2 + a2 xi^-4).

    Substituting Q = gamma xi^p u, u = sum_k a_k xi^{-2k}, into DF (3):

      * the transport group  i kappa xi Q' + i(kappa/sigma) Q - omega Q  annihilates the
        leading term exactly when p = -1/sigma - i omega/kappa, and acts on the k-th
        correction as  -2 i kappa k;
      * the Laplacian group contributes (1 - i eps) [p(p+d-2) - 2k(2p+d-1) + 2k(2k+1)];
      * the nonlinearity contributes |gamma|^{2 sigma} xi^{-2} times
        |u|^{2 sigma} u = 1 + [(sigma+1) a1 + sigma conj(a1)] xi^{-2} + O(xi^{-4}),
        which is where the expansion stops being holomorphic in gamma -- harmless
        numerically, and the reason a1's conjugate appears in a2.

    Truncating after a2 leaves a relative error O(xi^{-6}); `xi1_ladder` measures it
    instead of assuming it."""
    p = -1.0 / sigma - 1j * omega / kappa
    fac = 1.0 - 1j * eps
    g2s = abs(gamma) ** (2 * sigma)
    nl = (1.0 + 1j * delta) * g2s
    a1 = (fac * p * (p + d - 2) + nl) / (2j * kappa)
    a2 = (fac * a1 * (p * (p + d - 2) - 2 * (2 * p + d - 1) + 6)
          + nl * ((sigma + 1) * a1 + sigma * np.conj(a1))) / (4j * kappa)
    return p, a1, a2


def match_defect(mu, kappa, eps, d, sigma, xi1, omega=1.0, delta=0.0, **kw):
    """DF's matching condition (6), as one complex number.

    The VALUE equation is used to define gamma (a fixed-point iteration, since the
    expansion's coefficients depend on |gamma|), so what is left is the DERIVATIVE
    equation -- two real equations in the two real unknowns (mu, kappa).  Returns
    (defect, gamma, scale) with scale = |Q_0'(xi1)|, because an absolute defect without
    the scale it is small compared to is a number with no referent (discipline 73)."""
    Q, dQ, _ = integrate_from_zero(mu, kappa, eps, d, sigma, xi1, omega, delta, **kw)
    p = -1.0 / sigma - 1j * omega / kappa
    gamma = Q * xi1 ** (-p)
    for _ in range(50):
        p, a1, a2 = asymptotic_coefficients(gamma, kappa, eps, d, sigma, omega, delta)
        u = 1.0 + a1 / xi1 ** 2 + a2 / xi1 ** 4
        gamma_new = Q / (xi1 ** p * u)
        if abs(gamma_new - gamma) <= 1e-15 * abs(gamma):
            gamma = gamma_new
            break
        gamma = gamma_new
    p, a1, a2 = asymptotic_coefficients(gamma, kappa, eps, d, sigma, omega, delta)
    u = 1.0 + a1 / xi1 ** 2 + a2 / xi1 ** 4
    du = -2.0 * a1 / xi1 ** 3 - 4.0 * a2 / xi1 ** 5
    dQ_inf = gamma * (p * xi1 ** (p - 1) * u + xi1 ** p * du)
    return complex(dQ - dQ_inf), complex(gamma), float(abs(dQ))


# --------------------------------------------------------------------------
# VERIFIED: Newton on the shooting map, in two parameterisations
# --------------------------------------------------------------------------
def _damped_newton(residual, x0, tol=1e-12, max_iter=40, fd=1e-6):
    """Backtracking Newton on a 2-real-equation, 2-real-unknown map.

    Damped because the undamped step overshoots on Case II: the basin of the shooting
    zero is ~1e-3 wide in (mu, kappa) while the plain Newton step from three digits out
    is ~1e-2, and it limit-cycles.  A narrow basin is not a defect of the method -- it is
    the reason DF need rigorous enclosures rather than a converged float iterate."""
    x = np.array(x0, dtype=float)
    hist = []
    for _ in range(max_iter):
        R = residual(x)
        n0 = float(np.abs(R).max())
        hist.append(n0)
        if n0 < tol:
            break
        J = np.zeros((2, 2))
        for j in range(2):
            dx = fd * max(abs(x[j]), 1e-2)
            xp = x.copy()
            xp[j] += dx
            J[:, j] = (residual(xp) - R) / dx
        try:
            step = np.linalg.solve(J, R)
        except np.linalg.LinAlgError:
            break
        lam = 1.0
        while lam > 1.0 / 1024:
            if float(np.abs(residual(x - lam * step)).max()) < n0:
                break
            lam *= 0.5
        x = x - lam * step
    return x, hist


def shoot_newton(mu0, kappa0, eps, d, sigma, xi1, omega=1.0, **kw):
    """Solve for (mu, kappa) at fixed dissipation eps.  Returns (mu, kappa), history."""
    def residual(x):
        r, _, _ = match_defect(x[0], x[1], eps, d, sigma, xi1, omega, **kw)
        return np.array([r.real, r.imag])
    x, hist = _damped_newton(residual, [mu0, kappa0], **{k: v for k, v in kw.items()
                                                         if k in ("tol", "max_iter")})
    return (float(x[0]), float(x[1])), hist


def solve_at_kappa(mu0, eps0, kappa, d, sigma, xi1, omega=1.0, **kw):
    """Solve for (mu, eps) at fixed kappa -- the parameterisation that walks THROUGH the
    fold.

    Continuing in eps directly cannot pass the branch's turning point (two solutions
    below eps*, none above); kappa is monotone along the branch, so using it as the
    continuation parameter and solving for the dissipation makes the fold an ordinary
    interior point.  This is the standard fold-crossing trick, and it is what makes the
    fold MEASURABLE rather than a Newton failure."""
    def residual(x):
        r, _, _ = match_defect(x[0], kappa, x[1], d, sigma, xi1, omega, **kw)
        return np.array([r.real, r.imag])
    x, hist = _damped_newton(residual, [mu0, eps0])
    return (float(x[0]), float(x[1])), hist


def margin_proxy(mu, kappa, eps, d, sigma, xi1, omega=1.0, fd=1e-6, **kw):
    """||J^{-1}||_inf for the (mu, kappa) shooting Jacobian at fixed eps.

    THE FLOAT ANALOGUE OF THE CERTIFICATE'S MARGIN, and named as an analogue rather than
    as a certificate constant.  In a radii polynomial the approximate inverse A enters
    Y_0 = ||A F||, Z_1 = ||I - A DF|| and Z_2 ~ ||A||, so every constant degrades with
    ||DF^{-1}||; here DF is the 2x2 shooting Jacobian and ||J^{-1}|| is what diverges at
    a fold.  It is NOT Y_0/Z_1/Z_2 for this problem and is not called that."""
    def residual(x):
        r, _, _ = match_defect(x[0], x[1], eps, d, sigma, xi1, omega, **kw)
        return np.array([r.real, r.imag])
    x = np.array([mu, kappa], float)
    R = residual(x)
    J = np.zeros((2, 2))
    for j in range(2):
        dx = fd * max(abs(x[j]), 1e-2)
        xp = x.copy()
        xp[j] += dx
        J[:, j] = (residual(xp) - R) / dx
    Jinv = np.linalg.inv(J)
    return float(np.abs(Jinv).sum(axis=1).max()), float(np.linalg.cond(J))


def margin_law(branch, fold, d, sigma, xi1, offsets=(0.08, 0.04, 0.02, 0.01, 0.005),
               omega=1.0):
    """||J^-1|| as the fold is approached, and the exponent of its divergence.

    A fold is where the (mu, kappa) Jacobian at fixed eps loses rank, so ||J^-1|| should
    diverge like |kappa - kappa*|^-1 for an ordinary quadratic fold.  Measuring the
    EXPONENT rather than announcing "it blows up" is the Route-F rule (a threshold near a
    critical point is biased in the direction you expect; an exponent is checkable).

    Returns rows on both sides of the fold plus the least-squares slope of
    log10||J^-1|| against log10|kappa - kappa*|."""
    rec = [r for r in branch if r["converged"]]
    ks = fold["kappa_star"]
    rows = []
    for off in offsets:
        for side in (+1, -1):
            kappa = ks + side * off
            seed = min(rec, key=lambda r: abs(r["kappa"] - kappa))
            (mu, eps), hist = solve_at_kappa(seed["mu"], seed["eps"], kappa, d, sigma,
                                             xi1, omega)
            if hist[-1] > 1e-9:
                continue
            n_inv, cond = margin_proxy(mu, kappa, eps, d, sigma, xi1, omega)
            _, _, scale = match_defect(mu, kappa, eps, d, sigma, xi1, omega)
            rows.append({"kappa": float(kappa), "offset": float(side * off),
                         "distance": float(off), "eps": eps, "mu": mu,
                         "Jinv_norm": n_inv, "cond": cond, "defect_scale": scale})
    if len(rows) < 4:
        return {"rows": rows, "slope": None}
    x = np.log10([r["distance"] for r in rows])
    y = np.log10([r["Jinv_norm"] for r in rows])
    slope, intercept = np.polyfit(x, y, 1)
    return {"rows": rows, "slope": float(slope), "intercept": float(intercept),
            "expected_slope": -1.0}


# --------------------------------------------------------------------------
# VERIFIED: the branch in the DISSIPATION dial, and its fold
# --------------------------------------------------------------------------
def branch_in_kappa(mu0, kappa_start, kappa_stop, d, sigma, xi1, dkappa=0.01,
                    omega=1.0, eps0=0.0, tol=1e-9, **kw):
    """Follow one branch of DF's Fig. 1/2 by sweeping kappa downward.

    Returns a list of records (kappa, mu, eps, defect, converged).  The sweep STOPS when
    Newton stops converging or when eps leaves [0, 1): past the branch's end the map has
    other zeros (with negative eps, i.e. anti-dissipation) and a continuation that does
    not check will happily report them as branch points."""
    out = []
    mu, eps = float(mu0), float(eps0)
    kappas = np.arange(kappa_start, kappa_stop - 1e-12, -abs(dkappa))
    for kappa in kappas:
        (mu_n, eps_n), hist = solve_at_kappa(mu, eps, float(kappa), d, sigma, xi1,
                                             omega, **kw)
        # -1e-6 rather than 0: the branch STARTS at eps = 0, so its first record sits on
        # the boundary and float noise puts it either side of it.  A hard >= 0 test
        # rejects the branch's own starting point, which is how this guard first failed.
        ok = bool(hist[-1] < tol and -1e-6 <= eps_n < 1.0
                  and abs(eps_n - eps) < 0.05 and abs(mu_n - mu) < 0.5)
        if not ok:
            out.append({"kappa": float(kappa), "mu": mu_n, "eps": eps_n,
                        "defect": float(hist[-1]), "converged": False})
            break
        mu, eps = mu_n, eps_n
        out.append({"kappa": float(kappa), "mu": mu, "eps": eps,
                    "defect": float(hist[-1]), "converged": True})
    return out


def fold_of(branch):
    """(eps*, kappa*) -- the largest dissipation the branch reaches, by parabolic fit
    through the three records around the discrete maximum.

    Reported as a magnitude with the bracketing records, not as a boolean 'it folds'."""
    rec = [r for r in branch if r["converged"]]
    if len(rec) < 3:
        return None
    eps = np.array([r["eps"] for r in rec])
    kap = np.array([r["kappa"] for r in rec])
    k = int(np.argmax(eps))
    if k == 0 or k == len(rec) - 1:
        return {"eps_star": float(eps[k]), "kappa_star": float(kap[k]),
                "interior": False}
    x = kap[k - 1:k + 2]
    y = eps[k - 1:k + 2]
    c = np.polyfit(x, y, 2)
    ks = -0.5 * c[1] / c[0]
    return {"eps_star": float(np.polyval(c, ks)), "kappa_star": float(ks),
            "interior": True, "bracket": [float(eps[k - 1]), float(eps[k]),
                                          float(eps[k + 1])]}


# --------------------------------------------------------------------------
# the two guards: resolution, and far-field truncation
# --------------------------------------------------------------------------
def compare_to_published_branch(branch, samples=None):
    """Our computed branch against DF's published one, in THEIR units.

    Their curve is a function of kappa on each side of the fold, so kappa is the
    independent variable and the comparison is |eps_ours(kappa) - eps_theirs(kappa)|,
    interpolated on our records.  Returned as max and RMS with the per-sample table, not
    as a verdict."""
    samples = DF_FIG1A_BRANCH1_SAMPLES if samples is None else samples
    rec = [r for r in branch if r["converged"]]
    if len(rec) < 4:
        return None
    kap = np.array([r["kappa"] for r in rec])
    eps = np.array([r["eps"] for r in rec])
    rows = []
    for k_pub, e_pub in samples:
        if k_pub > kap.max() or k_pub < kap.min():
            continue
        # our sweep is monotone in kappa, so a plain interpolation is well-defined
        order = np.argsort(kap)
        e_ours = float(np.interp(k_pub, kap[order], eps[order]))
        rows.append({"kappa": float(k_pub), "eps_published": float(e_pub),
                     "eps_ours": e_ours, "diff": e_ours - float(e_pub)})
    if not rows:
        return None
    diffs = np.array([r["diff"] for r in rows])
    return {"rows": rows, "max_abs_diff": float(np.abs(diffs).max()),
            "rms_diff": float(np.sqrt(np.mean(diffs ** 2))), "n": len(rows)}


def resolution_ladder(mu, kappa, eps, d, sigma, xi1, omega=1.0):
    """The matching defect under step halving -- the integrator's own convergence."""
    out = []
    for spo, hmax in ((200, 0.01), (400, 0.005), (800, 0.0025)):
        r, g, scale = match_defect(mu, kappa, eps, d, sigma, xi1, omega,
                                   steps_per_osc=spo, hmax=hmax)
        out.append({"steps_per_osc": spo, "hmax": hmax, "defect": float(abs(r)),
                    "relative": float(abs(r) / scale), "gamma": [g.real, g.imag]})
    return out


def xi1_ladder(mu0, kappa0, eps, d, sigma, xi1s, omega=1.0):
    """(mu, kappa) as the matching point moves out -- the far-field truncation's cost.

    The three-term expansion errs at O(xi^{-6}), so this ladder is the honest error bar
    on the reproduction, and it is reported as a SHAPE (discipline 72) rather than as its
    tightest rung."""
    out = []
    for xi1 in xi1s:
        (mu, kappa), hist = shoot_newton(mu0, kappa0, eps, d, sigma, float(xi1), omega)
        out.append({"xi1": float(xi1), "mu": mu, "kappa": kappa,
                    "defect": float(hist[-1]), "iterations": len(hist)})
    return out
