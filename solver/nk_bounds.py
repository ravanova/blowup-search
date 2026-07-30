"""Genuine UPPER bounds for the Route-D Newton-Kantorovich constants.

Five Route-D legs produced a space (v3/v4/v5: decay grading alpha x Holder
smoothness gamma) and a set of MEASUREMENTS in it.  None of those measurements
was an upper bound:

  * ||A|| and C_Q were FAMILY-RESTRICTED -- maxima over a finite test family, so
    LOWER bounds (solver/holder_norms.py::family_op_norm says so itself).  The
    reported budget was an upper bound built on lower bounds: not a quantity a
    certificate could use.
  * Z1 was never bounded at all.  v4 W6 QUANTIFIED the collocation truncation
    (J^-2.1..-2.6) and stopped there.

This module supplies what can be supplied in closed form, and -- equally
important -- establishes which of the obvious routes are UNSOUND.

--------------------------------------------------------------------------
(A) THE DISCRETE-BALL TRAP  (why the obvious route to an upper bound fails)
--------------------------------------------------------------------------
The temptation is to compute the induced norm by duality over the DISCRETE unit
ball: for a domain functional with coefficient row c, take sup over grid vectors
g with (discrete) ||g||_Y <= 1.  That is unsound, and the failure is not subtle.

A discrete Holder seminorm only inspects pairs of GRID NODES.  A grid vector that
alternates in sign at the grid scale therefore reports a modest seminorm, while
the trigonometric interpolant it stands for oscillates violently BETWEEN nodes
and has an enormous continuum norm.  Measured on the extremizer that duality
actually selects, and comparing over the same theta-range, the inflation is a
factor 3e3 at J = 125 rising to 5e4 at J = 500 -- growing like J^2
(`discrete_ball_inflation`), while a smooth element of the same class stays
faithful.  The "worst direction" is simply not in the true unit ball.

This is banked lesson (9) -- BUILD THE ADVERSARY -- meeting its mirror image.
There, random sampling MISSED the adversary and reported boundedness that was
false.  Here, a discrete norm INVENTS an adversary and reports unboundedness that
is false.  A test family that is too small errs one way; a ball that is too big
errs the other.  Both are the instrument, not the operator.

The sound route is to use only inequalities that the CONTINUUM norm implies:

    |g_m| <= ||g||_Y / v_m ,      |g_m - g_m0| <= ||g||_Y / q_{m,m0}          (D)

-- both hold for the continuum norm because it dominates the discrete one on
nodal values.  Applying (D) to a functional row c and minimising over a reference
index m0 gives `two_point_dual`,

    ||c||_{Y*} <= min_{m0} [ |sum_m c_m| / v_m0 + sum_m |c_m| / q_{m,m0} ] ,

a bound valid against the continuum ball.  Minimising over a SUBSET of m0 keeps
it valid (a min over fewer terms is larger).  On the sup part of the domain norm
this bound SATURATES -- 5.53 flat from J = 125 to J = 1600 -- and is the
project's first genuine uniform upper bound on any part of ||A||.  On the domain
SEMINORM part it is valid but lossy, growing like J^gamma; the refined-grid test
shows the direction it prices is not in the continuum ball, so that growth is the
bound's slack, not the operator's behaviour.  (The continuum expectation is that
the seminorm part is comfortably finite: the inverse gains a whole derivative,
h_X = -(g + H(h) + X h)/c, so g in C^{0,gamma} puts h in C^{1,gamma}.)

--------------------------------------------------------------------------
(B) THE FAR-FIELD MODELLING ERROR, IN CLOSED FORM
--------------------------------------------------------------------------
v3's far-field model is L h = -c h_X - h/X, whose inverse norm between the
decay-graded sup norms is exactly 2/|alpha-2|.  The full linearization at the
anchor Omega_2 = -1/(1+X^2), H(Omega_2) = -X/(1+X^2) is
DF h = h H(Omega_2) + Omega_2 H(h) - c h_X, so the modelling error is an exact
two-term identity (gated to 1.5e-16 relative):

    (DF - L) h = h [H(Omega_2) + 1/X] + Omega_2 H(h)
               = h / (X (1 + X^2))  -  H(h) / (1 + X^2).                    (E)

The first term is pointwise.  The second needs |H(h)| in the far field for an
ARBITRARY h in the unit ball -- exactly where v4's adversary lives (H is
unbounded on L^infinity) and exactly what the Holder grading pays for.  Splitting
the principal value at half-scale,

    |H(h)(X)| <= (1/pi) [ I_near(X) + I_out(X) ] ,
    I_near <= (4/3) S 2^gamma (X/2)^gamma / gamma  +  (8/15) (1+(X/2)^2)^{-alpha/2},
    I_out  =  int_{y>=0, |y-X| > X/2} (1+y^2)^{-alpha/2} |K(X,y)| dy ,      (H)
    K(X,y) = 2X / (X^2 - y^2)     (the EVEN-function form of the kernel)

the singular half paid by the seminorm and the regular half by the decay
envelope.  v5 fixed the seminorm weight at alpha-gamma in THETA; converting with
|dtheta| <= 2 |dX| / (1 + X_min^2) (the Jacobian decreases in |X|, so the smaller
endpoint dominates) gives `holder_local_X_constant`,

    |h(y1) - h(y2)| <= 2^gamma (1 + min(y1,y2)^2)^{-(alpha+gamma)/2} |y1-y2|^gamma

-- note the X-side weight is alpha+gamma, not alpha-gamma.  I_out carries the far
field's 1/X: most mass sits at |y| = O(1), where |K| ~ 2/X, so I_out -> M_alpha/X
-- the SHARP constant, recovered because the even kernel keeps the cancellation
a two-sided 1/(X-y) split discards (measured X * bound -> 1.681 vs M/pi = 1.669).

Feeding (H) into (E) and taking the sup over X >= X0 gives
`farfield_modelling_error_bound` -- the first bounded piece of Z1 in six legs --
and feeding (H) into |h H(h)| gives `quadratic_constant_upper`, the first upper
bound on the quadratic constant.  Using the EVEN kernel is not cosmetic: it makes
the bound finite as X -> 0 (H of an even function is odd, so H(h)(0) = 0, which a
two-sided split cannot see and where it diverges logarithmically) and it recovers
the sharp far-field constant M_alpha/(pi X) instead of twice it.

--------------------------------------------------------------------------
WHAT THIS MODULE DOES NOT BOUND (carry the caveat)
--------------------------------------------------------------------------
Plain float64 throughout: analytic bounds with numerically evaluated constants,
gated against measurements.  NOT interval arithmetic, NOT rigorous.  And these
remain outside it:

  * the domain-SEMINORM part of ||A|| (see (A) -- bounded in the continuum by the
    derivative-gain argument, but not yet by a computation);
  * the CORE <-> FAR-FIELD coupling of Z1.  A sharp split at X0 has a 1/(X - X0)
    seam, because H is nonlocal, so it needs a smooth cutoff and a commutator
    estimate;
  * the CORE discretization error (v4's J^-2.1..-2.6).

So no budget computed from this module is a certificate, and any budget quoted is
CONDITIONAL on the three items above.
"""

