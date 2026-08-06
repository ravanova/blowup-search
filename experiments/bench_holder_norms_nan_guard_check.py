"""BENCH REPAIR CHECK -- solver/holder_norms.py's finiteness/degeneracy guard.

Not a leg.  This is the verification half of the bench repair that added input
validation to `solver/holder_norms.py` after leg 100 (Route-HNA) measured the module
answering confidently and wrongly on NaN/Inf-poisoned and degenerate input.  It answers
three questions, and it re-derives no constant and touches no banked result:

  A. **ZERO REGRESSION, BIT-FOR-BIT.**  On clean, in-window input, is every number the
     patched module returns bit-identical to the number the pre-patch module returned?
     The pre-patch module is loaded straight out of git (`git show <BASE>:solver/
     holder_norms.py`) and imported alongside the patched one under a different name, so
     this is a real A/B against the actual old code, not a re-reading of the new code.
     The guard is supposed to REFUSE input and compute nothing.

  B. **EVERY MEASURED DEFECT CLOSED.**  Leg 100 banked six silent-corruption mechanisms
     with exact magnitudes.  For each, this runs the identical poisoned call against
     both modules and records the wrong number the old one returned next to the
     exception type and message the new one raises.  A seventh case, found while
     repairing and not separated out by leg 100, is included and labelled as such: the
     builtin-`max` hazard at `jacobian_identity_error` line ~130, reachable from a
     REPEATED grid node with no NaN anywhere in the input.

  C. **PRECISION -- the guard must not reject legitimate input.**  A guard that is too
     aggressive is a new, self-inflicted correctness bug sitting on top of a fix, and
     nothing in A would catch it if the over-rejected configuration is not in A's
     battery.  This sweeps a wide grid of VALID configurations -- every (alpha, gamma)
     pair used anywhere in this repository, plus the edges of the legitimate ranges --
     and requires the guard to stay silent, raise nothing, and change no number.

Run: `.venv/bin/python experiments/bench_holder_norms_nan_guard_check.py`
"""

import json
import os
import subprocess
import sys
import types
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from solver import holder_norms as new                                    # noqa: E402

OUT = os.path.join(ROOT, "writeup", "data", "bench_holder_norms_nan_guard_check.json")

# The module BEFORE the guard, pinned by CONTENT-ADDRESSED git blob hash rather than by a
# branch name.  A branch would be wrong here in a way that is easy to miss: `origin/main`
# names the pre-guard module only until this very repair merges, after which the "A/B"
# would compare the patched module against itself and report a vacuous 100% pass.  A blob
# hash cannot drift, survives rebase and branch deletion, and stays reachable through
# history.  This is byte-for-byte the code leg 100 measured.
PREREPAIR_BLOB = "b614a1167ebd1b87fa0f63b0f94ebc63abb3b4d1"
BASE = os.environ.get("BENCH_BASE_REF", PREREPAIR_BLOB)

NAN, INF = float("nan"), float("inf")

# Leg 100's banked magnitudes, transcribed from writeup/data/p2_route_hna_v1_adversarial.json
# and experiments/journal/leg_100.md.  Read, never written.
LEG100 = {
    "conformal_check_clean_128": 1.517287054473293e-04,
    "jacobian_clean_128": 5.058518860e-04,
    "family_op_norm_clean_48": 661.2075718521894,
    "two_vector_clean": 221.978372,
    "two_vector_poisoned": 105.435714,
    "two_vector_understatement": 2.1053,
    "holder_H_random_clean": 0.8914207747116539,
}


def load_prepatch():
    """Import the pre-guard module out of git, alongside the patched one."""
    ref = BASE if ":" in BASE else None
    cmd = (["git", "show", f"{BASE}:solver/holder_norms.py"] if ref
           else ["git", "cat-file", "blob", BASE])
    src = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                         check=True).stdout
    if "_reject_nonfinite" in src:
        raise RuntimeError(
            "the baseline resolved from %r ALREADY CONTAINS the guard, so this would "
            "compare the patched module against itself and report a vacuous pass. Point "
            "BENCH_BASE_REF at the pre-repair blob %s." % (BASE, PREREPAIR_BLOB))
    mod = types.ModuleType("holder_norms_prepatch")
    mod.__dict__["__file__"] = os.path.join(ROOT, "solver", "holder_norms.py")
    exec(compile(src, "<prepatch:solver/holder_norms.py>", "exec"), mod.__dict__)
    return mod, src


