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

void vgamma_study(){
  
  TFile* zgamma1 = new TFile("/afs/f9.ijs.si/home/miham/Diboson36_13/nominal/Sherpa_CT10_eegammaPt10_35.root");
  TFile* zgamma2 = new TFile("/afs/f9.ijs.si/home/miham/Diboson36_13/nominal/Sherpa_CT10_eegammaPt35_70.root");
  TFile* zgamma3 = new TFile("/afs/f9.ijs.si/home/miham/Diboson36_13/nominal/Sherpa_CT10_eegammaPt70_140.root");
  TFile* zgamma4 = new TFile("/afs/f9.ijs.si/home/miham/Diboson36_13/nominal/Sherpa_CT10_eegammaPt140.root");

  TH1D* h_zgamma1 = (TH1D*) zgamma1->Get("regions/diboson-CR/ExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");
  TH1D* h_zgamma2 = (TH1D*) zgamma2->Get("regions/diboson-CR/ExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");
  TH1D* h_zgamma3 = (TH1D*) zgamma3->Get("regions/diboson-CR/ExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");
  TH1D* h_zgamma4 = (TH1D*) zgamma4->Get("regions/diboson-CR/ExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");

  TH1D* hf_zgamma1 = (TH1D*) zgamma1->Get("regions/diboson-CR-fakes/FailExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");
  TH1D* hf_zgamma2 = (TH1D*) zgamma2->Get("regions/diboson-CR-fakes/FailExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");
  TH1D* hf_zgamma3 = (TH1D*) zgamma3->Get("regions/diboson-CR-fakes/FailExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");
  TH1D* hf_zgamma4 = (TH1D*) zgamma4->Get("regions/diboson-CR-fakes/FailExactlyThreeTightEleMediumLLHisolLoose/event/h_invMass");

  h_zgamma1->Rebin(20);
  h_zgamma2->Rebin(20);
  h_zgamma3->Rebin(20);
  h_zgamma4->Rebin(20);
  hf_zgamma1->Rebin(20);
  hf_zgamma2->Rebin(20);
  hf_zgamma3->Rebin(20);
  hf_zgamma4->Rebin(20);

  h_zgamma1->SetLineColor(kRed);
  h_zgamma2->SetLineColor(kRed);
  h_zgamma3->SetLineColor(kRed);
  h_zgamma4->SetLineColor(kRed);
  h_zgamma1->SetMarkerColor(kRed);
  h_zgamma2->SetMarkerColor(kRed);
  h_zgamma3->SetMarkerColor(kRed);
  h_zgamma4->SetMarkerColor(kRed);

  h_zgamma1->GetXaxis()->SetRangeUser(80,200);
  hf_zgamma1->GetXaxis()->SetRangeUser(80,200);
  h_zgamma2->GetXaxis()->SetRangeUser(80,200);
  hf_zgamma2->GetXaxis()->SetRangeUser(80,200);
  h_zgamma3->GetXaxis()->SetRangeUser(80,200);
  hf_zgamma3->GetXaxis()->SetRangeUser(80,200);
  h_zgamma4->GetXaxis()->SetRangeUser(80,200);
  hf_zgamma4->GetXaxis()->SetRangeUser(80,200);

  leg = TLegend(0.2,0.58,0.3,0.72);
  leg.SetBorderSize(0);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetTextSize(0.045);
  leg.AddEntry(h_zgamma1,"#font[42]{Tight Z#gamma (TTT)}","pe0");
  leg.AddEntry(hf_zgamma1,"#font[42]{Fake Factor Z#gamma (F#timesTTL+F#timesTLT+...+F^{3}#timesLLL)}","pe0");


  TCanvas* c1 = new TCanvas("c1","c1",600,600);
  c1->cd();
  drawComparison2(c1,h_zgamma1,hf_zgamma1,"Entries [arb.]","m(e^{#pm}e^{#pm})",0,14,80,200,false,0,3);
  ATLASLabel(0.20,0.83,"internal",1);
  myText(0.20,0.78,1,"#sqrt{s} = 13 TeV, Sherpa_CT10_eegammaPt10_35");
  myText(0.20,0.73,1,"diboson CR");
  leg.Draw();

  TCanvas* c2 = new TCanvas("c2","c2",600,600);
  c2->cd();
  drawComparison2(c2,h_zgamma2,hf_zgamma2,"Entries [arb.]","m(e^{#pm}e^{#pm})",0,30,80,200,false,0,3);
  ATLASLabel(0.20,0.83,"internal",1);
  myText(0.20,0.78,1,"#sqrt{s} = 13 TeV, Sherpa_CT10_eegammaPt35_70");
  myText(0.20,0.73,1,"diboson CR");
  leg.Draw();

  TCanvas* c3 = new TCanvas("c3","c3",600,600);
  c3->cd();
  drawComparison2(c3,h_zgamma3,hf_zgamma3,"Entries [arb.]","m(e^{#pm}e^{#pm})",0,120,80,200,false,0,3);
  ATLASLabel(0.20,0.83,"internal",1);
  myText(0.20,0.78,1,"#sqrt{s} = 13 TeV, Sherpa_CT10_eegammaPt70_140");
  myText(0.20,0.73,1,"diboson CR");
  leg.Draw();

  TCanvas* c4 = new TCanvas("c4","c4",600,600);
  c4->cd();
  drawComparison2(c4,h_zgamma4,hf_zgamma4,"Entries [arb.]","m(e^{#pm}e^{#pm})",0,120,80,200,false,0,3);
  ATLASLabel(0.20,0.83,"internal",1);
  myText(0.20,0.78,1,"#sqrt{s} = 13 TeV, Sherpa_CT10_eegammaPt140");
  myText(0.20,0.73,1,"diboson CR");
  leg.Draw();

  c1->Print("Zgamma10-35.eps");
  c2->Print("Zgamma35-70.eps");
  c3->Print("Zgamma70-140.eps");
  c4->Print("Zgamma140.eps");


  
}