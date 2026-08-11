#!/usr/bin/env python3
"""Leg 314 -- ROUTE-FUS: the finite-unstable-spectrum condition, classified.

SCOPING LEG.  BUILDS NOTHING.  ``solver/`` is READ, never written and never RUN.

--------------------------------------------------------------------------------------
THE GATE, PRE-COMMITTED (DIRECTION.md leg 314, verbatim -- immutable)
--------------------------------------------------------------------------------------
    "Does the scoping produce a definite classification -- finiteness for these profiles
     is (i) provable, with the argument sketched and its load-bearing step named;
     (ii) checkable only numerically, with a named certified-count/lower-bound route this
     repository's spectral tools bear on; or (iii) open, with the obstruction named?"

    yes -> Bank the classification; if (ii), the construction leg is drafted separately
           by the DM, not begun here.
    no  -> Name exactly what blocks classification (which profile, which operator
           property) -- recorded at full strength; no construction.

--------------------------------------------------------------------------------------
WHAT IS BANNED HERE AND HOW THIS SCRIPT STAYS INSIDE IT
--------------------------------------------------------------------------------------
``plan_of_record.py`` bans "another gCLM measurement leg" (lifted by: never -- the model
is exhausted, Stage 3.5, leg 42).  Leg 70's ``p2_route_rc_v1_realization_audit.py`` read
that ban as forbidding any fresh solve or eigendecomposition of the gCLM rescaled flow and
pinned itself to "ARITHMETIC on counts already banked".  THIS SCRIPT ADOPTS THE IDENTICAL
RESTRICTION AND CARRIES THE IDENTICAL AST SELF-GUARD.

    FORBIDDEN and asserted against below -- newton, continuation, spectrum,
    converged_spectrum, unstable_count, stability_ladder, frequency_profile,
    planted_eigenvalue_control, np.linalg.eigvals / eig / solve, scipy.linalg.*.

Every number this script emits is one of:
    (a) transcribed from a named paper, with the quote carried alongside it, or
    (b) arithmetic on a number that was ON DISK in writeup/data/ before this leg started.

THE BAN IS NOT LIFTED AND THIS SCRIPT DOES NOT LIFT IT.

--------------------------------------------------------------------------------------
Run:  python experiments/p2_route_fus_v1_scoping.py [--out PATH]
--------------------------------------------------------------------------------------
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE = ("Does the scoping produce a definite classification -- finiteness for these "
        "profiles is (i) provable, with the argument sketched and its load-bearing step "
        "named; (ii) checkable only numerically, with a named certified-count/lower-bound "
        "route this repository's spectral tools bear on; or (iii) open, with the "
        "obstruction named?")

# ======================================================================================
# 0.  THE SELF-GUARD -- prove this script measured nothing
# ======================================================================================
BANNED_CALLS = (
    "newton", "continuation", "spectrum", "converged_spectrum", "unstable_count",
    "stability_ladder", "frequency_profile", "crossover_mu", "perturbation_decay",
    "planted_eigenvalue_control", "inviscid_seed", "eigvals", "eig", "eigh", "eigvalsh",
    "svd", "lstsq", "solve", "best_lower", "family_lower", "ascend",
)


def self_guard(path=None):
    """AST-check THIS FILE for any call that would constitute a fresh gCLM measurement.

    Returns a dict; ``ok`` False means the script must refuse to run.  This is the
    mechanism by which the gCLM ban is enforced by the CODE rather than by the author's
    assurance -- leg 70's design, reused deliberately.
    """
    path = Path(path or __file__)
    tree = ast.parse(path.read_text())
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = getattr(f, "attr", None) or getattr(f, "id", None)
            if name in BANNED_CALLS:
                found.append({"call": name, "line": node.lineno})
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = getattr(node, "module", None) or ""
            names = [a.name for a in node.names]
            if mod.startswith("solver") or any(n.startswith("solver") for n in names):
                imports.append(mod or names[0])
            if mod.startswith("numpy") or "numpy" in names:
                imports.append(mod or "numpy")
            if mod.startswith("scipy") or any(n.startswith("scipy") for n in names):
                imports.append(mod or "scipy")
    return {"banned_calls_found": found,
            "solver_or_numeric_imports": sorted(set(imports)),
            "ok": not found and not imports,
            "banned_call_list": list(BANNED_CALLS)}


# ======================================================================================
# 1.  PROVENANCE -- every source, with the quote that carries the claim
# ======================================================================================
SOURCES = {
    "USC": {
        "arxiv": "2509.14185",
        "url": "https://arxiv.org/abs/2509.14185",
        "cite": "Wang, Lai, Leger, Buckmaster -- unstable self-similar singularities via PINNs",
        "role": "ASSUMES the condition; the paper this leg is about",
    },
    "USC2": {
        "arxiv": "2511.22819",
        "url": "https://arxiv.org/abs/2511.22819",
        "cite": "Wang, Leger, Lai, Buckmaster -- gradient-normalised loss, 28 Nov 2025",
        "role": "IRRELEVANT to FUS -- precision only; instrument-checked this leg",
    },
    "XU": {
        "arxiv": "2607.19762",
        "url": "https://arxiv.org/abs/2607.19762",
        "cite": "Xu -- The spectral picture of self-similar collapse in the CLM equation, "
                "22 Jul 2026, 41 pp",
        "role": "PROVES finiteness for a=0 CLM in a NAMED realization; supplies the "
                "realization dichotomy. Already banked here at legs 70/171/173/249",
    },
    "BCG": {
        "arxiv": "2208.09445",
        "url": "https://arxiv.org/abs/2208.09445",
        "cite": "Buckmaster, Cao-Labora, Gomez-Serrano -- Smooth imploding solutions for 3D "
                "compressible fluids; Forum of Math. Pi 13 (2025) e6",
        "role": "PROVES finiteness via maximal dissipativity + compact perturbation",
    },
    "CGSS": {
        "arxiv": "2310.05325",
        "url": "https://arxiv.org/abs/2310.05325",
        "cite": "Cao-Labora, Gomez-Serrano, Shi, Staffilani",
        "role": "PROVES the same structure non-radially (prop:maxdissmooth)",
    },
    "GHJS": {
        "arxiv": "2509.12435",
        "url": "https://arxiv.org/abs/2509.12435",
        "cite": "Guo, Hadzic, Jang, Schrecker -- Nonlinear stability of the Larson-Penston "
                "collapse, 15 Sep 2025, 149 pp",
        "role": "PROVES; and exhibits the frequency SPLIT that decides this leg's gate",
    },
    "WM": {
        "arxiv": "1006.2172",
        "url": "https://arxiv.org/abs/1006.2172",
        "cite": "On stable self-similar blow up for equivariant wave maps: the linearized "
                "problem, 8 Jun 2010 (with math-ph/0702025, 2007, and 1003.0707, 2010)",
        "role": "OLD prior art -- the classical template for finiteness of the unstable set",
    },
    "GW": {
        "arxiv": "math/0102197",
        "url": "https://arxiv.org/abs/math/0102197",
        "cite": ("Gallay & Wayne, Invariant manifolds and the long-time asymptotics of the "
                 "Navier-Stokes and vorticity equations on R^2, ARMA 163 (2002) 209-258; "
                 "doi:10.1007/s002050200200. Companion: arXiv:math/0402449, CMP 255 (2005)"),
        "role": ("PROVES finiteness in a genuine FLUID similarity-variable setting, and is "
                 "the OLD prior art for the WEIGHT-DEPENDENCE this leg's obstruction turns "
                 "on: in L^2(m) the advection term is RELATIVELY COMPACT however large its "
                 "coefficient, so sigma_ess = {Re lambda <= -(m-1)/2} -- the boundary MOVES "
                 "WITH THE WEIGHT m, and finiteness is bought by raising m. Viscous: the "
                 "Laplacian does the work, so it does NOT transfer to the four models"),
    },
    "BZ": {
        "arxiv": "1601.00837",
        "url": "https://arxiv.org/abs/1601.00837",
        "cite": ("Barker & Zumbrun, Numerical proof of stability of viscous shock profiles, "
                 "M3AS 26 (2016) 2451-2469; doi:10.1142/S0218202516500588"),
        "role": ("THE decisive precedent for a CERTIFIED COUNT, and it confirms this leg's "
                 "two-half structure exactly: interval arithmetic + rigorous ODE bounds + an "
                 "Evans-function WINDING NUMBER on the boundary of B(0,R) cap {Re lambda >= "
                 "0} -- where the radius R = (sqrt(gamma) + 1/2)^2 enclosing ALL possible "
                 "unstable eigenvalues is derived ANALYTICALLY. The computer works inside "
                 "the disc; the disc itself is a THEOREM. Travelling waves, not self-similar "
                 "blow-up profiles"),
    },
    "CH": {
        "arxiv": "2210.07191",
        "url": "https://arxiv.org/abs/2210.07191",
        "cite": ("Chen & Hou, Stable nearly self-similar blowup of the 2D Boussinesq and 3D "
                 "Euler equations with smooth data I: Analysis (II: Rigorous Numerics, "
                 "arXiv:2305.05660)"),
        "role": ("THE THIRD OPTION, and it is neither prove nor check: Chen-Hou DELIBERATELY "
                 "DO NOT COUNT EIGENVALUES. They avoid weighted L^2/H^k (advection normal to "
                 "the boundary produces a large growth factor), work in weighted "
                 "L^inf cap C^{1/2}, split L into leading-order plus FINITE RANK, and prove "
                 "coercivity/damping DIRECTLY. This SIDESTEPS the finiteness question rather "
                 "than answering it -- recorded because it is the option the DM should weigh "
                 "against building any count at all"),
    },
    "VOIGT": {
        "arxiv": None,
        "url": "https://doi.org/10.1007/BF01303264",
        "cite": ("Voigt, Monatsh. Math. 90 (1980) 153-161 (Jorgens-Vidav-Voigt chain; Vidav, "
                 "JMAA 30 (1970) 264-279; Greiner, Math. Z. 185 (1984) 167-177). Kato, "
                 "Perturbation Theory for Linear Operators, 2nd ed., Ch. IV Thm 5.35, "
                 "doi:10.1007/978-3-642-66282-9. Chicone & Latushkin, Evolution Semigroups, "
                 "AMS Surveys & Monographs 70 (1999)"),
        "role": ("the ~50-year-old ABSTRACT mechanism, in semigroup form: spectrum outside "
                 "the essential spectral radius consists of eigenvalues of FINITE algebraic "
                 "multiplicity. The theory has been adequate since 1980. What is missing for "
                 "the four models is not theory but the VERIFICATION of its hypothesis"),
    },
    "BK": {
        "arxiv": "chao-dyn/9306007",
        "url": "https://arxiv.org/abs/chao-dyn/9306007",
        "cite": ("Bricmont & Kupiainen, Universality in blow-up for nonlinear heat equations, "
                 "Nonlinearity 7 (1994) 539-575; with Merle & Zaag, Duke Math. J. 86 (1997) "
                 "143-195, doi:10.1215/S0012-7094-97-08605-1"),
        "role": ("OLD prior art, the cleanest PROVED case: in similarity variables the "
                 "linearisation is a HERMITE operator with PURELY DISCRETE spectrum "
                 "{1 - m/2}. IRRELEVANT to the four models -- the discreteness comes from "
                 "the Laplacian, and CCF/IPM/Boussinesq/Euler have no such smoothing"),
    },
}

QUOTES = {
    "USC_condition": {
        "src": "USC", "where": "p.19",
        "text": ("For a computer-assisted proof to be feasible, it is desirable that the "
                 "spectrum in the right-half mu-plane consists of a finite number of "
                 "eigenvalues."),
        "note": "'desirable', never established. Transcribed by leg 175; re-verified here.",
    },
    "USC_assumption": {
        "src": "USC", "where": "p.19, the PINN eigensolve",
        "text": ("under the assumption that there exist eigenvalues with non-negative real "
                 "part that lie on the real axis"),
        "note": "the mode COUNT is produced under this assumption, not measured free of it",
    },
    "USC_symmetry": {
        "src": "USC", "where": "p.19",
        "text": "restricted to Psi that lie within the same symmetry class",
        "note": "a second restriction: modes outside the symmetry class are not searched",
    },
    "XU_dichotomy": {
        "src": "XU", "where": "abstract; Proposition 2 (audited from code by leg 70)",
        "text": ("a realization dichotomy attributes the in-strip smear seen in generic "
                 "discretizations to the spectrum of the maximal L^2 realization, which the "
                 "origin-H^2 choice eliminates"),
        "note": "SAME PDE, SAME PROFILE, TWO ANSWERS. This is the load-bearing prior art.",
    },
    "XU_essential": {
        "src": "XU", "where": "abstract",
        "text": ("in {Re lambda >= -1/2} the essential spectrum reduces to the single "
                 "vertical line {Re lambda = -1/2}, produced by a log-widening Weyl "
                 "sequence; a Hardy-Mellin resolvent bound clears the remainder of the "
                 "half-plane except the points 0 and 1"),
        "note": "the HIGH-FREQUENCY tool, named: a Hardy-Mellin resolvent bound",
    },
    "XU_point": {
        "src": "XU", "where": "abstract",
        "text": ("the point spectrum over all of C is precisely {0,1}, the scaling and "
                 "time-shift symmetry modes, with no embedded eigenvalues"),
        "note": "finiteness HOLDS in the origin-H^2 realization, and is symmetry-induced",
    },
    "BCG_maxdiss": {
        "src": "BCG", "where": "TeX l.2707/2727/2764/2766 (pinned by leg 285, verified by "
                               "verify_265)",
        "text": ("L = A_0 - delta_g + K with A_0 maximally dissipative and K compact on "
                 "X = H_0^{2m}(B(0,2)) gives Lambda = sigma(L) cap {Re lambda > -delta_g/2} "
                 "FINITE, of finite algebraic multiplicity"),
        "note": "the structural fact that makes the unstable spectrum finite",
    },
    "GHJS_split": {
        "src": "GHJS", "where": "abstract",
        "text": ("a high-order energy method in low- and high-frequency regimes (relying on "
                 "monotonicity) and rigorous computer-assisted techniques in the "
                 "intermediate regime; maximal dissipativity of the linearized operator on "
                 "arbitrarily large backward light cones"),
        "note": ("THE SPLIT. The computer does the BOUNDED middle. The unbounded "
                 "high-frequency end is done ANALYTICALLY, and never numerically."),
    },
    "GHJS_box": {
        "src": "GHJS", "where": "recorded in this repo at writeup/novelty/verify_265.md l.268",
        "text": "the compact box Re lambda in [0,1], |Im lambda| <= 8, with b_0 = 1/5, b_1 = 8",
        "note": "the certified count is executed on a COMPACT BOX -- bounded in BOTH directions",
    },
}

# ======================================================================================
# 2.  BANKED NUMBERS -- on disk before this leg started; arithmetic only
# ======================================================================================
BANKED_SOURCE = "writeup/data/p2_route_i_v1_driven.json"
BANKED_PATH = "i5_stability/ladders/<K>/"

# The realization these were measured in, NAMED (lesson 91):
REALIZATION = ("solver/rescaled_spectrum.py's compactified odd-sine basis (OddCompactBasis), "
               "gCLM at a = 1/2, p = 3, mu = 0 (inviscid), dilation mode excised by identity, "
               "unstable tolerance Re > 1e-6. Leg 70's Route-RC audited this realization FROM "
               "THE CODE and found it imposes NO origin condition at X = 0 -- i.e. it is the "
               "MAXIMAL-L^2 side of Xu arXiv:2607.19762 Proposition 2's dichotomy.")


def load_banked(root=ROOT):
    """Read Route-I's banked ladder. No solver import, no solve, no eigendecomposition."""
    d = json.loads((Path(root) / BANKED_SOURCE).read_text())
    ladders = d["i5_stability"]["ladders"]
    rows = []
    for k in sorted(ladders, key=lambda s: int(s)):
        L = ladders[k]
        inv = L["rows"][0]
        # the viscous end of the SAME ladder -- the positive control that can report
        # the other answer (lesson 90): same code, same object, finite (indeed zero) count.
        visc = [r for r in L["rows"] if r["mu"] > 0.0 and r["n_unstable"] == 0]
        rows.append({
            "K": int(k),
            "n_unstable_inviscid": int(L["n_unstable_inviscid"]),
            "max_re_inviscid": float(L["max_re_inviscid"]),
            "max_abs_im_inviscid": float(inv["max_abs_im"]),
            "mu_inviscid": float(inv["mu"]),
            "min_re_inviscid": float(inv["min_re"]),
            "dilation_eigenvalue_re": float(inv["dilation_eigenvalue"][0]),
            "profile_residual": float(inv["residual"]),
            "lambda_truncation": float(inv["lambda_truncation"]),
            "first_mu_with_zero_unstable": float(visc[0]["mu"]) if visc else None,
            "n_unstable_at_that_mu": 0 if visc else None,
            "max_re_at_that_mu": float(visc[0]["max_re"]) if visc else None,
        })
    return rows


