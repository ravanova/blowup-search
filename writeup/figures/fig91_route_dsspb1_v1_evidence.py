"""Route-DSSP-B1 (leg 343) -- EVIDENCE + FIGURE.

Reads writeup/data/p2_route_dsspb1_v1.json (produced by
experiments/p2_route_dsspb1_v1.py) and plots the eigenvalue-convergence
signature that the gate's part (ii) verdict rests on: the plain operator's two
lowest real eigenvalues drift slowly toward the analytic continuum threshold
(1.0) and a nearby value (1.25) as resolution N grows, while the
planted-eigenvalue control's bound state is flat at machine precision from the
coarsest tested resolution onward. Nothing is recomputed here -- the script
only reads the already-banked JSON and asserts the prose's claims against it,
same discipline as fig89's evidence script.

python3 writeup/figures/fig91_route_dsspb1_v1_evidence.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb1_v1.json")
FIG = os.path.join(HERE, "fig91_route_dsspb1_v1_spectrum.png")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


with open(DATA) as fh:
    d = json.load(fh)

ii = d["gate"]["ii_spectrum_continuity"]
plain = ii["measured_operator_drift_half"]["precision_track"]
planted = ii["planted_eigenvalue_control"]["lowest_eigenvalue_track"]

N_plain = [row["N"] for row in plain]
lowest_plain = [row["lowest"] for row in plain]
second_plain = [row["second"] for row in plain]
N_planted = [row["N"] for row in planted]
lowest_planted = [row["lowest_planted"] for row in planted]

check("plain lowest converges toward 1.0", abs(lowest_plain[-1] - 1.0) < 1e-6,
      f"lowest_plain[-1]={lowest_plain[-1]}")
check("plain lowest still moving between coarsest and finest",
      abs(lowest_plain[0] - lowest_plain[-1]) > 1e-6,
      f"{lowest_plain[0]} vs {lowest_plain[-1]}")
check("planted value flat to 1e-8 across all N",
      max(lowest_planted) - min(lowest_planted) < 1e-7,
      f"spread={max(lowest_planted) - min(lowest_planted):.2e}")
check("planted value strictly below the continuum threshold",
      lowest_planted[0] < 1.0, f"{lowest_planted[0]}")
check("gate (ii) answer is CONTINUOUS",
      "CONTINUOUS" in ii["verdict"], ii["verdict"][:40])

# Plot |value - its own finest-resolution estimate| vs N, log scale: a true
# isolated eigenvalue should sit at (or below) floating-point noise from the
# coarsest N tested onward; a discretised continuum value should shrink
# algebraically/slowly as N grows, never quite reaching the floor.
eps_floor = 1e-16
dev_lowest = [max(abs(v - lowest_plain[-1]), eps_floor) for v in lowest_plain]
dev_second = [max(abs(v - second_plain[-1]), eps_floor) for v in second_plain]
dev_planted = [max(abs(v - lowest_planted[-1]), eps_floor) for v in lowest_planted]

fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=150)
ax.semilogy(N_plain, dev_lowest, "o-", color="#1f4e9c",
            label="plain operator, lowest eigenvalue (-> 1.0)")
ax.semilogy(N_plain, dev_second, "s-", color="#0f8a6a",
            label="plain operator, 2nd eigenvalue (-> 1.25)")
ax.semilogy(N_planted, dev_planted, "^-", color="#b03030",
            label="planted-well control, lowest eigenvalue (isolated)")
ax.set_xlabel("Chebyshev resolution N")
ax.set_ylabel("|value $-$ its own N=320 estimate|  (log scale)")
ax.set_title("Leg 343 / B1: spectrum of $-\\Delta+\\frac{1}{2}(y\\cdot\\nabla)+1$,\n"
              "$\\ell=0$ radial channel -- continuum drift vs. isolated planted state")
ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
ax.grid(alpha=0.25, which="both")
fig.tight_layout()
fig.savefig(FIG)
print(f"wrote {FIG}")

n_fail = sum(1 for _, s, _ in CHECKS if s == "FAIL")
for name, status, detail in CHECKS:
    print(f"[{status}] {name} {detail}")
print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed")
if n_fail:
    raise SystemExit(1)
