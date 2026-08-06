"""Adversarial battery for solver/rescaled_spectrum.py (leg 203, Route-RSA).

WHY THIS FILE EXISTS, ALONGSIDE `test_rescaled_spectrum.py`.  The dedicated file asks each
piece of the module a question it can fail on its own terms -- an exact anchor, a closed-form
operator identity, the structural pair, the analytic spectrum -- on VALID input.  What it does
not do, and was never meant to do, is feed the module DEGENERATE, POISONED OR BOUNDARY input
and ask whether the wrong answer comes back silently.  Leg 203 does that.

THE GATE (DIRECTION.md, leg 203), answered YES:

    Under adversarial and degenerate inputs, does solver/rescaled_spectrum.py ever silently
    return a wrong value rather than reject or visibly propagate the defect?

READ THIS BEFORE CHANGING ANYTHING HERE.  Several checks below PIN CURRENT, DEFECTIVE
BEHAVIOUR.  That is deliberate, and it is legs 66 and 120's precedent: a leg whose territory is
read-only on `solver/` reports defects and pins them rather than fixing them silently, so the
defect cannot drift unnoticed and so the repair has an exact target.  **Every such check is
marked `PIN:` in its docstring and states what the CORRECT behaviour would be.  When the repair
lands, these checks WILL START FAILING -- that is the intended signal, not a regression.**
Update the pin then, in the same commit as the repair.

THIS LEG EDITED NO SOLVER FILE, under either gate branch.

THE EIGHT FINDINGS PINNED HERE (magnitudes measured by
experiments/p2_route_rsa_v1_adversarial.py, banked in
writeup/data/p2_route_rsa_v1_adversarial.json):

  R1  `converged_spectrum` HAS NO GUARD ON `K_fine` VS `K_coarse`.  The module's own line 116
      is the specification: "the discrete eigenvalues are the ones that stop moving under
      refinement, and the continuum is the part that never does."  At K_fine == K_coarse
      nothing is refined, so nothing can move, so EVERYTHING is kept.
      MEASURED at a = 0, where the analytic spectrum is exactly {0, -1}: n_kept goes from 2 to
      the full K (24/24, 32/32, 48/48 -- 24x at K = 48), every match distance is IDENTICALLY
      0.0, and the largest retained eigenvalue is a conjugate pair at +-40.4623i -- a purely
      imaginary pair, i.e. exactly the Hopf-crossing signature this module exists to rule out.
      CONTROL: K_fine < K_coarse (a COARSER "refinement") still returns 2, so the trap is
      EQUALITY specifically and the filter is not simply broken.

  R2  `spectrum` AND `converged_spectrum` DISCARD `newton`'s `converged` FLAG.  `newton`
      honours test 7 and returns it; `spectrum` then does
      `flow, out = continuation(...)` / `eigvals(flow.generator(out["b"]))` without ever
      reading it, and `converged_spectrum`'s `kept` array -- documented as "the
      grid-independent part of the spectrum" -- carries no convergence information at all.
      MEASURED at a = 0 against the EXACT spectrum {0, -1}, with the failure planted by
      capping max_iter: the worst silently-accepted iterate puts the amplitude eigenvalue
      2.632e-01 away from the exact -1 and places 44 eigenvalues in the RIGHT half plane
      (max Re = +0.3437) where the exact spectrum has none.
      THIS IS THE ONE FINDING THAT IS NOT LATENT -- see the severity note below.

  R3  `continuation` SILENTLY SKIPS THE CONTINUATION.  It builds
      `np.arange(0.0, a_target + 1e-12, da)`, which is EMPTY when `da`'s sign does not match
      `a_target`'s; the size-0 fallback appends `a_target` alone, so a FOLLOWED branch becomes
      a single cold solve from the anchor -- against the module's own line 315, "Continuation
      is the honest test for a branch: it FOLLOWS the object rather than searching for it."
      MEASURED at K = 48: at a = +0.50 the followed branch gives alpha = +3.00384222 and the
      silently-skipped path gives alpha = -0.98782818, |delta alpha| = 3.991670 -- a SIGN
      change in the far-field decay exponent.  At a = +0.30 the same defect moves alpha by
      only 5.21e-04, because a cold solve there still lands on the same branch: the defect is
      STRUCTURAL and its numerical size depends on how far the cold solve drifts.
      `da = 0.0` raises ZeroDivisionError -- a VISIBLE rejection, and a pass.

  R4  `continuum_defect` HAS NO ADMISSIBILITY CONTENT.  The docstring's claim is that the
      closed form is admissible EXACTLY on -1 < Re lambda < 1, but
      s = (w-1)^(1-l)(w+1)^(1+l) solves the homogeneous ODE for EVERY complex l --
      admissibility is a BOUNDARY condition -- and this function measures only the ODE
      residual.  It also drops the -s(w=1)(1+w) term on the stated grounds that
      "s(w=1) = 0 for Re lambda < 1", which is false outside the strip.
      MEASURED over 20 lambda: worst defect inside the strip 2.642e-06, worst outside
      3.734e-04, and NOTHING IS REJECTED -- the 2.2 decades between them track np.gradient's
      truncation error with |lambda| (lambda = +2i, INSIDE, gives 2.642e-06; lambda = -2,
      OUTSIDE, gives 8.180e-06), not admissibility.  The decisive number: at lambda = +5 the
      OMITTED term is 6.320e+32 times the scale the defect is normalised by, and the function
      reports 8.296e-05 -- a 36.9-decade gap between what was left out and what was reported.
      Lesson 90's shape, in a module that predates lesson 90.

  R5  NON-INTEGER `K` IS SILENTLY FLOOR-TRUNCATED.  `OddCompactBasis` does `int(K)` with no
      warning, on the RESOLUTION parameter: 5/5 cases (3.7 -> 3, 96.9 -> 96, 144.9999 -> 144).
      This is the reachability path for R1 -- K_coarse = 96 and K_fine = 96.9 collapse to the
      same grid.

  R6  THE FILTER'S KEPT-COUNT IS BLIND TO A PLANTED WRONG PROFILE.  Perturbing the exact a = 0
      fixed point by delta and running the same two-grid filter, the count stays at 2 -- the
      quantity Route-E reports -- for every delta up to 1e-01, at which the residual is
      already 1.801e-01, i.e. 7.3 decades above the module's own 1e-8 threshold.  The
      eigenvalue POSITIONS do move (|lambda + 1| tracks delta linearly), but nothing in the
      return value flags it.

  R7  `match_filter` TOLERANCE DEGENERACIES.  `tol = nan` keeps 0 silently (because
      `nan < tol` is False) and `tol = inf` keeps everything.  The nan case is the sharper
      one: "nothing survived the filter" is precisely this module's headline, so a nan
      tolerance REPRODUCES THE CONCLUSION.  An EMPTY fine spectrum raises ValueError -- a
      visible rejection, and a pass.

  R8  `planted_eigenvalue_control`'s DOCSTRING CRITERION DOES NOT HOLD -- PROSE ONLY.  It says
      "the control asserts that the filter reports MORE converged eigenvalues than the
      unperturbed operator does".  The count is UNCHANGED (2 vs 2).  The module's own test 6
      checks the right thing -- a POSITION shift into the right half plane (Re = +1.0831,
      shift 1.0831) -- so the CHECK is sound and only the description is wrong.  Recorded
      because a reader taking the docstring at its word would conclude the control had failed.
      No number depends on it.

SEVERITY, MEASURED, NOT ASSERTED.  **R1, R3, R4, R5, R7 are LATENT: no live call site passes
the trapping argument.**  Every `converged_spectrum`-shaped call site passes K = 96/144
(test_rescaled_spectrum.py:132, p2_route_e_v1_spectrum.py:158, p2_route_h_v1_critical.py:224,
critical_dissipation.py:576); Route-E passes a >= 0 with da = +0.02 and Route-G passes a < 0
with da = -0.02, so both signs match; every tol passed anywhere is in 1e-4 .. 1e-1.

**R2 is NOT latent.**  5/7 banked Route-E `E5_sweep` rows (a = 0.1, 0.2, 0.3, 0.4, 0.55;
residuals 6.187e-04 .. 1.135e-02) and 7/7 banked Route-G `g4_cross_model` rows (residuals
9.094e-05 .. 2.275e-03) were computed at points whose residual exceeds the module's own 1e-8
threshold.  TWO THINGS CUT THE OTHER WAY AND ARE STATED BECAUSE THEY DO: (i) both routes BANKED
their residuals alongside the values, so the condition is discoverable from the JSON and was
not hidden; (ii) the 1e-8 test is a hard-coded sup-residual test and is CONSERVATIVE -- the
banked a = 0.5 / K = 96 row is flagged converged=False at residual 3.319e-08 while its alpha is
3.00000002 against an exact 3.  So `converged=False` is NOT by itself evidence that a banked
spectrum is wrong, and this leg does not claim it is.  What it claims is that the MODULE offers
its consumers no flag, and that the affected rows are the intermediate a -- while the two
analytic points the module's own docstring says quantitative statements are quoted at (a = 0,
alpha = 1 and a = 1/2, alpha = 3) are exactly the two E5 rows that ARE converged, both giving
n_kept = 2 and n_unstable = 0.

**THE ORIGIN-H2 SPECTRAL GAP IS NOT DOWNSTREAM.**  `solver/origin_h2_certificate.py` -- the
STRICT realization, the one with the gap (legs 176/186) -- imports only `numpy` and
`math.comb`.  Legs 176/186 cite this module's DOCSTRING on the loose realization; no banked
origin-H2 gap number is computed by any code path in it.  Claim-adjacency runs through
Route-E/Route-G instead, which is why leg 203's yes-branch is ESCALATE, DO NOT PATCH.

NOT A RE-FIND OF LEGS 66/69/79/120.  Those are all `solver/spectral_utils.py` and its FFT path,
which this module does not import -- it is dense linear algebra on a sine collocation basis,
`numpy` only.  Leg 70 is the only prior audit of this module and it is docs-only: it lists
`newton`, `continuation`, `spectrum`, `converged_spectrum` and `np.linalg.eigvals` in its own
BANNED_CALLS and never executes them.

THE PASSES ARE CHECKED AS LOUDLY AS THE DEFECTS (leg 91's rule): `check_passes_*` below are the
map of inputs this module handles CORRECTLY, and they are the majority of what was tested.

Test convention (repo-wide): self-running script, no pytest.
    .venv/bin/python test_rescaled_spectrum_adversarial.py
"""

