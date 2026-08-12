"""SAMPLES -> CERTIFIED CELL ENCLOSURES: the input contract leg 382 named and did
not supply.

WHY THIS MODULE EXISTS.  `solver/dssp_decay_enclosure.py` (leg 382, Route-DEXC) certifies a
far-field decay exponent from **cell enclosures** -- data of the form "for every r in
[r_lo[i], r_hi[i]], f_lo[i] <= f(r) <= f_hi[i]".  Its own docstring names the gap in the
pipeline, at `:354`:

    "Supplying those is the caller's obligation and this routine cannot check it -- if the
     caller has only pointwise samples, it must first convert them using a certified modulus
     of continuity, or a monotonicity hypothesis, and must state which."

Any real profile-producing unit holds **point samples**, not cell enclosures.  This module is
the converter, and it is a separate module on purpose: leg 382's file is read here and edited
nowhere.

THE ONE FACT THAT SHAPES THE WHOLE DESIGN.  From finitely many point evaluations ALONE, with
no regularity hypothesis, no non-trivial enclosure of a function's range is derivable -- every
superinterval of the range is consistent with the data.  A converter that silently returned
"something" from bare samples would therefore be fabricating, not computing.  So:

  * an input carrying NEITHER hypothesis returns INCAPACITY.  Never a guess, never a default.
  * the hypothesis in force is written into the returned row, and
    `certified_decay_from_samples` merges it into leg 382's own output dict, so a downstream
    consumer reads the certificate and its condition in one object.

**A certificate whose conditionality is invisible is worse than no certificate**, because it
invites a reader to use it as if unconditional.  That sentence is the module's reason to
exist; the arithmetic below is elementary and is claimed as elementary (see
`writeup/novelty/leg_385.md`, which claims NO novel mathematics).

THE TWO PATHS.

  * ``MONOTONE`` -- the caller declares f monotone (``"nonincreasing"`` or
    ``"nondecreasing"``) on the whole window.  A monotone function attains its extremes on a
    cell at the cell's endpoints, and both endpoints are sampled, so the sample pair IS the
    enclosure:  non-increasing =>  f(r) in [f_lo[i+1], f_hi[i]]  for all r in cell i.
    No slack is added beyond the caller's own sample error bars.  This path is EXACT.

  * ``MODULUS`` -- the caller declares a certified non-decreasing modulus of continuity
    ``omega(h) = L * h**alpha`` with ``alpha in {1/2, 1}``, in one of two coordinate kinds:

      - ``kind="absolute"``:  |f(r) - f(s)| <= omega(|r - s|)
      - ``kind="loglog"``  :  |log f(r) - log f(s)| <= omega(|log r - log s|)

    Every point of a cell of width h is within h/2 of one endpoint, so
    ``f(r) in [min_endpoint - omega(h/2), max_endpoint + omega(h/2)]`` (absolute), and
    multiplicatively in the loglog kind.  This path is SOUND but NOT TIGHT: its width is set
    by ``omega`` and the grid, and leg 385 measured how much -- see `CEILING` below.

  * Both may be declared together, in which case the two enclosures are INTERSECTED (both
    hypotheses hold, so the intersection is valid) and the recorded hypothesis is
    ``"MONOTONE+MODULUS"``.

NO ``iexp`` IN THE SUBSTRATE, AND WHAT IS DONE ABOUT IT.  `solver/interval.py` provides
``ilog`` but no exponential, and leg 382 deliberately declined to add a transcendental whose
remainder it would then have to prove.  The ``loglog`` kind needs ``e**(+-omega)``, so it is
closed back to multiplicative form with two elementary bounds that use only ``+ - * /``:

    e**(-x) >= 1 - x           for all x >= 0
    e**(x)  <= 1 / (1 - x)     for 0 <= x < 1,  since 1/(1-x) = sum x^n >= sum x^n/n! = e^x

Both are applied OUTWARD, so the enclosure is rigorous; the overestimate is O(omega**2) and
at the sampling densities of interest (omega ~ 2e-3) it is ~5e-6 relative.  An input whose
``omega(h/2) >= 1`` in this kind is REFUSED rather than approximated.

NECESSARY CONDITIONS ARE CHECKED; THE HYPOTHESES THEMSELVES CANNOT BE.  A declared hypothesis
implies things about the samples: monotone samples for ``MONOTONE``, and
``|f_i - f_{i+1}| <= omega(h_i)`` for ``MODULUS``.  Those are checked, and a certain violation
(certain after outward rounding, so a refusal is never a rounding artefact) returns INCAPACITY
naming the offending index.  **Passing them proves nothing.**  A profile can agree with a
monotone sequence at every node and be wildly non-monotone between nodes; leg 385's control X3
plants exactly that and the adapter accepts it, as it must.  That is not a defect to be fixed
-- it is the definition of a hypothesis, and it is why the hypothesis is recorded in the row.

CEILING, MEASURED, NOT ASSERTED (leg 385, `writeup/data/p2_route_scel_v1.json`):

  * PATH A reproduces leg 382's exact-power certified widths to the rounding floor.
  * PATH B does not, and cannot: its width scales like ``omega(dt/2)``, i.e. like ``1/N``.
  * A GLOBALLY stated ``absolute`` modulus is useless on a multi-decade window: omega(h/2)
    grows with r while f decays, so the lower enclosure goes non-positive in the far cells and
    leg 382's routine then answers INCAPACITY.  Use the ``loglog`` kind, or per-sample local
    constants (both supported), on any window spanning decades.
  * Validated on PLANTED ANALYTIC KNOWNS ONLY.  No profile of route 4's object exists in this
    repository.  `CLAY_OBLIGATIONS.md` §6 items 1 and 2 stay OPEN and item 1's
    admissible-cutoff half is untouched.

SUBSTRATE.  `solver/interval.py` (`Interval`, `ilog`, outward rounding) and, read-only,
`solver/dssp_decay_enclosure.py` (`isqrt`/`ipow_half_integer` for the half-integer modulus
exponent, and `certified_decay_from_cell_enclosures` as the downstream consumer).  No new
interval primitive is introduced by this module.
"""

