"""Route-DFRE (fig74): the standing CAP-reproduction lane's FIRST ENTRY.

Legs 61 and 256 are two for two at finding real issues in published verification
packages; the steer makes it a lane -- one published computer-assisted proof reproduced
per cycle, in leg 256's shape, under leg 256's attribution rule. First entry: DF-CGL
(Dahne-Figueras, arXiv:2410.05480).

WHAT THIS LEG IS NOT.  Leg 48 (Route-V v0) already used this paper once, to close stage
V's novelty gate, by re-deriving their BRANCH/FOLD/ZEROS from the paper's own EQUATIONS
in float64.  This leg does something different: it decodes DF's own RELEASED PROOF-WITNESS
DATA (github.com/Joel-Dahne/CGL.jl, pinned at the exact commit their paper cites) and
independently checks, in EXACT RATIONAL ARITHMETIC (no Arb, no Julia, no CAPD -- none are
in this environment), whether that released data satisfies the box-chaining inclusion
condition their own Theorem 4.1 / Section 6 states is what makes the proof's boxes
constitute one continuous curve of solutions.  See writeup/novelty/leg_316.md for the ban
check, the pre-committed window, and why this is external validation, not a re-opening of
stage V.

THE ARB DUMP FORMAT (arf_dump_str / mag_dump_str / arb_dump_str, read from Arb's own C
source, arb/{arf,mag,arb}/dump_str.c): a ball is "mid_mantissa_hex mid_exponent_hex
rad_mantissa_hex rad_exponent_hex", each an exact dyadic number `mantissa * 2**exponent`
(mantissa==0 with exponent==0 means exactly zero; other zero-mantissa exponents are the
special values +-inf/nan, which this decoder rejects rather than silently mishandles).
Decoding into fractions.Fraction makes every comparison below EXACT -- not a float64
approximation of their output, an exact re-derivation of what interval each ball spans.

Deterministic. Network used once, to `git clone` the pinned public commit (a few MB,
cached under Papers/, which is entirely gitignored -- nothing of theirs is ever committed).
Estimated cost before running (recorded per the standing performance rule): ~49,465 CSV
rows for branch d=1,j=1 (top 6588 + turn 33281 + bottom 9596), pure hex/Fraction parsing,
O(1) work per row -- low tens of seconds at most, no vectorisation needed. Measured wall
time is written into the output JSON.

Writes writeup/data/p2_route_dfre_v1.json.
"""

import hashlib
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "writeup" / "data"
CACHE = ROOT / "Papers" / "_cgl_jl_cache"  # Papers/* is gitignored (see .gitignore); nothing here is ever committed
OUT = DATA / "p2_route_dfre_v1.json"

REPO_URL = "https://github.com/Joel-Dahne/CGL.jl.git"
# The exact commit the paper's own bibliography [15] names, read from Papers/2410.05480.txt
# line 4943: "Joel Dahne. CGL.jl. Version 1.0.0. Commit be034923c0b63e3103a9b2cb030a02699d05625e."
PINNED_COMMIT = "be034923c0b63e3103a9b2cb030a02699d05625e"
BRANCH_DIR = "proof/data/branch_d=1_j=1"

# From arXiv:2410.05480 Section 6 (extracted text, located independently of the CSV data):
# "epsilon1 = 0.0, mu1 = 1.23203752321003, kappa1 = 0.8531088807225934" -- the paper's own
# printed starting point of the j=1 branch's numerical approximation.  Sanity gate on the
# decoder, checked BEFORE the inclusion checks are trusted (pre-committed in the novelty log).
PAPER_MU1 = 1.23203752321003
PAPER_KAPPA1 = 0.8531088807225934
DECODER_SANITY_TOL = 2e-5  # the box radius at ~eps=0 is ~1e-5..1e-6; mu1 is inside the ball, not its centre


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def ensure_repo() -> Path:
    """Clone (or reuse a cached clone of) CGL.jl at the pinned commit. Read-only."""
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    if not (CACHE / ".git").exists():
        subprocess.run(["git", "clone", "--quiet", REPO_URL, str(CACHE)], check=True)
    # make sure the pinned commit is present, then hard-detach onto it (never mutate history)
    subprocess.run(["git", "-C", str(CACHE), "fetch", "--quiet", "origin", PINNED_COMMIT],
                    check=False)  # already-present pinned commits don't need a fetch
    subprocess.run(["git", "-C", str(CACHE), "checkout", "--quiet", PINNED_COMMIT], check=True)
    head = subprocess.run(["git", "-C", str(CACHE), "rev-parse", "HEAD"],
                           check=True, capture_output=True, text=True).stdout.strip()
    assert head == PINNED_COMMIT, f"checkout landed on {head}, not the pinned {PINNED_COMMIT}"
    return CACHE


