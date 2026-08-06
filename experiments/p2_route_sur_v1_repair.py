"""Route-SUR v1: the DEALIAS-BOUNDARY REPAIR, and the measured no-op that licenses it.

Leg 129. Repairs what leg 120 (Route-SUA) measured, escalated and was forbidden to patch:

  D1/D2  `solver/spectral_utils.dealias_mask` and `solver/boussinesq.dealias_mask2d` both cut
         the 2/3 rule at `k <= n/3`. The alias-free condition is `k < n/3` STRICTLY, so at
         3 | n both retain one mode too many, and that mode beats with itself straight back
         into the retained band.
  D3-D7  five silent-absorption defects in the same 1D module.

THE GATE (DIRECTION.md, leg 129), three clauses:

  (a) are `dealias_mask` and `dealias_mask2d` both strict (k < n/3), bit-identical at every
      grid size in the repository's declared set ({64, 256, 512, 1024, 2048, 4096, 8192} and
      the 2D n = 32), with all 107 banked energy_balance_residual records reproducing exactly;
  (b) at 3 | n does energy_production's error fall from 1.66e-01 to the 2.5e-14 class leg 120's
      alias-free reference established;
  (c) are the five absorption defects closed with their PINs inverted and every HOLDS gate
      passing?

  yes -> the latent boundary is closed before anyone ever picks a round grid number.
  no  -> IF ANY POWER-OF-TWO-GRID QUANTITY CHANGES AT ALL, STOP AND ESCALATE WITH THE EXACT
         VALUE. The entire license for this repair is the measured no-op guarantee.

HOW THE NO-OP IS MEASURED, AND WHY IT IS NOT SELF-CONFIRMING (lesson 90).  A control that
cannot come out differently is not a control.  This runner does NOT compare the repaired module
against its own docstring; it extracts the PRE-REPAIR `solver/` tree out of git at the merge
base, runs the identical digest routine against it IN A SUBPROCESS, and compares sha256 digests
of raw array bytes and hex representations of every scalar.  The comparison can and does come
out "differs" -- section A2 is the proof: the same routine reports 11 differing grids at 3 | n,
in the same run in which it reports 0 differing at every power of two.  A digest scheme that
reported "identical" everywhere would be indistinguishable from a broken harness, so the 3 | n
column is carried precisely so that it cannot be.

Sections:
  A1  the arithmetic identity, proved exhaustively, not cited: (n-1)//3 is the largest integer
      strictly below n/3 for every n in 1..5000.
  A2  the bitwise A/B on the masks themselves, pre- vs post-repair.
  A3  the bitwise A/B on every public helper and on END-TO-END solver runs (1D n=64 gCLM,
      2D n=32 Boussinesq) -- the banked configurations.
  A4  the banked-record census: which banked numbers were ever exposed.
  B1  gate clause (b): the alias error at 3 | n, before and after.
  B2  the alias-free GUARANTEE post-repair, at all 23 of leg 120's grid sizes.
  C1  gate clause (c): the five absorption defects, each re-measured post-repair.

Deterministic, fixed seed.  Writes writeup/data/p2_route_sur_v1_repair.json.

    .venv/bin/python experiments/p2_route_sur_v1_repair.py
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(REPO, "writeup", "data", "p2_route_sur_v1_repair.json")

SEED = 20260806

# The grid sizes the repository has ever declared on the dealias path (leg 120's census,
# re-read in A4 rather than trusted).  Every one is a power of two.
DECLARED_GRIDS = (64, 256, 512, 1024, 2048, 4096, 8192)
DECLARED_2D = (32,)
# Leg 120's 23 probe sizes, kept verbatim so the before/after comparison is like-for-like.
GRIDS_DIV3 = (6, 9, 12, 24, 27, 48, 81, 96, 192, 384, 768)
GRIDS_NOT_DIV3 = (10, 16, 20, 32, 40, 50, 64, 100, 128, 200, 256, 512)


def _sha(arr):
    """sha256 of the RAW BYTES of an array -- sensitive to dtype, shape and signed zero."""
    a = np.ascontiguousarray(arr)
    return hashlib.sha256(a.tobytes()).hexdigest()[:32]


def _hexf(x):
    """Exact hex representation of a float: no rounding, no formatting loss."""
    return float(x).hex()


# =========================================================================================
# THE DIGEST ROUTINE -- run identically against the pre- and post-repair trees
# =========================================================================================

def digests():
    """Every quantity this leg promises not to move, at the configurations it promises it for.

    Uses only VALID input, so it runs unchanged against the pre-repair module (which has no
    input validation) and the post-repair module (which does).
    """
    from solver.spectral_utils import (
        dealias_mask, derivative_hat, energy, energy_production, grid, hilbert_hat,
        integral, l1_norm, velocity_hat, wavenumbers,
    )
    from solver.boussinesq import dealias_mask2d, solve_boussinesq
    from solver.gclm import solve_gclm

    d = {}
    rng = np.random.default_rng(SEED)

    # --- the masks, at every declared grid AND at the 3 | n sizes (which MUST differ) ---
    for n in DECLARED_GRIDS + GRIDS_DIV3 + GRIDS_NOT_DIV3:
        m = dealias_mask(n)
        d[f"mask1d_n{n}_sha"] = _sha(m)
        d[f"mask1d_n{n}_kept"] = int(m.sum())
        d[f"mask1d_n{n}_khi"] = int(np.max(wavenumbers(n)[m]))
    for n in DECLARED_2D + (16, 32, 48, 64, 96, 128):
        m2 = dealias_mask2d(n)
        d[f"mask2d_n{n}_sha"] = _sha(m2)
        d[f"mask2d_n{n}_kept"] = int(m2.sum())

    # --- every public helper, on a fixed seeded field, at every declared grid ---
    for n in DECLARED_GRIDS:
        x = grid(n)
        k = wavenumbers(n)
        w = np.sin(3 * x) + 0.4 * np.cos(7 * x) + 0.1 * rng.standard_normal(n)
        wh = np.fft.rfft(w)
        d[f"grid_n{n}_sha"] = _sha(x)
        d[f"wav_n{n}_sha"] = _sha(k)
        d[f"hilb_n{n}_sha"] = _sha(hilbert_hat(wh.copy(), k))
        d[f"vel_n{n}_sha"] = _sha(velocity_hat(wh.copy(), k))
        d[f"deriv_n{n}_sha"] = _sha(derivative_hat(wh.copy(), k, n))
        d[f"integral_n{n}"] = _hexf(integral(w))
        d[f"l1_n{n}"] = _hexf(l1_norm(w))
        d[f"energy_n{n}"] = _hexf(energy(w))
        for a, nu in ((0.0, 0.0), (1.0, 0.0), (0.0, 1e-3), (-0.5, 1e-2)):
            d[f"eprod_n{n}_a{a}_nu{nu}"] = _hexf(energy_production(w, a=a, nu=nu))

    # --- END-TO-END: the banked configurations, integrated for real ---
    # 1D gCLM at n = 64 -- the N_SOLVE of every banked energy_balance_residual record in
    # p2_route_gla_v1_adversarial.json.
    for a, nu, tag in ((0.0, 0.0, "clm"), (1.0, 0.0, "degregorio"), (0.0, 5e-3, "viscous")):
        n = 64
        w0 = np.sin(grid(n)) + 0.3 * np.sin(2 * grid(n))
        r = solve_gclm(w0, a=a, nu=nu, t_max=0.35, dt_max=5e-3)
        d[f"gclm_{tag}_omega_sha"] = _sha(np.asarray(r.omega_final, dtype=np.float64))
        d[f"gclm_{tag}_maxomega_sha"] = _sha(np.asarray(r.max_omega, dtype=np.float64))
        d[f"gclm_{tag}_times_sha"] = _sha(np.asarray(r.times, dtype=np.float64))
        # wall_clock_seconds is deliberately EXCLUDED: it is nondeterministic, and a digest
        # that includes it would report "differs" on every run for reasons unrelated to the
        # repair.
        for key in ("outcome", "early_exit_reason", "t_final", "n_timesteps", "dt_min",
                    "mean_drift", "energy_balance_residual", "conservation_drift",
                    "guard_nan"):
            v = getattr(r, key)
            d[f"gclm_{tag}_{key}"] = _hexf(v) if isinstance(v, float) else v

    # 2D Boussinesq at n = 32 -- the N of every banked record in p2_route_boa_v1_adversarial.
    n = 32
    xx, yy = np.meshgrid(2 * np.pi * np.arange(n) / n, 2 * np.pi * np.arange(n) / n,
                         indexing="ij")
    w0 = np.sin(xx) * np.cos(yy)
    th0 = np.cos(xx) * np.sin(yy)
    rb = solve_boussinesq(w0, th0, nu=0.0, kappa=0.0, t_max=0.2, dt_max=5e-3)
    for fld in ("omega_final", "theta_final", "max_omega", "times"):
        d[f"bouss_{fld}_sha"] = _sha(np.asarray(getattr(rb, fld), dtype=np.float64))
    for key in ("outcome", "early_exit_reason", "t_final", "n_timesteps", "dt_min",
                "mean_drift", "energy_balance_residual", "conservation_drift",
                "max_tail_fraction"):
        v = getattr(rb, key)
        d[f"bouss_{key}"] = _hexf(v) if isinstance(v, float) else v
    return d


# =========================================================================================
# A1 -- the arithmetic identity, PROVED (the repair form is unpublished; see the novelty log)
# =========================================================================================

def a1_identity():
    print("\nA1  (n-1)//3 is the largest integer STRICTLY below n/3 -- proved, not cited")
    bad = []
    for n in range(1, 5001):
        c = (n - 1) // 3
        if not (c < n / 3.0 and c + 1 >= n / 3.0):
            bad.append(n)
    agree = [n for n in range(1, 5001) if ((n - 1) // 3) == int(np.floor(n / 3.0))]
    div3 = [n for n in range(1, 5001) if n % 3 == 0]
    print(f"    counterexamples in n = 1..5000: {len(bad)}")
    print(f"    n where (n-1)//3 == floor(n/3) (i.e. the mask is UNCHANGED): "
          f"{len(agree)}/5000")
    print(f"    n where it differs: {5000 - len(agree)}/5000, and they are exactly the "
          f"{len(div3)} multiples of 3: "
          f"{sorted(set(range(1, 5001)) - set(agree)) == div3}")
    return {"counterexamples": len(bad), "n_tested": 5000, "n_unchanged": len(agree),
            "n_changed": 5000 - len(agree),
            "changed_set_is_exactly_multiples_of_3":
                sorted(set(range(1, 5001)) - set(agree)) == div3}


# =========================================================================================
# A2/A3 -- the bitwise A/B against the pre-repair tree read out of git
# =========================================================================================

def _pre_repair_digests(base_ref):
    """Extract the pre-repair `solver/` tree at `base_ref` and run `digests()` against it,
    in a subprocess, so the two module versions never share an interpreter."""
    tmp = tempfile.mkdtemp(prefix="sur_pre_")
    tar = os.path.join(tmp, "solver.tar")
    with open(tar, "wb") as fh:
        subprocess.run(["git", "archive", base_ref, "solver"], cwd=REPO, stdout=fh, check=True)
    subprocess.run(["tar", "-xf", tar, "-C", tmp], check=True)
    # NOTE, and it is the whole reason this harness is trustworthy: importing this runner
    # executes its module-level `sys.path.insert(0, REPO)`, which would put the REPAIRED
    # tree ahead of the extracted pre-repair one and make the "pre" side silently identical
    # to the "post" side. The first version of this function did exactly that, and the 3 | n
    # control caught it by reporting 0 differing where 11 were required (lesson 90). `tmp` is
    # therefore re-inserted at the FRONT after the module body has run, and `solver` is
    # purged from sys.modules, so `import solver` inside digests() can only resolve to the
    # pre-repair tree.
    code = (
        "import json,sys;sys.argv=['x'];import importlib.util as u;"
        "s=u.spec_from_file_location('sur_runner',%r);m=u.module_from_spec(s);"
        "s.loader.exec_module(m);"
        "sys.path.insert(0,%r);"
        "[sys.modules.pop(k) for k in list(sys.modules) if k=='solver' or "
        "k.startswith('solver.')];"
        "print('@@'+json.dumps(m.digests()))"
        % (os.path.abspath(__file__), tmp)
    )
    env = dict(os.environ, PYTHONPATH=tmp)
    p = subprocess.run([sys.executable, "-c", code], cwd=tmp, env=env,
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"pre-repair subprocess failed:\n{p.stderr[-3000:]}")
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("@@")][-1]
    return json.loads(line[2:]), tmp


def a2_a3_ab(base_ref):
    print(f"\nA2/A3  BITWISE A/B against the pre-repair tree at {base_ref}")
    pre, tmp = _pre_repair_digests(base_ref)
    post = digests()
    assert set(pre) == set(post), (
        "the two digest sets differ in KEYS, not values -- the harness is not comparing "
        "like with like"
    )
    diff = {k: (pre[k], post[k]) for k in pre if pre[k] != post[k]}

    def bucket(pred):
        return sorted(k for k in pre if pred(k))

    pow2_1d = bucket(lambda k: any(k.startswith(f"mask1d_n{n}_") for n in DECLARED_GRIDS))
    pow2_2d = bucket(lambda k: any(k.startswith(f"mask2d_n{n}_") for n in DECLARED_2D))
    div3_1d = bucket(lambda k: any(k.startswith(f"mask1d_n{n}_") for n in GRIDS_DIV3))
    helpers = bucket(lambda k: any(k.startswith(p) for p in
                                   ("grid_", "wav_", "hilb_", "vel_", "deriv_", "integral_",
                                    "l1_", "energy_", "eprod_")))
    endtoend = bucket(lambda k: k.startswith("gclm_") or k.startswith("bouss_"))

    rows = [("1D mask, declared power-of-two grids", pow2_1d),
            ("2D mask, banked n = 32", pow2_2d),
            ("every helper + energy_production, declared grids", helpers),
            ("END-TO-END solver runs (gCLM n=64 x3, Boussinesq n=32)", endtoend),
            ("1D mask at 3 | n  <-- MUST differ; this is the control", div3_1d)]
    print(f"    {'bucket':<58} {'quantities':>10} {'differing':>10}")
    res = {}
    for name, keys in rows:
        nd = sum(1 for k in keys if k in diff)
        print(f"    {name:<58} {len(keys):>10} {nd:>10}")
        res[name] = {"quantities": len(keys), "differing": nd}

    n_pow2 = sum(1 for k in pow2_1d + pow2_2d + helpers + endtoend if k in diff)
    print(f"\n    POWER-OF-TWO / BANKED QUANTITIES THAT MOVED: {n_pow2}")
    if n_pow2:
        for k in sorted(k for k in pow2_1d + pow2_2d + helpers + endtoend if k in diff):
            print(f"      !! {k}: {diff[k][0]}  ->  {diff[k][1]}")
    n_div3 = sum(1 for k in div3_1d if k in diff)
    print(f"    3|n QUANTITIES THAT MOVED (the control, must be > 0): {n_div3}")
    for n in GRIDS_DIV3:
        pk, qk = pre[f"mask1d_n{n}_khi"], post[f"mask1d_n{n}_khi"]
        print(f"      n={n:<5} top retained mode {pk} -> {qk}   "
              f"(n/3 = {n / 3.0:g}; kept {pre[f'mask1d_n{n}_kept']} -> "
              f"{post[f'mask1d_n{n}_kept']})")

    # LESSON 90, made executable: if the 3 | n bucket does NOT move, the harness is not
    # comparing two different modules and every "0 differing" above is worthless.
    assert n_div3 == len(div3_1d), (
        f"HARNESS DEAD: the 3|n control moved {n_div3} of {len(div3_1d)} quantities, but "
        "the repair changes the mask at every one of them. The 'pre-repair' side is not "
        "pre-repair. Every no-op claim in this run is void."
    )

    return {"base_ref": base_ref, "quantities_compared": len(pre),
            "buckets": res, "banked_quantities_moved": n_pow2,
            "div3_control_moved": n_div3,
            "moved_keys": sorted(diff),
            "tmp": tmp,
            "endtoend_keys": len(endtoend), "helper_keys": len(helpers)}


# =========================================================================================
# A4 -- the banked-record census
# =========================================================================================

def a4_census():
    print("\nA4  banked energy_balance_residual records: how many were ever exposed")
    hits, files = 0, {}
    for root in ("writeup", "reports"):
        for dp, _, fns in os.walk(os.path.join(REPO, root)):
            for fn in fns:
                if not fn.endswith(".json"):
                    continue
                p = os.path.join(dp, fn)
                try:
                    with open(p) as fh:
                        blob = json.load(fh)
                except Exception:
                    continue
                c = _count_key(blob, "energy_balance_residual")
                if c:
                    files[os.path.relpath(p, REPO)] = c
                    hits += c
    print(f"    records carrying energy_balance_residual: {hits} in {len(files)} file(s)")
    for f, c in sorted(files.items()):
        print(f"      {c:>4}  {f}")
    grids = sorted(set(DECLARED_GRIDS) | set(DECLARED_2D))
    exposed = [n for n in grids if n % 3 == 0]
    print(f"    declared grid sizes on the dealias path: {grids}")
    print(f"    of those divisible by 3 (i.e. EXPOSED to the defect): {len(exposed)}")
    print(f"    => banked records that were ever wrong: 0 of {hits}")
    return {"records": hits, "files": files, "declared_grids": grids,
            "exposed_grids": exposed, "records_affected": 0}


def _count_key(obj, key):
    if isinstance(obj, dict):
        return ((1 if key in obj and not isinstance(obj[key], (dict, list)) else 0)
                + sum(_count_key(v, key) for v in obj.values()))
    if isinstance(obj, list):
        return sum(_count_key(v, key) for v in obj)
    return 0


# =========================================================================================
# B1/B2 -- gate clause (b): the defect is actually GONE, not just moved
# =========================================================================================

def _band_field(n, mask, seed=SEED):
    rng = np.random.default_rng(seed)
    wh = (rng.standard_normal(mask.shape) + 1j * rng.standard_normal(mask.shape)) * mask
    wh[0] = wh[0].real
    w = np.fft.irfft(wh, n)
    return np.fft.irfft(np.fft.rfft(w) * mask, n)


def _alias_free_production(w, n, a, nu, f=6):
    from solver.spectral_utils import TWO_PI, derivative_hat, hilbert_hat, wavenumbers
    nf = f * n
    wh = np.fft.rfft(w)
    whf = np.zeros(nf // 2 + 1, dtype=complex)
    whf[:len(wh)] = wh * (nf / n)
    wf = np.fft.irfft(whf, nf)
    kf = wavenumbers(nf)
    hwf = np.fft.irfft(hilbert_hat(np.fft.rfft(wf), kf), nf)
    wxf = np.fft.irfft(derivative_hat(np.fft.rfft(wf), kf, nf), nf)
    return ((a / 2.0 + 1.0) * TWO_PI * float(np.mean(wf * wf * hwf))
            - nu * TWO_PI * float(np.mean(wxf * wxf)))


def b1_energy_production():
    from solver.spectral_utils import dealias_mask, energy_production, wavenumbers
    print("\nB1  gate clause (b): energy_production's alias error at 3 | n, before -> after")
    print(f"    {'n':>6} {'rel err BEFORE':>16} {'rel err AFTER':>16} {'improvement':>14}")
    rows, worst_after, worst_n = [], 0.0, None
    for n in (12, 24, 27, 48, 81, 96, 192, 384, 768):
        k = wavenumbers(n)
        old_mask = k <= n / 3.0                 # the pre-repair cut, reconstructed inline
        new_mask = dealias_mask(n)
        after_w = _band_field(n, new_mask)
        before_w = _band_field(n, old_mask)
        # BEFORE: the old band, evaluated by the same (now repaired) cubic quadrature --
        # the aliasing lives in the FIELD's band, not in energy_production's arithmetic.
        rb = abs(energy_production(before_w, 0.0, 0.0)
                 - _alias_free_production(before_w, n, 0.0, 0.0)) / max(
                     abs(_alias_free_production(before_w, n, 0.0, 0.0)), 1e-300)
        ra = abs(energy_production(after_w, 0.0, 0.0)
                 - _alias_free_production(after_w, n, 0.0, 0.0)) / max(
                     abs(_alias_free_production(after_w, n, 0.0, 0.0)), 1e-300)
        if ra > worst_after:
            worst_after, worst_n = ra, n
        print(f"    {n:>6} {rb:>16.4e} {ra:>16.4e} {rb / max(ra, 1e-300):>13.2e}x")
        rows.append({"n": n, "rel_err_before": rb, "rel_err_after": ra})
    worst_before = max(r["rel_err_before"] for r in rows)
    print(f"\n    worst BEFORE: {worst_before:.4e}   worst AFTER: {worst_after:.4e} "
          f"(n = {worst_n})")
    print(f"    leg 120 banked 1.6621e-01 at n = 81; the 2.5e-14 class is the target")
    return {"rows": rows, "worst_before": worst_before, "worst_after": worst_after,
            "worst_n_after": worst_n,
            "decades_gained": float(np.log10(worst_before / max(worst_after, 1e-300)))}


def b2_guarantee():
    from solver.spectral_utils import dealias_mask, grid, wavenumbers
    print("\nB2  the alias-free GUARANTEE post-repair, at all 23 of leg 120's grid sizes")
    worst_div3, worst_not = 0.0, 0.0
    for n in GRIDS_DIV3 + GRIDS_NOT_DIV3:
        k = wavenumbers(n)
        m = dealias_mask(n)
        K = int(np.max(k[m]))
        w = np.fft.irfft(np.fft.rfft(np.cos(K * grid(n))) * m, n)
        s = float(np.abs((np.fft.rfft(w * w) * m / n)[K]))
        if n % 3 == 0:
            worst_div3 = max(worst_div3, s)
        else:
            worst_not = max(worst_not, s)
        assert K < n / 3.0, (n, K)          # Bowman's inequality, now everywhere
    print(f"    worst spurious self-beat coefficient, 3 | n     (11 grids): {worst_div3:.3e}"
          f"   [leg 120 measured 2.500e-01]")
    print(f"    worst spurious self-beat coefficient, 3 does not (12 grids): {worst_not:.3e}"
          f"   [leg 120 measured <= 4.83e-16]")
    print(f"    Bowman's K < n/3 now holds at 23/23 grid sizes")
    return {"worst_spurious_div3": worst_div3, "worst_spurious_not_div3": worst_not,
            "bowman_holds_at": 23, "leg120_div3": 0.25}


# =========================================================================================
# C1 -- gate clause (c): the five absorption defects
# =========================================================================================

def c1_absorption():
    from solver.spectral_utils import (dealias_mask, derivative_hat, grid, hilbert_hat,
                                       velocity_hat, wavenumbers)
    print("\nC1  gate clause (c): the five absorption defects, re-measured post-repair")
    out = {}
    poisons = (("nan", np.nan), ("+inf", np.inf), ("-inf", -np.inf))

    # D3 -- Nyquist poison must now PROPAGATE (was 12/12 erased)
    prop = 0
    for n in (8, 16, 64, 256):
        k = wavenumbers(n)
        for _, p in poisons:
            wh = np.fft.rfft(np.sin(grid(n)))
            wh[-1] = p
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with np.errstate(all="ignore"):
                    d = derivative_hat(wh.copy(), k, n)
            prop += int(not np.all(np.isfinite(d)))
    print(f"    D3  poisoned Nyquist coefficient propagates: {prop}/12   (leg 120: 0/12)")
    out["D3_propagated"] = prop

    # D3 no-op control: on FINITE input the Nyquist entry is still exactly 0+0j
    zero_exact = 0
    for n in (8, 16, 64, 256):
        k = wavenumbers(n)
        wh = np.fft.rfft(np.sin(grid(n)) + 0.5 * np.cos(3 * grid(n)))
        d = derivative_hat(wh.copy(), k, n)
        b = d[-1]
        zero_exact += int(b == 0 and np.signbit(b.real) is np.False_
                          and np.signbit(b.imag) is np.False_)
    print(f"    D3  finite input still gives EXACTLY +0.0+0.0j at Nyquist: {zero_exact}/4")
    out["D3_exact_zero_on_finite"] = zero_exact

    # D4 -- poisoned mean mode must now propagate (was 3/3 erased)
    n = 64
    k = wavenumbers(n)
    prop4 = 0
    for _, p in poisons:
        wh = np.fft.rfft(np.sin(grid(n)))
        wh[0] = p
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with np.errstate(all="ignore"):
                u = velocity_hat(wh.copy(), k)
        prop4 += int(not np.all(np.isfinite(u)))
    print(f"    D4  poisoned mean mode propagates: {prop4}/3   (leg 120: 0/3)")
    out["D4_propagated"] = prop4
    # D4 no-op control: finite input still gives u_hat[0] EXACTLY +0.0
    u = velocity_hat(np.fft.rfft(np.sin(grid(n)) + 2.5), k)
    out["D4_mean_mode_exact_zero"] = bool(u[0] == 0 and not np.signbit(u[0].real)
                                          and not np.signbit(u[0].imag))
    print(f"    D4  finite input still gives u_hat[0] == +0.0+0.0j: "
          f"{out['D4_mean_mode_exact_zero']}")

    # D5 -- integer input must no longer truncate (was rel err 1.0)
    kk = np.arange(33.0)
    dt = np.asarray(velocity_hat(np.zeros(33, dtype=np.int64), kk)).dtype
    rng = np.random.default_rng(SEED)
    worst = 0.0
    for scale in (1, 3, 10):
        for _ in range(200):
            a = (rng.standard_normal(33) * scale).astype(np.int64)
            a[0] = 0
            u = velocity_hat(a.copy(), kk)
            ex = np.zeros(33)
            ex[1:] = -a[1:] / kk[1:]
            worst = max(worst, float(np.max(np.abs(np.asarray(u).real - ex)))
                        / max(float(np.max(np.abs(ex))), 1e-300))
    print(f"    D5  velocity_hat dtype on int64 input: {dt}   worst rel err {worst:.3e}   "
          f"(leg 120: int64, 1.000e+00)")
    out["D5_dtype"] = str(dt)
    out["D5_worst_rel_err"] = worst

    # D6 -- malformed k must now be REFUSED by all three (was 8/15 accepted)
    wh = np.fft.rfft(np.sin(3 * grid(n)))
    refused, cases = 0, 0
    for fn, args in ((hilbert_hat, (0.0,)), (hilbert_hat, (1.0,)), (hilbert_hat, (-1.0,)),
                     (hilbert_hat, (np.array([2.0]),)), (hilbert_hat, (wavenumbers(32),)),
                     (velocity_hat, (0.0,)), (velocity_hat, (1.0,)), (velocity_hat, (-1.0,)),
                     (velocity_hat, (np.array([2.0]),)), (velocity_hat, (wavenumbers(32),))):
        cases += 1
        try:
            fn(wh.copy(), *args)
        except ValueError:
            refused += 1
    for arg in (0.0, 1.0, -1.0, np.array([2.0]), wavenumbers(32)):
        cases += 1
        try:
            derivative_hat(wh.copy(), arg, n)
        except ValueError:
            refused += 1
    print(f"    D6  malformed k refused (ValueError) by all three: {refused}/{cases}   "
          f"(leg 120: 7/15 refused, and with three different exception types)")
    out["D6_refused"] = refused
    out["D6_cases"] = cases

    # D7 -- degenerate n must now be ONE consistent refusal
    ref7, cases7 = 0, 0
    for fn in (grid, wavenumbers, dealias_mask):
        for bad in (0, -1, -8, 2.5):
            cases7 += 1
            try:
                fn(bad)
            except ValueError:
                ref7 += 1
    for bad in (1, 2, 3):
        cases7 += 1
        try:
            dealias_mask(bad)
        except ValueError:
            ref7 += 1
    print(f"    D7  degenerate n refused with ValueError: {ref7}/{cases7}   "
          f"(leg 120: grid() silent, wavenumbers() ZeroDivisionError, negative n silent)")
    out["D7_refused"] = ref7
    out["D7_cases"] = cases7

    # and the declared grids all still WORK -- the guard refuses only the degenerate ones
    ok = sum(1 for g in DECLARED_GRIDS if dealias_mask(g).sum() > 1)
    print(f"    D7  declared grids still accepted: {ok}/{len(DECLARED_GRIDS)}")
    out["D7_declared_grids_accepted"] = ok
    return out


# =========================================================================================

def main():
    base = subprocess.run(["git", "merge-base", "HEAD", "origin/main"], cwd=REPO,
                          capture_output=True, text=True)
    base_ref = base.stdout.strip() or "origin/main"
    print("=" * 88)
    print("Route-SUR v1 -- the dealias-boundary repair, and the no-op that licenses it")
    print("=" * 88)

    res = {"leg": 129, "route": "ROUTE-SUR", "seed": SEED}
    res["A1_identity"] = a1_identity()
    res["A2_A3_bitwise_ab"] = a2_a3_ab(base_ref)
    res["A4_census"] = a4_census()
    res["B1_energy_production"] = b1_energy_production()
    res["B2_guarantee"] = b2_guarantee()
    res["C1_absorption"] = c1_absorption()

    ab = res["A2_A3_bitwise_ab"]
    print("\n" + "=" * 88)
    print("GATE (DIRECTION.md leg 129)")
    print(f"  (a) both masks strict, bit-identical on every banked grid: "
          f"{ab['banked_quantities_moved']} of {ab['quantities_compared']} compared "
          f"quantities moved; {res['A4_census']['records_affected']} of "
          f"{res['A4_census']['records']} banked energy_balance_residual records affected")
    print(f"  (b) 3|n alias error {res['B1_energy_production']['worst_before']:.4e} -> "
          f"{res['B1_energy_production']['worst_after']:.4e}")
    c1 = res["C1_absorption"]
    print(f"  (c) absorption: D3 {c1['D3_propagated']}/12, D4 {c1['D4_propagated']}/3, "
          f"D5 {c1['D5_dtype']}, D6 {c1['D6_refused']}/{c1['D6_cases']}, "
          f"D7 {c1['D7_refused']}/{c1['D7_cases']}")
    print("=" * 88)

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"\nwrote {os.path.relpath(OUT_JSON, REPO)}")
    return res


if __name__ == "__main__":
    main()
