"""Route-C-PILOT: SEARCH the certificate's function space, on a known-answer object.

WHAT THIS MODULE IS FOR
-----------------------------------------------------------------------------
Leg 46 found, by accident, that whether a radii polynomial closes is a property of
the SPACE and not of the object: the tuned and naive weights on the same bordered
system differed in ONE constant and in whether the certificate existed at all
(5186x in `Y_0/budget` at n=201).  Route-D then hand-tuned a function space for
eleven legs; Routes K and L hand-picked preconditioners.  Those are search problems
being run by hand.

This module makes that search a MEASUREMENT rather than a habit:

    fitness(weight)  =  log10( Y_0 / budget ),     budget = (1 - Z_1)^2 / (2 Z_2)

one number, negative exactly when the certificate closes.  Everything else here
exists to answer the prior question -- IS THAT FITNESS SAFE TO OPTIMIZE? -- because
Stage 3.5 is the precedent: a fitness that fails the six-property viability gate
produces confident garbage at scale, and `plan_of_record.py` bans GA compute until
the gate reports.

WHY THE SUBSTRATE IS CLM AND NOT CHEN-HOU'S 2D PROFILE
-----------------------------------------------------------------------------
The plan named Chen-Hou's certified 2D Boussinesq profile as the known-answer
substrate.  IT CANNOT SUPPLY THIS FITNESS, and the reason is already in this
project's own record: the 2D relaxation limit-cycles and its residual GROWS under
refinement (Route-K, sec 32; `plan_of_record` bans re-measuring beta on it), so
there is no fixed profile to take a defect of, and `port_certification.
radii_polynomial_status` returns BLOCKED_AT_STEP_ONE by design.  A fitness whose
Y_0 does not exist cannot be validated.

The a=0 CLM profile does supply it, and supplies MORE known answers than the 2D
object would have:

  K1  The exact continuum profile is closed form -- Omega_0(X) = -4X/(1+4X^2), with
      H Omega_0 = 2/(1+4X^2) (CLM 1985; HQW25 arXiv:2401.14615).  It nulls the
      continuum residual identically, so every defect measured here is OURS.
  K2  Two convergence ladders with two different knobs, and both have the right
      sign: the discrete Newton profile approaches Omega_0 as the grid is refined,
      and the recovered gauge constant c_omega approaches its exact value -1 as the
      domain reach grows (the far field is where the truncated Hilbert transform
      loses it, and refining spacing does NOT fix that -- measured, see the tests).
  K3  An ANALYTIC WALL on the search space.  Omega_0 ~ -1/X, so a weight
      nu ~ |X|^(p+q) gives the TRUE profile an infinite weighted sup norm as soon as
      p + q > 1.  p* = 1 exactly, derived and not fitted -- and the pilot's sharpest
      question is whether the fitness can SEE that wall (it cannot; see below).
  K4  An exact gauge invariance of the fitness itself, proved below and gated to
      machine precision in `test_weight_search.py`.

THE GAUGE INVARIANCE (a known answer about the fitness, not about the object)
-----------------------------------------------------------------------------
Scale every weight by one constant s -- nu -> s nu, w_l -> s w_l, w_om -> s w_om.
Then Y_0 -> s Y_0 (it is a weighted sup of a fixed vector), Z_1 is unchanged (an
induced norm with the same weight on both sides), and Z_2 -> Z_2 / s (its bilinear
bound B carries exactly one inverse power of the weight).  So

    budget -> s * budget      and      Y_0 / budget  IS INVARIANT.

The fitness therefore lives on a quotient: the overall scale of the norm is a gauge,
not a search direction.  That kills one degeneracy for free -- a searcher cannot win
by making the norm big -- and it is why `w_om = 1` is FIXED here rather than searched.

NORMS ARE NAMED (standing discipline)
-----------------------------------------------------------------------------
All constants are computed in the weighted sup norm on z = (Omega, c_l, c_omega):

    ||z|| = max( max_j nu_j |Omega_j|,  w_l |c_l|,  w_om |c_omega| )

with the SAME weight vector used on the codomain (the convention `bordered_hl.py`
already uses, so the two modules' numbers are comparable).  The searched weight
family is a product of two algebraic factors -- the discrete cousin of Chen-Hou's
own "weight consisting of different powers" (arXiv:2210.07191 sec 5.3.3):

    nu(X) = (1 + (X/L)^2)^(p/2) * (1 + (X/l)^2)^(q/2)

so the genome is theta = (p, log10 L, q, log10 l, log10 w_l), five genes, with the
far-field power p + q the quantity the analytic wall K3 constrains.

WHAT IS EXACT HERE AND WHAT IS FLOAT
-----------------------------------------------------------------------------
F is exactly quadratic in z -- every term multiplies two unknowns and no more -- so
F(z+v) = F(z) + DF(z)v + Q(v,v) with NO remainder, and Z_2 is an exact bilinear
operator norm rather than a ball-radius estimate.  `quadratic()` returns Q and the
identity is gated to machine precision.  Everything else is float64: A = DF^-1 in
float, so Z_1 measures CONDITIONING and not a truncation tail.  This is a rehearsal
of a certificate, not a certificate -- the same boundary Route-D v16 drew and leg 46
restated.  The pilot's claim is about the FITNESS, not about CLM.

WHAT THE NOVELTY LEDGER SAYS, AND WHY THE CLAIM HERE IS NARROW
-----------------------------------------------------------------------------
Automatically searching for a CERTIFICATE is a mature field: sum-of-squares and
neural Lyapunov/barrier synthesis do exactly that, for stability certificates of
dynamical systems.  `PRECEDENTS` records it as ADJACENT and it is the reason no
originality is claimed for the IDEA.  What twelve arXiv queries do not find is
anyone searching the NORM of a Newton-Kantorovich / radii-polynomial argument --
and the best source in this project's library, Chen-Hou sec 5.3.3, describes doing
it by hand in a documented order.  `novelty_verdict()` computes the gate off the
ledger rather than remembering it.
"""

