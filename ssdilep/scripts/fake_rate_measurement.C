#include "Math/Minimizer.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "TRandom2.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "THStack.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TH2.h"
#include "TLegend.h"
#include "Fit/ParameterSettings.h"
#include <iostream>

void fake_rate_measurement(int rebin =1){
  
  TFile* nominal_t   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/Plots/hists_el_t_2D_pt_eta_FakeEnrichedRegion-nominal_FFnominal.root");
  TFile* nominal_l   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/Plots/hists_el_l_2D_pt_eta_FakeEnrichedRegion-nominal_FFnominal.root");
  TFile* nominal_sl  = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/Plots/hists_el_sl_2D_pt_eta_FakeEnrichedRegion-nominal_FFnominal.root");

  TH2F* nominal_t_wenu = (TH2F*) nominal_t->Get("h_FakeEnrichedRegion-nominal_nominal_WenuPowheg");
  TH2F* nominal_t_zee = (TH2F*) nominal_t->Get("h_FakeEnrichedRegion-nominal_nominal_ZeePowheg");
  TH2F* nominal_t_ttbar = (TH2F*) nominal_t->Get("h_FakeEnrichedRegion-nominal_nominal_ttbar_dilep");
  TH2F* nominal_t_diboson = (TH2F*) nominal_t->Get("h_FakeEnrichedRegion-nominal_nominal_diboson_sherpa");
  TH2F* nominal_t_singletop = (TH2F*) nominal_t->Get("h_FakeEnrichedRegion-nominal_nominal_singletop");
  TH2F* nominal_t_MC = (TH2F*) nominal_t_wenu->Clone("twenu");
  TH2F* nominal_t_data = (TH2F*) nominal_t->Get("h_FakeEnrichedRegion-nominal_nominal_data");
  TH2F* nominal_t_data_minus = (TH2F*) nominal_t_data->Clone("tdata");

  TH2F* nominal_l_wenu = (TH2F*) nominal_l->Get("h_FakeEnrichedRegion-nominal_nominal_WenuPowheg");
  TH2F* nominal_l_zee = (TH2F*) nominal_l->Get("h_FakeEnrichedRegion-nominal_nominal_ZeePowheg");
  TH2F* nominal_l_ttbar = (TH2F*) nominal_l->Get("h_FakeEnrichedRegion-nominal_nominal_ttbar_dilep");
  TH2F* nominal_l_diboson = (TH2F*) nominal_l->Get("h_FakeEnrichedRegion-nominal_nominal_diboson_sherpa");
  TH2F* nominal_l_singletop = (TH2F*) nominal_l->Get("h_FakeEnrichedRegion-nominal_nominal_singletop");
  TH2F* nominal_l_MC = (TH2F*) nominal_l_wenu->Clone("lwenu");
  TH2F* nominal_l_data = (TH2F*) nominal_l->Get("h_FakeEnrichedRegion-nominal_nominal_data");
  TH2F* nominal_l_data_minus = (TH2F*) nominal_l_data->Clone("ldata");

  TH2F* nominal_sl_wenu = (TH2F*) nominal_sl->Get("h_FakeEnrichedRegion-nominal_nominal_WenuPowheg");
  TH2F* nominal_sl_zee = (TH2F*) nominal_sl->Get("h_FakeEnrichedRegion-nominal_nominal_ZeePowheg");
  TH2F* nominal_sl_ttbar = (TH2F*) nominal_sl->Get("h_FakeEnrichedRegion-nominal_nominal_ttbar_dilep");
  TH2F* nominal_sl_diboson = (TH2F*) nominal_sl->Get("h_FakeEnrichedRegion-nominal_nominal_diboson_sherpa");
  TH2F* nominal_sl_singletop = (TH2F*) nominal_sl->Get("h_FakeEnrichedRegion-nominal_nominal_singletop");
  TH2F* nominal_sl_MC = (TH2F*) nominal_sl_wenu->Clone("slwenu");
  TH2F* nominal_sl_data = (TH2F*) nominal_sl->Get("h_FakeEnrichedRegion-nominal_nominal_data");
  TH2F* nominal_sl_data_minus = (TH2F*) nominal_sl_data->Clone("sldata");

  nominal_t_MC->Add(nominal_t_zee);
  nominal_t_MC->Add(nominal_t_ttbar);
  nominal_t_MC->Add(nominal_t_diboson);
  nominal_t_MC->Add(nominal_t_singletop);
  nominal_t_data_minus->Add(nominal_t_MC,-1.);

  nominal_l_MC->Add(nominal_l_zee);
  nominal_l_MC->Add(nominal_l_ttbar);
  nominal_l_MC->Add(nominal_l_diboson);
  nominal_l_MC->Add(nominal_l_singletop);
  nominal_l_data_minus->Add(nominal_t_MC,-1.);

  nominal_sl_MC->Add(nominal_sl_zee);
  nominal_sl_MC->Add(nominal_sl_ttbar);
  nominal_sl_MC->Add(nominal_sl_diboson);
  nominal_sl_MC->Add(nominal_sl_singletop);
  nominal_sl_data_minus->Add(nominal_sl_MC,-1.);

  TH2F* nominal_data_rate = (TH2F*) nominal_t_data_minus->Clone("clone1");
  nominal_data_rate->Divide(nominal_l_data_minus);

  TH2F* nominal_data_rateFF = (TH2F*) nominal_t_data_minus->Clone("clone2");
  nominal_data_rateFF->Divide(nominal_sl_data_minus);

  TEfficiency* eff = new TEfficiency(*nominal_t_data_minus, *nominal_l_data_minus);
  TH2F* nominal_data_rate_eff = (TH2F*) nominal_data_rate->Clone();
  for (int i = 1; i <= nominal_data_rate->GetNbinsX(); i++ ){
    for (int j = 1; j <= nominal_data_rate->GetNbinsY(); j++ ){
      nominal_data_rate_eff->SetBinContent(i,j,eff->GetEfficiency(eff->GetGlobalBin(i,j)));
      nominal_data_rate_eff->SetBinError(i,j,eff->GetEfficiencyErrorUp(eff->GetGlobalBin(i,j)));
    }
  }

  // fake rate
  TH1D* projX1 = nominal_data_rate_eff->ProjectionX("proj1",1,1);
  TH1D* projX3 = nominal_data_rate_eff->ProjectionX("proj3",3,3);
  projX3->SetLineColor(kRed);
  projX3->SetMarkerColor(kRed);
  TH1D* projX4 = nominal_data_rate_eff->ProjectionX("proj4",4,4);
  projX4->SetLineColor(kBlue);
  projX4->SetMarkerColor(kBlue);

  // fake factor
  TH1D* projX1FF = (TH1D*) projX1->Clone();
  TH1D* projX3FF = (TH1D*) projX3->Clone();
  TH1D* projX4FF = (TH1D*) projX4->Clone();
  for (int i = 1; i <= projX1->GetNbinsX(); i++){
    projX1FF->SetBinContent( i, projX1->GetBinContent(i)/(1-projX1->GetBinContent(i)) );
    projX1FF->SetBinError  ( i, projX1->GetBinError(i)/pow(1-projX1->GetBinContent(i),2) );
    projX3FF->SetBinContent( i, projX3->GetBinContent(i)/(1-projX3->GetBinContent(i)) );
    projX3FF->SetBinError  ( i, projX3->GetBinError(i)/pow(1-projX3->GetBinContent(i),2) );
    projX4FF->SetBinContent( i, projX4->GetBinContent(i)/(1-projX4->GetBinContent(i)) );
    projX4FF->SetBinError  ( i, projX4->GetBinError(i)/pow(1-projX4->GetBinContent(i),2) );
  }

  // fake factor direct
  TH1D* projX1ff = nominal_data_rateFF->ProjectionX("proj1ff",1,1);
  TH1D* projX3ff = nominal_data_rateFF->ProjectionX("proj3ff",3,3);
  projX3ff->SetLineColor(kRed);
  projX3ff->SetMarkerColor(kRed);
  TH1D* projX4ff = nominal_data_rateFF->ProjectionX("proj4ff",4,4);
  projX4ff->SetLineColor(kBlue);
  projX4ff->SetMarkerColor(kBlue);

  leg = TLegend(0.5,0.2,0.9,0.4);
  leg.SetBorderSize(0);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetTextSize(0.045);
  leg.AddEntry(projX1,"0 < |#eta| < 1.37","pe0");
  leg.AddEntry(projX3,"1.52 < |#eta| < 2.01","pe0");
  leg.AddEntry(projX4,"2.01 < |#eta| < 2.47","pe0");

  TFile* outFile = new TFile("fakeRate.root","RECREATE");
  nominal_data_rate->SetName("fakeRateDivide");
  nominal_data_rate_eff->SetName("fakeRateEff");
  nominal_data_rate->Write();
  nominal_data_rate_eff->Write();
  outFile->Close();

  TCanvas c1("c1","c1",800,600);
  c1.SetLogx();
  c1.SetRightMargin(0.1);
  nominal_data_rate->Draw("colz text e");
  nominal_data_rate->SetMarkerSize(0.6);
  nominal_data_rate->GetXaxis()->SetMoreLogLabels();
  nominal_data_rate->GetXaxis()->SetNoExponent();

  TCanvas c2("c2","c2",600,600);
  c2.SetLogx();
  projX1->GetYaxis()->SetRangeUser(0,1.1);
  projX1->GetXaxis()->SetNoExponent();
  projX1->GetXaxis()->SetMoreLogLabels();
  projX1->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1->GetYaxis()->SetTitle("fake rate");
  projX1->Draw("pe0");
  projX3->Draw("same");
  projX4->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);

  TCanvas c3("c3","c3",600,600);
  c3.SetLogx();
  projX1FF->GetXaxis()->SetNoExponent();
  projX1FF->GetXaxis()->SetMoreLogLabels();
  projX1FF->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1FF->GetYaxis()->SetTitle("fake factor");
  projX1FF->Draw("pe0");
  projX1FF->GetYaxis()->SetRangeUser(0,9.);
  projX3FF->Draw("same");
  projX4FF->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);

  TCanvas c4("c4","c4",600,600);
  c4.SetLogx();
  projX1ff->GetXaxis()->SetRangeUser(0,3.5);
  projX1ff->GetXaxis()->SetNoExponent();
  projX1ff->GetXaxis()->SetMoreLogLabels();
  projX1ff->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1ff->GetYaxis()->SetTitle("fake factor");
  projX1ff->Draw("pe0");
  projX1ff->GetYaxis()->SetRangeUser(0,9.);
  projX3ff->Draw("same");
  projX4ff->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);

  c1.Print("fakeRate2D.eps");
  c2.Print("fakeRate.eps");
  c3.Print("fakeFactor.eps");
  c4.Print("fakeFactorDirect.eps");

  
}