import os
import sys

import gzip
import lz4.block
import lzma
import snappy

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from python_utils.base import BaseFormatter

__version__ = '0.0.1'
DESCRIPTION = 'Python native decompressing formatter with gzip, lzma, lz4 ' \
              'and snappy support'


def is_gzip(value):
    return len(value) >= 3 and value[:3] == b'\x1f\x8b\x08'


def is_lzma(value):
    return len(value) >= 26 and value[:26] == \
                                b'\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!' \
                                b'\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x00'


def is_snappy(value):
    return snappy.isValidCompressed(value)


class DecompressingFormatter(BaseFormatter):
    description = DESCRIPTION
    version = __version__

    def format(self, value):
        try:
            if is_gzip(value):
                output = gzip.decompress(value)
            elif is_lzma(value):
                output = lzma.decompress(value)
            elif is_snappy(value):
                output = snappy.uncompress(value)
            else:
                output = lz4.block.decompress(value)
            return output
        except OSError as e:
            return self.process_error('Cannot decompress value: {}'.format(e))


if __name__ == "__main__":
    DecompressingFormatter().main()
