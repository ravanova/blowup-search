"""Adversarial gates for `solver/port_certification.py` (leg 200, Route-PCA).

`test_port_certification.py` validates this module on WELL-FORMED input: every gate in it
hands the module a legal problem and checks the answer. `test_port_certification_
regression.py` (leg 86) and `test_port_certification_postrepair.py` pin ONE function,
`radii_polynomial_status`, against legs 79/128. This file validates the other half -- what
the module's FLOATING-POINT KERNELS do with a violated precondition, an integer array, a
NaN ladder, a reversed dimension list and a degenerate certificate -- and banks leg 200's
battery so the answers cannot silently regress.

The gate leg 200 answered, verbatim and pre-committed on both branches:

  "Under adversarial and degenerate inputs, does `port_certification.py` ever silently
   return a wrong value rather than reject or visibly propagate the defect?"

Answered **YES**, on four independent mechanisms across seven of the battery's twelve
gates. The module has 16 public entry points (10 module-level functions + 6
`ProfileResidual` methods); prior batteries had covered exactly one of them. Leg 200 had
no patch authority under its own gate's yes-branch and did not patch:
`solver/port_certification.py` is byte-identical to what it inherited, and this leg's
finding is ESCALATED, not repaired.

**NO BANKED NUMBER MOVES.** Every PORT-family reach-table value was produced with
`min(s_rho) = 0.38963488051119644 > 0` (`writeup/data/p2_route_l_v1_precond.json`,
`outward_upwinding`) and float64 fields, i.e. inside the corner where all four mechanisms
are dormant. In leg 116's sense these defects are NOT load-bearing -- the
hypothesis-satisfying counterpart returns the same number. They are **latent**: they fire
on the next profile, grid, ablation or caller that leaves that corner, and nothing in the
module or its pipeline would say so.

READ THIS BEFORE "FIXING" A FAILURE IN GATES 1-7
------------------------------------------------
Gates 1-7 are CHARACTERIZATION gates. They assert that a defect is OPEN -- they pin the
wrong answer, with its magnitude. **If one of them fails, that is very likely GOOD NEWS:
someone has repaired the module.** The correct response is to read
`experiments/journal/leg_200.md`, confirm the fix, and CONVERT the gate to a soundness
gate asserting the repaired property -- keeping leg 200's pre-repair magnitude printed
next to the repaired one, exactly as `test_certificate_shapes_adversarial.py` does for leg
146 and `test_first_integral_adversarial.py` does for leg 107. It must NOT be "fixed" by
loosening an assertion or deleting the gate.

Gates 0, 8 and 9 are SOUNDNESS gates from the start and must keep passing unconditionally.

THE FOUR MECHANISMS, AS MAGNITUDES
----------------------------------
  | gate | site | leg 200 measured |
  |---|---|---|
  | 1 | `line_sweep_solve` never checks its stated `s_rho > 0` precondition; the checker `outward_upwinding_holds` is a separate function no caller gates on | at `min(s_rho) = -0.4`, **18820x** relative error against the operator the docstring advertises, residual **20681x** the rhs; already **0.97%** at `-1e-3` |
  | 2 | the same routine chooses the ANGULAR direction by `sign(s_beta)` pointwise and the RADIAL direction not at all | the sign-awareness is present on one axis and absent four lines away, in one loop body |
  | 3 | `leading_order_solve` allocates `np.zeros_like(rhs)` with no float cast; its sibling `line_sweep_solve` opens with `np.asarray(rhs, float)` | integer rhs truncates: exact **0.5 returned as 0**, worst relative error **1.000** |
  | 4 | `leading_order_solve` is sign-blind in `c_l` for the same reason as gate 1 | **26.0x** relative error at `c_l = -0.5` |
  | 5 | `stall_verdict`'s `flat = bool(gain < 2.0)` -- and `NaN < 2.0` is False | a NaN or `+inf` ladder returns the confident prose *"bending => finite ill-conditioning, and more Krylov work would help"*; a negative residual returns *"flat"* at gain **-25.0** |
  | 6 | `stall_verdict` reads the ladder's ends POSITIONALLY (`rows[0]`, `rows[-1]`), never by `m` | identical data with descending `dims` flips the published verdict; work ratio **16.0 -> 0.0625** |
  | 7 | `radii_polynomial_status` returns `closes` from the discriminant alone and never forms `r_min` | `Y_0 = 0` -- **the value leg 51 measured on the a=0 CLM profile** -- gives `closes=True` on a ball of radius exactly **0** |

Mechanism 5/6 propagates: `attribution_summary` ranks the NaN ablation into the published
attribution table with `gain=NaN, flat=False`, i.e. presents it as an ablation that
un-flattened the ladder.

TWO OF THE FOUR ARE A GUARD THAT ALREADY EXISTS AND IS NEVER CALLED
-------------------------------------------------------------------
This is the shape of the finding, and it is why the leg escalates rather than shrugs:

  * gate 1's check is `solver/port_certification.py::outward_upwinding_holds`, in the same
    file. Its single caller in the repository, `experiments/p2_route_l_v1_precond.py:113`,
    formats `min`/`max` into a `print()` and never branches on `holds`. A `holds=False`
    would change nothing at all. That same runner passes `0 * one` as `s_rho` to its ADI
    negative control at line 172 -- a configuration the guard rejects -- which is direct
    evidence nobody consults it.
  * gate 7's check is `solver/certificate_guards.py::radius_violation`, written verbatim
    for this class (*"a non-positive or non-finite `r_min` is not a conservative verdict
    -- it asserts a zero inside a degenerate or empty set. Leg 116 measured 14 such
    'certificates' in `nk_bounds.budget` alone"*). `solver/nk_bounds.py:561` calls it.
    `solver/port_certification.py` imports `hypothesis_violations` and `NAN_HINT_GE_ONE`
    from that module and nothing else. **Legs 79/128 repaired the HYPOTHESIS half of the
    defect here and left the RADIUS half** -- in the very module that was leg 128's
    bit-identical comparison target.

WHAT CAME OUT CLEAN, AND IT IS THE MECHANISM THAT WAS MOST LIKELY A PRIORI
--------------------------------------------------------------------------
`gmres` reports the projected Arnoldi least-squares residual and never forms
`||Ax-b||/||b||`; `gmres_controls` attaches a `rel_true` to the well-conditioned case and
NOT to the `cond ~ 1e8` case whose number (0.0864) the module's docstring uses to argue
the observed Jacobian stall is worse than ill-conditioning alone. Under modified
Gram-Schmidt the two residuals can drift (Greenbaum-Rozlozník-Strakoš, BIT 37 (1997);
Paige-Rozlozník-Strakoš, SIMAX). **Measured across cond 1e0..1e16 they do not**: the
worst deviation is 8.1e-06 relative, at cond 1e16. (Note the sign: taking a bare `max()`
over the ratios instead of over `|ratio - 1|` under-reports that by 14x, and the runner
carries a comment saying so -- a ratio below 1 is just as much a gap as one above.)
Gate 8 banks that null, because a null with a control that
could have reported the other answer is a result. Every non-finite input to `gmres` --
in the rhs or injected by the operator -- raises `LinAlgError` (gate 9).

Full battery: `experiments/p2_route_pca_v1_adversarial.py` ->
`writeup/data/p2_route_pca_v1_adversarial.json`. Prior art:
`writeup/novelty/leg_200.md`, committed before the battery was written.

Runs in ~3 s (the expensive GMRES ladder lives in the runner, not here).
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver.certificate_guards import radius_violation                # noqa: E402
from solver.port_certification import (                               # noqa: E402
    ProfileResidual,
    attribution_summary,
    gmres,
    leading_order_solve,
    line_sweep_solve,
    outward_upwinding_holds,
    radii_polynomial_status,
    stall_verdict,
)

BANKED_MIN_S_RHO = 0.38963488051119644


# ---------------------------------------------------------------------------
# shared fixtures -- the independent references
# ---------------------------------------------------------------------------
def _thomas(a, b, c, d):
    n = len(d)
    cp = np.zeros(n)
    dp = np.zeros(n)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        den = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / den
        dp[i] = (d[i] - a[i] * dp[i - 1]) / den
    x = np.zeros(n)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def _dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, upwind_by_sign):
    """Dense (-s_rho d_rho - s_beta d_beta + c_diag), first-order upwind.

    `upwind_by_sign=False` reproduces what `line_sweep_solve` COMPUTES (backward radial
    difference unconditionally); `True` reproduces what its docstring PROMISES (direction
    chosen by `sign(s_rho)`, the same rule the function already applies to `s_beta`).
    """
    N = nr * nb
    L = np.zeros((N, N))
    for i in range(nr):
        sr = s_rho[i] / drho
        for j in range(nb):
            sb = float(s_beta[i][j])
            r = i * nb + j
            L[r, r] += c_diag
            if (not upwind_by_sign) or s_rho[i] > 0:
                L[r, r] += -sr
                if i - 1 >= 0:
                    L[r, (i - 1) * nb + j] += sr
            else:
                L[r, r] += sr
                if i + 1 < nr:
                    L[r, (i + 1) * nb + j] += -sr
            if sb > 0:
                L[r, r] += -sb / dbeta
                if j - 1 >= 0:
                    L[r, i * nb + j - 1] += sb / dbeta
            else:
                L[r, r] += sb / dbeta
                if j + 1 < nb:
                    L[r, i * nb + j + 1] += -sb / dbeta
    return L


def _sweep_case(floor):
    """The battery's PCA1 fixture, at a chosen minimum radial speed."""
    nr, nb = 12, 8
    rng = np.random.default_rng(7)
    drho, dbeta, c_diag = 0.1, 0.2, -1.2
    rhs = rng.standard_normal((nr, nb))
    s_beta = 0.5 * rng.standard_normal((nr, nb))
    s_rho = np.linspace(BANKED_MIN_S_RHO, 5.731643960887419, nr)
    s_rho[nr // 2] = floor
    got = line_sweep_solve(rhs, s_rho, s_beta, drho, dbeta, c_diag, _thomas)
    L_code = _dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, False)
    L_true = _dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, True)
    x_code = np.linalg.solve(L_code, rhs.ravel()).reshape(nr, nb)
    x_true = np.linalg.solve(L_true, rhs.ravel()).reshape(nr, nb)
    return {
        "s_rho": s_rho, "rhs": rhs, "got": got,
        "err_vs_code": float(np.linalg.norm(got - x_code) / np.linalg.norm(x_code)),
        "err_vs_true": float(np.linalg.norm(got - x_true) / np.linalg.norm(x_true)),
        "residual": float(np.linalg.norm(L_true @ got.ravel() - rhs.ravel())
                          / np.linalg.norm(rhs)),
    }