# ---------------------------------------------------------------------------
# The arb_dump_str decoder -- exact, no floating point anywhere in this section.
# ---------------------------------------------------------------------------

class SpecialValue(Exception):
    """Raised if a dumped arf hits +-inf/nan (exponent in {-1,-2,-3} with mantissa 0).
    None of the proof-witness data this leg reads is expected to contain one; if it does,
    that is reported as a decoder-side finding, never silently coerced to a number."""


def decode_arf(mantissa_hex: str, exponent_hex: str) -> Fraction:
    m = int(mantissa_hex, 16)
    e = int(exponent_hex, 16)
    if m == 0:
        if e == 0:
            return Fraction(0)
        raise SpecialValue(f"mantissa=0, exponent={e} (special value, not a real number)")
    return Fraction(m) * (Fraction(2) ** e) if e >= 0 else Fraction(m, 2 ** (-e))


def decode_arb(tokens: list) -> tuple:
    """4 space-separated hex tokens -> (mid: Fraction, rad: Fraction)."""
    mid = decode_arf(tokens[0], tokens[1])
    rad = decode_arf(tokens[2], tokens[3])
    return mid, rad


def interval_of(mid: Fraction, rad: Fraction) -> tuple:
    return (mid - rad, mid + rad)


def contains(outer: tuple, inner: tuple) -> bool:
    """outer superset-or-equal inner, i.e. inner subset-or-equal outer (non-strict)."""
    return outer[0] <= inner[0] and inner[1] <= outer[1]


def strictly_contains(outer: tuple, inner: tuple) -> bool:
    return outer[0] < inner[0] and inner[1] < outer[1]


# ---------------------------------------------------------------------------
# Segment parsing: each of top/turn/bottom is a sequence of boxes over a swept parameter
# (eps for top/bottom, kappa for turn) with a (mu, gamma_re, gamma_im, kappa-or-eps)
# uniqueness box and a strictly-smaller existence box, per arXiv:2410.05480 Section 6.
# ---------------------------------------------------------------------------

TOP_BOTTOM_COLS = ["sweep_lo", "sweep_hi",
                    "mu_uniq", "gre_uniq", "gim_uniq", "third_uniq",
                    "mu_exists", "gre_exists", "gim_exists", "third_exists",
                    "num_critical_points"]
# "third" is kappa for top/bottom (the sweep variable is eps) and eps for turn (the sweep
# variable is kappa) -- see the CSV headers themselves, read verbatim below.


def parse_segment(path: Path):
    import csv
    import gzip
    rows = []
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as f:
        reader = csv.reader(f)
        header = next(reader)
        for line_no, row in enumerate(reader, start=2):
            if len(row) != len(header):
                raise ValueError(f"{path}:{line_no}: {len(row)} fields, header has {len(header)}")
            rec = {}
            rec["sweep_lo"] = decode_arf(*row[0].split())
            rec["sweep_hi"] = decode_arf(*row[1].split())
            rec["mu_uniq"] = decode_arb(row[2].split())
            rec["gre_uniq"] = decode_arb(row[3].split())
            rec["gim_uniq"] = decode_arb(row[4].split())
            rec["third_uniq"] = decode_arb(row[5].split())
            rec["mu_exists"] = decode_arb(row[6].split())
            rec["gre_exists"] = decode_arb(row[7].split())
            rec["gim_exists"] = decode_arb(row[8].split())
            rec["third_exists"] = decode_arb(row[9].split())
            rec["num_critical_points"] = int(row[10])
            rows.append(rec)
    return header, rows


