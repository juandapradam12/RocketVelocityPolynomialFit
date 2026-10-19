"""Unit tests for quadratic velocity fitting."""

from __future__ import annotations

import numpy as np
import pytest

from rocket_velocity.data import DEFAULT_OBSERVATIONS
from rocket_velocity.fitting.polynomial import fit_quadratic_velocity
from rocket_velocity.models import ObservationSet


def test_default_fit_interpolates_samples() -> None:
    fit = fit_quadratic_velocity(DEFAULT_OBSERVATIONS)
    predicted = fit.predict(DEFAULT_OBSERVATIONS.time_s)
    np.testing.assert_allclose(predicted, DEFAULT_OBSERVATIONS.velocity_mps, atol=1e-10)
    assert fit.residual_norm < 1e-10


def test_query_at_seven_seconds_is_positive() -> None:
    fit = fit_quadratic_velocity(DEFAULT_OBSERVATIONS)
    velocity = float(fit.predict(7.0))
    assert velocity > 0
    # Sanity band around the interpolated trajectory between t=5 and t=9.
    assert 160.0 < velocity < 200.0


def test_rejects_wrong_sample_count() -> None:
    observations = ObservationSet(
        time_s=np.array([1.0, 2.0]),
        velocity_mps=np.array([10.0, 20.0]),
    )
    with pytest.raises(ValueError, match="exactly three"):
        fit_quadratic_velocity(observations)


def test_observation_validation() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        ObservationSet(
            time_s=np.array([3.0, 2.0, 1.0]),
            velocity_mps=np.array([1.0, 2.0, 3.0]),
        )
