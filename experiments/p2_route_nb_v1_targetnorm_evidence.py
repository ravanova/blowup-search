"""Phase-2 Route-NB v1 (fig50): does the REAL target have finite norm at all?

Legs 51-53 all measured on the `a = 0` CLM anchor, which is exactly one basis mode.  A
live ban asserts of the REAL target that it "does not have finite norm in the class where
the operator is least bad" -- a clause that had never been measured.  This leg projects
`HL_S2_nonsymmetric` into the compactified basis `X = tan(theta/2)` and measures the decay
exponent of its coefficients on two ladders.

The answer: `|h_k| ~ C k^{-p}` with **p = 1.396**, so the norm is FINITE for every
`s < 0.396` -- including `s = 0` and `s = 0.3`, the two admissible classes legs 52-53
actually used.  It is DIVERGENT at `s = 1`, which is where leg 51 measured the operator to
be least bad.  Both halves matter, and they are the two sides of an empty window.

Rebuild fig50 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_nb_v1_targetnorm_evidence.py
Regenerate the data (deterministic, ~9 min):
    .venv/bin/python -u experiments/p2_route_nb_v1_targetnorm.py

Six panels: A the measured spectra against the controls; B the DOMAIN ladder, which is the
one that moves, with the physical-space tail exponent beside it; C the resolution ladder,
which is flat; D the calibration curve -- the instrument recovers exponents nobody gave it;
E the norm margin against s, with the admissible window and the operator's class; F the
gate answer and its scope.
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
JSON = DATA / "p2_route_nb_v1_targetnorm.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def load():
    with open(JSON) as fh:
        return json.load(fh)


def build_figure():
    d = load()
    cur = d["NB7_curves"]
    ctl = d["NB1_controls"]
    ev = d["evaluation"]
    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.2))
    (a, b, c), (e, f, g) = ax

    # -- A: the spectra ----------------------------------------------------
    t = cur["target_Omega"]
    a.loglog(t["k"], t["hk"], color=C["ours"], lw=1.6,
             label=r"target $\Omega$  ($p$ = %.3f)" % t["p"])
    kk = np.array(t["k"])
    a.loglog(kk, t["C"] * kk ** (-t["p"]), "--", color="k", lw=1.0,
             label=r"fit  $C k^{-p}$")
    v = cur["target_V"]
    a.loglog(v["k"], v["hk"], color=C["anchor"], lw=1.2, alpha=0.85,
             label=r"target $V$  ($p$ = %.3f)" % v["p"])
    s = cur["negative_control_sawtooth"]
    a.loglog(s["k"], s["hk"], color=C["bad"], lw=1.2, ls=":",
             label=r"neg. control sawtooth ($p$ = 1, divergent)")
    pc = cur["positive_control_clm"]
    a.loglog(pc["k"], np.maximum(pc["hk"], 1e-17), color=C["good"], lw=1.0, alpha=0.8,
             label=r"pos. control CLM anchor (one mode)")
    a.set_xlabel("mode $k$")
    a.set_ylabel(r"$|\hat h_k| = 2|c_k|$")
    a.set_ylim(1e-17, 5)
    a.legend(fontsize=7.4, loc="lower left")
    a.set_title("A. the spectra — the target is a clean power law,\nthe anchor is one mode",
                fontsize=10)
    a.grid(alpha=0.25, which="both")

    # -- B: the DOMAIN ladder ----------------------------------------------
    rows = d["NB3_domain_ladder"]["rows"]
    Xm = [r["X_max"] for r in rows]
    b.semilogx(Xm, [r["p_minus_1"] for r in rows], "o-", color=C["ours"], lw=1.8,
               label=r"$p - 1$ (coefficient space)")
    b.semilogx(Xm, [-r["tail_exponent_physical_space_outer"] for r in rows], "s--",
               color=C["anchor"], lw=1.4, label=r"$-$tail exponent (physical space)")
    b.semilogx(Xm, [r["alpha_from_constants"] for r in rows], "^:", color=C["good"],
               lw=1.4, label=r"$\alpha = -c_\omega/c_l$ (from the solve)")
    b.set_xlabel(r"$X_{\max}$")
    b.set_ylabel("exponent")
    b.legend(fontsize=7.6, loc="lower right")
    b.set_title("B. the DOMAIN ladder — the one that moves.\n"
                "two independent measurements converge on $\\alpha$", fontsize=10)
    b.grid(alpha=0.25)

    # -- C: the resolution ladder ------------------------------------------
    r2 = d["NB2_resolution_ladder"]["rows"]
    c.plot([r["n"] for r in r2], [r["p"] for r in r2], "o-", color=C["ours"], lw=1.8)
    span = d["NB2_resolution_ladder"]["p_drift_over_ladder"]
    mid = np.mean([r["p"] for r in r2])
    c.set_ylim(mid - 0.02, mid + 0.02)
    c.set_xlabel("$n$ (Newton grid)")
    c.set_ylabel("$p$")
    c.set_title("C. the resolution ladder — FLAT.\n"
                "drift %.1e over n = 201…801" % span, fontsize=10)
    c.grid(alpha=0.25)
    c.annotate("the exponent is not resolution-limited;\nit is DOMAIN-limited (panel B)",
               xy=(0.5, 0.18), xycoords="axes fraction", ha="center", fontsize=8,
               color=C["grey"])

    # -- D: the calibration curve ------------------------------------------
    cal = ctl["calibration_family"]["rows"]
    al = [r["alpha"] for r in cal]
    e.plot(al, [r["err"] for r in cal], "o-", color=C["anchor"], lw=1.6,
           label="calibration family")
    e.axhline(0.0, color="k", lw=0.8)
    e.axvline(d["NB5_norms"]["alpha"], color=C["ours"], ls="--", lw=1.2,
              label=r"target $\alpha$ = %.4f" % d["NB5_norms"]["alpha"])
    n1 = ctl["negative_control_1_inverse_X"]
    n2 = ctl["negative_control_2_sawtooth"]
    e.plot([1.0], [n1["p_measured"] - 2.0], "D", color=C["bad"], ms=7,
           label=r"neg. ctrl $1/(1+|X|)$: $p$ = %.3f" % n1["p_measured"])
    e.plot([0.0], [n2["p_measured"] - 1.0], "s", color=C["bad"], ms=7,
           label=r"neg. ctrl sawtooth: $p$ = %.3f" % n2["p_measured"])
    e.set_xlabel(r"$\alpha$")
    e.set_ylabel(r"$p_{\rm measured} - (1+\alpha)$")
    e.legend(fontsize=7.2, loc="upper left")
    e.set_title("D. the instrument recovers an exponent nobody\n"
                "supplied — systematic $\\leq$ %.3f" % ctl["calibration_family"]["max_abs_err"],
                fontsize=10)
    e.grid(alpha=0.25)

    # -- E: the norm margin ------------------------------------------------
    # NB5's own p, so the curve and the class markers cannot disagree.  It is the
    # headline-domain value (X_max = 4.1e+04); the largest-domain value ev["p_best"]
    # is slightly larger and is quoted in panel F.
    p = d["NB5_norms"]["p"]
    ss = np.linspace(0.0, 1.2, 300)
    marg = p - 1.0 - ss
    f.plot(ss, marg, color=C["ours"], lw=2.0)
    f.axhline(0.0, color="k", lw=1.0)
    f.fill_between(ss, 0, marg, where=marg > 0, color=C["good"], alpha=0.18)
    f.fill_between(ss, marg, 0, where=marg < 0, color=C["bad"], alpha=0.18)
    unresolved = set(ev.get("admissible_classes_not_resolved", []))
    sysm = ev["systematic"]
    f.fill_between(ss, -sysm, sysm, color=C["warn"], alpha=0.30, zorder=1,
                   label="within the instrument's systematic")
    f.legend(fontsize=7.0, loc="lower left")
    for cl in d["NB5_norms"]["classes"]:
        sv = cl["s"]
        col = (C["warn"] if sv in unresolved
               else (C["good"] if cl["verdict"]["finite"] else C["bad"]))
        f.plot([sv], [p - 1.0 - sv], "o", color=col, ms=8, zorder=5)
        f.annotate("s=%.2f\n%+.3f" % (sv, p - 1.0 - sv), xy=(sv, p - 1.0 - sv),
                   xytext=(0, 12 if sv < 0.9 else -28), textcoords="offset points",
                   ha="center", fontsize=7.6)
    f.axvline(1.0, color=C["bad"], ls=":", lw=1.2)
    f.annotate("s = 1: where the OPERATOR\nis least bad (leg 51)", xy=(1.0, -0.45),
               xytext=(-8, 0), textcoords="offset points", ha="right", fontsize=7.6,
               color=C["bad"])
    f.set_xlabel("weight exponent $s$")
    f.set_ylabel(r"margin  $p - 1 - s$")
    f.set_title("E. FINITE where the margin is positive.\n"
                "the object side of the window is $s < %.3f$" % (p - 1.0), fontsize=10)
    f.grid(alpha=0.25)

    # -- F: the gate -------------------------------------------------------
    g.axis("off")
    ww = d["NB5_norms"]["weight_window_object_vs_operator"]
    ff = d["NB4_ablations"]["far_field_closure"]
    txt = (
        "GATE (pre-committed wording)\n"
        "Do HL_S2_nonsymmetric's compactified-basis coefficients\n"
        "decay fast enough that ||.||_(l^1_w) is finite for at least\n"
        "one admissible s < 0.394, with the exponent stable across\n"
        "the resolution ladder?\n\n"
        f"  ANSWER: {ev['GATE'].upper()}\n\n"
        f"  p = {d['NB5_norms']['p']:.4f} at X_max = 4.1e+04\n"
        f"  p = {ev['p_best']:.4f} at X_max = 3.0e+05\n"
        f"  systematic {ev['systematic']:.4f} (at the headline's own M = {ev['systematic_measured_at_M']})\n"
        f"  finite at s = {', '.join(str(x) for x in ev['admissible_classes_with_finite_norm'])}\n"
        f"  NOT resolved at s = {', '.join(str(x) for x in ev['admissible_classes_not_resolved'])}"
        "  (margin 0.96x the systematic)\n"
        f"  resolution drift {d['NB2_resolution_ladder']['p_drift_over_ladder']:.1e}\n\n"
        "SCOPE -- BOTH HALVES ARE THE RESULT\n"
        f"  object side   s_max = {ww['s_max_object']:.3f}\n"
        f"  operator side s     = {ww['s_operator']:.3f}  (leg 51)\n"
        f"  window        gap   = {ww['gap']:+.3f}  EMPTY\n\n"
        "The clause is RIGHT for s = 1 -- leg 51 TECHNICAL v2 sec 9\n"
        "already said the operator's best class is the target's\n"
        "infinite-norm class.  This CONFIRMS it.  Escalated, not edited.\n\n"
        "AND ONE HONEST NEGATIVE\n"
        f"  at the shipped domain X_max = 745 the far-field closure\n"
        f"  MOVES p by {ff['spread_where_it_fires']:.3f}.  The headline is measured\n"
        "  where no sample point leaves the grid at all.\n\n"
        "NOTHING HERE SAYS A CERTIFICATE CLOSES.  MM owns that.\n"
        "NO LINK OF THE L1->L4 CHAIN MOVED.  Clay ~0.05%."
    )
    g.text(0.02, 1.0, txt, va="top", ha="left", fontsize=7.5, family="monospace")
    g.set_title("F. the gate, and what it does not say", fontsize=10)

    fig.suptitle("Route-NB v1 — the target IS in the space, for every $s$ below "
                 "$\\alpha$ = %.3f; the operator needs $s$ = 1; the window is empty"
                 % d["NB5_norms"]["alpha"], fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig50_route_nb_v1_targetnorm.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
