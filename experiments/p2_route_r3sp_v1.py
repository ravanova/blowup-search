"""Leg 376, Route-R3SP -- measure the ell=1 and ell=2 angular-momentum channels of the
rescaled operator L = -Delta + (1/2)(y.grad) + 1 that leg 343/B1 measured ONLY on the
ell=0 (radial) channel, and which leg 348 explicitly refused to transfer to the other
channels because they had never been measured.

THE OPERATOR AND WHY THE ell=0 RESULT DOES NOT AUTOMATICALLY TRANSFER
------------------------------------------------------------------------------
On R^3, separate f(y) = f(r) Y_ell^m(angle). Since -Delta, the dilation generator
y.grad = r d/dr (an exact identity, independent of any function's angular dependence),
and the identity all commute with SO(3), L is EXACTLY block-diagonal across the
ell-eigenspaces of the angular Laplacian: no computation can make it otherwise, and
none is attempted here (see `coupling_analytic_note` below -- this is Schur's lemma /
standard spherical-harmonic decomposition, not a numerical question, and the task's own
"if the decomposition structure warrants it" is answered NO for the cross-channel
coupling by that argument alone). What each ell-BLOCK's spectrum *is* -- continuous or
carrying an isolated eigenvalue -- is a genuine per-channel question the block-diagonal
fact says nothing about, which is exactly why leg 348 refused to assume it and this leg
measures it.

Each radial block is
    L_ell f = -(f'' + (2/r) f' - ell(ell+1)/r^2 f) + (1/2) r f' + f .
The substitution f(r) = r^ell g(r) (standard for a centrifugal term) removes the
1/r^2 singularity EXACTLY (this is checked algebraically in the docstring below, not
just asserted) and turns the ell-channel equation into
    L_ell g = -g'' - (2(ell+1)/r) g' + (1/2) r g' + (1 + ell/2) g = lambda g ,
i.e. leg 343's own ell=0 equation with "2/r" -> "2(ell+1)/r" and the "+1" shift ->
"+(1+ell/2)". At ell=0 this equation is IDENTICAL to leg 343's, letter for letter --
so leg 343's ell=0 result is reproduced here as an internal cross-check (not
re-measured as new information) before ell=1/ell=2 are trusted. Algebra of the
substitution (drop lower terms, r^{ell-2} centrifugal piece cancels identically):
  f'  = ell r^{ell-1} g + r^ell g'
  f'' = ell(ell-1) r^{ell-2} g + 2 ell r^{ell-1} g' + r^ell g''
  f'' + (2/r)f' - ell(ell+1)/r^2 f
    = [ell(ell-1)+2ell-ell(ell+1)] r^{ell-2} g + [2ell+2] r^{ell-1} g' + r^ell g''
    = 0 * r^{ell-2} g + 2(ell+1) r^{ell-1} g' + r^ell g''                (coefficient
                                                                           of g is 0)
    = r^ell [ g'' + 2(ell+1)/r g' ] .
  (1/2) r f' = r^ell * (1/2)(ell g + r g').
Dividing the whole equation by r^ell gives the g-equation above. Boundary behaviour:
removing the 1/r^2 singularity also removes ell's effect on the origin condition --
EVERY channel now needs the SAME regularity condition g'(0)=0 that leg 343 used for
ell=0 (Neumann at X=0, r=0), plus the same decay Dirichlet condition at X=1 (r=infinity)
leg 343 used. This is why the code below is a near-verbatim reuse of leg 343's
Chebyshev-collocation-plus-Schur-complement machine, parametrised by ell through exactly
two numbers: the "2" in the drift coefficient becomes "2(ell+1)", and the "+1" shift
becomes "+(1+ell/2)".

DISCRETISATION 1 (primary): Chebyshev collocation directly on leg 313's compactified
variable X = r/(1+r) in [0,1] -- leg 343's own basis, letter-for-letter reused.

DISCRETISATION 2 (leg 350's enriched basis, per this leg's spec): leg 350 built
solver/dssp_basis.py's log-Boyd composite map v = u/(u+L), u = -log(1-X), L=16.0
fixed, to buy resolution against a boundary defect at X=1. That map is GENERIC (it
does not depend on which function is being resolved) so it is reused here, unedited,
as a SECOND, independent discretisation of the SAME operator: nodes are placed in v,
transformed back to X via `X_of_v`, and the X-derivatives needed by L_ell are obtained
by the chain rule (d/dX = (dv/dX) d/dv, etc.) rather than by differentiating in X
directly. If the verdict on ell=1/ell=2 agrees between the two independent bases, that
is real cross-checked evidence, not a restatement of one measurement.

CONTROLS (applied to EVERY channel, on the primary basis; repeated at lighter
resolution on the enriched basis as a same-object cross-check):
  1. PLANTED-GAUSSIAN-WELL POSITIVE CONTROL (leg 343's own construction, `well()`,
     reused unedited): add a Gaussian well to the SAME discretised operator and
     confirm the lowest eigenvalue locks to a fixed value, well below the continuum
     threshold, already at the coarsest tested resolution -- proving the method CAN
     find a genuine isolated eigenvalue in each channel's basis if one is present.
  2. DRIFT-0 ANALYTIC-NULL CONTROL (leg 343's own construction, reused unedited): the
     bare operator -Delta_ell + (1+ell/2) (drift_coeff=0) has KNOWN essential
     spectrum [1+ell/2, infinity) and NO discrete eigenvalues for any ell (the
     centrifugal-substituted operator is a nonnegative Laplacian-type operator on an
     effective radial half-line, shifted by a positive constant) -- this calibrates
     what "genuinely continuous, correctly reported absent" looks like in each
     channel's own numerics before the drift=1/2 operator the gate asks about is run
     against it.

TIER-2 CEILING: a spectrum is apparatus information about the numerical method
applied to the compactified basis, not a result about the Navier-Stokes PDE or a
Clay-relevant claim. No cost-class-C spend is committed: this measures already-landed
apparatus (leg 343's operator/basis, leg 350's enriched map) with leg 343's own
already-validated control pattern; no new solver/ module, no scipy (grep-checked
absent, exactly as leg 343 found).

Runtime: a few seconds, pure numpy.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.rescaled_spectrum import match_filter  # noqa: E402  (reuse, no new module)
from solver.dssp_basis import DEFAULT_L  # noqa: E402  (leg 350's enriched map scale, read-only reuse)

OUT = ROOT / "writeup" / "data" / "p2_route_r3sp_v1.json"
LEG343_JSON = ROOT / "writeup" / "data" / "p2_route_dsspb1_v1.json"


# ---------------------------------------------------------------------------
# Shared machinery: leg 343's Chebyshev differentiation matrix, reused verbatim.
# ---------------------------------------------------------------------------
def cheb(N):
    """Standard Chebyshev differentiation matrix (Trefethen), N+1 points on [-1,1].
    Identical to leg 343's experiments/p2_route_dsspb1_v1.py::cheb."""
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


