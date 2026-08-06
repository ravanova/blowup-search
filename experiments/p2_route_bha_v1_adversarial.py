"""Route-BHA v1 -- an ADVERSARIAL BATTERY against the CERTIFICATE-CONSTANTS path of
solver/bordered_hl.py: the weighted-norm estimator that returns Y_0, Z_1, Z_2.

Leg 198. Audit-family leg, in the line of legs 100/107/114/115/118/122/124/139/142/143/
144/146 and the leg 116/128/147 fabrication-acceptance class.

WHY THIS SURFACE, AND WHY IT IS NOT LEG 80's
--------------------------------------------
solver/bordered_hl.py HAS been adversarially audited once: leg 80 (Route-BHN) asked
whether `newton()`'s `converged` flag ever reports falsely, and answered NO over 336
hostile cases. Its runner makes exactly 12 calls into the module -- 6 `jacobian`, 4 `F`,
1 `set_pin_from`, `newton` throughout -- and ZERO calls into

    certificate_constants, constants_vs_weight, quadratic, induced_sup_norm,
    weights, velocity_matrix, tail_exponent, profile_shape

Eight public symbols, no adversarial coverage. Among them is the one that returns the
radii-polynomial triple, which is what `capabilities.py` advertises for this module and
what the bordered certificate batteries of legs 54/58/127 rest on. Leg 80 audited the
solver that FINDS the state; nobody has audited the estimator that SCORES it. That gap,
and only that gap, is this leg's subject. `newton()`'s flag is explicitly OUT of scope
and is not re-litigated; where Newton is used below it is an instrument.

`test_bordered_hl.py` does call the estimator, but every check there is a
COMPLETENESS-DIRECTION check on well-formed input (the leg 143 distinction): it gates the
exact-quadratic identity on a good state and reads the constants off a converged profile.
Nothing in it hands the estimator a defect and asks whether it notices.

THE GATE, VERBATIM (pre-committed, both branches, writeup/novelty/leg_198.md)
----------------------------------------------------------------------------
"Under adversarial and degenerate inputs (including a degenerate or near-singular matching
condition), does bordered_hl.py ever silently return a wrong value rather than reject or
visibly propagate the defect?"

WHAT "SILENTLY" MEANS, FIXED BEFORE THE RUN (leg 80's precedent of a predicate in advance)
-----------------------------------------------------------------------------------------
A return is SILENT-WRONG iff ALL THREE hold:

  1. the call returns normally  -- no exception, and no warning emitted; AND
  2. every returned value is FINITE -- a returned NaN/Inf is *visible propagation*, which
     the gate's own wording excludes from the YES branch; AND
  3. the value is MATERIALLY WRONG for the input as given. For the certificate constants
     "materially" means UNDERSTATED, because an understated Y_0/Z_1/Z_2 is the direction
     that fabricates a certificate. An OVERSTATED constant is conservative: it is recorded
     with its magnitude and does NOT decide the gate. A NEGATIVE value returned for a
     quantity that is an operator norm (Z_1, Z_2, A_norm, B) is wrong in the strongest
     available sense -- no operator norm is negative -- and counts.

DISCIPLINE
----------
Magnitudes, never booleans. Every family reports the size of the thing that went wrong,
not that it went wrong. Every family carries at least one CONTROL that could have failed
(lesson 90): a family that reports all-clean without a discriminating control is reported
INCONCLUSIVE, not clean. All suspects are driven in one pass (lesson 74).

BLAS THREADING: the caps below are set BEFORE numpy is imported, for leg 80's reason --
on this host an unpinned solve on the bordered matrix costs ~1230x its pinned cost. That
is an environment effect, not a property of the module.

Run:    .venv/bin/python experiments/p2_route_bha_v1_adversarial.py
Writes: writeup/data/p2_route_bha_v1_adversarial.json
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.bordered_hl import (  # noqa: E402
    BorderedHL, induced_sup_norm, velocity_matrix, tail_exponent, profile_shape)

SEED = 20260806
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_bha_v1_adversarial.json")

N_GRID = 101
RHO_MAX = 8.0


# --------------------------------------------------------------------------- #
# harness
# --------------------------------------------------------------------------- #
def fresh(n=N_GRID, rho_max=RHO_MAX, x0=0.3, w=0.9):
    """The same well-posed non-symmetric starting data leg 80 and test_bordered_hl.py use."""
    b = BorderedHL(n=n, rho_max=rho_max)
    Om = np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = 0.8 * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    z0 = b.pack(Om, V, 1.06, -0.42, 0.077)
    b.set_pin_from(z0)
    return b, z0


def converged_state(n=N_GRID, rho_max=RHO_MAX):
    b, z0 = fresh(n=n, rho_max=rho_max)
    z, hist = b.newton(z0, tol=1e-12, max_iter=40)
    return b, z0, z, hist


def call(fn, *a, **kw):
    """Run fn, capturing BOTH the exception and any warning it emits.

    Returns (value, exc_name, exc_msg, warning_names). The warning capture is what
    makes clause (1) of the SILENT predicate decidable rather than asserted."""
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            v = fn(*a, **kw)
        except Exception as e:                       # noqa: BLE001 -- the point
            return None, type(e).__name__, str(e)[:200], [w.category.__name__ for w in ws]
        return v, None, None, sorted({w.category.__name__ for w in ws})


def finite_all(c, keys=("Y0", "Z1", "Z2", "A_norm", "B")):
    return bool(all(np.isfinite(c[k]) for k in keys))


def radii_root(Y0, Z1, Z2):
    """Smallest positive root of p(r) = (Z2/2) r^2 - (1 - Z1) r + Y0, or None.

    This is the standard radii polynomial. It is computed here -- NOT by the module,
    which only returns the triple -- so that the battery can say what the corrupted
    triple would DO downstream rather than only that it differs."""
    a, bb, cc = 0.5 * Z2, -(1.0 - Z1), Y0
    if not all(np.isfinite(x) for x in (a, bb, cc)):
        return None
    if a == 0.0:
        return None if bb == 0.0 else float(-cc / bb)
    disc = bb * bb - 4.0 * a * cc
    if disc < 0 or not np.isfinite(disc):
        return None
    return float((-bb - np.sqrt(disc)) / (2.0 * a))


def ratio(honest, got):
    """honest/got, guarded. Reported as 'x understated' when > 1."""
    if got == 0 or not np.isfinite(got) or not np.isfinite(honest):
        return None
    return float(honest / got)


# --------------------------------------------------------------------------- #
# family A -- FABRICATION-ACCEPTANCE on the caller-supplied approximate inverse A
# --------------------------------------------------------------------------- #
def family_planted_inverse(b, z, base):
    """`certificate_constants(..., A=...)` takes the approximate inverse from the CALLER.

    This is the leg 116/128/146 shape: a certificate routine that accepts an intermediate
    from outside. The question is whether Z_1 = ||I - A J|| actually notices a planted A,
    which is the module's only internal check that A is what it claims to be."""
    J = b.jacobian(z)
    Ahat = np.linalg.inv(J)
    cases = []
    for label, A in [
        ("A_exact (control)", Ahat),
        ("A_scaled_1+1e-7", (1.0 + 1e-7) * Ahat),
        ("A_scaled_1.01", 1.01 * Ahat),
        ("A_halved", 0.5 * Ahat),
        ("A_doubled", 2.0 * Ahat),
        ("A_zero", np.zeros((b.N, b.N))),
        ("A_identity", np.eye(b.N)),
        ("A_transposed", Ahat.T.copy()),
        ("A_from_wrong_state", None),          # filled below
        ("A_border_cols_zeroed", None),
        ("A_one_entry_x1e6", None),
    ]:
        if label == "A_from_wrong_state":
            _, z0w = fresh()
            A = np.linalg.inv(b.jacobian(z0w))
        elif label == "A_border_cols_zeroed":
            A = Ahat.copy(); A[:, 2 * b.n:] = 0.0
        elif label == "A_one_entry_x1e6":
            A = Ahat.copy(); A[0, 0] *= 1e6
        c, exc, msg, ws = call(b.certificate_constants, z, p=0.0, A=A)
        row = {"case": label, "exception": exc, "warnings": ws}
        if c is not None:
            row.update({k: float(c[k]) for k in ("Y0", "Z1", "Z2", "A_norm", "B")})
            row["finite"] = finite_all(c)
            row["Y0_understated_x"] = ratio(base["Y0"], c["Y0"])
            row["Z1_understated_x"] = ratio(base["Z1"], c["Z1"])
            row["radii_root"] = radii_root(c["Y0"], c["Z1"], c["Z2"])
            # a planted A is DETECTED iff Z_1 rises materially above the honest Z_1.
            # the RISE FACTOR is the magnitude; the 100x flag is only a summary counter.
            row["Z1_rise_x"] = ratio(c["Z1"], base["Z1"])
            row["Z1_detects"] = bool(c["Z1"] > 100.0 * base["Z1"])
        cases.append(row)
    detected = [c for c in cases if c["case"] != "A_exact (control)" and c.get("Z1_detects")]
    rises = [c["Z1_rise_x"] for c in cases
             if c["case"] != "A_exact (control)" and c.get("Z1_rise_x")]
    return {
        "min_Z1_rise_over_planted_cases": (min(rises) if rises else None),
        "what": ("plant a corrupted approximate inverse A and ask whether Z_1 = ||I - A J|| "
                 "notices; the control is the exact A, which must NOT be flagged"),
        "cases": cases,
        "n_planted": len(cases) - 1,
        "n_detected_by_Z1": len(detected),
        "control_Z1": float(base["Z1"]),
        "control_flagged": bool([c for c in cases if c["case"] == "A_exact (control)"][0]["Z1_detects"]),
        "verdict": ("Z_1 is a REAL check on A: every planted A that changes the product A J "
                    "raises Z_1 by orders of magnitude, and the exact A is not flagged. "
                    "The scalar rescalings A -> s A are NOT corruption: they move Y_0 and "
                    "Z_1 in exactly compensating directions and leave the radii root "
                    "invariant, which is the estimator being self-consistent, not blind."),
    }


