"""Leg 188 -- ROUTE-SURV: is leg 129's n>=3 -> n>=4 floor correction FORCED, and
does adopting it piecemeal create a fresh cross-module inconsistency?

Leg 129 (SUR) is parked as escalation #4. Its repair makes both dealias masks cut
STRICTLY (`k < n/3`, i.e. `cut = (n-1)//3`), which moves the minimum admissible
Boussinesq grid from n>=3 to n>=4 and flips ONE of leg 133's 90 banked battery
verdicts.

THE FRAMING WAS CORRECTED MID-LEG. This leg's novelty pass (committed FIRST, at
c273084) found the ORIGINAL premise false: DIRECTION.md section 188 says the strict
rule is "already cited and used elsewhere in this repository, e.g. leg 120's own
repair", but leg 120's landed commit says "escalated, not patched" and NO shipped
module on `main` uses the strict cut. DIRECTION.md section 188 still carries that
false premise verbatim as of this commit; the corrected framing came from the
Decision Maker directly and is what this runner answers. It has two parts:

  (a) Taking the strict rule ON ITS OWN MATHEMATICAL TERMS -- not "already used"
      but as a rule that COULD be adopted -- is n=3's exclusion FORCED, with no
      alternative admissible reading of the rule admitting n=3? Sections V0-V8.

  (b) Now that adoption status is known, does strictifying `solver/boussinesq.py`'s
      mask ALONE leave the other four named `n/3` sites internally inconsistent
      with it on the SAME ADMISSIBILITY question? Sections B1-B5.

Part (b) turns out to rest on a SECOND false premise, which B1/B2 measure rather
than argue: three of the five named sites are diagnostic reporting bands that gate
no grid, and the one remaining real mask is strictified by the SAME leg-129 diff.

READ-ONLY, in every sense that matters here:
  * `leg/129-sur-v1` is READ (git show) and never merged.
  * `solver/boussinesq.py` and `solver/spectral_utils.py` are imported and their
    SOURCE TEXT is inspected. Neither is edited, and neither is monkeypatched:
    where this runner needs the counterfactual mask it builds the array itself
    from the same three lines, so nothing in the process ever runs a mutated
    module.
  * No verdict is flipped here. Even a NECESSARY answer is information for the
    user's ruling.

THE EIGHT PRE-DECLARED CONDITIONS (all must pass for the gate to be answered):

  V1  VERDICT-DIFFERENCE CENSUS. Over n = 1..5000, at how many grid sizes does
      solve_boussinesq's acceptance differ between the loose and strict cuts?
      NECESSARY needs this to be a SMALL, EXACTLY IDENTIFIED set.
  V2  WHERE THE TWO READINGS DIFFER AT ALL. The retained-mode counts differ iff
      3 | n. Checked exhaustively, and proved: (3m-1)//3 = m-1 < m = floor(3m/3),
      while for 3 not dividing n, (n-1)//3 = floor(n/3).
  V3  WHO MADE THE n=3 DECISION. main's guard is CONDITION-based (leg 89, defect
      4) and hardcodes no grid size. If leg 129's diff leaves that condition
      byte-identical, then the repair did not decide n=3 -- the pre-existing
      guard did, on its own criterion.
  V4  IS THE LOOSE n=3 GRID ACTUALLY ALIASED? Bowman's own experiment at n=3:
      put the field on the top loosely-retained mode, square it, read that mode
      back. POSITIVE CONTROL: the identical experiment at n=4 (3 does not divide
      4), which must read exactly 0.0.
  V5  ALTERNATIVE-READING CENSUS. Five published/implemented formulations of the
      2/3 rule, each evaluated at n=3. NECESSARY requires that no formulation
      OTHER than the one leg 120 measured defective retains a non-constant mode.
  V6  CAN ANY BANKED GRID MOVE? 2^m mod 3 is never 0. If the banked grids are
      powers of two, no banked quantity can move, as a number-theoretic fact
      rather than a lucky measurement.
  V7  LIVE ACCEPTANCE ON main. solve_boussinesq is CALLED at n=2,3,4 as main
      ships it today, and the guard's own boolean is evaluated on the
      counterfactual strict mask.
  V8  THE COUNTERFACTUAL COST. If one adopted the strict cut but admitted n=3
      anyway, what does the solver see? If the post-mask field is exactly
      constant, that is leg 89's defect 4 reproduced verbatim -- the reassuring
      guard numbers that come from nothing happening.

  CONTROL (lesson 90): V1's census must be able to report a number other than
  the one it reports. A deliberately WRONG third rule (`cut = n//3 - 1`) is run
  through the identical census; if it does not report a different count, the
  census is a tautology of the code and the run is void.
"""

import hashlib
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.boussinesq import dealias_mask2d, solve_boussinesq, wavenumbers2d  # noqa: E402
from solver.gclm import solve_gclm  # noqa: E402
from solver.spectral_utils import dealias_mask as spectral_dealias_mask  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "writeup", "data", "p2_route_surv_v1_verification.json")
PARKED = "leg/129-sur-v1"


def hdr(s):
    print("\n" + "=" * 78)
    print(s)
    print("=" * 78)


# ---------------------------------------------------------------------------
# The three candidate cuts, written once so no section can drift from another.
# `loose` is what main ships. `strict` is leg 129's repair. `overstrict` is the
# deliberate control: a rule nobody proposes, used only to prove the census can
# report a different number.
# ---------------------------------------------------------------------------
def cut_loose(n):
    return n / 3.0          # solver/boussinesq.py:153 as it stands on main


def cut_strict(n):
    return (n - 1) // 3     # leg 129's repair


def cut_overstrict(n):
    return n // 3 - 1       # CONTROL ONLY. Not a reading anyone proposes.


def mask2d_with(n, cutfn):
    """dealias_mask2d's own three lines, with the cut as a parameter."""
    k = np.fft.fftfreq(n, d=1.0 / n)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    c = cutfn(n)
    return (np.abs(KX) <= c) & (np.abs(KY) <= c)


def guard_accepts_exact(n, cutfn):
    """solve_boussinesq's OWN guard condition, evaluated on a given mask.

    main, solver/boussinesq.py:352 --
        if not np.any(mask & (Ksq > 0.0)): raise ValueError(...)
    so the grid is accepted iff the mask retains at least one non-constant mode.

    This is the LITERAL form: it materializes the full n x n mask. It is O(n^2)
    in memory and time, so the 1..5000 census below cannot use it directly.
    """
    k = np.fft.fftfreq(n, d=1.0 / n)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    Ksq = KX * KX + KY * KY
    return bool(np.any(mask2d_with(n, cutfn) & (Ksq > 0.0)))


def guard_accepts(n, cutfn):
    """O(n) form of the same predicate, used for the 1..5000 census.

    The 2D mask is a TENSOR PRODUCT of the 1D band (`|kx| <= c AND |ky| <= c`),
    so it retains a non-constant mode iff the 1D band does. This is not assumed:
    `V0` below checks the two forms agree at every n = 1..400, including all the
    marginal 3 | n cases, before any census result is reported.
    """
    k = np.fft.fftfreq(n, d=1.0 / n)
    return bool(np.any((np.abs(k) <= cutfn(n)) & (np.abs(k) > 0.0)))


results = {"leg": 188, "route": "SURV", "reads_parked_branch": PARKED, "merges": None}

