"""Leg 210, Route-M2SV: the standing test for the independent verification of leg 185's nu.

Self-running script, per this repository's convention (`.venv/bin/python <this>`, no pytest).

WHAT IT GUARDS, AND WHAT IT DELIBERATELY DOES NOT.  The full verification
(`experiments/p2_route_m2sv_v1_postconstruction.py`) takes ~45 minutes, mostly in the n = 1201
grids and in replaying leg 185's least-squares path, so it is NOT re-run here.  What this test
does is:

  (1) re-run the INDEPENDENT re-derivation live at n = 201 -- cheap, because the odd-subspace
      reduction leaves a 101 x 101 system -- and check the SIGN pattern it produces.  This is a
      live computation, not a JSON self-consistency check: if the operators are edited, it fails.
  (2) re-validate the independent operators against CLOSED FORMS, live.
  (3) check the dilation covariance nu(kappa*g) * kappa^2 = nu(g) live, SEEDED with the dilated
      solution -- the algebraically distinct route that makes the confirmation independent.
  (4) guard the SPLIT verdict in the banked artifact.  This is the important one.  Leg 210 did
      NOT return a clean confirmation: the headline nu at a = 0.30 reproduces to ~6 digits, but
      leg 185's a = 1/2 MAGNITUDES do not reproduce, and its a* cross-check does not either.
      A later edit that quietly promotes this to "confirmed" must fail this test.

Nothing here asserts existence of Object B.  Everything here is float.
"""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from experiments.p2_route_m2sv_v1_postconstruction import (      # noqa: E402
    IndepProfile, solve_nu_indep, v0_operator_validation,
    LEG185_NU_A030, LEG125_A_STAR, DATA,
)
from solver.dissipative_profile import DissipativeProfile, chen_profile   # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not cond:
        FAILS.append(name)


def leg185_gauge(ip):
    dp = DissipativeProfile(a=0.30, n=ip.n, rho_max=8.0)
    return float(dp.D[dp.i0] @ chen_profile(dp.X)[0])


# ---------------------------------------------------------------------------
print("T1  independent operators still reproduce closed forms (live)")
v0 = v0_operator_validation(n=401)
check("Hilbert vs Chen's exact H Omega = U_x", v0["hilbert_on_chen_pair_relative"] < 1e-5,
      "rel %.3e" % v0["hilbert_on_chen_pair_relative"])
check("cumulative integral vs Chen's exact U = X/(b^2+X^2)",
      v0["cumint_on_chen_U_relative"] < 1e-6, "rel %.3e" % v0["cumint_on_chen_U_relative"])
check("6th-order d/dX vs closed-form Omega_X",
      v0["d1_on_chen_relative_sup_error"] < 1e-6,
      "rel %.3e" % v0["d1_on_chen_relative_sup_error"])
check("chain-rule d^2/dX^2 vs closed-form Omega_XX (NOT D@D)",
      v0["d2_on_chen_relative_sup_error"] < 1e-6,
      "rel %.3e" % v0["d2_on_chen_relative_sup_error"])
check("Omega_X(0) matches the closed form -2/b^3",
      v0["d1_at_origin_relative_error"] < 1e-6,
      "rel %.3e" % v0["d1_at_origin_relative_error"])

# ---------------------------------------------------------------------------
print("T2  the SIGN pattern reproduces live at n=201 (the part that DID verify)")
ip30 = IndepProfile(a=0.30, n=201)
g30 = leg185_gauge(ip30)
r30 = solve_nu_indep(ip30, 0.30, 0.3, g30)
check("a=0.30 converged", r30["residual_relative"] < 1e-10,
      "res %.2e, nu = %+.8f" % (r30["residual_relative"], r30["nu"]))
check("nu > 0 at a = 0.30 (Object B exists below a*)", r30["nu"] > 0,
      "nu = %+.8f" % r30["nu"])
check("a=0.30 nu within 1e-4 of leg 185's grid-converged 0.01799364 even at n=201",
      abs(r30["nu"] - LEG185_NU_A030) < 1e-4,
      "|diff| %.2e" % abs(r30["nu"] - LEG185_NU_A030))

ip45 = IndepProfile(a=0.45, n=201)
r45 = solve_nu_indep(ip45, 0.45, 0.3, leg185_gauge(ip45))
check("nu < 0 at a = 0.45 (anti-diffusive above a*)", r45["nu"] < 0,
      "nu = %+.8f, res %.2e" % (r45["nu"], r45["residual_relative"]))

# ---------------------------------------------------------------------------
print("T3  dilation covariance, SEEDED: nu(kappa*g) * kappa^2 = nu(g), live")
base = solve_nu_indep(ip30, 0.30, 0.3, g30)
Om_base = base["Omega"]
for kap in (0.5, 2.0):
    seed = np.interp(kap * ip30.X, ip30.X, Om_base, left=0.0, right=0.0)
    pred = base["nu"] / kap ** 2
    off = solve_nu_indep(ip30, 0.30, pred, g30 * kap, Om_start=seed)
    rel = abs(off["nu"] * kap ** 2 - base["nu"]) / abs(base["nu"])
    check("kappa=%.2f off-gauge solve rescales onto the on-gauge nu" % kap, rel < 1e-3,
          "rel %.3e" % rel)
    check("kappa=%.2f preserves the SIGN of nu (mu^2 > 0)" % kap,
          (off["nu"] > 0) == (base["nu"] > 0))

# ---------------------------------------------------------------------------
print("T4  the banked artifact carries the SPLIT verdict, not a clean confirmation")
if not os.path.exists(DATA):
    check("banked JSON exists", False, DATA + " missing -- run the experiment first")
