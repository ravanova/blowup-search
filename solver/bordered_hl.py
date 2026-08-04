"""The BORDERED steady system for the 1D Hou-Luo non-symmetric positive profile.

Route-PORT, step one. Target object `HL_S2_nonsymmetric` (Route-M's named target):
the strictly positive, regular, NON-SYMMETRIC self-similar profile of the 1D Hou-Luo
model, Chen-Huang-Li arXiv:2604.01868 sec 2.5 / sec 4. Reported April 2026 as a
"previously unreported blowup phenomenon", NUMERICAL ONLY -- no proof, computer-assisted
or otherwise (`solver/target_selection.py`, `LITERATURE_CHECK.md` seventh pass).

WHAT IS BORDERED, AND WHY IT HAS TO BE FROM THE START
-----------------------------------------------------
CHL's modified rescaling (4.1), evolving V := Theta_X, has a STEADY form

    (U + c_l X + c_r) Omega_X = c_omega Omega + V                      (n equations)
    (U + c_l X + c_r) V_X     = (2 c_omega - U_X) V                    (n equations)
    U_X = H(Omega),  U(0) = 0

with THREE unknown constants. The system carries exactly three continuous gauge
freedoms, which is why there are three constants and not two:

    amplitude   (Omega, V, c) -> (mu Omega, mu^2 V, mu c)     [c_l/c_omega invariant]
    dilation    X -> lambda X                                  [absorbed by c_l]
    translation X -> X + s                                     [absorbed by c_r]

So the object is a 3-parameter family of solutions and the square system is
(2n equations) + (2n + 3 unknowns): three short. The three missing equations are
CHL's normalization (4.2), which in the STEADY setting is not a gauge to be solved
for after the fact but three BORDER ROWS pinning the origin values:

    Omega(0) = om0*,   Omega_X(0) = omx0*,   V(0) = v0*.

Leg 44 (L-7) is why this module exists in this shape: it tried the other order on
the 2D object -- solve, then project the constants -- and Newton accepted no step at
all, lambda down to 1/1024. Here the constants are unknowns of the SAME Newton
system from the first iterate.

WHAT THE RELAXATION COULD NOT DO
--------------------------------
`solver/hl_rescaled.py::RescaledHLScenario2` time-steps the same equations with the
same origin gauge, and it FLOORS at residual ~1e-2 (its own leg said so in advance:
`experiments/p2_scenario2_relax.py`, clause S5). The far-field is why: the steady
equation forces the ALGEBRAIC tail Omega ~ |X|^(c_omega/c_l) ~ |X|^-0.4, and a
relaxation started from compactly-decaying data has to transport that tail outward
across a domain reaching |X| ~ 745. Newton does not transport anything; it solves.
That is the entire reason a defect Y_0 is available here and was not available in
Route-K (sec 32: "no fixed profile to take a defect of").

STRUCTURAL FACT THIS MODULE EXPLOITS -- F IS EXACTLY QUADRATIC
--------------------------------------------------------------
Every term of F is degree <= 2 in the packed unknown z = (Omega, V, c_l, c_omega, c_r):
U is LINEAR in Omega (U = Uop @ Omega), and each equation multiplies two unknowns and
no more. Therefore

    F(z + v) = F(z) + DF(z) v + Q(v, v)     EXACTLY, no remainder,

so the second derivative is CONSTANT and the radii-polynomial Z_2 is not a
ball-radius-dependent estimate but an exact bilinear operator norm. `quadratic()`
returns Q(v,v) and `test_bordered_hl.py` gates the identity above to machine
precision -- a known-answer test of the Jacobian that needs no finite differences.

NORMS ARE NAMED, NOT ASSUMED (standing discipline: "small in WHICH norm?")
--------------------------------------------------------------------------
All certificate constants are computed in the weighted sup norm

    ||z|| = max( max_j nu_j |Omega_j|,  max_j nu_j |V_j|,
                 w_l |c_l|, w_om |c_omega|, w_r |c_r| ),      nu_j = (1 + X_j^2)^(p/2)

with the scalar weights defaulting to w_l = max|X| (so that the c_l X term of the
residual is O(1) at unit norm), w_om = w_r = 1. The decay exponent p is a FREE
PARAMETER and `constants_vs_weight` sweeps it, because which p closes the radii
polynomial is exactly the question Directive 3 ("evolve the certificate") is meant
to search -- so it is reported as a curve, not a point.
"""

