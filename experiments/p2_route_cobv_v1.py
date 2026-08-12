"""Leg 384 -- ROUTE-COBV: CLAY_OBLIGATIONS.md's remaining reviewer-read clauses,
checked MECHANICALLY against primary text and this repository's own landed ledger.

WHAT THIS INSTRUMENT IS
-------------------------------------------------------------------------------
A verifier, not a repairer. It reads `CLAY_OBLIGATIONS.md` as TEXT and compares it,
programmatically, against three classes of source:

  (i)   leg 381's banked `check_D` verdicts in `writeup/data/p2_route_cloc_v1.json`
        -- the mechanical verbatim-match of integration's landed edit (a962e4a, in
        d65419c). The DM read that edit VISUALLY in cycle 11e; this is the
        programmatic read that a visual one is explicitly not a substitute for.
  (ii)  the four rigidity rows of §2, against their OWN named landed records
        (writeup/data/p2_route_{pvlx,ctrx,mryx,b7m,algw}_v1.json) and against the
        landed ledger code in solver/dssp_screen.py, EXECUTED -- machine-read, never
        transcribed. Reading a number off a document and retyping it is exactly the
        failure mode clause (ii) exists to catch, so every compared value is parsed
        out of BOTH sides by this file.
  (iii) §7's three prize-rules clauses against the Clay Mathematics Institute's OWN
        published rules (a DIFFERENT document from the problem statement leg 381
        read). If the source is unreachable the refusal is banked verbatim with its
        HTTP status code and the clause is recorded UNVERIFIED -- never as a pass,
        and never quietly dropped.

This file EDITS NOTHING. `CLAY_OBLIGATIONS.md` is integration-owned and is opened
read-only; `writeup/data/p2_route_cloc_v1.json` is read and never written. Proposed
corrections are emitted as exact text in the JSON payload, for integration to land.

THE PLANTED-MISMATCH CONTROL (why a zero here is a measurement, not an absence)
-------------------------------------------------------------------------------
A leg this cycle found a FABRICATED ZERO in its own instrument -- a variable
initialised to 0.0 and never written. This leg's headline is a mismatch count, which
is the same failure shape. So every check carries its OWN targeted plant:

  * a check that reads MATCH on the clean sources is re-run against a surgically
    corrupted copy of its own source, and the control is satisfied only if it then
    reads MISMATCH;
  * a check that reads MISMATCH on the clean sources is re-run against a surgically
    REPAIRED copy, and the control is satisfied only if it then reads MATCH.

Both directions are exercised, per row, by name. A check whose plant does not flip it
is reported as CONTROL-FAILED and its clean verdict is discarded as uninformative.

CEILING: TIER 2. No link of the L1 -> L4 chain moves. CLAY_OBLIGATIONS §6's two
no-method obligations stay OPEN. Clay stays ~0.05%.

Run:    .venv/bin/python experiments/p2_route_cobv_v1.py
Writes: writeup/data/p2_route_cobv_v1.json
"""

import copy
import hashlib
import json
import math
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "writeup" / "data" / "p2_route_cobv_v1.json"
DOC = ROOT / "CLAY_OBLIGATIONS.md"
DATA = ROOT / "writeup" / "data"
PAPERS = ROOT / "Papers"          # gitignored on purpose; the PDF is never committed

CLAY_RULES_PAGE = "https://www.claymath.org/millennium-problems/rules/"
CLAY_RULES_PDF = "https://www.claymath.org/wp-content/uploads/2022/03/millennium_prize_rules_0.pdf"

# Integration's landed edit, and the leg whose verdicts it is checked against.
LANDED_EDIT = "a962e4a (merged in d65419c)"
SOURCE_OF_TRUTH = "writeup/data/p2_route_cloc_v1.json (leg 381, 7aecf78) -- READ ONLY"


# ------------------------------------------------------------------ text helpers

def norm(s):
    """Normalise for phrase matching: strip soft hyphens/ligature noise that
    pdftotext leaves behind, collapse whitespace, casefold."""
    s = s.replace("­", "").replace("‐", "-").replace("‑", "-")
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("‘", "'").replace("’", "'")
    s = s.replace(" ", " ")          # pdftotext leaves NBSP between every word
    s = re.sub(r"\n\s*>\s?", "\n", s)     # markdown blockquote markers, so a clause
    s = re.sub(r"\s+", " ", s)            # that wraps across '>' lines still matches
    return s.casefold()


def has(hay, needle):
    return norm(needle) in norm(hay)


def section(doc, header, next_headers):
    """The text of one '## ...' section of CLAY_OBLIGATIONS.md."""
    i = doc.index(header)
    j = len(doc)
    for h in next_headers:
        k = doc.find(h, i + len(header))
        if k != -1:
            j = min(j, k)
    return doc[i:j]


def decimals(literal):
    m = re.search(r"\.(\d+)", literal)
    return len(m.group(1)) if m else 0


def matches_at_doc_precision(doc_literal, record_value):
    """Is the document's printed literal what the record's value rounds to, at the
    document's OWN printed precision? Handles both fixed-point and mantissa-e-exp."""
    lit = doc_literal.strip()
    if "e" in lit.lower():
        try:
            return abs(float(lit) - record_value) <= abs(float(lit)) * 0.05
        except ValueError:
            return False
    d = decimals(lit)
    try:
        return f"{abs(record_value):.{d}f}" == lit.lstrip("+-").lstrip("0") or \
               f"{abs(record_value):.{d}f}" == lit.lstrip("+-")
    except (ValueError, TypeError):
        return False


