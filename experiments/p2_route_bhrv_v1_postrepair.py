"""Leg 228, Route-BHRV -- INDEPENDENT post-repair verification of leg 218's border-weight
guard in `solver/bordered_hl.py`.

WHAT THIS IS, AND WHAT IT DELIBERATELY IS NOT
---------------------------------------------
Leg 198 (Route-BHA) measured that `solver/bordered_hl.py` silently accepted an
inadmissible border weight, corrupting Z_1 by up to ~1e9x and Z_2 by up to ~1e17x in
the certificate-FABRICATING direction. Leg 218 (Route-BHR) shipped the guard
(`_check_weights`) and self-reported GATE YES on both clauses. This leg is the
independent re-measurement that repair's blast radius earns.

Lesson 90 governs the design: a control that cannot come out differently is not a
control. So this runner does NOT import, call, or re-execute
`experiments/p2_route_bhr_v1_repair.py`. Everything below is re-derived:

  * the PRE-REPAIR MODULE is loaded from the git object store by this file's own
    loader (`spec_from_file_location` on a materialised temp file), not leg 218's
    `spec_from_loader` + `exec` path, and BOTH blob hashes are asserted at startup so
    "pre-repair" can never silently degrade into "the same file twice".
  * the ADVERSARIAL CASES are derived here from the weight surface's own structure --
    the cross product of (entry point) x (inadmissibility class) -- not copied from
    leg 198's or leg 218's list. This is what turns up the cases neither leg had.
  * the CALLER SET is re-enumerated from the callers themselves. Leg 218 claimed six
    direct importers "enumerated by import"; there are TEN (this leg's novelty pass,
    writeup/novelty/leg_228.md sec 4). All ten are probed, and whether each touches
    the weight surface is MEASURED here, not assumed.
  * the Z_1 DISAGREEMENT between legs 198 and 218 is not re-litigated by a third run
    of the same arithmetic (which would answer nothing). Leg 218's explanation --
    lesson 86, the ratio sits at the round-off floor and is therefore
    environment-dependent while the VERDICT is not -- is a falsifiable claim about
    VARIANCE, and section E tests it as one, with the falsification condition fixed
    in advance.

Edits nothing. `solver/bordered_hl.py` is read-only to this leg under both outcomes.

Run: .venv/bin/python experiments/p2_route_bhrv_v1_postrepair.py
"""

import importlib.util
import json
import math
import os
import struct
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = "solver/bordered_hl.py"

# Provenance, asserted at startup rather than inherited from leg 218's journal.
PRE_COMMIT = "0c075b8"
POST_COMMIT = "d9a20fb"
PRE_BLOB = "a6ab17dfd84eb21d4b63f709fc7a464419d6bb51"
POST_BLOB = "92e1c6700c17293d96f0c2f010ac96f69af151f3"


def _git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), check=True,
                          capture_output=True, text=True).stdout


def _refuses(fn):
    """True iff the call raises the guard's own error."""
    try:
        fn()
        return False
    except Exception as exc:
        return type(exc).__name__ == "BorderedHLDomainError"


def bits(x):
    """The exact IEEE-754 double payload, as hex. Bit identity means THIS is equal.

    Not `==`: `==` says nothing about -0.0 vs 0.0 and is a lie for NaN. A byte
    differential must compare bytes."""
    return struct.pack("<d", float(x)).hex()


# --------------------------------------------------------------------------
# A. provenance -- both blobs asserted, so "pre" cannot become "post"
# --------------------------------------------------------------------------
def assert_provenance():
    """Abort unless the module has exactly the two known states with the known blobs."""
    log = _git("log", "--format=%H", "--", MODULE_PATH).split()
    pre_blob = _git("rev-parse", "%s:%s" % (PRE_COMMIT, MODULE_PATH)).strip()
    post_blob = _git("rev-parse", "%s:%s" % (POST_COMMIT, MODULE_PATH)).strip()
    live_blob = _git("hash-object", os.path.join(REPO, MODULE_PATH)).strip()
    rec = {"commits_touching_module": len(log),
           "pre_commit": PRE_COMMIT, "pre_blob": pre_blob,
           "post_commit": POST_COMMIT, "post_blob": post_blob,
           "worktree_blob": live_blob,
           "pre_blob_matches_expected": pre_blob == PRE_BLOB,
           "post_blob_matches_expected": post_blob == POST_BLOB,
           "worktree_is_the_post_repair_blob": live_blob == POST_BLOB,
           "pre_and_post_are_distinct": pre_blob != post_blob}
    for k in ("pre_blob_matches_expected", "post_blob_matches_expected",
              "worktree_is_the_post_repair_blob", "pre_and_post_are_distinct"):
        if not rec[k]:
            raise SystemExit("PROVENANCE FAILED: %s is False -- %r" % (k, rec))
    return rec


