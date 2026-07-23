"""Pre-committed acceptance for the Phase 1 fitness-axis discrimination screen.

Frozen BEFORE the run (phase1_axis_screen.py header). Reads
experiments/phase1_axis_screen.jsonl and decides, per candidate axis, whether it
survives the routing screen on the labeled ground-truth pair.

The labeled truth: smooth_sharp BLOWS UP (amp > 100), smooth_mild SATURATES
(amp ~ 5), euler_control does NOT grow. So a propensity-tracking axis must order

        smooth_sharp  >  smooth_mild  >  euler_control

An axis PASSES the screen iff BOTH:

  (A) DIRECTION -- at BOTH N=256 and N=512 the axis orders
      sharp > mild > control, with a real separation between the two growers:
          sep = (v_sharp - v_mild) / max(|v_sharp|, |v_mild|, EPS) >= SEP_FLOOR
      (right SIGN and a >= SEP_FLOOR relative gap, not just noise).

  (B) RESOLUTION-STABLE -- the value does not swing more across N than the very
      signal it must resolve:
          max_ic |v(512) - v(256)|  <=  STAB_FRAC * |v_sharp - v_mild|(@512)
      (drift small vs the sharp-mild gap it has to rank; the Stage-1.5 rule
      shape, loosened to a screen tolerance because this is a screen not a gate).

This is deliberately a NECESSARY condition. The survivor still faces the full
six-property Gate 4 over 40 shapes. g_baseline is EXPECTED to fail (A) with the
wrong sign (mild > sharp) -- reproducing the spike is the screen's own sanity
check.

Usage: .venv/bin/python analyze_phase1_axis_screen.py [path.jsonl]
"""

import json
import sys
from collections import defaultdict

# --- pre-committed thresholds (frozen with phase1_axis_screen.py) ---
SEP_FLOOR = 0.10    # required relative gap between the two growers (right sign)
STAB_FRAC = 0.50    # max cross-N drift as a fraction of the sharp-mild gap
EPS = 1e-9
AXES = ("nu_crit", "persistence", "g_baseline")
NEEDED = ("smooth_sharp", "smooth_mild", "euler_control")


def load(path):
    by = defaultdict(dict)  # (ic_label) -> {N: row}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("sweep") != "phase1_axis_screen":
                continue
            by[row["ic_label"]][row["resolution_N"]] = row
    return by


def val(row, axis):
    v = row.get(axis)
    return None if v is None else float(v)


