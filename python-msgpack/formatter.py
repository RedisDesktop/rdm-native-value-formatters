import os
import sys

import msgpack

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from python_utils.base import BaseFormatter

__version__ = '0.0.1'
DESCRIPTION = 'Python msgpack native formatter'


class MsgpackFormatter(BaseFormatter):
    description = DESCRIPTION
    version = __version__

    def format(self, value):
        try:
            return msgpack.unpackb(value, raw=False)
        except msgpack.UnpackValueError as e:
            return self.process_error('Cannot unpack value: {}'.format(e))


if __name__ == "__main__":
    MsgpackFormatter().main()
