"""Leg 401, unit L6 -- EVIDENCE SCRIPT for `writeup/data/p2_route_l6_profile_v1.json`.

Lesson 68: an artefact that is not re-derivable is not evidence.  This script re-derives
every load-bearing claim of the artefact FROM THE ARTEFACT (and, for the two checks that
need it, by re-running the construction), and EXITS NON-ZERO on any disagreement.

It quotes no prose.  Every number it compares against is read out of a banked JSON.

    python3 experiments/p2_route_l6_v1_evidence.py            # full (re-runs the residual)
    python3 experiments/p2_route_l6_v1_evidence.py --fast     # artefact-internal only

Checks
------
 C01  self_hash recomputes
 C02  every rung's reported residual is the minimum over its starts
 C03  n_dof equals 2 * Lmax(Lmax+2) * Nr * (2Ks+1) at every rung
 C04  quadrature sizes equal the pre-registered formulas at every rung
 C05  the joint ladder equals the pre-registered table (leg_401.md SS5)
 C06  gate.smallest_residual is the minimum over the branch's rungs
 C07  gate.residual_at_best_affordable_resolution is the top rung's residual
 C08  gate.per_rung_relative_change recomputes
 C09  gate.rate_dlogresid_dlogndof_last3 / _all recompute by least squares
 C10  gate.decreases_under_refinement recomputes under the pre-registered decision rule
 C11  the load-bearing norm string equals the one banked by L5, character for character
 C12  BAN C1 block is present, engaged=False, and carries its citation
 C13  chain block says no L1->L4 link moved
 C14  self-tests are present and under their pre-registered thresholds
 C15  reading (c-1)/(c-3) fired-flags agree with their own tolerances
 C16  the banked profile's coefficient vector has length n_dof and is finite
 C17  axis-ladder rates recompute from the axis rungs
 C18  [slow] the banked coefficient vector reproduces the banked residual
 C19  [slow] the banked coefficient vector is divergence free
 C20  [slow] the banked field_samples reproduce from the banked coefficients
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"
L5_ART = ROOT / "writeup" / "data" / "p2_route_l5_finite_energy_v1.json"

PREREG_JOINT = [["J0", 2, 8, 1], ["J1", 2, 12, 1], ["J2", 3, 12, 2],
                ["J3", 3, 16, 2], ["J4", 4, 20, 3]]
SELFTEST_TOL = dict(
    T_A_div_V_max_abs_over_scale=1e-8,
    T_B_grad_max_rel_err=1e-5,
    T_C_curl_max_rel_err=1e-5,
    T_D_W_vs_fd_curlR_max_rel_err=1e-2,
    T_E_dss_period_max_rel_err=1e-12,
    T_F_quadrature_rel_err=1e-8,
)

FAILURES = []
NCHECK = 0


def chk(name, ok, detail=""):
    global NCHECK
    NCHECK += 1
    print(f"  [{'OK ' if ok else 'FAIL'}] {name}{('  ' + detail) if detail else ''}")
    if not ok:
        FAILURES.append(f"{name}: {detail}")


def close(a, b, rtol=1e-9, atol=1e-12):
    return abs(float(a) - float(b)) <= atol + rtol * abs(float(b))


def lstsq_slope(ns, rs):
    ns, rs = np.asarray(ns, float), np.asarray(rs, float)
    ok = rs > 0
    if ok.sum() < 2:
        return float("nan")
    A = np.vstack([np.log(ns[ok]), np.ones(int(ok.sum()))]).T
    return float(np.linalg.lstsq(A, np.log(rs[ok]), rcond=None)[0][0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true",
                    help="skip C18-C20, which re-run the construction")
    args = ap.parse_args()

    if not ART.exists():
        print(f"MISSING ARTEFACT {ART}")
        return 2
    doc = json.loads(ART.read_text())

    print(f"EVIDENCE for {ART.relative_to(ROOT)}")
    print(f"  leg={doc.get('leg')} unit={doc.get('unit')} "
          f"self_hash={doc.get('self_hash')}\n")

    # ---- C01 self_hash ----------------------------------------------------------------
    body = dict(doc)
    banked_hash = body.pop("self_hash", None)
    recomputed = hashlib.sha256(
        json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    chk("C01 self_hash recomputes", banked_hash == recomputed,
        f"banked={banked_hash} recomputed={recomputed}")

    lad = doc["ladder_results"]

    # ---- C02..C04 per-rung internal consistency ---------------------------------------
    bad2 = bad3 = bad4 = []
    bad2, bad3, bad4 = [], [], []
    axis_rungs = []
    for L in doc.get("axis_ladders", {}).get("ladders", {}).values():
        axis_rungs.extend(L["rungs"])
    for row in [r for br in lad.values() for r in br] + axis_rungs:
        who = f"{row.get('branch')}/{row.get('tag')}"
        mn = min(st["fun"] for st in row["starts"])
        if not close(row["residual_load_bearing"], mn, rtol=0, atol=0):
            bad2.append(f"{who}: {row['residual_load_bearing']} != min {mn}")
        nH = row["Lmax"] * (row["Lmax"] + 2)
        want = 2 * nH * row["Nr"] * (2 * row["Ks"] + 1)
        if row["n_dof"] != want:
            bad3.append(f"{who}: {row['n_dof']} != {want}")
        q = dict(nq_r=3 * row["Nr"] + 12, n_theta=2 * row["Lmax"] + 8,
                 n_phi=4 * row["Lmax"] + 12, n_s=4 * row["Ks"] + 6)
        for k, v in q.items():
            if row[k] != v:
                bad4.append(f"{who}.{k}: {row[k]} != {v}")
    chk("C02 reported residual is the minimum over starts", not bad2, "; ".join(bad2[:3]))
    chk("C03 n_dof = 2*Lmax(Lmax+2)*Nr*(2Ks+1)", not bad3, "; ".join(bad3[:3]))
    chk("C04 quadrature sizes match the pre-registered formulas", not bad4,
        "; ".join(bad4[:3]))

    # ---- C05 the ladder is the pre-registered one -------------------------------------
    got = [list(x) for x in doc["joint_ladder"]]
    chk("C05 joint ladder equals leg_401.md SS5", got == PREREG_JOINT[:len(got)],
        f"{got}")

    # ---- C06..C10 the gate block ------------------------------------------------------
    for branch in ("A", "B"):
        rows = lad[branch]
        g = doc["gate"][branch]
        rs = [r["residual_load_bearing"] for r in rows]
        ns = [r["n_dof"] for r in rows]
        chk(f"C06[{branch}] smallest_residual = min over rungs",
            close(g["smallest_residual"], min(rs), rtol=0, atol=0),
            f"{g['smallest_residual']} vs {min(rs)}")
        chk(f"C07[{branch}] residual at best affordable resolution = top rung",
            close(g["residual_at_best_affordable_resolution"], rs[-1], rtol=0, atol=0),
            f"{g['residual_at_best_affordable_resolution']} vs {rs[-1]}")
        rels = [(rs[i] - rs[i - 1]) / rs[i - 1] for i in range(1, len(rs))]
        chk(f"C08[{branch}] per-rung relative change recomputes",
            len(rels) == len(g["per_rung_relative_change"])
            and all(close(a, b) for a, b in zip(g["per_rung_relative_change"], rels)))
        k = slice(max(0, len(rs) - 3), len(rs))
        s3, sa = lstsq_slope(ns[k], rs[k]), lstsq_slope(ns, rs)
        chk(f"C09[{branch}] refinement rate recomputes",
            close(g["rate_dlogresid_dlogndof_last3"], s3, rtol=1e-8)
            and close(g["rate_dlogresid_dlogndof_all"], sa, rtol=1e-8),
            f"last3 {g['rate_dlogresid_dlogndof_last3']:.6g} vs {s3:.6g}")
        strictly_dec = all(rs[i] < rs[i - 1] for i in range(max(1, len(rs) - 2), len(rs)))
        big = all(r < -0.05 for r in rels[-2:]) if len(rels) >= 2 else False
        want = "YES" if (strictly_dec and big and s3 < -0.05) else "NO"
        chk(f"C10[{branch}] decision rule reproduces the YES/NO",
            g["decreases_under_refinement"] == want,
            f"banked={g['decreases_under_refinement']} recomputed={want}")

    # ---- C11 the norm is L5's banked norm, not an invented one -------------------------
    if L5_ART.exists():
        l5 = json.loads(L5_ART.read_text())
        l5norm = l5["realization_lesson_91"]["norms"]["vorticity_LOAD_BEARING"]
        norms = doc["realization_lesson_91"]["norms"]
        mine = norms["LOAD_BEARING"]
        head = "||curl F||_{L1_t L3/2_x}"
        # the artefact must carry L5's string CHARACTER FOR CHARACTER, and its own
        # statement of the norm must be the same functional
        chk("C11 load-bearing norm is the one L5 banked, quoted verbatim",
            norms.get("norm_source_verbatim") == l5norm
            and mine.startswith(head) and l5norm.startswith(head)
            and "L3/2" in mine and "pressure-free" in mine,
            f"L5={l5norm!r}")
    else:
        chk("C11 load-bearing norm is the one L5 banked, quoted verbatim", False,
            "L5 artefact missing")

    # ---- C12..C14 ---------------------------------------------------------------------
    b = doc["ban_C1"]
    chk("C12 BAN C1 pre-registration present and not engaged",
        b["engaged"] is False
        and b["constructs_no_bounded_approximate_inverse_uniform_in_M"] is True
        and "Byrd" in b["citation"] and "Nocedal" in b["citation"])
    c = doc["chain"]
    chk("C13 no L1->L4 link moved",
        c["L1_to_L4_link_moved"] == "NONE" and c["clay_percent_unchanged"] is True
        and c["this_is_not_a_blowup"] is True and c["this_is_not_a_certificate"] is True)
    st = doc["selftests"]
    badst = [f"{k}={st.get(k)}>{v}" for k, v in SELFTEST_TOL.items()
             if not (k in st and float(st[k]) < v)]
    chk("C14 self-tests present and under their thresholds", not badst, "; ".join(badst))

    # ---- C15 readings -----------------------------------------------------------------
    r1 = doc["readings"]["reading_c1_SS_collapse"]
    ok15 = all(r1[f"fired_{br}"] is bool(
        float(r1[f"branch_{br}_oscillating_fraction"]) < float(r1["tolerance"]))
        for br in ("A", "B"))
    chk("C15 reading (c-1) fired-flags agree with the banked tolerance", ok15,
        f"tol={r1['tolerance']} A={r1['branch_A_oscillating_fraction']:.3e} "
        f"B={r1['branch_B_oscillating_fraction']:.3e}")

    # ---- C16 the profile is actually banked -------------------------------------------
    bad16 = []
    for branch, prof in doc.get("banked_profile", {}).items():
        coef = np.asarray(prof["coefficients"], float)
        if coef.size != prof["n_dof"]:
            bad16.append(f"{branch}: {coef.size} != n_dof {prof['n_dof']}")
        if not np.all(np.isfinite(coef)):
            bad16.append(f"{branch}: non-finite coefficients")
        if coef.size and float(np.max(np.abs(coef))) == 0.0:
            bad16.append(f"{branch}: identically zero field")
    chk("C16 a nonzero, finite, correctly sized profile is banked for each branch",
        bool(doc.get("banked_profile")) and not bad16, "; ".join(bad16))

    # ---- C17 axis-ladder rates --------------------------------------------------------
    bad17 = []
    for name, L in doc.get("axis_ladders", {}).get("ladders", {}).items():
        rs = [r["residual_load_bearing"] for r in L["rungs"]]
        ns = [r["n_dof"] for r in L["rungs"]]
        if not close(L["rate_dlogresid_dlogndof"], lstsq_slope(ns, rs), rtol=1e-8):
            bad17.append(f"{name}: {L['rate_dlogresid_dlogndof']} vs "
                         f"{lstsq_slope(ns, rs)}")
        pr = L["per_rung_residual"]
        for row in L["rungs"]:
            if not close(pr[row["tag"]], row["residual_load_bearing"], rtol=0, atol=0):
                bad17.append(f"{name}/{row['tag']} residual table mismatch")
    chk("C17 axis-ladder rates and residual tables recompute", not bad17,
        "; ".join(bad17[:3]))

    # ---- C18..C20 re-run the construction ---------------------------------------------
    if args.fast:
        print("\n  (--fast: C18-C20 skipped)")
    else:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import p2_route_l6_v1 as L6  # noqa: E402
        from p2_route_l6_v1_ad import Var  # noqa: E402

        for branch, prof in doc.get("banked_profile", {}).items():
            g = L6.Geom(prof["Lmax"], prof["Nr"], prof["Ks"], prof["Lmap"])
            x = np.asarray(prof["coefficients"], float)
            aF, aQ = g.unpack(x)
            harm = [[int(l), int(m)] for (l, m) in g.harm]
            chk(f"C16b[{branch}] harmonic ordering reproduces",
                harm == [list(h) for h in prof["harmonics_l_m"]])

            W, _, _ = L6.residual_field(g, Var(aF), Var(aQ))
            rho = float(L6.load_bearing_norm(g, W).v)
            chk(f"C18[{branch}] banked coefficients reproduce the banked residual",
                close(rho, prof["residual_load_bearing"], rtol=1e-8),
                f"recomputed={rho:.12e} banked={prof['residual_load_bearing']:.12e}")

            # divergence, by central differences on the independent Cartesian evaluator
            rng = np.random.default_rng(4010)
            pts = rng.standard_normal((24, 3)) * 1.3
            h = 1e-5
            dv, sc = [], []
            for q in pts:
                acc = 0.0
                for j in range(3):
                    e = np.zeros(3)
                    e[j] = h
                    acc += (L6.eval_V_cart(g, aF, aQ, (q + e)[None, :], 0.37)[0, j]
                            - L6.eval_V_cart(g, aF, aQ, (q - e)[None, :], 0.37)[0, j]) \
                        / (2 * h)
                dv.append(abs(acc))
                sc.append(float(np.max(np.abs(
                    L6.eval_V_cart(g, aF, aQ, q[None, :], 0.37)))))
            rel = max(dv) / max(1e-300, max(sc))
            chk(f"C19[{branch}] the banked field is divergence free", rel < 1e-6,
                f"max|div V| / max|V| = {rel:.3e}")

            bad20, finite = 0.0, True
            for samp in prof["field_samples"]:
                P = np.asarray(samp["points"], float)
                Vb = np.asarray(samp["V"], float)
                Vr = L6.eval_V_cart(g, aF, aQ, P, samp["s"])
                finite = finite and bool(np.all(np.isfinite(Vb))
                                         and np.all(np.isfinite(Vr)))
                dev = np.max(np.abs(Vr - Vb)) / max(1e-300, np.max(np.abs(Vb)))
                # NaN must not be swallowed by max(): compare explicitly
                if not np.isfinite(dev) or dev > bad20:
                    bad20 = float(dev)
            chk(f"C20[{branch}] banked field samples are finite and reproduce",
                finite and np.isfinite(bad20) and bad20 < 1e-10,
                f"finite={finite} max rel dev = {bad20:.3e}")

    # ---- verdict ----------------------------------------------------------------------
    print(f"\n{NCHECK} checks, {len(FAILURES)} failure(s)")
    if FAILURES:
        for f in FAILURES:
            print(f"  FAIL {f}")
        print("EVIDENCE: DOES NOT REPRODUCE")
        return 1
    print("EVIDENCE: REPRODUCES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