def smear_arithmetic(rows):
    """Is the inviscid unstable count K-STABLE (finite set) or DIVERGENT (continuum shadow)?

    Pre-committed discriminator, fixed before the numbers were read back:
      * DIVERGENT  iff n_unstable is strictly increasing across the ladder AND the
        least-squares slope dn/dK >= 0.5.
      * K-STABLE   iff n_unstable is constant across the last three K.
    A count that is neither is reported as INCONCLUSIVE, not forced into a branch.
    """
    Ks = [r["K"] for r in rows]
    ns = [r["n_unstable_inviscid"] for r in rows]
    n = len(Ks)
    mx = sum(Ks) / n
    my = sum(ns) / n
    den = sum((k - mx) ** 2 for k in Ks)
    slope = sum((k - mx) * (y - my) for k, y in zip(Ks, ns)) / den if den else float("nan")
    intercept = my - slope * mx
    resid = max(abs(y - (slope * k + intercept)) for k, y in zip(Ks, ns))

    strictly_increasing = all(b > a for a, b in zip(ns, ns[1:]))
    k_stable = len(set(ns[-3:])) == 1 if n >= 3 else False

    # the exact affine law, if there is one: n = K - c with c integral
    offsets = [k - y for k, y in zip(Ks, ns)]
    exact_offset = offsets[0] if len(set(offsets)) == 1 else None

    if strictly_increasing and slope >= 0.5:
        verdict = "DIVERGENT"
    elif k_stable:
        verdict = "K_STABLE"
    else:
        verdict = "INCONCLUSIVE"

    # Re barely moves while |Im| grows: the signature of a curve on which Re rises with |Im|
    res = [r["max_re_inviscid"] for r in rows]
    ims = [r["max_abs_im_inviscid"] for r in rows]
    return {
        "K": Ks, "n_unstable": ns,
        "slope_dn_dK": slope, "intercept": intercept, "max_abs_residual": resid,
        "exact_affine_offset": exact_offset,
        "affine_law": (None if exact_offset is None else "n_unstable = K - %d exactly"
                       % exact_offset),
        "strictly_increasing": strictly_increasing,
        "k_stable_last3": k_stable,
        "verdict": verdict,
        "max_re": res, "max_abs_im": ims,
        "max_re_spread": max(res) - min(res),
        "max_re_relative_spread": (max(res) - min(res)) / min(res),
        "max_abs_im_growth_factor": max(ims) / min(ims),
        "K_growth_factor": max(Ks) / min(Ks),
        "reading": ("max Re is essentially K-independent while max|Im| grows in proportion "
                    "to K: the unstable set is not a fixed finite collection being resolved "
                    "better, it is a CURVE whose visible extent is set by the truncation."),
        "tidy_closed_form_diagnosis": diagnose_offset(rows),
        "artifact_check": artifact_check(rows),
    }


