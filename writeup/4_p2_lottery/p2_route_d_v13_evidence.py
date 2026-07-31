"""Phase-2 P2 Route-D v13 (fig31): the turning point, and where the wall actually is.

v12 found the a>0 profile ends at X_c and measured that the gauged inverse's graded
norm diverges with J there.  It attributed that to a mode ~ (X_c-X)^{-1/a}, which
is wrong: the mode at X_c VANISHES like (X_c-X)^{+1/a}.  The obstruction is in the
far field, where the same equation gives h ~ (log(X/X_c))^{1/a} -- growth, against
a domain space that is a decay class.  Level-1 tooling + a correction, NOT a
certificate.

Rebuilds fig31 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v13_evidence.py
Regenerate the data (deterministic; ~6 min):
    .venv/bin/python -u experiments/p2_route_d_v13_turning.py

Five panels: A the growing far-field mode; B its exponent against the parameter-free
prediction 1/a (with the a=0.5 row refined rather than dropped); C the inner mode,
which vanishes -- the correction; D the divergence attributed by outer radius, with
the a=0 control; E the cheap repair disqualified.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
JSON = DATA / "p2_route_d_v13_turning.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.0))

    # -- A: the growing mode ------------------------------------------------
    a0 = ax[0, 0]
    curves = [c for c in d["s2_outer_mode"]["curves"] if c["a"] <= 0.4]
    for col, cur in zip(plt.cm.viridis(np.linspace(0.0, 0.8, len(curves))), curves):
        a0.loglog(cur["X"], cur["h"], color=col, lw=1.4, label="a = %.2f" % cur["a"])
    a0.set_xlabel("X"), a0.set_ylabel("homogeneous solution h (h=1 at 1.5 X_c)")
    a0.set_title("A. beyond X_c the linearized mode GROWS")
    a0.legend(fontsize=7, loc="upper left")
    a0.grid(alpha=0.3, which="both")

    # -- B: its exponent vs 1/a --------------------------------------------
    b = ax[0, 1]
    rows = [r for r in d["s2_outer_mode"]["rows"]]
    A = [r["a"] for r in rows]
    b.plot(A, [r["predicted"] for r in rows], "k--", lw=1.2, label="prediction 1/a")
    ok = [r for r in rows if r["a"] <= 0.4]
    b.plot([r["a"] for r in ok], [r["exponent"] for r in ok], "o-",
           color=C["anchor"], ms=6, label="measured (J=400)")
    g = d["s2_outer_mode"]["grid_refinement"]
    for r in [x for x in g if x["a"] == 0.5]:
        b.plot([0.5], [r["exponent"]], "s", color=C["warn"], ms=5)
    b.annotate("a=0.5: profile not\nJ-converged (v12 T4);\nrefines 0.05 -> 1.84 -> 1.70",
               xy=(0.5, 1.0), fontsize=6.5, color=C["warn"], ha="right")
    b.set_xlabel("a"), b.set_ylabel("q in h ~ (log(X/X_c))^q")
    b.set_title("B. the exponent is the profile's own 1/a (<0.6% for a<=0.4)")
    b.legend(fontsize=8)
    b.grid(alpha=0.3)

    # -- C: the inner mode (the correction) ---------------------------------
    c = ax[0, 2]
    s1 = d["s1_correction"]["rows"]
    A1 = [r["a"] for r in s1]
    c.plot(A1, [r["predicted"] for r in s1], "k--", lw=1.2, label="corrected: +1/a")
    c.plot(A1, [-r["predicted"] for r in s1], ":", color=C["bad"], lw=1.4,
           label="v12's claim: -1/a")
    c.plot(A1, [r["inner_exponent"] for r in s1], "o-", color=C["good"], ms=6,
           label="measured")
    c.axhline(0.0, color="k", lw=0.8)
    c.set_xlabel("a"), c.set_ylabel("p in h ~ (X_c - X)^p at X_c")
    c.set_title("C. the mode AT X_c vanishes -- v12 had the sign wrong")
    c.legend(fontsize=8)
    c.grid(alpha=0.3)

    # -- D: the divergence, attributed --------------------------------------
    dd = ax[1, 0]
    for blk, style in zip(d["s3_attribution"]["blocks"], ["o-", "s-", "^-"]):
        cols = {0.0: C["good"], 0.2: C["warn"], 0.3: C["bad"]}
        for k, alpha_ in zip(["20", "50", "200", "inf"], [0.35, 0.55, 0.78, 1.0]):
            dd.loglog([r["J"] for r in blk["rows"]],
                      [r["by_cutoff"][k] for r in blk["rows"]], style,
                      color=cols[blk["a"]], alpha=alpha_, ms=4,
                      label="a=%.1f, X<=%s: J^%+.2f" % (blk["a"], k, blk["slopes"][k]))
    dd.set_xlabel("J"), dd.set_ylabel("||A|| (graded sup-to-sup)")
    dd.set_title("D. the divergence lives in the FAR FIELD, not at X_c")
    dd.legend(fontsize=5.5, ncol=2, loc="upper left")
    dd.grid(alpha=0.3, which="both")

    # -- E: where the extremal row is sourced -------------------------------
    e = ax[1, 1]
    for col, a in zip([C["good"], C["warn"], C["bad"]],
                      sorted({r["a"] for r in d["s4_source"]})):
        rs = [r for r in d["s4_source"] if r["a"] == a]
        e.semilogx([r["J"] for r in rs],
                   [100 * r["near_Xc_fraction"] for r in rs], "o-", color=col,
                   ms=5, label="a = %.1f" % a)
    e.set_ylim(0, 100)
    e.set_xlabel("J"), e.set_ylabel("% of the extremal row's mass")
    e.set_title("E. ... but it is SOURCED within 10% of X_c")
    e.legend(fontsize=8)
    e.grid(alpha=0.3)

    # -- F: the cheap repair disqualified -----------------------------------
    f = ax[1, 2]
    for col, blk in zip([C["good"], C["warn"], C["bad"]],
                        d["s5_repair"]["overdetermined"]):
        f.loglog([r["J"] for r in blk["rows"]], [r["norm"] for r in blk["rows"]],
                 "o-", color=col, ms=5,
                 label="a=%.1f bordered: J^%+.2f" % (blk["a"], blk["log_slope"]))
    plain = [b for b in d["s3_attribution"]["blocks"] if b["a"] == 0.0][0]
    f.loglog([r["J"] for r in plain["rows"]],
             [r["by_cutoff"]["inf"] for r in plain["rows"]], "k--", lw=1.4,
             label="a=0 plain (flat): J^%+.2f" % plain["slopes"]["inf"])
    f.set_xlabel("J"), f.set_ylabel("||A||")
    f.set_title("F. restoring the speed adds KERNEL, not range")
    f.legend(fontsize=7, loc="upper left")
    f.grid(alpha=0.3, which="both")

    fig.suptitle("Route-D v13 - the turning point: the mode at X_c vanishes, the "
                 "mode BEYOND it grows like (log X)^(1/a) (float64, NOT a certificate)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig31_p2_route_d_v13_turning.png"
    fig.savefig(out, dpi=150)
    print("[fig] wrote %s" % out)


if __name__ == "__main__":
    build_figure()
