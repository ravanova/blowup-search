"""Arc 7, unit K3 (leg 439): merge the five agents' answers — four workers (Q1–Q6) and the blind adversary.

    .venv/bin/python experiments/arc7_k3_merge.py

Inputs : writeup/data/arc7/k3/agent_{1_pulses,2_iteration,3_force,4_support,5_adversary}.json
Output : writeup/data/arc7/k3/merged.json — the gate table Q1–Q6 with each number, the adversary's X1 row
         by row, the DROPPED gates with their reason, and every worker/adversary disagreement RECORDED,
         not adjudicated. The pre-committed rule of leg_439_prereg.md §3 and §5: a gate the adversary
         FAKED is marked NOT EVIDENCE whatever the worker's gate said. Nothing else is adjudicated here.

Q6 was DROPPED by leg_439_prereg_amend.md BEFORE any run (its route-A prediction was mis-derived); it is
carried as a pre-registered drop, not as a worker's failure to answer.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WD = ROOT / "writeup" / "data" / "arc7" / "k3"
OUT = WD / "merged.json"
FILES = {1: "agent_1_pulses.json", 2: "agent_2_iteration.json", 3: "agent_3_force.json", 4: "agent_4_support.json", 5: "agent_5_adversary.json"}
GATES = {1: ["Q1", "Q2"], 2: ["Q3"], 3: ["Q4"], 4: ["Q5", "Q6"]}
PREREG_DROPPED = {"Q6": "DROPPED by leg_439_prereg_amend.md before any run: route A's `k = 8 - 3d` was mis-derived (the -3 log d term differentiates to -3d^2, not -3d) and the true linear coefficient is unreachable at resolvable d. Slot 4 ran Q5 only."}


CONDUCTOR_NOT_EVIDENCE = {
    "Q5": "its two routes were one closed form evaluated twice -- arc6_residual_v1.py:101-103 computes "
          "calB_beyond = (2+2h)*(sh-1.0), algebra in h and the heat flag that reads no field, and route A is "
          "the same algebra; hence abs_error is EXACTLY 0.0 in all four cells. CORRECTIONS.md sec 79"
}


def _norm(s):
    """'NO (not instantiated ...)' -> 'NO'; 'NOT FAKEABLE' stays; the detail lives in gates_detail."""
    s = str(s).strip()
    head = s.split("(")[0].strip()
    up = head.upper()
    for tok in ("NOT FAKEABLE", "FAKEABLE", "NOT ATTEMPTED", "NOT-INSTANTIATED", "NOT INSTANTIATED", "UNDER-RESOURCED", "NOT TESTABLE", "DROPPED", "YES", "NO"):
        if up.startswith(tok): return tok.replace("NOT INSTANTIATED", "NOT-INSTANTIATED")
    return head[:40]


def _answer(v):
    """A gate's worker verdict. Some slots report a single word; slot 3 reports per-cell
    outcomes and slot 4 buries it under 'overall'. Composites are kept composite -- collapsing
    slot 3's three NOs and two YESes into one word would misreport it either way."""
    if isinstance(v, str):
        return _norm(v)
    if isinstance(v, dict):
        for k in ("answer", "verdict", "result", "status", "gate", "overall"):
            if k in v and isinstance(v[k], str):
                return _norm(v[k])
    return "MISSING"


def _composite(slot_art, gid):
    """Slot 3's Q4 is a table of cells, not one answer. Return the cell map verbatim."""
    if gid == "Q4":
        gs = slot_art.get("gates_summary")
        if isinstance(gs, dict) and gs:
            return dict(gs)
    return None


def _numbers(v, _depth=0):
    """Every numeric leaf under a gate entry, keyed by path — §5 owes 'the gate table with each number'."""
    out = {}
    if _depth > 4: return out
    if isinstance(v, (int, float)) and not isinstance(v, bool): return {"": v}
    if isinstance(v, dict):
        for k, sub in v.items():
            for p, n in _numbers(sub, _depth + 1).items(): out[f"{k}.{p}".rstrip(".")] = n
    elif isinstance(v, (list, tuple)):
        for i, sub in enumerate(v):
            for p, n in _numbers(sub, _depth + 1).items(): out[f"[{i}].{p}".rstrip(".")] = n
    return out


