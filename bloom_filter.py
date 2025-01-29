import math
from hash_fn import fnv_1a


class BloomFilter:

    filter = []
    p = 0.01
    n = None
    m = None
    k = 1

    def __init__(self, n, p):
        self.capacity = n
        self.p = p

        if n is not None:
            self.m, self.k = self.calculate_optimal_m_k(n, p)
            self.filter = [0] * self.m

    def insert(self, item):
        for hash_value in self.compute_hashes(item):
            self.filter[hash_value] = 1

    def query(self, item):
        for hash_value in self.compute_hashes(item):
            if self.filter[hash_value] == 0:
                return False
        return True

    def compute_hashes(self, item: str):
        hash_values = []

        for i in range(0, self.k):
            seed = str(i + 1)
            data = "%s%s" % (seed, item)
            hash = fnv_1a(data.encode("utf-8"))
            hash_values.append(hash % self.m)

        return hash_values

    @classmethod
    def calculate_optimal_m_k(cls, n, p):
        m = math.ceil((-n * math.log(p)) / (math.log(2) ** 2))
        k = round((m / n) * math.log(2))

        return m, k

    @classmethod
    def from_bytes(cls, bytes_data, num_hash_fns, bit_size):
        bf = cls(n=None, p=0)
        bf.filter = list(bytes_data)
        bf.k = num_hash_fns
        bf.m = bit_size
        return bf
