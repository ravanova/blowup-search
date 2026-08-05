"""Gates for solver/viscous_novelty.py -- stage V's pre-committed novelty check.

The whole leg is a claim about the LITERATURE ("someone already did this"), and a claim
about the literature that cannot be re-run is exactly as durable as a figure looked at
once. So the gates are re-derivations, not assertions:

  (1) THE LEDGER IS WELL-FORMED AND THE VERDICT COMES FROM IT.  Every entry carries the
      six fields the gate needs; `novelty_verdict()` reads them rather than remembering
      an answer, and it must return YES with at least one PRE_EMPTS entry.
  (2) THE PUBLISHED NLS ZEROS REPRODUCE, from an independent integrator and an
      independently derived far-field expansion. Case I j=1 and Case II j=1 must land on
      Dahne-Figueras Tables 1 and 2 within 1e-06.
  (3) IT REPRODUCES MORE THAN ONE ROW.  Four rows of Table 1, so the machinery is not
      tuned to a single point.
  (4) THE DEFECT DISCRIMINATES.  Perturbing kappa by 1e-04 must raise the matching defect
      by at least 100x -- a residual that is small everywhere would gate nothing
      (lesson 55: check a diagnostic on a case you know is bad).
  (5) THE INTEGRATOR IS RESOLVED, and the far-field truncation is measured rather than
      assumed: halving the step must move the defect by less than the defect itself, and
      the (mu, kappa) it returns must be stable across matching points xi_1.
  (6) THE DISSIPATION BRANCH FOLDS, AND AT THEIR NUMBER.  Continuing branch j=1 in the
      dissipation dial must produce an interior maximum in eps, and it must agree with
      the fold read off their own Fig. 1a to 1e-05.
  (7) THE MARGIN PROXY BEHAVES LIKE ONE.  ||J^-1|| at the fold must exceed its value in
      mid-branch by at least 10x -- the certificate dies AT the fold, not at eps = 0.
  (8) THE FIGURE-READING CALIBRATION CHECKS ITSELF (skipped when Papers/ is empty, which
      is the normal state of a rebuilt container): the eight curves of Fig. 1a must start
      on the eight kappa of Table 1, which is transcribed from a different page.

Run: .venv/bin/python test_viscous_novelty.py
"""

import os
import time

import numpy as np

from solver.viscous_novelty import (
    DF_FIG1A_BRANCH1_FOLD, DF_FIG1A_CALIBRATION_RESIDUAL, DF_TABLE1, DF_TABLE2,
    PRECEDENTS, branch_in_kappa, fold_of, margin_proxy, match_defect, novelty_verdict,
    read_df_figure, resolution_ladder, shoot_newton, xi1_ladder,
)

PDF = "Papers/2410.05480.pdf"


def test_1_ledger_is_well_formed_and_the_verdict_reads_it():
    fields = {"id", "who", "what", "dial", "rigor", "verdict", "gate"}
    for p in PRECEDENTS:
        assert fields <= set(p), f"{p.get('id')} is missing {fields - set(p)}"
        assert p["verdict"] in ("PRE_EMPTS", "ADJACENT", "EXCLUSION"), p["verdict"]
        assert len(p["what"]) > 60, f"{p['id']}: 'what' is too thin to say what was checked"
    answer, pre = novelty_verdict()
    assert answer == "YES" and pre, "the gate must report YES off the ledger"
    assert any(p["id"].startswith("arXiv:2410.05480") for p in pre)
    print(f"  {len(PRECEDENTS)} entries, verdict {answer}, "
          f"{len(pre)} pre-empting: {[p['id'] for p in pre]}  OK")


def test_2_published_nls_zeros_reproduce():
    j, mu_p, kap_p, _ = DF_TABLE1[0]
    (mu, kap), hist = shoot_newton(round(mu_p, 3), round(kap_p, 3), 0.0, 1, 2.3, 15.0)
    d1 = (abs(mu - mu_p), abs(kap - kap_p))
    assert max(d1) < 1e-6, f"Case I j=1 off by {d1}"
    assert hist[-1] < 1e-11, hist[-1]

    j, mu_p, kap_p, _ = DF_TABLE2[0]
    (mu2, kap2), hist2 = shoot_newton(round(mu_p, 3), round(kap_p, 3), 0.0, 3, 1.0, 40.0)
    d2 = (abs(mu2 - mu_p), abs(kap2 - kap_p))
    assert max(d2) < 1e-6, f"Case II j=1 off by {d2}"
    assert hist2[-1] < 1e-11, hist2[-1]
    print(f"  Case I  j=1: dmu={d1[0]:.1e} dkappa={d1[1]:.1e} in {len(hist)} Newton steps\n"
          f"  Case II j=1: dmu={d2[0]:.1e} dkappa={d2[1]:.1e} in {len(hist2)} Newton steps  OK")


def test_3_more_than_one_published_row_reproduces():
    worst = 0.0
    for j, mu_p, kap_p, xi1 in DF_TABLE1:
        (mu, kap), hist = shoot_newton(round(mu_p, 3), round(kap_p, 3), 0.0, 1, 2.3,
                                       min(xi1, 20.0))
        worst = max(worst, abs(mu - mu_p), abs(kap - kap_p))
        assert hist[-1] < 1e-11, (j, hist[-1])
    assert worst < 1e-4, worst
    print(f"  four rows of Table 1 reproduce, worst deviation {worst:.1e}  OK")


def test_4_the_defect_discriminates():
    _, mu_p, kap_p, _ = DF_TABLE1[0]
    r0, _, scale = match_defect(mu_p, kap_p, 0.0, 1, 2.3, 15.0)
    rp, _, _ = match_defect(mu_p, kap_p + 1e-4, 0.0, 1, 2.3, 15.0)
    ratio = abs(rp) / abs(r0)
    assert ratio > 100, f"defect only grew {ratio:.1f}x under a 1e-4 kappa perturbation"
    print(f"  defect at the zero {abs(r0):.2e} (relative {abs(r0)/scale:.1e}), "
          f"at kappa+1e-4 {abs(rp):.2e}: {ratio:.0f}x  OK")


