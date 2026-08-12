"""ROUTE-MTSC v1 -- does the Malmquist-Takenaka (MT) survivor of leg 301's 14-candidate
screen survive the three-realization death, measured ON THE REAL TARGET, not a toy.

Leg 301 screened structurally (closed-form differentiation matrix only) and left exactly
one survivor, with three named counterweights it deliberately did not resolve. This leg's
whole job is clause (c): "the nonlinearity is entirely unmeasured -- measure it in float on
the target", plus re-checking (a)/(b) on the real coupled linear operator (not just the bare
differentiation matrix) and pricing (d).

WHAT "in MT coordinates" MEANS HERE. The real target's Jacobian `solver/bordered_hl.py`
builds is a discretisation, on a collocation grid, of the continuous linear operator
    L[dOmega, dV] = ( Om_X * Uop + S * D - c_omega ) dOmega  -  dV ,  ( S*D - 2 c_omega + HOm ) dV + V_X*Uop dOmega + V*H dOmega
(the top-left 2n x 2n block of `jacobian(z)`, border/gauge columns dropped -- those are a
finite rank-3 correction, irrelevant to the ASYMPTOTIC-in-truncation questions S1/S2 ask).
This runner represents that SAME discrete operator in MT coefficient space via a
quadrature Galerkin change of basis:  L_MT = A @ L_grid @ Phi^T,  A = conj(Phi) @ diag(w),
with Phi[j,i] = MT-mode-j evaluated at grid node i and w the grid's trapezoid weights.
This is NOT re-deriving the operator by hand term-by-term (that would silently assume
things about how Uop/H interact with MT that nobody has proven) -- it takes the operator
this repository ALREADY built and asks what it looks like in the new coordinates, which is
exactly what a Galerkin truncation error analysis would need as its starting point anyway.

MT closed forms (Iserles & Webb DAMTP NA2019/03 eq 3.3, as quoted and self-tested by leg 301):
    phi_n(x) = i^n sqrt(2/pi) exp(i n psi(x)) / (1 - 2ix),   psi(x) = 2 arctan(2x)
    D[n,n] = i(2n+1),  D[n,n+1] = n+1,  D[n,n-1] = -n            (skew-Hermitian, tridiagonal)
    Hilbert transform diagonal: -i on n>=0 (Hardy H^2, upper half plane), +i on n<0.

Run:  .venv/bin/python -u experiments/p2_route_mtsc_v1.py

PERFORMANCE NOTE (assessed before the logged run, per the standing performance rule).
A first pass at grid n=201 completed in 175s but its result was WRONG: a control run
(the MT analysis/synthesis Gram matrix `A @ Phi^T`, which must be ~ identity in the
continuous limit) showed `sigma_min(G)` collapsing to 1e-16..1e-17 for M >= 32 on that
grid -- i.e. the earlier σ_min collapse in the transported operator was the QUADRATURE
under-resolving the MT basis, not a property of the target (lesson 86: a bound
dominated by its own evaluation error is a statement about the code). A convergence
sweep of the Gram control across n = 201..3201 found the requirement is roughly
n >= 6x(2M+1); n=801 keeps `sigma_min(G) >= 0.945` through M=64. So this run uses
GRID_N=801 (measured Newton wall time 78.6s, one solve) and caps M_LADDER / the
nonlinearity projection at 64, where the quadrature is independently verified
trustworthy -- rather than the originally planned M=128, where at ANY grid size tried
here it was not. Total measured wall time is printed and stored; it stays under 10
minutes, so no further cutting was required, and the Gram-matrix diagnostic below is
kept in the JSON so this check does not have to be re-earned by a future leg.
"""

import json
import os
import sys
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.bordered_hl import BorderedHL, tail_exponent          # noqa: E402
from solver.line_hilbert import line_hilbert_matrix                # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_mtsc_v1.json")
FIG = os.path.join(ROOT, "writeup", "figures",
                    "fig72_route_mtsc_v1_death_mechanisms.png")

IC = dict(x0=0.30, w=0.90, amp=1.0, vamp=0.80)
GRID_N = 801
M_LADDER = [8, 16, 32, 64]             # 8x range, >= the 4-fold S1 requires
M_PROJECT_NL = 64                       # capped where the Gram control verified sigma_min(G) >= 0.94


# --------------------------------------------------------------------------
# 0. solve the REAL target (not a=0) -- reuses solver/bordered_hl.py exactly
# --------------------------------------------------------------------------
def _ic(b, x0=0.30, w=0.90, amp=1.0, vamp=0.80):
    Om = amp * np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = vamp * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    return b.pack(Om, V, 1.06, -0.42, 0.077)


