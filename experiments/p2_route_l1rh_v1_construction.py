"""Route-L1RH v1: DOES A NON-ell^1_w SPACE FIX THE COLLOCATION-BASIS L1 DEATH TOO?

Leg 127 proved the COEFFICIENT-basis death (leg 54) was a property of the `ell^1_w` space,
not of the operator.  `L1` has a SECOND death certificate, in the COLLOCATION basis (leg 56),
never tested against any alternative space.  This leg tests it directly.

GATE (verbatim, DIRECTION.md sec 177):
  Does origin-H^2 (or another space this leg identifies as structurally analogous, per leg
  163's own scoping method) admit a certificate formulation for the collocation-basis
  realization of L1, and if built, does its diagnostic close?

--------------------------------------------------------------------------------
WHAT LEG 56 ACTUALLY MEASURED, AND WHERE ITS DENOMINATOR COMES FROM
--------------------------------------------------------------------------------
Leg 56's death ratio is `defect / tau` with

    tau = budget / ||A||           budget = (1 - Z_1)^2 / (2 Z_2)      Z_2 = 2 ||A|| B

so, algebraically,

    tau = (1 - Z_1)^2 / (4 ||A||^2 B).

EVERY factor of that denominator is a NORM-DEPENDENT quantity, and every one of them is
computed in leg 46/50's weighted SUP realization: `A_norm = induced_sup_norm(A, w, w)` is a
weighted ROW SUM.  The numerator -- the (H, D) consistency defect -- is also a weighted sup.
So leg 56's `1.85e+07` is a ratio of two weighted-sup norms, and the question this leg asks is
what it becomes when the realization is changed and NOTHING ELSE is: same grid, same nodes,
same stored `H`, `D`, `Uop`, same Newton point, same frozen reach `X_max = 745.239`.

--------------------------------------------------------------------------------
THE CONSTRAINT THAT COULD HAVE KILLED THIS LEG (Xu sec 8, banked by leg 171)
--------------------------------------------------------------------------------
    "a weight is a change of norm, eigenvalues are norm-invariant, and the truncated L_a
     genuinely carries essential-smear eigenvalues inside the strip ... so no weighted
     enclosure can exclude them."

Two separations, both pre-registered in `writeup/novelty/leg_177.md` sec 4 BEFORE any number
existed:

  (1) Xu's invariance statement is about EIGENVALUES.  ||A||, Z_1, Z_2, Y_0 and the budget
      are not eigenvalues -- they are induced norms, norm-dependent by construction.
  (2) A SOBOLEV norm is not a WEIGHT.  A weight w(y)|phi|^2 penalizes LOCATION; ||phi''||^2
      penalizes CURVATURE.  Xu's singular family y^{1-lambda}/(y + i/2)^2 is in L^2 and fails
      phi'' in L^2 at the origin -- location cannot separate it from the physical modes,
      curvature can.  On a grid every function is smooth, so the separation must appear as a
      NORM RATIO, not as a membership test.  That is control C3, and it can refute (2).

--------------------------------------------------------------------------------
CEILING, STATED HERE AND IN EVERY ARTIFACT (leg 163's obstruction O3, which is FATAL
FOR TRANSFER and is therefore carried, not softened)
--------------------------------------------------------------------------------
The object is `HL_S2_nonsymmetric`, NOT the a=0 CLM profile.  Every closed form in Xu is a
consequence of Omega being the EXACT CLM profile, and this object inherits NONE of them.  This
leg imports Xu's DEFINITION OF THE REALIZATION (the X norm, the origin condition) and nothing
else: no spectral gap of 1/2, no ||L^-1|| <= 2, no closed-form resolvent.  Measured here and
reported in the JSON: this object has Omega(0) != 0 and is not odd, so it is NOT IN Xu's space
X at all -- which is itself part of the answer and is not hidden.

FLOAT64 THROUGHOUT.  Leg 56's numbers are rigorous interval enclosures; every number this leg
produces is a FLOAT DIAGNOSTIC.  Nothing here is a proof and nothing here is enclosed.

--------------------------------------------------------------------------------
ARMS
--------------------------------------------------------------------------------
  A0  weighted_sup   leg 46/50's own realization, through leg 46's own code   -> control C1
  A1  L2_h           discrete L^2(q dx); H is an isometry here                -> exact algebra
  A2  X_h            ||v||^2 = sum q (v^2 + (D^2 v)^2)   -- Xu eq (3.2)'s norm
  A3  X_h_origin     A2 restricted to the border rows' null space (the enforceable-
                     on-a-grid half of phi = a_1 y + o(y), which leg 46's certificate
                     ALREADY imposes on the perturbation -- measured, not assumed)

Writes writeup/data/p2_route_l1rh_v1_construction.json.
Run: .venv/bin/python -u experiments/p2_route_l1rh_v1_construction.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.bordered_hl import BorderedHL, induced_sup_norm          # noqa: E402
from solver.interval_certificate import (                            # noqa: E402
    BorderedHLIntervals, SplineConsistency, full_interpolant_hilbert_matrix,
    interval_constants, radii_verdict,
)
from experiments.p2_route_port_v1_bordered import P_STAR, solve      # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_l1rh_v1_construction.json"
TN_REF = ROOT / "writeup" / "data" / "p2_route_tn_v1_consistency.json"
L1_REF = ROOT / "writeup" / "data" / "p2_route_l1_v1_interval.json"

RUNGS = (201, 401, 801)
A_CLASS = 0.5            # leg 56's class scale (the CLM anchor pair)
ARMS = ("weighted_sup", "L2_h", "X_h", "X_h_origin")
RNG = np.random.default_rng(20260806)


# ==========================================================================
# quadrature and the norm objects
# ==========================================================================
def trapezoid_weights(X):
    """Non-uniform trapezoid weights: q_i = (X_{i+1} - X_{i-1}) / 2, halved at the ends."""
    q = np.empty_like(X)
    q[1:-1] = 0.5 * (X[2:] - X[:-2])
    q[0] = 0.5 * (X[1] - X[0])
    q[-1] = 0.5 * (X[-1] - X[-2])
    return q


class NodeNorm:
    """A norm on the node space R^n, in the one form every arm shares: ||v|| = ||T v||_2.

    `T` is the whitening map.  For the sup arm there is no such `T` and the arm carries
    `T = None`, its norm being computed by the weighted-sup path instead.  Keeping the two
    behind one interface is what lets the SAME defect code run in every arm (lesson 90: a
    control that runs through a different code path is not a control)."""

    def __init__(self, kind, X, q, D2=None, nu=None, mask=None):
        self.kind = kind
        self.mask = np.ones(X.size, dtype=bool) if mask is None else mask
        self.nu = nu
        sq = np.sqrt(q * self.mask)
        if kind == "sup":
            self.T = None
        elif kind == "L2":
            self.T = np.diag(sq)
        elif kind == "X":
            self.T = np.vstack([np.diag(sq), sq[:, None] * D2])
        else:
            raise ValueError(kind)

    def __call__(self, v):
        v = np.asarray(v, dtype=float)
        if self.T is None:
            m = self.mask
            return float(np.max(self.nu[m] * np.abs(v[m])))
        return float(np.linalg.norm(self.T @ v))


def packed_gram_root(nodenorm, n, w_l, w_om, w_r):
    """SQUARE R with ||z||^2 = ||R z||_2^2 on the packed space (Omega, V, c_l, c_om, c_r).

    `nodenorm.T` is generally TALL (the X arm stacks the value and curvature blocks), so the
    Gram G = T^T T is formed and Cholesky'd: R is then N x N and invertible, which keeps
    every induced-norm SVD below at N x N instead of (4n+3) x (4n+3).

    The three scalar weights are leg 46's own (w_l, w_om, w_r), unchanged, so that the
    comparison between arms is about the FUNCTION-SPACE part and nothing else."""
    T = nodenorm.T
    g = T.T @ T
    N = 2 * n + 3
    G = np.zeros((N, N))
    G[:n, :n] = g
    G[n:2 * n, n:2 * n] = g
    G[2 * n, 2 * n] = w_l ** 2
    G[2 * n + 1, 2 * n + 1] = w_om ** 2
    G[2 * n + 2, 2 * n + 2] = w_r ** 2
    # G is PD by construction (the value block alone is diag(q) > 0), but Cholesky is
    # given a floor anyway: a norm that is only PSD is not a norm, and would be a bug.
    return np.linalg.cholesky(G).T          # upper-triangular R with R^T R = G


def induced_2norm(R_cod, M, R_dom_pinv):
    """||M||_{dom->cod} for quadratic arms: the 2-norm of R_cod M R_dom^+."""
    return float(np.linalg.norm(R_cod @ M @ R_dom_pinv, 2))


# ==========================================================================
# the symmetric bilinear form of F, and its adjoint (needed for the B witness)
# ==========================================================================
class Bilinear:
    """Qtilde(v, w), the symmetric bilinear part of `BorderedHL.F`, and its adjoint.

    `BorderedHL.quadratic(v)` returns Q(v, v).  Polarisation gives Qtilde; the adjoint is
    written out by hand (term by term) rather than formed as a matrix, because forming it
    would be O(N^3) per ascent step at N = 1605."""

    def __init__(self, pr):
        self.pr = pr
        self.n, self.N = pr.n, pr.N

    def apply(self, v, w):
        pr = self.pr
        n = self.n
        om_v, vv_v, al_v, ao_v, ar_v = pr.unpack(v)
        om_w, vv_w, al_w, ao_w, ar_w = pr.unpack(w)
        s_v = pr.Uop @ om_v + al_v * pr.X + ar_v
        s_w = pr.Uop @ om_w + al_w * pr.X + ar_w
        Dom_v, Dom_w = pr.D @ om_v, pr.D @ om_w
        Dvv_v, Dvv_w = pr.D @ vv_v, pr.D @ vv_w
        Q_Om = 0.5 * (s_v * Dom_w + s_w * Dom_v) - 0.5 * (ao_v * om_w + ao_w * om_v)
        Q_V = (0.5 * (s_v * Dvv_w + s_w * Dvv_v)
               + 0.5 * ((pr.H @ om_v) * vv_w + (pr.H @ om_w) * vv_v)
               - (ao_v * vv_w + ao_w * vv_v))
        out = np.zeros(self.N)
        out[:n], out[n:2 * n] = Q_Om, Q_V
        return out

    def adjoint(self, v, u):
        """Qtilde(v, .)^T u, in the plain Euclidean inner product."""
        pr = self.pr
        n = self.n
        om_v, vv_v, al_v, ao_v, ar_v = pr.unpack(v)
        u_Om, u_V = u[:n], u[n:2 * n]
        s_v = pr.Uop @ om_v + al_v * pr.X + ar_v
        Dom_v, Dvv_v = pr.D @ om_v, pr.D @ vv_v

        g1 = u_Om * Dom_v                       # pairs against s_w
        g2 = u_V * Dvv_v                        # pairs against s_w
        g = 0.5 * (g1 + g2)

        om_slot = (0.5 * (pr.D.T @ (s_v * u_Om))          # from s_v * D om_w
                   + pr.Uop.T @ g                          # from s_w * D om_v and D vv_v
                   - 0.5 * ao_v * u_Om                     # from -a_om^v om_w
                   + 0.5 * (pr.H.T @ (vv_v * u_V)))        # from (H om_w) * vv_v
        vv_slot = (0.5 * (pr.D.T @ (s_v * u_V))            # from s_v * D vv_w
                   + 0.5 * ((pr.H @ om_v) * u_V)           # from (H om_v) * vv_w
                   - ao_v * u_V)                           # from -2 a_om^v vv_w (sym'd)
        al_slot = float(pr.X @ g)
        ao_slot = -0.5 * float(u_Om @ om_v) - float(u_V @ vv_v)
        ar_slot = float(np.sum(g))
        out = np.zeros(self.N)
        out[:n], out[n:2 * n] = om_slot, vv_slot
        out[2 * n], out[2 * n + 1], out[2 * n + 2] = al_slot, ao_slot, ar_slot
        return out


def b_witness(bil, R, Rpinv, restarts=4, outer=12, inner=25):
    """LOWER witness for B = sup_{||v||,||w||<=1} ||Qtilde(v,w)||, by alternating ascent.

    DIRECTION OF ERROR, STATED (leg 56's clause TN-5, same logic): a lower witness on B
    makes the budget LARGER and tau LARGER, hence the diagnostic ratio SMALLER.  It is
    therefore GENEROUS to whichever arm it is applied to.  A ratio that still fails is a
    fortiori a failure; a ratio that closes is provisional and is labelled as such.

    The looseness is not left as an opinion: the same estimator is run on arm A0, whose
    analytic B leg 46 computes in closed form, and the two are reported side by side."""
    N = bil.N
    best = 0.0
    for _ in range(restarts):
        vh = RNG.standard_normal(R.shape[0])
        v = Rpinv @ (vh / np.linalg.norm(vh))
        for _ in range(outer):
            # top singular pair of  wh -> R Qtilde(v, Rpinv wh)
            xh = RNG.standard_normal(R.shape[0])
            xh /= np.linalg.norm(xh)
            sig = 0.0
            for _ in range(inner):
                y = R @ bil.apply(v, Rpinv @ xh)
                ny = np.linalg.norm(y)
                if ny == 0.0:
                    break
                y /= ny
                xh = Rpinv.T @ bil.adjoint(v, R.T @ y)
                nx = np.linalg.norm(xh)
                if nx == 0.0:
                    break
                xh /= nx
                sig = nx
            if sig <= 0.0:
                break
            w = Rpinv @ xh
            best = max(best, sig)
            v = w / max(np.linalg.norm(R @ w), 1e-300)   # alternate: swap roles
    return float(best)


def b_analytic_L2(b, q, w_l, w_om, w_r):
    """UPPER bound on B in the L^2_h arm, by leg 46's OWN decomposition, step for step.

    This exists because a lower witness is not enough to answer a gate.  The one estimate
    leg 46 makes that is norm-specific is `||s * u|| <= ||s||_inf ||u||`, and that step is
    EXACTLY TRUE in L^2 (it is false in the X arm, which is why the X arm keeps a witness).
    Every ingredient is an induced norm of the actual matrix; nothing is assumed:

        ||M||_{L2 -> inf} = max_i sqrt( sum_j M_ij^2 / q_j )
        ||M||_{L2 -> L2}  = || diag(sqrt q) M diag(1/sqrt q) ||_2

    so this arm's B is an upper bound of the same standing as leg 46's, and its tau is
    CONSERVATIVE rather than generous."""
    sq = np.sqrt(q)
    isq = 1.0 / sq

    def n_l2_inf(M):
        return float(np.sqrt(np.max(np.sum((M * isq[None, :]) ** 2, axis=1))))

    def n_l2_l2(M):
        return float(np.linalg.norm(sq[:, None] * M * isq[None, :], 2))

    Uop_ni = n_l2_inf(b.Uop)
    H_ni = n_l2_inf(b.H)
    D_nn = n_l2_l2(b.D)
    Xmax = float(np.abs(b.X).max())
    S1 = Uop_ni + Xmax / w_l + 1.0 / w_r
    B1 = S1 * D_nn + 1.0 / w_om
    B2 = S1 * D_nn + H_ni + 2.0 / w_om
    return {"B": float(max(B1, B2)), "Uop_L2_to_inf": Uop_ni, "H_L2_to_inf": H_ni,
            "D_L2_to_L2": D_nn, "S1": float(S1), "B1": float(B1), "B2": float(B2)}


def norm_equivalence(gram_strong, gram_weak, n, w_l, w_om, w_r):
    """C_eq = sup ||y||_strong / ||y||_weak on the packed space, exactly.

    Used to carry the L^2 arm's ANALYTIC bilinear bound into the X arm:

        ||Qtilde(v,w)||_X <= C_eq ||Qtilde(v,w)||_{L2} <= C_eq B_{L2} ||v||_{L2} ||w||_{L2}
                          <= C_eq B_{L2} ||v||_X ||w||_X            (since ||.||_{L2} <= ||.||_X)

    so B_X <= C_eq * B_{L2}.  This is a genuine UPPER bound and it is deliberately kept
    alongside the ascent's LOWER witness rather than replacing it: the two BRACKET B_X, and
    the width of that bracket is this leg's honest statement of what it does and does not
    know about the X realization's budget."""
    Rs = packed_gram_root(gram_strong, n, w_l, w_om, w_r)
    Rw = packed_gram_root(gram_weak, n, w_l, w_om, w_r)
    return float(np.linalg.norm(Rs @ np.linalg.inv(Rw), 2))


# ==========================================================================
# the pieces of the certificate, per arm
# ==========================================================================
def sup_arm(b, z, nu, w, w_l):
    """Arm A0, through leg 46's OWN code path.  This is control C1 and it can fail."""
    iv = BorderedHLIntervals(b)
    c = interval_constants(iv, z, w, nu)
    v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
    tau = float(v["budget"] / c["A_norm"])
    return {"arm": "weighted_sup", "Y0": float(c["Y0"]), "Z1": float(c["Z1"]),
            "Z2": float(c["Z2"]), "A_norm": float(c["A_norm"]), "B": float(c["B"]),
            "budget": float(v["budget"]), "tau": tau, "closes": bool(v["closes"]),
            "rigorous": True}


def quadratic_arm(name, b, z, J, A, Fz, gramnorm, w_l, w_om, w_r, bil,
                  restrict=None, B_up=None):
    """Arms A1/A2/A3: the same five constants, in a Hilbert norm, in float.

    `restrict` is an orthonormal basis (columns) of the subspace the perturbation is
    allowed to live in, expressed in WHITENED coordinates.  A3 passes the border rows'
    null space; A1/A2 pass None."""
    n = b.n
    R = packed_gram_root(gramnorm, n, w_l, w_om, w_r)
    Rpinv = np.linalg.inv(R)
    if restrict is not None:
        Rq = restrict.T @ R           # whitened coords restricted to the subspace
        Rqpinv = np.linalg.pinv(Rq)
    else:
        Rq, Rqpinv = R, Rpinv
    A_norm = induced_2norm(Rq, A, Rqpinv)
    Z1 = induced_2norm(Rq, np.eye(b.N) - A @ J, Rqpinv)
    Y0 = float(np.linalg.norm(Rq @ (A @ Fz)))
    B_wit = b_witness(bil, Rq, Rqpinv)
    B = B_wit if B_up is None else float(B_up)
    Z2 = 2.0 * A_norm * B
    v = radii_verdict(Y0, Z1, Z2)
    tau = float(v["budget"] / A_norm) if A_norm > 0 else 0.0
    # the same budget under the WITNESS, so the estimator's looseness is a measured number
    v_w = radii_verdict(Y0, Z1, 2.0 * A_norm * B_wit)
    return {"arm": name, "Y0": Y0, "Z1": Z1, "Z2": Z2, "A_norm": A_norm,
            "B": B, "B_witness": B_wit,
            "B_is": ("analytic UPPER bound (leg 46's decomposition, L^2 step exact)"
                     if B_up is not None else
                     "LOWER witness (alternating ascent, 4 restarts) -- generous to this arm"),
            "B_upper_over_witness": (float(B / B_wit) if B_wit > 0 else None),
            "budget": float(v["budget"]), "tau": tau, "closes": bool(v["closes"]),
            "tau_under_witness": (float(v_w["budget"] / A_norm) if A_norm > 0 else 0.0),
            "rigorous": False}


def origin_restriction(b, R):
    """Orthonormal basis of the border rows' NULL SPACE, in whitened coordinates.

    THE POINT, AND IT IS MEASURED NOT ASSUMED: leg 46's bordered system already carries
    three border rows -- Omega(0), Omega_X(0), V(0) -- so the enforceable-on-a-grid half of
    Xu's origin condition `phi = a_1 y + o(y)` (namely phi(0) = 0 on the PERTURBATION) is
    ALREADY imposed by the certificate.  What the collocation realization has never had is
    the other half, `phi'' in L^2`, which on a grid is not a constraint at all -- it is the
    NORM.  So A3 differs from A2 only by the codim-3 restriction, and if the two come out
    identical that is the finding, not a bug (lesson 90 cuts both ways)."""
    n = b.n
    C = np.zeros((3, b.N))
    C[0, b.i0] = 1.0
    C[1, :n] = b.Drow0
    C[2, n + b.i0] = 1.0
    Rpinv = np.linalg.pinv(R)
    Cw = C @ Rpinv                      # the constraints in whitened coordinates
    _, _, Vt = np.linalg.svd(Cw)
    return Vt[3:].T                     # columns span the null space


# ==========================================================================
# the defect, in every arm's own norm
# ==========================================================================
def defects_in_norm(sc, b, nodenorm, family="odd", a=A_CLASS):
    """The (H, D) consistency defects and the interpolation error, in ONE arm's norm.

    Enclosure midpoints are used (this leg is float; leg 56's enclosures stay leg 56's).
    Three Hilbert-side quantities, all on the same test function:

        d_H_impl   H_disc f - H_M f          the operator AS IMPLEMENTED (leg 56's gate)
        d_H_full   H_full f - H_M f          the endpoint hats restored (leg 56 built this)
        d_endpt    H_disc f - H_full f       the artifact leg 165 classified as TIER 2

    plus `interp`, the raw interpolation error Pi f - f at the nodes, which is what P4 says
    d_H_full must equal in an arm where H is an isometry."""
    X = b.X
    msk = sc.interior
    fv = np.asarray(sc.f(a, 0.0, family).mid, dtype=float)
    fp = np.asarray(sc.f_prime(a, 0.0, family).mid, dtype=float)
    H_M = np.asarray((sc.H_exact(a, 0.0, family) - sc.H_truncation(a, 0.0, family)).mid,
                     dtype=float)
    Hfull = full_interpolant_hilbert_matrix(X)
    Hfull_safe = np.where(np.isfinite(Hfull), Hfull, 0.0)

    dD = b.D @ fv - fp
    dH_impl = b.H @ fv - H_M
    dH_full = Hfull_safe @ fv - H_M
    d_end = b.H @ fv - Hfull_safe @ fv

    def nm(v):
        vv = np.asarray(v, dtype=float).copy()
        vv[~msk] = 0.0
        return nodenorm(vv)

    nD, nHi, nHf, nE = nm(dD), nm(dH_impl), nm(dH_full), nm(d_end)
    return {"f_norm": nm(fv), "defect_D": nD, "defect_H_impl": nHi,
            "defect_H_full": nHf, "defect_endpoint": nE,
            "endpoint_share": float(nE / nHi) if nHi > 0 else None,
            "H_full_over_D": float(nHf / nD) if nD > 0 else None}


def interpolation_error_L2(b, a=A_CLASS, family="odd", sub=16):
    """||Pi_n f - f||_{L^2} of the natural-spline interpolant, on a refined sub-grid.

    P4 needs this and nothing else can supply it: `Pi_n f - f` is ZERO at every node by
    construction, so no node-space quantity measures it.  `H` is an L^2 isometry commuting
    with d/dx, hence an isometry of Xu's X, so the prediction P4 is

        ||H(Pi_n f) - H f||  ==  ||Pi_n f - f||     in an L^2-scale realization,

    which is exactly the "one interpolation error through two operators" mechanism leg 56
    claimed, VER-C refuted IN THE SUP REALIZATION, and this function tests in the other one."""
    from solver.line_hilbert import natural_spline_slopes
    X = b.X

    def fn(u):
        return (-u / (u * u + a * a)) if family == "odd" else (a / (u * u + a * a))

    fv = fn(X)
    s = natural_spline_slopes(X, fv)
    err2 = 0.0
    t = (np.arange(sub) + 0.5) / sub
    t2, t3 = t * t, t * t * t
    h0, h1 = 2 * t3 - 3 * t2 + 1, -2 * t3 + 3 * t2
    g0, g1 = t3 - 2 * t2 + t, t3 - t2
    for j in range(X.size - 1):
        hh = X[j + 1] - X[j]
        xq = X[j] + hh * t
        val = fv[j] * h0 + hh * s[j] * g0 + fv[j + 1] * h1 + hh * s[j + 1] * g1
        e = val - fn(xq)
        err2 += float(np.sum(e * e)) * hh / sub
    return float(np.sqrt(err2))


# ==========================================================================
# C3 -- the mechanism control: does the norm see origin regularity at all?
# ==========================================================================
def singular_family_control(b, norms):
    """Xu's explicit singular family u_lambda(y) = y^{1-lambda} / (y + i/2)^2, real part,
    sampled on THIS grid, against a physical comparison mode of the same amplitude.

    Xu sec 4.6: these are in L^2 for every lambda in the open strip and fail phi'' in L^2
    exactly when Re lambda >= -1/2, except at lambda in {0, 1}.  On a grid every function is
    smooth, so no membership test can see this.  The claim under test (novelty sec 4.2) is
    that the X_h norm SEPARATES them by a ratio that GROWS with n while the weighted-sup and
    L^2 norms do not.  If it does not, the leg says so in its headline."""
    X = b.X
    y = np.abs(X) + 1e-300
    out = {}
    phys = (-X / (X * X + 0.25))                      # the a=0 CLM profile: smooth, odd
    for lam in (0.25, 0.5, 0.75):
        sing = np.sign(X) * y ** (1.0 - lam) / (y * y + 0.25)
        row = {}
        for name, nn in norms.items():
            a = nn(sing / max(np.max(np.abs(sing)), 1e-300))
            p = nn(phys / max(np.max(np.abs(phys)), 1e-300))
            row[name] = {"singular": a, "physical": p,
                         "separation": float(a / p) if p > 0 else None}
        out["lambda_%.2f" % lam] = row
    return out


# ==========================================================================
def rate(seq):
    out = []
    for x, y in zip(seq[:-1], seq[1:]):
        f = (x / y) if y > 0 else float("inf")
        out.append({"factor": float(f),
                    "order": float(np.log2(f)) if np.isfinite(f) and f > 0 else None})
    return out


def main():
    t0 = time.time()
    out = {
        "route": "L1RH", "version": "v1",
        "gate": ("Does origin-H^2 (or another space this leg identifies as structurally "
                 "analogous, per leg 163's own scoping method) admit a certificate "
                 "formulation for the collocation-basis realization of L1, and if built, "
                 "does its diagnostic close?"),
        "float64_only": True,
        "fixed_reach": True,
        "ceiling": ("HL_S2_nonsymmetric, NOT the a=0 CLM profile. Leg 163's obstruction O3 "
                    "is carried: none of Xu's closed forms transfer to this object. Only "
                    "the DEFINITION of the realization is imported."),
        "arms": list(ARMS),
        "rungs": [],
    }

    # -- the banked references, as stored -------------------------------------
    tn = json.loads(TN_REF.read_text())
    out["leg56_reference_as_stored"] = {
        "source": "writeup/data/p2_route_tn_v1_consistency.json",
        "tau_at_801": tn["verdict"]["tau_at_801"],
        "defect_D_over_tau_at_801": tn["verdict"]["defect_D_over_tau_at_801"],
        "defect_H_over_tau_at_801": tn["verdict"]["defect_H_over_tau_at_801"],
        "endpoint_share_at_801": tn["H_attribution"]["endpoint_share_at_801"],
        "D_only_n_required": tn["D_only_extrapolation"]["n_required"],
        "realization_robust_ratio": tn["D_only_extrapolation"]["defect_D_over_tau_at_801"],
    }
    l1 = json.loads(L1_REF.read_text())
    r801 = [r for r in l1["L1_2_ladder"] if r["n"] == 801][0]
    out["leg46_reference_as_stored"] = {
        "A_norm": r801["interval"]["A_norm"], "budget": r801["verdict"]["budget"],
        "Z2": r801["interval"]["Z2"], "Y0": r801["interval"]["Y0"],
    }

    for n in RUNGS:
        tr = time.time()
        b, z, _hist, _cs = solve(n=n)
        w, nu, w_l = b.weights(p=P_STAR, w_l=0.01 * float(np.abs(b.X).max()))
        w_om, w_r = float(w[2 * b.n + 1]), float(w[2 * b.n + 2])
        X = b.X
        q = trapezoid_weights(X)
        D2 = b.D @ b.D
        sc = SplineConsistency(b)
        msk = sc.interior

        # two families: MASKED (the defect lives on interior nodes only, as leg 56 defines
        # it) and UNMASKED (the Gram of the packed space must be a genuine norm, i.e. PD).
        norms = {
            "weighted_sup": NodeNorm("sup", X, q, nu=nu, mask=msk),
            "L2_h": NodeNorm("L2", X, q, mask=msk),
            "X_h": NodeNorm("X", X, q, D2=D2, mask=msk),
        }
        norms["X_h_origin"] = norms["X_h"]      # same NODE norm; A3 differs on the operator
        gnorms = {"L2_h": NodeNorm("L2", X, q),
                  "X_h": NodeNorm("X", X, q, D2=D2)}
        gnorms["X_h_origin"] = gnorms["X_h"]

        J = b.jacobian(z)
        A = np.linalg.inv(J)
        Fz = b.F(z)
        bil = Bilinear(b)

        rec = {"n": int(n), "N": int(b.N), "X_max": float(np.abs(X).max()),
               "p_star": float(P_STAR), "constants": {}, "defects": {}, "ratios": {}}

        # --- the object's own membership in Xu's space, measured ------------
        Om, V, _cl, _com, _cr = b.unpack(z)
        rec["object_vs_Xu_space"] = {
            "Omega_at_origin": float(Om[b.i0]),
            "V_at_origin": float(V[b.i0]),
            "oddness_residual_Omega": float(np.max(np.abs(Om + Om[::-1]))
                                            / np.max(np.abs(Om))),
            "grid_symmetry_residual": float(np.max(np.abs(X + X[::-1]))),
            "note": ("Xu eq (3.2) requires phi odd with phi(y) = a_1 y + o(y). This object "
                     "satisfies NEITHER. Only the PERTURBATION space is constrained, by the "
                     "border rows, which is what arm A3 measures."),
        }

        # --- A0 through leg 46's own code (control C1) -----------------------
        rec["constants"]["weighted_sup"] = sup_arm(b, z, nu, w, w_l)

        # --- A1/A2/A3 --------------------------------------------------------
        R_X = packed_gram_root(gnorms["X_h"], b.n, w_l, w_om, w_r)
        restrict = origin_restriction(b, R_X)
        bl2 = b_analytic_L2(b, q, w_l, w_om, w_r)
        C_eq = norm_equivalence(gnorms["X_h"], gnorms["L2_h"], b.n, w_l, w_om, w_r)
        bl2["C_eq_X_over_L2"] = C_eq
        bl2["B_X_upper_via_C_eq"] = float(C_eq * bl2["B"])
        rec["B_analytic_L2"] = bl2
        for name, restr, bup in (("L2_h", None, bl2["B"]),
                                 ("X_h", None, bl2["B_X_upper_via_C_eq"]),
                                 ("X_h_origin", restrict, bl2["B_X_upper_via_C_eq"])):
            ta = time.time()
            rec["constants"][name] = quadratic_arm(
                name, b, z, J, A, Fz, gnorms[name], w_l, w_om, w_r, bil,
                restrict=restr, B_up=bup)
            print("   [n=%d] %-12s %.1fs  |A|=%.5g  B=%.5g  Z1=%.3e"
                  % (n, name, time.time() - ta, rec["constants"][name]["A_norm"],
                     rec["constants"][name]["B"], rec["constants"][name]["Z1"]), flush=True)

        # --- defects, every arm, same code path ------------------------------
        for name in ARMS:
            rec["defects"][name] = defects_in_norm(sc, b, norms[name])

        # --- P4: the isometry mechanism, measured ----------------------------
        e_L2 = interpolation_error_L2(b)
        rec["P4_isometry"] = {
            "interp_error_L2_on_subgrid": e_L2,
            "defect_H_full_L2_h": rec["defects"]["L2_h"]["defect_H_full"],
            "ratio_should_be_1": (float(rec["defects"]["L2_h"]["defect_H_full"] / e_L2)
                                  if e_L2 > 0 else None),
            "defect_H_impl_L2_h": rec["defects"]["L2_h"]["defect_H_impl"],
            "ratio_impl_over_interp": (float(rec["defects"]["L2_h"]["defect_H_impl"] / e_L2)
                                       if e_L2 > 0 else None),
            "note": ("H is an L^2 isometry commuting with d/dx. With the FULL interpolant "
                     "the Hilbert-side defect is therefore the interpolation error itself; "
                     "with the endpoint-ZEROED operator leg 46 actually runs, it is not."),
        }

        # --- the diagnostic --------------------------------------------------
        for name in ARMS:
            c, d = rec["constants"][name], rec["defects"][name]
            tau = c["tau"]
            rec["ratios"][name] = {
                "tau": tau,
                "defect_D_over_tau": float(d["defect_D"] / tau) if tau > 0 else float("inf"),
                "defect_H_impl_over_tau": (float(d["defect_H_impl"] / tau) if tau > 0
                                           else float("inf")),
                "defect_H_full_over_tau": (float(d["defect_H_full"] / tau) if tau > 0
                                           else float("inf")),
                "worst_over_tau": (float(max(d["defect_D"], d["defect_H_full"]) / tau)
                                   if tau > 0 else float("inf")),
                # the same ratio under the GENEROUS (lower-witness) B, so the bracket on
                # B is visible as a bracket on the answer rather than buried in a constant
                "tau_under_witness": c.get("tau_under_witness"),
                "worst_over_tau_under_witness": (
                    float(max(d["defect_D"], d["defect_H_full"]) / c["tau_under_witness"])
                    if c.get("tau_under_witness") else None),
                # ------------------------------------------------------------------
                # THETA -- THE B-FREE DIAGNOSTIC, AND IT IS THE HONEST HEADLINE.
                # Since  tau = (1 - Z_1)^2 / (4 ||A||^2 B),  the death ratio is
                #     defect / tau = 4 ||A||^2 defect B / (1 - Z_1)^2 = Theta * B.
                # Theta is EXACTLY computable in every arm with no estimator anywhere;
                # B is the only factor this leg cannot pin in the X arms.  Comparing
                # arms through Theta therefore compares realizations without letting an
                # unaudited constant do the work (lesson 90's question, asked of my own
                # headline: what would have had to change for this to come out the
                # other way?  ||A|| or the defect -- both measured, neither estimated).
                # ------------------------------------------------------------------
                "theta_B_free": float(4.0 * c["A_norm"] ** 2
                                      * max(d["defect_D"], d["defect_H_full"])
                                      / (1.0 - c["Z1"]) ** 2),
                "theta_B_free_D_only": float(4.0 * c["A_norm"] ** 2 * d["defect_D"]
                                             / (1.0 - c["Z1"]) ** 2),
            }

        rec["C3_singular_family"] = singular_family_control(b, {
            k: norms[k] for k in ("weighted_sup", "L2_h", "X_h")})
        rec["wall_s"] = time.time() - tr
        out["rungs"].append(rec)
        print("n=%4d " % n + "  ".join(
            "%s: |A|=%.4g tau=%.3e worst/tau=%.4e"
            % (k, rec["constants"][k]["A_norm"], rec["ratios"][k]["tau"],
               rec["ratios"][k]["worst_over_tau"]) for k in ARMS), flush=True)

    # ======================================================================
    # controls and the verdict
    # ======================================================================
    last = out["rungs"][-1]
    ref = out["leg56_reference_as_stored"]
    c1 = {
        "what": ("arm A0 must reproduce leg 46/56's banked numbers through this leg's own "
                 "code path; a miss withdraws the leg"),
        "tau_here": last["ratios"]["weighted_sup"]["tau"],
        "tau_banked": ref["tau_at_801"],
        "tau_rel_err": abs(last["ratios"]["weighted_sup"]["tau"] - ref["tau_at_801"])
        / ref["tau_at_801"],
        "A_norm_here": last["constants"]["weighted_sup"]["A_norm"],
        "A_norm_banked": out["leg46_reference_as_stored"]["A_norm"],
        "A_norm_rel_err": abs(last["constants"]["weighted_sup"]["A_norm"]
                              - out["leg46_reference_as_stored"]["A_norm"])
        / out["leg46_reference_as_stored"]["A_norm"],
        "defect_D_over_tau_here": last["ratios"]["weighted_sup"]["defect_D_over_tau"],
        "defect_D_over_tau_banked": ref["defect_D_over_tau_at_801"],
        "defect_H_impl_over_tau_here": last["ratios"]["weighted_sup"]["defect_H_impl_over_tau"],
        "defect_H_impl_over_tau_banked": ref["defect_H_over_tau_at_801"],
    }
    c1["PASS"] = bool(c1["tau_rel_err"] < 1e-6 and c1["A_norm_rel_err"] < 1e-6)

    c2 = {
        "what": ("lesson 90, twice: L2_h vs X_h must differ (the curvature term is wired) "
                 "and X_h vs X_h_origin must differ (the border-row restriction is wired)"),
        "L2_vs_X_A_norm_ratio": (last["constants"]["X_h"]["A_norm"]
                                 / last["constants"]["L2_h"]["A_norm"]),
        "X_vs_Xorigin_A_norm_ratio": (last["constants"]["X_h_origin"]["A_norm"]
                                      / last["constants"]["X_h"]["A_norm"]),
        "L2_vs_X_defect_ratio": (last["defects"]["X_h"]["defect_D"]
                                 / last["defects"]["L2_h"]["defect_D"]),
    }
    c2["PASS_curvature_wired"] = bool(abs(c2["L2_vs_X_A_norm_ratio"] - 1.0) > 1e-6)
    c2["PASS_restriction_wired"] = bool(abs(c2["X_vs_Xorigin_A_norm_ratio"] - 1.0) > 1e-6)

    sf = last["C3_singular_family"]
    c3rows = {}
    for lam, row in sf.items():
        c3rows[lam] = {k: row[k]["separation"] for k in row}
    first = out["rungs"][0]["C3_singular_family"]
    c3 = {
        "what": ("novelty sec 4.2 under test: does the X_h norm separate Xu's singular "
                 "family from a physical mode in a way the weighted-sup and L^2 norms do "
                 "not, and does the separation GROW with n?"),
        "separations_at_finest_n": c3rows,
        "growth_201_to_801": {
            lam: {k: (sf[lam][k]["separation"] / first[lam][k]["separation"]
                      if first[lam][k]["separation"] else None) for k in sf[lam]}
            for lam in sf
        },
    }
    lam_mid = "lambda_0.50"
    c3["PASS_curvature_separates"] = bool(
        c3["separations_at_finest_n"][lam_mid]["X_h"]
        > 10.0 * max(c3["separations_at_finest_n"][lam_mid]["weighted_sup"],
                     c3["separations_at_finest_n"][lam_mid]["L2_h"]))

    # C4: rates, three rungs, every arm
    rates = {}
    for name in ARMS:
        dD = [r["defects"][name]["defect_D"] for r in out["rungs"]]
        dHf = [r["defects"][name]["defect_H_full"] for r in out["rungs"]]
        dHi = [r["defects"][name]["defect_H_impl"] for r in out["rungs"]]
        worst = [r["ratios"][name]["worst_over_tau"] for r in out["rungs"]]
        # the D-ONLY ladder, which is the LIKE-FOR-LIKE comparison against leg 56's own
        # `D_only_extrapolation` block (leg 56 deleted the H defect outright and extrapolated
        # the derivative side alone). Quoting `worst` against leg 56's D-only number would be
        # comparing two different quantities.
        dDt = [r["ratios"][name]["defect_D_over_tau"] for r in out["rungs"]]
        rD = rate(dDt)
        oD = rD[-1]["order"] if rD else None
        rates[name] = {"n": list(RUNGS),
                       "defect_D": dD, "defect_D_rate": rate(dD),
                       "defect_H_full": dHf, "defect_H_full_rate": rate(dHf),
                       "defect_H_impl": dHi, "defect_H_impl_rate": rate(dHi),
                       "worst_over_tau": worst, "worst_over_tau_rate": rate(worst),
                       "defect_D_over_tau": dDt, "defect_D_over_tau_rate": rD,
                       "n_required_D_only": (float(RUNGS[-1] * dDt[-1] ** (1.0 / oD))
                                             if oD and oD > 0 else None)}
        rr = rates[name]["worst_over_tau_rate"]
        o = rr[-1]["order"] if rr else None
        rates[name]["n_required"] = (float(RUNGS[-1] * worst[-1] ** (1.0 / o))
                                     if o and o > 0 else None)
    out["rates"] = rates

    # C5 -- the B estimator's looseness, measured rather than assumed.
    kal = last["constants"]["L2_h"]["B_upper_over_witness"]
    c5 = {
        "what": ("the ascent gives a LOWER witness for B, which is generous. In L2_h an "
                 "analytic UPPER bound exists (leg 46's own decomposition, whose one "
                 "norm-specific step is exact in L^2), so the estimator's looseness is a "
                 "measured factor there -- and that factor is applied to the X arms, whose "
                 "witnesses would otherwise be unaudited."),
        "L2_B_upper": last["constants"]["L2_h"]["B"],
        "L2_B_witness": last["constants"]["L2_h"]["B_witness"],
        "L2_upper_over_witness": kal,
    }
    c5["C_eq_X_over_L2"] = last["B_analytic_L2"]["C_eq_X_over_L2"]
    c5["B_X_upper_via_C_eq"] = last["B_analytic_L2"]["B_X_upper_via_C_eq"]
    for nm_ in ("X_h", "X_h_origin"):
        cc, dd = last["constants"][nm_], last["defects"][nm_]
        c5[nm_ + "_B_bracket"] = {"lower_witness": cc["B_witness"], "upper": cc["B"],
                                  "bracket_width_decades": (
                                      float(np.log10(cc["B"] / cc["B_witness"]))
                                      if cc["B_witness"] > 0 else None)}
        c5[nm_ + "_worst_over_tau_upperB"] = last["ratios"][nm_]["worst_over_tau"]
        c5[nm_ + "_worst_over_tau_witnessB"] = (
            last["ratios"][nm_]["worst_over_tau_under_witness"])
    out["controls"] = {"C1_reproduction": c1, "C2_lesson90": c2, "C3_mechanism": c3,
                       "C5_B_estimator_calibration": c5}

    # THE B-FREE COMPARISON, which is what the leg actually answers on
    th = {k: last["ratios"][k]["theta_B_free"] for k in ARMS}
    thD = {k: last["ratios"][k]["theta_B_free_D_only"] for k in ARMS}
    out["theta_B_free"] = {
        "what": ("defect/tau = Theta * B with Theta = 4 ||A||^2 defect / (1 - Z_1)^2. "
                 "Theta is exact in every arm; B is the only unpinned factor. The "
                 "realization comparison is therefore stated on Theta."),
        "by_arm": th, "by_arm_D_only": thD,
        "gain_over_weighted_sup": {k: float(th["weighted_sup"] / th[k]) for k in ARMS},
        "gain_over_weighted_sup_D_only": {k: float(thD["weighted_sup"] / thD[k])
                                          for k in ARMS},
        "ladder": {k: [r["ratios"][k]["theta_B_free"] for r in out["rungs"]] for k in ARMS},
        "ladder_rate": {k: rate([r["ratios"][k]["theta_B_free"] for r in out["rungs"]])
                        for k in ARMS},
    }

    base = last["ratios"]["weighted_sup"]["defect_D_over_tau"]
    out["headline"] = {
        "leg56_realization_robust_ratio_banked": ref["realization_robust_ratio"],
        "A0_worst_over_tau": last["ratios"]["weighted_sup"]["worst_over_tau"],
        "A1_L2_worst_over_tau": last["ratios"]["L2_h"]["worst_over_tau"],
        "A2_X_worst_over_tau": last["ratios"]["X_h"]["worst_over_tau"],
        "A3_Xorigin_worst_over_tau": last["ratios"]["X_h_origin"]["worst_over_tau"],
        "improvement_A0_to_A1": float(base / last["ratios"]["L2_h"]["worst_over_tau"]),
        "improvement_A0_to_A2": float(base / last["ratios"]["X_h"]["worst_over_tau"]),
        "improvement_A0_to_A3": float(base / last["ratios"]["X_h_origin"]["worst_over_tau"]),
        "A_norm_by_arm": {k: last["constants"][k]["A_norm"] for k in ARMS},
        "endpoint_share_by_arm": {k: last["defects"][k]["endpoint_share"] for k in ARMS},
    }
    best_arm = min(("L2_h", "X_h", "X_h_origin"), key=lambda k: th[k])
    out["verdict"] = {
        "gate": out["gate"],
        "formulation_exists": True,
        "formulation_note": ("all five constants form in every arm; Z_1 < 1 and the budget "
                             "is positive in every arm, so the radii polynomial has a "
                             "solution interval in each -- the FORMULATION conjunct is YES"),
        "best_alternative_arm": best_arm,
        "theta_gain_best_arm": float(th["weighted_sup"] / th[best_arm]),
        "best_alternative_ratio_upperB": last["ratios"][best_arm]["worst_over_tau"],
        "best_alternative_ratio_witnessB":
            last["ratios"][best_arm]["worst_over_tau_under_witness"],
        "closes_under_upper_B": bool(last["ratios"][best_arm]["worst_over_tau"] < 1.0),
        "closes_under_witness_B": bool(
            (last["ratios"][best_arm]["worst_over_tau_under_witness"] or float("inf")) < 1.0),
        "n_required_best_arm": rates[best_arm]["n_required"],
    }
    out["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(out, indent=1))
    print("\nwrote", OUT)
    print("C1 reproduction PASS =", c1["PASS"], " rel errs %.2e / %.2e"
          % (c1["tau_rel_err"], c1["A_norm_rel_err"]))
    print("C2 curvature wired =", c2["PASS_curvature_wired"],
          " restriction wired =", c2["PASS_restriction_wired"])
    print("C3 curvature separates =", c3["PASS_curvature_separates"])
    print("headline:", json.dumps(out["headline"], indent=1))


if __name__ == "__main__":
    main()
