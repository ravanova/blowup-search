"""Route-ICA (leg 98): the fabrication-rejection battery for `interval_certificate.py`.

WHAT THIS ASKS, AND WHY IT IS NOT LEG 61's QUESTION
-----------------------------------------------------------------------------
Leg 61 (Route-KA) checked this pipeline against a PUBLISHED KNOWN ANSWER -- Cadiot-
Lessard-Nave's Kawahara radius -- i.e. *is the answer right when the problem is well
formed*.  That is a completeness check.  This leg asks the SOUNDNESS question, which
no gate in `test_interval_certificate.py` asks: **when the input is not well formed,
does the pipeline still say the certificate closes?**

The question is not speculative.  Leg 79 asked exactly this of the SIBLING pipeline,
`solver/port_certification.radii_polynomial_status`, and found it accepted fabricated
`Y_0`/`Z_1` 11 times out of 25 before its repair.  Leg 69 found real soundness gaps in
the interval PRIMITIVE (`solver/interval.py`) underneath both pipelines.  The one place
nobody has pointed the battery is this pipeline's own verdict path,
`interval_constants` -> `radii_verdict`.

WHAT COUNTS AS A FAILURE, PRE-COMMITTED
-----------------------------------------------------------------------------
A case FAILS -- is a `false_accept` -- when the pipeline returns `closes=True` on an
input that violates a hypothesis it is imported under.  Two hypothesis families, both
established in `writeup/novelty/leg_98.md` as textbook, not as findings of this leg:

  (H1) THE THEOREM'S.  `Y_0`, `Z_1`, `Z_2` are upper bounds on norms, hence FINITE and
       NONNEGATIVE.  A negative or non-finite constant is not a pessimistic input; it
       is an input the radii polynomial theorem says nothing about.
  (H2) THE ARITHMETIC'S.  An enclosure is a valid interval (`lo <= hi`, endpoints not
       NaN) and it CONTAINS the quantity it claims to enclose.  IEEE 1788-2015 carries
       a dedicated `ill` decoration for exactly this, so an enclosure that is ill-formed
       must not be silently consumed.

Three outcomes are recorded per case, and only the first is a failure:

  `false_accept`  closes=True on a hypothesis-violating input      -- UNSOUND
  `rejected`      closes=False, for any reason                     -- sound
  `raised`        an exception propagated                          -- sound but loud;
                  a crash is a refusal, and it is recorded separately because a caller
                  that catches broadly could still turn it into a silent skip.

MAGNITUDES, NOT BOOLEANS (discipline 73)
-----------------------------------------------------------------------------
Every case records the constants the pipeline actually produced and the r-interval it
reported, so the verdict arithmetic can be rechecked from the JSON without rerunning
anything.  For the poisoned-enclosure family the HONEST constants at the same point are
recorded alongside, so the size of the lie is a number: e.g. a fabricated `Y_0` of 0.0
against an honest `Y_0` of 2.7e-01 is a 2.7e-01 absolute swing, not "a failure".

Run: .venv/bin/python experiments/p2_route_ica_v1_adversarial.py
"""

import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.interval import Interval
from solver.interval_certificate import (BorderedCLMIntervals, interval_constants,
                                         radii_verdict)
from solver.weight_search import BorderedCLM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_ica_v1_adversarial.json")

N_GRID = 101
THETA = (0.0, 0.0, 0.0, 0.0, -2.0)      # nu = 1, w_l = 1e-2 X_max, w_om = 1 (the gauge)
POISON_STEP = 1e-3                      # the displacement that makes an iterate dishonest