import numpy as np

from solver.hl_rescaled import sinh_grid_origin
from solver.line_hilbert import line_hilbert_matrix, slope_matrix
from solver.target_selection import y0_budget

# --------------------------------------------------------------------------
# the novelty ledger (Route-M machinery: the gate is COMPUTED, not remembered)
# --------------------------------------------------------------------------
PRECEDENTS = [
    {
        "id": "SOS / neural Lyapunov + barrier synthesis (a field, not a paper)",
        "who": "e.g. arXiv:1101.1043 (SOS for fluid stability), arXiv:2312.09131 "
               "(PINN Lyapunov functions + verification), arXiv:2105.14311 "
               "(barrier certificates via difference-of-convex programming)",
        "what": "Automatic search for the free function of a stability certificate -- "
                "Lyapunov functions, barrier certificates -- by convex optimization or "
                "by learning, with a verification step afterwards.",
        "object_searched": "the certificate FUNCTION for a dynamical system's stability",
        "verdict": "ADJACENT",
        "why_not_preempting": (
            "Different object. They search V(x) for a flow; the search here is over the "
            "NORM of the Banach space in which a Newton-Kantorovich contraction is "
            "measured -- the weight decides whether Y_0, Z_1, Z_2 close, not whether a "
            "candidate function satisfies a pointwise inequality. The overlap is real "
            "enough that NO originality is claimed for the idea of searching a "
            "certificate."),
    },
    {
        "id": "arXiv:2210.07191 sec 5.3.3",
        "who": "J. Chen, T. Hou",
        "what": "'Order of choosing the parameters': an explicit, ordered, HAND procedure "
                "for picking the weights phi_1, phi_2, phi_3 of their weighted L^inf "
                "energy estimate -- powers chosen for the vanishing order at 0 and the "
                "far-field decay, parameters adjusted for a good damping factor, then the "
                "next weight chosen given the previous ones.",
        "object_searched": "the weights of the certificate's norm -- by hand",
        "verdict": "PREMISE_CONFIRMED",
        "why_not_preempting": (
            "This is the human search this stage proposes to automate, written down by "
            "the people who did it best. It confirms the premise and pre-empts nothing: "
            "no optimizer, no fitness, no reported landscape."),
    },
    {
        "id": "arXiv:2302.12877",
        "who": "Cadiot, Lessard, Nave",
        "what": "A completed unbounded-domain radii-polynomial certificate. The space "
                "(Hilbert/Fourier H^l) and its parameter l are FIXED by hand at the start "
                "and the constants are then bounded in it.",
        "object_searched": "none -- the space is a modelling choice, stated not searched",
        "verdict": "EXCLUSION",
        "why_not_preempting": (
            "No search of any kind over the space: l is a modelling decision stated in "
            "their section 2 and held fixed for the whole paper. Read for Route-M as the "
            "one completed unbounded-domain certificate in this project's library, and "
            "it is where the Y_0 budget algebra was gated."),
    },
    {
        "id": "arXiv:2509.14185",
        "who": "Wang, Lai, Gomez-Serrano, Buckmaster et al.",
        "what": "Machine learning (PINNs) used to DISCOVER unstable self-similar blow-up "
                "profiles to near-machine precision, as input to computer-assisted proofs.",
        "object_searched": "the PROFILE (the object), not the certificate around it",
        "verdict": "ADJACENT",
        "why_not_preempting": (
            "The learned thing is the solution; the certificate's function space is still "
            "chosen by hand afterwards. Opposite half of the same pipeline."),
    },
]

# The queries behind the ledger, kept so the gate can be re-run rather than believed.
SEARCH_LOG = [
    ('all:"radii polynomial" AND all:"weight"', 1, "one hit, an ill-posed-PDE application; "
     "no weight search"),
    ('abs:"computer-assisted proof" AND abs:"genetic algorithm"', 0, ""),
    ('abs:"validated numerics" AND abs:"optimal weight"', 0, ""),
    ('all:"weighted" AND all:"Newton-Kantorovich" AND all:"optimize"', 0, ""),
    ('abs:"rigorous numerics" AND abs:"weighted" AND abs:"sequence space"', 0, ""),
    ('all:"ell^1_nu" AND all:"computer-assisted"', 0, ""),
    ('abs:"contraction mapping" AND abs:"choice of norm" AND abs:"optimal"', 0, ""),
    ('abs:"computer-assisted" AND abs:"function space" AND abs:"search"', 0, ""),
    ('abs:"Bayesian optimization" AND abs:"formal verification"', 0, ""),
    ('abs:"machine learning" AND abs:"computer-assisted proof"', 4, "no weight/space search"),
    ('abs:"neural network" AND abs:"Lyapunov function" AND abs:"verification"', 12,
     "the ADJACENT field -- certificate FUNCTION search, not norm search"),
    ('abs:"sum of squares" AND abs:"Lyapunov function" AND abs:"search"', 24, "ditto"),
    ('abs:"barrier certificate" AND abs:"search"', 18, "ditto"),
    ('abs:"self-similar" AND abs:"computer-assisted proof" AND abs:"blow-up"', 2,
     "profile discovery by PINNs; the certificate space is still hand-chosen"),
]


def novelty_verdict():
    """The gate, computed off the ledger. Returns (answer, note, entries).

    answer == "PRE_EMPTED" would stop the stage the way leg 48 stopped stage V;
    "PROCEED_NARROW" means nothing pre-empts the specific question but the adjacent
    field is close enough that the claim must be stated narrowly."""
    pre = [p for p in PRECEDENTS if p["verdict"] == "PRE_EMPTS"]
    adj = [p for p in PRECEDENTS if p["verdict"] == "ADJACENT"]
    if pre:
        return "PRE_EMPTED", "; ".join(p["id"] for p in pre), pre
    note = ("nothing searches the norm of a radii-polynomial certificate; but automatic "
            "search for a stability certificate is a mature field (%d adjacent entries), "
            "so the idea is not new -- only its object is" % len(adj))
    return "PROCEED_NARROW", note, PRECEDENTS


