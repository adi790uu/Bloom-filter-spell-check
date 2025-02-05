from src.bloom_filter import BloomFilter


def test_calculation_of_optimal_m_and_k():
    n = 1000
    p = 0.01
    m, k = BloomFilter.calculate_optimal_m_k(n=n, p=p)
    assert m == 9586 and k == 7


def test_bloom_filter_init():
    bf = BloomFilter(n=1000, p=0.01)
    assert bf.capacity == 1000
    assert bf.p == 0.01
    assert len(bf.filter) == bf.m


def test_insert_and_query():
    bf = BloomFilter(n=1000, p=0.01)
    bf.insert("item")
    assert bf.query("item") is True
    assert bf.query("random") is False


def test_from_bytes():
    bf = BloomFilter(n=1000, p=0.01)
    bf.insert("item1")
    bytes_data = bytes(bf.filter)
    new_bf = BloomFilter.from_bytes(bytes_data, bf.k, bf.m)
    assert new_bf.query("item1") is True
    assert new_bf.query("item2") is False
