"""Leg 206 (Route-GSA) -- the adversarial battery against `solver/ga_search.py`.

THE QUESTION (the leg's gate, verbatim):

    Under adversarial and degenerate inputs, does `ga_search.py` ever silently return a
    wrong value (a fitness, a converged individual, a termination flag) rather than
    reject or visibly propagate the defect?

**THE GATE ANSWERED YES.**  Of 34 cases, 30 of them hypothesis-violating, **9 return a
finite, plausible-looking result that is wrong** -- a fitness that discards the true global
optimum, a "converged individual" carrying a NaN gene, a genome of a different dimension
than the caller declared, a genome outside the caller's own box, and a `generations` count
reporting a full search that never bred a single child.  17 are correctly REJECTED (11 raise,
6 propagate `+inf` into `best_fitness` where the caller must see it), and 4 controls confirm
the engine still works on well-formed input.

WHAT THIS IS NOT.  **No GA compute runs here in the banned sense.**  The plan-of-record ban
is on *"any GA compute on an unvalidated fitness"* -- the certificate/weight fitness whose
six-property viability gate answered NO at legs 49 and 59.  Nothing in this file touches that
fitness, `solver/weight_search.py`, or any gCLM residual.  Every fitness below is a
three-line closed-form function (a sphere, a planted optimum, a constant) whose exact minimum
is known analytically *before* the call, which is the only way the pass-through question can
be asked at all: you cannot detect a silently wrong answer without independently knowing the
right one.  Populations are 12 and generations 6-40, i.e. microseconds of arithmetic, and no
result here is a statement about any profile, certificate or blow-up.
`solver/ga_search.py` is **READ-ONLY** under this leg, under either gate branch; nothing is
patched.  The repair, if the DM authorises one, belongs to a bench agent, exactly as legs 66,
69, 79, 89 and 98 were handled.

WHY THIS MODULE, AND WHY NOBODY HAS ASKED THIS BEFORE.  Three legs have touched the GA
lane -- 49 and 59 scored the FITNESS against the six-property gate, and 160 measured why a
coarser grid fakes a pass.  All three asked *is the fitness valid?*  None asked *does the
search engine underneath it handle bad input?*  The engine is the one component the standing
ban does not cover: the ban freezes what may be optimised, not whether the optimiser is
sound.  `ga_search.py` has no adversarial gate of any name in the tree (confirmed: no
`test_ga_search*` file exists; `test_ga.py` tests the unrelated `ga/` package; the only
exercise of this module is `test_gclm_family.py`, all of it on well-formed input).

THE PRE-COMMITTED CORRUPTION CRITERION (fixed before the run; see `SILENT_RATIO`).
A case counts as SILENT CORRUPTION when `ga_minimize` RETURNS -- no exception -- and the
returned `GAResult` satisfies at least one of:

  (a) `best_fitness` is finite, but the true optimum of the supplied fitness is strictly
      better, and by more than `SILENT_RATIO = 100x` relative to a well-formed CONTROL run
      at the identical seed, pop_size and generation count.  The control is what separates
      "the defect broke the search" from "the GA is stochastic and got unlucky".
  (b) `best_fitness` is finite while `best_genome` carries a non-finite gene -- a
      "converged individual" that is not a point of the search space.
  (c) `best_genome.size != len(lower)` -- the caller declared a genome dimension and got a
      different one back.
  (d) `best_genome` lies outside the declared box `[lower, upper]`.
  (e) `generations` reports the full requested budget while the population provably never
      changed -- a termination flag describing a search that did not happen.

Returning `+inf` in `best_fitness`, or raising, both count as FLAGGED, not silent.  Every
case reports its magnitude either way, including the flagged ones.

THE INDEPENDENT ORACLE.  Every fitness here has a closed-form minimiser, so the "right
answer" is not a second numerical computation that could share the first one's bug -- it is
arithmetic done on paper.  For the sphere on a box containing the origin the optimum is
exactly `0.0` at `g = 0`; for `PLANTED_FITNESS` it is exactly `-inf` on a square of measure
`0.0625` of the box; for a constant fitness every point is optimal.

WHETHER ANY BANKED RESULT IS AFFECTED -- the question that decides escalation.  Family E
answers it *statically*, without running anything: it parses (via `ast`, so importing the
experiment scripts cannot execute them) every live `ga_minimize` call site in the tree and
checks the three preconditions each defect needs.  All four call sites pass: bound pairs are
equal-length and finite, every config leaves `elite_frac` at the 0.1 default, and the only
production fitness (`gclm_family.residual_two_scale_relnorm`) is a ratio of norms, hence
structurally in `[0, +inf) u {nan}` and never `-inf`.  So **no banked artifact is corrupted
by any defect below** -- these are latent defects in infrastructure, orthogonal to the
standing GA ban, not a claim-adjacent finding.

Run:  .venv/bin/python experiments/p2_route_gsa_v1_adversarial.py
Writes: writeup/data/p2_route_gsa_v1_adversarial.json
"""
from __future__ import annotations

