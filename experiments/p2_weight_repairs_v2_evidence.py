"""Evidence for Route-WV v2 (leg 59): rebuild fig58 and RE-DERIVE every quoted number.

This script reads ONLY the curated JSON (`writeup/data/p2_weight_repairs_v2.json`) --
it re-runs nothing -- and it is allowed to FAIL: if a number the prose quotes cannot be
recomputed from stored data to the precision the prose states, that is a reproduction
failure and it is the point of having this file (two of this repository's last three
discrepancies were caught exactly this way).

Writes writeup/figures/fig58_weight_repairs_v2.png.
Run: .venv/bin/python experiments/p2_weight_repairs_v2_evidence.py
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "writeup" / "data" / "p2_weight_repairs_v2.json"
FIG = ROOT / "writeup" / "figures" / "fig58_weight_repairs_v2.png"

CHECKS = []


def check(name, got, want, tol, unit=""):
    ok = abs(got - want) <= tol
    CHECKS.append((name, got, want, ok))
    print(f"  {'ok ' if ok else 'FAIL'} {name}: {got:.6g}{unit} vs quoted "
          f"{want:.6g}{unit} (tol {tol:g})")
    return ok


def main():
    d = json.loads(DATA.read_text())
    print("re-deriving the prose's numbers from the curated data alone")

    # -- A: the growth law, and its pre-committed known-answer window ---------------
    A = d["A_growth_law"]
    rows = {r["case"]: r for r in A["cases"]}
    check("A1 1-D slice measured growth", rows["slice_1d"]["measured_growth"], 7.39, 5e-3)
    check("A2 1-D slice 2-D law", rows["slice_1d"]["predicted_2d"], 7.39, 5e-3)
    check("A3 worst rel err of the 2-D law over the battery",
          A["worst_rel_err_2d"], 0.0, 1e-4)
    check("A4 worst factor the 1-D law is off by",
          A["worst_factor_1d_off"], max(r["factor_1d_law_is_off"] for r in A["cases"]),
          1e-12, "x")
    # the two interior-dominated cases are the ones that carry that factor
    worst_case = max(A["cases"], key=lambda r: r["factor_1d_law_is_off"])
    print(f"       (worst case is {worst_case['case']}, p+q = "
          f"{worst_case['far_field_power']:+.2f}, measured x"
          f"{worst_case['measured_growth']:.4f} against the 1-D law's x"
          f"{worst_case['predicted_1d']:.4f})")

    # -- B: how much of the failure set each wall model explains --------------------
    B = d["B_wall_disagreement"]
    raw = d["B_wall_disagreement_raw"]
    Z1 = np.array(raw["Z1"])
    fails = np.array(raw["fails"], dtype=bool)
    ffp = np.array(raw["far_field_power"])
    rngd = np.array(raw["log_range"])
    check("B1 failure count recomputed from Z1", float(np.sum(Z1 >= 1.0)),
          float(B["n_fail"]), 0.0)
    check("B2 stored fail flags match Z1 >= 1", float(np.sum(fails != (Z1 >= 1.0))),
          0.0, 0.0)
    r1 = B["wall_1d"]["failure_rate_among_admitted"]
    r2 = B["wall_2d"]["failure_rate_among_admitted"]
    check("B3 1-D wall failure rate among admitted",
          B["wall_1d"]["admitted_but_failing"] / B["wall_1d"]["admitted"], r1, 1e-12)
    check("B4 2-D wall failure rate among admitted",
          B["wall_2d"]["admitted_but_failing"] / B["wall_2d"]["admitted"], r2, 1e-12)
    check("B5 misclassification ratio 1-D / 2-D",
          B["wall_1d"]["misclassified"] / max(B["wall_2d"]["misclassified"], 1),
          B["ratio_misclassified_1d_over_2d"], 1e-12, "x")

    # -- C: the frozen gate ---------------------------------------------------------
    props = d["after"]["gate"]["properties"]
    delta = d["delta"]
    check("C1 P2 finite fraction, 2-D wall", props["P2_finite"]["finite_fraction"],
          delta["P2_finite_fraction"]["leg59_2d_wall"], 1e-12)
    check("C2 P3 worst |slope-1|, 2-D wall", props["P3_monotone"]["max_slope_error"],
          delta["P3_max_slope_error"]["leg59_2d_wall"], 1e-12)
    n_pass = sum(1 for v in props.values() if v["pass"])
    check("C3 properties passing", float(n_pass),
          float(delta["n_pass"]["leg59_2d_wall"]), 0.0)
    verdict = "PASS" if n_pass == 6 else "FAIL"
    ok_v = verdict == d["after"]["verdict"]
    CHECKS.append(("C4 verdict is the AND of the six properties", n_pass, 6, ok_v))
    print(f"  {'ok ' if ok_v else 'FAIL'} C4 verdict {d['after']['verdict']} "
          f"== AND of properties ({n_pass}/6)")
    check("C5 r_crit is the log-range at the 1-D crossing", d["wall_2d"]["r_crit"],
          d["after"]["gate"]["wall_2d"]["coarse"]["r_crit"], 1e-12, " decades")

    # -- D: the probe window, recomputed from the stored rows ----------------------
    D = d["D_probe_window"]
    wid = np.array([r["window_width_decades"] for r in D["rows"]])
    err = np.array([r["slope_error"] for r in D["rows"]])
    rw = np.argsort(np.argsort(wid)).astype(float)
    re_ = np.argsort(np.argsort(err)).astype(float)
    rw -= rw.mean()
    re_ -= re_.mean()
    rho = float(rw @ re_ / np.sqrt((rw @ rw) * (re_ @ re_)))
    check("D1 Spearman(window width, |slope-1|)", rho,
          D["spearman_width_vs_slope_error"], 1e-12)
    check("D2 worst slope error", float(err.max()), D["worst_slope_error"], 1e-12)
    check("D3 worst-error window width", float(wid[np.argmax(err)]),
          D["worst_window_decades"], 1e-12, " decades")
    check("D4 the worst slope error IS P3's reported one", float(err.max()),
          props["P3_monotone"]["max_slope_error"], 1e-12)

    # -- the figure -----------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 4, figsize=(21.5, 5.2))

    ax = axes[0]
    r_crit = d["wall_2d"]["r_crit"]
    p_minus = d["wall_2d"]["p_minus_1d"]
    ax.scatter(ffp[~fails], rngd[~fails], s=16, c="#2b7bba", alpha=0.7,
               label=r"$Z_1 < 1$ (certificate exists)")
    ax.scatter(ffp[fails], rngd[fails], s=18, c="#d1495b", marker="x",
               label=r"$Z_1 \geq 1$ (no certificate at any residual)")
    ax.axhline(r_crit, color="#1b7837", lw=2.0,
               label=f"2-D wall: log-range = {r_crit:.2f}")
    ax.axvline(p_minus, color="#7b3294", lw=2.0, ls="--",
               label=f"1-D wall: $p+q$ = {p_minus:.2f}")
    ax.set_xlabel("far-field power $p+q$  (the 1-D model's only coordinate)")
    ax.set_ylabel(r"weight log-range  $\log_{10}(\max_i w_i / \min_i w_i)$")
    ax.set_title("(a) the failure set is separated by RANGE, not by $p+q$\n"
                 f"1-D wall admits {B['wall_1d']['admitted_but_failing']}"
                 f"/{B['wall_1d']['admitted']} failing "
                 f"({100*r1:.1f}%); 2-D wall {B['wall_2d']['admitted_but_failing']}"
                 f"/{B['wall_2d']['admitted']} ({100*r2:.1f}%)", fontsize=10)
    ax.legend(fontsize=7.5, loc="upper right")
    ax.grid(alpha=0.25)

    ax = axes[1]
    cases = A["cases"]
    x = np.arange(len(cases))
    w = 0.27
    ax.bar(x - w, [c["measured_growth"] for c in cases], w, label="measured",
           color="#333333")
    ax.bar(x, [c["predicted_2d"] for c in cases], w, label="2-D law (this leg)",
           color="#1b7837")
    ax.bar(x + w, [c["predicted_1d"] for c in cases], w,
           label=r"1-D law $X_{max}^{p+q-1}$", color="#7b3294", alpha=0.75)
    ax.axhline(7.39, color="#d1495b", lw=1.2, ls=":",
               label="pre-committed window x7.39")
    ax.set_xticks(x)
    ax.set_xticklabels([c["case"].replace("_", "\n") for c in cases], fontsize=7.5)
    ax.set_ylabel(f"growth of $\\sup \\nu|\\Omega_0|$ over a "
                  f"{A['reach']:.1f}x reach")
    ax.set_title("(b) the analytic growth rate, re-derived in the 2-D geometry\n"
                 f"2-D law worst rel err {A['worst_rel_err_2d']:.1e}; "
                 f"1-D law off by up to {A['worst_factor_1d_off']:.2f}x", fontsize=10)
    ax.legend(fontsize=7.5)
    ax.grid(alpha=0.25, axis="y")

    ax = axes[2]
    p2 = delta["P2_finite_fraction"]
    p3 = delta["P3_max_slope_error"]
    labels = ["leg 49\n(no wall repair)", "leg 50\n(1-D wall)", "leg 59\n(2-D wall)"]
    p2v = [p2["leg49"], p2["leg50_1d_wall"], p2["leg59_2d_wall"]]
    p3v = [p3["leg49"], p3["leg50_1d_wall"], p3["leg59_2d_wall"]]
    xx = np.arange(3)
    ax.bar(xx - 0.2, p2v, 0.4, color="#2b7bba", label="P2 finite fraction")
    ax.bar(xx + 0.2, p3v, 0.4, color="#e08214", label=r"P3 worst $|slope-1|$")
    ax.axhline(p2["threshold"], color="#2b7bba", ls="--", lw=1.4,
               label=f"P2 floor {p2['threshold']}")
    ax.axhline(p3["threshold"], color="#e08214", ls="--", lw=1.4,
               label=f"P3 ceiling {p3['threshold']}")
    for i, (a, b) in enumerate(zip(p2v, p3v)):
        ax.text(i - 0.2, a, f"{a:.3f}", ha="center", va="bottom", fontsize=8)
        ax.text(i + 0.2, b, f"{b:.3f}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(xx)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_title("(c) the FROZEN gate, thresholds untouched\n"
                 f"verdict {d['after']['verdict']} "
                 f"({delta['n_pass']['leg59_2d_wall']}/6): the wall model was never "
                 "what P3 was about", fontsize=10)
    ax.legend(fontsize=7.5)
    ax.grid(alpha=0.25, axis="y")

    ax = axes[3]
    ax.scatter(wid, err, s=34, c="#333333")
    ax.axhline(0.05, color="#e08214", ls="--", lw=1.4, label="P3 ceiling 0.05")
    for r in D["rows"]:
        if r["slope_error"] > 0.05:
            ax.annotate(r["label"].replace("rand_", "r"),
                        (r["window_width_decades"], r["slope_error"]),
                        fontsize=6.5, xytext=(3, 2), textcoords="offset points")
    ax.set_xlabel("probe window width (decades of $\\epsilon$), "
                  "$[Y_0/\\max_i w_i|d_i|,\\; C/\\|A\\|_w]$")
    ax.set_ylabel(r"$|{\rm slope}-1|$")
    ax.set_title("(d) DIAGNOSIS, not folded into the gate: P3 measures\n"
                 f"the probe's window, not the weight — Spearman "
                 f"{D['spearman_width_vs_slope_error']:+.3f}", fontsize=10)
    ax.legend(fontsize=7.5)
    ax.grid(alpha=0.25)

    fig.suptitle("Route-WV (leg 59): the weight fitness's conditioning wall is 2-D — "
                 "modelling it in both factors fixes P2 and leaves P3 exactly where "
                 "it was", fontweight="bold", y=1.02)
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print(f"wrote {FIG}")

    bad = [c for c in CHECKS if not c[3]]
    if bad:
        print(f"\nREPRODUCTION FAILURE: {len(bad)} of {len(CHECKS)} checks")
        for name, got, want, _ in bad:
            print(f"  {name}: {got} vs {want}")
        sys.exit(1)
    print(f"\nall {len(CHECKS)} quoted numbers re-derived from the curated data")


if __name__ == "__main__":
    main()
