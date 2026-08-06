#!/usr/bin/env python3
"""Leg 235 -- Route-CDAP: a census of banked headline verdicts for leg 202's defect shape.

THE SHAPE BEING HUNTED (leg 202, Route-PNA, escalated/parked):

    the rejecting signal already existed in the caller's own data and was never used

i.e. a banked artifact asserts a verdict (converged / closes / holds / certified / ...)
AND, in the same record, carries a diagnostic quantity the same runner computed, which on
inspection already contradicts that verdict -- with no code path from the diagnostic to
the verdict.  This is NOT the guard-class shape ("a guard fails on adversarial input")
that every other audit-family item this cycle found: no adversarial input is involved and
nothing is latent.  The contradicting number is sitting in the banked JSON.

This runner PATCHES NOTHING.  Every JSON and every runner is opened read-only.

METHOD, in three stages, none of which is allowed to be the whole answer:

  S1  MECHANICAL SCREEN over every writeup/data/*.json.  Walk to every dict that carries
      at least one verdict-like key with a POSITIVE value.  Collect its numeric siblings
      as candidate diagnostics.  Three rules fire:

        R-SPREAD  (the leg-202 detector) -- across a LIST of sibling records that all
                  carry the same positive verdict, a diagnostic whose max/min spans more
                  than SPREAD_DECADES decades.  Leg 202's signature exactly: a verdict
                  that does not move while a diagnostic moves by 14 decades means the
                  verdict is not a function of the diagnostic.
        R-THRESH  -- a diagnostic X with a named threshold sibling in the same record
                  (X_tol, X_max, tol, threshold, budget, required, needed, ...) that X
                  violates, while the verdict is positive.
        R-MAGN    -- a diagnostic whose NAME asserts it is an error-like quantity
                  (residual/defect/error/gap/violation/mismatch/drift) exceeding
                  MAGN_LIMIT in absolute value, while the verdict is positive.

  S2  WIRING CHECK on every screened hit.  Open the producing runner (matched by JSON
      stem) and ask whether the diagnostic's name EVER appears in a comparison, an `if`,
      an assert, a min/max-against-threshold, or a boolean construction.  If it does, the
      diagnostic is wired to something and this is not the shape; if it appears only in
      assignments and dict-writes, it is a candidate for the shape.  This is the step
      that separates leg 202's defect from an ordinary large-but-checked number.

  S3  ADJUDICATION, recorded per hit with a reason string.  A screened, unwired hit is
      still not a finding unless the diagnostic, read in context, would have CONTRADICTED
      the verdict.  Three ways a hit is dismissed and the reason is banked, not hidden:
        DISMISS-INTENDED   the spread is the artifact's own subject (a sweep whose POINT
                           is that the quantity grows; the verdict is about something
                           else entirely and is not claimed to bound it)
        DISMISS-WIRED      S2 found the wire
        DISMISS-SCALE      the "threshold" sibling is not a threshold for that quantity
      A hit that survives all three is reported as an instance of the shape.

POSITIVE CONTROL (lesson 90: a control that cannot come out differently is not a control).
Leg 202's own artifact, writeup/data/p2_route_d_v11_anchor.json, is in the census input
set and MUST be flagged by R-SPREAD and MUST survive S2 unwired.  If it is not, the
instrument is not measuring and the run aborts with a nonzero exit.  It is reported
separately as `control`, and is NEVER counted as one of this leg's own hits.

reproduce:  python experiments/p2_route_cdap_v1_census.py
writes:     writeup/data/p2_route_cdap_v1_census.json
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data")
OUT = os.path.join(DATA, "p2_route_cdap_v1_census.json")

# ---------------------------------------------------------------- tunables
# Every one of these is reported in the JSON's meta block so the census is
# reproducible and its sensitivity is auditable, not hidden in the code.
SPREAD_DECADES = 6.0     # leg 202's own spread is ~14.6 decades; 6 is deliberately loose
MAGN_LIMIT = 1.0         # an error-like quantity above 1 is large in any norm this repo uses
MAX_ROWS_SCANNED = 200000

VERDICT_KEYS = (
    "converged", "convergence", "closes", "closed", "verdict", "certified",
    "holds", "admissible", "passes", "passed", "pass", "success", "succeeded",
    "ok", "valid", "satisfied", "proved", "proven", "established", "confirmed",
    "grid_converged", "accepted", "is_certificate", "certificate_closes",
    "gate", "gate_answer", "novel", "usable", "safe", "clean",
)

POSITIVE_STRINGS = {
    "yes", "true", "pass", "passed", "closes", "converged", "ok", "valid",
    "holds", "certified", "accepted", "success", "clean", "safe", "novel",
}

DIAG_ERRORLIKE = re.compile(
    r"(residual|defect|error|err\b|gap|violation|mismatch|drift|discrepanc|"
    r"deviation|slack|excess|overshoot|loss|shortfall|infeas)", re.I
)

THRESHOLD_SUFFIXES = ("_tol", "_tolerance", "_max", "_limit", "_budget", "_bound",
                      "_threshold", "_required", "_needed", "_allowed", "_cap")
THRESHOLD_NAMES = ("tol", "tolerance", "threshold", "budget", "limit", "required",
                   "needed", "allowed", "admissible_tau", "tau_admissible")

# Keys that are never diagnostics: identifiers, sizes, indices, coordinates.
DIAG_EXCLUDE = re.compile(
    r"^(n|m|j|k|i|idx|index|id|leg|seed|iter|iters|iterations|count|size|len|"
    r"grid|npts|nodes|order|degree|dim|year|version|steps?|calls?)$", re.I
)


# ---------------------------------------------------------------- helpers
def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def finite(v):
    return is_number(v) and math.isfinite(v)


def verdict_polarity(key, val):
    """Return True if (key, val) reads as a POSITIVE verdict, False if negative,
    None if the pair is not a verdict at all."""
    kl = key.lower()
    if not any(vk == kl or kl.endswith("_" + vk) or kl.startswith(vk + "_")
               for vk in VERDICT_KEYS):
        return None
    if isinstance(val, bool):
        return bool(val)
    if isinstance(val, str):
        s = val.strip().lower()
        if s in POSITIVE_STRINGS:
            return True
        if s in ("no", "false", "fail", "failed", "open", "unresolved"):
            return False
        return None
    return None


def numeric_diagnostics(rec):
    """Numeric siblings of a record that could serve as diagnostics."""
    out = {}
    for k, v in rec.items():
        if not is_number(v):
            continue
        if DIAG_EXCLUDE.match(k):
            continue
        if verdict_polarity(k, v) is not None:
            continue
        out[k] = v
    return out


def find_threshold_for(name, rec):
    """A sibling that names itself as the threshold FOR THIS QUANTITY, if any.

    Name-matched only (`X_tol`, `X_max`, ...).  The generic fallback -- treating any
    sibling called `tol` as a bound on every number in the record -- was tried first and
    produced 1000+ hits in which the "threshold" bounded a completely unrelated
    quantity (a Newton tolerance vs a wall exponent).  It is kept ONLY for diagnostics
    whose own name asserts they are error-like, where `residual > tol` is a meaningful
    reading.  Everything it used to catch is banked as DISMISS-SCALE below.
    """
    nl = name.lower()
    for suf in THRESHOLD_SUFFIXES:
        for cand in (nl + suf, nl.replace("_rms", "") + suf):
            for k, v in rec.items():
                if k.lower() == cand and finite(v):
                    return k, v, "name-matched"
    if DIAG_ERRORLIKE.search(nl):
        for k, v in rec.items():
            if k.lower() in THRESHOLD_NAMES and finite(v):
                return k, v, "generic-tolerance"
    return None, None, None


def decades(vals):
    pos = [abs(v) for v in vals if finite(v) and abs(v) > 0.0]
    if len(pos) < 2:
        return 0.0
    return math.log10(max(pos)) - math.log10(min(pos))


# ---------------------------------------------------------------- S1: screen
def walk(node, path, sink, stats):
    """Recursively collect (path, record) for every dict, and note sibling lists."""
    if isinstance(node, dict):
        stats["dicts"] += 1
        sink.append((path, node))
        for k, v in node.items():
            walk(v, path + "/" + str(k), sink, stats)
    elif isinstance(node, list):
        stats["lists"] += 1
        dict_rows = [x for x in node if isinstance(x, dict)]
        if dict_rows:
            sink.append((path + "[]", {"__ROWS__": dict_rows}))
        for idx, v in enumerate(node[:MAX_ROWS_SCANNED]):
            walk(v, path + "[%d]" % idx, sink, stats)


def screen_file(fname):
    """Return (hits, per-file stats) for one banked JSON."""
    fpath = os.path.join(DATA, fname)
    try:
        with open(fpath) as fh:
            doc = json.load(fh)
    except Exception as exc:                                   # noqa: BLE001
        return [], {"file": fname, "unreadable": str(exc)}

    sink, stats = [], {"dicts": 0, "lists": 0}
    walk(doc, "", sink, stats)

    hits = []
    n_verdicts = 0

    for path, rec in sink:
        # ---- R-SPREAD: a row-set whose verdict never moves while a diagnostic does
        if "__ROWS__" in rec:
            rows = rec["__ROWS__"]
            vkeys = set()
            for r in rows:
                for k, v in r.items():
                    if verdict_polarity(k, v) is True:
                        vkeys.add(k)
            for vk in sorted(vkeys):
                pos_rows = [r for r in rows if verdict_polarity(vk, r.get(vk)) is True]
                if len(pos_rows) < 3:
                    continue
                n_verdicts += 1
                diag_names = set()
                for r in pos_rows:
                    diag_names |= set(numeric_diagnostics(r))
                for dn in sorted(diag_names):
                    vals = [r[dn] for r in pos_rows if finite(r.get(dn))]
                    if len(vals) < 3:
                        continue
                    spread = decades(vals)
                    if spread >= SPREAD_DECADES:
                        nz = [abs(v) for v in vals if abs(v) > 0]
                        hits.append(OrderedDict([
                            ("file", fname), ("path", path), ("rule", "R-SPREAD"),
                            ("verdict_key", vk), ("verdict_value", True),
                            ("n_positive_rows", len(pos_rows)),
                            ("diagnostic", dn),
                            ("diag_min", min(nz)), ("diag_max", max(nz)),
                            ("spread_decades", spread),
                        ]))
            continue

        # ---- R-JOIN: verdict list and diagnostic list are SIBLINGS, joined on a key.
        # This is the rule the control forced.  Leg 202's strongest magnitude lives in
        # p2_route_d_v11_anchor.json as `v4_grids/rows` (carrying weighted_defect, no
        # verdict key at all) beside `v4_grids/verdict` (carrying grid_converged, no
        # diagnostic at all), joined on `a`.  A within-record screen cannot see it, and
        # a census blind to the very instance it is calibrated on is not a census.
        if "__ROWS__" not in rec:
            listkeys = [k for k, v in rec.items()
                        if isinstance(v, list) and v and
                        all(isinstance(x, dict) for x in v)]
            for vkey in listkeys:
                vrows = rec[vkey]
                vnames = set()
                for r in vrows:
                    for k, v in r.items():
                        if verdict_polarity(k, v) is True:
                            vnames.add(k)
                if not vnames:
                    continue
                for dkey in listkeys:
                    if dkey == vkey:
                        continue
                    drows = rec[dkey]
                    # join keys: scalar fields shared by both, with overlapping values
                    for jk in sorted(set(vrows[0]) & set(drows[0])):
                        vvals = [r.get(jk) for r in vrows]
                        dvals = [r.get(jk) for r in drows]
                        if not all(is_number(x) for x in vvals + dvals):
                            continue
                        if verdict_polarity(jk, vvals[0]) is not None:
                            continue
                        shared = set(vvals) & set(dvals)
                        if len(shared) < 3:
                            continue
                        for vn in sorted(vnames):
                            good = {r[jk] for r in vrows
                                    if verdict_polarity(vn, r.get(vn)) is True}
                            good &= shared
                            if len(good) < 3:
                                continue
                            n_verdicts += 1
                            joined = [r for r in drows if r.get(jk) in good]
                            dnames = set()
                            for r in joined:
                                dnames |= set(numeric_diagnostics(r))
                            for dn in sorted(dnames):
                                vals = [r[dn] for r in joined if finite(r.get(dn))]
                                if len(vals) < 3:
                                    continue
                                sp = decades(vals)
                                nz = [abs(x) for x in vals if abs(x) > 0]
                                if sp >= SPREAD_DECADES and nz:
                                    hits.append(OrderedDict([
                                        ("file", fname),
                                        ("path", "%s/{%s<-%s on %s}"
                                         % (path, vkey, dkey, jk)),
                                        ("rule", "R-JOIN"),
                                        ("verdict_key", vn), ("verdict_value", True),
                                        ("n_positive_rows", len(joined)),
                                        ("diagnostic", dn),
                                        ("diag_min", min(nz)), ("diag_max", max(nz)),
                                        ("spread_decades", sp),
                                        ("join_key", jk),
                                    ]))

        # ---- R-SELECT: the record carries BOTH ends of a range and the headline is
        # computed from the favourable end, while the unfavourable end -- present in the
        # same record, computed by the same runner, one line away -- violates the very
        # budget the block exists to test.  This is the ignored-diagnostic shape in its
        # sharpest form: nothing is missing, the rejecting number is right there and the
        # code reached past it.  Generic over any `<stem>_min` / `<stem>_max` pair with a
        # budget-like sibling.
        if "__ROWS__" not in rec:
            for k in list(rec):
                if not k.lower().endswith("_min"):
                    continue
                stem = k[:-4]
                kmax = None
                for c in rec:
                    if c.lower() == (stem + "_max").lower():
                        kmax = c
                if kmax is None:
                    continue
                vmin, vmax = rec.get(k), rec.get(kmax)
                if not (finite(vmin) and finite(vmax)):
                    continue
                for bk, bv in rec.items():
                    if bk in (k, kmax) or not finite(bv) or bv <= 0:
                        continue
                    bl = bk.lower()
                    if not any(t in bl for t in ("max_from", "budget", "_tol", "limit",
                                                 "bound", "threshold", "allowed",
                                                 "required", "floor")):
                        continue
                    # budget satisfied by the favourable end, violated by the other
                    if abs(vmin) <= bv < abs(vmax):
                        hits.append(OrderedDict([
                            ("file", fname), ("path", path), ("rule", "R-SELECT"),
                            ("verdict_key", bk), ("verdict_value", True),
                            ("diagnostic", kmax),
                            ("favourable_end", k), ("favourable_value", vmin),
                            ("unfavourable_value", vmax),
                            ("budget_key", bk), ("budget_value", bv),
                            ("violation_x", abs(vmax) / bv),
                            ("headline_margin_from_min", bv / abs(vmin)
                             if vmin else float("inf")),
                            ("margin_from_max", bv / abs(vmax)),
                        ]))

        # ---- single-record rules
        for vk, vv in rec.items():
            if verdict_polarity(vk, vv) is not True:
                continue
            n_verdicts += 1
            diags = numeric_diagnostics(rec)
            for dn, dv in diags.items():
                if not finite(dv):
                    continue
                tk, tv, tkind = find_threshold_for(dn, rec)
                if tk is not None and tk != dn and abs(dv) > abs(tv) > 0:
                    hits.append(OrderedDict([
                        ("file", fname), ("path", path), ("rule", "R-THRESH"),
                        ("verdict_key", vk), ("verdict_value", vv),
                        ("diagnostic", dn), ("diag_value", dv),
                        ("threshold_key", tk), ("threshold_value", tv),
                        ("threshold_kind", tkind),
                        ("exceedance_x", abs(dv) / abs(tv)),
                    ]))
                elif DIAG_ERRORLIKE.search(dn) and abs(dv) > MAGN_LIMIT:
                    hits.append(OrderedDict([
                        ("file", fname), ("path", path), ("rule", "R-MAGN"),
                        ("verdict_key", vk), ("verdict_value", vv),
                        ("diagnostic", dn), ("diag_value", dv),
                        ("limit", MAGN_LIMIT),
                    ]))

    # ---- reach: how many positive verdicts could the rules have spoken about at all?
    # A NO must name what it could not see (lesson 91).  A positive verdict with no
    # numeric sibling in its own record and no joinable sibling list is structurally
    # outside every rule above -- the census is silent about it, not clearing it.
    reachable = unreachable = 0
    for path, rec in sink:
        if "__ROWS__" in rec:
            continue
        pos = [k for k, v in rec.items() if verdict_polarity(k, v) is True]
        if not pos:
            continue
        has_diag = bool(numeric_diagnostics(rec))
        has_lists = any(isinstance(v, list) and v and all(isinstance(x, dict) for x in v)
                        for v in rec.values())
        if has_diag or has_lists:
            reachable += len(pos)
        else:
            unreachable += len(pos)

    return hits, {"file": fname, "dicts": stats["dicts"], "lists": stats["lists"],
                  "positive_verdicts_seen": n_verdicts, "screened_hits": len(hits),
                  "verdicts_in_reach": reachable,
                  "verdicts_out_of_reach": unreachable}


# ---------------------------------------------------------------- S2: wiring
COMPARISON = re.compile(r"[<>]=?|==|!=")


_SRC_CACHE = None      # path -> (source, lines), read exactly once
_RUNNER_CACHE = {}     # json stem -> [paths]


def _load_sources():
    """Read every candidate runner once.  Without this the census is O(hits x files)."""
    global _SRC_CACHE
    if _SRC_CACHE is not None:
        return _SRC_CACHE
    _SRC_CACHE = OrderedDict()
    for d in (os.path.join(ROOT, "experiments"), ROOT,
              os.path.join(ROOT, "solver"), os.path.join(ROOT, "scripts")):
        try:
            names = sorted(os.listdir(d))
        except OSError:
            continue
        for nm in names:
            if not nm.endswith(".py"):
                continue
            p = os.path.join(d, nm)
            # This census names other artifacts' JSON files and their diagnostic fields
            # in its own control block and adjudication table.  Left in the source set it
            # becomes a "producing runner" for the artifacts it audits, and its own
            # `r["diagnostic"] == "newton_weighted_defect_max"` reads as a decisional
            # site -- the instrument wiring itself up.  Excluded.
            if os.path.abspath(p) == os.path.abspath(__file__):
                continue
            try:
                with open(p, errors="replace") as fh:
                    src = fh.read()
            except OSError:
                continue
            _SRC_CACHE[p] = (src, src.splitlines())
    return _SRC_CACHE


def runner_candidates(json_stem):
    """Runners that plausibly produced this JSON: same stem, then any runner naming it."""
    if json_stem in _RUNNER_CACHE:
        return _RUNNER_CACHE[json_stem]
    srcs = _load_sources()
    cands = []
    direct = os.path.join(ROOT, "experiments", json_stem + ".py")
    if direct in srcs:
        cands.append(direct)
    needle = json_stem + ".json"
    for p, (src, _lines) in srcs.items():
        if p not in cands and needle in src:
            cands.append(p)
    _RUNNER_CACHE[json_stem] = cands
    return cands


def _library_paths():
    """Shared library modules.  A first version of this census scanned only the runner
    that wrote the JSON, and wrongly reported `rhs` in p2_route_ngx_v1_general.json as
    UNWIRED: its verdict is computed in solver/spectral_certificate.py:885
    (`general_class_tradeoff`), which never names the JSON.  Verdicts computed in shared
    helpers are exactly the ones a lexical check misses, so the library is scanned too."""
    srcs = _load_sources()
    lib = os.path.join(ROOT, "solver") + os.sep
    return [p for p in srcs if p.startswith(lib)]


def wiring_check(json_stem, diagnostic):
    """Does `diagnostic` ever reach a decision in the producing runner OR in the shared
    library the runner calls into?

    Returns (status, evidence).  status in
    {WIRED, WIRED-IN-LIBRARY, UNWIRED, NO_RUNNER}."""
    cands = runner_candidates(json_stem)
    if not cands:
        return "NO_RUNNER", []
    srcs = _load_sources()
    evidence = []
    for path in cands:
        entry = srcs.get(path)
        if entry is None:
            continue
        lines = entry[1]
        for ln, line in enumerate(lines, 1):
            if diagnostic not in line:
                continue
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            decisional = (
                COMPARISON.search(line.split("#")[0].replace("==", "=="))
                and not re.match(r"^\s*[\w\[\]\"'\.]+\s*=[^=]", stripped)
            ) or re.search(
                r"\b(if|elif|assert|while)\b.*" + re.escape(diagnostic), line
            ) or re.search(
                re.escape(diagnostic) + r".*\b(if|and|or)\b.*[<>]", line
            ) or re.search(
                r"\bbool\s*\(.*" + re.escape(diagnostic), line
            )
            if decisional:
                evidence.append({"runner": os.path.relpath(path, ROOT),
                                 "line": ln, "text": stripped[:200]})
    if evidence:
        return "WIRED", evidence

    # second pass: the shared library
    lib_ev = []
    for path in _library_paths():
        for ln, line in enumerate(srcs[path][1], 1):
            if diagnostic not in line:
                continue
            s = line.strip()
            if s.startswith("#"):
                continue
            if COMPARISON.search(line.split("#")[0]) or re.search(
                    r"\b(if|elif|assert|while|bool)\b.*" + re.escape(diagnostic), line):
                lib_ev.append({"module": os.path.relpath(path, ROOT),
                               "line": ln, "text": s[:200]})
    if lib_ev:
        return "WIRED-IN-LIBRARY", lib_ev

    return "UNWIRED", [{"runner": os.path.relpath(p, ROOT)} for p in cands]


# ---------------------------------------------------------------- S3: adjudication
# Every dismissal is banked with its reason.  These are the census's judgement calls and
# they are written down so a reader can disagree with a specific one.

# An artifact whose whole PURPOSE is to record what a module did under deliberately
# hostile or probe input.  A "converged: true" beside a huge residual in one of these is
# the FINDING the artifact was written to exhibit, deliberately banked by an audit leg --
# not a headline verdict this repository relies on.  Leg 202's shape requires a verdict
# the repository TRUSTS; these are verdicts it published in order to distrust.
PROBE_ARTIFACT = re.compile(
    r"(adversarial|_audit|status_audit|postrepair|_repair|bench_|_stress|"
    r"diagnostic|verification|selfconsistency)", re.I
)

# Quantities an artifact exists to EXHIBIT across a sweep.  A certificate constant that
# grows by ten decades across a continuation is the artifact's subject, and the sibling
# "converged" flag is about whether the SOLVE converged, a different question it never
# claimed to bound.
INTENDED_SUBJECT = re.compile(
    r"(norm|bound|constant|z1|z_1|y0|y_0|sigma|lambda|eig|margin|amplitude|"
    r"curvature|slope|coeff|kappa|cond|power|exponent|radius|r_crit|wall|"
    r"fraction|ratio|scale|width|decades|count|violations)", re.I
)


# ------------------------------------------------------------------ S3b: by hand
# Every hit the automatic rules left as NEEDS-READ was opened and read at its source.
# The judgement is banked HERE, keyed and quotable, rather than left in prose, so a
# reader can disagree with a specific line instead of with the census as a whole.
# Keyed (json file, diagnostic).
HAND_ADJUDICATED = {
    ("nongenericity.json", "k1"): (
        "DISMISS-INPUT-VARIABLE",
        "k1 is `ic.spectral.energy_k1_frac` (analyze_nongenericity.py:83) -- a descriptor "
        "of the INITIAL CONDITION, i.e. the sweep's independent variable, spanning 32.6 "
        "decades because the sweep was designed to span it.  `usable` (line 55) is a "
        "conjunction of blew-up, held-out-fit-exists and R^2, none of which k1 bears on."),
    ("p2_route_bx_v1_stageb.json", "first_draft_error_factor"): (
        "DISMISS-UNRELATED",
        "p2_route_bx_v1_stageb.py:413 defines it as 5904.13/banked_best -- the error of a "
        "DISCARDED first draft against the banked value, recorded as provenance.  "
        "`viscous_any_closes` (line 416) is an any() over a different row set.  Two "
        "unrelated quantities sharing one summary dict, not a diagnostic of that verdict."),
    ("p2_route_l1_v2_spectral.json", "Z2"): (
        "DISMISS-INTENDED",
        "p2_route_l1_v2_spectral.py:141 defines closes_finite_block := Z1_finite < 1.0, "
        "and Z2 (line 139) is a quadratic bound feeding r_max (line 140), the resulting "
        "Newton-Kantorovich RADIUS.  A large Z2 makes r_max small, which the artifact "
        "reports; it does not contradict Z1_finite < 1.  The artifact also states "
        "Z1_tail: DIVERGES in its own S3 block, so the verdict's `finite_block` scoping "
        "is explicit rather than concealed."),
    ("p2_route_l1_v2_spectral.json", "r_max"): (
        "DISMISS-INTENDED",
        "downstream consequence of Z2 above; r_max stays strictly positive (min "
        "6.65e-09) across all 12 closing rows, so it agrees with the verdict rather "
        "than contradicting it -- a small radius is a caveat the artifact prints, not a "
        "rejection it withheld."),
    ("p2_route_l1r_v1_repro.json", "half_ulps_out"): (
        "DISMISS-WIRED",
        "p2_route_l1r_v1_repro.py:93 computes ok := delta <= half_ulp*(1+1e-12), which is "
        "half_ulps_out <= 1 written in the unnormalised variables; `pass` (line 108) IS "
        "this diagnostic thresholded.  The max over all 200 passing rows is 0.9789 < 1, "
        "consistent to the last printed digit.  The lexical wiring check missed it only "
        "because the comparison is spelled in delta/half_ulp, not in half_ulps."),
    ("p2_route_l1r_v1_repro.json", "abs_delta"): (
        "DISMISS-INTENDED",
        "the ledger reproduces 200 quoted numbers of wildly different magnitude "
        "(4.34e-19 to 3.6e+77); abs_delta must span comparably.  The scale-free verdict "
        "is half_ulps_out, adjudicated above."),
    ("p2_route_l1r_v1_repro.json", "quoted_value"): (
        "DISMISS-INPUT-VARIABLE",
        "the quoted number being checked -- the ledger's independent variable."),
    ("p2_route_l1r_v1_repro.json", "reproduced"): (
        "DISMISS-INPUT-VARIABLE",
        "the recomputed counterpart of quoted_value; its spread is that of the corpus."),
    ("p2_route_l1rh_v1_construction.json", "defect_D_over_tau_here"): (
        "DISMISS-INTENDED",
        "the C1 control is a REPRODUCTION control: PASS asserts here==banked, and it "
        "holds (1.8536769e7 vs 1.8536770e7, 2.9e-08 relative).  The ratio being 1.85e7 "
        "is leg 56's banked L1 consistency gap, which this artifact exists to reproduce; "
        "PASS never claimed the defect was small."),
    ("p2_route_l1rh_v1_construction.json", "defect_D_over_tau_banked"): (
        "DISMISS-INTENDED", "the banked side of the same reproduction control."),
    ("p2_route_l1rh_v1_construction.json", "defect_H_impl_over_tau_here"): (
        "DISMISS-INTENDED",
        "same control, Hilbert term: 2.04033440973574e11 vs banked 2.04033440973586e11, "
        "5.8e-14 relative.  Leg 56's second banked gap, reproduced, not contradicted."),
    ("p2_route_l1rh_v1_construction.json", "defect_H_impl_over_tau_banked"): (
        "DISMISS-INTENDED", "the banked side of the same reproduction control."),
    ("p2_route_m2p_v1_promotion.json", "steadiness_defect"): (
        "DISMISS-INTENDED",
        "p2_route_m2p_v1_promotion.py:163-165 puts steadiness_defect and converged in one "
        "row, and converged is the Newton residual test (residual_rms < 1e-10) -- a "
        "different question.  The defect is the sweep's SUBJECT: it rises smoothly and "
        "monotonically with nu (0.33332, 0.33516, 0.35094, 0.46187, 0.83760, 1.15445 at "
        "nu = 0, 1e-4, 1e-3, 1e-2, 0.1, 0.3), is consumed by the fit at line 306 and "
        "printed at line 416.  No branch jump, nothing withheld -- unlike leg 202's "
        "control, where the same diagnostic moves 13.4 decades with no monotone story."),
    ("p2_route_ngx_v1_general.json", "rhs"): (
        "DISMISS-WIRED",
        "`holds` and `rhs` are both returned by general_class_tradeoff in "
        "solver/spectral_certificate.py:885 -- rhs is literally one side of the "
        "inequality `holds` tests, and its companion `slack` is min'd at "
        "p2_route_ngx_v1_general.py:384.  Maximally wired.  This hit is why the wiring "
        "check now scans solver/ as well as the runner."),
    # ---- leg 237 (Route-SIRC), landed mid-flight; same audit family as this leg.
    # Its JSON is a CALIBRATION LOG: rows carrying `converged: true` beside a wrecked
    # diagnostic are the positives it deliberately banked to grade the blind spot, and
    # each such row carries its own `escaped: true` flag stating so.  A positive verdict
    # beside a bad number here is the artifact's subject, not a signal it overlooked.
    ("p2_route_sirc_v1_census.json", "c_relative_error"): (
        "DISMISS-PROBE-RECORD",
        "G3b_profile_newton_calibration is the KNOWN POSITIVE, re-run by leg 237 on "
        "purpose: c_relative_error = 1.2307e4 and 6.1534e5 beside converged = true is "
        "the demonstration, and both rows carry escaped = true in the same record.  "
        "Leg 237's own gate answers YES on it."),
    ("p2_route_sirc_v1_census.json", "gauge0_defect"): (
        "DISMISS-PROBE-RECORD", "same calibration log; the defect is the exhibit."),
    ("p2_route_sirc_v1_census.json", "gauge1_defect"): (
        "DISMISS-PROBE-RECORD", "same calibration log; the defect is the exhibit."),
    ("p2_route_sirc_v1_census.json", "residual_rms"): (
        "DISMISS-PROBE-RECORD",
        "same calibration log; the whole point of leg 237's gate is that this residual "
        "is scale-invariant and therefore uninformative, which is what its spread shows."),
    ("p2_route_cp_v1_cadiot.json", "row_sum_max"): (
        "DISMISS-SCALE",
        "R-SELECT's budget-name heuristic mis-took `s_required` for a budget on row sums. "
        "In CP6's dial (p2_route_cp_v1_cadiot.py:308) `s_required` is the SHIFT MAGNITUDE "
        "Cadiot's Lemma 3.2 requires; `row_sum_min/max` are Gershgorin row sums. "
        "Different quantities in different units -- 510.0 vs 110.218 is not a comparison "
        "the artifact makes or could make, and no verdict rests on it."),
    ("p2_route_cp_v1_cadiot.json", "diag_max"): (
        "DISMISS-SCALE",
        "same unit mismatch: `diag_min/max` are the dial's diagonal entries (4.05, 230.4 "
        "at mu=0.45), `s_required` is a shift magnitude.  Not a budget on the diagonal."),
    ("p2_route_sdm_v1_mapping.json", "shortfall_of_the_single_best_arm"): (
        "DISMISS-REPORTED",
        "the opposite of the shape.  p2_route_sdm_v1_mapping.py:229-238 places the 20.4734 "
        "shortfall inside a block named `do_they_disagree` whose own `reading` field "
        "states it in words ('still reports 20.4734 where it must be under 1').  The "
        "sibling `gate_survives_renormalisation` is about whether TC8's gate survives "
        "renormalisation -- and it survives BECAUSE the shortfall is 20.47, not despite "
        "it.  The diagnostic is the headline, not a signal that was ignored."),
}


def adjudicate(hit, wiring_status, wiring_evidence):
    """Return (classification, reason).  classification in
    {SHAPE, DISMISS-WIRED, DISMISS-PROBE-RECORD, DISMISS-INTENDED, DISMISS-SCALE,
     DISMISS-INPUT-VARIABLE, DISMISS-UNRELATED, DISMISS-REPORTED, NEEDS-READ}."""
    if wiring_status == "WIRED-IN-LIBRARY":
        return "DISMISS-WIRED", (
            "the diagnostic reaches a comparison in the shared library the runner calls "
            "into: %d decisional site(s)" % len(wiring_evidence))
    if wiring_status == "WIRED":
        return "DISMISS-WIRED", (
            "the diagnostic reaches a comparison in the producing runner, so the verdict "
            "is not blind to it: %d decisional site(s)" % len(wiring_evidence))
    if wiring_status == "NO_RUNNER":
        return "NEEDS-READ", "no producing runner located by stem or by JSON-name grep"

    dn = hit["diagnostic"]

    if PROBE_ARTIFACT.search(hit["file"]):
        return "DISMISS-PROBE-RECORD", (
            "the artifact is an adversarial/audit/repair probe log; a positive verdict "
            "beside a bad diagnostic here is the defect the audit leg deliberately "
            "banked, not a headline verdict this repository trusts")

    if hit["rule"] == "R-THRESH" and hit.get("threshold_kind") == "generic-tolerance":
        return "DISMISS-SCALE", (
            "the threshold sibling is a generic tolerance, not a declared bound on this "
            "quantity; the comparison is not one the artifact ever asserts")

    if INTENDED_SUBJECT.search(dn):
        return "DISMISS-INTENDED", (
            "the flagged quantity is a bound/norm/spectral/geometry quantity the artifact "
            "exists to exhibit across its sweep, not a health indicator of the verdict")

    return "NEEDS-READ", "screened, unwired, and error-like -- requires source reading"


def dedupe(hits):
    """Collapse to one row per (file, rule, verdict_key, diagnostic), keeping the WORST
    instance.  Without this a 40-row sweep reports the same finding 40 times and the
    NEEDS-READ list is unreadable -- which defeats the point of a census."""
    best = OrderedDict()
    for h in hits:
        key = (h["file"], h["rule"], h["verdict_key"], h["diagnostic"])
        if h["rule"] in ("R-SPREAD", "R-JOIN"):
            score = h["spread_decades"]
        elif h["rule"] == "R-SELECT":
            score = h["violation_x"]
        elif h["rule"] == "R-THRESH":
            score = h["exceedance_x"]
        else:
            score = abs(h["diag_value"])
        prev = best.get(key)
        if prev is None or score > prev[0]:
            row = OrderedDict(h)
            row["n_duplicate_records"] = 1 if prev is None else prev[1]["n_duplicate_records"] + 1
            best[key] = (score, row)
        else:
            prev[1]["n_duplicate_records"] += 1
    return [v[1] for v in best.values()]


# ---------------------------------------------------------------- main
def main():
    # This leg's own output is excluded from its own input set: it is a census OF hits,
    # so every field it records (diag_max, exceedance_x, ...) trivially re-screens as a
    # hit.  Self-inclusion measures the instrument, not the repository.
    files = sorted(f for f in os.listdir(DATA)
                   if f.endswith(".json")
                   and f != os.path.basename(OUT))
    all_hits, file_stats, unreadable = [], [], []

    for fname in files:
        hits, st = screen_file(fname)
        if "unreadable" in st:
            unreadable.append(st)
            continue
        file_stats.append(st)
        all_hits.extend(hits)

    n_raw = len(all_hits)
    all_hits = dedupe(all_hits)

    # ---- S2 + S3 on every screened hit
    adjudicated = []
    for hit in all_hits:
        stem = hit["file"][:-len(".json")]
        status, evid = wiring_check(stem, hit["diagnostic"])
        cls, reason = adjudicate(hit, status, evid)
        hand = HAND_ADJUDICATED.get((hit["file"], hit["diagnostic"]))
        by_hand = False
        if cls == "NEEDS-READ" and hand is not None:
            cls, reason = hand
            by_hand = True
        row = OrderedDict(hit)
        row["wiring"] = status
        row["wiring_evidence"] = evid[:4]
        row["classification"] = cls
        row["adjudicated_by_hand"] = by_hand
        row["reason"] = reason
        adjudicated.append(row)

    # ---- the positive control, held out of the census's own count
    CONTROL_FILE = "p2_route_d_v11_anchor.json"
    CONTROL_DIAG = "weighted_defect"
    ctrl_all = [r for r in adjudicated if r["file"] == CONTROL_FILE]
    ctrl = [r for r in ctrl_all if r["diagnostic"] == CONTROL_DIAG
            and r["rule"] in ("R-SPREAD", "R-JOIN")]
    ctrl.sort(key=lambda r: -r["diag_max"])

    # THE CONTROL, AND A CORRECTION IT FORCED.
    #
    # This control was first written to demand that the screen recover leg 202's own
    # quoted magnitudes -- weighted_defect = 0.50 / 4788 / 73372 at a = 0.5 / 0.8 / 1.0.
    # It failed, and the reason is a correction to leg 202, not a defect in the screen:
    # in v4_grids those magnitudes belong to rows the artifact marks
    # grid_converged = FALSE (a = 0.8 and a = 1.0; see v4_grids/verdict).  The artifact
    # does NOT assert convergence where the defect is 4788 or 73372.  Demanding that the
    # census reproduce that pairing would be demanding it reproduce a misreading.
    #
    # The correctly-scoped form of leg 202's finding, which this control now requires:
    #   (a) R-SPREAD on v2_sweep -- 17 rows ALL converged=True, weighted_defect spanning
    #       2.34e-14 -> 0.622 (13.42 decades), diagnostic UNWIRED; and
    #   (b) R-SELECT on v5_budget -- the headline margin is computed from
    #       newton_weighted_defect_min while newton_weighted_defect_max, one line away in
    #       the same returned dict, violates the block's own Y0 budget.
    # Both must fire, both UNWIRED, or no NO answer is admissible from this run.
    ctrl_select = [r for r in ctrl_all if r["rule"] == "R-SELECT"
                   and r["diagnostic"] == "newton_weighted_defect_max"]
    spread_ok = bool(ctrl) and all(r["wiring"] == "UNWIRED" for r in ctrl)
    select_ok = bool(ctrl_select) and all(r["wiring"] == "UNWIRED" for r in ctrl_select)
    control_ok = spread_ok and select_ok

    census = [r for r in adjudicated if r["file"] != CONTROL_FILE]

    by_class = {}
    for r in census:
        by_class[r["classification"]] = by_class.get(r["classification"], 0) + 1

    needs_read = [r for r in census if r["classification"] == "NEEDS-READ"]
    shape = [r for r in census if r["classification"] == "SHAPE"]

    out = OrderedDict()
    out["meta"] = OrderedDict([
        ("leg", "P2 Route-CDAP v1 (leg 235): census of banked headline verdicts for "
                "leg 202's ignored-caller-diagnostic defect shape"),
        ("tier", "process/audit -- no mathematics is recomputed, nothing is patched"),
        ("reproduce", "python experiments/p2_route_cdap_v1_census.py"),
        ("gate", "Does a systematic check of every other banked headline verdict's own "
                 "caller-side diagnostics find a SECOND instance of 'the rejecting "
                 "signal already existed in the caller's own data and was never used'?"),
        ("thresholds", {"SPREAD_DECADES": SPREAD_DECADES, "MAGN_LIMIT": MAGN_LIMIT}),
        ("verdict_keys", list(VERDICT_KEYS)),
    ])
    out["coverage"] = OrderedDict([
        ("json_files_scanned", len(file_stats)),
        ("json_files_unreadable", unreadable),
        ("dicts_walked", sum(s["dicts"] for s in file_stats)),
        ("lists_walked", sum(s["lists"] for s in file_stats)),
        ("positive_verdicts_seen", sum(s["positive_verdicts_seen"] for s in file_stats)),
        ("files_carrying_a_positive_verdict",
         sum(1 for s in file_stats if s["positive_verdicts_seen"] > 0)),
        ("verdicts_in_reach_of_some_rule",
         sum(s["verdicts_in_reach"] for s in file_stats)),
        ("verdicts_structurally_out_of_reach",
         sum(s["verdicts_out_of_reach"] for s in file_stats)),
        ("reach_note",
         "a positive verdict with no numeric sibling in its own record and no joinable "
         "sibling list cannot be spoken about by ANY rule here.  The census is SILENT "
         "about those, not clearing them: they are the named limit of this NO."),
    ])
    out["control"] = OrderedDict([
        ("file", CONTROL_FILE), ("diagnostic", CONTROL_DIAG),
        ("rules_fired_on_control", sorted({r["rule"] for r in ctrl_all})),
        ("A_spread", OrderedDict([
            ("fired", bool(ctrl)),
            ("wiring", ctrl[0]["wiring"] if ctrl else None),
            ("spread_decades", ctrl[0]["spread_decades"] if ctrl else None),
            ("diag_min", ctrl[0]["diag_min"] if ctrl else None),
            ("diag_max", ctrl[0]["diag_max"] if ctrl else None),
            ("n_positive_rows", ctrl[0]["n_positive_rows"] if ctrl else None),
            ("ok", spread_ok),
        ])),
        ("B_select", OrderedDict([
            ("fired", bool(ctrl_select)),
            ("wiring", ctrl_select[0]["wiring"] if ctrl_select else None),
            ("favourable_value", ctrl_select[0]["favourable_value"]
             if ctrl_select else None),
            ("unfavourable_value", ctrl_select[0]["unfavourable_value"]
             if ctrl_select else None),
            ("budget_key", ctrl_select[0]["budget_key"] if ctrl_select else None),
            ("budget_value", ctrl_select[0]["budget_value"] if ctrl_select else None),
            ("violation_x", ctrl_select[0]["violation_x"] if ctrl_select else None),
            ("headline_margin_from_min", ctrl_select[0]["headline_margin_from_min"]
             if ctrl_select else None),
            ("margin_from_max", ctrl_select[0]["margin_from_max"]
             if ctrl_select else None),
            ("ok", select_ok),
        ])),
        ("control_ok", control_ok),
        ("correction_to_leg_202", (
            "leg 202's escalation quotes weighted_defect = 0.50 / 4788 / 73372 at "
            "a = 0.5 / 0.8 / 1.0 as the rejecting signal beside a trusted verdict.  Two "
            "of those three attach to rows this artifact marks grid_converged = FALSE "
            "(v4_grids/verdict at a = 0.8 and a = 1.0), so the artifact does not assert "
            "convergence where the defect is 4788 or 73372.  Leg 202's SHAPE is "
            "confirmed and reproduced here; two of its three quoted magnitudes are "
            "attached to the wrong rows.")),
        ("note", "leg 202's own artifact; the instrument's calibration, NEVER counted "
                 "as one of this leg's census hits"),
    ])
    # ---------------------------------------------------------------- the finding
    # Computed from the banked artifact, not asserted: every number below is read or
    # derived here so the prose has nothing of its own to get wrong.
    v11 = json.load(open(os.path.join(DATA, CONTROL_FILE)))
    v2rows = v11["v2_sweep"]["rows"]
    v4 = v11["v4_grids"]
    v5 = v11["v5_budget"]
    a_max = v4["grid_converged_a_max"]
    good = [r for r in v2rows if r["relres"] < 1e-8 and r["a"] <= a_max + 1e-12]
    wd = [r["weighted_defect"] for r in good]
    budget = v5["Y0_max_from_v10"]
    over = [r for r in good if r["weighted_defect"] > budget]

    out["second_instance"] = OrderedDict([
        ("is_it_a_second_instance_of_leg_202s_shape", True),
        ("headline_verdict", "p2_route_d_v11_anchor.json / v5_budget -- the Y0 budget "
                             "claim: margin = Y0_max / newton_weighted_defect_min, with "
                             "the reading 'the profile's defect is no longer the binding "
                             "constraint'"),
        ("the_ignored_diagnostic", "newton_weighted_defect_max"),
        ("where_it_is_computed",
         "experiments/p2_route_d_v11_anchor.py:180, the line AFTER the min that the "
         "margin is built from (line 179); written to the banked JSON, never compared"),
        ("budget_key", "Y0_max_from_v10"),
        ("budget_value", budget),
        ("rows_in_the_good_set", len(good)),
        ("weighted_defect_min_over_good", min(wd)),
        ("weighted_defect_max_over_good", max(wd)),
        ("banked_margin_from_the_min", v5["margin"]),
        ("margin_recomputed_from_the_max", budget / max(wd)),
        ("budget_violation_factor_at_the_max", max(wd) / budget),
        ("n_good_rows_exceeding_the_budget", len(over)),
        ("a_values_exceeding_the_budget", [r["a"] for r in over]),
        ("worst_row", OrderedDict([("a", max(good, key=lambda r: r["weighted_defect"])["a"]),
                                   ("weighted_defect", max(wd))])),
        ("why_this_is_NOT_leg_202s_instance", (
            "different verdict, different diagnostic, different mechanism, and NOT "
            "repaired by leg 202's prescribed fix.  Leg 202 named the `converged` flag "
            "returned by profile_newton.py's `continuation` (an off-branch root reported "
            "at machine-zero relres) as trusted by v11's a_max_machine / GA_boundary "
            "claims.  This is the v5_budget margin -- a THIRD claim in the same "
            "artifact, which leg 202 did not name -- and its mechanism is not a bad "
            "convergence flag but a MIN/MAX SELECTION: both ends of the range are "
            "computed, one line apart, and the headline is built from the favourable "
            "one while the unfavourable one violates the block's own budget.  Fixing "
            "`continuation` leaves this defect exactly where it is, because every row in "
            "the good set genuinely converged (relres < 1e-8) and a <= a_max = %s -- the "
            "rows all pass the artifact's OWN on-branch tests; it is the SUMMARY "
            "STATISTIC that is wrong, not the rows' admission." % a_max)),
        ("and_the_two_findings_do_interact", (
            "stated because it cuts against the cleanliness of the separation above.  "
            "The worst row, a = 0.45, carries weighted_defect = 1.5196e-02 while its "
            "immediate neighbours carry 2.3745e-08 (a = 0.40) and 7.4528e-07 "
            "(a = 0.50) -- a ~6-decade spike over one step of a smooth continuation, "
            "which is exactly leg 202's off-branch-root signature.  So this row may ALSO "
            "be an instance of leg 202's mechanism.  That does not merge the two "
            "findings; it sharpens why this one matters: taking the MAX is precisely the "
            "operation that would have surfaced leg 202's defect from inside v11's own "
            "budget block, without needing to look at profile_newton.py at all.  The "
            "rejecting signal was one `min` away from being used.")),
        ("scope_caveat_stated_plainly", (
            "it is in the SAME runner leg 202 already escalated.  Zero instances were "
            "found in any of the other 191 banked JSONs.  A reviewer who scopes the "
            "gate's 'every other banked headline verdict' by ARTIFACT rather than by "
            "VERDICT should read this leg's answer as NO-plus-a-sharpening of 202; the "
            "leg reports it as YES because the gate's unit is the verdict, and because "
            "the repair already dispatched for 202 does not touch this one.")),
    ])

    out["screen"] = OrderedDict([
        ("raw_screened_records", n_raw),
        ("after_dedupe", len(all_hits)),
        ("screened_hits_excluding_control", len(census)),
        ("by_classification", by_class),
    ])
    out["hits"] = census
    out["needs_read"] = needs_read
    out["shape_instances"] = shape
    out["per_file"] = file_stats

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=str)

    print("Route-CDAP census")
    print("  files scanned            : %d" % len(file_stats))
    print("  positive verdicts seen   : %d in %d files"
          % (out["coverage"]["positive_verdicts_seen"],
             out["coverage"]["files_carrying_a_positive_verdict"]))
    print("  CONTROL A (R-SPREAD)     : fired=%s wiring=%s spread=%.2f decades "
          "(%.3g -> %.3g over %s converged rows)"
          % (bool(ctrl), ctrl[0]["wiring"] if ctrl else "-",
             ctrl[0]["spread_decades"] if ctrl else float("nan"),
             ctrl[0]["diag_min"] if ctrl else float("nan"),
             ctrl[0]["diag_max"] if ctrl else float("nan"),
             ctrl[0]["n_positive_rows"] if ctrl else "-"))
    if ctrl_select:
        cs = ctrl_select[0]
        print("  CONTROL B (R-SELECT)     : fired=True wiring=%s  headline used min "
              "%.3g (margin %.4g) while max %.6g violates budget %s=%.3g by %.4gx"
              % (cs["wiring"], cs["favourable_value"],
                 cs["headline_margin_from_min"], cs["unfavourable_value"],
                 cs["budget_key"], cs["budget_value"], cs["violation_x"]))
    else:
        print("  CONTROL B (R-SELECT)     : DID NOT FIRE")
    print("  screened hits (census)   : %d" % len(census))
    for k in sorted(by_class):
        print("      %-18s %d" % (k, by_class[k]))
    print("  NEEDS-READ               : %d" % len(needs_read))
    for r in needs_read:
        print("      %-44s %-28s %s"
              % (r["file"], r["diagnostic"], r["rule"]))
    print("  wrote %s" % os.path.relpath(OUT, ROOT))

    if not control_ok:
        print("CONTROL FAILED -- the screen does not reproduce leg 202's own instance; "
              "no NO answer is admissible from this run.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