import ast
import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.ga_search import GAConfig, GAResult, ga_minimize  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- pre-committed constants -------------------------------------------------------
SILENT_RATIO = 100.0     # how much worse than the well-formed control counts as corruption
POP = 12                 # every case; small enough that the whole battery is microseconds
GENS = 6                 # the short budget, for the structural cases
GENS_LONG = 40           # the budget where a frozen search is visibly frozen
SEED = 0                 # every case; the module is deterministic per seed by contract
BOX_LO = [-1.0, -1.0]    # the well-formed reference box, contains the sphere's optimum
BOX_HI = [1.0, 1.0]
PLANT = np.array([0.3, -0.4])     # centre of the planted -inf basin
PLANT_HALFWIDTH = 0.25            # basin is a square of side 0.5 -> measure 0.25/4.0


# ---- the fitness substrate: closed-form, minimiser known on paper ------------------
def sphere(g):
    """f(g) = |g|^2.  Exact minimum 0.0 at g = 0, which is interior to BOX_LO/BOX_HI."""
    return float(np.sum(np.asarray(g, dtype=float) ** 2))


def planted_minus_inf(g):
    """A fitness whose TRUE global optimum is -inf, on a basin of known measure.

    This is not a contrived shape: it is what any log-scale objective does when it
    succeeds.  `log10(residual)` is exactly -inf at a zero residual, and this repo's own
    weight fitness is `log10(Y_0/budget)` (solver/weight_search.py:14).  A minimiser that
    cannot represent "perfect" is a minimiser that throws away the answer it was hired to
    find.  Everywhere off the basin the fitness is the sphere lifted by 1.0, so any
    returned value >= 1.0 proves the basin was discarded rather than never sampled."""
    g = np.asarray(g, dtype=float)
    if np.max(np.abs(g - PLANT)) < PLANT_HALFWIDTH:
        return -np.inf
    return float(np.sum(g ** 2)) + 1.0


def gene0_only(g):
    """f(g) = g[0]^2 -- gene 1 is INACTIVE.

    Also not contrived: an unused/parked parameter is the commonest shape in a real search
    box, and it is the shape under which a poisoned bound on that gene cannot be caught by
    the fitness returning nan.  Exact minimum 0.0 at g[0] = 0, any g[1]."""
    return float(np.asarray(g, dtype=float)[0] ** 2)


def const_one(g):
    return 1.0


def always_inf(g):
    return float("inf")


def always_nan(g):
    return float("nan")


def _cfg(**kw):
    kw.setdefault("pop_size", POP)
    kw.setdefault("n_generations", GENS)
    kw.setdefault("seed", SEED)
    return GAConfig(**kw)


class _Counting:
    """Wraps a fitness and records every genome it was asked about.

    Used only to MEASURE how much of the search actually happened (distinct offspring,
    evaluation count).  It never changes the value returned to the GA."""

    def __init__(self, fn):
        self.fn = fn
        self.seen = []

    def __call__(self, g):
        self.seen.append(np.array(g, dtype=float))
        return self.fn(g)

    def matrix(self):
        return np.array(self.seen) if self.seen else np.zeros((0, 0))


