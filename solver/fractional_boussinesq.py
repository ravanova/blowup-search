"""2D Boussinesq with fractional dissipation -- the critical-dissipation exponent,
ported off the 1D toy and onto the object where certification results count.

ROUTE G v1.  Ranked items (2) and (3) of "what would actually be worthwhile", which
merged: (3) said port to 2D Boussinesq / axisymmetric Euler WITH BOUNDARY, because
that is the Hou-Luo geometry that 1D gCLM is a model OF, and (2) said measure the
dissipation scaling at which viscosity kills a blow-up that exists.  Route-F v1 did
(2) in 1D and got s_c = alpha/2.  This leg asks the same question of the 2D system.

    omega_t + u.grad omega = theta_x - nu (-Delta)^s omega
    theta_t + u.grad theta = 0
    u = grad^perp (-Delta)^{-1} omega ,   omega odd-odd, theta even-odd

on the 2 pi-periodic square with the Hou-Luo symmetry (the parity that puts a
no-flow wall at y = 0 and an axis at x = 0 exactly).  s = 1 is the ordinary
Laplacian; s is the dial.

--------------------------------------------------------------------------
THE LAW IS NOT s_c = alpha/2.  IT IS s_c = 1/(2 beta), AND beta IS THE DIAL
--------------------------------------------------------------------------
Route-F v1 wrote the criticality condition as s_c = alpha(a)/2 with alpha the
FAR-FIELD DECAY EXPONENT of the 1D self-similar profile.  That form is specific to
gCLM -- worse, it is specific to gCLM's gauge c_l = 1 -- and it does not survive the
port.  The invariant statement underneath it is about the COLLAPSE EXPONENT.

Let a blow-up have amplitude and length scale

    omega ~ (T-t)^{-1} ,      L ~ (T-t)^{beta} .

The amplitude exponent is not a choice: omega_t ~ omega^2 forces it for any
quadratically nonlinear transport, and the Boussinesq route to it is the same
(omega_t ~ theta_x with theta ~ (T-t)^{beta-2}).  Then

    dissipation / driving  ~  nu omega L^{-2s} / omega^2  ~  nu (T-t)^{1 - 2 s beta}

so dissipation is asymptotically negligible exactly when 1 - 2 s beta > 0:

    **s  <  s_c = 1 / (2 beta) .**                                            (SC)

Three consequences, and the third is the reason to do the port at all.

* **1D is the special case.**  In the gCLM rescaling the two ODEs integrate to
  beta = 1/alpha (Route-E v1, with c_l = 1), so 1/(2 beta) = alpha/2 and Route-F's
  headline is (SC) written in the toy's own coordinates.
* **NAVIER-STOKES IS beta = 1/2.**  NS's scaling L ~ (T-t)^{1/2} is forced by
  dimensional analysis, and (SC) then returns s_c = 1 -- the ordinary Laplacian,
  exactly.  Every scaling argument about NS returns zero information because the
  two sides balance identically.  **beta = 1/2 is the critical line, and which side
  of it a blow-up sits on is the whole question.**
* **THE DIRECTION IS THE OPPOSITE OF THE INTUITIVE ONE.**  s_c = 1/(2 beta) is
  DECREASING in beta, so a blow-up that collapses FASTER than the NS rate loses to
  viscosity more easily, not less.  Beating ordinary viscosity requires beta < 1/2,
  i.e. an ANOMALOUSLY SLOW collapse.  This is worth stating in those words because
  "the singularity is very violent, so it should beat viscosity" is exactly wrong:
  violence in the amplitude is fixed at (T-t)^{-1}, and all the freedom is in how
  small the structure has to get to achieve it.  A structure that reaches the same
  amplitude on a LARGER length scale is the one viscosity cannot touch.

--------------------------------------------------------------------------
WHERE THE KNOWN 2D BOUSSINESQ BLOW-UP SITS -- ARITHMETIC ON PUBLISHED CONSTANTS
--------------------------------------------------------------------------
For the Chen-Hou self-similar profile (Part I arXiv:2210.07191 (2.23), transcribed
in PHASE2_SPIKE1_NOTES.md sec.1), the dynamic-rescaling constants are

    c_l = 3.00649898 ,   c_omega = -1.02942516 ,   alpha_2D = c_omega/c_l = -0.342407

and `collapse_exponent_from_rescaling` below derives beta = -c_l/c_omega = 2.92056
from the rescaling ODEs (see its docstring for the two-line derivation, which also
shows WHY the far-field exponent equals c_omega/c_l: it is the statement that the
blow-up does not disturb the outer solution).  So

    **beta(Chen-Hou 2D Boussinesq) = 2.9206  =>  s_c = 0.17120 .**

The proven Euler-type boundary blow-up sits at about ONE SIXTH of the NS-critical
exponent.  It is not close to beating ordinary viscosity; it is nearly six times
too fast a collapse.  That is not a defect of the Chen-Hou scenario -- it is a
measurement of how far the toy is from the obstruction, and it is the first number
this project has that says so on the 2D object rather than the 1D one.

--------------------------------------------------------------------------
WHAT THIS MODULE MEASURES
--------------------------------------------------------------------------
Same discipline as Route-F: measure an EXPONENT, not a threshold.  Track
D/N at the peak and fit D/N ~ (T-t)^p; the prediction is a LINE

    p(s) = 1 - 2 beta s ,     slope -2 beta ,     zero at s_c = 1/(2 beta) ,

whose slope, intercept and zero are separately checkable.  The 2D leg additionally
measures beta FROM THE RUN'S OWN GEOMETRY (amplitude over gradient, and the
enstrophy-spectrum centroid), which is a different observable from D/N.  So the
cross-check here is internal but not circular: geometry predicts the slope of a
line fitted to a dissipation ratio.

ANISOTROPY IS FIRST-CLASS.  The Hou-Luo collapse is not isotropic, and dissipation
is set by the SMALLEST scale, so L_x and L_y are tracked separately and the
prediction is quoted against beta_max = max(beta_x, beta_y) -- the fastest-collapsing
direction.  Using an isotropic proxy would silently average the thing that matters.

HONEST SCOPE.  The object here is the periodic-box grower from the Phase-1
ground-truth roster, not the Chen-Hou self-similar profile: it is a collapsing
structure in the right geometry with the right symmetry, and its beta is its own.
The Chen-Hou number above is arithmetic on published constants, not something this
module reproduces.  Plain float64; nothing is interval-enclosed and nothing is
rigorous.
"""

