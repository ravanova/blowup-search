"""Gates for solver/energy_coercivity.py -- the weighted-energy (Chen-Hou-shaped)
coercivity form of the `a = 0` CLM linearisation.

The claims under test are the ones Route-WE's conclusion rests on, in the order they are
used:

  (i)   the operator in this file IS `solver/spectral_certificate.py`'s operator -- checked
        two ways, pointwise-vs-matrix and matrix-vs-that-module, so the third realization
        is provably measured on the same object the first two died on;
  (ii)  the two PUBLISHED point-spectrum modes (Xu arXiv:2607.19762) are reproduced to
        machine precision, which is this leg's known-answer window;
  (iii) the quadrature is right -- the flat-weight Gram matrix is exactly `(pi/2) I`;
  (iv)  the damping factor's closed form is the derivative it claims to be;
  (v)   admissibility is MEASURED (`gamma < 3` converges, `gamma = 3` log-diverges,
        `gamma = 4` power-diverges) rather than asserted;
  (vi)  the gap respects the external ceiling `1/2` and the raw gap respects the published
        eigenvalue `1`;
  (vii) the POSITIVE CONTROL can report the other answer -- with `mu` large enough the
        gap goes positive, so a negative gap at `mu = 0` is a measurement and not a
        property of the code.
"""

import sys

import numpy as np

sys.path.insert(0, ".")

from solver.energy_coercivity import (
    KNOWN_ANSWER_CEILING, WEIGHT_FAMILY, admissibility, clm_linearization_matrix,
    clm_linearization_values, coercivity_gap, damping_factor, damping_factor_at_origin,
    form_matrices, graded_quadrature, known_modes, weight_values,
)
from solver.spectral_certificate import bordered_linearization

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


TH = np.linspace(0.07, np.pi - 0.07, 41)

# 1 -- the pointwise operator and the coefficient matrix are the same operator
_n = 24
_M = clm_linearization_matrix(_n)
_worst = 0.0
for _k in (1, 2, 3, 7, 12):                       # k < n so no column falls off the end
    _exact = clm_linearization_values(TH, _k)
    _via_matrix = sum(_M[_j - 1, _k - 1] * np.sin(_j * TH) for _j in range(1, _n + 1))
    _worst = max(_worst, float(np.max(np.abs(_exact - _via_matrix))))
gate("pointwise operator == coefficient matrix", _worst < 1e-13,
     f"max |L e_k (closed form) - sum_j M_jk sin j th| = {_worst:.2e} over k = 1,2,3,7,12")

# 2 -- and that matrix IS spectral_certificate's, so this is the SAME OBJECT legs 51-54
#      measured dead.  `bordered_linearization` adds a gauge row and a border column; the
#      interior block (rows/cols 1..K-1, since its own k=K column drops the k+1 entry) is
#      what must agree.
_K = 24
_F = bordered_linearization(_K)[: _K - 1, : _K - 1]
_G = clm_linearization_matrix(_K)[: _K - 1, : _K - 1]
gate("operator == solver/spectral_certificate.py's", float(np.max(np.abs(_F - _G))) == 0.0,
     f"max |bordered_linearization - clm_linearization_matrix| on the interior "
     f"{_K - 1}x{_K - 1} block = {float(np.max(np.abs(_F - _G))):.1e} (exactly zero)")

# 3 -- the KNOWN ANSWER: the two published point-spectrum modes, to machine precision
_mode_err = []
for _lam, _c in known_modes():
    _im = sum(_c[_j] * clm_linearization_values(TH, _j + 1) for _j in range(len(_c)))
    _tg = _lam * sum(_c[_j] * np.sin((_j + 1) * TH) for _j in range(len(_c)))
    _mode_err.append(float(np.max(np.abs(_im - _tg))))
gate("published point spectrum {0,1} reproduced", max(_mode_err) < 1e-14,
     f"|L(sin 2th) - 0| = {_mode_err[0]:.1e}, "
     f"|L(sin th + sin 2th/2) - (sin th + sin 2th/2)| = {_mode_err[1]:.1e} "
     f"(Xu arXiv:2607.19762: point spectrum is exactly {{0,1}})")

