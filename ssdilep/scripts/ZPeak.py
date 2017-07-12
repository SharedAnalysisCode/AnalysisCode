## modules
import ROOT
from array import array

import histmgr
import funcs
import os
import re

ROOT.gROOT.SetBatch(True)

ROOT.TGaxis.SetMaxDigits(4)
ROOT.gStyle.SetHatchesSpacing(0.5)
ROOT.gStyle.SetPadTickY(0)


#-----------------
# input
#-----------------

MARKERSIZE = 1.0

SSFile = ROOT.TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeakPaper/hists_invMass_7_same-sign-Zpeak-CR_ZPeak.root","READ")
OSFile = ROOT.TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeakPaper/hists_invMass_7_opposite-sign-Zpeak-CR_ZPeak.root","READ")

OSdata = OSFile.Get("h_opposite-sign-Zpeak-CR_nominal_data")
OSMC   = OSFile.Get("h_opposite-sign-Zpeak-CR_nominal_AllSM")

SSdata = SSFile.Get("h_same-sign-Zpeak-CR_nominal_data")
SSMC   = SSFile.Get("h_same-sign-Zpeak-CR_nominal_AllSM")

print OSdata," ",OSMC," ",SSdata," ",SSMC

canv = ROOT.TCanvas("c1","c1",800,600)
canv.cd()
canv.SetRightMargin(0.1)
canv.SetTopMargin(0.07)

OSdata.Draw("p e x0")
OSdata.GetXaxis().SetRangeUser(75,105)
OSdata.GetXaxis().SetLabelOffset(OSdata.GetXaxis().GetLabelOffset()+0.015)
OSdata.GetYaxis().SetRangeUser(0,1.35*OSdata.GetMaximum())
OSdata.GetYaxis().SetLabelOffset(OSdata.GetYaxis().GetLabelOffset())
OSdata.SetMarkerSize(MARKERSIZE)
OSMC.SetLineColor(ROOT.kGray+3)
OSMC.Scale(1.01)
canv.Update()

rightmax = 1.35*SSdata.GetMaximum()
scale = ROOT.gPad.GetUymax()/rightmax


SSGr = ROOT.TGraphErrors()
OSGr = ROOT.TGraphErrors()

for i in range(1,OSMC.GetNbinsX()+1):
  OSGr.SetPoint(OSGr.GetN(),OSMC.GetBinCenter(i),OSMC.GetBinContent(i))
  SSGr.SetPoint(SSGr.GetN(),SSMC.GetBinCenter(i),SSMC.GetBinContent(i)*scale)

  OSGr.SetPointError(OSGr.GetN()-1,OSMC.GetBinWidth(i)/2.,ROOT.TMath.Sqrt(OSMC.GetBinError(i)**2+(OSMC.GetBinContent(i)*0.03)**2 ) )
  SSGr.SetPointError(SSGr.GetN()-1,SSMC.GetBinWidth(i)/2.,ROOT.TMath.Sqrt((SSMC.GetBinError(i)*scale)**2+(SSMC.GetBinContent(i)*scale*0.03)**2 ) )

OSGr.SetFillStyle(3354)
SSGr.SetFillStyle(3354)

OSGr.SetFillColor(ROOT.kGray+2)
OSGr.SetLineColor(ROOT.kGray+3)
OSGr.SetLineWidth(2)
SSGr.SetFillColor(ROOT.kRed-2)
SSGr.SetLineColor(ROOT.kRed)
SSGr.SetLineWidth(2)


OSGr.Draw("same e2")
OSMC.Draw("same hist")


SSdata.SetMarkerColor(ROOT.kRed)
SSdata.SetLineColor(ROOT.kRed)
SSMC.SetLineColor(ROOT.kRed)
SSdata.SetMarkerSize(MARKERSIZE)
SSdata.Scale(scale)
SSMC.Scale(scale)
SSdata.Draw("p e x0 same")
SSGr.Draw("same e2")
SSMC.Draw("same hist")


OSdata.Draw("same p e x0")
SSdata.Draw("p e x0 same")

#draw an axis on the right side
axis = ROOT.TGaxis(ROOT.gPad.GetUxmax(),ROOT.gPad.GetUymin(),ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(),0,rightmax,510,"+L");
axis.SetLabelFont(OSdata.GetYaxis().GetLabelFont())
axis.SetLabelSize(OSdata.GetYaxis().GetLabelSize())
axis.SetLabelOffset(OSdata.GetYaxis().GetLabelOffset())
axis.SetLabelColor(ROOT.kRed)
axis.SetLineColor(ROOT.kRed)
axis.SetTextColor(ROOT.kRed)
# axis.SetTitle("Events / (1 GeV)")
# axis.SetTitleFont(OSdata.GetYaxis().GetTitleFont())
# axis.SetTitleSize(OSdata.GetYaxis().GetTitleSize())
# axis.SetTitleOffset(OSdata.GetYaxis().GetTitleOffset())
axis.Draw()



ROOT.ATLASLabel(0.2,0.875,"internal",1)
ROOT.myText(0.2,0.825,1,"Z #rightarrow ee peak")
ROOT.myText(0.195,0.768,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}")
leg = ROOT.TLegend(0.45,0.808,0.89,0.911)
leg.SetBorderSize(0)
leg.SetNColumns(2)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.045)
leg.AddEntry(OSdata,"#font[42]{OC data}","p e")
leg.AddEntry(SSdata,"#font[42]{SC data}","p e")
leg.AddEntry(OSGr,"#font[42]{OC tot. SM}","l f")
leg.AddEntry(SSGr,"#font[42]{SC tot. SM}","l f")
leg.Draw()

canv.Print("ZPeakPaper.eps")

 ## EOF



