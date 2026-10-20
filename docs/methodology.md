# Methodology

This use case reconstructs a continuous rocket velocity profile from three discrete measurements by solving a square linear system for a quadratic interpolant.

## Problem statement

Given samples $`\{(t_i, v_i)\}_{i=1}^{3}`$ with strictly increasing times $`t_i`$, seek coefficients $`a_2, a_1, a_0`$ such that

```math
v(t) = a_2 t^2 + a_1 t + a_0
```

satisfies $`v(t_i) = v_i`$ for each sample.

## Linear system

Enforcing the interpolation conditions yields the Vandermonde system

```math
\begin{bmatrix}
t_1^2 & t_1 & 1 \\
t_2^2 & t_2 & 1 \\
t_3^2 & t_3 & 1 \\
\end{bmatrix}
\begin{bmatrix}
a_2 \\
a_1 \\
a_0 \\
\end{bmatrix}
=
\begin{bmatrix}
v_1 \\
v_2 \\
v_3 \\
\end{bmatrix}
```

With three distinct nodes the coefficient matrix is nonsingular, so the quadratic interpolant is unique.

## Gauss–Jordan elimination

The package solves $`Ax = b`$ by operating on the augmented matrix $`[A \mid b]`$:

1. At column $`k`$, select the row with the largest absolute pivot (partial pivoting).
2. Scale the pivot row so that $`a_{kk} = 1`$.
3. Eliminate all other entries in column $`k`$.
4. After $`n`$ stages, the rightmost column of the reduced matrix is the solution $`x`$.

### Why partial pivoting matters

Vandermonde matrices grow rapidly with the node magnitudes, so the 2-norm condition number

```math
\kappa_2(A) = \|A\|_2 \, \|A^{-1}\|_2
```

can become large even for small systems. A large $`\kappa_2(A)`$ amplifies roundoff: relative perturbations in $`A`$ or $`b`$ of size $`\varepsilon`$ can perturb the computed $`x`$ by roughly $`\kappa_2(A)\,\varepsilon`$.

Partial pivoting chooses the largest available entry in the active column as the pivot. That choice reduces the growth of intermediate multipliers and is the standard first defense against catastrophic cancellation in dense elimination. For this three-point problem the matrix remains modestly conditioned, and the custom solver stays within floating-point agreement of `numpy.linalg.solve`.

## Reference cross-check

After Gauss–Jordan, coefficients are compared against NumPy’s LAPACK-backed solve. Agreement is reported as

```math
\Delta_{\max}
=
\max_j \left| a_j^{\mathrm{GJ}} - a_j^{\mathrm{NumPy}} \right|.
```

For the default samples, $`\Delta_{\max}`$ is on the order of machine epsilon, which confirms that the pedagogical solver reproduces a production reference on this use case.

## Query evaluation

Once the coefficients are known, velocity at any time of interest (for example $`t = 7\,\mathrm{s}`$) is obtained by direct evaluation of $`v(t)`$. Because the model is an exact interpolant of the three samples, residuals at the measurement nodes are expected to be on the order of floating-point roundoff.
