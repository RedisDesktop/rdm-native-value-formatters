import argparse
import base64
import sys
import time


TIMEOUT = 5


def get_arg_parser(description, version, actions):
    parser = argparse.ArgumentParser(
        description='{} {}'.format(description, version))
    parser.add_argument('-v', '--version', action='version',
                        version=version)
    parser.add_argument('action', help='Available actions: {}'.format(actions))
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
