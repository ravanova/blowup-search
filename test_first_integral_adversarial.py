"""Adversarial gates for `solver/first_integral.py` (leg 107, Route-FIA).

`test_first_integral.py` validates the module on WELL-FORMED parameters: the quadrature
against exact moments, the finite Hilbert transform against a Chebyshev known answer, the
a -> 0 anchor, the identity on independent profiles, the analytic Jacobian, the radius
against a cross-build, and the reconstruction nulling the original ODE residual. Every
input in that file is legal and in-domain. This file validates the other half — what the
module does at and beyond its own free boundary, and on NaN-poisoned samples — and banks
leg 107's battery so the answer cannot silently regress.

The gate leg 107 answered, verbatim:

  "Under an adversarial battery (inputs near the documented turning point, NaN-poisoned
   profile parameters), does solver/first_integral.py ever silently return a finite,
   plausible-looking wrong profile value instead of propagating or flagging the
   ill-conditioning?"

Answered **YES**, on two independent sites. Leg 107 had no patch authority under its own
gate and escalated; **a bench repair then closed both gaps**, and this file has been
updated the way leg 107's own escalation said it must be:

    "If one of them fails, that is very likely GOOD NEWS — someone has fixed the gap —
     and the correct response is to read leg 107's escalation, confirm the fix, and
     convert the gate to a soundness gate. It must NOT be 'fixed' by loosening the
     tolerance."

No tolerance was loosened. Gates 1-4 below were CHARACTERIZATION gates asserting the gap
was open; each is now a SOUNDNESS gate asserting the repaired property, and each still
prints leg 107's original magnitude next to the repaired one so the size of what was
fixed stays on the record:

  | gate | leg 107 measured (pre-repair) | this file now asserts (post-repair) |
  |---|---|---|
  | 1 | 96/96 out-of-support evaluations returned a finite nonzero value; truth is 0 | every out-of-support evaluation returns exactly 0.0 and warns |
  | 2 | within 1% of `X_c` the fabricated value matched the interior mirror to 5e-2 | there is no fabricated value left to mirror |
  | 3 | `max abs(T_2k(v>1) - T_2k(1)) = 0.0` (silent clip); `e_poly/e_true` up to 22.0 | `even_cheb`/`e_of` return NaN outside and warn; `"extrapolate"` reproduces the old numbers |
  | 4 | 397/400 NaN still certified (FI) to 1.33e-15 | 1/400 NaN is refused; 0 poisoned samples certified |

The pre-repair behaviour is still REACHABLE, on purpose, through the explicit legacy
policies `on_outside="extrapolate"` and `on_nonfinite="drop"` — leg 107's battery has to
keep being able to measure the gap it escalated — so gates 1-4 check both halves: that
the default is right, and that the legacy policy still reproduces the escalated numbers
and still warns.

WHAT "TRUE" MEANS OUTSIDE THE SUPPORT, AND WHERE IT COMES FROM
--------------------------------------------------------------
Not this leg's invention. `solver/first_integral.py`'s own module docstring, lines 29-33:

    THE PROFILE ENDS, and it is forced rather than assumed. E is decreasing ... so E
    reaches zero at a finite X_c; beyond it E < 0 and E^{1/a} is not real, so Omega == 0.

`solver/turning_point.py` states the same thing with the outside asymptotics
E ~ (a m / pi) log(X / X_c) < 0. So for v = X / X_c > 1 the true profile value is EXACTLY
ZERO, and any nonzero return there is wrong by its own full magnitude. The module's
`omega_of` computes `-np.abs(e) ** self.p`; the `abs` erases the branch cut that is the
entire reason the profile is compactly supported.

EVERY GATE IN THIS FILE IS NOW A SOUNDNESS GATE
-----------------------------------------------
There are no characterization gates left: all ten assert a property that HOLDS. If one
fails, the module has started absorbing bad input somewhere it previously flagged it, and
the response is to fix the module — never the tolerance.

Self-running, no pytest: `.venv/bin/python test_first_integral_adversarial.py`. ~35 s.
"""

import warnings

import numpy as np

from solver.first_integral import (FirstIntegralSampleWarning,
                                   FirstIntegralSupportWarning, ReducedProfile,
                                   even_cheb, first_integral_defect)


def _caught(fn, category=FirstIntegralSupportWarning):
    """Run `fn()`, returning (value, number of `category` warnings it raised)."""
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        val = fn()
    return val, sum(1 for w in rec if issubclass(w.category, category))

