"""
metaroot.hist

Module for formatting histograms, drawing multiple histograms on the same
canvas, and drawing stacks of histograms.

Part of the metaroot package.
"""

__author__ = 'Ryan D. Reece'
__email__ = 'ryan.reece@cern.ch'
__created__ = '2008-05-01'
__copyright__ = 'Copyright 2008-2010 Ryan D. Reece'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.html'

#------------------------------------------------------------------------------

import math
import re

import ROOT
import metaroot

black = ROOT.kBlack
white = ROOT.kWhite
red = ROOT.kRed-3
#blue = ROOT.kAzure+1
blue = 38
green = ROOT.kGreen-5
orange = ROOT.kOrange-3
gray = ROOT.kGray+1
brown = ROOT.kOrange-7
cyan = ROOT.kCyan+1
violet = ROOT.kViolet-5
magenta = ROOT.kMagenta-6
yellow = ROOT.kOrange-2

my_colors = [
    blue, red, gray, green,
    brown, yellow, violet, orange ]

fill_style_hollow = 1001
fill_style_solid = 1001
fill_style_diag1 = 3354
fill_style_diag2 = 3345
          
my_fill_styles_lines = [3004, 3005, 3006, 3007, 3345, 3354, 3315, 3351, 1001, 1001]
all_black = [black]*14
all_hollow = [0]*14
all_solid = [1001]*14
all_1 = [1]*14
all_2 = [2]*14
all_3 = [3]*14
all_8 = [8]*14
all_05 = [0.5]*14
all_06 = [0.6]*14
all_07 = [0.7]*14
all_08 = [0.8]*14
all_09 = [0.9]*14
all_1_1 = [1.1]*14



#------------------------------------------------------------------------------
# PlotOptions Class
#------------------------------------------------------------------------------
class PlotOptions(object):
    """Class for configuring histogram/graph properties.""" 
#______________________________________________________________________________
    def __init__(self, **kw):
        kw.setdefault('line_color', metaroot.style.black) # switched to dark blue default in ROOT 5.3X?
        kw.setdefault('line_width', metaroot.default)
        kw.setdefault('line_style', metaroot.default)
        kw.setdefault('fill_color', metaroot.default)
        kw.setdefault('fill_style', metaroot.default)
        kw.setdefault('marker_style', metaroot.default)
        kw.setdefault('marker_color', metaroot.default)
        kw.setdefault('marker_size', metaroot.default)
        kw.setdefault('scale', 0) # zero means don't normalize
        kw.setdefault('norm', 0) # zero means don't normalize
        for k,v in kw.iteritems():
            setattr(self, k, v)
#______________________________________________________________________________
    def configure(self, h):
        h.UseCurrentStyle()
        if not self.line_color is metaroot.default:
            h.SetLineColor(self.line_color)
        if not self.line_width is metaroot.default:
            h.SetLineWidth(self.line_width)
        if not self.line_style is metaroot.default:
            h.SetLineStyle(self.line_style)
        if not self.fill_color is metaroot.default:
            h.SetFillColor(self.fill_color)
        if not self.fill_style is metaroot.default:
            h.SetFillStyle(self.fill_style)
        if not self.marker_style is metaroot.default:
            h.SetMarkerStyle(self.marker_style)
        if not self.marker_color is metaroot.default:
            h.SetMarkerColor(self.marker_color)
        if not self.marker_size is metaroot.default:
            h.SetMarkerSize(self.marker_size)
        if isinstance(h, ROOT.TH1) or isinstance(h, ROOT.TH2):
            if self.scale:
                if not h.GetSumw2N(): h.Sumw2()
                h.Scale(self.scale)
            elif self.norm:
                normalize_hist(h, self.norm)


#------------------------------------------------------------------------------
# MetaLegend Class
#------------------------------------------------------------------------------
class MetaLegend(ROOT.TLegend):
    """
    A better TLegend class that increases in height as you call AddEntry.
    """ 
#______________________________________________________________________________
    def __init__(self, width=0.15, height=0.05,
            x1=None, y1=None,
            x2=None, y2=None,
            border=0, fill_color=0, fill_style=0):
