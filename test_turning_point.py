"""Gates for solver/turning_point.py -- the corrected mechanism behind v12's divergence.

  (1) THE CORRECTION ITSELF.  The INNER homogeneous mode vanishes like
      (X_c - X)^{+1/a}; v12's writeup said it blows up like the reciprocal, from a
      dropped sign.  The gate fits the exponent and checks the sign of the claim,
      so the error cannot come back.
  (2) THE ACTUAL OBSTRUCTION.  Outside X_c the same equation has a GROWING
      solution, ~ (log(X/X_c))^{1/a}.  Fitted against the prediction, which has no
      free constant.
  (3) THE INSTRUMENT IS CONVERGED.  Both fits are quadratures; refining the
      integration grid must not move them.
  (4) IT IS THE PROFILE'S OWN EXPONENT.  The far-field growth exponent tracks 1/a
      across a, not some fixed number -- the same 1/a as the profile's zero.
  (5) THE DIVERGENCE IS ATTRIBUTED, NOT ASSERTED.  With the domain sup restricted
      to a FIXED outer radius the norm grows far more slowly than the
      unrestricted one, and the extremal row's mass comes from codomain slots at
      X_c; the a = 0 control does neither.
  (6) THE CHEAP REPAIR IS DISQUALIFIED, AND FOR THE STATED REASON.  Restoring the
      speed as an unknown makes the SQUARE bordered system singular at a = 0
      (dilation is an exact symmetry there), and the overdetermined version's norm
      grows with J even at a = 0 -- so it adds kernel, not range.

Run: .venv/bin/python test_turning_point.py
"""

import numpy as np

from solver.collocation_newton import ACollocation
from solver.turning_point import (bordered_norm, graded_norm_by_radius,
                                  homogeneous_far_field, inner_mode_exponent,
                                  log_growth_exponent, solved_profile,
                                  source_of_the_row, square_bordered_smin)

ALPHA = 1.4


def test_1_inner_mode_vanishes():
    col, om, c = solved_profile(400, 0.3)
    p, Xc = inner_mode_exponent(col, om, c)
    assert p > 0, "the inner mode VANISHES at X_c; a negative exponent is v12's error"
    assert abs(p - 1.0 / 0.3) / (1.0 / 0.3) < 0.10, (p, 1 / 0.3)
    print("[ok] (1) inner homogeneous mode ~ (X_c-X)^%.3f at X_c=%.4f (predicted "
          "1/a = %.3f, and POSITIVE -- v12's writeup had the sign wrong)"
          % (p, Xc, 1 / 0.3))


def test_2_outer_mode_grows():
    col, om, c = solved_profile(400, 0.3)
    X, h, Xc = homogeneous_far_field(col, om, c)
    assert h[-1] > 1e3, h[-1]
    q = log_growth_exponent(X, h, Xc)
    assert abs(q - 1.0 / 0.3) / (1.0 / 0.3) < 0.05, (q, 1 / 0.3)
    print("[ok] (2) outer homogeneous mode GROWS to %.3e by X=1e8: exponent "
          "d log h / d log log(X/X_c) = %.4f vs the predicted 1/a = %.4f"
          % (h[-1], q, 1 / 0.3))


def test_3_quadrature_converged():
    col, om, c = solved_profile(400, 0.3)
    qs = []
    for n in (1001, 4001, 16001):
        X, h, Xc = homogeneous_far_field(col, om, c, n=n)
        qs.append(log_growth_exponent(X, h, Xc))
    spread = max(qs) - min(qs)
    p1, _ = inner_mode_exponent(col, om, c, n=1001)
    p2, _ = inner_mode_exponent(col, om, c, n=8001)
    assert spread < 2e-3, (qs, spread)
    assert abs(p1 - p2) < 2e-3, (p1, p2)
    print("[ok] (3) both fits are quadrature-converged: outer spread %.1e over a "
          "16x refinement, inner %.1e" % (spread, abs(p1 - p2)))


def test_4_tracks_one_over_a():
    out = []
    for a in (0.25, 0.3, 0.4):
        col, om, c = solved_profile(400, a)
        X, h, Xc = homogeneous_far_field(col, om, c)
        out.append((a, log_growth_exponent(X, h, Xc), 1.0 / a))
    for a, q, pred in out:
        assert abs(q - pred) / pred < 0.06, (a, q, pred)
    print("[ok] (4) the far-field exponent tracks the profile's own 1/a: "
          + ", ".join("a=%.2f -> %.3f (%.3f)" % r for r in out))


def test_5_attribution():
    rows = {}
    for a in (0.0, 0.3):
        col, om, c = solved_profile(400, a)
        rows[a] = graded_norm_by_radius(col, om, c, ALPHA)
    hot = rows[0.3]["by_cutoff"]
    cold = rows[0.0]["by_cutoff"]
    assert hot["inf"] > 30 * hot["20"], hot
    assert cold["inf"] < 2.0 * cold["20"], cold
    col, om, c = solved_profile(400, 0.3)
    src = source_of_the_row(col, om, c, ALPHA)
    assert src["near_Xc_fraction"] > 0.5, src
    print("[ok] (5) a=0.3: ||A|| by outer cutoff 20/50/200/inf = %.3g/%.3g/%.3g/"
          "%.3g and %.0f%% of the extremal row comes from within 10%% of X_c; "
          "the a=0 control is %.3g/%.3g/%.3g/%.3g"
          % (hot["20"], hot["50"], hot["200"], hot["inf"],
             100 * src["near_Xc_fraction"],
             cold["20"], cold["50"], cold["200"], cold["inf"]))


def test_6_speed_is_the_wrong_border():
    col = ACollocation(200, a=0.0)
    om = col.newton_gauged(c=0.5)["Omega"]
    smin, cond = square_bordered_smin(col, om, 0.5)
    assert cond > 1e12, (smin, cond)          # dilation symmetry => singular
    ns = [bordered_norm(*solved_profile(J, 0.0), ALPHA) for J in (200, 400)]
    assert ns[1] > 1.5 * ns[0], ns
    print("[ok] (6) restoring the speed adds KERNEL, not range: the square "
          "bordered system at a=0 has cond %.1e (smin %.1e), and the "
          "overdetermined version's norm grows %.3g -> %.3g over J=200->400 even "
          "at the anchor, where the plain system is flat" % (cond, smin, *ns))


if __name__ == "__main__":
    for t in (test_1_inner_mode_vanishes, test_2_outer_mode_grows,
              test_3_quadrature_converged, test_4_tracks_one_over_a,
              test_5_attribution, test_6_speed_is_the_wrong_border):
        t()
    print("\n6/6 gates passed.")
