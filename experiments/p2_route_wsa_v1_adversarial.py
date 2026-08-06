"""Leg 97 (Route-WSA) -- the adversarial battery against `FitnessEngine`'s shared inverse.

THE QUESTION (the leg's gate, verbatim):

    Under an adversarial battery (a batch member driving the shared Jacobian toward
    near-singularity, NaN-poisoned weight parameters), does FitnessEngine ever silently
    return a finite, plausible-looking fitness value instead of propagating or flagging
    the ill-conditioning?

WHAT THIS IS NOT.  It is not a re-scoring of the six-property gate, not a GA run, not a
search, not a statement about whether the fitness is scientifically viable.  Stage B's /
leg 49's / leg 59's gate verdicts are frozen and are not touched here.  The plan-of-record
ban on "GA compute on an unvalidated fitness" is respected literally: nothing in this file
optimises anything.  `solver/weight_search.py` is READ-ONLY under this leg.

THE SHORTCUT UNDER AUDIT.  `FitnessEngine.__init__` computes `J = jacobian(z)`,
`A = inv(J)`, `absM = |I - A J|`, `aAF = |A F(z)|` ONCE and reuses them for every weight in
the batch.  Two inputs are never re-validated: the state `z` (which fixes the conditioning
of `A` for the whole batch at once) and the genome `theta` (which enters every reciprocal
and every max in the batch).

THE PRE-COMMITTED CORRUPTION CRITERION (fixed before the run; see `SILENT_DECADES`).
A case counts as SILENT CORRUPTION when the engine returns a FINITE fitness and either

  (a) a higher-precision recomputation of the SAME constants says the certificate should
      not have been reported at all (reference `Z_1 >= 1` while float64 said `Z_1 < 1`), or
  (b) the reported fitness is better (smaller) than the higher-precision fitness by more
      than SILENT_DECADES = 0.5 decades -- i.e. the shortcut flatters the weight, or
  (c) the number returned belongs to a weight OTHER than the genome asked for (the
      `LOG_NU_CLIP` substitution) while the genome is inside the box.

Reporting the ill-conditioning by returning `+inf`, or by raising `LinAlgError`, both count
as FLAGGED, not silent.  Magnitudes are reported for every rung either way.

THE HIGHER-PRECISION REFERENCE is the same device `weight_search._F_longdouble` already
uses: the identical float64 `A` and `J` (both exactly representable) are re-multiplied in
`np.longdouble` (64-bit mantissa, ~3 extra decimal digits).  Gate A4 goes further and
recomputes the defect in EXACT rational arithmetic (`fractions.Fraction`, no rounding at
all) on a small grid, so the longdouble reference is itself known-answer checked.

Run:  python experiments/p2_route_wsa_v1_adversarial.py
Writes: writeup/data/p2_route_wsa_v1_adversarial.json
"""
from __future__ import annotations

import json
import os
import sys
import time
import warnings
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.weight_search import (  # noqa: E402
    BOX_LOWER, BOX_UPPER, LOG_NU_CLIP, BorderedCLM, FitnessEngine, hand_weights, in_box,
)

# ---- pre-committed constants ------------------------------------------------------
SILENT_DECADES = 0.5      # how much the shortcut may flatter a weight before it is corruption
N_GRID = 101              # the audit grid (fast; gate A2's ladder is resolution-independent
                          # in the only thing it claims -- the ORDER of the Z_1 crossing)
N_EXACT = 41              # the grid the exact-rational known-answer check runs on
TUNED = np.array([0.0, 0.0, 0.0, 0.0, -2.0])          # leg 46's hand weight, the control
NAIVE = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
PROBE_THETAS = np.array([
    NAIVE, TUNED,
    [1.0, 1.0, -1.0, -1.0, -2.0],
    [-2.0, 0.5, 1.0, 2.0, -3.0],
    [0.5, 2.0, 0.0, -1.0, -1.0],
    [-1.0, -2.0, 0.5, 1.5, -4.0],
])
POISONS = {"nan": np.nan, "+inf": np.inf, "-inf": -np.inf}
GENE_NAMES = ("p", "log10_L", "q", "log10_l", "log10_w_l_over_Xmax")


