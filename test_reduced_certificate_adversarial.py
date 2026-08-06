"""Adversarial gates for `solver/reduced_certificate.py` (leg 109, Route-RCA).

`test_reduced_certificate.py` validates the module on WELL-FORMED inputs: the interpolant
defect's convergence in K, Z_0's roundoff level, the a <= 1/2 threshold, the adversary vs
the naive probe, the +0.499 log slope, the Holder defusal, and that `rehearsal` reports
the negative. Every input in that file is legal and in-domain, and no test in it reads the
`verdict` sentence. This file validates the other half — what the module *claims* when the
numbers beside the claim contradict it, and what it does on NaN-poisoned coefficients —
and banks leg 109's battery so the answer cannot silently regress.

The gate leg 109 answered, verbatim:

  "Under an adversarial battery of degenerate or NaN-poisoned inputs, does
   solver/reduced_certificate.py ever report internal self-consistency on a case that is
   not actually self-consistent?"

Leg 109 answered **YES**, on three independent sites, with NO patch authority under its
own gate ("escalate, do not patch"). **Leg 0 (bench repair) then applied the three fixes
leg 109's journal named** (`experiments/journal/leg_109.md`, "Recommended repair"), and
gates 1, 2 and 5 below have been converted from CHARACTERIZATION to **SOUNDNESS** gates,
asserting the repaired property while keeping the pre-repair magnitude on the record in
the docstrings and print output.

  | gate | site | leg 109 measured (pre-repair) | now asserts (post-repair) |
  |---|---|---|---|
  | 1 | `rehearsal`'s hardcoded `verdict` | 1 distinct verdict string over 15 converged (a,K) cases whose Y_0 spans 10.1 orders of magnitude; 14 of 15 asserted "machine level" where Y_0 > 1e-10 | the verdict is computed from the measured Y_0/Z_0 against a real 1e-10 threshold: 15 distinct sentences, and each sentence's claim matches its own case |
  | 2 | `N2_finite` at p == 2 exactly | 4 of 4 poisoned states (all-NaN, all-inf, all-zero, garbage) certified `True` at a = 1/2, because `nan ** 0.0 == 1.0` | `second_derivative_sup` refuses (reports NaN) whenever `e` is non-finite, so `N2_finite` is `False` on all-NaN/all-inf; all-zero and garbage remain `True` because that is mathematically correct (N''(e) = 2 for ANY finite e at p == 2, including 0, as the e -> 0 limit) — 2 of 4 certified, not 0 of 4, and the two that stay True are the two where True is the honest answer |
  | 3 | the three-cutoff ladder | 0 of 16 cases where it changed the answer away from `a <= 1/2`; every evaluated ratio is exactly 1.0 (lesson 90) | unchanged — the ladder is still decorative; not part of this repair |
  | 4 | `z0_defect`'s residual side | reports the LEFT residual, 9.6x-278x LARGER than the right one — conservative, NOT corrupting | unchanged — not part of this repair |
  | 5 | `step_adversary`'s `kind` dispatch | 6 of 6 unrecognised strings silently return the adversary; only exact `"single"` reaches the control | 6 of 6 unrecognised strings now raise `ValueError`; only exact `"step"`/`"single"` are accepted |
  | 6 | poisoned `b` away from p == 2 | 0 of 24 probes silently finite | unchanged — the module already propagated correctly here |
  | 7 | degenerate `a` | 4 of 8 admitted by the constructor, 4 of 4 caught by `converged=False`, 0 emitted a verdict | unchanged — not part of this repair |

Gates 1, 2, 5 are SOUNDNESS gates now: if one of them fails, the repair has regressed —
read `experiments/journal/leg_109.md`'s "Recommended repair" section before touching
anything. Gates 3, 4, 6 and 7 assert properties that HOLD and were never part of this
repair; if one of those fails, the module has started absorbing bad input somewhere it
previously flagged it, and the response is to fix the module.

Self-running, no pytest: `.venv/bin/python test_reduced_certificate_adversarial.py`.
"""

import warnings

import numpy as np

from solver.first_integral import ReducedProfile
from solver.reduced_certificate import (interpolant_defect, rehearsal,
                                        second_derivative_sup, step_adversary,
                                        z0_defect)

