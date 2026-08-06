"""Adversarial gates for `solver/energy_coercivity.py` (leg 144, Route-ECA).

`test_energy_coercivity.py` validates this module on WELL-FORMED inputs: the operator
against `solver/spectral_certificate.py`, Xu's two published point-spectrum modes, the
flat-weight Gram matrix, the damping factor's closed form, the admissible members'
convergence, the `mu` positive control.  Every input in that file is legal and in-domain.

This file validates the other half -- what the module returns for inputs that are inside its
public API's REACHABLE domain but outside the domain its own docstrings declare -- and banks
leg 144's battery so the answer cannot silently regress.

The gate leg 144 answered, verbatim (frozen in `writeup/novelty/leg_144.md` before any
number was computed):

  "Does solver/energy_coercivity.py contain a silent-corruption site -- an input inside its
   public API's reachable domain for which it returns a finite, plausible number instead of
   refusing, warning, or reporting the quantity as absent?"

Answered **YES**, on six sites.  Leg 144 had no patch authority under its own gate and
ESCALATED; `solver/energy_coercivity.py` is byte-identical to the merge base.  Gates 1-6
below are therefore CHARACTERIZATION gates: they assert that the gap is still open, and they
carry leg 144's measured magnitude in the assertion message.

**IF ONE OF GATES 1-6 FAILS, THAT IS PROBABLY GOOD NEWS** -- someone has repaired the module.
The correct response is to read `experiments/journal/leg_144.md`, confirm the repair, and
convert the characterization gate into a SOUNDNESS gate asserting the repaired property (the
template is `test_first_integral_adversarial.py`, leg 107's battery after its bench repair).
It must NOT be "fixed" by loosening a tolerance or deleting a gate.

Gates 7-9 are SOUNDNESS gates that hold today and must keep holding: the guards that DO work,
and the control (C1) that stops this file from being a statement about the environment.

Run:  .venv/bin/python test_energy_coercivity_adversarial.py
"""

import json
import math
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver import energy_coercivity as ec

HERE = os.path.dirname(os.path.abspath(__file__))
LEG111 = os.path.join(HERE, "writeup", "data", "p2_route_we_v1_coercivity.json")

PASS, FAIL = "PASS", "FAIL"
_results = []


def gate(name, ok, detail):
    _results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


def capture(fn, *a, **k):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            value, err = fn(*a, **k), None
        except Exception as exc:                                  # noqa: BLE001
            value, err = None, f"{type(exc).__name__}: {exc}"
    return value, err, [str(w.message) for w in caught]


# ---------------------------------------------------------------------------
# 1 (CHARACTERIZATION) -- the gap function never consults admissibility, so a weight whose
#     space does not contain the trial basis still gets a finite, unwarned number back.
# ---------------------------------------------------------------------------
_val, _err, _warns = capture(ec.coercivity_gap, 48, "A", 4.0)
_adm4 = ec.admissibility("A", 4.0)
gate("inadmissible weight still returns a finite gap, silently",
     _err is None and _warns == [] and np.isfinite(_val["gap"]),
     f"gamma=4 has admissibility ratio {_adm4['ratio']:.3e} (power-divergent, shape "
     f"{_adm4['increment_ratio']:.0f}) yet coercivity_gap(48,'A',4.0) returns "
     f"{_val['gap']:+.6f} with {len(_warns)} warnings and no error "
     f"[leg 144 measured -3.346922; a repair should refuse or warn here]")

# ---------------------------------------------------------------------------
# 2 (CHARACTERIZATION) -- and that number violates the module's OWN invariant.  The trial
#     spaces are nested, so the Rayleigh sup is non-increasing in n (test_energy_coercivity.py
#     gate 13 asserts exactly this, at gamma = 2 only).
# ---------------------------------------------------------------------------
_lad4 = [ec.coercivity_gap(n, "A", 4.0)["gap"] for n in (8, 16, 32, 64)]
_lad2 = [ec.coercivity_gap(n, "A", 2.0)["gap"] for n in (8, 16, 32, 64)]
_worst4 = max(_lad4[i + 1] - _lad4[i] for i in range(3))
_worst2 = max(_lad2[i + 1] - _lad2[i] for i in range(3))
gate("the inadmissible ladder violates the nested-subspace invariant, the admissible one does not",
     _worst4 > 1e-9 and _worst2 <= 1e-9,
     f"gamma=4 ladder " + " -> ".join(f"{v:+.4f}" for v in _lad4) +
     f" (worst INCREASE {_worst4:+.4f}); gamma=2 control " +
     " -> ".join(f"{v:+.6f}" for v in _lad2) + f" (worst {_worst2:+.1e}, non-increasing)")

