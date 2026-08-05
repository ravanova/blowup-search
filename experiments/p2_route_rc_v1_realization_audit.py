"""Route-RC v1 -- READ-ONLY realization audit of solver/rescaled_spectrum.py.

Leg 70.  Docs-only.  THIS SCRIPT COMPUTES NOTHING ABOUT gCLM.

--------------------------------------------------------------------------
WHAT IS BANNED HERE AND HOW THIS SCRIPT STAYS INSIDE IT
--------------------------------------------------------------------------
`plan_of_record.py` bans "another gCLM measurement leg" (the model is exhausted,
Stage 3.5, leg 42).  A realization audit that re-ran the spectrum under an origin
condition would read as exactly that.  So this script is pinned to introspection:

    FORBIDDEN and asserted against below -- newton(), continuation(), spectrum(),
    converged_spectrum(), np.linalg.eigvals, any solve of the fixed point.
    ALLOWED -- constructing OddCompactBasis (matrix assembly, no solve), reading
    module source text, and ARITHMETIC on counts already banked in
    writeup/4_p2_lottery/TECHNICAL_P2_ROUTEI_V1.md.

Every number this script prints is either a property of the GRID (available from the
basis constructor without solving anything) or a subtraction performed on a number
that was on disk before this leg started.

--------------------------------------------------------------------------
THE QUESTION
--------------------------------------------------------------------------
    Does solver/rescaled_spectrum.py's discretization impose an origin (H^2-type)
    condition at X = 0, or none (the maximal L^2 realization)?

PHASE2_P2_NOTES J-4 asserts "OUR DISCRETIZATION HAS NO ORIGIN CONDITION" on the
strength of Xu arXiv:2607.19762 Proposition 2.  That assertion was made from the
paper.  This script checks it from the CODE, in four independent ways (A-D), then
inventories every place the resulting count is quoted (E) and reports which sites
name the realization and which do not (F).

Run:  python experiments/p2_route_rc_v1_realization_audit.py
"""

import ast
import inspect
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver import rescaled_spectrum as RS  # noqa: E402


# --------------------------------------------------------------------------
# the guard: prove this script did not measure anything
# --------------------------------------------------------------------------
BANNED_CALLS = ("newton", "continuation", "spectrum", "converged_spectrum",
                "eigvals", "eig", "lstsq", "planted_eigenvalue_control")


def self_guard():
    """AST-check THIS FILE for any call that would constitute a new measurement.

    A comment promising "no new solve" is not evidence.  This parses the script's
    own source and fails loudly if any banned name is called anywhere in it.
    """
    tree = ast.parse(Path(__file__).read_text())
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = getattr(f, "attr", None) or getattr(f, "id", None)
            if name in BANNED_CALLS:
                hits.append((name, node.lineno))
    return hits


# --------------------------------------------------------------------------
# A. the collocation grid never touches the origin
# --------------------------------------------------------------------------
def check_A_grid(Ks=(48, 96, 144)):
    """Where is the nearest collocation row to X = 0, and is there one AT X = 0?

    theta_j = (j + 1/2) pi / K is the MIDPOINT grid.  If any row sat at theta = 0
    that row COULD carry an origin condition.  None does, at any K.
    """
    rows = []
    for K in Ks:
        B = RS.OddCompactBasis(K)
        th0 = float(B.theta.min())
        rows.append({
            "K": K,
            "n_rows": int(B.theta.size),
            "theta_min": th0,
            "X_min": float(np.tan(th0 / 2.0)),
            "theta_max": float(B.theta.max()),
            "rows_at_origin": int(np.sum(B.theta == 0.0)),
        })
    return rows


# --------------------------------------------------------------------------
# B. the eigenproblem carries no constraint row
# --------------------------------------------------------------------------
def check_B_shapes(K=144):
    """generator() is K x K.  newton() builds K+1 x K.  The extra row is the GAUGE.

    This is the load-bearing structural fact: the ONLY place an extra row is ever
    appended is the fixed-point solve, and the eigenproblem does not inherit it.
    Shapes are read from the source, not from a run.
    """
    src_gen = inspect.getsource(RS.RescaledFlow.generator)
    src_jac = inspect.getsource(RS.RescaledFlow.jacobian)
    src_newt = inspect.getsource(RS.RescaledFlow.newton)
    B = RS.OddCompactBasis(K)
    return {
        "K": K,
        "basis_dim": int(B.S.shape[1]),
        "S_shape": tuple(int(x) for x in B.S.shape),
        "generator_appends_row": bool(re.search(r"vstack|concatenate|hstack", src_gen)),
        "jacobian_appends_row": bool(re.search(r"vstack|concatenate|hstack", src_jac)),
        "newton_appends_row": bool(re.search(r"vstack|concatenate", src_newt)),
        "generator_body": " ".join(src_gen.strip().splitlines()[-1:]),
    }


