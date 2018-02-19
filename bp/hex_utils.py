"""
functions that convert binary stuff. No side effects, ever
"""

# todo figure out best pattern to import this module with logging enabled


import re
import binascii

def string_to_bytes(line, sep = '-x', case_sen_sep = False, case_sen_num = False):
    """
    convert a line of text to binary object
    >>> string_to_bytes('-x45-x72-x6E-x69-x65')

    :param line: text formatted like -x45-x72-x63-x69-x65
    :return:
    """
    assert not case_sen_sep and not case_sen_num, 'case_sen_sep and case_sen_num not implemented yet'
    line = line.strip().upper()
    # if case_sensitive_sep == False:
    sep = sep if case_sen_sep else sep.upper()
    pattern = re.compile(sep + "[\dABCDEF][\dABCDEF]")

    if(len(line) % (2+len(sep)) != 0):
        raise ValueError("line must be like {}1F{}1F .. groups of {} chars".format(sep, sep, len(sep) + 2))

    n = 2 + len(sep)
    strings = [line[i:i+n] for i in range(0, len(line), n)] # line broken up into list, ie ['-X45', '-X72']

    # print(strings)

    to_unhexlify = ''

    for str in strings:
        if (pattern.match(str) == False) or (len(str) != 4):
            raise ValueError("must be formatted like -x1F, case insensitive")
        else:
            to_unhexlify += str[2:]

    # bs = bytes([ord(c) for c in word])
    # print(bs)
    # print(list(bs))
    return binascii.unhexlify(to_unhexlify)

if __name__ == '__main__':
    print('testing {} ....'.format(__file__))
    print(string_to_bytes('-x45-x72-x6E-x69-x65')) #Ernie