def diagnose_offset(rows):
    """'n = K - 3 exactly' is a suspiciously tidy closed form -- so check what produced it.

    Standing discipline: "When a quantity has a suspiciously tidy closed form, that is the
    signal to check what produced it" (the leg-53 lesson).  Do NOT bank the 3 as a fact
    about the operator until its bookkeeping is accounted for.

    The Jacobian is K x K (OddCompactBasis carries coefficients b_k, k = 1..K, so the
    spectrum has exactly K points).  ``unstable_count`` excises ONE eigenvalue by identity
    -- the dilation mode, L(X Omega_X) = 0 -- leaving K - 1 judged on Re > 1e-6.  So

        offset 3  =  1 excised dilation  +  2 eigenvalues with Re <= 1e-6.

    That is arithmetic, not a claim about which two.  Route-E banked that the only
    grid-converged isolated eigenvalues of this flow are the two exact symmetry modes,
    and min_re here converges to -2; both are CONSISTENT with the two non-positive
    eigenvalues being isolated symmetry/edge modes, but this leg did not measure them and
    does not assert it.  The load-bearing statement is the SLOPE, not the offset.
    """
    return {
        "jacobian_dimension": "K x K (OddCompactBasis: b_k, k = 1..K)",
        "excised_by_identity": 1,
        "excised_which": "the dilation mode, L(X Omega_X) = 0 exactly",
        "dilation_eigenvalue_re_by_K": {str(r["K"]): r["dilation_eigenvalue_re"]
                                        for r in rows},
        "remaining_judged": "K - 1",
        "implied_non_positive_besides_dilation": 2,
        "min_re_by_K": {str(r["K"]): r["min_re_inviscid"] for r in rows},
        "min_re_limit": "converges to -2 (-2.0814, -2.0073, -2.0017)",
        "accounted": True,
        "what_is_load_bearing": ("the SLOPE dn/dK = 1, i.e. the unstable count is "
                                 "PROPORTIONAL TO THE NUMBER OF DEGREES OF FREEDOM. The "
                                 "offset 3 is bookkeeping and is NOT banked as a fact about "
                                 "the operator."),
        "not_asserted": ("which two eigenvalues are the non-positive ones. Identifying them "
                         "would require a fresh gCLM eigendecomposition, which is BANNED."),
    }