import numpy as np

from solver.decay_collocation import grid
from solver.decay_grading import cos_power_mass


# ---------------------------------------------------------------------------
# (A) duality that is valid against the CONTINUUM ball
# ---------------------------------------------------------------------------


def two_point_dual(C, v_cod, q_cod, cand):
    """Upper bounds on ||c||_{Y*} for each row c of C, valid for the continuum ball.

    `v_cod` : codomain sup weights;  `q_cod` : codomain seminorm kernel
    (min(w_semi)/|dtheta|^gamma, diagonal suppressed);  `cand` : indices of the
    reference points m0 to minimise over (a subset keeps the bound valid).

    Uses only (D) of the module docstring, both of which the continuum norm
    implies, so nothing here depends on the discrete ball being faithful.
    """
    C = np.atleast_2d(np.asarray(C, dtype=float))
    cand = np.asarray(cand, dtype=int)
    q = np.asarray(q_cod, dtype=float)[:, cand]
    with np.errstate(divide="ignore"):
        invq = np.where(q > 0, 1.0 / q, 0.0)
    total = np.abs(C.sum(axis=1))[:, None] / np.asarray(v_cod, dtype=float)[cand][None, :]
    return (np.abs(C) @ invq + total).min(axis=1)


def sup_part_upper(A, w_dom, v_cod, q_cod, n_cand=24):
    """max_i w_i ||A_i.||_{Y*}: a uniform upper bound on the domain SUP part of ||A||.

    This is the piece that saturates in J (5.53 at alpha=1.5, gamma=0.5).
    """
    J = A.shape[1]
    cand = np.unique(np.linspace(1, J - 1, int(n_cand)).astype(int))
    return float((np.asarray(w_dom, dtype=float)
                  * two_point_dual(A, v_cod, q_cod, cand)).max())


def seminorm_part_upper(A, pair_dom, v_cod, q_cod, n_cand=16, chunk=48):
    """max_{j,k} p_jk ||A_j. - A_k.||_{Y*}: VALID but lossy (grows like J^gamma).

    Reported so the slack can be seen, not because it is usable.  O(J^3).
    """
    J = A.shape[0]
    cand = np.unique(np.linspace(1, A.shape[1] - 1, int(n_cand)).astype(int))
    pair_dom = np.asarray(pair_dom, dtype=float)
    best = 0.0
    for lo in range(0, J, chunk):
        hi = min(lo + chunk, J)
        D = (A[lo:hi, None, :] - A[None, :, :]).reshape(-1, A.shape[1])
        d = two_point_dual(D, v_cod, q_cod, cand).reshape(hi - lo, J)
        best = max(best, float((d * pair_dom[lo:hi, :]).max()))
    return best


