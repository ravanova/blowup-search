#!/usr/bin/env python3
"""Leg 412, unit `V-W7` -- THE WAVE-7 VERIFIER'S OWN EVIDENCE SCRIPT.

    .venv/bin/python experiments/p2_verify_wave7_v1_evidence.py            # verify
    .venv/bin/python experiments/p2_verify_wave7_v1_evidence.py --build    # (re)write artefact

Exits 0 iff every check passes.  This script exists because `CORRECTIONS.md` SS45
measured that 32 of 49 evidence scripts in this repository cannot detect an error shared
between an artefact and its own checker.  EVERY CHECK BELOW CARRIES ITS CLASS:

    [P]  recompute-from-primary   -- re-derived from raw data, from a file this unit did
                                     not write, or from `git` history.  Certifies the CLAIM.
    [A]  re-read-own-artefact     -- re-read from, or recomputed inside, `V-W7`'s own
                                     artefact.  Certifies INTERNAL CONSISTENCY only.

The pass line prints the SPLIT, never a bare `N/N`.

MEASUREMENT CONDITIONS, stated before any number (they are not decoration):

  * Three sibling units and a concurrent Conductor session share this working tree.
    `reports/ORCH_STATE.md` was measured at 94,696 B and 96,295 B in one session.  Every
    byte count is therefore taken at a NAMED REVISION via `git show <rev>:<path>`, never
    from the working tree.  A working-tree byte count is not a measurement here.
  * Load average was 23.21 on 12 cores during this leg.  `R-prof`'s banked
    `MACHINE_WAS_NOT_QUIET` applies with more force here than it did there.  No absolute
    timing is checked; only ratios and exact values.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "writeup" / "data" / "p2_verify_wave7_v1.json"

FAILS: list[str] = []
CLASS: dict[str, str] = {}
N = 0


def check(tag, cls, ok, msg):
    global N
    N += 1
    CLASS[tag] = cls
    if not ok:
        FAILS.append(tag)
    print(f"  {'PASS' if ok else 'FAIL'}  [{cls}] {tag:<8} {msg}")


def at(rev: str, path: str) -> bytes:
    """[P] the file as `git` holds it at `rev` -- immune to sibling writes."""
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{path}"],
                       capture_output=True)
    if r.returncode:
        raise SystemExit(f"git show {rev}:{path} failed: {r.stderr.decode()[:200]}")
    return r.stdout


def live_block(txt: bytes) -> bytes:
    """The ORCH_STATE LIVE block: `## LIVE` to the first `## Superseded`, SS3j's unit."""
    lines = txt.split(b"\n")
    st = None
    for i, l in enumerate(lines):
        if st is None and l.startswith(b"## LIVE"):
            st = i
        elif st is not None and l.startswith(b"## Superseded"):
            return b"\n".join(lines[st:i])
    return b"\n".join(lines[st:]) if st is not None else b""


def pearson_log(traj, lo, hi):
    """[P] Pearson r of log(scale_invariant_grad) against k over [lo, hi]."""
    import math
    w = [q for q in traj if lo <= q[0] <= hi and q[4] > 0]
    xs = [q[0] for q in w]
    ys = [math.log(q[4]) for q in w]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    return num / den


def residual_at(traj, k):
    """[P] the residual at the last recorded iterate with index <= k."""
    return [r for r in traj if r[0] <= k][-1][2]


