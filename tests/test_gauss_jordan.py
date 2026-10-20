"""Unit tests for the Gauss–Jordan solver."""

from __future__ import annotations

import numpy as np
import pytest

from rocket_velocity.solvers.gauss_jordan import gauss_jordan_solve


def test_solves_well_conditioned_system() -> None:
    a = np.array([[2.0, 1.0], [1.0, 3.0]])
    b = np.array([5.0, 10.0])
    x = gauss_jordan_solve(a, b)
    np.testing.assert_allclose(a @ x, b, atol=1e-12)


def test_matches_numpy_for_vandermonde() -> None:
    t = np.array([2.0, 5.0, 9.0])
    a = np.column_stack([t**2, t, np.ones_like(t)])
    b = np.array([45.948, 119.985, 231.497])
    x = gauss_jordan_solve(a, b)
    np.testing.assert_allclose(x, np.linalg.solve(a, b), rtol=1e-10, atol=1e-10)


def test_rejects_singular_matrix() -> None:
    a = np.array([[1.0, 2.0], [2.0, 4.0]])
    b = np.array([3.0, 6.0])
    with pytest.raises(ValueError, match="Singular"):
        gauss_jordan_solve(a, b)
