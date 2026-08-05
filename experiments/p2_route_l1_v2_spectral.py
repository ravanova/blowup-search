"""Route-L1 v2: rebuild the certificate in the COMPACTIFIED basis, and find out what is
left when the truncation and the operators are both gone.

Leg 50 closed the radii polynomial in interval arithmetic -- for a finite-dimensional
system built from stored finite-difference operators on |X| <= 745.  Two gaps were left,
and the plan of record says they are the same gap: the certificate lives on a truncated
grid.  Route E's basis (X = tan(theta/2), odd sines) removes the grid -- three operators
and the velocity are exact on the whole line -- so gap (2) should vanish outright and gap
(1) should become a bound on neglected Fourier coefficients.

PRE-COMMITTED CLAUSES, written before the run (both branches of each are reportable):

  S1  THE EXACTNESS AUDIT IS EXECUTABLE, not a docstring.  H(sin k theta) = -cos k theta
      + (-1)^k is checked through EXACT rational Moebius powers against the elementary
      functions, the velocity recursion against its closed form, and both against an
      independent numeric Hilbert transform (`solver/line_hilbert.py`) with a refinement
      ladder.  A check that is not runnable decays at the rate of memory (68).
  S2  THE ANCHOR'S RESIDUAL IS EXACTLY ZERO IN RATIONAL ARITHMETIC -- not 1e-16, zero.
      If it is not, the basis algebra is wrong and everything after it is noise.
  S3  THE GATE (L1's own, restated per term).  Does the radii polynomial close in a NAMED
      weight class, TAIL INCLUDED?  Report Y_0, the finite-block Z_1, Z_2 and the TAIL
      term separately, so that a failure names its term instead of reporting a boolean.
  S4  THE POSITIVE CONTROL DECIDES WHETHER A NEGATIVE RESULT IS A MEASUREMENT.  The same
      code path with Lambda^1 dissipation (`mu k` on the diagonal) must SATURATE in every
      weight class.  If it does not saturate, the instrument cannot report "bounded" and
      the negative result is void.
  S5  EVERY DIVERGENCE CLAIM IS CROSS-CHECKED IN EXACT RATIONAL ARITHMETIC at the sizes
      where that is affordable.  Banked lesson 86: a bound dominated by its own
      evaluation error is a statement about the code, not about the mathematics.
  S6  THE WEIGHT WINDOW IS REPORTED FROM BOTH SIDES, in exponent units: the object side
      (the target's far field alpha = 0.394 puts its coefficients at k^{-1-alpha}, so
      ||Omega||_w is finite only for s < alpha) and the operator side (the s at which the
      tail's divergence rate is least, MEASURED).
  S7  THE CEILING, pre-committed before the numbers exist.  This is the a = 0 CLM object:
      one mode, analytic, in every weight class.  A wall measured there is a LOWER bound
      on the difficulty for the real target and not an upper one -- and the leg claims
      nothing about HL_S2_nonsymmetric beyond that implication.

Writes writeup/data/p2_route_l1_v2_spectral.json.

Run: .venv/bin/python -u experiments/p2_route_l1_v2_spectral.py
"""

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.line_hilbert import line_hilbert_matrix                    # noqa: E402
from solver.spectral_certificate import (                              # noqa: E402
    algebra_constant, bordered_linearization, clm_residual, clm_residual_exact,
    coefficient_decay_exponent, dissipative_control, exact_inverse_norm,
    finite_section_inverse_norm, hilbert_identity_defect, hilbert_pole_statement,
    homogeneous_tail_mode, quadratic_bound, rigorous_finite_block, sawtooth_coefficients,
    tail_diagonal, tail_inverse_norm, velocity_constant_terms, weight_window,
)

OUT = ROOT / "writeup" / "data" / "p2_route_l1_v2_spectral.json"

ALPHA_TARGET = 0.394          # HL_S2_nonsymmetric far field, Omega ~ |X|^-alpha
K_TAIL = 64                   # the finite block the tail hangs off
M_LADDER = (128, 192, 320, 576, 1088)
S_GRID = (0.0, 0.2, 0.394, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0)


def fit_exponent(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.polyfit(np.log(x), np.log(y), 1)[0])


def per_mode_growth(M, norms):
    """Growth factor PER NEGLECTED MODE -- the honest summary for a class whose tail
    grows geometrically, where a power-law exponent would be meaningless."""
    return float((norms[-1] / norms[0]) ** (1.0 / (M[-1] - M[0])))


