# Architecture

The project is a small, layered scientific-computing package. Responsibilities are separated so that numerical methods, domain models, and presentation can evolve independently.

## Layout

```text
src/rocket_velocity/
  models.py           # Observation and coefficient value objects
  data.py             # Canonical sample set for this use case
  solvers/            # Linear solvers (Gauss–Jordan)
  fitting/            # Vandermonde construction and fit orchestration
  visualization.py    # Figure generation
  cli.py              # Thin command-line interface
scripts/run_fit.py    # Convenience runner without install
tests/                # Solver and fitting checks
docs/                 # Use-case documentation
figures/              # Generated plots
```

## Layers

| Layer | Responsibility |
| --- | --- |
| **Models** | Immutable data contracts (`ObservationSet`, `QuadraticCoefficients`) with validation. |
| **Solvers** | Pure numerical routines with no knowledge of rockets or plotting. |
| **Fitting** | Builds the design matrix, calls the solver, and returns a structured `PolynomialFit`. |
| **Presentation** | CLI output and matplotlib figures; no linear-algebra logic. |

## Design choices

- **Exact quadratic for three samples** — matches the original problem statement and keeps the linear system square.
- **Custom Gauss–Jordan with partial pivoting** — demonstrates an implemented numerical method instead of only calling a black-box library; tests still cross-check against `numpy.linalg.solve`.
- **Dataclasses over ad-hoc arrays** — makes coefficients and residuals explicit for readers of the portfolio.
- **Package under `src/`** — avoids accidental imports from the repository root and mirrors common Python packaging practice.