# --------------------------------------------------------------------------
# the known-answer object: bordered a=0 CLM
# --------------------------------------------------------------------------
def exact_profile(X):
    """The closed-form CLM (a=0) rescaled steady profile Omega_0 = -4X/(1+4X^2)."""
    X = np.asarray(X, dtype=float)
    return -4.0 * X / (1.0 + 4.0 * X ** 2)


def exact_hilbert(X):
    """H(Omega_0) = 2/(1+4X^2), in closed form -- the gate on the discrete H."""
    X = np.asarray(X, dtype=float)
    return 2.0 / (1.0 + 4.0 * X ** 2)


EXACT_SLOPE0 = -4.0        # Omega_0'(0)
EXACT_C_OMEGA = -1.0       # the gauge constant the equation returns at c_l = 1
EXACT_TAIL_POWER = 1.0     # |Omega_0| ~ |X|^-1, so the weighted-sup wall is p+q <= 1


class BorderedCLM:
    """The bordered a=0 CLM steady system, its exact Jacobian, and the float certificate.

    Unknown z = concat(Omega [n], c_l, c_omega), size N = n + 2.
    Residual F(z) = concat(R [n], G [2]) with

        R = (c_omega + H Omega) Omega - c_l X Omega_X
        G = ( Omega_X(0) - s_0,  Omega(X_*) - v_0 )

    The two border rows are the GAUGE.  The steady equation has a two-parameter
    family Omega = a Omega_0(b X) with c_omega = -a, c_l = a, so two conditions are
    needed: the slope at the origin and one profile value at a node X_* near the
    shoulder of the profile fix (a, b) together.  Both targets are taken from the
    EXACT continuum profile, so the pins carry no discretization error of their own.

    THE GAUGE IS PART OF THE OBJECT, AND IT DECIDES THE ANSWER.  Pinning the profile
    and letting (c_l, c_omega) come out IMPLICITLY is what `bordered_hl.py` does, and
    it is what makes this substrate comparable to the target.  An earlier version of
    this module pinned c_l = 1 directly; that makes A's c_l row a unit vector, kills
    the border-row conditioning, and with it the entire weight effect leg 46 found
    (the naive-vs-tuned gain drops from 5.6e3 to 0.6).  Measured, not assumed --
    `test_weight_search.py` gates both gauges.

    Both border rows are affine, so F stays exactly quadratic and Z_2 stays exact.
    """

    def __init__(self, n=201, c=0.5, rho_max=8.0, slope0=EXACT_SLOPE0, x_pin=1.0):
        rho, X = sinh_grid_origin(n, c=c, rho_max=rho_max)
        self.rho, self.X = rho, X
        self.n = X.size
        self.N = self.n + 2
        self.i0 = self.n // 2
        if abs(self.X[self.i0]) > 1e-12:
            raise ValueError("origin is not a node")
        self.H = line_hilbert_matrix(X)
        self.D = slope_matrix(X)
        self.XD = self.X[:, None] * self.D          # the X d/dX operator, as a matrix
        self.Drow0 = self.D[self.i0].copy()
        self.slope0 = float(slope0)
        self.Xmax = float(np.abs(self.X).max())
        self.jstar = int(np.argmin(np.abs(self.X - x_pin)))
        self.v_pin = float(exact_profile(self.X[self.jstar]))

    # -- packing -----------------------------------------------------------
    def pack(self, Omega, c_l, c_omega):
        return np.concatenate([Omega, [c_l, c_omega]])

    def unpack(self, z):
        return z[:self.n], float(z[self.n]), float(z[self.n + 1])

    def exact_state(self):
        """The continuum answer, sampled on the grid. NOT a solution of the discrete
        system -- the gap between the two is measured, not assumed."""
        return self.pack(exact_profile(self.X), 1.0, EXACT_C_OMEGA)

    # -- residual, Jacobian, exact remainder -------------------------------
    def F(self, z):
        Om, c_l, c_om = self.unpack(z)
        R = (c_om + self.H @ Om) * Om - c_l * (self.XD @ Om)
        return np.concatenate([R, [self.Drow0 @ Om - self.slope0,
                                   Om[self.jstar] - self.v_pin]])

    def jacobian(self, z):
        Om, c_l, c_om = self.unpack(z)
        n = self.n
        J = np.zeros((self.N, self.N))
        J[:n, :n] = (np.diag(c_om + self.H @ Om) + Om[:, None] * self.H
                     - c_l * self.XD)
        J[:n, n] = -(self.XD @ Om)
        J[:n, n + 1] = Om
        J[n, :n] = self.Drow0
        J[n + 1, self.jstar] = 1.0
        return J

    def quadratic(self, v):
        """Q(v,v) = F(z+v) - F(z) - DF(z)v, EXACTLY and independently of z."""
        om, a_l, a_om = self.unpack(v)
        return np.concatenate([(a_om + self.H @ om) * om - a_l * (self.XD @ om),
                               np.zeros(2)])

    def _F_longdouble(self, z):
        """F evaluated in np.longdouble -- used ONLY to measure how much of a float64
        residual is arithmetic noise.  Not part of any bound."""
        zl = np.asarray(z, dtype=np.longdouble)
        Om, c_l, c_om = zl[:self.n], zl[self.n], zl[self.n + 1]
        R = ((c_om + self.H.astype(np.longdouble) @ Om) * Om
             - c_l * (self.XD.astype(np.longdouble) @ Om))
        return np.concatenate([R, [self.Drow0.astype(np.longdouble) @ Om
                                   - np.longdouble(self.slope0),
                                   Om[self.jstar] - np.longdouble(self.v_pin)]])

    def residual_floor(self, z, safety=8.0):
        """The float64 EVALUATION noise of F at z -- the level below which |F| stops
        being a statement about the equation and becomes a statement about the
        arithmetic (banked lesson 86).

        Measured, not guessed: F is re-evaluated in longdouble at the same point and
        the difference taken.  `H @ Omega` is a dense n-term sum with cancellation, so
        this GROWS with n -- 2.4e-15 at n = 201, 5.9e-15 at 401, 1.0e-14 at 801,
        2.2e-14 at 1201.  A fixed 1e-14 tolerance is therefore below the floor from
        n ~ 800 upward, which is why `newton` used to spin its full iteration budget
        at n = 801 while the residual random-walked around 1.1e-14.
        """
        return float(safety * np.abs(np.asarray(self.F(z))
                                     - self._F_longdouble(z).astype(float)).max())

    def newton(self, z0=None, tol=None, max_iter=20, stall_factor=0.5):
        """Damped Newton. Returns (z, info) with the residual ladder in full -- the
        SHAPE of a ladder is the evidence (standing discipline 72).

        `tol=None` (the default) means "the measured float64 residual floor for this
        grid" rather than a hard-coded constant; pass a number to demand a specific
        one.  Iteration also stops when the ladder STALLS -- two consecutive steps
        that fail to improve the residual by `stall_factor` -- because a Newton that
        has reached its arithmetic floor is converged, and continuing only spends
        O(N^3) solves to random-walk in the last two digits.
        """
        z = self.exact_state() if z0 is None else np.array(z0, dtype=float)
        auto = tol is None
        tol = self.residual_floor(z) if auto else float(tol)
        ladder = [float(np.abs(self.F(z)).max())]
        stalled = False
        for _ in range(max_iter):
            Fz = self.F(z)
            dz = np.linalg.solve(self.jacobian(z), -Fz)
            lam, r0 = 1.0, float(np.abs(Fz).max())
            while lam > 1.0 / 1024 and float(np.abs(self.F(z + lam * dz)).max()) >= r0:
                lam *= 0.5
            z = z + lam * dz
            ladder.append(float(np.abs(self.F(z)).max()))
            if auto:
                tol = max(tol, self.residual_floor(z))
            if ladder[-1] < tol:
                break
            if len(ladder) >= 4 and all(ladder[-i] > stall_factor * ladder[-i - 1]
                                        for i in (1, 2)):
                stalled = True
                break
        floor = self.residual_floor(z)
        return z, {"residual_ladder": np.array(ladder),
                   "tolerance": float(tol),
                   "residual_floor": floor,
                   "stalled_at_floor": bool(stalled and ladder[-1] < floor),
                   "converged": bool(ladder[-1] < tol)}

    # -- the weighted-sup certificate --------------------------------------
    def weight_vector(self, theta):
        """nu(X) = (1+(X/L)^2)^(p/2) (1+(X/l)^2)^(q/2), then the two scalar weights.

        theta = (p, log10 L, q, log10 l, log10 (w_l / X_max)); w_om = 1 is the GAUGE
        fixed by the scale invariance proved in the module docstring.  The last gene
        is RELATIVE to X_max so that a genome means the same thing on every grid --
        leg 46's hand-tuned constant is w_l = 0.01 X_max, i.e. gene = -2 exactly."""
        p, logL, q, logl, logwl = (float(t) for t in theta)
        # built in log space and clipped: a weight that overflows float64 is a
        # NUMBER problem, not a search finding, and silently returning inf here
        # would let the optimizer "win" by overflowing (banked lesson 67).
        lg = (0.5 * p * np.log1p((self.X / 10.0 ** logL) ** 2)
              + 0.5 * q * np.log1p((self.X / 10.0 ** logl) ** 2))
        nu = np.exp(np.clip(lg, -LOG_NU_CLIP, LOG_NU_CLIP))
        return np.concatenate([nu, [self.Xmax * 10.0 ** logwl, 1.0]]), nu

    def certificate_constants(self, z, theta, A=None, J=None):
        """(Y_0, Z_1, Z_2) in the weighted sup norm at z, for the weight theta."""
        J = self.jacobian(z) if J is None else J
        A = np.linalg.inv(J) if A is None else A
        w, nu = self.weight_vector(theta)
        Fz = self.F(z)
        Y0 = float(np.max(w * np.abs(A @ Fz)))
        M = np.eye(self.N) - A @ J
        Z1 = float(np.max(w * (np.abs(M) @ (1.0 / w))))
        A_norm = float(np.max(w * (np.abs(A) @ (1.0 / w))))
        H_ni = float(np.max(np.abs(self.H) @ (1.0 / nu)))
        XD_nn = float(np.max(nu * (np.abs(self.XD) @ (1.0 / nu))))
        w_l, w_om = w[self.n], w[self.n + 1]
        B = H_ni + 1.0 / w_om + XD_nn / w_l
        Z2 = 2.0 * A_norm * B
        return {"Y0": Y0, "Z1": Z1, "Z2": Z2, "A_norm": A_norm, "B": B,
                "H_norm": H_ni, "XD_norm": XD_nn, "w_l": float(w_l),
                "budget": y0_budget(Z1, Z2)}


