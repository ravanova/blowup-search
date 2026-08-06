"""Permanent adversarial regression test for solver/gclm_family.py (leg 88, Route-GCA).

Banked because the gate answered NO: under NaN/Inf-poisoned c_l/c_omega/c_tw and `a`
nine decades outside [0,1], the module's residual computation never silently returned a
finite, plausible-looking value -- 0 silent corruptions in 37 gate-scoped cases. This
file freezes that property so a later refactor cannot quietly introduce a nan_to_num, a
clip, a bare except, or a "helpful" default.

The threat model, stated once. solver/gclm_family.py has NO validity flag and NO
validation layer; its whole contract is the arithmetic it documents,

    R  = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X          (one-scale)
    R2 = Omega H(Omega) - c_tw Omega_X - a U Omega_X                      (two-scale)

so the only two ways it can fail silently are (i) swallowing a non-finite input, and
(ii) evaluating something other than the documented formula. Both are checked, on the
same n=401 c=0.5 sinh grid the module's own test_gclm_family.py uses.

test_gclm_family.py (12 tests) covers correctness on well-formed data and is untouched
by this file; this is the robustness complement, not a replacement.

Repo convention: self-running script, no pytest.
  Run: .venv/bin/python test_gclm_family_adversarial.py

Companion battery: experiments/p2_route_gca_v1_adversarial.py
Companion data:    writeup/data/p2_route_gca_v1_adversarial.json
"""

import numpy as np

from solver.gclm_family import (
    GCLMResidual,
    _drho_centered4,
    clm_one_scale,
    clm_two_scale,
)

N = 401
POISONS = [("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf"))]

G = GCLMResidual(a=0.0, n=N)
OM1 = clm_one_scale(G.X)
OM2 = clm_two_scale(G.X)


def _quiet():
    """The invalid-value warnings ARE the expected behaviour here, not a failure."""
    return np.errstate(all="ignore")


def _reference_residual(Gr, Omega, c_omega, c_l, a):
    """Independent reassembly of the documented one-scale formula, with no branch on a.

    The module's residual() short-circuits the advection term behind `if self.a != 0.0`;
    this reference never does, so the comparison also catches a mis-taken branch."""
    HOmega = Gr.Hmat @ Omega
    Omega_X = _drho_centered4(Omega, Gr.drho) / Gr.X_rho
    U = Gr.Vmat @ HOmega
    return (c_omega + HOmega) * Omega - c_l * (Gr.X * Omega_X) - a * (U * Omega_X)


def _raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


# -- the anchors still hold (guards against a suite that passes vacuously) ----

def test_baseline_anchors_are_still_sharp():
    """If the anchors ever stop nulling, every 'poison propagated' below is meaningless."""
    n1 = G.residual_norm(OM1)
    n2 = G.residual_two_scale_norm(OM2)
    _, c_tw = G.residual_two_scale(OM2)
    print(f"    one-scale RMS {n1:.3e}, two-scale RMS {n2:.3e}, c_tw {c_tw:.6f}")
    assert n1 < 1e-5, "the a=0 one-scale anchor stopped nulling"
    assert n2 < 1e-5, "the a=0 two-scale anchor stopped nulling"
    assert abs(c_tw - 0.5) < 1e-6, "exact traveling-wave speed of Omega_2 moved"
    print("[ok] both a=0 anchors still sharp -- the battery below is not vacuous")


# -- (i) non-finite coefficients must PROPAGATE, not vanish ------------------

def test_poisoned_coefficient_propagates_to_every_node():
    """A NaN/Inf gauge coefficient must contaminate the WHOLE residual array and the
    scalar norm -- not one node, and certainly not zero nodes."""
    for slot in ("c_l", "c_omega"):
        for tag, val in POISONS:
            with _quiet():
                R, _, _ = G.residual(OM1, **{slot: val})
                nrm = G.residual_norm(OM1, **{slot: val})
            n_fin = int(np.sum(np.isfinite(R)))
            assert n_fin == 0, (
                f"{slot}={tag} left {n_fin}/{R.size} residual nodes finite; "
                "the poison was partially swallowed")
            assert not np.isfinite(nrm), (
                f"{slot}={tag} produced a finite scalar norm {nrm!r}")
    print(f"[ok] 6 single-slot poisons each reached 100% of {N} residual nodes")


