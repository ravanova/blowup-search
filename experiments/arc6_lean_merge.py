"""Arc 6, R6 fan-out (leg 431): merge the five Lean agents' answers.

    .venv/bin/python experiments/arc6_lean_merge.py

Inputs : writeup/data/arc6/lean/agent_{1_build,2_statement,3_census,4_comparator,5_coverage}.json
Output : writeup/data/arc6/lean/merged.json  -- the five gate answers, separately, plus the
         cross-agent facts (the same sorry count from two agents, the same main-theorem names, ...).
Nothing is adjudicated here; (a) "builds" and (b) "proved" are kept in separate fields.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LD = ROOT / "writeup" / "data" / "arc6" / "lean"
OUT = LD / "merged.json"
FILES = {1: "agent_1_build.json", 2: "agent_2_statement.json", 3: "agent_3_census.json", 4: "agent_4_comparator.json", 5: "agent_5_coverage.json"}


def run(write=True, verbose=True):
    A = {k: (json.loads((LD / f).read_text()) if (LD / f).exists() else None) for k, f in FILES.items()}
    out = {"schema": "arc6_lean_merged_v1", "leg": 431, "present": [k for k, v in A.items() if v], "absent": [k for k, v in A.items() if not v], "answers": {}}
    if A[1]:
        b = A[1]["build"]; kc = A[1]["kernel_check"]
        out["answers"]["1_build"] = {"gate_answer": A[1]["gate_answer"], "toolchain": A[1].get("toolchain"), "mathlib_rev": A[1].get("mathlib_rev"),
                                     "cache_get_exit": A[1]["cache_get"].get("exit_code"), "counter_start": b.get("counter_at_start"), "counter_end": b.get("counter_at_end"),
                                     "oleans_before": b.get("oleans_before"), "oleans_after": b.get("oleans_after"), "wall_s": b.get("wall_s"), "modules_per_min": b.get("modules_per_min"),
                                     "projected_remaining_min": b.get("projected_remaining_min"), "project_modules_built": b.get("project_modules_built"),
                                     "kernel_verdict": kc.get("verdict"), "kernel_reason": kc.get("reason")}
    if A[2]:
        out["answers"]["2_statement"] = {"gate_answer": A[2]["verdict"], "main_theorems": [t["name"] for t in A[2]["main_theorems"]],
                                         "diff_vs_theorem_1_1": {c["clause"]: c["status"] for c in A[2]["diff_vs_theorem_1_1"]},
                                         "diff_vs_fefferman_C": {c["clause"]: c["status"] for c in A[2].get("diff_vs_fefferman_C", [])},
                                         "diff_vs_fefferman_D": {c["clause"]: c["status"] for c in A[2].get("diff_vs_fefferman_D", [])},
                                         "could_not_determine": A[2].get("could_not_determine", [])}
    if A[3]:
        out["answers"]["3_census"] = {"gate_answer": A[3]["gate_answer"], "counts": A[3]["counts"], "axiom_declarations": A[3]["axiom_declarations"], "sorry_declarations": A[3]["sorry_declarations"],
                                      "import_closure": {k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if not isinstance(vv, (list, dict))}) for k, v in A[3]["import_closure"].items()},
                                      "scope": A[3]["scope"],
                                      "kernel_level": A[3]["kernel_level"], "mathlib_rev": A[3].get("mathlib_rev")}
    if A[4]:
        out["answers"]["4_comparator"] = {"gate_answer": A[4]["gate_answer"], "checks": [[c["check"], c["result"]] for c in A[4]["checks_performed"]],
                                          "n_pass": sum(1 for c in A[4]["checks_performed"] if c["result"] == "PASS"), "n_not_established": sum(1 for c in A[4]["checks_performed"] if c["result"] == "NOT-ESTABLISHED"),
                                          "n_fail": sum(1 for c in A[4]["checks_performed"] if c["result"] == "FAIL"), "what_it_does_not_establish": A[4]["what_it_does_not_establish"]}
    if A[5]:
        sm = A[5]["summary"]
        inv = A[5]["lean_inventory"]
        out["answers"]["5_coverage"] = {"gate_answer": A[5]["gate_answer"], "summary": sm, "n_map": len(A[5]["map"]), "lean_n_declarations": inv["n_declarations"],
                                        "lean_n_files": inv.get("n_files"), "sorry_count_in_source": inv.get("sorry_count_in_source"), "import_closure_of_main_theorem": inv.get("import_closure_of_main_theorem"),
                                        "per_section": sm.get("per_section"), "partial_ids": sm.get("partial_ids"), "could_not_determine": A[5].get("could_not_determine", []),
                                        "route_differences": A[5].get("route_differences"), "beyond_the_79": A[5].get("beyond_the_79")}
    # cross-agent consistency
    cross = {}
    if A[2] and A[4]:
        cross["main_theorem_names_agree"] = sorted(t["name"].split(".")[-1] for t in A[2]["main_theorems"])
    if A[3] and A[1]:
        cross["mathlib_rev_agree"] = (A[3].get("mathlib_rev") == A[1].get("mathlib_rev"))
    if A[3] and A[4]:
        cross["sorry_only_in_comparator_challenges"] = all("ComparatorChallenges" in d.get("file", d if isinstance(d, str) else "") for d in A[3]["sorry_declarations"]) if A[3]["sorry_declarations"] else None
    if A[3] and A[5]:
        # the two sorry counts are over different scopes: agent 3 scanned the whole clone (2486 files), agent 5 the NavierStokes/ library (644 files)
        cross["sorry_counts_by_scope"] = {"agent_3_whole_clone": A[3]["counts"]["sorry_in_code"], "agent_3_n_files": A[3]["scope"].get("n_lean_files"),
                                          "agent_5_NavierStokes_library": A[5]["lean_inventory"].get("sorry_count_in_source"), "agent_5_n_files": A[5]["lean_inventory"].get("n_files"),
                                          "consistent": (A[3]["counts"]["sorry_in_code"] == len(A[3]["sorry_declarations"]) and all("ComparatorChallenges" in str(d) for d in A[3]["sorry_declarations"]) and A[5]["lean_inventory"].get("sorry_count_in_source") == 0)}
    if A[1] and A[3]:
        cross["project_file_counts"] = {"agent_1": A[1]["build"].get("project_module_counts"), "agent_3": A[3]["scope"].get("n_lean_files_by_dir")}
    kv = [(str(k), a["kernel_check"]["verdict"] if k == 1 else a["kernel_level"]["verdict"]) for k, a in A.items() if a and k in (1, 3)]
    cross["kernel_verdicts"] = dict(kv)
    cross["no_agent_ran_a_kernel_check"] = all("NOT-ESTABLISHED" in v for _, v in kv)
    out["cross_agent"] = cross
    if write:
        OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    if verbose:
        print("present", out["present"], "absent", out["absent"])
        for k, v in out["answers"].items():
            print(f"== {k}: {str(v.get('gate_answer'))[:400]}")
        print("cross:", cross)
    return out


if __name__ == "__main__":
    run()