def _rows(pairs):
    return [{"m": m, "k": m, "rel_residual": r} for m, r in pairs]


# ---------------------------------------------------------------------------
# GATE 0 -- SOUNDNESS: the banked corner still works, so this file cannot pass
#           by the module being broken everywhere
# ---------------------------------------------------------------------------
def test_0_the_banked_corner_is_still_exact():
    """The positive control for the whole file (lesson 90: it must be able to differ).

    At the radial speeds the live PORT run actually had, `line_sweep_solve` is exact to
    ~1e-16 against BOTH dense assemblies -- because where `s_rho > 0` the two assemblies
    are the same matrix. If this gate ever fails, the defect gates below are measuring a
    broken fixture, not the module.
    """
    c = _sweep_case(BANKED_MIN_S_RHO)
    print(f"    banked min(s_rho) = {BANKED_MIN_S_RHO}: "
          f"err vs code-assembled {c['err_vs_code']:.3e}, "
          f"err vs advertised {c['err_vs_true']:.3e}, residual {c['residual']:.3e}")
    assert c["err_vs_code"] < 1e-12, c["err_vs_code"]
    assert c["err_vs_true"] < 1e-12, c["err_vs_true"]
    assert outward_upwinding_holds(c["s_rho"])["holds"] is True

    # and the module's own dtype-clean path is right
    rhs = np.array([[1.0, 0.0], [0.0, 0.0]])
    got = leading_order_solve(rhs, 1.0, 1.0, 3.0)
    ref = np.linalg.solve(np.array([[2.0, 0.0], [1.0, 2.0]]), rhs)
    assert np.allclose(got, ref), (got, ref)

    # and the honest certificate still closes with a POSITIVE radius
    v = radii_polynomial_status(1e-8, 0.5, 1.0)
    r_min = ((1.0 - 0.5) - math.sqrt(v["discriminant"])) / 2.0
    print(f"    honest certificate: closes={v['closes']}, r_min={r_min:.3e}, "
          f"radius_violation says {radius_violation(r_min)!r}")
    assert v["closes"] is True
    assert radius_violation(r_min) is None
    print("[ok] the banked corner is exact, the float path is right, and an honest "
          "certificate closes with a positive radius -- the fixtures can report the "
          "other answer")


