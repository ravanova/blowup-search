"""Leg 87 / Route-IVB: the PERMANENT post-repair regression suite for solver/interval.py.

WHY THIS FILE EXISTS, ALONGSIDE `test_interval_stress.py`.  Leg 69 found two real soundness
defects in the shared interval core and a bench-repair agent fixed both.  `test_interval_stress.py`
was then rewritten BY THAT REPAIR to assert the repaired behaviour -- so it is the repair marking
its own homework.  This file is the INDEPENDENT re-derivation (leg 87), and it gates three things
that the repair's own suite does not:

  1. **The eta constants against the extremal case, not against random data.**  The repair
     carries 2.0 eta per accumulated term on the plain path and 8.0 on the compensated one.
     Random subnormal data never approaches either.  `test_eta_constants_cover_the_extremal_case`
     constructs, in closed form, data whose absolute accumulation error is exactly m*eta/2 --
     Rump (BIT Numer. Math. 52:201-220, 2012) Thm 4.3 attained WITH EQUALITY -- and pins the
     resulting margins at 4x (plain) and 16x (compensated).  If anyone ever shrinks those
     constants, this is the test that notices.

  2. **The Dekker wall in BOTH operands and under product overflow.**  Leg 69 and the repair
     probed `a = 2^e, b = 1`.  The splitting is applied to both operands and the product can
     overflow independently of either.  `test_dekker_wall_is_closed_in_both_operands` sweeps the
     (e_a, e_b) grid and requires every cell to either RAISE or enclose the exact rational
     product -- never a silent NaN, never a miss.

  3. **That the repair is never NARROWER than what it replaced.**  A widening is sound; a
     narrowing would be a regression that no containment test can see, because a narrower
     enclosure that still happens to contain the answer passes every containment check.
     `test_post_repair_is_never_narrower_than_pre_repair` reconstructs the PRE-repair module from
     git and diffs endpoint bit patterns.  Measured at the time of writing: on the live
     `bordered_linearization` (K = 16..128) the uncancelled enclosures are bit-identical, the
     catastrophically-cancelled ones are 1-2 ulp WIDER, and NOTHING is narrower.

Everything is decided against EXACT RATIONAL ground truth (`fractions.Fraction` on exact float64
inputs), so containment is decided exactly rather than numerically.  Magnitudes are printed, not
booleans.

Do not weaken these to make a future change look harmless.
"""

import os
import subprocess
import sys
import types
import warnings
from fractions import Fraction as Fr

import numpy as np

from solver.interval import (
    Interval, dot2_matvec, matvec, _two_product, _ETA_TERMS_PLAIN, _ETA_TERMS_DOT2,
)

ETA = 2.0 ** -1074
ROOT = os.path.dirname(os.path.abspath(__file__))

# Rump, BIT 2012, Thm 4.3:  |s~_n - x^T y| < (n+2) u ufp(S~_n) + n eta/2.
# The published absolute underflow coefficient is 0.5 eta per accumulated term.
RUMP_PLAIN_ETA_PER_TERM = 0.5

warnings.simplefilter("ignore")


# --------------------------------------------------------------------------

def _exact(M, v):
    return [sum(Fr(M[i, j]) * Fr(v[j]) for j in range(M.shape[1]))
            for i in range(M.shape[0])]


def _cancel_row(row, v):
    """Two exact-float columns cancelling a row's exact dot product to ~1e-32 relative, with every
    stored number still exactly representable (which is what keeps the ground truth exact)."""
    S = sum(Fr(row[j]) * Fr(v[j]) for j in range(len(v)))
    h = float(S)
    return np.array([-h, -float(S - Fr(h))], dtype=float)


def _slack(lo, hi, ex):
    """(contained, relative slack, headroom in units of eta) against the exact rational."""
    lof, hif = float(lo), float(hi)
    assert not (np.isnan(lof) or np.isnan(hif)), "a NaN endpoint was stored in an enclosure"
    if np.isinf(lof) or np.isinf(hif):
        return True, None, float("inf")
    L, H = Fr(lof), Fr(hif)
    s = min(ex - L, H - ex)
    w = H - L
    try:
        head = float(s / Fr(ETA))
    except (OverflowError, ValueError):
        head = float("inf") if s > 0 else float("-inf")
    return s >= 0, (float(s / w) if w > 0 else 0.0), head


# --------------------------------------------------------------------------

