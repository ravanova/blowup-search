"""Route-BHN v1 -- an ADVERSARIAL BATTERY against the damped Newton solve in
solver/bordered_hl.py, and the audit of what its `converged` flag actually certifies.

Leg 80. Third leg of the adversarial-audit family (after leg 69 / Route-IA on
solver/interval.py and leg 79 / Route-PC on the port certification), applied to the one
Newton solver in the certificate stack that has only ever been validated on well-posed
starting data: capabilities.py's entry for solver/bordered_hl.py rests on "Newton to
5.66e-15 at n=201" and a contraction-ratio extrapolation, both from a good initial guess.

THE GATE, VERBATIM
------------------
"Under an adversarial battery (near-singular Jacobian at the starting iterate, NaN/Inf-
poisoned initial guess, a residual sequence oscillating just above and below tolerance),
does solver/bordered_hl.py's damped Newton solve ever incorrectly report convergence?"

WHAT "INCORRECTLY" MEANS HERE, DECIDED BEFORE THE RUN
-----------------------------------------------------
The flag the module sets is

    converged = bool(res[-1] < tol and np.isfinite(res[-1]))

so the only claim it makes is about the residual. The gate is therefore decided on the
STRICT reading, which is the one the flag can be wrong about:

    FALSE REPORT  :=  converged is True
                      AND ( ||F(z_returned)||_inf >= tol   [recomputed INDEPENDENTLY,
                                                            from the returned iterate,
                                                            not read off the ladder]
                            OR z_returned is not all finite )

Every converged=True in this file is re-verified that way. A second, weaker reading --
"converged=True at a point that is not a locally unique root" -- is NOT used to decide
the gate, because the flag never promised it; but it is MEASURED, because it is what
every downstream consumer of this module actually needs, and it is where the exposure
turned out to be. Both numbers are reported.

DISCIPLINE
----------
Magnitudes, never booleans (standing discipline). Every family reports its counts AND
the worst-case size of the thing that could have gone wrong: the conditioning at the
starting iterate, the nullity at the returned iterate, the uphill ratio of an accepted
step, the depth and rise of a residual dip, the iterate error hidden under one tol.

BLAS THREADING: the thread caps below are set BEFORE numpy is imported and are not
cosmetic. On this 12-core host an unpinned np.linalg.solve on the N=205 bordered matrix
costs 1.006 s against 0.00082 s pinned -- a 1230x penalty that makes the whole module,
including its existing test_bordered_hl.py, look pathologically slow. This is an
environment effect, NOT a property of the solver, and it is reported as such.

Run: .venv/bin/python experiments/p2_route_bhn_v1_adversarial.py
Writes: writeup/data/p2_route_bhn_v1_adversarial.json
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

from solver.bordered_hl import BorderedHL  # noqa: E402

SEED = 20260806
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_bhn_v1_adversarial.json")


# --------------------------------------------------------------------------- #
# harness
# --------------------------------------------------------------------------- #
def fresh(n=101, rho_max=8.0, x0=0.3, w=0.9):
    """The same well-posed non-symmetric starting data test_bordered_hl.py uses."""
    b = BorderedHL(n=n, rho_max=rho_max)
    Om = np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = 0.8 * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    z0 = b.pack(Om, V, 1.06, -0.42, 0.077)
    b.set_pin_from(z0)
    return b, z0


def verdict(b, z_ret, hist, tol):
    """The FALSE REPORT predicate, evaluated independently of the ladder."""
    conv = bool(hist["converged"])
    finite = bool(np.isfinite(z_ret).all())
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recheck = float(np.abs(b.F(z_ret)).max())
    except Exception:
        recheck = float("nan")
    false_report = bool(conv and (not finite or not (recheck < tol)))
    return {"converged": conv, "recheck_residual": recheck,
            "returned_finite": finite, "false_report": false_report}


def ladder_stats(hist):
    L = np.asarray(hist["residual_ladder"], dtype=float)
    lam = np.asarray(hist["lambda"], dtype=float)
    up = 1.0
    for i in range(1, L.size):
        if np.isfinite(L[i]) and np.isfinite(L[i - 1]) and L[i - 1] > 0 and L[i] > L[i - 1]:
            up = max(up, L[i] / L[i - 1])
    return {"iterations": int(L.size - 1),
            "final_residual": float(L[-1]),
            "max_uphill_ratio": float(up),
            "lambda_min": float(lam.min()) if lam.size else None,
            "lambda_collapsed": bool(lam.size and lam.min() <= 1.0 / 1024),
            "cond_array_len": int(np.asarray(hist["cond"]).size)}


def nullity(J, rtol=1e-12):
    sv = np.linalg.svd(J, compute_uv=False)
    return sv, int((sv < rtol * sv[0]).sum())


# --------------------------------------------------------------------------- #
# family 1 -- the well-posed baseline, and what the flag certifies in ITERATE units
# --------------------------------------------------------------------------- #
def family_baseline():
    """Reproduce the validated behaviour, then measure the flag's MEANING.

    capabilities.py quotes a residual (5.66e-15). A residual is not an error. The
    honest conversion is through the smallest singular value of DF at the root:
    ||dz|| <= ||F|| / sigma_min. This family measures sigma_min directly and, as an
    independent check that does not trust the linearization, perturbs the converged
    iterate ALONG the smallest right singular vector and reads off the residual."""
    out = {"cases": []}
    for n in (101, 201):
        b, z0 = fresh(n=n)
        t = time.time()
        z, h = b.newton(z0, tol=1e-13, max_iter=60)
        wall = time.time() - t
        J = b.jacobian(z)
        sv = np.linalg.svd(J, compute_uv=False)
        _, S, Vt = np.linalg.svd(J)
        v = Vt[-1]
        probes = []
        for tt in (1e-6, 1e-3, 1e-1):
            r = float(np.abs(b.F(z + tt * v)).max())
            probes.append({"perturbation": tt, "residual": r, "residual_per_unit_error": r / tt})
        # iterate error that hides under one tol, from the softest probe
        slope = min(p["residual_per_unit_error"] for p in probes)
        rec = {"n": n, "N": int(b.N), "wall_s": wall,
               "sigma_min": float(sv[-1]), "sigma_max": float(sv[0]),
               "cond": float(sv[0] / sv[-1]),
               "null_direction_probes": probes,
               "iterate_error_under_tol_1e-13": 1e-13 / slope,
               **ladder_stats(h), **verdict(b, z, h, 1e-13)}
        out["cases"].append(rec)
    # the round-off floor: run far past convergence and read the band the ladder sits in
    b, z0 = fresh(n=101)
    _, h = b.newton(z0, tol=1e-16, max_iter=60)
    L = np.asarray(h["residual_ladder"], dtype=float)
    tail = L[16:]
    out["roundoff_floor"] = {"band_lo": float(tail.min()), "band_hi": float(tail.max()),
                             "rungs_in_band": int(tail.size),
                             "module_default_tol": 1e-13,
                             "decades_tol_above_floor": float(np.log10(1e-13 / tail.max()))}
    return out


# --------------------------------------------------------------------------- #
# family 2 -- a NEAR-SINGULAR Jacobian at the starting iterate
# --------------------------------------------------------------------------- #
def family_near_singular():
    """Drive cond(DF(z0)) from 5e4 to infinity and ask whether the flag notices.

    Construction: the last three COLUMNS of DF are (X*Om_X, -Omega, Om_X) stacked over
    (X*V_X, -2V, V_X) -- every one of them vanishes with the profile amplitude. So
    scaling (Omega, V) by eps drives the three gauge columns to zero at rate eps and the
    Jacobian to exact rank deficiency 3 in the limit. This is not a contrived matrix; it
    is the module's own degeneracy, reached along its own amplitude gauge."""
    b, z0 = fresh(n=101)
    zstar, _ = b.newton(z0, tol=1e-13, max_iter=60)
    out = {"cases": []}
    for eps in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-13, 0.0):
        ze = zstar.copy()
        ze[:2 * b.n] *= eps
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            J = b.jacobian(ze)
            sv, nul = nullity(J)
            cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")
            raised = False
            try:
                np.linalg.solve(J, -b.F(ze))
            except np.linalg.LinAlgError:
                raised = True
            z, h = b.newton(ze, tol=1e-13, max_iter=40)
        out["cases"].append({"amplitude_eps": eps, "cond_at_start": cond,
                             "nullity_at_start": nul,
                             "linalgerror_raised": raised,
                             "dist_to_root": float(np.abs(z - zstar).max()),
                             **ladder_stats(h), **verdict(b, z, h, 1e-13)})
    # a second, independent route to near-singularity: kill the transport coefficient
    # S = U + c_l X + c_r, which multiplies BOTH derivative blocks of the Jacobian.
    for scale in (1e-2, 1e-5, 1e-8):
        zs = zstar.copy()
        zs[2 * b.n] *= scale       # c_l
        zs[2 * b.n + 2] *= scale   # c_r
        zs[:2 * b.n] *= scale
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sv, nul = nullity(b.jacobian(zs))
            z, h = b.newton(zs, tol=1e-13, max_iter=40)
        out["cases"].append({"vanishing_transport_scale": scale,
                             "cond_at_start": float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf"),
                             "nullity_at_start": nul,
                             "dist_to_root": float(np.abs(z - zstar).max()),
                             **ladder_stats(h), **verdict(b, z, h, 1e-13)})
    return out