import numpy as np

from solver.interval import Interval, ilog, _down, _up
from solver.dssp_decay_enclosure import (
    certified_decay_from_cell_enclosures,
    ipow_half_integer,
    DEFAULT_P_BRACKET,
    VERDICT_INCAPACITY,
)

__all__ = [
    "Modulus",
    "samples_to_cells",
    "certified_decay_from_samples",
    "containment_audit",
    "planted_sampled_power_law",
    "planted_node_aligned_wiggle",
    "HYP_MONOTONE", "HYP_MODULUS", "HYP_BOTH",
    "VERDICT_CELLS", "VERDICT_INCAPACITY",
    "MONOTONE_DIRECTIONS", "MODULUS_KINDS",
]

VERDICT_CELLS = "CELLS"

HYP_MONOTONE = "MONOTONE"
HYP_MODULUS = "MODULUS"
HYP_BOTH = "MONOTONE+MODULUS"

MONOTONE_DIRECTIONS = ("nonincreasing", "nondecreasing")
MODULUS_KINDS = ("absolute", "loglog")


# ---------------------------------------------------------------------------
# 0.  the declared modulus of continuity
# ---------------------------------------------------------------------------

class Modulus:
    """A CERTIFIED modulus of continuity, as declared by the caller.

    ``omega(h) = L * h**alpha``, non-decreasing in h, with ``alpha in {1/2, 1}`` and
    ``L >= 0``.  ``L`` may be a scalar (one constant for the whole window) or an array of
    per-sample constants, in which case cell ``i`` uses ``max(L[i], L[i+1])`` -- the
    conservative choice, since the cell is covered by both endpoints' neighbourhoods.

    ``kind="absolute"``:  |f(r) - f(s)|         <= omega(|r - s|)
    ``kind="loglog"``  :  |log f(r) - log f(s)| <= omega(|log r - log s|)

    THE RESTRICTION TO alpha in {1/2, 1} IS THE SUBSTRATE'S, NOT THE MATHEMATICS'.
    `solver/interval.py` has no `iexp`, so a general power ``h**alpha`` has no proved
    interval extension here; half-integer powers reduce to multiplication and leg 382's
    correctly-rounded `isqrt`.  alpha = 1 is Lipschitz, alpha = 1/2 is Hoelder-1/2.  An
    `alpha` outside the set is REFUSED, not rounded to a nearby one.

    NOTHING HERE VERIFIES THE MODULUS.  It is an input the caller owes, exactly as leg 382's
    `rel_tolerance` is, and the object of this module is to make sure it is *named* in the
    output rather than assumed silently."""

    def __init__(self, L, alpha=1.0, kind="absolute"):
        if kind not in MODULUS_KINDS:
            raise ValueError(f"Modulus: kind must be one of {MODULUS_KINDS}, got {kind!r}")
        twice = round(2.0 * float(alpha))
        if abs(2.0 * float(alpha) - twice) > 1e-12 or twice not in (1, 2):
            raise ValueError(
                "Modulus: alpha must be exactly 0.5 or 1.0 (the substrate proves only "
                f"half-integer powers); got {alpha!r}")
        L_arr = np.asarray(L, dtype=float)
        if not np.all(np.isfinite(L_arr)) or np.any(L_arr < 0.0):
            raise ValueError("Modulus: L must be finite and >= 0")
        self.L = L_arr
        self.alpha = float(alpha)
        self.kind = str(kind)

    # -- cell constants ----------------------------------------------------
    def _L_cells(self, n_nodes):
        """Per-cell constant: scalar L broadcast, or max of the two endpoint constants."""
        if self.L.ndim == 0:
            return np.full(n_nodes - 1, float(self.L))
        if self.L.shape != (n_nodes,):
            raise ValueError(
                f"Modulus: per-sample L has shape {self.L.shape}, expected ({n_nodes},)")
        return np.maximum(self.L[:-1], self.L[1:])

    def omega_upper(self, h, n_nodes=None):
        """An UPPER bound on ``omega(h)`` for each cell, outward-rounded.

        ``h`` is a per-cell array of (already upper-bounded) widths."""
        h = np.asarray(h, dtype=float)
        L_cells = self._L_cells(n_nodes if n_nodes is not None else h.size + 1)
        omega = Interval.point(L_cells) * ipow_half_integer(Interval.point(h), self.alpha)
        return np.asarray(omega.hi, dtype=float)

    def detail(self):
        return {"kind": self.kind,
                "alpha": self.alpha,
                "L": (float(self.L) if self.L.ndim == 0 else "per-sample array"),
                "L_min": float(np.min(self.L)),
                "L_max": float(np.max(self.L)),
                "form": ("|f(r)-f(s)| <= L*|r-s|**alpha" if self.kind == "absolute"
                         else "|log f(r)-log f(s)| <= L*|log r-log s|**alpha")}

    def __repr__(self):
        return f"Modulus(kind={self.kind!r}, alpha={self.alpha}, L={self.L!r})"


