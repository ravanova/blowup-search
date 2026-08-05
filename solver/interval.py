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


# --------------------------------------------------------------------------
# COMPENSATED matvec -- the enclosure that survives cancellation (Route-L1)
# --------------------------------------------------------------------------
# WHY THIS EXISTS.  `matvec` above bounds an m-term accumulation by
# gamma_m * sum_j |M_ij v_j|, which is sharp when the terms do not cancel and
# useless when they do.  Leg 50 measured exactly that: at a Newton-converged
# iterate the residual is 5.7e-15 while its interval enclosure is 2.3e-12 wide,
# because the slope operator's rows cancel to ~1/270 of their absolute mass.  The
# rigorous Y_0 was then set by the WIDTH OF THE EVALUATION rather than by the
# residual, and the certificate missed closing by 1.48x for a reason that had
# nothing to do with the mathematics.
#
# Dot2 (Ogita-Rump-Oishi 2005) fixes it with error-free transformations: the
# product and the sum each return their own rounding error exactly, and those
# errors are accumulated alongside.  The result carries the error bound
#
#     |dot2(x, y) - x.y|  <=  u |x.y|  +  gamma_m^2 sum_j |x_j y_j|
#
# so the cancellation-sensitive term is squared away (gamma_m^2 ~ 5e-28) and what
# is left is RELATIVE to the answer.  Vectorised over rows: the loop is over the
# m columns, each step a handful of length-n numpy operations.

_SPLIT = 134217729.0          # 2^27 + 1, Dekker's splitting constant


def _two_sum(a, b):
    """Knuth: s = fl(a+b) and err with a + b == s + err EXACTLY."""
    s = a + b
    bb = s - a
    return s, (a - (s - bb)) + (b - bb)


def _two_product(a, b):
    """Dekker: p = fl(a*b) and err with a*b == p + err EXACTLY (no FMA needed)."""
    p = a * b
    ca = _SPLIT * a
    ah = ca - (ca - a)
    al = a - ah
    cb = _SPLIT * b
    bh = cb - (cb - b)
    bl = b - bh
    return p, (((ah * bh - p) + ah * bl) + al * bh) + al * bl


def dot2_matvec(M, v):
    """Rigorous enclosure of (M @ v) for exact float M, v, robust to cancellation.

    Returns an Interval. Same signature as `matvec` but with v a plain float array
    (both operands must be exact data -- this is the residual-evaluation path, not
    the ball-evaluation path). The radius is
        u |result| / (1 - u)  +  gamma_m^2 * sum_j |M_ij v_j|
    pushed outward by one ulp, which is the Ogita-Rump-Oishi bound made outward."""
    M = np.asarray(M, dtype=float)
    v = np.asarray(v, dtype=float)
    n, m = M.shape
    if v.shape != (m,):
        raise ValueError(f"dot2_matvec: M is {M.shape}, v has shape {v.shape}")
    p, e = _two_product(M[:, 0], v[0])
    s = e.copy()
    for j in range(1, m):
        h, r = _two_product(M[:, j], v[j])
        p, q = _two_sum(p, h)
        s = s + (q + r)
    res = p + s
    absmass = _up(np.abs(M) @ np.abs(v))
    absmass = _up(absmass * (1.0 + _gamma(m)))      # the mass sum is itself rounded
    g2 = _up(_gamma(m) ** 2)
    t = _up(g2 * absmass)
    # |x.y| <= (|res| + t) / (1 - u) follows from the ORO bound itself, so the
    # relative term is bounded without assuming |res| >= |x.y|
    rad = _up(_up(_U * _up((np.abs(res) + t) / (1.0 - _U))) + t)
    return Interval(_down(res - rad), _up(res + rad))
