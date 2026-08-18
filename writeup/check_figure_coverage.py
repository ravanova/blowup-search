"""Does `build_figures.py` self-check every figure the record cites?

Unit `D-REPAIR` (wave 5). Lesson 68: a check that is not executable decays. This is the
executable form of that question, so the answer is a re-runnable measurement rather than a
claim in a journal:

    .venv/bin/python writeup/check_figure_coverage.py

It is MECHANICAL end to end -- nothing here reads a comment, a heading or a sentence:

  CITED     figure ids that appear as `figNN` anywhere in the record's markdown
            (writeup/**/*.md plus the repo-root *.md files), i.e. what a reader is
            told exists.
  REBUILT   figure ids whose `.png` filename appears in a source file that
            `build_figures.py` actually executes -- its own body, plus every script in
            its `P2_EVIDENCE` list (parsed with `ast`, never grepped, so a figure named
            only in a comment does not count).
  SELFCHK   of those, the ids whose rebuild script also carries an executable assertion
            (`assert`, `raise`, or a non-zero exit) -- a figure that is redrawn but never
            checked against its banked JSON is rebuilt, not self-checked.

Exit status is 0 when CITED is a subset of REBUILT and 1 otherwise, so the script can be
wired into a gate. The enumeration is printed either way: a NO with the list is the useful
output, and it is the answer this unit was commissioned to produce.

Scope note. This measures REGISTRATION COVERAGE. It does not run the figure scripts and so
says nothing about whether they succeed; `build_figures.py` itself is the thing that does
that, and it is not invoked here (running it costs a full matplotlib rebuild of ~50 scripts).

Citation forms. The record writes a figure four ways -- `fig19`, `fig 19`, `figs 1-5` and
`fig14/15`. All four are matched, and a range is expanded end to end; that is the only place
this script infers anything, and it errs towards a LARGER cited set, which makes a YES harder
to fake.
"""

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITEUP = ROOT / "writeup"
BUILD = WRITEUP / "build_figures.py"

# `fig19`, `fig 19`, `figs 1-5`, `figs 1--5`, `fig14/15`
FIG_RANGE = re.compile(r"\bfigs?\s*(\d+)\s*(?:[-–—]{1,2}|/)\s*(\d+)\b")
FIG_TOKEN = re.compile(r"\bfigs?\s*(\d+)\b")
FIG_PNG = re.compile(r"fig(\d+)[A-Za-z0-9_]*\.png")
ASSERTION = re.compile(r"^\s*(assert\b|raise\b)|sys\.exit\(\s*[1-9]|SystemExit\(\s*[1-9]")