def test_leg69_failing_band_is_closed():
    """(1) GATE CLAUSE (a), defect 1.  The exact band leg 69 measured failing -- input scales
    1e-145 to 1e-175, both reductions -- must now contain the exact rational value in every case.

    Leg 69 measured 62 false negatives in 1680 cases here, worst escape 6.58 eta = 3.25e-323.
    This re-derivation sweeps the band at FOUR accumulation lengths (leg 69 used one, m = 64),
    because the absolute term scales with m and a constant that is right at m = 64 can still be
    wrong at m = 258."""
    rng = np.random.default_rng(87)
    total = 0
    fails = []
    worst_escape = 0.0
    min_head = np.inf
    for e in (-145, -150, -155, -160, -165, -170, -175):
        for m in (8, 64, 258):
            base = rng.standard_normal((1, m))
            v0 = rng.standard_normal(m)
            ext = _cancel_row(base[0], v0)
            M = np.concatenate([base, ext[None, :]], axis=1) * (10.0 ** e)
            v = np.concatenate([v0, [1.0, 1.0]]) * (10.0 ** e)
            ex = _exact(M, v)[0]
            for name, r in (("dot2_matvec", dot2_matvec(M, v)),
                            ("matvec", matvec(M, Interval.point(v)))):
                ok, _, head = _slack(r.lo[0], r.hi[0], ex)
                total += 1
                min_head = min(min_head, head)
                if not ok:
                    fails.append((name, e, m, -head))
                    worst_escape = max(worst_escape, -head)
    assert not fails, (
        f"{len(fails)}/{total} false negatives in leg 69's failing band, worst escape "
        f"{worst_escape:.4g} eta -- the absolute (eta) term no longer covers the underflow "
        f"rounding.  First few: {fails[:5]}")
    print(f"    0/{total} false negatives across scales 1e-145..1e-175, m = 8/64/258, both "
          f"reductions; minimum containment headroom {min_head:.4g} eta "
          f"(leg 69 measured 62/1680 here, worst escape 6.58 eta)")
    print("[ok] leg 69's subnormal failure band is closed")


def test_eta_constants_cover_the_extremal_case():
    """(2) GATE CLAUSE (a), defect 1, SHARPENED -- the constants against the worst case that
    exists, not against random data.

    Construction: M_ij = eta exactly, v_j = c_j + 1/2 with all c_j of the SAME parity.  Each exact
    product (c_j + 1/2) * eta lands precisely halfway between two representable subnormals, so
    round-half-to-even rounds it the same way for every j, and sums of integer multiples of eta
    are exact while subnormal.  The absolute accumulation error is therefore exactly

        m * eta / 2,

    which is Rump Thm 4.3's n*eta/2 attained with EQUALITY.  The measured demand is 0.5 eta per
    term, so the implemented 2.0 and 8.0 carry exactly 4x and 16x margin.  Both are asserted:
    soundness (the enclosure still contains) AND the margin (so a future shrink is caught)."""
    demands = {}
    margins = {}
    min_head = {}
    for m in (4, 16, 64, 128, 258):
        for base in (0, 1):                       # both tie-break directions
            c = np.arange(base, base + 2 * m, 2, dtype=float)
            v = c + 0.5
            M = np.full((1, m), ETA)
            ex = _exact(M, v)[0]
            for name, r, impl in (("dot2_matvec", dot2_matvec(M, v), _ETA_TERMS_DOT2),
                                  ("matvec", matvec(M, Interval.point(v)), _ETA_TERMS_PLAIN)):
                ok, _, head = _slack(r.lo[0], r.hi[0], ex)
                assert ok, (f"{name} LOST the exact value on the extremal half-eta case at "
                            f"m={m}, parity={base}: escape {-head:.4g} eta")
                L, H = Fr(float(r.lo[0])), Fr(float(r.hi[0]))
                demand = abs(float((ex - (L + H) / 2) / Fr(ETA))) / m
                demands[name] = max(demands.get(name, 0.0), demand)
                if demand > 0:
                    margins[name] = min(margins.get(name, np.inf), impl / demand)
                min_head[name] = min(min_head.get(name, np.inf), head)
    # the construction must actually attain the published bound, or it is not the extremal case
    assert abs(demands["matvec"] - RUMP_PLAIN_ETA_PER_TERM) < 1e-12, (
        f"the extremal construction measured {demands['matvec']} eta/term, not the "
        f"{RUMP_PLAIN_ETA_PER_TERM} eta/term of Rump Thm 4.3 -- the construction, not the module, "
        "is what this assertion is checking")
    assert margins["matvec"] >= 4.0 - 1e-9, (
        f"the plain path's eta constant fell to {margins['matvec']:.4g}x the extremal demand "
        f"(was 4x at _ETA_TERMS_PLAIN = 2.0)")
    assert margins["dot2_matvec"] >= 16.0 - 1e-9, (
        f"the compensated path's eta constant fell to {margins['dot2_matvec']:.4g}x the extremal "
        f"demand (was 16x at _ETA_TERMS_DOT2 = 8.0)")
    print(f"    extremal demand {demands['matvec']:.4g} eta/term (Rump Thm 4.3's n*eta/2, "
          f"attained with equality); implemented {_ETA_TERMS_PLAIN} plain / {_ETA_TERMS_DOT2} "
          f"dot2 = {margins['matvec']:.4g}x / {margins['dot2_matvec']:.4g}x margin; minimum "
          f"headroom {min(min_head.values()):.4g} eta")
    print("[ok] both eta constants dominate the worst case that exists, with measured margin")


