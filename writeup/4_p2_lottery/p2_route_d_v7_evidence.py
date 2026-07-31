"""Phase-2 P2 Route-D v7 (fig25) evidence: the domain seminorm part of ||A||,
closed by a derivative gain -- and what the honest ||A|| costs.

v6 bounded three of the eight Newton-Kantorovich constants and named three gaps.
This leg closes the one it called sharpest, and the route that worked is not the
one v6 recommended: the J^gamma lossiness was never a question about which unit
ball one optimizes over, it was a near-diagonal artifact of pricing two rows of
an inverse independently.  Using the EQUATION instead -- neighbouring rows differ
by a derivative -- gives a bound with no J in it at all.  Level-1 tooling +
upper bounds, NOT a certificate; Clay odds unchanged.

Rebuilds fig25 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v7_evidence.py
Regenerate the underlying data (deterministic; ~15 min):
    .venv/bin/python experiments/p2_route_d_v7_seminorm.py

Six panels (fig25):
  A. WHERE THE J^gamma LIVES (V1).  v6's dual bound on the seminorm part, taken
     over pairs separated by at least Delta in theta.  Over all pairs it grows
     like J^+0.49 = J^gamma; excluding a FIXED theta-separation of 0.05 leaves
     J^+0.05, and 0.1 leaves J^+0.02.  All of the growth is on the near diagonal.
  B. THE SPLIT HILBERT BOUND (V2).  v6 charged |H(h)| to the total norm; keeping
     the sup-paid and seminorm-paid halves apart is exact (they sum to v6's bound
     to 2e-16) and strictly sharper for every element whose norm is not evenly
     divided -- worth ~30% on the closure.
  C. THE CLOSURE (V3).  The new bound on the seminorm part is 63.6 and does not
     move with J (the only J-dependence is inherited from v6's C_sup, which
     saturates); v6's dual bound on the same quantity runs 17 -> 34 over the same
     range.  The family lower bound (0.82-0.85) shows the remaining slack: the
     bracket is real but wide.
  D. THE (alpha, gamma) MAP (V4).  ||A|| alone falls monotonically as gamma -> 0
     -- a weaker domain norm is easier to bound -- so it must not be optimized
     alone.  Z2 = 2||A||C_Q, the quantity the budget sees, BOWLS in both knobs
     with an interior optimum at (1.4, 0.15): the first interior optimum in this
     project built entirely out of upper bounds.
  E. WHAT THE HONEST ||A|| COSTS (V5).  Replacing v6's far-field proxy 2/(2-alpha)
     by the real bound (10-20x larger) pushes the far-field matching radius from
     ~1e2 to 2e3-3e4 and costs the conditional budget an order of magnitude
     (2.8e-3 -> 2.0e-4).  The radius is still inside what the existing dense
     collocation can reach; the budget is now well BELOW the GA residual floor.
  F. THE INTERPOLANT DEFECT (V6).  A band-limited h is a trigonometric polynomial
     in theta with h(pi) != 0, while the decay weight sec^alpha(theta/2) diverges
     there: sup w_alpha|h| is INFINITE at every J.  The discrete norms of v1..v7
     are finite only because the midpoint grid stops half a step short of pi.
     h(pi) itself falls like J^-3.0, so the defect is soft -- but it is a change
     of ansatz, not a small correction.
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
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_route_d_v7_seminorm.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "alt": "#7b3294"}


def build_figure():
    d = json.loads(JSON.read_text())
    v1, v2, v3 = d["v1_near_diagonal"], d["v2_split"], d["v3_closure"]
    v4, v5, v6 = d["v4_map"], d["v5_price"], d["v6_interpolant"]

    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.4))

    # -- A: where the J^gamma lives -------------------------------------
    a = ax[0, 0]
    Js = [r["J"] for r in v1["ladder"]]
    seps = [x["separation"] for x in v1["ladder"][0]["by_separation"]]
    cols = [C["bad"], C["warn"], C["anchor"], C["good"]]
    for i, s in enumerate(seps):
        vals = [r["by_separation"][i]["dual_bound"] for r in v1["ladder"]]
        e = v1["growth_exponent_by_separation"][str(s)]
        a.plot(Js, vals, "o-", color=cols[i % len(cols)],
               label=(f"all pairs  (J^{e:+.2f})" if s == 0
                      else f"|d(theta)| >= {s}  (J^{e:+.2f})"))
    a.set_xscale("log")
    a.set_yscale("log")
    a.set_xlabel("J")
    a.set_ylabel("dual bound on the seminorm part")
    a.set_title("A. the J^gamma is a NEAR-DIAGONAL artifact\n"
                "(v6's own bound, restricted to separated pairs)", fontsize=10)
    a.legend(fontsize=7.5, loc="upper left")
    a.grid(alpha=0.3, which="both")

    # -- B: the split ---------------------------------------------------
    b = ax[0, 1]
    X = np.array(v2["X"])
    b.loglog(X, v2["v6_total"], color=C["grey"], lw=2.2,
             label="v6: charged to the total norm")
    b.loglog(X, v2["a_sup"], color=C["anchor"], lw=1.8,
             label="a_sup  (paid by the sup part)")
    b.loglog(X, v2["a_semi"], color=C["good"], lw=1.8, ls="--",
             label="a_semi (paid by the seminorm)")
    b.set_xlabel("X")
    b.set_ylabel("bound on |H(h)(X)| per unit of each part")
    b.set_title(f"B. splitting the Hilbert bound is free\n"
                f"(a_sup + a_semi = v6's bound to "
                f"{v2['identity_max_rel_error']:.0e})", fontsize=10)
    b.legend(fontsize=8)
    b.grid(alpha=0.3, which="both")

    # -- C: the closure --------------------------------------------------
    c = ax[0, 2]
    L = v3["ladder"]
    Jl = [r["J"] for r in L]
    c.plot(Jl, [r["T_upper"] for r in L], "o-", color=C["good"], lw=2.2,
           label="NEW: derivative-gain closure (UB)")
    du = [(r["J"], r["dual_seminorm_upper"]) for r in L
          if r["dual_seminorm_upper"] is not None]
    c.plot([x[0] for x in du], [x[1] for x in du], "s--", color=C["bad"],
           label="v6: two-point dual (UB, ~J^gamma)")
    c.plot(Jl, [r["C_sup_upper"] for r in L], "^-", color=C["anchor"],
           label="v6: sup part (UB, saturates)")
    c.plot(Jl, [r["family_seminorm_lower"] for r in L], "v-", color=C["grey"],
           label="family extremizer (LOWER bound)")
    c.set_xscale("log")
    c.set_yscale("log")
    c.set_xlabel("J")
    c.set_ylabel("seminorm part of ||A||")
    c.set_title(f"C. the closure is J-free\n"
                f"(||A|| <= {L[0]['A_upper']:.1f}; bracket still ~"
                f"{L[0]['T_upper']/L[0]['family_seminorm_lower']:.0f}x wide)",
                fontsize=10)
    c.legend(fontsize=7.5, loc="center left")
    c.grid(alpha=0.3, which="both")

    # -- D: the (alpha, gamma) map ---------------------------------------
    dd = ax[1, 0]
    gam = [x["gamma"] for x in v4["map"][0]["row"]]
    show = [1.2, 1.4, 1.6, 1.8]
    for row in v4["map"]:
        if row["alpha"] not in show:
            continue
        dd.plot(gam, [x["Z2"] for x in row["row"]], "o-",
                label=f"alpha = {row['alpha']}")
    az = v4["argmin_Z2"]
    dd.plot([az["gamma"]], [az["Z2"]], "*", ms=19, color="black", zorder=5,
            label=f"interior optimum ({az['alpha']}, {az['gamma']})")
    dd.set_xlabel("gamma (smoothness grading)")
    dd.set_ylabel("Z2 = 2 ||A|| C_Q   (all upper bounds)")
    dd.set_yscale("log")
    dd.set_title("D. the objective BOWLS in both knobs\n"
                 "(||A|| alone would run to gamma = 0)", fontsize=10)
    dd.legend(fontsize=7.5)
    dd.grid(alpha=0.3, which="both")

    # -- E: what the honest ||A|| costs ----------------------------------
    e = ax[1, 1]
    al = [r["alpha"] for r in v5["rows"]]
    e.semilogy(al, [r["Y0_max_v6_proxy"] for r in v5["rows"]], "s--",
               color=C["grey"], label="v6: ||A|| ~ far-field proxy")
    e.semilogy(al, [r["Y0_max_honest"] for r in v5["rows"]], "o-",
               color=C["bad"], lw=2.2, label="v7: honest ||A|| upper bound")
    e.axhline(1e-2, color=C["anchor"], ls=":", lw=1.6)
    e.text(al[0], 1.15e-2, "GA residual floor (~1e-2)", fontsize=7.5,
           color=C["anchor"])
    e2 = e.twinx()
    e2.semilogy(al, [(r["required_X0_honest"]["X0"]
                      if r["required_X0_honest"]["found"] else np.nan)
                     for r in v5["rows"]], "^-", color=C["good"], alpha=0.85)
    e2.set_ylabel("X0 needed for Z1 <= 0.5", color=C["good"], fontsize=9)
    e2.tick_params(axis="y", colors=C["good"])
    e.set_xlabel("alpha (decay grading)")
    e.set_ylabel("conditional budget Y0_max")
    e.set_title("E. pricing the real ||A|| costs an order of magnitude\n"
                "(and the budget drops below the GA floor)", fontsize=10)
    e.legend(fontsize=7.5, loc="lower right")
    e.grid(alpha=0.3, which="both")

    # -- F: the interpolant defect ---------------------------------------
    f = ax[1, 2]
    Jv = [r["J"] for r in v6["ladder"]]
    f.loglog(Jv, [r["weighted_at_last_node"] for r in v6["ladder"]], "o-",
             color=C["anchor"], label="w|h| at the LAST GRID NODE (what we measure)")
    f.loglog(Jv, [r["weighted_near_pi"] for r in v6["ladder"]], "s-",
             color=C["bad"], label="w|h| at theta = pi - 1e-6 (the same function)")
    f.loglog(Jv, [abs(r["h_pi"]) for r in v6["ladder"]], "^--", color=C["grey"],
             label=f"|h(pi)|  ~ J^{v6['h_pi_growth_exponent']:.1f}")
    f.set_xlabel("J")
    f.set_ylabel("weighted value")
    f.set_title("F. the interpolant is not in the space\n"
                "(sup w|h| is INFINITE at every J)", fontsize=10)
    f.legend(fontsize=7.5, loc="lower left")
    f.grid(alpha=0.3, which="both")

    fig.suptitle(
        "P2 Route-D v7 (fig25): the domain seminorm part of ||A|| is bounded, "
        "J-free -- and the honest ||A|| costs the budget an order of magnitude.  "
        "Level-1 tooling + upper bounds, NOT a certificate.", fontsize=11.5)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig25_route_d_v7_seminorm.png"
    fig.savefig(out, dpi=145)
    plt.close(fig)
    return out


def summary():
    d = json.loads(JSON.read_text())
    L = d["v3_closure"]["ladder"]
    az = d["v4_map"]["argmin_Z2"]
    print("Route-D v7 -- the domain seminorm part, closed")
    print(f"  V1  J^gamma is near-diagonal: all pairs J"
          f"{d['v1_near_diagonal']['growth_exponent_by_separation']['0.0']:+.3f}"
          f" -> separated (0.1) J"
          f"{d['v1_near_diagonal']['growth_exponent_by_separation']['0.1']:+.3f}")
    print(f"  V2  split exact to {d['v2_split']['identity_max_rel_error']:.1e}")
    print(f"  V3  seminorm part <= {L[0]['T_upper']:.2f}, ||A|| <= "
          f"{L[0]['A_upper']:.2f}, growth J"
          f"{d['v3_closure']['A_upper_growth_exponent']:+.4f}")
    print(f"  V4  Z2 optimum {az['Z2']:.1f} at (alpha, gamma) = "
          f"({az['alpha']}, {az['gamma']})")
    print(f"  V5  budget {d['v5_price']['rows'][-1]['Y0_max_v6_proxy']:.1e} "
          f"(v6 proxy) -> {d['v5_price']['rows'][-1]['Y0_max_honest']:.1e} (honest)")
    print(f"  V6  h(pi) ~ J^{d['v6_interpolant']['h_pi_growth_exponent']:.2f}; "
          f"the weighted sup is infinite at every J")


if __name__ == "__main__":
    out = build_figure()
    summary()
    print(f"\n[done] wrote {out.relative_to(ROOT)}")