import time

import numpy as np

from solver.boussinesq import (
    TWO_PI, dealias_mask2d, grid2d, project_even_odd, project_odd_odd,
    velocity_from_vorticity, wavenumbers2d,
)

# Chen-Hou Part I (2.23), the published one-scale rescaling constants.
CHEN_HOU_C_L = 3.00649898
CHEN_HOU_C_OMEGA = -1.02942516


def critical_s(beta):
    """s_c = 1/(2 beta) -- the dissipation exponent at which the blow-up stops winning.

    The invariant form of Route-F's s_c = alpha/2.  beta is the COLLAPSE EXPONENT
    of L ~ (T-t)^beta, which is what survives the change of model; alpha was the
    1D profile's far-field decay exponent, which does not.
    """
    return 0.5 / np.asarray(beta, float)


def relevance_exponent(s, beta):
    """p in  D/N ~ (T-t)^p.  Positive p = dissipation is asymptotically irrelevant."""
    return 1.0 - 2.0 * np.asarray(s, float) * np.asarray(beta, float)


def relevance_exponent_buoyancy(s, beta):
    """The SAME p, derived in the theta equation instead of the omega equation.

    Put the dissipation on the buoyancy rather than the vorticity -- kappa(-Delta)^s theta
    instead of nu(-Delta)^s omega -- and redo the count.  From omega_t ~ theta_x with
    omega ~ (T-t)^{-1} and L ~ (T-t)^beta, theta ~ (T-t)^{beta-2}.  Then

        theta_t          ~ (T-t)^{beta-3}
        kappa theta/L^2s ~ kappa (T-t)^{beta-2-2 s beta}
        ratio            ~ kappa (T-t)^{1 - 2 s beta}

    -- identical.  So the criticality condition does NOT depend on which field carries the
    dissipation, which is the strongest statement available that s_c is a property of the
    COLLAPSE and not of a modelling choice about where to put the damping.  (In 3D NS the
    question does not even arise: one viscosity damps everything.)  Kept as a function
    rather than a comment so that the identity is gated rather than asserted.
    """
    return 1.0 - 2.0 * np.asarray(s, float) * np.asarray(beta, float)


