import sys
from check_comment import check_comment

registers = {'r0': 0, 'r1': 1, 'r2': 2, 'r3': 3, 'r4': 4,
             'r5': 5, 'r6': 6, 'r7': 7, 'r8': 8, 'r9': 9,
             'r10': 10, 'r11': 11, 'r12': 12, 'r13': 13,
             'r14': 14, 'r15': 15, 'sl': 10, 'fp': 11,
             'ip': 12, 'sp': 13, 'lr': 14, 'pc': 15}


def process_mul_3_args(mach_code, args):
    token_count = 0
    if len(args) == 0:  # length check
        print('ERROR: Invalid operand')
        sys.exit(1)
    if (mach_code >> 21) & 1 == 0:  # tok == mul
        if len(args) <= 3:  # filling destination
            args = args[:3] + [',', args[0]] + args[3:]
        elif args[3][0] == "@":
            args = args[:3] + [',', args[0]] + args[3:]

        if args[0] in registers:  # Rd
            mach_code |= registers[args[0]] << 16
        else:  # destination must be register
            print('ERROR: Invalid operand')
            sys.exit(1)

        token_count += 1

        if args[1] != ',':
            print('ERROR: Invalid syntax')
            sys.exit(1)

        token_count += 1

        if args[2] in registers:  # Rm
            mach_code |= registers[args[2]]
        else:  # 1st operand must be register
            print('ERROR: Invalid operand')
            sys.exit(1)

        token_count += 1

        if len(args) < 4:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[3] != ',':
            print('ERROR: Invalid syntax')
            sys.exit(1)

        token_count += 1

        if len(args) < 5:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[4] in registers:  # Rs
            mach_code |= registers[args[4]] << 8
        else:  # operand is neither register nor constant
            print('ERROR: Invalid operand')
            sys.exit(1)

        token_count += 1
    else:  # tok == mla
        if args[0] in registers:  # Rd
            mach_code |= registers[args[0]] << 16
        else:  # destination must be register
            print('ERROR: Invalid operand')
            sys.exit(1)

        token_count += 1

        if len(args) < 2:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[1] != ',':
            print('ERROR: Invalid syntax')
            sys.exit(1)

        token_count += 1

        if len(args) < 3:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[2] in registers:  # Rm
            mach_code |= registers[args[2]]
        else:  # 1st operand must be register
            print('ERROR: Invalid operand')
            sys.exit(1)

        token_count += 1

        if len(args) < 4:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[3] != ',':
            print('ERROR: Invalid syntax')
            sys.exit(1)

        token_count += 1

        if len(args) < 5:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[4] in registers:  # Rs
            mach_code |= registers[args[4]] << 8
        else:  # operand is neither register nor constant
            print('ERROR: Invalid operand')
            sys.exit(1)

        token_count += 1

        if len(args) < 6:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[5] != ',':
            print('ERROR: Invalid syntax')
            sys.exit(1)

        token_count += 1

        if len(args) < 7:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[6] in registers:  # Rn
            mach_code |= registers[args[6]] << 12
        else:  # operand is neither register nor constant
            print('ERROR: Invalid operand')
            sys.exit(1)

        token_count += 1

    args = args[token_count:]
    check_comment(args)
    return mach_code
