"""Permanent adversarial regression test for solver/profile_newton.py (leg 202, Route-PNA).

WHAT THIS FILE IS.  Leg 202 ran the adversarial battery and THE GATE ANSWERED **YES**: 22
silent-wrong cases across three independent mechanisms.  The leg's territory forbade editing
`solver/profile_newton.py` under EITHER gate outcome, so this file is banked as a
**CHARACTERIZATION** test, exactly as leg 114 did for `solver/collocation_newton.py` and leg
92 for `solver/gclm.py` before their repairs:

  * checks named `check_KNOWN_GAP_*` pin the gaps **AS MEASURED**.  They assert the WRONG
    behaviour, on purpose, so that a later repair FAILS this file and is forced to record
    itself deliberately rather than sliding in.
  * checks named `check_ROBUST_*` pin behaviour that DID hold and still must: a repair may not
    buy the gaps back by breaking something that works.

`test_profile_newton.py` (6 gates) covers correctness on well-posed input and is untouched by
this file; this is the robustness complement, not a replacement.

THE GATE, VERBATIM
------------------
"Under adversarial and degenerate inputs (near-singular Jacobian, poor initial guess,
boundary-of-convergence parameters), does `solver/profile_newton.py` ever silently report a
converged solution that is not (a false-positive convergence claim), or silently return a
wrong value rather than reject/flag?"

ANSWER (leg 202): **YES**.  Three mechanisms, none of them the one the prior art already owned.

  M1  OFF-BRANCH ROOTS ARE RETURNED AS CONVERGED, WITH A MACHINE-ZERO RESIDUAL.  `R2` has
      spurious grid-scale roots that satisfy BOTH gauges to 0.0e+00 exactly and every residual
      row to machine precision.  Neither `solve` nor `continuation` computes any decay-class
      or smoothness diagnostic, so they are indistinguishable from the physical branch in
      every field the module returns.  Measured at n = 101, a = 1.05: `converged=True`,
      `relres = 4.17e-16`, far-field supremum 9.02 against the anchor's 6.48e-06 -- an
      inflation of **1.39e+06**, with sup|Omega| attained IN THE FAR FIELD and a node-to-node
      oscillation of 0.80 against the anchor's 0.09.  First departure is much earlier and much
      quieter: a = 0.45, n = 101, `converged=True`, `relres = 1.77e-15`, inflation **2079x**,
      reached on a WARM start with no retry involved.
      Consequence for the banked quantity: c(a = 1.50) is returned as 0.20427 / 0.23717 /
      0.97282 at n = 101 / 201 / 301, all three with `converged=True` and relres at machine
      zero (6.0e-16 / 5.8e-16 / 4.1e-15).  **79% relative spread, 376% between the extremes.**
      Vehicle: `continuation`'s retry clause (lines 182-189) accepts the spurious root because
      `alt["relres"] < r["relres"]`, then re-seeds the rest of the ladder from it via
      `if r["relres"] < 1e-10: om, c = ...`.

  M2  THE SCALING FAMILY IS ESCAPED AT DEFAULT PARAMETERS, AND THE GAUGES PAY FOR IT.  `R2`
      has an exact scaling degeneracy (Omega -> lam Omega with c -> lam c); the two gauge rows
      are the only thing pinning which member is returned, and they are 2 rows against n in an
      OVERDETERMINED least-squares solve, so they are tradeable.  From `om0 = 1e-8 * anchor`
      at n = 201 with nothing else touched: `converged=True`, `Omega(0) = -0.750000` instead
      of the gauged -1 (gauge residual **0.25**), and `c = -6127.935` against the true
      0.49797 -- a relative error of **1.23e+04**, with the sign flipped.  At eps = 1e-9 and
      1e-10 it is -30641.68 and -306421.26, i.e. c scales as 1/eps, which identifies the
      scaling family rather than roundoff.  `converged` never reads the gauge rows and
      `relres` is EXACTLY scale-invariant, so neither returned field can see it.

  M3  `c0` IS NEVER RANGE-CHECKED.  `solve(om0=anchor, c0=1e9)` returns `converged=True` with
      `c = 1.000000e+09` handed straight back -- the caller's own garbage returned as a
      converged wave speed, 9 orders from the true 0.498.

  M0  (PRIOR ART, pinned here only so a repair cannot silently change it.)  `converged=True`
      on iteration-capped stalls, because `max(1.0, hist[0])` pins the denominator at 1 and
      clause 1 collapses to an absolute `residual_rms < 1e-6` test.  `test_profile_newton.py`
      item (6) writes out the algebra and `experiments/journal/leg_71.md` banks an instance.
      This leg claims no credit for it.

ON THRESHOLDS AND FLOATING-POINT ENVIRONMENTS.  `test_profile_newton.py` item (6) is emphatic
that iteration-capped stalls in this module move **2.31 decades** across BLAS backends.  Every
assertion below is therefore either (a) EXISTENTIALLY quantified over a set of inputs, or
(b) a structural identity that does not depend on a stall level -- never an equality on a
stalled float.  The measured values are printed and recorded in the docstrings so that a
future environment can be compared against this one without the test being flaky.

Run: .venv/bin/python test_profile_newton_adversarial.py    (~60 s)
"""

