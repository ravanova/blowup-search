"""A LOWER bound on ||A|| that is worth reading -- and that is actually a LOWER bound.

Every bracket this project has quoted has a lower end that is a maximum over
sign patterns: for a domain index i, the codomain vector g = sign(A_i.)/v, whose
image maximizes the SUP part of ||A g||.  Those directions are the exact
extremizers of a sup-to-sup problem, and they are terrible here, for the reason
v6's discrete-ball trap already made famous in the other direction: a sign
pattern's HOLDER SEMINORM is enormous, so dividing by the full codomain norm
throws away almost everything the numerator gained.  At J = 400 they report 0.94
against an upper bound of 47.

That gap is not a measurement.  "The bound is 50x too big" and "the operator
really is that large" imply opposite decisions about the whole Route-D lane, and
until the lower end is earned they cannot be told apart.  v9 made the point the
expensive way: it converted the bracket into a "19x available gain" that was
pure artifact.

--------------------------------------------------------------------------
WHAT WORKS INSTEAD
--------------------------------------------------------------------------
ANY g gives a valid lower bound ||A|| >= ||A g||_X / ||g||_Y, so the whole
problem is constructing good ones -- this is banked lesson (9), BUILD THE
ADVERSARY, applied to the operator rather than to the quadratic.

The Y-ball's shape says what to look for.  An element with finite codomain norm
must decay at least like 1/v = cos^{alpha+1}(theta/2), and it must not oscillate,
or the seminorm eats it.  So the family is `1/v` times a SLOWLY VARYING shape:

  * powers cos^b(theta/2) and low-order cos(k theta) -- the smoothest elements;
  * Gaussian bumps over a wide sweep of centre and width -- localized mass;
  * smoothed STEPS tanh((theta-c)/w) -- one sign change, which turns out to be
    what the extremizer wants: the winner at (1.5, 0.5) is a step at theta =
    2.65 with width 0.2, giving 3.04 against the sign patterns' 0.94;
  * boxes (two steps) for two sign changes.

Then a random ascent in a smooth cosine basis from the best of those, which
polishes but rarely finds anything the family missed -- reported honestly rather
than dropped, because "the ascent adds nothing" is information about how flat the
maximum is.

--------------------------------------------------------------------------
WHY THE QUOTIENT IS EVALUATED THROUGH `_Quotient` AND NOT DIRECTLY (leg 101)
--------------------------------------------------------------------------
`||A|| >= ||Ag||_X / ||g||_Y` is a theorem in EXACT arithmetic.  This module is
float64, and leg 101's adversarial battery broke the theorem on **47 of 209**
gate-deciding cases, by two mechanisms that are genuinely different:

  (1) OVERFLOW, 46 cases.  `A @ g` reaches `inf` while the true norm is finite --
      the sharpest case reports `inf` as a lower bound on an operator whose norm
      is exactly 1.0e13.  Two routes get there: a small codomain weight, since
      every candidate carries `1/w` (at `w = 1e-300` the candidate is `1e300` and
      its image is `1e313`); and `ascend`'s own trial step, which is sized
      PROPORTIONAL TO THE BOUND FOUND SO FAR, so on any operator of norm above
      ~1e154 the search overflows itself even with unit weights, all-finite
      entries, and a perfectly sound value from `family_lower` one line earlier.
  (2) FINITE EXCEEDANCE, 1 case.  At denormal scale each product carries ~1e-6
      relative rounding, and the maximiser sits ON the extremal direction so
      nothing absorbs it: the reported value landed 425 ULP (6.04e-04 relative)
      ABOVE the exact true norm, as an ordinary-looking finite number.  That is
      the more insidious class -- `inf` at least announces itself.

The repair attacks the cause, which is that the quotient is SCALE-INVARIANT in
`g` and exactly HOMOGENEOUS OF DEGREE ONE in `A`, yet was evaluated at whatever
absolute scale the caller's inputs happened to carry:

  * `A` is normalised ONCE by an exact power of two into `[0.5, 1)`, and each
    candidate `g` likewise WHENEVER its scale threatens the exponent range.  The
    `A` exponent is recombined at the end.  Powers of two are exact in binary
    floating point, so this changes the mathematics not at all -- on any input
    that never over- or underflowed in the first place, every product, sum, max
    and difference downstream keeps its mantissa BIT FOR BIT and only its
    exponent moves.  It buys back the full 53-bit mantissa in the denormal range
    and puts ~600 decades of headroom under the overflow ceiling.
  * the surviving error -- ordinary normal-range rounding -- is removed by a
    DOWNWARD DEFLATION before the number is returned, using the standard
    dot-product bound `gamma_n = n u / (1 - n u)` scaled by the matvec's own
    cancellation ratio, plus a subnormal `eta` term, plus a fixed allowance for
    the norm functors' internal rounding.
  * a candidate whose image or norm is not finite is REJECTED, not maximised
    over; a candidate whose certified error bound is not small is DROPPED.
  * if the recombined exponent genuinely exceeds float64, the true norm really is
    above 1.798e308, so `finfo.max` is returned with a `saturated` count -- still
    a true lower bound, and one a caller can act on.

WHAT IS RIGOROUS HERE AND WHAT IS CALIBRATED, so the writeup cannot blur it.
The power-of-two rescaling is EXACT (test 8 verifies the round-trip rather than
assuming it).  The matvec deflation is RIGOROUS (Higham Thm 3.5 plus a subnormal
term).  The allowance for `dom` and `cod`'s own internal rounding, `NORM_SLACK`,
is NOT rigorous and cannot be: they are black-box callables this module does not
own, and the repo has no exact-arithmetic norm.  Its adequacy is a MEASUREMENT
over leg 101's battery, reported in ULP, not a proof.  That is also why
`solver/interval.py` is not the answer here -- interval arithmetic cannot wrap a
callable it does not control.

Every guard can only move the reported number DOWN.  This is not a sharpening of
the bound and must never become one: on the production Route-D path the change is
a deflation of ~1.4e-12 relative and nothing else.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous in the
sense the certificate lane means; what IS now true is that the number returned is
below the true norm rather than sometimes above it.
"""