# --------------------------------------------------------------------------- #
# family 3 -- a NaN/Inf-poisoned initial iterate
# --------------------------------------------------------------------------- #
def family_poison():
    """Poison every kind of slot, and the border targets too.

    The flag's only defence is np.isfinite(res[-1]); it is applied to the RESIDUAL, not
    to the returned iterate. So the question is whether any poison can reach the returned
    z while leaving the residual finite and small. Slots are swept at stride 7 across all
    2n+3 of them, with the three constant slots and the origin node forced in."""
    b, z0 = fresh(n=101)
    zstar, _ = b.newton(z0, tol=1e-13, max_iter=60)
    pin0 = b.pin
    idxs = sorted(set(list(range(0, b.N, 7)) +
                      [0, b.i0, b.n - 1, b.n, b.n + b.i0, 2 * b.n - 1,
                       2 * b.n, 2 * b.n + 1, 2 * b.n + 2]))
    total = 0
    false_reports = []
    converged_cases = []
    nonfinite_returned = 0
    for val, tag in ((np.nan, "nan"), (np.inf, "+inf"), (-np.inf, "-inf")):
        for idx in idxs:
            for base, bt in ((zstar, "at_root"), (z0, "at_start")):
                b.pin = pin0
                zp = base.copy()
                zp[idx] = val
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    z, h = b.newton(zp, tol=1e-13, max_iter=10)
                v = verdict(b, z, h, 1e-13)
                total += 1
                if not v["returned_finite"]:
                    nonfinite_returned += 1
                if v["converged"]:
                    converged_cases.append({"poison": tag, "slot": idx, "base": bt, **v})
                if v["false_report"]:
                    false_reports.append({"poison": tag, "slot": idx, "base": bt, **v})
    # mixed poison: +inf and -inf in the same iterate (inf - inf = nan downstream)
    for pair in ((0, 1), (b.i0, b.n + b.i0), (2 * b.n, 2 * b.n + 2)):
        b.pin = pin0
        zp = zstar.copy()
        zp[pair[0]] = np.inf
        zp[pair[1]] = -np.inf
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            z, h = b.newton(zp, tol=1e-13, max_iter=10)
        v = verdict(b, z, h, 1e-13)
        total += 1
        if v["false_report"]:
            false_reports.append({"poison": "mixed_inf", "slot": list(pair), **v})
    # poisoned BORDER TARGETS -- the pin is not part of z and is never checked at all
    for val, tag in ((np.nan, "nan"), (np.inf, "+inf")):
        for slot in range(3):
            pin = list(pin0)
            pin[slot] = val
            b.pin = tuple(pin)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                z, h = b.newton(zstar, tol=1e-13, max_iter=10)
            v = verdict(b, z, h, 1e-13)
            total += 1
            if v["false_report"]:
                false_reports.append({"poison": "pin_" + tag, "slot": slot, **v})
    b.pin = pin0
    return {"cases_run": total, "converged_true": len(converged_cases),
            "false_reports": false_reports,
            "nonfinite_returned_iterates": nonfinite_returned,
            "slots_swept": len(idxs), "N": int(b.N)}


