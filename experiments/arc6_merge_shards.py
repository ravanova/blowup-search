"""Arc 6, R2 fan-out (leg 428): merge five independent shard ledgers and
reconcile them against the solo ledger of leg 425.

    .venv/bin/python experiments/arc6_merge_shards.py

Inputs : writeup/data/arc6/ledger/shard_{A..E}.json  (one file, one author, never edited here)
         writeup/data/arc6/ledger.json                 (the solo ledger; READ, never written)
Output : writeup/data/arc6/ledger/merged.json

MERGE RULE (named). Every statement has a PRIMARY shard: the shard whose page
range holds it. Corollary B.10 (p. 157) was ledgered by C (whose range holds
p. 157) and by E (whose range holds Appendix B); E is primary because the
statement's hypotheses live in Appendix B, and C's own could_not_determine
says so. The four preamble statements were ledgered by all five shards; the
primary is D for Theorems 1.1 and 3.1 (D's pages hold their proofs) and, for
the two Definitions, the shard with non-empty cites (E; the other four left
cites empty). Every non-primary version is banked beside the primary, never
discarded.

RECONCILIATION (gate d). For every statement, the primary shard entry is
compared with the solo entry field by field: statement references and
equation labels in `cites` (Jaccard), counts of hypotheses and constants, and
conclusion length. The five preamble versions are compared with each other the
same way. Low agreement is a FLAG for the Conductor to read both texts and
classify (paper / solo read / shard read); the classification is written in
the journal, not here.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "writeup" / "data" / "arc6"
SH = D / "ledger"
OUT = SH / "merged.json"
KIND_RE = re.compile(r"\b(Theorem|Proposition|Lemma|Corollary|Definition)(s?)\b")
TOK_RE = re.compile(r"(?<![\(\w])((?:[0-9]{1,2}|[ABC])\.\d+)(?!\d)")
EQ_RE = re.compile(r"\(([0-9ABC]+\.\d+)\)")
PRIMARY_OVERRIDE = {"Corollary B.10": "E", "Theorem 1.1": "D", "Theorem 3.1": "D", "Definition 3.2": "E", "Definition 3.3": "E"}
PREAMBLE = ["Theorem 1.1", "Theorem 3.1", "Definition 3.2", "Definition 3.3"]


def statement_refs(s):
    events = []
    for m in KIND_RE.finditer(s):
        events.append((m.start(), "kind", m.group(1), bool(m.group(2))))
    for m in TOK_RE.finditer(s):
        events.append((m.start(), "tok", m.group(1), None))
    events.sort()
    out, kind, plural, taken = set(), None, False, 0
    for _, typ, val, pl in events:
        if typ == "kind":
            kind, plural, taken = val, pl, 0
        elif kind is not None and (plural or taken == 0):
            out.add(f"{kind} {val}")
            taken += 1
    return out


RANGE_RE = re.compile(r"\(([0-9ABC]+)\.(\d+)\)\s*[-–]\s*\(([0-9ABC]+)\.(\d+)\)")


def cite_sets(entry):
    """Statement references and equation labels in `cites`; a range '(4.1)-(4.11)'
    expands to every label in it, so range notation is not scored as disagreement."""
    refs, eqs = set(), set()
    for c in entry.get("cites", []):
        refs |= statement_refs(c)
        for m in RANGE_RE.finditer(c):
            if m.group(1) == m.group(3):
                eqs |= {f"{m.group(1)}.{k}" for k in range(int(m.group(2)), int(m.group(4)) + 1)}
        eqs |= {m.group(1) for m in EQ_RE.finditer(c)}
    return refs, eqs


def jaccard(a, b):
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def compare(x, y):
    rx, ex = cite_sets(x)
    ry, ey = cite_sets(y)
    return {"stmt_jaccard": round(jaccard(rx, ry), 3), "eq_jaccard": round(jaccard(ex, ey), 3),
            "stmt_only_x": sorted(rx - ry), "stmt_only_y": sorted(ry - rx),
            "eq_only_x": sorted(ex - ey), "eq_only_y": sorted(ey - ex),
            "n_hyp": [len(x.get("hypotheses", [])), len(y.get("hypotheses", []))],
            "n_const": [len(x.get("constants", [])), len(y.get("constants", []))],
            "concl_chars": [len(x.get("conclusion", "")), len(y.get("conclusion", ""))]}


def run(write=True, verbose=True):
    shards = {p.stem.split("_")[1]: json.loads(p.read_text()) for p in sorted(SH.glob("shard_*.json"))}
    solo = {e["id"]: e for e in json.loads((D / "ledger.json").read_text())["entries"]}
    index = {s["id"]: s for s in json.loads((D / "statement_index.json").read_text())["statements"]}
    versions = defaultdict(dict)  # id -> shard -> entry
    for sh, d in shards.items():
        for e in d.get("entries", []):
            versions[e["id"]][sh] = e
        for e in d.get("preamble_entries", []):
            versions[e["id"]][sh] = e
    merged, primary_of = [], {}
    for sid in index:
        vs = versions.get(sid, {})
        if not vs:
            continue
        prim = PRIMARY_OVERRIDE.get(sid) or (sorted(vs)[0] if len(vs) == 1 else None)
        if prim is None or prim not in vs:
            prim = sorted(vs)[0]
        primary_of[sid] = prim
        e = dict(vs[prim])
        e["primary_shard"] = prim
        e["other_versions"] = {k: v for k, v in vs.items() if k != prim}
        merged.append(e)
    have = {e["id"] for e in merged}
    absent = [i for i in index if i not in have]
    bad_page = [e["id"] for e in merged if e.get("page") != index[e["id"]]["page"]]
    empty = [(e["id"], k) for e in merged for k in ("hypotheses", "conclusion", "cites") if not e.get(k)]
    # gate (d): preamble five-way, B.10 two-way, and every primary vs solo
    preamble = {}
    for sid in PREAMBLE:
        vs = versions[sid]
        pair = {}
        keys = sorted(vs)
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                pair[f"{a}-{b}"] = compare(vs[a], vs[b])
        refs_all = {k: cite_sets(v)[0] for k, v in vs.items()}
        eqs_all = {k: cite_sets(v)[1] for k, v in vs.items()}
        preamble[sid] = {"shards": keys, "pairwise": pair,
                         "stmt_refs_union": sorted(set().union(*refs_all.values())),
                         "stmt_refs_in_all": sorted(set.intersection(*refs_all.values())) if refs_all else [],
                         "eq_union": sorted(set().union(*eqs_all.values())),
                         "eq_in_all": sorted(set.intersection(*eqs_all.values())) if eqs_all else [],
                         "n_hyp": {k: len(v.get("hypotheses", [])) for k, v in vs.items()},
                         "n_const": {k: len(v.get("constants", [])) for k, v in vs.items()},
                         "concl_chars": {k: len(v.get("conclusion", "")) for k, v in vs.items()}}
    b10 = compare(versions["Corollary B.10"]["C"], versions["Corollary B.10"]["E"]) if {"C", "E"} <= set(versions.get("Corollary B.10", {})) else None
    vs_solo = {}
    for e in merged:
        vs_solo[e["id"]] = compare(e, solo[e["id"]])
    flags = sorted(vs_solo, key=lambda k: (vs_solo[k]["stmt_jaccard"] + vs_solo[k]["eq_jaccard"]))
    cnd = [dict(r, shard=sh) for sh, d in shards.items() for r in d.get("could_not_determine", [])]
    hard = {sh: d.get("hard_pages", []) for sh, d in shards.items()}
    out = {
        "schema": "arc6_merged_ledger_v1", "leg": 428,
        "shards": {sh: {"pages": d.get("pages"), "n_entries": len(d.get("entries", [])), "n_preamble": len(d.get("preamble_entries", [])),
                        "n_hard_pages": len(d.get("hard_pages", [])), "n_could_not_determine": len(d.get("could_not_determine", [])),
                        "stopped_at_page": d.get("stopped_at_page")} for sh, d in shards.items()},
        "merge_rule": "primary = the shard whose page range holds the statement; overrides " + json.dumps(PRIMARY_OVERRIDE),
        "gate": {"a_all_79": not absent, "absent": absent, "n_merged": len(merged),
                 "b_all_nonempty": not empty, "empty_fields": empty, "page_mismatch": bad_page,
                 "c_hard_pages_per_shard": {sh: len(v) for sh, v in hard.items()},
                 "d_preamble_five_way": preamble, "d_corollary_B10_C_vs_E": b10,
                 "d_primary_vs_solo": vs_solo,
                 "d_lowest_agreement_with_solo": [{"id": k, **{x: vs_solo[k][x] for x in ("stmt_jaccard", "eq_jaccard")}} for k in flags[:15]],
                 "d_mean_stmt_jaccard": round(sum(v["stmt_jaccard"] for v in vs_solo.values()) / len(vs_solo), 3),
                 "d_mean_eq_jaccard": round(sum(v["eq_jaccard"] for v in vs_solo.values()) / len(vs_solo), 3)},
        "could_not_determine": cnd, "hard_pages": hard,
        "entries": merged,
    }
    if write:
        OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        g = out["gate"]
        print(f"shards: { {k: (v['n_entries'], v['n_preamble']) for k, v in out['shards'].items()} }")
        print(f"(a) all 79: {g['a_all_79']} (merged {g['n_merged']}, absent {g['absent']})   page mismatches: {g['page_mismatch']}")
        print(f"(b) all non-empty: {g['b_all_nonempty']}  empty: {g['empty_fields']}")
        print(f"(c) hard pages per shard: {g['c_hard_pages_per_shard']}")
        print(f"(d) mean Jaccard vs solo: statements {g['d_mean_stmt_jaccard']}, equations {g['d_mean_eq_jaccard']}")
        print("    lowest agreement:", g["d_lowest_agreement_with_solo"][:10])
        for sid, p in preamble.items():
            print(f"    preamble {sid}: refs in all {p['stmt_refs_in_all']} / union {len(p['stmt_refs_union'])}; eq in all {p['eq_in_all']} / union {len(p['eq_union'])}; n_hyp {p['n_hyp']} n_const {p['n_const']}")
        print(f"    B.10 C vs E: {b10 and {k: b10[k] for k in ('stmt_jaccard', 'eq_jaccard', 'n_hyp', 'n_const')}}")
        print(f"could_not_determine: {len(cnd)} records")
    return out


if __name__ == "__main__":
    run()
