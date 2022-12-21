import sys


def get_immediate(args):
    if args.startswith('-'):
        if len(args[1:]) > 1 and args[1:3] == '0x':
            try:
                imm = -int(args[3:], 16)
            except:
                print('ERROR: Invalid constant')
                sys.exit(1)
        elif len(args[1:]) > 1 and args[1:3] == '0b':
            try:
                imm = -int(args[3:], 2)
            except:
                print('ERROR: Invalid constant')
                sys.exit(1)
        else:
            try:
                imm = int(args)
            except:
                print('ERROR: Invalid constant')
                sys.exit(1)
    else:
        if len(args) > 1 and args[:2] == '0x':
            try:
                imm = int(args[2:], 16)
            except:
                print('ERROR: Invalid constant')
                sys.exit(1)

        elif len(args) > 1 and args[:2] == '0b':
            try:
                imm = int(args[2:], 2)
            except:
                print('ERROR: Invalid constant')
                sys.exit(1)
        else:
            try:
                imm = int(args)
            except:
                print('ERROR: Invalid constant')
                sys.exit(1)

    return imm
