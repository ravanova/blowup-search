#!/usr/bin/env python3
"""Script-injects verbatim quotations into a draft.

Rationale (leg 411 unit PB1, finding F8; re-confirmed at leg 414): the tool-output
channel silently drops words from long outputs, so a quotation retyped off screen can
contain a sentence the source does not have.  No quotation in the draft is typed by
hand: each is extracted here from the fetched source by start/end marker and written
straight into the file.
"""
import json, re, sys, pathlib

SRC = pathlib.Path(sys.argv[1])          # directory of fetched source text
REPO = pathlib.Path(sys.argv[2])         # repo root
TARGETS = [pathlib.Path(p) for p in sys.argv[3:]]

def span(fname, start, end, squash=True):
    t = (SRC / fname).read_text(encoding="utf-8", errors="replace")
    if squash:
        t = re.sub(r"\s+", " ", t)
    i = t.index(start)
    j = t.index(end, i) + len(end)
    return t[i:j]

QUOTES = {
 "Q_ROODMAN_DEF":  ("roodman_plain.txt", "A blind analysis is a measurement", "particular direction."),
 "Q_ROODMAN_KTEV": ("roodman_plain.txt", "The use of the", "as changes were made."),
 "Q_NOSEK_POST":   ("nosek_prereg.txt", "This distinction between postdiction", "credibility of research findings."),
 "Q_NOSEK_PREREG": ("nosek_prereg.txt", "Preregistration distinguishes analyses", "result from postdictions."),
 "Q_NOSEK_DEV":    ("nosek_prereg.txt", "Deviations from data collection", "most predictable investigations."),
 "Q_COMPARE_NUM":  ("compare_goldacre.txt", "on pre-specified primary outcomes (mean 76%", "range 2.9–8.3)"),
 "Q_COMPARE_N":    ("compare_goldacre.txt", "We assessed 67 trials in total", "(range 3–24)."),
 "Q_NASA_COINC":   ("ntrs_a.txt", "For the twenty", "assumption of independence."),
 "Q_NASA_INDEP":   ("ntrs_a.txt", "the present study suggests", "using a single version."),
 "Q_FLYSPECK":     ("flyspeck_plain.txt", "In the end, the proof was published", "from the referees."),
 "Q_FLYSPECK_REF": ("flyspeck_plain.txt", "The delay in publication was caused", "complex computer proof."),
 "Q_SANDVE_R1":    ("sandve_tenrules.txt", "Rule 1: For Every Result", "How It Was Produced"),
 "Q_SANDVE_R5":    ("sandve_tenrules.txt", "Rule 5: Record All Intermediate Results", "Standardized Formats"),
 "Q_PLOS_AC":      ("plos_advcollab.txt", "we established an", "Integrated Information Theory."),
 "Q_PLOS_LABS":    ("plos_advcollab.txt", "Six theory-impartial laboratories", "specified here"),
 "Q_NIST_AC5":     ("nist.txt", "Separation of duties addresses", "without collusion."),
 "Q_IEEE1012":     ("ieee1012.txt", "Verification and validation (V&V) processes", "intended use and user needs."),
}

def repo_quotes():
    out = {}
    d = json.loads((REPO / "writeup/data/p2_route_l6_profile_v1.json").read_text())
    out["Q_L6_CAPWHY"] = d["gate"]["B"]["stability_against_the_iteration_cap"]["why"]
    orch = re.sub(r"\s+", " ", (REPO / "ORCHESTRATION.md").read_text())
    i = orch.index("plus an `*_evidence.py` script")
    j = orch.index("without re-running anything", i) + len("without re-running anything")
    out["Q_ORCH63"] = orch[i:j]
    return out

def build():
    q = {}
    for k, (f, a, b) in QUOTES.items():
        try:
            q[k] = span(f, a, b)
        except (ValueError, FileNotFoundError) as e:
            q[k] = "EXTRACTION FAILED (%s: %s)" % (k, e)
    q.update(repo_quotes())
    return q

def main():
    q = build()
    miss = set()
    for t in TARGETS:
        s = t.read_text(encoding="utf-8")
        for k, v in q.items():
            s = s.replace("{{%s}}" % k, v)
        for m in re.findall(r"\{\{([A-Z0-9_]+)\}\}", s):
            miss.add(m)
        t.write_text(s, encoding="utf-8")
    print("injected %d quotations into %d file(s)" % (len(q), len(TARGETS)))
    for k, v in sorted(q.items()):
        print("  %-16s %3d chars %s" % (k, len(v), "FAILED" if v.startswith("EXTRACTION FAILED") else "ok"))
    if miss:
        print("UNRESOLVED TOKENS:", sorted(miss)); sys.exit(1)

main()
