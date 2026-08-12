"""Route-R3SP (leg 376) -- EVIDENCE + FIGURE.

Reads writeup/data/p2_route_r3sp_v1.json (produced by
experiments/p2_route_r3sp_v1.py) and plots the same eigenvalue-convergence
signature leg 343's fig91 plotted at ell=0, now shown side by side for the
ell=1 and ell=2 channels leg 343 never measured: each plain (drift=1/2)
operator's lowest eigenvalue drifts slowly toward its own analytic continuum
threshold (1.5 at ell=1, 2.0 at ell=2) as resolution N grows, while the
planted-well control's bound state is essentially flat from N=90 onward (the
N=60 point sits slightly off -- reported honestly, not hidden, per
leg_376.md's diagnosis of the higher centrifugal term's slower convergence).
This is a genuine NEW measurement (ell=1/ell=2 had never been computed or
plotted by any prior leg -- leg 348 explicitly refused to transfer leg 343's
ell=0-only finding to these channels), not a replot of an already-banked
number, so it is warranted per the same distinction leg 341 drew when it
declined a figure. Nothing is recomputed here -- the script only reads the
already-banked JSON and asserts the prose's claims against it, same
discipline as fig91's/fig89's evidence scripts.

python3 writeup/figures/fig96_route_r3sp_v1_evidence.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_r3sp_v1.json")
FIG = os.path.join(HERE, "fig96_route_r3sp_v1_spectrum.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


with open(DATA) as fh:
    d = json.load(fh)

ell1 = d["channel_ell1"]
ell2 = d["channel_ell2"]

check("selftest: ell=0 on this leg's build reproduces leg 343's own numbers",
      d["selftest_ell0_reproduces_leg343"]["reproduces_leg343_ell0_exactly"], "")
check("ell=1 verdict is (some form of) CONTINUOUS",
      "CONTINUOUS" in ell1["verdict"], ell1["verdict"])
check("ell=2 verdict is (some form of) CONTINUOUS",
      "CONTINUOUS" in ell2["verdict"], ell2["verdict"])
check("ell=1 both controls pass leg 343's strict criteria",
      ell1["both_controls_pass"], "")
check("ell=2 planted control converges from N=90 (even though it narrowly "
      "misses the strict all-N-incl-60 spread)",
      ell2["planted_eigenvalue_control"]["isolated_and_converged_to_1e-6_from_N90"],
      "")

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6), dpi=150, sharey=False)
eps_floor = 1e-16
colors = {"lowest": "#1f4e9c", "planted": "#b03030"}

for ax, ch, label in zip(axes, [ell1, ell2], ["$\\ell=1$", "$\\ell=2$"]):
    plain = ch["measured_operator_drift_half"]["precision_track"]
    planted = ch["planted_eigenvalue_control"]["lowest_eigenvalue_track"]
    N_plain = [row["N"] for row in plain]
    lowest_plain = [row["lowest"] for row in plain]
    N_planted = [row["N"] for row in planted]
    lowest_planted = [row["lowest_planted"] for row in planted]

    dev_lowest = [max(abs(v - lowest_plain[-1]), eps_floor) for v in lowest_plain]
    dev_planted = [max(abs(v - lowest_planted[-1]), eps_floor) for v in lowest_planted]

    ax.semilogy(N_plain, dev_lowest, "o-", color=colors["lowest"],
                label=f"plain operator, lowest eigenvalue "
                      f"($\\to$ {ch['analytic_continuum_threshold']})")
    ax.semilogy(N_planted, dev_planted, "^-", color=colors["planted"],
                label="planted-well control, lowest eigenvalue")
    ax.axvline(90 if ch["ell"] == 1 else 90, color="#999999", linestyle=":",
               linewidth=1, alpha=0.7)
    ax.set_xlabel("Chebyshev resolution N")
    verdict_short = "CONTINUOUS" if ch["verdict"].startswith("CONTINUOUS") else ch["verdict"]
    marginal = ch["verdict"] != "CONTINUOUS"
    ax.set_title(f"{label} channel -- {verdict_short}" + (" (marginal control)" if marginal else ""))
    ax.grid(alpha=0.25, which="both")

axes[0].set_ylabel("|value $-$ its own N=320 estimate|  (log scale)")
axes[0].legend(loc="upper right", fontsize=8, framealpha=0.9)
axes[1].legend(loc="upper right", fontsize=8, framealpha=0.9)
fig.suptitle("Leg 376 / R3SP: spectrum of $-\\Delta+\\frac{1}{2}(y\\cdot\\nabla)+1$,\n"
             "$\\ell=1$ and $\\ell=2$ channels -- continuum drift vs. planted control "
             "(dotted line marks N=90, where the planted control catches up)")
fig.tight_layout()
fig.savefig(FIG)
print(f"wrote {FIG}")

n_fail = sum(1 for _, s, _ in CHECKS if s == "FAIL")
for name, status, detail in CHECKS:
    print(f"[{status}] {name} {detail}")
print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed")
if n_fail:
    raise SystemExit(1)
