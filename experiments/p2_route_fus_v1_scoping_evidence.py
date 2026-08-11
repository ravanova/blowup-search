"""Route-FUS (leg 314) -- EVIDENCE: every number the BLOG and TECHNICAL write-ups quote,
re-derived from `writeup/data/p2_route_fus_v1.json` alone.

Also builds `writeup/figures/fig77_route_fus_v1.png`.

FIGURE NUMBER.  The leg brief records fig69-fig76 as taken, reserved or spoken for
(69->302, 70->311, 71->303, 72->320, 73->312, 74->316, 75->301, 76->313) and instructs this
leg to take **fig77** and say so plainly.  It does, here and in
`experiments/journal/leg_314.md`, so integration (leg 0) can register it.

No re-run of anything: this reads the curated JSON the runner
(`experiments/p2_route_fus_v1_scoping.py`) already produced.  In particular it performs NO
gCLM measurement -- see the runner's self-guard and the ban walk in
`writeup/novelty/leg_314.md` sec 3.

    .venv/bin/python experiments/p2_route_fus_v1_scoping_evidence.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig77_route_fus_v1.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-64s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_fus_v1.json")) as fh:
        w = json.load(fh)

    # ---- the gate, in its pre-committed wording ------------------------------------
    check("gate answered yes (a definite classification was produced)",
          w["gate_answer"].startswith("yes"), w["gate_answer"])
    check("classification is (iii) OPEN", w["classification"] == "iii_OPEN",
          w["classification_label"])
    check("an obstruction is NAMED (lesson 91)",
          "REALIZATION-INVARIANT" in w["named_obstruction"]
          and "HIGH-FREQUENCY RESOLVENT BOUND" in w["named_obstruction"],
          "%d chars" % len(w["named_obstruction"]))

    # ---- the self-guard: this leg measured no gCLM ---------------------------------
    g = w["self_guard"]
    check("self-guard: zero banned calls in the runner", len(g["banned_calls_found"]) == 0,
          str(g["banned_calls_found"]))
    check("self-guard: zero solver/numpy/scipy imports in the runner",
          g["solver_or_numeric_imports"] == [], str(g["solver_or_numeric_imports"]))
    check("self-guard ok flag", g["ok"] is True)

    # ---- the smear arithmetic ------------------------------------------------------
    s = w["smear_arithmetic"]
    check("K ladder is 48/96/144", s["K"] == [48, 96, 144], str(s["K"]))
    check("n_unstable is 45/93/141", s["n_unstable"] == [45, 93, 141], str(s["n_unstable"]))
    check("slope dn/dK == 1.0000", abs(s["slope_dn_dK"] - 1.0) < 1e-12,
          "%.6f" % s["slope_dn_dK"])
    check("affine fit is exact (max |residual| == 0)", s["max_abs_residual"] == 0,
          "%.3g" % s["max_abs_residual"])
    check("affine law is n = K - 3", s["exact_affine_offset"] == 3, s["affine_law"])
    check("verdict DIVERGENT", s["verdict"] == "DIVERGENT", s["verdict"])
    check("max Re relative spread < 1%", s["max_re_relative_spread"] < 0.01,
          "%.4f%%" % (100 * s["max_re_relative_spread"]))
    check("max|Im| growth x3.267 while K grows x3.000",
          abs(s["max_abs_im_growth_factor"] - 3.267) < 5e-3
          and abs(s["K_growth_factor"] - 3.0) < 1e-12,
          "%.3f vs %.3f" % (s["max_abs_im_growth_factor"], s["K_growth_factor"]))

    # ---- the tidy-closed-form diagnosis -------------------------------------------
    t = s["tidy_closed_form_diagnosis"]
    check("offset 3 accounted: 1 excised dilation + 2 non-positive",
          t["excised_by_identity"] == 1 and t["implied_non_positive_besides_dilation"] == 2
          and t["accounted"] is True)
    check("offset is explicitly NOT banked as a fact about the operator",
          "NOT banked" in t["what_is_load_bearing"])

    # ---- the anti-artifact check ---------------------------------------------------
    a = s["artifact_check"]
    check("profile residual improves > 10 decades across the ladder",
          a["residual_improvement_decades"] > 10.0,
          "%.2f decades" % a["residual_improvement_decades"])
    check("truncation parameter improves > 5 decades",
          a["truncation_improvement_decades"] > 5.0,
          "%.2f decades" % a["truncation_improvement_decades"])
    check("resolution improves AND count rises (not an under-resolution artifact)",
          a["resolution_improves_and_count_rises"] is True)

    # ---- the positive control (lesson 90) ------------------------------------------
    c = w["positive_control"]
    check("positive control: same code, mu>0, reports K_STABLE",
          c["verdict"] == "K_STABLE", c["verdict"])
    check("positive control: count is 0 at every K", c["all_zero"] is True)

    # ---- the classifier can come out differently (lesson 90) -----------------------
    st = w["classifier_self_tests"]
    check("classifier self-tests all pass", st["all_pass"] is True)
    check("classifier reaches all four outcomes",
          sorted(st["distinct_outcomes"]) ==
          ["DISCHARGED", "i_PROVABLE", "ii_NUMERICAL", "iii_OPEN"],
          str(st["distinct_outcomes"]))

    # ---- provenance ----------------------------------------------------------------
    b = w["banked_input"]
    check("banked input is Route-I's on-disk ladder",
          b["file"] == "writeup/data/p2_route_i_v1_driven.json", b["file"])
    check("the realization is NAMED (lesson 91)",
          "maximal-l^2" in b["realization"].lower()
          and "odd-sine" in b["realization"].lower()
          and "no origin condition" in b["realization"].lower(),
          b["realization"][:60] + "...")
    for key in ("XU", "BCG", "CGSS", "GHJS", "USC", "USC2", "WM"):
        check("source %s carries a link" % key,
              w["sources"][key]["url"].startswith("https://arxiv.org/abs/"),
              w["sources"][key]["arxiv"])
    check("corroborating sources folded in (GW, BZ, CH, VOIGT, BK)",
          all(k in w["sources"] for k in ("GW", "BZ", "CH", "VOIGT", "BK")),
          ",".join(sorted(w["sources"])))
    check("Barker-Zumbrun role records the ANALYTICALLY derived winding radius",
          "ANALYTICALLY" in w["sources"]["BZ"]["role"]
          and "winding" in w["sources"]["BZ"]["role"].lower())
    check("every source carries a LINK, not just a count (leg 174 lesson)",
          all(s.get("url", "").startswith("http") for s in w["sources"].values()),
          "%d sources" % len(w["sources"]))

    # ---- MF3 audit: no absence claim rests on an ANDed-quoted-phrase zero ------------
    m = w["mf3_audit"]
    check("MF3 was TESTED, not assumed: it did not reproduce here",
          m["reproduced_on_this_instrument"] is False)
    check("MF3 reproduction test recorded, all four probes",
          len(m["reproduction_test"]) == 4)
    check("an ANDed quoted pair returned NONZERO (conjunction operator works)",
          max(r["total_results"] for r in m["reproduction_test"]
              if r["shape"] == "ANDed quoted pair") == 251)
    check("zero ANDed-zero results banked anywhere in this leg",
          m["anded_zero_results_banked_anywhere_in_this_leg"] == 0
          and m["anded_queries_run_by_this_leg_all_nonzero"] is True)
    check("exactly ONE absence-based discriminator, and it is D4",
          m["absence_based_discriminators"]
          == ["D4_certified_count_exists_for_these_models"])
    check("D4 rests on a multi-instrument sweep, NOT on a query zero",
          "NOT any query returning zero" in m["d4_basis"])
    check("the (iii)-OPEN branch does NOT rest on an ANDed zero",
          m["does_the_iii_open_branch_rest_on_an_anded_zero"].startswith("NO"))
    check("the undercount limitation is recorded, not glossed",
          "UNDERCOUNT" in m["residual_limitation_recorded"])

    # ---- the ceiling ---------------------------------------------------------------
    ceil = w["ceiling"]
    check("Clay odds unchanged at ~0.05%", "0.05%" in ceil["clay_odds"], ceil["clay_odds"])
    check("no link of the L1->L4 chain moved", "no link" in ceil["chain"])
    check("scope limited to the measured realization, not claimed for the four models",
          "NOT a claim about CCF" in ceil["scope"])

    _figure(w)

    bad = [n for n, ok, _ in CHECKS if not ok]
    print("\n%d/%d checks pass" % (len(CHECKS) - len(bad), len(CHECKS)))
    if bad:
        raise SystemExit("FAILED: %s" % bad)
    print("wrote %s" % os.path.relpath(FIG, ROOT))


def _figure(w):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    s = w["smear_arithmetic"]
    c = w["positive_control"]
    K = s["K"]
    n = s["n_unstable"]
    nv = [r["n_unstable"] for r in c["rows"]]
    ims = s["max_abs_im"]
    res = s["max_re"]

    fig, ax = plt.subplots(1, 3, figsize=(13.6, 4.3))

    # (a) the count: divergent inviscid, flat viscous
    ax[0].plot(K, n, "o-", color="#B3412B", lw=2, ms=8,
               label=r"inviscid $\mu=0$:  $n = K-3$")
    ax[0].plot(K, nv, "s-", color="#2B6CB3", lw=2, ms=8,
               label=r"viscous $\mu>0$ (control):  $n = 0$")
    ax[0].plot(K, [k - 3 for k in K], "--", color="#888888", lw=1,
               zorder=0, label=r"slope $dn/dK = 1$")
    ax[0].set_xlabel("truncation $K$ (degrees of freedom)")
    ax[0].set_ylabel(r"unstable count  $\#\{\mathrm{Re}\,\mu > 10^{-6}\}$")
    ax[0].set_title("(a) the count tracks the GRID, not the operator")
    ax[0].legend(fontsize=8, loc="upper left")
    ax[0].grid(alpha=0.25)

    # (b) Re flat, |Im| grows -- a curve, not a finite set
    ax2 = ax[1]
    ax2.plot(K, res, "o-", color="#B3412B", lw=2, ms=8)
    ax2.set_xlabel("truncation $K$")
    ax2.set_ylabel(r"$\max\,\mathrm{Re}\,\mu$", color="#B3412B")
    ax2.tick_params(axis="y", labelcolor="#B3412B")
    ax2.set_ylim(0, 6)
    ax2b = ax2.twinx()
    ax2b.plot(K, ims, "^-", color="#2B6CB3", lw=2, ms=8)
    ax2b.set_ylabel(r"$\max\,|\mathrm{Im}\,\mu|$", color="#2B6CB3")
    ax2b.tick_params(axis="y", labelcolor="#2B6CB3")
    ax2.set_title("(b) $\\mathrm{Re}$ flat to %.2f%%, $|\\mathrm{Im}|$ grows $\\times$%.2f"
                  % (100 * s["max_re_relative_spread"], s["max_abs_im_growth_factor"]))
    ax2.grid(alpha=0.25)

    # (c) the anti-artifact check
    a = s["artifact_check"]
    rr = [a["profile_residual_by_K"][str(k)] for k in K]
    ax3 = ax[2]
    ax3.semilogy(K, rr, "v-", color="#2F7D4F", lw=2, ms=8, label="profile residual")
    ax3.set_xlabel("truncation $K$")
    ax3.set_ylabel("profile residual (log)", color="#2F7D4F")
    ax3.tick_params(axis="y", labelcolor="#2F7D4F")
    ax3b = ax3.twinx()
    ax3b.plot(K, n, "o-", color="#B3412B", lw=2, ms=8, label="unstable count")
    ax3b.set_ylabel("unstable count", color="#B3412B")
    ax3b.tick_params(axis="y", labelcolor="#B3412B")
    ax3.set_title("(c) resolution improves %.1f decades,\nand the count RISES"
                  % a["residual_improvement_decades"])
    ax3.grid(alpha=0.25)

    fig.suptitle("Leg 314 / Route-FUS -- the finite-unstable-spectrum condition is "
                 "REALIZATION-DEPENDENT:\nin the maximal-$L^2$ realization the unstable "
                 "count diverges with the grid  (gCLM $a=1/2$, $p=3$; banked Route-I data)",
                 fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
