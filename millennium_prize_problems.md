# Millennium Prize Problems — Notes

Reference doc tracking discussion of the 7 Millennium Prize Problems (Clay Mathematics Institute).
Only the **Poincaré Conjecture** has been solved (Perelman, 2002–2003, via Ricci flow). The other six remain open.

---

## 1. P vs NP
**Question:** Is every problem whose solution can be verified quickly also solvable quickly?

**Why unsolved:** Whole categories of proof technique have been formally shown *insufficient*:
- Diagonalization/relativization — fails per Baker–Gill–Solovay.
- Natural proofs — self-defeating if strong pseudorandom generators exist (Razborov–Rudich).
- Algebrization — also shown insufficient.
No fundamentally new proof strategy has replaced these.

**Evolutionary computing fit:** Poor. The claim is universal over all algorithms/circuits — no fitness landscape corresponds to "prove a lower bound holds for every possible algorithm."

---

## 2. Riemann Hypothesis
**Question:** Do all nontrivial zeros of ζ(s) have real part 1/2?

**Why unsolved:** No known algebraic structure forces zeros onto the critical line. Trillions of zeros verified numerically, positive proportion proven on the line, but no general proof. Random matrix theory (zero spacing resembles random Hermitian matrix eigenvalues) and the Hilbert–Pólya conjecture (hoping for a self-adjoint operator with these eigenvalues) are suggestive but incomplete — no such operator has been constructed.

**Evolutionary computing fit:** Poor. Universal claim over infinitely many zeros; disproof needs one counterexample zero, but zero-finding is already a solved precise numerical problem (Riemann–Siegel formula) with no useful fitness gradient for GA-style search.

---

## 3. Navier–Stokes Existence and Smoothness
**Question:** In 3D, do solutions always stay smooth, or can they blow up in finite time?

**Why unsolved:** Nonlinear term can concentrate energy into arbitrarily small scales. 2D has extra conserved quantities preventing blow-up (proven); 3D lacks them. Known energy estimates don't close the gap between controllable and required energy bounds. No proof of global smoothness, no rigorous blow-up example either.

**Evolutionary computing fit: BEST CANDIDATE.**
- Disproof is existential — need just one blow-up initial condition, which is a search/optimization problem.
- Natural fitness function: vorticity growth rate as sim approaches singularity.
- Precedent: Hou et al.'s numerical search over initial data for near-singular 3D Euler solutions; Buckmaster & Gómez-Serrano's computer-assisted proofs of singular solutions for related equations.
- Caveat: GA would only produce numerical evidence — still needs rigorous interval-arithmetic bounds to become an accepted proof, but that pipeline already exists.

---

## 4. Hodge Conjecture
**Question:** Is every Hodge class on a smooth projective variety representable by an algebraic cycle?

**Why unsolved:** Bridges topology/analysis (flexible, continuous) with algebraic geometry (rigid, discrete). Known for divisors (Lefschetz (1,1) theorem) but no general method exists to construct algebraic cycles for higher-codimension classes.

**Evolutionary computing fit:** Poor. Discrete algebraic-structure existence question, no continuous parameter space or natural fitness signal.

---

## 5. Birch and Swinnerton-Dyer Conjecture
**Question:** Does the rank of an elliptic curve's rational points equal the order of vanishing of its L-function at s=1?

**Why unsolved:** Links an algebraic invariant (rank) to an analytic one (L-function behavior). Proven for rank 0 and 1 (Gross–Zagier, Kolyvagin) via Selmer groups, but general case needs control over Tate–Shafarevich group finiteness, only known in special cases.

**Evolutionary computing fit:** Distant second place. Could evolve/search elliptic curve parameters hunting for rank ≠ analytic-rank counterexamples, similar to LMFDB's systematic computation — but rank computation is exact/expensive per curve, not a smooth landscape, so systematic sieve search already beats GA-style stochastic search.

---

## 6. Yang–Mills Existence and Mass Gap
**Question:** Does a rigorous 4D quantum Yang–Mills theory exist, and does it have a mass gap (smallest particle mass > 0)?

**Why unsolved:** Requires first rigorously constructing 4D QFT at all — physicists use it successfully via perturbative/lattice methods, but it's never been placed on rigorous mathematical footing (unlike lower-dimensional QFTs). Mass gap is well-supported by physics/lattice simulation intuition but proving it needs non-perturbative rigor around an infinite-dimensional path integral that doesn't yet exist mathematically.

**Evolutionary computing fit:** Poor. Not a search problem — foundational rigorous construction with no numeric fitness signal.

---

## Solved: Poincaré Conjecture (for reference)
Proven by Grigori Perelman (2002–2003) using Ricci flow with surgery, building on Hamilton's program. Confirmed the 3-sphere is the only simply-connected closed 3-manifold. Perelman declined both the Fields Medal and the $1M Clay Prize.
