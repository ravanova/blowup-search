"""Reformulated Gate 4 ANALYSIS — the FROZEN six-property predicate for `g_frac`.

Committed BEFORE the run (with phase1_gate4_reform.py) so a rail is a finding, not
a nudge. Reads experiments/phase1_gate4_reform.jsonl and reports each reformulated
property PASS/FAIL + the overall verdict. Contract + thresholds:
PHASE1_GATE4_REFORMULATED_PREDICATE.md. Produce/judge are separate scripts, same
discipline as the nu_crit Gate 4.

The six reformulated properties (rank-based inviscid growth-rate currency):
  1. Nonzero / discriminating -- growers have g_frac > G_MIN (not dead-flat).
  2. Direction + control      -- labeled sharp>mild>control at every N; euler
                                 censored low (replaces nu=hi "finite").
  3. Well-posed measurement   -- growers' g_frac finite AND window-robust (rank
                                 insensitive to the [0.5|0.6]*t_res window knob;
                                 replaces the bisection "monotone").
  4. RANK-resolution-stable   -- Spearman(rank@128,256) & (rank@256,512) >= RANK_MIN,
                                 not degrading, and 0 grower->non-grower flips.
  5. Wide band                -- grower g_frac spread >= WIDEBAND.
  6. Non-trivial optimum,      -- winner a grower / structured / not at a split rail /
     controlling for split       top-5 growers; no omega0 cheat (incl. partial-corr);
                                 structure not dissipation-penalized; split not a rail
                                 (interior sweep optimum + partial); STRUCTURED
                                 GRADIENT BEYOND SPLIT (partial rho(g,centroid|split)
                                 >= RESIDUAL_MIN -- the key strengthening); more than
                                 a t_res proxy.

Usage: .venv/bin/python analyze_phase1_gate4_reform.py [--in ...jsonl]
"""

import argparse
import json
from collections import defaultdict

import numpy as np

# --- FROZEN thresholds (pre-committed; see the predicate doc's rationale table) ---
T_MAX = 4.0
EPS = 1e-6
G_MIN = 0.10
NONZERO_FRAC = 0.80
WINDOW_ROBUST = 0.90
RANK_MIN = 0.85
RANK_EROSION = 0.10
WIDEBAND = 0.30
WINNER_CENTROID_MIN = 1.3 * np.sqrt(2.0)
SPLIT_RAIL_LO, SPLIT_RAIL_HI = 0.15, 0.85
RHO_W0 = 0.40
PARTIAL_W0 = 0.25
RHO_MAX = 0.70
RESIDUAL_MIN = 0.15
TOP5_GROWERS_MIN = 4
SWEEP_SPLITS = (0.10, 0.30, 0.50, 0.70, 0.90, 0.97)


# ----- stats helpers ---------------------------------------------------------
def _finite_pairs(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    return a[ok], b[ok]


def _pearson(a, b):
    a, b = _finite_pairs(a, b)
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def _spearman(a, b):
    a, b = _finite_pairs(a, b)
    if len(a) < 3:
        return float("nan")
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1]) if (np.std(ra) and np.std(rb)) else float("nan")


def _partial(x, y, z):
    """partial corr of x,y controlling for z (linear residuals)."""
    x, y, z = (np.asarray(v, float) for v in (x, y, z))
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[ok], y[ok], z[ok]
    if len(x) < 4:
        return float("nan")
    res = lambda a: a - np.polyval(np.polyfit(z, a, 1), z)
    return float(np.corrcoef(res(x), res(y))[0, 1])


def _grower(r):
    return isinstance(r.get("t_res"), (int, float)) and r["t_res"] < T_MAX - EPS


# ----- load ------------------------------------------------------------------
def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _by(rows, block):
    return [r for r in rows if r.get("block") == block]


def _at(rows, n):
    return {r["label"]: r for r in rows if r["resolution_N"] == n}