# ---------------------------------------------------------------------------
# GATE 1 -- CHARACTERIZATION: the unchecked outward-upwinding precondition
# ---------------------------------------------------------------------------
def test_1_line_sweep_solves_a_different_operator_when_s_rho_goes_negative():
    """OPEN DEFECT, pinned at leg 200's magnitudes.

    `line_sweep_solve`'s docstring: *"EXACT O(N) inverse of (-s_rho d_rho - s_beta d_beta
    + c_diag), first-order upwind. Requires s_rho > 0"*. It does not check. Where
    `s_rho < 0` the hard-coded backward difference is the ANTI-upwind stencil, so the
    routine exactly inverts a DIFFERENT operator and returns a finite, correctly shaped,
    plausible array with no exception, no NaN and no flag.

    The curve is deliberately sampled at three points because it is NOT monotone in the
    violation: the worst error is at a MILD breach, not a gross one (banked lesson 88 --
    the minimum of a failure curve is not where to repair it, and here the MAXIMUM is not
    at the extreme either).

    IF THIS GATE FAILS, the precondition is probably now enforced. Convert it to a
    soundness gate asserting the refusal, and keep these magnitudes in the docstring.
    """
    mild = _sweep_case(-1e-3)
    worst = _sweep_case(-0.4)
    gross = _sweep_case(-3.0)
    for label, c in (("-1e-3 (mild)", mild), ("-0.4 (worst)", worst),
                     ("-3.0 (gross)", gross)):
        print(f"    min(s_rho) = {label:14s} "
              f"err vs advertised operator {c['err_vs_true']:11.4f}  "
              f"residual {c['residual']:11.4f}  "
              f"err vs code-assembled {c['err_vs_code']:.2e}  "
              f"guard would say holds="
              f"{outward_upwinding_holds(c['s_rho'])['holds']}")

    # it does NOT raise, and it does NOT return anything non-finite -- that is the finding
    assert np.all(np.isfinite(worst["got"]))

    # exactly inverts the WRONG operator: ~1e-16 against what it assembles ...
    assert worst["err_vs_code"] < 1e-9, worst["err_vs_code"]
    # ... and wildly wrong against what it advertises
    assert worst["err_vs_true"] > 1e4, worst["err_vs_true"]
    assert worst["residual"] > 1e4, worst["residual"]

    # a breach 390x smaller than the live run's own margin already costs ~1%
    assert 5e-3 < mild["err_vs_true"] < 5e-2, mild["err_vs_true"]

    # NON-MONOTONE: the gross breach is far milder than the marginal one
    assert gross["err_vs_true"] < 10.0 < worst["err_vs_true"], (
        gross["err_vs_true"], worst["err_vs_true"])

    # and the guard that would catch all three is never consulted by the solver
    assert outward_upwinding_holds(worst["s_rho"])["holds"] is False
    print("[ok] OPEN: line_sweep_solve returns the exact inverse of a different operator "
          "at negative s_rho -- 18820x at the worst sampled breach -- silently, and the "
          "worst case is a MILD violation, not a gross one")