# ---------------------------------------------------------------------------
# 1.  refusal helper
# ---------------------------------------------------------------------------

def _incapacity(reason, hypothesis=None, hypothesis_detail=None, **extra):
    out = {"verdict": VERDICT_INCAPACITY,
           "reason": reason,
           "hypothesis": hypothesis,
           "hypothesis_detail": hypothesis_detail,
           "conditional_on": None,
           "r_lo": None, "r_hi": None, "f_lo": None, "f_hi": None,
           "n_cells": 0}
    out.update(extra)
    return out


def _conditional_sentence(hypothesis, monotone, modulus, sample_exactness):
    """The one sentence a downstream reader must see next to any number derived from these
    cells.  Assembled, never abbreviated."""
    parts = []
    if monotone is not None:
        parts.append(f"f is {monotone} on the whole window (declared by the caller, "
                     "NOT verified -- agreement of the samples with that direction is a "
                     "necessary condition only)")
    if modulus is not None:
        d = modulus.detail()
        parts.append(f"f obeys the caller-certified modulus {d['form']} with "
                     f"alpha = {d['alpha']} and L in [{d['L_min']:.6g}, {d['L_max']:.6g}] "
                     f"({d['kind']} coordinates)")
    if sample_exactness == "declared-exact":
        parts.append("the supplied sample values are EXACT values of f at the sample radii "
                     "(declared by the caller; a float64 evaluation is not exact)")
    else:
        parts.append("the supplied per-sample intervals enclose f at the sample radii")
    return ("These cell enclosures, and every certificate derived from them, hold "
            "CONDITIONALLY on: " + "; ".join(parts) + ".")


