# encoding: utf-8
'''
tools.py

description:

'''

from array import array
import sys
## modules
import ROOT
from pyplot import histutils
from math import sqrt
from decimal import Decimal
from copy import deepcopy

#import sys_conv


# atlas style
# remove this import if you don't have it
hackyPath = sys.modules[__name__].__file__[0:(-9 if sys.modules[__name__].__file__[-1]=="c" else -8)] + "atlasstyle-00-03-05/"
print hackyPath
ROOT.gROOT.LoadMacro(str(hackyPath + "AtlasStyle.C"))
ROOT.gROOT.LoadMacro(str(hackyPath + "AtlasUtils.C"))
ROOT.gROOT.LoadMacro(str(hackyPath + "AtlasLabels.C"))
ROOT.SetAtlasStyle()

# - - - - - - - - - - - class defs  - - - - - - - - - - - - #




# - - - - - - - - - - function defs - - - - - - - - - - - - #
def fixFakes(histo,FF):
  if not histo:
    print "YYYYYYYYYYYYY no histo"
    return
  for i in range(1,histo.GetNbinsX()+1):
    if histo.GetBinContent(i) == 0:
      histo.SetBinContent(i,1e-3)
      histo.SetBinError(i,1.14*2/3*FF-1.14/3*FF**2)

#____________________________________________________________
def apply_blind(h,blind_min):
    for i in range(1,h.GetNbinsX()+1):
        if h.GetBinLowEdge(i)>=blind_min: 
            h.SetBinContent(i,0.)
            h.SetBinError(i,0.)

#____________________________________________________________
def get_hists(
        region    = None,
        icut      = None,
        histname  = None,
        samples   = None,
        rebin     = None,
        rebinVar  = [],
        sys_dict  = None,
        ):
    '''
    if sys_dict is passed, hists for all systematics will be appended in a dict. 
    '''
    
    hists = {} 
    for s in samples:
      if not s.hist(region=region,icut=icut,histname=histname): continue
      h = s.hist(region=region,icut=icut,histname=histname).Clone()
      if rebin and len(rebinVar)==0 and h: h.Rebin(rebin)
      elif len(rebinVar)>1 and h:
        # print "Performing variable bin rebining with on " + histname
        # print "============ ",s.name
        # if s.name == "data":
        #   for i in range(h.GetNbinsX()+1):
        #     if h.GetBinContent(i)>0:
        #       print h.GetBinContent(i)," ",h.GetBinCenter(i)
        runArray = array('d',rebinVar)
        h = h.Rebin( len(rebinVar)-1, histname+"Var", runArray )
        print "OVERFLOW CHECK FOR ", s.name," ", h.GetBinContent(h.GetNbinsX()+1)
        h.SetBinContent(h.GetNbinsX(), h.GetBinContent(h.GetNbinsX()+1) + h.GetBinContent(h.GetNbinsX()) )
        h.SetBinError(h.GetNbinsX(), sqrt(h.GetBinError(h.GetNbinsX()+1)**2 + h.GetBinError(h.GetNbinsX())**2) )
      hists[s] = h
      assert h, 'failed to gen hist for %s'%s.name
      h.SetName('h_%s_%s'%(region,s.name))
      
      if sys_dict: 
         h.sys_hists = get_sys_hists(region    = region,
                                     icut      = icut,
                                     histname  = histname,
                                     sample    = s,
                                     rebin     = rebin,
                                     rebinVar  = rebinVar,
                                     sys_dict  = sys_dict,
                                     )

    for s in samples: s.estimator.flush_hists()
    return hists