import warnings

import numpy as np

from solver.rescaled_spectrum import (
    OddCompactBasis,
    RescaledFlow,
    continuation,
    continuum_defect,
    continuum_eigenfunction,
    converged_spectrum,
    match_filter,
    planted_eigenvalue_control,
)

SEED = 20260806
POISONS = (("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf")))

# The exact a = 0 spectrum in the analytic class (module docstring, lines 98-113).
EXACT_A0 = (0.0, -1.0)


# --------------------------------------------------------------------------
# R1 -- the self-comparison trap
# --------------------------------------------------------------------------
def check_R1_self_comparison_certifies_continuum():
    """PIN: converged_spectrum has no guard on K_fine vs K_coarse.

    CORRECT behaviour would be to raise (or at minimum warn) when K_fine == K_coarse, since
    the module's line 116 defines a discrete eigenvalue as one that survives REFINEMENT.
    Pinned here: with equal K the entire discretized continuum is returned as converged, with
    every match distance identically zero.
    """
    for K in (24, 32, 48):
        good = converged_spectrum(0.0, K_coarse=K, K_fine=K + 12, tol=1e-3)
        bad = converged_spectrum(0.0, K_coarse=K, K_fine=K, tol=1e-3)
        assert good["n_kept"] == 2, (K, good["n_kept"])
        kept_good = np.sort_complex(np.asarray(good["kept"]))
        assert min(abs(kept_good - 0.0)) < 1e-12
        assert min(abs(kept_good + 1.0)) < 1e-12
        # PIN: the defective branch keeps everything, at distance exactly zero
        assert bad["n_kept"] == K, (K, bad["n_kept"])
        assert bad["n_total"] == K
        assert float(np.max(bad["dist"])) == 0.0, float(np.max(bad["dist"]))
        # and what it keeps includes a large purely-imaginary pair
        assert float(np.max(np.abs(np.imag(bad["kept"])))) > 10.0

    # CONTROL that can come out differently: a COARSER "fine" grid is still filtered correctly
    coarser = converged_spectrum(0.0, K_coarse=24, K_fine=12, tol=1e-3)
    assert coarser["n_kept"] == 2, coarser["n_kept"]
    print("[pin] R1 converged_spectrum(K_c=K, K_f=K) keeps ALL K eigenvalues (24/24, 32/32, "
          "48/48) at match distance exactly 0.0, vs the correct 2 = {0, -1}; the retained "
          "set includes a purely imaginary pair beyond 10i. K_fine < K_coarse still gives 2, "
          "so the trap is EQUALITY specifically")


