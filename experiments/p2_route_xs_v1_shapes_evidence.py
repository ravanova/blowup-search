"""Phase-2 Route-XS v1 (fig52): the shape dichotomy, measured, and the published record.

Legs 51-53 explained Route-TC's failure with lesson 87 -- the tail estimate needs a
MULTIPLIER and this operator is a SHIFT.  This figure is that sentence's external check.

Panel A is the whole result as one picture: the tail inverse's ladder in the split `K`,
for the continuous dial from shift to multiplier.  Every `mu > 0` curve falls; the single
`mu = 0` curve RISES.  Panel B says why `mu = 0` has to be bordered at all -- unbordered
it grows linearly in `M`, i.e. the inverse does not exist in the limit -- and that
bordering fixes existence but not size.  Panel C is the published record classified, each
row traced to a located full-text statement.  Panel D is the hypothesis this leg posed and
killed: BDL's `delta < 1/2` is not the coordinate the behaviour turns on.

Rebuild fig52 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_xs_v1_shapes_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_xs_v1_shapes.py
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
JSON = DATA / "p2_route_xs_v1_shapes.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    dial = d["XS3_measured_dial"]["rows"]
    fig, ax = plt.subplots(2, 2, figsize=(15.0, 10.4))

    # ---- A: the ladder in K -- the dichotomy in one panel -----------------
    a = ax[0, 0]
    for r in dial:
        shift = (r["mu"] == 0.0)
        a.loglog(r["K"], r["tail_inverse"],
                 marker="o" if shift else "s", ms=7 if shift else 4.5,
                 lw=2.6 if shift else 1.5,
                 color=C["bad"] if shift else C["good"],
                 alpha=1.0 if shift else 0.45 + 0.12 * min(4, r["mu"]),
                 label=(r"$\mu=0$ SHIFT (bordered): $K^{%+.2f}$" % r["K_exponent"]
                        if shift else r"$\mu=%g$: $K^{%+.2f}$" % (r["mu"], r["K_exponent"])),
                 zorder=5 if shift else 2)
    a.set_xlabel("split $K$")
    a.set_ylabel(r"$\|$tail inverse$\|_w$   (flat $\ell^1$)")
    a.set_title("A  The tail inverse's ladder in $K$:\n"
                "one curve rises, and it is the one with no diagonal", fontsize=11)
    a.legend(fontsize=7.2, loc="lower left", ncol=2, framealpha=0.95,
             borderpad=0.5, columnspacing=1.0, handlelength=1.6)
    a.grid(alpha=0.25, which="both")
    a.text(0.985, 0.60,
           "a radii-polynomial tail\nestimate needs this to FALL",
           transform=a.transAxes, ha="right", va="top", fontsize=8.6, style="italic",
           color=C["grey"])

    # ---- B: does the inverse even EXIST?  growth in M at mu = 0 ----------
    b = ax[0, 1]
    m = d["XS3a_shift_M_divergence"]
    b.loglog(m["M"], m["unbordered"]["vals"], "o-", color=C["bad"], lw=2.4, ms=7,
             label=r"unbordered: $M^{%+.2f}$ — no limit" % m["unbordered"]["exponent_in_M"])
    b.loglog(m["M"], m["bordered"]["vals"], "s-", color=C["anchor"], lw=2.4, ms=6,
             label=r"bordered (leg 52): $M^{%+.2f}$ — saturates"
                   % m["bordered"]["exponent_in_M"])
    b.set_xlabel("tail truncation $M$   (at fixed split $K=8$)")
    b.set_ylabel(r"$\|$tail inverse$\|_w$")
    b.set_title("B  Why $\\mu=0$ must be bordered at all —\n"
                "and what bordering does and does not buy", fontsize=11)
    b.legend(fontsize=8.4, loc="upper left")
    b.grid(alpha=0.25, which="both")
    b.text(0.97, 0.42,
           "bordering fixes EXISTENCE (this panel),\nnot SIZE (panel A)",
           transform=b.transAxes, ha="right", va="top", fontsize=8.6, style="italic",
           color=C["grey"])

    # ---- C: the published record, classified --------------------------------
    c = ax[1, 0]
    c.axis("off")
    rows = d["XS1_ledger"]["rows"]
    c.set_title("C  The published record, each row traced to a located\n"
                "full-text statement (never an abstract)", fontsize=11)
    hdr = ["", "radii\npoly?", "unbounded\npart", "approx.\ninverse", "tail inv.\ndecays?"]
    cells, colours = [], []
    for r in rows:
        short = {"MULTIPLIER": "multiplier", "TRIDIAGONAL_DOMINANT": "tridiag-dom",
                 "SHIFT": "SHIFT", "NO_UNBOUNDED_PART": "(none)"}[r["unbounded_part"]]
        inv = {"BLOCK_DIAGONAL": "block-diag", "NOT_BLOCK_DIAGONAL": "NOT block-diag",
               "FINITE_JACOBIAN": "finite Jac.",
               "NO_APPROXIMATE_INVERSE": "none built"}[r["approx_inverse"]]
        dec = {True: "yes", False: "no", None: "n/a"}[r["tail_inverse_decays"]]
        cells.append([f"{r['tag']}\n{r['arxiv'].split(' ')[0]}",
                      "yes" if r["is_radii_polynomial"] else "no", short, inv, dec])
        colours.append(C["bad"] if r["unbounded_part"] == "SHIFT" else C["anchor"])
    t = c.table(cellText=cells, colLabels=hdr, loc="center", cellLoc="center")
    t.auto_set_font_size(False)
    t.set_fontsize(8.2)
    t.scale(1.0, 2.25)
    for j in range(len(hdr)):
        t[0, j].set_text_props(weight="bold")
    for i, col in enumerate(colours, start=1):
        t[i, 0].set_text_props(weight="bold", color=col)
    g = d["XS2_gate"]
    c.text(0.5, 0.045,
           f"gate: is there a published radii-polynomial certificate with a SHIFT\n"
           f"unbounded part whose tail inverse does not decay?   →   "
           f"{g['answer'].upper()}   (0 of {g['n_rows_examined']})\n"
           f"the same predicate answers YES on a fictitious control row — it is live",
           transform=c.transAxes, ha="center", fontsize=8.6,
           bbox=dict(fc="#f4f4f4", ec=C["grey"], lw=0.8, pad=5.0))

    # ---- D: the hypothesis that died ---------------------------------------
    e = ax[1, 1]
    mus = [r["mu"] for r in dial]
    kexp = [r["K_exponent"] for r in dial]
    cols = [C["bad"] if r["mu"] == 0.0 else C["good"] for r in dial]
    x = np.arange(len(mus))
    e.bar(x, kexp, color=cols, width=0.62)
    e.axhline(0.0, color="k", lw=1.1)
    e.axvline(3.0, color=C["warn"], ls="--", lw=1.8)
    e.text(3.06, max(kexp) * 0.62,
           "BDL's $\\delta<1/2$\nis $\\mu>1$ — the\nhypothesis said the\ntransition is HERE",
           fontsize=8.2, color=C["warn"], va="top")
    e.set_xticks(x)
    e.set_xticklabels([r"$\mu=%g$" % m for m in mus], fontsize=8.6)
    e.set_ylabel(r"$d\log\|\cdot\|\,/\,d\log K$   (negative = decays)")
    e.set_title("D  The hypothesis this leg posed and KILLED:\n"
                "the hinge is zero-vs-nonzero diagonal, not $\\delta$", fontsize=11)
    e.grid(alpha=0.25, axis="y")
    dh = d["XS4_dead_hypothesis"]
    e.text(0.5, -0.185,
           f"$\\mu=0.25$ has $\\delta={dh['test']['bdl_delta']:g}$, four times OUTSIDE BDL's "
           f"admissible set,\nand still decays at {dh['test']['K_exponent']:+.2f} — "
           "indistinguishable from $\\mu=2$.  Verdict: REFUTED.",
           transform=e.transAxes, ha="center", fontsize=8.6, style="italic")

    fig.suptitle("Route-XS v1 (leg 57) — the shape dichotomy against the published record: "
                 "the classification holds, and it is NOT this leg's finding",
                 fontsize=12.5, y=0.985)
    fig.tight_layout(rect=(0, 0.028, 1, 0.962))
    fig.text(0.5, 0.004,
             "The dichotomy is folklore in print (Cadiot arXiv:2505.03091 §2, §3). "
             "What is new here is only that it is executable and traced. "
             "No link of the L1→L4 chain moved.",
             ha="center", fontsize=8.4, color=C["grey"])
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig52_route_xs_v1_shapes.png"
    fig.savefig(out, dpi=145)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
