"""Arc-6 R5(ii) evidence (leg 432): rebuild every prose number from
writeup/data/arc6_residual_v1.json and draw fig114 from the banked JSON alone.

    .venv/bin/python writeup/arc6_residual_evidence.py

Nothing is re-run here (the runner takes minutes; test_arc6_residual_v1.py re-runs the
controls on a coarse grid). Checks that the banked gate answers follow from the banked
numbers by the pre-registered (and amended, before any number) rules, that the journal
quotes those numbers, and draws the figure. Exits nonzero on drift.
"""
import json, re, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "writeup" / "data" / "arc6_residual_v1.json").read_text())
J = re.sub(r"\s+", " ", (ROOT / "experiments" / "journal" / "leg_432.md").read_text())
FIGS = ROOT / "writeup" / "figures"
fail = []
def check(ok, label, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok: fail.append(label)
sys.path.insert(0, str(ROOT / "experiments"))
from arc6_residual_v1 import gates  # noqa: E402  (pure arithmetic on the banked dict; no build)

print("== 1. the pre-registered runs: gate answers follow from the banked numbers")
pre = D["preregistered_runs"]
check(sorted(pre) == ["0.001", "1e-07"] and D["prereg_commits"] == ["96657de", "fcac005"], "two pre-registered h, both pre-registration commits named")
for h, r in pre.items():
    g = gates(r)
    check({k: v[0] for k, v in g.items()} == {k: v[0] for k, v in r["gates"].items()}, f"h={h}: banked gate answers re-derive from the banked numbers")
    check(all(v[0] == "YES" for v in r["gates"].values()), f"h={h}: H0–H7 all YES", str({k: v[0] for k, v in r["gates"].items()}))
r7, r3 = pre["1e-07"], pre["0.001"]
check(max(r3["H0"].values()) < 1e-6 and max(r7["H0"].values()) < 1e-6, "H0: the two routes agree to 1e-6 on A, B and T_z at both h", f"h=1e-3: {r3['H0']}")
bb = r3["H2"]["boundary_over_b0"]
check(abs(bb["0.05"] - 1) < 0.5 and bb["0.4"] > bb["0.2"] > bb["0.1"] > bb["0.05"] > 1, "H2(i): the boundary term over b_theta(0,eta) tends to 1 from above", str(bb))
check(abs(r3["H2"]["local_power_Ttheta_hat_at_0.05"]) < 0.5 and abs(r7["H2"]["local_power_Ttheta_hat_at_0.05"]) < 0.5, "H2(ii): e^{4/delta^2} T_theta carries delta^0 at resolvable delta", f"{r3['H2']['local_power_Ttheta_hat_at_0.05']:.3f}")
check(r3["H2"]["log10_boundary_fraction_at_0.05"] < -190 and r3["H2"]["delta_cross"] < 1e-60, "H2(iii): the boundary term is ~1e-203 of the total; the (A.48) collar is delta < ~1e-69", f"log10 frac {r3['H2']['log10_boundary_fraction_at_0.05']:.1f}, delta_x {r3['H2']['delta_cross']:.2e}")
check(2.5 <= r3["H3"]["local_power_Tz_over_Ttheta_at_0.05"] <= 3.5 and 2.5 <= r7["H3"]["local_power_Tz_over_Ttheta_at_0.05"] <= 3.5, "H3: T_z/T_theta carries delta^3 at resolvable delta (the paper's delta^6 is the collar limit)", f"{r3['H3']['local_power_Tz_over_Ttheta_at_0.05']:.3f}")
check(r3["H3"]["C_sup_ratio_over_Epow"] < 10 and r7["H3"]["C_sup_ratio_over_Epow"] < 10, "H3: |T_z/T_theta| <= C E_pow with C < 10 (A.55)", f"C = {r3['H3']['C_sup_ratio_over_Epow']:.3f}")
check(abs(r3["H4"]["fop_over_fo_max_over_h"] - 0.4) < 0.01 and abs(r7["H4"]["fop_over_fo_max_over_h"] - 0.4) < 0.01, "H4: f_o'/f_o reaches 0.40 h at c_o = 0.1 — above the paper's h/4 (leg 430's prereg claimed otherwise)")
check(r3["H4"]["a_minus_2_min_over_h"] > 1.19 and r3["H4"]["a_minus_2_max_over_h"] <= 2.0 + 1e-9, "H4: a - 2 in (1.2 h, 2 h] — inside the paper's (h, 2h] all the same")
check(all(v["Ttheta_rel"] < 1e-10 and v["Tz_rel"] < 1e-10 for rr in (r3, r7) for v in rr["H6"].values()), "H6: q-invariance of q^{A+1/2} T at q = 1, 10, 1000 to 1e-10")
check(all(rr["H7"]["A_beyond_Xb"] == 0 and rr["H7"]["B_beyond_Xb"] == 0 and rr["H7"]["Tz_bracket_beyond_max"] == 0 for rr in (r3, r7)) and abs(r3["H7"]["delta3_dlogT_ddelta_at_0.05"] - 8) < 0.01, "H7: the stress vanishes identically beyond X_b and delta^3 d log T/d delta = 8", f"{r3['H7']['delta3_dlogT_ddelta_at_0.05']:.4f}")
check("could_not_determine" in r3["H8"], "H8: X_a reported as could-not-determine from the tail alone")

print("== 2. the six planted controls, each against its twin")
c = D["controls"]
check(sorted(c) == ["K1_poly_cutoff", "K2_D_equals_A", "K3_residual_moment", "K4_flip_cutoff", "K5_minus_h", "K6_no_heat"], "K1–K6 present")
check(c["K1_poly_cutoff"]["gates"]["H7"] == "NO" and c["K1_poly_cutoff"]["gates"]["H2"] == "NO" and abs(c["K1_poly_cutoff"]["H7"]["delta3_dlogT_ddelta_at_0.05"]) < 0.1, "K1 FIRED: without the flat factor delta^3 d log T/d delta ~ 0, not 8")
check(c["K2_D_equals_A"]["gates"]["H6"] == "NO" and c["K2_D_equals_A"]["H6"]["1000.0"]["Tz_rel"] > 1e-4, "K2 FIRED: D = A breaks the q-invariance of T_z", f"{c['K2_D_equals_A']['H6']['1000.0']['Tz_rel']:.2e}")
check(c["K3_residual_moment"]["gates"]["H7"] == "NO" and c["K3_residual_moment"]["H7"]["A_beyond_Xb"] == 1e-3, "K3 FIRED: a residual moment leaves stress beyond X_b")
check(c["K4_flip_cutoff"]["gates"]["H1"] == "NO" and c["K4_flip_cutoff"]["H1"]["min_A"] < 0, "K4 FIRED: the reversed cutoff makes T_theta negative")
check(c["K5_minus_h"]["gates"]["H4"] == "NO", "K5 FIRED: h -> -h leaves the shear bracket")
check(c["K6_no_heat"]["gates"]["H7"] == "NO" and abs(c["K6_no_heat"]["H7"]["B_beyond_Xb"] + 2.002) < 1e-9, "K6 FIRED: without the heat factor T_theta -> -(2+2h) F beyond X_b — the power law's own viscous residual")

print("== 3. the journal quotes what the artefact holds")
for tok in ["NOT TESTABLE", "amendment", f"{r3['H3']['local_power_Tz_over_Ttheta_at_0.05']:.2f}", f"{bb['0.05']:.2f}", "0.40", "10⁻⁶⁹", "Tier 2", "not a proof", "UNVERIFIED", "K1–K6", "could not determine"]:
    check(tok in J, f"journal quotes {tok!r}")

print("== 4. fig114, drawn from the banked JSON alone")
f = r3["fields"]; y = np.array(f["y"]); dl = np.array(f["delta"])
fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
ax[0].plot(y, f["log10_Ttheta_hat"], lw=1.2, label="log₁₀ e^{4/δ²} T₀,θ  (route A = route B to 10⁻⁹)")
ax[0].axvline(3, color="k", ls="--", lw=0.8); ax[0].set_xlabel("y = log(X/X_tail)"); ax[0].set_title("h = 10⁻³: the tail stress, flat factor removed"); ax[0].legend(fontsize=8)
m = (dl > 0.03) & (dl < 1.5)
ax[1].semilogx(dl[m], np.array(f["boundary_over_b0"])[m], "o-", ms=3, label="boundary term ÷ b_θ(0,η) of (A.48)")
ax[1].axhline(1, color="k", ls="--", lw=0.8); ax[1].set_xlabel("δ = 3 − y"); ax[1].set_title(f"the boundary term → b_θ(0,η); it is 10^{r3['H2']['log10_boundary_fraction_at_0.05']:.0f} of the total"); ax[1].legend(fontsize=8)
lz = np.array(f["log10_Tz_over_Ttheta_max"]); mm = (dl > 0.03) & (dl < 2.0) & np.isfinite(lz) & (lz > -299)
ax[2].plot(np.log10(dl[mm]), lz[mm], lw=1.2, label="log₁₀ |T_z/T_θ| (max over η)")
x0 = np.log10(0.05); i0 = np.argmin(np.abs(dl - 0.05)); ax[2].plot([x0 - 1, x0 + 0.5], [lz[i0] - 3, lz[i0] + 1.5], "--", color="C3", lw=0.9, label="slope 3 (the resolvable-δ prediction)")
ax[2].plot([x0 - 1, x0 + 0.5], [lz[i0] - 6, lz[i0] + 3], ":", color="C2", lw=0.9, label="slope 6 (the paper's collar limit)")
ax[2].set_xlabel("log₁₀ δ"); ax[2].set_title(f"direction: local power {r3['H3']['local_power_Tz_over_Ttheta_at_0.05']:.2f} at δ = 0.05"); ax[2].legend(fontsize=8)
fig.suptitle("fig114 — arc 6 / R5(ii): the residual stress on the terminal tail, Proposition A.10 measured where a grid can reach", fontsize=10)
fig.tight_layout(); FIGS.mkdir(exist_ok=True); fig.savefig(FIGS / "fig114_arc6_residual_v1.png", dpi=110); plt.close(fig)
print("  wrote", FIGS / "fig114_arc6_residual_v1.png")
if fail:
    print(f"DRIFT: {len(fail)}"); [print("  -", x) for x in fail]; sys.exit(1)
print("arc6 R5(ii) evidence: all checks pass")
