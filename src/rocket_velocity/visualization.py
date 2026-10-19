"""Plotting helpers for the fitted velocity curve."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from rocket_velocity.fitting.polynomial import PolynomialFit


def plot_velocity_fit(
    fit: PolynomialFit,
    *,
    output_path: str | Path,
    query_time_s: float | None = 7.0,
    t_min: float = 0.0,
    t_max: float = 10.0,
) -> Path:
    """Render samples and the fitted quadratic on a dense time grid."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    grid = np.linspace(t_min, t_max, 200)
    curve = fit.predict(grid)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(grid, curve, color="#1f4e79", linewidth=2.0, label="Quadratic fit")
    ax.scatter(
        fit.observations.time_s,
        fit.observations.velocity_mps,
        color="#c0392b",
        zorder=3,
        label="Measured samples",
    )

    if query_time_s is not None:
        query_velocity = float(fit.predict(query_time_s))
        ax.scatter(
            [query_time_s],
            [query_velocity],
            color="#2e7d32",
            marker="D",
            zorder=4,
            label=f"Estimate at t = {query_time_s:g} s",
        )

    ax.set_title("Rocket Velocity — Quadratic Polynomial Fit")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (m/s)")
    ax.set_xlim(t_min - 0.5, t_max + 0.5)
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path