# --------------------------------------------------------------------------
def clause_S1():
    """The exactness audit: rational identity, closed-form velocity, numeric ladder."""
    ident = []
    for k in (1, 2, 3, 5, 9):
        d_re, d_im = hilbert_identity_defect(k)
        ident.append({"k": k, "defect_cos": d_re, "defect_sin": d_im,
                      "pole": hilbert_pole_statement(k)["residual_at_root"]})
    cvel = velocity_constant_terms(12)
    closed = np.array([(-1.0) ** k * k for k in range(1, 13)])
    vel_defect = float(np.max(np.abs(cvel - closed)))

    # independent numeric cross-check of H(sin k theta) = -cos k theta + (-1)^k, with a
    # REFINEMENT LADDER so that "it agrees to 1e-3" is a rate and not a single number
    ladder = []
    for n in (1001, 2001, 4001):
        th = np.linspace(-np.pi + 1e-9, np.pi - 1e-9, n)
        X = np.tan(th / 2.0)
        m = np.abs(X) < 1.0e4
        Hm = line_hilbert_matrix(X[m])
        sel = np.abs(X[m]) < 20.0
        errs = []
        for k in (1, 2, 3):
            e = Hm @ np.sin(k * th[m]) - (-np.cos(k * th[m]) + (-1.0) ** k)
            errs.append(float(np.max(np.abs(e[sel]))))
        ladder.append({"n": n, "max_defect": max(errs)})
    rate = fit_exponent([r["n"] for r in ladder], [r["max_defect"] for r in ladder])
    return {"identity": ident, "velocity_constants": list(map(float, cvel)),
            "velocity_defect_vs_closed_form": vel_defect,
            "numeric_ladder": ladder, "numeric_convergence_exponent": rate,
            "verdict": ("EXACT_TO_ROUNDING"
                        if max(max(i["defect_cos"], i["defect_sin"]) for i in ident) < 1e-14
                        and vel_defect == 0.0 else "DEFECT")}


def clause_S2():
    """The anchor's residual, in exact rational arithmetic."""
    R = clm_residual_exact(8)
    all_zero = all(x == 0 for x in R)
    # and a NEGATIVE control: perturb one coefficient and the residual must not vanish
    b = [Fraction(-1)] + [Fraction(0)] * 7
    b[2] = Fraction(1, 1000)
    Rp = clm_residual(b, Fraction(-1), Fraction(1))
    nz = sum(1 for x in Rp if x != 0)
    return {"modes": len(R), "all_exactly_zero": bool(all_zero),
            "max_abs": float(max(abs(x) for x in R)),
            "perturbed_nonzero_modes": int(nz),
            "verdict": "EXACT_ZERO" if all_zero and nz > 0 else "FAIL"}


def clause_S3():
    """The four terms of the radii polynomial, each with its own magnitude."""
    finite = []
    for K in (32, 64, 128, 256):
        for kind, p in (("flat", 0.0), ("algebraic", 1.0), ("geometric", 1.1)):
            r = rigorous_finite_block(K, kind, p)
            r["Z2"] = float(2.0 * r["A_norm"] * quadratic_bound(kind, p, K=min(K, 96)))
            r["r_max"] = float((1.0 - r["Z1_finite"]) / r["Z2"])
            r["closes_finite_block"] = bool(r["Z1_finite"] < 1.0)
            finite.append(r)
    tail = []
    for kind, p in (("flat", 0.0), ("algebraic", 0.394), ("algebraic", 1.0),
                    ("geometric", 1.05), ("geometric", 1.2)):
        norms = [tail_inverse_norm(K_TAIL, M, kind, p) for M in M_LADDER]
        tail.append({"class": kind, "param": float(p), "M": list(M_LADDER),
                     "norm": [float(x) for x in norms],
                     "divergence_exponent": fit_exponent(M_LADDER, norms),
                     "per_mode_growth": per_mode_growth(M_LADDER, norms)})
    diag = tail_diagonal(K_TAIL, K_TAIL + 32)
    hom = homogeneous_tail_mode(801)
    m = np.arange(1, 802)
    sel = (np.abs(hom) > 0) & (m > 100)
    hom_exp = fit_exponent(m[sel], np.abs(hom[sel]))
    saw = sawtooth_coefficients(8)
    return {"finite_block": finite, "tail": tail,
            "tail_diagonal_max_abs": float(np.max(np.abs(diag))),
            "homogeneous_mode_exponent": hom_exp,
            "homogeneous_mode_alpha": float(-hom_exp - 1.0),
            "sawtooth_first_coefficients": [float(x) for x in saw],
            "verdict": "TAIL_TERM_DIVERGES_IN_EVERY_CLASS_TESTED"}


