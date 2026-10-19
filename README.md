# Polynomial Fitting for Rocket Velocity

Portfolio use case: recover a continuous rocket velocity profile from three discrete measurements by fitting the unique quadratic interpolant

$$
v(t) = a_2 t^2 + a_1 t + a_0
$$

and solving the resulting Vandermonde system with Gauss–Jordan elimination (partial pivoting).

## Use case

| Item | Detail |
| --- | --- |
| **Domain** | Scientific computing / numerical methods |
| **Input** | Time–velocity samples at $t \in \{2, 5, 9\}\,\mathrm{s}$ |
| **Model** | Exact quadratic interpolant |
| **Solver** | Custom Gauss–Jordan on the augmented matrix |
| **Output** | Coefficients, $v(7\,\mathrm{s})$, residual diagnostics, fit figure |

Measured samples:

$$
(t, v) = (2,\,45.948),\; (5,\,119.985),\; (9,\,231.497)
\quad [t] = \mathrm{s},\; [v] = \mathrm{m/s}.
$$

The linear system enforced by the interpolant is

$$
\begin{bmatrix}
t_i^2 & t_i & 1
\end{bmatrix}
\begin{bmatrix}
a_2 \\ a_1 \\ a_0
\end{bmatrix}
= v_i,
\quad i = 1,2,3.
$$

## Project structure

```text
src/rocket_velocity/   # Installable package (models, solver, fitting, CLI)
scripts/run_fit.py     # Run without installing
tests/                 # Solver and fitting tests
docs/                  # Methodology and architecture
figures/               # Generated fit plot
```

See [docs/methodology.md](docs/methodology.md) for the mathematics and [docs/architecture.md](docs/architecture.md) for the package layout.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python scripts/run_fit.py
pytest
```

Example CLI output shape:

```text
Quadratic model: v(t) = a2·t² + a1·t + a0
  a2 = ...
  a1 = ...
  a0 = ...
v(7 s) = ... m/s
Residual L2 norm at samples: ...
Figure written to: figures/rocket_velocity_fit.png
```

## Improvements over the legacy script

- Layered package (`models` → `solvers` → `fitting` → CLI/visualization) instead of a single procedural file
- Gauss–Jordan with **partial pivoting** and singular-system detection
- Typed dataclasses, input validation, and residual reporting
- Automated tests against `numpy.linalg.solve`
- English documentation with GitHub-renderable math

## Requirements

- Python 3.10+
- NumPy, Matplotlib (declared in `pyproject.toml`)

## License

MIT — see [LICENSE](LICENSE).
