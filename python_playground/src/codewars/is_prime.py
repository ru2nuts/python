def is_prime(num):
    for i in range(2, num+1):
        if num > i and num % i == 0:
            return False
    return num > 1