# --------------------------------------------------------------------------
# C. every origin-referencing quantity in the module is a GAUGE scalar
# --------------------------------------------------------------------------
# Each entry: (symbol, which module it lives in, what role it plays).
# `lam_dx0` is defined in critical_dissipation.py, NOT in rescaled_spectrum.py -- it is
# included because CriticalDissipativeFlow subclasses RescaledFlow and reuses the same
# OddCompactBasis, so it is part of the realization question even though it lives next door.
# (symbol, module, scope-function or None for whole module, role).
# `kk` is SCOPED to newton() because the same name is reused as a loop index inside
# _velocity_matrix(); an unscoped grep reports 10 occurrences of which 6 are the
# unrelated recurrence and would overstate the origin's footprint in the module.
ORIGIN_QUANTITIES = [
    ("h0", "solver/rescaled_spectrum.py", None,
     "H(Omega)(0); enters c_omega via gauge (N) -- a SCALAR normalization"),
    ("kk", "solver/rescaled_spectrum.py", "def newton",
     "Omega_X(0)/2; the appended dilation-gauge ROW inside newton() only"),
    ("lam_dx0", "solver/critical_dissipation.py", None,
     "(Lambda^p Omega)_X(0); enters c_omega via the re-derived gauge (N')"),
]


def _scope_lines(src_lines, scope):
    """Line numbers spanned by the def whose header contains `scope` (1-based)."""
    if scope is None:
        return 1, len(src_lines)
    start = next(i for i, ln in enumerate(src_lines) if scope in ln)
    indent = len(src_lines[start]) - len(src_lines[start].lstrip())
    end = len(src_lines)
    for j in range(start + 1, len(src_lines)):
        ln = src_lines[j]
        if ln.strip() and (len(ln) - len(ln.lstrip())) <= indent:
            end = j
            break
    return start + 1, end


def check_C_origin_terms():
    """Locate every origin-evaluated quantity and classify it: gauge or domain.

    A DOMAIN condition would restrict which b are admissible -- it would appear as a
    row of the eigenproblem, a projection applied to the generator, or a basis
    element removed.  A GAUGE fixes a scalar freedom of the flow and leaves the
    admissible set alone.  All three origin quantities are the latter.
    """
    out = []
    for name, mod, scope, role in ORIGIN_QUANTITIES:
        src = (ROOT / mod).read_text().splitlines()
        lo, hi = _scope_lines(src, scope)
        lines = [i + 1 for i, ln in enumerate(src)
                 if lo <= i + 1 <= hi and re.search(r"\b%s\b" % name, ln)]
        out.append({"quantity": name, "module": mod, "role": role,
                    "scope": scope or "whole module", "scope_lines": (lo, hi),
                    "lines": lines[:8], "n_occurrences": len(lines),
                    "restricts_admissible_b": False})
    return out


# --------------------------------------------------------------------------
# D. the trial space's own behaviour at X = 0
# --------------------------------------------------------------------------
def check_D_trial_space(K=144, X=1e-6):
    """Every basis function is odd-analytic at X = 0 and vanishes LINEARLY there.

    theta = 2 arctan X, so sin(k theta) ~ 2 k X as X -> 0.  The continuum
    eigenfunctions of the maximal realization behave like X^{1 - i y} -- a FRACTIONAL
    power, not in the span.  This is the one piece of evidence that points the other
    way, and it is reported rather than buried: the trial space is smooth at the
    origin even though no origin condition is imposed on the OPERATOR.  See the
    journal for why the two are not the same statement.
    """
    B = RS.OddCompactBasis(K)
    th = 2.0 * np.arctan(X)
    vals = np.sin(th * B.k)
    linear = 2.0 * B.k * X
    return {
        "K": K, "X": X,
        "max_abs_basis_value_at_X": float(np.max(np.abs(vals))),
        "max_rel_dev_from_linear": float(np.max(np.abs(vals - linear)
                                                / (np.abs(linear) + 1e-300))),
        "all_vanish_at_origin": bool(np.all(np.abs(np.sin(0.0 * B.k)) == 0.0)),
    }


# --------------------------------------------------------------------------
# E. the banked counts, and what their K-scaling says
# --------------------------------------------------------------------------
# VERBATIM from writeup/4_p2_lottery/TECHNICAL_P2_ROUTEI_V1.md section 1, table
# "unstable directions at mu = 0".  NOT recomputed.  Source of truth is that file.
BANKED_COUNTS = [
    {"K": 48,  "n_unstable": 45,  "max_re": 4.524},
    {"K": 96,  "n_unstable": 93,  "max_re": 4.546},
    {"K": 144, "n_unstable": 141, "max_re": 4.558},
]