import numpy as np

from solver.line_hilbert import line_hilbert_matrix, slope_matrix
from solver.hl_rescaled import sinh_grid_origin

CHL_RATIO = -2.5114          # Chen-Huang-Li Fig 4.2, c_l/c_omega (normalization-free)
CHL_TRIPLE = (1.0636, -0.4235, 0.0765)   # their raw triple; OUR normalization differs


# --------------------------------------------------------------------------
# the velocity operator as a matrix
# --------------------------------------------------------------------------
def velocity_matrix(X, i0):
    """Dense W with U = W @ H(Omega): trapezoidal antiderivative pinned to U(0) = 0.

    Same quadrature as `hl_rescaled.velocity`, written as a matrix because the
    bordered Jacobian needs dU/dOmega. The pin is exact rather than interpolated
    because X[i0] = 0 is a node of the origin-clustered grid."""
    X = np.asarray(X, dtype=float)
    n = X.size
    dx = np.diff(X)
    W = np.zeros((n, n))
    for k in range(1, n):
        W[k] = W[k - 1]
        W[k, k - 1] += 0.5 * dx[k - 1]
        W[k, k] += 0.5 * dx[k - 1]
    return W - W[i0][None, :]


# --------------------------------------------------------------------------
# weighted sup norms
# --------------------------------------------------------------------------
def induced_sup_norm(M, w_row, w_col):
    """Induced norm of M as a map (weighted sup, weights w_col) -> (ditto, w_row).

    For ||z||_w = max_i w_i |z_i| the induced norm is the weighted max row sum
    max_i w_i sum_j |M_ij| / w_j. Scalars broadcast, so w_row=None means the
    unweighted sup norm on the codomain."""
    M = np.asarray(M, dtype=float)
    w_row = np.ones(M.shape[0]) if w_row is None else np.broadcast_to(
        np.asarray(w_row, dtype=float), (M.shape[0],))
    w_col = np.broadcast_to(np.asarray(w_col, dtype=float), (M.shape[1],))
    return float(np.max(w_row * (np.abs(M) @ (1.0 / w_col))))