def test_jointly_poisoned_coefficients_do_not_cancel():
    """Notably +inf in one slot and -inf in the other must NOT cancel to a finite value."""
    for tag_l, pl in POISONS:
        for tag_o, po in POISONS:
            with _quiet():
                R, _, _ = G.residual(OM1, c_l=pl, c_omega=po)
                nrm = G.residual_norm(OM1, c_l=pl, c_omega=po)
            assert not np.any(np.isfinite(R)), (
                f"c_l={tag_l}, c_omega={tag_o} left residual nodes finite")
            assert not np.isfinite(nrm), (
                f"c_l={tag_l}, c_omega={tag_o} cancelled to a finite norm {nrm!r}")
    print("[ok] all 9 joint poisons propagate; +inf/-inf does not cancel to a finite norm")


def test_poisoned_a_propagates_on_both_residuals():
    """`a` is fixed per instance, and the advection term sits behind `if self.a != 0.0`.
    NaN and +-Inf all compare != 0.0, so the branch must be TAKEN and the poison must
    reach the output on the one-scale and the two-scale residual alike."""
    for tag, val in POISONS:
        with _quiet():
            Ga = GCLMResidual(a=val, n=N)
            R1, _, _ = Ga.residual(OM1)
            R2, _ = Ga.residual_two_scale(OM2)
            n1 = Ga.residual_norm(OM1)
            n2 = Ga.residual_two_scale_norm(OM2)
        assert not np.any(np.isfinite(R1)), f"a={tag} left one-scale nodes finite"
        assert not np.any(np.isfinite(R2)), f"a={tag} left two-scale nodes finite"
        assert not np.isfinite(n1) and not np.isfinite(n2), (
            f"a={tag} produced finite norms {n1!r}, {n2!r}")
    print("[ok] a in {nan,+inf,-inf}: advection branch taken, poison reaches both residuals")


def test_poisoned_c_tw_propagates():
    """The two-scale traveling-wave speed is the other user-supplied coefficient."""
    for tag, val in POISONS:
        with _quiet():
            R, _ = G.residual_two_scale(OM2, c_tw=val)
            nrm = G.residual_two_scale_norm(OM2, c_tw=val)
        assert not np.any(np.isfinite(R)), f"c_tw={tag} left residual nodes finite"
        assert not np.isfinite(nrm), f"c_tw={tag} produced a finite norm {nrm!r}"
    print("[ok] c_tw in {nan,+inf,-inf} propagates through the two-scale residual")


def test_per_node_poison_stays_localized():
    """A per-node c_l array with exactly one NaN must poison exactly one node: the
    failure mode in both directions (spreading, or vanishing) is caught here."""
    c_l = np.where(np.arange(G.n) == 5, np.nan, 1.0)
    with _quiet():
        R, _, _ = G.residual(OM1, c_l=c_l)
    n_bad = int(np.sum(~np.isfinite(R)))
    assert n_bad == 1, (
        f"one poisoned coefficient node produced {n_bad} non-finite residual nodes")
    assert not np.isfinite(R[5]), "the poison landed on the wrong node"
    print("[ok] a single poisoned c_l node poisons exactly node 5, no spread, no vanish")


# -- (ii) the module must evaluate the formula it documents ------------------

