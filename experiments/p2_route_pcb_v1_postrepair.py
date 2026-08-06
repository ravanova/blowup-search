"""Route-PCB v1 -- the POST-REPAIR REGRESSION CHECK of the line-sweep preconditioner.

THE GATE, verbatim from DIRECTION.md leg 86:

    After the bench-repair, does solver/port_certification.py's line-sweep preconditioner
    still (a) hit the 9.5e-16 precision gate it was originally validated to, and (b) run
    within normal benchmark variance of its pre-repair timing?

WHY THE QUESTION IS NOT IDLE.  Leg 79's repair (commit 3f187d8) added `_hypothesis_violations`
and an INVALID_INPUT branch to `radii_polynomial_status` -- 11 of 25 hypothesis-violating inputs
came back `closes=True` before, 0 of 25 after.  It landed inside a module whose OTHER claim, the
one `capabilities.py` advertises, is that `line_sweep_solve` inverts the full transport operator
to 9.5e-16 in O(N).  New branches in a module with a hot path are a classic place for a precision
or performance regression to hide, and nothing has re-checked that claim since the repair.

HOW THIS IS MEASURED, and the two pre-commitments made in writeup/novelty/leg_86.md BEFORE any
number was seen:

  (1) DIFFERENTIAL, NOT ABSOLUTE.  The pre-repair module is recovered from git (`3f187d8^`) into
      a scratch directory and imported side by side with the working-tree module, under distinct
      module names.  Every clause runs both.  A one-sided "it still passes" cannot distinguish
      "unchanged" from "changed but still inside a loose tolerance", and the repository's own
      existing gate (test_port_certification.py test_7) is exactly that loose: it asserts
      err < 1e-11 against a 9.5e-16 claim, ~4 decades of slack.

  (2) THE PRECISION ARM IS BIT-FOR-BIT.  Agreement is asserted on the IEEE-754 bit patterns of
      the returned arrays, not on "both are small".  A guard that perturbed the last bits without
      breaking a 1e-11 assertion is precisely the failure mode being hunted.

  (3) THE TIMING ARM CARRIES A NULL.  "Within normal benchmark variance" is unanswerable unless
      the variance is measured in the same run, on the same machine, under the same load.  So the
      bench interleaves THREE arms per round -- pre, post, and post again (the null) -- and the
      real pre/post ratio is judged against the null arm's own post/post spread.  A bare speed
      ratio would be the "timing anecdote" test_route_g_perf.py names and refuses.

  (4) STATIC ARM.  The repair's diff is read back out of git and the set of top-level definitions
      it touches is compared against the sweep's call path, so the numerical result is
      corroborated by the text of the change rather than resting on it.

Clauses:
  P1  static      -- which top-level defs commit 3f187d8 touched; is any on the sweep's path?
  P2  precision   -- the exactness battery (operator applied to its own sweep), pre vs post,
                     bit-for-bit, over 24 configurations including test_7's exact one
  P3  timing      -- interleaved pre / post / post-null rounds, median ns per call
  P4  consequence -- the Route-L preconditioned Krylov ladder recomputed pre vs post

Run:  python experiments/p2_route_pcb_v1_postrepair.py            (~1-2 min, no scipy)
      python experiments/p2_route_pcb_v1_postrepair.py --quick    (fewer timing rounds)

Writes writeup/data/p2_route_pcb_v1_postrepair.json.  Reports MAGNITUDES, never booleans:
every clause emits the number it measured next to the number it was judged against.
"""

import argparse
import importlib.util
import json
import re
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.boussinesq_velocity import _thomas          # noqa: E402

# The commit that carried leg 79's bench-repair.  Resolved by message, not by hash, so the
# script keeps working after a rebase renumbers it.
REPAIR_SUBJECT = "validate the radii polynomial's constants"
MODULE_PATH = "solver/port_certification.py"

# The claim under audit, from capabilities.py: "line sweep gated to 9.5e-16 against the
# operator it inverts".  Pre-committed as the number the precision arm is judged against.
CLAIMED_PRECISION = 9.5e-16

# test_port_certification.py test_7's exact configuration -- the run that produced 9.5e-16.
CANONICAL = {"seed": 11, "n_r": 48, "n_b": 16, "drho": 0.09, "dbeta": 0.033, "c": -1.0145}


# --------------------------------------------------------------------------
# recovering the pre-repair module
# --------------------------------------------------------------------------
def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, check=True).stdout


