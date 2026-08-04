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
