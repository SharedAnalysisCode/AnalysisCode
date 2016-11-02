import os
import ROOT
from array import array

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0000)

# -------------------------------------------------------------------------------------
# config
# -------------------------------------------------------------------------------------
indir   = "/coepp/cephfs/mel/fscutti/Analysis/ssdilep/scripts/FakesDir"
tag     = "Sherpa"
name    = "18SepSys"

# pt
'''
var     = "mulead_pt"
axislab = "p_{T}(#mu_{lead}) [GeV]"
new_bins = array('d', [0.,22.,23.,25.,28.,32.,36.,40.,45.,60.,200.])
'''

# eta
var     = "mulead_eta"
axislab = "#eta(#mu_{lead})"
new_bins = array('d', [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5,])


infile  = "merged_fr_"+var+"_"+name+"_"+tag+".root"
outfile = "sys_fr_"+var+"_"+name+"_"+tag+".root"
inf     = ROOT.TFile.Open(os.path.join(indir,infile),"READ")


# -------------------------------------------------------------------------------------

hdict = {}

#hdict["NOM"] = inf.Get("h_fr_FR1").Clone()
hdict["NOM"] = inf.Get("h_fr_FR1").Clone()
n_bins = hdict["NOM"].GetNbinsX()
#for i in [2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
for i in [2,3,4,5,6,7,8]:
  hdict["SYS%s"%str(i)] = inf.Get("h_fr_FR%s"%str(i)).Clone()

slabel = {}
slabel["NOM"]  = "nominal"
slabel["SYS2"] = "E^{miss}_{T} < 30 GeV"
slabel["SYS3"] = "E^{miss}_{T} < 50 GeV"
slabel["SYS4"] = "p_{T}(jet) > 40 GeV"
slabel["SYS5"] = "d_{0}/#sigma(d_{0}) < 2"
slabel["SYS6"] = "d_{0}/#sigma(d_{0}) < 4"
slabel["SYS7"] = "#Delta#phi(#mu,jet) < 2.8"
slabel["SYS8"] = "#Delta#phi(#mu,jet) < 2.6"

g_sys_fr = ROOT.TGraphAsymmErrors(n_bins)
g_nom_fr = ROOT.TGraphAsymmErrors(n_bins)


for ibin in xrange(1,n_bins+1):
    g_sys_fr.SetPoint(ibin,hdict["NOM"].GetBinCenter(ibin),hdict["NOM"].GetBinContent(ibin))  
    g_nom_fr.SetPoint(ibin,hdict["NOM"].GetBinCenter(ibin),hdict["NOM"].GetBinContent(ibin))  

    g_sys_fr.SetPointEYlow(ibin, hdict["NOM"].GetBinErrorLow(ibin))
    g_sys_fr.SetPointEYhigh(ibin, hdict["NOM"].GetBinErrorUp(ibin))
    
    g_nom_fr.SetPointEYlow(ibin, hdict["NOM"].GetBinErrorLow(ibin))
    g_nom_fr.SetPointEYhigh(ibin, hdict["NOM"].GetBinErrorUp(ibin))

    g_sys_fr.SetPointEXlow(ibin, hdict["NOM"].GetBinWidth(ibin)/2.)
    g_sys_fr.SetPointEXhigh(ibin, hdict["NOM"].GetBinWidth(ibin)/2.)
    
    g_nom_fr.SetPointEXlow(ibin, hdict["NOM"].GetBinWidth(ibin)/2.)
    g_nom_fr.SetPointEXhigh(ibin, hdict["NOM"].GetBinWidth(ibin)/2.)

g_nom_fr.SetNameTitle("g_fr_stat","")
g_sys_fr.SetNameTitle("g_fr_stat_sys","")

for sys,hist in hdict.iteritems():
  if sys == "NOM": continue
  for ibin in xrange(1,n_bins+1):
    
    nom_minus_sys = hdict["NOM"].GetBinContent(ibin)-hdict[sys].GetBinContent(ibin)
    
    if nom_minus_sys>0. and nom_minus_sys > hdict[sys].GetBinErrorUp(ibin):
     g_sys_fr.SetPointEYlow(ibin, max(g_sys_fr.GetErrorYlow(ibin),abs(nom_minus_sys)))

    if nom_minus_sys<0. and abs(nom_minus_sys) > hdict[sys].GetBinErrorLow(ibin):
     g_sys_fr.SetPointEYhigh(ibin, max(g_sys_fr.GetErrorYhigh(ibin),abs(nom_minus_sys)))
    
