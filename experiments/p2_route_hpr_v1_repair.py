"""Route-HPR, leg 130 -- the REPAIR runner for solver/hilbert_pointwise.py.

Leg 106 (Route-HPA) measured two configurations on which `pointwise_bound`'s pair is
EXCEEDED by the true |H(h)|, and escalated: its gate's yes-branch reports, it does not
patch.  Leg 130 lands the guard.  This runner is the evidence, and it answers the gate's
two clauses separately and with magnitudes:

  (a) do leg 106's two failing configurations now either RAISE or return a value
      verified to dominate the true |H(h)| on that configuration?
  (b) is the module BIT-IDENTICAL on every previously-passing case?

Clause (b) is the one that can only be answered by a differential, so it is run as one:
the PRE-REPAIR module is read out of git at this leg's merge base, imported into the same
process under a private name, and called side by side with the repaired module on every
shipped configuration.  Comparison is `==` on the raw float64 pair -- not `allclose`.

Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_hpr_v1_repair.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import hilbert_pointwise as HP                              # noqa: E402
from solver.hilbert_pointwise import (                                  # noqa: E402
    HEAD_WARN_TOL, HilbertPointwiseDomainError, HilbertPointwiseTruncationWarning,
    HilbertPointwiseUnsoundWarning, pointwise_bound, pointwise_curves, theta_grid,
    weighted_sups,
)
from experiments.p2_route_hpa_v1_adversarial import (                   # noqa: E402
    ALPHA, GAMMA, SHIPPED_RHOS, psi_of_step, step_norms,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_hpr_v1_repair.json")
THETA = 1.0                      # the reference angle leg 106 states every violation at
PRE_REPAIR_REF = "e95d0d2"       # last commit before the guard (the novelty correction)


# ---------------------------------------------------------------------------
# the pre-repair module, loaded from git into this same process
# ---------------------------------------------------------------------------


def load_pre_repair():
    """Import the module as it stood before the guard, under a private name."""
    src = subprocess.run(["git", "show", "%s:solver/hilbert_pointwise.py" % PRE_REPAIR_REF],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    fd, path = tempfile.mkstemp(suffix="_pre_hilbert_pointwise.py")
    with os.fdopen(fd, "w") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("_pre_hilbert_pointwise", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, len(src.splitlines())


# ---------------------------------------------------------------------------
# (b) zero movement: the bitwise differential
# ---------------------------------------------------------------------------


def bitwise_differential(pre):
    """Every shipped configuration, pre vs post, compared with `==`."""
    n = n_ident = 0
    worst = None
    for n_theta in (140, 560):
        for th in theta_grid(n_theta):
            for rho in SHIPPED_RHOS:
                for eps in (1e-10, 1e-14):
                    for n_quad in (400, 4000):
                        a = pre.pointwise_bound(th, ALPHA, GAMMA, rho=rho,
                                                n_quad=n_quad, eps=eps)
                        b = pointwise_bound(th, ALPHA, GAMMA, rho=rho,
                                            n_quad=n_quad, eps=eps)
                        n += 1
                        if a == b:
                            n_ident += 1
                        elif worst is None:
                            worst = {"theta": float(th), "rho": float(rho),
                                     "eps": eps, "n_quad": n_quad,
                                     "pre": list(a), "post": list(b)}
    return {"n_configurations": n, "n_bit_identical": n_ident,
            "n_moved": n - n_ident, "first_disagreement": worst}


def curve_differential(pre):
    """The consumed surface: whole curves and the four weighted sups."""
    rows = []
    for rho in SHIPPED_RHOS:
        for n_theta in (140, 560):
            cv_a = pre.pointwise_curves(ALPHA, GAMMA, rho=rho, n_theta=n_theta)
            cv_b = pointwise_curves(ALPHA, GAMMA, rho=rho, n_theta=n_theta)
            same = all(np.array_equal(x, y) for x, y in zip(cv_a, cv_b))
            wa, wb = weighted_sups(cv_a, ALPHA), weighted_sups(cv_b, ALPHA)
            rows.append({"rho": float(rho), "n_theta": n_theta,
                         "curves_bit_identical": bool(same),
                         "n_nodes": int(cv_a[0].size),
                         "weighted_sups_bit_identical": wa == wb,
                         "weighted_sups": wb})
    return rows


# ---------------------------------------------------------------------------
# (a) the two failing configurations
# ---------------------------------------------------------------------------


V1 = [("rho=nan", dict(rho=np.nan)), ("rho=+inf", dict(rho=np.inf)),
      ("rho=-inf", dict(rho=-np.inf)), ("rho=1e300", dict(rho=1e300))]
V2 = [("gamma=0", dict(gamma=0.0)), ("gamma=-0.5", dict(gamma=-0.5)),
      ("gamma=-1e-12", dict(gamma=-1e-12)), ("gamma=nan", dict(gamma=np.nan)),
      ("gamma=inf", dict(gamma=np.inf))]


def _call(pre, label_kwargs, on_unsound, module):
    rho = label_kwargs.get("rho", 1.0)
    gamma = label_kwargs.get("gamma", GAMMA)
    fn = module.pointwise_bound
    kw = {} if module is pre else {"on_unsound": on_unsound}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return fn(THETA, ALPHA, gamma, rho=rho, **kw)


def failing_configurations(pre):
    """For each: pre-repair value, post-repair disposition, and the domination check."""
    out = []
    for family, cases in (("V1_rho", V1), ("V2_gamma", V2)):
        for label, kwargs in cases:
            pre_pair = _call(pre, kwargs, None, pre)
            row = {"family": family, "case": label,
                   "pre_repair_pair": [float(x) for x in pre_pair],
                   "pre_repair_is_finite": bool(np.all(np.isfinite(pre_pair)))}

            # default policy: does it reject, loudly?
            try:
                _call(pre, kwargs, "raise", HP)
                row["default_policy"] = "RETURNED"
                row["raises"] = False
            except HilbertPointwiseDomainError as exc:
                row["default_policy"] = "HilbertPointwiseDomainError"
                row["raises"] = True
                row["message_head"] = str(exc)[:110]

            # the other branch of the gate: a value that TRULY dominates
            inflated = _call(pre, kwargs, "inflate", HP)
            row["inflate_pair"] = [float(x) for x in inflated]

            # The domination check itself, against leg 106's step adversary.  The
            # adversary's norms must be read at the SAME gamma the pair was computed
            # at -- substituting the shipped gamma into the norms of a gamma = 0 bound
            # silently understates the ratio by ~5 orders of magnitude.  When gamma is
            # non-finite the pair (S, T) has no referent at all, so the ratio is
            # recorded as null rather than bounded (lesson 73).
            gamma = kwargs.get("gamma", GAMMA)
            row["norms_read_at_gamma"] = float(gamma) if np.isfinite(gamma) else None
            if not np.isfinite(gamma):
                row["step_ratio_pre_repair"] = None
                row["step_ratio_after_inflate"] = None
                row["pre_repair_max_ratio"] = None
                row["inflate_max_ratio"] = None
            else:
                ratios_pre, ratios_post = {}, {}
                for delta in (1e-10, 1e-20, 1e-50):
                    S, T = step_norms(THETA, delta, gamma=gamma)
                    psi = abs(psi_of_step(THETA, delta))
                    dpre = pre_pair[0] * S + pre_pair[1] * T
                    dpost = inflated[0] * S + inflated[1] * T
                    ratios_pre["delta=%g" % delta] = (
                        float(psi / dpre) if dpre > 0 else np.inf)
                    ratios_post["delta=%g" % delta] = (
                        float(psi / dpost) if np.isfinite(dpost) and dpost > 0 else 0.0)
                row["step_ratio_pre_repair"] = ratios_pre
                row["step_ratio_after_inflate"] = ratios_post
                row["pre_repair_max_ratio"] = max(ratios_pre.values())
                row["inflate_max_ratio"] = max(ratios_post.values())
            # `inflate` dominates trivially here: the head is unbounded on every one of
            # these configurations, so the honest dominating value is +inf.  Recorded as
            # such rather than dressed up as a bound anyone would want.
            row["inflate_is_infinite"] = bool(not np.all(np.isfinite(inflated)))
            row["inflate_dominates"] = bool(
                row["inflate_is_infinite"] or row["inflate_max_ratio"] <= 1.0)

            # extrapolate keeps leg 106's measurement runnable, and says so
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                ex = _call(pre, kwargs, "extrapolate", HP)
            row["extrapolate_matches_pre_repair"] = bool(tuple(ex) == tuple(pre_pair))
            row["extrapolate_warns"] = bool(
                any(issubclass(w.category, HilbertPointwiseUnsoundWarning)
                    for w in caught))
            out.append(row)
    return out


def other_silent_inputs(pre):
    """Leg 106 gate 9's inventory: what the module SAYS now on each wrong argument."""
    cases = [("theta<0", -0.5, ALPHA, GAMMA, 1.0), ("theta=0", 0.0, ALPHA, GAMMA, 1.0),
             ("theta=pi", np.pi, ALPHA, GAMMA, 1.0),
             ("theta=nan", np.nan, ALPHA, GAMMA, 1.0),
             ("alpha=nan", THETA, np.nan, GAMMA, 1.0),
             ("rho=0", THETA, ALPHA, GAMMA, 0.0), ("rho=-1", THETA, ALPHA, GAMMA, -1.0)]
    rows = []
    for label, th, al, ga, rh in cases:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            pre_v = pre.pointwise_bound(th, al, ga, rho=rh, n_quad=200)
        pre_silent_finite = (not caught) and bool(np.all(np.isfinite(pre_v)))
        try:
            pointwise_bound(th, al, ga, rho=rh, n_quad=200)
            post = "RETURNED"
        except HilbertPointwiseDomainError:
            post = "HilbertPointwiseDomainError"
        rows.append({"case": label, "pre_repair_silent_and_finite": pre_silent_finite,
                     "pre_repair_pair": [float(x) for x in pre_v], "post_repair": post})
    return rows


