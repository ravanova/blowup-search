"""Route-WE (leg 111): the WEIGHTED-ENERGY coercivity gap of the `a = 0` CLM linearisation.

THE GATE, in its pre-committed wording (DIRECTION.md, leg 111):

    For at least one weight in the pre-named family, is the measured coercivity gap of the
    weighted-energy form on the a=0 CLM linearization positive and stable (within a
    pre-committed tolerance declared in the driver) across two grid refinements?

      yes -> A candidate third realization for L1 exists.  Bank the magnitudes and
             ESCALATE scoping to the user; build nothing further under this leg.
      no  -> The weighted-energy realization joins the dead list on the friendliest
             object, and the wall bounds the real target's difficulty from below.  Bank it
             as a third dead realization, which STRENGTHENS NG's framing; report
             magnitudes, not the boolean.

--------------------------------------------------------------------------
THE TOLERANCE, DECLARED HERE, AND WHY IT IS THE RELATIVE ONE
--------------------------------------------------------------------------
Three conditions, all three required, evaluated per weight:

  (P) POSITIVITY      gap > 0 at the finest `n`.
  (S) STABILITY       |gap(n_{i+1}) - gap(n_i)| / |gap(n_i)| <= 0.05 across EACH of the
                      last two refinements of the `n`-ladder.
  (A) ADMISSIBILITY   the weight defines a space that contains the basis at all:
                      |ratio - 1| <= 0.05, where `ratio` is `||sin theta||^2_phi` computed
                      at grading depth `2 n_grade` over the same at `n_grade`.

**(S) is RELATIVE on purpose, and the choice is disclosed.**  An ABSOLUTE tolerance
(`|delta| <= 0.05`) is passed trivially by any sequence collapsing to zero, which is
exactly the behaviour the inadmissible member of this family exhibits -- so an absolute
reading would convert "the gap is vanishing" into "the gap is stable", which is the
opposite of what the gate is asking.  The record below reports BOTH readings for every
weight so the difference is auditable rather than asserted.  Disclosure, since this
repository cares: the ladders were run exploratorily before this tolerance was written
down.  Exactly one weight (`A3`) is read differently by the two forms, and that weight is
independently disqualified on two further, wholly separate grounds -- (A), and the
quadrature-artifact sweep in section 4 -- so the gate's answer does not depend on the
choice.

--------------------------------------------------------------------------
THE PREDICTION, REGISTERED BEFORE THE LADDERS (the T-5 discipline)
--------------------------------------------------------------------------
From the closed forms in `solver/energy_coercivity.py`, with `phi = (2 sin(theta/2))^-gamma`:

    damping at the origin      D(0) = (3 - gamma)/2 < 0   iff   gamma > 3
    basis in the space         integrand ~ theta^(2-gamma) finite  iff   gamma < 3

**The two thresholds are the same number.**  So the prediction is: no member of the family
has both, the admissible members' gaps converge to `-D(0) = -(3 - gamma)/2` by
concentration at the origin, and the window closes to ZERO WIDTH at `gamma = 3` rather
than being empty by a margin.  Sections 2-4 are the test of that.

Writes writeup/data/p2_route_we_v1_coercivity.json.  Deterministic; float64 throughout.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from solver.energy_coercivity import (                             # noqa: E402
    KNOWN_ANSWER_CEILING, WEIGHT_FAMILY, admissibility, coercivity_gap,
    damping_factor_at_origin,
)

OUT = Path(__file__).resolve().parent.parent / "writeup" / "data" / "p2_route_we_v1_coercivity.json"

TOL_STABILITY_REL = 0.05
TOL_STABILITY_ABS = 0.05
TOL_ADMISSIBLE = 0.05
N_LADDER = (16, 32, 64, 128, 256)
GRADE_LADDER = (12, 24, 48, 96)
MU_LADDER = (0.0, 0.25, 0.5, 1.0, 2.0)


def _rel(ladder):
    return [abs(ladder[i + 1] - ladder[i]) / max(abs(ladder[i]), 1e-300)
            for i in range(len(ladder) - 1)]


def _abs(ladder):
    return [abs(ladder[i + 1] - ladder[i]) for i in range(len(ladder) - 1)]


def main():
    t0 = time.time()
    res = {
        "leg": 111, "route": "WE", "object": "a = 0 CLM linearisation, odd sine basis",
        "form": "weighted L^2 energy: gap = -sup <L h, h>_phi / ||h||^2_phi",
        "tolerances": {"stability_relative": TOL_STABILITY_REL,
                       "stability_absolute_reported_for_contrast": TOL_STABILITY_ABS,
                       "admissibility": TOL_ADMISSIBLE},
        "n_ladder": list(N_LADDER), "grade_ladder": list(GRADE_LADDER),
        "mu_ladder": list(MU_LADDER),
        "known_answer_ceiling": KNOWN_ANSWER_CEILING,
        "known_answer_source": "Xu arXiv:2607.19762 -- point spectrum exactly {0,1}, "
                               "essential spectrum on Re lambda = -1/2, modulated gap 1/2",
    }

    # 1 -- ADMISSIBILITY, measured
    print("[1] admissibility of the seven named weights")
    adm = {}
    for nm, fam, g in WEIGHT_FAMILY:
        a = admissibility(fam, g)
        a["admissible"] = abs(a["ratio"] - 1.0) <= TOL_ADMISSIBLE
        a["damping_at_origin"] = damping_factor_at_origin(fam, g)
        adm[nm] = a
        print(f"    {nm:12s} margin {a['exponent_margin']:+.1f}  norm2 {a['norm2_coarse']:.6g}"
              f"  ratio {a['ratio']:.6g}  D(0) {a['damping_at_origin']:+.2f}"
              f"  -> {'admissible' if a['admissible'] else 'NOT admissible'}")
    res["admissibility"] = adm

    # 2 -- THE GAP LADDERS, modulated (the two published point modes removed) and raw
    print("[2] coercivity gap ladders in n")
    gaps = {}
    for nm, fam, g in WEIGHT_FAMILY:
        recs = [coercivity_gap(n, fam, g) for n in N_LADDER]
        mod = [r["gap"] for r in recs]
        raw = [coercivity_gap(n, fam, g, modulate=False)["gap"] for n in N_LADDER]
        # The concentration limit is a prediction ONLY where the space exists.  Reporting
        # -(3-gamma)/2 for an inadmissible weight would be bounding a quantity with no
        # referent (lesson 73), so it is None there.
        pred = -(3.0 - g) / 2.0 if adm[nm]["admissible"] else None
        gaps[nm] = {
            "modulated": mod, "raw": raw,
            "rel_change": _rel(mod), "abs_change": _abs(mod),
            "predicted_concentration_limit": pred,
            "cond_G": [r["cond_G"] for r in recs],
            "dropped": [r["dropped"] for r in recs],
            "dim_trial": [r["dim_trial"] for r in recs],
        }
        print(f"    {nm:12s} mod " + " ".join(f"{v:+.6f}" for v in mod) +
              ("   pred %+.3f" % pred if pred is not None else "   pred n/a  ") +
              f"  cond(G) {recs[-1]['cond_G']:.3g}  dropped {recs[-1]['dropped']}")
    res["gaps"] = gaps

    # 3 -- THE GATE, evaluated per weight under both readings of (S)
    print("[3] the gate, per weight")
    verdicts = {}
    for nm, fam, g in WEIGHT_FAMILY:
        mod = gaps[nm]["modulated"]
        last2_rel = gaps[nm]["rel_change"][-2:]
        last2_abs = gaps[nm]["abs_change"][-2:]
        v = {
            "positive": mod[-1] > 0.0,
            "stable_relative": all(d <= TOL_STABILITY_REL for d in last2_rel),
            "stable_absolute": all(d <= TOL_STABILITY_ABS for d in last2_abs),
            "admissible": adm[nm]["admissible"],
        }
        v["gate_yes"] = v["positive"] and v["stable_relative"] and v["admissible"]
        v["gate_yes_under_absolute_reading"] = (
            v["positive"] and v["stable_absolute"] and v["admissible"])
        verdicts[nm] = v
        print(f"    {nm:12s} positive {str(v['positive']):5s}  stable_rel "
              f"{str(v['stable_relative']):5s}  stable_abs {str(v['stable_absolute']):5s}"
              f"  admissible {str(v['admissible']):5s}  -> "
              f"{'YES' if v['gate_yes'] else 'no'}")
    res["per_weight_verdict"] = verdicts

    # 4 -- IS THE ONE POSITIVE NUMBER A PROPERTY OF THE OPERATOR OR OF THE CODE?
    #      Sweep the QUADRATURE grading depth at fixed n.  An admissible weight must not
    #      move; a weight whose space is empty is finite only because the innermost panel
    #      is finite, and it moves.  (Lesson 86.)
    print("[4] quadrature-artifact sweep at fixed n = 64")
    art = {}
    for nm in ("A2", "A3"):
        fam, g = next((f, gg) for n_, f, gg in WEIGHT_FAMILY if n_ == nm)
        vals = [coercivity_gap(64, fam, g, n_grade=ng)["gap"] for ng in GRADE_LADDER]
        spread = (max(vals) - min(vals)) / max(abs(vals[-1]), 1e-300)
        art[nm] = {"gaps": vals, "relative_spread": spread}
        print(f"    {nm:12s} " + " ".join(f"{v:+.6f}" for v in vals) +
              f"   relative spread {spread:.3e}")
    res["quadrature_artifact_sweep"] = art

    # 5 -- THE POSITIVE CONTROL, which can report the other answer
    print("[5] positive control: L - mu*Lambda turns the shift into a multiplier")
    ctrl = {}
    for nm in ("A0_flat", "A2"):
        fam, g = next((f, gg) for n_, f, gg in WEIGHT_FAMILY if n_ == nm)
        vals = [coercivity_gap(64, fam, g, mu=mu)["gap"] for mu in MU_LADDER]
        ctrl[nm] = {"mu": list(MU_LADDER), "gaps": vals,
                    "sign_flips": vals[0] < 0 < vals[-1]}
        print(f"    {nm:12s} " + "  ".join(f"mu={m}:{v:+.5f}" for m, v in zip(MU_LADDER, vals)))
    res["positive_control"] = ctrl

    # 6 -- the external ceiling is respected at mu = 0 (instrument check, not a result)
    worst = max(gaps[nm]["modulated"][-1] for nm, _, g in WEIGHT_FAMILY if g < 3)
    res["ceiling_check"] = {"largest_admissible_modulated_gap": worst,
                            "ceiling": KNOWN_ANSWER_CEILING,
                            "respected": worst <= KNOWN_ANSWER_CEILING}

    # 7 -- the answer, in the gate's own wording
    any_yes = any(v["gate_yes"] for v in verdicts.values())
    res["gate_question"] = (
        "For at least one weight in the pre-named family, is the measured coercivity gap "
        "of the weighted-energy form on the a=0 CLM linearization positive and stable "
        "(within a pre-committed tolerance declared in the driver) across two grid "
        "refinements?")
    res["gate_answer"] = "YES" if any_yes else "NO"
    res["mechanism"] = (
        "The whole local part of the form is a multiplier by the damping factor "
        "D_phi(theta) = (3/2) cos theta + (1/2) sin theta (log phi)', whose value at the "
        "origin is (3 - gamma)/2 for both named families. Damping at the origin therefore "
        "needs gamma > 3. The basis is in L^2_phi only for gamma < 3. THE TWO THRESHOLDS "
        "ARE THE SAME NUMBER: the window does not merely fail to contain a good weight, it "
        "has ZERO WIDTH, closing at gamma = 3 where the weighted norm log-diverges. Every "
        "admissible member's measured gap converges to -(3 - gamma)/2, i.e. to minus the "
        "damping factor at the origin, by concentration there.")
    res["ceiling_S7"] = (
        "Measured on the a = 0 CLM linearisation: one mode, analytic, the friendliest "
        "object in the repository, and the same operator solver/spectral_certificate.py "
        "carries (checked matrix-for-matrix in test_energy_coercivity.py). A wall measured "
        "here bounds HL_S2_nonsymmetric's difficulty FROM BELOW, not above. Float64 "
        "throughout, nothing interval-enclosed. No stage is claimed under either branch "
        "and no link of the L1 -> L4 chain moves.")
    res["elapsed_s"] = time.time() - t0

    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)")
    print(f"GATE ANSWER: {res['gate_answer']}")


if __name__ == "__main__":
    main()
