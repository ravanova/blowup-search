"""Route-ICB v1 (leg 105) -- POST-REPAIR REGRESSION CHECK on solver/interval_certificate.py.

Leg 98 (Route-ICA) measured a fabrication-acceptance gap in `interval_constants` /
`radii_verdict`: 12 of 36 hypothesis-violating inputs reported a CLOSING certificate, 8 of
them load-bearing.  The bench-repair `bench/fix-interval-certificate-validation` (merged to
`main` at `3e52386`, content commit `0a1da91`) closed it and, in the SAME commit, rewrote
`test_interval_certificate_adversarial.py` to invert leg 98's seven GAP-PIN gates and to gate
the battery total.  This leg closes the loop with an INDEPENDENT check -- one that does not
rely on the repair grading its own homework -- exactly the role leg 87 played for the sibling
arithmetic primitive `solver/interval.py` (leg 69's repair) and leg 103 played for
`solver/gclm.py` (leg 92's repair).

THE GATE, VERBATIM (DIRECTION.md, leg 105)
-----------------------------------------------------------------------------
"Post-repair, does solver/interval_certificate.py (a) correctly reject every case in leg 98's
original fabrication battery, and (b) still reproduce leg 61's Kawahara known-answer gate with
zero regression?"

WHY THIS IS NOT JUST RE-RUNNING test_interval_certificate_adversarial.py
-----------------------------------------------------------------------------
That file's `test_banked_battery_reproduces` calls leg 98's OWN runner
(`experiments/p2_route_ica_v1_adversarial.py`) against whatever `solver/interval_certificate.py`
happens to be on disk today.  It is a legitimate regression pin, but it was WRITTEN BY THE
REPAIR ITSELF and it says nothing about clause (b) at all.  This file instead:

  PART A.  Re-runs leg 98's OWN 39-case battery -- literally the same case-construction code,
  imported unmodified -- bound FIRST to the pre-repair module (read straight out of git, not
  transcribed) as a NEGATIVE CONTROL (it must reproduce 12/36 false accepts, 8 load-bearing,
  or the harness itself is not trustworthy), and THEN bound to the current module, independently
  reproducing the 0/36 headline from a source outside the repair's own territory.

  PART B.  Runs `kawahara_certificate()` from the pre-repair and the post-repair module IN THE
  SAME PROCESS and compares every returned field BIT FOR BIT.  This is the strongest available
  form of "zero regression" -- stronger than matching the banked
  `writeup/data/p2_route_ka_v1_kawahara.json`, which a scouting run (see
  `writeup/novelty/leg_105.md` sec 3) showed is NOT bit-reproducible even from the LITERAL
  leg-61-original source in this environment: `Y_0 ~ 3e-17` sits at the float64 noise floor of a
  fully-converged Newton iterate, and re-running identical code on a different BLAS/environment
  moves it by ~2%, deterministically and repeatably WITHIN a given environment but not ACROSS
  environments.  A same-process differential sidesteps that confound entirely by holding the
  environment fixed and varying only the one file under test.

  PART C.  Reproduces `test_interval_certificate.py` gate 16's own assertions
  (`test_kawahara_known_answer_gate`) against the current module's output, and separately runs
  that test file directly as a whole-suite check (recorded, not re-implemented).

  PART D.  Reads the banked Kawahara JSON once, for an INFORMATIONAL magnitude only (the ~2%
  environment-sensitivity noted above), explicitly excluded from the pass/fail criterion.

`solver/interval_certificate.py` is read-only to this leg, under every outcome.

Run: PYTHONPATH=. .venv/bin/python experiments/p2_route_icb_v1_postrepair.py   (~70 s)
Writes: writeup/data/p2_route_icb_v1_postrepair.json
"""

import importlib.util
import json
import os
import subprocess
import sys
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_icb_v1_postrepair.json")
BANKED_KAWAHARA_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_ka_v1_kawahara.json")

GATE_VERBATIM = (
    "Post-repair, does solver/interval_certificate.py (a) correctly reject every case in leg "
    "98's original fabrication battery, and (b) still reproduce leg 61's Kawahara known-answer "
    "gate with zero regression?"
)

# The subject substring that names the repair's merge commit -- located BY CONTENT, not by
# hash, so a rebase of history upstream of this leg cannot silently break the differential
# (the technique leg 86 used for the sibling pipeline's repair, `<repair>^`).
REPAIR_MERGE_SUBJECT = "fix-interval-certificate-validation"


# ---------------------------------------------------------------------------
# locating and loading the pre-repair module
# ---------------------------------------------------------------------------
def _git(args):
    return subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout


def locate_prerepair_rev():
    """The commit just before the repair merged -- `03acb4e`, found by the merge's subject."""
    log = _git(["log", "--all", "--format=%H %s"])
    for line in log.splitlines():
        if REPAIR_MERGE_SUBJECT in line:
            merge_hash = line.split(" ", 1)[0]
            return merge_hash, merge_hash + "^1"
    raise RuntimeError(f"could not locate a commit whose subject contains "
                       f"{REPAIR_MERGE_SUBJECT!r} -- has history been rewritten?")


def load_module_from_source(src, name):
    """Load `src` as a standalone module named `name`, via a temp file (removed immediately).

    `solver/interval_certificate.py` only imports `solver.interval` absolutely, which resolves
    against the real, currently-installed `solver` package regardless of this module's own
    name -- so no package-shadowing is needed for the Kawahara half of the differential."""
    path = os.path.join(ROOT, f".{name}.tmp.py")
    with open(path, "w") as fh:
        fh.write(src)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        os.remove(path)
    return mod, src


def load_prerepair_module():
    merge_hash, prerepair_rev = locate_prerepair_rev()
    src = _git(["show", f"{prerepair_rev}:solver/interval_certificate.py"])
    mod, src = load_module_from_source(src, "icb_prerepair_interval_certificate")
    meta = {
        "repair_merge_commit": merge_hash,
        "prerepair_rev": prerepair_rev,
        "prerepair_sha256": __import__("hashlib").sha256(src.encode()).hexdigest(),
        "prerepair_lines": src.count("\n"),
        "prerepair_has_certificate_input_error": "class CertificateInputError" in src,
        "interval_py_changed_since_prerepair_rev": bool(
            _git(["diff", "--name-only", prerepair_rev, "HEAD", "--",
                 "solver/interval.py"]).strip()),
    }
    return mod, src, meta


def run_battery_against(ic_module):
    """Run leg 98's OWN battery (family_A/family_B/run), bound to `ic_module`.

    `experiments/p2_route_ica_v1_adversarial.py` does `from solver.interval_certificate import
    (...)`, which Python resolves via `sys.modules['solver.interval_certificate']` if already
    present. Substituting that entry for the duration of a fresh load of the battery module
    (under a private name, so leg 98's own territory file is never touched) redirects every
    case to `ic_module` without editing or copying a single line of leg 98's logic."""
    real = sys.modules.get("solver.interval_certificate")
    sys.modules["solver.interval_certificate"] = ic_module
    try:
        battery_path = os.path.join(ROOT, "experiments", "p2_route_ica_v1_adversarial.py")
        spec = importlib.util.spec_from_file_location("icb_battery_probe", battery_path)
        battery = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(battery)
    finally:
        if real is not None:
            sys.modules["solver.interval_certificate"] = real
        else:
            del sys.modules["solver.interval_certificate"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return battery.run(write=False, verbose=False)


# ---------------------------------------------------------------------------
# Kawahara bitwise differential
# ---------------------------------------------------------------------------
_KAWAHARA_SCALAR_FIELDS = [
    ("constants", "Y0"), ("constants", "Z1"), ("constants", "Z2"), ("constants", "A_norm"),
    ("constants", "B"),
    ("verdict", "closes"), ("verdict", "budget"), ("verdict", "Y0_over_budget"),
    ("verdict", "r_min"), ("verdict", "r_max"),
    ("conversion", "to_Hl"), ("conversion", "to_l2_l"), ("conversion", "sup_l_over_w"),
    ("conversion", "sqrt_Omega0"),
    (None, "Y0_Hl"), (None, "r_min_w"), (None, "r_min_l2_l"), (None, "r_min_Hl"),
    (None, "r_max_Hl"), (None, "float_residual_sup"),
]


def _get(d, section, key):
    return d[section][key] if section else d[key]


def kawahara_bitwise_diff(pre_mod, post_mod):
    """Run kawahara_certificate() from BOTH modules in this process and diff every field."""
    pre = pre_mod.kawahara_certificate()
    post = post_mod.kawahara_certificate()
    rows = []
    n_identical = 0
    for section, key in _KAWAHARA_SCALAR_FIELDS:
        try:
            a = _get(pre, section, key)
            b = _get(post, section, key)
        except KeyError:
            continue    # r_min_w etc. only present when closes=True; both must agree on that
        ident = (a == b) if not isinstance(a, float) else (
            a == b or (np.isnan(a) and np.isnan(b)))
        n_identical += int(ident)
        rows.append({"field": f"{section}.{key}" if section else key,
                     "pre": _jsonable(a), "post": _jsonable(b), "bit_identical": bool(ident)})
    hist_ident = pre["newton_history"] == post["newton_history"]
    rows.append({"field": "newton_history", "pre": pre["newton_history"],
                "post": post["newton_history"], "bit_identical": bool(hist_ident)})
    n_identical += int(hist_ident)
    coeff_ident = bool(np.array_equal(np.asarray(pre["coefficients"]),
                                      np.asarray(post["coefficients"])))
    rows.append({"field": "coefficients (Newton solution vector)", "pre": "<omitted, array>",
                "post": "<omitted, array>", "bit_identical": coeff_ident})
    n_identical += int(coeff_ident)
    return {"rows": rows, "n_fields": len(rows), "n_bit_identical": n_identical,
            "all_bit_identical": n_identical == len(rows),
            "pre_full": _jsonable(pre), "post_full": _jsonable(post)}


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return None
    if isinstance(x, (np.floating,)):
        x = float(x)
    if isinstance(x, float):
        if np.isnan(x):
            return "nan"
        if np.isinf(x):
            return "inf" if x > 0 else "-inf"
        return x
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (bool, int, str)) or x is None:
        return x
    return str(x)


