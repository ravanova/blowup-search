"""The codomain SEMINORM part of C_Q: weighted Holder boundedness of H.

This is the last constant in the Route-D ledger that the quadratic C_Q needs and
the only one v7's (alpha, gamma) map still omitted.  v7 said so in its own
caveat: the map's Z2 was assembled from upper bounds everywhere EXCEPT the
codomain seminorm of h H(h), and the omission is worst exactly where gamma is
smallest -- i.e. exactly where v7's optimum sat.  So the location (1.4, 0.15) was
provisional for a reason this module removes.

--------------------------------------------------------------------------
WHAT HAS TO BE BOUNDED, AND WITH WHICH WEIGHT
--------------------------------------------------------------------------
With Q(h) = h H(h) and psi = H(h), the codomain seminorm of the product splits
by the increment product rule, expanded about the INNER point of the pair
(theta_i = the one with smaller |theta|, which is where min(w) sits):

    w_{alpha+1-gamma}(th_i) |Q(th_1) - Q(th_2)| / d^gamma
        <=  [ w_{alpha+1-gamma} |h(th_i)| / d^gamma ] |dpsi|
          + [ w_{alpha+1-gamma} |psi(th_o)| / d^gamma ] |dh|
        <=  S * { w_{1-gamma}(th_i) |dpsi| / d^gamma }  +  T * w_1(th_i) B(th_o)

using |h| <= S / w_alpha and |dh| <= T d^gamma / w_{alpha-gamma}.  Two things
fall out of that line and both matter:

  * the SECOND term is already bounded, by v6's own quantity: w_1(th_i) <=
    w_1(th_o) because w increases in |theta|, so w_1(th_i) B(th_o) <= sup_theta
    w_1 B = the C_Q SUP part v6 computed.  No new work.

  * the FIRST term needs the weighted Holder seminorm of psi with weight
    **1 - gamma**, not alpha - gamma.  That is the whole point: H does not
    inherit h's decay.  For even h with nonzero mass, H(h)(X) -> (int h)/(pi X)
    however fast h decays, so psi's decay grading is 1 and its seminorm weight is
    1 - gamma by the same rule that gave the domain its alpha - gamma.  Asking
    for weight alpha - gamma here would be asking for something false.

So the quantity to bound is

    T_psi = sup_{th1 != th2} min(w_{1-gamma}) |psi(th1) - psi(th2)| / |dtheta|^gamma
          <= b_sup * S  +  b_semi * T .                                     (C_H)

--------------------------------------------------------------------------
THE ESTIMATE
--------------------------------------------------------------------------
Work relative to th_1: put phi = th_1 + t and th_2 = th_1 + sigma, |sigma| = d.
In t the two poles sit at t = 0 and t = sigma and NOTHING wraps, which is the
reason for the change of variable: in absolute theta the pair (th near pi,
phi near -pi) is a pair of NEIGHBOURS on the circle, and a "near region" defined
as an interval of the line would put a singularity in the far region.

Using p.v. int cot = 0 on the whole circle, psi(th) = (1/2pi) p.v. int [h(phi) -
h(th)] cot((th-phi)/2) dphi, and with N = [min(0,sigma) - 2d, max(0,sigma) + 2d]
the near region in t,

    psi(th1) - psi(th2) = (1/2pi) [ E_N + E_F + G ] ,
    E_N = int_N [h-h(th1)] cot(-t/2) dt  -  int_N [h-h(th2)] cot((sigma-t)/2) dt
    E_F = int_F [h-h(th1)] [cot(-t/2) - cot((sigma-t)/2)] dt
    G   = [h(th2) - h(th1)] int_F cot((sigma-t)/2) dt .

Each piece is then bounded by an integral of an EXPLICIT majorant:

  * increments of h by whichever of the two norm parts is cheaper at that point,
    |h(phi) - h(ref)| <= min( T |phi-ref|^gamma cos^{alpha-gamma}(th_near/2) ,
                              S [cos^alpha(phi/2) + cos^alpha(ref/2)] ) ,
    the choice made pointwise by a rule that does not depend on S or T (so the
    result stays LINEAR in (S, T) and can be reported as a pair of coefficients);
  * the kernels EXACTLY, with the far-field difference in the stable form
    cot(t/2) + cot((sigma-t)/2) = sin(sigma/2) / (sin(t/2) sin((sigma-t)/2)),
    which keeps the O(d) cancellation that makes E_F small;
  * G in closed form: int_F cot((sigma-t)/2) dt = -p.v. int_N = 2 log|sin((sigma
    -n1)/2) / sin((sigma-n2)/2)| -> 2 log(3/2) as d -> 0.

The estimate is used only for pairs with d <= (pi - |th_i|)/6, which guarantees
N stays inside the circle and that every point of N has pi - |phi| >= (pi -
|th_i|)/2, so the decay weights vary by a bounded factor across it.  For all
other pairs -- in particular the two-points-near-opposite-ends pairs, where the
circle distance is O(1) but the weight is huge -- the POINTWISE route is used
instead: |dpsi| <= |psi(th1)| + |psi(th2)| with v7's split pointwise bound.  Both
routes are valid, the choice per pair is made by a fixed rule (smaller
coefficient sum), and the reported (b_sup, b_semi) are the per-coefficient maxima
over the pair sweep -- valid, and lossy only by the mismatch between the two
maximizing pairs.

The two divergences are structural and both are present: b ~ 1/gamma from the
near region (int |t|^{gamma-1}) and b ~ 1/(1-gamma) from the far region (int
d |t|^{gamma-2}).  So C_H BOWLS in gamma, which is what puts an interior optimum
back into Z2 after v7's map ran off its own grid edge.

--------------------------------------------------------------------------
WHAT THIS IS NOT (carry the caveat)
--------------------------------------------------------------------------
Plain float64.  The pair supremum is taken over a GRID of (th, d), refined until
it stops moving (`sweep_convergence`) -- a grid sup UNDER-reports, which is the
mirror of the v6 discrete-ball trap, so the refinement study is not optional and
the bound should be read as "the majorant, sampled finely" rather than as a
certified supremum.  The majorant itself is honest: every inequality above is
pointwise in phi and holds for every h in the ball.

Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np

from solver.nk_seminorm import hilbert_split_bound

TWO_PI = 2.0 * np.pi


def wrap(theta):
    """Reduce to (-pi, pi] -- the circle identification, used for the envelopes."""
    return (np.asarray(theta, dtype=float) + np.pi) % TWO_PI - np.pi


def cos_half(theta):
    """cos(theta/2) = (1+X^2)^{-1/2} on the wrapped angle; the inverse decay weight."""
    return np.cos(0.5 * wrap(theta))


def _increment_env(phi, ref, alpha, gamma):
    """(c_S, c_T) with |h(phi) - h(ref)| <= c_S S + c_T T, one route per point.

    Distances are FOLDED, |{|phi|} - {|ref|}|, because the project's norms live
    on theta in (0, pi) and h is even: a pair straddling theta = 0 has increment
    zero, and the seminorm knows that.  Folding is also the only reading that
    keeps the bound valid -- the circle distance would over-state how far apart
    the two arguments of h are and hence claim an increment the seminorm does not
    supply.

    The Holder route uses the weighted seminorm (whose min-weight sits at
    whichever point is closer to theta = 0) and the sup route the decay envelope
    at both points.  The choice is made by comparing the two at S = T = 1, a rule
    that depends only on (phi, ref, alpha, gamma) -- so the result is a genuine
    linear bound in (S, T), not a concave envelope.
    """
    a_phi = np.abs(wrap(np.asarray(phi, dtype=float)))
    a_ref = abs(float(wrap(ref)))
    dphi = np.abs(a_phi - a_ref)
    inner = np.minimum(a_phi, a_ref)
    cT = dphi ** gamma * np.cos(0.5 * inner) ** (alpha - gamma)
    cS = np.cos(0.5 * a_phi) ** alpha + np.cos(0.5 * a_ref) ** alpha
    take_T = cT <= cS
    return np.where(take_T, 0.0, cS), np.where(take_T, cT, 0.0)


def _log_quad2(f_of_s, s_lo, s_hi, n):
    """int f ds for a 2-vector integrand, via the log substitution s^{p-1} -> s^p."""
    s = np.geomspace(s_lo, s_hi, int(n))
    y = np.asarray(f_of_s(s)) * s
    ls = np.log(s)
    tz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz     # noqa: NPY201
    return float(tz(y[0], ls)), float(tz(y[1], ls))


def _cot(u):
    return np.cos(0.5 * u) / np.sin(0.5 * u)


def near_padding(d, pad_max=2.0, pad_min=0.2, safety=0.9):
    """Half-width of the near region, in units of d: N = [min(0,s)-p d, max(0,s)+p d].

    The decomposition needs N to cover the circle at most once, i.e. (1+p) d <=
    pi.  For narrow pairs that is no constraint and p = 2 (the classical choice,
    which makes the far kernel's O(d) cancellation comfortable); for wide ones the
    padding is shrunk instead of abandoning the estimate, because the alternative
    -- the pointwise route -- is ~400x worse.
    """
    d = float(d)
    p = min(float(pad_max), float(safety) * (np.pi / d - 1.0))
    return p if p >= float(pad_min) else None


def increment_pair_bound(theta1, sigma, alpha, gamma, n_quad=400, eps=1e-10):
    """(u_S, u_T) for the weighted increment ratio of psi at one pair.

    Returns coefficients of S and T in

        w_{1-gamma}(th_inner) |psi(th1) - psi(th2)| / d^gamma <= u_S S + u_T T ,

    th2 = th1 + sigma, d = |sigma|.  Valid only in the regime d <= (pi-|th_i|)/6
    (see the module docstring); `increment_regime` tests it.
    """
    th1 = float(theta1)
    sig = float(sigma)
    d = abs(sig)
    th2 = th1 + sig
    pad = near_padding(d)
    if pad is None:
        raise ValueError("pair too wide for the increment route (d = %.3f)" % d)
    n1, n2 = min(0.0, sig) - pad * d, max(0.0, sig) + pad * d

    cS = cT = 0.0

    # ---- E_N : both reference points, each with its own exact kernel ----
    for ref, pole, kern in ((th1, 0.0, lambda t: _cot(-t)),
                            (th2, sig, lambda t: _cot(sig - t))):
        for lo, hi in ((pole - n1, "down"), (n2 - pole, "up")):
            if lo <= 0:
                continue
            sgn = -1.0 if hi == "down" else 1.0

            def integrand(s, ref=ref, pole=pole, kern=kern, sgn=sgn):
                t = pole + sgn * s
                a, b = _increment_env(th1 + t, ref, alpha, gamma)
                return np.stack([a, b]) * np.abs(kern(t))

            vS, vT = _log_quad2(integrand, eps * lo, lo, n_quad)
            cS += vS
            cT += vT

    # ---- E_F : the two tails, exact kernel difference (stable form) ----
    for lo, hi, sgn in ((n2, np.pi, 1.0), (-n1, np.pi, -1.0)):
        if lo >= hi:
            continue

        def integrand(t_abs, sgn=sgn):
            t = sgn * t_abs
            a, b = _increment_env(th1 + t, th1, alpha, gamma)
            k = np.abs(np.sin(0.5 * sig) / (np.sin(0.5 * t) * np.sin(0.5 * (t - sig))))
            return np.stack([a, b]) * k

        vS, vT = _log_quad2(integrand, lo, hi, n_quad)
        cS += vS
        cT += vT

    # ---- G : closed form ----
    L = 2.0 * np.log(abs(np.sin(0.5 * (sig - n1)) / np.sin(0.5 * (sig - n2))))
    gS, gT = _increment_env(np.array([th2]), th1, alpha, gamma)
    cS += abs(L) * float(gS[0])
    cT += abs(L) * float(gT[0])

    inner = min(abs(float(wrap(th1))), abs(float(wrap(th2))))
    w = np.cos(0.5 * inner) ** -(1.0 - gamma)
    scale = w / (TWO_PI * d ** gamma)
    return scale * cS, scale * cT


def increment_regime(theta1, sigma):
    """Whether the near region still fits: `near_padding` returns a usable width.

    That is the ONLY restriction the decomposition needs.  For a pair inside
    (0, pi) the separation already satisfies d < pi - theta_inner automatically
    (the outer point cannot pass pi), so the near region never has to reach past
    the endpoint from the inner point's side; and the envelopes wrap and fold, so
    a near region that crosses theta = pi is handled rather than excluded.  An
    earlier draft used d <= (pi - theta_inner)/6, which is what the scaling
    ARGUMENT needs, and the sweep then reported a constant a factor 12 too large
    -- entirely from pairs just outside that cutoff, where the far cruder
    pointwise route had to be used.  The lesson is banked: do not let the regime
    of an ARGUMENT become the regime of the CODE.
    """
    return near_padding(abs(float(sigma))) is not None


def pointwise_pair_bound(theta1, sigma, alpha, gamma, curves=None, n_quad=801):
    """(u_S, u_T) from |dpsi| <= |psi(th1)| + |psi(th2)| and v7's split bound.

    Valid for EVERY pair, and the only route available for the wide ones.
    `curves` is a (X, a_sup, a_semi) triple to interpolate in, which is what makes
    a dense sweep affordable.
    """
    th2 = float(theta1) + float(sigma)
    d = abs(float(sigma))
    aS = aT = 0.0
    for th in (float(theta1), th2):
        X = abs(np.tan(0.5 * wrap(th)))
        if curves is None:
            s, m = hilbert_split_bound(max(X, 1e-12), alpha, gamma, n=n_quad)
        else:
            Xs, a_s, a_m = curves
            lx = np.log(np.clip(X, Xs[0], Xs[-1]))
            s = float(np.interp(lx, np.log(Xs), a_s))
            m = float(np.interp(lx, np.log(Xs), a_m))
        aS += s
        aT += m
    inner = min(abs(float(wrap(theta1))), abs(float(wrap(th2))))
    w = np.cos(0.5 * inner) ** -(1.0 - gamma)
    return w * aS / d ** gamma, w * aT / d ** gamma


def pair_grid(n_theta=48, n_d=28, d_lo=1e-5, d_hi=None):
    """(theta, sigma) pairs inside (0, pi), theta graded to both ends.

    Both members of a pair lie in (0, pi) because that is where the project's
    norms live (solver/decay_collocation.grid): h is even, so the seminorm only
    ever compares X >= 0.  theta is placed by its distance to pi on a log grid
    (the weight's natural variable) plus a log grid down to 0, and sigma spans a
    log grid of separations in BOTH directions, so the inner point of a pair is
    sometimes theta and sometimes theta + sigma.
    """
    d_hi = float(np.pi) if d_hi is None else float(d_hi)
    ell = np.geomspace(1e-4, np.pi, int(n_theta) // 2)
    near0 = np.geomspace(1e-4, np.pi / 2.0, int(n_theta) - int(n_theta) // 2)
    th = np.unique(np.concatenate([np.pi - ell, near0]))
    th = th[(th > 0.0) & (th < np.pi)]
    ds = np.geomspace(float(d_lo), d_hi, int(n_d))
    out = []
    for t in th:
        for d in ds:
            for s in (d, -d):
                if 0.0 < t + s < np.pi:
                    out.append((t, s))
    return out


def hilbert_holder_constant(alpha, gamma, n_theta=48, n_d=28, n_quad=400,
                            curves=None, X_lo=1e-4, X_hi=1e8, n_X=90,
                            rule="increment"):
    """(b_sup, b_semi) with T_psi <= b_sup S + b_semi T, plus where they are attained.

    The per-pair route choice must be a SINGLE rule applied to both coefficients:
    picking the route that minimizes u_sup for one coefficient and the route that
    minimizes u_semi for the other mixes two different valid bounds and is not
    itself one.  Three admissible rules are offered:

      "increment" (default) -- the increment route wherever it is legal, the
          pointwise route only for the wide pairs (d > pi/3) where it is the only
          one available;
      "sum" -- the route with the smaller u_sup + u_semi.  Cheaper-looking, and
          WORSE: at pairs where the sums nearly tie it can hand back the
          pointwise route's much larger u_sup for a marginal gain in the sum, and
          the sweep maximum then jumps by a factor of ten;
      "pointwise" -- the pointwise route everywhere, as a control.
    """
    alpha, gamma = float(alpha), float(gamma)
    if curves is None:
        Xs = np.geomspace(X_lo, X_hi, int(n_X))
        pw = [hilbert_split_bound(X, alpha, gamma) for X in Xs]
        curves = (Xs, np.array([p[0] for p in pw]), np.array([p[1] for p in pw]))
    best_S = best_T = 0.0
    arg_S = arg_T = None
    n_inc = 0
    for th, sig in pair_grid(n_theta=n_theta, n_d=n_d):
        uS, uT = pointwise_pair_bound(th, sig, alpha, gamma, curves=curves)
        if rule != "pointwise" and increment_regime(th, sig):
            vS, vT = increment_pair_bound(th, sig, alpha, gamma, n_quad=n_quad)
            if rule == "increment" or vS + vT < uS + uT:
                uS, uT = vS, vT
                n_inc += 1
        if uS > best_S:
            best_S, arg_S = uS, (th, sig)
        if uT > best_T:
            best_T, arg_T = uT, (th, sig)
    return {"b_sup": float(best_S), "b_semi": float(best_T),
            "argmax_sup": arg_S, "argmax_semi": arg_T, "rule": rule,
            "n_increment_route": int(n_inc), "alpha": alpha, "gamma": gamma}


def sweep_convergence(alpha, gamma, levels=((32, 18), (48, 28), (72, 40)),
                      n_quad=400):
    """The same constant on progressively finer pair grids.

    A supremum sampled on a grid can only UNDER-report -- the mirror of v6's
    discrete-ball trap, where a set that was too big over-reported.  So the
    refinement is part of the measurement, not a nicety.
    """
    out = []
    for nt, nd in levels:
        r = hilbert_holder_constant(alpha, gamma, n_theta=nt, n_d=nd, n_quad=n_quad)
        out.append({"n_theta": nt, "n_d": nd, "b_sup": r["b_sup"],
                    "b_semi": r["b_semi"]})
    return out


# ---------------------------------------------------------------------------
# assembly: the full quadratic constant
# ---------------------------------------------------------------------------


def _quadratic_form_max(a, b, c):
    """max_{S+T=1, S,T>=0} a S^2 + b S T + c T^2 -- exact, on the closed segment."""
    def f(t):
        return a * t * t + b * t * (1.0 - t) + c * (1.0 - t) ** 2
    cands = [0.0, 1.0]
    A, B = a - b + c, b - 2.0 * c          # f(t) = A t^2 + B t + c
    if A != 0.0:
        t = -B / (2.0 * A)
        if 0.0 < t < 1.0:
            cands.append(t)
    return max(f(t) for t in cands)


def quadratic_constant_full(alpha, gamma, C_Q_sup_S, C_Q_sup_T, b_sup, b_semi):
    """C_Q upper bound including the codomain SEMINORM part.

    From the product-rule split of the module docstring, with w_1(th_i) B(th_o)
    <= sup_theta w_1 B = the v6 sup-part quantity (split by payer):

        sup part      <=  C_Q_sup_S S^2 + C_Q_sup_T S T
        seminorm part <=  (b_sup S + b_semi T) S  +  (C_Q_sup_S S + C_Q_sup_T T) T

    and C_Q = max of the total over the unit sphere S + T = 1.
    """
    a = C_Q_sup_S + b_sup
    b = C_Q_sup_T + b_semi + C_Q_sup_S
    c = C_Q_sup_T
    return {"C_Q_full": float(_quadratic_form_max(a, b, c)),
            "coef_S2": float(a), "coef_ST": float(b), "coef_T2": float(c)}


def cq_sup_split(alpha, gamma, X_lo=1e-3, X_hi=1e6, n_X=140, n_quad=801):
    """(sup_X w_1 a_sup, sup_X w_1 a_semi): v6's C_Q sup part, split by payer.

    Splitting matters here for the same reason it did in v7: the two halves are
    maximized at different X, so charging both to the total norm is ~30% lossy.
    """
    Xs = np.geomspace(X_lo, X_hi, int(n_X))
    w1 = np.sqrt(1.0 + Xs ** 2)
    aS, aT = [], []
    for X in Xs:
        s, m = hilbert_split_bound(X, alpha, gamma, n=n_quad)
        aS.append(s)
        aT.append(m)
    return float(np.max(w1 * np.asarray(aS))), float(np.max(w1 * np.asarray(aT)))


# ---------------------------------------------------------------------------
# measurement (LOWER bounds -- the other side of the bracket)
# ---------------------------------------------------------------------------


def conjugate(coef, theta):
    """psi = H(h) exactly, from h's cosine coefficients: cos k th -> sin k th."""
    k = np.arange(np.asarray(coef).size)
    return np.sin(np.outer(np.asarray(theta, dtype=float), k)) @ np.asarray(coef)


def weighted_seminorm(values, theta, beta, gamma):
    """sup min(w_beta) |dv| / |dtheta|^gamma on a grid -- a LOWER bound on the sup."""
    theta = np.asarray(theta, dtype=float)
    v = np.asarray(values, dtype=float)
    w = np.cos(0.5 * wrap(theta)) ** -float(beta)
    d = np.abs(theta[:, None] - theta[None, :])
    np.fill_diagonal(d, np.inf)
    pair = np.minimum(w[:, None], w[None, :]) / d ** float(gamma)
    return float(np.max(pair * np.abs(v[:, None] - v[None, :])))


# ---------------------------------------------------------------------------
# the same decomposition, EXACT -- the second build that gates the majorant
# ---------------------------------------------------------------------------


def decomposition_exact(coef, theta1, sigma, n_quad=4000, eps=1e-12):
    """psi(th1) - psi(th2) from the E_N + E_F + G split, with exact integrands.

    Same regions, same kernels, same closed-form G as `increment_pair_bound` --
    but with the true increments of h instead of their majorants.  Compared
    against the exact conjugate (cos k th -> sin k th) this gates the
    DECOMPOSITION rather than the envelopes, which is the half of the estimate an
    inequality test can never reach.  Banked lesson (3): build the same object
    twice.
    """
    coef = np.asarray(coef, dtype=float)
    th1, sig = float(theta1), float(sigma)
    d = abs(sig)
    th2 = th1 + sig
    pad = near_padding(d)
    n1, n2 = min(0.0, sig) - pad * d, max(0.0, sig) + pad * d

    def h(x):
        k = np.arange(coef.size)
        return np.cos(np.outer(np.atleast_1d(x), k)) @ coef

    h1, h2 = float(h(th1)[0]), float(h(th2)[0])
    tz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz     # noqa: NPY201

    def quad(f, length, pole, sgn):
        """int over the one-sided interval of length `length` starting at `pole`."""
        s = np.geomspace(eps * length, length, int(n_quad))
        return float(tz(f(pole + sgn * s) * s, np.log(s)))

    E_N = 0.0
    E_N += quad(lambda t: (h(t + th1) - h1) * -_cot(t), -n1, 0.0, -1.0)
    E_N += quad(lambda t: (h(t + th1) - h1) * -_cot(t), n2, 0.0, 1.0)
    E_N -= quad(lambda t: (h(t + th1) - h2) * _cot(sig - t), sig - n1, sig, -1.0)
    E_N -= quad(lambda t: (h(t + th1) - h2) * _cot(sig - t), n2 - sig, sig, 1.0)

    def far(t):
        k = np.sin(0.5 * sig) / (np.sin(0.5 * t) * np.sin(0.5 * (sig - t)))
        return -(h(t + th1) - h1) * k

    E_F = quad(far, np.pi - n2, n2, 1.0) + quad(far, np.pi + n1, n1, -1.0)
    L = 2.0 * np.log(abs(np.sin(0.5 * (sig - n1)) / np.sin(0.5 * (sig - n2))))
    G = (h2 - h1) * (-L)
    return (E_N + E_F + G) / TWO_PI
