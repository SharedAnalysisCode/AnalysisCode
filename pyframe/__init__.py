"""
    pyframe - lite Python framework for looping over ROOT trees

author: Ryan Reece  <ryan.reece@cern.ch>

See also:
    - http://www.hep.upenn.edu/~rreece/computing.html
    - https://twiki.cern.ch/twiki/bin/view/Sandbox/PyFrame
    - http://root.cern.ch/
    - http://root.cern.ch/root/HowtoPyROOT.html
"""

#------------------------------------------------------------------------------
# module metadata
#------------------------------------------------------------------------------
__author__ = 'Ryan D. Reece, Alex Tuna'
__email__ = 'ryan.reece@cern.ch, tuna@cern.ch'
__copyright__ = 'Copyright 2011-2013 Ryan Reece and Alex Tuna'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.html'

import ROOT
ROOT.gROOT.SetBatch(True)

## core components of pyframe
import core, algs, config
import test