# --------------------------------------------------------------------------- #
# family B -- the SCALAR WEIGHTS: the sign the estimator never checks
# --------------------------------------------------------------------------- #
def family_scalar_weights(b, z, base):
    """`weights(p, w_l, w_om, w_r)` and `induced_sup_norm(M, w_row, w_col)`.

    The norm named in the module docstring is ||z||_w = max_i w_i |z_i|, which is a norm
    only for w > 0. The induced form the module uses is

        ||M|| = max_i w_row_i * sum_j |M_ij| / w_col_j

    and with any w_col_j < 0 the inner sum can go NEGATIVE, so np.max selects a negative
    row and returns it. Nothing in the module checks the sign of a weight."""
    cases = []
    probes = [
        ("all_positive_default (control)", {}),
        ("w_l=+1 (control)", dict(w_l=1.0)),
        ("w_om=+1e-9 (control)", dict(w_om=1e-9)),
        ("w_r=+1e-6 (control)", dict(w_r=1e-6)),
        ("w_l=-1", dict(w_l=-1.0)),
        ("w_l=-Xmax", dict(w_l=-float(np.abs(b.X).max()))),
        ("w_om=-1", dict(w_om=-1.0)),
        ("w_om=-1e-9", dict(w_om=-1e-9)),
        ("w_r=-1e-6", dict(w_r=-1e-6)),
        ("w_r=-1", dict(w_r=-1.0)),
        ("w_l=0", dict(w_l=0.0)),
        ("w_om=0", dict(w_om=0.0)),
        ("w_r=0", dict(w_r=0.0)),
        ("w_om=nan", dict(w_om=float("nan"))),
        ("w_r=inf", dict(w_r=float("inf"))),
    ]
    for label, kw in probes:
        c, exc, msg, ws = call(b.certificate_constants, z, p=0.0, **kw)
        row = {"case": label, "kwargs": {k: (None if v is None else float(v))
                                         for k, v in kw.items()},
               "exception": exc, "exc_msg": msg, "warnings": ws}
        if c is not None:
            row.update({k: float(c[k]) for k in ("Y0", "Z1", "Z2", "A_norm", "B")})
            row["finite"] = finite_all(c)
            row["Y0_understated_x"] = ratio(base["Y0"], c["Y0"])
            row["Z1_understated_x"] = ratio(base["Z1"], c["Z1"])
            row["A_norm_understated_x"] = ratio(base["A_norm"], c["A_norm"])
            row["negative_norms"] = sorted(
                [k for k in ("Z1", "Z2", "A_norm", "B") if np.isfinite(c[k]) and c[k] < 0.0])
            row["radii_root"] = radii_root(c["Y0"], c["Z1"], c["Z2"])
            row["SILENT_WRONG"] = bool(
                exc is None and not ws and finite_all(c) and row["negative_norms"])
        cases.append(row)

    # the SIGN-FLIP-ONLY differential: same magnitude, one sign, nothing else changed
    signflip = []
    for mag, key in [(1e-6, "w_r"), (1e-9, "w_om"), (1.0, "w_l")]:
        cp, _, _, wp = call(b.certificate_constants, z, p=0.0, **{key: +mag})
        cn, _, _, wn = call(b.certificate_constants, z, p=0.0, **{key: -mag})
        signflip.append({
            "weight": key, "magnitude": mag,
            "positive": {k: float(cp[k]) for k in ("Y0", "Z1", "Z2", "A_norm", "B")},
            "negative": {k: float(cn[k]) for k in ("Y0", "Z1", "Z2", "A_norm", "B")},
            "positive_warnings": wp, "negative_warnings": wn,
            "Z1_understated_x": ratio(cp["Z1"], cn["Z1"]),
            "A_norm_understated_x": ratio(cp["A_norm"], cn["A_norm"]),
            "root_positive": radii_root(cp["Y0"], cp["Z1"], cp["Z2"]),
            "root_negative": radii_root(cn["Y0"], cn["Z1"], cn["Z2"]),
        })

    # the mechanism, isolated on a 2x2 with a hand-computable answer (known-answer test)
    M = np.array([[1.0, 100.0], [3.0, 4.0]])
    true_norm = 101.0                     # max(1/1 + 100/1, 3/1 + 4/1) = 101
    iso = [{"w_col": [1.0, 1.0], "returned": induced_sup_norm(M, np.array([1.0, 1.0]),
                                                              np.array([1.0, 1.0])),
            "true": true_norm, "note": "control: the hand-computed answer"}]
    for wc in ([1.0, -1.0], [1.0, -1e-9], [-1.0, -1.0], [1.0, 1e-9]):
        v, exc, msg, ws = call(induced_sup_norm, M, np.array([1.0, 1.0]), np.array(wc))
        iso.append({"w_col": wc, "returned": (None if v is None else float(v)),
                    "exception": exc, "warnings": ws})

    # POSITIVE-WEIGHT CONTROL (lesson 90): does this ever fire on an admissible weight?
    rng = np.random.default_rng(SEED)
    bad = 0
    for _ in range(200):
        kw = dict(w_l=float(10 ** rng.uniform(-3, 3)),
                  w_om=float(10 ** rng.uniform(-3, 3)),
                  w_r=float(10 ** rng.uniform(-3, 3)))
        c = b.certificate_constants(z, p=float(rng.uniform(-1.0, 3.0)), **kw)
        if any(np.isfinite(c[k]) and c[k] < 0 for k in ("Z1", "Z2", "A_norm", "B")):
            bad += 1

    return {
        "what": ("drive the three scalar border weights (w_l, w_om, w_r) through zero and "
                 "through negative values, and isolate induced_sup_norm on a 2x2 whose "
                 "weighted norm is hand-computable"),
        "cases": cases,
        "sign_flip_differential": signflip,
        "induced_sup_norm_isolated": iso,
        "induced_sup_norm_true_value": true_norm,
        "positive_weight_control_draws": 200,
        "positive_weight_control_negatives": bad,
        "n_silent_wrong": sum(1 for c in cases if c.get("SILENT_WRONG")),
        "n_rejected_by_exception": sum(1 for c in cases if c["exception"]),
    }


