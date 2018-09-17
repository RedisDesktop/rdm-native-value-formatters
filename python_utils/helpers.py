import argparse
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
        if not sys.stdin.isatty():
            sys.stdin.seek(0)
            value = sys.stdin.read()
            return value
        time.sleep(0.1)
    return None