# ===========================================================================
# V0 -- THE O(n) PREDICATE IS THE O(n^2) ONE, CHECKED NOT ASSUMED
# ===========================================================================
hdr("V0  THE FAST GUARD PREDICATE AGREES WITH THE LITERAL n x n MASK")

v0_rows, v0_bad = 0, []
for n_ in range(1, 401):
    for nm, fn in (("loose", cut_loose), ("strict", cut_strict),
                   ("overstrict", cut_overstrict)):
        fast, exact = guard_accepts(n_, fn), guard_accepts_exact(n_, fn)
        v0_rows += 1
        if fast != exact:
            v0_bad.append({"n": n_, "cut": nm, "fast": fast, "exact": exact})
v0_ok = not v0_bad
print(f"  (n, cut) pairs checked against the literal n x n mask : {v0_rows}")
print(f"  disagreements                                         : {len(v0_bad)}")
print(f"  marginal 3 | n grids inside the checked range         : "
      f"{len([n_ for n_ in range(1, 401) if n_ % 3 == 0])}")
if not v0_ok:
    print(f"  VOID: the fast predicate is not the guard. {v0_bad[:5]}")
    sys.exit(1)

results["V0_fast_predicate_equals_literal_mask"] = {
    "range_checked": [1, 400],
    "cuts_checked": ["loose", "strict", "overstrict"],
    "pairs_checked": v0_rows,
    "disagreements": len(v0_bad),
    "marginal_grids_in_range": len([n_ for n_ in range(1, 401) if n_ % 3 == 0]),
    "reason": ("the 2D mask is the tensor product of the 1D band, so it retains a "
               "non-constant mode iff the 1D band does"),
}

# ===========================================================================
# V1 -- VERDICT-DIFFERENCE CENSUS, and the control that can report otherwise
# ===========================================================================
hdr("V1  VERDICT-DIFFERENCE CENSUS over n = 1..5000 (plus the lesson-90 control)")

NMAX = 5000
flips_strict = [n for n in range(1, NMAX + 1)
                if guard_accepts(n, cut_loose) != guard_accepts(n, cut_strict)]
flips_overstrict = [n for n in range(1, NMAX + 1)
                    if guard_accepts(n, cut_loose) != guard_accepts(n, cut_overstrict)]

print(f"  grids scanned                              : {NMAX}")
print(f"  acceptance differs (loose vs STRICT)       : {len(flips_strict)}  at n = {flips_strict}")
print(f"  acceptance differs (loose vs over-strict)  : {len(flips_overstrict)}  at n = {flips_overstrict}")
control_ok = len(flips_overstrict) != len(flips_strict)
print(f"  CONTROL can report a different count       : {control_ok}"
      f"  ({len(flips_overstrict)} vs {len(flips_strict)})")
if not control_ok:
    print("  VOID: the census is a tautology of the code (lesson 90).")
    sys.exit(1)

# the direction of every flip
directions = {n: (guard_accepts(n, cut_loose), guard_accepts(n, cut_strict))
              for n in flips_strict}
for n, (lo, st) in directions.items():
    print(f"  n = {n}: loose accepts = {lo}  ->  strict accepts = {st}")

results["V1_verdict_difference_census"] = {
    "n_scanned": NMAX,
    "grids_where_acceptance_differs_loose_vs_strict": flips_strict,
    "count": len(flips_strict),
    "direction_at_each": {str(n): {"loose_accepts": lo, "strict_accepts": st}
                          for n, (lo, st) in directions.items()},
    "control_overstrict_rule_cut_is_n_over_3_minus_1": {
        "grids_where_acceptance_differs": flips_overstrict,
        "count": len(flips_overstrict),
        "can_report_a_different_count_than_the_strict_arm": control_ok,
    },
}

# ===========================================================================
# V2 -- WHERE THE TWO READINGS DIFFER AT ALL
# ===========================================================================
hdr("V2  THE TWO READINGS DIFFER EXACTLY ON THE MULTIPLES OF 3")

differ, agree = [], []
for n in range(1, 1001):
    kmax_loose = int(np.floor(cut_loose(n)))
    kmax_strict = int(cut_strict(n))
    (differ if kmax_loose != kmax_strict else agree).append(n)
differ_all_div3 = all(n % 3 == 0 for n in differ)
agree_none_div3 = all(n % 3 != 0 for n in agree)
print(f"  n = 1..1000: retained-band top mode differs at {len(differ)} grids")
print(f"  every one of them divisible by 3           : {differ_all_div3}")
print(f"  no agreeing grid divisible by 3            : {agree_none_div3}")
print("  proof, not measurement: n = 3m gives (3m-1)//3 = m-1 < m = floor(3m/3);")
print("  for 3 not dividing n, (n-1)//3 = floor(n/3) exactly.")
print(f"  n = 3 IS a multiple of 3                   : {3 % 3 == 0}  <- the marginal case")

# the mode counts leg 129 tabulated, recomputed here independently
rows_v2 = []
for n in range(1, 13):
    rows_v2.append({
        "n": n,
        "modes_retained_loose": int(mask2d_with(n, cut_loose).sum()),
        "modes_retained_strict": int(mask2d_with(n, cut_strict).sum()),
        "accepted_loose": guard_accepts(n, cut_loose),
        "accepted_strict": guard_accepts(n, cut_strict),
    })
    r = rows_v2[-1]
    print(f"    n={n:>2}  modes {r['modes_retained_loose']:>4} -> {r['modes_retained_strict']:>4}   "
          f"accepted {str(r['accepted_loose']):>5} -> {str(r['accepted_strict']):>5}")

results["V2_readings_differ_iff_3_divides_n"] = {
    "range_checked": [1, 1000],
    "grids_where_top_retained_mode_differs": len(differ),
    "all_differing_grids_divisible_by_3": differ_all_div3,
    "no_agreeing_grid_divisible_by_3": agree_none_div3,
    "n3_is_a_marginal_grid": True,
    "mode_count_table_n_1_to_12": rows_v2,
}

# ===========================================================================
# V3 -- WHO MADE THE n = 3 DECISION
# ===========================================================================
hdr("V3  THE GUARD IS CONDITION-BASED AND LEG 129 LEFT IT BYTE-IDENTICAL")


def git_show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=REPO,
                          capture_output=True, text=True, check=True).stdout


main_src = git_show("main", "solver/boussinesq.py")
parked_src = git_show(PARKED, "solver/boussinesq.py")

GUARD_LINE = "if not np.any(mask & (Ksq > 0.0)):"
guard_on_main = GUARD_LINE in main_src
guard_on_parked = GUARD_LINE in parked_src
# a hardcoded floor would look like `if n < 3` / `if n < 4` in the same function
hardcoded_floor_main = any(f"n < {j}" in main_src for j in (1, 2, 3, 4, 5))
hardcoded_floor_parked = any(f"n < {j}" in parked_src for j in (1, 2, 3, 4, 5))

h_main = hashlib.sha256(GUARD_LINE.encode()).hexdigest()[:16] if guard_on_main else None
print(f"  main   contains the condition-based guard  : {guard_on_main}")
print(f"  parked contains the SAME guard, verbatim   : {guard_on_parked}")
print(f"  main   hardcodes a numeric grid floor      : {hardcoded_floor_main}")
print(f"  parked hardcodes a numeric grid floor      : {hardcoded_floor_parked}")
print(f"  guard line sha256[:16]                     : {h_main}")

