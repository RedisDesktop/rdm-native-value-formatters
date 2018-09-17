import json
import gzip
import lz4
import lzma
import snappy
import sys

from python_utils.helpers import get_arg_parser, wait_for_stdin_value

__version__ = "0.0.1"
DESCRIPTION = "python native decompressing formatter with gzip, lzma, lz4 " \
              "and snappy support"

ACTION_VALIDATE = "validate"
ACTION_DECODE = "decode"

actions = (ACTION_DECODE, ACTION_VALIDATE)

parser = get_arg_parser(description=DESCRIPTION,
                        version=__version__,
                        actions=actions)


def is_gzip(value):
    return len(value) >= 3 and value[:3] == b'\x1f\x8b\x08'


def is_lzma(value):
    return len(value) >= 26 and value[:26] == \
                                b'\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!' \
                                b'\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x00'


def is_snappy(value):
    return snappy.isValidCompressed(value)


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
        if is_gzip(value):
            unpacked_value = gzip.decompress(value)
        elif is_lzma(value):
            unpacked_value = lzma.decompress(value)
        elif is_snappy(value):
            unpacked_value = snappy.uncompress(value)
        else:
            unpacked_value = lz4.block.decompress(value)
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
