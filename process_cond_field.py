cond = {'eq': 0, 'ne': 1, 'hs': 2, 'cs': 2, 'lo': 3,
        'cc': 3, 'mi': 4, 'pl': 5, 'vs': 6, 'vc': 7,
        'hi': 8, 'ls': 9, 'ge': 10, 'lt': 11, 'gt': 12,
        'le': 13, 'al': 14, 'nv': 15}


def process_cond_field(mach_code, tok):
    cond_field = tok[:2]
    if cond_field in cond:
        mach_code |= cond[cond_field] << 28
        tok = tok[2:]
        #        print('\tCOND is set to ' + str(cond[cond_field]))
        print('\tCOND is set to ' + str(bin(cond[cond_field])))
    else:  # if cond is undefined
        mach_code |= 14 << 28
        print('\tCOND is undefined')
    return (mach_code, tok)
