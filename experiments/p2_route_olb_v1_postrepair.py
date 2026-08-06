"""Route-OLB v1 -- INDEPENDENT POST-REPAIR REGRESSION RE-RUN of solver/op_lower.py.

THE GATE (leg 132, DIRECTION.md), quoted verbatim:

  Post-repair, does solver/op_lower.py (a) return a true lower bound (L <= N_true)
  on every one of leg 101's 209 original adversarial cases in an independent
  re-run, and (b) reproduce the 307.878-decade headroom and every other validated
  magnitude to the digit?
    yes -> Repair confirmed sound and non-regressive by an independent run.  Bank
           the 209-case battery as a permanent regression suite.
    no  -> An incomplete fix or a repair regression.  Report the exact case
           precisely; escalate as a priority finding, do not patch under this
           leg's own authority.

WHY THIS FILE EXISTS AT ALL, GIVEN THAT LEG 101'S RUNNER ALREADY RE-RAN.
`experiments/p2_route_ola_v1_adversarial.py` was written by the leg that found
the bug and re-run by the branch that fixed it, and it grades against a reference
that lives in the same file.  A defect shared between the reference and the fix
is invisible to it.  `experiments/p2_route_ola_v1_bench_check.py` grades the
non-regression clause against `PRE`, a dict of LITERALS the repair itself wrote.
So the two magnitudes the repair rests on -- "0 violations of 209" and "the
pre-repair numbers moved down by 1.6e-12" -- are, as banked, self-reported.

This runner imports NEITHER of them.  Four strands, all re-derived from the
specification rather than from the artifact under test:

  S1  the 209-case battery, zoo rebuilt from leg 101's documented specification.
      The case counts (408 / 209 / 199) are themselves a gate magnitude: a
      different count means this is not the same battery.
  S2  an INDEPENDENTLY DERIVED exact reference.  Leg 101 used the closed form
      N = max_{i,j} t_i |A_ij| / u_j.  This file ENUMERATES the extreme points
      +-e_j/u_j of the weighted-l1 ball, forms A g and takes the exact weighted
      sup, all in Fraction -- same theorem, different derivation, and it
      validates the closed form instead of assuming it.  Both routes are computed
      and their disagreement is reported as a magnitude.
  S3  the PRE-REPAIR module, reconstructed from git (`ef0ea2e:solver/op_lower.py`,
      the last commit before the repair `147e8c2`) and imported alongside the
      current one, so 47 -> 0 and the `PRE` literals become MEASUREMENTS.
      Nothing is written into the repository tree; solver/op_lower.py is untouched.
  S4  the known-answer line -- ALL SEVEN banked v10 rows (w1_ladder J =
      200/400/800/1600 at alpha=1.5,gamma=0.5; w2_operating J = 200/400/800 at
      alpha=1.4,gamma=0.15), which is a wider net than the bench check's three J
      at one (alpha,gamma) -- plus the 307.878-decade headroom.

THE POSITIVE CONTROL THAT CAN REPORT THE OTHER ANSWER (lesson 90).  The
pre-repair module is pushed through the SAME grader and MUST report 47
violations.  If both modules report 0, the grader is broken and this run says so
rather than claiming a pass.  Symmetrically, S2's two reference routes
disagreeing would indict the reference, not the module.

DECISION RULE, pre-committed in writeup/novelty/leg_132.md sec 3 before any
number was re-measured:

  (a) SOUNDNESS: over the 209 gate-deciding cases, records with L > N_true at ANY
      number of ULP must be 0.  L = 0 against a large N_true is a PASS (weak,
      true).  A raised exception is a PASS.  A case whose reference is not
      computable is OUT OF SCOPE by the gate's own words and is counted.
  (b) NON-REGRESSION: headroom decades move by EXACTLY 0; the seven banked v10
      `lower` and `sign_patterns` rows move DOWN ONLY by <= 1e-9 relative; the
      seven `argmax` are unchanged exactly; `rejected`/`saturated` are 0 on every
      production row; the battery counts are 408/209/199 exactly.

  REGRESSION := any magnitude moving UP, or DOWN by more than its budget, or an
  argmax/count changing.  ADMISSIBLE DEFLATION := L_post <= L_pre AND
  L_post <= N_true, within budget.  The asymmetry is DIRECTION.md's, not this
  leg's.

solver/op_lower.py is READ-ONLY under BOTH branches of the gate.

Run: .venv/bin/python experiments/p2_route_olb_v1_postrepair.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import warnings
from fractions import Fraction

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

import solver.op_lower as POST                                     # noqa: E402

#: the last commit before the bench repair `147e8c2`
PRE_COMMIT = "ef0ea2e"

N = 48                           # operator dimension for the zoo
KW = dict(n_centre=12, n_step=12)
ASCENT_ITERS = 200
BUDGET = 1e-9                    # the repair's own non-regression budget

#: leg 101's banked battery shape.  A different count means a different battery.
EXPECT_TOTAL, EXPECT_DECIDING, EXPECT_EXCLUDED = 408, 209, 199
#: The pre-repair violation counts the positive control must reproduce, under
#: BOTH grading rules -- because they are different rules and they give different
#: numbers, and quoting one against the other would be exactly the kind of
#: instrument confusion this leg exists to catch.
#:
#:   leg 101's rule: an exceedance counts only if it is more than ONE ULP of the
#:     returned float AND more than 1e-9 relative.  The one-ULP concession was a
#:     grading allowance for correct rounding in the denormal range.  -> 47.
#:   this leg's rule (sec 3 of the novelty pass, matching the repair's own
#:     pre-committed clause): ANY exceedance of the exact norm counts, 0 ULP.
#:     -> 47 + the 3 cases leg 101 excused as `sound_within_one_ulp` = 50.
#:
#: The overflow class is identical under both (46), since `inf` against a finite
#: norm is not a rounding question.
EXPECT_PRE_VIOLATIONS_LEG101 = 47
EXPECT_PRE_VIOLATIONS_0ULP = 50
EXPECT_PRE_OVERFLOW = 46


# ---------------------------------------------------------------------------
# S3 -- the pre-repair module, reconstructed from git rather than quoted
# ---------------------------------------------------------------------------
def load_pre_repair(commit=PRE_COMMIT):
    """Import `<commit>:solver/op_lower.py` under its own name.

    Written to a temp file OUTSIDE the repository tree: this leg edits no solver
    module and adds no file to the working tree.
    """
    src = subprocess.check_output(
        ["git", "show", "%s:solver/op_lower.py" % commit], cwd=_ROOT)
    fd, path = tempfile.mkstemp(suffix="_op_lower_pre.py")
    with os.fdopen(fd, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("op_lower_pre", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.__source_sha__ = subprocess.check_output(
        ["git", "rev-parse", "%s:solver/op_lower.py" % commit],
        cwd=_ROOT).decode().strip()
    mod.__source_path__ = path
    return mod


# ---------------------------------------------------------------------------
# duck-typed norms whose induced operator norm is EXACTLY computable
# ---------------------------------------------------------------------------
class WeightedL1:
    """||g|| = sum_j u_j |g_j|."""

    def __init__(self, u):
        self.u = np.asarray(u, dtype=float)
        self.w = self.u

    def __call__(self, g):
        return float(np.sum(self.u * np.abs(np.asarray(g, dtype=float))))


class WeightedLinf:
    """||v|| = max_i t_i |v_i|."""

    def __init__(self, t):
        self.t = np.asarray(t, dtype=float)
        self.w = self.t

    def __call__(self, v):
        return float(np.max(self.t * np.abs(np.asarray(v, dtype=float))))


class WeightedL2:
    """||v|| = ||t*v||_2."""

    def __init__(self, t):
        self.t = np.asarray(t, dtype=float)
        self.w = self.t

    def __call__(self, v):
        return float(np.sqrt(np.sum((self.t * np.asarray(v, dtype=float)) ** 2)))


# ---------------------------------------------------------------------------
# S2 -- the reference, derived independently of leg 101's closed form
# ---------------------------------------------------------------------------
def _restrict(A, u, restricted):
    """op_lower forces g[0] = 0, so column 0 is deleted for the gate reference."""
    return (A[:, 1:], u[1:]) if restricted else (A, u)


def _reference_computable(B, t, uu):
    if B.size == 0:
        return False
    if not (np.all(np.isfinite(B)) and np.all(np.isfinite(t))
            and np.all(np.isfinite(uu))):
        return False
    if np.any(uu == 0.0):
        return False                       # a zero codomain weight: unbounded
    return True


def ref_l1_linf_extreme_points(A, t, u, restricted):
    """EXACT induced l1(u) -> linf(t) norm, by ENUMERATING the ball's extreme points.

    The extreme points of {g : sum_j u_j |g_j| <= 1} are +- e_j / u_j.  For each
    one, `A g` is the j-th column divided by u_j, and its weighted-sup norm is
    max_i t_i |A_ij| / u_j.  The maximum over j is the induced norm.

    This is deliberately NOT leg 101's closed form `max_{i,j} t_i |A_ij| / u_j`
    written out again: the sup over i is taken as an inner maximisation over an
    explicitly constructed image vector, so a mistake in the closed form's index
    conventions would show up as a disagreement rather than being inherited.
    All arithmetic is Fraction, hence exact -- the same expression in float64
    UNDERFLOWS to 0.0 on the denormal cases, i.e. a naive reference is wrong
    exactly where the audit is sharpest.

    Returns a Fraction, or None when the reference is not computable.
    """
    B, uu = _restrict(A, u, restricted)
    if B.size == 0:
        return Fraction(0)
    if not _reference_computable(B, t, uu):
        return None
    ta = [Fraction(float(x)) for x in t]
    ua = [Fraction(float(x)) for x in uu]
    best = Fraction(0)
    for j in range(B.shape[1]):
        col = B[:, j]
        nz = np.nonzero(col)[0]
        if nz.size == 0:
            continue
        inv_uj = 1 / ua[j]
        # the image of the extreme point e_j / u_j, one nonzero component at a time
        sup_j = Fraction(0)
        for i in nz:
            v = ta[i] * Fraction(abs(float(col[i]))) * inv_uj
            if v > sup_j:
                sup_j = v
        if sup_j > best:
            best = sup_j
    return best


def ref_l1_linf_closed_form(A, t, u, restricted):
    """Leg 101's closed form, kept ONLY as a cross-check of the above (S2)."""
    B, uu = _restrict(A, u, restricted)
    if B.size == 0:
        return Fraction(0)
    if not _reference_computable(B, t, uu):
        return None
    ta = [Fraction(float(x)) for x in t]
    ua = [Fraction(float(x)) for x in uu]
    best = Fraction(0)
    for i in range(B.shape[0]):
        if ta[i] == 0:
            continue
        row = B[i]
        for j in np.nonzero(row)[0]:
            v = ta[i] * Fraction(abs(float(row[j]))) / ua[j]
            if v > best:
                best = v
    return best