# 4 -- the quadrature is right where the answer is known: flat weight => Gram = (pi/2) I.
#      This is the gate that caught a purely geometric mesh reporting cond(G) = 7e10 for a
#      matrix that is exactly diagonal, because its interior panels were wider than a
#      wavelength of sin(64 th).
_Gm, _ = form_matrices(64, "A", 0.0)
_gerr = float(np.max(np.abs(_Gm - np.eye(64) * np.pi / 2)))
gate("flat-weight Gram matrix is exactly (pi/2) I", _gerr < 1e-13,
     f"max |G - (pi/2) I| = {_gerr:.2e} at n = 64 -- the quadrature resolves mode 64")

# 5 -- and the quadrature weights sum to the length of the interval, for every weight that
#      is integrable, so the mesh itself is not losing mass
_th, _qw = graded_quadrature()
gate("quadrature is consistent", abs(float(np.sum(_qw)) - np.pi) < 1e-12,
     f"sum of weights - pi = {float(np.sum(_qw)) - np.pi:.2e}")

# 6 -- the damping factor's closed form is the derivative it says it is
_dwors = 0.0
for _nm, _f, _g in WEIGHT_FAMILY:
    _h = 1e-6
    _lp = (np.log(weight_values(TH + _h, _f, _g)) - np.log(weight_values(TH - _h, _f, _g))) / (2 * _h)
    _fd = 1.5 * np.cos(TH) + 0.5 * np.sin(TH) * _lp
    _dwors = max(_dwors, float(np.max(np.abs(_fd - damping_factor(TH, _f, _g)))))
gate("damping factor closed form == (3/2)cos th + (1/2) sin th (log phi)'", _dwors < 1e-6,
     f"max |closed form - central difference| = {_dwors:.2e} over all 7 named weights")

# 7 -- D(0) = (3 - gamma)/2 in both families: damping AT THE ORIGIN needs gamma > 3
_d0 = {nm: damping_factor_at_origin(f, g) for nm, f, g in WEIGHT_FAMILY}
_ok = all(abs(_d0[nm] - (3.0 - g) / 2.0) < 1e-12 for nm, f, g in WEIGHT_FAMILY)
gate("D(0) = (3 - gamma)/2, so local damping needs gamma > 3", _ok,
     "D(0) = " + ", ".join(f"{k}:{v:+.2f}" for k, v in _d0.items()))

# 8 -- ADMISSIBILITY IS MEASURED.  gamma < 3 converges (ratio 1), gamma = 3 LOG-diverges
#      (doubling the grading depth doubles the integral: ratio ~ 2), gamma = 4 power-
#      diverges.  So the exponent that would give damping is the exponent at which the
#      space stops containing the basis.
_adm = {nm: admissibility(f, g) for nm, f, g in WEIGHT_FAMILY}
_conv = [nm for nm, f, g in WEIGHT_FAMILY if g < 3]
gate("gamma < 3: the weighted norm converges",
     all(abs(_adm[nm]["ratio"] - 1.0) < 1e-6 for nm in _conv),
     "ratios " + ", ".join(f"{nm}:{_adm[nm]['ratio']:.6f}" for nm in _conv))
gate("gamma = 3 and gamma = 4 both diverge",
     _adm["A3"]["ratio"] > 1.5 and _adm["A4_chen_hou"]["ratio"] > 1e5,
     f"A3 ratio = {_adm['A3']['ratio']:.4f}, A4 ratio = {_adm['A4_chen_hou']['ratio']:.3e} "
     f"(admissible members are 1.000000 to six places)")

# 8b -- and the SHAPE of each divergence, which is mesh-independent where `ratio` is not:
#       equally spaced grading depths give EQUAL increments for a log divergence and
#       GEOMETRICALLY GROWING ones for a power divergence.
gate("gamma = 3 diverges LOGARITHMICALLY, gamma = 4 by a POWER",
     abs(_adm["A3"]["increment_ratio"] - 1.0) < 0.05
     and _adm["A4_chen_hou"]["increment_ratio"] > 100.0
     and all(_adm[nm]["increment_ratio"] is None for nm, f, g in WEIGHT_FAMILY if g < 3),
     f"increment ratio over equally spaced grading depths: A3 = "
     f"{_adm['A3']['increment_ratio']:.6f} (1 = logarithmic), A4 = "
     f"{_adm['A4_chen_hou']['increment_ratio']:.3e} (= {_adm['A4_chen_hou']['increment_ratio'] ** 0.5:.0f}^2, "
     f"a power); every admissible member reports None -- converged, so the shape of a "
     f"divergence has no referent there")