def discrete_ball_inflation(to_coef, J, vec, norm_factory, R=6):
    """||interpolant||_continuum / ||vec||_discrete for one nodal vector.

    The number that condemns discrete-ball duality: for the extremizer that
    duality selects it is ~5e5 at J=125, rising like J^2 to ~3e7 at J=1000.
    `norm_factory(theta, X)` builds the norm object for a given grid, so the SAME
    norm is applied on the coarse grid and on the R-times finer one.
    """
    th_f, X_f, fine = refine(to_coef, J, vec, R=R)
    th_c, X_c = grid(J)
    # Compare the two norms over the SAME domain.  The finer grid reaches
    # theta closer to pi (X larger by a factor R), and out there the degree-J
    # interpolant no longer tracks whatever it interpolates -- it oscillates,
    # against an enormous weight.  Including that region would measure
    # extrapolation error, not fidelity, so cut the fine grid at the coarse
    # grid's outermost node.
    keep = th_f <= th_c[-1]
    th_f, X_f, fine = th_f[keep], X_f[keep], fine[keep]
    n_disc = norm_factory(th_c, X_c)(vec)
    n_cont = norm_factory(th_f, X_f)(fine)
    return {"discrete": float(n_disc), "continuum": float(n_cont),
            "inflation": float(n_cont / n_disc) if n_disc > 0 else float("inf")}


def refine(to_coef, theta_len, vec, R=6):
    """Exact values of the trig interpolant of `vec` on an R-times finer grid.

    Returns (theta_fine, X_fine, values).  The interpolant is the object the
    nodal vector actually stands for, so this is how a discrete norm is checked
    for faithfulness.
    """
    coef = to_coef @ np.asarray(vec, dtype=float)
    J = coef.size
    th_f, X_f = grid(int(R) * theta_len)
    k = np.arange(J)
    return th_f, X_f, np.cos(np.outer(th_f, k)) @ coef


# ---------------------------------------------------------------------------
# (B) the far-field modelling error and the quadratic constant
# ---------------------------------------------------------------------------


def holder_local_X_constant(alpha, gamma, X_min):
    """Envelope of |h(y1)-h(y2)| / |y1-y2|^gamma for ||h||_{alpha,gamma} <= 1.

    2^gamma (1 + X_min^2)^{-(alpha+gamma)/2}, X_min = min(|y1|,|y2|).
    """
    return (2.0 ** gamma) * (1.0 + np.asarray(X_min, dtype=float) ** 2) ** (
        -0.5 * (alpha + gamma))


def _trapz(f, y):
    return float(np.trapezoid(f, y)) if hasattr(np, "trapezoid") else float(
        np.trapz(f, y))                                            # noqa: NPY201


def _I_out(X, alpha, n=1201, Ymax_factor=1e8):
    """int over y >= 0, |y-X| > X/2, of (1+y^2)^{-alpha/2} |K(X,y)| dy.

    K(X,y) = 2X / (X^2 - y^2) is the EVEN-function form of the line Hilbert
    kernel: for h even, H(h)(X) = (1/pi) p.v. int_0^inf h(y) K(X,y) dy.  Using it
    rather than the two-sided 1/(X-y) matters at BOTH ends -- it makes the bound
    vanish as X -> 0 (H of an even function is odd, so H(h)(0) = 0, which the
    two-sided split cannot see and where it diverges logarithmically), and it
    delivers the sharp far-field constant M_alpha / X rather than twice it,
    because the mass at |y| = O(1) sees |K| ~ 2/X.

    The bulk [0, X/2] is graded logarithmically: the mass of (1+y^2)^{-alpha/2}
    sits at y = O(1) while the bulk reaches X/2, so a linear grid misses it
    entirely once X is large and silently reports a far-field bound that does not
    decay.
    """
    X = float(X)
    def q(y):                                                      # noqa: E306
        K = np.abs(2.0 * X / (X * X - y * y))
        return _trapz((1.0 + y ** 2) ** (-0.5 * alpha) * K, y)
    eps = 1e-12 * max(X, 1.0)
    total = q(np.concatenate(([0.0], np.geomspace(eps, 0.5 * X, n))))
    total += q(np.geomspace(1.5 * X, Ymax_factor * max(X, 1.0), n))
    return total