def run(write=True, verbose=True):
    A = {k: (json.loads((WD / f).read_text()) if (WD / f).exists() else None) for k, f in FILES.items()}
    out = {"schema": "arc7_k3_merged_v1", "leg": 439, "prereg": "experiments/journal/leg_439_prereg.md", "amendment": "experiments/journal/leg_439_prereg_amend.md",
           "present": [k for k, v in A.items() if v], "absent": [k for k, v in A.items() if not v],
           "workers": {}, "adversary": {}, "gate_table": {}, "dropped": dict(PREREG_DROPPED), "disagreements": []}
    for k in (1, 2, 3, 4):
        a = A[k]
        if not a: continue
        g = a.get("gates", {}) or {}
        out["workers"][k] = {"agent": a.get("agent"), "gates": {gid: _answer(g.get(gid, "MISSING")) for gid in GATES[k]},
                             "numbers": {gid: _numbers(g.get(gid)) for gid in GATES[k] if gid in g},
                             "gates_detail": g, "claimed": a.get("claimed"), "routes": a.get("routes"), "controls": a.get("controls"),
                             "instantiated_vs_scaled": a.get("instantiated_vs_scaled"), "could_not_determine": a.get("could_not_determine", []),
                             "what_this_does_not_establish": a.get("what_this_does_not_establish"),
                             "tier2_sentence_present": "Tier 2, not a proof" in json.dumps(a, ensure_ascii=False)}
        for gid, why in (a.get("dropped") or {}).items() if isinstance(a.get("dropped"), dict) else []:
            out["dropped"].setdefault(str(gid), f"dropped by slot {k}: {why}")
        # a control that did not fire as planted is a DEFECT, surfaced here, never hidden
        # a control that did not fire as planted is a DEFECT, surfaced here, never hidden.
        # Slots report it two ways: an explicit fired=False flag, or a phrase in free text.
        def _scan(node, path, _k=k):
            if isinstance(node, dict):
                if node.get("fired") is False:
                    out["disagreements"].append({"kind": "control did not fire as planted", "slot": _k,
                                                 "control": path, "detail": node, "recorded_not_adjudicated": True})
                    return
                for kk, vv in node.items():
                    _scan(vv, f"{path}.{kk}" if path else str(kk), _k)
        _scan(a.get("controls") or {}, "")
        _blob = json.dumps({"c": a.get("controls"), "s": a.get("controls_summary")}, ensure_ascii=False).upper()
        if ("NOT FIRED" in _blob or "DID NOT FIRE" in _blob):
            out["disagreements"].append({"kind": "control did not fire as planted (reported in text)",
                                         "slot": k, "recorded_not_adjudicated": True})
    adv = A[5]
    verdicts = {}
    if adv:
        g = adv.get("gates", {}) or {}
        x1 = g.get("X1", adv.get("X1", adv.get("X1_per_gate", {})))
        if isinstance(x1, dict):
            verdicts = {gid: _answer(v) for gid, v in x1.items()}
        elif isinstance(x1, (list, tuple)):
            for row in x1:
                gid = (row or {}).get("gate") if isinstance(row, dict) else None
                if gid: verdicts[gid] = _answer(row)
        for att in adv.get("attempts", []) or []:
            gid = att.get("gate") or att.get("gate_id")
            if gid and gid not in verdicts: verdicts[gid] = _answer(att.get("verdict", "NOT ATTEMPTED"))
        out["adversary"] = {"verdicts": verdicts, "X1": x1, "X2": g.get("X2", adv.get("X2", adv.get("X2_verdict"))), "recipes": adv.get("attempts"),
                            "could_not_determine": adv.get("could_not_determine", []), "forbidden_paths_opened": adv.get("forbidden_paths_opened"),
                            "tier2_sentence_present": "Tier 2, not a proof" in json.dumps(adv, ensure_ascii=False)}
    # the pre-committed rule (leg_439_prereg.md §3, §5)
    for k, gids in GATES.items():
        for gid in gids:
            w = out["workers"].get(k, {}).get("gates", {}).get(gid, "ABSENT")
            v = verdicts.get(gid, "NOT ATTEMPTED")
            comp = _composite(A.get(k) or {}, gid)
            if comp is not None:
                yes = [c for c, r in comp.items() if r == "YES"]
                no = [c for c, r in comp.items() if r == "NO"]
                w = f"{len(no)} NO / {len(yes)} YES of {len(comp)} cells"

            faked = v.upper().startswith("FAKEABLE")
            if gid in PREREG_DROPPED:
                status = "DROPPED (pre-registered, before any run)"
            elif w.startswith("NOT-INSTANTIATED") or w.startswith("NOT INSTANTIATED"):
                status = "DROPPED by the rule (worker could not put it in two-route form)"
                if faked:
                    status += "; the gate as written is also FAKEABLE"
            elif w.startswith("UNDER-RESOURCED"):
                status = "NOT ESTABLISHED (worker did not instantiate it; not a NO)"
                if faked:
                    status += "; the gate as written is also FAKEABLE"
            elif comp is not None:
                status = f"{len(no)} cells NO"
                if yes:
                    status += (f"; the {len(yes)} YES cells are NOT EVIDENCE (adversary faked the gate)"
                               if faked else f"; {len(yes)} YES cells")
            elif faked:
                status = "NOT EVIDENCE (adversary faked it)"
            elif w == "YES" and v.upper().startswith("NOT FAKEABLE"):
                status = "EVIDENCE"
            elif w == "NO":
                status = "NO"
            else:
                status = f"{w} / adversary {v}"
            # Q5 carries a SECOND, independent disqualification found by the Conductor at integration.
            if gid in CONDUCTOR_NOT_EVIDENCE:
                status = "NOT EVIDENCE (" + CONDUCTOR_NOT_EVIDENCE[gid] + "); the adversary also faked it"
            out["gate_table"][gid] = {"slot": k, "worker": w, "adversary": v, "status": status,
                                      "numbers": out["workers"].get(k, {}).get("numbers", {}).get(gid, {})}
            if ("YES" in w) and v.upper().startswith("FAKEABLE"):
                out["disagreements"].append({"kind": "worker YES vs adversary FAKEABLE", "gate": gid, "slot": k,
                                             "recorded_not_adjudicated": True, "rule": "leg_439_prereg.md §5: marked NOT EVIDENCE"})
    st = [r["status"] for r in out["gate_table"].values()]
    counts = {
        "live_gates": sum(1 for g in st if not g.startswith("DROPPED (pre-registered")),
        "EVIDENCE": sum(1 for g in st if g == "EVIDENCE"),
        "not_evidence": sum(1 for g in st if g.startswith("NOT EVIDENCE")),
        "cells_NO_or_NO": sum(1 for g in st if "cells NO" in g or g == "NO"),
        "not_established_or_dropped_by_the_rule": sum(1 for g in st if g.startswith("NOT ESTABLISHED") or g.startswith("DROPPED by the rule")),
        "dropped_preregistered": sum(1 for g in st if g.startswith("DROPPED (pre-registered")),
        "gates_the_blind_adversary_faked": sum(1 for v in verdicts.values() if str(v).upper().startswith("FAKEABLE")),
    }
    out["counts"] = counts
    out["what_this_does_not_establish"] = "Tier 2 throughout. A two-route agreement is evidence about the manuscript's numerical claims, not a proof of its theorem, and no gate here is verified until a blind agent reproduces it."
    if write:
        WD.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        print("present", out["present"], "absent", out["absent"])
        for gid, r in out["gate_table"].items(): print(f"  {gid}: worker {r['worker']:>16} | adversary {r['adversary']:>14} | {r['status']}")
        for gid, why in out["dropped"].items(): print(f"  DROPPED {gid}: {why[:100]}")
        for d in out["disagreements"]: print(f"  DISAGREEMENT: {d}")
        print("counts", counts)
    return out


if __name__ == "__main__":
    run()