def collapse_exponent_from_rescaling(c_l, c_omega):
    """beta = -c_l/c_omega, from the dynamic-rescaling ODEs.  Two lines, exact.

    With omega~(x,tau) = C_omega(tau) omega(C_l(tau) x, t) and dt/dtau = C_omega, the
    rescaled system  omega_tau + (c_l x + u).grad omega = theta_x + c_omega omega
    holds with  c_omega = d log C_omega/dtau  and  c_l = -d log C_l/dtau.  At a fixed
    point both are constants, so C_omega ~ e^{c_omega tau} and C_l ~ e^{-c_l tau}.
    Then T - t = int_tau^inf C_omega dtau' ~ C_omega/|c_omega|, i.e.

        (T - t) ~ C_omega ,    L ~ C_l ~ (T-t)^{-c_l/c_omega} ,

    which is beta, and the physical amplitude 1/C_omega ~ (T-t)^{-1} comes out for
    free (the consistency check that the gauge is the blow-up gauge).

    THE FAR-FIELD EXPONENT IS THE SAME FACT.  Requiring that the outer solution be
    time-independent -- omega_phys(y) ~ (y/C_l)^{alpha}/C_omega independent of tau --
    gives alpha c_l = c_omega, i.e. alpha = c_omega/c_l = -1/beta.  So "the profile
    decays like r^alpha in the far field" and "the length scale collapses like
    (T-t)^beta" are one statement, in 1D and 2D alike.
    """
    return -np.asarray(c_l, float) / np.asarray(c_omega, float)


def chen_hou_beta():
    """beta = 2.92056 for the Chen-Hou 2D Boussinesq profile (published constants)."""
    return float(collapse_exponent_from_rescaling(CHEN_HOU_C_L, CHEN_HOU_C_OMEGA))


def houluo_sharp_ic(n):
    """The Phase-1 ground-truth grower (`smooth_sharp`), projected onto the Hou-Luo
    parity class.  Verbatim the IC that the Phase-1 axis screen labelled as blowing
    up (amp > 100) -- reused rather than re-tuned so that this leg inherits a run
    whose growth was established by an earlier, unrelated experiment."""
    X, Y = grid2d(n)
    w0 = project_odd_odd(0.2 * np.sin(X) * np.sin(Y))
    th0 = project_even_odd((1.0 + np.cos(2 * X)) * np.sin(2 * Y))
    return w0, th0


