import sys
from check_comment import check_comment
from get_immediate import get_immediate

registers = {'r0': 0, 'r1': 1, 'r2': 2, 'r3': 3, 'r4': 4,
             'r5': 5, 'r6': 6, 'r7': 7, 'r8': 8, 'r9': 9,
             'r10': 10, 'r11': 11, 'r12': 12, 'r13': 13,
             'r14': 14, 'r15': 15, 'sl': 10, 'fp': 11,
             'ip': 12, 'sp': 13, 'lr': 14, 'pc': 15}

shifts = {'lsl': 0, 'lsr': 1, 'asl': 0, 'asr': 2, 'ror': 3, 'rrx': 3}


def process_2_args(mach_code, args):
    token_count = 0

    if len(args) == 0:  # length check
        print('ERROR: Invalid operand')
        sys.exit(1)

    if args[0] in registers:
        mach_code |= registers[args[0]] << 12
    else:  # destination must be register
        print('ERROR: Invalid operand')
        sys.exit(1)

    token_count += 1

    if len(args) < 2:  # length check
        print('ERROR: Invalid syntax')
        sys.exit(1)

    if args[1] != ',':
        print('ERROR: Invalid syntax')
        sys.exit(1)

    token_count += 1

    if len(args) < 3:  # length check
        print('ERROR: Invalid operand')
        sys.exit(1)

    if args[2] in registers:
        mach_code |= registers[args[2]]

        token_count += 1

        if len(args) > 3:
            if args[3][0] == '@':
                return mach_code

            if args[3] != ',':
                print('ERROR: Invalid syntax')
                sys.exit(1)

            token_count += 1

            if len(args) < 5:  # length check
                print('ERROR: Invalid shift expression')
                sys.exit(1)

            if args[4] in shifts:
                rm_shift = shifts[args[4]]
            else:
                print('ERROR: Invalid shift expression')
                sys.exit(1)

            token_count += 1

            if args[4] == "rrx":  # args[5] == null
                mach_code |= rm_shift << 5
            else:  # args[5] != null
                if len(args) < 6:  # length check
                    print('ERROR: Invalid shift expression')
                    sys.exit(1)
                if args[5] in registers:
                    mach_code |= registers[args[5]] << 8
                    mach_code |= rm_shift << 5
                    mach_code |= 1 << 4

                elif args[5] == '#':
                    token_count += 1

                    if len(args) < 7:  # length check
                        print('ERROR: Invalid operand')
                        sys.exit(1)

                    imm = get_immediate(args[6])

                    if imm < 0 or imm > 32:
                        print('ERROR: Invalid shift amount')
                        sys.exit(1)
                    elif imm == 0:
                        pass
                    elif 0 < imm < 32:
                        mach_code |= imm << 7
                        mach_code |= rm_shift << 5
                    elif (args[4] == "lsr" or args[4] == "asr") and imm == 32:
                        mach_code |= rm_shift << 5
                    else:
                        print('ERROR: Invalid shift amount')
                        sys.exit(1)
                else:
                    print('ERROR: Invalid syntax')
                    sys.exit(1)

                token_count += 1

    elif args[2] == '#':
        mach_code |= 1 << 25

        token_count += 1

        if len(args) < 4:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        imm = get_immediate(args[3])

        if imm < 0:
            imm = -imm - 1  # using concept of 2's complement
            mach_code ^= 1 << 22  # mvn -> mov or # mov -> mvn

        zero_count = 0

        while imm % 2 == 0 and imm >= 256:
            imm //= 2
            zero_count += 1
        while zero_count != 0 and imm % 2 == 0:
            imm //= 2
            zero_count += 1
        if zero_count % 2 != 0 and imm * 2 < 256:
            imm *= 2
            zero_count -= 1

        if imm < 256 and zero_count % 2 == 0:
            if zero_count == 0:
                pass
            else:
                print('\timmediate rotated')
                mach_code |= (32 - zero_count) // 2 << 8
        else:
            print('ERROR: Invalid constant')
            sys.exit(1)

        token_count += 1

        mach_code |= imm
    else:  # operand is neither register nor constant
        print('ERROR: Invalid operand')
        sys.exit(1)

    args = args[token_count:]
    check_comment(args)
    return mach_code