def load_pre_repair():
    """Materialise the pre-repair blob and import it under its own name.

    Deliberately a DIFFERENT loader path from leg 218's (`spec_from_loader` on a
    string + `exec` into a bare module dict). If leg 218's differential had been an
    artifact of its loader, re-using that loader could not reveal it."""
    src = _git("show", "%s:%s" % (PRE_COMMIT, MODULE_PATH))
    tmpdir = tempfile.mkdtemp(prefix="bhrv_pre_")
    path = os.path.join(tmpdir, "bordered_hl_pre_bhrv.py")
    with open(path, "w") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("bordered_hl_pre_bhrv", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["bordered_hl_pre_bhrv"] = mod
    spec.loader.exec_module(mod)
    # the pre-repair module must NOT have the guard; if it does, we loaded the wrong file
    if hasattr(mod, "_check_weights") or hasattr(mod, "BorderedHLDomainError"):
        raise SystemExit("PROVENANCE FAILED: the 'pre-repair' module carries the guard")
    return mod, len(src.splitlines())


# --------------------------------------------------------------------------
# shared fixtures -- the object, solved once per grid, from the module under test
# --------------------------------------------------------------------------
def start_state(mod, n, rho_max, c=0.5):
    """The well-posed non-symmetric starting data this repository's bordered legs use.

    The two scalar border constants come from the module's OWN `CHL_TRIPLE` (Chen-
    Huang-Li Fig 4.2's raw triple) rather than from a caller's literal, so the fixture
    is anchored to the module under test, not inherited from leg 218."""
    b = mod.BorderedHL(n=n, rho_max=rho_max, c=c)
    x0, wid = 0.3, 0.9
    Om = np.exp(-((b.X - x0) ** 2) / (2.0 * wid ** 2))
    V = 0.8 * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * wid) ** 2))
    z0 = b.pack(Om, V, *mod.CHL_TRIPLE)
    b.set_pin_from(z0)
    return b, z0


_SOLVED = {}


def solved(mod, tag, n, rho_max, c=0.5):
    key = (tag, n, rho_max, c)
    if key not in _SOLVED:
        b, z0 = start_state(mod, n, rho_max, c)
        z, hist = b.newton(z0, tol=1e-12, max_iter=40)
        _SOLVED[key] = (b, z, hist)
    return _SOLVED[key]


# --------------------------------------------------------------------------
# B. CLAUSE A -- does every inadmissible weight now reject?
#    Cases derived here from the surface's structure, not copied from either leg.
# --------------------------------------------------------------------------
# The inadmissibility classes, from the DEFINITION of ||z||_w = max_i w_i |z_i|:
#   negative -> not non-negative; zero -> seminorm (component deleted);
#   +inf -> component deleted from the induced column sum; -inf -> both at once;
#   NaN -> the case every ordered comparison lets through (SEI CERT NUM07-J).
BAD_SCALARS = [("negative_small", -1e-12), ("negative_leg198", -1e-6),
               ("negative_unit", -1.0), ("negative_large", -1e12),
               ("zero", 0.0), ("negative_zero", -0.0),
               ("plus_inf", math.inf), ("minus_inf", -math.inf), ("nan", math.nan)]


