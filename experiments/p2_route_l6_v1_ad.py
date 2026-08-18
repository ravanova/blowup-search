"""Leg 401, unit L6 -- minimal reverse-mode AD tape (float64, numpy only).

Written for `experiments/p2_route_l6_v1.py`.  Exists so that the exact gradient of the
load-bearing residual functional is available to L-BFGS-B without 10^3 finite differences
per iteration.

BAN C1 NOTE (pre-registered, leg_401.md SS0.3): this module differentiates a SCALAR
OBJECTIVE.  It constructs no approximate inverse of any operator, no Y0/Z0/Z1/Z2, no
radii polynomial, no contraction constant, no enclosure.

Supported ops: add, sub, neg, mul (Var*Var and Var*const, broadcasting), truediv by a
Var or const, einsum with exactly one Var operand and one constant operand, sum over
axes, elementwise power, sqrt, reshape/transpose.
"""

from __future__ import annotations

import numpy as np


class Var:
    __slots__ = ("v", "_parents", "_vjp")

    # keep numpy from trying to broadcast a Var elementwise into an object array:
    # both of these force ndarray OP Var to defer to Var.__rop__.
    __array_ufunc__ = None
    __array_priority__ = 1000.0

    def __init__(self, v, parents=(), vjp=None):
        self.v = np.asarray(v, dtype=np.float64)
        self._parents = parents
        self._vjp = vjp

    # ---- shape helpers -------------------------------------------------------------
    @property
    def shape(self):
        return self.v.shape

    def __repr__(self):
        return f"Var(shape={self.v.shape})"

    # ---- arithmetic ----------------------------------------------------------------
    def __add__(self, o):
        return _binary(self, o, lambda a, b: a + b, lambda g, a, b: g, lambda g, a, b: g)

    __radd__ = __add__

    def __sub__(self, o):
        return _binary(self, o, lambda a, b: a - b, lambda g, a, b: g, lambda g, a, b: -g)

    def __rsub__(self, o):
        return _binary(o, self, lambda a, b: a - b, lambda g, a, b: g, lambda g, a, b: -g)

    def __neg__(self):
        return Var(-self.v, (self,), lambda g: (-g,))

    def __mul__(self, o):
        return _binary(self, o, lambda a, b: a * b,
                       lambda g, a, b: g * b, lambda g, a, b: g * a)

    __rmul__ = __mul__

    def __truediv__(self, o):
        return _binary(self, o, lambda a, b: a / b,
                       lambda g, a, b: g / b, lambda g, a, b: -g * a / (b * b))

    def __rtruediv__(self, o):
        return _binary(o, self, lambda a, b: a / b,
                       lambda g, a, b: g / b, lambda g, a, b: -g * a / (b * b))

    def __pow__(self, p):
        p = float(p)
        return Var(self.v ** p, (self,), lambda g: (g * p * self.v ** (p - 1.0),))

    def sum(self, axis=None):
        val = self.v.sum(axis=axis)
        shp = self.v.shape
        ax = axis

        def vjp(g):
            gg = np.asarray(g)
            if ax is None:
                return (np.broadcast_to(gg, shp).copy(),)
            axes = (ax,) if isinstance(ax, int) else tuple(ax)
            axes = tuple(a % len(shp) for a in axes)
            expanded = np.expand_dims(gg, axes)
            return (np.broadcast_to(expanded, shp).copy(),)

        return Var(val, (self,), vjp)

    def reshape(self, *shape):
        if len(shape) == 1 and isinstance(shape[0], tuple):
            shape = shape[0]
        old = self.v.shape
        return Var(self.v.reshape(shape), (self,), lambda g: (np.asarray(g).reshape(old),))

    def transpose(self, *axes):
        if len(axes) == 1 and isinstance(axes[0], (tuple, list)):
            axes = tuple(axes[0])
        inv = np.argsort(axes)
        return Var(self.v.transpose(axes), (self,),
                   lambda g: (np.asarray(g).transpose(inv),))


def _unbroadcast(g, shape):
    g = np.asarray(g)
    while g.ndim > len(shape):
        g = g.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and g.shape[i] != 1:
            g = g.sum(axis=i, keepdims=True)
    return g


def _binary(x, y, fwd, dx, dy):
    xv, yv = (x.v if isinstance(x, Var) else np.asarray(x, dtype=np.float64)), \
             (y.v if isinstance(y, Var) else np.asarray(y, dtype=np.float64))
    val = fwd(xv, yv)
    parents, slots = [], []
    if isinstance(x, Var):
        parents.append(x)
        slots.append(("x", xv.shape))
    if isinstance(y, Var):
        parents.append(y)
        slots.append(("y", yv.shape))

    def vjp(g):
        out = []
        for tag, shp in slots:
            gi = dx(g, xv, yv) if tag == "x" else dy(g, xv, yv)
            out.append(_unbroadcast(gi, shp))
        return tuple(out)

    return Var(val, tuple(parents), vjp)


def sqrt(x):
    if not isinstance(x, Var):
        return np.sqrt(x)
    val = np.sqrt(x.v)
    return Var(val, (x,), lambda g: (g * 0.5 / val,))


def einsum(spec, var, const):
    """einsum with EXACTLY one Var operand (first) and one constant ndarray (second)."""
    lhs, out_spec = spec.split("->")
    var_spec, const_spec = lhs.split(",")
    const = np.asarray(const, dtype=np.float64)
    val = np.einsum(spec, var.v, const, optimize=True)
    back = f"{out_spec},{const_spec}->{var_spec}"
    return Var(val, (var,), lambda g: (np.einsum(back, np.asarray(g), const, optimize=True),))


def backward(out):
    """Reverse sweep from a scalar Var.  Returns {id(Var): grad ndarray}."""
    topo, seen = [], set()
    stack = [(out, False)]
    while stack:
        node, done = stack.pop()
        if done:
            topo.append(node)
            continue
        if id(node) in seen:
            continue
        seen.add(id(node))
        stack.append((node, True))
        for p in node._parents:
            if id(p) not in seen:
                stack.append((p, False))
    grads = {id(out): np.ones_like(out.v)}
    for node in reversed(topo):
        g = grads.get(id(node))
        if g is None or node._vjp is None:
            continue
        for p, gp in zip(node._parents, node._vjp(g)):
            if id(p) in grads:
                grads[id(p)] = grads[id(p)] + gp
            else:
                grads[id(p)] = gp
    return grads


def grad_of(out, leaves):
    g = backward(out)
    return [g.get(id(l), np.zeros_like(l.v)) for l in leaves]
