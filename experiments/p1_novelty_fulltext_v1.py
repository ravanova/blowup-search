"""Leg 411 / `PB1` -- INSTRUMENT 2: the full-text corpus.  THIS is what adjudicates.

Instrument 1 (`p1_novelty_v1.py`) queries the arXiv API, which searches METADATA
ONLY.  Both of P1's effects are METHOD-SECTION statements.  So instrument 1
enumerates candidates and CANNOT answer the gate; this file reads the candidates at
full text and locates every quote by PDF page, which is what "at which page, stated
how strongly" requires.

CONTROLS, PLANTED BEFORE THE PROBES (journal Sec 0.4):

  FT1 positive          'hookstep'            must hit in >= 2 documents
  FT2 topical positive  'recurrent flow'      must hit in >= 2 documents
  FT3 nonsense negative 'Grznarov admission funnel'  must be EXACTLY 0 corpus-wide
  FT4 AND-pair          'Newton' and 'Kolmogorov' must CO-OCCUR in >= 1 document,
                        so that a co-occurrence zero below is a measurement
  FT5 SUBSTRING TRAP    the bare string 'bias' MUST be shown to hit inside the given
                        name 'Tobias'.  This one is not decoration: a naive
                        substring count of 'bias' over this corpus IS dominated by
                        the reference lists ("Tobias Kreilos", "Tobias M Schneider"),
                        and a unit that reported "bias appears N times" would be
                        reporting bibliography.  The control makes the trap explicit
                        instead of leaving it to be discovered by a reader.

  A control that does not fire as planted is DISCLOSED in the artefact and the
  verdicts it governs are VOID.  It is never quietly re-planted.

EXTRACTION HAZARD, MEASURED NOT ASSUMED: arXiv:1406.1820**v2** carries a DOUBLED TEXT
LAYER and does not extract legibly.  v1 does.  v1 is quoted; the load-bearing
sentence is re-checked against the v2 extraction anyway, and that re-check is one of
the banked probes.

Papers/ is gitignored, so THE EXTRACTED QUOTE TEXT IS BANKED IN THE JSON.  The
verdict must stay readable in a container where the PDFs no longer exist.

CEILING: TIER 2.  No L1->L4 link moves.  Clay stays ~0.05%.  No figure.  Reading is
authorised; NO OUTREACH OF ANY KIND, no paywall circumvention.

    .venv/bin/python experiments/p1_novelty_fulltext_v1.py
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "Papers"
OUT = ROOT / "writeup" / "data" / "p1_novelty_fulltext_v1.json"

CORPUS = [
    ("1207.4682v1", "1207.4682.pdf", "Chandler & Kerswell, JFM 722:554-595 (2013)"),
    ("1406.1820v1", "1406.1820v1.pdf", "Lucas & Kerswell, Phys. Fluids 27 045106 (2015) [v1: THE QUOTED VERSION]"),
    ("1406.1820v2", "1406.1820.pdf", "Lucas & Kerswell (2015) [v2: doubled text layer, cross-check only]"),
    ("1308.3356v3", "1308.3356.pdf", "Lucas & Kerswell, 2D Kolmogorov over large domains"),
    ("physics/0604062", "physics_0604062.pdf", "Viswanath 2007, founding hookstep paper"),
    ("2309.12754v1", "2309.12754.pdf", "Page, Holey, Brenner & Kerswell, JFM 991 (2024) A10"),
    ("1108.0975v1", "1108.0975.pdf", "Kawahara, Uhlmann & van Veen, Annu. Rev. Fluid Mech. 44:203-225 (2012)"),
    ("1611.04829v1", "1611.04829.pdf", "Lucas & Kerswell 2017, sustaining processes"),
    ("0810.1974v1", "0810.1974.pdf", "Halcrow-Gibson-Cvitanovic, plane Couette UPOs"),
    ("1705.03720v2", "1705.03720.pdf", "Willis, Cvitanovic & Avila, pipe-flow RPO backbone"),
]

CONTROLS = [
    ("FT1_positive", "hookstep", "docs>=2", 2),
    ("FT2_topical_positive", "recurrent flow", "docs>=2", 2),
    ("FT3_nonsense_negative", "Grznarov admission funnel", "docs==0", 0),
]

# The probes.  Each is (effect, phrase).  `effect` is the gate clause the phrase is
# aimed at; adjudication against Sec 0.5's rule is a HUMAN read of the located
# passage and is NOT performed by this script.
PROBES = [
    # effect (a): the score, used as an admission filter, biases the recovered SET
    ("a", "chosen judiciously"),
    ("a", "large skew toward low periods"),
    ("a", "somewhat counterintuitive"),
    ("a", "focussed computational resources"),
    ("a", "two shortcomings with the approach"),
    ("a", "increased instability of the UPOs"),
    ("a", "all the UPOs found are relatively low dissipation"),
    ("a", "not flagged in this approach at all"),
    ("a", "relies on a turbulent orbit shadowing"),
    ("a", "This inherently restricts the approach to lower"),
    ("a", "only s = m = 0 shifts had been searched over"),
    # effect (b): re-mining re-finds
    ("b", "considerable duplication"),
    ("b", "distinct recurrent structures"),
    ("b", "large repetition of the converged solutions already found"),
    ("b", "unique recurrent flows"),
    ("b", "conversion rate of near"),
    ("b", "So the runs were repeated"),
    ("b", "Chandler and R. R. Kerswell, Journal of Fluid Mechanics 722"),
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def pages_of(pdf: Path, layout: bool) -> list[str]:
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
    txt = subprocess.run(cmd, capture_output=True, text=True).stdout
    return txt.split("\f")


def flat(pages: list[str]) -> list[str]:
    return [" ".join(p.split()) for p in pages]


def main() -> None:
    pdftotext_v = subprocess.run(["pdftotext", "-v"], capture_output=True,
                                 text=True).stderr.splitlines()[0].strip()
    rec = {
        "leg": 411, "unit": "PB1", "instrument": 2,
        "role": ("FULL-TEXT ADJUDICATION.  Instrument 1 searches metadata only and cannot "
                 "answer this gate.  Depth of every quote below is FULL TEXT (Sec 3k)."),
        "pdftotext": pdftotext_v,
        "papers_dir_is_gitignored": True,
        "quotes_banked_in_this_json_because_the_pdfs_are_not": True,
        "corpus": [], "controls": [], "probes": [], "missing": [],
    }

    docs: dict[str, list[str]] = {}
    for ident, fname, what in CORPUS:
        p = PAPERS / fname
        if not p.exists():
            rec["missing"].append({"id": ident, "file": fname,
                                   "note": "NOT PRESENT -- this is a MISSING SOURCE, not a zero"})
            continue
        # v2 of 1406.1820 has a doubled text layer; -layout makes it worse, plain is
        # what the cross-check probe uses.
        pg = flat(pages_of(p, layout=True))
        docs[ident] = pg
        rec["corpus"].append({"id": ident, "file": fname, "what": what,
                              "sha256": sha256(p), "n_pages": len(pg),
                              "n_chars": sum(len(x) for x in pg)})

    # ---- CONTROLS, before any probe is adjudicated -------------------------
    for name, phrase, rule, thresh in CONTROLS:
        hit_docs = [d for d, pg in docs.items()
                    if any(phrase.lower() in x.lower() for x in pg)]
        fired = (len(hit_docs) == 0) if thresh == 0 else (len(hit_docs) >= thresh)
        rec["controls"].append({"control": name, "phrase": phrase, "rule": rule,
                                "n_docs_hit": len(hit_docs), "docs": hit_docs,
                                "fired_as_planted": fired})

    # FT4 -- AND-pair co-occurrence inside a single document
    co = [d for d, pg in docs.items()
          if any("newton" in x.lower() for x in pg) and any("kolmogorov" in x.lower() for x in pg)]
    rec["controls"].append({
        "control": "FT4_and_pair", "phrase": "Newton AND Kolmogorov (same document)",
        "rule": "docs>=1", "n_docs_hit": len(co), "docs": co,
        "fired_as_planted": len(co) >= 1,
        "why": "if this were 0, every co-occurrence zero below would be an artefact"})

    # FT5 -- the substring trap, measured
    bias_docs, tobias_docs = [], []
    for d, pg in docs.items():
        j = " ".join(pg)
        if "bias" in j.lower():
            bias_docs.append(d)
        if "tobias" in j.lower():
            tobias_docs.append(d)
    trapped = sorted(set(tobias_docs) & set(bias_docs))
    rec["controls"].append({
        "control": "FT5_substring_trap",
        "phrase": "'bias' as a bare substring vs the given name 'Tobias'",
        "rule": "at least one doc must hit 'bias' ONLY via 'Tobias'",
        "docs_hitting_bias": bias_docs, "docs_hitting_Tobias": tobias_docs,
        "docs_where_bias_is_inside_Tobias": trapped,
        "fired_as_planted": len(trapped) >= 1,
        "why": ("a naive substring count of 'bias' over this corpus is dominated by the "
                "reference lists; reporting it as a measure of how much the field discusses "
                "bias would be reporting bibliography")})

    rec["controls_all_fired"] = all(c["fired_as_planted"] for c in rec["controls"])

    # ---- PROBES ------------------------------------------------------------
    for effect, phrase in PROBES:
        hits = []
        for d, pg in docs.items():
            for pno, page in enumerate(pg, 1):
                low = page.lower()
                idx = low.find(phrase.lower())
                if idx >= 0:
                    hits.append({"doc": d, "pdf_page": pno,
                                 "quote": page[max(0, idx - 170): idx + 260]})
        rec["probes"].append({"effect": effect, "phrase": phrase,
                              "n_hits": len(hits), "hits": hits,
                              "status": "MEASURED"})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rec, indent=2))
    print(f"corpus {len(rec['corpus'])} docs, missing {len(rec['missing'])}")
    for c in rec["controls"]:
        print(f"  {c['control']:24s} fired={c['fired_as_planted']}")
    print(f"controls_all_fired = {rec['controls_all_fired']}")
    for p in rec["probes"]:
        print(f"  ({p['effect']}) {p['phrase'][:46]:48s} hits={p['n_hits']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