else:
    with open(DATA) as fh:
        d = json.load(fh)
    v = d["VERDICT"]
    c1, c2, c3 = (v["clause_1_headline_nu_at_a_0p30"],
                  v["clause_2_negative_values_at_chen_a"],
                  v["clause_3_a_star_crossing"])

    check("gate answer is SPLIT, not a bare YES", v["gate_answer"].startswith("SPLIT"),
          v["gate_answer"])
    check("escalation is flagged", v["escalation_required"] is True)

    # clause 1 -- the part that verified
    check("clause 1 CONFIRMED", c1["verdict"] == "CONFIRMED")
    check("clause 1 agrees to at least 5 significant digits",
          c1["relative_agreement"] < 1e-5,
          "rel %.3e (%.1f digits)" % (c1["relative_agreement"],
                                      c1["significant_digits_agreeing"]))
    check("leg 185's headline is transcribed exactly", c1["leg185_value"] == 0.01799364)
    check("clause 1's ladder is monotone-converging (4 grids)",
          len(c1["this_leg_ladder"]) == 4)

    # clause 2 -- the discrepancy, which must stay visible
    check("clause 2 records SIGN confirmed but MAGNITUDE not",
          c2["verdict"] == "SIGN CONFIRMED, MAGNITUDE NOT REPRODUCED", c2["verdict"])
    check("clause 2 sign_reproduced is true", c2["sign_reproduced"] is True)
    check("clause 2 magnitude_reproduced is FALSE", c2["magnitude_reproduced"] is False)
    check("clause 2 quantifies the magnitude gap (>2x)",
          c2["magnitude_ratio_leg185_over_this_leg"] > 2.0,
          "%.2fx" % c2["magnitude_ratio_leg185_over_this_leg"])
    check("clause 2 shows leg 185's OWN scheme is not grid-converged at a=1/2",
          c2["leg185_own_grid_span_at_a_0p50"] is not None
          and c2["leg185_own_grid_span_at_a_0p50"] > 0.1,
          "own relative span %s" % c2["leg185_own_grid_span_at_a_0p50"])

    # clause 3 -- the a* cross-check that did not survive
    check("clause 3 records a* NOT REPRODUCED", c3["verdict"] == "NOT REPRODUCED",
          c3["verdict"])
    check("clause 3 records leg 185's own straddling starts at a=0.3865",
          c3["leg185_own_two_starts_at_a_0p3865"][0] > 0
          > c3["leg185_own_two_starts_at_a_0p3865"][1])

    # the sign claim, which verified and was strengthened
    sc = v["sign_claim_overall"]
    check("sign claim confirmed and strengthened", sc["verdict"] == "CONFIRMED AND STRENGTHENED")
    check("sign shown dilation-invariant (gauge-independent)",
          sc["sign_is_dilation_invariant"] is True)

    # V5 must exist -- it is the instrument that found the discrepancy
    v5 = d["V5_negative_branch_grid_study"]
    check("V5 ran both schemes at a=0.30 control and a=1/2",
          {r["a"] for r in v5["per_a"]} >= {0.30, 0.50})
    v5_30 = [r for r in v5["per_a"] if r["a"] == 0.30][0]
    v5_50 = [r for r in v5["per_a"] if r["a"] == 0.50][0]
    check("V5 control: a=0.30 refines cleanly in BOTH schemes (span < 5e-3)",
          v5_30["this_leg_relative_span_over_converged"] < 5e-3
          and v5_30["leg185_relative_span_over_converged"] < 5e-3,
          "mine %.2e / leg185 %.2e" % (v5_30["this_leg_relative_span_over_converged"],
                                       v5_30["leg185_relative_span_over_converged"]))
    check("V5 contrast: a=1/2 span is >=50x the a=0.30 span in BOTH schemes",
          v5_50["this_leg_relative_span_over_converged"]
          > 50 * v5_30["this_leg_relative_span_over_converged"]
          and v5_50["leg185_relative_span_over_converged"]
          > 50 * v5_30["leg185_relative_span_over_converged"],
          "a=1/2: mine %.3f / leg185 %.3f" % (v5_50["this_leg_relative_span_over_converged"],
                                              v5_50["leg185_relative_span_over_converged"]))
    check("V5 records the amplitude collapse this leg's own scheme shows at a=1/2",
          v5_50["this_leg_min_over_max_amplitude"] < 0.7,
          "min/max amplitude %.3f (drifting toward the trivial null)"
          % v5_50["this_leg_min_over_max_amplitude"])

    # honesty clauses -- lesson 76: the limits stay in the artifact
    check("no_dynamics_run recorded true", d["no_dynamics_run"] is True)
    check("artifact says float, not certificate",
          "NOT an existence result" in d["what_this_is"]
          and "No certificate" in d["what_this_is"])
    check("the WEAKER a=0 CLM Hilbert check is reported, not suppressed",
          d["V0_operator_validation"]["hilbert_on_a0_clm_pair_sup_error"]
          > d["V0_operator_validation"]["hilbert_on_chen_pair_sup_error"]
          and "not a validation" in d["V0_operator_validation"]["hilbert_on_a0_clm_pair_note"])
    check("replay tier is labelled as the weakest",
          d["V1_replay_weakest_tier"]["tier"].startswith("WEAKEST"))
    check("the unseeded (basin) covariance numbers are kept, not dropped",
          all("unseeded_worst_relative_error" in r
              for r in d["V3_dilation_covariance_route"]["per_a"]))
    check("V4 reports non-converged scan points rather than hiding them",
          "points_failed_to_converge" in d["V4_sign_flip_location"])

# ---------------------------------------------------------------------------
print()
if FAILS:
    print("FAILED (%d): %s" % (len(FAILS), "; ".join(FAILS)))
    sys.exit(1)
print("ALL CHECKS PASS")
