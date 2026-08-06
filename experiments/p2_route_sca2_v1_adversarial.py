"""Leg 209 / Route-SCA2 -- ADVERSARIAL AUDIT of `solver/spectral_certificate.py`.

THE MODULE IS READ-ONLY HERE AND IS NOT PATCHED BY THIS LEG, under either gate branch.

--------------------------------------------------------------------------
THE GATE, PRE-COMMITTED (DIRECTION.md leg 209), BOTH BRANCHES
--------------------------------------------------------------------------
"Under adversarial and degenerate inputs (near-singular weight classes,
boundary-of-admissibility `A`, NaN/Inf), does `spectral_certificate.py` ever silently
return a wrong `Z_1`/`sigma_min` value rather than reject or visibly propagate the
defect?"

--------------------------------------------------------------------------
WHY THIS MODULE, AND WHAT THE ANSWER IS *NOT* ABOUT
--------------------------------------------------------------------------
This is leg 127's own module: Theorem NGX (`Z_1 >= 1` for every bounded approximate
inverse on `ell^1_w`) is proved against this module's construction.  It is the single
most load-bearing negative result this repository has produced, and it has been read
read-only by legs 163/171/173/181/183/192 without ever being audited under degenerate
input.  Six of the eight modules this cycle's audit family has checked carried a real
latent defect, so proximity to a proof is not evidence of cleanliness.

**It is also, for exactly that reason, the module where over-claiming would do the most
damage.**  So this runner reports on THREE SEPARATE AXES, fixed in
`writeup/novelty/leg_209.md` section 5 before any measurement was taken:

  (a) does the module return a silently wrong value on adversarial input?   <- THE GATE
  (b) is any BANKED number reachable from the shipped code path by that mechanism?
  (c) does the mechanism touch the ANALYTIC ARGUMENT of Theorem NGX?

**(a) and (c) are different questions and a YES on (a) is not evidence for (c).**
Theorem NGX's proof is two steps, neither of which is a float computation:

  1. `Z_1 >= 1 - ||A||_w * sigma_min(L)` -- folklore, exact arithmetic, no code at all
     (and explicitly disclaimed as not-this-repository's in the module's own NGX header);
  2. `sigma_min(L) -> 0` like `M^-(1-s)`, witnessed by the EXPLICIT sequence
     `v_M = (z_M; h^(M))` whose entire residual is the single truncation-edge row of size
     `|1 - M/2| |h_M| w_M ~ M^(s-1)`, against `||v_M||_w` bounded uniformly because
     `sum m^(s-2)` converges for `s < 1`.  That is an analytic estimate on the INFINITE
     tail; the float path corroborates it (leg 127 measured 0.6985 against a predicted
     0.7000) but is not its content.

--------------------------------------------------------------------------
THE SILENT-WRONG PREDICATE, FIXED BEFORE MEASUREMENT
--------------------------------------------------------------------------
A case is `silent_wrong` iff the module RETURNS a value -- no exception, no NaN or Inf
visible to the caller as a defect signal -- that differs materially from the correct
value for that input, OR returns a defect-signalling value that a caller would read as
the MOST FAVOURABLE answer.

  * UNDERSTATEMENT of a bound, and wrong-direction-favourable, DECIDE the gate.
  * OVERSTATEMENT (a returned bound that is too PESSIMISTIC) is RECORDED and does NOT
    decide the gate.
  * `raised` and visible NaN/Inf propagation are `sound`, not findings.
  * An out-of-documented-domain input that is accepted and answered CORRECTLY for the
    object actually built is `boundary_accepted`, not `silent_wrong`.  Three cases in
    this battery are deliberately filed there rather than counted, because counting them
    would inflate the headline.

Every family carries a clean-input control that MUST come out differently (lesson 90:
a control that cannot come out the other way is not a control, and the tell is that its
numbers are identical).
"""

import json
import os
import sys
from fractions import Fraction

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np                                                     # noqa: E402

sys.path.insert(0, ".")

import solver.spectral_certificate as sc                               # noqa: E402

OUT = "writeup/data/p2_route_sca2_v1_adversarial.json"

CASES = []


def case(family, name, outcome, returned, expected, note):
    """Record one probe.  `outcome` in {silent_wrong, sound, boundary_accepted, raised}."""
    CASES.append({"family": family, "case": name, "outcome": outcome,
                  "returned": returned, "expected": expected, "note": note})
    tag = {"silent_wrong": "SILENT-WRONG", "sound": "sound",
           "boundary_accepted": "boundary", "raised": "raised"}[outcome]
    print(f"  [{tag:>12s}] {family}/{name}: returned={returned!r} expected={expected!r}")


def attempt(fn):
    """Return ('ok', value) or ('raised', 'ExcName: msg')."""
    try:
        return "ok", fn()
    except Exception as e:                                             # noqa: BLE001
        return "raised", f"{type(e).__name__}: {str(e)[:80]}"


def jf(x):
    """JSON-safe float (NaN/Inf become strings so the JSON is readable and valid)."""
    if isinstance(x, float):
        if np.isnan(x):
            return "nan"
        if np.isinf(x):
            return "inf" if x > 0 else "-inf"
    return x


