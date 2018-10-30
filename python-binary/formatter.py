import os
import sys

import bitstring

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from python_utils.base import BaseFormatter

__version__ = '0.0.1'
DESCRIPTION = 'Python native binary formatter'


class BinaryFormatter(BaseFormatter):
    description = DESCRIPTION
    version = __version__

    def format(self, value):
        try:
            return bitstring.BitArray(value).bin
        except bitstring.Error as e:
            return self.process_error('Cannot format value: {}'.format(e))


if __name__ == "__main__":
    BinaryFormatter().main()
