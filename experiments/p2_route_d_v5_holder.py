"""P2 Route-D v5 -- THE TWO-GRADING SPACE: does decay x smoothness close the gap?

The last two legs each found half of the requirement and neither could satisfy it:

  v3 (fig21): a diagonal weight on Fourier coefficients measures SMOOTHNESS; the
              far-field transport needs DECAY.  No weighted-ell^1 pair works, and
              the obstruction is a conservation law.
  v4 (fig22): a weighted SUP norm measures DECAY and fixes the inverse -- but the
              Hilbert transform is unbounded on L^infinity, so the QUADRATIC term
              is uncontrolled.  Smoothness is needed as well.

So the certificate's space has to carry both gradings at once.  The classical
setting where H IS bounded is Holder, so the candidate is the two-parameter family

    ||h||_{a,g} = sup (1+X^2)^{a/2}|h|
                + sup_{j!=k} min over the pair of (1+X^2)^{(a-g)/2}
                  |h_j - h_k| / |th_j - th_k|^g

(the seminorm weight a-g is FORCED by the conformal geometry, not chosen -- see
solver/holder_norms.py; with weight a the model profile f_a itself would have
infinite seminorm).

NOT a logged Tier-1/2 experiment: deterministic (no GA, no seeds, no predicate
lock).  Run:

    .venv/bin/python experiments/p2_route_d_v5_holder.py
    -> writeup/data/p2_route_d_v5_holder.json ; figure via
       .venv/bin/python writeup/4_p2_lottery/p2_route_d_v5_evidence.py      (fig23)

SIX measurements.

  U1  THE DEFUSAL.  The exact construction that broke v4 -- partial sums of a
      square wave, bounded with a logarithmically divergent conjugate -- measured
      in both norms.  If the sup ratio grows and the Holder ratio does not, the v4
      obstruction is removed by the smoothness scale, at every gamma.

  U2  THE COST OF SMOOTHNESS.  The Holder constant of H against gamma.  It must
      blow up as gamma -> 0 (no smoothness = the v4 problem) and as gamma -> 1
      (Lipschitz, where H fails again), so gamma has an interior optimum of its
      own -- structurally the same shape alpha has.

  U3  THE INVERSE IN THE TWO-GRADED PAIR.  ||A|| over the (alpha, gamma) plane on
      a grid ladder.  FAMILY-RESTRICTED (a lower bound; the exact induced norm
      between two polyhedral norms is a linear program and this project has no LP).
      The question it can answer honestly: does it SATURATE in J, and where in the
      plane is it smallest?

  U4  THE QUADRATIC IN THE TWO-GRADED PAIR.  The same constant v4 measured, now in
      the Holder norm, on the adversary AND the smooth family.  v4's log growth
      should be gone.

  U5  THE JOINT OPTIMUM.  Z2 = 2||A||C_Q and the budget ceiling over (alpha,
      gamma).  Two independent optima, one per grading, and where they land.

  U6  THE LEDGER.  An explicit list of what is bounded, what is family-restricted,
      and what is not bounded at all.  Nothing here closes and nothing here is
      rigorous; the point is to know exactly which pieces are still missing.
"""

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import (  # noqa: E402
    Collocation, gauged_jacobian, sup_op_norm, C_ANCHOR,
)
from solver.holder_norms import (  # noqa: E402
    HolderNorm, family_op_norm, jacobian_identity_error,
)
from solver.decay_grading import cos_power_mass  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_d_v5_holder.json"

J_LADDER = [250, 500, 1000]
ALPHA_GRID = [1.2, 1.4, 1.5, 1.6, 1.8]
GAMMA_GRID = [0.15, 0.25, 0.35, 0.5, 0.65, 0.75, 0.85]
GAMMA_MAIN, ALPHA_MAIN = 0.5, 1.5


class GaugedNorm:
    """Codomain norm on [gauge slot ; collocation rows]: max(|g_0|, ||g_rest||)."""

    def __init__(self, col, rows, alpha, gamma):
        self.inner = HolderNorm(col.theta[rows], col.X[rows], alpha, gamma)
        self.w = np.empty(col.J)
        self.w[0] = 1.0
        self.w[1:] = self.inner.w

    def __call__(self, g):
        g = np.asarray(g, dtype=float)
        return max(abs(float(g[0])), self.inner(g[1:]))