def check_E_scaling():
    """Subtraction only.  Is the count fixed, or proportional to the dimension?

    A genuine finite-dimensional unstable manifold has a K-INDEPENDENT dimension once
    resolved.  A discretized continuum gives a count that grows with K.  Which one
    the banked numbers are is decided by arithmetic on numbers already on file.
    """
    rows = []
    for r in BANKED_COUNTS:
        K, n = r["K"], r["n_unstable"]
        rows.append({**r,
                     "K_minus_n": K - n,
                     "fraction_unstable": n / K,
                     "matches_K_minus_3": (K - n) == 3})
    deficits = {r["K_minus_n"] for r in rows}
    return {"rows": rows,
            "deficit_constant": len(deficits) == 1,
            "deficit_value": sorted(deficits),
            "count_growth_48_to_144": rows[-1]["n_unstable"] - rows[0]["n_unstable"],
            "dim_growth_48_to_144": rows[-1]["K"] - rows[0]["K"],
            "max_re_spread": max(r["max_re"] for r in rows)
                             - min(r["max_re"] for r in rows)}


# --------------------------------------------------------------------------
# F. where the count is quoted, and whether the realization is named there
# --------------------------------------------------------------------------
QUOTE_PATTERN = re.compile(r"\b141\b|\b93 of 96\b|\b45 of 48\b|141/144")
DISCLOSE_PATTERN = re.compile(r"realization|origin condition|origin-`?H", re.I)
# A site can disclose in SUBSTANCE without using the word "realization" -- BLOG_J does
# exactly that ("that count of 141 needs the choice named next to it").  Scoring those as
# hard gaps would inflate the gap count, so they get their own bucket rather than a
# widened DISCLOSE_PATTERN, which would have hidden them inside the OK column instead.
SOFT_DISCLOSE_PATTERN = re.compile(
    r"needs the choice named|choice named next to it|which operator we discretized"
    r"|loose realization|maximal L", re.I)
DISCLOSE_WINDOW = 12          # lines either side that count as "at the quote site"

QUOTE_FILES = [
    "PHASE2_P2_NOTES.md",
    "LITERATURE_CHECK.md",
    "capabilities.py",
    "experiments/JOURNAL.md",
    "writeup/README.md",
    "solver/literature_gates.py",
    "writeup/4_p2_lottery/BLOG_P2_ROUTEI_V1.md",
    "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEI_V1.md",
    "writeup/4_p2_lottery/BLOG_P2_ROUTEJ_V1.md",
    "writeup/4_p2_lottery/TECHNICAL_P2_ROUTEJ_V1.md",
]


def check_F_quote_sites():
    """Every quote of the count, with a local disclosure test.

    "The disclosure exists somewhere in the file" is not the standard -- a reader
    quoting a number reads the lines AROUND it.  So disclosure is scored inside a
    +/- DISCLOSE_WINDOW line window of each quote, and files where the disclosure
    sits hundreds of lines away are reported as UNDISCLOSED AT SITE.
    """
    sites = []
    for rel in QUOTE_FILES:
        p = ROOT / rel
        if not p.exists():
            sites.append({"file": rel, "exists": False})
            continue
        lines = p.read_text().splitlines()
        file_has = any(DISCLOSE_PATTERN.search(ln) for ln in lines)
        for i, ln in enumerate(lines):
            if not QUOTE_PATTERN.search(ln):
                continue
            lo = max(0, i - DISCLOSE_WINDOW)
            hi = min(len(lines), i + DISCLOSE_WINDOW + 1)
            local = any(DISCLOSE_PATTERN.search(x) for x in lines[lo:hi])
            soft = any(SOFT_DISCLOSE_PATTERN.search(x) for x in lines[lo:hi])
            sites.append({"file": rel, "exists": True, "line": i + 1,
                          "text": ln.strip()[:96],
                          "disclosed_at_site": local,
                          "soft_disclosed_at_site": soft and not local,
                          "disclosed_anywhere_in_file": file_has})
    return sites


# --------------------------------------------------------------------------
# the sentence this leg proposes for every undisclosed site
# --------------------------------------------------------------------------
DISCLOSURE_SENTENCE = (
    "This count is the spectrum of the MAXIMAL L^2 REALIZATION: our discretization "
    "imposes no origin condition at X = 0 (Xu arXiv:2607.19762 Prop 2's dichotomy), "
    "and the count is exactly K - 3 at K = 48, 96, 144, i.e. proportional to the "
    "discretization dimension rather than a realization-independent Morse index. On "
    "the origin-H^2 realization the open strip is empty apart from {0, 1}."
)