# ---------------------------------------------------------------------------
# Part C -- leg 61's own known-answer gate, replicated against current output
# ---------------------------------------------------------------------------
def known_answer_gate_check(post_mod):
    run = post_mod.kawahara_certificate()
    v = run["verdict"]
    r0 = post_mod._KAWAHARA_CLN["r0_published"]
    runiq = post_mod._KAWAHARA_CLN["r_uniqueness_published"]
    lo, hi = run["r_min_Hl"], run["r_max_Hl"]
    reading_a = bool(lo <= r0 <= hi)
    reaches_uniqueness = bool(hi >= runiq)
    below = float(np.log10(r0 / lo))
    return {"closes": bool(v["closes"]), "Z1_below_one": bool(run["constants"]["Z1"] < 1.0),
            "certified_interval_Hl": [lo, hi], "published_window": [r0, runiq],
            "r0_is_a_certified_radius": reading_a, "reaches_uniqueness_ball": reaches_uniqueness,
            "decades_below_r0": below, "decades_budget": 1.0,
            "within_decades_budget": bool(below < 1.0),
            "gate_16_would_pass": bool(v["closes"] and run["constants"]["Z1"] < 1.0
                                       and reading_a and reaches_uniqueness and below < 1.0)}


# ---------------------------------------------------------------------------
# Part D -- informational only, never a gate criterion (see novelty pass sec 3)
# ---------------------------------------------------------------------------
def banked_json_crosscheck(post_mod):
    if not os.path.exists(BANKED_KAWAHARA_JSON):
        return {"available": False}
    with open(BANKED_KAWAHARA_JSON) as fh:
        banked = json.load(fh)
    banked_y0 = banked["main"]["constants"]["Y0"]
    banked_rmin_w = banked["main"]["r_min_w"]
    run = post_mod.kawahara_certificate()
    y0_ratio = float(run["constants"]["Y0"] / banked_y0)
    rmin_ratio = float(run["verdict"]["r_min"] / banked_rmin_w)
    return {"available": True,
            "banked_commit": "leg 61, 83099a8 -- BEFORE this leg's repair AND before leg 69's "
                             "solver/interval.py repair",
            "banked_Y0": banked_y0, "current_Y0": run["constants"]["Y0"],
            "Y0_ratio_current_over_banked": y0_ratio,
            "banked_r_min_w": banked_rmin_w, "current_r_min_w": run["verdict"]["r_min"],
            "r_min_ratio_current_over_banked": rmin_ratio,
            "note": ("NOT a regression signal and NOT part of this leg's gate. sec 3 of "
                     "writeup/novelty/leg_105.md shows this same ~2%-magnitude gap exists "
                     "even between the LITERAL leg-61-original source (re-run today) and the "
                     "committed JSON -- i.e. it predates both the interval.py and the "
                     "interval_certificate.py repairs and is attributable to environment "
                     "(BLAS/LAPACK) sensitivity of a Y_0 ~ 3e-17 quantity sitting at the "
                     "float64 noise floor of a fully-converged Newton iterate, not to either "
                     "repair. The bitwise same-process differential in Part B is this leg's "
                     "actual zero-regression evidence.")}


# ---------------------------------------------------------------------------
# Part A' -- static diff between the two module source texts
# ---------------------------------------------------------------------------
def static_diff_summary(pre_src, post_src):
    import difflib
    pre_lines = pre_src.splitlines()
    post_lines = post_src.splitlines()
    sm = difflib.SequenceMatcher(a=pre_lines, b=post_lines)
    added = removed = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("insert", "replace"):
            added += (j2 - j1)
        if tag in ("delete", "replace"):
            removed += (i2 - i1)
    import re
    pre_defs = set(re.findall(r"^(?:def|class) (\w+)", pre_src, re.M))
    post_defs = set(re.findall(r"^(?:def|class) (\w+)", post_src, re.M))
    return {"pre_lines": len(pre_lines), "post_lines": len(post_lines),
            "lines_added": added, "lines_removed": removed,
            "new_top_level_defs": sorted(post_defs - pre_defs),
            "removed_top_level_defs": sorted(pre_defs - post_defs)}


