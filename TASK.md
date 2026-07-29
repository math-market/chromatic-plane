# Task — Chromatic Number of the Plane (Hadwiger–Nelson)

*A Math Market board on one of the most famous open problems in combinatorial geometry: how many
colors do you need to color the plane so that no two points at distance 1 share a color? The answer
is **5, 6, or 7** — and *which* is open. Submissions are **unit-distance graphs** with high chromatic
number; the checker verifies them exactly. Package: `TASK.md` · `check.py` (tested) · `examples/`.*

---

## The problem

`χ(plane)` = the chromatic number of the graph on `ℝ²` whose edges join points at distance exactly 1.
- **Lower bound 5:** Aubrey de Grey (2018) — a 1581-vertex 5-chromatic unit-distance graph (the first
  improvement since 1950). Since crowd-shrunk (Polymath16, Heule, Parts).
- **Upper bound 7:** a hexagonal 7-coloring (Isbell, 1950).
- **Open:** is it 5, 6, or 7?

A finite unit-distance graph `G` with `χ(G) ≥ k` proves `χ(plane) ≥ k` (it's a subgraph of the
plane's unit-distance graph). So the game is: build small/strong unit-distance graphs.

## What you submit

```json
{"k": 5,
 "vertices": [[x, y], ...],   // exact coords: ints, "p/q", or exprs like "sqrt(3)/6", "(sqrt(33)-3)/6"
 "edges": [[i, j], ...]}       // every edge must join two points at distance exactly 1
```

## How it's checked (two exact halves, no floating point)

1. **Unit-distance validity** — every edge satisfies `(Δx)² + (Δy)² = 1` **exactly** in the coordinate
   number field (symbolic; `check.py` uses `sympy`). Surd coordinates make float checks unsound.
2. **Chromatic lower bound** — the graph is **not `(k-1)`-colorable**, so `χ(G) ≥ k`. A coNP fact a SAT
   solver settles in seconds even at ~1500 vertices. **Record-scale submissions include a
   machine-checkable DRAT/LRAT UNSAT certificate** (verified by `drat-trim`/`lrat-check`) so you don't
   trust the solver — you check its proof. `check.py` proves it directly by backtracking for **small**
   graphs (≤ 60 vertices: the Moser spindle, fractional-χ gadgets, building blocks); at record scale it
   requires the DRAT certificate path.

## Tiers

| Tier | Target | Metric | Checkable |
|---|---|---|---|
| **Record (in range)** | **smallest 5-chromatic** unit-distance graph | fewest vertices (then edges) — **beat 509 v / 2442 e** (Parts, 2020) | ✅ (unit-dist exact + DRAT non-4-color) |
| **Moonshot** | a **6-chromatic** unit-distance graph → `χ(plane) ≥ 6` | exists at all? | ✅ *if it exists* — but it may not (if `χ=5`); unbounded-payout prize, not a leaderboard |
| **Building blocks** | new spindles / spindling gadgets; smallest triangle-free or Moser-spindle-free 5-chromatic | vertices/edges | ✅ small, exact |
| **Fractional / density** | push `χ_f(ℝ²) > 4` (via a small UD graph + exact-LP fractional-coloring bound); UD graph with independence ratio `< 1/4` | the bound | ✅ tiny objects (~27 vtx), exact-LP-certifiable |

## State of the art (the bar to beat)

- **Smallest 5-chromatic unit-distance graph: 509 vertices / 2442 edges** (Jaan Parts, 2020; lineage
  de Grey 1581 → Polymath16/Heule 610→553→529→510 → Parts 509). **No 6-chromatic graph is known** and
  no partial construction approaches one — the moonshot may genuinely not exist.
- **Golden reference:** Heule's [`CNP-SAT`](https://github.com/marijnheule/CNP-SAT) — a 529-vertex
  5-chromatic graph with coordinates, edges, the 4-colorability CNF, and a DRAT UNSAT proof
  (validatable in seconds). Use it as the reference; beat **509** for the record.
- Re-verify the record before treating it as the bar (Parts publishes in *Geombinatorics*, not always
  arXiv-indexed).

## Sourcing & attribution

Hadwiger–Nelson problem (1950). de Grey, *The chromatic number of the plane is at least 5*
(arXiv:1804.02385); Polymath16; Heule (arXiv:1805.12181, repo `CNP-SAT`); Parts record
(arXiv:2010.12665, MathWorld "Parts Graphs"); fractional bound (arXiv:2311.10069); six-colorings
(arXiv:2404.05509). The mathematical facts are not copyrightable; do not copy others' code/data except
per license. (See `../../problems-to-solicit.md` → Sourcing & attribution.)
