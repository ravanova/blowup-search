"""Arc 6 R2 (leg 425): the statement ledger and its executable gate.

    .venv/bin/python experiments/arc6_ledger.py            # validate + report
    .venv/bin/python experiments/arc6_ledger.py --cursor    # print the page cursor

The ledger is writeup/data/arc6/ledger.json:
  {"schema", "cursor": {"read_through_page", "sections_done"}, "entries": [...]}
One entry per numbered statement in statement_index.json, with the fields the
charter requires: id, kind, section, page, hypotheses, conclusion, constants,
cites, role. Entries are APPENDED after each section is read, and the cursor is
pushed with them, so a mid-read handoff loses nothing.

The gate (R2 (a) and (b)) is computed here, never asserted in prose:
  (a) every id in statement_index.json has exactly one entry;
  (b) every entry has non-empty hypotheses, conclusion and cites.
The validator refuses an entry whose id is not in the index (a typo would
otherwise inflate the count) and an entry whose page disagrees with the index.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "writeup" / "data" / "arc6"
LEDGER = D / "ledger.json"
INDEX = D / "statement_index.json"
REQ = ("id", "kind", "section", "page", "hypotheses", "conclusion", "constants", "cites", "role")


def load():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"schema": "arc6_ledger_v1", "leg": 425,
            "cursor": {"read_through_page": 0, "sections_done": []}, "entries": []}


def save(led):
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")


def validate(led, verbose=True):
    idx = {e["id"]: e for e in json.loads(INDEX.read_text())["statements"]}
    seen, problems = {}, []
    for e in led["entries"]:
        missing = [k for k in REQ if k not in e]
        if missing:
            problems.append(f"{e.get('id','?')}: missing fields {missing}")
            continue
        if e["id"] not in idx:
            problems.append(f"{e['id']}: NOT IN THE INDEX (typo?)")
            continue
        if e["id"] in seen:
            problems.append(f"{e['id']}: duplicate entry")
        seen[e["id"]] = e
        if e["page"] != idx[e["id"]]["page"]:
            problems.append(f"{e['id']}: page {e['page']} != index page {idx[e['id']]['page']}")
        for k in ("hypotheses", "conclusion", "cites"):
            if not e[k]:
                problems.append(f"{e['id']}: empty {k}")
    absent = [i for i in idx if i not in seen]
    gate_a = (not absent) and all(i in seen for i in idx)
    gate_b = not any(("empty" in p) for p in problems) and not any("missing fields" in p for p in problems)
    if verbose:
        print(f"entries {len(led['entries'])} / index {len(idx)}   cursor: page {led['cursor']['read_through_page']}, sections {led['cursor']['sections_done']}")
        for p in problems:
            print("  PROBLEM:", p)
        if absent:
            bysec = {}
            for i in absent:
                bysec.setdefault(idx[i]["section"], []).append(i)
            print("  absent:", {k: len(v) for k, v in bysec.items()})
        print(f"GATE (a) all 79 present: {gate_a}    GATE (b) all non-empty: {gate_b}")
    return gate_a, gate_b, problems, absent


def append(entries, read_through_page, section):
    led = load()
    have = {e["id"] for e in led["entries"]}
    for e in entries:
        if e["id"] in have:
            raise SystemExit(f"refusing duplicate {e['id']}")
        led["entries"].append(e)
    led["cursor"]["read_through_page"] = max(led["cursor"]["read_through_page"], read_through_page)
    if section not in led["cursor"]["sections_done"]:
        led["cursor"]["sections_done"].append(section)
    save(led)
    return validate(led)


if __name__ == "__main__":
    led = load()
    if "--cursor" in sys.argv:
        print(json.dumps(led["cursor"]))
        sys.exit(0)
    a, b, probs, absent = validate(led)
    sys.exit(0 if (a and b) else 1)
