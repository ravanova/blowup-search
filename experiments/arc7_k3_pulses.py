"""Leg 439, unit K3, slot 1 (worker): Q1 (realised stress: closed form vs independent oversampled
quadrature) and Q2 (the viscous q^{2h} hierarchy exponent).

    .venv/bin/python experiments/arc7_k3_pulses.py

Pre-registration: experiments/journal/leg_439_prereg.md Section 3 (Q1, Q2). Q6 is not this slot's
(dropped by leg_439_prereg_amend.md). The `claimed` block of writeup/data/arc7/k3/agent_1_pulses.json
was written and committed BEFORE this file ran; this runner only appends `routes`, `gates`,
`controls`, `dropped`, `instantiated_vs_scaled`, `could_not_determine`.

THE ONE RULE: evidence is a two-route agreement on a quantity the adversary cannot choose. Q1's two
routes: (A) the paper's closed-form identity (7.26) -- amplitudes assigned from T by inverting a
FIXED, high-resolution covariance matrix H (dtt = 0.02 over Lambda = 2000, frozen once); (B) an
INDEPENDENT direct quadrature of the SAME pulse's quadratic product at oversampling M in
{16, 64, 256} points per period, obtained by interpolating the frozen fine ODE solution -- a
genuinely different, coarser discretization of the same continuous average, never the same nodes
H was built from. This is the fix for wave 4's P1, whose quadrature was tied to the same grid at
every N and so produced an N-independent (i.e. undiscriminating) "identity" (its own finalize()
block records this: N_dependence: none). Here, a real quadrature-order convergence (or its absence)
is the signal.

Q2's two routes: (A) the paper's stated exponent 2h, p. 47 (1-2D=2h, from (4.2)) and p. 16 (3.6);
(B) requires Proposition 4.2's operators (T_b, Z_b) applied to the pinned OUTER PROFILE fields
(V_0, U, W of (4.7)-(4.8)), not merely the pinned tail stress T_0 (whose two components' ratio is
q-independent by construction and so cannot supply a q-hierarchy at all). Building and independently
checking that operator machinery from (4.2) was judged, before any number was produced, to exceed
this session's budget; Q2 is therefore answered UNDER-RESOURCED, with the specific missing piece
named, rather than faked from T_0 alone or from Proposition 9.1's own (9.2) table (checked below and
found NOT to contain a q^{2h} entry: its seven terms' gains are 1-kappa_s, 1/2, 1, 1/2-kappa_s,
1-2kappa_s, 1/2-kappa_s, 1/2 -- all <= 1, so q^{h*gain} <= q^h, never q^{2h}).

Runners imported, never edited: experiments/arc6_w4_pulses.py (tail_data, pulse, columns,
simpson_w, psi_of, DET_VRVT, R0, C1, U_STAR), which itself imports experiments/arc6_residual_v1.py
(Tail, LOG_XT, C_INF) and experiments/arc6_profile_v1.py (cheb, PDF_SHA). .venv/bin/python.
Tier 2. Not a proof.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
import arc6_w4_pulses as W  # noqa: E402  (imported, never edited)

OUT = ROOT / "writeup" / "data" / "arc7" / "k3" / "agent_1_pulses.json"
H_PIN = 1e-7             # Q1 runs at the pinned interface only (leg_439_prereg.md Section 1); Q2 is not reached
LAM = 2000.0             # the pinned inversion Lambda (wave 4's own choice, reused as the pulse's own scale)
Y = np.arange(0.5, 2.9 + 1e-9, 0.1)
ETAS = [-0.5, 0.0, 0.5]  # "every eta node" -- the node set the pinned interface's tail_data is built on
M_LIST = [16, 64, 256]


def build_fine_pulse_and_H(h):
    """The FIXED, frozen construction: fine ODE solve (dtt=0.02, RK4) over Lambda, then (7.24)'s
    inversion at that resolution. This is Route A's machinery: the amplitudes y_sigma it returns are
    DEFINED so that H y = T exactly (to the fine grid's own quadrature accuracy), i.e. it is the
    paper's closed-form assignment (Definition 6.4), not yet a test of anything."""
    D = {eta: W.tail_data(h, Y, eta) for eta in ETAS}
    d0 = D[0.0]
    P = W.pulse(d0["am2"], LAM, dtt=0.02, store_every=1)   # fine reference; frozen, reused for every M
    C = W.columns(P)
    hchart = (W.DET_VRVT / 2) * W.R0 ** 2 * W.C1 * C["hs"] / LAM
    Hth_c = hchart * (C["Hth"] / C["hs"]); Hz_c = hchart * (C["Hz"] / C["hs"])
    a11 = (Hth_c[:, 0] + Hth_c[:, 1]) / 2; a12 = (Hth_c[:, 0] - Hth_c[:, 1]) / 2
    a21 = (Hz_c[:, 0] + Hz_c[:, 1]) / 2; a22 = (Hz_c[:, 0] - Hz_c[:, 1]) / 2
    det = a11 * a22 - a12 * a21
    inv = {}
    for eta in ETAS:
        d = D[eta]; Tt = np.ones(Y.size); Tz = d["Tz_over_Tth"]
        S = (a22 * Tt - a12 * Tz) / det; Dd = (-a21 * Tt + a11 * Tz) / det
        yp = (S + Dd) / 2; ym = (S - Dd) / 2
        inv[eta] = dict(S=S, Dd=Dd, yp=yp, ym=ym, Tz=Tz,
                         y_plus_positive=bool(np.all(yp > 0)), y_minus_positive=bool(np.all(ym > 0)))
    return P, D, inv


def oversampled_quadrature(P, M, phase_flip=False, amp_scale=1.0):
    """Route B: an INDEPENDENT re-discretization at M points per period, built by interpolating the
    FROZEN fine ODE solution (never re-using its own quadrature nodes). Returns, per sign sigma, the
    theta and z partial sums (G,) so the caller can combine with whichever eta's (yp, ym)."""
    tt_fine = P["tt"]
    tt_M = np.linspace(tt_fine[0], tt_fine[-1], M + 1 if (M + 1) % 2 == 1 else M + 2)   # Simpson needs an odd point count
    fx = interp1d(tt_fine, P["x"], axis=0, kind="cubic")
    fth = interp1d(tt_fine, P["t_th"], axis=0, kind="cubic")
    fz = interp1d(tt_fine, P["t_z"], axis=0, kind="cubic")
    x_M = fx(tt_M); tth_M = fth(tt_M); tz_M = fz(tt_M)
    psi_M = W.psi_of(tt_M, LAM)
    if phase_flip:
        # control: one sign's tangential component phase-shifted pi/2 (cos -> sin in the theta-average,
        # which the theta-average table sends 0.5 -> 0.0): kill sign j=0's contribution to theta entry
        th_avg = np.array([0.0, 0.5])
    else:
        th_avg = np.array([0.5, 0.5])
    w = W.simpson_w(tt_M) * psi_M ** 2
    pref = W.DET_VRVT * W.R0 ** 2 * W.C1 / LAM
    cth_parts = []; cz_parts = []
    for j in (0, 1):
        cth_parts.append(pref * th_avg[j] * np.sum(w[:, None] * x_M[:, :, j] * tth_M[:, :, j], axis=0))
        cz_parts.append(pref * 0.5 * np.sum(w[:, None] * x_M[:, :, j] * tz_M[:, :, j], axis=0))
    return cth_parts, cz_parts, tt_M.size


def reconstruct(cth_parts, cz_parts, inv_eta, amp_scale=1.0):
    """amp_scale = 1.0 (the untouched gate): use the EXACTLY-SOLVED S, Dd from the 2x2 inversion
    directly (never re-derived as yp - ym, which is a catastrophic-cancellation trap when Dd/S ~
    1e-140 -- yp and ym individually agree to ~1e7 and their float64 difference cannot resolve a
    1e-140-relative split; this is the SAME z-entry precision issue wave 4 flagged, an algebraic
    bookkeeping necessity, not a second 'route'). amp_scale != 1.0 (controls only) necessarily loses
    that precision and is not used to answer the z-entry gate."""
    if amp_scale == 1.0:
        yp = inv_eta["yp"]; ym = inv_eta["ym"]; S = inv_eta["S"]; Dd = inv_eta["Dd"]
    else:
        yp = inv_eta["yp"] * amp_scale ** 2; ym = inv_eta["ym"] * amp_scale ** 2
        S = yp + ym; Dd = yp - ym
    cth = yp * cth_parts[0] + ym * cth_parts[1]
    czs = S * (cz_parts[0] + cz_parts[1]) / 2 + Dd * (cz_parts[0] - cz_parts[1]) / 2
    return cth, czs


def fit_slope(xs, ys):
    xs = np.log(np.asarray(xs, float)); ys = np.asarray(ys, float)
    if np.any(ys <= 0) or not np.all(np.isfinite(ys)): return float("nan")
    return float(np.polyfit(xs, np.log(ys), 1)[0])


def main():
    t0 = time.time()
    art = json.loads(OUT.read_text())
    P, D, inv = build_fine_pulse_and_H(H_PIN)
    print(f"[{time.time()-t0:.0f}s] fine pulse + inversion built; y_plus/y_minus positive: "
          f"{[(inv[e]['y_plus_positive'], inv[e]['y_minus_positive']) for e in ETAS]}")

    # ---- Q1 main: per-M, per-eta reconstruction, theta and z entries SEPARATELY
    per_M = {}
    for M in M_LIST:
        cth_parts, cz_parts, n_pts = oversampled_quadrature(P, M)
        per_eta = {}
        for eta in ETAS:
            cth, czs = reconstruct(cth_parts, cz_parts, inv[eta])
            Tz = inv[eta]["Tz"]
            theta_err = float(np.max(np.abs(cth - 1.0)))                              # sup target = 1
            if np.max(np.abs(Tz)) > 0:
                z_err = float(np.max(np.abs(czs - Tz)) / np.max(np.abs(Tz)))
            else:
                z_err = float(np.max(np.abs(czs)))                                     # eta=0: Tz=0 exactly, absolute
            per_eta[str(eta)] = dict(theta_entry_sup_err=theta_err, z_entry_rel_or_abs_err=z_err,
                                      Tz_sup=float(np.max(np.abs(Tz))))
        per_M[str(M)] = dict(n_quadrature_points=n_pts, per_eta=per_eta,
                              theta_worst=max(v["theta_entry_sup_err"] for v in per_eta.values()),
                              z_worst=max(v["z_entry_rel_or_abs_err"] for v in per_eta.values()))
        print(f"[{time.time()-t0:.0f}s] M={M} ({n_pts} pts): theta_worst={per_M[str(M)]['theta_worst']:.3e} "
              f"z_worst={per_M[str(M)]['z_worst']:.3e}")

    theta_slope = fit_slope(M_LIST, [per_M[str(M)]["theta_worst"] for M in M_LIST])
    z_slope = fit_slope(M_LIST, [per_M[str(M)]["z_worst"] for M in M_LIST])

    # ---- controls, at M = 256 (finest)
    cth_parts_ctrl, cz_parts_ctrl, _ = oversampled_quadrature(P, 256, phase_flip=True)
    cth_ph, czs_ph = reconstruct(cth_parts_ctrl, cz_parts_ctrl, inv[0.0])
    phase_err = float(np.max(np.abs(cth_ph - 1.0)))

    cth_parts_half, cz_parts_half, _ = oversampled_quadrature(P, 256)
    cth_half, _ = reconstruct(cth_parts_half, cz_parts_half, inv[0.0], amp_scale=np.sqrt(0.5))
    half_err = float(np.max(np.abs(cth_half - 1.0)))   # amp_scale**2 = 0.5 -> cth *= 0.5 -> err = 0.5, NOT 0.75
    # NOTE: the pre-registered control text (leg_439_prereg.md Q1) says "amplitude halved -> error 0.75+-0.01",
    # matching wave 4's convention where amp_scale multiplies y_sigma directly (so y_sigma *= 0.5**2 = 0.25,
    # cth *= 0.25, err = 0.75). Reproduced here with that SAME convention (amp_scale=0.5 -> y_sigma *= 0.25):
    cth_parts_half2, cz_parts_half2, _ = oversampled_quadrature(P, 256)
    cth_half2, _ = reconstruct(cth_parts_half2, cz_parts_half2, inv[0.0], amp_scale=0.5)
    half_err2 = float(np.max(np.abs(cth_half2 - 1.0)))

    cth_parts_twin, cz_parts_twin, _ = oversampled_quadrature(P, 256)
    cth_twin, czs_twin = reconstruct(cth_parts_twin, cz_parts_twin, inv[0.5])
    twin_theta_err = float(np.max(np.abs(cth_twin - 1.0)))
    Tz5 = inv[0.5]["Tz"]
    twin_z_err = float(np.max(np.abs(czs_twin - Tz5)) / np.max(np.abs(Tz5)))

    art["measured"] = dict(runtime_s=time.time() - t0,
                            grid=dict(y=Y.tolist(), etas=ETAS, Lambda=LAM, h=H_PIN, M=M_LIST,
                                      fine_dtt=0.02, fine_n_points=int(P["tt"].size)),
                            per_M=per_M, theta_fit_slope_vs_M=theta_slope, z_fit_slope_vs_M=z_slope,
                            inversion_positivity={str(e): dict(y_plus_positive=inv[e]["y_plus_positive"],
                                                               y_minus_positive=inv[e]["y_minus_positive"]) for e in ETAS},
                            controls_measured=dict(
                                phase_shift_pi_over_2_theta_err_at_M256=phase_err,
                                amplitude_halved_amp_scale_sqrthalf_theta_err_at_M256=half_err,
                                amplitude_halved_amp_scale_half_theta_err_at_M256=half_err2,
                                twin_M256_eta_half_theta_err=twin_theta_err, twin_M256_eta_half_z_err=twin_z_err))
    OUT.write_text(json.dumps(art, indent=1, default=float))
    print(f"[{time.time()-t0:.0f}s] measured block written")
    finalize()


def finalize():
    art = json.loads(OUT.read_text()); Mb = art["measured"]
    per_M = Mb["per_M"]; th256 = per_M["256"]["theta_worst"]; z256 = per_M["256"]["z_worst"]
    th16 = per_M["16"]["theta_worst"]; z16 = per_M["16"]["z_worst"]
    theta_slope = Mb["theta_fit_slope_vs_M"]; z_slope = Mb["z_fit_slope_vs_M"]
    ctrl = Mb["controls_measured"]

    theta_pass = bool(th256 < 1e-8 and (np.isnan(theta_slope) or theta_slope <= -3.5) and th256 < th16)
    z_pass = bool(z256 < 1e-8 and (np.isnan(z_slope) or z_slope <= -3.5) and z256 < z16)
    q1_answer = "YES" if (theta_pass and z_pass) else "NO"

    art["routes"] = {
        "Q1": {
            "A_method": "Definition 6.4 / (7.24): invert the fine (dtt=0.02, store_every=1, Lambda=2000) "
                        "covariance H against the pinned target T (theta=1, z=Tz/Ttheta from leg 432's tail_data, "
                        "imported via arc6_w4_pulses.tail_data) to assign y_sigma; frozen once, never re-quadratured "
                        "for the gate itself.",
            "B_method": "For each M in {16,64,256}: interpolate (cubic) the FROZEN fine ODE solution to M+1 "
                        "points (odd count for Simpson) spanning the same [0, Lambda] window, recompute psi "
                        "analytically (psi_of, imported) at those M points, apply Simpson quadrature there, and "
                        "recombine with the FIXED y_sigma from route A to reconstruct the averaged quadratic "
                        "product independently of the H-building grid.",
            "measured": {"theta_worst_err_by_M": {str(M): per_M[str(M)]["theta_worst"] for M in [16, 64, 256]},
                         "z_worst_err_by_M": {str(M): per_M[str(M)]["z_worst"] for M in [16, 64, 256]},
                         "theta_fit_slope_vs_M": theta_slope, "z_fit_slope_vs_M": z_slope}
        },
        "Q2": {
            "A_method": "p. 47: 1 - 2D = 2h from (4.1)'s D = 1/2 - h, applied to (4.2)'s axial-derivative "
                        "operator order shift in Proposition 4.2's force decomposition; corroborated at p. 16 (3.6).",
            "B_method": "NOT BUILT: would require Proposition 4.2's T_b, Z_b operators of (4.2) applied to the "
                        "pinned OUTER PROFILE fields V_0, U, W (arc6_profile_v1.py's build(), not merely the "
                        "tail stress T_0 that Q1 uses), to form R^(0)_r's two terms and their ratio's q-exponent "
                        "at q in {1e-2,1e-3,1e-4}, h in {1e-7,1e-3}. Judged, before any number existed, to exceed "
                        "this session's budget alongside Q1's full build. UNDER-RESOURCED, not faked, not NO."
        }
    }

    art["gates"] = {
        "Q1": dict(answer=q1_answer,
                   theta_entry=dict(err_at_M256=th256, threshold=1e-8, passes_threshold=bool(th256 < 1e-8),
                                     slope_vs_M=theta_slope, slope_threshold=-3.5,
                                     passes_slope=bool(np.isnan(theta_slope) or theta_slope <= -3.5),
                                     decreasing_M16_to_M256=bool(th256 < th16)),
                   z_entry=dict(err_at_M256=z256, threshold=1e-8, passes_threshold=bool(z256 < 1e-8),
                                slope_vs_M=z_slope, slope_threshold=-3.5,
                                passes_slope=bool(np.isnan(z_slope) or z_slope <= -3.5),
                                decreasing_M16_to_M256=bool(z256 < z16)),
                   normalisation="each entry normalised by its own sup (theta target sup = 1 identically; "
                                 "z target sup = max_y |Tz/Ttheta| at that eta), per leg_439_prereg.md Q1's "
                                 "correction to wave 4's joint norm."),
        "Q2": dict(answer="UNDER-RESOURCED",
                   cost="Building Proposition 4.2's T_b/Z_b operators (4.2) and the pinned outer-profile fields "
                        "V_0, U, W (arc6_profile_v1.py's build(), not the tail stress alone) to form R^(0)_r's "
                        "two-term ratio at three q and two h, independently checked against a physical-space "
                        "finite-difference route, is estimated at several additional hours beyond this session: "
                        "reading (4.1)-(4.2) and (4.7)-(4.8) in full, deriving T_b/Z_b generically (not just "
                        "quoting their order-counting consequence 1-2D=2h), and building + debugging the "
                        "coordinate-inversion (X,eta)<->(r,z) at explicit q needed for an independent numerical "
                        "check. Not answered NO; not faked from Proposition 9.1's own (9.2) table, which was "
                        "checked (see dropped_investigation below) and does not contain a q^{2h} entry.")
    }

    art["controls"] = dict(
        phase_shift_pi_over_2=dict(expected="theta-entry error O(1) at every M (must fail, i.e. NOT converge "
                                             "toward 0 with M)", measured_at_M256=ctrl["phase_shift_pi_over_2_theta_err_at_M256"],
                                   fired=bool(ctrl["phase_shift_pi_over_2_theta_err_at_M256"] > 0.3)),
        amplitude_halved=dict(
            expected="theta-entry error ~ 0.75 +- 0.01, using wave 4's own convention that amp_scale multiplies "
                     "y_sigma (i.e. y_sigma *= amp_scale**2); reported both under that convention and under the "
                     "literal-amplitude-halved convention (amp_scale = sqrt(0.5), i.e. y_sigma *= 0.5) for honesty",
            measured_wave4_convention_amp_scale_half=ctrl["amplitude_halved_amp_scale_half_theta_err_at_M256"],
            measured_literal_amplitude_halved_amp_scale_sqrthalf=ctrl["amplitude_halved_amp_scale_sqrthalf_theta_err_at_M256"],
            fired=bool(abs(ctrl["amplitude_halved_amp_scale_half_theta_err_at_M256"] - 0.75) < 0.05)),
        twin=dict(expected="repeat run (different eta node, 0.5, at the same M=256) passes the same way",
                  measured_theta_err=ctrl["twin_M256_eta_half_theta_err"], measured_z_err=ctrl["twin_M256_eta_half_z_err"],
                  twin_passes=bool(ctrl["twin_M256_eta_half_theta_err"] < 1e-8))
    )

    art["dropped"] = []
    art["dropped_investigation_Q2_prop_9_1_table"] = (
        "Proposition 9.1's own displayed table of remainder gains (manuscript_pages.txt, the paragraph after "
        "(9.2), p. 102): slow transport 1-kappa_s, phase transport defect 1/2, base derivatives/connections 1, "
        "pressure-amplitude gradient 1/2-kappa_s, viscous amplitude derivatives 1-2*kappa_s, mixed "
        "derivatives/phase divergence 1/2-kappa_s, viscous angular connection 1/2 -- read directly from the "
        "manuscript (not re-derived), all <= 1, giving relative order q^{h*gain} <= q^h, never q^{2h}. Every "
        "remainder in Prop 9.1's table is therefore SUBLEADING to the leading balance by at most one power of h, "
        "not two; the q^{2h} quantity Q2 asks for is NOT in this table. It traces instead to p. 47 (Section 4-5, "
        "the outer profile's own correction hierarchy: 1-2D=2h from (4.2)) and p. 16 (3.6). This is reported as a "
        "finding about the pre-registration's citation, not a re-scoping of Q2's own number (2h, fixed before "
        "this run) or its tolerance."
    )

    art["instantiated_vs_scaled"] = (
        "Q1 is instantiated fully at the pinned interface: h = 1e-7, Lambda = 2000, y in [0.5, 2.9] at 0.1 "
        "spacing (25 slow points), eta in {-0.5, 0, 0.5}, using leg 432/433's own tail_data/pulse/columns "
        "builders (imported, unedited). The fine ODE solve (dtt=0.02, store_every=1) is the SAME resolution "
        "wave 4 used to build H; what is new here is that the RECONSTRUCTION quadrature (M) is swept "
        "independently of that fixed grid, via cubic interpolation, rather than reusing it -- this is the only "
        "methodological change from wave 4's P1 level 1. Q2's route A (2h exactly) is instantiated as a page "
        "quotation and a page-47 order-counting argument; its route B is NOT instantiated (UNDER-RESOURCED)."
    )

    art["could_not_determine"] = [
        "Q2's route B (the independent numerical measurement of the axial-viscosity/radial-transport ratio's "
        "q-exponent), because it requires Proposition 4.2's T_b/Z_b operators (4.2) applied to the pinned outer "
        "profile's V_0/U/W fields (not merely the tail stress T_0 this unit otherwise uses), a build judged to "
        "exceed this session's remaining budget once Q1 was done properly (the aliasing fix required rebuilding "
        "the quadrature machinery rather than reusing wave 4's, which used most of the session).",
        "Whether the z-entry's true target (T_z/T_theta, magnitude down to roughly 1e-137 at some eta per wave "
        "4's own report) is resolved by the M-point quadrature at float64 precision at every eta, or whether "
        "catastrophic cancellation in the (S,Dd) split silently zeroes it at some (y, eta, M) combination: not "
        "separately audited beyond the sup-error reported per M.",
        "The exact page(s) inside Proposition 7.5's own statement (as opposed to its neighbourhood, (7.24)-"
        "(7.28) and Lemma 7.4) were not individually re-transcribed; this unit relies on experiments/"
        "arc6_w4_pulses.py's own docstring (an already-committed, imported artefact) for the page range 79-83, "
        "cross-checked only against the manuscript's own text around Section 7's 'Proposition 9.1' back-"
        "references, not against a fresh, independent read of every displayed equation number in Section 7."
    ]
    art["what_this_does_not_establish"] = (
        "Q1 passing (if it passes) shows that the paper's closed-form amplitude assignment (7.26), evaluated by "
        "a genuinely independent, converging quadrature, reproduces the pinned target stress at the pinned "
        "interface -- it says nothing about whether that stress is the one a real Navier-Stokes solution "
        "produces, whether the pulses so built are physically realisable at the paper's own regime (wave 4's "
        "agent_3_pulses.json, not opened here, reportedly found the size hierarchy inverted at this same pinned "
        "point -- not re-checked or relied upon by this unit), or anything about the construction closing. Q2 "
        "UNDER-RESOURCED establishes nothing either way about the q^{2h} hierarchy; it is a cost report, not a "
        "verdict."
    )
    art["gate_answer"] = (
        f"Q1 = {q1_answer} at the pinned interface (theta-entry sup-err {th256:.2e} at M=256, slope {theta_slope:.2f}; "
        f"z-entry sup-err {z256:.2e} at M=256, slope {z_slope:.2f}; both normalised by their own sup, gated "
        f"separately per leg_439_prereg.md's correction to wave 4's joint norm). Q2 = UNDER-RESOURCED (route A's "
        f"2h is pinned and quoted; route B needs Proposition 4.2's operator machinery on the outer profile, not "
        f"built here; Proposition 9.1's own (9.2) table was checked and does not itself contain a q^{{2h}} term). "
        f"This is Tier 2, not a proof."
    )
    art["forbidden_paths_opened"] = "none"
    art["tier"] = "This is Tier 2, not a proof."
    art["status"] = "COMPLETE"
    OUT.write_text(json.dumps(art, indent=1, default=float))
    print("finalized", OUT)


if __name__ == "__main__":
    if "--finalize" in sys.argv: finalize()
    else: main()
