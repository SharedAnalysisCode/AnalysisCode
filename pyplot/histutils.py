# encoding: utf-8
'''
histutils.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-11-13"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import ROOT

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
#class MyClass():
#    '''
#    description of MyClass
#    '''
#    #____________________________________________________________
#    def __init__(self):
#        pass



# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
def integral_and_error( hist, xmin = None, xmax = None ):
    axis = hist.GetXaxis()
    bin1 = 1
    if xmin: bin1 = axis.FindBin( xmin )
    bin2 = hist.GetNbinsX()
    if xmax: 
        bin2 = axis.FindBin( xmax )
        if axis.GetBinLowEdge(bin2)==xmax: bin2 = bin2-1
    err = ROOT.Double(0.)
    int = hist.IntegralAndError( bin1, bin2, err )
    #log.debug( 'integrating %s over [%.3f,%.3f]'%(hist.GetName(),axis.GetBinLowEdge(bin1),axis.GetBinUpEdge(bin2)) )
    #log.debug( 'result: %.2f +- %.2f'%(int,err) )
    return int, err



#____________________________________________________________
def integral( hist, xmin = None, xmax = None ):
    int, err = integral_and_error( hist, xmin, xmax )
    return int


#____________________________________________________________
def full_integral_and_error( hist ):
    err = ROOT.Double(0.)
    if isinstance(hist,ROOT.TH3):
        return hist.IntegralAndError(0,hist.GetNbinsX()+1, 
                0, hist.GetNbinsY()+1,
                0,hist.GetNbinsZ()+1, 
                err), err
    elif isinstance(hist,ROOT.TH2):
        return hist.IntegralAndError(0,hist.GetNbinsX()+1, 
                0, hist.GetNbinsY()+1,
                err), err
    elif isinstance(hist,ROOT.TH1):
        return hist.IntegralAndError(0,hist.GetNbinsX()+1, 
            err), err
    log.warning( 'Cannot integrate non TH1/2/3 object!')
    return 0.0, 0.0

#____________________________________________________________
def full_integral( hist ):
    int, err = full_integral_and_error( hist )
    return int

#____________________________________________________________
def normalise( hist ):
    if hist and getFullIntegral(hist) != 0.:
        hist.Scale( 1. / getFullIntegral( hist ) )


#____________________________________________________________
def get_xmin( hist_list ):
    xmin = None
    for hist in hist_list:
        temp_xmin = hist.GetXaxis().GetBinLowEdge(1)
        if xmin == None: xmin = temp_xmin
        elif xmin != temp_xmin: 
            log.error( 'mismatching xmin' )
            assert(false)
    return xmin

#____________________________________________________________
def get_xmax( hist_list ):
    xmax = None
    for hist in hist_list:
        temp_xmax = hist.GetXaxis().GetBinUpEdge(hist.GetNbinsX())
        if xmax == None: xmax = temp_xmax
        elif xmax != temp_xmax: 
            log.error( 'mismatching xmax' )
            assert(false)
    return xmax

 
#____________________________________________________________
def get_ymin( hist_list ):
    return min([h.GetMinimum() for h in hist_list])

#____________________________________________________________
def get_ymax( hist_list ):
    return max([h.GetMaximum() for h in hist_list])

#____________________________________________________________
def get_frame_boundaries( hist_list, logy = False ):
    xmin = get_xmin( hist_list )
    ymin = get_ymin( hist_list )
    xmax = get_xmax( hist_list )
    ymax = get_ymax( hist_list )
    log.debug( 'in get frame boundaries' )
    # correct for log
    if logy:
        if ymin <= 0.: ymin = 0.001
        ymax *= 10.
    else: 
        ymax *= 1.4
    
    log.debug( 'xmin: %s, ymin: %s, xmax: %s, ymax: %s' % ( xmin, ymin, xmax, ymax ) )

    return xmin, ymin, xmax, ymax



#____________________________________________________________
def add_hists( hists ):
    log.debug( 'in HistUtils.addHists' )
    log.debug( hists )
    out_hist = None
    for hist in hists:
        if not hist: continue
        if not out_hist: out_hist = hist.Clone()
        else:            out_hist.Add( hist )
    return out_hist



#____________________________________________________________
def make_eff_graph( h_pass, h_total, name ='g_graph' ):
    g = ROOT.TGraphAsymmErrors()
    g.Divide(h_pass,h_total, 'cl=0.683 b(1,1) mode')
    g.SetName(name)
    g.GetXaxis().SetTitle(h_pass.GetXaxis().GetTitle())
    g.GetYaxis().SetTitle('Efficiency')
    return g
  
#____________________________________________________________
def make_fake_factor_graph( h_pass, h_total, name ='g_graph' ):
    #g = ROOT.TGraphAsymmErrors()
    h = h_pass.Clone()
    h_fail = h_total.Clone()
    h_fail.Add(h_pass,-1.)
    h.Divide(h_fail)
    g = ROOT.TGraphErrors(h)
    g.SetName(name)
    g.GetXaxis().SetTitle(h_pass.GetXaxis().GetTitle())
    g.GetYaxis().SetTitle('Fake Factor')
    return g

#____________________________________________________________
def make_fake_factor_hist( h_pass, h_total, name ='h_ff' ):
    #g = ROOT.TGraphAsymmErrors()
    h = h_pass.Clone(name)
    h_fail = h_total.Clone()
    h_fail.Add(h_pass,-1.)
    h.Divide(h_fail)
    h.GetYaxis().SetTitle('Fake Factor')
    return h



## EOF
