"""Hand-rolled rigorous interval arithmetic (no scipy, no mpmath).

This is the Route-D (Level-2) tooling core: the first, evidence-gathering brick
of a computer-assisted certification stage for the gCLM two-scale traveling-wave
profiles (solver/gclm_family.py::GCLMResidual.residual_two_scale). It is
DELIBERATELY just the arithmetic layer -- an `Interval` type with guaranteed
outward-rounded +, -, *, /, and the two reductions (`isum`, `matvec`, `dot`)
needed to enclose the residual R2(Omega) = Omega H(Omega) - c_tw Omega_X. Whether
a certifiable fixed-point statement can then be *set up* (bound the linearized
inverse, the defect, the Lipschitz constant so a Newton-Kantorovich ball closes)
is the NEXT decision, to be made from the enclosure widths this layer produces at
the a=0 anchor. This file makes NO certification claim.

Rigor model. We do not have portable control of the FPU rounding mode from numpy,
so we use the standard *round-outward-by-one-ulp* discipline: evaluate the real
interval-extension formula in IEEE-754 double (each elementary op correctly
rounded to <= 0.5 ulp), then push the lower endpoint DOWN and the upper endpoint
UP by one ulp with np.nextafter. One ulp conservatively covers the <= 0.5 ulp
rounding of the elementary op, so the result is a guaranteed enclosure (it
over-estimates the width by up to ~1 ulp per op, which is the price of not owning
the rounding mode). For the sum/dot/matvec reductions, which accumulate m terms,
the classic running-error bound |fl(sum) - sum| <= gamma_m * sum|terms|, with
gamma_m = m*u/(1 - m*u) and u = 2^-53, is added before the outward push -- giving
a rigorous, fully-vectorized enclosure of a length-m accumulation without a
Python-level sequential loop.

Backed by numpy arrays, so an `Interval` may hold a scalar (0-d) or a whole
profile vector; all ops broadcast. Point (degenerate) intervals model exact
float inputs; `from_mid_rad` models a genome box.
"""

import numpy as np

_U = 2.0 ** -53          # unit roundoff (double precision)


def _down(x):
    """Round an array toward -inf by one ulp (rigorous lower push)."""
    return np.nextafter(x, -np.inf)


def _up(x):
    """Round an array toward +inf by one ulp (rigorous upper push)."""
    return np.nextafter(x, np.inf)


def _gamma(m):
    """Classic accumulation error factor gamma_m = m*u/(1 - m*u), m >= 0.

    Bounds the relative error of an m-term floating sum/dot. Guarded so a huge m
    (never reached here: m ~ 1200) cannot cross the 1/u wall."""
    mu = m * _U
    if mu >= 1.0:
        raise ValueError(f"accumulation length {m} too large for the gamma bound")
    return mu / (1.0 - mu)