# --------------------------------------------------------------------------
# R2 -- the dropped convergence flag
# --------------------------------------------------------------------------
def check_R2_convergence_flag_dropped():
    """PIN: spectrum()/converged_spectrum() never read newton's `converged`.

    CORRECT behaviour would be to propagate the flag into the returned dict (or refuse).
    Pinned here at a = 0, where the spectrum is EXACTLY {0, -1}: a capped-iteration solve is
    consumed silently and produces eigenvalues far from the truth, including spurious
    right-half-plane ones.
    """
    import inspect

    import solver.rescaled_spectrum as RS
    for fn in (RS.spectrum, RS.converged_spectrum):
        body = inspect.getsource(fn).split('"""')[-1]
        assert "converged" not in body, fn.__name__      # PIN

    rng = np.random.default_rng(SEED)
    K = 48
    f = RescaledFlow(0.0, K=K)
    b_start = f.B.anchor() + 0.5 * rng.standard_normal(K) / (1.0 + np.arange(K)) ** 2

    out1 = f.newton(b0=b_start.copy(), max_iter=1)
    assert not out1["converged"]
    ev1 = np.linalg.eigvals(f.generator(out1["b"]))
    d_amp = float(np.min(np.abs(ev1 + 1.0)))
    n_rhp = int(np.sum(np.real(ev1) > 1e-6))
    # PIN: the module hands this spectrum to any caller without complaint
    assert d_amp > 0.2, d_amp
    assert n_rhp >= 40, n_rhp

    # and the converged end of the same ladder recovers the exact pair
    out_ok = f.newton(b0=b_start.copy(), max_iter=120)
    assert out_ok["converged"]
    ev_ok = np.linalg.eigvals(f.generator(out_ok["b"]))
    assert float(np.min(np.abs(ev_ok + 1.0))) < 1e-12
    assert float(np.min(np.abs(ev_ok - 0.0))) < 1e-12
    print("[pin] R2 neither spectrum() nor converged_spectrum() mentions `converged`; a "
          "1-iteration solve at a = 0 yields |lambda + 1| = %.4e from the exact -1 and %d "
          "eigenvalues in the right half plane where the truth has none -- accepted silently. "
          "The converged end of the same ladder recovers {0, -1} to 1e-12" % (d_amp, n_rhp))


