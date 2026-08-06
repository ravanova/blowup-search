"""ADVERSARIAL gates for `solver/weight_search.py`'s FitnessEngine -- Route-WSA, leg 97.

`test_weight_search.py` (legs 49/50/59) tests that the module MEASURES correctly, on
well-posed input: a converged Newton state, the closed-form CLM profile, gauge invariance
to 4.4e-16.  This file tests what the module SAYS when the input is *wrong* rather than
merely hard.  `capabilities.py`'s validated line for the module names the shortcut under
audit verbatim -- "FitnessEngine (batched, Jacobian inverted once)".

The gate this file banks, verbatim:

    Under an adversarial battery (a batch member driving the shared Jacobian toward
    near-singularity, NaN-poisoned weight parameters), does FitnessEngine ever silently
    return a finite, plausible-looking fitness value instead of propagating or flagging
    the ill-conditioning?

Leg 97 answered **NO** over 100+ adversarial cases, so these gates pin the ROBUST
behaviour: each one fails the day an edit makes the engine start absorbing a bad input
quietly.  Full magnitudes in `writeup/data/p2_route_wsa_v1_adversarial.json`, produced by
`experiments/p2_route_wsa_v1_adversarial.py`; this file is the fast subset that runs in the
merge gate.

SCOPE, said first because it is the thing most easily misread.  This is a CODE-ROBUSTNESS
file.  It says nothing about whether the fitness is scientifically viable, and it neither
reopens nor re-scores stage B's / leg 49's / leg 59's frozen gate verdicts.  No GA, no
search, no roster scoring happens here -- the engine is called directly on hand-built
inputs, which is why the plan-of-record ban on "GA compute on an unvalidated fitness" is
untouched.  `solver/weight_search.py` was READ-ONLY under leg 97 and nothing here patches
it; gates 12 and 13 pin two measured gaps the leg had no authority to close.

THE REFERENCE is the device `weight_search._F_longdouble` already uses: the identical
float64 `A` and `J` (both exactly representable, so the cast is lossless) re-multiplied in
`np.longdouble`.  Gate 8 checks that reference itself against EXACT rational arithmetic, so
no step of the chain rests on an unverified higher-precision claim.
"""

import sys
import warnings
from fractions import Fraction

import numpy as np

sys.path.insert(0, ".")

