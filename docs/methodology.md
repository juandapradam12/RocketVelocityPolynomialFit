# Methodology

This use case reconstructs a continuous rocket velocity profile from three discrete measurements by solving a square linear system for a quadratic interpolant.

## Problem statement

Given samples $\{(t_i, v_i)\}_{i=1}^{3}$ with strictly increasing times $t_i$, seek coefficients $a_2, a_1, a_0$ such that

$$
v(t) = a_2 t^2 + a_1 t + a_0
$$

satisfies $v(t_i) = v_i$ for each sample.

## Linear system

Enforcing the interpolation conditions yields the Vandermonde system

$$
\begin{bmatrix}
t_1^2 & t_1 & 1 \\
t_2^2 & t_2 & 1 \\
t_3^2 & t_3 & 1
\end{bmatrix}
\begin{bmatrix}
a_2 \\
a_1 \\
a_0
\end{bmatrix}
=
\begin{bmatrix}
v_1 \\
v_2 \\
v_3
\end{bmatrix}.
$$

With three distinct nodes the coefficient matrix is nonsingular, so the quadratic interpolant is unique.

## Gauss–Jordan elimination

The package solves $Ax = b$ by operating on the augmented matrix $[A \mid b]$:

1. At column $k$, select the row with the largest absolute pivot (partial pivoting).
2. Scale the pivot row so that $a_{kk} = 1$.
3. Eliminate all other entries in column $k$.
4. After $n$ stages, the rightmost column of the reduced matrix is the solution $x$.

Partial pivoting improves numerical robustness relative to a naïve elimination without row exchanges.

## Query evaluation

Once the coefficients are known, velocity at any time of interest (for example $t = 7\,\mathrm{s}$) is obtained by direct evaluation of $v(t)$. Because the model is an exact interpolant of the three samples, residuals at the measurement nodes are expected to be on the order of floating-point roundoff.