# --------------------------------------------------------------------------
# R3 -- continuation silently skipped
# --------------------------------------------------------------------------
def check_R3_continuation_silently_skipped():
    """PIN: a sign-mismatched `da` empties the arange grid and the fallback solves cold.

    CORRECT behaviour would be to raise on sign(da) != sign(a_target), or to take
    abs(da) with the sign implied by a_target.  Pinned here: the two paths return the same
    shape with no flag, and at a = 0.5 they differ by a SIGN CHANGE in alpha.
    """
    K = 48
    # the grid really is empty -- the mechanism, not just the symptom
    assert np.arange(0.0, 0.5 + 1e-12, -0.02).size == 0
    assert np.arange(0.0, -0.3 + 1e-12, 0.02).size == 0

    _, followed = continuation(0.5, K=K, da=0.02)
    _, skipped = continuation(0.5, K=K, da=-0.02)
    a_followed = -followed["c_omega"]
    a_skipped = -skipped["c_omega"]
    assert a_followed > 2.9, a_followed
    assert a_skipped < 0.0, a_skipped                     # PIN: opposite sign
    assert abs(a_followed - a_skipped) > 3.9, abs(a_followed - a_skipped)
    # both report the same shape; nothing distinguishes them
    assert set(followed) == set(skipped)

    # da = 0 is a VISIBLE rejection -- a pass, kept here so it cannot regress into silence
    try:
        continuation(0.3, K=16, da=0.0)
        raise AssertionError("da = 0 should raise")
    except ZeroDivisionError:
        pass
    print("[pin] R3 sign-mismatched da empties np.arange and the fallback solves COLD: at "
          "a = 0.5, K = 48 alpha = %+.8f (followed) vs %+.8f (skipped), |delta| = %.6f, a "
          "sign change in the far-field exponent, with identical return shape. da = 0 raises "
          "ZeroDivisionError (visible -- a pass)"
          % (a_followed, a_skipped, abs(a_followed - a_skipped)))