# ---------------------------------------------------------------------------
# 3 (CHARACTERIZATION) -- admissibility()'s divergence detector reports CONVERGED, in its own
#     docstring's reading, when its grading depth is switched off through its public kwarg.
#     This is the highest-stakes site: admissibility() is what defines the gamma < 3 edge of
#     leg 111's zero-width window.
# ---------------------------------------------------------------------------
_a24 = ec.admissibility("A", 4.0, n_grade=24)
_a0 = ec.admissibility("A", 4.0, n_grade=0)
_reads_converged = abs(_a0["ratio"] - 1.0) < 1e-12 and _a0["increment_ratio"] is None
gate("admissibility(n_grade=0) reports a power-divergent weight as converged",
     _reads_converged and _a24["ratio"] > 1e6,
     f"gamma=4: n_grade=24 -> ratio {_a24['ratio']:.6e}, increments "
     f"{_a24['increments'][0]:.3e}/{_a24['increments'][1]:.3e}, increment_ratio "
     f"{_a24['increment_ratio']:.1f} (a power); n_grade=0 -> ratio {_a0['ratio']:.6f}, "
     f"increments [0, 0], increment_ratio None -- which the module's own docstring reads as "
     f"'the integral has CONVERGED'. Suppression factor {_a24['ratio'] / _a0['ratio']:.3e}. "
     f"Only exponent_margin = {_a0['exponent_margin']:+.1f} still tells the truth, and it is "
     f"computed from gamma alone, not measured")

# ---------------------------------------------------------------------------
# 4 (CHARACTERIZATION) -- graded_quadrature(grade >= 1) silently returns an UNGRADED mesh
#     whose total mass is still exactly pi, so the module's own consistency gate
#     (test_energy_coercivity.py gate 5) cannot see it; and grade > 1 puts nodes outside
#     (0, pi) entirely.
# ---------------------------------------------------------------------------
_th_d, _qw_d = ec.graded_quadrature()
_th_1, _qw_1 = ec.graded_quadrature(grade=1.0)
_th_15, _qw_15 = ec.graded_quadrature(grade=1.5)
_out15 = int(np.sum((_th_15 <= 0.0) | (_th_15 >= math.pi)))


def _ratio(gam, gr):
    def n2(ng):
        th, qw = ec.graded_quadrature(n_grade=ng, grade=gr)
        return float(np.sum(np.sin(th) ** 2 * ec.weight_values(th, "A", gam) * qw))
    return n2(48) / n2(24)


gate("grade >= 1 silently un-grades the mesh; grade > 1 leaves the interval",
     abs(float(np.sum(_qw_1)) - math.pi) < 1e-12 and _th_1.min() > 1e-6
     and _out15 > 0 and float(np.sum(_qw_15)) > 100.0,
     f"grade=1.0: total mass {float(np.sum(_qw_1)):.9f} (exactly pi, so the mass gate still "
     f"passes) but the innermost node moves {_th_d.min():.3e} -> {_th_1.min():.3e}, which "
     f"turns the gamma=4 divergence ratio {_ratio(4.0, 0.5):.3e} into {_ratio(4.0, 1.0):.6f}; "
     f"grade=1.5: {_out15}/{_th_15.size} nodes outside (0, pi), total mass "
     f"{float(np.sum(_qw_15)):.3f} = {float(np.sum(_qw_15)) / math.pi:.1f}x the interval, "
     f"min node {_th_15.min():.3e}")

