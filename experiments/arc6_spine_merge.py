"""Arc 6, R4 fan-out (leg 429): merge the four spine agents and the blind verifier.

    .venv/bin/python experiments/arc6_spine_merge.py

Inputs : writeup/data/arc6/spine/agent_{1..4}.json, agent_5_verifier.json (one file, one author)
Output : writeup/data/arc6/spine/merged.json

Per node: the assigned agent's verdict (CHECKED / GAP / NOT-CHECKED); for the ten
sampled nodes, the verifier's verdict beside it; agreement = both verdicts equal.
A node is VERIFIED only if its agent said CHECKED and the verifier, blind, also
said CHECKED. Everything else stays UNVERIFIED. GAPs and escalation candidates
are listed verbatim; nothing is adjudicated here.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SP = ROOT / "writeup" / "data" / "arc6" / "spine"
OUT = SP / "merged.json"


def run(write=True, verbose=True):
    agents = {}
    for k in (1, 2, 3, 4):
        p = SP / f"agent_{k}.json"
        if p.exists():
            agents[k] = json.loads(p.read_text())
    ver = json.loads((SP / "agent_5_verifier.json").read_text()) if (SP / "agent_5_verifier.json").exists() else None
    spine = json.loads((ROOT / "writeup" / "data" / "arc6" / "dag.json").read_text())["r4_spine"]
    nodes = {}
    for k, a in agents.items():
        for n in a["nodes"]:
            nodes[n["id"]] = {"agent": k, "verdict": n["verdict"], "gap": n.get("gap"), "not_checked_reason": n.get("not_checked_reason"),
                              "n_recomputed": len(n.get("recomputed", [])), "n_steps": len(n.get("steps_checked", [])),
                              "existence_source": n.get("existence_source"), "notes": n.get("notes", "")}
    vnodes = {n["id"]: n for n in ver["nodes"]} if ver else {}
    for sid, v in vnodes.items():
        nodes.setdefault(sid, {"agent": None, "verdict": None})
        nodes[sid]["verifier_verdict"] = v["verdict"]
        nodes[sid]["verifier_gap"] = v.get("gap")
        nodes[sid]["verifier_attack"] = v.get("attack", "")
        nodes[sid]["verifier_n_recomputed"] = len(v.get("recomputed", []))
        nodes[sid]["verifier_existence_source"] = v.get("existence_source")
    for sid, n in nodes.items():
        vv = n.get("verifier_verdict")
        n["status"] = "VERIFIED" if (n.get("verdict") == "CHECKED" and vv == "CHECKED") else "UNVERIFIED"
        n["agree"] = (n.get("verdict") == vv) if vv is not None else None
    counts = {v: sum(1 for n in nodes.values() if n.get("verdict") == v) for v in ("CHECKED", "GAP", "NOT-CHECKED")}
    sampled = [s for s, n in nodes.items() if n.get("verifier_verdict") is not None]
    agree = [s for s in sampled if nodes[s]["agree"]]
    missing = [s for s in spine if s not in nodes or nodes[s].get("verdict") is None]
    gaps = {s: n["gap"] for s, n in nodes.items() if n.get("verdict") == "GAP"}
    vgaps = {s: n["verifier_gap"] for s, n in nodes.items() if n.get("verifier_verdict") == "GAP"}
    esc = {f"agent_{k}": a.get("escalation_candidates", []) for k, a in agents.items()}
    if ver:
        esc["verifier"] = ver.get("escalation_candidates", [])
    artefacts = {f"agent_{k}": a.get("extraction_artefacts_found", []) for k, a in agents.items()}
    if ver:
        artefacts["verifier"] = ver.get("extraction_artefacts_found", [])
    out = {
        "schema": "arc6_spine_merged_v1", "leg": 429, "agents_present": sorted(agents), "verifier_present": ver is not None,
        "spine_size": len(spine), "nodes_with_verdict": len(spine) - len(missing), "missing": missing,
        "counts": counts, "verifier_counts": {v: sum(1 for n in ver["nodes"] if n["verdict"] == v) for v in ("CHECKED", "GAP", "NOT-CHECKED")} if ver else None,
        "sampled": sampled, "agreement": {"n": len(sampled), "agree": len(agree), "rate": (len(agree) / len(sampled)) if sampled else None,
                                          "disagreements": [{"id": s, "agent": nodes[s].get("verdict"), "verifier": nodes[s]["verifier_verdict"]} for s in sampled if not nodes[s]["agree"]]},
        "verified": sorted(s for s, n in nodes.items() if n["status"] == "VERIFIED"),
        "gaps": gaps, "verifier_gaps": vgaps, "escalation_candidates": esc,
        "existence_source": {s: {"agent": n.get("existence_source"), "verifier": n.get("verifier_existence_source")} for s, n in nodes.items() if n.get("existence_source") or n.get("verifier_existence_source")},
        "extraction_artefacts": artefacts,
        "nodes": nodes,
    }
    if write:
        OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        print(f"agents {sorted(agents)} verifier {ver is not None}; verdicts {counts}; missing {missing}")
        print(f"verifier {out['verifier_counts']}; agreement {out['agreement']['agree']}/{out['agreement']['n']} = {out['agreement']['rate']}; disagreements {out['agreement']['disagreements']}")
        print(f"VERIFIED ({len(out['verified'])}): {out['verified']}")
        print("GAPS:", {k: (v or {}).get("quoted_step", "")[:100] for k, v in gaps.items()})
        print("verifier GAPS:", {k: (v or {}).get("quoted_step", "")[:100] for k, v in vgaps.items()})
        print("escalation candidates:", esc)
        print("existence_source:", out["existence_source"])
    return out


if __name__ == "__main__":
    run()
