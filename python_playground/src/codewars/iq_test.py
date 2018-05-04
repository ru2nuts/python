def iq_test(numbers):
    import itertools
    #your code here
    #["Senior" if (c[0] >= 55 and c[1] > 7) else "Open" for c in numbers]
    numbers_ints = [int(c) for c in numbers.split(' ')]
    mods_zip_list = [(i, numbers_ints[i] % 2) for i in range(len(numbers_ints))]
    grouped_list = itertools.groupby(mods_zip_list, key=lambda x: x[1])

    print(grouped_list.list)
    return 0


assert iq_test("2 4 7 8 10"),3
assert iq_test("1 2 2"), 1