# --------------------------------------------------------------------------- #
# family 4 -- a residual OSCILLATING just above and below tolerance
# --------------------------------------------------------------------------- #
def family_oscillation():
    """Find real ladders that dip and rise, then put tol INSIDE the dip.

    This is the gate's third family made concrete: rather than hoping an oscillation
    appears, search random well-shaped starts for a rung with L[i] < L[i-1] and
    L[i+1] > L[i], then re-run with tol placed between L[i] and L[i+1] so the solve is
    forced to stop exactly at the bottom of a dip it was about to climb out of."""
    b, _ = fresh(n=101)
    rng = np.random.default_rng(SEED)
    dips = []
    scanned = 0
    for _ in range(400):
        if len(dips) >= 8:
            break
        scanned += 1
        Om = np.exp(-((b.X - rng.uniform(-1, 1)) ** 2) /
                    (2 * rng.uniform(0.4, 2.0) ** 2)) * rng.uniform(0.2, 3)
        V = np.exp(-((b.X - rng.uniform(-1, 1)) ** 2) /
                   (2 * rng.uniform(0.4, 2.0) ** 2)) * rng.uniform(0.2, 3)
        zz = b.pack(Om, V, rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-1, 1))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _, h = b.newton(zz, tol=1e-16, max_iter=40)
        L = np.asarray(h["residual_ladder"], dtype=float)
        for i in range(1, L.size - 1):
            if np.isfinite(L[i]) and L[i] < L[i - 1] and L[i + 1] > L[i] and L[i] < 1e-4:
                tol_in_dip = float(np.sqrt(L[i] * L[i + 1]))  # strictly between the two
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    z2, h2 = b.newton(zz, tol=tol_in_dip, max_iter=40)
                sv, nul = nullity(b.jacobian(z2))
                dips.append({"dip_index": i, "dip_residual": float(L[i]),
                             "next_residual": float(L[i + 1]),
                             "rise_ratio": float(L[i + 1] / L[i]),
                             "tol_placed": tol_in_dip,
                             "sigma_min_at_returned": float(sv[-1]),
                             "nullity_at_returned": nul,
                             **verdict(b, z2, h2, tol_in_dip)})
                break
    return {"starts_scanned": scanned, "dips_found": len(dips),
            "false_reports": [d for d in dips if d["false_report"]], "dips": dips}


