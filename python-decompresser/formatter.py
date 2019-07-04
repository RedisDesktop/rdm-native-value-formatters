from abc import ABC, abstractmethod
import binascii
import json
import logging
import argparse
import base64
import time
import os
import sys

import gzip
import lz4.block
import lzma
try:
    import snappy
    SNAPPY_SUPPORT = True
except ImportError:
    SNAPPY_SUPPORT = False

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


__version__ = '0.0.1'
DESCRIPTION = 'Python native decompressing formatter with gzip, lzma, lz4 ' \
              'and snappy support'


TIMEOUT = 5


def get_arg_parser(description, version, actions):
    parser = argparse.ArgumentParser(
        description='{} {}'.format(description, version))
    parser.add_argument('action', choices=actions,
                        help='Available actions: {}'.format(actions))
    return parser


def wait_for_stdin_value(timeout=TIMEOUT):
    stop = time.time() + timeout
    while time.time() < stop:
        try:
            value = sys.stdin.read()
            return base64.b64decode(value)
        except Exception:
            time.sleep(0.1)
    return None


class BaseFormatter(ABC):
    ACTION_DECODE = 'decode'
    ACTION_INFO = 'info'
    ACTION_VALIDATE = 'validate'

    actions = (ACTION_DECODE, ACTION_INFO, ACTION_VALIDATE)

    def __init__(self, debug=True):
        self.logger = logging.getLogger()

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    @property
    @abstractmethod
    def description(self):
        return DESCRIPTION

    @property
    @abstractmethod
    def version(self):
        return __version__

    @abstractmethod
    def format(self, value):
        raise NotImplementedError()

    def process_error(self, message):
        if self.action == self.ACTION_VALIDATE:
            print(json.dumps({
                'valid': False,
                'error': message
            }))
        else:
            self.logger.error(message)
            sys.exit(2)

    def validate_action(self, action):
        if action not in self.actions:
            self.logger.error('Error: Invalid action {}'.format(action))
            sys.exit(1)
        self.action = action

    @staticmethod
    def valid_output():
        print(json.dumps({
            'valid': True,
            'error': ''
        }))

    def info_output(self):
        print(json.dumps({
            'version': self.version,
            'description': self.description
        }))

    @staticmethod
    def formatted_output(output):
        def get_output_dict(output):
            return {
                'output': output,
                'read-only': True,
                'format': 'plain_text',
            }

        if hasattr(output, 'decode'):
            output = output.decode()

        try:
            json_output = json.dumps(get_output_dict(output))
        except (TypeError, OverflowError):
            json_output = json.dumps(get_output_dict(repr(output)))

        print(json_output)

    def main(self, *args):
        parser = get_arg_parser(description=self.description,
                                version=self.version,
                                actions=self.actions)
        if args:
            args = parser.parse_args(args)
        else:
            args = parser.parse_args()

        self.validate_action(args.action)

        if self.action == self.ACTION_INFO:
            return self.info_output()

        try:
            value = wait_for_stdin_value()
        except binascii.Error as e:
            return self.process_error('Cannot decode value: {}'.format(e))

        if not value:
            return self.process_error('No value to format.')

        try:
            output = self.format(value=value)
        except Exception as e:
            return self.process_error('Cannot format value: {}'.format(e))

        if self.action == self.ACTION_VALIDATE:
            return self.valid_output()

        return self.formatted_output(output)


class DecompressingFormatter(BaseFormatter):
    description = DESCRIPTION
    version = __version__

    def format(self, value):

        def is_gzip(value):
            return len(value) >= 3 and value[:3] == b'\x1f\x8b\x08'

        def is_lzma(value):
            return len(value) >= 26 and value[:26] == \
                   b'\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!' \
                   b'\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x00'

        def is_snappy(value):
            return snappy.isValidCompressed(value)

        try:
            if is_gzip(value):
                output = gzip.decompress(value)
            elif is_lzma(value):
                output = lzma.decompress(value)
            elif is_snappy(value):
                if SNAPPY_SUPPORT:
                    output = snappy.uncompress(value)
                else:
                    return self.process_error(
                        'Cannot decompress value: '
                        'Snappy is not available on this system.')
            else:
                output = lz4.block.decompress(value)
            return output
        except OSError as e:
            return self.process_error('Cannot decompress value: {}'.format(e))


if __name__ == "__main__":
    DecompressingFormatter().main()
