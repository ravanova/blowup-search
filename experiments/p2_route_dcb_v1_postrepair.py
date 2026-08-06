"""Leg 167 -- Route-DCB: INDEPENDENT POST-REPAIR REGRESSION CHECK of solver/decay_collocation.py.

Closes the loop on leg 151 (Route-DCR), which repaired the three silent-corruption sites leg
115 (Route-DCA) found.  No independent regression check has run since.  This runner is that
check.  It edits nothing: `solver/decay_collocation.py` is READ ONLY here, under either branch
of the gate.

THE GATE (pre-committed, DIRECTION.md leg 167, quoted verbatim):

    Post-repair, does solver/decay_collocation.py (a) reject or correctly flag every one of
    leg 115's original 3 failing cases in an independent re-run, and (b) reproduce every
    previously-validated result bit-identically?

WHY THIS IS NOT LEG 151 RE-RUN.  Two independence hazards were measured in the novelty pass
(writeup/novelty/leg_167.md) BEFORE this file was written, and both shape it:

  F2  The on-disk `test_decay_collocation_adversarial.py` is NOT leg 115's battery.  Leg 151
      rewrote it (191+/91-) in the SAME commit as the repair, inverting all 7 pins.  Running
      it grades the repairer with the repairer's own assertions -- lesson 90, a control that
      cannot come out differently.  So every leg-115 case here is re-derived from the battery
      and runner AS THEY STOOD AT 53f03fe, read out of git, never from the post-151 files.

  F1  Leg 115's own runner ABORTS against the repaired module on its FIRST G1 probe
      (DecayCollocationDomainError at J=1, line 114), so it never reaches G2 or G3 at all --
      the same shape legs 131 and 147 found.  So classification here is PER CASE, never per
      battery: each case runs in its own try/except and is classified

          REFUSED       -- raised, i.e. the caller cannot receive a corrupt number
          FLAGGED       -- returned, but non-finite or warned, i.e. visibly signalled
          SILENT_VALUE  -- returned an ordinary finite float with no signal  <-- the defect

      A raise is DATA here, not an abort.  A driver inheriting leg 115's control flow would
      report "0 cases checked" and could be mistaken for a pass.

  F3  Clause (b) is a SAME-PROCESS bitwise differential against the pre-repair module loaded
      out of git at blob `a595dcb` (the module's creating commit; `git log main --
      solver/decay_collocation.py` returns exactly two commits, a595dcb and 746c57a, so the
      pre/post boundary needs no judgement).  NOT a comparison against a committed JSON: leg
      105 measured a ~2.1% discrepancy that way which was environment drift predating both
      repairs, and leg 147 saw 22/763 leaves move <=3 ULP with 6 on paths that never touch the
      module.  Bitwise identity is the right ask BETWEEN VERSIONS OF THE SAME IMPLEMENTATION
      in one process (WG21 P3375R3; Demmel et al., ACM TOMS 10.1145/3389360) and the wrong ask
      across environments.

  Independence on clause (b) is in the ENUMERATION, not the instrument.  Leg 151 chose which
  1672 quantities to compare; re-running its list would inherit whatever it did not look at.
  The coverage set below is enumerated from the module's public surface here, and its size is
  reported as a magnitude against leg 151's 1672 rather than tuned to match it.

THE LESSON-90 CONTROL, and it is load-bearing.  Every clause-(a) case is run against BOTH
modules in the same process.  The run is VOID unless the PRE-REPAIR module reproduces leg 115's
banked SILENT_VALUE counts.  If the pre-repair side also refused, the comparison would be
measuring the harness, not the repair, and could not come out differently.

WHAT A CLEAN CLAUSE (b) DOES NOT MEAN.  Per the published limitation of golden-master /
characterization testing (Feathers; see novelty pass Q1): it does not infer correctness.  A
0-ULP result here says THE REPAIR MOVED NOTHING.  It does not say any banked number is right.

    .venv/bin/python experiments/p2_route_dcb_v1_postrepair.py
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import warnings

# ---------------------------------------------------------------------------
# BLAS THREADS PINNED TO ONE, and this is a correctness decision before it is a
# speed one.  Multi-threaded BLAS chooses its reduction order dynamically, so the
# last bit of a dot product can depend on how many threads happened to be free --
# precisely the effect the reproducibility literature names as the reason strict
# bitwise identity fails across runs (Demmel et al., ACM TOMS 10.1145/3389360;
# WG21 P3375R3).  Clause (b) asserts 0 ULP, so the reduction order must be fixed,
# not merely likely to repeat.  Pinning to one thread makes the differential
# deterministic by construction rather than by luck.
#
# It is also, measured on this box while four legs ran in parallel, ~60x FASTER:
# a 400x400 np.linalg.inv took 3.5s with the default thread pool (four legs
# oversubscribing the cores) and 0.0589s pinned.  Must be set BEFORE numpy loads.
# ---------------------------------------------------------------------------
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402  -- must follow the thread pinning above

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

# The module's two commits on main.  a595dcb created it; 746c57a is leg 151's repair.
PRE_REPAIR_REF = "a595dcb"
REPAIR_REF = "746c57a"
# Leg 115's battery and runner as they stood BEFORE leg 151 rewrote them (novelty finding F2).
LEG115_REF = "53f03fe"

SEED = 20260806          # leg 115's own seed, so its randomized battery replays exactly
OUT = os.path.join(REPO, "writeup", "data", "p2_route_dcb_v1_postrepair.json")

# Leg 115's banked magnitudes, for the control to check itself against.
LEG115_J1_COLLAPSE_VALUE = 1.681792830507429
LEG115_G2_WORKED_FLAT = 12.0
LEG115_G2_WORKED_COLUMN = 10.0
LEG115_G3_PIPELINE_VALUE = 3.5626111859714866


# =========================================================================
# loading the pre-repair module beside the post-repair one, in ONE process
# =========================================================================

def _git_show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=REPO,
                          capture_output=True, check=True).stdout


def load_pre_repair():
    """Import solver/decay_collocation.py at `PRE_REPAIR_REF` as a separate live module.

    Same interpreter, same NumPy, same BLAS, same process as the post-repair import -- which is
    exactly the setting in which the reproducibility literature says bitwise identity IS the
    correct criterion.
    """
    src = _git_show(PRE_REPAIR_REF, "solver/decay_collocation.py")
    fd, path = tempfile.mkstemp(suffix="_pre_decay_collocation.py")
    with os.fdopen(fd, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("pre_decay_collocation", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["pre_decay_collocation"] = mod
    spec.loader.exec_module(mod)
    mod.__source_path__ = path
    mod.__source_sha256__ = hashlib.sha256(src).hexdigest()
    return mod


# =========================================================================
# bit-level comparison primitives
# =========================================================================

def _u64(x):
    """Raw IEEE-754 bit patterns of a float64 array, as uint64.

    Compares NaN payloads and distinguishes -0.0 from 0.0, which `allclose` and even `==` do
    not.  This is the 0-ULP instrument, not a tolerance.
    """
    a = np.ascontiguousarray(np.asarray(x, dtype=np.float64))
    return a.view(np.uint64).ravel()


def bit_compare(a, b):
    """(n_leaves, n_identical) over raw float64 bit patterns; (n, 0) on any shape mismatch."""
    ua, ub = _u64(a), _u64(b)
    if ua.shape != ub.shape:
        return max(ua.size, ub.size), 0
    return int(ua.size), int(np.count_nonzero(ua == ub))


def digest(x):
    return hashlib.sha256(_u64(x).tobytes()).hexdigest()[:16]


# =========================================================================
# CLAUSE (a) -- leg 115's failing cases, per-case classification
# =========================================================================

REFUSED, FLAGGED, SILENT_VALUE = "REFUSED", "FLAGGED", "SILENT_VALUE"


def classify(fn):
    """Run one case; report which of the three outcomes the caller actually receives.

    Warnings are RECORDED, not suppressed: a module that returns a wrong number but shouts
    about it is FLAGGED, which the gate's own wording ("reject or correctly flag") accepts.
    Leg 115's pins suppressed warnings; not suppressing them here can only make the repaired
    module look BETTER on a case it merely warns about, so the classification is stated
    explicitly rather than folded into a pass/fail.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with np.errstate(all="ignore"):
            try:
                value = fn()
            except Exception as exc:                     # noqa: BLE001 -- classification IS the job
                return {"outcome": REFUSED, "exc_type": type(exc).__name__,
                        "exc_msg": str(exc)[:200], "value": None,
                        "warnings": [w.category.__name__ for w in caught]}
        wnames = [w.category.__name__ for w in caught]
    scalar = None
    try:
        scalar = float(np.asarray(value, dtype=float).ravel()[0])
    except Exception:                                     # noqa: BLE001
        pass
    finite = scalar is not None and np.isfinite(scalar)
    outcome = SILENT_VALUE if (finite and not wnames) else FLAGGED
    return {"outcome": outcome, "exc_type": None, "exc_msg": None,
            "value": scalar, "warnings": wnames}


