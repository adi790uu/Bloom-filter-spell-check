import sys
import struct
from src.bloom_filter import BloomFilter


def build_bloom_filter_from_file_path(file_path, false_postive_rate):
    words_count = None
    with open(file_path, "r") as file:
        words = [line.strip() for line in file]

        words_count = len(words)
        bloom_filter = BloomFilter(n=words_count, p=false_postive_rate)
        for word in words:
            bloom_filter.insert(word)

        return bloom_filter


def load_bloom_filter(file_path) -> BloomFilter:
    with open(file_path, "rb") as file:
        header = file.read(12)
        file_type, version, num_of_hash_fn, filter_length = struct.unpack(
            ">4sHHI", header
        )

        if file_type != b"CCBF" or version != 1:
            raise ValueError("Invalid file type or version")

        filter_bytes = file.read(filter_length)
        bloom_filter = BloomFilter.from_bytes(
            bytes_data=filter_bytes,
            num_hash_fns=num_of_hash_fn,
            bit_size=filter_length,
        )
        return bloom_filter


def check_spelling(words):
    bloom_filter = load_bloom_filter("./words.bf")
    spelt_wrong = []
    for word in words:
        result = bloom_filter.query(word)
        if not result:
            spelt_wrong.append(word)

    return f"These words are spelt wrong:\n{"\n ".join(spelt_wrong)}"


if __name__ == "__main__":
    if sys.argv[1] == "-build":
        dictionary_file_path = sys.argv[2]
        print(dictionary_file_path)
        output_file = "words.bf"
        bloom_filter = build_bloom_filter_from_file_path(
            dictionary_file_path, false_postive_rate=0.1
        )

        header = struct.pack(
            ">4sHHI", b"CCBF", 1, bloom_filter.k, len(bloom_filter.filter)
        )
        filter_bytes = bytes(bloom_filter.filter)

        with open(output_file, "wb") as file:
            file.write(header)
            file.write(filter_bytes)

    elif sys.argv[1] == "-check":
        words = sys.argv[2:]
        print(check_spelling(words))