def test_dekker_wall_is_closed_in_both_operands():
    """(3) GATE CLAUSE (a), defect 2, WIDENED.  Leg 69 probed `a = 2^e, b = 1` only; the splitting
    is applied to BOTH operands and the product can overflow independently of either.

    Every cell of the (e_a, e_b) x (sign, sign) grid must either RAISE OverflowError or return an
    enclosure containing the exact rational product.  A `[nan, nan]` return is the original defect;
    a finite enclosure missing the product is worse."""
    exps = [0, 500, 900, 996, 997, 1000, 1023]
    cells = raised = enclosed = 0
    holes = []
    for ea in exps:
        for eb in exps:
            for sa, sb in ((1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)):
                cells += 1
                ex = Fr(sa * sb) * (Fr(2) ** (ea + eb))
                try:
                    r = dot2_matvec(np.array([[sa * 2.0 ** ea]]), np.array([sb * 2.0 ** eb]))
                except OverflowError:
                    raised += 1
                    continue
                lo, hi = float(r.lo[0]), float(r.hi[0])
                if np.isnan(lo) or np.isnan(hi):
                    holes.append(("silent NaN", ea, eb, sa, sb))
                    continue
                if Fr(lo) <= ex <= Fr(hi):
                    enclosed += 1
                else:
                    holes.append(("missed", ea, eb, sa, sb, repr(lo), repr(hi)))
    assert not holes, f"{len(holes)} Dekker-wall holes: {holes[:5]}"
    # the wall itself, located independently in each operand
    def wall(slot):
        for e in range(900, 1024):
            try:
                if slot == 0:
                    _two_product(np.array([2.0 ** e]), np.array([1.0]))
                else:
                    _two_product(np.array([1.0]), np.array([2.0 ** e]))
            except OverflowError:
                return e
        return None
    wa, wb = wall(0), wall(1)
    assert wa == 997 and wb == 997, (
        f"the Dekker wall moved: operand a at 2^{wa}, operand b at 2^{wb}; leg 69 measured "
        f"2^997 = {2.0 ** 997:.6g} and the splitting constant 2^27+1 has not changed")
    # one binade below, the compensated path must still answer, and answer soundly
    r = dot2_matvec(np.array([[2.0 ** 996]]), np.array([1.0]))
    assert Fr(float(r.lo[0])) <= Fr(2) ** 996 <= Fr(float(r.hi[0])), \
        "the compensated path stopped enclosing one binade below the wall"
    print(f"    {cells} (e_a, e_b, sign, sign) cells: {raised} raised, {enclosed} enclosed the "
          f"exact rational product, 0 silent NaN, 0 missed; wall at 2^{wa} in operand a and "
          f"2^{wb} in operand b; 2^996 still encloses")
    print("[ok] the Dekker overflow wall is closed in both operands and under product overflow")


