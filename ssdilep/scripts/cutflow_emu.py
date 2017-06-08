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
  print mass
  m_iter += 1
  print m_iter
  for iterr in range(1,101):

    br = iterr/100.

    emem = br*br
    emmm = 2*br*(1-br)
    mmmm = (1-br)*(1-br)

    assert abs(emem+emmm+mmmm-1.0)<0.001, "something wrong " + str(br) + " " + str(emem+emmm+mmmm)

    cutflow_presel = mass.Get("cutflow_presel")
    assert cutflow_presel.GetXaxis().GetBinLabel(4)=="Pileup", "not pileup " + cutflow_presel.GetXaxis().GetBinLabel(4)

    cutflow_SR_emem = mass.Get("cutflow_SR-lepton-SR-signal-emem").Clone("emem" + str(m_iter) + str(br) )
    cutflow_SR_emem.GetXaxis().SetBinLabel(2,"DCHFilter")
    cutflow_SR_emmm = mass.Get("cutflow_SR-lepton-SR-signal-emmm").Clone("emmm" + str(m_iter) + str(br) )
    cutflow_SR_emmm.GetXaxis().SetBinLabel(2,"DCHFilter")


    cutflow_SR_emem.Scale(emem*4)
    cutflow_SR_emmm.Scale(emmm*4)

    cutflow_SR_emem.Add(cutflow_SR_emmm)

    cutflow_SR_emem.Scale( 1./(cutflow_presel.GetBinContent(4)) )

    finalEff[m_iter] += [cutflow_SR_emem.GetBinContent(cutflow_SR_emem.GetNbinsX())]

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

leg = ROOT.TLegend(0.2,0.5,0.55,0.83)
leg.SetBorderSize(0)
leg.SetNColumns(2)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.035)

ArrayY = array('d',[x-25 for x in mass_points]+[mass_points[-1]+25])
print ArrayY

efficiency = ROOT.TH2D("efficiency","efficiency",len(xaxis)-1,ArrayX,len(mass_points),ArrayY)
print efficiency.GetXaxis().GetBinCenter(1)
print efficiency.GetYaxis().GetBinCenter(1)

canv = ROOT.TCanvas("c1","c1",600,600)
canv.cd()
hstack = ROOT.THStack("hs","hs")
for e,m in zip(eff,mass_points):
  hstack.Add(e)
  leg.AddEntry(e,"#font[42]{DCH"+ str(m) +"}",'l')
  for i in range(1,e.GetNbinsX()+1):
    efficiency.SetBinContent(efficiency.FindBin(e.GetXaxis().GetBinCenter(i),m), e.GetBinContent(i))

hstack.Draw("line nostack")
hstack.GetXaxis().SetTitle("Br(H^{#pm#pm}#rightarrow e^{#pm}#mu^{#pm}) = 1-Br(H^{#pm#pm}#rightarrow X)")
hstack.GetYaxis().SetTitle("SR efficiency")
hstack.SetMaximum(1)
leg.Draw()
ROOT.ATLASLabel(0.2,0.9,"internal",1)
ROOT.myText(0.2,0.85,1,"#sqrt{s}=13 TeV")
canv.Print("efficiency_emu.eps")

canv2 = ROOT.TCanvas("c2","c2",800,600)
canv2.cd()
canv2.SetRightMargin(0.15)
efficiency.Draw("COLZ")
efficiency.GetXaxis().SetTitle("Br(H^{#pm#pm}#rightarrow e^{#pm}#mu^{#pm}) = 1-Br(H^{#pm#pm}#rightarrow X)")
efficiency.GetYaxis().SetTitle("m(H^{#pm#pm}) [GeV]")
ROOT.ATLASLabel(0.2,0.9,"internal",ROOT.kWhite)
ROOT.myText(0.2,0.85,ROOT.kWhite,"#sqrt{s}=13 TeV, SR efficiency")
canv2.Print("efficiency2D_emu.eps")

outfile = ROOT.TFile("efficiency_emu.root","RECREATE")
outfile.cd()
efficiency.Write("efficiency")
outfile.Close()


 ## EOF