# ---------------------------------------------------------------------------
# the residual band the repair did NOT reject, reported with its magnitude
# ---------------------------------------------------------------------------


def residual_band():
    """rho ~ 1e6..1e12: finite exact majorant, badly under-resolved at the default eps."""
    rows = []
    for rho in (25.0, 1e3, 1e5, 1e6, 1e9, 1e12, 1e100, 1e300):
        hS, hT, vanishes = HP._head_bound(THETA, ALPHA, GAMMA, rho, 1e-10)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                pair = pointwise_bound(THETA, ALPHA, GAMMA, rho=rho)
                disposition = "accepted"
            except HilbertPointwiseDomainError:
                pair, disposition = None, "rejected"
        total = (pair[0] + pair[1]) if pair else float("nan")
        rows.append({
            "rho": float(rho), "disposition": disposition,
            "head_sup": float(hS), "head_vanishes_as_eps_to_zero": bool(vanishes),
            "returned_total": float(total) if pair else None,
            "head_share_of_returned": float(hS / total) if pair and total > 0 else None,
            "warns": bool(any(issubclass(w.category, HilbertPointwiseTruncationWarning)
                              for w in caught))})
    return rows


def head_census():
    """The predicate's separation, over the whole shipped family."""
    n = n_head_positive = n_rejected = 0
    worst_share = 0.0
    worst_at = None
    for n_theta in (140, 560):
        for th in theta_grid(n_theta):
            for rho in SHIPPED_RHOS:
                for eps in (1e-10, 1e-14):
                    hS, hT, vanishes = HP._head_bound(th, ALPHA, GAMMA, rho, eps)
                    n += 1
                    if not vanishes:
                        n_rejected += 1
                    if hS > 0.0:
                        n_head_positive += 1
                        pair = pointwise_bound(th, ALPHA, GAMMA, rho=rho, eps=eps)
                        share = hS / (pair[0] + pair[1])
                        if share > worst_share:
                            worst_share, worst_at = share, {
                                "theta": float(th), "pi_minus_theta": float(np.pi - th),
                                "rho": float(rho), "eps": eps, "head_sup": float(hS)}
    return {"n_configurations": n, "n_with_positive_sup_head": n_head_positive,
            "n_rejected_by_the_guard": n_rejected,
            "worst_head_share_among_accepted": worst_share,
            "worst_at": worst_at, "warn_tolerance": HEAD_WARN_TOL,
            "margin_to_warn_tolerance": HEAD_WARN_TOL / worst_share if worst_share else None}