import numpy as np

# unit roundoff, smallest subnormal, and the float64 ceiling
_U = 0.5 * float(np.finfo(float).eps)             # 2^-53
_ETA = float(np.nextafter(0.0, 1.0))              # 4.94e-324
_MAXF = float(np.finfo(float).max)                # 1.7977e308
_TINY = float(np.finfo(float).tiny)               # 2.2251e-308, smallest normal

#: fixed relative allowance for the norm functors' OWN float evaluation error.
#: Calibrated, not proved -- see the module docstring.  1e-12 is ~4500 ULP, four
#: orders above the ~1e-16 a max-of-products norm can lose, and eleven orders
#: below the 1e-9 the production bracket is allowed to move.
NORM_SLACK = 1e-12

#: a candidate whose certified relative error bound exceeds this carries no
#: usable information about ||A|| and is dropped rather than maximised over.
REJECT_REL = 1e-6

#: `g` is renormalised by a power of two only when its scale threatens the
#: exponent range.  With max|A| < 1 after rescaling, |A g| <= n max|g|, so
#: max|g| <= 2^500 can never overflow; below 2^-500 the products would start
#: losing bits to the subnormal floor.  Leaving `g` alone inside the band is what
#: makes the production path BIT-IDENTICAL to the pre-repair code.
_G_HI, _G_LO = 2.0 ** 500, 2.0 ** -500


def _pow2_normalise(x):
    """(y, e) with y == x * 2**-e EXACTLY and max|y| in [0.5, 1).

    Returns e = 0 when x is all-zero or carries no finite entry, so the caller's
    array is passed through untouched.
    """
    x = np.asarray(x, dtype=float)
    a = np.abs(x)
    fin = a[np.isfinite(a)]
    m = float(fin.max()) if fin.size else 0.0
    if m == 0.0:
        return x, 0
    e = int(np.frexp(m)[1])
    return np.ldexp(x, -e), e


