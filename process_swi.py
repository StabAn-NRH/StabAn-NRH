import sys
from check_comment import check_comment
from get_immediate import get_immediate


def process_swi(mach_code, args):
    token_count = 0

    mach_code |= 0b1111 << 24
    if len(args) == 0:
        print('ERROR: Invalid value')
        sys.exit(1)

    addr = get_immediate(args[0])

    if addr < 0 or addr > 0xffffff:
        print('ERROR: Invalid value')
        sys.exit(1)
    else:
        mach_code |= addr

    token_count += 1

    args = args[token_count:]
    check_comment(args)
    return mach_code
