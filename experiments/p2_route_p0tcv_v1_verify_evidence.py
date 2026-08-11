"""Route-P0TCV v1 (leg 300) — EVIDENCE: every number the BLOG and TECHNICAL write-ups
quote, re-derived from `writeup/data/p2_route_p0tcv_v1_verify.json` alone.

Also builds `writeup/figures/fig68_route_p0tcv_v1_verify.png`.

Nothing expensive is recomputed and nothing is re-downloaded: this reads the curated
JSON and asserts the relations the prose asserts, so a reader can check the prose
without re-running the gate or re-fetching BCG's e-print.

The one thing this script does recompute from scratch, deliberately, is the single
magnitude the gate turned on: the width ratio.  It is re-derived here in exact rational
+ Decimal arithmetic, independently of the runner's own code path, so that the
gate-answering number has two independent implementations in the repository rather than
one.  If they ever disagree, this script fails.

    .venv/bin/python experiments/p2_route_p0tcv_v1_verify_evidence.py
"""

import json
import os
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig68_route_p0tcv_v1_verify.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-62s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_p0tcv_v1_verify.json")) as fh:
        w = json.load(fh)

    win = w["clause_c_window"]
    cmp_ = w["clause_c_claim_comparison"]
    rows = {r["quantity"]: r for r in cmp_["rows"]}
    a = w["clause_a_architecture"]
    b = w["clause_b_byte_untouched"]
    loc = w["clause_a_locators"]
    nc = w["negative_controls"]
    dg = cmp_["diagnosis"]

    # ---- the gate answer the prose reports -------------------------------
    check("gate answer is NO", w["gate_answer"] == "NO", w["gate_answer"])

    # ---- provenance ------------------------------------------------------
    check("BCG e-print md5 matched its pin",
          w["provenance"].get("md5_matches_pin") is True,
          w["provenance"].get("tarball_md5", "n/a"))
    check("BCG TeX line count 6898 agrees with leg 266",
          loc["tex_lines"] == 6898 and loc["tex_lines_agree"],
          f"{loc['tex_lines']} lines")

    # ---- clause (a): PASSES, and the prose says so ------------------------
    check("clause (a) passes: 3/3 architecture subclaims",
          a["clause_a_pass"] and a["n_confirmed"] == 3 and a["n_total"] == 3,
          f"{a['n_confirmed']}/{a['n_total']}")
    check("all 10 BCG locators confirmed by eye at source",
          loc["all_confirmed"] and loc["n_confirmed"] == 10,
          f"{loc['n_confirmed']}/{loc['n_locators']}")

    # ---- clause (b): PASSES ----------------------------------------------
    check("clause (b) passes: 29/29 verifier-confirmed claims byte-identical",
          b["clause_b_pass"] and b["n_confirmed_identical"] == b["n_confirmed_total"] == 29,
          f"{b['n_confirmed_identical']}/{b['n_confirmed_total']}")
    check("0 paths outside leg 266's declared territory",
          b["n_outside_territory"] == 0, str(b["paths_outside_declared_territory"]))
    check("0 shared ledgers touched by leg 266",
          b["shared_ledgers_touched"] == [], str(b["shared_ledgers_touched"]))
    check("leg 266's diff is 5 files / 9 hunks (3 of leg 251's + 2 new)",
          b["n_files"] == 5 and b["n_hunks"] == 9,
          f"{b['n_files']} files, {b['n_hunks']} hunks")
    check("no undeclared JSON path changed",
          b["json_paths_changed_undeclared"] == [],
          str(b["json_paths_changed_undeclared"]))

    # ---- clause (c): the failure, quantified ------------------------------
    check("clause (c) fails: 4 of 5 magnitudes reproduce",
          (not w["clause_c_pass"]) and cmp_["n_agree"] == 4 and cmp_["n_total"] == 5,
          f"{cmp_['n_agree']}/{cmp_['n_total']}")
    check("the single failing magnitude is the width ratio",
          cmp_["failing"] == ["width_ratio"], str(cmp_["failing"]))

    wr = rows["width_ratio"]
    check("leg 266 claimed 6.855", wr["claimed_by_266"] == "6.855")
    check("it re-derives to 6.854 at the quoted precision",
          wr["rederived_at_claimed_precision"] == "6.854",
          wr["rederived_at_claimed_precision"])
    check("relative error 1.310e-04 (0.0131%)",
          abs(wr["rel_error_float"] - 1.310e-4) < 5e-7,
          f"{wr['rel_error_float']:.4e}")

    # the four that DO reproduce, each named in the prose
    for q, claim in (("dominance_lo", "1.1666667"), ("dominance_hi", "1.1909830"),
                     ("dominance_width", "0.0243163"), ("target_width", "0.1666667")):
        check(f"{q} reproduces exactly at 7 d.p. ({claim})",
              rows[q]["agrees_at_quoted_precision"]
              and rows[q]["rederived_at_claimed_precision"] == claim,
              rows[q]["rederived_exact"][:16])

    # ---- INDEPENDENT re-implementation of the gate-answering number -------
    # r* = (7 - sqrt 5)/4 and 7/6, so the ratio is (1/6) / ((7-sqrt5)/4 - 7/6)
    # = 2/(7 - 3 sqrt 5) = (7 + 3 sqrt 5)/2.  Derived here without touching the runner.
    s5 = Decimal(5).sqrt()
    r_star_ind = (7 - s5) / 4
    r_res_ind = Decimal(7) / 6
    ratio_ind = (r_res_ind - 1) / (r_star_ind - r_res_ind)
    closed_ind = (7 + 3 * s5) / 2
    check("independent re-implementation agrees with the runner's r*",
          str(r_star_ind)[:22] == win["r_star"][:22],
          str(r_star_ind)[:22])
    check("independent re-implementation agrees with the runner's ratio",
          str(ratio_ind)[:22] == win["width_ratio"][:22],
          str(ratio_ind)[:22])
    check("ratio equals its closed form (7 + 3*sqrt5)/2 to 40 digits",
          abs(ratio_ind - closed_ind) < Decimal("1e-40"),
          str(closed_ind)[:22])
    check("6.855 is NOT the correctly rounded value of that closed form",
          str(closed_ind.quantize(Decimal("0.001"))) == "6.854")

    # ---- the diagnosis the prose leans on ---------------------------------
    check("defect localised: leg 266's OWN endpoints re-divide to 6.854 too",
          dg["formula_is_sound"] and dg["ratio_rounded_from_266_own_endpoints_4sf"] == "6.854",
          dg["ratio_rounded_from_266_own_endpoints_4sf"])

    # ---- negative controls ------------------------------------------------
    check("5/5 negative controls behaved as required",
          nc["all_behaved"] and nc["n"] == 5,
          f"{nc['n_behaved_as_required']}/{nc['n']}")

    # ---- propagation of the failing figure --------------------------------
    prop = w["propagation_of_the_failing_figure"]
    check("the failing figure has 8 restatement surfaces, 7 of them on main",
          prop["n_surfaces"] == 8 and prop["n_on_main"] == 7,
          f"{prop['n_surfaces']} surfaces / {prop['n_on_main']} on main")
    check("both main-side owners are outside leg 300's territory",
          sorted(prop["on_main_paths"]) == ["DIRECTION.md", "experiments/JOURNAL.md"],
          str(prop["on_main_paths"]))
    check("reserve leg 305's draft is among the DIRECTION.md surfaces",
          any(s["path"] == "DIRECTION.md" and s["line"] in ("13474", "13479")
              for s in prop["surfaces"]),
          str([s["line"] for s in prop["surfaces"] if s["path"] == "DIRECTION.md"]))

    # ---- Clay honesty -----------------------------------------------------
    check("Clay odds unmoved at ~0.05%", w["clay"]["odds"] == "~0.05%")

    build_figure(w)

    bad = [c for c in CHECKS if not c[1]]
    print()
    print("%d/%d checks pass" % (len(CHECKS) - len(bad), len(CHECKS)))
    print("wrote %s" % os.path.relpath(FIG, ROOT))
    return 1 if bad else 0


