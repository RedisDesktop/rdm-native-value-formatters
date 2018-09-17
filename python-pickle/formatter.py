from __future__ import print_function
import json
import pickle
import sys

from python_utils.helpers import get_arg_parser, wait_for_stdin_value

__version__ = "0.0.1"
DESCRIPTION = "python-pickle native formatter"

ACTION_VALIDATE = "validate"
ACTION_DECODE = "decode"

actions = (ACTION_DECODE, ACTION_VALIDATE)

parser = get_arg_parser(description=DESCRIPTION,
                        version=__version__,
                        actions=actions)


def main():
    args = parser.parse_args()

    if args.action not in actions:
        print("Error: Invalid action %s" % args.action)
        sys.exit(1)

    def process_error(msg):
        if args.action == ACTION_VALIDATE:
            return print(json.dumps({
                "valid": False,
                "message": msg
            }))
        else:
            print(msg)
            sys.exit(2)

    value = wait_for_stdin_value()
    if not value:
        return process_error("No value to format.")

    try:
        unpickled_value = pickle.loads(value)
    except pickle.PickleError as e:
        return process_error("Cannot unpickle value: %s" % e)

    if args.action == ACTION_VALIDATE:
        return print(json.dumps({
            "valid": True,
            "message": ""
        }))
    else:
        return print(json.dumps({
            "output": repr(unpickled_value),
            "read-only": True,
            "format": "plain_text",
        }))


if __name__ == "__main__":
    main()
