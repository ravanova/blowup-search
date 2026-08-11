"""Route-DSSP-B2 (leg 350) -- EVIDENCE + FIGURE.

Reads writeup/data/p2_route_dsspb2_v1.json (produced by
experiments/p2_route_dsspb2_v1.py). Plots the mode-count-vs-kappa curve for
leg 313's plain-Chebyshev baseline against this leg's enriched-basis
measurement, both at the identical 1e-6 truncation. Warranted as a NEW
measurement (the enriched-basis cost curve had never been computed or
plotted by any prior leg) -- not a replot of an already-banked number.

Nothing is recomputed here; the script only asserts the banked JSON supports
the claims made about it, same discipline fig89/fig91's evidence scripts use.

python3 writeup/figures/fig92_route_dsspb2_v1_enrichment.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb2_v1.json")
FIG = os.path.join(HERE, "fig92_route_dsspb2_v1_enrichment.png")

CHECKS = []


def check(name, ok, detail):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


def main():
    with open(DATA) as fh:
        d = json.load(fh)

    baseline = d["step1_full_baseline_table_reproduced"]["rows"]
    enriched = d["step2_enriched_basis"]["rows"]
    factors = d["step6_enrichment_factor"]["per_kappa"]

    kappas = sorted(float(k) for k in baseline)
    # JSON keys are stored as e.g. "1.0"
    base_n = [baseline[str(k)] for k in kappas]
    enr_n = [enriched[str(k)] for k in kappas]

    check("data has the five measured kappa rows on both curves",
          len(kappas) == 5, f"kappas={kappas}")
    check("gate answer recorded in the JSON is YES",
          d["gate_answer"] == "YES", d["gate_answer"])
    check("every enriched row is below its baseline row (what the plot must show)",
          all(e < b for e, b in zip(enr_n, base_n)),
          f"enriched={enr_n} vs baseline={base_n}")

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.loglog(kappas, base_n, "o-", color="#c0392b", linewidth=2, markersize=7,
              label="plain Chebyshev (leg 313 baseline)")
    ax.loglog(kappas, enr_n, "s-", color="#2471a3", linewidth=2, markersize=7,
              label="enriched compactified basis (leg 350, L=16 fixed)")
    ax.axhline(d["step0_smooth_control_reproduced_first"]["plain_X_smooth_modes_1e-6"],
               color="#7f8c8d", linestyle="--", linewidth=1.2,
               label="smooth control, plain-X (10 modes)")

    for kap, b, e in zip(kappas, base_n, enr_n):
        ax.annotate(f"{factors[str(kap)]:.1f}x", xy=(kap, e),
                    xytext=(0, -14), textcoords="offset points",
                    ha="center", fontsize=8, color="#2471a3")

    ax.set_xlabel(r"log-periodic frequency $\kappa$")
    ax.set_ylabel(r"modes needed for $10^{-6}$ relative truncation of $(1-X)^{1-i\kappa}$")
    ax.set_title("Route-DSSP brick B2: enriched basis vs leg 313's plain-Chebyshev\n"
                  "baseline, same target function, same 1e-6 truncation, single fixed L")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG, dpi=150)

    n_pass = sum(1 for _, r, _ in CHECKS if r == "PASS")
    for name, res, detail in CHECKS:
        print(f"{res} {name} :: {detail}")
    print(f"\n{n_pass}/{len(CHECKS)} checks pass -> {FIG}")
    return 0 if n_pass == len(CHECKS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