# --------------------------------------------------------------------------
# R4 -- continuum_defect has no admissibility content
# --------------------------------------------------------------------------
def check_R4_continuum_defect_not_discriminating():
    """PIN: continuum_defect accepts every lambda, in-strip and far outside.

    CORRECT behaviour would be to test ADMISSIBILITY (the boundary conditions at w = +-1),
    not merely the homogeneous ODE residual which the closed form satisfies identically for
    every complex lambda, and not to drop the -s(w=1)(1+w) term outside the strip where it is
    not zero.
    """
    inside = [0.0, -1.0, 0.9, 0.999, 0.5j, 2.0j, 0.3 + 0.7j]
    outside = [1.0, 1.5, 2.0, 3.0, 5.0, 10.0, -2.0, -5.0, 2.0 + 3.0j]
    d_in = [float(continuum_defect(z)) for z in inside]
    d_out = [float(continuum_defect(z)) for z in outside]
    # PIN: everything is "accepted" -- no lambda is rejected and none is even large
    assert max(d_in) < 1e-4, max(d_in)
    assert max(d_out) < 1e-3, max(d_out)
    # PIN: no threshold separates the groups -- an in-strip lambda beats an out-strip one
    assert float(continuum_defect(2.0j)) < float(continuum_defect(-2.0))

    # the decisive control: how big is the term the function drops?
    th = np.linspace(1e-3, np.pi - 1e-3, 4001)
    interior = slice(int(0.05 * 4001), int(0.95 * 4001))
    s5 = continuum_eigenfunction(5.0, th)
    scale5 = float(np.max(np.abs(s5[interior])))
    dropped5 = abs(complex(continuum_eigenfunction(5.0, np.array([1e-9]))[0])) / scale5
    assert dropped5 > 1e30, dropped5                      # PIN
    assert float(continuum_defect(5.0)) < 1e-3            # PIN: reported anyway
    # inside the strip the same omission is genuinely harmless -- the control that differs
    s05 = continuum_eigenfunction(0.5, th)
    dropped05 = (abs(complex(continuum_eigenfunction(0.5, np.array([1e-9]))[0]))
                 / float(np.max(np.abs(s05[interior]))))
    assert dropped05 < 1e-3, dropped05
    print("[pin] R4 continuum_defect rejects nothing: worst in-strip %.3e vs worst "
          "out-of-strip %.3e, and lambda = 2i (inside) scores WORSE than lambda = -2 "
          "(outside). At lambda = 5 the dropped term is %.3e x the normalising scale while "
          "the reported defect is %.3e (%.1f decades); inside the strip the same ratio is "
          "%.3e, which is why test 5b cannot see it"
          % (max(d_in), max(d_out), dropped5, float(continuum_defect(5.0)),
             np.log10(dropped5 / float(continuum_defect(5.0))), dropped05))


# --------------------------------------------------------------------------
# R5 -- non-integer K silently truncated
# --------------------------------------------------------------------------
def check_R5_non_integer_K_truncated():
    """PIN: OddCompactBasis does int(K) on the RESOLUTION parameter, with no warning.

    CORRECT behaviour would be to raise on a non-integral K.  Pinned here together with the
    consequence that makes it matter: 96 and 96.9 are the same grid, which is R1's input.
    """
    for req, got in ((3.7, 3), (15.9, 15), (96.9, 96), (144.9999, 144), (48.5, 48)):
        assert OddCompactBasis(req).K == got, (req, OddCompactBasis(req).K)
    assert OddCompactBasis(96).K == OddCompactBasis(96.9).K     # PIN: R1 reachability
    print("[pin] R5 non-integer K silently floor-truncated in 5/5 cases (96.9 -> 96), so "
          "K_coarse = 96 and K_fine = 96.9 are the SAME grid -- the reachability path for R1")


