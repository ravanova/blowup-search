"""ADVERSARIAL gates for solver/ga_search.py -- Route-GSA, leg 206.

`test_gclm_family.py` is the only file in the tree that exercises this module, and every
call in it hands `ga_minimize` a WELL-FORMED problem: equal-length finite bounds, correctly
oriented, a nonnegative fitness, default operator parameters.  This file asks the other
question, the one legs 79/89/98 asked of their pipelines: **what does the search engine do
when the input is not well formed?**

**LEG 206'S GATE ANSWERED YES, AND NOTHING HAS BEEN REPAIRED.**  Of 41 cases, 36 of them
hypothesis-violating, **12 return a finite, plausible-looking result that is wrong**.
`solver/ga_search.py` is READ-ONLY under this leg under either gate branch; the repair, if the
DM authorises one, belongs to a bench agent, exactly as legs 66, 69, 79, 89 and 98 were
handled.  So the gates below are **GAP-PINS**: they assert the DEFECT, at the exact inputs,
with the measured magnitude, so that (i) the finding cannot decay, and (ii) whenever the
repair lands, every one of them fails loudly and must be INVERTED to assert the refusal --
the same conversion legs 66/79/83/85/89/91/92/98 made when their findings were fixed.

The gates split into three kinds, and the kind is stated in each docstring:

  * **GAP-PIN** gates assert a measured silent corruption.  Each carries the magnitude.  When
    `ga_search.py` is repaired these MUST fail; that failure is the repair's acceptance test,
    not a regression.
  * **HOLDS** gates assert the things the module already does right and must never lose --
    NaN and +inf fitnesses propagating to a visible `best_fitness = inf`, the malformed
    configurations that correctly raise, determinism per seed (the one property
    `capabilities.py` claims for this module), and the honest degeneracies (a zero-width box,
    a one-member population, a zero generation budget) that a clumsy repair could easily turn
    into spurious exceptions.
  * **CONTROL** gates are the positive controls: the engine must still find the sphere's
    optimum on a well-formed box.  These matter MORE in a leg that found defects, because
    "nothing works any more" must not be able to masquerade as robustness.

**NO GA COMPUTE IN THE BANNED SENSE RUNS HERE.**  The plan-of-record ban is on "any GA compute
on an unvalidated fitness" -- the certificate/weight fitness whose six-property gate answered
NO at legs 49 and 59.  Every fitness in this file is a closed-form function (a sphere, a
planted optimum, a constant) whose exact minimum is known on paper before the call, which is
the only way a silently-wrong answer can be detected at all.  Nothing here touches
`solver/weight_search.py`, any gCLM residual, or any certificate.

**NO BANKED RESULT IS AFFECTED.**  `test_no_live_call_site_is_exposed` re-runs the static
audit at test time: every live `ga_minimize` call site has equal-length finite correctly
oriented bounds and the default `elite_frac`, and the only production fitness
(`gclm_family.residual_two_scale_relnorm`) is a ratio of norms, hence structurally in
`[0,+inf) u {nan}` and never `-inf`.  These are LATENT defects.

Run: .venv/bin/python test_ga_search_adversarial.py
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.p2_route_gsa_v1_adversarial import (  # noqa: E402
    BOX_HI, BOX_LO, GENS_LONG, PLANT, PLANT_HALFWIDTH, POP, SEED, SILENT_RATIO,
    _cfg, gene0_only, planted_minus_inf, run, sphere,
)
from solver.ga_search import GAConfig, ga_minimize  # noqa: E402

# The battery's banked headline. A change here is a change in the finding, and it must be
# accompanied by a change in writeup/data/p2_route_gsa_v1_adversarial.json.
BANKED = {"cases": 41, "hypothesis_violating": 36, "silent_corruption": 12,
          "raised": 8, "flagged": 5, "clean": 16,
          "silent_ids": ["A1", "A2", "A3", "A4", "A8", "A9", "B1", "B3",
                         "C1", "C2", "C6", "C7"]}


# --------------------------------------------------------------------------------------
# GAP-PIN 1 -- the headline: a legitimate -inf optimum is demoted to the WORST rank.
# --------------------------------------------------------------------------------------
def test_gappin_minus_inf_optimum_is_discarded():
    """GAP-PIN. `evaluate` does `vals[~np.isfinite(vals)] = np.inf`, so it cannot tell
    'perfect' from 'invalid': `np.isfinite(-inf)` is False.

    A fitness of `-inf` is what ANY log-scale objective returns when it succeeds --
    `log10(residual)` at a zero residual, and this repo's own weight fitness is
    `log10(Y_0/budget)` (solver/weight_search.py:14).  DEAP, the reference framework, keeps
    validity in a SEPARATE flag (`fitness.valid`) precisely so magnitude cannot be mistaken
    for invalidity -- see writeup/novelty/leg_206.md Q2.

    MEASURED (seed 0, pop 12, 40 generations): the true optimum was SAMPLED 10 times out of
    492 evaluations, ranked WORST every time, and `ga_minimize` returned +1.0000004926368158
    -- a finite, plausible, converged-looking number -- instead of -inf.  The error is not a
    ratio; it is the whole real line.

    AFTER THE REPAIR this must fail: the returned best_fitness should be -inf."""
    r = ga_minimize(planted_minus_inf, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    assert np.isfinite(r.best_fitness), "the -inf demotion is gone -- INVERT this gate"
    assert r.best_fitness >= 1.0, (
        f"off the basin the fitness is sphere+1 >= 1, so {r.best_fitness} would mean the "
        f"basin was retained after all -- INVERT this gate")
    # and the optimum really was inside the box, sampled, and thrown away
    assert planted_minus_inf(PLANT) == -np.inf
    assert np.all(PLANT - PLANT_HALFWIDTH >= np.array(BOX_LO))
    assert np.all(PLANT + PLANT_HALFWIDTH <= np.array(BOX_HI))


def test_holds_positive_control_for_the_minus_inf_gate():
    """CONTROL for GAP-PIN 1. The same landscape with the basin lifted to a FINITE floor is
    found normally, which proves the loss above is the `-inf` handling and not the basin's
    geometry or a search failure."""
    def finite_floor(g):
        g = np.asarray(g, dtype=float)
        if np.max(np.abs(g - PLANT)) < PLANT_HALFWIDTH:
            return -1.0
        return float(np.sum(g ** 2)) + 1.0

    r = ga_minimize(finite_floor, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    assert r.best_fitness == -1.0, (
        f"a FINITE optimum in the same basin must be found; got {r.best_fitness}")


# --------------------------------------------------------------------------------------
# GAP-PIN 2 -- a non-finite bound yields a "converged individual" carrying a NaN gene.
# --------------------------------------------------------------------------------------
def test_gappin_nonfinite_bound_returns_nan_gene_with_finite_fitness():
    """GAP-PIN. Four ways to poison one bound of a gene the fitness does not read -- NaN
    upper, NaN lower, +inf upper, -inf lower -- and all four return a FINITE best_fitness
    with a NaN in `best_genome`.

    Why an unread gene is the realistic case and not a contrivance: an inactive or parked
    parameter is the commonest shape in a real search box, and it is exactly the case where
    nothing downstream can turn the genome's NaN into a NaN fitness that the caller would
    see.  `+inf` is worse than a typo -- it is how a caller naturally writes 'no upper
    bound', and BLX then computes `hi - lo = inf - inf = nan`.  `np.clip` does not remove
    NaN, so the poison persists to the returned genome.

    MEASURED: best_fitness = 6.761311476498164e-06 (finite, looks converged) with 1 of 2
    genes non-finite, on all four poisonings, and ZERO Python warnings reach the caller.

    AFTER THE REPAIR this must fail: a non-finite bound should be rejected at entry."""
    cases = [("nan_upper", BOX_LO, [1.0, np.nan]),
             ("nan_lower", [-1.0, np.nan], BOX_HI),
             ("posinf_upper", BOX_LO, [1.0, np.inf]),
             ("neginf_lower", [-1.0, -np.inf], BOX_HI)]
    for name, lo, hi in cases:
        r = ga_minimize(gene0_only, lo, hi, _cfg())
        assert np.isfinite(r.best_fitness), f"{name}: fitness became visible -- INVERT"
        assert np.sum(~np.isfinite(np.asarray(r.best_genome, dtype=float))) == 1, (
            f"{name}: the NaN gene is gone -- INVERT this gate")


def test_holds_nonfinite_bound_on_an_ACTIVE_gene_is_visible():
    """HOLDS. The contrast that makes the gate above a real gap and not a generic complaint:
    when the fitness DOES read the poisoned gene, the NaN it returns is mapped to +inf and
    the caller sees `best_fitness = inf`.  The module's defence works -- it just runs through
    the fitness, so it cannot cover a gene the fitness ignores."""
    r = ga_minimize(sphere, BOX_LO, [1.0, np.nan], _cfg())
    assert not np.isfinite(r.best_fitness), (
        "a poisoned ACTIVE gene must still surface as a non-finite best_fitness")


# --------------------------------------------------------------------------------------
# GAP-PIN 3 -- inverted bounds collapse the population onto a single point, silently.
# --------------------------------------------------------------------------------------
def test_gappin_inverted_bounds_collapse_and_leave_the_box():
    """GAP-PIN. `np.clip(x, lo, hi)` with `lo > hi` returns `hi` unconditionally -- DOCUMENTED
    numpy behaviour (numpy manual; issues #15693, #27960), so this is our unchecked
    precondition, not a numpy bug.  `ga_minimize` never checks `lower <= upper`.

    MEASURED (seed 0, pop 12, 6 generations, box [2,2] -> [-1,-1]): 66 of the 72 post-gen-0
    evaluations are the single point `upper`, only 2 distinct offspring are ever bred against
    63 in the correctly-oriented control, and the returned genome
    [-0.01187324, 0.05843147] satisfies NEITHER `>= lower` NOR `<= upper`.  The search after
    generation 0 does not happen, and nothing says so.

    AFTER THE REPAIR this must fail: inverted bounds should be rejected at entry."""
    lo, hi = [2.0, 2.0], [-1.0, -1.0]
    r = ga_minimize(sphere, lo, hi, _cfg())
    assert np.isfinite(r.best_fitness), "inverted bounds became visible -- INVERT this gate"
    g = np.asarray(r.best_genome, dtype=float)
    assert not (np.all(g >= np.array(lo)) and np.all(g <= np.array(hi))), (
        "the returned genome is inside the declared box -- INVERT this gate")
    assert r.generations == 6, "the termination flag still claims the full budget"


# --------------------------------------------------------------------------------------
# GAP-PIN 4 -- an all-elite population reports a full search it never ran.
# --------------------------------------------------------------------------------------
def test_gappin_elite_frac_one_freezes_the_search_and_says_nothing():
    """GAP-PIN. `n_elite = max(1, round(elite_frac * pop_size))`; at `elite_frac >= 1` that is
    `pop_size`, so `while len(new_pop) < cfg.pop_size` never executes and not one child is
    ever bred.  The engine nonetheless re-scores the unchanged population every generation --
    it spends the ENTIRE evaluation budget, 492 calls at pop 12 x 40 generations, identical
    to a healthy run -- and returns `generations = 40`.  A caller watching wall-clock time or
    the evaluation count sees a completed search.

    MEASURED: best_fitness 1.843704e-01 against the well-formed control's 2.133060e-07 at the
    identical seed, i.e. **864346.9x worse**, with `history` constant across all 40 entries.
    At `elite_frac = 0.95` the rounding still reaches pop_size and it is 1749.2x worse, so the
    cliff is a rounding boundary, not a documented limit.

    AFTER THE REPAIR this must fail: `elite_frac >= 1` should be rejected, or clamped to leave
    at least one breeding slot."""
    frozen = ga_minimize(sphere, BOX_LO, BOX_HI,
                         _cfg(n_generations=GENS_LONG, elite_frac=1.0))
    healthy = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    assert frozen.generations == GENS_LONG, "the termination flag claims a full search"
    assert len(set(frozen.history)) == 1, "the frozen run's history is constant"
    ratio = frozen.best_fitness / healthy.best_fitness
    assert ratio > SILENT_RATIO, (
        f"elite_frac=1.0 is only {ratio:.1f}x worse than the control -- INVERT this gate")


# --------------------------------------------------------------------------------------
# GAP-PIN 5 -- the box's dimension is taken from `lower` alone; `upper` is never checked.
# --------------------------------------------------------------------------------------
def test_gappin_bounds_length_mismatch_changes_the_genome_dimension():
    """GAP-PIN. `dim = lower.size` and `upper` is never validated against it.  With
    `lower = [0.0]` and `upper = [1.0, 2.0, 3.0]` the caller declares a ONE-gene search and
    gets a THREE-gene genome back, with no error.

    SciPy's `differential_evolution` derives N from PAIRED bounds, so this mismatch is not
    even representable there (writeup/novelty/leg_206.md Q4).

    There is a second, quieter defect in the same case: because `dim` is 1, the uniform draw
    has shape (pop, 1) and is broadcast across all three genes, so every individual satisfies
    `g_j = lower + u * width_j` for a SINGLE u.  MEASURED: the initial population's centred
    matrix has **rank 1 of 3** -- it is a line through 3-space, not a sample of a box, and BLX
    crossover between collinear parents cannot leave that line.

    AFTER THE REPAIR this must fail: `len(lower) != len(upper)` should be rejected."""
    r = ga_minimize(sphere, [0.0], [1.0, 2.0, 3.0], _cfg())
    assert np.asarray(r.best_genome).size == 3, "the dimension mismatch is gone -- INVERT"
    seen = []
    ga_minimize(lambda g: seen.append(np.array(g, float)) or sphere(g),
                [0.0], [1.0, 2.0, 3.0], _cfg(n_generations=1))
    m = np.array(seen)[:POP]
    assert np.linalg.matrix_rank(m - m.mean(axis=0)) == 1, (
        "the rank-1 initial population is gone -- INVERT this gate")


def test_gappin_nan_operator_parameters_silently_stop_the_search():
    """GAP-PIN. `mutation_frac = NaN` makes `sigma` NaN, and `crossover_alpha = NaN` makes
    every BLX child NaN; either way every offspring evaluates to NaN -> +inf, the elites are
    all that survive, and the run degenerates to 'return the best of the initial random
    sample' while reporting the full generation count.

    MEASURED: 635.1x worse than the well-formed control at the identical seed, for both.

    AFTER THE REPAIR this must fail: non-finite operator parameters should be rejected."""
    healthy = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg())
    for name, cfg in [("mutation_frac", _cfg(mutation_frac=np.nan)),
                      ("crossover_alpha", _cfg(crossover_alpha=np.nan))]:
        r = ga_minimize(sphere, BOX_LO, BOX_HI, cfg)
        assert r.generations == 6, f"{name}: the flag claims a full search"
        assert r.best_fitness / healthy.best_fitness > SILENT_RATIO, (
            f"{name}: no longer materially worse than the control -- INVERT this gate")


# --------------------------------------------------------------------------------------
# HOLDS -- what the module already does right and must not lose to a clumsy repair.
# --------------------------------------------------------------------------------------
def test_holds_nan_and_inf_fitness_propagate_visibly():
    """HOLDS. A fitness that is NaN or +inf everywhere returns `best_fitness = inf`, which the
    caller cannot miss.  This is the module's ONE working defence and the repair must keep it
    as a returned non-finite value rather than an exception -- the same disposition leg 98
    gave `radii_verdict`'s NaN handling."""
    for name, f in [("nan", lambda g: np.nan), ("inf", lambda g: np.inf)]:
        r = ga_minimize(f, BOX_LO, BOX_HI, _cfg())
        assert not np.isfinite(r.best_fitness), f"{name} fitness must stay visible"


def test_holds_malformed_configurations_raise():
    """HOLDS. Eight configurations already fail loudly, and must keep failing loudly:
    `pop_size` 0 and -5 and `tournament_k` 0 and -3 (empty argmin / negative dimension),
    `elite_frac = 2.0` (elite index past the population), a lower/upper mismatch that is not
    broadcastable (3 vs 2), and a fitness returning a shape-(1,) or shape-(2,) array."""
    def raises(fitness, lo, hi, cfg):
        try:
            ga_minimize(fitness, lo, hi, cfg)
        except Exception:                                  # noqa: BLE001 -- that is the point
            return True
        return False

    assert raises(sphere, BOX_LO, BOX_HI, _cfg(pop_size=0))
    assert raises(sphere, BOX_LO, BOX_HI, _cfg(pop_size=-5))
    assert raises(sphere, BOX_LO, BOX_HI, _cfg(tournament_k=0))
    assert raises(sphere, BOX_LO, BOX_HI, _cfg(tournament_k=-3))
    assert raises(sphere, BOX_LO, BOX_HI, _cfg(elite_frac=2.0))
    assert raises(sphere, [0.0, 0.0, 0.0], [1.0, 2.0], _cfg())
    assert raises(lambda g: np.array([sphere(g)]), BOX_LO, BOX_HI, _cfg())
    assert raises(lambda g: np.array([sphere(g), 1.0]), BOX_LO, BOX_HI, _cfg())


def test_holds_honest_degeneracies_must_not_become_exceptions():
    """HOLDS. Four degenerate-but-honest inputs return a correct answer today, and a repair
    that validates the box too aggressively would break them.  A zero-width box has exactly
    one admissible point and returns it; a one-member population is all-elite by the same
    arithmetic as GAP-PIN 4 but the caller asked for it; a zero (or negative) generation
    budget returns the best of the initial sample and REPORTS `generations = 0`; a tournament
    larger than the population is maximal selection pressure, not an error, because sampling
    is with replacement."""
    r = ga_minimize(sphere, [0.5, 0.5], [0.5, 0.5], _cfg())
    assert r.best_fitness == 0.5 and np.allclose(r.best_genome, [0.5, 0.5])

    r = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(pop_size=1))
    assert np.isfinite(r.best_fitness)

    for budget in (0, -10):
        r = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=budget))
        assert r.generations == 0 and np.isfinite(r.best_fitness)

    r = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(tournament_k=1000))
    assert np.isfinite(r.best_fitness)