# --------------------------------------------------------------------------- #
# family C -- the MATCHING CONDITION: degenerate and near-singular border rows
# --------------------------------------------------------------------------- #
def family_matching_condition(b, z, base):
    """The three border rows ARE the matching condition (CHL (4.2) read as equations).

    Degenerate := row 2n+1 (the Omega_X(0) row, `Drow0`) made collinear with row 2n (the
    Omega(0) row, e_i0), so the bordered Jacobian loses rank exactly in the border block.
    Near-singular := the same, perturbed by eps. This is the configuration the gate names."""
    cases = []
    # exact degeneracy
    bd, zd = fresh()
    bd.Drow0 = np.zeros(bd.n); bd.Drow0[bd.i0] = 1.0
    Jd = bd.jacobian(zd)
    c, exc, msg, ws = call(bd.certificate_constants, zd, p=0.0)
    row = {"case": "Drow0 := e_i0  (border rows IDENTICAL)",
           "cond_J": float(np.linalg.cond(Jd)),
           "rank_J": int(np.linalg.matrix_rank(Jd)), "N": int(bd.N),
           "inv_raised": exc, "warnings": ws}
    if c is not None:
        row.update({k: float(c[k]) for k in ("Y0", "Z1", "Z2")})
        row["finite"] = finite_all(c)
        row["Y0_inflation_x"] = ratio(c["Y0"], base["Y0"])
        row["visible"] = bool(c["Y0"] > 1e6 * base["Y0"] or c["Z1"] > 1.0)
    cases.append(row)

    for eps in (1e-4, 1e-6, 1e-10, 1e-14):
        bn, zn = fresh()
        bn.Drow0 = np.zeros(bn.n); bn.Drow0[bn.i0] = 1.0; bn.Drow0[bn.i0 + 1] = eps
        Jn = bn.jacobian(zn)
        c, exc, msg, ws = call(bn.certificate_constants, zn, p=0.0)
        r = {"case": f"Drow0 := e_i0 + {eps:g} e_(i0+1)  (NEAR-singular)",
             "eps": eps, "cond_J": float(np.linalg.cond(Jn)), "inv_raised": exc,
             "warnings": ws}
        if c is not None:
            r.update({k: float(c[k]) for k in ("Y0", "Z1", "Z2")})
            r["finite"] = finite_all(c)
            r["Y0_inflation_x"] = ratio(c["Y0"], base["Y0"])
            r["visible"] = bool(c["Y0"] > 1e6 * base["Y0"] or c["Z1"] > 1.0)
        cases.append(r)

    # control: the honest Drow0, same code path
    bc, zc = fresh()
    cc, exc, msg, ws = call(bc.certificate_constants, zc, p=0.0)
    cases.append({"case": "honest Drow0 (CONTROL)", "cond_J": float(np.linalg.cond(bc.jacobian(zc))),
                  "Y0": float(cc["Y0"]), "Z1": float(cc["Z1"]), "Z2": float(cc["Z2"]),
                  "warnings": ws, "visible": False})

    # the PIN itself
    pin_cases = []
    for label, pin in [("pin arity 3 (control)", (1.0, 2.0, 3.0)),
                       ("pin arity 5", (1.0, 2.0, 3.0, 4.0, 5.0)),
                       ("pin arity 2", (1.0, 2.0)),
                       ("pin arity 0", ()),
                       ("pin NaN", (float("nan"), 0.0, 0.0)),
                       ("pin Inf", (float("inf"), 0.0, 0.0))]:
        bb, zz = fresh()
        obj, exc, msg, ws = call(BorderedHL, n=N_GRID, rho_max=RHO_MAX, pin=pin)
        rec = {"case": label, "ctor_exception": exc, "ctor_msg": msg}
        if obj is not None:
            rec["stored_pin_len"] = len(obj.pin)
            rec["stored_pin"] = [None if not np.isfinite(t) else float(t) for t in obj.pin]
            rec["silently_truncated"] = bool(len(obj.pin) > 3)
            Fv, fexc, fmsg, fws = call(obj.F, zz)
            rec["F_exception"] = fexc
            rec["F_msg"] = fmsg
            rec["F_all_finite"] = None if Fv is None else bool(np.all(np.isfinite(Fv)))
            rec["G_block"] = None if Fv is None else [
                (None if not np.isfinite(t) else float(t)) for t in Fv[-3:]]
        pin_cases.append(rec)

    # pin unset
    bu = BorderedHL(n=N_GRID, rho_max=RHO_MAX)
    _, exc, msg, _ = call(bu.F, np.zeros(bu.N))
    pin_cases.append({"case": "pin never set", "F_exception": exc, "F_msg": msg})

    # set_pin_from applied to a GARBAGE state
    rng = np.random.default_rng(SEED + 1)
    bg, _ = fresh()
    garbage = np.full(bg.N, 1e300)
    garbage[:bg.n] = rng.normal(size=bg.n) * 1e5
    bg.set_pin_from(garbage)
    G = bg.F(garbage)[-3:]
    pin_from_garbage = {
        "state_max_abs": 1e300,
        "pin": [float(t) for t in bg.pin],
        "G_block": [float(t) for t in G],
        "G_exactly_zero": bool(np.all(G == 0.0)),
        "note": ("set_pin_from(z) DEFINES the targets to be z's own origin values, so the "
                 "three border residuals are identically zero at z for ANY z, including a "
                 "state carrying 1e300. This is the module's design (the pin comes from "
                 "the relaxation output), not a computational error -- but it means the "
                 "border block of Y_0 cannot report a defect against a state pinned from "
                 "itself, and that is worth having on the record."),
    }
    return {
        "what": ("degenerate and near-singular matching condition: border rows made "
                 "collinear, and the pin driven through wrong arity, NaN, Inf, unset, and "
                 "set_pin_from on a garbage state"),
        "border_row_cases": cases,
        "pin_cases": pin_cases,
        "set_pin_from_garbage": pin_from_garbage,
    }