# ---- the harness -------------------------------------------------------------------
def _invoke(fitness, lower, upper, cfg):
    """Call ga_minimize, capturing exceptions AND any Python warnings it emits.

    Warnings matter to the gate's wording: a defect a caller can SEE is propagated, not
    silent.  numpy's RuntimeWarnings are the only channel this module has, and the count
    here is what decides whether a case is 'visible' on that channel."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            res = ga_minimize(fitness, lower, upper, cfg)
            err = None
        except Exception as exc:                          # noqa: BLE001 -- that is the point
            res, err = None, f"{type(exc).__name__}: {exc}"
    return res, err, [w.category.__name__ for w in caught]


def _describe(res: GAResult, lower):
    lo = np.asarray(lower, dtype=float)
    g = np.asarray(res.best_genome, dtype=float)
    return {
        "best_fitness": _jnum(res.best_fitness),
        "best_fitness_finite": bool(np.isfinite(res.best_fitness)),
        "genome": [_jnum(x) for x in np.atleast_1d(g)],
        "genome_dim": int(np.atleast_1d(g).size),
        "declared_dim": int(lo.size),
        "nonfinite_genes": int(np.sum(~np.isfinite(np.atleast_1d(g)))),
        "generations": int(res.generations),
    }


def _jnum(x):
    """JSON cannot hold inf/nan; keep them as tagged strings so nothing is lost."""
    x = float(x)
    if np.isnan(x):
        return "nan"
    if np.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


def _in_box(g, lower, upper):
    """Is the returned genome inside the box the caller declared?

    BROADCAST-AWARE on purpose: a length-1 `upper` against a length-3 `lower` is numpy's
    ordinary broadcast and the resulting box is well defined, so clause (d) must not fire on
    it.  Only a genuinely non-conforming shape, or a gene actually outside its own bounds
    (which includes any NaN gene, since every comparison against NaN is False), counts."""
    g = np.atleast_1d(np.asarray(g, dtype=float))
    lo = np.atleast_1d(np.asarray(lower, dtype=float))
    hi = np.atleast_1d(np.asarray(upper, dtype=float))
    with np.errstate(invalid="ignore"):
        try:
            return bool(np.all(g >= lo) and np.all(g <= hi))
        except ValueError:
            return False


def case(cid, family, what, fitness, lower, upper, cfg, *, violates, true_opt=None,
         control=None, expect, note=""):
    """Run one case and classify it against the pre-committed criterion.

    `expect` is the pre-committed disposition (SILENT / FLAGGED / RAISED / CONTROL) written
    down from the code read BEFORE the battery ran; the battery reports `verdict`, and the
    two are compared so a case cannot be silently re-labelled after the fact."""
    counted = _Counting(fitness)
    res, err, warns = _invoke(counted, lower, upper, cfg)

    row = {"id": cid, "family": family, "what": what, "violates_hypothesis": violates,
           "expected": expect, "warnings": warns, "note": note}

    if err is not None:
        row.update({"verdict": "RAISED", "error": err, "silent": False,
                    "evaluations": len(counted.seen)})
        return row

    d = _describe(res, lower)
    row.update(d)
    row["evaluations"] = len(counted.seen)

    reasons = []
    # (b) non-finite gene with a finite fitness
    if d["best_fitness_finite"] and d["nonfinite_genes"] > 0:
        reasons.append(f"(b) {d['nonfinite_genes']} non-finite gene(s) in a 'converged' "
                       f"individual whose fitness reads finite {d['best_fitness']}")
    # (c) dimension the caller did not declare
    if d["genome_dim"] != d["declared_dim"]:
        reasons.append(f"(c) returned genome dim {d['genome_dim']} != declared "
                       f"dim {d['declared_dim']}")
    # (d) outside the declared box
    if d["best_fitness_finite"] and not _in_box(res.best_genome, lower, upper):
        reasons.append("(d) returned genome is outside the declared box [lower, upper]")
    # A run that STOPPED EARLY says so in `generations`; the caller can see the budget was
    # not spent, so a worse fitness there is disclosed, not silent.  Clause (a) is therefore
    # suppressed for a visibly-truncated run -- see the D1 note.
    truncated = d["generations"] < cfg.n_generations

    # (a) worse than a well-formed control by more than SILENT_RATIO
    if control is not None and d["best_fitness_finite"] and not truncated:
        cres, cerr, _ = _invoke(control["fitness"], control["lower"], control["upper"],
                                control["config"])
        cf = float(cres.best_fitness) if cerr is None else float("nan")
        row["control_best_fitness"] = _jnum(cf)
        ratio = float(res.best_fitness) / cf if cf not in (0.0,) and np.isfinite(cf) else float("inf")
        row["control_ratio"] = _jnum(ratio)
        if np.isfinite(ratio) and ratio > SILENT_RATIO:
            reasons.append(f"(a) {ratio:.1f}x worse than the well-formed control at the "
                           f"identical seed/pop/generations (threshold {SILENT_RATIO:.0f}x)")
    # (a') the true optimum is known on paper and was not merely missed but DISCARDED
    if true_opt is not None and d["best_fitness_finite"]:
        row["true_optimum"] = _jnum(true_opt)
        if float(true_opt) == -np.inf:
            hits = sum(1 for g in counted.seen if fitness(g) == -np.inf)
            row["optimum_sampled_times"] = int(hits)
            if hits > 0:
                reasons.append(f"(a) the true optimum (-inf) was SAMPLED {hits} times out of "
                               f"{len(counted.seen)} evaluations and ranked WORST every time; "
                               f"returned {d['best_fitness']} instead")
    # (e) full budget reported over a provably frozen population
    m = counted.matrix()
    if m.size and m.shape[0] > cfg.pop_size:
        post = m[cfg.pop_size:]
        uniq = int(np.unique(np.nan_to_num(post, nan=-9e99), axis=0).shape[0])
        row["distinct_offspring"] = uniq
        row["offspring_evaluated"] = int(post.shape[0])
        gen0 = np.unique(np.nan_to_num(m[:cfg.pop_size], nan=-9e99), axis=0)
        frozen = uniq <= gen0.shape[0] and np.array_equal(
            np.unique(np.nan_to_num(post, nan=-9e99), axis=0), gen0)
        row["distinct_gen0"] = int(gen0.shape[0])
        # A population that was ALREADY a single point (a zero-width box, a pop_size of 1)
        # has nothing to breed and freezing it is honest arithmetic, not a lost search.
        # Clause (e) needs a genuinely non-degenerate population to have been available.
        if frozen and gen0.shape[0] > 1 and d["generations"] >= cfg.n_generations:
            reasons.append(f"(e) generations reports the full budget {d['generations']} while "
                           f"every one of the {post.shape[0]} post-gen-0 evaluations re-scored "
                           f"an unchanged population ({uniq} distinct genomes, all from gen 0)")

    row["silent_reasons"] = reasons
    row["silent"] = bool(reasons)
    # FLAGGED = the defect is DISCLOSED in the return value: either best_fitness is
    # non-finite, or `generations` reports fewer than the requested budget so the caller can
    # see the run was cut short. CLEAN = returned an honest, correct answer.
    row["verdict"] = "SILENT" if reasons else (
        "FLAGGED" if (not d["best_fitness_finite"] or truncated) else "CLEAN")
    return row


# ---- family E: does any LIVE call site trigger any of this? -------------------------
CALL_SITE_FILES = [
    "experiments/p2_two_scale_sweep.py",
    "experiments/p2_two_scale_kladder.py",
    "test_gclm_family.py",
    "writeup/4_p2_lottery/p2_ga_framework_evidence.py",
]


def _literal_lists(tree):
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, SyntaxError, TypeError):
                pass
    return out


def call_site_audit():
    """Static (ast, never imported, so nothing executes) audit of every ga_minimize call.

    Checks the three preconditions the measured defects need: (i) len(lower) == len(upper)
    and both finite -- defeats S-DIM and S-POISON; (ii) elite_frac < 1 -- defeats S-FREEZE;
    (iii) lower <= upper elementwise -- defeats S-INVERT.  A call site whose bounds are
    non-literal is reported as `unresolved` rather than assumed safe."""
    rows = []
    for rel in CALL_SITE_FILES:
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            rows.append({"file": rel, "status": "MISSING"})
            continue
        with open(path) as fh:
            src = fh.read()
        tree = ast.parse(src)
        consts = _literal_lists(tree)
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and getattr(node.func, "id", None) == "ga_minimize"):
                continue
            args = node.args
            entry = {"file": rel, "line": node.lineno, "elite_frac": "default(0.1)"}
            for kw in node.keywords:
                if isinstance(kw.value, ast.Call) and getattr(kw.value.func, "id", "") == "GAConfig":
                    for k2 in kw.value.keywords:
                        if k2.arg == "elite_frac":
                            entry["elite_frac"] = ast.dump(k2.value)
            for a in args:
                if isinstance(a, ast.Call) and getattr(a.func, "id", "") == "GAConfig":
                    for k2 in a.keywords:
                        if k2.arg == "elite_frac":
                            entry["elite_frac"] = ast.dump(k2.value)
            def _resolve(a):
                if isinstance(a, ast.Name) and a.id in consts:
                    return consts[a.id]
                try:
                    return ast.literal_eval(a)
                except (ValueError, SyntaxError, TypeError):
                    return None
            lo = _resolve(args[1]) if len(args) > 1 else None
            hi = _resolve(args[2]) if len(args) > 2 else None
            if lo is None or hi is None:
                # The two production sweeps pass the box through a `best_of(R, fn, lo, hi,
                # ...)` helper, so the call node itself carries only parameter names. The
                # boxes are still module-level literals (LO_*/HI_*, paired by suffix), and
                # those are what every caller of the helper supplies -- so resolve and check
                # every one of them rather than recording the site as unknown.
                pairs = {k[3:]: k for k in consts if k.startswith("LO_")}
                checked = []
                # Some boxes are BUILT by a small pure-literal constructor (kladder's
                # `even_bounds(K)`) rather than written as a constant. Extract that function's
                # source with ast and exec it in an EMPTY namespace -- the module is never
                # imported, so no experiment code runs -- then check the box it returns.
                for node2 in ast.walk(tree):
                    if isinstance(node2, ast.FunctionDef) and "bounds" in node2.name:
                        ns = {}
                        try:
                            exec(compile(ast.Module([node2], []), "<bounds>", "exec"), ns)
                        except Exception:                       # noqa: BLE001
                            continue
                        for arg in (1, 2, 3, 4, 6, 8):
                            try:
                                a_l, b_l = ns[node2.name](arg)
                            except Exception:                   # noqa: BLE001
                                continue
                            a = np.asarray(a_l, dtype=float)
                            b = np.asarray(b_l, dtype=float)
                            checked.append({
                                "box": f"{node2.name}({arg})", "dim": int(a.size),
                                "dims_match": bool(a.size == b.size),
                                "all_finite": bool(np.all(np.isfinite(a))
                                                   and np.all(np.isfinite(b))),
                                "correctly_oriented": bool(a.size == b.size
                                                           and np.all(a <= b)),
                            })
                # ... and some are literal lists written inline at the call to the helper.
                for node2 in ast.walk(tree):
                    if not (isinstance(node2, ast.Call)
                            and getattr(node2.func, "id", None) == "best_of"):
                        continue
                    lits = [x for x in node2.args if isinstance(x, (ast.List, ast.Tuple))]
                    if len(lits) == 2:
                        a = np.asarray(ast.literal_eval(lits[0]), dtype=float)
                        b = np.asarray(ast.literal_eval(lits[1]), dtype=float)
                        checked.append({
                            "box": f"inline literal at line {node2.lineno}", "dim": int(a.size),
                            "dims_match": bool(a.size == b.size),
                            "all_finite": bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b))),
                            "correctly_oriented": bool(a.size == b.size and np.all(a <= b)),
                        })
                for suffix, loname in sorted(pairs.items()):
                    hiname = "HI_" + suffix
                    if hiname not in consts:
                        continue
                    a = np.asarray(consts[loname], dtype=float)
                    b = np.asarray(consts[hiname], dtype=float)
                    checked.append({
                        "box": f"{loname}/{hiname}", "dim": int(a.size),
                        "dims_match": bool(a.size == b.size),
                        "all_finite": bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b))),
                        "correctly_oriented": bool(a.size == b.size and np.all(a <= b)),
                    })
                ok = bool(checked) and all(c["dims_match"] and c["all_finite"]
                                           and c["correctly_oriented"] for c in checked)
                entry.update({
                    "status": "SAFE" if (ok and entry["elite_frac"] == "default(0.1)")
                              else "AT_RISK",
                    "resolved_via": "module-level LO_*/HI_* literals (helper-passed box)",
                    "boxes": checked,
                })
            else:
                lo_a, hi_a = np.asarray(lo, dtype=float), np.asarray(hi, dtype=float)
                entry.update({
                    "dims_match": bool(lo_a.size == hi_a.size),
                    "all_finite": bool(np.all(np.isfinite(lo_a)) and np.all(np.isfinite(hi_a))),
                    "correctly_oriented": bool(lo_a.size == hi_a.size and np.all(lo_a <= hi_a)),
                    "dim": int(lo_a.size),
                })
                entry["status"] = "SAFE" if (entry["dims_match"] and entry["all_finite"]
                                             and entry["correctly_oriented"]
                                             and entry["elite_frac"] == "default(0.1)") else "AT_RISK"
            rows.append(entry)
    return rows


# ---- the battery -------------------------------------------------------------------
def build_cases():
    ctrl = {"fitness": sphere, "lower": BOX_LO, "upper": BOX_HI, "config": _cfg()}
    ctrl_long = {"fitness": sphere, "lower": BOX_LO, "upper": BOX_HI,
                 "config": _cfg(n_generations=GENS_LONG)}
    C = []

    # --- family A: NaN / Inf poisoning -------------------------------------------
    C.append(case("A1", "nan_inf", "upper bound NaN on an INACTIVE gene", gene0_only,
                  BOX_LO, [1.0, np.nan], _cfg(), violates=True, expect="SILENT",
                  note="the fitness cannot see the poisoned gene, so nothing turns the "
                       "genome's NaN into a NaN fitness"))
    C.append(case("A2", "nan_inf", "lower bound NaN on an INACTIVE gene", gene0_only,
                  [-1.0, np.nan], BOX_HI, _cfg(), violates=True, expect="SILENT"))
    C.append(case("A3", "nan_inf", "upper bound +inf on an INACTIVE gene ('unbounded above')",
                  gene0_only, BOX_LO, [1.0, np.inf], _cfg(), violates=True, expect="SILENT",
                  note="+inf is the natural way a caller writes 'no upper bound'; BLX's "
                       "hi - lo is then inf - inf = nan"))
    C.append(case("A4", "nan_inf", "lower bound -inf on an INACTIVE gene", gene0_only,
                  [-1.0, -np.inf], BOX_HI, _cfg(), violates=True, expect="SILENT"))
    C.append(case("A5", "nan_inf", "upper bound NaN on an ACTIVE gene", sphere,
                  BOX_LO, [1.0, np.nan], _cfg(), violates=True, expect="FLAGGED",
                  note="control for A1: when the fitness DOES read the gene, the NaN comes "
                       "back as +inf and the caller sees it"))
    C.append(case("A6", "nan_inf", "fitness returns NaN everywhere", always_nan,
                  BOX_LO, BOX_HI, _cfg(), violates=True, expect="FLAGGED"))
    C.append(case("A7", "nan_inf", "fitness returns +inf everywhere", always_inf,
                  BOX_LO, BOX_HI, _cfg(), violates=True, expect="FLAGGED"))
    C.append(case("A8", "nan_inf", "mutation_frac NaN", sphere, BOX_LO, BOX_HI,
                  _cfg(mutation_frac=np.nan), violates=True, expect="SILENT",
                  control=ctrl))
    C.append(case("A9", "nan_inf", "crossover_alpha NaN", sphere, BOX_LO, BOX_HI,
                  _cfg(crossover_alpha=np.nan), violates=True, expect="SILENT",
                  control=ctrl))
    C.append(case("A10", "nan_inf", "mutation_prob NaN", sphere, BOX_LO, BOX_HI,
                  _cfg(mutation_prob=np.nan), violates=True, expect="SILENT",
                  control=ctrl))

    # --- family B: the planted wrong value ---------------------------------------
    C.append(case("B1", "planted", "fitness whose TRUE optimum is -inf (a log-scale "
                  "objective at a zero residual)", planted_minus_inf, BOX_LO, BOX_HI,
                  _cfg(n_generations=GENS_LONG), violates=False, true_opt=-np.inf,
                  expect="SILENT",
                  note="-inf is a legitimate value of a MINIMISED objective, not an invalid "
                       "genome; `vals[~np.isfinite(vals)] = np.inf` cannot tell 'perfect' "
                       "from 'invalid' and demotes the optimum to the worst rank"))
    C.append(case("B2", "planted", "same fitness, optimum shifted to +inf-free region "
                  "(positive control)", lambda g: sphere(g) + 1.0, BOX_LO, BOX_HI,
                  _cfg(n_generations=GENS_LONG), violates=False, expect="CLEAN",
                  note="proves B1's loss is the -inf handling and not the basin's geometry"))
    C.append(case("B3", "planted", "bounds length mismatch: lower dim 1, upper dim 3",
                  sphere, [0.0], [1.0, 2.0, 3.0], _cfg(), violates=True, expect="SILENT",
                  note="dim = lower.size; upper never checked. The genome silently becomes "
                       "3-D and, because one uniform draw is broadcast across all three "
                       "genes, the initial population is a rank-1 line, not a box"))
    C.append(case("B4", "planted", "bounds length mismatch: lower dim 3, upper dim 1",
                  sphere, [0.0, 0.0, 0.0], [1.0], _cfg(), violates=True, expect="SILENT",
                  note="silently searches [0,1]^3 rather than rejecting a malformed box"))
    C.append(case("B5", "planted", "bounds length mismatch: lower dim 3, upper dim 2 "
                  "(non-broadcastable)", sphere, [0.0, 0.0, 0.0], [1.0, 2.0], _cfg(),
                  violates=True, expect="RAISED",
                  note="only the non-broadcastable mismatch is caught -- by numpy, not by "
                       "the module"))
    C.append(case("B6", "planted", "fitness returns a shape-(1,) array", lambda g: np.array([sphere(g)]),
                  BOX_LO, BOX_HI, _cfg(), violates=True, expect="RAISED"))
    C.append(case("B7", "planted", "fitness returns a shape-(2,) array", lambda g: np.array([sphere(g), 1.0]),
                  BOX_LO, BOX_HI, _cfg(), violates=True, expect="RAISED"))

    # --- family C: degenerate population and parameter bounds --------------------
    C.append(case("C1", "degenerate", "elite_frac = 1.0 (every slot elite)", sphere,
                  BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG, elite_frac=1.0),
                  violates=True, expect="SILENT", control=ctrl_long,
                  note="n_elite == pop_size, so the while-loop that breeds never runs; the "
                       "engine still spends the whole evaluation budget re-scoring the same "
                       "population and reports the full generation count"))
    C.append(case("C2", "degenerate", "elite_frac = 0.95", sphere, BOX_LO, BOX_HI,
                  _cfg(n_generations=GENS_LONG, elite_frac=0.95), violates=True,
                  expect="SILENT", control=ctrl_long,
                  note="rounds to n_elite = pop_size at pop_size = 12; the boundary of the "
                       "freeze is a rounding, not a documented limit"))
    C.append(case("C3", "degenerate", "elite_frac = 2.0", sphere, BOX_LO, BOX_HI,
                  _cfg(elite_frac=2.0), violates=True, expect="RAISED"))
    C.append(case("C4", "degenerate", "elite_frac = 0.0", sphere, BOX_LO, BOX_HI,
                  _cfg(elite_frac=0.0), violates=True, expect="CLEAN",
                  note="max(1, .) floors it at one elite; harmless"))
    C.append(case("C5", "degenerate", "elite_frac = -1.0", sphere, BOX_LO, BOX_HI,
                  _cfg(elite_frac=-1.0), violates=True, expect="CLEAN",
                  note="a negative elite fraction is meaningless input, accepted silently, "
                       "but max(1,.) makes it behave; reported, not counted as corruption"))
    C.append(case("C6", "degenerate", "inverted bounds: lower > upper", sphere,
                  [2.0, 2.0], [-1.0, -1.0], _cfg(), violates=True, expect="SILENT",
                  note="np.clip(x, lo, hi) with lo > hi returns hi unconditionally, so every "
                       "child collapses onto the single point `upper`"))
    C.append(case("C7", "degenerate", "inverted bounds on ONE gene only", sphere,
                  [-1.0, 2.0], [1.0, -1.0], _cfg(), violates=True, expect="SILENT"))
    C.append(case("C8", "degenerate", "zero-width box (lower == upper)", sphere,
                  [0.5, 0.5], [0.5, 0.5], _cfg(), violates=True, expect="CLEAN",
                  note="degenerate but honest: the only admissible point is returned"))
    C.append(case("C9", "degenerate", "empty bounds (dim 0)", sphere, [], [], _cfg(),
                  violates=True, expect="CLEAN",
                  note="a zero-dimensional search returns a zero-length genome and the "
                       "fitness of the empty vector; degenerate but not a wrong value"))
    C.append(case("C10", "degenerate", "pop_size = 0", sphere, BOX_LO, BOX_HI,
                  _cfg(pop_size=0), violates=True, expect="RAISED"))
    C.append(case("C11", "degenerate", "pop_size = 1", sphere, BOX_LO, BOX_HI,
                  _cfg(pop_size=1), violates=True, expect="CLEAN",
                  note="a one-member population is all-elite by the same arithmetic as C1, "
                       "but here the caller asked for it"))
    C.append(case("C12", "degenerate", "pop_size = -5", sphere, BOX_LO, BOX_HI,
                  _cfg(pop_size=-5), violates=True, expect="RAISED"))
    C.append(case("C13", "degenerate", "tournament_k = 0", sphere, BOX_LO, BOX_HI,
                  _cfg(tournament_k=0), violates=True, expect="RAISED"))
    C.append(case("C14", "degenerate", "tournament_k = -3", sphere, BOX_LO, BOX_HI,
                  _cfg(tournament_k=-3), violates=True, expect="RAISED"))
    C.append(case("C15", "degenerate", "tournament_k > pop_size", sphere, BOX_LO, BOX_HI,
                  _cfg(tournament_k=1000), violates=True, expect="CLEAN",
                  note="sampling with replacement, so an oversized tournament is only "
                       "maximal selection pressure, not an error"))

    # --- family D: the boundary of convergence -----------------------------------
    C.append(case("D1", "boundary", "target_fitness = +inf (stop immediately)", sphere,
                  BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG, target_fitness=np.inf),
                  violates=True, expect="FLAGGED", control=ctrl_long,
                  note="terminates after one generation and SAYS SO in `generations`; the "
                       "return value is worse but the termination flag is honest, so by the "
                       "pre-committed criterion this is visible, not silent"))
    C.append(case("D2", "boundary", "target_fitness = NaN", sphere, BOX_LO, BOX_HI,
                  _cfg(n_generations=GENS_LONG, target_fitness=np.nan), violates=True,
                  expect="CLEAN", note="NaN comparison is always False; the budget runs out "
                                       "normally, which is the safe direction"))
    C.append(case("D3", "boundary", "target_fitness exactly at the attainable optimum",
                  const_one, BOX_LO, BOX_HI, _cfg(target_fitness=1.0), violates=False,
                  expect="FLAGGED",
                  note="the early-stop boundary is <=, so an exactly-attained target does "
                       "stop the run; generations reports it"))
    C.append(case("D4", "boundary", "n_generations = 0", sphere, BOX_LO, BOX_HI,
                  _cfg(n_generations=0), violates=True, expect="CLEAN",
                  note="returns the best of the initial random sample and reports "
                       "generations = 0; exactly what was asked for, and honest"))
    C.append(case("D5", "boundary", "n_generations = -10", sphere, BOX_LO, BOX_HI,
                  _cfg(n_generations=-10), violates=True, expect="CLEAN",
                  note="range() over a negative budget is empty; same honest degeneracy "
                       "as D4, and a negative budget is accepted without comment"))
    C.append(case("D6", "boundary", "mutation_decay = 1.5 (sigma grows without bound)",
                  sphere, BOX_LO, BOX_HI, _cfg(mutation_decay=1.5), violates=True,
                  expect="CLEAN", note="clipping keeps it in the box; degrades to random "
                                       "search rather than corrupting"))
    C.append(case("D7", "boundary", "mutation_decay = 0.0 (mutation dies after gen 1)",
                  sphere, BOX_LO, BOX_HI, _cfg(mutation_decay=0.0), violates=True,
                  expect="CLEAN"))

    # --- family F: the controls ---------------------------------------------------
    C.append(case("F1", "control", "well-formed sphere run", sphere, BOX_LO, BOX_HI,
                  _cfg(n_generations=GENS_LONG), violates=False, expect="CLEAN"))
    C.append(case("F2", "control", "well-formed run on an inactive gene", gene0_only,
                  BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG), violates=False,
                  expect="CLEAN"))
    return C


def determinism_check():
    """The one property capabilities.py already claims: deterministic per seed."""
    a = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    b = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    c = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG, seed=1))
    return {"same_seed_identical": bool(a.best_fitness == b.best_fitness
                                        and np.array_equal(a.best_genome, b.best_genome)),
            "different_seed_differs": bool(a.best_fitness != c.best_fitness),
            "seed0_best": _jnum(a.best_fitness), "seed1_best": _jnum(c.best_fitness)}


def rank_diagnostic():
    """B3's second, quieter defect, measured: the mismatched-bounds population is RANK 1.

    With `lower` of length 1 and `upper` of length 3, `dim` is 1, so the uniform draw has
    shape (pop, 1) and is broadcast across all three genes -- every individual satisfies
    g_j = lower + u * width_j for a SINGLE u. The initial population therefore lies on a
    line through 3-space, not in the box, and no amount of crossover between collinear
    parents leaves that line (BLX interpolates); only mutation can, and mutation is a
    per-gene event at probability 0.3. So the caller does not merely get the wrong
    dimension -- the wrong-dimensional search starts from a degenerate 1-D sample."""
    counted = _Counting(sphere)
    ga_minimize(counted, [0.0], [1.0, 2.0, 3.0], _cfg(n_generations=1))
    m = counted.matrix()[:POP]
    centred = m - m.mean(axis=0)
    return {"declared_dim": 1, "realised_dim": int(m.shape[1]),
            "gen0_population_rank": int(np.linalg.matrix_rank(centred)),
            "gen0_population_rows": int(m.shape[0]),
            "note": "rank 1 of 3: the initial population is a line, not a box"}


def substrate():
    """The battery's declared substrate, for the test file to re-assert."""
    return {"fitnesses": ["sphere", "planted_minus_inf", "gene0_only", "const_one",
                          "always_inf", "always_nan"],
            "pop_size": POP, "generations": [GENS, GENS_LONG], "seed": SEED,
            "box": [BOX_LO, BOX_HI], "silent_ratio": SILENT_RATIO,
            "plant": PLANT.tolist(), "plant_halfwidth": PLANT_HALFWIDTH,
            "plant_basin_measure": float((2 * PLANT_HALFWIDTH) ** 2 / 4.0)}


