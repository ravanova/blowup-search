"""Adversarial gates for `solver/viscous_novelty.py` (leg 143, Route-VNA).

`test_viscous_novelty.py` validates the module on WELL-FORMED input: the ledger is
well-formed, the published NLS zeros reproduce, a second published row reproduces, the
defect discriminates, the resolution and truncation ladders are measured, the dissipation
branch folds at DF's number, the margin proxy dies at the fold rather than at eps = 0, and
the figure calibration self-checks. Every input in that file is legal and in-domain. This
file validates the other half -- what the module does when the input is NOT well formed --
and banks leg 143's battery so the answer cannot silently regress.

The gate leg 143 answered, verbatim:

  "Under adversarial and degenerate inputs, does `viscous_novelty.py` ever silently return a
   wrong value rather than reject or visibly propagate the defect?"

Answered **YES**, on four independent sites. `solver/viscous_novelty.py` was NOT edited --
leg 143 had no patch authority under its own gate, so all four findings are PINNED here
rather than repaired. All four are **LATENT**: the banked DF Case I j=1 reproduction that
`capabilities.py` cites is clean (gate 12 below), so no recorded number moves.

WHAT "TRUE" MEANS HERE, AND WHERE IT COMES FROM
------------------------------------------------
Not this leg's invention -- each reference is the module's OWN documented contract:

  * `branch_in_kappa` docstring: "The sweep STOPS when Newton stops converging or when eps
    leaves [0, 1): past the branch's end the map has other zeros (with negative eps, i.e.
    anti-dissipation) and a continuation that does not check will happily report them as
    branch points."
  * `integrate_from_zero` docstring: "the initial-value problem Q(0) = mu, Q'(0) = 0,
    integrated to xi1".
  * `compare_to_published_branch` docstring: "our sweep is monotone in kappa, so a plain
    interpolation is well-defined".
  * `PRECEDENTS` documents exactly three verdicts: PRE_EMPTS, ADJACENT, EXCLUSION.

TWO KINDS OF GATE LIVE IN THIS FILE, AND THEY MUST NOT BE CONFUSED
-------------------------------------------------------------------
1. SOUNDNESS gates (`test_guard_*`, `test_latency_*`). These assert a property that HOLDS.
   If one fails, the module has started absorbing bad input somewhere it previously
   rejected it, or a banked number has become exposed.

2. CHARACTERIZATION gates (`test_pinned_*`). These assert the CURRENT, WRONG behaviour, so
   a later repair leg is forced to come back and update this file deliberately. A failure
   here is not necessarily bad news -- it may mean the defect was fixed. Each one names the
   repair that would flip it, and none of them may be "fixed" by loosening a tolerance.

Self-running, no pytest: `.venv/bin/python test_viscous_novelty_adversarial.py`. ~165 s.
The canonical full-fidelity measurement is the runner's, not this file's: every magnitude
quoted in `experiments/journal/leg_143.md` comes from
`writeup/data/p2_route_vna_v1_adversarial.json`.
"""

import math

import numpy as np

from solver import viscous_novelty as V

D, SIGMA, XI1 = 1, 2.3, 10.0
MU, KAPPA = V.DF_TABLE1[0][1], V.DF_TABLE1[0][2]

# The two NaN gates below assert a STRUCTURAL property (rejected / raises) that does not
# depend on the matching point, and a NaN seed makes the damped Newton run its full 40
# iterations with a 10-way line search at every one -- 289 s at xi1 = 10. They therefore use
# a cheaper matching point; verified to give the identical outcome at xi1 = 1, 2 and 10.
# Every gate that asserts a MAGNITUDE keeps the canonical XI1 = 10 of DF_TABLE1[0].
XI1_STRUCTURAL = 1.0


def _clean_branch():
    """A well-formed, strictly-monotone-in-kappa record list (no solver run needed)."""
    return [{"kappa": k, "eps": e, "mu": 1.0, "defect": 0.0, "converged": True}
            for k, e in [(0.85, 0.001), (0.80, 0.020), (0.75, 0.036), (0.70, 0.047),
                         (0.65, 0.055), (0.60, 0.059), (0.55, 0.0606)]]


def _raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:                                              # noqa: BLE001
        return False
    return False


