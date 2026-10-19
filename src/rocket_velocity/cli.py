"""Command-line entry point for the rocket velocity use case."""

from __future__ import annotations

import argparse
from pathlib import Path

from rocket_velocity.data import DEFAULT_OBSERVATIONS
from rocket_velocity.fitting.polynomial import fit_quadratic_velocity
from rocket_velocity.visualization import plot_velocity_fit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fit a quadratic polynomial to rocket velocity samples "
            "using Gauss–Jordan elimination."
        )
    )
    parser.add_argument(
        "--query-time",
        type=float,
        default=7.0,
        help="Time (s) at which to evaluate the fitted velocity (default: 7).",
    )
    parser.add_argument(
        "--figure",
        type=Path,
        default=Path("figures/rocket_velocity_fit.png"),
        help="Output path for the fit figure.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    fit = fit_quadratic_velocity(DEFAULT_OBSERVATIONS)
    coeffs = fit.coefficients
    velocity = float(fit.predict(args.query_time))
    figure_path = plot_velocity_fit(
        fit,
        output_path=args.figure,
        query_time_s=args.query_time,
    )

    print("Quadratic model: v(t) = a2·t² + a1·t + a0")
    print(f"  a2 = {coeffs.a2:.6f}")
    print(f"  a1 = {coeffs.a1:.6f}")
    print(f"  a0 = {coeffs.a0:.6f}")
    print(f"v({args.query_time:g} s) = {velocity:.6f} m/s")
    print(f"Residual L2 norm at samples: {fit.residual_norm:.3e}")
    print(f"Design-matrix condition number κ₂(A): {fit.condition_number:.3e}")
    print(
        "Max |Δa| vs numpy.linalg.solve: "
        f"{fit.numpy_max_abs_coeff_delta:.3e}"
    )
    print(f"Figure written to: {figure_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
