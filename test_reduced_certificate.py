"""Gates for solver/reduced_certificate.py -- the float rehearsal.

Run:  .venv/bin/python test_reduced_certificate.py       (~3 min)

Six gates.  Note what they are gating: this module's headline is a NEGATIVE (the
sup-to-sup budget does not close), and a negative needs its instrument checked harder
than a positive does -- so three of the six are about the instrument rather than the
result.
"""

import numpy as np

from solver.first_integral import ReducedProfile
from solver.reduced_certificate import (holder_ratio, holder_seminorm,
                                        interpolant_defect, rehearsal,
                                        second_derivative_sup, step_adversary,
                                        z0_defect)

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}   {detail}")


# ---------------------------------------------------------------------------
def test_1_interpolant_defect_converges():
    print("\n[1] Y_0: the interpolant defect falls to machine level")
    rows = []
    for K in (16, 32, 48, 64, 96):
        rp = ReducedProfile(0.3, K=K)
        r = rp.solve(Xc0=10.0)
        assert r["converged"], (K, r)
        rows.append(interpolant_defect(rp, r["b"], r["Xc"]))
    print("      sup|F| off-node = " + " ".join(f"{x:.2e}" for x in rows))
    check("falls by >=9 orders and reaches <1e-10", rows[0] / rows[-1] > 1e9
          and rows[-1] < 1e-10, f"{rows[0]:.1e} -> {rows[-1]:.1e}")
    # and it must be much larger than the NODAL residual, or we are measuring nothing
    rp = ReducedProfile(0.3, K=32)
    r = rp.solve(Xc0=10.0)
    nodal = float(np.max(np.abs(rp.residual(r["b"], r["Xc"]))))
    off = interpolant_defect(rp, r["b"], r["Xc"])
    check("off-node defect >> nodal residual (we are measuring the function)",
          off > 1e3 * nodal, f"off {off:.2e} vs nodal {nodal:.2e}")


# ---------------------------------------------------------------------------
def test_2_z0():
    print("\n[2] Z_0 is roundoff")
    worst = 0.0
    for a in (0.3, 0.5):
        rp = ReducedProfile(a, K=64)
        r = rp.solve(Xc0=10.0)
        worst = max(worst, z0_defect(rp, r["b"], r["Xc"]))
    check("||I - A DF|| at roundoff", worst < 1e-8, f"{worst:.2e}")


# ---------------------------------------------------------------------------
def test_3_second_derivative_threshold():
    print("\n[3] sup|N''| is finite exactly for a <= 1/2")
    ok = True
    for a in (0.2, 0.3, 0.4, 0.5):
        rp = ReducedProfile(a, K=96)
        r = rp.solve(Xc0=10.0)
        row = second_derivative_sup(rp, r["b"])
        flat = max(row) / min(row) < 1.001
        ok = ok and flat
        print(f"      a={a}: " + " ".join(f"{x:.4e}" for x in row)
              + ("  FLAT" if flat else "  GROWING"))
    check("a <= 1/2: flat under edge cutoff (finite)", ok)

    ok = True
    for a in (0.55, 0.8):
        rp = ReducedProfile(a, K=96)
        r = rp.solve(Xc0=10.0)
        row = second_derivative_sup(rp, r["b"])
        grows = row[-1] / row[0] > 10.0
        ok = ok and grows
        print(f"      a={a}: " + " ".join(f"{x:.4e}" for x in row)
              + ("  GROWING" if grows else "  flat"))
    check("a > 1/2: grows with the cutoff (the sup is infinite)", ok)

    # the exact value at a = 1/2 is p(p-1) = 2 with p = 2, checkable by hand
    rp = ReducedProfile(0.5, K=96)
    r = rp.solve(Xc0=10.0)
    got = second_derivative_sup(rp, r["b"])[0]
    check("a = 1/2 hits the exact value p(p-1) = 2", abs(got - 2.0) < 1e-9,
          f"{got:.12f}")