def test_2_the_same_routine_is_sign_aware_on_one_axis_and_not_the_other():
    """OPEN DEFECT: the asymmetry is inside one loop body, four lines apart.

    This gate is separated from gate 1 because it is the part that makes the defect a
    finding rather than an omission of its era: `line_sweep_solve` DOES choose an upwind
    direction by sign -- `pos = sb > 0`, then `a[pos] = sb[pos]/dbeta` vs
    `c[~pos] = -sb[~pos]/dbeta` -- for the ANGULAR speed, and does not for the radial one.

    Measured behaviourally, not by reading the source: flip the sign of `s_beta` and the
    answer tracks the correctly-upwinded reference; flip the sign of `s_rho` and it does
    not.
    """
    nr, nb = 10, 6
    rng = np.random.default_rng(21)
    drho, dbeta, c_diag = 0.1, 0.2, -1.2
    rhs = rng.standard_normal((nr, nb))
    s_rho = np.linspace(0.5, 3.0, nr)

    for label, s_beta in (("s_beta > 0 everywhere", np.full((nr, nb), 0.7)),
                          ("s_beta < 0 everywhere", np.full((nr, nb), -0.7)),
                          ("s_beta mixed sign", 0.7 * np.sign(
                              rng.standard_normal((nr, nb))))):
        got = line_sweep_solve(rhs, s_rho, s_beta, drho, dbeta, c_diag, _thomas)
        L = _dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, True)
        ref = np.linalg.solve(L, rhs.ravel()).reshape(nr, nb)
        err = float(np.linalg.norm(got - ref) / np.linalg.norm(ref))
        print(f"    angular axis, {label:24s}: err vs correctly-upwinded {err:.3e}")
        assert err < 1e-12, (label, err)

    neg = _sweep_case(-0.4)
    print(f"    radial axis, s_rho < 0 somewhere : err vs correctly-upwinded "
          f"{neg['err_vs_true']:.3e}")
    assert neg["err_vs_true"] > 1e4
    print("[ok] OPEN: the angular difference direction is chosen by sign at every one of "
          "3 sign patterns; the radial one is never chosen at all")


