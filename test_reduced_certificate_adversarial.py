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

Answered **YES**, on three independent sites. Leg 109 had NO patch authority under its own
gate — its yes-branch reads "Report the exact failing case precisely; escalate, do not
patch under this leg's own authority" — so `solver/reduced_certificate.py` is byte-
identical to `origin/main` and the three gaps are OPEN. Gates 1, 2 and 5 below are
therefore **CHARACTERIZATION** gates: they assert that the gap is open, at the measured
magnitude, so the escalation is executable rather than a memory (lesson 68).

  | gate | site | leg 109 measured |
  |---|---|---|
  | 1 | `rehearsal`'s hardcoded `verdict` | 1 distinct verdict string over 15 converged (a,K) cases whose Y_0 spans 10.1 orders of magnitude; 14 of 15 assert "machine level" where Y_0 > 1e-10 |
  | 2 | `N2_finite` at p == 2 exactly | 4 of 4 poisoned states (all-NaN, all-inf, all-zero, garbage) certified `True` at a = 1/2, because `nan ** 0.0 == 1.0` |
  | 3 | the three-cutoff ladder | 0 of 16 cases where it changed the answer away from `a <= 1/2`; every evaluated ratio is exactly 1.0 (lesson 90) |
  | 4 | `z0_defect`'s residual side | reports the LEFT residual, 9.6x-278x LARGER than the right one — conservative, NOT corrupting |
  | 5 | `step_adversary`'s `kind` dispatch | 6 of 6 unrecognised strings silently return the adversary; only exact `"single"` reaches the control |
  | 6 | poisoned `b` away from p == 2 | 0 of 24 probes silently finite — the module propagates correctly everywhere else |
  | 7 | degenerate `a` | 4 of 8 admitted by the constructor, 4 of 4 caught by `converged=False`, 0 emitted a verdict |

**IF GATE 1, 2 OR 5 FAILS, THAT IS VERY LIKELY GOOD NEWS** — someone has repaired the
gap. The correct response is to read leg 109's escalation
(`experiments/journal/leg_109.md`, section "Recommended repair"), confirm the fix, and
convert the characterization gate to a SOUNDNESS gate asserting the repaired property,
keeping the pre-repair magnitude on the record. It must NOT be "fixed" by loosening a
tolerance, and it must not be fixed by deleting the gate.

