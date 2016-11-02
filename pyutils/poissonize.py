import ROOT
from math import sqrt

#______________________________________________________________________________
def GetPoissonizedGraph(histo):
    graph = ROOT.TGraphAsymmErrors()
    j=0
    for i in range(1,histo.GetNbinsX()): 
        if histo.GetBinContent(i)!=0: 
            graph.SetPoint(j,histo.GetBinCenter(i),histo.GetBinContent(i))
            graph.SetPointError(j,
                  histo.GetBinWidth(i)/2.,
                  histo.GetBinWidth(i)/2.,
                  error_poisson_down(histo.GetBinContent(i)),
                  error_poisson_up(histo.GetBinContent(i)))
            j+=1
    return graph


#______________________________________________________________________________
def GetPoissonizedRatioGraph(h_data,h_mc):
    graph = ROOT.TGraphAsymmErrors()
    j=0
    for i in range(1,h_data.GetNbinsX()): 
        nmc   = h_mc.GetBinContent(i)
        ndata = h_data.GetBinContent(i)
        if nmc !=0 and ndata!=0: 
            graph.SetPoint(j,h_data.GetBinCenter(i),ndata/nmc)
            graph.SetPointError(j,
                  h_data.GetBinWidth(i)/2.,
                  h_data.GetBinWidth(i)/2.,
                  error_poisson_down(ndata)/nmc,
                  error_poisson_up(ndata)/nmc
                  )
            j+=1
    return graph


#______________________________________________________________________________
def GetMCRatioBand(h_mc):
    graph = ROOT.TGraphAsymmErrors()
    j=0
    for i in range(1,h_mc.GetNbinsX()): 
        nmc   = h_mc.GetBinContent(i)
        enmc   = h_mc.GetBinError(i)
        enmcfrac = enmc/nmc if nmc else 0.0
        graph.SetPoint(j,h_mc.GetBinCenter(i),1.)
        graph.SetPointError(j,
              h_mc.GetBinWidth(i)/2.,
              h_mc.GetBinWidth(i)/2.,
              enmcfrac, 
              enmcfrac, 
              )
        j+=1
    return graph


#______________________________________________________________________________
def error_poisson_up(data):
    y1 = data + 1.0
    d = 1.0 - 1.0/(9.0*y1) + 1.0/(3*sqrt(y1))
    return y1*d*d*d-data


#______________________________________________________________________________
def error_poisson_down(data):
    y = data
    if y == 0.0: return 0.0
    d = 1.0 - 1.0/(9.0*y) - 1.0/(3.0*sqrt(y))
    return data-y*d*d*d


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


