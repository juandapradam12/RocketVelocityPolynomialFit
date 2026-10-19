"""Domain models for velocity observations and fit results."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class ObservationSet:
    """Paired time–velocity samples used for interpolation."""

    time_s: NDArray[np.floating]
    velocity_mps: NDArray[np.floating]

    def __post_init__(self) -> None:
        time = np.asarray(self.time_s, dtype=float)
        velocity = np.asarray(self.velocity_mps, dtype=float)

        if time.ndim != 1 or velocity.ndim != 1:
            raise ValueError("time_s and velocity_mps must be one-dimensional.")
        if time.size != velocity.size:
            raise ValueError("time_s and velocity_mps must have the same length.")
        if time.size < 2:
            raise ValueError("At least two samples are required.")
        if np.any(np.diff(time) <= 0):
            raise ValueError("time_s must be strictly increasing.")

        object.__setattr__(self, "time_s", time)
        object.__setattr__(self, "velocity_mps", velocity)

    @property
    def n_samples(self) -> int:
        return int(self.time_s.size)


@dataclass(frozen=True)
class QuadraticCoefficients:
    r"""Coefficients of \(v(t) = a_2 t^2 + a_1 t + a_0\)."""

    a2: float
    a1: float
    a0: float

    def as_array(self) -> NDArray[np.floating]:
        return np.array([self.a2, self.a1, self.a0], dtype=float)

    def evaluate(self, t: NDArray[np.floating] | float) -> NDArray[np.floating]:
        t_arr = np.asarray(t, dtype=float)
        return self.a2 * t_arr**2 + self.a1 * t_arr + self.a0
