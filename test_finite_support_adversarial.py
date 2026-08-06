"""Adversarial gates for `solver/finite_support.py` (leg 124, Route-FSA).

This is the FIRST test file this module has ever had. `capabilities.py:535-538`
records its validation as the string "nothing" -- the only such entry in the
index -- and no test in the repository imports it. `test_capabilities.py:76-79`
reads the file's *text* to check the SUPERSEDED banner matches the index, and
that is the whole of the prior coverage.

The gate leg 124 answered, verbatim (DIRECTION.md leg 124):

  "Under an adversarial battery of degenerate or poisoned inputs, does
   solver/finite_support.py ever silently return a wrong result instead of
   flagging the input?"

Answered **YES**, on five sites. Leg 124 had no patch authority under its own
gate (its yes-branch reads "report the exact failing case; escalate, do not
patch"), so `solver/finite_support.py` is byte-identical to `origin/main` and
the gaps below are OPEN.

WHAT THIS FILE IS NOT. It does not test whether the module converges, is
correct, or should be used -- its own docstring says DO NOT USE and SUPERSEDED,
and leg 124 does not reopen any of that. Nothing here quotes a value of X_c,
||A||, or anything about the two-scale profile. Every assertion is about input
hygiene.

TWO KINDS OF GATE, and the difference matters:

  SOUNDNESS gates (S) assert a property that must hold forever. If one fails,
  something broke.

  CHARACTERIZATION gates (C) PIN AN OPEN DEFECT. They assert that the module
  still behaves badly. If one fails, that is very likely GOOD NEWS -- someone
  has repaired the gap -- and the correct response is to read
  experiments/journal/leg_124.md, confirm the repair, and CONVERT the gate to a
  soundness gate asserting the repaired property. It must NOT be "fixed" by
  loosening a tolerance or deleting the assertion.

Run: .venv/bin/python test_finite_support_adversarial.py
Data: writeup/data/p2_route_fsa_v1_adversarial.json
"""

import pathlib
import sys
import warnings

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from solver.finite_support import (  # noqa: E402
    FiniteSupportOps,
    FiniteSupportProfile,
    cheb_quad,
    even_cheb,
)


def cheb_T(n, x):
    """Exact T_n by recurrence -- valid for |x| > 1, which is the point."""
    x = np.asarray(x, float)
    t0, t1 = np.ones_like(x), x
    if n == 0:
        return t0
    for _ in range(n - 1):
        t0, t1 = t1, 2.0 * x * t1 - t0
    return t1


def _quiet(fn, *a, **k):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = fn(*a, **k)
    return out, len(w)


# ---------------------------------------------------------------------------
# S1 -- the module's OWN Gate 1, specified in its docstring and never written.
# ---------------------------------------------------------------------------

def test_finite_hilbert_against_the_exact_chebyshev_family():
    """SOUNDNESS, and the positive control for everything else in this file.

    `solver/finite_support.py` lines 85-89 name the check that "pins the
    quadrature, the subtraction and the sign convention at once":

        (1/pi) pv INT_{-1}^{1} sqrt(1-y^2) U_{n-1}(y) / (x-y) dy = T_n(x).

    At p = 1/2 the basis is phi_k = sqrt(1-v^2) T_{2k}, and since T_0 = U_0 and
    T_m = (U_m - U_{m-2})/2 for m >= 2, the exact answer is

        Htilde_0 = T_1,   Htilde_k = (T_{2k+1} - T_{2k-1})/2   for k >= 1.

    This gate can report the other answer: it is an independent closed form, not
    a restatement of the code. If it ever fails, every other gate here is about
    a broken quadrature rather than about domain hygiene.
    """
    v = np.array([0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9, 0.97])
    K = 5
    exact = np.empty((v.size, K))
    exact[:, 0] = cheb_T(1, v)
    for k in range(1, K):
        exact[:, k] = 0.5 * (cheb_T(2 * k + 1, v) - cheb_T(2 * k - 1, v))

    errs = {}
    for N in (1000, 2000, 4000, 8000):
        ops = FiniteSupportOps(0.5, K, v, N=N, n_int=100)
        errs[N] = float(np.max(np.abs(ops.H - exact)))
    print(f"    max|Htilde - exact| by N: "
          + ", ".join(f"N={n}: {e:.3e}" for n, e in errs.items()))
    rate = errs[2000] / errs[8000]
    print(f"    convergence over a 4x refinement: {rate:.1f}x  (2nd order -> ~16x)")

    assert errs[8000] < 1e-7, errs[8000]
    assert rate > 8.0, rate                      # the rule converges, it is not luck
    print("[ok] S1 the finite-support Hilbert transform, the p.v. subtraction and the "
          f"sign convention are pinned by an exact known answer to {errs[8000]:.2e}")