# THE PRE-FIX MEASUREMENT, VERBATIM.  This battery was written by leg 98 to MEASURE a
# defect and now runs against the repaired module, so the numbers it prints are no longer
# the numbers that motivated the repair.  They are carried here and written into the JSON
# artifact under "history" so that regenerating the artifact cannot erase the finding
# (the convention leg 79's bench repair established for the sibling pipeline).  The cases
# and the judgement predicate are UNCHANGED -- the instrument that measured the defect is
# the instrument that now measures its absence.
PRE_FIX_MEASUREMENT = {
    "commit": "c6aee16 (leg 98, Route-ICA, branch leg/ica-v1)",
    "cases": 39, "hypothesis_violating": 36, "false_accepts": 12,
    "false_accepts_load_bearing": 8, "rejected": 20, "raised": 4,
    "false_accept_cases": ["A1_F_fabricated_zero", "A6_F_shrunk_1e-8_non_containing",
                           "A11_weight_all_negative", "A12_weight_one_negative",
                           "B04_Y0_negative_unit", "B05_Y0_negative_tiny",
                           "B06_Y0_negative_huge", "B07_Z1_negative",
                           "B08_Z1_negative_rescues_big_Y0", "B17_Y0_neg_inf",
                           "B22_Y0_negative_Z1_negative",
                           "B25_Y0_negative_Z1_just_below_one"],
    "load_bearing_cases": ["A1_F_fabricated_zero", "A6_F_shrunk_1e-8_non_containing",
                           "B04_Y0_negative_unit", "B06_Y0_negative_huge",
                           "B07_Z1_negative", "B08_Z1_negative_rescues_big_Y0",
                           "B17_Y0_neg_inf", "B25_Y0_negative_Z1_just_below_one"],
    "raised_cases": ["A2_F_negative_width_excluding", "A3_F_endpoints_swapped",
                     "B20_Z2_zero", "B21_Z2_negative_zero"],
    "note": ("12 of 36 hypothesis-violating inputs were reported as CLOSING certificates, "
             "8 of them load-bearing (the hypothesis-satisfying input of the same "
             "magnitude does NOT close). Two mechanisms: radii_verdict evaluated the "
             "discriminant on theorem-excluded constants, and interval_constants never "
             "checked the enclosure it was handed for containment."),
}


# --------------------------------------------------------------------------
# the substrate: the a=0 CLM bordered system, converged, and a point that is NOT
# --------------------------------------------------------------------------
def substrate(n=N_GRID):
    """(problem, honest z, poisoned z_bad, weight w, nu, enclosure object).

    z is a converged Newton iterate -- the certificate closes there.  z_bad is z
    displaced by POISON_STEP in every component; the certificate must NOT close there,
    and every poisoned-enclosure case below is built to make it close anyway."""
    b = BorderedCLM(n=n)
    z, info = b.newton()
    if not info["converged"]:
        raise RuntimeError("substrate Newton did not converge; the battery needs a "
                           "point where the honest certificate closes")
    w, nu = b.weight_vector(THETA)
    z_bad = z + POISON_STEP
    return b, z, z_bad, w, nu, BorderedCLMIntervals(b)


# --------------------------------------------------------------------------
# poisoned enclosure objects -- each one lies about F or DF in exactly one way
# --------------------------------------------------------------------------
class _Poisoned:
    """Wraps a real enclosure object and corrupts F and/or DF.

    Everything else -- N, n, bilinear_bound -- is forwarded untouched, so each case
    isolates a single lie and the pipeline sees an object that is, by duck typing,
    indistinguishable from the real one."""

    def __init__(self, inner, f_hook=None, j_hook=None):
        self.inner, self.f_hook, self.j_hook = inner, f_hook, j_hook
        self.n, self.N = inner.n, inner.N

    def __getattr__(self, name):
        """Forward everything not corrupted here, so the wrapper stays what its docstring
        says it is: by duck typing indistinguishable from the real object.

        Added by the leg-0 bench repair, and it makes the battery STRICTER, not laxer.
        `interval_constants` now re-evaluates the residual in float to check containment
        (`F_float`); without this forwarding the wrapper would simply lack that method
        and every family-A case would be refused for "this object cannot be checked"
        rather than for the lie it actually tells.  With it, A1 and A6 are caught by the
        containment check itself -- which is the check leg 98 asked for, tested against
        a genuinely non-containing enclosure of the real problem.  The hooks, the case
        list and the judgement predicate are untouched.
        """
        return getattr(self.inner, name)

    def F(self, z):
        out = self.inner.F(z)
        return out if self.f_hook is None else self.f_hook(out, z)

    def jacobian(self, z):
        lo, hi = self.inner.jacobian(z)
        return (lo, hi) if self.j_hook is None else self.j_hook(lo, hi, z)

    def bilinear_bound(self, w, nu):
        return self.inner.bilinear_bound(w, nu)


def _iv_zero(fz, z):
    """A fabricated EXACT ZERO residual: the narrowest possible lie."""
    return Interval(np.zeros_like(fz.lo), np.zeros_like(fz.hi))


