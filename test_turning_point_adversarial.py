"""Leg 118 / Route-TPA -- adversarial gates for solver/turning_point.py.

Banked as a permanent regression battery.  solver/turning_point.py is READ-ONLY
under leg 118: these gates record what the module DOES, and the ones marked
CHARACTERIZATION record behaviour the leg judged wrong and ESCALATED rather than
patched.  A later repair leg is expected to flip those, and the assertion messages
say so explicitly, so the flip cannot be mistaken for a regression.

  (A) THE POSITIVE CONTROL, AND IT CAN COME OUT DIFFERENTLY (lesson 90).
      At a = 0 the effective speed E = c + 0*U is the positive constant c, so it
      never crosses zero and X_c DOES NOT EXIST.  homogeneous_far_field carries an
      isfinite guard and RAISES on exactly this input.  That is the proof the
      module can flag it, and it is what makes (B) an omission rather than a
      design decision.
  (B) CHARACTERIZATION -- the same input, the unguarded consumer.
      source_of_the_row computes X_c at line 187 with no guard and then classifies
      "near X_c" as |X_j - X_c| <= 0.1*X_c.  At X_c = inf that is inf <= inf, which
      is True in IEEE-754, so every node is classified as near a turning point that
      does not exist, and a finite plausible fraction comes back.
  (C) CHARACTERIZATION -- the INVERSION, which is what makes (B) dangerous.
      The fabricated a = 0 fraction is LARGER than the honest fraction at a = 0.2,
      where the turning point is real: ranked by the module's own headline number,
      the profile with no turning point looks more turning-point-driven than the
      one that has one, and it is the only one of the two that passes the module's
      own >0.5 criterion.
  (D) inner_mode_exponent, the third consumer, FLAGS -- it raises rather than
      returning a number.  Recorded so a future repair does not silently lose it.
  (E) log_growth_exponent takes X_c from the CALLER and checks nothing.
  (F) Poisoned profiles do not come back as finite classifications.
  (G) `drop` is an unguarded public parameter of gauged_matrix.

Run: .venv/bin/python test_turning_point_adversarial.py
"""

import warnings

import numpy as np

from solver.collocation_newton import critical_radius, effective_speed
from solver.turning_point import (gauged_matrix, homogeneous_far_field,
                                  inner_mode_exponent, log_growth_exponent,
                                  solved_profile, source_of_the_row)

ALPHA = 1.4

# Quoted from test_turning_point.py line 96 -- `assert src["near_Xc_fraction"] > 0.5`.
# This leg did not choose it; it is the module's own attribution criterion.
MODULE_ATTRIBUTION_THRESHOLD = 0.5

ESCALATED = ("ESCALATED by leg 118, not patched. If a repair leg has since added the "
             "isfinite guard at solver/turning_point.py:187, this CHARACTERIZATION "
             "gate is expected to fail and should be re-pointed at the new "
             "behaviour -- it is not a regression.")


def _xc(col, om, c):
    return critical_radius(col.X, effective_speed(col.X, col.V @ om, c, col.a))


def test_A_the_guarded_site_flags_and_the_control_is_real():
    """a = 0: no turning point exists, and the guarded consumer says so."""
    col, om, c = solved_profile(120, 0.0)
    E = effective_speed(col.X, col.V @ om, c, col.a)
    assert np.all(E > 0), "a=0 control is only meaningful if E never crosses zero"
    assert int((np.diff(np.sign(E)) != 0).sum()) == 0, "E must not change sign"
    Xc = _xc(col, om, c)
    assert not np.isfinite(Xc), Xc

    raised = None
    try:
        homogeneous_far_field(col, om, c)
    except ValueError as e:
        raised = str(e)
    assert raised is not None and "no turning point" in raised, raised

    # The control that CAN come out differently: at a > 0 the SAME call succeeds.
    col2, om2, c2 = solved_profile(120, 0.3)
    assert np.isfinite(_xc(col2, om2, c2))
    X, h, Xc2 = homogeneous_far_field(col2, om2, c2, n=401)
    assert np.isfinite(Xc2) and h[-1] > 1.0, (Xc2, h[-1])
    print("[ok] (A) a=0: E in [%.4f, %.4f], 0 sign changes, X_c = %s, and the "
          "GUARDED consumer raises ValueError('%s'); the same call at a=0.3 "
          "succeeds with X_c = %.4f -- the control is real"
          % (E.min(), E.max(), Xc, raised.split(":")[0], Xc2))


