import sys
from get_immediate import get_immediate
from check_comment import check_comment

registers = {'r0': 0, 'r1': 1, 'r2': 2, 'r3': 3, 'r4': 4,
             'r5': 5, 'r6': 6, 'r7': 7, 'r8': 8, 'r9': 9,
             'r10': 10, 'r11': 11, 'r12': 12, 'r13': 13,
             'r14': 14, 'r15': 15, 'sl': 10, 'fp': 11,
             'ip': 12, 'sp': 13, 'lr': 14, 'pc': 15}

shifts = {'lsl': 0, 'lsr': 1, 'asl': 0, 'asr': 2, 'ror': 3, 'rrx': 3}


def process_data_transfer(mach_code, args):
    token_count = 0

    if len(args) == 0:  # length check
        print('ERROR: Invalid operand')
        sys.exit(1)

    if args[0] in registers:  # Rd
        mach_code |= registers[args[0]] << 12
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

    if args[2] != '[':
        print('ERROR: Invalid operand')
        sys.exit(1)

    token_count += 1

    if len(args) < 4:  # length check
        print('ERROR: Invalid operand')
        sys.exit(1)

    if args[3] in registers:  # Rn
        mach_code |= registers[args[3]] << 16
    else:
        print('ERROR: Invalid operand')
        sys.exit(1)

    token_count += 1

    if len(args) < 5:  # length check
        print('ERROR: Invalid operand')
        sys.exit(1)
    if args[4] == ']':  # post index
        token_count += 1

        if len(args) > 5:
            if args[5] == ',':
                token_count += 1
                if len(args) < 7:  # length check
                    print('ERROR: Invalid operand')
                    sys.exit(1)

                if args[6] == '#':
                    token_count += 1

                    if len(args) < 8:  # length check
                        print('ERROR: Invalid operand')
                        sys.exit(1)

                    imm = get_immediate(args[7])

                    if abs(imm) > 4095:
                        print('ERROR: Invalid constant')
                        sys.exit(1)
                    elif imm < 0:
                        mach_code |= (-imm)
                    else:
                        mach_code |= 1 << 23
                        mach_code |= imm

                    token_count += 1
                else:
                    if args[6].startswith('-'):
                        if args[6].strip('-') in registers:  # Rm
                            if registers[args[6].strip('-')] == 15:
                                print('ERROR: Cannot use pc register for register indexing with pc-relative')
                                sys.exit(1)
                            token_count += 1

                            mach_code |= 1 << 25
                            mach_code |= registers[args[6].strip('-')]

                    else:
                        mach_code |= 1 << 23
                        if args[6] in registers:  # Rm
                            if registers[args[6]] == 15:
                                print('ERROR: Cannot use pc register for register indexing with pc-relative')
                                sys.exit(1)
                            token_count += 1

                            mach_code |= 1 << 25
                            mach_code |= registers[args[6]]

                    if len(args) > 7:  # length check
                        if args[7] != ',':
                            print('ERROR: Invalid syntax')
                            sys.exit(1)

                        token_count += 1

                        if len(args) < 9:  # length check
                            print('ERROR: Invalid operand')
                            sys.exit(1)

                        if args[8] in shifts:
                            mach_code |= shifts[args[8]] << 5
                        else:
                            print('ERROR: Invalid shift expression')
                            sys.exit(1)

                        token_count += 1

                        if args[8] == "rrx":
                            token_count += 1
                        else:
                            if len(args) < 10:  # length check
                                print('ERROR: Invalid shift expression')
                                sys.exit(1)

                            if args[9] != '#':
                                print('ERROR: Invalid shift expression (use immediate)')
                                sys.exit(1)

                            token_count += 1

                            if len(args) < 11:  # length check
                                print('ERROR: Invalid shift expression')
                                sys.exit(1)

                            imm = get_immediate(args[10])

                            if imm < 0 or imm > 32:
                                print('ERROR: Invalid shift amount')
                                sys.exit(1)
                            elif imm == 0:
                                pass
                            elif 0 < imm < 32:
                                mach_code |= imm << 7
                            elif (args[7] == "lsr" or args[7] == "asr") and imm == 32:
                                pass
                            else:
                                print('ERROR: Invalid shift amount')
                                sys.exit(1)

                            token_count += 1
            elif args[5] == '!':
                mach_code |= 1 << 21
                mach_code |= 1 << 23
                mach_code |= 1 << 24
                token_count += 1
            elif args[5] == '@':
                pass
            else:
                print('ERROR: Invalid syntax')
                sys.exit(1)
        else:
            mach_code |= 1 << 23
            mach_code |= 1 << 24

    else:  # pre index
        mach_code |= 1 << 24
        if args[4] != ',':
            print('ERROR: Invalid syntax')
            sys.exit(1)

        token_count += 1

        if len(args) < 6:  # length check
            print('ERROR: Invalid operand')
            sys.exit(1)

        if args[5] == '#':
            token_count += 1

            if len(args) < 7:  # length check
                print('ERROR: Invalid operand')
                sys.exit(1)

            imm = get_immediate(args[6])

            if abs(imm) > 4095:
                print('ERROR: Invalid constant')
                sys.exit(1)
            elif imm < 0:
                mach_code |= (-imm)
            else:
                mach_code |= 1 << 23
                mach_code |= imm

            token_count += 1

            if len(args) < 8:  # length check
                print('ERROR: Invalid operand')
                sys.exit(1)

            if args[7] != ']':
                print('ERROR: Invalid operand')
                sys.exit(1)

            token_count += 1

            if len(args) > 8:
                if args[8] == '!':
                    mach_code |= 1 << 21
                elif args[8] == '@':
                    pass
                else:
                    print('ERROR: Invalid syntax')
                    sys.exit(1)
                token_count += 1
        else:
            if args[5].startswith('-'):
                if args[5].strip('-') in registers:  # Rm
                    if registers[args[5].strip('-')] == 15:
                        print('ERROR: Cannot use pc register for register indexing with pc-relative')
                        sys.exit(1)
                    token_count += 1

                    mach_code |= 1 << 25
                    mach_code |= registers[args[5].strip('-')]

            else:
                mach_code |= 1 << 23
                if args[5] in registers:  # Rm
                    if registers[args[5]] == 15:
                        print('ERROR: Cannot use pc register for register indexing with pc-relative')
                        sys.exit(1)
                    token_count += 1

                    mach_code |= 1 << 25
                    mach_code |= registers[args[5]]

            if len(args) < 7:  # length check
                print('ERROR: Invalid operand')
                sys.exit(1)

            if args[6] == ']':
                token_count += 1

                if len(args) > 7:
                    if args[7] == '!':
                        mach_code |= 1 << 21
                    elif args[7] == '@':
                        pass
                    else:
                        print('ERROR: Invalid syntax')
                        sys.exit(1)
                    token_count += 1

            elif args[6] == ',':
                token_count += 1

                if len(args) < 8:  # length check
                    print('ERROR: Invalid operand')
                    sys.exit(1)

                if args[7] in shifts:
                    mach_code |= shifts[args[7]] << 5
                else:
                    print('ERROR: Invalid shift expression')
                    sys.exit(1)

                token_count += 1

                if args[7] == "rrx":
                    if len(args) < 9:  # length check
                        print('ERROR: Invalid systax')
                        sys.exit(1)

                    if args[8] != ']':  # post index
                        print('ERROR: Invalid systax')
                        sys.exit(1)

                    token_count += 1

                    if len(args) > 9:
                        if args[9] == '!':
                            mach_code |= 1 << 21
                        elif args[9] == '@':
                            pass
                        else:
                            print('ERROR: Garbage instruction found')
                            sys.exit(1)
                        token_count += 1
                else:
                    if len(args) < 9:  # length check
                        print('ERROR: Invalid shift expression')
                        sys.exit(1)

                    if args[8] != '#':
                        print('ERROR: Invalid shift expression (use immediate)')
                        sys.exit(1)

                    token_count += 1

                    if len(args) < 10:  # length check
                        print('ERROR: Invalid shift expression')
                        sys.exit(1)

                    imm = get_immediate(args[9])

                    if imm < 0 or imm > 32:
                        print('ERROR: Invalid shift amount')
                        sys.exit(1)
                    elif imm == 0:
                        pass
                    elif 0 < imm < 32:
                        mach_code |= imm << 7
                    elif (args[7] == "lsr" or args[7] == "asr") and imm == 32:
                        pass
                    else:
                        print('ERROR: Invalid shift amount')
                        sys.exit(1)

                    token_count += 1

                    if len(args) < 11:  # length check
                        print('ERROR: Invalid systax')
                        sys.exit(1)

                    if args[10] != ']':  # post index
                        print('ERROR: Invalid systax')
                        sys.exit(1)

                    token_count += 1

                    if len(args) > 11:
                        if args[11] == '!':
                            mach_code |= 1 << 21
                        elif args[11] == '@':
                            pass
                        else:
                            print('ERROR: Garbage instruction found')
                            sys.exit(1)
                        token_count += 1
            else:
                print('ERROR: Invalid operand')
                sys.exit(1)

    args = args[token_count:]
    check_comment(args)
    return mach_code
