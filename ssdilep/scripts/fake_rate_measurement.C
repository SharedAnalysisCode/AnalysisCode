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

void fake_rate_measurement_helper(std::string var = "nominal"){
  
  double mcscale = 1.0;
  if (var=="mcup") mcscale = 1.10;
  else if (var=="mcdn") mcscale = 0.90;

  std::string var2 = var;
  if (var=="mcup") var2 = "nominal";
  else if (var=="mcdn") var2 = "nominal";

  
  TFile* nominal_t   = new TFile(("/afs/f9.ijs.si/home/miham/AnalysisCode/run/FFelectron36_3/hists_el_t_2D_pt_eta_FakeEnrichedRegion-" + var2 + "_FFnominal.root").c_str());
  TFile* nominal_l   = new TFile(("/afs/f9.ijs.si/home/miham/AnalysisCode/run/FFelectron36_3/hists_el_l_2D_pt_eta_FakeEnrichedRegion-" + var2 + "_FFnominal.root").c_str());
  TFile* nominal_sl  = new TFile(("/afs/f9.ijs.si/home/miham/AnalysisCode/run/FFelectron36_3/hists_el_sl_2D_pt_eta_FakeEnrichedRegion-" + var2 + "_FFnominal.root").c_str());

  TH2F* nominal_t_wenu = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_WenuPowheg").c_str());
  TH2F* nominal_t_zee = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ZeePowheg").c_str());
  TH2F* nominal_t_ttbar = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ttbar_dilep").c_str());
  TH2F* nominal_t_diboson = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_diboson_sherpa").c_str());
  TH2F* nominal_t_singletop = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_singletop").c_str());
  TH2F* nominal_t_MC = (TH2F*) nominal_t_wenu->Clone("twenu");
  TH2F* nominal_t_data = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_data").c_str());
  TH2F* nominal_t_data_minus = (TH2F*) nominal_t_data->Clone("tdata");

  TH2F* nominal_l_wenu = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_WenuPowheg").c_str());
  TH2F* nominal_l_zee = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ZeePowheg").c_str());
  TH2F* nominal_l_ttbar = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ttbar_dilep").c_str());
  TH2F* nominal_l_diboson = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_diboson_sherpa").c_str());
  TH2F* nominal_l_singletop = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_singletop").c_str());
  TH2F* nominal_l_MC = (TH2F*) nominal_l_wenu->Clone("lwenu");
  TH2F* nominal_l_data = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_data").c_str());
  TH2F* nominal_l_data_minus = (TH2F*) nominal_l_data->Clone("ldata");

  TH2F* nominal_sl_wenu = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_WenuPowheg").c_str());
  TH2F* nominal_sl_zee = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ZeePowheg").c_str());
  TH2F* nominal_sl_ttbar = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ttbar_dilep").c_str());
  TH2F* nominal_sl_diboson = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_diboson_sherpa").c_str());
  TH2F* nominal_sl_singletop = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_singletop").c_str());
  TH2F* nominal_sl_MC = (TH2F*) nominal_sl_wenu->Clone("slwenu");
  TH2F* nominal_sl_data = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_data").c_str());
  TH2F* nominal_sl_data_minus = (TH2F*) nominal_sl_data->Clone("sldata");

  nominal_t_MC->Add(nominal_t_zee);
  nominal_t_MC->Add(nominal_t_ttbar);
  nominal_t_MC->Add(nominal_t_diboson);
  nominal_t_MC->Add(nominal_t_singletop);
  nominal_t_data_minus->Add(nominal_t_MC,-1.*mcscale);

  nominal_l_MC->Add(nominal_l_zee);
  nominal_l_MC->Add(nominal_l_ttbar);
  nominal_l_MC->Add(nominal_l_diboson);
  nominal_l_MC->Add(nominal_l_singletop);
  nominal_l_data_minus->Add(nominal_t_MC,-1.*mcscale);

  nominal_sl_MC->Add(nominal_sl_zee);
  nominal_sl_MC->Add(nominal_sl_ttbar);
  nominal_sl_MC->Add(nominal_sl_diboson);
  nominal_sl_MC->Add(nominal_sl_singletop);
  nominal_sl_data_minus->Add(nominal_sl_MC,-1.*mcscale);

  TH2F* nominal_data_rate = (TH2F*) nominal_t_data_minus->Clone("clone1");
  nominal_data_rate->Divide(nominal_l_data_minus);

  TH2F* nominal_data_rateFF = (TH2F*) nominal_t_data_minus->Clone(("fakeFactorDirect-"+var+"").c_str());
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

  TH2F* nominal_data_factor_eff = (TH2F*) nominal_data_rate->Clone(("fakeFactor-"+var+"").c_str());
  for (int i = 1; i <= nominal_data_rate->GetNbinsX(); i++ ){
    for (int j = 1; j <= nominal_data_rate->GetNbinsY(); j++ ){
      nominal_data_factor_eff->SetBinContent(i,j,nominal_data_rate_eff->GetBinContent(i,j)/(1-nominal_data_rate_eff->GetBinContent(i,j)));
      nominal_data_factor_eff->SetBinError(i,j,nominal_data_rate_eff->GetBinError(i,j)/pow(1-nominal_data_rate_eff->GetBinContent(i,j),2));
    }
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

  TFile* outFile = new TFile(("fakeRate-"+var+".root").c_str(),"RECREATE");
  nominal_data_rate->SetName(("fakeRateDivide-"+var+"").c_str());
  nominal_data_rate_eff->SetName(("fakeRate-"+var+"").c_str());
  //nominal_data_rate->Write();
  nominal_data_rate_eff->Write();
  nominal_data_rateFF->Write();
  nominal_data_factor_eff->Write();
  outFile->Close();

  TCanvas c1("c1","c1",800,600);
  c1.SetLogx();
  c1.SetRightMargin(0.1);
  nominal_data_rate_eff->Draw("colz text e");
  nominal_data_rate_eff->SetMarkerSize(0.6);
  nominal_data_rate_eff->GetXaxis()->SetMoreLogLabels();
  nominal_data_rate_eff->GetXaxis()->SetNoExponent();

  TCanvas c2("c2","c2",600,600);
  c2.SetLogx();
  projX1->GetYaxis()->SetRangeUser(0,0.5);
  projX1->GetXaxis()->SetNoExponent();
  projX1->GetXaxis()->SetMoreLogLabels();
  projX1->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1->GetYaxis()->SetTitle("fake rate");
  projX1->Draw("pe0");
  projX3->Draw("same");
  projX4->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);
  myText(0.18,0.84,1,"fake rate ( T/L )");

  TCanvas c3("c3","c3",600,600);
  c3.SetLogx();
  projX1FF->GetXaxis()->SetNoExponent();
  projX1FF->GetXaxis()->SetMoreLogLabels();
  projX1FF->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1FF->GetYaxis()->SetTitle("fake factor");
  projX1FF->Draw("pe0");
  projX1FF->GetYaxis()->SetRangeUser(0,1.0);
  projX3FF->Draw("same");
  projX4FF->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);
  myText(0.18,0.84,1,"fake factor ( f/(1-f) )");

  TCanvas c4("c4","c4",600,600);
  c4.SetLogx();
  projX1ff->GetYaxis()->SetRangeUser(0,1.0);
  projX1ff->GetXaxis()->SetNoExponent();
  projX1ff->GetXaxis()->SetMoreLogLabels();
  projX1ff->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1ff->GetYaxis()->SetTitle("fake factor");
  projX1ff->Draw("pe0");
  projX1ff->GetYaxis()->SetRangeUser(0,1.);
  projX3ff->Draw("same");
  projX4ff->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);
  myText(0.18,0.84,1,"fake factor ( T/SL )");

  c1.Print(("fakeRate2D-"+var+".eps").c_str());
  c2.Print(("fakeRate-"+var+".eps").c_str());
  c3.Print(("fakeFactor-"+var+".eps").c_str());
  c4.Print(("fakeFactorDirect-"+var+".eps").c_str());

  
}