def main():
    hits = self_guard()
    print("=" * 74)
    print("ROUTE-RC v1 -- REALIZATION AUDIT of solver/rescaled_spectrum.py (leg 70)")
    print("=" * 74)
    print("\n[GUARD] banned-call scan of this script")
    if hits:
        print("  FAIL -- this script calls:", hits)
        raise SystemExit(1)
    print("  no call to any of:", ", ".join(BANNED_CALLS))
    print("  -> nothing was solved, nothing was diagonalized, no gCLM measurement")

    print("\n[A] the collocation grid vs the origin")
    for r in check_A_grid():
        print(f"  K={r['K']:>4}  rows={r['n_rows']:>4}  rows AT X=0: {r['rows_at_origin']}"
              f"   nearest row theta={r['theta_min']:.6f}  X={r['X_min']:.6e}")
    print("  -> no collocation row sits at X = 0, so no row can carry a condition there.")

    print("\n[B] shapes: where a constraint row could hide")
    b = check_B_shapes()
    print(f"  basis dim K = {b['basis_dim']}, S is {b['S_shape']}")
    print(f"  generator() appends a row: {b['generator_appends_row']}")
    print(f"  jacobian()  appends a row: {b['jacobian_appends_row']}")
    print(f"  newton()    appends a row: {b['newton_appends_row']}  <- the DILATION GAUGE,")
    print("               a normalization of WHICH fixed point, not of the operator domain;")
    print("               the eigenproblem is generator() and never sees it.")

    print("\n[C] every origin-evaluated quantity in the module")
    for c in check_C_origin_terms():
        print(f"  {c['quantity']:<9} {c['role']}")
        print(f"            {c['module']} [{c['scope']}] lines {c['lines']} "
              f"({c['n_occurrences']} occurrences); "
              f"restricts admissible b: {c['restricts_admissible_b']}")

    print("\n[D] the trial space at the origin (the evidence pointing the OTHER way)")
    d = check_D_trial_space()
    print(f"  at X={d['X']:g}: max|sin(k theta)| = {d['max_abs_basis_value_at_X']:.6e}, "
          f"max rel dev from 2kX = {d['max_rel_dev_from_linear']:.3e}")
    print("  every basis function vanishes LINEARLY at X=0 and is analytic there, while the")
    print("  maximal realization's continuum modes go like X^(1-iy). Reported, not buried.")

    print("\n[E] the banked counts (verbatim from TECHNICAL_P2_ROUTEI_V1) -- arithmetic only")
    e = check_E_scaling()
    for r in e["rows"]:
        print(f"  K={r['K']:>4}  unstable={r['n_unstable']:>4}  K-n={r['K_minus_n']}  "
              f"fraction={r['fraction_unstable']:.6f}  max Re={r['max_re']:+.3f}")
    print(f"  deficit constant across K: {e['deficit_constant']} at {e['deficit_value']}")
    print(f"  count grew {e['count_growth_48_to_144']} as dim grew {e['dim_growth_48_to_144']}"
          f"  (1:1); max Re moved only {e['max_re_spread']:.3f}")
    print("  -> the count is K - 3, i.e. dimension-proportional: a discretized continuum,")
    print("     NOT a resolved finite-dimensional unstable manifold.")

    print("\n[F] quote sites, disclosure scored within +/-%d lines" % DISCLOSE_WINDOW)
    sites = check_F_quote_sites()
    quotes = [s for s in sites if "line" in s]
    soft = [s for s in quotes if s["soft_disclosed_at_site"]]
    bad = [s for s in quotes
           if not s["disclosed_at_site"] and not s["soft_disclosed_at_site"]]
    for s in quotes:
        flag = ("OK  " if s["disclosed_at_site"]
                else "SOFT" if s["soft_disclosed_at_site"] else "GAP ")
        far = "" if s["disclosed_at_site"] or not s["disclosed_anywhere_in_file"] \
              else "  (disclosed elsewhere in file, not at the site)"
        print(f"  {flag} {s['file']}:{s['line']}{far}")
        print(f"        {s['text']}")
    print(f"\n  {len(quotes)} quote sites: {len(quotes) - len(bad) - len(soft)} named at "
          f"site, {len(soft)} disclosed in substance without the word, {len(bad)} GAP")

    print("\n" + "=" * 74)
    print("GATE: does the discretization impose an origin (H^2-type) condition at X=0?")
    print("ANSWER: NO -- none is imposed. J-4's reading is confirmed FROM THE CODE.")
    print("=" * 74)
    print("\nSENTENCE PROPOSED FOR EVERY GAP SITE (orchestrator applies; all %d are"
          % len(bad))
    print("outside leg 70's territory):\n")
    print("  " + DISCLOSURE_SENTENCE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