from solver.weight_search import (
    BOX_LOWER, BOX_UPPER, LOG_NU_CLIP, BorderedCLM, FitnessEngine, in_box,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


N_GRID = 81          # fast; none of these gates is a resolution claim
N_EXACT = 31         # the exact-rational grid: O(N^3) Fraction products
SILENT_DECADES = 0.5      # leg 97's pre-committed corruption threshold
TUNED = np.array([0.0, 0.0, 0.0, 0.0, -2.0])       # leg 46's hand weight
PROBE_THETAS = np.array([
    [0.0, 0.0, 0.0, 0.0, 0.0],                      # naive
    TUNED,
    [1.0, 1.0, -1.0, -1.0, -2.0],
    [-2.0, 0.5, 1.0, 2.0, -3.0],
    [0.5, 2.0, 0.0, -1.0, -1.0],
])
POISONS = {"nan": np.nan, "+inf": np.inf, "-inf": -np.inf}
POISON_GENOMES = np.array([[np.nan, 0.0, 0.0, 0.0, -2.0],
                           [0.0, 0.0, 0.0, 0.0, np.inf],
                           [1e6, 0.0, -1e6, 0.0, -2.0],
                           [0.0, -300.0, 0.0, 300.0, -2.0]])

warnings.filterwarnings("ignore")          # overflow/NaN warnings ARE the subject here


def degenerate_state(pr, z_star, s):
    """Drive the SHARED Jacobian toward singular.

    J's interior block diag(c_om + H Om) + Om (x) H - c_l XD is homogeneous of degree one
    in (Omega, c_l, c_omega) while the two border rows are not, so scaling the interior
    state by `s` grows cond(J) like 1/s and is exactly singular at s = 0.  Nothing about
    this state is physical -- it is an adversarial input, which is the point."""
    Om, c_l, c_om = pr.unpack(z_star)
    return pr.pack(Om * s, c_l * s, c_om * s)


def reference_constants(eng, pr, theta):
    """(Y0, Z1, Z2) for the engine's OWN A and J, recomputed in np.longdouble."""
    Al = np.asarray(eng.A, dtype=np.longdouble)
    Jl = np.asarray(eng.J, dtype=np.longdouble)
    w, nu = pr.weight_vector(np.asarray(theta, dtype=float))
    wl, nul = np.asarray(w, dtype=np.longdouble), np.asarray(nu, dtype=np.longdouble)
    Ml = np.abs(np.eye(pr.N, dtype=np.longdouble) - Al @ Jl)
    Fl = np.asarray(pr.F(eng.z), dtype=np.longdouble)
    Y0 = float(np.max(wl * np.abs(Al @ Fl)))
    Z1 = float(np.max(wl * (Ml @ (1.0 / wl))))
    A_norm = float(np.max(wl * (np.abs(Al) @ (1.0 / wl))))
    H_ni = float(np.max(np.abs(np.asarray(pr.H, dtype=np.longdouble)) @ (1.0 / nul)))
    XD_nn = float(np.max(nul * (np.abs(np.asarray(pr.XD, dtype=np.longdouble)) @ (1.0 / nul))))
    B = H_ni + 1.0 / float(w[pr.n + 1]) + XD_nn / float(w[pr.n])
    return Y0, Z1, 2.0 * A_norm * B


def reference_fitness(Y0, Z1, Z2):
    if not (np.isfinite(Y0) and np.isfinite(Z1) and np.isfinite(Z2)):
        return float("inf")
    if Z1 >= 1.0 or Z2 <= 0.0 or Y0 <= 0.0:
        return float("inf")
    return float(np.log10(Y0 / ((1.0 - Z1) ** 2 / (2.0 * Z2))))


PR = BorderedCLM(n=N_GRID)
Z_STAR, INFO = PR.newton()
ENG = FitnessEngine(PR, Z_STAR)

gate("substrate: the audit runs at a CONVERGED state",
     bool(INFO["converged"]),
     f"n = {N_GRID}, N = {PR.N}, residual {INFO['residual_ladder'][-1]:.3e} against a "
     f"measured float64 floor {INFO['residual_floor']:.3e}, cond(J) = "
     f"{np.linalg.cond(PR.jacobian(Z_STAR)):.3e}, tuned_leg46 fitness "
     f"{ENG.fitness(TUNED):.6f} -- every adversarial answer below is a DEPARTURE from "
     "this, not an artefact of a bad starting point")


# --------------------------------------------------------------------------
# 1-3.  the channel the thesis worries about: does not exist, and is checked
# --------------------------------------------------------------------------
_clean = ENG.fitness_many(PROBE_THETAS, box=False)
_last = ENG.fitness_many(np.vstack([PROBE_THETAS, POISON_GENOMES]), box=False)[:len(PROBE_THETAS)]
_first = ENG.fitness_many(np.vstack([POISON_GENOMES, PROBE_THETAS]),
                          box=False)[len(POISON_GENOMES):]
_alone = np.array([ENG.fitness(t, box=False) for t in PROBE_THETAS])
_shape_ulp = float(np.max(np.abs(_clean - _alone) / np.spacing(np.abs(_alone))))

gate("1 -- a poisoned batch member cannot move a clean member, BITWISE",
     bool(np.array_equal(_last, _clean) and np.array_equal(_first, _clean)),
     f"{len(PROBE_THETAS)} clean weights evaluated beside {len(POISON_GENOMES)} poisoned "
     f"ones (NaN gene, inf gene, |p| = 1e6, a 600-decade weight range), in BOTH orderings: "
     f"deviation {max(float(np.max(np.abs(_last - _clean))), float(np.max(np.abs(_first - _clean)))):.3e}. "
     "Bitwise is the right demand because the shared inverse does not depend on the "
     "weight at all, so there is no legitimate mechanism for one member to reach another")

gate("2 -- the shared inverse is a function of the STATE alone",
     bool(np.array_equal(FitnessEngine(PR, Z_STAR).A, ENG.A)
          and np.array_equal(FitnessEngine(PR, Z_STAR).J, ENG.J)),
     "J = jacobian(z) and A = inv(J) take no theta argument, so 'a batch member driving "
     "the shared Jacobian toward near-singularity' is structurally impossible -- the "
     "conditioning hazard enters through the STATE (gates 4-7), never through a weight. "
     f"The one batching artefact that does exist is benign and is measured: k = 1 and "
     f"k = {len(PROBE_THETAS)} can take different BLAS paths, so summation order differs "
     f"by {_shape_ulp:.1f} ulp here (1.0 ulp at n = 101, leg 97's headline grid) -- an "
     "effect present with no poison in the batch at all, and separate from gate 1's "
     "exactly-zero contamination")

_dev = {"Y0": 0.0, "Z1": 0.0, "Z2": 0.0}
for _s in (1.0, 1e-6, 1e-12):
    _zz = degenerate_state(PR, Z_STAR, _s)
    _e = FitnessEngine(PR, _zz)
    _Y0, _Z1, _Z2 = _e.constants_many(PROBE_THETAS)
    for _i, _th in enumerate(PROBE_THETAS):
        _c = PR.certificate_constants(_zz, _th, A=_e.A, J=_e.J)
        for _k, _got in (("Y0", _Y0[_i]), ("Z1", _Z1[_i]), ("Z2", _Z2[_i])):
            _dev[_k] = max(_dev[_k], abs(float(_got) / _c[_k] - 1.0) if _c[_k] else 0.0)

gate("3 -- the BATCHED path and the per-theta path agree, benign AND severe",
     max(_dev.values()) < 1e-12,
     f"`constants_many` vs `certificate_constants` over {3 * len(PROBE_THETAS)} "
     f"(state, weight) pairs spanning cond(J) 1e5 -> 1e17: max relative deviation "
     f"Y_0 {_dev['Y0']:.2e}, Z_1 {_dev['Z1']:.2e}, Z_2 {_dev['Z2']:.2e}. The shortcut "
     "computes the same numbers the documented path does, not a cheaper approximation")


# --------------------------------------------------------------------------
# 4-8.  the conditioning ladder -- the heart of the gate
# --------------------------------------------------------------------------
_conds, _z1s = [], []
for _s in (1.0, 1e-4, 1e-8, 1e-10, 1e-12, 1e-13, 1e-14):
    _e = FitnessEngine(PR, degenerate_state(PR, Z_STAR, _s))
    _conds.append(float(np.linalg.cond(_e.J)))
    _z1s.append(float(_e.constants_many(TUNED[None, :])[1][0]))

gate("4 -- Z_1 RISES with the conditioning and crosses 1",
     bool(all(b > a for a, b in zip(_z1s, _z1s[1:])) and _z1s[0] < 1e-6 and _z1s[-1] > 1.0
          and _conds[-1] / _conds[0] > 1e12),
     f"over cond(J) {_conds[0]:.2e} -> {_conds[-1]:.2e}, Z_1 runs {_z1s[0]:.2e} -> "
     f"{_z1s[-1]:.2e}, monotone in {len(_z1s)}/{len(_z1s)} rungs. The module's own comment "
     "claims Z_1 ~ eps * kappa * range; this asserts it as a MEASUREMENT. It is the whole "
     "robustness mechanism -- the defect I - A DF is what makes a garbage inverse visible")

_last_finite, _first_flagged = None, None
for _s in (1e-10, 1e-12, 1e-13, 1e-14, 1e-16):
    _e = FitnessEngine(PR, degenerate_state(PR, Z_STAR, _s))
    _c = float(np.linalg.cond(_e.J))
    if np.isfinite(_e.fitness(TUNED)):
        _last_finite = _c
    elif _first_flagged is None:
        _first_flagged = _c

gate("5 -- the certificate SHUTS before the inverse is meaningless",
     bool(_first_flagged is not None and (_last_finite is None or _last_finite < 1e19)),
     f"last finite answer at cond(J) = {_last_finite:.3e}, first +inf refusal at "
     f"{_first_flagged:.3e}. At cond * eps > 1 the inverse carries no correct digits, and "
     "the engine returns +inf there rather than a number")

_raised = None
try:
    FitnessEngine(PR, degenerate_state(PR, Z_STAR, 0.0))
except np.linalg.LinAlgError as _exc:
    _raised = _exc

gate("6 -- an exactly singular state RAISES rather than returns",
     _raised is not None,
     f"s = 0 (interior block identically zero): {type(_raised).__name__ if _raised else 'NOTHING'}"
     f"({str(_raised)!r}) -- loud failure, not a plausible number")

_worst_flatter, _n_should_reject, _n_finite = -np.inf, 0, 0
for _s in (1.0, 1e-8, 1e-11, 1e-12, 1e-13):
    _e = FitnessEngine(PR, degenerate_state(PR, Z_STAR, _s))
    _fits = _e.fitness_many(PROBE_THETAS, box=False)
    for _i, _th in enumerate(PROBE_THETAS):
        if not np.isfinite(_fits[_i]):
            continue
        _n_finite += 1
        _rY0, _rZ1, _rZ2 = reference_constants(_e, PR, _th)
        _n_should_reject += int(_rZ1 >= 1.0)
        _rfit = reference_fitness(_rY0, _rZ1, _rZ2)
        if np.isfinite(_rfit):
            _worst_flatter = max(_worst_flatter, _rfit - float(_fits[_i]))

gate("7 -- THE GATE: every finite answer is the TRUE one, and never a flattering one",
     bool(_n_finite >= 10 and _n_should_reject == 0 and _worst_flatter < SILENT_DECADES),
     f"{_n_finite} finite (state, weight) answers across cond(J) 1e5 -> 1e18, each against "
     f"a longdouble recomputation of the identical A and J: {_n_should_reject} cases where "
     f"the reference would have rejected a certificate float64 accepted, worst flattering "
     f"{_worst_flatter:+.3e} decades against a pre-committed {SILENT_DECADES}. Flattering "
     "(a reported fitness SMALLER than the truth) is the dangerous direction and is the "
     "corruption criterion itself")

_PRX = BorderedCLM(n=N_EXACT)
_ZX, _IX = _PRX.newton()
_exact_rows = []
for _s, _tol in ((1.0, 5e-2), (1e-12, 1e-8)):
    _e = FitnessEngine(_PRX, degenerate_state(_PRX, _ZX, _s))
    _Z1f = float(_e.constants_many(TUNED[None, :])[1][0])
    _N = _PRX.N
    _A = [[Fraction(x) for x in row] for row in _e.A]
    _J = [[Fraction(x) for x in row] for row in _e.J]
    _w = [Fraction(x) for x in _PRX.weight_vector(TUNED)[0]]
    _M = [[sum(_A[i][k] * _J[k][j] for k in range(_N)) - (1 if i == j else 0)
           for j in range(_N)] for i in range(_N)]
    _Z1x = float(max(_w[i] * sum(abs(_M[i][j]) / _w[j] for j in range(_N)) for i in range(_N)))
    _exact_rows.append((_s, float(np.linalg.cond(_e.J)), _Z1f, _Z1x, _tol))

gate("8 -- the longdouble reference is itself checked against EXACT rational arithmetic",
     bool(_IX["converged"]
          and all(abs(f / x - 1.0) < t and f >= x * (1.0 - t) for _, _, f, x, t in _exact_rows)),
     "; ".join(f"n = {N_EXACT}, s = {s:.0e}, cond {c:.2e}: Z_1 float64 {f:.6e} vs EXACT "
               f"{x:.6e} (rel {f / x - 1.0:+.2e}, tol {t:.0e})" for s, c, f, x, t in _exact_rows)
     + ". float64 values are exactly rational, so I - A J in `Fraction` has NO rounding "
       "anywhere and is the exact defect of the exact float64 A. The percent-level "
       "agreement at benign conditioning is a few ulps of a Z_1 that is pure roundoff "
       "(~1e-13); what matters is the direction, and the reported Z_1 never materially "
       "understates the exact defect")


# --------------------------------------------------------------------------
# 9-11.  poisoned inputs
# --------------------------------------------------------------------------
_geno_cases = [(f"{i}:{p}", np.where(np.arange(5) == i, v, TUNED))
               for i in range(5) for p, v in POISONS.items()]
_geno_cases.append(("all_five_nan", np.full(5, np.nan)))
_geno_cases.append(("nan_buried_in_a_legal_genome", np.array([1.0, 1.0, -1.0, np.nan, -2.0])))
_bad_geno = [(lab, float(ENG.fitness(np.asarray(th, dtype=float))))
             for lab, th in _geno_cases if np.isfinite(ENG.fitness(np.asarray(th, dtype=float)))]

gate("9 -- NO poisoned genome ever returns a number",
     not _bad_geno,
     f"{len(_geno_cases)} cases (NaN / +inf / -inf in each of the five genes, all five at "
     f"once, and a NaN buried in an otherwise-legal genome): {len(_bad_geno)} returned a "
     f"finite fitness. The poison reaches Y_0 and Z_1 as NaN, `Z1 < 1.0` is false for NaN, "
     "and the budget branch returns -1 -> +inf -- refusal by IEEE-754 semantics, and the "
     "same answer with the box off")

_bad_state = []
for _lab, _idx, _val in [("Omega[0]=nan", 0, np.nan), ("Omega[mid]=nan", PR.n // 2, np.nan),
                         ("Omega[0]=inf", 0, np.inf), ("c_l=nan", PR.n, np.nan),
                         ("c_l=inf", PR.n, np.inf), ("c_omega=nan", PR.n + 1, np.nan),
                         ("c_omega=inf", PR.n + 1, np.inf)]:
    _zz = Z_STAR.copy()
    _zz[_idx] = _val
    try:
        _f = FitnessEngine(PR, _zz).fitness(TUNED)
    except np.linalg.LinAlgError:
        continue
    if np.isfinite(_f):
        _bad_state.append((_lab, float(_f)))

gate("10 -- NO poisoned STATE ever returns a number",
     not _bad_state,
     "7 cases (NaN / inf in Omega at the edge and the middle, in c_l, in c_omega): "
     f"{len(_bad_state)} returned a finite fitness. The state is the highest-leverage "
     "input there is -- it fixes the shared inverse for the whole batch at once -- and "
     "every case either raises LinAlgError or comes back +inf")

_range_rows, _bad_range = [], []
for _th in [np.array([4.0, -3.0, 4.0, -3.0, -6.0]),
            np.array([-4.0, -3.0, -4.0, -3.0, 2.0]),
            np.array([400.0, -3.0, 0.0, 0.0, -2.0]),
            np.array([0.0, 0.0, 0.0, 0.0, -300.0]),
            np.array([0.0, 0.0, 0.0, 0.0, 300.0])]:
    _Z1 = float(ENG.constants_many(_th[None, :])[1][0])
    _range_rows.append(_Z1)
    if _Z1 == 0.0 or (np.isfinite(ENG.fitness(_th))) or not (_Z1 > 1.0 or np.isnan(_Z1)):
        _bad_range.append(([float(x) for x in _th], _Z1))

gate("11 -- an extreme weight RANGE overflows loudly, it does not underflow quietly",
     not _bad_range,
     f"5 weights with log10 ranges up to 217 decades: Z_1 comes back "
     f"{min(_range_rows):.2e} .. {max(_range_rows):.2e}, {sum(1 for z in _range_rows if z == 0.0)} "
     "underflowed to exactly zero, 5/5 refused with +inf. A Z_1 of 0 would be a "
     "certificate that closes for free, and it is the one arithmetic outcome that would "
     "make the max-of-products shortcut dangerous")


# --------------------------------------------------------------------------
# 12-13.  the two REMAINING gaps, pinned as measured.  Neither corrupts a fitness,
#         and leg 97 had no authority to patch solver/weight_search.py -- these exist
#         so a change of behaviour is NOTICED rather than discovered (lesson 68).
# --------------------------------------------------------------------------
_nan_admitted = [i for i in range(5) if in_box(np.where(np.arange(5) == i, np.nan, TUNED))]

gate("12 -- REMAINING GAP (harmless): in_box admits a NaN genome",
     bool(_nan_admitted == [0, 1, 2, 3, 4] and in_box(np.full(5, np.nan))
          and not np.isfinite(ENG.fitness(np.full(5, np.nan)))),
     f"`in_box` tests with `<` and `>`, and every comparison against NaN is false "
     f"(IEEE-754 5.11), so {len(_nan_admitted)}/5 single-NaN genomes and the all-NaN "
     "genome are ADMITTED by the box. This is not a corruption -- `fitness` still returns "
     "+inf for every one of them (gate 9) -- and it is pinned, not patched: the day the "
     "box admits NaN AND the fitness returns a number is the day this gate fails")

_rng = np.random.default_rng(0)
_T = BOX_LOWER + (BOX_UPPER - BOX_LOWER) * _rng.random((20000, 5))
_T = _T[np.array([in_box(t) for t in _T])]
_n_admitted = len(_T)
_worst_lg = 0.0
for _p, _logL, _q, _logl, _ in _T[:600]:
    _lg = (0.5 * _p * np.log1p((PR.X / 10.0 ** _logL) ** 2)
           + 0.5 * _q * np.log1p((PR.X / 10.0 ** _logl) ** 2))
    _worst_lg = max(_worst_lg, float(np.abs(_lg).max()))

gate("13 -- REMAINING GAP (unreachable): LOG_NU_CLIP never fires inside the box",
     bool(len(_T) > 100 and _worst_lg < 0.5 * LOG_NU_CLIP),
     f"where `weight_vector`'s clip bites, the fitness describes a weight the caller did "
     f"NOT ask for -- a silent substitution. Over {_n_admitted} box-admitted genomes of "
     f"20000 sampled ({min(600, _n_admitted)} evaluated on the grid), max|log nu| = "
     f"{_worst_lg:.1f} against LOG_NU_CLIP = {LOG_NU_CLIP:.0f}, a "
     f"{LOG_NU_CLIP / _worst_lg:.1f}x headroom. The substitution is real but unreachable "
     "from inside the box; the gate guards the headroom, not the exact number")


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("NOTE: leg 97's gate -- 'does FitnessEngine ever silently return a finite, "
      "plausible-looking fitness instead of propagating or flagging the ill-conditioning?' "
      "-- answered NO. These gates pin the ROBUST behaviour and will fail the day the "
      "engine starts absorbing a bad input quietly. Gates 12 and 13 pin what leg 97 did "
      "NOT close: it was read-only on solver/weight_search.py by construction.")
sys.exit(1 if n_fail else 0)