def _pipeline_with_om(dc, col, om, alpha, c, gauge="origin", drop=0):
    """Leg 115's check_J1_ignores_poisoned_om reconstruction, verbatim in arithmetic.

    graded_inverse_norm builds `om` internally, so leg 115 rebuilt its exact call sequence with
    a poisoned nodal field substituted.  Copied from the battery at 53f03fe, not paraphrased.
    """
    M, rows = dc.gauged_jacobian(col, om, c, gauge=gauge, drop=drop)
    A = np.linalg.inv(M)
    w_dom = col.w_domain(alpha)
    w_cod = np.empty(col.J)
    w_cod[0] = 1.0
    w_cod[1:] = col.w_codomain(alpha)[rows]
    return dc.sup_op_norm(A, w_dom, w_cod)


def leg115_cases(dc):
    """Leg 115's failing cases, as case-name -> zero-argument callable, bound to module `dc`.

    Enumerated from the UNION of leg 115's test battery and its runner at 53f03fe, because the
    two do not agree: the battery's G3 list is 4 complex alphas, the runner's is 6 (it adds
    1.0+0.0j and 1.5+1e-10j).  Taking the union rather than either file alone is deliberate --
    a check that used only the smaller list would silently skip two cases leg 115 banked.
    """
    cases = {}

    # ---- G1: the J = 1 grid collapse -----------------------------------
    col1 = dc.Collocation(1)
    A_ALPHA = 1.5

    # G1a -- 9 values of c, including nan/+-inf (battery + runner agree)
    for c in (0.0, 0.5, 1.0, 100.0, -50.0, 1e6, float("nan"), float("inf"), -float("inf")):
        cases[f"G1a_J1_c={c!r}"] = (lambda c=c: dc.graded_inverse_norm(col1, A_ALPHA, c=c)[0])

    # G1b -- 3 poisoned nodal fields through leg 115's own reconstructed pipeline
    for tag, p in (("nan", float("nan")), ("+inf", float("inf")), ("-inf", -float("inf"))):
        cases[f"G1b_J1_om={tag}"] = (
            lambda p=p: _pipeline_with_om(dc, col1, np.array([p]), A_ALPHA, p))

    # G1c -- 5 drop values at J = 1 (the four out-of-range ones are the 4 leg 115's own
    #        prescribed 'rows is empty' predicate would have MISSED; see leg 151 novelty)
    for drop in (0, 1, -1, 5, 100):
        cases[f"G1c_J1_drop={drop}"] = (
            lambda drop=drop: dc.graded_inverse_norm(col1, A_ALPHA, drop=drop)[0])

    # G1d -- both gauges at J = 1
    for gauge in ("origin", "a0"):
        cases[f"G1d_J1_gauge={gauge}"] = (
            lambda g=gauge: dc.graded_inverse_norm(col1, A_ALPHA, gauge=g)[0])

    # G1e -- the runner's closed-form multi-alpha sweep at J = 1 (6 alphas x 2 gauges)
    for alpha in (0.0, 0.5, 1.5, 2.0, 3.0, -1.0):
        for gauge in ("origin", "a0"):
            cases[f"G1e_J1_alpha={alpha}_gauge={gauge}"] = (
                lambda a=alpha, g=gauge: dc.graded_inverse_norm(col1, a, gauge=g)[0])

    # G1f -- the mechanism itself: gauged_jacobian at J = 1 retaining zero collocation rows
    cases["G1f_J1_gauged_jacobian_rows"] = (
        lambda: float(len(dc.gauged_jacobian(col1, col1.anchor(), dc.C_ANCHOR, drop=0)[1])))

    # ---- G2: sup_op_norm 1-D shape ambiguity ---------------------------
    A_flat = np.array([10.0, 1.0, 1.0])
    cases["G2a_worked_case_flat_3"] = (
        lambda: dc.sup_op_norm(A_flat, np.array([1.0, 1.0, 1.0]), np.array([1.0])))

    rng = np.random.default_rng(SEED)                 # leg 115's seed -> its exact 30 cases
    for i in range(30):
        n = int(rng.integers(2, 7))
        Af = rng.uniform(0.1, 20.0, size=n)
        cases[f"G2b_rand{i:02d}_n={n}"] = (
            lambda Af=Af, n=n: dc.sup_op_norm(Af, np.ones(n), np.ones(1)))

    # ---- G3: type-degenerate (complex) alpha ---------------------------
    col16 = dc.Collocation(16)
    om16 = col16.anchor()
    for a in (1.0 + 0.0j, 1.5 + 1e-10j, 1.5 + 0.1j, 1.5 + 1.0j, 0.0 + 1.0j, -1.0 + 2.0j):
        cases[f"G3a_norm_domain_alpha={a}"] = (lambda a=a: col16.norm_domain(om16, a))
        cases[f"G3b_norm_codomain_alpha={a}"] = (lambda a=a: col16.norm_codomain(om16, a))
    cases["G3c_full_pipeline_alpha=1.5+0.3j"] = (
        lambda: dc.graded_inverse_norm(col16, 1.5 + 0.3j)[0])

    return cases