#        assert (x1 == y1 == None) or (x2 == y2 == None)
#        assert (x1 != None and y1 != None) or (x2 != None and y2 != None)

        if x1 == x2 == None:
            x2 = 0.93
            x1 = x2 - width
        elif x1 == None:
            x1 = x2 - width
        elif x2 == None:
            x2 = x1 + width

        if y1 == y2 == None:
            y2 = 0.93
            y1 = y2 - width
        elif y1 == None:
            y1 = y2 - width
        elif y2 == None:
            y2 = y1 + width

        ROOT.TLegend.__init__(self, x1, y1, x2, y2)
        self.SetBorderSize(border)
        self.SetFillColor(fill_color)
        self.SetFillStyle(fill_style)
        self.width = width
        self.height = height # per entry
        self._nentries = 0
        self._has_drawn = False
#______________________________________________________________________________
    def AddEntry(self, obj, label='', option='P'):
        self._nentries += 1
        self.resize()
        ROOT.TLegend.AddEntry(self, obj, label, option)
#______________________________________________________________________________
    def Draw(self):
        self.resize()
        ROOT.TLegend.Draw(self)
        self._has_drawn = True
#______________________________________________________________________________
    def resize(self):
        if self._has_drawn:
            y2 = self.GetY2NDC()
            self.SetY1NDC(y2 - (self.height*self._nentries) - 0.01)
        else:
            y2 = self.GetY2()
            self.SetY1(y2 - (self.height*self._nentries) - 0.01)

#------------------------------------------------------------------------------
# CanvasOptions Class
#------------------------------------------------------------------------------
class CanvasOptions(object):
    """Class for configuring canvas properties.""" 
#______________________________________________________________________________
    def __init__(self, **kw):
        kw.setdefault('width', 800)
        kw.setdefault('height', 600)
        kw.setdefault('log_x', 0)
        kw.setdefault('log_y', 0)
        kw.setdefault('grid_x', 0)
        kw.setdefault('grid_y', 0)
        kw.setdefault('tick_x', 1)
        kw.setdefault('tick_y', 1)
        kw.setdefault('left_margin', metaroot.default)
        kw.setdefault('right_margin', metaroot.default)
        kw.setdefault('top_margin', metaroot.default)
        kw.setdefault('bottom_margin', metaroot.default)
        for k,v in kw.iteritems():
            setattr(self, k, v)
#______________________________________________________________________________
    def configure(self, c):
        c.UseCurrentStyle()
        c.SetLogx(self.log_x)
        c.SetLogy(self.log_y)
        if not self.grid_x is metaroot.default:
            c.SetGridx(self.grid_x)
        if not self.grid_y is metaroot.default:
            c.SetGridy(self.grid_y)
        if not self.tick_x is metaroot.default:
            c.SetTickx(self.tick_x)
        if not self.tick_y is metaroot.default:
            c.SetTicky(self.tick_y)
        if not self.left_margin is metaroot.default:
            c.SetLeftMargin(self.left_margin)
        if not self.right_margin is metaroot.default:
            c.SetRightMargin(self.right_margin)
        if not self.top_margin is metaroot.default:
            c.SetTopMargin(self.top_margin)
        if not self.bottom_margin is metaroot.default:
            c.SetBottomMargin(self.bottom_margin)
        c.SetBorderSize(0)
        c.SetBorderMode(0)
        c.Update()
#______________________________________________________________________________
    def create(self, name, title=metaroot.default):
        if title is metaroot.default:
            title = name
        c = ROOT.TCanvas(name, title,
                200, 10,
                self.width, self.height)
        self.configure(c)
        return c


#------------------------------------------------------------------------------
# Free Functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def calc_min(hists, include_errors=False, ignore_zeros=False, ignore_negatives=False):
    extremes = []
    for h in hists:
        points = []
        if isinstance(h, ROOT.TH1) or isinstance(h, ROOT.THStack): 
            if isinstance(h, ROOT.THStack): 
