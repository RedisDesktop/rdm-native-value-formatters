import argparse
import base64
import binascii
import json
import gzip
import lz4
import lzma
import snappy
import sys

__version__ = "0.0.1"

ACTION_VALIDATE = "validate"
ACTION_DECODE = "decode"

actions = (ACTION_DECODE, ACTION_VALIDATE)

parser = argparse.ArgumentParser(description='python-pickle native formatter %s' % __version__)
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
        if len(decoded_value) >= 3 and decoded_value[:3] == b'\x1f\x8b\x08':
            unpacked_value = gzip.decompress(decoded_value)
        elif len(decoded_value) >= 26 and decoded_value[:26] == \
                b'\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x00':
            unpacked_value = lzma.decompress(decoded_value)
        elif snappy.isValidCompressed(decoded_value):
            unpacked_value = snappy.uncompress(decoded_value)
        else:
            unpacked_value = lz4.block.decompress(decoded_value)
    except OSError as e:
        return process_error("Cannot decompress value: %s" % e)

    unpacked_value = unpacked_value.decode()

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
