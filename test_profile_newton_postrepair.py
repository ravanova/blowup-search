"""Leg 229, Route-PNRV: the banked POST-REPAIR check suite for leg 226's
repair of solver/profile_newton.py.

WHAT THIS FILE IS FOR
---------------------
Leg 226 added two tests (D2, the two gauge rows; D3, the decay class relative to
the a = 0 anchor) to `TwoScaleNewton.solve`'s `converged` verdict, and made
`continuation`'s warm/cold choice lexicographic in the decay class.  It reported
that this changes two of Route-D v11's four banked headline numbers.  Leg 226
wrote its repair and its own re-derivation in the same session, so no
independent run had ever re-derived either.  Leg 229 is that re-derivation
(`experiments/p2_route_pnrv_v1_postrepair.py`), and this file is the part of it
that is CHEAP ENOUGH TO RUN EVERY TIME -- banked so it cannot decay at the rate
of memory (standing lesson 68).  The three-hour arm lives in the runner; the
seconds-long arm lives here.

THE REPAIR IS NOT ON `main`.  It lives on branch `leg/226-pnr-v1-resume`, read
here with `git show` -- never checked out, never edited.  If that branch is not
reachable, the branch-dependent checks print UNAVAILABLE and are skipped rather
than failed: their absence is not a regression of anything `main` ships.  The
checks that test `main`'s own module and v11's own definitions always run.

WHAT EACH CHECK IS LOAD-BEARING FOR
-----------------------------------
* `check_the_newton_iteration_is_bit_identical` licences the whole measurement
  shortcut both legs use: v11's V3/V4 call only cold `solve()`, so if the repair
  moved a single float of the iteration, every "pre-repair value" either leg
  quotes from a post-repair run would be wrong.  Leg 226 checked ONE point.
* `check_D3_rejector_can_report_the_other_answer` is the control leg 226's own
  journal records getting WRONG the first time (lesson 90): its falsification
  probe added a constant tail and then re-imposed the amplitude gauge, which
  subtracted exactly the constant it had added, so every rung returned D3 =
  1.000 and the probe was vacuous.  This one varies the tail MULTIPLICATIVELY in
  the far field only, and asserts the rungs are DISTINCT before asserting they
  straddle the threshold -- identical numbers would be the bug, not the finding.
* `check_a_1p50_is_rejected_on_every_grid` pins this leg's own headline: the
  three grids that pre-repair reported three mutually contradictory speeds all
  around and were all flagged `converged`.
* `check_GA_boundary_cannot_move` pins the negative half of the census: no
  repair to profile_newton.py can move it, because it is a literal in v11's V3
  return dict and neither module mentions it.

Run:  .venv/bin/python test_profile_newton_postrepair.py
"""

import ast
import importlib.util
import os
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

np.seterr(all="ignore")

REPAIR_REF = "origin/leg/226-pnr-v1-resume"
PRE_REF = "6a17ce6"
V11_SRC = os.path.join(ROOT, "experiments", "p2_route_d_v11_anchor.py")

# Pinned from leg 229's own run of the repaired module (n = 101, the cheapest of
# v11's three a = 1.50 grids), not transcribed from leg 226's table.
A150_N101_PRE_C = 0.20426539933526314
A150_N101_D3_MIN = 1.0e5          # measured 1.120e+06; pinned an order low

_checks = []


def check(fn):
    _checks.append(fn)
    return fn