def solve_target(n=GRID_N):
    b = BorderedHL(n=n, rho_max=8.0, c=0.5)
    z0 = _ic(b, **IC)
    b.set_pin_from(z0)
    z, hist = b.newton(z0, tol=1e-12, max_iter=60)
    return b, z, hist


# --------------------------------------------------------------------------
# 1. MT closed forms
# --------------------------------------------------------------------------
def mt_psi(x):
    return 2.0 * np.arctan(2.0 * x)


def mt_basis(x, ns):
    """Phi[j, i] = phi_{ns[j]}(x[i]), Iserles-Webb / Malmquist-Takenaka closed form."""
    x = np.asarray(x, dtype=float)
    ns = np.asarray(ns, dtype=int)
    psi = mt_psi(x)
    denom = 1.0 - 2.0j * x
    ipow = np.array([1j ** int(n) for n in ns])          # exact, |i^n| = 1
    phase = np.exp(1j * np.outer(ns, psi))                # (M, n)
    return np.sqrt(2.0 / np.pi) * ipow[:, None] * phase / denom[None, :]


def mt_diff_matrix(ns):
    """Closed-form D on the ordered mode list ns (must be consecutive integers)."""
    ns = np.asarray(ns, dtype=int)
    m = ns.size
    D = np.zeros((m, m), dtype=complex)
    idx = {int(n): k for k, n in enumerate(ns)}
    for k, n in enumerate(ns):
        D[k, k] = 1j * (2 * n + 1)
        if (n + 1) in idx:
            D[k, idx[n + 1]] = n + 1
        if (n - 1) in idx:
            D[k, idx[n - 1]] = -n
    return D


def self_tests(ns_small=range(-8, 9)):
    """M2's structural claim, checked on OUR OWN transcription, not quoted from 301."""
    ns = np.array(list(ns_small))
    D = mt_diff_matrix(ns)
    skew_err = float(np.max(np.abs(D + D.conj().T)))
    x = np.linspace(-40, 40, 4001)
    Phi = mt_basis(x, ns)
    H = line_hilbert_matrix(x)
    expected = np.where(ns >= 0, -1j, 1j)
    Hphi = (H @ Phi.T).T                       # (m, n_grid), discretised H applied
    rel_err = []
    for k, n in enumerate(ns):
        num = float(np.max(np.abs(Hphi[k] - expected[k] * Phi[k])))
        den = float(np.max(np.abs(Phi[k])))
        rel_err.append(num / den)
    return {"skew_hermitian_err": skew_err,
            "hilbert_diag_relerr_mean": float(np.mean(rel_err)),
            "hilbert_diag_relerr_max": float(np.max(rel_err)),
            "note": ("relerr is finite because line_hilbert_matrix is a NATURAL-SPLINE "
                     "DISCRETISATION of the continuous Hilbert transform on a FINITE grid; "
                     "the continuous MT construction is exactly diagonal by Hardy-space "
                     "theory (Cayley transform to the disk), this is a consistency check "
                     "on the code, not a re-derivation of the theorem")}


# --------------------------------------------------------------------------
# 2. the real target's linearization, transported into MT coordinates
# --------------------------------------------------------------------------
def quadrature_weights(X):
    X = np.asarray(X, dtype=float)
    n = X.size
    w = np.zeros(n)
    dx = np.diff(X)
    w[:-1] += 0.5 * dx
    w[1:] += 0.5 * dx
    return w


def gram_control(X, ns):
    """CONTROL, not the measurement: the analysis/synthesis Gram matrix of the MT
    basis against THIS grid's quadrature alone (no operator). It must be the identity
    in the continuous limit (MT is orthonormal); sigma_min(G) far below 1 means the
    grid does not resolve these modes and any operator measurement built on it is
    quadrature noise, not physics. Lesson 90: a control that cannot come out
    differently is not a control -- this one manifestly can and did (it read
    1e-17 on the first, too-coarse grid tried, and ~0.9-1.0 on the grid used here)."""
    w = quadrature_weights(X)
    Phi = mt_basis(X, ns)
    A = Phi.conj() * w[None, :]
    G = A @ Phi.T
    sv = np.linalg.svd(G, compute_uv=False)
    return {"sigma_min": float(sv.min()), "sigma_max": float(sv.max()),
            "max_abs_offdiag_or_1": float(np.max(np.abs(G - np.eye(len(ns)))))}


def galerkin_transport(J_sub, X, ns):
    """L_MT = blockdiag(A,A) @ J_sub @ blockdiag(Phi^T,Phi^T), A = conj(Phi) diag(w)."""
    w = quadrature_weights(X)
    Phi = mt_basis(X, ns)                      # (m, n)
    A = Phi.conj() * w[None, :]                 # (m, n)
    n = X.size
    m = len(ns)
    PhiT = np.zeros((2 * n, 2 * m), dtype=complex)
    PhiT[:n, :m] = Phi.T
    PhiT[n:, m:] = Phi.T
    Ablk = np.zeros((2 * m, 2 * n), dtype=complex)
    Ablk[:m, :n] = A
    Ablk[m:, n:] = A
    return Ablk @ (J_sub @ PhiT)