def test_nan_widening_is_sound_and_isolating():
    """(4) The NaN path.  A NaN endpoint must never be STORED (the pre-repair `np.any(lo > hi)`
    invariant guard was vacuous on NaN, since every comparison against NaN is False).  A NaN
    arriving in CALLER data -- `interval_certificate.full_interpolant_hilbert_matrix` leaves two
    endpoint rows NaN on purpose -- must widen to the trivial enclosure and must not damage the
    other rows of the same matvec."""
    stored = 0
    for a, b in ((np.nan, np.nan), (np.nan, 1.0), (0.0, np.nan),
                 (-np.inf, np.nan), (np.nan, np.inf)):
        w = Interval(np.array([a]), np.array([b]))
        stored += int(np.isnan(w.lo[0]) or np.isnan(w.hi[0]))
        assert w.lo[0] == -np.inf and w.hi[0] == np.inf, f"({a}, {b}) not widened to entire"
        assert bool(w.contains(0.0)) and bool(w.contains(1e300)), "entire must contain everything"
    ent = Interval(np.array([-np.inf]), np.array([np.inf]))
    for label, r in (("entire - entire", ent - ent),
                     ("entire * zero", ent * Interval.point(np.array([0.0]))),
                     ("entire * entire", ent * ent)):
        stored += int(np.isnan(r.lo[0]) or np.isnan(r.hi[0]))
        assert not (np.isnan(r.lo[0]) or np.isnan(r.hi[0])), f"{label} stored a NaN endpoint"
    assert stored == 0, f"{stored} NaN endpoints were stored"
    M = np.array([[np.nan, 1.0], [2.0, 3.0], [np.nan, np.nan]])
    r = dot2_matvec(M, np.array([1.0, 1.0]))
    assert r.lo[0] == -np.inf and r.hi[0] == np.inf, "NaN row 0 did not widen"
    assert r.lo[2] == -np.inf and r.hi[2] == np.inf, "all-NaN row 2 did not widen"
    ok, _, _ = _slack(r.lo[1], r.hi[1], Fr(5))
    assert ok and np.isfinite(r.lo[1]), "the clean row was damaged by its NaN neighbours"
    print(f"    0 NaN endpoints stored across 8 constructor and arithmetic cases; a NaN row "
          f"widens to [-inf, +inf] while its clean neighbour keeps width "
          f"{float(r.hi[1] - r.lo[1]):.3g}")
    print("[ok] NaN widening is sound and does not leak across rows")


def test_live_k_range_exact_rational_containment():
    """(5) GATE CLAUSE (b).  The regression check proper: the LIVE operator legs 58 and 61 run
    on -- `bordered_linearization(K)`, nonzero entries 0.5 to K, tail diagonal EXACTLY zero --
    checked row by row against exact rational ground truth, uncancelled AND catastrophically
    cancelled, through both reductions."""
    from solver.spectral_certificate import bordered_linearization
    rng = np.random.default_rng(58)
    n = 0
    worst = 1.0
    entry_lo, entry_hi = np.inf, 0.0
    for K in (16, 64):
        M0 = np.asarray(bordered_linearization(K), dtype=float)
        nz = np.abs(M0)[np.abs(M0) > 0]
        entry_lo = min(entry_lo, float(nz.min()))
        entry_hi = max(entry_hi, float(nz.max()))
        v0 = rng.standard_normal(M0.shape[1])
        ext = np.array([_cancel_row(M0[i], v0) for i in range(M0.shape[0])])
        for M, v in ((M0, v0),
                     (np.concatenate([M0, ext], axis=1), np.concatenate([v0, [1.0, 1.0]]))):
            ex = _exact(M, v)
            for name, r in (("dot2_matvec", dot2_matvec(M, v)),
                            ("matvec", matvec(M, Interval.point(v)))):
                for i in range(M.shape[0]):
                    ok, rel, _ = _slack(r.lo[i], r.hi[i], ex[i])
                    assert ok, f"{name} lost the exact value at K={K}, row {i}"
                    if rel is not None:
                        assert rel > 0.0, f"{name} merely TOUCHED an endpoint at K={K}, row {i}"
                        worst = min(worst, rel)
                    n += 1
    assert worst > 0.3, (f"worst relative slack fell to {worst:.4g} on the live operator; "
                         "leg 69 banked 0.4764 and leg 87 measured 0.375 over a wider corpus")
    print(f"    {n} live-operator cases at K = 16, 64 (nonzero entries {entry_lo} to {entry_hi}, "
          f"tail diagonal exactly zero), uncancelled and cancelled, both reductions; worst "
          f"relative slack {worst:.4f} (0.5 = dead centre, 0 = touching)")
    print("[ok] exact-rational containment at the live K-range, no case touching an endpoint")