def hilbert_farfield_bound(X, alpha, gamma, n=1201):
    """Upper bound on |H(h)(X)| for every EVEN h in the unit ball of ||.||_{alpha,gamma}.

    Principal value split at half-scale, on the even kernel K(X,y)=2X/(X^2-y^2).
    On the band y in [X/2, 3X/2] write K = g(y)/(X-y) with g(y) = 2X/(X+y), so

        p.v. int_band h K dy = int_0^{X/2} [h(X-t) g(X-t) - h(X+t) g(X+t)] dt / t

    and split that into the Holder part (h's increment, g bounded by 4/3 on the
    band) and the kernel part (g's increment, |g(X-t)-g(X+t)| = 4Xt/(4X^2-t^2)
    <= (16/15) t / X for t <= X/2, against |h| <= envelope(X/2)).  Returns
    (bound, near_part, out_part).
    """
    X = float(X)
    delta = 0.5 * X
    S = float(holder_local_X_constant(alpha, gamma, 0.5 * X))
    env = (1.0 + (0.5 * X) ** 2) ** (-0.5 * alpha)
    I_holder = (4.0 / 3.0) * S * (2.0 ** gamma) * delta ** gamma / gamma
    I_kernel = (16.0 / 15.0) * env * delta / X
    I_near = I_holder + I_kernel
    I_out = _I_out(X, alpha, n=n)
    return (I_near + I_out) / np.pi, I_near / np.pi, I_out / np.pi


def farfield_modelling_error_bound(alpha, gamma, X0, Xmax_factor=1e4,
                                   n_X=40, n_quad=1201):
    """||(DF - L)||_{X -> Y} restricted to the far field {X >= X0}.

    From (E):  (1+X^2)^{(alpha+1)/2} |(DF-L)h| <= 1/(X sqrt(1+X^2))
               + (1+X^2)^{(alpha-1)/2} |H(h)(X)| .
    For alpha < 2 both terms decay, so the supremum sits at X0; the grid confirms
    it rather than assuming it.
    """
    Xs = np.geomspace(float(X0), float(X0) * Xmax_factor, int(n_X))
    vals, t1s, t2s = [], [], []
    for X in Xs:
        t1 = 1.0 / (X * np.sqrt(1.0 + X * X))
        hb, _, _ = hilbert_farfield_bound(X, alpha, gamma, n=n_quad)
        t2 = (1.0 + X * X) ** (0.5 * (alpha - 1.0)) * hb
        vals.append(t1 + t2); t1s.append(t1); t2s.append(t2)
    vals = np.asarray(vals)
    i = int(vals.argmax())
    return {"bound": float(vals.max()), "argmax_X": float(Xs[i]),
            "pointwise_term": float(t1s[i]), "hilbert_term": float(t2s[i]),
            "X": Xs.tolist(), "value": vals.tolist()}


def quadratic_constant_upper(alpha, gamma, X_lo=1e-3, X_hi=1e6, n_X=160,
                             n_quad=1201):
    """Upper bound on the SUP part of C_Q = sup ||h H(h)||_Y / ||h||_X^2.

    |h| <= ||h|| (1+X^2)^{-alpha/2} and |H(h)| <= ||h|| B(X) give

        (1+X^2)^{(alpha+1)/2} |h H(h)| <= ||h||^2 (1+X^2)^{1/2} B(X) ,

    whose supremum is finite because B(X) ~ 2 M_alpha / (pi X) far out.  This
    bounds only the sup part of the codomain norm; the codomain seminorm of
    h H(h) is not bounded here.
    """
    Xs = np.geomspace(X_lo, X_hi, int(n_X))
    vals = [np.sqrt(1.0 + X * X) * hilbert_farfield_bound(X, alpha, gamma,
                                                          n=n_quad)[0]
            for X in Xs]
    vals = np.asarray(vals)
    i = int(vals.argmax())
    return {"C_Q_sup_upper": float(vals.max()), "argmax_X": float(Xs[i]),
            "asymptote": float(cos_power_mass(alpha) / np.pi)}


def farfield_mass(alpha):
    """int (1+y^2)^{-alpha/2} dy -- the sharp constant in H(h) ~ (int h)/(pi X)."""
    return cos_power_mass(alpha)


# ---------------------------------------------------------------------------
# (C) assembly
# ---------------------------------------------------------------------------


def budget(Y0, Z0, Z1, Z2):
    """Radii-polynomial contraction budget: p(r) = Z2 r^2 - (1-Z0-Z1) r + Y0."""
    one_minus = 1.0 - Z0 - Z1
    Y0_max = (one_minus ** 2) / (4.0 * Z2) if (one_minus > 0 and Z2 > 0) else 0.0
    disc = one_minus ** 2 - 4.0 * Z2 * Y0
    closes = bool(one_minus > 0 and Z2 > 0 and disc >= 0)
    r_min = float((one_minus - np.sqrt(disc)) / (2.0 * Z2)) if closes else float("nan")
    return {"one_minus_Z": float(one_minus), "Y0_max": float(Y0_max),
            "closes": closes, "r_min": r_min}
