"""Pre-committed gate for the Stage 3.6 fine-N rough-data exponent measurement
(PLAN.md Stage 3.6 / CLAY_ROADMAP.md Route A, Phase 0).

Reads experiments/stage3_6_sweep.jsonl and answers ONE question, on criteria
frozen before the sweep ran (do not soften mid-run): with genuine Holder-h
rough vorticity near a=1, does the fitted BLOW-UP RATE exponent alpha CONVERGE
as N goes 1024 -> 2048 -> 4096, or does it still RAIL at grid scale (the
Stage 3.5 failure mode)?

Definitions (frozen):
  - An alpha at resolution N is USABLE iff the run blew up, a held-out fit
    exists, and its R^2 >= R2_FLOOR (0.9). An unreliable fit is not a
    measurement of the exponent.
  - RAILING: usable alpha within 1e-6 of a fit-grid edge (0.30 or 3.00) at
    either fine resolution -- the fit is chasing a grid-scale feature.
  - CONVERGED (for one (h, a)): usable at BOTH finest resolutions (2048, 4096),
    not railing, |alpha_4096 - alpha_2048| <= CONV_TOL (0.10 = 2 grid steps),
    and non-expanding across the refinement (the fine step no larger than the
    coarse step, within noise, when 1024 is also usable).
  - NON-GENERIC: |alpha - 1| > NONGENERIC_MARGIN (0.10). A converged alpha~1 is
    just CLM surviving advection (generic), NOT the novel target.

Verdict:
  - a=0.7 is the METHODOLOGICAL CONTROL. The measurement is trusted only if the
    fine-N fit recovers the Stage 3.5 known answer there: converged & generic
    (alpha~1) & resolution-stable for the rough roster. If the control fails,
    the whole probe is INCONCLUSIVE (the fine-N fit is not trustworthy), not a
    rails/converges verdict.
  - CONVERGES (surprise) iff the control passes AND at least one (h, a) with
    a in {0.9, 0.95, 1.0} is CONVERGED and NON-GENERIC -> gCLM not exhausted,
    re-plan before any 2D solver.
  - RAILS (expected) otherwise -> gCLM confirmed exhausted for smooth AND rough
    data at reachable N; carry the method + representation into Phase 1.

Usage: .venv/bin/python analyze_stage3_6.py [path.jsonl]
"""

import json
import sys

R2_FLOOR = 0.9
ALPHA_EDGES = (0.30, 3.00)
CONV_TOL = 0.10             # 2 grid steps: |alpha_4096 - alpha_2048| for "converged"
NONGENERIC_MARGIN = 0.10    # |alpha - 1| beyond this = non-generic
NOISE = 0.05               # exponent-grid step; slack for the contraction test
CONTROL_A = 0.7
TARGET_A = (0.9, 0.95, 1.0)


def load(path):
    table = {}
    for line in open(path):
        if line.strip():
            row = json.loads(line)
            table[(row["ic"]["label"], row["fixed"]["a"],
                   row["resolution_N"])] = row  # newest wins
    return table


def _usable(row):
    if row is None or not row["blowup"] or row["estimate"] is None:
        return None, None, False
    a = row["estimate"]["exponent"]
    r2 = row["estimate"]["r_squared"]
    return a, r2, (r2 >= R2_FLOOR)


def _railing(alpha):
    return alpha is not None and min(abs(alpha - e) for e in ALPHA_EDGES) < 1e-6


