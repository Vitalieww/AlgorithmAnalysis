from typing import List

def _mat_mult(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """Multiply two 2x2 matrices."""
    return [
        [a[0][0]*b[0][0] + a[0][1]*b[1][0],
         a[0][0]*b[0][1] + a[0][1]*b[1][1]],
        [a[1][0]*b[0][0] + a[1][1]*b[1][0],
         a[1][0]*b[0][1] + a[1][1]*b[1][1]],
    ]

def _mat_pow(mat: List[List[int]], exp: int) -> List[List[int]]:
    """Fast exponentiation (binary exponentiation) for 2x2 matrices."""
    # Identity matrix
    result = [[1, 0], [0, 1]]
    base = [row[:] for row in mat]
    e = exp
    while e > 0:
        if e & 1:
            result = _mat_mult(result, base)
        base = _mat_mult(base, base)
        e >>= 1
    return result

def matrix_power_method(n: int) -> int:
    """
    Return F(n) where F(0)=0, F(1)=1 using matrix power method.
    Raises ValueError for negative or non-integer n.
    """
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    # Fibonacci matrix
    M = [[1, 1], [1, 0]]
    # M^(n-1) * [F(1), F(0)]^T => top-left element is F(n)
    P = _mat_pow(M, n - 1)
    return P[0][0]