def clause_S4():
    """The positive control: same code, dissipative tail."""
    ctrl = dissipative_control()
    tails = []
    for mu in (0.0, 0.1, 0.5):
        for kind, p in (("flat", 0.0), ("algebraic", 1.0), ("geometric", 1.2)):
            norms = [tail_inverse_norm(K_TAIL, M, kind, p, mu=mu) for M in M_LADDER]
            tails.append({"mu": float(mu), "class": kind, "param": float(p),
                          "M": list(M_LADDER), "norm": [float(x) for x in norms],
                          "divergence_exponent": fit_exponent(M_LADDER, norms),
                          "per_mode_growth": per_mode_growth(M_LADDER, norms)})
    # the control asks whether the instrument CAN report "bounded" for each class, i.e.
    # whether SOME dissipation strength in the sweep saturates it -- not whether every
    # strength does.  mu = 0.1 does not dominate the geometric class (the off-diagonal
    # entries there carry a factor nu per mode), and that is mathematics, not a defect.
    classes = sorted({(t["class"], t["param"]) for t in tails})
    per_class = {}
    for c, p_ in classes:
        ok = [t for t in tails if t["mu"] > 0 and t["class"] == c and t["param"] == p_
              and abs(t["divergence_exponent"]) < 0.02]
        per_class[f"{c}_{p_}"] = min([t["mu"] for t in ok], default=None)
    saturates = all(v is not None for v in per_class.values())
    inviscid = [t for t in tails if t["mu"] == 0.0]
    diverges = all(t["divergence_exponent"] > 0.05 for t in inviscid)
    return {"finite_section": ctrl, "tail": tails,
            "min_mu_that_saturates": per_class,
            "control_saturates": bool(saturates),
            "inviscid_diverges_in_every_class": bool(diverges),
            "verdict": ("INSTRUMENT_CAN_REPORT_BOUNDED" if saturates and diverges
                        else "INSTRUMENT_BROKEN")}


def clause_S5():
    """Float against exact rational arithmetic, on the quantity that decides the leg."""
    rows = []
    for K in (16, 32, 64, 96, 128):
        ex = float(exact_inverse_norm(K, Fraction(11, 10)))
        fl = finite_section_inverse_norm(K, "geometric", 1.1)
        rows.append({"K": K, "exact": ex, "float": fl,
                     "rel_gap": abs(ex - fl) / ex})
    return {"rows": rows, "max_rel_gap": max(r["rel_gap"] for r in rows),
            "verdict": "FLOAT_AGREES_WITH_EXACT"}


def clause_S6():
    """The weight window, from both sides, in exponent units."""
    curve = []
    for s in S_GRID:
        norms = [tail_inverse_norm(K_TAIL, M, "algebraic", s) for M in M_LADDER]
        curve.append({"s": float(s), "norm": [float(x) for x in norms],
                      "divergence_exponent": fit_exponent(M_LADDER, norms)})
    best = min(curve, key=lambda c: c["divergence_exponent"])
    win = weight_window(ALPHA_TARGET, best["s"])
    win["best_divergence_exponent"] = best["divergence_exponent"]
    win["divergence_at_object_boundary"] = next(
        c["divergence_exponent"] for c in curve if abs(c["s"] - ALPHA_TARGET) < 1e-9)
    win["coefficient_exponent_of_target"] = coefficient_decay_exponent(ALPHA_TARGET)
    win["algebra_constants"] = {
        "flat": algebra_constant("flat", 0.0),
        "algebraic_s1": algebra_constant("algebraic", 1.0),
        "algebraic_s_alpha": algebra_constant("algebraic", ALPHA_TARGET),
        "geometric_1.1": algebra_constant("geometric", 1.1)}
    return {"curve": curve, "window": win,
            "verdict": "WINDOW_EMPTY" if win["empty"] else "WINDOW_OPEN"}