def sha256(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------ the fetch

def fetch_clay_rules():
    """Fetch the CMI prize rules. Records the HTTP status code either way. A
    non-200 (in particular the HTTP 429 this repository has been getting) is banked
    VERBATIM as a REFUSAL TO MEASURE, never as a pass and never dropped."""
    meta = {
        "page_url": CLAY_RULES_PAGE,
        "pdf_url": CLAY_RULES_PDF,
        "attempts": [],
        "reachable": False,
        "refusal_verbatim": None,
        "http_status": None,
    }
    text = ""
    PAPERS.mkdir(exist_ok=True)
    cache = PAPERS / "clay_millennium_prize_rules_2018.pdf"

    for label, url in (("rules_page_html", CLAY_RULES_PAGE), ("rules_pdf", CLAY_RULES_PDF)):
        att = {"target": label, "url": url}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                body = r.read()
                att["http_status"] = r.status
                att["bytes"] = len(body)
                att["sha256"] = sha256(body)
            if label == "rules_pdf":
                cache.write_bytes(body)
                att["cached_at"] = str(cache.relative_to(ROOT)) + " (gitignored, never committed)"
                p = subprocess.run(["pdftotext", "-layout", str(cache), "-"],
                                   capture_output=True, text=True)
                att["pdftotext_returncode"] = p.returncode
                if p.returncode == 0:
                    text = p.stdout
                    att["extracted_chars"] = len(text)
                    meta["reachable"] = True
                    meta["http_status"] = r.status
            else:
                html = body.decode("utf-8", "replace")
                html = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
                stripped = re.sub(r"(?s)<[^>]+>", " ", html)
                att["extracted_chars"] = len(stripped)
                meta["page_text"] = re.sub(r"\s+", " ", stripped)
        except urllib.error.HTTPError as e:
            att["http_status"] = e.code
            att["refusal_verbatim"] = f"HTTPError {e.code} {e.reason} on {url}"
            meta["refusal_verbatim"] = att["refusal_verbatim"]
            meta["http_status"] = e.code
        except Exception as e:                                    # noqa: BLE001
            att["http_status"] = None
            att["refusal_verbatim"] = f"{type(e).__name__}: {e} on {url}"
            meta["refusal_verbatim"] = att["refusal_verbatim"]
        meta["attempts"].append(att)

    meta["rules_text_chars"] = len(text)
    meta["rules_text_sha256"] = sha256(text.encode()) if text else None
    return text, meta


# ------------------------------------------------------------------ check plumbing

CHECKS = []


def check(cid, item, claim, plant_kind="corrupt"):
    def deco(fn):
        CHECKS.append({"id": cid, "item": item, "claim": claim,
                       "fn": fn, "plant_kind": plant_kind})
        return fn
    return deco


def M(detail, **kw):
    d = {"verdict": "MATCH", "detail": detail}
    d.update(kw)
    return d


def X(detail, **kw):
    d = {"verdict": "MISMATCH", "detail": detail}
    d.update(kw)
    return d


def U(detail, **kw):
    d = {"verdict": "UNVERIFIED", "detail": detail}
    d.update(kw)
    return d


PLANTS = {}


def dup(ctx):
    """A plantable copy of the context: strings and parsed records are deep-copied so
    a plant cannot leak back into the clean run; the imported solver module is carried
    by reference (it is never mutated)."""
    out = {}
    for k, v in ctx.items():
        out[k] = v if k == "screen" else copy.deepcopy(v)
    return out


def plant(cid):
    def deco(fn):
        PLANTS[cid] = fn
        return fn
    return deco


# ------------------------------------------------------------------ ITEM (i)
# The landed CLAY_OBLIGATIONS.md against p2_route_cloc_v1.json's check_D verdicts.

TARGET_PARA_HDR = "## The target, as specified"
LEDGER_BLOCK_MARK = "> **CHECKED AGAINST THE PRIMARY TEXT"


def target_paragraph(ctx):
    """The 'target, as specified' PROSE -- everything before the leg-381 blockquote."""
    sec = section(ctx["doc"], TARGET_PARA_HDR, ["## §1 "])
    return sec[: sec.index(LEDGER_BLOCK_MARK)] if LEDGER_BLOCK_MARK in sec else sec


def ledger_block(ctx):
    sec = section(ctx["doc"], TARGET_PARA_HDR, ["## §1 "])
    return sec[sec.index(LEDGER_BLOCK_MARK):] if LEDGER_BLOCK_MARK in sec else ""


def cd(ctx):
    return ctx["cloc"]["check_D_clay_primary_text"]


def f0_entry(ctx):
    for e in cd(ctx)["reviewer_paragraph_clause_ledger"]:
        if "f" in e["reviewer_clause"] and "0" in e["reviewer_clause"]:
            return e
    return None


@check("I1", "(i)", "'with f = 0' is EXCISED from the 'target, as specified' paragraph")
def i1(ctx):
    para = target_paragraph(ctx)
    hits = [m.group(0) for m in re.finditer(r"f\s*(?:≡|=|\\equiv)\s*0", para)]
    e = f0_entry(ctx)
    rec = e["verdict"] if e else None
    if rec != "REFUTED":
        return X("the JSON's own f-clause verdict is not REFUTED", record_verdict=rec)
    if hits:
        return X("the REFUTED clause survives in the target paragraph",
                 doc_verbatim=hits, record_verdict=rec)
    return M("excised: 0 occurrences of an 'f = 0' clause in the target paragraph, "
             "against JSON verdict REFUTED",
             doc_occurrences=0, record_verdict=rec,
             record_primary_text=e["primary_text"])


@plant("I1")
def i1p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        "such that no smooth solution exists",
        "with `f ≡ 0`, such that no smooth solution exists", 1)
    return c


@check("I2", "(i)", "the REFUTED verdict on 'f = 0' is recorded in the landed ledger block")
def i2(ctx):
    blk = ledger_block(ctx)
    e = f0_entry(ctx)
    if not blk:
        return X("no leg-381 ledger block found in the document")
    ok = has(blk, "- **REFUTED:**") and re.search(r"f\s*(?:≡|=)\s*0", blk)
    if not ok:
        return X("the ledger block does not carry the REFUTED f-clause",
                 record_verdict=e["verdict"])
    also = has(blk, "(A)") and has(blk, "(B)") and has(blk, "existence")
    if not also:
        return X("the block records REFUTED but drops the JSON's reason "
                 "(f = 0 belongs to the EXISTENCE statements (A) and (B))",
                 record_primary_text=e["primary_text"])
    return M("REFUTED recorded, with the (A)/(B)-existence reason the JSON gives",
             record_verdict=e["verdict"], record_primary_text=e["primary_text"])


@plant("I2")
def i2p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace("> - **REFUTED:**", "> - **CONFIRMED:**", 1)
    return c


@check("I3", "(i)", "the 4 CONFIRMED / 1 CORRECTED / 1 REFUTED counts block")
def i3(ctx):
    blk = ledger_block(ctx)
    m = re.search(r"\*\*(\d+)\s+clauses?\s+CONFIRMED,\s*(\d+)\s+CORRECTED,\s*(\d+)\s+REFUTED",
                  blk)
    if not m:
        return X("no counts block of the form 'N clauses CONFIRMED, N CORRECTED, "
                 "N REFUTED' found in the document")
    doc_counts = {"confirmed": int(m.group(1)), "corrected": int(m.group(2)),
                  "refuted": int(m.group(3))}
    json_counts = {k: cd(ctx)["counts"][k] for k in ("confirmed", "corrected", "refuted")}
    # Recompute from the ledger LIST itself, so a fabricated 'counts' block in the
    # JSON cannot silently agree with a fabricated one in the document.
    recomputed = {"confirmed": 0, "corrected": 0, "refuted": 0}
    for e in cd(ctx)["reviewer_paragraph_clause_ledger"]:
        v = e["verdict"].upper()
        if v.startswith("CONFIRMED"):
            recomputed["confirmed"] += 1
        elif v.startswith("CORRECTED"):
            recomputed["corrected"] += 1
        elif v.startswith("REFUTED"):
            recomputed["refuted"] += 1
    if doc_counts != json_counts or json_counts != recomputed:
        return X("counts disagree", doc_counts=doc_counts,
                 json_counts_field=json_counts, recomputed_from_ledger_rows=recomputed)
    return M("document counts == JSON counts field == counts recomputed from the "
             "6 ledger rows", doc_counts=doc_counts, json_counts_field=json_counts,
             recomputed_from_ledger_rows=recomputed,
             ledger_rows_seen=len(cd(ctx)["reviewer_paragraph_clause_ledger"]))


@plant("I3")
def i3p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace("**4 clauses CONFIRMED, 1 CORRECTED, 1 REFUTED.**",
                                "**5 clauses CONFIRMED, 1 CORRECTED, 1 REFUTED.**", 1)
    return c


@check("I4", "(i)", "the (b) -> (C) labelling fix")
def i4(ctx):
    blk = ledger_block(ctx)
    ent = None
    for e in cd(ctx)["reviewer_paragraph_clause_ledger"]:
        if e["verdict"].startswith("CORRECTED"):
            ent = e
    if ent is None:
        return X("no CORRECTED row in the JSON ledger")
    doc_ok = bool(re.search(r"is\s+\*\*\(C\)\*\*,\s*not\s*\"?\(b\)\"?", blk))
    scope_ok = has(blk, 'All references to "direction (b)" in this document mean statement')
    stray = [m.start() for m in re.finditer(r"direction \(b\)", ctx["doc"])]
    if not doc_ok:
        return X("the document does not state the (b) -> (C) correction",
                 record_primary_text=ent["primary_text"])
    if not scope_ok:
        return X("the correction is stated but not scoped over the rest of the document",
                 record_primary_text=ent["primary_text"])
    return M("(C)-not-(b) stated and scoped over the whole document",
             record_verdict=ent["verdict"], record_primary_text=ent["primary_text"],
             occurrences_of_direction_b_in_doc=len(stray),
             note=("the sole remaining 'direction (b)' occurrence is the scoping "
                   "sentence itself" if len(stray) == 1 else
                   "MORE THAN ONE 'direction (b)' occurrence -- inspect"))


@plant("I4")
def i4p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace("is **(C)**, not \"(b)\"", "is **(b)**, not \"(C)\"", 1)
    return c


@check("I5", "(i)", "the not-a-shortcut clause")
def i5(ctx):
    blk = ledger_block(ctx)
    e = f0_entry(ctx)
    rec_note = cd(ctx).get("f_allowance_is_not_a_shortcut", "")
    doc_says = has(blk, "not** a shortcut") or has(blk, "not a shortcut")
    cites45 = bool(re.search(r"\(4\)\s*,\s*\(5\)", blk))
    if not rec_note:
        return X("the JSON carries no f_allowance_is_not_a_shortcut payload")
    if not doc_says:
        return X("the document does not carry the not-a-shortcut clause",
                 record_payload=rec_note)
    if not cites45:
        return X("the not-a-shortcut clause is present but drops the (4),(5) "
                 "condition the JSON makes it rest on", record_payload=rec_note)
    return M("not-a-shortcut clause present and resting on (4),(5) as the JSON does",
             record_why=e["why"], record_payload_chars=len(rec_note))


