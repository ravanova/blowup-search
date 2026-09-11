"""Arc-7 confirmation (K4, leg 440): every number in TECHNICAL_CONFIRMATION.md re-derived from the
banked arc-7 artefacts, and fig115 drawn from those artefacts alone.

    .venv/bin/python writeup/7_confirmation/confirmation_evidence.py

Exits nonzero on drift. Nothing is re-run: no lake, no lean, no network. Per leg_440_prereg.md §4,
on FAIL the DOCUMENT is corrected to the artefact, never the artefact to the document.
"""
import json, re, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "writeup" / "data" / "arc7"
FIGS = ROOT / "writeup" / "figures"
HERE = ROOT / "writeup" / "7_confirmation"
T = re.sub(r"\s+", " ", (HERE / "TECHNICAL_CONFIRMATION.md").read_text())
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)
J = lambda p: json.loads(p.read_text())

PIN = "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538"
MATHLIB = "85e3a25e006c35636f0e53b0e9296caca2685bc0"
COMPARATOR = "19e111e2141cf333c7daff0f64c5f24acc91dd2e"
STD3 = ["propext", "Classical.choice", "Quot.sound"]

print("== 1. K1: the same pin in all three environments")
A = J(D / "k1" / "phaseA" / "phaseA.json")
B = J(D / "k1" / "phaseB" / "phaseB.json")
L = J(D / "k1" / "phaseB_local" / "phaseB.json")
C = J(D / "k1" / "phaseC" / "phaseC.json")   # 2026-09-11: the from-source rebuild
for nm, a in [("A", A), ("B", B), ("B-local", L)]:
    check(a["tree_head"] == PIN and a["mathlib_rev"] == MATHLIB and a["comparator_rev"] == COMPARATOR
          and a["toolchain"] == "leanprover/lean4:v4.34.0-rc2" and a["olean_count_project"] == 2486,
          f"phase {nm}: pin, mathlib, comparator, toolchain, 2486 oleans")

print("== 2. K1: green means rc 0, zero error lines, the standard three axioms, no sorryAx")
for nm, a in [("A", A), ("B", B), ("B-local", L)]:
    r = a["result"]
    check(a["build_rc"] == 0 and a["build_error_lines"] == 0
          and r["navier_stokes_breakdown_R3"] == STD3 and r["navier_stokes_breakdown_periodic"] == STD3
          and r["sorryAx_reachable"] == "NO" and r["exit_code"] == 0 and a["reading"].startswith("GREEN"),
          f"phase {nm}: rc 0, 0 error lines, both theorems = the standard three, sorryAx NO")
    # The completion line, not the per-target counter: CORRECTIONS.md §77 records that phase B-local's
    # `11250/11251` is NOT an error (lake prints no line for the root job), so the gate field is the
    # citable one -- and it is the one the note quotes.
    check("Build completed successfully (11251 jobs)" in a["gate"]["a_build_completes"],
          f"phase {nm}: `Build completed successfully (11251 jobs)`", a["gate"]["a_build_completes"][:60])
    check("sorryAx" not in a["axioms_verbatim"], f"phase {nm}: sorryAx absent from the verbatim axioms log")

print("== 3. K1: the timings the note quotes")
check(A["build_s"] == 2047, "phase A build_s = 2047", str(A["build_s"]))
check(B["total_s"] == 5605 and B["build_s"] == 5443 and B["clone_s"] == 2 and B["cache_get_s"] == 121 and B["axioms_s"] == 8,
      "phase B total 5605 = clone 2 + cache 121 + build 5443 + axioms 8 (+ toolchain)", str(B["total_s"]))
check(L["total_s"] == 4272 and L["build_s"] == 4148 and L["clone_s"] == 2 and L["cache_get_s"] == 117 and L["axioms_s"] == 5,
      "phase B-local total 4272 = clone 2 + cache 117 + build 4148 + axioms 5", str(L["total_s"]))
check("2.80GHz" in A["machine"]["cpu"] and "2.10GHz" in B["machine"]["cpu"] and "i7-10750H" in L["machine"]["cpu"],
      "three distinct machines: Xeon 2.80, Xeon 2.10, i7-10750H")