def test_post_repair_is_never_narrower_than_pre_repair():
    """(6) GATE CLAUSE (b), the part no containment test can see.

    A repair that made an enclosure NARROWER would still pass every containment check whenever the
    narrower enclosure happened to keep the answer -- and would have silently eaten the rigour.
    So the pre-repair module is reconstructed from git and endpoint bit patterns are diffed.
    Three counts: identical, wider (sound -- more conservative), narrower (a regression, must be
    zero).

    Measured at the time of writing: on `bordered_linearization` K = 16..128 the UNCANCELLED
    enclosures are bit-identical pre/post, the catastrophically-CANCELLED ones are 1-2 ulp wider
    (the repair added a second outward push alongside the eta term, and on a cancelled row the
    error term IS the endpoint), and nothing anywhere is narrower."""
    subject = "repair the two soundness defects leg 69 measured in solver/interval.py"
    try:
        log = subprocess.run(["git", "-C", ROOT, "log", "--format=%H%x1f%s",
                              "--", "solver/interval.py"],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"    SKIPPED: git history unavailable ({exc})")
        return
    commit = next((l.split("\x1f")[0] for l in log.splitlines() if subject in l), None)
    if commit is None:
        print("    SKIPPED: the repair commit is not in this history (shallow clone?)")
        return
    src = subprocess.run(["git", "-C", ROOT, "show", f"{commit}^:solver/interval.py"],
                         capture_output=True, text=True, check=True).stdout
    pre = types.ModuleType("interval_prerepair")
    pre.__file__ = f"<pre-repair solver/interval.py @ {commit[:8]}^>"
    exec(compile(src, pre.__file__, "exec"), pre.__dict__)

    from solver.spectral_certificate import bordered_linearization
    rng = np.random.default_rng(69)
    bits = lambda x: np.asarray(x, dtype=float).view(np.int64)
    counts = {"endpoints": 0, "identical": 0, "wider": 0, "narrower": 0}
    uncancelled_identical = uncancelled_endpoints = 0
    max_ulp = 0
    for K in (16, 64, 128):
        M0 = np.asarray(bordered_linearization(K), dtype=float)
        v0 = rng.standard_normal(M0.shape[1])
        ext = np.array([_cancel_row(M0[i], v0) for i in range(M0.shape[0])])
        variants = [(False, M0, v0),
                    (True, np.concatenate([M0, ext], axis=1),
                     np.concatenate([v0, [1.0, 1.0]]))]
        for cancelled, M, v in variants:
            for fpre, fpost in ((pre.dot2_matvec, dot2_matvec),
                                (lambda M, v: pre.matvec(M, pre.Interval.point(v)),
                                 lambda M, v: matvec(M, Interval.point(v)))):
                a, b = fpre(M, v), fpost(M, v)
                for i in range(M.shape[0]):
                    for end in ("lo", "hi"):
                        av = float(getattr(a, end)[i])
                        bv = float(getattr(b, end)[i])
                        counts["endpoints"] += 1
                        if not cancelled:
                            uncancelled_endpoints += 1
                        if bits(av) == bits(bv):
                            counts["identical"] += 1
                            uncancelled_identical += int(not cancelled)
                        elif (end == "lo" and bv < av) or (end == "hi" and bv > av):
                            counts["wider"] += 1
                            max_ulp = max(max_ulp, abs(int(bits(bv)) - int(bits(av))))
                        else:
                            counts["narrower"] += 1
    assert counts["narrower"] == 0, (
        f"{counts['narrower']}/{counts['endpoints']} endpoints are NARROWER post-repair than "
        "pre-repair on the live operator -- the repair tightened an enclosure it had no rigorous "
        "grounds to tighten.  This is invisible to every containment test.")
    assert uncancelled_identical == uncancelled_endpoints, (
        f"only {uncancelled_identical}/{uncancelled_endpoints} UNCANCELLED live-operator "
        "endpoints are bit-identical pre/post; the repair was verified as bit-for-bit inert "
        "there, so a change means the eta term has started moving live-range bits")
    print(f"    {counts['endpoints']} live-operator endpoints vs the pre-repair source "
          f"({commit[:8]}^): {counts['identical']} identical, {counts['wider']} wider "
          f"(max {max_ulp} ulp, all on catastrophically-cancelled rows), "
          f"{counts['narrower']} narrower; uncancelled rows "
          f"{uncancelled_identical}/{uncancelled_endpoints} bit-identical")
    print("[ok] the repair only ever widened, and left the uncancelled live range untouched")


def _main():
    test_leg69_failing_band_is_closed()
    test_eta_constants_cover_the_extremal_case()
    test_dekker_wall_is_closed_in_both_operands()
    test_nan_widening_is_sound_and_isolating()
    test_live_k_range_exact_rational_containment()
    test_post_repair_is_never_narrower_than_pre_repair()
    print("\nALL POST-REPAIR REGRESSION GATES PASSED "
          "(leg 87: leg 69's defects independently re-derived as closed, no live-range regression)")


if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    _main()