def run_clause_a(dc_post, dc_pre):
    """Classify every leg-115 case against BOTH modules.  The pre-repair arm is the control."""
    post = {k: classify(f) for k, f in leg115_cases(dc_post).items()}
    pre = {k: classify(f) for k, f in leg115_cases(dc_pre).items()}

    def tally(d, prefix):
        sel = {k: v for k, v in d.items() if k.startswith(prefix)}
        out = {"n": len(sel)}
        for o in (REFUSED, FLAGGED, SILENT_VALUE):
            out[o] = sum(1 for v in sel.values() if v["outcome"] == o)
        return out

    groups = ("G1", "G2", "G3")
    summary = {
        "post_repair": {g: tally(post, g) for g in groups},
        "pre_repair_control": {g: tally(pre, g) for g in groups},
    }
    summary["post_repair"]["ALL"] = tally(post, "G")
    summary["pre_repair_control"]["ALL"] = tally(pre, "G")

    # --- the lesson-90 control: could this have come out differently? ----
    pre_silent = summary["pre_repair_control"]["ALL"][SILENT_VALUE]
    post_silent = summary["post_repair"]["ALL"][SILENT_VALUE]
    pre_refused = summary["pre_repair_control"]["ALL"][REFUSED]
    post_refused = summary["post_repair"]["ALL"][REFUSED]

    g3_live = pre["G3c_full_pipeline_alpha=1.5+0.3j"]["value"]
    g3_drift = (abs(g3_live - LEG115_G3_PIPELINE_VALUE) / abs(LEG115_G3_PIPELINE_VALUE)
                if isinstance(g3_live, float) else float("inf"))
    control = {
        "pre_repair_silent_values": pre_silent,
        "post_repair_silent_values": post_silent,
        "pre_repair_refused": pre_refused,
        "post_repair_refused": post_refused,
        "pre_reproduces_leg115_J1_value": any(
            v["value"] is not None and v["value"] == LEG115_J1_COLLAPSE_VALUE
            for k, v in pre.items() if k.startswith("G1a")),
        "pre_reproduces_leg115_G2_worked_flat": (
            pre["G2a_worked_case_flat_3"]["value"] == LEG115_G2_WORKED_FLAT),
        # G3's banked value is compared to a TOLERANCE, not bitwise, and the reason is measured
        # rather than assumed: it is the one of leg 115's three headline numbers that passes
        # through np.linalg.inv (a 16x16, i.e. LAPACK), so its last bit is a property of the
        # library build.  Demanding bitwise equality here would report a NO caused by the
        # comparison rather than by the module -- see the journal, and leg 105's identical trap.
        "pre_G3_pipeline_live": g3_live,
        "pre_G3_pipeline_leg115_json": LEG115_G3_PIPELINE_VALUE,
        "pre_G3_pipeline_relative_drift": g3_drift,
        "pre_G3_pipeline_bitwise_equal_to_json": g3_live == LEG115_G3_PIPELINE_VALUE,
        "pre_reproduces_leg115_G3_pipeline_to_tolerance": g3_drift < 1e-14,
    }
    control["VOID_unless_pre_repair_did_not_refuse"] = pre_refused == 0
    control["comparison_can_come_out_differently"] = bool(
        pre_refused == 0 and pre_silent > 0
        and control["pre_reproduces_leg115_J1_value"]
        and control["pre_reproduces_leg115_G2_worked_flat"]
        and control["pre_reproduces_leg115_G3_pipeline_to_tolerance"])

    # --- the residue: any case the repaired module still answers silently ---
    residue = {k: v for k, v in post.items() if v["outcome"] == SILENT_VALUE}

    # --- exception TYPE audit: a raise is only useful if it is the module's own -------
    exc_types = {}
    for v in post.values():
        if v["outcome"] == REFUSED:
            exc_types[v["exc_type"]] = exc_types.get(v["exc_type"], 0) + 1

    # --- the G2 unambiguous spelling must still WORK (no over-refusal) ---
    still_works = {}
    Af = np.array([10.0, 1.0, 1.0])
    still_works["G2_column_spelling_3x1"] = classify(
        lambda: dc_post.sup_op_norm(Af.reshape(3, 1), np.ones(3), np.ones(1)))
    for a, tag in ((1.5, "float"), (2, "int"), (np.float64(1.5), "np.float64"),
                   (np.int64(2), "np.int64")):
        col16 = dc_post.Collocation(16)
        still_works[f"G3_real_alpha_{tag}"] = classify(
            lambda a=a, c=col16: c.norm_domain(c.anchor(), a))
    for J in (2, 8, 16):
        still_works[f"G1_ordinary_J{J}"] = classify(
            lambda J=J: dc_post.graded_inverse_norm(dc_post.Collocation(J), 1.5)[0])

    # --- G3 under PRODUCTION warning filters, not forced ones -------------
    # classify() forces warnings.simplefilter("always"), which is the generous reading: it lets
    # a ComplexWarning count as FLAGGED.  That is not what a caller actually sees.  Leg 115's
    # finding rests on the claim that this warning is easy to miss, so the claim is MEASURED
    # here at both filter settings rather than repeated.
    g3_prod = {}
    for tag, filt in (("default", "default"), ("always", "always"), ("ignore", "ignore")):
        col16 = dc_pre.Collocation(16)
        om16 = col16.anchor()
        seen, values = 0, []
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter(filt)
            with np.errstate(all="ignore"):
                for a in (1.0 + 0.0j, 1.5 + 1e-10j, 1.5 + 0.1j, 1.5 + 1.0j,
                          0.0 + 1.0j, -1.0 + 2.0j):
                    values.append(col16.norm_domain(om16, a))
            seen = len(caught)
        g3_prod[filt] = {
            "n_calls": len(values),
            "n_warnings_surfaced": seen,
            "all_returned_ordinary_finite_float": all(
                isinstance(v, float) and np.isfinite(v) for v in values),
            "n_exceptions": 0,
        }

    return {
        "summary": summary,
        "lesson90_control": control,
        "g3_pre_repair_under_production_warning_filters": g3_prod,
        "residue_silent_after_repair": residue,
        "refusal_exception_types": exc_types,
        "no_over_refusal_probes": still_works,
        "per_case_post": post,
        "per_case_pre": pre,
    }


