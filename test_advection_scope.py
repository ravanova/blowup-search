"""Known-answer tests for the a-scope of the Route-D bound programme.

The claim under test is a NEGATIVE about scope -- that the space eleven legs
built cannot carry the advection term for any a != 0 -- so each gate pins a
quantitative prediction rather than an inequality, and each has an a = 0 control
where the effect must vanish identically.

Pre-committed predicates:
  (1) THE LOG LAW: the fitted dU/d log X matches M_window/pi (M = int Omega over
      the fit window) to <= 1%, at a = 0, 0.3 and 0.5, on an independently
      integrated mass. The WINDOWED mass is the right predictor: dU/dlogX =
      X H(Omega) is an identity, and what (U) claims is that it tends to M/pi --
      which the coarse outermost decade of the sinh grid corrupts at a = 0.5.
  (2) THE SPLIT IS REAL: in the TWO-SCALE grading the transport piece a U h_X
      GROWS like log X at the predicted rate a|M|alpha/pi, while the stretch piece
      a (V H h) Omega_X is NOT MEASURABLE out there at all. The discriminator is
      reproducibility: transport is built from U (fixed by the profile's core
      mass) and an analytic h, so it repeats under refinement; stretch carries
      Omega_X, whose far field for a != 0 sits at the discretization noise floor
      (the tail does not converge -- its sign flips between grids), so it does
      not. Only the reproducible half is quoted as a result.
  (3) THE a = 0 CONTROL: both pieces are identically zero at a = 0, so the
      divergence is the advection term and nothing else.
  (4) THE FIX: in the ONE-SCALE grading (one power weaker) the transport piece
      DECAYS to zero instead of growing -- for the same profile, same h, same
      grid. One power is exactly enough.
  (5) THE STAGNATION POINT IS REAL: c + a U changes sign at an X* that is stable
      to 5% under refinement of BOTH the node count and the domain radius, and
      there is no crossing at a = 0.
  (6) SANITY OF THE INPUTS: the Newton profiles used here are converged, and the
      d/dX matrix is the one that already carries 1/X_rho (dividing again would
      cost exactly one power of X and hide the whole effect -- it did, once).

Run: python test_advection_scope.py    (no scipy; ~4 min)
"""

import numpy as np

from solver.profile_newton import TwoScaleNewton, derivative_matrix
from solver.advection_scope import (
    profile_mass, velocity, velocity_log_rate, advection_split,
    grading_comparison, stagnation_point,
)

ALPHA = 1.4          # the operating point of v8-v10


def _solved(a, n=2401, rho_max=12.0):
    nw = TwoScaleNewton(a=a, n=n, rho_max=rho_max)
    r = nw.solve()
    return nw, r["Omega"], r["c"], r


def test_log_law():
    """(1) dU/dlogX == M/pi."""
    out = []
    for a in (0.0, 0.3, 0.5):
        nw, om, c, r = _solved(a)
        d = velocity_log_rate(nw.fam, om)
        rel = abs(d["measured"] - d["predicted"]) / abs(d["predicted"])
        assert rel < 0.01, f"a={a}: measured {d['measured']:.4f} vs {d['predicted']:.4f}"
        out.append((a, d["measured"], d["predicted"]))
    print("[ok] (1) U ~ (M/pi) log X: "
          + "; ".join(f"a={a}: {m:+.4f} vs {p:+.4f}" for a, m, p in out))


def test_split_is_real():
    """(2) transport diverges at the predicted rate AND reproduces across grids;
    the stretch piece does neither, because it carries Omega_X."""
    rows = []
    for a in (0.3, 0.5):
        got = {}
        for n, rho_max in ((2401, 12.0), (3601, 12.0)):
            nw, om, c, _ = _solved(a, n=n, rho_max=rho_max)
            D = derivative_matrix(nw.fam)
            got[n] = advection_split(nw.fam, om, a, ALPHA, D, grading="two_scale")
        s = got[2401]
        assert s["transport_log_rate"] > 0.2, \
            f"a={a}: transport must diverge, got {s['transport_log_rate']:.4f}"
        # the predicted rate is asymptotic; gate the ORDER, not the digits
        assert 0.4 < s["transport_log_rate"] / s["transport_predicted_rate"] < 1.6, \
            (f"a={a}: rate {s['transport_log_rate']:.4f} vs predicted "
             f"{s['transport_predicted_rate']:.4f}")

        # WHICH HALF OF THIS MEASUREMENT IS REAL.  The transport piece is built
        # from U (set by the profile's CORE mass) and an analytic h, so it must
        # reproduce under refinement.  The stretch piece carries Omega_X, and for
        # a != 0 the profile has collapsed to the far-field discretization noise
        # floor by X ~ 10 -- that tail does not converge, its sign flips between
        # grids -- so the stretch piece is amplified noise and must NOT be quoted.
        def spread(key):                                          # noqa: E306
            v = [got[n][key][1e3] for n in got]
            return abs(v[0] - v[1]) / max(abs(v[0]), abs(v[1]), 1e-300)
        st, ss = spread("transport_at"), spread("stretch_at")
        assert st < 0.10, f"a={a}: transport must reproduce, spread {st:.3f}"
        assert ss > 3 * st, \
            (f"a={a}: the stretch piece should be the unreproducible one "
             f"(transport {st:.3f} vs stretch {ss:.3f})")
        rows.append((a, s["transport_log_rate"], s["transport_predicted_rate"], st, ss))
    print("[ok] (2) two-scale split: "
          + "; ".join(f"a={a}: transport {t:+.3f} (pred {p:+.3f}), grid-spread "
                      f"{st:.1%} vs stretch {ss:.0%}" for a, t, p, st, ss in rows))