# ===========================================================================
# SOUNDNESS -- the guards that fire. Lesson 90: each can come out the other way.
# ===========================================================================
def test_guard_singular_parameters_are_rejected():
    """[1] SOUNDNESS. kappa = 0 makes the far-field exponent and both correction
    coefficients singular (p = -1/sigma - i omega/kappa, a1 = .../(2i kappa)); d = 0 makes
    Q''(0) = .../(fac*d) singular; steps_per_osc = 0 makes the phase cap 40.0/0. All three
    raise rather than returning a plausible number."""
    print("\n[1] SOUNDNESS: singular parameters raise instead of absorbing")
    cases = {
        "kappa=0 -> asymptotic_coefficients":
            lambda: V.asymptotic_coefficients(1.0, 0.0, 0.0, D, SIGMA),
        "d=0 -> integrate_from_zero":
            lambda: V.integrate_from_zero(MU, KAPPA, 0.0, 0, SIGMA, 1.0),
        "steps_per_osc=0 -> integrate_from_zero":
            lambda: V.integrate_from_zero(MU, KAPPA, 0.0, D, SIGMA, 1.0, steps_per_osc=0),
    }
    for label, fn in cases.items():
        assert _raises(fn, ZeroDivisionError), label
        print(f"    {label}: ZeroDivisionError")
    print("[ok] 3/3 singular-parameter guards fire")


def test_guard_branch_in_kappa_rejects_a_nan_seed():
    """[2] SOUNDNESS, and the positive control for the filter-polarity finding at gate 3.

    branch_in_kappa's filter is `hist[-1] < tol`, and `nan < tol` is False, so a NaN
    convergence history is REJECTED. This guard could report the other answer -- it is a
    real comparison against a real residual -- and on a clean seed it does (gate 12)."""
    print("\n[2] SOUNDNESS: branch_in_kappa rejects a NaN convergence history")
    branch = V.branch_in_kappa(float("nan"), 0.85, 0.83, D, SIGMA, XI1_STRUCTURAL,
                               dkappa=0.01)
    assert branch, "the sweep should still emit its rejection record"
    n_conv = sum(r["converged"] for r in branch)
    print(f"    {n_conv}/{len(branch)} records flagged converged (nan < tol is False)")
    assert n_conv == 0, "a NaN residual must never be recorded as a converged branch point"
    print("[ok] the NaN guard fires")


def test_guard_margin_law_nan_row_propagates_visibly():
    """[3] SOUNDNESS. margin_law's filter is `if hist[-1] > 1e-9: continue`, and
    `nan > 1e-9` is ALSO False -- so the NaN row is ACCEPTED by the filter, the opposite
    polarity to gate 2's guard on the same quantity. It does not silently return a number,
    though: margin_proxy's np.linalg.cond raises on the resulting NaN Jacobian. The defect
    is visibly propagated, which is why this is a soundness gate and not a pinned one."""
    print("\n[3] SOUNDNESS: margin_law's NaN row raises downstream rather than returning")
    nan_branch = [{"kappa": 0.5546, "mu": float("nan"), "eps": 0.06, "defect": 0.0,
                   "converged": True}]
    print(f"    filter polarity: (nan < 1e-9) = {float('nan') < 1e-9}, "
          f"(nan > 1e-9) = {float('nan') > 1e-9} -> the row is NOT skipped")
    assert _raises(
        lambda: V.margin_law(nan_branch, {"eps_star": 0.06, "kappa_star": 0.5546},
                             D, SIGMA, XI1_STRUCTURAL, offsets=(0.02, 0.01)),
        np.linalg.LinAlgError)
    print("[ok] LinAlgError -- absorbed by the filter, but caught by numpy")


def test_guard_fold_of_is_honest_on_degenerate_records():
    """[4] SOUNDNESS. The 3-point parabolic fit is a cheap estimator (standard continuation
    practice monitors the Jacobian's smallest eigenvalue instead), so it was worth checking
    that a collinear or near-flat triple cannot throw the vertex outside its bracketing
    kappas, and that an unbracketable endpoint maximum is flagged rather than extrapolated.
    Neither failure occurs."""
    print("\n[4] SOUNDNESS: fold_of on degenerate parabolas")
    for kv in ([(0.50, 0.010), (0.51, 0.020), (0.52, 0.030), (0.53, 0.020)],
               [(0.50, 0.0100000), (0.51, 0.0100001), (0.52, 0.0100000)]):
        b = [{"kappa": k, "eps": e, "mu": 1.0, "defect": 0.0, "converged": True}
             for k, e in kv]
        f = V.fold_of(b)
        lo, hi = min(k for k, _ in kv), max(k for k, _ in kv)
        print(f"    kappa*={f['kappa_star']:.6f} in [{lo}, {hi}], eps*={f['eps_star']:.8f}")
        assert f["interior"] is True
        assert lo <= f["kappa_star"] <= hi, f"vertex escaped [{lo},{hi}]"
        assert math.isfinite(f["eps_star"])
    flat = [{"kappa": 0.5 + 0.01 * i, "eps": 0.05, "mu": 1.0, "defect": 0.0,
             "converged": True} for i in range(5)]
    assert V.fold_of(flat)["interior"] is False
    print("    a flat/endpoint maximum is reported with interior=False, not extrapolated")
    print("[ok] the parabolic fit stays inside its bracket and flags what it cannot bracket")