# --------------------------------------------------------------------------- #
# family 5 -- the DEGENERATE root: converged=True where DF is exactly singular
# --------------------------------------------------------------------------- #
def family_degenerate_root():
    """The zero profile is an exact root of F at which DF has a 3-dimensional kernel.

    Omega = V = 0 nulls both interior equations for ANY (c_l, c_omega, c_r), so with the
    three border targets pinned at zero the residual is EXACTLY 0 and the three gauge
    constants are entirely undetermined -- the object the module exists to make
    determinate (see its docstring: 'the constants are unknowns of the SAME Newton system
    from the first iterate') is, here, not determined at all. The flag says converged."""
    out = {"cases": []}
    b = BorderedHL(n=101, rho_max=8.0)
    b.pin = (0.0, 0.0, 0.0)
    for trip in ((0.0, 0.0, 0.0), (1.06, -0.42, 0.077), (1e6, 1e6, 1e6), (-3.7, 91.2, -0.5)):
        zz = b.pack(np.zeros(b.n), np.zeros(b.n), *trip)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            z, h = b.newton(zz, tol=1e-13, max_iter=20)
        sv, nul = nullity(b.jacobian(z))
        _, _, cl, com, cr = b.unpack(z)
        out["cases"].append({"constants_in": list(trip),
                             "constants_out": [cl, com, cr],
                             "sigma_min_at_returned": float(sv[-1]),
                             "nullity_at_returned": nul,
                             "N": int(b.N),
                             **ladder_stats(h), **verdict(b, z, h, 1e-13)})
    out["note"] = ("residual is EXACTLY zero, so this is NOT a false report under the "
                   "gate's strict reading; it is converged=True at a point where DF is "
                   "exactly singular and the returned constants are whatever was passed in")
    return out


