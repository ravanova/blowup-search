"""Gates for solver/literature_gates.py -- the primary-source pass.

  (1) THE EXPONENT DICTIONARY.  ALS/XU write omega ~ tau^-beta f(x/tau^c_l); we write
      omega ~ tau^-1 with L ~ tau^beta_ours and alpha := 1/beta_ours.  So THEIR c_l is
      OUR 1/alpha, and their Lambda^s is our (-Delta)^{s/2}.  Get this wrong and every
      other gate here inverts its verdict while still passing.  It goes first.
  (2) SCHOCHET'S CONSTANT.  ALS §5.1 correct a 1986 CPAM value.  We settle it from our
      own side: the residual of the complex Burgers equation on the exact pole ansatz,
      analytically differentiated.  The gate is on the SEPARATION between the two
      candidates, not on one of them passing a threshold.
  (3) ROUTE-H's (E) IS ALS (57)-(58).  This is a retraction written as a test: an
      explicit parameter map, pointwise agreement at four times, ALS's own t_c formula
      returning our T, and (E) landing on ALS's blow-up branch rather than near it.
  (4) alpha(1/2) = 3 FROM THE PUBLISHED a = 1/2 SYSTEM, integrated cold -- no shared
      grid, basis, or code with our compactified Newton solve.  With the refusal gate
      that a loose first version did not have: what must stay resolvable is d tau, the
      quantity the difference quotient divides by, NOT tau.  Gated on the rungs that
      actually turn over, so the gate is tested rather than merely present.
  (5) THE SUPERCRITICAL BALANCE, measured.  Schochet collapses at beta = 2 and not at
      beta = 1, and -- the part that makes it a measurement rather than a four-way fit
      -- the beta = 2 residual SHRINKS on deeper sub-ladders, which is ALS's stated
      O(tau^-1) correction behaving as stated.
  (6) OUR BRANCH AGAINST XU's, read from the COMMITTED Route-E/F JSON so the comparison
      cannot drift from the data, and compared at XU's own stated accuracy rather than
      at ours.  Includes the gate that we are the LEAST accurate source on a_c.
  (7) THE LEDGER DOES NOT ROT.  Every claim names a source, a verdict from a closed
      vocabulary, and what survives.

Run: .venv/bin/python test_literature_gates.py
"""

import json
from pathlib import Path

import numpy as np

from solver.critical_dissipation import exact_a0_spacetime
from solver.literature_gates import (
    CHEN_HOU_BETA, CLAIM_LEDGER, LSS_A_C, PRIMARY_SOURCES, XU_TABLE1,
    a_half_branch, a_half_verdict, als_a0_sigma1, als_a0_sigma1_tc, collapse_spread,
    compare_branch, ledger_counts, ours_alpha_from_cl, ours_s_c, rescaled_collapse,
    route_h_E_as_als, schochet_K, schochet_blowup_time, schochet_pde_residual,
    supercritical_beta, xu_s_star,
)

DATA = Path(__file__).resolve().parent / "writeup" / "data"