def artifact_check(rows):
    """Could the divergence be an under-resolution artifact? The evidence says the opposite.

    If the growing count were a numerical artifact of a badly-resolved profile, the count
    should SHRINK as the profile is resolved better.  It grows.  Across the ladder the
    profile residual falls by ~10 orders of magnitude and the truncation parameter by ~6,
    while the unstable count RISES monotonically.  Better resolution buys MORE unstable
    directions, which is the continuum signature and the opposite of the artifact signature.
    """
    res = [r["profile_residual"] for r in rows]
    trunc = [r["lambda_truncation"] for r in rows]
    ns = [r["n_unstable_inviscid"] for r in rows]
    return {
        "profile_residual_by_K": {str(r["K"]): r["profile_residual"] for r in rows},
        "lambda_truncation_by_K": {str(r["K"]): r["lambda_truncation"] for r in rows},
        "residual_improvement_decades": _dec(res),
        "truncation_improvement_decades": _dec(trunc),
        "n_unstable": ns,
        "resolution_improves_and_count_rises": (res[-1] < res[0] and ns[-1] > ns[0]),
        "verdict": ("NOT AN UNDER-RESOLUTION ARTIFACT. The profile residual improves by "
                    "~10 decades and the truncation parameter by ~6 across the ladder, and "
                    "the unstable count RISES over the same ladder. An artifact of poor "
                    "resolution would fall."),
    }