def find_repair_commit():
    """Locate leg 79's repair commit by subject line, over the module's own history."""
    log = _git("log", "--format=%H%x1f%s", "--", MODULE_PATH).strip().splitlines()
    for line in log:
        h, subject = line.split("\x1f", 1)
        if REPAIR_SUBJECT in subject:
            return {"repair_commit": h, "repair_subject": subject,
                    "parent": _git("rev-parse", f"{h}^").strip()}
    raise SystemExit(f"could not find the repair commit ({REPAIR_SUBJECT!r}) in the history "
                     f"of {MODULE_PATH}")


def load_module(source_text, name):
    """Import a source string as a module under its own name, from a real file on disk."""
    tmp = Path(tempfile.mkdtemp(prefix="pcb_")) / f"{name}.py"
    tmp.write_text(source_text)
    spec = importlib.util.spec_from_file_location(name, tmp)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def clause_P1_static(commits):
    """Which top-level definitions did the repair touch, and is any of them on the sweep's path?

    The sweep's call path is deliberately enumerated by reading the function, not guessed:
    `line_sweep_solve` calls only numpy and the injected `thomas`, so its in-module path is
    itself alone.  `make_preconditioner`/`leading_order_solve` are listed too because the
    preconditioner Route-L actually installs is built through them in the radial-only arm.
    """
    diff = _git("diff", "-U0", f"{commits['parent']}..{commits['repair_commit']}",
                "--", MODULE_PATH)
    touched, current = [], None
    for line in diff.splitlines():
        m = re.match(r"^@@.*@@\s*(?:def|class)\s+(\w+)", line)
        if m:
            current = m.group(1)
        if line.startswith("+") and not line.startswith("+++"):
            m2 = re.match(r"^\+\s*(?:def|class)\s+(\w+)", line)
            if m2:
                current = m2.group(1)
            if current and current not in touched:
                touched.append(current)
    sweep_path = ["line_sweep_solve"]
    adjacent = ["make_preconditioner", "leading_order_solve", "gmres", "krylov_ladder"]
    added = sum(1 for ln in diff.splitlines()
                if ln.startswith("+") and not ln.startswith("+++"))
    removed = sum(1 for ln in diff.splitlines()
                  if ln.startswith("-") and not ln.startswith("---"))
    return {"repair_commit": commits["repair_commit"], "parent": commits["parent"],
            "lines_added": added, "lines_removed": removed,
            "top_level_defs_touched": touched,
            "sweep_call_path": sweep_path,
            "adjacent_hot_path": adjacent,
            "defs_touched_on_sweep_path": [d for d in touched if d in sweep_path],
            "defs_touched_adjacent": [d for d in touched if d in adjacent],
            "reading": ("the repair's text is disjoint from the sweep's call path"
                        if not [d for d in touched if d in sweep_path + adjacent] else
                        "the repair touched code the sweep runs through -- the numerical "
                        "arms below are load-bearing, not corroborative")}


# --------------------------------------------------------------------------
# P2 -- the precision arm
# --------------------------------------------------------------------------
def apply_transport(x, s_rho, s_beta, drho, dbeta, c):
    """Apply (-s_rho d_rho - s_beta d_beta + c) with the SAME first-order upwinding the sweep
    inverts.  This is the residual instrument, and it is written here rather than imported so
    that it is identical for both module versions and cannot itself drift across the repair.
    """
    back = np.empty_like(x)
    prev = np.zeros(x.shape[1])
    for i in range(x.shape[0]):
        sr = s_rho[i] / drho
        sb = s_beta[i]
        row = (c - sr) * x[i] + sr * prev
        xm = np.concatenate([[0.0], x[i][:-1]])
        xp = np.concatenate([x[i][1:], [0.0]])
        row = row + np.where(sb > 0, -sb / dbeta * (x[i] - xm), -sb / dbeta * (xp - x[i]))
        back[i] = row
        prev = x[i]
    return back


def make_case(seed, n_r, n_b, drho, dbeta, c, s_rho_lo=0.5, s_rho_hi=4.5):
    rng = np.random.default_rng(seed)
    s_rho = s_rho_lo + (s_rho_hi - s_rho_lo) * rng.random((n_r, n_b))
    s_beta = rng.standard_normal((n_r, n_b))
    rhs = rng.standard_normal((n_r, n_b))
    return {"label": f"seed{seed}_{n_r}x{n_b}", "seed": seed, "n_r": n_r, "n_b": n_b,
            "drho": drho, "dbeta": dbeta, "c": c,
            "min_s_rho": float(s_rho.min()), "max_s_rho": float(s_rho.max()),
            "arrays": (s_rho, s_beta, rhs)}