def quiet(fn, *a, **kw):
    """Run with warnings and numpy errstate suppressed -- the point is the RETURN VALUE."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            return fn(*a, **kw)


def call(mod, spec):
    """Run one battery case against `mod`; return ('ok', value) or ('raise', type, msg)."""
    try:
        return {"outcome": "value", "value": quiet(spec, mod)}
    except Exception as e:                                     # noqa: BLE001 -- classifying
        return {"outcome": "raise", "type": type(e).__name__, "message": str(e)}


def grid(J, eps=1e-3):
    th = np.linspace(-np.pi + eps, np.pi - eps, J)
    return th, np.tan(0.5 * th)


def jsonify(v):
    if isinstance(v, (list, tuple)):
        return [jsonify(x) for x in v]
    if isinstance(v, np.ndarray):
        return [jsonify(x) for x in v.tolist()]
    if isinstance(v, (np.floating, float)):
        f = float(v)
        return f if np.isfinite(f) else repr(f)
    if isinstance(v, (np.integer, int)):
        return int(v)
    return v


def flatten(v, out):
    """Flatten the ragged (list, float) / (float, float) / array shapes this returns."""
    if isinstance(v, np.ndarray):
        out.extend(float(x) for x in v.ravel())
    elif isinstance(v, (list, tuple)):
        for x in v:
            flatten(x, out)
    else:
        out.append(float(v))
    return out


def same_bits(a, b):
    """Bit-identity, NaN counting as equal to NaN, over the flattened returns."""
    aa, bb = flatten(a, []), flatten(b, [])
    if len(aa) != len(bb):
        return False
    return all(x == y or (np.isnan(x) and np.isnan(y)) for x, y in zip(aa, bb))


# ---------------------------------------------------------------------------
# the CLEAN battery -- every public entry point, on in-window input
# ---------------------------------------------------------------------------

TH128, X128 = grid(128)
TH64, X64 = grid(64)
TH300, X300 = grid(300)
A48 = np.random.default_rng(1).standard_normal((48, 48)) * 0.05
TH48, X48 = grid(48)
H64 = 1.0 / (1.0 + X64 ** 2)

# every (alpha, gamma) pair this repository actually uses, plus the legitimate edges
REPO_PAIRS = [(0.0, 0.5), (1.5, 0.4), (1.5, 0.5), (2.5, 0.5), (1.0, 0.3),
              (0.0, 0.15), (0.0, 0.25), (0.0, 0.35), (0.0, 0.65), (0.0, 0.75),
              (0.0, 0.85), (1.5, 0.05), (1.5, 0.1), (1.5, 0.2), (1.5, 0.65),
              (1.5, 0.8), (1.5, 0.9), (-1.0, 0.5), (3.0, 0.5)]


def clean_cases():
    """(label, fn(mod) -> value) for every entry point, on legitimate input."""
    C = []

    for g in (0.3, 0.5, 0.7):
        C.append((f"conformal_check(J=128, gamma={g})",
                  lambda m, g=g: m.conformal_check(TH128, g)))
    for J in (64, 128, 300):
        C.append((f"jacobian_identity_error(J={J})",
                  lambda m, J=J: m.jacobian_identity_error(grid(J)[0])))
    for nn in (1, 2, 3, 5):
        C.append((f"jacobian_identity_error(J=128, n_near={nn})",
                  lambda m, nn=nn: m.jacobian_identity_error(TH128, n_near=nn)))
    for rs in (0.02, 0.1, 0.5, 2.0):
        C.append((f"jacobian_identity_error(J=128, resolved={rs})",
                  lambda m, rs=rs: m.jacobian_identity_error(TH128, resolved=rs)))
    # the uniform (0, pi) grid experiments/p2_route_d_v5_holder.py uses
    C.append(("jacobian_identity_error(uniform (0,pi) 4000)",
              lambda m: m.jacobian_identity_error(
                  np.pi * (np.arange(4000) + 0.5) / 4000)))

    for a in (-1.0, 0.0, 0.5, 1.5, 3.0):
        C.append((f"decay_weight(alpha={a})",
                  lambda m, a=a: m.decay_weight(X64, a)))

    for a, g in REPO_PAIRS:
        C.append((f"HolderNorm(alpha={a}, gamma={g}) triple",
                  lambda m, a=a, g=g: (lambda n: (n.sup_part(H64), n.seminorm(H64),
                                                  n(H64)))(m.HolderNorm(TH64, X64, a, g))))
    C.append(("HolderNorm(semi_alpha=0, plain) triple",
              lambda m: (lambda n: (n.sup_part(H64), n.seminorm(H64), n(H64)))(
                  m.HolderNorm(TH64, X64, 0.0, 0.5, semi_alpha=0.0))))
    C.append(("HolderNorm(sup_only=True) triple",
              lambda m: (lambda n: (n.sup_part(H64), n.seminorm(H64), n(H64)))(
                  m.HolderNorm(TH64, X64, 1.5, 0.5, sup_only=True))))

    for mdeg in (16, 32, 64, 256):
        C.append((f"square_wave_partial_sum(m={mdeg})",
                  lambda m, mdeg=mdeg: m.square_wave_partial_sum(TH128, mdeg)))

    def fam(m, extra_on, sup_on):
        dn = m.HolderNorm(TH48, X48, 1.0, 0.3)
        cn = m.HolderNorm(TH48, X48, 1.0, 0.3)
        ga = np.exp(-X48 ** 2)
        gb = np.exp(-0.25 * X48 ** 2) * np.cos(TH48)
        ex = [ga, gb] if extra_on else ()
        return m.family_op_norm(A48, dn, cn, extra=ex, include_sup_extremizers=sup_on)

    for eo in (False, True):
        for so in (False, True):
            if not eo and not so:
                continue
            C.append((f"family_op_norm(extra={eo}, sup_extremizers={so})",
                      lambda m, eo=eo, so=so: fam(m, eo, so)))
    # the zero operator: legitimately (0.0, -1), and it must STAY that way
    C.append(("family_op_norm(zero operator) -- legitimately (0.0, -1)",
              lambda m: m.family_op_norm(
                  np.zeros((48, 48)), m.HolderNorm(TH48, X48, 1.0, 0.3),
                  m.HolderNorm(TH48, X48, 1.0, 0.3))))
    # mismatched domain/codomain gradings, as test_op_lower.py builds them
    C.append(("family_op_norm(alpha vs alpha+1 gradings)",
              lambda m: m.family_op_norm(
                  A48, m.HolderNorm(TH48, X48, 1.5, 0.5),
                  m.HolderNorm(TH48, X48, 2.5, 0.5))))

    for g in (0.3, 0.5):
        C.append((f"holder_H_constant(J=128, gamma={g})",
                  lambda m, g=g: m.holder_H_constant(TH128, g, degrees=(4, 16, 64),
                                                     n_random=60)))
    C.append(("holder_H_constant(J=128, gamma=0.3, default degrees, n_random=200)",
              lambda m: m.holder_H_constant(TH128, 0.3)))
    return C


def part_a(old):
    rows, n_same = [], 0
    for label, fn in clean_cases():
        ro, rn = call(old, fn), call(new, fn)
        if ro["outcome"] == "value" and rn["outcome"] == "value":
            ident = same_bits(ro["value"], rn["value"])
        else:
            ident = False
        n_same += bool(ident)
        rows.append({
            "case": label,
            "prepatch": jsonify(ro.get("value")) if ro["outcome"] == "value"
            else f"RAISE {ro['type']}",
            "patched": jsonify(rn.get("value")) if rn["outcome"] == "value"
            else f"RAISE {rn['type']}",
            "bit_identical": bool(ident),
        })
    return {
        "what": ("every public entry point on clean, in-window input, patched vs the "
                 "pre-guard module loaded out of git"),
        "base_ref": BASE,
        "n_cases": len(rows),
        "n_bit_identical": n_same,
        "all_bit_identical": n_same == len(rows),
        "cases": rows,
    }


# ---------------------------------------------------------------------------
# B -- leg 100's six mechanisms, plus the seventh found while repairing
# ---------------------------------------------------------------------------


def defect_cases():
    D = []

    def poisoned_grid(i, val, J=128):
        t = grid(J)[0].copy()
        t[i] = val
        return t

    D.append(("M1 conformal_check on a NaN-poisoned grid node (theta[64])",
              "returned the CLEAN value bit-identically: 1.517287054473293e-04",
              lambda m: m.conformal_check(poisoned_grid(64, NAN), 0.3)))
    D.append(("M1b jacobian_identity_error on the same NaN-poisoned grid",
              "returned the clean 5.058518860e-04 to the last bit",
              lambda m: m.jacobian_identity_error(poisoned_grid(64, NAN))))
    D.append(("M2 conformal_check on an ALL-NaN 16-node grid",
              "returned (0.0, 0.0) -- 0.0 is the value that means EXACT agreement",
              lambda m: m.conformal_check(np.full(16, NAN), 0.3)))

    def op_nan(m, k):
        P = np.where(np.arange(A48.size).reshape(A48.shape) == k, NAN, A48)
        return m.family_op_norm(P, m.HolderNorm(TH48, X48, 1.0, 0.3),
                                m.HolderNorm(TH48, X48, 1.0, 0.3))

    D.append(("M3 family_op_norm with ONE NaN operator entry",
              "collapsed 661.207572 -> exactly 0.0 (arg=-1), a 100% collapse",
              lambda m: op_nan(m, 3 * 48 + 7)))

    def two_vector(m, poison):
        dn = m.HolderNorm(TH48, X48, 1.0, 0.3)
        cn = m.HolderNorm(TH48, X48, 1.0, 0.3)
        ga = np.exp(-X48 ** 2)
        gb = np.exp(-0.25 * X48 ** 2) * np.cos(TH48)
        ra, rb = dn(A48 @ ga) / cn(ga), dn(A48 @ gb) / cn(gb)
        hi, lo = (ga, gb) if ra > rb else (gb, ga)
        if poison:
            hi = hi.copy()
            hi[len(hi) // 2] = NAN
        return m.family_op_norm(A48, dn, cn, extra=[lo, hi],
                                include_sup_extremizers=False)

    D.append(("M4 family_op_norm with a poisoned TRUE MAXIMIZER (the sharpest case)",
              "dropped the maximizer and reported the runner-up: 221.978372 -> "
              "105.435714, a 2.1053x UNDERSTATEMENT of a lower bound",
              lambda m: two_vector(m, True)))

    for lab, tt, gg in (
        ("gamma=NaN", TH128, NAN),
        ("gamma=-0.3", TH128, -0.3),
        ("theta[7]=NaN", poisoned_grid(7, NAN), 0.3),
        ("theta[7]=+Inf", poisoned_grid(7, INF), 0.3),
    ):
        D.append((f"M5 holder_H_constant random arm, {lab}",
                  "random arm returned exactly 0.0 against a clean 0.891421 -- i.e. "
                  "that the Hilbert transform ANNIHILATES the Holder space",
                  lambda m, tt=tt, gg=gg: m.holder_H_constant(
                      tt, gg, degrees=(4, 16, 64), n_random=60)[1]))

    D.append(("M6 conformal_check on an Inf-poisoned grid node (the Inf twin)",
              "returned the clean value, flagged only by an incidental numpy "
              "RuntimeWarning that fires once per source location",
              lambda m: m.conformal_check(poisoned_grid(64, INF), 0.3)))

    # --- the seventh: found while repairing, NOT separated out by leg 100 ---
    def dup_node(J=128):
        t = grid(J)[0].copy()
        t[64] = t[63]
        return t

    D.append(("M7 jacobian_identity_error with a REPEATED grid node (NEW: found "
              "while repairing, no NaN anywhere in the input)",
              "dth=0 gives a 0/0 quotient at offset 1 whose NaN the BUILTIN max "
              "discards, deleting the finest offset: 5.058518860e-04 -> "
              "8.127828757e-04, a 1.6068x change, finite and plausible",
              lambda m: m.jacobian_identity_error(dup_node())))
    D.append(("M7b conformal_check on the same repeated-node grid",
              "1.517287054e-04 -> 2.437655300e-04",
              lambda m: m.conformal_check(dup_node(), 0.3)))
    D.append(("M7c jacobian_identity_error on a DESCENDING grid",
              "dth<0 satisfies |mid|*dth <= resolved for EVERY pair, switching the "
              "resolution restriction off: claimed coverage |X|<=1019.81 against a "
              "true 1.9095, a 534.1x overstatement of the range verified",
              lambda m: m.jacobian_identity_error(grid(128)[0][::-1].copy())))

    D.append(("M8 HolderNorm on a repeated grid node",
              "kernel |th_j-th_k|^{-gamma} becomes +inf at that pair",
              lambda m: (lambda n: n(H64))(
                  m.HolderNorm(np.concatenate([TH64[:63], TH64[62:63]]),
                               np.concatenate([X64[:63], X64[62:63]]), 1.0, 0.3))))
    return D


def part_b(old):
    rows, n_closed = [], 0
    for label, banked, fn in defect_cases():
        ro, rn = call(old, fn), call(new, fn)
        closed = rn["outcome"] == "raise" and rn["type"] == "ValueError"
        n_closed += bool(closed)
        rows.append({
            "mechanism": label,
            "leg100_banked_behaviour": banked,
            "prepatch_returned": jsonify(ro.get("value")) if ro["outcome"] == "value"
            else f"RAISE {ro['type']}: {ro['message'][:120]}",
            "prepatch_was_silent": ro["outcome"] == "value",
            "patched_outcome": f"RAISE {rn['type']}" if rn["outcome"] == "raise"
            else jsonify(rn.get("value")),
            "patched_message": rn.get("message", "")[:400],
            "closed": bool(closed),
        })
    return {
        "what": ("each measured silent-corruption mechanism, run identically against "
                 "both modules"),
        "n_mechanisms": len(rows),
        "n_silent_prepatch": sum(1 for r in rows if r["prepatch_was_silent"]),
        "n_closed": n_closed,
        "all_closed": n_closed == len(rows),
        "mechanisms": rows,
    }


# ---------------------------------------------------------------------------
# C -- precision: the guard must not reject legitimate input
# ---------------------------------------------------------------------------


def part_c():
    """Every VALID configuration must pass the guard silently and unchanged."""
    rows = []

    def ok(label, fn):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                v = fn()
                rows.append({"case": label, "raised": None,
                             "n_warnings": len(caught),
                             "finite": bool(np.all(np.isfinite(flatten(v, []))))})
            except Exception as e:                     # noqa: BLE001 -- classifying
                rows.append({"case": label, "raised": f"{type(e).__name__}: {e}",
                             "n_warnings": len(caught), "finite": None})

    for a, g in REPO_PAIRS:
        ok(f"HolderNorm(alpha={a}, gamma={g})",
           lambda a=a, g=g: new.HolderNorm(TH64, X64, a, g)(H64))
    for g in (1e-6, 0.01, 1.0, 2.0, 5.0):
        ok(f"HolderNorm(gamma={g}) -- extreme but positive",
           lambda g=g: new.HolderNorm(TH64, X64, 1.0, g)(H64))
    for a in (-50.0, -1.0, 0.0, 1.0, 50.0):
        ok(f"HolderNorm(alpha={a}) -- extreme but finite",
           lambda a=a: new.HolderNorm(TH64, X64, a, 0.5)(H64))
    for sa in (-3.0, 0.0, 3.0):
        ok(f"HolderNorm(semi_alpha={sa})",
           lambda sa=sa: new.HolderNorm(TH64, X64, 1.0, 0.5, semi_alpha=sa)(H64))
    for J in (8, 16, 64, 128, 300, 512):
        ok(f"jacobian_identity_error(J={J}) -- coarse to fine",
           lambda J=J: new.jacobian_identity_error(grid(J)[0]))
    for J in (64, 128, 256):
        ok(f"holder_H_constant(J={J}) -- at and above the stated J>=64 precondition",
           lambda J=J: new.holder_H_constant(grid(J)[0], 0.3, degrees=(4, 16),
                                             n_random=20))
    ok("holder_H_constant(J=32, n_random=0) -- coarse grid, per-degree arm only",
       lambda: new.holder_H_constant(grid(32)[0], 0.3, degrees=(4, 16), n_random=0))
    # non-uniform but strictly increasing grids: the guard must not demand uniformity
    ok("jacobian_identity_error(non-uniform strictly increasing grid)",
       lambda: new.jacobian_identity_error(
           np.sort(np.unique(np.concatenate(
               [np.linspace(-3.0, 3.0, 200), np.linspace(-0.5, 0.5, 200)])))))
    ok("HolderNorm(non-uniform grid)",
       lambda: (lambda t: new.HolderNorm(t, np.tan(0.5 * t), 1.0, 0.5)(
           1.0 / (1.0 + np.tan(0.5 * t) ** 2)))(
               np.sort(np.unique(np.concatenate(
                   [np.linspace(-3.0, 3.0, 120), np.linspace(-0.5, 0.5, 120)])))))
    ok("family_op_norm(zero operator) -- legitimately (0.0, -1)",
       lambda: new.family_op_norm(np.zeros((48, 48)),
                                  new.HolderNorm(TH48, X48, 1.0, 0.3),
                                  new.HolderNorm(TH48, X48, 1.0, 0.3))[0])
    ok("family_op_norm(a zero test vector among valid extras)",
       lambda: new.family_op_norm(A48, new.HolderNorm(TH48, X48, 1.0, 0.3),
                                  new.HolderNorm(TH48, X48, 1.0, 0.3),
                                  extra=[np.zeros(48), np.exp(-X48 ** 2)],
                                  include_sup_extremizers=False)[0])

    n_rej = sum(1 for r in rows if r["raised"])
    n_warn = sum(r["n_warnings"] for r in rows)
    return {
        "what": ("valid configurations the guard must NOT reject: every (alpha, gamma) "
                 "pair used in this repository, the edges of the legitimate ranges, "
                 "non-uniform grids, and the legitimate zero-norm paths"),
        "n_cases": len(rows),
        "n_rejected": n_rej,
        "n_warnings_emitted": n_warn,
        "no_false_rejection": n_rej == 0,
        "cases": rows,
    }


def main():
    old, src = load_prepatch()
    prepatch_guards = {
        "n_raise": src.count("raise "),
        "has_isfinite": "isfinite" in src,
        "has_isnan": "isnan" in src,
        "has_warn": "warn" in src,
    }
    pay = {
        "what": "bench repair check: solver/holder_norms.py NaN/Inf/degeneracy guard",
        "not_a_leg": True,
        "base_ref_for_prepatch_module": BASE,
        "prepatch_validation_surface": prepatch_guards,
        "leg100_banked_magnitudes": LEG100,
    }
    pay["A_zero_regression"] = part_a(old)
    print("A: zero-regression A/B done -- %d/%d bit-identical"
          % (pay["A_zero_regression"]["n_bit_identical"],
             pay["A_zero_regression"]["n_cases"]), flush=True)
    pay["B_defects_closed"] = part_b(old)
    print("B: %d/%d mechanisms closed (%d were silent pre-patch)"
          % (pay["B_defects_closed"]["n_closed"],
             pay["B_defects_closed"]["n_mechanisms"],
             pay["B_defects_closed"]["n_silent_prepatch"]), flush=True)
    pay["C_no_false_rejection"] = part_c()
    print("C: %d/%d valid configurations accepted, %d warnings"
          % (pay["C_no_false_rejection"]["n_cases"]
             - pay["C_no_false_rejection"]["n_rejected"],
             pay["C_no_false_rejection"]["n_cases"],
             pay["C_no_false_rejection"]["n_warnings_emitted"]), flush=True)

    a, b, c = (pay["A_zero_regression"], pay["B_defects_closed"],
               pay["C_no_false_rejection"])
    pay["headline"] = {
        "clean_input_bit_identical": a["all_bit_identical"],
        "n_clean_cases": a["n_cases"],
        "n_mechanisms_closed": b["n_closed"],
        "n_mechanisms": b["n_mechanisms"],
        "n_silent_prepatch": b["n_silent_prepatch"],
        "all_mechanisms_closed": b["all_closed"],
        "n_valid_configurations_checked": c["n_cases"],
        "no_false_rejection": c["no_false_rejection"],
        "repair_is_sound": bool(a["all_bit_identical"] and b["all_closed"]
                                and c["no_false_rejection"]),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(pay, fh, indent=2, default=str)
    print("\n" + json.dumps(pay["headline"], indent=2))
    for r in b["mechanisms"]:
        print("  [%s] %s\n        pre-patch: %s" %
              ("CLOSED" if r["closed"] else "OPEN", r["mechanism"],
               r["prepatch_returned"]))
    for r in a["cases"]:
        if not r["bit_identical"]:
            print("  [REGRESSION] %s: %s -> %s" %
                  (r["case"], r["prepatch"], r["patched"]))
    for r in c["cases"]:
        if r["raised"]:
            print("  [FALSE REJECTION] %s: %s" % (r["case"], r["raised"]))
    print(f"\nwrote {OUT}")
    return pay


if __name__ == "__main__":
    main()