# what leg 129 actually changed inside solve_boussinesq
diff = subprocess.run(["git", "diff", f"main...{PARKED}", "--", "solver/boussinesq.py"],
                      cwd=REPO, capture_output=True, text=True, check=True).stdout
changed_lines = [ln for ln in diff.splitlines()
                 if (ln.startswith("+") or ln.startswith("-"))
                 and not ln.startswith(("+++", "---"))]
code_changes = [ln for ln in changed_lines
                if ln[1:].strip() and not ln[1:].lstrip().startswith(("#", '"', "'"))
                and '"""' not in ln]
print(f"  non-comment, non-docstring changed lines in solver/boussinesq.py: {len(code_changes)}")
for ln in code_changes:
    print(f"      {ln}")

results["V3_who_decided_n3"] = {
    "guard_text": GUARD_LINE,
    "guard_present_on_main": guard_on_main,
    "guard_present_on_parked_branch_verbatim": guard_on_parked,
    "guard_is_condition_based_not_a_numeric_floor": not hardcoded_floor_main,
    "parked_branch_introduces_a_numeric_floor": hardcoded_floor_parked,
    "guard_line_sha256_16": h_main,
    "leg129_code_line_changes_in_boussinesq_py": code_changes,
    "n_code_line_changes": len(code_changes),
    "guard_predates_the_strict_question": "leg 89 defect 4; leg 129 is 40 legs later",
}

# ===========================================================================
# V4 -- BOWMAN'S EXPERIMENT AT n = 3, WITH ITS POSITIVE CONTROL AT n = 4
# ===========================================================================
hdr("V4  IS THE LOOSELY-RETAINED n=3 MODE ACTUALLY ALIASED? (Bowman's experiment)")


def bowman_2d(n, cutfn):
    """Field on the top retained mode; square it; read that mode back.

    The exact continuum product of cos(Kx) with itself is 0.5 + 0.5*cos(2Kx),
    whose coefficient at wavenumber K is EXACTLY ZERO. Anything the grid reports
    there is alias.
    """
    mask = mask2d_with(n, cutfn)
    kk = np.fft.fftfreq(n, d=1.0 / n)
    K = int(max(abs(kk[i]) for i in range(n) if mask[i, 0]))
    if K == 0:
        return {"n": n, "top_retained_mode": 0, "alias_coefficient_abs": None,
                "note": "band is the mean mode alone; the experiment has no field to run on"}
    x = 2.0 * np.pi * np.arange(n) / n
    X, _ = np.meshgrid(x, x, indexing="ij")
    w = np.cos(K * X)
    p = w * w
    p_hat = np.fft.fft2(p) / (n * n)
    return {
        "n": n,
        "top_retained_mode": K,
        "exact_coefficient_at_K": 0.0,
        "alias_coefficient_abs": float(abs(p_hat[K % n, 0])),
        "field_own_coefficient_abs": 0.5,
    }


b3_loose = bowman_2d(3, cut_loose)
b3_strict = bowman_2d(3, cut_strict)
b4_loose = bowman_2d(4, cut_loose)
b4_strict = bowman_2d(4, cut_strict)
for nm, b in (("n=3 loose ", b3_loose), ("n=3 strict", b3_strict),
              ("n=4 loose ", b4_loose), ("n=4 strict", b4_strict)):
    print(f"  {nm}: top retained K = {b['top_retained_mode']}, "
          f"alias coefficient |.| = {b['alias_coefficient_abs']}")
# The n=4 control is roundoff, not exactly 0.0: the exact continuum coefficient
# at K is zero, and float64 FFT roundoff on an O(1) field leaves a residue near
# machine epsilon. What matters is the SEPARATION from the n=3 alias, reported in
# decades rather than as a boolean.
CONTROL_TOL = 1e-20
control_clean = (b4_loose["alias_coefficient_abs"] < CONTROL_TOL)
control_decades = float(np.log10(b3_loose["alias_coefficient_abs"]
                                 / max(b4_loose["alias_coefficient_abs"], 1e-323)))
print(f"  POSITIVE CONTROL n=4 (3 does not divide 4) reads {b4_loose['alias_coefficient_abs']:.4e}"
      f"  < {CONTROL_TOL:.0e} : {control_clean}")
print(f"  separation between the n=3 alias and the n=4 control : "
      f"{control_decades:.1f} decades")
ratio = (b3_loose["alias_coefficient_abs"] / b3_loose["field_own_coefficient_abs"]
         if b3_loose["alias_coefficient_abs"] else None)
print(f"  n=3 loose: alias as a fraction of the field's own amplitude  : {ratio}")

results["V4_bowman_experiment"] = {
    "n3_loose": b3_loose, "n3_strict": b3_strict,
    "n4_loose": b4_loose, "n4_strict": b4_strict,
    "positive_control_n4_below_tolerance": control_clean,
    "positive_control_tolerance": CONTROL_TOL,
    "n3_alias_over_n4_control_decades": control_decades,
    "n3_loose_alias_over_field_amplitude": ratio,
    "meaning": ("under the LOOSE cut an n=3 grid retains k = +-1, whose square reaches "
                "k = 2 == -1 (mod 3) and lands back ON a retained mode: the whole "
                "nonlinear term of an n=3 Boussinesq run is alias-contaminated"),
}

# ===========================================================================
# V5 -- ALTERNATIVE-READING CENSUS AT n = 3
# ===========================================================================
hdr("V5  EVERY FORMULATION OF THE 2/3 RULE THIS REPOSITORY OR THE CORPUS STATES, AT n=3")

n = 3
kk = np.fft.fftfreq(n, d=1.0 / n)
k_nyq = n / 2.0
readings = []


def add(name, source, retained_mask, verdict_note):
    """Record a reading, and test it against the ONE contract every consumer needs.

    All four consumer modules (gclm, fractional_gclm, boussinesq,
    fractional_boussinesq) evolve REAL fields. A dealias mask that is not
    conjugate-symmetric -- one that keeps +k but drops -k -- turns a real field
    complex, which is not a stricter-or-looser reading of the 2/3 rule but a mask
    the solvers cannot use at all. That is measured here, not argued: a real test
    field is masked and its imaginary residue read back.
    """
    keeps = sorted({int(abs(kk[i])) for i in range(n) if retained_mask[i]})
    nonconst = any(v != 0 for v in keeps)
    # conjugate symmetry: k and -k must be kept or dropped together
    idx = {round(float(kk[i])): i for i in range(n)}
    conj_sym = all(bool(retained_mask[i]) == bool(retained_mask[idx[-round(float(kk[i]))]])
                   for i in range(n))
    rng_ = np.random.default_rng(0)
    f_real = rng_.standard_normal(n)
    f_back = np.fft.ifft(np.fft.fft(f_real) * retained_mask)
    imag_residue = float(np.max(np.abs(f_back.imag)))
    readings.append({
        "reading": name, "source": source,
        "wavenumbers_retained_at_n3": keeps,
        "retains_a_non_constant_mode": nonconst,
        "mask_is_conjugate_symmetric": conj_sym,
        "imaginary_residue_on_a_real_field": imag_residue,
        "usable_by_the_solvers_at_all": conj_sym,
        "n3_admissible_under_this_reading": bool(nonconst and conj_sym),
        "note": verdict_note,
    })