# ---- the higher-precision references ----------------------------------------------
def reference_constants(engine, problem, theta):
    """(Y0, Z1, Z2) for the engine's OWN A and J, recomputed in np.longdouble.

    Nothing here is a different algorithm -- it is `certificate_constants`' formula at
    higher precision on bit-identical inputs, so any disagreement is the float64 batch
    path's own rounding and nothing else."""
    Al = np.asarray(engine.A, dtype=np.longdouble)
    Jl = np.asarray(engine.J, dtype=np.longdouble)
    w, nu = problem.weight_vector(np.asarray(theta, dtype=float))
    wl = np.asarray(w, dtype=np.longdouble)
    nul = np.asarray(nu, dtype=np.longdouble)
    Fl = np.asarray(problem.F(engine.z), dtype=np.longdouble)
    Ml = np.abs(np.eye(problem.N, dtype=np.longdouble) - Al @ Jl)
    Y0 = float(np.max(wl * np.abs(Al @ Fl)))
    Z1 = float(np.max(wl * (Ml @ (1.0 / wl))))
    A_norm = float(np.max(wl * (np.abs(Al) @ (1.0 / wl))))
    H_ni = float(np.max(np.abs(np.asarray(problem.H, dtype=np.longdouble)) @ (1.0 / nul)))
    XD_nn = float(np.max(nul * (np.abs(np.asarray(problem.XD, dtype=np.longdouble))
                                @ (1.0 / nul))))
    B = H_ni + 1.0 / float(w[problem.n + 1]) + XD_nn / float(w[problem.n])
    return Y0, Z1, 2.0 * A_norm * B


def fitness_from(Y0, Z1, Z2):
    """The module's own fitness formula, applied to reference constants."""
    if not (np.isfinite(Y0) and np.isfinite(Z1) and np.isfinite(Z2)):
        return float("inf")
    if Z1 >= 1.0 or Z2 <= 0.0 or Y0 <= 0.0:
        return float("inf")
    bud = (1.0 - Z1) ** 2 / (2.0 * Z2)
    return float(np.log10(Y0 / bud)) if bud > 0 else float("inf")


def exact_constants(engine, problem, theta):
    """Y0 and Z1 in EXACT rational arithmetic -- no rounding anywhere.

    float64 values are exactly rational, so `Fraction(x)` is lossless and the defect
    I - A J is evaluated with no cancellation error at all.  O(N^3) Fraction products, so
    this runs on the small grid only; it is the known-answer check that licenses the
    longdouble reference used everywhere else."""
    N = problem.N
    A = [[Fraction(x) for x in row] for row in engine.A]
    J = [[Fraction(x) for x in row] for row in engine.J]
    F = [Fraction(x) for x in problem.F(engine.z)]
    w = [Fraction(x) for x in problem.weight_vector(np.asarray(theta, dtype=float))[0]]
    M = [[sum(A[i][k] * J[k][j] for k in range(N)) - (1 if i == j else 0)
          for j in range(N)] for i in range(N)]
    Z1 = max(w[i] * sum(abs(M[i][j]) / w[j] for j in range(N)) for i in range(N))
    AF = [sum(A[i][k] * F[k] for k in range(N)) for i in range(N)]
    Y0 = max(w[i] * abs(AF[i]) for i in range(N))
    return float(Y0), float(Z1)


# ---- the conditioning family -------------------------------------------------------
def degenerate_state(problem, z_star, s):
    """A one-parameter family of states driving the SHARED Jacobian toward singular.

    J[:n,:n] = diag(c_om + H Om) + Om (x) H - c_l XD is homogeneous of degree one in
    (Om, c_l, c_om), so scaling the whole interior state by `s` scales that block by `s`
    while the two border rows stay O(1) -- the condition number therefore grows like 1/s
    and reaches exact singularity at s = 0.  Nothing about this state is physical; it is
    an adversarial input, which is the point."""
    Om, c_l, c_om = problem.unpack(z_star)
    return problem.pack(Om * s, c_l * s, c_om * s)


