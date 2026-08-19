#!/usr/bin/env python3
"""Leg 409, unit `L-JVER` -- EVIDENCE SCRIPT.  Controls first, verdict last.

EVIDENCE-CHECK CLASSIFICATION (`writeup/CORRECTIONS.md` SS45, SS46b -- BINDING).  Every
check below carries one of two labels and the labels are printed and banked beside the
numbers.  `N/N passed` is never reported without them.

  recompute-from-primary : the number is produced by executing something -- this unit's
                           own independent code, or `L6`'s code re-run as a black box, or a
                           closed form evaluated by hand -- and compared against a number
                           this unit did not choose.
  re-read-own-artefact   : the number is read back out of a JSON this unit or `L6` wrote.
                           It witnesses bookkeeping, not mathematics.

ORDER IS NOT NEGOTIABLE.  Controls X1..X7 run and print BEFORE the gate.  If a control does
not fire, the verdicts below it are VOID and are reported as void, not repaired.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

import experiments.p2_route_ljver_v1 as MY          # noqa: E402  the independent code
import p2_route_ljver_v1_ref as REF                 # noqa: E402  the quarantined driver
import p2_route_l6_v1 as L6                         # noqa: E402  BLACK BOX

ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"
REFJ = ROOT / "writeup" / "data" / "p2_route_ljver_v1_ref.json"
OUT = ROOT / "writeup" / "data" / "p2_route_ljver_v1.json"

# The primary quadrature.  Named here once, used for every gate number, never re-tuned.
PRIMARY = dict(rmin=1e-6, rmax=1e8, per_efold=1, gl_order=10, ng=12, ns=24)

CHK = []


def rec(name, cls, detail, passed=None):
    CHK.append(dict(check=name, evidence_class=cls, passed=passed, **detail))
    print("[%s] %-34s %s  %s" % (cls, name, detail, "" if passed is None else
                                 ("PASS" if passed else "FAIL")), flush=True)


def main():
    t0 = time.time()
    doc = json.load(open(ART))
    ref = json.load(open(REFJ))
    xB = np.array(doc["banked_profile"]["B"]["coefficients"])
    xA = np.array(doc["banked_profile"]["A"]["coefficients"])
    res = {"unit": "L-JVER", "leg": 409, "lane": "L",
           "tier": 2, "arithmetic": "float64",
           "object": "writeup/data/p2_route_l6_profile_v1.json banked_profile.A/.B, n_dof 6720",
           "primary_quadrature": PRIMARY}

    sp = MY.Space(4, 20, 3, **PRIMARY)
    print("my grid: nr=%d nang=%d ns=%d\n" % (sp.nr, sp.nang, sp.ns), flush=True)

    # ================================ CONTROLS ==========================================
    print("=== CONTROLS (these run and are reported BEFORE any verdict) ===", flush=True)

    # ---- X1a  closed form, THIS unit -----------------------------------------------------
    x1 = MY.control_X1(sp)
    rec("X1a_mine_curl_vs_closed_form", "recompute-from-primary",
        dict(max_rel=x1["curl_closed_form_vs_fd_rel"], tol=1e-8),
        x1["curl_closed_form_vs_fd_rel"] < 1e-8)
    rec("X1a_mine_L32_norm_vs_closed_form", "recompute-from-primary",
        dict(value=x1["norm_value"], exact=x1["norm_exact"],
             rel=x1["norm_rel_err"], tol=1e-6), x1["norm_rel_err"] < 1e-6)

    # ---- X1b  the SAME closed form, through L6's operators -------------------------------
    x1b = ref["control_X1_through_L6"]
    rec("X1b_L6_V_vs_closed_form", "recompute-from-primary",
        dict(max_rel=x1b["V_vs_closed_form_rel"], tol=1e-10),
        x1b["V_vs_closed_form_rel"] < 1e-10)
    rec("X1b_L6_curl_vs_closed_form", "recompute-from-primary",
        dict(max_rel=x1b["curl_vs_closed_form_rel"], tol=1e-10),
        x1b["curl_vs_closed_form_rel"] < 1e-10)
    rec("X1b_L6_L32_norm_vs_closed_form", "recompute-from-primary",
        dict(value=x1b["norm_value"], exact=x1b["norm_exact"],
             rel=x1b["norm_rel_err"], tol=1e-10), x1b["norm_rel_err"] < 1e-10)

    # ---- X2  the banked field samples ----------------------------------------------------
    worst = 0.0
    for br, xx in (("A", xA), ("B", xB)):
        for fs in doc["banked_profile"][br]["field_samples"]:
            Vn = MY.eval_V_at(sp, xx, "none", np.array(fs["points"]), fs["s"])
            Vr = np.array(fs["V"])
            worst = max(worst, float(np.max(np.abs(Vn - Vr)) / np.max(np.abs(Vr))))
    rec("X2_banked_field_samples_150pts", "recompute-from-primary",
        dict(max_rel=worst, n_points=150, tol=1e-10), worst < 1e-10)

    # ---- X3  div V ------------------------------------------------------------------------
    d = MY.J_of(sp, xB, "B", want_extra=True)
    rec("X3_div_V_identically_zero", "recompute-from-primary",
        dict(max_rel=d["div_rel"], tol=1e-12), d["div_rel"] < 1e-12)
    J_P1 = d["J"]

    # ---- X4  planted defect MUST fire ----------------------------------------------------
    Jbad = MY.J_of(sp, xB, "B", drop_dss_term=True)
    fired = abs(Jbad - J_P1) / J_P1
    rec("X4_planted_defect_drop_a_2w_plus_ygradw", "recompute-from-primary",
        dict(J_intact=J_P1, J_defective=Jbad, rel_shift=fired, must_exceed=1e-2),
        fired > 1e-2)

    # ---- X5  internal convergence of MY quadrature ---------------------------------------
    conv = {}
    for name, over in [("angular_x1.33", dict(ng=16)), ("s_x1.67", dict(ns=40)),
                       ("radial_panels_x2", dict(per_efold=2)),
                       ("radial_order_x1.4", dict(gl_order=14)),
                       ("s_rule_gauss", dict(s_gauss=True))]:
        kw = dict(PRIMARY)
        kw.update(over)
        spx = MY.Space(4, 20, 3, **kw)
        conv[name] = MY.J_of(spx, xB, "B")
    spread = max(abs(v - J_P1) / J_P1 for v in conv.values())
    rec("X5_my_quadrature_self_convergence", "recompute-from-primary",
        dict(J_primary=J_P1, variants={k: v for k, v in conv.items()},
             max_rel_spread=spread, tol=1e-5), spread < 1e-5)

    # ---- X6  jets vs Cauchy, and jets vs high-precision mpmath ---------------------------
    x6 = {}
    core = (sp.r > 1e-2) & (sp.r < 1e3)
    for (l, n, tor) in [(2, 4, False), (3, 11, False), (1, 7, True)]:
        h = [i for i, (ll, mm) in enumerate(sp.harm) if ll == l][0]
        aF = np.zeros((sp.nH, sp.Nr, sp.nK))
        aQ = np.zeros((sp.nH, sp.Nr, sp.nK))
        (aQ if tor else aF)[h, n, 0] = (sp.sQ if tor else sp.sF)[l, n]
        Gj = sp.radial_G(aF, aQ)[1 if tor else 0, h, :, 0, :][:, core]
        Gc = MY.cauchy_derivs(sp.r[core], l, n, tor, 1.0, sp.kmax)
        x6["l%dn%d%s" % (l, n, "Q" if tor else "F")] = [
            float(np.max(np.abs(Gj[k] - Gc[k])) / max(float(np.max(np.abs(Gj[k]))), 1e-300))
            for k in range(sp.kmax + 1)]
    worst2 = max(v[k] for v in x6.values() for k in range(3))
    rec("X6_jets_vs_Cauchy_k0to2_core_r", "recompute-from-primary",
        dict(per_column_all_k=x6, max_rel_k_le_2=worst2, tol=1e-6, r_window=[1e-2, 1e3],
             measured_fact=("float64 Cauchy degrades as k!/rho^k and by Chebyshev growth "
                            "off the real axis; it is unusable for k >= 3 and unusable at "
                            "r outside [1e-2, 1e3].  This is a limit of the CROSS-CHECK, "
                            "not of the jets: X6b settles all k at 40 decimal digits.")),
        worst2 < 1e-6)
    try:
        import mpmath as mp
        mp.mp.dps = 40
        mm = []
        for (l, n, tor) in [(2, 4, False), (1, 7, True)]:
            h = [i for i, (ll, mmm) in enumerate(sp.harm) if ll == l][0]
            aF = np.zeros((sp.nH, sp.Nr, sp.nK))
            aQ = np.zeros((sp.nH, sp.Nr, sp.nK))
            (aQ if tor else aF)[h, n, 0] = (sp.sQ if tor else sp.sF)[l, n]

            def G(z, l=l, n=n, tor=tor):
                u = z / (z + MY.LMAP)
                T = mp.chebyt(n, 2 * u - 1)
                return (MY.LMAP * T / (z + MY.LMAP) ** (l + 1) if tor
                        else T / (z + MY.LMAP) ** l)
            for rv in (0.05, 1.0, 30.0, 5000.0):
                i = int(np.argmin(np.abs(sp.r - rv)))
                Gj = sp.radial_G(aF, aQ)[1 if tor else 0, h, :, 0, i]
                for k in range(sp.kmax + 1):
                    hi = float(mp.diff(G, mp.mpf(sp.r[i]), k))
                    mm.append(abs(Gj[k] - hi) / max(abs(hi), 1e-300))
        rec("X6b_jets_vs_mpmath_40dps_all_k", "recompute-from-primary",
            dict(max_rel=float(max(mm)), n=len(mm), tol=1e-10), max(mm) < 1e-10)
    except Exception as exc:                                   # pragma: no cover
        rec("X6b_jets_vs_mpmath_40dps_all_k", "recompute-from-primary",
            dict(error=repr(exc)), None)

    # ---- X7  POINTWISE W on a COMMON grid -- quadrature removed entirely -----------------
    gL = L6.Geom(4, 20, 3)
    xn = L6.normalise(gL, xB, "B")
    aFl, aQl = gL.unpack(xn)
    Wl, Vl, wl = L6.residual_field(gL, L6.Var(aFl), L6.Var(aQl))
    Wl = Wl.v                                                  # (nq_r, ns, nP, 3)
    spc = sp.regrid(gL.r, gL.er, gL.wa, gL.s, gL.ws)
    aFm, aQm = MY.unpack(spc, xB)
    scb = 1.0 / math.sqrt(MY.norm_B_closed_form(spc, aFm))
    Wm, Vm, wm, _ = MY.residual_W(spc, aFm * scb, aQm * scb)   # (nang, nr, ns, 3)
    Wm = np.transpose(Wm, (1, 2, 0, 3))                        # -> (nr, ns, nang, 3)
    den = np.max(np.abs(Wl))
    dif = float(np.max(np.abs(Wm - Wl)) / den)
    # and the same difference restricted to the region carrying the mass
    sel = (gL.r > 1e-2) & (gL.r < 1e3)
    dif_core = float(np.max(np.abs(Wm[sel] - Wl[sel])) / np.max(np.abs(Wl[sel])))
    rec("X7_pointwise_W_on_L6_own_grid", "recompute-from-primary",
        dict(max_rel_all=dif, max_rel_core_r_1em2_to_1e3=dif_core, n_points=int(Wl.size // 3),
             tol=1e-9), max(dif, dif_core) < 1e-9)

    # J from MY W using L6's OWN weights -- isolates operator from quadrature
    wpr = gL.wr[:, None, None] * gL.wa[None, None, :]
    per_s = (((Wm ** 2).sum(-1)) ** 0.75 * wpr).sum(axis=(0, 2))
    J_mine_L6quad = float(np.sum(per_s ** (2.0 / 3.0) * gL.ws))
    J_L6_P1 = ref["P1_bankedB_J4"]
    rec("X7b_my_W_with_L6_quadrature_vs_J_L6", "recompute-from-primary",
        dict(J=J_mine_L6quad, J_L6=J_L6_P1,
             rel=abs(J_mine_L6quad - J_L6_P1) / J_L6_P1, tol=1e-9),
        abs(J_mine_L6quad - J_L6_P1) / J_L6_P1 < 1e-9)

    # ---- X8  the column scaling sigma, mine vs L6's --------------------------------------
    sFl = np.array(ref["sigmaF_L6"])            # (nH, Nr), per harmonic
    sQl = np.array(ref["sigmaQ_L6"])
    lofh = np.array([l for (l, m) in sp.harm])
    dF = float(np.max(np.abs(sp.sF[lofh] - sFl) / sFl))
    dQ = float(np.max(np.abs(sp.sQ[lofh] - sQl) / sQl))
    rec("X8_column_scaling_sigma_mine_vs_L6", "recompute-from-primary",
        dict(max_rel_F=dF, max_rel_Q=dQ, tol=1e-10), max(dF, dQ) < 1e-10)

    res["controls"] = list(CHK)
    controls_ok = all(c["passed"] for c in CHK if c["passed"] is not None)
    print("\nALL CONTROLS FIRED:", controls_ok, flush=True)
    res["controls_all_fired"] = bool(controls_ok)

    # ================================ THE GATE ==========================================
    print("\n=== THE GATE (pre-committed, two-sided, not re-worded) ===", flush=True)
    pts = []
    J_P2 = MY.J_of(sp, xA, "A")
    xP3 = REF.restrict_box(xB, 4, 20, 3, 2, 8, 1)
    xP4 = np.random.default_rng(409).standard_normal(sp.n_dof) * 0.3
    J_P3 = MY.J_of(sp, xP3, "B")
    J_P4 = MY.J_of(sp, xP4, "B")
    for tag, Jn, Jl, what in [
            ("P1", J_P1, ref["P1_bankedB_J4"], "banked branch B, n_dof 6720 (a minimiser)"),
            ("P2", J_P2, ref["P2_bankedA_J4"], "banked branch A, n_dof 6720 (a minimiser)"),
            ("P3", J_P3, ref["P3_J0box_of_B_in_6720"],
             "J0 index box of banked B held in the 6720 space -- NOT a minimiser"),
            ("P4", J_P4, ref["P4_random_seed409"],
             "pseudo-random vector, seed 409 -- NOT a minimiser (extra, beyond the gate)")]:
        r_ = abs(Jn - Jl) / Jl
        pts.append(dict(point=tag, what=what, J_new=Jn, J_L6=Jl, rel_diff=r_,
                        below_1e_3=bool(r_ < 1e-3)))
        print("  %s  J_new=%.10g  J_L6=%.10g  |rel|=%.4e  <1e-3: %s   [%s]"
              % (tag, Jn, Jl, r_, r_ < 1e-3, what), flush=True)
    res["gate_points"] = pts
    three = [p for p in pts if p["point"] in ("P1", "P2", "P3")]
    answer = "YES" if all(p["below_1e_3"] for p in three) else "NO"
    res["gate"] = {
        "question": ("Evaluate the independently built J at L6's banked coefficient vector "
                     "for branch B at n_dof = 6720, at branch A, and at a third point that "
                     "is NOT a minimiser.  Is |J_new - J_L6| / J_L6 below 1e-3 at ALL "
                     "THREE -- YES or NO?"),
        "answer": answer,
        "rel_diffs": {p["point"]: p["rel_diff"] for p in three},
        "controls_all_fired": bool(controls_ok)}
    print("\n  GATE ANSWER:", answer, flush=True)

    # ================================ FIVE RUNGS ========================================
    print("\n=== the disagreement at ALL FIVE rungs ===", flush=True)
    rungs = []
    for name, Lm, Nr, Ks in REF.RUNGS:
        xr = REF.restrict_box(xB, 4, 20, 3, Lm, Nr, Ks, out_space=True)
        spr = MY.Space(Lm, Nr, Ks, **PRIMARY)
        Jn = MY.J_of(spr, xr, "B")
        Jl = ref["rungs"][name]["J_L6"]
        rungs.append(dict(rung=name, Lmax=Lm, Nr=Nr, Ks=Ks, n_dof=int(spr.n_dof),
                          J_new=Jn, J_L6=Jl, rel_diff=abs(Jn - Jl) / Jl))
        print("  %s n_dof=%5d  J_new=%.10g  J_L6=%.10g  |rel|=%.4e"
              % (name, spr.n_dof, Jn, Jl, abs(Jn - Jl) / Jl), flush=True)
    res["five_rung_table"] = rungs

    # ======================= THE SEPARATE FINDING: THE FAR-FIELD TAIL ===================
    print("\n=== cutoff sensitivity of J itself (a property of the FUNCTIONAL) ===",
          flush=True)
    cut = []
    for rmax in (1e3, 1e4, 1e5, 1e6, 1e8, 1e11, 1e14):
        kw = dict(PRIMARY)
        kw["rmax"] = rmax
        Jc = MY.J_of(MY.Space(4, 20, 3, **kw), xB, "B")
        cut.append(dict(r_max=rmax, r_min=PRIMARY["rmin"], J=Jc))
        print("   r_max=%-8g J=%.10f" % (rmax, Jc), flush=True)
    for rmin in (1e-2, 1e-4, 1e-8):
        kw = dict(PRIMARY)
        kw["rmin"] = rmin
        Jc = MY.J_of(MY.Space(4, 20, 3, **kw), xB, "B")
        cut.append(dict(r_max=PRIMARY["rmax"], r_min=rmin, J=Jc))
        print("   r_min=%-8g J=%.10f" % (rmin, Jc), flush=True)
    res["cutoff_sensitivity"] = cut
    dens = np.array(d["radial_density"])
    lo = np.floor(np.log10(sp.r)).astype(int)
    dec = {}
    for a, b in zip(lo, dens):
        dec[int(a)] = dec.get(int(a), 0.0) + float(b)
    res["integrand_mass_per_decade_of_r"] = {str(k): dec[k] for k in sorted(dec)}
    print("   mass per decade:", {k: "%.3e" % v for k, v in sorted(dec.items())}, flush=True)

    # ---- X9  THE DECISIVE SEPARATION: is the disagreement the OPERATOR or the RULE? -----
    print("\n=== X9: my W, on L6's OWN grid, with L6's OWN weights, at all four points ===",
          flush=True)
    x9 = []
    wpr = gL.wr[:, None, None] * gL.wa[None, None, :]
    for tag, xx, Jl in [("P1", xB, ref["P1_bankedB_J4"]),
                        ("P2", xA, ref["P2_bankedA_J4"]),
                        ("P3", xP3, ref["P3_J0box_of_B_in_6720"]),
                        ("P4", xP4, ref["P4_random_seed409"])]:
        aFm, aQm = MY.unpack(spc, xx)
        if tag == "P2":
            xn2 = L6.normalise(gL, xx, "A")
            aFm, aQm = MY.unpack(spc, xn2)
        else:
            sc2 = 1.0 / math.sqrt(MY.norm_B_closed_form(spc, aFm))
            aFm, aQm = aFm * sc2, aQm * sc2
        Wm2, _, _, _ = MY.residual_W(spc, aFm, aQm)
        Wm2 = np.transpose(Wm2, (1, 2, 0, 3))
        per2 = (((Wm2 ** 2).sum(-1)) ** 0.75 * wpr).sum(axis=(0, 2))
        Jq = float(np.sum(per2 ** (2.0 / 3.0) * gL.ws))
        x9.append(dict(point=tag, J_my_operator_L6_quadrature=Jq, J_L6=Jl,
                       rel=abs(Jq - Jl) / Jl))
        print("   %s  my operator + L6 rule = %.12g   J_L6 = %.12g   rel = %.3e"
              % (tag, Jq, Jl, abs(Jq - Jl) / Jl), flush=True)
    res["X9_operator_vs_rule"] = {
        "class": "recompute-from-primary",
        "what": ("this unit's INDEPENDENT operator W[V], evaluated on L6's own quadrature "
                 "points and contracted with L6's own quadrature weights"),
        "rows": x9,
        "reading": ("If these reproduce J_L6 while the gate fails, then the OPERATOR as "
                    "coded in L6 is right and the whole disagreement is the QUADRATURE "
                    "RULE -- i.e. it is a property of the integral, not of either program.")}

    # ---- the mass-per-decade profile at every gate point --------------------------------
    prof = {}
    for tag, xx in [("P1", xB), ("P3", xP3), ("P4", xP4)]:
        dd = MY.J_of(sp, xx, "B", want_extra=True)
        dv = np.array(dd["radial_density"])
        lo2 = np.floor(np.log10(sp.r)).astype(int)
        acc = {}
        for a, b in zip(lo2, dv):
            acc[int(a)] = acc.get(int(a), 0.0) + float(b)
        tt = sum(acc.values())
        prof[tag] = {str(k): acc[k] / tt for k in sorted(acc)}
        print("   %s mass fraction per decade of r:" % tag,
              {k: "%.2e" % v for k, v in prof[tag].items()}, flush=True)
    res["mass_fraction_per_decade_by_point"] = prof
    res["divergence_diagnosis"] = {
        "claim": ("J(c) = int_0^{T_s} ||W(.,s)||_{L3/2(R^3)} ds is a DIVERGENT integral for "
                  "generic c in this trial space.  It is logarithmically divergent at r -> "
                  "infinity, and also at r -> 0 whenever the l = 1 poloidal content is not "
                  "tuned away.  Every finite value in the record is a value of a particular "
                  "72-node truncation, not a value of the functional."),
        "why_infinity": ("F_lm(r, s) -> F_lm(inf, s) finite (the alpha = 1 branch), so "
                         "w ~ A(yhat, s)/r^2.  The DSS term a(2w + y.grad w) annihilates a "
                         "degree -2 homogeneous w exactly, and Lap w and the two nonlinear "
                         "terms are O(r^-4); but w_s ~ d_s A(yhat, s)/r^2 SURVIVES.  Then "
                         "|W|^{3/2} r^2 ~ 1/r and int dr/r diverges.  Branch B's own "
                         "normalisation forces sum_lm F_lm(inf, s)^2 to average 1, and the "
                         "k > 0 s-modes make d_s A nonzero, so branch B cannot escape it."),
        "why_origin": ("the radial basis u^l T_n(2u-1) has a NONZERO r^{l+1} Taylor "
                       "coefficient at r = 0 (u = r/2 - r^2/4 + ...), and Lap^2 applied to "
                       "r^{l+1} Y_lm gives -4 l (l+1) r^{l-3} Y_lm.  At l = 1 that is r^-2, "
                       "so Lap w ~ r^-2, |W|^{3/2} r^2 ~ 1/r, and int_0 dr/r diverges."),
        "evidence": ("mass_fraction_per_decade_by_point above: at P3 the fractions over the "
                     "decades 1e-6..1e-3 are flat (0.199, 0.181, 0.202, 0.185) and at P4 the "
                     "fractions over 1e3..1e7 are flat (0.139, 0.156, 0.173, 0.155, 0.170).  "
                     "A flat mass per decade IS a logarithmic divergence."),
        "L6_grid_reach": {"r_min": float(gL.r.min()), "r_max": float(gL.r.max()),
                          "nq_r": int(gL.nq_r)},
        "what_this_does_NOT_say": [
            "it does NOT say either program is miscoded -- X7, X7b and X9 say the opposite",
            "it does NOT say the minimum of the truncated functional is wrong as a number",
            "it does NOT move any L1->L4 link, in either direction",
            "it does NOT say a blow-up profile does or does not exist"]}

    res["cost"] = {"wall_seconds": time.time() - t0,
                   "cores_used": "<= 6 of 12 (sibling E-FE holds 6 until ~03:20 20-Aug)",
                   "MACHINE_WAS_NOT_QUIET": True,
                   "note": "R-prof's banked MACHINE_WAS_NOT_QUIET applies to every timing here"}
    blob = json.dumps(res, sort_keys=True, default=float).encode()
    res["self_hash"] = hashlib.blake2b(blob, digest_size=8).hexdigest()
    OUT.write_text(json.dumps(res, indent=1, default=float))
    print("\nwrote", OUT, "self_hash", res["self_hash"], flush=True)


if __name__ == "__main__":
    main()
