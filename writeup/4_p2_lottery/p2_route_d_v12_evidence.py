"""Phase-2 P2 Route-D v12 (fig30): the defect in the basis the bounds live in.

v11 drove the profile's residual to machine precision on the sinh-rho grid and
asked for the same measurement in the theta-collocation basis every Route-D bound
is written in.  Carrying it across needed the a-transport term in that basis
(exact velocity integrals I_k), and the measurement found something the far-field
analysis of eleven legs could not see: at a > 0 the effective transport speed
c + a U(X) VANISHES at a finite radius X_c, and the profile ends there with an
algebraic zero of order 1/a.  The a = 0 anchor -- the object all the decay-graded
machinery was designed around -- is the degenerate X_c = infinity limit.

Level-1 tooling + a structural finding, NOT a certificate.

Rebuilds fig30 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v12_evidence.py
Regenerate the data (deterministic; ~25 min):
    .venv/bin/python -u experiments/p2_route_d_v12_defect.py

Six panels: A the profiles and where they end; B the effective speed that ends
them; C the zero order against the prediction 1/a, in two discretizations;
D the defect in the certificate's own norm against the budget; E its convergence
rate in J; F what the real profile does to the operator norm the bounds price.
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
JSON = DATA / "p2_route_d_v12_defect.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.2))

    # -- A: the profiles, and where they stop ------------------------------
    a0 = ax[0, 0]
    cols = plt.cm.viridis(np.linspace(0.0, 0.85, len(d["t0_profiles"]["profiles"])))
    for col, p in zip(cols, d["t0_profiles"]["profiles"]):
        X = np.array(p["X"])
        om = np.abs(np.array(p["Omega"]))
        m = X > 0
        a0.loglog(X[m], np.maximum(om[m], 1e-20), color=col, lw=1.4,
                  label="a = %.2f" % p["a"])
        if np.isfinite(p["Xc"]):
            a0.axvline(p["Xc"], color=col, ls=":", lw=1.0)
    a0.set_xlim(1e-2, 3e3)
    a0.set_ylim(1e-18, 3)
    a0.set_xlabel("X"), a0.set_ylabel("|Omega|")
    a0.set_title("A. the profile ENDS at X_c (dotted): a>0 is not a tail")
    a0.legend(fontsize=7, loc="lower left")
    a0.grid(alpha=0.3, which="both")

    # -- B: the effective speed --------------------------------------------
    b = ax[0, 1]
    for col, p in zip(cols, d["t0_profiles"]["profiles"]):
        X = np.array(p["X"])
        E = np.array(p["E"])
        m = X > 0
        b.semilogx(X[m], E[m], color=col, lw=1.4, label="a = %.2f" % p["a"])
    b.axhline(0.0, color="k", lw=0.8)
    b.set_xlim(1e-1, 3e3)
    b.set_ylim(-1.5, 0.7)
    b.set_xlabel("X"), b.set_ylabel("E = c + a U(X)")
    b.set_title("B. the mechanism: U ~ (int Omega / pi) log X drags E through 0")
    b.legend(fontsize=7, loc="lower left")
    b.grid(alpha=0.3, which="both")

    # -- C: the zero order, two builds vs the prediction -------------------
    c = ax[0, 2]
    th = [r for r in d["t3_structure"]["theta_collocation"] if r["J"] == 800]
    rh = [r for r in d["t3_structure"]["sinh_rho"] if r["n"] == 801]
    A = [r["a"] for r in th]
    c.plot(A, [1.0 / x for x in A], "k--", lw=1.2, label="prediction 1/a")
    c.plot(A, [r["zero_order"] for r in th], "o-", color=C["anchor"], ms=5,
           label="theta-collocation (J=800)")
    c.plot([r["a"] for r in rh], [r["zero_order"] for r in rh], "s-",
           color=C["bad"], ms=5, label="sinh-rho (n=801)")
    c.set_xlabel("a"), c.set_ylabel("order p of the zero at X_c")
    c.set_title("C. Omega ~ (X_c - X)^p with p = 1/a, no fitted constant")
    c.legend(fontsize=8)
    c.grid(alpha=0.3)

    # -- D: the defect in the certificate's own norm -----------------------
    dd = ax[1, 0]
    t2 = d["t2_defect"]
    A2 = [r["a"] for r in t2["rows"]]
    dd.semilogy(A2, [max(r["Y0_upper"], 1e-18) for r in t2["rows"]], "o-",
                color=C["bad"], ms=5, label="Y0 <= ||A|| ||F||_Y")
    dd.semilogy(A2, [max(r["F_norm"], 1e-18) for r in t2["rows"]], "s--",
                color=C["anchor"], ms=4, label="||F||_Y (codomain norm)")
    dd.axhline(t2["Y0_max"], color=C["good"], lw=1.6,
               label="budget %.2e (v10)" % t2["Y0_max"])
    ctrl = d["t1_carry_over"]["control_exact_anchor"]["norm"]
    dd.axhline(max(ctrl, 1e-18), color=C["grey"], ls=":", lw=1.2,
               label="control: exact anchor %.1e" % ctrl)
    dd.set_xlabel("a"), dd.set_ylabel("defect")
    dd.set_title("D. what the certificate sees at (alpha,gamma) = (1.4, 0.15)")
    dd.legend(fontsize=7, loc="lower right")
    dd.grid(alpha=0.3, which="both")

    # -- E: the rate --------------------------------------------------------
    e = ax[1, 1]
    for col, blk in zip(plt.cm.plasma(np.linspace(0.1, 0.75, len(d["t4_rate"]))),
                        d["t4_rate"]):
        Js = [r["J"] for r in blk["rows"]]
        e.loglog(Js, [r["F_norm"] for r in blk["rows"]], "o-", color=col, ms=4,
                 label="a=%.1f: J^%.2f (pred %.2f)"
                       % (blk["a"], blk["log_slope"], blk["predicted_rate"]))
    e.axhline(d["t2_defect"]["Y0_max"] / d["meta"]["A_norm_upper_v10"],
              color=C["good"], lw=1.4, label="||F||_Y the budget allows")
    e.set_xlabel("J"), e.set_ylabel("||F||_Y")
    e.set_title("E. algebraic, not spectral: limited regularity at X_c")
    e.legend(fontsize=7, loc="lower left")
    e.grid(alpha=0.3, which="both")

    # -- F: does the operator transfer? ------------------------------------
    f = ax[1, 2]
    lad = d["t5_operator"]["ladder"]
    for col, a in zip([C["good"], C["warn"], C["bad"]],
                      sorted({r["a"] for r in lad})):
        rs = [r for r in lad if r["a"] == a]
        f.loglog([r["J"] for r in rs], [r["norm"] for r in rs], "o-", color=col,
                 ms=5, label="a=%.1f: J^%+.2f" % (a, rs[0]["log_slope"]))
    f.set_xlabel("J"), f.set_ylabel("||A|| (sup-to-sup, graded, alpha=1.4)")
    f.set_title("F. flat at the anchor, DIVERGENT at the real profile")
    f.legend(fontsize=8)
    f.grid(alpha=0.3, which="both")

    fig.suptitle("Route-D v12 - Y0 in the bounds' own basis: the a>0 profile "
                 "ends at a finite radius (float64, NOT a certificate)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "fig30_p2_route_d_v12_defect.png"
    fig.savefig(out, dpi=150)
    print("[fig] wrote %s" % out)


if __name__ == "__main__":
    build_figure()