def _pow2(x):
    fin = np.abs(x)[np.isfinite(x)]
    m = float(fin.max()) if fin.size else 0.0
    if m == 0.0:
        return np.asarray(x, dtype=float), 0
    e = int(np.frexp(m)[1])
    return np.ldexp(np.asarray(x, dtype=float), -e), e


def ref_l2_l2(A, t, u, restricted):
    """sigma_max(diag(t) A diag(u)^-1) from eigvalsh(M^T M) -- NOT svd.

    A different LAPACK path from leg 101's `svd`, on a power-of-two-rescaled
    matrix (exact in binary floating point, so it neither creates nor destroys
    information).  Float, ~1e-13 relative, NOT exact -- so per leg 101's own
    pre-committed rule this reference may decide only the OVERFLOW class; any
    finite exceedance it sees is reported unconfirmed and the gate is decided on
    the exact l1->linf reference.
    """
    B, uu = _restrict(A, u, restricted)
    if B.size == 0:
        return Fraction(0)
    if not _reference_computable(B, t, uu):
        return None
    B2, eB = _pow2(B)
    t2, et = _pow2(t)
    u2, eu = _pow2(uu)
    M = (t2[:, None] * B2) / u2[None, :]
    if not np.all(np.isfinite(M)):
        return None
    # The Gram matrix SQUARES M, so it dies a full factor of two in exponent
    # sooner than M does -- on this zoo `M` reaches ~1e300 and `M^T M` overflows
    # to inf on 7 operators where leg 101's `svd(M)` is perfectly happy.  That is
    # a defect of THIS reference, not of the module under test, and it excluded
    # 16 cases from the battery on the first run.  One more exact power-of-two
    # rescale of M itself fixes it; the exponent is carried in the return.
    M2, eM = _pow2(M)
    G = M2.T @ M2
    if not np.all(np.isfinite(G)):
        return None
    try:
        lam = float(np.linalg.eigvalsh(G)[-1])
    except np.linalg.LinAlgError:
        return None
    if lam <= 0.0:
        return Fraction(0)
    return (Fraction(float(np.sqrt(lam)))
            * Fraction(2) ** (eB + et - eu + eM))