#                h = h.GetHistogram()
                h = h.GetStack().Last()
            for i_bin in xrange(1, h.GetXaxis().GetNbins()+1):
                point = h.GetBinContent(i_bin)
                if include_errors:
                    point -= h.GetBinError(i_bin) # -= : min/max differnce
                points.append(point)
        elif isinstance(h, ROOT.TGraph) or isinstance(h, ROOT.TGraphErrors) or isinstance(h, ROOT.TGraphAsymmErrors): 
            x = ROOT.Double() ;  y = ROOT.Double()
            for i_bin in xrange(1, h.GetN()+1):
                h.GetPoint(i_bin, x, y)
                point = float(y)
                if include_errors:
                    if isinstance(h, ROOT.TGraphErrors):
                        point -= h.GetErrorY(i_bin) # -= : min/max differnce
                    elif isinstance(h, ROOT.TGraphAsymmErrors): 
                        point -= h.GetErrorYlow(i_bin) # -= : min/max differnce
                points.append(point)

        if ignore_zeros:
            points = filter(lambda x: x, points)
        if ignore_negatives:
            points = filter(lambda x: x > 0, points)
        if points:
            extremes.append(min(points)) # min/max differnce

    if extremes:
        return min(extremes) # min/max differnce
    else:
        return 0.

#______________________________________________________________________________
def calc_max(hists, include_errors=False, ignore_zeros=False, ignore_negatives=False):
    extremes = []
    for h in hists:
        points = []
        if isinstance(h, ROOT.TH1) or isinstance(h, ROOT.THStack): 
            if isinstance(h, ROOT.THStack): 
#                h = h.GetHistogram()
                h = h.GetStack().Last()
            for i_bin in xrange(1, h.GetXaxis().GetNbins()+1):
                point = h.GetBinContent(i_bin)
                if include_errors:
                    point += h.GetBinError(i_bin) # -= : min/max differnce
                points.append(point)
        elif isinstance(h, ROOT.TGraph) or isinstance(h, ROOT.TGraphErrors) or isinstance(h, ROOT.TGraphAsymmErrors): 
            x = ROOT.Double() ;  y = ROOT.Double()
            for i_bin in xrange(1, h.GetN()+1):
                h.GetPoint(i_bin, x, y)
                point = float(y)
                if include_errors:
                    if isinstance(h, ROOT.TGraphErrors):
                        point += h.GetErrorY(i_bin) # -= : min/max differnce
                    elif isinstance(h, ROOT.TGraphAsymmErrors): 
                        point += h.GetErrorYhigh(i_bin) # -= : min/max differnce
                points.append(point)

        if ignore_zeros:
            points = filter(lambda x: x, points)
        if ignore_negatives:
            points = filter(lambda x: x > 0, points)
        if points:
            extremes.append(max(points)) # min/max differnce

    if extremes:
        return max(extremes) # min/max differnce
    else:
        return 0.

#______________________________________________________________________________
def set_min(hists, min=metaroot.default, top_buffer=0.1, bottom_buffer=0.1,
        log_y=False, limit=None, include_errors=True,
        include=None):
    """ 
    Sets the minimum of all histograms or graphs in the list hists to be the
    factor times the minimum among hists.  If limit is specified, then the
    miniumum cannot be set below that.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if min is None:
        return None
    if include is None:
        include = []
    if not isinstance(include, list):
        include = [include]
    ## metaroot default ranges
    if min is metaroot.default or min is metaroot.ignore_zeros:
        ## calculated range
        if min is metaroot.default:
            y_min = calc_min(hists, include_errors, ignore_zeros=False, ignore_negatives=log_y)
            y_max = calc_max(hists, include_errors, ignore_zeros=False, ignore_negatives=log_y)
        elif min is metaroot.ignore_zeros:
            y_min = calc_min(hists, include_errors, ignore_zeros=True, ignore_negatives=log_y)
            y_max = calc_max(hists, include_errors, ignore_zeros=True, ignore_negatives=log_y)
        ## check to change range to include values
        for y in include:
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y
        ## calculate setting with buffer
        if log_y and y_min != 0 and y_max != 0:
            setting = math.pow( 10.0, ( (1.0-top_buffer)*math.log(y_min,10.0) + (-1.0*bottom_buffer)*math.log(y_max,10.0) )/( 1.0 - top_buffer - bottom_buffer ) )
#            setting = math.pow( 10, math.log(y_min,10) - (math.log(y_max,10) - math.log(y_min,10)) * bottom_buffer / (1 + top_buffer + bottom_buffer) )
        else:
            setting = ( (1.0-top_buffer)*y_min + (-1.0*bottom_buffer)*y_max )/( 1.0 - top_buffer - bottom_buffer )
#            setting = y_min - (y_max - y_min) * bottom_buffer / (1 + top_buffer + bottom_buffer)
    ## user set range
    else:
        setting = min
    if not limit is None and setting < limit:
        setting = limit
    for h in hists:
        h.SetMinimum(setting)
    return setting

#______________________________________________________________________________
def set_max(hists, max=metaroot.default, top_buffer=0.2, bottom_buffer=0.1,
        log_y=False, limit=None, include_errors=True,
        include=None):
    """
    Sets the maximum of all histograms or graphs in the list hists to be the
    factor times the maximum among hists.  If limit is specified, then the
    maxiumum cannot be set above that.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if max is None:
        return None
    if include is None:
        include = []
    if not isinstance(include, list):
        include = [include]
    ## metaroot default ranges
    if max is metaroot.default or max is metaroot.ignore_zeros:
        ## calculated range
        if max is metaroot.default:
            y_min = calc_min(hists, include_errors, ignore_zeros=False, ignore_negatives=log_y)
            y_max = calc_max(hists, include_errors, ignore_zeros=False, ignore_negatives=log_y)
        elif max is metaroot.ignore_zeros:
            y_min = calc_min(hists, include_errors, ignore_zeros=True, ignore_negatives=log_y)
            y_max = calc_max(hists, include_errors, ignore_zeros=True, ignore_negatives=log_y)
        ## check to change range to include values
        for y in include:
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y
        ## calculate setting with buffer
        if log_y and y_min != 0 and y_max != 0:
            setting = math.pow( 10.0, ( (-1.0*top_buffer)*math.log(y_min,10.0) + (1.0-bottom_buffer)*math.log(y_max,10.0) )/( 1.0 - top_buffer - bottom_buffer ) )
