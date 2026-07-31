"""Gates for solver/op_lower.py -- the lower bound on ||A||.

  (1) VALIDITY is structural: every candidate g gives ||A g||_X / ||g||_Y, which
      is a lower bound by definition.  What has to be checked is that the code
      computes that ratio for a vector that is really IN the space -- i.e. that
      the norms used are the project's and the gauge slot is handled -- and that
      the reported maximum is attained by a member of the family it names.
  (2) IT BEATS THE BASELINE by a large factor, at three J.
  (3) IT NEVER EXCEEDS THE UPPER BOUND (the bracket is a bracket).
  (4) THE WINNER IS A WIDE FAR-FIELD SHAPE (a broad bump or a step, never an
      oscillatory member), and the top few are reported so a reader can see what
      the extremizer actually looks like.
  (5) J-STABILITY: the lower bound does not fall apart as J grows (the sign
      patterns do -- they get worse with J, which is why they were misleading).
  (6) THE ASCENT is honest: it is run, and its (small) gain is reported rather
      than folded silently into the headline.

Run: .venv/bin/python test_op_lower.py
"""

import numpy as np

from solver.decay_collocation import Collocation, C_ANCHOR
from solver.holder_norms import HolderNorm
from solver.nk_bounds import sup_part_upper
from solver.nk_seminorm import seminorm_closure
from solver.hilbert_pointwise import pointwise_curves
from solver.op_lower import (
    ascend, best_lower, family_lower, sign_pattern_lower, smooth_family,
)

ALPHA, GAMMA = 1.5, 0.5


def setup(J, alpha=ALPHA, gamma=GAMMA):
    col = Collocation(J)
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    A = np.linalg.inv(M)
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
    cod.w[0] = 1.0
    return col, A, dom, cod


def test_1_validity():
    col, A, dom, cod = setup(300)
    r = family_lower(A, dom, cod, col.theta, n_centre=12, n_step=12)
    hit = None
    for name, g in smooth_family(col.theta, cod.w, n_centre=12, n_step=12):
        if name == r["argmax"]:
            hit = g.copy()
            break
    assert hit is not None, r["argmax"]
    hit[0] = 0.0
    ratio = dom(A @ hit) / cod(hit)
    assert abs(ratio - r["lower"]) < 1e-12, (ratio, r["lower"])
    assert np.isfinite(cod(hit)) and cod(hit) > 0
    print("[ok] (1) the reported maximum %.4f is reproduced exactly by the named "
          "family member (%s), whose codomain norm is finite"
          % (r["lower"], r["argmax"]))


def test_2_beats_baseline():
    gains = []
    for J in (200, 300, 400):
        col, A, dom, cod = setup(J)
        b = sign_pattern_lower(A, dom, cod)["lower"]
        f = family_lower(A, dom, cod, col.theta, n_centre=20, n_step=24)["lower"]
        gains.append(f / b)
    assert min(gains) > 2.0, gains
    print("[ok] (2) beats the sign-pattern baseline by %.1f-%.1fx over J = "
          "200..400" % (min(gains), max(gains)))


def test_3_inside_the_bracket():
    col, A, dom, cod = setup(400)
    lo = family_lower(A, dom, cod, col.theta, n_centre=20, n_step=24)["lower"]
    C_sup = sup_part_upper(A, dom.w, cod.w, cod.pair)
    cv = pointwise_curves(ALPHA, GAMMA, rho=6.0, n_theta=90, n_quad=300)
    up = seminorm_closure(ALPHA, GAMMA, C_sup, curves=cv)["A_upper"]
    assert lo < up, (lo, up)
    print("[ok] (3) %.3f <= ||A|| <= %.2f -- a bracket of %.0fx (the sign "
          "patterns made it %.0fx)"
          % (lo, up, up / lo,
             up / sign_pattern_lower(A, dom, cod)["lower"]))


def test_4_the_winner():
    col, A, dom, cod = setup(400)
    scored = []
    for name, g in smooth_family(col.theta, cod.w, n_centre=20, n_step=24):
        g = g.copy()
        g[0] = 0.0
        n = cod(g)
        if n > 0:
            scored.append((dom(A @ g) / n, name))
    scored.sort(reverse=True)
    top = scored[:5]
    # the winner is always a WIDE, FAR-FIELD-supported shape (a broad bump or a
    # step) -- never one of the oscillatory members.  Which of bump/step wins
    # depends on the sweep's resolution, and they are within a few percent of
    # each other, so the gate checks the SHAPE CLASS rather than the label.
    assert all(n.startswith(("bump", "step")) for _, n in top), top
    def centre(name):
        return float(name.split("%")[0].replace("bump", "").replace("step", "")
                     .split("/")[0])
    assert centre(top[0][1]) > 2.0, top
    print("[ok] (4) the extremizer is a wide FAR-FIELD shape (centre theta = "
          "%.2f, i.e. X ~ %.0f); top five: %s"
          % (centre(top[0][1]), np.tan(0.5 * centre(top[0][1])),
             ", ".join("%s %.3f" % (n, v) for v, n in top)))


def test_5_J_stability():
    lo, base = [], []
    for J in (200, 400, 800):
        col, A, dom, cod = setup(J)
        lo.append(family_lower(A, dom, cod, col.theta, n_centre=16,
                               n_step=20)["lower"])
        base.append(sign_pattern_lower(A, dom, cod)["lower"])
    lo, base = np.array(lo), np.array(base)
    assert np.ptp(lo) / lo.mean() < 0.2, lo
    assert base[-1] < base[0], base            # the baseline DEGRADES with J
    print("[ok] (5) stable in J (%.3f, %.3f, %.3f over J = 200/400/800) while "
          "the sign-pattern baseline degrades (%.3f -> %.3f)"
          % (lo[0], lo[1], lo[2], base[0], base[-1]))


def test_6_ascent_reported():
    col, A, dom, cod = setup(300)
    r = best_lower(A, dom, cod, col.theta, ascent_iters=400, n_centre=12,
                   n_step=12)
    assert r["lower"] >= r["smooth_family"] - 1e-12
    assert r["lower"] >= r["sign_patterns"]
    print("[ok] (6) ascent runs and is reported: family %.4f -> after ascent "
          "%.4f (gain %.3fx); headline %.4f"
          % (r["smooth_family"], r["after_ascent"], r["ascent_gain"], r["lower"]))


if __name__ == "__main__":
    test_1_validity()
    test_2_beats_baseline()
    test_3_inside_the_bracket()
    test_4_the_winner()
    test_5_J_stability()
    test_6_ascent_reported()
    print("\nALL OP-LOWER TESTS PASSED")