def test_holds_early_stop_is_disclosed_in_the_generations_flag():
    """HOLDS, and the discrimination that keeps the battery honest.  `target_fitness = +inf`
    stops the run after ONE generation and the returned fitness is 864346.9x worse than a
    full run -- but `generations` says 1, not 40, so the caller can see the budget was not
    spent.  By the pre-committed criterion that is DISCLOSED, not silent, and the battery
    classifies it FLAGGED.  Contrast GAP-PIN 4, where the same magnitude of loss comes with
    `generations = 40`."""
    r = ga_minimize(sphere, BOX_LO, BOX_HI,
                    _cfg(n_generations=GENS_LONG, target_fitness=np.inf))
    assert r.generations == 1 < GENS_LONG, "the early stop must remain visible"


def test_holds_determinism_per_seed():
    """HOLDS. The one property `capabilities.py` claims for this module ('deterministic per
    seed').  Two runs at seed 0 agree exactly in both fitness and genome; seed 1 differs."""
    a = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    b = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    c = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG, seed=1))
    assert a.best_fitness == b.best_fitness
    assert np.array_equal(a.best_genome, b.best_genome)
    assert a.best_fitness != c.best_fitness


# --------------------------------------------------------------------------------------
# CONTROL -- the engine must still work.
# --------------------------------------------------------------------------------------
def test_control_well_formed_search_still_converges():
    """CONTROL. On a well-formed box the sphere's optimum is found to 2.13e-07 at seed 0,
    beating the best of an equal-budget uniform random sample by a wide margin.  A repair
    that makes everything above 'safe' by refusing to search is caught here."""
    r = ga_minimize(sphere, BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    assert r.best_fitness < 1e-5, f"the engine stopped working: {r.best_fitness}"
    rng = np.random.default_rng(SEED)
    n = POP * (GENS_LONG + 1)
    rand_best = float(np.min(np.sum((-1 + rng.random((n, 2)) * 2) ** 2, axis=1)))
    assert r.best_fitness < rand_best, (
        f"GA {r.best_fitness:.3e} must beat equal-budget random search {rand_best:.3e}")


def test_control_optimum_on_the_box_boundary_is_reachable():
    """CONTROL. Clipping is exact at the bounds, so an optimum sitting ON the boundary is
    attainable and not pushed inside -- the boundary-of-convergence case for a healthy box."""
    r = ga_minimize(lambda g: float((np.asarray(g, float)[0] - 1.0) ** 2),
                    BOX_LO, BOX_HI, _cfg(n_generations=GENS_LONG))
    assert r.best_fitness < 1e-4, f"boundary optimum not reached: {r.best_fitness}"
    assert np.asarray(r.best_genome)[0] <= 1.0, "clipping must not exceed the upper bound"


# --------------------------------------------------------------------------------------
# The battery, and the reason this leg does not escalate.
# --------------------------------------------------------------------------------------
def test_battery_matches_the_banked_headline():
    """The full 41-case battery re-run, checked against the banked counts.  A change here is
    a change in the finding and must move writeup/data/p2_route_gsa_v1_adversarial.json with
    it."""
    out = run()
    s = out["summary"]
    assert out["gate_answer"] == "YES"
    for k, v in BANKED.items():
        assert s[k] == v, f"{k}: banked {v}, measured {s[k]}"
    assert s["expectation_mismatches"] == ["A10", "B4"], (
        "the two honest prediction misses are part of the record")


def test_no_live_call_site_is_exposed():
    """The gate's escalation question, re-checked at test time rather than asserted once.

    Every live `ga_minimize` call site must have equal-length, finite, correctly oriented
    bounds and the default `elite_frac`; the boxes reached through a helper are resolved from
    the module-level literals and the pure-literal `even_bounds(K)` constructor, parsed with
    `ast` so no experiment code executes.  If a future call site ever fails this, the latent
    defects above stop being latent and the leg's ORTHOGONAL-to-the-GA-ban conclusion no
    longer holds."""
    out = run()
    audit = out["call_site_audit"]
    assert audit["all_safe"], [r for r in audit["rows"] if r.get("status") != "SAFE"]
    assert len(audit["rows"]) >= 9


def test_production_fitness_cannot_emit_minus_inf():
    """The other half of the escalation question, checked on the real object.

    `gclm_family.residual_two_scale_relnorm` is a ratio of norms, so it is structurally in
    `[0, +inf) u {nan}` and can never take the `-inf` value that GAP-PIN 1 exposes.  This is
    asserted on the SOURCE (no gCLM compute, no GA run, nothing banned): the function's final
    expression is a nonnegative quantity divided by a nonnegative scale."""
    import inspect

    from solver import gclm_family
    src = inspect.getsource(gclm_family.GCLMResidual.residual_two_scale_relnorm)
    assert "np.sqrt(np.mean(stretch ** 2))" in src, (
        "the denominator is no longer a norm -- re-check the -inf exposure")
    assert "-np.inf" not in src and "-inf" not in src


if __name__ == "__main__":
    fns = [(n, f) for n, f in sorted(globals().items())
           if n.startswith("test_") and callable(f)]
    failed = []
    for name, fn in fns:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as exc:
            failed.append((name, exc))
            print(f"  FAIL  {name}: {exc}")
    print(f"\n{len(fns) - len(failed)}/{len(fns)} gates pass "
          f"(GAP-PINs assert leg 206's UNREPAIRED defects; they must fail after a repair)")
    sys.exit(1 if failed else 0)
