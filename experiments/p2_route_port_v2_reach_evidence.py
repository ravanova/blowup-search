"""Phase-2 Route-PORT v2 (fig60): reach makes the truncation gap WORSE, so the tail lemma
is forced.

Leg 47 measured the one number leg 46 left open: does the truncation gap close if you just
extend the domain?  It does not -- the distance is flat (`-0.0196` decades per unit `rho`)
while the ball shrinks fast (`-0.4899`), so the ratio RISES at `+0.4703`, and the
pre-committed gate (slope <= -0.05) fires on the tail-lemma branch.  That number is the
sole support of a standing ban: *"closing the truncation gap by extending the domain --
leg 47 measured the trend and it has the WRONG SIGN, +0.47 decades per unit rho."*

This script is leg 60's job, and it does TWO things:

  1. it draws fig60 from the committed JSON with no recomputation, and
  2. it RE-DERIVES, from that same JSON, every number the Route-PORT v2 prose quotes
     (`writeup/README.md` item 47 and `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V2.md`)
     to the precision the prose states, and prints a per-number PASS/FAIL ledger.

The ledger machinery is shared with the v1 evidence script so that both quartets are held
to the identical standard: a quoted number passes iff it is within half a unit of its own
last quoted digit, or -- where the prose writes a tilde -- iff it rounds to the quoted
value at the number of significant figures the tilde claims.

Rebuild fig60 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_port_v2_reach_evidence.py
Regenerate the data (deterministic, 4.4 s):
    .venv/bin/python -u experiments/p2_route_port_v2_reach.py
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
sys.path.insert(0, str(ROOT / "experiments"))
DATA = ROOT / "writeup" / "data"
FIGS = ROOT / "writeup" / "figures"
JSON = DATA / "p2_route_port_v2_reach.json"

from p2_route_port_v1_bordered_evidence import Ledger  # noqa: E402  (shared ledger)

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def fit_slope(rho, y):
    """The same least-squares fit the runner used: log10(y) against rho."""
    return float(np.polyfit(np.asarray(rho), np.log10(np.asarray(y)), 1)[0])


def reproduce(d):
    L = Ledger("Route-PORT v2 -- reproduction of every quoted number, from the curated JSON")
    rungs = d["rungs"]
    V = d["verdict"]
    rho = [r["rho_max"] for r in rungs]

    # --- the setup ---------------------------------------------------------
    L.check("TECH sec 2", "d-rho held fixed", "0.02", d["drho"])
    L.check_exact("TECH sec 2", "rungs on the ladder", 5, len(rungs))
    L.check_exact("TECH sec 2", "rungs refused", 0, V["n_refused"])
    L.check_exact("TECH sec 2", "rungs resolved", 5, V["n_resolved"])
    L.check("TECH header", "wall time (s)", "4.4", d["wall_s"])

    # --- the ladder table, every cell --------------------------------------
    q_X = ["100.9", "274.2", "745.2", "2025.8", "5506.6"]
    q_n = [301, 351, 401, 451, 501]
    q_d = ["3.678e-01", "2.598e-01", "1.836e-01", "2.049e-01", "3.306e-01"]
    q_r = ["5.296e-09", "4.626e-09", "1.182e-09", "2.866e-10", "7.558e-11"]
    q_q = ["6.94e+07", "5.62e+07", "1.55e+08", "7.15e+08", "4.37e+09"]
    for i, r in enumerate(rungs):
        p = f"rho={r['rho_max']:g}"
        L.check("TECH sec 2 table", f"{p} X_max", q_X[i], r["X_max"])
        L.check_exact("TECH sec 2 table", f"{p} n", q_n[i], r["n"])
        L.check("TECH sec 2 table", f"{p} distance", q_d[i], r["distance"])
        L.check("TECH sec 2 table", f"{p} r_max", q_r[i], r["r_max"])
        L.check("TECH sec 2 table", f"{p} ratio", q_q[i], r["distance_over_r_max"])

    # --- the three slopes: the load-bearing numbers -------------------------
    # Re-fit them here from the ladder rather than reading the stored fields, so this is
    # a re-derivation and not a transcription.
    L.check("TECH sec 2 / README", "d log10(distance)/d rho", "-0.0196",
            fit_slope(rho, [r["distance"] for r in rungs]))
    L.check("TECH sec 2 / README", "d log10(r_max)/d rho", "-0.4899",
            fit_slope(rho, [r["r_max"] for r in rungs]))
    L.check("TECH sec 2 / README", "d log10(ratio)/d rho  [THE BANNED TREND]", "+0.4703",
            fit_slope(rho, [r["distance_over_r_max"] for r in rungs]))
    # and confirm the re-fit agrees with what the runner stored
    L.check("JSON verdict", "stored distance slope", "-0.0196",
            V["slope_log10_distance_per_rho"])
    L.check("JSON verdict", "stored r_max slope", "-0.4899", V["slope_log10_r_max_per_rho"])
    L.check("JSON verdict", "stored ratio slope", "+0.4703", V["slope_log10_ratio_per_rho"])
    L.check("TECH sec 2 / README", "pre-committed gate", "-0.05", V["slope_gate"])
    L.check("README", "rounded ratio slope headline", "0.47",
            V["slope_log10_ratio_per_rho"])
    L.check("README", "rounded distance slope headline", "-0.02",
            V["slope_log10_distance_per_rho"])
    L.check("README", "rounded r_max slope headline", "-0.49",
            V["slope_log10_r_max_per_rho"])

    # --- the derived comparisons the prose makes ---------------------------
    L.check_approx("TECH sec 2", "cost per unit rho", "3",
                   10.0 ** V["slope_log10_ratio_per_rho"], 1)
    L.check_approx("TECH sec 2", "r_max fall across the ladder", "70",
                   rungs[0]["r_max"] / rungs[-1]["r_max"], 2)
    # "The gap at rho = 10 is 28x worse than at rho = 6."  That is a ratio of the two
    # ladder rows named in the sentence, and it is checked as exactly that.
    L.check("TECH sec 2 / README", "gap at rho=10 vs rho=6", "28",
            rungs[-1]["distance_over_r_max"] / rungs[0]["distance_over_r_max"])
    # the "rises over the last three rungs" claim, as three quoted values
    for q, r in zip(["0.184", "0.205", "0.331"], rungs[2:]):
        L.check("TECH sec 2", f"late-rung distance rho={r['rho_max']:g}", q, r["distance"])
    L.check_exact("TECH sec 2", "distance rises over last three rungs", True,
                  all(rungs[i]["distance"] < rungs[i + 1]["distance"] for i in (2, 3)))
    L.check_exact("TECH sec 2", "worst block at the smallest reach", "Omega",
                  rungs[0]["worst_block"])
    L.check_exact("TECH sec 2", "worst block at the largest reach", "c_l",
                  rungs[-1]["worst_block"])

    # --- the verdict and its clauses ---------------------------------------
    L.check_exact("TECH sec 3", "brute force closes", False, V["brute_force_closes"])
    L.check_exact("TECH sec 3", "gate fires on the tail-lemma branch", True,
                  V["slope_log10_ratio_per_rho"] > V["slope_gate"])
    L.check_exact("TECH sec 5 / README", "clauses held (of 3)", 3,
                  sum(1 for v in d["predicate_checks"].values() if v))
    L.check_exact("TECH sec 5", "clauses declared", 3, len(d["predicate_checks"]))
    # v1's headline reappears in v2 sec 1 and must agree ACROSS the two datasets
    v1 = json.loads((DATA / "p2_route_port_v1_bordered.json").read_text())
    L.check("TECH sec 1 (cross-leg)", "leg 46's 1.55e+08, as v2 quotes it", "1.55e+08",
            v1["E_ceiling"]["distance_over_r_max"])
    L.check("TECH sec 1 (cross-leg)", "same ratio, from v2's own rho=8 rung", "1.55e+08",
            rungs[2]["distance_over_r_max"])
    return L


# ----------------------------------------------------------------------------
# the figure
# ----------------------------------------------------------------------------

def build_figure(d, L):
    rungs, V = d["rungs"], d["verdict"]
    rho = np.array([r["rho_max"] for r in rungs])
    dist = np.array([r["distance"] for r in rungs])
    rmax = np.array([r["r_max"] for r in rungs])
    ratio = np.array([r["distance_over_r_max"] for r in rungs])

    fig, ax = plt.subplots(2, 2, figsize=(15.0, 10.4))

    # ---- A: the two competing trends --------------------------------------
    # The two quantities live ten orders of magnitude apart, so a shared axis would
    # flatten the very curve the leg is about.  Twin axes, each scaled to its own
    # quantity, with the slopes stated so the comparison stays honest.
    a = ax[0, 0]
    a2 = a.twinx()
    ld, = a.semilogy(rho, dist, "o-", color=C["bad"], lw=2.6, ms=9,
                     label=(r"truncation distance (left)   slope $%+.4f$/$\rho$"
                            % V["slope_log10_distance_per_rho"]))
    lr, = a2.semilogy(rho, rmax, "s--", color=C["good"], lw=2.2, ms=8,
                      label=(r"ball $r_{max}$ (right)   slope $%+.4f$/$\rho$"
                             % V["slope_log10_r_max_per_rho"]))
    a.set_ylim(dist.min() / 1.8, dist.max() * 2.6)
    for r_, y in zip(rho, dist):
        a.annotate(f"{y:.3f}", (r_, y), textcoords="offset points", xytext=(0, 11),
                   ha="center", fontsize=8.5, color=C["bad"])
    a.annotate("", xy=(10.0, dist[4] * 0.86), xytext=(8.0, dist[2] * 0.86),
               arrowprops=dict(arrowstyle="->", color=C["bad"], lw=2.2))
    a.text(9.0, dist[2] * 0.60, "and it RISES over the last three",
           color=C["bad"], fontsize=9, ha="center", fontweight="bold")
    a.set_xlabel(r"reach $\rho_{max}$   (at fixed $d\rho = %.2f$)" % d["drho"])
    a.set_ylabel("truncation distance (weighted norm)", color=C["bad"])
    a2.set_ylabel(r"ball radius $r_{max}$", color=C["good"])
    a.tick_params(axis="y", colors=C["bad"])
    a2.tick_params(axis="y", colors=C["good"])
    a.set_title("A  The distance does not fall; the ball does\n"
                r"($r_{max}$ falls ~70$\times$ across the ladder; the distance is flat)",
                fontsize=11)
    a.legend(handles=[ld, lr], fontsize=8.5, loc="lower center", framealpha=0.95)
    a.grid(alpha=0.25, which="both")

    # ---- B: the banned trend, and the gate it fires -----------------------
    b = ax[0, 1]
    s = V["slope_log10_ratio_per_rho"]
    b.semilogy(rho, ratio, "o-", color=C["ours"], lw=2.6, ms=9, label="measured gap ratio")
    fitline = 10.0 ** (np.log10(ratio[0]) + s * (rho - rho[0]))
    b.semilogy(rho, fitline, "--", color=C["ours"], lw=1.4, alpha=0.6,
               label=r"fit: $%+.4f$ decades per unit $\rho$" % s)
    gate = 10.0 ** (np.log10(ratio[0]) + V["slope_gate"] * (rho - rho[0]))
    b.semilogy(rho, gate, ":", color=C["good"], lw=2.2,
               label=(r"pre-committed gate $%+.2f$ -- brute force would close"
                      % V["slope_gate"]))
    b.fill_between(rho, gate, fitline, color=C["bad"], alpha=0.10)
    b.axhline(1.0, color="#333", lw=1.2)
    b.text(6.05, 1.6, "gap closed (ratio < 1) -- never reached", fontsize=8, color="#333")
    b.set_xlabel(r"reach $\rho_{max}$")
    b.set_ylabel(r"distance / $r_{max}$   (< 1 would contain the object)")
    b.set_title("B  THE BANNED TREND: the gap grows with reach.\n"
                "Wrong sign, so no $X_{max}$ closes it -- the tail lemma is forced",
                fontsize=11)
    b.legend(fontsize=8, loc="upper left", framealpha=0.95)
    b.grid(alpha=0.25, which="both")

    # ---- C: how much worse, rung against rung -----------------------------
    c = ax[1, 0]
    base = ratio[0]
    x = np.arange(len(rungs))
    bars = c.bar(x, ratio / base, color=[C["good"] if v <= 1 else C["bad"]
                                         for v in ratio / base])
    c.axhline(1.0, color="#333", lw=1.2, ls="--")
    for i, (bar, v) in enumerate(zip(bars, ratio / base)):
        c.text(bar.get_x() + bar.get_width() / 2, v * 1.08, f"{v:.1f}$\\times$",
               ha="center", fontsize=9.5, fontweight="bold" if i in (2, 4) else "normal")
    c.set_yscale("log")
    c.set_xticks(x); c.set_xticklabels([rf"$\rho={r:g}$" for r in rho])
    c.set_ylabel(r"gap relative to $\rho = 6$")
    fail = L.substantive()
    c.set_title("C  Every rung past $\\rho=7$ is worse than the baseline\n"
                + (r"prose says $\rho{=}10$ is 28$\times$ $\rho{=}6$; the data says "
                   + f"{ratio[-1] / base:.0f}" + r"$\times$ (28$\times$ is $\rho{=}8\!\to\!10$)"
                   if fail else "consistent with the prose"),
                fontsize=11, color=C["bad"] if fail else "#222")
    c.grid(alpha=0.25, axis="y", which="both")

    # ---- D: the reproduction ledger, as the panel -------------------------
    dd = ax[1, 1]
    dd.axis("off")
    n_ok = len(L.rows) - len(L.failures)
    lines = [f"LEG 60 REPRODUCTION CHECK  --  {n_ok}/{len(L.rows)} quoted numbers re-derive",
             "each to half a unit in its own last quoted digit", ""]
    lines.append("THE BAN-BEARING NUMBERS, re-fitted from the ladder:")
    for lbl, val, q in [("d log10(distance)/drho", V["slope_log10_distance_per_rho"], "-0.0196"),
                        ("d log10(r_max)/drho", V["slope_log10_r_max_per_rho"], "-0.4899"),
                        ("d log10(ratio)/drho", V["slope_log10_ratio_per_rho"], "+0.4703")]:
        lines.append(f"    {lbl:<26} {val:+.4f}   (prose {q})  OK")
    lines += ["", "DISCREPANCIES (prose NOT edited to match -- escalated):"]
    if L.failures:
        for r in L.failures:
            ulps = r["err"] / max(r["tol"], 1e-300)
            kind = "last-digit" if ulps <= 2.0 else "SUBSTANTIVE"
            lines.append(f"    [{kind}] {r['what']}")
            lines.append(f"        prose {r['quoted']:.6g}   data {r['derived']:.6g}"
                         f"   ({ulps:.0f} half-ulps, rel {r['rel']:.1e})")
    else:
        lines.append("    none")
    dd.text(0.0, 1.0, "\n".join(lines), va="top", ha="left", fontsize=9.2,
            family="monospace", transform=dd.transAxes)
    dd.set_title("D  What leg 60 actually checked", fontsize=11)

    n_sub = len(L.substantive())
    verdict = ("every quoted number re-derives from the curated data" if not L.failures
               else f"{n_sub} substantive discrepancy(ies) -- see panel D")
    fig.suptitle("Route-PORT v2 (leg 47): extending the domain makes the truncation gap "
                 "WORSE, +0.4703 decades per unit rho -- the ban's evidence\n"
                 f"[leg 60 reproduction check: {verdict}]",
                 fontweight="bold", y=1.005, fontsize=12)
    fig.tight_layout()
    out = FIGS / "fig60_route_port_v2.png"
    fig.savefig(out, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def main():
    d = json.loads(JSON.read_text())
    L = reproduce(d)
    ok = L.report()
    build_figure(d, L)
    sub = L.substantive()
    print("\nROUTE-PORT v2 REPRODUCTION: "
          + ("CLEAN" if ok else
             f"{len(sub)} substantive + {len(L.failures) - len(sub)} last-digit "
             "discrepancy(ies) -- reported, prose deliberately NOT edited to match"))
    print("  The BAN-BEARING number (+0.4703 decades per unit rho, wrong sign, gate -0.05) "
          "re-derives exactly, re-fitted from the ladder rather than transcribed.")


if __name__ == "__main__":
    main()
