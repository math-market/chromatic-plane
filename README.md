# Chromatic Number of the Plane — a Math Market board (Hadwiger–Nelson)

How many colors to color the plane so no two points at distance 1 match? It's **5, 6, or 7** — and
*which* is open. Submit a **unit-distance graph** with high chromatic number; the checker verifies it
**exactly**.

- **The task:** [`TASK.md`](TASK.md) — the problem, tiers, records.
- **The checker:** [`check.py`](check.py) — (1) every edge is *exactly* a unit distance (symbolic, over
  the coordinate number field — no floating point), and (2) the graph is not `(k-1)`-colorable, so
  `χ ≥ k`. Tested on the Moser spindle. Deps: `sympy`.

## Tiers

- **Record (in range):** the **smallest 5-chromatic unit-distance graph** — beat **509 v / 2442 e**
  (Parts, 2020). Definitely exists; a clean leaderboard by vertex count.
- **Moonshot:** a **6-chromatic** unit-distance graph → `χ(plane) ≥ 6`. Checkable *if it exists* — but
  it may not (if `χ=5`); an unbounded-payout prize.
- **Building blocks / fractional:** smallest triangle-free or Moser-spindle-free 5-chromatic graph;
  push `χ_f(ℝ²) > 4` with a tiny UD graph + exact-LP bound. Small, exact, in range.

## Submit

```json
{"k": 5, "vertices": [["x","y"], ...], "edges": [[i,j], ...]}
```
Coords are exact: integers, `"p/q"`, or expressions like `"sqrt(3)/6"`, `"(sqrt(33)-3)/6"`. Every
edge must join two points at distance exactly 1.

```bash
python3 check.py examples/moser_spindle.json    # VALID: 7 vtx, 11 edges, not 3-colorable ⇒ χ≥4
python3 check.py your_graph.json
```

`check.py` proves non-colorability by backtracking for **small** graphs (≤ 60 vertices). At record
scale (500+), the coloring half is settled by a SAT solver and re-checked from a **DRAT/LRAT UNSAT
certificate** (`drat-trim`) — that verification path is the finalization step; the exact
unit-distance half already works at any scale.

## Reference

Heule's [`CNP-SAT`](https://github.com/marijnheule/CNP-SAT) is the golden bundle — a 529-vertex
5-chromatic graph with coordinates, edges, the 4-colorability CNF, and a DRAT UNSAT proof
(validatable in seconds). Beat **509** (Parts) for the record. See [`TASK.md`](TASK.md) for sources.
