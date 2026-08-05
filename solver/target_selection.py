"""ROUTE M v1: TARGET SELECTION -- "certify WHAT, that isn't already done?"

--------------------------------------------------------------------------
WHY THIS MODULE EXISTS
--------------------------------------------------------------------------
For twenty legs the certification effort has been aimed at the 2D Boussinesq profile
of Chen-Hou, arXiv:2210.07191.  **That object was certified by its authors in 2022, in
145 pages of analysis plus a separate rigorous-numerics Part II.**  Closing a radii
polynomial there would prove that we can certify; it would not be a result.

Route-J (leg 42) deleted seven of twelve standing novelty claims by reading the primary
sources, and made the gap visible: the phenomenology this project treated as candidate-
novel is largely in print.  What nobody had checked is the complementary question --
which objects with numerically convincing blow-up are **still uncertified**, and which
of those are within interval-arithmetic reach.  This module is that check, in the form
Route-J's lesson (68) demands: **executable, not prose.**  A literature check that is
not runnable decays at the rate of memory.

--------------------------------------------------------------------------
THE THREE QUESTIONS, AND WHY THEY ARE IN THIS ORDER
--------------------------------------------------------------------------
Per candidate object:

  Q1  **Is it already certified?**  Not "is blow-up known" -- is there a computer-
      assisted proof *of this specific profile*.  An analytic proof counts too, and
      counts harder: an object proved by hand (Huang-Qin-Wang-Wei's fixed-point
      construction, J. Chen's perturbative argument) does not become more true when a
      computer re-proves it.  `CERTIFICATION_RECORD` below is the answer set.

  Q2  **Is it within interval-arithmetic reach?**  The honest discriminator is the
      unknown count and the nonlocal operator's cost, not elegance.  `unknowns()` is an
      exact arithmetic count, and `cost_ratio_vs_certified()` measures every candidate
      against **the object that was actually certified** -- which is the only calibration
      point in existence where a proof of this kind is known to have been completed.

  Q3  **What would certifying it contribute?**  A sentence a specialist would accept.
      Where the answer is "it reproduces X", the entry says so and ranks last.

Q1 dominates Q3 dominates Q2, and that ordering is deliberate: a cheap object that
reproduces a published theorem is worth nothing, and an expensive object that settles
an open conjecture is worth attempting even if it fails.

--------------------------------------------------------------------------
WHAT IS VERIFIED HERE, AND WHAT IS TRANSCRIBED
--------------------------------------------------------------------------
**VERIFIED** (re-derived from published equations/constants by code in this module):

  M2a  the radii-polynomial / Newton-Kantorovich feasibility algebra, against
       Cadiot-Lessard-Nave (arXiv:2302.12877) Theorem 4.6 and their Kawahara soliton
       constants -- `radii_polynomial`, `y0_budget`, `cln_kawahara_check`.
  M2b  the scalar closure asserted by arXiv:2604.09949 for 3D Navier-Stokes, in BOTH the
       form the manuscript states and the form Kantorovich's theorem actually requires
       -- `ns_preprint_closure_audit`.  **It closes in both.**  Recorded because the
       useful finding is that the arithmetic is NOT where that manuscript fails, which
       is what makes the other reasons decisive rather than piled-on.
  M3   reachability of the top-ranked candidate, measured on our own code as a
       refinement ladder -- that lives in `experiments/p2_route_m_v1_targets.py`
       because it needs the integrator, not the ledger.

**TRANSCRIBED, not verified:** every entry of `CERTIFICATION_RECORD` and every
`published` field of `TARGET_LEDGER`.  Those are read off PDFs and are exactly as good
as that.  Mesh sizes in particular are NOT transcribed as precise counts, because the
published meshes are adaptive and a fabricated count would poison `cost_ratio`.

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* Not a survey.  Three questions per object, ranked, time-boxed to one leg.
* Not a novelty claim for anything.  Naming an object as uncertified is a statement
  about the literature we read, and `Papers/MANIFEST.md` says which that is.
* Not a promise that the top-ranked object can be certified.  It says the object is
  uncertified and that its unknown count is small; both walls in `CLAY_ROADMAP.md` §7
  are untouched by this leg.
"""

import numpy as np

# --------------------------------------------------------------------------
# provenance -- the sources this leg read, beyond Route-J's four
# --------------------------------------------------------------------------
ROUTE_M_SOURCES = {
    "2302.12877": {
        "tag": "CLN",
        "authors": "Cadiot, Lessard, Nave",
        "title": ("Rigorous computation of solutions of semi-linear PDEs on unbounded "
                  "domains via spectral methods"),
        "venue": "arXiv v3, 29 Feb 2024",
        "read": "sections 3, 4.2, 4.3, 6 closely; Theorem 4.6 and Theorem 6.6 transcribed",
        "gates": ["Q2 for a whole class -- what a CAP on an UNBOUNDED domain costs",
                  "Route-D's weighted-l1 no-go and discrete-ball trap"],
    },
    "2604.01868": {
        "tag": "CHL",
        "authors": "Chen, Huang, Li",
        "title": ("Novel self-similar finite-time blowups with singular profiles of the "
                  "1D Hou-Luo model and the 2D Boussinesq equations: "
                  "a numerical investigation"),
        "venue": "arXiv, Apr 2026",
        "read": "sections 1, 2.3-2.5, 3, 4, 5, 6.2 closely",
        "gates": ["the top TWO uncertified candidates", "Conjecture 2.4"],
    },
    "2603.25104": {
        "tag": "HTW26",
        "authors": "Huang, Tong, Wang",
        "title": ("Self-similar finite-time blowups with singular profiles of the "
                  "generalized Constantin-Lax-Majda model"),
        "venue": "arXiv, Mar 2026",
        "read": "abstract, sections 1, 4.1, 4.2 closely; Table 4.1 transcribed",
        "gates": ["the cheapest uncertified candidate, and a sign change in c_l"],
    },
    "2308.01528": {
        "tag": "HQWW",
        "authors": "Huang, Qin, Wang, Wei",
        "title": ("Exact self-similar finite-time blowup of the Hou-Luo model with "
                  "smooth profiles"),
        "venue": "arXiv, Aug 2023",
        "read": "abstract, section 1",
        "gates": ["Q1 for the Hou-Luo odd non-degenerate profile -- it is ANALYTIC now"],
    },
    "2305.05895": {
        "tag": "HQWW-gCLM",
        "authors": "Huang, Qin, Wang, Wei",
        "title": ("Self-similar finite-time blowups with smooth profiles of the "
                  "generalized Constantin-Lax-Majda model"),
        "venue": "arXiv, May 2023",
        "read": "abstract, section 1",
        "gates": ["Q1 for the whole gCLM a <= 1 smooth branch -- ANALYTIC"],
    },
    "1908.09385": {
        "tag": "JC19",
        "authors": "J. Chen",
        "title": ("Singularity formation and global well-posedness for the generalized "
                  "Constantin-Lax-Majda equation with dissipation"),
        "venue": "arXiv, Aug 2019",
        "read": "sections 1, 2 (statement level)",
        "gates": ["Q1 for DISSIPATIVE gCLM near a = 1/2 -- analytic, no computer"],
    },
    "2604.09949": {
        "tag": "NS-PREPRINT",
        "authors": "Shahmurov",
        "title": ("Stable finite-time singularity formation for 3D Navier-Stokes via "
                  "5D-lifted axisymmetric reductions"),
        "venue": "arXiv, Apr 2026",
        "read": "full text; sections 8-14 and appendix D closely",
        "gates": ["Q1 for the single most consequential target -- see the audit below"],
    },
}