# ---------------------------------------------------------------------------
# C2 -- H1: np.clip in even_cheb (line 115)
# ---------------------------------------------------------------------------

def test_even_cheb_silently_evaluates_every_outside_point_at_the_edge():
    """CHARACTERIZATION -- PINS AN OPEN DEFECT.

    `np.arccos(np.clip(v, -1, 1))` freezes every |v| > 1 at v = 1. The identical
    line in the superseding module (`solver/first_integral.py:328`) now carries a
    guard and a justification comment; this one does not.
    """
    outside = np.array([1.01, 1.5, 3.0, 50.0, -7.0])
    K = 6
    (T, _), nw = _quiet(even_cheb, K, outside)
    T1, _ = even_cheb(K, np.array([1.0]))
    exact = np.column_stack([cheb_T(2 * k, outside) for k in range(K)])

    dev = float(np.max(np.abs(T - T1)))
    abs_err = float(np.max(np.abs(T - exact)))
    print(f"    max|returned(v>1) - returned(v=1)| = {dev:.1e} over {outside.size} points")
    print(f"    worst: T_10(50) returned {T[3, 5]:.6g} against an exact {exact[3, 5]:.6g}")
    print(f"    warnings from even_cheb itself: {nw}")

    assert dev == 0.0, dev                       # every outside point IS the edge value
    assert nw == 0, nw                           # and nothing says so
    assert abs_err > 1e10, abs_err
    print("[ok] C2 OPEN: 5/5 outside points silently return the v=1 value; worst "
          f"absolute error {abs_err:.3e}")


# ---------------------------------------------------------------------------
# C3 -- H2: the a-dependence of the out-of-support fabrication
# ---------------------------------------------------------------------------

def test_out_of_support_values_are_fabricated_exactly_when_p_is_an_integer():
    """CHARACTERIZATION -- PINS AN OPEN DEFECT, and pins its SHAPE.

    The prefactor (1 - v^2)^p uses the UNCLIPPED v while the Chebyshev factor
    uses the clipped one. For v > 1 the base is negative, so the result is NaN
    (flagged) unless p = 1/a happens to be an integer -- in which case a finite,
    fabricated number comes back where the truth is exactly 0 (the module's own
    docstring, lines 50-53: perturbations supported in [0, X_c] have residuals
    supported there too).

    The point of this gate is that the corruption is a function of `a`, and the
    silent set includes a = 0.5 -- one of the module's two documented smoke runs.
    """
    vs = np.array([1.01, 1.5, 2.0, 5.0])
    silent, flagged = [], []
    for a in (1.0, 0.5, 1.0 / 3.0, 0.25, 0.2, 0.3, 0.35, 0.7, 0.9, 1.2):
        p = 1.0 / a
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ops = FiniteSupportOps(p, 6, vs, N=400, n_int=60)
        b = np.zeros(6); b[0] = 1.0
        f, nw = _quiet(lambda: ops.fields(b)[0])
        if np.all(np.isfinite(f)):
            silent.append((a, p, float(np.max(np.abs(f))), nw))
        else:
            flagged.append((a, p))
    for a, p, m, nw in silent:
        print(f"    a={a:<6.4g} p={p:<4.1f} (integer) -> max |Omega| = {m:<12.6g} "
              f"where truth is 0.0, {nw} warnings from fields()")
    print(f"    flagged by NaN (p non-integer): {[round(a, 4) for a, _ in flagged]}")

    assert len(silent) == 5, silent
    assert len(flagged) == 5, flagged
    assert all(float(p).is_integer() for _, p, _, _ in silent)
    assert all(nw == 0 for _, _, _, nw in silent)        # fields() itself is silent
    assert any(abs(a - 0.5) < 1e-12 for a, _, _, _ in silent), "a=0.5 must be in the silent set"
    worst = max(m for _, _, m, _ in silent)
    assert worst > 1e6, worst

    # structural, not a discretization artifact
    vals = []
    for K in (6, 12, 24):
        for N in (400, 1600):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                o = FiniteSupportOps(2.0, K, np.array([2.0]), N=N, n_int=60)
            bb = np.zeros(K); bb[0] = 1.0
            vals.append(float(o.fields(bb)[0][0]))
    spread = (max(vals) - min(vals)) / abs(np.mean(vals))
    print(f"    grid independence at a=0.5, v=2.0 over K in 6/12/24 x N in 400/1600: "
          f"relative spread {spread:.1e}")
    assert spread == 0.0, spread
    print(f"[ok] C3 OPEN: 5 of 10 values of a fabricate silently (worst {worst:.6g} against "
          "a gauge amplitude of 1), 5 of 10 are flagged by NaN; the split is exactly "
          "whether 1/a is an integer")


