"""Route-L1 v1: the certificate constants as RIGOROUS BOUNDS, on the named target.

`solver/interval.py` has been an unused arithmetic layer since Route-D. `L1`'s first
deliverable is to wire it through the bordered residual so `Z_1` BOUNDS an operator norm
instead of measuring float conditioning -- and so `Y_0` bounds a residual instead of
reading one.

PRE-COMMITTED CLAUSES, written before the run (both branches of each are reportable):

  L1-1  THE ENCLOSURE IS CHECKED AGAINST AN EXACT RATIONAL REFERENCE, not against itself.
        Selected rows of the three operator products are recomputed in exact rational
        arithmetic (`fractions.Fraction`); every enclosure must contain the exact value.
        A rigorous bound that has only been checked against another float is not checked.
  L1-2  THE GATE. Does the radii polynomial close in INTERVAL arithmetic at each rung?
        YES -> report it as a rigorous statement about the TRUNCATED DISCRETE system and
        nothing more. NO -> report WHICH term ran out of margin, and do not harden.
  L1-3  BOTH EVALUATION PATHS ARE REPORTED. The naive interval matvec and the compensated
        one are run side by side at every rung, because if they differ the difference IS
        the finding: it says the binding constraint was the arithmetic and not the object.
  L1-4  A POISONED ITERATE MUST BE REJECTED. Perturbing z by 1e-6 must push Y_0 above the
        budget; a certificate that closes around a wrong point certifies nothing.
  L1-5  THE KNOWN-ANSWER OBJECT GOES THROUGH THE SAME PIPE. The a=0 CLM system of leg 49,
        whose exact solution is closed form, is certified by the same code path.
  L1-6  THE CEILING, pre-committed before the numbers exist. Closing here is a statement
        about a zero of the FINITE-DIMENSIONAL system built from the stored operators. It
        is NOT a statement about the continuum profile: the consistency of (H, D) with the
        operators they discretise, and the far field beyond X_max, are unbounded here.
        Leg 46's measured truncation gap -- the ball is 1.55e+08 radii from the true
        object -- stands untouched.

Writes writeup/data/p2_route_l1_v1_interval.json.

Run: .venv/bin/python -u experiments/p2_route_l1_v1_interval.py
"""

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.bordered_hl import BorderedHL                             # noqa: E402
from solver.interval import Interval, dot2_matvec, matvec             # noqa: E402
from solver.interval_certificate import (                             # noqa: E402
    BorderedCLMIntervals, BorderedHLIntervals, interval_constants, radii_verdict,
)
from solver.target_selection import y0_budget                         # noqa: E402
from solver.weight_search import BorderedCLM, hand_weights            # noqa: E402
from experiments.p2_route_port_v1_bordered import P_STAR, solve       # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_l1_v1_interval.json"
RUNGS = (201, 401, 801)


def exact_rows(M, v, rows):
    """Exact rational value of (M @ v)[i] for the given rows -- the L1-1 reference."""
    out = {}
    for i in rows:
        s = Fraction(0)
        for j in range(M.shape[1]):
            s += Fraction(float(M[i, j])) * Fraction(float(v[j]))
        out[int(i)] = float(s)
    return out


def check_enclosures(M, v, name, n_rows=6, seed=0):
    """L1-1: both enclosures must contain the exact rational answer."""
    rng = np.random.default_rng(seed)
    rows = sorted(rng.choice(M.shape[0], size=min(n_rows, M.shape[0]), replace=False))
    ex = exact_rows(M, v, rows)
    naive = matvec(M, Interval.point(v))
    tight = dot2_matvec(M, v)
    rec = {"operator": name, "rows": list(ex),
           "naive_contains": True, "tight_contains": True,
           "naive_width_max": float((naive.hi - naive.lo).max()),
           "tight_width_max": float((tight.hi - tight.lo).max()),
           "worst_naive_rel": 0.0, "worst_tight_rel": 0.0}
    for i, e in ex.items():
        rec["naive_contains"] &= bool(naive.lo[i] <= e <= naive.hi[i])
        rec["tight_contains"] &= bool(tight.lo[i] <= e <= tight.hi[i])
        scale = max(abs(e), 1e-300)
        rec["worst_naive_rel"] = max(rec["worst_naive_rel"],
                                     float((naive.hi[i] - naive.lo[i]) / scale))
        rec["worst_tight_rel"] = max(rec["worst_tight_rel"],
                                     float((tight.hi[i] - tight.lo[i]) / scale))
    rec["tightening"] = (rec["naive_width_max"] / rec["tight_width_max"]
                         if rec["tight_width_max"] > 0 else float("inf"))
    return rec