# --------------------------------------------------------------------------
# Q1 -- the certification record.  What has actually been PROVED, and how.
# --------------------------------------------------------------------------
# proof_kind: CAP (computer-assisted), ANALYTIC (by hand), NONE.
CERTIFICATION_RECORD = [
    {
        "object": "2D Boussinesq / 3D Euler with boundary, Chen-Hou profile",
        "proof_kind": "CAP",
        "source": "Chen-Hou, arXiv:2210.07191 (Part I, analysis) + Part II (rigorous numerics)",
        "note": ("The object the L1->L2 port has been aimed at for twenty legs.  "
                 "Certified by its authors; 145 pages plus a separate numerics paper."),
    },
    {
        "object": "1D Hou-Luo, odd NON-degenerate smooth profile",
        "proof_kind": "CAP+ANALYTIC",
        "source": ("Chen-Hou-Huang, Ann. PDE 8 (2022) 24 (CAP); "
                   "Huang-Qin-Wang-Wei, arXiv:2308.01528 (analytic, exact profiles)"),
        "note": ("Proved twice, the second time by a purely analytic fixed-point "
                 "construction that also settles monotonicity, convexity and far-field "
                 "decay.  A third proof of this object is worth nothing."),
    },
    {
        "object": "De Gregorio (gCLM a = 1) self-similar blow-up",
        "proof_kind": "CAP",
        "source": "Chen-Hou-Huang, CPAM 74 (2021) 1282",
        "note": "Certified.",
    },
    {
        "object": "gCLM smooth self-similar profiles, ALL a <= 1",
        "proof_kind": "ANALYTIC",
        "source": "Huang-Qin-Wang-Wei, arXiv:2305.05895",
        "note": ("A whole one-parameter FAMILY, proved by hand, with regularity, "
                 "monotonicity and decay rates.  This closes the entire smooth gCLM "
                 "branch -- exactly the branch Routes D/E/F measured."),
    },
    {
        "object": "dissipative gCLM near a = 1/2, full Laplacian",
        "proof_kind": "ANALYTIC",
        "source": "J. Chen, arXiv:1908.09385 Theorem 1.1",
        "note": ("Nonlinear stability of an approximate self-similar profile, "
                 "perturbatively around the exact a = 1/2 solution.  No computer "
                 "assistance appears in that paper."),
    },
    {
        "object": "3D axisymmetric Euler without swirl, C^{1,alpha} velocity",
        "proof_kind": "ANALYTIC",
        "source": "Elgindi, Ann. of Math. 194 (2021) 647",
        "note": "Analytic; stability in Elgindi-Ghoul-Masmoudi.",
    },
    {
        "object": "1D Hou-Luo singular steady state 1_{X>1}(X-1)^{-1/2}, EXISTENCE",
        "proof_kind": "ANALYTIC",
        "source": "Chen-Huang-Li, arXiv:2604.01868 Theorem 2.3 / Theorem 5.3",
        "note": ("Existence in the WEAK sense is proved.  Its asymptotic STABILITY -- "
                 "which is what makes it a blow-up mechanism rather than a curiosity -- "
                 "is their Conjecture 2.4 and is open."),
    },
    {
        "object": "3D Navier-Stokes on T^3, exact backward self-similar profile",
        "proof_kind": "NONE",
        "source": "claimed by arXiv:2604.09949; see `ns_preprint_closure_audit`",
        "note": ("Not usable as a certification: no verification package is released "
                 "(the manuscript's own appendix F says the reproducibility package is "
                 "'intended to contain' its contents), and the ansatz is the backward "
                 "self-similar one excluded by Necas-Ruzicka-Sverak and Tsai under the "
                 "decay its own function space implies.  Its reference list cites "
                 "Jia-Sverak on FORWARD self-similar solutions, which exist, in place "
                 "of the backward non-existence results, which are the relevant ones."),
    },
]


def certified_objects():
    """The objects Q1 answers YES for, with the proof kind -- the exclusion list."""
    return [c for c in CERTIFICATION_RECORD if c["proof_kind"] != "NONE"]


# --------------------------------------------------------------------------
# Q2 -- reach, as an exact unknown count against the one calibration point
# --------------------------------------------------------------------------
# The only honest calibration for "can interval arithmetic close this?" is an object
# where a proof of exactly this kind WAS completed.  That is Chen-Hou's: 2D, three
# fields (omega, eta, xi), piecewise 6th-order B-splines on an adaptive mesh over
# [0, L]^2 with L ~ 1e13.  Their mesh is ADAPTIVE and this module does not transcribe a
# node count, because a fabricated count would silently set every ratio below.  What is
# used instead is the SHAPE of the cost: fields x n^dim, with n the per-direction
# resolution, compared at the SAME n.  That comparison is exact arithmetic and it is the
# only part of the cost that a change of quadrature cannot move.
CERTIFIED_REFERENCE = {
    "object": "2D Boussinesq / 3D Euler with boundary (Chen-Hou)",
    "dim": 2,
    "n_fields": 3,          # omega, eta, xi  (their (2.10) variables)
    "n_modulation": 2,      # c_l, c_omega
    "nonlocal": "2D Biot-Savart with boundary; a 2D singular integral per evaluation",
}


def unknowns(dim, n_fields, n_per_dim, n_modulation=0):
    """Exact unknown count for a spectral/collocation truncation.  No fudge factors.

    This is the quantity a rigorous Jacobian enclosure is quadratic in, and it is the
    only part of the cost comparison that does not depend on anyone's quadrature.
    """
    return int(n_fields) * int(n_per_dim) ** int(dim) + int(n_modulation)


def cost_ratio_vs_certified(dim, n_fields, n_per_dim, n_modulation=0):
    """(unknowns of this object) / (unknowns of the CERTIFIED object) at the same n.

    Returns a dict with both counts and the ratio.  A ratio <= 1 means cost is not the
    obstruction, because a proof at that size has been carried out by somebody.  It
    does NOT mean the proof is easy: the ratio is silent about conditioning, about the
    nonlocal operator's enclosure width, and about whether a fixed point exists at all
    (which is a separate measurement -- see M3).
    """
    mine = unknowns(dim, n_fields, n_per_dim, n_modulation)
    ref = unknowns(CERTIFIED_REFERENCE["dim"], CERTIFIED_REFERENCE["n_fields"],
                   n_per_dim, CERTIFIED_REFERENCE["n_modulation"])
    return {"n_per_dim": int(n_per_dim), "unknowns": mine, "unknowns_certified": ref,
            "ratio": mine / ref, "log10_ratio": float(np.log10(mine / ref))}


