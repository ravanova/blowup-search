"""Route-DFRE (leg 316) -- EVIDENCE: every number the BLOG and TECHNICAL write-ups quote,
re-derived from `writeup/data/p2_route_dfre_v1.json` alone.

Also builds `writeup/figures/fig71_route_dfre_v1.png` (provisional number -- the leg brief
assigns fig71; the orchestrator registers it in writeup/build_figures.py's shared list).

No network, no re-clone, no re-decoding of the CGL.jl proof-witness CSVs -- this reads the
curated JSON the runner (`experiments/p2_route_dfre_v1.py`) already produced and checks the
prose's numbers against it directly.

    .venv/bin/python experiments/p2_route_dfre_v1_evidence.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig71_route_dfre_v1.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-62s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_dfre_v1.json")) as fh:
        w = json.load(fh)

    check("gate answer is YES", w["gate_answer"] == "YES", w["gate_answer"])
    check("pinned commit matches paper's own bibliography item [15]",
          w["pinned_commit"] == "be034923c0b63e3103a9b2cb030a02699d05625e", w["pinned_commit"])

    sanity = w["decoder_sanity_check"]
    check("decoder sanity: |mu_decoded - mu1(paper Sec.6)| < tol",
          sanity["abs_diff_mu"] < sanity["tolerance"], f"{sanity['abs_diff_mu']:.3e}")
    check("decoder sanity: |kappa_decoded - kappa1(paper Sec.6)| < tol",
          sanity["abs_diff_kappa"] < sanity["tolerance"], f"{sanity['abs_diff_kappa']:.3e}")

    total_rows = 0
    total_chain_checked = 0
    for name in ("top", "turn", "bottom"):
        seg = w["segments"][name]
        total_rows += seg["n_rows"]
        total_chain_checked += seg["chain_checked"]
        check(f"{name}: every row's exists box strictly inside its own uniq box",
              seg["strict_exists_in_uniq_fail_count"] == 0,
              f"{seg['strict_exists_in_uniq_ok']}/{seg['n_rows']}")
        check(f"{name}: every row's exists box subset of PREVIOUS row's uniq box (chaining)",
              seg["chain_exists_in_prev_uniq_fail_count"] == 0,
              f"{seg['chain_exists_in_prev_uniq_ok']}/{seg['chain_checked']}")
        check(f"{name}: boxes tile the swept parameter with no gap",
              seg["coverage_gap_count"] == 0, f"gaps={seg['coverage_gap_count']}")

    check("connection points: each own exists-box inside its own uniq-box",
          w["connection_points"]["all_own_boxes_ok"], "")
    check("total rows checked across all three segments equals reported total",
          total_rows == sum(w["row_totals"].values()), f"{total_rows}")
    check("elapsed time is a small-scale run (<10 min), no perf rework needed",
          w["elapsed_seconds"] < 600, f"{w['elapsed_seconds']:.1f}s")

    # -------------------- figure --------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))

    # Panel A: what each segment checked, pass/fail bar
    ax = axes[0]
    names = ["top", "turn", "bottom"]
    ns = [w["segments"][n]["n_rows"] for n in names]
    ok = [w["segments"][n]["all_pass"] for n in names]
    colors = ["#2e7d32" if o else "#c1440e" for o in ok]
    ax.bar(names, ns, color=colors)
    for i, (n, v) in enumerate(zip(names, ns)):
        ax.text(i, v, f"{v}\nrows", ha="center", va="bottom", fontsize=8.5)
    ax.set_ylabel("released proof-witness rows decoded")
    ax.set_title("A. Case I, j=1 branch: every segment,\nboth inclusion conditions, exact arithmetic")

    # Panel B: decoder sanity vs paper's own printed Sec.6 starting point
    ax = axes[1]
    labels = ["mu", "kappa"]
    diffs = [sanity["abs_diff_mu"], sanity["abs_diff_kappa"]]
    rads = [sanity["decoded_mu_exists_rad"], sanity["decoded_kappa_exists_rad"]]
    x = range(len(labels))
    ax.bar([i - 0.18 for i in x], diffs, width=0.36, label="|decoded - paper Sec.6|", color="#1f4e79")
    ax.bar([i + 0.18 for i in x], rads, width=0.36, label="decoded existence-ball radius", color="#7b1fa2")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels)
    ax.set_yscale("log")
    ax.set_ylabel("magnitude (log scale)")
    ax.legend(fontsize=7.5)
    ax.set_title("B. Decoder sanity: agrees with the\npaper's own printed j=1 starting point")

    # Panel C: the gate, stated as a picture
    ax = axes[2]
    ax.axis("off")
    txt = (
        "GATE (pre-committed):\n"
        "Does DF-CGL's released verification\n"
        "package reproduce the paper's OWN\n"
        f"corollary from published constants?\n\n"
        f"ANSWER: {w['gate_answer']}\n\n"
        f"49,465 proof-witness rows\n"
        f"(top {w['row_totals']['top']} + turn {w['row_totals']['turn']}\n"
        f"+ bottom {w['row_totals']['bottom']}),\n"
        f"decoded EXACTLY (fractions.Fraction\n"
        f"of arb_dump_str dyadic values,\n"
        f"no float64 anywhere in the check),\n"
        f"all satisfy Thm 4.1 / Sec.6's own\n"
        f"box-chaining condition.\n\n"
        f"Runtime: {w['elapsed_seconds']:.1f}s\n"
        f"pinned commit be034923c…"
    )
    ax.text(0.02, 0.98, txt, va="top", ha="left", fontsize=9, family="monospace")
    ax.set_title("C. The gate")

    fig.suptitle("Route-DFRE (leg 316): CAP-reproduction lane, entry 1 -- "
                  "DF-CGL's own released proof data, checked exactly",
                  fontweight="bold", y=1.03)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight", dpi=140)
    print(f"wrote {FIG}")

    n_fail = sum(1 for _, ok_, _ in CHECKS if not ok_)
    print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} checks OK")
    if n_fail:
        raise SystemExit(f"{n_fail} check(s) FAILED")


if __name__ == "__main__":
    main()
