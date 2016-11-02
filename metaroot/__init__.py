"""
    metaroot - Python package for making ROOT plots

author: Ryan D. Reece  <ryan.reece@cern.ch>

This module provides a simplified interface to PyROOT, automating some of the
overhead for making plots, and hiding much of the ugliness of ROOT.  It
provides classes and functions for coloring and styling histograms and graphs,
and stacking and scaling multiple histograms.

This package includes the following modules:
    - HistGetter: for retrieving plots from ROOT files
    - HistFormatter: for coloring and styling plots
    - PlotMaker: for making various kinds of plots
    - TreeMaker: for making and filling TTrees in Python
    - This __init__ file also declares some helper functions below.

See also:
    http://www.hep.upenn.edu/~rreece/computing.html
    http://root.cern.ch/
    http://root.cern.ch/root/HowtoPyROOT.html
"""

#------------------------------------------------------------------------------
# module metadata
#------------------------------------------------------------------------------
__author__ = 'Ryan D. Reece'
__email__ = 'ryan.reece@cern.ch'
__copyright__ = 'Copyright 2008-2010 Ryan D. Reece'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.html'

default = object()
ignore_zeros = object()

import file, hist, plot, style, tree, utils

