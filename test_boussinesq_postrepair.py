"""Leg 89's adversarial battery, BANKED AS A PERMANENT REGRESSION SUITE (leg 133,
Route-BOB).

Leg 133's gate answered YES on both clauses, and its yes-branch reads, verbatim:

  "Repair confirmed solid and non-regressive; the severest finding of the run is fully
   closed. Bank leg 89's battery as a permanent regression suite."

This file is that bank. It differs from `test_boussinesq_adversarial.py` -- which the
bench-repair wrote and which exercises **12 representative checks, one per defect** -- by
running **all 90 of leg 89's cases** on every invocation and pinning the whole verdict
census, not a sample.

WHAT EACH KIND OF CHECK IS FOR
------------------------------
1. `check_battery_*` -- the full 90-case census, and the per-case comparison against leg
   89's banked artifact along a LOUDNESS LADDER (silent < benign < propagated < flagged <
   raised). The census totals are not the real gate: what makes the repair non-regressive
   is that **no case ever moves DOWN that ladder**. A future change that turned one
   `raised` back into a `silent` would be caught by `n_moved_quieter`, even if the
   headline "0 silent" still held for a different reason.

2. `check_defect*` -- the four defects leg 89 found (plus the two detection-parameter
   families), each probed by code written from the defect DESCRIPTION rather than copied
   from leg 89's battery, so a regression in the battery and a regression in the module
   cannot mask each other. Each docstring carries the PRE-REPAIR magnitude, so this file
   can never later be read as though the defect never existed.

3. `check_zero_regression_*` -- 15 well-formed n=32 configurations pinned at the BIT
   level (sha256 of the float64 bit pattern of `omega_final`, `theta_final` and the
   `max_omega` trajectory, plus every scalar to full `repr` precision), against the table
   leg 133 measured and banked. These hashes were verified equal to the PRE-repair
   module's, so this pin is simultaneously a zero-regression guarantee and a
   don't-drift-later guarantee.

4. `check_banked_*` -- the banked Phase-1 record: the N=128 column of
   `writeup/data/phase1_spike.json` recomputed and compared on all six banked
   quantities.

5. `check_CONTROL_the_battery_can_still_report_silent` -- **the control that can come out
   differently** (lesson 90). It loads the PRE-REPAIR module source from git blob
   `2b787e4` in a subprocess and asserts the same harness reports leg 89's original
   **19 gate-deciding silent / 4 secondary / 13 masked**. Without it, every "0" above
   would be unfalsifiable: a harness that classified nothing would pass checks 1-4. This
   is the check to look at FIRST if this file ever starts failing.

Evidence: writeup/data/p2_route_bob_v1_postrepair.json (leg 133)
Instrument: experiments/p2_route_boa_v1_adversarial.py (leg 89, families only -- its
            `main()` is never called here, so its frozen artifact is never overwritten)
Pre-fix record: writeup/data/p2_route_boa_v1_adversarial.json (leg 89)
Repair: commit 0c54d8a, merged 14b2e98 (bench/fix-boussinesq-silent-corruption)

Run: .venv/bin/python test_boussinesq_postrepair.py
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import tempfile  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import experiments.p2_route_bob_v1_postrepair as bob  # noqa: E402

from solver.boussinesq import (  # noqa: E402
    ZERO_OMEGA_REL_TOL,
    dealias_mask2d,
    grid2d,
    solve_boussinesq,
)

ARTIFACT = os.path.join(HERE, "writeup", "data", "p2_route_bob_v1_postrepair.json")
LEG89_ARTIFACT = os.path.join(HERE, "writeup", "data",
                              "p2_route_boa_v1_adversarial.json")

N = 32
T_MAX = 0.3

# Leg 89's measurement of the pre-repair module, from its own banked artifact.
LEG89_SILENT_GATE_DECIDING = 19
LEG89_SILENT_SECONDARY = 4
LEG89_MASKED = 13
LEG89_N_CASES = 90

_BATTERY_CACHE = {}


def _fields():
    X, Y = grid2d(N)
    return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)


def _battery():
    """The 90 cases, run once per interpreter and reused across checks."""
    if "cases" not in _BATTERY_CACHE:
        _BATTERY_CACHE["cases"] = bob.run_battery()
    return _BATTERY_CACHE["cases"]


def _artifact():
    with open(ARTIFACT) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# 1. the full battery
# ---------------------------------------------------------------------------
def check_battery_all_90_cases_report_zero_silent():
    """Leg 89 measured 19 of 82 gate-deciding cases silently returning a plausible-looking
    wrong result, plus 4 of 8 secondary, with `conservation_drift` masking a NaN limb in
    13 of 90. All three must stay at zero."""
    census = bob._census(_battery())
    out = {"n_cases": census["n_cases"],
           "n_silent_gate_deciding": census["n_silent_gate_deciding"],
           "n_silent_secondary": census["n_silent_secondary"],
           "n_masked": census["n_cases_where_conservation_drift_masks_a_nan_limb"],
           "leg89_was": f"{LEG89_SILENT_GATE_DECIDING}/{LEG89_SILENT_SECONDARY}/"
                        f"{LEG89_MASKED}"}
    assert census["n_cases"] == LEG89_N_CASES, census["n_cases"]
    assert census["n_silent_gate_deciding"] == 0, census["families"]
    assert census["n_silent_secondary"] == 0, census["families"]
    assert census["n_cases_where_conservation_drift_masks_a_nan_limb"] == 0, out
    return out


def check_battery_family_census_matches_the_banked_one():
    """The per-family verdict breakdown, pinned. A change that kept the silent count at
    zero while moving cases between `raised`, `flagged` and `benign` would be a real
    behavioural change and must be looked at, not absorbed."""
    census = bob._census(_battery())
    banked = _artifact()["part1_postrepair_battery"]["families"]
    got = {k: v["verdicts"] for k, v in census["families"].items()}
    want = {k: v["verdicts"] for k, v in banked.items()}
    assert got == want, {"got": got, "want": want}
    return {"families": got}


def check_battery_no_case_is_quieter_than_leg89_measured():
    """THE non-regression gate, and the one that survives a change of headline.

    Compare all 90 verdicts to leg 89's banked artifact along the loudness ladder. Leg
    133 measured 40 cases moving louder (23 of them `silent -> raised`), 50 unchanged and
    **0 quieter**. Any quieter move is a repair regression.
    """
    with open(LEG89_ARTIFACT) as fh:
        leg89 = {c["label"]: c["verdict"] for c in json.load(fh)["cases"]}
    now = {c["label"]: c["verdict"] for c in _battery()}
    common = sorted(set(leg89) & set(now))
    quieter = [(lab, leg89[lab], now[lab]) for lab in common
               if bob._LOUDNESS[now[lab]] < bob._LOUDNESS[leg89[lab]]]
    louder = [lab for lab in common
              if bob._LOUDNESS[now[lab]] > bob._LOUDNESS[leg89[lab]]]
    silent_to_raised = [lab for lab in common
                        if leg89[lab] == "silent" and now[lab] == "raised"]
    out = {"n_compared": len(common), "n_quieter": len(quieter),
           "n_louder": len(louder), "n_silent_to_raised": len(silent_to_raised)}
    assert len(common) == LEG89_N_CASES, out
    assert not quieter, quieter
    assert len(silent_to_raised) == LEG89_SILENT_GATE_DECIDING + LEG89_SILENT_SECONDARY, out
    return out


# ---------------------------------------------------------------------------
# 2. the four defects, probed from their descriptions
# ---------------------------------------------------------------------------
def check_defect1_dealias_annihilated_vorticity_is_rejected():
    """PRE-REPAIR: sin(15x)sin(15y) at n=32 has a represented max|w| of 1.797e-16 after
    the 2/3 mask, and `amplification_factor * m0` was therefore a roundoff-scale threshold
    that ordinary O(1) buoyancy forcing cleared in one step -- returning
    `blowup_candidate`, the most consequential label the module emits, amplified
    5.566e13x off dealiasing noise. This was leg 89's headline finding."""
    X, Y = grid2d(N)
    _, th0 = _fields()
    w_kill = np.sin(15 * X) * np.sin(15 * Y)
    rep = float(np.max(np.abs(
        np.fft.ifft2(np.fft.fft2(w_kill) * dealias_mask2d(N)).real)))
    try:
        r = solve_boussinesq(w_kill, th0, t_max=T_MAX)
    except ValueError as exc:
        assert "numerically zero" in str(exc), str(exc)
        return {"represented_m0": rep, "rejected": True,
                "prefix_amplification_was": 55657830311010.46}
    raise AssertionError(
        f"accepted a dealias-annihilated vorticity (represented m0 = {rep:.3e}) "
        f"and returned outcome={r.outcome!r}")