def test_B_CHARACTERIZATION_unguarded_consumer_invents_an_attribution():
    """The same a = 0 input the guarded site rejects, through the unguarded one."""
    col, om, c = solved_profile(120, 0.0)
    Xc = _xc(col, om, c)
    assert not np.isfinite(Xc)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = source_of_the_row(col, om, c, ALPHA)

    frac = out["near_Xc_fraction"]
    assert np.isfinite(frac), (frac, "expected a finite fabricated fraction")
    assert out["Xc"] == float("inf"), out["Xc"]
    assert len(w) == 0, ("the module warns about nothing here; " + ESCALATED)
    assert frac > MODULE_ATTRIBUTION_THRESHOLD, (
        "leg 118 measured %.6f > %.2f, i.e. the fabricated attribution PASSES the "
        "module's own criterion. %s" % (frac, MODULE_ATTRIBUTION_THRESHOLD, ESCALATED))

    # The mechanism, isolated: it is inf <= inf, not a near-miss.
    assert (np.abs(1.0 - Xc) <= 0.1 * Xc), "IEEE-754: inf <= inf is True"
    print("[ok] (B) CHARACTERIZATION: with X_c = inf (no turning point), "
          "source_of_the_row returns near_Xc_fraction = %.6f, finite, no warning, "
          "and ABOVE the module's own >%.1f attribution criterion. Mechanism: "
          "|X_j - inf| <= 0.1*inf is inf <= inf, True for every node."
          % (frac, MODULE_ATTRIBUTION_THRESHOLD))


def test_C_CHARACTERIZATION_the_inversion():
    """The sharp form: NO turning point scores HIGHER than a real turning point.

    This is what makes the fabricated number dangerous rather than merely wrong.
    At a = 0 there is no X_c at all and the module returns ~0.72, passing its own
    >0.5 attribution criterion. At a = 0.2 there IS a turning point, at a finite
    X_c the module locates correctly, and the honest fraction is ~0.19 -- which
    FAILS the same criterion. Ranked by the module's own headline number, the
    profile with no turning point looks more turning-point-driven than the one
    that has one.
    """
    col0, om0, c0 = solved_profile(120, 0.0)
    col2, om2, c2 = solved_profile(120, 0.2)
    Xc0, Xc2 = _xc(col0, om0, c0), _xc(col2, om2, c2)
    assert not np.isfinite(Xc0), Xc0
    assert np.isfinite(Xc2), ("a=0.2 must have a real turning point for this "
                              "comparison to mean anything")

    f0 = source_of_the_row(col0, om0, c0, ALPHA)["near_Xc_fraction"]
    f2 = source_of_the_row(col2, om2, c2, ALPHA)["near_Xc_fraction"]
    assert np.isfinite(f0) and np.isfinite(f2), (f0, f2)
    assert f0 > f2, (
        "the inversion is the finding; if a repair made the no-X_c case return "
        "nan this assertion is expected to fail. %s" % ESCALATED)
    assert f0 > MODULE_ATTRIBUTION_THRESHOLD >= f2, (f0, f2, ESCALATED)
    print("[ok] (C) CHARACTERIZATION -- THE INVERSION: a=0 (X_c does NOT exist) "
          "scores %.6f and PASSES the module's own >%.1f criterion; a=0.2 (real "
          "X_c = %.4f) scores %.6f and FAILS it. The fabricated attribution is "
          "%.2fx the honest one."
          % (f0, MODULE_ATTRIBUTION_THRESHOLD, Xc2, f2, f0 / f2))


def test_D_third_consumer_flags():
    """inner_mode_exponent is unguarded too, but its degeneracy is loud."""
    col, om, c = solved_profile(120, 0.0)
    raised = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            inner_mode_exponent(col, om, c, n=401)
    except Exception as e:                                       # noqa: BLE001
        raised = type(e).__name__
    assert raised is not None, (
        "inner_mode_exponent returned a value with X_c = inf; if a repair made it "
        "return nan cleanly that is an improvement -- re-point this gate")
    print("[ok] (D) the third unguarded consumer inner_mode_exponent does NOT "
          "invent a number at X_c = inf: it raises %s. The gap is confined to "
          "source_of_the_row." % raised)


def test_E_log_growth_exponent_trusts_the_caller_s_Xc():
    col, om, c = solved_profile(120, 0.3)
    X, h, Xc = homogeneous_far_field(col, om, c, n=1001)
    true_q = log_growth_exponent(X, h, Xc)
    assert np.isfinite(true_q) and true_q > 0, true_q
    moved = {}
    for f in (0.1, 0.5, 2.0, 10.0):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            moved[f] = log_growth_exponent(X, h, Xc * f)
    finite = {f: q for f, q in moved.items() if np.isfinite(q)}
    assert finite, "expected at least one wrong-Xc call to return a finite number"
    spread = max(abs(q - true_q) for q in finite.values())
    assert spread > 1e-6, (
        "if a wrong X_c cannot move the exponent at all, this gate is not a "
        "control (lesson 90) -- check the realization before trusting it")
    print("[ok] (E) log_growth_exponent accepts any caller X_c: true exponent "
          "%.4f, and wrong X_c moves it by up to %.4f (%.1f%%) with no complaint "
          "-- %s" % (true_q, spread, 100 * spread / abs(true_q),
                     ", ".join("x%g->%.4f" % (f, q) for f, q in sorted(moved.items()))))