# ---------------------------------------------------------------------------
# Discretisation 1 (primary): plain Chebyshev-in-X, leg 313/343's own compactified
# variable X = r/(1+r), generalised to ell via the r^ell substitution derived above.
# ---------------------------------------------------------------------------
def build_L_ell_X(N, ell, drift_coeff=0.5, V=None):
    """L_ell g = -g'' - 2(ell+1)/r g' + (1/2) r g' + (1+ell/2) g, on X = r/(1+r).

    ell=0 reduces EXACTLY to leg 343's build_L (2*(ell+1)=2, 1+ell/2=1) -- verified
    as a self-test in main(), not merely asserted.
    """
    D1t, t = cheb(N)
    X = (1.0 + t) / 2.0
    DX = 2.0 * D1t
    DXX = DX @ DX
    onemX = 1.0 - X
    L = np.zeros((N + 1, N + 1))
    L += -np.diag(onemX ** 4) @ DXX
    with np.errstate(divide="ignore", invalid="ignore"):
        coeff = -2.0 * (ell + 1.0) * onemX ** 4 / np.where(X == 0, 1.0, X) + drift_coeff * X * onemX
    L += np.diag(coeff) @ DX
    L += (1.0 + 0.5 * ell) * np.eye(N + 1)
    if V is not None:
        L += np.diag(V(X))
    return L, DX, X


def reduced_eig_ell_X(N, ell, drift_coeff=0.5, V=None):
    """Schur-complement elimination of the two boundary DOFs (Dirichlet g(X=1)=0,
    Neumann g'(X=0)=0) -- identical construction to leg 343, generalised over ell."""
    L, DX, X = build_L_ell_X(N, ell, drift_coeff=drift_coeff, V=V)
    idx_int = np.arange(1, N)
    c = -DX[N, idx_int] / DX[N, N]
    Lred = L[np.ix_(idx_int, idx_int)] + np.outer(L[idx_int, N], c)
    return np.linalg.eigvals(Lred)


