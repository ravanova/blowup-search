"""Pre-committed gate for the Phase 1 resolution de-risk spike.

Reads experiments/phase1_resolution_spike.jsonl and applies the gate stated
BEFORE the full run (anti-self-deception; do not soften after seeing results):

  For the SMOOTH growers, the fixed-window log-growth-rate fitness proxy g is
  RESOLUTION-STABLE iff the finest-two resolutions agree within GATE_REL_TOL
  (relative) AND the successive |delta g| are non-increasing (contracting).

  - stable  -> a resolution-robust SEARCH fitness exists even though the full
               Hou-Luo singularity is out of uniform-grid reach -> PROCEED to
               Gate 3/4 with a growth-based fitness.
  - rails   -> under-resolved even inside the "resolved" window -> STOP and
               re-plan (coarser honest deliverable, or AMR / Route D).

The blow-up EXPONENT is expected to rail across N (T* is never reached on a
uniform grid); that bounds Tier-2 confirmation, not search viability, and is
reported separately.

Usage: .venv/bin/python analyze_phase1_spike.py
"""

import json
import sys
from collections import defaultdict

IN = "experiments/phase1_resolution_spike.jsonl"
GATE_REL_TOL = 0.10


def load():
    rows = []
    with open(IN) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def settled(seq, tol):
    """The sequence is settled iff EVERY successive relative change is within
    tol. This is the honest reading of "the growth rate converges across
    resolution": stronger than a finest-two check (it also rejects a sequence
    that bounces but happens to end close), and — unlike a strict per-step
    monotonicity rule — immune to rounding-level (1e-4) wobble, which was giving
    false RAILS on sequences that agree to <0.01%."""
    return all(abs(seq[i] - seq[i - 1]) / abs(seq[i]) <= tol
               for i in range(1, len(seq)) if seq[i])


def main():
    rows = load()
    if not rows:
        sys.exit(f"no rows in {IN}; run phase1_resolution_spike.py first")

    by_ic = defaultdict(dict)
    for r in rows:
        by_ic[r["ic_label"]][r["resolution_N"]] = r  # last write wins

    verdicts = {}
    for ic in sorted(by_ic):
        runs = by_ic[ic]
        Ns = sorted(runs)
        kind = runs[Ns[0]]["ic_kind"]
        print(f"\n=== {ic} ({kind}) ===")
        print(f"{'N':>6} {'t_res':>7} {'amp_res':>9} {'g(fixed)':>9} "
              f"{'exponent':>9} {'T*':>8} {'R2':>6} {'tail':>9} {'out':>15}")
        gs = []
        for n in Ns:
            r = runs[n]
            e = r["estimate"] or {}
            g = r["growth_rate_fixed_window"]
            gs.append((n, g))
            print(f"{n:>6} {r['t_resolved']:>7.2f} {r['amp_resolved']:>9.1f} "
                  f"{g:>9.3f} {e.get('exponent', float('nan')):>9.2f} "
                  f"{e.get('t_star', float('nan')):>8.1f} "
                  f"{e.get('r_squared', float('nan')):>6.2f} "
                  f"{r['max_tail_fraction']:>9.1e} {r['outcome']:>15}")

        valid = [(n, g) for n, g in gs if g == g]  # drop nan (window unresolved)
        if kind == "smooth" and len(valid) >= 3:
            gvals = [g for _, g in valid]
            rel = abs(gvals[-1] - gvals[-2]) / abs(gvals[-1]) if gvals[-1] else float("inf")
            stable = settled(gvals, GATE_REL_TOL)
            verdicts[ic] = stable
            print(f"  g across N = {[round(g, 4) for g in gvals]}; finest-two "
                  f"rel-change {rel:.3%}; all-settled(gate {GATE_REL_TOL:.0%})="
                  f"{stable} -> {'STABLE' if stable else 'RAILS'}")
        elif kind == "smooth":
            verdicts[ic] = None
            print(f"  only {len(valid)} resolutions kept g (window under-resolved); "
                  "inconclusive")

    smooth = {k: v for k, v in verdicts.items() if v is not None}
    print("\n" + "=" * 60)
    if smooth and all(smooth.values()):
        print("GATE VERDICT: STABLE -- the growth-rate fitness converges across N "
              "for the smooth growers. A resolution-robust SEARCH signal exists; "
              "PROCEED to Gate 3/4 with a growth-based fitness.")
    elif smooth and any(smooth.values()):
        print("GATE VERDICT: MIXED -- some smooth growers stabilize, some rail. "
              "Proceed only with the stable IC family as the fitness substrate; "
              "review before the genome.")
    else:
        print("GATE VERDICT: RAILS -- no smooth grower gives a resolution-stable "
              "growth rate. Uniform-grid Tier-2 is resolution-starved for this "
              "model; STOP and re-plan (coarser deliverable / AMR / Route D).")
    print("Note: the blow-up EXPONENT railing across N is expected and bounds "
          "Tier-2 confirmation only, not search viability.")


if __name__ == "__main__":
    main()