# 9 -- the RAW (unmodulated) gap can never exceed -1, because the published eigenvalue 1
#      has its eigenfunction in the trial space for every n >= 2
_raw = {nm: coercivity_gap(48, f, g, modulate=False)["gap"]
        for nm, f, g in WEIGHT_FAMILY if g < 3}
gate("raw gap <= -1 for every admissible weight (published eigenvalue 1)",
     max(_raw.values()) <= -1.0 + 1e-9,
     "raw gaps " + ", ".join(f"{k}:{v:+.4f}" for k, v in _raw.items()))

# 10 -- and the MODULATED gap can never exceed 1/2, because the numerical range contains
#       the essential spectrum, which sits on Re lambda = -1/2.  A value above this is an
#       instrument bug, not a result.
_mod = {nm: coercivity_gap(48, f, g)["gap"] for nm, f, g in WEIGHT_FAMILY}
gate(f"modulated gap <= the published ceiling {KNOWN_ANSWER_CEILING}",
     max(_mod.values()) <= KNOWN_ANSWER_CEILING + 1e-9,
     f"largest modulated gap over the family = {max(_mod.values()):+.5f} "
     f"(Xu arXiv:2607.19762 ceiling {KNOWN_ANSWER_CEILING})")

# 11 -- modulation removes exactly the two published modes and nothing else
_r = coercivity_gap(32, "A", 2.0)
gate("modulation removes exactly 2 directions", _r["dim_trial"] == 30,
     f"trial dimension {_r['dim_trial']} of 32 after removing the scaling and "
     f"time-shift modes; dropped by conditioning = {_r['dropped']}, cond(G) = {_r['cond_G']:.3g}")

# 12 -- THE POSITIVE CONTROL, and it can report the other answer.  `-mu*Lambda` turns the
#       unbounded part from a shift into a MULTIPLIER; nothing else changes.
_ctrl = [(mu, coercivity_gap(48, "A", 2.0, mu=mu)["gap"]) for mu in (0.0, 0.5, 2.0)]
gate("positive control goes POSITIVE once the operator is a multiplier",
     _ctrl[0][1] < 0 < _ctrl[-1][1] and _ctrl[0][1] < _ctrl[1][1] < _ctrl[-1][1],
     "gap at mu = " + ", ".join(f"{m}:{g:+.4f}" for m, g in _ctrl) +
     " -- monotone in mu and the sign flips, so a negative gap at mu = 0 is a measurement")

# 13 -- the gap is a Rayleigh quotient over NESTED subspaces, so it must be non-increasing
#       in n.  A refinement ladder that wanders is a bug in the trial space.
_lad = [coercivity_gap(n, "A", 2.0)["gap"] for n in (8, 16, 32, 64)]
gate("gap is monotone non-increasing in n (nested trial spaces)",
     all(_lad[i + 1] <= _lad[i] + 1e-9 for i in range(len(_lad) - 1)),
     "ladder " + " -> ".join(f"{v:+.6f}" for v in _lad))

# 14 -- and it converges to -D(0) = -(3 - gamma)/2, the concentration limit: the sup of the
#       Rayleigh quotient is attained by concentrating at the origin, where the damping
#       factor is worst.  This is the mechanism, checked, not asserted.
_conc = {}
for _nm, _f, _g in WEIGHT_FAMILY:
    if _g < 3:
        _conc[_nm] = (coercivity_gap(128, _f, _g)["gap"], -(3.0 - _g) / 2.0)
gate("gap -> -(3 - gamma)/2, the value of the damping factor at the origin",
     all(abs(v - p) < 0.01 for v, p in _conc.values()),
     ", ".join(f"{k}: {v:+.5f} vs {p:+.3f}" for k, (v, p) in _conc.items()))


n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
sys.exit(1 if n_fail else 0)