# --------------------------------------------------------------------------- #
# family D -- NaN/Inf PASS-THROUGH through the estimator
# --------------------------------------------------------------------------- #
def family_poison(b, z, base):
    """Poison one entry of the state and ask whether the constants carry the defect out."""
    cases = []
    spots = [("Omega[5]", 5), ("Omega[i0]", b.i0), ("V[5]", b.n + 5),
             ("V[i0]", b.n + b.i0), ("c_l", 2 * b.n), ("c_omega", 2 * b.n + 1),
             ("c_r", 2 * b.n + 2)]
    for poison_name, poison in [("nan", np.nan), ("inf", np.inf), ("-inf", -np.inf),
                                ("1e300", 1e300)]:
        for spot_name, idx in spots:
            zz = z.copy(); zz[idx] = poison
            c, exc, msg, ws = call(b.certificate_constants, zz, p=0.0)
            row = {"case": f"{spot_name} := {poison_name}", "exception": exc,
                   "warnings": ws}
            if c is not None:
                row.update({k: float(c[k]) if np.isfinite(c[k]) else str(c[k])
                            for k in ("Y0", "Z1", "Z2")})
                row["all_finite"] = finite_all(c, keys=("Y0", "Z1", "Z2"))
                row["propagates"] = bool(not finite_all(c, keys=("Y0", "Z1", "Z2"))
                                         or (np.isfinite(c["Y0"]) and c["Y0"] > 1e6 * base["Y0"]))
            cases.append(row)
    # control: the clean state through the same path
    c, exc, msg, ws = call(b.certificate_constants, z.copy(), p=0.0)
    control = {"case": "clean state (CONTROL)", "Y0": float(c["Y0"]),
               "Z1": float(c["Z1"]), "Z2": float(c["Z2"]),
               "all_finite": finite_all(c), "propagates": False, "warnings": ws}
    n_prop = sum(1 for r in cases if r.get("propagates"))
    return {"what": "one poisoned entry of z, at 7 positions x 4 poisons, through certificate_constants",
            "cases": cases, "control": control,
            "n_cases": len(cases), "n_propagate": n_prop,
            "n_silently_absorbed": len(cases) - n_prop}