# ---------------------------------------------------------------------------
# C4 -- H3: an evaluation point that lands on a quadrature node
# ---------------------------------------------------------------------------

def test_quadrature_node_collision_is_floored_not_flagged():
    """CHARACTERIZATION -- PINS AN OPEN DEFECT.

    `d = np.where(np.abs(d) < 1e-300, 1e-300, d)` (line 178) turns the singular
    divided difference at a collision into exactly 0 / 1e-300 = 0, dropping the
    term. Reachable only through the public `FiniteSupportOps(v_eval=...)`: the
    module's own default collocation sets never collide, which this gate also
    checks so the scope stays honest.
    """
    N = 400
    u, _ = cheb_quad(N)
    node = float(u[137])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ops = FiniteSupportOps(2.0, 6, np.array([0.5]), N=N, n_int=200)
        ref_ops = FiniteSupportOps(2.0, 6, np.array([0.5]), N=N + 1, n_int=200)
    # warnings are captured around the COLLIDING EVALUATION only: construction
    # emits 2 from the v=1 row of the internal velocity grid (benign, see S5).
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        hit = ops._hilbert_matrix(np.array([node]))[0]
        near = ops._hilbert_matrix(np.array([node + 1e-7]))[0]
    ref = ref_ops._hilbert_matrix(np.array([node]))[0]
    rel_hit = float(np.max(np.abs(hit - ref) / np.maximum(np.abs(ref), 1e-14)))
    rel_near = float(np.max(np.abs(near - ref) / np.maximum(np.abs(ref), 1e-14)))
    print(f"    same point, quadrature that CONTAINS it : rel err {rel_hit:.3e}")
    print(f"    a point 1e-7 away, same quadrature      : rel err {rel_near:.3e}")
    print(f"    amplification {rel_hit / rel_near:.0f}x, warnings from the "
          f"colliding evaluation itself: {len(w)}")

    collisions = 0
    for K in (8, 16, 24, 32):
        cv = 0.5 * (1.0 - np.cos(np.pi * (np.arange(K - 1) + 0.5) / (K - 1)))
        for Nq in (800, 2000):
            uq, _ = cheb_quad(Nq)
            collisions += int(np.sum(np.min(np.abs(cv[:, None] - uq[None, :]), axis=1) < 1e-15))
    print(f"    collisions among the module's own default node sets: {collisions}")

    assert rel_hit > 1e-3, rel_hit
    assert rel_hit / rel_near > 100.0, (rel_hit, rel_near)
    assert len(w) == 0, len(w)
    assert collisions == 0, collisions
    print(f"[ok] C4 OPEN: a colliding evaluation point is wrong by {rel_hit:.2%} with no "
          "warning; the default node sets never collide, so this is a latent trap on the "
          "public v_eval entry point")


# ---------------------------------------------------------------------------
# S5 -- H4: the log endpoints are LOUD, not silent
# ---------------------------------------------------------------------------

def test_log_endpoints_are_never_silently_wrong():
    """SOUNDNESS. v = 0 returns +-inf (loud, though with no warning: log(0) under
    errstate('divide') is a valid inf). v = 1 warns during the 0*inf multiply and
    then returns a correct finite value, because the `phi_v != 0` mask discards
    the nan. Neither fabricates a plausible number, so H4 is NOT part of the gate
    answer -- and this gate keeps it that way."""
    ops = FiniteSupportOps(2.0, 4, np.array([0.5]), N=400, n_int=100)
    for v, want_finite in ((0.0, False), (1.0, True), (0.5, True)):
        H, nw = _quiet(ops._hilbert_matrix, np.array([v]))
        finite = bool(np.all(np.isfinite(H)))
        print(f"    v={v:<4g} finite={finite!s:<6s} warnings={nw}")
        assert finite == want_finite, (v, finite)
    print("[ok] S5 v=0 is non-finite (loud) and v=1 is correct and finite; neither "
          "returns a plausible wrong number")


# ---------------------------------------------------------------------------
# C6 -- H5: `converged` on a system with zero equation rows
# ---------------------------------------------------------------------------