# --------------------------------------------------------------------------
# the radii polynomial, and the Y_0 BUDGET -- what "reachable" means numerically
# --------------------------------------------------------------------------
# [CLN] Theorem 4.6 (Newton-Kantorovich, in the radii-polynomial form this project has
# been writing since Route-D).  With  X a Banach space, A an approximate inverse,
#     ||A F(x)||           <= Y0
#     ||I - A DF(x)||      <= Z1
#     ||A (DF(v) - DF(x))|| <= Z2(r) r   for v in the closed r-ball about x,
# a solution exists in B_r(x) whenever
#     (1/2) Z2 r^2 - (1 - Z1) r + Y0 < 0     AND     Z1 + Z2 r < 1.
def radii_polynomial(Y0, Z1, Z2):
    """Roots and feasibility of (1/2) Z2 r^2 - (1 - Z1) r + Y0 < 0, with the Z1+Z2 r<1 side.

    Reported as MAGNITUDES (banked lesson 58): the discriminant and the admissible
    r-interval come back even when the polynomial has no negative part, so a failure
    says HOW FAR from feasible rather than merely 'no'.
    """
    Y0, Z1, Z2 = float(Y0), float(Z1), float(Z2)
    a, b, c = 0.5 * Z2, -(1.0 - Z1), Y0
    disc = b * b - 4.0 * a * c
    out = {"Y0": Y0, "Z1": Z1, "Z2": Z2, "discriminant": disc,
           "Y0_budget": y0_budget(Z1, Z2),
           "Y0_over_budget": Y0 / y0_budget(Z1, Z2) if y0_budget(Z1, Z2) > 0 else np.inf}
    if Z1 >= 1.0:
        out.update({"feasible": False, "reason": "Z1 >= 1: A is not an approximate inverse",
                    "r_min": None, "r_max": None})
        return out
    if disc < 0.0 or a <= 0.0:
        if a <= 0.0:                     # Z2 = 0: the polynomial is affine
            r = Y0 / (1.0 - Z1)
            out.update({"feasible": Y0 < np.inf, "r_min": r, "r_max": np.inf,
                        "reason": "Z2 = 0, affine"})
            return out
        out.update({"feasible": False, "r_min": None, "r_max": None,
                    "reason": "no positive part: Y0 exceeds the budget"})
        return out
    s = np.sqrt(disc)
    r_min, r_max = (-b - s) / (2 * a), (-b + s) / (2 * a)
    # the second condition Z1 + Z2 r < 1 caps r_max
    r_cap = (1.0 - Z1) / Z2
    out.update({"feasible": r_min < min(r_max, r_cap), "r_min": r_min,
                "r_max": min(r_max, r_cap), "r_cap_from_Z1Z2": r_cap,
                "reason": "ok"})
    return out


def y0_budget(Z1, Z2):
    """The largest residual a certificate can tolerate: Y0 <= (1 - Z1)^2 / (2 Z2).

    THIS is the number that makes "is it within interval-arithmetic reach?" a
    measurement rather than an opinion.  Z1 and Z2 are properties of the operator and
    the space; Y0 is a property of how well the profile is resolved.  Reach means:
    can the truncation be pushed until Y0 falls under a budget set by the other two.
    """
    Z1, Z2 = float(Z1), float(Z2)
    if Z2 <= 0.0:
        return np.inf
    return (1.0 - Z1) ** 2 / (2.0 * Z2)


def cln_kawahara_check():
    """[CLN] Theorem 6.6: Y0 <= 2.26e-14 and ||DF(u0)^{-1}||_{2,l} <= 4.4 give r0 = 2.27e-14.

    The published pair is the only place in the Route-M reading where a completed
    unbounded-domain certificate states its constants, so it is the natural gate on
    this module's algebra.  With A an approximate inverse of norm ~ ||DF^{-1}||, the
    affine part of the radii polynomial gives r ~ Y0 / (1 - Z1); the published r0
    exceeds Y0 by a factor 1.0044, i.e. their effective Z1 is 4.4e-3.  We report the
    IMPLIED Z1 rather than asserting one, because CLN split Z1 into a periodic part and
    an unbounded-domain part and do not print the sum.
    """
    Y0, r0, dfinv = 2.26e-14, 2.27e-14, 4.4
    z1_implied = 1.0 - Y0 / r0
    rp = radii_polynomial(Y0, z1_implied, 0.0)
    return {"Y0_published": Y0, "r0_published": r0, "dfinv_published": dfinv,
            "Z1_implied": z1_implied, "r_from_our_algebra": rp["r_min"],
            "rel_err_vs_published_r0": abs(rp["r_min"] - r0) / r0}


def ns_preprint_closure_audit():
    """Audit of arXiv:2604.09949's scalar Newton-Kantorovich closure, both forms.

    Their appendix D constants: residual delta = 8.421739e-12, inverse-stability bound
    M = 482.6, local Lipschitz constant K = 1.1e4.  The manuscript closes on

        2 delta M K < 1                                    (as printed, ~8.9e-5)

    but Kantorovich's hypothesis with beta = ||DF^{-1}|| <= M, eta = ||DF^{-1} F|| <=
    M delta and Lipschitz constant K is  h = beta K eta = M^2 K delta <= 1/2, i.e. in
    radii-polynomial form Y0 = M delta, Z1 = 0, Z2 = M K, whose budget condition is

        2 M^2 K delta < 1                                  (~4.3e-2)

    -- one factor of M larger.  **BOTH CLOSE.**  That is the point of running this: the
    arithmetic is not where that manuscript fails, so the reasons it cannot be used are
    the ones stated in CERTIFICATION_RECORD (no released verification package; a
    backward self-similar ansatz excluded by Necas-Ruzicka-Sverak / Tsai under the decay
    its own analytic weight implies), and they stand on their own.
    """
    delta, M, K = 8.421739e-12, 482.6, 1.1e4
    as_printed = 2.0 * delta * M * K
    corrected = 2.0 * M ** 2 * K * delta
    rp = radii_polynomial(M * delta, 0.0, M * K)
    # their own K is asserted as a product of two other certified constants
    K_from_parts = 2.5652e7 * 4.2872e-4
    return {"delta": delta, "M": M, "K": K,
            "closure_as_printed_2dMK": as_printed,
            "closure_corrected_2M2Kdelta": corrected,
            "both_close": bool(as_printed < 1.0 and corrected < 1.0),
            "margin_of_corrected_form": 1.0 / corrected,
            "K_recomputed_from_their_parts": K_from_parts,
            "K_rel_err": abs(K_from_parts - K) / K,
            "radii_polynomial_r_min": rp["r_min"],
            "verdict": ("arithmetic self-consistent in both forms; NOT usable as a "
                        "certification for the reasons in CERTIFICATION_RECORD")}


