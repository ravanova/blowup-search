"""Gates for solver/first_integral.py -- the first integral and the reduced profile.

Run:  .venv/bin/python test_first_integral.py       (~50 s)

Seven gates, each against something that is not this module:
  1. Gauss-Legendre against exact polynomial moments.
  2. The finite Hilbert transform against the exact airfoil family
     (1/pi) p.v. int sqrt(1-u^2) U_{n-1}(u)/(v-u) du = T_n(v).
  3. The a -> 0 limit of the first integral against the EXACT anchor.
  4. The first integral against converged profiles from an INDEPENDENT
     discretization (solver/collocation_newton), on a J-ladder.
  5. The analytic Jacobian against central differences.
  6. X_c/c from the reduced system against the same independent build's own
     zero crossing of E = c + aU.
  7. The reconstructed Omega against the ORIGINAL residual R, evaluated with an
     independent quadrature and refined so the agreement is a rate, not a number.
"""

import numpy as np

from solver.first_integral import (ReducedProfile, anchor_limit, even_cheb,
                                   first_integral_defect, gauss_legendre,
                                   graded_grid, hilbert_pv)

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   {detail}")


# ---------------------------------------------------------------------------
def test_1_gauss_legendre():
    print("\n[1] Gauss-Legendre against exact moments")
    worst = 0.0
    for n in (4, 10, 20, 32):
        x, w = gauss_legendre(n)
        for k in range(0, 2 * n):          # exact through degree 2n-1
            exact = 0.0 if k % 2 else 2.0 / (k + 1)
            worst = max(worst, abs(float(np.sum(w * x ** k)) - exact))
    check("moments exact to degree 2n-1", worst < 1e-13, f"max err {worst:.2e}")


# ---------------------------------------------------------------------------
def test_2_finite_hilbert():
    print("\n[2] finite Hilbert transform vs the exact airfoil family")
    v = np.array([0.03, 0.2, 0.5, 0.8, 0.95, 0.999])

    def cheb(kind, n, x):
        out = [np.ones_like(x), (2.0 * x if kind == "U" else x.copy())]
        for k in range(2, n + 1):
            out.append(2 * x * out[-1] - out[-2])
        return out

    prev = None
    for levels, order in ((10, 16), (16, 20), (26, 24)):
        u, w = graded_grid(levels, order)
        Uu, Uv, Tv = cheb("U", 12, u), cheb("U", 12, v), cheb("T", 12, v)
        worst = 0.0
        for n in (1, 2, 5, 8, 10):
            f_u = np.sqrt(np.maximum(0.0, 1.0 - u * u)) * Uu[n - 1]
            f_v = np.sqrt(1.0 - v * v) * Uv[n - 1]
            worst = max(worst, float(np.max(np.abs(
                hilbert_pv(u, w, f_u, f_v, v) - Tv[n]))))
        print(f"      levels={levels:3d} order={order:3d} N={u.size:5d}"
              f"  max err {worst:.3e}")
        prev = worst
    # sqrt is the WORST endpoint this module will ever see (the profiles have
    # order 1/a >= 2); if the default rule handles it, it handles them.
    check("exact family reproduced at the default rule", prev < 1e-13,
          f"{prev:.2e} at levels=26")

    # and the orders that actually occur: self-convergence to machine precision
    worst = 0.0
    for p in (2.0, 1.0 / 0.3, 4.0):
        ref = None
        for levels, order in ((8, 12), (16, 20), (26, 24)):
            u, w = graded_grid(levels, order)
            Tu, Tv2 = cheb("T", 6, u), cheb("T", 6, v)
            got = hilbert_pv(u, w, (1 - u * u) ** p * Tu[4],
                             (1 - v * v) ** p * Tv2[4], v)
            if ref is not None:
                worst = max(worst, float(np.max(np.abs(got - ref))))
            ref = got
    check("machine precision at the endpoint orders 1/a >= 2", worst < 1e-13,
          f"max drift {worst:.2e}")


