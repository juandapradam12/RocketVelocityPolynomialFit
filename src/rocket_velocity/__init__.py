"""Rocket velocity polynomial fitting package."""

from rocket_velocity.fitting.polynomial import PolynomialFit, fit_quadratic_velocity
from rocket_velocity.models import ObservationSet

__all__ = [
    "ObservationSet",
    "PolynomialFit",
    "fit_quadratic_velocity",
]

__version__ = "1.0.0"