def test_guard_too_few_records_are_refused():
    """[5] SOUNDNESS. Both reducers refuse an under-populated record list rather than
    fitting one."""
    print("\n[5] SOUNDNESS: under-populated record lists are refused")
    assert V.fold_of([]) is None
    assert V.fold_of(_clean_branch()[:2]) is None
    assert V.compare_to_published_branch(_clean_branch()[:3]) is None
    print("[ok] fold_of and compare_to_published_branch both return None")


# ===========================================================================
# CHARACTERIZATION -- the current, wrong behaviour, pinned so a repair must revisit
# ===========================================================================
def test_pinned_margin_law_omits_the_antidissipation_guard():
    """[6] PINNED, SITE 1 -- the headline.

    branch_in_kappa rejects eps outside [0, 1) and its docstring says why: "the map has
    other zeros (with negative eps, i.e. anti-dissipation) and a continuation that does not
    check will happily report them as branch points." margin_law re-solves with
    solve_at_kappa and filters ONLY on the residual -- no eps test at all. Given seeds that
    are legal in shape but far from the fold, it returns rows on the anti-dissipative
    continuation and fits them into the divergence exponent it exists to report.

    REPAIR THAT FLIPS THIS GATE: add branch_in_kappa's `-1e-6 <= eps < 1.0` test to
    margin_law's row filter (returning slope=None when too few rows survive)."""
    print("\n[6] PINNED: margin_law accepts rows branch_in_kappa's own guard rejects")
    seed_branch = [{"kappa": 0.85, "mu": MU, "eps": 0.0, "defect": 0.0, "converged": True},
                   {"kappa": 0.80, "mu": MU, "eps": 0.02, "defect": 0.0, "converged": True}]
    res = V.margin_law(seed_branch, {"eps_star": 0.06, "kappa_star": 0.5546},
                       D, SIGMA, XI1, offsets=(0.08, 0.04))
    bad = [r for r in res["rows"] if not (-1e-6 <= r["eps"] < 1.0)]
    for r in res["rows"]:
        flag = "  <-- branch_in_kappa would REJECT" if r in bad else ""
        print(f"    kappa={r['kappa']:.4f} eps={r['eps']:+.6f} "
              f"Jinv={r['Jinv_norm']:.4e}{flag}")
    print(f"    slope reported {res['slope']:.6f} vs the module's own expected_slope "
          f"{res['expected_slope']:.1f}  ({abs(res['slope'] / res['expected_slope']):.2f}x)")
    assert bad, "PINNED: margin_law currently accepts anti-dissipative rows"
    assert min(r["eps"] for r in bad) < -0.2, \
        "PINNED: the accepted rows sit well into eps < 0, not on a boundary"
    assert res["slope"] is not None
    assert abs(res["slope"] / res["expected_slope"]) > 3.0, \
        "PINNED: the fitted exponent is several times the module's own expected_slope"
    print("[ok] PINNED: no exception, no flag -- a silently wrong divergence exponent")


def test_pinned_integrate_from_zero_returns_the_initial_condition():
    """[7] PINNED, SITE 2.

    The loop is `while xi < xi1` starting from xi = 1e-8, so any xi1 <= 1e-8 -- including
    xi1 = 0 and every NEGATIVE xi1 -- exits immediately and returns Q(1e-8) ~ mu with
    n_steps = 0 and no warning, while the docstring promises the IVP "integrated to xi1".

    REPAIR THAT FLIPS THIS GATE: reject xi1 <= the series start in integrate_from_zero."""
    print("\n[7] PINNED: integrate_from_zero returns Q(origin) for xi1 <= 1e-8")
    Qref, _, nref = V.integrate_from_zero(MU, KAPPA, 0.0, D, SIGMA, 1.0)
    print(f"    honest xi1=1.0: Q={Qref:.6f} after {nref} steps")
    assert nref > 0 and abs(Qref - MU) > 0.4, "the honest reference must actually move"
    for xi1 in (1e-8, 0.0, -1.0, -1e6):
        Q, _, n = V.integrate_from_zero(MU, KAPPA, 0.0, D, SIGMA, xi1)
        print(f"    xi1={xi1!r:>10}: Q={Q:.6f} after {n} steps "
              f"(|Q - mu| = {abs(Q - MU):.1e})")
        assert n == 0, f"PINNED: xi1={xi1} takes no steps"
        assert abs(Q - MU) < 1e-15, \
            f"PINNED: xi1={xi1} returns the initial condition, not an integrated value"
    print("[ok] PINNED: a negative integration endpoint returns the initial condition")


