#!/usr/bin/env python3
"""fig69 -- Leg 302 (Route-P2T1): evidence + redraw from curated JSON, no re-run.

Leg 302's own runner (`experiments/p2_route_p2t1_v1.py`) only emits fig69 under a
`--figure PATH` flag, and it exits nonzero because the leg's own gate answered NO
(`writeup/data/p2_route_p2t1_v1.json`'s `gate.answer`). That is a correct leg
outcome, but it means fig69 cannot be produced by a shared/CI rebuild of
`writeup/build_figures.py`, which runs every figure unconditionally and treats a
nonzero exit as a hard failure. `writeup/build_figures.py` names this debt
explicitly in the comment above its `P2_EVIDENCE` registry.

This script is the fix: it reads ONLY the already-banked
`writeup/data/p2_route_p2t1_v1.json` -- every scalar plotted below is looked up by
key, nothing is retyped and nothing is re-measured -- and redraws fig69 from it.
Panel A's line is the CLOSED FORM delta_dis(r) = 6r - 7 at gamma = 7/5, which is
itself a curated fact (probe KA2, verified there to 6.66e-16, not a new
computation); it is evaluated only at the banked window endpoints and at the
sampling grid used for the plot, never against the runner.

What this script asserts and will not let through quietly: KA8 is the one probe
that FAILED (`gate.half_one_known_answers == False`), and its measured magnitude is
129.048x its own pre-stated tolerance (`|k(1)-1| = 1.2904784973954975e-07` against
tolerance `1e-09`) -- that number is checked below and printed on the figure itself,
not rounded or smoothed away.

    .venv/bin/python experiments/p2_route_p2t1_v1_evidence.py
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_p2t1_v1.json")
FIG = os.path.join(ROOT, "writeup", "figures", "fig69_route_p2t1_v1_sensitivity.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-72s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(DATA) as fh:
        j = json.load(fh)

    gate = j["gate"]
    probes = j["probes"]
    plants = j["plants"]
    loss_curve = j["post_hoc_conditioning_diagnostic"]["loss_curve"]
    ka4 = probes["KA4"]["detail"]
    ka8 = probes["KA8"]

    # ---- the load-bearing facts, asserted before anything is drawn --------------------
    check("(G1) the leg's own gate answered NO", gate["answer"] == "NO", "")
    check("(G2) it is KA8, and only KA8, that failed among the 11 known-answer probes",
          [k for k, v in probes.items() if not v["passed"]] == ["KA8"], "")
    ka8_ratio = ka8["residual"]  # residual is already dev/tolerance for KA8 (see JSON "units")
    dev_k_at_1 = ka8["detail"]["dev_k_at_1"]
    tol_k_at_1 = 1e-09
    recomputed_ratio = dev_k_at_1 / tol_k_at_1
    check("(G3) KA8's banked 129.048x residual is exactly dev_k_at_1 / its own 1e-9 tolerance",
          abs(recomputed_ratio - ka8_ratio) < 1e-6 * ka8_ratio,
          "%.6f vs banked %.6f" % (recomputed_ratio, ka8_ratio))
    check("(G4) KA8 fails a >=100x margin, not a rounding-distance miss",
          ka8_ratio > 100.0, "%.3fx" % ka8_ratio)
    lo, hi, margin = ka4["lo"], ka4["hi"], ka4["delta_dis_at_r_star"]
    check("(G5) the closed form 6r-7 reproduces the window's banked endpoints",
          abs((6 * lo - 7) - 0.0) < 1e-6 and abs((6 * hi - 7) - margin) < 1e-9,
          "6*hi-7=%.12f vs margin=%.12f" % (6 * hi - 7, margin))

    fig = plt.figure(figsize=(15.5, 5.0))
    axA, axB, axC = fig.subplots(1, 3)

    # ---- Panel A: delta_dis(r) = 6r-7 at gamma=7/5, closed form, with the dominance window ----
    r = [1.05 + 0.001 * i for i in range(int((1.22 - 1.05) / 0.001) + 1)]
    d = [6 * rr - 7 for rr in r]
    axA.plot(r, d, color="#2563eb", lw=1.8, label=r"$\delta_{dis}(r) = 6r-7$ (KA2, closed form)")
    axA.axhline(0.0, color="#6b7280", lw=0.8)
    axA.axvspan(lo, hi, color="#059669", alpha=0.15, label="dominance window (KA4, leg 240)")
    axA.axvline(lo, color="#059669", lw=1.0, ls=":")
    axA.axvline(hi, color="#059669", lw=1.0, ls=":")
    axA.plot([hi], [margin], "o", color="#059669", ms=6)
    axA.annotate("margin = %.6f" % margin, xy=(hi, margin), xytext=(hi + 0.005, margin + 0.03),
                 fontsize=8, color="#059669")
    axA.set_xlabel(r"self-similar exponent $r$  ($\gamma=7/5$)")
    axA.set_ylabel(r"$\delta_{dis}(r)$")
    axA.set_title("A. dominance window (all probes here PASS)", fontsize=10)
    axA.legend(loc="upper left", fontsize=7.6)

    # ---- Panel B: probe x plant detection-threshold matrix, BLIND cells marked ----------
    probe_names = list(probes.keys())
    plant_names = list(plants.keys())
    import math
    mat = []
    blind_mask = []
    for pn in probe_names:
        row = []
        blind_row = []
        for qn in plant_names:
            cell = plants[qn][pn]
            blind_row.append(cell["blind"])
            thr = cell["detection_threshold"]
            if cell["blind"] or thr is None:
                row.append(float("nan"))
            elif thr <= 0.0:
                row.append(-20.0)  # already fails unplanted -- KA8's row
            else:
                row.append(math.log10(thr))
        mat.append(row)
        blind_mask.append(blind_row)

    im = axB.imshow(mat, aspect="auto", cmap="viridis_r")
    axB.set_xticks(range(len(plant_names)))
    axB.set_xticklabels(plant_names, fontsize=9)
    axB.set_yticks(range(len(probe_names)))
    axB.set_yticklabels(probe_names, fontsize=8)
    for i, pn in enumerate(probe_names):
        for k, qn in enumerate(plant_names):
            if blind_mask[i][k]:
                axB.text(k, i, "BLIND", ha="center", va="center", fontsize=6.5, color="white")
            elif pn == "KA8":
                axB.text(k, i, "FAILS\nunplanted", ha="center", va="center",
                          fontsize=6, color="#ff6b6b", fontweight="bold")
    cbar = fig.colorbar(im, ax=axB, fraction=0.046, pad=0.04)
    cbar.set_label(r"$\log_{10}$(detection threshold)", fontsize=8)
    axB.set_title("B. probe x plant sensitivity", fontsize=10)

    # ---- Panel C: double vs 60-digit k(1+h) -- the KA8 conditioning defect, at its
    #      MEASURED magnitude, unsmoothed ----------------------------------------------
    hs = [max(row["h"], 1e-16) for row in loss_curve]
    abs_err = [row["abs_err"] for row in loss_curve]
    axC.loglog(hs, abs_err, "o-", color="#dc2626", lw=1.5, ms=4,
               label=r"$|k_{double}(1+h) - k_{hp}(1+h)|$")
    axC.axhline(tol_k_at_1, color="#6b7280", lw=1.0, ls="--", label="KA8 tolerance (1e-9)")
    axC.plot([hs[0]], [abs_err[0]], "*", color="#7f1d1d", ms=16, zorder=5)
    axC.annotate(
        "r=1: |k(1)-1| = %.4e\n= %.3fx the 1e-9 tolerance\n(FAIL, not rounded away)"
        % (dev_k_at_1, ka8_ratio),
        xy=(hs[0], abs_err[0]), xytext=(hs[0] * 3, abs_err[0] * 0.15),
        fontsize=7.8, color="#7f1d1d",
        arrowprops=dict(arrowstyle="->", color="#7f1d1d", lw=0.8))
    axC.set_xlabel(r"$h = r - 1$")
    axC.set_ylabel("absolute error vs 60-digit reference")
    axC.set_title("C. KA8: cancellation defect at r=1 (129.048x tol)", fontsize=10)
    axC.legend(loc="lower right", fontsize=7.6)

    fig.suptitle(
        "fig69 -- Route-P2T1 v1 (leg 302): gate = NO. 10/11 known-answer probes pass; "
        "KA8 fails %.3fx its pre-stated tolerance "
        "(transcription correct, IEEE-double evaluation ill-conditioned at r=1). "
        "Redrawn from writeup/data/p2_route_p2t1_v1.json alone (leg 327), no re-run."
        % ka8_ratio, fontsize=10.5, y=1.03)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=150, bbox_inches="tight")
    plt.close(fig)

    n_ok = sum(1 for _, ok, _ in CHECKS if ok)
    print("\n%d/%d checks pass" % (n_ok, len(CHECKS)))
    print(os.path.basename(FIG))
    if n_ok != len(CHECKS):
        sys.exit(1)


if __name__ == "__main__":
    main()