# ---------------------------------------------------------------------------
# 2.  the adapter
# ---------------------------------------------------------------------------

def samples_to_cells(r, f=None, f_lo=None, f_hi=None, monotone=None, modulus=None):
    """Convert point samples into CERTIFIED CELL ENCLOSURES under a named hypothesis.

    ``r``            strictly increasing sample radii, all > 1 (leg 382's window condition).
    ``f``            sample values DECLARED EXACT -- mutually exclusive with ``f_lo``/``f_hi``.
    ``f_lo``/``f_hi``  per-sample enclosures ``f_lo[i] <= f(r[i]) <= f_hi[i]``.  This is the
                     honest form: a float64 evaluation of a profile is not its exact value.
    ``monotone``     ``"nonincreasing"``, ``"nondecreasing"`` or ``None``.
    ``modulus``      a `Modulus` or ``None``.

    Returns a dict with ``verdict`` in {``CELLS``, ``INCAPACITY``}; on ``CELLS`` the arrays
    ``r_lo, r_hi, f_lo, f_hi`` satisfy ``f_lo[i] <= f(r) <= f_hi[i]`` for EVERY r in cell i,
    **given the declared hypothesis**, and the fields ``hypothesis``, ``hypothesis_detail``,
    ``sample_exactness`` and ``conditional_on`` record exactly what that is.

    **Neither hypothesis => INCAPACITY.**  There is no default and no guess."""

    # -- 2.0 the central refusal, checked first so nothing else can mask it -------------
    if monotone is None and modulus is None:
        return _incapacity(
            "NO HYPOTHESIS SUPPLIED. Point samples alone determine no enclosure: with no "
            "regularity hypothesis every superinterval of the range is consistent with the "
            "data, so any returned cell enclosure would be fabricated. Supply monotone= "
            f"(one of {MONOTONE_DIRECTIONS}) or modulus=Modulus(...), or both.")

    if monotone is not None and monotone not in MONOTONE_DIRECTIONS:
        return _incapacity(
            f"monotone must be one of {MONOTONE_DIRECTIONS} or None; got {monotone!r}")
    if modulus is not None and not isinstance(modulus, Modulus):
        return _incapacity(
            "modulus must be a Modulus instance or None; a bare number is refused because "
            "its coordinate kind (absolute / loglog) and exponent would be a guess")

    hypothesis = (HYP_BOTH if (monotone is not None and modulus is not None)
                  else (HYP_MONOTONE if monotone is not None else HYP_MODULUS))
    detail = {"monotone": monotone,
              "modulus": (modulus.detail() if modulus is not None else None)}

    # -- 2.1 sample validation ----------------------------------------------------------
    r = np.asarray(r, dtype=float)
    if (f is None) == (f_lo is None or f_hi is None):
        return _incapacity(
            "supply EITHER f= (values declared exact) OR both f_lo= and f_hi= "
            "(per-sample enclosures), not neither and not both",
            hypothesis, detail)
    if f is not None:
        sample_exactness = "declared-exact"
        f_lo = np.asarray(f, dtype=float).copy()
        f_hi = f_lo.copy()
    else:
        sample_exactness = "enclosed"
        f_lo = np.asarray(f_lo, dtype=float)
        f_hi = np.asarray(f_hi, dtype=float)

    n = r.size
    if n < 2:
        return _incapacity(f"need at least 2 samples to form a cell; got {n}",
                           hypothesis, detail)
    if f_lo.shape != (n,) or f_hi.shape != (n,):
        return _incapacity(
            f"sample arrays must have shape ({n},) matching r; got {f_lo.shape} / {f_hi.shape}",
            hypothesis, detail)
    if not (np.all(np.isfinite(r)) and np.all(np.isfinite(f_lo)) and np.all(np.isfinite(f_hi))):
        return _incapacity("non-finite value in r, f_lo or f_hi", hypothesis, detail)
    if np.any(np.diff(r) <= 0.0):
        return _incapacity("sample radii must be STRICTLY increasing", hypothesis, detail)
    if np.any(r <= 1.0):
        return _incapacity(
            "every sample radius must exceed 1: leg 382's enclosure needs log r > 0, which "
            "is what fixes the sign in its p >= 0 relaxation",
            hypothesis, detail)
    if np.any(f_lo <= 0.0):
        return _incapacity(
            "sample lower bounds must be strictly positive; the downstream certificate takes "
            "logs and a non-positive lower bound has no log",
            hypothesis, detail)
    if np.any(f_hi < f_lo):
        return _incapacity("f_hi < f_lo at some sample: not an enclosure", hypothesis, detail)

    r_lo, r_hi = r[:-1], r[1:]
    n_cells = n - 1

    # -- 2.2 necessary conditions the declared hypothesis implies -----------------------
    #
    # A CERTAIN violation (certain after outward rounding) is a refusal.  Passing proves
    # nothing: these are necessary, never sufficient.
    checks = {}
    if monotone is not None:
        if monotone == "nonincreasing":
            gap = _down(f_lo[1:] - f_hi[:-1])       # > 0  =>  f went UP for certain
        else:
            gap = _down(f_lo[:-1] - f_hi[1:])
        worst = int(np.argmax(gap))
        checks["monotone_worst_violation"] = float(gap[worst])
        checks["monotone_worst_index"] = worst
        if gap[worst] > 0.0:
            return _incapacity(
                f"DECLARED {monotone} IS CONTRADICTED BY THE SAMPLES THEMSELVES at cell "
                f"{worst} (radii {r_lo[worst]:.17g} -> {r_hi[worst]:.17g}): the sample "
                f"enclosures are disjoint in the wrong order by {gap[worst]:.6g}. This is a "
                "necessary condition of the declared hypothesis, so the hypothesis is false "
                "and no enclosure is returned.",
                hypothesis, detail, necessary_condition_checks=checks)

    if modulus is not None:
        if modulus.kind == "absolute":
            h_full = _up(r_hi - r_lo)
            om_full = modulus.omega_upper(h_full, n)
            jump = _down(np.maximum(f_lo[1:] - f_hi[:-1], f_lo[:-1] - f_hi[1:]))
            jump = np.maximum(jump, 0.0)
        else:
            T = ilog(Interval.point(r))
            h_full = _up(T.hi[1:] - T.lo[:-1])
            om_full = modulus.omega_upper(h_full, n)
            G = ilog(Interval(f_lo, f_hi))
            jump = _down(np.maximum(G.lo[1:] - G.hi[:-1], G.lo[:-1] - G.hi[1:]))
            jump = np.maximum(jump, 0.0)
        ratio = jump / np.maximum(om_full, np.finfo(float).tiny)
        worst = int(np.argmax(ratio))
        checks["modulus_worst_ratio"] = float(ratio[worst])
        checks["modulus_worst_index"] = worst
        checks["modulus_worst_jump"] = float(jump[worst])
        checks["modulus_worst_omega"] = float(om_full[worst])
        if jump[worst] > om_full[worst]:
            return _incapacity(
                f"DECLARED MODULUS IS UNDERSTATED, PROVABLY, AT THE SAMPLES THEMSELVES: at "
                f"cell {worst} (radii {r_lo[worst]:.17g} -> {r_hi[worst]:.17g}) adjacent "
                f"samples differ by at least {jump[worst]:.6g} in "
                f"{'f' if modulus.kind == 'absolute' else 'log f'}, while the declared "
                f"omega(h) allows at most {om_full[worst]:.6g} -- a factor "
                f"{ratio[worst]:.6g}. This is a necessary condition of the declared "
                "hypothesis, so the hypothesis is false and no enclosure is returned.",
                hypothesis, detail, necessary_condition_checks=checks)

    # -- 2.3 the enclosures -------------------------------------------------------------
    cell_lo = np.full(n_cells, -np.inf)
    cell_hi = np.full(n_cells, np.inf)
    parts = {}

    if monotone is not None:
        if monotone == "nonincreasing":
            m_lo, m_hi = f_lo[1:], f_hi[:-1]
        else:
            m_lo, m_hi = f_lo[:-1], f_hi[1:]
        cell_lo = np.maximum(cell_lo, m_lo)
        cell_hi = np.minimum(cell_hi, m_hi)
        parts["monotone"] = {"max_cell_log_span": float(np.max(np.log(m_hi / m_lo)))}

    if modulus is not None:
        if modulus.kind == "absolute":
            h_half = _up(_up(r_hi - r_lo) * 0.5)
            om = modulus.omega_upper(h_half, n)
            base_lo = np.minimum(f_lo[:-1], f_lo[1:])
            base_hi = np.maximum(f_hi[:-1], f_hi[1:])
            w_lo = _down(base_lo - _up(om))
            w_hi = _up(base_hi + _up(om))
            parts["modulus"] = {"kind": "absolute",
                                "omega_half_cell_min": float(np.min(om)),
                                "omega_half_cell_max": float(np.max(om)),
                                "n_cells_nonpositive_lower": int(np.count_nonzero(w_lo <= 0.0)),
                                "first_nonpositive_radius": (
                                    float(r_lo[np.argmax(w_lo <= 0.0)])
                                    if np.any(w_lo <= 0.0) else None)}
        else:
            T = ilog(Interval.point(r))
            h_half = _up(_up(T.hi[1:] - T.lo[:-1]) * 0.5)
            om = modulus.omega_upper(h_half, n)
            if np.any(om >= 1.0):
                bad = int(np.argmax(om >= 1.0))
                return _incapacity(
                    "the loglog modulus gives omega(dt/2) = "
                    f"{om[bad]:.6g} >= 1 at cell {bad}; this module's exp-free closure "
                    "(e**x <= 1/(1-x)) needs omega < 1, and it REFUSES rather than "
                    "approximate. Sample more densely, or state a smaller L.",
                    hypothesis, detail, necessary_condition_checks=checks)
            one_minus = Interval(_down(1.0 - _up(om)), _up(1.0 - _down(om)))
            base_lo = Interval.point(np.minimum(f_lo[:-1], f_lo[1:]))
            base_hi = Interval.point(np.maximum(f_hi[:-1], f_hi[1:]))
            w_lo = np.asarray((base_lo * one_minus).lo, dtype=float)   # <= f_min * e**(-om)
            w_hi = np.asarray((base_hi / one_minus).hi, dtype=float)   # >= f_max * e**(+om)
            parts["modulus"] = {"kind": "loglog",
                                "omega_half_cell_min": float(np.min(om)),
                                "omega_half_cell_max": float(np.max(om)),
                                "max_relative_inflation": float(np.max(_up(1.0 / _down(1.0 - _up(om))) - 1.0)),
                                "n_cells_nonpositive_lower": int(np.count_nonzero(w_lo <= 0.0)),
                                "first_nonpositive_radius": (
                                    float(r_lo[np.argmax(w_lo <= 0.0)])
                                    if np.any(w_lo <= 0.0) else None)}
        cell_lo = np.maximum(cell_lo, w_lo)
        cell_hi = np.minimum(cell_hi, w_hi)

    if np.any(cell_hi < cell_lo):
        bad = int(np.argmax(cell_hi < cell_lo))
        return _incapacity(
            "the two declared hypotheses are MUTUALLY INCONSISTENT on the samples: their "
            f"cell enclosures are disjoint at cell {bad} "
            f"([{cell_lo[bad]:.6g}, {cell_hi[bad]:.6g}]). At least one declaration is false; "
            "no enclosure is returned.",
            hypothesis, detail, necessary_condition_checks=checks)

    out = {"verdict": VERDICT_CELLS,
           "reason": "",
           "hypothesis": hypothesis,
           "hypothesis_detail": detail,
           "sample_exactness": sample_exactness,
           "conditional_on": _conditional_sentence(hypothesis, monotone, modulus,
                                                   sample_exactness),
           "r_lo": r_lo, "r_hi": r_hi, "f_lo": cell_lo, "f_hi": cell_hi,
           "n_cells": int(n_cells),
           "n_samples": int(n),
           "window": [float(r[0]), float(r[-1])],
           "max_cell_log_tube_width": float(np.max(np.log(cell_hi / cell_lo)))
                                      if np.all(cell_lo > 0.0) else None,
           "n_cells_nonpositive_lower": int(np.count_nonzero(cell_lo <= 0.0)),
           "necessary_condition_checks": checks,
           "enclosure_parts": parts}
    return out


