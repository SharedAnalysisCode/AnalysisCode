"""
    metaroot/utils.py
"""

import ROOT
import math

#______________________________________________________________________________
def make_text(x, y, text, size=0.05, angle=0, font=42, color=None, NDC=True):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    t = ROOT.TLatex(x, y, text)
    if not size is None:  t.SetTextSize(size)
    if not angle is None: t.SetTextAngle(angle)
    if not font is None:  t.SetTextFont(font)
    if not color is None: t.SetTextColor(color)
    if NDC: t.SetNDC()
    return t


#______________________________________________________________________________
def make_atlas_watermark(x, y, splitline=''):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if splitline: # 'Preliminary' or 'Internal'
        t = make_text(x, y, '#splitline{ATLAS}{%s}' % splitline, size=0.05, font=72)
    else:
        t = make_text(x, y, 'ATLAS', size=0.05, font=72)
    return t

#______________________________________________________________________________
def make_ryan_watermark(x=0.01, y=0.01):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    t = make_text(x, y, 'Ryan Reece (UPenn)', size=0.03, font=52,
            color=ROOT.kGray)
    return t

#______________________________________________________________________________
def make_lumi_text(x=0.55, y=0.82, lumi='XX pb^{-1}', size=0.04):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    t = make_text(x=x, y=y, text='#scale[0.7]{#int}dt L = %s' % lumi, size=size)
    return t

#______________________________________________________________________________
def latex_to_tlatex(s):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    s = s.replace('\\ell', 'l')
    s = s.replace('\\mathrm', '')
    s = s.replace('\\', '#')
    s = s.replace('$', '')
    return s
    
#______________________________________________________________________________
def tlatex_to_latex(s):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    s = s.replace('_{T}', '_\\mathrm{T}')
    s = s.replace('_{vis}', '_\\mathrm{vis}')
    s = s.replace('_{inv}', '_\\mathrm{inv}')
    s = s.replace('_{tracks}', '_\\mathrm{tracks}')
    s = s.replace('#sumcos', '\\sum\\cos')
    s = s.replace(' or ', '~\\mathrm{or}~')
    s = s.replace('charge', '\\mathrm{charge}')
    s = s.replace('GeV', '~\\mathrm{GeV}')
    s = s.replace('MET', 'E_\\mathrm{T}^\\mathrm{miss}')
    s = s.replace('#', '\\')
    s = '$%s$' % s
    return s

#______________________________________________________________________________
def draw_horiz_line(canvas, y, color=ROOT.kBlack, width=1, style=1):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    canvas.cd()
    x1 = canvas.GetUxmin()
    x2 = canvas.GetUxmax()
    line = ROOT.TLine(x1, y, x2, y) 
    line.SetLineColor(color)
    line.SetLineWidth(width)
    line.SetLineStyle(style)
    line.Draw()
    return line

#______________________________________________________________________________
def draw_vert_line(canvas, x, color=ROOT.kBlack, width=1, style=1):
    """
    http://root.cern.ch/phpBB3/viewtopic.php?f=3&t=10745#p46300
    canvas.cd()
    line = ROOT.TLine()
    lm = canvas.GetLeftMargin()
    rm = 1. - canvas.GetRightMargin()
    tm = 1. - canvas.GetTopMargin()
    bm = canvas.GetBottomMargin()
    xndc = (rm-lm)*((x-canvas.GetUxmin())/(canvas.GetUxmax()-canvas.GetUxmin()))+lm
    line.SetLineColor(color)
    line.SetLineWidth(width)
    line.SetLineStyle(style)
    line.DrawLineNDC(xndc,bm,xndc,tm)
    """
    y1 = canvas.GetFrame().GetY1()
    y2 = canvas.GetFrame().GetY2()
    if canvas.GetLogy():
        y1 = math.pow(10, y1)
        y2 = math.pow(10, y2)
    line = ROOT.TLine(x, y1, x, y2) 
    line.SetLineColor(color)
    line.SetLineWidth(width)
    line.SetLineStyle(style)
    line.Draw()
    return line

