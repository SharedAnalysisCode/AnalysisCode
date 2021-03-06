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

void mergeBins(TH2* histo2D, int binX1, int binY1, int binX2, int binY2){
  double sum = histo2D->GetBinContent(binX1 ,binY1) + histo2D->GetBinContent(binX2,binY2);
  double sum_err = TMath::Sqrt( TMath::Power(histo2D->GetBinError(binX1 ,binY1),2) + TMath::Power(histo2D->GetBinError(binX2,binY2),2) );
  histo2D->SetBinContent(binX1, binY1, sum );
  histo2D->SetBinContent(binX2 ,binY2, sum );
  histo2D->SetBinError(binX1, binY1, sum_err );
  histo2D->SetBinError(binX2, binY2, sum_err );
}

void fake_rate_measurement_helper(std::string var = "nominal", std::string var3 = "_FFnominal", std::string var4 = ""){
  
  double mcscale = 1.0;
  if (var=="mcup") mcscale = 1.10;
  else if (var=="mcdn") mcscale = 0.90;

  std::string var2 = var;
  if (var=="mcup") var2 = "nominal";
  else if (var=="mcdn") var2 = "nominal";

  std::cout << var << std::endl;

  
  TFile* nominal_t   = new TFile(("/afs/f9.ijs.si/home/miham/AnalysisCode/run/FFele_HN_v2_002/hists_el_t_2D_pt_Ceta_FakeEnrichedRegion-" + var2 + var3 + ".root").c_str());
  TFile* nominal_l   = new TFile(("/afs/f9.ijs.si/home/miham/AnalysisCode/run/FFele_HN_v2_002/hists_el_l_2D_pt_Ceta_FakeEnrichedRegion-" + var2 + var3 + ".root").c_str());
  TFile* nominal_sl  = new TFile(("/afs/f9.ijs.si/home/miham/AnalysisCode/run/FFele_HN_v2_002/hists_el_sl_2D_pt_Ceta_FakeEnrichedRegion-" + var2 + var3 + ".root").c_str());
  
  std::cout << var << " " << var3 << " " << var4 << std::endl;
  std::cout << nominal_t << " " << nominal_l << " " << nominal_sl << std::endl;

  TH2F* nominal_t_wenu = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Wenu221").c_str());
  TH2F* nominal_t_Wtaunu = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Wtaunu221").c_str());
  TH2F* nominal_t_zee = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Zee221").c_str());
  TH2F* nominal_t_Ztautau = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Ztautau221").c_str());
  TH2F* nominal_t_ttbar = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ttbar_dilep").c_str());
  TH2F* nominal_t_diboson = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_dibosonSherpaAll").c_str());
  TH2F* nominal_t_singletop = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_singletop").c_str());
  TH2F* nominal_t_MC = (TH2F*) nominal_t_wenu->Clone("twenu");
  TH2F* nominal_t_data = (TH2F*) nominal_t->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_data").c_str());
  TH2F* nominal_t_data_minus = (TH2F*) nominal_t_data->Clone("tdata");

  std::cout << nominal_t_wenu << std::endl;
  std::cout << nominal_t_Wtaunu << std::endl;
  std::cout << nominal_t_zee << std::endl;
  std::cout << nominal_t_Ztautau << std::endl;
  std::cout << nominal_t_ttbar << std::endl;
  std::cout << nominal_t_diboson << std::endl;
  std::cout << nominal_t_singletop << std::endl;

  TH2F* nominal_l_wenu = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Wenu221").c_str());
  TH2F* nominal_l_Wtaunu = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Wtaunu221").c_str());
  TH2F* nominal_l_zee = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Zee221").c_str());
  TH2F* nominal_l_Ztautau = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Ztautau221").c_str());
  TH2F* nominal_l_ttbar = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ttbar_dilep").c_str());
  TH2F* nominal_l_diboson = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_dibosonSherpaAll").c_str());
  TH2F* nominal_l_singletop = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_singletop").c_str());
  TH2F* nominal_l_MC = (TH2F*) nominal_l_wenu->Clone("lwenu");
  TH2F* nominal_l_data = (TH2F*) nominal_l->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_data").c_str());
  TH2F* nominal_l_data_minus = (TH2F*) nominal_l_data->Clone("ldata");

  TH2F* nominal_sl_wenu = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Wenu221").c_str());
  TH2F* nominal_sl_Wtaunu = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Wtaunu221").c_str());
  TH2F* nominal_sl_zee = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Zee221").c_str());
  TH2F* nominal_sl_Ztautau = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_Ztautau221").c_str());
  TH2F* nominal_sl_ttbar = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_ttbar_dilep").c_str());
  TH2F* nominal_sl_diboson = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_dibosonSherpaAll").c_str());
  TH2F* nominal_sl_singletop = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_singletop").c_str());
  TH2F* nominal_sl_MC = (TH2F*) nominal_sl_wenu->Clone("slwenu");
  TH2F* nominal_sl_data = (TH2F*) nominal_sl->Get(("h_FakeEnrichedRegion-" + var2 + "_nominal_data").c_str());
  TH2F* nominal_sl_data_minus = (TH2F*) nominal_sl_data->Clone("sldata");

  nominal_t_MC->Add(nominal_t_zee);
  nominal_t_MC->Add(nominal_t_Ztautau);
  nominal_t_MC->Add(nominal_t_Wtaunu);
  nominal_t_MC->Add(nominal_t_ttbar);
  nominal_t_MC->Add(nominal_t_diboson);
  nominal_t_MC->Add(nominal_t_singletop);
  nominal_t_data_minus->Add(nominal_t_MC,-1.*mcscale);

  nominal_l_MC->Add(nominal_l_zee);
  nominal_l_MC->Add(nominal_l_Ztautau);
  nominal_l_MC->Add(nominal_l_Wtaunu);
  nominal_l_MC->Add(nominal_l_ttbar);
  nominal_l_MC->Add(nominal_l_diboson);
  nominal_l_MC->Add(nominal_l_singletop);
  nominal_l_data_minus->Add(nominal_t_MC,-1.*mcscale);

  nominal_sl_MC->Add(nominal_sl_zee);
  nominal_sl_MC->Add(nominal_sl_Ztautau);
  nominal_sl_MC->Add(nominal_sl_Wtaunu);
  nominal_sl_MC->Add(nominal_sl_ttbar);
  nominal_sl_MC->Add(nominal_sl_diboson);
  nominal_sl_MC->Add(nominal_sl_singletop);
  nominal_sl_data_minus->Add(nominal_sl_MC,-1.*mcscale);

  // rebin
  mergeBins(nominal_t_data_minus,nominal_t_data_minus->GetNbinsX(),4,nominal_t_data_minus->GetNbinsX()-1,4);
  mergeBins(nominal_l_data_minus,nominal_l_data_minus->GetNbinsX(),4,nominal_l_data_minus->GetNbinsX()-1,4);
  mergeBins(nominal_sl_data_minus,nominal_sl_data_minus->GetNbinsX(),4,nominal_sl_data_minus->GetNbinsX()-1,4);
  // double sum_t = nominal_t_data_minus->GetBinContent(nominal_t_data_minus->GetNbinsX() ,4) + nominal_t_data_minus->GetBinContent(nominal_t_data_minus->GetNbinsX()-1,4);
  // double sum_err_t = TMath::Sqrt( TMath::Power(nominal_t_data_minus->GetBinError(nominal_t_data_minus->GetNbinsX() ,4),2) + TMath::Power(nominal_t_data_minus->GetBinError(nominal_t_data_minus->GetNbinsX()-1,4),2) );
  // nominal_t_data_minus->SetBinContent(nominal_t_data_minus->GetNbinsX()  ,4, sum_t );
  // nominal_t_data_minus->SetBinContent(nominal_t_data_minus->GetNbinsX()-1,4, sum_t );
  // nominal_t_data_minus->SetBinError(nominal_t_data_minus->GetNbinsX()  ,4, sum_err_t );
  // nominal_t_data_minus->SetBinError(nominal_t_data_minus->GetNbinsX()-1,4, sum_err_t );
  // double sum_l = nominal_l_data_minus->GetBinContent(nominal_l_data_minus->GetNbinsX() ,4) + nominal_l_data_minus->GetBinContent(nominal_l_data_minus->GetNbinsX()-1,4);
  // double sum_err_l = TMath::Sqrt( TMath::Power(nominal_l_data_minus->GetBinError(nominal_l_data_minus->GetNbinsX() ,4),2) + TMath::Power(nominal_l_data_minus->GetBinError(nominal_l_data_minus->GetNbinsX()-1,4),2) );
  // nominal_l_data_minus->SetBinContent(nominal_l_data_minus->GetNbinsX()  ,4, sum_l );
  // nominal_l_data_minus->SetBinContent(nominal_l_data_minus->GetNbinsX()-1,4, sum_l );
  // nominal_l_data_minus->SetBinError(nominal_l_data_minus->GetNbinsX()  ,4, sum_err_l );
  // nominal_l_data_minus->SetBinError(nominal_l_data_minus->GetNbinsX()-1,4, sum_err_l );
  // double sum_sl = nominal_sl_data_minus->GetBinContent(nominal_sl_data_minus->GetNbinsX() ,4) + nominal_sl_data_minus->GetBinContent(nominal_sl_data_minus->GetNbinsX()-1,4);
  // double sum_err_sl = TMath::Sqrt( TMath::Power(nominal_sl_data_minus->GetBinError(nominal_sl_data_minus->GetNbinsX() ,4),2) + TMath::Power(nominal_sl_data_minus->GetBinError(nominal_sl_data_minus->GetNbinsX()-1,4),2) );
  // nominal_sl_data_minus->SetBinContent(nominal_sl_data_minus->GetNbinsX()  ,4, sum_sl );
  // nominal_sl_data_minus->SetBinContent(nominal_sl_data_minus->GetNbinsX()-1,4, sum_sl );
  // nominal_sl_data_minus->SetBinError(nominal_sl_data_minus->GetNbinsX()  ,4, sum_err_sl );
  // nominal_sl_data_minus->SetBinError(nominal_sl_data_minus->GetNbinsX()-1,4, sum_err_sl );

  if (0 and var=="TwoJets"){
    mergeBins(nominal_t_data_minus, 4,1,5,1);
    mergeBins(nominal_l_data_minus, 4,1,5,1);
    mergeBins(nominal_sl_data_minus,4,1,5,1);
    mergeBins(nominal_t_data_minus, 6,1,7,1);
    mergeBins(nominal_l_data_minus, 6,1,7,1);
    mergeBins(nominal_sl_data_minus,6,1,7,1);
    mergeBins(nominal_t_data_minus, 8,1,9,1);
    mergeBins(nominal_l_data_minus, 8,1,9,1);
    mergeBins(nominal_sl_data_minus,8,1,9,1);

    mergeBins(nominal_t_data_minus, 4,3,5,3);
    mergeBins(nominal_l_data_minus, 4,3,5,3);
    mergeBins(nominal_sl_data_minus,4,3,5,3);
    mergeBins(nominal_t_data_minus, 6,3,7,3);
    mergeBins(nominal_l_data_minus, 6,3,7,3);
    mergeBins(nominal_sl_data_minus,6,3,7,3);
    mergeBins(nominal_t_data_minus, 8,3,9,3);
    mergeBins(nominal_l_data_minus, 8,3,9,3);
    mergeBins(nominal_sl_data_minus,8,3,9,3);
    mergeBins(nominal_t_data_minus, 10,3,11,3);
    mergeBins(nominal_l_data_minus, 10,3,11,3);
    mergeBins(nominal_sl_data_minus,10,3,11,3);

    mergeBins(nominal_t_data_minus, 4,4,5,4);
    mergeBins(nominal_l_data_minus, 4,4,5,4);
    mergeBins(nominal_sl_data_minus,4,4,5,4);
    mergeBins(nominal_t_data_minus, 6,4,7,4);
    mergeBins(nominal_l_data_minus, 6,4,7,4);
    mergeBins(nominal_sl_data_minus,6,4,7,4);
    mergeBins(nominal_t_data_minus, 8,4,9,4);
    mergeBins(nominal_l_data_minus, 8,4,9,4);
    mergeBins(nominal_sl_data_minus,8,4,9,4);
    mergeBins(nominal_t_data_minus, 10,4,11,4);
    mergeBins(nominal_l_data_minus, 10,4,11,4);
    mergeBins(nominal_sl_data_minus,10,4,11,4);
  }

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

  leg = TLegend(0.5,0.5,0.9,0.7);
  leg.SetBorderSize(0);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetTextSize(0.045);
  leg.AddEntry(projX1,"0 < |#eta| < 1.37","pe0");
  leg.AddEntry(projX3,"1.52 < |#eta| < 2.01","pe0");
  leg.AddEntry(projX4,"2.01 < |#eta| < 2.47","pe0");

  TFile* outFile = new TFile(("fakeRate-"+var+var4+".root").c_str(),"RECREATE");
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
  projX1->GetYaxis()->SetRangeUser(0,3.0);
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
  myText(0.18,0.79,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");

  TCanvas c3("c3","c3",600,600);
  c3.SetLogx();
  projX1FF->GetXaxis()->SetNoExponent();
  projX1FF->GetXaxis()->SetMoreLogLabels();
  projX1FF->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1FF->GetYaxis()->SetTitle("fake factor");
  projX1FF->Draw("pe0");
  projX1FF->GetYaxis()->SetRangeUser(0,3.0);
  projX3FF->Draw("same");
  projX4FF->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);
  myText(0.18,0.84,1,"fake factor ( f/(1-f) )");
  myText(0.18,0.79,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");


  TCanvas c4("c4","c4",600,600);
  c4.SetLogx();
  projX1ff->GetYaxis()->SetRangeUser(0,3.0);
  projX1ff->GetXaxis()->SetNoExponent();
  projX1ff->GetXaxis()->SetMoreLogLabels();
  projX1ff->GetXaxis()->SetTitle("p_{T} [GeV]");
  projX1ff->GetYaxis()->SetTitle("fake factor");
  projX1ff->Draw("pe0");
  projX1ff->GetYaxis()->SetRangeUser(0,3.);
  projX3ff->Draw("same");
  projX4ff->Draw("same");
  leg.Draw();
  ATLASLabel(0.18,0.89,"Internal",1);
  myText(0.18,0.84,1,"fake factor ( T/SL )");
  myText(0.18,0.79,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");


  c1.Print(("fakeRate2D-"+var+".eps").c_str());
  c2.Print(("fakeRate-"+var+".eps").c_str());
  c3.Print(("fakeFactor-"+var+".eps").c_str());
  c4.Print(("fakeFactorDirect-"+var+".eps").c_str());

  
}

void fake_rate_measurement(){

  fake_rate_measurement_helper("nominal");
  fake_rate_measurement_helper("MET60");
  fake_rate_measurement_helper("MET100");
  // fake_rate_measurement_helper("nominal","_FFNoLooseTrig","-NoLooseTrig");
  fake_rate_measurement_helper("InclusiveJets");
  fake_rate_measurement_helper("mcup");
  fake_rate_measurement_helper("mcdn");

  TFile* nominalFile = new TFile("fakeRate-nominal.root","READ");
  TFile* MET60File = new TFile("fakeRate-MET60.root","READ");
  TFile* MET100File = new TFile("fakeRate-MET100.root","READ");
  // TFile* ASjetFile = new TFile("fakeRate-nominal-NoLooseTrig.root","READ");
  TFile* TwoJetsFile = new TFile("fakeRate-InclusiveJets.root","READ");
  TFile* mcupfile = new TFile("fakeRate-mcup.root","READ");
  TFile* mcdnfile = new TFile("fakeRate-mcdn.root","READ");

  TH2F* fr1 = (TH2F*) nominalFile->Get("fakeFactor-nominal");
  TH2F* fr2 = (TH2F*) MET60File->Get("fakeFactor-MET60");
  // TH2F* fr3 = (TH2F*) ASjetFile->Get("fakeFactor-nominal");
  TH2F* fr4 = (TH2F*) mcupfile->Get("fakeFactor-mcup");
  TH2F* fr5 = (TH2F*) mcdnfile->Get("fakeFactor-mcdn");
  TH2F* fr6 = (TH2F*) MET100File->Get("fakeFactor-MET100");
  TH2F* fr7 = (TH2F*) TwoJetsFile->Get("fakeFactor-InclusiveJets");


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

  TH1D* temp7 = new TH1D();
  temp7->SetMarkerColor(kRed+2);
  temp7->SetLineColor(kRed+2);
  TH1D* temp8 = new TH1D();
  temp8->SetMarkerColor(kBlue+2);
  temp8->SetLineColor(kBlue+2);


  leg = TLegend(0.18,0.40,0.4,0.75);
  leg.SetBorderSize(0);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetTextSize(0.045);
  leg.AddEntry(temp1,"#font[42]{nominal}","pe0");
  leg.AddEntry(temp2,"#font[42]{MET < 60}","pe0");
  leg.AddEntry(temp7,"#font[42]{MET < 100}","pe0");
  // leg.AddEntry(temp3,"#font[42]{No LooseLH Trig}","pe0");
  leg.AddEntry(temp8,"#font[42]{Inclusive}","pe0");
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
  TH1D* proj1M100 = fr6->ProjectionX("proj1M100",1,1);
  // TH1D* proj1asj = fr3->ProjectionX("proj1asj",1,1);
  TH1D* proj1twoj = fr7->ProjectionX("proj1twoj",1,1);
  TH1D* proj1up = fr4->ProjectionX("proj1up",1,1);
  TH1D* proj1dn = fr5->ProjectionX("proj1dn",1,1);
  proj1M60->SetLineWidth(0);
  proj1M100->SetLineWidth(0);
  proj1up->SetLineWidth(0);
  proj1dn->SetLineWidth(0);
  // proj1asj->SetLineWidth(0);
  proj1twoj->SetLineWidth(1);

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
  TGraphErrors*  proj1M100ErrGr =  TH1TOTGraph(proj1M100);
  // TGraphErrors*  proj1asjErrGr =  TH1TOTGraph(proj1asj);
  TGraphErrors*  proj1twojErrGr =  TH1TOTGraph(proj1twoj);
  TGraphErrors*  proj1upErrGr =  TH1TOTGraph(proj1up);
  TGraphErrors*  proj1dnErrGr =  TH1TOTGraph(proj1dn);

  TGraphAsymmErrors* proj1ErrBand = myMakeBand(proj1StatGr, proj1StatErrUpGr, proj1StatErrDnGr);
  // myAddtoBand(proj1M60ErrGr, proj1ErrBand);
  myAddtoBand(proj1M100ErrGr, proj1ErrBand);
  // myAddtoBand(proj1asjErrGr, proj1ErrBand);
  myAddtoBand(proj1twojErrGr, proj1ErrBand);
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
  proj1M100->SetMarkerColor(kRed+2);
  proj1M100->SetLineColor(kRed+2);
  // proj1asj->SetMarkerColor(kBlue);
  // proj1asj->SetLineColor(kBlue);
  proj1twoj->SetMarkerColor(kBlue+2);
  proj1twoj->SetLineColor(kBlue+2);
  proj1up->SetMarkerStyle(22);
  proj1dn->SetMarkerStyle(23);
  proj1nom->SetMarkerSize(0.8);
  // proj1asj->SetMarkerSize(0.8);
  proj1twoj->SetMarkerSize(0.8);
  proj1M60->SetMarkerSize(0.8);
  proj1M100->SetMarkerSize(0.8);
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
  proj1nom->GetYaxis()->SetRangeUser(0.,3.0);
  proj1nom->GetXaxis()->SetLabelSize(0);
  proj1up->Draw("same P E X0");
  proj1dn->Draw("same P E X0");
  proj1M60->Draw("same P E X0");
  proj1M100->Draw("same P E X0");
  // proj1asj->Draw("same P E X0");
  proj1twoj->Draw("same P E");
  proj1nom->Draw("same P E");
  ATLASLabel(0.18,0.85,"Internal",1);
  myText(0.18,0.80,1,"0.0 < |#eta| < 1.37");
  myText(0.18,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  leg.Draw();
  pad_2->SetLogx();
  pad_2->cd();
  TH1D* proj1M60r = (TH1D*) proj1M60->Clone(); proj1M60r->Divide(proj1nom);
  TH1D* proj1M100r = (TH1D*) proj1M100->Clone(); proj1M100r->Divide(proj1nom);
  TH1D* proj1upr = (TH1D*) proj1up->Clone(); proj1upr->Divide(proj1nom);
  TH1D* proj1dnr = (TH1D*) proj1dn->Clone(); proj1dnr->Divide(proj1nom);
  // TH1D* proj1asjr = (TH1D*) proj1asj->Clone(); proj1asjr->Divide(proj1nom);
  TH1D* proj1twojr = (TH1D*) proj1twoj->Clone(); proj1twojr->Divide(proj1nom);
  proj1M60r->SetLineWidth(0);
  proj1M100r->SetLineWidth(0);
  proj1upr->SetLineWidth(0);
  proj1dnr->SetLineWidth(0);
  // proj1asjr->SetLineWidth(0);
  proj1twojr->SetLineWidth(1);
  proj1M60r->Draw("PE0X0");
  proj1ErrBandRatio->Draw("E3");
  proj1M60r->Draw("same PE0X0");
  proj1M100r->Draw("same PE0X0");
  proj1upr->Draw("same PE0X0");
  proj1dnr->Draw("same PE0X0");
  // proj1asjr->Draw("same PE0X0");
  proj1twojr->Draw("same PE0X0");
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
  // proj1asjr->SetMarkerSize(0.8);
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
  TH1D* proj3M100 = fr6->ProjectionX("proj3M100",3,3);
  // TH1D* proj3asj = fr3->ProjectionX("proj3asj",3,3);
  TH1D* proj3twoj = fr7->ProjectionX("proj3twoj",3,3);
  TH1D* proj3up = fr4->ProjectionX("proj3up",3,3);
  TH1D* proj3dn = fr5->ProjectionX("proj3dn",3,3);
  proj3M60->SetLineWidth(0);
  proj3M100->SetLineWidth(0);
  proj3up->SetLineWidth(0);
  proj3dn->SetLineWidth(0);
  // proj3asj->SetLineWidth(0);
  proj3twoj->SetLineWidth(1);

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
  TGraphErrors*  proj3M100ErrGr =  TH1TOTGraph(proj3M100);
  // TGraphErrors*  proj3asjErrGr =  TH1TOTGraph(proj3asj);
  TGraphErrors*  proj3twojErrGr =  TH1TOTGraph(proj3twoj);
  TGraphErrors*  proj3upErrGr =  TH1TOTGraph(proj3up);
  TGraphErrors*  proj3dnErrGr =  TH1TOTGraph(proj3dn);

  TGraphAsymmErrors* proj3ErrBand = myMakeBand(proj3StatGr, proj3StatErrUpGr, proj3StatErrDnGr);
  // myAddtoBand(proj3M60ErrGr, proj3ErrBand);
  myAddtoBand(proj3M100ErrGr, proj3ErrBand);
  // myAddtoBand(proj3asjErrGr, proj3ErrBand);
  myAddtoBand(proj3twojErrGr, proj3ErrBand);
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
  proj3M100->SetMarkerColor(kRed+2);
  proj3M100->SetLineColor(kRed+2);
  // proj3asj->SetMarkerColor(kBlue);
  // proj3asj->SetLineColor(kBlue);
  proj3twoj->SetMarkerColor(kBlue+2);
  proj3twoj->SetLineColor(kBlue+2);
  proj3up->SetMarkerStyle(22);
  proj3dn->SetMarkerStyle(23);
  proj3nom->SetMarkerSize(0.8);
  // proj3asj->SetMarkerSize(0.8);
  proj3twoj->SetMarkerSize(0.8);
  proj3M60->SetMarkerSize(0.8);
  proj3M100->SetMarkerSize(0.8);
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
  proj3nom->GetYaxis()->SetRangeUser(0.,3.0);
  proj3nom->GetXaxis()->SetLabelSize(0);
  proj3up->Draw("same P E X0");
  proj3dn->Draw("same P E X0");
  proj3M60->Draw("same P E X0");
  proj3M100->Draw("same P E X0");
  // proj3asj->Draw("same P E X0");
  proj3twoj->Draw("same P E");
  proj3nom->Draw("same P E");
  ATLASLabel(0.18,0.85,"Internal",1);
  myText(0.18,0.80,1,"1.52 < |#eta| < 2.01");
  myText(0.18,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  leg.Draw();
  pad_2->SetLogx();
  pad_2->cd();
  TH1D* proj3M60r = (TH1D*) proj3M60->Clone(); proj3M60r->Divide(proj3nom);
  TH1D* proj3M100r = (TH1D*) proj3M100->Clone(); proj3M100r->Divide(proj3nom);
  TH1D* proj3upr = (TH1D*) proj3up->Clone(); proj3upr->Divide(proj3nom);
  TH1D* proj3dnr = (TH1D*) proj3dn->Clone(); proj3dnr->Divide(proj3nom);
  // TH1D* proj3asjr = (TH1D*) proj3asj->Clone(); proj3asjr->Divide(proj3nom);
  TH1D* proj3twojr = (TH1D*) proj3twoj->Clone(); proj3twojr->Divide(proj3nom);
  proj3M60r->SetLineWidth(0);
  proj3M100r->SetLineWidth(0);
  proj3upr->SetLineWidth(0);
  proj3dnr->SetLineWidth(0);
  // proj3asjr->SetLineWidth(0);
  proj3twojr->SetLineWidth(1);
  proj3M60r->Draw("PE0X0");
  proj3ErrBandRatio->Draw("E3");
  proj3M60r->Draw("same PE0X0");
  proj3M100r->Draw("same PE0X0");
  proj3upr->Draw("same PE0X0");
  proj3dnr->Draw("same PE0X0");
  // proj3asjr->Draw("same PE0X0");
  proj3twojr->Draw("same PE0X0");
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
  // proj3asjr->SetMarkerSize(0.8);
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
  TH1D* proj4M100 = fr6->ProjectionX("proj4M100",4,4);
  // TH1D* proj4asj = fr3->ProjectionX("proj4asj",4,4);
  TH1D* proj4twoj = fr7->ProjectionX("proj4twoj",4,4);
  TH1D* proj4up = fr4->ProjectionX("proj4up",4,4);
  TH1D* proj4dn = fr5->ProjectionX("proj4dn",4,4);
  proj4M60->SetLineWidth(0);
  proj4M100->SetLineWidth(0);
  proj4up->SetLineWidth(0);
  proj4dn->SetLineWidth(0);
  // proj4asj->SetLineWidth(0);
  proj4twoj->SetLineWidth(1);

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
  TGraphErrors*  proj4M100ErrGr =  TH1TOTGraph(proj4M100);
  // TGraphErrors*  proj4asjErrGr =  TH1TOTGraph(proj4asj);
  TGraphErrors*  proj4twojErrGr =  TH1TOTGraph(proj4twoj);
  TGraphErrors*  proj4upErrGr =  TH1TOTGraph(proj4up);
  TGraphErrors*  proj4dnErrGr =  TH1TOTGraph(proj4dn);

  TGraphAsymmErrors* proj4ErrBand = myMakeBand(proj4StatGr, proj4StatErrUpGr, proj4StatErrDnGr);
  // myAddtoBand(proj4M60ErrGr, proj4ErrBand);
  myAddtoBand(proj4M100ErrGr, proj4ErrBand);
  // myAddtoBand(proj4asjErrGr, proj4ErrBand);
  myAddtoBand(proj4twojErrGr, proj4ErrBand);
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
  proj4M100->SetMarkerColor(kRed+2);
  proj4M100->SetLineColor(kRed+2);
  // proj4asj->SetMarkerColor(kBlue);
  // proj4asj->SetLineColor(kBlue);
  proj4twoj->SetMarkerColor(kBlue+2);
  proj4twoj->SetLineColor(kBlue+2);
  proj4up->SetMarkerStyle(22);
  proj4dn->SetMarkerStyle(23);
  proj4nom->SetMarkerSize(0.8);
  // proj4asj->SetMarkerSize(0.8);
  proj4twoj->SetMarkerSize(0.8);
  proj4M60->SetMarkerSize(0.8);
  proj4M100->SetMarkerSize(0.8);
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
  proj4nom->GetYaxis()->SetRangeUser(0.,3.0);
  proj4nom->GetXaxis()->SetLabelSize(0);
  proj4up->Draw("same P E X0");
  proj4dn->Draw("same P E X0");
  proj4M60->Draw("same P E X0");
  proj4M100->Draw("same P E X0");
  // proj4asj->Draw("same P E X0");
  proj4twoj->Draw("same P E");
  proj4nom->Draw("same P E");
  ATLASLabel(0.18,0.85,"Internal",1);
  myText(0.18,0.80,1,"2.01 < |#eta| < 2.47");
  myText(0.18,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");  
  leg.Draw();
  pad_2->SetLogx();
  pad_2->cd();
  TH1D* proj4M60r = (TH1D*) proj4M60->Clone(); proj4M60r->Divide(proj4nom);
  TH1D* proj4M100r = (TH1D*) proj4M100->Clone(); proj4M100r->Divide(proj4nom);
  TH1D* proj4upr = (TH1D*) proj4up->Clone(); proj4upr->Divide(proj4nom);
  TH1D* proj4dnr = (TH1D*) proj4dn->Clone(); proj4dnr->Divide(proj4nom);
  // TH1D* proj4asjr = (TH1D*) proj4asj->Clone(); proj4asjr->Divide(proj4nom);
  TH1D* proj4twojr = (TH1D*) proj4twoj->Clone(); proj4twojr->Divide(proj4nom);
  proj4M60r->SetLineWidth(0);
  proj4M100r->SetLineWidth(0);
  proj4upr->SetLineWidth(0);
  proj4dnr->SetLineWidth(0);
  // proj4asjr->SetLineWidth(0);
  proj4twojr->SetLineWidth(1);
  proj4M60r->Draw("PE0X0");
  proj4ErrBandRatio->Draw("E3");
  proj4M60r->Draw("same PE0X0");
  proj4M100r->Draw("same PE0X0");
  proj4upr->Draw("same PE0X0");
  proj4dnr->Draw("same PE0X0");
  // proj4asjr->Draw("same PE0X0");
  proj4twojr->Draw("same PE0X0");
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
  // proj4asjr->SetMarkerSize(0.8);
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