# ---------------------------------------------------------------------------
# 5 (CHARACTERIZATION) -- n_unif = 1 makes the two end panels each span the whole interval,
#     so every node is counted twice: the measure of (0, pi) comes back as 2 pi.
# ---------------------------------------------------------------------------
_th_u1, _qw_u1 = ec.graded_quadrature(n_unif=1)
_G1, _ = ec.form_matrices(8, "A", 0.0, n_unif=1)
_g32_def = ec.coercivity_gap(32, "A", 2.0)["gap"]
_g32_u1 = ec.coercivity_gap(32, "A", 2.0, n_unif=1)["gap"]
gate("n_unif=1 doubles the measure of the interval, silently",
     abs(float(np.sum(_qw_u1)) / math.pi - 2.0) < 1e-12
     and abs(_G1[0, 0] / (math.pi / 2) - 2.0) < 1e-12,
     f"total mass {float(np.sum(_qw_u1)):.9f} = {float(np.sum(_qw_u1)) / math.pi:.6f} x pi; "
     f"flat-weight Gram diagonal {_G1[0, 0]:.8f} instead of pi/2 = {math.pi / 2:.8f} "
     f"(ratio exactly 2); the gap agrees with the default to "
     f"{abs(ec.coercivity_gap(8,'A',2.0)['gap'] - ec.coercivity_gap(8,'A',2.0,n_unif=1)['gap']):.1e} "
     f"at n=8 -- where a person would sanity-check it -- and is {_g32_u1:+.4f} vs "
     f"{_g32_def:+.4f} at n=32 ({abs(_g32_u1 / _g32_def):.1f}x)")

# ---------------------------------------------------------------------------
# 6 (CHARACTERIZATION) -- weight_values is silently EVEN and PERIODIC: off the declared
#     domain (0, pi) it returns the mirror of an in-domain point, finite and unwarned.  Same
#     shape as leg 107's finding in solver/first_integral.py (an even function erasing the
#     branch that defines the domain), in a different module.
# ---------------------------------------------------------------------------
_wp = float(ec.weight_values(np.array([0.1]), "A", 2.0)[0])
_wm = float(ec.weight_values(np.array([-0.1]), "A", 2.0)[0])
_wn3 = float(ec.weight_values(np.array([-0.1]), "A", 3.0)[0])
_v25, _e25, _warn25 = capture(ec.weight_values, np.array([-0.1]), "A", 2.5)
_wwrap = float(ec.weight_values(np.array([2 * math.pi + 0.1]), "A", 2.0)[0])
_, _, _warn_m = capture(ec.weight_values, np.array([-0.1]), "A", 2.0)
gate("weight_values mirrors and wraps outside (0, pi) instead of refusing",
     _wm == _wp and _warn_m == [] and _wn3 < 0.0 and abs(_wwrap - _wp) < 1e-11,
     f"theta=-0.1 returns {_wm:.8f}, BIT-IDENTICAL to theta=+0.1 ({_wp:.8f}), no warning; "
     f"at gamma=3 the same input returns a NEGATIVE weight {_wn3:+.4f} (an indefinite "
     f"'inner product'); at gamma=2.5 it returns {_v25[0]} with "
     f"{len(_warn25)} warning(s); theta=2pi+0.1 wraps to {_wwrap:.8f} "
     f"({abs(_wwrap - _wp):.1e} from the in-domain value)")

# ---------------------------------------------------------------------------
# 7 (CHARACTERIZATION) -- a trial space smaller than the modulation it is asked to quotient
#     out returns a positive gap that SATURATES the published ceiling from below, so the
#     module's own instrument-bug tripwire (a `<=` test against KNOWN_ANSWER_CEILING) cannot
#     fire.  n = 1 and n = 2 raise loudly, which is the control: the failure is specific.
# ---------------------------------------------------------------------------
_r3 = ec.coercivity_gap(3, "A", 2.0)
_e1 = capture(ec.coercivity_gap, 1, "A", 2.0)[1]
_e2 = capture(ec.coercivity_gap, 2, "A", 2.0)[1]
gate("n=3 saturates the published ceiling from a 1-dimensional trial space",
     _r3["gap"] > 0 and _r3["dim_trial"] == 1
     and _r3["gap"] <= ec.KNOWN_ANSWER_CEILING
     and abs(_r3["gap"] - ec.KNOWN_ANSWER_CEILING) < 1e-14
     and _e1 is not None and _e2 is not None,
     f"gap = {_r3['gap']:.16f} at n=3, gamma=2, dim_trial={_r3['dim_trial']} -- "
     f"{abs(_r3['gap'] - ec.KNOWN_ANSWER_CEILING):.1e} below the published ceiling "
     f"{ec.KNOWN_ANSWER_CEILING}, so `gap <= ceiling` still passes; the converged value at "
     f"n=48 is {ec.coercivity_gap(48, 'A', 2.0)['gap']:+.6f}. n=1 raises ({_e1.split(':')[0]}), "
     f"n=2 raises ({_e2.split(':')[0]}) -- the module CAN fail loudly, so this is specific")