# ---------------------------------------------------------------------------
# 3.  the composed entry point
# ---------------------------------------------------------------------------

def certified_decay_from_samples(r, f=None, f_lo=None, f_hi=None, monotone=None,
                                 modulus=None, p_bracket=DEFAULT_P_BRACKET,
                                 rel_tolerance=0.0):
    """samples -> cells -> leg 382's certified decay exponent, in one call.

    Returns leg 382's own output dict with the adapter's ``hypothesis``,
    ``hypothesis_detail``, ``sample_exactness`` and ``conditional_on`` fields MERGED IN, plus
    ``adapter`` (the conversion diagnostics) and ``enclosure_called``.

    On a refusal, leg 382's routine is **never called** and the refusal is returned as-is
    with ``enclosure_called: False``.  There is no path through this function that produces a
    decay exponent without a named hypothesis attached to it."""
    cells = samples_to_cells(r, f=f, f_lo=f_lo, f_hi=f_hi, monotone=monotone, modulus=modulus)
    if cells["verdict"] != VERDICT_CELLS:
        out = dict(cells)
        out["enclosure_called"] = False
        out["p_lo"] = out["p_hi"] = out["width"] = None
        return out

    res = certified_decay_from_cell_enclosures(cells["r_lo"], cells["r_hi"],
                                               cells["f_lo"], cells["f_hi"],
                                               p_bracket, rel_tolerance)
    res["mode"] = "cells-from-samples"
    res["enclosure_called"] = True
    for key in ("hypothesis", "hypothesis_detail", "sample_exactness", "conditional_on"):
        res[key] = cells[key]
    res["adapter"] = {k: cells[k] for k in
                      ("n_samples", "n_cells", "max_cell_log_tube_width",
                       "n_cells_nonpositive_lower", "necessary_condition_checks",
                       "enclosure_parts")}
    res["cells"] = cells
    return res


