"""PROG-R4, wave 7 unit R-BANK -- BANK THE SEED FIELDS.

  ####################################################################
  ##  THIS FILE IS COMMITTED BEFORE THE ARTEFACT IT BUILDS.         ##
  ##  The selection-rule EXTENSION, the bit-identity comparator,    ##
  ##  the planted controls and the three gate questions are fixed   ##
  ##  here so that no reading can be chosen after a count exists.   ##
  ####################################################################

THE GATE, in its final wording (`writeup/waves/WAVE7_PLAN.md` SS A, committed
before dispatch and NOT re-scoped here):

    Bank the 160 seed fields the ensemble will use, as a committed artefact
    under experiments/programme_r4/, with a manifest recording for each field:
    the row, the arm, the field index, the snapshot index it came from, the
    selection rule that chose it, and a SHA-256 of the field bytes. Then
    answer, with the numbers:
      (i)   is every field bit-identical to what
            u2_m2_dns_recurrence.regenerate produces from the same snapshot
            index -- YES or NO, over how many of the 160?
      (ii)  re-verify E's 16 original fields against its banked ledger
            specifically, and report that count separately;
      (iii) run one attempt from the banked artefact in a tree with the DNS
            checkpoint absent, and report whether it reproduces E's banked
            result for that attempt BIT FOR BIT.

PRE-COMMITTED READING (fixed before the first count existed): anything short of
160/160 bit-identical means the ensemble DOES NOT LAUNCH from this artefact and
the shortfall is a finding about the re-integration path's determinism, reported
as one and NOT patched around. No tolerance is loosened, nothing is re-seeded,
and whatever the code produces is never written into the manifest and called
identical. Bit-identity here means EXACTLY THAT: byte equality of the IEEE-754
float64 C-order buffer, checked by SHA-256, never `allclose`.

WHY THIS UNIT EXISTS. The seed for every PROG-R4 direct-seed attempt is an
exact re-integration (`u2_m2_dns_recurrence.regenerate`) of one snapshot of
U2's T = 1e5 trajectory. That re-integration needs `u2_dns_ckpt.npy`
(36.9 MB) and the pipeline around it needs `u2_dns_feat.f32` (232 MB) -- both
gitignored, both regenerable only by re-running a 3.4 h DNS, and both already
lost with a container once. The FIELDS THEMSELVES are 24 x 24 float64 =
4,608 bytes each; 160 of them is 737,280 bytes of payload. Banking them turns
a 3.4 h per-shard prerequisite into a `git clone`.

WHAT THIS UNIT DOES NOT DO. It runs no search, moves no wall, and moves no
L1 -> L4 link. Tier 2 is never a proof. It is instrument work: it makes an
existing artefact portable, and portability is not evidence about the object.

SS3k, RULE 3 -- THE EXEMPTION IS STATED, NOT ASSUMED SILENTLY. Rule 3 asks a
construction unit to name the published method it implements. This unit
implements NO published method: it re-executes THIS REPOSITORY'S OWN existing
code (`u2_m2_dns_recurrence.regenerate`, `e_hhard_diagnostic.select_seeds`,
`u5_stratified_attempts.solve_with_stall_exit`) and hashes the bytes that come
out. The only external machinery is SHA-256 (FIPS 180-4) and IEEE-754 binary64,
neither of which is a method this programme could have found already built. No
new external source is relied on, so `writeup/SOURCES.md` gains no row.

THE SELECTION-RULE EXTENSION, fixed here, and its cost stated. `E` drew ONE
field per (row, arm). The ensemble needs TEN. The extension is:

  STAGE 1. Run `e_hhard_diagnostic.select_seeds()` VERBATIM -- imported, not
     copied -- and reserve its 16 snapshots as FIELD INDEX 0 of their (row,
     arm). This is what makes E's 16 originals recoverable from the bank.
  STAGE 2. For rows in TABLE_IV order, arm S before arm Q (E's own nesting),
     draw field indices 1..9 by applying E'S OWN PER-ARM RULE to the anchored
     m = 0 pool with every already-drawn snapshot excluded -- exactly the
     `used` bookkeeping E does, continued.

E's per-arm rule is re-expressed as `_pick()` below because E's `select_seeds()`
is monolithic and cannot be called for a single draw. A RE-EXPRESSION IS A
SECOND REALIZATION UNLESS IT IS CHECKED, so selftest T1 drives `_pick()` through
E's own loop and asserts it reproduces all 16 of E's snapshots, rule strings and
R values. If T1 fails the artefact is not built.

THE ORDERING IS A CHOICE AND IT IS DECLARED. Row-major draw (all 10 of UPO37 S
before any of UPO35 S) lets early rows take contested candidates first; a
round-robin would spread the contention differently. Row-major is chosen because
it is the literal continuation of E's loop, and the manifest records, per field,
whether the |s|-matched subset was still non-empty when that field was drawn, so
the contention is visible rather than assumed away.

Usage:
    .venv/bin/python experiments/programme_r4/r_bank_build.py --build
    .venv/bin/python experiments/programme_r4/r_bank_build.py --verify
    .venv/bin/python experiments/programme_r4/r_bank_build.py --demo-attempt 15
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from solver.kolmogorov2d_nkbasin import Kolmogorov2D  # noqa: E402
from experiments.programme_r4.u2_m2_dns_recurrence import (  # noqa: E402
    CKPT, DT, DT_SAVE, LIB, N_FORCING, N_GRID, RE, regenerate,
)
from experiments.programme_r4 import e_hhard_diagnostic as E  # noqa: E402
from experiments.programme_r4.u5_stratified_attempts import (  # noqa: E402
    wrap_abs,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

BANK = os.path.join(HERE, "seedbank")
FIELDS_NPY = os.path.join(BANK, "seed_fields.npy")
MANIFEST = os.path.join(BANK, "manifest.json")
DEMO_JSON = os.path.join(BANK, "demo_attempt.json")
OUT = os.path.join(ROOT, "writeup", "data", "p2_r_bank_v1.json")

E_LEDGER = os.path.join(HERE, "e_hhard_ledger.json")
E_CURATED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_e_v1.json")

N_ROWS = 8
N_ARMS = 2
N_FIELDS_PER_ARM = 10
N_TOTAL = N_ROWS * N_ARMS * N_FIELDS_PER_ARM      # 160
GRID_BYTES = N_GRID * N_GRID * 8                  # 4608


# ==========================================================================
# BIT-IDENTITY, defined once, used everywhere
# ==========================================================================

def field_sha256(w):
    """SHA-256 of the field bytes: IEEE-754 float64, little-endian, C order.

    This is the ONLY definition of "the field bytes" in this unit. It is not
    a tolerance and it never becomes one."""
    a = np.ascontiguousarray(w, dtype="<f8")
    if a.shape != (N_GRID, N_GRID):
        raise SystemExit(f"field shape {a.shape} != ({N_GRID}, {N_GRID})")
    b = a.tobytes(order="C")
    if len(b) != GRID_BYTES:
        raise SystemExit(f"field byte length {len(b)} != {GRID_BYTES}")
    return hashlib.sha256(b).hexdigest()


def bit_identical(a, b):
    """True iff two fields are byte-equal. Deliberately NOT np.allclose."""
    return (np.ascontiguousarray(a, dtype="<f8").tobytes(order="C")
            == np.ascontiguousarray(b, dtype="<f8").tobytes(order="C"))


# ==========================================================================
# THE SELECTION RULE -- E's, re-expressed for a single draw, checked by T1
# ==========================================================================

def _pick(pool, arm, aps):
    """One draw. Byte-for-byte the branch structure of E's select_seeds().

    Returns (candidate, rule_string, n_shift_matched_available)."""
    if arm == "S":
        near = [c for c in pool
                if abs(wrap_abs(c["s"]) - aps) <= E.MATCH_S_TOL]
        if near:
            c = min(near, key=lambda c: c["R"])
            rule = ("min R among |s|-matched (<= 0.05) anchored "
                    "m=0 candidates")
        else:
            c = min(pool, key=lambda c: abs(wrap_abs(c["s"]) - aps))
            rule = ("no |s|-matched candidate; min | |s|_c - |s|_pub | "
                    "over anchored m=0 candidates")
        return c, rule, len(near)
    c = min(pool, key=lambda c: c["R"])
    return c, "min R among anchored m=0 candidates (U3's own ranking)", None


def _m0_candidates():
    with open(LIB) as f:
        lib = json.load(f)
    return [c for c in lib["candidates"] if c["m"] == 0]


def selftest_T1_pick_reproduces_E():
    """_pick(), driven through E's own loop, must reproduce E's 16 exactly."""
    m0 = _m0_candidates()
    used = set()
    mine = []
    for name, Tp, sp, _mp in E.TABLE_IV:
        aps = wrap_abs(sp)
        anch = [c for c in m0 if abs(c["T"] - Tp) <= E.T_ANCHOR_TOL]
        for arm in ("S", "Q"):
            pool = [c for c in anch if c["snapshot_earlier"] not in used]
            if not pool:
                continue
            c, rule, n_near = _pick(pool, arm, aps)
            used.add(c["snapshot_earlier"])
            mine.append((name, arm, int(c["snapshot_earlier"]), rule,
                         float(c["R"]), n_near))
    theirs = [(j["row"], j["arm"], int(j["snapshot_earlier"]),
               j["selection_rule"], float(j["R_seed"]),
               j["n_shift_matched_available"]) for j in E.select_seeds()]
    return dict(name="T1_pick_reproduces_E_select_seeds",
                n_expected=len(theirs), n_matched=sum(
                    1 for a, b in zip(mine, theirs) if a == b),
                passed=bool(mine == theirs))


def select_seedbank():
    """The 160 metas, in manifest order (row, arm, field_index)."""
    m0 = _m0_candidates()
    originals = E.select_seeds()
    if len(originals) != N_ROWS * N_ARMS:
        raise SystemExit(f"E returned {len(originals)} seeds, expected 16")
    by_key = {}
    for i, j in enumerate(originals):
        by_key[(j["row"], j["arm"])] = [dict(
            j, field_index=0, is_E_original=True, e_attempt_index=i)]
    used = {int(j["snapshot_earlier"]) for j in originals}

    exhausted = []
    for name, Tp, sp, mp_ in E.TABLE_IV:
        aps = wrap_abs(sp)
        anch = [c for c in m0 if abs(c["T"] - Tp) <= E.T_ANCHOR_TOL]
        for arm in ("S", "Q"):
            for k in range(1, N_FIELDS_PER_ARM):
                pool = [c for c in anch if c["snapshot_earlier"] not in used]
                if not pool:
                    exhausted.append(dict(row=name, arm=arm, field_index=k))
                    continue
                c, rule, n_near = _pick(pool, arm, aps)
                used.add(int(c["snapshot_earlier"]))
                by_key[(name, arm)].append(dict(
                    row=name, arm=arm, T_published=Tp, s_published=sp,
                    m_published=mp_, abs_s_published=aps,
                    selection_rule=rule, n_shift_matched_available=n_near,
                    n_anchored_m0=len(anch),
                    R_seed=c["R"], T_candidate=c["T"],
                    abs_s_candidate=wrap_abs(c["s"]),
                    delta_abs_s_candidate_to_published=abs(
                        wrap_abs(c["s"]) - aps),
                    delta_T_candidate_to_published=abs(c["T"] - Tp),
                    candidate_in_newton_window=bool(c["in_newton_window"]),
                    snapshot_earlier=int(c["snapshot_earlier"]),
                    field_index=k, is_E_original=False,
                    e_attempt_index=None))
    metas = []
    for name, _Tp, _sp, _mp in E.TABLE_IV:
        for arm in ("S", "Q"):
            for m in by_key[(name, arm)]:
                metas.append(dict(m, global_index=len(metas)))
    if exhausted:
        raise SystemExit(
            "anchored pool exhausted before 160 fields: "
            f"{exhausted}. This is a SHORTFALL, not something to patch: "
            "report it and stop.")
    if len(metas) != N_TOTAL:
        raise SystemExit(f"{len(metas)} metas, expected {N_TOTAL}")
    snaps = [m["snapshot_earlier"] for m in metas]
    if len(set(snaps)) != N_TOTAL:
        raise SystemExit("snapshot reuse across the 160 -- rule violated")
    return metas


# ==========================================================================
# BUILD
# ==========================================================================

def _solver():
    return Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)


def _regenerate(indices, solver, ckpt_path):
    ckpt = np.load(ckpt_path, mmap_mode="r")
    return regenerate(indices, solver, ckpt, int(round(DT_SAVE / DT)))


def build(args):
    t0 = time.time()
    t1 = selftest_T1_pick_reproduces_E()
    print(f"selftest T1: {t1}")
    if not t1["passed"]:
        raise SystemExit("T1 FAILED -- the re-expressed rule is not E's. "
                         "Artefact NOT built.")
    ckpt_path = args.ckpt or CKPT
    if not os.path.exists(ckpt_path):
        raise SystemExit(f"DNS checkpoint absent at {ckpt_path}; --build is "
                         "the one command that needs it.")
    metas = select_seedbank()
    print(f"selected {len(metas)} seeds; regenerating fields ...", flush=True)
    fields = _regenerate([m["snapshot_earlier"] for m in metas], _solver(),
                         ckpt_path)
    arr = np.stack([np.ascontiguousarray(fields[m["snapshot_earlier"]],
                                         dtype="<f8") for m in metas])
    os.makedirs(BANK, exist_ok=True)
    np.save(FIELDS_NPY, arr, allow_pickle=False)

    entries = []
    for m in metas:
        w = arr[m["global_index"]]
        entries.append(dict(
            global_index=m["global_index"], row=m["row"], arm=m["arm"],
            field_index=m["field_index"],
            snapshot_index=m["snapshot_earlier"],
            selection_rule=m["selection_rule"],
            sha256=field_sha256(w),
            is_E_original=m["is_E_original"],
            e_attempt_index=m["e_attempt_index"],
            T_published=m["T_published"], s_published=m["s_published"],
            m_published=m["m_published"],
            abs_s_published=m["abs_s_published"],
            R_seed=m["R_seed"], T_candidate=m["T_candidate"],
            abs_s_candidate=m["abs_s_candidate"],
            delta_T_candidate_to_published=m[
                "delta_T_candidate_to_published"],
            delta_abs_s_candidate_to_published=m[
                "delta_abs_s_candidate_to_published"],
            candidate_in_newton_window=m["candidate_in_newton_window"],
            n_anchored_m0=m["n_anchored_m0"],
            n_shift_matched_available=m["n_shift_matched_available"]))

    doc = dict(
        unit="R-bank", wave=7, lane="R", programme="PROG-R4",
        what=("the 160 seed fields of the E-FE field ensemble, banked so a "
              "shard never needs the 1.2 GB gitignored DNS artefacts"),
        n_fields=len(entries), grid=N_GRID, dtype="float64",
        byte_order="little-endian", array_order="C",
        bytes_per_field=GRID_BYTES,
        fields_file=os.path.relpath(FIELDS_NPY, ROOT),
        fields_file_sha256=hashlib.sha256(
            open(FIELDS_NPY, "rb").read()).hexdigest(),
        array_shape=list(arr.shape),
        provenance=dict(
            regenerated_by="u2_m2_dns_recurrence.regenerate",
            from_checkpoint=os.path.relpath(ckpt_path, ROOT),
            dns="U2's T = 1e5 trajectory (MILESTONE M2)",
            snapshot_spacing=DT_SAVE, dt=DT, Re=RE, n_forcing=N_FORCING,
            state="real vorticity w(x, y) on a uniform 24 x 24 grid"),
        selection=dict(
            stage_1=("e_hhard_diagnostic.select_seeds(), imported verbatim, "
                     "reserved as field_index 0 of each (row, arm)"),
            stage_2=("E's own per-arm rule continued for field_index 1..9, "
                     "row-major in TABLE_IV order, arm S before arm Q, with "
                     "every already-drawn snapshot excluded"),
            no_snapshot_is_reused=True,
            admission_window_R_lt_0p25_applied=False,
            T_anchor_tol=E.T_ANCHOR_TOL, match_s_tol=E.MATCH_S_TOL),
        selftest_T1=t1,
        build_seconds=round(time.time() - t0, 2),
        fields=entries)
    with open(MANIFEST, "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print(f"wrote {FIELDS_NPY} ({os.path.getsize(FIELDS_NPY)} bytes) and "
          f"{MANIFEST} in {doc['build_seconds']:.1f}s")
    return doc


# ==========================================================================
# LOAD -- what E-FE and any shard call. Touches the seedbank ONLY.
# ==========================================================================

def load_bank():
    with open(MANIFEST) as f:
        man = json.load(f)
    arr = np.load(FIELDS_NPY, allow_pickle=False, mmap_mode=None)
    return man, np.ascontiguousarray(arr, dtype="<f8")


def load_seed(row, arm, field_index=0):
    """The seed field for one (row, arm, field_index). No DNS artefact."""
    man, arr = load_bank()
    for e in man["fields"]:
        if (e["row"] == row and e["arm"] == arm
                and e["field_index"] == field_index):
            w = arr[e["global_index"]]
            if field_sha256(w) != e["sha256"]:
                raise SystemExit(
                    f"seedbank CORRUPT at {row}/{arm}/{field_index}: "
                    "SHA-256 disagrees with the manifest.")
            return w, e
    raise SystemExit(f"no banked field for {row}/{arm}/{field_index}")


# ==========================================================================
# VERIFY
# ==========================================================================

def _gate_i(man, arr, ckpt_path, one_at_a_time=True):
    """Every banked field vs regenerate() from the same snapshot index."""
    solver = _solver()
    n_ok = 0
    mismatches = []
    if one_at_a_time:
        # The SHARD case: one snapshot, one call, no batch context.
        for e in man["fields"]:
            got = _regenerate([e["snapshot_index"]], solver,
                              ckpt_path)[e["snapshot_index"]]
            if bit_identical(got, arr[e["global_index"]]):
                n_ok += 1
            else:
                d = np.abs(np.asarray(got, dtype="<f8")
                           - arr[e["global_index"]])
                mismatches.append(dict(
                    global_index=e["global_index"], row=e["row"],
                    arm=e["arm"], field_index=e["field_index"],
                    snapshot_index=e["snapshot_index"],
                    max_abs_diff=float(d.max()),
                    n_differing_entries=int((d != 0).sum()),
                    sha256_banked=e["sha256"],
                    sha256_regenerated=field_sha256(got)))
    else:
        # The BATCH case: E regenerated all its seeds in ONE call, so batch
        # context is a live confound and is measured, not assumed away.
        got = _regenerate([e["snapshot_index"] for e in man["fields"]],
                          solver, ckpt_path)
        for e in man["fields"]:
            if bit_identical(got[e["snapshot_index"]],
                             arr[e["global_index"]]):
                n_ok += 1
            else:
                mismatches.append(dict(global_index=e["global_index"],
                                       snapshot_index=e["snapshot_index"]))
    return dict(n_checked=len(man["fields"]), n_bit_identical=n_ok,
                answer="YES" if n_ok == len(man["fields"]) else "NO",
                mismatches=mismatches)


def _gate_ii(man, arr):
    """E's 16 originals against E's banked ledger, SPECIFICALLY.

    WHAT THE LEDGER ACTUALLY HOLDS, stated because it bounds this check.
    `e_hhard_ledger.json` is a per-Newton-iteration ledger; it contains NO
    field bytes (`run_attempt` pops `_w0`, and only CONVERGED attempts had
    their state saved, of which there were 2). So bit-identity against the
    LEDGER cannot be byte equality of a field -- it is exact float64 equality
    of the ledger's iteration-0 record, which is a functional of the field:
      residual_before  == seed_extended_residual = ||R(w0, T_pub, s_seeded)||
      T_before         == T_published
      s_before         == s_seeded (the SIGN E measured, not assumed)
    Three exact floats per attempt, recomputed from the BANKED bytes through
    E's own `seed_residual`. A field that differed in one ULP would move
    residual_before. This is the strongest check the banked ledger supports
    and the ceiling is stated rather than papered over."""
    solver = _solver()
    with open(E_LEDGER) as f:
        led = json.load(f)["attempts"]
    with open(E_CURATED) as f:
        cur = json.load(f)["diagnostic_3"]["attempts"]
    by_att = {a["attempt"]: a for a in led}
    cur_by = {a["attempt"]: a for a in cur}
    n_ok = 0
    n_cur_ok = 0
    rows = []
    for e in man["fields"]:
        if not e["is_E_original"]:
            continue
        idx = e["e_attempt_index"]
        rec = by_att[idx]
        it0 = rec["ledger"][0]
        w = arr[e["global_index"]]
        aps = e["abs_s_published"]
        r_plus = E.seed_residual(w, e["T_published"], aps, solver)
        r_minus = E.seed_residual(w, e["T_published"], -aps, solver)
        s0 = aps if r_plus <= r_minus else -aps
        ok_ledger = bool(
            rec["row"] == e["row"] and rec["arm"] == e["arm"]
            and it0["residual_before"] == min(r_plus, r_minus)
            and it0["T_before"] == e["T_published"]
            and it0["s_before"] == s0)
        c = cur_by[idx]
        ok_cur = bool(
            c["snapshot_earlier"] == e["snapshot_index"]
            and c["selection_rule"] == e["selection_rule"]
            and c["R_seed"] == e["R_seed"]
            and c["seed_residual_plus"] == r_plus
            and c["seed_residual_minus"] == r_minus)
        n_ok += ok_ledger
        n_cur_ok += ok_cur
        rows.append(dict(
            e_attempt_index=idx, row=e["row"], arm=e["arm"],
            snapshot_index=e["snapshot_index"],
            ledger_residual_before=it0["residual_before"],
            recomputed_seed_residual=min(r_plus, r_minus),
            exact_float_equal=bool(
                it0["residual_before"] == min(r_plus, r_minus)),
            ulp_gap=(0 if it0["residual_before"] == min(r_plus, r_minus)
                     else abs(it0["residual_before"] - min(r_plus, r_minus))),
            ledger_s_before=it0["s_before"], recomputed_s_seeded=s0,
            ledger_T_before=it0["T_before"],
            ledger_match=ok_ledger, curated_match=ok_cur))
    return dict(
        n_checked=len(rows), n_matching_E_ledger=n_ok,
        n_matching_E_curated_json=n_cur_ok,
        answer="YES" if n_ok == len(rows) else "NO",
        what_the_ledger_supports=(
            "exact float64 equality of the iteration-0 record "
            "(residual_before, T_before, s_before), which is a functional of "
            "the field; the ledger holds NO field bytes, so this is not a "
            "byte comparison and is not reported as one"),
        per_attempt=rows)


def _controls(man, arr):
    """Planted controls that must fire in BOTH directions."""
    w = np.array(arr[0], dtype="<f8")
    sha_true = field_sha256(w)
    pos = dict(name="C_POS_unmodified_field_is_identical",
               expect=True,
               got=bool(bit_identical(w, arr[0])
                        and sha_true == man["fields"][0]["sha256"]))
    # 1 ULP on ONE entry of ONE field. If the comparator cannot see this it is
    # not a bit-identity comparator and every count above is worthless.
    wp = np.array(arr[0], dtype="<f8")
    wp[0, 0] = np.nextafter(wp[0, 0], np.inf)
    neg = dict(name="C_NEG_one_ulp_perturbation_is_caught",
               expect=True,
               perturbation_abs=float(abs(wp[0, 0] - arr[0][0, 0])),
               got=bool((not bit_identical(wp, arr[0]))
                        and field_sha256(wp) != sha_true))
    # A field from a DIFFERENT snapshot must not hash to this one's.
    other = dict(name="C_NEG_distinct_snapshots_have_distinct_hashes",
                 expect=True,
                 got=bool(len({e["sha256"] for e in man["fields"]})
                          == len(man["fields"])))
    return [pos, neg, other]


def verify(args):
    t0 = time.time()
    man, arr = load_bank()
    tests = []

    t1 = selftest_T1_pick_reproduces_E()
    tests.append(t1)

    # T2: manifest SHA-256s recompute from the banked array.
    n_sha = sum(1 for e in man["fields"]
                if field_sha256(arr[e["global_index"]]) == e["sha256"])
    tests.append(dict(name="T2_manifest_sha256_recomputes",
                      n_checked=len(man["fields"]), n_ok=n_sha,
                      passed=n_sha == len(man["fields"])))

    # T3: the artefact has the shape the gate names.
    keys = {(e["row"], e["arm"]) for e in man["fields"]}
    tests.append(dict(
        name="T3_shape_8_rows_x_2_arms_x_10_fields",
        n_fields=len(man["fields"]), n_row_arm_keys=len(keys),
        per_key_counts=sorted({sum(1 for e in man["fields"]
                                   if (e["row"], e["arm"]) == k)
                               for k in keys}),
        n_distinct_snapshots=len({e["snapshot_index"]
                                  for e in man["fields"]}),
        passed=bool(len(man["fields"]) == N_TOTAL and len(keys) == 16
                    and len({e["snapshot_index"]
                             for e in man["fields"]}) == N_TOTAL)))

    # T4: E's 16 are IN the bank, at field_index 0.
    orig = [e for e in man["fields"] if e["is_E_original"]]
    e_snaps = {(j["row"], j["arm"]): int(j["snapshot_earlier"])
               for j in E.select_seeds()}
    tests.append(dict(
        name="T4_E_originals_present_at_field_index_0",
        n_originals=len(orig),
        n_matching_E_select_seeds=sum(
            1 for e in orig
            if e["field_index"] == 0
            and e_snaps.get((e["row"], e["arm"])) == e["snapshot_index"]),
        passed=bool(len(orig) == 16 and all(
            e["field_index"] == 0
            and e_snaps.get((e["row"], e["arm"])) == e["snapshot_index"]
            for e in orig))))

    # T5: the file on disk is the file the manifest hashed.
    fsha = hashlib.sha256(open(FIELDS_NPY, "rb").read()).hexdigest()
    tests.append(dict(name="T5_fields_file_sha256",
                      manifest=man["fields_file_sha256"], on_disk=fsha,
                      passed=fsha == man["fields_file_sha256"]))

    tests.extend(_controls(man, arr))

    ckpt_path = args.ckpt or CKPT
    have_ckpt = os.path.exists(ckpt_path)
    if have_ckpt:
        gi = _gate_i(man, arr, ckpt_path, one_at_a_time=True)
        gi_batch = _gate_i(man, arr, ckpt_path, one_at_a_time=False)
    else:
        gi = dict(n_checked=0, n_bit_identical=0, answer="NOT_RUN",
                  reason=("DNS checkpoint absent at "
                          f"{ckpt_path}; gate (i) is the ONE check that "
                          "needs it, by construction"), mismatches=[])
        gi_batch = dict(answer="NOT_RUN")
    gii = _gate_ii(man, arr)

    demo = None
    if os.path.exists(DEMO_JSON):
        with open(DEMO_JSON) as f:
            demo = json.load(f)

    doc = dict(
        unit="R-bank", wave=7, lane="R", leg=404, programme="PROG-R4",
        kind="reproducibility / instrument",
        what=("bank the 160 E-FE seed fields so no shard needs the 1.2 GB "
              "gitignored DNS artefacts, and prove the banked bytes are the "
              "bytes the re-integration path produces"),
        gate_source="writeup/waves/WAVE7_PLAN.md SS A, on main, final wording",
        artefact=dict(
            fields=os.path.relpath(FIELDS_NPY, ROOT),
            manifest=os.path.relpath(MANIFEST, ROOT),
            bytes_on_disk=os.path.getsize(FIELDS_NPY),
            payload_bytes=N_TOTAL * GRID_BYTES,
            n_fields=len(man["fields"]),
            fields_file_sha256=fsha),
        gate=dict(
            i_bit_identical_to_regenerate=dict(
                question=("is every field bit-identical to what "
                          "u2_m2_dns_recurrence.regenerate produces from the "
                          "same snapshot index?"),
                answer=gi["answer"], n_bit_identical=gi["n_bit_identical"],
                n_checked=gi["n_checked"],
                one_snapshot_per_call=True,
                batch_call_cross_check=dict(
                    answer=gi_batch.get("answer"),
                    n_bit_identical=gi_batch.get("n_bit_identical"),
                    note=("E regenerated all 16 of its seeds in ONE call; a "
                          "shard will call for one. Both are measured so "
                          "batch context is not an untested assumption.")),
                mismatches=gi["mismatches"]),
            ii_E_16_against_E_banked_ledger=dict(
                question=("do E's 16 original fields verify against E's "
                          "banked ledger e_hhard_ledger.json?"),
                answer=gii["answer"],
                n_matching=gii["n_matching_E_ledger"],
                n_checked=gii["n_checked"],
                n_matching_curated_json=gii["n_matching_E_curated_json"],
                ceiling=gii["what_the_ledger_supports"],
                per_attempt=gii["per_attempt"]),
            iii_attempt_without_the_dns_checkpoint=(
                demo if demo else dict(
                    answer="NOT_RUN",
                    note="run --demo-attempt N in a checkout with the DNS "
                         "artefacts removed, then re-run --verify"))),
        selftests=tests,
        clay_movement=dict(
            L1_to_L4_link_moved="none",
            tier="this unit produces no candidate and no certificate; "
                 "Tier 2 is never a proof",
            scale_is_not_evidence=("737 KB of committed fields is a "
                                   "portability fact, not evidence about "
                                   "the Navier-Stokes object")),
        sources_3k=dict(
            rule_3_exemption=("STATED, not assumed: this unit implements no "
                              "published method. It re-executes this "
                              "repository's own code (regenerate, "
                              "select_seeds, solve_with_stall_exit) and "
                              "hashes the output bytes."),
            external_machinery=["SHA-256 (FIPS 180-4)",
                                "IEEE-754 binary64"],
            new_rows_added_to_SOURCES_md=0,
            depth="RECOMPUTED (own code, re-executed and byte-compared)"),
        verify_seconds=round(time.time() - t0, 2))
    return doc


def finalise(doc):
    doc.pop("self_hash", None)
    body = json.dumps(doc, sort_keys=True)
    doc["self_hash"] = hashlib.sha256(body.encode()).hexdigest()[:16]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print(f"wrote {OUT}  self_hash={doc['self_hash']}")
    return doc


# ==========================================================================
# GATE (iii) -- one attempt, from the bank, with the DNS artefacts ABSENT
# ==========================================================================

def demo_attempt(args):
    """Re-run ONE of E's 16 attempts, seeded from the BANK, and compare to
    E's banked ledger bit for bit.

    The point of the unit is exactly this call graph: nothing below opens
    u2_dns_ckpt.npy or u2_dns_feat.f32. The check that it does not is not a
    claim -- it is asserted here, and the run is made in a tree where those
    files do not exist."""
    idx = args.demo_attempt
    with open(E_CURATED) as f:
        cur = {a["attempt"]: a
               for a in json.load(f)["diagnostic_3"]["attempts"]}
    with open(E_LEDGER) as f:
        led = {a["attempt"]: a for a in json.load(f)["attempts"]}
    ref = cur[idx]
    row, arm = ref["row"], ref["arm"]

    for p in (CKPT, os.path.join(HERE, "u2_dns_feat.f32")):
        print(f"  DNS artefact {os.path.basename(p)} present: "
              f"{os.path.exists(p)}")
    dns_absent = not any(os.path.exists(p) for p in
                         (CKPT, os.path.join(HERE, "u2_dns_feat.f32")))

    w0, entry = load_seed(row, arm, 0)
    solver = _solver()
    aps = entry["abs_s_published"]
    r_plus = E.seed_residual(w0, entry["T_published"], aps, solver)
    r_minus = E.seed_residual(w0, entry["T_published"], -aps, solver)
    s0 = aps if r_plus <= r_minus else -aps
    meta = dict(row=row, arm=arm, T_published=entry["T_published"],
                s_published=entry["s_published"],
                m_published=entry["m_published"], abs_s_published=aps,
                snapshot_earlier=entry["snapshot_index"],
                selection_rule=entry["selection_rule"],
                R_seed=entry["R_seed"], T_candidate=entry["T_candidate"],
                abs_s_candidate=entry["abs_s_candidate"],
                delta_abs_s_candidate_to_published=entry[
                    "delta_abs_s_candidate_to_published"],
                delta_T_candidate_to_published=entry[
                    "delta_T_candidate_to_published"],
                candidate_in_newton_window=entry[
                    "candidate_in_newton_window"],
                n_anchored_m0=entry["n_anchored_m0"],
                n_shift_matched_available=entry["n_shift_matched_available"],
                T_seeded=entry["T_published"], s_seeded=s0,
                seed_residual_plus=r_plus, seed_residual_minus=r_minus,
                seed_extended_residual=min(r_plus, r_minus))
    t0 = time.time()
    rec = E.run_attempt((idx, w0, entry["T_published"], s0, meta))
    wall = time.time() - t0
    rec.pop("_w0", None)
    new_led = rec.pop("_ledger")
    old_led = led[idx]["ledger"]

    def _same(a, b):
        return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)

    scalars = ["reason", "success", "final_residual", "n_iters",
               "T_converged", "s_converged", "abs_s_converged",
               "matched_row", "recovered_named_orbit",
               "recovered_any_named_orbit", "krylov_dims", "radius_trials",
               "residual_history", "seed_residual_plus",
               "seed_residual_minus", "s_seeded"]
    cmp_rows = []
    for k in scalars:
        a, b = rec.get(k), ref.get(k)
        cmp_rows.append(dict(field=k, banked=b, reproduced=a,
                             exact_equal=bool(_same(a, b))))
    n_eq = sum(1 for c in cmp_rows if c["exact_equal"])
    led_eq = _same(new_led, old_led)
    n_iter_eq = sum(1 for a, b in zip(new_led, old_led) if _same(a, b))

    out = dict(
        attempt=idx, row=row, arm=arm,
        seeded_from="experiments/programme_r4/seedbank (manifest + npy)",
        dns_artefacts_absent_in_this_tree=dns_absent,
        tree=os.path.abspath(ROOT),
        answer=("YES" if (led_eq and n_eq == len(cmp_rows) and dns_absent)
                else "NO"),
        n_scalar_fields_exact=n_eq, n_scalar_fields_checked=len(cmp_rows),
        per_iteration_ledger_exact=bool(led_eq),
        n_iterations_banked=len(old_led), n_iterations_reproduced=len(new_led),
        n_iterations_byte_equal=n_iter_eq,
        comparison=cmp_rows,
        wall_seconds=round(wall, 1),
        banked_wall_seconds=ref["wall_seconds"],
        note=("bit-for-bit here means exact equality of every banked float, "
              "compared through canonical JSON, not a tolerance"))
    os.makedirs(BANK, exist_ok=True)
    with open(DEMO_JSON, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k != "comparison"},
                     indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--demo-attempt", type=int, default=None)
    ap.add_argument("--ckpt", default=None)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    if args.build:
        build(args)
    if args.demo_attempt is not None:
        demo_attempt(args)
    if args.verify:
        doc = verify(args)
        if args.no_write:
            print(json.dumps(doc["gate"], indent=1)[:4000])
        else:
            finalise(doc)
    if not (args.build or args.verify or args.demo_attempt is not None):
        ap.error("one of --build / --verify / --demo-attempt is required")


if __name__ == "__main__":
    main()
