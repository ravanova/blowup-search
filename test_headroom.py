#!/usr/bin/env python3
"""§3j HEADROOM — the caps, checked mechanically, at every merge gate.

WHY THIS EXISTS, and it is not a general tidiness test.  `ORCHESTRATION.md` §3j
caps four files in BYTES and caps `STATE.md`'s rows in CHARACTERS.  Until
2026-08-19 nothing enforced them: the Conductor measured them by hand at wave
boundaries, and a unit writing to a capped file between boundaries could put it
over with nothing objecting.  That is not hypothetical.  Unit `PB2` (leg 410)
added 25 lines to `WALLS.md` and landed it through a `MERGE GATE: PASS` with the
file **2,151 bytes over its cap** (`writeup/CORRECTIONS.md` §48).  The brief did
not carry §3j, the gate did not check it, and the discipline that was supposed
to hold the cap was a human reading `wc -c` at a boundary that had not arrived.

This is a PROSPECTIVE check.  It fails the merge gate rather than recording a
retraction afterwards.

Run:  .venv/bin/python test_headroom.py
Exit: 0 iff every cap holds.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# §3j, verbatim.  Bytes, not characters, not lines.
CAPS = {
    "STATE.md": 24576,
    "WALLS.md": 32768,
    "OPTIONS.md": 24576,
}

# §3j's fourth cap is not a file: it is the LIVE block of reports/ORCH_STATE.md,
# delimited by its own heading and the next top-level heading.
ORCH = "reports/ORCH_STATE.md"
ORCH_LIVE_CAP = 8192

# §3j: "NO ROW OVER 600 CHARACTERS" in STATE.md.  Characters, not bytes — the
# file is full of `‖`, `∇`, `³` and em dashes, and conflating the two is the
# same substitution this repository has recorded six times (§45's table).
STATE_ROW_CHARS = 600


def orch_live_block(text):
    """The LIVE block: from its heading to the next line starting '## '."""
    i = text.find("## LIVE")
    if i < 0:
        return None
    j = text.find("\n## ", i + 4)
    return text[i:] if j < 0 else text[i:j]


def main():
    fails = []
    rows = []

    for name, cap in sorted(CAPS.items()):
        p = ROOT / name
        if not p.exists():
            fails.append("%s is MISSING and is a capped file" % name)
            continue
        n = len(p.read_bytes())
        rows.append((name, n, cap))
        if n > cap:
            fails.append("%s is %d bytes OVER its §3j cap (%d > %d)"
                         % (name, n - cap, n, cap))

    p = ROOT / ORCH
    if not p.exists():
        fails.append("%s is MISSING" % ORCH)
    else:
        text = p.read_text()
        live = orch_live_block(text)
        if live is None:
            fails.append("%s has no '## LIVE' heading — the §3j block cannot be "
                         "located, so the cap is UNCHECKED, which is a fail and "
                         "not a pass" % ORCH)
        else:
            n = len(live.encode())
            rows.append((ORCH + " LIVE", n, ORCH_LIVE_CAP))
            if n > ORCH_LIVE_CAP:
                fails.append("%s LIVE block is %d bytes OVER its §3j cap "
                             "(%d > %d)" % (ORCH, n - ORCH_LIVE_CAP, n,
                                            ORCH_LIVE_CAP))

    p = ROOT / "STATE.md"
    worst = 0
    if p.exists():
        for k, line in enumerate(p.read_text().split("\n"), start=1):
            worst = max(worst, len(line))
            if len(line) > STATE_ROW_CHARS:
                fails.append("STATE.md:%d is %d characters, over the §3j row cap "
                             "of %d" % (k, len(line), STATE_ROW_CHARS))

    for name, n, cap in rows:
        print("  %-28s %7d / %7d   %+d" % (name, n, cap, cap - n))
    print("  %-28s %7d / %7d   %+d"
          % ("STATE.md longest row (chars)", worst, STATE_ROW_CHARS,
             STATE_ROW_CHARS - worst))

    if fails:
        print("\n§3j HEADROOM: FAIL")
        for f in fails:
            print("  - " + f)
        print("\nRemedy, in §3j's own order of preference: RETIRE a block "
              "VERBATIM to WALLS_HISTORY.md or to a '## Superseded' section, "
              "and leave a pointer. Compaction is the second choice. Deleting "
              "the text is not a remedy.")
        return 1

    print("\n§3j HEADROOM: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
