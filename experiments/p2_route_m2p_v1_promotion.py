#!/usr/bin/env python3
"""Route-M2P v1 -- leg 125: Chen's gamma = 2 dissipative gCLM candidate, promoted or not.

Discharges leg 63's three explicit debts, in its order:
  (i)   novelty pass FIRST -- committed separately, `writeup/novelty/leg_125.md`;
  (ii)  full-text read of arXiv:1908.09385, transcribed with provenance into
        `solver/dissipative_profile.CHEN_1908_09385`;
  (iii) the profile constructed numerically at >= 2 resolutions, and the FIRST Y_0
        measured against this pipeline's radii-polynomial budget.

THE GATE, pre-committed in DIRECTION.md and quoted verbatim in the report:
    "With Chen's theorem located and constants transcribed from the FULL TEXT, and the
     profile constructed at two or more resolutions, does Y_0 come in under the
     radii-polynomial budget at any tested resolution?"

Runs NO gCLM dynamics (`no_dynamics_run: true`) and sweeps NO dissipation parameter
(`nu_swept: false`) -- the stage-V tripwire.

    .venv/bin/python experiments/p2_route_m2p_v1_promotion.py
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.dissipative_profile import (  # noqa: E402
    CHEN_1908_09385, chen_gamma_tension, chen_known_answer, measure_chen_object,
    measure_viscous_object,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_m2p_v1_promotion.json")

RESOLUTIONS = (201, 401, 801, 1601)
WEIGHTS = (0.0, 1.0, 2.0)
NU_FIXED = 1.0            # FIXED.  Never swept.  See the tripwire note in the JSON.


def _jsonable(o):
    if isinstance(o, dict):
        return {k: _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return _jsonable(o.tolist())
    # np.generic covers np.bool_ as well as np.floating/np.integer -- `radii_polynomial`
    # returns numpy comparisons, and np.bool_ is NOT JSON serializable.
    if isinstance(o, np.generic):
        return _jsonable(o.item())
    if isinstance(o, float) and not np.isfinite(o):
        return str(o)
    return o


def main():
    res = {
        "leg": 125,
        "route": "M2P",
        "branch": "leg/m2p-v1",
        "no_dynamics_run": True,
        "nu_swept": False,
        "nu_fixed": NU_FIXED,
        "stage_claimed": None,
        "clay_progress": False,
        "clay_odds_unchanged": 0.0005,
        "honest_ceiling": (
            "NOT movement on L1->L4 and NOT Clay progress, whichever way the gate "
            "answers.  Only the novel-output sub-goal is in play."),
        "tripwire_stage_V": (
            "If the work drifts into floating a dissipation parameter against an existing "
            "certificate's margin, that IS stage V as posed -- stop and escalate.  It did "
            "not: nu is a FIXED constant here, there is no existing certificate whose "
            "margin could be floated, and LSS arXiv:2207.07548 sec 2 note nu is a pure "
            "gauge for this equation anyway ('By rescaling each of t and omega, we can "
            "eliminate nu from the problem')."),
        "gate_verbatim": (
            "With Chen's theorem located and constants transcribed from the FULL TEXT, and "
            "the profile constructed at two or more resolutions, does Y_0 come in under "
            "the radii-polynomial budget at any tested resolution?"),
    }

    # (ii) the transcription and the gamma tension, resolved from the located text
    res["chen_transcription"] = CHEN_1908_09385
    res["gamma_tension_resolved"] = chen_gamma_tension()

    # the known-answer gate: Chen's closed form against the discrete residual
    print("== known-answer gate: Chen (2.2) against the discrete residual ==")
    ka = [chen_known_answer(n=n) for n in RESOLUTIONS]
    for r in ka:
        print(f"  n={r['n']:5d}  residual_sup={r['residual_sup']:.4e}  "
              f"u_x(0) rel err={r['ux0_rel_error']:.3e}")
    orders = [float(np.log2(ka[i]["residual_sup"] / ka[i + 1]["residual_sup"]))
              for i in range(len(ka) - 1)]
    print(f"  observed convergence order: {['%.2f' % o for o in orders]}")
    res["known_answer_gate"] = {"rows": ka, "observed_order": orders}

    # (iii) Object A -- Chen's object as his text poses it
    print("\n== Object A: Chen's gamma=2 object (the profile is INVISCID, p.4) ==")
    A = []
    for n in RESOLUTIONS[:3]:
        for s in WEIGHTS:
            r = measure_chen_object(n=n, s=s)
            A.append(r)
            print(f"  n={r['n']:5d} s={s:.0f}  conv={str(r['newton_converged']):5s} "
                  f"res={r['final_residual_sup']:.2e}  c_l={r['c_l']:.9f} "
                  f"(|err| {r['c_l_abs_error']:.1e})  Y0={r['Y0']:.4e}  "
                  f"budget={r['budget']:.4e}  Y0/budget={r['Y0_over_budget']:.4e}  "
                  f"under={r['under_budget']}")
    res["object_A_chen"] = A

    # Object B -- the dissipative steady profile that WOULD have to exist
    print("\n== Object B: the gamma=2 DISSIPATIVE steady profile (nu fixed, never swept) ==")
    B = []
    for n in RESOLUTIONS[:3]:
        r = measure_viscous_object(n=n, nu=NU_FIXED, s=0.0)
        B.append(r)
        print(f"  n={r['n']:5d}  conv={str(r['newton_converged']):5s} "
              f"({r['newton_reason']})  res={r['final_residual_sup']:.3e}  "
              f"c_l={r['c_l']:.6g}  c_omega={r['c_omega']:.6g}  "
              f"dist to Chen={r['dist_to_chen_profile_rel']:.3e}  Y0={r['Y0']:.4e}  "
              f"Y0/budget={r['Y0_over_budget']:.4e}")
    res["object_B_viscous"] = B

    # THE a-NEIGHBOURHOOD.  Theorem 1.1 is stated for a in (1/2 - delta, 1/2 + delta) and
    # NEVER quantifies delta -- confirmed absent from the source, not merely unread.  At
    # a = 1/2 exactly Chen's profile is a CLOSED FORM, so a Y_0 there certifies an object
    # one can already write down.  Off a = 1/2 there is no closed form, and THAT is where
    # a Y_0 measurement carries information.  Varying `a` is varying the ADVECTION
    # parameter, not a dissipation parameter -- the stage-V tripwire is untouched.
    print("\n== the a-neighbourhood (no closed form off a = 1/2) ==")
    NB = []
    for a in (0.50, 0.48, 0.45, 0.40, 0.55, 0.60):
        for n in (401, 801):
            r = measure_chen_object(n=n, a=a, s=0.0)
            NB.append(r)
            print(f"  a={a:.2f} n={r['n']:5d}  conv={str(r['newton_converged']):5s} "
                  f"c_l={r['c_l']:.8f}  dist to Chen's closed form="
                  f"{r['dist_to_closed_form_rel']:.2e}  Y0={r['Y0']:.4e}  "
                  f"Y0/budget={r['Y0_over_budget']:.4e}  under={r['under_budget']}")
    res["a_neighbourhood"] = NB
    res["a_neighbourhood_note"] = (
        "delta is UNQUANTIFIED in arXiv:1908.09385 -- Theorem 1.1 asserts 'There exists "
        "delta > 0' and no numerical value appears anywhere in the text.  Any certificate "
        "attempt must supply its own delta; this leg measures the Y_0 landscape across a "
        "band rather than inheriting one.")

    # THE GATE
    under_A = [r for r in A if r["under_budget"]]
    under_B = [r for r in B if r["under_budget"]]
    best_A = min(A, key=lambda r: r["Y0_over_budget"])
    best_B = min(B, key=lambda r: r["Y0_over_budget"])
    res["gate"] = {
        "answer": "YES" if (under_A or under_B) else "NO",
        "n_rows_under_budget_A": len(under_A),
        "n_rows_under_budget_B": len(under_B),
        "best_A": {k: best_A[k] for k in ("n", "s", "Y0", "Z1", "Z2", "budget",
                                          "Y0_over_budget", "under_budget")},
        "best_B": {k: best_B[k] for k in ("n", "s", "Y0", "Z1", "Z2", "budget",
                                          "Y0_over_budget", "under_budget")},
        "gap_to_budget_decades_A": float(np.log10(best_A["Y0_over_budget"])),
        "gap_to_budget_decades_B": float(np.log10(best_B["Y0_over_budget"])),
    }

    # the leg-53 positive control, RE-READ rather than transferred
    res["leg53_control_reread"] = {
        "banked_number": 0.9156,
        "banked_claim_as_carried": "Z_1 = 0.9156 at mu = 2",
        "what_mu_actually_is": (
            "mu is the COEFFICIENT of Lambda^1 dissipation, not the exponent.  "
            "solver/spectral_certificate.py line 74: 'POSITIVE CONTROL: add `-mu k` to the "
            "diagonal (fractional dissipation `Lambda^1`...)', and lines 257/371 subtract "
            "`mu * k`.  So the control is gamma = 1 with coefficient 2."),
        "transfers_to_gamma_2": False,
        "why_not": (
            "Two independent mismatches.  (1) EXPONENT: the control is Lambda^1 "
            "(multiplier -mu k); this candidate is gamma = 2 (multiplier ~ -nu k^2).  "
            "(2) OBJECT: the control was measured on the a=0 CLM linearisation in the "
            "compactified coefficient basis at K=16, s=0.3, with the UNBORDERED tail -- "
            "and that anchor's Y_0 is exactly 0 for the banned degenerate reason.  "
            "Neither the operator nor the basis nor the anchor is this leg's."),
        "what_it_does_still_license": (
            "The narrow methodological point it was built for, which survives: a "
            "dissipative multiplier can bring an assembled Z_1 below 1, so a Z_1 above 1 "
            "is a measurement rather than a broken instrument.  That is a statement about "
            "the INSTRUMENT, not a constant this leg may reuse."),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(_jsonable(res), f, indent=1)
    print(f"\nwrote {OUT}")
    print(f"GATE: {res['gate']['answer']}   "
          f"best Y0/budget (A) {best_A['Y0_over_budget']:.4e} at n={best_A['n']}, "
          f"s={best_A['s']:.0f}; (B) {best_B['Y0_over_budget']:.4e}")
    build_figure()
    return res


# --------------------------------------------------------------------------
# the figure -- rebuilt from the COMMITTED JSON only, never from a re-run
# --------------------------------------------------------------------------
FIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "figures", "fig61_route_m2p_v1_promotion.png")


def build_figure(data_path=OUT, fig_path=FIG):
    """fig61 -- the three panels this leg's gate actually turns on.

    Registered nowhere else on purpose: `writeup/build_figures.py` is outside this leg's
    declared territory, so the one-line entry in its `P2_EVIDENCE` list is left as an
    integration step rather than taken here.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(open(data_path).read())
    plt.rcParams.update({"figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
                         "legend.frameon": False})
    fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.1))

    # (a) the known-answer gate and its 4th-order convergence
    ka = d["known_answer_gate"]["rows"]
    ns = [r["n"] for r in ka]
    ax[0].loglog(ns, [r["residual_sup"] for r in ka], "o-", color="#2563eb",
                 label="residual at Chen's closed form (2.2)")
    ref = ka[0]["residual_sup"] * (np.array(ns, float) / ns[0]) ** -4
    ax[0].loglog(ns, ref, "--", color="#6b7280", label="4th order reference")
    ax[0].set_xlabel("grid points n"); ax[0].set_ylabel("residual sup norm")
    ax[0].set_title("(a) KNOWN-ANSWER GATE\nChen (2.2) nulls the residual; observed orders "
                    + ", ".join(f"{o:.2f}" for o in d["known_answer_gate"]["observed_order"]),
                    fontsize=9.5)
    ax[0].legend(fontsize=8)

    # (b) Y_0 against budget, Object A vs Object B
    A = [r for r in d["object_A_chen"] if r["s"] == 0.0]
    B = d["object_B_viscous"]
    ax[1].loglog([r["n"] for r in A], [r["Y0"] for r in A], "o-", color="#059669",
                 label="Object A: $Y_0$ (Chen, inviscid profile)")
    ax[1].loglog([r["n"] for r in A], [r["budget"] for r in A], "s--", color="#059669",
                 alpha=0.5, label="Object A: budget $(1-Z_1)^2/2Z_2$")
    ax[1].loglog([r["n"] for r in B], [r["Y0"] for r in B], "o-", color="#dc2626",
                 label="Object B: $Y_0$ (viscous steady state)")
    ax[1].loglog([r["n"] for r in B], [r["budget"] for r in B], "s--", color="#dc2626",
                 alpha=0.5, label="Object B: budget")
    ax[1].set_xlabel("grid points n"); ax[1].set_ylabel("$Y_0$ and budget")
    _gapA = [np.log10(r["Y0_over_budget"]) for r in A]
    ax[1].set_title("(b) THE GATE (s=0)\nA is under budget by "
                    f"{-max(_gapA):.1f}-{-min(_gapA):.1f} decades; B has no steady state\n"
                    "to be under budget OF", fontsize=9.5)
    ax[1].legend(fontsize=7.5, loc="best")

    # (c) the a-neighbourhood: Y_0/budget off a = 1/2
    nb = [r for r in d["a_neighbourhood"] if r["n"] == max(x["n"] for x in d["a_neighbourhood"])]
    nb.sort(key=lambda r: r["a"])
    ok = [r for r in nb if r["newton_converged"]]
    bad = [r for r in nb if not r["newton_converged"]]
    if ok:
        ax[2].semilogy([r["a"] for r in ok], [r["Y0_over_budget"] for r in ok], "o-",
                       color="#2563eb", label="Newton converged")
    if bad:
        ax[2].semilogy([r["a"] for r in bad], [r["Y0_over_budget"] for r in bad], "x",
                       color="#dc2626", ms=9, label="Newton did NOT converge")
    ax[2].axhline(1.0, color="#111", lw=1.0)
    ax[2].axvline(0.5, color="#6b7280", ls=":", lw=1.0)
    ax[2].text(0.5, ax[2].get_ylim()[1], " a=1/2 (closed form)", fontsize=7.5,
               va="top", color="#6b7280")
    ax[2].set_xlabel("advection parameter a"); ax[2].set_ylabel("$Y_0$ / budget")
    ax[2].set_title("(c) THE a-NEIGHBOURHOOD\nChen's $\\delta$ is UNQUANTIFIED in the "
                    "source;\nbelow 1 = under budget", fontsize=9.5)
    ax[2].legend(fontsize=8)

    fig.suptitle("Route-M2P (leg 125): Chen's $\\gamma=2$ gCLM candidate — the profile at "
                 "$\\gamma=2$ is the INVISCID closed form, and it clears the budget; "
                 "no dissipative steady profile exists to certify",
                 fontweight="bold", y=1.02, fontsize=10.5)
    fig.tight_layout()
    os.makedirs(os.path.dirname(fig_path), exist_ok=True)
    fig.savefig(fig_path, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {fig_path}")


if __name__ == "__main__":
    main()