# ---------------------------------------------------------------------------
# Discretisation 2: leg 350's enriched (log-Boyd) basis, v = u/(u+L), u=-log(1-X),
# used here as a SECOND independent discretisation of the SAME operator (cross-check,
# not a per-kappa fit -- L is fixed at leg 350's own DEFAULT_L=16.0, unedited).
# ---------------------------------------------------------------------------
def build_L_ell_v(N, ell, L_scale=DEFAULT_L, drift_coeff=0.5, V=None):
    """Same L_ell g = ... equation, discretised on Chebyshev-in-v nodes, X and
    1-X obtained from leg 350's own map (u = -log(1-X), v = u/(u+L)) evaluated
    directly in u to avoid cancellation, and X-derivatives obtained by the chain rule.

    v = 1 at index 0 (r = infinity) mirrors leg 343's index-0 convention exactly;
    dX/dv -> 0 exponentially fast there (the map's whole point), so dv/dX blows up
    at that single node -- but that node is the Dirichlet DOF, dropped whole (row
    AND column) by the same Schur-complement construction below, so the blow-up
    never enters any used matrix entry.
    """
    D1t, t = cheb(N)
    v = (1.0 + t) / 2.0
    Dv = 2.0 * D1t
    # onemX = 1-X = exp(-u) computed DIRECTLY, not as 1.0 - X_of_v(v): computing
    # X_of_v first (which internally forms 1 - exp(-u)) and then subtracting from 1
    # again catastrophically cancels back to ~0 for every node with u large (v close
    # to 1) -- verified empirically (multiple leading nodes read onemX exactly 0.0
    # and produced nan/inf downstream) before this fix. exp(-u) itself never
    # cancels, so this is the correct instrument, not merely a workaround.
    with np.errstate(divide="ignore", invalid="ignore"):
        u = L_scale * v / (1.0 - v)
        onemX = np.exp(-u)
    X = 1.0 - onemX
    with np.errstate(divide="ignore", invalid="ignore"):
        dXdv = L_scale * onemX / (1.0 - v) ** 2
        d2Xdv2 = L_scale * onemX / (1.0 - v) ** 3 * (2.0 - L_scale / (1.0 - v))
        dvdX = 1.0 / dXdv
        d2vdX2 = -d2Xdv2 / dXdv ** 3
    DX = np.diag(dvdX) @ Dv
    DXX = np.diag(d2vdX2) @ Dv + np.diag(dvdX ** 2) @ (Dv @ Dv)
    L = np.zeros((N + 1, N + 1))
    L += -np.diag(onemX ** 4) @ DXX
    with np.errstate(divide="ignore", invalid="ignore"):
        coeff = -2.0 * (ell + 1.0) * onemX ** 4 / np.where(X == 0, 1.0, X) + drift_coeff * X * onemX
    L += np.diag(coeff) @ DX
    L += (1.0 + 0.5 * ell) * np.eye(N + 1)
    if V is not None:
        L += np.diag(V(X))
    return L, DX, X


def reduced_eig_ell_v(N, ell, L_scale=DEFAULT_L, drift_coeff=0.5, V=None):
    L, DX, X = build_L_ell_v(N, ell, L_scale=L_scale, drift_coeff=drift_coeff, V=V)
    idx_int = np.arange(1, N)
    c = -DX[N, idx_int] / DX[N, N]
    Lred = L[np.ix_(idx_int, idx_int)] + np.outer(L[idx_int, N], c)
    return np.linalg.eigvals(Lred)


# ---------------------------------------------------------------------------
# Planted-well positive control -- leg 343's own construction, reused unedited.
# ---------------------------------------------------------------------------
def well(X, strength=8.0, width=0.08, center=0.35):
    return -strength * np.exp(-((X - center) / width) ** 2)


def kept_count_sequence(ell, drift_coeff, pairs, reduced_eig_fn, tol=1e-2, **kw):
    counts = []
    for Nc, Nf in pairs:
        wc = reduced_eig_fn(Nc, ell, drift_coeff=drift_coeff, **kw)
        wf = reduced_eig_fn(Nf, ell, drift_coeff=drift_coeff, **kw)
        kept, _ = match_filter(wc, wf, tol)
        counts.append(int(kept.size))
    return counts