def build_figure(w):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    win = w["clause_c_window"]
    cmp_ = w["clause_c_claim_comparison"]
    rows = cmp_["rows"]

    r_res = float(win["r_restriction_lower_edge"])
    r_star = float(win["r_star"])
    ratio = float(win["width_ratio"])
    claimed_ratio = float(w["claimed_by_leg_266"]["width_ratio"])

    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(9.2, 5.6), gridspec_kw={"height_ratios": [1.9, 1.0]})

    # --- top: the two r-windows, to scale ---
    ax.barh(0.72, r_res - 1.0, left=1.0, height=0.24,
            color="#3B7EA1", edgecolor="black", linewidth=0.8,
            label="target window $(1,\\,7/6]$ — width %.7f" % (r_res - 1.0))
    ax.barh(0.34, r_star - r_res, left=r_res, height=0.24,
            color="#C4622D", edgecolor="black", linewidth=0.8,
            label="BCG dominance window $(7/6,\\,r^*)$ — width %.7f" % (r_star - r_res))
    for x, lab, y, ha in ((1.0, "1", 0.05, "left"),
                          (r_res, "$7/6$ = %.7f" % r_res, 0.16, "right"),
                          (r_star, "$r^*$ = %.7f" % r_star, 0.05, "right")):
        ax.axvline(x, color="0.35", linewidth=0.8, linestyle=":")
        ax.text(x, y, " " + lab + " ", ha=ha, va="bottom", fontsize=8.5)
    ax.annotate("", xy=(r_res, 0.95), xytext=(r_star, 0.95),
                arrowprops=dict(arrowstyle="<->", linewidth=0.9, color="#C4622D"))
    ax.text(1.002, 1.0,
            "widths differ by $(7+3\\sqrt{5})/2$ = %.7f$\\times$ — leg 266 wrote %.3f"
            % (ratio, claimed_ratio),
            ha="left", va="bottom", fontsize=8.5)
    ax.set_xlim(0.995, 1.205)
    ax.set_ylim(0.0, 1.12)
    ax.set_yticks([])
    ax.set_xlabel("similarity exponent $r$   (BCG arXiv:2208.09445, $\\gamma = 7/5$)")
    ax.legend(loc="center left", fontsize=8.5, framealpha=0.95)
    ax.set_title("Leg 300 / Route-P0TCV — leg 266's window, re-derived from BCG's own\n"
                 "(eq:r:restriction) and (eq:rstar) at 60-digit precision",
                 fontsize=10.5)

    # --- bottom: which of leg 266's quoted magnitudes reproduce ---
    labels = [r["quantity"] for r in rows]
    rels = [max(r["rel_error_float"], 1e-12) for r in rows]
    cols = ["#4C9A6A" if r["agrees_at_quoted_precision"] else "#B3202C" for r in rows]
    ax2.bar(labels, rels, color=cols, edgecolor="black", linewidth=0.7)
    ax2.set_yscale("log")
    ax2.set_ylim(1e-9, 3e-2)
    ax2.set_ylabel("rel. error of\nleg 266's figure", fontsize=8.5)
    ax2.tick_params(axis="x", labelsize=8)
    ax2.axhline(5e-8, color="0.4", linewidth=0.8, linestyle="--")
    ax2.text(0.015, 6e-8, "rounding floor at the quoted 7 d.p.", fontsize=7.5,
             va="bottom", transform=ax2.get_yaxis_transform())
    idx = labels.index("width_ratio")
    ax2.annotate("claimed %.3f, re-derives %.7f\n(rel. err %.3e)"
                 % (claimed_ratio, ratio, rels[idx]),
                 xy=(idx, rels[idx]), xytext=(idx - 1.55, rels[idx] * 4.0),
                 fontsize=8, ha="center",
                 arrowprops=dict(arrowstyle="->", linewidth=0.8))
    ax2.set_title("%d/%d of leg 266's quoted magnitudes reproduce at the precision it "
                  "quoted — clauses (a) and (b) pass in full"
                  % (cmp_["n_agree"], cmp_["n_total"]), fontsize=9.5)

    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
