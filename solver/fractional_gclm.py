"""gCLM with fractional dissipation -- the Clay question in miniature.

ROUTE F v1.  Ranked item (2) of "what would actually be worthwhile": take a blow-up
that exists, add dissipation, and find the scaling at which dissipation kills it.
That is the only item on the list which probes the ACTUAL obstruction between a
toy-model certificate and Navier-Stokes, rather than polishing the toy.

    omega_t + a u omega_x = omega u_x - nu (-Delta)^s omega ,     u_x = H(omega)

on a 2 pi-periodic domain.  s = 1 is the ordinary Laplacian; s is the dial.

--------------------------------------------------------------------------
THE CRITICALITY CONDITION, AND WHY IT IS EXACTLY alpha/2
--------------------------------------------------------------------------
A self-similar blow-up has omega ~ (T-t)^{-1} and a length scale L ~ (T-t)^beta.
Route-E v1 computed beta for this family without knowing it was going to be needed
here.  In the dynamically-rescaled variables of solver/rescaled_spectrum.py, with
c_l = 1 and the amplitude gauge, the two rescaling ODEs

    A'/A^2 = -c_omega ,      L'/(L A) = -c_l

integrate to  A ~ 1/(alpha (T-t))  and  L ~ (T-t)^{c_l/alpha},  where
alpha = -c_omega is the profile's FAR-FIELD DECAY EXPONENT, Omega ~ X^{-alpha}.
So with c_l = 1,

    **beta = 1 / alpha .**

Now compare the two terms at the blow-up scale.  The nonlinearity is ~ omega^2 and
the dissipation is ~ nu omega / L^{2s}, so

    dissipation / nonlinearity  ~  nu / (omega L^{2s})  ~  nu (T-t)^{1 - 2 s beta} .

Dissipation is asymptotically NEGLIGIBLE -- the blow-up beats it -- exactly when
1 - 2 s beta > 0, i.e.

    **s  <  s_c(a) = 1 / (2 beta) = alpha(a) / 2 .**                          (SC)

Two things make (SC) worth measuring rather than just asserting.

* **It is a statement about s, not about nu.**  For s < s_c the blow-up survives
  EVERY nu > 0 (the ratio vanishes as t -> T); for s > s_c dissipation eventually
  dominates for every nu > 0.  So the transition location must be nu-INDEPENDENT,
  and that is the experiment's own control: a transition that moves with nu is not
  this mechanism.
* **It says where the Navier-Stokes difficulty lives.**  NS's natural scaling is
  L ~ (T-t)^{1/2}, i.e. beta = 1/2, i.e. alpha = 2 -- for which the Laplacian s = 1
  sits EXACTLY at s_c.  Navier-Stokes is critical, which is the whole problem.  In
  this family alpha is a measured function of a, so the same arithmetic says
  **alpha > 2 (measured: a >~ 0.39) puts the full Laplacian STRICTLY BELOW s_c** --
  a toy blow-up that beats ordinary viscosity.  Stated as arithmetic about gCLM,
  not as a claim about NS: gCLM's scaling is not NS's, and the whole reason NS is
  hard is that its own alpha is pinned at 2 by dimensional analysis rather than
  being free to move.

--------------------------------------------------------------------------
WHAT THIS MODULE MEASURES, AND WHY NOT "DID IT BLOW UP"
--------------------------------------------------------------------------
A binary blow-up test near a critical exponent is exactly the kind of measurement
this project has learned not to trust: close to s_c the blow-up is only
ASYMPTOTICALLY dissipation-free, so at finite compute the apparent transition is
biased and resolution-dependent.  The primary diagnostic here is quantitative
instead:

    RELEVANCE EXPONENT.  Track  D/N := (dissipation term)/(nonlinear term) at the
    peak, and fit  D/N ~ (T - t)^p.  Prediction: **p = 1 - 2 s / alpha**, which
    crosses zero at s = alpha/2.  Measuring p across s gives a LINE whose zero
    locates s_c, instead of a threshold located by eye.

The binary test is kept as a secondary check, with the nu-independence control.

--------------------------------------------------------------------------
THE KNOWN ANSWER (the gate everything else hangs from)
--------------------------------------------------------------------------
At a = 0 the inviscid model is EXACTLY solvable, on the circle as well as the line:
with z = H(omega) + i omega,  z_t = z^2 / 2,  so

    **z(x, t) = z_0(x) / (1 - t z_0(x)/2)** ,     omega = Im z ,

verified here against a fine RK4 integration to 1.8e-14.  Blow-up occurs at
T = 2 / max{ H(omega_0) : omega_0 = 0 }.  And alpha(0) = 1 exactly (Route-E v1's
anchor, Omega = -2X/(1+X^2)), so (SC) predicts **s_c(0) = 1/2** -- a number the
literature on dissipative CLM also has, which makes a = 0 a genuine known-answer
gate rather than a self-consistency check.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np

from solver.spectral_utils import (
    TWO_PI, dealias_mask, derivative_hat, hilbert_hat, velocity_hat, wavenumbers,
)


def critical_s(alpha):
    """s_c = alpha/2 -- the dissipation exponent at which the blow-up stops winning."""
    return 0.5 * np.asarray(alpha, float)


def relevance_exponent(s, alpha):
    """p in  D/N ~ (T-t)^p.  Positive p = dissipation is asymptotically irrelevant."""
    return 1.0 - 2.0 * np.asarray(s, float) / np.asarray(alpha, float)


# --------------------------------------------------------------------------
def clm_exact(omega0, t, k=None):
    """The exact a = 0, nu = 0 solution on the circle: omega = Im[z0/(1 - t z0/2)].

    Gate 1 checks this against RK4; it is also what the dissipative runs are
    measured AGAINST, so that "the blow-up survived" is a comparison with a known
    object rather than an impression from a growing maximum.
    """
    n = omega0.size
    if k is None:
        k = wavenumbers(n)
    u0 = np.fft.irfft(hilbert_hat(np.fft.rfft(omega0), k), n)
    z0 = u0 + 1j * omega0
    return np.imag(z0 / (1.0 - 0.5 * float(t) * z0))


def clm_blowup_time(omega0, k=None):
    """T = 2 / max{H(omega0) : omega0 = 0}, by interpolating the zeros of omega0."""
    n = omega0.size
    if k is None:
        k = wavenumbers(n)
    u0 = np.fft.irfft(hilbert_hat(np.fft.rfft(omega0), k), n)
    w = np.concatenate([omega0, omega0[:1]])
    u = np.concatenate([u0, u0[:1]])
    best = -np.inf
    for i in range(n):
        if w[i] == 0.0:
            best = max(best, u[i])
        elif w[i] * w[i + 1] < 0.0:
            th = w[i] / (w[i] - w[i + 1])
            best = max(best, u[i] + th * (u[i + 1] - u[i]))
    return 2.0 / best if best > 0 else np.inf


# --------------------------------------------------------------------------
class FractionalGCLM:
    """Pseudo-spectral gCLM with (-Delta)^s dissipation, 2 pi-periodic.

    RK4 on the nonlinearity with 2/3-rule dealiasing, and the dissipation applied
    as an EXACT integrating factor exp(-nu |k|^{2s} dt) after each step -- so the
    s-dependence enters through a diagonal multiplier and carries no scheme error
    of its own.  That matters here: the whole leg is about the size of the
    dissipation term, so it must not be the thing with the largest discretization
    error.
    """

    # DOMAIN GUARD (bench repair, leg 91's finding).  Both bounds are the literature's,
    # not this file's taste: the dissipative-gCLM corpus writes the dissipation as
    # Lambda^sigma-hat = |k|^sigma with sigma = 2 s, and works at sigma >= 0 throughout --
    # the lowest exponent anyone treats is the "marginal" sigma = 0 (the Oldroyd-B stress
    # reading), which is why **s = 0 is ADMISSIBLE and is not rejected here**.  Below that
    # the object is not a weak dissipation, it is a different operator: for a negative
    # exponent |k|^{2s} is singular at k = 0 and Riesz-potential theory says the multiplier
    # is not well defined there at all.  The `self.visc[0] = 0.0` line below -- written for
    # the correct physical reason that the mean is not dissipated -- would OVERWRITE that
    # inf, which is precisely the signal that the operator is ill-defined, and what survived
    # was a finite multiplier DECREASING in |k|: a smoothing operator wearing the
    # dissipation's name.  Leg 91 measured what that costs: the pipeline ran to completion
    # and returned a finite, plausible-looking p (+2.1864 at s = -0.5), which, injected into
    # the p(s) fit whose zero crossing IS the measured s_c, moved that crossing by -0.07% at
    # s = -0.5 and +13.33% at s = -2.0 -- with no exception, no warning, and no field of the
    # returned dict recording it.  A negative nu is the same failure on the other input: an
    # energy SOURCE wearing the dissipation's name, +6.38% on p, equally silent.
    #
    # There is no published UPPER bound on sigma, so none is imposed: the only upper wall is
    # float64's own overflow of |k|^{2s}, and the module already refuses there correctly
    # (visc goes non-finite, the run's isfinite check breaks out, p = nan).  Likewise NaN
    # inputs already propagate correctly and are deliberately left to do so -- they are not
    # converted into exceptions here.  This guard closes the LOW side only, which is where
    # the gap was.
    def __init__(self, n=2048, a=0.0, nu=0.0, s=1.0, dt_frac=0.02):
        self.n = int(n)
        self.dt_frac = float(dt_frac)
        self.a = float(a)
        self.nu = float(nu)
        self.s = float(s)
        if self.s < 0.0:
            raise ValueError(
                "s = %r is outside the admissible dissipation range: the operator is "
                "(-Delta)^s with symbol |k|^{2s}, and sigma = 2 s >= 0 is required "
                "(s = 0, the marginal case, IS admissible). For s < 0 the symbol is "
                "singular at k = 0 and |k|^{2s} is not a dissipation at all -- it "
                "decreases in |k|." % self.s)
        if self.nu < 0.0:
            raise ValueError(
                "nu = %r is a negative dissipation strength -- anti-dissipation, an "
                "energy source, not a viscosity. nu >= 0 is required (nu = 0, the "
                "inviscid case, IS admissible)." % self.nu)
        self.x = np.arange(self.n) * TWO_PI / self.n
        self.k = wavenumbers(self.n)
        self.mask = dealias_mask(self.n)
        self.visc = np.abs(self.k).astype(float) ** (2.0 * self.s)
        self.visc[0] = 0.0                       # the mean is not dissipated

    # -- pieces ------------------------------------------------------------
    def hilbert(self, w):
        return np.fft.irfft(hilbert_hat(np.fft.rfft(w), self.k), self.n)

    def _rhs(self, w_hat):
        """The NONLINEAR right-hand side only (dissipation is the integrating factor)."""
        w = np.fft.irfft(w_hat, self.n)
        u_x = np.fft.irfft(hilbert_hat(w_hat, self.k), self.n)
        out = w * u_x
        if self.a != 0.0:
            u = np.fft.irfft(velocity_hat(w_hat, self.k), self.n)
            w_x = np.fft.irfft(derivative_hat(w_hat, self.k, self.n), self.n)
            out = out - self.a * u * w_x
        return np.fft.rfft(out) * self.mask

    def terms(self, w):
        """(nonlinear, dissipative) pointwise -- the two things being compared."""
        w_hat = np.fft.rfft(w)
        u_x = np.fft.irfft(hilbert_hat(w_hat, self.k), self.n)
        nl = w * u_x
        if self.a != 0.0:
            u = np.fft.irfft(velocity_hat(w_hat, self.k), self.n)
            w_x = np.fft.irfft(derivative_hat(w_hat, self.k, self.n), self.n)
            nl = nl - self.a * u * w_x
        dis = -self.nu * np.fft.irfft(self.visc * w_hat, self.n)
        return nl, dis

    def dt_stable(self, w):
        """Advective + amplitude CFL.  The viscous part is exact, so it is not in it."""
        amp = float(np.max(np.abs(w))) + 1e-300
        dt = self.dt_frac / amp
        if self.a != 0.0:
            u = self.hilbert(w) * 0.0
            u = np.fft.irfft(velocity_hat(np.fft.rfft(w), self.k), self.n)
            umax = float(np.max(np.abs(u))) + 1e-300
            dt = min(dt, 0.3 * (TWO_PI / self.n) / (abs(self.a) * umax))
        return dt

    # -- the run -----------------------------------------------------------
    def run(self, w0, t_end=np.inf, amp_factor=1e4, max_steps=2000000,
            sample_every=5, tail_max=1e-2):
        """Integrate until max|omega| grows by `amp_factor`, or t_end, or max_steps.

        Records max|omega|, the two term sizes at the peak, and the spectral tail
        fraction (the under-resolution guard: if the last third of the spectrum
        carries a non-negligible share of the energy, the run is not resolved and
        the result is reported as such rather than used).
        """
        w = np.asarray(w0, float).copy()
        w_hat = np.fft.rfft(w)
        amp0 = float(np.max(np.abs(w)))
        t = 0.0
        ts, amps, ratios, tails = [], [], [], []
        outcome, steps = "max_steps", 0
        # UNDER-RESOLUTION GUARD, and it took two tries to define honestly.
        #  * Energy above 2/3 of k_max reads exactly 0.0 at some n and not others,
        #    because the 2/3 dealiasing rule has already zeroed that band and
        #    whether it lands inside the cutoff depends on rounding in n.  A guard
        #    that is zero by construction reads as "perfectly resolved".
        #  * Energy above n/6 reads ~0.37 for every run, resolved or not: a
        #    near-singular solution genuinely has a fat spectrum, so a broad band
        #    measures the physics rather than the discretization.
        # What actually discriminates is the amplitude AT THE CUTOFF relative to the
        # peak: the top 10% of the KEPT band against the largest mode.  The
        # resolution ladder (F5) remains the real check; this is the cheap proxy
        # that can reject a run in flight.
        k_cut = self.n / 3.0
        hi = int(np.searchsorted(self.k, 0.9 * k_cut))
        keep = self.k <= k_cut
        for steps in range(1, int(max_steps) + 1):
            dt = self.dt_stable(w)
            if t + dt > t_end:
                dt = t_end - t
            if dt <= 0:
                outcome = "t_end"
                break
            e = np.exp(-self.nu * self.visc * dt)
            e2 = np.exp(-self.nu * self.visc * dt * 0.5)
            k1 = self._rhs(w_hat)
            k2 = self._rhs(e2 * (w_hat + 0.5 * dt * k1))
            k3 = self._rhs(e2 * w_hat + 0.5 * dt * k2)
            k4 = self._rhs(e * w_hat + dt * e2 * k3)
            w_hat = (e * (w_hat + dt * (k1 + 2 * k2) / 6.0)
                     + dt * (2 * e2 * k3 + k4) / 6.0)
            w = np.fft.irfft(w_hat, self.n)
            t += dt
            if not np.all(np.isfinite(w)):
                outcome = "diverged"
                break
            if steps % int(sample_every) == 0:
                amp = float(np.max(np.abs(w)))
                i = int(np.argmax(np.abs(w)))
                nl, dis = self.terms(w)
                ts.append(t)
                amps.append(amp)
                ratios.append(abs(dis[i]) / (abs(nl[i]) + 1e-300))
                pk = np.abs(w_hat) ** 2
                band = pk[hi:][keep[hi:]]
                tails.append(float(band.max() / (pk.max() + 1e-300))
                             if band.size else 0.0)
                if tails[-1] > tail_max:
                    # REFUSE rather than return a number off an unresolved state
                    # (banked lesson 45).  The recorded history up to here is
                    # resolved and usable; the run simply stops being trustworthy.
                    outcome = "under_resolved"
                    break
                if amp > amp_factor * amp0:
                    outcome = "blowup_candidate"
                    break
                if amp < 0.05 * amp0:
                    outcome = "decayed"
                    break
            if t >= t_end:
                outcome = "t_end"
                break
        return {"outcome": outcome, "t": np.array(ts), "amp": np.array(amps),
                "ratio": np.array(ratios), "tail": np.array(tails),
                "t_final": t, "steps": steps, "omega": w,
                "amp0": amp0, "n": self.n, "a": self.a, "nu": self.nu, "s": self.s,
                "max_tail": float(max(tails)) if tails else 0.0}


# --------------------------------------------------------------------------
def estimate_T(res, lo=0.55, hi=1.0):
    """Blow-up time from the run itself: 1/amp is LINEAR in t for an omega ~ 1/(T-t)
    blow-up, so extrapolate it to zero.

    This matters more than it looks.  Dissipation DELAYS the blow-up, so using the
    inviscid T_0 in the relevance fit biases the exponent -- measured against T_0 the
    zero crossing came out ~10% high, and every point sat above its prediction with a
    shallower slope, which is the signature of a wrong singular time rather than of a
    wrong exponent.
    """
    amp, t = res["amp"], res["t"]
    if amp.size < 8:
        return float("nan")
    g = np.log(amp / amp[0]) / np.log(amp[-1] / amp[0] + 1e-300)
    m = (g >= lo) & (g <= hi)
    if m.sum() < 4:
        return float("nan")
    c = np.polyfit(t[m], 1.0 / amp[m], 1)
    return float(-c[1] / c[0]) if c[0] < 0 else float("nan")


def fit_relevance(res, T, lo=0.40, hi=0.94):
    """Fit  D/N ~ (T-t)^p  over an interior window of the run.

    THE WINDOW IS THE DOMINANT SYSTEMATIC AND IS SWEPT, NOT CHOSEN.  p = 1 - 2s/alpha
    is an ASYMPTOTIC statement, so an early window has not reached it and a very late
    one is noise-dominated.  Measured at a = 0, s = 0.35 (prediction +0.300) the
    single-exponent value runs +0.414 / +0.343 / +0.318 / +0.305 / +0.270 over windows
    0.20-0.80 ... 0.60-0.98 -- a +-0.07 spread that approaches the prediction
    monotonically from above, which is what an asymptotic approach looks like.

    THE SLOPE IS MUCH MORE ROBUST THAN ANY SINGLE EXPONENT, because every s uses the
    same window and the bias largely cancels in the difference: -1.896 / -2.043 /
    -2.068 / -2.074 / -2.001 over the same five windows, i.e. -2.03 +- 0.09 against a
    prediction of exactly -2.  That is why this leg's claims are made about the SLOPE
    and the ZERO CROSSING, with the window sweep quoted as the error bar.

    `lo`/`hi` are fractions of the recorded amplitude range, not of time, so the
    window follows the blow-up rather than the clock.
    """
    amp, t, r = res["amp"], res["t"], res["ratio"]
    if amp.size < 8:
        return {"p": float("nan"), "n_points": int(amp.size)}
    g = np.log(amp / amp[0]) / np.log(amp[-1] / amp[0] + 1e-300)
    m = (g > lo) & (g < hi) & (r > 0) & (T - t > 0)
    if m.sum() < 5:
        return {"p": float("nan"), "n_points": int(m.sum())}
    c = np.polyfit(np.log(T - t[m]), np.log(r[m]), 1)
    resid = np.log(r[m]) - np.polyval(c, np.log(T - t[m]))
    return {"p": float(c[0]), "n_points": int(m.sum()),
            "fit_rms": float(np.sqrt(np.mean(resid ** 2))),
            "window_amp": [float(amp[m][0]), float(amp[m][-1])]}