class _Quotient:
    """Certified evaluator of `dom(A g) / cod(g)`, deflated DOWNWARD.

    Construction normalises `A` by an exact power of two once.  `probe(g)` then
    returns `(r_scaled, rel)` -- the float quotient of the RESCALED problem (i.e.
    `2**-eA` times the true quotient) together with a relative error bound -- or
    `None` if the candidate is rejected.  Search compares `r_scaled` values, which
    is legitimate because `eA` is fixed for the whole search; `certify` is applied
    once, to the winner, and is the only place a number a caller may quote is
    produced.

    Splitting it that way is deliberate: the ordering the search sees is the
    ordering the pre-repair code saw, bit for bit, so the repair cannot change
    which direction wins -- only the value reported for it.
    """

    def __init__(self, A, dom, cod):
        self.A, self.eA = _pow2_normalise(np.asarray(A, dtype=float))
        self.absA = np.abs(self.A)
        self.dom, self.cod = dom, cod
        n = int(self.A.shape[1]) if self.A.ndim == 2 else int(self.A.size)
        self.n = n
        self.gamma_n = (n * _U / (1.0 - n * _U)) if n * _U < 1.0 else np.inf
        self.n_probed = 0
        self.n_rejected = 0
        self.n_saturated = 0
        self.max_rel = 0.0

    # -- one candidate ------------------------------------------------------
    def probe(self, g):
        """`(r_scaled, rel)` for an admissible candidate, else `None`.

        The quotient is scale-free in `g`, so two exactly-equivalent scalings are
        available and the first one that EVALUATES is used: `g` as the caller
        built it, and `g` renormalised by a power of two.  Which is tried first
        depends on which hazard is nearer -- see `_G_HI` / `_G_LO`.  The fallback
        is not cosmetic: the norm functors are black boxes with their own
        exponent limits (a weighted l2 squares its argument, so it dies two
        orders of exponent sooner than the matvec does), and forcing one fixed
        scaling on them turns 37 of leg 101's cases from a usable bound into a
        weak-but-true zero.
        """
        self.n_probed += 1
        g = np.asarray(g, dtype=float)
        if not np.all(np.isfinite(g)):
            self.n_rejected += 1
            return None
        m = float(np.max(np.abs(g)))
        gn, e = _pow2_normalise(g)
        if e == 0:
            order = (g,)
        elif m > _G_HI or m < _G_LO:
            order = (gn, g)                    # as-is is the one at risk
        else:
            order = (g, gn)
        for gs in order:
            out = self._probe_one(gs)
            if out is not None:
                return out
        self.n_rejected += 1
        return None

    def _probe_one(self, gs):
        """One fixed scaling of one candidate.  `None` means "not evaluable"."""
        den = self.cod(gs)
        if not (np.isfinite(den) and den > 0.0):
            return None
        v = self.A @ gs
        if not np.all(np.isfinite(v)):
            return None
        num = self.dom(v)
        if not (np.isfinite(num) and num >= 0.0):
            return None
        r = num / den
        if not (np.isfinite(r) and r >= 0.0):
            return None
        # Rigorous componentwise bound on the matvec (Higham, Accuracy and
        # Stability of Numerical Algorithms, Thm 3.5) plus Rump's absolute
        # subnormal term, expressed relative to the largest image component --
        # which is the component every norm here is largest on.
        vmax = float(np.max(np.abs(v)))
        if vmax == 0.0:
            rel = NORM_SLACK
        else:
            amax = float(np.max(self.absA @ np.abs(gs)))
            rel = self.gamma_n * (amax / vmax) + self.n * _ETA / vmax + NORM_SLACK
        if not np.isfinite(rel) or rel > REJECT_REL:
            return None
        if rel > self.max_rel:
            self.max_rel = rel
        return r, rel

    # -- the number a caller may quote --------------------------------------
    def certify(self, r_scaled, rel):
        """Deflate downward, then recombine the exponent `A` was normalised by."""
        if not (np.isfinite(r_scaled) and r_scaled > 0.0):
            return 0.0
        d = r_scaled * (1.0 - float(rel))
        d = float(np.nextafter(d, -np.inf))     # and the deflation's own rounding
        if not (np.isfinite(d) and d > 0.0):
            return 0.0
        out = float(np.ldexp(d, self.eA))
        if not np.isfinite(out):
            # the true norm really is past the ceiling: saturate, never `inf`
            self.n_saturated += 1
            return _MAXF
        if 0.0 < out < _TINY:
            # The recombination landed in the SUBNORMAL range, where `ldexp` is
            # no longer exact -- it rounds, by up to half an ULP, and half an ULP
            # there is ~1e-6 relative, which is far more than the deflation above
            # could remove (a 1e-12 deflation of a subnormal is a no-op).  This is
            # the residue of leg 101's second mechanism, and one step down is
            # enough: the only error left is that single rounding.
            out = float(np.nextafter(out, -np.inf))
        return out if out > 0.0 else 0.0

    def report(self):
        return {"probed": int(self.n_probed), "rejected": int(self.n_rejected),
                "saturated": int(self.n_saturated),
                "max_rel_bound": float(self.max_rel),
                "pow2_exponent": int(self.eA)}


