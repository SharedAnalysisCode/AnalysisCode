## file:    latex_table.py
## author:  Ryan D. Reece <ryan.reece@cern.ch>
## created: July 2009
"""
Module for taking a table in the form of a list of rows
which is a list of columns,
[ [row1 col1, row1 col2, ... ], [row2 col1, row2 col2, ... ] ... ]
and writing a latex table to a tex file.
"""

__author__ = 'Ryan D. Reece  <ryan.reece@cern.ch>'

_default = object()

def write(table_list, tex_file='table.tex', col_format=_default, col_width=10, first_col_width=_default):
    if first_col_width is _default:
        first_col_width = col_width
    num_cols = len(table_list[0])
    format = '        %-' + str(first_col_width) + 's' + (num_cols-1)*(' & %' + str(col_width) + 's') + ' \\\\\n'
    if col_format is _default:
        col_format = ' l ' + 'r '*(num_cols-1)
    out_lines = []
    out_lines += [  '\\documentclass[10pt]{article}\n',
                    '\\pagestyle{empty}\n',
                    '\\usepackage[landscape, top=2mm, bottom=2mm, left=2mm, right=2mm]{geometry}\n',
                    '\\begin{document}\n',
                    '\n',
                    '\\begin{table}[htbp]\n',
                    '    \\centering\n',
                    '    \\begin{tabular}{%s}\n' % col_format,
                    '        \\hline\\hline\n' ] 
    for ri, r in enumerate(table_list):
        assert len(r) == num_cols
        if ri == 1:
            out_lines += [ '        \\hline\n' ] 
        for ci, c in enumerate(r):
            if not isinstance(c, str):
                r[ci] = str(c)
        out_lines += [format % tuple(r)]
    out_lines += [  '        \\hline\\hline\n',
                    '    \\end{tabular}\n',
                    '%    \\caption{Put a caption here.}\n',
                    '%    \\label{tab:put_label_here}\n',
                    '\\end{table}\n',
                    '\n',
                    '\\end{document}\n' ]
    f = file(tex_file, 'w')
    f.writelines(out_lines)
    f.close
    print '%s written' % tex_file


def read(tex_file, table_num=1):
    table_count = 0
    is_in_tabular = False
    tab = []
    row = []
    f = file(tex_file, 'r')
    for line in f:
        if line.count('\\begin{tabular}'):
            table_count += 1
            is_in_tabular = True
        elif line.count('\\end{tabular}'):
            is_in_tabular = False
        elif is_in_tabular and table_count==table_num:
            if line.count('hline'):
                continue
            entries = line.split('&')
            len_entries = len(entries)
            for ei, e in enumerate(entries):
                print ei, e
                if ei == len_entries-1:
                    assert(e.count('\\\\'))
                    row.append(e.split('\\\\')[0].strip())
                    tab.append(row)
                    row = []
                else:
                    row.append(e.strip())
    f.close()
    return tab


def test_me():
    tab =  [['a', 'b', 'c', 'd'],
            [1,2,3,4],
            [5,6,7,8]]
    write(tab, 'test_latex_table.tex')
    tab2 = read('test_latex_table.tex')
    print tab2

