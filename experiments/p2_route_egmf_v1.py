"""Leg 329 -- ROUTE-EGMF: do `T2_egm|B4_egm` and `T2_egm|E_egm` pass all five of
leg 178's clauses at arbitrary precision?

Gate, verbatim from the DM's pre-committed brief in `DIRECTION.md`:

    "Do B4_egm and E_egm pass all five clauses at arbitrary precision?
       yes -> Leg 178's NO is measured to flip in substance: REPORT AND ESCALATE
              to the user -- parked escalation #3's resolution is the user's; the
              historical gate stays byte-identical, the flip lives in this leg's
              own record.
       no  -> Bank the corrected magnitudes and which clause still fails;
              escalation #3 stays parked, the artifact explanation stands refined,
              not overturned."

EVERYTHING THIS DRIVER DECIDES WAS DECIDED BEFORE IT EXISTED.  The five clauses
and their constants, the precision protocol (`prec`, the patch threshold `tau`,
and the decision NOT to patch `phi` or the quadrature weights), and the ten
controls C1-C10 -- four of which can come out AGAINST a flip -- are
`writeup/novelty/leg_329.md` sections 7, 7a and 7b, committed to `main` at
`e81a6ea` before any number in this file existed.  This runner executes that
pre-registration and chooses nothing.

WHAT IS NOT CLAIMABLE (inherited verbatim from leg 178, unchanged)
-----------------------------------------------------------------
The construction is Elgindi-Ghoul-Masmoudi arXiv:1906.05811 Prop. 2.1 and the
framing is Xu arXiv:2607.19762 sec 3.1.  Neither is this repository's.  EGM buy
the origin conditions with two free modulation parameters, so a gap on a
constrained trial space is NOT a certificate.  No stage is claimed, no ban is
lifted, and no link of the L1 -> L4 chain moves from anything below.

Leg 178's runner, its JSON and its gate text are READ-ONLY to this leg and are
not edited.  `solver/energy_coercivity.py` is read-only likewise: the assembly
below MIRRORS its published formulas (which is what lets `F` be patched between
the pointwise contraction and the weighting) and is checked against it by
control C1.

Run:    `.venv/bin/python experiments/p2_route_egmf_v1.py`
Writes: `writeup/data/p2_route_egmf_v1.json`
"""

from __future__ import annotations

import json
import math
import sys
import time
from decimal import Context, Decimal, localcontext
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.energy_coercivity import (  # noqa: E402
    KNOWN_ANSWER_CEILING,
    WES_CONSTRAINT_CLASSES,
    WES_PROBE_VECTORS,
    clm_linearization_values,
    graded_quadrature,
    wes_admissibility,
    wes_coercivity_gap_exact,
    wes_constrained_basis,
    wes_constraint_rows,
    wes_damping_factor,
    wes_weight_values,
)
from solver.interval_mp import assert_exact_as_decimal  # noqa: E402

# leg 312's landed capability, re-used BY IMPORT, not by copy
# (writeup/novelty/leg_329.md sec 4).
from experiments.p2_route_apia_v1 import (  # noqa: E402
    _mp_sin_cos,
    _spot_check_against_rigorous_mp,
)

OUT = ROOT / "writeup" / "data" / "p2_route_egmf_v1.json"
WES_JSON = ROOT / "writeup" / "data" / "p2_route_wes_v1_space.json"

# ---------------------------------------------------------------------------
# LEG 178's OWN CONSTANTS.  Copied verbatim from experiments/p2_route_wes_v1_space.py.
# None is retuned, loosened or reinterpreted (novelty pass sec 7).
# ---------------------------------------------------------------------------
N_LADDER = (32, 64, 128, 256)
GRADE_DEPTHS = (12, 24, 48, 96)
N_QUAD_CHECK = 128
LADDER_N_GRADE = 24
ORDER = 12
RCOND = 1e-12
REL_STABILITY_TOL = 0.05        # leg 111's own tolerance
QUAD_SPREAD_TOL = 1e-3          # the disqualifier that killed leg 111's A3 at 2.665e-01
ADMISS_TOL = 1e-6
CEILING_SLACK = 1e-9

# ---------------------------------------------------------------------------
# THIS LEG's own protocol constants -- novelty pass sec 7a, fixed before any run.
# ---------------------------------------------------------------------------
PREC = 200          # working decimal digits
TAU = 1e-1          # min(theta, pi-theta) below this is recomputed in MP
TAU_LADDER = (1e-3, 1e-2, 1e-1)     # control C2
TAU_ALL = 3.2                       # > pi: patches EVERY node (post-hoc control C2b)
PREC_LADDER = (200, 400)            # control C3
RCOND_LADDER = (1e-14, 1e-12, 1e-10, 1e-8)   # control C5

PRIMARY_ROWS = (("T2_egm", "B4_egm", "B", 4.0), ("T2_egm", "E_egm", "E", 4.0))
C6_ROWS = (("T3_hilbert_only", "B4_egm", "B", 4.0), ("T1_dprime", "B4_egm", "B", 4.0))
C7_ROW = ("T2_egm", "A4_chen_hou", "A", 4.0)
ALL_ROWS = PRIMARY_ROWS + C6_ROWS + (C7_ROW,)

C1_REL_TOL = 1e-12
C2_REL_TOL = 1e-12
C3_REL_TOL = 1e-12
C5_SPREAD_TOL = 1e-6
C10_GUARD_DIGITS = 40

_EPS = float(np.finfo(float).eps)


def rel_spread(xs):
    """Leg 178's own `rel_spread`, byte-for-byte."""
    xs = [float(x) for x in xs]
    lo, hi = min(xs), max(xs)
    denom = max(abs(sum(xs) / len(xs)), 1e-300)
    return (hi - lo) / denom


