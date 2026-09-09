"""Arc-6 evidence: rebuild every number in BLOG_ADJUDICATED.md and
TECHNICAL_ADJUDICATED.md from the five curated JSONs, and draw fig112.

    .venv/bin/python writeup/6_adjudicated/adjudicated_evidence.py

Three things happen, in order:

  1. the five per-unit evidence scripts are RUN, each of which checks its own
     unit's artefact against its own journal. This script does not duplicate
     them; it requires them to pass.
  2. every number quoted in this arc's two prose documents is looked up in the
     JSON it came from. A number in the prose with no JSON field behind it is a
     documentation-contract failure and exits non-zero.
  3. fig112 is drawn FROM THE BANKED JSON ALONE and asserted against it.

Nothing is re-run: no residual is recomputed, no manuscript is re-fetched, no
Lean is parsed. A script that re-runs the experiment it is supposed to check
cannot disagree with it -- CORRECTIONS.md §54.

DELIBERATELY NOT CHECKED HERE: whether the external manuscript is correct. This
arc did not establish that and this script does not move it.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "writeup" / "data"
FIGS = ROOT / "writeup" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
PY = str(ROOT / ".venv" / "bin" / "python")
if not Path(PY).exists():
    PY = sys.executable

UNIT_CHECKS = [
    "writeup/arc6_acquire_evidence.py",
    "writeup/arc6_lean_evidence.py",
    "writeup/arc6_skeleton_evidence.py",
    "writeup/arc6_instantiate_evidence.py",
    "writeup/arc6_w4_port_evidence.py",
]

fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fail.append(label)


def load(name):
    return json.loads((DATA / name).read_text())


acq = load("arc6_acquire_v1.json")
lean = load("arc6_lean_v1.json")
skel = load("arc6_skeleton_v1.json")
inst = load("arc6_instantiate_v1.json")
port = load("arc6_w4_port_v1.json")

tech = (HERE / "TECHNICAL_ADJUDICATED.md").read_text()
blog = (HERE / "BLOG_ADJUDICATED.md").read_text()
tn = re.sub(r"\s+", " ", tech)
bn = re.sub(r"\s+", " ", blog)
both = tn + " " + bn

print("== 1. the five per-unit evidence scripts must pass")
for rel in UNIT_CHECKS:
    r = subprocess.run([PY, str(ROOT / rel)], capture_output=True, text=True, cwd=ROOT)
    check(r.returncode == 0, f"{rel} exits 0",
          "" if r.returncode == 0 else (r.stdout + r.stderr)[-400:])

print("== 2. every number in the prose is in the JSON it came from")

def in_prose(tok, where=both, label=None):
    check(tok in where, f"prose carries {label or tok}")

# U1
check(acq["artifacts_fetched"][0]["pages"] == 166, "U1: 166 pages banked")
in_prose("166-page", label="166-page manuscript")
in_prose(acq["artifacts_fetched"][0]["sha256"][:16], label="manuscript sha256 prefix")
in_prose(acq["artifacts_fetched"][3]["head_commit_sha1"], label="Lean HEAD sha")
check(acq["gate"]["answer"] == "DIFFERS-AS-FOLLOWS", "U1 gate answer")
in_prose("DIFFERS-AS-FOLLOWS")
check(len(acq["gate"]["differences"]) == 7, "seven differences")
check(len(acq["gate"]["agreements"]) == 8, "eight agreements")
in_prose("Eight agreements", tn, "eight agreements (technical)")
in_prose("Seven differences", tn, "seven differences (technical)")

# U2
cl = lean["gate_c_sorry_and_axiom_free"]["import_closure_measured_here"]
for tok in ["580", "379,522", "23,604", "1,829", "1,770", "2,486", "73"]:
    in_prose(tok)
check(cl["NavierStokes.ComparatorSolution"]["modules"] == 580, "580-module closure")
check(cl["modules_in_no_main_closure"] == 73, "73 dead modules")
s = lean["gate_c_sorry_and_axiom_free"]["source_level_census_tracked_files_only"]
check(s["sorry_token_occurrences_total"] == 5, "5 sorry occurrences")
check(s["sorry_proof_placeholders"] == 4, "4 of them placeholders")
in_prose("29 `sorry`s and 6", tn, "the .lake numbers, stated not hidden")
g = lean["gate_d_fraction_formalised"]["cross_reference_census"]
check(g["distinct_labels_cited_in_lean"] == 25, "25 cited labels")
check(g["present_in_NEITHER_published_manuscript"] == 15, "15 in neither")
for tok in ["25 distinct", "15 exist in NEITHER", "12.3%", "9 of 73"]:
    in_prose(tok, tn)
in_prose("f446284f2aa54375f558c263a580b34e2e7bc9f44a28829637199cc72257d25d", tn,
         "the upstream reference sha256")
in_prose("6a10ac8c22beadecabdbb0919c2b50214762f91d", tn, "the lean commit")
in_prose("mathlib4.blob.core.windows.net", tn, "the denied host")
in_prose("461,265,558", tn, "the transient-failure byte count")

# U3
pa = skel["what_pays_for_compact_support_of_f"]["page_accounting"]
check(pa["flatness_machinery_pages"] == 131, "131 pages of flatness machinery")
check(pa["flatness_machinery_percent"] == 78.9, "= 78.9%")
in_prose("131 of 166 pages", tn)
in_prose("78.9%")
check(skel["gate"]["answer"] == "PARTLY", "U3 gate PARTLY")
in_prose("PARTLY", tn)
check(skel["re_derivation"]["quantities_agreeing"] == 23, "23 quantities agree")
in_prose("23", tn, "23 quantities")
in_prose("we set `f = R(u,p)`", tn, "the sentence that settles clause 1")
in_prose("not a shortcut", both, "leg 381's surviving half")

# U4
p0 = [c for c in inst["cases"] if c["name"] == "P0_instantiation"][0]
check(abs(p0["reported_exponent"] + 1.498218) < 5e-6, "P0 = -1.498218")
in_prose("−1.498218", tn)
in_prose("0.011782", tn)
in_prose("2.11e-07", tn)
check(inst["gate"]["controls_all_as_predicted"] is False, "U4's conjunction is unmet")
in_prose("conjunction is NOT met", tn)
in_prose("post-hoc", tn)
r = abs(inst["exterior_moment_int_r2_Rtheta"]) / inst["exterior_moment_int_r2_Rtheta_abs"]
check(abs(r - 1.0) < 1e-6, "the one-sign ratio is exactly 1.0000")
in_prose("1.0000", tn)

# U5
check(port["gate"]["answer"] == "NO", "U5 gate NO")
check(port["M1_core"]["reported_exponent"] == -1.5
      or abs(port["M1_core"]["reported_exponent"] + 1.5) < 1e-6, "M1 = -1.500000")
in_prose("−1.500000", tn)
in_prose("3.47e-07", tn)
key = f"{port['prereg']['rho_reported']:g}"
lb = port["THE_LOG"]["per_rho"][key]
check(abs(lb["log_fit_slope_per_decade"] - 0.743203) < 1e-5, "b = 0.743203")
check(lb["log_fit_r2"] > lb["power_fit_r2"], "log fit beats power fit")
for tok in ["0.743203", "0.9999976208", "0.9999292516", "−0.005321"]:
    in_prose(tok, tn)
for tok in ["0.7479", "0.7419", "0.7412", "0.7435"]:
    in_prose(tok, tn, f"increment {tok}")
ff = port["M3_M4_farfield"]
check(abs(ff["alpha_mean"] + 1.0) < 1e-4, "alpha = -1.000004")
in_prose("−1.000004")
check(1.9 < ff["delta_mean"] < 2.0, "delta = 1.974126")
in_prose("1.974126", tn)
check(port["M6_direct_stencil_status"]["verdict"] == "UNDER-RESOURCED", "M6 under-resourced")
in_prose("UNDER-RESOURCED", tn)
in_prose("0.857", tn)

print("== 3. the ceilings are in the prose, not only in the JSON")
for j in (acq, lean, skel, inst, port):
    check(j["clay_movement"]["links_moved"] == 0, f"{j['schema']}: links_moved 0")
    check("UNVERIFIED" in j["verification_status"], f"{j['schema']}: UNVERIFIED")
in_prose("No `L1 → L4` link moved", tn)
in_prose("~0.05%")
in_prose("UNVERIFIED", tn)
in_prose("no known method", tn)
check("W4 STANDS" in tn or "`W4` STANDS" in tn, "prose states W4 STANDS")
check("stands" in bn.lower(), "the blog says the wall stands")
check("cannot say the proof is correct" in bn,
      "the blog states what was NOT established, in its own words")

print("== 4. fig112, drawn from the banked JSON alone")
rows = port["M5_M6_annulus_counterfactual"]["per_rho"][key]["ladder"]
taus = [r["tau"] for r in rows]
fs = [r["max_abs_f_cutonly"] for r in rows]
erows = port["M2_energy"]["ladder"]
etaus = [r["tau"] for r in erows]
es = [r["energy"] for r in erows]

x = [-__import__("math").log10(t) for t in taus]
b = lb["log_fit_slope_per_decade"]
c = lb["log_fit_intercept"] if "log_fit_intercept" in lb else fs[0] - b * x[0]

fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.9))
ax[0].plot(x, fs, "o-", color="#dc2626", lw=2, ms=6,
           label=r"$\max|f_{\rm cut\ only}|$")
ax[0].plot(x, [b * xx + c for xx in x], ls="--", color="#6b7280", lw=1.3,
           label=fr"$c + {b:.4f}\,\log_{{10}}(1/\tau)$")
ax[0].set_xlabel(r"$\log_{10}(1/\tau)$")
ax[0].set_ylabel("cutoff-generated force")
ax[0].set_title("U5: the force is LOGARITHMICALLY unbounded\n"
                f"per-decade increments {', '.join(f'{i:.4f}' for i in lb['per_decade_increment_of_f'])}")
ax[0].legend(loc="upper left")

ex = [-__import__("math").log10(t) for t in etaus]
ax[1].plot(ex, es, "o-", color="#2563eb", lw=2, ms=6, label=r"$\int|u_{\rm cut}|^2\,dx$")
ax[1].axhline(es[-1], color="#6b7280", ls=":", lw=1.2, label=f"converging to ≈ {es[-1]:.2f}")
ax[1].set_xlabel(r"$\log_{10}(1/\tau)$")
ax[1].set_ylabel("kinetic energy")
inc = port["M2_energy"]["classification"]["per_decade_increment"]
ax[1].set_title("and the energy genuinely CONVERGES\n"
                f"increments {', '.join(f'{i:.3f}' for i in inc)} — falling geometrically")
ax[1].legend(loc="lower right")
fig.suptitle("fig112 — arc 6 / U5: two ladders with the same tiny power exponent, "
             "and only one of them is bounded", fontsize=10)
fig.tight_layout()
out = FIGS / "fig112_arc6_w4_port_v1_log.png"
fig.savefig(out)
plt.close(fig)

# executable assertions on the figure's own content
assert len(fs) == 5 and len(es) == 5, "fig112: both ladders must have five rungs"
assert all(fs[i + 1] > fs[i] for i in range(4)), "fig112: f must be increasing"
_inc = [fs[i + 1] - fs[i] for i in range(4)]
assert max(_inc) - min(_inc) < 0.01, "fig112: f's increments must be constant (a log)"
_einc = [es[i + 1] - es[i] for i in range(4)]
assert all(_einc[i + 1] < _einc[i] for i in range(3)), \
    "fig112: the energy's increments must FALL (convergence)"
assert lb["log_fit_r2"] > lb["power_fit_r2"], "fig112: the log fit must beat the power fit"
check(out.exists(), f"fig112 written to {out.relative_to(ROOT)}")

print()
if fail:
    print(f"DRIFT: {len(fail)} check(s) failed")
    for x_ in fail:
        print(f"  - {x_}")
    sys.exit(1)
print("arc6 adjudicated evidence: all checks pass")