# ---------------------------------------------------------------------------
def test_4_adversary_is_real_and_the_naive_probe_is_not():
    print("\n[4] the adversary vs the naive probe, under quadrature refinement")
    rules = ((20, 20), (20, 40), (24, 60), (30, 80))
    print("      single high mode (the NAIVE probe -- should collapse to ~1):")
    last = None
    for K in (64, 128, 256):
        row = [step_adversary(K, lv, od, kind="single") for lv, od in rules]
        print(f"        K={K:4d}: " + "  ".join(f"{x:8.4f}" for x in row))
        last = row[-1]
    check("naive probe's growth is the QUADRATURE (flat ~1 when refined)",
          abs(last - 1.0) < 0.02, f"K=256 refined: {last:.4f}")

    print("      step partial sums (the ADVERSARY -- should survive refinement):")
    vals = []
    for K in (64, 128, 256):
        row = [step_adversary(K, lv, od, kind="step") for lv, od in rules]
        print(f"        K={K:4d}: " + "  ".join(f"{x:8.4f}" for x in row))
        vals.append(row[-1])
    stable = max(vals[i] / step_adversary((64, 128, 256)[i], 20, 40, kind="step")
                 for i in range(3)) < 1.05
    check("adversary is stable under refinement AND grows with K",
          stable and vals[-1] / vals[0] > 1.2,
          f"{vals[0]:.4f} -> {vals[-1]:.4f} at the finest rule")


# ---------------------------------------------------------------------------
def test_5_sup_diverges_logarithmically():
    print("\n[5] the sup ratio diverges like log K")
    Ks = (8, 16, 32, 64, 128, 256)
    r = [step_adversary(K, kind="step") for K in Ks]
    slope = float(np.polyfit(np.log(Ks), r, 1)[0])
    print("      " + " ".join(f"{x:.4f}" for x in r) + f"   slope {slope:+.4f}/e-fold")
    # linear in log K is the signature; check the fit is good AND the slope positive
    resid = np.max(np.abs(np.polyval(np.polyfit(np.log(Ks), r, 1), np.log(Ks))
                          - np.asarray(r)))
    check("positive slope in log K, and linear in log K", slope > 0.3 and resid < 0.15,
          f"slope {slope:+.4f}, max fit residual {resid:.3f}")


# ---------------------------------------------------------------------------
def test_6_holder_defuses_it():
    print("\n[6] a Holder domain norm defuses the adversary at gamma >~ 0.35")
    Ks = (8, 16, 32, 64, 128, 256)
    slopes = {}
    for g in (0.15, 0.35, 0.5, 0.85):
        r = [holder_ratio(K, g) for K in Ks]
        slopes[g] = float(np.polyfit(np.log(Ks), r, 1)[0])
        print(f"      gamma={g}: " + " ".join(f"{x:.4f}" for x in r)
              + f"   slope {slopes[g]:+.4f}")
    check("gamma >= 0.35 stops the divergence",
          slopes[0.35] < 0.0 and slopes[0.5] < 0.0 and slopes[0.85] < 0.0,
          "slopes " + ", ".join(f"{g}:{slopes[g]:+.4f}" for g in (0.35, 0.5, 0.85)))
    check("gamma = 0.15 does NOT (the threshold is real, not an artefact of using "
          "any seminorm at all)", slopes[0.15] > 0.0, f"{slopes[0.15]:+.4f}")

    # the seminorm helper itself, against a function whose Holder constant is known
    x = np.linspace(0.0, 1.0, 501)
    got = holder_seminorm(np.abs(x - 0.5) ** 0.5, x, 0.5)
    check("holder_seminorm exact on |x-c|^gamma (constant 1)",
          abs(got - 1.0) < 1e-9, f"{got:.12f}")


# ---------------------------------------------------------------------------
def test_7_rehearsal_reports_the_negative():
    print("\n[7] the assembled rehearsal refuses to return a budget")
    out = rehearsal(0.3, K=96)
    print(f"      Y0={out['Y0_interpolant_defect']:.2e}  Z0={out['Z0']:.2e}  "
          f"||A||={out['opnorm']:.4f}  N2_finite={out['N2_finite']}  Z1={out['Z1']}")
    check("Z_1 is reported as None, not as zero", out["Z1"] is None)
    check("verdict says the budget does not close",
          "DOES NOT CLOSE" in out["verdict"])
    check("a=0.3 has finite N''", out["N2_finite"] is True)
    check("a=0.8 does not", rehearsal(0.8, K=96)["N2_finite"] is False)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 72)
    print("solver/reduced_certificate.py -- gates")
    print("=" * 72)
    test_1_interpolant_defect_converges()
    test_2_z0()
    test_3_second_derivative_threshold()
    test_4_adversary_is_real_and_the_naive_probe_is_not()
    test_5_sup_diverges_logarithmically()
    test_6_holder_defuses_it()
    test_7_rehearsal_reports_the_negative()
    print("\n" + "=" * 72)
    print(f"{len(PASS)}/{len(PASS) + len(FAIL)} passed")
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
        raise SystemExit(1)