def check_defect1_denormal_vorticity_is_rejected():
    """PRE-REPAIR: max|omega0| = 1e-300 passed the `== 0.0` guard and produced a
    `blowup_candidate` at an amplification of 1.000e+298."""
    w0, th0 = _fields()
    try:
        solve_boussinesq(1e-300 * w0, th0, t_max=T_MAX)
    except ValueError as exc:
        assert "numerically zero" in str(exc), str(exc)
        return {"rejected": True, "ZERO_OMEGA_REL_TOL": ZERO_OMEGA_REL_TOL,
                "prefix_amplification_was": 9.999999999479186e297}
    raise AssertionError("accepted a 1e-300 vorticity")


def check_defect2_out_of_domain_coefficients_are_rejected():
    """PRE-REPAIR: nu and kappa outside [0, inf) were applied behind `if nu > 0.0`, so the
    run that executed was the coefficient-free one BIT FOR BIT while `params` recorded the
    ignored value. kappa is the sharper case: the energy identity does not contain kappa,
    so no diagnostic in the result could ever have revealed it."""
    w0, th0 = _fields()
    rejected = {}
    for name, val in (("nu", -0.5), ("kappa", -0.5), ("nu", float("nan")),
                      ("kappa", float("nan")), ("nu", float("-inf")),
                      ("kappa", float("inf"))):
        try:
            solve_boussinesq(w0, th0, t_max=T_MAX, **{name: val})
        except ValueError as exc:
            rejected[f"{name}={val!r}"] = str(exc)[:60]
            continue
        raise AssertionError(f"accepted {name} = {val!r}")
    assert len(rejected) == 6, rejected
    return {"n_rejected": len(rejected)}