def sign_pattern_lower(A, dom, cod, n_rows=40):
    """The baseline every earlier leg used: raw sign-pattern directions."""
    q = _Quotient(A, dom, cod)
    A = np.asarray(A, dtype=float)
    with np.errstate(all="ignore"):
        B = A / cod.w[None, :]
    rows = np.unique(np.linspace(0, A.shape[0] - 1, int(n_rows)).astype(int))
    best, rel, arg = 0.0, 0.0, -1
    for i in rows:
        with np.errstate(all="ignore"):
            g = np.sign(B[i]) / cod.w
        g[0] = 0.0
        p = q.probe(g)
        if p is not None and p[0] > best:
            best, rel, arg = p[0], p[1], int(i)
    out = {"lower": q.certify(best, rel), "row": arg,
           "family": "raw sign patterns"}
    out.update(q.report())
    return out


def smooth_family(theta, cod_w, n_centre=40, n_step=60):
    """The candidate directions: 1/v times a slowly varying shape.

    Yields (name, g).  Every member has the codomain weight built in, so the sup
    part of its norm is O(1) and the seminorm is whatever the shape costs.
    """
    with np.errstate(all="ignore"):
        iv = 1.0 / cod_w
    th = np.asarray(theta, dtype=float)
    for b in (0.0, 0.5, 1.0, 2.0, 4.0):
        yield "pow%.1f" % b, iv * np.cos(0.5 * th) ** b
    for k in range(0, 9):
        yield "cos%d" % k, iv * np.cos(k * th)
    for c0 in np.linspace(0.02, np.pi - 0.02, int(n_centre)):
        for w in (0.01, 0.03, 0.08, 0.2, 0.5, 1.0, 2.0, 4.0):
            yield "bump%.2f/%.2f" % (c0, w), iv * np.exp(-((th - c0) / w) ** 2)
    for c0 in np.linspace(0.02, np.pi - 0.02, int(n_step)):
        for w in (0.02, 0.2):
            yield "step%.2f/%.2f" % (c0, w), iv * np.tanh((th - c0) / w)
    for c0 in np.linspace(0.05, np.pi - 0.2, 16):
        for c1 in np.linspace(0.05, np.pi - 0.05, 16):
            if c1 > c0:
                yield ("box%.2f-%.2f" % (c0, c1),
                       iv * (np.tanh((th - c0) / 0.05) - np.tanh((th - c1) / 0.05)))


