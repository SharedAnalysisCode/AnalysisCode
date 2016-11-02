import os
import ROOT
from array import array

ROOT.gROOT.SetBatch(True)

f_leadpt_ALTFAKES_TT    = ROOT.TFile.Open("plain_hists_leadpt_ALTFAKES_TT.root","READ")
f_subleadpt_ALTFAKES_TT = ROOT.TFile.Open("plain_hists_subleadpt_ALTFAKES_TT.root","READ")
f_leadpt_ALTFAKES_LL    = ROOT.TFile.Open("plain_hists_leadpt_ALTFAKES_LL.root","READ")
f_subleadpt_ALTFAKES_LL = ROOT.TFile.Open("plain_hists_subleadpt_ALTFAKES_LL.root","READ")
f_leadpt_ALTFAKES_TL    = ROOT.TFile.Open("plain_hists_leadpt_ALTFAKES_TL.root","READ")
f_subleadpt_ALTFAKES_TL = ROOT.TFile.Open("plain_hists_subleadpt_ALTFAKES_TL.root","READ")
f_leadpt_ALTFAKES_LT    = ROOT.TFile.Open("plain_hists_leadpt_ALTFAKES_LT.root","READ")
f_subleadpt_ALTFAKES_LT = ROOT.TFile.Open("plain_hists_subleadpt_ALTFAKES_LT.root","READ")

h_leadpt_ALTFAKES_TT     = f_leadpt_ALTFAKES_TT.Get("h_ALTFAKES_TT_nominal_fakes_cr").Clone()
h_subleadpt_ALTFAKES_TT  = f_subleadpt_ALTFAKES_TT.Get("h_ALTFAKES_TT_nominal_fakes_cr").Clone()
h_leadpt_ALTFAKES_LL     = f_leadpt_ALTFAKES_LL.Get("h_ALTFAKES_LL_nominal_fakes_cr").Clone()
h_subleadpt_ALTFAKES_LL  = f_subleadpt_ALTFAKES_LL.Get("h_ALTFAKES_LL_nominal_fakes_cr").Clone()
h_leadpt_ALTFAKES_TL     = f_leadpt_ALTFAKES_TL.Get("h_ALTFAKES_TL_nominal_fakes_cr").Clone()
h_subleadpt_ALTFAKES_TL  = f_subleadpt_ALTFAKES_TL.Get("h_ALTFAKES_TL_nominal_fakes_cr").Clone()
h_leadpt_ALTFAKES_LT     = f_leadpt_ALTFAKES_LT.Get("h_ALTFAKES_LT_nominal_fakes_cr").Clone()
h_subleadpt_ALTFAKES_LT  = f_subleadpt_ALTFAKES_LT.Get("h_ALTFAKES_LT_nominal_fakes_cr").Clone()

h_num = h_leadpt_ALTFAKES_TT.Clone()
h_num.SetNameTitle("h_num","h_num")
h_num.Add(h_subleadpt_ALTFAKES_TT)
h_num.Add(h_leadpt_ALTFAKES_TL)
h_num.Add(h_subleadpt_ALTFAKES_LT)


h_den = h_leadpt_ALTFAKES_LL.Clone()
h_den.SetNameTitle("h_den","h_den")
h_den.Add(h_subleadpt_ALTFAKES_LL)
h_den.Add(h_leadpt_ALTFAKES_LT)
h_den.Add(h_subleadpt_ALTFAKES_TL)

#new_bins = array('d', [22.,23.,24.,26.,28.,30.,34.,38.,45.,80.])
new_bins = array('d', [10.,12.,15.,20.,22.,25.,30.,35.,60.])

h_new_num = h_num.Rebin(8,"h_num",new_bins)
h_new_den = h_den.Rebin(8,"h_den",new_bins)

h_ff = h_new_num.Clone()
h_ff.Divide(h_new_den)

h_ff.SetNameTitle("h_ff","")
h_ff.GetYaxis().SetTitle("Fake-factor")
h_ff.GetYaxis().SetTitleOffset(1.1)
h_ff.GetXaxis().SetTitleOffset(1.1)
h_ff.GetXaxis().SetRangeUser(0.,60)
h_ff.SetMaximum(0.5)
h_ff.SetMinimum(0)

c = ROOT.TCanvas("c_ff","c_ff",650,600)
c.SetTopMargin(0.05)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.13)
c.SetRightMargin(0.05)
c.SetTickx()
c.SetTicky()

h_ff.Draw()

ff_file = ROOT.TFile.Open("hist_alt_ff.root","RECREATE")

ff_file.WriteTObject(h_ff)
ff_file.WriteTObject(c)