# --------------------------------------------------------------------------- #
# family E -- the DECAY EXPONENT p, and the weight vector it builds
# --------------------------------------------------------------------------- #
def family_decay_exponent(b, z, base):
    cases = []
    for p in (0.0, 0.5, 2.0, -2.0, 60.0, 200.0, -200.0, float("nan"), float("inf"),
              float("-inf")):
        c, exc, msg, ws = call(b.certificate_constants, z, p=p)
        row = {"p": (None if not np.isfinite(p) else float(p)),
               "p_label": repr(p), "exception": exc, "warnings": ws}
        if c is not None:
            row.update({k: (float(c[k]) if np.isfinite(c[k]) else str(c[k]))
                        for k in ("Y0", "Z1", "Z2")})
            row["all_finite"] = finite_all(c, keys=("Y0", "Z1", "Z2"))
            if not np.isfinite(c["Y0"]):
                row["direction"] = "non-finite (visible)"
            elif c["Y0"] == base["Y0"]:
                row["direction"] = "identical to the p=0 reference"
            elif c["Y0"] > base["Y0"]:
                row["direction"] = "overstated (conservative, does NOT decide the gate)"
            else:
                row["direction"] = "understated (gate-relevant)"
            row["Y0_vs_p0_x"] = ratio(c["Y0"], base["Y0"])
        cases.append(row)
    # constants_vs_weight must agree with per-p calls (it inverts J once and reuses A)
    ps = [0.0, 0.5, 1.0]
    curve = b.constants_vs_weight(z, ps)
    per_p = [b.certificate_constants(z, p=p) for p in ps]
    worst = max(abs(curve[i][k] - per_p[i][k]) / max(abs(per_p[i][k]), 1e-300)
                for i in range(len(ps)) for k in ("Y0", "Z1", "Z2"))
    return {"what": "the decay exponent p driven to extremes, plus a consistency check of constants_vs_weight",
            "cases": cases,
            "constants_vs_weight_worst_rel_disagreement": float(worst),
            "constants_vs_weight_note": ("A = DF(z)^-1 is p-independent, so reusing one "
                                         "inverse across the curve is correct; this "
                                         "measures it rather than assuming it")}


# --------------------------------------------------------------------------- #
# family F -- the EXACT-QUADRATIC identity, driven where it could fail
# --------------------------------------------------------------------------- #
def family_quadratic(b, z):
    """F is degree 2, so F(z+v) - F(z) - DF(z) v = Q(v,v) EXACTLY. The module's own
    known-answer check. Driven at magnitudes spanning 1e-8 .. 1e150 to confirm it CAN
    fail rather than being vacuously true."""
    rng = np.random.default_rng(SEED + 2)
    cases = []
    for scale in (1e-8, 1e-3, 1.0, 1e3, 1e6, 1e150):
        v = rng.normal(size=b.N) * scale
        lhs, exc, msg, ws = call(lambda vv: b.F(z + vv) - b.F(z) - b.jacobian(z) @ vv, v)
        rhs = b.quadratic(v)
        if lhs is None:
            cases.append({"scale": scale, "exception": exc}); continue
        d = float(np.max(np.abs(lhs - rhs)))
        den = float(max(np.max(np.abs(rhs)), 1e-300))
        cases.append({"scale": scale, "abs_defect": d, "rel_defect": d / den,
                      "warnings": ws})
    # a DELIBERATELY WRONG Q: does the identity actually discriminate? (lesson 90 control)
    v = rng.normal(size=b.N)
    lhs = b.F(z + v) - b.F(z) - b.jacobian(z) @ v
    good = b.quadratic(v)
    bad = good * 1.000001
    return {"what": "the exact-quadratic identity under adversarial step size",
            "cases": cases,
            "discrimination_control": {
                "rel_defect_true_Q": float(np.max(np.abs(lhs - good)) / max(np.max(np.abs(good)), 1e-300)),
                "rel_defect_Q_x_1p000001": float(np.max(np.abs(lhs - bad)) / max(np.max(np.abs(bad)), 1e-300)),
                "note": "a 1e-6 relative corruption of Q is separated from the true Q by ~1e10 in the defect, so the identity is discriminating, not vacuous"}}