# --------------------------------------------------------------------------
# THE TARGET LEDGER -- the deliverable
# --------------------------------------------------------------------------
# `certified`: YES_CAP | YES_ANALYTIC | NO | CLAIMED_UNUSABLE
# `rank` is by Q3 (contribution) first, Q1 second, Q2 last -- see the module docstring.
TARGET_LEDGER = [
    {
        "rank": 1,
        "id": "HL_S2_nonsymmetric",
        "object": ("1D Hou-Luo, the NON-SYMMETRIC positive regular self-similar profile "
                   "(Chen-Huang-Li Scenario 2)"),
        "source": "arXiv:2604.01868 sections 2.5 and 4",
        "certified": "NO",
        "q1": ("Reported April 2026 as a numerical observation, explicitly 'a previously "
               "unreported blowup phenomenon'.  No proof, computer-assisted or "
               "otherwise.  It is NOT covered by Chen-Hou-Huang (odd, non-degenerate) "
               "nor by Huang-Qin-Wang-Wei's analytic construction, both of which use the "
               "symmetry at the origin."),
        "q2": {"dim": 1, "n_fields": 2, "n_modulation": 3,
               "nonlocal": "one Hilbert transform on R, plus U = int_0^X H(Omega)",
               "note": ("THREE modulation constants (c_l, c_omega, c_r), because the "
                        "profile has no symmetry point to pin the translation.  That is "
                        "a BORDERED system, not a projected one -- which is exactly the "
                        "shape leg 44 concluded the 2D port needs.")},
        "published": {"c_l": 1.0636, "c_omega": -0.4235, "c_r": 0.0765,
                      "ratio_cl_over_comega": -2.5114,
                      "note": ("Their Figure 4.2 limiting values; the ratio is the "
                               "normalization-INDEPENDENT one and is the number to "
                               "compare against.  Chen-Hou-Huang's symmetric branch sits "
                               "at about -2.9987, so this is a genuinely different "
                               "contraction rate, not a re-parametrization.")},
        "q3": ("First proof of a self-similar blow-up of the Hou-Luo model at a point "
               "OTHER than the symmetry point, and the first certificate for a profile "
               "with no symmetry to anchor the stability argument.  Chen-Huang-Li state "
               "the mechanism plainly: in every existing proof 'the origin always acts "
               "as the source of stability', and here there is no such origin -- the "
               "translation degree of freedom has to be carried by the certificate "
               "itself.  That is a methodological first, not another profile."),
        "our_machinery": ("ALREADY BUILT AND VALIDATED: solver/hl_rescaled.py::"
                          "RescaledHLScenario2 implements their (4.1)/(4.2) with the "
                          "3-constant origin-pinned gauge; test_hl_rescaled.py gates the "
                          "gauge to 4.4e-16; PHASE2_P2_NOTES section 8 reproduced the "
                          "ratio to about 1%.  It has been sitting in the repository "
                          "since 2026-07-26 while the port aimed at a certified object."),
    },
    {
        "rank": 2,
        "id": "gCLM_degenerate_one_scale",
        "object": ("gCLM one-scale self-similar profiles from DEGENERATE data, a > 0 "
                   "(Huang-Tong-Wang, vanishing order k = 3)"),
        "source": "arXiv:2603.25104 section 4, Table 4.1",
        "certified": "NO",
        "q1": ("Numerical only, March 2026, explicitly 'not been found in previous "
               "studies'.  Their analytic construction covers a < 0 (singular profiles) "
               "and a = 0; the a > 0 regular branch is observed, not proved.  Huang-Qin-"
               "Wang-Wei's analytic gCLM branch is the NON-degenerate one and does not "
               "cover these."),
        "q2": {"dim": 1, "n_fields": 1, "n_modulation": 2,
               "nonlocal": "one Hilbert transform on R",
               "note": ("The cheapest object on the list: a single scalar field.  The "
                        "cost is that the certificate must carry a k-th order "
                        "degeneracy constraint at the origin, which is a constraint on "
                        "the SPACE, not just the residual.")},
        "published": {"a": [0.1, 0.2, 0.232931, 0.232932, 0.3, 0.4, 0.5],
                      "c_l": [1.0888, 0.0691, 6.4688e-7, -9.7142e-7, -0.0717, -0.1135,
                              -0.1288],
                      "c_omega": [-3.8668, -0.8357, -0.6055, -0.6055, -0.3479, -0.1718,
                                  -0.0872],
                      "gamma": [0.2816, 0.0827, 1.0683e-6, -1.6043e-6, -0.2061, -0.6604,
                                -1.4771],
                      "note": ("Their Table 4.1, k = 3.  c_l CHANGES SIGN between "
                               "a = 0.232931 and 0.232932 -- they resolve the crossing "
                               "to six digits in a, and gamma passes through zero there.")},
        "q3": ("A branch of self-similar profiles nobody has proved, in the family this "
               "project has the most machinery for, with a SIGN CHANGE in c_l at "
               "a ~ 0.2329 that a certificate would have to straddle.  Ranked second and "
               "not first because it adds a branch to a family whose smooth profiles "
               "were classified analytically in 2023 -- the contribution is real but "
               "narrower than a first non-symmetric certificate."),
        "our_machinery": ("solver/gclm_family.py::GCLMResidual is the right residual "
                          "object; the degeneracy constraint at the origin is new."),
    },
    {
        "rank": 3,
        "id": "Boussinesq_S2_nonsymmetric",
        "object": ("2D Boussinesq, the NON-SYMMETRIC regular profile "
                   "(Chen-Huang-Li Scenario 2, 2D)"),
        "source": "arXiv:2604.01868 section 6.2",
        "certified": "NO",
        "q1": "Numerical only, April 2026.  Same status as rank 1, in 2D.",
        "q2": {"dim": 2, "n_fields": 2, "n_modulation": 3,
               "nonlocal": "2D Biot-Savart, no symmetry reduction available",
               "note": ("Scenario 2 REMOVES the symmetry constraint, so the velocity "
                        "recovery runs on the full domain rather than a quadrant -- "
                        "strictly more expensive than the certified Chen-Hou object, on "
                        "top of an extra modulation constant.")},
        "published": {"ratio_cl_over_comega": -2.4489,
                      "note": "'remarkably close to the 1D case' (-2.5114)."},
        "q3": ("The same methodological first as rank 1, on the object that actually "
               "models 3D Euler with boundary.  Strictly more valuable and strictly "
               "harder; the right thing to attempt AFTER rank 1, not instead of it."),
        "our_machinery": ("solver/boussinesq_rescaled.py + the Route-L line-sweep "
                          "preconditioner, which is aimed at the symmetric object and "
                          "would need the third constant."),
    },
    {
        "rank": 4,
        "id": "HL_singular_steady_stability",
        "object": ("1D Hou-Luo, asymptotic STABILITY of the singular steady state "
                   "1_{X>1}(X-1)^{-1/2} (Chen-Huang-Li Conjecture 2.4)"),
        "source": "arXiv:2604.01868 Theorem 2.3 (existence) + Conjecture 2.4 (open)",
        "certified": "NO",
        "q1": ("Existence in the weak sense is PROVED (their Theorem 5.3).  Stability is "
               "an explicitly stated conjecture with numerical support only."),
        "q2": {"dim": 1, "n_fields": 2, "n_modulation": 2,
               "nonlocal": "one Hilbert transform on R",
               "note": ("The obstruction is not the unknown count, it is the SPACE: the "
                        "profile is UNBOUNDED at X = 1 and only in L^p for p < 2, so no "
                        "weighted sup-norm or H^1 certificate can hold it.  Route-D "
                        "spent eleven legs on the function space for a BOUNDED profile.")},
        "published": {"c_l": 2.0, "c_omega": -1.0,
                      "note": "exact, from the closed-form profile; c_l + 2 c_omega = 0."},
        "q3": ("Would settle a stated conjecture and would be the first certificate for "
               "a SINGULAR self-similar profile.  Ranked fourth because the function "
               "space is an open problem before the certificate is even posed, and this "
               "project's own history says that is where legs go to die."),
        "our_machinery": ("solver/hl_rescaled.py has the exact anchor (omega_bar, "
                          "U_bar_exact) and gates its steady residual already."),
    },
    {
        "rank": 5,
        "id": "Boussinesq_ChenHou",
        "object": "2D Boussinesq / 3D Euler with boundary, the Chen-Hou profile",
        "source": "arXiv:2210.07191 + Part II",
        "certified": "YES_CAP",
        "q1": "CERTIFIED BY ITS AUTHORS.  This is the object the port is currently aimed at.",
        "q2": {"dim": 2, "n_fields": 3, "n_modulation": 2,
               "nonlocal": "2D Biot-Savart with boundary",
               "note": "The calibration point for every ratio in this module."},
        "published": {"ratio_cl_over_comega": -2.9205600},
        "q3": ("Nothing.  A second certificate of a certified object demonstrates "
               "capability and produces no result.  Kept in the ledger BECAUSE it is "
               "the current target -- deleting it would hide the finding."),
        "our_machinery": "solver/port_certification.py, aimed here.",
    },
    {
        "rank": 6,
        "id": "NS_3D_selfsimilar",
        "object": "3D Navier-Stokes, exact backward self-similar profile",
        "source": "claimed by arXiv:2604.09949",
        "certified": "CLAIMED_UNUSABLE",
        "q1": ("A Clay-level claim, April 2026, with no released verification package "
               "and an ansatz excluded by Necas-Ruzicka-Sverak / Tsai under the decay "
               "its own space implies.  `ns_preprint_closure_audit` checks the one thing "
               "that CAN be checked from the manuscript -- the scalar closure -- and it "
               "holds in both the printed and the corrected form.  The arithmetic is not "
               "the problem, which is why the other reasons are decisive."),
        "q2": {"dim": 3, "n_fields": 3, "n_modulation": 2,
               "nonlocal": "3D Biot-Savart",
               "note": "Wall 2 in CLAY_ROADMAP.md section 7.3.  A dimensional wall."},
        "published": {"delta": 8.421739e-12, "M": 482.6, "K": 1.1e4},
        "q3": ("Everything, and it is not reachable.  Listed so that 'is the top target "
               "certified?' has a recorded answer instead of an assumption."),
        "our_machinery": "none, and none is planned.",
    },
]


