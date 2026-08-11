"""Route-CAPA v2 (leg 292) -- the SECOND-GENERATION freshness audit of capabilities.py.

Leg 71 (Route-CAP) ran the first generation at merge base `e203b52`: 42 rows, 40
distinct cited tests, 2 RED at HEAD, 1 `test` field corrected.  ~220 legs have landed
since.  This runner re-asks the same question at the current HEAD and adds the axis
leg 71 flagged but did not systematise: the **known-answer-gate presence** encoded in
each row's `validated` field.

WHAT THIS MEASURES (four axes, each reported as a COUNT, never a boolean)

  S1  module completeness, both directions
        - solver/*.py on disk with no row  ("missing")
        - rows naming a module not on disk ("ghost")
  S2  cited-test existence -- every row's `test` field resolves to a file on disk
  S3  GREENNESS AT HEAD -- every distinct cited test file actually executed
        (`<python> test_x.py`, this repo's convention: each test_*.py is a
        self-running script, no pytest).  This is precisely the check
        `test_capabilities.py` does NOT do: the drift detector asserts the cited path
        EXISTS and that `validated` is longer than 20 characters, never that the test
        runs, passes, or has anything to do with the module citing it.
  S5  RELEVANCE -- does the cited test file actually LOAD the module citing it?  Leg 71
        named this gap in words ("existence is checked; greenness and relevance are
        not") and found one instance by hand (solver/ga_search.py cited test_ga.py,
        which imports only the `ga/` package and never touches the module).  It never
        systematised the check.  This runner does: for each row, the cited test file is
        scanned -- and so are the local test-side helpers it imports -- for any
        `solver.<name>` / `solver/<name>.py` reference.  A row whose test never mentions
        its own module is a confidently-worded pointer at a test that cannot fail when
        the module breaks, which is strictly worse than an empty field.
  S4  known-answer-gate presence -- does the `validated` field state a gate with a
        MAGNITUDE, or does it say "no known-answer gate" plainly (which the file's own
        header declares to be an acceptable, honest value), or is it prose that claims
        validation while naming no number at all?  The third class is the stale-prose
        risk surface.

OPERATIONAL LESSON CARRIED FORWARD (leg 71, commit e742f6d, measured not guessed):
at 6 parallel workers this box thrashed -- test_marginal_flow.py went 112s -> >3600s,
a 32x blowup consistent with BLAS thread oversubscription.  At 3 workers there were no
timeouts and the same 40 tests cost 8,426s against 22,839s, 37% of the cumulative time.
This runner therefore pins OMP/MKL/OPENBLAS/NUMEXPR thread counts to 1 in every child
and defaults to a small worker count; `--workers` is exposed so the number that was
actually used is recorded in the JSON rather than assumed.

FLAKE DIAGNOSIS BEFORE BELIEF (ORCHESTRATION.md 9g): a test that comes back non-zero
under a loaded parallel sweep is NOT recorded as red-at-HEAD on that evidence.  Pass
`--recheck t1.py t2.py ...` to re-run named tests ALONE, serially, with the same pinned
environment; the JSON records both the sweep verdict and the solo verdict, and the two
disagreeing IS the finding (a flake), not an inconvenience.

USAGE
    .venv/bin/python experiments/p2_route_capa_v2_audit.py                 # full sweep
    .venv/bin/python experiments/p2_route_capa_v2_audit.py --workers 1
    .venv/bin/python experiments/p2_route_capa_v2_audit.py --static-only   # S1/S2/S4
    .venv/bin/python experiments/p2_route_capa_v2_audit.py --recheck test_x.py
    .venv/bin/python experiments/p2_route_capa_v2_audit.py --figure        # fig only

Writes writeup/data/p2_route_capa_v2_audit.json and, with --figure,
writeup/figures/fig67_route_capa_v2_audit.png.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from capabilities import CAPABILITIES  # noqa: E402

DATA = ROOT / "writeup" / "data" / "p2_route_capa_v2_audit.json"
FIG = ROOT / "writeup" / "figures" / "fig67_route_capa_v2_audit.png"

# Pinned so a parallel sweep cannot oversubscribe the BLAS pool (leg 71's 32x blowup).
PINNED_ENV = {
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
}

# A `validated` field earns "gate with a magnitude" only if it names a NUMBER of the
# kind a known-answer gate produces: an exponent, a decimal, a percentage, an x-factor.
_MAGNITUDE = re.compile(
    r"(\d+\.?\d*[eE][-+]?\d+)"      # 4.4e-16
    r"|(\d+\.\d+)"                  # 2.5114
    r"|(\d+\s?%)"                   # 3 %
    r"|(\d+\.?\d*\s?x\b)"           # 42x
    r"|(\b\d{2,}\b)"                # 1024
)
_NO_GATE = re.compile(r"no known[- ]answer gate", re.I)


def python_exe() -> str:
    """The repo convention is .venv/bin/python; fall back to the running interpreter.

    A worktree may not carry its own .venv, so the main checkout's is tried too.
    """
    for cand in (ROOT / ".venv" / "bin" / "python",
                 ROOT.parent.parent.parent / ".venv" / "bin" / "python"):
        if cand.exists() and os.access(cand, os.X_OK):
            return str(cand)
    return sys.executable


# --------------------------------------------------------------------------------
# S1 / S2 / S4 -- static axes
# --------------------------------------------------------------------------------

def disk_modules() -> list[str]:
    return sorted(
        f"solver/{p.name}" for p in (ROOT / "solver").glob("*.py")
        if p.name != "__init__.py"
    )


def cited_test_files(entry: dict) -> list[str]:
    """A `test` field may name more than one file; take every *.py token in it."""
    raw = entry.get("test", "") or ""
    return [tok for tok in re.split(r"[\s,;]+", raw) if tok.endswith(".py")]


def _test_text_with_local_imports(test: str, depth: int = 1) -> str:
    """The test's own source, plus the source of any sibling test_*/helper it imports.

    A row is not stale merely because the loading happens one file away (a dedicated
    test importing a shared harness), so the scan follows local imports one hop.
    """
    p = ROOT / test
    if not p.exists():
        return ""
    text = p.read_text(errors="replace")
    if depth <= 0:
        return text
    for m in re.finditer(r"^\s*(?:from|import)\s+([A-Za-z_][\w]*)", text, re.M):
        name = m.group(1)
        if name in ("solver", "ga"):
            continue
        sib = ROOT / f"{name}.py"
        if sib.exists() and sib != p:
            text += "\n" + sib.read_text(errors="replace")
    return text


def relevance_axis(rows: list[dict]) -> list[dict]:
    """S5: for every row, does any cited test actually reference the module?"""
    out = []
    for r in rows:
        mod = r.get("module", "")
        stem = Path(mod).stem                      # e.g. "ga_search"
        pats = [f"solver.{stem}", f"solver/{stem}.py", f"import {stem}"]
        hits, per_test = [], {}
        for t in cited_test_files(r):
            text = _test_text_with_local_imports(t)
            found = [pat for pat in pats if pat in text]
            per_test[t] = found
            hits += found
        out.append({
            "module": mod,
            "tests": cited_test_files(r),
            "loads_module": bool(hits),
            "per_test": per_test,
        })
    return out


def check_count_claims(rows: list[dict]) -> list[dict]:
    """Rows whose `validated` prose claims 'test_x.py (N checks)' -- verify N.

    A count is the most falsifiable thing a `validated` field can say, so it is the
    cheapest place to catch prose that a later leg overtook without correcting the row.
    N is compared against the number of `def test_*` functions in the named file.
    """
    out = []
    pat = re.compile(r"(test_[\w]+\.py)\s*\((\d+)\s+checks?\)")
    for r in rows:
        for m in pat.finditer(r.get("validated", "") or ""):
            fname, claimed = m.group(1), int(m.group(2))
            f = ROOT / fname
            actual = (len(re.findall(r"^def test_", f.read_text(errors="replace"), re.M))
                      if f.exists() else None)
            out.append({
                "module": r["module"], "file": fname,
                "claimed_checks": claimed, "actual_test_defs": actual,
                "agrees": (actual == claimed),
            })
    return out


def artifact_references(rows: list[dict]) -> list[dict]:
    """S6: `validated`/`holds` prose that cites a repo PATH -- does the path still exist?

    Several rows point at their evidence by filename (writeup/data/*.json,
    experiments/*.py, test_*.py named inside the prose rather than in the `test` field).
    Those are load-bearing citations -- a reader follows them to check the claim -- and
    nothing in the repository checks them.  A moved or deleted artifact leaves the claim
    unfalsifiable while still reading as evidenced.
    """
    pat = re.compile(
        r"\b((?:writeup|experiments|solver|reports|docs|ga)/[\w./-]+\.\w+"
        r"|test_[\w]+\.py"
        r"|[\w]+\.(?:json|md|py))\b")
    # A bare filename in the prose is written the way a reader would say it out loud
    # ("port_certification.py 11/25"), not as a path from the repo root, so a bare name
    # is resolved against the directories this repository actually keeps things in
    # before it is called dangling.
    roots = ["", "solver/", "writeup/data/", "experiments/", "ga/", "reports/", "docs/"]
    seen, out = set(), []
    for r in rows:
        prose = (r.get("validated", "") or "") + " " + (r.get("holds", "") or "")
        # Reflow: the prose is hard-wrapped with embedded newlines and padding spaces.
        # Collapse to a SINGLE space -- deleting the whitespace outright welds the last
        # word of one line onto the first of the next and manufactures fake filenames.
        prose = re.sub(r"\s*\n\s*", " ", prose)
        for m in pat.finditer(prose):
            path = m.group(1)
            key = (r["module"], path)
            if key in seen:
                continue
            seen.add(key)
            hit = next((f"{root}{path}" for root in roots
                        if (ROOT / f"{root}{path}").exists()), None)
            out.append({
                "module": r["module"],
                "cited_path": path,
                "resolved_as": hit,
                "exists": hit is not None,
            })
    return out


def vacuity_axis(tests: list[str]) -> list[dict]:
    """S8: is a GREEN result meaningful, or did the file exit 0 having run nothing?

    This repo runs `<python> test_x.py` -- there is no pytest.  A file written in the
    pytest style (`def test_*` functions, no `__main__` block, no module-level calls)
    therefore imports cleanly, defines some functions, and exits 0 WITHOUT EXECUTING A
    SINGLE ASSERTION.  It is green, it is worthless, and every existence-based check in
    the repository passes it.  Leg 71 tracked this as `S2_runtime_noop`.

    Classification:
      "main-block"      has `if __name__ == "__main__":` -> the calls happen there
      "module-level"    no main block, but 0 `def test_` and real top-level statements
                        (the `gate(...)`/`sys.exit(n_fail)` script style this repo uses)
      "VACUOUS"         `def test_` functions AND no main block -> nothing runs
    """
    out = []
    for t in tests:
        p = ROOT / t
        if not p.exists():
            out.append({"test": t, "style": "missing", "n_test_defs": 0})
            continue
        src = p.read_text(errors="replace")
        n_defs = len(re.findall(r"^def test_", src, re.M))
        has_main = "__main__" in src
        if has_main:
            style = "main-block"
        elif n_defs == 0:
            style = "module-level"
        else:
            style = "VACUOUS"
        out.append({"test": t, "style": style, "n_test_defs": n_defs,
                    "has_main_block": has_main})
    return out


def merge_gate_coverage(rows: list[dict]) -> list[dict]:
    """S7: does scripts/merge_gate.sh's OWN name mapping resolve for each module?

    The merge gate maps a changed `solver/<name>.py` to `test_<name>.py` at the repo
    root and runs it only IF that file exists.  A module whose test is named anything
    else is therefore ungated: editing it triggers no test at merge time, however good
    the test cited in this index is.  Leg 71 measured this and flagged 6 of 42 rows
    `S4_ungated_by_merge_gate`; re-measured here at HEAD for the cross-generation delta.
    """
    out = []
    for r in rows:
        stem = Path(r["module"]).stem
        implied = f"test_{stem}.py"
        out.append({
            "module": r["module"],
            "merge_gate_implied_test": implied,
            "exists": (ROOT / implied).exists(),
            "index_cites": r.get("test", ""),
        })
    return out


def static_axes() -> dict:
    rows = list(CAPABILITIES)
    mods = [r.get("module", "") for r in rows]
    on_disk = disk_modules()

    dup = sorted({m for m in mods if mods.count(m) > 1})
    missing = sorted(set(on_disk) - set(mods))     # S1: module with no row
    ghost = sorted(set(mods) - set(on_disk))       # S1: row with no module

    per_row, absent_tests, no_test_field = [], [], []
    for r in rows:
        files = cited_test_files(r)
        if not files:
            no_test_field.append(r.get("module", "?"))
        gone = [f for f in files if not (ROOT / f).exists()]
        if gone:
            absent_tests.append({"module": r["module"], "absent": gone})
        val = r.get("validated", "") or ""
        if _NO_GATE.search(val):
            gate = "declared-absent"
        elif _MAGNITUDE.search(val):
            gate = "magnitude"
        else:
            gate = "prose-without-magnitude"
        per_row.append({
            "module": r.get("module", "?"),
            "object": r.get("object", ""),
            "tests": files,
            "validated_chars": len(val),
            "gate_class": gate,
            "superseded": "supersed" in (r.get("object", "") + r.get("holds", "")).lower(),
        })

    distinct = sorted({f for r in rows for f in cited_test_files(r)})
    rel = relevance_axis(rows)
    counts = check_count_claims(rows)
    return {
        "S5_relevance": rel,
        "S5_rows_whose_test_never_loads_the_module":
            [r["module"] for r in rel if not r["loads_module"]],
        "count_claims": counts,
        "count_claims_disagreeing": [c for c in counts if not c["agrees"]],
        "S8_vacuity": (vac := vacuity_axis(distinct)),
        "S8_vacuous_tests": [v["test"] for v in vac if v["style"] == "VACUOUS"],
        "S8_style_counts": {k: sum(1 for v in vac if v["style"] == k)
                            for k in ("main-block", "module-level", "VACUOUS")},
        "S7_merge_gate_coverage": (mg := merge_gate_coverage(rows)),
        "S7_modules_ungated_by_merge_gate": [m["module"] for m in mg if not m["exists"]],
        "S6_artifact_references": (refs := artifact_references(rows)),
        "S6_n_cited_paths": len(refs),
        "S6_dangling_paths": [r for r in refs if not r["exists"]],
        "n_rows": len(rows),
        "n_distinct_modules": len(set(mods)),
        "n_modules_on_disk": len(on_disk),
        "duplicate_module_rows": dup,
        "S1_missing_rows": missing,
        "S1_ghost_rows": ghost,
        "S2_rows_with_absent_test_file": absent_tests,
        "S2_rows_with_no_test_field": no_test_field,
        "n_distinct_cited_tests": len(distinct),
        "distinct_cited_tests": distinct,
        "S4_gate_class_counts": {
            k: sum(1 for p in per_row if p["gate_class"] == k)
            for k in ("magnitude", "declared-absent", "prose-without-magnitude")
        },
        "rows": per_row,
    }


# --------------------------------------------------------------------------------
# S3 -- greenness at HEAD
# --------------------------------------------------------------------------------

def run_one(test: str, timeout: int) -> dict:
    env = dict(os.environ)
    env.update(PINNED_ENV)
    t0 = time.time()
    try:
        p = subprocess.run(
            [python_exe(), test], cwd=str(ROOT), env=env,
            capture_output=True, text=True, timeout=timeout,
        )
        rc, out, err, timed_out = p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        rc, timed_out = None, True
        out = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = (e.stderr or b"").decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
    wall = time.time() - t0
    return {
        "test": test,
        "returncode": rc,
        "timed_out": timed_out,
        "green": (rc == 0),
        "wall_s": round(wall, 2),
        "stdout_tail": out[-1200:],
        "stderr_tail": err[-2500:],
    }


SWEEP_LINE = re.compile(
    r"^\[\s*\d+/\s*\d+\]\s+(ok|RED|TMO)\s+([\d.]+)s\s+(\S+)\s*$")


def ingest_sweep_log(path: Path) -> list[dict]:
    """Reconstruct sweep verdicts from the runner's own printed progress lines.

    WHY THIS EXISTS, stated plainly so a later reader does not mistake it for a
    convenience: this audit's sweep is hours long, and on the run of record the driver
    process was killed by the surrounding harness at 45 of 46 tests -- after every one
    of those 45 verdicts had been printed, but before the JSON was serialised.  The
    verdicts are real measurements (each is the exit status of a real subprocess); the
    only thing lost was the serialisation step.  Discarding them and re-running would
    not have made them truer, so they are ingested from the log the runner itself
    printed, and every ingested record is stamped `source: "log-ingest"` so it can never
    be confused with a record this process observed directly.

    The per-test stdout/stderr tails are NOT recoverable this way and are recorded as
    empty rather than fabricated.
    """
    out = []
    for line in path.read_text(errors="replace").splitlines():
        m = SWEEP_LINE.match(line.strip())
        if not m:
            continue
        flag, wall, test = m.group(1), float(m.group(2)), m.group(3)
        out.append({
            "test": test,
            "returncode": (0 if flag == "ok" else None),
            "timed_out": (flag == "TMO"),
            "green": (flag == "ok"),
            "wall_s": wall,
            "stdout_tail": "",
            "stderr_tail": "",
            "source": "log-ingest",
        })
    return sorted(out, key=lambda r: r["test"])


def sweep(tests: list[str], workers: int, timeout: int) -> list[dict]:
    results = []
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_one, t, timeout): t for t in tests}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            r = fut.result()
            results.append(r)
            flag = "ok  " if r["green"] else ("TMO " if r["timed_out"] else "RED ")
            print(f"[{i:3d}/{len(tests)}] {flag} {r['wall_s']:8.1f}s  {r['test']}", flush=True)
    return sorted(results, key=lambda r: r["test"])


# --------------------------------------------------------------------------------
# figure
# --------------------------------------------------------------------------------

def make_figure(payload: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    st = payload["static"]
    runs = payload.get("sweep", []) or []
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12.5, 5.4))

    # left: the five audit axes, as counts of clean vs. flagged
    axes = ["S1 completeness\nmissing + ghost rows",
            "S2 cited test\nfile absent",
            "S3 greenness\nred at HEAD",
            "S4 `validated`\nnames no magnitude",
            "S5 relevance\ntest never loads module"]
    flagged = [
        len(st["S1_missing_rows"]) + len(st["S1_ghost_rows"]),
        len(st["S2_rows_with_absent_test_file"]) + len(st["S2_rows_with_no_test_field"]),
        sum(1 for r in runs if not r["green"]),
        st["S4_gate_class_counts"]["prose-without-magnitude"],
        len(st.get("S5_rows_whose_test_never_loads_the_module", [])),
    ]
    totals = [st["n_rows"], st["n_rows"], len(runs) or 1, st["n_rows"], st["n_rows"]]
    clean = [t - f for t, f in zip(totals, flagged)]
    y = range(len(axes))
    ax0.barh(list(y), clean, color="#3b6ea5", label="clean")
    ax0.barh(list(y), flagged, left=clean, color="#c1512b", label="flagged")
    ax0.set_yticks(list(y))
    ax0.set_yticklabels(axes, fontsize=8.5)
    ax0.invert_yaxis()
    ax0.set_xlabel("rows (S1/S2/S4/S5) or distinct cited tests (S3)")
    ax0.set_title("the five freshness axes  (S3 and S5 are the two the\n"
                  "drift detector structurally cannot check)", fontsize=10)
    for i, (c, f) in enumerate(zip(clean, flagged)):
        ax0.text(c + f + 0.6, i, f"{f} flagged / {c + f}", va="center", fontsize=9,
                 color=("#c1512b" if f else "#333333"),
                 fontweight=("bold" if f else "normal"))
    ax0.legend(loc="center right", fontsize=9, framealpha=0.95)
    ax0.set_xlim(0, max(totals) * 1.42)

    # right: the cost distribution -- what an executable index costs to keep honest
    if runs:
        walls = sorted(r["wall_s"] for r in runs)
        ax1.plot(range(1, len(walls) + 1), walls, "o-", ms=3.5, color="#3b6ea5")
        ax1.set_yscale("log")
        ax1.set_xlabel("cited test, ranked by wall time")
        ax1.set_ylabel("wall time (s, log)")
        tot = sum(walls)
        ax1.set_title(
            f"cost of executing the index: {len(walls)} tests, "
            f"{tot / 3600:.2f} h cumulative\nmedian {walls[len(walls) // 2]:.1f}s, "
            f"max {walls[-1]:.0f}s",
            fontsize=11)
        ax1.grid(alpha=0.3, which="both")
    else:
        ax1.text(0.5, 0.5, "no sweep in this run (--static-only)",
                 ha="center", va="center", transform=ax1.transAxes)
        ax1.set_axis_off()

    fig.suptitle(
        "capabilities.py freshness audit, second generation (leg 292; first was leg 71)",
        fontsize=12)
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"[fig] {FIG}")


# --------------------------------------------------------------------------------

def git_head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT),
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=5400)
    ap.add_argument("--static-only", action="store_true")
    ap.add_argument("--recheck", nargs="*", default=None,
                    help="re-run these tests ALONE, serially (flake diagnosis)")
    ap.add_argument("--figure", action="store_true", help="rebuild the figure from JSON")
    ap.add_argument("--ingest-sweep-log", type=str, default=None,
                    help="reconstruct sweep verdicts from a killed run's progress log")
    ap.add_argument("--only", nargs="*", default=None,
                    help="sweep only these tests and MERGE them into the banked sweep "
                         "(used to finish a sweep whose driver was interrupted)")
    args = ap.parse_args()

    if args.figure and DATA.exists():
        make_figure(json.loads(DATA.read_text()))
        return 0

    payload = json.loads(DATA.read_text()) if DATA.exists() else {}
    # Metadata keys mirror leg 71's writeup/data/p2_route_cap_v1_audit.json so the two
    # generations of this audit can be diffed directly rather than read side by side.
    payload["leg"] = 292
    payload["route"] = "CAPA"
    payload["generation"] = 2
    payload["predecessor"] = {"leg": 71, "route": "CAP",
                              "data": "writeup/data/p2_route_cap_v1_audit.json",
                              "rows": 42, "distinct_tests": 40}
    payload["convention"] = (
        "no pytest in this repo; every test_*.py is a self-running script run as "
        "`<python> test_x.py` (scripts/merge_gate.sh)")
    payload["gate"] = (
        "Does a fresh audit find every solver/*.py module represented by an accurate "
        "capability line (test presence, pass status, known-answer gate presence), "
        "with zero modules missing and zero stale entries?")
    payload["axes"] = {
        "S1": "module completeness, both directions",
        "S2": "cited-test existence",
        "S3": "greenness at HEAD -- every distinct cited test actually executed",
        "S4": "known-answer-gate presence in the `validated` field",
        "S5": "relevance -- does the cited test actually load the module citing it",
        "S6": "artifact-reference integrity -- do repo paths cited in row prose exist",
    }
    payload["head"] = git_head()
    payload["python"] = python_exe()
    payload["static"] = static_axes()
    st = payload["static"]

    print(f"S1  rows {st['n_rows']}  modules-on-disk {st['n_modules_on_disk']}  "
          f"missing {len(st['S1_missing_rows'])}  ghost {len(st['S1_ghost_rows'])}")
    print(f"S2  rows with an absent cited test file: "
          f"{len(st['S2_rows_with_absent_test_file'])}; with no test field: "
          f"{len(st['S2_rows_with_no_test_field'])}")
    print(f"S4  gate classes: {st['S4_gate_class_counts']}")
    print(f"S5  rows whose cited test never loads the module: "
          f"{st['S5_rows_whose_test_never_loads_the_module']}")
    print(f"    `(N checks)` prose claims: {len(st['count_claims'])}, "
          f"disagreeing: {st['count_claims_disagreeing']}")
    print(f"S6  repo paths cited in row prose: {st['S6_n_cited_paths']}, "
          f"dangling: {len(st['S6_dangling_paths'])}")
    print(f"S7  modules ungated by merge_gate.sh's name mapping: "
          f"{len(st['S7_modules_ungated_by_merge_gate'])} "
          f"{st['S7_modules_ungated_by_merge_gate']}")
    print(f"S8  run styles {st['S8_style_counts']}; VACUOUS (green but nothing runs): "
          f"{st['S8_vacuous_tests']}")
    for d in st["S6_dangling_paths"]:
        print(f"      DANGLING  {d['module']} -> {d['cited_path']}")
    print(f"S3  distinct cited tests to execute: {st['n_distinct_cited_tests']}")

    if args.ingest_sweep_log:
        got = ingest_sweep_log(Path(args.ingest_sweep_log))
        have = {r["test"] for r in payload.get("sweep", [])}
        merged = payload.get("sweep", []) + [r for r in got if r["test"] not in have]
        payload["sweep"] = sorted(merged, key=lambda r: r["test"])
        payload["sweep_source_log"] = args.ingest_sweep_log
        missing = sorted(set(st["distinct_cited_tests"]) -
                         {r["test"] for r in payload["sweep"]})
        print(f"[ingest] {len(got)} verdicts from log; sweep now "
              f"{len(payload['sweep'])} of {st['n_distinct_cited_tests']}; "
              f"still missing: {missing}")
    elif args.only:
        fresh = sweep(args.only, args.workers, args.timeout)
        keep = [r for r in payload.get("sweep", [])
                if r["test"] not in {f["test"] for f in fresh}]
        payload["sweep"] = sorted(keep + fresh, key=lambda r: r["test"])
        missing = sorted(set(st["distinct_cited_tests"]) -
                         {r["test"] for r in payload["sweep"]})
        print(f"[only] sweep now {len(payload['sweep'])} of "
              f"{st['n_distinct_cited_tests']}; still missing: {missing}")
    elif args.recheck is not None:
        tests = args.recheck or [r["test"] for r in payload.get("sweep", [])
                                 if not r["green"]]
        print(f"[recheck] {len(tests)} test(s), serial, pinned env")
        solo = [run_one(t, args.timeout) for t in tests]
        for r in solo:
            print(f"  {'ok ' if r['green'] else 'RED'} {r['wall_s']:8.1f}s  {r['test']}")
        payload["recheck_solo"] = solo
        payload["recheck_workers"] = 1
    elif not args.static_only:
        payload["sweep_workers"] = args.workers
        payload["sweep_timeout_s"] = args.timeout
        t0 = time.time()
        payload["sweep"] = sweep(st["distinct_cited_tests"], args.workers, args.timeout)
        payload["sweep_wall_s"] = round(time.time() - t0, 1)
        red = [r["test"] for r in payload["sweep"] if not r["green"]]
        print(f"\nS3  {len(payload['sweep']) - len(red)} green / "
              f"{len(payload['sweep'])} executed; {len(red)} non-green: {red}")
        print(f"    sweep wall {payload['sweep_wall_s']}s at {args.workers} workers; "
              f"cumulative test time "
              f"{sum(r['wall_s'] for r in payload['sweep']):.0f}s")

    runs = payload.get("sweep", []) or []
    solo = payload.get("recheck_solo", []) or []
    solo_red = [r["test"] for r in solo if not r["green"]]
    payload["summary"] = {
        "n_rows": st["n_rows"],
        "S1_missing": len(st["S1_missing_rows"]),
        "S1_ghost": len(st["S1_ghost_rows"]),
        "S2_absent_test_files": len(st["S2_rows_with_absent_test_file"]),
        "S3_executed": len(runs),
        "S3_green_in_sweep": sum(1 for r in runs if r["green"]),
        "S3_nongreen_in_sweep": sum(1 for r in runs if not r["green"]),
        "S3_red_after_solo_recheck": len(solo_red),
        "S3_red_after_solo_recheck_names": solo_red,
        "S4_magnitude": st["S4_gate_class_counts"]["magnitude"],
        "S4_declared_absent": st["S4_gate_class_counts"]["declared-absent"],
        "S4_prose_without_magnitude": st["S4_gate_class_counts"]["prose-without-magnitude"],
        "S5_irrelevant_pointers": len(st["S5_rows_whose_test_never_loads_the_module"]),
        "S6_cited_paths": st["S6_n_cited_paths"],
        "S6_dangling": len(st["S6_dangling_paths"]),
        "count_claims_checked": len(st["count_claims"]),
        "count_claims_disagreeing": len(st["count_claims_disagreeing"]),
    }
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"[data] {DATA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