# --------------------------------------------------------------------------
# R6 -- the kept-count is blind to a planted wrong profile
# --------------------------------------------------------------------------
def check_R6_planted_profile_pass_through():
    """PIN: the filter's kept-COUNT does not move until the perturbation is large.

    The module offers no injection hook, so the two-grid filter is reproduced here around a
    deliberately perturbed profile.  CORRECT behaviour would be for the caller to be told the
    profile is not a fixed point (see R2); the count alone cannot carry that.
    """
    K_c, K_f = 32, 48
    fc, ff = RescaledFlow(0.0, K=K_c), RescaledFlow(0.0, K=K_f)

    def kept_at(delta):
        r1 = np.random.default_rng(SEED)
        vc = r1.standard_normal(K_c) / (1.0 + np.arange(K_c)) ** 2
        vc = vc / np.max(np.abs(vc))
        r2 = np.random.default_rng(SEED)
        vf = r2.standard_normal(K_f) / (1.0 + np.arange(K_f)) ** 2
        vf = vf / np.max(np.abs(vf))
        bc, bf = fc.B.anchor() + delta * vc, ff.B.anchor() + delta * vf
        ev_c = np.linalg.eigvals(fc.generator(bc))
        ev_f = np.linalg.eigvals(ff.generator(bf))
        kept, _ = match_filter(ev_c, ev_f, 1e-3)
        return kept, float(np.max(np.abs(fc.residual(bc))))

    base, res0 = kept_at(0.0)
    assert base.size == 2 and res0 < 1e-14
    for delta in (1e-8, 1e-4, 1e-2, 1e-1):
        kept, res = kept_at(delta)
        assert kept.size == 2, (delta, kept.size)         # PIN: count unmoved
    kept_big, res_big = kept_at(1e-1)
    assert res_big > 1e-1, res_big                        # ... at a residual this large
    # the POSITIONS do move, which is what a repair would surface
    kept_mid, _ = kept_at(1e-2)
    assert float(np.min(np.abs(kept_mid + 1.0))) > 1e-3
    print("[pin] R6 the kept-COUNT stays at 2 for planted delta up to 1e-01, where the "
          "residual is already %.3e -- 7.3 decades above the module's own 1e-8 threshold. "
          "The eigenvalue POSITIONS move (|lambda + 1| = %.3e at delta = 1e-02) but nothing "
          "in the return value flags it"
          % (res_big, float(np.min(np.abs(kept_mid + 1.0)))))


# --------------------------------------------------------------------------
# R7 / R8
# --------------------------------------------------------------------------
def check_R7_tolerance_degeneracies():
    """PIN: match_filter accepts a non-finite tolerance silently.

    CORRECT behaviour would be to require a finite, strictly positive tol.  The nan case is
    the sharp one: it returns the module's own headline ("nothing survived") for a reason that
    has nothing to do with the operator.
    """
    ev_c = np.array([0.0, -1.0, 0.5j, -0.5j])
    ev_f = np.array([1e-12, -1.0 + 1e-12, 0.6j, -0.6j])
    assert match_filter(ev_c, ev_f, 1e-3)[0].size == 2
    assert match_filter(ev_c, ev_f, float("nan"))[0].size == 0        # PIN
    assert match_filter(ev_c, ev_f, float("inf"))[0].size == 4        # PIN
    assert match_filter(ev_c, ev_f, 0.0)[0].size == 0
    assert match_filter(ev_c, ev_f, -1.0)[0].size == 0
    print("[pin] R7 match_filter(tol = nan) silently keeps 0 -- reproducing this module's "
          "headline conclusion for a reason unrelated to the operator -- and tol = inf keeps "
          "all 4")


def check_R8_control_docstring_criterion():
    """PIN: the planted control's DOCSTRING criterion (a larger count) does not hold.

    The CHECK is sound -- test 6 asserts a position shift, which does hold.  Only the prose is
    wrong.  Pinned so it is repaired as prose, not by weakening test 6.
    """
    r = planted_eigenvalue_control(a=0.0, K_coarse=96, K_fine=144, strength=6.0, tol=1e-3)
    assert r["n_planted"] == r["n_plain"], (r["n_plain"], r["n_planted"])   # PIN
    planted = np.asarray(r["planted"])
    plain = np.asarray(r["plain"])
    max_re = float(np.max(np.real(planted)))
    shift = max(float(np.min(np.abs(plain - z))) for z in planted)
    assert max_re > 0.5 and shift > 0.5, (max_re, shift)   # the criterion that DOES hold
    print("[pin] R8 planted control: count UNCHANGED (%d vs %d), so the docstring's 'MORE "
          "converged eigenvalues' is wrong; the position criterion test 6 actually uses does "
          "hold (max Re = %+.4f, shift = %.4f). Prose-only; no number depends on it"
          % (r["n_plain"], r["n_planted"], max_re, shift))


