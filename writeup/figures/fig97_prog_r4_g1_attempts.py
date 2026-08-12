"""fig97 -- PROG-R4 unit U3, gate G1: seeded hookstep-Newton attempts on the
named Lucas & Kerswell 2015 Table IV relative periodic orbits.

The figure is deliberately written to be correct in BOTH pre-committed branches
of G1. It plots magnitudes, never a boolean: the final residual reached by every
attempt against the tol=1e-8 line, the residual history of every attempt, and
the relation between how good a seed was and how far the solver got. If G1 is
YES the recovered attempts fall below the line and are marked; if G1 is NO the
same axes show exactly how far short a resourced attempt fell, which is the
deliverable of a resourced null rather than a defect.

Checks assert that the banked JSON supports every claim the panels make. The
script exits non-zero if any check fails.

STATUS 2026-08-12: gate G1 is UNANSWERED and this script HAS NEVER SEEN REAL
DATA -- the programme was wound down mid-U2 and writeup/data/p2_prog_r4_g1_v1
.json does not exist. Running this now will fail on a missing file, which is
the correct behaviour. It has been smoke-tested only against synthetic records
in both gate branches plus two doctored records its checks correctly reject.

Data: writeup/data/p2_prog_r4_g1_v1.json
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
LEG353 = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb5_v1.json")
FIG = os.path.join(HERE, "fig97_prog_r4_g1_attempts.png")

TOL = 1e-8
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail
                                                    else ""))
    return bool(ok)


def main():
    with open(DATA) as f:
        d = json.load(f)
    with open(LEG353) as f:
        prev = json.load(f)

    att = d["attempts"]
    finals = np.array([a["final_residual"] for a in att], float)
    seeds = np.array([a["seed_extended_residual"] for a in att], float)
    anchors = [a["anchor"] for a in att]
    recovered = np.array([a["recovered_named_orbit"] for a in att], bool)
    answer = d["gate"]["answer"]

    # ---- checks on the banked record -----------------------------------
    # UNANSWERED is a THIRD admissible branch, added when the planted controls
    # were wired in (addendum section 3). It is not a softening of the gate: it
    # fires only when the controls did not fire as planted, and it is STRICTER
    # than NO, because a NO is a resourced null that stops route 4 under section
    # 3d and may only be recorded on an instrument shown able to say YES.
    check("gate answer is one of the three pre-committed branches",
          answer in ("YES", "NO", "UNANSWERED"), f"answer={answer}")
    ctrl = d["gate"].get("controls_fired_as_planted")
    raw = d["gate"].get("answer_without_controls")
    check("the controls verdict is banked with the gate",
          ctrl is not None and raw in ("YES", "NO"),
          f"controls_fired={ctrl}, answer_without_controls={raw}")
    check("raw answer agrees with the per-attempt recovery flags",
          (raw == "YES") == bool(recovered.any()),
          f"n_recovered={int(recovered.sum())}")
    check("the controls override is applied exactly as pre-registered",
          answer == (raw if ctrl else "UNANSWERED"),
          f"answer={answer} from raw={raw} with controls_fired={ctrl}")
    # The controls must be able to fire in BOTH directions, so both the
    # positive and the negative must be present and must carry their outcome.
    cb = d.get("controls", {})
    check("planted controls P and N both recorded with outcomes",
          isinstance(cb.get("P"), dict) and isinstance(cb.get("N"), dict)
          and "recovered" in cb.get("P", {}) and "recovered" in cb.get("N", {}),
          f"P.recovered={cb.get('P', {}).get('recovered')}, "
          f"N.recovered={cb.get('N', {}).get('recovered')} (N must be False)")
    check("a NO is never recorded on controls that did not fire",
          not (answer == "NO" and not ctrl))
    check("gate n_recovered matches the attempt rows",
          d["gate"]["n_recovered"] == int(recovered.sum()))
    check("every attempt carries a named Table IV anchor (Ban 2)",
          all(a["anchor"] in d["seed"]["rows"] for a in att),
          f"{len(set(anchors))} distinct anchors over {len(att)} attempts")
    check("seed source named verbatim",
          d["seed"]["source"] ==
          "Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV")
    check("resourced at the scale the question is posed at",
          float(d["resourcing"]["T_dns"]) >= 1e5
          and d["resourcing"]["N"] == 24
          and len(att) >= 100
          and d["resourcing"]["globalisation"].startswith("genuine"),
          f"T={d['resourcing']['T_dns']:.3g}, N={d['resourcing']['N']}, "
          f"{len(att)} attempts")
    check("tol banked as 1e-8", float(d["resourcing"]["tol"]) == TOL)
    check("recovery flags are consistent with the residuals they claim",
          all((not a["recovered_named_orbit"]) or a["final_residual"] <= TOL
              for a in att))
    check("CLAY_OBLIGATIONS section 4 carried OPEN in this gate",
          any("section 4" in s and "OPEN" in s
              for s in d["open_obligations_carried"]))
    check("no Clay movement asserted", d["clay_movement"].startswith("none"))
    check("leg 353 comparison baseline present",
          prev["newton_attempts"] and not prev["any_converged"],
          f"leg 353: {len(prev['newton_attempts'])} attempts, "
          f"any_converged={prev['any_converged']}")

    prev_finals = np.array([a["final_residual"] for a in prev["newton_attempts"]],
                           float)

    # ---- figure ---------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.6))

    ax = axes[0]
    order = np.argsort(finals)
    x = np.arange(1, len(finals) + 1)
    ax.semilogy(x, finals[order], "o", ms=4, color="#2b6cb0",
                label="this unit (seeded hookstep-Newton)")
    if recovered.any():
        rx = np.array([i + 1 for i, j in enumerate(order) if recovered[j]])
        ax.semilogy(rx, finals[order][rx - 1], "*", ms=14, color="#c53030",
                    label="recovered a named Table IV orbit")
    ax.axhline(TOL, color="k", ls="--", lw=1.2, label=f"tol = {TOL:g}")
    for k, v in enumerate(np.sort(prev_finals)):
        ax.axhline(v, color="#a0aec0", lw=0.8, ls=":",
                   label="leg 353 attempts (line search, 5)" if k == 0 else None)
    ax.set_xlabel("attempt, sorted by final residual")
    ax.set_ylabel(r"final $\|R\|$")
    ax.set_title(f"A. where each attempt stopped  (G1 = {answer})")
    ax.legend(fontsize=7, loc="lower right")
    ax.grid(alpha=0.3, which="both")

    ax = axes[1]
    for a in att:
        h = np.array(a["residual_history"], float)
        ax.semilogy(np.arange(len(h)), h, lw=0.7, alpha=0.45,
                    color="#c53030" if a["recovered_named_orbit"] else "#2b6cb0")
    ax.axhline(TOL, color="k", ls="--", lw=1.2)
    ax.set_xlabel("Newton iteration")
    ax.set_ylabel(r"$\|R\|$")
    ax.set_title("B. residual history, every attempt")
    ax.grid(alpha=0.3, which="both")

    ax = axes[2]
    names = sorted(set(anchors))
    cmap = plt.get_cmap("tab10")
    for i, nm in enumerate(names):
        m = np.array([a == nm for a in anchors], bool)
        ax.loglog(seeds[m], finals[m], "o", ms=5, color=cmap(i % 10), label=nm,
                  alpha=0.8)
    ax.axhline(TOL, color="k", ls="--", lw=1.2)
    lim = [seeds.min() * 0.5, seeds.max() * 2]
    ax.plot(lim, lim, color="#a0aec0", lw=0.8, ls=":")
    ax.set_xlim(lim)
    ax.set_xlabel(r"seed $\|R\|$ (extended residual at the recurrence guess)")
    ax.set_ylabel(r"final $\|R\|$")
    ax.set_title("C. seed quality vs. how far Newton got")
    ax.legend(fontsize=7, ncol=2)
    ax.grid(alpha=0.3, which="both")

    fig.suptitle(
        "fig97  PROG-R4 U3 / gate G1: seeded recovery of named Lucas & Kerswell "
        "2015 Table IV RPOs, Re=60, N=24, "
        f"T_DNS={float(d['resourcing']['T_dns']):.3g}",
        fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG, dpi=150)
    print(f"wrote {FIG}")

    bad = [n for n, ok, _ in CHECKS if not ok]
    print(f"\n{len(CHECKS) - len(bad)}/{len(CHECKS)} checks passed")
    if bad:
        print("FAILED: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