# ----- the six properties ----------------------------------------------------
def evaluate(rows):
    results = {}
    labeled = _by(rows, "labeled")
    roster = _by(rows, "roster")
    sweep = _by(rows, "sweep")
    res_ns = sorted({r["resolution_N"] for r in roster})
    n_fine = res_ns[-1]

    fine = _at(roster, n_fine)                       # genome shapes @ finest N
    growers_fine = {l: r for l, r in fine.items() if _grower(r)}
    randoms = {l: r for l, r in fine.items() if r["shape_class"] == "random"}
    rand_grow = {l: r for l, r in randoms.items() if _grower(r)}

    # --- 1. Nonzero / discriminating ---
    gv = [r["g_frac"] for r in growers_fine.values() if np.isfinite(r["g_frac"])]
    nz = [v for v in gv if v > G_MIN]
    p1 = len(gv) >= 3 and (len(nz) / len(gv)) >= NONZERO_FRAC and np.std(gv) > 0
    results["1. nonzero/discriminating"] = (
        p1, f"{len(nz)}/{len(gv)} growers > {G_MIN} ({len(nz)/max(len(gv),1):.0%}, "
            f"need {NONZERO_FRAC:.0%}); spread {max(gv)-min(gv):.3f}" if gv else (False, "no growers"))

    # --- 2. Direction + control censored (labeled) ---
    dir_ok, cens_ok, detail = True, True, []
    for n in res_ns:
        at = _at(labeled, n)
        if not all(k in at for k in ("smooth_sharp", "smooth_mild", "euler_control")):
            dir_ok = False; detail.append(f"N={n}:missing"); continue
        s, m, c = (at["smooth_sharp"]["g_frac"], at["smooth_mild"]["g_frac"],
                   at["euler_control"]["g_frac"])
        d = s > m > c
        cl = c < G_MIN
        dir_ok &= bool(d); cens_ok &= bool(cl)
        detail.append(f"N={n}:{s:+.2f}>{m:+.2f}>{c:+.2f}={'ok' if d else 'NO'},ctrl<{G_MIN}={'ok' if cl else 'NO'}")
    p2 = dir_ok and cens_ok
    results["2. direction+control"] = (p2, "; ".join(detail))

    # --- 3. Well-posed (finite + window-robust) ---
    finite_ok = all(np.isfinite(r["g_frac"]) for r in growers_fine.values())
    a = [r["g_frac"] for r in growers_fine.values()]
    b = [r.get("g_frac_06") for r in growers_fine.values()]
    win_rob = _spearman(a, b)
    p3 = finite_ok and np.isfinite(win_rob) and win_rob >= WINDOW_ROBUST
    results["3. well-posed measurement"] = (
        p3, f"finite growers={finite_ok}; window-robust spearman(g05,g06)={win_rob:+.3f} "
            f"(need >= {WINDOW_ROBUST})")

    # --- 4. RANK-resolution-stable ---
    if len(res_ns) >= 3:
        n0, n1, n2 = res_ns[0], res_ns[1], res_ns[-1]
        r0, r1, r2 = _at(roster, n0), _at(roster, n1), _at(roster, n2)
        common = [l for l in fine if l in r0 and l in r1 and l in r2]
        sp01 = _spearman([r0[l]["g_frac"] for l in common], [r1[l]["g_frac"] for l in common])
        sp12 = _spearman([r1[l]["g_frac"] for l in common], [r2[l]["g_frac"] for l in common])
        flips = [l for l in common
                 for (rc, rf) in [(r0[l], r1[l]), (r1[l], r2[l])]
                 if _grower(rc) and not _grower(rf)]
        p4 = (np.isfinite(sp01) and np.isfinite(sp12) and sp01 >= RANK_MIN
              and sp12 >= RANK_MIN and sp12 >= sp01 - RANK_EROSION and not flips)
        results["4. rank-resolution-stable"] = (
            p4, f"spearman({n0},{n1})={sp01:+.3f} spearman({n1},{n2})={sp12:+.3f} "
                f"(need both >= {RANK_MIN}, not degrading); grower->nongrower flips: "
                f"{sorted(set(flips)) or 'none'}")
    else:
        results["4. rank-resolution-stable"] = (None, f"need 3 resolutions, have {res_ns}")

    # --- 5. Wide band ---
    band = (max(gv) - min(gv)) if len(gv) >= 2 else 0.0
    p5 = band >= WIDEBAND
    results["5. wide band"] = (p5, f"grower g_frac spread {band:.3f} (need >= {WIDEBAND})")

    # --- 6. Non-trivial optimum controlling for split ---
    ranked = sorted((r for r in fine.values() if np.isfinite(r["g_frac"])),
                    key=lambda r: -r["g_frac"])
    sub = {}
    if len(ranked) >= 5 and len(rand_grow) >= 4:
        win = ranked[0]
        wd = win["descriptors"]
        sub["a_winner_grower"] = _grower(win)
        sub["b_winner_structured"] = (win["shape_class"] != "trivial"
                                      and wd["centroid"] >= WINNER_CENTROID_MIN)
        sub["b_winner_not_split_rail"] = SPLIT_RAIL_LO < wd["split"] < SPLIT_RAIL_HI
        sub["c_top5_growers"] = sum(_grower(r) for r in ranked[:5]) >= TOP5_GROWERS_MIN

        rg = list(rand_grow.values())
        gf = [r["g_frac"] for r in rg]
        lw0 = [np.log(r["max_w0"]) for r in rg]
        spl = [r["descriptors"]["split"] for r in rg]
        cen = [r["descriptors"]["centroid"] for r in rg]
        trs = [r["t_res"] for r in rg]
        rho_w0 = _pearson(gf, lw0)
        part_w0 = _partial(gf, lw0, spl)
        rho_cen = _pearson(gf, cen)
        part_cen_split = _partial(gf, cen, spl)         # residual beyond split (6g)
        part_split_w0 = _partial(gf, spl, lw0)
        rho_tres = _pearson(gf, trs)
        part_cen_tres = _partial(gf, cen, trs)          # beyond t_res proxy (6h)

        sub["d_no_omega0_cheat"] = (np.isfinite(rho_w0) and abs(rho_w0) <= RHO_W0
                                    and np.isfinite(part_w0) and part_w0 <= PARTIAL_W0)
        sub["e_structure_not_penalized"] = np.isfinite(rho_cen) and rho_cen > -RHO_MAX
        sub["g_gradient_beyond_split"] = (np.isfinite(part_cen_split)
                                          and part_cen_split >= RESIDUAL_MIN)
        sub["h_more_than_tres_proxy"] = (np.isfinite(part_cen_tres)
                                         and part_cen_tres >= RESIDUAL_MIN)

        # 6f interior optimum on the sweep + split acts through buoyancy
        interior = True; sweep_detail = []
        for basenm in sorted({r["label"].rsplit("_s", 1)[0] for r in sweep}):
            pts = sorted((r for r in sweep if r["label"].startswith(basenm + "_s")),
                         key=lambda r: r["target_split"])
            gg = [r["g_frac"] for r in pts]
            if not any(np.isfinite(x) for x in gg):
                continue
            am = pts[int(np.nanargmax(gg))]["target_split"]
            rail = am in (SWEEP_SPLITS[0], SWEEP_SPLITS[-1])
            interior &= not rail
            sweep_detail.append(f"{basenm}:argmax@{am}{'(RAIL)' if rail else ''}")
        sub["f_split_interior"] = interior and (np.isfinite(part_split_w0) and part_split_w0 > 0)

        p6 = all(sub.values())
        results["6. non-trivial optimum (split-controlled)"] = (
            p6,
            f"winner={win['label']}[{win['shape_class'][:4]}] g={win['g_frac']:+.3f} "
            f"cen={wd['centroid']:.2f} split={wd['split']:.2f} | "
            f"a_grow={sub['a_winner_grower']} b_struct={sub['b_winner_structured']} "
            f"b_notrail={sub['b_winner_not_split_rail']} c_top5={sub['c_top5_growers']} | "
            f"rho(w0)={rho_w0:+.2f} part(w0|split)={part_w0:+.2f} d={sub['d_no_omega0_cheat']} | "
            f"rho(cen)={rho_cen:+.2f} e={sub['e_structure_not_penalized']} | "
            f"part(cen|split)={part_cen_split:+.2f} g={sub['g_gradient_beyond_split']} | "
            f"rho(tres)={rho_tres:+.2f} part(cen|tres)={part_cen_tres:+.2f} h={sub['h_more_than_tres_proxy']} | "
            f"sweep[{', '.join(sweep_detail)}] part(split|w0)={part_split_w0:+.2f} f={sub['f_split_interior']}")
        results["_6sub"] = sub
    else:
        results["6. non-trivial optimum (split-controlled)"] = (
            None, f"too few growers ({len(ranked)} ranked, {len(rand_grow)} random growers)")

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="experiments/phase1_gate4_reform.jsonl")
    args = ap.parse_args()
    rows = load(args.inp)
    results = evaluate(rows)

    print(f"Reformulated Gate 4 analysis: {len(rows)} rows from {args.inp}\n")
    print("PROPERTY VERDICTS (frozen predicate):")
    passed = failed = 0
    for k, v in results.items():
        if k.startswith("_"):
            continue
        ok, detail = v
        if ok is None:
            tag = "N/A "
        elif ok:
            tag = "PASS"; passed += 1
        else:
            tag = "FAIL"; failed += 1
        print(f"  [{tag}] {k}")
        print(f"         {detail}")

    n_props = sum(1 for k in results if not k.startswith("_"))
    overall = ("PASS -- proceed to the GA campaign (Gate 5)"
               if failed == 0 and passed == n_props
               else "FAIL -- STOP. A finding, not a push-harder signal.")
    print(f"\nOVERALL: {passed} pass / {failed} fail / {n_props - passed - failed} N-A "
          f"=>  {overall}")
    if "_6sub" in results and not all(results["_6sub"].values()):
        bad = [k for k, v in results["_6sub"].items() if not v]
        print(f"  property-6 failing sub-conditions: {bad}")
        if bad == ["g_gradient_beyond_split"]:
            print("  (constructive finding: g_frac is split-dominated -> usable only "
                  "with split as a BINNED archive axis; a Gate-3 descriptor revisit.)")


if __name__ == "__main__":
    main()