def ledger_counts():
    """How the target ledger comes out, as counts."""
    out = {}
    for t in TARGET_LEDGER:
        out[t["certified"]] = out.get(t["certified"], 0) + 1
    return out


def uncertified_targets():
    """The answer to Route-M's gate, in rank order."""
    return [t for t in TARGET_LEDGER if t["certified"] == "NO"]


def rank_table(n_per_dim=600):
    """One row per candidate: certified?, unknown count, ratio to the certified object.

    `n_per_dim` is the per-direction resolution at which the comparison is made; it
    cancels in the DIMENSION part of the ratio and only sets the scale, so the ranking
    it produces is insensitive to the choice.  600 is used because Chen-Hou's own
    adaptive mesh is quoted at that order in Part I section 7.
    """
    rows = []
    for t in TARGET_LEDGER:
        q2 = t["q2"]
        c = cost_ratio_vs_certified(q2["dim"], q2["n_fields"], n_per_dim,
                                    q2["n_modulation"])
        rows.append({"rank": t["rank"], "id": t["id"], "certified": t["certified"],
                     "dim": q2["dim"], "n_fields": q2["n_fields"],
                     "n_modulation": q2["n_modulation"], **c})
    return sorted(rows, key=lambda r: r["rank"])


def gate_verdict():
    """Route-M's pre-committed gate: does an uncertified, reachable target exist?

    'Reachable' here is the ledger's own criterion -- an unknown count at or below the
    object that was actually certified.  It is NOT a claim that the certificate closes;
    that needs Y0 under budget, which is measured separately (M3) and on one object only.
    """
    rows = {r["id"]: r for r in rank_table()}
    live = [t for t in uncertified_targets() if rows[t["id"]]["ratio"] <= 1.0]
    return {"uncertified_count": len(uncertified_targets()),
            "uncertified_and_cheaper_than_certified": [t["id"] for t in live],
            "named_target": live[0]["id"] if live else None,
            "gate": "YES" if live else "NO"}


# ==========================================================================
# ROUTE-M2 (leg 63): THE SAME LEDGER, WITH THE LEG-57 PREDICATE AS A COLUMN
# ==========================================================================
# Stage M ranked candidates by Q1/Q2/Q3.  Legs 51-57 then refuted the METHOD's reach
# rather than any candidate, and refuted it with a predicate sharp enough to screen:
#
#     does the linearization's UNBOUNDED part act as a MULTIPLIER (diagonal in the
#     spectral basis -- cut at K and the tail inverse decays) or as a SHIFT
#     (off-diagonal, tail inverse a constant that GROWS in K)?
#
# `solver/certificate_shapes.py` (leg 57) made that predicate executable on ONE dial:
# `mu`, the strength of a `Lambda^1` dissipation.  That dial cannot screen targets,
# because the thing that separates candidate MODELS is not the strength of dissipation
# but its ORDER.  Where the crossover in that order SITS is then a measurement, and it
# is not where a size comparison against the `k/2` off-diagonal would put it -- see
# `multiplier_crossover`, which records the guess it refuted.
#
# So this section re-runs the predicate on a two-parameter dial, `nu * k^gamma`:
#
#     T[j, j] = -nu k^gamma ,   T[j+1, j] = 1 - k/2 ,   T[j-1, j] = k/2
#
# `gamma = 1` reproduces `spectral_certificate.tail_block(K, M, mu=nu)` ENTRY BY ENTRY
# -- gated in `test_target_selection.py`, because a new dial that does not contain the
# old one is a new operator, not a generalization (leg 53's wrong-operator control).
# Nothing else is rebuilt: the weight classes, the bordered inverse and the
# decay-exponent fit are imported from the modules that already own them.
#
# WHAT IS VERIFIED HERE (recomputed, reported as magnitudes):
#   M2P1  the `K`-exponent of the tail inverse as a function of the dissipation ORDER
#         `gamma` -- `screen_operator`, the executable predicate column.
#   M2P2  the crossover order `gamma*(nu)` where that exponent changes sign, by
#         bracketed bisection -- `multiplier_crossover`.  The number the ledger screens on.
#   M2P3  the `M`-divergence at `nu = 0`, i.e. that the inviscid rows are shift-shaped
#         for leg 52's measured reason and not by assertion.
#
# TRANSCRIBED, not verified: every `blowup` field of `M2_CANDIDATES` -- which model has
# a PROVED blow-up, at which dissipation order, by whom.  Those are read off abstracts
# and surveys (`writeup/novelty/leg_63.md` has the queries and the links) and are exactly
# as good as that.  The provenance sits on the row so the next pass can check the quote
# instead of trusting it.
# --------------------------------------------------------------------------

from solver.certificate_shapes import (            # noqa: E402  (ledger first, by design)
    MULTIPLIER, SHIFT, TRIDIAGONAL_DOMINANT, decay_exponent,
)
from solver.spectral_certificate import (          # noqa: E402
    bordered_tail_inverse_norm, tail_block,
)