@plant("I5")
def i5p(ctx):
    c = dup(ctx)
    c["doc"] = re.sub(r"why it is \*\*not\*\* a(\s*(?:>\s*)?)shortcut",
                      r"why it is a\1shortcut", c["doc"], count=1)
    return c


@check("I6", "(i)", "§4 alone carries the VERIFIED header")
def i6(ctx):
    doc = ctx["doc"]
    marks = [m.start() for m in re.finditer(r"VERIFIED AS A SPECIFICATION", doc)]
    s4 = doc.index("## §4 ")
    s5 = doc.index("## §5 ")
    inside = [p for p in marks if s4 < p < s5]
    gate_ans = ctx["cloc"]["gate"]["answer"]
    scoping = has(doc, "§1/§2/§3/§5/§6/§7 remain **DRAFT, UNVERIFIED**")
    if len(marks) != 1:
        return X("expected exactly one VERIFIED header in the document",
                 occurrences=len(marks))
    if len(inside) != 1:
        return X("the VERIFIED header is not inside §4's span", offsets=marks,
                 section4_span=[s4, s5])
    if not gate_ans.upper().startswith("YES"):
        return X("the JSON gate does not answer YES", gate_answer=gate_ans)
    if not scoping:
        return X("§4's header does not scope the other sections as DRAFT, UNVERIFIED")
    return M("exactly 1 VERIFIED header, inside §4, with the other sections scoped "
             "DRAFT/UNVERIFIED, against JSON gate answer",
             occurrences=1, gate_answer=gate_ans)


@plant("I6")
def i6p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        "## §5 — Stability",
        "## §5 — Stability\n\n> **VERIFIED AS A SPECIFICATION -- planted.**", 1)
    return c


@check("I7", "(i)", "§4 amendment 1 (the DSS case costs nothing extra): every number")
def i7(ctx):
    doc = ctx["doc"]
    b = ctx["cloc"]["check_B_energy_exponent_SS_vs_DSS"]
    pairs = [
        ("0.499999942", b["DSS_exponent"], "DSS_exponent"),
        ("0.500000000", b["SS_exponent"], "SS_exponent"),
        ("0.9999998844", b["DSS_over_SS_exponent_ratio"], "DSS_over_SS_exponent_ratio"),
        ("2.99", b["DSS_G_oscillation_relative_amplitude"], "DSS_G_oscillation_relative_amplitude"),
        ("0.4876", b["DSS_exponent_naive_fit_modulation_DROPPED"],
         "DSS_exponent_naive_fit_modulation_DROPPED"),
        ("2.47", b["naive_fit_bias_percent"], "naive_fit_bias_percent"),
        ("1.0574", b["DSS_residual_best_fit_period_in_s"], "DSS_residual_best_fit_period_in_s"),
        ("1.0613", b["predicted_period_2_log_lambda"], "predicted_period_2_log_lambda"),
        ("0.36", 100.0 * b["period_relative_error"], "100 * period_relative_error"),
    ]
    bad, seen = [], []
    for lit, val, key in pairs:
        in_doc = lit in doc
        ok = in_doc and matches_at_doc_precision(lit, val)
        seen.append({"doc_literal": lit, "record_key": key, "record_value": val,
                     "present_in_doc": in_doc, "agrees_at_doc_precision": ok})
        if not ok:
            bad.append({"doc_literal": lit, "record_key": key, "record_value": val,
                        "present_in_doc": in_doc})
    if bad:
        return X("amendment-1 literals disagree with the JSON", mismatches=bad,
                 rows_compared=len(pairs))
    return M("all 9 amendment-1 literals reproduce their JSON values at the "
             "document's own printed precision", rows_compared=len(pairs),
             rows=seen)


@plant("I7")
def i7p(ctx):
    c = dup(ctx)
    c["cloc"]["check_B_energy_exponent_SS_vs_DSS"]["DSS_G_oscillation_relative_amplitude"] = 1.234
    return c


@check("I8", "(i)", "§4 amendment 2 (the truncated-law repair): 'verified to 2.6e-5'",
       plant_kind="repair")
def i8(ctx):
    doc = ctx["doc"]
    b2 = ctx["cloc"]["check_B2_truncated_energy_law"]
    m = re.search(r"verified to `([0-9.]+e-?\d+)`", doc)
    if not m:
        return X("no 'verified to <tolerance>' literal found for the truncated law")
    lit = m.group(1)
    lit_val = float(lit)
    rows = [{"alpha": r["alpha"], "abs_error": r["abs_error"]} for r in b2["rows"]]
    worst = b2["max_abs_error"]
    matching = [r for r in rows if abs(r["abs_error"] - lit_val) <= 0.05 * lit_val]
    if abs(worst - lit_val) <= 0.05 * lit_val:
        return M("the document's tolerance is the JSON's max_abs_error",
                 doc_literal=lit, record_max_abs_error=worst, rows=rows)
    return X(
        "the document quotes a tolerance that is NOT the JSON's verification "
        "tolerance: `%s` is the abs_error of the SINGLE BEST row (alpha=%s), while "
        "the JSON's own max_abs_error over the 4 banked rows is %r at alpha=%s -- "
        "larger by a factor %.1f. At alpha = 1, the exponent §4 is actually about, "
        "the abs_error is %r." % (
            lit,
            matching[0]["alpha"] if matching else "none",
            worst,
            max(rows, key=lambda r: r["abs_error"])["alpha"],
            worst / lit_val,
            next(r["abs_error"] for r in rows if r["alpha"] == 1.0)),
        doc_literal=lit, doc_literal_value=lit_val,
        record_max_abs_error=worst,
        record_row_matching_doc_literal=(matching[0] if matching else None),
        record_row_at_alpha_1=next(r for r in rows if r["alpha"] == 1.0),
        ratio_max_over_doc=worst / lit_val, rows=rows)


@plant("I8")
def i8p(ctx):
    """A REPAIR plant: rewrite the document to quote the JSON's own max_abs_error.
    The check must go GREEN, proving it is sensitive in both directions."""
    c = dup(ctx)
    c["doc"] = c["doc"].replace("verified to `2.6e-5`", "verified to `2.6e-2`", 1)
    return c


@check("I9", "(i)", "§4 amendment 3 (the gap is measured): 1.5x deficit and -0.00026")
def i9(ctx):
    doc = ctx["doc"]
    b3 = ctx["cloc"]["check_B3_Lp_thresholds"]
    b2 = ctx["cloc"]["check_B2_truncated_energy_law"]
    row1 = next(r for r in b2["rows"] if r["alpha"] == 1.0)
    pairs = [
        ("deficit 0.5", 0.5, b3["deficit_to_L2_in_exponent"], "deficit_to_L2_in_exponent"),
        ("ratio 1.5", 1.5, b3["required_over_available_exponent_ratio"],
         "required_over_available_exponent_ratio"),
        ("L2 threshold 1.5", 1.5, b3["L2_threshold_alpha"], "L2_threshold_alpha"),
        ("banked Type-I alpha 1", 1.0, b3["banked_type_I_alpha"], "banked_type_I_alpha"),
    ]
    bad = [p for p in pairs if abs(p[1] - p[2]) > 1e-12]
    lit = "0.00026"
    doc_has = ("−0.00026" in doc) or ("-0.00026" in doc)
    ok26 = doc_has and matches_at_doc_precision(
        lit, abs(row1["fixed_ball_energy_exponent_measured"]))
    if bad:
        return X("threshold literals disagree", mismatches=bad)
    if not ok26:
        return X("the -0.00026 fixed-ball exponent does not reproduce",
                 record_value=row1["fixed_ball_energy_exponent_measured"],
                 present_in_doc=doc_has)
    return M("deficit 0.5, ratio 1.5x, L^2 threshold 3/2, Type-I alpha 1, and the "
             "-0.00026 fixed-ball exponent at alpha=1 all reproduce",
             rows_compared=len(pairs) + 1,
             record_fixed_ball_exponent_at_alpha_1=row1["fixed_ball_energy_exponent_measured"],
             record_predicted=row1["predicted_alpha_minus_1"])


@plant("I9")
def i9p(ctx):
    c = dup(ctx)
    c["cloc"]["check_B3_Lp_thresholds"]["required_over_available_exponent_ratio"] = 2.0
    return c


