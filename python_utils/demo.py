import bitstring
import cbor
import gzip
import lz4
import lzma
import msgpack
import pickle
import snappy

import redis

db = redis.Redis(db=3)


binary_values = [
        b'{"hello": "object"}',
        b'hello string'
    ]

value = {'hello': 'dict'}


def binary_format_demo():
    key = 'format_demo_binary'
    db.setbit(key, 15, 0)
    binary_value = db.get(key)
    try:
        bitstring.BitArray(binary_value)
    except bitstring.Error as e:
        print(e)


def cbor_format_demo():
    cbored = cbor.dumps(value)
    key = 'format_demo_cbor'
    db.set(key, cbored)
    assert value == cbor.loads(db.get(key))


def gzip_format_demo():
    for i, binary in enumerate(binary_values):
        compressed = gzip.compress(binary)
        key = 'format_demo_gzip_{}'.format(i)
        db.set(key, compressed)
        decompressed = gzip.decompress(db.get(key))
        assert binary == decompressed


def lz4_format_demo():
    for i, binary in enumerate(binary_values):
        compressed = lz4.block.compress(binary)
        key = 'format_demo_lz4_{}'.format(i)
        db.set(key, compressed)
        decompressed = lz4.block.decompress(db.get(key))
        assert binary == decompressed


def lzma_format_demo():
    for i, binary in enumerate(binary_values):
        compressed = lzma.compress(binary)
        key = 'format_demo_lzma_{}'.format(i)
        db.set(key, compressed)
        decompressed = lzma.decompress(db.get(key))
        assert binary == decompressed


def msgpack_format_demo():
    msgpacked = msgpack.packb(value)
    key = 'format_demo_msgpack'
    db.set(key, msgpacked)
    assert value == msgpack.unpackb(db.get(key), encoding='utf-8')


def pickle_format_demo():
    pickled = pickle.dumps(value)
    key = 'format_demo_pickle'
    db.set(key, pickled)
    assert value == pickle.loads(db.get(key))


def snappy_format_demo():
    for i, binary in enumerate(binary_values):
        compressed = snappy.compress(binary)
        key = 'format_demo_snappy_{}'.format(i)
        db.set(key, compressed)
        decompressed = snappy.uncompress(db.get(key))
        assert binary == decompressed


if __name__ == '__main__':
    binary_format_demo()
    cbor_format_demo()
    gzip_format_demo()
    lz4_format_demo()
    lzma_format_demo()
    msgpack_format_demo()
    pickle_format_demo()
    snappy_format_demo()