def check_defect3_a_nan_limb_reaches_conservation_drift():
    """PRE-REPAIR: a 100%-NaN theta with buoyancy off reported `conservation_drift =
    8.077e-18` -- Python's builtin `max` drops a NaN, so the poisoned energy limb hid
    behind the healthy mean-drift limb, and `drift_guard=1e-9` never fired.

    Post-repair the drift is NaN, and a non-finite drift is its OWN reportable failure."""
    w0, _ = _fields()
    r = solve_boussinesq(w0, np.full((N, N), np.nan), t_max=T_MAX,
                         buoyancy=False, drift_guard=1e-9)
    out = {"conservation_drift_is_nan": bool(not np.isfinite(r.conservation_drift)),
           "outcome": r.outcome, "early_exit_reason": r.early_exit_reason,
           "prefix_drift_was": 8.077335912845782e-18}
    assert not np.isfinite(r.conservation_drift), float(r.conservation_drift)
    assert r.outcome == "under_resolved", r.outcome
    assert r.early_exit_reason == "nonfinite_drift", r.early_exit_reason
    return out


def check_defect4_degenerate_grid_is_rejected():
    """PRE-REPAIR: at n = 1 and n = 2 the 2/3 mask retains exactly ONE mode -- the (0,0)
    mean -- so the discretization can represent no dynamics at all, yet the solver ran 30
    steps and reported `no_blowup` with `conservation_drift` exactly 0.0, i.e. the most
    reassuring guard number in the whole battery, precisely because nothing happened."""
    out = {}
    for n in (1, 2):
        Xn, Yn = grid2d(n)
        try:
            solve_boussinesq(np.sin(Xn) * np.sin(Yn) + 0.5,
                             np.cos(Xn) * np.sin(Yn) + 0.5, t_max=T_MAX)
        except ValueError as exc:
            out[f"n{n}"] = str(exc)[:50]
            continue
        raise AssertionError(f"accepted n = {n}")
    assert len(out) == 2, out
    out["retained_modes_n1"] = int(np.sum(dealias_mask2d(1)))
    out["retained_modes_n2"] = int(np.sum(dealias_mask2d(2)))
    return out