# ---------------------------------------------------------------------------


def main():
    pre, pre_lines = load_pre_repair()
    bits = bitwise_differential(pre)
    curves = curve_differential(pre)
    fails = failing_configurations(pre)
    silent = other_silent_inputs(pre)
    band = residual_band()
    census = head_census()

    v1 = [r for r in fails if r["family"] == "V1_rho"]
    v2 = [r for r in fails if r["family"] == "V2_gamma"]
    gate_a = all(r["raises"] and r["inflate_dominates"] for r in fails)
    gate_b = (bits["n_moved"] == 0
              and all(r["curves_bit_identical"] and r["weighted_sups_bit_identical"]
                      for r in curves)
              and census["n_rejected_by_the_guard"] == 0)

    doc = {
        "leg": 130, "route": "ROUTE-HPR", "module": "solver/hilbert_pointwise.py",
        "repairs": "leg 106 (Route-HPA), writeup/data/p2_route_hpa_v1_adversarial.json",
        "pre_repair_ref": PRE_REPAIR_REF, "pre_repair_module_lines": pre_lines,
        "alpha": ALPHA, "gamma": GAMMA, "shipped_rhos": list(SHIPPED_RHOS),
        "B_zero_movement_bitwise": bits,
        "B_zero_movement_curves": curves,
        "A_failing_configurations": fails,
        "A_v1_all_raise": all(r["raises"] for r in v1),
        "A_v2_all_raise": all(r["raises"] for r in v2),
        "A_all_inflate_dominate": all(r["inflate_dominates"] for r in fails),
        "A_worst_pre_repair_step_ratio": max(r["pre_repair_max_ratio"] for r in fails
                                             if r["pre_repair_max_ratio"] is not None),
        "A_worst_post_inflate_step_ratio": max(r["inflate_max_ratio"] for r in fails
                                               if r["inflate_max_ratio"] is not None),
        "A_all_inflate_are_infinite": all(r["inflate_is_infinite"] for r in fails),
        "C_other_inputs": silent,
        "D_residual_band_not_rejected": band,
        "E_predicate_census": census,
        "gate_a_answer": "YES" if gate_a else "NO",
        "gate_b_answer": "YES" if gate_b else "NO",
        "gate_answer": "YES" if (gate_a and gate_b) else "NO",
    }
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=2, sort_keys=False)

    print("PRE-REPAIR MODULE  %s  (%d lines)" % (PRE_REPAIR_REF, pre_lines))
    print("(b) ZERO MOVEMENT  %d/%d shipped configurations bit-identical, %d moved"
          % (bits["n_bit_identical"], bits["n_configurations"], bits["n_moved"]))
    print("    curves         %d/%d curve+weighted_sups pairs bit-identical"
          % (sum(1 for r in curves if r["curves_bit_identical"]
                 and r["weighted_sups_bit_identical"]), len(curves)))
    print("    guard fires on %d of %d shipped configurations"
          % (census["n_rejected_by_the_guard"], census["n_configurations"]))
    print("(a) V1 rho:        %d/%d raise" % (sum(r["raises"] for r in v1), len(v1)))
    print("    V2 gamma:      %d/%d raise" % (sum(r["raises"] for r in v2), len(v2)))
    print("    worst step-adversary |H(h)|/bound  %.4f pre-repair -> %.4f after inflate"
          % (doc["A_worst_pre_repair_step_ratio"], doc["A_worst_post_inflate_step_ratio"]))
    print("(d) residual band  %s"
          % ", ".join("rho=%g:%s%s" % (r["rho"], r["disposition"],
                                       "+warn" if r["warns"] else "")
                      for r in band))
    print("GATE (a) %s   GATE (b) %s   ->  %s" % (doc["gate_a_answer"],
                                                  doc["gate_b_answer"],
                                                  doc["gate_answer"]))
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