def precision_battery():
    """24 configurations.  The first is test_7's exact one -- the run 9.5e-16 came from."""
    cases = [make_case(CANONICAL["seed"], CANONICAL["n_r"], CANONICAL["n_b"],
                       CANONICAL["drho"], CANONICAL["dbeta"], CANONICAL["c"])]
    cases[0]["label"] = "CANONICAL(test_7)"
    for seed in (0, 1, 2, 3):
        for (n_r, n_b) in ((48, 16), (96, 32), (192, 48)):
            cases.append(make_case(seed, n_r, n_b, 0.09, 0.033, -1.0145))
    # marginal-but-valid upwinding: s_rho close to zero, where the sweep is worst conditioned
    for seed in (5, 6):
        cases.append(make_case(seed, 96, 32, 0.09, 0.033, -1.0145,
                               s_rho_lo=1e-3, s_rho_hi=5e-3))
        cases[-1]["label"] += "_marginal_s_rho"
    # the Route-L live geometry: c = c_omega-shaped, both field scalings
    for c in (-1.0145, -2.029):
        cases.append(make_case(7, 300, 48, 0.0334, 0.0654, c))
        cases[-1]["label"] += f"_live_c{c}"
    for seed in (8, 9, 10):
        cases.append(make_case(seed, 300, 48, 0.0334, 0.0654, -1.0145))
    return cases


def clause_P2_precision(pre, post):
    rows = []
    worst_pre = worst_post = 0.0
    n_bit_identical = 0
    for case in precision_battery():
        s_rho, s_beta, rhs = case["arrays"]
        args = (rhs, s_rho, s_beta, case["drho"], case["dbeta"], case["c"], _thomas)
        x_pre = pre.line_sweep_solve(*args)
        x_post = post.line_sweep_solve(*args)
        scale = float(np.max(np.abs(rhs)))
        e_pre = float(np.max(np.abs(apply_transport(
            x_pre, s_rho, s_beta, case["drho"], case["dbeta"], case["c"]) - rhs)) / scale)
        e_post = float(np.max(np.abs(apply_transport(
            x_post, s_rho, s_beta, case["drho"], case["dbeta"], case["c"]) - rhs)) / scale)
        bits_pre = x_pre.view(np.uint64)
        bits_post = x_post.view(np.uint64)
        identical = bool(np.array_equal(bits_pre, bits_post))
        n_bit_identical += int(identical)
        differing = int(np.count_nonzero(bits_pre != bits_post))
        max_ulp = int(np.max(np.abs(bits_pre.astype(np.int64)
                                    - bits_post.astype(np.int64)))) if not identical else 0
        worst_pre = max(worst_pre, e_pre)
        worst_post = max(worst_post, e_post)
        rows.append({"case": case["label"], "n_r": case["n_r"], "n_b": case["n_b"],
                     "min_s_rho": case["min_s_rho"],
                     "rel_residual_pre": e_pre, "rel_residual_post": e_post,
                     "post_over_pre": (e_post / e_pre) if e_pre > 0 else
                                      (1.0 if e_post == 0 else float("inf")),
                     "bit_identical": identical, "entries_differing": differing,
                     "max_ulp_gap": max_ulp,
                     "entries": int(case["n_r"] * case["n_b"])})
    canonical = rows[0]
    return {"claimed_precision_gate": CLAIMED_PRECISION,
            "n_cases": len(rows),
            "canonical_case_rel_residual_post": canonical["rel_residual_post"],
            "canonical_case_rel_residual_pre": canonical["rel_residual_pre"],
            "worst_rel_residual_pre": worst_pre,
            "worst_rel_residual_post": worst_post,
            "worst_post_over_claimed_gate": worst_post / CLAIMED_PRECISION,
            "cases_bit_identical": n_bit_identical,
            "cases_total": len(rows),
            "worst_ulp_gap_over_all_cases": max(r["max_ulp_gap"] for r in rows),
            "total_entries_differing": sum(r["entries_differing"] for r in rows),
            "rows": rows}


