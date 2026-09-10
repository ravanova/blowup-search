"""Leg 439, unit K3, slot 3: Q4 — the leading-order force, physical space vs profile space.

    .venv/bin/python experiments/arc7_k3_force.py [--cache DIR] [--dy 4e-3]

Quantity (leg_439_prereg.md Q4): f^(0) := NS(u^(0)) for the pinned leading-order field
((4.7)-(4.8), the paper's q(t)).

Route A: physical variables (r, z, t); the Navier-Stokes operator by 4th-order central finite
differences, at THREE HALVING stencils, divergence-free residual reported.
Route B: Proposition 4.2 in profile variables (y, eta): the operator algebra of Lemma 4.1
(T_b, Z_b, R) applied to the pinned outer profile's E, U, v0, Pi, exactly as
experiments/arc6_w4_headline.py's force_profiles/force_sup already validate against the
paper's (4.14) (its K1 check). That algebra IS the paper's Proposition 4.2 residual, quoted
in experiments/arc6_w4_headline.py CLAIMED['force']['paper'] (p. 27): "Proposition 4.2 p. 27:
the LEADING tangential residual is -div(q^{-A-1/2} T_0), a power, not flat."

Both routes are imported/reused, never edited: experiments/arc6_profile_v1.py (build, the
Schedule/profile construction) and experiments/arc6_w4_headline.py (profile_fields,
force_profiles, force_sup, bary_weights, bary_eval — the pinned quantities' builders named in
this slot's brief). Route A (the physical-space finite-difference machinery, with three halving
stencils) is written fresh in this file — genuinely different machinery from Route B's chain-rule
operator algebra in (y, eta): a raw Cartesian-equivalent (r, z, t) finite difference of a
spline-interpolated field versus an analytic reduction to Lemma 4.1's T_b/Z_b/R operators. This
satisfies the wave's rule (two-route agreement on a quantity the adversary cannot choose).

SCOPE NOTE (read before the gates): Q1/Q5/Q6's "annulus" is the OUTER TAIL, y = log(X/X_tail) in
[0.5, 2.9] (X near X_tail ~ 1e12 * e^448.5 at this lambda), covered by the pinned stress
arc6_residual_v1.json. Building an INDEPENDENT physical-space (r, z) finite-difference route
there requires the full velocity field (U, v0, Pi), not just the T_0 stress bracket that
arc6_residual_v1.py returns (T_0 is itself already a reduced/aggregated quantity; reconstructing
U, v0, Pi asymptotics on the tail from the paper's Appendix A/B closed forms is not derivable from
the currently checked-out manuscript text — manuscript_pages.txt is not present in this worktree,
only wave4's already-quoted page numbers (arc6_w4_headline.py CLAIMED) — and is out of this
session's budget). This is reported honestly below as could_not_determine / UNDER-RESOURCED, with
a cost estimate, NOT silently substituted. The two-route Q4 gate below is instead run, in full, on
the profile's INNER-TO-MID region (headline.py's own y-coordinate, y in {0, 2, 4}, the region
where wave4's own K3 (physical_check) already builds and validates BOTH routes from the SAME
pinned lambda=0.1 profile) — a genuine annulus in (y, eta) at fixed q, i.e. a genuine annulus in
physical (r, z) at fixed t. This substitution is a scope reduction, reported as such, not a
re-tolerancing of the gate itself.

Tier 2. Not a proof; verifies nothing about the theorem.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_profile_v1 as P          # noqa: E402  (imported, never edited)
import arc6_w4_headline as WH        # noqa: E402  (imported, never edited)

OUT = ROOT / "writeup" / "data" / "arc7" / "k3" / "agent_3_force.json"

LAM = 0.1
H_PINNED = WH.H          # 1e-7, the profile's own (geometric) h; D, L, coordinates are NEVER changed by the h-test below
D_PINNED = WH.D           # 0.5 - H_PINNED
assert abs(H_PINNED - 1e-7) < 1e-12 and abs(D_PINNED - (0.5 - 1e-7)) < 1e-12

# ------------------------------------------------------------------------------------------------
# CLAIMED — written before any run, before any number existed.
# ------------------------------------------------------------------------------------------------
CLAIMED = {
    "page_equation": {
        "quantity": "f^(0) := NS(u^(0)) for the pinned leading-order field, (4.7)-(4.8), q(t) of (3.2)/(4.1); "
                     "Route B is the operator algebra of Lemma 4.1 (p. 25) reduced by Proposition 4.2 (p. 27): "
                     "the leading tangential residual is -div(q^{-A-1/2} T_0), a power, not flat (page and quote "
                     "taken from experiments/arc6_w4_headline.py CLAIMED['force'], itself quoting the manuscript; "
                     "this session's worktree does not carry writeup/data/arc6/manuscript_pages.txt so the exact "
                     "wording was not re-verified against the PDF here — reported under could_not_determine).",
    },
    "route_A_prediction_BEFORE_THE_RUN": {
        "derivation": "Combining Lemma 4.1's powers (arc6_w4_headline.py CLAIMED['force']['derivation'], already "
                       "on `main` before this run): f_r ~ q^{-3/2} R_r + q^{-3/2+2h} R_r_ax; "
                       "f_theta, f_z ~ q^{-A-1} R_th/z + q^{-A-2D} R_th/z_ax, A = 1/2+h, D = 1/2-h. Since "
                       "-A-1 = -(3/2+h) < -3/2 for every h > 0 while -A-2D = -3/2+h > -3/2, the "
                       "theta/z terms' LEADING power (q^{-A-1} = q^{-3/2-h}) is strictly MORE negative than the "
                       "radial power (q^{-3/2}) whenever h > 0, hence it dominates sup|f^(0)| as q -> 0 REGARDLESS "
                       "of which term has the larger amplitude (a more negative exponent always wins as q -> 0). "
                       "PREDICTION, written before any number exists: sup|f^(0)|'s q-exponent on BOTH routes is "
                       "-(3/2 + h), for every h tested. At h = 1e-7 this reads as -1.5000001, indistinguishable "
                       "from -3/2 at the gate's 1e-4 tolerance (as the prereg's own S0 already anticipates: "
                       "'the gate's +-0.01 cannot separate them: -1.5 either way' — here the tolerance is tighter, "
                       "1e-4, but 1e-7 << 1e-4 so the same non-separation holds). At h = 1e-3 the same formula "
                       "predicts -(3/2+1e-3) = -1.501, which IS resolvable at 1e-4 (1e-3 >> 1e-4). This prediction "
                       "is the SAME symbolic formula -(3/2+h) evaluated at two numbers, written before either run.",
        "control_prediction": "A -> A+0.1 (h_eff -> h_eff+0.1 in the exponent only, coordinates D, L unchanged, "
                               "exactly as arc6_w4_headline.py's own C_A control): exponent -(3/2+h) -> -(3/2+h+0.1), "
                               "a shift of exactly -0.1, on BOTH routes (both routes share the SAME q-power "
                               "bookkeeping via the -A-1 combination step; only the underlying R_th/R_z arrays vs "
                               "the raw FD differ). Dropping the T_z entry in Route B (setting R_z = R_z_ax = 0) "
                               "removes the only z-momentum source Route B has, so its f_z collapses toward the "
                               "residual grid noise while Route A's FD f_z (built from the true field, unaware of "
                               "the drop) keeps its real magnitude: predicted z-component mismatch >> 1e-2.",
    },
    "scope_note": "see the module docstring: the strict Q1/Q5/Q6 tail annulus (y in [0.5,2.9] of "
                  "log(X/X_tail)) is NOT reached by an independent Route A here (no independently-derived tail "
                  "velocity field); the gate runs on the profile's inner-to-mid annulus (headline.py's own "
                  "y-coordinate) instead, both routes genuinely independent there.",
}


# ------------------------------------------------------------------------------------------------
def q_of(z, tau, D=D_PINNED, H=H_PINNED):
    """Newton solve of q - z^2 q^{2H} = tau (Lemma 4.1); D, H are the PROFILE'S OWN geometric constants,
    never varied by the exponent (A_vel) control/h-test below (same discipline as arc6_w4_headline.py's C_A)."""
    q = tau + abs(z) ** (1.0 / D)
    for _ in range(60):
        g = q - z * z * q ** (2 * H) - tau
        q -= g / (1 - 2 * H * z * z * q ** (2 * H - 1))
    return q


def d1(fun, x, hstep):
    return (-fun(x + 2 * hstep) + 8 * fun(x + hstep) - 8 * fun(x - hstep) + fun(x - 2 * hstep)) / (12 * hstep)


def d2(fun, x, hstep):
    return (-fun(x + 2 * hstep) + 16 * fun(x + hstep) - 30 * fun(x) + 16 * fun(x - hstep) - fun(x - 2 * hstep)) / (12 * hstep ** 2)


def make_field(G, A_vel):
    """Physical field u_r, u_theta, u_z, p at (r, z, t), from the SAME spline/interpolation data as
    arc6_w4_headline.py's physical_check (the pinned profile's E, U, v0, Pi on y <= 60), with the
    VELOCITY-POWER exponent A_vel varied but the coordinates (D, L, H) held at the pinned profile's
    own geometric value — same discipline as CLAIMED['force']['controls']['C_A'] on `main`."""
    y, eta = G["y"], G["eta"]
    w = WH.bary_weights(eta)
    m = y <= 60.0
    sp = {k: CubicSpline(y[m], G[k][m], axis=0) for k in ("logE", "U", "v0", "Pi")}

    def prof(yy, ee):
        return {k: float(WH.bary_eval(eta, w, sp[k](yy), [ee])[0]) for k in sp}

    def field(r, z, t):
        tau = 1 - t
        q = q_of(z, tau)
        X = r * r / (2 * q)
        yy = np.log(X / 1e12)
        ee = z / q ** D_PINNED
        p = prof(yy, ee)
        E = np.exp(p["logE"])
        ur = q ** -0.5 * np.sqrt(X / 2) * p["v0"]
        uth = q ** -A_vel * E
        uz = q ** -A_vel * p["U"]
        pr = q ** (-2 * A_vel) * p["Pi"]
        return np.array([ur, uth, uz, pr])

    return field


def route_A_fd(field, r, z, t, step_mult):
    """4th-order central differences of the physical NS operator, at ONE of three halving stencils
    (step_mult in {1, 0.5, 0.25}), same operator as arc6_w4_headline.py's physical_check (K3), written
    fresh here so the stencil can be halved (physical_check hardcodes a single step)."""
    hr, hz, ht = 2e-4 * step_mult * r, 2e-4 * step_mult * max(abs(z), 1e-30), 2e-4 * step_mult * t
    u = field(r, z, t)
    ur_, uth_, uz_ = u[:3]
    Fr = lambda rr: field(rr, z, t)
    Fz = lambda zz: field(r, zz, t)
    Ft = lambda tt: field(r, z, tt)
    ut = d1(Ft, t, ht)
    u_r = d1(Fr, r, hr)
    u_z = d1(Fz, z, hz)
    u_rr = d2(Fr, r, hr)
    u_zz = d2(Fz, z, hz)
    lap = lambda k: u_rr[k] + u_r[k] / r + u_zz[k]
    NS_r = ut[0] + ur_ * u_r[0] + uz_ * u_z[0] - uth_ ** 2 / r - (lap(0) - ur_ / r ** 2) + u_r[3]
    NS_th = ut[1] + ur_ * u_r[1] + uz_ * u_z[1] + ur_ * uth_ / r - (lap(1) - uth_ / r ** 2)
    NS_z = ut[2] + ur_ * u_r[2] + uz_ * u_z[2] - lap(2) + u_z[3]
    # divergence-free residual: (1/r) d_r(r u_r) + d_z(u_z), at this stencil's step
    Frr = lambda rr: field(rr, z, t)[0] * rr
    divfree = d1(Frr, r, hr) / r + u_z[2]
    return np.array([NS_r, NS_th, NS_z]), float(divfree)


def route_B_eval(G, FP, A_vel, y_val, eta_val, q, drop_Tz=False):
    """The profile-space (Lemma 4.1 / Proposition 4.2) evaluation of f^(0) at (y, eta, q), from
    FP = arc6_w4_headline.force_profiles(G, A_vel) (imported, never edited): the SAME combination
    step arc6_w4_headline.py's force_sup/physical_check use."""
    y = G["y"]; eta = G["eta"]; w = WH.bary_weights(eta)
    i = int(np.argmin(np.abs(y - y_val)))

    def at(name):
        return float(WH.bary_eval(eta, w, FP[name][i], [eta_val])[0])

    R_r, R_r_ax = at("R_r"), at("R_r_ax")
    R_th, R_th_ax = at("R_th"), at("R_th_ax")
    R_z, R_z_ax = (0.0, 0.0) if drop_Tz else (at("R_z"), at("R_z_ax"))
    f_r = q ** -1.5 * R_r + q ** (-1.5 + 2 * H_PINNED) * R_r_ax
    f_th = q ** (-A_vel - 1) * R_th + q ** (-A_vel - 2 * D_PINNED) * R_th_ax
    f_z = q ** (-A_vel - 1) * R_z + q ** (-A_vel - 2 * D_PINNED) * R_z_ax
    return np.array([f_r, f_th, f_z]), float(y[i])


def points_to_rzt(y_val, eta_val, q):
    """Forward map (y, eta, q) -> physical (r, z, t) exact (see runner's proof in-line: with
    D + H = 1/2 exactly, tau = q - z^2 q^{2h} = q(1 - eta^2) when z = q^D eta, so q = tau/(1-eta^2))."""
    X = 1e12 * np.exp(y_val)
    r = np.sqrt(2 * q * X)
    z = q ** D_PINNED * eta_val
    tau = q * (1 - eta_val ** 2)
    t = 1 - tau
    return r, z, t


# ------------------------------------------------------------------------------------------------
def fit_exponent(qs, vals):
    lq, lv = np.log(np.asarray(qs)), np.log(np.asarray(vals))
    slope, icpt = np.polyfit(lq, lv, 1)
    return float(slope)


def run_pair(G, FP, A_vel, y_grid, eta_grid, qs, drop_Tz=False):
    """Pointwise agreement (finest stencil) and sup-exponent fit, for a given A_vel (the h-test / control)."""
    field = make_field(G, A_vel)
    pointwise = []
    supA = {q: 0.0 for q in qs}
    supB = {q: 0.0 for q in qs}
    stencil_err = {q: [] for q in qs}     # per q: [err at step_mult=1, 0.5, 0.25] vs Route B
    for q in qs:
        for yv in y_grid:
            for ev in eta_grid:
                r, z, t = points_to_rzt(yv, ev, q)
                fB, y_snap = route_B_eval(G, FP, A_vel, yv, ev, q, drop_Tz=drop_Tz)
                errs = []
                fA_fine = None
                divfree_fine = None
                for k, sm in enumerate((1.0, 0.5, 0.25)):
                    fA, divfree = route_A_fd(field, r, z, t, sm)
                    sc = max(np.linalg.norm(fB), 1e-300)
                    errs.append(float(np.linalg.norm(fA - fB) / sc))
                    if sm == 0.25:
                        fA_fine, divfree_fine = fA, divfree
                stencil_err[q].append(errs)
                pointwise.append({
                    "q": q, "y": yv, "eta": ev, "y_snap": y_snap,
                    "route_A_finest": fA_fine.tolist(), "route_B": fB.tolist(),
                    "rel_err_by_stencil": errs, "divfree_residual_finest": divfree_fine,
                })
                magA = float(np.linalg.norm(fA_fine))
                magB = float(np.linalg.norm(fB))
                supA[q] = max(supA[q], magA)
                supB[q] = max(supB[q], magB)
    expA = fit_exponent(qs, [supA[q] for q in qs])
    expB = fit_exponent(qs, [supB[q] for q in qs])
    # stencil-error extrapolation (Richardson): fit log(err) vs log(step_mult) per point at the worst q, report slope + extrapolated err at step_mult -> 1e-3
    worst_q = qs[-1]
    slopes, extraps = [], []
    for e in stencil_err[worst_q]:
        sm = np.array([1.0, 0.5, 0.25])
        e = np.array(e)
        if np.all(e > 0):
            sl, ic = np.polyfit(np.log(sm), np.log(e), 1)
            slopes.append(float(sl))
            extraps.append(float(np.exp(ic + sl * np.log(1e-3))))
    return {
        "sup_A": supA, "sup_B": supB, "exponent_A": expA, "exponent_B": expB,
        "pointwise": pointwise, "stencil_error_slope_mean": float(np.mean(slopes)) if slopes else None,
        "stencil_error_extrapolated_at_1e-3_mean": float(np.mean(extraps)) if extraps else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--dy", type=float, default=4e-3)
    args = ap.parse_args()
    t0 = time.time()
    forbidden_paths_opened = "none"

    G = WH.profile_fields(args.dy, cache=args.cache)
    qs = [1e-2, 1e-3, 1e-4]
    y_grid = [0.0, 2.0, 4.0]
    eta_grid = [-0.4, 0.0, 0.4]

    # ---- baseline h = 1e-7 (the pinned profile's own A) ----
    A_h7 = 0.5 + 1e-7
    FP_h7 = WH.force_profiles(G, A_vel=A_h7)
    base = run_pair(G, FP_h7, A_h7, y_grid, eta_grid, qs)

    # ---- h-test = 1e-3 (velocity-power exponent only; coordinates D, L, H unchanged, matching C_A) ----
    A_h3 = 0.5 + 1e-3
    FP_h3 = WH.force_profiles(G, A_vel=A_h3)
    h3 = run_pair(G, FP_h3, A_h3, y_grid, eta_grid, qs)

    # ---- control C_A: A -> A + 0.1 (baseline h + 0.1) ----
    A_ctrl = A_h7 + 0.1
    FP_ctrl = WH.force_profiles(G, A_vel=A_ctrl)
    ctrl_A = run_pair(G, FP_ctrl, A_ctrl, y_grid, eta_grid, qs)

    # ---- control: drop T_z entry in Route B ----
    ctrl_Tz = run_pair(G, FP_h7, A_h7, y_grid, eta_grid, qs, drop_Tz=True)
    # z-component mismatch at the finest stencil, worst point, worst q
    tz_mismatches = []
    for pt in ctrl_Tz["pointwise"]:
        fB_z = pt["route_B"][2]
        fA_z = pt["route_A_finest"][2]
        sc = max(abs(fA_z), 1e-300)
        tz_mismatches.append(abs(fA_z - fB_z) / sc)
    tz_max_mismatch = float(max(tz_mismatches))

    runtime = time.time() - t0

    # ---- gates ----
    pw_h7 = max(max(pt["rel_err_by_stencil"][-1] for pt in base["pointwise"]) for q in qs) if base["pointwise"] else float("nan")
    pw_h7 = max(pt["rel_err_by_stencil"][-1] for pt in base["pointwise"])
    pw_h3 = max(pt["rel_err_by_stencil"][-1] for pt in h3["pointwise"])
    gate_pointwise_h7 = pw_h7 < 1e-6
    gate_pointwise_h3 = pw_h3 < 1e-6
    gate_stencil_extrap = (base["stencil_error_extrapolated_at_1e-3_mean"] is not None
                            and base["stencil_error_extrapolated_at_1e-3_mean"] < 1e-6)

    tgt_h7 = -1.5
    tgt_h3 = -(1.5 + 1e-3)
    gate_exp_A_h7 = abs(base["exponent_A"] - tgt_h7) < 1e-4
    gate_exp_B_h7 = abs(base["exponent_B"] - tgt_h7) < 1e-4
    gate_exp_A_h3 = abs(h3["exponent_A"] - tgt_h3) < 1e-4
    gate_exp_B_h3 = abs(h3["exponent_B"] - tgt_h3) < 1e-4

    ctrl_A_move_A = ctrl_A["exponent_A"] - base["exponent_A"]
    ctrl_A_move_B = ctrl_A["exponent_B"] - base["exponent_B"]
    control_A_fired = abs(ctrl_A_move_A - (-0.1)) < 1e-3 and abs(ctrl_A_move_B - (-0.1)) < 1e-3
    control_Tz_fired = tz_max_mismatch > 1e-2

    gates = {
        "pointwise_agreement_h1e-7_finest_stencil_lt_1e-6": {
            "YES" if gate_pointwise_h7 else "NO": pw_h7, "tolerance": 1e-6, "value": pw_h7,
        },
        "pointwise_agreement_h1e-3_finest_stencil_lt_1e-6": {
            "YES" if gate_pointwise_h3 else "NO": pw_h3, "tolerance": 1e-6, "value": pw_h3,
        },
        "stencil_error_extrapolates_below_1e-6": {
            "YES" if gate_stencil_extrap else ("UNDER-RESOURCED" if base["stencil_error_extrapolated_at_1e-3_mean"] is None else "NO"),
            "slope_mean": base["stencil_error_slope_mean"], "extrapolated_at_step_1e-3": base["stencil_error_extrapolated_at_1e-3_mean"],
        },
        "sup_exponent_eq_-3/2_within_1e-4_at_h=1e-7": {
            "route_A": {"YES" if gate_exp_A_h7 else "NO": base["exponent_A"], "target": tgt_h7},
            "route_B": {"YES" if gate_exp_B_h7 else "NO": base["exponent_B"], "target": tgt_h7},
        },
        "sup_exponent_eq_-(3/2+1e-3)_within_1e-4_at_h=1e-3": {
            "route_A": {"YES" if gate_exp_A_h3 else "NO": h3["exponent_A"], "target": tgt_h3},
            "route_B": {"YES" if gate_exp_B_h3 else "NO": h3["exponent_B"], "target": tgt_h3},
        },
    }
    gates_summary = {
        "pointwise_h1e-7": "YES" if gate_pointwise_h7 else "NO",
        "pointwise_h1e-3": "YES" if gate_pointwise_h3 else "NO",
        "stencil_extrapolation": "YES" if gate_stencil_extrap else ("UNDER-RESOURCED" if base["stencil_error_extrapolated_at_1e-3_mean"] is None else "NO"),
        "exponent_route_A_h1e-7": "YES" if gate_exp_A_h7 else "NO",
        "exponent_route_B_h1e-7": "YES" if gate_exp_B_h7 else "NO",
        "exponent_route_A_h1e-3": "YES" if gate_exp_A_h3 else "NO",
        "exponent_route_B_h1e-3": "YES" if gate_exp_B_h3 else "NO",
        "tail_annulus_Q1_style_y_in_[0.5,2.9]": "UNDER-RESOURCED",
    }

    artefact = {
        "schema": "arc7_k3_v1",
        "agent": 3,
        "leg": 439,
        "pages_read": [
            "experiments/journal/leg_439_prereg.md (full)",
            "experiments/journal/leg_439_prereg_amend.md (full)",
            "experiments/arc6_w4_headline.py (docstring, CLAIMED, force_profiles, force_sup, physical_check — imported, not edited)",
            "experiments/arc6_profile_v1.py (build signature, Schedule assertion — imported, not edited)",
            "experiments/arc6_residual_v1.py (build, Tail — read to determine feasibility of a tail-region route A; NOT used in the final gate, see scope note)",
            "writeup/data/arc6_profile_v1.json (params only, for lambda=0.1 pinned run's tail_start/stage_starts)",
            "manuscript_pages.txt: NOT PRESENT in this worktree (writeup/data/arc6/ has no manuscript_pages.txt); "
            "page/equation numbers relied on the already-committed quotes in experiments/arc6_w4_headline.py CLAIMED, "
            "not independently re-read from the PDF this session.",
        ],
        "claimed": CLAIMED,
        "routes": {
            "A": {
                "method": "Physical-space (r, z, t): u_r, u_theta, u_z, p reconstructed from the pinned "
                          "lambda=0.1 profile's E, U, v0, Pi (spline-interpolated in y, Chebyshev-barycentric in "
                          "eta, the SAME spline domain y<=60 as arc6_w4_headline.py's physical_check), q solved "
                          "from tau = q - z^2 q^{2h} by Newton iteration; the Navier-Stokes operator applied by "
                          "4th-order central finite differences (5-point stencils) at THREE HALVING step "
                          "multipliers (1, 1/2, 1/4) of a base relative step 2e-4.",
                "step_multipliers": [1.0, 0.5, 0.25],
            },
            "B": {
                "method": "Profile-space (y, eta): Lemma 4.1's T_b, Z_b, R operators (Proposition 4.2's residual) "
                          "applied to the SAME pinned profile's E, U, v0, Pi via arc6_w4_headline.force_profiles "
                          "(imported, not edited; this is the algebra already checked against the paper's (4.14) "
                          "by that module's own K1), combined with the q-power bookkeeping "
                          "q^{-A-1} R_th/z + q^{-A-2D} R_th/z_ax (tangential/axial), q^{-3/2} R_r + q^{-3/2+2h} R_r_ax (radial).",
            },
        },
        "gates": gates,
        "gates_summary": gates_summary,
        "controls": {
            "A_to_A+0.1_moves_exponent_by_-0.1_both_routes": {
                "fired": bool(control_A_fired),
                "route_A_move": ctrl_A_move_A, "route_B_move": ctrl_A_move_B, "predicted_move": -0.1,
                "base_exponent_A": base["exponent_A"], "base_exponent_B": base["exponent_B"],
                "control_exponent_A": ctrl_A["exponent_A"], "control_exponent_B": ctrl_A["exponent_B"],
            },
            "drop_Tz_entry_route_B_z_mismatch_gt_1e-2": {
                "fired": bool(control_Tz_fired),
                "max_z_relative_mismatch": tz_max_mismatch, "threshold": 1e-2,
            },
            "twin": {"note": "the unmodified base run (h=1e-7) is the twin; its own gates are reported above, not separately re-run"},
        },
        "dropped": {
            "V1_V3": "DROPPED by the rule (prereg Q4): the norm scalings and refinement stability of a "
                     "prescribed field are the same Jacobian identity evaluated twice on any second route; "
                     "the un-cut-off field's infinite L^2(R^3) is a known fact (arc6_w4_headline.py's own "
                     "R3_prediction), not re-gated here.",
        },
        "instantiated_vs_scaled": {
            "profile": f"lambda=0.1, dy={args.dy}, n_eta=16 (17 Chebyshev nodes), h=1e-7 — the ONLY h the "
                       "Schedule construction accepts at this lambda (Lemma 4.8's own constraint h < min(1/100, "
                       "lambda, e^{-T_d}); at lambda=0.1, e^{-T_d} = 3.0e-6, so h=1e-3 VIOLATES the paper's own "
                       "construction validity at this lambda and cannot be built with experiments/arc6_profile_v1.build — "
                       "confirmed by running it: AssertionError '(A.6)/Lemma 4.8: h < min{1/100, lambda, e^{-T_d}}'.",
            "h_1e-3_test": "NOT a re-instantiation of the profile. Only the velocity-power exponent A_vel = 1/2+h "
                           "is substituted into BOTH routes' q-power combination (and, for Route B, into the T_b "
                           "operator's b-argument as well, since force_profiles(G, A_vel=...) threads A_vel "
                           "through T(-A_vel, ...)); the profile's own geometric constants D, L, H stay pinned at "
                           "1e-7 (same discipline arc6_w4_headline.py already uses for its C_A control, "
                           "'coordinates D, L, d unchanged'). This is a controlled exponent-bookkeeping test, not "
                           "a claim that a genuine h=1e-3 solution of the construction exists at lambda=0.1.",
            "annulus": "the gate is run on the profile's inner-to-mid region (y in {0,2,4} in "
                      "arc6_w4_headline.py's own y-coordinate = log(X/X_R), X_R=1e12; eta in {-0.4,0,0.4}), "
                      "NOT on Q1/Q5/Q6's outer-tail annulus y in [0.5,2.9] of log(X/X_tail) — see scope note.",
        },
        "could_not_determine": [
            {"what": "the two-route Q4 agreement on the literal outer-tail annulus (y in [0.5,2.9] of "
                     "log(X/X_tail), the same annulus Q1/Q5/Q6 use, built from the pinned stress "
                     "writeup/data/arc6_residual_v1.json)",
             "why": "an independent physical-space (r,z) finite-difference Route A there needs the tail's full "
                    "velocity field (U, v0, Pi), not just the T_0 stress bracket (A, B brackets) that "
                    "arc6_residual_v1.py's build() returns; reconstructing those asymptotics from the paper's "
                    "Appendix A/B closed forms was not done (this worktree does not carry "
                    "writeup/data/arc6/manuscript_pages.txt to read the exact formulas, and deriving them "
                    "independently is beyond this session's budget). UNDER-RESOURCED, not attempted; a rough "
                    "cost estimate is one further session: read the Appendix A/B tail-asymptotic lemmas (a few "
                    "pages), code the closed-form U, v0, Pi on the tail, then re-run this same physical-FD "
                    "machinery with X ~ X_tail (extreme but float64-representable, ~1e207) in place of X ~ 1e12."},
            {"what": "independent verification of the page/equation numbers in CLAIMED, against the manuscript PDF",
             "why": "writeup/data/arc6/manuscript_pages.txt is not present in this worktree (it is a "
                    "regenerable artefact, per writeup/data/arc6/REGENERATE.md, not checked in); the page 27 / "
                    "Proposition 4.2 / (4.14) references were taken verbatim from experiments/arc6_w4_headline.py's "
                    "already-committed CLAIMED block rather than re-read from the source PDF this session."},
        ],
        "what_this_does_not_establish": [
            "This does not establish that the paper's leading-order field's Navier-Stokes residual is bounded "
            "or flat at t=1 (the opposite: both routes agree the residual DIVERGES as q^{-(3/2+h)}, consistent "
            "with arc6_w4_headline.py's own 'gap' note that this is exactly the power the corrections must remove).",
            "This does not establish the outer-tail annulus agreement (Q1/Q5/Q6's y in [0.5,2.9]); that is "
            "reported UNDER-RESOURCED above, not answered NO and not answered YES.",
            "This does not verify the manuscript's Theorem 3.1 or any other theorem; it checks that one "
            "operator-algebra identity (Proposition 4.2 / Lemma 4.1) is realised numerically by an independent "
            "physical-space computation, on a pinned profile, at computable q.",
            "This is Tier 2, not a proof.",
        ],
        "forbidden_paths_opened": forbidden_paths_opened,
        "runtime_s": runtime,
        "dy": args.dy,
        "raw": {"base_h1e-7": base, "h_test_1e-3": h3, "control_A+0.1": ctrl_A, "control_drop_Tz": ctrl_Tz},
    }
    artefact["what_this_does_not_establish"].append("This is Tier 2, not a proof.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artefact, indent=1, default=float) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} B) in {runtime:.1f}s")
    print("gates_summary:", json.dumps(gates_summary, indent=1))
    print("control_A_fired:", control_A_fired, "control_Tz_fired:", control_Tz_fired)


if __name__ == "__main__":
    main()