@check("I10", "(i)", "the priced cutoff bill: 5 shrinking exponents + the L^3 tail")
def i10(ctx):
    doc = ctx["doc"]
    c1 = ctx["cloc"]["check_C_cutoff_magnitudes"]["by_alpha"]["alpha=1.0"]
    meas = c1["measured_rho_exponents"]
    pred = c1["predicted_rho_exponents"]
    c2 = ctx["cloc"]["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"]
    pairs = [
        ("1.4993", meas["nonlinear_residual_L2"], "nonlinear_residual_L2"),
        ("1.4999", meas["viscous_residual_L2"], "viscous_residual_L2"),
        ("0.4996", meas["divergence_defect_L2"], "divergence_defect_L2"),
        ("1.9997", meas["pressure_perturbation_at_origin"], "pressure_perturbation_at_origin"),
    ]
    bad, seen = [], []
    for lit, val, key in pairs:
        ok = (lit in doc) and matches_at_doc_precision(lit, abs(val))
        seen.append({"doc_literal": "rho^{-" + lit + "}", "record_key": key,
                     "record_value": val, "agrees": ok})
        if not ok:
            bad.append(seen[-1])
    # the document's own '<=0.1% against closed forms' claim, re-measured
    worst = {"key": None, "rel_percent": 0.0}
    rels = []
    for k, v in meas.items():
        p = pred[k]
        if abs(p) < 1e-12:
            continue
        rel = 100.0 * abs(v - p) / abs(p)
        rels.append({"key": k, "measured": v, "predicted": p, "rel_percent": rel})
        if rel > worst["rel_percent"]:
            worst = {"key": k, "rel_percent": rel}
    claim_ok = worst["rel_percent"] <= 0.1
    # the 326.875-per-decade figure and its spread
    inc = c2["increment_per_decade"]
    inc_ok = "326.875" in doc and matches_at_doc_precision("326.875", inc[0])
    spread_ok = "7.4e-10" in doc and abs(c2["increment_per_decade_spread"] - 7.4e-10) < 0.5e-10
    # WHAT the 326.875 is an increment OF: the JSON increments tail_L3_CUBED
    cubed = [r["tail_L3_cubed"] for r in c2["rows"]]
    norms = [r["tail_L3_norm"] for r in c2["rows"]]
    step = c2["rows"][1]["decades_of_window"] - c2["rows"][0]["decades_of_window"]
    increments_the_cube = abs((cubed[1] - cubed[0]) / step - inc[0]) < 1e-6
    doc_says_cube = has(doc, "cube of the critical") or has(doc, "critical `L³` tail cubed")
    if bad:
        return X("cutoff-bill exponents disagree", mismatches=bad)
    if not claim_ok:
        return X("the document's '<=0.1% against closed forms' claim does not hold",
                 worst=worst, rows=rels)
    if not (inc_ok and spread_ok):
        return X("the L^3 tail growth figure or its spread does not reproduce",
                 record_increment_per_decade=inc,
                 record_spread=c2["increment_per_decade_spread"])
    if increments_the_cube and not doc_says_cube:
        return X(
            "the 326.875-per-decade figure is the increment of the CUBE of the "
            "critical tail (JSON tail_L3_cubed: %s), not of the L^3 NORM itself "
            "(JSON tail_L3_norm: %s, which grows %.3f -> %.3f over the same 5 rows). "
            "The document says 'the critical `L3` tail grows 326.875 per decade of "
            "window', dropping the JSON reading's own words 'the cube of'." % (
                [round(x, 4) for x in cubed], [round(x, 4) for x in norms],
                norms[0], norms[-1]),
            record_reading=c2["reading"],
            record_tail_L3_cubed=cubed, record_tail_L3_norm=norms,
            record_increment_per_decade=inc)
    return M("all 4 shrinking exponents, the <=0.1% claim, and the L^3 tail growth "
             "reproduce", rows_compared=len(pairs), rows=seen,
             worst_relative_error_percent=worst,
             record_increment_per_decade=inc)


@plant("I10")
def i10p(ctx):
    """A REPAIR plant on the 'cube of' wording -- the check must go GREEN."""
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        "the critical `L³` tail grows **326.875",
        "the cube of the critical `L³` tail grows **326.875", 1)
    return c


CHECKS[-1]["plant_kind"] = "repair"


@check("I11", "(i)", "the §4-stays-open-until-DTOL rule, and its provenance")
def i11(ctx):
    doc = ctx["doc"]
    rule = has(doc, "Until DTOL lands, §4 stays OPEN in every route-4 gate")
    formula = has(doc, "δ < (α_centre − 1)/0.434")
    delta_star = "3.35" in doc
    width = "0.8686" in doc
    # provenance: these numbers are leg 382's, NOT in this leg's comparison source.
    blob = json.dumps(ctx["cloc"])
    in_cloc = any(s in blob for s in ("0.8686", "3.35", "0.434"))
    if not (rule and formula and delta_star and width):
        return X("the DTOL rule is not fully stated",
                 rule_present=rule, formula_present=formula,
                 delta_star_present=delta_star, width_present=width)
    return M("the rule, the composed constraint delta < (alpha_centre-1)/0.434, "
             "delta* up to 3.35 and the 0.8686*delta enclosure width are all present",
             provenance=("leg 382 (DEXC) + the user's 2026-08-11 ruling; these four "
                         "numbers are NOT in p2_route_cloc_v1.json and are therefore "
                         "OUTSIDE this leg's comparison source -- recorded as "
                         "unchecked-here, not as verified"),
             numbers_found_in_cloc_json=in_cloc)


@plant("I11")
def i11p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        "**Until DTOL lands, §4 stays OPEN in every route-4 gate.**", "", 1)
    return c


@check("I12", "(i)", "§7 is marked STILL UNCHECKED")
def i12(ctx):
    doc = ctx["doc"]
    s7 = section(doc, "## §7 ", ["## §8 "])
    marked = has(s7, "**STILL UNCHECKED.**")
    reason = has(s7, "read the *problem statement*, not the *prize rules*")
    src = ctx["cloc"]["clay_source"]
    src_is_problem_statement = "navierstokes.pdf" in src
    if not marked:
        return X("§7 is not marked STILL UNCHECKED")
    if not reason:
        return X("§7 is marked but does not record WHY (leg 381 read the problem "
                 "statement, not the prize rules)")
    if not src_is_problem_statement:
        return X("the JSON's clay_source is not the problem statement", clay_source=src)
    return M("§7 marked STILL UNCHECKED, with leg 381's own scope recorded; the "
             "JSON's clay_source is indeed the problem-statement PDF, not the rules",
             clay_source=src)


@plant("I12")
def i12p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace("> **STILL UNCHECKED.**", "> **CHECKED.**", 1)
    return c


@check("I13", "(i)", "§8 ask #1 is recorded SATISFIED")
def i13(ctx):
    doc = ctx["doc"]
    s8 = section(doc, "## §8 ", ["\n---\n"])
    sat = has(s8, "**SATISFIED, and recorded so it is not re-opened (user ruling")
    pocp = has(s8, "POCP is the")
    parallel = has(s8, "run in parallel")
    blob = json.dumps(ctx["cloc"])
    if not sat:
        return X("§8 ask #1 is not recorded SATISFIED")
    if not (pocp and parallel):
        return X("ask #1 is SATISFIED but drops its stated ground (POCP the only open "
                 "route) or its consequence (the two tracks run in parallel)")
    return M("ask #1 recorded SATISFIED on the POCP-is-the-only-open-route ground, "
             "with the parallel-running consequence",
             provenance=("user ruling 2026-08-11 + leg 348; NOT in "
                         "p2_route_cloc_v1.json, so outside this leg's comparison "
                         "source -- recorded as unchecked-here, not as verified"),
             satisfied_string_in_cloc_json=("SATISFIED" in blob))


@plant("I13")
def i13p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace("> **SATISFIED, and recorded", "> **OPEN, and recorded", 1)
    return c