def rel_diff(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ===========================================================================
# The MP patch.  Leg 312's protocol, generalised from one cell to twenty-eight.
# ===========================================================================
def _mp_sin_cos_all_k(theta_dec, n_k, prec):
    """`sin(k th)` and `cos(k th)` for `k = 1..n_k`, from ONE base pair by the
    angle-addition recurrence (leg 312's `_mp_recurrence_all_k`, extended to
    return the cosines the linearisation and the Hilbert transform also need)."""
    with localcontext(Context(prec=prec)):
        s1, c1 = _mp_sin_cos(theta_dec, prec)
        sk, ck = s1, c1
        sins, coss = [s1], [c1]
        for _ in range(2, n_k + 1):
            sk, ck = sk * c1 + ck * s1, ck * c1 - sk * s1
            sins.append(sk)
            coss.append(ck)
        return sins, coss, s1, c1


_PATCH_CACHE = {}


def mp_patch(class_name, n, n_grade, n_unif, tau=TAU, prec=PREC, order=ORDER,
             verbose=True):
    """Recompute `F = V^T E`, `LF = V^T LE`, `HF = V^T HE` in `Decimal` at every
    node with `min(theta, pi - theta) < tau`, leaving the mesh, the weight `phi`
    and the quadrature weights EXACTLY as float64 produced them.

    The float64 loss lives in the POINTWISE contraction (an `O(theta^{2p+1})`
    cancellation between `O(theta)` terms), not in `phi` or `qw`, both of which
    are cancellation-free by inspection -- patching only where the cancellation
    is, is leg 312's own protocol (novelty pass sec 7a) and it is inherited here
    unchanged.  The mesh is deliberately NOT patched: the object being
    re-measured is leg 178's quadrature rule, evaluated exactly, and moving the
    nodes would measure a different rule.  Diagnostic D1 below reports what that
    choice costs.
    """
    key = (class_name, n, n_grade, n_unif, tau, prec, order)
    if key in _PATCH_CACHE:
        return _PATCH_CACHE[key]
    t0 = time.time()

    th, qw = graded_quadrature(n_unif=n_unif, n_grade=n_grade, order=order)
    for x in th[:5]:
        assert_exact_as_decimal(x)      # float -> Decimal is exact; spot-checked
    V = wes_constrained_basis(n, class_name)
    ks = np.arange(1, n + 1)
    E = np.stack([np.sin(k * th) for k in ks])
    LE = np.stack([clm_linearization_values(th, int(k)) for k in ks])
    HE = np.stack([-np.cos(k * th) + (-1.0) ** int(k) for k in ks])
    F_f, LF_f, HF_f = V.T @ E, V.T @ LE, V.T @ HE

    # ---- control C8: the constrained basis is EXACTLY constrained
    R = wes_constraint_rows(n, class_name)
    c8_residual = float(np.max(np.abs(R @ V))) if R.size else 0.0

    # ---- diagnostic D1: nodes the float64 MESH cannot represent at all
    dist = np.minimum(th, math.pi - th)
    n_collapsed = int(np.sum(dist == 0.0))

    V_int = np.rint(V).astype(np.int64)
    assert np.max(np.abs(V - V_int)) == 0.0, "constrained basis is not integral"
    nz = [np.nonzero(V_int[:, m])[0] for m in range(V.shape[1])]

    unsafe_idx = np.nonzero(dist < tau)[0]
    F_p, LF_p, HF_p = F_f.copy(), LF_f.copy(), HF_f.copy()
    # control C10 ingredients, accumulated over the patched nodes
    Fabs = np.abs(V).T @ np.abs(E)
    worst_depth = 0.0
    worst_depth_at = None

    for i in unsafe_idx:
        theta_dec = Decimal(float(th[i]))
        with localcontext(Context(prec=prec)):
            sins, coss, s_th, c_th = _mp_sin_cos_all_k(theta_dec, n, prec)
            le_k, he_k = [], []
            for k in range(1, n + 1):
                sk_, ck_ = sins[k - 1], coss[k - 1]
                alt = Decimal((-1) ** k)
                le_k.append(c_th * sk_ - s_th * (-ck_ + alt) - Decimal(k) * s_th * ck_)
                he_k.append(-ck_ + alt)
            for m in range(V.shape[1]):
                idx = nz[m]
                if idx.size == 0:
                    continue
                fs = Decimal(0)
                fl = Decimal(0)
                fh = Decimal(0)
                for k in idx:
                    coef = Decimal(int(V_int[k, m]))
                    fs += coef * sins[k]
                    fl += coef * le_k[k]
                    fh += coef * he_k[k]
                F_p[m, i] = float(fs)
                LF_p[m, i] = float(fl)
                HF_p[m, i] = float(fh)
                # C10: how many digits of cancellation did this entry actually meet?
                if fs != 0:
                    d = math.log10(Fabs[m, i] / abs(float(fs))) if Fabs[m, i] > 0 else 0.0
                    if d > worst_depth:
                        worst_depth, worst_depth_at = d, (int(m), int(i))

    # per-node effective machine epsilon under the patch: 10^-prec where patched
    eps_node = np.full(th.shape, _EPS)
    eps_node[unsafe_idx] = 10.0 ** (-prec)

    res = {
        "th": th, "qw": qw, "V": V, "E": E,
        "F_float": F_f, "LF_float": LF_f, "HF_float": HF_f,
        "F_mp": F_p, "LF_mp": LF_p, "HF_mp": HF_p,
        "Fabs": Fabs, "eps_node": eps_node,
        "meta": {
            "class": class_name, "n": int(n), "n_grade": int(n_grade),
            "n_unif": int(n_unif), "order": int(order), "tau": tau, "prec": prec,
            "n_nodes": int(len(th)), "n_patched": int(len(unsafe_idx)),
            "C8_exact_basis_constraint_residual": c8_residual,
            "C10_max_cancellation_digits": worst_depth,
            "C10_worst_at_col_node": worst_depth_at,
            "C10_budget_ok": bool(worst_depth + C10_GUARD_DIGITS < prec),
            "D1_nodes_with_collapsed_endpoint_distance": n_collapsed,
            "seconds": time.time() - t0,
        },
    }
    _PATCH_CACHE[key] = res
    if verbose:
        m = res["meta"]
        print(f"   patch {class_name:16s} n={n:4d} ng={n_grade:3d} tau={tau:g} "
              f"prec={prec}: {m['n_patched']:5d}/{m['n_nodes']:5d} nodes, "
              f"cancel {worst_depth:6.2f} digits, {m['seconds']:6.1f}s")
    return res


def assemble_gap(patch, family, gamma, which="mp", rcond=RCOND):
    """`wes_form_matrices_constrained` + `wes_coercivity_gap_exact`, mirrored
    exactly, on either the float64 or the MP-patched pointwise contraction.
    Control C1 checks this mirror against the module itself."""
    th, qw = patch["th"], patch["qw"]
    F = patch["F_mp"] if which == "mp" else patch["F_float"]
    LF = patch["LF_mp"] if which == "mp" else patch["LF_float"]
    HF = patch["HF_mp"] if which == "mp" else patch["HF_float"]
    phi = wes_weight_values(th, family, gamma)
    pw = phi * qw
    G = (F * pw) @ F.T
    B = (F * pw) @ LF.T

    eps = patch["eps_node"] if which == "mp" else np.full(th.shape, _EPS)
    num = ((eps * patch["Fabs"]) ** 2 * pw).sum(axis=1)
    den = (F ** 2 * pw).sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        contamination = float(np.nanmax(np.where(den > 0, num / den, 0.0)))

    D = wes_damping_factor(th, family, gamma)
    B_loc = (F * (pw * D)) @ F.T
    sw = pw * np.sin(th)
    M = (F * sw) @ HF.T
    B_nl = -0.5 * (M + M.T)
    S = 0.5 * (B + B.T)
    scale = float(np.max(np.abs(S))) if S.size else 1.0
    resid = float(np.max(np.abs(S - B_loc - B_nl))) / (scale if scale > 0 else 1.0)

    ev, U = np.linalg.eigh(0.5 * (G + G.T))
    top = float(ev.max()) if ev.size else 0.0
    keep = ev > rcond * top
    dropped = int(np.sum(~keep))
    if not np.any(keep):
        return {"gap": float("nan"), "contamination": contamination,
                "dropped": dropped, "dim_kept": 0, "cond_G": float("inf"),
                "local_gap": None, "nonlocal_gap": None,
                "byparts_rel_residual": resid, "argmax": None}
    W = U[:, keep] / np.sqrt(ev[keep])

    def rayleigh(Mat, want_vec=False):
        Mh = W.T @ (0.5 * (Mat + Mat.T)) @ W
        Mh = 0.5 * (Mh + Mh.T)
        if not want_vec:
            return -float(np.linalg.eigvalsh(Mh).max())
        w, Q = np.linalg.eigh(Mh)
        return -float(w.max()), W @ Q[:, -1]

    gap, xmax = rayleigh(0.5 * (B + B.T), want_vec=True)
    return {
        "gap": gap, "local_gap": rayleigh(B_loc), "nonlocal_gap": rayleigh(B_nl),
        "contamination": contamination, "byparts_rel_residual": resid,
        "dim_trial": int(G.shape[0]), "dim_kept": int(np.sum(keep)),
        "dropped": dropped, "cond_G": float(top / float(ev[keep].min())),
        "argmax": xmax,
    }


# ===========================================================================
# Control C4: an MP Rayleigh quotient that bypasses the float64 assembly and
# the float64 eigensolve entirely.  CAN COME OUT AGAINST A FLIP.
# ===========================================================================
def mp_rayleigh_at(patch, family, gamma, x):
    """`R(x) = (x^T Sym(B) x)/(x^T G x)` evaluated NODE BY NODE in `Decimal`:

        R = sum_i pw_i f(th_i) lf(th_i) / sum_i pw_i f(th_i)^2,
        f  = sum_m x_m F_m(th_i),   lf = sum_m x_m LF_m(th_i).

    Because `x` is a genuine trial vector, `R(x) <= lambda_max`, hence
    `-R(x) >= gap`: a rigorous UPPER bound on the gap that never forms `G` or `B`
    and never calls an eigensolver.  Clause 5 is a one-sided ceiling, so an upper
    bound is exactly the side that can refute it.
    """
    th, qw = patch["th"], patch["qw"]
    F, LF = patch["F_mp"], patch["LF_mp"]
    phi = wes_weight_values(th, family, gamma)
    with localcontext(Context(prec=PREC)):
        xs = [Decimal(float(v)) for v in x]
        nzx = [m for m in range(len(xs)) if xs[m] != 0]
        num = Decimal(0)
        den = Decimal(0)
        for i in range(len(th)):
            pw = Decimal(float(phi[i])) * Decimal(float(qw[i]))
            f = Decimal(0)
            lf = Decimal(0)
            for m in nzx:
                f += xs[m] * Decimal(float(F[m, i]))
                lf += xs[m] * Decimal(float(LF[m, i]))
            num += pw * f * lf
            den += pw * f * f
        if den == 0:
            return None
        return float(num / den)


# ===========================================================================
# The five clauses -- leg 178's, unchanged.
# ===========================================================================
def five_clauses(ladder_gaps, quad_gaps, adm_ratio, exponent_margin):
    g = list(ladder_gaps)
    steps = []
    for i in (len(g) - 2, len(g) - 1):
        prev = g[i - 1]
        steps.append(abs(g[i] - prev) / max(abs(prev), 1e-300))
    qspread = rel_spread(quad_gaps)
    c_pos = bool(all(x > 0 for x in g))
    c_grid = bool(all(s <= REL_STABILITY_TOL for s in steps))
    c_quad = bool(qspread <= QUAD_SPREAD_TOL)
    c_adm = bool(abs(adm_ratio - 1.0) <= ADMISS_TOL and exponent_margin > 0)
    c_ceil = bool(g[-1] <= KNOWN_ANSWER_CEILING + CEILING_SLACK)
    return {
        "rel_steps_last_two": steps, "quad_rel_spread": qspread,
        "clause_positive": c_pos, "clause_grid_stable": c_grid,
        "clause_quad_stable": c_quad, "clause_admissible": c_adm,
        "clause_under_ceiling": c_ceil,
        "PASS": bool(c_pos and c_grid and c_quad and c_adm and c_ceil),
        "failing_clauses": [k for k, v in (("clause_positive", c_pos),
                                           ("clause_grid_stable", c_grid),
                                           ("clause_quad_stable", c_quad),
                                           ("clause_admissible", c_adm),
                                           ("clause_under_ceiling", c_ceil))
                            if not v],
    }


# ===========================================================================
# Clause 4 at arbitrary precision: the probe norm and the constrained Gram top.
# ===========================================================================
ADM_N_SPACE = 32
ADM_N_UNIF = 128


def mp_probe_norm2(class_name, family, gamma, n_grade):
    """`||h||^2_phi` for the class's own integer probe vector, with the pointwise
    cancellation done in `Decimal`.  The probe has at most three modes, so this
    is cheap and needs no basis machinery."""
    c = [int(round(v)) for v in WES_PROBE_VECTORS[class_name]]
    th, qw = graded_quadrature(n_unif=ADM_N_UNIF, n_grade=n_grade, order=ORDER)
    phi = wes_weight_values(th, family, gamma)
    dist = np.minimum(th, math.pi - th)
    tot = 0.0
    with localcontext(Context(prec=PREC)):
        for i in range(len(th)):
            if dist[i] < TAU:
                sins, _, _, _ = _mp_sin_cos_all_k(Decimal(float(th[i])), len(c), PREC)
                h = Decimal(0)
                for j, cj in enumerate(c):
                    if cj:
                        h += Decimal(cj) * sins[j]
                hv = float(h)
            else:
                hv = float(sum(cj * math.sin((j + 1) * th[i])
                               for j, cj in enumerate(c)))
            tot += hv * hv * float(phi[i]) * float(qw[i])
    return tot


def mp_gram_top(class_name, family, gamma, n_grade):
    p = mp_patch(class_name, ADM_N_SPACE, n_grade, ADM_N_UNIF)
    th, qw = p["th"], p["qw"]
    pw = wes_weight_values(th, family, gamma) * qw
    F = p["F_mp"]
    G = (F * pw) @ F.T
    return float(np.linalg.eigvalsh(0.5 * (G + G.T)).max())


def mp_admissibility(class_name, family, gamma):
    a = mp_probe_norm2(class_name, family, gamma, LADDER_N_GRADE)
    b = mp_probe_norm2(class_name, family, gamma, 2 * LADDER_N_GRADE)
    ga = mp_gram_top(class_name, family, gamma, LADDER_N_GRADE)
    gb = mp_gram_top(class_name, family, gamma, 2 * LADDER_N_GRADE)
    p = dict((x[0], x[2]) for x in WES_CONSTRAINT_CLASSES)[class_name]
    return {
        "norm2_coarse": a, "norm2_fine": b,
        "ratio": (b / a if a > 0 else float("inf")),
        "gram_top_coarse": ga, "gram_top_fine": gb,
        "gram_top_ratio": (gb / ga if ga > 0 else float("inf")),
        "vanishing_order_declared": float(p),
        "exponent_margin": float(2 * p + 1) - float(gamma),
    }


# ===========================================================================
def main():
    t_start = time.time()
    banked = json.loads(WES_JSON.read_text())

    out = {
        "leg": 329,
        "route": "ROUTE-EGMF",
        "role": "LEG",
        "claim_bearing": True,
        "gate": ("Do B4_egm and E_egm pass all five clauses at arbitrary "
                 "precision?"),
        "gate_branches": {
            "yes": ("Leg 178's NO is measured to flip in substance: REPORT AND "
                    "ESCALATE to the orchestrator/user -- parked escalation #3's "
                    "resolution is the user's; the historical gate text stays "
                    "byte-identical, the flip lives in this leg's own record only."),
            "no": ("Bank the corrected magnitudes and which clause still fails; "
                   "escalation #3 stays parked, the artifact explanation stands "
                   "refined, not overturned."),
        },
        "not_claimable": banked["not_claimable"],
        "ceiling": (
            "The MP patch is applied to the POINTWISE CONTRACTION ONLY. It is a "
            "high-precision recomputation, NOT an interval enclosure, so nothing "
            "here is a rigorous bound except control C4's MP Rayleigh quotient, "
            "which is a genuine one-sided bound because it evaluates a real trial "
            "vector. Object is the a = 0 CLM linearisation: a gap measured here "
            "bounds difficulty FROM BELOW, never above. No stage claimed, no ban "
            "lifted, no link of the L1 -> L4 chain moved. Clay odds ~0.05%."),
        "pre_registration": {
            "file": "writeup/novelty/leg_329.md",
            "committed_before_any_number_at": "e81a6ea (main)",
            "leg178_constants_reused_verbatim": {
                "n_ladder": list(N_LADDER), "grade_depths": list(GRADE_DEPTHS),
                "n_quad_check": N_QUAD_CHECK, "ladder_n_grade": LADDER_N_GRADE,
                "order": ORDER, "rcond": RCOND,
                "rel_stability_tol": REL_STABILITY_TOL,
                "quad_spread_tol": QUAD_SPREAD_TOL, "admiss_tol": ADMISS_TOL,
                "ceiling_slack": CEILING_SLACK,
                "known_answer_ceiling": KNOWN_ANSWER_CEILING,
            },
            "this_legs_own_protocol": {"prec": PREC, "tau": TAU,
                                       "phi_and_qw_patched": False,
                                       "mesh_patched": False},
        },
        "reads_only": ["writeup/data/p2_route_wes_v1_space.json",
                       "solver/interval_mp.py (leg 312, landed d89bedd)",
                       "experiments/p2_route_apia_v1.py (leg 312, by import)"],
    }

    # ------------------------------------------------------------------ C9
    print("== control C9: the fast adaptive sin/cos series vs the RIGOROUS "
          "MPInterval dsin/dcos")
    th96, _ = graded_quadrature(n_unif=4 * N_QUAD_CHECK, n_grade=96, order=ORDER)
    d96 = np.minimum(th96, math.pi - th96)
    idx = np.nonzero(d96 < TAU)[0]
    order_by = idx[np.argsort(d96[idx])]
    sample = np.unique(np.concatenate([order_by[:4], order_by[len(order_by) // 2:
                                                             len(order_by) // 2 + 2],
                                       order_by[-4:]]))
    c9 = _spot_check_against_rigorous_mp(
        [Decimal(float(min(th96[i], math.pi - th96[i]))) for i in sample],
        prec=PREC, n_report=len(sample))
    out["control_C9_series_containment"] = {
        "n_sampled": int(len(sample)), "all_contained": c9["all_contained"],
        "rows": c9["rows"],
        "meaning": ("every sampled node's fast series value lies INSIDE leg 312's "
                    "rigorous MPInterval enclosure; any escape withdraws the "
                    "result"),
    }
    print(f"   {len(sample)} nodes sampled, all_contained = {c9['all_contained']}")

    # ------------------------------------------------------- build the patches
    print(f"== MP patches (prec={PREC}, tau={TAU:g}); mesh, phi and qw untouched")
    configs = ([(n, LADDER_N_GRADE, max(64, 4 * n)) for n in N_LADDER]
               + [(N_QUAD_CHECK, ng, max(64, 4 * N_QUAD_CHECK)) for ng in GRADE_DEPTHS])
    configs = sorted(set(configs))
    classes = sorted({r[0] for r in ALL_ROWS})
    for cls in classes:
        for (n, ng, nu) in configs:
            mp_patch(cls, n, ng, nu)
        mp_patch(cls, ADM_N_SPACE, LADDER_N_GRADE, ADM_N_UNIF)
        mp_patch(cls, ADM_N_SPACE, 2 * LADDER_N_GRADE, ADM_N_UNIF)

    patch_meta = {f"{k[0]}|n{k[1]}|ng{k[2]}|tau{k[4]:g}|prec{k[5]}": v["meta"]
                  for k, v in _PATCH_CACHE.items()}
    out["patch_provenance"] = patch_meta
    out["control_C8_exact_basis"] = {
        "max_constraint_residual_over_all_patches":
            max(v["C8_exact_basis_constraint_residual"] for v in patch_meta.values()),
        "all_exactly_zero": all(v["C8_exact_basis_constraint_residual"] == 0.0
                                for v in patch_meta.values()),
    }
    out["control_C10_cancellation_budget"] = {
        "guard_digits": C10_GUARD_DIGITS, "prec": PREC,
        "max_cancellation_digits_met":
            max(v["C10_max_cancellation_digits"] for v in patch_meta.values()),
        "all_within_budget": all(v["C10_budget_ok"] for v in patch_meta.values()),
    }
    out["diagnostic_D1_mesh_representation"] = {
        "nodes_with_collapsed_endpoint_distance":
            {k: v["D1_nodes_with_collapsed_endpoint_distance"]
             for k, v in patch_meta.items()},
        "note": ("min(theta, pi-theta) == 0.0 EXACTLY in float64 for some nodes at "
                 "n_grade >= 48: the geometric refinement at the RIGHT endpoint "
                 "descends below the float64 spacing near pi (4.44e-16), so those "
                 "panels collapse onto pi itself. This is a MESH representation "
                 "failure, distinct from the pointwise-contraction failure this leg "
                 "patches, and it is NOT repaired here -- repairing it would measure "
                 "a different quadrature rule than leg 178's. Its size is bounded by "
                 "control D1b below."),
    }

    # ------------------------------------------------------ D1b: is D1 binding?
    p96 = mp_patch("T2_egm", N_QUAD_CHECK, 96, 4 * N_QUAD_CHECK)
    th, qw = p96["th"], p96["qw"]
    collapsed = np.nonzero(np.minimum(th, math.pi - th) == 0.0)[0]
    d1b = {}
    for cls, wname, fam, gam in PRIMARY_ROWS:
        pp = mp_patch(cls, N_QUAD_CHECK, 96, 4 * N_QUAD_CHECK)
        pw = wes_weight_values(pp["th"], fam, gam) * pp["qw"]
        F = pp["F_mp"]
        Gd_all = (F ** 2 * pw).sum(axis=1)
        Gd_col = (F[:, collapsed] ** 2 * pw[collapsed]).sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            frac = float(np.nanmax(np.where(Gd_all > 0, Gd_col / Gd_all, 0.0)))
        g_with = assemble_gap(pp, fam, gam, "mp")["gap"]
        keep = np.ones(len(th), bool)
        keep[collapsed] = False
        pp2 = dict(pp)
        pp2 = {**pp, "th": pp["th"][keep], "qw": pp["qw"][keep],
               "F_mp": pp["F_mp"][:, keep], "LF_mp": pp["LF_mp"][:, keep],
               "HF_mp": pp["HF_mp"][:, keep], "F_float": pp["F_float"][:, keep],
               "LF_float": pp["LF_float"][:, keep], "HF_float": pp["HF_float"][:, keep],
               "Fabs": pp["Fabs"][:, keep], "eps_node": pp["eps_node"][keep]}
        g_without = assemble_gap(pp2, fam, gam, "mp")["gap"]
        d1b[f"{cls}|{wname}"] = {
            "n_collapsed_nodes": int(len(collapsed)),
            "max_fraction_of_a_gram_diagonal": frac,
            "gap_mp_with_collapsed_nodes": g_with,
            "gap_mp_with_collapsed_nodes_deleted": g_without,
            "abs_diff": abs(g_with - g_without),
        }
        print(f"   D1b {cls}|{wname}: gap {g_with:.12f} (kept) vs {g_without:.12f} "
              f"(deleted), diff {abs(g_with - g_without):.2e}")
    out["diagnostic_D1b_collapsed_node_influence"] = {
        "rows": d1b, "n_grade": 96, "n": N_QUAD_CHECK,
        "note": ("deleting the collapsed nodes outright is a DIFFERENT rule and is "
                 "reported only to size D1, never as the gate-answering number"),
    }

    # ---------------------------------------------------------- the ladders
    print("== gap ladders and quadrature sweeps, float64 mirror and MP-patched")
    rows = {}
    for cls, wname, fam, gam in ALL_ROWS:
        key = f"{cls}|{wname}"
        ladder_f, ladder_m, ladder_full = [], [], []
        for n in N_LADDER:
            p = mp_patch(cls, n, LADDER_N_GRADE, max(64, 4 * n))
            rf = assemble_gap(p, fam, gam, "float")
            rm = assemble_gap(p, fam, gam, "mp")
            ladder_f.append(rf["gap"])
            ladder_m.append(rm["gap"])
            ladder_full.append({"n": n,
                                "float": {k: v for k, v in rf.items() if k != "argmax"},
                                "mp": {k: v for k, v in rm.items() if k != "argmax"}})
        quad_f, quad_m, quad_full = [], [], []
        for ng in GRADE_DEPTHS:
            p = mp_patch(cls, N_QUAD_CHECK, ng, 4 * N_QUAD_CHECK)
            rf = assemble_gap(p, fam, gam, "float")
            rm = assemble_gap(p, fam, gam, "mp")
            quad_f.append(rf["gap"])
            quad_m.append(rm["gap"])
            quad_full.append({"n_grade": ng,
                              "float": {k: v for k, v in rf.items() if k != "argmax"},
                              "mp": {k: v for k, v in rm.items() if k != "argmax"}})
        adm_f = wes_admissibility(cls, fam, gam)
        adm_m = mp_admissibility(cls, fam, gam)
        v_f = five_clauses(ladder_f, quad_f, adm_f["ratio"], adm_f["exponent_margin"])
        v_m = five_clauses(ladder_m, quad_m, adm_m["ratio"], adm_m["exponent_margin"])
        rows[key] = {
            "class": cls, "weight": wname, "family": fam, "gamma": gam,
            "float64_mirror": {"gap_ladder": ladder_f, "quad_gaps": quad_f,
                               "admissibility": adm_f, "verdict": v_f},
            "mp": {"gap_ladder": ladder_m, "quad_gaps": quad_m,
                   "admissibility": adm_m, "verdict": v_m},
            "detail_ladder": ladder_full, "detail_quad": quad_full,
        }
        print(f"   {key:28s} float64 PASS={v_f['PASS']!s:5s} -> MP PASS={v_m['PASS']!s:5s}"
              f"   gap(n=256) {ladder_f[-1]:+.10f} -> {ladder_m[-1]:+.10f}"
              f"   quad spread {v_f['quad_rel_spread']:.4e} -> "
              f"{v_m['quad_rel_spread']:.4e}")
    out["rows"] = rows

    # ------------------------------------------------------------------ C1
    print("== control C1: does the float64 mirror reproduce leg 178's BANKED numbers?")
    c1 = {}
    for cls, wname, fam, gam in ALL_ROWS:
        key = f"{cls}|{wname}"
        bv = banked["verdicts"][key]
        bq = banked["quadrature_stability"][key]
        mine = rows[key]["float64_mirror"]
        dl = [rel_diff(a, b) for a, b in zip(mine["gap_ladder"], bv["gap_ladder"])]
        dq = [rel_diff(a, b) for a, b in zip(mine["quad_gaps"], bq["gaps"])]
        c1[key] = {"max_rel_diff_gap_ladder": max(dl),
                   "max_rel_diff_quad_sweep": max(dq),
                   "banked_gap_ladder": bv["gap_ladder"],
                   "mirror_gap_ladder": mine["gap_ladder"],
                   "banked_quad_gaps": bq["gaps"], "mirror_quad_gaps": mine["quad_gaps"],
                   "banked_clauses": {k: bv[k] for k in
                                      ("clause_positive", "clause_grid_stable",
                                       "clause_quad_stable", "clause_admissible",
                                       "clause_under_ceiling", "PASS")},
                   "mirror_clauses": {k: mine["verdict"][k] for k in
                                      ("clause_positive", "clause_grid_stable",
                                       "clause_quad_stable", "clause_admissible",
                                       "clause_under_ceiling", "PASS")},
                   "ok": bool(max(dl) <= C1_REL_TOL and max(dq) <= C1_REL_TOL)}
        print(f"   {key:28s} max rel diff  ladder {max(dl):.2e}  quad {max(dq):.2e}"
              f"   ok={c1[key]['ok']}")
    out["control_C1_reproduction"] = {
        "tol": C1_REL_TOL, "rows": c1, "all_ok": all(v["ok"] for v in c1.values()),
        "meaning": ("if the unpatched path in THIS runner does not reproduce leg "
                    "178's banked numbers, this leg is not measuring leg 178's "
                    "object and nothing is comparable -- result withdrawn"),
    }

    # ------------------------------------------------------------------ C2
    print(f"== control C2: tau-independence at n={N_QUAD_CHECK}, n_grade=96")
    c2 = {}
    for cls, wname, fam, gam in PRIMARY_ROWS:
        vals = []
        for tau in TAU_LADDER:
            p = mp_patch(cls, N_QUAD_CHECK, 96, 4 * N_QUAD_CHECK, tau=tau)
            vals.append(assemble_gap(p, fam, gam, "mp")["gap"])
        c2[f"{cls}|{wname}"] = {"tau": list(TAU_LADDER), "gaps": vals,
                                "rel_spread": rel_spread(vals),
                                "ok": bool(rel_spread(vals) <= C2_REL_TOL)}
        print(f"   {cls}|{wname}: " + "  ".join(f"{v:+.14f}" for v in vals)
              + f"   spread {rel_spread(vals):.2e}")
    out["control_C2_tau_independence"] = {
        "tol": C2_REL_TOL, "rows": c2, "all_ok": all(v["ok"] for v in c2.values()),
        "pre_registered_failure_meaning": ("disagreement => the patch boundary is "
                                           "itself the answer => withdraw"),
    }

    # --------------------------------------------------------------- C2b
    # POST-HOC, ADDED AFTER C2 WAS SEEN TO FAIL.  Labelled as such, and it is
    # NOT permitted to rescue a `yes` (see gate_answer.disposition below).  It
    # tests the MECHANISM C2 names: at tau > pi every node is patched, so there
    # is NO patch boundary at all.  If the value still scatters in the same
    # band, "the patch boundary is itself the answer" is measurably false and
    # the scatter must be attributed elsewhere.  The competing attribution is
    # quantitative and predicted in advance of looking: the float64 whitening
    # and eigensolve at condition number `cond(G)` lose `cond(G) * eps`.
    print("== control C2b (POST-HOC): tau > pi patches EVERY node, so there is no "
          "patch boundary; and the cond(G)*eps prediction")
    c2b = {}
    for cls, wname, fam, gam in PRIMARY_ROWS:
        entry = {}
        for label, (n, ng, nu) in (("n128_ng96", (N_QUAD_CHECK, 96, 4 * N_QUAD_CHECK)),
                                   ("n256_ng24", (N_LADDER[-1], LADDER_N_GRADE,
                                                  4 * N_LADDER[-1]))):
            p_bnd = mp_patch(cls, n, ng, nu)
            p_all = mp_patch(cls, n, ng, nu, tau=TAU_ALL)
            r_bnd = assemble_gap(p_bnd, fam, gam, "mp")
            r_all = assemble_gap(p_all, fam, gam, "mp")
            entry[label] = {
                "n": n, "n_grade": ng,
                "gap_tau_boundary": r_bnd["gap"], "gap_all_nodes_patched": r_all["gap"],
                "abs_diff": abs(r_bnd["gap"] - r_all["gap"]),
                "cond_G": r_bnd["cond_G"],
                "predicted_float64_noise_band_cond_G_times_eps": r_bnd["cond_G"] * _EPS,
                "diff_inside_predicted_band":
                    bool(abs(r_bnd["gap"] - r_all["gap"]) <= r_bnd["cond_G"] * _EPS),
            }
            print(f"   {cls}|{wname} {label}: boundary {r_bnd['gap']:.14f}  "
                  f"all-patched {r_all['gap']:.14f}  diff "
                  f"{abs(r_bnd['gap'] - r_all['gap']):.2e}  "
                  f"cond(G)*eps {r_bnd['cond_G'] * _EPS:.2e}")
        c2b[f"{cls}|{wname}"] = entry
    out["control_C2b_no_boundary_posthoc"] = {
        "status": "POST-HOC -- added after C2 failed; may not rescue a yes",
        "tau_all": TAU_ALL, "rows": c2b,
        "mechanism_named_by_C2_refuted": all(
            e[k]["diff_inside_predicted_band"] for e in c2b.values() for k in e),
    }

    # ------------------------------------------------------------------ C3
    print(f"== control C3: precision-independence at n={N_QUAD_CHECK}, n_grade=96")
    c3 = {}
    for cls, wname, fam, gam in PRIMARY_ROWS:
        vals = []
        for pr in PREC_LADDER:
            p = mp_patch(cls, N_QUAD_CHECK, 96, 4 * N_QUAD_CHECK, prec=pr)
            vals.append(assemble_gap(p, fam, gam, "mp")["gap"])
        c3[f"{cls}|{wname}"] = {"prec": list(PREC_LADDER), "gaps": vals,
                                "rel_spread": rel_spread(vals),
                                "ok": bool(rel_spread(vals) <= C3_REL_TOL)}
        print(f"   {cls}|{wname}: " + "  ".join(f"{v:+.14f}" for v in vals)
              + f"   spread {rel_spread(vals):.2e}")
    out["control_C3_precision_independence"] = {
        "tol": C3_REL_TOL, "rows": c3, "all_ok": all(v["ok"] for v in c3.values())}

    # ------------------------------------------------------------------ C4
    print("== control C4: MP Rayleigh at the float64 maximiser -- a one-sided "
          "bound that bypasses the assembly AND the eigensolve")
    c4 = {}
    for cls, wname, fam, gam in PRIMARY_ROWS:
        p = mp_patch(cls, N_LADDER[-1], LADDER_N_GRADE, max(64, 4 * N_LADDER[-1]))
        r = assemble_gap(p, fam, gam, "mp")
        R = mp_rayleigh_at(p, fam, gam, r["argmax"])
        gap_bound = -R
        c4[f"{cls}|{wname}"] = {
            "n": N_LADDER[-1], "gap_mp_eigensolve": r["gap"],
            "minus_R_mp_upper_bound_on_gap": gap_bound,
            "abs_diff": abs(r["gap"] - gap_bound),
            "cond_G": r["cond_G"],
            "float64_noise_band_cond_G_times_eps": r["cond_G"] * _EPS,
            "diff_inside_float64_noise_band":
                bool(abs(r["gap"] - gap_bound) <= r["cond_G"] * _EPS),
            "bound_under_ceiling": bool(gap_bound <= KNOWN_ANSWER_CEILING
                                        + CEILING_SLACK),
            "ok": bool(abs(r["gap"] - gap_bound) <= CEILING_SLACK),
        }
        print(f"   {cls}|{wname}: eigensolve {r['gap']:+.14f}   -R_mp "
              f"{gap_bound:+.14f}   diff {abs(r['gap'] - gap_bound):.2e}   "
              f"cond(G) {r['cond_G']:.2e}")
    out["control_C4_mp_rayleigh"] = {
        "tol": CEILING_SLACK, "rows": c4, "all_ok": all(v["ok"] for v in c4.values()),
        "meaning": ("-R(x) for a genuine trial vector x is >= the true gap, so it "
                    "is the side of the one-sided ceiling clause that can refute "
                    "it. Pre-registered: a disagreement above CEILING_SLACK "
                    "declares clause 5 NOT ESTABLISHABLE and the gate answers no."),
    }

    # ------------------------------------------------------------------ C5
    print(f"== control C5: rcond ladder at n={N_LADDER[-1]}")
    c5 = {}
    for cls, wname, fam, gam in PRIMARY_ROWS:
        p = mp_patch(cls, N_LADDER[-1], LADDER_N_GRADE, max(64, 4 * N_LADDER[-1]))
        vals = [assemble_gap(p, fam, gam, "mp", rcond=rc)["gap"] for rc in RCOND_LADDER]
        drops = [assemble_gap(p, fam, gam, "mp", rcond=rc)["dropped"]
                 for rc in RCOND_LADDER]
        c5[f"{cls}|{wname}"] = {"rcond": list(RCOND_LADDER), "gaps": vals,
                                "dropped": drops, "rel_spread": rel_spread(vals),
                                "ok": bool(rel_spread(vals) <= C5_SPREAD_TOL)}
        print(f"   {cls}|{wname}: " + "  ".join(f"{v:+.10f}" for v in vals)
              + f"   spread {rel_spread(vals):.2e}  dropped {drops}")
    out["control_C5_rcond_ladder"] = {
        "tol": C5_SPREAD_TOL, "rows": c5, "all_ok": all(v["ok"] for v in c5.values()),
        "meaning": ("a spread above 1e-6 means the reported gap is a property of "
                    "the truncation, not of the operator; clause 5 is then not "
                    "credited"),
    }

    # ------------------------------------------------------------------ C6
    c6 = {}
    for cls, wname, fam, gam in C6_ROWS:
        key = f"{cls}|{wname}"
        v = rows[key]["mp"]["verdict"]
        c6[key] = {"PASS_under_mp": v["PASS"], "failing_clauses": v["failing_clauses"],
                   "gap_ladder_mp": rows[key]["mp"]["gap_ladder"],
                   "still_fails": bool(not v["PASS"])}
    out["control_C6_falsification_rows"] = {
        "rows": c6, "all_ok": all(v["still_fails"] for v in c6.values()),
        "meaning": ("T3_hilbert_only has vanishing order 1 so gamma=4 is outside "
                    "its own window, and T1_dprime keeps one point mode so its raw "
                    "gap is bounded above by -1. If the MP patch makes either PASS, "
                    "the patch is manufacturing passes rather than removing "
                    "cancellation, and this leg's result is WITHDRAWN."),
    }
    print(f"== control C6: falsification rows still fail under MP = "
          f"{out['control_C6_falsification_rows']['all_ok']}")

    # ------------------------------------------------------------------ C7
    cls, wname, fam, gam = C7_ROW
    key = f"{cls}|{wname}"
    g256 = rows[key]["mp"]["gap_ladder"][-1]
    out["control_C7_ceiling_control"] = {
        "row": key,
        "banked_gap_n256": banked["verdicts"][key]["gap_n256"],
        "mp_gap_n256": g256,
        "banked_contamination_n256": banked["verdicts"][key]["contamination_n256"],
        "still_above_ceiling": bool(g256 > KNOWN_ANSWER_CEILING + CEILING_SLACK),
        "excess_above_ceiling": g256 - KNOWN_ANSWER_CEILING,
        "mp_verdict": rows[key]["mp"]["verdict"],
        "ok": bool(g256 > KNOWN_ANSWER_CEILING + CEILING_SLACK),
        "meaning": ("A4_chen_hou sits 3.8e-05 ABOVE the ceiling with an n=256 "
                    "contamination of 4.1e-17, so no credible float64 effect is "
                    "that size. If MP moves it below 0.5, the patch is changing "
                    "the answer where no float64 error exists."),
    }
    print(f"== control C7: {key} MP gap(n=256) {g256:+.10f} "
          f"(banked {banked['verdicts'][key]['gap_n256']:+.10f}), still above "
          f"ceiling = {out['control_C7_ceiling_control']['ok']}")

    # ------------------------------------------------------------- the gate
    controls = {
        "C1_reproduction": out["control_C1_reproduction"]["all_ok"],
        "C2_tau_independence": out["control_C2_tau_independence"]["all_ok"],
        "C3_precision_independence": out["control_C3_precision_independence"]["all_ok"],
        "C4_mp_rayleigh": out["control_C4_mp_rayleigh"]["all_ok"],
        "C5_rcond_ladder": out["control_C5_rcond_ladder"]["all_ok"],
        "C6_falsification_rows_still_fail": out["control_C6_falsification_rows"]["all_ok"],
        "C7_ceiling_control_unmoved": out["control_C7_ceiling_control"]["ok"],
        "C8_exact_basis": out["control_C8_exact_basis"]["all_exactly_zero"],
        "C9_series_containment": out["control_C9_series_containment"]["all_contained"],
        "C10_cancellation_budget": out["control_C10_cancellation_budget"]["all_within_budget"],
    }
    withdrawing = [k for k in ("C1_reproduction", "C2_tau_independence",
                               "C3_precision_independence",
                               "C6_falsification_rows_still_fail",
                               "C9_series_containment", "C10_cancellation_budget")
                   if not controls[k]]
    both_pass = all(rows[f"{c}|{w}"]["mp"]["verdict"]["PASS"] for c, w, _, _ in PRIMARY_ROWS)
    clause5_establishable = (controls["C4_mp_rayleigh"] and controls["C5_rcond_ladder"])
    gate_yes = bool(both_pass and clause5_establishable and not withdrawing)

    out["gate_answer"] = {
        "answer": "YES" if gate_yes else "NO",
        "withdrawn_under_literal_pre_registration": bool(withdrawing),
        "withdrawing_controls": withdrawing,
        "both_primary_rows_pass_all_five": both_pass,
        "clause5_establishable_C4_and_C5": clause5_establishable,
        "controls": controls,
        "per_row": {
            f"{c}|{w}": {
                "banked_gap_n256": banked["verdicts"][f"{c}|{w}"]["gap_n256"],
                "mp_gap_n256": rows[f"{c}|{w}"]["mp"]["gap_ladder"][-1],
                "banked_quad_rel_spread": banked["verdicts"][f"{c}|{w}"]["quad_rel_spread"],
                "mp_quad_rel_spread": rows[f"{c}|{w}"]["mp"]["verdict"]["quad_rel_spread"],
                "banked_n_grade_96_gap": banked["quadrature_stability"][f"{c}|{w}"]["gaps"][-1],
                "mp_n_grade_96_gap": rows[f"{c}|{w}"]["mp"]["quad_gaps"][-1],
                "mp_failing_clauses": rows[f"{c}|{w}"]["mp"]["verdict"]["failing_clauses"],
                "mp_PASS": rows[f"{c}|{w}"]["mp"]["verdict"]["PASS"],
            } for c, w, _, _ in PRIMARY_ROWS},
        "branch_text": (out["gate_branches"]["yes"] if gate_yes
                        else out["gate_branches"]["no"]),
        "leg178_gate_text_edited": False,
        "escalation_3_status": ("ESCALATE -- resolution is the user's"
                                if gate_yes else "stays parked"),
        "disposition_rule": (
            "C2 fails at its literal pre-registered tolerance. Its failure is NOT "
            "argued away: it is taken at the STRONGER of the two available "
            "readings. The post-hoc control C2b refutes the MECHANISM C2 names "
            "(there is no patch boundary at all at tau > pi and the scatter is "
            "unchanged) and re-attributes the scatter to the float64 whitening and "
            "eigensolve, whose predicted size cond(G)*eps matches it. Neither "
            "reading permits a `yes`, and C2b is explicitly barred from producing "
            "one. The standing rule applied to every number this leg banks: NO "
            "CLAIM RESTS ON A DIFFERENCE SMALLER THAN THE MEASURED NOISE BAND "
            "cond(G)*eps. Clause 3's repair survives that rule by a factor of ~1e4; "
            "clause 5's 1e-9 ceiling slack does not survive it at all, which is "
            "precisely what control C4 was pre-registered to detect."),
        "noise_band_per_row": {
            f"{c}|{w}": c4[f"{c}|{w}"]["float64_noise_band_cond_G_times_eps"]
            for c, w, _, _ in PRIMARY_ROWS},
    }
    out["performance"] = {"total_seconds": time.time() - t_start,
                          "n_patches": len(_PATCH_CACHE),
                          "patch_seconds": sum(v["meta"]["seconds"]
                                               for v in _PATCH_CACHE.values())}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, default=str) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print(f"GATE ANSWER: {out['gate_answer']['answer']}")
    print(f"CONTROLS: {controls}")
    for k, v in out["gate_answer"]["per_row"].items():
        print(f"  {k}: gap(n=256) {v['banked_gap_n256']:+.10f} -> "
              f"{v['mp_gap_n256']:+.10f}; quad spread "
              f"{v['banked_quad_rel_spread']:.4e} -> {v['mp_quad_rel_spread']:.4e}; "
              f"failing {v['mp_failing_clauses']}")
    print(f"total {out['performance']['total_seconds']:.1f}s")


if __name__ == "__main__":
    main()