def test_zero_a_control():
    """(3) at a = 0 both pieces vanish identically."""
    nw, om, c, _ = _solved(0.0)
    D = derivative_matrix(nw.fam)
    s = advection_split(nw.fam, om, 0.0, ALPHA, D)
    assert np.max(np.abs(s["transport"])) == 0.0
    assert np.max(np.abs(s["stretch"])) == 0.0
    assert stagnation_point(nw.fam, om, c, 0.0) is None, "no crossing at a = 0"
    print("[ok] (3) a = 0 control: both advection pieces identically 0, "
          "and c_eff never changes sign")


def test_one_scale_fix():
    """(4) the one-scale grading absorbs the log."""
    rows = []
    for a in (0.3, 0.5):
        nw, om, c, _ = _solved(a)
        D = derivative_matrix(nw.fam)
        g = grading_comparison(nw.fam, om, a, ALPHA, D)
        two, one = g["two_scale"], g["one_scale"]
        assert two["transport_log_rate"] > 0.2, "two-scale must diverge"
        assert one["transport_log_rate"] < 0.0, \
            f"one-scale must decay, got {one['transport_log_rate']:.4f}"
        far_two = two["transport_at"][1e4]
        far_one = one["transport_at"][1e4]
        assert far_one < 0.01 * far_two, \
            f"one-scale far field {far_one:.3e} vs two-scale {far_two:.3e}"
        rows.append((a, two["transport_log_rate"], one["transport_log_rate"],
                     far_two, far_one))
    print("[ok] (4) one-scale grading fixes it: "
          + "; ".join(f"a={a}: rate {t:+.3f} -> {o:+.3f}, at X=1e4 {ft:.2f} -> {fo:.1e}"
                      for a, t, o, ft, fo in rows))


def test_stagnation_point_is_real():
    """(5) X* is grid-independent under BOTH refinements."""
    rows = []
    for a in (0.3, 0.5):
        vals = []
        for n, rho_max in ((1201, 10.0), (2401, 12.0), (2401, 14.0)):
            nw, om, c, _ = _solved(a, n=n, rho_max=rho_max)
            vals.append(stagnation_point(nw.fam, om, c, a))
        vals = np.array(vals, dtype=float)
        spread = float(vals.max() - vals.min()) / float(vals.mean())
        assert np.all(vals > 0), f"a={a}: X* must be positive, got {vals}"
        assert spread < 0.05, f"a={a}: X* spread {spread:.3f} over refinements {vals}"
        rows.append((a, float(vals.mean()), spread))
    assert rows[1][1] < rows[0][1], "X* should move inward as a grows"
    print("[ok] (5) stagnation point: "
          + "; ".join(f"a={a}: X* = {x:.2f} (spread {s:.1%} over 3 grids)"
                      for a, x, s in rows))


def test_input_sanity():
    """(6) the profiles are converged and d/dX is not double-counted."""
    nw, om, c, r = _solved(0.3)
    assert r["converged"] and r["relres"] < 1e-10, f"input profile: {r['relres']:.2e}"
    D = derivative_matrix(nw.fam)
    X = nw.fam.X
    # d/dX of a known function: d/dX (1+X^2)^{-1} = -2X/(1+X^2)^2
    f = 1.0 / (1.0 + X ** 2)
    exact = -2.0 * X / (1.0 + X ** 2) ** 2
    m = np.abs(X) < 50.0
    err = float(np.abs((D @ f) - exact)[m].max() / np.abs(exact[m]).max())
    assert err < 1e-6, f"D must be d/dX already (rel err {err:.2e})"
    print(f"[ok] (6) inputs sane: relres {r['relres']:.2e}, "
          f"d/dX matches the exact derivative to {err:.1e} "
          f"(it already carries 1/X_rho)")


if __name__ == "__main__":
    test_log_law()
    test_split_is_real()
    test_zero_a_control()
    test_one_scale_fix()
    test_stagnation_point_is_real()
    test_input_sanity()
    print("\nALL ADVECTION-SCOPE TESTS PASSED")
