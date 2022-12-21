import sys


def check_comment(args):
    if len(args) > 0 and args[0][0] != '@':
        print('ERROR: Garbage instruction found')
        sys.exit(1)