# =========================================================================
# CLAUSE (b) -- zero regression, same-process bitwise differential
# =========================================================================

# Enumerated from the module's public surface HERE (see F3), not inherited from leg 151.
J_FULL = (2, 3, 4, 8, 16, 32, 64, 128, 256, 400)   # every matrix-valued quantity
J_CHEAP = (512, 800, 1000)                          # vector/scalar quantities only (O(J^2) mats
                                                    # at J=1000 are 8 MB each; the cap is stated
                                                    # in the journal as an honest limit)
ALPHAS = (-1.0, 0.0, 0.5, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0)
ALPHAS_BIG = (0.0, 1.5, 3.0)      # the inverse arm's reduced alpha set at large J -- see below
C_VALUES = (0.0, 0.5, 1.0, -50.0)
GAUGES = ("origin", "a0")

# The inverse arm (np.linalg.inv) is the only O(J^3) quantity here and it dominates the whole
# run.  Every CHEAP quantity -- grid, transforms, H, D, transport, anchor, residual, jacobian,
# dc_column, quadratic, both weights, both norms -- is swept at EVERY J in the list, full alpha
# set.  The inverse arm is swept in full only up to J = 400 and thinned above it.  This is an
# honest declared limit, not a silent one, and it is the same shape as leg 151's own (its
# inverse arm capped at J = 1000 while its cheap arm reached J = 2000).
J_INVERSE_FULL_MAX = 400


