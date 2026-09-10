"""Arc 6, wave 4 (leg 433): merge the five agents' answers — four workers (iii)–(vi) and the adversary (vii).

    .venv/bin/python experiments/arc6_wave4_merge.py

Inputs : writeup/data/arc6/wave4/agent_{3_pulses,4_iteration,5_headline,6_support,7_adversary}.json
Output : writeup/data/arc6/wave4/merged.json — the gate table of (iii)–(vi) with each number, the
         adversary's verdict row by row, and the pre-committed rule of leg_433_prereg.md §3: a gate the
         adversary FAKED is marked NOT EVIDENCE whatever the worker's gate said. Nothing else is adjudicated.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WD = ROOT / "writeup" / "data" / "arc6" / "wave4"
OUT = WD / "merged.json"
FILES = {3: "agent_3_pulses.json", 4: "agent_4_iteration.json", 5: "agent_5_headline.json", 6: "agent_6_support.json", 7: "agent_7_adversary.json"}
GATES = {3: ["P1", "P2", "P3"], 4: ["I1", "I2", "I3"], 5: ["V1", "V2", "V3"], 6: ["S1", "S2", "S3"]}


def _norm(s):
    """'NO (refinement NOT-INSTANTIATED ...)' -> 'NO'; 'NOT FAKEABLE' stays; the detail lives in gates_detail."""
    s = str(s).strip()
    head = s.split("(")[0].strip()
    up = head.upper()
    for tok in ("NOT FAKEABLE", "FAKEABLE", "NOT ATTEMPTED", "NOT-INSTANTIATED", "NOT TESTABLE", "YES", "NO"):
        if up.startswith(tok): return tok
    return head[:40]


def _answer(v):
    """A gate entry may be a string, a [answer, detail] pair, or a dict with an 'answer'/'verdict' key."""
    if isinstance(v, str): return _norm(v)
    if isinstance(v, (list, tuple)) and v: return _norm(v[0])
    if isinstance(v, dict):
        for k in ("answer", "verdict", "result", "status"):
            if k in v: return _norm(v[k])
    return str(v)[:40]


def run(write=True, verbose=True):
    A = {k: (json.loads((WD / f).read_text()) if (WD / f).exists() else None) for k, f in FILES.items()}
    out = {"schema": "arc6_wave4_merged_v1", "leg": 433, "prereg_commit": "c6aaf72", "present": [k for k, v in A.items() if v], "absent": [k for k, v in A.items() if not v],
           "workers": {}, "adversary": {}, "evidence_table": {}}
    for k in (3, 4, 5, 6):
        a = A[k]
        if not a: continue
        g = a.get("gates", {})
        out["workers"][k] = {"unit": a.get("unit"), "gates": {gid: _answer(g.get(gid, "MISSING")) for gid in GATES[k]}, "gates_detail": g,
                             "controls": a.get("controls"), "claimed": a.get("claimed"), "instantiated_vs_scaled": a.get("instantiated_vs_scaled"),
                             "could_not_determine": a.get("could_not_determine", []), "gate_answer": a.get("gate_answer"), "pages_read": a.get("pages_read"),
                             "tier2_sentence_present": "Tier 2, not a proof" in json.dumps(a)}
    adv = A[7]
    verdicts = {}
    if adv:
        x1 = (adv.get("gates") or {}).get("X1", {})
        if isinstance(x1, dict):
            verdicts = {gid: _answer(v) for gid, v in x1.items()}
        for att in adv.get("attempts", []) or []:
            gid = att.get("gate") or att.get("gate_id")
            if gid and gid not in verdicts: verdicts[gid] = _answer(att.get("verdict", "NOT ATTEMPTED"))
        out["adversary"] = {"verdicts": verdicts, "X2": (adv.get("gates") or {}).get("X2"), "attempts": adv.get("attempts"), "could_not_determine": adv.get("could_not_determine", []),
                            "tier2_sentence_present": "Tier 2, not a proof" in json.dumps(adv)}
    # the pre-committed rule (leg_433_prereg.md §3)
    for k, gids in GATES.items():
        for gid in gids:
            w = out["workers"].get(k, {}).get("gates", {}).get(gid, "ABSENT")
            v = verdicts.get(gid, "NOT ATTEMPTED")
            status = "NOT EVIDENCE (faked)" if v.upper().startswith("FAKEABLE") else ("EVIDENCE" if w == "YES" and v.upper().startswith("NOT FAKEABLE") else ("NO" if w == "NO" else f"{w} / adversary {v}"))
            out["evidence_table"][gid] = {"worker": w, "adversary": v, "status": status}
    counts = {"workers_YES": sum(1 for r in out["evidence_table"].values() if r["worker"] == "YES"), "workers_NO": sum(1 for r in out["evidence_table"].values() if r["worker"] == "NO"),
              "faked": sum(1 for r in out["evidence_table"].values() if r["status"].startswith("NOT EVIDENCE")), "evidence": sum(1 for r in out["evidence_table"].values() if r["status"] == "EVIDENCE")}
    out["counts"] = counts
    if write: OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        print("present", out["present"], "absent", out["absent"])
        for gid, r in out["evidence_table"].items(): print(f"  {gid}: worker {r['worker']:>18} | adversary {r['adversary']:>14} | {r['status']}")
        print("counts", counts)
    return out


if __name__ == "__main__":
    run()