def _close(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


# --------------------------------------------------------------------------
def test_1_exponent_dictionary():
    for c_l in (1.0, 0.8730, 1.0 / 3.0, 0.0775):
        assert _close(ours_alpha_from_cl(c_l), xu_s_star(c_l), 1e-14)
        assert _close(ours_s_c(ours_alpha_from_cl(c_l)), 0.5 * xu_s_star(c_l), 1e-14)
    assert _close(ours_alpha_from_cl(1.0), 1.0, 1e-14)
    assert _close(ours_alpha_from_cl(1.0 / 3.0), 3.0, 1e-14)
    print("  c_l -> alpha is 1/x on both anchors; our s_c is half XU's s* identically OK")


def test_2_schochet_constant():
    worst_corr = max(schochet_pde_residual(schochet_K(s, corrected=True), nu=nu, t=t)
                     for s in (+1, -1) for nu, t in ((1.0, 0.01), (1.0, 0.02), (0.4, 0.05)))
    best_print = min(schochet_pde_residual(schochet_K(s, corrected=False), nu=nu, t=t)
                     for s in (+1, -1) for nu, t in ((1.0, 0.01), (1.0, 0.02), (0.4, 0.05)))
    assert worst_corr < 1e-12, worst_corr
    assert best_print > 1e-3, best_print
    dec = np.log10(best_print / worst_corr)
    assert dec > 10, dec
    # ALS (44) against the pole geometry, which is closed-form for poles on the -i axis
    K = schochet_K(+1, corrected=True)
    assert _close(schochet_blowup_time(-1j, -2j, 1.0, K), 8.0 / ((5.0 / 3.0) * K), 1e-13)
    print(f"  corrected 24(3+-sqrt6) residual {worst_corr:.2e}; printed 12(6+-sqrt6) "
          f"{best_print:.2e}; {dec:.1f} decades apart.  t_c matches the geometry  OK")


def test_3_route_h_E_is_als_57():
    x = np.linspace(-8.0, 8.0, 2001)
    worst = 0.0
    for mu0, nu, T in ((0.7, 1.3, 2.0), (3.1, 0.25, 5.0), (0.05, 1.0, 1.0)):
        m = route_h_E_as_als(mu0, nu, T)
        assert m["w_m1_0"] < -nu, "must land on ALS's blow-up branch Re w_{-1}(0) < -nu"
        assert _close(m["dvc_dt_from_als"], m["dvc_dt_from_E"], 1e-13)
        assert _close(als_a0_sigma1_tc(m["w_m1_0"], m["vc0"], nu), T, 1e-13)
        for frac in (0.0, 0.45, 0.85, 0.99):
            a = als_a0_sigma1(x, frac * T, m["w_m1_0"], m["vc0"], nu)
            b = exact_a0_spacetime(x, frac * T, nu, mu0, T=T)["omega"]
            r = float(np.max(np.abs(a - b)) / np.max(np.abs(b)))
            worst = max(worst, r)
            assert r < 1e-12, (mu0, nu, T, frac, r)
    print(f"  (E) == ALS (57)-(58) on 3 parameter sets x 4 times, worst {worst:.2e}; "
          f"t_c formula returns T exactly  OK  [Route-H (E) is PRE-EMPTED]")


def test_4_alpha_half_is_three_from_als():
    br = a_half_branch(Om0=10.0, n=120_000)
    v = a_half_verdict(br, frac=0.9)
    assert not v["refused"]
    assert _close(v["c_l"], 1.0 / 3.0, 2e-3), v["c_l"]
    assert _close(v["alpha_ours"], 3.0, 2e-3), v["alpha_ours"]
    assert _close(v["dlogOmega_dlogvc"], -2.0, 1e-3), v["dlogOmega_dlogvc"]
    print(f"  c_l = {v['c_l']:.9f} vs 1/3 (rel {v['c_l_rel_err']:.1e}) => "
          f"alpha(1/2) = {v['alpha_ours']:.6f}; Omega ~ v_c^{v['dlogOmega_dlogvc']:.5f}  OK")


def test_5_dtau_gate_refuses_the_turnover():
    br = a_half_branch(Om0=10.0, n=120_000)
    bad = (~br["resolved"]) & (br["tau"] > 0)
    assert bad.sum() > 0, "the run must reach the floor or the gate is untested"
    assert np.all(br["dtau"][bad] <= br["dtau_floor"])
    deepest = np.flatnonzero(bad)[-50:]
    off = float(np.min(np.abs(br["c_l_local"][deepest] - 1.0 / 3.0)))
    assert off > 1e-3, off
    # and tau itself is still enormous compared to underflow there -- which is exactly
    # why a threshold on tau could not have caught this
    assert float(np.min(br["tau"][deepest])) > 1e-300
    print(f"  {int(bad.sum())} rungs refused on d tau; the deepest would have read c_l "
          f"off by >= {off:.1e} while tau there is {float(np.min(br['tau'][deepest])):.1e}  OK")


def test_6_supercritical_balance():
    K, nu = schochet_K(+1, corrected=True), 1.0
    taus = [1e-3, 3e-4, 1e-4, 3e-5, 1e-5]
    xi, curves, _ = rescaled_collapse(-1j, -2j, nu, K, taus)
    s = {b: collapse_spread(xi, curves, b) for b in (1.0, 1.5, 2.0, 2.5)}
    assert min(s, key=lambda b: s[b]) == 2.0, s
    assert s[1.0] / s[2.0] > 20, s
    sp = [collapse_spread(xi, {t: curves[t] for t in taus[lo:]}, 2.0)
          for lo in range(len(taus) - 2)]
    assert sp == sorted(sp, reverse=True), sp
    assert sp[0] / sp[-1] > 5, sp
    assert _close(supercritical_beta(2.0, 1.0), 2.0, 1e-14)
    assert _close(supercritical_beta(1.0, 1.0), 1.0, 1e-14)
    print(f"  spread(beta=1)/spread(beta=2) = {s[1.0] / s[2.0]:.0f}; the beta=2 residual "
          f"falls {sp[0]:.2e} -> {sp[-1]:.2e} on deeper ladders (ALS's O(tau) term)  OK")


def test_7_branch_against_xu():
    f = json.loads((DATA / "p2_route_f_v1_viscosity.json").read_text())
    rows = compare_branch(f["F6_sc_map"]["rows"])
    assert len(rows) >= 6, len(rows)
    worst = max(r["rel_diff"] for r in rows)
    assert worst < 5e-3, worst           # XU claim 2-3 s.f. at nonzero a; compare there
    ex = {r["a"]: r for r in rows}
    assert ex[0.0]["rel_diff"] < 1e-12 and ex[0.5]["rel_diff"] < 1e-12
    e = json.loads((DATA / "p2_route_e_v1_spectrum.json").read_text())
    ours_ac = float(e["E7_end"]["a_c_linear_extrapolation"])
    ours_err = abs(ours_ac - LSS_A_C) / LSS_A_C
    xu_err = abs(0.6888 - LSS_A_C) / LSS_A_C
    assert ours_err > xu_err, "if this fails we became the better source -- say so"
    assert ours_err < 0.02, ours_err
    for a, c_l, s_star in XU_TABLE1:
        assert _close(s_star, 1.0 / c_l, 2e-3), a
    cls = [c for _, c, _ in XU_TABLE1]
    assert cls == sorted(cls, reverse=True)
    print(f"  our alpha(a) vs XU s*(a): worst {worst:.2e} over {len(rows)} rows, exact at "
          f"a=0 and a=1/2; a_c ours {ours_err:.2%} vs XU {xu_err:.2%}  OK  [F PRE-EMPTED]")


def test_8_ledger_does_not_rot():
    allowed = {"PRE-EMPTED", "CONFIRMED_AND_PRE-EMPTED", "PRE-EMPTED_AND_RE-CLASSIFIED",
               "PARTIAL", "SURVIVES", "OPEN_QUESTION_ANSWERED_BY_THE_LITERATURE",
               "UNSEARCHED_AT_PRIMARY_SOURCE", "CONFIRMED (never claimed as ours)"}
    for c in CLAIM_LEDGER:
        assert c["verdict"] in allowed, c["verdict"]
        assert c["claim"] and c["leg"] and c["source"] and c.get("survives")
    counts = ledger_counts()
    assert sum(counts.values()) == len(CLAIM_LEDGER)
    lost = sum(v for k, v in counts.items() if "PRE-EMPTED" in k)
    assert lost >= 6, counts
    for aid in ("2207.07548", "2607.19762", "2210.07191", "2209.08232"):
        s = PRIMARY_SOURCES[aid]
        assert s["read"] and s["gates"] and s["venue"]
    assert _close(CHEN_HOU_BETA, 2.9205600, 1e-9)
    print(f"  {len(CLAIM_LEDGER)} claims, {lost} pre-empted; every entry names a source "
          f"and what survives  OK")


def test_9_artifact_matches_the_module():
    p = DATA / "p2_route_j_v1_literature.json"
    if not p.exists():
        print("  SKIP -- run experiments/p2_route_j_v1_literature.py first")
        return
    d = json.loads(p.read_text())
    assert d["J6_ledger"]["n_claims"] == len(CLAIM_LEDGER)
    assert d["J2_route_h_E_is_als"]["worst_rel_diff"] < 1e-12
    assert d["J2_route_h_E_is_als"]["tc_abs_err"] == 0.0
    assert d["J1_schochet_constant"]["separation_decades"] > 10
    assert _close(d["J3_alpha_half_from_als"]["verdict_row"]["c_l"], 1.0 / 3.0, 2e-3)
    assert d["J4_supercritical"]["best_beta"] == 2.0
    assert d["J5_branch_vs_xu"]["worst_rel_diff"] < 5e-3
    print("  committed JSON agrees with a fresh call on all six headline numbers  OK")


# ==========================================================================
# ROUTE-CP v1 (leg 62): Cadiot's own hypotheses, re-derived rather than trusted
# ==========================================================================
def test_10_cadiot_assumption1_holds_at_his_own_published_parameters():
    """CP5.  If this failed, leg 62's whole reading of the paper would be wrong.

    Assumption 1 requires `l_min > 0` AND `|l| -> infinity`.  Both are recomputed from
    the published symbols at the published parameters, and both are asserted with their
    MAGNITUDE.
    """
    from solver.literature_gates import cadiot_assumption1_check
    c = cadiot_assumption1_check()

    sh = c["swift_hohenberg"]
    # |l(xi)| = |(1-|2 pi xi|^2)^2 + mu| is minimised where |2 pi xi|^2 = 1, giving mu
    assert abs(sh["l_min_measured"] - sh["l_min_expected_analytic"]) < 1e-4, sh
    assert sh["l_min_measured"] > 0.0 and sh["assumption1_l_min_positive"]
    assert abs(sh["growth_exponent"] - 4.0) < 1e-3, sh["growth_exponent"]

    wh = c["whitham"]
    # T = 0.5 > 1/3, so m_T increases from m_T(0) = 1 and inf|l| = 1 - c = 0.2
    assert abs(wh["l_min_measured"] - 0.2) < 1e-6, wh["l_min_measured"]
    assert abs(wh["growth_exponent"] - 0.5) < 5e-3, wh["growth_exponent"]

    gs = c["gray_scott"]
    # lower-triangular symbol: det = d11 * d22, minimised at xi = 0 at 1 * lambda2 = 10
    assert abs(gs["sigma0_measured"] - gs["sigma0_expected_analytic"]) < 1e-6, gs
    assert gs["cb_assumption1_det_bounded_away_from_zero"]
    assert gs["offdiagonal_entry"] == 189.0, gs["offdiagonal_entry"]

    print(f"  SH: l_min={sh['l_min_measured']:.4f} (=mu), growth "
          f"{sh['growth_exponent']:.4f}")
    print(f"  Whitham: l_min={wh['l_min_measured']:.4f} (=1-c), growth "
          f"{wh['growth_exponent']:.4f}")
    print(f"  Gray-Scott: sigma0={gs['sigma0_measured']:.3f} (=lambda2), "
          f"off-diagonal entry {gs['offdiagonal_entry']:.0f} CONSTANT")


def test_11_the_one_offdiagonal_entry_in_the_corpus_is_dominated():
    """CP3.  Gray-Scott is the only place Cadiot's LINEAR part has an off-diagonal entry.

    It is a constant while the diagonal grows quadratically, so the dominance ratio
    DECAYS.  The point is not that a crossover exists -- it is that rho decays at all;
    ours is +infinity at every index.
    """
    from solver.literature_gates import cadiot_gray_scott_crossover
    d = cadiot_gray_scott_crossover()
    assert d["offdiagonal_entry"] == 189.0
    # at the crossover the ratio is exactly 1, and it falls away like |xi|^-2 after it
    assert abs(d["rho_at_probe"][0] - 1.0) < 1e-9, d["rho_at_probe"][0]
    assert abs(d["rho_decay_exponent"] + 2.0) < 1e-2, d["rho_decay_exponent"]
    assert d["rho_at_probe"][-1] < 1e-3, d["rho_at_probe"][-1]
    assert 2.0 < d["crossover_xi"] < 2.2, d["crossover_xi"]
    print(f"  off-diagonal 189 constant vs diagonal ~|2 pi xi|^2: crossover at "
          f"xi={d['crossover_xi']:.4f}, rho decays with exponent "
          f"{d['rho_decay_exponent']:+.4f}")
    print(f"  rho at 100x the crossover: {d['rho_at_probe'][-1]:.2e}  "
          f"(ours: +inf at every index)")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_exponent_dictionary,
               test_2_schochet_constant,
               test_3_route_h_E_is_als_57,
               test_4_alpha_half_is_three_from_als,
               test_5_dtau_gate_refuses_the_turnover,
               test_6_supercritical_balance,
               test_7_branch_against_xu,
               test_8_ledger_does_not_rot,
               test_9_artifact_matches_the_module,
               test_10_cadiot_assumption1_holds_at_his_own_published_parameters,
               test_11_the_one_offdiagonal_entry_in_the_corpus_is_dominated):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
