"""Route-M2CI v1 (leg 187) — EVIDENCE: every number the prose quotes, re-derived from
`writeup/data/p2_route_m2ci_v1_construction.json`. Also builds
`writeup/figures/fig65_route_m2ci_v1_construction.png`.

Nothing expensive is recomputed: this reads the curated JSON and asserts the relations the
BLOG and TECHNICAL write-ups assert, so a reader can check the prose without re-running the
construction.

    .venv/bin/python experiments/p2_route_m2ci_v1_construction_evidence.py
"""

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig65_route_m2ci_v1_construction.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-62s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_m2ci_v1_construction.json")) as fh:
        m = json.load(fh)

    B = m["battery_n801"]
    V = m["gate_verdict"]
    DV = m["divergence_exponents"]
    H = m["headline_magnitudes"]

    # ---- the gate, and the scope the writeups must preserve --------------------
    check("gate answered NO", V["answer"] == "NO", V["answer"])
    check("three clauses named as failing", len(V["failing_clauses"]) == 3,
          ", ".join(V["failing_clauses"]))
    check("scope is stated INVISCID and disclaims the viscous question",
          "INVISCID" in V["scope"] and "viscous" in V["scope"])
    check("the YES branch is on record as hollow (closed form already published)",
          "closed form" in V["and_the_YES_branch_would_have_been_hollow"].lower())

    # ---- H2: Y_0 is exactly zero, in EXACT arithmetic --------------------------
    rows = B["H2_exact_rows"]
    check("H2: all %d orbit points have an identically zero residual numerator" % len(rows),
          all(r["exact_zero"] for r in rows))
    check("H2: Chen's own gamma = 3/8 is one of them",
          any(r["is_chen_profile"] and r["exact_zero"] for r in rows))
    check("H2 CONTROL: perturbed amplitude is nonzero at every gamma",
          all(r["control_is_nonzero"] for r in rows))
    check("H2: Y_0 = 0 exactly", H["Y0_exact"] == 0.0)
    check("leg 125's budget lead is quoted, not recomputed",
          m["leg125_budget_lead"]["min"] == 1.325e-09
          and m["leg125_budget_lead"]["max"] == 5.800e-05,
          "%.3e .. %.3e over %d rows" % (m["leg125_budget_lead"]["min"],
                                         m["leg125_budget_lead"]["max"],
                                         m["leg125_budget_lead"]["rows"]))

    # ---- H3/H5: the kernel, and the bound it forces ----------------------------
    check("H5: Z_0 + Z_1 >= 1 for every A", H["Z0_plus_Z1_lower_bound_every_A"] == 1.0)
    check("H5: contraction factor upper bound is 0",
          H["contraction_factor_upper_bound"] == 0.0)
    lb = B["H5_Z_lower_bound"]
    check("H5: default-rcond pinv shadow is misleadingly ~0",
          lb["float_shadow_pinv_default_rcond"] < 1e-5,
          "%.3e" % lb["float_shadow_pinv_default_rcond"])
    check("H5: truncated-rcond shadow returns to 1",
          abs(lb["float_shadow_pinv_rcond_1e-6"] - 1.0) < 1e-3,
          "%.7f" % lb["float_shadow_pinv_rcond_1e-6"])
    check("H5: sigma_ratio sits above numpy's default cutoff (why regime 1 lies)",
          lb["sigma_ratio"] > 1e-13, "%.3e" % lb["sigma_ratio"])

    check("H4: kernel/control relative-defect ratio > 1e4",
          H["kernel_to_control_ratio_n801"] > 1e4,
          "%.3e" % H["kernel_to_control_ratio_n801"])
    check("H4: the control is O(1), i.e. genuinely not in the kernel",
          0.1 < H["control_relative_defect_n801"] < 10.0,
          "%.4f" % H["control_relative_defect_n801"])

    iso = B["H3_isolation"]["rows"]
    check("H3: a competitor exact zero exists at every tested ball radius",
          all(abs(r["distance_achieved"] / r["ball_radius_r"] - 1.0) < 1e-6 for r in iso),
          "radii " + ", ".join("%g" % r["ball_radius_r"] for r in iso))
    check("H3: every competitor's residual sits at the centre's own floor",
          all(r["competitor_residual_sup"] < 2.0 * r["centre_residual_sup"] for r in iso))

    # ---- H7: Z_2 diverges; the kernel control collapses -------------------------
    check("H7: Z_2 diverges with n", DV["Z2_diverges"] and H["Z2_slope_in_log_n"] > 1.0,
          "Z_2 ~ n^%.2f" % H["Z2_slope_in_log_n"])
    check("H7: Z_2 grows by >10x over the 6x ladder",
          H["Z2_growth_over_6x_ladder"] > 10.0, "%.1fx" % H["Z2_growth_over_6x_ladder"])
    check("H7 CONTROL: sigma_min/sigma_max COLLAPSES (kernel is an operator fact)",
          H["sigma_ratio_slope_in_log_n"] < -2.0,
          "~ n^%.2f, %.3ex over the ladder" % (H["sigma_ratio_slope_in_log_n"],
                                               H["sigma_ratio_collapse_over_6x_ladder"]))
    # the ladder must actually be monotone, not just fit a slope
    Z2s = [r["Z2"] for r in DV["rows"]]
    check("H7: the Z_2 ladder is monotone increasing (not a fit artifact)",
          all(b > a for a, b in zip(Z2s, Z2s[1:])),
          " -> ".join("%.2e" % z for z in Z2s))

    # ---- H6b: the symbol/decay coincidence (novelty pass N4) --------------------
    fs = B["H6b_farfield_symbol"]
    check("H6b: the far-field symbol vanishes exactly at s = 3",
          abs(H["farfield_symbol_zero_at_s"] - 3.0) < 1e-12)
    check("H6b: the profile's MEASURED decay exponent is 3",
          abs(H["measured_profile_decay_exponent"] - 3.0) < 1e-3,
          "%.6f" % H["measured_profile_decay_exponent"])
    check("H6b CONTROL: an X^-2 profile measures 2, not 3",
          abs(H["decay_control_on_Xminus2"] + 2.0) < 1e-3,
          "%.6f" % H["decay_control_on_Xminus2"])
    check("H6b: no grading at or above s = 3 is admissible",
          not any(r["admissible"] for r in fs["rows"] if r["s"] >= 3.0))
    check("H6b: gradings below 3 ARE admissible (the clause is not vacuous)",
          any(r["admissible"] for r in fs["rows"] if r["s"] < 3.0))

    # ---- H6a: the standard repair is available (so the NO is not for that reason)
    check("H6a: bordering lifts sigma_min by >100x",
          H["bordering_sigma_min_lift_n801"] > 100.0,
          "%.3ex" % H["bordering_sigma_min_lift_n801"])

    # ---- H1: membership, and the divergence above s = 3 -------------------------
    mem = B["H1_space_membership"]
    check("H1: for s <= 3 the weighted norm is grid-converged",
          all(abs(r["ratio_vs_half_domain"] - 1.0) < 1e-6 for r in mem if r["s"] <= 3.0))
    check("H1 CONTROL: at s = 3.5 the norm is carried by the outermost nodes",
          [r for r in mem if r["s"] == 3.5][0]["ratio_vs_half_domain"] > 1.1)

    build_figure(m)

    print()
    bad = [c for c in CHECKS if not c[1]]
    if bad:
        print("FAILED %d of %d: %s" % (len(bad), len(CHECKS), [c[0] for c in bad]))
        return 1
    print("all %d evidence checks passed" % len(CHECKS))
    print("wrote %s" % FIG)
    return 0


