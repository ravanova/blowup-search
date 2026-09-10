"""Arc-6 R5(i) evidence (leg 430): rebuild every prose number from
writeup/data/arc6_profile_v1.json and draw fig113 from the banked JSON alone.

    .venv/bin/python writeup/arc6_profile_evidence.py

Nothing is re-run: no profile is rebuilt here (the runner takes half an hour;
test_arc6_profile_v1.py re-runs the controls on a coarse grid). This script
checks that the banked gate answers follow from the banked numbers by the
pre-registered rules, that the journal quotes those numbers, and draws the
figure. Exits nonzero on drift.
"""
import json, re, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "writeup" / "data" / "arc6_profile_v1.json").read_text())
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_430.md").read_text())
FIGS = ROOT / "writeup" / "figures"
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)

sys.path.insert(0, str(ROOT / "experiments"))
from arc6_profile_v1 import gates  # noqa: E402  (pure arithmetic on the banked dict; no build)

print("== 1. the pre-registered runs: gate answers follow from the banked numbers")
pre = D["preregistered_runs"]
check(sorted(pre) == ["0.025", "0.05", "0.1"], "three pre-registered lambdas")
for lam, r in pre.items():
    g = gates(r)
    check({k: v[0] for k, v in g.items()} == {k: v[0] for k, v in r["gates"].items()}, f"lambda={lam}: banked gate answers re-derive from the banked numbers")
r1 = pre["0.1"]
check(r1["gates"]["G1"][0] == "YES" and 0.20 < r1["G1"]["K_b"] <= 0.25, f"G1 K_b = {r1['G1']['K_b']:.5f}")
check(r1["gates"]["G2"][0] == "YES", "G2 bracket values")
check(all(pre[l]["gates"]["G3"][0] == "NO" and pre[l]["G3"]["n_nan"] == pre[l]["params"]["n_eta"] for l in pre), "G3 NO at every pre-registered lambda: no root on [.9, 1.2] at any eta")
check(all(pre[l]["gates"]["G7"][0] == "NO" for l in pre), "G7 NO at every pre-registered lambda")
check(all(pre[l]["gates"]["G6"][0] == "YES" and pre[l]["gates"]["G8"][0] == "YES" for l in pre), "G6, G8 YES at every pre-registered lambda")
check(all(pre[l]["gates"]["G4_paper_normalisation"][0] == "YES" and pre[l]["gates"]["G4_as_preregistered"][0] == "NO" for l in pre), "G4: NO as pre-registered (the wrong scale), YES at the paper's bump-centre scale")
check(all(pre[l]["gates"]["G5"][0] == "NO" and pre[l]["G5"]["rI_tail_end_rel_err"] < 1e-13 for l in pre), "G5: NO on the pre-registered 1e-6 measure; the identity holds in Lemma A.8's form to 1e-13")
rem = {l: pre[l]["G3"]["S_pieces"]["S_start/norm"] for l in pre}
check(all(abs(rem[l]) > 1e3 for l in pre), "the (A.19) remainder exceeds 1e3 at every pre-registered lambda", str(rem))

print("== 2. controls: two fired, two did not, one was not run — as the journal says")
c = D["controls"]
check(sorted(c) == ["C1_flip_lambda", "C3_drop_c12", "C5_drop_A11_bumps", "C6_R0_cut_5"], "C1, C3, C5, C6 were run; C2 was not (its twin G3 fails at every pre-registered lambda)")
check(c["C1_flip_lambda"]["G7"][0] == "NO" and c["C1_flip_lambda"]["G6"][0] == "NO", "C1 flip lambda FIRED: G6, G7 fail")
check(c["C3_drop_c12"]["G4_paper_normalisation"][0] == "NO" and max(c["C3_drop_c12"]["G4_paper_normalisation"][1]) > 1e-3, "C3 drop c1,c2 FIRED: G4 fails", str(c["C3_drop_c12"]["G4_paper_normalisation"][1]))
check(c["C5_drop_A11_bumps"]["G4_paper_normalisation"][0] == "YES" and abs(c["C5_drop_A11_bumps"]["G5"][1] - r1["G5"]["angular_moment_integral_over_abs"]) < 1e-9 and max(abs(x) for x in r1["G4"]["cb"]) < 1e-10,
      "C5 drop (A.11) bumps DID NOT FIRE: the bump coefficients are ~1e-14 and nothing measurable changes", f"cb={r1['G4']['cb']}")
check(c["C6_R0_cut_5"]["G1"][0] == "YES" and c["C6_R0_cut_5"]["G2"][0] == "YES" and 0 < r1["G1"]["K_b"] - c["C6_R0_cut_5"]["G1"][1] < 1e-3,
      "C6 R_0 cut at 5 DID NOT FIRE: K_b shifts by less than 1e-3 and stays in (.20, .25]", f"{c['C6_R0_cut_5']['G1'][1]:.5f} vs {r1['G1']['K_b']:.5f}")