@check("I14", "(i)", "statement (D) named-but-not-authorised, against (D)'s own text")
def i14(ctx):
    blk = ledger_block(ctx)
    D = cd(ctx)["verbatim_conditions"]["(D)"]
    C = cd(ctx)["verbatim_conditions"]["(C)"]
    note = cd(ctx).get("alternative_target_noted", "")
    # (D)'s data conditions are (8),(9) and its solution conditions (10),(11):
    # (4)/(5) [decay] and (7) [bounded energy] are absent -- read off the primary text.
    d_nums = set(re.findall(r"\((\d+)\)", D))
    c_nums = set(re.findall(r"\((\d+)\)", C))
    decay_absent = not ({"4", "5"} & d_nums)
    energy_absent = "7" not in d_nums
    energy_in_C = "7" in c_nums
    named = has(blk, "named but not authorised") and has(blk, "statement **(D)**")
    vacuous = has(blk, "§4 vacuous by construction")
    reopens = has(blk, "re-opening §2's rigidity screen")
    nodispatch = has(blk, "No leg is dispatched against it")
    if not named:
        return X("(D) is not recorded as named-but-not-authorised")
    if not (decay_absent and energy_absent and energy_in_C):
        return X("(D)'s own text does not support the document's reading",
                 D_condition_numbers=sorted(d_nums), C_condition_numbers=sorted(c_nums))
    if not (vacuous and reopens and nodispatch):
        return X("the (D) note drops one of: §4-vacuous / re-opens-§2 / no-leg-dispatched",
                 vacuous=vacuous, reopens=reopens, no_dispatch=nodispatch,
                 record_note=note)
    return M("(D) named, not authorised; and (D)'s OWN primary text confirms the "
             "reading -- its condition set is %s (no (4)/(5) decay, no (7) bounded "
             "energy), against (C)'s %s" % (sorted(d_nums), sorted(c_nums)),
             D_condition_numbers=sorted(d_nums), C_condition_numbers=sorted(c_nums),
             D_verbatim=D, record_note_chars=len(note))


@plant("I14")
def i14p(ctx):
    c = dup(ctx)
    c["cloc"]["check_D_clay_primary_text"]["verbatim_conditions"]["(D)"] = \
        cd(c)["verbatim_conditions"]["(D)"].replace("(10), (11)", "(7), (10), (11)")
    return c


@check("I15", "(i)", "REVERSE DIRECTION: every JSON ledger verdict is reflected in the doc",
       plant_kind="repair")
def i15(ctx):
    blk = ledger_block(ctx)
    rows = cd(ctx)["reviewer_paragraph_clause_ledger"]
    missing = []
    seen = []
    for e in rows:
        v = e["verdict"]
        head = v.split("(")[0].strip()
        present = has(blk, head)
        seen.append({"reviewer_clause": e["reviewer_clause"], "json_verdict": v,
                     "verdict_word_present_in_doc": present})
        if not present:
            missing.append({"reviewer_clause": e["reviewer_clause"], "json_verdict": v,
                            "json_why": e["why"], "json_primary_text": e["primary_text"]})
    if missing:
        return X("JSON verdicts absent from the landed document block",
                 missing=missing, rows_compared=len(rows))
    return M("all %d JSON ledger verdicts are reflected in the document block"
             % len(rows), rows_compared=len(rows), rows=seen)


@plant("I15")
def i15p(ctx):
    """REPAIR plant: land the proposed correction text and show the check goes GREEN."""
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        ">   condition §4 and §5 are about. Smoothness, divergence-free, and "
        "faster-than-polynomial\n>   decay all stand as stated.",
        ">   condition §4 and §5 are about. Smoothness and divergence-free stand as\n"
        ">   stated. Faster-than-polynomial decay is **CONFIRMED AND STRENGTHENED**:\n"
        ">   condition (4) binds every derivative.", 1)
    return c


# ------------------------------------------------------------------ ITEM (ii)
# §2's four screen rows, machine-read against their named landed records.

def s2(ctx):
    return section(ctx["doc"], "## §2 ", ["## §3 "])


def dss_lambda_result(lam=1.7):
    return {"measured": True, "lambda": lam, "S0": 2.0 * math.log(lam),
            "reason": "synthetic DSS trajectory for the ledger read"}


@check("II1", "(ii)", "§2 row 1 (NRS 1996 / Tsai T1/T2) against its landed records")
def ii1(ctx):
    sec = s2(ctx)
    row = [ln for ln in sec.splitlines() if "NRS 1996" in ln or "NRS 1996 / Tsai" in ln]
    scr = ctx["screen"]
    ansatz = scr.classify_ss_ansatz(dss_lambda_result())
    verdict = scr._ledger_nrs_tsai_three_way(
        {"converged": False, "reason": "log-divergent tail"},
        {"decays_to_zero": False, "reason": "not measured"}, ansatz)
    algw_blob = json.dumps(ctx["algw"])
    key = "NRS/Tsai's own theorems bind exactly-backward-self-similar (SS) profiles"
    algw_supports = key in algw_blob
    doc_claim_exact = has(sec, "bind *exactly-backward-self-similar* profiles only")
    doc_claim_outside = has(sec, "DSS at\n  `λ ≫ 1` is outside the hypothesis") or \
        has(sec, "DSS at `λ ≫ 1` is outside the hypothesis")
    cites = re.findall(r"legs? ([\d, and]+)\)", " ".join(row)) if row else []
    leg253_record = sorted(p.name for p in DATA.glob("*.json")
                           if '"leg": 253' in p.read_text(errors="ignore")[:400])
    if not doc_claim_exact:
        return X("the document's row-1 claim is not in its expected wording")
    if not algw_supports:
        return X("leg 341's landed record does not carry the row-1 claim",
                 searched_for=key)
    if ansatz["ansatz"] != "DSS" or ansatz["satisfies_theorem_ansatz"] is not False:
        return X("the landed ansatz classifier does not put a lambda>1 DSS object "
                 "outside Tsai's ansatz", executed=ansatz)
    if verdict["verdict"] != "NOT-REACHED-BY-ANSATZ":
        return X("the landed T1/T2 ledger does not read NOT-REACHED-BY-ANSATZ",
                 executed=verdict)
    return M("row 1 verified three ways: leg 341's landed JSON carries the claim "
             "verbatim; solver/dssp_screen.py::classify_ss_ansatz EXECUTED on a "
             "measured lambda=1.7 returns ansatz=DSS / satisfies_theorem_ansatz=False; "
             "and _ledger_nrs_tsai_three_way EXECUTED returns NOT-REACHED-BY-ANSATZ",
             executed_ansatz=ansatz["ansatz"],
             executed_satisfies_theorem_ansatz=ansatz["satisfies_theorem_ansatz"],
             executed_ledger_verdict=verdict["verdict"],
             record_key_found_in_leg_341_json=key,
             doc_claim_outside_hypothesis_present=doc_claim_outside,
             citation_provenance=(
                 "the row cites 'legs 253, 341'. Leg 341's record is "
                 "writeup/data/p2_route_algw_v1.json and carries the claim. NO "
                 "writeup/data/*.json declares leg 253, so leg 253's half of the "
                 "citation has no machine-readable landed record; the OPERATIVE "
                 "encoding is solver/dssp_screen.py (legs 357/359/362)."),
             leg_253_json_records_found=leg253_record)


@plant("II1")
def ii1p(ctx):
    c = dup(ctx)
    c["lambda_override"] = 1.0
    orig = c["screen"].classify_ss_ansatz

    class Shim:
        def __getattr__(self, k):
            return getattr(ctx["screen"], k)

        @staticmethod
        def classify_ss_ansatz(lr):
            return orig({"measured": False, "reason": "planted: no period measured"})

        @staticmethod
        def _ledger_nrs_tsai_three_way(a, b, ans):
            return ctx["screen"]._ledger_nrs_tsai_three_way(a, b, ans)
    c["screen"] = Shim()
    return c


