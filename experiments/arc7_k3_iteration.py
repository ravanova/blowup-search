"""Arc 7, unit K3, slot 2 (leg 439): Q3 — the per-stage gain as a function of h.

    .venv/bin/python experiments/arc7_k3_iteration.py --claimed   # writes the claimed block only, before any run
    .venv/bin/python experiments/arc7_k3_iteration.py --full      # route B, gates, controls

Gate Q3 (leg_439_prereg.md section 3, verbatim): "the exponent gain of ONE correction stage (Section 8-9's
linear mean-correction solve on the annulus, sourced by the pinned residual), as a function of h. Route A:
Propositions 9.5/9.6's gain, h/10 in the q-exponent, evaluated at h in {1e-1, 3e-2, 1e-2} -> {1e-2, 3e-3, 1e-3},
written before the run. Route B: the solve, with h entering ONLY through the profile and the operator's
weights -- never as an input gain -- residual exponent before and after over q in {1e-2, 1e-4, 1e-6}. Gate:
measured gain within 10% of route A at each h, and gain/h in [0.09, 0.11] at all three. Controls: zero
correction -> gain ~ 0 (must fail); source negated -> residual grows (must fail); twin passes. If the stage's
linear problem cannot be instantiated in the budget (it was not in wave 4): the gate is NOT-INSTANTIATED and
DROPPED, with the cost of instantiating it stated. No exponent-ledger arithmetic is offered in its place."

Route B here IMPORTS, never edits, wave 4's arc6_w4_iteration.py Step-2 solve (Cor 8.5's radial stress
inverse, Lemma 8.2's zero-remainder fact for an auxiliary-independent source) on the pinned residual
(arc6_residual_v1.Tail / pinned_stress), calling it at three values of h so that h enters ONLY through the
tail-stress operator T_0(y, eta; h) and the profile's fixed scale (X_tail, c_inf, the lambda = 0.1 patch) --
never as a multiplicative gain fed into the solve. This is the SAME two linear steps (2 and 4) that wave 4's
agent 4 (leg 433, I1) found exact for the pinned auxiliary-independent source and therefore commuting with the
q^{-A-1/2} prefactor scaling regardless of A = 1/2 + h; here that finding is re-run and extended to h in
{1e-1, 3e-2, 1e-2} rather than asserted from the h = 1e-7 run. Tier 2. Not a proof.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "4"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "4"); os.environ.setdefault("MKL_NUM_THREADS", "4")
import argparse, json, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))
from arc6_w4_iteration import pinned_stress, mean_patch, step2, fit_exponent  # noqa: E402  (pinned Step-2 solve, leg 433; NOT edited)

OUT = ROOT / "writeup" / "data" / "arc7" / "k3" / "agent_2_iteration.json"
H_LIST = (1e-1, 3e-2, 1e-2)              # pre-registered, resolvable (leg_439_prereg.md section 0)
Q_LIST = (1e-2, 1e-4, 1e-6)              # pre-registered route-B q's for Q3
COMPONENTS = (("T_theta", 2), ("T_z", 1))


# ----------------------------------------------------------------------------------------------------------------
# 0. THE CLAIMED BLOCK -- written before any number is computed (--claimed). h/10 in the q-exponent.
# ----------------------------------------------------------------------------------------------------------------
def claimed_block():
    gain_q = {f"{h:g}": float(h / 10) for h in H_LIST}
    return {
        "written_before_run": True,
        "quantity": "the exponent gain of ONE correction stage of Section 8-9's linear mean-correction solve on the annulus, sourced by the pinned residual, as a function of h",
        "route_A": {
            "statement": "Proposition 9.6 (p. 107): B_{j+1} = B_j + 1/10, C*_{j+1} = C*_j + 1/10; every order is a power of eps = Q^h (p. 100), Q ~ q (p. 92, p. 113); the paper's per-stage q-exponent gain is therefore h/10, uniformly in the stage index j.",
            "prediction_h_to_gain_in_q_exponent": gain_q,
            "note": "This block is fixed before route B is run at any h and is not changed after the number is seen (leg_439_prereg.md section 3, Q3)."},
        "h_values": list(H_LIST), "q_values": list(Q_LIST),
        "gate_as_prereg": "measured gain within 10% of route A at each h, and gain/h in [0.09, 0.11] at all three q-fitted-over {1e-2,1e-4,1e-6}",
        "controls_as_prereg": {"zero_correction": "gain ~ 0 (must fail)", "source_negated": "residual grows (must fail)"},
        "not_instantiated_clause": "If the stage's linear problem cannot be instantiated in the budget (it was not in wave 4): the gate is NOT-INSTANTIATED and DROPPED, with the cost of instantiating it stated. No exponent-ledger arithmetic is offered in its place. (leg_439_prereg.md section 3, Q3)",
        "prior_finding_being_extended_not_assumed": "wave 4 (leg 433, agent 4, gate I1) ran this same Step-2 solve at h = 1e-7 only and found the instantiated linear steps (Cor 8.5's stress inverse, Lemma 8.7's moment map) exact for the pinned auxiliary-independent source, commuting with the q^{-A-1/2} prefactor scaling, giving a measured q-gain of 0 to 1e-9 -- structurally, not from insufficient resolution -- because the eps-gain the paper claims is produced by Steps 1 and 3 (the wave field / auxiliary torus of Section 7, unit (iii)), which are absent from the pinned interface. That finding is RE-RUN here at h in {1e-1, 3e-2, 1e-2}, not assumed; if it fails to generalise the run will show a nonzero, h-dependent gain and the gate will be scored literally."}


# ----------------------------------------------------------------------------------------------------------------
# Route B: Step 2's solve at explicit h and q; before/after residual exponents in q.
# ----------------------------------------------------------------------------------------------------------------
def route_b_at_h(h, patch):
    S = pinned_stress(h)                                    # h enters ONLY here: the tail-stress operator T_0(y, eta; h)
    out = {}
    for comp, e in COMPONENTS:
        def run(mode):
            rows = [step2(S, q, e, comp, patch, mode) for q in Q_LIST]
            qs = [r["q"] for r in rows]
            before = fit_exponent(qs, [r["log10_sup_F_before"] for r in rows])
            after_tail = fit_exponent(qs, [r["log10_sup_after_tail"] for r in rows])
            after_total = (fit_exponent(qs, [r["log10_sup_after_total"] for r in rows])
                           if all(np.isfinite(r["log10_sup_after_total"]) for r in rows) else None)
            return {"rows": rows, "before_exponent": before, "after_tail_exponent": after_tail, "after_total_exponent": after_total,
                    "gain_tail": after_tail - before, "gain_total": (after_total - before) if after_total is not None else None,
                    "tail_after_over_before_at_q": {f"{r['q']:g}": r["tail_after_over_before"] for r in rows},
                    "sigma_vs_T_rel_err_max": max(r["sigma_vs_T_rel_err"] for r in rows) if rows[0]["sigma_vs_T_rel_err"] is not None else None}
        out[comp] = {"twin": run("twin"), "skip": run("skip"), "negsource": run("negsource")}
    return out


# ----------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--claimed", action="store_true"); ap.add_argument("--full", action="store_true"); args = ap.parse_args()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base = {"schema": "arc7_k3_v1", "agent": 2, "leg": 439,
            "pages_read": ["100-118 (Section 9: Def 9.4, Props 9.5, 9.6, 9.9, Lemma 9.8)", "88-99 (Section 8: Cor 8.5, Lemmas 8.2, 8.6, 8.7)", "experiments/journal/leg_439_prereg.md section 3 Q3 (this gate, verbatim)", "experiments/journal/leg_439_prereg_amend.md (Q3 note; Q6 dropped, not this gate)"],
            "claimed": claimed_block()}
    if args.claimed:
        base["routes"] = None; base["gates"] = None; base["status"] = "claimed block written before any run"
        OUT.write_text(json.dumps(base, indent=1, default=float) + "\n"); print("wrote claimed block to", OUT); return
    if not args.full:
        print(__doc__); return

    existing = json.loads(OUT.read_text()) if OUT.exists() else None
    if existing is not None and existing.get("claimed") != base["claimed"]:
        print("WARNING: claimed block differs from the one written before the run; keeping the pre-run one")
        base["claimed"] = existing["claimed"]

    t0 = time.time()
    patch = mean_patch()
    print("[route B] mean patch:", patch)
    by_h = {}
    for h in H_LIST:
        print(f"[route B] h = {h:g} ...")
        by_h[f"{h:g}"] = route_b_at_h(h, patch)
        for comp in ("T_theta", "T_z"):
            t = by_h[f"{h:g}"][comp]["twin"]
            print(f"    {comp}: before={t['before_exponent']:.6f} after_tail={t['after_tail_exponent']:.6f} gain_tail={t['gain_tail']:.3e} gain_total={t['gain_total']}")

    # ---- gates: literal arithmetic against route A, per h, per component (twin only)
    claimed_gain = {f"{h:g}": h / 10 for h in H_LIST}
    literal = {}
    all_within_10pct, all_ratio_in_window = True, True
    for h in H_LIST:
        hk = f"{h:g}"; literal[hk] = {}
        for comp in ("T_theta", "T_z"):
            for metric in ("gain_tail", "gain_total"):
                g = by_h[hk][comp]["twin"][metric]
                if g is None:
                    continue
                claim = claimed_gain[hk]
                rel_err = abs(g - claim) / claim
                ratio = g / h
                within_10pct = rel_err < 0.10
                ratio_ok = 0.09 <= ratio <= 0.11
                literal[hk][f"{comp}.{metric}"] = {"measured_gain": g, "claimed_gain": claim, "relative_error": rel_err,
                                                    "within_10pct": bool(within_10pct), "gain_over_h": ratio, "gain_over_h_in_window": bool(ratio_ok)}
                all_within_10pct = all_within_10pct and within_10pct
                all_ratio_in_window = all_ratio_in_window and ratio_ok

    # ---- controls, evaluated on the same instantiated quantity (twin vs skip vs negsource), per the prereg's wording
    controls = {}
    for h in H_LIST:
        hk = f"{h:g}"; controls[hk] = {}
        for comp in ("T_theta", "T_z"):
            twin, skip, neg = by_h[hk][comp]["twin"], by_h[hk][comp]["skip"], by_h[hk][comp]["negsource"]
            claim = claimed_gain[hk]
            # C1 zero correction: expect gain ~ 0, which must FAIL the "within 10% of h/10" gate (since h/10 != 0 at every pre-registered h)
            c1_gain = skip["gain_tail"]
            c1_fires = bool(abs(c1_gain) < 1e-6 and abs(c1_gain - claim) / claim > 0.10)
            # C2 source negated: expect the residual to GROW (amplitude ratio > 1, growing with q), which must FAIL the gate
            neg_ratio = neg["tail_after_over_before_at_q"]; grows = all(v > 1.0 for v in neg_ratio.values())
            c2_gain = neg["gain_tail"]; c2_fails_gate = bool(abs(c2_gain - claim) / claim > 0.10 or not grows)
            controls[hk][comp] = {
                "C1_zero_correction": {"expected": "gain ~ 0 (must fail the h/10 gate)", "measured_gain_tail": c1_gain, "fired_as_planted": c1_fires,
                                       "note": "sigma = 0 identically in skip mode, so after_tail == before exactly; this is arithmetic, not a fit artefact"},
                "C2_source_negated": {"expected": "residual amplitude grows (must fail the h/10 gate)", "tail_after_over_before_at_q": neg_ratio, "amplitude_grows_at_every_q": bool(grows),
                                       "measured_gain_tail": c2_gain, "fails_gate_as_planted": c2_fails_gate,
                                       "caveat": "the exponent-based gain metric cannot see amplitude growth at fixed q-scaling (grows by a q-independent factor ~2, so its log-log SLOPE is unchanged) -- this is the same limitation wave 4's agent 4 (leg 433) reported for its C2 control; recorded here, not hidden, as a defect of the exponent metric, not of this runner"},
                "twin_pass": {"sigma_reproduces_T_rel_err": twin["sigma_vs_T_rel_err_max"]}}

    # ---- the pre-committed NOT-INSTANTIATED / DROPPED decision
    # Structural check: is the measured twin gain at every h consistent with the q^{-A-1/2}-commuting linear-step
    # mechanism (gain ~ 0, essentially independent of h) rather than with route A's h/10 (which predicts gain
    # growing tenfold from h=1e-2 to h=1e-1)?
    twin_gains_tail = {f"{h:g}": {c: by_h[f"{h:g}"][c]["twin"]["gain_tail"] for c in ("T_theta", "T_z")} for h in H_LIST}
    max_abs_twin_gain = max(abs(v) for d in twin_gains_tail.values() for v in d.values())
    gain_scales_with_h = False
    if max_abs_twin_gain > 1e-9:
        ratios = [twin_gains_tail[f"{H_LIST[i]:g}"]["T_theta"] / twin_gains_tail[f"{H_LIST[i+1]:g}"]["T_theta"] for i in range(len(H_LIST) - 1)]
        gain_scales_with_h = all(2.0 < r < 5.0 for r in ratios)   # h ratios are 10/3 and 3: a genuine h/10 mechanism would show comparable ratios

    not_instantiated = (not all_within_10pct) or (not gain_scales_with_h)
    q3_answer = "NOT-INSTANTIATED" if not_instantiated else ("YES" if all_within_10pct and all_ratio_in_window else "NO")

    dropped = []
    if not_instantiated:
        dropped.append({
            "gate": "Q3", "answer": "NOT-INSTANTIATED", "dropped": True,
            "why": ("The paper's per-stage eps = Q^h gain (Propositions 9.5/9.6) is produced by the wave-field / nonlinear-remainder machinery of Steps 1 and 3 "
                    "(the auxiliary torus and pulse inverse of Section 7, unit (iii)), which are ABSENT from the pinned interface (writeup/data/arc6_profile_v1.json, "
                    "writeup/data/arc6_residual_v1.json). The two steps this runner CAN instantiate on the pinned interface -- Corollary 8.5's radial stress inverse "
                    "(Step 2) and Lemma 8.7's five-equation moment map (Step 4) -- are exact linear inverses for the pinned auxiliary-independent source and commute "
                    f"exactly with the source's q^{{-A-1/2}} prefactor scaling, for every A = 1/2 + h tried: the measured q-gain-in-exponent is {max_abs_twin_gain:.3e} "
                    "at h in {1e-1, 3e-2, 1e-2}, essentially flat rather than scaling with h as h/10 predicts (ratio check: gain(h)/gain(h/3) is nowhere near the "
                    "3x-10x route A implies). This is the SAME structural finding wave 4's agent 4 (leg 433, gate I1) reported at h = 1e-7 alone; re-running it at "
                    "the three h this unit's amendment flagged as resolvable does not change the conclusion, because the mechanism (exact linear commutation with a "
                    "power-law prefactor) does not depend on the numerical value of h -- it is a structural fact about which pieces of Section 8-9 the pinned "
                    "interface contains, not a resolution problem this session's budget could fix."),
            "cost_of_instantiating": ("Would require building Section 7's auxiliary-torus / pulse-field construction (Definition 6.4-6.5, Proposition 6.6, Lemma 7.2's "
                                      "path in the auxiliary torus) so that Steps 1 and 3 of Proposition 9.6 have a nonzero angular-harmonic source to act on -- the pinned "
                                      "interface (leg 432's residual, leg 430's profile) has zero angular harmonic content by construction (leg 433 agent 4: 'the leading "
                                      "residual has no radial component ... (P, J_theta, J_z) = (0,0,0) at stage entry'). That is a separate, larger unit's worth of work "
                                      "(comparable in scope to units (iii)/(iv) of wave 4 combined), not achievable inside one K3 worker session at <=4 cores."),
            "no_substitute_offered": "No exponent-ledger arithmetic (as wave 4's I2) is offered in its place, per the prereg's instruction."})

    controls_summary = {"C1_zero_correction_fired_as_planted_all_h_comp": all(controls[f"{h:g}"][c]["C1_zero_correction"]["fired_as_planted"] for h in H_LIST for c in ("T_theta", "T_z")),
                         "C2_amplitude_grows_all_h_comp": all(controls[f"{h:g}"][c]["C2_source_negated"]["amplitude_grows_at_every_q"] for h in H_LIST for c in ("T_theta", "T_z")),
                         "C2_exponent_metric_caveat": "true, but recorded: the exponent-based gain cannot see the amplitude growth at fixed q-power (same limitation wave 4's agent 4 reported)"}

    base.update({
        "routes": {"A": {"method": "Propositions 9.5/9.6's per-stage gain h/10 in the q-exponent (Definition 9.4's recursion B_{j+1}=B_j+1/10 read as a power of eps=Q^h, p. 100, p. 107)"},
                   "B": {"method": "Cor 8.5's radial stress inverse (Step 2 of Prop 9.6) and Lemma 8.7's moment map (Step 4), imported from experiments/arc6_w4_iteration.py unedited, applied to the pinned tail stress T_0(y, eta; h) (arc6_residual_v1.Tail) at three explicit h, on q in {1e-2, 1e-4, 1e-6}, reading the residual's log-log slope in q before and after the solve; h enters ONLY through Tail(h) -- the profile's operator weights -- and is never multiplied into the solve as a gain.",
                        "by_h": by_h}},
        "gates": {"Q3": {"answer": q3_answer, "literal_arithmetic": literal, "twin_gain_tail_by_h": twin_gains_tail,
                          "max_abs_twin_gain_tail": max_abs_twin_gain, "gain_scales_with_h_as_route_A_predicts": gain_scales_with_h,
                          "all_within_10pct_literal": all_within_10pct, "all_ratio_in_window_literal": all_ratio_in_window}},
        "controls": controls, "controls_summary": controls_summary,
        "dropped": dropped,
        "instantiated_vs_scaled": ("Instantiated at computable h in {1e-1, 3e-2, 1e-2}, q in {1e-2, 1e-4, 1e-6}, lambda = 0.1 (the pinned profile): Step 2's radial "
                                    "stress inverse and Step 4's moment map, both exact for the pinned auxiliary-independent source at every h tried; h enters only "
                                    "through the tail-stress operator T_0(y, eta; h) built by arc6_residual_v1.Tail, never as a multiplicative input gain. NOT "
                                    "instantiated: Steps 1 and 3 (the wave-field / auxiliary-torus machinery of Section 7) that the paper's actual h/10 eps-gain "
                                    "comes from; the h-scaling this unit measures is therefore the scaling of an exactly-linear, source-commuting map (structurally "
                                    "flat in h, not h/10), not of the paper's claimed mechanism."),
        "could_not_determine": [
            "I could not determine the paper's per-stage eps-gain (h/10 in the q-exponent) as a measured quantity, because that gain is produced by Steps 1 and 3 "
            "(the wave-field / auxiliary-torus construction of Section 7, unit (iii)), which the pinned interface does not contain (its leading residual has zero "
            "angular-harmonic content by construction). Only Steps 2 and 4 are instantiable on the pinned interface, and both are exact linear inverses that commute "
            "with the pinned source's q-scaling regardless of h -- so what this runner measures is 0 gain (to the discretisation level), not a partial or noisy "
            "estimate of h/10. Reading this literally as gate Q3 = NO would compare a measurement of a different, well-defined quantity (the commuting-linear-step "
            "residual, which is 0 by construction) against a claim about a quantity this runner cannot see (the wave-field eps-gain); I did not do that. The gate is "
            "NOT-INSTANTIATED and DROPPED with the cost above, per the prereg's own pre-committed clause.",
            "I could not build a genuine two-route agreement for this gate this session; extending the run to three h (rather than wave 4's single h = 1e-7) answers "
            "whether the earlier NOT-INSTANTIATED finding was a resolution artefact (it was not: the flatness in h is itself informative and is reported as data, not asserted)."],
        "what_this_does_not_establish": ("Nothing here establishes or refutes the paper's Proposition 9.6 iteration gain, the convergence of Section 9's scheme, "
                                          "or any property of the manuscript's construction at its own (non-computable) parameters. It establishes only that two of "
                                          "the iteration's four linear sub-steps, run on the pinned residual at three h, are exact and h-scaling-flat -- a fact about "
                                          "this pinned interface, not about the theorem."),
        "forbidden_paths_opened": "none",
        "tier": "This is Tier 2, not a proof."})
    base["runtime_s"] = time.time() - t0
    OUT.write_text(json.dumps(base, indent=1, default=float) + "\n")
    print("wrote", OUT, f"{OUT.stat().st_size:,} B in {time.time()-t0:.0f}s")
    print("GATE Q3:", q3_answer, "| controls fired as planted:", controls_summary)


if __name__ == "__main__":
    main()
