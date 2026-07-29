# Submissions

Add `submissions/<your-handle>.json` = `{"k": 5, "vertices": [...], "edges": [...]}` via a PR from
your fork. Coords: ints, `"p/q"`, or exact expressions (`"sqrt(3)/6"`). Every edge must be a unit
distance. CI runs [`../check.py`](../check.py).

- **Record tier:** a **5-chromatic** unit-distance graph with **fewer than 509 vertices**.
- **Moonshot:** a **6-chromatic** one (`"k": 6`).
- Record-scale graphs (500+ vertices): also include a DRAT/LRAT UNSAT proof of non-(k-1)-colorability
  under `submissions/<handle>/` (the coloring half is verified from the certificate; see ../TASK.md).

Run locally first: `python3 check.py submissions/your.json` (needs `pip install sympy`).