# --------------------------------------------------------------------------
# THE PASSES
# --------------------------------------------------------------------------
def check_passes_non_finite_propagation():
    """PASS: every planted nan/inf stays visible and finally hard-stops at eigvals."""
    n = raised = 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for K in (16, 32):
            f = RescaledFlow(0.0, K=K)
            for slot in (0, 3, K - 1):
                for _, val in POISONS:
                    b = f.B.anchor()
                    b[slot] = val
                    n += 1
                    assert not np.isfinite(np.max(np.abs(f.residual(b))))
                    assert not np.isfinite(f.c_omega(b))
                    # np.linalg.solve does NOT reject a non-finite matrix; it propagates
                    assert not np.all(np.isfinite(f.generator(b)))
                    # the hard rejection happens one frame later, inside spectrum()
                    try:
                        np.linalg.eigvals(f.generator(b))
                    except np.linalg.LinAlgError:
                        raised += 1
                    out = RescaledFlow(0.0, K=K).newton(b0=b)
                    assert out["converged"] is False
        for _, val in POISONS:
            assert RescaledFlow(val, K=16).newton()["converged"] is False
    assert raised == n, (raised, n)
    print("[ok]  PASS non-finite: %d/%d coefficient poisons stayed visible through "
          "residual/c_omega/generator and raised LinAlgError at eigvals; newton flagged all "
          "of them, and a poisoned model parameter a is flagged 3/3. Nothing erased" % (n, n))


def check_passes_degenerate_and_visible_rejections():
    """PASS: the inputs this module refuses, and refuses loudly."""
    assert OddCompactBasis(0).S.shape == (0, 0)
    try:
        OddCompactBasis(0).anchor()
        raise AssertionError("K = 0 anchor should raise")
    except IndexError:
        pass
    for K, exc in ((-1, IndexError), (-4, ValueError)):
        try:
            OddCompactBasis(K)
            raise AssertionError("negative K should raise")
        except exc:
            pass
    ev_c = np.array([0.0, -1.0])
    try:
        match_filter(ev_c, np.array([]), 1e-3)
        raise AssertionError("empty fine spectrum should raise")
    except ValueError:
        pass
    print("[ok]  PASS rejections: K = 0 builds empty operators and anchor() raises "
          "IndexError; negative K raises (K=-1 IndexError, K=-4 ValueError -- different "
          "doors, leg 120's D7 shape, but both visible); an empty fine spectrum raises "
          "ValueError")


def check_passes_exact_anchor_untouched():
    """PASS / CONTROL: on VALID input the module is exact, so the pins are about the edges."""
    for K in (16, 48, 96):
        f = RescaledFlow(0.0, K=K)
        b = f.B.anchor()
        assert float(np.max(np.abs(f.residual(b)))) < 1e-14
        assert abs(f.c_omega(b) + 1.0) < 1e-14
        ev = np.linalg.eigvals(f.generator(b))
        assert float(np.min(np.abs(ev - EXACT_A0[0]))) < 1e-12
        assert float(np.min(np.abs(ev - EXACT_A0[1]))) < 1e-12
    print("[ok]  PASS control: on valid input the a = 0 anchor still nulls the residual to "
          "<1e-14 with c_omega = -1 and reproduces the exact pair {0, -1} to <1e-12 at "
          "K = 16, 48, 96 -- every pin above is about DEGENERATE input, not about the "
          "module's arithmetic")


if __name__ == "__main__":
    check_R1_self_comparison_certifies_continuum()
    check_R2_convergence_flag_dropped()
    check_R3_continuation_silently_skipped()
    check_R4_continuum_defect_not_discriminating()
    check_R5_non_integer_K_truncated()
    check_R6_planted_profile_pass_through()
    check_R7_tolerance_degeneracies()
    check_R8_control_docstring_criterion()
    check_passes_non_finite_propagation()
    check_passes_degenerate_and_visible_rejections()
    check_passes_exact_anchor_untouched()
    print("\nall leg-203 adversarial checks pass (8 PINS of current defective behaviour + 3 "
          "PASS batteries). Gate: YES -- the module can silently return a wrong value. "
          "No solver file was edited by this leg.")
