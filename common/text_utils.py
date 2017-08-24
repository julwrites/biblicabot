
# Python modules
import string

# Local modules
import debug

def stringify(value):
    if value is None:
        return ''

    return str(value)

def fuzzify(s):
    return s.upper().strip().replace('-', ' ').replace(',', ' ').split()

def overlap(lhs_sub, rhs_sub):
    for lhs in lhs_sub:
        for rhs in rhs_sub:
            if lhs == rhs:
                return True
    return False

def fuzzy_compare(lhs, rhs):
    lhs_parts = fuzzify(lhs)
    rhs_parts = fuzzify(rhs)
    lhs = ''.join(lhs_parts)
    rhs = ''.join(rhs_parts)
    debug.log('Comparing ' + lhs + ' and ' + rhs)

    return ( lhs == rhs or overlap(lhs_parts, rhs_parts) )

def strip_whitespace(s):
    s = s.strip().split()
    return ' '.join(s)

def strip_numbers(s):
    result = ''.join([c for c in s if not c.isdigit()])
    return result if len(result) > 0 else None

def strip_alpha(s):
    result = ''.join([c for c in s if not c.isalpha()])
    return result if len(result) > 0 else None