#: nonzero diagonal, and the tail inverse still GROWS in K.  Not in leg 57's vocabulary
#: because leg 57's dial could not reach it: at `gamma = 1` the diagonal/off-diagonal
#: ratio is `2 nu`, independent of `k`, so this state only appears once the ORDER is
#: allowed below 1.  For the certificate it is on the SHIFT side -- nothing to decay with.
TRIDIAGONAL_SUBDOMINANT = "TRIDIAGONAL_SUBDOMINANT"

#: the closed vocabulary a screened row may carry.  `TRIDIAGONAL_DOMINANT` is leg 57's
#: label, earned from BDL-admissibility, and this dial never emits it -- it is listed so
#: the vocabulary stays one set across the two modules instead of forking quietly.
M2_SHAPES = (MULTIPLIER, SHIFT, TRIDIAGONAL_DOMINANT, TRIDIAGONAL_SUBDOMINANT)

#: the predicate's verdict vocabulary, kept separate from the shape label so a row can
#: never be quoted as "multiplier" without the measured exponent that licensed it
MULTIPLIER_SIDE = "MULTIPLIER_SIDE"
SHIFT_SIDE = "SHIFT_SIDE"

#: memo for `screen_operator`, keyed on its full argument list -- see its docstring
_SCREEN_CACHE = {}


def fractional_tail_block(K, M, nu=0.0, gamma=1.0):
    """The tail block with a dissipation of ORDER `gamma`: diagonal `-nu k^gamma`.

    Identical to `spectral_certificate.tail_block(K, M, mu=nu)` when `gamma == 1`, and
    that identity is a gated test rather than a comment.
    """
    K, M = int(K), int(M)
    T = tail_block(K, M, mu=0.0)
    if nu:
        k = np.arange(K + 1, M + 1, dtype=float)
        T[np.diag_indices_from(T)] -= float(nu) * k ** float(gamma)
    return T


def _log_weight(k, kind, param):
    """The three weight classes, exactly as `spectral_certificate` defines them."""
    if kind == "flat":
        return np.zeros_like(k)
    if kind == "algebraic":
        return float(param) * np.log1p(k)
    if kind == "geometric":
        return k * np.log(float(param))
    raise ValueError(kind)


def _tridiagonal_inverse(Ts):
    """The inverse of a tridiagonal matrix by Thomas elimination, O(n^2) not O(n^3).

    The tail block is tridiagonal by construction, and on this machine a dense
    `np.linalg.inv` at `n = 768` costs about ten seconds, which prices the crossover
    bisection out of existence.  This is the same arithmetic at a lower exponent.

    **No pivoting**, so it is not unconditionally safe: it returns `None` whenever the
    elimination meets a zero (or denormal) pivot, and every caller falls back to the
    dense inverse in that case.  `test_target_selection.py` gates the fast path against
    the dense one across the whole dial, because a fast number that disagrees with the
    slow one is not an optimization, it is a second operator.
    """
    n = Ts.shape[0]
    a = np.diag(Ts, -1)
    b = np.diag(Ts).astype(float).copy()
    c = np.diag(Ts, 1)
    if not np.all(np.isfinite(b)) or np.min(np.abs(b)) == 0.0:
        return None
    X = np.eye(n)
    cp = np.zeros(max(n - 1, 1))
    if abs(b[0]) < 1e-300:
        return None
    if n > 1:
        cp[0] = c[0] / b[0]
    X[0] /= b[0]
    for i in range(1, n):
        m = b[i] - a[i - 1] * cp[i - 1]
        if abs(m) < 1e-300:
            return None
        if i < n - 1:
            cp[i] = c[i] / m
        X[i] = (X[i] - a[i - 1] * X[i - 1]) / m
    for i in range(n - 2, -1, -1):
        X[i] -= cp[i] * X[i + 1]
    return X


def fractional_tail_inverse_norm(K, M, kind="flat", param=0.0, nu=0.0, gamma=1.0,
                                 dense=False):
    """||T_tail^{-1}||_w with a dissipation of order `gamma`.  A magnitude, never a flag."""
    T = fractional_tail_block(K, M, nu=nu, gamma=gamma)
    k = np.arange(int(K) + 1, int(M) + 1, dtype=float)
    lw = _log_weight(k, kind, param)
    Ts = T * np.exp(lw[:, None] - lw[None, :])
    A = None if dense else _tridiagonal_inverse(Ts)
    if A is None:
        A = np.linalg.inv(Ts)
    return float(np.max(np.abs(A).sum(0)))


def screen_m_divergence(nu, gamma, K=8, Ms=(128, 256, 512, 1024), kind="flat", param=0.0):
    """Does the tail inverse EXIST as M -> infinity?  Growth in M at fixed K.

    The question `certificate_shapes.m_divergence` asks on the `Lambda^1` dial, asked on
    the order dial.  Linear growth means the tail operator is not boundedly invertible at
    all and a certificate must border it (leg 52).
    """
    Ms = [int(m) for m in Ms]
    vals = [fractional_tail_inverse_norm(K, m, kind, param, nu=nu, gamma=gamma)
            for m in Ms]
    s, _ = np.polyfit(np.log(Ms), np.log(vals), 1)
    return {"M": Ms, "vals": vals, "exponent_in_M": float(s),
            "ratio_last_over_first": float(vals[-1] / vals[0])}


def screen_operator(nu, gamma, Ks=(4, 8, 16, 32, 64), M=768, kind="flat", param=0.0,
                    border="analytic", Ms=(128, 256, 512, 1024)):
    """THE PREDICATE, measured: is the unbounded part a multiplier or a shift?

    The rule is leg 57's, unchanged -- if the tail block is boundedly invertible use the
    unbordered inverse, otherwise the honest object is the BORDERED one -- and the verdict
    is read off the SIGN of the `K`-exponent, which is returned next to it so the verdict
    can never be quoted without its magnitude.

    Bordering is only ever reached at `nu = 0`, where the bordered object is exactly the
    one `spectral_certificate.bordered_tail_inverse_norm` already owns; the order dial is
    vacuous there because there is no diagonal to give an order to.

    Memoized on its full argument list.  The inviscid rows of the ledger all screen the
    SAME operator -- the shape is a property of the operator, not of the target, which is
    lesson 87 and the reason this column can be computed at all -- so without the memo the
    ledger would pay for the identical bordered inverse four times over.
    """
    nu, gamma = float(nu), float(gamma)
    key = (nu, gamma, tuple(int(K) for K in Ks), int(M), kind, float(param), border,
           tuple(int(m) for m in Ms))
    if key in _SCREEN_CACHE:
        return dict(_SCREEN_CACHE[key])
    md = screen_m_divergence(nu, gamma, K=int(Ks[0]) * 2, Ms=Ms, kind=kind, param=param)
    invertible = md["exponent_in_M"] < 0.25
    if invertible:
        vals = [fractional_tail_inverse_norm(int(K), M, kind, param, nu=nu, gamma=gamma)
                for K in Ks]
    else:
        vals = [bordered_tail_inverse_norm(int(K), M, kind, param, border, mu=0.0)
                for K in Ks]
    de = decay_exponent([int(K) for K in Ks], vals, tail=min(4, len(Ks)))
    decays = None if de.get("refused") else de["exponent"] < 0.0
    if not invertible:
        shape = SHIFT
    elif decays:
        shape = MULTIPLIER
    else:
        # nonzero diagonal, tail inverse still GROWS.  Never TRIDIAGONAL_DOMINANT: leg 57
        # earned that label from BDL-admissibility, and a diagonal that does not buy decay
        # has not dominated anything the certificate cares about.
        shape = TRIDIAGONAL_SUBDOMINANT
    out = {"nu": nu, "gamma": gamma, "shape": shape,
            "predicate": MULTIPLIER_SIDE if decays else SHIFT_SIDE,
            "tail_block_boundedly_invertible": bool(invertible),
            "needed_bordering": not invertible,
            "M_exponent": md["exponent_in_M"],
            "K": [int(K) for K in Ks], "tail_inverse": vals,
            "K_exponent": de.get("exponent"),
            "tail_inverse_decays": decays,
            "ratio_last_over_first": de.get("ratio_last_over_first")}
    _SCREEN_CACHE[key] = out
    return dict(out)