K = 48
A_CASES = (0.3, 0.5)


def _solved(a, k=K):
    rp = ReducedProfile(a, K=k)
    r = rp.solve(Xc0=10.0)
    assert r["converged"], f"a={a}: the clean solve must converge first ({r})"
    return rp, r["b"], r["Xc"]


# ---------------------------------------------------------------------------
# 0. the fixture itself, before anything is concluded from it
# ---------------------------------------------------------------------------
def test_clean_reference_selfcheck():
    """Every gate below is read against a converged profile; gate that first."""
    print("\n[0] clean reference self-check")
    for a in A_CASES:
        rp, b, Xc = _solved(a)
        res = float(np.max(np.abs(rp.residual(b, Xc))))
        e_nodes = rp.e_of(b)
        interior = np.abs(rp.omega_of(b, np.linspace(0.0, 1.0, 201)))
        print(f"    a={a}: X_c/c = {Xc:.6f}, residual {res:.2e}, "
              f"min e at nodes {e_nodes.min():.3e} (>0), "
              f"max |Omega| on support {interior.max():.6f}")
        assert res < 1e-10, "the clean solve is not converged; nothing below is meaningful"
        assert e_nodes.min() > 0.0, "e must be positive on the support"
        # the amplitude gauge: Omega(0) = -1, so the profile's own range is [0, 1]
        assert abs(interior.max() - 1.0) < 1e-9, interior.max()
    print("[ok] fixture converged, e > 0 on the support, gauge |Omega| <= 1 holds")


# ---------------------------------------------------------------------------
# 1. CHARACTERIZATION -- the turning point (finding A, escalated, unpatched)
# ---------------------------------------------------------------------------
def test_profile_is_exactly_zero_past_its_own_support():
    """SOUNDNESS (was characterization). Outside the support `omega_of` returns 0 and warns.

    Leg 107 measured 96/96 out-of-support evaluations coming back finite, NONZERO and
    inside the profile's own gauge range, silently. The repaired default `on_outside=
    "zero"` returns the module's own documented truth, `Omega == 0`, and raises
    `FirstIntegralSupportWarning`. The legacy value is still reachable, deliberately,
    via `on_outside="extrapolate"` — and this gate checks that it is still WRONG by the
    same magnitude leg 107 reported, so the size of the repair stays measured.
    """
    print("\n[1] SOUNDNESS: omega_of past the turning point (truth: exactly 0)")
    n_eval = n_zero = n_warned = 0
    for a in A_CASES:
        rp, b, Xc = _solved(a)
        vs = (1.0 + 1e-9, 1.001, 1.1, 1.5, 2.0)
        got, nw = _caught(lambda: rp.omega_of(b, np.array(vs)))
        legacy, nwl = _caught(
            lambda: rp.omega_of(b, np.array(vs), on_outside="extrapolate"))
        n_eval += len(vs)
        n_zero += int(np.count_nonzero(got == 0.0))
        n_warned += 1 if nw else 0
        print(f"    a={a}: repaired " + " ".join(f"{x:+.1e}" for x in got)
              + f"   ({nw} warning)")
        print(f"          legacy   " + " ".join(f"{x:+.3e}" for x in legacy)
              + f"   ({nwl} warning)")
        assert np.all(got == 0.0), (a, got)          # the module's own documented truth
        assert nw == 1 and nwl == 1, (a, nw, nwl)    # and it is never silent
        # the legacy path is still wrong by its full magnitude -- that is the repair's size
        assert np.all(legacy != 0.0) and np.all(np.abs(legacy[:4]) < 1.0), legacy
        # strict mode
        try:
            rp.omega_of(b, np.array([2.0]), on_outside="raise")
        except ValueError:
            pass
        else:
            raise AssertionError(f"a={a}: on_outside='raise' did not raise")
        with warnings.catch_warnings():
            warnings.simplefilter("error", FirstIntegralSupportWarning)
            try:
                rp.omega_of(b, np.array([2.0]))
            except FirstIntegralSupportWarning:
                pass
            else:
                raise AssertionError(f"a={a}: simplefilter('error') did not bite")
    print(f"[ok] {n_zero}/{n_eval} out-of-support evaluations return exactly 0.0, "
          f"{n_warned}/{len(A_CASES)} calls warned, 0 silent; leg 107 measured "
          f"0/{n_eval} correct here and 96/96 fabricated across its wider grid")


