"""Exploratory v4: dynamic rescaling on CLM (a=0), periodic, INTEGRAL modulation
+ two stabilizations:
  (S1) dealias the sawtooth product yc*W_y (the y=+-pi wrap injects high-freq noise);
  (S2) explicit exact renormalization of int W^2 each step (amplitude runaway guard).

Rescaled PDE:  W_tau = -beta W + delta*y*W_y + W*HW
Modulation (conserve I2=int W^2, J2=int W_y^2):
    2b+d = R1 = 2 int(W^2 HW)/I2 ;  2b-d = R2 = -2 int(W_yy W HW)/J2
Target (CLM, w0=-sin x): beta->1, delta->-1, Phi = -4y/(1+4y^2), T*=2.
"""
import numpy as np
import sys
sys.path.insert(0, "/home/andy/projects/Unsolved")
from solver.spectral_utils import grid, wavenumbers, hilbert_hat, dealias_mask

def dpow(w_hat, k, p):
    return (1j * k) ** p * w_hat

def run(N=2048, dtau=1e-3, tau_max=20.0, report_every=1000):
    x = grid(N)
    yc = np.where(x > np.pi, x - 2 * np.pi, x)
    k = wavenumbers(N)
    mask = dealias_mask(N)
    W = -np.sin(x)
    I2_0 = np.mean(W * W)

    def deal(f):
        return np.fft.irfft(np.fft.rfft(f) * mask, N)

    def diag(Wf):
        Wh = np.fft.rfft(Wf)
        HW = np.fft.irfft(hilbert_hat(Wh, k), N)
        W_y = np.fft.irfft(dpow(Wh, k, 1), N)
        W_yy = np.fft.irfft(dpow(Wh, k, 2), N)
        I2 = np.mean(Wf * Wf); J2 = np.mean(W_y * W_y)
        R1 = 2 * np.mean(Wf * Wf * HW) / I2
        R2 = -2 * np.mean(W_yy * Wf * HW) / J2
        return (R1 + R2) / 4.0, (R1 - R2) / 2.0, W_y, HW

    def rhs(Wf):
        beta, delta, W_y, HW = diag(Wf)
        return deal(Wf * HW) - beta * Wf + delta * deal(yc * W_y), beta, delta

    print(f"{'tau':>6} {'beta':>9} {'delta':>9} {'maxW':>8} {'peak_y':>7} "
          f"{'edge|W|':>8} {'B_fit':>8} {'d(maxW)':>9}")
    tau = 0.0; step = 0; prev_max = np.max(np.abs(W))
    while tau < tau_max:
        k1, beta, delta = rhs(W)
        k2, *_ = rhs(W + 0.5 * dtau * k1)
        k3, *_ = rhs(W + 0.5 * dtau * k2)
        k4, *_ = rhs(W + dtau * k3)
        W = W + (dtau / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        tau += dtau; step += 1
        # (S3) project onto odd subspace (CLM with odd data stays exactly odd;
        # kills the even-mode drift that migrates the peak to the boundary)
        Wh = np.fft.rfft(W); Wh.real = 0.0; W = np.fft.irfft(Wh, N)
        # (S2) exact int W^2 renorm
        W = W * np.sqrt(I2_0 / np.mean(W * W))
        if step % report_every == 0:
            b, d, _, _ = diag(W)
            am = np.argmax(np.abs(W)); mx = np.max(np.abs(W))
            m = np.abs(yc) < 1.0; yy = yc[m]; Wm = W[m]
            p_now = np.fft.irfft(dpow(np.fft.rfft(W), k, 1), N)[0]
            num = np.sum((p_now * yy - Wm) * (Wm * yy**2)); den = np.sum((Wm * yy**2)**2)
            B = num / den if den > 0 else np.nan
            print(f"{tau:6.2f} {b:9.5f} {d:9.5f} {mx:8.4f} {yc[am]:7.3f} "
                  f"{abs(W[N//2]):8.4f} {B:8.3f} {mx-prev_max:9.2e}")
            prev_max = mx

if __name__ == "__main__":
    run()