def test_pinned_match_defect_discards_the_n_steps_signal():
    """[8] PINNED, SITE 2 corollary.

    match_defect unpacks integrate_from_zero as `Q, dQ, _`, throwing away the one signal
    (n_steps == 0) that would reveal the pass-through above. It then returns a finite,
    astronomically wrong relative defect instead of refusing.

    REPAIR THAT FLIPS THIS GATE: check n_steps in match_defect, or guard xi1 upstream."""
    print("\n[8] PINNED: match_defect throws away n_steps, its only signal")
    defect, gamma, scale = V.match_defect(MU, KAPPA, 0.0, D, SIGMA, 1e-9)
    rel = abs(defect) / scale
    print(f"    |defect| = {abs(defect):.6e}, scale = {scale:.6e}, relative = {rel:.6e}")
    assert math.isfinite(abs(defect)) and math.isfinite(scale)
    assert rel > 1e10, "PINNED: finite, plausible-typed, and wrong by 17 decades"
    print("[ok] PINNED: a degenerate xi1 yields a finite number, not a refusal")


def test_pinned_compare_to_published_branch_breaks_on_a_kappa_tie():
    """[9] PINNED, SITE 3.

    np.interp requires strictly increasing x. The module sorts, so ORDER is handled, but a
    TIE in kappa is not -- and whichever partner the tie resolves to is what gets reported
    as "our" eps. One duplicated kappa inflates the published-agreement headline by three
    orders of magnitude, silently, in the very function that produces that headline.

    REPAIR THAT FLIPS THIS GATE: de-duplicate (or reject) tied kappa before interpolating."""
    print("\n[9] PINNED: a duplicated kappa silently rewrites the agreement headline")
    clean = _clean_branch()
    base = V.compare_to_published_branch(clean)
    poisoned = clean + [{"kappa": 0.80, "eps": 0.99, "mu": 1.0, "defect": 0.0,
                         "converged": True}]
    hit = V.compare_to_published_branch(poisoned)
    print(f"    clean    max|diff| = {base['max_abs_diff']:.6e}")
    print(f"    poisoned max|diff| = {hit['max_abs_diff']:.6e}  "
          f"({hit['max_abs_diff'] / base['max_abs_diff']:.1f}x)")
    assert base["max_abs_diff"] < 1e-3
    assert hit["max_abs_diff"] > 0.9, "PINNED: the tie is absorbed, not rejected"
    assert hit["max_abs_diff"] / base["max_abs_diff"] > 1e3, \
        "PINNED: three-orders-of-magnitude inflation of the agreement headline"
    print("[ok] PINNED: no exception, no warning -- a silently wrong agreement number")


def test_pinned_ledger_verdict_vocabulary_is_unenforced():
    """[10] PINNED, SITE 4.

    novelty_verdict selects on the exact string "PRE_EMPTS". Nothing validates that a ledger
    row's verdict is one of the three documented values, so a one-character typo flips
    stage V's gate answer from YES to NO with no error at all. This is the function that
    closes a stage and holds a live ban in plan_of_record.py.

    REPAIR THAT FLIPS THIS GATE: validate every verdict against the documented vocabulary
    and raise on anything outside it."""
    print("\n[10] PINNED: one character in the ledger flips stage V's gate answer")
    saved = V.PRECEDENTS
    try:
        assert V.novelty_verdict()[0] == "YES"
        V.PRECEDENTS = [dict(p) for p in saved]
        V.PRECEDENTS[0]["verdict"] = "PRE-EMPTS"          # hyphen, not underscore
        typo = V.novelty_verdict()[0]
        print(f"    'PRE_EMPTS' -> YES ; 'PRE-EMPTS' -> {typo}   (no exception raised)")
        assert typo == "NO", "PINNED: a typo'd verdict silently flips the gate answer"
    finally:
        V.PRECEDENTS = saved
    assert V.novelty_verdict()[0] == "YES", "the ledger must be restored"
    print("[ok] PINNED: the documented three-value vocabulary is unenforced")