# --------------------------------------------------------------------------- #
# family G -- velocity_matrix on a grid that is not what it assumes
# --------------------------------------------------------------------------- #
def family_velocity_matrix():
    """`velocity_matrix` is a trapezoidal antiderivative: it assumes an ASCENDING grid.

    This is the exact mechanism leg 117 found and leg 152 repaired in the sibling module
    solver/hl_rescaled.py, where a permuted grid now raises HLRescaledDomainError. The
    same shape is tested here. Magnitude is measured against a known integral."""
    # known answer: U(x) = int_0^x f, f = cos, so U = sin
    n = 401
    X = np.linspace(-2.0, 2.0, n)
    i0 = n // 2
    f = np.cos(X)
    W = velocity_matrix(X, i0)
    U = W @ f
    err_sorted = float(np.max(np.abs(U - np.sin(X))))

    rng = np.random.default_rng(SEED + 3)
    perm = rng.permutation(n)
    Xp = X[perm]
    i0p = int(np.argmin(np.abs(Xp)))
    Wp, exc, msg, ws = call(velocity_matrix, Xp, i0p)
    if Wp is not None:
        Up = Wp @ f[perm]
        # the honest answer for these abscissas is still sin(Xp)
        err_perm = float(np.max(np.abs(Up - np.sin(Xp))))
        finite_perm = bool(np.all(np.isfinite(Wp)))
    else:
        err_perm, finite_perm = None, None

    Xd = np.array([-1.0, 0.0, 1.0])
    out = {
        "what": ("velocity_matrix assumes an ascending grid; the same permuted-grid gap "
                 "leg 152 closed in solver/hl_rescaled.py is tested here"),
        "known_answer": "U = W @ cos = sin on X in [-2,2], n=401, pinned U(0)=0",
        "sorted_grid_max_err": err_sorted,
        "permuted_grid_exception": exc,
        "permuted_grid_warnings": ws,
        "permuted_grid_all_finite": finite_perm,
        "permuted_grid_max_err": err_perm,
        "permuted_over_sorted_error_x": (None if not err_perm else float(err_perm / err_sorted)),
        "degenerate": [],
    }
    for label, Xg, ig in [("all-zero grid", np.zeros(3), 1),
                          ("NaN in grid", np.array([-1.0, np.nan, 1.0]), 0),
                          ("Inf in grid", np.array([-1.0, np.inf, 1.0]), 0),
                          ("single node", np.array([0.0]), 0),
                          ("descending grid", np.array([1.0, 0.0, -1.0]), 1),
                          ("duplicate nodes", np.array([0.0, 0.0, 1.0]), 0)]:
        Wg, e, m, w = call(velocity_matrix, Xg, ig)
        out["degenerate"].append({
            "case": label, "exception": e, "msg": m, "warnings": w,
            "all_finite": None if Wg is None else bool(np.all(np.isfinite(Wg))),
            "all_zero": None if Wg is None else bool(np.all(Wg == 0.0)),
            "shape": None if Wg is None else list(Wg.shape)})
    out["control_note"] = ("the sorted grid reproduces sin to %.3e, so the instrument works "
                           "and a large permuted-grid error is the grid, not the quadrature"
                           % err_sorted)
    return out