import warnings

import numpy as np

from solver.profile_newton import TwoScaleNewton

LADDER = [0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05]


def _diag(nw, O):
    """The decay-class diagnostics the module never computes."""
    X = nw.fam.X
    outer = np.abs(X) > 0.5 * np.max(np.abs(X))
    a_ff = float(np.max(np.abs(nw.anchor()[outer])))
    ff = float(np.max(np.abs(O[outer])))
    sup = float(np.max(np.abs(O)))
    return {"farfield_sup": ff, "anchor_farfield_sup": a_ff, "inflation": ff / a_ff,
            "sup": sup, "osc": float(np.max(np.abs(np.diff(O))) / sup),
            "g1": float(O[nw.i0] + 1.0), "g2": float(O[nw.i1] + 0.5)}


def _ladder(n):
    """Reproduces `continuation`'s own warm-start + retry logic, keeping the profile."""
    out, om, c = [], None, 0.5
    for a in LADDER:
        nw = TwoScaleNewton(a=float(a), n=n)
        r = nw.solve(om0=om, c0=c)
        used = "warm"
        if r["relres"] > 1e-10:
            alt = nw.solve(om0=None, c0=0.5)
            if alt["relres"] < r["relres"]:
                r, used = alt, "retry"
        d = _diag(nw, r["Omega"])
        out.append({"a": a, "n": n, "used": used, "conv": bool(r["converged"]),
                    "relres": float(r["relres"]), "c": float(r["c"]),
                    "it": int(r["iterations"]), **d})
        if r["relres"] < 1e-10:
            om, c = r["Omega"], r["c"]
    return out


# ---------------------------------------------------------------------------
# M1 -- off-branch roots returned as converged
# ---------------------------------------------------------------------------
def check_KNOWN_GAP_M1_offbranch_root_reported_converged():
    """A machine-zero-residual root that is NOT a deformation of the anchor.

    AS MEASURED (n = 101): first departure a = 0.45, converged=True, relres 1.77e-15,
    inflation 2079x, on a WARM start.  Worst a = 1.05, relres 4.17e-16, inflation 1.39e+06,
    sup|Omega| = 9.02 attained in the far field, oscillation 0.80.
    """
    rows = _ladder(101)
    bad = [r for r in rows if r["conv"] and r["relres"] < 1e-10 and r["inflation"] > 1e2]
    assert bad, ("no off-branch root was returned as converged -- if this fails after a "
                 "repair, the repair is REAL and must be recorded; rows: %s"
                 % [(r["a"], r["conv"], "%.1e" % r["relres"], "%.1e" % r["inflation"])
                    for r in rows])
    worst = max(bad, key=lambda r: r["inflation"])
    first = min(bad, key=lambda r: r["a"])
    # the residual is genuinely at machine zero -- this is NOT the item (6) stall mechanism
    assert worst["relres"] < 1e-10, worst
    # the far field is not a rounding wobble: it is orders above the anchor's
    assert worst["inflation"] > 1e2, worst
    # and both gauges are satisfied, so the two-gauge design is NOT the defence here
    assert abs(worst["g1"]) < 1e-8 and abs(worst["g2"]) < 1e-8, worst
    print("[gap] M1 off-branch root returned CONVERGED: %d of %d ladder rows.  first "
          "a = %.2f (%s start, relres %.2e, far field x%.0f); worst a = %.2f (relres %.2e, "
          "far field x%.3g, sup|Omega| = %.3g, osc %.2f); both gauges exact to %.1e"
          % (len(bad), len(rows), first["a"], first["used"], first["relres"],
             first["inflation"], worst["a"], worst["relres"], worst["inflation"],
             worst["sup"], worst["osc"], max(abs(worst["g1"]), abs(worst["g2"]))))