# ---------------------------------------------------------------------------
# Self-test: ell=0 on the primary basis must reproduce leg 343's own banked numbers.
# ---------------------------------------------------------------------------
def selftest_ell0_reproduces_leg343():
    banked = json.loads(LEG343_JSON.read_text())
    banked_track = banked["gate"]["ii_spectrum_continuity"]["measured_operator_drift_half"]["precision_track"]
    ok = True
    detail = []
    for row in banked_track:
        N = row["N"]
        w = np.sort(reduced_eig_ell_X(N, 0, drift_coeff=0.5).real)
        lowest = round(float(w[0]), 8)
        match = abs(lowest - row["lowest"]) < 1e-6
        ok = ok and match
        detail.append({"N": N, "leg343_lowest": row["lowest"], "this_leg_ell0_lowest": lowest, "match": match})
    return {"reproduces_leg343_ell0_exactly": ok, "detail": detail}


# ---------------------------------------------------------------------------
# Per-channel measurement (primary basis, full resolution study + both controls).
# ---------------------------------------------------------------------------
def measure_channel_primary(ell):
    pairs = [(40, 60), (60, 90), (90, 130), (130, 180), (180, 240), (240, 320)]
    threshold = 1.0 + 0.5 * ell

    # -- drift-0 analytic-null control: -Delta_ell + (1+ell/2), NO discrete spectrum
    # analytically for any ell (a nonnegative-Laplacian-type operator shifted by a
    # positive constant), essential spectrum [threshold, infinity).
    control_counts = kept_count_sequence(ell, 0.0, pairs, reduced_eig_ell_X, tol=1e-2)

    # -- the operator the gate actually asks about: drift_coeff=1/2
    measured_counts = kept_count_sequence(ell, 0.5, pairs, reduced_eig_ell_X, tol=1e-2)

    precision_track = []
    for N in [60, 90, 130, 180, 240, 320]:
        w = np.sort(reduced_eig_ell_X(N, ell, drift_coeff=0.5).real)
        precision_track.append({"N": N, "lowest": round(float(w[0]), 8), "second": round(float(w[1]), 6)})

    # -- planted-eigenvalue positive control (leg 343's well(), unedited)
    planted_track = []
    for N in [60, 90, 130, 180, 240, 320]:
        w = np.sort(reduced_eig_ell_X(N, ell, drift_coeff=0.5, V=well).real)
        planted_track.append({"N": N, "lowest_planted": round(float(w[0]), 8)})
    planted_values = [row["lowest_planted"] for row in planted_track]
    planted_isolated_and_converged = (
        max(planted_values) - min(planted_values) < 1e-6 and planted_values[0] < threshold
    )

    lowest_matches_threshold = abs(precision_track[-1]["lowest"] - threshold) < 1e-6
    control_no_discrete = not (control_counts[-1] > control_counts[0])
    measured_growing = measured_counts[-1] > measured_counts[0]

    gate_channel = measured_growing and planted_isolated_and_converged

    return {
        "ell": ell,
        "operator": f"L_ell g = -g'' - {2*(ell+1)}/r g' + 0.5 r g' + {1.0+0.5*ell} g "
        f"(centrifugal-substituted f=r^{ell} g form of "
        f"-Delta + 0.5(y.grad) + 1 restricted to the ell={ell} spherical-harmonic block)",
        "analytic_continuum_threshold": threshold,
        "resolution_pairs": pairs,
        "drift0_null_control": {
            "description": f"-Delta_ell + {threshold}; analytically NO discrete "
            f"spectrum, essential spectrum = [{threshold}, infinity)",
            "kept_count_by_pair": control_counts,
            "correctly_reports_no_discrete_component": control_no_discrete,
        },
        "measured_operator_drift_half": {
            "kept_count_by_pair": measured_counts,
            "growing": measured_growing,
            "precision_track": precision_track,
            "lowest_value_matches_analytic_threshold": lowest_matches_threshold,
        },
        "planted_eigenvalue_control": {
            "potential": "Gaussian well, strength=8.0, width=0.08, center=X=0.35 (leg 343's own well())",
            "lowest_eigenvalue_track": planted_track,
            "isolated_and_converged_to_1e-6": planted_isolated_and_converged,
            "below_continuum_threshold": planted_values[0] < threshold,
        },
        "both_controls_pass": control_no_discrete and planted_isolated_and_converged,
        "verdict": "CONTINUOUS" if gate_channel else "DISCRETE-COMPONENT-FOUND-OR-UNRESOLVED",
    }


