"""Route-PORT v2: does the truncation gap CLOSE under reach, or does the ball shrink with it?

Leg 46 measured the ceiling at one point: the distance between the truncated object and the
less-truncated one is 1.55e+08 x the certificate's ball radius, so the float certificate
closes around the TRUNCATED object and not the real one.

It did NOT measure how that ratio SCALES, and the two readings differ completely:

  * the DISTANCE falls like X_max^-0.437 (leg 46's reach power law).  Closing 8 orders of
    magnitude by reach alone needs X_max ~ 10^21 -- which on a LOG-radial grid is only
    ~7-8x more points, i.e. not obviously out of range.
  * but the certificate's own constants move with X_max too.  The tuned weight is
    w_l = 0.01 * X_max BY CONSTRUCTION, so the norm the ball is measured in changes as the
    domain grows.  If r_max shrinks as fast as the distance, brute force NEVER closes.

Nobody has measured which.  That decides between two completely different next legs:

  ratio FALLS  -> extend the domain; the gap is an engineering cost, and this run says
                  roughly what it costs.
  ratio FLAT or RISES -> reach cannot close it at any affordable size, and a rigorous
                  ANALYTIC FAR-FIELD ENCLOSURE (a tail lemma) is FORCED, not optional.

PRE-COMMITTED PREDICATE, written before the run (lesson 77 -- and note that BOTH branches
are actionable, so this cannot be argued either way after the fact):

  Q1  every rung's Newton solve converges, or the rung is refused rather than averaged in;
  Q2  the distance falls with reach (it must, or leg 46's power law was wrong);
  Q3  THE VERDICT: fit log10(distance / r_max) against rho_max over the resolved rungs.
      slope <= -0.05 per unit rho  ->  BRUTE FORCE CLOSES; report the rho_max where the
                                       ratio would reach 1, and the grid cost of getting there.
      slope >  -0.05               ->  TAIL LEMMA FORCED; say so plainly and do not
                                       propose "just refine" as the next leg.

Deterministic, ~1 min.  Writes writeup/data/p2_route_port_v2_reach.json.

Run: .venv/bin/python -u experiments/p2_route_port_v2_reach.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.target_selection import radii_polynomial                  # noqa: E402
from p2_route_port_v1_bordered import (                              # noqa: E402
    P_STAR, solve, weighted_distance,
)

OUT = ROOT / "writeup" / "data" / "p2_route_port_v2_reach.json"

# Hold the RADIAL resolution fixed as reach grows, so the ladder varies reach and not
# resolution.  n is chosen to keep d(rho) ~ constant; the leg 46 anchor is n=401 at
# rho_max=8, i.e. d(rho) = 0.02.
DRHO = 8.0 / 400.0
REACHES = [6.0, 7.0, 8.0, 9.0, 10.0]
SLOPE_GATE = -0.05


def n_for(rho_max):
    return int(round(rho_max / DRHO)) + 1


def main():
    t0 = time.time()
    print("== Route-PORT v2: does the truncation gap close under reach? ==", flush=True)
    print(f"   holding d(rho) = {DRHO} fixed; rungs rho_max = {REACHES}\n", flush=True)

    rows = []
    for rho in REACHES:
        n = n_for(rho)
        try:
            b_ref, z_ref, h_ref, cs_ref = solve(n=n, rho_max=rho)
            # the finer-domain reference for the distance, same pins so the two are comparable
            b_fin, z_fin, h_fin, _ = solve(n=n_for(rho + 1.0), rho_max=rho + 1.0,
                                           pin=b_ref.pin)
        except Exception as e:                                    # noqa: BLE001
            rows.append({"rho_max": rho, "n": n, "refused": True, "reason": repr(e)[:200]})
            print(f"   rho_max={rho:4.1f}  REFUSED ({e!r:.60})", flush=True)
            continue

        res_ref = float(np.abs(b_ref.F(z_ref)).max())
        res_fin = float(np.abs(b_fin.F(z_fin)).max())
        converged = res_ref < 1e-10 and res_fin < 1e-10
        if not converged:
            rows.append({"rho_max": rho, "n": n, "refused": True,
                         "reason": f"residual {res_ref:.2e}/{res_fin:.2e} above 1e-10"})
            print(f"   rho_max={rho:4.1f}  REFUSED (residual "
                  f"{res_ref:.2e}/{res_fin:.2e})", flush=True)
            continue

        dist, parts = weighted_distance(b_ref, z_ref, b_fin, z_fin)
        X_max = float(np.abs(b_ref.X).max())
        A = np.linalg.inv(b_ref.jacobian(z_ref))
        c = b_ref.certificate_constants(z_ref, p=P_STAR, w_l=0.01 * X_max, A=A)
        st = radii_polynomial(c["Y0"], c["Z1"], c["Z2"])
        r_max = st["r_max"]
        ratio = dist / r_max if r_max else float("inf")
        rows.append({"rho_max": rho, "n": n, "refused": False, "X_max": X_max,
                     "residual_ref": res_ref, "residual_fine": res_fin,
                     "distance": dist, "worst_block": max(parts, key=parts.get),
                     "Y0": c["Y0"], "Z1": c["Z1"], "Z2": c["Z2"],
                     "r_min": st["r_min"], "r_max": r_max, "feasible": bool(st["feasible"]),
                     "distance_over_r_max": ratio, "w_l": 0.01 * X_max})
        print(f"   rho_max={rho:4.1f}  X_max={X_max:9.1f}  n={n:5d}  "
              f"dist={dist:.3e}  r_max={r_max:.3e}  ratio={ratio:.3e}", flush=True)

    ok = [r for r in rows if not r["refused"]]
    verdict = {"n_resolved": len(ok), "n_refused": len(rows) - len(ok)}
    if len(ok) >= 3:
        x = np.array([r["rho_max"] for r in ok])
        d = np.log10([r["distance"] for r in ok])
        rm = np.log10([r["r_max"] for r in ok])
        q = np.log10([r["distance_over_r_max"] for r in ok])
        sl_d = float(np.polyfit(x, d, 1)[0])
        sl_r = float(np.polyfit(x, rm, 1)[0])
        sl_q = float(np.polyfit(x, q, 1)[0])
        closes = sl_q <= SLOPE_GATE
        verdict.update({
            "slope_log10_distance_per_rho": sl_d,
            "slope_log10_r_max_per_rho": sl_r,
            "slope_log10_ratio_per_rho": sl_q,
            "slope_gate": SLOPE_GATE,
            "brute_force_closes": bool(closes),
        })
        print(f"\n   d log10(distance)/d rho = {sl_d:+.4f}")
        print(f"   d log10(r_max)   /d rho = {sl_r:+.4f}")
        print(f"   d log10(ratio)   /d rho = {sl_q:+.4f}   (gate {SLOPE_GATE})")
        if closes:
            rho_needed = ok[-1]["rho_max"] - np.log10(ok[-1]["distance_over_r_max"]) / sl_q
            verdict["rho_max_for_ratio_1"] = float(rho_needed)
            verdict["X_max_for_ratio_1"] = float(np.exp(rho_needed))
            verdict["n_for_ratio_1"] = int(n_for(rho_needed))
            print(f"\n   VERDICT: BRUTE FORCE CLOSES. ratio -> 1 at rho_max ~ "
                  f"{rho_needed:.1f} (X_max ~ {np.exp(rho_needed):.2e}), "
                  f"n ~ {n_for(rho_needed)} at this resolution.")
        else:
            print("\n   VERDICT: TAIL LEMMA FORCED. The ball shrinks with the domain at "
                  "least as fast as the distance falls;\n            reach cannot close "
                  "the gap at any size, and a rigorous analytic far-field\n            "
                  "enclosure is required rather than optional.")
    else:
        verdict["undecided"] = "fewer than 3 resolved rungs"
        print("\n   VERDICT REFUSED: fewer than 3 resolved rungs")

    checks = {
        "Q1_every_rung_converges_or_is_refused": all(
            r["refused"] or (r["residual_ref"] < 1e-10) for r in rows),
        "Q2_distance_falls_with_reach": bool(
            len(ok) >= 2 and ok[-1]["distance"] < ok[0]["distance"]),
        "Q3_verdict_decided": "brute_force_closes" in verdict,
    }
    print("\n--- PRE-COMMITTED PREDICATE ---")
    for k, v in checks.items():
        print(f"    {'PASS' if v else 'FAIL'}  {k}")

    payload = {"route": "PORT", "version": 2,
               "question": "does the truncation gap close under reach, or does the ball "
                           "shrink with it?",
               "drho": DRHO, "reaches": REACHES, "rungs": rows, "verdict": verdict,
               "predicate_checks": checks,
               "wall_s": round(time.time() - t0, 1)}
    def _j(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        raise TypeError(type(o))

    OUT.write_text(json.dumps(payload, indent=1, default=_j))
    print(f"\nwrote {OUT}  [{payload['wall_s']}s]")


if __name__ == "__main__":
    main()
