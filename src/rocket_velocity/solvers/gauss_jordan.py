"""Gauss–Jordan elimination with partial pivoting."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def gauss_jordan_solve(
    matrix: NDArray[np.floating],
    rhs: NDArray[np.floating],
    *,
    atol: float = 1e-12,
) -> NDArray[np.floating]:
    r"""Solve \(Ax = b\) by reducing the augmented matrix to reduced row echelon form.

    Parameters
    ----------
    matrix:
        Square coefficient matrix \(A\).
    rhs:
        Right-hand side vector \(b\).
    atol:
        Absolute tolerance used to detect singular pivots.

    Returns
    -------
    NDArray[np.floating]
        Solution vector \(x\).

    Raises
    ------
    ValueError
        If shapes are incompatible or the system is singular.
    """
    a = np.asarray(matrix, dtype=float)
    b = np.asarray(rhs, dtype=float).reshape(-1)

    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("matrix must be square.")
    if b.ndim != 1 or b.shape[0] != a.shape[0]:
        raise ValueError("rhs must be a vector with length equal to matrix dimension.")

    n = a.shape[0]
    augmented = np.concatenate([a, b.reshape(n, 1)], axis=1)

    for col in range(n):
        pivot_row = col + int(np.argmax(np.abs(augmented[col:, col])))
        pivot = augmented[pivot_row, col]
        if abs(pivot) <= atol:
            raise ValueError("Singular system: no usable pivot found.")

        if pivot_row != col:
            augmented[[col, pivot_row]] = augmented[[pivot_row, col]]

        augmented[col] /= augmented[col, col]

        for row in range(n):
            if row == col:
                continue
            augmented[row] -= augmented[row, col] * augmented[col]

    return augmented[:, -1].copy()