def hl_rung(n, naive_path=False):
    """One rung of the target object: solve, enclose, certify."""
    t0 = time.time()
    b, z, hist, cs = solve(n=n)
    w, nu, w_l = b.weights(p=P_STAR, w_l=0.01 * float(np.abs(b.X).max()))
    iv = BorderedHLIntervals(b)
    if naive_path:
        iv = _NaiveHL(b)
    c = interval_constants(iv, z, w, nu)
    v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
    cf = b.certificate_constants(z, p=P_STAR, w_l=w_l)
    return b, z, {
        "n": n, "N": b.N, "X_max": float(np.abs(b.X).max()),
        "newton_residual": float(hist["residual_ladder"][-1]),
        "ratio_c_l_over_c_omega": float(cs[0] / cs[1]),
        "interval": {k: float(x) for k, x in c.items() if k != "rigorous"},
        "verdict": {k: (float(x) if isinstance(x, (int, float)) and not isinstance(x, bool)
                        else x) for k, x in v.items()},
        "float": {"Y0": float(cf["Y0"]), "Z1": float(cf["Z1"]), "Z2": float(cf["Z2"]),
                  "Y0_over_budget": float(cf["Y0"] / y0_budget(cf["Z1"], cf["Z2"]))},
        "widening_Y0": float(c["Y0"] / cf["Y0"]),
        "widening_Z1": float(c["Z1"] / cf["Z1"]),
        "wall_s": time.time() - t0,
    }


class _NaiveHL(BorderedHLIntervals):
    """L1-3's control: the SAME certificate with the uncompensated matvec."""

    def F(self, z):
        pr = self.pr
        Om, V, c_l, c_om, c_r = pr.unpack(np.asarray(z, dtype=float))
        iOm, iV = Interval.point(Om), Interval.point(V)
        HOm = matvec(pr.H, iOm)
        S = matvec(pr.Uop, iOm) + Interval.point(c_l * pr.X) + Interval.point(c_r)
        R_Om = S * matvec(pr.D, iOm) - Interval.point(c_om) * iOm - iV
        R_V = S * matvec(pr.D, iV) - (Interval.point(2.0 * c_om) - HOm) * iV
        gd = matvec(pr.Drow0[None, :], iOm)
        G = Interval(np.array([Om[pr.i0] - pr.pin[0], gd.lo[0] - pr.pin[1],
                               V[pr.i0] - pr.pin[2]]),
                     np.array([Om[pr.i0] - pr.pin[0], gd.hi[0] - pr.pin[1],
                               V[pr.i0] - pr.pin[2]]))
        return Interval(np.concatenate([R_Om.lo, R_V.lo, G.lo]),
                        np.concatenate([R_Om.hi, R_V.hi, G.hi]))


