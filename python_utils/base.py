from abc import ABC, abstractmethod, abstractproperty
import binascii
import json
import logging
import sys

from python_utils.helpers import get_arg_parser, wait_for_stdin_value

__version__ = '0.0.1'
DESCRIPTION = 'Python generic formatter'

ACTION_DECODE = 'decode'
ACTION_INFO = 'info'
ACTION_VALIDATE = 'validate'


class BaseFormatter(ABC):
    actions = (ACTION_DECODE, ACTION_INFO, ACTION_VALIDATE)

    def __init__(self, debug=True):
        self.logger = logging.getLogger()

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)


    @abstractproperty
    def description(self):
        return DESCRIPTION

    @abstractproperty
    def version(self):
        return __version__

    @abstractmethod
    def format(self, value):
        raise NotImplementedError()

    def process_error(self, message):
        if self.action == ACTION_VALIDATE:
            return print(json.dumps({
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
    def return_valid():
        return print(json.dumps({
            'valid': True,
            'error': ''
        }))

    def return_info(self):
        return print(json.dumps({
            'version': self.version,
            'description': self.description
        }))

    def return_formatted_output(self, output):
        if self.action == ACTION_VALIDATE:
            self.return_valid()
        else:
            return print(json.dumps({
                'output': repr(output),
                'read-only': True,
                'format': 'plain_text',
            }))

    def main(self, *args):
        parser = get_arg_parser(description=self.description,
                                version=self.version,
                                actions=self.actions)
        args = parser.parse_args(args)
        self.validate_action(args.action)

        if self.action == ACTION_INFO:
            self.return_info()

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

        self.return_formatted_output(output)