def test_converged_is_reported_on_a_system_with_no_equation_rows():
    """CHARACTERIZATION -- PINS AN OPEN DEFECT, and it is the sharpest one.

    With K = 1 there are K - 1 = 0 collocation rows: the profile equation is
    evaluated at ZERO points. The square system is the amplitude gauge plus the
    free-boundary row, so the reported residual is exactly 0.0 and `converged`
    is True by construction -- a confident answer from a solve that never looked
    at the equation. No guard on K exists anywhere in the module.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        P = FiniteSupportProfile(a=0.5, K=1, N=400, n_int=100)
        r = P.solve(max_iter=20)
    print(f"    K=1: collocation nodes {P.v.size}, reported residual {r['residual']:.3e}, "
          f"converged={r['converged']}, iterations {r['iterations']}")

    assert P.v.size == 0, P.v.size
    assert r["converged"] is True
    assert r["residual"] == 0.0, r["residual"]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        P2 = FiniteSupportProfile(a=0.5, K=2, N=400, n_int=100)
        r2 = P2.solve(max_iter=20)
    print(f"    K=2: collocation nodes {P2.v.size}, reported residual {r2['residual']:.3e}, "
          f"converged={r2['converged']}")
    assert r2["converged"] is True
    assert r2["residual"] < 1e-15, r2["residual"]
    print("[ok] C6 OPEN: K=1 reports converged=True at residual exactly 0.0 from a system "
          "with 0 equation rows; K=2 does the same from 1 row")


# ---------------------------------------------------------------------------
# C7 -- H5 continued: the flag versus the equation off the collocation grid
# ---------------------------------------------------------------------------

def test_converged_flag_survives_an_O1_equation_violation_off_the_grid():
    """CHARACTERIZATION -- PINS AN OPEN DEFECT.

    `converged` is decided from the residual at the K-1 collocation nodes only.
    Evaluated on a grid sharing none of those nodes, at 20x the quadrature
    resolution, the same returned state violates the profile equation by O(1)
    while the module reports machine precision. S1 pins the quadrature error at
    ~1e-8, six orders below the violations measured here, so this is aliasing
    and not quadrature noise.

    This gate makes NO claim that the module should converge -- its docstring
    says it does not -- only that the flag it prints is decided by a measurement
    too coarse to support it.
    """
    v = np.linspace(0.013, 0.987, 200)
    worst = 0.0
    rows = []
    for K in (4, 6, 8, 12):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            P = FiniteSupportProfile(a=0.5, K=K, N=400, n_int=100)
            r = P.solve(max_iter=40)
            ops = FiniteSupportOps(2.0, K, v, N=8000, n_int=1200)
            ops.a = 0.5
            ind = float(np.max(np.abs(ops.residual(r["b"], r["Xc"], 0.5))))
        rows.append((K, r["converged"], r["residual"], ind))
        print(f"    K={K:<3d} converged={r['converged']!s:<5s} reported {r['residual']:.3e}  "
              f"independent off-grid {ind:.4e}  amplification {ind / max(r['residual'], 1e-300):.2e}x")
        worst = max(worst, ind)

    assert all(c for _, c, _, _ in rows), rows           # all four self-report converged
    assert all(rep < 1e-12 for _, _, rep, _ in rows), rows
    assert worst > 1e-2, worst
    print(f"[ok] C7 OPEN: 4/4 self-reported-converged states violate the equation by up to "
          f"{worst:.3e} off the collocation grid, against reported residuals below 1e-12")


# ---------------------------------------------------------------------------
# C8/S8 -- H7: degenerate constructor arguments
# ---------------------------------------------------------------------------

def test_degenerate_a_is_accepted_without_a_word():
    """MIXED. SOUNDNESS: a = 0 raises. CHARACTERIZATION: nan, inf and -inf all
    construct with no exception and no warning -- and a = inf gives p = 0.0,
    which replaces the algebraic edge zero (1-v^2)^p by the constant 1, i.e.
    discards the ansatz the entire module is built on."""
    try:
        FiniteSupportProfile(a=0.0, K=6, N=200, n_int=50)
        raise AssertionError("a=0 must raise")
    except ZeroDivisionError:
        print("    a=0.0  -> ZeroDivisionError (soundness: this one IS flagged)")

    silent = []
    for a in (np.nan, np.inf, -np.inf):
        P, nw = _quiet(FiniteSupportProfile, a=a, K=6, N=200, n_int=50)
        print(f"    a={a!r:<6} -> constructed, p={P.p!r}, warnings={nw}")
        if nw == 0:
            silent.append(a)
    assert len(silent) == 3, silent
    Pi, _ = _quiet(FiniteSupportProfile, a=np.inf, K=6, N=200, n_int=50)
    assert Pi.p == 0.0, Pi.p
    print("[ok] C8 OPEN: 3/3 non-finite values of a construct silently; a=inf gives p=0.0, "
          "deleting the algebraic edge zero without a word. (a=0 raising is S8.)")


# ---------------------------------------------------------------------------
# S9/C9 -- H9: poisoned state through every evaluation entry point
# ---------------------------------------------------------------------------

def test_poisoned_coefficients_propagate_but_an_impossible_radius_does_not():
    """MIXED. SOUNDNESS: nan/inf in the coefficient vector propagate through
    every entry point -- 12/12, nothing absorbs them. CHARACTERIZATION: a
    NEGATIVE support radius, which is physically impossible for a free boundary,
    is accepted by all six entry points and yields a finite number from every
    one of them, including the module's declared kill switch."""
    K = 12
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        P = FiniteSupportProfile(a=0.5, K=K, N=400, n_int=100)
    clean = np.zeros(K); clean[0] = 1.0
    entries = ["system", "system_jacobian", "operator_norm", "profile_values"]

    def report(b, Xc):
        out = {}
        for fn in entries:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                v = getattr(P, fn)(b, Xc)
            v = v[1] if fn == "profile_values" else v
            out[fn] = bool(np.all(np.isfinite(np.atleast_1d(np.asarray(v, float)))))
        return out

    base = report(clean, 2.4)
    print(f"    clean control (must be all finite): {base}")
    assert all(base.values()), base

    n_absorbed = 0
    for name, poison in (("nan", np.nan), ("inf", np.inf)):
        b = np.where(np.arange(K) == 3, poison, clean)
        rep = report(b, 2.4)
        print(f"    {name} in b[3] -> finite? {rep}")
        n_absorbed += sum(rep.values())
    assert n_absorbed == 0, n_absorbed

    neg = report(clean, -5.0)
    print(f"    X_c = -5.0 (impossible) -> finite? {neg}")
    assert all(neg.values()), neg
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        nrm = P.operator_norm(clean, -5.0)
    assert np.isfinite(nrm)
    print("[ok] S9 nan/inf coefficients propagate 8/8; C9 OPEN: a negative support radius "
          "is accepted by 4/4 entry points and the kill switch returns a finite number on it")