# --------------------------------------------------------------------------
# P3 -- the timing arm, with its null
# --------------------------------------------------------------------------
def _time_calls(fn, args, calls):
    t0 = time.perf_counter()
    for _ in range(calls):
        fn(*args)
    return (time.perf_counter() - t0) / calls


def clause_P3_timing(pre, post, rounds=15, calls=6):
    """Interleaved pre / post / post-null rounds.

    Each round times the same work three times: the pre-repair function, the post-repair
    function, and the post-repair function AGAIN.  The third arm is the null: its ratio to the
    second is a pure noise measurement -- same code, same data, same machine, same moment -- and
    it is the yardstick the pre/post ratio is read against.  Reporting the pre/post ratio alone
    would be uninterpretable.
    """
    grids = [(300, 48, 0.0334, 0.0654), (96, 32, 0.09, 0.033)]
    out = {}
    for (n_r, n_b, drho, dbeta) in grids:
        case = make_case(4, n_r, n_b, drho, dbeta, -1.0145)
        s_rho, s_beta, rhs = case["arrays"]
        args = (rhs, s_rho, s_beta, drho, dbeta, -1.0145, _thomas)
        pre.line_sweep_solve(*args)                       # warm the caches for both
        post.line_sweep_solve(*args)
        t_pre, t_post, t_null = [], [], []
        for _ in range(rounds):
            t_pre.append(_time_calls(pre.line_sweep_solve, args, calls))
            t_post.append(_time_calls(post.line_sweep_solve, args, calls))
            t_null.append(_time_calls(post.line_sweep_solve, args, calls))
        med_pre, med_post, med_null = (statistics.median(t_pre),
                                       statistics.median(t_post),
                                       statistics.median(t_null))
        out[f"{n_r}x{n_b}"] = {
            "rounds": rounds, "calls_per_round": calls,
            "median_s_pre": med_pre, "median_s_post": med_post, "median_s_null": med_null,
            "min_s_pre": min(t_pre), "min_s_post": min(t_post), "min_s_null": min(t_null),
            "post_over_pre_median": med_post / med_pre,
            "null_over_post_median": med_null / med_post,
            "post_over_pre_min": min(t_post) / min(t_pre),
            "spread_pre_max_over_min": max(t_pre) / min(t_pre),
            "spread_post_max_over_min": max(t_post) / min(t_post),
            "spread_null_max_over_min": max(t_null) / min(t_null),
            "excess_over_noise": (abs(med_post / med_pre - 1.0)
                                  / max(abs(med_null / med_post - 1.0), 1e-12)),
        }
    return out


