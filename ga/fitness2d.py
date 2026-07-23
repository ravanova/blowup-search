"""nu_crit-analog fitness for the smooth 2D Boussinesq genome (Route A Phase 1,
Gate 3). THE fitness axis chosen by the pre-Gate-4 discrimination screen
(PHASE1_AXIS_SCREEN_RESULTS.md):

  nu_crit = the viscosity nu at which NET resolved amplification
            amp = max|w|(t_resolved) / max|w|(0)
  crosses A_CRIT = 2x, with kappa = 0 (nu the single regularizing knob; the theta
  scalar left undamped), measured only inside the tail_guard-trusted (resolved)
  window. Higher nu_crit = harder to kill = more blow-up prone.

This reuses ga.fitness.bisect_critical -- the warm-startable bisection with edge
censoring and post-hoc monotonicity probes -- with the v3 amplification-only
predicate: a run is on the blow-up side iff it diverged OR its net resolved
amplification reached A_CRIT. amplification is the project's blow-up currency and
is monotone in nu, unlike an in-window slope (the axis-screen smoke caught a
net-DECAYING run showing a positive in-window slope; amp cannot be fooled that
way). bisect_critical assumes blow-up at the LOW (nu=0) end and regularity at the
HIGH end -- exactly the nu_crit geometry -- and censors both edges: a non-grower
at nu=0 censors low (nu_crit = 0, the correct bottom for a non-buoyant control),
a still-growing high end censors high.

The tail_guard is what makes the fitness read only TRUSTED dynamics: solve stops
with outcome "under_resolved" once enstrophy piles at the grid scale, so amp is
the amplification achieved inside the resolved window, never a grid artifact
(PHASE1_SPIKE_RESULTS.md -- the singularity itself sharpens below grid scale on a
uniform grid, so t_final / max_omega bound the trustworthy window).

The `critical_value_monotone` / `monotone_probes` bisect_critical returns are
exactly the instrument Gate 4 needs to test property 6 (non-trivial optimum):
whether nu_crit is a genuine boundary or a censored/degenerate rail.

Not the GA driver: Gate 3 delivers the fitness callable; the full MAP-Elites
campaign is gated behind the NON-NEGOTIABLE Gate 4 six-property viability check.
"""

import time

from ga.fitness import bisect_critical
from solver.boussinesq import solve_boussinesq

# Frozen fitness constants, identical to the axis screen that chose this axis
# (phase1_axis_screen.py) so nu_crit here is comparable to the screen's values.
FITNESS2D_DEFAULTS = {
    "fitness_axis": "nu_crit_amp2x_kappa0",
    "A_CRIT": 2.0,          # net-amplification boundary: amp >= 2x (a doubling)
    "kappa": 0.0,           # theta scalar left undamped; nu the sole knob
    "t_max": 4.0,           # covers the resolved window of the screen's growers
    "tail_guard": 1e-3,     # the under-resolution trust instrument (spike)
    "amplification_factor": 1e5,  # never reached; the tail guard stops first
    "max_steps": 4000,
    "dt_max": 1e-2,
    "bisection": {
        "range": [0.0, 1.5],           # low end grows, high end viscosity-killed
        "tolerance": 5e-3,             # bisection half-width stop
        "warm_start": {"margin": 0.4},  # used only when a warm_center is passed
        "probe_fractions": [0.05, 0.15],  # monotonicity probes past the boundary
        "max_iters": 12,
    },
}


def _merge_config(config):
    cfg = {**FITNESS2D_DEFAULTS, **(config or {})}
    # shallow-merge the nested bisection block so a caller can override one key
    cfg["bisection"] = {**FITNESS2D_DEFAULTS["bisection"], **(cfg.get("bisection") or {})}
    return cfg


def _run(omega0, theta0, nu, cfg, buoyancy):
    return solve_boussinesq(
        omega0, theta0, nu=float(nu), kappa=cfg["kappa"], t_max=cfg["t_max"],
        buoyancy=buoyancy, symmetry="houluo",
        amplification_factor=cfg["amplification_factor"],
        tail_guard=cfg["tail_guard"], max_steps=cfg["max_steps"],
        dt_max=cfg["dt_max"])


def nu_crit(omega0, theta0, config=None, buoyancy=True, warm_center=None):
    """Bisect the amp>=A_CRIT boundary in nu for one (omega0, theta0) pair.

    Returns the bisect_critical dict: `critical_value` is nu_crit, plus
    `bracket_censored` ("low" non-grower / "high" still-growing / None clean),
    `critical_value_monotone`, `monotone_probes`, and the per-run list (each run
    carries amp, outcome, t_final, max_tail_fraction, conservation_drift)."""
    cfg = _merge_config(config)
    a_crit = float(cfg["A_CRIT"])

    def run_at(nu_val):
        t0 = time.perf_counter()
        r = _run(omega0, theta0, nu_val, cfg, buoyancy)
        amp = float(r.max_omega[-1] / r.max_omega[0])
        grew = (r.outcome == "diverged") or (amp >= a_crit)
        summary = {
            "amp": amp,
            "outcome": r.outcome,
            "t_final": float(r.t_final),
            "n_timesteps": int(r.n_timesteps),
            "max_tail_fraction": float(r.max_tail_fraction),
            "conservation_drift": float(r.conservation_drift),
            "wall_clock_seconds": time.perf_counter() - t0,
        }
        return grew, summary

    return bisect_critical(run_at, cfg["bisection"], warm_center=warm_center)


def nu_crit_from_genome(genome, n_res, config=None, buoyancy=True, warm_center=None):
    """Convenience: realize a Genome2D at resolution n_res and bisect nu_crit.
    This is the entry point the Gate-4 viability sweep drives over ~40 shapes."""
    from ga.genome2d_smooth import realize

    omega0, theta0 = realize(genome, n_res)
    return nu_crit(omega0, theta0, config=config, buoyancy=buoyancy,
                   warm_center=warm_center)