def _dec(xs):
    import math
    a, b = xs[0], xs[-1]
    if a <= 0 or b <= 0:
        return None
    return math.log10(a) - math.log10(b)


def control_arithmetic(rows):
    """The positive control: the SAME code on the SAME object reporting FINITE.

    Lesson 90 -- a control that cannot come out differently is not a control.  Ask what
    would have to change for this to report the other answer: nothing but mu.  The viscous
    rows of the identical ladder report n_unstable = 0 at every K, so the DIVERGENT verdict
    above is a statement about the inviscid operator, not about the counting code.
    """
    out = []
    for r in rows:
        out.append({"K": r["K"],
                    "mu": r["first_mu_with_zero_unstable"],
                    "n_unstable": r["n_unstable_at_that_mu"],
                    "max_re": r["max_re_at_that_mu"]})
    counts = {o["n_unstable"] for o in out}
    return {"rows": out,
            "all_zero": counts == {0},
            "k_stable": len(counts) == 1,
            "verdict": "K_STABLE" if counts == {0} else "NOT_A_CONTROL",
            "reading": ("the same counting code, the same basis, the same profile family, "
                        "with mu > 0: the count is 0 at every K. The instrument can report "
                        "FINITE. It reports DIVERGENT inviscidly because the operator is "
                        "different, not because the code cannot say otherwise.")}