#            setting = math.pow( 10, math.log(y_max,10) + (math.log(y_max,10) - math.log(y_min,10)) * top_buffer / (1 + top_buffer + bottom_buffer) )
        else:
            setting = ( (-1.0*top_buffer)*y_min + (1.0-bottom_buffer)*y_max )/( 1.0 - top_buffer - bottom_buffer )
#            setting = y_max + (y_max - y_min) * top_buffer / (1 + top_buffer + bottom_buffer)

    ## user set range
    else:
        setting = max
    if not limit is None and setting > limit:
        setting = limit
    for h in hists:
        h.SetMaximum(setting)
    return setting

#______________________________________________________________________________
def normalize_hist(h, norm=1.0):
    """
    Scales hist to have integral equal to norm.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if not h.GetSumw2N(): h.Sumw2()
    if isinstance(h, ROOT.TH2):
        integral =  h.Integral(0, h.GetNbinsX()+1, 0, h.GetNbinsY()+1) # includes under/overlfow
    else:
        integral =  h.Integral(0, h.GetNbinsX()+1) # includes under/overlfow
    if integral != 0:
        scale = norm / integral
    else:
        scale = 1.0
        print 'WARNING: normalize_hist: integral=0'
    h.Scale(scale)
#    h.SetYTitle('')


#______________________________________________________________________________
def arrange_stats(hists, statbox_w = 0.15, statbox_h = 0.10):
    """
    For each histogram in the hists list, the stat box is moved so
    that they are stacked in a column starting in the top right
    of the canvas when the histograms are drawn together.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for i, h in enumerate(hists):
        statbox = h.GetListOfFunctions().FindObject("stats")
        if statbox:
            statbox.SetX1NDC(0.99 - statbox_w)
            statbox.SetY1NDC(0.99 - i*(statbox_h + 0.01) - statbox_h)
            statbox.SetX2NDC(0.99)
            statbox.SetY2NDC(0.99 - i*(statbox_h + 0.01))
            # stats colored by fill color
            statbox.SetTextColor(h.GetFillColor())
            statbox.SetBorderSize(1)
            statbox.SetFillStyle(1001) # solid
            statbox.SetFillColor(ROOT.kWhite)
        else:
            print 'WARNING: arrange_stats: statbox not found.'