# ---------------------------------------------------------------------------
# 8 (SOUNDNESS) -- the guard that DOES work, on every public entry point.  C3 of the novelty
#     log: a battery in which nothing raises has not reached the guards.
# ---------------------------------------------------------------------------
_guards = {
    "weight_values": capture(ec.weight_values, np.array([1.0]), "Z", 2.0)[1],
    "weight_values('b')": capture(ec.weight_values, np.array([1.0]), "b", 2.0)[1],
    "damping_factor": capture(ec.damping_factor, np.array([1.0]), "Z", 2.0)[1],
    "damping_factor_at_origin": capture(ec.damping_factor_at_origin, "Z", 2.0)[1],
    "form_matrices": capture(ec.form_matrices, 8, "Z", 2.0)[1],
    "coercivity_gap": capture(ec.coercivity_gap, 8, "Z", 2.0)[1],
    "admissibility": capture(ec.admissibility, "Z", 2.0)[1],
}
gate("the unknown-family guard is reachable on every public entry point",
     all(e is not None and e.startswith("ValueError") for e in _guards.values()),
     f"{sum(1 for e in _guards.values() if e)}/{len(_guards)} entry points raise ValueError: "
     + ", ".join(sorted(_guards)))

# ---------------------------------------------------------------------------
# 9 (SOUNDNESS, and the CONTROL for the whole file) -- the members leg 111's conclusion rests
#     on reproduce its banked JSON to machine precision, while the power-divergent member
#     does not reproduce at all.  Without this gate, every number above could be a statement
#     about this machine (lesson 90).
# ---------------------------------------------------------------------------
_banked = json.load(open(LEG111))
_repro = {}
for _nm, _fam, _gam in ec.WEIGHT_FAMILY:
    _now = [ec.coercivity_gap(n, _fam, _gam)["gap"] for n in (16, 32, 64)]
    _bank = _banked["gaps"][_nm]["modulated"][:3]
    _repro[_nm] = max(abs(a - b) for a, b in zip(_now, _bank))
_ok = [k for k, v in _repro.items() if v < 1e-12]
gate("leg 111's ADMISSIBLE ladders reproduce bit-for-bit; the inadmissible one does not",
     len(_ok) == 6 and "A4_chen_hou" not in _ok and _repro["A4_chen_hou"] > 1e-3,
     f"{len(_ok)}/7 members reproduce to <= {max(_repro[k] for k in _ok):.1e} absolute "
     f"({', '.join(sorted(_ok))}); A4_chen_hou differs by {_repro['A4_chen_hou']:.4f} "
     f"absolute over n=16,32,64 -- deterministic within one environment, not across builds. "
     f"So the flags above are properties of the MODULE, not of this machine")


_n_fail = sum(1 for s, _, _ in _results if s == FAIL)
print(f"\n{len(_results) - _n_fail}/{len(_results)} gates pass")
if _n_fail == 0:
    print("All leg-144 adversarial gates hold: 7 CHARACTERIZATION gates assert the six "
          "silent-corruption sites are still open (module untouched, ESCALATED not patched) "
          "and 2 SOUNDNESS gates hold. A failure in gates 1-7 probably means a repair "
          "landed -- see experiments/journal/leg_144.md before touching this file.")
sys.exit(1 if _n_fail else 0)