# --------------------------------------------------------------------------
# P4 -- the consequence arm: the ladder the sweep exists to bend
# --------------------------------------------------------------------------
def clause_P4_ladder(pre, post):
    """A self-contained preconditioned-GMRES ladder, pre vs post.

    The point of the sweep is that it turns a FLAT Krylov ladder into a bending one.  A
    precision regression too small for P2 to care about could still move that.  The operator
    here is the transport operator itself plus a perturbation, so the ladder is meaningful
    without relaunching the whole Route-L relaxation (which is another leg's territory and
    would take an hour).
    """
    rng = np.random.default_rng(21)
    n_r, n_b, drho, dbeta, c = 300, 48, 0.0334, 0.0654, -1.0145
    s_rho = 0.5 + 4.0 * rng.random((n_r, n_b))
    s_beta = rng.standard_normal((n_r, n_b))
    pert = 0.15 * rng.standard_normal((n_r, n_b))
    b = rng.standard_normal((n_r, n_b))

    def make_arms(mod):
        def A(v):
            x = v.reshape(n_r, n_b)
            return (apply_transport(x, s_rho, s_beta, drho, dbeta, c) + pert * x).ravel()

        def Minv(v):
            return mod.line_sweep_solve(v.reshape(n_r, n_b), s_rho, s_beta,
                                        drho, dbeta, c, _thomas).ravel()
        return A, Minv

    out = {}
    for name, mod in (("pre", pre), ("post", post)):
        A, Minv = make_arms(mod)
        rows = mod.krylov_ladder(lambda v: A(Minv(v)), b.ravel(), dims=(10, 20, 40, 80))
        out[name] = {"ladder": rows, "verdict": mod.stall_verdict(rows)}
    rel_pre = out["pre"]["ladder"][-1]["rel_residual"]
    rel_post = out["post"]["ladder"][-1]["rel_residual"]
    rungs_identical = sum(1 for a, b in zip(out["pre"]["ladder"], out["post"]["ladder"])
                          if a["rel_residual"] == b["rel_residual"])
    out["comparison"] = {
        "rel_at_max_dim_pre": rel_pre, "rel_at_max_dim_post": rel_post,
        "post_over_pre": (rel_post / rel_pre) if rel_pre > 0 else
                         (1.0 if rel_post == 0 else float("inf")),
        "gain_pre": out["pre"]["verdict"]["residual_gain"],
        "gain_post": out["post"]["verdict"]["residual_gain"],
        "rungs_identical": rungs_identical,
        "rungs_total": len(out["pre"]["ladder"]),
        "identical": bool(rel_pre == rel_post)}
    return out


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="fewer timing rounds")
    ap.add_argument("--out", default=str(ROOT / "writeup/data/p2_route_pcb_v1_postrepair.json"))
    args = ap.parse_args()

    t0 = time.time()
    commits = find_repair_commit()
    print(f"[PCB] repair commit {commits['repair_commit'][:8]} "
          f"({commits['repair_subject'][:60]}...)")
    pre_src = _git("show", f"{commits['parent']}:{MODULE_PATH}")
    post_src = (ROOT / MODULE_PATH).read_text()
    pre = load_module(pre_src, "pcb_pre_repair")
    post = load_module(post_src, "pcb_post_repair")
    assert not hasattr(pre, "_hypothesis_violations"), \
        "the 'pre' module already carries the repair -- the commit lookup is wrong"
    assert hasattr(post, "_hypothesis_violations"), \
        "the working-tree module does not carry the repair"
    print(f"[PCB] pre-repair module {len(pre_src.splitlines())} lines, "
          f"post-repair {len(post_src.splitlines())} lines")

    res = {"leg": 86, "route": "PCB", "version": 1,
           "gate": ("After the bench-repair, does solver/port_certification.py's line-sweep "
                    "preconditioner still (a) hit the 9.5e-16 precision gate it was originally "
                    "validated to, and (b) run within normal benchmark variance of its "
                    "pre-repair timing?")}

    print("[P1] static: what the repair's text touched ...")
    res["P1_static"] = clause_P1_static(commits)
    p1 = res["P1_static"]
    print(f"  [P1] +{p1['lines_added']}/-{p1['lines_removed']} lines, defs touched "
          f"{p1['top_level_defs_touched']}; on the sweep's path: "
          f"{p1['defs_touched_on_sweep_path'] or 'none'}")

    print("[P2] precision: exactness battery, pre vs post, bit-for-bit ...")
    res["P2_precision"] = clause_P2_precision(pre, post)
    p2 = res["P2_precision"]
    print(f"  [P2] canonical case {p2['canonical_case_rel_residual_post']:.3e} "
          f"(claim {CLAIMED_PRECISION:.1e}); worst of {p2['n_cases']} cases "
          f"{p2['worst_rel_residual_post']:.3e} = "
          f"{p2['worst_post_over_claimed_gate']:.2f}x the claimed gate; "
          f"bit-identical pre/post in {p2['cases_bit_identical']}/{p2['cases_total']} cases, "
          f"{p2['total_entries_differing']} entries differing")

    print("[P3] timing: interleaved pre / post / post-null ...")
    res["P3_timing"] = clause_P3_timing(pre, post,
                                        rounds=5 if args.quick else 15,
                                        calls=3 if args.quick else 6)
    for grid, t in res["P3_timing"].items():
        print(f"  [P3] {grid}: pre {t['median_s_pre']*1e3:.2f} ms, "
              f"post {t['median_s_post']*1e3:.2f} ms -> ratio {t['post_over_pre_median']:.4f}; "
              f"null (post/post) {t['null_over_post_median']:.4f}; "
              f"excess/noise {t['excess_over_noise']:.2f}")

    print("[P4] consequence: preconditioned Krylov ladder, pre vs post ...")
    res["P4_ladder"] = clause_P4_ladder(pre, post)
    p4 = res["P4_ladder"]["comparison"]
    print(f"  [P4] rel at m=80: pre {p4['rel_at_max_dim_pre']:.6e}, "
          f"post {p4['rel_at_max_dim_post']:.6e} (ratio {p4['post_over_pre']:.6f}); "
          f"gain {p4['gain_pre']:.2f} -> {p4['gain_post']:.2f}")

    # ---- the gate answer, assembled from magnitudes only ----
    worst_ratio = max(abs(t["post_over_pre_median"] - 1.0) for t in res["P3_timing"].values())
    worst_noise = max(abs(t["null_over_post_median"] - 1.0) for t in res["P3_timing"].values())

    # (a) THE PRECISION CRITERION, and why it is written this way.
    # The 9.5e-16 in capabilities.py is the number test_7's ONE configuration produces; it is a
    # per-configuration figure, not a uniform bound over grids.  So "still hits the gate" is two
    # separate statements, and conflating them would answer the wrong question:
    #   (a1) the configuration the claim was measured on still returns <= 9.5e-16, and
    #   (a2) NOTHING in the battery moved across the repair -- bit-for-bit.
    # A battery-wide worst case above 9.5e-16 is a fact about the CLAIM'S SCOPE, and it is only
    # attributable to the repair if it differs pre vs post.  It is reported below as a magnitude,
    # separately, with its pre-repair twin beside it, so the two readings cannot be mixed up.
    canon_ok = p2["canonical_case_rel_residual_post"] <= CLAIMED_PRECISION
    unmoved = p2["cases_bit_identical"] == p2["cases_total"]
    precision_ok = canon_ok and unmoved
    timing_ok = worst_ratio <= max(3.0 * worst_noise, 0.10)
    scope = {
        "worst_rel_residual_post": p2["worst_rel_residual_post"],
        "worst_rel_residual_pre": p2["worst_rel_residual_pre"],
        "worst_over_claimed_gate": p2["worst_post_over_claimed_gate"],
        "moved_across_the_repair": bool(p2["worst_rel_residual_post"]
                                        != p2["worst_rel_residual_pre"]),
        "note": ("PRE-EXISTING, NOT A REGRESSION when moved_across_the_repair is false: the "
                 "9.5e-16 figure is test_7's single configuration, and the battery's worst case "
                 "is larger on bigger grids in BOTH module versions by the identical amount. "
                 "This is a scope caveat on how capabilities.py words the claim, not an effect "
                 "of leg 79's repair.")}
    res["gate_answer"] = {
        "a_precision": {
            "canonical_case_post": p2["canonical_case_rel_residual_post"],
            "canonical_case_pre": p2["canonical_case_rel_residual_pre"],
            "claimed_gate": CLAIMED_PRECISION,
            "canonical_margin_factor": (CLAIMED_PRECISION
                                        / max(p2["canonical_case_rel_residual_post"], 1e-300)),
            "canonical_meets_claimed_gate": bool(canon_ok),
            "bit_identical_cases": f"{p2['cases_bit_identical']}/{p2['cases_total']}",
            "total_entries_differing": p2["total_entries_differing"],
            "worst_ulp_gap": p2["worst_ulp_gap_over_all_cases"],
            "nothing_moved_across_the_repair": bool(unmoved),
            "battery_scope_caveat": scope,
            "meets_gate": bool(precision_ok)},
        "b_timing": {
            "worst_abs_pre_post_deviation": worst_ratio,
            "worst_null_arm_deviation": worst_noise,
            "criterion": "|post/pre - 1| <= max(3 x null deviation, 10%)",
            "sign_consistent_across_grids": bool(
                len({t["post_over_pre_median"] > 1.0 for t in res["P3_timing"].values()}) == 1),
            "within_variance": bool(timing_ok)},
        "answer": "yes" if (precision_ok and timing_ok) else "no",
        "reading": ("no precision or performance regression -- the repair was surgical"
                    if (precision_ok and timing_ok) else
                    "a regression is present; see the clause that failed")}

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(res, indent=1))
    g = res["gate_answer"]
    print(f"\n[PCB] GATE: {g['answer'].upper()} -- canonical configuration "
          f"{g['a_precision']['canonical_case_post']:.3e} vs claim {CLAIMED_PRECISION:.1e} "
          f"({g['a_precision']['canonical_margin_factor']:.2f}x margin), bit-identical "
          f"{g['a_precision']['bit_identical_cases']}; timing deviation "
          f"{g['b_timing']['worst_abs_pre_post_deviation']:.2%} against a null arm of "
          f"{g['b_timing']['worst_null_arm_deviation']:.2%}")
    print(f"[PCB] wrote {args.out}  ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
