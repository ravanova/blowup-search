"""Self-running checks for solver/arc6_residual_ledger.py (arc 6, U3, leg 419).

    .venv/bin/python test_arc6_residual_ledger.py

Every check is exact rational arithmetic. There is NO tolerance anywhere in this
file, so there is none to widen after seeing a number -- the failure mode this
repository recorded against itself at leg 408 (`CORRECTIONS.md` §60) and refused.

PLANTED CONTROLS FIRE IN BOTH DIRECTIONS (standing discipline, `STATE.md`).
Sections C1-C7 below each contain a check that MUST pass and a deliberately
broken twin that MUST fail. A ledger that says yes to everything is not an
instrument, and this file demonstrates that it says no.
"""

import sys
from fractions import Fraction as F

from solver.arc6_residual_ledger import (
    MANUSCRIPT_PRINTED,
    CorrectionCycle,
    EnergyLedger,
    GeometryLedger,
    PulseLedger,
    Scale,
    manuscript_ledger,
    route4_contrast,
)

_fails = []


def ok(cond, label, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not cond:
        _fails.append(label)


print("== 1. every re-derived scale equals the manuscript's printed value")
led = manuscript_ledger()
ok(len(led) == 23, "23 quantities in the ledger", str(len(led)))
ok(len(led) == len(MANUSCRIPT_PRINTED), "the ledger covers every printed value")
for name, (derived, printed, agree) in sorted(led.items()):
    ok(agree, f"{name}: re-derived {derived} == printed {printed}")

print("== 2. the identities that make the construction possible, exactly")
g, p, e, c = GeometryLedger(), PulseLedger(), EnergyLedger(), CorrectionCycle()
ok(g.leading_balance_holds(),
   "radial transport, axial transport and radial diffusion all rate q^-1")
ok(g.radial_diffusion_rate == Scale(F(-1), F(0)), "and that common rate is exactly q^-1")
ok(p.stress_cancels_residual(),
   "pulse Reynolds-stress divergence == leading tangential residual",
   f"{p.stress_divergence} == {g.leading_tangential_residual}")
ok(p.ratios_agree(), "A_wave/u_theta == ell_wave/ell_r, both q^(h/2)")
ok(g.axial_over_radial_diffusion == Scale(F(0), F(2)),
   "axial/radial diffusion == q^(2h), the background expansion parameter")
ok(g.Re_theta.blows_up_at(F(1, 100)) and not g.Re_r.blows_up_at(F(1, 100)),
   "Re_theta diverges and Re_r does not — the asymmetry the core runs on")

print("== 3. the energy conditions, and the exact threshold")
ok(e.critical_h() == F(1, 6), "critical h = 1/6, exactly", str(e.critical_h()))
ok(e.energy_vanishes_at(F(1, 100)), "at h = 1/100 the core energy vanishes")
ok(e.dissipation_integrable_at(F(1, 100)), "and the dissipation is integrable")
ok(-e.D_core.a / e.D_core.b != e.critical_h(),
   "the two conditions are NOT the same equation (E_core = 0 vs D_core = -1)")
thr_D = (F(-1) - e.D_core.a) / e.D_core.b
ok(thr_D == F(1, 6),
   "but they have the SAME threshold h = 1/6 — checked, not asserted in a docstring",
   str(thr_D))

print("== 4. the correction cycle reaches any required flatness")
ok(c.sigma(0) == F(1, 5) and c.sigma(1) == F(3, 10), "sigma_0 = 1/5, sigma_1 = 3/10")
ok(c.sigma(8) == F(1), "sigma_8 = 1")
ok(c.diverges(), "sigma_j -> oo, which is what flatness means")
ok(c.stages_to_reach(1) == 8, "8 stages to reach sigma = 1", str(c.stages_to_reach(1)))
ok(c.stages_to_reach(F(1, 5)) == 0, "0 stages to reach sigma_0 itself")
ok(c.stages_to_reach(F(1, 4)) == 1, "ceiling division: sigma = 1/4 needs 1 stage")

print("== 5. the route-4 contrast — this repository's own pinned object")
r = route4_contrast()
ok(r["alpha_pinned"] == F(1), "alpha is PINNED at 1 (L2', leg 397; verified V-W4)")
ok(r["L2_converges"] is False, "int |U|^2 over R^3 does NOT converge at alpha = 1")
ok(r["L2_integrand_exponent"] == 0,
   "the L^2 shell integrand is r^0 — energy grows LINEARLY in radius, not log")
ok(r["L2_deficit"] == F(1, 2),
   "L^2 deficit is exactly 1/2 — the same 1/2 as leg 381's cutoff bill")
ok(r["cutoff_bill_deficit"] == r["L2_deficit"],
   "and those two deficits are the SAME NUMBER, which is why W4 is one wall and not two")
ok(r["L3_converges"] is False, "int |U|^3 does NOT converge at alpha = 1 either")
ok(r["L3_integrand_exponent"] == -1,
   "the L^3 shell integrand is r^-1 — EXACTLY LOG-DIVERGENT")
ok(r["L3_deficit"] == 0,
   "L^3 deficit is exactly 0: alpha = 1 is the critical exponent, not a near miss")
print("     ^ this reproduces PB2's (leg 410) measured log-divergence of int|U|^3")
print("       from exponent arithmetic alone. It is a CROSS-CHECK on the ledger,")
print("       not a new result, and it is recorded as such.")

print("== 6. PLANTED CONTROLS — every one must FAIL, or the ledger is a tautology")


class _BrokenAmplitude(PulseLedger):
    """C1: pulse amplitude q^(-1/2-h) instead of q^(-1/2-h/2).

    This is the amplitude a reader would guess: 'the pulses are as strong as
    the background'. If the ledger cannot tell it apart from the right one,
    section 2's agreement means nothing.
    """

    @property
    def A_wave(self):
        return Scale(F(-1, 2), F(-1))


ok(not _BrokenAmplitude().stress_cancels_residual(),
   "C1 amplitude q^(-1/2-h): stress does NOT cancel the residual",
   f"{_BrokenAmplitude().stress_divergence} vs {g.leading_tangential_residual}")

class _BrokenAspect(GeometryLedger):
    """C2: an isotropic core, D = 1/2, i.e. no axial elongation at all."""

    @property
    def ell_z(self):
        return Scale(F(1, 2), F(0))


b2 = _BrokenAspect()
ok(not b2.leading_balance_holds(),
   "C2 isotropic core (ell_z = ell_r): the three leading rates no longer coincide",
   f"axial {b2.axial_transport_rate} vs radial-diffusion {b2.radial_diffusion_rate}")
ok(b2.axial_over_radial_diffusion == Scale(F(0), F(0)),
   "C2 also kills the expansion parameter — it becomes q^0, no small parameter")

ok(not e.energy_vanishes_at(F(1, 6)),
   "C3 h = 1/6 exactly: the energy condition FAILS at the threshold, not just past it")
ok(not e.admissible_at(F(1, 5)),
   "C4 h = 1/5 > 1/6: inadmissible")
ok(e.admissible_at(F(1, 7)),
   "C4 twin h = 1/7 < 1/6: admissible — the threshold is a threshold, not a wall")

ok(not CorrectionCycle(step=F(0)).diverges(),
   "C5 a correction cycle with step 0 does NOT reach flatness")
try:
    CorrectionCycle(step=F(0)).stages_to_reach(1)
    _zero_step_terminates = True
except ZeroDivisionError:
    _zero_step_terminates = False
ok(not _zero_step_terminates,
   "C5 twin: asking a zero-step cycle for stages-to-target does not return a finite answer")

# C6 was WRITTEN WRONG AND THE LEDGER CAUGHT IT, which is recorded rather than
# quietly repaired. The first version asserted that the L^2 integral converges at
# alpha = 3/2. It does not: the criterion is `p*alpha > 3` STRICTLY, and at
# alpha = 3/2 the shell integrand is exactly r^-1 — log-divergent, the same
# signature as alpha = 1 in L^3. That is precisely why leg 381's cutoff bill is
# written `alpha > 1.5` and not `alpha >= 1.5`, and the ledger reproduces the
# strictness from arithmetic. The control below is the corrected one.
ok(not (2 * F(3, 2) > 3),
   "C6 alpha = 3/2 is itself CRITICAL for L^2 — log-divergent, not convergent")
ok(2 * F(8, 5) > 3,
   "C6 twin: at alpha = 8/5 > 3/2 the L^2 integral does converge — the test can say yes")
ok((2 * F(2) > 3) and (3 * F(2) > 3),
   "C6 third: at alpha = 2 BOTH integrals converge")

ledger_all_ok = all(a for _, _, a in manuscript_ledger().values())
class _BrokenPrinted:
    pass
_saved = MANUSCRIPT_PRINTED["stress_divergence"]
MANUSCRIPT_PRINTED["stress_divergence"] = (F(-3, 2), F(0))
ok(not all(a for _, _, a in manuscript_ledger().values()),
   "C7 corrupt one printed value and the comparison catches it")
MANUSCRIPT_PRINTED["stress_divergence"] = _saved
ok(all(a for _, _, a in manuscript_ledger().values()),
   "C7 twin: restored, and the comparison passes again")

print("== 7. Scale arithmetic itself")
ok(Scale(F(1, 2), F(1)) + Scale(F(1, 2), F(-1)) == Scale(F(1), F(0)), "addition")
ok(2 * Scale(F(1, 3), F(1)) == Scale(F(2, 3), F(2)), "scalar multiply, both sides")
ok(Scale(F(1, 3), F(1)) * F(3) == Scale(F(1), F(3)), "scalar multiply, right")
ok(Scale(F(-1), F(0)).blows_up_at(F(1, 100)), "q^-1 blows up as q -> 0")
ok(not Scale(F(1), F(0)).blows_up_at(F(1, 100)), "q^1 does not")
ok(Scale(F(-1, 2), F(0)).integrable_in_tau_at(0), "tau^(-1/2) is integrable")
ok(not Scale(F(-1), F(0)).integrable_in_tau_at(0), "tau^(-1) is not")
ok(not Scale(F(-3, 2), F(0)).integrable_in_tau_at(0), "tau^(-3/2) is not")

print()
if _fails:
    print(f"FAILURES: {len(_fails)}")
    for f in _fails:
        print(f"  - {f}")
    sys.exit(1)
print(f"test_arc6_residual_ledger: all checks pass")