# --------------------------------------------------------------------------
# the fitness -- ONE NUMBER, and the box the equation itself imposes
# --------------------------------------------------------------------------
GENE_NAMES = ("p", "log10_L", "q", "log10_l", "log10_w_l_over_Xmax")
# The box. Only the WALL below is analytic; these bounds are engineering, and the
# rule they were set by is stated so a reader can check it: each one is wide enough
# that widening it further does not move the optimum (measured -- see the leg's
# `box_widening` probe, which pushed |p|,|q| to 32 and gained nothing).
#   p, q            four powers either side of flat
#   log10 L, l      from far inside the profile's own scale (0.5) to the domain edge
#                   (X_max = 745 at log10 = 2.87)
#   log10 w_l/X_max six decades below leg 46's hand constant to two above naive
BOX_LOWER = np.array([-4.0, -3.0, -4.0, -3.0, -6.0])
BOX_UPPER = np.array([4.0, 3.0, 4.0, 3.0, 2.0])
LOG_NU_CLIP = 500.0              # exp() guard; see weight_vector

WALL_POWER = EXACT_TAIL_POWER    # p+q > 1 => the TRUE profile has infinite norm
WALL_DELTA = 0.05                # the box stops short of the wall by this much

# --- P2 REPAIR (leg 50, prep/weight-repairs) ---------------------------------------
# Leg 49's P2 measured 0.775 finite against a 0.90 threshold: 9/40 roster weights
# returned no fitness because Z_1 >= 1 there, and every one of them had far-field power
# p+q <= -2.41 -- i.e. they sat below a SECOND wall (`lower_wall()`, already in this
# module) that the box never carried. The upper wall K3 is analytic and was already a
# hard constraint on `in_box`; this repair carries the MEASURED lower wall the same
# way, so the roster and the grid search stop being handed points the equation's own
# float conditioning has already ruled out. Named in TECHNICAL_P2_ROUTEC_PILOT_V0 S4b.
WALL_LOWER_DELTA = 0.05          # the box stops short of the measured lower wall too

