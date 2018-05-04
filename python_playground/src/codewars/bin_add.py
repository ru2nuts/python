def add_binary(a, b):
    # your code here
    c = a + b
    import math
    max_2_pow = int(math.floor(math.log(c, 2)))
    return "".join(["1" if (c & (2 ** i)) > 0 else "0" for i in range(max_2_pow, -1, -1)])


print(add_binary(5, 9), "1110")
print(add_binary(0, 1), "1")
print(add_binary(1, 1), "10")
print(add_binary(0, 1), "1")
print(add_binary(1, 0), "1")
print(add_binary(2, 2), "100")
print(add_binary(51, 12), "111111")