# ---------------------------------------------------------------------------
# GATE 3/4 -- CHARACTERIZATION: leading_order_solve
# ---------------------------------------------------------------------------
def test_3_leading_order_solve_truncates_an_integer_right_hand_side():
    """OPEN DEFECT: `np.zeros_like(rhs)` inherits the dtype; NumPy truncates on assign.

    Its sibling twenty lines away opens with `rhs = np.asarray(rhs, float)`. Handing a
    linear solver a canonical basis vector or an indicator mask is ordinary; here it
    silently returns integers. (numpy#7730, numpy#8733 -- the truncation itself is
    documented NumPy behaviour, not a finding; the missing cast is.)
    """
    c_l, drho, c_diag = 1.0, 1.0, 3.0
    for label, rhs_int, expect in (
            ("canonical basis vector e_0", np.array([[1, 0], [0, 0]]), 1.0),
            ("indicator mask", np.array([[1, 1], [1, 1]]), 1.0),
            ("small integer rhs", np.array([[1, 2], [3, 4]]), 1.0 / 3.0)):
        got = leading_order_solve(rhs_int, c_l, drho, c_diag)
        ref = leading_order_solve(rhs_int.astype(float), c_l, drho, c_diag)
        rel = float(np.linalg.norm(got - ref) / np.linalg.norm(ref))
        print(f"    {label:26s} dtype {str(rhs_int.dtype):7s} -> "
              f"{str(got.dtype):7s}  int result {got.tolist()}  "
              f"float result {np.round(ref, 4).tolist()}  rel err {rel:.4f}")
        assert got.dtype == rhs_int.dtype
        assert np.all(np.isfinite(got))
        assert abs(rel - expect) < 1e-9, (label, rel, expect)

    # the sibling does NOT have this defect -- the asymmetry is the point
    rhs_int = np.array([[1, 0], [0, 0]])
    s_rho = np.full(2, 1.0)
    s_beta = np.zeros((2, 2))
    sw = line_sweep_solve(rhs_int, s_rho, s_beta, 1.0, 1.0, 3.0, _thomas)
    print(f"    sibling line_sweep_solve on the SAME integer rhs -> dtype {sw.dtype}")
    assert sw.dtype == np.dtype(float)
    print("[ok] OPEN: leading_order_solve truncates an integer rhs (exact 0.5 -> 0, rel "
          "err 1.000) while its sibling casts")


def test_4_leading_order_solve_is_sign_blind_in_c_l():
    """OPEN DEFECT: gate 1's twin, in the radial-only preconditioner.

    Docstring: *"upwinded outward"*, justified by *"at large r the advection speed
    s_rho -> c_l (bounded OUTWARD dilation)"*. No check. `c_l < 0` is not the sign the
    Hou-Luo rescaling produces, so this is LATENT rather than live -- pinned because it is
    the same missing check in the second solver, and a repair of gate 1 that misses it
    would leave half the defect standing.
    """
    nr = 16
    rng = np.random.default_rng(3)
    rhs = rng.standard_normal((nr, 4))
    drho, c_diag = 0.1, -1.2

    def ref_for(c_l):
        L = np.zeros((nr, nr))
        a = c_l / drho
        for i in range(nr):
            if c_l > 0:
                L[i, i] = c_diag - a
                if i - 1 >= 0:
                    L[i, i - 1] = a
            elif c_l < 0:
                L[i, i] = c_diag + a
                if i + 1 < nr:
                    L[i, i + 1] = -a
            else:
                L[i, i] = c_diag
        return np.linalg.solve(L, rhs)

    errs = {}
    for c_l in (2.5, 0.5, 0.0, -0.5, -2.5):
        got = leading_order_solve(rhs, c_l, drho, c_diag)
        ref = ref_for(c_l)
        errs[c_l] = float(np.linalg.norm(got - ref) / np.linalg.norm(ref))
        print(f"    c_l = {c_l:+5.2f}: err vs correctly-upwinded {errs[c_l]:.4e}")
    assert errs[2.5] < 1e-12 and errs[0.5] < 1e-12 and errs[0.0] == 0.0
    assert errs[-0.5] > 10.0, errs[-0.5]
    assert errs[-2.5] > 1.0, errs[-2.5]
    print("[ok] OPEN: leading_order_solve is exact for c_l > 0 and 26.0x wrong at "
          "c_l = -0.5, with no flag")


