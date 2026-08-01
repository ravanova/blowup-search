"""Phase-2 P2 Route-D v14 (fig32): the first integral, and the kill switch passing.

The two-scale profile equation has an exact first integral, Omega = -(E/c)^{1/a}
with E = c + aU.  It contains the known a = 0 anchor as its degenerate limit, it
FORCES the compact support v12 discovered by measurement, and it reduces the whole
problem to a scalar equation on [0, X_c].  Posed that way, the approximate inverse
that diverged as J^+2.86 on the whole line is FLAT: K^+0.0001 over an 8x refinement.
Level-1 tooling plus a structural identity -- NOT a certificate.

Rebuilds fig32 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v14_evidence.py
Regenerate the data (deterministic; ~6 min):
    .venv/bin/python -u experiments/p2_route_d_v14_first_integral.py

Six panels: A the identity vanishing with J on an independent build; B the profile
on its own support; C THE KILL SWITCH, reduced vs whole-line on one axis; D the
radius law with the profile's own constants; E large-a K-convergence; F the
ledger of what the reformulation retires.
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
JSON = DATA / "p2_route_d_v14_first_integral.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.6))

    # ---- A: the identity, on a build that knows nothing about it -----------
    A = d["A_identity"]
    a0 = ax[0, 0]
    for a, col in (("0.2", C["anchor"]), ("0.3", C["good"])):
        r = A[a]
        a0.loglog(r["J"], r["defect"], "o-", color=col, label=f"a={a}: FI defect")
        a0.loglog(r["J"], r["relres"], "s--", color=col, alpha=0.45,
                  label=f"a={a}: profile residual")
    a0.set_xlabel("J (whole-line collocation)")
    a0.set_ylabel("relative spread of $|\\Omega|/E^{1/a}$")
    a0.set_title("A  the first integral is exact\n"
                 "defect $\\to$ 0 no slower than the profile's own error",
                 fontsize=10)
    a0.legend(fontsize=7)
    a0.grid(alpha=0.3, which="both")
    a0.text(0.03, 0.05, "$a\\to0$ limit vs the EXACT anchor: "
            f"{A['anchor_limit_max_err']:.1e}", transform=a0.transAxes,
            fontsize=8, color=C["good"],
            bbox=dict(fc="white", ec=C["good"], alpha=0.9))

    # ---- B: the profile on its own support --------------------------------
    B = d["B_profile"]
    a1 = ax[0, 1]
    v = np.asarray(B["v"])
    for a, Xc in zip(B["a"], B["Xc"]):
        a1.plot(v * Xc, B["Omega"][str(a)], lw=1.6,
                label=f"a={a}, $X_c/c$={Xc:.2f}")
    a1.set_xscale("log")
    a1.set_xlim(0.03, 45)
    a1.set_xlabel("$X/c$")
    a1.set_ylabel("$\\Omega$")
    a1.set_title("B  the profile ENDS -- forced by the identity,\n"
                 "not imposed on the grid", fontsize=10)
    a1.legend(fontsize=7, loc="lower left")
    a1.grid(alpha=0.3)
    txt = "\n".join(f"a={a}: edge exponent {q:.5f} vs 1/a={1/a:.5f}"
                    for a, q in zip(B["a"], B["edge_exponent"]))
    a1.text(0.03, 0.60, txt, transform=a1.transAxes, fontsize=6.6,
            family="monospace", bbox=dict(fc="white", ec=C["grey"], alpha=0.9))

    # ---- C: THE KILL SWITCH ------------------------------------------------
    Cd = d["C_kill_switch"]
    a2 = ax[0, 2]
    for a, col in (("0.2", "#6a3d9a"), ("0.3", C["good"]),
                   ("0.4", "#1f78b4"), ("0.5", C["warn"])):
        r = Cd["reduced"][a]
        a2.loglog(r["K"], r["norm_e"], "o-", color=col,
                  label=f"reduced, a={a}: $K^{{{r['slope_e_resolved']:+.4f}}}$")
    for a, col, mk in (("0.0", C["grey"], "s"), ("0.2", C["bad"], "^"),
                       ("0.3", C["bad"], "v")):
        r = Cd["control"][a]
        a2.loglog(r["J"], r["norm"], mk + "--", color=col, alpha=0.8,
                  label=f"whole line, a={a}: $J^{{{r['slope']:+.3f}}}$")
    a2.set_xlabel("modes (K reduced / J whole line)")
    a2.set_ylabel("$\\|A\\|$")
    a2.set_title("C  THE KILL SWITCH\nremove the far field and the inverse converges",
                 fontsize=10)
    a2.set_xticks([16, 32, 64, 128, 200, 400, 800])
    a2.set_xticklabels(["16", "32", "64", "128", "200", "400", "800"], fontsize=8)
    a2.minorticks_off()
    a2.legend(fontsize=6.4, loc="center left")
    a2.grid(alpha=0.3, which="major")

    # ---- D: the radius law -------------------------------------------------
    D = d["D_radius_law"]
    a3 = ax[1, 0]
    inv_a = 1.0 / np.asarray(D["a"])
    a3.semilogy(inv_a, D["Xc"], "o-", color=C["good"], label="measured $X_c/c$")
    a3.semilogy(inv_a, D["Xc_pred"], "s--", color=C["anchor"],
                label="$\\exp[-\\pi(c/a+U_0)/m]$, own $(m,U_0)$")
    a3.semilogy(inv_a, np.exp(inv_a * 1.0), ":", color=C["bad"],
                label="v12's $e^{c/a}$ (anchor's $m=-\\pi$)")
    a3.set_xlabel("$1/a$")
    a3.set_ylabel("$X_c/c$")
    a3.set_ylim(1, 200)
    a3.set_title("D  the radius law, constants MEASURED\n"
                 "the exponent is $-\\pi c/(am)$, not $c/a$", fontsize=10)
    a3.legend(fontsize=7)
    a3.grid(alpha=0.3, which="both")
    ratio = np.asarray(D["Xc_pred"]) / np.asarray(D["Xc"])
    a3.text(0.35, 0.06, "law/measured: %.3f (a=%.2f) -> %.3f (a=%.2f)"
            % (ratio[0], D["a"][0], ratio[-1], D["a"][-1]),
            transform=a3.transAxes, fontsize=7.5,
            bbox=dict(fc="white", ec=C["grey"], alpha=0.9))

    # ---- E: large-a convergence -------------------------------------------
    E = d["E_large_a"]
    a4 = ax[1, 1]
    keys = sorted(E, key=float)
    sp = [max(E[k]["spread"], 1e-16) for k in keys]
    a4.bar(range(len(keys)), sp, color=[C["good"]] * len(keys))
    a4.set_yscale("log")
    a4.set_xticks(range(len(keys)))
    a4.set_xticklabels([f"a={k}" for k in keys], fontsize=8)
    a4.axhline(1e-9, color=C["grey"], ls="--", lw=1)
    a4.set_ylabel("relative spread of $X_c/c$ over $K \\geq 64$")
    a4.set_title("E  grid converged well past $a^*\\approx0.5$\n"
                 "v11's fourth confirmation was the whole-line basis", fontsize=10)
    a4.grid(alpha=0.3, axis="y", which="both")
    a4.text(0.03, 0.86, "v11 read n-spread 3.7e-3 / 1.3e-2 at a=0.8 / 1.0\n"
                        "as 'not a continuum object'.  On its own support\n"
                        "the same object is converged to ~1e-10.",
            transform=a4.transAxes, fontsize=7,
            bbox=dict(fc="white", ec=C["warn"], alpha=0.95))

    # ---- F: the ledger -----------------------------------------------------
    a5 = ax[1, 2]
    a5.axis("off")
    k03 = Cd["reduced"]["0.3"]
    lines = [
        ("WHAT THE FIRST INTEGRAL RETIRES", "head"),
        ("", "n"),
        ("$\\Omega = -(E/c)^{1/a}$,  $E = c + aU$,  $U_X = H(\\Omega)$", "eq"),
        ("", "n"),
        ("v12  profile ends at $X_c$      measured $\\to$ FORCED", "good"),
        ("v12  zero of order $1/a$        balance $\\to$ exact, with amplitude",
         "good"),
        ("v12  $X_c\\sim e^{c/a}$             anchor's $m$ $\\to$ own $(m,U_0)$, 0.3%",
         "good"),
        ("v13  far-field growing mode    removed from the DOMAIN", "good"),
        ("v11  'not continuum past $a^*$'  was the whole-line basis", "warn"),
        ("", "n"),
        (f"KILL SWITCH:  $\\|A\\|$ = {k03['norm_e'][0]:.3f} $\\to$ "
         f"{k03['norm_e'][-1]:.3f} over K=16..192", "good"),
        (f"              $K^{{{k03['slope_e_resolved']:+.4f}}}$  (whole line: "
         f"$J^{{{Cd['control']['0.2']['slope']:+.2f}}}$)", "good"),
        ("", "n"),
        ("NOT CLAIMED: a certificate. Different operator in a", "bad"),
        ("different space from the 47-70 of v7-v9; what is", "bad"),
        ("comparable is the SLOPE, not the value.  Nothing here", "bad"),
        ("is interval-enclosed. Still Level-1 + tooling.", "bad"),
    ]
    y = 0.97
    for txt, kind in lines:
        if kind == "n":
            y -= 0.028
            continue
        col = {"head": "black", "eq": C["anchor"], "good": C["good"],
               "warn": C["warn"], "bad": C["bad"]}[kind]
        a5.text(0.0, y, txt, transform=a5.transAxes, fontsize=8.4, color=col,
                family="monospace" if kind in ("good", "warn", "bad") else None,
                weight="bold" if kind == "head" else None)
        y -= 0.052

    fig.suptitle("Route-D v14 — the two-scale profile equation has a first integral, "
                 "and on its own support the inverse converges",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig32_route_d_v14_first_integral.png"
    fig.savefig(out, dpi=145)
    print("wrote " + str(out))


if __name__ == "__main__":
    build_figure()