# ---- gates -------------------------------------------------------------------------
def gate_A1_batch_independence(problem, z_star):
    """Can ONE batch member move the shared inverse, or another member's answer?

    Structural half: J and A are functions of `z` alone -- no weight enters them -- so the
    channel the thesis worries about does not exist by construction.  Empirical half: put
    poison in a batch beside clean weights and compare the clean members' returned bits
    against the same weights evaluated alone."""
    eng = FitnessEngine(problem, z_star)
    k = len(PROBE_THETAS)
    poisons = np.array([[np.nan, 0.0, 0.0, 0.0, -2.0],
                        [0.0, 0.0, 0.0, 0.0, np.inf],
                        [1e6, 0.0, -1e6, 0.0, -2.0],
                        [0.0, -300.0, 0.0, 300.0, -2.0]])
    alone = np.array([eng.fitness(t, box=False) for t in PROBE_THETAS])
    clean_batch = eng.fitness_many(PROBE_THETAS, box=False)
    poison_last = eng.fitness_many(np.vstack([PROBE_THETAS, poisons]), box=False)[:k]
    poison_first = eng.fitness_many(np.vstack([poisons, PROBE_THETAS]), box=False)[len(poisons):]
    clean_batch_boxed = eng.fitness_many(PROBE_THETAS)
    poison_last_boxed = eng.fitness_many(np.vstack([PROBE_THETAS, poisons]))[:k]

    def maxdev(a, b):
        return float(np.max(np.abs(a - b)))

    # THE contamination question: does the PRESENCE of poison move a clean member at all?
    contamination = max(maxdev(poison_last, clean_batch), maxdev(poison_first, clean_batch),
                        maxdev(poison_last_boxed, clean_batch_boxed))
    # the separate, benign effect: k = 1 and k = 6 take different BLAS paths, so the
    # summation order differs. Measured in ulps so it cannot be mistaken for the above.
    shape_effect = maxdev(clean_batch, alone)
    ulps = float(np.max(np.abs(clean_batch - alone) / np.spacing(np.abs(alone))))
    e2 = FitnessEngine(problem, z_star)
    _ = e2.fitness_many(np.vstack([PROBE_THETAS, poisons]), box=False)
    same_A = bool(np.array_equal(e2.A, eng.A) and np.array_equal(e2.J, eng.J))
    return {"n_clean_members": k, "n_poison_members": len(poisons),
            "poison_contamination_max_abs_deviation": contamination,
            "clean_members_bitwise_identical_with_poison_present": bool(contamination == 0.0),
            "batch_shape_effect_max_abs_deviation": shape_effect,
            "batch_shape_effect_ulps": ulps,
            "shared_inverse_unchanged_by_batch": same_A,
            "weight_enters_J_or_A": False,
            "note": "J = jacobian(z), A = inv(J): neither takes theta as an argument, so no "
                    "batch member can move the shared inverse -- the channel the thesis "
                    "worries about does not exist by construction, and is checked bitwise "
                    "in both orderings (poison first and poison last). The separate 1-ulp "
                    "shift between k = 1 and k = 6 is BLAS summation order for a different "
                    "matmul shape, present with no poison in the batch at all."}


def gate_A2_conditioning_ladder(problem, z_star):
    """The ladder: drive the shared Jacobian to singular and watch what comes back."""
    rungs = []
    for s in [1.0, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-11, 1e-12, 1e-13, 1e-14, 1e-16, 0.0]:
        zz = degenerate_state(problem, z_star, s)
        J = problem.jacobian(zz)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cond = float(np.linalg.cond(J))
        row = {"s": s, "cond_J": cond}
        try:
            eng = FitnessEngine(problem, zz)
        except np.linalg.LinAlgError as exc:
            row.update({"outcome": "raised", "exception": type(exc).__name__,
                        "message": str(exc)})
            rungs.append(row)
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Y0, Z1, Z2 = eng.constants_many(TUNED[None, :])
            fit = eng.fitness(TUNED)
        row.update({"outcome": "finite" if np.isfinite(fit) else "flagged_inf",
                    "Y0": float(Y0[0]), "Z1": float(Z1[0]), "Z2": float(Z2[0]),
                    "fitness": None if not np.isfinite(fit) else float(fit)})
        rungs.append(row)
    finite = [r for r in rungs if r.get("outcome") == "finite"]
    flagged = [r for r in rungs if r.get("outcome") in ("flagged_inf", "raised")]
    crossing = next((r["cond_J"] for r in rungs if r.get("Z1", 0.0) >= 1.0), None)
    return {"rungs": rungs, "n_rungs": len(rungs), "n_finite": len(finite),
            "n_flagged": len(flagged),
            "cond_at_Z1_crossing": crossing,
            "cond_span": [rungs[0]["cond_J"], rungs[-2]["cond_J"]],
            "Z1_span": [rungs[0]["Z1"], max(r.get("Z1", 0.0) for r in rungs)],
            "exact_singular_raises": rungs[-1].get("outcome") == "raised"}


