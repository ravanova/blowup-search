"""Arc-6 U3 evidence: rebuild every number in leg 419's prose from the ledger.

    .venv/bin/python writeup/arc6_skeleton_evidence.py

Two independent things are checked, and they are checked against each other:

  1. writeup/data/arc6_skeleton_v1.json against experiments/journal/leg_419.md —
     no prose number without a JSON field behind it;
  2. the JSON against solver/arc6_residual_ledger.py RE-RUN HERE — every banked
     scale, deficit and threshold is recomputed, not read back. If the module
     and the artefact ever disagree, the artefact is the one that is wrong and
     this script says so.

Exit 0 = no drift. Exit 1 = a prose number, or a banked one, left its source.

DELIBERATELY NOT DONE HERE: any claim that the manuscript is correct. This
script checks that a scaling ledger is internally consistent and that the prose
reports it faithfully. A consistent ledger is a necessary condition on a
construction and nowhere near a sufficient one.
"""

import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from solver.arc6_residual_ledger import (  # noqa: E402
    CorrectionCycle,
    EnergyLedger,
    GeometryLedger,
    PulseLedger,
    Scale,
    manuscript_ledger,
    route4_contrast,
)

JSON = ROOT / "writeup" / "data" / "arc6_skeleton_v1.json"
JOURNAL = ROOT / "experiments" / "journal" / "leg_419.md"

fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fail.append(label)

d = json.loads(JSON.read_text())
j = JOURNAL.read_text()
# The journal is hard-wrapped Markdown, so a quotation can straddle a newline and
# an exponent can be written without the spaces the module's __str__ inserts.
# Prose checks run against a whitespace-normalised copy; the JSON checks do not.
jn = re.sub(r"\s+", " ", j)
jt = re.sub(r"\s+", "", j)

print("== 1. the banked ledger table is what the module produces, re-run here")
led = manuscript_ledger()
tab = d["re_derivation"]["table"]
check(len(tab) == len(led) == 23, "23 quantities, module and artefact agree", str(len(tab)))
for name, (derived, printed, agree) in led.items():
    row = tab[name]
    check(row["re_derived"] == str(derived),
          f"{name}: banked re-derived value is the module's", row["re_derived"])
    check(row["manuscript_prints"] == str(printed), f"{name}: banked printed value matches")
    check(row["agree"] is agree is True, f"{name}: agrees, in the artefact and on re-run")
check(d["re_derivation"]["quantities_agreeing"] == 23, "artefact records 23 agreements")
check(d["re_derivation"]["mismatches"] == [], "artefact records zero mismatches")

print("== 2. the identities, recomputed")
g, p, e, c = GeometryLedger(), PulseLedger(), EnergyLedger(), CorrectionCycle()
check(g.leading_balance_holds(), "the three leading rates coincide")
check(g.radial_diffusion_rate == Scale(F(-1), F(0)), "and the common rate is exactly q^-1")
check(p.stress_cancels_residual(), "pulse stress divergence == leading tangential residual")
check(str(p.stress_divergence) == "q^(-3/2 - h)", "and that value is q^(-3/2 - h)",
      str(p.stress_divergence))
check("q^(-3/2-h)" in jt, "the journal quotes q^(-3/2 - h)")
check(e.critical_h() == F(1, 6), "critical h = 1/6")
check("h = 1/6" in jn, "the journal quotes h = 1/6")
check(c.sigma(0) == F(1, 5) and c.stages_to_reach(1) == 8,
      "sigma_0 = 1/5 and 8 stages reach sigma = 1")
check("8 stages" in jn, "the journal quotes 8 stages")

print("== 3. the route-4 contrast, recomputed")
r = route4_contrast()
b = d["route4_contrast"]
check(b["alpha_pinned"] == str(r["alpha_pinned"]) == "1", "alpha pinned at 1")
check(b["L2_deficit"] == str(r["L2_deficit"]) == "1/2", "L^2 deficit exactly 1/2")
check(b["cutoff_bill_deficit"] == b["L2_deficit"],
      "leg 381's cutoff-bill deficit is the SAME number as the L^2 deficit")