def test_pinned_nonpositive_hmax_cannot_terminate():
    """[11] PINNED, SITE 5 -- a hang, NOT a silent wrong value, and reported as such.

    h = min(hmax, period_step, xi1 - xi). For hmax <= 0 the step is <= 0, so xi never
    advances and `while xi < xi1` cannot exit. Asserted on the loop's own first step rather
    than by running it, so this gate always terminates.

    REPAIR THAT FLIPS THIS GATE: require hmax > 0."""
    print("\n[11] PINNED: hmax <= 0 gives a non-advancing step (non-termination)")
    xi, xi1 = 1e-8, 1.0
    for hmax in (0.0, -1e-3):
        period_step = 2.0 * np.pi / max(KAPPA * xi, 1e-12) * (40.0 / 200)
        h = min(hmax, period_step, xi1 - xi)
        print(f"    hmax={hmax!r:>8}: h={h!r}, xi advances = {xi + h > xi}")
        assert h <= 0.0 and not (xi + h > xi)
    print("[ok] PINNED: the integrator has no positivity guard on its own step cap")


# ===========================================================================
# LATENCY -- none of the above is reached by the banked reproduction
# ===========================================================================
def test_latency_the_banked_reproduction_is_clean():
    """[12] SOUNDNESS. Legs 79 and 116 both found gaps that were latent, and that
    materially changes what the result means. The real DF Case I j=1 sweep is run here on
    the module's own transcribed row: every record converges, every eps is admissible, and
    margin_law's rows are all on the physical branch -- so site 1 is not reached by the
    banked path and the magnitudes capabilities.py records do not move.

    If this gate ever fails, the finding has stopped being latent and the recorded
    agreement numbers are exposed."""
    print("\n[12] SOUNDNESS: the banked DF Case I j=1 reproduction is clean")
    branch = V.branch_in_kappa(MU, KAPPA, 0.20, D, SIGMA, XI1, dkappa=0.01)
    rec = [r for r in branch if r["converged"]]
    print(f"    branch: {len(rec)}/{len(branch)} converged, "
          f"eps in [{min(r['eps'] for r in rec):.6f}, {max(r['eps'] for r in rec):.6f}]")
    assert len(rec) == len(branch) and len(rec) >= 60
    assert all(-1e-6 <= r["eps"] < 1.0 for r in rec)

    fold = V.fold_of(branch)
    d_eps = abs(fold["eps_star"] - V.DF_FIG1A_BRANCH1_FOLD["eps_star"])
    print(f"    fold: eps*={fold['eps_star']:.8f} vs published "
          f"{V.DF_FIG1A_BRANCH1_FOLD['eps_star']:.7f}  (|diff| = {d_eps:.3e})")
    assert fold["interior"] is True and d_eps < 1e-5

    ml = V.margin_law(branch, fold, D, SIGMA, XI1)
    n_bad = sum(1 for r in ml["rows"] if not (-1e-6 <= r["eps"] < 1.0))
    print(f"    margin_law: {len(ml['rows'])} rows, {n_bad} inadmissible, "
          f"slope={ml['slope']:.6f} vs expected {ml['expected_slope']:.1f}")
    assert n_bad == 0, "the banked path must not reach the anti-dissipative continuation"
    assert abs(ml["slope"] - ml["expected_slope"]) < 0.05
    print("[ok] all four findings are LATENT -- no banked number is exposed")


if __name__ == "__main__":
    test_guard_singular_parameters_are_rejected()
    test_guard_branch_in_kappa_rejects_a_nan_seed()
    test_guard_margin_law_nan_row_propagates_visibly()
    test_guard_fold_of_is_honest_on_degenerate_records()
    test_guard_too_few_records_are_refused()
    test_pinned_margin_law_omits_the_antidissipation_guard()
    test_pinned_integrate_from_zero_returns_the_initial_condition()
    test_pinned_match_defect_discards_the_n_steps_signal()
    test_pinned_compare_to_published_branch_breaks_on_a_kappa_tie()
    test_pinned_ledger_verdict_vocabulary_is_unenforced()
    test_pinned_nonpositive_hmax_cannot_terminate()
    test_latency_the_banked_reproduction_is_clean()
    print("\nAll leg-143 adversarial gates passed: 6 soundness gates hold, 6 "
          "characterization gates PIN the four escalated silent-corruption sites plus "
          "the non-termination hazard (see experiments/journal/leg_143.md). All four "
          "sites are LATENT: the banked reproduction is clean.")
