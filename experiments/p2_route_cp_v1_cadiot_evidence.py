"""Phase-2 Route-CP v1 (fig56): does Cadiot arXiv:2505.03091 cover the zero-diagonal case?

The gate is a literature question and the answer is NO, but the answer is worth nothing
as a boolean -- leg 53 lost a claim by reading a hypothesis off an abstract.  So this
figure shows the hypothesis as a MAGNITUDE, measured through one code path on two
operators: Cadiot's own worked examples, and the a = 0 CLM linearisation this repository
actually built.

Panel A is Lemma 3.2's dominance ratio `r_n / |lambda_n|`, the quantity his generalized
Gershgorin argument needs to control.  On his own capillary-gravity Whitham operator it
DECAYS; on ours it is FLAT at every dissipation `mu > 0` and does not exist at `mu = 0`,
where every row's diagonal is exactly zero.  Panel B is the consequence: the minimum
shift `|s|` his proof needs, versus truncation -- one finite number for him at every
size, and a quantity growing LINEARLY in the truncation for us, so no `s` survives the
limit.  Panel C is Assumption 1 itself, `l_min`, re-derived from his symbols and checked
against the numbers he states in words; ours is exactly zero.

Rebuild fig56 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_cp_v1_cadiot_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_cp_v1_cadiot.py
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
JSON = DATA / "p2_route_cp_v1_cadiot.json"

C = {"cadiot": "#1f4e79", "ours": "#c1440e", "warn": "#e08a1e",
     "good": "#2e7d32", "grey": "#888888", "mid": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    cp4 = d["CP4_lemma_3_2_shift"]
    cp2 = d["CP2_assumption_1_on_cadiots_own_examples"]
    cp6 = d["CP6_thresholds"]
    fig, ax = plt.subplots(1, 3, figsize=(16.6, 6.6))

    # ---------------- A: Lemma 3.2's dominance ratio ----------------
    a = ax[0]
    cur = cp4["ratio_curves"]
    cw = cur["cadiot_whitham_N512"]
    a.loglog(cw["n"], cw["ratio"], color=C["cadiot"], lw=2.6,
             label="Cadiot §5.2 Whitham (his symbol)")
    mus = [k for k in cur if k.startswith("ours_mu_")]
    mus.sort(key=lambda s: float(s.split("_")[-1]))
    shades = plt.cm.Oranges(np.linspace(0.42, 0.95, len(mus)))
    n_infinite = 0
    for col, key in zip(shades, mus):
        mu = float(key.split("_")[-1])
        r = np.array([np.nan if v is None else v for v in cur[key]["ratio"]], float)
        if not np.isfinite(r).any():
            n_infinite = int(r.size)
            continue
        a.loglog(cur[key]["k"], r, color=col, lw=1.7, ls="--",
                 label=rf"ours, $\mu={mu:g}$")
    a.set_ylim(1.5e-1, 6.0e2)
    a.axhspan(1.0e2, 6.0e2, color="#fdece0", zorder=0)
    a.text(11.0, 2.3e2, rf"ours at $\mu=0$: all {n_infinite} rows are $\infty$"
           "\n(diagonal exactly zero — off the axis)",
           fontsize=8.3, color=C["ours"], va="center")
    a.set_xlabel("mode index  $n$  (Fourier index)")
    a.set_ylabel(r"Gershgorin dominance ratio  $r_n/|\lambda_n|$")
    a.set_title("A — the quantity Lemma 3.2 must control", fontsize=10.5)
    a.grid(alpha=0.25, which="both")
    a.legend(fontsize=7.6, loc="lower left", ncol=2, framealpha=0.95)
    exp_c = cp4["gershgorin_ratio_ladder_cadiot"][-1]["exponent"]
    exp_o = next(r["exponent"] for r in cp4["gershgorin_ratio_ladder_ours"]
                 if r["exponent"] is not None)
    a.text(0.97, 0.60,
           f"Cadiot: exponent {exp_c:+.3f}\n(drifting to the analytic $-1/2$)\n"
           f"ours: {exp_o:+.4f} at every $\\mu>0$ — FLAT",
           transform=a.transAxes, va="top", ha="right", fontsize=8.3,
           bbox=dict(fc="#fff6e8", ec=C["warn"], alpha=0.96, boxstyle="round,pad=0.4"))

    # ---------------- B: the shift Lemma 3.2 needs ----------------
    b = ax[1]
    lc = cp4["cadiot_whitham"]
    b.loglog(lc["sizes"], lc["s_required"], "o-", color=C["cadiot"], lw=2.6, ms=7,
             label=f"Cadiot §5.2 Whitham — {lc['s_required'][0]:.5f} at every $N$")
    zero_mus = []
    for key, lad in sorted(cp4["ours_by_mu"].items(), key=lambda kv: float(kv[0])):
        mu = float(key)
        if lad["exponent"] is None:
            zero_mus.append(mu)
            continue
        b.loglog(lad["sizes"], lad["s_required"], "s--", ms=5,
                 color=plt.cm.Oranges(0.42 + 0.53 * min(mu, 0.5) / 0.5),
                 label=rf"ours, $\mu={mu:g}$ — exponent {lad['exponent']:+.3f}")
    b.set_xticks([128, 256, 512, 1024, 2048])
    b.set_xticklabels(["128", "256", "512", "1024", "2048"])
    b.minorticks_off()
    b.set_ylim(1.0e-1, 4.0e3)
    b.set_xlabel("truncation  ($N$ for Cadiot, $M$ for ours)")
    b.set_ylabel(r"minimum shift  $|s|$  with  $|\lambda_n+s|>r_n/2$  for all $n$")
    b.set_title("B — one finite shift, or none at all", fontsize=10.5)
    b.grid(alpha=0.25, which="major")
    b.legend(fontsize=7.6, loc="upper left", framealpha=0.95)
    b.text(0.5, 0.035,
           r"ours at $\mu\in\{" + ", ".join(f"{m:g}" for m in zero_mus) + r"\}$: "
           "$|s|=0$ exactly\n(already dominant — not on a log axis)",
           transform=b.transAxes, ha="center", va="bottom", fontsize=8.3,
           bbox=dict(fc="#eef7ee", ec=C["good"], alpha=0.96, boxstyle="round,pad=0.4"))

    # ---------------- C: Assumption 1, as a number ----------------
    c = ax[2]
    names = list(cp2["examples"].keys())
    labels = [n.replace("_", " ") for n in names] + ["OURS\n$a=0$ CLM"]
    vals = [cp2["examples"][n]["l_min"] for n in names] + [0.0]
    cols = [C["cadiot"]] * len(names) + [C["ours"]]
    xs = np.arange(len(vals))
    floor = 1.2e-2
    c.bar(xs[:-1], vals[:-1], color=cols[:-1], width=0.62)
    c.bar(xs[-1:], [floor * 1.25], color=C["ours"], width=0.62, hatch="//",
          edgecolor="white")
    c.set_yscale("log")
    c.set_ylim(floor, 6.0)
    c.set_xticks(xs)
    c.set_xticklabels(labels, fontsize=8.4, rotation=16, ha="right")
    c.set_ylabel(r"Assumption 1's  $l_{\min}=\inf_\xi\,\sigma_{\min}(l(\xi))$")
    c.set_title("C — Assumption 1 on the paper's own examples", fontsize=10.5)
    c.grid(alpha=0.25, axis="y", which="major")
    for x, v, n in zip(xs, vals, names + [None]):
        if n is None:
            c.text(x, floor * 1.45, "EXACTLY 0", ha="center", va="bottom",
                   fontsize=8.6, color=C["ours"], weight="bold")
        else:
            st = cp2["examples"][n]["author_states"]["l_min"]
            tag = (f"{v:.3f}\n(author states {st:g})" if st is not None
                   else f"{v:.3f}\n(not stated; measured)")
            c.text(x, v * 1.15, tag, ha="center", va="bottom", fontsize=7.4)

    g = d["CP7_gate"]
    fig.suptitle("Route-CP v1 (leg 62) — Cadiot arXiv:2505.03091 does NOT cover the "
                 "off-diagonal / zero-diagonal case: the gate answers "
                 f"{g['answer'].upper()} on {g['n_clauses_failing']} of "
                 f"{len(g['clauses_examined']) if 'clauses_examined' in g else g['n_clauses_failing']}"
                 " located clauses",
                 fontsize=12.5, y=0.975)
    fig.tight_layout(rect=(0, 0.145, 1, 0.935))
    th = cp6["thresholds"]
    fig.text(0.5, 0.098,
             "Three numbers on one dial, kept apart:  Cadiot's Lemma 3.2 admits the "
             f"$\\Lambda^1$-dissipated family for $\\mu\\geq"
             f"{th['cadiot_lemma_3_2_mu_threshold']:g}$;  BDL's assumption (5) only for "
             f"$\\mu>{th['bdl_assumption_5_mu_threshold']:g}$ (factor "
             f"{th['factor_between_them']:g});  and the OPERATOR's own hinge (leg 57) is "
             f"$\\mu={th['leg_57_operator_hinge']:g}$ exactly.\n"
             "Two hypotheses of two constructions and one property of an operator — and "
             "both hypotheses are vacuous at the case of interest.",
             ha="center", va="top", fontsize=8.8, style="italic")
    fig.text(0.5, 0.018,
             "Scope: this leg settles somebody else's paper and claims NO mathematical "
             "novelty of its own (novelty pass verdict PROCEED_AS_BOOKKEEPING). "
             "A gap in one paper is not a theorem — it CAPS NG's claim, it does not "
             "support it.  No link of the L1→L4 chain moved.",
             ha="center", va="bottom", fontsize=8.4, color=C["grey"])
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig56_route_cp_v1_cadiot.png"
    fig.savefig(out, dpi=145)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
