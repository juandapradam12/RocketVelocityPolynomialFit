"""Quadratic velocity interpolation from discrete samples."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from rocket_velocity.models import ObservationSet, QuadraticCoefficients
from rocket_velocity.solvers.gauss_jordan import gauss_jordan_solve


def vandermonde_quadratic(time_s: NDArray[np.floating]) -> NDArray[np.floating]:
    r"""Build the design matrix for \(v(t) = a_2 t^2 + a_1 t + a_0\)."""
    t = np.asarray(time_s, dtype=float)
    return np.column_stack([t**2, t, np.ones_like(t)])


@dataclass(frozen=True)
class PolynomialFit:
    """Result of fitting a quadratic velocity model."""

    observations: ObservationSet
    coefficients: QuadraticCoefficients
    residual_norm: float
    max_abs_residual: float

    def predict(self, t: NDArray[np.floating] | float) -> NDArray[np.floating]:
        return self.coefficients.evaluate(t)


def fit_quadratic_velocity(observations: ObservationSet) -> PolynomialFit:
    """Interpolate rocket velocity with an exact quadratic polynomial.

    For three non-collinear samples the Vandermonde system is square and
    yields a unique interpolating parabola.
    """
    if observations.n_samples != 3:
        raise ValueError(
            "This use case fits an exact quadratic to exactly three samples."
        )

    design = vandermonde_quadratic(observations.time_s)
    coeffs = gauss_jordan_solve(design, observations.velocity_mps)
    model = QuadraticCoefficients(a2=float(coeffs[0]), a1=float(coeffs[1]), a0=float(coeffs[2]))

    residuals = model.evaluate(observations.time_s) - observations.velocity_mps
    return PolynomialFit(
        observations=observations,
        coefficients=model,
        residual_norm=float(np.linalg.norm(residuals)),
        max_abs_residual=float(np.max(np.abs(residuals))),
    )