def p2_evidence_entries():
    """Parse P2_EVIDENCE out of build_figures.py with `ast` -- no import, no grep.

    Returns (paths, raw_entries). A comment mentioning a figure is invisible here by
    construction, which is the point: that is exactly how fig107 hid.
    """
    tree = ast.parse(BUILD.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "P2_EVIDENCE":
                    entries = ast.literal_eval(node.value)
                    paths = []
                    for e in entries:
                        paths.append(e if isinstance(e, str) else e[0])
                    return paths, entries
    raise SystemExit("FATAL: no P2_EVIDENCE assignment found in build_figures.py")


def record_markdown():
    files = sorted(WRITEUP.rglob("*.md"))
    files += sorted(ROOT.glob("*.md"))
    return files


def main():
    paths, entries = p2_evidence_entries()

    # --- REBUILT: what build_figures.py actually executes -------------------------------
    executed = {"writeup/build_figures.py": BUILD}
    missing_scripts = []
    for rel in paths:
        script = (WRITEUP / rel).resolve()
        key = str(script.relative_to(ROOT)) if str(script).startswith(str(ROOT)) else str(script)
        if not script.exists():
            missing_scripts.append(rel)
            continue
        executed[key] = script

    rebuilt = {}      # fig id -> sorted list of scripts that emit it
    selfchecked = {}  # fig id -> sorted list of scripts that emit it AND assert
    for key, script in sorted(executed.items()):
        src = script.read_text()
        ids = {int(m) for m in FIG_PNG.findall(src)}
        if not ids:
            continue
        asserts = any(ASSERTION.search(line) for line in src.splitlines())
        for i in ids:
            rebuilt.setdefault(i, []).append(key)
            if asserts:
                selfchecked.setdefault(i, []).append(key)

    # --- CITED: what the record tells a reader exists ----------------------------------
    cited = {}  # fig id -> set of md files citing it
    for md in record_markdown():
        try:
            text = md.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        ids = {int(m) for m in FIG_TOKEN.findall(text)}
        for lo, hi in FIG_RANGE.findall(text):
            lo, hi = int(lo), int(hi)
            if 0 < hi - lo < 40:
                ids |= set(range(lo, hi + 1))
        for i in ids:
            cited.setdefault(i, set()).add(str(md.relative_to(ROOT)))

    cited_ids = set(cited)
    rebuilt_ids = set(rebuilt)
    selfchecked_ids = set(selfchecked)
    pngs = {int(m.group(1)) for f in (WRITEUP / "figures").glob("*.png")
            for m in [FIG_PNG.match(f.name)] if m}

    gap_rebuild = sorted(cited_ids - rebuilt_ids)
    gap_selfcheck = sorted(cited_ids - selfchecked_ids)
    orphan = sorted(rebuilt_ids - cited_ids)

    # A cited id splits three ways, and the three mean different things.
    landed_gap = [i for i in gap_rebuild if i in pngs]        # figure EXISTS, nothing rebuilds it
    phantom_gap = [i for i in gap_rebuild if i not in pngs]   # number cited, no figure on disk

    def fmt(ids):
        return "[" + ", ".join(str(i) for i in ids) + "]"

    print("=" * 78)
    print("DOES build_figures.py SELF-CHECK EVERY FIGURE THE RECORD CITES?")
    print("=" * 78)
    print(f"P2_EVIDENCE entries registered  : {len(entries)}")
    print(f"  registered but file missing   : {len(missing_scripts)} {missing_scripts}")
    print(f"figure ids CITED in the record  : {len(cited_ids)}")
    print(f"figure ids REBUILT              : {len(rebuilt_ids)}  {fmt(sorted(rebuilt_ids))}")
    print(f"figure ids SELF-CHECKED         : {len(selfchecked_ids)}  {fmt(sorted(selfchecked_ids))}")
    print(f".png files in writeup/figures   : {len(pngs)}")
    print()
    print(f"[A] CITED, .png EXISTS, NOT REBUILT  ({len(landed_gap)}): {fmt(landed_gap)}")
    print("    -- a figure the record shows a reader, that build_figures.py cannot reproduce")
    print(f"[B] CITED, NO .png, NOT REBUILT      ({len(phantom_gap)}): {fmt(phantom_gap)}")
    print("    -- reserved/allocated/parked numbers; no artefact exists to rebuild")
    print(f"[C] REBUILT but never cited          ({len(orphan)}): {fmt(orphan)}")
    print(f"[D] REBUILT without any assertion    ({len(sorted(rebuilt_ids - selfchecked_ids))}): "
          f"{fmt(sorted(rebuilt_ids - selfchecked_ids))}")
    print()
    print("[A] in detail -- where each is cited:")
    for i in landed_gap:
        src = sorted(cited[i])
        print(f"    fig{i:<4} {len(src)} file(s): {', '.join(src[:3])}"
              + (" ..." if len(src) > 3 else ""))
    print()

    ok_rebuild = not gap_rebuild
    ok_selfcheck = not gap_selfcheck
    print(f"ANSWER, rebuild coverage    (CITED subset of REBUILT)     : "
          f"{'YES' if ok_rebuild else 'NO'}  ({len(gap_rebuild)} uncovered)")
    print(f"ANSWER, self-check coverage (CITED subset of SELF-CHECKED): "
          f"{'YES' if ok_selfcheck else 'NO'}  ({len(gap_selfcheck)} uncovered)")
    print("=" * 78)
    return 0 if (ok_rebuild and ok_selfcheck) else 1


if __name__ == "__main__":
    sys.exit(main())
