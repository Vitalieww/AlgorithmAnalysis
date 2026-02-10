def _fib_fast_doubling(n):
    if n == 0:
        return (0, 1)

    a, b = _fib_fast_doubling(n // 2)

    c = a * (2 * b - a)        # F(2k)
    d = a * a + b * b          # F(2k + 1)

    if n % 2 == 0:
        return (c, d)
    else:
        return (d, c + d)

def fib_fast_doubling(n):
    return _fib_fast_doubling(n)[0]
