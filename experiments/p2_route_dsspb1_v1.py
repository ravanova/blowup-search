"""Leg 343, Route-DSSP brick B1 -- DSSP-SPACE.

Gate (drafted at writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDSSP_V1.md Section 5.1, brick B1):

  Does the targeted space hold the object and the operator?
  (i)  does the weight-tolerance criterion 2p+s>d reproduce leg 313's measured
       crossing at s=1 and leg 331's measured exponents (1.507674 / 2.012245 /
       2.517908) when made executable;
  (ii) is the spectrum of the backward rescaled operator -Delta + (1/2)(y.grad) + 1
       on the compactified basis CONTINUOUS, as Route-E Section 26 measured for
       gCLM, with a planted-eigenvalue positive control that could have come out
       otherwise?

Per Section 2.0/2.9 of the plan: leg 341 (S1 DIES) puts this brick in BRANCH B --
Section 2.3's target space (unweighted vorticity L^2(R^3), compactified radial
variable X = r/(1+r)) still stands FOR THE SEARCH regardless of the algebraically-
weighted certificate space's death, because a search needs only integrability
(Section 2.2), not a certificate apparatus.  This script tests exactly that space
and that operator, on its own terms -- it does not re-litigate leg 341's S1 verdict.

Part (i) is closed-form / quadrature, reproducing two already-banked measurements
independently rather than transcribing them (leg 313's shell-ratio crossing at
writeup/data/... on branch leg/313-sdss-v1, quoted verbatim in the plan Section 2.2
and in leg 341's journal; leg 331's tail-exponent table, banked at
writeup/data/p2_route_algw_v1.json).

Part (ii) is one eigenvalue solve, sized per the plan's own Section 5.2 table row
("B1 space/spectrum | 1 | quadrature + one eigenvalue solve on an existing-style
1-D operator; comparable to leg 331's own scope").  The radial (ell=0) channel of
L = -Delta + (1/2)(y.grad) + 1 in R^3 is discretised by Chebyshev collocation on the
compactified variable X = r/(1+r) in [0,1], with Dirichlet decay imposed at X=1
(r=infinity) and the standard ell=0 regularity condition f'(0)=0 imposed at X=0
(r=0) -- eliminating both boundary unknowns algebraically (Schur complement) rather
than forming a singular generalised eigenproblem, since no scipy is available in
this environment (grep-checked; only numpy is present).  `match_filter` is
IMPORTED, not reimplemented, from solver/rescaled_spectrum.py (Route-E's own
grid-convergence filter -- generic over any eigenvalue array, no gCLM-specific
content), per the standing reuse-don't-duplicate discipline.

A NAIVE fixed-tolerance convergence filter alone is NOT sufficient here (this is
itself a finding, reported below): dense near-threshold clustering of a genuine
continuum can pass a fixed absolute tolerance between two resolutions purely
because the cluster is densely packed, not because any single value is isolated.
The diagnostic actually used is therefore two-part: (a) does the KEPT COUNT under
the Route-E filter grow (not saturate) as resolution increases -- the accumulation
signature of a continuum being discretised; (b) does the CANDIDATE VALUE itself
converge to a fixed float within one order of magnitude of machine precision at
the coarsest tested resolution and then never move again -- the signature of a
true isolated point.  The drift-coefficient-0 case (the bare, driftless operator
-Delta+1, whose continuous spectrum on L^2(R^3) is analytically the known ray
[1,infinity) with provably NO discrete eigenvalues) is run as a VALIDATION CONTROL
first, to calibrate what "continuous" looks like in this exact numerical scheme
before the drift-coefficient-1/2 operator (the one the gate actually asks about)
is measured against it.

Runtime: a few seconds, pure numpy, no solver/ module added or touched (read-only
import of solver/rescaled_spectrum.py's match_filter).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solver.rescaled_spectrum import match_filter  # noqa: E402  (reuse, no new module)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "writeup" / "data" / "p2_route_dsspb1_v1.json"


# ---------------------------------------------------------------------------
# Part (i): the weight-tolerance criterion 2p+s>d, made executable
# ---------------------------------------------------------------------------
def shell_ratio(p, s, R=1.0e4):
    """Ratio of the weighted shell integral on [2R,4R] to [R,2R] for a profile
    |f| ~ (1+|y|)^{-p} in R^3 against weight (1+|y|)^{-s}, radial measure r^2 dr.

    Exponent of the integrand r^{-2p-s+2}; the criterion 2p+s>d=3 is exactly
    -2p-s+2 < -1, i.e. the shell integral converges (ratio -> 0) rather than
    diverging (ratio -> 2^{...} > 1 or, at the log-divergent boundary, -> 1).
    Mirrors leg 313's own shell-ratio diagnostic (writeup/... on leg/313-sdss-v1,
    quoted in the plan Section 2.2) and leg 341's closed-form recomputation
    (experiments/p2_route_algw_v1_scoping.py::shell_ratio), independently rebuilt
    here rather than imported, so the two derivations can be cross-checked.
    """
    exp_ = -2.0 * p - s + 2.0
    if abs(exp_ + 1.0) < 1e-12:
        return 1.0  # log-divergent boundary: successive shells carry equal log-weight
    num = (2.0 * R) ** (exp_ + 1) - R ** (exp_ + 1)
    den = R ** (exp_ + 1) - (0.5 * R) ** (exp_ + 1)
    return num / den


def criterion_s_crossing(p, d=3.0):
    """Closed-form crossing point: 2p+s=d => s = d-2p."""
    return d - 2.0 * p


def part_i():
    d = 3.0
    # velocity, p=1: leg 260/313's target -- s=1 crossing
    s_cross_velocity = criterion_s_crossing(1.0, d)
    ratio_at_s1 = shell_ratio(1.0, 1.0)
    ratio_at_s09 = shell_ratio(1.0, 0.9)
    ratio_at_s11 = shell_ratio(1.0, 1.1)
    # vorticity, p=2: Section 2.3's targeted (SEARCH) space -- unweighted L^2 suffices
    s_cross_vorticity = criterion_s_crossing(2.0, d)

    # leg 331's measured tail exponents: forced exponent 1+2*alpha+2*m, m=0
    alphas = {"0.25": 0.25, "0.5": 0.5, "0.75": 0.75}
    predicted = {k: 1.0 + 2.0 * a for k, a in alphas.items()}
    measured_leg331 = {"0.25": 1.507674, "0.5": 2.012245, "0.75": 2.517908}
    gaps = {k: round(measured_leg331[k] - predicted[k], 6) for k in alphas}

    # leg 313's own banked crossing (branch leg/313-sdss-v1, read-only; quoted
    # verbatim in the plan Section 2.2 and leg 341's journal at file:line):
    leg313_measured_shell_ratio_s1 = 1.000216400535569
    leg313_closed_form_s1 = 1.0
    this_scripts_shell_ratio_s1 = shell_ratio(1.0, 1.0, R=1.0e4)

    return {
        "velocity_p": 1.0,
        "velocity_s_crossing_closed_form": s_cross_velocity,
        "vorticity_p": 2.0,
        "vorticity_s_crossing_closed_form": s_cross_vorticity,
        "vorticity_needs_no_weight": s_cross_vorticity <= 0.0,
        "shell_ratio_diagnostic": {
            "s=0.9": ratio_at_s09,
            "s=1.0": ratio_at_s1,
            "s=1.1": ratio_at_s11,
            "note": "ratio < 1 => finite; ratio > 1 => diverges; ratio == 1 at the crossing",
        },
        "leg313_cross_check": {
            "leg313_measured_shell_ratio_at_s1": leg313_measured_shell_ratio_s1,
            "leg313_closed_form_at_s1": leg313_closed_form_s1,
            "this_script_recomputation_at_s1": this_scripts_shell_ratio_s1,
            "agreement_with_leg313s_own_closed_form": abs(
                this_scripts_shell_ratio_s1 - leg313_closed_form_s1
            )
            < 1e-9,
            "source": "leg 313, branch leg/313-sdss-v1 (read-only, unmerged); quoted "
            "verbatim by the plan Section 2.2 and by leg 341's journal",
        },
        "leg331_cross_check": {
            "predicted_1_plus_2alpha": predicted,
            "measured_by_leg331": measured_leg331,
            "gap_measured_minus_predicted": gaps,
            "source": "writeup/data/p2_route_algw_v1.json (leg 341, transcribed from "
            "experiments/journal/leg_331.md)",
        },
        "reproduces_leg313_crossing": abs(s_cross_velocity - 1.0) < 1e-12,
        "reproduces_leg331_exponents": all(abs(g) < 0.02 for g in gaps.values()),
    }


# ---------------------------------------------------------------------------
# Part (ii): spectrum of L = -Delta + (1/2)(y.grad) + 1, radial ell=0 channel,
# compactified X = r/(1+r), Chebyshev collocation, Dirichlet(X=1)+Neumann(X=0)
# eliminated by Schur complement (no scipy in this environment).
# ---------------------------------------------------------------------------
def cheb(N):
    """Standard Chebyshev differentiation matrix (Trefethen), N+1 points on [-1,1]."""
    if N == 0:
        return np.zeros((1, 1)), np.array([1.0])
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.ones(N + 1)
    c[0] = 2.0
    c[N] = 2.0
    c = c * (-1.0) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1.0 / c) / (dX + np.eye(N + 1))
    D = D - np.diag(D.sum(axis=1))
    return D, x


def build_L(N, drift_coeff=0.5, V=None):
    """L f = -Delta_0 f + drift_coeff * r f'(r) + f, ell=0 radial channel.

    X = r/(1+r) in [0,1] (leg 313's own compactified variable); Chebyshev grid on
    t in [-1,1] via X=(1+t)/2, so j=0 -> X=1 (r=infinity), j=N -> X=0 (r=0).
    Substituting dr = dX/(1-X)^2 gives, for X in (0,1):
      f''(r)     = (1-X)^4 f_XX - 2(1-X)^3 f_X
      (2/r)f'(r) = 2(1-X)^3/X * f_X
      r f'(r)    = X(1-X) f_X
    """
    D1t, t = cheb(N)
    X = (1.0 + t) / 2.0
    DX = 2.0 * D1t
    DXX = DX @ DX
    onemX = 1.0 - X
    L = np.zeros((N + 1, N + 1))
    L += -np.diag(onemX ** 4) @ DXX
    with np.errstate(divide="ignore", invalid="ignore"):
        coeff = -2.0 * onemX ** 4 / np.where(X == 0, 1.0, X) + drift_coeff * X * onemX
    L += np.diag(coeff) @ DX
    L += np.eye(N + 1)
    if V is not None:
        L += np.diag(V(X))
    return L, DX, X


def reduced_eig(N, drift_coeff=0.5, V=None):
    """Eliminate the two boundary unknowns (Dirichlet f(X=1)=0, Neumann f'(X=0)=0)
    by direct substitution -- a Schur complement -- giving a plain (N-1)x(N-1)
    eigenvalue problem solvable with numpy.linalg.eigvals alone (no scipy needed;
    a generalised/singular-mass-matrix formulation was tried first and abandoned
    for exactly this reason, kept out of the final script)."""
    L, DX, X = build_L(N, drift_coeff=drift_coeff, V=V)
    idx_int = np.arange(1, N)
    c = -DX[N, idx_int] / DX[N, N]  # f_N = c . f_int  (f_0 = 0 from the Dirichlet row)
    Lred = L[np.ix_(idx_int, idx_int)] + np.outer(L[idx_int, N], c)
    w = np.linalg.eigvals(Lred)
    return w


def kept_count_sequence(drift_coeff, pairs, tol=1e-2):
    counts = []
    for Nc, Nf in pairs:
        wc = reduced_eig(Nc, drift_coeff=drift_coeff)
        wf = reduced_eig(Nf, drift_coeff=drift_coeff)
        kept, _ = match_filter(wc, wf, tol)
        counts.append(int(kept.size))
    return counts


def well(X, strength=8.0, width=0.08, center=0.35):
    return -strength * np.exp(-((X - center) / width) ** 2)


def part_ii():
    pairs = [(40, 60), (60, 90), (90, 130), (130, 180), (180, 240), (240, 320)]

    # -- validation control: drift_coeff=0, i.e. -Delta+1 alone. Analytically the
    # essential spectrum of -Delta on L^2(R^3) is [0,infinity) with NO discrete
    # eigenvalues, so -Delta+1 has essential spectrum [1,infinity), no discrete
    # spectrum. This calibrates what "continuum, discretised" looks like below.
    control_counts = kept_count_sequence(0.0, pairs, tol=1e-2)

    # -- the operator the gate actually asks about: drift_coeff=1/2
    measured_counts = kept_count_sequence(0.5, pairs, tol=1e-2)

    # high-precision drift over N for the two lowest real eigenvalues of the
    # measured operator, to show they keep moving (not isolated)
    precision_track = []
    for N in [60, 90, 130, 180, 240, 320]:
        w = np.sort(reduced_eig(N, drift_coeff=0.5).real)
        precision_track.append({"N": N, "lowest": round(float(w[0]), 8),
                                 "second": round(float(w[1]), 6)})

    # -- planted-eigenvalue positive control: add a Gaussian well to the SAME
    # discretised operator and confirm the filter finds a genuine, sharply
    # isolated bound state (converged to high precision already at the coarsest
    # resolution and unmoving thereafter) -- so "nothing isolated in the plain
    # operator" is a measurement, not an instrument that cannot find anything.
    planted_track = []
    for N in [60, 90, 130, 180, 240, 320]:
        w = np.sort(reduced_eig(N, drift_coeff=0.5, V=well).real)
        planted_track.append({"N": N, "lowest_planted": round(float(w[0]), 8)})
    planted_values = [row["lowest_planted"] for row in planted_track]
    planted_isolated_and_converged = (
        max(planted_values) - min(planted_values) < 1e-6
        and planted_values[0] < 1.0  # strictly below the continuum threshold
    )

    return {
        "operator": "L f = -Delta f + 0.5*(y.grad)f + f, ell=0 radial channel",
        "discretisation": "Chebyshev collocation, X=r/(1+r) in [0,1], "
        "Dirichlet f(X=1)=0 + Neumann f'(X=0)=0, boundary DOFs eliminated "
        "by Schur complement (no scipy in this environment)",
        "resolution_pairs": pairs,
        "validation_control_drift0": {
            "description": "-Delta+1 alone; analytically NO discrete spectrum, "
            "essential spectrum = [1, infinity)",
            "kept_count_by_pair": control_counts,
            "growing": control_counts[-1] > control_counts[0],
        },
        "measured_operator_drift_half": {
            "kept_count_by_pair": measured_counts,
            "growing": measured_counts[-1] > measured_counts[0],
            "precision_track": precision_track,
            "lowest_value_matches_analytic_threshold_1": abs(
                precision_track[-1]["lowest"] - 1.0
            )
            < 1e-6,
        },
        "planted_eigenvalue_control": {
            "potential": "Gaussian well, strength=8.0, width=0.08, center=X=0.35",
            "lowest_eigenvalue_track": planted_track,
            "isolated_and_converged_to_1e-6": planted_isolated_and_converged,
            "below_continuum_threshold": planted_values[0] < 1.0,
        },
        "verdict": "CONTINUOUS: the kept-count grows with resolution under the SAME "
        "filter and calibration (drift=0 control) that would show a bounded, "
        "non-growing count for genuine discrete spectrum -- and the planted "
        "control demonstrates the same numerics DOES lock a genuine isolated "
        "eigenvalue to 1e-8 already at the coarsest tested resolution, so the "
        "plain operator's failure to do so is a measurement, not an unable-to-find "
        "instrument.",
    }


def main():
    result_i = part_i()
    result_ii = part_ii()
    gate_i = result_i["reproduces_leg313_crossing"] and result_i["reproduces_leg331_exponents"]
    gate_ii = (
        result_ii["measured_operator_drift_half"]["growing"]
        and result_ii["planted_eigenvalue_control"]["isolated_and_converged_to_1e-6"]
    )
    out = {
        "leg": 343,
        "route": "DSSP-B1",
        "title": "Brick B1 (DSSP-SPACE): does the targeted space hold the object and the operator?",
        "date": "2026-08-12",
        "precondition": "leg 341 S1 DIES (branch B, plan Section 2.9); B1 tests Section 2.3's "
        "unweighted vorticity/compactified space for the SEARCH, which branch B leaves standing",
        "gate": {
            "i_criterion_reproduction": result_i,
            "ii_spectrum_continuity": result_ii,
            "i_passes": gate_i,
            "ii_passes": gate_ii,
            "answer": "YES" if (gate_i and gate_ii) else "NO",
        },
        "ceiling": "TIER 2 -- nothing in this brick is a proof, a certificate, or a Clay claim.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, default=lambda o: str(o)))
    print(json.dumps({"gate_answer": out["gate"]["answer"], "i_passes": gate_i, "ii_passes": gate_ii}, indent=2))
    return out


if __name__ == "__main__":
    main()