# ---------------------------------------------------------------------------
# 4.  the containment audit -- a VALIDATION device, never part of a certificate
# ---------------------------------------------------------------------------

def containment_audit(cells, true_float_fn, n_probe=17):
    """Does the TRUE planted profile actually stay inside the claimed cell enclosures?

    Evaluates ``true_float_fn`` at ``n_probe`` radii spread through each cell (endpoints
    included) and reports the worst SIGNED excess: positive means the truth escaped the
    enclosure, so the hypothesis under which those cells were built is false.

    THIS IS FLOAT64 AND IT IS A VALIDATION TOOL ONLY.  It requires the true profile, which
    exists only for planted knowns, and it is used here to DEMONSTRATE failures whose margins
    (~5e-2 relative) sit ~14 orders of magnitude above float64 noise.  A clean audit is NOT a
    certificate of anything: passing at finitely many probes is exactly the kind of pointwise
    evidence this module exists to refuse to over-read."""
    if cells["verdict"] != VERDICT_CELLS:
        return {"audited": False, "reason": "no cells to audit (adapter refused)"}
    r_lo = np.asarray(cells["r_lo"], dtype=float)
    r_hi = np.asarray(cells["r_hi"], dtype=float)
    f_lo = np.asarray(cells["f_lo"], dtype=float)
    f_hi = np.asarray(cells["f_hi"], dtype=float)
    s = np.linspace(0.0, 1.0, int(n_probe))[None, :]
    R = r_lo[:, None] * (r_hi[:, None] / r_lo[:, None]) ** s
    F = np.asarray(true_float_fn(R), dtype=float)

    excess = np.maximum(f_lo[:, None] - F, F - f_hi[:, None])
    rel = excess / np.abs(F)
    flat = int(np.argmax(excess))
    i, j = np.unravel_index(flat, excess.shape)
    viol_cells = np.any(excess > 0.0, axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        log_excess = np.maximum(np.log(np.maximum(f_lo[:, None], 1e-300)) - np.log(np.abs(F)),
                                np.log(np.abs(F)) - np.log(np.maximum(f_hi[:, None], 1e-300)))
    return {"audited": True,
            "n_probe_per_cell": int(n_probe),
            "worst_signed_excess": float(excess[i, j]),
            "worst_signed_relative_excess": float(np.max(rel)),
            "worst_signed_log_excess": float(np.max(log_excess)),
            "worst_cell_index": int(i),
            "worst_radius": float(R[i, j]),
            "n_cells_violated": int(np.count_nonzero(viol_cells)),
            "contained": bool(np.all(excess <= 0.0))}


# ---------------------------------------------------------------------------
# 5.  planted sampled profiles (leg 385's pre-registered inputs)
# ---------------------------------------------------------------------------

def planted_sampled_power_law(C, p, r):
    """Certified per-sample ENCLOSURES of ``f = C r**(-p)`` at the radii ``r``.

    Uses leg 382's own interval generator at point radii, so the sample error bars are real
    rather than declared: a float64 evaluation of ``C r**(-p)`` is not its exact value, and
    the whole point of this module is not to launder that away.  Returns
    ``(f_lo, f_hi, float_fn)``."""
    from solver.dssp_decay_enclosure import planted_power_law
    iv_fn, float_fn = planted_power_law(C, p)
    F = iv_fn(Interval.point(np.asarray(r, dtype=float)))
    return np.asarray(F.lo, dtype=float), np.asarray(F.hi, dtype=float), float_fn


def planted_node_aligned_wiggle(C, p, A, r_nodes):
    """The SECRET-violation control: a profile that is invisible at the sample nodes.

    ``f(r) = C r**(-p) * (1 + A*sin(2*pi*(log r - t0)/dt))`` where ``dt`` is EXACTLY the node
    spacing of ``r_nodes`` in ``t = log r`` (the nodes must be geometrically spaced) and
    ``t0 = log r_nodes[0]``.  The sine then vanishes at every node, so the samples are
    bit-identical to the pure power law's, while the true profile bulges by a relative ``A``
    inside every cell.

    No adapter can detect this from the samples -- and that is the point.  It violates
    monotonicity (for ``A`` above the per-cell decay) and it violates any modulus that the
    node increments satisfy.  Returns ``float_fn`` only: it is a control, and a certified
    enclosure of it is neither needed nor claimed."""
    t = np.log(np.asarray(r_nodes, dtype=float))
    dt = float(t[1] - t[0])
    t0 = float(t[0])

    def float_fn(rr):
        rr = np.asarray(rr, dtype=float)
        tt = np.log(rr)
        return C * rr ** (-float(p)) * (1.0 + float(A) * np.sin(2.0 * np.pi * (tt - t0) / dt))

    return float_fn