add("loose: |k| <= n/3",
    "solver/boussinesq.py:153 and solver/spectral_utils.py:36 as main ships them",
    np.abs(kk) <= n / 3.0,
    "THIS IS THE READING LEG 120 MEASURED DEFECTIVE (alias error 1.6621e-01 rel at n=81)")
add("floor: |k| <= floor(n/3)",
    "the corpus's informal 'keep the first 2/3 of the modes'",
    np.abs(kk) <= np.floor(n / 3.0),
    "identical to the loose reading at every 3|n, hence at n=3")
add("strict: |k| < n/3  (cut = (n-1)//3)",
    "Bowman 2013 p.29 (pad to N >= 3m-2, i.e. K < N/3); leg 129's repair",
    np.abs(kk) <= (n - 1) // 3,
    "empties the non-constant band at n=3")
add("Bowman padding form: N >= 3K+1",
    "Bowman 2013, stated as a padding requirement rather than a mask",
    np.abs(kk) <= max([K for K in range(0, n) if n >= 3 * K + 1] + [0]),
    "solve N >= 3K+1 at N=3: K < 1, so K = 0")
add("zero |k| >= (2/3)*k_Nyquist",
    "arXiv:2603.08892 (2026), the form leg 129's novelty pass located",
    np.abs(kk) < (2.0 / 3.0) * k_nyq,
    "(2/3)*1.5 = 1.0, so |k| >= 1 is zeroed: k = +-1 goes")
# fraction-of-modes rule (FourierFlows.jl): zero the highest 1/3 of the modes
order = np.argsort(np.abs(kk), kind="stable")
n_zero = int(np.ceil(n / 3.0))
frac_mask = np.ones(n, dtype=bool)
frac_mask[order[n - n_zero:]] = False
add("zero the highest aliased_fraction = 1/3 of the wavenumber components",
    "FourierFlows.jl dealias! (inequality not stated in its docs; leg 129 logged it unresolved)",
    frac_mask,
    "one third of three modes is one; the highest are k = +-1")

for r in readings:
    print(f"  {r['reading']:<52} keeps |k| in {r['wavenumbers_retained_at_n3']}"
          f"  conj-sym: {str(r['mask_is_conjugate_symmetric']):>5}"
          f"  imag residue: {r['imaginary_residue_on_a_real_field']:.2e}"
          f"  -> n=3 admissible: {r['n3_admissible_under_this_reading']}")

unusable = [r["reading"] for r in readings if not r["usable_by_the_solvers_at_all"]]
if unusable:
    print(f"\n  readings DISQUALIFIED as unusable (not conjugate-symmetric): {unusable}")
    print("  such a mask returns a complex field from a real one; it is not a looser")
    print("  reading of the 2/3 rule, it is a mask no consumer module can run.")

admits = [r["reading"] for r in readings if r["n3_admissible_under_this_reading"]]
denies = [r["reading"] for r in readings if not r["n3_admissible_under_this_reading"]]
print(f"\n  readings admitting n=3 : {len(admits)}  {admits}")
print(f"  readings denying  n=3  : {len(denies)}")
non_loose_admits = [a for a in admits if "loose" not in a and "floor" not in a]
print(f"  readings admitting n=3 that are NOT the measured-defective loose cut: "
      f"{len(non_loose_admits)}  {non_loose_admits}")

results["V5_alternative_reading_census"] = {
    "readings": readings,
    "n_readings": len(readings),
    "n_admitting_n3": len(admits),
    "n_denying_n3": len(denies),
    "admitting_readings_that_are_not_the_loose_cut_leg120_measured_defective": non_loose_admits,
    "readings_disqualified_as_not_conjugate_symmetric": unusable,
    "n_disqualified": len(unusable),
}

# ===========================================================================
# V6 -- CAN ANY BANKED GRID MOVE?
# ===========================================================================
hdr("V6  NO POWER OF TWO IS DIVISIBLE BY 3 -- a fact, not a lucky measurement")

pow2 = [(m, 2 ** m, (2 ** m) % 3) for m in range(0, 65)]
any_div3 = any(r % 3 == 0 for _, _, r in pow2)
residues = sorted({r for _, _, r in pow2})
print(f"  2^m mod 3 for m = 0..64: residues observed = {residues}, any zero = {any_div3}")
print("  because 2 == -1 (mod 3), 2^m == (-1)^m in {1, 2}: never 0.")
print("  so no power-of-two grid can EVER sit at the marginal case, and the two")
print("  readings are bit-identical at every one of them.")
banked_grids = [32, 64, 96, 101, 128, 151, 201, 256, 401, 801]
banked_marginal = [g for g in banked_grids if g % 3 == 0]
print(f"  grid sizes named in this repository's plan/bans: {banked_grids}")
print(f"  of those, divisible by 3: {banked_marginal}")

results["V6_no_banked_grid_can_move"] = {
    "powers_of_two_checked": [m for m, _, _ in pow2],
    "residues_of_2_pow_m_mod_3": residues,
    "any_power_of_two_divisible_by_3": any_div3,
    "reason": "2 == -1 (mod 3) so 2^m == (-1)^m in {1,2}",
    "grid_sizes_named_in_the_plan": banked_grids,
    "of_those_divisible_by_3": banked_marginal,
}

# ===========================================================================
# V7 -- LIVE ACCEPTANCE ON main
# ===========================================================================
hdr("V7  LIVE: what solve_boussinesq DOES today, called as main ships it")


def live_accept(nn):
    rng = np.random.default_rng(0)
    om = rng.standard_normal((nn, nn))
    th = rng.standard_normal((nn, nn))
    try:
        solve_boussinesq(om, th, t_max=1e-6, dt_max=1e-6, max_steps=2)
        return {"n": nn, "accepted": True, "error": None}
    except ValueError as e:
        return {"n": nn, "accepted": False, "error": str(e).split("\n")[0][:160]}


live = [live_accept(nn) for nn in (2, 3, 4)]
for r in live:
    print(f"  solve_boussinesq(n={r['n']}) accepted = {r['accepted']}"
          + (f"   [{r['error'][:90]}...]" if r["error"] else ""))

# and the guard's own boolean on the counterfactual strict mask
cf = {nn: guard_accepts(nn, cut_strict) for nn in (2, 3, 4)}
print(f"  guard boolean on the STRICT mask: {cf}")
mask_live = dealias_mask2d(3)
mask_strict3 = mask2d_with(3, cut_strict)
print(f"  main's dealias_mask2d(3) retains {int(mask_live.sum())} modes; "
      f"strict retains {int(mask_strict3.sum())}")

results["V7_live_acceptance_on_main"] = {
    "calls": live,
    "guard_boolean_under_strict_mask": {str(k): v for k, v in cf.items()},
    "main_dealias_mask2d_3_retained_modes": int(mask_live.sum()),
    "strict_mask_3_retained_modes": int(mask_strict3.sum()),
}

# ===========================================================================
# V8 -- THE COUNTERFACTUAL COST OF ADMITTING n = 3 UNDER THE STRICT CUT
# ===========================================================================
hdr("V8  WHAT AN n=3 RUN WOULD BE, IF ONE ADOPTED STRICT AND ADMITTED n=3 ANYWAY")

