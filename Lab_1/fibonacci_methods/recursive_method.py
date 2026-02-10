def recursive_method(n):
    if n <= 1:
        return n
    else:
        return recursive_method(n-1) + recursive_method(n-2)