# ---------------------------------------------------------------------------
# GATE 5/6 -- CHARACTERIZATION: the verdict layer
# ---------------------------------------------------------------------------
def test_5_stall_verdict_reports_bending_on_a_nan_ladder():
    """OPEN DEFECT: `flat = bool(gain < 2.0)` and `NaN < 2.0` is False.

    This is byte-for-byte the mechanism `certificate_guards.NAN_HINT_GE_ONE` names
    (*"note that `NaN >= 1.0` is False, so an unguarded NaN would slip past the
    contraction test"*), moved from a certificate verdict to an attribution verdict. The
    harm is not lost information: it is the CONFIDENT prose, which is the exact opposite
    of this module's entire finding about the operator.
    """
    nan = float("nan")
    controls = {"honest flat": (_rows([(10, 0.6623), (160, 0.6300)]), True),
                "honest bending": (_rows([(10, 0.4463), (160, 0.0188)]), False)}
    for label, (rows, want_flat) in controls.items():
        v = stall_verdict(rows)
        print(f"    control {label:16s}: gain {v['residual_gain']:8.4f}  "
              f"flat={v['flat']}")
        assert v["flat"] is want_flat, (label, v)

    poisoned = {"both NaN": _rows([(10, nan), (160, nan)]),
                "NaN at far end": _rows([(10, 0.66), (160, nan)]),
                "NaN at near end": _rows([(10, nan), (160, 0.02)]),
                "+inf residual": _rows([(10, float("inf")), (160, 0.02)])}
    for label, rows in poisoned.items():
        v = stall_verdict(rows)
        print(f"    poisoned {label:16s}: gain {v['residual_gain']}  flat={v['flat']}  "
              f"prose {v['reading'][:34]!r}...")
        assert v["flat"] is False, (label, v)
        assert v["reading"].startswith("bending"), (label, v["reading"])

    # a negative "residual" -- an impossible norm -- is called flat with a negative gain
    v = stall_verdict(_rows([(10, -0.5), (160, 0.02)]))
    print(f"    poisoned negative residual : gain {v['residual_gain']}  flat={v['flat']}")
    assert v["flat"] is True and v["residual_gain"] == -25.0, v

    # it propagates: attribution_summary RANKS the poisoned ablation
    ranked = attribution_summary({"full": _rows([(10, 0.6623), (160, 0.6300)]),
                                  "angular transport OFF": _rows([(10, nan),
                                                                  (160, nan)])})
    labels = [r["ablation"] for r in ranked]
    nan_row = [r for r in ranked if r["ablation"] == "angular transport OFF"][0]
    print(f"    attribution_summary ranks {labels} with the NaN row at gain "
          f"{nan_row['gain']}, flat={nan_row['flat']}")
    assert len(ranked) == 2 and math.isnan(nan_row["gain"])
    assert nan_row["flat"] is False
    print("[ok] OPEN: 5 of 5 poisoned ladders get a confident verdict, and the NaN one "
          "takes a rank in the attribution table")


def test_6_stall_verdict_reads_the_ladder_positionally_not_by_dimension():
    """OPEN DEFECT: `first, last = rows[0], rows[-1]`.

    `krylov_ladder(dims=...)` preserves the caller's ordering, so a descending `dims`
    tuple -- a natural thing to write when probing the expensive end first -- inverts the
    work ratio and FLIPS the published verdict on identical measurements, with no error.
    """
    asc = stall_verdict(_rows([(10, 0.66), (160, 0.02)]))
    desc = stall_verdict(_rows([(160, 0.02), (10, 0.66)]))
    print(f"    dims ascending : work_ratio {asc['work_ratio']:7.4f}  "
          f"gain {asc['residual_gain']:8.4f}  flat={asc['flat']}")
    print(f"    dims descending: work_ratio {desc['work_ratio']:7.4f}  "
          f"gain {desc['residual_gain']:8.4f}  flat={desc['flat']}")
    assert asc["work_ratio"] == 16.0 and desc["work_ratio"] == 0.0625
    assert asc["flat"] is False and desc["flat"] is True
    assert asc["reading"] != desc["reading"]
    print("[ok] OPEN: the same two measurements give opposite published verdicts "
          "depending on the order of the dims tuple")