COMPONENTS_UNIQ = ["mu_uniq", "gre_uniq", "gim_uniq", "third_uniq"]
COMPONENTS_EXISTS = ["mu_exists", "gre_exists", "gim_exists", "third_exists"]


def check_segment(name: str, rows: list) -> dict:
    n = len(rows)
    strict_ok = 0
    strict_fail = []
    chain_ok = 0
    chain_fail = []
    coverage_gap = []  # sweep_hi[i] should equal sweep_lo[i+1] (boxes tile the interval)
    crit_point_values = set()

    for i, r in enumerate(rows):
        crit_point_values.add(r["num_critical_points"])
        # condition A: exists (box in R^4) strictly inside uniq (box in R^4), componentwise
        ok = True
        for cu, ce in zip(COMPONENTS_UNIQ, COMPONENTS_EXISTS):
            outer = interval_of(*r[cu])
            inner = interval_of(*r[ce])
            if not strictly_contains(outer, inner):
                ok = False
        if ok:
            strict_ok += 1
        else:
            strict_fail.append(i)

        if i > 0:
            prev = rows[i - 1]
            # condition B: exists_i subset-or-equal uniq_{i-1}, componentwise
            ok2 = True
            for cu, ce in zip(COMPONENTS_UNIQ, COMPONENTS_EXISTS):
                outer = interval_of(*prev[cu])
                inner = interval_of(*r[ce])
                if not contains(outer, inner):
                    ok2 = False
            if ok2:
                chain_ok += 1
            else:
                chain_fail.append(i)
            # The sweep direction differs by segment (top/bottom ascend in eps; turn
            # descends in kappa, confirmed by inspecting the raw rows), so the tiling
            # check must accept either orientation -- this is an ANCILLARY sanity check,
            # not part of the paper's pre-committed corollary (which only requires the
            # containment checked above, and does not require the boxes to touch exactly).
            if r["sweep_lo"] != prev["sweep_hi"] and r["sweep_hi"] != prev["sweep_lo"]:
                coverage_gap.append(i)

    return {
        "segment": name,
        "n_rows": n,
        "strict_exists_in_uniq_ok": strict_ok,
        "strict_exists_in_uniq_fail_rows": strict_fail[:20],
        "strict_exists_in_uniq_fail_count": len(strict_fail),
        "chain_exists_in_prev_uniq_ok": chain_ok,
        "chain_exists_in_prev_uniq_fail_rows": chain_fail[:20],
        "chain_exists_in_prev_uniq_fail_count": len(chain_fail),
        "chain_checked": max(n - 1, 0),
        "coverage_gap_count": len(coverage_gap),
        "num_critical_points_values": sorted(crit_point_values),
        "all_pass": (len(strict_fail) == 0 and len(chain_fail) == 0),
    }


def decoder_sanity_check(top_rows: list) -> dict:
    r0 = top_rows[0]
    mid_mu, rad_mu = r0["mu_exists"]
    mid_k, rad_k = r0["third_exists"]
    mu0 = float(mid_mu)
    k0 = float(mid_k)
    d_mu = abs(mu0 - PAPER_MU1)
    d_k = abs(k0 - PAPER_KAPPA1)
    return {
        "row0_sweep_interval_eps": [float(r0["sweep_lo"]), float(r0["sweep_hi"])],
        "decoded_mu_exists_mid": mu0,
        "decoded_mu_exists_rad": float(rad_mu),
        "paper_mu1_section6": PAPER_MU1,
        "abs_diff_mu": d_mu,
        "decoded_kappa_exists_mid": k0,
        "decoded_kappa_exists_rad": float(rad_k),
        "paper_kappa1_section6": PAPER_KAPPA1,
        "abs_diff_kappa": d_k,
        "tolerance": DECODER_SANITY_TOL,
        "pass": d_mu < DECODER_SANITY_TOL and d_k < DECODER_SANITY_TOL,
    }


