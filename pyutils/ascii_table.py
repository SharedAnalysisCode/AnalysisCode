#!/usr/bin/env python
__author__ = 'Ryan D. Reece  <ryan.reece@cern.ch>'
__date__ = '2010-04-20'
__copyright__ = 'Copyright 2010 Ryan D. Reece'
__license__ = 'GPL <http://www.gnu.org/licenses/gpl.html>'
__doc__ = """
NAME
    name.py - short description

SYNOPSIS
    Put synposis here.

DESCRIPTION
    Module for taking a table in the form of a list of rows
    which is a list of columns,
    [ [row1 col1, row1 col2, ... ], [row2 col1, row2 col2, ... ] ... ]
    and writing a latex table to a tex file.

OPTIONS
    -h, --help
        Prints this manual and exits.
        
    -n VAL
        Blah blah.

AUTHOR
    %(author)s

COPYRIGHT
    %(copyright)s
    License: %(license)s

SEE ALSO
    ROOT <http://root.cern.ch>

TO DO
    - One.
    - Two.

%(date)s
""" % {'author':__author__, 'date':__date__, 'copyright':__copyright__, 'license':__license__}
#------------------------------------------------------------------------------

#______________________________________________________________________________
def make_str(tab, formats=''):
    n_rows = len(tab)
    n_cols = len(tab[0])

    if not formats:
        formats = ['%s'] * n_cols
    assert len(formats) == n_cols

    ## convert to strings
    new_tab = []
    for i_row in xrange(n_rows):
        row = []
        for i_col in xrange(n_cols):
            if isinstance(tab[i_row][i_col], str):
                row.append( tab[i_row][i_col] )
            else:
                row.append( formats[i_col] % tab[i_row][i_col] )
        new_tab.append( row )

    set_widths(new_tab)

    lines = []
    for row in new_tab:
        lines.append(''.join(row) + '\n')
    return ''.join(lines)


#______________________________________________________________________________
def write(tab, fname, formats=''):

    f = file(fname, 'w')
    f.write(make_str(tab, formats))
    f.close()


#______________________________________________________________________________
def set_widths(tab):
    n_rows = len(tab)
    n_cols = len(tab[0])
    max_widths = []
    for i_col in xrange(n_cols):
        max_widths.append( max([ len(tab[i_row][i_col]) for i_row in xrange(n_rows) ]) )
    for i_row in xrange(n_rows):
        for i_col in xrange(n_cols):
            tab[i_row][i_col] = ('%' + str(max_widths[i_col]+2) + 's') % tab[i_row][i_col]


#______________________________________________________________________________
def read(fname):
    f = file(fname)
    tab = []
    for line in f:
        line = line.split('#')[0].strip() # remove comments
        if line:
            tab.append(line.split())
    return tab

#______________________________________________________________________________
def read_rc_dict(fname):
    d = dict()
    tab = read(fname)
    col_names = tab[0][1:]
    row_names = [ row[0] for row in tab[1:] ]
    for row in tab[1:]:
        r = row[0]
        i_c = 0
        for v in row[1:]:
            c = col_names[i_c]
            d[(r,c)] = v
            i_c += 1
    return d, row_names, col_names

#______________________________________________________________________________
def test_me():
    tab =  [['a', 'b', 'c', 'd'],
            [1.56721, -2e9, 31 , 4440101],
            [5, 6, 7, 8]]
    write(tab, 'test_ascii_table.txt', '%.3g%.2g%.3g%.3g')
    tab2 = read('test_ascii_table.txt')
    print tab2



