"""Route-APIA v1 (leg 312) -- EVIDENCE: every number the BLOG and TECHNICAL write-ups
quote, re-derived from `writeup/data/p2_route_apia_v1.json`. Also builds
`writeup/figures/fig73_route_apia_v1.png`.

Nothing expensive is recomputed here -- this reads the curated JSON (already produced by
`experiments/p2_route_apia_v1.py`, which is the one script that runs the actual arbitrary-
precision arithmetic) and asserts the relations the prose asserts.

    .venv/bin/python experiments/p2_route_apia_v1_evidence.py
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig73_route_apia_v1.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-64s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_apia_v1.json")) as fh:
        j = json.load(fh)["leg_312_route_apia"]
    l178, l176 = j["leg178"], j["leg176"]

    # ---- leg 178 -----------------------------------------------------------
    gap_before = l178["before_banked_n_grade_96"]["gap"]
    gap_after = l178["after_mp_patched_n_grade_96"]["gap"]
    contam_before = l178["before_banked_n_grade_96"]["contamination"]
    check("(178a) banked gap at n_grade=96 matches the journal's -230.7108028",
          abs(gap_before - (-230.7108027866136)) < 1e-6, f"{gap_before}")
    check("(178b) banked contamination matches the journal's 3.066e+03",
          abs(contam_before - 3066.38495045281) < 1e-3, f"{contam_before}")
    check("(178c) MP-patched gap recovers the +0.5 ceiling, not the -230.71 reading",
          abs(gap_after - 0.5) < 1e-6, f"{gap_after}")
    check("(178d) MP-patched gap is within the n_grade=12..48 clean-depth spread",
          abs(gap_after - l178["before_banked_n_grade_48_crosscheck"]["gap"]) < 1e-5,
          f"after={gap_after} vs n_grade=48 clean={l178['before_banked_n_grade_48_crosscheck']['gap']}")
    check("(178e) float64 re-derivation reproduces the banked reading exactly",
          l178["float64_reproduction_check_n_grade_96"]["gap"] == gap_before, "")
    check("(178f) spot check against the rigorous MPInterval dsin/dcos holds",
          l178["spot_check_vs_rigorous_mpinterval"]["all_contained"], "")
    check("(178g) performance: under the 10-minute budget",
          l178["performance"]["total_seconds"] < 600,
          f"{l178['performance']['total_seconds']:.1f}s")

    # ---- leg 176 -------------------------------------------------------------
    smin_before = l176["before_banked_N1024"]["sigma_min"]
    smin_after = l176["after_mp_N1024"]["sigma_min"]
    smin_512 = l176["before_banked_N512_crosscheck"]["sigma_min"]
    check("(176a) banked N=1024 sigma_min matches leg 176's own ladder",
          abs(smin_before - 0.09093626075500859) < 1e-9, f"{smin_before}")
    check("(176b) banked N=1024 BREAKS the ladder's own monotone-non-increasing shape",
          smin_before > smin_512, f"N1024={smin_before} > N512={smin_512}")
    check("(176c) MP-patched N=1024 RESTORES monotonicity (falls below N=512)",
          smin_after < smin_512, f"N1024_mp={smin_after} < N512={smin_512}")
    check("(176d) MP-patched N=512 cross-check agrees with the banked reliable-window value",
          abs(l176["after_mp_N512_crosscheck"]["sigma_min"] - smin_512) < 1e-4, "")
    check("(176e) performance: under the 10-minute budget",
          l176["performance"]["total_seconds"] < 600,
          f"{l176['performance']['total_seconds']:.1f}s")

    # ---- figure --------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    ax = axes[0]
    depths = [12, 24, 48, 96]
    # gaps at the three clean depths (12,24,48) come from the gap_ladder pattern; only
    # 48 and 96 are carried in this leg's own JSON (96 both ways, 48 as the crosscheck),
    # so the plot shows the two directly-measured points plus the two re-measured ones.
    ax.axhline(0.5, color="#999", ls=":", lw=1, label="Xu's modulated ceiling, 1/2")
    ax.scatter([48, 96], [l178["before_banked_n_grade_48_crosscheck"]["gap"], gap_before],
               color="crimson", marker="x", s=70, label="banked (float64)", zorder=5)
    ax.scatter([96], [gap_after], color="royalblue", marker="o", s=70,
               label="arbitrary precision (leg 312)", zorder=6)
    ax.set_xlabel("n_grade"); ax.set_ylabel("coercivity gap")
    ax.set_title("Leg 178: T2_egm | E_egm, n=128, gamma=4\nfloat64 catastrophic cancellation "
                  "at theta~3e-31", fontsize=9.5)
    ax.legend(fontsize=8)

    ax = axes[1]
    Ns = [512, 1024]
    ax.plot(Ns, [smin_512, smin_before], "x--", color="crimson", label="banked (float64)")
    ax.plot(Ns, [l176["after_mp_N512_crosscheck"]["sigma_min"], smin_after], "o-",
            color="royalblue", label="arbitrary precision (leg 312)")
    ax.set_xlabel("N"); ax.set_ylabel(r"$\sigma_{\min}$")
    ax.set_title("Leg 176: rect_sigma ladder\nfloat64 breaks monotonicity at N=1024",
                  fontsize=9.5)
    ax.legend(fontsize=8)

    fig.suptitle("Route-APIA (leg 312): arbitrary precision changes both banked headlines",
                 fontweight="bold", y=1.03)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG}")

    n_fail = sum(1 for _, ok, _ in CHECKS if not ok)
    print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed")
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