def _git_show(ref_path):
    r = subprocess.run(["git", "show", ref_path], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _load(name, src, tmpdir):
    path = os.path.join(tmpdir, name + ".py")
    with open(path, "w") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


TMP = tempfile.mkdtemp(prefix="pnrv_test_")
_post_src = _git_show("%s:solver/profile_newton.py" % REPAIR_REF)
_pre_src = _git_show("%s:solver/profile_newton.py" % PRE_REF)
POST = _load("_pnrv_t_post", _post_src, TMP) if _post_src else None
PRE = _load("_pnrv_t_pre", _pre_src, TMP) if _pre_src else None
BRANCH_OK = POST is not None and PRE is not None


def needs_branch(fn):
    def wrapper():
        if not BRANCH_OK:
            print("  UNAVAILABLE  %s -- branch %s not reachable; skipped, not "
                  "failed (the repair is not on main)"
                  % (fn.__name__, REPAIR_REF))
            return
        return fn()
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


# ===========================================================================
# THE LICENCE FOR THE MEASUREMENT SHORTCUT
# ===========================================================================


@check
@needs_branch
def check_the_newton_iteration_is_bit_identical():
    """The repair changes the returned dict, not the Newton loop.

    Both legs read pre-repair verdicts off post-repair runs, which is only valid
    if the iteration is untouched.  Checked here at two points on two grids, in
    exact equality -- not `np.allclose`, since agreement to a tolerance would be
    a different and much weaker statement.
    """
    for a, n in ((0.2, 101), (0.5, 201)):
        rp = PRE.TwoScaleNewton(a=a, n=n).solve(om0=None, c0=0.5)
        rq = POST.TwoScaleNewton(a=a, n=n).solve(om0=None, c0=0.5)
        assert rp["c"] == rq["c"], (a, n, "c moved", rp["c"], rq["c"])
        assert rp["relres"] == rq["relres"], (a, n, "relres moved")
        assert rp["iterations"] == rq["iterations"], (a, n, "iteration count moved")
        # And the pre-repair verdict really is recoverable post-repair.
        assert rq["residual_converged"] == rp["converged"], (
            a, n, "residual_converged is not the pre-repair `converged`")
    print("  OK  Newton iteration bit-identical pre/post at (0.2,101) and "
          "(0.5,201); `residual_converged` reproduces the pre-repair verdict")


# ===========================================================================
# THE REJECTORS, EACH WITH A CONTROL THAT CAN COME OUT THE OTHER WAY
# ===========================================================================


@check
@needs_branch
def check_D3_rejector_can_report_the_other_answer():
    """D3 must ACCEPT the anchor and REJECT a fattened far field.

    Leg 226's first version of this probe was vacuous (its gauge renormalisation
    cancelled the tail it added).  This one multiplies the OUTER half of the
    grid, leaves the two gauge nodes alone, and asserts the rungs are distinct
    before asserting they straddle -- four identical numbers would be the bug.
    """
    nw = POST.TwoScaleNewton(a=0.0, n=201)
    anc = nw.anchor()
    base = nw.decay_diagnostics(anc)["farfield_inflation"]
    assert abs(base - 1.0) < 1e-12, ("the anchor is not its own reference", base)

    X = nw.fam.X
    outer = np.abs(X) > 0.5 * np.max(np.abs(X))
    rungs = []
    for factor in (1.0, 10.0, 1e3, 1e5):
        om = anc.copy()
        om[outer] = om[outer] * factor
        rungs.append(nw.decay_diagnostics(om)["farfield_inflation"])
    assert len(set(rungs)) == len(rungs), (
        "the rungs are IDENTICAL -- the probe is measuring nothing (lesson 90)",
        rungs)
    assert rungs[0] < POST.FARFIELD_INFLATION_MAX <= rungs[2], (
        "D3 does not straddle its own threshold on this ladder", rungs)
    accepted = [r for r in rungs if r < POST.FARFIELD_INFLATION_MAX]
    rejected = [r for r in rungs if r >= POST.FARFIELD_INFLATION_MAX]
    assert accepted and rejected, ("D3 cannot report both answers", rungs)
    print("  OK  D3 ladder %s straddles the %.0fx threshold (%d accept, %d "
          "reject), rungs distinct"
          % (["%.3g" % r for r in rungs], POST.FARFIELD_INFLATION_MAX,
             len(accepted), len(rejected)))


@check
@needs_branch
def check_D2_gauge_rejector_can_report_the_other_answer():
    """D2 must be 0 on the anchor and non-zero on a gauge-violating profile."""
    nw = POST.TwoScaleNewton(a=0.0, n=201)
    anc = nw.anchor()
    # SCOPE, found by this check and not by either earlier leg: D2 is a test of
    # what `solve` RETURNS (Newton drives the two gauge rows), not a property
    # any admissible profile has.  The exact continuum anchor FAILS D2 by
    # 2.03e-3 -- three decades above GAUGE_TOL -- because gauge 2 pins
    # Omega = -1/2 at the node nearest X = 1, and that node is at
    # X = 0.9959420145786071, not at 1.  See check_the_width_gauge_node.
    base = nw.gauge_residual(anc)
    assert anc[nw.i0] + 1.0 == 0.0, "the anchor violates gauge 1 exactly"
    assert base > POST.GAUGE_TOL, (
        "the anchor now PASSES D2 -- the width-gauge node has moved onto "
        "X = 1 and this check's scope note is stale", base)
    solved = nw.solve(om0=None, c0=0.5)
    assert solved["gauge_residual"] < POST.GAUGE_TOL, (
        "the Newton solution itself fails the gauge test D2 rejects on",
        solved["gauge_residual"])
    for shift in (1e-3, 0.25):
        om = anc.copy()
        om[nw.i0] += shift
        got = nw.gauge_residual(om)
        assert abs(got - max(shift, base)) < 1e-12, (shift, got, base)
    bad = solved["Omega"].copy()
    bad[nw.i0] += 0.25
    assert nw.gauge_residual(bad) >= POST.GAUGE_TOL, "D2 cannot reject"
    assert nw.gauge_residual(solved["Omega"]) < POST.GAUGE_TOL, "D2 cannot accept"
    print("  OK  D2 = %.3e on the exact anchor (ABOVE GAUGE_TOL = %.0e -- D2 "
          "scopes solve()'s output, not any admissible profile), %.3e on the "
          "Newton solution, and tracks an imposed violation exactly"
          % (base, POST.GAUGE_TOL, solved["gauge_residual"]))


# ===========================================================================
# A PROPERTY OF THE SHARED SUBSTRATE, FOUND BY THIS LEG'S OWN CONTROL
# ===========================================================================


@check
def check_the_width_gauge_node_does_not_move_under_refinement():
    """The width gauge is imposed at X = 0.9959420145786071 at EVERY n.

    `i1 = argmin|X - 1|` and the rho-grids are nested, so the node nearest
    X = 1 is the SAME node at n = 101 and at n = 1601 -- a 16x refinement that
    moves it not at all.  Consequences, each a magnitude rather than a boolean:

      * gauge 2 asks for Omega = -1/2 at X = 0.99594, while -1/2 is the
        anchor's value at X = 1 exactly.  The exact anchor therefore misses
        gauge 2 by 2.033109e-03, IDENTICALLY at every resolution.
      * so the discrete a = 0 traveling wave is a slightly narrower profile
        than the anchor, and its speed is not 1/2 but X[i1]/2 =
        0.49797100728930355 -- which is what v11's own V4 rows report at
        a = 0 (0.4979712 at n = 401, 0.4979710 at n = 801).

    Four identical numbers across a refinement ladder are normally the tell for
    a control that cannot come out differently (lesson 90).  Here they are the
    finding: the quantity really is grid-independent, and this check asserts
    the nesting that makes it so, so that it cannot be mistaken for either a
    bug or a discretization error later.

    This is a statement about `solver/gclm_family`'s grid and v11's gauge
    choice.  It is NOT a defect of leg 226's repair, and leg 229 changes
    nothing on account of it.
    """
    from solver.gclm_family import GCLMResidual                      # noqa: E402
    seen = {}
    for n in (101, 201, 401, 801, 1601):
        f = GCLMResidual(a=0.0, n=n)
        X = f.X
        i1 = int(np.argmin(np.abs(X - 1.0)))
        anc = -1.0 / (1.0 + X ** 2)
        seen[n] = (X[i1], abs(anc[i1] + 0.5), f.drho)
    xs = {v[0] for v in seen.values()}
    gs = {v[1] for v in seen.values()}
    assert len(xs) == 1, ("the width-gauge node now moves with n -- this "
                          "check's whole reading is stale", seen)
    assert len(gs) == 1, ("the anchor's gauge-2 miss now depends on n", seen)
    assert abs(seen[101][2] / seen[1601][2] - 16.0) < 1e-9, (
        "the grid is not refining 16x across this ladder", seen)
    x1 = xs.pop()
    g1 = gs.pop()
    assert x1 == 0.9959420145786071, ("the gauge node moved", x1)
    assert g1 == 0.0020331094880823297, ("the gauge miss moved", g1)
    print("  OK  width gauge pinned at X = %.16f for n = 101..1601 (drho 16x), "
          "anchor misses gauge 2 by %.6e at every n; predicted discrete a=0 "
          "speed X[i1]/2 = %.17f" % (x1, g1, x1 / 2))


# ===========================================================================
# THIS LEG'S OWN HEADLINE, PINNED
# ===========================================================================


@check
@needs_branch
def check_a_1p50_is_rejected_post_repair_and_accepted_before():
    """a = 1.50, n = 101: pre-repair `converged` on an off-branch root.

    The cheapest of v11's three a = 1.50 grids, walked on leg 226's own
    continuation ladder.  Pre-repair this returns `converged = True` at a speed
    that disagrees with the other two grids by 163%; post-repair it is rejected
    on the decay class.  Pinned in exact equality on the pre-repair speed: this
    is the number a future change would have to move.
    """
    ladder = [float(v) for v in np.round(np.arange(0.0, 1.51, 0.15), 10)]
    pre_row = [r for r in PRE.continuation(ladder, n=101)
               if abs(r["a"] - 1.5) < 1e-12][0]
    post_row = [r for r in POST.continuation(ladder, n=101)
                if abs(r["a"] - 1.5) < 1e-12][0]
    assert pre_row["converged"] is True, "pre-repair no longer accepts a=1.50"
    assert pre_row["c"] == A150_N101_PRE_C, (
        "the pre-repair a=1.50 speed moved", pre_row["c"], A150_N101_PRE_C)
    assert post_row["converged"] is False, "the repair no longer rejects a=1.50"
    assert post_row["farfield_inflation"] >= A150_N101_D3_MIN, (
        "the a=1.50 root is no longer far off-branch",
        post_row["farfield_inflation"])
    assert "off-branch decay class" in (post_row.get("reason") or ""), (
        "rejected for a different reason than the decay class",
        post_row.get("reason"))
    print("  OK  a=1.50 n=101: pre-repair converged at c = %.15f; post-repair "
          "REJECTED, D3 = %.3e (off-branch decay class)"
          % (pre_row["c"], post_row["farfield_inflation"]))


@check
@needs_branch
def check_the_repair_is_not_a_blanket_rejection():
    """A rejector that rejected everything would reproduce the headline for the
    wrong reason.  The genuine small-a branch must still be ACCEPTED."""
    accepted = []
    for a in (0.0, 0.2, 0.5):
        r = POST.TwoScaleNewton(a=a, n=201).solve(om0=None, c0=0.5)
        if r["converged"]:
            accepted.append((a, r["farfield_inflation"]))
    assert len(accepted) >= 2, (
        "the repaired verdict accepts almost nothing -- it is a blanket "
        "rejector, and any headline it produces is uninformative", accepted)
    print("  OK  the repaired verdict still accepts the genuine branch at %s"
          % ", ".join("a=%.1f (D3 %.3g)" % t for t in accepted))


# ===========================================================================
# THE HEADLINE THAT CANNOT MOVE, AND WHY THAT IS NOT A VACUOUS CONTROL
# ===========================================================================


@check
def check_GA_boundary_is_a_literal_no_repair_can_move():
    """`GA_boundary` is a hardcoded literal in v11's V3 return dict.

    Reporting it as "unchanged by the repair" without saying this would be a
    control that cannot come out differently (lesson 90).  Asserted
    structurally, on v11's AST, and by the absence of the string from both
    modules -- so the claim is executable rather than remembered.
    """
    with open(V11_SRC) as fh:
        src = fh.read()
    tree = ast.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    found = None
    for node in ast.walk(funcs["v3_boundary"]):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value == "GA_boundary":
                    found = ast.literal_eval(v)
    assert found == [0.5, 0.55], ("GA_boundary is no longer the banked literal",
                                  found)
    live = open(os.path.join(ROOT, "solver", "profile_newton.py")).read()
    assert "GA_boundary" not in live, "profile_newton.py now mentions GA_boundary"
    if BRANCH_OK and _post_src is not None:
        assert "GA_boundary" not in _post_src, "the repair mentions GA_boundary"
    print("  OK  GA_boundary = [0.5, 0.55] is an AST-confirmed literal in v11's "
          "V3; the string appears in neither module, so no repair can move it")


@check
def check_v11_definitions_are_still_the_ones_this_leg_measured_against():
    """Every v11 constant leg 229's runner extracts, pinned.

    The runner reads these by AST instead of transcribing them.  If v11's source
    ever changes shape, the runner raises -- and this check says so in seconds
    rather than three hours into a re-run.
    """
    with open(V11_SRC) as fh:
        src = fh.read()
    tree = ast.parse(src)
    top = {n.targets[0].id: n.value for n in tree.body
           if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    assert ast.literal_eval(top["N"]) == 801, "v11's N moved"
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    v2_lists = [ast.literal_eval(n.value) for n in ast.walk(funcs["v2_sweep"])
                if isinstance(n, ast.Assign) and isinstance(n.value, ast.List)]
    assert len(v2_lists) == 1 and len(v2_lists[0]) == 17, (
        "v11's V2 a-ladder is no longer a single 17-point list")
    assert max(v2_lists[0]) == 1.0 and min(v2_lists[0]) == 0.0
    sig = funcs["v4_grids"].args
    kw = dict(zip([a.arg for a in sig.args],
                  [ast.literal_eval(d) for d in sig.defaults]))
    assert tuple(kw["ns"]) == (401, 801, 1601), "v11's V4 grids moved"
    assert tuple(kw["a_values"]) == (0.0, 0.2, 0.5, 0.8, 1.0), "V4 a-values moved"
    for expr in ('r["relres"] < 1e-8',
                 "max(cs) - min(cs) < 1e-3",
                 "n_ok >= 2",
                 'cs = [r["c"] for r in sub]',
                 'n_ok = sum(1 for r in sub if r["relres"] < 1e-8)'):
        assert expr in src, ("v11 no longer contains the expression %r that "
                             "leg 229 measured against" % expr)
    print("  OK  v11's N=801, 17-point V2 ladder, V4 grids (401,801,1601) x "
          "a in (0,0.2,0.5,0.8,1.0), and all five threshold expressions intact")


@check
def check_v11_spread_convention_differs_from_leg226s():
    """v11's V4 spreads over ALL grids and counts only the converged ones.

    Leg 226 took both statistics over the accepted rows.  They are different
    statistics, which is why leg 229 reports both -- pinned here so that the
    distinction cannot quietly evaporate into "the convention".
    """
    with open(V11_SRC) as fh:
        src = fh.read()
    i_cs = src.index('cs = [r["c"] for r in sub]')
    i_ok = src.index('n_ok = sum(1 for r in sub if r["relres"] < 1e-8)')
    assert i_cs < i_ok, "v11's V4 no longer computes cs before n_ok"
    seg = src[i_cs:i_ok]
    assert "relres" not in seg, (
        "v11's cs now filters on relres -- the two conventions have converged "
        "and leg 229's double reporting needs revisiting")
    print("  OK  v11's c_spread is over ALL grids while its count is over the "
          "converged ones -- distinct from leg 226's accepted-rows-only reading")


# ===========================================================================


def main():
    print(__doc__.strip().splitlines()[0])
    print()
    for fn in _checks:
        fn()
    print()
    if BRANCH_OK:
        print("%d/%d checks ran against leg 226's repaired module, read off %s "
              "with `git show`." % (len(_checks), len(_checks), REPAIR_REF))
    else:
        print("%d checks defined; the branch-dependent ones were SKIPPED "
              "because %s is unreachable. The repair is not on main, so this "
              "is not a regression -- but nothing here verified it either."
              % (len(_checks), REPAIR_REF))


if __name__ == "__main__":
    main()
