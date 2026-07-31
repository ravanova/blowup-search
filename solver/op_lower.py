"""A LOWER bound on ||A|| that is worth reading.

Every bracket this project has quoted has a lower end that is a maximum over
sign patterns: for a domain index i, the codomain vector g = sign(A_i.)/v, whose
image maximizes the SUP part of ||A g||.  Those directions are the exact
extremizers of a sup-to-sup problem, and they are terrible here, for the reason
v6's discrete-ball trap already made famous in the other direction: a sign
pattern's HOLDER SEMINORM is enormous, so dividing by the full codomain norm
throws away almost everything the numerator gained.  At J = 400 they report 0.94
against an upper bound of 47.

That gap is not a measurement.  "The bound is 50x too big" and "the operator
really is that large" imply opposite decisions about the whole Route-D lane, and
until the lower end is earned they cannot be told apart.  v9 made the point the
expensive way: it converted the bracket into a "19x available gain" that was
pure artifact.

--------------------------------------------------------------------------
WHAT WORKS INSTEAD
--------------------------------------------------------------------------
ANY g gives a valid lower bound ||A|| >= ||A g||_X / ||g||_Y, so the whole
problem is constructing good ones -- this is banked lesson (9), BUILD THE
ADVERSARY, applied to the operator rather than to the quadratic.

The Y-ball's shape says what to look for.  An element with finite codomain norm
must decay at least like 1/v = cos^{alpha+1}(theta/2), and it must not oscillate,
or the seminorm eats it.  So the family is `1/v` times a SLOWLY VARYING shape:

  * powers cos^b(theta/2) and low-order cos(k theta) -- the smoothest elements;
  * Gaussian bumps over a wide sweep of centre and width -- localized mass;
  * smoothed STEPS tanh((theta-c)/w) -- one sign change, which turns out to be
    what the extremizer wants: the winner at (1.5, 0.5) is a step at theta =
    2.65 with width 0.2, giving 3.04 against the sign patterns' 0.94;
  * boxes (two steps) for two sign changes.

Then a random ascent in a smooth cosine basis from the best of those, which
polishes but rarely finds anything the family missed -- reported honestly rather
than dropped, because "the ascent adds nothing" is information about how flat the
maximum is.

--------------------------------------------------------------------------
WHAT THIS IS AND IS NOT
--------------------------------------------------------------------------
Still a LOWER bound from a finite family: the true norm is at least this, and the
bracket it forms with the upper bound is still only an upper bound on how lossy
that upper bound is.  What changes is that the number is now within a small
factor of the upper bound instead of two orders below it, so the bracket carries
information.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np


def sign_pattern_lower(A, dom, cod, n_rows=40):
    """The baseline every earlier leg used: raw sign-pattern directions."""
    B = A / cod.w[None, :]
    rows = np.unique(np.linspace(0, A.shape[0] - 1, int(n_rows)).astype(int))
    best, arg = 0.0, -1
    for i in rows:
        g = np.sign(B[i]) / cod.w
        g[0] = 0.0
        n = cod(g)
        if n > 0:
            r = dom(A @ g) / n
            if r > best:
                best, arg = r, int(i)
    return {"lower": float(best), "row": arg, "family": "raw sign patterns"}


def smooth_family(theta, cod_w, n_centre=40, n_step=60):
    """The candidate directions: 1/v times a slowly varying shape.

    Yields (name, g).  Every member has the codomain weight built in, so the sup
    part of its norm is O(1) and the seminorm is whatever the shape costs.
    """
    iv = 1.0 / cod_w
    th = np.asarray(theta, dtype=float)
    for b in (0.0, 0.5, 1.0, 2.0, 4.0):
        yield "pow%.1f" % b, iv * np.cos(0.5 * th) ** b
    for k in range(0, 9):
        yield "cos%d" % k, iv * np.cos(k * th)
    for c0 in np.linspace(0.02, np.pi - 0.02, int(n_centre)):
        for w in (0.01, 0.03, 0.08, 0.2, 0.5, 1.0, 2.0, 4.0):
            yield "bump%.2f/%.2f" % (c0, w), iv * np.exp(-((th - c0) / w) ** 2)
    for c0 in np.linspace(0.02, np.pi - 0.02, int(n_step)):
        for w in (0.02, 0.2):
            yield "step%.2f/%.2f" % (c0, w), iv * np.tanh((th - c0) / w)
    for c0 in np.linspace(0.05, np.pi - 0.2, 16):
        for c1 in np.linspace(0.05, np.pi - 0.05, 16):
            if c1 > c0:
                yield ("box%.2f-%.2f" % (c0, c1),
                       iv * (np.tanh((th - c0) / 0.05) - np.tanh((th - c1) / 0.05)))


def family_lower(A, dom, cod, theta, **kw):
    """max over the smooth family -- the honest lower bound."""
    best, arg = 0.0, ""
    for name, g in smooth_family(theta, cod.w, **kw):
        g = g.copy()
        g[0] = 0.0
        n = cod(g)
        if n <= 0:
            continue
        r = dom(A @ g) / n
        if r > best:
            best, arg = r, name
    return {"lower": float(best), "argmax": arg, "family": "smooth shapes / v"}


def ascend(A, dom, cod, theta, g0, K=24, iters=3000, seed=0, scale=0.35):
    """Random ascent in a smooth cosine basis, starting from `g0`.

    Reported even when it adds nothing: a flat maximum is information about the
    shape of the problem, not a failed experiment.
    """
    rng = np.random.default_rng(int(seed))
    iv = 1.0 / cod.w
    basis = np.array([iv * np.cos(k * np.asarray(theta)) for k in range(int(K))])
    cur = np.asarray(g0, dtype=float).copy()
    cur[0] = 0.0

    def ratio(g):
        n = cod(g)
        return 0.0 if n <= 0 else dom(A @ g) / n

    best = ratio(cur)
    for _ in range(int(iters)):
        step = scale * best * (rng.normal(size=int(K)) @ basis) / np.sqrt(K)
        cand = cur + step * rng.uniform(0.2, 1.0)
        cand[0] = 0.0
        r = ratio(cand)
        if r > best:
            cur, best = cand, r
    return {"lower": float(best), "vector": cur}


def best_lower(A, dom, cod, theta, ascent_iters=3000, **kw):
    """The full construction: baseline, family, ascent -- and the bracket inputs."""
    base = sign_pattern_lower(A, dom, cod)
    fam = family_lower(A, dom, cod, theta, **kw)
    g0 = None
    for name, g in smooth_family(theta, cod.w, **kw):
        if name == fam["argmax"]:
            g0 = g
            break
    asc = ascend(A, dom, cod, theta, g0, iters=ascent_iters) if g0 is not None \
        else {"lower": fam["lower"]}
    return {"sign_patterns": base["lower"], "smooth_family": fam["lower"],
            "family_argmax": fam["argmax"], "after_ascent": asc["lower"],
            "lower": float(max(base["lower"], fam["lower"], asc["lower"])),
            "ascent_gain": asc["lower"] / fam["lower"] if fam["lower"] > 0 else 1.0}