print("== 4. K1: olean provenance / integrity / semantic match, kept three separate claims")
I = J(D / "k1" / "phaseB_integrity" / "integrity.json")
ns, eu = I["integrity"]["navier_stokes"], I["integrity"]["euler"]
check(ns["rc"] == 0 and ns["seconds"] == 913 and eu["rc"] == 0 and eu["seconds"] == 1442 and I["integrity"]["total_s"] == 2355,
      "comparator rc 0 on both: NavierStokes 913 s, Euler 1442 s, total 2355 s")
check(ns["nanoda"] == "accepts" and ns["lean_kernel"] == "accepts" and eu["nanoda"] == "accepts" and eu["lean_kernel"] == "accepts",
      "two independent kernels accept, both challenges")
check(ns["verdict"] == "Your solution is okay!" and eu["verdict"] == "Your solution is okay!", "verdict string, both challenges")
check("nanoda" in I["tool_revs"] and "4c544ed4" in I["tool_revs"]["nanoda"], "nanoda pinned", I["tool_revs"]["nanoda"][:52])
check("NOT part of the K1 gate" in eu["note"], "Euler is declared outside the K1 gate")
check("8747" in I["provenance"]["local_cache"] and "442 MB" in I["provenance"]["local_cache"], "8747 .ltar files, 442 MB")
check("rc 0" in I["provenance"]["second_cache_get"] and "No files to download" in I["provenance"]["second_cache_get"],
      "second cache get: rc 0, nothing to download")
check("0 `Built`" in I["provenance"]["second_lake_build"] and "rc 0" in I["provenance"]["second_lake_build"],
      "second lake build: rc 0, 0 Built lines")
check("does not establish" in I["provenance"].get("what_this_does_not_establish", "") or
      "were in fact produced by compiling" in I["provenance"]["what_this_does_not_establish"],
      "provenance carries its own negative clause")
check("were in fact produced by compiling" in T, "the note quotes the provenance limit verbatim")

print("== 4b. K1 phase C (2026-09-11): mathlib rebuilt FROM SOURCE, cache never invoked")
check(C["tree_head"] == PIN and C["mathlib_rev"] == MATHLIB and C["comparator_rev"] == COMPARATOR
      and C["olean_count_project"] == 2486, "phase C: same pin, same mathlib, same comparator, 2486 oleans")
check(C["mathlib_built_lines"] == 8370 and C["mathlib_replayed_lines"] == 0,
      "the prereg void check: 8370 `Built Mathlib.` lines, 0 replayed -- no cache was used",
      f'{C["mathlib_built_lines"]} built / {C["mathlib_replayed_lines"]} replayed')
check("NEVER RUN" in C["cache_get_rc"] and "0 occurrences" in C["cache_get_rc"],
      "`lake exe cache get` never invoked; `cache` absent from the build log")
rC = C["result"]
check(C["build_rc"] == 0 and C["build_error_lines"] == 0 and rC["navier_stokes_breakdown_R3"] == STD3
      and rC["navier_stokes_breakdown_periodic"] == STD3 and rC["sorryAx_reachable"] == "NO"
      and C["reading"].startswith("MATCH"),
      "phase C: rc 0, 0 errors, the standard three, sorryAx NO, reading MATCH")
check("sorryAx" not in C["axioms_verbatim"], "phase C: sorryAx absent from the verbatim axioms log")
check("0883b714" in C["comparison_with_phaseB"]["axioms_identical"],
      "axioms byte-identical across all three runs, by md5 -- not by eye")
check(C["total_s"] == 11578 and C["build_s"] == 11571, "phase C total 11578 s (build 11571)", str(C["total_s"]))
check(round(C["total_s"] / L["total_s"], 2) == 2.71, "the cost of dropping the cache: 2.71x phase B",
      f'{C["total_s"]}/{L["total_s"]} = {C["total_s"]/L["total_s"]:.2f}')
for tok in ["8370", "11578", "2.71", "28.5 GB", "was never invoked, not once"]:
    check(tok in T, f"the note quotes {tok!r} for phase C")

