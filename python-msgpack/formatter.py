import argparse
import base64
import binascii
import json
import msgpack
import sys

__version__ = "0.0.1"

ACTION_VALIDATE = "validate"
ACTION_DECODE = "decode"

actions = (ACTION_DECODE, ACTION_VALIDATE)

parser = argparse.ArgumentParser(description='python msgpack native formatter %s' % __version__)
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('action', help="Available actions: %s" % str(actions))
parser.add_argument('value', help="Value encoded with base64")


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

    try:
        decoded_value = base64.b64decode(args.value)
    except binascii.Error as e:
        return process_error("Cannot decode value: %s" % e)

    try:
        unpacked_value = msgpack.unpackb(decoded_value, encoding='utf-8')
    except msgpack.UnpackValueError as e:
        return process_error("Cannot unpack value: %s" % e)

    if args.action == ACTION_VALIDATE:
        return print(json.dumps({
            "valid": True,
            "message": ""
        }))
    else:
        return print(json.dumps({
            "output": repr(unpacked_value),
            "read-only": True,
            "format": "plain_text",
        }))

if __name__ == "__main__":
    main()
