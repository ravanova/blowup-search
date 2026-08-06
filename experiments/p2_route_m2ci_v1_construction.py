"""Route-M2CI v1 (leg 187) -- the RUNNER.

Chen's INVISCID a = 1/2 gCLM profile ("Object A", arXiv:1908.09385 eq (2.2) p.4) against
EVERY hypothesis of the radii-polynomial framework, not just the budget comparison leg 125
made.  Writes `writeup/data/p2_route_m2ci_v1_construction.json`, which is the single source
for every number quoted in the BLOG and TECHNICAL writeups and for the figure.

Run:  .venv/bin/python experiments/p2_route_m2ci_v1_construction.py

SCOPE, PRE-COMMITTED.  Object A is INVISCID (nu = 0) -- Chen's own framing, sec 1.5.  This
leg says NOTHING about the viscous "missing rung" question; that stays exactly as open as
leg 125 left it.  Object A is also a PUBLISHED CLOSED FORM (Chen eq (2.2); the whole branch
a <= 1 in HQWW arXiv:2305.05895), which is why the YES branch was recorded as hollow in
writeup/novelty/leg_187.md BEFORE any number below was computed.
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.chen_inviscid_certificate import (  # noqa: E402
    certificate_battery, divergence_exponents, gate_verdict, resolution_ladder,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_m2ci_v1_construction.json")

# The 9 rows leg 125 measured Object A at, under the radii-polynomial budget -- the lead
# this leg was dispatched to exploit.  Quoted, not recomputed; the point of this leg is
# that this column was never the binding one.
LEG125_Y0_OVER_BUDGET = {"min": 1.325e-09, "max": 5.800e-05, "rows": 9,
                         "source": "leg 125 (Route-M2P), writeup/data/p2_route_m2p_v1_promotion.json",
                         "reading_then": "comfortably inside certificate range",
                         "reading_now": ("correct, and irrelevant -- Y_0 is EXACTLY ZERO "
                                         "here and the certificate still cannot close")}


def main():
    print("Route-M2CI v1 -- Object A against every certificate hypothesis")
    print("  battery at n = 801 ...")
    battery = certificate_battery(n=801, s=2.0)

    print("  divergence ladder n = 201..1201 ...")
    divergence = divergence_exponents(ns=(201, 301, 401, 601, 801, 1201), s=2.0)

    print("  clause ladder n = 401, 601, 801 ...")
    ladder = resolution_ladder(ns=(401, 601, 801), s=2.0)

    verdict = gate_verdict(battery, divergence)

    payload = {
        "leg": 187,
        "route": "M2CI",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "object": ("Chen arXiv:1908.09385 eq (2.2) p.4 -- the INVISCID a = 1/2 gCLM "
                   "self-similar profile Omega = -2bX/(X^2+b^2)^2, b^2 = 3/8, "
                   "c_l = 1/3, c_omega = -1 (nu = 0)"),
        "scope_disclaimer": verdict["scope"],
        "gate_verdict": verdict,
        "battery_n801": battery,
        "divergence_exponents": divergence,
        "clause_ladder": ladder,
        "leg125_budget_lead": LEG125_Y0_OVER_BUDGET,
        "headline_magnitudes": {
            "Y0_exact": 0.0,
            "Z0_plus_Z1_lower_bound_every_A": 1.0,
            "contraction_factor_upper_bound": 0.0,
            "exact_orbit_gammas_verified_zero": len(battery["H2_exact_rows"]),
            "kernel_relative_defect_n801":
                battery["H4_injectivity"]["orbit_tangent_phi"]["relative_defect"],
            "control_relative_defect_n801":
                battery["H4_injectivity"]["control_localised_bump"]["relative_defect"],
            "kernel_to_control_ratio_n801":
                battery["H4_injectivity"]["kernel_to_control_ratio"],
            "Z2_slope_in_log_n": divergence["slopes_in_log_n"]["Z2"],
            "Z2_growth_over_6x_ladder": divergence["Z2_growth_over_ladder"],
            "sigma_ratio_slope_in_log_n": divergence["slopes_in_log_n"]["sigma_ratio"],
            "sigma_ratio_collapse_over_6x_ladder":
                divergence["sigma_ratio_collapse_over_ladder"],
            "farfield_symbol_zero_at_s": battery["H6b_farfield_symbol"]["symbol_zero_at_s"],
            "measured_profile_decay_exponent": battery["H6c_measured_decay"]["exponent"],
            "decay_control_on_Xminus2":
                battery["H6c_measured_decay"]["control_slope_on_Xminus2_profile"],
            "bordering_sigma_min_lift_n801":
                battery["H6a_bordered"]["sigma_min"]
                / battery["H6a_bordered"]["unbordered_sigma_min"],
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, default=str)

    h = payload["headline_magnitudes"]
    print()
    print(f"  GATE: {verdict['answer']} -- {', '.join(verdict['failing_clauses'])}")
    print(f"  Y_0 exactly {h['Y0_exact']}, Z_0 + Z_1 >= {h['Z0_plus_Z1_lower_bound_every_A']}"
          f" for EVERY A")
    print(f"  kernel/control relative defect ratio: {h['kernel_to_control_ratio_n801']:.3e}")
    print(f"  Z_2 ~ n^{h['Z2_slope_in_log_n']:.2f} "
          f"({h['Z2_growth_over_6x_ladder']:.1f}x over the ladder)")
    print(f"  sigma_min/sigma_max ~ n^{h['sigma_ratio_slope_in_log_n']:.2f}")
    print(f"  far-field symbol vanishes at s = {h['farfield_symbol_zero_at_s']:.3f}; "
          f"profile decays at {h['measured_profile_decay_exponent']:.4f}")
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