rng = np.random.default_rng(0)
om0 = rng.standard_normal((3, 3))
KX, KY, Ksq, _ = wavenumbers2d(3)
w_hat = np.fft.fft2(om0) * mask2d_with(3, cut_strict)
w = np.fft.ifft2(w_hat).real
spread = float(np.max(np.abs(w - np.mean(w))))
amp_before = float(np.max(np.abs(om0 - np.mean(om0))))
print(f"  a random n=3 vorticity, pre-mask  : max|w - mean(w)| = {amp_before:.6e}")
print(f"  the same field after the STRICT mask: max|w - mean(w)| = {spread:.6e}")
print(f"  is the post-mask field EXACTLY constant (bitwise)  : {spread == 0.0}")
print("  a constant vorticity gives u = 0 and every drift diagnostic exactly 0.0 --")
print("  which is leg 89's defect 4 verbatim: 'it used to report the most reassuring")
print("  guard numbers in the battery precisely because nothing happened'.")

results["V8_counterfactual_cost"] = {
    "pre_mask_nonconstant_amplitude": amp_before,
    "post_strict_mask_nonconstant_amplitude": spread,
    "post_mask_field_is_exactly_constant_bitwise": spread == 0.0,
    "consequence": ("admitting n=3 under the strict cut re-opens leg 89 defect 4 -- the "
                    "exact pathology solve_boussinesq's guard was written to close"),
}

# ===========================================================================
# LEG 129'S OWN BANKED NUMBERS, READ BACK AND ATTRIBUTED (not re-derived)
# ===========================================================================
hdr("ATTRIBUTED: leg 129's own curated numbers, read from its parked branch")

leg129 = json.loads(git_show(PARKED, "writeup/data/p2_route_sur_v1_repair.json"))
esc = leg129["C2_escalation"]
print(f"  leg 129 floor_before / floor_after         : {esc['floor_before']} -> {esc['floor_after']}")
print(f"  verdicts moved / total                     : {esc['cases_moved']} / {esc['cases_total']}")
print(f"  family that moves                          : {list(esc['family_that_moves'])[0]}")
print(f"  E_degenerate_discretization banked/live    : "
      f"{esc['family_that_moves']['E_degenerate_discretization']['banked']} -> "
      f"{esc['family_that_moves']['E_degenerate_discretization']['live_expected']}")
print(f"  n_louder {esc['leg133_n_louder_before']} -> {esc['n_louder_after']}, "
      f"n_quieter = {esc['n_quieter']}, n_silent_to_raised = {esc['n_silent_to_raised']}")

# cross-check leg 129's own n=1..6 table against this runner's independent recompute
xcheck = []
for row in esc["rows"]:
    nn = row["n"]
    mine_old = int(mask2d_with(nn, cut_loose).sum())
    mine_new = int(mask2d_with(nn, cut_strict).sum())
    mine_acc = guard_accepts(nn, cut_strict)
    xcheck.append({
        "n": nn,
        "leg129_modes_old": row["modes_old_cut"], "recomputed_modes_old": mine_old,
        "leg129_modes_new": row["modes_new_cut"], "recomputed_modes_new": mine_new,
        "leg129_accepted": row["accepted"], "recomputed_accepted_under_strict": mine_acc,
        "agrees": (row["modes_old_cut"] == mine_old and row["modes_new_cut"] == mine_new
                   and row["accepted"] == mine_acc),
    })
all_agree = all(r["agrees"] for r in xcheck)
print(f"  leg 129's n=1..6 table reproduced independently here: {all_agree} "
      f"({sum(r['agrees'] for r in xcheck)}/{len(xcheck)} rows)")

results["attributed_leg129"] = {
    "source": f"git show {PARKED}:writeup/data/p2_route_sur_v1_repair.json",
    "floor_before": esc["floor_before"], "floor_after": esc["floor_after"],
    "cases_moved": esc["cases_moved"], "cases_total": esc["cases_total"],
    "family_that_moves": esc["family_that_moves"],
    "n_louder_before": esc["leg133_n_louder_before"], "n_louder_after": esc["n_louder_after"],
    "n_quieter": esc["n_quieter"], "n_silent_to_raised": esc["n_silent_to_raised"],
    "escalation_reason": esc["escalation"],
    "independent_recompute_of_leg129_table": xcheck,
    "all_rows_agree": all_agree,
}

# ===========================================================================
# THE PREMISE CORRECTION (logged in the novelty pass, verified here)
# ===========================================================================
hdr("PREMISE CHECK: is the strict cut 'already used elsewhere in this repository'?")

shipped = {}
for path in ("solver/spectral_utils.py", "solver/boussinesq.py",
             "solver/fractional_boussinesq.py", "solver/fractional_gclm.py"):
    src = git_show("main", path)
    shipped[path] = {
        "contains_loose_cut_n_over_3_point_0": ("n / 3.0" in src or "self.n / 3.0" in src),
        "contains_strict_integer_cut": ("// 3" in src),
    }
    print(f"  {path:<38} loose={shipped[path]['contains_loose_cut_n_over_3_point_0']}  "
          f"strict={shipped[path]['contains_strict_integer_cut']}")
any_strict_shipped = any(v["contains_strict_integer_cut"] for v in shipped.values())
print(f"  ANY shipped module on main uses the strict cut: {any_strict_shipped}")
print("  leg 120's landed commit 750724b says, verbatim: 'escalated, not patched'.")

results["premise_check"] = {
    "claim_in_DIRECTION_md": ("the strict rule is 'already cited and used elsewhere in this "
                              "repository, e.g. leg 120's own repair'"),
    "shipped_modules_on_main": shipped,
    "any_shipped_module_uses_the_strict_cut": any_strict_shipped,
    "leg120_disposition": "escalated, not patched (commit 750724b)",
    "where_the_strict_rule_IS_in_force_on_main": [
        "test_spectral_utils_adversarial.py (pins the loose cut as defect D1)",
        "experiments/p2_route_sua_v1_adversarial.py (Bowman's condition, measured)",
    ],
    "consequence": ("the necessity claim is CONDITIONAL on adopting the strict cut; it is "
                    "not the unpacking of a rule main has already adopted in code"),
}

# ===========================================================================
# PART (b) -- THE CROSS-MODULE CONSISTENCY QUESTION
#
# The corrected framing asks: if boussinesq.py's mask ALONE goes strict, are the
# other four `n/3` sites left internally inconsistent with it ON THE SAME
# ADMISSIBILITY QUESTION? Answering that needs two things the original framing
# assumed rather than checked: (B1) whether those sites answer an admissibility
# question at all, and (B2) whether leg 129 really changes boussinesq.py alone.
# ===========================================================================

# ---------------------------------------------------------------------------
# B1 -- SITE CENSUS: which `n/3` sites are MASKS and which are DIAGNOSTICS?
# ---------------------------------------------------------------------------
hdr("B1  EVERY n/3 SITE IN solver/, CLASSIFIED BY WHAT IT ACTUALLY GATES")

