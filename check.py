#!/usr/bin/env python3
"""
Deterministic checker for the chromatic-number-of-the-plane board (Hadwiger–Nelson).

A submission is a **unit-distance graph** (vertices are exact points in the plane; every edge
joins two points at distance exactly 1) that is **k-chromatic** — a witness for χ(plane) ≥ k.
The checker verifies both halves:

  (1) UNIT-DISTANCE VALIDITY — for every edge (u,v): (xu-xv)^2 + (yu-yv)^2 = 1, EXACTLY.
      Coordinates are given as expressions in a real number field (e.g. sqrt(3), sqrt(11)); the
      check is symbolic/exact (sympy) — never floating point (surd coordinates make floats unsound).

  (2) CHROMATIC LOWER BOUND — the graph is NOT (k-1)-colorable, so χ(graph) ≥ k and hence
      χ(plane) ≥ k. This is a coNP fact; a standard SAT solver settles it in seconds even at ~1500
      vertices. For record-scale graphs, submit a machine-checkable DRAT/LRAT UNSAT certificate
      (verified by drat-trim/lrat-check) — see README. This reference checker proves it by
      backtracking, which is fine for small graphs (the Moser-spindle example) but not at 500+
      vertices; there, use a SAT proof.

Input JSON:
    {"k": 5,
     "vertices": [[x, y], ...],     # x,y: ints, "p/q", or sympy exprs like "sqrt(3)/6", "(sqrt(33)-3)/6"
     "edges": [[i, j], ...]}        # indices into vertices; every edge must be a unit distance

Exit 0 = VALID (a k-chromatic unit-distance graph), 1 = INVALID, 2 = malformed / needs a SAT proof.
"""
import json
import sys

import sympy

_BACKTRACK_LIMIT = 60          # refuse to prove non-colorability by backtracking above this |V|


def _pt(c):
    return sympy.nsimplify(sympy.sympify(str(c)), rational=False) if isinstance(c, str) \
        else sympy.Rational(c) if isinstance(c, int) else sympy.sympify(c)


def _is_unit(px, py, qx, qy):
    d = sympy.expand((px - qx) ** 2 + (py - qy) ** 2 - 1)
    d = sympy.simplify(d)
    if d == 0:
        return True
    return bool(sympy.sqrtdenest(d) == 0) or bool(sympy.nsimplify(d) == 0) or d.equals(0)


def _colorable(n, adj, colors):
    """True iff the graph (adjacency sets `adj`) is properly `colors`-colorable. Backtracking."""
    order = sorted(range(n), key=lambda v: -len(adj[v]))     # most-constrained first
    col = [0] * n

    def bt(pos):
        if pos == n:
            return True
        v = order[pos]
        used = {col[u] for u in adj[v] if col[u]}
        cap = min(colors, pos + 1)                            # symmetry: colors introduced in order
        for c in range(1, cap + 1):
            if c not in used:
                col[v] = c
                if bt(pos + 1):
                    return True
                col[v] = 0
        return False

    return bt(0)


def validate(obj):
    if not isinstance(obj, dict) or "vertices" not in obj or "edges" not in obj:
        return (False, "input needs 'k', 'vertices', 'edges'", 2)
    k = obj.get("k", 5)
    V, E = obj["vertices"], obj["edges"]
    if not isinstance(V, list) or not isinstance(E, list) or not V:
        return (False, "'vertices' and 'edges' must be lists; vertices nonempty", 2)
    try:
        P = [(_pt(v[0]), _pt(v[1])) for v in V]
    except Exception as e:
        return (False, f"bad vertex coordinate: {e}", 2)
    n = len(P)

    # distinct vertices
    seen = set()
    for i, (x, y) in enumerate(P):
        key = (sympy.srepr(x), sympy.srepr(y))
        if key in seen:
            return (False, f"duplicate vertex {i}", 1)
        seen.add(key)

    # (1) every edge is a unit distance
    adj = [set() for _ in range(n)]
    for e, (i, j) in enumerate(E):
        if not (0 <= i < n and 0 <= j < n) or i == j:
            return (False, f"edge {e} has bad indices {i},{j}", 1)
        if not _is_unit(P[i][0], P[i][1], P[j][0], P[j][1]):
            return (False, f"edge {e} = ({i},{j}) is NOT a unit distance", 1)
        adj[i].add(j); adj[j].add(i)

    # (2) not (k-1)-colorable  ⇒  χ ≥ k
    if n > _BACKTRACK_LIMIT:
        return (False, f"{n} vertices: too large to prove non-colorability by backtracking — "
                       f"submit a DRAT/LRAT UNSAT certificate for non-{k-1}-colorability (see README)", 2)
    if _colorable(n, adj, k - 1):
        return (False, f"graph IS {k-1}-colorable, so it does not witness χ ≥ {k}", 1)

    return (True, f"valid unit-distance graph, {n} vertices, {len(E)} edges, "
                  f"not {k-1}-colorable ⇒ χ(plane) ≥ {k}", 0)


def main(argv):
    if len(argv) != 2:
        print("usage: python3 check.py <graph.json>", file=sys.stderr)
        return 2
    try:
        obj = json.load(open(argv[1]))
    except (OSError, json.JSONDecodeError) as e:
        print(f"malformed input: {e}", file=sys.stderr)
        return 2
    ok, msg, code = validate(obj)
    print(("VALID  " if ok else "INVALID  ") + msg)
    return 0 if ok else code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