# ---------------------------------------------------------------------------
def test_3_anchor_limit():
    print("\n[3] the a -> 0 limit IS the exact anchor")
    X = np.linspace(0.0, 200.0, 40001)
    got, exact = anchor_limit(X, c=0.5)
    err = float(np.max(np.abs(got - exact)))
    check("Omega = -exp(U/c) equals -1/(1+X^2)", err < 1e-15, f"max err {err:.2e}")

    # and the finite-a form converges to it at rate O(a)
    U = -0.5 * np.log(1.0 + X ** 2)
    errs = []
    for a in (0.08, 0.04, 0.02, 0.01):
        E = 0.5 + a * U
        m = E > 0
        errs.append(float(np.max(np.abs((E[m] / 0.5) ** (1.0 / a)
                                        - np.exp(U[m] / 0.5)))))
    rate = np.polyfit(np.log([0.08, 0.04, 0.02, 0.01]), np.log(errs), 1)[0]
    check("finite-a form converges to it at O(a)", 0.85 < rate < 1.15,
          f"fitted a^{rate:.3f}, errs " + " ".join(f"{e:.1e}" for e in errs))


# ---------------------------------------------------------------------------
def test_4_identity_on_independent_profiles():
    print("\n[4] the first integral on an INDEPENDENT discretization")
    from solver.collocation_newton import ACollocation
    # An EXACT identity, evaluated on an approximate profile, must show a defect
    # that is bounded by the profile's own error and vanishes at least as fast.
    # That is the gate -- not any particular number, which would only measure the
    # profile.
    ok = True
    detail = []
    for a in (0.2, 0.3):
        devs, res = [], []
        for J in (200, 400, 800):
            col = ACollocation(J=J, a=a)
            r = col.newton_gauged(c=0.5, tol=1e-14)
            om = r["Omega"]
            mask = (np.abs(om) > 1e-11) & (col.X > 0) & (col.X < 3.0)
            devs.append(first_integral_defect(om, col.V @ om, a, 0.5, mask))
            res.append(r["relres"])
        ok = ok and (devs[0] / devs[-1]) >= (res[0] / res[-1]) and devs[-1] < 1e-6
        detail.append(f"a={a}: dev " + "/".join(f"{d:.1e}" for d in devs)
                      + " falls x%.0f vs residual x%.0f" % (devs[0] / devs[-1],
                                                            res[0] / res[-1]))
    check("|Omega|/E^{1/a} constant, vanishing no slower than the profile's own "
          "residual", ok, "; ".join(detail))


# ---------------------------------------------------------------------------
def test_5_jacobian():
    print("\n[5] analytic Jacobian vs central differences")
    worst = 0.0
    for a in (0.3, 0.5):
        red = ReducedProfile(a, K=20)
        r = red.solve(Xc0=10.0)
        assert r["converged"], r
        b, Xc, h = r["b"], r["Xc"], 1e-6
        Ja = red.jacobian(b, Xc)
        Jn = np.zeros_like(Ja)
        for k in range(red.K):
            bp, bm = b.copy(), b.copy()
            bp[k] += h
            bm[k] -= h
            Jn[:, k] = (red.residual(bp, Xc) - red.residual(bm, Xc)) / (2 * h)
        Jn[:, red.K] = (red.residual(b, Xc + h) - red.residual(b, Xc - h)) / (2 * h)
        worst = max(worst, float(np.max(np.abs(Ja - Jn)) / np.max(np.abs(Ja))))
    check("matches to finite-difference accuracy", worst < 1e-8,
          f"max rel err {worst:.2e}")


# ---------------------------------------------------------------------------
def test_6_radius_cross_build():
    print("\n[6] X_c/c against the independent whole-line build")
    from solver.collocation_newton import ACollocation
    worst = 0.0
    for a in (0.3, 0.4, 0.5):
        col = ACollocation(J=1600, a=a)
        r = col.newton_gauged(c=0.5, tol=1e-14)
        E, X = 0.5 + a * (col.V @ r["Omega"]), col.X
        i = int(np.argmax(E < 0.0))
        Xc_col = (X[i - 1] + (X[i] - X[i - 1]) * E[i - 1] / (E[i - 1] - E[i])) / 0.5
        rr = ReducedProfile(a, K=64).solve(Xc0=10.0)
        assert rr["converged"], (a, rr)
        rel = abs(rr["Xc"] - Xc_col) / rr["Xc"]
        worst = max(worst, rel)
        print(f"      a={a}: reduced {rr['Xc']:.6f}  whole-line {Xc_col:.6f}"
              f"  rel {rel:.2e}")
    check("agrees to <1e-4 (v12's two builds agreed to ~1e-3)", worst < 1e-4,
          f"worst {worst:.2e}")

    # and it is grid converged in its own K
    rows = [ReducedProfile(0.3, K=K).solve(Xc0=10.0)["Xc"]
            for K in (32, 64, 128, 192)]
    print("      X_c/c over K=32/64/128/192: " + " ".join(f"{x:.9f}" for x in rows))
    spread = max(rows[1:]) / min(rows[1:]) - 1.0
    check("K-converged in the reduced basis", spread < 1e-9 and
          abs(rows[0] / rows[-1] - 1.0) < 1e-6,
          f"spread {spread:.1e} over K=64..192 (K=32 already within "
          f"{abs(rows[0] / rows[-1] - 1.0):.0e})")