# --- FROZEN six-property thresholds (pre-committed, before any run) ---
P1_SPREAD_MIN = 1.0        # decades of fitness spread over the roster: not dead flat
P2_FINITE_FRAC = 0.90      # fraction of roster weights returning a finite fitness
P3_MONO_VIOLATIONS = 0     # Newton ladder: the fitness must fall every step, always
P4_RANK_RHO_MIN = 0.90     # Spearman rank correlation of the roster across resolutions
P4_TOP3_OVERLAP = 2        # of the top three weights, this many must survive refinement
P5_BAND_MIN = 2.0          # decades: the band the search has to work with
P6_INTERIOR_FRAC = 0.05    # the optimum must sit this far (in box widths) off every bound


def far_field_power(theta):
    """p + q: the exponent nu carries as |X| -> infinity."""
    return float(theta[0]) + float(theta[2])


def in_box(theta, lower_wall_power=None):
    """The analytic wall K3 (upper), as a hard constraint -- derived from the profile's
    tail BEFORE any run, so it is the equation's wall, not a fitted one -- AND, the P2
    repair, the MEASURED lower wall (`lower_wall()`), carried the same way.

    `lower_wall_power` is None by default, which reproduces the pre-repair behaviour
    exactly (only the upper wall applies) -- callers that have measured a lower wall
    for their resolution (the six-property gate; anything built off a `FitnessEngine`
    with `lower_wall_power` set) pass it through."""
    t = np.asarray(theta, dtype=float)
    if np.any(t < BOX_LOWER) or np.any(t > BOX_UPPER):
        return False
    ffp = far_field_power(t)
    if ffp > WALL_POWER - WALL_DELTA:
        return False
    if lower_wall_power is not None and ffp < lower_wall_power + WALL_LOWER_DELTA:
        return False
    return True


class FitnessEngine:
    """Batched evaluation of log10(Y_0/budget) over many weights at a fixed state.

    The Jacobian, its inverse and the residual do NOT depend on the weight, so they
    are computed once; every evaluation is then four matrix-vector products. This is
    why a 5-gene brute-force grid is affordable and the gate does not need the GA
    (which `plan_of_record.py` bans until the gate reports).
    """

    def __init__(self, problem, z, lower_wall_power=None):
        self.pr = problem
        self.z = np.array(z, dtype=float)
        # P2 repair: the measured lower wall for THIS problem/resolution, carried in
        # the box the same way the analytic upper wall already is. None reproduces the
        # pre-repair behaviour (upper wall only).
        self.lower_wall_power = lower_wall_power
        self.J = problem.jacobian(self.z)
        self.A = np.linalg.inv(self.J)
        self.absA = np.abs(self.A)
        self.absM = np.abs(np.eye(problem.N) - self.A @ self.J)
        self.aAF = np.abs(self.A @ problem.F(self.z))
        self.absH = np.abs(problem.H)
        self.absXD = np.abs(problem.XD)

    def constants_many(self, thetas):
        """(Y0, Z1, Z2) for each row of thetas. Shapes (k,)."""
        pr = self.pr
        thetas = np.atleast_2d(np.asarray(thetas, dtype=float))
        k = thetas.shape[0]
        W = np.empty((k, pr.N))
        NU = np.empty((k, pr.n))
        for i, th in enumerate(thetas):
            W[i], NU[i] = pr.weight_vector(th)
        iW, iNU = 1.0 / W, 1.0 / NU
        Y0 = np.max(W * self.aAF[None, :], axis=1)
        Z1 = np.max(W * (iW @ self.absM.T), axis=1)
        A_norm = np.max(W * (iW @ self.absA.T), axis=1)
        H_ni = np.max(iNU @ self.absH.T, axis=1)
        XD_nn = np.max(NU * (iNU @ self.absXD.T), axis=1)
        B = H_ni + 1.0 / W[:, pr.n + 1] + XD_nn / W[:, pr.n]
        Z2 = 2.0 * A_norm * B
        return Y0, Z1, Z2

    def fitness_many(self, thetas, box=True):
        """log10(Y_0 / budget) per row; +inf where Z_1 >= 1 or the box is violated."""
        thetas = np.atleast_2d(np.asarray(thetas, dtype=float))
        Y0, Z1, Z2 = self.constants_many(thetas)
        bud = np.where(Z1 < 1.0, (1.0 - Z1) ** 2 / (2.0 * Z2), -1.0)
        out = np.where((bud > 0) & (Y0 > 0), np.log10(np.abs(Y0) / np.abs(bud)), np.inf)
        out = np.where(np.isfinite(out), out, np.inf)
        if box:
            bad = np.array([not in_box(th, self.lower_wall_power) for th in thetas])
            out = np.where(bad, np.inf, out)
        return out

    def fitness(self, theta, box=True):
        return float(self.fitness_many(np.atleast_2d(theta), box=box)[0])