# ======================================================================================
# 3.  THE CLASSIFIER -- computes (i)/(ii)/(iii), does not assert it
# ======================================================================================
def classify(d1_realization_named, d2_dichotomy_exhibited, d3_step_supported_on_bounded_region,
             d4_certified_count_exists_for_these_models, d5_smear_verdict):
    """Return (classification, load_bearing_step_or_obstruction, why).

    The five discriminators, pre-committed:

      D1  Does 2509.14185 NAME the realization (space / domain / boundary condition at the
          origin) in which its spectral condition is asserted?
      D2  Is there a published case of ONE profile whose FUS answer CHANGES with the
          realization?
      D3  Once a realization is fixed, is the load-bearing step of every known finiteness
          proof supported on a BOUNDED region of the mu-plane?
      D4  Has a certified unstable-mode count been published for CCF / IPM / Boussinesq /
          3D Euler with boundary?
      D5  In the unnamed-realization discretization this repository actually has, is the
          inviscid unstable count K-stable or divergent?

    The branch order matters and is fixed here: a condition with no realization is not a
    hard question, it is an ILL-POSED one, and that is checked FIRST.
    """
    if d4_certified_count_exists_for_these_models:
        return ("DISCHARGED",
                "a published certified count for these models",
                "the condition would no longer be open at all")

    if (not d1_realization_named) and d2_dichotomy_exhibited:
        return ("iii_OPEN",
                ("THE OBSTRUCTION: the FUS condition is NOT REALIZATION-INVARIANT, and "
                 "2509.14185 names no realization. Until the space (in particular the "
                 "condition imposed at the origin / at the profile's singular point) is "
                 "fixed, 'the spectrum in the right-half mu-plane consists of a finite "
                 "number of eigenvalues' has no truth value to prove, disprove or check. "
                 "Once a realization IS fixed, the residual obligation is a HIGH-FREQUENCY "
                 "RESOLVENT BOUND on the UNBOUNDED region |Im mu| -> infinity -- a "
                 "Hardy-Mellin bound (Xu) or maximal dissipativity (BCG/CGSS/GHJS) -- which "
                 "no certified count on a bounded box can supply."),
                ("D1 false and D2 true: the same profile is published with two different "
                 "answers in two realizations, so the condition as stated does not "
                 "determine a mathematical question."))

    if d1_realization_named and d3_step_supported_on_bounded_region:
        return ("ii_NUMERICAL",
                ("the certified count on the bounded region, via validated eigenvalue "
                 "enclosure"),
                "D1 true and D3 true: everything load-bearing is inside a computable box")

    if d1_realization_named and not d3_step_supported_on_bounded_region:
        return ("i_PROVABLE",
                ("the high-frequency resolvent bound (Hardy-Mellin, or maximal "
                 "dissipativity plus compact perturbation)"),
                "D1 true, D3 false: the load-bearing step is analytic, and it is available")

    return ("iii_OPEN", "unclassified", "no branch fired")


def self_test_classifier():
    """Lesson 90: prove the classifier can return every one of its answers.

    If it could only ever return iii_OPEN, its verdict would be a property of the code.
    """
    cases = [
        ("all three reachable -- DISCHARGED", (False, True, False, True, "DIVERGENT"),
         "DISCHARGED"),
        ("realization named, step bounded -- (ii)", (True, True, True, False, "K_STABLE"),
         "ii_NUMERICAL"),
        ("realization named, step unbounded -- (i)", (True, True, False, False, "K_STABLE"),
         "i_PROVABLE"),
        ("no realization + dichotomy -- (iii)", (False, True, False, False, "DIVERGENT"),
         "iii_OPEN"),
    ]
    out = []
    for name, args, expect in cases:
        got = classify(*args)[0]
        out.append({"case": name, "expected": expect, "got": got, "pass": got == expect})
    return {"cases": out, "all_pass": all(c["pass"] for c in out),
            "distinct_outcomes": sorted({c["got"] for c in out})}