def compute():
    """Every V-W7 number, recomputed from primaries.  Nothing is typed in."""
    l6 = json.loads((ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json").read_text())
    l6b = json.loads((ROOT / "writeup" / "data" / "p2_route_l6b_v1.json").read_text())
    B = l6["gate"]["B"]
    pr = B["per_rung_residual"]
    new = l6b["gate"]["smallest_residual_at_20000"]

    # --- the under-claim: 25x budget at FIXED n_dof against the WHOLE refinement ladder
    budget_move = (new - pr["J4"]) / pr["J4"]
    ladder_move = (pr["J4"] - pr["J1"]) / pr["J1"]
    j3_needed = (pr["J3"] - new) / pr["J3"]

    # --- SS46 recomputed: the SAME seeds at two budgets, seed/continuation ratio
    cont = l6b["starts"]["banked_J4_minimiser"]["trajectory_k_sec_J_ginf_gscaled"]
    ratios = {}
    for name in ("seed406", "seed407"):
        t = l6b["starts"][name]["trajectory_k_sec_J_ginf_gscaled"]
        ratios[name] = {
            "J_at_800": residual_at(t, 800),
            "J_at_20000": t[-1][2],
            "ratio_at_800": residual_at(t, 800) / residual_at(cont, 800),
            "ratio_at_20000": t[-1][2] / cont[-1][2],
        }
    # SS46's own supporting sentence: L6's five branch-B seeds at the 800 cap
    l6_seed_ratios = sorted(
        s["scale_invariant_grad"] for s in [] )  # (not the quantity; see below)
    l6_b_seed_J = sorted(
        r["residual_load_bearing"] / pr["J4"]
        for r in l6.get("start_records", [])
        if r.get("branch") == "B" and r.get("n_dof") == 6720
        and str(r.get("start", "")).startswith("seed"))

    # --- SS46b recomputed: the two windows of the correlation
    corr = {}
    for name in l6b["starts"]:
        t = l6b["starts"][name]["trajectory_k_sec_J_ginf_gscaled"]
        K = t[-1][0]
        corr[name] = {
            "trailing_3000": pearson_log(t, K - 3000, K),
            "mid_run_4700_7700": pearson_log(t, 4700, 7700),
        }

    # --- SS3j headroom, at the revision the table was committed at
    hr = {}
    for rev in ("c6287a2", "HEAD"):
        row = {f: len(at(rev, f)) for f in ("STATE.md", "WALLS.md", "OPTIONS.md")}
        row["ORCH_STATE_LIVE"] = len(live_block(at(rev, "reports/ORCH_STATE.md")))
        hr[rev] = row
    longest = max(len(l) for l in at("c6287a2", "STATE.md").decode().split("\n"))

    # --- the cap sweep: L6's refinement rate as a function of the truncation
    sweep = {k: v["rate_dlogresid_dlogndof_last3"]
             for k, v in B["stability_against_the_iteration_cap"]["by_cap"].items()}

    return {
        "l6b_gate": {
            "smallest_residual_at_20000": new,
            "L6_residual": pr["J4"],
            "materially_below_1_6138": l6b["gate"]["materially_below_1_6138"],
            "material_threshold": l6b["gate"]["material_threshold"],
            "UNDER_RESOURCED": l6b["cost_and_shortfall"]["UNDER_RESOURCED"],
        },
        "the_under_claim_absent_from_the_landing_record": {
            "what": ("25x the budget at a FIXED truncation moved the residual 1.35x as far "
                     "as L6's ENTIRE four-rung refinement ladder did"),
            "budget_move_at_J4_rel": budget_move,
            "refinement_ladder_J1_to_J4_rel": ladder_move,
            "ratio": abs(budget_move / ladder_move),
            "J3_at_800": pr["J3"],
            "J3_fall_needed_to_invert_the_ladder_rel": j3_needed,
            "measured_one_rung_up_at_25x_budget_rel": abs(budget_move),
            "margin_percentage_points": 100 * (j3_needed - abs(budget_move)),
            "L6_cap_sweep_rate_last3_by_cap": sweep,
            "why_the_cap_sweep_does_not_answer_it": (
                "V-W6/SS38 ruled L6's cap sweep post-hoc truncation of the SAME 800-iteration "
                "runs, so it controls nothing about budgets ABOVE 800; and read as a trend it "
                "points the wrong way -- the rate shrinks monotonically as the cap rises."),
        },
        "SS46_recomputed": ratios,
        "SS46b_recomputed": corr,
        "SS3j_headroom_measured_by_V_W7": hr,
        "longest_STATE_row_chars_at_c6287a2": longest,
    }


def main(argv):
    d = compute()

    if "--build" in argv:
        import hashlib
        doc = {"unit": "V-W7", "leg": 412, "wave": 8, "lane": "V",
               "verifies": "wave 7 (R-bank leg 404, R-prof leg 405, L6-b leg 406) AND the "
                           "Conductor's seventeen wave-7 integration commits",
               "measured": d}
        doc["self_hash"] = hashlib.sha256(
            json.dumps(doc, indent=2, sort_keys=True, default=float).encode()
        ).hexdigest()[:16]
        ART.write_text(json.dumps(doc, indent=2, sort_keys=True, default=float) + "\n")
        print(f"wrote {ART}  self_hash {doc['self_hash']}")
        return 0

    if not ART.exists():
        print(f"no artefact at {ART}; run with --build", file=sys.stderr)
        return 2
    a = json.loads(ART.read_text())
    m = a["measured"]

    print("\n-- [A] the artefact is internally consistent --")
    import hashlib
    stripped = {k: v for k, v in a.items() if k != "self_hash"}
    h = hashlib.sha256(json.dumps(
        stripped, indent=2, sort_keys=True, default=float).encode()).hexdigest()[:16]
    check("V01", "A", h == a["self_hash"],
          f"V-W7 artefact self_hash recomputes to {h}")

    print("\n-- [P] L6-b's gate, re-derived from the two primaries --")
    g = m["l6b_gate"]
    check("V02", "P", abs(g["smallest_residual_at_20000"]
                          - d["l6b_gate"]["smallest_residual_at_20000"]) == 0.0
          and g["smallest_residual_at_20000"] > g["material_threshold"],
          f"smallest residual at 20,000 = {g['smallest_residual_at_20000']!r} "
          f"> {g['material_threshold']} -- the gate answers NO")
    check("V03", "P", g["materially_below_1_6138"] == "NO"
          and g["UNDER_RESOURCED"] is False,
          "a real NO, not an under-resourced null (SS3d): the pre-registered 20,000 ran in full")

    print("\n-- [P] THE UNDER-CLAIM: budget move against the whole refinement ladder --")
    u = m["the_under_claim_absent_from_the_landing_record"]
    r = d["the_under_claim_absent_from_the_landing_record"]
    check("V04", "P", abs(u["budget_move_at_J4_rel"] - r["budget_move_at_J4_rel"]) < 1e-15
          and abs(u["refinement_ladder_J1_to_J4_rel"]
                  - r["refinement_ladder_J1_to_J4_rel"]) < 1e-15,
          f"budget {100*r['budget_move_at_J4_rel']:.6f}% vs whole ladder "
          f"{100*r['refinement_ladder_J1_to_J4_rel']:.6f}%")
    check("V05", "P", abs(r["ratio"] - 1.3518) < 5e-4 and r["ratio"] > 1.0,
          f"25x budget at FIXED n_dof moved the residual x{r['ratio']:.4f} of the ENTIRE "
          f"four-rung refinement ladder")
    check("V06", "P", 0.0 < r["margin_percentage_points"] < 1.0,
          f"J3 needs {100*r['J3_fall_needed_to_invert_the_ladder_rel']:.4f}% to invert the "
          f"ladder; {100*r['measured_one_rung_up_at_25x_budget_rel']:.4f}% was measured one "
          f"rung up -- margin {r['margin_percentage_points']:.4f} percentage points")
    sw = r["L6_cap_sweep_rate_last3_by_cap"]
    order = [sw[k] for k in sorted(sw, key=int)]
    check("V07", "P", all(a_ < b_ for a_, b_ in zip(order, order[1:])),
          "L6's refinement rate shrinks MONOTONICALLY as its truncation rises 50 -> 800: "
          + " -> ".join(f"{v:.5f}" for v in order))

    print("\n-- [P] SS46: the SAME seeds at two budgets --")
    s = d["SS46_recomputed"]
    check("V08", "P",
          abs(s["seed406"]["ratio_at_800"] - 17.8098) < 1e-3
          and abs(s["seed407"]["ratio_at_800"] - 22.0724) < 1e-3
          and abs(s["seed406"]["ratio_at_20000"] - 4.29257) < 1e-4
          and abs(s["seed407"]["ratio_at_20000"] - 4.32093) < 1e-4,
          "seed/continuation ratio 17.81-22.07x at k=800 falls to 4.29-4.32x at k=20,000 "
          "on nothing but budget -- SS46's withdrawal is RIGHT")
    check("V09", "P", s["seed406"]["ratio_at_20000"] > 3.93,
          f"SS46 IS TOO BROAD AT THE LOW END: the 20,000-iteration ratios "
          f"({s['seed406']['ratio_at_20000']:.4f}, {s['seed407']['ratio_at_20000']:.4f}) sit "
          f"ABOVE the 3.93x floor SS46 withdraws; only the UPPER end is shown cap-dependent")
    check("V10", "P", s["seed406"]["J_at_800"] < 29.566940188487212,
          f"SS46's SUPPORT SENTENCE IS FALSE: seed406 reads {s['seed406']['J_at_800']!r} at "
          f"k=800, BELOW the '29.57-38.20' range it is said to sit inside")

    print("\n-- [P] SS46b: both windows of the correlation, recomputed --")
    c = d["SS46b_recomputed"]
    check("V11", "P",
          abs(c["seed406"]["trailing_3000"] + 0.2264) < 1e-3
          and abs(c["seed407"]["trailing_3000"] + 0.3509) < 1e-3,
          f"trailing-3,000 r = {c['seed406']['trailing_3000']:.6f} / "
          f"{c['seed407']['trailing_3000']:.6f} -- SS46b's -0.23/-0.35 are EXACT, so the old "
          f"C41's `all(r > 0.5)` really did fail on a TRUE artefact")
    check("V12", "P",
          c["seed406"]["mid_run_4700_7700"] > 0.5 and c["seed407"]["mid_run_4700_7700"] > 0.5
          and abs(c["seed406"]["mid_run_4700_7700"] - 0.7564) < 1e-3
          and abs(c["seed407"]["mid_run_4700_7700"] - 0.8222) < 1e-3,
          f"mid-run k=4,700-7,700 r = {c['seed406']['mid_run_4700_7700']:.4f} / "
          f"{c['seed407']['mid_run_4700_7700']:.4f} -- SS46b's +0.76/+0.82 are EXACT; the "
          f"finding is real and WINDOW-SCOPED, and it reverses")

    print("\n-- [P] SS3j headroom, measured at the revision the table was committed at --")
    hr = d["SS3j_headroom_measured_by_V_W7"]["c6287a2"]
    check("V13", "P", hr["STATE.md"] == 24016 and hr["ORCH_STATE_LIVE"] == 7401,
          f"at c6287a2 the committed table claims STATE.md 23,639 (free 937) and LIVE 7,247 "
          f"(free 945); MEASURED at that same revision: {hr['STATE.md']:,} (free "
          f"{24576-hr['STATE.md']}) and {hr['ORCH_STATE_LIVE']:,} (free "
          f"{8192-hr['ORCH_STATE_LIVE']}) -- headroom OVERSTATED on both")
    check("V14", "P", hr["WALLS.md"] == 32526 and hr["OPTIONS.md"] == 23971,
          f"the other two rows are CORRECT at that revision: WALLS.md {hr['WALLS.md']:,}, "
          f"OPTIONS.md {hr['OPTIONS.md']:,} -- a PARTIAL refresh, the hardest kind to see")
    hd = d["SS3j_headroom_measured_by_V_W7"]["HEAD"]
    check("V15", "P", hd["ORCH_STATE_LIVE"] == 8080,
          f"the Conductor's correction is committed and CORRECT: HEAD claims LIVE 8,080 and "
          f"I measure {hd['ORCH_STATE_LIVE']:,} -- {8192-hd['ORCH_STATE_LIVE']} bytes, "
          f"{100*(8192-hd['ORCH_STATE_LIVE'])/8192:.1f}%, of headroom left")
    check("V16", "P", all(hd[f] <= cap for f, cap in
                          (("STATE.md", 24576), ("WALLS.md", 32768), ("OPTIONS.md", 24576)))
          and hd["ORCH_STATE_LIVE"] <= 8192,
          f"every SS3j surface is INSIDE its cap at HEAD "
          f"(STATE {hd['STATE.md']:,} / WALLS {hd['WALLS.md']:,} / "
          f"OPTIONS {hd['OPTIONS.md']:,} / LIVE {hd['ORCH_STATE_LIVE']:,})")
    check("V17", "P", d["longest_STATE_row_chars_at_c6287a2"] <= 600,
          f"longest STATE.md row at c6287a2 is "
          f"{d['longest_STATE_row_chars_at_c6287a2']} characters, inside the 600 limit")

    print("\n-- [P] the withdrawn readings are gone from the live record, except one --")
    opts = at("HEAD", "OPTIONS.md").decode()
    l6row = [l for l in opts.split("\n") if l.startswith("| **L6** |")]
    check("V18", "P", bool(l6row) and "23.67" in l6row[0] and "§46" not in l6row[0],
          "DEFECT: OPTIONS.md's L6 row still presents the WITHDRAWN 3.93-23.67x as a standing "
          "V-W6/SS38 correction with NO SS46 marker, on a capped live surface")
    for path in ("STATE.md", "WALLS.md"):
        txt = at("HEAD", path).decode()
        check(f"V19_{path}", "P", "§46" in txt,
              f"{path} DOES carry the SS46 withdrawal")

    print("\n-- [P] territory, derived from git rather than from any unit's claims --")
    for rev, sub in (("8019c35", "R-bank"), ("1f89ceb", "R-prof"), ("4df0ca0", "L6-b")):
        out = subprocess.run(["git", "-C", str(ROOT), "show", "--stat",
                              "--format=", "--name-status", rev],
                             capture_output=True).stdout.decode()
        rows = [l for l in out.split("\n") if l.strip()]
        check(f"V20_{sub}", "P", bool(rows) and not any(l.startswith("D") for l in rows),
              f"{sub} landing {rev}: {len(rows)} paths, "
              f"{sum(l.startswith('A') for l in rows)} added, "
              f"{sum(l.startswith('M') for l in rows)} modified, 0 deleted")
    for rev in ("04f9ff5", "6ca49a6"):
        out = subprocess.run(["git", "-C", str(ROOT), "show", "--format=%s",
                              "--name-only", rev], capture_output=True).stdout.decode()
        subj = out.split("\n")[0]
        swept = [l for l in out.split("\n") if "l6b_ckpt" in l]
        check(f"V21_{rev}", "P", bool(swept) and "l6b" not in subj.lower(),
              f"CONDUCTOR TERRITORY CROSSING: {rev} sweeps {len(swept)} of L6-b's LIVE "
              f"in-run checkpoints under a subject that does not name them "
              f"({subj[:56]!r})")

    npass = N - len(FAILS)
    prim = sum(1 for t, c in CLASS.items() if c == "P")
    prim_pass = sum(1 for t, c in CLASS.items() if c == "P" and t not in FAILS)
    print(f"\n{npass}/{N} checks passed"
          + (f"; FAILED: {FAILS}" if FAILS else ""))
    print(f"CLASS SPLIT (SS45): {prim_pass}/{prim} recompute-from-primary, "
          f"{npass-prim_pass}/{N-prim} re-read-own-artefact.  "
          f"The [A] checks certify internal consistency and nothing more.")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