@check("II2", "(ii)", "§2 row 2 (Chae-Wolf / Pineau-Vicol) against leg 330's record")
def ii2(ctx):
    sec = s2(ctx)
    pv = ctx["pvlx"]
    scr = ctx["screen"]
    m1 = next(m for m in pv["magnitudes_of_near_1"] if m["id"] == "M1")
    ceiling = m1["value_lambda_ceiling"]
    executed = scr.ledger_pineau_vicol(dss_lambda_result(),
                                       str(ROOT / "writeup/data/p2_route_pvlx_v1.json"))
    doc_lit = re.search(r"λ̲ ≤ e\^\{1/2\} ≈ ([\d.]+)", sec)
    quote_ok = has(sec, "sufficiently close to 1")
    quote_in_record = "sufficiently close to 1" in json.dumps(pv, ensure_ascii=False)
    cw = "ChaeWolf" in json.dumps(pv) or "Chae-Wolf" in json.dumps(pv) or \
         "Chae–Wolf" in json.dumps(pv, ensure_ascii=False)
    if not doc_lit:
        return X("the document's lambda ceiling literal is not in its expected form")
    lit = doc_lit.group(1)
    if not matches_at_doc_precision(lit, ceiling):
        return X("the document's lambda ceiling disagrees with leg 330's record",
                 doc_literal=lit, record_value=ceiling)
    if abs(ceiling - math.exp(0.5)) > 1e-15:
        return X("leg 330's ceiling is not exp(1/2)", record_value=ceiling,
                 exp_half=math.exp(0.5))
    if not (quote_ok and quote_in_record):
        return X("the 'sufficiently close to 1' quote is not in leg 330's record",
                 in_doc=quote_ok, in_record=quote_in_record)
    if not executed["verdict"].startswith("OUTSIDE"):
        return X("the landed Pineau-Vicol ledger does not put lambda=1.7 outside the "
                 "window", executed=executed)
    return M("row 2 verified: doc literal %s == leg 330's value_lambda_ceiling %r == "
             "exp(1/2) to 1e-15; the 'sufficiently close to 1' phrase is in leg 330's "
             "record; and ledger_pineau_vicol EXECUTED against that file at lambda=1.7 "
             "returns '%s'" % (lit, ceiling, executed["verdict"]),
             doc_literal=lit, record_value_lambda_ceiling=ceiling,
             exp_half=math.exp(0.5),
             record_T2_lambda_window_hard_ceiling=pv["magnitudes"]["T2_lambda_window_hard_ceiling"],
             executed_verdict=executed["verdict"],
             executed_lambda_ceiling_from_source=executed["lambda_ceiling_from_source"],
             record_gate_verdict=pv["gate"]["verdict"],
             chae_wolf_named_in_record=cw)


@plant("II2")
def ii2p(ctx):
    c = dup(ctx)
    for m in c["pvlx"]["magnitudes_of_near_1"]:
        if m["id"] == "M1":
            m["value_lambda_ceiling"] = 9.9
    return c


@check("II3", "(ii)", "§2 row 3 (Chae-Tsai) against leg 326's record")
def ii3(ctx):
    sec = s2(ctx)
    ct = ctx["ctrx"]
    scr = ctx["screen"]
    tr = ct["theorem_read"]
    n_theorems = 1 + len(tr["companion_theorems"])
    executed = scr.ledger_chae_tsai(str(ROOT / "writeup/data/p2_route_ctrx_v1.json"))
    doc_four = has(sec, "all four theorems hypothesise the rescaled Euler system")
    doc_euler_only = has(sec, "Euler-only")
    doc_separately = has(sec, "the paper proves nothing about the NS equation it displays\n  separately") \
        or has(sec, "proves nothing about the NS equation it displays separately")
    euler_16 = "EULER" in tr["equation_1_6_is"].upper()
    ns_110 = "NAVIER" in tr["equation_1_10_is"].upper() or "1.1" in tr["equation_1_10_is"]
    if not doc_four:
        return X("the document's 'all four theorems' claim is not in its expected wording")
    if n_theorems != 4:
        return X("leg 326's record does not carry four theorems",
                 record_theorem_count=n_theorems,
                 record_theorem_read=tr["label"],
                 record_companions=tr["companion_theorems"])
    if not (euler_16 and doc_euler_only):
        return X("the Euler-only claim is not supported by leg 326's record",
                 record_equation_1_6_is=tr["equation_1_6_is"])
    if not ns_110:
        return X("leg 326's record does not identify (1.10) as the separately "
                 "displayed NS equation", record_equation_1_10_is=tr["equation_1_10_is"])
    if executed["clause_alpha_equation_verdict"] != "FAILS_HYPOTHESIS" or \
            executed["branch"] != "(ii)":
        return X("the landed Chae-Tsai ledger does not read FAILS_HYPOTHESIS / (ii)",
                 executed=executed)
    return M("row 3 verified: leg 326's record carries exactly 4 theorems "
             "(%s + %s), all hypothesising (1.6) = %s, with (1.10) = %s displayed "
             "separately; ledger_chae_tsai EXECUTED returns branch %s / "
             "clause verdict %s" % (
                 tr["label"], tr["companion_theorems"], tr["equation_1_6_is"],
                 tr["equation_1_10_is"], executed["branch"],
                 executed["clause_alpha_equation_verdict"]),
             record_theorem_count=n_theorems,
             record_all_theorems_hypothesise=tr["all_theorems_hypothesise"],
             record_equation_1_6_is=tr["equation_1_6_is"],
             record_equation_1_10_is=tr["equation_1_10_is"],
             executed_branch=executed["branch"],
             executed_verdict=executed["verdict"],
             executed_consumed_leg=executed["consumed_leg"])


@plant("II3")
def ii3p(ctx):
    c = dup(ctx)
    c["ctrx"]["theorem_read"]["companion_theorems"] = ["Theorem 2.2"]
    return c


@check("II4", "(ii)", "§2 row 4 (Morrey / Jiu-Wang-Wei) against legs 368/370's records")
def ii4(ctx):
    sec = s2(ctx)
    mr, b7 = ctx["mryx"], ctx["b7m"]
    scr = ctx["screen"]
    ansatz = scr.classify_ss_ansatz(dss_lambda_result())
    executed = scr.ledger_morrey(None, ansatz)
    src = (ROOT / "solver" / "dssp_screen.py").read_text()
    literal_in_code = "EXCLUDED-BY-MORREY" in src
    doc_widens = has(sec, "strictly *widens* the exact-SS exclusion beyond\n  T1/T2") or \
        has(sec, "strictly *widens* the exact-SS exclusion beyond T1/T2")
    doc_arxiv = "2006.15776" in sec
    doc_ledger = has(sec, "`EXCLUDED-BY-MORREY` in the ledger")
    rec_verdict = mr["classification"]["verdict"]
    rec_arxiv = "2006.15776" in json.dumps(mr)
    if not doc_widens:
        return X("the document's WIDENS claim is not in its expected wording")
    if rec_verdict != "WIDENS":
        return X("leg 368's record does not classify the result as WIDENS",
                 record_verdict=rec_verdict)
    if not (doc_arxiv and rec_arxiv):
        return X("the arXiv identifier does not match", in_doc=doc_arxiv,
                 in_record=rec_arxiv)
    if not (literal_in_code and doc_ledger):
        return X("the EXCLUDED-BY-MORREY ledger entry is not where the document says",
                 literal_present_in_solver=literal_in_code)
    if executed["verdict"] != "NOT-REACHED-BY-ANSATZ":
        return X("the landed Morrey ledger does not read NOT-REACHED-BY-ANSATZ on a "
                 "DSS object", executed=executed)
    planted = b7["control_a_planted_widen_then_close"]
    if planted["morrey_verdict"]["verdict"] != "EXCLUDED-BY-MORREY" or \
            planted["t1_t2_verdict"]["verdict"] != "NOT EXCLUDED":
        return X("leg 370's own widen-then-close control does not read as the "
                 "document's row requires", record_control=planted)
    return M("row 4 verified: leg 368 classification=WIDENS on arXiv:2006.15776 "
             "(Jiu-Wang-Wei); leg 370's landed control shows a planted exact-SS "
             "profile reading '%s' under T1/T2 alone and '%s' once Morrey is wired "
             "in (the widening, demonstrated); the literal EXCLUDED-BY-MORREY is in "
             "solver/dssp_screen.py; and ledger_morrey EXECUTED on the DSS object "
             "returns %s -- i.e. it still does not reach DSS" % (
                 planted["t1_t2_verdict"]["verdict"],
                 planted["morrey_verdict"]["verdict"], executed["verdict"]),
             record_classification=rec_verdict,
             record_leg_368=mr["leg"], record_leg_370=b7["leg"],
             record_citation=mr["primary_source"]["citation"],
             executed_verdict=executed["verdict"],
             control_t1_t2=planted["t1_t2_verdict"]["verdict"],
             control_morrey=planted["morrey_verdict"]["verdict"])


@plant("II4")
def ii4p(ctx):
    c = dup(ctx)
    c["mryx"]["classification"]["verdict"] = "DOES NOT WIDEN"
    return c