#____________________________________________________________
def get_sys_hists(
        region   = None,
        icut     = None,
        histname = None,
        sample   = None,
        rebin    = None,
        rebinVar = [],
        sys_dict = None,
        ):
    
    '''
    TODO: put description here
    '''

    hist_dict = {}
    for name,sys in sys_dict.items():
        h_up = h_dn = None
        if sample.estimator.is_affected_by_systematic(sys):
          print name," ",sys," ",sys.envelope

          if sys.envelope == True:
            print "envelope mode"
            nominal = deepcopy(sample.hist(region=region,icut=icut,histname=histname).Clone())
            print nominal.Integral()
            constituents = []
            for sysConst in sys.constituents:
              print "GETTING HIST"
              tempHisto = deepcopy(sample.hist(region=region,icut=icut,histname=histname,sys=sysConst,mode='up',envelope=True).Clone())
              print sample.name," ",tempHisto," ",tempHisto.Integral()
              constituents += [tempHisto]
            ## rebin in the function
            h_up,h_dn = make_sys_hists(nominal,constituents,rebin,rebinVar, sqrt(99) if name == "PDF_SYS_ENVELOPE" else 1. )

          else:
            if not h_up:
              print "GET UP HIST"
              h_up = sample.hist(region=region,icut=icut,histname=histname,sys=sys,mode='up').Clone() 
            else:
              assert 1==0, "not sure what this part of the code is about"
              h_up.Add(sample.hist(region=region,icut=icut,histname=histname,sys=sys,mode='up').Clone())
            if not h_dn:
              print "GET DN HIST"
              h_dn = sample.hist(region=region,icut=icut,histname=histname,sys=sys,mode='dn').Clone() 
            else:
              assert 1==0, "not sure what this part of the code is about"
              h_dn.Add(sample.hist(region=region,icut=icut,histname=histname,sys=sys,mode='dn').Clone())

            ## rebin histogram
            if rebin and len(rebinVar)==0 :
              if h_up: h_up.Rebin(rebin)
              if h_dn: h_dn.Rebin(rebin)
            elif len(rebinVar)>1 :
              runArray = array('d',rebinVar)
              print "Performing variable bin rebining with on " + histname + " SYS: " + str(sys) + " " + name
              if h_up: h_up = h_up.Rebin( len(rebinVar)-1, histname+"Var", runArray )
              if h_dn: h_dn = h_dn.Rebin( len(rebinVar)-1, histname+"Var", runArray )
              h_up.SetBinContent(h_up.GetNbinsX(), h_up.GetBinContent(h_up.GetNbinsX()+1) + h_up.GetBinContent(h_up.GetNbinsX()) )
              h_up.SetBinError(h_up.GetNbinsX(), sqrt(h_up.GetBinError(h_up.GetNbinsX()+1)**2 + h_up.GetBinError(h_up.GetNbinsX())**2) )
              h_dn.SetBinContent(h_dn.GetNbinsX(), h_dn.GetBinContent(h_dn.GetNbinsX()+1) + h_dn.GetBinContent(h_dn.GetNbinsX()) )
              h_dn.SetBinError(h_dn.GetNbinsX(), sqrt(h_dn.GetBinError(h_dn.GetNbinsX()+1)**2 + h_dn.GetBinError(h_dn.GetNbinsX())**2) )

            ## symmetrizing the sys
            if sys.symmetrize == True:
              ## get nominal histo
              nominal = deepcopy(sample.hist(region=region,icut=icut,histname=histname).Clone())
              ## rebin nominal histogram
              if rebin and len(rebinVar)==0 :
                nominal.Rebin(rebin)
              elif len(rebinVar)>1 :
                runArray = array('d',rebinVar)
                nominal = nominal.Rebin( len(rebinVar)-1, histname+"Var", runArray )
                nominal.SetBinContent(nominal.GetNbinsX(), nominal.GetBinContent(nominal.GetNbinsX()+1) + nominal.GetBinContent(nominal.GetNbinsX()) )
                nominal.SetBinError(nominal.GetNbinsX(), sqrt(nominal.GetBinError(nominal.GetNbinsX()+1)**2 + nominal.GetBinError(nominal.GetNbinsX())**2) )
              print nominal
              ## the loop
              for i in range(0,h_up.GetNbinsX()+2):
                up = abs(nominal.GetBinContent(i) - h_up.GetBinContent(i))
                dn = abs(nominal.GetBinContent(i) - h_dn.GetBinContent(i))
                h_up.SetBinContent(i, nominal.GetBinContent(i) + max(up,dn) )
                h_dn.SetBinContent(i, nominal.GetBinContent(i) - max(up,dn) )


          h_up.SetName('h_%s_%s_up_%s'%(region,sys.name,sample.name))
          h_dn.SetName('h_%s_%s_dn_%s'%(region,sys.name,sample.name))

        hist_dict[sys] = (h_up,h_dn)
    return hist_dict 


#____________________________________________________________
def make_stat_hist(h):
    '''
    makes histogram with fractional bin uncertainty as entries
    ie. new bin content = old bin error/old bin content
    (used for making stat. ratio bands)
    '''
    h_stat = h.Clone('%s_stat'%(h.GetName()))
    for i in range(1,h.GetNbinsX()+1): 
        n = h.GetBinContent(i)
        en = h.GetBinError(i)
        stat = en / n if n else 0.0
        h_stat.SetBinContent(i,stat) 
    return h_stat

#____________________________________________________________
def make_band_graph_from_hist(h_UP,h_DN=None):
    '''
    makes band graph from hist.
    anti-symmetric if h_DN supplied, otherwise symmetric
    '''
    graph = ROOT.TGraphAsymmErrors()
    # added following line
    #graph.GetXaxis().SetRangeUser(h_UP.GetXaxis().GetXmin(),h_UP.GetXaxis().GetXmax()) 
    for i in range(1,h_UP.GetNbinsX()+1):
        eUP = abs(h_UP.GetBinContent(i))
        eDN = abs(h_UP.GetBinContent(i))
        if h_DN: eDN = abs(h_DN.GetBinContent(i))
        ex = h_UP.GetBinWidth(i)/2.
        graph.SetPoint(i-1,h_UP.GetBinCenter(i),1.)
        graph.SetPointError(i-1,ex,ex,eUP,eDN)
    return graph