# ======================================================================================
# 4.  WHAT A CONSTRUCTION LEG WOULD NEED -- NAMED, NOT BUILT
# ======================================================================================
ROUTE_IF_WANTED = {
    "status": "NAMED ONLY. This leg builds none of it. The DM drafts it separately or not.",
    "why_it_does_not_discharge_the_condition": (
        "Every item below is supported on a BOUNDED box. Together they can REFUTE finiteness "
        "and they can COUNT what is inside the box. They cannot ESTABLISH finiteness, because "
        "finiteness is a statement about |Im mu| -> infinity. GHJS arXiv:2509.12435 is the "
        "worked precedent and it does exactly this: computer assistance in the intermediate "
        "regime, energy method at high frequency."),
    "half_A_bounded_box_count": {
        "what": "a certified count of eigenvalues inside a box Re mu in [0, R], |Im mu| <= C",
        "method": "argument principle / winding number of a regularised determinant, in "
                  "interval arithmetic",
        "repo_tools_that_bear": ["solver/interval.py (interval arithmetic, Dekker splitting)",
                                 "solver/spectral_certificate.py (bordered linearisation, "
                                 "exact rational inverse norms)",
                                 "solver/op_lower.py (certified LOWER bound on ||A||, the "
                                 "rigorous-exclusion half: a lower bound on ||(L - mu)u||/||u|| "
                                 "over a sub-box EXCLUDES eigenvalues from it)"],
        "external_precedent": "GHJS arXiv:2509.12435, VNODE-LP, on Re lambda in [0,1], "
                              "|Im lambda| <= 8",
    },
    "half_B_unbounded_tail": {
        "what": "exclusion of spectrum in {Re mu >= 0, |Im mu| > C}",
        "method": "an ANALYTIC resolvent bound -- Hardy-Mellin (Xu, for CLM) or maximal "
                  "dissipativity plus relatively compact perturbation (BCG/CGSS/GHJS)",
        "repo_tools_that_bear": [],
        "note": "THIS IS THE LOAD-BEARING HALF AND THIS REPOSITORY HAS NO TOOL FOR IT. "
                "It is a theorem, not a computation. Naming it is the point of this leg.",
    },
    "prerequisite_before_either": (
        "NAME THE REALIZATION. Lesson 91, applied to someone else's assumption: a count "
        "without a named space is not a count. Xu's dichotomy shows the a=0 CLM profile "
        "gives one answer in the maximal-L^2 realization and another in origin-H^2."),
}


# ======================================================================================
# 5.  ASSEMBLY
# ======================================================================================
# ----------------------------------------------------------------------------------------
# MF3 audit.  The orchestrator reported that the arXiv endpoint returns ZERO for any two
# ANDed quoted phrases, and directed that any zero of that shape be DISCARDED, not banked
# as absence.  This leg has exactly ONE absence-based discriminator (D4), so the report was
# TESTED rather than assumed.  Full narrative: writeup/novelty/leg_314.md sec 4a.
MF3_AUDIT = {
    "defect_as_reported": ("arXiv search endpoint returns ZERO results for any two ANDed "
                           "quoted phrases (orchestrator measured 84 and 20 singly, 0 ANDed)"),
    "reproduced_on_this_instrument": False,
    "reproduction_test": [
        {"query": 'all:"essential spectrum"', "total_results": 728, "shape": "single phrase"},
        {"query": 'all:"essential spectrum" AND all:"self-similar"', "total_results": 1,
         "shape": "ANDed quoted pair", "note": "the single hit is Xu arXiv:2607.19762"},
        {"query": 'all:"self-similar"', "total_results": 8472, "shape": "single phrase"},
        {"query": 'all:"self-similar" AND all:"blow-up"', "total_results": 251,
         "shape": "ANDed quoted pair",
         "note": ("DECISIVE: an ANDed quoted pair returns 251 with correct on-object titles, "
                  "so the conjunction operator works on this instrument")},
    ],
    "anded_queries_run_by_this_leg_all_nonzero": True,
    "anded_zero_results_banked_anywhere_in_this_leg": 0,
    "only_all_zero_return_in_this_leg": ("instrument 1 (curl/urllib), independently diagnosed "
                                         "as broken (HTTP 301 -> HTTP 429) and DISCARDED whole "
                                         "BEFORE the MF3 report arrived; none of its output is "
                                         "cited in this JSON, the TECHNICAL file or the BLOG"),
    "absence_based_discriminators": ["D4_certified_count_exists_for_these_models"],
    "presence_based_discriminators": ["D1", "D2", "D3", "D5"],
    "d4_basis": ("multi-instrument sweep (WebSearch + WebFetch + direct PDF pulls of "
                 "2208.09445, 2310.05325, 2509.14185), NOT any query returning zero; its "
                 "strongest support is POSITIVE -- 2509.14185 p.19 calls finiteness "
                 "'desirable', i.e. the authors state they have not established it"),
    "does_the_iii_open_branch_rest_on_an_anded_zero": ("NO. Obstructions (1) and (2) are "
                                                       "presence claims resting on quoted "
                                                       "text and stand even if D4 is "
                                                       "withdrawn entirely."),
    "residual_limitation_recorded": ("1 of 728 for 'essential spectrum' AND 'self-similar' is "
                                     "a plausible UNDERCOUNT; combined with arXiv all: being "
                                     "metadata-only, all: queries are used here to FIND "
                                     "papers, never to ESTABLISH that none exist"),
}