#______________________________________________________________________________
def make_legend(hists, labels, draw_options=metaroot.default,
        width=0.15, height=0.05, x1=None, y1=None, x2=None, y2=None):
    """
    Creates a legend from a list of hists (or graphs).
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if draw_options is metaroot.default:
        draw_options = ['P']*len(hists)
    if not isinstance(draw_options, list):
        draw_options = [draw_options]*len(hists)
    assert len(hists) == len(labels) == len(draw_options)
    leg = MetaLegend(width=width, height=height, x1=x1, y1=y1, x2=x2, y2=y2)
    for h, lab, opt in zip(hists, labels, draw_options):
        if not opt in ('P', 'F', 'L'):
            ## assume opt is of the same format as draw_options used with Draw
            if opt.count('P'):
                if opt.count('E'):
                    opt = 'PL'
                else:
                    opt = 'P'
            else: # '', 'HIST', etc.
                opt = 'F'
        leg.AddEntry(h, label=lab, option=opt)
    return leg


#______________________________________________________________________________
def pile_hists( hists, name, title=None,
        min=None, max=metaroot.default,
        plot_options=None,
        canvas_options=metaroot.default,
        draw_options='',
        show_stats=False,
        include_y=None,
        **kw):
    """
    Function for formatting a list of histograms and plotting them on the same
    canvas.  Returns a dictionary with the following keys:
    'canvas', 'hists'.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if canvas_options is metaroot.default:
        canvas_options = CanvasOptions()
    c = canvas_options.create(name)
    if not isinstance(draw_options, list):
        draw_options = [draw_options]*len(hists)
    # must configure prior to setting min/max if scaling
    if plot_options:
        for i, h in enumerate(hists):
            plot_options[i].configure(h)
    # set title
    if not title is None:
        for h in hists:
            h.SetTitle(title)
    # set min/max
    set_min(hists, min, log_y=canvas_options.log_y, include=include_y)
    set_max(hists, max, log_y=canvas_options.log_y, include=include_y)
    # draw hists in reverse order such that the first is drawn on top
    num_hists = len(hists)
    has_drawn_first = False
    for j in range(num_hists-1, -1, -1):
        h = hists[j]
        draw_opt = draw_options[j]
        if not has_drawn_first:
            if isinstance(h, ROOT.TGraph) or isinstance(h, ROOT.TGraphErrors) or isinstance(h, ROOT.TGraphAsymmErrors):
                first_hist = None
                for x in hists:
                    if isinstance(x, ROOT.TH1) or isinstance(x, ROOT.TH2):
                        first_hist = x
                        break
                if not first_hist is None:
                    x_min = first_hist.GetXaxis().GetXmin()
                    x_max = first_hist.GetXaxis().GetXmax()
                    y_min = first_hist.GetMinimum()
                    y_min = first_hist.GetMaximum()
                    title = ';%s;%s' % (h.GetXaxis().GetTitle(), h.GetYaxis().GetTitle())
                    frame = ROOT.TH1F('dummy_frame', title, 1, x_min, x_max, 1, y_min, y_max)
                    frame.Draw()
                elif draw_opt.count('A') == 0:
                    draw_opt = 'A' + draw_opt
        elif isinstance(h, ROOT.TH1) or isinstance(h, ROOT.TH2):
            draw_opt += 'same'
            if show_stats:
                draw_opt += 's'
        h.Draw(draw_opt)
        has_drawn_first = True
    # arrange stats
    if show_stats:
        c.Update()
        arrange_stats(hists)
    c.Update()
    return {'canvas':c, 'hists':hists}