#____________________________________________________________
def get_total_stat_sys_hists(hists,sys_dict):
    """
    first make total hist for each systematic. 
    then sum deviations in quadrature bin-by-bin to make band.
    """

    ## make total sys hists
    h_total = histutils.add_hists(hists)
    h_total_stat = make_stat_hist(h_total)
    sys_hists_total = {}
    for sys in sys_dict.values():
        hists_up = []
        hists_dn = []
        for h in hists: 
            ## if hist not found, take nominal
            if not h.sys_hists.has_key(sys):
                hists_up.append(h)
                hists_dn.append(h)
            else:
                hists_up.append(h.sys_hists[sys][0] or h)
                hists_dn.append(h.sys_hists[sys][1] or h)

        h_up = histutils.add_hists(hists_up)
        h_dn = histutils.add_hists(hists_dn)
        sys_hists_total[sys] = (h_up,h_dn)

    ## sum bin-by-bin deviations in quadrature
    h_sys_UP = h_total.Clone('%s_sys_UP'%(h_total.GetName()))
    h_sys_DN = h_total.Clone('%s_sys_DN'%(h_total.GetName()))
    h_total_UP = h_total.Clone('%s_total_UP'%(h_total.GetName()))
    h_total_DN = h_total.Clone('%s_total_DN'%(h_total.GetName()))
    for i in range(1,h_total.GetNbinsX()+1):
        n = h_total.GetBinContent(i)
        tot_sys_UP2 = 0.0
        tot_sys_DN2 = 0.0
        for sys in sys_dict.values():
            (h_UP,h_DN) = sys_hists_total[sys]
            n_UP = h_UP.GetBinContent(i)
            n_DN = h_DN.GetBinContent(i)
            v_UP = (n_UP-n)/n if (n_UP!=None and n) else 0.0
            v_DN = (n_DN-n)/n if (n_DN!=None and n) else 0.0
            if sys.onesided:
              v_DN = v_UP
            if v_UP > 0.:
              tot_sys_UP2 += pow(v_UP,2)
            else:
              tot_sys_DN2 += pow(v_UP,2)
            if v_DN > 0.:
              tot_sys_UP2 += pow(v_DN,2)
            else:
              tot_sys_DN2 += pow(v_DN,2)
        tot_sys_UP = sqrt(tot_sys_UP2)            
        tot_sys_DN = sqrt(tot_sys_DN2)    
        h_sys_UP.SetBinContent(i,tot_sys_UP)
        h_sys_DN.SetBinContent(i,tot_sys_DN)
        
        stat = h_total_stat.GetBinContent(i)
        tot_UP = sqrt(pow(tot_sys_UP,2)+pow(stat,2))
        tot_DN = sqrt(pow(tot_sys_DN,2)+pow(stat,2))
        # tot_UP = sqrt(pow(tot_sys_UP,2))
        # tot_DN = sqrt(pow(tot_sys_DN,2))
        h_total_UP.SetBinContent(i,tot_UP)
        h_total_DN.SetBinContent(i,tot_DN)

    return (h_total_stat,h_sys_UP,h_sys_DN,h_total_UP,h_total_DN)