def test_matches_independent_reference_for_a_far_outside_unit_interval():
    """The strong check: every node of the returned array must match an independent
    reassembly of the documented formula, at |a| up to 1e9. A clamp, a saturation or a
    mis-taken `if self.a != 0.0` branch all break this."""
    worst = 0.0
    for a in (-1e9, -1e5, -10.0, 0.0, 0.5, 10.0, 1e5, 1e9):
        Ga = GCLMResidual(a=a, n=N)
        with _quiet():
            R, c_om, c_l = Ga.residual(OM1)
            ref = _reference_residual(Ga, OM1, c_om, c_l, a)
        assert np.all(np.isfinite(R)), f"finite a={a:g} produced non-finite residual nodes"
        rel = float(np.max(np.abs(R - ref))) / float(np.max(np.abs(ref)))
        worst = max(worst, rel)
        assert rel < 1e-12, (
            f"a={a:g}: module departs from its documented formula by {rel:.3e}")
    print(f"[ok] 8 values of a match an independent recomputation to {worst:.2e} relative")


def test_large_a_does_not_saturate():
    """||R|| must keep tracking |a| with no ceiling. The signature is that the deviation
    of ||R||/|a| from the pure-advection constant decays like 1/|a|; a clamp would make
    that deviation GROW. Measured at leg 88: dev*|a| constant at 8.0697e-07."""
    HOm = G.Hmat @ OM1
    OmX = _drho_centered4(OM1, G.drho) / G.X_rho
    k = float(np.sqrt(np.mean(((G.Vmat @ HOm) * OmX) ** 2)))
    assert k > 0, "the pure-advection constant vanished; the probe is degenerate"

    prods = []
    for a in (1e1, 1e2, 1e3, 1e5):
        nrm = GCLMResidual(a=a, n=N).residual_norm(OM1)
        assert np.isfinite(nrm), f"a={a:g} gave a non-finite norm"
        prods.append(abs(nrm / a / k - 1.0) * a)
    spread = max(prods) / min(prods)
    print(f"    k={k:.7f}, dev*|a| = {['%.4e' % p for p in prods]} (spread {spread:.3f}x)")
    assert spread < 2.0, (
        f"deviation from the linear-in-a law does not decay as 1/|a|: dev*|a| = {prods}")

    n1 = GCLMResidual(a=1e3, n=N).residual_norm(OM1)
    n2 = GCLMResidual(a=1e6, n=N).residual_norm(OM1)
    assert n2 / n1 > 9e2, f"||R|| saturated: 1000x in a gave only {n2/n1:.3g}x in ||R||"
    print(f"[ok] no saturation: 1000x in a gives {n2/n1:.1f}x in ||R||")


def test_huge_finite_a_overflows_honestly_rather_than_clamping():
    """a=1e300 must overflow to inf, not silently return a plausible finite number."""
    with _quiet():
        nrm = GCLMResidual(a=1e300, n=N).residual_norm(OM1)
    assert not np.isfinite(nrm), f"a=1e300 returned a finite norm {nrm!r}"
    print("[ok] a=1e300 overflows to inf rather than clamping to a plausible number")


def test_extreme_finite_coefficients_are_not_clamped():
    """Huge finite coefficients must produce a huge (or infinite) residual, never a
    number that looks like a converged one."""
    baseline = G.residual_norm(OM1)
    for slot in ("c_l", "c_omega"):
        for v in (1e300, -1e300, 1e16):
            with _quiet():
                nrm = G.residual_norm(OM1, **{slot: v})
            assert not np.isfinite(nrm) or nrm > 1e6 * max(baseline, 1e-12), (
                f"{slot}={v:g} returned {nrm!r}, implausibly close to the "
                f"baseline {baseline:.3e}")
    print(f"[ok] 6 extreme finite coefficients all dwarf the {baseline:.2e} baseline")


# -- (iii) malformed shapes must RAISE, not answer ---------------------------

def test_malformed_shapes_raise():
    """A raise is a FLAG. A silent wrong-shaped answer would be the failure."""
    checks = [
        ("wrong-length profile", lambda: G.residual(np.ones(7)), ValueError),
        ("column-shaped profile", lambda: G.residual(OM1.reshape(-1, 1)), ValueError),
        ("wrong-length c_l array", lambda: G.residual(OM1, c_l=np.ones(7)), ValueError),
        ("a=None in constructor", lambda: GCLMResidual(a=None, n=101), TypeError),
    ]
    for name, fn, exc in checks:
        assert _raises(fn, exc), f"{name} did not raise {exc.__name__}"
    print(f"[ok] all {len(checks)} malformed-shape adversaries raise rather than answer")


