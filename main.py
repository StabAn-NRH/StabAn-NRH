import sys
import re
from process_s_flag import process_s_flag
from process_cond_field import process_cond_field
from process_2_args import process_2_args
from process_3_args import process_3_args
from process_swi import process_swi
from process_mul_3_args import process_mul_3_args
from process_data_transfer import process_data_transfer

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


def process_adr(mach_code, args):
    if len(args) < 3:
        print('ERROR: Invalid expression')
        sys.exit(1)

    if args[2] not in symbol_table:
        print('ERROR: Undefined symbol')
        sys.exit(1)

    args = args[:2] + ['pc', ',', '#', str(symbol_table[args[2]] - (addr + 8))]

    return process_3_args(mach_code, args)


def process_branch(mach_code, args):
    if len(args) == 0:  # length check
        print('ERROR: Invalid expression')
        sys.exit(1)
    if args[0] in symbol_table:
        label_value = symbol_table[args[0]]
    else:
        label_value = addr
    # addr + 8 => pc
    # (addr + 8)[pc] - label value -> 2의 보수 -> 부호 유지 >> 2 -> 오프셋 삽입
    offset = (addr + 8) - label_value
    offset = (0xffffff ^ offset) + 1
    offset = offset >> 2
    if offset >> 21 == 1:
        offset |= (0b11 << 22)
    mach_code |= offset
    return mach_code


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

    b_re = "b" + cond_regexp + '?'
    bl_re = "bl" + cond_regexp + '?'

    ldr_re = "ldr" + cond_regexp + '?'
    ldrb_re = "ldrb" + cond_regexp + '?'

    str_re = "str" + cond_regexp + '?'
    strb_re = "strb" + cond_regexp + '?'

    adr_re = 'adr' + cond_regexp + '?' + 's' + '?'

    '''
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

    print('\treg exp for ldr: ' + ldr_re)
    print('\treg exp for ldrb: ' + ldrb_re)

    print('\treg exp for str: ' + str_re)
    print('\treg exp for strb: ' + strb_re)

    print('\treg exp for b:   ' + b_re)
    print('\treg exp for bl:  ' + bl_re)
    
    print('\treg exp for adr: ' + adr_re)
    '''
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

    elif re.match(ldr_re, tok) and tok != "ldrb":
        print('\tLDR FAMILY')
        mach_code = 1 << 26
        mach_code |= 1 << 20
        mach_code = process_data_transfer(mach_code, args)

    elif re.match(ldrb_re, tok):
        print('\tLDRB FAMILY')
        mach_code = 1 << 26
        mach_code |= 1 << 20
        mach_code |= 1 << 22
        mach_code = process_data_transfer(mach_code, args)

    elif re.match(str_re, tok) and tok != "strb":
        print('\tSTR FAMILY')
        mach_code = 1 << 26
        mach_code = process_data_transfer(mach_code, args)

    elif re.match(strb_re, tok):
        print('\tSTRB FAMILY')
        mach_code = 1 << 26
        mach_code |= 1 << 22
        mach_code = process_data_transfer(mach_code, args)

    elif re.match(b_re, tok) and tok != "bl":
        print('\tB FAMILY')
        mach_code = 0b101 << 25
        mach_code = process_branch(mach_code, args)

    elif re.match(bl_re, tok):
        print('\tBL FAMILY')
        mach_code = 0b101 << 25
        mach_code |= 1 << 24
        mach_code = process_branch(mach_code, args)

    elif re.match(bl_re, tok):
        print('\tBL FAMILY')
        mach_code = 0b101 << 25
        mach_code |= 1 << 24
        mach_code = process_branch(mach_code, args)

    elif re.match(adr_re, tok):
        print('\tADR FAMILY')
        mach_code = 0b0100 << 21
        mach_code = process_adr(mach_code, args)
    else:
        print('ERROR: Invalid operation')
        sys.exit(1)

    instruct = tok
    if tok[0] == 'b':
        if len(tok) < 4:
            tok = tok[1:]
        else:
            tok = tok[2:]
    else:
        tok = tok[3:]
    (mach_code, tok) = process_cond_field(mach_code, tok)
    if instruct != "swi" and instruct[0] != "b":
        (mach_code, tok) = process_s_flag(mach_code, tok)

    return mach_code


# main() starts here #


lines = sys.stdin.readlines()
splitter = re.compile(r'([ \t\n,#!\[\]@])')
instruction_list = []
addr = 0x8080
current_symbol = ''

# 1 pass
for line in lines:
    if line[0] == '@':
        continue

    tokens = splitter.split(line)
    tokens = [tok for tok in tokens
              if re.match('\s*$', tok) == None]
    instruction_list.append(tokens)
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
            current_symbol = tokens[0].rstrip(':')
            for key, value in symbol_table.items():
                if key == current_symbol:
                    print('ERROR: [{}] label already defined'.format(current_symbol))
                    sys.exit(1)
            symbol_table[current_symbol] = 0
            break
        elif tokens[0].startswith('.'):  # process directive
            break
        else:  # process instruction
            for key, value in symbol_table.items():
                if key == current_symbol:
                    if value == 0:
                        symbol_table[key] = addr
                    break
            addr += 4
            break

addr = 0x8080

# 2 pass
for instruction in instruction_list:

    print(str(instruction).rstrip("\n").strip("\t"))
    '''
    tokens = splitter.split(instruction)
    tokens = [tok for tok in tokens
              if re.match('\s*$', tok) is None]
    '''
    mach_code = 0
    if len(instruction) > 0:
        if instruction[0].endswith(':'):  # process label
            print('\tLABEL ' + instruction[0].rstrip(':') + ' FOUND')
            current_symbol = instruction[0].rstrip(':')
            instruction = instruction[1:]
            print()
        elif instruction[0].startswith('.'):  # process directive
            print('\tDIRECTIVE ' + instruction[0] + ' FOUND')
            tokens = instruction[1:]
            print()
        else:  # process instruction
            mach_code = process_instruction(instruction)
            print(hex(mach_code) + ' : Machine Instruction\n')
            addr += 4
print()
print("symbol table: ")
for key, value in symbol_table.items():
    print("{} | {}".format(key, hex(value)))