#____________________________________________________________
def plot_hist( 
    backgrounds   = None,
    signal        = None,   
    data          = None,
    region        = None,
    label         = None,
    label2        = None,
    icut          = None,
    histname      = None,
    log           = False,
    logx          = False,
    blind         = None,
    xmin          = None,
    xmax          = None,
    rebin         = None,
    rebinVar      = [],
    sys_dict      = None,
    do_ratio_plot = True,
    save_eps      = False,
    plotsfile     = None,
    sig_rescale   = None,
    xlabel        = None,
    Ymin          = 1e-2,
    ):
    
    '''
    TODO: 
        * move this to a new module when finished
        * write description for this function

    '''
    # print 'making plot: ', histname, ' in region', region
    print 'rebinVar', rebinVar
    # print xlabel
    
    #assert signal, "ERROR: no signal provided for plot_hist"
    assert backgrounds, "ERROR: no background provided for plot_hist"
    
    samples = list(backgrounds)
    if signal: samples += signal
    if data:   samples += [data]

    ## generate nominal hists
    hists = get_hists(
        region=region,
        icut=icut,
        histname=histname,
        samples=samples,
        rebin=rebin,
        rebinVar=rebinVar,
        sys_dict=sys_dict,
        )
    ## sum nominal background
    h_bkg_list = []
    for b in backgrounds:
      if not b in hists.keys(): continue
      h_bkg_list.append(hists[b])
    
    h_total = histutils.add_hists(h_bkg_list)

    ## get stat / sys bands
    if sys_dict: 
        total_hists = get_total_stat_sys_hists(h_bkg_list,sys_dict)
        
        g_stat = make_band_graph_from_hist(total_hists[0])
        g_stat.SetFillColor(ROOT.kGray)
        g_stat.SetLineColor(ROOT.kGray)
        g_tot  = make_band_graph_from_hist(total_hists[3],total_hists[4])
        g_tot.SetFillColor(ROOT.kOrange-9)
        g_tot.SetLineColor(ROOT.kOrange-9)

    else:
        h_total_stat = make_stat_hist(h_total)
        g_stat = make_band_graph_from_hist(h_total_stat)
        g_stat.SetFillColor(ROOT.kGray)
        g_stat.SetLineColor(ROOT.kGray)
        g_tot = None

    ## blind data and create ratio 
    h_data  = None
    h_ratio = None
    if data: 
        h_data = hists[data]
        h_data.SetMarkerSize(0.8)
        # if h_data.GetSumOfWeights()==h_data.GetEntries():
        h_data.Sumw2(0)
        h_data.SetBinErrorOption(1)
        # h_data.Sumw2(1)
        # h_data.SetBinErrorOption(1)
        if blind: apply_blind(h_data,blind)
        h_ratio = h_data.Clone('%s_ratio'%(h_data.GetName()))
        h_ratioGr = ROOT.TGraphAsymmErrors()
        h_ratioGr.SetMarkerSize(0.8)
        ## dont use Divide as it will propagate MC stat error to the ratio.
        #h_ratio.Divide(h_total)
        for i in range(1,h_ratio.GetNbinsX()+1):
          if h_total.GetBinContent(i)!=0 and h_data.GetBinContent(i)!=0:
            h_ratio.SetBinContent(i, h_ratio.GetBinContent(i)/h_total.GetBinContent(i) )
            h_ratio.SetBinError(i, h_ratio.GetBinError(i)/h_total.GetBinContent(i) )
            h_ratioGr.SetPoint(h_ratioGr.GetN(), h_ratio.GetBinCenter(i), h_ratio.GetBinContent(i) )
            h_ratioGr.SetPointError(h_ratioGr.GetN()-1, 0,0, h_data.GetBinErrorLow(i)/h_total.GetBinContent(i), h_data.GetBinErrorUp(i)/h_total.GetBinContent(i) )
          else:
            h_ratio.SetBinContent(i, -100 )
            h_ratio.SetBinError(i, 0 )
            h_ratioGr.SetPoint(h_ratioGr.GetN(), h_ratio.GetBinCenter(i), h_ratio.GetBinContent(i) )
            h_ratioGr.SetPointError(h_ratioGr.GetN()-1, 0,0, 0,0 )

    yaxistitle = None
    for b in reversed(backgrounds):
      if not b in hists.keys(): continue
      else : 
        yaxistitle = hists[b].GetYaxis().GetTitle()
        break

    ## create stack
    h_stack = ROOT.THStack()
    #for s in reversed(signal+backgrounds):
    for b in reversed(backgrounds):
      if not b in hists.keys(): continue
      h_stack.Add(hists[b])
   

    nLegend = len(backgrounds) + 2
    x_legend = 0.63
    x_leg_shift = 0
    y_leg_shift = -0.1 
    legYCompr = 8.0
    legYMax = 0.85
    legYMin = legYMax - (legYMax - (0.55 + y_leg_shift)) / legYCompr * nLegend
    legXMin = x_legend + x_leg_shift
    legXMax = legXMin + 0.25
  
    ## create legend (could use metaroot functionality?)
    if not do_ratio_plot:
      legXMin -= 0.005
      legXMax -= 0.058
    leg = ROOT.TLegend(legXMin/1.2,legYMin+0.05+(legYMax-legYMin)/1.9,legXMax+0.08,legYMax+0.05)
    leg.SetBorderSize(0)
    leg.SetNColumns(2)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.045)
    if not do_ratio_plot:
        leg.SetTextSize(0.035)
    if data: leg.AddEntry(h_data,"#font[42]{Data}",'P')
    for b in backgrounds: 
      if not b in hists.keys(): continue
      leg.AddEntry(hists[b],"#font[42]{"+str(b.tlatex)+"}",'F')

    if signal:
      leg2 = ROOT.TLegend(legXMin/1.2,legYMin+(legYMax-legYMin)/1.9-0.035*len(signal),legXMax+0.08-0.2,legYMin+0.05+(legYMax-legYMin)/1.9)
      leg2.SetBorderSize(0)
      leg2.SetFillColor(0)
      leg2.SetFillStyle(0)
      leg2.SetTextSize(0.045)
      if not do_ratio_plot:
          leg2.SetTextSize(0.035)
      if signal:
       for s in signal:
         sig_tag = s.tlatex
         if sig_rescale: sig_tag = "%d #times "%int(sig_rescale) + sig_tag
         if not s in hists.keys(): continue
         leg2.AddEntry(hists[s],"#font[42]{"+str(sig_tag)+"}",'F')


    ## create canvas
    reg = region
    if not reg: reg = ""
    name = '_'.join([reg,histname]).replace('/','_') 
    cname = "c_final_%s"%name
    if do_ratio_plot: c = ROOT.TCanvas(cname,cname,600,600)
    else: c = ROOT.TCanvas(cname,cname,600,600)
    if xmin==None: xmin = h_total.GetBinLowEdge(1)
    if xmax==None: xmax = h_total.GetBinLowEdge(h_total.GetNbinsX()+1)
    ymin = Ymin if log else 0.000001
    yvalues = []
    for i in range(h_total.FindBin(xmin),h_total.FindBin(xmax)):
      yvalues += [h_total.GetBinContent(i)]
    yvaluesdata = []
    for i in range(h_data.FindBin(xmin),h_data.FindBin(xmax)):
      yvaluesdata += [h_data.GetBinContent(i)]
    ymax = max(yvalues)
    ymaxdata = max(yvaluesdata)
    # for b in backgrounds:
    #   if not b in hists.keys(): continue
    #   ymax = max([ymax,hists[b].GetMaximum()])
    if data: ymax = max([ymax,ymaxdata])
    if log: ymax *= 4000.
    else:   ymax *= 1.7
    xtitle = h_total.GetXaxis().GetTitle()

    if do_ratio_plot: rsplit = 0.3
    else: rsplit = 0.
    pad1 = ROOT.TPad("pad1","top pad",0.,rsplit,1.,1.)
    pad1.SetLeftMargin(0.15)
    pad1.SetLeftMargin(0.15)
    pad1.SetTicky()
    pad1.SetTickx()
    if do_ratio_plot:
      pad1.SetBottomMargin(0.04)
      pad1.SetTopMargin(0.07)
    else: 
      pad1.SetBottomMargin(0.15)

    pad1.Draw()
    if do_ratio_plot:
      pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,rsplit)
      pad2.SetTopMargin(0.04)
      pad2.SetBottomMargin(0.40)
      pad2.SetLeftMargin(0.15)
      pad2.SetTicky()
      pad2.SetTickx()
      pad2.SetGridy()
    #if do_ratio_plot: pad2.Draw()
      pad2.Draw()
    pad1.cd()

    ytitle = "Events" 
    if not rebin: ytitle = yaxistitle
    elif rebin!=1:
      if not "BDT" in xtitle:
        ytitle += " / %s"%rebin
        if ("eta" in xtitle) or ("phi" in xtitle) or ("trk" in xtitle): pass
        else: ytitle += " GeV"
      else: ytitle += " / %s"%(0.05)

    fr1 = pad1.DrawFrame(xmin,ymin,xmax,ymax,';%s;%s'%(xtitle,ytitle))
    if do_ratio_plot:
      fr1.GetXaxis().SetTitleSize(0)
      fr1.GetXaxis().SetLabelSize(0)
    xaxis1 = fr1.GetXaxis()
    yaxis1 = fr1.GetYaxis()
    scale = (1.3+rsplit)

    if not do_ratio_plot:
      xaxis1.SetTitleSize( 0.7 * xaxis1.GetTitleSize() * scale )
      xaxis1.SetLabelSize( 0.7 * xaxis1.GetLabelSize() * scale )
      xaxis1.SetTickLength( xaxis1.GetTickLength() * scale )
      xaxis1.SetTitleOffset( xaxis1.GetTitleOffset() / scale  )
      xaxis1.SetLabelOffset( 1.* xaxis1.GetLabelOffset() / scale )
      xaxis1.SetNoExponent()
      xaxis1.SetMoreLogLabels()

    yaxis1.SetTitleSize( yaxis1.GetTitleSize() * scale /1.3 )
    yaxis1.SetTitleOffset( 2.1 * yaxis1.GetTitleOffset() / scale /1.8 )
    yaxis1.SetLabelSize( 0.8 * yaxis1.GetLabelSize() * scale / 1.09 )
    yaxis1.SetLabelOffset( 1. * yaxis1.GetLabelOffset() / scale )
    xaxis1.SetNdivisions(510)
    yaxis1.SetNdivisions(510)

    h_stack.Draw("SAME,HIST")
    # ROOT.TGaxis.SetMaxDigits(3)

    if signal:
     for s in reversed(signal):
       if not s in hists.keys(): continue
       if sig_rescale: hists[s].Scale(sig_rescale)
       hists[s].Draw("SAME,HIST")

    if data: 
      h_data.Draw("SAME X0 P E")
    pad1.SetLogy(log)
    if logx!=None : pad1.SetLogx(logx)
    leg.Draw()
    if signal: leg2.Draw()
    pad1.RedrawAxis()

    tlatex = ROOT.TLatex()
    tlatex.SetNDC()
    tlatex.SetTextSize(0.05)
    lx = 0.6 # for ATLAS internal
    ly = 0.845
    tlatex.SetTextFont(42)
    
    ty = 0.96
    th = 0.07
    tx = 0.18
    lumi = backgrounds[0].estimator.hm.target_lumi/1000.
    textsize = 0.8
    if not do_ratio_plot: textsize = 0.8
    latex_y = ty-2.*th+0.05
    tlatex.DrawLatex(tx,latex_y-0.054,'#font[42]{#sqrt{s} = 13 TeV, %2.1f fb^{-1}}'%(lumi) )
    ROOT.ATLASLabel(tx,latex_y,"Internal",1) 
    if label:
      latex_y -= 0.06
      #for i,line in enumerate(label):
      #  tlatex.DrawLatex(tx,latex_y-i*0.06,"#scale[%lf]{%s}"%(textsize,line))
      tlatex.DrawLatex(tx,latex_y - 0.04,"#font[42]{%s}"%label)
    if label2:
      latex_y -= 0.06
      #for i,line in enumerate(label):
      #  tlatex.DrawLatex(tx,latex_y-i*0.06,"#scale[%lf]{%s}"%(textsize,line))
      tlatex.DrawLatex(tx,latex_y - 0.025,"#font[42]{%s}"%label2)
    if blind:
        line = ROOT.TLine()
        line.SetLineColor(ROOT.kBlack)
        line.SetLineStyle(2)
        line.DrawLine(blind,ymin,blind,ymax)
        bltext = ROOT.TLatex()
        bltext.SetTextFont(42)
        bltext.SetTextSize(0.04)
        bltext.SetTextAngle(90.)
        bltext.SetTextAlign(31)
        bltext.DrawLatex(blind,ymax, 'Blind   ')

    if do_ratio_plot:
      pad2.cd()
      fr2 = pad2.DrawFrame(xmin,0.0,xmax,2.0,';%s;Data / Bkg.'%(xtitle))
      xaxis2 = fr2.GetXaxis()
      yaxis2 = fr2.GetYaxis()
      scale = (1. / rsplit)
      yaxis2.SetTitleSize( yaxis2.GetTitleSize() * scale / 1.2 )
      yaxis2.SetLabelSize( yaxis2.GetLabelSize() * scale / 1.2 )
      yaxis2.SetTitleOffset( 2.1* yaxis2.GetTitleOffset() / scale / 2 )
      yaxis2.SetLabelOffset(0.4 * yaxis2.GetLabelOffset() * scale )
      xaxis2.SetTitleSize( xaxis2.GetTitleSize() * scale / 1.2 )
      xaxis2.SetLabelSize( 0.8 * xaxis2.GetLabelSize() * scale )
      xaxis2.SetTickLength( xaxis2.GetTickLength() * scale )
      xaxis2.SetTitleOffset( 3.2* xaxis2.GetTitleOffset() / scale / 1.2  )
      xaxis2.SetLabelOffset( 2.5* xaxis2.GetLabelOffset() / scale )
      yaxis2.SetNdivisions(505)
      xaxis2.SetNdivisions(510)


      if logx: 
        pad2.SetLogx(logx) 
        xaxis2.SetMoreLogLabels()
        xaxis2.SetNoExponent()
      else: 
        pass

      if g_tot: 
         g_tot.Draw("E2")
         g_stat.Draw("SAME,E2")
         leg.AddEntry(g_stat,"#font[42]{"+str("MC Stat.")+"}",'F')
         leg.AddEntry(g_tot, "#font[42]{"+str("Sys. Unc.")+"}",'F')

      else: 
        g_stat.Draw("E2")
        leg.AddEntry(g_stat,"#font[42]{"+str("MC Stat.")+"}",'F')

      arrows = []
      if data: 
        #h_ratio.Draw("SAME X0 P E0")
        h_ratioGr.Draw("SAME E0 P")
        h_ratioGr.SetLineWidth(2)
        for bin_itr in range(1,h_ratio.GetNbinsX()+1):
          if (h_total.GetBinContent(bin_itr)==0 or h_data.GetBinContent(bin_itr)==0): continue
          if (h_ratio.GetBinContent(bin_itr)-h_data.GetBinErrorLow(bin_itr)/h_total.GetBinContent(bin_itr)) > 2.01:
            print h_ratio.GetBinCenter(bin_itr)," ",h_ratio.GetBinContent(bin_itr)
            arrowX = h_ratio.GetBinCenter(bin_itr)
            arrow = ROOT.TArrow(arrowX,1.85,arrowX,2.0,0.012,"=>");
            arrow.SetLineWidth(2)
            arrow.SetLineColor(ROOT.kRed+1)
            arrow.SetFillColor(ROOT.kRed+1)
            arrows += [arrow]
            arrow.Draw()
          # elif (h_ratio.GetBinContent(bin_itr)+h_data.GetBinErrorUp(bin_itr)/h_total.GetBinContent(bin_itr)) < 0.49 and h_ratio.GetBinContent(bin_itr) not in [-100,0]:
          #   print h_ratio.GetBinCenter(bin_itr)," ",h_ratio.GetBinContent(bin_itr)
          #   arrowX = h_ratio.GetBinCenter(bin_itr)
          #   arrow = ROOT.TArrow(arrowX,0.50,arrowX,0.65,0.012,"<=");
          #   arrow.SetLineWidth(2)
          #   arrow.SetLineColor(ROOT.kRed+1)
          #   arrow.SetFillColor(ROOT.kRed+1)
          #   arrows += [arrow]
          #   arrow.Draw()
      pad2.RedrawAxis()
      pad2.RedrawAxis("g")

    if xlabel:
        if not do_ratio_plot:
            xaxis1.SetTitle(xlabel)
        else:
            xaxis2.SetTitle(xlabel)        

    print 'saving plot...'
    if save_eps:
     eps_file = plotsfile.replace(".root",".eps")
     if not log: c.SaveAs(eps_file)
     else: c.SaveAs(eps_file.replace(".eps","_LOG.eps"))

    fout = ROOT.TFile.Open(plotsfile,'UPDATE')
    fout.WriteTObject(c)
    fout.Close()

