FNV_PRIME = 0x1000193
FNV_OFFSET_BASIS = 0x811C9DC5


def fnv_1a(data):
    hash = FNV_OFFSET_BASIS
    for byte in data:
        hash = hash ^ byte
        hash = hash * FNV_PRIME
        hash &= 0xFFFFFFFF

    return hash


data = input("Enter data: ").encode("utf-8")
hash_value = fnv_1a(data)

print(hash_value)