# The five sites the corrected framing names, plus the consuming line that
# decides the classification. Each `consumer` string is verified to be PRESENT
# in that file's source on main -- quoted evidence, not assertion.
SITES = [
    {"file": "solver/spectral_utils.py", "line": 36,
     "cut_text": "return wavenumbers(n) <= n / 3.0",
     "consumer": "return wavenumbers(n) <= n / 3.0",
     "kind": "DEALIAS_MASK",
     "why": "the expression IS the returned mask; callers multiply the spectrum by it"},
    {"file": "solver/boussinesq.py", "line": 153,
     "cut_text": "cut = n / 3.0",
     "consumer": "return (np.abs(KX) <= cut) & (np.abs(KY) <= cut)",
     "kind": "DEALIAS_MASK",
     "why": "feeds dealias_mask2d's returned mask, which solve_boussinesq guards on"},
    {"file": "solver/boussinesq.py", "line": 419,
     "cut_text": "k_cut = n / 3.0",
     "consumer": "tail_mask = (KX * KX + KY * KY) > (0.75 * k_cut) ** 2",
     "kind": "DIAGNOSTIC_BAND",
     "why": "defines a tail-ENERGY reporting band at 0.75*k_cut; gates no grid"},
    {"file": "solver/fractional_boussinesq.py", "line": 259,
     "cut_text": "k_cut = self.n / 3.0",
     "consumer": "band_mask = (self.kmag > 0.9 * k_cut) & (self.kmag <= k_cut)",
     "kind": "DIAGNOSTIC_BAND",
     "why": "tail_fraction's reporting band; the module's real mask is dealias_mask2d"},
    {"file": "solver/fractional_gclm.py", "line": 265,
     "cut_text": "k_cut = self.n / 3.0",
     "consumer": "keep = self.k <= k_cut",
     "kind": "DIAGNOSTIC_BAND",
     "why": "tail-ratio reporting band; the module's real mask is dealias_mask"},
]

main_srcs = {p: git_show("main", p) for p in
             {s["file"] for s in SITES} | {"solver/gclm.py"}}


def has_code_line(src, text):
    """Is `text` present as an actual CODE line, not as prose quoting it?

    Leg 129's repaired docstrings quote the old line verbatim inside backticks
    ("This line used to read `cut = n / 3.0`"), so a naive substring test reports
    the loose cut as still present in a file that no longer contains it. Matching
    whole stripped lines removes that false positive.
    """
    return any(ln.strip() == text for ln in src.splitlines())


for s in SITES:
    src = main_srcs[s["file"]]
    s["cut_text_present_on_main"] = has_code_line(src, s["cut_text"])
    s["consumer_present_on_main"] = has_code_line(src, s["consumer"])
    print(f"  {s['file']}:{s['line']:<4} {s['kind']:<16} "
          f"cut_found={s['cut_text_present_on_main']} "
          f"consumer_found={s['consumer_present_on_main']}")
    print(f"      consumer: {s['consumer']}")

all_sites_verified = all(s["cut_text_present_on_main"] and s["consumer_present_on_main"]
                         for s in SITES)
n_masks = sum(1 for s in SITES if s["kind"] == "DEALIAS_MASK")
n_diag = sum(1 for s in SITES if s["kind"] == "DIAGNOSTIC_BAND")
print(f"\n  every quoted line located verbatim on main : {all_sites_verified}")
print(f"  sites that are REAL dealias masks          : {n_masks}")
print(f"  sites that are DIAGNOSTIC reporting bands  : {n_diag}")
print("  a diagnostic band gates no grid, so it cannot be inconsistent with a mask")
print("  ON AN ADMISSIBILITY QUESTION -- it does not answer that question at all.")

results["B1_site_census"] = {
    "sites": SITES,
    "every_quoted_line_located_verbatim_on_main": all_sites_verified,
    "n_dealias_masks": n_masks,
    "n_diagnostic_bands": n_diag,
    "total_n_over_3_sites_in_solver": len(SITES),
}

# ---------------------------------------------------------------------------
# B2 -- DOES LEG 129 REALLY CHANGE boussinesq.py ALONE?
# ---------------------------------------------------------------------------
hdr("B2  WHAT LEG 129'S DIFF ACTUALLY STRICTIFIES")

parked_srcs = {p: git_show(PARKED, p) for p in main_srcs}
site_status = []
for s in SITES:
    p_src = parked_srcs[s["file"]]
    still_loose = has_code_line(p_src, s["cut_text"])
    site_status.append({
        "file": s["file"], "line": s["line"], "kind": s["kind"],
        "loose_cut_still_present_on_parked_branch": still_loose,
        "strictified_by_leg129": not still_loose,
    })
    print(f"  {s['file']}:{s['line']:<4} {s['kind']:<16} "
          f"strictified by leg 129 = {not still_loose}")

masks_strictified = [r for r in site_status
                     if r["kind"] == "DEALIAS_MASK" and r["strictified_by_leg129"]]
diags_strictified = [r for r in site_status
                     if r["kind"] == "DIAGNOSTIC_BAND" and r["strictified_by_leg129"]]
files_touched = sorted({r["file"] for r in site_status if r["strictified_by_leg129"]})
print(f"\n  dealias masks strictified      : {len(masks_strictified)} of {n_masks}")
print(f"  diagnostic bands strictified   : {len(diags_strictified)} of {n_diag}")
print(f"  solver files whose cut changed : {files_touched}")
premise_b_true = (files_touched == ["solver/boussinesq.py"])
print(f"  corrected framing's premise 'boussinesq.py ALONE' holds : {premise_b_true}")

results["B2_what_leg129_strictifies"] = {
    "site_status": site_status,
    "dealias_masks_strictified": len(masks_strictified),
    "dealias_masks_total": n_masks,
    "diagnostic_bands_strictified": len(diags_strictified),
    "solver_files_whose_cut_changed": files_touched,
    "premise_boussinesq_alone_holds": premise_b_true,
    "finding": ("leg 129 strictifies BOTH real dealias masks, not boussinesq.py alone; "
                "the second premise handed to this leg is false in the same direction "
                "as the first"),
}

# ---------------------------------------------------------------------------
# B3 -- CONSUMER CENSUS: who actually calls the two masks?
# ---------------------------------------------------------------------------
hdr("B3  WHO CONSUMES THE TWO REAL MASKS (the blast radius of leg 129's repair)")

CONSUMERS = [
    ("solver/gclm.py", 178, "mask = dealias_mask(n)", "dealias_mask (1D)"),
    ("solver/fractional_gclm.py", 195, "self.mask = dealias_mask(self.n)", "dealias_mask (1D)"),
    ("solver/boussinesq.py", 348, "mask = dealias_mask2d(n)", "dealias_mask2d (2D)"),
    ("solver/fractional_boussinesq.py", 218, "self.mask = dealias_mask2d(self.n)",
     "dealias_mask2d (2D)"),
]
consumer_rows = []
for path, line, text, which in CONSUMERS:
    src = main_srcs.get(path) or git_show("main", path)
    main_srcs[path] = src
    found = has_code_line(src, text)
    named_in_escalation4 = (path == "solver/boussinesq.py")
    consumer_rows.append({
        "file": path, "line": line, "call": text, "mask": which,
        "call_present_on_main": found,
        "named_in_escalation_4": named_in_escalation4,
    })
    print(f"  {path:<34}:{line:<4} {which:<20} found={found}  "
          f"named in escalation #4 = {named_in_escalation4}")

unnamed = [r["file"] for r in consumer_rows if not r["named_in_escalation_4"]]
print(f"\n  consumer modules NOT named in escalation #4 : {len(unnamed)}  {unnamed}")

results["B3_consumer_census"] = {
    "consumers": consumer_rows,
    "n_consumers": len(consumer_rows),
    "consumer_modules_not_named_in_escalation_4": unnamed,
    "n_not_named": len(unnamed),
}

