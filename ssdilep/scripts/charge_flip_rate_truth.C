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

void charge_flip_rate_truth(int rebin =1){
  
  double m_ptBins[12] = {30., 34., 38., 43., 48., 55., 62., 70., 100., 140., 200., 1/0.};

  TFile* flipRates = new TFile("chargeFlipRates_h_ZWindowAS_nominal_Zee221.root");
  TH1F* flipRatePt = (TH1F*) flipRates->Get("flipRatePth_ZWindowAS_nominal_Zee221");
  TH1F* flipRateEta = (TH1F*) flipRates->Get("flipRateEtah_ZWindowAS_nominal_Zee221");

  TFile* AllElePow   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_all_BeyondZAS_PowhegTrueCHF.root");
  TFile* CHF2ElePow   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf2_BeyondZAS_PowhegTrueCHF.root");
  TFile* CHF4ElePow   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf4_BeyondZAS_PowhegTrueCHF.root");

  TFile* AllEle   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_all_ZWindowAS_SherpaTrueCHF.root");
  TFile* CHF2Ele   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf2_ZWindowAS_SherpaTrueCHF.root");
  TFile* CHF4Ele   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf4_ZWindowAS_SherpaTrueCHF.root");

  TH2F* hAllElePow = (TH2F*) AllElePow->Get("h_BeyondZAS_nominal_Zee");
  TH2F* hCHF2ElePow = (TH2F*) CHF2ElePow->Get("h_BeyondZAS_nominal_Zee");
  TH2F* hCHF4ElePow = (TH2F*) CHF4ElePow->Get("h_BeyondZAS_nominal_Zee"); 

  TH2F* hAllEle = (TH2F*) AllEle->Get("h_ZWindowAS_nominal_Zee221");
  TH2F* hCHF2Ele = (TH2F*) CHF2Ele->Get("h_ZWindowAS_nominal_Zee221");
  TH2F* hCHF4Ele = (TH2F*) CHF4Ele->Get("h_ZWindowAS_nominal_Zee221");

  // partial charge-flip rates
  hCHF2Zpeak = (TH2F*) hCHF2Ele->Clone();
  hCHF4Zpeak = (TH2F*) hCHF4Ele->Clone();
  hALLZpeak = (TH2F*) hAllEle->Clone();
  hCHF2Zpeak->Rebin2D(1,3);
  hCHF4Zpeak->Rebin2D(1,3);
  hALLZpeak->Rebin2D(1,3);
  hCHF2Zpeak->Divide(hALLZpeak);
  hCHF4Zpeak->Divide(hALLZpeak);
  hCHF2Beyond = (TH2F*) hCHF2ElePow->Clone();
  hCHF4Beyond = (TH2F*) hCHF4ElePow->Clone();
  hALLBeyond = (TH2F*) hAllElePow->Clone();
  hCHF2Beyond->Rebin2D(1,3);
  hCHF4Beyond->Rebin2D(1,3);
  hALLBeyond->Rebin2D(1,3);
  hCHF2Beyond->Divide(hALLBeyond);
  hCHF4Beyond->Divide(hALLBeyond);

  hCHF2Zpeak->Divide(hCHF2Beyond);
  hCHF4Zpeak->Divide(hCHF4Beyond);


  // chf2 / chf4 ratio vs pt - eta
  TH2F* CHFratios = (TH2F*) hCHF2Ele->Clone();
  TH2F* CHFratios4 = (TH2F*) hCHF4Ele->Clone();
  CHFratios->RebinY(15);
  CHFratios->RebinX(1);
  CHFratios4->RebinY(15);
  CHFratios4->RebinX(1);
  CHFratios->Divide(CHFratios4);

  TH2F* CHFratiosPow = (TH2F*) hCHF2ElePow->Clone();
  TH2F* CHFratios4Pow = (TH2F*) hCHF4ElePow->Clone();
  CHFratiosPow->RebinY(15);
  CHFratiosPow->RebinX(1);
  CHFratios4Pow->RebinY(15);
  CHFratios4Pow->RebinX(1);
  CHFratiosPow->Divide(CHFratios4Pow);

  TH2F* hCHF = (TH2F*) hCHF2Ele->Clone();
  hCHF->Add(hCHF4Ele);
  hCHF->Divide(hAllEle);
  
  TH2D* hCHFClosure = (TH2D*) hCHF->Clone();

  for (int i = 1; i<=hCHF->GetNbinsX(); i++){
    for (int j =1; j<=hCHF->GetNbinsY(); j++){
      if ( flipRatePt->GetBinCenter(i)!=hCHFClosure->GetXaxis()->GetBinCenter(i) ) std::cout << "error 1" << std::endl;
      if ( flipRateEta->GetBinCenter(j)!=hCHFClosure->GetYaxis()->GetBinCenter(j) ) std::cout << "error 2" << std::endl;
      double flipRate = flipRatePt->GetBinContent(i)*flipRateEta->GetBinContent(j);
      hCHFClosure->SetBinContent(i,j,hCHFClosure->GetBinContent(i,j)/flipRate);
      hCHFClosure->SetBinError(i,j,hCHFClosure->GetBinError(i,j)/flipRate);
    }
  }
 
  std::vector<TH1D*> CHF2Slices;
  std::vector<TH1D*> CHF4Slices;
  std::vector<TH1D*> CHFSlices;

  int NX = flipRatePt->GetNbinsX();

  TH1D* projAll = hAllEle->ProjectionY("projAll",1,NX+1);
  TH1D* projCHF2 = hCHF2Ele->ProjectionY("projCHF2",1,NX+1);
  TH1D* projCHF4 = hCHF4Ele->ProjectionY("projCHF4",1,NX+1);
  TH1D* projCHF  = (TH1D*) projCHF2->Clone();
  projCHF->Add(projCHF4);

  projCHF2->Divide(projAll);
  projCHF4->Divide(projAll);
  projCHF->Divide(projAll);

  for(int i=1; i<=NX; i=i+rebin){
    std::cout << "slice: " << i << " to " << std::min(i+rebin-1,NX) << std::endl;
    std::ostringstream name;
    name << "proj" << i;
    TH1D* projAll = hAllEle->ProjectionY(name.str().c_str(), i,std::min(i+rebin-1,NX));
    name << "chf2";
    TH1D* projCHF2 = hCHF2Ele->ProjectionY(name.str().c_str(), i,std::min(i+rebin-1,NX));
    name << "chf4";
    TH1D* projCHF4 = hCHF4Ele->ProjectionY(name.str().c_str(), i,std::min(i+rebin-1,NX));

    TH1D* projCHF = (TH1D*) projCHF2->Clone();
    projCHF->Add(projCHF4);

    projCHF2->Divide(projAll);
    projCHF4->Divide(projAll);
    projCHF ->Divide(projAll);

    CHF2Slices.push_back(projCHF2);
    CHF4Slices.push_back(projCHF4);
    CHFSlices .push_back(projCHF );
  }

  TLegend* leg = new TLegend(0.20,0.35,0.4,0.75);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  leg->SetFillStyle(0);
  leg->SetTextSize(0.042);
  leg->AddEntry(flipRateEta,"#font[42]{f(#eta) LH fit}","lpe0");
  std::ostringstream leg0; leg0 << "#font[42]{normalized p_{T} [" << m_ptBins[0] << ", " << m_ptBins[1+rebin-1]<< "] slice}";
  leg->AddEntry(CHFSlices.at(0),leg0.str().c_str(),"lpe0");

  TLegend* leg2 = new TLegend(0.20,0.67,0.4,0.82);
  leg2->SetBorderSize(0);
  leg2->SetFillColor(0);
  leg2->SetFillStyle(0);
  leg2->SetTextSize(0.045);

  TCanvas c1("c1","c1",600,600);
  c1.SetLogy();
  CHF2Slices.at(0)->Scale(1./CHF2Slices.at(0)->Integral());
  CHF2Slices.at(0)->Draw();
  for(int i=1; i<CHF2Slices.size(); i++){
    CHF2Slices.at(i)->Scale(1./CHF2Slices.at(i)->Integral());
    CHF2Slices.at(i)->Draw("same");
    CHF2Slices.at(i)->SetLineColor(i);
    CHF2Slices.at(i)->SetMarkerColor(i);
  }
  std::ostringstream name1; name1 << "chf2slicesZpeak" << rebin << ".eps";
  c1.Print(name1.str().c_str());

  TCanvas c2("c2","c2",600,600);
  c2.SetLogy();
  CHF4Slices.at(0)->Scale(1./CHF4Slices.at(0)->Integral());
  CHF4Slices.at(0)->Draw();
  for(int i=1; i<CHF4Slices.size(); i++){
    double area = 0;
    for(int k = 1; k <= CHF4Slices.at(i)->GetNbinsX(); k++){
      area += CHF4Slices.at(i)->GetBinContent(k)*CHF4Slices.at(i)->GetBinWidth(k);
    }
    CHF4Slices.at(i)->Scale(1./area);
    CHF4Slices.at(i)->Draw("same");
    CHF4Slices.at(i)->SetLineColor(i);
    CHF4Slices.at(i)->SetMarkerColor(i);
  }
  std::ostringstream name2; name2 << "chf4slicesZpeak" << rebin << ".eps";
  c2.Print(name2.str().c_str());

  TCanvas c3("c3","c3",600,600);
  double area = 0;
  for(int k = 1; k <= CHFSlices.at(0)->GetNbinsX(); k++){
    area += CHFSlices.at(0)->GetBinContent(k)*CHFSlices.at(0)->GetBinWidth(k);
  }
  CHFSlices.at(0)->Scale(1./area);
  CHFSlices.at(0)->Draw();
  CHFSlices.at(0)->SetLineColor(kBlue+4);
  CHFSlices.at(0)->SetMarkerColor(kBlue+4);
  for(int i=1; i<CHFSlices.size(); i++){
    double area = 0;
    for(int k = 1; k <= CHFSlices.at(i)->GetNbinsX(); k++){
      area += CHFSlices.at(i)->GetBinContent(k)*CHFSlices.at(i)->GetBinWidth(k);
    }
    CHFSlices.at(i)->Scale(1./area);
    CHFSlices.at(i)->Draw("same");
    CHFSlices.at(i)->SetLineColor(kBlue+4-i);
    CHFSlices.at(i)->SetMarkerColor(kBlue+4-i);
    std::ostringstream legName; legName << "#font[42]{normalized p_{T} [" << m_ptBins[rebin*i] << ", " << m_ptBins[std::min(rebin*(i+1),NX)]<< "] slice}";
    leg->AddEntry(CHFSlices.at(i),legName.str().c_str(),"lpe0");
  }
  flipRateEta->Draw("same");
  flipRateEta->SetLineColor(kRed);
  flipRateEta->SetMarkerColor(kRed);
  flipRateEta->SetMarkerSize(1.2);
  flipRateEta->SetLineWidth(2);
  CHFSlices.at(0)->GetXaxis()->SetTitle("abs(#eta)");
  CHFSlices.at(0)->GetYaxis()->SetTitle("f(#eta)");
  CHFSlices.at(0)->GetYaxis()->SetRangeUser(0,3.);
  ATLASLabel(0.20,0.90,"internal",1);
  myText(0.20,0.83,1,"#sqrt{s} = 13 TeV, 18.2 fb^{-1}, Sherpa Zee");
  leg->Draw();
  std::ostringstream name3; name3 << "chfslicesZpeak" << rebin << ".eps";
  c3.Print(name3.str().c_str());
  CHFSlices.at(0)->GetYaxis()->SetRangeUser(5e-3,1e2);
  c3.SetLogy();
  std::ostringstream name32; name32 << "chfslicesZpeak_LOG" << rebin << ".eps";
  c3.Print(name32.str().c_str());

  TCanvas c3a("c3a","c3a",600,600);
  double yratiomin;
  double yratiomax;
  if (rebin < 2){
    yratiomin = 0.5;
    yratiomax = 2;
  }
  else if (rebin < 4){
    yratiomin = 0.5;
    yratiomax = 2;
  }
  else {
    yratiomin = 0.5;
    yratiomax = 2;    
  }
  drawComparison2(&c3a,&CHFSlices,(TH1D*)flipRateEta,"f(#eta)","abs(#eta)",0,2.5,0,2.5,false,yratiomin,yratiomax,true,0,true,"PE0",true);
  ATLASLabel(0.18,0.83,"internal",1);
  myText(0.18,0.78,1,"#sqrt{s} = 13 TeV, Sherpa Zee");
  leg->Draw();
  gROOT->ProcessLine("pad_1->cd();");
  flipRateEta->Draw("same EP0");
  c3a.Print( (std::string("improved") + name32.str()).c_str() );

  TCanvas c4("c4","c4",600,600);
  c4.SetLogy();
  projCHF2->Draw();
  projCHF2->SetLineColor(2);
  projCHF2->SetMarkerColor(2);
  projCHF4->Draw("same");
  projCHF4->SetLineColor(4);
  projCHF4->SetMarkerColor(4);
  projCHF->Draw("same");
  std::ostringstream name4; name4 << "chfProjAllZpeak.eps";
  ATLASLabel(0.20,0.90,"internal",1);
  myText(0.20,0.83,1,"#sqrt{s} = 13 TeV, 18.2 fb^{-1}, Sherpa Zee");
  leg2->AddEntry(projCHF,"#font[42]{total charge-flip}","lpe0");
  leg2->AddEntry(projCHF2,"#font[42]{charge-flip type-2}","lpe0");
  leg2->AddEntry(projCHF4,"#font[42]{charge-flip type-4}","lpe0");
  projCHF2->GetXaxis()->SetTitle("#eta");
  projCHF2->GetYaxis()->SetTitle("charge-flip rate");
  projCHF2->GetYaxis()->SetRangeUser(1e-4,1e-1);
  leg2->Draw();
  c4.Print(name4.str().c_str());

  TCanvas c5("c5","c5",800,600);
  c5.SetLogx();
  c5.SetRightMargin(0.2);
  hCHF->Draw("colz");
  hCHF->SetMarkerSize(0.4);
  hCHF->GetXaxis()->SetTitle("true charge-flip rate           p_{T} [GeV]");
  hCHF->GetYaxis()->SetTitle("#eta");
  hCHF->GetXaxis()->SetMoreLogLabels();
  hCHF->GetXaxis()->SetNoExponent();
  c5.Print("chf2D.eps");

  TCanvas c6("c6","c6",800,600);
  c6.SetLogx();
  c6.SetRightMargin(0.15);
  hCHFClosure->Draw("colz text e");
  hCHFClosure->SetMarkerSize(0.6);
  c6.Print("chf2DComparison.eps");

  TCanvas c7("c7","c7",800,600);
  c7.SetLogx();
  c7.SetRightMargin(0.1);
  CHFratios->Draw("colz text e");
  CHFratios->SetMarkerSize(0.8);
  CHFratios->GetXaxis()->SetTitle("Z Peak type-2/type-4 ratio       p_{T} [GeV]");
  CHFratios->GetYaxis()->SetTitle("#eta");
  CHFratios->GetXaxis()->SetMoreLogLabels();
  CHFratios->GetXaxis()->SetNoExponent();
  c7.Print("chfRatioSherpa.eps");

  TCanvas c8("c8","c8",800,600);
  c8.SetLogx();
  c8.SetRightMargin(0.1);
  CHFratiosPow->Draw("colz text e");
  CHFratiosPow->SetMarkerSize(0.8);
  CHFratiosPow->GetXaxis()->SetTitle("m(ee) > 130 GeV type-2/type-4 ratio       p_{T} [GeV]");
  CHFratiosPow->GetYaxis()->SetTitle("#eta");
  CHFratiosPow->GetXaxis()->SetMoreLogLabels();
  CHFratiosPow->GetXaxis()->SetNoExponent();
  c8.Print("chfRatioPowheg.eps");

  TCanvas c9("c9","c9",800,600);
  c9.SetLogx();
  c9.SetRightMargin(0.1);
  CHFRatioRatio = (TH2F*) CHFratiosPow->Clone();
  CHFRatioRatio->Divide(CHFratios);
  CHFRatioRatio->Draw("colz text e");
  CHFRatioRatio->SetMarkerSize(0.8);
  CHFRatioRatio->GetXaxis()->SetTitle("Beyond Z ratio / Z peak ratio       p_{T} [GeV]");
  CHFRatioRatio->GetYaxis()->SetTitle("#eta");
  CHFRatioRatio->GetXaxis()->SetMoreLogLabels();
  CHFRatioRatio->GetXaxis()->SetNoExponent();
  c9.Print("chfRatioRatio.eps");

  TCanvas c10("c10","c10",800,600);
  c10.SetLogx();
  c10.SetRightMargin(0.1);
  hCHF2Zpeak->Draw("colz text e");
  hCHF2Zpeak->SetMarkerSize(0.8);
  hCHF2Zpeak->GetXaxis()->SetTitle("type-2 flip rate  Z peak / beyond Z       p_{T} [GeV]");
  hCHF2Zpeak->GetYaxis()->SetTitle("#eta");
  hCHF2Zpeak->GetXaxis()->SetMoreLogLabels();
  hCHF2Zpeak->GetXaxis()->SetNoExponent();
  c10.Print("chfType2Comparison.eps");

  TCanvas c11("c11","c11",800,600);
  c11.SetLogx();
  c11.SetRightMargin(0.1);
  hCHF4Zpeak->Draw("colz text e");
  hCHF4Zpeak->SetMarkerSize(0.6);
  hCHF4Zpeak->GetXaxis()->SetTitle("type-4 flip rate  Z peak / beyond Z       p_{T} [GeV]");
  hCHF4Zpeak->GetYaxis()->SetTitle("#eta");
  hCHF4Zpeak->GetXaxis()->SetMoreLogLabels();
  hCHF4Zpeak->GetXaxis()->SetNoExponent();
  c11.Print("chfType4Comparison.eps");
  
}