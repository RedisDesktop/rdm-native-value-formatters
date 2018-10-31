import redis
import unittest

import bitstring
import cbor
import gzip
import lz4.block
import lzma
import msgpack
import pickle
import snappy


REDIS_DB = 3

binary_values = [
    b'{"hello": "object"}',
    b'hello string'
]

value = {'hello': 'dict'}


class TestPythonFormatters(unittest.TestCase):
    def setUp(self):
        self.db = redis.Redis(db=3)

    def test_binary_format(self):
        key = 'format_demo_binary'
        digits_count = 15
        self.db.setbit(key, digits_count, 0)
        binary_value = self.db.get(key)
        self.db.delete(key)
        bitarray = bitstring.BitArray(binary_value)

        self.assertEqual('0' * (digits_count + 1), bitarray.bin)

    def test_cbor_format(self):
        cbored = cbor.dumps(value)
        key = 'format_demo_cbor'
        self.db.set(key, cbored)

        self.assertEqual(value, cbor.loads(self.db.get(key)))

    def test_gzip_format(self):
        for i, binary in enumerate(binary_values):
            compressed = gzip.compress(binary)
            key = 'format_demo_gzip_{}'.format(i)
            self.db.set(key, compressed)
            decompressed = gzip.decompress(self.db.get(key))

            self.assertEqual(binary, decompressed)

    def test_lz4_format(self):
        for i, binary in enumerate(binary_values):
            compressed = lz4.block.compress(binary)
            key = 'format_demo_lz4_{}'.format(i)
            self.db.set(key, compressed)
            decompressed = lz4.block.decompress(self.db.get(key))

            self.assertEqual(binary, decompressed)

    def test_lzma_format(self):
        for i, binary in enumerate(binary_values):
            compressed = lzma.compress(binary)
            key = 'format_demo_lzma_{}'.format(i)
            self.db.set(key, compressed)
            decompressed = lzma.decompress(self.db.get(key))

            self.assertEqual(binary, decompressed)

    def test_msgpack_format(self):
        msgpacked = msgpack.packb(value)
        key = 'format_demo_msgpack'
        self.db.set(key, msgpacked)
        unpacked = msgpack.unpackb(self.db.get(key), encoding='utf-8')

        self.assertEqual(value, unpacked)

    def test_pickle_format(self):
        pickled = pickle.dumps(value)
        key = 'format_demo_pickle'
        self.db.set(key, pickled)

        self.assertEqual(value, pickle.loads(self.db.get(key)))

    def test_snappy_format(self):
        for i, binary in enumerate(binary_values):
            compressed = snappy.compress(binary)
            key = 'format_demo_snappy_{}'.format(i)
            self.db.set(key, compressed)
            decompressed = snappy.uncompress(self.db.get(key))

            self.assertEqual(binary, decompressed)


if __name__ == '__main__':
    unittest.main()