c = ROOT.TCanvas("c_fr","c_fr",650,600)
c.SetTopMargin(0.05)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.13)
c.SetRightMargin(0.05)
c.SetTickx()
c.SetTicky()

l = ROOT.TLegend(0.15,0.65,0.55,0.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)


g_sys_fr.GetYaxis().SetTitle("mis-ID probability")
g_sys_fr.GetXaxis().SetTitle(axislab)
g_sys_fr.GetYaxis().SetTitleSize(0.045)
g_sys_fr.GetXaxis().SetTitleSize(0.045)
g_sys_fr.GetYaxis().SetLabelSize(0.045)
g_sys_fr.GetXaxis().SetLabelSize(0.045)
g_sys_fr.GetYaxis().SetTitleOffset(1.2)
g_sys_fr.GetXaxis().SetTitleOffset(1.2)
g_sys_fr.GetXaxis().SetRangeUser(min(new_bins),max(new_bins))
g_sys_fr.SetLineColor(ROOT.kYellow)
g_sys_fr.SetMarkerColor(ROOT.kBlack)
g_sys_fr.SetFillColor(ROOT.kYellow)
g_sys_fr.SetMarkerSize(1.3)
g_sys_fr.SetMaximum(1.0)
g_sys_fr.SetMinimum(0)

g_nom_fr.GetYaxis().SetTitle("mis-ID probability")
g_nom_fr.GetXaxis().SetTitle(axislab)
g_nom_fr.GetYaxis().SetTitleSize(0.045)
g_nom_fr.GetXaxis().SetTitleSize(0.045)
g_nom_fr.GetYaxis().SetLabelSize(0.045)
g_nom_fr.GetXaxis().SetLabelSize(0.045)
g_nom_fr.GetYaxis().SetTitleOffset(1.2)
g_nom_fr.GetXaxis().SetTitleOffset(1.2)
g_nom_fr.GetXaxis().SetRangeUser(min(new_bins),max(new_bins))
g_nom_fr.SetLineColor(ROOT.kBlack)
g_nom_fr.SetLineWidth(2)
g_nom_fr.SetMarkerColor(ROOT.kBlack)
g_nom_fr.SetMarkerStyle(20)
g_nom_fr.SetMarkerSize(0.9)
g_nom_fr.SetMaximum(1.0)
g_nom_fr.SetMinimum(0)

c.cd() 

g_sys_fr.Draw("APE2")
g_nom_fr.Draw("SAME,P")
l.SetHeader("Nominal mis-ID probability")
l.AddEntry(g_sys_fr,"stat.+sys.","F")
l.AddEntry(g_nom_fr,"stat.","PL")
l.Draw()
c.RedrawAxis()

c2 = ROOT.TCanvas("c_sys","c_sys",650,600)
c2.SetTopMargin(0.05)
c2.SetBottomMargin(0.13)
c2.SetLeftMargin(0.13)
c2.SetRightMargin(0.05)
c2.SetTickx()
c2.SetTicky()

l2 = ROOT.TLegend(0.15,0.5,0.45,0.9)
l2.SetBorderSize(0)
l2.SetFillColor(0)
l2.SetFillStyle(0)

c2.cd()

hdict["NOM"].SetStats(0)
hdict["NOM"].SetLineWidth(2)
hdict["NOM"].Draw()
l2.SetHeader("Systematics")

l2.AddEntry(hdict["NOM"],"nominal","PL")

for sys,hist in hdict.iteritems():
    if sys == "NOM": continue
    hist.Draw("SAME,E1")
    l2.AddEntry(hist,slabel[sys],"PL")

hdict["NOM"].Draw("SAME,PE1")

l2.Draw()

outfile = ROOT.TFile.Open(os.path.join(indir,outfile),"RECREATE")

outfile.WriteTObject(g_sys_fr)
outfile.WriteTObject(g_nom_fr)
outfile.WriteTObject(c)
outfile.WriteTObject(c2)

