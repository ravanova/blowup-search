"""Route-BOB v1 -- the POST-REPAIR REGRESSION CHECK of solver/boussinesq.py, closing the
loop on leg 89 (Route-BOA), the most severe finding of the adversarial-audit run.

Leg 133. Companion in kind to legs 86 (port_certification), 103 (interval), 104
(boussinesq_velocity) and 105 (target_norm). Leg 89 found FOUR silent-corruption defects in
solver/boussinesq.py -- headline a false `blowup_candidate` triggered off a represented
initial vorticity of 1.797e-16 amplified 5.566e13x by ordinary dealiasing noise -- and its
bench-repair (branch `bench/fix-boussinesq-silent-corruption`, commit 0c54d8a, merged
14b2e98) landed with a banked-result audit concluding no Phase-1 number was affected.

THE GATE, VERBATIM (DIRECTION.md, "### 133 -- ROUTE-BOB")
--------------------------------------------------------
"Post-repair, does solver/boussinesq.py (a) pass leg 89's full original battery -- no false
blowup_candidate under dealiasing noise, kappa honored, NaNs propagated or flagged -- and
(b) reproduce the banked n=32 Boussinesq results bit-identically, confirming the repair's
no-contamination conclusion independently?"
  yes -> Repair confirmed solid and non-regressive; the severest finding of the run is
         fully closed. Bank leg 89's battery as a permanent regression suite.
  no  -> An incomplete fix, a repair regression, or a contamination the repair's own audit
         missed. Report the exact case precisely; escalate as a PRIORITY finding, do not
         patch under this leg's own authority.

WHY THIS LEG EXISTS AND WHY IT DOES NOT TRUST THE REPAIR'S OWN REPORT
---------------------------------------------------------------------
The only existing evidence for both halves of the gate is
`writeup/data/bench_boussinesq_silent_corruption_check.json` -- produced by the repair
branch, grading its own homework. Leg 60 taught this repository not to accept a repair's own
claim as the only evidence. Every number this leg reports is therefore re-derived here:
the battery re-run, the call-site scan, the banked-artifact scan and the Phase-1
reproduction are all independent implementations reading only the banked JSONs and the live
module.

THE CONTROL THAT CAN COME OUT DIFFERENTLY (lesson 90)
-----------------------------------------------------
"0 silent cases" is worthless on its own: a harness that classified nothing would report the
same. PART 2 therefore runs the identical 90 cases against the PRE-REPAIR module source,
recovered from git blob 2b787e4 (`git show 4959e6b:solver/boussinesq.py`) and injected as
`solver.boussinesq` in a subprocess before the battery imports it. It must reproduce leg
89's banked 19 / 4 / 13 -- and, case by case, leg 89's banked per-case verdict for all 90.
If it does not, the post-repair zeros are measuring a broken harness, not a fixed module,
and this leg's gate cannot be answered. Four identical zeros with nothing that could have
made them non-zero is exactly the shape lesson 90 bans.

INDEPENDENCE, AND ITS HONEST CEILING
------------------------------------
PART 1 and PART 2 reuse leg 89's case constructors and its `run_case` classifier, because
"leg 89's full original battery" IS that instrument -- re-implementing 90 cases would be
less faithful, not more. The verdict predicate is therefore inherited, and that is stated
rather than hidden. PART 3 compensates: five defect probes written from the DEFECT
DESCRIPTIONS, in this file's own code, touching none of leg 89's, each measuring the
before/after magnitude of the thing that used to go wrong.

Provenance is checked, not assumed (PART 0): leg 89's battery file was touched by the
repair commit, so this file verifies that the +34-line diff is confined to `main()`'s
payload and that every case constructor and the classifier are byte-identical to leg 89's
original blob.

MODULE IS READ-ONLY. solver/boussinesq.py is not edited by this leg under EITHER gate
outcome. A contamination the repair's audit missed is escalated as a PRIORITY finding,
never patched here.

Leg 89's own artifact `writeup/data/p2_route_boa_v1_adversarial.json` is READ and never
written: this file never calls the battery's `main()`, only its family constructors.

Run: .venv/bin/python experiments/p2_route_bob_v1_postrepair.py
Writes: writeup/data/p2_route_bob_v1_postrepair.json
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import ast  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)

OUT = os.path.join(REPO, "writeup", "data", "p2_route_bob_v1_postrepair.json")

# Leg 89's commit: solver/boussinesq.py was untouched by that leg, so this blob is the
# PRE-REPAIR module. Verified equal to 0c54d8a^:solver/boussinesq.py (blob 2b787e4).
PRE_FIX_REV = "4959e6b"
BATTERY_REL = "experiments/p2_route_boa_v1_adversarial.py"
BATTERY_ABS = os.path.join(REPO, BATTERY_REL)
LEG89_ARTIFACT = os.path.join(REPO, "writeup", "data", "p2_route_boa_v1_adversarial.json")
BENCH_ARTIFACT = os.path.join(REPO, "writeup", "data",
                              "bench_boussinesq_silent_corruption_check.json")
PHASE1_SPIKE = os.path.join(REPO, "writeup", "data", "phase1_spike.json")

N = 32
T_MAX = 0.3

GATE_FAMILIES = ["A_degenerate_streamfunction", "B_nan_seeded_vorticity",
                 "C_nan_seeded_temperature", "D_out_of_domain_coefficient",
                 "E_degenerate_discretization"]


def _git(*args):
    return subprocess.check_output(["git", "-C", REPO, *args])


def _jsonable(x):
    if isinstance(x, float):
        if np.isnan(x):
            return "nan"
        if np.isinf(x):
            return "inf" if x > 0 else "-inf"
    return x


# ---------------------------------------------------------------------------
# PART 0 -- provenance: is the battery on disk still leg 89's battery?
# ---------------------------------------------------------------------------
def part0_provenance():
    """The repair commit touched leg 89's battery file (+34 lines). Establish that the
    change is confined to `main()`'s payload dict, so importing family_a..family_f from
    the file at HEAD really is running leg 89's ORIGINAL battery.

    The split point is the `def main(` line: everything above it is the case
    constructors, the verdict vocabulary and `run_case`, i.e. the entire instrument.
    """
    orig = _git("show", f"{PRE_FIX_REV}:{BATTERY_REL}").decode()
    with open(BATTERY_ABS) as fh:
        head = fh.read()
    marker = "\ndef main("
    o_pre, h_pre = orig.split(marker)[0], head.split(marker)[0]
    solver_pre = _git("show", f"{PRE_FIX_REV}:solver/boussinesq.py")
    solver_now = open(os.path.join(REPO, "solver", "boussinesq.py"), "rb").read()
    return {
        "battery_file": BATTERY_REL,
        "leg89_rev": PRE_FIX_REV,
        "instrument_bytes_compared": len(o_pre),
        "instrument_sha256_leg89": hashlib.sha256(o_pre.encode()).hexdigest(),
        "instrument_sha256_head": hashlib.sha256(h_pre.encode()).hexdigest(),
        "instrument_byte_identical": o_pre == h_pre,
        "battery_total_bytes_leg89": len(orig),
        "battery_total_bytes_head": len(head),
        "battery_delta_bytes_in_main_payload": len(head) - len(orig),
        "solver_sha256_prerepair": hashlib.sha256(solver_pre).hexdigest(),
        "solver_sha256_postrepair": hashlib.sha256(solver_now).hexdigest(),
        "solver_changed_by_repair": solver_pre != solver_now,
        "note": ("if instrument_byte_identical is False the rest of this run is not "
                 "'leg 89's original battery' and the gate cannot be answered from it"),
    }


# ---------------------------------------------------------------------------
# PARTS 1 & 2 -- the 90-case battery, against the repaired and the pre-repair module
# ---------------------------------------------------------------------------
def _census(cases):
    families = {}
    for c in cases:
        f = families.setdefault(c["family"], {"n_cases": 0, "verdicts": {},
                                              "silent_labels": []})
        f["n_cases"] += 1
        f["verdicts"][c["verdict"]] = f["verdicts"].get(c["verdict"], 0) + 1
        if c["verdict"] == "silent":
            f["silent_labels"].append(c["label"])
    n_silent_gate = sum(1 for c in cases
                        if c["verdict"] == "silent" and c["family"] in GATE_FAMILIES)
    n_silent_secondary = sum(1 for c in cases
                             if c["verdict"] == "silent" and c["family"] not in GATE_FAMILIES)
    n_masked = sum(1 for c in cases if c.get("guard_masks_a_nan_limb"))
    return {
        "n_cases": len(cases),
        "families": families,
        "n_silent_gate_deciding": n_silent_gate,
        "n_silent_secondary": n_silent_secondary,
        "n_cases_where_conservation_drift_masks_a_nan_limb": n_masked,
        "leg89_gate_answer": "YES" if n_silent_gate > 0 else "NO",
        "verdict_by_label": {c["label"]: c["verdict"] for c in cases},
        "exception_by_label": {c["label"]: c["exception"]
                               for c in cases if "exception" in c},
    }


def run_battery():
    """Run all 90 of leg 89's cases against whatever `solver.boussinesq` currently is.

    Imports the family constructors ONLY. `main()` is never called, so leg 89's frozen
    artifact writeup/data/p2_route_boa_v1_adversarial.json is never written.
    """
    import experiments.p2_route_boa_v1_adversarial as boa
    cases = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # the poisoned cases warn by design
        for fn in (boa.family_a, boa.family_b, boa.family_c,
                   boa.family_d, boa.family_e, boa.family_f):
            cases.extend(fn())
    return cases


def load_prerepair_solver():
    """Inject git blob 2b787e4 as `solver.boussinesq` BEFORE the battery imports it.

    Must be called in a fresh process, before `experiments.p2_route_boa_v1_adversarial`
    is imported -- that module does `from solver.boussinesq import ...` at import time and
    would otherwise bind the repaired functions.
    """
    assert "experiments.p2_route_boa_v1_adversarial" not in sys.modules, \
        "battery already imported: the pre-repair injection would be a no-op"
    src = _git("show", f"{PRE_FIX_REV}:solver/boussinesq.py").decode()
    tmpdir = tempfile.mkdtemp(prefix="leg133_prerepair_")
    path = os.path.join(tmpdir, "boussinesq_prerepair.py")
    with open(path, "w") as fh:
        fh.write(src)
    import solver  # the package must exist before we graft a submodule onto it
    spec = importlib.util.spec_from_file_location("solver.boussinesq", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["solver.boussinesq"] = mod
    spec.loader.exec_module(mod)
    setattr(solver, "boussinesq", mod)
    # Positive identification of WHICH source is loaded, both directions.
    assert not hasattr(mod, "_guard_max"), \
        "injected module has the repair's _guard_max: it is NOT the pre-repair source"
    assert not hasattr(mod, "ZERO_OMEGA_REL_TOL"), \
        "injected module has the repair's ZERO_OMEGA_REL_TOL: not the pre-repair source"
    return mod


def compare_to_leg89_artifact(census):
    """Case-by-case agreement between this leg's pre-repair re-run and leg 89's banked
    artifact. This is the sharpest form of the control: not just the totals, but all 90
    verdicts."""
    with open(LEG89_ARTIFACT) as fh:
        banked = json.load(fh)
    banked_verdicts = {c["label"]: c["verdict"] for c in banked["cases"]}
    mine = census["verdict_by_label"]
    common = sorted(set(banked_verdicts) & set(mine))
    disagreements = {lab: {"banked": banked_verdicts[lab], "rerun": mine[lab]}
                     for lab in common if banked_verdicts[lab] != mine[lab]}
    return {
        "banked_artifact": "writeup/data/p2_route_boa_v1_adversarial.json",
        "banked_n_cases": banked["n_cases"],
        "rerun_n_cases": census["n_cases"],
        "labels_only_in_banked": sorted(set(banked_verdicts) - set(mine)),
        "labels_only_in_rerun": sorted(set(mine) - set(banked_verdicts)),
        "n_labels_compared": len(common),
        "n_verdicts_agreeing": len(common) - len(disagreements),
        "n_verdicts_disagreeing": len(disagreements),
        "disagreements": disagreements,
        "banked_totals": {
            "n_silent_gate_deciding": banked["n_silent_gate_deciding"],
            "n_silent_secondary": banked["n_silent_secondary"],
            "n_cases_where_conservation_drift_masks_a_nan_limb":
                banked["n_cases_where_conservation_drift_masks_a_nan_limb"],
            "gate_answer": banked["gate_answer"],
        },
        "rerun_totals": {
            "n_silent_gate_deciding": census["n_silent_gate_deciding"],
            "n_silent_secondary": census["n_silent_secondary"],
            "n_cases_where_conservation_drift_masks_a_nan_limb":
                census["n_cases_where_conservation_drift_masks_a_nan_limb"],
            "gate_answer": census["leg89_gate_answer"],
        },
    }


# ---------------------------------------------------------------------------
# PART 3 -- independent defect probes, written from the DEFECT DESCRIPTIONS
# ---------------------------------------------------------------------------
def part3_defect_probes():
    """Five probes in this file's own code, sharing nothing with leg 89's battery.

    Each returns the SAME dict shape whichever module is loaded, so the pre-repair and
    post-repair arms are directly comparable and the magnitude of what changed is
    reported, never a boolean. `raised` is the repaired behaviour; the accompanying
    magnitude is what the pre-repair module produced instead.
    """
    from solver.boussinesq import dealias_mask2d, grid2d, solve_boussinesq

    X, Y = grid2d(N)
    w0 = np.sin(X) * np.sin(Y)
    th0 = np.cos(X) * np.sin(Y)
    probes = {}

    def attempt(name, fn):
        try:
            probes[name] = fn()
            probes[name]["raised"] = False
        except Exception as exc:  # noqa: BLE001 -- the exception IS the repaired behaviour
            probes[name] = {"raised": True,
                            "exception": f"{type(exc).__name__}: {exc}"}

    # --- DEFECT 1: false blowup_candidate off dealiasing noise -----------------
    # A vorticity living entirely above the 2/3 cut is annihilated by the mask, so the
    # represented m0 is roundoff and `amplification_factor*m0` is a roundoff-scale
    # threshold that O(1) buoyancy clears in one step.
    def d1():
        w_kill = np.sin(15 * X) * np.sin(15 * Y)
        mask = dealias_mask2d(N)
        rep = float(np.max(np.abs(np.fft.ifft2(np.fft.fft2(w_kill) * mask).real)))
        r = solve_boussinesq(w_kill, th0, t_max=T_MAX)
        m0 = float(r.max_omega[0])
        return {"represented_m0_independently_computed": rep,
                "m0_reported_by_module": m0,
                "outcome": r.outcome,
                "amplification": _jsonable(float(r.max_omega[-1] / m0) if m0 else
                                           float("inf")),
                "false_blowup_label_emitted": r.outcome == "blowup_candidate"}
    attempt("defect1_false_blowup_dealias_annihilated", d1)

    def d1b():
        r = solve_boussinesq(1e-300 * w0, th0, t_max=T_MAX)
        m0 = float(r.max_omega[0])
        return {"m0_reported_by_module": m0, "outcome": r.outcome,
                "amplification": _jsonable(float(r.max_omega[-1] / m0) if m0 else
                                           float("inf")),
                "false_blowup_label_emitted": r.outcome == "blowup_candidate"}
    attempt("defect1_false_blowup_denormal_1e-300", d1b)

    # --- DEFECT 2: nu/kappa outside [0,inf) neither applied nor rejected --------
    # Witness is bit-for-bit equality against the neutral (coefficient = 0) run: identical
    # arrays prove the integration that executed is not the one requested. "Both small" is
    # not accepted. kappa is the sharper case -- the energy identity does not contain it,
    # so no diagnostic could ever have caught it.
    ctrl = solve_boussinesq(w0, th0, t_max=T_MAX)
    ctrl_w, ctrl_th = ctrl.omega_final.copy(), ctrl.theta_final.copy()

    def d2(name, val):
        def go():
            r = solve_boussinesq(w0, th0, t_max=T_MAX, **{name: val})
            return {"requested_coefficient": _jsonable(float(r.params[name])),
                    "bit_identical_omega_to_zero_coefficient_run":
                        bool(np.array_equal(r.omega_final, ctrl_w)),
                    "bit_identical_theta_to_zero_coefficient_run":
                        bool(np.array_equal(r.theta_final, ctrl_th)),
                    "max_abs_diff_omega": float(np.max(np.abs(
                        r.omega_final - ctrl_w))),
                    "outcome": r.outcome}
        return go
    attempt("defect2_kappa_negative_dropped", d2("kappa", -0.5))
    attempt("defect2_nu_negative_dropped", d2("nu", -0.5))
    attempt("defect2_kappa_nan_dropped", d2("kappa", float("nan")))
    # Control: an IN-DOMAIN coefficient must still be honoured, i.e. must NOT be
    # bit-identical to the neutral run. A module that refused everything would pass every
    # probe above and fail this one.
    attempt("CONTROL_defect2_kappa_in_domain_0.5", d2("kappa", 0.5))
    attempt("CONTROL_defect2_nu_in_domain_0.5", d2("nu", 0.5))

    # --- DEFECT 3: builtin max drops a NaN limb --------------------------------
    # A 100%-NaN theta with buoyancy off keeps the vorticity clean, so max_omega looks
    # healthy; the question is whether the NaN reaches conservation_drift.
    def d3():
        th_nan = np.full((N, N), np.nan)
        r = solve_boussinesq(w0, th_nan, t_max=T_MAX, buoyancy=False, drift_guard=1e-9)
        limbs = (float(r.mean_drift), float(r.energy_balance_residual))
        return {"nan_fraction_theta_final": float(np.mean(~np.isfinite(r.theta_final))),
                "conservation_drift": _jsonable(float(r.conservation_drift)),
                "mean_drift": _jsonable(limbs[0]),
                "energy_balance_residual": _jsonable(limbs[1]),
                "outcome": r.outcome,
                "early_exit_reason": r.early_exit_reason,
                "guard_masks_a_nan_limb": bool(
                    any(v != v for v in limbs) and np.isfinite(r.conservation_drift))}
    attempt("defect3_nan_limb_masked_by_builtin_max", d3)

    # --- DEFECT 4: degenerate grid, mask retains only the mean mode -------------
    def d4(n):
        def go():
            Xn, Yn = grid2d(n)
            wn = np.sin(Xn) * np.sin(Yn) + 0.5
            thn = np.cos(Xn) * np.sin(Yn) + 0.5
            n_modes = int(np.sum(dealias_mask2d(n)))
            r = solve_boussinesq(wn, thn, t_max=T_MAX)
            return {"n": n, "retained_modes_after_dealias": n_modes,
                    "outcome": r.outcome, "n_timesteps": int(r.n_timesteps),
                    "conservation_drift": _jsonable(float(r.conservation_drift))}
        return go
    attempt("defect4_degenerate_grid_n1", d4(1))
    attempt("defect4_degenerate_grid_n2", d4(2))
    # Control: the smallest grid that CAN represent a non-constant field must still run.
    attempt("CONTROL_defect4_grid_n3_still_runs", d4(3))

    # --- DEFECT 2b: non-finite CFL safety factor removes its `min` limb ---------
    big = 5.0 * w0
    ref = solve_boussinesq(big, th0, t_max=T_MAX, dt_max=1.0)
    ref_dt = float(ref.dt_min)

    def d5():
        r = solve_boussinesq(big, th0, t_max=T_MAX, dt_max=1.0,
                             c1=float("nan"), c2=float("nan"))
        return {"dt_min": _jsonable(float(r.dt_min)),
                "dt_min_of_control": ref_dt,
                "dt_relaxation_factor": _jsonable(float(r.dt_min) / ref_dt),
                "n_timesteps": int(r.n_timesteps),
                "outcome": r.outcome}
    attempt("defect5_nonfinite_cfl_factor_relaxes_dt", d5)

    def d6():
        r = solve_boussinesq(w0, th0, t_max=6.0, amplification_factor=float("nan"))
        peak = float(np.max(r.max_omega))
        return {"outcome": r.outcome,
                "peak_amplification_reached": _jsonable(peak / float(r.max_omega[0])),
                "detection_disabled_but_reported_no_blowup":
                    r.outcome == "no_blowup"}
    attempt("defect5_nonfinite_amplification_factor_disables_detection", d6)

    return probes


# ---------------------------------------------------------------------------
# PART 4 -- the banked-result audit, re-derived from the banked JSONs
# ---------------------------------------------------------------------------
def part5_zero_regression_n32():
    """The gate's clause (b), taken literally: do the WELL-FORMED n=32 runs come out
    bit-identically before and after the repair?

    Fourteen configurations covering every branch of the solver a caller can reach -- each
    outcome the module can emit, both guards, both physics switches, the symmetry
    projection, frozen-u transport, and the degenerate t_max=0 request. Both final arrays
    are hashed byte-for-byte (`.tobytes()` on a C-contiguous float64 array, so the hash
    is of the exact bit pattern, not of a rounded repr) and every scalar the result
    carries is recorded to full precision.

    Run in BOTH arms; the comparison is done in the main process. This is computed by
    this leg, on this leg's own roster -- the repair's own part A used 19 cases of its own
    choosing, and agreement between two independently chosen rosters is the point.
    """
    from solver.boussinesq import grid2d, solve_boussinesq

    X, Y = grid2d(N)
    w0 = np.sin(X) * np.sin(Y)
    th0 = np.cos(X) * np.sin(Y)
    big = 5.0 * w0

    roster = {
        "inviscid_default": (w0, th0, dict(t_max=T_MAX)),
        "viscous_nu_and_kappa": (w0, th0, dict(t_max=T_MAX, nu=0.05, kappa=0.02)),
        "kappa_only": (w0, th0, dict(t_max=T_MAX, kappa=0.02)),
        "nu_only": (w0, th0, dict(t_max=T_MAX, nu=0.05)),
        "buoyancy_off": (w0, th0, dict(t_max=T_MAX, buoyancy=False)),
        "nonlinear_off": (w0, th0, dict(t_max=T_MAX, nonlinear=False)),
        "pure_diffusion": (w0, th0, dict(t_max=T_MAX, nonlinear=False, nu=0.05,
                                         kappa=0.05)),
        "houluo_symmetry": (w0, th0, dict(t_max=T_MAX, symmetry="houluo")),
        "frozen_u": (w0, th0, dict(t_max=T_MAX, frozen_u=(0.3, -0.2))),
        "drift_guard_cold": (w0, th0, dict(t_max=T_MAX, drift_guard=1.0)),
        "drift_guard_hot_negative": (w0, th0, dict(t_max=T_MAX, drift_guard=-1.0)),
        "tail_guard_cold": (w0, th0, dict(t_max=T_MAX, tail_guard=1.0)),
        "max_steps_branch": (big, th0, dict(t_max=6.0, max_steps=5)),
        "blowup_candidate_real": (w0, th0, dict(t_max=6.0, amplification_factor=2.0)),
        "t_max_zero": (w0, th0, dict(t_max=0.0)),
    }
    out = {}
    for label, (a, b, kw) in roster.items():
        r = solve_boussinesq(a, b, **kw)
        out[label] = {
            "outcome": r.outcome,
            "early_exit_reason": r.early_exit_reason,
            "n_timesteps": int(r.n_timesteps),
            "t_final": repr(float(r.t_final)),
            "dt_min": repr(float(r.dt_min)),
            "mean_drift": repr(float(r.mean_drift)),
            "energy_balance_residual": repr(float(r.energy_balance_residual)),
            "conservation_drift": repr(float(r.conservation_drift)),
            "max_tail_fraction": repr(float(r.max_tail_fraction)),
            "sha256_omega_final": hashlib.sha256(
                np.ascontiguousarray(r.omega_final, dtype=np.float64).tobytes()
            ).hexdigest(),
            "sha256_theta_final": hashlib.sha256(
                np.ascontiguousarray(r.theta_final, dtype=np.float64).tobytes()
            ).hexdigest(),
            "sha256_max_omega_trajectory": hashlib.sha256(
                np.ascontiguousarray(r.max_omega, dtype=np.float64).tobytes()
            ).hexdigest(),
        }
    return out


def compare_zero_regression(pre, post):
    cases = {}
    n_identical = 0
    for label in sorted(set(pre) | set(post)):
        p, q = pre.get(label), post.get(label)
        if p is None or q is None:
            cases[label] = {"present_in_both": False}
            continue
        differing = sorted(k for k in p if p[k] != q.get(k))
        same = not differing
        n_identical += int(same)
        cases[label] = {"present_in_both": True, "bit_identical": same,
                        "outcome": q["outcome"],
                        "n_timesteps": q["n_timesteps"],
                        "differing_fields": differing,
                        **({"prerepair": {k: p[k] for k in differing},
                            "postrepair": {k: q[k] for k in differing}}
                           if differing else {})}
    return {"n_cases": len(cases), "n_bit_identical": n_identical,
            "n_differing": len(cases) - n_identical,
            "grid_n": N,
            "hash_basis": "sha256 of the float64 bit pattern of omega_final, "
                          "theta_final and the max_omega trajectory, plus repr() of "
                          "every scalar the result carries",
            "cases": cases}


# Loudness order. The repair may only move a case UP this ladder; a case that gets
# quieter is a repair regression whatever the totals say.
_LOUDNESS = {"silent": 0, "benign": 1, "propagated": 2, "flagged": 3, "raised": 4}


def verdict_transitions(pre_census, post_census, post_cases):
    """Case-by-case movement, and its DIRECTION.

    "0 silent cases" is a total; what actually decides whether the repair is
    non-regressive is that no case moved DOWN the loudness ladder. `benign` is the
    subtle one: leg 89's `benign` means only "no witness fired", which for a malformed
    input is not the same as "the input was valid" -- so a benign -> raised move is a
    tightening, and a benign -> silent move would be a catastrophe. Both are counted.
    """
    pre, post = pre_census["verdict_by_label"], post_census["verdict_by_label"]
    exc = post_census.get("exception_by_label", {})
    invalid_because = {c["label"]: c.get("invalid_because", "") for c in post_cases}
    matrix = {}
    quieter, louder, unchanged = [], [], 0
    for label in sorted(set(pre) & set(post)):
        a, b = pre[label], post[label]
        key = f"{a}->{b}"
        matrix[key] = matrix.get(key, 0) + 1
        if _LOUDNESS[b] < _LOUDNESS[a]:
            quieter.append({"label": label, "from": a, "to": b})
        elif _LOUDNESS[b] > _LOUDNESS[a]:
            louder.append({"label": label, "from": a, "to": b,
                           "exception": exc.get(label, "")[:200],
                           "invalid_because": invalid_because.get(label, "")[:200]})
        else:
            unchanged += 1
    return {
        "n_labels_compared": len(set(pre) & set(post)),
        "transition_matrix": dict(sorted(matrix.items(), key=lambda kv: -kv[1])),
        "loudness_order": _LOUDNESS,
        "n_unchanged": unchanged,
        "n_moved_louder": len(louder),
        "n_moved_quieter": len(quieter),
        "moved_quieter": quieter,
        "moved_louder": louder,
        "note": ("n_moved_quieter is the repair-regression counter: any case whose "
                 "verdict got softer would be a defect introduced by the fix. Each "
                 "louder move carries the case's own `invalid_because` so an "
                 "over-refusal of VALID input would be visible as a tightening on a "
                 "case whose justification does not describe a malformed input."),
    }


def part4a_call_sites():
    """Every `solve_boussinesq(...)` call site in the repository, and the `kappa`/`nu` it
    passes -- found by parsing the AST, not by grepping for a literal.

    Defect 2 can only have contaminated a banked number if some call site ever passed an
    out-of-domain coefficient. A site that omits the keyword gets the signature default,
    which is read from the live function, not assumed.
    """
    import inspect

    from solver.boussinesq import solve_boussinesq
    sig = inspect.signature(solve_boussinesq)
    defaults = {k: sig.parameters[k].default for k in ("nu", "kappa")}

    def literal_of(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value), "literal"
        if (isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub)
                and isinstance(node.operand, ast.Constant)):
            return -float(node.operand.value), "negated_literal"
        return None, ast.dump(node)[:80]

    sites = []
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", ".venv", "__pycache__", "Papers", ".claude")]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, REPO)
            try:
                with open(path) as fh:
                    tree = ast.parse(fh.read(), filename=rel)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                f = node.func
                name = (f.id if isinstance(f, ast.Name)
                        else f.attr if isinstance(f, ast.Attribute) else None)
                if name != "solve_boussinesq":
                    continue
                rec = {"file": rel, "line": node.lineno}
                for key in ("nu", "kappa"):
                    kw = next((k for k in node.keywords if k.arg == key), None)
                    if kw is None:
                        rec[key] = _jsonable(float(defaults[key]))
                        rec[f"{key}_source"] = "signature_default"
                    else:
                        val, how = literal_of(kw.value)
                        rec[key] = _jsonable(val) if val is not None else None
                        rec[f"{key}_source"] = how
                sites.append(rec)

    def out_of_domain(rec, key):
        v = rec[key]
        if v is None:
            return None  # not a literal: resolved separately below
        return not (isinstance(v, float) and np.isfinite(v) and v >= 0.0)

    # Sites in this leg's OWN files deliberately pass out-of-domain values (that is what
    # the probes test) and are excluded from the contamination verdict, but reported.
    own = {"experiments/p2_route_bob_v1_postrepair.py", "test_boussinesq_postrepair.py",
           "experiments/p2_route_boa_v1_adversarial.py", "test_boussinesq_adversarial.py",
           "experiments/bench_boussinesq_silent_corruption_check.py"}
    production = [s for s in sites if s["file"] not in own]
    unresolved = [s for s in production
                  if s["nu"] is None or s["kappa"] is None]
    bad = [s for s in production
           if (out_of_domain(s, "nu") is True) or (out_of_domain(s, "kappa") is True)]
    return {
        "n_call_sites_total": len(sites),
        "n_call_sites_in_audit_or_test_files": len(sites) - len(production),
        "n_production_call_sites": len(production),
        "production_call_sites": production,
        "n_production_sites_with_non_literal_coefficient": len(unresolved),
        "non_literal_sites": unresolved,
        "n_production_sites_with_out_of_domain_coefficient": len(bad),
        "out_of_domain_sites": bad,
    }


def part4a2_resolve_nonliteral_sites():
    """The AST scan above resolves a coefficient only when it is a literal. Eight sites
    pass a variable, and a contamination by defect 2 could hide in exactly one of those.
    Resolve each by reading the code that binds it -- and, crucially, check the domain of
    the values the BANKED ARTIFACTS actually record, which is a measurement rather than a
    reading of the source.
    """
    from ga.fitness2d import FITNESS2D_DEFAULTS
    return {
        "ga/fitness2d.py:70": {
            "kappa_expression": "cfg['kappa']",
            "kappa_default": _jsonable(float(FITNESS2D_DEFAULTS["kappa"])),
            "kappa_default_in_domain": bool(
                np.isfinite(FITNESS2D_DEFAULTS["kappa"])
                and FITNESS2D_DEFAULTS["kappa"] >= 0.0),
            "fitness_axis": FITNESS2D_DEFAULTS["fitness_axis"],
            "nu_expression": "float(nu), bisected inside "
                             f"{FITNESS2D_DEFAULTS['bisection']['range']}",
            "nu_bisection_range": [float(v) for v in
                                   FITNESS2D_DEFAULTS["bisection"]["range"]],
            "nu_range_in_domain": bool(
                min(FITNESS2D_DEFAULTS["bisection"]["range"]) >= 0.0),
        },
        "phase1_axis_screen.py:120": {
            "kappa_expression": "0.0 (literal)",
            "nu_expression": "float(nu) from bisect_nu_crit, bracketed by the module's "
                             "own bisection range",
        },
        "note": ("the remaining non-literal sites are in test files "
                 "(test_solver_boussinesq.py, test_boussinesq_dedicated.py), which "
                 "produce no banked artifact; they are excluded from the contamination "
                 "verdict and counted separately"),
    }


def part4f_banked_coefficient_values():
    """Measure, over the whole banked record, whether any recorded nu/kappa is outside
    [0, inf).

    This is the arm that actually decides defect 2's contamination question, because it
    reads the values the banked runs RECORDED rather than the values the source could in
    principle produce. Any key named nu, kappa, nu_crit or nu0 anywhere in any banked
    JSON/JSONL is checked.
    """
    keys = ("nu", "kappa", "nu_crit", "nu0", "nu_c")
    blank = {"n": 0, "min": None, "max": None, "n_out_of_domain": 0,
             "out_of_domain_examples": []}
    found = {"scientific_measurement": {k: dict(blank, out_of_domain_examples=[])
                                        for k in keys},
             "audit_artifact": {k: dict(blank, out_of_domain_examples=[])
                                for k in keys}}
    n_files = 0

    def walk(node, path, rel, bucket):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in keys and isinstance(v, (int, float)) and not isinstance(v, bool):
                    e = found[bucket][k]
                    fv = float(v)
                    e["n"] += 1
                    e["min"] = fv if e["min"] is None else min(e["min"], fv)
                    e["max"] = fv if e["max"] is None else max(e["max"], fv)
                    if not (np.isfinite(fv) and fv >= 0.0):
                        e["n_out_of_domain"] += 1
                        if len(e["out_of_domain_examples"]) < 10:
                            e["out_of_domain_examples"].append(
                                {"file": rel, "path": f"{path}.{k}",
                                 "value": _jsonable(fv)})
                walk(v, f"{path}.{k}", rel, bucket)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]", rel, bucket)

    for root in (os.path.join(REPO, "writeup", "data"),
                 os.path.join(REPO, "experiments")):
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in ("__pycache__",)]
            for fn in filenames:
                if not fn.endswith((".json", ".jsonl")):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path, REPO)
                if rel == OWN_ARTIFACT_REL:
                    continue  # this leg's own output is not part of the banked record
                n_files += 1
                try:
                    with open(path, errors="replace") as fh:
                        text = fh.read()
                except OSError:
                    continue
                bucket, _ = _classify_artifact(rel, text)
                try:
                    if fn.endswith(".jsonl"):
                        for i, line in enumerate(text.splitlines()):
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                walk(json.loads(line), f"line{i}", rel, bucket)
                            except json.JSONDecodeError:
                                pass
                    else:
                        walk(json.loads(text), "$", rel, bucket)
                except (json.JSONDecodeError, ValueError):
                    continue

    def clean(bucket):
        return {k: {kk: (_jsonable(vv) if isinstance(vv, float) else vv)
                    for kk, vv in v.items()} for k, v in found[bucket].items()}

    sci_out = sum(v["n_out_of_domain"]
                  for v in found["scientific_measurement"].values())
    aud_out = sum(v["n_out_of_domain"] for v in found["audit_artifact"].values())
    return {
        "n_files_scanned": n_files, "keys_scanned": list(keys),
        "by_key_scientific_measurements": clean("scientific_measurement"),
        "by_key_audit_artifacts": clean("audit_artifact"),
        "n_recorded_coefficients_out_of_domain": sci_out,
        "n_out_of_domain_inside_audit_artifacts": aud_out,
        "scanner_positive_control": (
            f"the scanner reports {aud_out} out-of-domain coefficient(s) inside "
            "adversarial-battery artifacts, where a negative nu/kappa is the deliberately "
            "injected DATA rather than a contamination. So the zero reported for "
            "scientific artifacts is a measurement, not a scan that could only return "
            "zero (lesson 90)."),
    }


OWN_ARTIFACT_REL = os.path.join("writeup", "data", "p2_route_bob_v1_postrepair.json")

# A banked JSON is an ADVERSARIAL/AUDIT artifact -- a file whose entire subject is some
# module's defects, in which a deliberately malformed value or a deliberately provoked
# label is the DATA, not a contamination -- iff it declares one of these keys or its
# basename marks it as a bench-repair check. Declared before any scan output is read.
# `not_a_physics_measurement` is leg 91 (Route-FGA)'s own top-level declaration in
# writeup/data/p2_route_fga_v1_adversarial.json -- an adversarial artifact of
# solver/fractional_gclm.py that records a deliberately injected nu = -1e-3. It is
# honoured here rather than overridden: a file that declares it is not a measurement is
# not a banked measurement to contaminate.
_AUDIT_DECL_KEYS = ("module_under_audit", "module_repaired", "module_under_check",
                    "not_a_physics_measurement")


def _classify_artifact(rel, text):
    """('audit_artifact'|'scientific_measurement', declared-metadata dict)."""
    declared = {}
    obj = None
    if rel.endswith(".json"):
        try:
            obj = json.loads(text)
        except (json.JSONDecodeError, ValueError):
            obj = None
    if isinstance(obj, dict):
        for k in (*_AUDIT_DECL_KEYS, "leg", "route"):
            if k in obj:
                declared[k] = str(obj[k])[:120]
    is_audit = (bool(set(declared) & set(_AUDIT_DECL_KEYS))
                or os.path.basename(rel).startswith("bench_"))
    return ("audit_artifact" if is_audit else "scientific_measurement"), declared


def part4b_banked_blowup_labels():
    """Scan the banked record for any `blowup_candidate` -- defect 1's false label could
    only have contaminated a banked number by appearing in one -- and ATTRIBUTE every
    hit, since a hit produced by a different solver, or by leg 89's own audit of the
    defect, is not a contamination of anything."""
    hits = []
    scanned = []
    roots = [os.path.join(REPO, "writeup", "data"), os.path.join(REPO, "experiments"),
             os.path.join(REPO, "reports")]
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in ("__pycache__",)]
            for fn in filenames:
                if not fn.endswith((".json", ".jsonl")):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path, REPO)
                if rel == OWN_ARTIFACT_REL:
                    continue  # this leg's own output is not part of the banked record
                scanned.append(rel)
                try:
                    with open(path, errors="replace") as fh:
                        text = fh.read()
                except OSError:
                    continue
                if rel == OWN_ARTIFACT_REL or "blowup_candidate" not in text:
                    continue
                classification, declared = _classify_artifact(rel, text)
                # Attribute PER OCCURRENCE, not per file: leg 71's capabilities audit
                # contains a `blowup_candidate` from `check_solve_gclm_result_contract`
                # -- solve_gclm, a different solver -- inside a file that also mentions
                # Boussinesq elsewhere. A file-level "mentions boussinesq" test calls
                # that a hit; a +/-400-character context window does not.
                occ = []
                i = text.find("blowup_candidate")
                while i != -1:
                    ctx = text[max(0, i - 400):i + 400].lower()
                    occ.append({"boussinesq_in_context": "boussinesq" in ctx,
                                "gclm_in_context": "gclm" in ctx})
                    i = text.find("blowup_candidate", i + 1)
                n_bouss = sum(1 for o in occ if o["boussinesq_in_context"])
                hits.append({
                    "file": rel,
                    "n_occurrences": len(occ),
                    "n_occurrences_in_a_boussinesq_context": n_bouss,
                    "n_occurrences_in_a_gclm_context":
                        sum(1 for o in occ if o["gclm_in_context"]),
                    "classification": classification,
                    "declared": declared,
                    # A hit contaminates a banked NUMBER only if it is a scientific
                    # measurement AND the occurrence is in a Boussinesq context.
                    "n_attributable_to_a_banked_solve_boussinesq_measurement":
                        n_bouss if classification == "scientific_measurement" else 0,
                })
    n_attrib = sum(h["n_attributable_to_a_banked_solve_boussinesq_measurement"]
                   for h in hits)
    n_in_audit = sum(h["n_occurrences"] for h in hits
                     if h["classification"] == "audit_artifact")
    return {"n_files_scanned": len(scanned), "roots_scanned":
            [os.path.relpath(r, REPO) for r in roots],
            "n_files_with_a_blowup_candidate_string": len(hits),
            "n_occurrences_total": sum(h["n_occurrences"] for h in hits),
            "n_occurrences_inside_audit_artifacts": n_in_audit,
            "n_hits_attributable_to_a_banked_solve_boussinesq_measurement": n_attrib,
            "scanner_positive_control": (
                "the scanner is demonstrably able to report a non-zero count: it finds "
                "the deliberately-provoked blowup_candidate labels inside leg 89's own "
                "battery artifact and the bench-repair check. A scanner that could only "
                "ever return 0 would be lesson 90's forbidden control."),
            "hits": hits}


def part4c_zero_guard_false_refusal():
    """Would the NEW scale-aware zero guard REFUSE any initial condition the banked
    Phase-1 record actually used? A repair that rejects real data is a regression even
    when it fixes the defect it targeted.

    Recomputed here from ga.genome2d directly, at every banked resolution, using the
    module's own mask and its own ZERO_OMEGA_REL_TOL -- not read from the repair's JSON.
    """
    from ga.genome2d import realize_holder_density_2d, realize_holder_vorticity_2d
    from solver.boussinesq import ZERO_OMEGA_REL_TOL, dealias_mask2d, grid2d

    def represented(f, n):
        return np.fft.ifft2(np.fft.fft2(f) * dealias_mask2d(n)).real

    ics = {}
    worst = None
    for n in (128, 256, 512, 1024):
        for label in ("smooth_sharp", "smooth_mild", "rough_h0.5", "rough_h0.3"):
            if label.startswith("rough"):
                h = float(label.split("_h")[1])
                w0, th0 = (realize_holder_vorticity_2d(h, n),
                           realize_holder_density_2d(h, n))
            else:
                X, Y = grid2d(n)
                if label == "smooth_sharp":
                    w0 = 0.2 * np.sin(X) * np.sin(Y)
                    th0 = (1.0 + np.cos(2 * X)) * np.sin(2 * Y)
                else:
                    w0, th0 = np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)
            w = represented(w0, n)
            th = represented(th0, n)
            m0 = float(np.max(np.abs(w)))
            scale = max(m0, float(np.max(np.abs(w0))), float(np.max(np.abs(th))))
            ratio = m0 / scale
            rec = {"represented_m0": m0, "state_scale": scale,
                   "m0_over_state_scale": ratio,
                   "margin_over_tolerance": ratio / ZERO_OMEGA_REL_TOL,
                   "guard_would_fire": bool(m0 <= ZERO_OMEGA_REL_TOL * scale)}
            ics[f"{label}_n{n}"] = rec
            if worst is None or ratio < worst[1]:
                worst = (f"{label}_n{n}", ratio)
    return {
        "ZERO_OMEGA_REL_TOL": ZERO_OMEGA_REL_TOL,
        "n_ics_checked": len(ics),
        "n_ics_where_guard_would_fire": sum(1 for v in ics.values()
                                            if v["guard_would_fire"]),
        "worst_ic": worst[0],
        "worst_m0_over_state_scale": worst[1],
        "worst_margin_over_tolerance": worst[1] / ZERO_OMEGA_REL_TOL,
        "ics": ics,
    }


def part4d_phase1_reproduction():
    """Re-run the banked Phase-1 spike at N=128 and compare EVERY banked quantity.

    The repair's own audit compared two per IC (t_resolved, amp_resolved) plus the
    outcome. This compares five: t_resolved, amp_resolved, outcome, the fixed-window
    log-growth-rate fitness proxy `g`, and the (exponent, t_star) estimate -- i.e. the
    quantities the spike's own conclusion was drawn from.

    The solve is reconstructed here from phase1_resolution_spike.py's module constants
    and IC realizers; the banked values come from writeup/data/phase1_spike.json.
    """
    import phase1_resolution_spike as spike
    from solver.boussinesq import solve_boussinesq
    from win_condition import InsufficientDataError, estimate_blowup_time

    with open(PHASE1_SPIKE) as fh:
        banked = json.load(fh)

    n = 128
    ics = {}
    worst_rel = 0.0
    n_exact = 0
    for ic in spike.build_ics():
        label = ic["label"]
        w0, th0 = spike.realize_ic(ic, n)
        r = solve_boussinesq(w0, th0, nu=0.0, t_max=spike.T_MAX, buoyancy=True,
                             symmetry="houluo",
                             amplification_factor=spike.AMPLIFICATION,
                             tail_guard=spike.TAIL_GUARD, max_steps=spike.MAX_STEPS,
                             dt_max=spike.DT_MAX)
        times, mom = r.times.tolist(), r.max_omega.tolist()
        m0 = mom[0]
        t1, t2 = spike.GROWTH_WINDOW
        if times[-1] >= t2:
            a1, a2 = spike._interp(times, mom, t1), spike._interp(times, mom, t2)
            g = float((np.log(a2) - np.log(a1)) / (t2 - t1))
        else:
            g = float("nan")
        est = None
        try:
            e = estimate_blowup_time(times, mom, tail_fraction=0.5, fit_exponent=True)
            if e is not None:
                est = {"t_star": float(e.t_star), "exponent": float(e.exponent)}
        except InsufficientDataError:
            est = None

        b = banked["ics"][label]
        key = str(n)
        fields = {}

        def cmp(name, banked_val, mine):
            if banked_val is None and mine is None:
                fields[name] = {"banked": None, "repaired": None, "exact": True}
                return 0.0
            if banked_val is None or mine is None:
                fields[name] = {"banked": banked_val, "repaired": mine, "exact": False}
                return float("inf")
            if isinstance(banked_val, str) or isinstance(mine, str):
                ok = banked_val == mine
                fields[name] = {"banked": banked_val, "repaired": mine, "exact": ok}
                return 0.0 if ok else float("inf")
            bv, mv = float(banked_val), float(mine)
            if np.isnan(bv) and np.isnan(mv):
                fields[name] = {"banked": "nan", "repaired": "nan", "exact": True,
                                "abs_diff": 0.0}
                return 0.0
            d = abs(bv - mv)
            rel = d / abs(bv) if bv != 0.0 else d
            fields[name] = {"banked": _jsonable(bv), "repaired": _jsonable(mv),
                            "abs_diff": _jsonable(d), "rel_diff": _jsonable(rel),
                            "exact": d == 0.0}
            return rel

        rels = [
            cmp("t_resolved", b["t_resolved_by_N"][key], float(r.t_final)),
            cmp("amp_resolved", b["amp_resolved_by_N"][key], float(mom[-1] / m0)),
            cmp("outcome", b["outcome_by_N"][key], r.outcome),
            cmp("growth_rate_fixed_window", b["g_by_N"][key], g),
            cmp("exponent", b["exponent_by_N"][key],
                None if est is None else est["exponent"]),
            cmp("tstar", b["tstar_by_N"][key],
                None if est is None else est["t_star"]),
        ]
        exact = all(f.get("exact") for f in fields.values())
        n_exact += int(exact)
        worst_rel = max(worst_rel, max(x for x in rels if np.isfinite(x)) if rels else 0.0)
        ics[label] = {"fields": fields, "all_fields_exact": exact,
                      "n_fields_compared": len(fields)}

    return {
        "banked_artifact": "writeup/data/phase1_spike.json",
        "resolution": n,
        "n_ics": len(ics),
        "n_ics_reproducing_every_field_exactly": n_exact,
        "n_fields_compared_per_ic": 6,
        "worst_relative_difference": _jsonable(worst_rel),
        "ics": ics,
    }


def part4e_repair_selfreport_crosscheck():
    """Cross-check this leg's independent numbers against the repair's own JSON, and say
    plainly which of the two is the evidence. Any disagreement is the finding."""
    if not os.path.exists(BENCH_ARTIFACT):
        return {"available": False}
    with open(BENCH_ARTIFACT) as fh:
        b = json.load(fh)
    return {
        "available": True,
        "artifact": "writeup/data/bench_boussinesq_silent_corruption_check.json",
        "repair_claims": {
            "n_silent_gate_deciding": b["part_c_battery_rerun"]["n_silent_gate_deciding"],
            "n_silent_secondary": b["part_c_battery_rerun"]["n_silent_secondary"],
            "n_cases_where_conservation_drift_masks_a_nan_limb":
                b["part_c_battery_rerun"][
                    "n_cases_where_conservation_drift_masks_a_nan_limb"],
            "n_call_sites": b["part_b1_coefficient_domains"]["n_call_sites"],
            "n_call_sites_with_out_of_domain_kappa":
                b["part_b1_coefficient_domains"]["n_call_sites_with_out_of_domain_kappa"],
            "n_banked_blowup_hits_attributable_to_solve_boussinesq":
                b["part_b3_banked_blowup_labels"][
                    "hits_attributable_to_solve_boussinesq"],
            "n_phase1_n128_ics_exact": b["part_b4_banked_headline_reproduction"]["n_exact"],
            "phase1_worst_abs_diff":
                b["part_b4_banked_headline_reproduction"]["worst_abs_diff"],
            "n_wellformed_cases_bit_identical":
                b["part_a_zero_regression"]["n_bit_identical"],
        },
        "note": ("this block is the CLAIM under audit, not evidence for it. Leg 133's "
                 "numbers are computed independently above; agreement is a corroboration "
                 "and disagreement is this leg's finding."),
    }


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def _prerepair_worker(out_path):
    """Subprocess entry point: inject the pre-repair module, then measure."""
    load_prerepair_solver()
    cases = run_battery()
    payload = {"census": _census(cases), "probes": part3_defect_probes(),
               "zero_regression": part5_zero_regression_n32()}
    with open(out_path, "w") as fh:
        json.dump(payload, fh, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prerepair-out", default=None,
                    help="internal: run the pre-repair arm and dump JSON here")
    args = ap.parse_args()
    if args.prerepair_out:
        _prerepair_worker(args.prerepair_out)
        return

    t_start = time.perf_counter()
    prov = part0_provenance()

    # PART 2 first, in a fresh process: it must not contaminate this one's sys.modules.
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp.close()
    subprocess.check_call([sys.executable, os.path.abspath(__file__),
                           "--prerepair-out", tmp.name], cwd=REPO)
    with open(tmp.name) as fh:
        pre = json.load(fh)
    os.unlink(tmp.name)

    # PART 1 and 3: the repaired module, in this process.
    from solver.boussinesq import _guard_max  # noqa: F401  -- identifies the repaired src
    post_cases = run_battery()
    post = _census(post_cases)
    post_probes = part3_defect_probes()
    zr = compare_zero_regression(pre["zero_regression"], part5_zero_regression_n32())

    trans = verdict_transitions(pre["census"], post, post_cases)

    control = compare_to_leg89_artifact(pre["census"])

    a = part4a_call_sites()
    a2 = part4a2_resolve_nonliteral_sites()
    ff = part4f_banked_coefficient_values()
    bb = part4b_banked_blowup_labels()
    cc = part4c_zero_guard_false_refusal()
    dd = part4d_phase1_reproduction()
    ee = part4e_repair_selfreport_crosscheck()

    clause_a = (post["n_silent_gate_deciding"] == 0
                and post["n_silent_secondary"] == 0
                and post["n_cases_where_conservation_drift_masks_a_nan_limb"] == 0
                and trans["n_moved_quieter"] == 0)
    control_valid = (control["n_verdicts_disagreeing"] == 0
                     and pre["census"]["n_silent_gate_deciding"] == 19
                     and pre["census"]["n_silent_secondary"] == 4
                     and pre["census"][
                         "n_cases_where_conservation_drift_masks_a_nan_limb"] == 13)
    clause_b = (zr["n_differing"] == 0
                and dd["n_ics_reproducing_every_field_exactly"] == dd["n_ics"]
                and a["n_production_sites_with_out_of_domain_coefficient"] == 0
                and ff["n_recorded_coefficients_out_of_domain"] == 0
                and bb["n_hits_attributable_to_a_banked_solve_boussinesq_measurement"] == 0
                and cc["n_ics_where_guard_would_fire"] == 0)
    gate_answer = "YES" if (clause_a and clause_b and control_valid
                            and prov["instrument_byte_identical"]) else "NO"

    payload = {
        "leg": 133,
        "route": "BOB",
        "module_under_audit": "solver/boussinesq.py",
        "module_edited": False,
        "closes_the_loop_on": {"leg": 89, "route": "BOA",
                               "repair_commit": "0c54d8a", "merge_commit": "14b2e98"},
        "gate_verbatim": (
            "Post-repair, does solver/boussinesq.py (a) pass leg 89's full original "
            "battery -- no false blowup_candidate under dealiasing noise, kappa honored, "
            "NaNs propagated or flagged -- and (b) reproduce the banked n=32 Boussinesq "
            "results bit-identically, confirming the repair's no-contamination conclusion "
            "independently?"),
        "gate_answer": gate_answer,
        "clause_a_battery_passes": clause_a,
        "clause_b_banked_record_uncontaminated": clause_b,
        "control_is_valid": control_valid,
        "part0_provenance": prov,
        "part1_postrepair_battery": post,
        "part2_prerepair_control_battery": pre["census"],
        "part2_control_vs_leg89_banked_artifact": control,
        "part1b_verdict_transitions_prerepair_to_postrepair": trans,
        "part3_defect_probes_postrepair": post_probes,
        "part3_defect_probes_prerepair": pre["probes"],
        "part5_zero_regression_n32_prerepair_vs_postrepair": zr,
        "part4a_call_sites": a,
        "part4a2_nonliteral_site_resolution": a2,
        "part4f_banked_coefficient_values": ff,
        "part4b_banked_blowup_labels": bb,
        "part4c_zero_guard_false_refusal": cc,
        "part4d_phase1_reproduction": dd,
        "part4e_repair_selfreport_crosscheck": ee,
        "wall_seconds": time.perf_counter() - t_start,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)

    print(f"PART 0  instrument byte-identical to leg 89: "
          f"{prov['instrument_byte_identical']} "
          f"({prov['instrument_bytes_compared']} bytes)")
    print(f"PART 2  PRE-repair control: silent {pre['census']['n_silent_gate_deciding']}"
          f"/{pre['census']['n_silent_secondary']}, masked "
          f"{pre['census']['n_cases_where_conservation_drift_masks_a_nan_limb']} "
          f"(leg 89 banked 19/4/13); per-case agreement "
          f"{control['n_verdicts_agreeing']}/{control['n_labels_compared']}")
    print(f"PART 1  POST-repair: silent {post['n_silent_gate_deciding']}"
          f"/{post['n_silent_secondary']}, masked "
          f"{post['n_cases_where_conservation_drift_masks_a_nan_limb']}, of "
          f"{post['n_cases']} cases")
    for fname, f in post["families"].items():
        print(f"          {fname:32s} n={f['n_cases']:3d}  {f['verdicts']}")
    print(f"PART 1b transitions: {trans['n_moved_louder']} louder, "
          f"{trans['n_moved_quieter']} quieter, {trans['n_unchanged']} unchanged  "
          f"{trans['transition_matrix']}")
    print(f"PART 5  zero regression at n={N}: {zr['n_bit_identical']}/{zr['n_cases']} "
          f"well-formed cases bit-identical pre- vs post-repair "
          f"({zr['n_differing']} differing)")
    print(f"PART 4a call sites: {a['n_production_call_sites']} production, "
          f"{a['n_production_sites_with_out_of_domain_coefficient']} out-of-domain")
    print(f"PART 4f banked coefficient values scanned in {ff['n_files_scanned']} files: "
          f"{ff['n_recorded_coefficients_out_of_domain']} out of domain")
    print(f"PART 4b banked files scanned {bb['n_files_scanned']}, "
          f"blowup_candidate strings in {bb['n_files_with_a_blowup_candidate_string']}, "
          f"attributable to a banked solve_boussinesq measurement: "
          f"{bb['n_hits_attributable_to_a_banked_solve_boussinesq_measurement']}")
    print(f"PART 4c zero guard would fire on "
          f"{cc['n_ics_where_guard_would_fire']}/{cc['n_ics_checked']} Phase-1 ICs; "
          f"worst margin {cc['worst_margin_over_tolerance']:.3e}x")
    print(f"PART 4d phase1_spike N=128: "
          f"{dd['n_ics_reproducing_every_field_exactly']}/{dd['n_ics']} ICs exact on all "
          f"6 fields; worst rel diff {dd['worst_relative_difference']}")
    print(f"GATE ANSWER: {gate_answer}   wall {payload['wall_seconds']:.1f}s")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