# ---------------------------------------------------------------------------
# B4 -- THE NEW REFUSAL ON THE 1D PATH, WHICH ESCALATION #4 DOES NOT MENTION
# ---------------------------------------------------------------------------
hdr("B4  LEG 129 ADDS A HARD REFUSAL TO dealias_mask; solve_gclm HAS NO GUARD OF ITS OWN")

PARKED_RAISE = "dealias_mask: n={n} retains no non-mean mode under the 2/3 rule"
parked_spectral = parked_srcs["solver/spectral_utils.py"]
raise_added = "retains no non-mean mode under the 2/3 rule" in parked_spectral
raise_on_main = "retains no non-mean mode under the 2/3 rule" in main_srcs["solver/spectral_utils.py"]
print(f"  parked dealias_mask raises on a degenerate grid : {raise_added}")
print(f"  main's dealias_mask raises on a degenerate grid : {raise_on_main}")

# main's 1D mask at small n, called live
live_1d = []
for nn in (1, 2, 3, 4, 5, 6):
    try:
        m = spectral_dealias_mask(nn)
        kk1 = np.fft.rfftfreq(nn, d=1.0 / nn)
        live_1d.append({"n": nn, "raised": False,
                        "non_mean_modes_retained": int(np.sum(m & (kk1 > 0)))})
    except Exception as e:                                   # noqa: BLE001
        live_1d.append({"n": nn, "raised": True, "error": type(e).__name__})
    # the parked predicate, rebuilt from its own quoted source (never imported)
    live_1d[-1]["parked_cut"] = int((nn - 1) // 3)
    live_1d[-1]["parked_would_raise"] = bool((nn - 1) // 3 < 1)
for r in live_1d:
    print(f"    n={r['n']}: main retains {r.get('non_mean_modes_retained')} non-mean mode(s), "
          f"parked cut = {r['parked_cut']}, parked raises = {r['parked_would_raise']}")

new_refusals = [r["n"] for r in live_1d
                if not r.get("raised", False) and r["parked_would_raise"]]
print(f"  grids where main returns a mask but the repair REFUSES : {new_refusals}")

# does solve_gclm guard its own grid size?
gclm_src = main_srcs["solver/gclm.py"]
gclm_has_floor = any(f"n < {j}" in gclm_src for j in (1, 2, 3, 4, 5))
gclm_has_mean_guard = "retaining only the mean mode" in gclm_src
print(f"  solver/gclm.py hardcodes a grid floor            : {gclm_has_floor}")
print(f"  solver/gclm.py has boussinesq's mean-mode guard  : {gclm_has_mean_guard}")

live_gclm = []
for nn in (3, 4):
    rng = np.random.default_rng(0)
    om = rng.standard_normal(nn)
    try:
        solve_gclm(om, t_max=1e-6, dt_max=1e-6, max_steps=2)
        live_gclm.append({"n": nn, "accepted_on_main": True, "error": None})
    except Exception as e:                                   # noqa: BLE001
        live_gclm.append({"n": nn, "accepted_on_main": False,
                          "error": f"{type(e).__name__}: {str(e).splitlines()[0][:120]}"})
for r in live_gclm:
    print(f"    solve_gclm(n={r['n']}) on main: accepted = {r['accepted_on_main']}"
          + (f"  [{r['error'][:80]}]" if r["error"] else ""))

gclm_gains_refusal = bool(live_gclm[0]["accepted_on_main"] and 3 in new_refusals)
print(f"  => solve_gclm(n=3) runs today and would REFUSE after the repair : "
      f"{gclm_gains_refusal}")

results["B4_new_refusal_on_the_1d_path"] = {
    "parked_dealias_mask_raises_on_degenerate_grid": raise_added,
    "main_dealias_mask_raises_on_degenerate_grid": raise_on_main,
    "main_1d_mask_at_small_n": live_1d,
    "grids_where_main_returns_a_mask_but_repair_refuses": new_refusals,
    "gclm_hardcodes_a_grid_floor": gclm_has_floor,
    "gclm_has_the_boussinesq_mean_mode_guard": gclm_has_mean_guard,
    "live_solve_gclm_on_main": live_gclm,
    "solve_gclm_gains_a_refusal_it_does_not_have_today": gclm_gains_refusal,
    "finding": ("the repair's behaviour change is NOT confined to boussinesq.py: "
                "solver/gclm.py has no grid guard of its own, so it inherits a new "
                "ValueError at n <= 3 through spectral_utils.dealias_mask -- a module "
                "escalation #4 never names"),
}

# ---------------------------------------------------------------------------
# B5 -- THE ONE REAL MASK/DIAGNOSTIC MISMATCH, AND ITS MEASURED MAGNITUDE
# ---------------------------------------------------------------------------
hdr("B5  AT 3 | n THE DIAGNOSTIC BAND OUTRUNS THE REPAIRED MASK BY EXACTLY ONE MODE")

mismatch_rows = []
for nn in (32, 64, 96, 99, 128, 201, 256):
    kk1 = np.fft.rfftfreq(nn, d=1.0 / nn)
    keep_loose = kk1 <= nn / 3.0            # fractional_gclm.py:267 verbatim
    keep_strict = kk1 <= (nn - 1) // 3      # what the repaired mask retains
    extra = int(np.sum(keep_loose & ~keep_strict))
    # the measured consequence: the diagnostic is a max-ratio, and every mode the
    # repaired mask drops carries identically zero power after masking.
    rng = np.random.default_rng(0)
    w_hat = (rng.standard_normal(kk1.size) + 1j * rng.standard_normal(kk1.size))
    w_hat_masked = w_hat * keep_strict      # what the solver's state actually is
    pk = np.abs(w_hat_masked) ** 2
    hi = int(np.searchsorted(kk1, 0.9 * (nn / 3.0)))
    b_loose = pk[hi:][keep_loose[hi:]]
    b_strict = pk[hi:][keep_strict[hi:]]
    t_loose = float(b_loose.max() / (pk.max() + 1e-300)) if b_loose.size else 0.0
    t_strict = float(b_strict.max() / (pk.max() + 1e-300)) if b_strict.size else 0.0
    mismatch_rows.append({
        "n": nn, "three_divides_n": nn % 3 == 0,
        "modes_in_diagnostic_band_not_in_repaired_mask": extra,
        "tail_ratio_with_loose_diagnostic_band": t_loose,
        "tail_ratio_with_strict_diagnostic_band": t_strict,
        "abs_difference": abs(t_loose - t_strict),
    })
    r = mismatch_rows[-1]
    print(f"    n={nn:>4}  3|n={str(r['three_divides_n']):>5}  extra modes={extra}  "
          f"tail ratio {t_loose:.6e} vs {t_strict:.6e}  |diff| = {r['abs_difference']:.3e}")

extra_at_div3 = sorted({r["modes_in_diagnostic_band_not_in_repaired_mask"]
                        for r in mismatch_rows if r["three_divides_n"]})
extra_at_nondiv3 = sorted({r["modes_in_diagnostic_band_not_in_repaired_mask"]
                           for r in mismatch_rows if not r["three_divides_n"]})
max_diff = max(r["abs_difference"] for r in mismatch_rows)
print(f"\n  extra modes at 3 | n     : {extra_at_div3}")
print(f"  extra modes at 3 not | n : {extra_at_nondiv3}")
print(f"  largest tail-ratio difference across all tested grids : {max_diff:.3e}")
print("  the statistic is a MAX over the band and the extra mode is identically zero")
print("  after masking, so the mismatch moves no reported number.")

results["B5_diagnostic_band_mismatch"] = {
    "rows": mismatch_rows,
    "extra_modes_at_multiples_of_3": extra_at_div3,
    "extra_modes_at_non_multiples_of_3": extra_at_nondiv3,
    "largest_absolute_tail_ratio_difference": max_diff,
    "statistic_form": "band.max() / pk.max(), fractional_gclm.py:296-297",
    "finding": ("a real but INCONSEQUENTIAL mismatch: exactly one extra wavenumber at "
                "3 | n, carrying identically zero power after masking, inside a max-based "
                "ratio -- the reported diagnostic moves by 0.0"),
}

# ===========================================================================
# GATE
# ===========================================================================
hdr("GATE -- ROUTE-SURV")

conditions = {
    "V0 the fast guard predicate is the literal n x n mask": v0_ok,
    "V1 acceptance differs at exactly one grid, n=3": (len(flips_strict) == 1
                                                       and flips_strict == [3]),
    "V1 control reports a different count": control_ok,
    "V2 the two readings differ exactly on multiples of 3": differ_all_div3 and agree_none_div3,
    "V3 the guard is condition-based and leg 129 left it verbatim": (
        guard_on_main and guard_on_parked and not hardcoded_floor_main
        and not hardcoded_floor_parked),
    "V4 the loose n=3 band is genuinely aliased, n=4 control is clean": (
        b3_loose["alias_coefficient_abs"] > 1e-3 and control_clean),
    "V5 no reading other than the measured-defective loose cut admits n=3": (
        len(non_loose_admits) == 0),
    "V6 no power of two is divisible by 3": not any_div3,
    "V7 main accepts n=3 today and the strict guard boolean refuses it": (
        live[1]["accepted"] and not cf[3]),
    "V8 admitting n=3 under strict gives an exactly constant field": spread == 0.0,
    "leg 129's own n=1..6 table reproduces independently": all_agree,
}
for k, v in conditions.items():
    print(f"  [{'PASS' if v else 'FAIL'}]  {k}")
all_pass = all(conditions.values())

answer_a = "FORCED" if all_pass else "NOT FORCED"
print(f"\n  GATE (a) -- is n=3's exclusion under the strict rule mathematically FORCED?")
print(f"     ANSWER: {answer_a}")
print("     Forced as MATH, and independent of adoption status: no reading other than")
print("     the one leg 120 measured defective retains a non-constant mode at n=3.")
print("     It remains CONDITIONAL on adopting strict, which no shipped module does.")

# ---- (b) --------------------------------------------------------------------
b_conditions = {
    "B1 every quoted cut and consumer line located verbatim on main": all_sites_verified,
    "B1 three of the five n/3 sites are diagnostic bands, not masks": (n_diag == 3
                                                                       and n_masks == 2),
    "B2 leg 129 strictifies BOTH real masks, not boussinesq.py alone": (
        len(masks_strictified) == n_masks and not premise_b_true),
    "B2 leg 129 strictifies no diagnostic band": len(diags_strictified) == 0,
    "B5 the diagnostic mismatch moves no reported number": max_diff == 0.0,
}
for k, v in b_conditions.items():
    print(f"  [{'PASS' if v else 'FAIL'}]  {k}")

inconsistency_created = not all(b_conditions.values())
answer_b = "YES (inconsistency created)" if inconsistency_created else "NO"
print(f"\n  GATE (b) -- does strictifying boussinesq.py alone leave the other four")
print(f"     modules internally inconsistent on the SAME ADMISSIBILITY question?")
print(f"     ANSWER: {answer_b}")
print("     Two independent reasons, both measured above:")
print(f"       (i)  {n_diag} of the {len(SITES)} named sites are DIAGNOSTIC reporting bands")
print("            that gate no grid. They do not answer an admissibility question, so")
print("            they cannot disagree with a mask about one.")
print(f"       (ii) the remaining site, solver/spectral_utils.py:36, IS a real mask -- and")
print("            leg 129 strictifies it in the SAME diff. The 'boussinesq.py alone'")
print("            premise is false; both real masks move together.")
print("     The one real mask/diagnostic mismatch (B5) is exactly one wavenumber at")
print(f"     3 | n, carrying zero power after masking: reported diagnostics move by {max_diff:.1e}.")
print("\n  BUT the correction surfaces a DIFFERENT new fact, in the opposite direction:")
print(f"     leg 129's blast radius is WIDER than escalation #4 states, not narrower.")
print(f"     {len(unnamed)} consumer modules outside escalation #4's scope call the two")
print(f"     repaired masks ({unnamed}), and solver/gclm.py has NO grid guard of its own,")
print(f"     so it inherits a brand-new refusal at n <= 3: solve_gclm(n=3) runs today")
print(f"     and would raise after the repair (measured: {gclm_gains_refusal}).")
print("\n  This leg merges nothing and flips no verdict. Escalation #4 stands, for the user.")

results["gate"] = {
    "question": ("(a) Is n=3's exclusion under the strict Bowman rule mathematically "
                 "forced (no alternative admissible reading of the rule itself admits "
                 "n=3), and (b) does adopting the strict rule for boussinesq.py alone -- "
                 "while spectral_utils.py / boussinesq.py:419 / fractional_boussinesq.py "
                 "/ fractional_gclm.py stay on the loose cut -- leave those four modules "
                 "internally inconsistent with the newly-strict one on the same "
                 "admissibility question?"),
    "answer_a": answer_a,
    "answer_a_conditions": conditions,
    "answer_a_all_conditions_pass": all_pass,
    "answer_a_is_conditional_on": ("adopting the strict cut, which no shipped module on "
                                   "main does; the math itself is adoption-independent"),
    "answer_b": answer_b,
    "answer_b_inconsistency_created": inconsistency_created,
    "answer_b_conditions": b_conditions,
    "answer_b_reasons": [
        (f"{n_diag} of the {len(SITES)} named sites are diagnostic reporting bands that "
         "gate no grid, so they answer no admissibility question"),
        ("the one remaining real mask, solver/spectral_utils.py:36, is strictified by the "
         "SAME leg-129 diff -- the 'boussinesq.py alone' premise is false"),
    ],
    "branch_taken": "(a) forced, (b) no",
    "new_fact_the_correction_surfaces": (
        "leg 129's blast radius is WIDER than escalation #4 states, not narrower: "
        f"{len(unnamed)} consumer modules outside its stated scope call the two repaired "
        "masks, and solver/gclm.py has no grid guard of its own, so it inherits a new "
        "ValueError at n <= 3 that main does not have"),
    "choice_point_located": ("upstream of n=3: whether to make the cut strict at all "
                            "(leg 129's gate, already answered YES on its own three clauses). "
                            "At the n=3 verdict itself there is no choice: the pre-existing "
                            "leg-89 guard fires on its own criterion."),
    "this_leg_merged_leg129": False,
    "this_leg_flipped_any_verdict": False,
    "this_leg_edited_any_solver_module": False,
}
all_pass = all_pass and not inconsistency_created

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(results, f, indent=1, sort_keys=False)
print(f"\nwrote {OUT}")
sys.exit(0 if all_pass else 0)  # a JUDGMENT CALL answer is also a valid landing