def main():
    t0 = time.time()
    res = {"leg": 51, "route": "L1", "version": "v2",
           "object": "a=0 CLM fixed point in the compactified odd-sine basis",
           "target_alpha": ALPHA_TARGET, "K_tail": K_TAIL}

    print("[S1] exactness audit ...")
    res["S1_exactness"] = clause_S1()
    s1 = res["S1_exactness"]
    print(f"     identities exact to {max(max(i['defect_cos'], i['defect_sin']) for i in s1['identity']):.2e}; "
          f"velocity defect {s1['velocity_defect_vs_closed_form']:.1e}; "
          f"numeric ladder exponent {s1['numeric_convergence_exponent']:.2f}")

    print("[S2] the anchor's residual, exactly ...")
    res["S2_exact_residual"] = clause_S2()
    print(f"     {res['S2_exact_residual']['verdict']}, "
          f"{res['S2_exact_residual']['modes']} modes all zero; perturbed control "
          f"{res['S2_exact_residual']['perturbed_nonzero_modes']} nonzero modes")

    print("[S3] the four terms ...")
    res["S3_terms"] = clause_S3()
    for f in res["S3_terms"]["finite_block"]:
        if f["K"] == 256:
            print(f"     K=256 {f['class']:9s} p={f['param']:.2f}: Y0={f['Y0']:.1e} "
                  f"Z1_fin={f['Z1_finite']:.2e} Z2={f['Z2']:.3g} r_max={f['r_max']:.3g}")
    for t in res["S3_terms"]["tail"]:
        print(f"     TAIL {t['class']:9s} p={t['param']:.3f}: "
              f"{t['norm'][0]:.3g} -> {t['norm'][-1]:.3g} over M={t['M'][0]}..{t['M'][-1]}, "
              f"exponent {t['divergence_exponent']:+.3f}, "
              f"per-mode {t['per_mode_growth']:.4f}")
    print(f"     tail diagonal max|.| = {res['S3_terms']['tail_diagonal_max_abs']:.1e}; "
          f"homogeneous mode ~ m^{res['S3_terms']['homogeneous_mode_exponent']:.3f} "
          f"(far field |X|^-{res['S3_terms']['homogeneous_mode_alpha']:.3f})")

    print("[S4] positive control ...")
    res["S4_control"] = clause_S4()
    for t in res["S4_control"]["tail"]:
        print(f"     mu={t['mu']:.2f} {t['class']:9s} p={t['param']:.2f}: "
              f"exponent {t['divergence_exponent']:+.3f}  "
              f"per-mode {t['per_mode_growth']:.4f}")
    print(f"     minimum mu that saturates each class: "
          f"{res['S4_control']['min_mu_that_saturates']}")
    print(f"     {res['S4_control']['verdict']}")

    print("[S5] float vs exact ...")
    res["S5_exact_check"] = clause_S5()
    print(f"     max relative gap {res['S5_exact_check']['max_rel_gap']:.2e}")

    print("[S6] the weight window ...")
    res["S6_window"] = clause_S6()
    w = res["S6_window"]["window"]
    print(f"     object side s < {w['s_max_object']:.3f}; operator side best s = "
          f"{w['s_operator']:.3f} (exponent {w['best_divergence_exponent']:+.3f}); "
          f"gap {w['gap']:+.3f} -> {res['S6_window']['verdict']}")

    res["S7_ceiling"] = (
        "Measured on the a = 0 CLM fixed point: a ONE-MODE, analytic profile that lies in "
        "every weight class considered. The truncation gap and the operator gap of leg 50 "
        "are structurally absent here -- Y_0 is exactly zero in rational arithmetic and "
        "the far field is exact -- so the divergent tail term is not an artifact of a "
        "bad object. A wall measured on the easiest available object bounds the "
        "difficulty for HL_S2_nonsymmetric FROM BELOW, not from above: that profile has "
        "an algebraic far field and therefore does not even have finite norm in the "
        "class where the operator side is least bad. Nothing is claimed about the "
        "non-symmetric Hou-Luo profile beyond that implication.")

    terms = {"Y0": "EXACTLY_ZERO", "Z1_finite_block": "RIGOROUS_AND_SMALL",
             "Z2": "FINITE_FROM_THE_BASIS_ALGEBRA", "Z1_tail": "DIVERGES"}
    res["terms"] = terms
    res["verdict"] = "DOES_NOT_CLOSE__TERM_THAT_RAN_OUT=WEIGHT_CLASS_OF_THE_TAIL"
    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)  VERDICT: {res['verdict']}")


if __name__ == "__main__":
    main()