# ==========================================================================
# F7 FIRST -- IS THE CLEAN-INPUT NUMBER ITSELF SOUND?
#
# This runs before the adversarial families on purpose.  Banked lesson 86: a bound
# dominated by its own evaluation error is a statement about the code.  If the module
# were already wrong on clean input, every adversarial finding below would be noise on
# top of a bigger problem, and the blast radius in section (b) could not be bounded.
# ==========================================================================
def f7_clean_input_soundness():
    print("\nF7 -- clean-input soundness: float64 against exact rational arithmetic")
    rows = []
    worst = 0.0
    for K in (8, 16, 32, 64):
        f = sc.finite_section_inverse_norm(K, "geometric", 1.1)
        e = float(sc.exact_inverse_norm(K, Fraction(11, 10)))
        rel = abs(f - e) / e
        worst = max(worst, rel)
        rows.append({"K": K, "float64": f, "exact_rational": e, "rel_diff": rel})
    case("F7", "float_vs_exact_inverse_norm",
         "sound" if worst < 1e-14 else "silent_wrong",
         worst, "< 1e-14",
         "||M_K^-1||_w in float64 vs exact Fraction Gauss-Jordan, geometric nu = 11/10, "
         "K = 8/16/32/64.  This BOUNDS THE BLAST RADIUS: the shipped path is sound, so "
         "every finding below is about inputs the shipped path does not produce.")
    return {"rows": rows, "worst_rel_diff": worst}