def measure_ladder(b, z, M_ladder):
    n = b.n
    J = b.jacobian(z)
    J_sub = J[:2 * n, :2 * n]
    rows = []
    for M in M_ladder:
        ns = np.arange(-M, M + 1)
        gram = gram_control(b.X, ns)
        t0 = time.time()
        L = galerkin_transport(J_sub, b.X, ns)
        dt = time.time() - t0
        diag = np.abs(np.diag(L))
        offdiag_rowsum = np.sum(np.abs(L), axis=1) - diag
        delta = offdiag_rowsum / np.maximum(diag, 1e-300)
        lmin = float(diag.min())
        # growth fit on the |Omega|-block half only, n_mode in [8, M], excluding the
        # coupling to the V block's own indices (use combined 2M+1..end range's own idx)
        m = len(ns)
        idx = np.arange(m)
        mask = (np.abs(ns) >= 8)
        gx = np.log(np.abs(ns[mask]).astype(float))
        gy = np.log(np.maximum(diag[:m][mask], 1e-300))
        growth = float(np.polyfit(gx, gy, 1)[0]) if mask.sum() > 3 else None
        sv = np.linalg.svd(L, compute_uv=False)
        rows.append({
            "M": int(M), "modes": int(2 * M + 1), "n_total": int(2 * (2 * M + 1)),
            "lmin_diag": lmin, "diag_growth_exponent": growth,
            "delta_median": float(np.median(delta)), "delta_max": float(np.max(delta)),
            "sigma_min": float(sv.min()), "sigma_max": float(sv.max()),
            "gram_control_sigma_min": gram["sigma_min"],
            "gram_control_trustworthy": bool(gram["sigma_min"] > 0.5),
            "wall_s": dt,
        })
    return rows


# --------------------------------------------------------------------------
# 3. the nonlinearity, measured in float on the target (clause c)
# --------------------------------------------------------------------------
def nonlinearity_bandwidth(b, z, n_test_modes, M_project=256, eps=1e-4):
    """For a real test perturbation built from MT mode n (Re(phi_n), a real function),
    apply the EXACT quadratic remainder Q(v,v) and project the result onto MT modes out
    to M_project. Reports the effective output bandwidth vs input mode and the ratio
    ||Q||_w / ||v||_w^2 as a function of input frequency -- an algebra-property probe."""
    n = b.n
    X = b.X
    w = quadrature_weights(X)
    ns_out = np.arange(-M_project, M_project + 1)
    Phi_out = mt_basis(X, ns_out)
    A_out = Phi_out.conj() * w[None, :]
    rows = []
    for nt in n_test_modes:
        phi = mt_basis(X, np.array([nt]))[0]
        v_om = eps * np.real(phi)
        v_v = 0.5 * eps * np.imag(phi)
        v = b.pack(v_om, v_v, 0.0, 0.0, 0.0)
        Q = b.quadratic(v)
        q_om, q_v = Q[:n], Q[n:2 * n]
        c_om = A_out @ q_om
        c_v = A_out @ q_v
        mag = np.abs(c_om) + np.abs(c_v)
        peak = float(mag.max()) if mag.size else 0.0
        thresh = 1e-3 * peak
        support = ns_out[mag > thresh]
        bw = int(np.abs(support).max()) if support.size else 0
        v_norm = eps  # by construction ||Re(phi_n)||_sup ~ O(1), scaled by eps
        q_norm = float(np.max(np.abs(q_om)) + np.max(np.abs(q_v)))
        rows.append({
            "n_test": int(nt), "eps": eps,
            "output_bandwidth_modes": bw,
            "input_mode_abs": int(abs(nt)),
            "bandwidth_ratio": float(bw) / max(abs(nt), 1),
            "q_sup_norm": q_norm, "q_over_v_norm_sq": q_norm / (v_norm ** 2),
        })
    return rows