def _iv_reversed(fz, z):
    """lo > hi: a negative-width interval (IEEE 1788 `ill`), and one that excludes
    the true residual -- [+1e-16, -1e-16] where |F| is O(POISON_STEP)."""
    e = 1e-16
    return Interval(np.full_like(fz.lo, e), np.full_like(fz.hi, -e))


def _iv_swapped(fz, z):
    """The honest enclosure with its endpoints swapped -- negative width everywhere the
    enclosure was not already a point, but the same magnitudes."""
    return Interval(fz.hi.copy(), fz.lo.copy())


def _iv_nan(fz, z):
    lo, hi = fz.lo.copy(), fz.hi.copy()
    lo[0], hi[0] = np.nan, np.nan
    return Interval(lo, hi)


def _iv_inf(fz, z):
    lo, hi = fz.lo.copy(), fz.hi.copy()
    lo[0], hi[0] = -np.inf, np.inf
    return Interval(lo, hi)


def _iv_shrunk(fz, z):
    """Non-containing WITHOUT being ill-formed: a perfectly valid interval, 1e-8 times
    the honest one, which simply does not contain the residual it claims to enclose.
    This is the case an `lo <= hi` check would not catch."""
    return Interval(fz.lo * 1e-8, fz.hi * 1e-8)


def _j_swapped(lo, hi, z):
    return hi.copy(), lo.copy()


def _j_nan(lo, hi, z):
    lo, hi = lo.copy(), hi.copy()
    lo[0, 0], hi[0, 0] = np.nan, np.nan
    return lo, hi


def _j_zero_offdiag(lo, hi, z):
    """A fabricated Jacobian enclosure claiming the operator is the identity: makes
    `Z_1 = ||I - A DF||` collapse for a DF that is nothing like the true one."""
    n = lo.shape[0]
    return np.eye(n), np.eye(n)