def gate_A3_highprec_defect(problem, z_star):
    """Is the FINITE number the engine returns on the ladder the TRUE one?

    Every rung x every probe weight, float64 batch path against the longdouble
    recomputation of the identical A and J.  The dangerous direction is one-sided: a
    reported fitness SMALLER than the truth flatters the weight."""
    cases, worst_flatter, worst_rel_Z1, worst_rel_Y0 = [], -np.inf, 0.0, 0.0
    n_should_have_been_rejected = 0
    for s in [1.0, 1e-4, 1e-8, 1e-10, 1e-11, 1e-12, 1e-13]:
        zz = degenerate_state(problem, z_star, s)
        eng = FitnessEngine(problem, zz)
        cond = float(np.linalg.cond(eng.J))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Y0, Z1, Z2 = eng.constants_many(PROBE_THETAS)
            fits = eng.fitness_many(PROBE_THETAS, box=False)
        for i, th in enumerate(PROBE_THETAS):
            rY0, rZ1, rZ2 = reference_constants(eng, problem, th)
            rfit = fitness_from(rY0, rZ1, rZ2)
            flatter = (rfit - float(fits[i])) if np.isfinite(fits[i]) and np.isfinite(rfit) else 0.0
            rejected = bool(np.isfinite(fits[i]) and rZ1 >= 1.0)
            n_should_have_been_rejected += int(rejected)
            worst_flatter = max(worst_flatter, flatter)
            worst_rel_Z1 = max(worst_rel_Z1, abs(float(Z1[i]) / rZ1 - 1.0) if rZ1 > 0 else 0.0)
            worst_rel_Y0 = max(worst_rel_Y0, abs(float(Y0[i]) / rY0 - 1.0) if rY0 > 0 else 0.0)
            cases.append({"s": s, "cond_J": cond, "theta": [float(x) for x in th],
                          "Z1_float64": float(Z1[i]), "Z1_longdouble": rZ1,
                          "Y0_float64": float(Y0[i]), "Y0_longdouble": rY0,
                          "fitness_float64": None if not np.isfinite(fits[i]) else float(fits[i]),
                          "fitness_longdouble": None if not np.isfinite(rfit) else rfit,
                          "decades_flattered": flatter,
                          "reference_would_reject": rejected})
    return {"n_cases": len(cases),
            "max_relative_deviation_Z1": worst_rel_Z1,
            "max_relative_deviation_Y0": worst_rel_Y0,
            "max_decades_the_shortcut_flatters": float(worst_flatter),
            "threshold_decades": SILENT_DECADES,
            "n_finite_that_reference_would_reject": n_should_have_been_rejected,
            "cases": cases}


def gate_A4_exact_rational():
    """The longdouble reference, itself checked against exact rational arithmetic."""
    pr = BorderedCLM(n=N_EXACT)
    z_star, _ = pr.newton()
    out = []
    for s in [1.0, 1e-8, 1e-12]:
        zz = degenerate_state(pr, z_star, s)
        eng = FitnessEngine(pr, zz)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Y0, Z1, _ = eng.constants_many(TUNED[None, :])
        eY0, eZ1 = exact_constants(eng, pr, TUNED)
        rY0, rZ1, _ = reference_constants(eng, pr, TUNED)
        out.append({"n": N_EXACT, "s": s, "cond_J": float(np.linalg.cond(eng.J)),
                    "Z1_float64": float(Z1[0]), "Z1_longdouble": rZ1, "Z1_exact": eZ1,
                    "Y0_float64": float(Y0[0]), "Y0_longdouble": rY0, "Y0_exact": eY0,
                    "rel_float64_vs_exact_Z1": float(Z1[0]) / eZ1 - 1.0 if eZ1 else 0.0,
                    "rel_longdouble_vs_exact_Z1": rZ1 / eZ1 - 1.0 if eZ1 else 0.0,
                    "float64_understates_Z1": bool(float(Z1[0]) < eZ1)})
    return {"cases": out,
            "worst_rel_float64_vs_exact_Z1": max(abs(c["rel_float64_vs_exact_Z1"]) for c in out),
            "worst_rel_longdouble_vs_exact_Z1": max(abs(c["rel_longdouble_vs_exact_Z1"]) for c in out)}