# -- (iv) the known fallbacks, pinned as measured ----------------------------

def test_gauge_c_tw_zero_fallback_is_pinned_and_its_residual_still_propagates():
    """RECORDED CAVEAT, not a clean pass: `if denom > 0 else 0.0`
    (gclm_family.py:190/204/233) compares False on a NaN denominator, so a NaN-poisoned
    PROFILE yields a finite gauge speed of exactly 0.0. Pinned so the behaviour cannot
    change unnoticed. It did NOT decide leg 88's gate, because (a) profile poisoning is
    not the gated input class -- the gate asks about coefficients -- and (b) the residual
    accompanying that gauge is still 100% non-finite, so no consumer of the RESIDUAL
    receives a clean-looking value."""
    poisoned = OM2.copy()
    poisoned[10] = np.nan
    with _quiet():
        c = G.gauge_c_tw(poisoned)
        R, c_tw = G.residual_two_scale(poisoned)
    assert c == 0.0 and np.isfinite(c), f"the pinned 0.0 fallback moved to {c!r}"
    assert c_tw == 0.0
    assert not np.any(np.isfinite(R)), (
        "the residual accompanying the zeroed gauge became finite -- that WOULD be a "
        "silent corruption and must be escalated")
    print("[ok] gauge_c_tw zero-fallback pinned; its residual is still 100% non-finite")


def test_relnorm_scale_invariance_holds_where_used_and_fails_below():
    """RECORDED CAVEAT, out of leg 88's gate scope (amplitude, not coefficients).

    residual_two_scale_relnorm's docstring claims scale-invariance so a GA cannot cheat
    by shrinking the amplitude. The max(scale, 1e-30) floor on line 236 breaks that below
    |Omega| ~ 1e-15. Pinned in BOTH directions: invariance must hold over the amplitudes
    the GA actually explores, and the known break must not silently move."""
    ref = G.residual_two_scale_relnorm(OM2)
    for eps in (1e0, 1e-3, 1e-6, 1e-10, 1e-14):
        v = G.residual_two_scale_relnorm(eps * OM2)
        assert abs(v / ref - 1.0) < 1e-6, (
            f"scale-invariance lost at eps={eps:g}, well above the known 1e-15 break")
    with _quiet():
        broken = G.residual_two_scale_relnorm(1e-15 * OM2)
        zeroed = G.residual_two_scale_relnorm(1e-100 * OM2)
    assert broken < 0.5 * ref, (
        "the known relnorm break at eps=1e-15 has moved; re-audit before trusting the "
        "fitness at small amplitude")
    assert zeroed == 0.0, "the pinned exact-zero collapse at eps=1e-100 moved"
    print(f"    invariance exact to eps=1e-14; at eps=1e-15 ratio {broken/ref:.3e}; "
          f"exactly 0.0 by eps=1e-100")
    print("[ok] relnorm break pinned in both directions (caveat, not a gate failure)")


if __name__ == "__main__":
    test_baseline_anchors_are_still_sharp()
    test_poisoned_coefficient_propagates_to_every_node()
    test_jointly_poisoned_coefficients_do_not_cancel()
    test_poisoned_a_propagates_on_both_residuals()
    test_poisoned_c_tw_propagates()
    test_per_node_poison_stays_localized()
    test_matches_independent_reference_for_a_far_outside_unit_interval()
    test_large_a_does_not_saturate()
    test_huge_finite_a_overflows_honestly_rather_than_clamping()
    test_extreme_finite_coefficients_are_not_clamped()
    test_malformed_shapes_raise()
    test_gauge_c_tw_zero_fallback_is_pinned_and_its_residual_still_propagates()
    test_relnorm_scale_invariance_holds_where_used_and_fails_below()
    print("\nALL GCLM-FAMILY ADVERSARIAL TESTS PASSED")