# --------------------------------------------------------------------------
# family A -- poisoned enclosures fed to interval_constants
# --------------------------------------------------------------------------
def family_A(b, z, z_bad, w, nu, iv):
    """Each case: which hypothesis is violated, at which point, and what came out."""
    honest_good = interval_constants(iv, z, w, nu)
    honest_bad = interval_constants(iv, z_bad, w, nu)
    A_bad = np.linalg.inv(0.5 * np.add(*iv.jacobian(z_bad)))

    cases = [
        ("A1_F_fabricated_zero", z_bad, dict(f_hook=_iv_zero), None,
         "H2 containment: F enclosed as exactly [0,0] at an iterate whose true "
         "residual is far from zero"),
        ("A2_F_negative_width_excluding", z_bad, dict(f_hook=_iv_reversed), None,
         "H2 validity AND containment: lo=+1e-16 > hi=-1e-16, and the true residual "
         "is outside"),
        ("A3_F_endpoints_swapped", z_bad, dict(f_hook=_iv_swapped), None,
         "H2 validity: the honest enclosure with lo and hi exchanged (negative width, "
         "same magnitudes)"),
        ("A4_F_nan_endpoint", z, dict(f_hook=_iv_nan), None,
         "H2 validity: a NaN endpoint in component 0 of the residual enclosure"),
        ("A5_F_infinite_endpoint", z, dict(f_hook=_iv_inf), None,
         "H2 validity: an unbounded endpoint in component 0 of the residual enclosure"),
        ("A6_F_shrunk_1e-8_non_containing", z_bad, dict(f_hook=_iv_shrunk), None,
         "H2 containment ONLY -- a well-formed interval (lo<=hi, finite) that simply "
         "does not contain the residual"),
        ("A7_J_endpoints_swapped", z_bad, dict(j_hook=_j_swapped), A_bad,
         "H2 validity: the Jacobian enclosure with lo and hi exchanged"),
        ("A8_J_nan_entry", z, dict(j_hook=_j_nan), None,
         "H2 validity: a NaN entry in the Jacobian enclosure"),
        ("A9_J_fabricated_identity", z_bad, dict(j_hook=_j_zero_offdiag), A_bad,
         "H2 containment: DF enclosed as the identity, which contains none of the "
         "true Jacobian's off-diagonal mass"),
        ("A10_F_and_J_both_fabricated", z_bad,
         dict(f_hook=_iv_zero, j_hook=_j_zero_offdiag), A_bad,
         "H2 both: a fully fabricated certificate -- zero residual, identity Jacobian"),
    ]

    out = []
    for name, point, hooks, A, why in cases:
        rec = {"case": name, "family": "A_poisoned_enclosure", "violates": why,
               "point": "z_bad" if point is z_bad else "z"}
        honest = honest_bad if point is z_bad else honest_good
        rec["weight"] = "honest"
        rec["honest"] = {k: honest[k] for k in ("Y0", "Z1", "Z2")}
        rec["honest_verdict_closes"] = radii_verdict(
            honest["Y0"], honest["Z1"], honest["Z2"])["closes"]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                c = interval_constants(_Poisoned(iv, **hooks), point, w, nu, A=A)
                v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
            rec["constants"] = {k: _num(c[k]) for k in ("Y0", "Z1", "Z2")}
            rec["verdict"] = {k: _num(v[k]) for k in
                              ("closes", "reason", "r_min", "r_max", "budget")}
            rec["outcome"] = "false_accept" if v["closes"] else "rejected"
            rec["poison_is_load_bearing"] = bool(
                v["closes"] and not rec["honest_verdict_closes"])
        except Exception as ex:                      # noqa: BLE001 -- the point is to see it
            rec["constants"] = None
            rec["verdict"] = None
            rec["outcome"] = "raised"
            rec["exception"] = f"{type(ex).__name__}: {str(ex)[:160]}"
        out.append(rec)

    # -- supplementary: the WEIGHT is the other piece of caller data ------------
    # `interval_constants` takes the norm's weight vector on trust too.  w defines the
    # norm, so it must be strictly positive and finite; anything else is not a norm.
    # These are recorded in the same family and counted the same way, and they are the
    # only end-to-end path in this battery from valid enclosures to a NEGATIVE Y_0.
    for name, wp, why in [
        ("A11_weight_all_negative", -np.asarray(w),
         "H3 norm data: w < 0 everywhere -- not a norm"),
        ("A12_weight_one_negative", np.concatenate([[-w[0]], w[1:]]),
         "H3 norm data: a single negative weight component"),
        ("A13_weight_has_zero", np.concatenate([[0.0], w[1:]]),
         "H3 norm data: a zero weight component -- 1/w_j is not finite"),
        ("A14_weight_has_nan", np.concatenate([[np.nan], w[1:]]),
         "H3 norm data: a NaN weight component"),
    ]:
        rec = {"case": name, "family": "A_poisoned_enclosure", "violates": why,
               "point": "z", "weight": "poisoned",
               "honest": {k: _num(honest_good[k]) for k in ("Y0", "Z1", "Z2")},
               "honest_verdict_closes": True}
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                c = interval_constants(iv, z, wp, nu)
                v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
            rec["constants"] = {k: _num(c[k]) for k in ("Y0", "Z1", "Z2")}
            rec["verdict"] = {k: _num(v[k]) for k in
                              ("closes", "reason", "r_min", "r_max", "budget")}
            rec["outcome"] = "false_accept" if v["closes"] else "rejected"
            rec["poison_is_load_bearing"] = False    # honest w closes at z anyway
        except Exception as ex:                      # noqa: BLE001
            rec["constants"] = None
            rec["verdict"] = None
            rec["outcome"] = "raised"
            rec["exception"] = f"{type(ex).__name__}: {str(ex)[:160]}"
        out.append(rec)

    return out, honest_good, honest_bad