def gate_A5_poisoned_genome(problem, z_star):
    """NaN / +-inf in every gene, with the box on and off."""
    eng = FitnessEngine(problem, z_star)
    cases, n_finite = [], 0
    for g in range(5):
        for pname, pval in POISONS.items():
            th = TUNED.copy()
            th[g] = pval
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                f_box = eng.fitness(th, box=True)
                f_nobox = eng.fitness(th, box=False)
                Y0, Z1, Z2 = eng.constants_many(th[None, :])
            fin_box = bool(np.isfinite(f_box))
            fin_nobox = bool(np.isfinite(f_nobox))
            n_finite += int(fin_box)
            cases.append({"gene": GENE_NAMES[g], "poison": pname,
                          "in_box": bool(in_box(th)),
                          "fitness_box_on": None if not fin_box else float(f_box),
                          "fitness_box_off": None if not fin_nobox else float(f_nobox),
                          "finite_box_on": fin_box, "finite_box_off": fin_nobox,
                          "Y0": None if not np.isfinite(Y0[0]) else float(Y0[0]),
                          "Z1": None if not np.isfinite(Z1[0]) else float(Z1[0])})
    # all five genes NaN at once, and a NaN in the middle of an otherwise-legal genome
    for label, th in [("all_five_nan", np.full(5, np.nan)),
                      ("nan_in_legal_genome", np.array([1.0, 1.0, -1.0, np.nan, -2.0]))]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f_box, f_nobox = eng.fitness(th, box=True), eng.fitness(th, box=False)
        n_finite += int(np.isfinite(f_box))
        cases.append({"gene": label, "poison": "nan", "in_box": bool(in_box(th)),
                      "fitness_box_on": None if not np.isfinite(f_box) else float(f_box),
                      "fitness_box_off": None if not np.isfinite(f_nobox) else float(f_nobox),
                      "finite_box_on": bool(np.isfinite(f_box)),
                      "finite_box_off": bool(np.isfinite(f_nobox))})
    n_inbox_nan = sum(1 for c in cases if c["poison"] == "nan" and c["in_box"])
    n_nan = sum(1 for c in cases if c["poison"] == "nan")
    return {"n_cases": len(cases), "n_finite_with_box": n_finite,
            "n_finite_without_box": sum(1 for c in cases if c["finite_box_off"]),
            "n_nan_genomes_accepted_by_in_box": n_inbox_nan, "n_nan_genomes": n_nan,
            "cases": cases}