def check_KNOWN_GAP_M1_c_disagrees_across_grids_at_machine_zero():
    """The same physical quantity, two grids, both `converged` at machine zero, different c.

    AS MEASURED HERE: c(a = 1.05) = 0.184112 at n = 101 (converged=True, relres 4.2e-16,
    inflation 1.39e+06) against 0.806733 at n = 201 -- 77.2% apart, with n = 101 the
    off-branch one.  The runner carries the sharper version on the full ladder to a = 1.50,
    where the three grids give 0.20427 / 0.23717 / 0.97282 (79% spread, 376% between the
    extremes) with ALL THREE reporting converged=True at machine-zero relres; that row is in
    writeup/data/p2_route_pna_v1_adversarial.json, not re-run here, to keep this file at ~8 s.
    """
    a_t = 1.05
    got = {}
    for n in (101, 201):
        rows = _ladder(n)
        r = [x for x in rows if x["a"] == a_t][0]
        got[n] = r
    # at least one grid returns a converged, machine-zero, OFF-BRANCH answer here
    off = [n for n, r in got.items() if r["conv"] and r["relres"] < 1e-10
           and r["inflation"] > 1e2]
    assert off, got
    spread = abs(got[101]["c"] - got[201]["c"]) / max(abs(got[101]["c"]),
                                                      abs(got[201]["c"]))
    print("[gap] M1 c(a = %.2f) = %.6f (n=101, relres %.1e, x%.3g) vs %.6f (n=201, relres "
          "%.1e, x%.3g) -- %.1f%% apart, off-branch at n = %s"
          % (a_t, got[101]["c"], got[101]["relres"], got[101]["inflation"],
             got[201]["c"], got[201]["relres"], got[201]["inflation"], 100 * spread, off))


# ---------------------------------------------------------------------------
# M2 -- the scaling-family escape, at DEFAULT parameters
# ---------------------------------------------------------------------------
def check_KNOWN_GAP_M2_scaling_family_escape_breaks_the_gauges():
    """A poor (small-amplitude) initial guess, nothing else touched.

    AS MEASURED (n = 201): eps = 1e-8 -> converged=True, Omega(0) = -0.750000 (gauge
    residual 0.25), c = -6127.935 against the true 0.49797.  eps = 1e-9 / 1e-10 give
    c = -30641.68 / -306421.26, i.e. c ~ 1/eps.
    """
    C_TRUE = 0.49797481
    nw = TwoScaleNewton(a=0.0, n=201)
    ex = nw.anchor()
    rows = []
    for eps in (1e-8, 1e-9, 1e-10):
        r = nw.solve(om0=eps * ex, c0=0.5)
        d = _diag(nw, r["Omega"])
        rows.append({"eps": eps, "conv": bool(r["converged"]), "c": float(r["c"]),
                     "relres": float(r["relres"]), "g1": d["g1"],
                     "relerr": abs(float(r["c"]) - C_TRUE) / C_TRUE})
    bad = [r for r in rows if r["conv"] and abs(r["g1"]) > 1e-3]
    assert bad, ("the scaling-family escape no longer fires -- a repair must record itself; "
                 "rows: %s" % rows)
    worst = max(bad, key=lambda r: r["relerr"])
    assert worst["relerr"] > 1e2, worst          # c wrong by >100x, measured 1.2e4..6.2e5
    assert abs(worst["g1"]) > 1e-3, worst        # measured 0.25
    print("[gap] M2 scaling-family escape at DEFAULT parameters: eps = %.0e -> "
          "converged=%s, Omega(0) = %+.6f (gauge residual %+.3f, gauged value is -1), "
          "c = %.3f against %.5f -- relative error %.3g, relres %.2e"
          % (worst["eps"], worst["conv"], worst["g1"] - 1.0, worst["g1"], worst["c"],
             C_TRUE, worst["relerr"], worst["relres"]))


def check_KNOWN_GAP_M2_relres_is_blind_to_the_scaling_family():
    """`relres` is a ratio of two quantities that both scale as lam^2, hence lam-invariant.

    AS MEASURED (n = 201, max_iter = 0): lam = 1, 2, 10 all report relres = 2.067e-07 to
    better than 1e-12 relative, while c is 0.5, 1.0, 5.0 and Omega(0) is -1, -2, -10.
    """
    nw = TwoScaleNewton(a=0.0, n=201)
    ex = nw.anchor()
    got = []
    for lam in (1.0, 2.0, 10.0):
        r = nw.solve(om0=ex * lam, c0=0.5 * lam, max_iter=0)
        got.append((lam, float(r["relres"]), float(r["c"])))
    rr = [g[1] for g in got]
    spread = (max(rr) - min(rr)) / max(rr)
    assert spread < 1e-9, got
    print("[gap] M2 `relres` is EXACTLY scale-invariant: lam = 1/2/10 give relres "
          "%.4e/%.4e/%.4e (spread %.1e) while c is %.2f/%.2f/%.2f -- the field a caller "
          "would use to detect this cannot"
          % (rr[0], rr[1], rr[2], spread, got[0][2], got[1][2], got[2][2]))