# --------------------------------------------------------------------------
# family B -- fabricated constants fed straight to radii_verdict
# --------------------------------------------------------------------------
def family_B():
    """Leg 79's battery, re-aimed at THIS pipeline's verdict function.

    `interval_constants` is not the only caller of `radii_verdict`; the function is
    public, and every certificate in the repository is read off its `closes` field.
    So it is audited as its own trust boundary, exactly as the sibling was."""
    cases = [
        ("B01_baseline_valid", 1e-12, 0.3, 1.0, None),
        ("B02_baseline_valid_tight", 1e-3, 0.9, 1.0, None),
        ("B03_honest_non_closing", 1.0, 0.3, 1.0, None),
        ("B04_Y0_negative_unit", -1.0, 0.3, 1.0, "H1: Y_0 < 0"),
        ("B05_Y0_negative_tiny", -1e-12, 0.3, 1.0, "H1: Y_0 < 0"),
        ("B06_Y0_negative_huge", -1e6, 0.3, 1.0, "H1: Y_0 < 0"),
        ("B07_Z1_negative", 1e-12, -5.0, 1.0, "H1: Z_1 < 0"),
        ("B08_Z1_negative_rescues_big_Y0", 1e3, -1e6, 1.0, "H1: Z_1 < 0"),
        ("B09_Z2_negative", 1e-12, 0.3, -1.0, "H1: Z_2 < 0"),
        ("B10_Z2_negative_big_Y0", 1e6, 0.3, -1.0, "H1: Z_2 < 0"),
        ("B11_all_three_negative", -1.0, -1.0, -1.0, "H1: all three < 0"),
        ("B12_Y0_nan", np.nan, 0.3, 1.0, "H1: Y_0 not finite"),
        ("B13_Z1_nan", 1e-12, np.nan, 1.0, "H1: Z_1 not finite"),
        ("B14_Z2_nan", 1e-12, 0.3, np.nan, "H1: Z_2 not finite"),
        ("B15_all_nan", np.nan, np.nan, np.nan, "H1: none finite"),
        ("B16_Y0_inf", np.inf, 0.3, 1.0, "H1: Y_0 not finite"),
        ("B17_Y0_neg_inf", -np.inf, 0.3, 1.0, "H1: Y_0 not finite"),
        ("B18_Z1_neg_inf", 1e-12, -np.inf, 1.0, "H1: Z_1 not finite"),
        ("B19_Z2_inf", 1e-12, 0.3, np.inf, "H1: Z_2 not finite"),
        ("B20_Z2_zero", 1e-12, 0.3, 0.0, "H1 edge: Z_2 = 0, the quadratic degenerates"),
        ("B21_Z2_negative_zero", 1e-12, 0.3, -0.0, "H1 edge: Z_2 = -0.0"),
        ("B22_Y0_negative_Z1_negative", -1e-3, -1e-3, 1.0, "H1: Y_0 < 0 and Z_1 < 0"),
        ("B23_Z1_exactly_one", 1e-12, 1.0, 1.0, "boundary: Z_1 = 1, no contraction"),
        ("B24_Z1_just_below_one", 1e-30, 1.0 - 1e-16, 1.0, "boundary: Z_1 = 1 - 1e-16"),
        ("B25_Y0_negative_Z1_just_below_one", -1e-30, 1.0 - 1e-16, 1.0, "H1: Y_0 < 0"),
    ]
    out = []
    for name, Y0, Z1, Z2, why in cases:
        rec = {"case": name, "family": "B_fabricated_constants",
               "Y0": _num(Y0), "Z1": _num(Z1), "Z2": _num(Z2),
               "violates": why, "valid_input": why is None}
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                v = radii_verdict(Y0, Z1, Z2)
            rec["verdict"] = {k: _num(v[k]) for k in
                              ("closes", "reason", "r_min", "r_max", "budget")}
            if why is None:
                rec["outcome"] = "valid_closes" if v["closes"] else "valid_rejects"
            else:
                rec["outcome"] = "false_accept" if v["closes"] else "rejected"
            # SEVERITY, as a number rather than a label.  Replace each poisoned
            # constant by the nearest hypothesis-SATISFYING one of the same magnitude
            # (|x| for a negative, and drop the case if any is non-finite) and ask
            # whether THAT closes.  If it does not, the hypothesis violation is what
            # bought the certificate; if it does, the poison was inert here.
            trip = (Y0, Z1, Z2)
            if all(np.isfinite(t) for t in trip):
                a = radii_verdict(*(abs(t) for t in trip))
                rec["magnitude_counterpart_closes"] = bool(a["closes"])
                rec["poison_is_load_bearing"] = bool(v["closes"] and not a["closes"])
            else:
                rec["magnitude_counterpart_closes"] = None
                rec["poison_is_load_bearing"] = bool(v["closes"])
        except Exception as ex:                      # noqa: BLE001
            rec["verdict"] = None
            rec["outcome"] = "raised"
            rec["exception"] = f"{type(ex).__name__}: {str(ex)[:160]}"
        out.append(rec)
    return out