# ---------------------------------------------------------------------------
# GATE 7 -- CHARACTERIZATION: the radius half of legs 79/128's repair
# ---------------------------------------------------------------------------
def test_7_radii_polynomial_status_closes_on_a_ball_of_radius_zero():
    """OPEN DEFECT, and the sharpest one: the guard exists and is never asked.

    `radii_polynomial_status` returns `closes = bool(disc >= 0)` and never forms
    `r_min = ((1-Z_1) - sqrt(disc)) / (2 Z_2)`. `solver/certificate_guards.radius_violation`
    was written for exactly this class and is called by `solver/nk_bounds.py:561`;
    `port_certification.py` imports only `hypothesis_violations` and `NAN_HINT_GE_ONE`.

    `Y_0 = 0` is not synthetic here: leg 51 measured it EXACTLY zero on the a=0 CLM
    profile (it is one basis mode), and `plan_of_record.py` carries a standing ban on
    reading that zero as progress. Fed that banked value, this function issues a closing
    certificate for a ball containing exactly one point.
    """
    for label, (y, z1, z2) in (("Y_0 = 0 (leg 51's banked value)", (0.0, 0.5, 1e4)),
                               ("Y_0 = 0, Z_1 = 0.9", (0.0, 0.9, 1.0)),
                               ("Y_0 = -0.0 signed zero", (-0.0, 0.5, 1.0)),
                               ("Y_0 = Z_1 = Z_2 = 0", (0.0, 0.0, 0.0))):
        v = radii_polynomial_status(y, z1, z2)
        r_min = 0.0
        why = radius_violation(r_min)
        print(f"    {label:32s}: status {v['status']}, closes={v['closes']}, "
              f"r_min={r_min}, radius_violation -> {why[:38]!r}...")
        assert v["status"] == "EVALUATED"
        assert v["closes"] is True, (label, v)
        assert "r_min" not in v and "radius" not in str(v.keys())
        assert why is not None, "the shared guard must reject a zero radius"

    # the hypothesis half IS guarded -- legs 79/128 must not regress (soundness inside
    # a characterization gate, so a repair of one half cannot silently undo the other)
    for label, args in (("Y_0 negative", (-1.0, 0.9, 1e4)),
                        ("Z_1 NaN", (1e-6, float("nan"), 1.0)),
                        ("Z_2 +inf", (1e-6, 0.5, float("inf")))):
        v = radii_polynomial_status(*args)
        assert v["status"] == "INVALID_INPUT" and v["closes"] is False, (label, v)
    print("    legs 79/128 hypothesis guard: 3 of 3 violating inputs still INVALID_INPUT")
    print("[ok] OPEN: closes=True on a radius-zero ball for 4 of 4 degenerate "
          "certificates; the hypothesis half of the repair holds and the radius half "
          "was never written")


# ---------------------------------------------------------------------------
# GATE 8/9 -- SOUNDNESS: what came out clean
# ---------------------------------------------------------------------------
def test_8_gmres_projected_residual_tracks_the_true_residual():
    """SOUNDNESS + the leg's NULL result. Must keep passing.

    `gmres` reports the projected Arnoldi least-squares residual and never forms
    `||Ax-b||/||b||`; the module's `cond ~ 1e8` control carries no `rel_true`. Under MGS
    the two can drift (Greenbaum-Rozlozník-Strakoš, BIT 37 (1997)). Across the condition
    ladder they do not, and this gate banks that -- a null measured with a reference that
    could have reported a gap. Trimmed to three rungs so the suite stays fast; the full
    nine-rung ladder is in the runner.
    """
    n, m = 300, 200
    rng = np.random.default_rng(0)
    b = rng.standard_normal(n)
    worst = 0.0
    for e in (4, 10, 16):
        rng2 = np.random.default_rng(100 + e)
        A = np.diag(np.logspace(0.0, float(e), n)) @ (
            np.eye(n) + 0.1 * rng2.standard_normal((n, n)) / np.sqrt(n))
        x, rel, _ = gmres(lambda v: A @ v, b, m=m, tol=1e-10)
        true = float(np.linalg.norm(A @ x - b) / np.linalg.norm(b))
        ratio = true / rel
        worst = max(worst, abs(ratio - 1.0))
        print(f"    cond ~ 1e{e:<2d}: reported {rel:.6e}  true {true:.6e}  "
              f"ratio {ratio:.9f}")
    assert worst < 1e-4, worst
    print(f"[ok] CLEAN: the projected residual tracks the true one to {worst:.2e} "
          "relative -- the a-priori-likeliest mechanism is a NULL")


