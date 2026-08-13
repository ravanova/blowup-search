"""Reduce U5's mined library to the part the repo needs to keep.

The full mined library is ~18 MB: 75,873 anchored strict local minima of R_red,
each with its full minimisation over the continuous x-shift and discrete
y-shift. It is a REGENERABLE INTERMEDIATE -- deterministic from
u5_shift_mining.py and the DNS checkpoint, and checked bit for bit against U2's
serial regeneration when it was built -- so it is gitignored beside the 1.2 GB
DNS artefacts it derives from, on the same rule.

What is committed instead is everything a reader needs to re-derive the
allocation and the pool-level statements without it:

  * every candidate that passed the Newton window R < 0.25, admissible or not.
    allocate() filters on the window first, so these reproduce the seed funnel
    and the chosen 100 EXACTLY -- the reduction cannot change which seeds were
    tried, and that is asserted here rather than asserted in prose.
  * the full-pool counts, unreduced.
  * the admission table against |s| over all 75,873, binned. This is the
    measurement U3 §5 made on 2,014 candidates, remade on 38x as many, and it
    is the reason the reduced file carries a histogram at all.

Usage:
    python experiments/programme_r4/u5_reduce_library.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from experiments.programme_r4 import u5_stratified_attempts as U5  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "u5_shift_library.json")
OUT = os.path.join(HERE, "u5_shift_library_admissible.json")

# Bins chosen to straddle the published band's edges (0.295 and 0.707) so the
# band is a union of bins and no bin has to be split to read the table.
EDGES = [0.0, 0.150, 0.295, 0.450, 0.550, 0.707, 0.900, 1.500, np.pi]


def main():
    with open(FULL) as f:
        lib = json.load(f)
    cand = lib["candidates"]
    a_s = np.array([U5.wrap_abs(c["s"]) for c in cand])
    R = np.array([c["R"] for c in cand])
    m = np.array([c["m"] for c in cand])
    win = R < U5.R_THRES_WINDOW

    table = []
    for lo, hi in zip(EDGES[:-1], EDGES[1:]):
        g = (a_s >= lo) & (a_s < hi)
        n = int(g.sum())
        table.append(dict(
            lo=float(lo), hi=float(hi), n=n,
            n_in_window=int((g & win).sum()),
            n_in_window_m0=int((g & win & (m == 0)).sum()),
            rate_in_window=float((g & win).sum() / n) if n else None,
            rate_admissible=float((g & win & (m == 0)).sum() / n) if n else None,
            median_R=float(np.median(R[g])) if n else None,
            fraction_m0=float(np.mean(m[g] == 0)) if n else None))

    keep = [c for c, w in zip(cand, win) if w]
    red = {k: v for k, v in lib.items() if k != "candidates"}
    red["candidates"] = keep
    red["reduction"] = dict(
        what=("every candidate that passed the Newton window R < 0.25 is kept; "
              "the rest are dropped, and the full library is a regenerable "
              "intermediate (gitignored, like the DNS artefacts it derives "
              "from)"),
        n_full=len(cand), n_kept=len(keep),
        allocation_is_unchanged_by_this=("asserted below, not claimed: the "
                                         "quota allocation is re-run on both "
                                         "and required to select the same 100 "
                                         "seeds in the same order"),
        regenerate_with="python experiments/programme_r4/u5_shift_mining.py")
    red["admission_vs_shift"] = dict(
        note=("U3 §5's admission-against-shift measurement, remade on the "
              "exhaustive anchored pool instead of 2,014 globally-ranked "
              "candidates. READ WITH ITS CONFOUND: for a candidate that is not "
              "a near-recurrence, the minimising shift is a nuisance parameter "
              "and |s| is close to meaningless, so the high-|s| bins mix 'shift "
              "is hard' with 'this was never a recurrence'. The m = 0 column is "
              "the one that separates them -- above |s| = 0.9 the window rate "
              "recovers while the m = 0 rate collapses, which says those cells "
              "are the y-shifted class the residual cannot express at all."),
        bins=table)

    # CONTAINMENT. R_red <= R pointwise, so every candidate U2 found admissible
    # has R_red <= R < 0.25 and must therefore be inside U5's take. That is a
    # prediction of the mining rule, not a restatement of it, and it is checked
    # against all 133 of U2's anchored admissible candidates rather than the 40
    # the mining pass sampled -- if the exhaustive pass had missed a region of
    # the (t, T) plane, this is where it would show.
    u2 = json.load(open(os.path.join(HERE, "u2_recurrence_library.json")))

    def admissible(c):
        return (c["in_newton_window"] and c["m"] == 0
                and U5.anchor_of(c["T"]) is not None)

    def key(c):
        return (c["snapshot_earlier"], round(c["T"], 9))

    a = {key(c): (c["R"], c["s"], c["m"]) for c in u2["candidates"]
         if admissible(c)}
    b = {key(c): (c["R"], c["s"], c["m"]) for c in keep if admissible(c)}
    missing = sorted(set(a) - set(b))
    disagree = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    red["containment_check"] = dict(
        statement=("every anchored admissible U2 candidate is inside U5's take, "
                   "with identical (R, s, m) to full float precision"),
        n_u2_anchored_admissible=len(a), n_u5_anchored_admissible=len(b),
        n_missing_from_u5=len(missing), n_disagreeing=len(disagree),
        passes=bool(not missing and not disagree))
    assert not missing, f"U5's take MISSES {len(missing)} U2 admissible candidates"
    assert not disagree, f"{len(disagree)} candidates disagree on (R, s, m)"
    print(f"containment: all {len(a)} U2 anchored admissible candidates are in "
          f"U5's {len(b)}, none disagreeing on (R, s, m)")

    # THE CHECK THAT MAKES THE REDUCTION SAFE.
    ch_full, fn_full = U5.allocate(lib, 100)
    ch_red, fn_red = U5.allocate(red, 100)
    same = ([(p["c"]["snapshot_earlier"], p["c"]["T"], p["c"]["s"])
             for p in ch_full]
            == [(p["c"]["snapshot_earlier"], p["c"]["T"], p["c"]["s"])
                for p in ch_red])
    assert same, "the reduction changed the allocation -- do NOT commit it"
    # n_candidates is the one entry that MUST differ -- it is the size of the
    # take, and the reduced file is not the take. Everything downstream of the
    # window has to be identical, and the full count is preserved in `counts`.
    drop = "n_candidates"
    assert ({k: v for k, v in fn_full.items() if k != drop}
            == {k: v for k, v in fn_red.items() if k != drop}), (
        "the reduction changed the seed funnel below the window")
    assert fn_full[drop] == lib["counts"]["n_candidates"] == len(cand)
    red["reduction"]["n_candidates_full"] = fn_full[drop]
    print(f"reduction {len(cand)} -> {len(keep)} candidates; allocation "
          f"identical: {same}; funnel below the window identical: True")

    with open(OUT, "w") as f:
        json.dump(red, f, indent=1)
    print(f"wrote {OUT} ({os.path.getsize(OUT)/1e6:.2f} MB)")
    print(f"{'|s| bin':>16} {'n':>7} {'window':>7} {'&m=0':>6} {'adm rate':>9} "
          f"{'med R':>7}")
    for t in table:
        print(f"[{t['lo']:.3f},{t['hi']:.3f}) {t['n']:7d} {t['n_in_window']:7d} "
              f"{t['n_in_window_m0']:6d} {t['rate_admissible']:9.2%} "
              f"{t['median_R']:7.4f}")


if __name__ == "__main__":
    main()