# "machine level" / "roundoff" as the module's own docstring uses them, two orders
# LOOSER than its finding (1) claims ("~1e-12 by K ~ 96 at a = 0.3"), so that a case
# counted as contradicting the verdict contradicts it by a wide margin.
MACHINE_LEVEL = 1e-10


def _n2_finite(rp, b):
    """`rehearsal`'s own N2_finite expression, reproduced verbatim (post-repair)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        npp = second_derivative_sup(rp, b)
    if not (rp.p >= 2.0):                 # Python short-circuits before the ratio
        return False, npp
    if not np.all(np.isfinite(npp)) or min(npp) == 0.0:
        return False, npp
    return bool(max(npp) / min(npp) < 1.01), npp


def _rehearse(a, k):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return rehearsal(float(a), K=int(k))


# ---------------------------------------------------------------------------
# 0. the fixture itself, before anything is concluded from it
# ---------------------------------------------------------------------------
def test_clean_reference_selfcheck():
    """Every gate below is read against the module's own headline case; gate that first.

    This is also the POSITIVE CONTROL for gate 1: at a = 0.3, K = 96 the verdict sentence
    is TRUE (both before and after the repair -- this case never contradicted it).
    """
    print("\n[0] clean reference self-check")
    r = _rehearse(0.3, 96)
    assert r["converged"], r
    y0 = r["Y0_interpolant_defect"]
    print(f"    a=0.3, K=96: Y_0 = {y0:.4e}, Z_0 = {r['Z0']:.4e}, "
          f"N2_finite = {r['N2_finite']}")
    assert y0 <= MACHINE_LEVEL, y0            # the verdict sentence is TRUE here
    assert r["Z0"] <= MACHINE_LEVEL, r["Z0"]
    assert r["N2_finite"] is True
    assert r["Z1"] is None, "Z_1 must stay uncomputed and explicitly None"
    print("[ok] the module's headline case is intact and the verdict is true ON IT")


# ---------------------------------------------------------------------------
# 1. SOUNDNESS (post-repair) -- the verdict is a measurement, not a constant
# ---------------------------------------------------------------------------
def test_verdict_is_decoupled_from_the_numbers_it_asserts():
    """`rehearsal` used to emit one hardcoded sentence for every input (leg 109, finding
    A), asserting "Y_0 is at machine level and Z_0 is roundoff" regardless of the
    measured values -- lesson 90's shape, applied to a claim. Pre-repair magnitude kept
    on the record: 15 converged (a, K) cases, 1 distinct verdict string, Y_0 spanning
    10.10 orders of magnitude (1.23e-12 .. 1.55e-2), 14 of 15 contradicting the sentence.

    Post-repair: the verdict is assembled from the measured Y0_interpolant_defect and Z0
    against the same 1e-10 threshold the module's own docstring implies ("machine
    level" / "roundoff"), so each case gets its own sentence and that sentence's Y_0/Z_0
    claim must agree with the number reported beside it.
    """
    print("\n[1] SOUNDNESS: the verdict sentence now tracks the numbers beside it")
    rows, verdicts = [], set()
    for a in (0.3, 0.5, 0.8, 1.0, 1.2):
        for k in (16, 32, 96):
            r = _rehearse(a, k)
            if not r.get("converged"):
                continue
            verdicts.add(r["verdict"])
            rows.append((a, k, r["Y0_interpolant_defect"], r["Z0"], r["verdict"]))
    y0s = [y for _, _, y, _, _ in rows]
    false_rows = [t for t in rows if t[2] > MACHINE_LEVEL]
    worst = max(rows, key=lambda t: t[2])
    spread = np.log10(max(y0s) / min(y0s))
    print(f"    {len(rows)} converged cases, {len(verdicts)} distinct verdict string(s)")
    print(f"    Y_0 spans {min(y0s):.3e} .. {max(y0s):.3e}  ({spread:.2f} orders)")
    print(f"    Y_0 > {MACHINE_LEVEL:g} (should NOT read 'is at machine level'): "
          f"{len(false_rows)} of {len(rows)}")
    print(f"    worst: a={worst[0]}, K={worst[1]}, Y_0 = {worst[2]:.4e}")
    # the fix is wired: at least as many distinct sentences as distinct Y_0/Z_0 pairs
    assert len(verdicts) >= 14, (
        f"only {len(verdicts)} distinct verdicts over {len(rows)} converged cases -- "
        "the verdict may have regressed to a constant; see leg 109's journal")
    assert spread > 9.0, spread            # the underlying spread is unchanged
    assert worst[2] > 1e-3, worst          # a=0.3, K=16 still reaches 1.5e-2
    # every sentence's claim must agree with its own case's numbers
    n_checked = 0
    for a, k, y0, z0, verdict in rows:
        n_checked += 1
        if y0 <= MACHINE_LEVEL:
            assert "Y_0 is at machine level" in verdict, (a, k, y0, verdict)
        else:
            assert "Y_0 is NOT at machine level" in verdict, (a, k, y0, verdict)
        if z0 <= MACHINE_LEVEL:
            assert "Z_0 is roundoff" in verdict, (a, k, z0, verdict)
        else:
            assert "Z_0 is NOT roundoff" in verdict, (a, k, z0, verdict)
    assert n_checked == len(rows)
    print(f"    checked {n_checked} verdict sentences against their own Y_0/Z_0: all agree")
    print("[ok] SOUNDNESS: the verdict is now a measurement of its own dict, "
          f"not a constant ({len(false_rows)} of {len(rows)} cases correctly say NOT "
          "at machine level)")


# ---------------------------------------------------------------------------
# 2. SOUNDNESS (post-repair) -- N2_finite refuses non-finite input at p == 2
# ---------------------------------------------------------------------------
def test_n2_finite_certifies_poisoned_states_at_a_one_half():
    """`nan ** 0.0 == 1.0`, so pre-repair the cutoff ladder read 2.0 for ANY b at
    a = 1/2 -- all-NaN, all-inf, all-zero and garbage were ALL certified `True`, 4 of 4.

    Post-repair, `second_derivative_sup` requires `np.all(np.isfinite(e))` before
    computing the power (leg 109's own recommended repair): all-NaN and all-inf now
    report NaN cutoffs and `N2_finite = False`. all-zero and garbage stay `True`, and
    that is the CORRECT answer, not a residual gap: N''(e) = p(p-1) e^{p-2} = 2 for
    p == 2 and ANY finite e (including the e -> 0 limit at e = 0), so a finite input --
    however unphysical -- genuinely has sup|N''| = 2. Only nan/inf are undefined, and
    those are the two IEEE-754 exploits this repair closes.

    POSITIVE CONTROL: the SAME poisoned vectors at a = 0.3 (p = 3.33), where the ratio
    is not exactly 1.0 and the check must refuse everything but the finite garbage.
    """
    print("\n[2] SOUNDNESS: N2_finite at p == 2 exactly, post-repair")
    assert np.nan ** 0.0 == 1.0, "the whole mechanism -- IEEE-754; unchanged, now guarded"
    k = 32
    poisons = {"all_nan": np.full(k, np.nan), "all_inf": np.full(k, np.inf),
               "all_zero": np.zeros(k),
               "garbage": np.random.default_rng(0).normal(size=k)}
    certified = {}
    fin_by_name = {}
    for a in (0.5, 0.3):
        rp = ReducedProfile(a, K=k)
        n_true = 0
        fin_by_name[a] = {}
        for name, b in poisons.items():
            fin, npp = _n2_finite(rp, b)
            fin_by_name[a][name] = fin
            n_true += 1 if fin is True else 0
            print(f"    a={a} p={rp.p:.3f} {name:>8}: N2_finite={fin!s:>17} "
                  f"cutoffs={[f'{x:.4g}' for x in npp]}")
        certified[a] = n_true
    print(f"    certified True: a=0.5 -> {certified[0.5]} of 4 (was 4 of 4 pre-repair), "
          f"a=0.3 -> {certified[0.3]} of 4")
    # the two genuinely undefined states must now be refused
    assert fin_by_name[0.5]["all_nan"] is False, fin_by_name[0.5]
    assert fin_by_name[0.5]["all_inf"] is False, fin_by_name[0.5]
    # the two finite states are correctly True: N''(e) = 2 regardless of e's value
    assert fin_by_name[0.5]["all_zero"] is True, fin_by_name[0.5]
    assert fin_by_name[0.5]["garbage"] is True, fin_by_name[0.5]
    assert certified[0.5] == 2, certified          # nan/inf refused; zero/garbage correct
    assert certified[0.3] == 1, certified          # only the finite garbage; control works
    print("[ok] SOUNDNESS: at a = 1/2 all-NaN/all-inf are now refused (False); "
          "all-zero/garbage stay True because that IS the correct value")


# ---------------------------------------------------------------------------
# 3. SOUNDNESS (lesson 90) -- the cutoff ladder never decides anything
# ---------------------------------------------------------------------------
def test_the_cutoff_ladder_never_changes_the_answer():
    """N2_finite == (a <= 1/2) in every converged case; the ladder is decorative.

    The docstring presents the three-cutoff comparison as the evidence ("FLAT across
    cutoffs => finite"). It is not: for p > 2 the sup of e^{p-2} is attained in the
    INTERIOR, so the edge cutoff cannot move it, and every evaluated ratio is exactly
    1.0; for p < 2 the `p >= 2.0` conjunct short-circuits before any cutoff is read.
    """
    print("\n[3] lesson 90: does the ladder ever decide?")
    ratios, changed, n = set(), 0, 0
    for a in (0.1, 0.2, 0.3, 0.4, 0.45, 0.48, 0.5, 0.52, 0.6, 0.8, 1.0, 1.2):
        rp = ReducedProfile(a, K=48)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = rp.solve()
        if not r["converged"]:
            continue
        n += 1
        fin, npp = _n2_finite(rp, r["b"])
        if rp.p >= 2.0:
            ratios.add(round(max(npp) / min(npp), 9))
        changed += 0 if (fin == (a <= 0.5)) else 1
    print(f"    {n} converged cases; ladder changed the answer {changed} time(s)")
    print(f"    distinct cutoff ratios where the ratio was evaluated: {sorted(ratios)}")
    assert changed == 0, changed
    assert ratios == {1.0}, ratios
    print("[ok] the flag is decided by `a` alone; the ladder is decorative")


# ---------------------------------------------------------------------------
# 4. SOUNDNESS -- z0_defect is conservative, not corrupting
# ---------------------------------------------------------------------------
def test_z0_reports_the_larger_residual():
    """`np.linalg.inv` solves M X = I, so it guarantees ||M A - I||; the module reports
    ||A M - I||, the other one. Measured: the reported one is LARGER in every case, so
    this site is conservative. If this ever inverts, Z_0 has started under-reporting."""
    print("\n[4] which inversion residual does z0_defect report?")
    worst = 0.0
    for a in (0.3, 0.5, 0.8):
        for k in (32, 96):
            rp = ReducedProfile(a, K=k)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                r = rp.solve()
                if not r["converged"]:
                    continue
                M = rp.jacobian(r["b"], r["Xc"])
                A = np.linalg.inv(M)
                eye = np.eye(rp.K + 1)
                left = float(np.max(np.abs(A @ M - eye).sum(axis=1)))
                right = float(np.max(np.abs(M @ A - eye).sum(axis=1)))
                rep = float(z0_defect(rp, r["b"], r["Xc"]))
            assert rep == left, (rep, left)      # the reported one IS the left residual
            assert left >= right, (left, right)  # and it is the larger one
            worst = max(worst, left / right)
            print(f"    a={a} K={k}: reported(left)={left:.3e} right={right:.3e} "
                  f"ratio={left / right:7.1f} cond={np.linalg.cond(M):.2e}")
    assert worst > 5.0, worst
    print(f"[ok] conservative by up to {worst:.0f}x; not a corruption site")


# ---------------------------------------------------------------------------
# 5. SOUNDNESS (post-repair) -- an unrecognised `kind` now raises, not falls through
# ---------------------------------------------------------------------------
def test_step_adversary_kind_falls_through_to_the_adversary():
    """Pre-repair, any `kind` that was not exactly "single" silently returned the
    adversary -- 6 of 6 unrecognised strings, including the plausible typo "Single"
    (a stray capital). The naive probe is the module's designated CONTROL (its
    docstring: "kept as the CONTROL, because it reports a divergence that is purely the
    quadrature"), and a control reachable only by exact string match is a control that a
    typo switches off.

    Post-repair: `step_adversary` raises `ValueError` for any `kind` other than the two
    recognised strings, so a typo is loud, not silent.
    """
    print("\n[5] SOUNDNESS: step_adversary's kind dispatch now raises on typos")
    adversary = step_adversary(32, kind="step")
    control = step_adversary(32, kind="single")
    assert control != adversary, (control, adversary)   # the control is real
    unrecognised = ["typo", "", "STEP", "Single", "naive", None]
    raised = []
    for k in unrecognised:
        try:
            step_adversary(32, kind=k)
        except ValueError:
            raised.append(k)
    print(f"    adversary(step) = {adversary:.6f}   control(single) = {control:.6f}")
    print(f"    unrecognised kinds now raising ValueError: "
          f"{len(raised)} of {len(unrecognised)}  {raised}")
    assert len(raised) == len(unrecognised), (
        f"only {len(raised)} of {len(unrecognised)} raised -- some unrecognised kind is "
        f"still falling through silently: {[k for k in unrecognised if k not in raised]}")
    print("[ok] SOUNDNESS: 6 of 6 unrecognised kinds (including 'Single', a stray "
          "capital) now raise instead of silently returning the adversary")


# ---------------------------------------------------------------------------
# 6. SOUNDNESS -- poisoned b propagates everywhere except p == 2
# ---------------------------------------------------------------------------
def test_poisoned_coefficients_propagate():
    """A single NaN/inf coefficient must never produce a silently finite answer."""
    print("\n[6] single-coefficient poison through every public entry point")
    k = 32
    rp = ReducedProfile(0.3, K=k)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = rp.solve()
    b0, Xc = r["b"], r["Xc"]
    probes, silently_finite = 0, 0
    for poison in (np.nan, np.inf):
        for idx in (0, 5, k - 1):
            b = b0.copy()
            b[idx] = poison
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                for name, call in (
                        ("interpolant_defect", lambda: interpolant_defect(rp, b, Xc)),
                        ("z0_defect", lambda: z0_defect(rp, b, Xc)),
                        ("operator_norm", lambda: rp.operator_norm(b, Xc)),
                        ("second_derivative_sup",
                         lambda: max(second_derivative_sup(rp, b)))):
                    probes += 1
                    try:
                        if np.isfinite(float(call())):
                            silently_finite += 1
                            print(f"    SILENT: {name} poison={poison} idx={idx}")
                    except Exception:                      # noqa: BLE001
                        pass                               # raising is acceptable
    print(f"    {probes} probes, {silently_finite} silently finite")
    assert silently_finite == 0, silently_finite
    print("[ok] no absorption away from p == 2")


# ---------------------------------------------------------------------------
# 7. SOUNDNESS -- degenerate `a` never reaches a verdict
# ---------------------------------------------------------------------------
def test_degenerate_a_never_emits_a_verdict():
    """`__init__`'s guard `not 0.0 < float(a)` admits inf and 1e300; `rehearsal` must
    still refuse to emit a self-consistency verdict for them."""
    print("\n[7] degenerate a: what the constructor admits, and what rehearsal does")
    admitted, verdicts = 0, 0
    for a in (np.nan, np.inf, -np.inf, 0.0, -1.0, 1e-300, 1e300, 1e-12):
        try:
            ReducedProfile(float(a), K=16)
        except ValueError:
            print(f"    a={a!r:>10}: constructor rejects")
            continue
        admitted += 1
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = rehearsal(float(a), K=16)
        has_verdict = "verdict" in r
        verdicts += 1 if has_verdict else 0
        print(f"    a={a!r:>10}: ADMITTED, converged={r.get('converged')}, "
              f"verdict emitted={has_verdict}")
    print(f"    admitted by constructor: {admitted}; emitted a verdict: {verdicts}")
    assert admitted >= 4, admitted
    assert verdicts == 0, verdicts
    print("[ok] the constructor guard is incomplete but `converged` catches all of them")


if __name__ == "__main__":
    test_clean_reference_selfcheck()
    test_verdict_is_decoupled_from_the_numbers_it_asserts()
    test_n2_finite_certifies_poisoned_states_at_a_one_half()
    test_the_cutoff_ladder_never_changes_the_answer()
    test_z0_reports_the_larger_residual()
    test_step_adversary_kind_falls_through_to_the_adversary()
    test_poisoned_coefficients_propagate()
    test_degenerate_a_never_emits_a_verdict()
    print("\nAll leg-109 adversarial gates passed: 7 SOUNDNESS gates hold -- gates 1, 2 "
          "and 5 now confirm the bench repair (leg 109's three named fixes) closed the "
          "escalated gaps, and gates 3, 4, 6, 7 confirm nothing else regressed. If a "
          "gate fails, read experiments/journal/leg_109.md's 'Recommended repair' "
          "before touching anything.")
