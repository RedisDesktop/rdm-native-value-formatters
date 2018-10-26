import binascii
import json
import os
import sys

from python_utils.helpers import get_arg_parser, wait_for_stdin_value

__version__ = '0.0.1'
ACTION_DECODE = 'decode'
ACTION_VALIDATE = 'validate'


class BaseFormatter:
    def __init__(self):
        sys.path.append(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        parser = get_arg_parser(description=self.description,
                                version=self.version,
                                actions=self.actions)
        args = parser.parse_args()
        action = args.action

        if action not in self.actions:
            print('Error: Invalid action {}'.format(action))
            sys.exit(1)

        self.action = action

    description = 'Python generic formatter'
    actions = (ACTION_DECODE, ACTION_VALIDATE)
    version = __version__

    def format(self, value):
        raise NotImplementedError()

    def process_error(self, message):
        if self.action == ACTION_VALIDATE:
            return print(json.dumps({
                'valid': False,
                'message': message
            }))
        else:
            print(message)
            sys.exit(2)

    def main(self):
        try:
            value = wait_for_stdin_value()
        except binascii.Error as e:
            return self.process_error('Cannot decode value: {}'.format(e))

        if not value:
            return self.process_error(message='No value to format.')

        try:
            output = self.format(value=value).decode()
        except UnicodeDecodeError as e:
            return self.process_error(
                message='Cannot decode value: {}'.format(e))
        except Exception as e:
            return self.process_error(
                message='Cannot format value: {}'.format(e))

        if self.action == ACTION_VALIDATE:
            return print(json.dumps({
                'valid': True,
                'message': ''
            }))
        else:
            return print(json.dumps({
                'output': repr(output),
                'read-only': True,
                'format': 'plain_text',
            }))
