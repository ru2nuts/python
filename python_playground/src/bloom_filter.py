from hashlib import sha1
from bitarray import bitarray
from struct import unpack

bit_array = bitarray(160)
slice = 2 ^ 40 - 1

bit_array.setall(0)


def bloom_put(key: str):
    hashfn = sha1(key.encode('utf-8'))
    hd = hashfn.hexdigest()
    uhd = unpack(b'!QQQQQ', hd.encode('utf-8'))

    slice1pos = uhd[0] % slice
    slice2pos = uhd[1] % slice
    slice3pos = uhd[2] % slice
    slice4pos = uhd[3] % slice

    bit_array[slice1pos + slice * 0] = 1
    bit_array[slice2pos + slice * 1] = 1
    bit_array[slice3pos + slice * 2] = 1
    bit_array[slice4pos + slice * 3] = 1


def bloom_test(key: str) -> bool:
    hashfn = sha1(key.encode('utf-8'))
    hd = hashfn.hexdigest()
    uhd = unpack(b'!QQQQQ', hd.encode('utf-8'))

    slice1pos = uhd[0] % slice
    slice2pos = uhd[1] % slice
    slice3pos = uhd[2] % slice
    slice4pos = uhd[3] % slice

    return bit_array[slice1pos + slice * 0] == 1 and \
           bit_array[slice2pos + slice * 1] == 1 and \
           bit_array[slice3pos + slice * 2] == 1 and \
           bit_array[slice4pos + slice * 3] == 1


print('=== Storing values into Bloom Filter ===')

for c in ['a', 'b', 'c', 'd', 'e', 'f', 'w', 'x', 'y', 'z']:
    bloom_put(c)
    print(bit_array)
    print('******')

print('=== Tesging if values are in Bloom Filter ===')

print('=== True ===')

for c in ['a', 'b', 'c', 'd', 'e', 'f', 'w', 'x', 'y', 'z']:
    print(bloom_test(c))
    print(bit_array)

print('=== False ===')

for c in ['g', 'h', 'i']:
    print(bloom_test(c))
    print(bit_array)

for c in range(1, 70):
    bloom_put(str(c))
    print(bit_array)