def test_5_resolution_and_truncation_are_measured():
    _, mu_p, kap_p, _ = DF_TABLE2[0]
    lad = resolution_ladder(mu_p, kap_p, 0.0, 3, 1.0, 40.0)
    spread = abs(lad[-1]["defect"] - lad[0]["defect"])
    assert spread < lad[-1]["defect"], (
        f"step halving moved the defect by {spread:.1e}, which is not below the defect "
        f"{lad[-1]['defect']:.1e} -- the integrator, not the matching, is the limit")

    _, mu_p1, kap_p1, _ = DF_TABLE1[0]
    lad2 = xi1_ladder(round(mu_p1, 3), round(kap_p1, 3), 0.0, 1, 2.3, [15.0, 20.0, 30.0])
    kaps = np.array([r["kappa"] for r in lad2])
    mus = np.array([r["mu"] for r in lad2])
    kap_spread = float(kaps.max() - kaps.min())
    mu_spread = float(mus.max() - mus.min())
    assert kap_spread < 1e-6 and mu_spread < 1e-6, (kap_spread, mu_spread)
    print(f"  step halving moves the defect {spread:.1e} (defect {lad[-1]['defect']:.1e}); "
          f"xi_1 = 15/20/30 moves kappa by {kap_spread:.1e}  OK")


def test_6_the_dissipation_branch_folds_at_their_number():
    _, mu_p, kap_p, _ = DF_TABLE1[0]
    br = branch_in_kappa(mu_p, kap_p, 0.45, 1, 2.3, 15.0, dkappa=0.01)
    assert sum(r["converged"] for r in br) > 30, "the branch did not run"
    f = fold_of(br)
    assert f is not None and f["interior"], f
    de = abs(f["eps_star"] - DF_FIG1A_BRANCH1_FOLD["eps_star"])
    dk = abs(f["kappa_star"] - DF_FIG1A_BRANCH1_FOLD["kappa_star"])
    assert de < 1e-5 and dk < 1e-4, (de, dk)
    print(f"  fold at eps*={f['eps_star']:.7f}, kappa*={f['kappa_star']:.6f}; "
          f"published {DF_FIG1A_BRANCH1_FOLD['eps_star']:.7f}, "
          f"{DF_FIG1A_BRANCH1_FOLD['kappa_star']:.6f}  (deps={de:.1e}, dkappa={dk:.1e})  OK")


def test_7_margin_proxy_dies_at_the_fold_not_at_zero():
    _, mu_p, kap_p, _ = DF_TABLE1[0]
    br = branch_in_kappa(mu_p, kap_p, 0.50, 1, 2.3, 15.0, dkappa=0.01)
    f = fold_of(br)
    rec = [r for r in br if r["converged"]]
    at_fold = min(rec, key=lambda r: abs(r["kappa"] - f["kappa_star"]))
    mid = min(rec, key=lambda r: abs(r["kappa"] - 0.70))
    start = rec[0]
    n_fold, c_fold = margin_proxy(at_fold["mu"], at_fold["kappa"], at_fold["eps"], 1, 2.3, 15.0)
    n_mid, c_mid = margin_proxy(mid["mu"], mid["kappa"], mid["eps"], 1, 2.3, 15.0)
    n_0, c_0 = margin_proxy(start["mu"], start["kappa"], start["eps"], 1, 2.3, 15.0)
    assert n_fold > 10 * n_mid, (n_fold, n_mid)
    assert n_mid < n_0, (
        "switching dissipation on must not be what degrades the conditioning -- "
        f"mid-branch {n_mid:.2e} is not below the eps=0 end {n_0:.2e}")
    print(f"  ||J^-1||: eps=0 {n_0:.2e}, mid-branch {n_mid:.2e}, at the fold {n_fold:.2e} "
          f"({n_fold/n_mid:.0f}x); cond(J) {c_0:.1e} / {c_mid:.1e} / {c_fold:.1e}  OK")


def test_8_figure_calibration_checks_itself():
    if not os.path.exists(PDF):
        print(f"  SKIPPED: {PDF} not present (Papers/ is gitignored; "
              f"bash Papers/fetch.sh 2410.05480)")
        return
    out = read_df_figure(PDF, 8, "/Im1")
    assert out is not None, "the figure did not parse"
    curves, cal = out
    assert len(curves) >= 8, f"expected 8 branches in Fig. 1a, parsed {len(curves)}"
    starts = sorted(float(k[0]) for _, k in curves[:8])
    table = sorted(row[2] for row in DF_TABLE1)
    worst = max(min(abs(s - t) for s in starts) for t in table)
    assert worst <= DF_FIG1A_CALIBRATION_RESIDUAL, worst
    print(f"  8 curves parsed; their eps=0 endpoints hit Table 1's kappa to {worst:.1e} "
          f"(x_per_unit {cal['x_per_unit']:.1f}, {cal['n_x_ticks']} ticks)  OK")


if __name__ == "__main__":
    t0 = time.time()
    for fn in (test_1_ledger_is_well_formed_and_the_verdict_reads_it,
               test_2_published_nls_zeros_reproduce,
               test_3_more_than_one_published_row_reproduces,
               test_4_the_defect_discriminates,
               test_5_resolution_and_truncation_are_measured,
               test_6_the_dissipation_branch_folds_at_their_number,
               test_7_margin_proxy_dies_at_the_fold_not_at_zero,
               test_8_figure_calibration_checks_itself):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
