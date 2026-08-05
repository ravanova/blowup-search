"""Route-KA v1 (leg 61): the interval pipeline, pointed at a PUBLISHED certified radius.

WHAT THIS RUNS, AND WHY IT IS NOT ANOTHER INTERNAL CHECK
-----------------------------------------------------------------------------
`capabilities.py`'s `validated` column, for the whole certificate stack, says
internal things: enclosures contain exact rationals, rigorous bounds dominate float
readings, a poisoned iterate is rejected.  Every one of those is the pipeline
agreeing with itself.  Before this leg the stack had never reproduced a certified
radius that somebody else published.

`solver/target_selection.py` looks like a counterexample and is not: it reproduces
Cadiot-Lessard-Nave's Kawahara `r_0` by putting THEIR `Y_0` and THEIR implied `Z_1`
into our radii polynomial.  That checks four lines of algebra.  It does not run the
certificate.

This runner runs the certificate.  `solver/interval_certificate.py` gets the Kawahara
problem at CLN's own truncation (N = 250 cosine modes, half-domain d = 50, Bond number
T = 0.35, speed c = 0.9 -- from `ProofKawahara.jl`, since the paper prints only the
first two), computes `Y_0`, `Z_1`, `Z_2` from scratch in interval arithmetic, and
closes its own radii polynomial.  Then the radius is converted, rigorously, into the
norm CLN quote theirs in, and compared to the window pre-committed in
`writeup/novelty/leg_61.md` BEFORE any of this was built.

THE GATE
-----------------------------------------------------------------------------
"Does `solver/interval_certificate.py`, run end to end on the Kawahara problem,
produce a certified radius inside CLN's published interval at their truncation?"

Two readings are reported, both as magnitudes, because they answer differently and
hiding either one would be a choice dressed up as a result:

  READING A (the gate's words, on the certified SET).  A radii polynomial certifies
  existence at EVERY r in [r_min, r_max].  Reading A asks whether some certified r
  lies inside CLN's published interval [r_0, r_uniq] = [2.27e-14, 1.5e-2].

  READING B (the pre-committed window, on the certified RADIUS r_min).  Reading B
  asks whether r_min itself, converted, lands in that window.  This is the stricter
  one and it is the one written down in advance.

THE ABLATIONS EXIST TO KILL EXPLANATIONS, NOT TO DECORATE
-----------------------------------------------------------------------------
Reading B comes out low, and the leg's job is then to find out why with measurements
rather than paragraphs (standing discipline 85/90).  Two mechanisms were nominated in
advance as the obvious causes, and BOTH ARE FALSIFIED HERE:

  * CLN certify a trace-PROJECTED iterate (`ker T^N_{4,e}`), not the Newton iterate,
    and projection can only raise the residual.  Ablation: do the same projection.
  * CLN's `Y_0` carries the mode-(N, 2N] tail of `u^2`, which our finite Galerkin
    system discards outright.  Ablation: compute that tail and see how big it is.

Neither survives contact with a number.  What is left is reported as what it is.
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.interval_certificate import (  # noqa: E402
    _KAWAHARA_CLN,
    KawaharaIntervals,
    KawaharaProblem,
    interval_constants,
    kawahara_certificate,
    kawahara_norm_conversion,
    kawahara_trace_projection,
    radii_verdict,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_ka_v1_kawahara.json")

# The window, pre-committed in writeup/novelty/leg_61.md before construction.
WINDOW_HL = (_KAWAHARA_CLN["r0_published"], _KAWAHARA_CLN["r_uniqueness_published"])


def decades(x, y):
    """log10(x / y) -- the magnitude this repository reports instead of a boolean."""
    return float(np.log10(x / y))


def quadratic_tail(pr, a):
    """||lam3 (a*a)_n||_{l^2(Z)} over the modes n > N that the Galerkin system drops.

    This is the term CLN's Y_0 carries and ours cannot: their bound includes
    ||U^2 - pi^N U^2||_2, and a finite-dimensional certificate has no such thing.
    Reported in CLN's function-space normalisation (the sqrt(|Omega_0|) factor) so it
    can be compared directly with the gap it is supposed to explain."""
    n = pr.n
    ext = np.zeros(4 * n)
    ext[:n] = a
    m = np.arange(-n + 1, n)
    tail = np.array([float(np.sum(ext[np.abs(m)] * ext[np.abs(k - m)]))
                     for k in range(n, 2 * n)])
    l2 = float(np.sqrt(2.0 * np.sum(tail ** 2)))       # whole-line index set
    return {"max_abs_coefficient": float(np.max(np.abs(tail))),
            "l2_norm_Hl_normalised": float(pr.lam3 * l2 * np.sqrt(2.0 * pr.d))}


def poison(pr, scale):
    """Perturb the iterate and re-run the constants: an over-optimistic certificate
    is one that does not notice.  The perturbation is put on the LOW modes, where the
    profile actually lives, so it is a real displacement and not a tail tickle."""
    a, _ = pr.newton()
    rng = np.random.default_rng(20610)
    bad = a.copy()
    bad[:20] = bad[:20] + scale * rng.standard_normal(20)
    iv = KawaharaIntervals(pr)
    w = pr.weight()
    consts = interval_constants(iv, bad, w, w)
    v = radii_verdict(consts["Y0"], consts["Z1"], consts["Z2"])
    conv = kawahara_norm_conversion(pr)
    return {"scale": float(scale), "Y0": consts["Y0"], "Z1": consts["Z1"],
            "closes": bool(v["closes"]),
            "Y0_over_budget": float(v["Y0_over_budget"]),
            "r_min_Hl": (float(v["r_min"] * conv["to_Hl"]) if v["closes"] else None)}


def main():
    out = {}

    # ---- 1. the run the gate is about -----------------------------------------
    main_run = kawahara_certificate()
    a = main_run.pop("coefficients")
    pr = KawaharaProblem()
    out["published"] = dict(_KAWAHARA_CLN)
    out["main"] = main_run

    # the profile itself, against CLN's Figure 1 -- a check on the SIGN CONVENTION,
    # made before any certificate number is quoted
    x = np.linspace(-pr.d, pr.d, 2001)
    u = a[0] + 2.0 * sum(a[k] * np.cos(k * np.pi * x / pr.d) for k in range(1, pr.n))
    out["profile_check"] = {
        "u_min": float(u.min()),
        "u_min_location": float(x[int(u.argmin())]),
        "u_at_domain_edge": float(abs(u[-1])),
        "cln_figure1_min_read_off": -0.18,
        "kdv_seed_alpha": float(-6.0 / (4.0 * pr.lam3)),
        "kdv_seed_beta": float(np.sqrt(-1.0 / (4.0 * pr.lam1))),
        "coefficient_at_N": float(abs(a[-1])),
    }

    # magnitudes this leg's prose cites from ELSEWHERE, banked here so the note's
    # numbers are all in one file (leg 56's two defects are the reason the gate's
    # RESOLUTION, not just its verdict, has to be reported)
    out["referenced_elsewhere"] = {
        "leg56_H_consistency_defect_x": 1.85e7,
        "leg56_second_defect_x": 2.04e11,
        "source": "leg 56, Route-TN, writeup/4_p2_lottery/TECHNICAL_P2_ROUTETN_V1.md",
    }

    # ---- 2. the two readings of the gate ---------------------------------------
    r_min_hl = main_run["r_min_Hl"]
    r_max_hl = main_run["r_max_Hl"]
    r0, runiq = WINDOW_HL
    reading_a = bool(r_min_hl <= r0 <= r_max_hl)
    reading_b = bool(r0 <= r_min_hl <= runiq)
    out["gate"] = {
        "window_Hl_precommitted": [r0, runiq],
        "certified_interval_Hl": [r_min_hl, r_max_hl],
        "reading_A_published_r0_is_a_certified_radius": reading_a,
        "reading_A_margin_decades_below_r0": decades(r0, r_min_hl),
        "reading_A_margin_decades_above_r0": decades(r_max_hl, r0),
        "reading_B_r_min_inside_window": reading_b,
        "reading_B_shortfall_factor_at_lower_end": float(r0 / r_min_hl),
        "reading_B_shortfall_decades": decades(r0, r_min_hl),
        "reading_B_headroom_decades_at_upper_end": decades(runiq, r_min_hl),
        "window_span_decades": decades(runiq, r0),
        "r_max_over_published_uniqueness": float(r_max_hl / runiq),
    }

    # ---- 3. the constants, side by side ----------------------------------------
    out["constants_vs_published"] = {
        "Y0_ours_Hl": main_run["Y0_Hl"],
        "Y0_published": _KAWAHARA_CLN["Y0_published"],
        "Y0_ratio_published_over_ours": float(_KAWAHARA_CLN["Y0_published"]
                                              / main_run["Y0_Hl"]),
        "Y0_ratio_decades": decades(_KAWAHARA_CLN["Y0_published"], main_run["Y0_Hl"]),
        "A_norm_ours_weighted_sup": main_run["constants"]["A_norm"],
        "DFinv_published_2l": _KAWAHARA_CLN["DFinv_published"],
        "note": ("the two A-norms are in DIFFERENT norms and are not the same "
                 "quantity; the pair is reported for magnitude only"),
        "Z1_ours": main_run["constants"]["Z1"],
        "Z2_ours": main_run["constants"]["Z2"],
        "Y0_over_budget": main_run["verdict"]["Y0_over_budget"],
    }

    # ---- 4. ablation 1: CLN's trace projection ---------------------------------
    proj = kawahara_certificate(trace_project=True)
    proj.pop("coefficients")
    a_proj = kawahara_trace_projection(pr, a)
    out["ablation_trace_projection"] = {
        "Y0_Hl_newton_iterate": main_run["Y0_Hl"],
        "Y0_Hl_trace_projected": proj["Y0_Hl"],
        "ratio": float(proj["Y0_Hl"] / main_run["Y0_Hl"]),
        "displacement_sup_norm": float(np.max(np.abs(a_proj - a))),
        "gap_it_needed_to_explain": float(_KAWAHARA_CLN["Y0_published"]
                                          / main_run["Y0_Hl"]),
        "explains_the_gap": bool(proj["Y0_Hl"] >= _KAWAHARA_CLN["Y0_published"]),
    }

    # ---- 5. ablation 2: the discarded mode-(N, 2N] tail -------------------------
    tail = quadratic_tail(pr, a)
    gap_abs = _KAWAHARA_CLN["Y0_published"] - main_run["Y0_Hl"]
    out["ablation_quadratic_tail"] = dict(tail)
    out["ablation_quadratic_tail"].update({
        "gap_to_explain_absolute": float(gap_abs),
        "tail_over_gap": float(tail["l2_norm_Hl_normalised"] / gap_abs),
        "decades_short": decades(gap_abs, tail["l2_norm_Hl_normalised"]),
        "explains_the_gap": bool(tail["l2_norm_Hl_normalised"] >= gap_abs),
    })

    # ---- 6. resolution sweep: is r_min set by OUR resolution? ------------------
    sweep = []
    for N in (60, 100, 150, 200, 250, 300):
        run = kawahara_certificate(N=N)
        run.pop("coefficients")
        sweep.append({"N": N, "float_residual_sup": run["float_residual_sup"],
                      "Y0": run["constants"]["Y0"], "Z1": run["constants"]["Z1"],
                      "Z2": run["constants"]["Z2"],
                      "closes": run["verdict"]["closes"],
                      "Y0_over_budget": run["verdict"]["Y0_over_budget"],
                      "r_min_Hl": run.get("r_min_Hl"),
                      "conversion_to_Hl": run["conversion"]["to_Hl"]})
    out["resolution_sweep"] = sweep

    # ---- 7. does the certificate notice a displaced iterate? -------------------
    out["poisoning"] = [poison(pr, s) for s in (1e-12, 1e-8, 1e-4)]

    # ---- 8. the conversion, spelled out ----------------------------------------
    out["conversion"] = main_run["conversion"]
    out["conversion"]["what_it_bounds"] = (
        "||a||_{l^2_l} <= sqrt(2N+1) * sup_n(l_n/w_n) * ||a||_w, then "
        "sqrt(|Omega_0|) to CLN's H^l(R) normalisation; both factors round UP, so "
        "every converted radius here is CONSERVATIVE (too large, never too small)")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=float)

    # -- console summary, magnitudes only ---------------------------------------
    print("ROUTE-KA v1 -- the interval pipeline on CLN's Kawahara problem")
    print(f"  truncation      N = {pr.N}, d = {pr.d}, T = {pr.T}, c = {pr.c}")
    print(f"  float residual  {main_run['float_residual_sup']:.3e}")
    print(f"  Y0 {main_run['constants']['Y0']:.4e}   Z1 {main_run['constants']['Z1']:.3e}"
          f"   Z2 {main_run['constants']['Z2']:.4e}")
    print(f"  Y0 / budget     {main_run['verdict']['Y0_over_budget']:.3e}")
    print(f"  certified [r_min, r_max] in H^l : "
          f"[{r_min_hl:.4e}, {r_max_hl:.4e}]")
    print(f"  CLN published interval          : [{r0:.4e}, {runiq:.4e}]")
    print(f"  READING A  published r0 is a certified radius : {reading_a}"
          f"  (margins {out['gate']['reading_A_margin_decades_below_r0']:.2f} /"
          f" {out['gate']['reading_A_margin_decades_above_r0']:.2f} decades)")
    print(f"  READING B  r_min inside the window            : {reading_b}"
          f"  (short by {out['gate']['reading_B_shortfall_factor_at_lower_end']:.2f}x"
          f" = {out['gate']['reading_B_shortfall_decades']:.2f} decades)")
    print(f"  Y0 published / Y0 ours = "
          f"{out['constants_vs_published']['Y0_ratio_published_over_ours']:.2f}x")
    print(f"  ablation trace projection : x"
          f"{out['ablation_trace_projection']['ratio']:.3f}  "
          f"explains gap = {out['ablation_trace_projection']['explains_the_gap']}")
    print(f"  ablation quadratic tail   : "
          f"{tail['l2_norm_Hl_normalised']:.3e}  "
          f"{out['ablation_quadratic_tail']['decades_short']:.2f} decades short  "
          f"explains gap = {out['ablation_quadratic_tail']['explains_the_gap']}")
    for p in out["poisoning"]:
        print(f"  poison {p['scale']:.0e} -> closes {p['closes']}, "
              f"Y0/budget {p['Y0_over_budget']:.3e}")
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
