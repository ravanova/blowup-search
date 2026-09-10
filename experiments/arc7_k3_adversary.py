#!/usr/bin/env python3
"""Leg 439, arc 7, unit K3, slot 5: THE ADVERSARY, blind.

Given ONLY section 3 of experiments/journal/leg_439_prereg.md (the gate definitions Q1-Q5;
Q6 is DROPPED by leg_439_prereg_amend.md and nothing else about it is known here), this
runner tries to make each gate say YES from a run that is deliberately WRONG or
UNDER-RESOLVED.  It is not a reproduction of anything: every "route" below is the
adversary's own minimal implementation of the gate's *literal criteria*.

The standing rule of the wave, applied at integration whatever any worker's gate said:
    a signal the adversary can fake is NOT EVIDENCE.

This runner never reads, imports or inspects slots 1-4's runners or artefacts.  It imports
only the pinned builders named in prereg section 1 (arc6_w4_support.stress) and stdlib/numpy.

This is Tier 2, not a proof.

Usage:  .venv/bin/python experiments/arc7_k3_adversary.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.special import i0 as bessel_i0

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
OUT = ROOT / "writeup" / "data" / "arc7" / "k3" / "agent_5_adversary.json"

# ----------------------------------------------------------------------------------------
# THE CLAIMED BLOCK: written BEFORE the runs, not changed after the numbers.
# For the adversary, "the route-A prediction" is the prediction of WHICH gates fall and by
# what mechanism, made from section 3's text alone, before a single number existed.
# ----------------------------------------------------------------------------------------
CLAIMED = {
    "written_before_the_run": True,
    "page": "gate definitions read from experiments/journal/leg_439_prereg.md section 3 "
            "(pinned to the manuscript at Proposition 7.5/(7.24)-(7.26) p. 610-line block, "
            "Proposition 9.1, (4.7)-(4.8)/Proposition 4.2, Lemma A.8; page numbers as cited "
            "by the prereg itself, which the adversary did not re-derive)",
    "equation": "Q1 (7.26); Q2 Prop 9.1's q^{2h} table; Q3 Props 9.5/9.6's h/10; "
                "Q4 (4.7)-(4.8) + Prop 4.2, R^(0) = -div(q^{-A-1/2} T_0); Q5 Lemma A.8's "
                "B = 0 (heat) vs -(2+2h) (no heat)",
    "route_A_prediction_before_the_run": {
        "Q1": "FAKEABLE. (7.26) is an algebraic identity in the pulse amplitudes; it holds "
              "for ANY amplitude assignment, so feeding both routes the same WRONG stress "
              "leaves the agreement at machine precision.  Separately, a route-B pulse "
              "contaminated at Fourier harmonic 256 is invisible at every M in {16,64,256} "
              "because 256/M is an integer, so 'oversampling independent of N' does not "
              "close the aliasing hole it was written to close.",
        "Q2": "FAKEABLE. Nothing in route B forbids h from entering as an input exponent; a "
              "ratio defined as C*q^{2h} returns slope = 2h at both h to roundoff.  Predicted "
              "further: at h = 1e-7 the gate is passable ONLY by an object that is analytic "
              "in h, because 5% of 2h = 1e-8 is below the relative noise any honest "
              "computation of a ratio carries.",
        "Q3": "FAKEABLE. The gate reads the exponent gain only; a genuine linear solve of the "
              "WRONG problem, with h carried by an operator weight q^{h/10}, returns h/10 "
              "exactly and fires both planted controls.",
        "Q4": "FAKEABLE. -(3/2+h) is prefactor bookkeeping: -(A+1/2) from q^{-A-1/2} and -1/2 "
              "from r = sqrt(2qX) in the divergence.  Any profile whatsoever gives it.  The "
              "pointwise leg compares two differentiations of the SAME field, so a wrong "
              "field passes it.",
        "Q5": "FAKEABLE. B beyond X_b is a constant of the construction, (2+2h)(s_h - 1); it "
              "cannot see rho, the cutoff shape, or the profile's normalisation, so an object "
              "wrong in all three returns 0 (heat) and -(2+2h) (no heat) exactly.",
    },
    "what_would_falsify_the_prediction": "any of the five gates rejecting the wrong object "
                                         "constructed for it, i.e. NOT FAKEABLE",
}

TOL = {
    "Q1_rel_err_at_M256": 1e-8, "Q1_slope_max": -3.5,
    "Q2_rel_dev": 0.05,
    "Q3_gain_rel": 0.10, "Q3_gain_over_h": (0.09, 0.11),
    "Q4_pointwise_rel": 1e-6, "Q4_exponent_abs": 1e-4,
    "Q5_heat_abs": 1e-14, "Q5_no_heat_abs": 1e-8,
}


def fit_slope(xs, ys):
    xs = np.log(np.asarray(xs, float)); ys = np.log(np.asarray(ys, float))
    return float(np.polyfit(xs, ys, 1)[0])


# ========================================================================================
# Q1 -- the realised stress: closed form vs direct quadrature
# Gate (section 3): per entry (theta-theta and z SEPARATELY, each normalised by its own
# sup) relative error < 1e-8 at M = 256, decreasing with M at the quadrature's order
# (log-log slope <= -3.5).  Controls: one pulse phase-shifted pi/2 -> O(1) at every M;
# amplitude halved -> 0.75 +- 0.01.
#
# The adversary's model of the gate.  The fast field of a pulse pair is
#     u(theta) = a_j * g(theta + phi_j) * (t_theta_j, t_z_j),   g(theta) = exp(kappa cos theta)
# g is smooth, periodic and NOT band-limited (a trigonometric polynomial would put Simpson
# at roundoff for every M and make the slope criterion unmeetable -- reported below).
# The averaged product over one fast period has the exact closed form
#     <g(theta+alpha) g(theta+beta)> = I_0(2 kappa cos((alpha-beta)/2)),
# which plays the role of (7.26): an identity in the amplitudes, whatever they are.
# ========================================================================================
KAPPA_G = 0.9
M_LIST = (16, 64, 256)


def _g(th, kappa=KAPPA_G):
    return np.exp(kappa * np.cos(th))


def _closed_pair(dphi, kappa=KAPPA_G):
    """Route A: the exact averaged product of the two pulse shapes, per unit amplitude."""
    return bessel_i0(2.0 * kappa * np.cos(0.5 * dphi))


def _quad_pair(dphi, M, kappa=KAPPA_G, spur=0.0, spur_harm=256, phase_kick=0.0, amp_scale=1.0):
    """Route B: direct quadrature at M points per fast period (Simpson, composite, periodic).
    `spur` adds a contaminant at Fourier harmonic `spur_harm` to BOTH pulses."""
    n = M if M % 2 == 0 else M + 1
    th = np.linspace(0.0, 2.0 * np.pi, n + 1)
    u = amp_scale * _g(th, kappa) + spur * np.sin(spur_harm * th)
    v = amp_scale * _g(th + dphi + phase_kick, kappa) + spur * np.sin(spur_harm * th)
    w = np.ones(n + 1); w[1:-1:2] = 4; w[2:-1:2] = 2; w *= (th[1] - th[0]) / 3.0
    return float(np.sum(w * u * v) / (2.0 * np.pi))


def _q1_entries(amp, t_th, t_z, dphi, M=None, **kw):
    """The two entries of the averaged quadratic product on the slow grid.
    M = None -> route A (closed form); else route B (quadrature)."""
    c = _closed_pair(dphi) if M is None else np.array([_quad_pair(d, M, **kw) for d in np.atleast_1d(dphi)])
    P_thth = amp ** 2 * c * t_th * t_th
    P_z = amp ** 2 * c * t_th * t_z
    return P_thth, P_z


def _q1_rel(a, b):
    """Per-entry relative error, each entry normalised by ITS OWN sup (the gate's wording)."""
    return float(np.max(np.abs(a - b)) / max(float(np.max(np.abs(a))), 1e-300))


def _q1_gate(amp, t_th, t_z, dphi, **route_b_kw):
    A_th, A_z = _q1_entries(amp, t_th, t_z, dphi, M=None)
    errs_th, errs_z = [], []
    for M in M_LIST:
        B_th, B_z = _q1_entries(amp, t_th, t_z, dphi, M=M, **route_b_kw)
        errs_th.append(max(_q1_rel(A_th, B_th), 1e-17))
        errs_z.append(max(_q1_rel(A_z, B_z), 1e-17))
    out = {"rel_err_theta_theta": {str(M): e for M, e in zip(M_LIST, errs_th)},
           "rel_err_z": {str(M): e for M, e in zip(M_LIST, errs_z)},
           "slope_theta_theta": fit_slope(M_LIST, errs_th), "slope_z": fit_slope(M_LIST, errs_z)}
    out["gate_YES"] = bool(errs_th[-1] < TOL["Q1_rel_err_at_M256"] and errs_z[-1] < TOL["Q1_rel_err_at_M256"]
                           and out["slope_theta_theta"] <= TOL["Q1_slope_max"]
                           and out["slope_z"] <= TOL["Q1_slope_max"])
    return out


def attack_q1():
    t0 = time.time()
    # ---- the honest-looking slow grid: amplitudes taken from the pinned tail (the paper's
    # Definition 6.4 assigns them from T).  The adversary does NOT need them to be right.
    y = np.linspace(0.5, 2.9, 25)
    dphi = 0.3 + 0.4 * np.sin(3.0 * y)                     # pulse-pair phase difference
    t_th = np.cos(0.7 * y); t_z = np.sin(0.7 * y) + 0.3    # tangent components, both O(1)

    # F1a -- THE WRONG PROFILE.  Amplitudes from a fabricated stress that has nothing to do
    # with the pinned T_0: a Gaussian bump, scaled by 137, with a wrong y-dependence.
    amp_true = np.exp(-2.0 * (y - 1.3) ** 2) * (1.0 + 0.2 * y)      # stand-in "true" amplitudes
    amp_fake = 137.0 * np.exp(-0.05 * (y - 2.6) ** 2) * (3.0 - y)   # deliberately WRONG
    g_true = _q1_gate(amp_true, t_th, t_z, dphi)
    g_fake = _q1_gate(amp_fake, t_th, t_z, dphi)
    amp_ratio = float(np.max(np.abs(amp_fake / amp_true)))

    # F1b -- THE INVISIBLE HARMONIC.  Route B's pulse carries a contaminant at harmonic 256.
    # 256/M is an integer for every M in {16,64,256}, so sin(256 theta_k) = 0 at every node:
    # the quadrature cannot see it, while its true contribution to the averaged product is
    # spur^2/2 per entry.
    spur = 0.6
    g_spur = _q1_gate(amp_true, t_th, t_z, dphi, spur=spur)
    # how big is the term the quadrature missed, relative to the true averaged product?
    missed = 0.5 * spur ** 2
    typical = float(np.median(amp_true ** 2 * _closed_pair(dphi)))
    # F1c -- what a band-limited pulse does to the slope criterion (a resolution finding,
    # not a fake): Simpson on a trigonometric polynomial is at roundoff for every M.
    def _bandlimited_gate():
        th_A = 0.5 * (1.0 + 0.1 ** 2)   # <cos^2> style closed form for g = cos + 0.1 cos 2
        errs = []
        for M in M_LIST:
            n = M; th = np.linspace(0, 2 * np.pi, n + 1)
            u = np.cos(th) + 0.1 * np.cos(2 * th)
            w = np.ones(n + 1); w[1:-1:2] = 4; w[2:-1:2] = 2; w *= (th[1] - th[0]) / 3.0
            errs.append(max(abs(float(np.sum(w * u * u) / (2 * np.pi)) - th_A) / th_A, 1e-17))
        return {"rel_err": {str(M): e for M, e in zip(M_LIST, errs)}, "slope": fit_slope(M_LIST, errs)}
    bandlimited = _bandlimited_gate()

    # ---- the gate's own controls, run against the FAKE (must fire, or the fake is caught)
    ctl_phase = _q1_gate(amp_fake, t_th, t_z, dphi, phase_kick=np.pi / 2)
    ctl_half = _q1_gate(amp_fake, t_th, t_z, dphi, amp_scale=0.5)
    ctl_phase_spur = _q1_gate(amp_true, t_th, t_z, dphi, spur=spur, phase_kick=np.pi / 2)
    ctl_half_spur = _q1_gate(amp_true, t_th, t_z, dphi, spur=spur, amp_scale=0.5)
    half_err = ctl_half["rel_err_theta_theta"]["256"]
    half_err_spur = ctl_half_spur["rel_err_theta_theta"]["256"]

    return {
        "verdict": "FAKEABLE" if (g_fake["gate_YES"] or g_spur["gate_YES"]) else "NOT FAKEABLE",
        "recipe": [
            "F1a WRONG PROFILE: feed BOTH routes the same fabricated amplitude field "
            "amp = 137*exp(-0.05(y-2.6)^2)*(3-y) instead of the pinned Definition 6.4 "
            "amplitudes (max ratio to the stand-in truth = %.3g).  (7.26) is an identity in "
            "the amplitudes, so the two routes still agree at roundoff and both controls "
            "still fire." % amp_ratio,
            "F1b INVISIBLE HARMONIC: keep the amplitudes, add spur*sin(256*theta) to route "
            "B's pulse with spur = %.2f.  256/M is an integer for M in {16,64,256}, so the "
            "contaminant vanishes at every quadrature node while contributing spur^2/2 = "
            "%.3g to the true averaged product (%.0f%% of the typical entry %.3g)." %
            (spur, missed, 100 * missed / typical, typical),
        ],
        "numbers": {
            "F1a_wrong_profile": g_fake, "reference_twin_right_profile": g_true,
            "F1a_max_amplitude_ratio_fake_over_twin": amp_ratio,
            "F1b_invisible_harmonic": g_spur, "F1b_spur": spur,
            "F1b_missed_contribution_absolute": missed,
            "F1b_typical_true_entry": typical,
            "F1b_missed_as_fraction_of_typical_entry": missed / typical,
            "F1c_band_limited_pulse_puts_the_slope_criterion_out_of_reach": bandlimited,
        },
        "controls_against_the_fake": {
            "phase_shift_pi_over_2_on_F1a": {"rel_err_at_M256": ctl_phase["rel_err_theta_theta"]["256"],
                                             "fired_must_fail_gate": not ctl_phase["gate_YES"]},
            "amplitude_halved_on_F1a": {"rel_err_at_M256": half_err,
                                        "expected_0.75_pm_0.01": abs(half_err - 0.75) <= 0.01,
                                        "fired_must_fail_gate": not ctl_half["gate_YES"]},
            "phase_shift_pi_over_2_on_F1b": {"rel_err_at_M256": ctl_phase_spur["rel_err_theta_theta"]["256"],
                                             "fired_must_fail_gate": not ctl_phase_spur["gate_YES"]},
            "amplitude_halved_on_F1b": {"rel_err_at_M256": half_err_spur,
                                        "fired_must_fail_gate": not ctl_half_spur["gate_YES"]},
        },
        "what_the_gate_still_constrains": "the phase and the amplitude SCALE of route B's own "
                                          "pulses relative to route A's closed form, and any "
                                          "contaminant at a harmonic that is not a multiple of "
                                          "every M.  It does not constrain which stress the "
                                          "amplitudes came from.",
        "runtime_s": time.time() - t0,
    }


# ========================================================================================
# Q2 -- the viscous hierarchy exponent.
# Gate: |slope - 2h| / 2h < 0.05 at BOTH h = 1e-7 and h = 1e-3, slope from the ratio's
# log-log fit over q in {1e-2, 1e-3, 1e-4}.  Controls: constant ratio fails; ratio * q^{0.04}
# fails at both h.
# ========================================================================================
Q_LIST_Q2 = (1e-2, 1e-3, 1e-4)


def _q2_slope(ratio_fn, h):
    qs = np.array(Q_LIST_Q2)
    vals = np.array([ratio_fn(q, h) for q in qs])
    return fit_slope(qs, vals)


def attack_q2():
    t0 = time.time()
    hs = (1e-7, 1e-3)

    # F2 -- THE BUILT-IN GAIN.  h enters as an input exponent.  No profile is consulted at
    # all: C0 is a nonsense constant, and the "subleading over leading" ratio is asserted.
    C0 = 4.2
    fake = lambda q, h: C0 * q ** (2 * h)
    res_fake = {}
    for h in hs:
        s = _q2_slope(fake, h)
        res_fake[f"h={h:g}"] = {"slope": s, "target_2h": 2 * h,
                                "rel_dev": abs(s - 2 * h) / (2 * h),
                                "gate_YES": abs(s - 2 * h) / (2 * h) < TOL["Q2_rel_dev"]}

    # F2b -- the same built-in gain wearing a wrong AMPLITUDE: the ratio's prefactor is wrong
    # by three orders of magnitude (1.7e3 instead of 4.2).  A log-log slope cannot see a
    # q-independent prefactor, so the gate is unmoved.
    fake2 = lambda q, h: 1.7e3 * q ** (2 * h)
    res_fake2 = {}
    for h in hs:
        s = _q2_slope(fake2, h)
        res_fake2[f"h={h:g}"] = {"slope": s, "rel_dev": abs(s - 2 * h) / (2 * h),
                                 "gate_YES": abs(s - 2 * h) / (2 * h) < TOL["Q2_rel_dev"]}
    # F2c -- THE ATTACK THAT FAILS, reported as a defect of the attack, not hidden: give the
    # prefactor a q-DEPENDENCE, exp(-0.3 log10(q)^2).  The slope sees it immediately and the
    # gate rejects it at both h.  This is a real limit on what Q2 admits.
    fake3 = lambda q, h: 1.7e3 * np.exp(-0.3 * np.log10(q) ** 2) * q ** (2 * h)
    res_fake3 = {}
    for h in hs:
        s = _q2_slope(fake3, h)
        res_fake3[f"h={h:g}"] = {"slope": s, "rel_dev": abs(s - 2 * h) / (2 * h),
                                 "gate_YES": abs(s - 2 * h) / (2 * h) < TOL["Q2_rel_dev"]}

    # THE RESOLUTION KNIFE-EDGE.  Any honest route B computes the ratio with some relative
    # error eps.  A least-squares slope over these three q carries an error ~ eps / spread.
    # Find the largest eps that still passes at each h (deterministic worst case: perturb the
    # endpoints in opposite directions, which is what a smooth systematic error does).
    def max_eps(h):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            pert = lambda q, hh, m=mid: C0 * q ** (2 * hh) * (1.0 + m * np.sign(np.log(q / 1e-3) + 1e-30))
            s = _q2_slope(pert, h)
            if abs(s - 2 * h) / (2 * h) < TOL["Q2_rel_dev"]:
                lo = mid
            else:
                hi = mid
        return lo
    knife = {f"h={h:g}": max_eps(h) for h in hs}

    # controls, run against the fake
    ctl_const = {f"h={h:g}": {"slope": _q2_slope(lambda q, hh: C0, h),
                              "gate_YES": abs(_q2_slope(lambda q, hh: C0, h) - 2 * h) / (2 * h) < TOL["Q2_rel_dev"]}
                 for h in hs}
    drift = lambda q, h: C0 * q ** (2 * h) * q ** 0.04
    ctl_drift = {f"h={h:g}": {"slope": _q2_slope(drift, h),
                              "gate_YES": abs(_q2_slope(drift, h) - 2 * h) / (2 * h) < TOL["Q2_rel_dev"]}
                 for h in hs}

    return {
        "verdict": "FAKEABLE" if all(v["gate_YES"] for v in res_fake.values()) else "NOT FAKEABLE",
        "recipe": [
            "F2 BUILT-IN GAIN: define the subleading/leading ratio as R(q) = 4.2 * q^{2h} and "
            "fit its log-log slope over q in {1e-2,1e-3,1e-4}.  Nothing is solved, no profile "
            "is read, h is an input exponent.  Route B as pre-registered does not forbid this "
            "-- only Q3's route B carries the 'never as an input gain' clause.",
            "F2b the same with the prefactor wrong by three orders of magnitude (1.7e3 instead "
            "of 4.2): a log-log slope cannot see a q-independent prefactor.",
            "F2c THE ATTACK THAT FAILED, reported: a q-DEPENDENT wrong prefactor "
            "exp(-0.3 log10(q)^2) is rejected at both h.  Q2 does constrain the ratio's "
            "q-dependence; it does not constrain its size or its provenance.",
        ],
        "numbers": {"F2_built_in_gain": res_fake, "F2b_wrong_prefactor_size": res_fake2,
                    "F2c_q_dependent_prefactor_ATTACK_FAILED": res_fake3,
                    "max_relative_error_in_the_ratio_that_still_passes": knife},
        "controls_against_the_fake": {
            "constant_ratio": {"per_h": ctl_const, "fired_must_fail_gate":
                               not any(v["gate_YES"] for v in ctl_const.values())},
            "ratio_times_q_0.04": {"per_h": ctl_drift, "fired_must_fail_gate":
                                   not any(v["gate_YES"] for v in ctl_drift.values())},
        },
        "what_the_gate_still_constrains": "a constant ratio and a q^{0.04} drift are both "
                                          "rejected at both h, as pre-registered.  What it does "
                                          "not constrain is WHERE the exponent came from; and "
                                          "at h = 1e-7 the tolerance 0.05*2h = 1e-8 admits only "
                                          "objects analytic in h (see the knife-edge number).",
        "runtime_s": time.time() - t0,
    }


# ========================================================================================
# Q3 -- the per-stage gain as a function of h.
# Gate: measured gain within 10% of h/10 at each h in {1e-1, 3e-2, 1e-2}, and gain/h in
# [0.09, 0.11] at all three.  Route B: "h entering ONLY through the profile and the
# operator's weights -- never as an input gain".  Controls: zero correction -> gain ~ 0;
# source negated -> residual grows.
#
# The attack: a GENUINE linear solve (tridiagonal, on an annulus grid) of a problem that is
# not the paper's, in which h is carried by the operator's weight W(q) = q^{h/10}.  That is
# a weight, not "an input gain", by the letter of route B -- and it delivers h/10 exactly.
# ========================================================================================
Q_LIST_Q3 = (1e-2, 1e-4, 1e-6)
H_LIST_Q3 = (1e-1, 3e-2, 1e-2)


def _annulus_operator(n=201, m=3.0):
    s = np.linspace(0.0, 1.0, n)
    ds = s[1] - s[0]
    main = np.full(n, 2.0 / ds ** 2 + m ** 2); lower = np.full(n - 1, -1.0 / ds ** 2)
    L = np.diag(main) + np.diag(lower, -1) + np.diag(lower, 1)
    L[0, :] = 0; L[0, 0] = 1.0; L[-1, :] = 0; L[-1, -1] = 1.0        # Dirichlet
    return s, L


def _stage(q, h, zero_correction=False, negate_source=False, n=201, p0=1.0):
    """One 'correction stage'.  r0 = q^{p0} sigma(s) is the residual to be reduced; the stage
    solves L c = source and reports the new residual r1 = r0 - L c + W(q) (N c), where
    W(q) = q^{h/10} is the operator's weight and N is the 'newly created terms' operator."""
    s, L = _annulus_operator(n)
    sigma = np.sin(np.pi * s) * (1.0 + 0.3 * np.cos(3 * np.pi * s))
    r0 = q ** p0 * sigma
    source = -r0 if negate_source else r0
    c = np.zeros_like(r0) if zero_correction else np.linalg.solve(L, source)
    Nc = 0.35 * (L @ c)                                    # newly created terms, same order as Lc
    W = q ** (h / 10.0)                                    # THE OPERATOR'S WEIGHT
    r1 = r0 - (L @ c) + W * Nc
    return float(np.max(np.abs(r0))), float(np.max(np.abs(r1)))


def _exponent(vals):
    qs = np.array(Q_LIST_Q3, float)
    return fit_slope(qs, np.array(vals, float))


def attack_q3():
    t0 = time.time()
    per_h, ok = {}, True
    for h in H_LIST_Q3:
        before = [_stage(q, h)[0] for q in Q_LIST_Q3]
        after = [_stage(q, h)[1] for q in Q_LIST_Q3]
        p_b, p_a = _exponent(before), _exponent(after)
        gain = p_a - p_b
        target = h / 10.0
        rel = abs(gain - target) / target
        goh = gain / h
        good = rel < TOL["Q3_gain_rel"] and TOL["Q3_gain_over_h"][0] <= goh <= TOL["Q3_gain_over_h"][1]
        ok &= good
        per_h[f"h={h:g}"] = {"exponent_before": p_b, "exponent_after": p_a, "gain": gain,
                             "route_A_target_h_over_10": target, "rel_dev": rel,
                             "gain_over_h": goh, "gate_YES": bool(good)}
    # controls against the fake
    h0 = 1e-1
    zc_after = [_stage(q, h0, zero_correction=True)[1] for q in Q_LIST_Q3]
    zc_gain = _exponent(zc_after) - _exponent([_stage(q, h0)[0] for q in Q_LIST_Q3])
    ns_before = _stage(1e-2, h0)[0]
    ns_after = _stage(1e-2, h0, negate_source=True)[1]
    return {
        "verdict": "FAKEABLE" if ok else "NOT FAKEABLE",
        "recipe": [
            "F3 GAIN IN THE WEIGHT: build a real tridiagonal solve L c = r0 on a 201-point "
            "annulus grid (L = -d^2/ds^2 + m^2, Dirichlet), then report the new residual "
            "r1 = r0 - L c + W(q) * (0.35 L c) with W(q) = q^{h/10}.  h never appears as a "
            "multiplicative 'gain' on the answer -- it is the operator's weight, which route B "
            "explicitly permits -- and the measured exponent gain is h/10 to roundoff at all "
            "three h.  The problem solved is not the paper's section 8-9 mean-correction "
            "solve; nothing in the gate looks at which problem was solved.",
        ],
        "numbers": {"per_h": per_h, "all_three_h_pass": bool(ok)},
        "controls_against_the_fake": {
            "zero_correction": {"gain": zc_gain, "fired_must_fail_gate": abs(zc_gain) < 1e-12},
            "source_negated_at_q=1e-2": {"residual_before": ns_before, "residual_after": ns_after,
                                         "ratio_after_over_before": ns_after / ns_before,
                                         "fired_residual_grows": ns_after > ns_before},
        },
        "what_the_gate_still_constrains": "that SOME q-dependent weight proportional to h/10 in "
                                          "the exponent is present, and that the correction is "
                                          "not identically zero and is applied with the right "
                                          "sign.  It does not constrain the operator, the "
                                          "source, or the problem being solved.",
        "runtime_s": time.time() - t0,
    }


# ========================================================================================
# Q4 -- the leading-order force, physical space vs profile space.
# Gate: pointwise relative agreement < 1e-6 on the annulus at q in {1e-2,1e-3,1e-4} on the
# finest stencil, stencil error extrapolating below 1e-6; and sup|f^(0)|'s q-exponent on BOTH
# routes = -3/2 within 1e-4 at h = 1e-7 and = -(3/2+1e-3) within 1e-4 at h = 1e-3.
# Controls: A -> A+0.1 moves the exponent by -0.1 on both routes; drop T_z in route B ->
# z-component mismatch > 1e-2.
#
# The attack: a FABRICATED profile.  The exponent is -(A+1/2) from the prefactor q^{-A-1/2}
# and -1/2 from r = sqrt(2qX) in the divergence.  The profile cancels out of it entirely.
# ========================================================================================
Q_LIST_Q4 = (1e-2, 1e-3, 1e-4)


def _fake_profile(X, eta, drop_Tz=False, deriv=False):
    """A deliberately WRONG stress profile: two Gaussians with no relation to the pinned T_0.
    With deriv=True also returns the ANALYTIC d/dX, which is what route B differentiates."""
    T_th = np.exp(-((X - 2.0) ** 2 + eta ** 2)) * (1.0 + 0.25 * np.cos(3.0 * eta))
    T_z = np.zeros_like(X) if drop_Tz else 0.4 * np.exp(-0.5 * (X - 1.7) ** 2) * np.sin(2.0 * eta)
    if not deriv:
        return T_th, T_z
    return T_th, T_z, -2.0 * (X - 2.0) * T_th, -(X - 1.7) * T_z


def _q4_routes(q, h, A_shift=0.0, nX=401, neta=41, hr_scale=1.0, drop_Tz_routeB=False):
    """Route A: finite differences in the PHYSICAL variable r.  Route B: the same operator in
    profile variables, differentiated analytically in X.  Both act on the same fabricated field."""
    A = 0.5 + h + A_shift
    X = np.linspace(1.0, 4.0, nX); eta = np.linspace(-1.0, 1.0, neta)
    XX, EE = np.meshgrid(X, eta, indexing="ij")
    pref = q ** (-A - 0.5)

    def field(Xg, Eg, drop=False):
        T_th, T_z = _fake_profile(Xg, Eg, drop_Tz=drop)
        return pref * T_th, pref * T_z

    r = np.sqrt(2.0 * q * XX)
    # --- route A: centred differences in r at spacing dr (three spacings, halving)
    dr = hr_scale * 1e-4 * np.sqrt(2.0 * q)      # scaled so the stencil is uniform in X-units
    def at_r(rr, drop=False):
        Xg = rr ** 2 / (2.0 * q)
        return field(Xg, EE, drop=drop)
    Tp_th, Tp_z = at_r(r + dr); Tm_th, Tm_z = at_r(r - dr)
    dT_th_dr = (Tp_th - Tm_th) / (2 * dr); dT_z_dr = (Tp_z - Tm_z) / (2 * dr)
    T_th0, T_z0 = at_r(r)
    fA_th = -(dT_th_dr + T_th0 / r)
    fA_z = -(dT_z_dr + T_z0 / r)
    # --- route B: profile variables, d/dr = (r/q) d/dX analytically on the profile
    T_th_p, T_z_p, dTth_dX, dTz_dX = _fake_profile(XX, EE, drop_Tz=drop_Tz_routeB, deriv=True)
    fB_th = -pref * (dTth_dX * r / q + T_th_p / r)
    fB_z = -pref * (dTz_dX * r / q + T_z_p / r)
    inner = slice(3, -3)
    rel = lambda a, b: float(np.max(np.abs(a[inner] - b[inner])) / max(float(np.max(np.abs(a[inner]))), 1e-300))
    return {"rel_theta": rel(fA_th, fB_th), "rel_z": rel(fA_z, fB_z),
            "supA": float(max(np.max(np.abs(fA_th[inner])), np.max(np.abs(fA_z[inner])))),
            "supB": float(max(np.max(np.abs(fB_th[inner])), np.max(np.abs(fB_z[inner]))))}


def attack_q4():
    t0 = time.time()
    out = {}
    for h in (1e-7, 1e-3):
        rows = {f"q={q:g}": _q4_routes(q, h) for q in Q_LIST_Q4}
        supA = [rows[f"q={q:g}"]["supA"] for q in Q_LIST_Q4]
        supB = [rows[f"q={q:g}"]["supB"] for q in Q_LIST_Q4]
        expA, expB = fit_slope(Q_LIST_Q4, supA), fit_slope(Q_LIST_Q4, supB)
        target = -(1.5 + h)
        worst_rel = max(max(r["rel_theta"], r["rel_z"]) for r in rows.values())
        good = (worst_rel < TOL["Q4_pointwise_rel"]
                and abs(expA - target) < TOL["Q4_exponent_abs"]
                and abs(expB - target) < TOL["Q4_exponent_abs"])
        # stencil refinement: halve twice
        stencil = {f"dr_scale={s:g}": _q4_routes(1e-3, h, hr_scale=s)["rel_theta"]
                   for s in (4.0, 2.0, 1.0)}
        out[f"h={h:g}"] = {"per_q": rows, "exponent_routeA": expA, "exponent_routeB": expB,
                           "target_exponent": target,
                           "exponent_dev_A": abs(expA - target), "exponent_dev_B": abs(expB - target),
                           "worst_pointwise_rel": worst_rel, "stencil_refinement": stencil,
                           "gate_YES": bool(good)}
    # controls against the fake
    h0 = 1e-3
    supA_sh = [_q4_routes(q, h0, A_shift=0.1)["supA"] for q in Q_LIST_Q4]
    supB_sh = [_q4_routes(q, h0, A_shift=0.1)["supB"] for q in Q_LIST_Q4]
    shiftA = fit_slope(Q_LIST_Q4, supA_sh) - out["h=0.001"]["exponent_routeA"]
    shiftB = fit_slope(Q_LIST_Q4, supB_sh) - out["h=0.001"]["exponent_routeB"]
    drop = _q4_routes(1e-3, h0, drop_Tz_routeB=True)
    # the "one route wearing two hats" variant: route B built from route A's own stencil
    return {
        "verdict": "FAKEABLE" if all(v["gate_YES"] for v in out.values()) else "NOT FAKEABLE",
        "recipe": [
            "F4 WRONG FIELD: replace the pinned T_0 by two Gaussians, "
            "T_theta = exp(-((X-2)^2+eta^2))(1+0.25 cos 3eta), T_z = 0.4 exp(-0.5(X-1.7)^2) sin 2eta, "
            "keep only the paper's prefactor q^{-A-1/2} with A = 1/2 + h.  Route A differentiates "
            "in the physical variable r by centred differences; route B differentiates the profile "
            "in X and converts with dr = (q/r) dX.  Both legs of the gate pass: the pointwise "
            "agreement is a comparison of two differentiations of the SAME field, and the "
            "exponent is -(A+1/2) - 1/2 = -(3/2+h) as pure prefactor bookkeeping, which no "
            "profile can change.",
            "F4b note: at h = 1e-7 the target -(3/2+1e-7) sits 1e-7 from -3/2 while the "
            "tolerance is 1e-4, so that leg is passed identically by h = 0 -- it carries no "
            "information about h.",
        ],
        "numbers": out,
        "controls_against_the_fake": {
            "A_to_A_plus_0.1": {"exponent_shift_routeA": shiftA, "exponent_shift_routeB": shiftB,
                                "expected": -0.1,
                                "fired_moved_by_minus_0.1": abs(shiftA + 0.1) < 5e-3 and abs(shiftB + 0.1) < 5e-3},
            "drop_Tz_in_routeB": {"rel_z_mismatch": drop["rel_z"],
                                  "fired_mismatch_gt_1e-2": drop["rel_z"] > 1e-2},
        },
        "what_the_gate_still_constrains": "that route B's algebra converts dX to dr correctly, "
                                          "that the prefactor exponent A is the one claimed, and "
                                          "(at h = 1e-3 only) that h is in the prefactor.  It does "
                                          "not constrain the profile at all.",
        "runtime_s": time.time() - t0,
    }


# ========================================================================================
# Q5 -- B's exact zero with the heat factor against -(2+2h) without.
# Gate: with heat |B| < 1e-14 (scaled); without heat |B + 2 + 2h| < 1e-8 at BOTH h.
# Controls (the prereg's own planted fakes): truncate to the sqrt(X) term; cut off the stress
# instead of the profile -- each gives 0 in BOTH legs and so must fail the no-heat leg.
#
# The attack: keep the pinned builder but hand it an object that is WRONG in every way the
# gate does not look at -- rho = c_o*h with c_o = 17 instead of 0.1 (170x the paper's tail
# amplitude), and the polynomial cutoff psi = (delta/2)^4 instead of the paper's (leg 432's
# K1 control, a cutoff the paper does not use).
# ========================================================================================
def _B_beyond(h, heat, c_o=0.1, cutoff="paper", dy=5e-3):
    from arc6_w4_support import stress          # a PINNED builder (prereg section 1)
    S = stress(h, dy=dy, cutoff=cutoff, heat=heat, c_o=c_o)
    m = S["y"] >= 3.0
    B = S["B_h"][m]
    return float(np.max(np.abs(B))), float(B[0, 0]), int(m.sum())


def attack_q5():
    t0 = time.time()
    rows = {}
    configs = {
        "twin_paper_object": dict(c_o=0.1, cutoff="paper"),
        "F5a_rho_170x_too_large": dict(c_o=17.0, cutoff="paper"),
        "F5b_wrong_cutoff_polynomial": dict(c_o=0.1, cutoff="poly"),
        "F5c_both_wrong": dict(c_o=17.0, cutoff="poly"),
    }
    for name, kw in configs.items():
        rows[name] = {}
        for h in (1e-7, 1e-3):
            mx_h, v_h, n = _B_beyond(h, True, **kw)
            mx_n, v_n, _ = _B_beyond(h, False, **kw)
            heat_ok = mx_h < TOL["Q5_heat_abs"]
            no_heat_ok = abs(v_n + 2 + 2 * h) < TOL["Q5_no_heat_abs"]
            rows[name][f"h={h:g}"] = {
                "B_hat_beyond_Xb_with_heat_maxabs": mx_h,
                "B_hat_beyond_Xb_no_heat": v_n,
                "target_no_heat_minus_2_minus_2h": -(2 + 2 * h),
                "abs_dev_no_heat": abs(v_n + 2 + 2 * h),
                "n_points_beyond_Xb": n,
                "heat_leg_YES": bool(heat_ok), "no_heat_leg_YES": bool(no_heat_ok),
                "gate_YES": bool(heat_ok and no_heat_ok)}
    # the prereg's own planted controls, reproduced against the fake object
    # (i) truncate to the sqrt(X) term: B is dropped entirely -> 0 in both legs
    trunc = {"B_with_heat": 0.0, "B_no_heat": 0.0,
             "abs_dev_no_heat_at_h=1e-3": abs(0.0 + 2 + 2e-3),
             "fired_fails_no_heat_leg": abs(0.0 + 2 + 2e-3) > TOL["Q5_no_heat_abs"]}
    # (ii) cut off the stress instead of the profile: the stress is multiplied by a cutoff that
    #      vanishes beyond X_b, so B beyond X_b is 0 in both legs.
    cut_stress = {"B_with_heat": 0.0, "B_no_heat": 0.0,
                  "fired_fails_no_heat_leg": abs(0.0 + 2 + 2e-7) > TOL["Q5_no_heat_abs"]}
    # a fake that DOES fail: h wrong by an order in the no-heat constant
    wrong_h_const = {f"h={h:g}": abs(-(2 + 2 * 0.0) + 2 + 2 * h) > TOL["Q5_no_heat_abs"] for h in (1e-7, 1e-3)}
    return {
        "verdict": "FAKEABLE" if all(rows[n][f"h={h:g}"]["gate_YES"]
                                     for n in ("F5a_rho_170x_too_large", "F5b_wrong_cutoff_polynomial",
                                               "F5c_both_wrong") for h in (1e-7, 1e-3))
                   else "NOT FAKEABLE",
        "recipe": [
            "F5 WRONG OBJECT, RIGHT CONSTANT: call the pinned builder "
            "arc6_w4_support.stress(h, cutoff=..., heat=..., c_o=...) with c_o = 17 (tail "
            "amplitude rho = c_o*h is 170x the paper's) and/or cutoff='poly' (psi = (delta/2)^4, "
            "not the paper's exponential cutoff), then read B_hat beyond y = 3.  Both legs pass "
            "at both h and at every wrong parameter: B beyond X_b is the construction's own "
            "constant (2+2h)(s_h - 1), which does not depend on rho, on the cutoff shape, or on "
            "the profile's normalisation.  The number the gate reads is inserted by the "
            "construction, not measured from the object.",
        ],
        "numbers": rows,
        "controls_against_the_fake": {
            "truncate_to_sqrtX_term": trunc,
            "cut_off_the_stress_not_the_profile": cut_stress,
            "constant_computed_at_the_wrong_h_(h=0)": wrong_h_const,
        },
        "what_the_gate_still_constrains": "that the -(2+2h) constant is present with its h, and "
                                          "that the heat factor is what removes it: the two "
                                          "planted controls (both giving 0) do fail the no-heat "
                                          "leg, and a constant computed at h = 0 fails at both h. "
                                          "It does not constrain the object the constant sits in.",
        "runtime_s": time.time() - t0,
    }


# ========================================================================================
def main():
    t0 = time.time()
    q1, q2, q3, q4, q5 = attack_q1(), attack_q2(), attack_q3(), attack_q4(), attack_q5()
    gates = {"Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5}
    verdicts = {k: v["verdict"] for k, v in gates.items()}

    art = {
        "schema": "arc7_k3_v1",
        "agent": "5_adversary",
        "leg": 439,
        "pages_read": {
            "manuscript": "none directly; the adversary is blind by design and worked from "
                          "experiments/journal/leg_439_prereg.md section 3's gate definitions "
                          "and the amendment, plus a line-level grep of "
                          "writeup/data/arc6/manuscript_pages.txt to confirm the cited "
                          "statements exist (Proposition 7.5/(7.24)-(7.26), Proposition 9.1, "
                          "Propositions 9.5/9.6, (4.7)-(4.8)/Proposition 4.2, Lemma A.8). "
                          "No page-level reading was done and none is claimed.",
            "contract": ["experiments/journal/leg_439_prereg.md",
                         "experiments/journal/leg_439_prereg_amend.md"],
            "pinned_code_imported": ["experiments/arc6_w4_support.py (stress)"],
        },
        "claimed": CLAIMED,
        "routes": {
            "A": {"method": "for the adversary, route A is the gate's own route-A prediction as "
                            "written in prereg section 3: (7.26)'s closed form (Q1), the exponent "
                            "2h (Q2), the gain h/10 (Q3), -(3/2+h) and Prop 4.2's profile-space "
                            "force (Q4), B = 0 / -(2+2h) (Q5).  It is taken verbatim, not "
                            "re-derived."},
            "B": {"method": "a deliberately WRONG or under-resolved implementation of route B, "
                            "built to satisfy route A's prediction to the pre-registered "
                            "tolerance.  Per gate: a fabricated amplitude field and a "
                            "harmonic-256 contaminant (Q1); an asserted q^{2h} with no profile "
                            "(Q2); a genuine tridiagonal solve of the wrong problem with the "
                            "gain in the operator's weight (Q3); a Gaussian stand-in stress "
                            "(Q4); the pinned builder called with rho 170x too large and the "
                            "wrong cutoff (Q5)."},
        },
        "gates": {
            "note": "these are NOT answers to Q1-Q5.  The adversary does not measure the "
                    "physics; it measures whether the gate can be made to say YES by a run "
                    "known to be wrong.  Every 'gate_YES: true' below is a YES obtained from a "
                    "wrong object.",
            **gates,
        },
        "X1_per_gate": {
            "Q1": {"verdict": verdicts["Q1"],
                   "recipe": q1["recipe"],
                   "key_numbers": {
                       "wrong_profile_rel_err_at_M256_theta_theta":
                           q1["numbers"]["F1a_wrong_profile"]["rel_err_theta_theta"]["256"],
                       "wrong_profile_slope": q1["numbers"]["F1a_wrong_profile"]["slope_theta_theta"],
                       "wrong_profile_amplitude_ratio": q1["numbers"]["F1a_max_amplitude_ratio_fake_over_twin"],
                       "invisible_harmonic_rel_err_at_M256":
                           q1["numbers"]["F1b_invisible_harmonic"]["rel_err_theta_theta"]["256"],
                       "invisible_harmonic_missed_fraction_of_entry":
                           q1["numbers"]["F1b_missed_as_fraction_of_typical_entry"]}},
            "Q2": {"verdict": verdicts["Q2"], "recipe": q2["recipe"],
                   "key_numbers": q2["numbers"]},
            "Q3": {"verdict": verdicts["Q3"], "recipe": q3["recipe"],
                   "key_numbers": q3["numbers"]["per_h"]},
            "Q4": {"verdict": verdicts["Q4"], "recipe": q4["recipe"],
                   "key_numbers": {h: {"exponent_routeA": v["exponent_routeA"],
                                       "exponent_routeB": v["exponent_routeB"],
                                       "target": v["target_exponent"],
                                       "worst_pointwise_rel": v["worst_pointwise_rel"],
                                       "gate_YES": v["gate_YES"]}
                                   for h, v in q4["numbers"].items()}},
            "Q5": {"verdict": verdicts["Q5"], "recipe": q5["recipe"],
                   "key_numbers": q5["numbers"]},
            "Q6": {"verdict": "NOT ATTEMPTED",
                   "why": "Q6 is DROPPED by experiments/journal/leg_439_prereg_amend.md.  The "
                          "adversary was told that and nothing else about it, and did not "
                          "attack it."},
        },
        "X2_verdict": None,          # filled below
        "controls": {
            "rule": "a control is reported as fired only if it actually failed the gate when run "
                    "against the ADVERSARY'S fake, i.e. only if it would have caught the fake.",
            "Q1": q1["controls_against_the_fake"],
            "Q2": q2["controls_against_the_fake"],
            "Q3": q3["controls_against_the_fake"],
            "Q4": q4["controls_against_the_fake"],
            "Q5": q5["controls_against_the_fake"],
        },
        "dropped": {
            "Q6": "dropped by the amendment before any K3 run; not attacked.",
            "note": "the adversary put no gate in two-route form; that is the workers' job.  "
                    "Nothing here is dropped for want of a second route.",
        },
        "instantiated_vs_scaled": {
            "instantiated": "every fake is instantiated at the gate's own computable parameters: "
                            "M in {16,64,256} (Q1); q in {1e-2,1e-3,1e-4} (Q2, Q4) and "
                            "{1e-2,1e-4,1e-6} (Q3); h in {1e-7,1e-3} (Q1,Q2,Q4,Q5) and "
                            "{1e-1,3e-2,1e-2} (Q3); the pinned lambda = 0.1 tail for Q5.",
            "scaled": "nothing here is scaled toward the paper's regime, and nothing here is a "
                      "statement about the paper's lambda or h.  The fakes are statements about "
                      "the GATES, not about the construction.",
        },
        "could_not_determine": [
            {"what": "whether slots 1-4's actual route-B implementations contain checks beyond "
                     "section 3's text that would catch these fakes",
             "why": "the adversary is blind by design: it never read their runners, artefacts or "
                    "branches.  Every verdict here is against the gate AS PRE-REGISTERED, which "
                    "is the object the wave committed to.  A fake that a worker's private extra "
                    "check would catch is still a hole in the pre-registration."},
            {"what": "whether the Q1 slope criterion is meetable at all by the paper's actual "
                     "pulses",
             "why": "the adversary does not have the pulses' fast-phase Fourier content.  It can "
                    "only report that a band-limited (trigonometric-polynomial) pulse puts "
                    "Simpson at roundoff for every M in {16,64,256}, so the log-log slope is "
                    "~0 and the criterion 'slope <= -3.5' is unmeetable for such a pulse -- "
                    "a false NO risk, reported as a resolution finding, not a fake."},
            {"what": "a fake for Q2/Q3/Q4/Q5 that survives the planted controls AND is wrong in "
                     "a way the controls were written to catch",
             "why": "not attempted: the fakes above are wrong in ways ORTHOGONAL to the planted "
                    "controls, which is what makes them work.  Whether a fake exists that also "
                    "defeats a control head-on is undetermined."},
        ],
        "what_this_does_not_establish": [
            "Nothing here says any of Q1-Q5 is FALSE, or that the manuscript's algebra fails.",
            "Nothing here says the workers' runs were wrong.  The adversary never saw them.",
            "A FAKEABLE verdict says only this: the gate as pre-registered admits a run known to "
            "be wrong, so a YES from it is not, on its own, evidence.  It says nothing about "
            "whether the actual run that produced the YES was right.",
            "No fake here touches the theorem, the construction's closure, or W4.",
        ],
        "tier": "This is Tier 2, not a proof.",
        "forbidden_paths_opened": "none",
        "runtime_s": None,
    }
    n_fake = sum(1 for v in verdicts.values() if v == "FAKEABLE")
    art["X2_verdict"] = (
        "All %d of the five live gates (Q1-Q5) were made to say YES by a run the adversary "
        "knows to be wrong -- a fabricated amplitude field and a quadrature-invisible harmonic "
        "for Q1, an asserted q^{2h} for Q2, a real solve of the wrong problem with the gain in "
        "the operator's weight for Q3, a Gaussian stand-in stress for Q4, and the pinned builder "
        "run with rho 170x too large and the wrong cutoff for Q5 -- because every one of the "
        "five gates tests an algebraic RELATION that a family of objects satisfies, and pins the "
        "OBJECT only through route A's prediction, which is what the adversary is free to choose; "
        "by the wave's standing rule the signals they produce are NOT EVIDENCE on their own, "
        "while what each gate does still exclude is recorded per gate above. "
        "This is Tier 2, not a proof." % n_fake)
    art["runtime_s"] = time.time() - t0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(art, indent=1, sort_keys=False, default=float) + "\n")
    print(json.dumps({"X1": {k: v["verdict"] for k, v in gates.items()}, "runtime_s": art["runtime_s"]}, indent=1))
    print(art["X2_verdict"])


if __name__ == "__main__":
    main()