# ---------------------------------------------------------------------------
def test_7_reconstruction_solves_the_original():
    print("\n[7] the reconstructed Omega solves the ORIGINAL residual R")
    a, red = 0.3, ReducedProfile(0.3, K=64)
    r = red.solve(Xc0=10.0)
    assert r["converged"], r
    b, Xc = r["b"], r["Xc"]
    u, w = red.u, red.w
    Tu, _ = even_cheb(red.K, u)
    w_u = np.abs((1.0 - u ** 2) * (Tu @ b)) ** red.p

    vq = np.linspace(0.02, 0.98, 97)                 # OFF the collocation nodes
    T, dT = even_cheb(red.K, vq)
    e = (1.0 - vq ** 2) * (T @ b)
    de = -2.0 * vq * (T @ b) + (1.0 - vq ** 2) * (dT @ b)
    Om = -np.abs(e) ** red.p
    dOm = -red.p * np.abs(e) ** (red.p - 1.0) * de
    H_om = -hilbert_pv(u, w, w_u, np.abs(e) ** red.p, vq)

    errs = []
    for n in (1001, 4001, 16001, 64001):             # U by an independent trapezoid
        vg = np.linspace(0.0, 1.0, n)
        Tg, _ = even_cheb(red.K, vg)
        w_g = np.abs((1.0 - vg ** 2) * (Tg @ b)) ** red.p
        Lg = np.zeros(n)
        Lg[:-1] = np.log((1.0 + vg[:-1]) / (1.0 - vg[:-1]))
        d = vg[:, None] - u[None, :]
        H_g = -((((w_u[None, :] - w_g[:, None]) / d) @ w) + w_g * Lg) / np.pi
        U = np.interp(vq, vg, Xc * np.concatenate(
            [[0.0], np.cumsum(0.5 * (H_g[1:] + H_g[:-1]) * np.diff(vg))]))
        errs.append(float(np.max(np.abs(Om * H_om - (1.0 + a * U) * (dOm / Xc)))))
    rate = np.polyfit(np.log([1001, 4001, 16001, 64001]), np.log(errs), 1)[0]
    print("      max|R| = " + " ".join(f"{x:.2e}" for x in errs))
    check("R -> 0 at the U-quadrature's own 2nd order", rate < -1.8 and errs[-1] < 1e-9,
          f"fitted n^{rate:.2f}, final {errs[-1]:.1e}")

    # the edge exponent that the ansatz e = (1-v^2)s implies for Omega
    worst = 0.0
    for aa in (0.25, 0.3, 0.5):
        rp = ReducedProfile(aa, K=96)
        rr = rp.solve(Xc0=10.0)
        s = np.geomspace(1e-7, 1e-4, 60)
        Om_e = np.abs(rp.omega_of(rr["b"], 1.0 - s))
        worst = max(worst, abs(np.polyfit(np.log(s), np.log(Om_e), 1)[0] - 1.0 / aa) * aa)
    check("Omega ~ (X_c - X)^{1/a} at the edge", worst < 1e-4,
          f"worst relative exponent error {worst:.1e}")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 72)
    print("solver/first_integral.py -- gates")
    print("=" * 72)
    test_1_gauss_legendre()
    test_2_finite_hilbert()
    test_3_anchor_limit()
    test_4_identity_on_independent_profiles()
    test_5_jacobian()
    test_6_radius_cross_build()
    test_7_reconstruction_solves_the_original()
    print("\n" + "=" * 72)
    print(f"{len(PASS)}/{len(PASS) + len(FAIL)} passed")
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
        raise SystemExit(1)