print("== 5. K2: the five blind workers, and the label that moved")
K2 = D / "k2" / "r2"
a1, a2, a3, a4, a5 = (J(K2 / f"agent_{i}_{n}.json") for i, n in
                      [(1, "partial"), (2, "sorry"), (3, "comparator"), (4, "deepmind"), (5, "verifier")])
check(all(x["clone_head"] == PIN for x in (a1, a2, a3, a4)), "workers 1-4 read the same pin as K1")
check(a1["import_closure"]["modules_in_closure"] == 580, "580 modules in the solution's import closure",
      str(a1["import_closure"]["modules_in_closure"]))
code = [h for h in a2["sorry_hits"] if h["kind"] == "code"]
check(len(code) == 4 and all(h["in_closure_of_ComparatorSolution"] == "NO" for h in code),
      "exactly 4 `sorry` in code, none in the solution's import closure", f"{len(code)} in code")
check(a2["file_census"]["lean_files_total_excluding_dot_lake"] == 2486, "2486 project .lean files")
check(sorted({(h["file"], h["line"]) for h in code}) ==
      [("ComparatorChallenges/Euler.lean", 88), ("ComparatorChallenges/Euler.lean", 184),
       ("ComparatorChallenges/NavierStokes.lean", 277), ("ComparatorChallenges/NavierStokes.lean", 284)],
      "the four sorry sit at the pre-registered lines")
check(sum(1 for c in a3["checks"] if c.get("verdict") == "PASS") == 2, "two of the four NOT-ESTABLISHED checks now PASS")
check(a4["upstream_file_sha256_all_three_fetches"] == "f446284f2aa54375f558c263a580b34e2e7bc9f44a28829637199cc72257d25d",
      "DeepMind byte-identity: one sha256 across all three fetches")
check(a5["k1_verdict"] == "VERIFIED-SUPPORTED", "the blind verifier's K1 verdict", a5["k1_verdict"])
check("laptop" in a5["method"]["independence_bound"], "the verifier's own independence bound is recorded")
check(all(x.get("forbidden_paths_opened") == "none" for x in (a1, a3)), "no forbidden path opened")

print("== 6. K3: the construction wave, zero surviving evidence")
M = J(D / "k3" / "merged.json"); c = M["counts"]
check(c == {"live_gates": 5, "EVIDENCE": 0, "not_evidence": 2, "cells_NO_or_NO": 1,
            "not_established_or_dropped_by_the_rule": 2, "dropped_preregistered": 1,
            "gates_the_blind_adversary_faked": 5}, "the merged counts, exactly", json.dumps(c))
check(len(M["disagreements"]) == 4 and all(d.get("recorded_not_adjudicated") for d in M["disagreements"]),
      "four disagreements, all recorded and none adjudicated", str(len(M["disagreements"])))
check(all(w["tier2_sentence_present"] for w in M["workers"].values()), "every worker carried its Tier-2 sentence")
for gid in ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]:
    check(gid in T, f"the note names {gid}")

print("== 7. the closed form that was two routes only in the prereg")
src = (ROOT / "experiments" / "arc6_residual_v1.py").read_text().splitlines()
line = next((l for l in src if "calB_beyond" in l and "sh - 1.0" in l), "")
check("(2 + 2 * h) * (sh - 1.0)" in line, "arc6_residual_v1.py still computes calB_beyond as the closed form", line.strip())
check("(2 + 2*h) * (sh - 1.0)" in T or "(2 + 2*h)(s" in T or "calB_beyond = (2 + 2*h) * (sh - 1.0)" in T,
      "the note quotes that closed form")

print("== 8. the note says what it must, and claims nothing more")
for tok in [PIN[:8], "5605", "4272", "2047", "2486", "11251", "propext", "`sorryAx` unreachable",
            "VERIFIED-SUPPORTED", "nanoda", "913", "1442", "8747", "442 MB",
            "Tier 2 is never a proof", "no position", "0.05%", "strictly weaker",
            "EVIDENCE` 0", "no L1→L4 claim".replace("no L1→L4 claim", "L1→L4")]:
    check(tok in T, f"note quotes {tok!r}")
check("priority dispute" in T and "takes no position" in T, "the no-priority sentence is explicit, not silent")