def test_in_support_evaluation_is_untouched_by_the_guard():
    """SOUNDNESS (was the mirror characterization). The guard costs the interior nothing.

    Leg 107's finding was dangerous because `Omega(1+d)` matched `Omega(1-d)` to 5e-2 at
    d = 1e-2 — the fabricated value was indistinguishable from a legitimate one. There is
    now nothing to mirror: the outside is exactly 0 while the inside is bit-for-bit what
    it always was. The second half of that sentence is the one worth gating, because a
    domain guard that perturbs the domain it guards is a worse bug than the one it fixes.
    """
    print("\n[2] SOUNDNESS: the interior is bit-identical, the exterior is 0")
    for a in A_CASES:
        rp, b, Xc = _solved(a)
        d_list = (1e-7, 1e-4, 1e-2)
        inside = np.array([1.0 - d for d in d_list])
        # the guard must not be entered at all for interior points
        guarded, nw = _caught(lambda: rp.omega_of(b, inside))
        raw = -np.abs(rp._e_raw(b, inside)) ** rp.p          # the pre-repair expression
        bits = int(np.count_nonzero(guarded.view(np.int64) != raw.view(np.int64)))
        outside, _ = _caught(lambda: rp.omega_of(b, 1.0 + np.array(d_list)))
        print(f"    a={a}: interior bit-differences {bits}/3, warnings {nw}; "
              f"exterior " + " ".join(f"{x:+.1e}" for x in outside))
        assert bits == 0, (a, guarded, raw)
        assert nw == 0, (a, nw)
        assert np.all(outside == 0.0), (a, outside)
    # v = 1 exactly is the support EDGE and is INSIDE: the true value is zero and the
    # pre-repair expression already returns it, sign of the zero included.
    rp, b, Xc = _solved(0.3)
    edge, nw = _caught(lambda: rp.omega_of(b, np.array([1.0])))
    raw_edge = -np.abs(rp._e_raw(b, np.array([1.0]))) ** rp.p
    print(f"    v=1.0 exactly: {edge[0]!r} vs pre-repair {raw_edge[0]!r}, "
          f"warnings {nw} (the edge is inside)")
    assert edge.view(np.int64)[0] == raw_edge.view(np.int64)[0] and nw == 0
    print("[ok] 0 bit-differences on interior points and on the edge v=1, 0 spurious "
          "warnings; the exterior is exactly 0")


def test_even_cheb_refuses_to_extrapolate_silently():
    """SOUNDNESS (was characterization). `even_cheb` no longer freezes v > 1 at v = 1.

    Leg 107 measured `max abs(T_2k(v) - T_2k(1)) = 0.0` over v in (1.5, 3, 50) — every
    out-of-range point silently evaluated AT the edge — while `e_of` kept the unclipped
    `(1 - v^2)` prefactor, so the two halves of e(v) described different points and the
    result overstated the true `|E|` by up to 22x. Both halves now return NaN and warn.
    The clip itself STAYS, because its legitimate job is the removable endpoints v = ±1.
    """
    print("\n[3] SOUNDNESS: even_cheb's clip is no longer a domain check")
    far = np.array([1.5, 3.0, 50.0])
    (T_far, _), nw = _caught(lambda: even_cheb(6, far))
    print(f"    even_cheb(v>1) -> all-NaN rows: {bool(np.all(np.isnan(T_far)))}, "
          f"warnings {nw}")
    assert np.all(np.isnan(T_far)) and nw == 1, (T_far, nw)
    # the removable endpoints are still served, silently and exactly
    (T_edge, dT_edge), nw_edge = _caught(lambda: even_cheb(6, np.array([1.0, -1.0])))
    assert nw_edge == 0 and np.all(np.isfinite(T_edge)) and np.all(np.isfinite(dT_edge))
    print(f"    v=+-1 (removable): finite, {nw_edge} warnings, T_2k(1) = "
          + " ".join(f"{x:.0f}" for x in T_edge[0]))
    # the legacy clip is still reachable and still measurably wrong
    (T_leg, _), nw_leg = _caught(lambda: even_cheb(6, far, on_outside="extrapolate"))
    dev = float(np.max(np.abs(T_leg - T_edge[0][None, :])))
    print(f"    legacy policy: max abs(T_2k(v) - T_2k(1)) = {dev:.1e} "
          f"(leg 107's 0.0, reproduced), warnings {nw_leg}")
    assert dev == 0.0 and nw_leg == 1
    a = 0.3
    rp, b, Xc = _solved(a)
    wq = -np.abs(rp.PHI_u @ b) ** rp.p
    for v, lo in ((1.1, 1.05), (2.0, 2.0)):
        y = np.geomspace(1.0, v, 2001)
        Hy = ((wq[None, :] / (y[:, None] - rp.u[None, :])) @ rp.w) / np.pi
        e_true = (a / rp.c) * Xc * float(np.sum(0.5 * (Hy[1:] + Hy[:-1]) * np.diff(y)))
        e_new, nwe = _caught(lambda: float(rp.e_of(b, np.array([v]))[0]))
        e_leg, _ = _caught(
            lambda: float(rp.e_of(b, np.array([v]), on_outside="extrapolate")[0]))
        print(f"    v={v}: e_of -> {e_new} ({nwe} warning);  legacy {e_leg:+.4e} vs "
              f"e_true(outer) {e_true:+.4e}, ratio {e_leg / e_true:.3f}")
        assert np.isnan(e_new) and nwe == 1
        assert e_leg / e_true > lo, (v, e_leg / e_true)
    print("[ok] the exterior basis is NaN and warned; the removable endpoints still "
          "work silently; the legacy overstatement (1.1x at v=1.1, >2x at v=2) is "
          "reproduced only on explicit request")