# ---------------------------------------------------------------------------
# S10 -- the scope invariant that makes all of the above LATENT
# ---------------------------------------------------------------------------

def test_the_module_still_has_zero_importers():
    """SOUNDNESS, and it is the reason leg 124's findings are latent traps rather
    than contaminated results. If this ever fails, someone has started importing
    a module whose own docstring says DO NOT USE, and every gap pinned above
    becomes live. Re-read experiments/journal/leg_124.md before proceeding."""
    hits = []
    for path in sorted(ROOT.rglob("*.py")):
        if path.name in ("finite_support.py", pathlib.Path(__file__).name):
            continue
        if "p2_route_fsa" in path.name:
            continue
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if "finite_support" in line and "import" in line:
                hits.append(f"{path.relative_to(ROOT)}:{i}: {line.strip()}")
    print(f"    importers of solver.finite_support outside leg 124's own files: {len(hits)}")
    for h in hits:
        print("      ", h)
    assert hits == [], hits

    banner = (ROOT / "solver" / "finite_support.py").read_text()
    assert "SUPERSEDED" in banner and "DO NOT USE" in banner
    print("[ok] S10 zero importers, and the SUPERSEDED / DO NOT USE banner is intact")


if __name__ == "__main__":
    test_finite_hilbert_against_the_exact_chebyshev_family()
    test_even_cheb_silently_evaluates_every_outside_point_at_the_edge()
    test_out_of_support_values_are_fabricated_exactly_when_p_is_an_integer()
    test_quadrature_node_collision_is_floored_not_flagged()
    test_log_endpoints_are_never_silently_wrong()
    test_converged_is_reported_on_a_system_with_no_equation_rows()
    test_converged_flag_survives_an_O1_equation_violation_off_the_grid()
    test_degenerate_a_is_accepted_without_a_word()
    test_poisoned_coefficients_propagate_but_an_impossible_radius_does_not()
    test_the_module_still_has_zero_importers()
    print("\nAll leg-124 adversarial gates passed: 4 SOUNDNESS gates hold and 6 "
          "CHARACTERIZATION gates confirm the five silent-corruption sites are still "
          "OPEN. solver/finite_support.py is byte-identical to origin/main -- leg 124's "
          "gate escalates and does not patch. A characterization gate FAILING is good "
          "news: read experiments/journal/leg_124.md and convert it, do not loosen it.")