Gates 3, 4, 6 and 7 assert properties that HOLD today. If one of those fails, the module
has started absorbing bad input somewhere it previously flagged it, and the response is to
fix the module.

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
    """`rehearsal`'s own N2_finite expression, reproduced verbatim from line 220."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        npp = second_derivative_sup(rp, b)
    if not (rp.p >= 2.0):                 # Python short-circuits before the ratio
        return False, npp
    try:
        return bool(max(npp) / min(npp) < 1.01), npp
    except ZeroDivisionError:
        return "ZeroDivisionError", npp


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
    is TRUE. Without this row, "14 of 15" would be indistinguishable from a broken build.
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
# 1. CHARACTERIZATION -- the verdict is a constant, not a measurement
# ---------------------------------------------------------------------------
def test_verdict_is_decoupled_from_the_numbers_it_asserts():
    """`rehearsal` emits one hardcoded sentence for every input (leg 109, finding A).

    The sentence asserts "Y_0 is at machine level and Z_0 is roundoff". Nothing in
    `rehearsal` reads `Y0_interpolant_defect` or `Z0` before emitting it, so there is no
    input for which it can come out differently — lesson 90's shape, applied to a claim.
    """
    print("\n[1] CHARACTERIZATION: the verdict sentence vs the numbers beside it")
    rows, verdicts = [], set()
    for a in (0.3, 0.5, 0.8, 1.0, 1.2):
        for k in (16, 32, 96):
            r = _rehearse(a, k)
            if not r.get("converged"):
                continue
            verdicts.add(r["verdict"])
            rows.append((a, k, r["Y0_interpolant_defect"]))
    y0s = [y for _, _, y in rows]
    false_rows = [t for t in rows if t[2] > MACHINE_LEVEL]
    worst = max(rows, key=lambda t: t[2])
    spread = np.log10(max(y0s) / min(y0s))
    print(f"    {len(rows)} converged cases, {len(verdicts)} distinct verdict string(s)")
    print(f"    Y_0 spans {min(y0s):.3e} .. {max(y0s):.3e}  ({spread:.2f} orders)")
    print(f"    asserting 'machine level' where Y_0 > {MACHINE_LEVEL:g}: "
          f"{len(false_rows)} of {len(rows)}")
    print(f"    worst: a={worst[0]}, K={worst[1]}, Y_0 = {worst[2]:.4e}")
    assert len(verdicts) == 1, (
        f"{len(verdicts)} distinct verdicts -- if this is now > 1 the verdict may have "
        "been wired to the measurement; see the module docstring above")
    assert "Y_0 is at machine level" in verdicts.pop()
    assert len(false_rows) >= 14, len(false_rows)
    assert spread > 9.0, spread
    assert worst[2] > 1e-3, worst          # a=0.3, K=16 reaches 1.5e-2
    print("[ok] CHARACTERIZED: one sentence, 10+ orders of magnitude beneath it")


# ---------------------------------------------------------------------------
# 2. CHARACTERIZATION -- N2_finite certifies garbage at p == 2 exactly
# ---------------------------------------------------------------------------
def test_n2_finite_certifies_poisoned_states_at_a_one_half():
    """`nan ** 0.0 == 1.0`, so at a = 1/2 the cutoff ladder is 2.0 for ANY b.

    POSITIVE CONTROL: the SAME poisoned vectors at a = 0.3 (p = 3.33), where the check
    must refuse. The two code paths differ only in the exponent, so a control that comes
    out differently is what makes the a = 1/2 row a finding.
    """
    print("\n[2] CHARACTERIZATION: N2_finite at p == 2 exactly")
    assert np.nan ** 0.0 == 1.0, "the whole mechanism -- IEEE-754"
    k = 32
    poisons = {"all_nan": np.full(k, np.nan), "all_inf": np.full(k, np.inf),
               "all_zero": np.zeros(k),
               "garbage": np.random.default_rng(0).normal(size=k)}
    certified = {}
    for a in (0.5, 0.3):
        rp = ReducedProfile(a, K=k)
        n_true = 0
        for name, b in poisons.items():
            fin, npp = _n2_finite(rp, b)
            n_true += 1 if fin is True else 0
            print(f"    a={a} p={rp.p:.3f} {name:>8}: N2_finite={fin!s:>17} "
                  f"cutoffs={[f'{x:.4g}' for x in npp]}")
        certified[a] = n_true
    print(f"    certified True: a=0.5 -> {certified[0.5]} of 4, "
          f"a=0.3 -> {certified[0.3]} of 4")
    assert certified[0.5] == 4, certified          # every poison certified
    assert certified[0.3] == 1, certified          # only the finite garbage; control works
    print("[ok] CHARACTERIZED: at a = 1/2 the check certifies an all-NaN state; "
          "at a = 0.3 the same states are refused")


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
# 5. CHARACTERIZATION -- the designated control is reachable only by exact string
# ---------------------------------------------------------------------------
def test_step_adversary_kind_falls_through_to_the_adversary():
    """Any `kind` that is not exactly "single" returns the adversary, silently.

    The naive probe is the module's designated CONTROL (its docstring: "kept as the
    CONTROL, because it reports a divergence that is purely the quadrature"). A control
    reachable only by exact string match is a control that a typo switches off.
    """
    print("\n[5] CHARACTERIZATION: step_adversary's kind dispatch")
    adversary = step_adversary(32, kind="step")
    control = step_adversary(32, kind="single")
    assert control != adversary, (control, adversary)   # the control is real
    unrecognised = ["typo", "", "STEP", "Single", "naive", None]
    fell = [k for k in unrecognised if step_adversary(32, kind=k) == adversary]
    print(f"    adversary(step) = {adversary:.6f}   control(single) = {control:.6f}")
    print(f"    unrecognised kinds silently returning the adversary: "
          f"{len(fell)} of {len(unrecognised)}  {fell}")
    assert len(fell) == len(unrecognised), fell
    print("[ok] CHARACTERIZED: 6 of 6 fall through; 'Single' (a capital) is not the "
          "control")


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
    print("\nAll leg-109 adversarial gates passed: 4 SOUNDNESS gates hold, and 3 "
          "CHARACTERIZATION gates (1, 2, 5) confirm the escalated gaps are still open. "
          "If a characterization gate fails, read experiments/journal/leg_109.md before "
          "touching anything.")