void fake_rate_measurement(){

  fake_rate_measurement_helper("nominal");
  fake_rate_measurement_helper("MET60");
  fake_rate_measurement_helper("ASjet");
  fake_rate_measurement_helper("mcup");
  fake_rate_measurement_helper("mcdn");

  TFile* nominalFile = new TFile("fakeRate-nominal.root","READ");
  TFile* MET60File = new TFile("fakeRate-MET60.root","READ");
  TFile* ASjetFile = new TFile("fakeRate-ASjet.root","READ");
  TFile* mcupfile = new TFile("fakeRate-mcup.root","READ");
  TFile* mcdnfile = new TFile("fakeRate-mcdn.root","READ");

  TH2F* fr1 = (TH2F*) nominalFile->Get("fakeFactor-nominal");
  TH2F* fr2 = (TH2F*) MET60File->Get("fakeFactor-MET60");
  TH2F* fr3 = (TH2F*) ASjetFile->Get("fakeFactor-ASjet");
  TH2F* fr4 = (TH2F*) mcupfile->Get("fakeFactor-mcup");
  TH2F* fr5 = (TH2F*) mcdnfile->Get("fakeFactor-mcdn");

  TH1D* temp1 = new TH1D();
  TH1D* temp2 = new TH1D();
  temp2->SetMarkerColor(kRed);
  temp2->SetLineColor(kRed);
  TH1D* temp3 = new TH1D();
  temp3->SetMarkerColor(kBlue);
  temp3->SetLineColor(kBlue);
  TH1D* temp4 = new TH1D();
  temp4->SetMarkerStyle(22);
  TH1D* temp5 = new TH1D();
  temp5->SetMarkerStyle(23);
  TGraphAsymmErrors* temp6 = new TGraphAsymmErrors();
  temp6->SetFillColor(kYellow);
  temp6->SetLineColor(kYellow);

  leg = TLegend(0.18,0.45,0.4,0.75);
  leg.SetBorderSize(0);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetTextSize(0.045);
  leg.AddEntry(temp1,"#font[42]{nominal}","pe0");
  leg.AddEntry(temp2,"#font[42]{MET < 60}","pe0");
  leg.AddEntry(temp3,"#font[42]{away side jet}","pe0");
  leg.AddEntry(temp4,"#font[42]{MC up 10%}","pe0");
  leg.AddEntry(temp5,"#font[42]{MC down 10%}","pe0");
  leg.AddEntry(temp6,"#font[42]{Final Sys. Unc.}","f");

  TCanvas c1("c1","c1",600,600);
  pad_1 = new TPad("c1up", "c1up", 0., 0.299, 1., 1.);
  pad_1->SetBottomMargin(0.03);
  pad_1->SetTopMargin(0.08);
  pad_1->Draw();

  pad_2 = new TPad("c1dn", "c1dn", 0.0, 0.0, 1.0, 0.301);
  pad_2->SetTopMargin(0.03);
  pad_2->SetBottomMargin(0.35);
  pad_2->SetGridy();
  pad_2->Draw();

  TH1D* proj1nom = fr1->ProjectionX("proj1nom",1,1);
  TH1D* proj1M60 = fr2->ProjectionX("proj1M60",1,1);
  TH1D* proj1asj = fr3->ProjectionX("proj1asj",1,1);
  TH1D* proj1up = fr4->ProjectionX("proj1up",1,1);
  TH1D* proj1dn = fr5->ProjectionX("proj1dn",1,1);
  proj1M60->SetLineWidth(0);
  proj1up->SetLineWidth(0);
  proj1dn->SetLineWidth(0);
  proj1asj->SetLineWidth(0);

  TH1D* proj1StatErrUp = (TH1D*) proj1nom->Clone();
  TH1D* proj1StatErrDn = (TH1D*) proj1nom->Clone();
  for (int i = 1; i <= proj1nom->GetNbinsX(); i++){
    proj1StatErrUp->SetBinContent(i,proj1nom->GetBinContent(i)+proj1nom->GetBinError(i));
    proj1StatErrDn->SetBinContent(i,proj1nom->GetBinContent(i)-proj1nom->GetBinError(i));
  }
  TGraphErrors*  proj1StatGr =  TH1TOTGraph(proj1nom);
  TGraphErrors*  proj1StatErrUpGr =  TH1TOTGraph(proj1StatErrUp);
  TGraphErrors*  proj1StatErrDnGr =  TH1TOTGraph(proj1StatErrDn);
  TGraphErrors*  proj1M60ErrGr =  TH1TOTGraph(proj1M60);
  TGraphErrors*  proj1asjErrGr =  TH1TOTGraph(proj1asj);
  TGraphErrors*  proj1upErrGr =  TH1TOTGraph(proj1up);
  TGraphErrors*  proj1dnErrGr =  TH1TOTGraph(proj1dn);

  TGraphAsymmErrors* proj1ErrBand = myMakeBand(proj1StatGr, proj1StatErrUpGr, proj1StatErrDnGr);
  myAddtoBand(proj1M60ErrGr, proj1ErrBand);
  myAddtoBand(proj1asjErrGr, proj1ErrBand);
  myAddtoBand(proj1upErrGr, proj1ErrBand);
  myAddtoBand(proj1dnErrGr, proj1ErrBand);

  TGraphAsymmErrors* proj1ErrBandRatio = (TGraphAsymmErrors*) proj1ErrBand->Clone();
  proj1ErrBandRatio->SetFillColor(kYellow);

  for (int i=0;i<proj1ErrBandRatio->GetN();i++) {
    proj1ErrBandRatio->GetY()[i] *= 1./proj1nom->GetBinContent(i+1);
    proj1ErrBandRatio->GetEYhigh()[i] *= 1./proj1nom->GetBinContent(i+1);
    proj1ErrBandRatio->GetEYlow()[i] *= 1./proj1nom->GetBinContent(i+1);
  }

  pad_1->SetLogx();
  pad_1->cd();
  proj1M60->SetMarkerColor(kRed);
  proj1M60->SetLineColor(kRed);
  proj1asj->SetMarkerColor(kBlue);
  proj1asj->SetLineColor(kBlue);
  proj1up->SetMarkerStyle(22);
  proj1dn->SetMarkerStyle(23);
  proj1nom->SetMarkerSize(0.8);
  proj1asj->SetMarkerSize(0.8);
  proj1M60->SetMarkerSize(0.8);
  proj1up->SetMarkerSize(0.8);
  proj1dn->SetMarkerSize(0.8);
  proj1nom->Draw("P E");
  proj1ErrBand->SetFillColor(kYellow);
  proj1ErrBand->Draw("same E3");
  proj1nom->GetYaxis()->SetTitle("fake factor");
  proj1nom->GetXaxis()->SetLabelSize(0);
  proj1nom->GetYaxis()->SetLabelSize(0.06);
  proj1nom->GetYaxis()->SetNdivisions(515);
  proj1nom->GetYaxis()->SetTitleSize(0.07);
  proj1nom->GetYaxis()->SetTitleOffset(0.95);
  proj1nom->GetYaxis()->SetRangeUser(0.1,0.7);
  proj1nom->GetXaxis()->SetLabelSize(0);
  proj1up->Draw("same P E X0");
  proj1dn->Draw("same P E X0");
  proj1M60->Draw("same P E X0");
  proj1asj->Draw("same P E X0");
  proj1nom->Draw("same P E");
  ATLASLabel(0.18,0.85,"Internal",1);
  myText(0.18,0.79,1,"0.0 < |#eta| < 1.37");
  leg.Draw();
  pad_2->SetLogx();
  pad_2->cd();
  TH1D* proj1M60r = (TH1D*) proj1M60->Clone(); proj1M60r->Divide(proj1nom);
  TH1D* proj1upr = (TH1D*) proj1up->Clone(); proj1upr->Divide(proj1nom);
  TH1D* proj1dnr = (TH1D*) proj1dn->Clone(); proj1dnr->Divide(proj1nom);
  TH1D* proj1asjr = (TH1D*) proj1asj->Clone(); proj1asjr->Divide(proj1nom);
  proj1M60r->SetLineWidth(0);
  proj1upr->SetLineWidth(0);
  proj1dnr->SetLineWidth(0);
  proj1asjr->SetLineWidth(0);
  proj1M60r->Draw("PE0X0");
  proj1ErrBandRatio->Draw("E3");
  proj1M60r->Draw("same PE0X0");
  proj1upr->Draw("same PE0X0");
  proj1dnr->Draw("same PE0X0");
  proj1asjr->Draw("same PE0X0");
  proj1M60r->GetXaxis()->SetLabelSize(0.15);
  proj1M60r->GetYaxis()->SetLabelSize(0.13);
  proj1M60r->GetYaxis()->SetDecimals();
  proj1M60r->GetXaxis()->SetTitle("p_{T} [GeV]");
  proj1M60r->GetYaxis()->SetTitle("ratio");
  proj1M60r->GetXaxis()->SetTitleSize(0.15);
  proj1M60r->GetXaxis()->SetTitleOffset(1.0);
  proj1M60r->GetYaxis()->SetTitleSize(0.15);
  proj1M60r->GetYaxis()->SetTitleOffset(0.40);
  proj1M60r->GetYaxis()->SetRangeUser(0.5,1.5);
  proj1M60r->GetYaxis()->SetNdivisions(106);
  proj1M60r->GetXaxis()->SetNoExponent();
  proj1M60r->GetXaxis()->SetMoreLogLabels();
  proj1M60r->SetMarkerSize(0.8);
  proj1upr->SetMarkerSize(0.8);
  proj1dnr->SetMarkerSize(0.8);
  proj1asjr->SetMarkerSize(0.8);
  gPad->RedrawAxis("g");
  c1.Print("fakeProjSys1.eps");

  TCanvas c2("c2","c2",600,600);
  pad_1 = new TPad("c2up", "c2up", 0., 0.299, 1., 1.);
  pad_1->SetBottomMargin(0.03);
  pad_1->SetTopMargin(0.08);
  pad_1->Draw();

  pad_2 = new TPad("c2dn", "c2dn", 0.0, 0.0, 1.0, 0.301);
  pad_2->SetTopMargin(0.03);
  pad_2->SetBottomMargin(0.35);
  pad_2->SetGridy();
  pad_2->Draw();

  TH1D* proj3nom = fr1->ProjectionX("proj3nom",3,3);
  TH1D* proj3M60 = fr2->ProjectionX("proj3M60",3,3);
  TH1D* proj3asj = fr3->ProjectionX("proj3asj",3,3);
  TH1D* proj3up = fr4->ProjectionX("proj3up",3,3);
  TH1D* proj3dn = fr5->ProjectionX("proj3dn",3,3);
  proj3M60->SetLineWidth(0);
  proj3up->SetLineWidth(0);
  proj3dn->SetLineWidth(0);
  proj3asj->SetLineWidth(0);

  TH1D* proj3StatErrUp = (TH1D*) proj3nom->Clone();
  TH1D* proj3StatErrDn = (TH1D*) proj3nom->Clone();
  for (int i = 1; i <= proj3nom->GetNbinsX(); i++){
    proj3StatErrUp->SetBinContent(i,proj3nom->GetBinContent(i)+proj3nom->GetBinError(i));
    proj3StatErrDn->SetBinContent(i,proj3nom->GetBinContent(i)-proj3nom->GetBinError(i));
  }
  TGraphErrors*  proj3StatGr =  TH1TOTGraph(proj3nom);
  TGraphErrors*  proj3StatErrUpGr =  TH1TOTGraph(proj3StatErrUp);
  TGraphErrors*  proj3StatErrDnGr =  TH1TOTGraph(proj3StatErrDn);
  TGraphErrors*  proj3M60ErrGr =  TH1TOTGraph(proj3M60);
  TGraphErrors*  proj3asjErrGr =  TH1TOTGraph(proj3asj);
  TGraphErrors*  proj3upErrGr =  TH1TOTGraph(proj3up);
  TGraphErrors*  proj3dnErrGr =  TH1TOTGraph(proj3dn);

  TGraphAsymmErrors* proj3ErrBand = myMakeBand(proj3StatGr, proj3StatErrUpGr, proj3StatErrDnGr);
  myAddtoBand(proj3M60ErrGr, proj3ErrBand);
  myAddtoBand(proj3asjErrGr, proj3ErrBand);
  myAddtoBand(proj3upErrGr, proj3ErrBand);
  myAddtoBand(proj3dnErrGr, proj3ErrBand);

  TGraphAsymmErrors* proj3ErrBandRatio = (TGraphAsymmErrors*) proj3ErrBand->Clone();
  proj3ErrBandRatio->SetFillColor(kYellow);

  for (int i=0;i<proj3ErrBandRatio->GetN();i++) {
    proj3ErrBandRatio->GetY()[i] *= 1./proj3nom->GetBinContent(i+1);
    proj3ErrBandRatio->GetEYhigh()[i] *= 1./proj3nom->GetBinContent(i+1);
    proj3ErrBandRatio->GetEYlow()[i] *= 1./proj3nom->GetBinContent(i+1);
  }

  pad_1->SetLogx();
  pad_1->cd();
  proj3M60->SetMarkerColor(kRed);
  proj3M60->SetLineColor(kRed);
  proj3asj->SetMarkerColor(kBlue);
  proj3asj->SetLineColor(kBlue);
  proj3up->SetMarkerStyle(22);
  proj3dn->SetMarkerStyle(23);
  proj3nom->SetMarkerSize(0.8);
  proj3asj->SetMarkerSize(0.8);
  proj3M60->SetMarkerSize(0.8);
  proj3up->SetMarkerSize(0.8);
  proj3dn->SetMarkerSize(0.8);
  proj3nom->Draw("P E");
  proj3ErrBand->SetFillColor(kYellow);
  proj3ErrBand->Draw("same E3");
  proj3nom->GetYaxis()->SetTitle("fake factor");
  proj3nom->GetXaxis()->SetLabelSize(0);
  proj3nom->GetYaxis()->SetLabelSize(0.06);
  proj3nom->GetYaxis()->SetNdivisions(515);
  proj3nom->GetYaxis()->SetTitleSize(0.07);
  proj3nom->GetYaxis()->SetTitleOffset(0.95);
  proj3nom->GetYaxis()->SetRangeUser(0.1,0.7);
  proj3nom->GetXaxis()->SetLabelSize(0);
  proj3up->Draw("same P E X0");
  proj3dn->Draw("same P E X0");
  proj3M60->Draw("same P E X0");
  proj3asj->Draw("same P E X0");
  proj3nom->Draw("same P E");
  ATLASLabel(0.18,0.85,"Internal",1);
  myText(0.18,0.79,1,"1.52 < |#eta| < 2.01");
  leg.Draw();
  pad_2->SetLogx();
  pad_2->cd();
  TH1D* proj3M60r = (TH1D*) proj3M60->Clone(); proj3M60r->Divide(proj3nom);
  TH1D* proj3upr = (TH1D*) proj3up->Clone(); proj3upr->Divide(proj3nom);
  TH1D* proj3dnr = (TH1D*) proj3dn->Clone(); proj3dnr->Divide(proj3nom);
  TH1D* proj3asjr = (TH1D*) proj3asj->Clone(); proj3asjr->Divide(proj3nom);
  proj3M60r->SetLineWidth(0);
  proj3upr->SetLineWidth(0);
  proj3dnr->SetLineWidth(0);
  proj3asjr->SetLineWidth(0);
  proj3M60r->Draw("PE0X0");
  proj3ErrBandRatio->Draw("E3");
  proj3M60r->Draw("same PE0X0");
  proj3upr->Draw("same PE0X0");
  proj3dnr->Draw("same PE0X0");
  proj3asjr->Draw("same PE0X0");
  proj3M60r->GetXaxis()->SetLabelSize(0.15);
  proj3M60r->GetYaxis()->SetLabelSize(0.13);
  proj3M60r->GetYaxis()->SetDecimals();
  proj3M60r->GetXaxis()->SetTitle("p_{T} [GeV]");
  proj3M60r->GetYaxis()->SetTitle("ratio");
  proj3M60r->GetXaxis()->SetTitleSize(0.15);
  proj3M60r->GetXaxis()->SetTitleOffset(1.0);
  proj3M60r->GetYaxis()->SetTitleSize(0.15);
  proj3M60r->GetYaxis()->SetTitleOffset(0.40);
  proj3M60r->GetYaxis()->SetRangeUser(0.5,1.5);
  proj3M60r->GetYaxis()->SetNdivisions(106);
  proj3M60r->GetXaxis()->SetNoExponent();
  proj3M60r->GetXaxis()->SetMoreLogLabels();
  proj3M60r->SetMarkerSize(0.8);
  proj3upr->SetMarkerSize(0.8);
  proj3dnr->SetMarkerSize(0.8);
  proj3asjr->SetMarkerSize(0.8);
  gPad->RedrawAxis("g");
  c2.Print("fakeProjSys3.eps");


  TCanvas c3("c3","c3",600,600);
  pad_1 = new TPad("c3up", "c3up", 0., 0.299, 1., 1.);
  pad_1->SetBottomMargin(0.03);
  pad_1->SetTopMargin(0.08);
  pad_1->Draw();

  pad_2 = new TPad("c3dn", "c3dn", 0.0, 0.0, 1.0, 0.301);
  pad_2->SetTopMargin(0.03);
  pad_2->SetBottomMargin(0.35);
  pad_2->SetGridy();
  pad_2->Draw();

  TH1D* proj4nom = fr1->ProjectionX("proj4nom",4,4);
  TH1D* proj4M60 = fr2->ProjectionX("proj4M60",4,4);
  TH1D* proj4asj = fr3->ProjectionX("proj4asj",4,4);
  TH1D* proj4up = fr4->ProjectionX("proj4up",4,4);
  TH1D* proj4dn = fr5->ProjectionX("proj4dn",4,4);
  proj4M60->SetLineWidth(0);
  proj4up->SetLineWidth(0);
  proj4dn->SetLineWidth(0);
  proj4asj->SetLineWidth(0);

  TH1D* proj4StatErrUp = (TH1D*) proj4nom->Clone();
  TH1D* proj4StatErrDn = (TH1D*) proj4nom->Clone();
  for (int i = 1; i <= proj4nom->GetNbinsX(); i++){
    proj4StatErrUp->SetBinContent(i,proj4nom->GetBinContent(i)+proj4nom->GetBinError(i));
    proj4StatErrDn->SetBinContent(i,proj4nom->GetBinContent(i)-proj4nom->GetBinError(i));
  }
  TGraphErrors*  proj4StatGr =  TH1TOTGraph(proj4nom);
  TGraphErrors*  proj4StatErrUpGr =  TH1TOTGraph(proj4StatErrUp);
  TGraphErrors*  proj4StatErrDnGr =  TH1TOTGraph(proj4StatErrDn);
  TGraphErrors*  proj4M60ErrGr =  TH1TOTGraph(proj4M60);
  TGraphErrors*  proj4asjErrGr =  TH1TOTGraph(proj4asj);
  TGraphErrors*  proj4upErrGr =  TH1TOTGraph(proj4up);
  TGraphErrors*  proj4dnErrGr =  TH1TOTGraph(proj4dn);

  TGraphAsymmErrors* proj4ErrBand = myMakeBand(proj4StatGr, proj4StatErrUpGr, proj4StatErrDnGr);
  myAddtoBand(proj4M60ErrGr, proj4ErrBand);
  myAddtoBand(proj4asjErrGr, proj4ErrBand);
  myAddtoBand(proj4upErrGr, proj4ErrBand);
  myAddtoBand(proj4dnErrGr, proj4ErrBand);

  TGraphAsymmErrors* proj4ErrBandRatio = (TGraphAsymmErrors*) proj4ErrBand->Clone();
  proj4ErrBandRatio->SetFillColor(kYellow);

  for (int i=0;i<proj4ErrBandRatio->GetN();i++) {
    proj4ErrBandRatio->GetY()[i] *= 1./proj4nom->GetBinContent(i+1);
    proj4ErrBandRatio->GetEYhigh()[i] *= 1./proj4nom->GetBinContent(i+1);
    proj4ErrBandRatio->GetEYlow()[i] *= 1./proj4nom->GetBinContent(i+1);
  }

  pad_1->SetLogx();
  pad_1->cd();
  proj4M60->SetMarkerColor(kRed);
  proj4M60->SetLineColor(kRed);
  proj4asj->SetMarkerColor(kBlue);
  proj4asj->SetLineColor(kBlue);
  proj4up->SetMarkerStyle(22);
  proj4dn->SetMarkerStyle(23);
  proj4nom->SetMarkerSize(0.8);
  proj4asj->SetMarkerSize(0.8);
  proj4M60->SetMarkerSize(0.8);
  proj4up->SetMarkerSize(0.8);
  proj4dn->SetMarkerSize(0.8);
  proj4nom->Draw("P E");
  proj4ErrBand->SetFillColor(kYellow);
  proj4ErrBand->Draw("same E3");
  proj4nom->GetYaxis()->SetTitle("fake factor");
  proj4nom->GetXaxis()->SetLabelSize(0);
  proj4nom->GetYaxis()->SetLabelSize(0.06);
  proj4nom->GetYaxis()->SetNdivisions(515);
  proj4nom->GetYaxis()->SetTitleSize(0.07);
  proj4nom->GetYaxis()->SetTitleOffset(0.95);
  proj4nom->GetYaxis()->SetRangeUser(0.1,0.7);
  proj4nom->GetXaxis()->SetLabelSize(0);
  proj4up->Draw("same P E X0");
  proj4dn->Draw("same P E X0");
  proj4M60->Draw("same P E X0");
  proj4asj->Draw("same P E X0");
  proj4nom->Draw("same P E");
  ATLASLabel(0.18,0.85,"Internal",1);
  myText(0.18,0.79,1,"2.01 < |#eta| < 2.47");
  leg.Draw();
  pad_2->SetLogx();
  pad_2->cd();
  TH1D* proj4M60r = (TH1D*) proj4M60->Clone(); proj4M60r->Divide(proj4nom);
  TH1D* proj4upr = (TH1D*) proj4up->Clone(); proj4upr->Divide(proj4nom);
  TH1D* proj4dnr = (TH1D*) proj4dn->Clone(); proj4dnr->Divide(proj4nom);
  TH1D* proj4asjr = (TH1D*) proj4asj->Clone(); proj4asjr->Divide(proj4nom);
  proj4M60r->SetLineWidth(0);
  proj4upr->SetLineWidth(0);
  proj4dnr->SetLineWidth(0);
  proj4asjr->SetLineWidth(0);
  proj4M60r->Draw("PE0X0");
  proj4ErrBandRatio->Draw("E3");
  proj4M60r->Draw("same PE0X0");
  proj4upr->Draw("same PE0X0");
  proj4dnr->Draw("same PE0X0");
  proj4asjr->Draw("same PE0X0");
  proj4M60r->GetXaxis()->SetLabelSize(0.15);
  proj4M60r->GetYaxis()->SetLabelSize(0.13);
  proj4M60r->GetYaxis()->SetDecimals();
  proj4M60r->GetXaxis()->SetTitle("p_{T} [GeV]");
  proj4M60r->GetYaxis()->SetTitle("ratio");
  proj4M60r->GetXaxis()->SetTitleSize(0.15);
  proj4M60r->GetXaxis()->SetTitleOffset(1.0);
  proj4M60r->GetYaxis()->SetTitleSize(0.15);
  proj4M60r->GetYaxis()->SetTitleOffset(0.40);
  proj4M60r->GetYaxis()->SetRangeUser(0.5,1.5);
  proj4M60r->GetYaxis()->SetNdivisions(106);
  proj4M60r->GetXaxis()->SetNoExponent();
  proj4M60r->GetXaxis()->SetMoreLogLabels();
  proj4M60r->SetMarkerSize(0.8);
  proj4upr->SetMarkerSize(0.8);
  proj4dnr->SetMarkerSize(0.8);
  proj4asjr->SetMarkerSize(0.8);
  gPad->RedrawAxis("g");
  c3.Print("fakeProjSys4.eps");



  TH2D* finalFFhist = (TH2D*) fr1->Clone();
  TH2D* finalFFhistUp = (TH2D*) fr1->Clone();
  TH2D* finalFFhistDn = (TH2D*) fr1->Clone();
  finalFFhist->SetName("FF");
  finalFFhistUp->SetName("FFup");
  finalFFhistDn->SetName("FFdn");
  for(int pt_i = 1; pt_i <= finalFFhist->GetNbinsX(); pt_i++){
    finalFFhist->SetBinContent(pt_i,1, proj1ErrBand->GetY()[pt_i-1] );
    finalFFhist->SetBinContent(pt_i,2, 0 );
    finalFFhist->SetBinContent(pt_i,3, proj3ErrBand->GetY()[pt_i-1] );
    finalFFhist->SetBinContent(pt_i,4, proj4ErrBand->GetY()[pt_i-1] );

    finalFFhistUp->SetBinContent(pt_i,1, proj1ErrBand->GetY()[pt_i-1]+proj1ErrBand->GetEYhigh()[pt_i-1] );
    finalFFhistUp->SetBinContent(pt_i,2, 0 );
    finalFFhistUp->SetBinContent(pt_i,3, proj3ErrBand->GetY()[pt_i-1]+proj3ErrBand->GetEYhigh()[pt_i-1] );
    finalFFhistUp->SetBinContent(pt_i,4, proj4ErrBand->GetY()[pt_i-1]+proj4ErrBand->GetEYhigh()[pt_i-1] );

    finalFFhistDn->SetBinContent(pt_i,1, proj1ErrBand->GetY()[pt_i-1]-proj1ErrBand->GetEYlow()[pt_i-1] );
    finalFFhistDn->SetBinContent(pt_i,2, 0 );
    finalFFhistDn->SetBinContent(pt_i,3, proj3ErrBand->GetY()[pt_i-1]-proj3ErrBand->GetEYlow()[pt_i-1] );
    finalFFhistDn->SetBinContent(pt_i,4, proj4ErrBand->GetY()[pt_i-1]-proj4ErrBand->GetEYlow()[pt_i-1] );
  }
  TFile *outfile = new TFile("fakeFactorSys.root","RECREATE");
  finalFFhist->Write();
  finalFFhistUp->Write();
  finalFFhistDn->Write();

}