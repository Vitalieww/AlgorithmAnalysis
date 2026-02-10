# python
from decimal import Decimal, getcontext, ROUND_HALF_UP
import math
from typing import Any

def binet_method(n: int) -> int:
    """
    Return F(n) using Binet's formula:
      F(n) = round(phi**n / sqrt(5))
    Uses float for small n and Decimal with increased precision for large n.
    Raises ValueError for non-integer or negative n.
    """
    if not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1

    # for small n floats are exact enough and much faster
    if n <= 70:
        sqrt5 = math.sqrt(5.0)
        phi = (1.0 + sqrt5) / 2.0
        return int(round((phi ** n) / sqrt5))

    # high-precision Decimal path for larger n
    # estimate digits needed: n * log10(phi) + safety margin
    LOG10_PHI = math.log10((1.0 + math.sqrt(5.0)) / 2.0)  # ~0.208987...
    needed_digits = int(n * LOG10_PHI) + 20

    ctx = getcontext()
    old_prec = ctx.prec
    try:
        ctx.prec = max(needed_digits, 50)
        sqrt5 = Decimal(5).sqrt()
        phi = (Decimal(1) + sqrt5) / Decimal(2)
        # Decimal exponentiation to integer power
        val = (phi ** n) / sqrt5
        # round half up to nearest integer
        rounded = val.to_integral_value(rounding=ROUND_HALF_UP)
        return int(rounded)
    finally:
        ctx.prec = old_prec