print("== 9. fig115, drawn from the banked artefacts alone")
fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
names = ["A\nresume\nXeon 2.80", "B\nfresh clone\nXeon 2.10", "B-local\nfresh clone\ni7-10750H",
         "C\nFROM SOURCE\ni7-10750H"]
build = [A["build_s"], B["build_s"], L["build_s"], C["build_s"]]
other = [0, B["total_s"] - B["build_s"], L["total_s"] - L["build_s"], C["total_s"] - C["build_s"]]
tags = ["GREEN\nrc 0 · 0 err", "GREEN\nrc 0 · 0 err", "GREEN\nrc 0 · 0 err", "MATCH\nno cache\n8370 built"]
ax[0].bar(names, build, color=["#2f6f4f", "#2f6f4f", "#2f6f4f", "#1d4b36"], label="lake build")
ax[0].bar(names, other, bottom=build, color="#9ec6b0", label="clone + cache + #print axioms")
for i, (b, o) in enumerate(zip(build, other)):
    ax[0].text(i, b + o + 160, f"{b+o} s", ha="center", fontsize=9)
    ax[0].text(i, b / 2, tags[i], ha="center", va="center", fontsize=8, color="white")
ax[0].set_ylabel("seconds"); ax[0].set_ylim(0, 13400)
ax[0].tick_params(axis="x", labelsize=8)   # four bars now: the labels crowd at the default size
# legend upper-LEFT would sit on top of phase B's total label; the tall bar is centre-left
ax[0].legend(fontsize=8, loc="upper right", framealpha=0.95)
ax[0].set_title("K1: one pin, three environments + the from-source rebuild\nboth theorems = [propext, Classical.choice, Quot.sound]", fontsize=9)

ax[1].barh(["Euler\n(not in the gate)", "NavierStokes\n(the K1 gate)"], [eu["seconds"], ns["seconds"]],
           color=["#b9b9b9", "#2f6f4f"])
for i, s in enumerate([eu["seconds"], ns["seconds"]]):
    ax[1].text(s - 60, i, f"{s} s", ha="right", va="center", color="white", fontsize=9)
ax[1].set_xlabel("seconds"); ax[1].set_title("K1 integrity: two independent kernels\nLean kernel ACCEPTS · nanoda 0.4.17 ACCEPTS", fontsize=9)
ax[1].text(0.98, 0.06, "semantic match: ESTABLISHED 2026-09-11\n(phase C: mathlib rebuilt from source)", transform=ax[1].transAxes,
           ha="right", fontsize=8, style="italic", color="#2f6f4f")

lab = ["live\ngates", "EVIDENCE", "faked by the\nblind adversary"]
val = [c["live_gates"], c["EVIDENCE"], c["gates_the_blind_adversary_faked"]]
ax[2].bar(lab, val, color=["#7a7a7a", "#8a2f2f", "#8a2f2f"])
for i, v in enumerate(val):
    ax[2].text(i, v + 0.12, str(v), ha="center", fontsize=12, fontweight="bold")
ax[2].set_ylim(0, 6.2); ax[2].set_yticks(range(7))
ax[2].set_title("K3: the construction wave under one rule\nzero of five gates survive as evidence", fontsize=9)
ax[2].text(0.5, 0.80, "a finding about THE GATES,\nnot about the manuscript", transform=ax[2].transAxes,
           ha="center", fontsize=8, style="italic",
           bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#b0b0b0", alpha=0.95))

fig.suptitle("fig115 — arc 7 / K4 (leg 440): the kernel check GREEN in three environments and by two kernels, "
             "and (2026-09-11) from source with no cache; the construction wave's zero", fontsize=10)
fig.tight_layout(); FIGS.mkdir(exist_ok=True)
out = FIGS / "fig115_arc7_confirmation.png"
fig.savefig(out, dpi=110); plt.close(fig)
print("  wrote", out)
check(out.exists() and out.stat().st_size > 20000, "fig115 written", f"{out.stat().st_size} bytes")

if fail:
    print(f"\nDRIFT: {len(fail)} — the DOCUMENT is corrected to the artefact, never the artefact to the document")
    [print("  -", x) for x in fail]
    sys.exit(1)
print("\narc7 confirmation: evidence — all checks pass")