class FractionalBoussinesq:
    """Pseudo-spectral 2D Boussinesq with (-Delta)^s dissipation on the vorticity.

    RK4 on the inviscid terms with 2/3-rule dealiasing; the dissipation is an EXACT
    integrating factor exp(-nu |k|^{2s} dt), so the s-dependence enters as a diagonal
    multiplier and carries no scheme error of its own.  That is not a nicety: the
    whole leg is about the SIZE of the dissipation term, which must therefore not be
    the term with the largest discretization error.

    theta is transported without diffusion (kappa = 0), matching the Euler-type
    scenario -- the NS analogue dissipates the vorticity, not the buoyancy.
    """

    def __init__(self, n=512, nu=0.0, s=1.0, dt_frac=0.05, cfl=0.4, dt_max=1e-2,
                 symmetry=True):
        self.n = int(n)
        self.nu = float(nu)
        self.s = float(s)
        self.dt_frac = float(dt_frac)
        self.cfl = float(cfl)
        self.dt_max = float(dt_max)
        self.symmetry = bool(symmetry)
        self.KX, self.KY, self.Ksq, self.inv_Ksq = wavenumbers2d(self.n)
        self.mask = dealias_mask2d(self.n)
        self.kmag = np.sqrt(self.Ksq)
        self.visc = self.Ksq ** self.s          # |k|^{2s}
        self.visc[0, 0] = 0.0                   # the mean is not dissipated
        self.dx = TWO_PI / self.n

    # -- pieces ------------------------------------------------------------
    def _rhs(self, w_hat, th_hat):
        """The INVISCID right-hand side only (dissipation is the integrating factor)."""
        u, v = velocity_from_vorticity(w_hat, self.KX, self.KY, self.inv_Ksq)
        wx = np.fft.ifft2(1j * self.KX * w_hat).real
        wy = np.fft.ifft2(1j * self.KY * w_hat).real
        tx = np.fft.ifft2(1j * self.KX * th_hat).real
        ty = np.fft.ifft2(1j * self.KY * th_hat).real
        dw = -np.fft.fft2(u * wx + v * wy) * self.mask + 1j * self.KX * th_hat
        dth = -np.fft.fft2(u * tx + v * ty) * self.mask
        return dw, dth, u, v

    def terms(self, w_hat, th_hat):
        """(driving, dissipative) pointwise -- the two things being compared.

        `driving` is the full inviscid RHS of the omega equation, -u.grad omega +
        theta_x, mirroring Route-F's `nl`.  At the peak of |omega| the advective
        piece vanishes identically (grad omega = 0 there), so what the ratio actually
        compares is the BUOYANCY FORCING against the dissipation -- which is the
        right comparison for this system, since theta_x is the entire singular
        mechanism.  Both pieces are returned so the claim can be checked rather than
        asserted.
        """
        u, v = velocity_from_vorticity(w_hat, self.KX, self.KY, self.inv_Ksq)
        wx = np.fft.ifft2(1j * self.KX * w_hat).real
        wy = np.fft.ifft2(1j * self.KY * w_hat).real
        adv = -(u * wx + v * wy)
        buo = np.fft.ifft2(1j * self.KX * th_hat).real
        dis = -self.nu * np.fft.ifft2(self.visc * w_hat).real
        return adv + buo, dis, adv, buo

    def tail_fraction(self, w_hat):
        """The under-resolution guard, exposed so it can be tested against a case
        known to be resolved and one known not to be (banked lesson 55: a guard that
        can return "perfect" by construction is worse than no guard)."""
        k_cut = self.n / 3.0
        band_mask = (self.kmag > 0.9 * k_cut) & (self.kmag <= k_cut)
        pk = np.abs(w_hat) ** 2
        band = pk[band_mask]
        return float(band.max() / (pk.max() + 1e-300)) if band.size else 0.0

    def dt_stable(self, w, u, v):
        """Advective CFL + an amplitude cap.  The viscous part is exact and absent."""
        umax = max(float(np.abs(u).max()), float(np.abs(v).max())) + 1e-300
        amp = float(np.abs(w).max()) + 1e-300
        return min(self.dt_max, self.cfl * self.dx / umax, self.dt_frac / amp)

    def _project(self, w_hat, th_hat):
        if not self.symmetry:
            return w_hat, th_hat
        w = project_odd_odd(np.fft.ifft2(w_hat).real)
        th = project_even_odd(np.fft.ifft2(th_hat).real)
        return np.fft.fft2(w) * self.mask, np.fft.fft2(th) * self.mask

    # -- the run -----------------------------------------------------------
    def run(self, w0, th0, t_end=np.inf, amp_factor=1e4, max_steps=200000,
            sample_every=10, tail_max=1e-2, wall_max=np.inf):
        """Integrate until max|omega| grows by `amp_factor`, or the resolution guard
        fires, or a cap is hit.

        Records at each sample: amplitude, three length-scale diagnostics, the
        term ratio at the peak, and the spectral tail fraction.

        UNDER-RESOLUTION GUARD (banked lesson 55, inherited from Route-F): the guard
        is the amplitude AT THE CUTOFF relative to the peak, NOT the energy in a
        broad high band.  Two of Route-F's three candidate definitions were silently
        degenerate -- one identically zero because the 2/3 rule had already emptied
        the band it measured, one identically fat because a near-singular spectrum
        genuinely is broad.  When it fires the run REFUSES ("under_resolved") rather
        than returning a number computed off an unresolved state; the history up to
        that point is still resolved and is returned.
        """
        w_hat = np.fft.fft2(np.asarray(w0, float)) * self.mask
        th_hat = np.fft.fft2(np.asarray(th0, float)) * self.mask
        w_hat, th_hat = self._project(w_hat, th_hat)
        amp0 = float(np.abs(np.fft.ifft2(w_hat).real).max())
        if amp0 == 0.0:
            raise ValueError("omega0 is identically zero")

        t, t0 = 0.0, time.perf_counter()
        ts, amps, ratios, tails = [], [], [], []
        Lx, Ly, Lg, Lk = [], [], [], []
        outcome, steps = "max_steps", 0

        e = e2 = None
        last_dt = None
        for steps in range(1, int(max_steps) + 1):
            w = np.fft.ifft2(w_hat).real
            k1 = self._rhs(w_hat, th_hat)
            dt = self.dt_stable(w, k1[2], k1[3])
            if t + dt > t_end:
                dt = t_end - t
            if dt <= 0:
                outcome = "t_end"
                break
            if dt != last_dt:
                e = np.exp(-self.nu * self.visc * dt)
                e2 = np.exp(-self.nu * self.visc * dt * 0.5)
                last_dt = dt
            # RK4 in the integrating-factor variable (identical structure to the 1D
            # module, so the two legs share a scheme as well as a diagnostic).
            k2 = self._rhs(e2 * (w_hat + 0.5 * dt * k1[0]), th_hat + 0.5 * dt * k1[1])
            k3 = self._rhs(e2 * w_hat + 0.5 * dt * k2[0], th_hat + 0.5 * dt * k2[1])
            k4 = self._rhs(e * w_hat + dt * e2 * k3[0], th_hat + dt * k3[1])
            w_hat = (e * (w_hat + dt * (k1[0] + 2 * k2[0]) / 6.0)
                     + dt * (2 * e2 * k3[0] + k4[0]) / 6.0)
            th_hat = th_hat + dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
            w_hat, th_hat = self._project(w_hat, th_hat)
            t += dt

            if not np.all(np.isfinite(w_hat)):
                outcome = "diverged"
                break
            if steps % int(sample_every) == 0:
                w = np.fft.ifft2(w_hat).real
                aw = np.abs(w)
                amp = float(aw.max())
                idx = np.unravel_index(int(np.argmax(aw)), aw.shape)
                wx = np.fft.ifft2(1j * self.KX * w_hat).real
                wy = np.fft.ifft2(1j * self.KY * w_hat).real
                drv, dis, _, _ = self.terms(w_hat, th_hat)
                ts.append(t)
                amps.append(amp)
                # ANISOTROPIC length scales: dissipation is set by the SMALLEST one.
                Lx.append(amp / (float(np.abs(wx).max()) + 1e-300))
                Ly.append(amp / (float(np.abs(wy).max()) + 1e-300))
                Lg.append(amp / (float(np.sqrt(wx ** 2 + wy ** 2).max()) + 1e-300))
                pk = np.abs(w_hat) ** 2
                Lk.append(float(pk.sum() / ((self.kmag * pk).sum() + 1e-300)))
                ratios.append(abs(dis[idx]) / (abs(drv[idx]) + 1e-300))
                tails.append(self.tail_fraction(w_hat))
                if tails[-1] > tail_max:
                    outcome = "under_resolved"
                    break
                if amp > amp_factor * amp0:
                    outcome = "blowup_candidate"
                    break
                if amp < 0.05 * amp0:
                    outcome = "decayed"
                    break
                if time.perf_counter() - t0 > wall_max:
                    outcome = "wall_max"
                    break
            if t >= t_end:
                outcome = "t_end"
                break

        return {"outcome": outcome, "t": np.array(ts), "amp": np.array(amps),
                "ratio": np.array(ratios), "tail": np.array(tails),
                "Lx": np.array(Lx), "Ly": np.array(Ly), "Lgrad": np.array(Lg),
                "Lspec": np.array(Lk), "t_final": t, "steps": steps,
                "amp0": amp0, "n": self.n, "nu": self.nu, "s": self.s,
                "wall_seconds": time.perf_counter() - t0,
                "max_tail": float(max(tails)) if tails else 0.0}