def run():
    t0 = time.time()
    cases = build_cases()
    silent = [c for c in cases if c.get("silent")]
    summary = {
        "cases": len(cases),
        "hypothesis_violating": sum(1 for c in cases if c["violates_hypothesis"]),
        "silent_corruption": len(silent),
        "raised": sum(1 for c in cases if c["verdict"] == "RAISED"),
        "flagged": sum(1 for c in cases if c["verdict"] == "FLAGGED"),
        "clean": sum(1 for c in cases if c["verdict"] == "CLEAN"),
        "silent_ids": [c["id"] for c in silent],
        "expectation_mismatches": [c["id"] for c in cases if c["verdict"] != c["expected"]],
    }
    sites = call_site_audit()
    return {
        "leg": 206, "route": "GSA", "module": "solver/ga_search.py",
        "gate": ("Under adversarial and degenerate inputs, does ga_search.py ever silently "
                 "return a wrong value (a fitness, a converged individual, a termination "
                 "flag) rather than reject or visibly propagate the defect?"),
        "gate_answer": "YES" if silent else "NO",
        "criterion": {
            "silent_ratio": SILENT_RATIO,
            "clauses": {
                "a": "finite best_fitness worse than a well-formed control at the identical "
                     "seed/pop/generations by more than silent_ratio, or a known -inf "
                     "optimum sampled and discarded",
                "b": "finite best_fitness with a non-finite gene in best_genome",
                "c": "best_genome.size != len(lower)",
                "d": "best_genome outside the declared box",
                "e": "generations reports the full budget over a provably frozen population",
            },
        },
        "substrate": substrate(),
        "summary": summary,
        "cases": cases,
        "prediction_misses": {
            "ids": summary["expectation_mismatches"],
            "A10": ("predicted SILENT, measured CLEAN. `mutation_prob = NaN` makes every "
                    "`rng.random() < prob` comparison False, so mutation switches OFF "
                    "entirely -- but BLX crossover alone still converges to within the "
                    "control's factor, so no wrong value is returned. Recorded as a miss "
                    "rather than quietly deleted."),
            "B4": ("predicted SILENT, measured CLEAN. `lower` dim 3 against `upper` dim 1 "
                   "broadcasts to the well-defined box [0,1]^3 and the returned genome is "
                   "correct FOR THAT BOX. The malformed argument is accepted without "
                   "comment -- an unvalidated input, but not a wrong answer, so by the "
                   "pre-committed criterion it is not corruption. Contrast B3, where the "
                   "same class of mismatch DOES change the answer."),
        },
        "rank_diagnostic": rank_diagnostic(),
        "determinism": determinism_check(),
        "call_site_audit": {
            "rows": sites,
            "all_safe": all(r.get("status") == "SAFE" for r in sites),
            "conclusion": ("Every live ga_minimize call site passes all three preconditions "
                           "(equal-length finite bounds, correct orientation, default "
                           "elite_frac), and the only production fitness "
                           "(gclm_family.residual_two_scale_relnorm) is a ratio of norms, "
                           "structurally in [0,+inf) u {nan}, so it can never emit the -inf "
                           "that B1 exposes. No banked artifact is affected by any defect "
                           "found here."),
        },
        "ban_relationship": (
            "ORTHOGONAL to the standing ban on 'any GA compute on an unvalidated fitness'. "
            "That ban is about WHICH fitness may be optimised (legs 49/59's six-property "
            "gate, still NO); these are defects in the OPTIMISER's input handling, found "
            "with closed-form fitnesses whose minima are known on paper. No banned fitness "
            "was evaluated, no search was run or repaired, and solver/ga_search.py was not "
            "edited. The lift condition for that ban is untouched."),
        "wall_seconds": round(time.time() - t0, 3),
    }


def main():
    out = run()
    path = os.path.join(REPO, "writeup", "data", "p2_route_gsa_v1_adversarial.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=False)
        fh.write("\n")
    s = out["summary"]
    print(f"GATE: {out['gate_answer']}")
    print(f"  cases {s['cases']}  hypothesis-violating {s['hypothesis_violating']}")
    print(f"  SILENT {s['silent_corruption']}  RAISED {s['raised']}  "
          f"FLAGGED {s['flagged']}  CLEAN {s['clean']}")
    print(f"  silent ids: {s['silent_ids']}")
    print(f"  expectation mismatches: {s['expectation_mismatches'] or 'none'}")
    for c in out["cases"]:
        if c.get("silent"):
            print(f"\n  [{c['id']}] {c['what']}")
            for r in c["silent_reasons"]:
                print(f"      {r}")
    print(f"\n  determinism: {out['determinism']}")
    print(f"  call sites all safe: {out['call_site_audit']['all_safe']}")
    print(f"\nwrote {path}  ({out['wall_seconds']}s)")


if __name__ == "__main__":
    main()
