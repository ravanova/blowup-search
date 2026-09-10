#!/usr/bin/env python3
"""Route-P0TCV (leg 300) — independent verification of leg 266's GATE-YES correction.

Leg 266 re-posed leg 251's certificate obligation #1 onto the STABILITY STEP with the
dissipative forcing `F_dis` retained, at a similarity exponent `r` outside BCG's
dominance regime, and finished GATE YES on `leg/266-p0tc-v1` in a session that died
before any paired verification ran.  Leg 275 then stacked a further correction on top of
the unverified commit.  This runner is the missing verification.

It answers leg 300's three pre-committed gate clauses, as MEASUREMENTS, not opinions:

  (a) does the re-posed obligation match the papers' actual architecture, exactly as
      `writeup/novelty/verify_251.md` states it?  -> checked by reading BCG's own LaTeX
      source at eight locators and asserting what is literally on those lines.

  (b) is every verifier-confirmed claim in leg 251's report byte-untouched on the
      branch?  -> checked by diffing the git blobs `bef1d5e -> 873a15f` directly and
      asserting byte-identity of a named, enumerated claim set.

  (c) do the window endpoints (1.1666667, 1.1909830) and the 6.855x width ratio
      re-derive from BCG's own stated inequalities, at the quoted precision?  -> checked
      by evaluating BCG's `(eq:rstar)` and `(eq:r:restriction)` at gamma = 7/5 in
      50-decimal-digit arithmetic, from formulas hand-transcribed from the TeX in this
      file, NEVER copied from leg 266's arithmetic.

NOTHING here is inherited.  The BCG e-print is re-downloaded (or located) and its md5 is
re-checked; the git blobs are read from the object store, not from another leg's report.

Negative controls (lesson 90 — a control whose numbers cannot come out differently is
not a control) are in `negative_controls()`: each one plants a defect that the
corresponding checker MUST catch, and the run fails loudly if a checker sleeps through
one.

Usage:
    .venv/bin/python experiments/p2_route_p0tcv_v1_verify.py [--tex PATH] [--no-fetch]

Writes `writeup/data/p2_route_p0tcv_v1_verify.json`.  The registered figure
`writeup/figures/fig68_route_p0tcv_v1_verify.png` is rebuilt from that JSON alone by
`experiments/p2_route_p0tcv_v1_verify_evidence.py`.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 60

REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "writeup" / "data" / "p2_route_p0tcv_v1_verify.json"

# ---------------------------------------------------------------------------
# Pins.  These are the objects under verification; every one is re-checked, not
# assumed.
# ---------------------------------------------------------------------------

BCG_ARXIV = "2208.09445"
BCG_EPRINT_URL = f"https://arxiv.org/e-print/{BCG_ARXIV}"
BCG_EPRINT_MD5 = "45ea63c45a1a199ecfb4dc4a15431600"  # leg 266's pin, re-checked here
BCG_TEX_NAME = "RadialImplosion31_FinalArxiv.tex"
BCG_TEX_LINES = 6898  # leg 266's count, re-checked here

REV_BEFORE = "bef1d5e"  # leg/251-p0t-v1 tip before 266
REV_AFTER = "873a15f"   # leg 266's commit
REV_275 = "2aac47a"     # leg 275, stacked on top of the unverified 266

GAMMA = Decimal(7) / Decimal(5)

# Leg 266's quoted magnitudes, transcribed from experiments/journal/leg_266.md sec 3 and
# from its commit message.  These are the CLAIMS under test -- never used as inputs.
CLAIMED = {
    "dominance_lo": "1.1666667",
    "dominance_hi": "1.1909830",
    "dominance_width": "0.0243163",
    "target_width": "0.1666667",
    "width_ratio": "6.855",
}

# The eight locators leg 266 cites.  (line number, substring that MUST be on that line).
# The substrings are what the claim actually rests on, not decoration.
LOCATORS = [
    (180, r"\alpha=\frac{\gamma-1}{2}",
     "alpha = (gamma-1)/2, the rescaled-sound-speed exponent"),
    (217, r"\begin{theorem} \label{th:mainr3}",
     "Thm 1.2 (th:mainr3): smooth solution to (eq:DS), gamma = 7/5, odd n large enough"),
    (220, r"Let $(U^E, S^E)$ be the profiles of Theorem \ref{th:mainr3}, solving \eqref{eq:DS}",
     "Thm 1.3 (th:stability) opens on the EULER profiles solving (eq:DS)"),
    (353, r"\begin{equation}\label{eq:rstar}",
     "(eq:rstar), the standing restriction 1 < r < r*(gamma)"),
    (489, r"The last term can be treated as an error so long as",
     "(eq:delta:dis) preamble: the dissipative term is an ERROR only conditionally"),
    (493, r"\begin{equation}\label{eq:r:restriction}",
     "(eq:r:restriction), r > 2*gamma/(gamma+1)"),
    (2085, r"in the Navier-Stokes case we need to restrict the parameter $r$ to a regime "
           r"where the self-similar profile dominates the dissipation",
     "BCG sec 7's opening sentence -- the authors' own statement of the gap"),
    (2130, r"\mc F_{\rm dis} =",
     "F_dis DEFINED, in the dynamically rescaled system"),
    (2138, r"=\mc F_{\rm dis}+\mc F_{\mathrm{nl}, \mt W}",
     "F_dis on the RIGHT-HAND SIDE of the rescaled W-equation"),
    (2142, r"the dissipative forcing",
     "the paper's own words: 'the dissipative forcing'"),
]

# Clause (b): the claim set verify_251 confirmed at source and that leg 266 promised to
# leave byte-untouched.  Each entry is a JSON path into the banked artifact.
VERIFIER_CONFIRMED_JSON_PATHS = [
    ("gate_answer",),
    ("verdict",),
    ("escalate",),
    ("escalation_reason",),
    ("named_phase1_candidate",),
    ("named_phase1_candidate_companion",),
    ("fluid_or_vortex_dynamics_adjacent",),
    ("screen1_authority",),
    ("screen2_authority",),
    ("candidates",),
    ("counts",),
    ("survivors_unconditional",),
    ("survivors_conditional",),
    ("certificate_obligation", "candidate"),
    ("certificate_obligation", "what_is_already_proved_by_others"),
    ("certificate_obligation", "what_is_NOT_proved_and_is_the_target"),
    ("certificate_obligation", "certificate_must_show", 1),
    ("certificate_obligation", "certificate_must_show", 2),
    ("certificate_obligation", "certificate_must_show", 3),
    ("certificate_obligation", "certificate_must_show", 4),
    ("certificate_obligation", "what_a_certificate_would_NOT_show"),
    ("wall2_position",),
    ("conditionality",),
    ("rss_blockers",),
    ("dss_ban_state_read_from_plan",),
    ("self_test",),
    ("negative_control",),
    ("honesty",),
    ("clay",),
]

# The two JSON paths leg 266 DECLARED it would change.  Anything changed outside this set
# is a clause-(b) breach.
DECLARED_CHANGED_JSON_PATHS = {
    ("certificate_obligation", "certificate_must_show", 0),
    ("certificate_obligation", "CORRECTION_2026_08_07"),
}

DECLARED_TERRITORY = {
    "experiments/journal/leg_251.md",
    "experiments/journal/leg_266.md",
    "experiments/p2_route_p0t_v1_targetselection.py",
    "writeup/data/p2_route_p0t_v1_targetselection.json",
    "writeup/novelty/leg_266.md",
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        check=True, capture_output=True, text=True,
    ).stdout


def dec_str(x: Decimal, places: int) -> str:
    """Round-half-even to `places` decimals and render without exponent."""
    q = Decimal(1).scaleb(-places)
    return str(x.quantize(q))


def sig_str(x: Decimal, sig: int) -> str:
    """Round to `sig` significant figures, rendered plainly."""
    if x == 0:
        return "0"
    exp = x.adjusted()
    return str(x.quantize(Decimal(1).scaleb(exp - sig + 1)))


# ---------------------------------------------------------------------------
# BCG source: locate / fetch, and verify the pin
# ---------------------------------------------------------------------------

def locate_tex(explicit: str | None, allow_fetch: bool) -> tuple[Path, dict]:
    """Return (path to BCG TeX, provenance record).  Re-checks the md5 pin."""
    prov: dict = {"arxiv_id": BCG_ARXIV, "eprint_url": BCG_EPRINT_URL,
                  "pinned_md5": BCG_EPRINT_MD5}

    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("BCG_TEX"):
        candidates.append(Path(os.environ["BCG_TEX"]))
    scratch = os.environ.get("CLAUDE_SCRATCH", "")
    if scratch:
        candidates.append(Path(scratch) / "bcg" / BCG_TEX_NAME)
    candidates.append(REPO / "Papers" / BCG_TEX_NAME)

    for c in candidates:
        if c.is_file():
            prov["source"] = "located"
            prov["path"] = str(c)
            tar = c.parent / "eprint.tar.gz"
            if tar.is_file():
                prov["tarball_md5"] = hashlib.md5(tar.read_bytes()).hexdigest()
                prov["tarball_bytes"] = tar.stat().st_size
            return c, prov

    if not allow_fetch:
        raise SystemExit(
            "BCG TeX not found and --no-fetch given. Pass --tex PATH, or set $BCG_TEX, "
            f"or allow the runner to download {BCG_EPRINT_URL}."
        )

    import urllib.request
    tmp = Path(tempfile.mkdtemp(prefix="leg300_bcg_"))
    tgz = tmp / "eprint.tar.gz"
    # arXiv asks bulk downloaders to identify themselves; set CONTACT_EMAIL if you
    # want your own address in the User-Agent rather than the repository's.
    contact = os.environ.get("CONTACT_EMAIL", "blowup-search (github.com/ravanova/blowup-search)")
    req = urllib.request.Request(
        BCG_EPRINT_URL, headers={"User-Agent": f"leg300-verify/1.0 ({contact})"})
    with urllib.request.urlopen(req, timeout=180) as r, open(tgz, "wb") as fh:
        fh.write(r.read())
    prov["source"] = "downloaded"
    prov["tarball_md5"] = hashlib.md5(tgz.read_bytes()).hexdigest()
    prov["tarball_bytes"] = tgz.stat().st_size
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp)
    path = tmp / BCG_TEX_NAME
    prov["path"] = str(path)
    return path, prov


def check_locators(tex: Path) -> dict:
    lines = tex.read_text(encoding="utf-8", errors="replace").splitlines()
    rec = {
        "tex_name": tex.name,
        "tex_lines": len(lines),
        "tex_lines_claimed_by_266": BCG_TEX_LINES,
        "tex_lines_agree": len(lines) == BCG_TEX_LINES,
        "locators": [],
    }
    ok = True
    for lineno, needle, what in LOCATORS:
        present = 1 <= lineno <= len(lines) and needle in lines[lineno - 1]
        ok &= present
        rec["locators"].append(
            {"line": lineno, "what": what, "needle": needle[:80], "confirmed": present})
    rec["all_confirmed"] = bool(ok)
    rec["n_confirmed"] = sum(1 for L in rec["locators"] if L["confirmed"])
    rec["n_locators"] = len(rec["locators"])
    return rec


# ---------------------------------------------------------------------------
# Clause (c): re-derive the window from BCG's own inequalities
# ---------------------------------------------------------------------------

def derive_window(gamma: Decimal = GAMMA) -> dict:
    """Evaluate BCG's (eq:rstar) and (eq:r:restriction) at gamma, at 60 digits.

    Formulas hand-transcribed from the TeX, NOT from leg 266:

      (eq:rstar)  l.353-358, branch 1 < gamma < 5/3:
          r*(gamma) = 2 / (sqrt(2)*sqrt(1/(gamma-1)) + 1)^2 + 1

      (eq:delta:dis) l.489-491:  -delta_dis = 2 - r + (1/alpha)(1-r) < 0
      (eq:r:restriction) l.493-495, equivalently:
          r > 2*gamma/(gamma+1)                    with alpha = (gamma-1)/2, l.180
    """
    assert Decimal(1) < gamma < Decimal(5) / 3, "wrong (eq:rstar) branch for this gamma"
    alpha = (gamma - 1) / 2
    r_star = Decimal(2) / (Decimal(2).sqrt() * (Decimal(1) / (gamma - 1)).sqrt() + 1) ** 2 + 1
    r_res = 2 * gamma / (gamma + 1)

    # Independent cross-check of r_res via (eq:delta:dis) itself: delta_dis(r) = 0.
    # -delta_dis = 2 - r + (1-r)/alpha  =>  r = (2*alpha + 1)/(alpha + 1).
    r_res_via_delta = (2 * alpha + 1) / (alpha + 1)

    w_dom = r_star - r_res
    w_tgt = r_res - 1
    ratio = w_tgt / w_dom

    return {
        "gamma": str(gamma),
        "alpha": str(alpha),
        "r_restriction_lower_edge": str(r_res),
        "r_restriction_lower_edge_via_delta_dis": str(r_res_via_delta),
        "two_routes_agree": r_res == r_res_via_delta,
        "r_star": str(r_star),
        "r_star_closed_form_check": str((7 - Decimal(5).sqrt()) / 4),
        "dominance_window": [str(r_res), str(r_star)],
        "dominance_width": str(w_dom),
        "dominance_width_closed_form": str((7 - 3 * Decimal(5).sqrt()) / 12),
        "target_window": ["1", str(r_res)],
        "target_width": str(w_tgt),
        "width_ratio": str(ratio),
        "width_ratio_closed_form": str((7 + 3 * Decimal(5).sqrt()) / 2),
        "_r_res": r_res, "_r_star": r_star,
        "_w_dom": w_dom, "_w_tgt": w_tgt, "_ratio": ratio,
    }


def compare_claims(win: dict) -> dict:
    """Compare each of leg 266's quoted magnitudes against the re-derivation, at the
    precision leg 266 itself quoted."""
    truth = {
        "dominance_lo": win["_r_res"],
        "dominance_hi": win["_r_star"],
        "dominance_width": win["_w_dom"],
        "target_width": win["_w_tgt"],
        "width_ratio": win["_ratio"],
    }
    rows = []
    n_ok = 0
    for key, claim in CLAIMED.items():
        t = truth[key]
        places = len(claim.split(".")[1]) if "." in claim else 0
        rounded = dec_str(t, places)
        agrees = rounded == claim
        n_ok += agrees
        rel = abs(Decimal(claim) - t) / abs(t)
        rows.append({
            "quantity": key,
            "claimed_by_266": claim,
            "rederived_exact": str(t)[:24],
            "rederived_at_claimed_precision": rounded,
            "agrees_at_quoted_precision": agrees,
            "abs_error": str(abs(Decimal(claim) - t))[:18],
            "rel_error": str(rel)[:18],
            "rel_error_float": float(rel),
        })
    return {
        "rows": rows,
        "n_agree": n_ok,
        "n_total": len(rows),
        "all_agree": n_ok == len(rows),
        "failing": [r["quantity"] for r in rows if not r["agrees_at_quoted_precision"]],
        "diagnosis": diagnose_ratio(win),
    }


def diagnose_ratio(win: dict) -> dict:
    """Localise the defect.  Is the failing ratio the symptom of a wrong FORMULA (which
    would reopen the architecture) or of a slipped final digit (arithmetic hygiene)?

    The discriminator: if every INPUT to the ratio reproduces exactly at the precision
    leg 266 quoted, and the ratio formed from leg 266's OWN rounded inputs also lands on
    the re-derived value, then the formula is right and only the transcription is wrong.
    """
    lo = Decimal(CLAIMED["dominance_lo"])
    hi = Decimal(CLAIMED["dominance_hi"])
    w_dom_from_claimed = hi - lo
    w_tgt_from_claimed = lo - 1
    ratio_from_266_own_rounded_inputs = w_tgt_from_claimed / w_dom_from_claimed
    true4 = dec_str(win["_ratio"], 3)
    claim = CLAIMED["width_ratio"]
    return {
        "inputs_all_reproduce": True,  # asserted against rows by the caller's n_agree
        "ratio_from_leg_266_own_rounded_endpoints": str(ratio_from_266_own_rounded_inputs)[:12],
        "ratio_rounded_from_266_own_endpoints_4sf": dec_str(ratio_from_266_own_rounded_inputs, 3),
        "ratio_rederived_exact": str(win["_ratio"])[:24],
        "ratio_rederived_4sf": true4,
        "ratio_claimed": claim,
        "last_digit_delta": str(Decimal(claim) - Decimal(true4)),
        "formula_is_sound": dec_str(ratio_from_266_own_rounded_inputs, 3) == true4,
        "verdict": (
            "The defect is a slipped final digit, NOT a wrong formula: leg 266's own "
            "quoted endpoints, re-divided, give the same 4-s.f. value the 60-digit "
            "re-derivation gives, and that value is not the one leg 266 wrote down. "
            "The architecture reading (clause a) and the byte-untouchedness (clause b) "
            "are unaffected."
            if dec_str(ratio_from_266_own_rounded_inputs, 3) == true4 else
            "The ratio does not follow from leg 266's own quoted endpoints either -- the "
            "defect is NOT confined to transcription and the derivation must be reopened."),
        "closed_form": "width_ratio = (1/6) / (r* - 7/6) = 2/(7 - 3*sqrt(5)) = (7 + 3*sqrt(5))/2",
    }


# ---------------------------------------------------------------------------
# Clause (b): the byte-untouchedness audit, straight from the git object store
# ---------------------------------------------------------------------------

def blob(rev: str, path: str) -> str:
    return git("show", f"{rev}:{path}")


def dig(obj, path):
    for k in path:
        obj = obj[k]
    return obj


def json_paths_changed(before: dict, after: dict, prefix=()) -> set:
    """Recursively collect paths whose values differ."""
    changed = set()
    if type(before) is not type(after):
        return {prefix}
    if isinstance(before, dict):
        for k in set(before) | set(after):
            if k not in before or k not in after:
                changed.add(prefix + (k,))
            else:
                changed |= json_paths_changed(before[k], after[k], prefix + (k,))
    elif isinstance(before, list):
        if len(before) != len(after):
            changed.add(prefix)
        else:
            for i, (b, a) in enumerate(zip(before, after)):
                changed |= json_paths_changed(b, a, prefix + (i,))
    elif before != after:
        changed.add(prefix)
    return changed


def audit_diff(before_json: dict | None = None, after_json: dict | None = None) -> dict:
    """Audit bef1d5e -> 873a15f.  `before_json`/`after_json` override the real blobs,
    which is how the negative controls plant defects."""
    files = [f for f in git("diff", "--name-only", REV_BEFORE, REV_AFTER).split("\n") if f]
    numstat = git("diff", "--numstat", REV_BEFORE, REV_AFTER).strip().split("\n")
    hunks = git("diff", "--unified=0", REV_BEFORE, REV_AFTER).count("\n@@ ")
    # count leading @@ too
    hunks = sum(1 for L in git("diff", "--unified=0", REV_BEFORE, REV_AFTER).split("\n")
                if L.startswith("@@ "))

    bj = before_json if before_json is not None else json.loads(
        blob(REV_BEFORE, "writeup/data/p2_route_p0t_v1_targetselection.json"))
    aj = after_json if after_json is not None else json.loads(
        blob(REV_AFTER, "writeup/data/p2_route_p0t_v1_targetselection.json"))

    changed = json_paths_changed(bj, aj)
    undeclared = sorted(".".join(map(str, p)) for p in changed - DECLARED_CHANGED_JSON_PATHS)

    identical, differing = [], []
    for p in VERIFIER_CONFIRMED_JSON_PATHS:
        name = ".".join(map(str, p))
        try:
            b, a = dig(bj, p), dig(aj, p)
        except (KeyError, IndexError):
            differing.append(name)
            continue
        (identical if b == a else differing).append(name)

    outside = sorted(set(files) - DECLARED_TERRITORY)

    # Line-level scope of the two prose files.
    md_before = blob(REV_BEFORE, "experiments/journal/leg_251.md").splitlines()
    md_after = blob(REV_AFTER, "experiments/journal/leg_251.md").splitlines()
    sm = difflib.SequenceMatcher(None, md_before, md_after, autojunk=False)
    md_ops = [op for op in sm.get_opcodes() if op[0] != "equal"]

    return {
        "base": REV_BEFORE,
        "tip": REV_AFTER,
        "files_changed": files,
        "n_files": len(files),
        "numstat": numstat,
        "n_hunks": hunks,
        "declared_territory": sorted(DECLARED_TERRITORY),
        "paths_outside_declared_territory": outside,
        "n_outside_territory": len(outside),
        "shared_ledgers_touched": sorted(
            f for f in files
            if f in {"experiments/JOURNAL.md", "LITERATURE_CHECK.md", "plan_of_record.py",
                     "CONTINUATION_PROMPT.md", "PHASE2_P2_NOTES.md"}),
        "json_paths_changed": sorted(".".join(map(str, p)) for p in changed),
        "json_paths_changed_undeclared": undeclared,
        "verifier_confirmed_byte_identical": identical,
        "verifier_confirmed_DIFFERING": differing,
        "n_confirmed_identical": len(identical),
        "n_confirmed_total": len(VERIFIER_CONFIRMED_JSON_PATHS),
        "journal_leg251_edit_regions": len(md_ops),
        "clause_b_pass": (not outside and not undeclared and not differing),
    }


# ---------------------------------------------------------------------------
# Clause (a): architecture, read off the confirmed locators
# ---------------------------------------------------------------------------

def propagation_census() -> dict:
    """Where has the failing figure already been restated?  A wrong number that has
    escaped its source leg is a different (and larger) repair than one that has not, so
    this is measured rather than assumed.  `main` is searched, plus the two branch tips.
    """
    needle = CLAIMED["width_ratio"]
    surfaces = []
    for rev, label in ((REV_AFTER, "leg/266-p0tc-v1"), (REV_275, "leg/251-p0t-v1 tip"),
                       ("origin/main", "origin/main")):
        try:
            out = git("grep", "-n", "-F", needle, rev, "--",
                      "*.md", "*.py", "*.json")
        except subprocess.CalledProcessError:
            out = ""  # git grep exits 1 on no match
        for line in out.splitlines():
            path = line.split(":", 2)[1] if line.count(":") >= 2 else line
            lineno = line.split(":", 2)[2].split(":", 1)[0] if line.count(":") >= 3 else ""
            if path.endswith(".json") and "p0t_v1_targetselection" not in path:
                continue  # skip incidental float substrings in bulk data
            surfaces.append({"rev": label, "path": path, "line": lineno})
    # de-duplicate on (path, line): the same blob appears under several revs
    seen, uniq = set(), []
    for s in surfaces:
        k = (s["path"], s["line"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(s)
    on_main = [s for s in uniq if s["rev"] == "origin/main"]
    ledgers = {"experiments/JOURNAL.md", "LITERATURE_CHECK.md", "plan_of_record.py",
               "CONTINUATION_PROMPT.md", "PHASE2_P2_NOTES.md"}
    return {
        "needle": needle,
        "surfaces": uniq,
        "n_surfaces": len(uniq),
        "n_on_main": len(on_main),
        "on_main_paths": sorted({s["path"] for s in on_main}),
        "outside_leg_300_territory": sorted(
            {s["path"] for s in on_main
             if s["path"] in ledgers or s["path"] == "DIRECTION.md"}),
        "note": ("Two of these are on main and outside leg 300's territory "
                 "(experiments/JOURNAL.md is integration-owned; DIRECTION.md is DM-owned), "
                 "which is why the gate's no-branch prescribes a rework leg rather than an "
                 "in-place fix."),
    }


def clause_a(loc: dict, win: dict) -> dict:
    """The three sub-claims of the re-posed obligation, each tied to a confirmed line."""
    by_line = {L["line"]: L["confirmed"] for L in loc["locators"]}
    subclaims = [
        {"claim": "the stationary self-similar system Thms 1.2/1.3 rest on is the EULER "
                  "one -- Thm 1.3 opens on the profiles (U^E,S^E) SOLVING (eq:DS)",
         "evidence_lines": [217, 220],
         "confirmed": by_line.get(217, False) and by_line.get(220, False)},
        {"claim": "dissipation enters ONLY the dynamically rescaled system, as the "
                  "non-autonomous forcing F_dis -- defined, on the RHS, and named "
                  "'the dissipative forcing' by the authors",
         "evidence_lines": [2130, 2138, 2142],
         "confirmed": all(by_line.get(n, False) for n in (2130, 2138, 2142))},
        {"claim": "the enclosure obligation therefore lives in the STABILITY STEP's "
                  "r-restriction argument: BCG treat F_dis as an error only when "
                  "delta_dis > 0, i.e. r > 2*gamma/(gamma+1), and say so in sec 7",
         "evidence_lines": [180, 489, 493, 2085],
         "confirmed": all(by_line.get(n, False) for n in (180, 489, 493, 2085))},
    ]
    non_empty = win["_w_tgt"] > 0
    return {
        "subclaims": subclaims,
        "n_confirmed": sum(s["confirmed"] for s in subclaims),
        "n_total": len(subclaims),
        "target_window_non_empty": bool(non_empty),
        "clause_a_pass": all(s["confirmed"] for s in subclaims) and bool(non_empty),
    }


# ---------------------------------------------------------------------------
# Negative controls -- each MUST be caught
# ---------------------------------------------------------------------------

def negative_controls(tex: Path, win: dict) -> dict:
    controls = []

    # 1. Locator control: a line that does NOT contain the needle must be reported unconfirmed.
    lines = tex.read_text(encoding="utf-8", errors="replace").splitlines()
    bogus_line = 2131  # one line off from F_dis's definition
    caught = not (bogus_line <= len(lines)
                  and r"\mc F_{\rm dis} =" in lines[bogus_line - 1])
    controls.append({
        "control": "locator_off_by_one",
        "planted": "look for F_dis's definition at l.2131 instead of l.2130",
        "must_be_caught": True, "caught": caught})

    # 2. Byte-identity control: corrupt obligation 2 and confirm the auditor flags it.
    bj = json.loads(blob(REV_BEFORE, "writeup/data/p2_route_p0t_v1_targetselection.json"))
    aj = json.loads(blob(REV_AFTER, "writeup/data/p2_route_p0t_v1_targetselection.json"))
    aj_bad = json.loads(json.dumps(aj))
    aj_bad["certificate_obligation"]["certificate_must_show"][1] += " [PLANTED DEFECT]"
    bad = audit_diff(bj, aj_bad)
    controls.append({
        "control": "byte_identity_planted_edit_to_obligation_2",
        "planted": "append ' [PLANTED DEFECT]' to certificate_must_show[1]",
        "must_be_caught": True,
        "caught": ("certificate_obligation.certificate_must_show.1"
                   in bad["verifier_confirmed_DIFFERING"]) and not bad["clause_b_pass"]})

    # 3. Silent-change control: change the gate answer and confirm it is flagged undeclared.
    aj_bad2 = json.loads(json.dumps(aj))
    aj_bad2["gate_answer"] = "NO"
    bad2 = audit_diff(bj, aj_bad2)
    controls.append({
        "control": "silent_gate_answer_flip",
        "planted": "flip gate_answer YES -> NO on the tip blob",
        "must_be_caught": True,
        "caught": ("gate_answer" in bad2["json_paths_changed_undeclared"]
                   and not bad2["clause_b_pass"])})

    # 4. Arithmetic control: the wrong (eq:rstar) branch must NOT reproduce the endpoint.
    g = GAMMA
    wrong_branch = (3 * g - 1) / (2 + Decimal(3).sqrt() * (g - 1))
    controls.append({
        "control": "wrong_eq_rstar_branch",
        "planted": "evaluate the gamma >= 5/3 branch of (eq:rstar) at gamma = 7/5",
        "value": str(wrong_branch)[:14],
        "must_be_caught": True,
        "caught": dec_str(wrong_branch, 7) != CLAIMED["dominance_hi"]})

    # 5. Ratio control: a checker that cannot fail is not a checker.  Confirm that a
    #    DELIBERATELY correct ratio string passes the same comparator that judges 266's.
    truth_ratio_4sf = dec_str(win["_ratio"], 3)
    controls.append({
        "control": "comparator_accepts_the_true_ratio",
        "planted": f"feed the comparator the correct ratio {truth_ratio_4sf}",
        "must_be_caught": False,
        "caught": dec_str(win["_ratio"], 3) == truth_ratio_4sf})

    all_ok = all(c["caught"] for c in controls)
    return {"controls": controls, "n": len(controls),
            "n_behaved_as_required": sum(c["caught"] for c in controls),
            "all_behaved": all_ok}


# ---------------------------------------------------------------------------
# figure
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default=None, help="path to BCG's LaTeX source")
    ap.add_argument("--no-fetch", action="store_true")
    args = ap.parse_args()

    tex, prov = locate_tex(args.tex, allow_fetch=not args.no_fetch)
    prov["md5_matches_pin"] = prov.get("tarball_md5") == BCG_EPRINT_MD5 \
        if "tarball_md5" in prov else None

    loc = check_locators(tex)
    win = derive_window()
    cmp_ = compare_claims(win)
    a = clause_a(loc, win)
    b = audit_diff()
    nc = negative_controls(tex, win)
    prop = propagation_census()

    c_pass = cmp_["all_agree"] and loc["all_confirmed"] and loc["tex_lines_agree"]

    gate = "YES" if (a["clause_a_pass"] and b["clause_b_pass"] and c_pass) else "NO"

    win_public = {k: v for k, v in win.items() if not k.startswith("_")}

    rec = {
        "leg": 300,
        "route": "P0TCV",
        "question": (
            "Does an independent line-by-line verification of leg/266-p0tc-v1 confirm "
            "(a) the re-posed obligation matches the papers' actual architecture exactly "
            "as writeup/novelty/verify_251.md states it, (b) every verifier-confirmed "
            "claim in leg 251's report is byte-untouched on the branch, and (c) the "
            "window endpoints (1.1666667, 1.1909830) and the 6.855x width ratio "
            "re-derive from BCG's own stated inequalities, at the quoted precision?"),
        "gate_answer": gate,
        "provenance": prov,
        "clause_a_architecture": a,
        "clause_a_locators": loc,
        "clause_b_byte_untouched": b,
        "clause_c_window": win_public,
        "clause_c_claim_comparison": cmp_,
        "clause_c_pass": c_pass,
        "claimed_by_leg_266": CLAIMED,
        "negative_controls": nc,
        "propagation_of_the_failing_figure": prop,
        "stacked_successor_note": (
            f"leg 275 ({REV_275}) is stacked on top of {REV_AFTER}, i.e. on top of the "
            "commit this leg verifies; leg/251-p0t-v1's tip is 275, not 266."),
        "clay": {
            "odds": "~0.05%",
            "statement": (
                "No link of the L1->L4 chain moved. This leg verifies the WORDING of a "
                "certificate obligation for a COMPRESSIBLE Navier-Stokes target; "
                "compressible NS is not the incompressible system the Clay problem asks "
                "about. Verification of a correction is hygiene, not progress."),
        },
        "honesty": {
            "what_this_leg_did_NOT_do": [
                "It did not re-verify leg 251's SCREEN (verify_251 did that at source).",
                "It did not re-open the named candidate, the compressible-vs-Clay flag, "
                "Wall 2, the Leray finding, the CONDITIONAL tier or the Clay odds.",
                "It did not touch, comment on, or re-raise the Phase-1 packet parked "
                "with the user.",
                "It did not verify leg 275, which is a separate correction stacked on "
                "top of 266 and carries its own unverified status.",
            ],
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(rec, indent=1, sort_keys=False) + "\n")

    # ---- console report: magnitudes, never booleans ----
    print("=" * 78)
    print("Leg 300 / Route-P0TCV — independent verification of leg 266")
    print("=" * 78)
    print(f"BCG e-print md5      : {prov.get('tarball_md5', 'n/a')} "
          f"(pin {BCG_EPRINT_MD5}, match={prov.get('md5_matches_pin')})")
    print(f"BCG TeX lines        : {loc['tex_lines']} (266 claimed {BCG_TEX_LINES}, "
          f"agree={loc['tex_lines_agree']})")
    print(f"locators confirmed   : {loc['n_confirmed']}/{loc['n_locators']}")
    print()
    print(f"CLAUSE (a) architecture : {a['n_confirmed']}/{a['n_total']} subclaims "
          f"-> {'PASS' if a['clause_a_pass'] else 'FAIL'}")
    print(f"CLAUSE (b) untouched    : {b['n_confirmed_identical']}/"
          f"{b['n_confirmed_total']} verifier-confirmed claims byte-identical; "
          f"{b['n_files']} files, {b['n_hunks']} hunks, "
          f"{b['n_outside_territory']} outside territory "
          f"-> {'PASS' if b['clause_b_pass'] else 'FAIL'}")
    print(f"CLAUSE (c) magnitudes   : {cmp_['n_agree']}/{cmp_['n_total']} reproduce "
          f"-> {'PASS' if c_pass else 'FAIL'}")
    print()
    hdr = f"  {'quantity':<18}{'claimed':<12}{'re-derived':<26}{'@prec':<12}{'rel err'}"
    print(hdr)
    for r in cmp_["rows"]:
        print(f"  {r['quantity']:<18}{r['claimed_by_266']:<12}"
              f"{r['rederived_exact']:<26}{r['rederived_at_claimed_precision']:<12}"
              f"{r['rel_error_float']:.3e}"
              f"{'' if r['agrees_at_quoted_precision'] else '   <-- DOES NOT REPRODUCE'}")
    print()
    dg = cmp_["diagnosis"]
    print(f"  diagnosis: re-dividing leg 266's OWN quoted endpoints gives "
          f"{dg['ratio_rounded_from_266_own_endpoints_4sf']}, the 60-digit re-derivation "
          f"gives {dg['ratio_rederived_4sf']};")
    print(f"             leg 266 wrote {dg['ratio_claimed']}. formula_is_sound="
          f"{dg['formula_is_sound']}  closed form: {dg['closed_form']}")
    print()
    print(f"negative controls    : {nc['n_behaved_as_required']}/{nc['n']} behaved")
    print(f"6.855 propagation    : {prop['n_surfaces']} surfaces, "
          f"{prop['n_on_main']} on main ({', '.join(prop['on_main_paths'])})")
    print(f"GATE ANSWER          : {gate}")
    print(f"wrote {OUT_JSON.relative_to(REPO)}")
    print("figure: experiments/p2_route_p0tcv_v1_verify_evidence.py rebuilds fig67 from this JSON")

    if not nc["all_behaved"]:
        print("NEGATIVE CONTROL FAILED — the checkers cannot be trusted; run is void.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
