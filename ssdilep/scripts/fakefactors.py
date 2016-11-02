import os
import ROOT
from array import array


# -------------------------------------------------------------------------------------
# config
# -------------------------------------------------------------------------------------
indir     = "/coepp/cephfs/mel/fscutti/Analysis/ssdilep/scripts/FakesDir"
tag       = "Sherpa"
name      = "18SepSys"

# pt 
'''
var       = "mulead_pt"
new_bins = array('d', [0.,22.,23.,25.,28.,32.,36.,40.,45.,60.,200.])
'''

# eta
new_bins = array('d', [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5,])
var       = "mulead_eta"

infile    = "hists_"+var+"_FAKESFR%s_%s_"+tag+".root"
outfile   = "ff_"+var+"_"+name+"_"+tag+"_FR%s.root"
outmerged = "merged_ff_"+var+"_"+name+"_"+tag+".root"

# -------------------------------------------------------------------------------------


ROOT.gROOT.SetBatch(True)
rcol = [
   ROOT.kBlack,
   #ROOT.kBlue+1,
   ROOT.kRed,
   #ROOT.kRed+1, 
   #ROOT.kRed+2,
   #ROOT.kRed+3,
   #ROOT.kGreen,
   #ROOT.kGreen+1,
   ROOT.kGreen+2,
   #ROOT.kGreen+3,
   ROOT.kBlue,
   #ROOT.kBlue+1,
   #ROOT.kBlue+2,
   #ROOT.kBlue+3,
   #ROOT.kMagenta, 
   #ROOT.kMagenta+1,
   ROOT.kMagenta+2,
   #ROOT.kMagenta+3,
   ROOT.kYellow,
   ROOT.kYellow+1,
   #ROOT.kYellow+2,
   #ROOT.kYellow+3,
   ROOT.kOrange+7,
   ROOT.kCyan+1,
   ]

"""
c_all = ROOT.TCanvas("c_all_ff","c_all_ff",650,600)
c_all.SetTopMargin(0.05)
c_all.SetBottomMargin(0.13)
c_all.SetLeftMargin(0.13)
c_all.SetRightMargin(0.05)
c_all.SetTickx()
c_all.SetTicky()
"""

merged_ff_file = ROOT.TFile.Open(os.path.join(indir,outmerged),"UPDATE")

for i in xrange(1,9):
  num_file = ROOT.TFile.Open(os.path.join(indir,infile%(i,"NUM")),"READ")
  den_file = ROOT.TFile.Open(os.path.join(indir,infile%(i,"DEN")),"READ")

  h_num = num_file.Get("h_FAKESFR%s_NUM_nominal_fakes"%i).Clone()
  h_num.SetNameTitle("h_num","h_num")
  h_den = den_file.Get("h_FAKESFR%s_DEN_nominal_fakes"%i).Clone()
  h_den.SetNameTitle("h_den","h_den")

 
  h_new_num = h_num.Rebin(len(new_bins)-1,"h_new_num",new_bins)
  h_new_den = h_den.Rebin(len(new_bins)-1,"h_new_den",new_bins)
 
  h_ff = h_new_num.Clone()
  h_ff.Divide(h_new_den)
 
  h_ff.SetNameTitle("h_ff_FR%s"%i,"")
  h_ff.GetYaxis().SetTitle("Fake-factor")
  
  h_ff.GetYaxis().SetTitleSize(0.045)
  h_ff.GetXaxis().SetTitleSize(0.045)
  h_ff.GetYaxis().SetLabelSize(0.045)
  h_ff.GetXaxis().SetLabelSize(0.045)
  h_ff.GetYaxis().SetTitleOffset(1.2)
  h_ff.GetXaxis().SetTitleOffset(1.2)
  
  h_ff.GetXaxis().SetRangeUser(min(new_bins),max(new_bins))
  h_ff.SetLineColor(rcol[i-1])
  h_ff.SetMarkerColor(rcol[i-1])
  h_ff.SetMarkerSize(0.01)
  h_ff.SetMaximum(1.0)
  h_ff.SetMinimum(0)
  
  #c_all.cd()
  #if i==1: h_ff.Draw("E1 SAME")
  #else: h_ff.Draw("E1 SAME")
  
  c = ROOT.TCanvas("c_ff_FR%s"%i,"c_ff_FR%s"%i,650,600)
  c.SetTopMargin(0.05)
  c.SetBottomMargin(0.13)
  c.SetLeftMargin(0.13)
  c.SetRightMargin(0.05)
  c.SetTickx()
  c.SetTicky()
  c.cd() 
  
  h_ff.SetStats(0)
  h_ff.Draw("E1")
  
  merged_ff_file.WriteTObject(h_ff.Clone())
  merged_ff_file.WriteTObject(c.Clone())
  
  ff_file = ROOT.TFile.Open(os.path.join(indir,outfile%i),"RECREATE")
  ff_file.WriteTObject(h_ff.Clone())
  ff_file.WriteTObject(c.Clone())
 