#______________________________________________________________________________
def stack_hists( hists, name, title=metaroot.default,
                 min=None, max=metaroot.default,
                 plot_options=None,
                 canvas_options=metaroot.default,
                 draw_options='hist',
                 show_stats=False,
                 include_y=None):
    """
    Function for formatting a list of histograms and plotting them on the same
    canvas, stacked. Returns a dictionary with the following keys:
    'canvas', 'stack', 'hists'.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if canvas_options is metaroot.default:
        canvas_options = CanvasOptions()

    c = canvas_options.create(name)
        
    # must configure prior to setting min/max if scaling
    if plot_options:
        for i, h in enumerate(hists):
            plot_options[i].configure(h)
    # set title
    if title is metaroot.default:
        title = '%s;%s;%s' % (hists[0].GetTitle(), hists[0].GetXaxis().GetTitle(), hists[0].GetYaxis().GetTitle())
    stack = ROOT.THStack(name, title)
    # add hists to stack in reverse order such that first hist is on top
    num_hists = len(hists)
    for j in range(num_hists-1, -1, -1):
        if show_stats:
            stack.Add(hists[j], 'sames')
        else:
            stack.Add(hists[j])
    # set min/max
#    if not min is None: 
#        stack.SetMinimum(min)  
#    if not max is None: 
#        stack.SetMaximum(max) 
    set_min([stack], min, log_y=canvas_options.log_y)
    set_max([stack], max, log_y=canvas_options.log_y)
    # draw
    if draw_options:
        stack.Draw(draw_options)
    else:    
        stack.Draw()
    # arrange stats
    if show_stats:
        c.Update()
        arrange_stats(hists)
    c.Update()
    return {'canvas':c, 'stack':stack, 'hists':hists}


#______________________________________________________________________________
def stack_with_data(data, mc, name,**kw):

    #defaults
    title         = kw.get('title',          metaroot.default)
    ymin          = kw.get('min',            None)
    ymax          = kw.get('max',            metaroot.default)
    plot_options  = kw.get('plot_options',   None)
    canvas_options= kw.get('canvas_options', metaroot.default)
    draw_options  = kw.get('draw_options',   'hist')
    show_stats    = kw.get('show_stats',     False)
    max_factor    = kw.get('max_factor',     None)
    data_plot_options = kw.get('data_plot_options', metaroot.hist.PlotOptions(marker_style=20, marker_size=1.0))

    plot = stack_hists(
        hists         = mc,
        name          = name,
        title         = title,
        min           = None,
        max           = None,
        plot_options  = plot_options,
        canvas_options= canvas_options,
        draw_options  = draw_options,
        show_stats    = show_stats)

    # make the stack sum
    stacksum=data.Clone("tmp") if len(mc)==0 else mc[0].Clone("tmp")
    stacksum.Reset()
    for h in mc:
        stacksum.Add(h)
    
    # make stack plot
    stack = plot['stack']

    # set min/max
    if canvas_options.log_y:
        for b in range(1,data.GetNbinsX()+1):
            if data.GetBinContent(b) > 0.0:
                if ymin==None:
                    ymin=1e10
                ymin=min(ymin,0.1*data.GetBinContent(b))
                
    if len(mc) > 0:
        set_min([data, stack, stacksum], ymin, log_y=canvas_options.log_y)
        set_max([data, stack, stacksum], ymax, log_y=canvas_options.log_y)
    else:
        set_min([data,        stacksum], ymin, log_y=canvas_options.log_y)
        set_max([data,        stacksum], ymax, log_y=canvas_options.log_y)

    # draw data
    data_plot_options.configure(data)
    data.GetXaxis().SetTitle("")
    data.GetYaxis().SetTitle("")
    data.Draw('PE same')
    
    plot['canvas'].Update()    
    plot['data'] = data
    plot['sum'] = stacksum
    return plot


#______________________________________________________________________________
def calc_integral_and_error(h, xmin=None, xmax=None):
    nbins = h.GetNbinsX()
    error = ROOT.Double(0)
    if xmin is None:
        bin1 = 0
    else:
        bin1 = h.FindBin(xmin)
    if xmax is None:
        bin2 = nbins+1
    else:
        bin2 = h.FindBin(xmax)-1
    integral = h.IntegralAndError(bin1, bin2, error)
    error = float(error)
    return integral, error

#______________________________________________________________________________
def calc_max_in_range(hists,x1,x2,incErr=True):
    m=-1e10
    for h in hists:
        xaxis=h.GetXaxis()
        for b in range(xaxis.FindBin(x1),max(xaxis.FindBin(x2),xaxis.FindBin(x1)+1)):
            if incErr:
                m=max(m,h.GetBinContent(b)+h.GetBinError(b))
            else:
                m=max(m,h.GetBinContent(b))
    print "max=",m
    return m

#______________________________________________________________________________
def rebin(h, n_merge=0, n_bins=0, bin_width=0, title_y=''):
    ## check the format of y-axis title for bin width and a unit
    current_title_y = h.GetYaxis().GetTitle()
    reo_pi = re.match('(.*)\s*/\s*\(?\s*#pi\s*/(\d+\.?\d*)\s*\)?', current_title_y)
    reo = None
    if reo_pi:
        title = reo_pi.group(1).strip()
        bin = 1.0/float(reo_pi.group(2))
    else:
        reo = re.match('(.*)\s*/\s*\(?\s*(\d+\.?\d*)\s*(\w*)\s*\)?', current_title_y)
        if reo:
            title = reo.group(1).strip()
            bin = float(reo.group(2))
            unit = reo.group(3)
            
            if round(bin) == int(bin):
                bin = int(bin)
        
    ## do the rebinning
    if n_merge:
        h.Rebin(n_merge)
        bin *= n_merge
    elif n_bins:
        n_bins_orig = h.GetNbinsX()
        if n_bins_orig % n_bins == 0:
            h.Rebin( int(n_bins_orig / n_bins) )
            bin = n_bins
        else:
            print 'WARNING metaroot.hist.rebin: n_bins specified does not divide evenly for %.' % h.GetName()
    elif bin_width:
        range = abs(h.GetXaxis().GetXmax() - h.GetXaxis().GetXmin())
        n_bins_target = range / bin_width
        n_bins_orig = h.GetNbinsX()
        n_bins_merge = n_bins_orig / n_bins_target
        if n_bins_target == int(n_bins_target) and n_bins_merge == int(n_bins_merge): # number of bins should be integer
            h.Rebin( int(n_bins_merge) )
            bin = bin_width
        else:
            print 'WARNING metaroot.hist.rebin: bin_width specified does not divide evenly for %s.' % h.GetName()
            print '    range = %s, bin_width = %s, n_bins_target = %s, n_bins_merge = %s' % (range, bin_width, n_bins_target, n_bins_merge)

    ## correct the bin width in the y-axis title
    if title_y:
            h.GetYaxis().SetTitle(title_y)
    elif reo_pi:
        bin_denom = 1.0/bin
        if round(bin_denom) == int(bin_denom):
            bin_denom = int(bin_denom)
        h.GetYaxis().SetTitle('%s / (#pi/%s)' % (title, bin_denom))
    elif reo:
        if unit:
            h.GetYaxis().SetTitle('%s / (%s %s)' % (title, bin, unit))
        else:
            h.GetYaxis().SetTitle('%s / %s' % (title, bin))
    return h

#______________________________________________________________________________
def variable_rebin(h, bins, title_y=''):
    ## check the format of y-axis title for a unit
    ## copied from rebin -- bin width disregarded
    current_title_y = h.GetYaxis().GetTitle()
    reo_pi = re.match('(.*)\s*/\s*\(?\s*#pi\s*/(\d+\.?\d*)\s*\)?', current_title_y)
    reo = None
    if reo_pi:
        title = reo_pi.group(1).strip()
    else:
        reo = re.match('(.*)\s*/\s*\(?\s*(\d+\.?\d*)\s*(\w*)\s*\)?', current_title_y)
        if reo:
            title = reo.group(1).strip()
            unit = reo.group(3)

    ## do the rebinning
    import array
    var_bins   = array.array('d', bins)
    n_var_bins = len(var_bins)-1
    h_varbins  = h.Rebin(n_var_bins, "%s_varbins" % h.GetName(), var_bins)

    ## correct the bin width in the y-axis title
    if title_y:
        h_varbins.GetYaxis().SetTitle(title_y)
    elif reo_pi:
        h_varbins.GetYaxis().SetTitle('%s / variable bin' % title)
    elif reo:
        if unit:
            h_varbins.GetYaxis().SetTitle('%s / (variable bin %s)' % (title, unit))
        else:
            h_varbins.GetYaxis().SetTitle('%s / variable bin' % title)
    return h_varbins


#______________________________________________________________________________
def reverse_bins(h):
    nbins = h.GetNbinsX()
    x_axis = h.GetXaxis()
    vals = [ h.GetBinContent(i) for i in xrange(0, nbins+2) ]
    errors = [ h.GetBinError(i) for i in xrange(0, nbins+2) ]
    labels = [ x_axis.GetBinLabel(i) for i in xrange(1, nbins+1) ]
    vals.reverse()
    errors.reverse()
    labels.reverse()
    for i in xrange(0, nbins+2):
        h.SetBinContent(i, vals[i])
        h.SetBinError(i, errors[i])
    for i in xrange(1, nbins+1):
        x_axis.SetBinLabel(i, labels[i-1])

