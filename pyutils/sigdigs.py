## $Id $
## file:    sigdigs.py
## author:  Ryan D. Reece <ryan.reece@cern.ch>
## created: July 2009
"""
Python module for rounding floats to significant digits
and making strings thereof.
"""

__author__ = 'Ryan D. Reece  <ryan.reece@cern.ch>'

import math, re, __builtin__
rex = re.compile(r'(([+-]?\d+)\.?(\d*))(?:[eE]?([+-]?\d+))?')


def calc_sci_exp(x):
   if x == 0:
       return 0
   else:
       return int(math.floor( math.log(abs(x), 10) ))


def round(x, digits):
    assert isinstance(digits, int)
    assert digits > 0
    e = calc_sci_exp(x)
    return __builtin__.round(x/float(pow(10,e+1)), digits)*pow(10,e+1)


def latex_sci(s):
    if s.count('e'):
        L = s.split('e')
        assert len(L) == 2
        neg_exp = L[1].count('-')
        L[1] = L[1].lstrip('+-0')
        if neg_exp:
            L[1] = '-' + L[1]
        s = '$%s \\times 10^{%s}$' % tuple(L)
    else:
        s = '$%s$' % s
    return s


def round_to_str(x, digits, latex=False, eng_exp=False, keep_whole=False):
    e = calc_sci_exp(x)
    s = ''
    if e + 1 >= digits and keep_whole: # all sig digs are whole numbers
        s = str(int(__builtin__.round(x)))
    else:
        s = '%.*e' % (digits-1, x) # does rounding
        if eng_exp and abs(e) >= 3:
            # shift digits for exponent to be multiple of 3
            rmd_e = e % 3
            if rmd_e:
                div_e = e // 3
                new_e = '%0+3i' % (3*div_e)
                reo = rex.match(s)
                assert reo
                left = reo.group(2)
                right = reo.group(3)
                len_right = len(right)
                if len_right > rmd_e:
                    left += right[:rmd_e]
                    right = right[rmd_e:]
                else:
                    left += right + '0'*(rmd_e-len_right)
                    right = ''
                if right:
                    s = '%s.%se%s' % (left, right, new_e)
                else:
                    s = '%se%s' % (left, new_e)
        else:
            s = '%g' % float(s)
        # append significant zeros
        dig_count = 0
        has_started = False
        for c in s:
            if not has_started and c.isdigit() and c != '0':
                has_started = True
            if has_started:
                if c == 'e': break
                if c.isdigit(): dig_count += 1
        if dig_count < digits:
            s_list = s.split('e')
            assert 1 <= len(s_list) <= 2
            if s_list[0].count('.'):
                s_list[0] += '0'*(digits-dig_count)
            else:
                s_list[0] += '.'+'0'*(digits-dig_count)
            if len(s_list) == 2:
                s_list[1] = 'e' + s_list[1]
            s = ''.join(s_list)
    if latex:
        s = latex_sci(s)
    return s


def round_to_error(x, error, latex=False, eng_exp=False, keep_whole=True):
    if not x:
        return '0'
    round_error = round(error, 1)
    error_exp = calc_sci_exp(round_error)
    round_x = __builtin__.round(x * math.pow(10, -1*error_exp)) * math.pow(10, error_exp)
    x_exp = calc_sci_exp(round_x)
    error_digit = '%i' % __builtin__.round(round_error * math.pow(10, -1*error_exp))
    digits = x_exp - error_exp + 1
    if not (x > 1 and keep_whole):
        x = round_x
    if digits == 0:
        digits = 1
        error_digit = error_digit + '0'
    assert digits >= 1
    s = round_to_str(x, digits, latex=False, eng_exp=eng_exp, keep_whole=keep_whole)
    reo = rex.match(s)
    assert reo
    if reo.group(4): # has exponent
        s = '%s(%s)e%s' % (reo.group(1), error_digit, reo.group(4))
        if latex:
            s = latex_sci(s)
    else:
        if error_exp >= 0:
            s = '%s(%i)' % (s, __builtin__.round(error))
        else:
            s = '%s(%s)' % (s, error_digit)
    return s


def test_me():
    test_cases = [ 'round_to_str(0.49717514124293788, 3, keep_whole=True, latex=True)',
                   'round_to_str(12345, 2)',
                   'round_to_str(12545, 2)',
                   'round_to_str(1254, 2, keep_whole=False)',
                   'round_to_str(12545, 8)',
                   'round_to_str(12545, 8, eng_exp=True)',
                   'round_to_str(12545.94523, 2, keep_whole=True)',
                   'round_to_str(12545, 2, keep_whole=True)',
                   'round_to_str(0.0000012545, 3, keep_whole=True)',
                   'round_to_str(0.0000012545, 3)',
                   'round_to_str(0.000012545, 3)',
                   'round_to_str(125450000000, 2)',
                   'round_to_str(125450000000, 2, eng_exp=True)',
                   'round_to_str(0.12345, 2)',
                   'round_to_str(0.0000012345, 2)',
                   'round_to_str(0.00000012345, 3)',
                   'round_to_str(0.00000012345, 4)',
                   'round_to_str(0.00000012345, 4, eng_exp=False)',
                   'round_to_str(125450000000, 2, latex=True)',
                   'round_to_str(0.000000012345, 3, latex=True)',
                   'round_to_str(0.000000012345, 3, latex=True, eng_exp=True)',
                   'round_to_str(1.9e99, 1)',
                   'round_to_str(1.9e99, 3)',
                   'round_to_str(1.9e98, 3)',
                   'round_to_str(0.0009, 2)',
                   'round_to_error(2000176.2378, 60000, latex=True)',
                   'round_to_error(2000176.2378, 60000)',
                   'round_to_error(5.345678e-8, 2e-10)',
                   'round_to_error(5.345678e-8, 2e-10, latex=True)',
                   'round_to_error(5.345678e-8, 2e-10, latex=True, eng_exp=True)',
                   'round_to_error(1.2378, 0.05)',
                   'round_to_error(176.2378, 50)',
                   'round_to_error(0.0378, 0.005)',
                   'round_to_error(0.01038088, 0.007340)',
                   'round_to_error(0.087, 0.10)',
                   'round_to_error(0.97, 0.10)',
                 ]
    results = map(eval, test_cases)
    for t, r in zip(test_cases, results):
        print t.ljust(55), r


if __name__ == '__main__':
   test_me()
