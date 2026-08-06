"""Leg 218, Route-BHR -- the border-weight guard for solver/bordered_hl.py, and its
bit-identity licence.

WHAT THIS LEG REPAIRS
---------------------
Leg 198 (Route-BHA) measured that `solver/bordered_hl.py` silently accepts a NEGATIVE
border weight. `induced_sup_norm(M, w_row, w_col)` computes

    max_i  w_row_i * sum_j |M_ij| / w_col_j

which is the induced norm of ||z||_w = max_i w_i |z_i| -- and that display is a norm
ONLY for w > 0. With a negative w_col_j the inner row sum goes negative, `np.max`
selects it, and a NEGATIVE "operator norm" is returned: finite, unwarned, unraised.
On a 2x2 whose true weighted norm is 101.0 it returns -1.0 to -4.0e9. Through
`certificate_constants` a single sign flip understates Z_1 by ~1e8-1e12x and ||A|| by
~1e10x, drives Z_2 NEGATIVE (inverting the radii polynomial's curvature, so the
fabricated certificate claims an unbounded validation radius), and converts a
certificate that does NOT close into one that closes at r ~ 2.2e-11.

Leg 198 escalated rather than patched, per its own gate's YES branch. This leg is the
repair, and its territory is the border-weight guard ONLY -- leg 198's BHA-2
(permuted grid), BHA-3 (pin arity) and BHA-4 (tail_exponent NaN drop) are declared
residues and are NOT touched.

THE GATE (pre-committed, both branches, exact wording)
------------------------------------------------------
"Does adding a border-weight non-negativity guard (per leg 198's own identified
mechanism) cause every one of leg 198's adversarial negative-weight cases to now
reject, while every live caller across 54/58/127/192's own re-derivation stays
bit-identical to its pre-repair banked value?"

Clause (a) is the repair. Clause (b) is the LICENCE, and it is a measurement and not
an argument: the pre-repair module is read out of git and imported into THIS SAME
PROCESS under a second name, both modules are run over every clean configuration the
live callers use, and the float64 results are compared with `==` on their raw bytes --
not `allclose`. That method is inherited verbatim from legs 129/130/150/151/152.

The reason it must be same-process and bytewise is measured, not stylistic:
`Z_1 = ||I - A*DF||` with `A = inv(DF)` in float64 is a near-total cancellation
(honest value here 5.5e-09), so it is dominated by its own round-off and its RATIOS
are not stable across BLAS build or threading. See `writeup/novelty/leg_218.md` sec 6,
which re-measures two of leg 198's Z_1 ratios for exactly this reason.

TWO PREMISES OF THE DISPATCH ARE MEASURED FALSE HERE, NOT ARGUED
-----------------------------------------------------------------
(1) Legs 54/58/127 do NOT call this module -- 0 of their 7 runner/evidence files
    import it; they rest on `solver/spectral_certificate.py`. Leg 192 has not landed.
    Checking clause (b) on those four would be a lesson-90 tautology -- a control that
    cannot come out differently. So clause (b) is answered on the caller set
    enumerated BY IMPORT, which is the load-bearing one.
(2) The gate's own word "non-negativity" is the WEAKEST of the three candidate
    predicates and admits w = 0 (a seminorm), NaN, and +inf. The landed predicate is
    strict positivity AND finiteness, in confirm-good polarity. Family P measures
    every candidate on the same inputs so the choice is visible, not asserted.

LESSON-90 CONTROL, DECLARED BEFORE THE RUN
-------------------------------------------
The differential is VOID unless the two module objects are demonstrably
DISTINGUISHABLE: pre-repair must ACCEPT w_r = -1e-6 and return a negative-weight
Z_1 where post-repair REFUSES. Without that, "0 leaves moved" would be a tautology
about having loaded the same file twice. The runner aborts if the control does not hold.

Run: .venv/bin/python experiments/p2_route_bhr_v1_repair.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import time
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.bordered_hl import (                                        # noqa: E402
    BorderedHL, BorderedHLDomainError, induced_sup_norm)

OUT = ROOT / "writeup" / "data" / "p2_route_bhr_v1_repair.json"

# The module's only commit; origin/main's blob is byte-identical to it and this is
# ASSERTED below, not assumed (leg 130's d871675 correction on pre-repair pins).
PRE_REF = "0c075b8"
MODULE_PATH = "solver/bordered_hl.py"


# --------------------------------------------------------------------------- #
# load the PRE-REPAIR module out of git, into this same process
# --------------------------------------------------------------------------- #
def load_pre_repair():
    """Import the pre-repair `bordered_hl` under a second name, same interpreter.

    Same process is the point: identical BLAS, identical threading, identical
    libm. Anything that differs between the two objects is then the patch and
    nothing else."""
    src = subprocess.run(["git", "show", f"{PRE_REF}:{MODULE_PATH}"],
                         cwd=str(ROOT), capture_output=True, check=True).stdout
    head = subprocess.run(["git", "rev-parse", f"origin/main:{MODULE_PATH}"],
                          cwd=str(ROOT), capture_output=True).stdout.decode().strip()
    pin = subprocess.run(["git", "rev-parse", f"{PRE_REF}:{MODULE_PATH}"],
                         cwd=str(ROOT), capture_output=True).stdout.decode().strip()
    spec = importlib.util.spec_from_loader("bordered_hl_pre", loader=None)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = str(ROOT / MODULE_PATH)
    sys.modules["bordered_hl_pre"] = mod
    exec(compile(src, "<bordered_hl@%s>" % PRE_REF, "exec"), mod.__dict__)
    return mod, {"pre_ref": PRE_REF, "pre_blob": pin, "origin_main_blob": head,
                 "blob_identical": bool(head == pin and pin != ""),
                 "source_bytes": len(src)}


# --------------------------------------------------------------------------- #
# harness
# --------------------------------------------------------------------------- #
def fresh(mod, n=101, rho_max=8.0, c=0.5, x0=0.3, w=0.9):
    """The well-posed non-symmetric starting data test_bordered_hl.py and legs 80/198 use."""
    b = mod.BorderedHL(n=n, rho_max=rho_max, c=c)
    Om = np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = 0.8 * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    z0 = b.pack(Om, V, 1.06, -0.42, 0.077)
    b.set_pin_from(z0)
    return b, z0


def converged(mod, n=101, rho_max=8.0, c=0.5):
    b, z0 = fresh(mod, n=n, rho_max=rho_max, c=c)
    z, hist = b.newton(z0, tol=1e-12, max_iter=40)
    return b, z0, z, hist


def call(fn, *a, **kw):
    """Run fn capturing BOTH exception and warnings -- leg 198's own predicate needs
    the warning channel to be decidable rather than asserted."""
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            v = fn(*a, **kw)
        except Exception as e:                       # noqa: BLE001 -- the point
            return None, type(e).__name__, str(e)[:220], sorted(
                {w.category.__name__ for w in ws})
        return v, None, None, sorted({w.category.__name__ for w in ws})


def radii_root(Y0, Z1, Z2):
    """Smallest positive root of p(r) = (Z2/2) r^2 - (1 - Z1) r + Y0, or None.

    Computed HERE and not by the module -- the module only returns the triple -- so the
    battery can say what a corrupted triple would DO downstream, not merely that it
    differs. Same helper as leg 198's, so the two legs' columns are comparable."""
    a, bb, cc = 0.5 * Z2, -(1.0 - Z1), Y0
    if not all(np.isfinite(x) for x in (a, bb, cc)):
        return None
    if a == 0.0:
        return None if bb == 0.0 else float(-cc / bb)
    disc = bb * bb - 4.0 * a * cc
    if disc < 0 or not np.isfinite(disc):
        return None
    return float((-bb - np.sqrt(disc)) / (2.0 * a))


# --------------------------------------------------------------------------- #
# bitwise leaf comparison
# --------------------------------------------------------------------------- #
def leaves(obj, prefix, out):
    """Flatten to named float64 leaves. NaN is compared by BIT PATTERN, so NaN==NaN
    counts as identical (leg 152's convention) and a NaN that MOVED is still caught."""
    if isinstance(obj, dict):
        for k in sorted(obj):
            leaves(obj[k], f"{prefix}.{k}", out)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            leaves(v, f"{prefix}[{i}]", out)
    elif isinstance(obj, np.ndarray):
        flat = np.asarray(obj, dtype=float).ravel()
        for i, v in enumerate(flat):
            out.append((f"{prefix}[{i}]", float(v)))
    elif isinstance(obj, (bool, np.bool_)):
        out.append((prefix, 1.0 if obj else 0.0))
    elif isinstance(obj, (int, float, np.floating, np.integer)):
        out.append((prefix, float(obj)))


def same_bits(a, b):
    """`==` on the raw float64 bytes, with NaN==NaN counted identical."""
    xa = np.float64(a).tobytes()
    xb = np.float64(b).tobytes()
    if xa == xb:
        return True
    return bool(np.isnan(a) and np.isnan(b))


# --------------------------------------------------------------------------- #
# family P -- the PREDICATE, measured rather than prescribed
# --------------------------------------------------------------------------- #
def family_predicate(pre, post):
    """Every candidate predicate on the same inputs, plus what each module returns.

    This is the family that decides the gate's own WORD. "Non-negativity" (w < 0) is
    the gate's literal text and it is the weakest of the three: it admits w = 0 (which
    makes the display a SEMINORM, deleting a component) and NaN and +inf."""
    M = np.array([[1.0, 100.0], [3.0, 4.0]])        # true weighted norm = 101.0 exactly
    TRUE = 101.0
    cases = {"positive (control)": [1.0, 1.0], "negative": [1.0, -1.0],
             "negative tiny": [1.0, -1e-9], "both negative": [-1.0, -1.0],
             "zero": [1.0, 0.0], "nan": [1.0, np.nan],
             "posinf": [1.0, np.inf], "neginf": [1.0, -np.inf]}
    preds = {
        "any(w<0)   [the gate's literal word: NON-NEGATIVITY]": lambda w: np.any(w < 0),
        "any(w<=0)  [detect-bad, non-positivity]": lambda w: np.any(w <= 0),
        "not all(isfinite(w) & w>0)  [ADOPTED, confirm-good]":
            lambda w: not np.all(np.isfinite(w) & (w > 0)),
    }
    rows = []
    for name, wc in cases.items():
        w = np.array(wc, dtype=float)
        vpre, epre, mpre, wpre = call(pre.induced_sup_norm, M, np.array([1.0, 1.0]), w)
        vpost, epost, mpost, wpost = call(post.induced_sup_norm, M, np.array([1.0, 1.0]), w)
        silent_wrong_pre = bool(
            epre is None and not wpre and vpre is not None
            and np.isfinite(vpre) and abs(vpre - TRUE) > 1e-9)
        rows.append({
            "case": name, "w_col": [None if not np.isfinite(x) else float(x) for x in w],
            "w_col_repr": [repr(float(x)) for x in w],
            "true_norm": TRUE,
            "pre": {"returned": None if vpre is None else float(vpre),
                    "exception": epre, "warnings": wpre},
            "post": {"returned": None if vpost is None else float(vpost),
                     "exception": epost, "message": mpost, "warnings": wpost},
            "pre_silent_wrong": silent_wrong_pre,
            "understatement_x": (None if vpre is None or not np.isfinite(vpre) or vpre == 0
                                 else float(TRUE / vpre)),
            "post_rejects": bool(epost == "BorderedHLDomainError"),
            "predicates": {k: bool(f(w)) for k, f in preds.items()},
        })
    # w_row is guarded too, and pre-repair it is correct BY LUCK on leg 198's matrix
    luck = []
    for lab, MM, wr, truth in [
            ("leg 198's own 2x2 (max picks the UNflipped row)", M, [1.0, -1.0], 101.0),
            ("a 2x2 where the luck runs out", np.array([[1.0, 2.0], [3.0, 400.0]]),
             [1.0, -1.0], 403.0)]:
        v, e, m, ws = call(pre.induced_sup_norm, MM, np.array(wr), np.array([1.0, 1.0]))
        v2, e2, m2, _ = call(post.induced_sup_norm, MM, np.array(wr), np.array([1.0, 1.0]))
        luck.append({"case": lab, "w_row": wr, "true_norm": truth,
                     "pre_returned": None if v is None else float(v),
                     "pre_correct_by_luck": bool(v is not None and abs(v - truth) < 1e-9),
                     "pre_understatement_x": (None if v is None or v == 0
                                              else float(truth / v)),
                     "post_exception": e2})
    return {
        "what": ("every candidate predicate on the same inputs, against what the pre- "
                 "and post-repair modules actually return on leg 198's hand-computable "
                 "2x2 (true weighted norm 101.0 exactly)"),
        "matrix": M.tolist(), "true_norm": TRUE,
        "cases": rows,
        "w_row_is_guarded_too": luck,
        "n_pre_silent_wrong": sum(r["pre_silent_wrong"] for r in rows),
        "n_post_rejects": sum(r["post_rejects"] for r in rows),
        "control_positive_unchanged": bool(
            rows[0]["pre"]["returned"] == rows[0]["post"]["returned"] == TRUE),
    }


# --------------------------------------------------------------------------- #
# family A -- leg 198's adversarial negative-weight battery, re-run against the guard
# --------------------------------------------------------------------------- #
def family_adversarial(pre, post):
    """Clause (a). Leg 198's OWN cases, at leg 198's OWN configuration.

    Every magnitude leg 198 measured is re-asserted here; only the verdict flips.
    The `on_nonpositive="allow"` column is leg 135's rule in force: the repair must not
    make the escalating leg's battery unrunnable, so the pre-repair numbers must still
    be reachable THROUGH the repaired module."""
    bpre, _, zpre, hpre = converged(pre)
    bpost, _, zpost, hpost = converged(post)
    rows = []
    for lab, kw in [("w_r = -1e-6", dict(w_r=-1e-6)),
                    ("w_om = -1e-9", dict(w_om=-1e-9)),
                    ("w_l = -1 * Xmax", dict(w_l=-float(np.abs(bpre.X).max()))),
                    ("w_r = -1.0", dict(w_r=-1.0)),
                    ("w_om = -1.0", dict(w_om=-1.0)),
                    ("all three negative",
                     dict(w_l=-1.0, w_om=-1.0, w_r=-1.0)),
                    ("w_r = 0.0 (the SEMINORM case leg 198 read as rejected)",
                     dict(w_r=0.0)),
                    ("w_om = 0.0", dict(w_om=0.0)),
                    ("w_r = nan", dict(w_r=np.nan)),
                    ("w_r = +inf", dict(w_r=np.inf))]:
        vpre, epre, _, wspre = call(bpre.certificate_constants, zpre, p=0.0, **kw)
        vpost, epost, mpost, _ = call(bpost.certificate_constants, zpost, p=0.0, **kw)
        vesc, eesc, _, _ = call(bpost.certificate_constants, zpost, p=0.0,
                                on_nonpositive="allow", **kw)
        row = {"case": lab,
               "pre": (None if vpre is None else
                       {k: float(vpre[k]) for k in ("Y0", "Z1", "Z2", "A_norm")}),
               "pre_exception": epre, "pre_warnings": wspre,
               "post_exception": epost, "post_message": mpost,
               "post_rejects": bool(epost == "BorderedHLDomainError"),
               "escape_hatch_reproduces_pre": (
                   None if vpre is None or vesc is None else
                   bool(all(same_bits(vpre[k], vesc[k])
                            for k in ("Y0", "Z1", "Z2", "A_norm")))),
               "escape_hatch_exception": eesc}
        if vpre is not None:
            row["pre_negative_constants"] = sorted(
                k for k in ("Y0", "Z1", "Z2", "A_norm")
                if np.isfinite(vpre[k]) and vpre[k] < 0)
            row["pre_radii_root"] = radii_root(vpre["Y0"], vpre["Z1"], vpre["Z2"])
        rows.append(row)

    # the sign-flip differential: same magnitude, one character changed
    honest, _, _, _ = call(bpre.certificate_constants, zpre, p=0.0)
    signflip = []
    for lab, kwp, kwn in [("w_r = +/-1e-6", dict(w_r=1e-6), dict(w_r=-1e-6)),
                          ("w_om = +/-1e-9", dict(w_om=1e-9), dict(w_om=-1e-9))]:
        cp, _, _, _ = call(bpre.certificate_constants, zpre, p=0.0, **kwp)
        cn, _, _, _ = call(bpre.certificate_constants, zpre, p=0.0, **kwn)
        _, en, _, _ = call(bpost.certificate_constants, zpost, p=0.0, **kwn)
        _, ep, _, _ = call(bpost.certificate_constants, zpost, p=0.0, **kwp)
        signflip.append({
            "case": lab,
            "positive": {k: float(cp[k]) for k in ("Y0", "Z1", "Z2", "A_norm")},
            "negative": {k: float(cn[k]) for k in ("Y0", "Z1", "Z2", "A_norm")},
            "Z1_understated_x": float(cp["Z1"] / cn["Z1"]),
            "A_norm_understated_x": float(cp["A_norm"] / cn["A_norm"]),
            "radii_root_positive": radii_root(cp["Y0"], cp["Z1"], cp["Z2"]),
            "radii_root_negative": radii_root(cn["Y0"], cn["Z1"], cn["Z2"]),
            "post_rejects_negative": bool(en == "BorderedHLDomainError"),
            "post_still_accepts_positive": bool(ep is None),
        })
    return {
        "what": ("leg 198's adversarial negative-weight cases re-run against the guard, "
                 "at leg 198's own configuration (n=101, rho_max=8.0, p=0.0)"),
        "configuration": {"n": 101, "rho_max": 8.0, "p": 0.0,
                          "pre_converged": bool(hpre["converged"]),
                          "post_converged": bool(hpost["converged"]),
                          "pre_final_residual": float(hpre["residual_ladder"][-1]),
                          "post_final_residual": float(hpost["residual_ladder"][-1])},
        "honest_constants": {k: float(honest[k]) for k in ("Y0", "Z1", "Z2", "A_norm")},
        "honest_radii_root": radii_root(honest["Y0"], honest["Z1"], honest["Z2"]),
        "cases": rows,
        "n_cases": len(rows),
        "n_post_rejects": sum(r["post_rejects"] for r in rows),
        "n_pre_accepted": sum(r["pre_exception"] is None for r in rows),
        "sign_flip_differential": signflip,
        "escape_hatch_reproduces_all_pre": bool(all(
            r["escape_hatch_reproduces_pre"] in (True, None) for r in rows)),
    }


# --------------------------------------------------------------------------- #
# family B -- CLAUSE (b): the bit-identity licence
# --------------------------------------------------------------------------- #
def shipped_configurations(b):
    """Every (p, w_l, w_om, w_r) the live callers actually pass, enumerated by IMPORT.

    port_v1:322  p in {0.0, 0.2, 0.39}, w_l = f*Xmax, f in {1e-3,1e-2,1e-1,1.0}
    port_v1:358 / port_v2:100          p = 0.39, w_l = 0.01*Xmax
    l1_v1:106 / test_interval_cert:86  p = 0.39, w_l from the weight vector
    test_bordered_hl:234,261,284       p = 0.39, w_l in {Xmax, 0.01*Xmax}
    Every one of them leaves w_om = w_r = 1.0. The grid below is a SUPERSET.
    """
    Xmax = float(np.abs(b.X).max())
    cfgs = []
    for p in (0.0, 0.2, 0.39, 1.0, 2.0, -0.5):
        for f in (1e-3, 1e-2, 1e-1, 1.0):
            cfgs.append(dict(p=p, w_l=f * Xmax, w_om=1.0, w_r=1.0))
    for w_om in (1e-3, 1.0, 1e3):
        for w_r in (1e-3, 1.0, 1e3):
            cfgs.append(dict(p=0.39, w_l=0.01 * Xmax, w_om=w_om, w_r=w_r))
    cfgs.append(dict(p=0.39, w_l=None, w_om=1.0, w_r=1.0))   # the default w_l branch
    return cfgs


def snapshot(mod, n, rho_max, c):
    """Every float this module can be asked for, at one grid, on CLEAN input."""
    b, z0, z, hist = converged(mod, n=n, rho_max=rho_max, c=c)
    s = {}
    s["grid.X"] = b.X
    s["grid.rho"] = b.rho
    s["grid.i0"] = b.i0
    s["grid.N"] = b.N
    s["op.Uop_rowsums"] = b.Uop.sum(axis=1)
    s["op.Uop_trace"] = float(np.trace(b.Uop))
    s["op.H_rowsums"] = b.H.sum(axis=1)
    s["op.D_rowsums"] = b.D.sum(axis=1)
    s["op.Drow0"] = b.Drow0
    s["pin"] = np.array(b.pin)
    s["newton.ladder"] = hist["residual_ladder"]
    s["newton.lambda"] = hist["lambda"]
    s["newton.converged"] = hist["converged"]
    s["state.z"] = z
    s["F.at_z"] = b.F(z)
    s["F.at_z0"] = b.F(z0)
    s["jac.rowsums"] = b.jacobian(z).sum(axis=1)
    s["jac.colsums"] = b.jacobian(z).sum(axis=0)
    for i, v in enumerate([z * 1e-3, z0 * 0.5]):
        s[f"quad.{i}"] = b.quadratic(v)
    # the free functions
    s["velocity.rowsums"] = mod.velocity_matrix(b.X, b.i0).sum(axis=1)
    Om, V = b.unpack(z)[0], b.unpack(z)[1]
    s["tail.Omega"] = mod.tail_exponent(b.X, Om, 10.0, 100.0)
    s["tail.V"] = mod.tail_exponent(b.X, V, 10.0, 100.0)
    s["shape"] = mod.profile_shape(b.X, Om, V)
    # the weight path -- the surface the guard sits on
    for k, cfg in enumerate(shipped_configurations(b)):
        w, nu, w_l = b.weights(**cfg)
        s[f"weights.{k}.w"] = w
        s[f"weights.{k}.nu"] = nu
        s[f"weights.{k}.w_l"] = w_l
        s[f"cert.{k}"] = b.certificate_constants(z, **cfg)
    s["curve"] = b.constants_vs_weight(z, [0.0, 0.2, 0.39, 1.0],
                                       w_l=0.01 * float(np.abs(b.X).max()))
    # induced_sup_norm on the module's own matrices, both weight directions
    _, nu39, _ = b.weights(p=0.39)
    s["isn.Uop"] = mod.induced_sup_norm(b.Uop, None, nu39)
    s["isn.H"] = mod.induced_sup_norm(b.H, None, nu39)
    s["isn.D"] = mod.induced_sup_norm(b.D, nu39, nu39)
    s["isn.D_scalar_w"] = mod.induced_sup_norm(b.D, 2.0, 3.0)
    return s


def family_bit_identity(pre, post):
    """Clause (b), and it is the load-bearing one. `==` on float64 bytes, not allclose."""
    grids = [(51, 8.0, 0.5), (101, 8.0, 0.5), (101, 9.0, 0.5), (201, 8.0, 0.5),
             (401, 8.0, 0.5)]
    total = moved = 0
    per_grid, movers = [], []
    for (n, rho_max, c) in grids:
        spre = snapshot(pre, n, rho_max, c)
        spost = snapshot(post, n, rho_max, c)
        lpre, lpost = [], []
        for k in sorted(spre):
            leaves(spre[k], k, lpre)
            leaves(spost[k], k, lpost)
        assert len(lpre) == len(lpost), "leaf-count mismatch -- the snapshots disagree"
        g_moved = 0
        for (ka, va), (kb, vb) in zip(lpre, lpost):
            assert ka == kb, f"leaf-name mismatch {ka} vs {kb}"
            total += 1
            if not same_bits(va, vb):
                g_moved += 1
                if len(movers) < 40:
                    movers.append({"grid": [n, rho_max, c], "leaf": ka,
                                   "pre": float(va), "post": float(vb)})
        moved += g_moved
        per_grid.append({"n": n, "rho_max": rho_max, "c": c,
                         "leaves": len(lpre), "moved": g_moved})
    return {
        "what": ("every float64 leaf the module can be asked for, on CLEAN input, "
                 "pre- vs post-repair in the SAME process, compared with == on raw "
                 "bytes (NaN == NaN counted identical); NOT allclose"),
        "method": ("pre-repair module read out of git at %s and exec'd into this "
                   "interpreter under the name bordered_hl_pre" % PRE_REF),
        "grids": per_grid, "total_leaves": total, "leaves_moved": moved,
        "movers": movers,
        "configurations_per_grid": None,
        "bit_identical": bool(moved == 0),
    }


def family_live_callers(pre, post):
    """The caller set enumerated BY IMPORT, and the guard's firing rate on it.

    A guard that fires on a shipped configuration would move a banked number. The
    honest form of "0 banked numbers moved" is a COUNT of shipped configurations that
    reach the guard and are accepted."""
    callers = [
        {"file": "experiments/p2_route_port_v1_bordered.py", "site": "322, 358",
         "leg": 46, "note": "the banked PORT certificate"},
        {"file": "experiments/p2_route_port_v2_reach.py", "site": "100", "leg": 47},
        {"file": "experiments/p2_route_l1_v1_interval.py", "site": "106", "leg": 50},
        {"file": "experiments/p2_route_l1rh_v1_construction.py", "site": "86", "leg": 56,
         "note": "imports induced_sup_norm directly"},
        {"file": "test_bordered_hl.py", "site": "205-214, 234, 261, 284",
         "note": "the capabilities.py validated line"},
        {"file": "test_interval_certificate.py", "site": "86"},
    ]
    # the four legs the gate names, checked mechanically rather than assumed
    named = {}
    for leg, files in {
            54: ["experiments/p2_route_mm_v1_shape.py",
                 "experiments/p2_route_mm_v1_shape_evidence.py",
                 "experiments/p2_route_mm_v1_headline_verify.py"],
            58: ["experiments/p2_route_ng_v1_nogo.py",
                 "experiments/p2_route_ng_v1_nogo_evidence.py"],
            127: ["experiments/p2_route_ngx_v1_general.py",
                  "experiments/p2_route_ngx_v1_general_evidence.py"],
            192: []}.items():
        hits = []
        for f in files:
            pth = ROOT / f
            if pth.exists():
                hits.append({"file": f,
                             "mentions_bordered_hl": pth.read_text().count("bordered_hl")})
        named[str(leg)] = {
            "files_checked": len(hits), "hits": hits,
            "landed": bool(files) and all((ROOT / f).exists() for f in files),
            "calls_this_module": bool(any(h["mentions_bordered_hl"] for h in hits)),
        }
    named["192"]["landed"] = (ROOT / "experiments" / "journal" / "leg_192.md").exists()
    named["192"]["note"] = ("no journal and no runner on main -- leg 192 has not landed, "
                            "so it has no re-derivation to be bit-identical to")

    b, _, z, _ = converged(post, n=101)
    cfgs = shipped_configurations(b)
    accepted = 0
    for cfg in cfgs:
        _, e, _, _ = call(b.certificate_constants, z, **cfg)
        accepted += int(e is None)
    return {
        "what": ("the live caller set enumerated BY IMPORT, and the guard's firing rate "
                 "on the configurations they ship"),
        "live_callers": callers, "n_live_callers": len(callers),
        "legs_named_by_the_gate": named,
        "shipped_configurations_probed": len(cfgs),
        "shipped_configurations_accepted": accepted,
        "guard_fires_on_shipped": len(cfgs) - accepted,
    }


# --------------------------------------------------------------------------- #
# the lesson-90 control
# --------------------------------------------------------------------------- #
def control_distinguishable(pre, post):
    """The run is VOID unless the two module objects behave DIFFERENTLY where they must.

    Declared in writeup/novelty/leg_218.md before the run. Without it, "0 leaves moved"
    is a statement about having loaded the same file twice."""
    bpre, _, zpre, _ = converged(pre)
    bpost, _, zpost, _ = converged(post)
    vpre, epre, _, _ = call(bpre.certificate_constants, zpre, p=0.0, w_r=-1e-6)
    vpost, epost, _, _ = call(bpost.certificate_constants, zpost, p=0.0, w_r=-1e-6)
    ok = bool(epre is None and vpre is not None and vpre["Z1"] > 0
              and epost == "BorderedHLDomainError")
    return {
        "what": ("pre-repair must ACCEPT w_r = -1e-6 where post-repair REFUSES; the "
                 "differential is void otherwise"),
        "pre_accepts": bool(epre is None),
        "pre_Z1": None if vpre is None else float(vpre["Z1"]),
        "pre_A_norm": None if vpre is None else float(vpre["A_norm"]),
        "pre_Z2": None if vpre is None else float(vpre["Z2"]),
        "post_exception": epost,
        "modules_distinguishable": ok,
    }


# --------------------------------------------------------------------------- #
def main():
    t0 = time.time()
    pre, prov = load_pre_repair()
    post = sys.modules["solver.bordered_hl"]

    assert prov["blob_identical"], (
        "origin/main's blob is NOT byte-identical to %s -- the pre-repair pin is not "
        "stable and the differential would compare the wrong thing" % PRE_REF)

    ctl = control_distinguishable(pre, post)
    assert ctl["modules_distinguishable"], (
        "LESSON-90 CONTROL FAILED: the pre- and post-repair modules are not "
        "distinguishable; the differential is void. %r" % ctl)
    print("  control: modules distinguishable (pre accepts w_r=-1e-6 at Z1=%.6e, "
          "post raises %s)" % (ctl["pre_Z1"], ctl["post_exception"]), flush=True)

    print("  family P -- the predicate", flush=True)
    P = family_predicate(pre, post)
    print("  family A -- clause (a), leg 198's negative-weight battery", flush=True)
    A = family_adversarial(pre, post)
    print("  family C -- the live caller set", flush=True)
    C = family_live_callers(pre, post)
    print("  family B -- clause (b), the bit-identity differential", flush=True)
    B = family_bit_identity(pre, post)

    clause_a = bool(A["n_post_rejects"] == A["n_cases"]
                    and P["n_post_rejects"] == P["n_pre_silent_wrong"] + sum(
                        1 for r in P["cases"] if r["case"] != "positive (control)"
                        and not r["pre_silent_wrong"])
                    and P["control_positive_unchanged"])
    clause_a = bool(A["n_post_rejects"] == A["n_cases"] and P["control_positive_unchanged"]
                    and all(r["post_rejects"] for r in P["cases"]
                            if r["case"] != "positive (control)"))
    clause_b = bool(B["bit_identical"] and C["guard_fires_on_shipped"] == 0)

    out = {
        "leg": 218, "route": "BHR", "role": "LEG (repair family, 150-154 precedent)",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_s": round(time.time() - t0, 1),
        "module_under_repair": MODULE_PATH,
        "repairs": "leg 198 BHA-1 (the border-weight guard) ONLY",
        "residues_not_patched": [
            "BHA-2 velocity_matrix accepts a permuted grid (896675x)",
            "BHA-3 BorderedHL(pin=) truncates a mis-arity pin",
            "BHA-4 tail_exponent silently drops NaN samples (5.358e-13)"],
        "gate": ("Does adding a border-weight non-negativity guard (per leg 198's own "
                 "identified mechanism) cause every one of leg 198's adversarial "
                 "negative-weight cases to now reject, while every live caller across "
                 "54/58/127/192's own re-derivation stays bit-identical to its "
                 "pre-repair banked value?"),
        "provenance": prov,
        "lesson90_control": ctl,
        "adopted_predicate": "np.all(np.isfinite(w) & (w > 0)), confirm-good polarity",
        "predicate_note": (
            "the gate's own word 'non-negativity' (any(w<0)) is the WEAKEST of the three "
            "candidates and admits w=0 (a seminorm), NaN and +inf; family P measures all "
            "three on the same inputs"),
        "P_predicate": P,
        "A_clause_a_adversarial": A,
        "C_live_callers": C,
        "B_clause_b_bit_identity": B,
        "clause_a_every_adversarial_case_rejects": clause_a,
        "clause_b_every_live_caller_bit_identical": clause_b,
        "gate_answer": "YES" if (clause_a and clause_b) else "NO",
        "banked_numbers_impeached": 0,
        "banked_numbers_moved": 0 if clause_b else None,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=False, default=str))

    print()
    print("  predicate    : %d/%d pre-repair silent-wrong cases, %d/%d post-repair rejects"
          % (P["n_pre_silent_wrong"], len(P["cases"]) - 1,
             P["n_post_rejects"], len(P["cases"]) - 1))
    print("  clause (a)   : %d/%d adversarial cases rejected (pre-repair accepted %d)"
          % (A["n_post_rejects"], A["n_cases"], A["n_pre_accepted"]))
    print("  clause (b)   : %d/%d clean leaves bit-identical, %d moved"
          % (B["total_leaves"] - B["leaves_moved"], B["total_leaves"], B["leaves_moved"]))
    print("  guard fires on %d of %d shipped configurations"
          % (C["guard_fires_on_shipped"], C["shipped_configurations_probed"]))
    print("  GATE: %s   ->  %s" % (out["gate_answer"], OUT))
    return 0 if out["gate_answer"] == "YES" else 1


if __name__ == "__main__":
    sys.exit(main())