check(b["L3_shell_integrand_exponent"] == str(r["L3_integrand_exponent"]) == "-1",
      "L^3 shell integrand exponent is exactly -1, i.e. log-divergent")
check(b["L3_deficit"] == "0", "L^3 deficit exactly 0 — alpha = 1 is critical, not a near miss")
check(r["L2_converges"] is False and r["L3_converges"] is False,
      "neither integral converges at alpha = 1")
check(not (2 * F(3, 2) > 3),
      "and alpha = 3/2 is ITSELF critical for L^2 — why leg 381's bill is strict")
check("α ≥ 1.5" in jn and "α > 1.5" in jn,
      "the journal states the strict/non-strict distinction it caught")

print("== 4. the page accounting adds to 166")
pa = d["what_pays_for_compact_support_of_f"]["page_accounting"]
parts = [pa["sections_1_3_setup_and_outline_pages"],
         pa["sections_4_9_MAKING_THE_RESIDUAL_FLAT_pages"],
         pa["section_10_localisation_and_force_extension_pages"],
         pa["appendices_A_C_serving_section_4_pages"],
         pa["references_pages"]]
check(sum(parts) == 166 == pa["total"], "23 + 92 + 10 + 39 + 2 = 166", str(sum(parts)))
check(pa["flatness_machinery_pages"] == 92 + 39 == 131, "flatness machinery = 131 pages")
check(pa["flatness_machinery_percent"] == round(100 * 131 / 166, 1) == 78.9,
      "= 78.9% of the manuscript", str(pa["flatness_machinery_percent"]))
check("78.9%" in jn and "131 of 166 pages" in jn, "the journal quotes both figures")
check(pa["condition_5_discharge"].startswith("3 lines"),
      "and records that condition (5) costs three lines")

print("== 5. the gate is answered in its pre-committed wording")
gt = d["gate"]
check(gt["question"].startswith("Is TECHNICAL_OUTPACED.md §2 right"),
      "gate question is the pre-committed one")
check(gt["answer"] in ("YES", "NO", "PARTLY"), "answer is one of the three permitted words",
      gt["answer"])
check(gt["answer"] == "PARTLY", "answer is PARTLY")
check("PARTLY" in jn, "journal states the gate answer")
check("UNVERIFIED" in gt["answer_status"], "gate answer labelled UNVERIFIED (§3f rule 1)")
check(gt["clause_1"]["verdict"] == "RIGHT", "clause 1 verdict RIGHT")
check("we set f = R(u,p)" in gt["clause_1"]["the_line_that_settles_it"],
      "clause 1 cites the manuscript line that settles it")
check(gt["clause_2"]["verdict"].startswith("RIGHT ABOUT CONDITION (5)"),
      "clause 2 verdict splits (5) from the cost of compact support")
ol = gt["on_leg_381"]
check(ol["verdict"].startswith("SPLIT"), "leg 381 verdict is a SPLIT, not a reversal")
check("IT DOES NOT APPLY AND IT IS NOT SAID" in ol["the_words_NOT_said"],
      "the charter's offered sentence is explicitly NOT said")
check("IT DOES NOT APPLY AND IT IS NOT SAID" in jn,
      "and the journal says so in the same words")

print("== 6. the ceiling is stated as a number, not an adjective")
cm = d["clay_movement"]
check(cm["links_moved"] == 0, "L1->L4 links moved = 0")
check(cm["walls_moved"] == "none", "walls moved = none")
check("0.05" in cm["clay_odds"], "Clay odds unchanged")
check("UNVERIFIED" in d["verification_status"], "unit banked UNVERIFIED")
check(d["novelty_pass"].endswith("BEFORE the module existed"),
      "the novelty pass is recorded as preceding the module")
check("cc52087" in d["novelty_pass"], "with the commit that proves it")

print()
if fail:
    print(f"DRIFT: {len(fail)} check(s) failed")
    for x in fail:
        print(f"  - {x}")
    sys.exit(1)
print("arc6 U3 evidence: all checks pass")