# ---------------------------------------------------------------------------
# S1 -- the zoo, rebuilt from leg 101's documented specification
# ---------------------------------------------------------------------------
def operator_zoo(n=N, seed=7):
    rng = np.random.default_rng(seed)
    G = rng.normal(size=(n, n))
    out = []

    def add(name, A, note):
        out.append({"name": name, "A": np.asarray(A, dtype=float), "note": note})

    add("benign_random", G.copy(), "control: well-formed dense Gaussian")
    i, j = np.arange(n), np.arange(n)
    add("hilbert", 1.0 / (i[:, None] + j[None, :] + 1.0),
        "ill-conditioned control")
    M = np.eye(n)
    M[3, 3] = 1e-13
    add("near_singular_inverse", np.linalg.inv(M), "one 1e-13 pivot -> a 1e13 entry")
    add("near_defective", np.eye(n) * 1e-12 + np.diag(np.ones(n - 1), 1),
        "near-defective Jordan block")
    add("rank1", np.outer(G[:, 0], G[0, :]), "rank-deficient (rank 1)")
    add("zero", np.zeros((n, n)), "the zero operator")
    Z = G.copy()
    Z[:, 0] = 0.0
    add("zero_col0", Z, "the gauge column is zero")
    Zr = G.copy()
    Zr[5, :] = 0.0
    add("zero_row", Zr, "one zero row")
    P = G.copy()
    P[5, 7] = np.nan
    add("nan_entry", P, "a single NaN in a generic entry")
    P = G.copy()
    P[:, 0] = np.nan
    add("nan_col0", P, "the whole GAUGE column is NaN")
    P = G.copy()
    P[3, :] = np.nan
    add("nan_row", P, "a whole row is NaN")
    P = G.copy()
    P[9, 11] = np.inf
    add("inf_entry", P, "a single +inf")
    P = G.copy()
    P[4, :] = -np.inf
    add("neg_inf_row", P, "a whole row is -inf")
    add("huge_1e300", G * 1e300, "entries ~1e300")
    P = G.copy() * 1e-300
    P[:, 3] *= 1e300
    add("mixed_scale", P, "1e-300 background with one 1e0-scale column")
    add("denormal", G * 1e-320, "denormal-scale entries")
    P = G * 1e-300
    P[:, 0] = G[:, 0] * 1e300
    add("huge_col0_only", P, "all the mass in the gauge column op_lower discards")
    P = G * 1e300
    P[7, 7] = np.nan
    add("huge_and_nan", P, "overflow scale AND a NaN")
    add("hilbert_1e200", (1.0 / (i[:, None] + j[None, :] + 1.0)) * 1e200,
        "ill-conditioned and near the overflow ceiling")
    return out


def theta_grid(n=N):
    return (np.arange(n) + 0.5) * np.pi / n