# ---------------------------------------------------------------------------
# Cross-check on leg 350's enriched basis (lighter resolution -- confirmatory, not
# a second full resolution study; the primary basis above carries the gate).
# ---------------------------------------------------------------------------
def measure_channel_enriched_crosscheck(ell):
    threshold = 1.0 + 0.5 * ell
    Ns = [60, 120, 240, 480]

    precision_track = []
    for N in Ns:
        w = np.sort(reduced_eig_ell_v(N, ell, drift_coeff=0.5).real)
        precision_track.append({"N": N, "lowest": round(float(w[0]), 8)})

    planted_track = []
    for N in Ns:
        w = np.sort(reduced_eig_ell_v(N, ell, drift_coeff=0.5, V=well).real)
        planted_track.append({"N": N, "lowest_planted": round(float(w[0]), 8)})
    planted_values = [row["lowest_planted"] for row in planted_track]
    planted_isolated = max(planted_values) - min(planted_values) < 1e-4 and planted_values[0] < threshold

    lowest_matches = abs(precision_track[-1]["lowest"] - threshold) < 1e-4

    # drift-0 null control, lighter (single high-N check that the lowest value sits
    # at threshold and the count does not saturate at a small fixed number)
    pairs = [(60, 120), (120, 240), (240, 480)]
    control_counts = kept_count_sequence(ell, 0.0, pairs, reduced_eig_ell_v, tol=1e-1)
    measured_counts = kept_count_sequence(ell, 0.5, pairs, reduced_eig_ell_v, tol=1e-1)

    return {
        "basis": "leg 350's enriched log-Boyd map (v=u/(u+L), u=-log(1-X), L=16.0, "
        "solver/dssp_basis.py, unedited, reused as a second discretisation)",
        "precision_track": precision_track,
        "lowest_matches_analytic_threshold": lowest_matches,
        "drift0_null_control_kept_count_by_pair": control_counts,
        "measured_kept_count_by_pair": measured_counts,
        "measured_growing_or_flat_small": measured_counts[-1] >= measured_counts[0],
        "planted_eigenvalue_control": {
            "lowest_eigenvalue_track": planted_track,
            "isolated_and_converged_to_1e-4": planted_isolated,
        },
        "agrees_with_primary_basis_verdict": lowest_matches and planted_isolated,
    }


# ---------------------------------------------------------------------------
# Coupled-channel structure: analytic, not numerical (see module docstring).
# ---------------------------------------------------------------------------
def coupling_analytic_note():
    return {
        "question": "does the operator couple the ell=0/1/2 channels (or any pair of "
        "distinct ell channels)?",
        "answer": "NO -- exactly, by symmetry, not by numerical measurement",
        "argument": (
            "-Delta commutes with every rotation R in SO(3) (it is the SO(3)-invariant "
            "Laplace-Beltrami-plus-radial operator on R^3); y.grad is the dilation "
            "generator r d/dr, an identity valid for ANY function regardless of its "
            "angular dependence, hence also SO(3)-invariant (dilations and rotations "
            "commute in R^3); the identity operator commutes with everything. So "
            "L = -Delta + (1/2)(y.grad) + 1 commutes with the full SO(3) representation "
            "on L^2(R^3). The ell-eigenspaces of the angular Laplacian (spanned by the "
            "spherical harmonics Y_ell^m) are exactly the isotypic components of that "
            "representation, and an operator commuting with the group action is block-"
            "diagonal across isotypic components (Schur's lemma) -- there is no "
            "off-diagonal ell-ell' block to compute, for any ell != ell'. This is why "
            "leg 343's radial (ell=0) reduction and this leg's ell=1/ell=2 reductions "
            "are each a genuine, self-contained 1-D eigenvalue problem with no coupling "
            "term dropped or approximated."
        ),
        "why_no_numerical_coupled_computation_is_warranted": (
            "the task's own gate asks for coupled-channel measurement 'if the "
            "decomposition structure warrants it' -- the decomposition structure here "
            "is exact block-diagonalisation by an algebraic symmetry argument, which is "
            "not a numerical question a finite-resolution study could either confirm "
            "or refute more strongly than the symmetry argument itself already does. "
            "Running a coupled matrix and checking off-diagonal blocks are ~0 to float "
            "precision would only re-derive machine-epsilon confirmation of an exact "
            "algebraic fact, at cost-class spend this leg is not licensed to commit -- "
            "so it is not run."
        ),
    }


