"""
metaroot.plot

Module for making various special kinds of ROOT plots.
This module should be creating/modifying plots, not formatting.
metaroot.hist should be used to format and style existing
plots.

Part of the metaroot package.
"""

__author__ = 'Ryan D. Reece'
__email__ = 'ryan.reece@cern.ch'
__created__ = '2008-05-01'
__copyright__ = 'Copyright 2008-2010 Ryan D. Reece'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.html'

#------------------------------------------------------------------------------

import os, time, math
import ROOT
import ascii_table


#------------------------------------------------------------------------------

_latex_header = r"""\documentclass[10pt]{article}
\usepackage[a4paper, includeheadfoot, head=5mm, headsep=2mm, foot=4mm, top=2mm, bottom=2mm, left=2mm, right=4mm]{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}

\renewcommand{\familydefault}{\ttdefault}

\usepackage{fancyhdr}
\pagestyle{fancyplain}
\lhead[%(file_name)s]{%(file_name)s}
\chead[%(user)s]{%(user)s}
\rhead[%(time)s]{%(time)s}
\lfoot[]{}
\cfoot[\thepage]{\thepage}
\rfoot[]{}

\begin{document}

%(notes)s


"""

_latex_footer = r"""
%-------------------------------------------------------------------------------
\end{document}
%-------------------------------------------------------------------------------
"""

_fig_stats = r"""
%%-------------------------------------------------------------------------------
\noindent
\begin{minipage}{\textwidth}
    %(caption)s\\*
    \begin{minipage}[c]{0.45\textwidth}
        \includegraphics[width=\textwidth]{%(name)s}
    \end{minipage}
    \begin{minipage}[c]{0.54\textwidth}
        \scriptsize{
        \begin{tabular}[c]{lrrrrrrrr}
%(tab)s
        \end{tabular}
        }
    \end{minipage}
\end{minipage}
%%-------------------------------------------------------------------------------
"""



#------------------------------------------------------------------------------
# LatexWriter Class
#------------------------------------------------------------------------------
class LatexWriter(object):
    """Please write a docstring."""
#______________________________________________________________________________
    def __init__(self, file_name, notes=''):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.file_name = file_name
        self.out_file = open(file_name, 'w')
        self.write_header(notes)
#______________________________________________________________________________
    def write(self, s):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.out_file.write(s)
#______________________________________________________________________________
    def log(self, s):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print s
        s = "\\verb$%s$\\\\*\n" % s
        self.out_file.write(s)
#______________________________________________________________________________
    def write_header(self, notes=''):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.out_file.write(_latex_header % {
                'file_name' : self.file_name.replace('_', r'\_'),
                'user' : os.environ['USER'],
                'time' : time.ctime(),
                'notes' : notes.replace('_', r'\_') } )
#______________________________________________________________________________
    def write_footer(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.out_file.write(_latex_footer)
#______________________________________________________________________________
    def close(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.write_footer()
        self.out_file.close()
#______________________________________________________________________________
    def write_stack(self, name, hists, labels):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        tab = [['', '&', r'\tiny{entries}', '&', r'\tiny{int}', '&', r'\tiny{err}', '&', r'\tiny{mean}', '&', r'\tiny{\sc rms}', '&', r'\tiny{under}', '&', r'\tiny{over}', r'\\ \hline']]
        for h, label in zip(hists, labels):
            nbins = h.GetNbinsX()
            nentries = h.GetEntries()
            integral = h.Integral(0, nbins+1)
            err = math.sqrt(float(nentries))*integral/nentries if nentries else 0
            row = [label, '&']
            row += [ '%i' % nentries, '&']
            row += [ '%.3g' % integral, '&']
            row += [ '%.3g' % err, '&']
            row += [ '%.3g' % h.GetMean(), '&']
            row += [ '%.3g' % h.GetRMS(), '&']
            row += [ '%.3g' % h.GetBinContent(0) , '&']
            row += [ '%.3g' % h.GetBinContent(nbins+1) , r'\\' ]
            tab.append(row)
        tab_str = ascii_table.make_str(tab)
        caption = r'{\tt %s}' % name.replace('_', r'\_')
        self.out_file.write(_fig_stats % {
            'name' : name,
            'tab' : tab_str,
            'caption' : caption } )