#____________________________________________________________
def write_hist(
        backgrounds = None,
        signal      = None,
        data        = None,
        region      = None,
        icut        = None,
        histname    = None,
        rebin       = None,
        rebinVar    = [],
        sys_dict    = None,
        outname     = None,
        rebinToEq   = None,
        regName     = None,
        varName     = None,
        noNorm      = None,
        ):
    """
    write hists for backgrounds, signals and data to file.
    will also write sys hists if sys_dict passed. 
    also write smtot hists for summed background.
    No folder structure is provided
    """
    samples = list(backgrounds)
    if signal: samples += signal
    if data: samples += [data]
    ## generate nominal hists
    hists = get_hists(
        region=region,
        icut=icut,
        histname=histname,
        samples=samples,
        rebin=rebin,
        rebinVar=rebinVar,
        sys_dict=sys_dict,
        )

    print "noNorm ",noNorm

    #histnamestr = histname.replace('/','_')
    fname = outname
    fout = ROOT.TFile.Open(fname,'RECREATE')
    for s,h in hists.items():
        # print s.name
        # print "hist name: ", h.GetName()
        # print h.GetSum()
        if hasattr(s,"nameSuffix"):
            s.name += s.nameSuffix
        hname = ""
        hnameNorm = ""
        if rebinToEq:
            hname = 'h%sNom_%s_%s' % (s.name,region if not regName else regName, varName)
            hnameNorm = 'h%sNom_%sNorm' % (s.name,region if not regName else regName)
            h.SetNameTitle(hname+"temp",hname+"temp")
        else:
            hname = 'h_%s_nominal_%s' % (region,s.name)
            h.SetNameTitle(hname,hname)
        hEquiDistant = None
        hNorm = None
        if rebinToEq:
            nbins = h.GetNbinsX()
            hEquiDistant = ROOT.TH1F(hname,hname,nbins,0,nbins)
            hEquiDistant.Sumw2(1)
            hNorm = ROOT.TH1F(hnameNorm+"temp",hnameNorm+"temp",nbins,0,nbins)
            hNorm.Sumw2(1)
            for i in range(0,nbins+2):
                binVal = 0
                binErr = 0
                if h.GetBinContent(i) >= 0 :
                    binVal = h.GetBinContent(i)
                    binErr = h.GetBinError(i)
                else:
                    binVal = 0.
                    binErr = 0.
                hEquiDistant.SetBinContent(i,binVal)
                hEquiDistant.SetBinError(i,binErr)
                hNorm.SetBinContent(i,binVal)
                hNorm.SetBinError(i,binErr)
            hNorm.Rebin(nbins)
            if s.name == "fakes":
              print "XXXXXXXXXXXXXXXXXXX fixing fakes with 0 entries ",s.name, " ",region
              fixFakes(hEquiDistant,0.5 if "elect" in region else 0.9)
            fout.WriteTObject(hEquiDistant,hname)
            hNormOut = ROOT.TH1F(hnameNorm,hnameNorm,1,0.5,1.5)
            hNormOut.SetBinContent(1,hNorm.GetBinContent(1))
            hNormOut.SetBinError(1,hNorm.GetBinError(1))
            if noNorm != True:
              fout.WriteTObject(hNormOut,hnameNorm)
        else:
            fout.WriteTObject(h,hname)
        ## systematics
        if hasattr(h,'sys_hists'):
         print "sys hists"
         if sys_dict:
            newHup = None
            newHdn = None
            for sys,hsys in h.sys_hists.items():
                
                s_name = sys.name

                hname = ""
                hnameNorm = ""
                if rebinToEq:
                    hname_sys_up = 'h%s%s_%s_%s' % (s.name,s_name+"High",region if not regName else regName, varName)
                    hname_sys_dn = 'h%s%s_%s_%s' % (s.name,s_name+"Low",region if not regName else regName, varName)
                    hname_sys_upNorm = 'h%s%s_%sNorm' % (s.name,s_name+"High",region if not regName else regName)
                    hname_sys_dnNorm = 'h%s%s_%sNorm' % (s.name,s_name+"Low",region if not regName else regName)
                    if hsys[0]: hsys[0].SetNameTitle(hname_sys_up+"temp",hname_sys_up+"temp")
                    if hsys[1]: hsys[1].SetNameTitle(hname_sys_dn+"temp",hname_sys_dn+"temp")

                else:
                    hname_sys_up = hname.replace('nominal','%s_%s' % (s_name,'UP'))
                    hname_sys_dn = hname.replace('nominal','%s_%s' % (s_name,'DN'))
                    if hsys[0]: hsys[0].SetNameTitle(hname_sys_up,hname_sys_up)
                    if hsys[1]: hsys[1].SetNameTitle(hname_sys_dn,hname_sys_dn)
                    fout.WriteTObject(hsys[0],hname_sys_up)
                    fout.WriteTObject(hsys[1],hname_sys_dn)

                hupEquiDistant = None
                hdnEquiDistant = None
                hupNorm = None
                hdnNorm = None

                if hsys[0] and hsys[1] and rebinToEq:
                    nbins = h.GetNbinsX()
                    hupEquiDistant = ROOT.TH1F(hname_sys_up,hname_sys_up,nbins,0,nbins)
                    hdnEquiDistant = ROOT.TH1F(hname_sys_dn,hname_sys_dn,nbins,0,nbins)
                    hupNorm = ROOT.TH1F(hname_sys_upNorm+"temp",hname_sys_upNorm+"temp",nbins,0,nbins)
                    hdnNorm = ROOT.TH1F(hname_sys_dnNorm+"temp",hname_sys_dnNorm+"temp",nbins,0,nbins)
                    hupEquiDistant.Sumw2(1)
                    hdnEquiDistant.Sumw2(1)
                    hupNorm.Sumw2(1)
                    hdnNorm.Sumw2(1)
                    for i in range(0,nbins+2):
                        binValU = 0
                        binErrU = 0
                        binValD = 0
                        binErrD = 0
                        if hsys[0].GetBinContent(i) >= 0:
                            binValU = hsys[0].GetBinContent(i)
                            binErrU = hsys[0].GetBinError(i)
                        else:
                            binValU = 0.
                            binErrU = 0.
                        if hsys[1].GetBinContent(i) >= 0:
                            binValD = hsys[1].GetBinContent(i)
                            binErrD = hsys[1].GetBinError(i)
                        else:
                            binValD = 0.
                            binErrD = 0.
                        hupEquiDistant.SetBinContent(i,binValU)
                        hupEquiDistant.SetBinError(i,binErrU)
                        hdnEquiDistant.SetBinContent(i,binValD)
                        hdnEquiDistant.SetBinError(i,binErrD)
                        hupNorm.SetBinContent(i,binValU)
                        hupNorm.SetBinError(i,binErrU)
                        hdnNorm.SetBinContent(i,binValD)
                        hdnNorm.SetBinError(i,binErrD)
                    hupNorm.Rebin(nbins)
                    hdnNorm.Rebin(nbins)

                if rebinToEq:
                    if s.name == "fakes":
                      fixFakes(hupEquiDistant,0.5 if "elect" in region else 0.9)
                      fixFakes(hdnEquiDistant,0.5 if "elect" in region else 0.9)
                    fout.WriteTObject(hupEquiDistant,hname_sys_up)
                    fout.WriteTObject(hdnEquiDistant,hname_sys_dn)
                    hupNormOut = ROOT.TH1F(hname_sys_upNorm,hname_sys_upNorm,1,0.5,1.5)
                    if(hsys[0]):
                        hupNormOut.SetBinContent(1,hupNorm.GetBinContent(1))
                        hupNormOut.SetBinError(1,hupNorm.GetBinError(1))
                    hdnNormOut = ROOT.TH1F(hname_sys_dnNorm,hname_sys_dnNorm,1,0.5,1.5)
                    if(hsys[1]):
                        hdnNormOut.SetBinContent(1,hdnNorm.GetBinContent(1))
                        hdnNormOut.SetBinError(1,hdnNorm.GetBinError(1))
                    if noNorm != True:
                      fout.WriteTObject(hupNormOut,hname_sys_upNorm)
                      fout.WriteTObject(hdnNormOut,hname_sys_dnNorm)


    ## create total background hists
    #h_total = histutils.add_hists([ hists[s] for s in backgrounds ])
    #fout.WriteTObject(h_total,'h_%s_nominal_smtot'%region)
    
    fout.Close()