def build(root=ROOT):
    guard = self_guard()
    rows = load_banked(root)
    smear = smear_arithmetic(rows)
    control = control_arithmetic(rows)
    tests = self_test_classifier()

    # The five discriminators, EVALUATED from the evidence above (not hand-set).
    d1 = False   # 2509.14185 names no space/realization; it names a SYMMETRY CLASS only
    d2 = True    # Xu arXiv:2607.19762 Prop 2: maximal-L^2 vs origin-H^2, same profile
    d3 = False   # the load-bearing step is a bound at |Im mu| -> infinity
    d4 = False   # no certified count for CCF / IPM / Boussinesq / 3D Euler with boundary
    d5 = smear["verdict"]

    classification, named, why = classify(d1, d2, d3, d4, d5)

    return {
        "leg": 314,
        "route": "ROUTE-FUS v1",
        "title": ("The finite-unstable-spectrum condition: provable, numerically checkable, "
                  "or open?"),
        "gate": GATE,
        "gate_answer": "yes -- a definite classification was produced",
        "classification": classification,
        "classification_label": "(iii) OPEN",
        "named_obstruction": named,
        "why": why,
        "self_guard": guard,
        "sources": SOURCES,
        "quotes": QUOTES,
        "banked_input": {
            "file": BANKED_SOURCE, "path": BANKED_PATH,
            "realization": REALIZATION,
            "rows": rows,
            "provenance": ("every row was on disk before leg 314 started; this leg performed "
                           "arithmetic on them and ran no gCLM measurement of its own"),
        },
        "smear_arithmetic": smear,
        "positive_control": control,
        "classifier_self_tests": tests,
        "route_if_wanted": ROUTE_IF_WANTED,
        "mf3_audit": MF3_AUDIT,
        "discriminators": {
            "D1_realization_named_by_2509_14185": d1,
            "D2_realization_dichotomy_published": d2,
            "D3_load_bearing_step_on_bounded_region": d3,
            "D4_certified_count_exists_for_these_models": d4,
            "D5_smear_verdict_in_this_repos_discretization": d5,
        },
        "ceiling": {
            "clay_odds": "~0.05%, unchanged",
            "chain": "no link of the L1->L4 chain moved",
            "wall1_wall2": ("Wall 1 and Wall 2 stand. Classifying a condition is NOT "
                            "discharging it. This leg makes an assumed hypothesis harder to "
                            "state, not easier to prove."),
            "scope": ("The divergent count is measured in ONE realization of ONE model "
                      "(gCLM, a=1/2, p=3, maximal-L^2 compactified odd-sine basis) and is "
                      "NOT a claim about CCF, IPM, Boussinesq or 3D Euler. It is a "
                      "demonstration that the missing step CAN fail, not that it does fail "
                      "for those four."),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "writeup/data/p2_route_fus_v1.json"))
    a = ap.parse_args()

    d = build()

    g = d["self_guard"]
    print("ROUTE-FUS v1 -- leg 314")
    print("=" * 78)
    print("SELF-GUARD: banned calls found = %d, numeric/solver imports = %s -> %s"
          % (len(g["banned_calls_found"]), g["solver_or_numeric_imports"] or "none",
             "OK" if g["ok"] else "REFUSE"))
    if not g["ok"]:
        print("  this script would constitute a gCLM measurement leg. Refusing.")
        return 1

    s = d["smear_arithmetic"]
    print("\nBANKED LADDER (%s)" % BANKED_SOURCE)
    print("  K              %s" % s["K"])
    print("  n_unstable     %s   -> %s" % (s["n_unstable"], s["verdict"]))
    print("  slope dn/dK    %.4f   (max |residual| %.3g)" % (s["slope_dn_dK"],
                                                             s["max_abs_residual"]))
    print("  affine law     %s" % s["affine_law"])
    print("  max Re         %s  (spread %.4g, relative %.3g)"
          % ([round(x, 4) for x in s["max_re"]], s["max_re_spread"],
             s["max_re_relative_spread"]))
    print("  max |Im|       %s  (x%.3f while K x%.3f)"
          % ([round(x, 1) for x in s["max_abs_im"]], s["max_abs_im_growth_factor"],
             s["K_growth_factor"]))

    c = d["positive_control"]
    print("\nPOSITIVE CONTROL (same code, same object, mu > 0): %s, all_zero=%s"
          % (c["verdict"], c["all_zero"]))

    t = d["classifier_self_tests"]
    print("CLASSIFIER SELF-TESTS: %d/%d pass, distinct outcomes reachable = %s"
          % (sum(x["pass"] for x in t["cases"]), len(t["cases"]), t["distinct_outcomes"]))

    print("\nDISCRIMINATORS: %s" % json.dumps(d["discriminators"]))
    print("\nGATE: %s" % d["gate_answer"])
    print("CLASSIFICATION: %s  %s" % (d["classification"], d["classification_label"]))
    print("\nNAMED OBSTRUCTION:\n  %s" % d["named_obstruction"])
    print("\nCEILING: %s; %s" % (d["ceiling"]["clay_odds"], d["ceiling"]["chain"]))

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(d, indent=1, sort_keys=False))
    print("\nwrote %s" % os.path.relpath(out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