def weight_zoo(n=N):
    th = theta_grid(n)
    decay = (1.0 + np.tan(0.5 * th) ** 2) ** (-0.75)
    out = [("unit", np.ones(n), "all weights 1"),
           ("decay", decay.copy(), "the project's algebraic-decay shape")]
    for label, val, note in (
        ("zero_entry", 0.0, "one weight is exactly 0 -> 1/w is inf"),
        ("denormal_entry", 1e-320, "one weight is denormal -> 1/w ~ 1e320 overflows"),
        ("huge_entry", 1e300, "one weight is 1e300 -> 1/w underflows"),
        ("nan_entry", np.nan, "one weight is NaN"),
    ):
        w = decay.copy()
        w[7] = val
        out.append(("decay_" + label, w, note))
    out.append(("tiny_all", np.full(n, 1e-300), "every weight 1e-300"))
    out.append(("huge_all", np.full(n, 1e300), "every weight 1e300"))
    return out


def grid_zoo(n=N):
    th = theta_grid(n)
    out = [("regular", th.copy(), "the ordinary grid")]
    c = th.copy()
    c[:] = th[0]
    out.append(("constant", c, "a constant theta grid"))
    p = th.copy()
    p[3] = np.nan
    out.append(("nan_point", p, "one NaN collocation point"))
    return out