# ---------------------------------------------------------------------------
# 2. SOUNDNESS -- the validator's NaN blindness, repaired (finding B)
# ---------------------------------------------------------------------------
def test_defect_refuses_nan_poisoned_samples():
    """SOUNDNESS (was characterization). One NaN point is now enough to refuse.

    Leg 107 measured 397 of 400 points NaN and the identity still certified to 1.33e-15,
    the number IMPROVING as the poisoning worsened, because every ordered comparison
    against NaN is false (IEEE-754 5.11) and the default mask therefore dropped the
    poison instead of being poisoned by it. The census is now taken BEFORE the mask.
    """
    print("\n[4] SOUNDNESS: first_integral_defect on NaN-poisoned samples")
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)
    clean, nw = _caught(lambda: first_integral_defect(Om, U, a, c),
                        FirstIntegralSampleWarning)
    print(f"    clean defect {clean:.3e} ({nw} warnings)")
    assert clean < 1e-12 and nw == 0, (clean, nw)
    absorbed, legacy_worst = 0, 0
    for nbad in (1, 10, 100, 397, 398, 400):
        Op = Om.copy()
        Op[:nbad] = np.nan
        d, nw = _caught(lambda: first_integral_defect(Op, U, a, c),
                        FirstIntegralSampleWarning)
        leg, _ = _caught(lambda: first_integral_defect(Op, U, a, c,
                                                       on_nonfinite="drop"),
                         FirstIntegralSampleWarning)
        if not np.isnan(d):
            absorbed = max(absorbed, nbad)
        if not np.isnan(leg):
            legacy_worst = max(legacy_worst, nbad)
        print(f"      {nbad:3d}/{N} NaN -> repaired {d!s:<8} ({nw} warning)"
              f"   legacy-drop {leg!s}")
        assert np.isnan(d) and nw == 1, (nbad, d, nw)
    print(f"    largest NaN count silently absorbed: {absorbed}/{N} "
          f"(leg 107 measured {legacy_worst}/{N} under the legacy policy, "
          f"reproduced here)")
    assert absorbed == 0, absorbed
    assert legacy_worst >= 397, (
        "the legacy policy stopped reproducing leg 107's escalated number -- re-derive")
    # the census is reported, not just used: a caller can see 3 survivors, not 400
    det, _ = _caught(
        lambda: first_integral_defect(np.where(np.arange(N) < 397, np.nan, Om), U, a, c,
                                      on_nonfinite="drop", detail=True),
        FirstIntegralSampleWarning)
    print(f"    detail on the 397-NaN sample: n_used={det['n_used']} of "
          f"n_points={det['n_points']}, n_nonfinite={det['n_nonfinite']}, "
          f"sample_valid={det['sample_valid']}, defect={det['defect']:.3e}")
    assert det["n_used"] == 3 and det["n_nonfinite"] == 397
    assert det["sample_valid"] is False
    # strict mode
    try:
        first_integral_defect(np.where(np.arange(N) == 0, np.nan, Om), U, a, c,
                              on_nonfinite="raise")
    except ValueError:
        pass
    else:
        raise AssertionError("on_nonfinite='raise' did not raise")
    print("[ok] 0 of 6 NaN-poisoned samples certified (leg 107: 397/400 absorbed); the "
          "legacy policy still reproduces the escalated number and still warns")


