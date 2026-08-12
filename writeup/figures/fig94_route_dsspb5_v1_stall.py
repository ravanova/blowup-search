"""Route-DSSP-B5 (leg 353) -- EVIDENCE + FIGURE.

Reads writeup/data/p2_route_dsspb5_v1.json (produced by
experiments/p2_route_dsspb5_v1.py). Plots the Newton-Krylov residual history
for every recurrence-seeded attempt at a published UPO (all 5 stall within a
handful of iterations, none within two orders of magnitude of tol=1e-8)
against the laminar-fixed-point CONTROL run of the identical Newton-Krylov +
phase-condition code (99.3% monotone reduction from a seed 0.01*||w_lam||
away from an exact solution) -- the two curve families sitting on opposite
sides of the plot is the leg's central evidence that the extraction layer
itself is not broken (the control converges cleanly) while the recurrence-
search seeds it can afford within this leg's DNS budget are outside the
method's local basin (the real attempts do not converge at all).

Warranted as a NEW measurement (no prior leg ever ran Newton-Krylov on 2D
Kolmogorov flow) -- not a replot of an already-banked number.

Nothing is recomputed here; the script only asserts the banked JSON supports
the claims made about it, same discipline fig89/fig91/fig92's evidence
scripts use.

python3 writeup/figures/fig94_route_dsspb5_v1_stall.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb5_v1.json")
FIG = os.path.join(HERE, "fig94_route_dsspb5_v1_stall.png")

CHECKS = []


def check(name, ok, detail):
    CHECKS.append((name, "PASS" if ok else "FAIL", detail))


def main():
    with open(DATA) as fh:
        d = json.load(fh)

    attempts = d["newton_attempts"]
    control = d["laminar_control"]

    check("5 Newton attempts at published UPOs were run",
          len(attempts) == 5, f"n={len(attempts)}")
    check("none of the 5 attempts converged",
          all(not a["success"] for a in attempts),
          [a["reason"] for a in attempts])
    check("the laminar control DID reduce residual monotonically",
          control["monotone_decrease"] is True, control["monotone_decrease"])
    check("the control's fractional reduction is >>90%% while every real "
          "attempt's best final residual stays >20 (no comparable drop)",
          control["fractional_reduction"] > 0.9
          and all(a["residual_history"][-1] > 20.0 for a in attempts),
          dict(control_reduction=control["fractional_reduction"],
               attempt_finals=[a["residual_history"][-1] for a in attempts]))
    check("gate answer recorded in the JSON is 'no converged orbit'",
          d["any_converged"] is False, d["any_converged"])

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    colors = ["#c0392b", "#e67e22", "#8e44ad", "#2471a3", "#16a085"]
    for a, c in zip(attempts, colors):
        hist = a["residual_history"]
        label = f"{a['target']}[{a['candidate_index']}] (seed rel-res={a['seed_residual']:.2f})"
        ax.plot(range(len(hist)), hist, "o-", color=c, linewidth=1.6,
                markersize=5, label=label)
    ax.plot(range(len(control["residual_history"])), control["residual_history"],
            "s--", color="#2c3e50", linewidth=2.2, markersize=6,
            label="control: laminar fixed point + 1% perturbation")
    ax.set_yscale("log")
    ax.set_xlabel("Newton iteration")
    ax.set_ylabel(r"$\|R(x_k)\|$ (extended residual, state + 2 phase rows)")
    ax.set_title("Route-DSSP brick B5: Newton-Krylov residual history\n"
                  "published-UPO attempts (stall) vs laminar-fixed-point control (converges)")
    ax.legend(loc="upper right", fontsize=7.5)
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG, dpi=150)

    n_pass = sum(1 for _, r, _ in CHECKS if r == "PASS")
    for name, res, detail in CHECKS:
        print(f"{res} {name} :: {detail}")
    print(f"\n{n_pass}/{len(CHECKS)} checks pass -> {FIG}")
    return 0 if n_pass == len(CHECKS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