def check_connection_points(path: Path, top_last, turn_rows, bottom_rows) -> dict:
    import csv
    with open(path, "rt") as f:
        reader = csv.reader(f)
        header = next(reader)
        recs = []
        for row in reader:
            rec = {
                "eps": decode_arb(row[0].split()),
                "mu_uniq": decode_arb(row[1].split()),
                "gre_uniq": decode_arb(row[2].split()),
                "gim_uniq": decode_arb(row[3].split()),
                "kappa_uniq": decode_arb(row[4].split()),
                "mu_exists": decode_arb(row[5].split()),
                "gre_exists": decode_arb(row[6].split()),
                "gim_exists": decode_arb(row[7].split()),
                "kappa_exists": decode_arb(row[8].split()),
            }
            recs.append(rec)
    out = {"header": header, "n_rows": len(recs), "rows": []}
    comp_u = ["mu_uniq", "gre_uniq", "gim_uniq", "kappa_uniq"]
    comp_e = ["mu_exists", "gre_exists", "gim_exists", "kappa_exists"]
    for rec in recs:
        ok = all(strictly_contains(interval_of(*rec[cu]), interval_of(*rec[ce]))
                  for cu, ce in zip(comp_u, comp_e))
        out["rows"].append({"eps_mid": float(rec["eps"][0]),
                             "own_exists_in_own_uniq": ok})
    out["all_own_boxes_ok"] = all(r["own_exists_in_own_uniq"] for r in out["rows"])
    return out


def main():
    t0 = time.perf_counter()
    print("== ensuring CGL.jl at the pinned commit ==")
    repo = ensure_repo()
    branch_dir = repo / BRANCH_DIR

    files = {
        "top": branch_dir / "top.csv.gz",
        "turn": branch_dir / "turn.csv.gz",
        "bottom": branch_dir / "bottom.csv.gz",
    }
    for k, p in files.items():
        if not p.exists():
            raise FileNotFoundError(f"expected {p}; CGL.jl layout may have changed at this commit")

    print("== decoding (exact dyadic arithmetic) ==")
    segment_results = {}
    raw_rows = {}
    headers = {}
    for name, path in files.items():
        header, rows = parse_segment(path)
        headers[name] = header
        raw_rows[name] = rows
        segment_results[name] = check_segment(name, rows)
        print(f"   {name}: {len(rows)} rows, all_pass={segment_results[name]['all_pass']}")

    sanity = decoder_sanity_check(raw_rows["top"])
    print(f"   decoder sanity vs paper Sec 6 mu1/kappa1: pass={sanity['pass']}")

    conn_path = branch_dir / "connection_points.csv.gz"
    conn = None
    if conn_path.exists():
        import gzip
        import shutil
        tmp = branch_dir / "_connection_points_tmp.csv"
        with gzip.open(conn_path, "rt") as fin, open(tmp, "w") as fout:
            shutil.copyfileobj(fin, fout)
        conn = check_connection_points(tmp, raw_rows["top"][-1], raw_rows["turn"], raw_rows["bottom"])
        tmp.unlink()
        print(f"   connection_points: {conn['n_rows']} rows, all_own_boxes_ok={conn['all_own_boxes_ok']}")

    all_segments_pass = all(v["all_pass"] for v in segment_results.values())
    gate_yes = all_segments_pass and sanity["pass"] and (conn is None or conn["all_own_boxes_ok"])

    elapsed = time.perf_counter() - t0
    print(f"== done in {elapsed:.1f}s; GATE = {'YES' if gate_yes else 'NO'} ==")

    result = {
        "leg": 316,
        "route": "DFRE",
        "paper": "arXiv:2410.05480 (Dahne-Figueras)",
        "pdf_sha256": sha256_of(ROOT / "Papers" / "2410.05480.pdf") if (ROOT / "Papers" / "2410.05480.pdf").exists() else None,
        "repo_url": REPO_URL,
        "pinned_commit": PINNED_COMMIT,
        "branch_target": "Case I, d=1, j=1",
        "gate_question": ("Does DF-CGL's published verification package reproduce the "
                           "paper's own corollary from its published constants, in this "
                           "environment?"),
        "gate_answer": "YES" if gate_yes else "NO",
        "decoder_sanity_check": sanity,
        "segments": segment_results,
        "connection_points": conn,
        "elapsed_seconds": elapsed,
        "row_totals": {k: len(v) for k, v in raw_rows.items()},
    }

    DATA.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, default=str))
    print(f"wrote {OUT}")
    return result


if __name__ == "__main__":
    main()