def test_no_silent_absorption_of_finite_poison():
    """SOUNDNESS. A poison that is a NUMBER rather than a NaN IS caught."""
    print("\n[5] SOUNDNESS: a finite poison is caught")
    a, c, N = 0.3, 0.5, 400
    X = np.linspace(0.01, 3.0, N)
    E = c * np.exp(-X ** 2 / 4.0)
    U = (E - c) / a
    Om = -(E / c) ** (1.0 / a)
    d = first_integral_defect(np.where(np.arange(N) == 200, Om * 2.0, Om), U, a, c)
    print(f"    one point doubled -> defect {d:.6f} (clean is ~6e-15)")
    assert d > 0.5, d
    # BEHAVIOUR CHANGE, recorded rather than hidden: pre-repair an inf point came back as
    # an inf defect (caught by arithmetic). It is now caught by the finiteness census one
    # step earlier and reported as nan, with a warning naming the count. Both are loud;
    # the new one also says HOW MANY points are bad, which the inf never did.
    dinf, nw = _caught(
        lambda: first_integral_defect(np.where(np.arange(N) == 3, np.inf, Om), U, a, c),
        FirstIntegralSampleWarning)
    dinf_legacy, _ = _caught(
        lambda: first_integral_defect(np.where(np.arange(N) == 3, np.inf, Om), U, a, c,
                                      on_nonfinite="drop"), FirstIntegralSampleWarning)
    print(f"    one point +inf     -> defect {dinf} ({nw} warning); "
          f"legacy-drop policy gives {dinf_legacy}")
    assert np.isnan(dinf) and nw == 1, (dinf, nw)
    for bad, label in ((float("nan"), "a"), (float("nan"), "c")):
        got = (first_integral_defect(Om, U, bad, c) if label == "a"
               else first_integral_defect(Om, U, a, bad))
        print(f"    {label}=nan -> {got}")
        assert np.isnan(got), (label, got)
    print("[ok] finite poison, inf poison and NaN SCALARS all propagate or flag")


# ---------------------------------------------------------------------------
# 3. SOUNDNESS -- everything the module gets right
# ---------------------------------------------------------------------------
def test_no_silent_corruption_from_nan_coefficients():
    """SOUNDNESS. A NaN in b_k reaches every derived quantity as NaN."""
    print("\n[6] SOUNDNESS: NaN in a Chebyshev coefficient propagates")
    rp, b, Xc = _solved(0.3)
    probes, finite = 0, 0
    for k in (0, 1, 10, rp.K - 1):
        bp = b.copy()
        bp[k] = np.nan
        with np.errstate(all="ignore"):
            outs = {"mass": rp.mass(bp, Xc),
                    "edge_amplitude": rp.edge_amplitude(bp, Xc),
                    "omega_of(0.5)": float(rp.omega_of(bp, np.array([0.5]))[0]),
                    "operator_norm": rp.operator_norm(bp, Xc),
                    "residual": float(np.max(np.abs(rp.residual(bp, Xc))))}
        for name, x in outs.items():
            probes += 1
            if np.isfinite(x):
                finite += 1
                print(f"    !! b[{k}]=nan -> {name} returned finite {x}")
    print(f"    finite values returned across {probes} probes: {finite}")
    assert finite == 0, "a NaN coefficient is being absorbed somewhere -- escalate"
    print("[ok] 0 silent finite values across 20 poisoned-coefficient probes")


def test_constructor_rejects_degenerate_a():
    """SOUNDNESS (with one pinned edge). a <= 0 and a = nan are refused."""
    print("\n[7] SOUNDNESS: the constructor's guard on a")
    for label, aa in (("nan", float("nan")), ("zero", 0.0), ("negative", -0.5)):
        try:
            ReducedProfile(aa, K=8)
        except ValueError:
            print(f"    a={label}: ValueError (refused)")
        else:
            raise AssertionError(f"a={label} was accepted")
    # PINNED EDGE: a = inf passes the guard (0.0 < inf) and gives p = 0, but the solve
    # then refuses rather than returning a number.
    rp = ReducedProfile(float("inf"), K=16)
    assert rp.p == 0.0, rp.p
    with np.errstate(all="ignore"):
        r = rp.solve(Xc0=10.0)
    print(f"    a=inf: accepted by the guard (p={rp.p}), solve converged="
          f"{r['converged']} residual={r['residual']}")
    assert not r["converged"], "a=inf now converges to something -- re-derive"
    print("[ok] nan/0/negative refused at construction; inf is admitted but never "
          "yields a converged answer")