# --------------------------------------------------------------------------
# the reference weights: what a hand does, so the search has something to beat
# --------------------------------------------------------------------------
def hand_weights(problem=None):
    """The two hand-picked weights this project has actually used.

    `naive` is `bordered_hl.weights`'s default (flat nu, w_l = max|X|, chosen so the
    c_l X term is O(1) at unit norm). `tuned_leg46` is leg 46's one-constant change,
    w_l = 0.01 max|X|, which bought 5186x on the HL object. In this genome the last
    gene is log10(w_l / X_max), so the pair is exactly 0 and -2."""
    flat = (0.0, 0.0, 0.0, 0.0)      # p, log10 L, q, log10 l  -> nu == 1
    return {
        "naive": np.array([*flat, 0.0]),
        "tuned_leg46": np.array([*flat, -2.0]),
    }


def roster(problem, n_random=32, seed=0, lower_wall_power=None):
    """The fixed weight roster the six-property gate is measured on.

    Structured like Gate 4's shape roster: controls (the two hand weights), trivial
    /degenerate candidates that TEST property 6 (weights that turn a component of the
    norm off, or push the far-field power at the wall), and a random spanning set.

    P2 REPAIR: `lower_wall_power`, when given, is carried into the random draw's
    `in_box` check exactly like the analytic upper wall already is -- so the roster
    stops being handed weights the measured wall has already ruled out. None (the
    default) reproduces the pre-repair roster exactly."""
    rng = np.random.default_rng(seed)
    hw = hand_weights()
    items = [("ctrl_naive", hw["naive"]), ("ctrl_tuned_leg46", hw["tuned_leg46"])]
    Xmax = float(np.abs(problem.X).max())
    degenerate = {
        # w_l pushed to both ends: does the fitness reward switching off the c_l row?
        "triv_wl_tiny": np.array([0.0, 0.0, 0.0, 0.0, BOX_LOWER[4]]),
        "triv_wl_huge": np.array([0.0, 0.0, 0.0, 0.0, BOX_UPPER[4]]),
        # all the weight at the wall, and a two-factor weight that cancels in the tail
        "triv_at_wall": np.array([WALL_POWER - WALL_DELTA, 0.0, 0.0, 0.0, -2.0]),
        "triv_cancel": np.array([1.5, 0.0, -1.5, np.log10(Xmax), -2.0]),
        # scales pushed outside the profile's own length scale (0.5 sets Omega_0)
        "triv_L_tiny": np.array([0.5, BOX_LOWER[1], 0.0, 0.0, -2.0]),
        "triv_L_huge": np.array([0.5, BOX_UPPER[1], 0.0, 0.0, -2.0]),
    }
    items += list(degenerate.items())
    for i in range(n_random):
        while True:
            th = BOX_LOWER + rng.random(5) * (BOX_UPPER - BOX_LOWER)
            if in_box(th, lower_wall_power):
                break
        items.append((f"rand_{i:02d}", th))
    return items


# --------------------------------------------------------------------------
# brute force: the deterministic optimum, which is the GA's known answer
# --------------------------------------------------------------------------
def grid_search(engine, per_gene=7, box=True, refine=2, shrink=0.35):
    """Dense grid + local refinement. Deterministic, and the reason the gate does not
    need the GA: `plan_of_record` bans GA compute until the fitness is validated."""
    lo, hi = BOX_LOWER.copy(), BOX_UPPER.copy()
    best, best_f, evals = None, np.inf, 0
    for _ in range(refine + 1):
        axes = [np.linspace(lo[i], hi[i], per_gene) for i in range(5)]
        grid = np.stack([g.ravel() for g in np.meshgrid(*axes, indexing="ij")], axis=1)
        vals = engine.fitness_many(grid, box=box)
        evals += grid.shape[0]
        k = int(np.argmin(vals))
        if vals[k] < best_f:
            best_f, best = float(vals[k]), grid[k].copy()
        span = (hi - lo) * shrink
        lo = np.maximum(BOX_LOWER, best - 0.5 * span)
        hi = np.minimum(BOX_UPPER, best + 0.5 * span)
    return {"theta": best, "fitness": best_f, "evaluations": evals}


def lower_wall(engine, w_l_gene=-2.0, lo=-8.0, hi=3.0, iters=45):
    """The OTHER wall, and this one is measured rather than derived.

    Sweep the far-field power down a single-factor slice nu = (1+X^2)^(p/2) and find
    where Z_1 crosses 1 -- past that point A stops being an approximate inverse in
    the norm and no certificate exists at any residual. The admissible band for the
    far-field power is therefore (p_-, p*], bounded above by the equation (the true
    profile's norm) and below by the FLOAT rehearsal's conditioning.

    Returns p_- as a bisection, or hi if Z_1 < 1 everywhere on the slice."""
    def z1_at(p):
        _, Z1, _ = engine.constants_many(np.array([[p, 0.0, 0.0, 0.0, w_l_gene]]))
        return float(Z1[0])
    if z1_at(hi) < 1.0 and z1_at(lo) < 1.0:
        return float(lo)               # no crossing: the whole slice is admissible
    a, b = lo, hi
    for _ in range(iters):
        mid = 0.5 * (a + b)
        if z1_at(mid) >= 1.0:
            a = mid
        else:
            b = mid
    return 0.5 * (a + b)