#____________________________________________________________
def generateLogBins(bins_N,bins_min,bins_max):
  bins = []
  bins += [bins_min]
  bins_factor = pow( Decimal(bins_max)/Decimal(bins_min) , Decimal(1)/Decimal(bins_N) )
  for i in range(1,bins_N+1):
    bins += [bins[i-1]*bins_factor]
  for i in range(bins_N+1):
    bins[i] = round(bins[i],0)
    if i!=0: assert bins[i]!=bins[i-1], "two consetuvie bin edges have the same value due to rounding"
  return bins

def list_open_files():
    l = ROOT.gROOT.GetListOfFiles()
    itr = l.MakeIterator()
    obj = itr.Next()
    while obj:
        print obj.GetName()
        obj = itr.Next()

#____________________________________________________________
def make_sys_hists(nominal, sys, rebin, rebinVar, X):
  if rebin and len(rebinVar)==0:
    if nominal: nominal.Rebin(rebin)
    for i,s in enumerate(sys):
      if s: s.Rebin(rebin)
      sys[i] = s
  elif len(rebinVar)>1:
    runArray = array('d',rebinVar)
    nominal = nominal.Rebin( len(rebinVar)-1, nominal.GetName()+"Var", runArray )
    nominal.SetBinContent(nominal.GetNbinsX(), nominal.GetBinContent(nominal.GetNbinsX()+1) + nominal.GetBinContent(nominal.GetNbinsX()) )
    nominal.SetBinError(nominal.GetNbinsX(), sqrt(nominal.GetBinError(nominal.GetNbinsX()+1)**2 + nominal.GetBinError(nominal.GetNbinsX())**2) )
    for i,s in enumerate(sys):
      s = s.Rebin( len(rebinVar)-1, s.GetName()+"Var"+str(i), runArray )
      s.SetBinContent(s.GetNbinsX(), s.GetBinContent(s.GetNbinsX()+1) + s.GetBinContent(s.GetNbinsX()) )
      s.SetBinError(s.GetNbinsX(), sqrt(s.GetBinError(s.GetNbinsX()+1)**2 + s.GetBinError(s.GetNbinsX())**2) )
      sys[i] = s
      assert s.GetNbinsX() == nominal.GetNbinsX(), "incompatible histograms "+str(s.GetNbinsX())+" vs "+str(nominal.GetNbinsX())

  h_up = nominal.Clone()
  h_dn = nominal.Clone()

  for i in range(0,nominal.GetNbinsX()+1):
    yn = nominal.GetBinContent(i)
    for s in sys:
      y  = s.GetBinContent(i)
      ey = h_up.GetBinContent(i) - yn
      h_up.SetBinContent( i, yn + sqrt(ey**2 + (y-yn)**2)/X )
      h_dn.SetBinContent( i, yn - sqrt(ey**2 + (y-yn)**2)/X )

  return (h_up,h_dn)



## EOF