class Interval:
    """Rigorous interval [lo, hi], numpy-backed (scalar or array), broadcasting.

    Invariant: lo <= hi elementwise. Arithmetic returns enclosures rounded
    outward by one ulp; comparisons/reductions preserve enclosure. Construct from
    explicit endpoints, an exact point (`point`), or a midpoint+radius box
    (`from_mid_rad`)."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        lo = np.asarray(lo, dtype=float)
        hi = np.asarray(hi, dtype=float)
        if lo.shape != hi.shape:
            lo, hi = np.broadcast_arrays(lo, hi)
        if np.any(lo > hi):
            raise ValueError("Interval requires lo <= hi")
        self.lo = lo
        self.hi = hi

    # -- constructors -------------------------------------------------------
    @classmethod
    def point(cls, x):
        """Degenerate interval [x, x] enclosing exactly the float(s) x."""
        x = np.asarray(x, dtype=float)
        return cls(x.copy(), x.copy())

    @classmethod
    def from_mid_rad(cls, mid, rad):
        """Box [mid - rad, mid + rad], rounded outward (rad >= 0)."""
        mid = np.asarray(mid, dtype=float)
        rad = np.abs(np.asarray(rad, dtype=float))
        return cls(_down(mid - rad), _up(mid + rad))

    # -- views --------------------------------------------------------------
    @property
    def mid(self):
        return 0.5 * (self.lo + self.hi)

    @property
    def rad(self):
        """Half-width (diagnostic; a point has rad 0). Not used in the rigor path."""
        return 0.5 * (self.hi - self.lo)

    @property
    def width(self):
        """Endpoint gap hi - lo (diagnostic; a point has width 0)."""
        return self.hi - self.lo

    @property
    def shape(self):
        return self.lo.shape

    def contains(self, x):
        """Elementwise: is the real number x inside [lo, hi]?"""
        x = np.asarray(x, dtype=float)
        return (self.lo <= x) & (x <= self.hi)

    def mag(self):
        """Elementwise magnitude sup{|t| : t in [lo,hi]} = max(|lo|,|hi|)."""
        return np.maximum(np.abs(self.lo), np.abs(self.hi))

    # -- coercion -----------------------------------------------------------
    @staticmethod
    def _coerce(x):
        return x if isinstance(x, Interval) else Interval.point(x)

    # -- arithmetic (outward-rounded) --------------------------------------
    def __add__(self, other):
        o = self._coerce(other)
        return Interval(_down(self.lo + o.lo), _up(self.hi + o.hi))

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        o = self._coerce(other)
        return Interval(_down(self.lo - o.hi), _up(self.hi - o.lo))

    def __rsub__(self, other):
        return self._coerce(other).__sub__(self)

    def __mul__(self, other):
        o = self._coerce(other)
        p1 = self.lo * o.lo
        p2 = self.lo * o.hi
        p3 = self.hi * o.lo
        p4 = self.hi * o.hi
        lo = np.minimum(np.minimum(p1, p2), np.minimum(p3, p4))
        hi = np.maximum(np.maximum(p1, p2), np.maximum(p3, p4))
        return Interval(_down(lo), _up(hi))

    __rmul__ = __mul__

    def reciprocal(self):
        """1 / [lo, hi]; requires 0 not in the interval (elementwise)."""
        if np.any((self.lo <= 0.0) & (0.0 <= self.hi)):
            raise ZeroDivisionError("reciprocal of an interval containing 0")
        return Interval(_down(1.0 / self.hi), _up(1.0 / self.lo))

    def __truediv__(self, other):
        o = self._coerce(other)
        return self.__mul__(o.reciprocal())

    def __rtruediv__(self, other):
        return self._coerce(other).__truediv__(self)

    # -- indexing / shape ---------------------------------------------------
    def __getitem__(self, key):
        return Interval(self.lo[key], self.hi[key])

    def __len__(self):
        return len(self.lo)

    def __repr__(self):
        if self.lo.ndim == 0:
            return f"Interval([{float(self.lo):.16g}, {float(self.hi):.16g}])"
        return f"Interval(shape={self.lo.shape}, max_width={float(self.width.max()):.3e})"


# --------------------------------------------------------------------------
# rigorous reductions over an accumulation of m terms
# --------------------------------------------------------------------------

def isum(iv, axis=None):
    """Rigorous sum of an Interval array along `axis` (default: all).

    Adds the gamma_m running-error bound for the m-term float accumulation
    before the outward push, so the enclosure is guaranteed without a sequential
    Python loop."""
    lo = np.asarray(iv.lo, dtype=float)
    hi = np.asarray(iv.hi, dtype=float)
    m = lo.shape[axis] if axis is not None else lo.size
    g = _gamma(m)
    s_lo = np.sum(lo, axis=axis)
    s_hi = np.sum(hi, axis=axis)
    err_lo = _up(g * np.sum(np.abs(lo), axis=axis))
    err_hi = _up(g * np.sum(np.abs(hi), axis=axis))
    return Interval(_down(s_lo - err_lo), _up(s_hi + err_hi))


def matvec(M, v):
    """Rigorous enclosure of (M @ v) for a POINT matrix M and Interval vector v.

    M is an exact float (n, m) array (e.g. the Hilbert or derivative operator);
    v is an Interval of length m. Splits M into nonneg/neg parts so the endpoint
    matmuls are monotone, then adds the gamma_m dot-accumulation bound. Fully
    vectorized (three numpy matmuls), no Python loop over rows."""
    M = np.asarray(M, dtype=float)
    m = M.shape[1]
    if v.lo.shape != (m,):
        raise ValueError(f"matvec: M is {M.shape}, v has shape {v.lo.shape}")
    Mp = np.maximum(M, 0.0)
    Mn = np.minimum(M, 0.0)
    lo = Mp @ v.lo + Mn @ v.hi
    hi = Mp @ v.hi + Mn @ v.lo
    g = _gamma(m)
    # sum_j |M_ij| * |v_j|-endpoint bounds the per-row accumulation error
    a_lo = Mp @ np.abs(v.lo) + (-Mn) @ np.abs(v.hi)
    a_hi = Mp @ np.abs(v.hi) + (-Mn) @ np.abs(v.lo)
    return Interval(_down(lo - _up(g * a_lo)), _up(hi + _up(g * a_hi)))


def dot(u, v):
    """Rigorous enclosure of the inner product sum_j u_j v_j (Interval . Interval)."""
    return isum(u * v)