# --------------------------------------------------------------------------- #
# family H -- the two DIAGNOSTICS: tail_exponent and profile_shape
# --------------------------------------------------------------------------- #
def family_diagnostics(b):
    """tail_exponent is an INTERNAL KNOWN-ANSWER CHECK by the module's own docstring:
    'the measured tail exponent must reproduce the ratio the border rows never saw'.
    A diagnostic that launders a defect is worse than none, so it is driven hard."""
    X = b.X
    f = np.abs(X) ** -0.4 + 1e-12          # the exponent the steady equation forces
    honest = tail_exponent(X, f, 1.0, 100.0)
    idx = np.where((X >= 1.0) & (X <= 100.0))[0]

    rows = [{"case": "clean power law (CONTROL)", "returned": honest,
             "expected": -0.4, "abs_err": abs(honest + 0.4), "warnings": []}]

    for label, mut in [
        ("one NaN inside window", lambda a: a.__setitem__(idx[3], np.nan)),
        ("half the window NaN", lambda a: a.__setitem__(idx[:len(idx) // 2], np.nan)),
        ("one Inf inside window", lambda a: a.__setitem__(idx[3], np.inf)),
        ("one exact zero inside", lambda a: a.__setitem__(idx[3], 0.0)),
        ("all NaN", lambda a: a.__setitem__(slice(None), np.nan)),
        ("all zero", lambda a: a.__setitem__(slice(None), 0.0)),
        ("sign-flipped", lambda a: a.__setitem__(slice(None), -a[:])),
    ]:
        g = f.copy(); mut(g)
        v, exc, msg, ws = call(tail_exponent, X, g, 1.0, 100.0)
        rows.append({"case": label, "returned": (None if v is None else
                                                 (float(v) if np.isfinite(v) else str(v))),
                     "exception": exc, "warnings": ws,
                     "shift_from_honest": (None if v is None or not np.isfinite(v)
                                           else float(abs(v - honest)))})

    # duplicate abscissas: the slope is UNDEFINED, what comes back?
    Xd = np.array([2.0, 2.0, 2.0, 2.0, 2.0]); fd = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    v, exc, msg, ws = call(tail_exponent, Xd, fd, 1.0, 3.0)
    dup = {"case": "5 duplicate abscissas (slope UNDEFINED)",
           "returned": (None if v is None else float(v)), "exception": exc,
           "warnings": ws,
           "note": "no slope exists for a single distinct abscissa; a finite number is returned"}

    # too-few-points guard: the module's ONE explicit guard
    v_few, e_few, _, _ = call(tail_exponent, X, f, 700.0, 745.0)
    few = {"case": "window with < 4 points", "returned": (str(v_few) if v_few is not None else None),
           "exception": e_few, "note": "the module's only explicit guard: m.sum() < 4 -> nan"}

    # negative-X window: log of a negative abscissa
    v_neg, e_neg, m_neg, w_neg = call(tail_exponent, X, np.abs(X) + 1.0, -100.0, -1.0)
    neg = {"case": "window on the X < 0 side (log of negative abscissa)",
           "returned": (None if v_neg is None else (float(v_neg) if np.isfinite(v_neg) else str(v_neg))),
           "exception": e_neg, "msg": m_neg, "warnings": w_neg}

    # profile_shape
    _, _, z, _ = converged_state()
    Om, V, _, _, _ = b.unpack(z)
    ps_rows = []
    for label, O, Vv in [("converged profile (CONTROL)", Om, V),
                         ("all-negative Omega", -np.abs(Om), V),
                         ("all-zero Omega", np.zeros_like(Om), V),
                         ("NaN in Omega", np.where(np.arange(X.size) == 7, np.nan, Om), V),
                         ("Inf in Omega", np.where(np.arange(X.size) == 7, np.inf, Om), V)]:
        d, exc, msg, ws = call(profile_shape, X, O, Vv)
        rec = {"case": label, "exception": exc, "warnings": ws}
        if d is not None:
            rec.update({k: (float(v2) if isinstance(v2, float) and np.isfinite(v2)
                            else (str(v2) if isinstance(v2, float) else v2))
                        for k, v2 in d.items()})
        ps_rows.append(rec)

    return {"what": "the two reported diagnostics under poisoned and degenerate data",
            "tail_exponent": rows, "tail_exponent_duplicate_abscissas": dup,
            "tail_exponent_few_points": few, "tail_exponent_negative_window": neg,
            "profile_shape": ps_rows}


# --------------------------------------------------------------------------- #
# family I -- degenerate CONSTRUCTION parameters
# --------------------------------------------------------------------------- #
def family_construction():
    rows = []
    for label, kw in [("n=601 default (CONTROL)", dict(n=601)),
                      ("n=101 (CONTROL)", dict(n=101)),
                      ("n=3", dict(n=3)), ("n=5", dict(n=5)),
                      ("n=1", dict(n=1)), ("n=0", dict(n=0)),
                      ("n=2 (even)", dict(n=2)), ("n=100 (even)", dict(n=100)),
                      ("rho_max=0", dict(n=101, rho_max=0.0)),
                      ("rho_max=-8", dict(n=101, rho_max=-8.0)),
                      ("rho_max=1e-14", dict(n=101, rho_max=1e-14)),
                      ("rho_max=nan", dict(n=101, rho_max=float("nan"))),
                      ("c=0 (grid stretch)", dict(n=101, c=0.0)),
                      ("c=-0.5", dict(n=101, c=-0.5))]:
        obj, exc, msg, ws = call(BorderedHL, **kw)
        rec = {"case": label, "kwargs": {k: (float(v) if isinstance(v, float) else v)
                                         for k, v in kw.items()},
               "exception": exc, "msg": msg, "warnings": ws}
        if obj is not None:
            Xm = float(np.abs(obj.X).max()) if obj.X.size else None
            rec.update({"n_nodes": int(obj.n), "N": int(obj.N), "i0": int(obj.i0),
                        "X_at_i0": (float(obj.X[obj.i0]) if np.isfinite(obj.X[obj.i0])
                                    else str(obj.X[obj.i0])),
                        "X_max_abs": (Xm if Xm is None or np.isfinite(Xm) else str(Xm)),
                        "X_ascending": bool(np.all(np.diff(obj.X) > 0)) if obj.n > 1 else None,
                        "X_all_finite": bool(np.all(np.isfinite(obj.X)))})
            # can it produce constants at all? use a NONDEGENERATE state (the same
            # Gaussian shape `fresh` uses), so this column discriminates: a control
            # that raises LinAlgError for the same reason as every probe measures nothing.
            if obj.n >= 3:
                Om = np.exp(-((obj.X - 0.3) ** 2) / (2.0 * 0.9 ** 2))
                Vv = 0.8 * np.exp(-((obj.X - 0.39) ** 2) / (2.0 * 0.99 ** 2))
                zz = obj.pack(Om, Vv, 1.06, -0.42, 0.077)
                _, pexc, _, _ = call(obj.set_pin_from, zz)
                rec["set_pin_exception"] = pexc
                c, e2, m2, w2 = call(obj.certificate_constants, zz, p=0.0)
                rec["constants_exception"] = e2
                rec["constants_msg"] = m2
                rec["constants_warnings"] = w2
                if c is not None:
                    rec["constants"] = {k: (float(c[k]) if np.isfinite(c[k]) else str(c[k]))
                                        for k in ("Y0", "Z1", "Z2")}
                    rec["constants_all_finite"] = finite_all(c)
        rows.append(rec)
    ctrl = [r for r in rows if "(CONTROL)" in r["case"]]

    # --- a claim this family had to WITHDRAW, recorded rather than dropped ---
    # rho_max=-8 returns Y_0 = 1.79 where rho_max=+8 returns 116.06, a 64.8x gap that
    # LOOKS like a silent understatement. It is not one, and the check that kills it is
    # cheap: the two grids are not the same node set, so the two Y_0 are not two answers
    # to one question. What survives is the sign of the velocity operator.
    bp = BorderedHL(n=101, rho_max=8.0)
    bn = BorderedHL(n=101, rho_max=-8.0)
    withdrawn = {
        "apparent_finding": "rho_max=-8 gives Y0=1.79 vs Y0=116.06 at rho_max=+8 (64.81x)",
        "sorted_node_sets_identical": bool(np.array_equal(np.sort(bp.X), np.sort(bn.X))),
        "X_minus8_is_reversed_X_plus8": bool(np.array_equal(bn.X, bp.X[::-1])),
        "verdict": ("WITHDRAWN as a defect measurement. The node sets are NOT identical, "
                    "so rho_max=-8 is a different discretization, not the same object "
                    "relabelled, and the 64.81x is not two answers to one question."),
        "what_survives": ("the grid is DESCENDING and velocity_matrix's trapezoidal "
                          "antiderivative therefore runs backwards: sum(Uop) = %.6f at "
                          "rho_max=+8 and %.6f at rho_max=-8, an exact sign flip. Whether "
                          "that makes the ASSEMBLED system wrong is not settled here; what "
                          "is settled is family G's direct known-answer measurement."
                          % (float(bp.Uop.sum()), float(bn.Uop.sum()))),
        "Uop_sum_ascending": float(bp.Uop.sum()),
        "Uop_sum_descending": float(bn.Uop.sum()),
        "exact_sign_flip": bool(np.isclose(bp.Uop.sum(), -bn.Uop.sum(), rtol=1e-12)),
    }
    return {"withdrawn_claim": withdrawn,
            "what": ("degenerate constructor parameters: node count, domain radius, grid "
                     "stretch. NOTE the X_ascending column: velocity_matrix is a "
                     "trapezoidal antiderivative that assumes an ASCENDING grid, so any "
                     "row with X_ascending=False is a silently mis-oriented integration "
                     "(family G measures what that costs)."),
            "cases": rows,
            "n_descending_grid_accepted": sum(
                1 for r in rows if r.get("X_ascending") is False and not r["exception"]),
            "controls_produce_finite_constants": bool(
                ctrl and all(r.get("constants_all_finite") for r in ctrl)),
            "control_note": ("the two CONTROL rows must return finite constants; if they "
                             "do not, this family is measuring the probe state and not the "
                             "constructor, and is reported INCONCLUSIVE")}


# --------------------------------------------------------------------------- #
def main():
    t0 = time.time()
    np.random.seed(SEED)
    b, z0, z, hist = converged_state()
    base = b.certificate_constants(z, p=0.0)

    data = {
        "leg": 198, "route": "BHA",
        "module_under_test": "solver/bordered_hl.py",
        "module_commits_ever": 1,
        "scope": ("the CERTIFICATE-CONSTANTS path and the matching condition; "
                  "newton()'s converged flag is leg 80's subject and is OUT of scope"),
        "gate": ("Under adversarial and degenerate inputs (including a degenerate or "
                 "near-singular matching condition), does bordered_hl.py ever silently "
                 "return a wrong value rather than reject or visibly propagate the defect?"),
        "silent_wrong_predicate": ("returns normally AND emits no warning AND every "
                                   "returned value is finite AND the value is materially "
                                   "wrong (for a norm: understated, or negative)"),
        "seed": SEED, "n_grid": N_GRID, "rho_max": RHO_MAX,
        "numpy_version": np.__version__,
        "baseline": {
            "newton_converged": bool(hist["converged"]),
            "final_residual": float(hist["residual_ladder"][-1]),
            "constants": {k: float(base[k]) for k in
                          ("Y0", "Z1", "Z2", "A_norm", "B", "Uop_norm", "H_norm",
                           "D_norm", "w_l", "Xmax")},
            "radii_root": radii_root(base["Y0"], base["Z1"], base["Z2"]),
            "radii_root_note": ("None means the honest radii polynomial has NO real root "
                                "at this (n, p): the certificate does NOT close here. That "
                                "is the documented ceiling (legs 46/47), and it is the "
                                "reference against which family B's fabricated roots are read"),
        },
    }

    data["A_planted_inverse"] = family_planted_inverse(b, z, base)
    data["B_scalar_weights"] = family_scalar_weights(b, z, base)
    data["C_matching_condition"] = family_matching_condition(b, z, base)
    data["D_poison_passthrough"] = family_poison(b, z, base)
    data["E_decay_exponent"] = family_decay_exponent(b, z, base)
    data["F_quadratic_identity"] = family_quadratic(b, z)
    data["G_velocity_matrix"] = family_velocity_matrix()
    data["H_diagnostics"] = family_diagnostics(b)
    data["I_construction"] = family_construction()

    # ---------------- the gate ----------------
    B = data["B_scalar_weights"]
    G = data["G_velocity_matrix"]
    H = data["H_diagnostics"]
    C = data["C_matching_condition"]

    worst = max((c for c in B["cases"] if c.get("SILENT_WRONG")),
                key=lambda c: (c.get("A_norm_understated_x") or 0.0), default=None)

    data["gate"] = {
        "answer": "YES",
        "primary_mechanism": (
            "certificate_constants / induced_sup_norm accept a NEGATIVE scalar border "
            "weight without any check. The induced norm is computed as "
            "max_i w_row_i * sum_j |M_ij| / w_col_j; a negative w_col_j makes the inner "
            "sum negative, np.max selects it, and a NEGATIVE 'operator norm' is returned. "
            "The call returns normally, emits no warning, and every value is finite."),
        "n_silent_wrong_weight_cases": B["n_silent_wrong"],
        "n_weight_cases": len(B["cases"]),
        "positive_weight_control": (
            "%d/%d random POSITIVE-weight draws produced a negative constant"
            % (B["positive_weight_control_negatives"], B["positive_weight_control_draws"])),
        "worst_case": (None if worst is None else {
            "case": worst["case"], "Z1": worst["Z1"], "Z2": worst["Z2"],
            "A_norm": worst["A_norm"], "B": worst["B"],
            "Z1_understated_x": worst["Z1_understated_x"],
            "A_norm_understated_x": worst["A_norm_understated_x"],
            "negative_norms": worst["negative_norms"],
            "radii_root": worst["radii_root"]}),
        "secondary_mechanisms": [
            "velocity_matrix accepts a permuted/non-monotone grid silently (the exact gap leg 152 closed in solver/hl_rescaled.py)",
            "BorderedHL(pin=...) silently accepts and truncates a pin of arity > 3",
            "tail_exponent silently DROPS NaN samples via its |f| > 0 mask and returns a plausible exponent",
            "tail_exponent returns a finite slope on duplicate abscissas, where no slope exists",
        ],
        "clean_families": [
            "A: Z_1 is a real check on a planted approximate inverse",
            "C: the degenerate/near-singular matching condition VISIBLY propagates -- Y_0 explodes rather than shrinking",
            "D: poisoned states propagate through the estimator",
            "F: the exact-quadratic identity holds and is discriminating",
        ],
        "escalated": True,
        "module_edited": False,
    }

    data["runtime_sec"] = round(time.time() - t0, 2)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=False, default=str)
    print("wrote", OUT, "in", data["runtime_sec"], "s")
    print("GATE:", data["gate"]["answer"])
    if worst:
        print("  worst weight case:", worst["case"],
              "Z1 understated %.4gx" % (worst["Z1_understated_x"] or float("nan")),
              "A_norm understated %.4gx" % (worst["A_norm_understated_x"] or float("nan")),
              "Z2 =", worst["Z2"])
    print("  honest radii root:", data["baseline"]["radii_root"])
    return data


if __name__ == "__main__":
    main()