def family_lower(A, dom, cod, theta, **kw):
    """max over the smooth family -- the honest lower bound."""
    q = _Quotient(A, dom, cod)
    best, rel, arg = 0.0, 0.0, ""
    for name, g in smooth_family(theta, cod.w, **kw):
        g = g.copy()
        g[0] = 0.0
        p = q.probe(g)
        if p is not None and p[0] > best:
            best, rel, arg = p[0], p[1], name
    out = {"lower": q.certify(best, rel), "argmax": arg,
           "family": "smooth shapes / v"}
    out.update(q.report())
    return out


def ascend(A, dom, cod, theta, g0, K=24, iters=3000, seed=0, scale=0.35):
    """Random ascent in a smooth cosine basis, starting from `g0`.

    Reported even when it adds nothing: a flat maximum is information about the
    shape of the problem, not a failed experiment.

    The trial step is sized proportional to the bound found so far -- leg 101's
    third mechanism, and the reason this routine could overflow itself on a
    large-norm operator with no degenerate input of any kind.  The step law is
    KEPT (changing it would change which directions the search visits, i.e. it
    would sharpen or blunt the bound, which this repair may not do); what changed
    is that every candidate is evaluated through `_Quotient`, so a step that runs
    out of exponent range yields a REJECTED candidate instead of an `inf`
    headline, and `cur` can never become non-finite.
    """
    q = _Quotient(A, dom, cod)
    rng = np.random.default_rng(int(seed))
    with np.errstate(all="ignore"):
        iv = 1.0 / cod.w
        basis = np.array([iv * np.cos(k * np.asarray(theta)) for k in range(int(K))])
    cur = np.asarray(g0, dtype=float).copy()
    cur[0] = 0.0
    p = q.probe(cur)
    best, rel = (0.0, 0.0) if p is None else p

    for _ in range(int(iters)):
        # `best` is held in the rescaled problem; the step law is stated in the
        # caller's units, so it is recombined here -- and clamped rather than
        # allowed to become `inf`, which would poison `cur`.
        with np.errstate(all="ignore"):
            b = float(np.ldexp(best, q.eA))
        if not np.isfinite(b):
            b = _MAXF
        with np.errstate(all="ignore"):
            step = scale * b * (rng.normal(size=int(K)) @ basis) / np.sqrt(K)
            cand = cur + step * rng.uniform(0.2, 1.0)
        cand[0] = 0.0
        p = q.probe(cand)
        if p is not None and p[0] > best:
            cur, best, rel = cand, p[0], p[1]
    out = {"lower": q.certify(best, rel), "vector": cur}
    out.update(q.report())
    return out


def best_lower(A, dom, cod, theta, ascent_iters=3000, **kw):
    """The full construction: baseline, family, ascent -- and the bracket inputs."""
    base = sign_pattern_lower(A, dom, cod)
    fam = family_lower(A, dom, cod, theta, **kw)
    g0 = None
    for name, g in smooth_family(theta, cod.w, **kw):
        if name == fam["argmax"]:
            g0 = g
            break
    asc = ascend(A, dom, cod, theta, g0, iters=ascent_iters) if g0 is not None \
        else {"lower": fam["lower"], "rejected": 0, "saturated": 0,
              "max_rel_bound": 0.0}
    return {"sign_patterns": base["lower"], "smooth_family": fam["lower"],
            "family_argmax": fam["argmax"], "after_ascent": asc["lower"],
            "lower": float(max(base["lower"], fam["lower"], asc["lower"])),
            "ascent_gain": asc["lower"] / fam["lower"] if fam["lower"] > 0 else 1.0,
            "rejected": int(base["rejected"] + fam["rejected"]
                            + asc.get("rejected", 0)),
            "saturated": int(base["saturated"] + fam["saturated"]
                             + asc.get("saturated", 0)),
            "max_rel_bound": float(max(base["max_rel_bound"], fam["max_rel_bound"],
                                       asc.get("max_rel_bound", 0.0)))}