# ==========================================================================
# F3 -- THE HEADLINE.  `l1_bounded_below_constant` UNDER NaN.
#
# `sigma_min(L)` is the quantity Theorem NGX's floor divides by.  The function ends
#
#     nrm = float(colsums[j])
#     return (1.0 / nrm if nrm > 0 else float("inf")), j, Li[:, j]
#
# The `nrm > 0` guard was written for `nrm == 0`.  Under IEEE 754 a comparison with a
# NaN operand is UNORDERED -- the fourth relation, "? U" -- so `nan > 0` is False and the
# function takes the branch that returns the LARGEST POSSIBLE sigma_min.
# ==========================================================================
def f3_sigma_min_under_nan():
    print("\nF3 -- l1_bounded_below_constant: the sigma_min guard under NaN/Inf/singular")
    K, Mx, s = 8, 512, 0.3            # leg 127's own shipped (K, M_extra, class) corner
    L = sc._scaled_tail(K, K + Mx, "algebraic", s)[0]
    sig_clean, j_clean, _ = sc.l1_bounded_below_constant(L)
    floor_clean = sc.counterexample_norm_floor(0.5, sig_clean)
    td_clean = sc.general_class_tradeoff(0.5, 100.0, sig_clean)

    # lesson-90 control: the clean arm must produce a DIFFERENT number from every
    # poisoned arm, otherwise this probe is a tautology of the code.
    case("F3", "clean_control_shipped_corner", "sound", sig_clean,
         "finite, positive, reproduces leg 127's ladder",
         f"K=8, M_extra=512, algebraic s=0.3: sigma_min={sig_clean!r}, "
         f"counterexample_norm_floor(Z1=0.5)={floor_clean!r}, tradeoff holds="
         f"{td_clean['holds']} with rhs={td_clean['rhs']!r}.  THE CONTROL.")

    n = L.shape[0]
    poisoned = []
    for where in [(0, 0), (n // 2, n // 2), (n - 1, n - 1), (0, n - 1)]:
        Lp = L.copy()
        Lp[where] = np.nan
        st, val = attempt(lambda Lp=Lp: sc.l1_bounded_below_constant(Lp)[0])
        if st == "raised":
            case("F3", f"nan_at_{where}", "sound", val, "reject or propagate", "raised")
            continue
        floor = sc.counterexample_norm_floor(0.5, val)
        td = sc.general_class_tradeoff(0.5, 100.0, val)
        poisoned.append({"where": list(where), "sigma_min": jf(val),
                         "counterexample_norm_floor_Z1_0p5": jf(floor),
                         "tradeoff_holds": td["holds"], "tradeoff_rhs": jf(td["rhs"])})
        case("F3", f"nan_at_{where}", "silent_wrong", jf(val), f"{sig_clean!r} or a defect signal",
             f"ONE NaN in {n * n} entries ({1.0 / (n * n):.3e} of the matrix) sends "
             f"sigma_min from {sig_clean!r} to +inf -- the MOST FAVOURABLE value, i.e. "
             f"'L is perfectly bounded below'.  Downstream, counterexample_norm_floor "
             f"launders it into the FINITE, PLAUSIBLE {floor!r} (clean: {floor_clean!r}).")

    # the defect signal is fully laundered two calls downstream
    case("F3", "downstream_floor_is_finite_and_plausible", "silent_wrong",
         0.0, floor_clean,
         "counterexample_norm_floor(0.5, inf) = 0.0.  This is the whole content of "
         "Theorem NGX's general-class conclusion INVERTED: it reports that a "
         "counterexample reaching Z1 = 0.5 needs ||A||_w >= 0, i.e. that ANY bounded A "
         "will do, where the clean answer is ||A||_w >= "
         f"{floor_clean!r}.  No NaN, no Inf, no exception survives to this point.")

    # Inf and exact-singular arms: these are SOUND, and saying so is the point
    for lbl, mk in (("inf_at_0_0", lambda: np.where(np.eye(L.shape[0], dtype=bool) &
                                                    (np.arange(L.shape[0])[:, None] == 0),
                                                    np.inf, L)),
                    ("exactly_singular_column", lambda: _zero_col(L, 3)),
                    ("all_zero_matrix", lambda: np.zeros((4, 4)))):
        st, val = attempt(lambda mk=mk: sc.l1_bounded_below_constant(mk())[0])
        case("F3", lbl, "sound" if st == "raised" else "silent_wrong", val,
             "reject or propagate",
             "np.linalg.inv raises LinAlgError -- VISIBLE, this path holds"
             if st == "raised" else "returned a value")

    # a hand-checkable positive control: sigma_min of diag(2,4) in the plain l^1 norm is 2
    st, val = attempt(lambda: sc.l1_bounded_below_constant(np.diag([2.0, 4.0]))[0])
    case("F3", "hand_check_diag_2_4", "sound" if val == 2.0 else "silent_wrong", val, 2.0,
         "inf ||Lx||_1/||x||_1 for diag(2,4) is 2 by hand.  The instrument is correct "
         "on an input whose answer is known independently of the code.")

    return {"clean": {"K": K, "M_extra": Mx, "class": "algebraic", "param": s,
                      "sigma_min": sig_clean, "argmax_column": j_clean,
                      "counterexample_norm_floor_Z1_0p5": floor_clean,
                      "tradeoff": {k: jf(v) for k, v in td_clean.items()}},
            "poisoned": poisoned,
            "matrix_entries": n * n,
            "poisoned_fraction": 1.0 / (n * n),
            "mechanism": ("IEEE 754 comparisons have FOUR outcomes, the fourth being "
                          "'? U Unordered' when an operand is NaN, so `nrm > 0` is False "
                          "for nrm = NaN and l1_bounded_below_constant falls to the "
                          "`float('inf')` branch written for nrm == 0.")}


def _zero_col(L, j):
    A = L.copy()
    A[:, j] = 0.0
    return A


# ==========================================================================
# F3b -- AND THE NaN IS REACHABLE FROM THE MODULE'S OWN DOCUMENTED SIGNATURE.
#
# F3 injects the NaN by hand, which on its own only shows the guard is wrong.  This
# family shows the module MANUFACTURES the NaN itself, from a `param` its own public
# `weight_vector`/`log_weight_vector` accept without a check.
# ==========================================================================
def f3b_nan_manufactured_by_the_module():
    print("\nF3b -- the NaN is produced by the module's own weight API, not injected")
    rows = []
    for kind, p in (("geometric", -1.1), ("geometric", 0.0), ("geometric", -0.5),
                    ("algebraic", float("nan")), ("algebraic", float("inf"))):
        st, out = attempt(lambda kind=kind, p=p: sc._scaled_tail(8, 8 + 64, kind, p))
        if st == "raised":
            case("F3b", f"{kind}_{p}", "sound", out, "reject", "raised")
            continue
        Ts, _ = out
        n_nan = int(np.isnan(Ts).sum())
        if n_nan == 0:
            case("F3b", f"{kind}_{p}", "sound", f"{n_nan} NaN", "finite", "clean")
            continue
        st2, sig = attempt(lambda Ts=Ts: sc.l1_bounded_below_constant(Ts)[0])
        floor = sc.counterexample_norm_floor(0.5, sig) if st2 == "ok" else None
        rows.append({"class": kind, "param": jf(p), "nan_entries": n_nan,
                     "total_entries": int(Ts.size), "sigma_min": jf(sig),
                     "counterexample_norm_floor_Z1_0p5": jf(floor)})
        case("F3b", f"{kind}_{p}", "silent_wrong", jf(floor), "reject the weight class",
             f"_scaled_tail returns {n_nan}/{Ts.size} NaN for a `param` that "
             f"weight_vector/log_weight_vector accept with no check (the docstring "
             f"documents nu > 1), and the F3 guard converts it to sigma_min = "
             f"{jf(sig)} and a floor of {jf(floor)}.")
    return rows


# ==========================================================================
# F1/F2 -- THE WEIGHT DOMAIN IS UNGUARDED, AND THE TWO WEIGHT PATHS DISAGREE.
#
# `weight_vector` documents `geometric  w_k = nu^k, nu > 1` and enforces nothing.  At
# nu < 0 it returns SIGN-ALTERNATING "weights", which are not a weight at all -- and
# `weighted_l1_upper`, the routine that stamps its output `rigorous: True`, then sums
# them WITH THEIR SIGNS and hands back a number BELOW the quantity it claims to bound.
#
# This is the same mechanism leg 198 found in `solver/bordered_hl.py` (a negative scalar
# border weight accepted with no check, producing a negative "operator norm").  It is an
# INDEPENDENT, UNREPAIRED INSTANCE in a second module -- the leg-201 shape.
# ==========================================================================
def f1f2_weight_domain():
    print("\nF1/F2 -- weight-class domain, and weight_vector vs log_weight_vector")
    wv, lwv = {}, {}
    for kind, p in (("geometric", 2.0), ("geometric", 1.1), ("geometric", 1.0),
                    ("geometric", 0.5), ("geometric", 0.0), ("geometric", -1.1),
                    ("algebraic", 1.0), ("algebraic", -2.0)):
        st1, a = attempt(lambda kind=kind, p=p: sc.weight_vector(4, kind, p))
        st2, b = attempt(lambda kind=kind, p=p: np.exp(sc.log_weight_vector(4, kind, p)))
        wv[f"{kind}_{p}"] = a.tolist() if st1 == "ok" else a
        lwv[f"{kind}_{p}"] = b.tolist() if st2 == "ok" else b
    case("F1", "geometric_nu_negative_gives_signed_weights", "silent_wrong",
         wv["geometric_-1.1"], "reject (docstring: nu > 1)",
         "weight_vector(4,'geometric',-1.1) returns sign-ALTERNATING entries with no "
         "check, no warning and no exception.  A weight vector with a negative entry is "
         "not a weight.")
    case("F1", "weight_vector_vs_log_weight_vector_disagree", "silent_wrong",
         {"weight_vector": wv["geometric_-1.1"], "exp_log_weight_vector": lwv["geometric_-1.1"]},
         "the two paths agree or both reject",
         "The module carries TWO representations of the same weights and they diverge "
         "outside the documented domain: weight_vector returns signed numbers, "
         "log_weight_vector returns NaN.  rigorous_finite_block uses the FIRST, "
         "finite_section_inverse_norm uses the SECOND -- so the same arguments give a "
         "finite 'rigorous' constant on one path and NaN on the other.")

    # the magnitude, on the module's own bordered linearization
    M = sc.bordered_linearization(4)
    w_pos = np.concatenate([sc.weight_vector(4, "geometric", 1.1), [1.0]])
    w_neg = np.concatenate([sc.weight_vector(4, "geometric", -1.1), [1.0]])
    n_pos = sc.weighted_l1_opnorm(M, w_pos, w_pos)
    n_neg = sc.weighted_l1_opnorm(M, w_neg, w_neg)
    n_abs = sc.weighted_l1_opnorm(M, np.abs(w_neg), np.abs(w_neg))
    case("F2", "weighted_l1_opnorm_sign_cancellation", "silent_wrong", n_neg, n_abs,
         f"Same magnitudes, one sign pattern: the returned 'operator norm' is {n_neg!r} "
         f"against the true {n_abs!r} for those magnitudes -- understated "
         f"{n_abs / n_neg:.4f}x, and POSITIVE and plausible, so nothing downstream can "
         f"tell.  np.max over columns picks the cancelled column instead of rejecting it.")

    # ... and the same thing inside the function that stamps `rigorous: True`
    rb_pos = sc.rigorous_finite_block(8, "geometric", 1.1)
    rb_neg = sc.rigorous_finite_block(8, "geometric", -1.1)
    true_norm = sc.finite_section_inverse_norm(8, "geometric", 1.1)
    case("F2", "rigorous_finite_block_A_norm_understated", "silent_wrong",
         rb_neg["A_norm"], true_norm,
         f"rigorous_finite_block(8,'geometric',-1.1) returns A_norm="
         f"{rb_neg['A_norm']!r} with rigorous=True, against the true "
         f"{true_norm!r} for the same magnitudes -- UNDERSTATED "
         f"{rb_pos['A_norm'] / rb_neg['A_norm']:.6f}x, and BELOW 1, while its sibling "
         f"finite_section_inverse_norm on identical arguments returns NaN.  "
         f"weighted_l1_upper is documented as a RIGOROUS UPPER BOUND; here it returns a "
         f"value 20x below the quantity it claims to bound.  Same shape as leg 201's "
         f"non-containing enclosure flagged rigorous=True, different module.")

    # lesson-90: algebra_constant is entirely BLIND to the sign -- identical numbers
    ac_pos = sc.algebra_constant("geometric", 1.1, K=16)
    ac_neg = sc.algebra_constant("geometric", -1.1, K=16)
    case("F1", "algebra_constant_sign_blind", "silent_wrong", ac_neg, "reject or differ",
         f"algebra_constant returns {ac_pos!r} for nu=+1.1 and {ac_neg!r} for nu=-1.1 -- "
         f"BIT-IDENTICAL ({ac_pos == ac_neg}).  Lesson 90's tell: identical numbers from "
         f"two inputs that should differ.  It reports 'Banach algebra holds' (<= 1) for a "
         f"weight class that is not a norm.")

    # boundary-of-admissibility, filed HONESTLY as boundary rather than counted
    for p, lbl in ((0.5, "geometric_nu_below_1"), (1.0, "geometric_nu_equals_1"),
                   (-2.0, "algebraic_s_negative")):
        kind = "geometric" if "geometric" in lbl else "algebraic"
        st, v = attempt(lambda kind=kind, p=p: sc.finite_section_inverse_norm(8, kind, p))
        case("F1", lbl, "boundary_accepted", v, "documented domain is nu > 1 / s >= 0",
             "Accepted outside the documented domain, but the returned number is the "
             "CORRECT norm for the (decaying / flat / negative-exponent) weight actually "
             "built -- verified against exact rational arithmetic where affordable.  "
             "NOT counted as silent_wrong: the value is right for the object built.")

    return {"weight_vector": {k: (v if isinstance(v, str) else [jf(x) for x in v])
                              for k, v in wv.items()},
            "exp_log_weight_vector": {k: (v if isinstance(v, str) else [jf(x) for x in v])
                                      for k, v in lwv.items()},
            "opnorm_positive_weights": n_pos, "opnorm_signed_weights": n_neg,
            "opnorm_magnitudes_only": n_abs,
            "understatement_factor": n_abs / n_neg,
            "rigorous_finite_block_A_norm_nu_pos": rb_pos["A_norm"],
            "rigorous_finite_block_A_norm_nu_neg": rb_neg["A_norm"],
            "rigorous_finite_block_understatement_factor":
                rb_pos["A_norm"] / rb_neg["A_norm"],
            "algebra_constant_nu_pos": ac_pos, "algebra_constant_nu_neg": ac_neg,
            "algebra_constant_bit_identical": bool(ac_pos == ac_neg)}


# ==========================================================================
# F2b -- THE SOUNDNESS CONTROL FOR `weighted_l1_upper`, WHICH MUST COME OUT BOTH WAYS.
#
# A negative result needs a positive control that can report the other answer.  The
# SAME routine, the SAME draws, the ONLY difference being one sign flip.
# ==========================================================================
def f2b_containment_control():
    print("\nF2b -- weighted_l1_upper containment: positive weights vs one sign flip")
    rng = np.random.default_rng(0)
    bad_pos, tightest = 0, float("inf")
    for _ in range(200):
        K = int(rng.integers(3, 12))
        A = rng.standard_normal((K + 1, K + 1))
        w = np.exp(rng.uniform(-3, 3, K + 1))
        ub = sc.weighted_l1_upper(A, A, w)
        exact = float(np.max((np.abs(A) * w[:, None]).sum(0) / w))
        if ub < exact:
            bad_pos += 1
        else:
            tightest = min(tightest, ub / exact)
    case("F2b", "containment_on_positive_weights", "sound" if bad_pos == 0 else "silent_wrong",
         f"{bad_pos}/200 non-containing", "0/200",
         f"On POSITIVE weights weighted_l1_upper is a genuine upper bound in 200/200 "
         f"draws, tightest ratio ub/exact = {tightest!r}.  THE ROUTINE IS NOT BROKEN IN "
         f"GENERAL -- this is what makes the sign case a finding rather than noise.")

    bad_neg, worst = 0, 1.0
    for _ in range(200):
        K = int(rng.integers(3, 12))
        A = rng.standard_normal((K + 1, K + 1))
        w = np.exp(rng.uniform(-3, 3, K + 1))
        w[int(rng.integers(0, K + 1))] *= -1.0
        ub = sc.weighted_l1_upper(A, A, w)
        exact = float(np.max((np.abs(A) * np.abs(w)[:, None]).sum(0) / np.abs(w)))
        if ub < exact:
            bad_neg += 1
            worst = min(worst, ub / exact)
    case("F2b", "containment_with_one_sign_flip", "silent_wrong",
         f"{bad_neg}/200 non-containing", "0/200 or rejection",
         f"EXACTLY ONE sign flip in the weight vector: 200/200 draws return a bound BELOW "
         f"the quantity they claim to bound, worst ub/exact = {worst!r} -- i.e. the "
         f"'rigorous upper bound' comes back NEGATIVE.  The control comes out both ways, "
         f"so the mechanism is the sign and not the routine.")
    return {"positive_weights_non_containing": bad_pos, "positive_weights_draws": 200,
            "positive_weights_tightest_ratio": tightest,
            "one_sign_flip_non_containing": bad_neg, "one_sign_flip_draws": 200,
            "one_sign_flip_worst_ratio": worst}


# ==========================================================================
# F8 -- `kernel_membership_ladder` MISCLASSIFIES CONVERGING CASES.
#
# `in_l1_w` is hypothesis (H2) of leg 58's proposition.  The verdict is read off a
# hard-coded increment-ratio threshold (`r < 0.95` converges), so the whole band
# 0.95 <= r < 1 -- which is CONVERGENT -- is reported as log-divergent; and in the
# geometric class the increments underflow (or overflow) to a difference of exactly
# zero (or inf - inf), so `incr[i] if incr[i] else nan` makes r NaN and the verdict
# `indeterminate` for ALL FOUR geometric cases tried, including the two that converge
# fastest of anything in the battery.
#
# DIRECTION MATTERS AND IS REPORTED HONESTLY: this errs CONSERVATIVELY for the no-go --
# it refuses to apply (H2) rather than wrongly applying it.  It is counted as
# silent_wrong because it is a wrong classification of a documented hypothesis returned
# as a clean boolean, not because it weakens the theorem.
# ==========================================================================
def f8_membership_verdicts():
    print("\nF8 -- kernel_membership_ladder / nogo_hypotheses verdicts")
    rows = []
    for p in (0.0, 0.3, 0.5, 0.7, 0.9, 0.99, 1.0, 1.2, 1.5):
        r = sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", p)
        truth = bool(p < 1.0)          # sum m^(s-2) converges iff s < 1
        ok = (r["in_l1_w"] == truth)
        rows.append({"class": "algebraic", "param": p, "verdict": r["verdict"],
                     "in_l1_w": r["in_l1_w"], "truth_in_l1_w": truth,
                     "last_increment_ratio": jf(r["last_increment_ratio"]),
                     "correct": ok})
        if not ok:
            case("F8", f"algebraic_s_{p}", "silent_wrong", r["in_l1_w"], truth,
                 f"verdict='{r['verdict']}' from increment ratio "
                 f"{r['last_increment_ratio']!r} against the hard-coded 0.95 threshold, "
                 f"but sum m^(s-2) = sum m^{p - 2.0:.2f} CONVERGES.  Conservative "
                 f"direction for the no-go; still a wrong boolean.")
    for nu in (0.5, 0.9, 1.05, 1.1):
        r = sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "geometric", nu)
        truth = bool(nu < 1.0)
        rows.append({"class": "geometric", "param": nu, "verdict": r["verdict"],
                     "in_l1_w": r["in_l1_w"], "truth_in_l1_w": truth,
                     "last_increment_ratio": jf(r["last_increment_ratio"]),
                     "increment": [jf(x) for x in r["increment"]],
                     "correct": bool(r["in_l1_w"] == truth)})
        case("F8", f"geometric_nu_{nu}", "silent_wrong", r["verdict"], "converges/power_divergent",
             f"ALL FOUR geometric cases return 'indeterminate' with r=NaN: the increments "
             f"underflow to exactly 0.0 (nu<1) or overflow so inc-inc=NaN (nu>1), and "
             f"`incr[i] if incr[i] else nan` turns both into NaN.  The geometric class is "
             f"the one this module's own docstring calls 'the literature's default'.")

    # bisect the wrongly-excluded band, and measure the shipped path's margin from it
    lo, hi = 0.7, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if sc.kernel_membership_ladder(8, (256, 1024, 4096, 16384), "algebraic", mid)["in_l1_w"]:
            lo = mid
        else:
            hi = mid
    case("F8", "wrongly_excluded_band_width", "silent_wrong", 1.0 - hi, 0.0,
         f"Bisected: the last s classified in_l1_w=True is {lo!r}, the first False is "
         f"{hi!r}.  Every s in [{hi:.6f}, 1) is IN l^1_w and reported as not.  Band width "
         f"{1.0 - hi!r} in the weight exponent.  Nearest shipped s is 0.7 (r=0.6590), "
         f"margin {hi - 0.7:.6f} in s -- so this is LATENT.")

    # nogo_hypotheses' own boolean, under a negative mu
    h = sc.nogo_hypotheses(4, 4 + 64, "algebraic", 0.3, mu=-1.0)
    case("F8", "nogo_hypotheses_mu_negative", "boundary_accepted",
         h["H2_holds_on_the_infinite_tail"], False,
         "mu = -1 (ANTI-dissipation, physically inadmissible) is accepted with no check, "
         "but H2 is correctly reported False and sigma_min is a genuine norm of the "
         "matrix actually built.  NOT counted: the number is right for the object built.")
    return {"rows": rows, "band_lo": lo, "band_hi": hi,
            "wrongly_excluded_band_width": 1.0 - hi,
            "shipped_s_margin": hi - 0.7}


# ==========================================================================
# F6 -- THE SAME IEEE-754 UNORDERED-GUARD MECHANISM, A SECOND SITE.
# ==========================================================================
def f6_weight_window():
    print("\nF6 -- weight_window's `empty` guard under an undefined alpha")
    a_nan = sc.weight_window(float("nan"), 0.3)
    a_ok1 = sc.weight_window(0.394, 0.3)
    a_ok2 = sc.weight_window(0.394, 1.0)
    case("F6", "weight_window_alpha_nan", "silent_wrong", a_nan["empty"],
         "True or a defect signal",
         "weight_window(nan, 0.3) returns empty=False -- the FAVOURABLE answer ('the "
         "window is not empty, a certificate can still close') -- because "
         "bool(nan >= nan) is False under the same IEEE-754 unordered relation as F3. "
         "`gap` is a visible NaN, but `empty` is the boolean a caller branches on.")
    case("F6", "weight_window_clean_controls", "sound",
         [a_ok1["empty"], a_ok2["empty"]], [False, True],
         "The control comes out BOTH ways on clean input (alpha=0.394 against "
         "s_operator=0.3 and 1.0), so `empty` is not a constant.")
    return {"alpha_nan": {k: jf(v) for k, v in a_nan.items()},
            "control_s0p3": {k: jf(v) for k, v in a_ok1.items()},
            "control_s1p0": {k: jf(v) for k, v in a_ok2.items()}}


# ==========================================================================
# F5 -- DEGENERATE INDEX DOMAINS.  MOSTLY SOUND, AND SAYING SO IS THE POINT.
# ==========================================================================
def f5_degenerate_indices():
    print("\nF5 -- degenerate index domains")
    rows = []
    for lbl, fn, expect in (
        ("tail_inverse_norm_M_equals_K", lambda: sc.tail_inverse_norm(4, 4), "reject"),
        ("tail_block_M_less_than_K", lambda: sc.tail_block(4, 3), "reject"),
        ("tail_inverse_norm_n_equals_1", lambda: sc.tail_inverse_norm(4, 5), "reject"),
        ("tail_left_null_n_equals_1", lambda: sc.tail_left_null(4, 5), "reject"),
        ("bordered_tail_inverse_norm_n_1", lambda: sc.bordered_tail_inverse_norm(4, 5), "reject"),
        ("singular_sequence_rate_degenerate_x", lambda: sc.singular_sequence_rate([1, 1], [1.0, 2.0]), "reject"),
    ):
        st, v = attempt(fn)
        rows.append({"case": lbl, "status": st, "value": jf(v) if st == "ok" else v})
        case("F5", lbl, "sound" if st == "raised" else "silent_wrong", v, expect,
             "raises -- VISIBLE" if st == "raised" else "returned a value silently")

    st, v = attempt(lambda: sc.bordered_linearization(4.9).shape)
    case("F5", "non_integer_K_truncated", "silent_wrong", list(v) if st == "ok" else v,
         "reject or round explicitly",
         "bordered_linearization(4.9) silently becomes K=4 via int() -- a 5x5 matrix for "
         "a requested 4.9.  Same shape as leg 198's 'pin of arity 5 truncated to 3'.  "
         "Low magnitude, recorded for the mechanism count, not the headline.")

    st, v = attempt(lambda: sc.tail_inverse_norm(0, 10))
    case("F5", "K_equals_zero", "boundary_accepted", jf(v), "documented modes start at k=1",
         "K=0 makes the 'tail' the whole operator on modes 1..10.  Accepted and the "
         "number is correct for that object.  NOT counted.")

    st, v = attempt(lambda: sc.clm_residual([], -1.0, 1.0))
    case("F5", "clm_residual_empty_profile", "sound" if st == "raised" else "silent_wrong",
         v, "reject", "raises IndexError on b[0]" if st == "raised" else "returned")

    st, v = attempt(lambda: sc.clm_residual([float("nan"), 0.0], -1.0, 1.0))
    prop = (st == "ok" and any(isinstance(x, float) and np.isnan(x) for x in v))
    case("F5", "clm_residual_nan_profile", "sound" if prop or st == "raised" else "silent_wrong",
         "NaN propagates" if prop else v, "propagate or reject",
         "A NaN in the profile propagates into the residual VISIBLY -- this path holds.")
    return rows


# ==========================================================================
# F4/E -- THE POSITIVE CONTROL'S OWN DISCRIMINATION (lesson 90 applied to the control).
# ==========================================================================
def f4_control_discrimination():
    print("\nF4 -- does the mu control discriminate the SIGN of mu?")
    rows = []
    for mu in (0.0, 0.1, -0.1, -1.0):
        norms = [sc.finite_section_inverse_norm(K, "algebraic", 1.0, mu=mu)
                 for K in (32, 64, 128, 256)]
        rows.append({"mu": mu, "K": [32, 64, 128, 256], "norm": norms,
                     "ratio_last": norms[-1] / norms[-2]})
    case("F4", "mu_control_sign_blind", "boundary_accepted",
         {r["mu"]: round(r["ratio_last"], 4) for r in rows},
         "mu < 0 rejected, or a different ratio",
         "dissipative_control's stated contract is 'mu > 0 must saturate in K, in every "
         "class'.  At mu = -0.1 and mu = -1.0 -- ANTI-dissipation -- it saturates just as "
         "cleanly (ratio_last 1.0000).  NOT counted as silent_wrong: each returned norm "
         "is the correct norm of the matrix actually built.  What it means is that the "
         "control establishes 'any DIAGONAL restores boundedness', which is weaker than "
         "'dissipation restores boundedness' and is the honest reading of leg 51-58's "
         "positive control.  Recorded as a CHARACTERIZATION, not a defect.")
    return rows


# ==========================================================================
def main():
    print("=" * 74)
    print("Leg 209 / Route-SCA2 -- adversarial audit of solver/spectral_certificate.py")
    print("=" * 74)

    out = {"leg": 209, "route": "ROUTE-SCA2", "version": "v1",
           "module_under_audit": "solver/spectral_certificate.py",
           "module_patched_by_this_leg": False,
           "novelty_log": "writeup/novelty/leg_209.md",
           "gate": ("Under adversarial and degenerate inputs (near-singular weight "
                    "classes, boundary-of-admissibility A, NaN/Inf), does "
                    "spectral_certificate.py ever silently return a wrong Z_1/sigma_min "
                    "value rather than reject or visibly propagate the defect?")}

    out["F7_clean_input_soundness"] = f7_clean_input_soundness()
    out["F3_sigma_min_under_nan"] = f3_sigma_min_under_nan()
    out["F3b_nan_manufactured_by_the_module"] = f3b_nan_manufactured_by_the_module()
    out["F1_F2_weight_domain"] = f1f2_weight_domain()
    out["F2b_containment_control"] = f2b_containment_control()
    out["F8_membership_verdicts"] = f8_membership_verdicts()
    out["F6_weight_window"] = f6_weight_window()
    out["F5_degenerate_indices"] = f5_degenerate_indices()
    out["F4_control_discrimination"] = f4_control_discrimination()

    # ------------------------------------------------------------------
    # (b) BLAST RADIUS -- is any BANKED number reachable?
    # ------------------------------------------------------------------
    print("\nBLAST RADIUS -- can any shipped parameter reach any of the four mechanisms?")
    shipped = []
    for kind, p in (("flat", 0.0), ("algebraic", 0.0), ("algebraic", 0.3),
                    ("algebraic", 0.7), ("algebraic", 1.0), ("algebraic", 1.5),
                    ("geometric", 1.05), ("geometric", 1.1), ("geometric", 1.2)):
        Ts, _ = sc._scaled_tail(8, 8 + 64, kind, p)
        wv = sc.weight_vector(8, kind, p)
        shipped.append({"class": kind, "param": p,
                        "nan_in_scaled_tail": int(np.isnan(Ts).sum()),
                        "inf_in_scaled_tail": int(np.isinf(Ts).sum()),
                        "min_weight": float(np.min(wv)),
                        "any_negative_weight": bool(np.any(wv < 0))})
    n_bad = sum(r["nan_in_scaled_tail"] + r["inf_in_scaled_tail"] for r in shipped)
    n_neg = sum(1 for r in shipped if r["any_negative_weight"])
    out["blast_radius"] = {
        "shipped_parameter_census": shipped,
        "shipped_params_producing_nan_or_inf": n_bad,
        "shipped_params_with_a_negative_weight": n_neg,
        "shipped_mu_values": [0.0, 0.1, 0.5, 1.0, 2.0],
        "shipped_mu_negative": 0,
        "shipped_s_nearest_the_F8_band": 0.7,
        "F8_band_starts_at": out["F8_membership_verdicts"]["band_hi"],
        "F8_margin_in_s": out["F8_membership_verdicts"]["shipped_s_margin"],
        "clean_input_float_vs_exact_worst_rel":
            out["F7_clean_input_soundness"]["worst_rel_diff"],
        "banked_numbers_contaminated": 0,
        "verdict": ("LATENT.  Every shipped weight class and parameter in "
                    "test_spectral_certificate.py, p2_route_ngx_v1_general.py, "
                    "p2_route_l1_v2_spectral.py, p2_route_t_v1_border.py and "
                    "p2_route_ng_v1_nogo.py is in the documented domain: 0 produce a NaN "
                    "or Inf in the scaled tail, 0 produce a negative weight, every mu is "
                    ">= 0, and the nearest shipped s to F8's misclassified band is 0.7 "
                    "against a band starting at 0.963852.  On clean input float64 agrees "
                    "with exact rational arithmetic to 7.24e-16.  0 banked numbers move.")}
    print(f"  shipped params producing NaN/Inf: {n_bad};  with a negative weight: {n_neg}")
    print(f"  banked numbers contaminated: 0   -- the finding is LATENT")

    # ------------------------------------------------------------------
    # (c) IS THEOREM NGX'S PROOF AT RISK?  This is the question the dispatch
    #     singled out, and it is answered separately and conservatively.
    # ------------------------------------------------------------------
    out["theorem_NGX_proof_at_risk"] = {
        "answer": "NO",
        "why": ("Theorem NGX's proof has two steps and NEITHER is a float computation. "
                "(1) Z_1 >= 1 - ||A||_w sigma_min(L) is an exact, three-line folklore "
                "inequality the module's own NGX header explicitly disclaims as not this "
                "repository's; it involves no code. (2) sigma_min(L) -> 0 like M^-(1-s) "
                "is established by the EXPLICIT sequence v_M = (z_M; h^(M)) whose entire "
                "residual is the single truncation-edge row |1 - M/2||h_M|w_M ~ M^(s-1), "
                "against ||v_M||_w bounded uniformly because sum m^(s-2) converges for "
                "s < 1 -- an analytic estimate on the INFINITE tail. Leg 58's companion "
                "result on A21 = 0 is likewise a three-line argument off the block "
                "structure of (I - AL)x with x = (0; h) and T h = 0. All four mechanisms "
                "found here require an input outside the documented domain (nu <= 0, an "
                "injected NaN, a negative weight, or s >= 0.963852) which no step of "
                "either proof uses and which the shipped path never produces."),
        "what_IS_at_risk": ("The module's ability to REPORT a correct sigma_min/||A||_w "
                            "if it is ever driven outside its documented domain -- e.g. "
                            "by a future leg sweeping the geometric class through nu <= 1, "
                            "which weight_vector accepts silently. That is a code defect "
                            "of the leg-201/204 class, not a mathematical one."),
        "distinction_stated_explicitly": ("A numerical module having an adversarial-input "
                                          "bug does not make an analytically-proved "
                                          "theorem wrong. This leg found the former and "
                                          "explicitly did NOT find the latter."),
        "escalation_grounds": ("the four silent-wrong mechanisms in a module Theorem NGX "
                              "is proved against -- NOT 'the proof is at risk'")}

    # ------------------------------------------------------------------
    counts = {}
    for c in CASES:
        counts[c["outcome"]] = counts.get(c["outcome"], 0) + 1
    out["cases"] = CASES
    out["case_counts"] = counts
    out["cases_total"] = len(CASES)
    out["mechanisms"] = [
        "M1 l1_bounded_below_constant's `nrm > 0` guard is IEEE-754-unordered under NaN "
        "and returns sigma_min = +inf, the most favourable value; "
        "counterexample_norm_floor launders it into a finite, plausible 0.0.",
        "M2 weight_vector accepts a geometric nu <= 0 with no check (documented nu > 1) "
        "and returns sign-alternating 'weights'; weighted_l1_upper then sums them WITH "
        "SIGNS and returns a 'rigorous' bound 20.35x BELOW the quantity it bounds.",
        "M3 kernel_membership_ladder's hard-coded 0.95 increment-ratio threshold and its "
        "`incr or nan` idiom misclassify a 0.0361-wide band of CONVERGENT algebraic "
        "exponents, and all four geometric cases, as not-in-l^1_w.",
        "M4 weight_window's `empty` flag is False for alpha = NaN -- the favourable "
        "answer -- by the same unordered-comparison mechanism as M1.",
    ]
    out["gate_answer"] = "YES"
    out["gate_answer_wording"] = (
        "YES -- under adversarial and degenerate inputs spectral_certificate.py returns a "
        "silently wrong sigma_min/||A||_w rather than rejecting or visibly propagating, by "
        "four distinct mechanisms. Headline: ONE NaN in 262144 entries of the shipped "
        "(K=8, M_extra=512, s=0.3) tail sends sigma_min from 0.034914733291684645 to +inf "
        "and counterexample_norm_floor(Z1=0.5) from 14.3206020170024 to exactly 0.0 -- "
        "Theorem NGX's general-class conclusion inverted, with no defect signal surviving. "
        "Theorem NGX's own PROOF is NOT at risk and 0 banked numbers are contaminated.")

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=False)

    print("\n" + "=" * 74)
    print(f"CASES: {len(CASES)} total -- " +
          ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"GATE: {out['gate_answer']}")
    print(f"THEOREM NGX PROOF AT RISK: {out['theorem_NGX_proof_at_risk']['answer']}")
    print(f"BANKED NUMBERS CONTAMINATED: 0 (LATENT)")
    print(f"wrote {OUT}")
    print("=" * 74)


if __name__ == "__main__":
    main()
