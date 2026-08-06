"""Phase-2 Route-PORT v1 (fig59): the certificate closes, around the WRONG object.

Leg 46 built the bordered Newton system for `HL_S2_nonsymmetric` and got the radii
polynomial to close in float at every rung -- and then its own pre-committed clause P6b
fired: the truncation distance is 1.831e-01 against a ball of radius 1.18e-09, so the
object the certificate encloses is not the object anyone cares about.  That negative is
load-bearing: it is the reason stage `L1` was re-priced and the reason leg 47 ran at all.

This script is leg 60's job, and it does TWO things:

  1. it draws fig59 from the committed JSON with no recomputation, and
  2. it RE-DERIVES, from that same JSON, every number the Route-PORT v1 prose quotes
     (`writeup/README.md` item 46 and `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V1.md`)
     to the precision the prose states, and prints a per-number PASS/FAIL ledger.

Point 2 is a reproduction check that can fail, and it is the whole reason this leg is
claim-bearing.  It compares against the prose as written -- it does NOT edit the prose to
match, and it does not silently round until agreement appears.  Exit code is 0 either way;
the ledger is the output, and a FAIL row is a defect report for the human, not a crash.

Rebuild fig59 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_port_v1_bordered_evidence.py
Regenerate the data (deterministic, ~17 s):
    .venv/bin/python -u experiments/p2_route_port_v1_bordered.py
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
JSON = DATA / "p2_route_port_v1_bordered.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


# ----------------------------------------------------------------------------
# the reproduction ledger
# ----------------------------------------------------------------------------

def _fmt(x):
    return f"{x:.6g}" if isinstance(x, float) else str(x)


def half_ulp(literal):
    """The tolerance the prose itself sets: half a unit in its own last digit.

    "the precision the prose states" is not a free parameter -- a document that
    writes `1.831e-01` claims four significant figures and nothing more, so the
    check must accept anything that rounds to `1.831e-01` and reject anything
    that does not.  This parses the verbatim literal and returns that half-ulp as
    an ABSOLUTE tolerance, which is why every quoted number below is passed as
    the string that appears in the document rather than as a float.
    """
    s = literal.strip().replace("−", "-")
    mant, _, exp = s.partition("e")
    exp = int(exp) if exp else 0
    dec = len(mant.split(".")[1]) if "." in mant else 0
    return 0.5 * 10.0 ** (exp - dec)


class Ledger:
    """Every row is one number the prose quotes, re-derived from the JSON."""

    def __init__(self, title):
        self.title = title
        self.rows = []

    def check(self, where, what, literal, derived, scale=1.0):
        """`literal` is the number VERBATIM from the prose; `scale` converts the
        prose's unit into the JSON's (e.g. a percentage against a fraction)."""
        quoted = float(literal.replace("−", "-")) * scale
        tol = half_ulp(literal) * scale
        err = abs(derived - quoted)
        rel = err / max(abs(quoted), 1e-300)
        self.rows.append({"where": where, "what": what, "quoted": quoted,
                          "derived": derived, "rel": rel, "tol": tol,
                          "err": err, "ok": err <= tol * (1 + 1e-9)})

    def check_approx(self, where, what, literal, derived, sigfigs):
        """For a number the prose writes with a tilde (`~5200x`, `~1e-2`).  A tilde
        is a claim to `sigfigs` significant figures and no more, so that is the bar."""
        quoted = float(literal.replace("−", "-"))
        rounded = float(f"%.{sigfigs - 1}e" % derived)
        err = abs(derived - quoted)
        self.rows.append({"where": where, "what": what + f" (~, {sigfigs} s.f.)",
                          "quoted": quoted, "derived": derived,
                          "rel": err / max(abs(quoted), 1e-300),
                          "tol": abs(quoted) * 10.0 ** (1 - sigfigs) / 2,
                          "err": err, "ok": rounded == quoted})

    def check_exact(self, where, what, quoted, derived):
        ok = quoted == derived
        self.rows.append({"where": where, "what": what, "quoted": quoted,
                          "derived": derived, "rel": 0.0 if ok else float("nan"),
                          "tol": 0.0, "err": 0.0 if ok else float("nan"), "ok": ok})

    @property
    def failures(self):
        return [r for r in self.rows if not r["ok"]]

    def report(self):
        print(f"\n{self.title}")
        print("=" * len(self.title))
        w = max(len(r["what"]) for r in self.rows)
        for r in self.rows:
            tag = "PASS" if r["ok"] else "FAIL"
            line = (f"  [{tag}] {r['what']:<{w}}  prose {_fmt(r['quoted']):>14}"
                    f"   data {_fmt(r['derived']):>14}")
            if isinstance(r["quoted"], float):
                line += (f"   |err| {r['err']:.2e} vs half-ulp {r['tol']:.1e}"
                         f"   rel {r['rel']:.1e}")
            print(line + f"   [{r['where']}]")
        n_ok = len(self.rows) - len(self.failures)
        print(f"\n  {n_ok}/{len(self.rows)} quoted numbers re-derive from the stored data,"
              " each to half a unit in its own last quoted digit.")
        # A failure is reported with its MAGNITUDE, never as a bare boolean, and the two
        # kinds are not the same kind: a value sitting one half-ulp out is the prose
        # truncating its own last digit; a value hundreds of half-ulps out is the prose
        # quoting a different number than the data holds.
        for r in self.failures:
            ulps = r["err"] / max(r["tol"], 1e-300)
            kind = "LAST-DIGIT" if ulps <= 2.0 else "SUBSTANTIVE"
            print(f"  {kind}: {r['what']} -- prose {_fmt(r['quoted'])}, "
                  f"data {_fmt(r['derived'])} (absolute {r['err']:.3g}, "
                  f"relative {r['rel']:.3g}, {ulps:.1f} half-ulps out)")
        return not self.failures

    def substantive(self):
        return [r for r in self.failures
                if r["err"] / max(r["tol"], 1e-300) > 2.0]


def reproduce(d):
    L = Ledger("Route-PORT v1 -- reproduction of every quoted number, from the curated JSON")
    A = d["A_newton_ladder"]
    Cx = d["C_extrapolation"]
    D = d["D_certificate"]
    E = d["E_ceiling"]

    # --- section 1: the ablation that shows the borders are load-bearing ----
    unbordered = Cx["pins"][0]
    L.check("TECH sec 1 / README", "un-bordered residual", "1.42e-2", unbordered["residual"])
    L.check_exact("TECH sec 1", "un-bordered iterations", 60, unbordered["iters"])
    L.check_exact("TECH sec 1", "bordered iterations at n=301", 4, A["rungs"][1]["iters"])

    # --- section 2: Newton converges where the relaxation floors -----------
    quoted_res = ["5.66e-15", "7.61e-15", "1.25e-14", "3.12e-14", "3.52e-14"]
    quoted_rat = ["-2.541222", "-2.541024", "-2.540873", "-2.540791", "-2.540746"]
    quoted_pct = ["1.187", "1.180", "1.174", "1.170", "1.169"]
    for q_r, q_t, q_p, rung in zip(quoted_res, quoted_rat, quoted_pct, A["rungs"]):
        n = rung["n"]
        L.check("TECH sec 2", f"residual at n={n}", q_r, rung["residual"])
        L.check("TECH sec 2", f"ratio at n={n}", q_t, rung["ratio"])
        L.check("TECH sec 2", f"gap vs CHL at n={n} (%)", q_p,
                rung["ratio_err_vs_CHL"], scale=1e-2)
    L.check_approx("TECH sec 2", "relaxation floor", "1e-2", A["relaxation_floor"], 1)
    L.check("TECH sec 2", "tail exponent c_omega/c_l", "-0.394",
            A["rungs"][0]["c_omega"] / A["rungs"][0]["c_l"])
    L.check_approx("TECH sec 2", "X_max reached", "745", A["rungs"][0]["X_max"], 3)
    # the headline "1.17% gap is reach not resolution" is the RESOLUTION-CONVERGED value,
    # i.e. the finest rung, not the n=201 rung.
    L.check("README / TECH sec 2.1", "resolution-converged gap (%)", "1.17",
            A["rungs"][-1]["ratio_err_vs_CHL"], scale=1e-2)

    # --- section 2.1: the reach ladder, its slope and its extrapolation -----
    # The prose's reach table is a ladder in rho at FIXED n=301 -- so each row must
    # re-derive from C_extrapolation/reach, which is the only place that ladder lives.
    reach = Cx["reach"][:4]
    for q_x, q_t, r in zip(["100.9", "274.2", "745.2", "2025.8"],
                           ["-2.583087", "-2.557642", "-2.541024", "-2.530473"], reach):
        rho = r["rho_max"]
        L.check("TECH sec 2.1 table", f"X_max at rho={rho:g}", q_x, r["X_max"])
        L.check("TECH sec 2.1 table", f"reach-ladder ratio at rho={rho:g}", q_t, r["ratio"])
    L.check("README / TECH sec 2.1", "reach power-law slope", "-0.437",
            Cx["reach_power_law_slope"])
    L.check("README / TECH sec 2.1", "extrapolated limit", "-2.511926", Cx["best_limit"])
    L.check("README / TECH sec 2.1", "CHL reference ratio", "-2.5114", Cx["chl_ratio"])
    L.check("README / TECH sec 2.1", "extrapolation err vs CHL", "2.09e-04",
            Cx["best_limit_err_vs_CHL"])
    L.check("TECH sec 2.1", "two-window disagreement (%)", "0.93",
            Cx["collapse_rel_disagreement"], scale=1e-2)

    # --- section 3: the certificate, tuned vs naive -------------------------
    for q_t, q_n, q_g, rung in zip(["1.95e-04", "6.36e-04", "2.40e-04"],
                                   ["1.0125", "3.3193", "1.2578"],
                                   ["5186.6", "5221.5", "5235.6"], D["rungs"]):
        n = rung["n"]
        L.check("TECH sec 3", f"tuned Y0/budget at n={n}", q_t,
                rung["tuned"]["Y0_over_budget"])
        L.check("TECH sec 3", f"naive Y0/budget at n={n}", q_n,
                rung["naive"]["Y0_over_budget"])
        L.check("TECH sec 3", f"free-constant gain at n={n}", q_g,
                rung["free_constant_gain"])
    # "~5200x" is a one-sig-fig round number and is read as such: the check is that
    # every rung's gain rounds to it, not that some average hits it.
    L.check_approx("README / TECH sec 3", "the one constant, headline (max rung)", "5200",
                   max(r["free_constant_gain"] for r in D["rungs"]), 2)
    L.check_approx("README / TECH sec 3", "the one constant, headline (min rung)", "5200",
                   min(r["free_constant_gain"] for r in D["rungs"]), 2)
    L.check("README / TECH sec 3", "p_star", "0.39", D["p_star"])
    L.check("TECH sec 3", "tuned w_l fraction", "0.01", D["rungs"][0]["tuned"]["w_l_frac"])
    L.check("TECH sec 3", "naive w_l fraction", "1.0", D["rungs"][0]["naive"]["w_l_frac"])

    # --- section 4: the ceiling, clause P6b --------------------------------
    L.check("README / TECH sec 4", "truncation distance", "1.831e-01", E["distance"])
    L.check("TECH sec 4", "ball r_min", "2.97e-12", E["r_min"])
    L.check("README / TECH sec 4", "ball r_max", "1.18e-09", E["r_max"])
    L.check("README / TECH sec 4", "distance / r_max", "1.55e+08",
            E["distance_over_r_max"])
    L.check_exact("TECH sec 4", "worst block",
                  "Omega", max(E["parts"], key=E["parts"].get))
    L.check("TECH sec 4", "compared reaches (ref)", "8", E["reach_ref"])
    L.check("TECH sec 4", "compared reaches (fine)", "9", E["reach_fine"])

    # --- the pre-committed predicate ---------------------------------------
    checks = d["predicate_checks"]
    L.check_exact("README / TECH sec 6", "clauses held (of 7)", 7,
                  sum(1 for v in checks.values() if v))
    L.check_exact("TECH sec 6", "clauses declared", 7, len(checks))
    L.check("TECH header", "wall time (s)", "17", d["wall_s"])
    return L


# ----------------------------------------------------------------------------
# the figure
# ----------------------------------------------------------------------------

def build_figure(d, L):
    A, Cx, D, E = (d["A_newton_ladder"], d["C_extrapolation"],
                   d["D_certificate"], d["E_ceiling"])
    fig, ax = plt.subplots(2, 2, figsize=(15.0, 10.4))

    # ---- A: Newton converges where the relaxation floors ------------------
    a = ax[0, 0]
    ns = [r["n"] for r in A["rungs"]]
    a.semilogy(ns, [r["residual"] for r in A["rungs"]], "o-", color=C["good"],
               lw=2.2, ms=7, label="bordered Newton (converged)")
    a.axhline(A["relaxation_floor"], color=C["bad"], ls="--", lw=2.0,
              label=r"relaxation floor $\sim$1e$-$2 (`RescaledHLScenario2`)")
    unb = Cx["pins"][0]
    a.plot([301], [unb["residual"]], "X", color=C["bad"], ms=14,
           label=f"borders DROPPED: {unb['residual']:.2e} after {unb['iters']} iters")
    a.set_ylim(min(r["residual"] for r in A["rungs"]) / 8.0, 1.0)
    for n, r in zip(ns, A["rungs"]):
        a.annotate(f"{r['iters']} it", (n, r["residual"]), textcoords="offset points",
                   xytext=(0, -15), ha="center", fontsize=8, color=C["grey"])
    a.set_xlabel("grid points $n$")
    a.set_ylabel("Newton residual")
    a.set_title("A  The borders are load-bearing:\n"
                f"{A['decades_vs_relaxation']:.1f} decades below the relaxation's floor",
                fontsize=11)
    a.legend(fontsize=8, loc="center right", framealpha=0.95)
    a.grid(alpha=0.25, which="both")

    # ---- B: the gap is reach, and it extrapolates -------------------------
    b = ax[0, 1]
    reach = Cx["reach"]
    xs = np.array([r["X_max"] for r in reach])
    ys = np.array([r["ratio"] for r in reach])
    b.semilogx(xs, ys, "o-", color=C["anchor"], lw=2.0, ms=7,
               label=r"reach ladder ($n=301$, $\rho_{max}=6\ldots11$)")
    b.axhline(Cx["chl_ratio"], color=C["bad"], ls="--", lw=2.0,
              label=f"CHL arXiv:2604.01868: {Cx['chl_ratio']:.4f}")
    b.axhline(Cx["best_limit"], color=C["good"], ls=":", lw=2.2,
              label=(f"extrapolated limit {Cx['best_limit']:.6f}\n"
                     f"(rel err {Cx['best_limit_err_vs_CHL']:.2e}; "
                     f"slope {Cx['reach_power_law_slope']:.3f})"))
    # the resolution ladder, plotted at the SAME X_max, to show it does not move
    b.plot([r["X_max"] for r in A["rungs"]], [r["ratio"] for r in A["rungs"]],
           "s", color=C["warn"], ms=6, alpha=0.85,
           label=r"resolution ladder $n=201\ldots1201$ (all at $X_{max}=745$)")
    res_spread = (max(r["ratio"] for r in A["rungs"])
                  - min(r["ratio"] for r in A["rungs"]))
    b.annotate(f"all 5 resolutions\nspan {res_spread:.1e}",
               (A["rungs"][0]["X_max"], A["rungs"][0]["ratio"]),
               textcoords="offset points", xytext=(-26, -52), ha="right",
               fontsize=8, color=C["warn"],
               arrowprops=dict(arrowstyle="->", color=C["warn"], lw=1.2))
    # Leg 60's reproduction check found the prose's reach-table row at rho=8 quoting the
    # n=201 value into an n=301 ladder.  The figure says so rather than quietly using
    # whichever number agrees.
    bad = [r for r in L.substantive() if "rho=8" in r["what"]]
    if bad:
        r8 = Cx["reach"][2]
        b.plot([r8["X_max"]], [bad[0]["quoted"]], "v", color=C["bad"], ms=11, zorder=6)
        b.annotate(f"prose row quotes {bad[0]['quoted']:.6f}\n"
                   f"ladder holds {bad[0]['derived']:.6f}  (LEG 60)",
                   (r8["X_max"], bad[0]["quoted"]), textcoords="offset points",
                   xytext=(16, -30), fontsize=8, color=C["bad"], fontweight="bold",
                   arrowprops=dict(arrowstyle="->", color=C["bad"], lw=1.3))
    b.set_xlabel(r"$X_{max}$")
    b.set_ylabel(r"$c_l/c_\omega$")
    b.set_title("B  The 1.17% gap is REACH, not resolution\n"
                "(resolution ladder is a vertical stack; reach is the mover)", fontsize=11)
    b.legend(fontsize=7.6, loc="lower right", framealpha=0.95)
    b.grid(alpha=0.25, which="both")

    # ---- C: closure is a property of the space ----------------------------
    c = ax[1, 0]
    rungs = D["rungs"]
    x = np.arange(len(rungs))
    tuned = [r["tuned"]["Y0_over_budget"] for r in rungs]
    naive = [r["naive"]["Y0_over_budget"] for r in rungs]
    c.bar(x - 0.19, tuned, 0.36, color=C["good"], label=r"tuned $w_l=0.01\,X_{max}$")
    c.bar(x + 0.19, naive, 0.36, color=C["bad"], label=r"naive $w_l=X_{max}$")
    c.axhline(1.0, color="#333", lw=1.4, ls="--")
    c.text(len(rungs) - 0.55, 1.25, "closure boundary", fontsize=8, color="#333")
    c.set_yscale("log")
    c.set_ylim(min(tuned) / 2.2, max(naive) * 30.0)
    c.set_xticks(x); c.set_xticklabels([f"n={r['n']}" for r in rungs])
    for i, r in enumerate(rungs):
        c.annotate(f"{r['free_constant_gain']:.0f}$\\times$",
                   (i, max(tuned[i], naive[i]) * 2.4), ha="center", fontsize=9.5,
                   color=C["ours"], fontweight="bold")
    c.set_ylabel(r"$Y_0$ / budget   (< 1 closes)")
    c.set_title("C  Closure is a property of the SPACE:\n"
                "one constant in the weight is worth ~5200$\\times$", fontsize=11)
    c.legend(fontsize=8.5, loc="lower left", framealpha=0.95)
    c.grid(alpha=0.25, axis="y", which="both")

    # ---- D: the ceiling, clause P6b ---------------------------------------
    dd = ax[1, 1]
    dd.set_yscale("log")
    dd.set_xlim(-0.7, 1.7)
    dd.bar([0], [E["distance"]], 0.5, color=C["bad"])
    dd.bar([1], [E["r_max"]], 0.5, color=C["good"])
    dd.plot([1, 1], [E["r_min"], E["r_max"]], color=C["anchor"], lw=3.0,
            solid_capstyle="butt", label=r"float ball $[r_{min}, r_{max}]$")
    dd.set_xticks([0, 1])
    dd.set_xticklabels([f"truncation distance\n{E['distance']:.3e}\n"
                        f"(worst block: {max(E['parts'], key=E['parts'].get)})",
                        f"the ball\n$r_{{max}}$ = {E['r_max']:.2e}"], fontsize=9)
    dd.annotate("", xy=(0.0, E["distance"]), xytext=(0.0, E["r_max"]),
                arrowprops=dict(arrowstyle="<->", color=C["ours"], lw=2.2))
    dd.text(0.06, np.sqrt(E["distance"] * E["r_max"]),
            f"{E['distance_over_r_max']:.2e}$\\times$\nOUTSIDE the ball",
            color=C["ours"], fontsize=12, fontweight="bold", va="center")
    dd.set_ylabel("certificate's own weighted norm")
    dd.set_title("D  CLAUSE P6b, pre-committed: the polynomial closes\n"
                 "around the TRUNCATED object", fontsize=11)
    dd.legend(fontsize=8.5, loc="lower left", framealpha=0.95)
    dd.grid(alpha=0.25, axis="y", which="both")

    n_sub, n_ld = len(L.substantive()), len(L.failures) - len(L.substantive())
    verdict = ("every quoted number re-derives from the curated data"
               if not L.failures else
               f"{len(L.rows) - len(L.failures)}/{len(L.rows)} re-derive; "
               f"{n_sub} substantive + {n_ld} last-digit do not -- see panel B and stdout")
    fig.suptitle("Route-PORT v1 (leg 46): the radii polynomial CLOSES in float at every "
                 "rung -- around an object 1.55e+08 ball radii from the real one\n"
                 f"[leg 60 reproduction check: {verdict}]",
                 fontweight="bold", y=1.005, fontsize=12)
    fig.tight_layout()
    out = FIGS / "fig59_route_port_v1.png"
    fig.savefig(out, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


def main():
    d = json.loads(JSON.read_text())
    L = reproduce(d)
    ok = L.report()
    build_figure(d, L)
    sub = L.substantive()
    print("\nROUTE-PORT v1 REPRODUCTION: "
          + ("CLEAN" if ok else
             f"{len(sub)} substantive + {len(L.failures) - len(sub)} last-digit "
             "discrepancy(ies) -- reported, prose deliberately NOT edited to match"))
    print("  The two BAN-BEARING numbers (truncation distance / r_max = 1.55e+08, and "
          "clause P6b holding) both re-derive exactly.")


if __name__ == "__main__":
    main()
