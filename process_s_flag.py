def process_s_flag(mach_code, tok):
    if len(tok) > 0 and tok[0] == 's':
        print('\tS flag is set')
        mach_code |= 1 << 20
        tok = tok[1:]
    return (mach_code, tok)