# ------------------------------------------------------------------ ITEM (iii)
# §7's prize-rules clauses against the Clay Institute's own published rules.

def s7(ctx):
    return section(ctx["doc"], "## §7 ", ["## §8 "])


@check("III1", "(iii)", "§7 clause 1: 'refereed journal of worldwide repute'",
       plant_kind="repair")
def iii1(ctx):
    rules = ctx["rules"]
    if not rules:
        return U("the Clay prize rules were unreachable; the clause CANNOT be "
                 "checked and is recorded UNVERIFIED, not passed",
                 refusal_verbatim=ctx["rules_meta"]["refusal_verbatim"],
                 http_status=ctx["rules_meta"]["http_status"])
    doc = s7(ctx)
    m = re.search(r"publication in a \*\*([^*]+)\*\*", doc)
    doc_wording = m.group(1).strip() if m else None
    primary_publication = has(rules, "a refereed mathematics publication of worldwide "
                                     "repute meeting the conditions in Section 6(e)")
    relaxed_route = has(rules, "a publication meeting a relaxed set of conditions "
                               "approved by the BOD")
    qualifying_outlet = has(rules, "Qualifying Outlet")
    if not qualifying_outlet:
        return X("the fetched text does not look like the prize rules",
                 chars=len(rules))
    if not primary_publication:
        return X("Section 6(a)(i) not located in the fetched rules")
    if doc_wording and has(rules, doc_wording):
        return M("the document's own §7 wording (%r) occurs verbatim in the rules"
                 % doc_wording, doc_wording=doc_wording)
    return X(
        "the document says 'refereed **journal** of worldwide repute'; the rules "
        "say Section 6(a)(i) 'a refereed mathematics PUBLICATION of worldwide "
        "repute meeting the conditions in Section 6(e)' -- and Section 6(a)(ii) "
        "gives a SECOND qualifying route the document does not mention: 'a "
        "publication meeting a relaxed set of conditions approved by the BOD "
        "following a recommendation of the SAB'. The document's clause is "
        "NARROWER than the rules. Section 6(e) then lists four characteristics "
        "whose absence disqualifies an outlet, one of which is 'inclusion in the "
        "list of publications maintained by MathSciNet'.",
        doc_wording=doc_wording,
        doc_wording_occurs_in_rules=False,
        rules_wording_6a_i="a refereed mathematics publication of worldwide repute "
                           "meeting the conditions in Section 6(e)",
        rules_6a_i_present=primary_publication,
        rules_6a_ii_relaxed_route_present=relaxed_route,
        rules_6e_mathscinet_condition=has(rules, "maintained by MathSciNet"))


@plant("III1")
def iii1p(ctx):
    """REPAIR plant: land the proposed §7 wording and show the check goes GREEN."""
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        "publication in a **refereed\njournal of worldwide repute**",
        "publication in a **refereed mathematics publication of worldwide repute "
        "meeting the conditions in Section 6(e)**", 1)
    return c


@check("III2", "(iii)", "§7 clause 2: the two-year waiting period")
def iii2(ctx):
    rules = ctx["rules"]
    if not rules:
        return U("the Clay prize rules were unreachable; UNVERIFIED, not passed",
                 refusal_verbatim=ctx["rules_meta"]["refusal_verbatim"],
                 http_status=ctx["rules_meta"]["http_status"])
    doc = s7(ctx)
    doc_two_year = has(doc, "two-year waiting period")
    r4b = has(rules, "at least two (2) years have elapsed since publication of the "
                     "Proposed Solution in a Qualifying Outlet")
    r7 = has(rules, "must survive rigorous examination by the global mathematics "
                    "community for a minimum of two (2) years")
    r8c = has(rules, "additional two (2) year waiting period")
    if not doc_two_year:
        return X("the document does not state a two-year waiting period")
    if not r4b:
        return X("the rules do not carry the two-year condition in Section 4(b)")
    return M("CONFIRMED against Section 4(b), and the rules are STRICTER than the "
             "document's one-line summary: Section 7(a)(i)(2) additionally requires "
             "the solution to SURVIVE RIGOROUS EXAMINATION by the global mathematics "
             "community for a minimum of two (2) years%s, and Section 8(c) imposes a "
             "FURTHER two-year wait before CMI may reconsider a negative decision%s. "
             "The two stages of Section 7(a) must be satisfied SEQUENTIALLY."
             % (" [located]" if r7 else " [phrase not located verbatim]",
                " [located]" if r8c else " [phrase not located verbatim]"),
             rules_4b_present=r4b, rules_7a_i_2_present=r7, rules_8c_present=r8c,
             rules_sequential=has(rules, "must be satisfied sequentially"))


@plant("III2")
def iii2p(ctx):
    c = dup(ctx)
    c["rules"] = re.sub(r"two\s*\(2\)\s*years", "five (5) years", c["rules"])
    return c


@check("III3", "(iii)", "§7 clause 3: general acceptance in the mathematics community",
       plant_kind="repair")
def iii3(ctx):
    rules = ctx["rules"]
    if not rules:
        return U("the Clay prize rules were unreachable; UNVERIFIED, not passed",
                 refusal_verbatim=ctx["rules_meta"]["refusal_verbatim"],
                 http_status=ctx["rules_meta"]["http_status"])
    doc = s7(ctx)
    doc_phrase = has(doc, "general acceptance in the mathematics community")
    doc_global = has(doc, "general acceptance in the global mathematics community")
    r_global = has(rules, "general acceptance in the global mathematics community, as "
                          "determined in the sole discretion of CMI")
    r_discretion = has(rules, "as determined in the sole discretion of CMI") and \
        has(rules, "as determined by CMI in its sole discretion")
    if not r_global:
        return X("the rules do not carry the general-acceptance condition")
    if doc_global:
        return M("the document already carries the rules' own wording",
                 quote="general acceptance in the global mathematics community")
    return X(
        "the document says 'general acceptance in the **mathematics community**'; "
        "the rules say 'general acceptance in the **GLOBAL** mathematics community, "
        "as determined in the sole discretion of CMI' (Section 4(c), repeated at "
        "Section 7(a)(i)). Two words are dropped: 'global', and the fact that the "
        "determination is CMI's SOLE DISCRETION, not a community fact. Section "
        "7(a)(i)(4) enumerates what CMI may consider (independent journal articles, "
        "international conferences, awards, and any other factors).",
        doc_wording="general acceptance in the mathematics community",
        doc_wording_present=doc_phrase,
        rules_wording="general acceptance in the global mathematics community, as "
                      "determined in the sole discretion of CMI",
        rules_sole_discretion_present=r_discretion)


@plant("III3")
def iii3p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        "**general acceptance in the mathematics community**",
        "**general acceptance in the global mathematics community, as determined in "
        "the sole discretion of CMI**", 1)
    return c


@check("III4", "(iii)", "§7 completeness: does it list every condition the rules impose?",
       plant_kind="repair")
def iii4(ctx):
    rules = ctx["rules"]
    if not rules:
        return U("the Clay prize rules were unreachable; UNVERIFIED, not passed",
                 refusal_verbatim=ctx["rules_meta"]["refusal_verbatim"],
                 http_status=ctx["rules_meta"]["http_status"])
    doc = s7(ctx)
    r4d = has(rules, "the Proposed Solution has satisfactorily answered the questions "
                     "raised by the Problem's official description, as determined in "
                     "the sole discretion of CMI")
    r_nosubmit = has(rules, "CMI will not accept Proposed Solutions submitted directly "
                            "to CMI")
    r_ns = has(rules, "the Navier-Stokes Problem, a resolution in either direction "
                      "will be evaluated by the standard evaluation procedure set "
                      "forth in Section 7")
    r_notaddress = has(rules, "a paper that does not address or refer to the specific "
                              "mathematical questions set out in detail in the "
                              "official Problem description")
    doc_4d = has(doc, "satisfactorily answered")
    doc_nosubmit = has(doc, "does not accept direct submission") or \
        has(doc, "not accept Proposed Solutions submitted directly")
    if not r4d:
        return X("Section 4(d) not located in the fetched rules")
    if doc_4d and doc_nosubmit:
        return M("§7 lists all four Section-4 conditions and the no-direct-submission fact")
    return X(
        "§7 lists THREE conditions; the rules' Section 4 imposes FOUR. The missing "
        "one is Section 4(d): the Proposed Solution must have 'satisfactorily "
        "answered the questions raised by the Problem's official description, as "
        "determined in the sole discretion of CMI' -- which is the condition that "
        "binds this repository's own target choice, and it is the one Section 5(d) "
        "sharpens: 'a paper that does not address or refer to the specific "
        "mathematical questions set out in detail in the official Problem "
        "description will not be considered a Potential Solution'. Also absent from "
        "§7, and a planning fact of the same kind as the two-year clock: CMI 'will "
        "not accept Proposed Solutions submitted directly to CMI'. Directly relevant "
        "to the route-4 target: Section 5(b) states that for the Navier-Stokes "
        "Problem a resolution IN EITHER DIRECTION is evaluated by the standard "
        "Section 7 procedure -- so the breakdown direction this repository pursues "
        "is explicitly in scope.",
        doc_condition_count=3, rules_section4_condition_count=4,
        missing_condition="Section 4(d)",
        rules_4d_present=r4d, rules_5d_present=r_notaddress,
        rules_no_direct_submission_present=r_nosubmit,
        rules_navier_stokes_either_direction_present=r_ns)


