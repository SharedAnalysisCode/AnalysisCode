## modules
import ROOT
from array import array

import histmgr
import funcs
import os
import re

ROOT.gStyle.SetPaintTextFormat("3.2f")

folder = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/HN_v060_SYS_root/"

MlljjMljj1_electron = ROOT.TFile(folder+"hists_MlljjMljj1_electron-SS-Z-SR_2D.root","READ")
MlljjMljj1_muon = ROOT.TFile(folder+"hists_MlljjMljj1_muon-SS-Z-SR_2D.root","READ")
MlljjMljj2_electron = ROOT.TFile(folder+"hists_MlljjMljj2_electron-SS-Z-SR_2D.root","READ")
MlljjMljj2_muon = ROOT.TFile(folder+"hists_MlljjMljj2_muon-SS-Z-SR_2D.root","READ")

for file in [MlljjMljj1_electron,MlljjMljj1_muon,MlljjMljj2_electron,MlljjMljj2_muon]:

  print file.GetName()

  data = file.Get("h_%s-SS-Z-SR_nominal_data" % ("muon" if "muon" in file.GetName() else "electron"))
  fakes = file.Get("h_%s-SS-Z-SR_nominal_fakes" % ("muon" if "muon" in file.GetName() else "electron"))
  Zjets = file.Get("h_%s-SS-Z-SR_nominal_SherpaDY221" % ("muon" if "muon" in file.GetName() else "electron"))
  diboson = file.Get("h_%s-SS-Z-SR_nominal_dibosonSherpa" % ("muon" if "muon" in file.GetName() else "electron"))
  top = file.Get("h_%s-SS-Z-SR_nominal_top_physics" % ("muon" if "muon" in file.GetName() else "electron"))

  print data,fakes,Zjets,diboson,top

  totMc = diboson.Clone("totMc"+os.path.basename(file.GetName()))
  totMc.Add(fakes)
  totMc.Add(top)
  if "electron" in file.GetName():
    totMc.Add(Zjets)

  totMc = totMc.Rebin2D(200,200,"totMc"+os.path.basename(file.GetName())+"rebinned")

  leg = ROOT.TLegend(0.18,0.62,0.3,0.7)
  leg.SetBorderSize(0)
  leg.SetFillColor(0)
  leg.SetFillStyle(0)
  leg.SetTextSize(0.045)
  leg.AddEntry(data,"#font[42]{Data}","p")


  canv = ROOT.TCanvas(os.path.basename(file.GetName()),os.path.basename(file.GetName()),800,600)
  canv.SetRightMargin(0.18)
  totMc.Draw("colz text e")
  data.Draw("same")
  if "Mljj1" in file.GetName():
    totMc.GetYaxis().SetTitle("m(l1jj) [GeV]")
  else:
    totMc.GetYaxis().SetTitle("m(l2jj) [GeV]")
  totMc.GetXaxis().SetTitle("m(lljj) [GeV]")
  totMc.GetXaxis().SetRangeUser(0,6000)
  totMc.GetYaxis().SetRangeUser(0,6000)
  totMc.GetZaxis().SetTitle("Events / (2 TeV #times 2 TeV)")
  totMc.SetMarkerSize(2)

  ROOT.ATLASLabel(0.18,0.9,"internal",1)
  ROOT.myText(0.18,0.84,1,"#sqrt{s}=13 TeV, 36.1 fb^{-1}")
  ROOT.myText(0.18,0.78,1,("e^{#pm}e^{#pm} SR" if "electron" in file.GetName() else "#mu^{#pm}#mu^{#pm} SR"))
  ROOT.myText(0.18,0.72,1,"stat. uncertainty only")
  leg.Draw()

  canv.Print("HN2D/"+os.path.basename(file.GetName())+".eps")
  canv.Print("HN2D/"+os.path.basename(file.GetName())+".pdf")
  