# ---------------------------------------------------------------------------
# grading -- one case, both modules
# ---------------------------------------------------------------------------
def _headline(mod, A, dom, cod, theta):
    """`best_lower` through one module.  A raised exception is a PASS."""
    rec = {}
    with np.errstate(all="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            r = mod.best_lower(A, dom, cod, theta, ascent_iters=ASCENT_ITERS, **KW)
            rec["raised"] = ""
            rec["L"] = float(r["lower"])
            rec["L_sign"] = float(r["sign_patterns"])
            rec["L_family"] = float(r["smooth_family"])
            rec["L_ascent"] = float(r["after_ascent"])
            rec["argmax"] = str(r["family_argmax"])
            rec["rejected"] = int(r.get("rejected", 0))
            rec["saturated"] = int(r.get("saturated", 0))
        except Exception as exc:
            rec["raised"] = "%s: %s" % (type(exc).__name__, exc)
            for k in ("L", "L_sign", "L_family", "L_ascent"):
                rec[k] = float("nan")
            rec["argmax"] = ""
            rec["rejected"] = rec["saturated"] = 0
    return rec


def _verdict(L, raised, Nr, exact_ref):
    """The pre-committed grading, at 0 ULP.  Returns (verdict, ratio, excess_ulps)."""
    if raised:
        return "raised", float("nan"), 0.0
    if Nr is None:
        return "excluded_ref_nonfinite", float("nan"), 0.0
    if np.isnan(L):
        return "nan_headline", float("nan"), 0.0
    if np.isinf(L):
        return "VIOLATION_overflow", float("inf"), float("inf")
    LF = Fraction(L)
    ratio = 0.0 if (Nr == 0 and LF == 0) else (
        float("inf") if Nr == 0 else _safe_float(LF / Nr))
    if LF > Nr:
        ulp = float(np.nextafter(abs(L), np.inf) - abs(L)) if L != 0.0 else 5e-324
        ex = float((LF - Nr) / Fraction(ulp))
        # clause (a) is graded at 0 ULP: ANY exceedance of the exact norm counts
        return ("VIOLATION_finite" if exact_ref
                else "finite_exceedance_unconfirmed"), ratio, ex
    if L == 0.0 and Nr > 0:
        return "sound_but_zero", ratio, 0.0
    return "sound", ratio, 0.0


def _safe_float(x):
    try:
        return float(x)
    except (OverflowError, ValueError):
        return float("inf")


def _fstr(x):
    if x is None:
        return None
    try:
        return "%.17e" % float(x)
    except (OverflowError, ValueError):
        return "beyond float64 (exact rational)"


def run_case(PRE, A, dom, cod, theta, t, u, ref_fn, exact_ref):
    post = _headline(POST, A, dom, cod, theta)
    pre = _headline(PRE, A, dom, cod, theta)
    with np.errstate(all="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Nr = ref_fn(A, t, u, True)
        Nf = ref_fn(A, t, u, False)
        # S2 cross-check: only the exact pair has a second exact route
        Nx = ref_l1_linf_closed_form(A, t, u, True) if exact_ref else None
    rec = {"N_res": _fstr(Nr), "N_full": _fstr(Nf), "exact_ref": bool(exact_ref)}
    if exact_ref:
        rec["ref_routes_agree"] = bool(
            (Nr is None and Nx is None) or (Nr is not None and Nr == Nx))
    v, ratio, ex = _verdict(post["L"], post["raised"], Nr, exact_ref)
    rec["verdict"], rec["ratio"], rec["excess_ulps"] = v, ratio, ex
    vp, ratiop, exp_ = _verdict(pre["L"], pre["raised"], Nr, exact_ref)
    rec["verdict_pre"], rec["ratio_pre"], rec["excess_ulps_pre"] = vp, ratiop, exp_
    for k, val in post.items():
        rec[k] = val
    for k, val in pre.items():
        rec["pre_" + k] = val
    # the admissibility direction: a deflation is fine, an inflation is not
    lp, lq = pre["L"], post["L"]
    rec["moved_up"] = bool(np.isfinite(lp) and np.isfinite(lq) and lq > lp)
    rec["argmax_changed"] = bool(post["argmax"] != pre["argmax"]
                                 and not (post["raised"] or pre["raised"]))
    return rec


def battery(PRE):
    ops, wts, grids = operator_zoo(), weight_zoo(), grid_zoo()
    recs = []
    for op in ops:
        for wname, w, wnote in wts:
            for gname, th, gnote in grids:
                if gname != "regular" and op["name"] not in (
                        "benign_random", "huge_1e300", "nan_entry"):
                    continue
                for pair, dom, cod, ref, exact in (
                    ("l1->linf", WeightedLinf(w), WeightedL1(w),
                     ref_l1_linf_extreme_points, True),
                    ("l2->l2", WeightedL2(w), WeightedL2(w), ref_l2_l2, False),
                ):
                    r = run_case(PRE, op["A"], dom, cod, th, w, w, ref, exact)
                    r.update(operator=op["name"], op_note=op["note"],
                             weights=wname, w_note=wnote, grid=gname,
                             pair=pair, tier="A")
                    recs.append(r)
    # the dedicated denormal dimension sweep -- leg 101's second mechanism
    for n in (16, 24, 32, 40, 48, 64, 80, 96):
        th = (np.arange(n) + 0.5) * np.pi / n
        w = (1.0 + np.tan(0.5 * th) ** 2) ** (-0.75)
        A = np.random.default_rng(7).normal(size=(n, n)) * 1e-320
        r = run_case(PRE, A, WeightedLinf(w), WeightedL1(w), th, w, w,
                     ref_l1_linf_extreme_points, True)
        r.update(operator="denormal_1e-320", op_note="denormal-scale entries",
                 weights="decay", w_note="the project's decay shape",
                 grid="regular", pair="l1->linf", tier="A_denormal", dim=n)
        recs.append(r)
    return recs


# ---------------------------------------------------------------------------
# S4 -- the known-answer line: all seven banked v10 rows, plus the headroom
# ---------------------------------------------------------------------------
def _setup(J, alpha, gamma):
    from solver.decay_collocation import Collocation, C_ANCHOR
    from solver.holder_norms import HolderNorm
    col = Collocation(J)
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    A = np.linalg.inv(M)
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    cod = HolderNorm(col.theta, col.X, alpha + 1.0, gamma)
    cod.w[0] = 1.0
    return col, A, dom, cod


def banked_rows(PRE):
    """Re-run the SEVEN banked v10 rows through both modules and compare."""
    with open(os.path.join(_ROOT, "writeup", "data",
                           "p2_route_d_v10_lower.json")) as fh:
        banked = json.load(fh)
    plan = ([("w1_ladder", 1.5, 0.5, r) for r in banked["w1_ladder"]["ladder"]]
            + [("w2_operating", 1.4, 0.15, r) for r in banked["w2_operating"]["ladder"]])
    rows = []
    for block, alpha, gamma, b in plan:
        J = int(b["J"])
        col, A, dom, cod = _setup(J, alpha, gamma)
        f = POST.family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
        s = POST.sign_pattern_lower(A, dom, cod)
        fp = PRE.family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
        sp = PRE.sign_pattern_lower(A, dom, cod)
        def move(banked_v, post_v):
            return (banked_v - post_v) / banked_v if banked_v else 0.0
        rows.append({
            "block": block, "J": J, "alpha": alpha, "gamma": gamma,
            "lower_banked": float(b["lower"]),
            "lower_pre_measured": float(fp["lower"]),
            "lower_post": float(f["lower"]),
            "lower_move_vs_banked": float(move(b["lower"], f["lower"])),
            "pre_matches_banked_bitwise": bool(fp["lower"] == b["lower"]),
            # how far the RECONSTRUCTED pre-repair module lands from the banked
            # literal: this is the environment's `np.linalg.inv` reproducibility,
            # measured rather than assumed, and it sets the floor below which
            # "moved by X" cannot be attributed to the repair at all
            "pre_vs_banked_rel": float(move(b["lower"], fp["lower"])),
            "post_vs_pre_rel": float((fp["lower"] - f["lower"]) / fp["lower"])
            if fp["lower"] else 0.0,
            "sign_banked": float(b["sign_patterns"]),
            "sign_pre_measured": float(sp["lower"]),
            "sign_post": float(s["lower"]),
            "sign_move_vs_banked": float(move(b["sign_patterns"], s["lower"])),
            "sign_pre_matches_banked_bitwise": bool(sp["lower"] == b["sign_patterns"]),
            "argmax_banked": str(b["argmax"]),
            "argmax_post": str(f["argmax"]),
            "argmax_pre": str(fp["argmax"]),
            "argmax_unchanged": bool(f["argmax"] == b["argmax"] == fp["argmax"]),
            "moved_down_only": bool(f["lower"] <= b["lower"]
                                    and s["lower"] <= b["sign_patterns"]),
            "within_budget": bool(move(b["lower"], f["lower"]) <= BUDGET
                                  and move(b["sign_patterns"], s["lower"]) <= BUDGET),
            "rejected": int(f["rejected"] + s["rejected"]),
            "saturated": int(f["saturated"] + s["saturated"]),
            "max_rel_bound": float(max(f["max_rel_bound"], s["max_rel_bound"])),
        })
    return rows


#: leg 101's re-measured headroom, the number DIRECTION.md's gate names
HEADROOM_BANKED = {200: 307.87817655904615, 300: 307.87814237362215,
                   400: 307.8781273371988}


def headroom(PRE):
    """The 307.878-decade production headroom, re-measured through both modules.

    The candidate family is what sets it, so this is where "the repair did not
    touch how candidates are built" is either true to the bit or is not.
    """
    rows = []
    for J in (200, 300, 400):
        col, A, dom, cod = _setup(J, 1.5, 0.5)
        out = {}
        for tag, mod in (("post", POST), ("pre", PRE)):
            worst = 0.0
            for name, g in mod.smooth_family(col.theta, cod.w, n_centre=8,
                                             n_step=8):
                g = g.copy()
                g[0] = 0.0
                worst = max(worst, float(np.max(np.abs(A @ g))))
            out[tag + "_max_image"] = worst
            out[tag + "_decades"] = float(np.log10(np.finfo(float).max / worst))
        d = HEADROOM_BANKED[J]
        rows.append({
            "J": J, "decades_banked": d,
            "decades_post": out["post_decades"], "decades_pre": out["pre_decades"],
            "decades_move_vs_banked": float(out["post_decades"] - d),
            # The clause that tests the REPAIR is post-vs-pre in one process on
            # one `A`; post-vs-banked additionally carries whatever last-bit
            # difference `np.linalg.inv` shows across BLAS builds, which is a
            # property of the environment and not of solver/op_lower.py.  Both
            # are reported; only the first decides.
            "decades_post_equals_pre": bool(out["post_decades"]
                                            == out["pre_decades"]),
            "bit_identical_to_pre": bool(out["post_max_image"]
                                         == out["pre_max_image"]),
            "max_image_post": out["post_max_image"],
            "max_image_pre": out["pre_max_image"],
            "max_absA": float(np.max(np.abs(A))),
        })
    return rows


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    PRE = load_pre_repair()
    print("PRE-REPAIR MODULE reconstructed from git: %s:solver/op_lower.py "
          "(blob %s)" % (PRE_COMMIT, PRE.__source_sha__[:12]))

    recs = battery(PRE)

    DEC = ("sound", "sound_but_zero", "VIOLATION_overflow", "VIOLATION_finite",
           "finite_exceedance_unconfirmed")
    dec = [r for r in recs if r["verdict"] in DEC]
    excl = [r for r in recs if r["verdict"] == "excluded_ref_nonfinite"]
    over = [r for r in dec if r["verdict"] == "VIOLATION_overflow"]
    finv = [r for r in dec if r["verdict"] == "VIOLATION_finite"]
    unconf = [r for r in dec if r["verdict"] == "finite_exceedance_unconfirmed"]
    zero = [r for r in dec if r["verdict"] == "sound_but_zero"]
    nanh = [r for r in recs if r["verdict"] == "nan_headline"]
    raised = [r for r in recs if r["verdict"] == "raised"]
    viol = over + finv
    fin = [r["ratio"] for r in dec if np.isfinite(r["ratio"])]

    # the positive control: the SAME grader on the pre-repair module
    over_p = [r for r in dec if r["verdict_pre"] == "VIOLATION_overflow"]
    finv_p = [r for r in dec if r["verdict_pre"] == "VIOLATION_finite"]
    zero_p = [r for r in dec if r["verdict_pre"] == "sound_but_zero"]
    viol_p = over_p + finv_p
    fin_p = [r["ratio_pre"] for r in dec if np.isfinite(r["ratio_pre"])]
    # the same records re-graded under LEG 101'S OWN rule, so the control can be
    # checked against the number leg 101 actually published
    finv_p_101 = [r for r in finv_p
                  if r["excess_ulps_pre"] > 1.0
                  and np.isfinite(r["ratio_pre"])
                  and r["ratio_pre"] > 1.0 + 1e-9]
    # identity, not equality: these dicts carry NaN fields and NaN != NaN
    _keep = {id(r) for r in finv_p_101}
    within_ulp_p = [r for r in finv_p if id(r) not in _keep]
    viol_p_101 = over_p + finv_p_101

    disagree = [r for r in recs if r.get("exact_ref") and not r["ref_routes_agree"]]
    moved_up = [r for r in recs if r["moved_up"]]

    counts_ok = (len(recs) == EXPECT_TOTAL and len(dec) == EXPECT_DECIDING
                 and len(excl) == EXPECT_EXCLUDED)
    control_ok = (len(viol_p_101) == EXPECT_PRE_VIOLATIONS_LEG101
                  and len(viol_p) == EXPECT_PRE_VIOLATIONS_0ULP
                  and len(over_p) == EXPECT_PRE_OVERFLOW)

    print("\nS1 -- BATTERY SHAPE (a gate magnitude: a different count is a "
          "different battery)")
    print("  total cases ....... %d (leg 101: %d)  %s"
          % (len(recs), EXPECT_TOTAL, "MATCH" if len(recs) == EXPECT_TOTAL else "DIFFERS"))
    print("  gate-deciding ..... %d (leg 101: %d)  %s"
          % (len(dec), EXPECT_DECIDING,
             "MATCH" if len(dec) == EXPECT_DECIDING else "DIFFERS"))
    print("  excluded .......... %d (leg 101: %d)  %s"
          % (len(excl), EXPECT_EXCLUDED,
             "MATCH" if len(excl) == EXPECT_EXCLUDED else "DIFFERS"))

    print("\nS2 -- REFERENCE CROSS-CHECK (extreme-point enumeration vs leg 101's "
          "closed form, both exact rational)")
    print("  cases with an exact reference ..... %d"
          % sum(1 for r in recs if r.get("exact_ref")))
    print("  routes DISAGREE ................... %d" % len(disagree))

    print("\nS3 -- THE 209-CASE BATTERY, POST-REPAIR (clause (a), graded at 0 ULP)")
    print("  VIOLATIONS, overflow (L = inf vs a finite norm) .. %d" % len(over))
    print("  VIOLATIONS, a FINITE value above the true norm ... %d" % len(finv))
    print("  finite exceedance, float ref, unconfirmed ........ %d" % len(unconf))
    print("  sound, nonzero .................................. %d"
          % (len(dec) - len(zero) - len(viol) - len(unconf)))
    print("  sound but L = 0 (weak, TRUE -- a PASS) ........... %d" % len(zero))
    print("  NaN headline / raised ........................... %d / %d"
          % (len(nanh), len(raised)))
    if fin:
        print("  max FINITE L/N_true over the decided cases: %.12f (min %.3e)"
              % (max(fin), min(fin)))
    print("  headlines that moved UP vs the pre-repair module . %d" % len(moved_up))

    print("\n  POSITIVE CONTROL -- the SAME grader on the PRE-REPAIR module")
    print("    under LEG 101's rule (>1 ULP and >1e-9 rel): %d violations "
          "(overflow %d, finite %d)   leg 101 published %d  %s"
          % (len(viol_p_101), len(over_p), len(finv_p_101),
             EXPECT_PRE_VIOLATIONS_LEG101,
             "REPRODUCED" if len(viol_p_101) == EXPECT_PRE_VIOLATIONS_LEG101
             else "DIFFERS"))
    print("    under THIS leg's rule (0 ULP, stricter): %d violations "
          "(overflow %d, finite %d) = %d + the %d cases leg 101 excused as "
          "`sound_within_one_ulp`"
          % (len(viol_p), len(over_p), len(finv_p),
             EXPECT_PRE_VIOLATIONS_LEG101, len(within_ulp_p)))
    print("    CONTROL: %s"
          % ("FIRES, and reproduces leg 101's decomposition exactly"
             if control_ok else "DID NOT REPRODUCE"))
    if fin_p:
        print("    max FINITE L/N_true, pre-repair: %.12f (leg 101: 1.000604187)"
              % max(fin_p))
    print("    sound_but_zero, pre-repair: %d (post-repair %d)"
          % (len(zero_p), len(zero)))

    for r in viol + unconf:
        print("  !! %s %s | %s | %s | %s : L = %.6e  N_true = %s  ratio = %.12g"
              % (r["verdict"], r["operator"], r["weights"], r["grid"], r["pair"],
                 r["L"], r["N_res"], r["ratio"]))

    rows = banked_rows(PRE)
    hd = headroom(PRE)

    print("\nS4 -- THE KNOWN-ANSWER LINE: ALL SEVEN BANKED v10 ROWS")
    print("  %-13s %-5s %-20s %-20s %-11s %s"
          % ("block", "J", "banked lower", "post-repair lower", "rel move", "argmax"))
    for r in rows:
        print("  %-13s %-5d %-20.16f %-20.16f %-11.3e %s"
              % (r["block"], r["J"], r["lower_banked"], r["lower_post"],
                 r["lower_move_vs_banked"],
                 r["argmax_post"] + ("" if r["argmax_unchanged"] else " CHANGED")))
    worst_move = max(max(r["lower_move_vs_banked"], r["sign_move_vs_banked"])
                     for r in rows)
    all_down = all(r["moved_down_only"] for r in rows)
    all_bud = all(r["within_budget"] for r in rows)
    argmax_ok = all(r["argmax_unchanged"] for r in rows)
    pre_bitwise = sum(1 for r in rows if r["pre_matches_banked_bitwise"])
    pre_bitwise_s = sum(1 for r in rows if r["sign_pre_matches_banked_bitwise"])
    tot_rej = sum(r["rejected"] for r in rows)
    tot_sat = sum(r["saturated"] for r in rows)
    print("  direction: %s   worst move %.3e (budget %.0e)   argmax unchanged: %s"
          % ("DOWN on all seven" if all_down else "NOT ALL DOWN", worst_move,
             BUDGET, argmax_ok))
    worst_pre_vs_banked = max(abs(r["pre_vs_banked_rel"]) for r in rows)
    worst_post_vs_pre = max(abs(r["post_vs_pre_rel"]) for r in rows)
    print("  the RECONSTRUCTED pre-repair module lands within %.3e relative of "
          "the banked literal (%d/7 bitwise on `lower`, %d/7 on `sign_patterns`)"
          " -- the environment's inv() floor, below which no move is "
          "attributable to the repair" % (worst_pre_vs_banked, pre_bitwise,
                                          pre_bitwise_s))
    print("  post-repair vs the pre-repair module MEASURED in the same process: "
          "worst %.3e relative, down on all seven" % worst_post_vs_pre)
    print("  candidates rejected / saturated on the production rows: %d / %d"
          % (tot_rej, tot_sat))

    print("\n  THE 307.878-DECADE HEADROOM, re-measured through BOTH modules")
    for r in hd:
        print("    J = %-4d banked %.8f   post-repair %.8f   vs banked %+.2e   "
              "post == pre exactly: %s   candidate images bit-identical: %s"
              % (r["J"], r["decades_banked"], r["decades_post"],
                 r["decades_move_vs_banked"], r["decades_post_equals_pre"],
                 r["bit_identical_to_pre"]))
    headroom_vs_pre = all(r["decades_post_equals_pre"] for r in hd)
    headroom_bitid = all(r["bit_identical_to_pre"] for r in hd)
    headroom_worst_vs_banked = max(abs(r["decades_move_vs_banked"]) for r in hd)

    clause_a = (len(viol) == 0 and len(nanh) == 0 and counts_ok
                and len(disagree) == 0 and control_ok)
    # `moved_up` is deliberately NOT a clause-(b) term.  The pre-committed rule
    # (writeup/novelty/leg_132.md sec 3) enumerates six validated magnitudes and
    # sec 2.3 states in advance that adversarial-case headlines are not among
    # them.  An adversarial case whose bound rose while staying <= N_true is the
    # repair RECOVERING information the pre-repair module lost to overflow, which
    # is sound; the count is reported as a magnitude, not graded.
    clause_b = (all_down and all_bud and argmax_ok and tot_rej == 0
                and tot_sat == 0 and headroom_vs_pre and headroom_bitid)
    gate = "yes" if (clause_a and clause_b) else "no"

    print("\nCLAUSE (a) true lower bound on all %d cases ....... %s"
          % (EXPECT_DECIDING, "YES" if clause_a else "NO"))
    print("CLAUSE (b) every validated magnitude to the digit .. %s"
          % ("YES" if clause_b else "NO"))
    print("GATE (repair sound AND non-regressive, independently): %s" % gate.upper())
    dt = time.time() - t0
    print("elapsed %.1f s" % dt)

    out = {
        "leg": 132, "route": "OLB", "generated": time.strftime("%Y-%m-%d"),
        "gate_question": (
            "Post-repair, does solver/op_lower.py (a) return a true lower bound "
            "(L <= N_true) on every one of leg 101's 209 original adversarial "
            "cases in an independent re-run, and (b) reproduce the 307.878-decade "
            "headroom and every other validated magnitude to the digit?"),
        "gate_answer": gate,
        "clause_a_soundness": clause_a, "clause_b_non_regression": clause_b,
        "pre_repair_commit": PRE_COMMIT, "pre_repair_blob": PRE.__source_sha__,
        "grading": "L > N_true at ANY number of ULP is a violation (0 ULP rule)",
        "dimension": N, "budget_rel": BUDGET, "elapsed_s": round(dt, 2),
        "battery": {
            "cases": len(recs), "cases_expected": EXPECT_TOTAL,
            "gate_deciding": len(dec), "gate_deciding_expected": EXPECT_DECIDING,
            "excluded_ref_nonfinite": len(excl),
            "excluded_expected": EXPECT_EXCLUDED,
            "counts_match_leg101": counts_ok,
            "violations": len(viol), "violations_overflow": len(over),
            "violations_finite": len(finv),
            "finite_exceedance_unconfirmed": len(unconf),
            "sound_nonzero": len(dec) - len(zero) - len(viol) - len(unconf),
            "sound_but_zero": len(zero),
            "nan_headline": len(nanh), "raised": len(raised),
            "max_ratio": max(fin) if fin else None,
            "min_ratio": min(fin) if fin else None,
            "headlines_moved_up_vs_pre": len(moved_up),
            "reference_routes_disagree": len(disagree),
        },
        "positive_control_pre_repair": {
            "control_fires": control_ok,
            "violations_leg101_rule": len(viol_p_101),
            "violations_leg101_rule_expected": EXPECT_PRE_VIOLATIONS_LEG101,
            "violations_0ulp_rule": len(viol_p),
            "violations_0ulp_rule_expected": EXPECT_PRE_VIOLATIONS_0ULP,
            "violations_overflow": len(over_p),
            "violations_overflow_expected": EXPECT_PRE_OVERFLOW,
            "violations_finite_0ulp": len(finv_p),
            "violations_finite_leg101_rule": len(finv_p_101),
            "excused_within_one_ulp_by_leg101": len(within_ulp_p),
            "sound_but_zero": len(zero_p),
            "max_ratio": max(fin_p) if fin_p else None,
        },
        "known_answer_line": {
            "rows": rows, "worst_rel_move": worst_move,
            "all_moved_down": all_down, "all_within_budget": all_bud,
            "argmax_unchanged": argmax_ok,
            "pre_repair_bitwise_lower": pre_bitwise,
            "pre_repair_bitwise_sign": pre_bitwise_s,
            "worst_pre_vs_banked_rel": worst_pre_vs_banked,
            "worst_post_vs_pre_rel": worst_post_vs_pre,
            "rejected_total": tot_rej, "saturated_total": tot_sat,
        },
        "headroom": {"rows": hd,
                     "post_equals_pre_exactly": headroom_vs_pre,
                     "bit_identical_to_pre_repair": headroom_bitid,
                     "worst_abs_move_vs_banked_decades": headroom_worst_vs_banked},
        "records": recs,
    }
    path = os.path.join(_ROOT, "writeup", "data", "p2_route_olb_v1_postrepair.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote %s" % path)
    try:
        os.unlink(PRE.__source_path__)
    except OSError:
        pass
    return out


if __name__ == "__main__":
    main()