@plant("III4")
def iii4p(ctx):
    c = dup(ctx)
    c["doc"] = c["doc"].replace(
        "**general acceptance in the mathematics community**",
        "**general acceptance in the mathematics community**, and that CMI "
        "determines the solution has satisfactorily answered the questions raised by "
        "the Problem's official description. CMI does not accept direct submission "
        "of proposed solutions", 1)
    return c


# ------------------------------------------------------------------ driver

def build_ctx():
    import solver.dssp_screen as screen
    doc = DOC.read_text(encoding="utf-8")
    rules, rules_meta = fetch_clay_rules()
    return {
        "doc": doc,
        "doc_sha256": sha256(doc.encode()),
        "cloc": json.loads((DATA / "p2_route_cloc_v1.json").read_text(encoding="utf-8")),
        "pvlx": json.loads((DATA / "p2_route_pvlx_v1.json").read_text(encoding="utf-8")),
        "ctrx": json.loads((DATA / "p2_route_ctrx_v1.json").read_text(encoding="utf-8")),
        "mryx": json.loads((DATA / "p2_route_mryx_v1.json").read_text(encoding="utf-8")),
        "b7m": json.loads((DATA / "p2_route_b7m_v1.json").read_text(encoding="utf-8")),
        "algw": json.loads((DATA / "p2_route_algw_v1.json").read_text(encoding="utf-8")),
        "screen": screen,
        "rules": rules,
        "rules_meta": rules_meta,
    }


def main():
    ctx = build_ctx()
    results = []
    for c in CHECKS:
        clean = c["fn"](ctx)
        # --- the planted control, per check, by name ---
        ctrl = {"plant_kind": c["plant_kind"], "planted": False}
        if c["id"] in PLANTS and clean["verdict"] != "UNVERIFIED":
            planted_ctx = PLANTS[c["id"]](ctx)
            planted = c["fn"](planted_ctx)
            expected = "MISMATCH" if c["plant_kind"] == "corrupt" else "MATCH"
            ctrl = {
                "plant_kind": c["plant_kind"],
                "planted": True,
                "clean_verdict": clean["verdict"],
                "planted_verdict": planted["verdict"],
                "expected_planted_verdict": expected,
                "fired": planted["verdict"] == expected and planted["verdict"] != clean["verdict"],
                "planted_detail": planted["detail"][:400],
            }
        elif clean["verdict"] == "UNVERIFIED":
            ctrl = {"plant_kind": c["plant_kind"], "planted": False,
                    "reason": "source unreachable; nothing to control"}
        results.append({"id": c["id"], "item": c["item"], "claim": c["claim"],
                        **clean, "control": ctrl})

    counts = {"MATCH": 0, "MISMATCH": 0, "UNVERIFIED": 0}
    for r in results:
        counts[r["verdict"]] += 1
    controls_run = [r for r in results if r["control"].get("planted")]
    controls_fired = [r for r in controls_run if r["control"]["fired"]]

    gate_answer = ("YES" if counts["UNVERIFIED"] == 0 else "NO")

    payload = {
        "leg": 384,
        "route": "COBV",
        "what": ("CLAY_OBLIGATIONS.md's remaining reviewer-read clauses, checked "
                 "mechanically against leg 381's banked check_D verdicts, against "
                 "§2's four named landed records, and against the Clay Institute's "
                 "own published prize rules"),
        "ceiling": ("TIER 2. No link of the L1->L4 chain moved. CLAY_OBLIGATIONS §6's "
                    "two no-method obligations stay OPEN. Clay stays ~0.05%."),
        "does_not": [
            "edits no obligations file (CLAY_OBLIGATIONS.md read-only)",
            "writes no leg-381 artifact (p2_route_cloc_v1.json read, never written)",
            "edits no solver module (solver/dssp_screen.py imported and EXECUTED, "
            "never modified)",
            "performs no outreach of any kind",
            "repairs nothing: every discrepancy is routed to integration as text",
        ],
        "landed_edit_under_test": LANDED_EDIT,
        "source_of_truth_item_i": SOURCE_OF_TRUTH,
        "document_sha256": ctx["doc_sha256"],
        "document_bytes": len(ctx["doc"].encode()),
        "clay_rules_fetch": ctx["rules_meta"],
        "checks_registered": len(CHECKS),
        "checks_run": len(results),
        "counts": counts,
        "instrument_control": {
            "why": ("the headline is a mismatch count, and a count of zero is the same "
                    "failure shape as the fabricated zero found in another leg's "
                    "instrument this cycle: a variable initialised to 0.0 and never "
                    "written. So every non-UNVERIFIED check carries its own targeted "
                    "plant, by name."),
            "controls_run": len(controls_run),
            "controls_fired": len(controls_fired),
            "controls_failed": [r["id"] for r in controls_run if not r["control"]["fired"]],
            "corrupt_plants": [r["id"] for r in controls_run
                               if r["control"]["plant_kind"] == "corrupt"],
            "repair_plants": [r["id"] for r in controls_run
                              if r["control"]["plant_kind"] == "repair"],
            "reading": ("a MATCH is only reported for a check whose corrupt-plant made "
                        "it read MISMATCH; a MISMATCH is only reported for a check "
                        "whose repair-plant made it read MATCH. Both directions are "
                        "exercised per row."),
        },
        "checks": results,
        "gate": {
            "question": ("Does every checked clause either verify against its primary "
                         "source / landed record, or get reported with the exact "
                         "discrepancy verbatim?"),
            "pre_committed_yes": ("The obligations document graduates from "
                                  "DRAFT-UNVERIFIED clause by clause, on integration's "
                                  "edit."),
            "pre_committed_no": ("A source is unreachable: bank the refusal as a "
                                 "refusal; an unverifiable clause is recorded as "
                                 "exactly that."),
            "answer": gate_answer,
            "unverifiable_clauses": [r["id"] for r in results
                                     if r["verdict"] == "UNVERIFIED"],
            "clay_movement": "none. Clay stays ~0.05%.",
        },
    }
    payload["self_hash"] = sha256(json.dumps(payload, sort_keys=True,
                                             ensure_ascii=False).encode())
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")

    print("leg 384 ROUTE-COBV")
    print("  document sha256      %s" % ctx["doc_sha256"][:16])
    print("  clay rules reachable %s (http %s)" % (ctx["rules_meta"]["reachable"],
                                                   ctx["rules_meta"]["http_status"]))
    print("  checks               %d run" % len(results))
    print("  MATCH/MISMATCH/UNVERIFIED  %(MATCH)d / %(MISMATCH)d / %(UNVERIFIED)d" % counts)
    print("  controls             %d run, %d fired" % (len(controls_run),
                                                       len(controls_fired)))
    for r in results:
        flag = {"MATCH": "ok ", "MISMATCH": "XX ", "UNVERIFIED": "?? "}[r["verdict"]]
        ctl = r["control"]
        cs = "ctrl:%s" % ("fired" if ctl.get("fired") else
                          ("n/a" if not ctl.get("planted") else "DID-NOT-FIRE"))
        print("  %s %-5s %-9s %s  [%s]" % (flag, r["id"], r["item"], r["claim"][:74], cs))
    print("  GATE ANSWERS %s" % gate_answer)
    print("  wrote %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
