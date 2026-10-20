# Rocket Velocity Polynomial Fit

[![CI](https://github.com/juandapradam12/Polynomial-Fitting-For-a-Rocket-Velocity/actions/workflows/ci.yml/badge.svg)](https://github.com/juandapradam12/Polynomial-Fitting-For-a-Rocket-Velocity/actions/workflows/ci.yml)

Recover a continuous rocket velocity profile from three discrete samples by fitting a quadratic interpolant and solving the Vandermonde system with Gauss–Jordan elimination (partial pivoting).

The model is

$$
v(t) = a_2 t^2 + a_1 t + a_0,
$$

cross-checked against `numpy.linalg.solve`, with residual and condition-number diagnostics.

## Figures

Quadratic interpolant through the measured samples, with the query at $t = 7\,\mathrm{s}$:

![Quadratic fit of rocket velocity samples with estimate at t = 7 s](figures/rocket_velocity_fit.png)

Interpolation residuals at the sample nodes (machine-precision scale):

![Residuals of the quadratic interpolant at sample times](figures/rocket_velocity_residuals.png)

Acceleration implied by differentiating the fitted velocity, $a(t) = 2 a_2 t + a_1$:

![Implied acceleration profile from the velocity fit](figures/rocket_acceleration_profile.png)

Coefficient agreement between the custom Gauss–Jordan solver and `numpy.linalg.solve`:

![Coefficient comparison between Gauss-Jordan and NumPy](figures/solver_coefficient_agreement.png)

## Use case

| Item | Detail |
| --- | --- |
| **Domain** | Scientific computing / numerical methods |
| **Input** | Time–velocity samples at $t \in \{2, 5, 9\}\,\mathrm{s}$ |
| **Model** | Exact quadratic interpolant |
| **Solver** | Custom Gauss–Jordan on the augmented matrix |
| **Reference** | Cross-checked against `numpy.linalg.solve` |
| **Output** | Coefficients, $v(7\,\mathrm{s})$, residual / condition diagnostics, diagnostic figures |

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

## Result snapshot

| Quantity | Value |
| --- | --- |
| $a_2, a_1, a_0$ | $0.457$, $21.480$, $1.160$ |
| $v(7\,\mathrm{s})$ | $173.913\,\mathrm{m/s}$ |
| Sample residual $\|r\|_2$ | $\sim 10^{-14}$ |
| $\kappa_2(A)$ | $\approx 2.45 \times 10^{2}$ |
| $\max\lvert\Delta a\rvert$ vs NumPy | $\sim 10^{-15}$ |

## Project structure

```text
src/rocket_velocity/   # Installable package (models, solver, fitting, CLI)
scripts/run_fit.py     # Run without installing
tests/                 # Solver and fitting tests
docs/                  # Methodology and architecture
figures/               # Generated diagnostic plots
.github/workflows/     # CI
```

See [docs/methodology.md](docs/methodology.md) for the mathematics (including conditioning and the NumPy cross-check) and [docs/architecture.md](docs/architecture.md) for the package layout.

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
Design-matrix condition number κ₂(A): ...
Max |Δa| vs numpy.linalg.solve: ...
Figures written:
  - velocity_fit: figures/rocket_velocity_fit.png
  - residuals: figures/rocket_velocity_residuals.png
  - acceleration: figures/rocket_acceleration_profile.png
  - solver_agreement: figures/solver_coefficient_agreement.png
```

## Improvements over the legacy script

- Layered package (`models` → `solvers` → `fitting` → CLI/visualization) instead of a single procedural file
- Gauss–Jordan with **partial pivoting** and singular-system detection
- Condition-number reporting and coefficient cross-check vs `numpy.linalg.solve`
- Typed dataclasses, input validation, and residual reporting
- Automated tests and GitHub Actions CI
- English documentation with GitHub-renderable math

## Requirements

- Python 3.10+
- NumPy, Matplotlib (declared in `pyproject.toml`)

## License

MIT — see [LICENSE](LICENSE).
