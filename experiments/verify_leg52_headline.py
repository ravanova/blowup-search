"""VERIFIER: re-measure leg 52's (Route-T v1) headline, and ablate the MECHANISM (lesson 85).

This script does NOT repair anything and does NOT touch any file leg 51/52 produced.  It
re-derives leg 52's headline numbers independently of its driver, and then asks the
questions the headline's own construction leaves open -- the ones a TC assembly would
inherit.

  V1  REPRODUCTION.  Recompute the five ladders from `solver/spectral_certificate.py`
      directly and compare to the committed JSON, elementwise.
  V2  NEGATIVE CONTROLS.  Is the second-singular-pair top rung EXACTLY the unbordered
      value (leg 52 claims 48.76 = 48.76)?  Do both controls diverge in all five classes?
  V3  NORMALISATION ABLATION.  `bordered_tail_inverse_norm` measures a weighted-l^1
      operator norm, but normalises the two border vectors in the EUCLIDEAN norm, and
      gives the border unknown weight 1.  ||B^{-1}|| is NOT invariant under rescaling
      u, v.  Re-run the analytic border with the border vectors normalised in the norm
      the operator norm actually uses.  If the saturation is an artifact of the
      Euclidean convention, it dies here.
  V4  ADJOINT CONVENTION.  In scaled coordinates Ts = W T W^{-1}, the left null vector
      is u/w, not u*w; the driver borders with u*w.  Both are legitimate borders (the
      matrix is still invertible) but only one is "the adjoint".  Measure both.
  V5  LADDER EXTENSION.  The committed M ladder (320, 576, 1088, 2112, 3136) is not
      geometric -- its last step is 1.48x where the others are ~1.9x, so the last
      increment is over a SHORTER interval in log M and the "increments are falling"
      reading is partly a step-size effect.  Re-measure increments per unit log M, and
      extend the ladder to M = 6208.
  V6  K-DEPENDENCE.  The whole leg is at K = 64.  Does the saturation survive K = 32
      and K = 128?
  V7  THE ANALYTIC MODE IS ONLY APPROXIMATELY A KERNEL.  `tail_right_null` fixes h_0 = 1
      and ignores the block's first row.  Report ||T h|| / ||h|| and ||u^T T|| / ||u||.

Run: .venv/bin/python -u experiments/verify_leg52_headline.py
Writes nothing under writeup/data (verification only); prints a report.
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.spectral_certificate import (                                    # noqa: E402
    bordered_tail_inverse_norm, fredholm_sides, tail_inverse_norm,
    tail_left_null, tail_right_null, tail_singular_pair, _scaled_tail,
)

COMMITTED = ROOT / "writeup" / "data" / "p2_route_t_v1_border.json"
K_TAIL = 64
M_LADDER = (320, 576, 1088, 2112, 3136)
CLASSES = (("flat", 0.0), ("algebraic", 0.3), ("algebraic", 0.394),
           ("algebraic", 1.0), ("algebraic", 1.5))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def bordered_custom(K, M, kind, param, scale="l2", adjoint="times_w"):
    """`bordered_tail_inverse_norm` with the two conventions exposed as knobs."""
    Ts, w = _scaled_tail(K, M, kind, param)
    v = tail_right_null(K, M) * w
    u = tail_left_null(K, M) * (w if adjoint == "times_w" else 1.0 / w)
    if scale == "l2":
        v, u = v / np.linalg.norm(v), u / np.linalg.norm(u)
    elif scale == "l1":
        v, u = v / np.abs(v).sum(), u / np.abs(u).sum()
    elif scale == "linf":
        v, u = v / np.abs(v).max(), u / np.abs(u).max()
    elif scale == "l1u_linfv":       # the pairing a weighted-l^1 certificate induces:
        v, u = v / np.abs(v).max(), u / np.abs(u).sum()   # v in the dual, u in the space
    else:
        raise ValueError(scale)
    n = Ts.shape[0]
    B = np.empty((n + 1, n + 1))
    B[:n, :n] = Ts
    B[:n, n] = u
    B[n, :n] = v
    B[n, n] = 0.0
    return float(np.max(np.abs(np.linalg.inv(B)).sum(0)))


def shape(ms, vals):
    ms, vals = np.asarray(ms, float), np.asarray(vals, float)
    inc = np.diff(vals)
    dlog = np.diff(np.log(ms))
    return {"vals": [round(float(x), 4) for x in vals],
            "inc": [round(float(x), 4) for x in inc],
            "inc_per_dlogM": [round(float(x), 4) for x in inc / dlog],
            "exponent": round(float(np.polyfit(np.log(ms), np.log(vals), 1)[0]), 4)}


def main():
    t0 = time.time()
    ok, gaps = [], []

    def check(name, got, want, tol=2e-3):
        good = rel(got, want) <= tol
        (ok if good else gaps).append(f"{name}: got {got!r} vs claimed {want!r}")
        print(f"  [{'OK ' if good else 'GAP'}] {name}: {got:.6g}  (claimed {want:.6g}, "
              f"rel {rel(got, want):.2g})")

    d = json.loads(COMMITTED.read_text())
    lad = {(r["class"], r["param"]): r for r in d["T1_ladders"]}

    # ---------------- V1 reproduction --------------------------------------
    print("\n=== V1  REPRODUCTION of the committed ladders (independent of the driver)")
    maxrel = 0.0
    for kind, p in CLASSES:
        row = lad[(kind, float(p))]
        for lab in ("analytic", "svd", "second", "random"):
            mine = [bordered_tail_inverse_norm(K_TAIL, M, kind, p, border=lab)
                    for M in M_LADDER]
            maxrel = max(maxrel, max(rel(a, b) for a, b in zip(mine, row[lab])))
        mine = [tail_inverse_norm(K_TAIL, M, kind, p) for M in M_LADDER]
        maxrel = max(maxrel, max(rel(a, b) for a, b in zip(mine, row["unbordered"])))
        sp = [tail_singular_pair(K_TAIL, M, kind, p) for M in M_LADDER]
        maxrel = max(maxrel, max(rel(a, b) for a, b in zip([s[0] for s in sp],
                                                           row["sigma_min"])))
        maxrel = max(maxrel, max(rel(a, b) for a, b in zip([s[2] for s in sp],
                                                           row["alignment"])))
        print(f"  {kind:9s} s={p:<6.3g} reproduced")
    print(f"  max relative deviation over every committed ladder entry: {maxrel:.3e}")
    (ok if maxrel < 1e-9 else gaps).append(f"reproduction maxrel={maxrel:.3e}")

    # ---------------- V1b prose numbers ------------------------------------
    print("\n=== V1b  PROSE vs JSON (the headline table)")
    flat, a03, a10, a15 = (lad[("flat", 0.0)], lad[("algebraic", 0.3)],
                           lad[("algebraic", 1.0)], lad[("algebraic", 1.5)])
    check("flat unbordered first", flat["unbordered"][0], 4.06, 2e-3)
    check("flat unbordered last", flat["unbordered"][-1], 48.76, 2e-3)
    check("flat unbordered exponent", flat["unbordered_shape"]["exponent"], 1.085, 2e-3)
    check("flat analytic first", flat["analytic"][0], 7.46, 2e-3)
    check("flat analytic last", flat["analytic"][-1], 9.44, 2e-3)
    check("flat analytic exponent", flat["analytic_shape"]["exponent"], 0.100, 6e-3)
    check("s=0.3 unbordered", a03["unbordered"][-1], 20.67, 2e-3)
    check("s=0.3 analytic last", a03["analytic"][-1], 11.37, 2e-3)
    check("s=0.3 analytic exponent", a03["analytic_shape"]["exponent"], 0.147, 5e-3)
    check("s=1.0 analytic last", a10["analytic"][-1], 20.51, 2e-3)
    check("s=1.5 analytic last", a15["analytic"][-1], 31.81, 2e-3)
    check("T5 kernel exponent", d["T5_fredholm"]["kernel_exponent"], -2.0024, 1e-3)
    check("T5 cokernel exponent", d["T5_fredholm"]["cokernel_exponent"], 1.0012, 1e-3)
    for lbl, want in (("flat", 1.000), ("algebraic", 1.007)):
        got = [x for x in d["T2_analytic_vs_svd"]
               if x["class"] == lbl and x["param"] in (0.0, 0.3)][0]["ratio_last"]
        check(f"analytic/SVD {lbl}", got, want, 2e-3)
    check("alignment flat", d["T4_alignment_top"]["flat_0.0"], 1.00000, 1e-5)
    check("alignment s=1.5", d["T4_alignment_top"]["algebraic_1.5"], 0.90209, 1e-5)

    # ---------------- V2 negative controls ---------------------------------
    print("\n=== V2  NEGATIVE CONTROLS")
    r = rel(flat["second"][-1], flat["unbordered"][-1])
    print(f"  second-pair top rung {flat['second'][-1]:.10f} vs unbordered "
          f"{flat['unbordered'][-1]:.10f}  rel {r:.2e}")
    (ok if r < 1e-12 else gaps).append(f"second==unbordered rel={r:.2e}")
    for kind, p in CLASSES:
        row = lad[(kind, float(p))]
        rr = rel(row["second"][-1], row["unbordered"][-1])
        print(f"  {kind:9s} s={p:<6.3g} second/unbordered = "
              f"{row['second'][-1] / row['unbordered'][-1]:.4f}  "
              f"(the 'lands exactly on it' claim holds only in the flat class)")
        del rr
    div = all(not lad[(k, float(p))][lab + "_shape"]["saturating"]
              for k, p in CLASSES for lab in ("second", "random"))
    print(f"  both controls diverge in all five classes: {div}")
    (ok if div else gaps).append(f"controls diverge {div}")

    # ---------------- V7 is the analytic mode a kernel ----------------------
    print("\n=== V7  THE ANALYTIC BORDER'S OWN DEFECT (it is only approximately a kernel)")
    for M in (1088, 3136):
        Ts, w = _scaled_tail(K_TAIL, M, "flat", 0.0)
        h, u = tail_right_null(K_TAIL, M), tail_left_null(K_TAIL, M)
        print(f"  M={M:5d}  ||T h||/||h|| = {np.linalg.norm(Ts @ h) / np.linalg.norm(h):.3e}"
              f"   ||u^T T||/||u|| = {np.linalg.norm(u @ Ts) / np.linalg.norm(u):.3e}"
              f"   sigma_min = {np.linalg.svd(Ts, compute_uv=False)[-1]:.3e}")

    # ---------------- V3/V4 conventions ------------------------------------
    print("\n=== V3/V4  ABLATION: the two conventions the constant depends on")
    print("  ||B^-1|| is NOT invariant under rescaling u and v; the driver picks the")
    print("  EUCLIDEAN normalisation while the norm measured is weighted l^1.")
    for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
        print(f"  -- {kind} s={p}")
        for scale in ("l2", "l1", "linf", "l1u_linfv"):
            vals = [bordered_custom(K_TAIL, M, kind, p, scale=scale) for M in M_LADDER]
            s = shape(M_LADDER, vals)
            print(f"     norm={scale:10s} {s['vals']}  exp {s['exponent']:+.3f}  "
                  f"inc/dlogM {s['inc_per_dlogM']}")
        for adj in ("times_w", "over_w"):
            vals = [bordered_custom(K_TAIL, M, kind, p, adjoint=adj) for M in M_LADDER]
            s = shape(M_LADDER, vals)
            print(f"     adjoint={adj:9s} {s['vals']}  exp {s['exponent']:+.3f}")

    # ---------------- V5 ladder extension ----------------------------------
    print("\n=== V5  LADDER EXTENSION and increments per unit log M")
    LONG = (320, 576, 1088, 2112, 3136, 4160, 6208)
    for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
        vals = [bordered_tail_inverse_norm(K_TAIL, M, kind, p) for M in LONG]
        un = [tail_inverse_norm(K_TAIL, M, kind, p) for M in LONG]
        s, su = shape(LONG, vals), shape(LONG, un)
        print(f"  {kind:9s} s={p}  M={LONG}")
        print(f"     bordered   {s['vals']}  exp {s['exponent']:+.3f}")
        print(f"     inc/dlogM  {s['inc_per_dlogM']}")
        print(f"     unbordered {su['vals']}  exp {su['exponent']:+.3f}")

    # ---------------- V6 K dependence --------------------------------------
    print("\n=== V6  K-DEPENDENCE (the whole leg is at K = 64)")
    for K in (32, 64, 128):
        for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
            vals = [bordered_tail_inverse_norm(K, M, kind, p) for M in M_LADDER]
            s = shape(M_LADDER, vals)
            print(f"  K={K:4d} {kind:9s} s={p}  {s['vals']}  exp {s['exponent']:+.3f}")
        print(f"  K={K:4d} fredholm {fredholm_sides(K, 3136)['kernel_exponent']:+.4f} / "
              f"{fredholm_sides(K, 3136)['cokernel_exponent']:+.4f}")

    # ---------------- V6b does the larger-K ladder still saturate ----------
    print("\n=== V6b  DOES THE LARGER-K LADDER STILL SATURATE (out to M = 6208)")
    for K in (128, 256):
        for kind, p in (("flat", 0.0), ("algebraic", 0.3)):
            v = np.array([bordered_tail_inverse_norm(K, M, kind, p) for M in LONG])
            dd = np.diff(v) / np.diff(np.log(LONG))
            print(f"  K={K:4d} {kind:9s} s={p}  {np.round(v, 4).tolist()}")
            print(f"        inc/dlogM {np.round(dd, 4).tolist()}  exp "
                  f"{np.polyfit(np.log(LONG), np.log(v), 1)[0]:+.4f}")

    # ---------------- V7b where the border defect lives --------------------
    print("\n=== V7b  WHERE THE ANALYTIC BORDER'S DEFECT LIVES (flat, K = 64) -- TC-3")
    from solver.spectral_certificate import tail_block                     # noqa: E402
    for M in (576, 1088, 2112, 3136, 6208):
        T, h, u = tail_block(64, M), tail_right_null(64, M), tail_left_null(64, M)
        r, ru = T @ h, u @ T
        n2 = np.linalg.norm(r) / np.linalg.norm(h)
        li = np.abs(ru).max() / np.abs(u).max()
        print(f"  M={M:5d} ||T h||2/||h||2 = {n2:.4e} (interior rows "
              f"{np.linalg.norm(r[:-1]) / np.linalg.norm(h):.1e}, M x it = {M * n2:.0f})"
              f" | l1 {np.abs(r).sum() / np.abs(h).sum():.4e}"
              f" | ||u^T T||inf/||u||inf = {li:.4e} (interior cols "
              f"{np.abs(ru[1:]).max() / np.abs(u).max():.1e}, M x it = {M * li:.0f})")

    print(f"\n=== SUMMARY  {len(ok)} checks passed, {len(gaps)} gaps "
          f"({time.time() - t0:.0f}s)")
    for g in gaps:
        print("  GAP:", g)


if __name__ == "__main__":
    main()
