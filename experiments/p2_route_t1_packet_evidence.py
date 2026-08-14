"""T1 / leg 391 — MISSING-RECORD REPAIR, made executable.

Banked by V-W2 (branch `verify/wave2`) to discharge an obligation the wave-1 verifier
raised on 2026-08-13: **leg 391 / unit `T1` banked no machine record at all**, so its gate
answer could only ever be checked against prose.

This script checks `writeup/data/p2_route_t1_packet_v1.json` against the escalation
document it claims to describe,
`writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md`.

**Lesson 68: gate this by the EXIT CODE, never by reading a printed line.**
Exit 0 = every check passed. Exit 1 = at least one FAILED.

WHAT THIS DOES NOT DO
    It states what the packet ASKED and that it RULED NONE of the three ban-wording
    questions. It is not evidence for or against `T1`'s gate answer and does not re-open
    it. There is no gate verdict anywhere in the banked record, and this script asserts
    that too.

    .venv/bin/python experiments/p2_route_t1_packet_evidence.py
"""

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(ROOT, "writeup", "data", "p2_route_t1_packet_v1.json")
SRC_REL = os.path.join("writeup", "escalations", "ESCALATION_BAN_WORDING_2026-08-13.md")

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-78s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(REC, encoding="utf-8") as fh:
        rec = json.load(fh)

    src_rel = rec["source_document"]["path"]
    src = os.path.join(ROOT, src_rel)
    check("the escalation document the record names actually exists", os.path.exists(src),
          src_rel)
    if not os.path.exists(src):
        raise SystemExit("source document missing -- nothing can be verified")

    raw = open(src, "rb").read()
    text = raw.decode("utf-8")

    # ---- 1. provenance --------------------------------------------------------
    check("record points at the 2026-08-13 ban-wording escalation",
          os.path.normpath(src_rel) == os.path.normpath(SRC_REL), src_rel)
    check("source document sha256 matches the banked digest",
          hashlib.sha256(raw).hexdigest() == rec["source_document"]["sha256"],
          rec["source_document"]["sha256"][:16])
    check("source document line count matches",
          len(text.splitlines()) == rec["source_document"]["lines"],
          "%d lines" % len(text.splitlines()))
    check("the document itself names leg 391 / unit T1 as the raiser",
          rec["source_document"]["raised_by_line_verbatim"] in text)
    check("the record is banked FOR leg 391, unit T1",
          rec["banks_for"]["leg"] == 391 and rec["banks_for"]["unit"] == "T1")

    # ---- 2. THE THREE QUESTIONS, verbatim -------------------------------------
    qs = rec["three_questions"]
    check("exactly THREE ban-wording questions are banked", len(qs) == 3, "n=%d" % len(qs))
    check("their ids are (a), (b), (c)", [q["id"] for q in qs] == ["a", "b", "c"],
          str([q["id"] for q in qs]))
    for q in qs:
        check("question (%s) occurs VERBATIM in the escalation document" % q["id"],
              q["question_verbatim"] in text, q["question_verbatim"][:58] + "...")
        check("question (%s): its 'pending since' occurs verbatim" % q["id"],
              q["pending_since_verbatim"] in text, q["pending_since_verbatim"])
        check("question (%s): what it blocks occurs verbatim" % q["id"],
              q["blocks_verbatim"] in text, q["blocks_verbatim"][:48] + "...")
    # the fourth item is banked as NOT one of the three
    d = rec["fourth_item_not_a_ban_wording_question"]
    check("the fourth item (d) is banked verbatim and separately from the three",
          d["id"] == "d" and d["question_verbatim"] in text)
    check("the fourth item's own text says it is NOT a ban-wording question",
          "Not a ban-wording question" in d["question_verbatim"])

    # ---- 3. IT RULED NONE OF THEM ---------------------------------------------
    r = rec["ruling"]
    check("banked count of questions RULED is zero", r["questions_ruled"] == 0,
          "ruled=%d of %d asked" % (r["questions_ruled"], r["questions_asked"]))
    check("banked count of questions ASKED is three", r["questions_asked"] == 3)
    check("'This packet rules nothing.' occurs VERBATIM in the document",
          r["packet_rules_nothing_verbatim"] in text)
    check("'It ruled none of (a), (b), (c).' occurs VERBATIM in the document",
          r["ruled_none_verbatim"] in text)
    # independent of the banked strings: the document must not endorse a reading.
    # Each question offers exactly two lettered readings; a ruling would name a winner.
    # "rules nothing" / "ruled none" are REFUSALS to rule, not endorsements, so they are
    # excluded by an explicit lookahead rather than by post-filtering a truncated match.
    endorse = re.findall(
        r"(?i)\b(?:we|this packet|the packet)\s+(?:hereby\s+)?"
        r"(?:rule|rules|ruled|adopt|adopts|endorse|endorses|prefer|prefers|select|selects)"
        r"\b(?!\s+(?:nothing|none|no\b))\s+\S+",
        text)
    check("no endorsement verb attaches to the packet anywhere in the document",
          not endorse, str(endorse))
    check("the document states it ruled none, in its 'what this packet did not do' list",
          "It ruled none of" in text)

    # ---- 4. SCOPE LIMIT (reading (f)): this record re-opens nothing ------------
    check("record is explicitly marked as NOT re-opening T1's gate answer",
          rec["does_not_reopen_t1_gate_answer"] is True)
    check("record carries no gate verdict of its own",
          rec["carries_no_gate_verdict"] is True
          and not any(k in rec for k in ("gate_answer", "verdict", "verdict_rule_fired")))
    blob = json.dumps(rec, ensure_ascii=False).lower()
    for banned in ("gate answer:", "we rule", "therefore the ban"):
        check("record contains no ruling language (%r)" % banned, banned not in blob)

    # ---- 5. the ceiling the document states for itself -------------------------
    check("the Tier-2 / Clay ~0.05% ceiling sentence is quoted verbatim from the source",
          rec["ceiling_verbatim_from_source"] in text,
          rec["ceiling_verbatim_from_source"])

    n_fail = sum(1 for _, ok_, _ in CHECKS if not ok_)
    print("\n%d/%d checks OK" % (len(CHECKS) - n_fail, len(CHECKS)))
    if n_fail:
        print("%d check(s) FAILED" % n_fail, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
