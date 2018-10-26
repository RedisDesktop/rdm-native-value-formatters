import cbor

from python_utils.base import BaseFormatter

__version__ = '0.0.1'
DESCRIPTION = 'Python CBOR native formatter'


class CBORFormatter(BaseFormatter):
    description = DESCRIPTION
    version = __version__

    def format(self, value):
        try:
            return cbor.loads(value)
        except ValueError as e:
            return self.process_error(
                message='Cannot format value: {}'.format(e))


if __name__ == "__main__":
    CBORFormatter().main()
