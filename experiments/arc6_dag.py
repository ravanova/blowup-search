"""Arc 6, unit R3 (leg 426): the dependency DAG of Theorem 1.1 and its spine.

    .venv/bin/python experiments/arc6_dag.py          # build both passes, gate, write dag.json

PRE-REGISTRATION: experiments/journal/leg_426_prereg.md, committed at 15fc747
BEFORE this file existed: the five edge-direction rules, the judgment spine
(the prereg's summary line says 36 nodes; its list holds 38 -- banked, not
edited), the mechanical spine SPINE_M = longest chain U {transitive fan-in >=
20}, and every numeric expectation.

TWO PASSES, and why there are two.
  LEDGER pass -- exactly what the pre-registration specified: edges from the R2
    ledger's `cites` strings under the five named rules. Its result against
    the pre-committed numbers is reported as it fell.
  TEXT pass -- decided AFTER the ledger pass had been seen (post hoc, and
    labelled so): edges from the MANUSCRIPT'S OWN PROOF TEXT, one edge X -> Y
    for every statement Y named inside the proof of X (between "Proof." and
    the next box, or a "Proof of X." block). It does not use the ledger's
    judgment at all; it is the check on it. Its numbers were NOT pre-committed.

X -> Y means "X depends on Y". Both graphs are pictures of what the manuscript
SAYS it uses. Neither can see a wrong step or an unstated dependency. R4 does.

CEILING: bookkeeping. Nothing here verifies anything. UNVERIFIED (§3f rule 1).
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "writeup" / "data" / "arc6"
LEDGER = D / "ledger.json"
INDEX = D / "statement_index.json"
PAGES = D / "manuscript_pages.jsonl"
OUT = D / "dag.json"
ROOT_NODE = "Theorem 1.1"

KIND_RE = re.compile(r"\b(Theorem|Proposition|Lemma|Corollary|Definition)(s?)\b")
TOK_RE = re.compile(r"(?<![\(\w])((?:[0-9]{1,2}|[ABC])\.\d+)(?!\d)")
EQ_RE = re.compile(r"\(([0-9ABC]+\.\d+)\)")
HYPHEN_RE = re.compile(r"\b(Proposi|Propo|Lem|Corol|Theo|Defini)-\s+")

# Named overrides from the pre-registration. Nothing else may be added without a
# CORRECTIONS.md entry.
TARGET = {("Proposition 9.9", "Theorem 3.1"), ("Proposition C.3", "Theorem 4.6")}
POINTER = {("Theorem 1.1", "Corollary 10.6"), ("Lemma A.5", "Proposition B.2")}
FANIN_SPINE = 20

PREREG_SPINE = [
    "Theorem 1.1", "Lemma 10.5", "Lemma 10.3", "Proposition 10.1", "Lemma 10.4",
    "Theorem 3.1", "Proposition 9.9", "Lemma 5.4", "Proposition 5.5",
    "Proposition 9.6", "Proposition 9.3", "Proposition 9.5", "Proposition 9.1", "Lemma 9.2",
    "Proposition 7.2", "Lemma 7.1", "Proposition 7.5", "Proposition 7.6", "Lemma 7.7",
    "Lemma 8.2", "Lemma 8.6", "Lemma 8.7", "Lemma 6.2", "Definition 6.4",
    "Theorem 4.6", "Proposition C.3", "Proposition C.2", "Lemma C.1",
    "Proposition A.4", "Proposition A.7", "Lemma A.8", "Proposition A.10",
    "Proposition B.2", "Proposition B.5", "Proposition B.8", "Corollary B.10",
    "Lemma 4.5", "Lemma 4.4",
]
PREREG_OUTSIDE = [
    "Lemma 4.3", "Lemma 6.3", "Corollary 7.3", "Lemma 7.4", "Corollary 7.8",
    "Proposition 8.4", "Corollary 8.5", "Lemma 9.7", "Lemma 9.8", "Corollary 10.6",
    "Lemma A.1", "Lemma A.2", "Lemma A.9", "Lemma B.1", "Lemma B.4", "Lemma B.7",
    "Corollary A.3", "Corollary B.6",
]


# ----------------------------------------------------------------- parsing
def statement_refs(s):
    """Statement identifiers named in one string, plural lists included.

    'Propositions A.4, A.7 and Lemmas A.5' -> [Proposition A.4, Proposition A.7, Lemma A.5].
    A bare S.n token counts only after a kind word: one token after a singular
    kind, any number after a plural kind. Parenthesised tokens are equations.
    """
    s = HYPHEN_RE.sub(lambda m: m.group(1), s)
    events = []
    for m in KIND_RE.finditer(s):
        events.append((m.start(), "kind", m.group(1), bool(m.group(2))))
    for m in TOK_RE.finditer(s):
        events.append((m.start(), "tok", m.group(1), None))
    events.sort()
    out, kind, plural, taken = [], None, False, 0
    for _, typ, val, pl in events:
        if typ == "kind":
            kind, plural, taken = val, pl, 0
        elif kind is not None and (plural or taken == 0):
            out.append(f"{kind} {val}")
            taken += 1
    return out


def classify(s, refs):
    if refs:
        return "STATEMENT"
    if re.search(r"\[\d+", s):
        return "REFERENCE"
    if s.lower().startswith("used"):
        return "USED-BY"
    if s.lower().startswith("proved"):
        return "LOCATION"
    if re.search(r"\bSections?\b|\bRemark\b|\bafter \(", s):
        return "UNNUMBERED"
    if EQ_RE.search(s):
        return "EQUATION"
    return "CLASSICAL"


# ------------------------------------------------------------ ledger pass
def build(ledger, used_by_rule=True, overrides=True):
    """Return (dep_edges, log). dep_edges: set of (X, Y) meaning X depends on Y."""
    ids = {e["id"] for e in ledger["entries"]}
    dep, log = set(), {"fired": [], "dropped": [], "non_statement": []}
    for e in ledger["entries"]:
        for c in e["cites"]:
            refs = [r for r in statement_refs(c) if r in ids and r != e["id"]]
            cls = classify(c, refs)
            if cls != "STATEMENT":
                log["non_statement"].append({"from": e["id"], "cite": c, "class": cls})
            plural = bool(re.search(r"\b(Propositions|Lemmas|Theorems|Corollaries|Definitions)\b", c))
            for r in refs:
                if used_by_rule and c.lower().startswith("used"):
                    dep.add((r, e["id"]))
                    log["fired"].append({"from": r, "to": e["id"], "rule": "USED-BY", "cite": c})
                elif overrides and (e["id"], r) in TARGET:
                    log["dropped"].append({"from": e["id"], "to": r, "rule": "TARGET", "cite": c})
                elif overrides and (e["id"], r) in POINTER:
                    log["dropped"].append({"from": e["id"], "to": r, "rule": "POINTER", "cite": c})
                else:
                    dep.add((e["id"], r))
                    log["fired"].append({"from": e["id"], "to": r, "rule": "PLURAL" if plural else "DEP", "cite": c})
    return dep, log


# -------------------------------------------------------------- text pass
def load_lines():
    return [json.loads(l) for l in PAGES.open()]


def proof_spans(lines, index):
    """Map statement id -> list of (start, end) line-index spans holding its proof.

    An immediate proof: the first line beginning 'Proof.' inside the statement's
    scope (its header up to the next header), through the next line carrying a
    box. A deferred proof: a line beginning 'Proof of <id>.' anywhere, through
    the next box. Theorem 3.1 has no proof block of its own; the manuscript
    proves it inside Proposition 9.9, whose statement is 'all conclusions of
    Theorem 3.1 hold' -- that link is added as TARGET-REVERSED below.
    """
    pos = {}
    for s in index["statements"]:
        for i, l in enumerate(lines):
            if l["page"] == s["page"] and l["line"] == s["line"]:
                pos[s["id"]] = i
                break
    order = sorted(pos, key=pos.get)
    spans = defaultdict(list)
    n = len(lines)

    def next_box(i):
        j = i
        while j < n and "□" not in lines[j]["text"]:
            j += 1
        return min(j, n - 1)

    for k, sid in enumerate(order):
        start = pos[sid]
        end = pos[order[k + 1]] if k + 1 < len(order) else n
        for i in range(start, end):
            if re.match(r"\s*Proof\.", lines[i]["text"]):
                spans[sid].append((i, next_box(i)))
                break
    for i, l in enumerate(lines):
        m = re.match(r"\s*Proof of ((?:Theorem|Proposition|Lemma|Corollary) [0-9ABC]+\.\d+)\.", l["text"])
        if m and m.group(1) in pos:
            spans[m.group(1)].append((i, next_box(i)))
    return spans, pos


def build_text(lines, index):
    ids = {s["id"] for s in index["statements"]}
    spans, pos = proof_spans(lines, index)
    dep, mentions = set(), {}
    for sid, sps in spans.items():
        text = " ".join(lines[i]["text"] for a, b in sps for i in range(a, b + 1))
        refs = sorted({r for r in statement_refs(text) if r in ids and r != sid})
        mentions[sid] = refs
        for r in refs:
            if (sid, r) in TARGET:
                continue  # a proof naming the statement it proves is not a dependency
            dep.add((sid, r))
    # the two proofs whose conclusion IS another statement
    for prover, target in TARGET:
        dep.add((target, prover))
    return dep, {"spans": {k: [[lines[a]["page"], lines[b]["page"]] for a, b in v] for k, v in spans.items()},
                 "mentions": mentions, "no_proof_block": sorted(ids - set(spans))}


# ---------------------------------------------- equation-resolved pass
SECTION_PAGES = {"1": (1, 5), "3": (6, 23), "4": (24, 44), "5": (45, 61), "6": (62, 72), "7": (73, 87),
                 "8": (88, 99), "9": (100, 115), "10": (116, 125), "A": (126, 143), "B": (144, 156), "C": (157, 164)}
LABEL_RE = re.compile(r"\(([0-9ABC]+)\.(\d+)\)")


def scopes(lines, index):
    """Per statement: body span [header, proof start or next header) and proof spans."""
    spans, pos = proof_spans(lines, index)
    order = sorted(pos, key=pos.get)
    body = {}
    n = len(lines)
    # A statement's body runs from its header to its proof, the next header, or the
    # next (sub)section heading, whichever is first. Headings are what stop a
    # proof-less statement (a Definition, Theorem 3.1) from swallowing the prose
    # that follows it.
    heading = re.compile(r"^\s*(?:[0-9]+|[A-C])(?:\.\d+)?\.\s+[A-Z][a-z]")
    para = re.compile(r"^\s{1,3}[A-Z]|^\s*Table\b")   # an indented new paragraph, or a table
    for k, sid in enumerate(order):
        start = pos[sid]
        end = pos[order[k + 1]] if k + 1 < len(order) else n
        stop = end
        for i in range(start + 1, end):
            t = lines[i]["text"]
            if re.match(r"\s*Proof", t) or heading.match(t):
                stop = i
                break
            if not t.strip():  # a blank line followed by a new paragraph ends a proof-less statement
                j = i + 1
                while j < end and not lines[j]["text"].strip():
                    j += 1
                if j < end and para.match(lines[j]["text"]):
                    stop = i
                    break
        body[sid] = (start, stop)
    return body, dict(spans), pos


def label_owners(lines, body, proofs):
    """Owner of each displayed equation label: the statement in whose body or proof
    it is first displayed (within its own section's pages), else '§S prose'."""
    def where(i):
        for sid, (a, b) in body.items():
            if a <= i < b:
                return sid, "body"
        for sid, sps in proofs.items():
            for a, b in sps:
                if a <= i <= b:
                    return sid, "proof"
        return None, "prose"
    occ = defaultdict(list)  # label -> [(line index, display_like)]
    for i, l in enumerate(lines):
        for m in LABEL_RE.finditer(l["text"]):
            sec = m.group(1)
            lo, hi = SECTION_PAGES.get(sec, (0, 0))
            if not (lo <= l["page"] <= hi):
                continue
            tail = l["text"][m.end():]
            display = bool(re.match(r"\s*$", tail) or re.match(r"\s{3,}", tail))
            occ[f"{sec}.{m.group(2)}"].append((i, display))
    owner = {}
    for lab, lst in occ.items():
        disp = [i for i, d in lst if d]
        i = disp[0] if disp else lst[0][0]
        sid, kind = where(i)
        sec = lab.split(".")[0]
        owner[lab] = {"owner": sid if sid else f"§{sec} prose", "kind": kind, "page": lines[i]["page"]}
    return owner


def build_eq(lines, index):
    ids = {s["id"] for s in index["statements"]}
    body, proofs, pos = scopes(lines, index)
    owner = label_owners(lines, body, proofs)
    dep, detail, unresolved = set(), {}, defaultdict(list)
    named_edges, eq_edges = {}, {}
    for sid in sorted(ids):
        spans = [body[sid]] + [(a, b + 1) for a, b in proofs.get(sid, [])]
        text = " ".join(lines[i]["text"] for a, b in spans for i in range(a, b))
        refs = {r for r in statement_refs(text) if r in ids and r != sid and (sid, r) not in TARGET and (sid, r) not in POINTER}
        labels = sorted({f"{m.group(1)}.{m.group(2)}" for m in LABEL_RE.finditer(text)})
        via_eq = defaultdict(list)
        for lab in labels:
            o = owner.get(lab)
            if o is None:
                unresolved[sid].append(lab)
                continue
            tgt = o["owner"]
            if tgt != sid and (sid, tgt) not in TARGET and (sid, tgt) not in POINTER:
                via_eq[tgt].append(lab)
        named_edges[sid] = refs
        eq_edges[sid] = dict(via_eq)
        detail[sid] = {"named": sorted(refs), "via_equations": {k: v for k, v in sorted(via_eq.items())}}
    dropped = []
    for sid in sorted(ids):
        for r in sorted(named_edges[sid]):
            if sid in named_edges.get(r, set()) and pos[sid] < pos[r]:
                # MUTUAL-NAMED: two statements name each other; the earlier one's
                # mention of the later one is a forward pointer, not a dependency
                dropped.append({"from": sid, "to": r, "rule": "MUTUAL-NAMED"}); continue
            dep.add((sid, r))
        for tgt, labs in sorted(eq_edges[sid].items()):
            if tgt in named_edges[sid]:
                continue  # already a named dependency
            if tgt == ROOT_NODE:
                dropped.append({"from": sid, "to": tgt, "rule": "ROOT-EQ", "labels": labs}); continue
            if sid in named_edges.get(tgt, set()):
                dropped.append({"from": sid, "to": tgt, "rule": "TARGET-EQ", "labels": labs}); continue
            dep.add((sid, tgt))
    for prover, target in TARGET:
        dep.add((target, prover))
    return dep, {"owners": owner, "detail": detail, "unresolved_labels": dict(unresolved), "dropped": dropped,
                 "prose_nodes": sorted({o["owner"] for o in owner.values() if o["owner"].startswith("§")})}


def narrative_mentions(lines, index, sid, body, proofs):
    """Lines mentioning sid outside its own body/proof (section narrative, tables, other proofs)."""
    own = set(range(*body[sid])) | {i for a, b in proofs.get(sid, []) for i in range(a, b + 1)}
    out = []
    for i, l in enumerate(lines):
        if i in own:
            continue
        if sid in statement_refs(l["text"]):
            out.append(l["page"])
    return sorted(set(out))


# ------------------------------------------------------------ graph tools
def adjacency(edges):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
    return adj


def cycles(edges):
    adj = adjacency(edges)
    color, out = {}, []

    def dfs(u, stack):
        color[u] = 1
        stack.append(u)
        for v in sorted(adj[u]):
            if color.get(v, 0) == 1:
                out.append(stack[stack.index(v):] + [v])
            elif color.get(v, 0) == 0:
                dfs(v, stack)
        stack.pop()
        color[u] = 2

    for u in sorted(set(a for a, _ in edges) | set(b for _, b in edges)):
        if color.get(u, 0) == 0:
            dfs(u, [])
    return out


def reachable(adj, start):
    seen, todo = set(), [start]
    while todo:
        u = todo.pop()
        if u in seen:
            continue
        seen.add(u)
        todo.extend(adj[u])
    return seen


def longest_chain(adj, start):
    """Longest path from start in a DAG (edges counted); ties by lexicographic path."""
    memo = {}

    def best(u):
        if u in memo:
            return memo[u]
        cands = [best(v) for v in sorted(adj[u])]
        if not cands:
            memo[u] = (0, [u])
        else:
            n_max = max(t[0] for t in cands)
            path = min([t[1] for t in cands if t[0] == n_max])
            memo[u] = (n_max + 1, [u] + path)
        return memo[u]

    return best(start)


def transitive_fanin(adj, closure):
    """For each node v in closure: number of closure nodes u != v with v reachable from u."""
    fan = {v: 0 for v in closure}
    for u in closure:
        for v in reachable(adj, u) - {u}:
            if v in fan:
                fan[v] += 1
    return fan


def section_of(sid):
    return sid.split()[1].split(".")[0]


def analyse(dep, ids, dangling):
    cyc = cycles(dep)
    adj = adjacency(dep)
    closure = reachable(adj, ROOT_NODE)
    outside = sorted(set(ids) - closure)
    prose_reached = sorted(v for v in closure if v.startswith("§"))
    closure = {v for v in closure if not v.startswith("§")} | set(prose_reached)  # statements + reached prose
    dangling = list(dangling) + [{"from": "(reached)", "cite": v} for v in prose_reached]
    leaves = sorted(v for v in closure if not adj[v])
    if cyc:  # chain and fan-in are only defined on a DAG; report the cycles and stop
        n_chain, chain, fan = -1, [], {v: 0 for v in closure}
    else:
        n_chain, chain = longest_chain(adj, ROOT_NODE)
        fan = transitive_fanin(adj, closure)
    spine_m = sorted(set(chain) | {v for v, f in fan.items() if f >= FANIN_SPINE}, key=lambda v: (-fan[v], v))
    secs_m = sorted({section_of(v) for v in spine_m}, key=lambda s: (s.isalpha(), s.zfill(2)))
    secs_closure = sorted({section_of(v) for v in closure}, key=lambda s: (s.isalpha(), s.zfill(2)))
    prereg_in = [v for v in PREREG_SPINE if v in spine_m]
    prereg_absent = [{"id": v, "fanin": fan.get(v), "in_closure": v in closure} for v in PREREG_SPINE if v not in spine_m]
    overlap = len(prereg_in) / len(spine_m) if spine_m else 0.0
    missing = [s for s in ("4", "7", "9") if s not in secs_m]
    gate = {
        "acyclic": "YES" if not cyc else "NO", "cycles": cyc,
        "complete": "YES" if not dangling else "NO-AND-HERE-ARE-THE-DANGLING-NODES",
        "dangling": dangling,
        "closure_size": len([v for v in closure if not v.startswith("§")]), "prose_nodes_reached": prose_reached,
        "closure_sections": secs_closure, "outside_closure": outside,
        "longest_chain_edges": n_chain, "longest_chain": chain,
        "spine_m_sections": secs_m,
        "spine_contains_4_7_9": "YES" if not missing else "NO-AND-MISSING-" + ",".join(missing),
        "overlap_prereg_over_spine_m": round(overlap, 4),
    }
    checks = {
        "acyclic_expected_YES": gate["acyclic"] == "YES",
        "closure_ge_60": len([v for v in closure if not v.startswith("§")]) >= 60,
        "outside_le_8": len(outside) <= 8,
        "dangling_ge_1": len(dangling) >= 1,
        "remark_B9_dangling": any("Remark B.9" in d["cite"] for d in dangling),
        "chain_ge_8": n_chain >= 8,
        "spine_has_4_7_9": not missing,
        "overlap_ge_0.75": overlap >= 0.75,
    }
    return {
        "gate": gate, "prereg_checks": checks, "n_passed": sum(checks.values()), "n_checks": len(checks),
        "fanin": dict(sorted(fan.items(), key=lambda kv: (-kv[1], kv[0]))),
        "spine_m": spine_m,
        "prereg": {"in_spine_m": prereg_in, "absent_from_spine_m": prereg_absent,
                   "spine_m_not_in_prereg": [v for v in spine_m if v not in PREREG_SPINE],
                   "expected_outside_actually_outside": [v for v in PREREG_OUTSIDE if v in outside],
                   "expected_outside_but_in_closure": [{"id": v, "fanin": fan.get(v)} for v in PREREG_OUTSIDE if v in closure]},
        "leaves": leaves,
        "edges": sorted(map(list, dep)),
    }


def run(write=True, verbose=True):
    led = json.loads(LEDGER.read_text())
    index = json.loads(INDEX.read_text())
    ids = [e["id"] for e in led["entries"]]
    # ledger pass
    raw, _ = build(led, used_by_rule=False, overrides=False)
    dep, log = build(led)
    closure_l = reachable(adjacency(dep), ROOT_NODE)
    dangling_l = sorted({(n["from"], n["cite"]) for n in log["non_statement"] if n["class"] == "UNNUMBERED" and n["from"] in closure_l})
    dangling_l = [{"from": a, "cite": b} for a, b in dangling_l]
    L = analyse(dep, ids, dangling_l)
    supports = defaultdict(list)
    for n in log["non_statement"]:
        supports[n["from"]].append({"class": n["class"], "cite": n["cite"]})
    L["leaves"] = [{"id": v, "supports": supports.get(v, [])} for v in L["leaves"]]
    L["counts"] = {"dep_edges": len(dep), "raw_edges_no_rules": len(raw), "raw_cycles_no_rules": len(cycles(raw)),
                   "by_rule": {r: sum(1 for f in log["fired"] if f["rule"] == r) for r in ("DEP", "PLURAL", "USED-BY")},
                   "dropped": len(log["dropped"]),
                   "non_statement_cites": {c: sum(1 for n in log["non_statement"] if n["class"] == c)
                                           for c in ("REFERENCE", "CLASSICAL", "UNNUMBERED", "LOCATION", "EQUATION", "USED-BY")}}
    L["edge_log"] = log
    # text pass
    lines = load_lines()
    dep_t, tlog = build_text(lines, index)
    T = analyse(dep_t, ids, dangling=[])  # unnumbered pointers are not parsed from proof text; see journal
    T["counts"] = {"dep_edges": len(dep_t), "statements_with_proof_block": len(tlog["spans"]),
                   "no_proof_block": tlog["no_proof_block"], "target_reversed": sorted([t, p] for p, t in TARGET)}
    T["proof_spans_pages"] = tlog["spans"]
    T["mentions"] = tlog["mentions"]
    # equation-resolved pass
    dep_e, elog = build_eq(lines, index)
    Q = analyse(dep_e, ids, dangling=[])
    body, proofs, _ = scopes(lines, index)
    closure_e = reachable(adjacency(dep_e), ROOT_NODE)
    Q["counts"] = {"dep_edges": len(dep_e), "labels_owned": len(elog["owners"]), "dropped": elog["dropped"],
                   "labels_owned_by_prose": sum(1 for o in elog["owners"].values() if o["owner"].startswith("§")),
                   "prose_nodes": elog["prose_nodes"], "unresolved_labels": elog["unresolved_labels"]}
    Q["label_owners"] = elog["owners"]
    Q["detail"] = elog["detail"]
    Q["outside_invoked_by_narrative"] = {v: narrative_mentions(lines, index, v, body, proofs)
                                         for v in Q["gate"]["outside_closure"]}
    Q["prose_nodes_reached"] = {v: sorted(l for l, o in elog["owners"].items() if o["owner"] == v)
                                for v in closure_e if v.startswith("§")}
    # agreement between passes
    common = set(map(tuple, L["edges"])) & set(map(tuple, T["edges"]))
    agree = {"edges_in_both": len(common), "ledger_only": len(L["edges"]) - len(common), "text_only": len(T["edges"]) - len(common),
             "closure_in_both": len(closure_l & reachable(adjacency(dep_t), ROOT_NODE)),
             "spine_m_in_both": sorted(set(L["spine_m"]) & set(T["spine_m"])),
             "text_closure_minus_ledger_closure": sorted(reachable(adjacency(dep_t), ROOT_NODE) - closure_l),
             "ledger_closure_minus_text_closure": sorted(closure_l - reachable(adjacency(dep_t), ROOT_NODE))}
    out = {
        "schema": "arc6_dag_v2", "leg": 426, "root": ROOT_NODE, "statements": len(ids),
        "rules": {"DEP": "citer depends on cited (default; also 'proved in/from')",
                  "USED-BY": "string begins 'used ...': reversed, each listed statement depends on the citer",
                  "PLURAL": "'Propositions A.4, A.7, ... and Lemmas ...': one DEP edge per item",
                  "TARGET": sorted(map(list, TARGET)), "POINTER": sorted(map(list, POINTER)),
                  "TEXT": "X -> Y for every statement Y named inside the proof block of X in manuscript_pages.jsonl; plus TARGET reversed (Theorem 3.1 -> Proposition 9.9, Theorem 4.6 -> Proposition C.3)"},
        "prereg": {"spine_list": PREREG_SPINE, "spine_list_length": len(PREREG_SPINE), "prereg_summary_line_said": 36,
                   "expected_outside": PREREG_OUTSIDE, "fanin_threshold": FANIN_SPINE,
                   "text_pass_is_post_hoc": True},
        "ledger_pass": L, "text_pass": T, "equation_pass": Q, "agreement": agree,
        "r4_spine_named_additions": ["Lemma 4.8", "Lemma 9.7"],
        "r4_spine": sorted(set(PREREG_SPINE) | set(v for v in Q["gate"]["longest_chain"] if not v.startswith("§"))
                           | (set(Q["gate"]["outside_closure"]) - {"Corollary 10.6"}) | {"Lemma 4.8", "Lemma 9.7"},
                           key=lambda v: (section_of(v).isalpha(), section_of(v).zfill(2), v)),
        "closure_union_all_passes": sorted((closure_l | reachable(adjacency(dep_t), ROOT_NODE) | closure_e) & set(ids)),
    }
    if write:
        OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        for name, P in (("LEDGER PASS (pre-registered)", L), ("TEXT PASS (post hoc)", T), ("EQUATION PASS (post hoc)", Q)):
            g = P["gate"]
            print(f"===== {name}: {P['counts']['dep_edges']} edges")
            print(f"  acyclic {g['acyclic']} ({len(g['cycles'])} cycles)   complete {g['complete']}")
            for c in g["cycles"][:10]:
                print("     CYCLE:", " -> ".join(c))
            for d in g["dangling"]:
                print(f"     DANGLING: {d['from']} -> {d['cite']!r}")
            print(f"  closure {g['closure_size']}/79 sections {g['closure_sections']}")
            print(f"  outside ({len(g['outside_closure'])}): {g['outside_closure']}")
            print(f"  chain {g['longest_chain_edges']}: " + " -> ".join(g["longest_chain"]))
            print(f"  top fan-in: {list(P['fanin'].items())[:12]}")
            print(f"  SPINE_M ({len(P['spine_m'])}) sections {g['spine_m_sections']}  4/7/9: {g['spine_contains_4_7_9']}  overlap {g['overlap_prereg_over_spine_m']}")
            print(f"  prereg absent: {[p['id'] for p in P['prereg']['absent_from_spine_m']]}")
            print(f"  prereg checks {P['n_passed']}/{P['n_checks']}: {P['prereg_checks']}")
        print("no proof block:", T["counts"]["no_proof_block"])
        print("EQ pass: labels owned", Q["counts"]["labels_owned"], "by prose", Q["counts"]["labels_owned_by_prose"], "unresolved", {k: v for k, v in Q["counts"]["unresolved_labels"].items()})
        print("EQ prose nodes reached:", Q["prose_nodes_reached"])
        print("EQ outside, invoked by narrative on pages:", Q["outside_invoked_by_narrative"])
        print("closure union of all passes:", len(out["closure_union_all_passes"]))
        print("agreement:", {k: v for k, v in agree.items() if not isinstance(v, list)}, "\n  text-only closure:", agree["text_closure_minus_ledger_closure"], "\n  ledger-only closure:", agree["ledger_closure_minus_text_closure"])
    return out


if __name__ == "__main__":
    run()
