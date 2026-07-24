"""Route A Phase 1 -- the 256->512 RANK-stability de-risk for g_frac.

This is the one un-run, expensive leg the g_sustained probe paused on
(PHASE1_GSUSTAINED_RESULTS.md, "Consequence / open decision"). The staged probe
established that g_frac's MAGNITUDE is on the uniform-grid resolution wall but its
RANK order is stable at N=128<->256 (Spearman +0.90) and survives the cheat audit.
The whole forward path (reformulated rank-based Gate 4) turns on ONE question:

  does the RANKING hold at higher N, or is even the rank on the wall?

This script answers it. It runs the SAME 20-shape fixed-split roster (the LEG-2
roster of the probe) at N=256 AND N=512, then reports:

  1. Spearman(rank@256, rank@512) for g_frac -- the decision statistic. The probe's
     precommitted bar is Spearman > ~0.85 to proceed to the reformulated Gate 4.
     accel_ratio (the KNOWN small-denominator cheat) is run alongside as a control:
     it was MORE rank-stable at 128<->256 (+0.95) precisely because it is organized
     by a resolution-stable cheat, so it is NOT a positive signal -- it is the
     reminder that rank-stability is necessary, not sufficient.

  2. The FULL cheat audit re-run AT N=512 (not just carried over from 256): winner
     is a genuine grower?, top-5 growers, rho(g_frac, log|w0|) [omega0 cheat],
     rho(g_frac, early_rate) [spike early-growth mis-rank], rho(g_frac, centroid)
     [structure], rho(g_frac, t_res) [fast-scale-generators rank high]. Banked
     lesson: interrogate the winner against the dumbest cheat at the NEW resolution
     too -- a rank can be stable AND cheat-organized (that is exactly accel_ratio).

Reuses the probe's solver, currencies, run_roster, and audit helpers verbatim, so
the 256 numbers here are directly comparable to the probe's 256 numbers.

Cheap-first accounting: N=256 roster (~cheap) + N=512 roster (~20-40 min, the
expensive leg). One nu=0 solve per (shape, N); no bisection.

Usage: .venv/bin/python phase1_gsustained_rankcheck.py --workers 8
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import argparse
import json
import multiprocessing
import sys
from datetime import datetime, timezone

import numpy as np

from ga.logbook import code_version, working_tree_dirty
from phase1_gate4_probe import build_probe_roster
from phase1_gsustained_probe import T_MAX, _rho, _spearman, run_roster

RANK_RES = (256, 512)          # the de-risk: does 128<->256 stability survive to 512?
PROCEED_BAR = 0.85             # precommitted: Spearman(256,512) > this => reformulated Gate 4


def _audit(rows256, rows512, cur):
    """Spearman(256,512) for `cur` + the full cheat audit re-run at N=512."""
    labs = sorted(rows256)
    a = [rows256[l][cur] for l in labs]
    b = [rows512[l][cur] for l in labs]
    sp = _spearman(a, b)

    fin = [rows512[l] for l in labs if np.isfinite(rows512[l][cur])]
    fin.sort(key=lambda r: -r[cur])
    v = [r[cur] for r in fin]
    win = fin[0]
    grow = lambda r: r["t_res"] < T_MAX - 1e-6
    return {
        "currency": cur,
        "spearman_256_512": sp,
        "n_finite@512": len(fin),
        "winner": win["label"],
        "winner_class": win["shape_class"],
        "winner_is_grower": bool(grow(win)),
        "top5_growers": int(sum(grow(r) for r in fin[:5])),
        "rho_logw0": _rho(v, list(np.log([r["max_w0"] for r in fin]))),
        "rho_early_rate": _rho(v, [r["early_rate"] for r in fin]),
        "rho_centroid": _rho(v, [r["descriptors"]["centroid"] for r in fin]),
        "rho_t_res": _rho(v, [r["t_res"] for r in fin]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_gsustained_rankcheck.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not args.allow_dirty:
        sys.exit("working tree is dirty; commit first (or --allow-dirty)")
    base = dict(code_version=code_version(), code_dirty=dirty)

    tasks = [dict(label=s["label"], cls=s["cls"], genome=s["genome"], n=n, base=base)
             for s in build_probe_roster() for n in RANK_RES]
    # run N=512 first (long tail) so the slow solves are not stuck behind the fast ones
    tasks.sort(key=lambda t: -t["n"])
    print(f"rank-check: 20-shape roster at N={RANK_RES} = {len(tasks)} solves "
          f"on {args.workers} workers (N=512 is the expensive leg)", flush=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    rows = []
    with open(args.out, "a") as f:
        pool = multiprocessing.get_context().Pool(args.workers)
        try:
            done = 0
            for row in pool.imap_unordered(run_roster, tasks, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush(); rows.append(row)
                done += 1
                print(f"  [{done}/{len(tasks)}] {row['label']} N={row['resolution_N']} "
                      f"g_frac={row['g_frac']:+.3f} t_res={row['t_res']:.2f}", flush=True)
        finally:
            pool.close(); pool.join()

    _report(rows)
    print(f"\n-> {args.out}", flush=True)


def _report(rows):
    at = {(r["label"], r["resolution_N"]): r for r in rows}
    labs = sorted({r["label"] for r in rows})
    r256 = {l: at[(l, 256)] for l in labs if (l, 256) in at}
    r512 = {l: at[(l, 512)] for l in labs if (l, 512) in at}
    common = sorted(set(r256) & set(r512))
    r256 = {l: r256[l] for l in common}
    r512 = {l: r512[l] for l in common}

    print("\n=== 256->512 RANK-STABILITY (fixed-split 20-shape roster) ===")
    hdr = f"  {'shape':14s} {'g_frac@256':>11s} {'g_frac@512':>11s} {'t_res@256':>10s} {'t_res@512':>10s}"
    print(hdr)
    for l in sorted(common, key=lambda l: -r512[l]["g_frac"] if np.isfinite(r512[l]["g_frac"]) else 1e9):
        print(f"  {l:14s} {r256[l]['g_frac']:+11.3f} {r512[l]['g_frac']:+11.3f} "
              f"{r256[l]['t_res']:10.2f} {r512[l]['t_res']:10.2f}")

    print("\n=== DECISION STATISTIC + cheat audit re-run @N=512 ===")
    verdict = None
    for cur in ("g_frac", "accel_ratio"):
        a = _audit(r256, r512, cur)
        tag = "  (KNOWN CHEAT control)" if cur == "accel_ratio" else ""
        print(f"\n  [{cur}]{tag}")
        print(f"     spearman(256,512) = {a['spearman_256_512']:+.3f}  "
              f"(precommitted bar > {PROCEED_BAR}; finite@512={a['n_finite@512']}/{len(common)})")
        print(f"     winner={a['winner']}[{a['winner_class'][:4]}] grower={a['winner_is_grower']} "
              f"top5_growers={a['top5_growers']}/5")
        print(f"     rho(.,log|w0|)={a['rho_logw0']:+.3f}  rho(.,early_rate)={a['rho_early_rate']:+.3f}  "
              f"rho(.,centroid)={a['rho_centroid']:+.3f}  rho(.,t_res)={a['rho_t_res']:+.3f}")
        if cur == "g_frac":
            verdict = a

    print("\n=== VERDICT ===")
    sp = verdict["spearman_256_512"]
    holds = np.isfinite(sp) and sp > PROCEED_BAR
    cheatfree = (verdict["winner_is_grower"] and abs(verdict["rho_logw0"]) < 0.4
                 and verdict["top5_growers"] >= 3)
    print(f"  g_frac rank holds 256->512 (spearman {sp:+.3f} > {PROCEED_BAR}): {holds}")
    print(f"  g_frac still cheat-free @512 (winner grows, |rho_w0|<0.4, top5>=3 grow): {cheatfree}")
    if holds and cheatfree:
        print("  => RANK SURVIVES the wall. Proceed to reformulate the six-property")
        print("     predicate (property-4 RANK-stable, property-6 controlling for split)")
        print("     and run the full 40-shape Gate 4.")
    elif not holds:
        print("  => RANK IS ON THE WALL TOO. Even the ranking does not survive to N=512;")
        print("     the g_frac currency is a complete negative. Conclude the fitness search.")
    else:
        print("  => rank holds but a cheat re-emerges at 512; interrogate before proceeding.")


if __name__ == "__main__":
    main()