def build_figure(m):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    B = m["battery_n801"]
    DV = m["divergence_exponents"]
    H = m["headline_magnitudes"]

    fig, ax = plt.subplots(2, 2, figsize=(12.4, 8.6))
    fig.suptitle("Route-M2CI (leg 187): Chen's INVISCID $a=1/2$ profile fails the "
                 "certificate on ISOLATION, not on the budget", fontsize=12.5)

    # (a) the orbit -- a continuum of exact solutions through Object A
    a0 = ax[0][0]
    X = np.linspace(-3.5, 3.5, 800)
    for g, lw, col in ((0.20, 1.0, "0.72"), (0.28, 1.0, "0.58"),
                       (0.375, 2.4, "crimson"), (0.50, 1.0, "0.44"), (0.65, 1.0, "0.30")):
        y = -(16.0 / 3.0) * g ** 1.5 * X / (X ** 2 + g) ** 2
        a0.plot(X, y, color=col, lw=lw,
                label=(r"Chen $g=3/8$ (Object A)" if g == 0.375 else None))
    a0.set_title(r"(a) H3 fails: $\Psi_g=-\frac{16}{3}g^{3/2}X/(X^2+g)^2$ is exact "
                 r"for EVERY $g$", fontsize=10)
    a0.set_xlabel("$X$"); a0.set_ylabel(r"$\Omega$")
    a0.legend(fontsize=9, loc="upper right")
    a0.text(0.03, 0.06, "residual numerator = 0 in exact\nrational arithmetic, %d/%d $g$ "
                        "tested" % (H["exact_orbit_gammas_verified_zero"],
                                    H["exact_orbit_gammas_verified_zero"]),
            transform=a0.transAxes, fontsize=8.5,
            bbox=dict(fc="lightyellow", ec="0.6", alpha=0.9))
    a0.grid(alpha=0.3)

    # (b) the kernel is an operator fact: defect falls, control flat
    a1 = ax[0][1]
    L = m["clause_ladder"]
    ns = [r["n"] for r in L]
    a1.loglog(ns, [r["kernel_relative_defect"] for r in L], "o-", color="crimson",
              label="orbit tangent $\\phi$ (kernel)")
    a1.loglog(ns, [r["control_relative_defect"] for r in L], "s-", color="steelblue",
              label="CONTROL: localised bump")
    a1.set_title("(b) H4: the kernel sharpens with the grid; the control does not",
                 fontsize=10)
    a1.set_xlabel("$n$"); a1.set_ylabel(r"$\|DF\,v\|_s/\|v\|_s$")
    a1.legend(fontsize=9); a1.grid(alpha=0.3, which="both")
    a1.text(0.03, 0.30, "separation at $n=801$:\n%.2e" % H["kernel_to_control_ratio_n801"],
            transform=a1.transAxes, fontsize=8.5,
            bbox=dict(fc="lightyellow", ec="0.6", alpha=0.9))

    # (c) Z_2 diverges while sigma_ratio collapses
    a2 = ax[1][0]
    dn = [r["n"] for r in DV["rows"]]
    a2.loglog(dn, [r["Z2"] for r in DV["rows"]], "o-", color="darkorange",
              label=r"$Z_2 \sim n^{%.2f}$" % H["Z2_slope_in_log_n"])
    a2b = a2.twinx()
    a2b.loglog(dn, [r["sigma_ratio"] for r in DV["rows"]], "^--", color="seagreen",
               label=r"$\sigma_{\min}/\sigma_{\max} \sim n^{%.2f}$"
                     % H["sigma_ratio_slope_in_log_n"])
    a2.set_title("(c) H7 fails: $Z_2$ unbounded; and the kernel control collapses",
                 fontsize=10)
    a2.set_xlabel("$n$"); a2.set_ylabel("$Z_2$", color="darkorange")
    a2b.set_ylabel(r"$\sigma_{\min}/\sigma_{\max}$", color="seagreen")
    h1, l1 = a2.get_legend_handles_labels(); h2, l2 = a2b.get_legend_handles_labels()
    a2.legend(h1 + h2, l1 + l2, fontsize=9, loc="center left")
    a2.grid(alpha=0.3, which="both")

    # (d) the far-field symbol vanishes at the profile's own decay rate
    a3 = ax[1][1]
    # offset the sample points so none lands exactly on the pole at s = 3
    s = np.linspace(0.5, 4.0, 401) + 0.5 * (3.5 / 400)
    sig = s / 3.0 - 1.0                       # sigma(s) = c_omega + s c_l, c_l = 1/3
    a3.plot(s, np.abs(1.0 / sig), color="purple", lw=1.8,
            label=r"tail inverse norm $1/|\sigma(s)|$")
    a3.axvline(3.0, color="crimson", ls="--", lw=1.6,
               label=r"$\sigma(s)=0$ at $s=3$")
    a3.axvline(H["measured_profile_decay_exponent"], color="black", ls=":", lw=1.6,
               label="profile's MEASURED decay\nexponent %.4f"
                     % H["measured_profile_decay_exponent"])
    a3.axvspan(3.0, 4.0, color="0.85", alpha=0.6)
    a3.set_yscale("log"); a3.set_ylim(0.5, 1e3); a3.set_xlim(0.5, 4.0)
    a3.set_title("(d) H6b: the symbol vanishes AT the centre's own decay rate", fontsize=10)
    a3.set_xlabel("weight grading $s$"); a3.set_ylabel(r"$1/|\sigma(s)|$")
    a3.legend(fontsize=8.5, loc="upper left")
    a3.text(3.05, 0.9, "centre leaves\nthe space", fontsize=8.5, color="0.25")
    a3.grid(alpha=0.3, which="both")

    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    fig.text(0.5, 0.005,
             "INVISCID ($\\nu=0$), Chen's own framing. Nothing here bears on the viscous "
             "question. $Y_0=0$ exactly — the budget was never the binding clause.",
             ha="center", fontsize=9, style="italic")
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