class BorderedHL:
    """The bordered residual F, its exact Jacobian, and the float certificate.

    Unknown vector z = concat(Omega [n], V [n], c_l, c_omega, c_r), size N = 2n+3.
    Residual  F(z) = concat(R_Omega [n], R_V [n], G [3]), same size.

    The three border rows G pin (Omega(0), Omega_X(0), V(0)) to targets supplied at
    construction time (`pin`); those are CHL (4.2)'s three conditions read as
    equations rather than as a gauge solve.
    """

    def __init__(self, n=601, c=0.5, rho_max=8.0, pin=None):
        rho, X = sinh_grid_origin(n, c=c, rho_max=rho_max)
        self.rho = rho
        self.X = X
        self.n = X.size
        self.N = 2 * self.n + 3
        self.i0 = self.n // 2
        if abs(self.X[self.i0]) > 1e-12:
            raise ValueError("origin is not a node")
        self.H = line_hilbert_matrix(X)
        self.D = slope_matrix(X)
        self.Uop = velocity_matrix(X, self.i0) @ self.H
        self.Drow0 = self.D[self.i0].copy()      # the Omega_X(0) border row
        self.pin = None if pin is None else tuple(float(t) for t in pin)

    # -- packing -----------------------------------------------------------
    def pack(self, Omega, V, c_l, c_omega, c_r):
        return np.concatenate([Omega, V, [c_l, c_omega, c_r]])

    def unpack(self, z):
        n = self.n
        return z[:n], z[n:2 * n], float(z[2 * n]), float(z[2 * n + 1]), float(z[2 * n + 2])

    def set_pin_from(self, z):
        """Take the three border targets from a state (usually the relaxation's
        output, whose origin values (4.2) held fixed by construction)."""
        Omega, V, _, _, _ = self.unpack(z)
        self.pin = (float(Omega[self.i0]), float(self.Drow0 @ Omega), float(V[self.i0]))
        return self.pin

    # -- residual ----------------------------------------------------------
    def F(self, z):
        Omega, V, c_l, c_omega, c_r = self.unpack(z)
        HOm = self.H @ Omega
        U = self.Uop @ Omega
        S = U + c_l * self.X + c_r
        R_Om = S * (self.D @ Omega) - c_omega * Omega - V
        R_V = S * (self.D @ V) - (2.0 * c_omega - HOm) * V
        if self.pin is None:
            raise ValueError("border targets not set; call set_pin_from() first")
        G = np.array([Omega[self.i0] - self.pin[0],
                      self.Drow0 @ Omega - self.pin[1],
                      V[self.i0] - self.pin[2]])
        return np.concatenate([R_Om, R_V, G])

    def jacobian(self, z):
        """Exact analytic DF(z). Dense (N x N); the Hilbert block is dense anyway."""
        n = self.n
        Omega, V, c_l, c_omega, c_r = self.unpack(z)
        HOm = self.H @ Omega
        U = self.Uop @ Omega
        S = U + c_l * self.X + c_r
        Om_X = self.D @ Omega
        V_X = self.D @ V
        J = np.zeros((self.N, self.N))
        # R_Omega rows
        J[:n, :n] = Om_X[:, None] * self.Uop + S[:, None] * self.D
        J[:n, :n] -= c_omega * np.eye(n)
        J[:n, n:2 * n] = -np.eye(n)
        J[:n, 2 * n] = self.X * Om_X
        J[:n, 2 * n + 1] = -Omega
        J[:n, 2 * n + 2] = Om_X
        # R_V rows
        J[n:2 * n, :n] = V_X[:, None] * self.Uop + V[:, None] * self.H
        J[n:2 * n, n:2 * n] = S[:, None] * self.D
        J[n:2 * n, n:2 * n] -= np.diag(2.0 * c_omega - HOm)
        J[n:2 * n, 2 * n] = self.X * V_X
        J[n:2 * n, 2 * n + 1] = -2.0 * V
        J[n:2 * n, 2 * n + 2] = V_X
        # border rows
        J[2 * n, self.i0] = 1.0
        J[2 * n + 1, :n] = self.Drow0
        J[2 * n + 2, n + self.i0] = 1.0
        return J

    def quadratic(self, v):
        """Q(v, v), the EXACT remainder F(z+v) - F(z) - DF(z) v (independent of z).

        F is degree-2 in z, so this is the whole nonlinearity. Border rows are
        linear and contribute zero."""
        om, vv, a_l, a_om, a_r = self.unpack(v)
        s = self.Uop @ om + a_l * self.X + a_r
        Q_Om = s * (self.D @ om) - a_om * om
        Q_V = s * (self.D @ vv) + (self.H @ om) * vv - 2.0 * a_om * vv
        return np.concatenate([Q_Om, Q_V, np.zeros(3)])

    # -- Newton ------------------------------------------------------------
    def newton(self, z0, tol=1e-12, max_iter=40, damping=True, verbose=False):
        """Damped Newton on the bordered system. Returns (z, history dict).

        Damping is a plain backtracking line search on ||F||_inf; on this object
        it is used only for the first two or three iterates, and the ladder is
        reported in full because the SHAPE of a convergence ladder is the evidence
        (standing discipline 72), not its endpoint."""
        z = np.array(z0, dtype=float)
        res = [float(np.abs(self.F(z)).max())]
        lam_hist, cond_hist = [], []
        for _ in range(max_iter):
            Fz = self.F(z)
            J = self.jacobian(z)
            try:
                dz = np.linalg.solve(J, -Fz)
            except np.linalg.LinAlgError:
                break
            lam = 1.0
            r0 = float(np.abs(Fz).max())
            if damping:
                while lam > 1.0 / 1024:
                    if float(np.abs(self.F(z + lam * dz)).max()) < r0:
                        break
                    lam *= 0.5
            z = z + lam * dz
            r = float(np.abs(self.F(z)).max())
            res.append(r)
            lam_hist.append(lam)
            if verbose:
                print(f"    newton  lam={lam:6.4f}  ||F||_inf={r:.3e}", flush=True)
            if r < tol:
                break
            if not np.isfinite(r) or r > 1e12:
                break
        return z, {"residual_ladder": np.array(res), "lambda": np.array(lam_hist),
                   "cond": np.array(cond_hist),
                   "converged": bool(res[-1] < tol and np.isfinite(res[-1]))}

    # -- weights and certificate constants ---------------------------------
    def weights(self, p=0.0, w_l=None, w_om=1.0, w_r=1.0):
        """Domain/codomain weight vector for the norm named in the module docstring."""
        nu = (1.0 + self.X ** 2) ** (0.5 * p)
        if w_l is None:
            w_l = float(np.abs(self.X).max())
        return np.concatenate([nu, nu, [w_l, w_om, w_r]]), nu, float(w_l)

    def certificate_constants(self, z, p=0.0, w_l=None, w_om=1.0, w_r=1.0, A=None):
        """(Y_0, Z_1, Z_2) in float, in the weighted sup norm, at the state z.

        A is the approximate inverse; default A = DF(z)^-1 computed in float64, which
        is what "the float rehearsal" means -- Z_1 then measures the CONDITIONING of
        the bordered Jacobian and NOT a truncation tail. Said plainly in the writeup:
        this is a rehearsal, not a proof (the same boundary Route-D v16 drew).

        Z_2 is EXACT rather than estimated, because F is exactly quadratic:
            Z_2 = 2 ||A|| * B,   B = sup_{||v||,||w||<=1} ||Qtilde(v,w)||
        with Qtilde the symmetric bilinear form of `quadratic`. B is bounded from the
        weighted operator norms of Uop, D and H -- every one of them measured on the
        actual matrix, none assumed.
        """
        w, nu, w_l = self.weights(p=p, w_l=w_l, w_om=w_om, w_r=w_r)
        J = self.jacobian(z)
        if A is None:
            A = np.linalg.inv(J)
        Fz = self.F(z)

        Y0 = float(np.max(w * np.abs(A @ Fz)))
        Z1 = induced_sup_norm(np.eye(self.N) - A @ J, w, w)

        # the bilinear bound
        Uop_ni = induced_sup_norm(self.Uop, None, nu)     # nu-weighted -> plain sup
        H_ni = induced_sup_norm(self.H, None, nu)
        D_nn = induced_sup_norm(self.D, nu, nu)
        Xmax = float(np.abs(self.X).max())
        S1 = Uop_ni + Xmax / w_l + 1.0 / w_r
        B1 = S1 * D_nn + 1.0 / w_om
        B2 = S1 * D_nn + H_ni + 2.0 / w_om
        B = max(B1, B2)
        A_norm = induced_sup_norm(A, w, w)
        Z2 = 2.0 * A_norm * B
        return {"Y0": Y0, "Z1": Z1, "Z2": Z2, "p": float(p),
                "A_norm": A_norm, "B": B, "Uop_norm": Uop_ni, "H_norm": H_ni,
                "D_norm": D_nn, "w_l": w_l, "Xmax": Xmax}

    def constants_vs_weight(self, z, ps, **kw):
        """The constants as a function of the decay exponent p -- reported as a
        curve because 'which space closes it' is Directive 3's search variable."""
        J = self.jacobian(z)
        A = np.linalg.inv(J)             # p-independent; invert once
        return [self.certificate_constants(z, p=p, A=A, **kw) for p in ps]