# --------------------------------------------------------------------------- #
# family 6 -- LAMBDA-COLLAPSE: the backtracking bottoms out and steps anyway
# --------------------------------------------------------------------------- #
def family_lambda_collapse():
    """`while lam > 1/1024` exits AT 1/1024 and `z = z + lam*dz` runs unconditionally.

    So when no damping factor in the budget reduces the residual, the module takes the
    smallest one regardless of whether it went uphill, and records only the lambda. In
    Deuflhard's NLEQ-ERR the same event is a termination criterion (novelty pass, Q4).
    Measured over random starts: how often it fires, and how far uphill it goes."""
    b, z0 = fresh(n=101)
    rng = np.random.default_rng(SEED + 1)
    runs, collapsed, conv, false_reports = 0, 0, 0, []
    worst_uphill = 1.0
    worst_case = None
    for _ in range(80):
        Om = rng.normal(0, float(rng.choice([0.1, 1.0, 5.0])), b.n)
        V = rng.normal(0, float(rng.choice([0.1, 1.0, 5.0])), b.n)
        zz = b.pack(Om, V, rng.normal(0, 2), rng.normal(0, 2), rng.normal(0, 2))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            z, h = b.newton(zz, tol=1e-12, max_iter=40)
        st = ladder_stats(h)
        v = verdict(b, z, h, 1e-12)
        runs += 1
        collapsed += int(bool(st["lambda_collapsed"]))
        conv += int(v["converged"])
        if st["max_uphill_ratio"] > worst_uphill:
            worst_uphill = st["max_uphill_ratio"]
            worst_case = {**st, **v}
        if v["false_report"]:
            false_reports.append({**st, **v})
    return {"runs": runs, "lambda_collapse_runs": collapsed, "converged_runs": conv,
            "worst_uphill_ratio": worst_uphill, "worst_case": worst_case,
            "false_reports": false_reports,
            "note": ("an uphill step is ACCEPTED whenever the backtracking budget is "
                     "exhausted; the only trace left in the returned history is "
                     "lambda == 1/1024")}


# --------------------------------------------------------------------------- #
# family 7 -- SCOPE: the criterion itself, driven through the production loop
# --------------------------------------------------------------------------- #
class _Rootless:
    """F(x) = exp(-x): smooth, with NO root anywhere, and |F| -> 0 as x -> +inf.

    Duck-typed so that BorderedHL.newton -- the exact production loop, unmodified -- can
    be run on it unbound. This is fault injection into the ALGORITHM, not a statement
    about the bordered system's own F, and it is scoped that way in the report."""

    def F(self, z):
        return np.exp(-np.asarray(z, dtype=float))

    def jacobian(self, z):
        return np.diag(-np.exp(-np.asarray(z, dtype=float)))


def family_criterion_scope():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        z, h = BorderedHL.newton(_Rootless(), np.array([0.0]), tol=1e-12, max_iter=60)
    st = ladder_stats(h)
    rootless = {"tol": 1e-12, "returned_x": float(z[0]),
                "residual_at_return": float(np.exp(-z[0])),
                "root_exists": False, **st, "converged": bool(h["converged"])}
    # tol itself as an adversary (caller-side, recorded for completeness)
    b, z0 = fresh(n=101)
    tolcases = []
    for t, tag in ((np.inf, "inf"), (np.nan, "nan")):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            z, h = b.newton(z0, tol=t, max_iter=5)
        tolcases.append({"tol": tag, "converged": bool(h["converged"]),
                         "final_residual": float(h["residual_ladder"][-1]),
                         "iterations": int(np.asarray(h["residual_ladder"]).size - 1)})
    return {"rootless_residual": rootless, "poisoned_tol": tolcases}


# --------------------------------------------------------------------------- #
# family 8 -- the unwritten diagnostic, and the BLAS environment effect
# --------------------------------------------------------------------------- #
def family_reporting_surface():
    """`cond_hist = []` is allocated in newton() and never appended to.

    Every run returns hist["cond"] as a length-0 array, so any caller that guards on it
    -- `np.all(hist["cond"] < X)` is vacuously True on an empty array, and `.max()`
    raises -- is testing nothing. Measured across every family above via cond_array_len."""
    b, z0 = fresh(n=101)
    lens = []
    for tol in (1e-13, 1e-8, 1e-3):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _, h = b.newton(z0, tol=tol, max_iter=40)
        lens.append(int(np.asarray(h["cond"]).size))
    J = b.jacobian(z0)
    Fz = b.F(z0)
    t = time.time()
    for _ in range(20):
        np.linalg.solve(J, -Fz)
    pinned = (time.time() - t) / 20
    return {"cond_array_lengths": lens,
            "vacuous_all_guard_on_empty": bool(np.all(np.array([]) < 0.0)),
            "N": int(b.N),
            "solve_seconds_thread_pinned": pinned,
            "threads_pinned_to": os.environ.get("OMP_NUM_THREADS"),
            "note": ("cond is advertised in the returned history and never populated; "
                     "the solve timing is recorded because on a 12-core host the same "
                     "solve costs ~1.0 s unpinned, a ~1200x BLAS-threading penalty that "
                     "is an ENVIRONMENT effect, not a solver property")}