def _num(x):
    """JSON-safe: NaN and +-inf become strings so the file round-trips as strict JSON."""
    if isinstance(x, (bool, str)) or x is None:
        return x
    x = float(x)
    if np.isnan(x):
        return "nan"
    if np.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


# --------------------------------------------------------------------------
def run(n=N_GRID, write=True, verbose=True):
    b, z, z_bad, w, nu, iv = substrate(n)
    A_cases, honest_good, honest_bad = family_A(b, z, z_bad, w, nu, iv)
    B_cases = family_B()
    cases = A_cases + B_cases

    poisoned = [c for c in cases if c.get("violates") is not None]
    false_accepts = [c for c in poisoned if c["outcome"] == "false_accept"]
    load_bearing = [c for c in false_accepts if c.get("poison_is_load_bearing")]
    raised = [c for c in poisoned if c["outcome"] == "raised"]

    data = {
        "leg": 98, "route": "ICA",
        "question": ("Under an adversarial battery of poisoned interval enclosures "
                     "(negative widths, NaN endpoints, non-containing enclosures) fed "
                     "to interval_constants / radii_verdict, does the pipeline ever "
                     "incorrectly report a closing/valid certificate?"),
        "substrate": {"object": "BorderedCLM (a=0 CLM, bordered)", "n": int(b.n),
                      "N": int(b.N), "theta": list(THETA),
                      "poison_step": POISON_STEP,
                      "honest_at_z": {k: _num(honest_good[k]) for k in ("Y0", "Z1", "Z2")},
                      "honest_at_z_closes": radii_verdict(
                          honest_good["Y0"], honest_good["Z1"],
                          honest_good["Z2"])["closes"],
                      "honest_at_z_bad": {k: _num(honest_bad[k]) for k in ("Y0", "Z1", "Z2")},
                      "honest_at_z_bad_closes": radii_verdict(
                          honest_bad["Y0"], honest_bad["Z1"],
                          honest_bad["Z2"])["closes"]},
        "totals": {"cases": len(cases),
                   "hypothesis_violating": len(poisoned),
                   "false_accepts": len(false_accepts),
                   "false_accepts_load_bearing": len(load_bearing),
                   "rejected": len([c for c in poisoned if c["outcome"] == "rejected"]),
                   "raised": len(raised)},
        "history": {"pre_fix": dict(PRE_FIX_MEASUREMENT)},
        "false_accept_cases": [c["case"] for c in false_accepts],
        "load_bearing_cases": [c["case"] for c in load_bearing],
        "raised_cases": [c["case"] for c in raised],
        "cases": cases,
    }

    if not verbose:
        if write:
            with open(os.path.abspath(OUT), "w") as fh:
                json.dump(data, fh, indent=2)
        return data

    print(f"substrate: BorderedCLM n={b.n} N={b.N}; honest Y0={honest_good['Y0']:.3e} "
          f"Z1={honest_good['Z1']:.3e} Z2={honest_good['Z2']:.3e} -> "
          f"closes={data['substrate']['honest_at_z_closes']}")
    print(f"           at z_bad (+{POISON_STEP}): Y0={honest_bad['Y0']:.3e} -> "
          f"closes={data['substrate']['honest_at_z_bad_closes']}")
    print()
    for c in cases:
        v = c.get("verdict") or {}
        lb = " <-- poison is load-bearing" if c.get("poison_is_load_bearing") else ""
        print(f"  {c['case']:34s} {c['outcome']:14s} closes={str(v.get('closes')):5s} "
              f"{c.get('exception', '')}{lb}")
    print()
    t = data["totals"]
    print(f"FALSE ACCEPTS: {t['false_accepts']}/{t['hypothesis_violating']} "
          f"hypothesis-violating inputs reported a CLOSING certificate "
          f"({t['rejected']} rejected, {t['raised']} raised)")
    print(f"  of which {t['false_accepts_load_bearing']} are LOAD-BEARING -- the "
          f"hypothesis-satisfying counterpart does NOT close, so the violation is "
          f"what bought the certificate")
    if load_bearing:
        print("  " + ", ".join(c["case"] for c in load_bearing))

    if write:
        with open(os.path.abspath(OUT), "w") as fh:
            json.dump(data, fh, indent=2)
        print(f"\nwrote {os.path.abspath(OUT)}")
    return data


if __name__ == "__main__":
    run()