def check_defect5_nonfinite_detection_parameters_are_rejected():
    """PRE-REPAIR: a NaN CFL safety factor REMOVED its limb from the timestep `min`,
    relaxing dt_min by 168.8x; a NaN `amplification_factor` made the blow-up comparison
    permanently False, reporting `no_blowup` on a trajectory that reached 4.013x."""
    w0, th0 = _fields()
    rejected = {}
    for kw in (dict(c1=np.nan), dict(c2=np.nan), dict(c1=np.inf),
               dict(dt_max=0.0), dict(dt_max=-1e-3), dict(dt_max=np.nan),
               dict(amplification_factor=np.nan), dict(amplification_factor=-1.0),
               dict(drift_guard=np.nan), dict(tail_guard=np.nan),
               dict(t_max=-1.0)):
        base = dict(t_max=T_MAX)
        base.update(kw)
        try:
            solve_boussinesq(w0, th0, **base)
        except ValueError as exc:
            # key on name AND value: c1=nan and c1=inf are different cases
            rejected[", ".join(f"{k}={v!r}" for k, v in sorted(kw.items()))] = \
                str(exc)[:50]
            continue
        raise AssertionError(f"accepted {kw}")
    assert len(rejected) == 11, rejected
    return {"n_rejected": len(rejected),
            "prefix_dt_relaxation_was": 168.7817592345333,
            "prefix_missed_amplification_was": 4.01276241234652}


# ---------------------------------------------------------------------------
# 3. the controls that keep the repair gates falsifiable
# ---------------------------------------------------------------------------
def check_CONTROL_valid_input_is_still_accepted():
    """A module that refused EVERYTHING would pass every `check_defect*` above. These are
    the cases that must still be accepted, and whose answers must still be right:
    in-domain coefficients that genuinely change the run, the smallest grid that can carry
    a non-constant field, and the dull-but-correct constant-vorticity steady state."""
    w0, th0 = _fields()
    ctrl = solve_boussinesq(w0, th0, t_max=T_MAX)
    out = {}
    for name in ("nu", "kappa"):
        r = solve_boussinesq(w0, th0, t_max=T_MAX, **{name: 0.5})
        d = float(np.max(np.abs(r.omega_final - ctrl.omega_final)))
        out[f"{name}_0.5_max_abs_diff_from_neutral_run"] = d
        assert d > 0.0, f"in-domain {name} was dropped: the run is identical"
    X3, Y3 = grid2d(3)
    r3 = solve_boussinesq(np.sin(X3) * np.sin(Y3) + 0.5,
                          np.cos(X3) * np.sin(Y3) + 0.5, t_max=T_MAX)
    out["n3_outcome"] = r3.outcome
    out["n3_retained_modes"] = int(np.sum(dealias_mask2d(3)))
    assert out["n3_retained_modes"] > 1, out
    rc = solve_boussinesq(np.full((N, N), 2.0), th0, t_max=T_MAX)
    out["constant_vorticity_outcome"] = rc.outcome
    out["constant_vorticity_amplification"] = float(rc.max_omega[-1] / rc.max_omega[0])
    assert rc.outcome == "no_blowup", rc.outcome
    assert out["constant_vorticity_amplification"] < 2.0, out
    r0 = solve_boussinesq(w0, th0, t_max=0.0)
    out["t_max_zero_outcome"] = r0.outcome
    out["t_max_zero_n_timesteps"] = int(r0.n_timesteps)
    assert int(r0.n_timesteps) == 0, out
    return out