def gate_A6_poisoned_state(problem, z_star):
    """NaN / inf in the STATE -- the input that fixes the shared inverse for everyone."""
    n = problem.n
    muts = {"Omega[0]=nan": (0, np.nan), "Omega[mid]=nan": (n // 2, np.nan),
            "Omega[0]=inf": (0, np.inf), "c_l=nan": (n, np.nan),
            "c_l=inf": (n, np.inf), "c_omega=nan": (n + 1, np.nan),
            "c_omega=inf": (n + 1, np.inf)}
    cases, n_finite = [], 0
    for label, (idx, val) in muts.items():
        zz = z_star.copy()
        zz[idx] = val
        row = {"case": label}
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                eng = FitnessEngine(problem, zz)
                f = eng.fitness(TUNED)
            fin = bool(np.isfinite(f))
            n_finite += int(fin)
            row.update({"outcome": "finite" if fin else "flagged_inf",
                        "fitness": float(f) if fin else None})
        except np.linalg.LinAlgError as exc:
            row.update({"outcome": "raised", "exception": type(exc).__name__,
                        "message": str(exc)})
        cases.append(row)
    # the exactly-singular state, from the ladder's own s = 0 end
    zz = degenerate_state(problem, z_star, 0.0)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f = FitnessEngine(problem, zz).fitness(TUNED)
        cases.append({"case": "exactly_singular_state",
                      "outcome": "finite" if np.isfinite(f) else "flagged_inf",
                      "fitness": float(f) if np.isfinite(f) else None})
        n_finite += int(np.isfinite(f))
    except np.linalg.LinAlgError as exc:
        cases.append({"case": "exactly_singular_state", "outcome": "raised",
                      "exception": type(exc).__name__, "message": str(exc)})
    return {"n_cases": len(cases), "n_finite": n_finite,
            "n_raised": sum(1 for c in cases if c["outcome"] == "raised"),
            "n_flagged_inf": sum(1 for c in cases if c["outcome"] == "flagged_inf"),
            "cases": cases}


def gate_A7_clip_substitution(problem, n_sample=200000, n_eval=4000, seed=0):
    """`weight_vector` CLIPS log nu at +-LOG_NU_CLIP. Where the clip fires, the returned
    fitness describes a weight the caller did not ask for. Does that ever happen inside
    the box the search is allowed to use?"""
    rng = np.random.default_rng(seed)
    T = BOX_LOWER + (BOX_UPPER - BOX_LOWER) * rng.random((n_sample, 5))
    keep = np.array([in_box(t) for t in T])
    T = T[keep][:n_eval]
    X = problem.X
    worst = 0.0
    for t in T:
        p, logL, q, logl, _ = t
        lg = (0.5 * p * np.log1p((X / 10.0 ** logL) ** 2)
              + 0.5 * q * np.log1p((X / 10.0 ** logl) ** 2))
        worst = max(worst, float(np.abs(lg).max()))
    # out-of-box demonstration that the clip DOES bite when it is reached
    fired = np.array([20.0, -3.0, 20.0, -3.0, -2.0])
    p, logL, q, logl, _ = fired
    lg_fired = float(np.abs(0.5 * p * np.log1p((X / 10.0 ** logL) ** 2)
                            + 0.5 * q * np.log1p((X / 10.0 ** logl) ** 2)).max())
    return {"n_box_accepted_of_sample": int(keep.sum()), "n_sample": n_sample,
            "n_evaluated": int(len(T)), "max_abs_log_nu_in_box": worst,
            "LOG_NU_CLIP": float(LOG_NU_CLIP),
            "headroom_factor": float(LOG_NU_CLIP / worst) if worst else None,
            "clip_fires_in_box": bool(worst >= LOG_NU_CLIP),
            "out_of_box_demo_theta": [float(x) for x in fired],
            "out_of_box_demo_max_abs_log_nu": lg_fired,
            "out_of_box_demo_in_box": bool(in_box(fired)),
            "out_of_box_demo_clip_fires": bool(lg_fired >= LOG_NU_CLIP)}


def gate_A8_batch_vs_single_path(problem, z_star):
    """`constants_many` (batched) against `certificate_constants` (per-theta, the path the
    module's own docstring documents). Same A, same J, different code."""
    eng = FitnessEngine(problem, z_star)
    devs = {"Y0": 0.0, "Z1": 0.0, "Z2": 0.0}
    rows = []
    for s in [1.0, 1e-6, 1e-12]:
        zz = degenerate_state(problem, z_star, s)
        e = FitnessEngine(problem, zz)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Y0, Z1, Z2 = e.constants_many(PROBE_THETAS)
        for i, th in enumerate(PROBE_THETAS):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                c = problem.certificate_constants(zz, th, A=e.A, J=e.J)
            for key, got in (("Y0", Y0[i]), ("Z1", Z1[i]), ("Z2", Z2[i])):
                ref = c[key]
                d = abs(float(got) / ref - 1.0) if ref else abs(float(got) - ref)
                devs[key] = max(devs[key], d)
            rows.append({"s": s, "theta": [float(x) for x in th],
                         "Y0_batch": float(Y0[i]), "Y0_single": float(c["Y0"]),
                         "Z1_batch": float(Z1[i]), "Z1_single": float(c["Z1"]),
                         "Z2_batch": float(Z2[i]), "Z2_single": float(c["Z2"])})
    del eng
    return {"n_comparisons": len(rows), "max_relative_deviation": devs, "rows": rows}


def gate_A9_extreme_range(problem, z_star):
    """A weight with an enormous dynamic range: does the max-of-products OVERFLOW to inf
    (flagged) or UNDERFLOW to zero (a Z_1 of 0 is a certificate that closes for free)?"""
    eng = FitnessEngine(problem, z_star)
    cases = []
    for th in [np.array([4.0, -3.0, 4.0, -3.0, -6.0]),
               np.array([-4.0, -3.0, -4.0, -3.0, 2.0]),
               np.array([400.0, -3.0, 0.0, 0.0, -2.0]),
               np.array([0.0, 0.0, 0.0, 0.0, -300.0]),
               np.array([0.0, 0.0, 0.0, 0.0, 300.0])]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            w, _ = problem.weight_vector(th)
            Y0, Z1, Z2 = eng.constants_many(th[None, :])
            f_on, f_off = eng.fitness(th), eng.fitness(th, box=False)
        rng_log = (float(np.log10(np.max(w) / np.min(w)))
                   if np.isfinite(w).all() and np.min(w) > 0 else None)
        cases.append({"theta": [float(x) for x in th], "in_box": bool(in_box(th)),
                      "log10_weight_range": rng_log,
                      "Z1": float(Z1[0]) if np.isfinite(Z1[0]) else None,
                      "Z1_is_nan": bool(np.isnan(Z1[0])), "Z1_is_zero": bool(Z1[0] == 0.0),
                      "Y0": float(Y0[0]) if np.isfinite(Y0[0]) else None,
                      "fitness_box_on": float(f_on) if np.isfinite(f_on) else None,
                      "fitness_box_off": float(f_off) if np.isfinite(f_off) else None})
    return {"n_cases": len(cases),
            "n_spurious_zero_Z1": sum(1 for c in cases if c["Z1_is_zero"]),
            "n_finite_box_on": sum(1 for c in cases if c["fitness_box_on"] is not None),
            "n_finite_box_off": sum(1 for c in cases if c["fitness_box_off"] is not None),
            "cases": cases}


# ---- the verdict -------------------------------------------------------------------
def verdict(A1, A2, A3, A4, A5, A6, A7, A9):
    """The gate, applied to the measurements by the pre-committed criterion."""
    findings = []
    if A1["poison_contamination_max_abs_deviation"] > 0.0:
        findings.append(f"(g) a poisoned batch member moved a clean member's fitness by "
                        f"{A1['poison_contamination_max_abs_deviation']:.3e}")
    if A3["n_finite_that_reference_would_reject"] > 0:
        findings.append(f"(a) {A3['n_finite_that_reference_would_reject']} finite fitness "
                        f"values whose higher-precision Z_1 is >= 1")
    if A3["max_decades_the_shortcut_flatters"] > SILENT_DECADES:
        findings.append(f"(b) the shortcut flatters a weight by "
                        f"{A3['max_decades_the_shortcut_flatters']:.3f} decades "
                        f"(threshold {SILENT_DECADES})")
    if A7["clip_fires_in_box"]:
        findings.append("(c) LOG_NU_CLIP substitutes a different weight inside the box")
    if A5["n_finite_with_box"] > 0:
        findings.append(f"(d) {A5['n_finite_with_box']} poisoned genomes returned a finite "
                        f"fitness with the box on")
    if A6["n_finite"] > 0:
        findings.append(f"(e) {A6['n_finite']} poisoned states returned a finite fitness")
    if A9["n_spurious_zero_Z1"] > 0:
        findings.append(f"(f) {A9['n_spurious_zero_Z1']} extreme-range weights underflowed "
                        f"Z_1 to exactly zero")
    return {"gate": ("Under an adversarial battery (a batch member driving the shared "
                     "Jacobian toward near-singularity, NaN-poisoned weight parameters), "
                     "does FitnessEngine ever silently return a finite, plausible-looking "
                     "fitness value instead of propagating or flagging the "
                     "ill-conditioning?"),
            "answer": "YES" if findings else "NO",
            "findings": findings,
            "criterion": {"silent_decades": SILENT_DECADES,
                          "reference": "np.longdouble recomputation of the identical A and "
                                       "J, itself checked against exact rational arithmetic "
                                       "(gate A4)"}}


def main():
    t0 = time.time()
    problem = BorderedCLM(n=N_GRID)
    z_star, info = problem.newton()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        A1 = gate_A1_batch_independence(problem, z_star)
        A2 = gate_A2_conditioning_ladder(problem, z_star)
        A3 = gate_A3_highprec_defect(problem, z_star)
        A4 = gate_A4_exact_rational()
        A5 = gate_A5_poisoned_genome(problem, z_star)
        A6 = gate_A6_poisoned_state(problem, z_star)
        A7 = gate_A7_clip_substitution(problem)
        A8 = gate_A8_batch_vs_single_path(problem, z_star)
        A9 = gate_A9_extreme_range(problem, z_star)
    out = {
        "leg": 97, "route": "WSA", "module_audited": "solver/weight_search.py",
        "class_audited": "FitnessEngine",
        "read_only": True,
        "scope_note": ("Code robustness only. Stage B's / leg 49's / leg 59's frozen gate "
                       "verdicts are NOT reopened, contested or re-scored here; no GA, no "
                       "search, no roster scoring, no six-property property is re-measured."),
        "substrate": {"n": N_GRID, "N": problem.N, "Xmax": float(problem.Xmax),
                      "newton_converged": bool(info["converged"]),
                      "residual": float(info["residual_ladder"][-1]),
                      "residual_floor": float(info["residual_floor"]),
                      "cond_J_at_solution": float(np.linalg.cond(problem.jacobian(z_star))),
                      "baseline_fitness": {k: float(FitnessEngine(problem, z_star).fitness(v))
                                           for k, v in hand_weights().items()}},
        "A1_batch_independence": A1,
        "A2_conditioning_ladder": A2,
        "A3_highprec_defect": A3,
        "A4_exact_rational": A4,
        "A5_poisoned_genome": A5,
        "A6_poisoned_state": A6,
        "A7_clip_substitution": A7,
        "A8_batch_vs_single_path": A8,
        "A9_extreme_range": A9,
        "verdict": verdict(A1, A2, A3, A4, A5, A6, A7, A9),
        "runtime_seconds": None,
    }
    out["runtime_seconds"] = round(time.time() - t0, 2)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(here, "writeup", "data", "p2_route_wsa_v1_adversarial.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    v = out["verdict"]
    print(f"substrate: n={N_GRID} cond(J*)={out['substrate']['cond_J_at_solution']:.3e} "
          f"baseline fitness {out['substrate']['baseline_fitness']}")
    print(f"A1 batch: poison contamination {A1['poison_contamination_max_abs_deviation']:.3e}, "
          f"batch-shape effect {A1['batch_shape_effect_ulps']:.1f} ulp")
    print(f"A2 ladder: {A2['n_rungs']} rungs, cond {A2['cond_span'][0]:.2e} -> "
          f"{A2['cond_span'][1]:.2e}, Z_1 crosses 1 at cond {A2['cond_at_Z1_crossing']:.2e}, "
          f"{A2['n_flagged']} flagged, exact-singular raises: {A2['exact_singular_raises']}")
    print(f"A3 high precision: {A3['n_cases']} cases, max rel dev Z_1 "
          f"{A3['max_relative_deviation_Z1']:.3e}, worst flattering "
          f"{A3['max_decades_the_shortcut_flatters']:+.3e} decades, "
          f"{A3['n_finite_that_reference_would_reject']} finite-but-should-reject")
    print(f"A4 exact rational: float64 vs EXACT worst rel {A4['worst_rel_float64_vs_exact_Z1']:.3e}")
    print(f"A5 genomes: {A5['n_cases']} poisoned, {A5['n_finite_with_box']} finite with box, "
          f"{A5['n_nan_genomes_accepted_by_in_box']}/{A5['n_nan_genomes']} NaN genomes pass in_box")
    print(f"A6 states: {A6['n_cases']} poisoned, {A6['n_finite']} finite, "
          f"{A6['n_raised']} raised, {A6['n_flagged_inf']} +inf")
    print(f"A7 clip: max|log nu| in box {A7['max_abs_log_nu_in_box']:.2f} vs clip "
          f"{A7['LOG_NU_CLIP']:.0f} ({A7['headroom_factor']:.2f}x headroom)")
    print(f"A8 batch vs single: max rel dev {A8['max_relative_deviation']}")
    print(f"A9 extreme range: {A9['n_spurious_zero_Z1']} spurious zero Z_1, "
          f"{A9['n_finite_box_on']}/{A9['n_cases']} finite with box")
    print(f"VERDICT: {v['answer']}  {v['findings']}")
    print(f"wrote {path} in {out['runtime_seconds']}s")
    return out


if __name__ == "__main__":
    main()