def interior_margin(theta):
    """How far the optimum sits off every BOX bound, in box widths (property 6a).

    The wall is deliberately NOT folded in here: an optimum can be interior in every
    gene and still be decided by the wall, and conflating the two hides which one is
    load-bearing. `wall_binding` answers that separately."""
    t = np.asarray(theta, dtype=float)
    width = BOX_UPPER - BOX_LOWER
    return float(np.min(np.minimum(t - BOX_LOWER, BOX_UPPER - t) / width))


# --------------------------------------------------------------------------
# the six-property viability gate, on THIS fitness
# --------------------------------------------------------------------------
def _spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    ra = np.argsort(np.argsort(a[m])).astype(float)
    rb = np.argsort(np.argsort(b[m])).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    d = np.sqrt((ra @ ra) * (rb @ rb))
    return float(ra @ rb / d) if d > 0 else 0.0


def _r2(x, y):
    """R^2 of the least-squares line y ~ x, on the finite entries."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if x.size < 3 or np.std(x) == 0:
        return 0.0
    c = np.polyfit(x, y, 1)
    r = y - np.polyval(c, x)
    return float(1.0 - (r @ r) / ((y - y.mean()) @ (y - y.mean())))


# --- P3 REPAIR (leg 50, prep/weight-repairs) ---------------------------------------
# Leg 49's raw P3 pushed every weight through the SAME global eps grid and asked for
# slope-1 everywhere on it. That conflates two different things: F(z*+eps d) is only
# LINEAR in eps once eps is small enough relative to ||A||_w -- and ||A||_w spans three
# orders of magnitude across the roster (naive 1.69e8 down to the searched optimum
# 3.37e5). A grid that is safely linear for the searched weight is already nonlinear
# for the naive one, so probing all weights on one grid measures the PROBE's own
# breakdown at some weights, not the fitness's defect-tracking. Diagnosed in
# TECHNICAL_P2_ROUTEC_PILOT_V0 S4a: the corrected window (eps <~ 1/||A||_w) recovers
# the known answer (slope 1) at the median, 0.2% typically.
#
# THE REPAIR: give every weight its OWN eps window, set from its OWN ||A||_w at the
# converged state, fixed before any slope is fit -- and report what that window BUYS
# (how many decades, how many weights it resolves) as a RESOLUTION, rather than
# silently assuming the whole grid was in the linear regime for every weight.
DEFECT_WINDOW_C = 0.1        # eps <= C / ||A||_w defines "linear enough"; a factor of
                              # 10 inside the empirically-found onset (eps ~ 1/||A||_w),
                              # fixed once, before this repair's numbers were measured
DEFECT_EPS_DEFAULT = (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11)
DEFECT_MIN_WINDOW = 3         # fewer usable eps than this -> UNRESOLVED, not "passes"


def defect_ladder(problem, z_star, engine_thetas, direction=None, eps=None):
    """Property 3 with a KNOWN ANSWER, not merely a known direction -- WITH the P3
    repair: each weight gets its own linear window instead of one grid for all.

    Push the converged state off the solution by eps in a fixed direction. For small
    eps, F(z*+eps d) = eps DF d + O(eps^2), so Y_0 is LINEAR in eps and the fitness
    must fall with slope exactly 1 per decade -- but only INSIDE the window where the
    linearisation actually holds for that weight's own ||A||_w. Returns
    (eps, fitness table, slopes, mono_ok, resolution):

      eps         the full probed grid (unchanged shape, for backward compatibility)
      table       fitness at every (eps, weight) pair, box=False
      slopes      per-weight fitted slope, using ONLY that weight's window; NaN where
                  the window held fewer than DEFECT_MIN_WINDOW usable points
      mono_ok     per-weight bool, monotone decrease WITHIN the window
      resolution  per-weight dict {eps_max, n_window, resolved} -- the accuracy
                  statement this repair asks for instead of assumed exactness
    """
    z_star = np.asarray(z_star, float)
    if direction is None:
        rng = np.random.default_rng(7)
        direction = rng.standard_normal(problem.N)
        direction /= np.abs(direction).max()
    if eps is None:
        eps = DEFECT_EPS_DEFAULT
    eps = np.asarray(eps, float)
    thetas = np.atleast_2d(np.asarray(engine_thetas, dtype=float))

    rows = []
    for e in eps:
        engp = FitnessEngine(problem, z_star + e * direction)
        rows.append(engp.fitness_many(thetas, box=False))
    tab = np.array(rows)                        # (len(eps), n_weights)
    le = np.log10(eps)

    # each weight's own window, from ITS OWN ||A||_w at the converged (unperturbed)
    # state -- the probe direction is fixed and small, so the base-state conditioning
    # is what decides where the linear regime starts
    eng0 = FitnessEngine(problem, z_star)
    a_norms = np.array([
        problem.certificate_constants(z_star, th, A=eng0.A, J=eng0.J)["A_norm"]
        for th in thetas])
    eps_max = DEFECT_WINDOW_C / np.maximum(a_norms, 1.0)

    n_theta = thetas.shape[0]
    slopes = np.full(n_theta, np.nan)
    mono_ok = np.zeros(n_theta, dtype=bool)
    resolution = []
    for j in range(n_theta):
        mask = eps <= eps_max[j]
        col = tab[mask, j]
        n_pts = int(mask.sum())
        resolved = bool(n_pts >= DEFECT_MIN_WINDOW and np.all(np.isfinite(col)))
        resolution.append({"eps_max": float(eps_max[j]), "n_window": n_pts,
                           "resolved": resolved})
        if resolved:
            slopes[j] = float(np.polyfit(le[mask], col, 1)[0])
            mono_ok[j] = bool(np.all(np.diff(col) < 0))
    return eps, tab, slopes, mono_ok, resolution


def six_property_gate(problem_coarse, problem_fine, n_random=32, seed=0,
                      per_gene=9, refine=4):
    """The FROZEN predicate, run on the weight fitness. Returns a report dict.

    Both branches are actionable and were written before the run: PASS lifts the ban
    on GA compute and stage B proceeds; FAIL stops the stage and names the property.
    """
    zc, info_c = problem_coarse.newton()
    zf, _ = problem_fine.newton()
    eng_c, eng_f = FitnessEngine(problem_coarse, zc), FitnessEngine(problem_fine, zf)

    # P2 REPAIR: measure this resolution's lower wall and carry it in the box the
    # same way the analytic upper wall already is -- both the roster draw and the
    # grid search (via the engines' `lower_wall_power`) now respect it.
    lw_c, lw_f = lower_wall(eng_c), lower_wall(eng_f)
    eng_c.lower_wall_power, eng_f.lower_wall_power = lw_c, lw_f

    rost_c = roster(problem_coarse, n_random=n_random, seed=seed, lower_wall_power=lw_c)
    labels = [lab for lab, _ in rost_c]
    th = np.array([t for _, t in rost_c])
    vc = eng_c.fitness_many(th, box=False)
    vf = eng_f.fitness_many(th, box=False)

    fin = np.isfinite(vc)
    spread = float(np.max(vc[fin]) - np.min(vc[fin])) if fin.any() else 0.0

    # P3 REPAIR -- the defect ladder, each weight in its OWN linear window; report
    # the accuracy as a resolution (how many weights resolved, and how well the
    # resolved ones track slope 1) instead of assuming one global eps grid is valid
    # everywhere.
    eps, tab, slopes, mono_ok, resolution = defect_ladder(problem_coarse, zc, th)
    resolved = np.array([r["resolved"] for r in resolution])
    mono_viol = int(np.sum(resolved & ~mono_ok))
    good_slopes = slopes[resolved & np.isfinite(slopes)]
    slope_err = float(np.max(np.abs(good_slopes - 1.0))) if good_slopes.size else np.inf
    n_unresolved = int(np.sum(~resolved))

    # P4 -- ranking survives refinement
    rho = _spearman(vc, vf)
    top3_c = set(np.argsort(np.where(fin, vc, np.inf))[:3])
    top3_f = set(np.argsort(np.where(np.isfinite(vf), vf, np.inf))[:3])
    overlap = len(top3_c & top3_f)

    # P6 -- the optimum: interior in the genes, and is the WALL what stops it?
    g_box = grid_search(eng_c, per_gene=per_gene, box=True, refine=refine)
    g_free = grid_search(eng_c, per_gene=per_gene, box=False, refine=refine)
    margin = interior_margin(g_box["theta"])
    wall_gain = float(g_box["fitness"] - g_free["fitness"])   # >0 means the wall costs

    props = {
        "P1_nonzero": {"spread_decades": spread, "threshold": P1_SPREAD_MIN,
                       "pass": bool(spread >= P1_SPREAD_MIN)},
        "P2_finite": {"finite_fraction": float(fin.mean()), "threshold": P2_FINITE_FRAC,
                      "lower_wall_power_coarse": lw_c, "lower_wall_power_fine": lw_f,
                      "pass": bool(fin.mean() >= P2_FINITE_FRAC)},
        "P3_monotone": {"violations": mono_viol, "max_slope_error": slope_err,
                        "n_resolved": int(resolved.sum()), "n_unresolved": n_unresolved,
                        "threshold_violations": P3_MONO_VIOLATIONS,
                        "threshold_slope_error": 0.05,
                        "pass": bool(mono_viol <= P3_MONO_VIOLATIONS and slope_err <= 0.05)},
        "P4_resolution_stable": {"spearman": rho, "top3_overlap": overlap,
                                 "threshold_spearman": P4_RANK_RHO_MIN,
                                 "threshold_overlap": P4_TOP3_OVERLAP,
                                 "pass": bool(rho >= P4_RANK_RHO_MIN
                                              and overlap >= P4_TOP3_OVERLAP)},
        "P5_wide_band": {"band_decades": spread, "threshold": P5_BAND_MIN,
                         "pass": bool(spread >= P5_BAND_MIN)},
        "P6_nontrivial_optimum": {
            "interior_margin": margin, "threshold_margin": P6_INTERIOR_FRAC,
            "far_field_power_free": far_field_power(g_free["theta"]),
            "wall_power": WALL_POWER,
            "wall_cost_decades": wall_gain, "threshold_wall_cost": 0.05,
            "pass": bool(margin >= P6_INTERIOR_FRAC and wall_gain <= 0.05
                         and far_field_power(g_free["theta"]) < WALL_POWER)},
    }
    verdict = "PASS" if all(p["pass"] for p in props.values()) else "FAIL"

    # the SUBSTANTIVE diagnostics -- Gate 4's lesson is that a 6/6 can still be a
    # false pass, and what caught it was a correlation nobody had gated
    single = {GENE_NAMES[i]: _r2(th[:, i], vc) for i in range(5)}
    single["far_field_power"] = _r2(th[:, 0] + th[:, 2], vc)
    return {
        "verdict": verdict, "properties": props,
        "labels": labels, "theta": th.tolist(),
        "fitness_coarse": vc.tolist(), "fitness_fine": vf.tolist(),
        "newton_ladder_coarse": info_c["residual_ladder"].tolist(),
        "defect_ladder": {"eps": eps.tolist(), "slopes": slopes.tolist(),
                          "resolution": resolution},
        "lower_wall": {"coarse": lw_c, "fine": lw_f},
        "optimum_box": {"theta": g_box["theta"].tolist(), "fitness": g_box["fitness"],
                        "evaluations": g_box["evaluations"]},
        "optimum_free": {"theta": g_free["theta"].tolist(), "fitness": g_free["fitness"]},
        "single_predictor_r2": single,
    }