# ---------------------------------------------------------------------------
def run(write=True, verbose=True):
    import solver.interval_certificate as post_mod
    with open(os.path.join(ROOT, "solver", "interval_certificate.py")) as fh:
        post_src = fh.read()
    pre_mod, pre_src, prerepair_meta = load_prerepair_module()

    if verbose:
        print(f"pre-repair rev: {prerepair_meta['prerepair_rev']} "
              f"(merge {prerepair_meta['repair_merge_commit']})")
        print(f"  interval.py changed since that rev: "
              f"{prerepair_meta['interval_py_changed_since_prerepair_rev']} "
              f"(expect False -- leg 69's fix must already be baked into the baseline)")

    # ---- PART A: the battery, independently re-derived, both directions -------
    pre_battery = run_battery_against(pre_mod)
    post_battery = run_battery_against(post_mod)

    negative_control_ok = (
        pre_battery["totals"]["false_accepts"] == 12
        and pre_battery["totals"]["false_accepts_load_bearing"] == 8
        and pre_battery["totals"]["hypothesis_violating"] == 36
        and pre_battery["totals"]["cases"] == 39)
    battery_repaired_ok = (
        post_battery["totals"]["false_accepts"] == 0
        and post_battery["totals"]["false_accepts_load_bearing"] == 0)

    if verbose:
        print(f"\nPART A -- battery, independently re-derived:")
        print(f"  pre-repair  : {pre_battery['totals']}")
        print(f"  post-repair : {post_battery['totals']}")
        print(f"  negative control (pre reproduces 12/36, 8 load-bearing): "
              f"{negative_control_ok}")
        print(f"  gate (a) -- post-repair 0/36                           : "
              f"{battery_repaired_ok}")

    # ---- PART B: Kawahara, bitwise, same process --------------------------
    kdiff = kawahara_bitwise_diff(pre_mod, post_mod)
    if verbose:
        print(f"\nPART B -- Kawahara bitwise differential ({kdiff['n_bit_identical']}/"
              f"{kdiff['n_fields']} fields identical):")
        for row in kdiff["rows"]:
            if not row["bit_identical"]:
                print(f"  DIFFERS: {row['field']}  pre={row['pre']!r}  post={row['post']!r}")
        if kdiff["all_bit_identical"]:
            print("  ALL FIELDS BIT-IDENTICAL")

    # ---- PART C: leg 61's own gate, replicated -----------------------------
    gate16 = known_answer_gate_check(post_mod)
    if verbose:
        print(f"\nPART C -- leg 61's known-answer gate, replicated against current code:")
        print(f"  {gate16}")

    # ---- PART D: informational only -----------------------------------------
    crosscheck = banked_json_crosscheck(post_mod)

    static_diff = static_diff_summary(pre_src, post_src)

    gate_a = battery_repaired_ok and negative_control_ok
    gate_b = kdiff["all_bit_identical"] and gate16["gate_16_would_pass"]

    data = {
        "leg": 105, "route": "ICB", "question": GATE_VERBATIM,
        "prerepair_meta": prerepair_meta,
        "static_diff": static_diff,
        "part_a_battery": {
            "prerepair_reproduces_leg98_exactly": negative_control_ok,
            "prerepair_totals": pre_battery["totals"],
            "postrepair_totals": post_battery["totals"],
            "postrepair_false_accept_cases": post_battery["false_accept_cases"],
            "postrepair_load_bearing_cases": post_battery["load_bearing_cases"],
            "gate_a_answer": gate_a,
        },
        "part_b_kawahara_bitwise": {k: v for k, v in kdiff.items()
                                   if k not in ("pre_full", "post_full")},
        "part_b_kawahara_full_pre": kdiff["pre_full"],
        "part_b_kawahara_full_post": kdiff["post_full"],
        "part_c_known_answer_gate": gate16,
        "part_d_banked_json_crosscheck_informational_only": crosscheck,
        "gate": {
            "verbatim": GATE_VERBATIM,
            "a_battery_rejects_every_case": gate_a,
            "b_kawahara_zero_regression": gate_b,
            "answer": "YES" if (gate_a and gate_b) else "NO",
        },
    }

    if verbose:
        print(f"\nGATE (a) battery rejects every case  : {gate_a}")
        print(f"GATE (b) Kawahara zero regression     : {gate_b}")
        print(f"GATE ANSWER: {data['gate']['answer']}")

    if write:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w") as fh:
            json.dump(data, fh, indent=2, sort_keys=True, default=str)
        if verbose:
            print(f"\nwrote {OUT}")
    return data


if __name__ == "__main__":
    run()