def evaluate_axis(by, axis):
    """Return (pass, detail-dict) for one candidate axis."""
    Ns = sorted({n for ic in NEEDED for n in by.get(ic, {})})
    detail = {"per_N": {}, "reasons": []}

    # (A) direction at each N
    direction_ok = bool(Ns)
    for N in Ns:
        vs = {ic: val(by.get(ic, {}).get(N, {}), axis) for ic in NEEDED}
        if any(vs[ic] is None for ic in NEEDED):
            direction_ok = False
            detail["reasons"].append(f"N={N}: missing value(s) {vs}")
            detail["per_N"][N] = {"vals": vs, "ordered": None, "sep": None}
            continue
        ordered = vs["smooth_sharp"] > vs["smooth_mild"] > vs["euler_control"]
        denom = max(abs(vs["smooth_sharp"]), abs(vs["smooth_mild"]), EPS)
        sep = (vs["smooth_sharp"] - vs["smooth_mild"]) / denom
        ok = ordered and sep >= SEP_FLOOR
        direction_ok = direction_ok and ok
        detail["per_N"][N] = {"vals": vs, "ordered": ordered, "sep": sep, "ok": ok}
        if not ok:
            detail["reasons"].append(
                f"N={N}: ordered={ordered} sep={sep:+.3f} (need sign + >={SEP_FLOOR})")

    # (B) resolution stability across the two finest N (need >= 2 N)
    stable = None
    if len(Ns) >= 2:
        Nlo, Nhi = Ns[-2], Ns[-1]
        gap = None
        vs_hi = {ic: val(by.get(ic, {}).get(Nhi, {}), axis) for ic in NEEDED}
        if vs_hi["smooth_sharp"] is not None and vs_hi["smooth_mild"] is not None:
            gap = abs(vs_hi["smooth_sharp"] - vs_hi["smooth_mild"])
        max_drift = 0.0
        drift_by_ic = {}
        ok_pair = gap is not None and gap > EPS
        for ic in NEEDED:
            a = val(by.get(ic, {}).get(Nlo, {}), axis)
            b = val(by.get(ic, {}).get(Nhi, {}), axis)
            if a is None or b is None:
                ok_pair = False
                drift_by_ic[ic] = None
                continue
            d = abs(b - a)
            drift_by_ic[ic] = d
            max_drift = max(max_drift, d)
        if ok_pair:
            stable = max_drift <= STAB_FRAC * gap
            detail["stability"] = {"N_lo": Nlo, "N_hi": Nhi, "gap": gap,
                                   "max_drift": max_drift, "drift_by_ic": drift_by_ic,
                                   "threshold": STAB_FRAC * gap}
            if not stable:
                detail["reasons"].append(
                    f"cross-N drift {max_drift:.4f} > {STAB_FRAC}*gap "
                    f"{STAB_FRAC * gap:.4f}")
        else:
            stable = False
            detail["reasons"].append("stability: missing values or zero gap")
    else:
        detail["reasons"].append("only one N -- cannot assess resolution stability")

    passed = bool(direction_ok and stable)
    detail["direction_ok"] = direction_ok
    detail["stable"] = stable
    return passed, detail


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "experiments/phase1_axis_screen.jsonl"
    by = load(path)

    print(f"=== PHASE 1 AXIS SCREEN ({path}) ===\n")
    Ns = sorted({n for ic in by for n in by[ic]})
    print(f"ICs seen: {sorted(by)}   N: {Ns}\n")

    # raw table
    hdr = f"{'axis':12s} {'N':>5s} " + " ".join(f"{ic:>14s}" for ic in NEEDED)
    print(hdr)
    print("-" * len(hdr))
    for axis in AXES:
        for N in Ns:
            cells = []
            for ic in NEEDED:
                v = val(by.get(ic, {}).get(N, {}), axis)
                cells.append("        --    " if v is None else f"{v:14.4f}")
            print(f"{axis:12s} {N:5d} " + " ".join(cells))
        print()

    results = {}
    for axis in AXES:
        passed, detail = evaluate_axis(by, axis)
        results[axis] = (passed, detail)

    print("=== VERDICT (pre-committed: direction sharp>mild>control @ both N, "
          f"sep>={SEP_FLOOR}; drift<={STAB_FRAC}*gap) ===\n")
    survivors = []
    for axis in AXES:
        passed, detail = results[axis]
        tag = "PASS" if passed else "FAIL"
        print(f"[{tag}] {axis:12s}  direction_ok={detail['direction_ok']} "
              f"stable={detail['stable']}")
        for r in detail["reasons"]:
            print(f"         - {r}")
        if passed:
            survivors.append(axis)
    print()

    g_passed = results["g_baseline"][0]
    if g_passed:
        print("!! SANITY WARNING: g_baseline PASSED the direction test. The spike "
              "found mild>sharp on g; a pass here means the screen does NOT "
              "reproduce the spike -- investigate before trusting any verdict.")
    else:
        print("sanity ok: g_baseline fails the direction test (reproduces the "
              "spike's mild>sharp), so the screen's discriminator is trustworthy.")
    print()

    if not survivors:
        print("ROUTING VERDICT: NO axis survives. This is a FINDING, not a "
              "push-harder signal -- no resolution-stable, propensity-ordered "
              "fitness on the labeled pair. STOP and re-plan (persistence variant, "
              "different window, or reconsider the deliverable) before Gate 3.")
    else:
        pref = "nu_crit" if "nu_crit" in survivors else survivors[0]
        print(f"ROUTING VERDICT: survivor(s) {survivors}. Build full six-property "
              f"Gate 4 around >>> {pref} <<< over 40 shapes. Passing this screen is "
              f"NECESSARY, not sufficient -- Gate 4 still decides viability.")


if __name__ == "__main__":
    main()