# ---------------------------------------------------------------------------
# M3 -- c0 is never range-checked
# ---------------------------------------------------------------------------
def check_KNOWN_GAP_M3_c0_returned_unchecked():
    """AS MEASURED (n = 101, max_iter = 5): c0 = 1e9 -> converged=True, c = 1.0e+09."""
    nw = TwoScaleNewton(a=0.0, n=101)
    ex = nw.anchor()
    rows = []
    for c0 in (1e6, 1e9, 1e12):
        r = nw.solve(om0=ex, c0=c0, max_iter=5)
        rows.append((c0, bool(r["converged"]), float(r["c"]), float(r["relres"])))
    bad = [r for r in rows if r[1] and abs(r[2]) > 1e3]
    assert bad, rows
    print("[gap] M3 `c0` is never range-checked: %s"
          % "; ".join("c0 = %.0e -> converged=%s, c = %.6e (relres %.2e)"
                      % (r[0], r[1], r[2], r[3]) for r in bad))


# ---------------------------------------------------------------------------
# M0 -- prior art, pinned so a repair cannot change it silently
# ---------------------------------------------------------------------------
def check_KNOWN_GAP_M0_converged_true_on_an_iteration_capped_stall():
    """PRIOR ART (test_profile_newton.py item (6); leg 71).  Pinned, not claimed.

    Existentially quantified over (a, n) precisely because item (6) measured this class of
    number moving 2.31 decades across BLAS backends.
    """
    hits = []
    for n in (101, 201):
        for a in (0.30, 0.45, 0.60, 0.90):
            r = TwoScaleNewton(a=a, n=n).solve()
            if r["converged"] and r["iterations"] >= 40 and r["relres"] > 1e-10:
                hits.append((n, a, float(r["relres"]), int(r["iterations"])))
    assert hits, ("no capped stall was reported converged in this environment -- item (6) "
                  "warns this is environment-dependent, so investigate before weakening")
    print("[gap] M0 (prior art) converged=True on a 40-iteration stall: %s"
          % "; ".join("n=%d a=%.2f relres %.2e at %d iters" % h for h in hits))


def check_KNOWN_GAP_M0_failure_path_omits_two_keys():
    """The LinAlgError branch returns a dict without `residual_rms`/`relres`.

    `continuation` reads `r["relres"]` unconditionally at line 182, so this is a live
    KeyError on a poisoned sweep -- LOUD, not silent, and recorded as a contract gap.
    """
    nw = TwoScaleNewton(a=0.0, n=101)
    bad = nw.anchor().copy()
    bad[7] = np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = nw.solve(om0=bad, c0=0.5, max_iter=3)
    missing = [k for k in ("residual_rms", "relres") if k not in r]
    assert missing == ["residual_rms", "relres"], sorted(r.keys())
    assert r["converged"] is False and "reason" in r, r
    print("[gap] M0 failure path returns %s -- missing %s that every success path carries; "
          "continuation() line 182 reads r['relres'] unconditionally"
          % (sorted(r.keys()), missing))


# ---------------------------------------------------------------------------
# ROBUST -- behaviour that held and must keep holding
# ---------------------------------------------------------------------------
def check_ROBUST_leg114_M2_constant_profile_is_killed_by_the_two_gauges():
    """leg 114 predicted this module immune to its own M2 vector.  It is.  Keep it that way.

    AS MEASURED (n = 201): om0 = -ones and om0 = zeros both return converged=False at
    relres 2.79e-03.
    """
    nw = TwoScaleNewton(a=0.0, n=201)
    for name, om0 in (("const_minus_one", -np.ones(201)), ("zeros", np.zeros(201))):
        r = nw.solve(om0=om0, c0=0.5)
        assert not r["converged"], (name, r["relres"], r["c"])
    print("[ok]  ROBUST leg 114's M2 constant-profile root is killed by the two gauges, "
          "exactly as leg 114 sec M2 predicted ('one gauge kills the scaling symmetry; it "
          "does not kill the constant. Two gauges do')")


