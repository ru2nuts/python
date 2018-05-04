def countBits(n):
    if n == 0:
        return 0
    import math
    max_2_pow = math.ceil(math.log(n, 2))
    count = sum([1 if (n & (2 ** i)) > 0 else 0 for i in range(0, max_2_pow + 1)])
    return count

print(countBits(1234))
assert countBits(1234), 5
