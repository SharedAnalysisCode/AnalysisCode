## modules
import ROOT
from array import array

import histmgr
import funcs
import os
import re

from optparse import OptionParser

#-----------------
# input
#-----------------
parser = OptionParser()
parser.add_option('-i', '--input', dest='infile',
                  help='input directory',metavar='INFILE',default=None)

(options, args) = parser.parse_args()

indir = options.infile

infile = []
finalEff = []
mass_points = []

color_palette = []

ROOT.gROOT.SetBatch(True)

for m in range(21):
  infile += [ROOT.TFile(indir+"Pythia8EvtGen_A14NNPDF23LO_DCH" + str(250+50*m) + ".root","READ")]
  print indir+"Pythia8EvtGen_A14NNPDF23LO_DCH" + str(250+50*m) + ".root"
  finalEff += [[0]]
  mass_points += [250+50*m]
  if m < 5:
    color_palette += [ROOT.kRed + 4 - 2*m%5]
  elif m < 10:
    color_palette += [ROOT.kBlue + 4 - 2*m%5]
  elif m < 15:
    color_palette += [ROOT.kSpring + 4 - 2*m%5]
  elif m < 20:
    color_palette += [ROOT.kOrange + 4 - 2*m%5]
  elif m < 25:
    color_palette += [ROOT.kPink + 4 - 2*m%5]
  elif m < 30:
    color_palette += [ROOT.kTeal + 4 - 2*m%5]

xaxis = [0]
eff = []

m_iter = -1
for mass in infile:
  m_iter += 1
  print m_iter
  for iterr in range(1,101):

    br = iterr/100.

    eeee = br*br
    eemm = 2*br*(1-br)
    mmmm = (1-br)*(1-br)

    assert abs(eeee+eemm+mmmm-1.0)<0.001, "something wrong " + str(br) + " " + str(eeee+eemm+mmmm)

    cutflow_presel = mass.Get("cutflow_presel")
    assert cutflow_presel.GetXaxis().GetBinLabel(3)=="Pileup", "not pileup"

    cutflow_SR1_eeee = mass.Get("cutflow_SR1-ele-SR-signal-eeee").Clone("eeee" + str(m_iter) + str(br) )
    cutflow_SR1_eeee.GetXaxis().SetBinLabel(2,"DCHFilter")
    cutflow_SR1_eemm = mass.Get("cutflow_SR1-ele-SR-signal-eemm").Clone("eemm" + str(m_iter) + str(br) )
    cutflow_SR1_eemm.GetXaxis().SetBinLabel(2,"DCHFilter")


    cutflow_SR1_eeee.Scale(eeee*16)
    cutflow_SR1_eemm.Scale(eemm*8)

    cutflow_SR1_eeee.Add(cutflow_SR1_eemm)

    cutflow_SR1_eeee.Scale( 1./(cutflow_presel.GetBinContent(3)) )

    finalEff[m_iter] += [cutflow_SR1_eeee.GetBinContent(cutflow_SR1_eeee.GetNbinsX())]

    if m_iter == 0:
      xaxis += [br]

  ArrayX = array('d',xaxis)

  effVsBr = ROOT.TH1F("eff"+ str(m_iter),"eff"+ str(m_iter),len(xaxis)-1,ArrayX)
  for i in range(1,effVsBr.GetNbinsX()+1):
    effVsBr.SetBinContent(i,finalEff[m_iter][i-1])
    effVsBr.SetBinError(i,0)
    effVsBr.SetLineColor( color_palette[m_iter] )
    effVsBr.SetMarkerColor( color_palette[m_iter] )

  eff += [effVsBr]

leg = ROOT.TLegend(0.5,0.2,0.9,0.55)
leg.SetBorderSize(0)
leg.SetNColumns(2)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.035)


canv = ROOT.TCanvas("c1","c1",600,600)
canv.cd()
hstack = ROOT.THStack("hs","hs")
for e,m in zip(eff,mass_points):
  hstack.Add(e)
  leg.AddEntry(e,"#font[42]{DCH"+ str(m) +"}",'l')

hstack.Draw("line nostack")
hstack.GetXaxis().SetTitle("Br(H^{#pm#pm}#rightarrow e^{#pm}e^{#pm}) = 1-Br(H^{#pm#pm}#rightarrow X)")
hstack.GetYaxis().SetTitle("SR1(e^{#pm}e^{#pm} or e^{#pm}e^{#pm}e^{#mp}) efficiency")
hstack.SetMaximum(0.5)
leg.Draw()
ROOT.ATLASLabel(0.2,0.9,"internal",1)
ROOT.myText(0.2,0.85,1,"#sqrt{s}=13 TeV")
canv.Print("efficiency.eps")


 ## EOF