def check_ROBUST_nonfinite_input_is_rejected_not_absorbed():
    """No NaN/Inf input is absorbed into a converged=True answer."""
    nw = TwoScaleNewton(a=0.0, n=101)
    ex = nw.anchor()
    bad_nan = ex.copy(); bad_nan[7] = np.nan
    bad_inf = ex.copy(); bad_inf[7] = np.inf
    cases = {"om0_nan": (bad_nan, 0.5), "om0_inf": (bad_inf, 0.5),
             "om0_all_nan": (np.full(101, np.nan), 0.5),
             "c0_nan": (ex, float("nan")), "c0_inf": (ex, float("inf"))}
    for name, (om0, c0) in cases.items():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = nw.solve(om0=om0, c0=c0, max_iter=5)
        assert not r["converged"], (name, r)
        assert r.get("reason") == "singular Jacobian", (name, r.get("reason"))
    print("[ok]  ROBUST all %d NaN/Inf inputs are rejected with reason='singular Jacobian', "
          "never absorbed into a converged answer" % len(cases))


def check_ROBUST_the_well_posed_anchor_still_converges_on_branch():
    """C1/C2: a repair may not buy the gaps back by breaking the case that works."""
    nw = TwoScaleNewton(a=0.0, n=201)
    ex = nw.anchor()
    r = nw.solve(om0=ex * 1.3 + 0.05 * np.exp(-nw.fam.X ** 2), c0=0.4)
    d = _diag(nw, r["Omega"])
    assert r["converged"] and r["relres"] < 1e-12, r["relres"]
    assert d["inflation"] < 10.0, d
    assert abs(d["g1"]) < 1e-10 and abs(d["g2"]) < 1e-10, d
    rows = _ladder(201)
    a03 = [x for x in rows if x["a"] == 0.30][0]
    assert a03["relres"] < 1e-10 and a03["inflation"] < 10.0, a03
    print("[ok]  ROBUST the well-posed solve is untouched: perturbed anchor -> relres %.1e, "
          "far-field inflation %.2f, gauges exact to %.1e; ladder a = 0.30 -> relres %.1e, "
          "inflation %.2f"
          % (r["relres"], d["inflation"], max(abs(d["g1"]), abs(d["g2"])),
             a03["relres"], a03["inflation"]))


def check_ROBUST_jacobian_still_matches_finite_differences():
    """C3: if this moves, every other verdict is about the derivative, not the guards."""
    nw = TwoScaleNewton(a=0.3, n=201)
    om = nw.anchor() * 0.9
    J = nw.jacobian(om, 0.6)
    rng = np.random.default_rng(4)
    worst = 0.0
    for _ in range(4):
        h = rng.normal(size=201) * 1e-6
        fd = (nw.residual(om + h, 0.6) - nw.residual(om - h, 0.6)) / 2.0
        worst = max(worst, float(np.max(np.abs(fd - J[:201, :201] @ h))
                                 / max(np.max(np.abs(fd)), 1e-30)))
    assert worst < 1e-6, worst
    print("[ok]  ROBUST the analytic Jacobian still matches finite differences to %.1e "
          "(leg 71 measured 6.7e-11 on a different host)" % worst)


CHECKS = [check_KNOWN_GAP_M1_offbranch_root_reported_converged,
          check_KNOWN_GAP_M1_c_disagrees_across_grids_at_machine_zero,
          check_KNOWN_GAP_M2_scaling_family_escape_breaks_the_gauges,
          check_KNOWN_GAP_M2_relres_is_blind_to_the_scaling_family,
          check_KNOWN_GAP_M3_c0_returned_unchecked,
          check_KNOWN_GAP_M0_converged_true_on_an_iteration_capped_stall,
          check_KNOWN_GAP_M0_failure_path_omits_two_keys,
          check_ROBUST_leg114_M2_constant_profile_is_killed_by_the_two_gauges,
          check_ROBUST_nonfinite_input_is_rejected_not_absorbed,
          check_ROBUST_the_well_posed_anchor_still_converges_on_branch,
          check_ROBUST_jacobian_still_matches_finite_differences]


if __name__ == "__main__":
    np.seterr(all="ignore")
    for fn in CHECKS:
        fn()
    print("\nALL PROFILE-NEWTON ADVERSARIAL CHECKS PASSED "
          "(7 pin OPEN defects as measured; 4 pin robustness that must not regress)")
