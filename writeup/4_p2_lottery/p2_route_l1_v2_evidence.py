"""Phase-2 Route-L1 v2 (fig46): the representation change works, and then the tail fails.

Leg 50's certificate closed in interval arithmetic around a TRUNCATED grid object. This
leg rebuilds it in the compactified basis, where the three operators and the velocity are
exact on the whole line: the operator gap vanishes, the residual of the anchor is exactly
zero in rational arithmetic, and the truncation gap becomes one term -- a bound on
neglected Fourier coefficients. That term diverges in every weight class tested, and the
same code with dissipation saturates immediately.

Rebuild fig46 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_l1_v2_evidence.py
Regenerate the data (deterministic, ~55 s):
    .venv/bin/python -u experiments/p2_route_l1_v2_spectral.py

Six panels: A the exactness audit; B THE PICTURE — the tail term across weight classes,
inviscid against the dissipative control; C the divergence exponent as a function of the
weight exponent, with the object's admissible band; D the tail operator's structure (zero
diagonal, and a kernel that is the 1/X far field); E the four terms of the radii
polynomial side by side; F what this says and what it does not.
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
JSON = DATA / "p2_route_l1_v2_spectral.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    s1, s2, s3 = d["S1_exactness"], d["S2_exact_residual"], d["S3_terms"]
    s4, s6 = d["S4_control"], d["S6_window"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the exactness audit ------------------------------------------
    a = ax[0, 0]
    ks = [i["k"] for i in s1["identity"]]
    xn = np.arange(len(ks))
    a.bar(xn - 0.2, [max(i["defect_cos"], 1e-18) for i in s1["identity"]], 0.4,
          color=C["anchor"], alpha=0.85, label=r"$|\,\Re w^k-\cos k\theta\,|$")
    a.bar(xn + 0.2, [max(i["defect_sin"], 1e-18) for i in s1["identity"]], 0.4,
          color=C["ours"], alpha=0.85, label=r"$|\,\Im w^k-\sin k\theta\,|$")
    a.axhline(2.2e-16, color="k", ls=":", lw=1)
    a.text(-0.4, 2.6e-16, "machine epsilon", fontsize=8)
    a.set_yscale("log")
    a.set_xticks(xn)
    a.set_xticklabels([f"k={k}" for k in ks])
    a.set_ylabel("defect of the basis identity")
    a.set_ylim(1e-18, 1e-13)
    a.legend(fontsize=8, loc="upper left")
    a.set_title("A. the operators are EXACT, and the check is executable\n"
                f"$c_k=(-1)^k k$ exactly; the grid Hilbert transform\n"
                f"converges to the identity at $n^{{{s1['numeric_convergence_exponent']:.2f}}}$",
                fontsize=10)
    a.grid(alpha=0.3, axis="y")

    # ---- B: THE PICTURE — the tail term ----------------------------------
    b = ax[0, 1]
    style = {"flat": ("o-", C["bad"], r"flat $w_k=1$"),
             "algebraic": ("s-", C["warn"], None),
             "geometric": ("^-", C["ours"], None)}
    for t in s3["tail"]:
        mk, col, lab = style[t["class"]]
        if t["class"] == "algebraic":
            lab = rf"algebraic $s={t['param']:.3g}$"
            col = C["good"] if t["param"] == 1.0 else C["warn"]
        elif t["class"] == "geometric":
            lab = rf"geometric $\nu={t['param']:.2f}$"
            col = C["ours"] if t["param"] < 1.1 else "#3b0a5c"
        b.plot(t["M"], t["norm"], mk, color=col, lw=1.8, ms=5, label=lab)
    ctrl = [t for t in s4["tail"] if t["mu"] == 0.5 and t["class"] == "algebraic"][0]
    b.plot(ctrl["M"], ctrl["norm"], "d--", color=C["grey"], lw=2,
           label=r"CONTROL: $+\mu k$ dissipation")
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlabel("modes retained in the tail block, $M$")
    b.set_ylabel(r"$\|T_{\rm tail}^{-1}\|_w$")
    b.set_ylim(1e-2, 1e8)
    b.legend(fontsize=7.5, loc="upper left")
    b.set_title("B. THE TERM THAT RAN OUT: the tail inverse diverges in\n"
                "every weight class — and the same code saturates with dissipation",
                fontsize=10)
    b.grid(alpha=0.3, which="both")

    # ---- C: divergence exponent vs weight exponent -----------------------
    c = ax[0, 2]
    ss = [q["s"] for q in s6["curve"]]
    ee = [q["divergence_exponent"] for q in s6["curve"]]
    c.plot(ss, ee, "o-", color=C["anchor"], lw=2)
    alpha = d["target_alpha"]
    c.axvspan(-0.05, alpha, color=C["good"], alpha=0.16)
    c.text(alpha / 2, max(ee) * 0.92, "the only band where\nthe TARGET has\nfinite norm",
           ha="center", fontsize=8, color=C["good"])
    c.axvline(s6["window"]["s_operator"], color=C["bad"], ls="--", lw=1.5)
    c.text(s6["window"]["s_operator"] + 0.05, max(ee) * 0.55,
           f"operator's best\n$s={s6['window']['s_operator']:.2f}$", fontsize=8,
           color=C["bad"])
    c.axhline(0.0, color="k", lw=1.2)
    c.text(0.75, 0.06, "bounded tail would need this line", fontsize=8)
    c.set_xlabel(r"weight exponent $s$  ($w_k=(1+k)^s$)")
    c.set_ylabel("measured divergence exponent of the tail")
    c.set_title("C. THE WINDOW IS EMPTY, by "
                f"{s6['window']['gap']:.3f} in exponent units\n"
                "the whole curve sits above zero: no $s$ makes the tail bounded",
                fontsize=10)
    c.grid(alpha=0.3)

    # ---- D: the tail operator's structure --------------------------------
    e = ax[1, 0]
    from solver.spectral_certificate import homogeneous_tail_mode
    h = np.abs(homogeneous_tail_mode(801))
    m = np.arange(1, 802)
    sel = h > 0
    e.loglog(m[sel], h[sel], ".", color=C["ours"], ms=3, label="homogeneous tail mode")
    ref = h[sel][20] * (m[sel] / m[sel][20]) ** -2.0
    e.loglog(m[sel], ref, "k--", lw=1.2, label=r"$m^{-2}$")
    e.set_xlabel("mode index $m$")
    e.set_ylabel(r"$|h_m|$")
    e.legend(fontsize=8)
    e.set_title("D. the tail operator has ZERO DIAGONAL, and its kernel is\n"
                rf"$h_m\sim m^{{{s3['homogeneous_mode_exponent']:.3f}}}$ — i.e. the "
                rf"$|X|^{{-{s3['homogeneous_mode_alpha']:.2f}}}$ far field",
                fontsize=10)
    e.grid(alpha=0.3, which="both")

    # ---- E: the four terms -----------------------------------------------
    g = ax[1, 1]
    fb = [f for f in s3["finite_block"] if f["class"] == "algebraic" and f["K"] == 256][0]
    tail_best = min(s3["tail"], key=lambda t: t["divergence_exponent"])
    labels = [r"$Y_0$" + "\n(exact)", r"$Z_1$ finite" + "\n(rigorous)",
              r"$Z_2$" + "\n(basis algebra)", r"$Z_1$ TAIL" + "\n(M=1088)"]
    vals = [1e-20, fb["Z1_finite"], fb["Z2"], tail_best["norm"][-1]]
    cols = [C["good"], C["good"], C["good"], C["bad"]]
    g.bar(np.arange(4), vals, color=cols, alpha=0.85)
    g.set_yscale("log")
    g.set_xticks(np.arange(4))
    g.set_xticklabels(labels, fontsize=8)
    g.set_ylim(1e-21, 1e4)
    g.text(0, 3e-20, "EXACTLY 0\n(rational\narithmetic)", ha="center", fontsize=8,
           color=C["good"])
    g.text(3, tail_best["norm"][-1] * 2.5, "and still\nclimbing", ha="center", fontsize=8,
           color=C["bad"])
    g.set_title("E. three terms of four are finite and rigorous\n"
                f"($K=256$, algebraic $s=1$; the grid version's $Y_0$ was "
                f"5.2e-12 with two unbounded gaps)", fontsize=10)
    g.grid(alpha=0.3, axis="y")

    # ---- F: what it says, what it does not -------------------------------
    f = ax[1, 2]
    f.axis("off")
    txt = (
        "WHAT THE REPRESENTATION CHANGE BOUGHT\n"
        "  * the operator gap is GONE: H, the dilation and the\n"
        "    velocity are exact on the whole line, checked in\n"
        "    exact rational arithmetic\n"
        f"  * Y_0 = 0 EXACTLY ({s2['modes']} modes, Fraction(0))\n"
        "  * the truncation gap became ONE term: the neglected\n"
        "    Fourier coefficients\n\n"
        "AND WHAT THAT TERM DOES\n"
        f"  * flat l^1:   diverges like M^{s3['tail'][0]['divergence_exponent']:.2f}\n"
        f"  * algebraic:  best at s = {s6['window']['s_operator']:.2f}, still "
        f"M^{s6['window']['best_divergence_exponent']:.2f}\n"
        f"  * geometric:  x{s3['tail'][-1]['per_mode_growth']:.3f} PER MODE "
        f"(nu = {s3['tail'][-1]['param']:.2f})\n"
        "  * with dissipation: saturates in every class\n\n"
        "THE CEILING (pre-committed)\n"
        "  measured on the a = 0 CLM object: one mode, analytic,\n"
        "  in every class. A wall there bounds the difficulty for\n"
        "  the real target FROM BELOW. That target's far field\n"
        f"  alpha = {d['target_alpha']} does not even have finite norm in the\n"
        "  class where the operator side is least bad."
    )
    f.text(0.02, 0.97, txt, va="top", ha="left", fontsize=9.5, family="monospace")
    f.set_title("F. the ceiling, pre-committed before the numbers", fontsize=10)

    fig.suptitle("Route-L1 v2 — the certificate rebuilt where the operators are exact: "
                 "two open-ended gaps collapse into one, and that one is the weight class",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig46_route_l1_v2_spectral.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
