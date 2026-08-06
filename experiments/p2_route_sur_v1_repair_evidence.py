"""Phase-2 Route-SUR v1 (fig61): the dealias-boundary repair, and the measured no-op that
licensed it.

Leg 129 repaired what leg 120 measured and was forbidden to patch: both 2/3-rule masks in this
repository (`solver/spectral_utils.dealias_mask` and `solver/boussinesq.dealias_mask2d`) cut at
`k <= n/3`, where the alias-free condition is `k < n/3` strictly, so whenever 3 divided n they
retained one Fourier mode too many and that mode beat with itself straight back into the
retained band. Five silent-absorption defects in the same 1D module were closed in the same
commit, and seven pinned regression checks were inverted.

THE POINT OF THIS FIGURE IS THE LICENCE, NOT THE FIX. A repair to a shared numerical core that
every solver imports is only allowed here if it provably moves nothing that has already been
banked. Panel B is that proof and it is a real measurement, not a restatement: the pre-repair
`solver/` tree is read out of git, run in a separate interpreter, and compared against the
repaired tree by sha256 of raw array bytes and hex floats. 0 of 156 power-of-two and banked
quantities moved -- including three end-to-end gCLM integrations at n = 64 and a Boussinesq
integration at n = 32 -- while 33 of 33 quantities at 3 | n moved, which is what proves the
comparison was capable of reporting a difference at all (lesson 90).

Rebuild fig61 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_sur_v1_repair_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_sur_v1_repair.py

Six panels: A the boundary itself, and where the two cuts differ; B the bitwise A/B with its
live control; C energy_production's alias error before and after, per 3 | n grid; D the
alias-free guarantee across all 23 probe grids; E the five absorption defects, before and
after; F the banked-record census and the gate answer.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "writeup" / "data"
FIGS = ROOT / "writeup" / "figures"
JSON = DATA / "p2_route_sur_v1_repair.json"

C_BEFORE, C_AFTER, C_CTRL, C_GREY = "#dc2626", "#059669", "#2563eb", "#6b7280"


def main():
    d = json.loads(JSON.read_text())
    FIGS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(2, 3, figsize=(15.5, 8.6))
    fig.suptitle("Route-SUR v1 (leg 129) — the dealias-boundary repair, and the measured "
                 "no-op that licensed it", fontsize=12.5, y=0.985)

    # ---- A: the boundary, and exactly where the two cuts differ -------------------------
    a = ax[0, 0]
    ns = np.arange(4, 61)
    old = np.floor(ns / 3.0)            # the pre-repair cut: k <= n/3
    new = (ns - 1) // 3                 # the repaired cut:   k <  n/3
    a.step(ns, old, where="mid", color=C_BEFORE, lw=2.0, label="before:  k ≤ n/3")
    a.step(ns, new, where="mid", color=C_AFTER, lw=1.4, ls="--", label="after:  k ≤ (n−1)//3")
    diff = ns[old != new]
    a.plot(diff, old[old != new], "o", ms=4.5, color=C_BEFORE, zorder=5)
    a.set_title("A · the cut: top retained mode K(n)", fontsize=10.5)
    a.set_xlabel("grid size n")
    a.set_ylabel("largest retained wavenumber K")
    a.legend(loc="upper left", fontsize=8.5)
    id_ = d["A1_identity"]
    a.text(0.97, 0.06,
           f"differs only at 3 | n\n{id_['n_changed']}/{id_['n_tested']} of n = 1..5000\n"
           f"{id_['counterexamples']} counterexamples to\nK = (n−1)//3 < n/3",
           transform=a.transAxes, ha="right", va="bottom", fontsize=8,
           bbox=dict(boxstyle="round,pad=0.4", fc="#fef2f2", ec=C_BEFORE, alpha=0.9))

    # ---- B: the bitwise A/B -- THE LICENCE ----------------------------------------------
    b = ax[0, 1]
    ab = d["A2_A3_bitwise_ab"]
    names, tot, mov = [], [], []
    short = {"1D mask, declared power-of-two grids": "1D mask,\npow-2 grids",
             "2D mask, banked n = 32": "2D mask,\nn = 32",
             "every helper + energy_production, declared grids": "every helper,\npow-2 grids",
             "END-TO-END solver runs (gCLM n=64 x3, Boussinesq n=32)": "END-TO-END\nsolver runs",
             "1D mask at 3 | n  <-- MUST differ; this is the control": "1D mask at 3|n\n(CONTROL)"}
    for k, v in ab["buckets"].items():
        names.append(short.get(k, k))
        tot.append(v["quantities"])
        mov.append(v["differing"])
    y = np.arange(len(names))
    b.barh(y, tot, color="#e5e7eb", ec=C_GREY, lw=0.6, label="quantities compared")
    cols = [C_CTRL if "CONTROL" in n else C_AFTER for n in names]
    b.barh(y, mov, color=cols, ec="none", label="quantities that MOVED")
    for i, (t, m) in enumerate(zip(tot, mov)):
        b.text(t + 1.2, i, f"{m}/{t}", va="center", fontsize=8.5,
               color=C_CTRL if "CONTROL" in names[i] else C_AFTER, fontweight="bold")
    b.set_yticks(y)
    b.set_yticklabels(names, fontsize=8)
    b.invert_yaxis()
    b.set_xlabel("quantities (sha256 of raw bytes / hex floats)")
    b.set_title("B · bitwise A/B vs the PRE-REPAIR tree read out of git", fontsize=10.5)
    b.legend(loc="upper right", fontsize=8)
    b.set_xlim(0, max(tot) * 1.28)
    b.text(0.97, 0.04,
           f"{ab['banked_quantities_moved']} of "
           f"{sum(tot) - ab['buckets'][[k for k in ab['buckets'] if 'CONTROL' in short.get(k, k)][0]]['quantities']}"
           f" banked quantities moved\n"
           f"{ab['div3_control_moved']} of "
           f"{ab['buckets'][[k for k in ab['buckets'] if 'CONTROL' in short.get(k, k)][0]]['quantities']}"
           f" control quantities moved\n→ the harness could report a difference",
           transform=b.transAxes, ha="right", va="bottom", fontsize=8.5,
           bbox=dict(boxstyle="round,pad=0.4", fc="#eff6ff", ec=C_CTRL, alpha=0.95))

    # ---- C: energy_production, before vs after -----------------------------------------
    c = ax[0, 2]
    rows = d["B1_energy_production"]["rows"]
    xs = np.arange(len(rows))
    before = [r["rel_err_before"] for r in rows]
    after = [max(r["rel_err_after"], 1e-18) for r in rows]
    c.bar(xs - 0.2, before, 0.4, color=C_BEFORE, label="before repair")
    c.bar(xs + 0.2, after, 0.4, color=C_AFTER, label="after repair")
    c.set_yscale("log")
    c.set_xticks(xs)
    c.set_xticklabels([str(r["n"]) for r in rows], fontsize=8)
    c.set_xlabel("grid size n (all divisible by 3)")
    c.set_ylabel("relative error vs alias-free reference")
    c.set_title("C · energy_production — the “Exact rate dE/dt”", fontsize=10.5)
    c.axhline(2.47e-14, color=C_GREY, ls=":", lw=1.2,
              label="2.47e-14 — the round-off class at 3∤n")
    c.legend(loc="lower left", fontsize=7.6)
    c.text(0.97, 0.95,
           f"worst {d['B1_energy_production']['worst_before']:.3e}\n"
           f"  →  {d['B1_energy_production']['worst_after']:.3e}\n"
           f"{d['B1_energy_production']['decades_gained']:.1f} decades",
           transform=c.transAxes, ha="right", va="top", fontsize=8,
           bbox=dict(boxstyle="round,pad=0.35", fc="#ecfdf5", ec=C_AFTER, alpha=0.95))

    # ---- D: the alias-free guarantee ----------------------------------------------------
    e = ax[1, 0]
    g = d["B2_guarantee"]
    cats = ["3 | n\n(11 grids)", "3 ∤ n\n(12 grids)"]
    bef = [g["leg120_div3"], 4.83e-16]
    aft = [max(g["worst_spurious_div3"], 1e-18), max(g["worst_spurious_not_div3"], 1e-18)]
    xs2 = np.arange(2)
    e.bar(xs2 - 0.2, bef, 0.4, color=C_BEFORE, label="before repair")
    e.bar(xs2 + 0.2, aft, 0.4, color=C_AFTER, label="after repair")
    e.set_yscale("log")
    e.set_xticks(xs2)
    e.set_xticklabels(cats, fontsize=9)
    e.set_ylabel("spurious self-beat coefficient at mode K")
    e.set_title("D · Bowman's experiment: put the field on K, square it", fontsize=10.5)
    e.legend(loc="upper right", fontsize=8)
    e.set_ylim(1e-18, 1e2)
    e.text(0.5, 0.30,
           "the 3∤n column NEVER moved — that is what\nshows the repair did not relocate "
           "the defect",
           transform=e.transAxes, ha="center", va="bottom", fontsize=8,
           bbox=dict(boxstyle="round,pad=0.35", fc="#f9fafb", ec=C_GREY, alpha=0.95))

    # ---- E: the five absorption defects -------------------------------------------------
    f = ax[1, 1]
    c1 = d["C1_absorption"]
    labels = ["D3 Nyquist\npoison propagates", "D4 mean-mode\npoison propagates",
              "D5 int input\nnot truncated", "D6 malformed k\nrefused",
              "D7 degenerate n\nrefused"]
    before_f = [0 / 12, 0 / 3, 0.0, 7 / 15, 0 / 15]
    after_f = [c1["D3_propagated"] / 12, c1["D4_propagated"] / 3, 1.0,
               c1["D6_refused"] / c1["D6_cases"], c1["D7_refused"] / c1["D7_cases"]]
    y2 = np.arange(len(labels))
    f.barh(y2 - 0.2, before_f, 0.4, color=C_BEFORE, label="before repair")
    f.barh(y2 + 0.2, after_f, 0.4, color=C_AFTER, label="after repair")
    ann = [f"{c1['D3_propagated']}/12", f"{c1['D4_propagated']}/3",
           f"{c1['D5_dtype']}", f"{c1['D6_refused']}/{c1['D6_cases']}",
           f"{c1['D7_refused']}/{c1['D7_cases']}"]
    for i, t in enumerate(ann):
        f.text(1.02, i + 0.2, t, va="center", fontsize=8, color=C_AFTER, fontweight="bold")
    f.set_yticks(y2)
    f.set_yticklabels(labels, fontsize=8)
    f.invert_yaxis()
    f.set_xlim(0, 1.35)
    f.set_xlabel("fraction of adversarial cases handled correctly")
    f.set_title("E · the five silent-absorption defects", fontsize=10.5)
    f.legend(loc="lower right", fontsize=8)

    # ---- F: the census and the gate ------------------------------------------------------
    h = ax[1, 2]
    h.axis("off")
    cen = d["A4_census"]
    lines = [
        ("GATE (DIRECTION.md leg 129)", "bold"),
        ("", ""),
        (f"(a) both masks strict, bit-identical on every", ""),
        (f"    banked grid:  {ab['banked_quantities_moved']} of "
         f"{ab['quantities_compared']} compared quantities moved", "g"),
        (f"    {cen['records_affected']} of {cen['records']} banked "
         f"energy_balance_residual", "g"),
        (f"    records affected, in {len(cen['files'])} files", "g"),
        ("", ""),
        (f"(b) alias error at 3 | n:", ""),
        (f"    {d['B1_energy_production']['worst_before']:.4e}  →  "
         f"{d['B1_energy_production']['worst_after']:.4e}", "g"),
        ("", ""),
        (f"(c) five absorption defects closed,", ""),
        (f"    7 pins inverted, 11/11 checks pass", "g"),
        ("", ""),
        ("→ GATE ANSWERS YES ON ALL THREE CLAUSES", "bold"),
        ("", ""),
        ("⚠ PARKED under escalation #4:", "bold"),
        (f"    the 2D floor moves n≥{d['C2_escalation']['floor_before']} → "
         f"n≥{d['C2_escalation']['floor_after']}, moving", "r"),
        (f"    {d['C2_escalation']['cases_moved']} of "
         f"{d['C2_escalation']['cases_total']} banked verdicts (louder; 0 quieter)", "r"),
        ("", ""),
        (f"declared grids on the dealias path:", ""),
        (f"  {cen['declared_grids']}", "grey"),
        (f"  divisible by 3: {len(cen['exposed_grids'])}  → the defect was LATENT", "grey"),
    ]
    yy = 0.97
    for txt, style in lines:
        h.text(0.0, yy, txt, transform=h.transAxes, va="top", fontsize=9.2,
               fontweight="bold" if style == "bold" else "normal",
               color={"g": C_AFTER, "grey": C_GREY, "r": C_BEFORE}.get(style, "#111827"),
               family="monospace" if style in ("g", "grey", "r") else None)
        yy -= 0.0505
    h.set_title("F · the gate, and what was ever at risk", fontsize=10.5)

    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig61_route_sur_v1_repair.png"
    fig.savefig(out)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