# --------------------------------------------------------------------------
def _window_mask(res, lo, hi):
    """Select by fraction of the LOG-AMPLITUDE range, so the window follows the
    collapse rather than the clock (identical convention to Route-F)."""
    amp = res["amp"]
    g = np.log(amp / amp[0]) / np.log(amp[-1] / amp[0] + 1e-300)
    return (g > lo) & (g < hi)


def estimate_T(res, lo=0.55, hi=1.0):
    """Blow-up time from the run itself: 1/amp is LINEAR in t for omega ~ 1/(T-t).

    Route-F v1 learned this the expensive way -- dissipation DELAYS the blow-up, so
    using an inviscid T in the fit biases every exponent in the same direction with
    a shallower slope, which is the signature of a wrong singular time rather than a
    wrong exponent (banked lesson 54).  T is therefore re-estimated per run.
    """
    amp, t = res["amp"], res["t"]
    if amp.size < 8:
        return float("nan")
    m = _window_mask(res, lo, hi)
    if m.sum() < 4:
        return float("nan")
    c = np.polyfit(t[m], 1.0 / amp[m], 1)
    return float(-c[1] / c[0]) if c[0] < 0 else float("nan")


def fit_collapse(res, T, lo=0.40, hi=0.94, keys=("Lx", "Ly", "Lgrad", "Lspec")):
    """beta from L ~ (T-t)^beta, per length diagnostic, plus the amplitude exponent.

    The amplitude exponent is a GATE, not an output: the derivation assumes
    omega ~ (T-t)^{-1}, so a run whose measured amplitude exponent is far from -1 is
    not in the regime the prediction is about, and its beta means nothing.
    """
    t, amp = res["t"], res["amp"]
    m = _window_mask(res, lo, hi) & (T - res["t"] > 0)
    out = {"n_points": int(m.sum())}
    if m.sum() < 5:
        return {**out, **{k: float("nan") for k in keys}, "amp_exponent": float("nan")}
    x = np.log(T - t[m])
    for k in keys:
        out[k] = float(np.polyfit(x, np.log(res[k][m]), 1)[0])
    out["amp_exponent"] = float(np.polyfit(x, np.log(amp[m]), 1)[0])
    # beta_max is the FASTEST-collapsing direction and only exists when both directional
    # diagnostics were asked for -- callers that want a single length scale (e.g.
    # collapse_window_report, which sweeps windows on Lgrad alone) pass one key.
    if "Lx" in out and "Ly" in out:
        out["beta_max"] = max(out["Lx"], out["Ly"])
    return out