def check_CONTROL_the_battery_can_still_report_silent():
    """THE control that can come out differently (lesson 90).

    Everything above reports a zero. A harness that had quietly stopped classifying would
    report the same zeros. So: load the PRE-REPAIR module source (git blob 2b787e4) in a
    subprocess and run the identical 90 cases through the identical classifier. It must
    reproduce leg 89's original 19 / 4 / 13.

    If THIS check fails, none of the zeros above mean anything -- fix this one first.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp.close()
    try:
        subprocess.check_call(
            [sys.executable,
             os.path.join(HERE, "experiments", "p2_route_bob_v1_postrepair.py"),
             "--prerepair-out", tmp.name],
            cwd=HERE, stdout=subprocess.DEVNULL)
        with open(tmp.name) as fh:
            pre = json.load(fh)["census"]
    finally:
        os.unlink(tmp.name)
    out = {"prerepair_n_silent_gate_deciding": pre["n_silent_gate_deciding"],
           "prerepair_n_silent_secondary": pre["n_silent_secondary"],
           "prerepair_n_masked":
               pre["n_cases_where_conservation_drift_masks_a_nan_limb"],
           "prerepair_gate_answer": pre["leg89_gate_answer"]}
    assert pre["n_silent_gate_deciding"] == LEG89_SILENT_GATE_DECIDING, out
    assert pre["n_silent_secondary"] == LEG89_SILENT_SECONDARY, out
    assert pre["n_cases_where_conservation_drift_masks_a_nan_limb"] == LEG89_MASKED, out
    assert pre["leg89_gate_answer"] == "YES", out
    return out


# ---------------------------------------------------------------------------
# 4. bit-level and banked-record pins
# ---------------------------------------------------------------------------
def check_zero_regression_n32_hashes_are_unchanged():
    """15 well-formed n=32 configurations, pinned at the bit level against the table leg
    133 banked -- which was itself measured EQUAL to the pre-repair module's, so this pin
    is a zero-regression guarantee and a no-drift-later guarantee at once."""
    want = _artifact()[
        "part5_zero_regression_n32_prerepair_vs_postrepair"]["postrepair_hashes"]
    got = bob.part5_zero_regression_n32()
    differing = {}
    for label in sorted(set(want) | set(got)):
        if want.get(label) != got.get(label):
            differing[label] = sorted(
                k for k in want.get(label, {})
                if want[label][k] != got.get(label, {}).get(k))
    assert not differing, differing
    return {"n_cases": len(got), "n_bit_identical": len(got)}


def check_banked_phase1_n128_reproduces_on_all_six_fields():
    """The banked Phase-1 spike's N=128 column, recomputed and compared on all six banked
    quantities per IC (t_resolved, amp_resolved, outcome, the fixed-window log-growth-rate
    fitness proxy, and the exponent/t_star estimate). The bench-repair's own audit
    compared three."""
    res = bob.part4d_phase1_reproduction()
    out = {"n_ics": res["n_ics"],
           "n_exact": res["n_ics_reproducing_every_field_exactly"],
           "n_fields_per_ic": res["n_fields_compared_per_ic"],
           "worst_relative_difference": res["worst_relative_difference"]}
    assert res["n_ics_reproducing_every_field_exactly"] == res["n_ics"], res["ics"]
    return out



# ---------------------------------------------------------------------------
# leg 379's narrowing of check_banked_record_carries_no_out_of_domain_coefficient.
#
# `bob.part4f_banked_coefficient_values()` greps every banked JSON/JSONL for a key named
# nu/kappa/nu_crit/nu0/nu_c, ANYWHERE, regardless of whether that key was ever the
# `solve_boussinesq(nu=..., kappa=...)` coefficient defect 2 is about. Leg 185
# (Route-M2SD, `writeup/data/p2_route_m2sd_v1_diagnostic.json`, section "D5 -- genuine
# profile reachable?") and its continuation leg 284 (Route-NU12,
# `writeup/data/p2_route_nu12_v1_converge.json`) both bank a `nu` key that is NOT a
# Boussinesq viscosity: it is the recovered diffusion coefficient of a Newton
# continuation on `solver/dissipative_profile.py`'s STEADY profile equation (`M7`).
# Neither runner ever imports or calls `solve_boussinesq` -- confirmed by grep of both
# scripts for the symbol, zero hits -- so a negative value there cannot be defect 2's
# call-site contamination reaching a Boussinesq run; it is leg 185's own, explicitly
# self-flagged finding (its journal, section D5: "The negative rows DOWNGRADED TO
# SIGN-ONLY... only sign banked", reaffirmed and refined by leg 284/leg 210's grid
# ladder). `check_banked_record_carries_no_out_of_domain_coefficient` therefore excludes
# exactly these two banked files, by relative path, from the no-out-of-domain assertion,
# and only them -- everything else must still be clean.
_LEG185_LINEAGE_DIAGNOSTIC_FILES = (
    os.path.join("writeup", "data", "p2_route_m2sd_v1_diagnostic.json"),
    os.path.join("writeup", "data", "p2_route_nu12_v1_converge.json"),
)

_COEFFICIENT_KEYS = ("nu", "kappa", "nu_crit", "nu0", "nu_c")


def _scan_scientific_out_of_domain_coefficients(extra_roots=()):
    """Re-derive the full (file, path, key, value) list of out-of-domain
    nu/kappa/nu_crit/nu0/nu_c entries in files `bob._classify_artifact` buckets as
    `scientific_measurement`, across the same roots `bob.part4f_banked_coefficient_values`
    scans plus any `extra_roots` (used only by the planted-failure control below).

    This duplicates `bob`'s walk deliberately: `bob.part4f_banked_coefficient_values`
    caps its `out_of_domain_examples` at 10 per key, too few to name leg 185's ~295 rows
    individually and filter them out by file; this walker returns every hit.
    """
    hits = []
    roots = [os.path.join(HERE, "writeup", "data"), os.path.join(HERE, "experiments"),
             *extra_roots]

    def walk(node, path, rel):
        if isinstance(node, dict):
            for k, v in node.items():
                if (k in _COEFFICIENT_KEYS and isinstance(v, (int, float))
                        and not isinstance(v, bool)):
                    fv = float(v)
                    if not (np.isfinite(fv) and fv >= 0.0):
                        hits.append((rel, f"{path}.{k}", k, fv))
                walk(v, f"{path}.{k}", rel)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]", rel)

    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                if not fn.endswith((".json", ".jsonl")):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path, HERE)
                if rel == os.path.join("writeup", "data",
                                       "p2_route_bob_v1_postrepair.json"):
                    continue
                try:
                    with open(path, errors="replace") as fh:
                        text = fh.read()
                except OSError:
                    continue
                bucket, _ = bob._classify_artifact(rel, text)
                if bucket != "scientific_measurement":
                    continue
                try:
                    if fn.endswith(".jsonl"):
                        for i, line in enumerate(text.splitlines()):
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                walk(json.loads(line), f"line{i}", rel)
                            except json.JSONDecodeError:
                                pass
                    else:
                        walk(json.loads(text), "$", rel)
                except (json.JSONDecodeError, ValueError):
                    continue
    return hits


def check_banked_record_carries_no_out_of_domain_coefficient():
    """Defect 2 could only have contaminated a banked number through a call site that
    passed an out-of-domain coefficient to `solve_boussinesq`. Re-derived from the banked
    JSONs: every recorded nu/kappa/nu_crit/nu0/nu_c in a scientific artifact is in
    [0, inf), EXCEPT leg 185's (and leg 284's continuation of leg 185's) self-flagged
    `nu` diagnostic rows, which are not `solve_boussinesq` coefficients at all -- see the
    module comment above `_LEG185_LINEAGE_DIAGNOSTIC_FILES`.

    The scan's own positive control is that it DOES find the deliberately-injected
    negative coefficients inside the adversarial-battery artifacts."""
    res = bob.part4f_banked_coefficient_values()
    sites = bob.part4a_call_sites()

    all_hits = _scan_scientific_out_of_domain_coefficients()
    excused = [h for h in all_hits if h[0] in _LEG185_LINEAGE_DIAGNOSTIC_FILES]
    unexcused = [h for h in all_hits if h[0] not in _LEG185_LINEAGE_DIAGNOSTIC_FILES]

    out = {"n_files_scanned": res["n_files_scanned"],
           "n_out_of_domain_total": len(all_hits),
           "n_out_of_domain_excused_leg185_lineage": len(excused),
           "n_out_of_domain_unexcused": len(unexcused),
           "excused_files": sorted(set(h[0] for h in excused)),
           "n_out_of_domain_inside_audit_artifacts":
               res["n_out_of_domain_inside_audit_artifacts"],
           "n_production_call_sites": sites["n_production_call_sites"],
           "n_production_sites_out_of_domain":
               sites["n_production_sites_with_out_of_domain_coefficient"]}
    # Sanity: the excused set must be non-empty (leg 185's rows are really there) and
    # must be EXACTLY the two named files -- no third file has quietly started relying
    # on this exclusion.
    assert set(h[0] for h in excused) == set(_LEG185_LINEAGE_DIAGNOSTIC_FILES), out
    assert not unexcused, unexcused
    assert sites["n_production_sites_with_out_of_domain_coefficient"] == 0, sites[
        "out_of_domain_sites"]
    # The positive control: the scanner must be able to report a non-zero count.
    assert res["n_out_of_domain_inside_audit_artifacts"] > 0, (
        "the coefficient scanner found no out-of-domain value ANYWHERE, including in the "
        "adversarial artifacts that deliberately contain them -- the scanner is broken, "
        "and its zero for scientific artifacts is meaningless")
    return out


def check_CONTROL_narrowed_scan_still_catches_a_planted_out_of_domain_coefficient():
    """THE planted-failure control for the narrowing above (the 361 lesson): a check
    loosened without a demonstrated still-fails control is a blinded instrument.

    Plants a THIRD file, outside the two named exclusions, containing a synthetic
    out-of-domain `nu` inside a dict with no `_AUDIT_DECL_KEYS` (so `bob._classify_artifact`
    buckets it `scientific_measurement`, same as a real production artifact), in a
    scratch directory added to `_scan_scientific_out_of_domain_coefficients`'s roots.
    The narrowed scan must still report it as UNEXCUSED. If this check ever passes
    silently on a plant that should trip it, the narrowing above is too wide and must be
    tightened, not the other way around.
    """
    tmp_dir = tempfile.mkdtemp(prefix="leg379_planted_ood_")
    try:
        planted_rel_dir = os.path.join(tmp_dir, "writeup_data_stand_in")
        os.makedirs(planted_rel_dir, exist_ok=True)
        planted_path = os.path.join(planted_rel_dir, "p2_route_zzzz_v1_synthetic.json")
        with open(planted_path, "w") as fh:
            json.dump({"leg": "379-planted-control", "route": "ZZZZ",
                      "some_production_run": {"nu": -0.42, "kappa": 3.0}}, fh)
        hits = _scan_scientific_out_of_domain_coefficients(extra_roots=(tmp_dir,))
        planted_rel = os.path.relpath(planted_path, HERE)
        matches = [h for h in hits if h[0] == planted_rel]
        assert matches, (
            "planted control FAILED TO TRIP: a synthetic nu=-0.42 outside the two "
            "excused leg-185-lineage files was not detected by the narrowed scan -- "
            f"the narrowing is too wide. hits={hits}")
        assert planted_rel not in _LEG185_LINEAGE_DIAGNOSTIC_FILES
        return {"planted_file": planted_rel, "planted_hits": matches,
               "control": "TRIPPED as required"}
    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)


def check_zero_guard_refuses_no_banked_phase1_initial_condition():
    """The repair added a scale-aware zero guard. A guard that rejected real data would be
    a regression even though it fixes defect 1. Every Phase-1 IC at every banked
    resolution, recomputed from ga.genome2d: the least-resolved one still sits a factor
    1.000e+12 above the tolerance."""
    res = bob.part4c_zero_guard_false_refusal()
    out = {"n_ics_checked": res["n_ics_checked"],
           "n_would_fire": res["n_ics_where_guard_would_fire"],
           "worst_ic": res["worst_ic"],
           "worst_margin_over_tolerance": res["worst_margin_over_tolerance"]}
    assert res["n_ics_where_guard_would_fire"] == 0, res["ics"]
    assert res["worst_margin_over_tolerance"] > 1e6, out
    return out


CHECKS = [
    check_battery_all_90_cases_report_zero_silent,
    check_battery_family_census_matches_the_banked_one,
    check_battery_no_case_is_quieter_than_leg89_measured,
    check_defect1_dealias_annihilated_vorticity_is_rejected,
    check_defect1_denormal_vorticity_is_rejected,
    check_defect2_out_of_domain_coefficients_are_rejected,
    check_defect3_a_nan_limb_reaches_conservation_drift,
    check_defect4_degenerate_grid_is_rejected,
    check_defect5_nonfinite_detection_parameters_are_rejected,
    check_CONTROL_valid_input_is_still_accepted,
    check_CONTROL_the_battery_can_still_report_silent,
    check_zero_regression_n32_hashes_are_unchanged,
    check_banked_phase1_n128_reproduces_on_all_six_fields,
    check_banked_record_carries_no_out_of_domain_coefficient,
    check_CONTROL_narrowed_scan_still_catches_a_planted_out_of_domain_coefficient,
    check_zero_guard_refuses_no_banked_phase1_initial_condition,
]


def test_battery_all_90_cases_report_zero_silent():
    check_battery_all_90_cases_report_zero_silent()


def test_battery_family_census_matches_the_banked_one():
    check_battery_family_census_matches_the_banked_one()


def test_battery_no_case_is_quieter_than_leg89_measured():
    check_battery_no_case_is_quieter_than_leg89_measured()


def test_defect1_dealias_annihilated_vorticity_is_rejected():
    check_defect1_dealias_annihilated_vorticity_is_rejected()


def test_defect1_denormal_vorticity_is_rejected():
    check_defect1_denormal_vorticity_is_rejected()


def test_defect2_out_of_domain_coefficients_are_rejected():
    check_defect2_out_of_domain_coefficients_are_rejected()


def test_defect3_a_nan_limb_reaches_conservation_drift():
    check_defect3_a_nan_limb_reaches_conservation_drift()


def test_defect4_degenerate_grid_is_rejected():
    check_defect4_degenerate_grid_is_rejected()


def test_defect5_nonfinite_detection_parameters_are_rejected():
    check_defect5_nonfinite_detection_parameters_are_rejected()


def test_CONTROL_valid_input_is_still_accepted():
    check_CONTROL_valid_input_is_still_accepted()


def test_CONTROL_the_battery_can_still_report_silent():
    check_CONTROL_the_battery_can_still_report_silent()


def test_zero_regression_n32_hashes_are_unchanged():
    check_zero_regression_n32_hashes_are_unchanged()


def test_banked_phase1_n128_reproduces_on_all_six_fields():
    check_banked_phase1_n128_reproduces_on_all_six_fields()


def test_banked_record_carries_no_out_of_domain_coefficient():
    check_banked_record_carries_no_out_of_domain_coefficient()


def test_CONTROL_narrowed_scan_still_catches_a_planted_out_of_domain_coefficient():
    check_CONTROL_narrowed_scan_still_catches_a_planted_out_of_domain_coefficient()


def test_zero_guard_refuses_no_banked_phase1_initial_condition():
    check_zero_guard_refuses_no_banked_phase1_initial_condition()


if __name__ == "__main__":
    import warnings

    warnings.simplefilter("ignore")  # the poisoned cases warn by design
    failures = 0
    for chk in CHECKS:
        try:
            res = chk()
        except AssertionError as exc:
            failures += 1
            print(f"FAIL {chk.__name__}: {exc}")
            continue
        print(f"ok   {chk.__name__}")
        for k, v in (res or {}).items():
            print(f"       {k} = {v}")
    print()
    if failures:
        print(f"test_boussinesq_postrepair: {failures} FAILED")
        sys.exit(1)
    print(f"test_boussinesq_postrepair: all {len(CHECKS)} checks passed")