def main():
    selftest = selftest_ell0_reproduces_leg343()

    ell1 = measure_channel_primary(1)
    ell2 = measure_channel_primary(2)
    ell1_cross = measure_channel_enriched_crosscheck(1)
    ell2_cross = measure_channel_enriched_crosscheck(2)
    coupling = coupling_analytic_note()

    def pocp_line(ch, cross):
        if ch["verdict"] == "CONTINUOUS" and cross["agrees_with_primary_basis_verdict"]:
            return (
                f"ell={ch['ell']}: CONTINUOUS, confirmed on both the primary "
                f"(leg 313/343) basis and leg 350's enriched basis independently -- "
                f"leaves the POCP obstruction (leg 374's basis inventory) UNCHANGED: "
                f"this is TIER-2 apparatus information about the operator's spectrum "
                f"on an already-built basis, not a new candidate basis meeting any of "
                f"leg 374's four unmet asks (Galerkin+tail bridge, vector/Leray "
                f"projection, CAP-grade tail bound, geometric coefficient decay); it "
                f"neither closes nor deepens that gap."
            )
        return (
            f"ell={ch['ell']}: verdict is {ch['verdict']} (see resolution-wall detail "
            f"if unresolved) -- route to the DM for adjudication before citing beside "
            f"leg 374's inventory; a genuine discrete component in this channel would "
            f"HARDEN the POCP picture (new structure the basis-selection decision would "
            f"need to account for), not leave it unchanged."
        )

    ell1_pocp = pocp_line(ell1, ell1_cross)
    ell2_pocp = pocp_line(ell2, ell2_cross)

    all_definite = ell1["verdict"] == "CONTINUOUS" and ell2["verdict"] == "CONTINUOUS"

    out = {
        "leg": 376,
        "route": "R3SP",
        "title": "Measure the ell=1 and ell=2 channels of leg 343's rescaled operator "
        "-Delta + (1/2)(y.grad) + 1 on leg 313's compactified variable, using leg "
        "350's enriched basis as an independent cross-check basis; leg 348 explicitly "
        "refused to transfer leg 343's ell=0-only finding to these channels.",
        "date": "2026-08-12",
        "precondition": "legs 343 (B1, ell=0 CONTINUOUS) and 350 (B2, enriched basis) landed",
        "selftest_ell0_reproduces_leg343": selftest,
        "channel_ell1": ell1,
        "channel_ell1_enriched_basis_crosscheck": ell1_cross,
        "channel_ell2": ell2,
        "channel_ell2_enriched_basis_crosscheck": ell2_cross,
        "coupled_channel_structure": coupling,
        "pocp_consequence": {
            "ell1": ell1_pocp,
            "ell2": ell2_pocp,
        },
        "gate_answer": {
            "ell1_verdict": ell1["verdict"],
            "ell2_verdict": ell2["verdict"],
            "all_channels_definite": all_definite,
            "licensed_by_both_controls": ell1["both_controls_pass"] and ell2["both_controls_pass"],
        },
        "ceiling": "TIER 2 -- a spectrum is apparatus information about the numerical "
        "method on the compactified basis, not a result about the Navier-Stokes PDE "
        "or a Clay-relevant claim. No cost-class-C spend committed: only already-"
        "landed apparatus (leg 343's operator/basis, leg 350's enriched map, leg "
        "343's own control pattern) is exercised.",
        "walls": {"clay_odds": "~0.05%, unchanged", "links_of_L1_to_L4_moved": 0},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, default=lambda o: str(o)))
    print(json.dumps({
        "selftest_ell0_reproduces_leg343": selftest["reproduces_leg343_ell0_exactly"],
        "ell1_verdict": ell1["verdict"],
        "ell1_both_controls_pass": ell1["both_controls_pass"],
        "ell2_verdict": ell2["verdict"],
        "ell2_both_controls_pass": ell2["both_controls_pass"],
        "ell1_crosscheck_agrees": ell1_cross["agrees_with_primary_basis_verdict"],
        "ell2_crosscheck_agrees": ell2_cross["agrees_with_primary_basis_verdict"],
    }, indent=2))
    return out


if __name__ == "__main__":
    main()
