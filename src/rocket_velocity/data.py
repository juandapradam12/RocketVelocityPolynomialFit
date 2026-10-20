"""Canonical observation set used by this use case."""

from __future__ import annotations

import numpy as np

from rocket_velocity.models import ObservationSet

# Measured rocket velocity samples (time in seconds, velocity in m/s).
# These three points uniquely determine a quadratic interpolant.
DEFAULT_OBSERVATIONS = ObservationSet(
    time_s=np.array([2.0, 5.0, 9.0], dtype=float),
    velocity_mps=np.array([45.948, 119.985, 231.497], dtype=float),
)