print("== 2b. G6's cross-lambda exponent (pre-registered window [30, 36]; not implemented in gates(), computed here)")
lam3 = [0.1, 0.05, 0.025]; eb = [pre[str(l)]["G6"]["e_b_over_P1"] for l in lam3]
slope = float(np.polyfit(np.log(lam3), np.log(eb), 1)[0])
pred = [((30 + 60 * lam3[i + 1]) * np.log(lam3[i + 1]) - (30 + 60 * lam3[i]) * np.log(lam3[i])) / (np.log(lam3[i + 1]) - np.log(lam3[i])) for i in range(2)]
pair = [(np.log(eb[i + 1]) - np.log(eb[i])) / (np.log(lam3[i + 1]) - np.log(lam3[i])) for i in range(2)]
check(not (30 <= slope <= 36), f"the fitted exponent {slope:.2f} is OUTSIDE the pre-registered [30, 36]: G6's exponent sub-gate is NO")
check(all(abs(pair[i] - pred[i]) < 0.1 for i in range(2)), "and it equals the schedule's own lambda^(30 + 60 lambda) to 0.1", f"measured {[round(x, 2) for x in pair]} vs {[round(x, 2) for x in pred]}")
ratio = [eb[i] / lam3[i] ** (30 + 60 * lam3[i]) for i in range(3)]
check(max(ratio) / min(ratio) < 1.1 and all(l ** (60 * l) < 1 for l in lam3), "e_b / lambda^(30 + 60 lambda) is one constant across the three lambda (to 10 %), so e_b <= C lambda^30 (A.14) holds with that constant", f"{[f'{x:.3e}' for x in ratio]}")

print("== 3. the post-hoc sweep, labelled as such")
ph = D["post_hoc"]
check("decided after" in ph["label"], "post-hoc block carries its label")
sw = ph["lambda_sweep"]
lams = sorted((float(k) for k in sw), reverse=True)
check(lams[0] == 0.1 and lams[-1] <= 1e-4, f"sweep from 0.1 down to {lams[-1]}")
for k, v in sw.items():
    lam = float(k)
    asym = (lam ** (-120 * lam) - 1) / 2
    check(abs(v["remainder_E_at_Amp1"]) / asym > 0.3 and abs(v["remainder_E_at_Amp1"]) / asym < 3.0, f"lambda={k}: remainder within a factor 3 of (lambda^-120lambda - 1)/2", f"{v['remainder_E_at_Amp1']:.3g} vs {asym:.3g}")
roots = [k for k, v in sw.items() if v["root_in_bracket"]]
check(sorted(float(k) for k in roots) == sorted(l for l in lams if l <= 3e-4), "a root on the paper's bracket exists at every swept lambda <= 3e-4 and at none above (measured; the pre-sweep guess from the asymptote was 1e-4)", str(roots))
check(all(abs(sw[k]["remainder_E_at_Amp1"]) > 0.0384 for k in sw if not sw[k]["root_in_bracket"]), "wherever there is no root, |remainder| exceeds P(1.2)'s lower bound .038 (p. 133)")
ps = ph["P_star_role_at_lambda_0.01"]
check(ps["paper"]["int_fraction_ok"] < ps["1.0"]["int_fraction_ok"], "at lambda = 0.01 a smaller P_* enlarges the part of the intermediate interval that passes the cone test")

print("== 4. the journal quotes what the artefact holds")
for tok in [f"{r1['G1']['K_b']:.4f}", "NO-AND", "post hoc", "UNVERIFIED", "Tier 2", "DID NOT FIRE", "C2 was not run", f"{slope:.1f}", "3·10⁻⁴", "not a proof"]:
    check(tok in J, f"journal quotes {tok!r}")

print("== 5. fig113, drawn from the banked JSON alone")
fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
fld = r1["fields"]
y = np.array(fld["y"]); ax[0].plot(y, np.array(fld["test2_max_over_eta"]).clip(1e-30, None), lw=0.8, label="max_η test₂ (A.24)")
ax[0].axhline(2, color="k", ls="--", lw=0.8, label="2")
ax[0].set_yscale("log"); ax[0].set_xlabel("y = log(X/X_R)"); ax[0].set_title("λ = 0.1: the second cone test along the profile")
for k, v in r1["params"]["stage_starts"].items():
    ax[0].axvline(v, color="0.8", lw=0.5)
ax[0].legend(fontsize=8)
xs = np.array(lams); ys = np.array([abs(sw[str(l) if str(l) in sw else repr(l)]["remainder_E_at_Amp1"]) for l in lams])
ax[1].loglog(xs, ys, "o-", label="measured |E| at Amp = 1")
ax[1].loglog(xs, (xs ** (-120 * xs) - 1) / 2, "--", label="(λ^{-120λ} − 1)/2")
ax[1].loglog(xs, 60 * xs * np.log(1 / xs), ":", label="60 λ log(1/λ)")
ax[1].axhline(0.038, color="k", lw=0.8); ax[1].set_xlabel("λ"); ax[1].set_title("(A.19) remainder vs λ; .038 = bracket margin"); ax[1].legend(fontsize=8)
ax[2].semilogx(xs, [sw[k]["int_fraction_ok"] for k in map(str, lams) if k in sw], "s-", label="intermediate interval")
ax[2].semilogx(xs, [sw[k]["pulse_fraction_ok"] for k in map(str, lams) if k in sw], "^-", label="pulse")
ax[2].set_ylim(0, 1.05); ax[2].set_xlabel("λ"); ax[2].set_title("fraction of grid points passing (A.24), P_* = 2e^{T_d}"); ax[2].legend(fontsize=8)
fig.suptitle("fig113 — arc 6 / R5(i): Lemma 4.8's outer profile from Appendix A's schedule; where the paper's asymptotics bite", fontsize=10)
fig.tight_layout()
out = FIGS / "fig113_arc6_profile_v1.png"
fig.savefig(out, dpi=110)
check(out.exists() and out.stat().st_size > 20000, f"fig113 written ({out.stat().st_size:,} B)")
print()
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 R5(i) evidence: all checks pass")