def square_wave(theta, m):
    j = np.arange((int(m) - 1) // 2 + 1)
    k = 2 * j + 1
    c = (4.0 / np.pi) * (-1.0) ** j / k
    return np.cos(np.outer(theta, k)) @ c, np.sin(np.outer(theta, k)) @ c


def power_fit(xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    if np.any(ys <= 0):
        return float("nan")
    return float(np.polyfit(np.log(xs), np.log(ys), 1)[0])


# ---------------------------------------------------------------------------


def u1_defusal(J=2000, degrees=(8, 16, 32, 64, 128, 256, 512)):
    th = np.pi * (np.arange(J) + 0.5) / J
    X = np.tan(0.5 * th)
    out = []
    for gamma in GAMMA_GRID:
        hn = HolderNorm(th, X, 0.0, gamma, semi_alpha=0.0)     # plain: no decay weight
        sup_r, hol_r = [], []
        for m in degrees:
            p, Hp = square_wave(th, m)
            sup_r.append(float(np.max(np.abs(Hp)) / np.max(np.abs(p))))
            hol_r.append(hn(Hp) / hn(p))
        out.append({"gamma": gamma, "degrees": list(degrees),
                    "sup_ratio": sup_r, "holder_ratio": hol_r,
                    "sup_growth": sup_r[-1] / sup_r[0],
                    "holder_growth": hol_r[-1] / hol_r[0]})
    return out


def u2_holder_H_constant(J=2000, n_random=300, seed=11):
    """C_H(gamma): the best ratio [H p] / ||p|| over adversarial + random families."""
    th = np.pi * (np.arange(J) + 0.5) / J
    X = np.tan(0.5 * th)
    k_all = np.arange(256)
    Cm, Sm = np.cos(np.outer(th, k_all)), np.sin(np.outer(th, k_all))
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_random):
        m = int(rng.integers(2, 200))
        a = rng.standard_normal(m + 1) / (1.0 + np.arange(m + 1)) ** rng.uniform(0.0, 1.5)
        draws.append((Cm[:, :m + 1] @ a, Sm[:, :m + 1] @ a))
    for m in (8, 32, 128, 512):
        draws.append(square_wave(th, m))
    out = []
    for gamma in GAMMA_GRID:
        hn = HolderNorm(th, X, 0.0, gamma, semi_alpha=0.0)
        best = 0.0
        for p, Hp in draws:
            n = hn(p)
            if n > 0:
                best = max(best, hn(Hp) / n)
        out.append({"gamma": gamma, "C_H": best})
    return out


def u3_inverse(J_ladder=J_LADDER, max_candidates=120):
    """||A|| over (alpha, gamma), family-restricted, on a grid ladder."""
    per_J = {}
    for J in J_ladder:
        col = Collocation(J)
        M, rows = gauged_jacobian(col, col.anchor(), C_ANCHOR)
        A = np.linalg.inv(M)
        step = max(1, A.shape[0] // max_candidates)
        idx = np.arange(0, A.shape[0], step)
        vals = {}
        for alpha in ALPHA_GRID:
            for gamma in GAMMA_GRID:
                dom = HolderNorm(col.theta, col.X, alpha, gamma)
                cod = GaugedNorm(col, rows, alpha + 1.0, gamma)
                S = np.sign(A[idx]) / cod.w[None, :]
                best = 0.0
                for g in S:
                    ng = cod(g)
                    if ng > 0:
                        best = max(best, dom(A @ g) / ng)
                # the natural residual directions too
                for beta in (alpha + 1.0, alpha + 1.5, 3.0):
                    g = np.empty(col.J)
                    g[0] = 0.0
                    g[1:] = (1.0 + col.X[rows] ** 2) ** (-0.5 * beta)
                    ng = cod(g)
                    if ng > 0:
                        best = max(best, dom(A @ g) / ng)
                vals[(alpha, gamma)] = best
        per_J[J] = vals
    rows_out = []
    for alpha in ALPHA_GRID:
        for gamma in GAMMA_GRID:
            ys = [per_J[J][(alpha, gamma)] for J in J_ladder]
            rows_out.append({"alpha": alpha, "gamma": gamma,
                             "A_per_J": ys, "A_norm": ys[-1],
                             "growth_exponent_in_J": power_fit(J_ladder, ys)})
    return {"J_ladder": list(J_ladder), "max_candidates": max_candidates,
            "rows": rows_out,
            "caveat": "FAMILY-RESTRICTED: a lower bound on the induced norm. The "
                      "exact induced norm between two polyhedral norms is a linear "
                      "program and this project has no LP."}


def u3b_focused_ladder(alpha=ALPHA_MAIN, gamma=GAMMA_MAIN,
                      Js=(125, 250, 500, 1000, 2000), max_candidates=120):
    """The same norm on a LONGER ladder at one (alpha, gamma): does it saturate?

    The coarse (alpha, gamma) sweep shows a growth exponent of ~0.1 in J, which is
    small but not obviously zero -- and in a LOWER bound, growth is meaningful.
    This resolves it: if the increments shrink the norm is settling; if they hold,
    the two-graded pair has a problem the sup pair did not.
    """
    ys, sup_ys = [], []
    for J in Js:
        col = Collocation(J)
        M, rows = gauged_jacobian(col, col.anchor(), C_ANCHOR)
        A = np.linalg.inv(M)
        step = max(1, A.shape[0] // max_candidates)
        idx = np.arange(0, A.shape[0], step)
        dom = HolderNorm(col.theta, col.X, alpha, gamma)
        cod = GaugedNorm(col, rows, alpha + 1.0, gamma)
        S = np.sign(A[idx]) / cod.w[None, :]
        best = 0.0
        for g in S:
            ng = cod(g)
            if ng > 0:
                best = max(best, dom(A @ g) / ng)
        ys.append(best)
        # and the pure-sup norm on the SAME operator, for reference (v4's number)
        wcod = cod.w
        sup_ys.append(sup_op_norm(A, dom.w, wcod))
    return {"alpha": alpha, "gamma": gamma, "J": list(Js),
            "A_holder_family": ys, "A_sup_exact": sup_ys,
            "holder_growth_exponent": power_fit(Js, ys),
            "sup_growth_exponent": power_fit(Js, sup_ys),
            "holder_increments": [ys[i + 1] - ys[i] for i in range(len(ys) - 1)]}


def u3c_critical_direction(alpha=ALPHA_MAIN, gamma=GAMMA_MAIN,
                           Js=(125, 250, 500, 1000, 2000),
                           deltas=(0.0, 0.1, 0.25, 0.5, 1.0)):
    """Is the two-graded inverse bounded, and on which directions?

    The coarse sweep and the focused ladder disagreed, and the reason is the
    direction that dominates.  Feed the inverse residuals f_beta with
    beta = alpha + 1 + delta -- delta = 0 is EXACTLY the codomain's critical decay
    rate, delta > 0 is strictly inside it -- and watch the ratio against J.

    Prediction from the v3 resonance analysis: at the critical exponent the
    far-field inverse produces a LOG, not a power, so delta = 0 should creep up
    logarithmically while every delta > 0 saturates.  If so the fix is the same one
    v3 used for alpha: keep the residual class OPEN (decay strictly faster than
    critical), at a cost set by delta.
    """
    out = {d: [] for d in deltas}
    for J in Js:
        col = Collocation(J)
        M, rows = gauged_jacobian(col, col.anchor(), C_ANCHOR)
        A = np.linalg.inv(M)
        dom = HolderNorm(col.theta, col.X, alpha, gamma)
        cod = GaugedNorm(col, rows, alpha + 1.0, gamma)
        for d in deltas:
            g = np.empty(col.J)
            g[0] = 0.0
            g[1:] = (1.0 + col.X[rows] ** 2) ** (-0.5 * (alpha + 1.0 + d))
            ng = cod(g)
            out[d].append(dom(A @ g) / ng if ng > 0 else 0.0)
    rows_out = []
    for d in deltas:
        ys = out[d]
        rows_out.append({"delta": d, "J": list(Js), "ratio": ys,
                         "growth_exponent_in_J": power_fit(Js, ys),
                         "increments": [ys[i + 1] - ys[i] for i in range(len(ys) - 1)]})
    return {"alpha": alpha, "gamma": gamma, "rows": rows_out}


def u4_quadratic(J=1000, degrees=(8, 32, 128, 512)):
    col = Collocation(J)
    out = []
    for alpha in ALPHA_GRID:
        for gamma in GAMMA_GRID:
            dom = HolderNorm(col.theta, col.X, alpha, gamma)
            cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
            base = (1.0 + col.X ** 2) ** (-0.5 * alpha)

            def ratio(h):
                n = dom(h)
                return 0.0 if n <= 0 else cod(col.quadratic(h)) / n ** 2

            adv = []
            for m in degrees:
                p, _ = square_wave(col.theta, m)
                adv.append(ratio(base * p))
            smooth, arg = 0.0, None
            for b in (alpha, alpha + 0.5, 2.0, 3.0):
                r = ratio((1.0 + col.X ** 2) ** (-0.5 * b))
                if r > smooth:
                    smooth, arg = r, f"f_{b:g}"
            for k in (1, 2, 4):
                r = ratio(base * np.cos(k * col.theta))
                if r > smooth:
                    smooth, arg = r, f"f_a cos{k}"
            out.append({"alpha": alpha, "gamma": gamma, "degrees": list(degrees),
                        "C_Q_adversary": adv, "C_Q_adversary_growth": adv[-1] / adv[0],
                        "C_Q_smooth": smooth, "argmax": arg,
                        "C_Q": max(max(adv), smooth)})
    return out


def u5_budget(u3rows, u4rows):
    by = {(r["alpha"], r["gamma"]): r for r in u4rows}
    out = []
    for r in u3rows:
        key = (r["alpha"], r["gamma"])
        if key not in by:
            continue
        CQ = by[key]["C_Q"]
        Z2 = 2.0 * r["A_norm"] * CQ
        out.append({"alpha": r["alpha"], "gamma": r["gamma"],
                    "A_norm": r["A_norm"], "C_Q": CQ, "Z2": Z2,
                    "budget_ceiling": 1.0 / (4.0 * Z2)})
    best = max(out, key=lambda r: r["budget_ceiling"])
    # restrict to where the v4 adversary is actually defused (gamma >= 0.35): the
    # unrestricted argmax sits at gamma = 0.25, which U1/U4 show is still on the
    # wrong side of the transition.
    ok = [r for r in out if r["gamma"] >= 0.35]
    best_ok = max(ok, key=lambda r: r["budget_ceiling"]) if ok else None
    return {"rows": out, "best": best, "best_defused": best_ok,
            "defused_gamma_min": 0.35,
            "note": "Z2 built from a family-restricted ||A|| (a lower bound) and a "
                    "family-restricted C_Q (also a lower bound), so this Z2 is a "
                    "LOWER bound and the budget ceiling an UPPER bound on an upper "
                    "bound. It locates the optimum; it does not certify anything."}


def main():
    print("U1 defusal ...", flush=True)
    u1 = u1_defusal()
    print("U2 Holder constant of H ...", flush=True)
    u2 = u2_holder_H_constant()
    print("U3 inverse over (alpha, gamma) ...", flush=True)
    u3 = u3_inverse()
    print("U3b focused ladder ...", flush=True)
    u3b = u3b_focused_ladder()
    print("U3c critical direction ...", flush=True)
    u3c = u3c_critical_direction()
    print("U4 quadratic ...", flush=True)
    u4 = u4_quadratic()
    u5 = u5_budget(u3["rows"], u4)
    jerr, xmax = jacobian_identity_error(np.pi * (np.arange(4000) + 0.5) / 4000)

    data = {
        "meta": {
            "leg": "P2 Route-D v5 (the two-grading decay x smoothness space)",
            "tier": "Level-1 tooling + scoping (NOT a certificate)",
            "norm": "||h|| = sup (1+X^2)^{a/2}|h| + [h]_{gamma, weight (a-gamma)}",
            "reproduce": "python experiments/p2_route_d_v5_holder.py",
            "arithmetic": "plain float64 -- nothing interval-enclosed, nothing rigorous",
            "conformal_jacobian_error": jerr, "conformal_resolved_to_X": xmax,
            "open": "operator norms here are FAMILY-RESTRICTED lower bounds (the exact "
                    "induced norm between polyhedral norms is an LP); Z1 is not "
                    "bounded; nothing closes.",
        },
        "u1_defusal": u1,
        "u2_holder_H_constant": u2,
        "u3_inverse": u3,
        "u3b_focused_ladder": u3b,
        "u3c_critical_direction": u3c,
        "u4_quadratic": u4,
        "u5_budget": u5,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    # ---- console summary ---------------------------------------------------
    print("\nU1 the v4 adversary, in both norms (degrees "
          f"{u1[0]['degrees'][0]}..{u1[0]['degrees'][-1]}):")
    for r in u1:
        print(f"   gamma={r['gamma']:.2f}: sup ratio x{r['sup_growth']:.2f} (GROWS)"
              f"   Holder ratio x{r['holder_growth']:.2f}"
              f"   [{r['holder_ratio'][0]:.3f} -> {r['holder_ratio'][-1]:.3f}]")

    print("\nU2 the Holder constant of H vs gamma (should bowl):")
    for r in u2:
        print(f"   gamma={r['gamma']:.2f}: C_H = {r['C_H']:.3f}")
    bestg = min(u2, key=lambda r: r["C_H"])
    print(f"   -> minimized at gamma = {bestg['gamma']:.2f} (C_H = {bestg['C_H']:.3f})")

    print("\nU3 ||A|| over (alpha, gamma), family-restricted, at "
          f"J={u3['J_ladder'][-1]} (growth exponent in J in brackets):")
    print("   alpha \\ gamma  " + "  ".join(f"{g:>6.2f}" for g in GAMMA_GRID))
    for alpha in ALPHA_GRID:
        row = [r for r in u3["rows"] if r["alpha"] == alpha]
        print(f"   {alpha:>11.2f}  " + "  ".join(f"{r['A_norm']:>6.2f}" for r in row))
    print("   growth exponents in J:")
    for alpha in ALPHA_GRID:
        row = [r for r in u3["rows"] if r["alpha"] == alpha]
        print(f"   {alpha:>11.2f}  "
              + "  ".join(f"{r['growth_exponent_in_J']:>6.2f}" for r in row))

    print(f"\nU3b focused ladder at alpha={u3b['alpha']}, gamma={u3b['gamma']} "
          f"(J={u3b['J'][0]}..{u3b['J'][-1]}):")
    print("   Holder-pair (family): " + " ".join(f"{v:.3f}" for v in u3b["A_holder_family"])
          + f"   ~J^{u3b['holder_growth_exponent']:.3f}")
    print("   sup-pair (exact):     " + " ".join(f"{v:.3f}" for v in u3b["A_sup_exact"])
          + f"   ~J^{u3b['sup_growth_exponent']:.3f}")
    print("   Holder increments: "
          + " ".join(f"{v:+.3f}" for v in u3b["holder_increments"]))

    print(f"\nU3c the critical codomain direction (alpha={u3c['alpha']}, "
          f"gamma={u3c['gamma']}; residual f_(alpha+1+delta)):")
    print("   delta   " + "  ".join(f"J={J:<6d}" for J in u3c["rows"][0]["J"])
          + "  exponent")
    for r in u3c["rows"]:
        print(f"   {r['delta']:>5.2f}   "
              + "  ".join(f"{v:<8.3f}" for v in r["ratio"])
              + f"  {r['growth_exponent_in_J']:+.3f}")
    print("   -> delta = 0 is the codomain's critical rate: it CREEPS (a log, as the "
          "v3 resonance predicts); every delta > 0 saturates")

    print("\nU4 the quadratic constant (adversary growth over degree 8..512):")
    for alpha in (ALPHA_MAIN,):
        for r in [x for x in u4 if x["alpha"] == alpha]:
            print(f"   alpha={r['alpha']:.2f} gamma={r['gamma']:.2f}: "
                  f"adversary x{r['C_Q_adversary_growth']:.2f} "
                  f"({r['C_Q_adversary'][0]:.3f} -> {r['C_Q_adversary'][-1]:.3f}), "
                  f"smooth {r['C_Q_smooth']:.3f} ({r['argmax']}), C_Q={r['C_Q']:.3f}")

    b, bd = u5["best"], u5["best_defused"]
    print(f"\nU5 joint optimum (unrestricted): alpha = {b['alpha']:.2f}, gamma = "
          f"{b['gamma']:.2f}  (||A|| = {b['A_norm']:.2f}, C_Q = {b['C_Q']:.3f}, "
          f"Z2 = {b['Z2']:.2f}, budget ceiling {b['budget_ceiling']:.3e})")
    if bd is not None:
        print(f"   restricted to the DEFUSED region gamma >= "
              f"{u5['defused_gamma_min']}: alpha = {bd['alpha']:.2f}, gamma = "
              f"{bd['gamma']:.2f}  (||A|| = {bd['A_norm']:.2f}, C_Q = {bd['C_Q']:.3f}, "
              f"Z2 = {bd['Z2']:.2f}, budget ceiling {bd['budget_ceiling']:.3e})")
    print(f"[done] wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