def multiplier_crossover(nu, lo=0.05, hi=2.0, tol=0.02, Ks=(4, 8, 16, 32, 64), M=768,
                         kind="flat", param=0.0, Ms=(128, 256, 512)):
    """The ORDER `gamma*(nu)` at which the tail inverse stops growing and starts decaying.

    Bisection on the sign of the measured `K`-exponent.  `lo` must come out shift-side and
    `hi` multiplier-side or the bracket is REFUSED rather than reported -- a crossover
    quoted from an unbracketed bisection is a number with no content.

    **THE HYPOTHESIS THIS FUNCTION KILLED, KEPT BECAUSE IT WAS THIS LEG'S OWN.**  The
    obvious guess is `gamma* = 1`: the transport off-diagonal grows like `k/2`, so the
    diagonal `nu k^gamma` should have to grow faster than `k` to win.  **It is false, and
    by a wide margin** -- the measured crossover is far below 1 (see
    `writeup/data/p2_route_m2_v1_targets.json`).  Entry-wise dominance is not the
    coordinate; the tail inverse is set by the *recursion*, and a diagonal that is
    pointwise much smaller than the off-diagonal still breaks it.  This is leg 57's
    `delta < 1/2` lesson repeating on a different dial: the threshold a size comparison
    predicts is not the threshold the operator has.
    """
    def f(g):
        return screen_operator(nu, g, Ks=Ks, M=M, kind=kind, param=param, Ms=Ms)
    a, b = float(lo), float(hi)
    fa, fb = f(a), f(b)
    if fa["predicate"] != SHIFT_SIDE or fb["predicate"] != MULTIPLIER_SIDE:
        return {"refused": True, "reason": "bracket does not straddle the crossover",
                "lo": {"gamma": a, "predicate": fa["predicate"],
                       "K_exponent": fa["K_exponent"]},
                "hi": {"gamma": b, "predicate": fb["predicate"],
                       "K_exponent": fb["K_exponent"]}}
    n = 0
    while b - a > float(tol):
        m = 0.5 * (a + b)
        if f(m)["predicate"] == MULTIPLIER_SIDE:
            b = m
        else:
            a = m
        n += 1
    return {"refused": False, "nu": float(nu), "gamma_star": 0.5 * (a + b),
            "bracket": [a, b], "iterations": n, "tol": float(tol),
            "K_exponent_below": f(a)["K_exponent"],
            "K_exponent_above": f(b)["K_exponent"]}


# --------------------------------------------------------------------------
# THE M2 CANDIDATES -- uncertified targets on models where blow-up is PROVABLE
# --------------------------------------------------------------------------
# Stage M's `TARGET_LEDGER` is left EXACTLY as it was: it records an answered gate and
# rewriting it would destroy that record.  These rows are the ones the leg-57 predicate
# makes newly relevant -- DISSIPATIVE models, which stage M never considered because
# until leg 51 nobody knew the shape of the unbounded part was the deciding variable.
# Each carries the same fields as a `TARGET_LEDGER` row plus:
#
#   `dissipation`  {"gamma": the order of Lambda in the model's own dissipation,
#                   "nu": the strength at which the predicate is evaluated}
#   `blowup`       {"provable", "where", "kind", "source", "quote"} -- TRANSCRIBED.
#                  `provable` answers the gate's "on a model where blow-up is provable",
#                  which is a statement about the MODEL, not about the specific profile.
M2_CANDIDATES = [
    {
        "rank": 1,
        "id": "gCLM_Lambda2_viscous_profiles",
        "object": ("gCLM with FULL Laplacian dissipation, nu Lambda^2 -- self-similar "
                   "profiles off the proved neighbourhood of a = 1/2, i.e. the viscous "
                   "unimodal branch that exists only as numerics"),
        "source": "arXiv:1908.09385 (the proof) + the viscous unimodal numerics",
        "certified": "NO",
        "q1": ("No computer-assisted certificate of ANY dissipative self-similar profile "
               "was located (leg 63 novelty pass, Q4): every certificate in this family "
               "-- Chen-Hou-Huang for inviscid De Gregorio/gCLM, Chen-Hou for 2D "
               "Boussinesq -- is inviscid.  The dissipative blow-up result that does "
               "exist is ANALYTIC and local in a ('a close to 1/2'); profiles off that "
               "neighbourhood are numerical only."),
        "q2": {"dim": 1, "n_fields": 1, "n_modulation": 2,
               "nonlocal": "one Hilbert transform on R, plus a Lambda^2 diagonal",
               "note": ("The cheapest shape in either ledger AND the only one whose tail "
                        "block the standard estimate can invert unaided: the k^2 diagonal "
                        "beats the k/2 transport off-diagonal by a whole power of k, so "
                        "no bordering is needed and Y_0 is not competing against a "
                        "constant tail inverse.")},
        "dissipation": {"gamma": 2.0, "nu": 0.1},
        "blowup": {"provable": "YES",
                   "where": "a close to 1/2, gamma = 2",
                   "kind": "ANALYTIC",
                   "source": "https://arxiv.org/abs/1908.09385",
                   "quote": ("'We use the method in [chen2019finite] to prove finite time "
                             "self-similar blowup for a close to 1/2 and gamma=2' -- "
                             "abstract, fetched verbatim.  The a-neighbourhood is NOT "
                             "quantified there and the nu-dependence is not stated.  "
                             "TRANSCRIBED from the abstract, not read at full text.")},
        "published": {"note": ("No (c_l, c_omega) table at gamma = 2 was transcribed this "
                               "leg.  A promotion leg must read arXiv:1908.09385 at full "
                               "text and pull the constants before any residual is "
                               "computed -- this row is scoping, not a specification.")},
        "q3": ("The first computer-assisted certificate of a DISSIPATIVE self-similar "
               "blow-up profile, in the one family where dissipative blow-up is proved to "
               "exist at all.  It is also the only row in either ledger whose "
               "linearization the method's tail estimate is SHAPED for, which is the whole "
               "point of the screen: legs 51-57 did not run out of targets, they ran out "
               "of targets of the right shape."),
        "our_machinery": ("solver/gclm_family.py owns the residual and "
                          "solver/fractional_gclm.py owns the criticality exponent "
                          "s_c = alpha/2; adding a diagonal Lambda^2 to a spectral "
                          "residual is the cheapest modification in the repository."),
    },
    {
        "rank": 2,
        "id": "CCF_fractional_subcritical",
        "object": ("Cordoba-Cordoba-Fontelos nonlocal flux with fractional dissipation "
                   "Lambda^gamma, in the range where blow-up is proved"),
        "source": ("Li-Rodrigo, SIAM J. Math. Anal., doi:10.1137/100794924; "
                   "Kiselev, arXiv:1009.0540"),
        "certified": "NO",
        "q1": ("Blow-up is PROVED at small order; no computer-assisted certificate of a "
               "self-similar profile was located."),
        "q2": {"dim": 1, "n_fields": 1, "n_modulation": 2,
               "nonlocal": "one Hilbert transform on R, plus a Lambda^gamma diagonal",
               "note": ("Same cost class as rank 1.  The entire difference between the two "
                        "rows is the ORDER of the dissipation, which is exactly the "
                        "variable the screen measures.")},
        "dissipation": {"gamma": 0.5, "nu": 0.1},
        "blowup": {"provable": "YES",
                   "where": ("small order only -- the located ranges are Lambda^{2 alpha} "
                             "with alpha < 1/4, extended in parts of the literature toward "
                             "alpha = 1/2, i.e. gamma < 1 at the most generous reading"),
                   "kind": "ANALYTIC",
                   "source": "https://arxiv.org/pdf/1009.0540",
                   "quote": ("The range alpha in [1/2, 1] is stated as a longstanding OPEN "
                             "problem, i.e. the proved region stops below it.  TRANSCRIBED "
                             "from surveys, not full text.  The row is evaluated at the "
                             "GENEROUS end of the proved range, which makes the screen "
                             "harder to pass, not easier.")},
        "published": {"note": "no profile constants transcribed this leg"},
        "q3": ("Would be the first certificate for a dissipative CCF profile.  Ranked "
               "below rank 1 for one measured reason and not for taste: its dissipation "
               "ORDER sits below the measured crossover, so the method's tail estimate has "
               "nothing to decay with there either."),
        "our_machinery": "solver/gclm.py's Hilbert transform; nothing else.",
    },
]


