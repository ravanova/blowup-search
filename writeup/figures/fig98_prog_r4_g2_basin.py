"""fig98 -- PROG-R4 unit U4, gate G2: the Newton basin around a recovered
Lucas & Kerswell Table IV relative periodic orbit.

Correct in BOTH pre-committed branches of G2. Panel A is the success fraction
p(eps) with the two planted controls drawn on the same axis, so a ragged
(non-monotone) p reads as the measurement it is rather than as a missing
boundary; panel B shows every individual run's final residual against its
perturbation size, which is where the mechanism of any failure is visible; panel
C shows how far off-orbit the converged runs landed, separating "Newton failed"
from "Newton succeeded onto something else".

Checks assert the banked JSON supports every claim. Non-zero exit on any
failure.

Data: writeup/data/p2_prog_r4_g2_v1.json
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g2_v1.json")
FIG = os.path.join(HERE, "fig98_prog_r4_g2_basin.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail
                                                    else ""))
    return bool(ok)


def main():
    with open(DATA) as f:
        d = json.load(f)

    rungs = d["rungs"]
    eps = np.array([r["eps"] for r in rungs], float)
    p = np.array([r["success_fraction"] for r in rungs], float)
    runs = [r for r in d["runs"] if r["kind"] == "sweep"]
    tol = float(d["resourcing"]["tol"])
    answer = d["gate"]["answer"]

    # ---- checks ---------------------------------------------------------
    check("gate answer is one of the two pre-committed branches",
          answer in ("YES", "NO"), f"answer={answer}")
    check("gate answer is exactly the conjunction it claims",
          (answer == "YES") == bool(d["gate"]["monotone"]
                                    and d["gate"]["bracketed"]
                                    and d["gate"]["controls_fired_as_planted"]),
          f"monotone={d['gate']['monotone']}, "
          f"bracketed={d['gate']['bracketed']}, "
          f"controls={d['gate']['controls_fired_as_planted']}")
    check("monotone flag agrees with the banked p(eps)",
          d["gate"]["monotone"] == bool(np.all(np.diff(p) <= 1e-12)))
    check("violation list length agrees with the monotone flag",
          bool(d["gate"]["monotonicity_violations"]) != d["gate"]["monotone"])
    check("planted success control converged onto the orbit",
          d["controls"]["planted_success"]["same_orbit"] is True)
    check("planted failure control did NOT land on the orbit",
          d["controls"]["planted_failure"]["same_orbit"] is False,
          "an unrelated turbulent snapshot at the same (T*,s*)")
    check("planted failure really is far from the orbit",
          float(d["controls"]["planted_failure_distance_from_orbit"]) > 0.1,
          f"rel. distance after optimal shift = "
          f"{d['controls']['planted_failure_distance_from_orbit']:.4f}")
    check("orbit under test is a NAMED published orbit",
          d["orbit"]["source"].startswith("Lucas & Kerswell 2015")
          and d["orbit"]["provenance"].endswith("(gate G1 = YES)"),
          d["orbit"]["anchor"])
    check("orbit was actually converged to tol at recovery",
          float(d["orbit"]["final_residual_at_recovery"]) <= tol)
    check("radius bracket is ordered when one exists",
          d["radius"]["largest_eps_with_all_directions_returning"] is None
          or d["radius"]["smallest_eps_with_no_direction_returning"] is None
          or (d["radius"]["largest_eps_with_all_directions_returning"]
              < d["radius"]["smallest_eps_with_no_direction_returning"]))
    check("every rung has the full direction budget",
          len({r["n_trials"] for r in rungs}) == 1
          and rungs[0]["n_trials"] == d["resourcing"]["n_directions"],
          f"{rungs[0]['n_trials']} directions x {len(rungs)} rungs")
    check("CLAY_OBLIGATIONS section 4 carried OPEN in this gate",
          any("section 4" in s and "OPEN" in s
              for s in d["open_obligations_carried"]))
    check("ceiling stays Tier 2 and no Clay movement asserted",
          d["ceiling"] == "Tier 2" and d["clay_movement"].startswith("none"))

    lo = d["radius"]["largest_eps_with_all_directions_returning"]
    hi = d["radius"]["smallest_eps_with_no_direction_returning"]

    # ---- figure ---------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.6))

    ax = axes[0]
    ax.semilogx(eps, p, "o-", color="#2b6cb0", lw=1.5, ms=6,
                label="fraction returning to the orbit")
    if lo is not None and hi is not None:
        ax.axvspan(lo, hi, color="#f6ad55", alpha=0.25,
                   label="bracket: last all-return -> first none-return\n"
                         "(a bracket alone is NOT a coherent boundary)")
    for v in d["gate"]["monotonicity_violations"]:
        ax.plot(v["eps"], v["p"], "x", ms=11, color="#c53030",
                label="monotonicity violation"
                if v is d["gate"]["monotonicity_violations"][0] else None)
    ax.plot(1e-5, 1.0 if d["controls"]["planted_success"]["same_orbit"] else 0.0,
            "^", ms=9, color="#2f855a", label="planted success (eps=0)")
    ax.plot(float(d["controls"]["planted_failure_distance_from_orbit"]),
            1.0 if d["controls"]["planted_failure"]["same_orbit"] else 0.0,
            "v", ms=9, color="#c53030", label="planted failure (foreign state)")
    ax.set_xlabel(r"perturbation $\varepsilon$ (relative to $\|w^*\|$)")
    ax.set_ylabel("success fraction")
    ax.set_ylim(-0.06, 1.06)
    ax.set_title(f"A. failure boundary  (G2 = {answer})")
    ax.legend(fontsize=7, loc="lower left")
    ax.grid(alpha=0.3, which="both")

    ax = axes[1]
    for lab, sel, col in (("returned to the orbit",
                           lambda r: r["same_orbit"], "#2f855a"),
                          ("converged elsewhere",
                           lambda r: r["converged"] and not r["same_orbit"],
                           "#d69e2e"),
                          ("did not converge",
                           lambda r: not r["converged"], "#c53030")):
        xs = [r["eps"] for r in runs if sel(r)]
        ys = [r["final_residual"] for r in runs if sel(r)]
        if xs:
            ax.loglog(xs, ys, "o", ms=4, alpha=0.7, color=col,
                      label=f"{lab} ({len(xs)})")
    ax.axhline(tol, color="k", ls="--", lw=1.2, label=f"tol = {tol:g}")
    if lo is not None and hi is not None:
        ax.axvspan(lo, hi, color="#f6ad55", alpha=0.2)
    ax.set_xlabel(r"perturbation $\varepsilon$")
    ax.set_ylabel(r"final $\|R\|$")
    ax.set_title("B. every run, by outcome")
    ax.legend(fontsize=7, loc="lower right")
    ax.grid(alpha=0.3, which="both")

    ax = axes[2]
    conv = [r for r in runs if r["converged"]
            and r["field_rel_after_shift"] is not None]
    if conv:
        ax.loglog([r["eps"] for r in conv],
                  [max(r["field_rel_after_shift"], 1e-16) for r in conv],
                  "o", ms=4, alpha=0.7, color="#2b6cb0")
    ax.axhline(float(d["match_criterion"]
                     ["match_field_tol_after_optimal_shift"]),
               color="k", ls="--", lw=1.2, label="same-orbit criterion")
    ax.set_xlabel(r"perturbation $\varepsilon$")
    ax.set_ylabel(r"$\|w_{\rm final}-w^*\|/\|w^*\|$ after optimal shift")
    ax.set_title("C. where the converged runs landed")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3, which="both")

    fig.suptitle(
        "fig98  PROG-R4 U4 / gate G2: Newton basin around recovered orbit "
        f"{d['orbit']['anchor']} (T*={d['orbit']['T']:.4f}, "
        f"s*={d['orbit']['s']:.4f}), Re=60, N=24", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG, dpi=150)
    print(f"wrote {FIG}")

    bad = [n for n, ok, _ in CHECKS if not ok]
    print(f"\n{len(CHECKS) - len(bad)}/{len(CHECKS)} checks passed")
    if bad:
        print("FAILED: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
