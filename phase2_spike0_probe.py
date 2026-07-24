"""Exploratory v3: dynamic rescaling on CLM (a=0) with INTEGRAL modulation.

Rescaled PDE:  W_tau = -beta W + delta*y*W_y + W*HW
Robust modulation from conserving  I2=int W^2  and  J2=int W_y^2  (no fragile
pointwise high derivatives):
    2*beta + delta = R1 = 2*int(W^2 HW)/int(W^2)
    2*beta - delta = R2 = -2*int(W_yy W HW)/int(W_y^2)
    => beta=(R1+R2)/4,  delta=(R1-R2)/2
Known CLM answer (w0=-sin x): blowup at x=0, T*=2, self-similar exponents
    beta -> 1,  delta -> -1,  profile Phi ~ -4y/(1+4y^2).
"""
import numpy as np
import sys
sys.path.insert(0, "/home/andy/projects/Unsolved")
from solver.spectral_utils import grid, wavenumbers, hilbert_hat, dealias_mask

def dpow(w_hat, k, p):
    return (1j * k) ** p * w_hat

def run(N=2048, dtau=1e-3, tau_max=12.0, report_every=500):
    x = grid(N)
    yc = np.where(x > np.pi, x - 2 * np.pi, x)
    k = wavenumbers(N)
    mask = dealias_mask(N)
    W = -np.sin(x)

    def diag(Wf):
        Wh = np.fft.rfft(Wf)
        HW = np.fft.irfft(hilbert_hat(Wh, k), N)
        W_y = np.fft.irfft(dpow(Wh, k, 1), N)
        W_yy = np.fft.irfft(dpow(Wh, k, 2), N)
        I2 = np.mean(Wf * Wf)
        J2 = np.mean(W_y * W_y)
        R1 = 2 * np.mean(Wf * Wf * HW) / I2
        R2 = -2 * np.mean(W_yy * Wf * HW) / J2
        beta = (R1 + R2) / 4.0
        delta = (R1 - R2) / 2.0
        return beta, delta, W_y, HW, I2, J2

    def rhs(Wf):
        beta, delta, W_y, HW, _, _ = diag(Wf)
        P = np.fft.irfft(np.fft.rfft(Wf * HW) * mask, N)
        return P - beta * Wf + delta * yc * W_y, beta, delta

    print(f"{'tau':>6} {'beta':>9} {'delta':>9} {'maxW':>8} {'peak_y':>7} "
          f"{'int W2':>9} {'edge|W|':>8} {'B_fit':>8}")
    tau = 0.0; step = 0
    while tau < tau_max:
        k1, beta, delta = rhs(W)
        k2, *_ = rhs(W + 0.5 * dtau * k1)
        k3, *_ = rhs(W + 0.5 * dtau * k2)
        k4, *_ = rhs(W + dtau * k3)
        W = W + (dtau / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        tau += dtau; step += 1
        if step % report_every == 0:
            b, d, _, _, I2, _ = diag(W)
            am = np.argmax(np.abs(W))
            m = np.abs(yc) < 1.0
            yy = yc[m]; Wm = W[m]
            p_now = np.fft.irfft(dpow(np.fft.rfft(W), k, 1), N)[0]
            num = np.sum((p_now * yy - Wm) * (Wm * yy**2)); den = np.sum((Wm * yy**2)**2)
            B = num / den if den > 0 else np.nan
            print(f"{tau:6.2f} {b:9.5f} {d:9.5f} {np.max(np.abs(W)):8.4f} "
                  f"{yc[am]:7.3f} {2*np.pi*I2:9.4f} {abs(W[N//2]):8.4f} {B:8.3f}")

if __name__ == "__main__":
    run()