def main():
    t0 = time.time()
    res = {"route": "L1", "version": "v1",
           "question": "Do the certificate constants close in INTERVAL arithmetic on "
                       "HL_S2_nonsymmetric, and if not, which term runs out?"}

    # -- L1-1 the enclosures against an exact rational reference ------------
    b0, z0, _, _ = solve(n=201)
    Om0, V0 = b0.unpack(z0)[0], b0.unpack(z0)[1]
    checks = [check_enclosures(b0.H, Om0, "H"),
              check_enclosures(b0.Uop, Om0, "Uop"),
              check_enclosures(b0.D, Om0, "D"),
              check_enclosures(b0.D, V0, "D(V)")]
    res["L1_1_exact_reference"] = {
        "method": "fractions.Fraction on selected rows -- exact rational dot products",
        "checks": checks,
        "all_contain": bool(all(c["naive_contains"] and c["tight_contains"]
                                for c in checks))}
    for c in checks:
        print(f"[L1-1] {c['operator']:5s} exact-contained naive={c['naive_contains']} "
              f"tight={c['tight_contains']}  width {c['naive_width_max']:.2e} -> "
              f"{c['tight_width_max']:.2e}  ({c['tightening']:.0f}x tighter)")

    # -- L1-2/L1-3 the ladder, both paths ------------------------------------
    ladder, ladder_naive = [], []
    for n in RUNGS:
        _, _, row = hl_rung(n)
        ladder.append(row)
        print(f"[L1-2] n={n:4d}  Y0={row['interval']['Y0']:.3e}  "
              f"Z1={row['interval']['Z1']:.3e}  budget={row['verdict']['budget']:.3e}  "
              f"Y0/budget={row['verdict']['Y0_over_budget']:.3e}  "
              f"{'CLOSES' if row['verdict']['closes'] else 'does NOT close'}  "
              f"[{row['wall_s']:.0f}s]")
        _, _, rown = hl_rung(n, naive_path=True)
        ladder_naive.append(rown)
        print(f"[L1-3] n={n:4d}  naive matvec: Y0={rown['interval']['Y0']:.3e}  "
              f"Y0/budget={rown['verdict']['Y0_over_budget']:.3e}  "
              f"{'CLOSES' if rown['verdict']['closes'] else 'does NOT close'}")
    res["L1_2_ladder"] = ladder
    res["L1_3_naive_path"] = ladder_naive

    # -- L1-4 the poisoned iterate -------------------------------------------
    b, z, _, _ = solve(n=201)
    w, nu, w_l = b.weights(p=P_STAR, w_l=0.01 * float(np.abs(b.X).max()))
    iv = BorderedHLIntervals(b)
    rng = np.random.default_rng(11)
    poison = []
    for eps in (1e-10, 1e-8, 1e-6):
        d = rng.standard_normal(b.N)
        d /= np.abs(d).max()
        cp = interval_constants(iv, z + eps * d, w, nu)
        vp = radii_verdict(cp["Y0"], cp["Z1"], cp["Z2"])
        poison.append({"eps": eps, "Y0": float(cp["Y0"]),
                       "Y0_over_budget": float(vp["Y0_over_budget"]),
                       "closes": bool(vp["closes"])})
        print(f"[L1-4] poisoned by {eps:.0e}: Y0/budget = {vp['Y0_over_budget']:.3e}  "
              f"{'CLOSES' if vp['closes'] else 'REJECTED'}")
    res["L1_4_poison"] = poison

    # -- L1-5 the known-answer object through the same pipe -------------------
    known = []
    for n in (201, 401):
        pc = BorderedCLM(n=n)
        zc, infc = pc.newton()
        wc, nuc = pc.weight_vector(hand_weights()["tuned_leg46"])
        ivc = BorderedCLMIntervals(pc)
        cc = interval_constants(ivc, zc, wc, nuc)
        vc = radii_verdict(cc["Y0"], cc["Z1"], cc["Z2"])
        cfc = pc.certificate_constants(zc, hand_weights()["tuned_leg46"])
        known.append({"n": n, "interval": {k: float(x) for k, x in cc.items()
                                           if k != "rigorous"},
                      "Y0_over_budget": float(vc["Y0_over_budget"]),
                      "closes": bool(vc["closes"]),
                      "r_min": vc["r_min"], "r_max": vc["r_max"],
                      "float_Y0_over_budget": float(cfc["Y0"] / cfc["budget"]),
                      "sup_distance_to_exact_profile": float(
                          np.abs(zc[:pc.n] - (-4.0 * pc.X / (1.0 + 4.0 * pc.X ** 2))).max()),
                      "newton_residual": float(infc["residual_ladder"][-1])})
        print(f"[L1-5] CLM n={n}: Y0/budget = {vc['Y0_over_budget']:.3e}  "
              f"{'CLOSES' if vc['closes'] else 'does NOT close'}; the enclosed zero is "
              f"within r_max = {vc['r_max']} of the iterate, which is "
              f"{known[-1]['sup_distance_to_exact_profile']:.2e} from the exact profile")
    res["L1_5_known_answer"] = known

    # -- L1-5b does leg 49's SEARCHED weight transfer to the rigorous constants? ---
    # Not a validated method (leg 49's gate said FAIL) -- a measurement, and a cheap
    # one: the weight was optimised against the FLOAT fitness, so whether it also
    # helps a rigorous bound is exactly the kind of thing that does not follow.
    theta_star = np.array([-1.7878937499999998, -0.75, 2.71115,
                           -0.2737546875, -2.8775])
    transfer = []
    for n in (201, 401):
        pc = BorderedCLM(n=n)
        zc, _ = pc.newton()
        ivc = BorderedCLMIntervals(pc)
        row = {"n": n}
        for lab, th in (("hand_leg46", hand_weights()["tuned_leg46"]),
                        ("searched_leg49", theta_star)):
            wq, nuq = pc.weight_vector(th)
            cq = interval_constants(ivc, zc, wq, nuq)
            vq = radii_verdict(cq["Y0"], cq["Z1"], cq["Z2"])
            row[lab] = {"Y0_over_budget": float(vq["Y0_over_budget"]),
                        "closes": bool(vq["closes"]), "Z1": float(cq["Z1"])}
        row["gain"] = (row["hand_leg46"]["Y0_over_budget"]
                       / row["searched_leg49"]["Y0_over_budget"])
        transfer.append(row)
        print(f"[L1-5b] CLM n={n}: hand {row['hand_leg46']['Y0_over_budget']:.3e} vs "
              f"searched {row['searched_leg49']['Y0_over_budget']:.3e} "
              f"({row['gain']:.2f}x)")
    res["L1_5b_weight_transfer"] = transfer

    # -- L1-6 the ceiling ----------------------------------------------------
    res["L1_6_ceiling"] = (
        "What closes is a statement about a zero of the FINITE-DIMENSIONAL polynomial "
        "system built from the STORED operators H, D, Uop on a truncated domain. The "
        "consistency of those operators with the continuum ones is NOT bounded here, and "
        "neither is the far field beyond X_max. Leg 46 measured the truncation gap at "
        "1.55e+08 ball radii and leg 47 measured that reach makes it WORSE; both stand. "
        "This is step one of L1, not L1.")
    res["verdict"] = ("CLOSES_IN_INTERVAL_ARITHMETIC_ON_THE_TRUNCATED_DISCRETE_SYSTEM"
                      if all(r["verdict"]["closes"] for r in ladder) else
                      "DOES_NOT_CLOSE")
    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)  VERDICT: {res['verdict']}")


if __name__ == "__main__":
    main()
