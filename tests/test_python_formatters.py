import base64
from importlib import import_module
import io
import json
import sys
import unittest

import redis

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

expected_value = {'hello': 'dict'}


class TestBase(unittest.TestCase):
    expected_value = None

    def setUp(self):
        self.db = redis.Redis(db=3)

    def call_formatter(self):
        raise NotImplementedError()

    def get_formatted_output(self, base64_value):
        sys.stdin = io.StringIO(base64_value)
        stdout = sys.stdout
        sys.stdout = io.StringIO()

        self.call_formatter()

        sys.stdin = sys.__stdin__
        output = sys.stdout.getvalue()
        sys.stdout = stdout
        return output

    def check_formatting(self, value):
        base64_value = base64.b64encode(value).decode()
        json_output = self.get_formatted_output(base64_value)
        output = json.loads(json_output)
        formatted_value = eval(output.get('output', ''))

        self.assertEqual(formatted_value, self.expected_value,
                         'Unexpected output: {}'.format(formatted_value))


class TestPythonBinaryFormatter(TestBase):
    formatter = import_module('python-binary.formatter')
    digits_number = 15
    expected_value = '0' * (digits_number + 1)

    def call_formatter(self):
        self.formatter.BinaryFormatter().main('decode')

    def test_binary_format(self):
        key = 'format_demo_binary'
        self.db.delete(key)
        self.db.setbit(key, self.digits_number, 0)
        binary_value = self.db.get(key)

        bitarray = bitstring.BitArray(binary_value)

        self.assertEqual(self.expected_value, bitarray.bin)

    def test_binary_formatter(self):
        value = bitstring.BitArray(bin=self.expected_value).bytes
        self.check_formatting(value)


class TestPythonDecompressingFormatter(TestBase):
    formatter = import_module('python-decompresser.formatter')
    expected_value = binary_values[0]

    def call_formatter(self):
        self.formatter.DecompressingFormatter().main('decode')

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

    def test_snappy_format(self):
        for i, binary in enumerate(binary_values):
            compressed = snappy.compress(binary)
            key = 'format_demo_snappy_{}'.format(i)
            self.db.set(key, compressed)
            decompressed = snappy.uncompress(self.db.get(key))

            self.assertEqual(binary, decompressed)

    def test_gzip_formatter(self):
        value = gzip.compress(self.expected_value)
        self.check_formatting(value)

    def test_lz4_formatter(self):
        value = lz4.block.compress(self.expected_value)
        self.check_formatting(value)

    def test_lzma_formatter(self):
        value = lzma.compress(self.expected_value)
        self.check_formatting(value)

    def test_snappy_formatter(self):
        value = snappy.compress(self.expected_value)
        self.check_formatting(value)


class TestPythonCBORFormatter(TestBase):
    formatter = import_module('python-cbor.formatter')
    expected_value = expected_value

    def call_formatter(self):
        self.formatter.CBORFormatter().main('decode')

    def test_cbor_format(self):
        cbored = cbor.dumps(self.expected_value)
        key = 'format_demo_cbor'
        self.db.set(key, cbored)

        self.assertEqual(self.expected_value, cbor.loads(self.db.get(key)))

    def test_cbor_formatter(self):
        value = cbor.dumps(self.expected_value)
        self.check_formatting(value)


class TestPythonMsgpackFormatter(TestBase):
    formatter = import_module('python-msgpack.formatter')
    expected_value = expected_value

    def call_formatter(self):
        self.formatter.MsgpackFormatter().main('decode')

    def test_msgpack_format(self):
        msgpacked = msgpack.packb(self.expected_value)
        key = 'format_demo_msgpack'
        self.db.set(key, msgpacked)
        unpacked = msgpack.unpackb(self.db.get(key), raw=False)

        self.assertEqual(self.expected_value, unpacked)

    def test_msgpack_formatter(self):
        value = msgpack.packb(self.expected_value)
        self.check_formatting(value)


class TestPythonPickleFormatter(TestBase):
    formatter = import_module('python-pickle.formatter')
    expected_value = expected_value

    def call_formatter(self):
        self.formatter.PickleFormatter().main('decode')

    def test_pickle_format(self):
        pickled = pickle.dumps(self.expected_value)
        key = 'format_demo_pickle'
        self.db.set(key, pickled)

        self.assertEqual(self.expected_value, pickle.loads(self.db.get(key)))

    def test_pickle_formatter(self):
        value = pickle.dumps(self.expected_value)
        self.check_formatting(value)


if __name__ == '__main__':
    unittest.main()