# --------------------------------------------------------------------------
# diagnostics on a converged profile
# --------------------------------------------------------------------------
def tail_exponent(X, f, x_lo, x_hi):
    """Least-squares slope of log|f| vs log|X| over x_lo <= X <= x_hi (X > 0 side).

    The steady equation forces Omega ~ |X|^(c_omega/c_l) and V ~ |X|^(2 c_omega/c_l)
    in the far field, so this is an INTERNAL known-answer check: the measured tail
    exponent must reproduce the ratio the border rows never saw."""
    X = np.asarray(X, dtype=float)
    f = np.asarray(f, dtype=float)
    m = (X >= x_lo) & (X <= x_hi) & (np.abs(f) > 0)
    if m.sum() < 4:
        return float("nan")
    lx, lf = np.log(X[m]), np.log(np.abs(f[m]))
    return float(np.polyfit(lx, lf, 1)[0])


def profile_shape(X, Omega, V):
    """Non-symmetry / regularity descriptors of a converged profile."""
    X = np.asarray(X, dtype=float)
    k = int(np.argmax(Omega))
    peak = float(Omega[k])
    return {"X_peak": float(X[k]), "Omega_peak": peak,
            "Omega_min": float(Omega.min()), "V_min": float(V.min()),
            "positive": bool(Omega.min() > 0 and V.min() > 0),
            "asymmetry": float(np.abs(Omega - Omega[::-1]).max() / max(peak, 1e-300))}
