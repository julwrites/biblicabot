
# Python modules
import string

# Local modules

def stringify(value):
    if value is None:
        return ''

    return str(value)

def fuzzy_compare(lhs, rhs):
    lhs = lhs.upper().strip().split()
    lhs = ''.join(lhs)

    rhs = rhs.upper().strip().split()
    rhs = ''.join(rhs)

    return lhs == rhs

def strip_whitespace(s):
    s = s.strip().split()
    return ' '.join(s)

def strip_numbers(s):
    return ''.join([c for c in s if not c.isdigit()])

def strip_alpha(s):
    return ''.join([c for c in s if not c.isalpha()])