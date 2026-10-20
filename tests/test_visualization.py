"""Smoke tests for figure generation."""

from __future__ import annotations

from pathlib import Path

from rocket_velocity.data import DEFAULT_OBSERVATIONS
from rocket_velocity.fitting.polynomial import fit_quadratic_velocity
from rocket_velocity.visualization import generate_all_figures


def test_generate_all_figures(tmp_path: Path) -> None:
    fit = fit_quadratic_velocity(DEFAULT_OBSERVATIONS)
    paths = generate_all_figures(fit, figures_dir=tmp_path, query_time_s=7.0)

    assert set(paths) == {
        "velocity_fit",
        "residuals",
        "acceleration",
        "solver_agreement",
    }
    for path in paths.values():
        assert path.exists()
        assert path.stat().st_size > 0
