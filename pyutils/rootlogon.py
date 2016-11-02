## file:    rootlogon.py
## author:  Ryan Reece <ryan.reece@cern.ch>
## created: July 2009
#-----------------------------------------------------------------------------

__author__ = 'Ryan D. Reece  <ryan.reece@cern.ch>'

from ROOT import gStyle, TColor, kGray
from array import array

print 'Using %s' % (__file__)


#-----------------------------------------------------------------------------
# whitening
#-----------------------------------------------------------------------------
gStyle.SetFrameBorderMode(0)
gStyle.SetFrameFillColor(0)
gStyle.SetFrameLineColor(0)
gStyle.SetFrameLineWidth(0)
gStyle.SetCanvasBorderMode(0)
gStyle.SetCanvasColor(0)
gStyle.SetPadBorderMode(0)
gStyle.SetPadColor(0)
gStyle.SetStatColor(0)
gStyle.SetDrawBorder(0)


#-----------------------------------------------------------------------------
# pad margins
#-----------------------------------------------------------------------------
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadRightMargin(0.05)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetTitleOffset(1.2, 'x')
gStyle.SetTitleOffset(1.2, 'y')


#-----------------------------------------------------------------------------
# fonts
#-----------------------------------------------------------------------------
font = 42 # 22 = Times, 42 = Helvetica
gStyle.SetTextFont(font)
gStyle.SetLabelFont(font, 'xyz')
gStyle.SetTitleFont(font, 'xyz')
gStyle.SetTitleFont(font, 't')
gStyle.SetStatFont(font)


#-----------------------------------------------------------------------------
# text sizes
#-----------------------------------------------------------------------------
gStyle.SetTextSize(0.06)
gStyle.SetLabelSize(0.06, 'xyz')
gStyle.SetTitleSize(0.06, 'xyz')
gStyle.SetTitleSize(0.06, 't')
gStyle.SetStatFontSize(0.04)

#gStyle.SetTextSizePixels(30)
#gStyle.SetLabelSize(30, 'xyz')
#gStyle.SetTitleSize(30, 'xyz')
#gStyle.SetTitleSize(30, 't')
#gStyle.SetStatFontSize(15)


#-----------------------------------------------------------------------------
# stat box
#-----------------------------------------------------------------------------
gStyle.SetOptStat(0)
#gStyle.SetOptStat(1110)
gStyle.SetStatH(0.2)
gStyle.SetStatW(0.2)
gStyle.SetStatX(0.99)


#-----------------------------------------------------------------------------
# title
#-----------------------------------------------------------------------------
gStyle.SetOptTitle(0)
gStyle.SetTitleColor(1)
gStyle.SetTitleFillColor(0)
gStyle.SetTitleStyle(0)
gStyle.SetTitleBorderSize(0)
gStyle.SetTitleY(0.99)
gStyle.SetTitleX(.1)


#-----------------------------------------------------------------------------
# error bars
#-----------------------------------------------------------------------------
#gStyle.SetErrorX(0.001) # get rid of x error bars
gStyle.SetEndErrorSize(0.) # get rid of error bar caps


#-----------------------------------------------------------------------------
# pad ticks
#-----------------------------------------------------------------------------
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
#gStyle.SetTickLength(0.03, 'x')
#gStyle.SetTickLength(0.03, 'y')
#gStyle.SetTickLength(0.03, 'z')
#gStyle.SetLineWidth(3) # set tick width

gStyle.SetMarkerStyle(20)
gStyle.SetMarkerSize(1.2)

#-----------------------------------------------------------------------------
# hist lines
#-----------------------------------------------------------------------------
gStyle.SetHistLineWidth(2)
gStyle.SetGridWidth(1)
gStyle.SetGridColor(kGray+1)


#-----------------------------------------------------------------------------
# color palette
#-----------------------------------------------------------------------------
#gStyle.SetPalette(1)
    
def set_palette(name='default', ncontours=200):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == 'gray' or name == 'grayscale':
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    # elif name == "whatever":
        # (define more palettes)
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    npoints = len(s)
    TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    gStyle.SetNumberContours(ncontours)
    
set_palette()


#-----------------------------------------------------------------------------
# force style
#-----------------------------------------------------------------------------
#from ROOT import gROOT
#gROOT.ForceStyle()


#-----------------------------------------------------------------------------
# open argument ROOT files
#-----------------------------------------------------------------------------
import sys
from ROOT import TFile
f = []
for i in sys.argv[1:]:
    if i.endswith('.root'):
        f.append(TFile(i, 'READ'))

## EOF