def m2_ledger():
    """Stage M's UNCERTIFIED rows plus the dissipative candidates the predicate reaches.

    Stage M's rows enter at `gamma = 0`, which is not an assumption about them -- it is
    what their models are.  The predicate is then MEASURED on each, never assigned.
    """
    rows = []
    for t in uncertified_targets():
        r = dict(t)
        r["dissipation"] = {"gamma": 0.0, "nu": 0.0}
        r["blowup"] = {"provable": "YES", "where": "inviscid model",
                       "kind": "CAP+ANALYTIC",
                       "source": "arXiv:2210.07191 / arXiv:2308.01528, and the M ledger",
                       "quote": ("Blow-up is established for the inviscid Hou-Luo / gCLM / "
                                 "Boussinesq family; what is uncertified is the specific "
                                 "profile, which is what these rows are.")}
        r["origin"] = "TARGET_LEDGER"
        rows.append(r)
    for c in M2_CANDIDATES:
        r = dict(c)
        r["origin"] = "M2_CANDIDATES"
        rows.append(r)
    return rows


def m2_rank_table(Ks=(4, 8, 16, 32, 64), M=768, n_per_dim=600):
    """One row per M2 candidate with the PREDICATE MEASURED, ranked by it.

    Ranking rule, pre-committed, in this order:
      1. the predicate -- MULTIPLIER_SIDE first.  It dominates everything else because
         legs 51-57 measured that the shift side costs the method its tail estimate
         outright, not by a factor.
      2. blow-up provability on the model -- the prize's own wording.
      3. cost, via stage M's `cost_ratio_vs_certified`, unchanged.
    """
    rows = []
    for t in m2_ledger():
        d = t["dissipation"]
        s = screen_operator(d["nu"], d["gamma"], Ks=Ks, M=M)
        q2 = t["q2"]
        c = cost_ratio_vs_certified(q2["dim"], q2["n_fields"], n_per_dim,
                                    q2["n_modulation"])
        rows.append({"id": t["id"], "origin": t["origin"], "certified": t["certified"],
                     "gamma": d["gamma"], "nu": d["nu"],
                     "predicate": s["predicate"], "shape": s["shape"],
                     "K_exponent": s["K_exponent"],
                     "tail_inverse_first": s["tail_inverse"][0],
                     "tail_inverse_last": s["tail_inverse"][-1],
                     "ratio_last_over_first": s["ratio_last_over_first"],
                     "needed_bordering": s["needed_bordering"],
                     "M_exponent": s["M_exponent"],
                     "blowup_provable": t["blowup"]["provable"],
                     "blowup_where": t["blowup"]["where"],
                     "blowup_kind": t["blowup"]["kind"],
                     "blowup_source": t["blowup"]["source"],
                     "ratio": c["ratio"], "unknowns": c["unknowns"]})
    rows.sort(key=lambda r: (0 if r["predicate"] == MULTIPLIER_SIDE else 1,
                             0 if r["blowup_provable"] == "YES" else 1,
                             r["ratio"]))
    for i, r in enumerate(rows, 1):
        r["m2_rank"] = i
    return rows


#: The constraint a YES verdict must be quoted WITH, every time.  It lives in the module
#: rather than in prose so that it cannot be dropped in a summary.
M2_LIFT_CONSTRAINT = (
    "Every multiplier-side row in this ledger is DISSIPATIVE.  plan_of_record.py bans "
    "re-opening stage V as posed, and its lift condition reads 'unless the question is "
    "re-posed for a FLUID transport model, which needs L1 first'.  L1 is measured dead in "
    "both realizations (legs 51-54).  Whether that lift condition can ever be met is "
    "therefore a USER call.  Leg 63 surfaces it and does not make it: this ledger is "
    "scoping, and nothing in it promotes a row into the committed sequence."
)


def m2_gate_verdict(rows=None):
    """Leg 63's pre-committed gate, answered from the measured column.

    "Is there at least one uncertified target, on a model where blow-up is provable,
    whose linearization's unbounded part is a MULTIPLIER under the leg-57 predicate?"

    A YES is SCOPING, not promotion: promoting any row into the committed sequence is
    escalation #1, and this module does not make that call.  The blocking constraint
    travels WITH the verdict rather than being left in prose.
    """
    rows = m2_rank_table() if rows is None else rows
    live = [r for r in rows
            if r["predicate"] == MULTIPLIER_SIDE
            and r["certified"] == "NO"
            and r["blowup_provable"] == "YES"]
    return {"gate": "YES" if live else "NO",
            "n_rows": len(rows),
            "n_multiplier_side": sum(1 for r in rows if r["predicate"] == MULTIPLIER_SIDE),
            "multiplier_side_ids": [r["id"] for r in live],
            "top_candidate": live[0]["id"] if live else None,
            "top_K_exponent": live[0]["K_exponent"] if live else None,
            "promotion": "ESCALATION_1_USER_CALL -- this module promotes nothing",
            "blocked_by": M2_LIFT_CONSTRAINT if live else None}