def _inverse_arm_alphas(J):
    return ALPHAS if J <= J_INVERSE_FULL_MAX else ALPHAS_BIG


def _quantities(dc, J, heavy):
    """Every float64-valued thing the module's public surface produces at grid size J."""
    q = {}
    th, X = dc.grid(J)
    q["grid.theta"], q["grid.X"] = th, X
    to_coef, cos_eval, sin_eval = dc.transforms(J)
    if heavy:
        q["transforms.to_coef"] = to_coef
        q["transforms.cos_eval"] = cos_eval
        q["transforms.sin_eval"] = sin_eval

    col = dc.Collocation(J)
    q["Collocation.theta"], q["Collocation.X"] = col.theta, col.X
    if heavy:
        q["Collocation.H"] = col.H
        q["Collocation.D"] = col.D
        q["Collocation.transport"] = col.transport
    om = col.anchor()
    q["anchor"] = om

    for c in C_VALUES:
        q[f"residual(c={c})"] = col.residual(om, c)
        if heavy:
            q[f"jacobian_matrix(c={c})"] = col.jacobian_matrix(om, c)
    q["dc_column"] = col.dc_column(om)
    q["quadratic"] = col.quadratic(om)

    for a in ALPHAS:
        q[f"w_domain(a={a})"] = col.w_domain(a)
        q[f"w_codomain(a={a})"] = col.w_codomain(a)
        q[f"norm_domain(a={a})"] = col.norm_domain(om, a)
        q[f"norm_codomain(a={a})"] = col.norm_codomain(om, a)

    # the gauged square system and the headline norm -- J >= 2 only, which is now the
    # module's own domain; J = 1 is clause (a)'s business, not clause (b)'s
    drops = sorted({0, 1, J // 2, J - 1})
    inv_drops = drops if J <= J_INVERSE_FULL_MAX else sorted({0, J - 1})
    for gauge in GAUGES:
        for drop in drops:
            M, rows = dc.gauged_jacobian(col, om, dc.C_ANCHOR, gauge=gauge, drop=drop)
            q[f"gauged_jacobian.rows(g={gauge},d={drop})"] = np.asarray(rows, dtype=float)
            if heavy:
                q[f"gauged_jacobian.M(g={gauge},d={drop})"] = M
        for a in _inverse_arm_alphas(J):
            for drop in inv_drops:
                v, A, M = dc.graded_inverse_norm(col, a, gauge=gauge, drop=drop)
                q[f"graded_inverse_norm.value(a={a},g={gauge},d={drop})"] = v
                if heavy:
                    q[f"graded_inverse_norm.A(a={a},g={gauge},d={drop})"] = A
    return q


def _sup_op_norm_quantities(dc):
    """sup_op_norm on explicitly 2-D input -- the only spelling any in-repo caller uses."""
    q = {}
    rng = np.random.default_rng(SEED)
    for i in range(40):
        n = int(rng.integers(2, 9))
        m = int(rng.integers(2, 9))
        A = rng.uniform(-10.0, 10.0, size=(n, m))
        wd = rng.uniform(0.5, 3.0, size=n)
        wc = rng.uniform(0.5, 3.0, size=m)
        q[f"sup_op_norm.2d[{i:02d}]"] = dc.sup_op_norm(A, wd, wc)
    return q


def run_clause_b(dc_post, dc_pre):
    n_quant = n_leaf = n_leaf_same = n_quant_same = 0
    moved = {}
    per_J = {}

    for J in J_FULL + J_CHEAP:
        heavy = J in J_FULL
        qp = _quantities(dc_post, J, heavy)
        qr = _quantities(dc_pre, J, heavy)
        assert set(qp) == set(qr), "coverage sets diverged -- harness bug, not a regression"
        jl = jls = 0
        for k in qp:
            n, same = bit_compare(qp[k], qr[k])
            n_quant += 1
            n_leaf += n
            n_leaf_same += same
            jl += n
            jls += same
            if same == n:
                n_quant_same += 1
            else:
                moved[f"J={J}::{k}"] = {"leaves": n, "identical": same,
                                        "post_digest": digest(qp[k]),
                                        "pre_digest": digest(qr[k])}
        per_J[str(J)] = {"heavy": heavy, "leaves": jl, "identical": jls}

    qp = _sup_op_norm_quantities(dc_post)
    qr = _sup_op_norm_quantities(dc_pre)
    for k in qp:
        n, same = bit_compare(qp[k], qr[k])
        n_quant += 1
        n_leaf += n
        n_leaf_same += same
        if same == n:
            n_quant_same += 1
        else:
            moved[k] = {"leaves": n, "identical": same}

    return {
        "n_quantities": n_quant,
        "n_quantities_bit_identical": n_quant_same,
        "n_float64_leaves": n_leaf,
        "n_float64_leaves_bit_identical": n_leaf_same,
        "n_leaves_moved": n_leaf - n_leaf_same,
        "moved": moved,
        "per_J": per_J,
        "J_full_matrix_arm": list(J_FULL),
        "J_vector_only_arm": list(J_CHEAP),
        "instrument": "sha256/uint64 view of raw IEEE-754 float64 bits; 0 ULP, not allclose",
        "leg151_quantity_count_for_scale": 1672,
        "blas_threads_pinned_to": os.environ.get("OMP_NUM_THREADS"),
        "why_threads_pinned": (
            "Multi-threaded BLAS picks its reduction order dynamically, so the last bit of a "
            "dot product can depend on how many threads were free. Clause (b) asserts 0 ULP, "
            "so the reduction order is fixed by construction rather than by luck. Measured "
            "side effect on this box with four legs running in parallel: a 400x400 "
            "np.linalg.inv took 3.5s unpinned and 0.0589s pinned, ~60x."),
        "declared_limit_inverse_arm": (
            "Every cheap quantity is swept at every J with the full 10-alpha set. The O(J^3) "
            "inverse arm is swept in full only to J = %d; above it the alpha set is %r and the "
            "drop set is {0, J-1}. Same shape as leg 151's own declared cap (its inverse arm "
            "stopped at J = 1000 while its cheap arm reached J = 2000)."
            % (J_INVERSE_FULL_MAX, list(ALPHAS_BIG))),
    }


# =========================================================================
# CLAUSE (b), second arm -- the capabilities.py validated line, byte for byte
# =========================================================================

_RUN_TEST = r"""
import importlib.util, runpy, sys
sys.path.insert(0, {repo!r})
import solver
if {pre!r}:
    spec = importlib.util.spec_from_file_location("solver.decay_collocation", {pre!r})
    m = importlib.util.module_from_spec(spec)
    sys.modules["solver.decay_collocation"] = m
    solver.decay_collocation = m
    spec.loader.exec_module(m)
runpy.run_path({test!r}, run_name="__main__")
"""


def run_validated_line(pre_path):
    """test_decay_collocation.py is what capabilities.py line 346 names as this module's
    validated line.  Run it twice in subprocesses -- against the shipped module, and against
    the pre-repair module substituted into sys.modules -- and compare stdout BYTE FOR BYTE.

    Its six gates print measured numbers, so byte-identical stdout is a stronger statement than
    'both passed': it says every number the repo's own known-answer gate reports is unmoved.
    """
    test = os.path.join(REPO, "test_decay_collocation.py")
    outs = {}
    for tag, pre in (("post_repair", None), ("pre_repair", pre_path)):
        code = _RUN_TEST.format(repo=REPO, pre=pre, test=test)
        r = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True)
        outs[tag] = {"returncode": r.returncode,
                     "stdout": r.stdout.decode(),
                     "stderr_tail": r.stderr.decode()[-400:]}
    a, b = outs["post_repair"]["stdout"], outs["pre_repair"]["stdout"]
    return {
        "capabilities_line": "capabilities.py:346 -> test_decay_collocation.py",
        "post_repair_returncode": outs["post_repair"]["returncode"],
        "pre_repair_returncode": outs["pre_repair"]["returncode"],
        "post_repair_passed": "ALL DECAY-COLLOCATION TESTS PASSED" in a,
        "pre_repair_passed": "ALL DECAY-COLLOCATION TESTS PASSED" in b,
        "stdout_bytes_identical": a == b,
        "stdout_sha256_post": hashlib.sha256(a.encode()).hexdigest()[:16],
        "stdout_sha256_pre": hashlib.sha256(b.encode()).hexdigest()[:16],
        "n_gate_lines": a.count("[ok]"),
        "stdout_post": a,
        "stderr_tail_post": outs["post_repair"]["stderr_tail"],
        "stderr_tail_pre": outs["pre_repair"]["stderr_tail"],
    }


# =========================================================================
# CLAUSE (b), third arm -- the inheritance arm
# =========================================================================

def run_inheritance_arm(dc_pre):
    """solver/collocation_newton.py's ACollocation SUBCLASSES Collocation and was NOT edited by
    leg 151.  A guard added to a base class can change a subclass's behaviour without the
    subclass's own file changing at all, so the arm is measured rather than assumed.
    """
    import solver.collocation_newton as cn
    out = {"module_edited_by_leg151": False, "checks": {}}
    n_leaf = n_same = 0
    for J in (16, 64, 200):
        for K in (2, 4):
            ac = cn.ACollocation(J, K) if _takes_two(cn.ACollocation) else cn.ACollocation(J)
            base_q = {"theta": ac.theta, "X": ac.X, "H": ac.H, "D": ac.D,
                      "transport": ac.transport, "anchor": ac.anchor()}
            pre_col = dc_pre.Collocation(J)
            pre_q = {"theta": pre_col.theta, "X": pre_col.X, "H": pre_col.H, "D": pre_col.D,
                     "transport": pre_col.transport, "anchor": pre_col.anchor()}
            for k in base_q:
                n, same = bit_compare(base_q[k], pre_q[k])
                n_leaf += n
                n_same += same
                out["checks"][f"J={J},K={K}::{k}"] = {"leaves": n, "identical": same}
            break     # ACollocation's extra args do not affect the inherited base quantities
    out["n_leaves"] = n_leaf
    out["n_leaves_bit_identical"] = n_same
    return out


def _takes_two(cls):
    import inspect
    try:
        return len(inspect.signature(cls.__init__).parameters) > 2
    except (TypeError, ValueError):
        return False


# =========================================================================

def main():
    dc_pre = load_pre_repair()
    import solver.decay_collocation as dc_post

    a = run_clause_a(dc_post, dc_pre)
    b = run_clause_b(dc_post, dc_pre)
    vline = run_validated_line(dc_pre.__source_path__)
    inh = run_inheritance_arm(dc_pre)

    sa = a["summary"]["post_repair"]["ALL"]
    ctrl = a["lesson90_control"]
    # The gate's own wording is "reject or CORRECTLY FLAG every one of leg 115's original 3
    # failing cases", so the criterion is that no case is answered SILENTLY -- with the control
    # attached, because a suite that refused everything would satisfy it vacuously.
    clause_a_yes = (sa[SILENT_VALUE] == 0
                    and sa[REFUSED] + sa[FLAGGED] == sa["n"]
                    and ctrl["comparison_can_come_out_differently"])
    clause_b_yes = (b["n_leaves_moved"] == 0 and vline["stdout_bytes_identical"]
                    and vline["post_repair_passed"]
                    and inh["n_leaves"] == inh["n_leaves_bit_identical"])

    result = {
        "leg": 167,
        "route": "DCB",
        "branch": "leg/167-dcb-v1",
        "date": "2026-08-06",
        "module_under_check": "solver/decay_collocation.py",
        "module_edited_by_this_leg": False,
        "closes": "leg 151 (Route-DCR), which repaired leg 115's (Route-DCA) three findings",
        "gate": ("Post-repair, does solver/decay_collocation.py (a) reject or correctly flag "
                 "every one of leg 115's original 3 failing cases in an independent re-run, "
                 "and (b) reproduce every previously-validated result bit-identically?"),
        "refs": {
            "pre_repair": PRE_REPAIR_REF,
            "repair": REPAIR_REF,
            "leg115_battery_and_runner": LEG115_REF,
            "pre_repair_source_sha256": dc_pre.__source_sha256__,
            "note": ("git log --oneline main -- solver/decay_collocation.py returns exactly "
                     "two commits, so the pre/post boundary needs no judgement call."),
        },
        "clause_a_reject_or_flag": a,
        "clause_b_zero_regression": b,
        "clause_b_validated_line": vline,
        "clause_b_inheritance_arm": inh,
        "gate_answer": {
            "clause_a": "YES" if clause_a_yes else "NO",
            "clause_b": "YES" if clause_b_yes else "NO",
            "overall": "YES" if (clause_a_yes and clause_b_yes) else "NO",
        },
        "what_a_clean_clause_b_does_NOT_mean": (
            "Golden-master / characterization testing does not infer correctness (Feathers; "
            "see writeup/novelty/leg_167.md Q1). A 0-ULP result says THE REPAIR MOVED NOTHING. "
            "It does not say any banked number is right."),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(result, fh, indent=2, default=str)

    print("=" * 78)
    print("LEG 167 -- ROUTE-DCB: post-repair regression check, solver/decay_collocation.py")
    print("=" * 78)
    print("\nCLAUSE (a) -- leg 115's cases, re-run independently (cases read from git @%s):"
          % LEG115_REF)
    for arm in ("pre_repair_control", "post_repair"):
        print("  %-20s" % arm, end="")
        for g in ("G1", "G2", "G3", "ALL"):
            t = a["summary"][arm][g]
            print("  %s n=%d ref=%d flag=%d SILENT=%d" %
                  (g, t["n"], t[REFUSED], t[FLAGGED], t[SILENT_VALUE]), end="")
        print()
    print("  lesson-90 control: pre-repair SILENT=%d, post-repair SILENT=%d, "
          "can-come-out-differently=%s"
          % (ctrl["pre_repair_silent_values"], ctrl["post_repair_silent_values"],
             ctrl["comparison_can_come_out_differently"]))
    print("  refusal exception types: %r" % (a["refusal_exception_types"],))
    over = [k for k, v in a["no_over_refusal_probes"].items() if v["outcome"] != SILENT_VALUE]
    print("  over-refusal probes that did NOT return a clean value: %d of %d %r"
          % (len(over), len(a["no_over_refusal_probes"]), over))

    print("\nCLAUSE (b) -- same-process bitwise differential vs %s:" % PRE_REPAIR_REF)
    print("  quantities  %d / %d bit-identical" % (b["n_quantities_bit_identical"],
                                                   b["n_quantities"]))
    print("  float64 leaves %d / %d bit-identical at 0 ULP  (moved: %d)"
          % (b["n_float64_leaves_bit_identical"], b["n_float64_leaves"], b["n_leaves_moved"]))
    print("  capabilities.py validated line: post passed=%s, stdout byte-identical pre/post=%s "
          "(%d gate lines)" % (vline["post_repair_passed"], vline["stdout_bytes_identical"],
                               vline["n_gate_lines"]))
    print("  inheritance arm (ACollocation): %d / %d leaves bit-identical"
          % (inh["n_leaves_bit_identical"], inh["n_leaves"]))

    print("\nGATE: clause (a) = %s, clause (b) = %s, overall = %s"
          % (result["gate_answer"]["clause_a"], result["gate_answer"]["clause_b"],
             result["gate_answer"]["overall"]))
    print("wrote %s" % OUT)
    return result


if __name__ == "__main__":
    main()
