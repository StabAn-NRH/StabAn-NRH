import sys
import re
import struct
from process_s_flag import process_s_flag
from process_cond_field import process_cond_field
from process_2_args import process_2_args
from process_3_args import process_3_args
from process_swi import process_swi
from process_mul_3_args import process_mul_3_args

cond = {'eq': 0, 'ne': 1, 'hs': 2, 'cs': 2, 'lo': 3,
        'cc': 3, 'mi': 4, 'pl': 5, 'vs': 6, 'vc': 7,
        'hi': 8, 'ls': 9, 'ge': 10, 'lt': 11, 'gt': 12,
        'le': 13, 'al': 14, 'nv': 15}


symbol_table = {}


def make_regexp(li):
    res = '('
    for elem in li:
        res += elem + '|'
    res.rstrip('|')
    res += ')'
    return res


cond_regexp = make_regexp(cond.keys())


def process_instruction(tokens):
    mach_code = 0
    tok = tokens[0]
    args = tokens[1:]

    mov_re = 'mov' + cond_regexp + '?' + 's' + '?'
    mvn_re = 'mvn' + cond_regexp + '?' + 's' + '?'
    add_re = 'add' + cond_regexp + '?' + 's' + '?'
    sub_re = 'sub' + cond_regexp + '?' + 's' + '?'
    rsb_re = 'rsb' + cond_regexp + '?' + 's' + '?'
    and_re = 'and' + cond_regexp + '?' + 's' + '?'
    orr_re = 'orr' + cond_regexp + '?' + 's' + '?'

    swi_re = 'swi' + cond_regexp + '?'

    mul_re = 'mul' + cond_regexp + '?' + 's' + '?'
    mla_re = 'mla' + cond_regexp + '?' + 's' + '?'
    print('\treg exp for mov: ' + mov_re)
    print('\treg exp for mvn: ' + mvn_re)
    print('\treg exp for add: ' + add_re)
    print('\treg exp for sub: ' + sub_re)
    print('\treg exp for rsb: ' + rsb_re)
    print('\treg exp for and: ' + and_re)
    print('\treg exp for orr: ' + orr_re)

    print('\treg exp for swi: ' + swi_re)

    print('\treg exp for mul: ' + mul_re)
    print('\treg exp for mla: ' + mla_re)
    if re.match(mov_re, tok):
        print('\tMOV FAMILY')
        mach_code = 0b1101 << 21
        mach_code = process_2_args(mach_code, args)
    elif re.match(mvn_re, tok):
        print('\tMVN FAMILY')
        mach_code = 0b1111 << 21
        mach_code = process_2_args(mach_code, args)

    elif re.match(add_re, tok):
        print('\tADD FAMILY')
        mach_code = 0b0100 << 21
        mach_code = process_3_args(mach_code, args)

    elif re.match(sub_re, tok):
        print('\tSUB FAMILY')
        mach_code = 0b0010 << 21
        mach_code = process_3_args(mach_code, args)

    elif re.match(rsb_re, tok):
        print('\tRSB FAMILY')
        mach_code = 0b0011 << 21
        mach_code = process_3_args(mach_code, args)

    elif re.match(and_re, tok):
        print('\tAND FAMILY')
        mach_code = 0
        mach_code = process_3_args(mach_code, args)

    elif re.match(orr_re, tok):
        print('\tORR FAMILY')
        mach_code = 0b1100 << 21
        mach_code = process_3_args(mach_code, args)

    elif re.match(swi_re, tok):
        print('\tSWI FAMILY')
        mach_code = 0
        mach_code = process_swi(mach_code, args)

    elif re.match(mul_re, tok):
        print('\tMUL FAMILY')
        mach_code = 0b1001 << 4
        mach_code = process_mul_3_args(mach_code, args)

    elif re.match(mla_re, tok):
        print('\tMLA FAMILY')
        mach_code = 0b1001 << 4
        mach_code |= 1 << 21
        mach_code = process_mul_3_args(mach_code, args)


    tok = tok[3:]
    (mach_code, tok) = process_cond_field(mach_code, tok)
    if tok != "swi":
        (mach_code, tok) = process_s_flag(mach_code, tok)

    return mach_code


# main() starts here #


lines = sys.stdin.readlines()
splitter = re.compile(r'([ \t\n,])')
addr = 0x8080
current_symbol = ''
for line in lines:
    if line[0] == '@':
        continue
    print()
    print(line.rstrip("\n").strip("\t"))

    tokens = splitter.split(line)
    print(tokens)
    tokens = [tok for tok in tokens
              if re.match('\s*$', tok) == None]
    print(tokens)

    mach_code = 0
    while len(tokens) > 0:
        if tokens[0].endswith(':'):  # process label
            if len(tokens[0].rstrip(':')) == 0:
                print('ERROR: Invalid label name')
                sys.exit(1)
            elif not tokens[0].startswith('_') and not tokens[0][0].isalpha():
                print('ERROR: Invalid label name')
                sys.exit(1)
            else:
                for i in range(1, len(tokens[0].rstrip(':'))):
                    if tokens[0][i] != '_' and not tokens[0][i].isalnum():
                        print('ERROR: Invalid label name')
                        sys.exit(1)
            print('\tLABEL ' + tokens[0].rstrip(':') + ' FOUND')
            current_symbol = tokens[0].rstrip(':')
            symbol_table[current_symbol] = 0
            tokens = tokens[1:]
            #continue
            break
        elif tokens[0].startswith('.'):  # process directive
            print('\tDIRECTIVE ' + tokens[0] + ' FOUND')
            tokens = tokens[1:]
            #continue
            break
        else:  # process instruction
            mach_code = process_instruction(tokens)
            print(hex(mach_code) + ' : Machine Instruction\n')
            print(struct.pack('I', mach_code))
            for key, value in symbol_table.items():
                if key == current_symbol:
                    if value == 0:
                        symbol_table[key] = addr
                    break
            addr += 4
            break

for key, value in symbol_table.items():
    print("{} | {}".format(key, hex(value)))
