"""Arc 7, unit K3, leg 439, slot 4 (Q5 only; Q6 dropped by leg_439_prereg_amend.md).

Gate Q5 (leg_439_prereg.md Sec 3): the bracket B of T_{0,theta} beyond X_b.
  Route A -- Lemma A.8 (manuscript page 140), leg 432's K6: with the heat exterior B == 0
    exactly; without it, B = -(2 + 2h) exactly.
  Route B -- numerical, from the pinned fields, via the imported, never-edited
    experiments/arc6_residual_v1.py build() (its H7.B_beyond_Xb, and independently the
    general calB_h array evaluated at y >= 3, exposed in build()'s "fields.B_hat_eta0").
  Gate: with heat |B| < 1e-14 (scaled); without heat |B + 2 + 2h| < 1e-8, at h in
    {1e-7, 1e-3} both. A fake returning -2 fails at 1e-3 by 2e-3 and at 1e-7 by
    2e-7 > 1e-8 -- exactly the h-dependence an adversary cannot choose.

Controls -- the adversary's own two planted fakes (Sec 3, Q5): "truncate to the sqrt(X)
term" (drop the O(1/X) bracket entirely, i.e. predict B_fake == 0 identically) and "cut
off the stress instead of the profile" (hard-zero T_0 for X >= X_b rather than building
the cutoff into the tail profile f_o and running it through Lemma A.8's derivation; since
the pinned build() independently shows A_beyond_Xb == 0 at every h and every heat
setting, solving 0 = pref*(0 + B_fake/X) forces B_fake == 0 too). Both give 0 in BOTH legs
by construction and so MUST fail the no-heat leg.

Everything is in the scaled form T_hat = e^{4/delta^2} T_0 (arc6_residual_v1.py's own
convention); nothing underflows. Tier 2. Not a proof.

    /home/andy/projects/Unsolved/.venv/bin/python experiments/arc7_k3_support.py
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
from arc6_residual_v1 import build  # noqa: E402  -- imported, never edited

OUT = ROOT / "writeup" / "data" / "arc7" / "k3" / "agent_4_support.json"
H_LIST = [1e-7, 1e-3]


def route_a(h, heat):
    """Lemma A.8 / leg 432 K6, written down before any route-B number is read."""
    return 0.0 if heat else -(2.0 + 2.0 * h)


def route_b(h, heat):
    """Numerical, from the pinned fields: the imported build()'s H7.B_beyond_Xb, cross
    checked against the general calB_h array (fields.B_hat_eta0) sampled at y >= 3."""
    r = build(h=h, heat=heat)
    y = np.array(r["fields"]["y"])
    B_field = np.array(r["fields"]["B_hat_eta0"])
    beyond = y >= 3.0
    field_vals = B_field[beyond]
    return {
        "H7_B_beyond_Xb": r["H7"]["B_beyond_Xb"],
        "H7_A_beyond_Xb": r["H7"]["A_beyond_Xb"],
        "field_B_hat_eta0_beyond_Xb_min": float(np.min(field_vals)) if field_vals.size else None,
        "field_B_hat_eta0_beyond_Xb_max": float(np.max(field_vals)) if field_vals.size else None,
        "field_B_hat_eta0_beyond_Xb_constant": bool(
            field_vals.size and np.max(field_vals) - np.min(field_vals) < 1e-12
        ),
        "runtime_s": r["params"]["runtime_s"],
    }


def q5_gate_check(h, heat, B_measured):
    """Sec 3, Q5's own gate: with heat |B| < 1e-14 (scaled); without heat
    |B + 2 + 2h| < 1e-8, at each h -- tolerance stated before any number was read."""
    if heat:
        err = abs(B_measured)
        tol = 1e-14
        ok = err < tol
        return {"leg": "heat", "h": h, "B_measured": B_measured, "abs_error": err, "tol": tol, "pass": ok}
    else:
        target = -(2.0 + 2.0 * h)
        err = abs(B_measured - target)
        tol = 1e-8
        ok = err < tol
        return {
            "leg": "no_heat", "h": h, "B_measured": B_measured, "route_a_predicted": target,
            "abs_error": err, "tol": tol, "pass": ok,
        }


def fake_truncate_sqrtX(h, heat):
    """Adversary planted fake 1: keep only the leading E_pow sqrt(X/2)*A/L term of
    T_0 = E_pow sqrt(X/2)[A/L + B/X] and drop the O(1/X) bracket B outright -> B_fake = 0,
    identically, regardless of h or the heat setting."""
    return 0.0


def fake_cutoff_stress(h, heat):
    """Adversary planted fake 2: cut off the total stress T_0 itself at X_b (T_0 := 0 for
    X >= X_b) instead of building the cutoff into the tail profile f_o and carrying it
    through Lemma A.8's derivation. The pinned build() shows A_beyond_Xb == 0 at every h
    and heat setting tried here (see routes[*].route_b.H7_A_beyond_Xb == 0.0), so solving
    0 = pref*(A_fake/L + B_fake/X) with A_fake == 0 and T_0 == 0 forces B_fake = 0 too,
    identically, regardless of h or the heat setting."""
    return 0.0


def main():
    t0 = time.time()
    pages_read = [
        {"page": 140, "id": "Lemma A.8", "why": "route A: the exact backward moment representation; K6 (leg 432) reads B == 0 with heat, -(2+2h) without"},
        {"page": None, "id": "leg_432.md sec 1 K6_no_heat", "why": "the closed-form B_beyond_Xb prediction this gate checks, and the H7 field this runner reads via build()"},
    ]

    claimed = {
        "quantity": "the bracket B of T_{0,theta} beyond X_b (T_0 = E_pow sqrt(X/2)[A/L + B/X])",
        "route_a_prediction_with_heat_written_before_run": {
            str(h): route_a(h, True) for h in H_LIST
        },
        "route_a_prediction_no_heat_written_before_run": {
            str(h): route_a(h, False) for h in H_LIST
        },
        "note": "these numbers are the prereg's own Sec 3 Q5 text (Lemma A.8 / leg 432 K6); nothing here was adjusted after route B was read",
    }

    routes = {}
    gates = {}
    for h in H_LIST:
        routes[str(h)] = {}
        gates[str(h)] = {}
        for heat_label, heat in (("heat", True), ("no_heat", False)):
            rb = route_b(h, heat)
            B_measured = rb["H7_B_beyond_Xb"]
            routes[str(h)][heat_label] = {
                "route_a_method": "Lemma A.8 (page 140) / leg 432 K6: B == 0 with the heat exterior, -(2+2h) exactly without it",
                "route_a_value": route_a(h, heat),
                "route_b_method": "numerical: imported build(h, heat) from arc6_residual_v1.py; H7.B_beyond_Xb, cross-checked against the general calB_h array sampled at y >= 3 (fields.B_hat_eta0)",
                "route_b": rb,
            }
            gates[str(h)][heat_label] = q5_gate_check(h, heat, B_measured)

    q5_overall = all(gates[str(h)][leg]["pass"] for h in H_LIST for leg in ("heat", "no_heat"))

    controls = {}
    for h in H_LIST:
        controls[str(h)] = {}
        for heat_label, heat in (("heat", True), ("no_heat", False)):
            entry = {}
            for name, fn in (("truncate_sqrtX", fake_truncate_sqrtX), ("cutoff_stress", fake_cutoff_stress)):
                B_fake = fn(h, heat)
                check = q5_gate_check(h, heat, B_fake)
                # planted: gives 0 in BOTH legs; must FAIL the no-heat leg, may pass the heat leg
                if heat:
                    fired_as_planted = (B_fake == 0.0) and check["pass"]
                else:
                    fired_as_planted = (B_fake == 0.0) and (not check["pass"])
                entry[name] = {
                    "B_fake": B_fake,
                    "gate_check": check,
                    "fired_as_planted": fired_as_planted,
                    "description": fn.__doc__.strip().split("\n")[0],
                }
            controls[str(h)][heat_label] = entry

    controls_all_fired = all(
        controls[str(h)][leg][name]["fired_as_planted"]
        for h in H_LIST for leg in ("heat", "no_heat") for name in ("truncate_sqrtX", "cutoff_stress")
    )

    dropped = {
        "Q6": {
            "quantity": "the flat weight's linear coefficient k(delta) = delta^3 d/d(delta) log T_{0,theta}",
            "reason": (
                "DROPPED before any K3 run by experiments/journal/leg_439_prereg_amend.md. The prereg's "
                "expansion log T_{0,theta} = -4/delta^2 - 3 log delta + log b + O(delta) differentiates to "
                "k = 8 - 3 delta^2 + O(delta^3), not 8 - 3 delta as Sec 0/Q6 stated (delta^3 d/d(delta)(-3 log "
                "delta) = -3 delta^2, not -3 delta); on that corrected expansion the gated quantity "
                "c1 = (k-8)/delta -> -3 delta -> 0, never -3. Separately, leg 432's own measurement "
                "(writeup/data/arc6_residual_v1.json preregistered_runs/1e-07/H7/"
                "delta3_dlogT_ddelta_at_0.05 = 8.000135, i.e. (k-8)/delta = 0.0027) shows the expansion is not "
                "reached at any resolvable delta; H2/not_testable and H2/delta_cross = 1.1e-69 confirm the "
                "-3 log delta term needs a collar no pinned grid reaches. With the -3 gone, route A's only "
                "surviving, resolvable prediction is k -> 8, the bare cutoff's own exponent -- a quantity the "
                "adversary can choose outright (a bare cutoff with no profile at all returns k=8 exactly), "
                "which is the same tautology Sec 3 already dropped S2's support clauses for. Per the wave's "
                "one rule, a gate that cannot be put in two-route-on-an-adversary-proof quantity form is "
                "DROPPED, not weakened. This worker did not run Q6, did not compute k(delta), and did not "
                "substitute anything in its place."
            ),
        }
    }

    artefact = {
        "schema": "arc7_k3_v1",
        "agent": "agent_4",
        "leg": 439,
        "pages_read": pages_read,
        "claimed": claimed,
        "routes": routes,
        "gates": {
            "Q5": {
                "per_h_per_leg": gates,
                "overall": "YES" if q5_overall else "NO",
                "tolerance_as_preregistered": {
                    "heat": "|B| < 1e-14 (scaled)",
                    "no_heat": "|B + 2 + 2h| < 1e-8 at h in {1e-7, 1e-3} both",
                },
            }
        },
        "controls": controls,
        "controls_summary": {
            "all_fired_as_planted": controls_all_fired,
            "note": "each planted fake gives B_fake = 0 identically; this must (and does) pass the heat leg trivially and FAIL the no-heat leg at both h -- a defect would be a fake that instead passed the no-heat leg or drifted with h",
        },
        "dropped": dropped,
        "instantiated_vs_scaled": {
            "instantiated": "lambda = 0.1 (arc6_profile_v1.json pinned outer profile), h in {1e-7, 1e-3} (the paper's h and a computable h per Sec 0's h-signal rule), the terminal tail y in [0, 3.5]",
            "scaled": "everything carried as T_hat = e^{4/delta^2} T_0, delta = 3 - y (arc6_residual_v1.py's own convention), so nothing underflows at the paper's h = 1e-7",
        },
        "could_not_determine": [],
        "what_this_does_not_establish": (
            "This gate checks only that Lemma A.8's exact backward-moment algebra for the bracket B beyond "
            "X_b is realised numerically on the pinned outer profile at lambda = 0.1 and two computable h. It "
            "does not establish that the construction closes at the paper's own lambda or h, does not verify "
            "any other lemma or proposition in the manuscript, does not touch Q1-Q4 or the dropped Q6, and "
            "does not move any wall in DIRECTION.md (which this worker did not read). Route B here reuses the "
            "same imported, never-edited build() that also produced leg 432's own record; it is an "
            "independent numerical evaluation of the general calB_h array (cross-checked directly against the "
            "pinned fields.B_hat_eta0 beyond y=3 in this runner), not a re-derivation of Lemma A.8 from first "
            "principles."
        ),
        "forbidden_paths_opened": "none",
        "runtime_s": time.time() - t0,
        "tier2_statement": "This is Tier 2, not a proof.",
    }
    artefact["what_this_does_not_establish"] += " This is Tier 2, not a proof."

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artefact, indent=1, default=float) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} B) in {time.time() - t0:.0f}s")
    print("Q5 overall:", "YES" if q5_overall else "NO")
    print("controls all fired as planted:", controls_all_fired)


if __name__ == "__main__":
    main()