def test_9_non_finite_inputs_to_gmres_raise_rather_than_return():
    """SOUNDNESS: every non-finite path through `gmres` is VISIBLE. Must keep passing.

    NOTE: `np.linalg.lstsq` prints `** On entry to DLASCL parameter number 4 had an
    illegal value` to stderr before raising. That noise is the gate working.
    """
    A = np.eye(4) * 2.0
    for label, b in (("b has a NaN", np.array([1.0, np.nan, 3.0, 1.0])),
                     ("b has a +inf", np.array([1.0, np.inf, 3.0, 1.0])),
                     ("b is all NaN", np.full(4, np.nan))):
        try:
            gmres(lambda v: A @ v, b, m=4)
            raise AssertionError(f"{label} returned instead of raising")
        except np.linalg.LinAlgError as exc:
            print(f"    {label:16s} -> LinAlgError: {exc}")

    def nan_matvec(v):
        w = np.asarray(v, float).copy()
        w[0] = np.nan
        return w

    try:
        gmres(nan_matvec, np.ones(5), m=4)
        raise AssertionError("a NaN-injecting operator returned instead of raising")
    except np.linalg.LinAlgError as exc:
        print(f"    {'matvec injects NaN':16s} -> LinAlgError: {exc}")

    # the legitimate early return must survive
    x, rel, k = gmres(lambda v: A @ v, np.zeros(4), m=4)
    print(f"    zero rhs -> rel {rel}, k {k} (legitimate early return)")
    assert rel == 0.0 and k == 0 and np.all(x == 0.0)
    print("[ok] CLEAN: 4 of 4 non-finite paths raise; the zero-rhs early return is "
          "preserved")


def test_10_pack_unpack_is_shape_blind():
    """OPEN DEFECT, minor and reported for completeness.

    `pack` is `concatenate([ravel(o), ravel(e), ravel(x)])`; `unpack` is three
    `reshape(self.shape)` calls. Only the TOTAL size is validated, so a field handed in
    the transposed layout -- a live hazard in a codebase carrying both (rho, beta) and
    (beta, rho) conventions -- round-trips into a different, finite, plausible field.
    """
    class _Grid:
        def __init__(self, nr, nb):
            self.rho = np.zeros(nr)
            self.beta = np.zeros(nb)
            self.drho = 0.1

    nr, nb = 6, 4
    res = ProfileResidual(solver=None, grid=_Grid(nr, nb))
    rng = np.random.default_rng(5)
    o, e, x = (rng.standard_normal((nr, nb)) for _ in range(3))

    o2, e2, x2 = res.unpack(res.pack(o, e, x))
    assert np.array_equal(o, o2) and np.array_equal(e, e2) and np.array_equal(x, x2)

    _, e_bad, _ = res.unpack(res.pack(o, e.T.copy(), x))
    rel = float(np.linalg.norm(e_bad - e) / np.linalg.norm(e))
    print(f"    transposed field round-trips: shape {e_bad.shape}, no exception, "
          f"rel err vs the intended field {rel:.4f}")
    assert e_bad.shape == (nr, nb)
    assert not np.allclose(e_bad, e)
    assert rel > 1.0

    try:
        res.unpack(np.zeros(3 * nr * nb + 1))
        raise AssertionError("a wrong total length returned instead of raising")
    except ValueError as exc:
        print(f"    wrong TOTAL length -> ValueError: {exc}")
    print("[ok] OPEN: a transposed field round-trips silently at 1.32 relative error; "
          "only the total length is checked")


if __name__ == "__main__":
    test_0_the_banked_corner_is_still_exact()
    test_1_line_sweep_solves_a_different_operator_when_s_rho_goes_negative()
    test_2_the_same_routine_is_sign_aware_on_one_axis_and_not_the_other()
    test_3_leading_order_solve_truncates_an_integer_right_hand_side()
    test_4_leading_order_solve_is_sign_blind_in_c_l()
    test_5_stall_verdict_reports_bending_on_a_nan_ladder()
    test_6_stall_verdict_reads_the_ladder_positionally_not_by_dimension()
    test_7_radii_polynomial_status_closes_on_a_ball_of_radius_zero()
    test_8_gmres_projected_residual_tracks_the_true_residual()
    test_9_non_finite_inputs_to_gmres_raise_rather_than_return()
    test_10_pack_unpack_is_shape_blind()
    print("\nAll leg-200 adversarial gates passed: 1 anchor + 7 CHARACTERIZATION gates "
          "pinning open silent-wrong-value mechanisms + 2 SOUNDNESS gates + 1 minor "
          "characterization gate. A failure in the characterization gates most likely "
          "means the module was repaired -- see the header and "
          "experiments/journal/leg_200.md before changing anything.")