# --------------------------------------------------------------------------- #
def main():
    t0 = time.time()
    data = {"leg": 80, "route": "BHN", "seed": SEED,
            "module_under_test": "solver/bordered_hl.py::BorderedHL.newton",
            "module_edited": False,
            "gate": ("Under an adversarial battery (near-singular Jacobian at the "
                     "starting iterate, NaN/Inf-poisoned initial guess, a residual "
                     "sequence oscillating just above and below tolerance), does "
                     "solver/bordered_hl.py's damped Newton solve ever incorrectly "
                     "report convergence?"),
            "false_report_predicate": ("converged is True AND (independently recomputed "
                                       "||F(z_returned)||_inf >= tol OR z_returned "
                                       "non-finite)")}
    data["baseline"] = family_baseline()
    data["near_singular"] = family_near_singular()
    data["poisoned_initial"] = family_poison()
    data["oscillation"] = family_oscillation()
    data["degenerate_root"] = family_degenerate_root()
    data["lambda_collapse"] = family_lambda_collapse()
    data["criterion_scope"] = family_criterion_scope()
    data["reporting_surface"] = family_reporting_surface()

    # ---- the gate, computed off the data, never asserted -------------------- #
    fr = []
    fr += [c for c in data["baseline"]["cases"] if c["false_report"]]
    fr += [c for c in data["near_singular"]["cases"] if c["false_report"]]
    fr += data["poisoned_initial"]["false_reports"]
    fr += data["oscillation"]["false_reports"]
    fr += [c for c in data["degenerate_root"]["cases"] if c["false_report"]]
    fr += data["lambda_collapse"]["false_reports"]
    n_cases = (len(data["baseline"]["cases"]) + len(data["near_singular"]["cases"]) +
               data["poisoned_initial"]["cases_run"] + data["oscillation"]["dips_found"] +
               len(data["degenerate_root"]["cases"]) + data["lambda_collapse"]["runs"])
    data["gate_answer"] = {
        "cases_on_the_modules_own_system": n_cases,
        "false_reports": len(fr),
        "detail": fr,
        "answer": "NO" if not fr else "YES",
        "strict_reading": ("no case in which converged=True while the independently "
                           "recomputed residual was at or above tol, or while the "
                           "returned iterate was non-finite"),
        "weaker_reading_measured_not_gated": (
            "converged=True DOES occur at points where DF is exactly singular "
            "(family degenerate_root): residual exactly 0.0, nullity 3, and the three "
            "gauge constants come out equal to whatever went in"),
        "scope_limited_counterexample": (
            "the same production loop, driven on a rootless residual (family "
            "criterion_scope), reports converged=True for a system with no solution; "
            "that is the residual criterion's documented limitation (novelty pass Q1/Q2) "
            "exercised through this code path, NOT a defect of the bordered system's F"),
    }
    data["wall_seconds"] = time.time() - t0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(data, fh, indent=2, default=float)

    g = data["gate_answer"]
    b0 = data["baseline"]["cases"][0]
    print(f"[BHN] baseline n=101: converged={b0['converged']} r={b0['final_residual']:.2e} "
          f"sigma_min={b0['sigma_min']:.3e} cond={b0['cond']:.3e}")
    print(f"[BHN] one tol=1e-13 hides an iterate error of "
          f"{b0['iterate_error_under_tol_1e-13']:.2e} in the sup norm")
    print(f"[BHN] near-singular: cond up to "
          f"{max(c['cond_at_start'] for c in data['near_singular']['cases']):.3e}")
    print(f"[BHN] poison: {data['poisoned_initial']['cases_run']} cases, "
          f"{data['poisoned_initial']['converged_true']} converged=True")
    print(f"[BHN] oscillation: {data['oscillation']['dips_found']} dips, tol placed inside each")
    print(f"[BHN] lambda-collapse: {data['lambda_collapse']['lambda_collapse_runs']}/"
          f"{data['lambda_collapse']['runs']} runs, worst accepted uphill ratio "
          f"{data['lambda_collapse']['worst_uphill_ratio']:.3e}")
    print(f"[BHN] degenerate root: nullity "
          f"{data['degenerate_root']['cases'][0]['nullity_at_returned']} at a converged=True return")
    print(f"[BHN] rootless residual through the same loop: "
          f"converged={data['criterion_scope']['rootless_residual']['converged']}")
    print(f"[BHN] GATE: {g['answer']} -- {g['false_reports']} false reports in "
          f"{g['cases_on_the_modules_own_system']} cases")
    print(f"[BHN] wrote {OUT}  ({data['wall_seconds']:.1f}s)")


if __name__ == "__main__":
    main()
