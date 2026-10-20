"""Plotting helpers for the fitted velocity model."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from rocket_velocity.fitting.polynomial import PolynomialFit, vandermonde_quadratic
from rocket_velocity.solvers.gauss_jordan import gauss_jordan_solve

_COLOR_FIT = "#1f4e79"
_COLOR_SAMPLE = "#c0392b"
_COLOR_QUERY = "#2e7d32"
_COLOR_NUMPY = "#6c757d"


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
    ax.plot(grid, curve, color=_COLOR_FIT, linewidth=2.0, label="Quadratic fit")
    ax.scatter(
        fit.observations.time_s,
        fit.observations.velocity_mps,
        color=_COLOR_SAMPLE,
        zorder=3,
        label="Measured samples",
    )

    if query_time_s is not None:
        query_velocity = float(fit.predict(query_time_s))
        ax.scatter(
            [query_time_s],
            [query_velocity],
            color=_COLOR_QUERY,
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


def plot_sample_residuals(
    fit: PolynomialFit,
    *,
    output_path: str | Path,
) -> Path:
    """Plot interpolation residuals at the measurement nodes."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    t = fit.observations.time_s
    residuals = fit.predict(t) - fit.observations.velocity_mps

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axhline(0.0, color="#888888", linewidth=1.0)
    ax.stem(t, residuals, linefmt="C3-", markerfmt="C3o", basefmt=" ")
    ax.set_title("Interpolation Residuals at Sample Times")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Residual v̂(t) − v (m/s)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot_acceleration_profile(
    fit: PolynomialFit,
    *,
    output_path: str | Path,
    query_time_s: float | None = 7.0,
    t_min: float = 0.0,
    t_max: float = 10.0,
) -> Path:
    """Plot the acceleration implied by differentiating the velocity model."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    coeffs = fit.coefficients
    grid = np.linspace(t_min, t_max, 200)
    acceleration = 2.0 * coeffs.a2 * grid + coeffs.a1

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(grid, acceleration, color=_COLOR_FIT, linewidth=2.0, label="a(t) = dv/dt")
    ax.scatter(
        fit.observations.time_s,
        2.0 * coeffs.a2 * fit.observations.time_s + coeffs.a1,
        color=_COLOR_SAMPLE,
        zorder=3,
        label="At sample times",
    )

    if query_time_s is not None:
        query_acc = float(2.0 * coeffs.a2 * query_time_s + coeffs.a1)
        ax.scatter(
            [query_time_s],
            [query_acc],
            color=_COLOR_QUERY,
            marker="D",
            zorder=4,
            label=f"Estimate at t = {query_time_s:g} s",
        )

    ax.set_title("Implied Acceleration from the Velocity Fit")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Acceleration (m/s²)")
    ax.set_xlim(t_min - 0.5, t_max + 0.5)
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot_solver_agreement(
    fit: PolynomialFit,
    *,
    output_path: str | Path,
) -> Path:
    """Compare Gauss–Jordan coefficients against NumPy's reference solve."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    design = vandermonde_quadratic(fit.observations.time_s)
    gj = gauss_jordan_solve(design, fit.observations.velocity_mps)
    ref = np.linalg.solve(design, fit.observations.velocity_mps)

    labels = ["$a_2$", "$a_1$", "$a_0$"]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, gj, width, color=_COLOR_FIT, label="Gauss–Jordan")
    ax.bar(x + width / 2, ref, width, color=_COLOR_NUMPY, label="numpy.linalg.solve")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Coefficient value")
    ax.set_title("Solver Agreement — Coefficients")
    ax.legend(frameon=False)
    ax.grid(True, axis="y", alpha=0.3)

    delta: NDArray[np.floating] = np.abs(gj - ref)
    for i, d in enumerate(delta):
        ax.text(i, max(gj[i], ref[i]), f"  |Δ|={d:.1e}", va="bottom", fontsize=9)

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def generate_all_figures(
    fit: PolynomialFit,
    *,
    figures_dir: str | Path = "figures",
    query_time_s: float = 7.0,
) -> dict[str, Path]:
    """Write the standard figure set used by the README and CLI."""
    root = Path(figures_dir)
    root.mkdir(parents=True, exist_ok=True)
    return {
        "velocity_fit": plot_velocity_fit(
            fit,
            output_path=root / "rocket_velocity_fit.png",
            query_time_s=query_time_s,
        ),
        "residuals": plot_sample_residuals(
            fit,
            output_path=root / "rocket_velocity_residuals.png",
        ),
        "acceleration": plot_acceleration_profile(
            fit,
            output_path=root / "rocket_acceleration_profile.png",
            query_time_s=query_time_s,
        ),
        "solver_agreement": plot_solver_agreement(
            fit,
            output_path=root / "solver_coefficient_agreement.png",
        ),
    }