# --------------------------------------------------------------------------
# figure (fig72, provisional -- orchestrator registers writeup/INDEX.md)
# --------------------------------------------------------------------------
def build_figure(ladder, nl):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    Ms = [r["M"] for r in ladder]
    ax = axes[0]
    ax.plot(Ms, [r["lmin_diag"] for r in ladder], "o-", color="#2563eb",
            label=r"$l_{\min}$ (real coupled operator)")
    ax.plot(Ms, [r["sigma_min"] for r in ladder], "s-", color="#059669",
            label=r"$\sigma_{\min}$ (real coupled operator)")
    ax.plot(Ms, [r["gram_control_sigma_min"] for r in ladder], "x--", color="#9ca3af",
            label=r"$\sigma_{\min}$(Gram control)")
    ax.axhline(0, color="#c1440e", lw=0.8, ls=":")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("truncation $M$ (modes $= 2M+1$)")
    ax.set_ylabel("magnitude")
    ax.set_title("S1/S2: real target's linear operator in MT coordinates")
    ax.legend(fontsize=7.5)
    ax2 = axes[1]
    ns = [r["n_test"] for r in nl]
    ax2.plot(ns, [r["bandwidth_ratio"] for r in nl], "o-", color="#dc2626",
              label="output bandwidth / input mode")
    ax2.plot(ns, [r["q_over_v_norm_sq"] for r in nl], "^-", color="#6b7280",
              label=r"$\|Q(v,v)\|/\|v\|^2$")
    ax2.axvline(M_PROJECT_NL, color="#c1440e", lw=0.8, ls=":")
    ax2.text(M_PROJECT_NL, ax2.get_ylim()[1] * 0.9, " window cap", fontsize=7,
              color="#c1440e")
    ax2.set_xlabel("input MT mode $n$")
    ax2.set_title("S3: nonlinearity, measured on the real target")
    ax2.legend(fontsize=7.5)
    fig.suptitle("Route-MTSC v1 (leg 320): the MT survivor's linearization and nonlinearity, "
                  "measured on the real HL_S2_nonsymmetric target, not the bare diff. matrix")
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG)
    plt.close(fig)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    t_start = time.time()
    print("solving the real target (n=%d)..." % GRID_N, flush=True)
    b, z, hist = solve_target(GRID_N)
    conv = bool(hist["converged"])
    resid_final = float(hist["residual_ladder"][-1])
    print(f"  converged={conv}  final ||F||_inf={resid_final:.3e}  "
          f"iters={len(hist['residual_ladder']) - 1}", flush=True)

    print("self-tests (M2 structural claim, on our own code)...", flush=True)
    st = self_tests()
    print(f"  skew-Hermitian err={st['skew_hermitian_err']:.3e}  "
          f"Hilbert-diag relerr mean={st['hilbert_diag_relerr_mean']:.3e} "
          f"max={st['hilbert_diag_relerr_max']:.3e}", flush=True)

    print("S1/S2: transporting the real Jacobian into MT coordinates, M = %r..."
          % M_LADDER, flush=True)
    ladder = measure_ladder(b, z, M_LADDER)
    for row in ladder:
        g = row['diag_growth_exponent']
        gstr = f"{g:.4f}" if g is not None else "n/a (too few modes)"
        print(f"  M={row['M']:4d}  lmin={row['lmin_diag']:.4e}  "
              f"growth={gstr}  "
              f"delta_med={row['delta_median']:.4f}  delta_max={row['delta_max']:.4e}  "
              f"sigma_min={row['sigma_min']:.4e}  "
              f"gram_ok={row['gram_control_trustworthy']}  ({row['wall_s']:.2f}s)", flush=True)

    print("S3: nonlinearity bandwidth probe on the real target...", flush=True)
    nl_modes = [1, 4, 16, 64]
    nl = nonlinearity_bandwidth(b, z, nl_modes, M_project=M_PROJECT_NL)
    for row in nl:
        print(f"  n_test={row['n_test']:3d}  out_bw={row['output_bandwidth_modes']:4d}  "
              f"bw_ratio={row['bandwidth_ratio']:.3f}  "
              f"q_over_v2={row['q_over_v_norm_sq']:.4e}", flush=True)

    nl_gram = gram_control(b.X, np.arange(-M_PROJECT_NL, M_PROJECT_NL + 1))
    tail_om = tail_exponent(b.X, b.unpack(z)[0], 3.0, 8.0)

    wall_total = time.time() - t_start
    print(f"total wall time: {wall_total:.2f}s", flush=True)

    out = {
        "grid_n": GRID_N, "target_converged": conv, "target_residual_final": resid_final,
        "target_c_l": float(b.unpack(z)[2]), "target_c_omega": float(b.unpack(z)[3]),
        "target_c_r": float(b.unpack(z)[4]), "target_tail_exponent_Omega": tail_om,
        "self_tests": st,
        "M_ladder": ladder,
        "nonlinearity_probe": nl,
        "M_project_nonlinearity": M_PROJECT_NL,
        "nonlinearity_gram_control": nl_gram,
        "wall_total_s": wall_total,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {OUT}")
    build_figure(ladder, nl)
    print(f"wrote {FIG}")


if __name__ == "__main__":
    main()