def collapse_window_report(res, T, min_decades=1.5, max_spread=0.25,
                           windows=((0.40, 0.70), (0.55, 0.85), (0.70, 0.98))):
    """Is this run entitled to quote a collapse exponent at all?  REFUSES if not.

    Route-F's 1D runs grew by 1e4 and spanned nearly four decades of (T-t); a fit over
    that has something to converge to.  A uniform-grid 2D run of the same object grows
    by ~90x before the spectral guard fires, which is UNDER ONE DECADE of (T-t), and
    over that span beta measured on three sub-windows moves by more than a factor of
    two.  Quoting a beta from it would be quoting the window.

    So this is a gate and not a diagnostic: it returns `measurable=False` with the two
    numbers that make the call, and the callers treat beta as absent (banked lesson 45
    -- an unknown ledger entry must be None, never a number, and the assembly must
    refuse).  The repair is not more grid; it is a different instrument (dynamic
    rescaling, where the collapse exponent is a MODULATION CONSTANT and no fit, no
    window and no singular-time estimate enter at all).
    """
    t = res["t"]
    m = _window_mask(res, 0.40, 0.94) & (T - t > 0)
    if m.sum() < 5 or not np.isfinite(T):
        return {"measurable": False, "reason": "too few points", "decades": 0.0,
                "beta_spread": float("inf")}
    span = (T - t[m])
    decades = float(np.log10(span[0] / span[-1]))
    betas = []
    for lo, hi in windows:
        f = fit_collapse(res, T, lo=lo, hi=hi, keys=("Lgrad",))
        if np.isfinite(f["Lgrad"]):
            betas.append(f["Lgrad"])
    spread = (float(max(betas) - min(betas)) / abs(np.mean(betas))
              if len(betas) >= 2 else float("inf"))
    ok = (decades >= min_decades) and (spread <= max_spread)
    return {"measurable": bool(ok), "decades": decades, "beta_spread": spread,
            "betas_by_window": [float(b) for b in betas],
            "growth": float(res["amp"][-1] / res["amp0"]),
            "reason": "" if ok else
            (f"only {decades:.2f} decades of (T-t) (need {min_decades}); "
             f"beta moves {spread * 100:.0f}% across sub-windows (allow "
             f"{max_spread * 100:.0f}%)")}


def fit_relevance(res, T, lo=0.40, hi=0.94):
    """Fit  D/N ~ (T-t)^p  over an interior window of the run.

    THE WINDOW IS THE DOMINANT SYSTEMATIC AND IS SWEPT, NOT CHOSEN (Route-F F7).
    p = 1 - 2 beta s is an ASYMPTOTIC statement, so an early window has not reached
    it and a very late one is noise-dominated.  The SLOPE of p against s is much more
    robust than any single p, because every s shares the window and the bias largely
    cancels in the difference -- which is why the claims are about the slope and the
    zero crossing, with the window sweep quoted as the error bar.
    """
    amp, t, r = res["amp"], res["t"], res["ratio"]
    if amp.size < 8:
        return {"p": float("nan"), "n_points": int(amp.size)}
    m = _window_mask(res, lo, hi) & (r > 0) & (T - t > 0)
    if m.sum() < 5:
        return {"p": float("nan"), "n_points": int(m.sum())}
    c = np.polyfit(np.log(T - t[m]), np.log(r[m]), 1)
    resid = np.log(r[m]) - np.polyval(c, np.log(T - t[m]))
    return {"p": float(c[0]), "n_points": int(m.sum()),
            "fit_rms": float(np.sqrt(np.mean(resid ** 2))),
            "window_amp": [float(amp[m][0]), float(amp[m][-1])]}
