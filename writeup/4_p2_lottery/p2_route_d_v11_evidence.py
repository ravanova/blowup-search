"""Phase-2 P2 Route-D v11 (fig29): Newton on the two-scale profile.

The other side of the inequality.  v10 measured that sharpening the constants
cannot close the gap; Y0 -- the profile's defect -- had never been attacked, and
every a != 0 profile in this project carried ~1e-2 because it came from a GA over
a small genome or from fixed-grid relaxation.  Level-1 tooling + a structural
positive, NOT a certificate.

Rebuilds fig29 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v11_evidence.py
Regenerate the data (deterministic; ~25 min):
    .venv/bin/python experiments/p2_route_d_v11_anchor.py

Four panels: A the a-sweep against the GA floor; B the grid test that decides
which of those solutions are continuum objects; C the WEIGHTED defect, which is
what the certificate actually sees and which behaves quite differently; D where
Y0 now sits against the budget.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
JSON = DATA / "p2_route_d_v11_anchor.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    v2, v3, v4, v5 = d["v2_sweep"], d["v3_boundary"], d["v4_grids"], d["v5_budget"]
    fig, ax = plt.subplots(2, 2, figsize=(13.5, 9.0))

    a = ax[0, 0]
    A = [r["a"] for r in v2["rows"]]
    a.semilogy(A, [max(r["relres"], 1e-16) for r in v2["rows"]], "o-",
               color=C["good"], lw=2.2, label="Newton (no genome)")
    a.axhline(v2["GA_floor"], color=C["bad"], ls="--", lw=2.0,
              label="GA / relaxation floor (~1e-2)")
    a.axvline(v4["grid_converged_a_max"], color=C["anchor"], ls=":", lw=1.6,
              label="grid-converged up to a = %.2f" % v4["grid_converged_a_max"])
    a.set_xlabel("a  (advection strength)")
    a.set_ylabel("relative residual")
    a.set_title("A. the 1e-2 floor was the SEARCH, not the equation\n"
                "(best %.0e -- %.0f orders below it)"
                % (v2["best_relres"], v2["orders_below_GA"]), fontsize=10)
    a.legend(fontsize=8)
    a.grid(alpha=0.3, which="both")

    b = ax[0, 1]
    ver = v4["verdict"]
    xs = np.arange(len(ver))
    b.bar(xs - 0.2, [max(v["c_spread"], 1e-6) for v in ver], width=0.4,
          color=C["anchor"], label="spread in c across n")
    b.bar(xs + 0.2, [max(abs(v["Omega_at_X4_spread"]), 1e-6) for v in ver],
          width=0.4, color=C["warn"], label="spread in Omega(X=4)")
    b.axhline(1e-3, color=C["bad"], ls="--", lw=1.5, label="convergence cut")
    b.set_xticks(xs)
    b.set_xticklabels(["a=%.1f\n%s" % (v["a"], "OK" if v["grid_converged"]
                                       else "NO") for v in ver], fontsize=8)
    b.set_yscale("log")
    b.set_title("B. the test that decides: is it a CONTINUUM object?\n"
                "(machine precision alone proves nothing)", fontsize=10)
    b.legend(fontsize=8)
    b.grid(alpha=0.3, axis="y", which="both")

    c = ax[1, 0]
    ok = [r for r in v2["rows"] if r["a"] <= v4["grid_converged_a_max"]
          and r["relres"] < 1e-8]
    c.semilogy([r["a"] for r in ok], [r["relres"] for r in ok], "o-",
               color=C["good"], lw=2.0, label="RMS residual")
    c.semilogy([r["a"] for r in ok], [r["weighted_defect"] for r in ok], "s-",
               color=C["bad"], lw=2.2, label="WEIGHTED defect (what Y0 is)")
    c.axhline(v5["Y0_max_from_v10"], color=C["anchor"], ls="--", lw=1.8,
              label="budget Y0_max = %.1e" % v5["Y0_max_from_v10"])
    c.set_xlabel("a")
    c.set_ylabel("defect")
    c.set_title("C. the weighted defect is a DIFFERENT quantity\n"
                "(6+ orders larger, and not uniformly under the budget)",
                fontsize=10)
    c.legend(fontsize=8)
    c.grid(alpha=0.3, which="both")

    dd = ax[1, 1]
    wd = [r["weighted_defect"] for r in ok]
    names = ["GA / relaxation\n(RMS)", "Newton\n(RMS)", "Newton\n(weighted, typ.)",
             "budget\nY0_max"]
    vals = [v5["GA_floor_rms"], v2["best_relres"],
            float(np.median(wd)), v5["Y0_max_from_v10"]]
    dd.bar(names, vals, color=[C["bad"], C["good"], C["warn"], C["anchor"]],
           width=0.55)
    for i, v in enumerate(vals):
        dd.text(i, v * 1.6, "%.0e" % v, ha="center", fontsize=9)
    dd.set_yscale("log")
    dd.set_ylabel("defect")
    dd.set_title("D. Y0 is no longer SEARCH-limited\n"
                 "-- it is now DISCRETIZATION-limited", fontsize=10)
    dd.grid(alpha=0.3, axis="y", which="both")

    fig.suptitle("Route-D v11 -- Newton on the two-scale profile: the 1e-2 "
                 "residual floor was the search, the survival boundary is real, "
                 "and Y0's limit moves to discretization "
                 "(Level-1 tooling, NOT a certificate)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    out = FIGS / "fig29_route_d_v11_anchor.png"
    fig.savefig(out, dpi=145)
    plt.close(fig)
    return out


if __name__ == "__main__":
    out = build_figure()
    d = json.loads(JSON.read_text())
    print("Route-D v11 -- Newton on the profile")
    print("  V2  best relres %.1e (%.0f orders below the GA floor)"
          % (d["v2_sweep"]["best_relres"], d["v2_sweep"]["orders_below_GA"]))
    print("  V4  grid-converged up to a = %.2f"
          % d["v4_grids"]["grid_converged_a_max"])
    print("  V5  weighted defect %.1e .. %.1e vs budget %.1e"
          % (d["v5_budget"]["newton_weighted_defect_min"],
             d["v5_budget"]["newton_weighted_defect_max"],
             d["v5_budget"]["Y0_max_from_v10"]))
    print(f"\n[done] wrote {out.relative_to(ROOT)}")