def test_solve_never_lies_about_convergence():
    """SOUNDNESS. `converged` is true only when the residual really is below 1e-10."""
    print("\n[8] SOUNDNESS: the honesty of solve()['converged']")
    rp, b, Xc = _solved(0.3)
    bad = b.copy()
    bad[3] = np.nan
    with np.errstate(all="ignore"):
        cases = [("b0 poisoned", rp.solve(Xc0=10.0, b0=bad)),
                 ("Xc0 = nan", rp.solve(Xc0=float("nan"))),
                 ("Xc0 = -10", rp.solve(Xc0=-10.0)),
                 ("Xc0 = 1e9", rp.solve(Xc0=1e9))]
    for label, r in cases:
        drift = abs(r["Xc"] / Xc - 1.0) if r["converged"] else float("nan")
        print(f"    {label:12s} converged={r['converged']!s:5s} "
              f"residual={r['residual']:.2e}" +
              (f"  X_c drift {drift:.1e}" if r["converged"] else ""))
        assert r["converged"] == bool(r["residual"] < 1e-10), label
        if r["converged"]:
            # an extreme but legal start must land on the SAME radius
            assert drift < 1e-10, (label, drift)
    assert not cases[0][1]["converged"] and not cases[1][1]["converged"]
    print("[ok] 0 dishonest flags in 4 cases; extreme legal starts land on the same "
          "X_c to better than 1e-10 relative")


def test_negative_e_inside_the_support_is_caught_on_both_paths():
    """SOUNDNESS. A state that has left the support is now loud on BOTH paths.

    This was the gate that scoped leg 107's finding to EVALUATION rather than to the
    solver: `residual` on a sign-flipped state is ~14 decades above the clean one and
    `solve`'s line search refuses the step outright, while `omega_of` came back with a
    plausible number. The Newton path is deliberately unchanged by the repair (it is the
    objective the banked X_c and ||A|| were computed from), so this gate now checks the
    equation path is exactly as loud as it was AND that the evaluation path has stopped
    being silent.
    """
    print("\n[9] SOUNDNESS: e < 0 inside the support, on both paths")
    rp, b, Xc = _solved(0.3)
    bneg = b.copy()
    bneg[0] *= -1.0
    e_min = float(rp.e_of(bneg).min())
    om, nw = _caught(lambda: float(rp.omega_of(bneg, np.array([0.5]))[0]))
    om_leg, _ = _caught(
        lambda: float(rp.omega_of(bneg, np.array([0.5]), on_outside="extrapolate")[0]))
    m, nw_mass = _caught(lambda: rp.mass(bneg, Xc))
    res = float(np.max(np.abs(rp.residual(bneg, Xc))))
    clean = float(np.max(np.abs(rp.residual(b, Xc))))
    print(f"    min e at nodes {e_min:.4f} (<0)")
    print(f"    omega_of(0.5) = {om:+.4e} ({nw} warning); legacy {om_leg:+.4e}")
    print(f"    mass = {m:+.6f} ({nw_mass} warning)")
    print(f"    residual {res:.3e} vs clean {clean:.2e}  ({res / clean:.1e}x)")
    assert e_min < 0.0
    assert nw >= 1 and nw_mass >= 1, (nw, nw_mass)     # no longer silent
    assert om_leg != 0.0, om_leg                       # the legacy value is still there
    assert res > 1e10 * clean, (res, clean)
    print("[ok] the equation path is still 14 decades loud AND the evaluation path now "
          "warns on both omega_of and mass")


if __name__ == "__main__":
    test_clean_reference_selfcheck()
    test_profile_is_exactly_zero_past_its_own_support()
    test_in_support_evaluation_is_untouched_by_the_guard()
    test_even_cheb_refuses_to_extrapolate_silently()
    test_defect_refuses_nan_poisoned_samples()
    test_no_silent_absorption_of_finite_poison()
    test_no_silent_corruption_from_nan_coefficients()
    test_constructor_rejects_degenerate_a()
    test_solve_never_lies_about_convergence()
    test_negative_e_inside_the_support_is_caught_on_both_paths()
    print("\nAll leg-107 adversarial gates passed: 10 SOUNDNESS gates hold. The 4 that "
          "were characterization gates now assert the repaired property and still "
          "report leg 107's pre-repair magnitude (see experiments/journal/leg_107.md).")
