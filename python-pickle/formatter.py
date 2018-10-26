import pickle

from python_utils.base import BaseFormatter

__version__ = '0.0.1'
DESCRIPTION = 'Python pickle native formatter'


class PickleFormatter(BaseFormatter):
    description = DESCRIPTION
    version = __version__

    def format(self, value):
        try:
            return pickle.loads(value)
        except pickle.PickleError as e:
            return self.process_error(
                message='Cannot unpickle value: {}'.format(e))


if __name__ == "__main__":
    PickleFormatter().main()