def test_F_poisoned_profiles_do_not_return_finite_classifications():
    col, om0, c = solved_profile(120, 0.3)
    bad = 0
    total = 0
    for val in (float("nan"), float("inf")):
        for idx in (0, 60, 119):
            om = np.array(om0, float, copy=True)
            om[idx] = val
            for fn in (lambda o: source_of_the_row(col, o, c, ALPHA),
                       lambda o: inner_mode_exponent(col, o, c, n=401),
                       lambda o: homogeneous_far_field(col, o, c, n=401)):
                total += 1
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        r = fn(om)
                except Exception:                                # noqa: BLE001
                    continue                                     # flagged: good
                flat = np.asarray([x for x in (r.values() if isinstance(r, dict)
                                               else np.atleast_1d(r))
                                   if isinstance(x, (int, float, np.floating))],
                                  dtype=float)
                if flat.size and np.all(np.isfinite(flat)):
                    bad += 1
    assert bad == 0, ("%d of %d poisoned-profile calls returned an all-finite "
                      "classification" % (bad, total))
    print("[ok] (F) %d poisoned-profile calls across three consumers: 0 returned "
          "an all-finite classification -- NaN/inf in the profile propagates or "
          "raises, it is never absorbed." % total)


def test_G_drop_out_of_range_HELD():
    """A declared hazard that did NOT fire, banked so it stays that way.

    `drop` has no explicit range check, but `keep` then has the wrong length and
    the assignment `M[1:, :] = col.jacobian_a(...)[keep, :]` fails on shape.  The
    guard is incidental rather than designed, which is exactly why it is worth a
    regression gate: a refactor could remove it without anyone noticing.
    """
    col, om, c = solved_profile(120, 0.3)
    ref, _ = gauged_matrix(col, om, c, drop=0)
    raised, silent = [], []
    for d in (120, 125, -1, -120, 10 ** 6):
        try:
            M, _ = gauged_matrix(col, om, c, drop=d)
        except Exception as e:                                   # noqa: BLE001
            raised.append((d, type(e).__name__))
            continue
        silent.append((d, list(M.shape)))
    assert not silent, ("out-of-range drop returned a matrix instead of raising: "
                        "%s -- the incidental shape guard has been lost" % silent)
    assert len(raised) == 5, raised
    # In-range values must still differ from each other, or the gate is vacuous.
    m1, _ = gauged_matrix(col, om, c, drop=1)
    assert not np.allclose(m1, ref), "drop=1 and drop=0 must give different matrices"
    print("[ok] (G) HELD: all 5 out-of-range `drop` values raise (%s); in-range "
          "drop=0 and drop=1 give genuinely different matrices, so the gate is "
          "not vacuous." % ", ".join("%d->%s" % r for r in raised))


def test_H_log_growth_exponent_absorbs_poison_outside_its_fit_window():
    """tail=0.1: only the outer 10% of the array is fitted. The rest is ignored.

    A NaN anywhere in the first 90% changes the returned exponent by EXACTLY
    zero -- the module reports a clean classification on a corrupted array. The
    positive control is a NaN inside the window, which must destroy it.
    """
    col, om, c = solved_profile(120, 0.3)
    X, h, Xc = homogeneous_far_field(col, om, c, n=1001)
    clean = log_growth_exponent(X, h, Xc)
    assert np.isfinite(clean)

    outside = np.array(h, float, copy=True)
    outside[len(h) // 2] = float("nan")                 # index 500 of 1001: 50%
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        q_out = log_growth_exponent(X, outside, Xc)
    assert np.isfinite(q_out), q_out
    assert q_out == clean, ("expected EXACT absorption, got a shift of %.3e"
                            % abs(q_out - clean))

    inside = np.array(h, float, copy=True)
    inside[int(0.97 * len(h))] = float("nan")           # inside the fitted tail
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        q_in = log_growth_exponent(X, inside, Xc)
    assert not np.isfinite(q_in), (
        "the positive control failed: a NaN INSIDE the fit window must not "
        "produce a finite exponent, or this gate is not a control (lesson 90)")
    print("[ok] (H) log_growth_exponent fits only the outer 10%%: a NaN at 50%% "
          "of the array shifts the exponent by EXACTLY 0.0 (%.10f both ways), "
          "while the control NaN at 97%% gives %s. Poison outside the window is "
          "absorbed, not detected." % (clean, q_in))


if __name__ == "__main__":
    np.seterr(all="ignore")
    tests = (test_A_the_guarded_site_flags_and_the_control_is_real,
             test_B_CHARACTERIZATION_unguarded_consumer_invents_an_attribution,
             test_C_CHARACTERIZATION_the_inversion,
             test_D_third_consumer_flags,
             test_E_log_growth_exponent_trusts_the_caller_s_Xc,
             test_F_poisoned_profiles_do_not_return_finite_classifications,
             test_G_drop_out_of_range_HELD,
             test_H_log_growth_exponent_absorbs_poison_outside_its_fit_window)
    for t in tests:
        t()
    print("\n%d/%d adversarial gates passed." % (len(tests), len(tests)))