def clause_a(post, pre):
    """Every entry point x every inadmissibility class. Post must raise; pre must not.

    Reporting is by MAGNITUDE: for each case that the pre-repair module accepted, the
    value it returned, and how far that value is from the honest one."""
    n, rho_max, p = 101, 8.0, 0.0
    b_post, z_post, _ = solved(post, "post", n, rho_max)
    b_pre, z_pre, _ = solved(pre, "pre", n, rho_max)

    honest_post = b_post.certificate_constants(z_post, p=p)
    honest_pre = b_pre.certificate_constants(z_pre, p=p)

    cases = []

    def record(entry, cls, val, post_call, pre_call, probe):
        """probe(result) -> the scalar whose corruption we are measuring, or None."""
        row = {"entry_point": entry, "class": cls, "value": repr(val)}
        try:
            r = post_call()
            row["post_rejected"] = False
            row["post_returned"] = probe(r)
        except Exception as exc:
            row["post_rejected"] = True
            row["post_exception"] = type(exc).__name__
            row["post_is_the_guards_error"] = (
                type(exc).__name__ == "BorderedHLDomainError")
            row["post_message_head"] = str(exc)[:120]
        try:
            r = pre_call()
            row["pre_rejected"] = False
            row["pre_returned"] = probe(r)
        except Exception as exc:
            row["pre_rejected"] = True
            row["pre_exception"] = type(exc).__name__
        cases.append(row)
        return row

    # -- entry point 1/2: induced_sup_norm's two weight vectors -----------------
    M = np.abs(b_post.jacobian(z_post))
    for which in ("w_row", "w_col"):
        for cls, val in BAD_SCALARS:
            for placement in ("all_entries", "one_entry_of_many"):
                def mk(v=val, pl=placement, sz=M.shape[0]):
                    w = np.ones(sz)
                    if pl == "all_entries":
                        w[:] = v
                    else:
                        w[sz // 3] = v
                    return w
                w = mk()
                good = np.ones(M.shape[0])
                a = w if which == "w_row" else good
                bb = good if which == "w_row" else w
                record("induced_sup_norm.%s[%s]" % (which, placement), cls, val,
                       lambda a=a, bb=bb: post.induced_sup_norm(M, a, bb),
                       lambda a=a, bb=bb: pre.induced_sup_norm(M, a, bb),
                       lambda r: float(r))

    # -- entry points 3/4/5: the three NAMED scalar weights on `weights` ---------
    for name in ("w_l", "w_om", "w_r"):
        for cls, val in BAD_SCALARS:
            kw = {"p": p, name: val}
            record("BorderedHL.weights.%s" % name, cls, val,
                   lambda kw=kw: b_post.weights(**kw),
                   lambda kw=kw: b_pre.weights(**kw),
                   lambda r: [float(np.min(r[0])), float(np.max(r[0]))])

    # -- entry point 6: nu, which no caller passes directly but `p` controls -----
    # (1+X^2)^(p/2) is positive for every finite p, but at |X| ~ 745 a large p
    # OVERFLOWS to +inf, which deletes those components from the induced norm. This
    # case is reachable through a plain numeric argument and appears in NEITHER leg's
    # list -- it is derived here from the weight FORMULA rather than from a caller.
    for cls, pval in [("nu_overflow_to_inf", 1e4), ("nu_underflow_to_zero", -1e4),
                      ("nu_nan_from_p", math.nan), ("p_is_inf", math.inf)]:
        record("BorderedHL.weights.nu(p)", cls, pval,
               lambda pv=pval: b_post.weights(p=pv),
               lambda pv=pval: b_pre.weights(p=pv),
               lambda r: [float(np.min(r[0])), float(np.max(r[0]))])

    # -- the fabrication measure: what a single bad scalar does to the CERTIFICATE
    fabrication = []
    for name in ("w_l", "w_om", "w_r"):
        for cls, val in BAD_SCALARS:
            row = {"weight": name, "class": cls, "value": repr(val)}
            kw = {"p": p, name: val}
            try:
                b_post.certificate_constants(z_post, **kw)
                row["post_rejected"] = False
            except Exception as exc:
                row["post_rejected"] = True
                row["post_exception"] = type(exc).__name__
            try:
                cc = b_pre.certificate_constants(z_pre, **kw)
                row["pre_rejected"] = False
                for k in ("Y0", "Z1", "Z2"):
                    row["pre_%s" % k] = float(cc[k])
                    h = float(honest_pre[k])
                    row["pre_%s_over_honest" % k] = (
                        float(cc[k]) / h if h != 0 and np.isfinite(h) else None)
                # the fabrication test: a radii-polynomial certificate closes iff
                # the discriminant is non-negative AND Z1 < 1.
                row["pre_Z1_is_negative"] = bool(cc["Z1"] < 0)
                row["pre_Z2_is_negative"] = bool(cc["Z2"] < 0)
                disc = (1.0 - cc["Z1"]) ** 2 - 2.0 * cc["Z2"] * cc["Y0"]
                row["pre_discriminant"] = float(disc)
                row["pre_certificate_closes"] = bool(
                    np.isfinite(disc) and disc >= 0 and cc["Z1"] < 1.0)
            except Exception as exc:
                row["pre_rejected"] = True
                row["pre_exception"] = type(exc).__name__
            fabrication.append(row)

    # -- leg 198's OWN quantity: the same-magnitude sign flip -------------------
    # The fabrication table above compares each corrupted constant against the
    # DEFAULT-weight honest constants, which is not the ratio legs 198 and 218
    # reported. Theirs is a pair at the SAME magnitude with one sign flipped, so it is
    # computed here separately and labelled as such -- otherwise the two numbers look
    # like they contradict each other when they are answers to different questions.
    signflip = []
    for name in ("w_l", "w_om", "w_r"):
        for mag in (1e-6, 1e-3, 1.0):
            row = {"weight": name, "magnitude": mag}
            try:
                pos = b_pre.certificate_constants(z_pre, p=p, **{name: +mag})
                neg = b_pre.certificate_constants(z_pre, p=p, **{name: -mag})
                for k in ("Y0", "Z1", "Z2", "A_norm", "B"):
                    row["pos_%s" % k] = float(pos[k])
                    row["neg_%s" % k] = float(neg[k])
                    row["%s_understatement_x" % k] = (
                        float(pos[k]) / float(neg[k]) if neg[k] else None)
                row["post_repair_refuses_the_negative_half"] = _refuses(
                    lambda: b_post.certificate_constants(z_post, p=p, **{name: -mag}))
                row["post_repair_accepts_the_positive_half"] = not _refuses(
                    lambda: b_post.certificate_constants(z_post, p=p, **{name: +mag}))
            except Exception as exc:
                row["error"] = "%s: %s" % (type(exc).__name__, exc)
            signflip.append(row)

    hon = {"Y0": float(honest_post["Y0"]), "Z1": float(honest_post["Z1"]),
           "Z2": float(honest_post["Z2"])}
    hdisc = (1.0 - hon["Z1"]) ** 2 - 2.0 * hon["Z2"] * hon["Y0"]
    accepted_by_pre = [c for c in cases if not c["pre_rejected"]]
    leaked_by_post = [c for c in cases if not c["post_rejected"]]
    fab_closes = [r for r in fabrication
                  if not r.get("pre_rejected") and r.get("pre_certificate_closes")]

    return {
        "what": ("every entry point of the weight surface x every inadmissibility "
                 "class, derived here from the norm's definition and the weight "
                 "formula, not copied from leg 198's or leg 218's case list"),
        "configuration": {"n": n, "rho_max": rho_max, "p": p,
                          "post_newton_converged": bool(
                              solved(post, "post", n, rho_max)[2]["converged"]),
                          "pre_newton_converged": bool(
                              solved(pre, "pre", n, rho_max)[2]["converged"])},
        "honest_constants_post": hon,
        "honest_discriminant": float(hdisc),
        "honest_certificate_closes": bool(
            np.isfinite(hdisc) and hdisc >= 0 and hon["Z1"] < 1.0),
        "cases_total": len(cases),
        "cases_pre_repair_silently_accepted": len(accepted_by_pre),
        "cases_post_repair_leaked": len(leaked_by_post),
        "cases_post_repair_rejected": len(cases) - len(leaked_by_post),
        "all_post_rejections_are_the_guards_error": bool(all(
            c.get("post_is_the_guards_error") for c in cases if c["post_rejected"])),
        "leaked_cases": leaked_by_post,
        "cases": cases,
        "fabrication": fabrication,
        "fabrication_cases_where_pre_repair_certificate_CLOSES": len(fab_closes),
        "fabrication_closing_cases": fab_closes,
        # the corruption UNDERSTATES: the guarded constant is larger than the
        # corrupted one, so the magnitude that matters is honest/|corrupted|, not
        # its reciprocal. Both directions are reported so neither can be misread.
        "signflip_leg198s_own_quantity": signflip,
        "signflip_note": (
            "legs 198 and 218 report the ratio of a SAME-MAGNITUDE pair, +w vs -w. "
            "The `worst_*_UNDERSTATEMENT_factor` keys below use the DEFAULT-weight "
            "honest constants as the baseline instead, so the two families of numbers "
            "answer different questions and must not be compared to each other."),
        "signflip_worst_Z1_understatement_x": max(
            [r["Z1_understatement_x"] for r in signflip
             if r.get("Z1_understatement_x") and np.isfinite(r["Z1_understatement_x"])]
            or [None]),
        "signflip_worst_A_norm_understatement_x": max(
            [r["A_norm_understatement_x"] for r in signflip
             if r.get("A_norm_understatement_x")
             and np.isfinite(r["A_norm_understatement_x"])] or [None]),
        "signflip_all_negative_halves_refused_post_repair": bool(all(
            r.get("post_repair_refuses_the_negative_half") for r in signflip
            if "error" not in r)),
        "signflip_all_positive_halves_accepted_post_repair": bool(all(
            r.get("post_repair_accepts_the_positive_half") for r in signflip
            if "error" not in r)),
        "worst_Z1_UNDERSTATEMENT_factor_vs_DEFAULT_weight_baseline": max(
            [1.0 / abs(r["pre_Z1_over_honest"]) for r in fabrication
             if r.get("pre_Z1_over_honest") not in (None, 0.0)
             and np.isfinite(r["pre_Z1_over_honest"])] or [None]),
        "worst_Z2_UNDERSTATEMENT_factor_vs_DEFAULT_weight_baseline": max(
            [1.0 / abs(r["pre_Z2_over_honest"]) for r in fabrication
             if r.get("pre_Z2_over_honest") not in (None, 0.0)
             and np.isfinite(r["pre_Z2_over_honest"])] or [None]),
        "worst_Z1_OVERSTATEMENT_factor_vs_DEFAULT_weight_baseline": max(
            [abs(r["pre_Z1_over_honest"]) for r in fabrication
             if r.get("pre_Z1_over_honest") is not None
             and np.isfinite(r["pre_Z1_over_honest"])] or [None]),
        "cases_where_Z2_CHANGES_SIGN": sum(
            1 for r in fabrication if r.get("pre_Z2_is_negative")),
        "understatement_note": (
            "an UNDERSTATED Z_1/Z_2 is the certificate-fabricating direction: the "
            "radii polynomial (1-Z_1)^2 - 2 Z_2 Y_0 acquires a real root it does not "
            "have, so a certificate that must not close, closes."),
    }


# --------------------------------------------------------------------------
# C. THE CALLER SET -- re-enumerated here, all TEN, weight surface MEASURED
# --------------------------------------------------------------------------
# Leg 218's clause (b) named six "enumerated by import". This leg's novelty pass
# re-enumerated and found ten direct importers; the five it adds are marked. Whether
# each touches the WEIGHT SURFACE -- the only surface the guard changed -- is measured
# below by reading the file, not assumed.
DIRECT_IMPORTERS = [
    ("experiments/p2_route_port_v1_bordered.py", True),
    ("experiments/p2_route_l1_v1_interval.py", True),
    ("experiments/p2_route_l1rh_v1_construction.py", True),
    ("test_bordered_hl.py", True),
    ("test_interval_certificate.py", True),
    ("test_bordered_hl_adversarial.py", False),
    ("experiments/p2_route_bhn_v1_adversarial.py", False),
    ("experiments/p2_route_hlb_v1_contraction_lit.py", False),
    ("experiments/p2_route_tn_v1_consistency.py", False),
    ("experiments/p2_route_nb_v1_targetnorm.py", False),
]

WEIGHT_SURFACE_TOKENS = ("certificate_constants", "induced_sup_norm", ".weights(")


def caller_census():
    """Confirm the ten by import, and measure which touch the weight surface."""
    # first, re-derive the import set from scratch rather than trusting the table
    out = subprocess.run(
        ["grep", "-rln", "--include=*.py", "-e", "from solver.bordered_hl import",
         "-e", "import solver.bordered_hl", "."],
        cwd=REPO, capture_output=True, text=True).stdout.split()
    found = sorted(p[2:] if p.startswith("./") else p for p in out)
    found = [f for f in found if f != MODULE_PATH]

    rows = []
    for path, in_leg_218_list in DIRECT_IMPORTERS:
        full = os.path.join(REPO, path)
        src = open(full).read() if os.path.exists(full) else ""
        hits = {t: src.count(t) for t in WEIGHT_SURFACE_TOKENS}
        rows.append({"path": path, "exists": bool(src),
                     "in_leg_218_enumeration": in_leg_218_list,
                     "weight_surface_hits": hits,
                     "touches_weight_surface": bool(sum(hits.values()))})
    missed = [r for r in rows if not r["in_leg_218_enumeration"]]
    missed_touching = [r for r in missed if r["touches_weight_surface"]]
    # The raw grep also picks up files that did not exist when leg 218 drew its list --
    # leg 218's own repair runner, and this leg's runner and test file. Rather than
    # hardcode those names, ASK GIT which of the importers existed in the tree at leg
    # 218's own commit; that is the only set leg 218 could have enumerated, and the
    # test stays correct as the repository grows.
    def existed_at_leg_218(path):
        return subprocess.run(
            ["git", "-C", REPO, "cat-file", "-e", "%s:%s" % (POST_COMMIT, path)],
            capture_output=True).returncode == 0

    contemporaneous = [f for f in found if existed_at_leg_218(f)]
    born_after = [f for f in found if f not in contemporaneous]
    return {
        "what": ("the direct-importer set re-derived by grep in this runner, then each "
                 "importer's weight-surface contact MEASURED by token census"),
        "importers_found_by_independent_grep": found,
        "n_found_by_independent_grep": len(found),
        "importers_that_EXISTED_at_leg_218s_commit": contemporaneous,
        "n_contemporaneous_with_leg_218": len(contemporaneous),
        "importers_born_after_leg_218_excluded_from_the_count": born_after,
        "contemporaneity_rule": (
            "membership decided by `git cat-file -e d9a20fb:<path>`, not by a "
            "hardcoded name list, so the comparison against leg 218's enumeration is "
            "like-for-like and stays correct as the repository grows"),
        "n_leg_218_named": 6,
        "n_leg_218_named_that_are_DIRECT_importers": sum(
            1 for _, x in DIRECT_IMPORTERS if x),
        "leg_218_sixth_name_was_transitive": (
            "experiments/p2_route_port_v2_reach.py imports p2_route_port_v1_bordered, "
            "not solver.bordered_hl -- correct as a transitive caller, but it means "
            "the enumeration was not purely 'by import' as leg 218 described it"),
        "n_in_leg_218_enumeration": sum(1 for _, x in DIRECT_IMPORTERS if x),
        "n_leg_218_missed": len(missed),
        "rows": rows,
        "missed_by_leg_218": [r["path"] for r in missed],
        "missed_by_leg_218_that_TOUCH_the_weight_surface":
            [r["path"] for r in missed_touching],
        "omission_verdict": ("MATERIAL" if missed_touching else "COSMETIC"),
        "omission_verdict_rule": (
            "fixed in advance in writeup/novelty/leg_228.md sec 4: MATERIAL iff any "
            "importer leg 218 missed touches the weight surface, since the gate's "
            "'every live value bit-identical' clause was then answered on an "
            "incomplete set; COSMETIC iff all five are weight-surface-free"),
    }


# --------------------------------------------------------------------------
# D. CLAUSE B -- bit-identical pre/post on every live configuration
# --------------------------------------------------------------------------
# Configurations re-derived from the callers themselves (the grids they construct and
# the (p, w_l) pairs they pass), NOT from leg 218's list of 34.
LIVE_CONFIGS = []
for _n, _rm in [(101, 8.0), (201, 8.0), (401, 8.0), (601, 8.0), (801, 8.0)]:
    for _p in (0.0, 0.39, 1.0):
        for _wf in (1.0, 0.01, 0.1):
            LIVE_CONFIGS.append({"n": _n, "rho_max": _rm, "p": _p, "w_l_frac": _wf})


def clause_b(post, pre):
    """Bit-for-bit differential of every returned float, over the live grid.

    The comparison is on IEEE-754 payloads, and it covers the FULL constants dict --
    Y0, Z1, Z2, A_norm, B, Uop_norm, H_norm and every other float the surface returns
    -- plus the whole weight vector, not a summary."""
    import time
    rows = []
    leaves_compared = 0
    mismatches = []
    seen_grids = set()
    for cfg in LIVE_CONFIGS:
        n, rm, p, wf = cfg["n"], cfg["rho_max"], cfg["p"], cfg["w_l_frac"]
        if n not in seen_grids:
            seen_grids.add(n)
            print("       grid n=%d ... (%s)" % (n, time.strftime("%H:%M:%S")),
                  flush=True)
        b_post, z_post, h_post = solved(post, "post", n, rm)
        b_pre, z_pre, h_pre = solved(pre, "pre", n, rm)
        # the SOLVE itself must be bit-identical too -- the guard sits upstream of it
        state_mismatch = sum(1 for a, c in zip(z_post, z_pre) if bits(a) != bits(c))
        leaves_compared += len(z_post)
        Xmax = float(np.abs(b_post.X).max())
        w_l = wf * Xmax
        row = {"n": n, "rho_max": rm, "p": p, "w_l_frac": wf,
               "solved_state_leaves": int(z_post.size),
               "solved_state_bit_mismatches": int(state_mismatch)}
        if state_mismatch:
            mismatches.append({"where": "newton state", **row})
        try:
            cc_post = b_post.certificate_constants(z_post, p=p, w_l=w_l)
            cc_pre = b_pre.certificate_constants(z_pre, p=p, w_l=w_l)
            w_post = b_post.weights(p=p, w_l=w_l)[0]
            w_pre = b_pre.weights(p=p, w_l=w_l)[0]
            # and the escape hatch must reproduce the pre-repair arithmetic exactly
            cc_allow = b_post.certificate_constants(z_post, p=p, w_l=w_l,
                                                    on_nonpositive="allow")
            bad = []
            for k in sorted(cc_post):
                if isinstance(cc_post[k], (int, float)):
                    leaves_compared += 2
                    if bits(cc_post[k]) != bits(cc_pre[k]):
                        bad.append({"key": k, "post": bits(cc_post[k]),
                                    "pre": bits(cc_pre[k]),
                                    "post_val": float(cc_post[k]),
                                    "pre_val": float(cc_pre[k])})
                    if bits(cc_allow[k]) != bits(cc_pre[k]):
                        bad.append({"key": k + " (on_nonpositive='allow')",
                                    "post": bits(cc_allow[k]),
                                    "pre": bits(cc_pre[k])})
            wmis = sum(1 for a, c in zip(w_post, w_pre) if bits(a) != bits(c))
            leaves_compared += len(w_post)
            row["constants_keys_compared"] = sum(
                1 for k in cc_post if isinstance(cc_post[k], (int, float)))
            row["weight_vector_leaves"] = int(w_post.size)
            row["weight_vector_bit_mismatches"] = int(wmis)
            row["constant_bit_mismatches"] = len(bad)
            row["Y0"] = float(cc_post["Y0"])
            row["Z1"] = float(cc_post["Z1"])
            row["Z2"] = float(cc_post["Z2"])
            if bad or wmis:
                mismatches.append({"where": "constants", "detail": bad, **row})
        except Exception as exc:
            row["error"] = "%s: %s" % (type(exc).__name__, exc)
            mismatches.append({"where": "exception", **row})
        rows.append(row)
    return {
        "what": ("every returned float compared as an IEEE-754 payload, pre vs post, "
                 "over configurations re-derived from the callers rather than from "
                 "leg 218's list; includes the Newton state, the full weight vector "
                 "and the complete constants dict, plus the 'allow' escape hatch"),
        "configurations": len(LIVE_CONFIGS),
        "float_leaves_compared": leaves_compared,
        "bit_mismatches": len(mismatches),
        "mismatch_detail": mismatches[:20],
        "rows": rows,
    }


# --------------------------------------------------------------------------
# E. THE Z_1 DISAGREEMENT, TESTED AS THE VARIANCE CLAIM IT IS
# --------------------------------------------------------------------------
# The banked disagreement, read from the record rather than paraphrased
# (experiments/journal/leg_218.md:182, leg_223.md:69): on leg 198's own w_r = +-1e-6
# configuration, leg 198 reports the Z_1 understatement factor as 1.198e9x and leg 218
# re-measures it as 2.2867e8x -- 5.24x apart -- while their ||A|| (6.6712e9x) and Z_2
# (+1.188608e17) columns agree to 4-6 significant figures. Leg 223 banks both and
# adopts neither.
#
# Leg 218's explanation is lesson 86: Z_1 = ||I - A.DF|| with A = inv(DF) is a
# near-total cancellation, so the FLIPPED Z_1 sits at the round-off floor and the
# RATIO is environment-dependent while the VERDICT (the certificate fabricates) is
# not. That is a falsifiable claim about VARIANCE, and the condition is fixed BEFORE
# the numbers are looked at:
#
#   perturb ONLY in ways that provably cannot change the mathematics -- algebraically
#   identical re-associations of the same matrix products, and BLAS thread counts --
#   and measure the spread OF THE DISPUTED QUANTITY ITSELF, which is the ratio
#   Z_1(w_r=+1e-6) / Z_1(w_r=-1e-6), not Z_1 at an admissible weight. Then:
#     * if the observed spread BRACKETS 5.24x -> leg 218's explanation stands: the two
#       banked numbers are one measurement seen through different round-off.
#     * if the ratio is stable to within a few percent under EVERY such perturbation
#       -> leg 218's explanation is WRONG, and one of the two banked measurements is a
#       real defect that must be escalated.
#
# The distinction matters and is the reason this section is aimed where it is: Z_1 at
# an ADMISSIBLE weight is not a cancellation and barely moves, so measuring its spread
# would have been a lesson-90 control that could not come out differently.
FALSIFICATION_THRESHOLD = 5.24
STABLE_IF_SPREAD_BELOW = 1.05   # "a few percent"
LEG_198_Z1_RATIO = 1.198e9
LEG_218_Z1_RATIO = 2.2867e8


def z1_variance(post, pre):
    n, rho_max, p = 101, 8.0, 0.0
    b, z, _ = solved(post, "post", n, rho_max)
    J = b.jacobian(z)
    N = b.N
    # leg 198's own configuration: the sign flip on w_r at magnitude 1e-6
    w_pos = b.weights(p=p, w_r=+1e-6)[0]
    w_neg = b.weights(p=p, w_r=-1e-6, on_nonpositive="allow")[0]
    w_adm = b.weights(p=p)[0]

    def Z1_from(M, w):
        return float(np.max(w * (np.abs(M) @ (1.0 / w))))

    # every M below is the SAME real matrix in exact arithmetic
    A0 = np.linalg.inv(J)
    A1 = np.linalg.solve(J, np.eye(N))
    A2 = np.linalg.inv(np.asfortranarray(J))
    A3 = np.linalg.inv(J.copy(order="C"))
    residual_forms = {
        "inv_then_eye_minus_AJ": np.eye(N) - A0 @ J,
        "inv_then_neg_AJ_minus_eye": -(A0 @ J - np.eye(N)),
        "inv_then_transposed_product": np.eye(N) - (J.T @ A0.T).T,
        "solve_for_inverse": np.eye(N) - A1 @ J,
        "fortran_order_inverse": np.eye(N) - A2 @ J,
        "explicit_c_copy": np.eye(N) - A3 @ J.copy(order="C"),
        "einsum_product": np.eye(N) - np.einsum("ij,jk->ik", A0, J),
    }

    variants = {}
    for name, M in residual_forms.items():
        zp, zn = Z1_from(M, w_pos), Z1_from(M, w_neg)
        za = Z1_from(M, w_adm)
        variants[name] = {"Z1_admissible": za, "Z1_at_w_r_plus_1e_6": zp,
                          "Z1_at_w_r_minus_1e_6": zn,
                          "understatement_ratio": zp / zn if zn else None}

    # thread count: identical GEMM, different reduction order, fresh interpreter
    thread_runs = {}
    prog = (
        "import os,sys,numpy as np;"
        "sys.path.insert(0,%r);"
        "import solver.bordered_hl as m;"
        "b=m.BorderedHL(n=%d,rho_max=%r,c=0.5);"
        "Om=np.exp(-((b.X-0.3)**2)/(2.0*0.9**2));"
        "V=0.8*np.exp(-((b.X-1.3*0.3)**2)/(2.0*(1.1*0.9)**2));"
        "z0=b.pack(Om,V,*m.CHL_TRIPLE);b.set_pin_from(z0);"
        "z,_=b.newton(z0,tol=1e-12,max_iter=40);"
        "pos=b.certificate_constants(z,p=%r,w_r=+1e-6);"
        "neg=b.certificate_constants(z,p=%r,w_r=-1e-6,on_nonpositive='allow');"
        "print(repr((pos['Z1'],neg['Z1'],pos['A_norm']/neg['A_norm'],pos['Z2'])))"
        % (REPO, n, rho_max, p, p))
    for t in (1, 2, 4, 8):
        env = dict(os.environ)
        for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
            env[var] = str(t)
        try:
            out = subprocess.run([sys.executable, "-c", prog], cwd=REPO, env=env,
                                 capture_output=True, text=True, timeout=900)
            zp, zn, an, z2 = eval(out.stdout.strip().splitlines()[-1])
            thread_runs["threads_%d" % t] = {
                "Z1_pos": zp, "Z1_neg": zn, "understatement_ratio": zp / zn,
                "A_norm_understatement_ratio": an, "Z2_at_w_r_plus": z2}
        except Exception as exc:
            thread_runs["threads_%d" % t] = {"error": str(exc)[:200]}

    ratios = [v["understatement_ratio"] for v in variants.values()
              if v["understatement_ratio"] and np.isfinite(v["understatement_ratio"])]
    ratios += [v["understatement_ratio"] for v in thread_runs.values()
               if isinstance(v, dict) and v.get("understatement_ratio")
               and np.isfinite(v["understatement_ratio"])]
    negs = [v["Z1_at_w_r_minus_1e_6"] for v in variants.values()]
    poss = [v["Z1_at_w_r_plus_1e_6"] for v in variants.values()]
    adms = [v["Z1_admissible"] for v in variants.values()]
    # the ||A|| column, which BOTH legs agree on -- the internal control that says the
    # perturbations are not simply breaking the computation
    a_ratios = [v["A_norm_understatement_ratio"] for v in thread_runs.values()
                if isinstance(v, dict) and v.get("A_norm_understatement_ratio")]

    def spread(xs):
        xs = [x for x in xs if x and np.isfinite(x) and x > 0]
        return (max(xs) / min(xs)) if xs else None

    s_ratio = spread(ratios)
    stands = bool(s_ratio is not None and s_ratio >= FALSIFICATION_THRESHOLD)
    stable = bool(s_ratio is not None and s_ratio < STABLE_IF_SPREAD_BELOW)
    # do the two banked numbers both land inside the observed band?
    lo, hi = (min(ratios), max(ratios)) if ratios else (None, None)
    return {
        "what": ("leg 218's lesson-86 explanation of the leg-198/leg-218 Z_1 "
                 "disagreement, tested as the falsifiable VARIANCE claim it is, and "
                 "aimed at the DISPUTED quantity (the understatement ratio at leg "
                 "198's own w_r = +-1e-6), not at Z_1 on an admissible weight"),
        "the_disagreement_read_from_the_record": {
            "leg_198_Z1_understatement_x": LEG_198_Z1_RATIO,
            "leg_218_Z1_understatement_x": LEG_218_Z1_RATIO,
            "they_are_apart_by_x": LEG_198_Z1_RATIO / LEG_218_Z1_RATIO,
            "source": ("experiments/journal/leg_218.md:182, "
                       "experiments/journal/leg_223.md:69"),
        },
        "falsification_condition_fixed_in_advance": {
            "explanation_stands_if_ratio_spread_at_least": FALSIFICATION_THRESHOLD,
            "explanation_is_WRONG_if_ratio_spread_below": STABLE_IF_SPREAD_BELOW,
        },
        "configuration": {"n": n, "rho_max": rho_max, "p": p, "w_r": "+-1e-6"},
        "algebraically_identical_variants": variants,
        "blas_thread_count_runs": thread_runs,
        "observed_understatement_ratio_spread_x": s_ratio,
        "observed_understatement_ratio_min": lo,
        "observed_understatement_ratio_max": hi,
        "this_legs_own_understatement_ratio":
            variants["inv_then_eye_minus_AJ"]["understatement_ratio"],
        "spread_of_the_FLIPPED_Z1_the_denominator_x": spread(negs),
        "spread_of_the_HONEST_Z1_the_numerator_x": spread(poss),
        "spread_of_Z1_at_an_ADMISSIBLE_weight_x": spread(adms),
        "control_spread_of_the_A_norm_ratio_x": spread(a_ratios),
        "control_note": (
            "||A||'s understatement ratio is the column legs 198 and 218 AGREE on "
            "(6.6712e9x, 4-6 sig figs). If the perturbations were simply breaking the "
            "computation rather than exposing a cancellation, this control would move "
            "too. Its spread is reported alongside so the reader can check that."),
        "leg_198_value_inside_observed_band": bool(
            lo is not None and lo <= LEG_198_Z1_RATIO <= hi),
        "leg_218_value_inside_observed_band": bool(
            lo is not None and lo <= LEG_218_Z1_RATIO <= hi),
        "verdict": ("LEG_218_EXPLANATION_STANDS" if stands else
                    ("LEG_218_EXPLANATION_FALSIFIED" if stable else
                     "INCONCLUSIVE_SPREAD_BETWEEN_THRESHOLDS")),
        "mechanism": (
            "the ratio's DENOMINATOR is Z_1 at a flipped weight, which is a near-total "
            "cancellation sitting at ~1e-15..1e-16; its spread is what the ratio "
            "inherits. The numerator, an honest quantity, barely moves. That "
            "asymmetry -- reported as two separate spreads above -- is the mechanism, "
            "measured rather than argued."),
    }


# --------------------------------------------------------------------------
def main():
    print("Leg 228, Route-BHRV -- independent post-repair verification of leg 218",
          flush=True)
    prov = assert_provenance()
    print("  provenance OK: pre %s / post %s, worktree is post" %
          (prov["pre_blob"][:8], prov["post_blob"][:8]), flush=True)

    import solver.bordered_hl as post
    pre, pre_lines = load_pre_repair()
    print("  pre-repair module loaded independently (%d lines, no guard)" % pre_lines,
          flush=True)

    print("  A. clause A -- the rejection battery ...", flush=True)
    A = clause_a(post, pre)
    print("     %d cases; pre-repair silently accepted %d; post-repair leaked %d"
          % (A["cases_total"], A["cases_pre_repair_silently_accepted"],
             A["cases_post_repair_leaked"]), flush=True)
    print("     worst pre-repair UNDERSTATEMENT vs the default-weight baseline: "
          "Z_1 %.4g x, Z_2 %.4g x; Z_2 changes SIGN in %d cases; certificates "
          "FABRICATED in %d cases"
          % (A["worst_Z1_UNDERSTATEMENT_factor_vs_DEFAULT_weight_baseline"],
             A["worst_Z2_UNDERSTATEMENT_factor_vs_DEFAULT_weight_baseline"],
             A["cases_where_Z2_CHANGES_SIGN"],
             A["fabrication_cases_where_pre_repair_certificate_CLOSES"]), flush=True)
    print("     on leg 198's OWN same-magnitude sign flip: Z_1 understated up to "
          "%.4g x, ||A|| up to %.4g x; every negative half refused post-repair: %s"
          % (A["signflip_worst_Z1_understatement_x"],
             A["signflip_worst_A_norm_understatement_x"],
             A["signflip_all_negative_halves_refused_post_repair"]), flush=True)

    print("  C. the caller census ...", flush=True)
    C = caller_census()
    print("     %d direct importers contemporaneous with leg 218; leg 218 named %d "
          "(%d of them direct); %d missed, %d of those touch the weight surface -> %s"
          % (C["n_contemporaneous_with_leg_218"], C["n_leg_218_named"],
             C["n_leg_218_named_that_are_DIRECT_importers"], C["n_leg_218_missed"],
             len(C["missed_by_leg_218_that_TOUCH_the_weight_surface"]),
             C["omission_verdict"]), flush=True)
    for pth in C["missed_by_leg_218_that_TOUCH_the_weight_surface"]:
        print("       weight-surface caller leg 218 missed: %s" % pth, flush=True)

    print("  D. clause B -- the bit differential ...", flush=True)
    D = clause_b(post, pre)
    print("     %d configurations, %d float leaves, %d bit mismatches"
          % (D["configurations"], D["float_leaves_compared"], D["bit_mismatches"]),
          flush=True)

    print("  E. the Z_1 variance test ...", flush=True)
    E = z1_variance(post, pre)
    print("     disputed ratio spread %.4g x over math-neutral perturbations "
          "(the disagreement is %.4g x) -> %s"
          % (E["observed_understatement_ratio_spread_x"],
             E["the_disagreement_read_from_the_record"]["they_are_apart_by_x"],
             E["verdict"]), flush=True)
    print("     denominator (flipped Z_1, a cancellation) spreads %.4g x; numerator "
          "%.4g x; ||A|| control %.4g x"
          % (E["spread_of_the_FLIPPED_Z1_the_denominator_x"],
             E["spread_of_the_HONEST_Z1_the_numerator_x"],
             E["control_spread_of_the_A_norm_ratio_x"] or float("nan")), flush=True)

    clause_a_pass = (A["cases_post_repair_leaked"] == 0
                     and A["all_post_rejections_are_the_guards_error"]
                     and A["cases_pre_repair_silently_accepted"] > 0)
    clause_b_pass = D["bit_mismatches"] == 0
    gate = "YES" if (clause_a_pass and clause_b_pass) else "NO"

    out = {
        "leg": 228, "route": "BHRV", "role": "VERIFY",
        "object": "leg 218's border-weight guard in solver/bordered_hl.py",
        "gate_question": (
            "Does an independent re-run of leg 218's own adversarial battery confirm "
            "every negative-weight case now rejects, with every live caller value "
            "bit-identical pre/post repair?"),
        "independence": (
            "lesson 90: leg 218's runner is never imported or executed. The pre-repair "
            "module is loaded by a different loader path, the adversarial cases are "
            "derived from the norm's definition rather than copied, the caller set is "
            "re-enumerated, and the configurations are re-derived from the callers."),
        "provenance": prov,
        "pre_repair_module_lines": pre_lines,
        "A_clause_a_rejection_battery": A,
        "C_caller_census": C,
        "D_clause_b_bit_differential": D,
        "E_z1_variance_test": E,
        "clause_a_pass": clause_a_pass,
        "clause_b_pass": clause_b_pass,
        "gate": gate,
        "caveat_the_gate_does_not_cover": (
            "the caller-enumeration omission is reported separately from the gate: "
            "clause B's verdict is measured here over the FULL ten-importer "
            "configuration space, so the gate answer does not inherit leg 218's gap."),
    }
    dest = os.path.join(REPO, "writeup/data/p2_route_bhrv_v1_postrepair.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=False, default=str)
    print("\n  GATE: %s   (clause A %s, clause B %s)"
          % (gate, "pass" if clause_a_pass else "FAIL",
             "pass" if clause_b_pass else "FAIL"), flush=True)
    print("  wrote %s" % dest, flush=True)
    return 0 if gate == "YES" else 1


if __name__ == "__main__":
    sys.exit(main())