def classify(table, label, a, resolutions):
    """Classify one (shape, a) across resolutions. Returns a dict describing
    its convergence behaviour on the exponent axis."""
    rows = {N: table.get((label, a, N)) for N in resolutions}
    usable = {}
    alpha = {}
    for N in resolutions:
        al, _, ok = _usable(rows[N])
        alpha[N] = al
        usable[N] = ok
    res_sorted = sorted(resolutions)
    n_fine, n_top = (res_sorted[-2], res_sorted[-1]) if len(res_sorted) >= 2 \
        else (res_sorted[-1], res_sorted[-1])       # (2048, 4096) in the real run
    welldef_fine = usable[n_fine] and usable[n_top]

    blew_any = any(rows[N] is not None and rows[N]["blowup"] for N in resolutions)
    info = {
        "label": label, "a": a,
        "alpha": alpha, "usable": usable,
        "blew_any": blew_any,
        "welldef_fine": welldef_fine,
        "railing": welldef_fine and (_railing(alpha[n_fine]) or _railing(alpha[n_top])),
        "flip": len({usable[N] for N in resolutions}) > 1,  # usability changes with N
        "d_fine": None, "converged": False, "nongeneric": False,
        "kind": None,
    }
    if not blew_any:
        info["kind"] = "dead"
        return info
    if not welldef_fine:
        info["kind"] = "flip" if info["flip"] else "ill_defined"
        return info
    if info["railing"]:
        info["kind"] = "railing"
        return info

    d_fine = abs(alpha[n_top] - alpha[n_fine])
    info["d_fine"] = d_fine
    contracting = True
    n_coarse = sorted(resolutions)[0]
    if usable[n_coarse]:
        d_coarse = abs(alpha[n_fine] - alpha[n_coarse])
        contracting = d_fine <= d_coarse + NOISE
    info["converged"] = (d_fine <= CONV_TOL) and contracting
    alpha_fine_mean = 0.5 * (alpha[n_fine] + alpha[n_top])
    info["nongeneric"] = abs(alpha_fine_mean - 1.0) > NONGENERIC_MARGIN
    if info["converged"]:
        info["kind"] = "converged_nongeneric" if info["nongeneric"] \
            else "converged_generic"
    else:
        info["kind"] = "unconverged"
    return info


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "experiments/stage3_6_sweep.jsonl"
    table = load(path)
    labels = sorted({k[0] for k in table})
    a_values = sorted({k[1] for k in table})
    resolutions = sorted({k[2] for k in table})

    all_info = {}
    for a in a_values:
        print(f"\n=== rough-data blow-up exponent at a = {a} "
              f"({'CONTROL' if a == CONTROL_A else 'target'}, inviscid) ===")
        hdr = f"{'shape':16s} " + " ".join(f"a@{N:<5d}" for N in resolutions)
        print(hdr + "  kind")
        for label in labels:
            info = classify(table, label, a, resolutions)
            all_info[(label, a)] = info
            cells = []
            for N in resolutions:
                al = info["alpha"][N]
                # '*' only when a fit exists but sits below the R^2 floor;
                # '-' means no blow-up or no fittable tail (al is None).
                mark = "*" if (al is not None and not info["usable"][N]) else ""
                cells.append(f"{'  -  ' if al is None else f'{al:.2f}'}{mark:1s}")
            print(f"{label:16s} " + " ".join(f"{c:>7s}" for c in cells)
                  + f"  {info['kind']}")
        print("  (* = blew up but fit below R^2 floor -> not usable; "
              "'-' = no blow-up / no fit)")

    # --- control check (a = 0.7): must recover generic, stable alpha~1 --------
    ctrl = [all_info[(l, CONTROL_A)] for l in labels
            if (l, CONTROL_A) in all_info]
    ctrl_welldef = [c for c in ctrl if c["welldef_fine"]]
    ctrl_ok_shapes = [c for c in ctrl_welldef
                      if c["converged"] and not c["nongeneric"]]
    control_pass = (len(ctrl_welldef) >= 3
                    and len(ctrl_ok_shapes) >= max(3, len(ctrl_welldef) // 2))

    # --- target check (a near 1): any converged NON-GENERIC exponent? ---------
    surprises = [all_info[(l, a)] for l in labels for a in TARGET_A
                 if (l, a) in all_info
                 and all_info[(l, a)]["kind"] == "converged_nongeneric"]

    print("\n=== STAGE 3.6 GATE ===")
    print(f" control a={CONTROL_A}: {len(ctrl_welldef)} well-defined at fine N, "
          f"{len(ctrl_ok_shapes)} converged & generic (alpha~1) "
          f"-> {'PASS' if control_pass else 'FAIL'}")
    for a in TARGET_A:
        kinds = {}
        for l in labels:
            info = all_info.get((l, a))
            if info:
                kinds[info["kind"]] = kinds.get(info["kind"], 0) + 1
        print(f" target a={a}: " + ", ".join(f"{k}={v}" for k, v in
                                              sorted(kinds.items())))

    print()
    if not control_pass:
        print(" -> INCONCLUSIVE: the fine-N exponent measurement did NOT "
              "recover the known generic alpha~1 at the a=0.7 control, so it "
              "is not trustworthy near a=1. Fix the measurement before ruling "
              "on the gate.")
        return
    if surprises:
        print(" -> CONVERGES (SURPRISE): a resolution-stable NON-GENERIC "
              "blow-up exponent exists near a=1 with rough data:")
        for s in surprises:
            am = 0.5 * (s["alpha"][sorted(resolutions)[-2]]
                        + s["alpha"][sorted(resolutions)[-1]])
            print(f"      {s['label']} at a={s['a']}: alpha~{am:.2f} "
                  f"(|d_fine|={s['d_fine']:.3f})")
        print("    gCLM is NOT exhausted; a novel 1D candidate may be "
              "reachable. STOP and re-plan before building any 2D solver.")
    else:
        print(" -> RAILS (EXPECTED): with the measurement validated at the "
              "a=0.7 control, NO (h, a) near a=1 yields a converged, "
              "non-generic blow-up exponent. Rough data does not change the "
              "Stage 3.5 verdict: gCLM is confirmed exhausted for smooth AND "
              "rough data at reachable N. Carry the rough-data representation "
              "principle + this fine-N method into Phase 1 (2D Boussinesq); a "
              "Phase-0 negative is informative, NOT a kill-signal for Phase 1.")


if __name__ == "__main__":
    main()
